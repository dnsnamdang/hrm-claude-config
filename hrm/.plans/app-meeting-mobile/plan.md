# Plan — App Meeting trên di động (TPE_APP / Flutter)

Phụ trách: @dnsnamdang · File thiết kế: `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen`

> Đây là công việc **THIẾT KẾ**, chưa đụng code `hrm-api` / `hrm-client`.
> Mọi phát hiện cần BE/FE làm đều gom ở mục "Việc chuyển cho dev" bên dưới.

---

## Phase 1 — Bộ màn nền (trước 15/09) ✅

- [x] 42 artboard: 5 bước nghiệp vụ + bộ màn chỉ xem + nhóm ngoại lệ
- [x] 14 component dùng chung `C/*`, accent `#E8972C`
- [x] Trang `00 · Tổng quan luồng` + bản đồ luồng toàn cảnh
- [x] Đề xuất API lưu từng phần → `api-luu-tung-phan.md`

## Phase 2 — Chọn khách hàng & người liên hệ (15/09) ✅

- [x] Màn **41 · Chọn khách hàng** (ô tìm + lọc MST/SĐT, kết quả dạng thẻ)
- [x] Màn **41b · Không tìm thấy khách hàng**
- [x] Màn **42 · Thêm nhanh khách hàng** (rút gọn, chỉ trường bắt buộc)
- [x] Sheet **43 · Chọn người liên hệ** · Sheet **44 · Thêm nhanh người liên hệ**
- [x] Bỏ field Trạng thái meeting khỏi W05 / W25 / W28 / W33
- [x] Khối tóm tắt KH đã chọn (Mã KH · MST · SĐT · Địa chỉ) + nút ✕ bỏ chọn
- [x] Bổ sung ô Người liên hệ còn thiếu ở màn 03

## Phase 3 — Bổ sung theo phản hồi (15/09) ✅

- [x] Bỏ logic "KH đã có người đăng ký" (không suy diễn từ web)
- [x] Xếp lại bản đồ: tối đa 4 màn/hàng, khung 5685 → 2825px ngang
- [x] Đổi nhãn thành phần **Nội bộ → Công ty** toàn hệ thống (giữ "Họp nội bộ" ở Phân loại họp)
- [x] Màn **45 · Cảnh báo chưa lưu khi Quay lại** (3 nút)
- [x] Hub: dấu `*` bắt buộc + thanh Mức độ hoàn thiện hồ sơ (9 Hub) + màn **46 · Hub chặn Hoàn thành**
- [x] Màn **47 · Thêm nhanh dự án TKT** + nút ở màn 06
- [x] Mã công ty trên dòng nhân sự (màn 07 · 14 · 17 · 35)
- [x] Màn 18: bỏ nút Thêm thừa ở khối người liên hệ, gắn badge "Người liên hệ" vào NGƯỜI 1
- [x] Gỡ 19 dòng chú thích logic khỏi trong khung điện thoại

## Phase 4 — Chuẩn hoá & chỉnh theo nghiệm thu (15–16/09) ✅

- [x] Nút **Xem** trên 10 dòng file ở 4 màn tài liệu (11 · 19 · 36 · 38)
- [x] Sửa chữ tràn nút màn 23 (`Xác nhận gửi lịch` → `Xác nhận`); quét 93 nút còn lại, không nút nào tràn
- [x] Đồng nhất thông báo: bỏ toast đè, gom còn 3 loại dải (đỏ / xám / xanh)
- [x] Màn **21** dựng lại theo timeline: ngày–giờ là mốc trên trục, thêm người chủ trì
- [x] Màn **06**: khối giải pháp đổi sang cây cha – con
- [x] Màn **01**: tab `Tôi chủ trì` / `Tôi tham gia` + 3 chip lọc nhanh; màn **02** bỏ ô Công ty / Phòng ban
- [x] Dấu `*` trên Hub đổi sang **theo trạng thái từng màn** (tắt 28, giữ 22)
- [x] DEV NOTE trên artboard 01 · 04a · 06 · 21

## Phase 5 — Bàn giao v11 (16/09) ✅

- [x] Xuất **PDF bản đồ theo bước** — 8 trang, 4 màn/hàng đúng bố cục canvas (bản khách hàng + bản nội bộ)
- [x] Xuất **PDF chi tiết 50 trang** (bản khách hàng + bản nội bộ có ghi chú dev)
- [x] Xuất **50 ảnh PNG 3x**
- [x] File tóm tắt thay đổi gửi khách: `exports/Meeting-Mobile_v11_Tom-tat-thay-doi_2026-09-16.md`

---

## Việc chuyển cho dev (chưa làm, cần chốt/triển khai)

**BE bắt buộc sửa**
- [ ] `customerMeetingHistory()` lọc sai đối tượng: đang so `me.employee_id` với `m.created_by` (người TẠO) thay vì user đang đăng nhập → mọi user thấy danh sách giống nhau. Port khuôn `PotentialCustomerCareService::applyPermissionFilter()`
- [ ] Endpoint `customer-history` trả thêm `host_name` + `end_date` (màn 21 hiện người chủ trì và khung giờ)
- [ ] API danh sách nhân viên trả thêm `company_code` (`c.code as company_code` như các báo cáo đang làm)
- [ ] `projects.*.scope_id` / `implementation_type` / `project_address` đang nullable trong khi FE bắt buộc → lưu thiếu không báo lỗi (cùng loại lỗi Redmine #10874)
- [ ] App dùng `MeetingCalendarCriteria` cho danh sách meeting, KHÔNG dùng `MeetingCriteria`
- [ ] Nhóm API lưu từng phần cho điều hướng Hub → xem `api-luu-tung-phan.md`
- [ ] Danh mục Lý do huỷ + `meetings.cancel_reason_id` → xem `api-luu-tung-phan.md` mục 7

**Cần chốt với khách trước khi code**
- [ ] Màn 06: web chỉ cho 1 Giải pháp + 1 Hạng mục mỗi dự án (SearchPicker đơn), app vẽ chọn nhiều → đổi web hay đổi app?
- [ ] Màn 06: meeting gắn NHIỀU dự án thì chọn dự án trước rồi mới tới cây giải pháp — chưa thiết kế
- [ ] Màn 42: bản rút gọn mặc định copy địa chỉ chính sang địa chỉ xuất hoá đơn
- [ ] Màn 44: liên hệ tạo từ app có tự thêm vào Thành phần khách hàng không
- [ ] Màn 18: dòng NGƯỜI 1 (người liên hệ) có cho xoá tại màn này không
- [ ] Khối "Phiếu tổng hợp kết quả meeting" (#11130) chưa vẽ ở Hub lẫn màn nhập

**Chưa vẽ**
- [ ] Trạng thái rỗng màn 21 ("Bạn chưa tham gia cuộc họp nào với khách hàng này")
- [ ] Biến thể màn 01 lúc đang bật 1 chip lọc
- [ ] Tab `Nhân sự Khách hàng` ở màn 14 (web `PopupStaff` có 2 tab, app mới có 1)
- [ ] Người thực hiện biên bản chọn NHIỀU (Redmine #11044) — màn 10 đang vẽ ô đơn

---

### Checkpoint — 2026-09-16 08:50
Vừa hoàn thành: xuất bản giao hàng v11 (4 PDF + 50 PNG 3x + file tóm tắt), 50 artboard, khung 2825 × 24617.
Đang làm dở: không có — bộ thiết kế ở trạng thái bàn giao được.
Bước tiếp theo: gửi khách bản `BAN-DO-THEO-BUOC_v11_…_BAN-KHACH-HANG.pdf` + file tóm tắt; chờ phản hồi để chốt 6 câu hỏi ở mục "Cần chốt với khách".
Blocked: "logic tạo task giao cho người xử lý ở biên bản" — user báo đã có nhưng KHÔNG tìm thấy trên `tpe`, `tpe-develop-assign`, `gop_db` (Task entity không có FK sang meeting). Chờ user cho số Redmine / tên nhánh.
