# Fix: In hợp đồng lao động ra trang trắng — @khoipv

URL lỗi: `/human/employment-contract/9/print?redirect=%2Fhuman%2Femployment-contract`

## Phase 1 — Điều tra (XONG)

- [x] Trace FE `pages/human/employment-contract/_id/print.vue` → gọi `GET human/employment-contracts/{id}/print`, chỉ có `.then()`, KHÔNG có `.catch()` → API lỗi thì `form` giữ nguyên `''` → card rỗng, trang trắng
- [x] Trace BE `EmploymentContractController::print()` (dòng 249-255): nếu `print_template` (snapshot) rỗng → `PrintTemplate::query()->findOrFail($employmentContract->print_template_id)`
- [x] Query DB (`thanhan_stag_22092026`): HĐ id 9 có `print_template_id = 6`, `print_template` NULL. Bảng `print_templates` chỉ còn id 1, 3, 7, 8, 9, 10 → **mẫu in id 6 đã bị xóa**
- [x] Verify bằng tinker: `ModelNotFoundException — No query results for model [PrintTemplate] 6` → rơi vào `catch` → trả HTTP 400
- [x] Quét toàn bảng: **6 HĐ cùng lỗi** — id 3, 4 (tpl 2), 7 (tpl 5), 8 (tpl 4), 9, 10 (tpl 6)
- [x] Tìm lý do snapshot rỗng: migration `2026_05_22_160000_add_print_template_column_to_employment_contracts` chỉ backfill `print_template` khi mẫu còn tồn tại (`if ($template)`) → 6 HĐ trỏ mẫu đã xóa bị bỏ qua

## Phase 2 — Fix (CHỜ USER CHỐT HƯỚNG)

- [ ] BE: `findOrFail` → `find`, mẫu đã mất thì trả thông báo nghiệp vụ rõ ràng thay vì exception
- [ ] FE: thêm `.catch()` cho lời gọi API print → hiện thông báo lỗi thay vì trang trắng
- [ ] Data: gán lại `print_template_id` cho 6 HĐ sang mẫu còn tồn tại — **cần user chốt mẫu nào cho từng HĐ**
- [ ] Cân nhắc: chặn xóa mẫu in đang được HĐ tham chiếu (hoặc snapshot template ngay lúc tạo HĐ)

## Checkpoint — 2026-09-23

Vừa hoàn thành: Phase 1 — xác định root cause (mẫu in đã bị xóa + FE không bắt lỗi)
Đang làm dở: chưa sửa dòng code nào
Bước tiếp theo: chờ user chốt hướng fix ở Phase 2
Blocked: cần user chốt mẫu in thay thế cho 6 HĐ; cần xác nhận DB demo `demothanhan.dnsmedia.vn` cũng thiếu mẫu id 6 (mới verify trên bản sao stag local)
