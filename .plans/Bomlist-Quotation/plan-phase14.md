# Plan Phase 14 — Parent roll-up từ Children

> **Ngày bắt đầu:** 2026-04-23
> **Người phụ trách:** @dnsnamdang
> **Branch:** `tpe-develop-assign`

**Goal:** Khi hàng hoá cha có con, các trường đơn giá của cha tự động tính từ con và không cho sửa.

**Công thức chốt (user confirm 2026-04-23):**
- Giá nhập / giá bán là **đơn giá trên 1 đơn vị**.
- `parent.unit_price = SUM(child.unit_price × child.qty) / parent.qty`
- `parent.VAT% = MAX(child.VAT%)`
- `parent.qty` vẫn cho user nhập.

## Phase 14A — BOM (chỉ giá nhập)

Scope tối thiểu: `estimated_price` cha + thành tiền nhập cha.

### BE
- [x] 1. Không sửa BE (BOM đã lưu `estimated_price` per-row; FE sẽ gửi giá cha đã tính sẵn).

### FE — `BomBuilderEditor.vue`
- [x] 2. Skip (inline trong refreshParentTotals).
- [x] 3. Sửa `refreshParentTotals()`: với mỗi group có children, set `g.parent.estimatedPrice = SUM(child.est × child.qty) / parent.qty`; parent.qty=0 → set 0.
- [x] 4. Deep watcher `groups` đã có sẵn (line 789) tự gọi `refreshParentTotals` khi child qty/price đổi. Vue setter strict equality không gây loop.

### FE — `BomBuilderTableCard.vue`
- [x] 5. Disable V2BaseCurrencyInput `parent.estimatedPrice` khi `group.children.length > 0` + tooltip "Tự động tính từ hàng con" (replace_all cả 2 render path grouped/ungrouped).
- [x] 6. Không cần — deep watcher xử lý.

### Test thủ công
- [ ] 7. Tạo BOM: thêm parent qty=2, child1 (giá=10, qty=3), child2 (giá=20, qty=1) → parent.giá = (10×3+20×1)/2 = 25.
- [ ] 8. Sửa child.qty → parent.giá recalculate.
- [ ] 9. Xoá child cuối → parent input mở lại, giữ giá trị cuối.
- [ ] 10. Parent.qty=0 → parent.giá=0, không chia 0 (NaN).

---

## Phase 14B — Báo giá (6 cột)

Scope: `estimated_price`, `quoted_price`, `vat_percent` + 3 thành tiền tương ứng.

**Design change vs Phase 12:** Children giờ CÓ `vat_percent` riêng (Phase 12 children = "—"). Parent.vat_percent = MAX(children.vat_percent).

### BE — `Modules/Assign/`
- [x] 11. Migration: không cần.
- [x] 12. QuotationService `upsertPrices`: bỏ force `quoted_price=0` cho CHA-có-CON + bỏ force `vat_percent=0` cho CON → trust FE rolled-up values.
- [x] 13. Không đổi validate (BE không bắt buộc price; FE đã validate).

### FE — `pages/assign/quotations/_id/edit.vue`
- [x] 14. Children cell VAT% → `V2BaseInput vat_percent` editable.
- [x] 15. Children cell "Tiền VAT" + "Sau VAT" giữ "—" (chỉ CHA mới tính VAT tổng).
- [x] 16. Skip — với `parent.estimated_price = SUM/qty` thì `lineImportTotal(parent) = (SUM/qty)*qty = SUM` (auto đúng). `totalImport` vẫn có special-case roll-up cũ (harmless redundant).
- [x] 17. `parent.estimated_price` disable + tooltip khi có con; auto-compute qua `refreshParentRollups` watcher.
- [x] 18. `parent.quoted_price` đã disable từ Phase 12; auto-compute qua `refreshParentRollups`.
- [x] 19. `parent.vat_percent` disable + tooltip khi có con; auto-compute = MAX(children.vat_percent).
- [x] 20. `lineVatAmount(parent)` giữ nguyên (formula không đổi).
- [x] 21. Skip — totalImport/totalSale/totalVat đã có special-case sum theo leaf từ Phase 12.

### FE — `pages/assign/quotations/_id/index.vue` (show)
- [x] 22. Children VAT% cell: thay "—" bằng giá trị `child.vat_percent`. Parent tự hiển thị values đã lưu từ BE.

### Test thủ công
- [ ] 23. Edit Báo giá: thêm parent có 2 con, nhập giá/VAT từng con → parent 3 trường auto-compute.
- [ ] 24. Margin % của parent tính đúng dựa trên (sale - import) / sale aggregated.
- [ ] 25. Tổng footer không double-count parent + children.

---

## Trạng thái

- Phase 14A: Code DONE (chờ test thủ công task 7-10)
- Phase 14B: Code DONE (chờ test thủ công task 23-25)

## Checkpoint — 2026-04-23 (Khởi tạo)
Vừa hoàn thành: Brainstorm + chốt công thức với user.
Bước tiếp theo: Implement Phase 14A task 2-6.
Blocked: Không.

## Checkpoint — 2026-04-23 (Phase 14B code DONE)
Vừa hoàn thành:
- FE `edit.vue`: thêm `refreshParentRollups()` + deep watcher `products` → auto-compute parent.estimated_price / quoted_price / vat_percent từ children; children VAT% editable; parent 3 field disable + tooltip khi có con.
- FE `index.vue`: children VAT% hiển thị giá trị thay "—".
- BE `QuotationService::upsertPrices`: bỏ force `quoted_price=0` cho CHA + `vat_percent=0` cho CON → trust FE rolled-up values.

Bước tiếp theo: User test thủ công (task 23-25) — tạo báo giá có parent 2 con, nhập giá/VAT từng con → parent auto-compute, total footer không double-count.
Blocked: Không.
