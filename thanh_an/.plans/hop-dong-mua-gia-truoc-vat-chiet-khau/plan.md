# Plan — HĐ mua: Đơn giá trước VAT + Chiết khấu (%) + Tổng tiền trước VAT

**Người phụ trách:** @khoipv
**Ngày:** 29/09/2026
**Design:** [design.md](design.md) · **Spec:** [docs/superpowers/specs/2026-09-29-hop-dong-mua-gia-truoc-vat-chiet-khau-design.md](../../docs/superpowers/specs/2026-09-29-hop-dong-mua-gia-truoc-vat-chiet-khau-design.md)

## Phase 1 — BE (`hrm-thanhan-api/Modules/Supply`)
- [x] B1. Migration: `purchase_contract_products` thêm `discount_percent` decimal(5,2), đổi `amount` → decimal(20,3);
      đổi `purchase_contracts.total_amount` → decimal(20,3)
- [x] B2. `PurchaseContractService`: tính tiền riêng cho HĐ mua (không đụng trait dùng chung) — snapshot VAT từ `products.tax`,
      CK% theo khách, amount = tổng tiền trước VAT; `total_amount` = Thành tiền sau VAT
- [x] B3. Endpoint `POST supply/purchase-contracts/product-taxes` → `{product_id: tax}` cho FE hiển thị VAT
- [x] B4. `DetailPurchaseContractResource` trả `discount_percent`, `amount` ép float (entity `$guarded = []`, không cần casts)
- [x] B5. Validate `products.*.discount_percent` 0–100

## Phase 2 — FE (`hrm-thanhan-client/pages/supply/purchase_contracts`)
- [x] F1. Helper `pricing.js` (công thức dùng chung ProductsTab + Form)
- [x] F2. `ProductsTab.vue`: VAT theo danh mục (1 ô/dòng), thêm cột Đơn giá trước VAT, CK% (nhập theo khách), Đơn giá sau CK,
      đổi Thành tiền → Tổng tiền, sửa dòng TỔNG CỘNG / colspan / dòng phụ đổi hàng
- [x] F3. Khối tổng dưới bảng: Thành tiền trước VAT / VAT / Thành tiền sau VAT (chỉ HĐ Thương mại)
- [x] F4. `PurchaseContractForm.vue`: `totalAmount` = Thành tiền sau VAT (tab Điều khoản thanh toán)
- [x] F5. Kiểm tra compile template + SCSS
- [x] F6. Cột VAT chỉ hiện % VAT (bỏ dòng tiền VAT); bỏ ký hiệu "%" trong ô VAT + ô CK (header đã có "(%)")
- [x] F7. Xóa hàng hóa trong bảng: thay `confirm()` của trình duyệt bằng modal xác nhận `confirm-delete-selected` (giống màn danh sách HĐ mua)

## Phase 3 — Kiểm thử
- [ ] T1. Chạy migration trên DB dev, lưu thử HĐ TM 1 khách / nhiều khách / mua ngoài phiếu / HĐ NT
      (đã chạy migration local + đối chiếu BE lineMoney/calcTotalAmount = FE pricing.js; CHƯA lưu thử qua UI)
- [x] T2. Mở lại HĐ cũ (chưa có CK%) — hiển thị CK 0%, không vỡ

## Việc còn treo
- [ ] `PrintTab.vue` vẫn in đơn giá có VAT × SL — chờ user chốt mẫu in có tách trước VAT / CK% không

### Checkpoint — 29/09/2026
Vừa hoàn thành: BE (B1–B5) + FE (F1–F5): pricing.js, ProductsTab thêm cột Đơn giá trước VAT / CK% (theo khách) / Đơn giá sau CK / Tổng tiền, khối tổng dưới bảng, Form totalAmount = sau VAT; migration đã chạy local
Đang làm dở: —
Bước tiếp theo: User lưu thử trên UI (T1): HĐ TM 1 khách / nhiều khách / mua ngoài phiếu / HĐ NT; chốt mẫu in PrintTab
Blocked:
