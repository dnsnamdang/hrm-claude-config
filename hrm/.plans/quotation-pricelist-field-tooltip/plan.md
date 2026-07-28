# Plan — Tạo báo giá: thêm field "Bảng giá áp dụng: Bán lẻ" + sửa tooltip Làm tròn

Màn: Quản lý Báo giá → Tạo báo giá (`quotations/_id/edit.vue`).

## Phase 1 — FE

### AC1 — Field read-only "Bảng giá áp dụng: Bán lẻ"
- [x] Thêm dòng read-only "Bảng giá áp dụng: Bán lẻ" ngay dưới select "Loại tiền tệ" (text .text-muted, không input → không sửa được)

### AC2 — Tooltip "Làm tròn"
- User chốt: THAY bằng đúng text mới trong AC2.
- [x] Đổi tooltip icon "i" (dòng ~199) = 'Khi bấm Áp dụng, hệ thống tự động tính toán giá trị làm tròn dựa trên cấu hình, giá trị làm tròn áp dụng với các cột GIÁ NHẬP, GIÁ BÁN'. Bỏ điều kiện isVndCurrency ở icon để LUÔN hiện text mới (create mặc định VNĐ vẫn đúng AC2). Tooltip trên ô select (VNĐ disabled) giữ nguyên.

### Verify (Playwright, màn create)
- [x] AC1: DOM có "Bảng giá áp dụng: Bán lẻ" read-only dưới Loại tiền tệ (ảnh xác nhận)
- [x] AC2: hover icon "i" → tooltip text KHỚP CHÍNH XÁC chuỗi AC2, mentionsVAT=false (ảnh xác nhận)

### Checkpoint — 2026-07-09
Vừa hoàn thành: CODE DONE + VERIFIED cả AC1 + AC2. FE-only, không BE/migration/git.
File: hrm-client quotations/_id/edit.vue (field Bảng giá + tooltip Làm tròn)
Đang làm dở: không
Bước tiếp: user verify browser
