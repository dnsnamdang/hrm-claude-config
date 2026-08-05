# Popup chi tiết đề xuất khi bấm mã phiếu đề xuất — màn HĐ mua (@khoipv)

Màn `supply/purchase_contracts/add` (Hợp đồng mua). Trong bảng hàng hóa (ProductsTab) và
popup chọn hàng hóa (GoodsPickerModal), cột mã phiếu đề xuất → bấm vào mã mở popup chi tiết
đề xuất cung ứng. Giống UX màn "Đơn mua hàng" / Báo cáo nhu cầu mua (`reports/purchase-demand`).

Popup dùng API có sẵn: `GET supply/supply-proposals/{id}` (meta + danh sách hàng hóa).

## Bối cảnh
- Trên nhánh đúng: màn "Đơn mua hàng" DÙNG popup `purchase_orders/components/SupplyDocDetailModal.vue`
  (self-contained, props `:visible.sync` + `kind` + `:doc-id`, fetch `supply/supply-proposals/{id}`).
  → TÁI SỬ DỤNG popup này thay vì tự tạo `ProposalDetailModal.vue` (đã xóa) để giống hệt màn DMH.
- `goods-pool` trả `demand[].lines[].proposal_id` (SupplyReportService dòng 168) nhưng
  `purposes` đang bỏ mất → phải thêm `proposal_id` vào purpose.

## Tasks
- [x] T1: ~~Tạo `ProposalDetailModal.vue`~~ → thay bằng tái sử dụng `SupplyDocDetailModal.vue` (màn DMH)
- [x] T2: `GoodsPickerModal.buildCandidates` — thêm `proposal_id` vào purpose; render mã phiếu
      đề xuất dạng link bấm được (@click.stop.prevent); cột "Khách hàng SD" mỗi khách 1 dòng;
      gắn `<SupplyDocDetailModal :visible.sync>` + method `openProposal` set doc-id/visible
- [x] T3: `ProductsTab.vue` — cột "Mục đích mua": mã `pp.proposal` thành link bấm được;
      gắn `<SupplyDocDetailModal :visible.sync>` + method `openProposal`
- [x] T4: Verify compile (vue-template-compiler PASS cả 2 file)
- [x] T5: Danh sách HĐ mua (`index.vue`) — trạng thái đổi `b-badge` → `BaseStatusColor`
      + colorMap giống màn Đơn mua hàng (Nháp = pill xanh dương pastel)
- [x] T6: Mã HĐ bán ra trong cột "Mục đích mua" (ProductsTab) — trước để rỗng
      (`saleContract: ''`). goods-pool BE có `contract_id`/`contract_code` (SupplyReportService
      dòng 175-176) → đọc vào purpose `saleContract` + `saleContract_id`; render link bấm được
      → mở `purchase_orders/components/ContractDetailModal.vue` (fetch
      `supply/purchase-orders/sale-contracts/{id}`). Compile PASS.
- [x] T7: Mã HĐ bán hiển thị SAI = số HĐ (contracts.number) thay vì mã HĐ (contracts.code
      dạng HD-002/2025). BE `$codeByContract` ưu tiên number (dùng cho DMH) → KHÔNG đổi, thêm
      map mới `$saleCodeByContract` (= code) + field line `sale_contract_code` (additive, không
      phá DMH). FE GoodsPickerModal đọc `l.sale_contract_code || l.contract_code`. BE lint + FE compile PASS.

### Checkpoint — 2026-08-05 (dùng chung SupplyDocDetailModal của màn DMH)
Vừa hoàn thành: bỏ `ProposalDetailModal.vue` tự tạo → cả ProductsTab + GoodsPickerModal đều
tái sử dụng `purchase_orders/components/SupplyDocDetailModal.vue` (giống hệt popup màn Đơn mua
hàng, phần thông tin bên trên). Cột "Khách hàng SD" mỗi khách 1 dòng. Compile PASS cả 2 file.
Đang làm dở: (không)
Bước tiếp theo: user bật client, E2E — mở `supply/purchase_contracts/add`, chọn hàng theo phiếu
đề xuất, bấm mã phiếu ở cả bảng hàng hóa lẫn popup chọn hàng → popup chi tiết hiện đúng đề xuất.
Blocked:

## Ghi chú
- Chỉ FE, không đụng BE, không migration.
- Link chỉ hiện khi có `proposal_id` (guard v-if) → edit mode thiếu id không vỡ.
