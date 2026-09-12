# Đề xuất API lưu từng phần — Meeting trên app mobile

**Ngày:** 10/09/2026
**Bối cảnh:** thiết kế app `TPE_APP` (Flutter) cho phân hệ Meeting — file `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen`
**Trạng thái:** đề xuất, CHƯA làm

---

## 1. Vì sao cần

App dùng điều hướng **Hub**: màn chi tiết liệt kê 8 khối (Thông tin chung · Dự án · Thành phần · Tài liệu chuẩn bị · Biên bản · Tài liệu biên bản · Khảo sát · Kết luận), bấm từng khối mở một màn con riêng. Đây là kiểu điều hướng bắt buộc trên điện thoại — không thể bê 4 tab ngang của web sang màn 393px.

Kiểu này chỉ chạy trơn khi **mỗi màn con lưu được phần của nó**.

## 2. Hiện trạng bản web

| Endpoint | Dùng khi |
|---|---|
| `POST assign/meeting` | Tạo mới |
| `POST assign/meeting/{id}` | Cập nhật |
| `POST assign/meeting/{id}/change-status` | **Chỉ dùng cho Huỷ** (`status=4` + `cancel_reason`) |

`MeetingForm.getFormData()` gửi `{...this.form, ...extra}` — **toàn bộ form một cục**: thông tin chung, thành phần công ty + khách hàng, điểm danh, biên bản, tài liệu, khảo sát, kết luận.

Bốn nút `Lưu nháp / Lên lịch hẹn / Đã chốt / Hoàn thành` thực chất **cùng một API**, chỉ khác `status` (0/1/2/3); riêng Lên lịch gửi thêm `send_notification: 1`.

→ **Không có API lưu từng phần.**

## 3. Vấn đề nếu bê nguyên lên mobile

1. **Payload lớn** — mỗi lần sửa 1 ô ghi chú điểm danh vẫn đẩy cả biên bản + tài liệu + khảo sát lên server. Nhân viên đi thị trường dùng 3G/4G yếu.
2. **Mất dữ liệu** — điền 3 khối rồi app bị kill / hết pin: mất sạch vì chưa lần nào chạm server.
3. **Ghi đè chéo** — thư ký ghi biên bản trong lúc trưởng phòng sửa thành phần: ai lưu sau ghi đè toàn bộ của người kia, kể cả phần mình không đụng tới.
4. **Điểm danh tại chỗ** — thao tác cần lưu ngay từng người, không đợi bấm Lưu cả form.

## 4. Đề xuất endpoint

Giữ nguyên 3 endpoint cũ (web vẫn dùng), **bổ sung** nhóm lưu từng phần:

| Màn con trên app | Endpoint đề xuất | Payload |
|---|---|---|
| Thông tin chung | `PATCH assign/meeting/{id}/info` | `name`, `is_customer_meeting`, `meeting_type_id`, `mode_id`, `start_date`, `end_date`, `location`, `online_link`, `purpose`, `host_employee_id`, `customer_id`, `customer_contact_*` |
| Dự án tiền khả thi | `PATCH assign/meeting/{id}/projects` | `projects[]` |
| Thành phần tham dự | `PATCH assign/meeting/{id}/members` | `company_members[]`, `customer_members[]` |
| Điểm danh | `PATCH assign/meeting/{id}/attendance` | `attendances[{member_id, attendance_status, attendance_note}]` |
| Biên bản | `PATCH assign/meeting/{id}/reports` | `reports[]` |
| Tài liệu chuẩn bị | `PATCH assign/meeting/{id}/prepare-attachments` | `prepare_attachments[]` |
| Tài liệu biên bản | `PATCH assign/meeting/{id}/attachments` | `attachments[]` |
| Khảo sát nhu cầu KH | `PATCH assign/meeting/{id}/survey` | `has_investment_demand`, `investment_scopes[]`, `investment_demands[]`, `has_maintenance_demand` |
| Kết luận | `PATCH assign/meeting/{id}/conclusion` | `conclusion` |
| Đổi trạng thái | **mở rộng** `POST assign/meeting/{id}/change-status` cho `status` 1/2/3 (hiện chỉ nhận 4) | `status`, `send_notification`, `cancel_reason` |

## 5. Ràng buộc bắt buộc kèm theo

- **Guard đầu hàm, không phải chỉ ẩn nút ở FE**: mỗi endpoint kiểm `can_manage` và trạng thái khoá (`status` 3/4 chặn sửa) NGAY ĐẦU, trả `423 LOCKED` kèm message rõ. Đặt điều kiện trong 1 method của Entity (`isCanEdit()`) rồi dùng lại, không rải `if` khắp controller.
  - ⚠️ Controller nhận `FormRequest` thì `if` đầu hàm **không chạy trước validate** — trường hợp đó phải đưa guard ra **middleware route**.
- **Điểm danh chỉ nhận khi `status = 2`** (đúng như `MeetingAttendance.vue:95`), khác thì trả `422`.
- **Validate cục bộ**: mỗi endpoint chỉ validate phần của nó. Các luật toàn cục vẫn nằm ở `change-status`:
  - Hoàn thành: bắt buộc đã có ≥1 nội dung biên bản
  - Hoàn thành: bắt buộc điểm danh đủ — **họp nội bộ (`is_customer_meeting = 0`) không tính thành phần khách hàng**, nếu không meeting nội bộ sẽ kẹt vĩnh viễn
  - Hoàn thành: bắt buộc có `conclusion`
- **Chống ghi đè chéo**: FE gửi kèm `updated_at` đang giữ; lệch thì trả `409 CONFLICT` để app hỏi người dùng tải lại. Không im lặng ghi đè.
- **Trả về**: bản ghi đã cập nhật của đúng phần đó + `updated_at` mới, để app cập nhật state mà không phải gọi lại API detail.
- **Lịch sử**: mỗi `PATCH` ghi 1 dòng lịch sử đúng nhóm hành động (xem `.claude/skills/entity-history/SKILL.md`).
- **Index**: kiểm index trước khi bàn giao nếu thêm bảng/cột phục vụ nhóm endpoint này.

## 6. Phương án chạy tạm nếu BE chưa kịp

Nút `Lưu` ở màn con gọi `POST assign/meeting/{id}` với **toàn bộ payload** như web. App vẫn chạy đúng, chỉ tốn băng thông và vẫn dính rủi ro ghi đè chéo ở mục 3.3. Khi có API từng phần thì đổi lại, **không phải sửa giao diện** — các nút `Lưu ...` ở từng màn con giữ nguyên.

---

## 7. Danh mục Lý do huỷ (mới — web cũng chưa có)

Chốt 10/09/2026: màn Huỷ meeting đổi từ **1 ô ghi chú tự do** thành **2 ô**:

1. **Lý do huỷ** — select lấy từ **danh mục lý do huỷ** (danh mục dùng chung, sẽ bổ sung trên cả website sau)
2. **Ghi chú huỷ** — textarea nhập thêm, giữ đúng chỗ của `cancel_reason` hiện tại

Hiện web chỉ có ô `cancel_reason` tự do (`BaseConfirmModal` với `input-label="Lý do huỷ (không bắt buộc)"`).

**Cần bổ sung:**

- Bảng danh mục `meeting_cancel_reasons` (id, code, name, is_active, company_id) + màn quản trị danh mục như các danh mục khác của phân hệ Assign
- `GET assign/meeting-cancel-reasons` để app/web nạp option
- `meetings` thêm cột `cancel_reason_id` (FK), **giữ nguyên** `cancel_reason` cho ghi chú tự do — không bỏ cột cũ, dữ liệu lịch sử đang nằm ở đó
- `POST assign/meeting/{id}/change-status` nhận thêm `cancel_reason_id`

**Đã chốt 10/09/2026:** `cancel_reason_id` **BẮT BUỘC** (`required`) — mockup vẽ dấu `*` đỏ ở ô Lý do huỷ. Ô `cancel_reason` (Ghi chú huỷ) vẫn **không bắt buộc**. Lưu ý đây là **thay đổi so với web hiện tại** (đang cho huỷ mà không cần lý do): khi triển khai phải quyết dữ liệu huỷ cũ đang `NULL` xử lý ra sao — đề xuất backfill về một lý do hệ thống `KHAC` thay vì bắt validate ngược dữ liệu lịch sử.

**Áp quy tắc danh mục dùng chung:** lý do đã khoá/ngừng hoạt động vẫn phải hiện ở bản ghi đang dùng nó (kèm 🔒), không được để select trống khi mở lại meeting cũ.
