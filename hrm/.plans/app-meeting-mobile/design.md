# Design (tóm tắt) — App Meeting trên di động

**Sản phẩm:** bộ thiết kế giao diện cho `TPE_APP` (Flutter) — phân hệ Meeting.
**Không phải task code**: đầu ra là file `.pen` + PDF/PNG bàn giao, không sửa `hrm-api` / `hrm-client`.

| | |
|---|---|
| File thiết kế | `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen` |
| Bàn giao | `~/Documents/demo giao dien/pencil_design/exports/` (v11 · 16/09/2026) |
| Quy mô | **50 artboard**, khung bản đồ 2825 × 24617 |
| Nhánh code đối chiếu | `tpe-develop-assign` (cả 2 repo) |

## Mục tiêu

Đưa toàn bộ nghiệp vụ Meeting của bản web lên điện thoại 393px, **bám 100% logic web** — chỉ đổi
cách trình bày, không đổi luật nghiệp vụ. Mọi chỗ buộc phải khác web đều ghi rõ lý do và đánh dấu
cần chốt lại.

## Các quyết định lớn đã chốt

1. **Điều hướng Hub** — màn chi tiết meeting là bảng điều khiển liệt kê 9 khối, bấm từng khối mở màn con.
   Không bê 4 tab ngang của web sang điện thoại. Kéo theo nhu cầu **API lưu từng phần** (`api-luu-tung-phan.md`).
2. **Phạm vi dữ liệu = của tôi** — app chỉ quản lý meeting mình **chủ trì hoặc tham gia**; bỏ bộ lọc
   Công ty / Phòng ban. Tab cấp 1 tách theo **đúng vai trò**, hai tab rời nhau.
3. **Chọn khách hàng / người liên hệ / dự án TKT** có màn riêng + lối **thêm nhanh**, vì trên điện thoại
   không thể mở modal bảng nhiều cột như web.
4. **Thông báo chỉ một kiểu** — dải nằm trong luồng, 3 loại màu (đỏ lỗi · xám khoá · xanh thông tin).
   Không dùng toast đè. Hộp thoại hỏi ý kiến vẫn là popup.
5. **Dấu `*` bắt buộc theo trạng thái từng màn**, khác với thanh *Mức độ hoàn thiện hồ sơ* (đếm theo
   bộ khối cần cho Hoàn thành).
6. **Không viết chú thích logic vào trong khung điện thoại** — phần giải thích nằm ở caption artboard;
   ghi chú kỹ thuật cho dev nằm ở khối `DEV NOTE` bên ngoài khung máy (4 màn: 01 · 04a · 06 · 21).

## Chốt với khách — 14/10/2026

| # | Câu hỏi | Chốt |
|---|---|---|
| 1 | Màn 06 chọn 1 hay nhiều Giải pháp / Hạng mục | **Meeting chỉ chọn tới cấp DỰ ÁN** → bỏ hẳn phần chọn Giải pháp / Hạng mục khỏi app |
| 2 | Meeting gắn nhiều dự án | Hết vướng sau câu 1: màn 06 chỉ còn danh sách dự án TKT đã gắn (không còn cây giải pháp theo từng dự án) |
| 3 | Màn 42 — địa chỉ xuất hoá đơn | Mặc định **chép từ địa chỉ chính, cho phép sửa** |
| 4 | Màn 44 — liên hệ tạo từ app tự vào Thành phần KH | **Có** (như web) |
| 5 | Màn 18 — xoá dòng NGƯỜI 1 | **Làm theo web** (giữ icon xoá) |
| 6 | Phiếu tổng hợp kết quả meeting #11130 | **Có đưa vào app** — cần vẽ khối trên Hub + màn nhập + màn xem |
| 7 | Nút Xem file (màn 11 · 19 · 36 · 38) | **Chỉ xem PDF + ảnh**; loại khác chỉ có Tải xuống |
| 8 | `customerMeetingHistory()` | **Thay** điều kiện `created_by` bằng "user đang đăng nhập có trong thành phần", không cộng thêm |
| 9 | Biên bản tạo task giao người xử lý | **Bổ sung sau** — bỏ khỏi trạng thái Blocked |

## Khảo sát web — Meeting theo đối tượng (nhánh `gop_db`, 14/10/2026)

Nguồn: `hrm-api` 59537031f + `hrm-client` 3ea829c51 (09/10) · design web `.plans/gop-db/meeting-theo-doi-tuong/design.md`.

- **Cấu hình nằm ở LOẠI MEETING**: `meeting_types.target_type` = 1 Dự án TKT · 2 Hợp đồng · NULL không. Bỏ checkbox "Meeting theo dự án".
- **Bắt buộc ở MỌI lượt lưu, kể cả Lưu nháp** (`ValidatesMeetingTarget` chạy trong `after()`, không xét status):
  loại TKT → `projects` ≥ 1 ("Vui lòng chọn Dự án TKT.") · loại HĐ → `contract_id` ("Vui lòng chọn Hợp đồng.").
  ⇒ App PHẢI có ô đối tượng ngay ở màn 03 Tạo meeting, không thể để sang màn con của Hub.
- **Dự án TKT**: chọn NHIỀU · nguồn `GET assign/prospective-projects/getForMeeting?meeting_id=` · tiến trình 2→10 · phạm vi: mình tạo / làm giải pháp / hỗ trợ · chọn dự án → tự điền KH.
- **Hợp đồng**: chọn MỘT · nguồn `GET assign/contracts/for-meeting?customer_id=&include_id=` · mọi trạng thái trừ Đang tạo, Đã thanh lý · không lọc quyền, KHÔNG trả tiền/SĐT ·
  đã chọn KH → chỉ HĐ của KH đó; chọn HĐ trước → tự điền KH + TÊN người liên hệ (SĐT để trống) · đổi KH khác → bỏ HĐ · đổi loại khỏi HĐ → bỏ HĐ.
  Dòng hiển thị: `Mã HĐ` + tên KH + badge trạng thái (`status_name` / `status_color` do BE trả).
- **Hiện ô** Dự án TKT khi loại = TKT HOẶC meeting đã có dự án HOẶC tạo từ dự án (khi đó dấu `*` chỉ có ở loại TKT). Ô HĐ hiện khi loại = HĐ hoặc meeting đã có HĐ.
- **Đối tượng cũ đã ra khỏi dải trạng thái vẫn giữ** khi sửa meeting (BE chỉ kiểm giá trị mới chọn thêm).
- Màn xem: HĐ = mã (bấm mở HĐ) + tên KH + badge trạng thái. Lịch sử meeting ghi "Hợp đồng: cũ → mới".
- ⚠️ Web VẪN giữ Giải pháp / Hạng mục theo từng dự án (`solution_id`, `solution_module_id`). App bỏ theo chốt #1 → app gửi lại payload `projects` PHẢI giữ nguyên 2 cột này của dự án đã gắn, không được xoá dữ liệu nhập từ web.
- Phát hiện phụ: web có tab **Nhiệm vụ** (#11456, chỉ ở màn chi tiết) — nhiều khả năng là logic "tạo task" của câu 9, để bổ sung sau.

## Đề xuất — tải danh sách Dự án TKT đồng nhất web + app (14/10/2026, ĐÃ DUYỆT — chưa code BE/FE web)

> Triển khai trên nhánh `gop_db` → theo dõi tại `.plans/gop-db/meeting-chon-du-an-tkt/`.

**Hiện trạng web:** `getForMeeting?per_page=10000` tải MỌI dự án trong phạm vi, mỗi dòng kèm toàn bộ resource
(`RESOURCE_EAGER_RELATIONS` + 5 subquery giải pháp) rồi lọc KH / tìm kiếm ở FE. Lý do tải nặng: chọn dự án là
chép nguyên object vào `form.projects` để tab "Dự án tiền khả thi" có đủ trường. App không thể dùng kiểu này.

**Đề xuất — tách 2 việc: CHỌN (nhẹ, phân trang) và LẤY CHI TIẾT (chỉ dự án vừa chọn)**

1. Endpoint mới `GET assign/prospective-projects/meeting-options` — dùng chung web + app.
   - Tham số: `search` (mã / tên) · `customer_id` · `page` · `per_page` (mặc định 20, trần 50).
   - Điều kiện GIỮ NGUYÊN `getForMeeting`: tiến trình 2–10 + (người tạo / người làm giải pháp / người hỗ trợ).
     Tách thành 1 scope dùng chung (vd `scopeSelectableForMeetingBy($userId)`) để 2 endpoint không lệch nhau.
   - Trả gọn: `id, code, name, customer_id, customer_code, customer_name, status, status_name, status_color, is_parent`.
     KHÔNG eager load, KHÔNG subquery giải pháp, KHÔNG ngân sách.
   - Sắp id giảm dần; có `meta` phân trang. Lọc KH và tìm kiếm làm ở BE (thay lọc FE).
   - ⚠️ Tên `meeting-options` đã dùng cho chiều ngược lại (#11142: meeting cho form dự án) → đặt tên khác, vd `options-for-meeting`.
2. Dự án ĐÃ GẮN không cần nằm trong danh sách chọn: lấy từ chi tiết meeting (`form.projects` đã có mã + tên) và
   hiện thành chip đã chọn. Bỏ cơ chế `meeting_id` / include ở danh sách. BE vẫn cho lưu dự án cũ ngoài dải
   (`ValidatesMeetingTarget` chỉ kiểm dự án mới thêm) — không đổi.
3. Chọn thêm 1 dự án → gọi chi tiết đúng dự án đó để điền tab "Dự án tiền khả thi" (web). Dùng endpoint riêng có
   cùng điều kiện phạm vi (vd `GET .../options-for-meeting/{id}`), KHÔNG dùng `show` vì `show` theo quyền xem dự án
   — người hỗ trợ không có quyền xem dự án sẽ bị 403. App không cần bước này (đã bỏ Giải pháp / Hạng mục).
4. FE web: `MultiSearchPicker` hiện chỉ lọc tại chỗ (prop `items`). Cần chế độ tìm phía server: gõ → debounce 300ms
   + huỷ request cũ → gọi endpoint (1); cuộn cuối → trang kế. Đây là component DÙNG CHUNG → hỏi trước khi sửa,
   hoặc tạo component mới riêng. Chưa có component tìm phía server nào trong `components/` để bám.
5. `getForMeeting` cũ: giữ tới khi web chuyển xong, sau đó gỡ (còn chỗ khác gọi thì kiểm trước).

**App (màn Chọn dự án TKT):** ô tìm (mã / tên) + danh sách thẻ phân trang cuộn, mỗi thẻ: mã · tên · KH · badge
tiến trình (màu BE trả). Chọn nhiều, chip đã chọn ở đầu màn. Đã chọn KH ở meeting → truyền `customer_id`.
Có nút Thêm nhanh dự án TKT (màn 47).

## Tài liệu liên quan

| File | Nội dung |
|---|---|
| `plan.md` | 5 phase + **danh sách việc chuyển cho dev** + 6 câu cần chốt với khách |
| `chon-khach-hang-va-lien-he.md` | **Spec chi tiết** — 17 mục, ghi từng vòng sửa kèm căn cứ tra từ source web |
| `api-luu-tung-phan.md` | Đề xuất nhóm endpoint lưu từng phần + danh mục Lý do huỷ |
| `docs/superpowers/specs/2026-09-16-app-meeting-mobile-design.md` | Spec kỹ thuật gom đầu mối |
