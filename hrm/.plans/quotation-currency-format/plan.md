# Plan — Đổi định dạng tiền tệ (, nghìn / . thập phân) luồng quản lý dự án

## Phase 1 — FE hiển thị + ô nhập + BE

- [x] **T1. FE hiển thị**: đổi `NumberFormat('vi-VN'`/`toLocaleString('vi-VN'` → `'en-US'` (chỉ dòng format SỐ, KHÔNG đụng `toLocaleDateString`) tại 9 file:
  - quotations/index.vue:580, quotations/_id/edit.vue:1829, quotations/_id/index.vue:1074
  - components/assign/quotation/QuotationPrintPreview.vue:452, QuotationSubmitModal.vue:129
  - bom-list/components/BomBuilderEditor.vue:1450, BomBuilderTableCard.vue:789
  - prospective-projects/components/ProspectiveProjectQuotationsTab.vue:457
  - settings/price-approval/index.vue:464
- [x] **T2. FE ô nhập** `components/V2BaseCurrencyInput.vue` (Assign-only): `formatCurrency` thousands `,` + decimal `.`; `parseRawValue` bỏ `,` giữ `.`; `onInput` sửa nhận diện thập phân trailing `,`→`.`.
- [x] **T3. BE** `QuotationService.php` fmtNum: `number_format($v,0,',','.')` → `number_format($v,0,'.',',')` (log đổi giá).
- [x] **T4. Verify**: grep sạch `vi-VN` (number) trong core dirs; `php -l` QuotationService OK; date `toLocaleDateString('vi-VN')` giữ nguyên. Không round-trip parse output hiển thị.
- [ ] **T5. Verify E2E** (user): build FE → báo giá/BOM hiển thị `1,234,567.89`; gõ ô giá nhập/bán → format `,` nghìn `.` thập phân, lưu đúng số; bản in + submit modal + tab dự án + cấu hình duyệt giá đồng bộ.

### Checkpoint — 2026-07-02
Vừa hoàn thành: T1–T4 (FE hiển thị 9 file + input V2BaseCurrencyInput + BE fmtNum). Chỉ đổi dấu phân cách; giữ công thức + date.
Đang làm dở: (không)
Bước tiếp theo: user build FE + E2E (T5).
Blocked:
