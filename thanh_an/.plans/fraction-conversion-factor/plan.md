# Fraction Conversion Factor — Plan

@khoipv

## Phase 1: Backend Core
- [x] Task 1: Tạo Helper `ConversionHelper::parseConversionFactor()`
- [x] Task 2: Tạo Validation Rule `ConversionFactorRule`
- [x] Task 3: Migration đổi column `conversion_factor` sang `string(50)`

## Phase 2: Backend — Cập nhật logic tính giá
- [x] Task 4: Sửa `ProductService.php` — parse khi tính giá cho đơn vị mới
- [x] Task 5: Sửa `ProductUnitPriceService.php` — parse khi lưu/tính giá
- [x] Task 6: Sửa `PriceCapitalImport.php` — parse khi import giá vốn

## Phase 3: Backend — Cập nhật Resource + Validation
- [x] Task 7: Sửa 4 Resource Transformers (parse conversion_factor → coefficient)
- [x] Task 8: Sửa Validation (ProductRequest, ProductImportV2)

## Phase 4: Frontend
- [x] Task 9: Sửa `UnitComponent.vue.vue` — đổi input type + validate phân số

## Phase 5: Verify
- [x] Task 10: Syntax check toàn bộ 12 file — PASS

---

Chi tiết từng task: `docs/superpowers/plans/2026-04-16-fraction-conversion-factor.md`

---

### Checkpoint — 2026-04-16
Vừa hoàn thành: Toàn bộ 10 task (3 file mới, 10 file sửa, migration + helper + validation)
Đang làm dở: Không — đã xong. Cần user test thủ công trên trình duyệt
Bước tiếp theo: User test UI — tạo/sửa sản phẩm với hệ số phân số, kiểm tra các màn Quotation/Contract/BidPackage
Blocked: Không
