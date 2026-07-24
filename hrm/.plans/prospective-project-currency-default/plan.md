# Plan — Mặc định VNĐ cho Loại tiền tệ (form dự án TKT)

Người phụ trách: @manhcuong

Màn: form tạo/sửa dự án tiền khả thi (`/assign/prospective-projects/add` + `_id/edit`).

## Task
- [x] AC1: FinanceSection.loadCurrencies → mặc định `currency_id` = VNĐ (theo code) khi TẠO MỚI (`!formSubmit.id` & chưa chọn); form sửa giữ nguyên
- [x] AC2 (có sẵn): currency_id `required|integer`, service fill → lưu được khi đổi USD
- [x] AC3 (có sẵn): DetailProspectiveProjectResource trả currency_id → edit.vue populate, droplist khóa hiển thị đúng

## Verify
- [x] Playwright: form tạo mới → "Loại tiền tệ" = VNĐ (select value=1, select2 rendered "VNĐ"), 0 lỗi liên quan (currency-default-vnd.png) — AC1 PASS
- [x] AC2/AC3: xác minh qua code (currency_id required|integer + fill khi lưu; DetailResource trả currency_id + edit.vue populate {...form,...data} + droplist khóa hiển thị đúng) — luồng có sẵn, không đổi
- [ ] (tùy chọn) User E2E đầy đủ: tạo dự án chọn USD → lưu → mở sửa xem USD

Không đụng BE/migration/permission. 1 file FE: FinanceSection.vue.

### Checkpoint — 2026-07-14
Vừa hoàn thành: FinanceSection.loadCurrencies mặc định VNĐ (theo code) khi tạo mới. Verify Playwright AC1 live.
Bước tiếp: User verify browser (đổi USD + lưu + mở sửa).
