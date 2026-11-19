# Plan — YCXH lịch sử chỉ ghi ô người dùng tự đổi

Phụ trách: @dangquang.tom · Nhánh: `develop` (gop_db) · Repo: hrm-api

## Phase 1 — BE: lọc log theo ô người dùng trực tiếp đổi

- [x] T1. `catalogColumns()`: thêm `firm_contract_id` vào whitelist (cạnh `emplement_contract_code`).
- [x] T2. `catalogDisplay()`: `firm_contract_id` → hiển thị MÃ hợp đồng (`FirmContract::where('id',…)->value('code')`), null trả null.
- [x] T3. Thêm hằng `SOURCE_DERIVED_LOG_COLUMNS = ['customer_name']` (các cột tự điền theo nguồn).
- [x] T4. `updateFromRequest()`: hoist `$sourceChanged` ra ngoài transaction + by-ref vào closure.
- [x] T5. `updateFromRequest()`: trước `logCatalogUpdate($model,$before)`, nếu `$sourceChanged` thì
      ghi đè `$before[col] = catalogDisplay(col, $model->col)` cho mọi cột trong `SOURCE_DERIVED_LOG_COLUMNS`
      → before==after → không log cột suy-ra.
- [x] T6. `CatalogHistoryService::TABLES['product_export_requests']`: thêm nhãn `'firm_contract_id' => 'Hợp đồng'`.
- [x] T7. `php -l` cả 2 file — sạch.

## Phase 2 — Kiểm thử (dry-run, rollBack, không ghi DB)

- [x] T8. Loại 14 (PYCXH-39254): đổi HĐ hãng → log chỉ "Hợp đồng", không "Khách hàng". ✅
- [x] T9. Loại 19 (id 38510): đổi HĐ thực hiện → log chỉ "Hợp đồng", không "Khách hàng". ✅
- [~] T10. Loại 20/21: không có phiếu nháp trong DB dev → suy ra từ đường dùng chung (đã xác minh 14+19).

## Chưa làm / chờ

- [ ] Commit + push: CHƯA — chờ user yêu cầu rõ ràng.

---

### Checkpoint — 2026-10-14
Vừa hoàn thành: toàn bộ Phase 1 (6 edit BE) + dry-run xác minh loại 14 và loại 19.
Đang làm dở: không.
Bước tiếp theo: báo kết quả cho user; chờ lệnh commit.
Blocked: không.
