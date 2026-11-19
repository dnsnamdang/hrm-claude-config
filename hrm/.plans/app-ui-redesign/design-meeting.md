# Design — Phân hệ Meeting trên app (TPE_APP)

Nguồn: thiết kế `meeting-mobile.pen` (52 màn) · API sẵn có của web · nghiệp vụ màn web · bản thiết kế cũ `.plans/app-meeting-mobile/`.

| Tài liệu | Nội dung |
|---|---|
| `meeting-design-screens.md` | Spec từng màn trích từ file thiết kế (bố cục, trường, nút, "CHỐT CHO DEV" nguyên văn) |
| `meeting-api-contract.md` | Hợp đồng API meeting của hrm-api (route, payload, trạng thái, quyền, upload, thông báo, lỗi BE đã thấy) |
| `meeting-web-behavior.md` | Nghiệp vụ màn web (khối, trường bắt buộc theo trạng thái, nút theo trạng thái, khoá) |
| `../app-meeting-mobile/` | Thiết kế cũ (16/09) + đề xuất API lưu từng phần + câu hỏi chờ khách |

## Nguyên tắc

- **Bám 100% luật nghiệp vụ web**, chỉ đổi cách trình bày (Hub + màn con thay cho 4 tab web).
- **Phạm vi dữ liệu = của tôi**: 2 tab rời nhau "Tôi chủ trì" (host = tôi) / "Tôi tham gia" (có trong thành phần công ty, host ≠ tôi). Nháp chỉ người tạo thấy. Không lọc Công ty / Phòng ban.
- **Thông báo trong màn**: 3 loại dải (đỏ lỗi/chặn/đã huỷ · xám khoá/chỉ xem · xanh hướng dẫn), không toast đè. Popup chỉ cho hộp thoại hỏi quyết định.
- **Dấu `*` theo trạng thái** của màn; thanh "Mức độ hoàn thiện hồ sơ" đếm theo bộ khối cần cho Hoàn thành (x/3, có Khảo sát thì x/4).
- Dùng lại các chuẩn đã chốt của app: header `PrimaryAppBar`, loading mẫu E, nút cao 44, skeleton, `NotificationBellButton`, `OverviewHeaderBand`.

## Trạng thái & luồng (theo BE)

0 Đang tạo (nháp) → 1 Lên lịch → 2 Chốt lịch → 3 Hoàn thành; 1/2 → 4 Huỷ (người tạo, trước giờ họp, bắt buộc lý do). Hoàn thành chỉ khi đã tới giờ họp + điểm danh đủ + có biên bản + kết luận (+ khảo sát nếu loại "Họp tìm hiểu & giới thiệu SP"). 3/4 khoá sửa toàn bộ.

## Quyết định đã chốt (22/10/2026)

1. **Danh sách meeting của tôi**: thêm API mới `GET assign/meeting/mine?role=host|member` (không đụng API web).
2. **Cách lưu**: màn con trên Hub gửi cả form qua `POST assign/meeting/{id}` như web — chưa làm API lưu từng phần.
3. **Thứ tự**: M1 khung + tìm cuộc họp → M2 tạo + Hub + hồ sơ → M3 chốt lịch, điểm danh, biên bản, hoàn thành → M4 dự án TKT, khảo sát, KH → M5 Tổng quan + Phòng họp. Mỗi giai đoạn xong cho xem trên simulator.
4. **Lỗi BE nhỏ sửa kèm** khi tới màn dùng: `customer-history` lọc sai người + thêm host_name/end_date; `getListEmployee` thêm company_code; show id không tồn tại → 404.

## Lệch giữa các bản vẽ (xử lý)

- Lý do huỷ: BE đã bắt buộc (`cancel_reason_id`, #11357) → giữ `*` như màn 16.
- Số tiền màn 12/39 vẽ kiểu VN `12.500.000.000 ₫` → app hiển thị chuẩn quốc tế `12,500,000,000` (quy định CLAUDE.md).
- Bottom menu theo màn 00h: Tổng quan · Lịch · [Tạo meeting] · Danh sách · Phòng họp; Báo cáo nằm trong drawer.
- Nền Hub của popup 16/22/23 là bản cũ → dùng Hub thật của đúng trạng thái.


## Quyết định đã chốt (22/10/2026, phiên làm M2–M5)
- **Validate**: app chỉ kiểm định dạng; bắt buộc / nghiệp vụ do BE trả lỗi gắn trường, app tô đỏ ô / khối. BE bổ sung khi Hoàn thành: `reports` (≥1 nội dung), `attendance` (điểm danh đủ), `projects.N.answers` (phiếu thu thập còn câu bắt buộc — luật mới, áp cả web).
- **Báo lỗi lưu**: snackbar tự ẩn + lỗi tại ô / khối đỏ — KHÔNG dùng dải đỏ "Còn n lỗi" (như các form khác của app). Dải chỉ dùng cho trạng thái (đã huỷ, đã hoàn thành, chỉ xem, hạn biên bản).
- **15 Xem biên bản**: PDF do BE dựng (`GET meeting/{id}/print-pdf`, dompdf, cùng mẫu in); app tải về + mở / chia sẻ (share_plus). Không chuyển HTML→PDF trên máy (làm app iOS thoát).
- **42 Thêm nhanh KH**: thêm Mã số thuế + Người đại diện (BE bắt buộc với KH tổ chức), khác thiết kế (thiết kế để MST bổ sung sau).
- **20 Chọn địa điểm**: dùng lại MapPage có sẵn của app; nguồn bản đồ theo cấu hình hệ thống (không có nút gạt Google/OSM như thiết kế).
- **Phòng họp**: app chỉ xem tình trạng phòng; đặt phòng làm trên web.
- **21 Lịch sử meeting KH**: BE lọc theo người đang xem (chủ trì / tham dự) thay cho điều kiện cũ theo người tạo (áp cả popup web).
- **01 Lịch meeting — 2 tab (user chốt 22/10/2026, KHÁC bản vẽ):** "Tôi tham gia" = có tên trong Nhân sự tham gia phía công ty, GỒM CẢ meeting tôi chủ trì (chủ trì luôn nằm trong thành phần) → tab Tham gia ≥ tab Chủ trì. Bản vẽ tách rời 2 tab (Tham gia loại trừ chủ trì) gây hiểu nhầm. 3 chip đếm theo tab đang chọn.
- **Phạm vi "meeting của tôi" (user chốt 23/10/2026):** tôi có tên trong Nhân sự tham gia phía công ty **HOẶC tôi là người tạo** (người tạo có thể không tham gia — thư ký tạo hộ — nhưng vẫn sửa / huỷ / xoá như web). Tab Lịch: Tôi chủ trì = host; Tôi tham gia = có tên trong thành phần.
- **00h Tổng quan — link (user chốt 23/10/2026):** mọi link mở **danh sách trơn** (giao diện tab Danh sách, không tab vai trò / chip, tiêu đề theo dòng bấm) trên phạm vi "meeting của tôi" (`role=all`) và ra ĐÚNG các meeting đang đếm — không dùng API danh sách web vì phạm vi theo quyền xem có thể làm lệch số: dòng "Cần xử lý gấp" → BE trả `meeting_ids`, danh sách lọc `ids` (1 meeting thì mở thẳng chi tiết); 4 số thống kê tháng → lọc tháng + `exclude_draft` (thống kê không tính nháp). `ids` / `exclude_draft` là phạm vi cố định của màn mở ra, "Làm mới" bộ lọc không xoá.
- **Logic Tạo / sửa meeting phải theo web, cách trình bày được khác (user chốt 23/10/2026):**
  - Nháp có đủ 3 nút như web: **Lưu nháp** (0) · **Lên lịch** (1, báo thành viên) · **Chốt lịch** (2, báo thành viên). Lên lịch → Lưu · Chốt lịch. (Bỏ bản cũ "Lên lịch hẹn" nhảy thẳng sang Chốt lịch.)
  - Mỗi dự án TKT chọn được **Giải pháp / Hạng mục** (không bắt buộc) như thẻ dự án bản web: nguồn `GET assign/solutions/getAll?prospective_project_id=`, đổi giải pháp thì xoá hạng mục, có "Bỏ chọn". Payload luôn gửi `solution_id` / `solution_module_id` (kể cả null) — BE thiếu khoá sẽ giữ giá trị cũ, bỏ chọn không ăn.
  - **Thêm nhanh khách hàng** chỉ hiện khi `GET assign/customers/my-permissions` → `create = true` (fail-closed, như web).
  - Hub lưu xong **tải lại chi tiết**, không dùng response của lệnh cập nhật (MeetingTransformer trả `projects` thô, thiếu `prospective_project_id` / giải pháp → lần lưu kế tiếp 400 "Bắt buộc phải nhập").

## Nút + hộp thoại theo chuẩn web (user chốt 23/10/2026)
- Màu: Lưu nháp trắng (SecondaryButton); Lưu · Lên lịch · Chốt lịch · Hoàn thành = màu chính (PrimaryButton) — theo bảng skill button-convention, KHÔNG theo footer web (Chốt lịch cam / Hoàn thành xanh lá).
- Lên lịch / Chốt lịch hỏi xác nhận (skill 6c) — web meeting hiện chưa hỏi.
- Hộp thoại dùng `AppDialog` / `showAppConfirm` chung toàn app. Chi tiết: skill `app-ui-convention`.
