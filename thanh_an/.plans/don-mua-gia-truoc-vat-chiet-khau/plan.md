# Plan — Đơn mua hàng: Đơn giá trước VAT + Chiết khấu (%) + Tổng tiền trước VAT

**Người phụ trách:** @khoipv
**Ngày:** 06/10/2026
**Design:** [design.md](design.md) · **Spec:** [docs/superpowers/specs/2026-10-06-don-mua-gia-truoc-vat-chiet-khau-design.md](../../docs/superpowers/specs/2026-10-06-don-mua-gia-truoc-vat-chiet-khau-design.md)

## Quyết định (user chốt 06/10/2026)
1. Y hệt HĐ mua: `Đơn giá có VAT | VAT (%) | Đơn giá trước VAT | Chiết khấu (%) | Đơn giá sau CK | Tổng tiền (trước VAT)`,
   VAT theo danh mục hàng hóa (snapshot BE), CK% nhập theo khách, 3 số lẻ, khối tổng 3 dòng dưới bảng,
   `purchase_orders.total_amount` = Thành tiền sau VAT (đã trừ CK).
2. Khối tổng theo "Cty thực hiện mua" dưới bảng: GIỮ, số tiền = sau CK + VAT.
3. Tách công thức ra dùng chung: FE `pricing.js` → helper chung; BE `lineMoney/lineVat/productTaxMap/percentOf` → trait mới.
   HĐ mua đổi import / dùng trait, công thức giữ nguyên.

## Phase 1 — BE (`hrm-thanhan-api/Modules/Supply`)
- [x] B1. Trait mới `Services/Concerns/CalculatesPurchaseLineMoney` (chuyển lineMoney, lineVat, productTaxMap, percentOf từ PurchaseContractService);
      PurchaseContractService dùng trait (productTaxMap vẫn public — controller gọi)
- [x] B2. Migration: `purchase_order_products` thêm `discount_percent` decimal(5,2) + `discount_amount` bigint; `amount` → decimal(20,3);
      `purchase_orders.total_amount` → decimal(20,3)
- [x] B3. PurchaseOrderService: calcTotalAmount = Σ sau VAT; syncProducts snapshot vat_percent, discount_percent, discount_amount, amount trước VAT
- [x] B4. Endpoint `POST supply/purchase-orders/product-taxes` (hoặc FE dùng chung endpoint HĐ mua — xem quyền route)
- [x] B5. DetailPurchaseOrderResource trả `discount_percent`, `amount`/`total_amount` ép float; validate `products.*.discount_percent` 0–100

## Phase 2 — FE (`hrm-thanhan-client/pages/supply`)
- [x] F1. Chuyển `purchase_contracts/pricing.js` ra helper chung, HĐ mua sửa import
- [x] F2. Đơn mua `ProductsTab.vue`: thêm cột VAT (%), Đơn giá trước VAT, CK% (theo khách), Đơn giá sau CK; Thành tiền → Tổng tiền (trước VAT);
      sửa colspan / dòng phụ đổi hàng / cố định cột
- [x] F3. Khối tổng 3 dòng dưới bảng + khối theo Cty mua tính sau VAT
- [x] F4. `PurchaseOrderForm.vue`: totalAmount = Thành tiền sau VAT (tab Thanh toán); màn danh sách ép Number total_amount
- [x] F5. Kiểm tra compile template
- [x] F6. Khối "Tổng tiền theo công ty thực hiện mua" chuyển sang bên trái, ngang hàng khối tổng 3 dòng
- [x] F7. Khối 3 dòng tổng tiền lùi sang phải thêm, khối Cty mua bên trái ngang hàng

## Phase 3 — Kiểm thử
- [x] T1. Chạy migration local, đối chiếu BE/FE; mở đơn cũ (chưa có CK) hiển thị CK 0%

### Checkpoint — 2026-10-06
Vừa hoàn thành: F2–F5 + T1 (đơn mua có đủ cột VAT/CK như HĐ mua, khối tổng 3 dòng, migration đã chạy local, FE/BE khớp số trên 4 đơn thật)
Đang làm dở: —
Bước tiếp theo: user test tay trên trình duyệt (lập / sửa / xem đơn, đơn nhiều khách, đổi hàng) → wrap up (fill design.md + spec)
Blocked:

## Phase 4 — Sửa cách tính tiền: tính ngược từ giá có VAT (user chốt 06/10/2026)
Lý do: 100.000 × 3, VAT 5% ra Thành tiền sau VAT 299.999,999 (tách đơn giá trước VAT làm tròn 3 số lẻ rồi mới nhân SL).
Quy tắc mới (dùng chung Đơn mua + HĐ mua):
  Sau VAT   = round_đồng(Σ SL × Đơn giá có VAT × (1 − CK%))   — làm tròn từng DÒNG
  Trước VAT = round_đồng(Sau VAT / (1 + VAT%))
  VAT       = Sau VAT − Trước VAT
  Tổng chứng từ = cộng các dòng. Cột Đơn giá trước VAT / sau CK chỉ để xem, giữ 3 số lẻ.
- [x] R1. BE trait `CalculatesPurchaseLineMoney::lineMoney` trả thêm vat_amount / total (sau VAT) theo quy tắc mới
- [x] R2. BE `PurchaseOrderService::calcTotalAmount` + `PurchaseContractService` (chỗ cộng VAT) dùng total của trait
- [x] R3. FE `utils/purchase-pricing.js` lineMoney / sumTotals theo quy tắc mới
- [x] R4. FE ProductsTab đơn mua + HĐ mua: ô tiền theo nhóm khách / tổng theo Cty mua dùng số mới; ô CK hiện "0" thay "00"
- [x] R5. Đối chiếu FE/BE (case 100.000 × 3 VAT 5% → 300.000; đơn nhiều khách có CK)

### Checkpoint — 2026-10-06 (Phase 4)
Vừa hoàn thành: R1–R5 — tính ngược từ giá có VAT, làm tròn đồng từng dòng (trait BE + utils FE + ProductsTab đơn mua & HĐ mua);
  khối theo Cty mua chia Thành tiền sau VAT của dòng cho từng khách (phần lẻ dồn nhóm cuối) nên luôn khớp TỔNG CỘNG;
  ô CK = 0 để trống + placeholder "0", rời ô thì vẽ lại (hết "00"). FE/BE khớp 4 đơn thật + 2 case tự dựng (100.000 × 3 VAT 5% → 300.000).
Đang làm dở: —
Bước tiếp theo: user test tay lại (đơn mua + HĐ mua; đơn/HĐ cũ đã lưu total_amount 3 số lẻ chỉ đổi khi mở sửa và lưu lại) → wrap up
Blocked:

## Phase 5 — Gộp `thanhan-dev` vào `update-ui` (client) — 06/10/2026
- [x] M1. Fix conflict `purchase_orders/components/ProductsTab.vue`: giữ 5 cột VAT/CK của thanhan-dev, dấu * theo V2 (`req-star`, bỏ `<Required />`); giữ style `.num-field/.disc-field` cho ô CK (vẫn dùng base-input-field)
- [x] M2. Fix conflict `PurchaseOrderForm.vue`: giữ khung V2 (tab, formValidateMixin, confirm gửi duyệt) + `sumTotals`; bỏ `lineAmount` / `scrollToInputError` (không còn dùng)
- [ ] M3. (Tuỳ chọn) Chuyển phần mới của thanhan-dev sang V2: ô CK (base-input-field → V2BaseInput), base-helper-error → V2BaseError, currency-input khối tổng, nút xoá phiếu `mdi-close`

### Checkpoint — 2026-10-06 (merge)
Vừa hoàn thành: M1–M2 — hết conflict, 2 file compile template + parse script OK, đã `git add` (chưa commit)
Đang làm dở: —
Bước tiếp theo: user test tay màn lập/sửa đơn mua trên update-ui rồi tự commit merge; quyết định có làm M3 không
Blocked:
