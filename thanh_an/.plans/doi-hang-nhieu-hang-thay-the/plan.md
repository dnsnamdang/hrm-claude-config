# Đổi 1 hàng gốc sang nhiều hàng thay thế (PĐX / PXL)

@khoipv — Bắt đầu 01/10/2026 · Design: [design.md](design.md)
Spec: [docs/superpowers/specs/2026-10-01-doi-hang-nhieu-hang-thay-the-design.md](../../docs/superpowers/specs/2026-10-01-doi-hang-nhieu-hang-thay-the-design.md)

## Phase 0 — Brainstorming
- [x] Chốt yêu cầu + phương án dữ liệu (tách dòng, thay hết A, tổng lệch → chặn lưu)
- [x] Viết spec + design tóm tắt
- [x] User duyệt spec ("ok làm đi", "bạn cứ làm hết đi")
- [x] Lên plan chi tiết

## Phase 1 — BE (Modules/Supply)
- [x] `ValidatesSwapProduct`: rule `products.*.swap_group_quantity` + `validateSwapBlocks($validator, $originField)` (R2, R3, R5, R6)
- [x] Gọi `validateSwapBlocks` từ `StoreSupplyProposalRequest` ('quantity') và `StoreSupplyHandlingRequest` ('swap_origin_quantity')
- [x] `ExposesSwapProduct`: `blockSwapIdsMap()` + `swapMismatch` bỏ qua hàng thay thế cùng khối; 2 resource chi tiết truyền map
- [x] Kiểm tra `php -l` + script PHP độc lập thử validate khối

## Phase 2 — FE helper + PĐX
- [x] Helper `pages/supply/supply_proposals/swapBlocks.js` (`blockKey`, `groupBlocks`, `blockMeta`, `blockOriginSum`)
- [x] `GoodsTable.vue`: bố cục khối (STT chung, ô "thay x A", dòng THAY CHO A có SL A khối + tổng gốc, + Thêm hàng thay thế, ↶, 🗑 khối), vượt HĐ theo khối
- [x] PĐX `add.vue`: loadDetail gom khối, swap add-mode, clearSwap gộp khối, xóa khối, excludeKeys, validate R2–R5, payload `swap_group_quantity`, Excel

## Phase 3 — FE PXL
- [x] PXL `add.vue`: prefill theo khối (§8), loadHandling gom khối, swap add-mode, clearSwap, xóa khối, validate, payload, Excel, cảnh báo theo khối
- [x] `HandlingGoodsTable.vue`: bố cục khối như PĐX, ô "thay x A" lên dòng hàng thay thế, SL A khối, cảnh báo vượt HĐ/đề xuất theo khối, mismatch khử trùng
- [x] `HandlingSummaryTabs.vue`: tab HĐ / thông tin hàng khử trùng theo hàng gốc; tab đề nghị xuất kho / mua / xuất gửi / trả vay hiện hàng thay thế (ĐVT + số liệu nguồn của nó), key theo dòng (`SimpleQtyTable` key `r.key || r.product_id`)

## Phase 4 — Kiểm tra
- [x] Compile template/script FE (vue-template-compiler + @babel/parser) — 9 file OK
- [x] Rà lại spec mục 10 (edge case) — đã cover hết 7 tình huống
- [ ] User test UI theo spec §11

## Phase 5 — Sửa đổi 1: thiết kế lại quy đổi SL (user duyệt "ok")
- [x] Cập nhật spec (header, Q3, §3, §4, §7, §8, §9, §10, §11) + design.md
- [x] BE `ValidatesSwapProduct`: bỏ R5 + rule `products.*.swap_group_quantity`
- [x] `swapBlocks.js`: `blockGroupQty` = Σ, `groupBlocks` bỏ điền `swap_group_quantity`, `swapBlockError` bỏ kiểm tra tổng
- [x] PĐX `GoodsTable.vue`: cột "Thay cho A" sau SL đề xuất; dòng THAY CHO hiện "= Σ" + cảnh báo; bỏ ô SL A khối / "thay x A" / Tổng gốc
- [x] PĐX `add.vue`: bỏ gửi `swap_group_quantity`; + thêm dòng trống; clearSwap SL = Σ; Excel cột "Thay cho A"
- [x] PXL `HandlingGoodsTable.vue`: như PĐX (sau Đặt đơn), mốc "còn HĐ · đề xuất còn"
- [x] PXL `add.vue`: `mapProposalItems` prefill theo cặp; bỏ `swap_group_quantity`; + thêm dòng trống; clearSwap; Excel
- [x] Compile FE (`check_vue.js`) + `php -l`
- [x] Bỏ dấu "=" trước tổng SL hàng gốc ở dòng THAY CHO (PĐX + PXL)
- [ ] User test lại theo spec §11 (bản sửa đổi 1)

### Checkpoint — 01/10/2026
Vừa hoàn thành: Phase 5 — BE bỏ R5, swapBlocks.js, PĐX (GoodsTable + add), PXL (HandlingGoodsTable + add: prefill theo cặp, Excel cột "Thay cho hàng gốc"); compile 9 file FE + php -l OK
Đang làm dở: —
Bước tiếp theo: user test UI PĐX/PXL theo spec §11
Blocked:
