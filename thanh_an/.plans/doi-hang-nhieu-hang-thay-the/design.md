# Design tóm tắt — Đổi 1 hàng gốc sang nhiều hàng thay thế (PĐX / PXL)

> Phụ trách: @khoipv · Bắt đầu: 01/10/2026 · Trạng thái: **đã duyệt — sửa đổi 1: thiết kế lại quy đổi SL (01/10/2026)**
> Spec đầy đủ: [docs/superpowers/specs/2026-10-01-doi-hang-nhieu-hang-thay-the-design.md](../../docs/superpowers/specs/2026-10-01-doi-hang-nhieu-hang-thay-the-design.md)
> Feature gốc: [.plans/doi-hang-cung-ung/design.md](../doi-hang-cung-ung/design.md)

## Mục tiêu
Dòng hàng A trên HĐ bán đổi được sang **nhiều** hàng thay thế (VD 10 máy A → 4 máy B + 3 máy C) ở phiếu đề xuất
và phiếu xử lý cung ứng. Hiện chỉ đổi được sang 1 hàng.

## Quyết định lớn
- Mỗi hàng thay thế có SL riêng (ĐVT của nó) + **SL A tương ứng ("Thay cho A")** do người lập nhập.
- Hàng thay thế **thay hết** A — không vừa đổi vừa giữ A.
- **Sửa đổi 1:** SL A của khối **= Σ "Thay cho A"** (tự cộng, không nhập riêng) → không còn trạng thái "tổng lệch",
  bỏ `swap_group_quantity` + rule R5.
- **Tách dòng**: mỗi hàng thay thế = 1 dòng riêng cùng mang A (`supply_proposal_products` / `supply_handling_products`).
  Các dòng cùng (HĐ, A) = 1 **khối đổi hàng**. **Không migration**, dữ liệu đổi 1 hàng cũ = khối 1 dòng.
  - PĐX: "Thay cho A" = `quantity`; PXL: = `swap_origin_quantity`; phân bổ PXL riêng từng dòng.
- BE "đã xử lý" (`handledKey`, `qty_a`, `isFullyHandled`), đơn mua/HĐ mua, phân bổ & báo cáo nhu cầu mua đã gom
  theo cặp (A, hàng thay thế) / theo A → **không sửa**. Chỉ sửa validate (`ValidatesSwapProduct`) và
  `swapMismatch` (bỏ qua hàng thay thế cùng khối).

## UI
Hàng thay thế ở trên có chip ĐỔI, "↳ THAY CHO A" ở dưới:
- Cột **"Thay cho A"** ngay sau ô SL: dòng hàng thay thế có ô nhập + ĐVT A (kể cả khối 1 dòng); dòng thường trống.
- Dòng hàng thay thế: ⇄ chọn lại, ✕ bỏ (bỏ dòng cuối = bỏ đổi).
- Dòng THAY CHO A: "Σ ĐVT" (chỉ đọc), mốc còn HĐ / đề xuất còn, cảnh báo vượt HĐ (đỏ) / vượt đề xuất (vàng) theo Σ;
  "+ Thêm hàng thay thế" (dòng mới trống SL + thay), ↶ gộp về A (SL = Σ), 🗑 xóa khối.
- Excel: thêm cột "Thay cho A"; tên hàng không ghép chú thích.
- PĐX → PXL: prefill **theo từng cặp A→B**: `B còn = swap_quantity − sl_da_xu_ly(cặp)`,
  `thay còn = quantity × B còn ÷ swap_quantity`; cặp hết bỏ, khối hết bỏ. PXL đầu = y đề xuất.

## Phạm vi file
- BE: `ValidatesSwapProduct`, `ExposesSwapProduct` (+ 2 resource chi tiết truyền tập hàng thay thế của khối).
- FE: `GoodsTable.vue`, `HandlingGoodsTable.vue`, `supply_proposals/add.vue`, `supply_handlings/add.vue`,
  `ContractRefTab.vue`, `ProductInfoTab.vue`, `HandlingSummaryTabs.vue`, `SimpleQtyTable.vue`,
  helper `supply_proposals/swapBlocks.js`.
