# Plan — Đổi hàng trong phiếu đề xuất / phiếu xử lý cung ứng

> Phụ trách: @khoipv · Ngày tạo: 2026-09-26
> Spec: [docs/superpowers/specs/2026-09-26-doi-hang-cung-ung-design.md](../../docs/superpowers/specs/2026-09-26-doi-hang-cung-ung-design.md)
> Design tóm tắt: [design.md](design.md)

**Mục tiêu:** dòng hàng cung ứng ghi được cặp (A theo HĐ · B giao thật) — hóa đơn/đối trừ HĐ vẫn A, mua & giao là B.

**Kiến trúc:** thêm 8 cột `swap_*` vào `supply_proposal_products` + `supply_handling_products`; `swap_product_id IS NULL` = dòng không đổi (mọi logic cũ giữ nguyên). FE hiển thị dòng phụ nền vàng dưới dòng A.

**Ràng buộc chung:**
- PHP 7.4 / Laravel 8 — migration **chỉ index, không khóa ngoại**.
- Cột decimal trả về string → resource ép `(float)`, FE ép `Number()`.
- FE: nút theo `.claude/skills/button-convention/SKILL.md`; không dùng input/select native; nhãn bắt buộc dùng `Required`.
- Không commit / không push (user tự commit).
- Không chạy E2E nếu user không yêu cầu.

---

## Phase 0 — Brainstorming & design

- [x] Chốt nghiệp vụ đổi hàng (A theo HĐ / B giao thật)
- [x] Viết spec chi tiết + design tóm tắt + STATUS.md
- [x] User duyệt spec (26/09/2026)
- [x] Lập plan task BE/FE

## Phase 1 — Backend

### Task 1.1 — Migration 2 bảng
- [x] Tạo `Modules/Supply/Database/Migrations/2026_09_26_000001_add_swap_columns_to_supply_proposal_products_table.php` (7 cột `swap_*`, `after('quantity')`, index `swap_product_id`)
- [x] Tạo `2026_09_26_000002_add_swap_columns_to_supply_handling_products_table.php` (cùng bộ cột, `after('dat_don')`)
- [x] Chạy `php artisan migrate` — kiểm tra `DESC supply_proposal_products` / `supply_handling_products`

### Task 1.2 — Lưu dữ liệu
- [x] `SupplyProposalService::syncProducts()` — thêm 7 khóa `swap_*`, chuẩn hóa: `swap_product_id` rỗng/0 ⇒ toàn bộ `swap_*` = null
- [x] `SupplyHandlingService` (hàm sync dòng hàng) — như trên
- [x] Helper dùng chung `normalizeSwap(array $item): array` để 2 service không lặp logic chuẩn hóa

### Task 1.3 — Validate
- [x] `StoreSupplyProposalRequest`: rule `products.*.swap_product_id|swap_quantity`
- [x] `withValidator`: B ≠ A · `swap_quantity > 0` · B tồn tại trong `products` (1 query `whereIn`)
- [x] `StoreSupplyHandlingRequest`: cùng bộ rule + message tiếng Việt

### Task 1.4 — Resource trả về FE
- [x] `DetailSupplyProposalResource`: 7 field `swap_*`, `swap_quantity` ép `(float)`
- [x] `DetailSupplyHandlingResource`: như trên
- [x] `liveCodeMap()` gọi 1 lần cho hợp `product_id` ∪ `swap_product_id` (không thêm query)

### Task 1.5 — Kế thừa khi lập phiếu xử lý
- [x] Rà soát BE: prefill dòng hàng do **FE** làm (`supply_handlings/add.vue` đọc detail đề xuất), BE không có chỗ copy ⇒ không sửa gì. `DetailSupplyProposalResource` đã trả đủ `swap_*` ⇒ FE có dữ liệu để kế thừa (thực thi ở Task 2.5)
- [x] BE vẫn ép `dat_don = swap_quantity` khi lưu (`SupplyHandlingService::syncProducts`) — chốt chặn nếu FE gửi lệch

### Task 1.6 — Gom "SL đã xử lý" theo cặp (A,B)
- [x] `SupplyProposalService::handledQtyByProduct()` — khóa gom `product_id . '_' . (swap_product_id ?? 0)` (qua `handledDetailByProduct()` + `handledKey()`)
- [x] Cập nhật nơi gọi: `DetailSupplyProposalResource`, `DetailSupplyHandlingResource`, `isFullyHandled()`
- [x] Trả thêm `swap_mismatch` (danh sách mã B' của PXL đổi khác) để FE cảnh báo — lấy từ `handledDetailByProduct()['variants']`, không thêm query
- [x] `isFullyHandled()`: dòng PXL **không đổi** cộng như cũ (giữ nguyên hành vi phiếu cũ), dòng PXL **có đổi** chỉ cộng khi khớp cặp của đề xuất

### Task 1.7 — Báo cáo Nhu cầu mua theo hàng B
- [x] `SupplyReportService` 2 query (`:46`, `:409`): group theo `COALESCE(shp.swap_product_id, shp.product_id)`
- [x] Tên hàng / ĐVT / nhóm hàng theo hàng hiệu lực; thêm cột "Thay thế cho" (mã A)
- [x] Rà soát export Excel của báo cáo: file xuất dựng ở **FE** (`pages/supply/reports/purchase-demand/index.vue`) ⇒ thêm cột "Thay thế cho" ở Phase 2 (Task 2.6)

### Task 1.8 — Export Excel 2 phiếu
- [x] `exportGoods` (SupplyProposalController + SupplyHandlingController): chèn dòng phụ "↳ Đổi sang…" ngay dưới dòng A, nền vàng nhạt

### Task 1.9 — Verify BE
- [x] Tinker (bọc transaction + rollback): lưu phiếu có đổi → đọc lại đúng; bỏ đổi → `swap_*` null sạch; `handledQtyByProduct` gom đúng cặp

## Phase 2 — Frontend

### Task 2.1 — Popup chọn hàng thay thế
- [x] `supply_proposals/components/GoodsPickerModal.vue`: prop `mode` (`'normal' | 'swap'`) + `swap-for-label`; chế độ swap = chỉ hàng ngoài HĐ, radio chọn đúng 1 dòng, ẩn cột/nút liên quan HĐ
- [x] Emit `confirm-swap` trả `{ product_id, product_code, product_hh_code, product_name, unit_id, unit_name }`

### Task 2.2 — Bảng hàng phiếu đề xuất
- [x] `supply_proposals/components/GoodsTable.vue`: nút **Đổi** (`mdi-swap-horizontal`) ở cột thao tác (đổi tên cột "Xóa" → "Thao tác")
- [x] Dòng phụ `<tr class="swap-row">` nền vàng: mã B · mã HH B · tên B · ĐVT B · pill NK/PPL của B · input SL B · nút Sửa/Bỏ đổi
- [x] Badge `ĐỔI` cạnh mã nội bộ A ở dòng chính (tooltip trỏ xuống dòng phụ)
- [x] Số liệu nguồn: dòng chính theo **A**, dòng phụ theo **B** (`swap_src` + hằng `SWAP_SRC_KEYS` ở constants.js); `sl_con_lai_hd` chỉ có ở dòng chính — *sửa 26/09 theo yêu cầu “hàng nào thể hiện số của hàng đó”*

### Task 2.3 — Màn lập/sửa đề xuất
- [x] `supply_proposals/add.vue`: state `swap_*`, mặc định `swap_quantity = quantity` khi chọn B
- [x] Payload submit gửi `swap_*`; bỏ đổi → gửi null (`clearSwap`)
- [x] Gọi `product-info` gửi thêm item của B (`swap_product_id` / `swap_unit_id`) để lấy NK-PPL, giá theo ĐVT B
- [x] Validate FE: chọn B mà SL B ≤ 0 → highlight + chặn submit

### Task 2.4 — Bảng hàng phiếu xử lý
- [x] `supply_handlings/components/HandlingGoodsTable.vue`: dòng phụ + nút như đề xuất
- [x] Dòng đã đổi: `dat_don` **chính là** SL của B (gõ ở ô Đặt đơn, đồng bộ 2 chiều với `swap_quantity`), có ghi chú "theo <ĐVT B>"
- [x] Cột "Đã xử lý" / "Còn lại" và validate vượt đặt đơn tính theo B
- [x] Bỏ qua validate vượt HĐ cho dòng đã đổi (`isOverContract` trả false) + tooltip giải thích
- [x] Cảnh báo `swap_mismatch` — gom thành ghi chú vàng dưới bảng (liệt kê phiếu khác xử lý mã hàng này theo cách đổi khác)

### Task 2.5 — Màn lập/sửa phiếu xử lý
- [x] `supply_handlings/add.vue`: nhận `swap_*` kế thừa từ đề xuất (`swapFieldsOf`), cho sửa/bỏ đổi, payload gửi lên
- [x] Bỏ đổi → `dat_don` về SL của A (mốc `dat_don_a`) + toast nhắc kiểm tra lại ô phân bổ
- [x] Đổi tiếp khi đã nhập phân bổ → `confirm()` trước khi ghi đè

### Task 2.6 — Export Excel FE + báo cáo Nhu cầu mua
- [x] `utils/supply-excel-export.js`: nhận dòng dạng `{ cells, swap: true }` → tô nền vàng + chữ nghiêng
- [x] `supply_proposals/add.vue` + `supply_handlings/add.vue`: chèn dòng phụ "↳ Đổi sang…" vào file xuất
- [x] `pages/supply/reports/purchase-demand/index.vue`: thêm cột **Thay thế cho** (bảng + Excel, đọc `lines[].swap_for_code` / `swap_for_name`), cập nhật colspan nhóm cột & ghi chú dưới bảng
- [x] ~~`supply_proposals/inbox.vue`: khối chi tiết hiển thị hàng đổi~~ — **không áp dụng**: inbox chỉ là bảng danh sách phiếu (mã phiếu, người lập, khách hàng…), không hiển thị dòng hàng hóa

### Task 2.7 — Kiểm tra compile
- [x] Parse/compile 8 file FE đã sửa bằng `vue-template-compiler` + `@babel/parser` (Node 14) — **8/8 sạch**
- [ ] ⚠️ `npm run build` đầy đủ: **user tự chạy khi tắt dev server**. Lần thử 26/09 bị hủy vì `npm run dev` đang chạy cùng lúc → hai tiến trình ghi chung `.nuxt` sinh lỗi `ENOENT .nuxt/client.js` / `.nuxt/views/app.template.html` ở dev server

### Task 2.8 — Chốt phạm vi: chỉ đổi hàng LẤY TỪ HỢP ĐỒNG (26/09/2026)
- [x] `GoodsTable.vue` + `HandlingGoodsTable.vue`: nút **Đổi** chỉ hiện khi `p.in_contract && !p.swap_product_id`
- [x] `supply_proposals/add.vue` + `supply_handlings/add.vue`: `openSwapPicker()` chặn dòng ngoài HĐ + toast "Chỉ đổi được hàng lấy từ hợp đồng…"
- [x] BE `ValidatesSwapProduct::validateSwapLines()`: thêm rule `in_contract` — dòng ngoài HĐ gửi kèm `swap_*` bị chặn
- [x] Cập nhật spec (phạm vi + validate + UX nút)

### Task 2.9 — Số liệu nguồn: hàng nào thể hiện số của hàng đó (26/09/2026)
- [x] `GoodsTable.vue` + `HandlingGoodsTable.vue`: `srcVal()` / `tonText()` bỏ nhánh `swap_src` — dòng chính luôn là số của hàng gốc A
- [x] Thêm `swapSrcVal()` / `swapTonText()`: dòng phụ hiển thị số của riêng B ở đúng các cột (thay cho ô ghi chú colspan cũ), `sl_con_lai_hd` để `—`
- [x] Phiếu cũ chưa có `swap_src` → hiện `—` + tooltip “chọn lại hàng để lấy số mới”
- [x] Export Excel 2 màn: dòng phụ xuất số liệu nguồn của B (`swapSrcVal`) thay cho các ô trống
- [x] Parse/compile lại 8 file FE — 8/8 sạch
- [x] Cập nhật spec mục 5.5 + 6.4 + bảng quyết định (dòng 6)

### Task 2.10 — Thiết kế lại khối “Đổi” / “Đổi sang” (26/09/2026 — user: *“nhìn đang không được đẹp”*)
- [x] Dựng demo `demos/demo-doi-hang-cung-ung.html` — 3 phương án (PA A khối cặp · PA B hai tầng 1 dòng · PA C dải gọn) + bảng so sánh, cập nhật `demos/README.md`
- [x] User chọn **PA A — khối cặp**
- [x] Áp vào `GoodsTable.vue` + `HandlingGoodsTable.vue`: dòng chính thêm class `swap-top` (viền đứt nét hổ phách dưới + thanh `inset 3px` bên trái), dòng phụ nền `#fbf4e4` (thay `#fff9e6`) cùng thanh trái → 2 dòng thành 1 khối
- [x] Badge `ĐỔI` nền vàng đặc → chip viền mảnh `.swap-chip` (icon `mdi-swap-horizontal` + chữ); bỏ `.swap-tag` / `.pill-swap`
- [x] Dòng phụ: ô STT để trống, mã B mở đầu bằng `↳` + nhãn **THAY BẰNG** (thay tag “ĐỔI SANG” nền đặc)
- [x] Đồng bộ báo cáo Nhu cầu mua (`.swap-chip`) và Excel (`SWAP_FILL` → `FFFBF4E4`, nhãn dòng phụ “↳ Thay bằng:”)
- [x] Parse/compile lại 8 file — 8/8 sạch
- [x] 26/09/2026 (user: *“cột mã nội bộ ở phiếu xử lý cho bằng với bên phiếu đề xuất”*) — thêm class `.col-code` (`white-space: nowrap; width: 1%`) cho `<th>Mã nội bộ</th>` và 2 ô dữ liệu (dòng chính + dòng phụ) ở cả 2 bảng: cột khít nội dung, không xuống dòng → bảng xử lý (nhiều nhóm cột hơn) trình bày y hệt bảng đề xuất

### Task 2.11 — Fix: popup chọn hàng ở phiếu xử lý không khóa hợp đồng (26/09/2026 — user: *“chọn hàng A của HĐ X rồi sang phiếu xử lý vẫn chọn được hàng của HĐ khác”*)
- [x] Truy nguyên: `supply_handlings/add.vue` KHÔNG truyền `locked-contract-id` cho `GoodsPickerModal` → `activeContractId` = null → `isOtherContract()` luôn false → hàng của mọi HĐ cùng khách đều chọn được. BE `goodsPool()` cố ý trả hàng của mọi HĐ của khách — việc khóa 1 HĐ/phiếu do popup làm.
- [x] Thêm computed `lockedContractId` (contract_id của dòng `in_contract` đầu tiên — kế thừa từ đề xuất) và truyền xuống popup
- [x] Lỗi kèm: template truyền `:exclude-ids` trong khi popup khai prop `excludeKeys` → prop rơi vào attrs, hàng đã có trong phiếu không bị khóa (tick được rồi bị bỏ im lặng lúc confirm). Thêm computed `excludeKeys` (`p:<product_id>`) và sửa template.
- [x] Parse/compile lại 8 file — 8/8 sạch

### Task 2.12 — Fix: dòng phụ mất số liệu nguồn khi mở lại phiếu / sang phiếu xử lý (26/09/2026 — user: *“đề xuất hàng VT-PK-010, sang phiếu xử lý để trống hết”*, đề xuất #50)
- [x] Truy nguyên: `swap_src` (số liệu nguồn của B) chỉ sống ở client — do `onSwapConfirm` copy từ pool, KHÔNG lưu DB, BE không trả → mở lại đề xuất hoặc lập phiếu xử lý từ đề xuất là dòng phụ toàn “—”
- [x] BE: `Transformers/Concerns/ExposesSwapProduct::swapFields()` trả thêm khóa `swap_src` (7 ô: ton_kho / ton_kha_dung / ton_giu / dang_mua / sl_vay / sl_gui / sl_doi), null khi dòng không đổi hàng
- [x] FE: `supply_handlings/add.vue → swapFieldsOf()` copy `swap_src` → kế thừa được cả khi lập từ đề xuất lẫn khi mở lại PXL đã lưu
- [x] Lint PHP + parse/compile 8 file FE — sạch
- [ ] **Chưa wire số thật**: ton_kho / dang_mua / sl_vay / sl_gui / sl_doi đang là placeholder `0` trên TOÀN hệ (2 `Detail*Resource` ghi rõ *“số liệu nguồn realtime — Task sau wire; tạm 0”*), nay thêm `swap_src` là chỗ thứ 3 → wire cả 3 trong cùng 1 Task

### Task 2.13 — Phiếu xử lý ĐẢO VAI dòng chính / dòng phụ (26/09/2026 — user: *“hàng A đã được thay bằng B thì đi mua hàng không quan tâm thông tin của A nữa”*; chốt: phiếu xử lý đảo vai, phiếu đề xuất giữ nguyên)
- [x] `HandlingGoodsTable.vue`: dòng chính hiện mã / mã HH / tên / ĐVT / NK-PPL / số liệu nguồn của **B** (nhóm method `lead*`), giữ chip ĐỔI + mọi ô nhập; bỏ chú thích `.swap-unit-note` (cột ĐVT đã là của B)
- [x] Dòng phụ đổi nhãn **THAY CHO** + thông tin hàng gốc **A**; cột “SL còn lại theo HĐ” chuyển xuống dòng phụ (in đậm `.src-strong`); ô Đặt đơn dòng phụ hiện `dat_don_a` + ĐVT A (phiếu đã lưu không giữ số này → “—”)
- [x] Excel phiếu xử lý (`supply_handlings/add.vue → exportExcel`) đảo vai y hệt, nhãn dòng phụ `↳ Thay cho:`
- [x] Parse/compile 8 file — 8/8 sạch

### Task 2.14 — Tổng SL đề xuất tính theo hàng thay thế B (28/09/2026 — user: *“hàng A hiển thị chỉ để biết sau này trừ vào HĐ, SL đề xuất phải tính từ hàng B”*, đề xuất #50 đang ra 3 thay vì 6)
- [x] Helper `proposalBuyQty(p)` trong `supply_proposals/constants.js`: đã đổi → `swap_quantity`, chưa đổi → `quantity`
- [x] `GoodsTable.vue`: `totalQty` + `countWithQty` dùng helper
- [x] `supply_proposals/add.vue → exportExcel`: dòng tổng cột SL đề xuất dùng helper
- [x] Giữ nguyên: kiểm tra vượt HĐ + SL đã đề xuất theo HĐ (`SupplyProposalService` SUM `spp.quantity`) vẫn theo A — đó là mốc đối trừ hợp đồng. BE `proposedQtyByKey()` đã theo B sẵn.
- [x] Parse/compile 8 file — 8/8 sạch

### Task 2.15 — Đổi tooltip nút Đổi (28/09/2026 — user)
- [x] “Đổi sang hàng khác để giao” → “Đổi sang hàng khác” ở `GoodsTable.vue` + `HandlingGoodsTable.vue`

### Task 2.16 — Cố định cột Định danh khi cuộn ngang — bảng hàng phiếu xử lý (28/09/2026 — user)
- [x] `HandlingGoodsTable.vue`: STT + Mã nội bộ + Mã hàng hóa + Tên thương mại + ĐVT `position: sticky` (thead 2 hàng, dòng chính, dòng phụ đổi hàng, dòng tổng)
- [x] Vị trí `left` đo bằng JS (bề rộng cột thay đổi theo nội dung: chip ĐỔI, nhãn THAY CHO) → CSS var `--stk-1..4`; đo lại khi `updated` + resize
- [x] Ô đầu dòng tổng tách thành `colspan=5` sticky (chữ “N mặt hàng có xử lý” luôn thấy); cột Tên thương mại chặn 160–240px; thêm ResizeObserver
- [x] Parse/compile 8 file — 8/8 sạch

### Task 2.17 — Sắp nút Xóa / Đổi / Bỏ đổi theo đúng dòng + dễ phân biệt (28/09/2026 — user)
- [x] Phiếu xử lý `HandlingGoodsTable.vue`: đã đổi → dòng chính (hàng thay thế) có **Đổi sang hàng khác** + **Bỏ đổi**; dòng phụ (hàng gốc) có **Xóa hàng**. Chưa đổi → giữ Đổi + Xóa trên dòng chính
- [x] Phiếu đề xuất `GoodsTable.vue`: vị trí đã đúng (Xóa ở hàng gốc, Đổi/Bỏ đổi ở dòng hàng thay thế) → chỉ đồng bộ icon/tooltip
- [x] Icon phân biệt: Đổi = `mdi-swap-horizontal` (xanh mặc định), Bỏ đổi = `mdi-undo-variant` (cam, không đỏ), Xóa = `mdi-trash-can-outline` đỏ + tooltip "Xóa hàng"
- [x] Parse/compile 8 file

### Task 2.18 — Phiếu đề xuất cũng ĐẢO VAI cho giống phiếu xử lý (28/09/2026 — user chọn phương án 1)
- [x] `GoodsTable.vue`: đã đổi → dòng chính = hàng thay thế B (mã/HH/tên/ĐVT/NK-PPL/số liệu nguồn của B, ô SL = `swap_quantity`, nút Đổi + Bỏ đổi); dòng phụ "THAY CHO" = hàng gốc A (số liệu nguồn của A, "SL còn lại HĐ" in đậm, ô SL = `quantity` theo HĐ + cảnh báo vượt HĐ, nút Xóa)
- [x] Tô đỏ vượt HĐ chuyển xuống dòng hàng gốc khi đã đổi
- [x] `supply_proposals/add.vue` — Excel: dòng chính theo B, dòng phụ `↳ Thay cho: A`
- [x] Cập nhật spec mục 6.4
- [x] Parse/compile 8 file

### Task 2.19 — Phiếu xử lý: "SL hàng gốc tương ứng" khi đổi hàng (28/09/2026 — user chọn phương án a)
Kịch bản: đề xuất A 60 thùng → phiếu xử lý đổi sang B 140 hộp, tương ứng 70 thùng A. Hệ thống không tự quy đổi A↔B (2 mã khác nhau) → người lập nhập tay.
- [x] BE migration `2026_09_28_000001_add_swap_origin_quantity_to_supply_handling_products_table` — cột `swap_origin_quantity decimal(15,3) null` sau `swap_quantity` (không khóa ngoại; DB chưa có dòng PXL đổi hàng → không backfill)
- [x] BE `SupplyHandlingService::syncProducts` lưu `swap_origin_quantity` (chỉ dòng đã đổi, còn lại null)
- [x] BE `StoreSupplyHandlingRequest`: rule numeric min:0 + dòng đã đổi bắt buộc > 0
- [x] BE `handledDetailByProduct` thêm `qty_a[product_id]` = SL A tương đương đã xử lý (dòng đổi: `origin × Σphân bổ ÷ dat_don`; dòng không đổi: Σphân bổ)
- [x] BE `SupplyProposal::isFullyHandled` so theo ĐVT hàng gốc A (Σ quantity đề xuất vs Σ qty_a) — PXL đổi sang B' khác đề xuất vẫn được tính
- [x] BE `proposedQtyMap` (hàm dùng chung — user đã đồng ý): dòng đề xuất có PXL đổi hàng đang hiệu lực → HĐ bị đối trừ `max(SL đề xuất, Σ SL A theo PXL)`
- [x] BE resource: đề xuất trả `sl_da_xu_ly_a`; PXL trả `swap_origin_quantity` + `sl_con_de_xuat_a` (SL A còn lại theo đề xuất, null nếu hàng không thuộc đề xuất)
- [x] FE `HandlingGoodsTable.vue`: dòng "THAY CHO" có ô nhập SL hàng gốc tương ứng (ĐVT A) + cảnh báo vượt đề xuất (cam, không chặn) / vượt SL còn lại HĐ (đỏ)
- [x] FE `supply_handlings/add.vue`: prefill theo `sl_da_xu_ly_a`; onSwapConfirm mặc định origin = SL đặt đơn A; clearSwap trả dat_don = origin; mapHandlingItem đọc lại; banner vượt HĐ quy về A; banner cảnh báo vượt đề xuất; validate origin > 0; Excel dòng phụ dùng origin
- [x] Cập nhật spec 6.4; `php -l` + migrate; parse/compile FE

### Task 2.20 — Báo cáo Nhu cầu mua: bỏ cột riêng "Thay thế cho" (28/09/2026 — user)
- [x] Web: gộp "⇄ ĐỔI · thay cho <mã A>" (tooltip tên A) vào ô "Phiếu đề xuất mua", dưới dòng "từ DX-…"; bỏ th/td riêng, colspan nhóm "Chi tiết đề xuất mua" 10→9, ô rỗng 18/17→17/16; sửa ghi chú cuối bảng
- [x] Excel: bỏ cột "Thay thế cho", ghi thêm dòng "⇄ Thay cho: <mã A · tên A>" trong ô "Phiếu XLCU"
- [x] Parse/compile

### Task 2.21 — Phiếu xử lý: ô nhập dùng base component + nới rộng cột Đơn giá (28/09/2026)
- [x] FE `HandlingGoodsTable.vue`: Đơn giá → `base-currency-input` (phân cách hàng nghìn, căn phải), cột rộng hơn (~130px)
- [x] FE `HandlingGoodsTable.vue`: Đặt đơn / phân bổ / SL hàng gốc tương ứng → `base-input-field type="number"`; điều hướng bàn phím `@keydown.native`
- [x] CSS: style ô nhập qua `>>>` (input nằm trong base component), giữ cao 28px + viền focus
- [x] Verify compile `verify_vue.js`

### Task 2.22 — Fix: PXL khách lẻ / HĐ đặt-mượn / trao tặng / nguyên tắc kẹt "Chờ duyệt" (28/09/2026)
Bug: `SupplyHandlingService::submitStatus()` chỉ cho type 1 (KH) chốt luôn 5, type 3-6 rơi vào Chờ duyệt (3) nhưng
bước duyệt (`guardApprove`, `can_approve`, FE `showApproveActions`) chỉ dành cho Nội bộ → phiếu kẹt, không lên BC nhu cầu mua (VD PXL-2026-0019).
- ~~BE `submitStatus`: chỉ Nội bộ → Chờ duyệt~~ → user chốt: GIỮ Chờ duyệt cho type 2-6, bổ sung nút duyệt
- [x] BE `SupplyHandling::canApprove()` (inline): type != 1 + Chờ duyệt + quyền "Duyệt phiếu xử lý cung ứng"; `guardApprove` + 2 resource `can_approve` dùng chung
- [x] FE `add.vue` `showApproveActions`: bỏ điều kiện chỉ Nội bộ, dựa vào `can_approve` của BE

### Task 2.23 — PXL đang Chờ duyệt không được sửa (28/09/2026)
- [x] BE `SupplyHandling::getIsCanEditAttribute`: bỏ Chờ duyệt → chỉ Nháp / Từ chối duyệt (API update đã chặn theo is_can_edit; FE nút Sửa theo is_can_edit)
- [x] BE `getIsCanDeleteAttribute` (user chốt): chỉ người tạo, khi Nháp / Từ chối duyệt; Chờ duyệt không xóa được

### Task 2.24 — Đơn mua hàng / HĐ mua: nhãn "thay cho" ở nguồn/mục đích (28/09/2026)
Chốt: chỉ hiện NỘI BỘ ở phần nguồn (purposes) của từng dòng hàng; KHÔNG đưa lên dòng hàng chính, bản in / Excel gửi NCC.
Không migration — ghi thêm `swap_for_code` / `swap_for_name` vào từng phần tử JSON `purposes`. Phiếu đã lập trước không có.
- [x] FE báo cáo nhu cầu mua: 2 chỗ dựng purposes (Lập HĐ mua / Lập đơn mua) thêm swap_for_code/name
- [x] FE `purchase_contracts/GoodsPickerModal.vue` + `purchase_orders/GoodsPickerModal.vue`: thêm swap_for_code/name khi dựng purposes
- [x] FE `purchase_contracts/ProductsTab.vue` + `purchase_orders/ProductsTab.vue`: nhãn `⇄ ĐỔI · thay cho <mã A>` (tooltip mã · tên) ở dòng nguồn; điều kiện chống trùng khi ghép purposes thêm swap_for_code
- [x] BE: kiểm tra request/service giữ nguyên key mới trong purposes (không lọc bỏ) — json_encode nguyên mảng, không cần sửa
- [x] Verify compile

### Task 2.25 — Đổi hàng trên Đơn mua hàng / HĐ mua (28/09/2026) — spec mục 10
Chốt: NCC không có hàng → đổi dòng sang C trên đơn mua / HĐ mua; C làm mã chính, hàng gốc ở `swap_from_*`; không ghi ngược PXL.
- [x] BE migration `swap_from_*` (10 cột, index swap_from_product_id) cho 2 bảng dòng hàng + chạy migrate
- [x] BE `syncProducts` 2 service + 2 Detail resource + 2 Request (rule swap_from_*)
- [x] BE tra theo hàng gốc: `SyncsNoteToQuotation`, `SupplyNoteLookupService`, `purchaseContractsByProduct`
- [x] BE endpoint `GET purchase-orders/swap-catalog`
- [x] FE `SwapProductModal.vue` dùng chung
- [x] FE `purchase_orders/ProductsTab.vue`: nút Đổi / Bỏ đổi, hiển thị hàng gốc, refs theo hàng gốc, lineKey / excludeCodes
- [x] FE `purchase_contracts/ProductsTab.vue`: như trên
- [x] php -l + verify_vue
- [x] Gọn giao diện dòng đã đổi (user chốt "gọn 1 dòng"): bỏ chip ở cột Mã, dưới tên 1 dòng `[⇄ Đổi NCC] thay <mã gốc> (i)` + tooltip tên / SL gốc, viền trái vàng ở cột STT
- [x] Bỏ chip "Đổi NCC": dưới tên chỉ ghi `thay <mã gốc>`; tooltip / nút không nhắc NCC
- [x] SL hàng gốc THEO TỪNG HĐ BÁN (user chốt 28/09/2026): purposes[].swapOrigQty (ĐVT hàng gốc); `swap_from_quantity` = Σ (dòng không phiếu nhập trực tiếp)
  - [x] Popup: sau khi chọn hàng mới, bảng từng phiếu / HĐ bán nhập SL gốc (A) + SL mua hàng mới (C); HĐ nguyên tắc không hỏi SL
  - [x] 2 ProductsTab: ô `= [SL gốc] <ĐVT A>` cạnh ô "Mua" từng phiếu (dòng đã đổi); dòng ngoài phiếu có ô cấp dòng; Bỏ đổi trả SL mua về SL gốc
  - [x] BE request: `swap_from_quantity` bắt buộc > 0 khi có `swap_from_product_id` (đơn mua; HĐ mua chỉ loại thương mại)
  - [x] BE service: `swap_from_quantity` = Σ purposes[].swapOrigQty (tự tính lại khi lưu)
  - [x] verify_vue + php -l + test BE (swapFromColumns + rule đơn mua) OK
- [x] Chỉ cho đổi hàng ở dòng CÓ HĐ BÁN (user chốt 28/09/2026): dòng có ít nhất 1 phiếu gắn HĐ bán
  - [x] FE 2 ProductsTab: ẩn nút Đổi ở dòng không có HĐ bán (nút Bỏ đổi vẫn giữ cho dữ liệu cũ); chặn cả trong openSwap
  - [x] BE 2 request: dòng mới đổi mà không có HĐ bán → báo lỗi
  - [x] verify_vue + php -l + test BE
- [x] Quy đổi theo TỶ LỆ cho cả dòng (user chốt 28/09/2026 — thay cách nhập 2 số từng HĐ của Task 2.26)
  - [x] BE migration cột `swap_ratio` decimal(18,6) null (2 bảng, không khóa ngoại) + resource + request (bắt buộc > 0 khi đã đổi)
  - [x] BE service: lưu swap_ratio; purposes[].swapOrigQty = buyQty ÷ tỷ lệ, swap_from_quantity = Σ (tự tính lại)
  - [x] FE popup: ô "1 <ĐVT A> = [x] <ĐVT C>"; bảng từng HĐ chỉ nhập SL mua C, cột "Trừ HĐ" tự tính; SL mua tự theo tỷ lệ nếu chưa gõ tay
  - [x] FE 2 ProductsTab: bỏ ô nhập SL gốc; hiện "thay <mã> · 1 A = x C", mỗi phiếu "ĐX 10 hộp → Mua [20] vỉ (trừ HĐ 10 hộp)"; SL gốc tự tính khi sửa SL mua; đổi ĐVT hàng mới thì quy đổi lại tỷ lệ, không quy đổi SL đề xuất (theo ĐVT hàng gốc)
  - [x] verify_vue + php -l + test BE
- [x] Fix popup đổi hàng: chọn hàng xong nút "Đổi hàng" bị khóa mà không thấy vì sao (ô tỷ lệ bắt buộc nằm dưới danh sách, phải cuộn mới thấy)
  - [x] Chọn hàng → tự cuộn tới khối quy đổi + focus ô tỷ lệ; danh sách thu thấp khi đã chọn
  - [x] Footer hiện lý do khóa nút (thiếu tỷ lệ / SL mua sai)

### Task 2.29 — HOÀN TÁC đổi hàng trên Đơn mua / HĐ mua (user yêu cầu 28/09/2026)
Gỡ toàn bộ Task 2.25 → 2.28 + fix popup. GIỮ Task 2.24 (nhãn "⇄ ĐỔI thay cho <mã>" từ PXL, swap_for_code/name trong purposes).
- [x] DB: rollback 2 migration `2026_09_28_000002` (swap_from_*) + `2026_09_28_000003` (swap_ratio), xóa file
- [x] BE: PurchaseOrderService / PurchaseContractService (swapFromColumns, swapPurposes, ghi cột), 2 Store request (rule + withValidator đổi hàng), 2 Detail resource, endpoint swap-catalog (controller + route), tra theo hàng gốc (SyncsNoteToQuotation, SupplyNoteLookupService, SupplyReportService::purchaseContractsByProduct)
- [x] FE: xóa `SwapProductModal.vue`; 2 ProductsTab bỏ cột Thao tác đổi/bỏ đổi, swap-from, SWAP_KEYS, syncSwapOrig, applySwapQty…, lineKey/excludeCodes/refs theo hàng gốc, giá báo giá/chiết khấu dòng đã đổi (HĐ mua)
- [x] Spec mục 10 ghi "đã hoàn tác"; php -l + verify_vue

### Task 2.30 — Đơn mua: nới rộng 3 cột Ghi chú báo giá / thầu / hợp đồng (user yêu cầu 28/09/2026)
- [x] FE `purchase_orders/components/ProductsTab.vue`: `td.cell-ref-note` min-width 120 → 200px, max-width 220 → 320px
- [x] FE `purchase_contracts/components/ProductsTab.vue` (HĐ mua): làm tương tự (user yêu cầu)

### Task 2.31 — Đổi hàng trên Đơn mua / HĐ mua — làm lại theo khối cặp như PXL (user chốt 28/09/2026) — spec mục 11
Chốt: khách đổi hàng ở khâu mua; thao tác + hiển thị như PĐX/PXL (nút Đổi → chọn 1 hàng, khối cặp: dòng chính hàng mới C,
dòng phụ `↳ THAY CHO <A>`); SL hàng gốc nhập TỪNG PHIẾU / HĐ bán ngay trên dòng phụ (không popup, không tỷ lệ);
SL gốc chỉ dùng cảnh báo vượt đề xuất / vượt SL còn lại HĐ (không chặn lưu); PXL đã đổi A→B thì hàng gốc = A; làm cả HĐ mua.
- [x] BE migration 9 cột `swap_from_*` cho `purchase_order_products` + `purchase_contract_products` (index, không khóa ngoại) + migrate
- [x] BE báo cáo Nhu cầu mua: lines[] trả thêm `swap_for_product_id` / `swap_for_unit_id` / `swap_for_unit_name` / `swap_for_qty` (SL A tương ứng)
- [x] BE 2 service `syncProducts` ghi `swap_from_*` (dòng không đổi → null cả khối) + 2 Detail resource trả về
- [x] BE 2 Store request: rule `swap_from_*`; dòng đã đổi phải có HĐ bán, mỗi phiếu `swapOrigQty` > 0 (HĐ nguyên tắc bỏ qua SL)
- [x] BE endpoint `POST purchase-orders|purchase-contracts/swap-info` (quy cách hàng mới + SL còn lại theo HĐ của hàng gốc theo cặp hàng × HĐ) — method mới `purchaseSwapInfo` trong trait, không sửa hàm cũ
- [x] FE GoodsPickerModal (đơn mua + HĐ mua): chuyển tiếp `swap_for_product_id/unit/qty` vào purposes
- [x] FE `purchase_orders/ProductsTab.vue`: cột Thao tác (Đổi / Bỏ đổi / Xóa), picker chọn 1 hàng, khối cặp, ô SL gốc từng phiếu, cảnh báo, refs theo hàng gốc, excludeCodes, ĐVT C không quy đổi SL đề xuất
- [x] FE `purchase_contracts/ProductsTab.vue`: như trên (+ giá báo giá / chiết khấu dòng đã đổi, HĐ nguyên tắc không hỏi SL gốc)
- [x] php -l + verify_vue + test lưu BE (transaction rollback)

### Task 2.32 — Phiếu đề xuất: bỏ tooltip ô SL đề xuất dòng đã đổi (user yêu cầu 28/09/2026)
- [x] FE `supply_proposals/components/GoodsTable.vue`: bỏ `v-b-tooltip` "SL theo ĐVT của hàng thay thế — không quy đổi từ SL hàng gốc" trên ô nhập `swap_quantity`
- [x] FE `supply_proposals/components/GoodsTable.vue`: bỏ `v-b-tooltip` "SL theo hợp đồng của hàng gốc (ĐVT hàng gốc) — dùng để đối trừ hợp đồng" trên ô nhập `quantity` dòng hàng gốc
- [x] FE `supply_handlings/components/HandlingGoodsTable.vue` (Phiếu xử lý): bỏ `v-b-tooltip` "SL hàng gốc tương ứng (ĐVT hàng gốc) — dùng để đối trừ hợp đồng" trên ô nhập `swap_origin_quantity`
- [x] FE GoodsTable (Phiếu đề xuất) + HandlingGoodsTable (Phiếu xử lý): bỏ `v-b-tooltip` "SL còn lại theo HĐ của hàng gốc — mốc đối trừ hợp đồng" trên số SL còn lại theo HĐ dòng hàng gốc

### Task 2.33 — Đơn mua: cột Thao tác lên cạnh cột Tên hàng hóa (giống plan/quotation/add) (user yêu cầu 29/09/2026)
- [x] FE `purchase_orders/components/ProductsTab.vue`: th/td Thao tác chuyển ngay sau Tên hàng hóa, đông cứng (`col-freeze col-act`, left = STT + Mã + Tên); mốc `col-freeze-last` chuyển sang cột Thao tác (readonly vẫn là Tên hàng hóa)
- [x] Dòng phụ ĐỔI HÀNG thêm ô trống cột Thao tác, colspan cuối 11/10 → 10; dòng TỔNG CỘNG colspan 3 → 4 (bỏ ô trống cuối); verify_vue

### Task 2.34 — Đơn mua: thu nhỏ icon nút cột Thao tác cho đỡ tốn diện tích (user yêu cầu 29/09/2026)
- [x] FE `purchase_orders/components/ProductsTab.vue`: trong `td.cell-act` giảm padding nút (5px → 3px), icon mdi 14px, ảnh thùng rác 14px, khoảng cách 3px; `$w-act` 104 → 84px (không sửa `.btn-small` dùng chung); verify_vue

### Task 2.35 — Đơn mua: cột Thao tác hẹp thêm (user yêu cầu 29/09/2026)
- [x] FE `purchase_orders/components/ProductsTab.vue`: `$w-act` 84 → 72px; nút padding 3 → 2px, khoảng cách 3 → 2px, đệm ngang ô `td.cell-act` 6 → 3px; verify_vue

### Task 2.36 — HĐ mua: cột Thao tác lên cạnh Tên hàng hóa + thu gọn nút (như Task 2.33–2.35) (user yêu cầu 29/09/2026)
- [x] FE `purchase_contracts/components/ProductsTab.vue`: th/td Thao tác chuyển ngay sau Tên hàng hóa, đông cứng (`col-freeze col-freeze-last col-act`, `$w-act` 72px); Tên hàng hóa bỏ `col-freeze-last`, thêm vạch ngăn inset
- [x] Dòng phụ ĐỔI HÀNG thêm ô trống cột Thao tác, colspan gợi ý `isTm ? 10 : 8` → `9 : 7`; dòng TỔNG CỘNG colspan 3 → 4, bỏ 1 ô trống cuối
- [x] Nút trong `td.cell-act`: padding 2px, icon/ảnh 14px, khoảng cách 2px, đệm ngang ô 3px (không sửa `.btn-small` chung); verify_vue

## Phase 3 — Kiểm thử (user)

- [ ] 1. Đề xuất: chọn A → đổi B → SL B mặc định = SL A → sửa SL B → lưu nháp → mở lại đúng
- [ ] 2. Đổi rồi bỏ đổi → DB `swap_*` null sạch
- [ ] 3. Gửi đề xuất → lập phiếu xử lý → kế thừa B, `dat_don` = SL B
- [ ] 4. PXL đổi sang B' khác → đề xuất không đổi theo, hiện cảnh báo dưới bảng
- [ ] 5. Validate: B trùng A → chặn; SL B = 0 → chặn
- [ ] 6. Báo cáo Nhu cầu mua: ra mã B + ô "Phiếu đề xuất mua" có nhãn "⇄ ĐỔI · thay cho <mã A>" (không còn cột riêng)
- [ ] 7. Export Excel 2 phiếu + báo cáo có dòng phụ / cột "Thay thế cho"
- [ ] 8. Regression: phiếu cũ không đổi hàng hiển thị & số liệu y như trước
- [ ] 9. Dòng hàng chọn thêm **ngoài hợp đồng**: không có nút Đổi ở cả 2 màn
- [ ] 10. Phiếu xử lý → nút **Chọn hàng hóa**: chỉ tick được hàng của đúng HĐ đề xuất đang bám + hàng ngoài HĐ; hàng HĐ khác bị mờ, có dòng ghi chú “Phiếu đang bám hợp đồng …”; hàng đã có trong phiếu hiện nhãn “đã thêm” và bị khóa
- [ ] 12. Đơn mua / HĐ mua (Nháp): dòng có HĐ bán → nút Đổi → chọn C → khối cặp (dòng chính C chip ĐỔI, dòng phụ `↳ THAY CHO A`), ô Gốc từng phiếu mặc định = SL mua → Lưu → mở lại đúng
- [ ] 13. Nhập SL gốc > ĐX → chip cam "Vượt đề xuất"; Σ SL gốc cùng HĐ > "HĐ còn" → chip đỏ "Vượt SL còn lại HĐ"; vẫn lưu được. SL gốc = 0 khi có SL mua → báo lỗi
- [ ] 14. Bỏ đổi → quay về A, SL mua = SL gốc; PXL đã đổi A→B rồi đơn mua đổi B→C → dòng phụ hiện A (không phải B)
- [ ] 15. HĐ mua: dòng đã đổi — Đơn giá báo giá là giá của A (tooltip ghi rõ), Chiết khấu = 0; HĐ nguyên tắc không có ô Gốc
- [ ] 11. Đề xuất A 60 thùng → PXL đổi B 140 hộp, **SL hàng gốc tương ứng** nhập 70 → cảnh báo cam "Vượt đề xuất 10", banner vàng, vẫn lưu được; gửi PXL → đề xuất "Đã xử lý"; lập đề xuất mới cùng HĐ → SL còn lại HĐ đã trừ 70 (không phải 60); Bỏ đổi → Đặt đơn = 70

---

## Checkpoint

---
### Checkpoint — 2026-09-28 (đổi hàng đơn mua / HĐ mua — khối cặp như PXL)
Vừa hoàn thành: Task 2.31 — BE (migration 9 cột `swap_from_*`, lưu / đọc, validate, endpoint `swap-info`) + FE 2 ProductsTab (cột Thao tác Đổi / Bỏ đổi / Xóa, popup chọn 1 hàng dùng chung PXL, khối cặp chip ĐỔI + dòng phụ `↳ THAY CHO`, ô Gốc từng phiếu, cảnh báo vượt ĐX / vượt SL còn lại HĐ, refs HĐ bán theo hàng gốc; HĐ mua: giá báo giá = giá A, chiết khấu 0, HĐ nguyên tắc không có ô Gốc). verify_vue 2 file OK, php -l 12 file OK, test lưu + resource + validate (t2.php, rollback) OK cả đơn mua lẫn HĐ mua.
Đang làm dở: —
Bước tiếp theo: build lại client + user test tay case 12 → 15 (Phase 3). Chưa làm: Excel đơn mua / HĐ mua, đối trừ HĐ bán theo `swapOrigQty` ở các màn sau (hóa đơn / xuất kho).
Blocked:

---
### Checkpoint — 2026-09-28 (hoàn tác đổi hàng đơn mua / HĐ mua)
Vừa hoàn thành: Task 2.29 — gỡ toàn bộ đổi hàng trên đơn mua / HĐ mua (Task 2.25 → 2.28 + fix popup). DB: chạy down() + xóa dòng `migrations` + xóa file 2 migration `2026_09_28_000002` / `000003` (2 bảng không còn cột swap_*). BE: trả về bản gốc controller, route, 2 service, 2 Store request, 2 Detail resource, SyncsNoteToQuotation, SupplyNoteLookupService; gỡ tay hunk `purchaseContractsByProduct` trong SupplyReportService (giữ phần PXL / swap_for_*). FE: xóa SwapProductModal.vue; 2 ProductsTab trả về bản gốc rồi gắn lại riêng phần 2.24 (chip "⇄ ĐỔI thay cho <mã>", điều kiện gộp phiếu theo swap_for_code, CSS pp-swap). Spec mục 10 ghi "đã hoàn tác". php -l + verify_vue sạch, grep không còn swap_from_ / swap_ratio / SwapProductModal / swap-catalog.
Đang làm dở: —
Bước tiếp theo: user test tay đơn mua / HĐ mua (tạo / sửa / lưu bình thường, nhãn "⇄ ĐỔI thay cho" từ PXL đã đổi vẫn hiện); tiếp tục Phase 3 kiểm thử đổi hàng phiếu đề xuất / PXL.
Blocked:
### Checkpoint — 2026-09-28 (quy đổi theo tỷ lệ)
Vừa hoàn thành: Đổi hàng đơn mua / HĐ mua quy đổi theo TỶ LỆ cả dòng — BE cột `swap_ratio` (migrate đã chạy) + `swapPurposes` tự tính `swapOrigQty = buyQty ÷ tỷ lệ` + rule bắt buộc > 0; FE popup ô "1 A = [x] C" + bảng chỉ nhập SL mua, cột "Trừ HĐ bán" tự tính; 2 ProductsTab bỏ ô SL gốc, hiện "thay <mã> · 1 A = x C" và "(trừ HĐ x A)", `syncSwapOrig`, đổi ĐVT quy đổi lại tỷ lệ, không quy đổi SL đề xuất. verify_vue + php -l + test BE (t228.php) đạt.
Đang làm dở: —
Bước tiếp theo: user test tay trên đơn mua / HĐ mua (đổi hàng khác ĐVT, sửa SL mua, đổi ĐVT, bỏ đổi); sau đó làm phần đối trừ HĐ bán theo `swapOrigQty`.
Blocked:

### Checkpoint — 28/09/2026 (chỉ đổi hàng có HĐ bán)
Vừa hoàn thành: Task 2.27 — nút Đổi chỉ hiện ở dòng có ít nhất 1 phiếu gắn HĐ bán (contract_id / saleContract_id), openSwap chặn thêm; BE 2 request báo "Chỉ đổi được hàng có hợp đồng bán." cho dòng đã đổi mà không có HĐ bán. verify_vue sạch, php -l OK, test validator 5 case × 2 request OK
Đang làm dở: —
Bước tiếp theo: user test tay đơn mua / HĐ mua Nháp: dòng không HĐ bán không có nút Đổi; dòng có HĐ bán đổi + nhập SL quy đổi → Lưu → mở lại. Sau đó làm đối trừ HĐ bán theo swapOrigQty
Blocked:

### Checkpoint — 28/09/2026 (SL hàng gốc theo từng HĐ bán)
Vừa hoàn thành: Task 2.26 — popup đổi hàng có bảng "Quy đổi số lượng" theo từng phiếu / HĐ bán (SL mua hàng mới = SL hàng gốc được thay); bảng hàng hiện `Mua [x] ĐVT mới = [y] ĐVT gốc`, sửa được; purposes[].swapOrigQty, swap_from_quantity = Σ (BE tự tính lại); đơn mua bắt buộc SL gốc > 0 khi đã đổi, HĐ mua chỉ bắt buộc khi thương mại; Bỏ đổi trả SL mua về SL gốc; cảnh báo vượt/thiếu đề xuất so theo SL gốc. verify_vue sạch, php -l OK, test BE OK
Đang làm dở: —
Bước tiếp theo: user test tay đơn mua / HĐ mua (Nháp) có 2 phiếu đề xuất: Đổi hàng → nhập 2 cặp số → Lưu → mở lại; sửa ô SL gốc trên bảng; Bỏ đổi. Sau đó mới làm đối trừ HĐ bán theo swapOrigQty (chưa có chỗ nào đọc)
Blocked:

### Checkpoint — 28/09/2026 (đổi hàng trên đơn mua / HĐ mua)
Vừa hoàn thành: Task 2.25 — BE 10 cột swap_from_* + lưu/đọc + tra theo hàng gốc + endpoint swap-catalog; FE popup `SwapProductModal.vue` dùng chung, 2 ProductsTab có cột Thao tác (Đổi / Bỏ đổi / Xóa), chip ĐỔI + dòng "thay cho", refs HĐ bán theo hàng gốc, lineKey / excludeCodes gồm mã gốc; HĐ mua: giá báo giá dòng đã đổi không quy đổi, chiết khấu = 0, HĐ nguyên tắc không hỏi SL gốc. verify_vue sạch, test lưu BE (rollback) OK
Đang làm dở: —
Bước tiếp theo: user test tay đơn mua / HĐ mua ở trạng thái Nháp: Đổi hàng → Lưu → mở lại; thử Bỏ đổi, đổi tiếp C → D
Blocked:

### Checkpoint — 28/09/2026 (nhãn "thay cho" ở đơn mua / HĐ mua)
Vừa hoàn thành: Task 2.24 — purposes mang thêm swap_for_code/swap_for_name (báo cáo nhu cầu mua + 2 GoodsPickerModal); ProductsTab đơn mua / HĐ mua hiện nhãn `⇄ ĐỔI thay cho <mã>` + tooltip ở dòng nguồn. Bản in / Excel NCC không đổi. verify_vue sạch
Đang làm dở: —
Bước tiếp theo: user lập đơn mua / HĐ mua MỚI từ báo cáo nhu cầu mua với phiếu có đổi hàng → kiểm tra nhãn ở cột nguồn (phiếu cũ không có nhãn)
Blocked:

### Checkpoint — 28/09/2026 (khóa sửa/xóa PXL Chờ duyệt)
Vừa hoàn thành: Task 2.23 — `SupplyHandling` is_can_edit + is_can_delete: chỉ người tạo, trạng thái Nháp / Từ chối duyệt. Chờ duyệt khóa hẳn, chỉ còn Duyệt / Từ chối duyệt (Task 2.22)
Đang làm dở: —
Bước tiếp theo: user kiểm tra danh sách PXL — phiếu Chờ duyệt không còn nút Sửa/Xóa; phiếu Từ chối duyệt có Sửa + Xóa
Blocked:

### Checkpoint — 28/09/2026 (bước duyệt cho PXL khách lẻ / HĐ đặt-mượn / trao tặng / nguyên tắc)
Vừa hoàn thành: Task 2.22 — `SupplyHandling::canApprove()` (type != 1 + Chờ duyệt + quyền), dùng cho `guardApprove` + `can_approve` ở 2 resource; FE `showApproveActions` bỏ điều kiện chỉ Nội bộ. `submitStatus` giữ nguyên (type 1 chốt luôn, còn lại Chờ duyệt). php -l + verify_vue sạch
Đang làm dở: —
Bước tiếp theo: user mở PXL-2026-0019 (id 32) bằng tài khoản có quyền "Duyệt phiếu xử lý cung ứng" → bấm Duyệt → kiểm tra BC nhu cầu mua có mã 557-172 SL 91
Blocked:

### Checkpoint — 28/09/2026 (ô nhập base component + cột Đơn giá)
Vừa hoàn thành: Task 2.21 — `HandlingGoodsTable.vue`: Đơn giá dùng `base-currency-input` (phân cách hàng nghìn, cột min 140px, ô 130px); Đặt đơn / phân bổ / SL hàng gốc tương ứng dùng `base-input-field type="number"` (ô 72px); điều hướng bàn phím chuyển sang `@keydown.native` (data-grid-cell đi qua $attrs xuống input bên trong); CSS đè khung viền base qua `>>>`. verify_vue.js sạch
Đang làm dở: —
Bước tiếp theo: user xem lại trên /supply/supply_handlings/add?proposal_id=52 (gõ đơn giá có dấu phẩy, ↑↓←→/Enter chuyển ô). Hỏi có chuyển luôn ô nhập native ở `supply_proposals/components/GoodsTable.vue` không
Blocked:

### Checkpoint — 28/09/2026 (bỏ cột "Thay thế cho" ở báo cáo Nhu cầu mua)
Vừa hoàn thành: Task 2.20 — gộp nhãn đổi hàng vào ô "Phiếu đề xuất mua" (web) và ô "Phiếu XLCU" (Excel), bỏ cột riêng, chỉnh colspan
Đang làm dở: —
Bước tiếp theo: user xem lại báo cáo Nhu cầu mua + test Phase 3
Blocked:

### Checkpoint — 28/09/2026 (SL hàng gốc tương ứng trên phiếu xử lý)
Vừa hoàn thành: Task 2.19 — cột `swap_origin_quantity` (đã migrate trên thanhan_stag_07052026), BE lưu/validate/resource, `qty_a` + `isFullyHandled` theo A, `proposedQtyMap` đối trừ HĐ theo PXL khi đổi hàng; FE ô nhập ở dòng THAY CHO + cảnh báo vượt đề xuất / vượt HĐ + banner + Excel. Đã chạy thử giả lập trong transaction (rollback): đề xuất 5, PXL đổi origin 7 → HĐ đối trừ 35→37; phân bổ 14/14 → qty_a 7, 7/14 → 3.5
Đang làm dở: —
Bước tiếp theo: user test trên màn hình (đề xuất A 60 → PXL đổi B 140 hộp, nhập 70 → cảnh báo vượt đề xuất 10, lưu được; mở popup chọn hàng đề xuất mới xem SL còn lại HĐ đã trừ 70)
Blocked:

### Checkpoint — 28/09/2026 (cố định cột Định danh)
Vừa hoàn thành: Task 2.15 (tooltip nút Đổi) + Task 2.16 — bảng hàng phiếu xử lý cố định STT + 4 cột Định danh khi cuộn ngang.
Đang làm dở: không có.
Bước tiếp theo: user reload `/supply/supply_handlings/add?proposal_id=51` kiểm tra cuộn ngang.
Blocked:

---

### Checkpoint — 28/09/2026 (phiếu đề xuất đảo vai)
Vừa hoàn thành: Task 2.18 — phiếu đề xuất đảo vai giống phiếu xử lý (B dòng chính, A dòng phụ "THAY CHO" giữ SL theo HĐ + cảnh báo vượt HĐ), Excel đề xuất đảo theo, spec 6.4 cập nhật. Parse/compile 8/8 sạch.
Đang làm dở: không có.
Bước tiếp theo: user reload đề xuất #50 (xem + sửa) kiểm tra thứ tự dòng, ô SL 2 dòng, nút, Excel.
Blocked:

---

### Checkpoint — 28/09/2026 (sắp lại nút Xóa / Đổi / Bỏ đổi)
Vừa hoàn thành: Task 2.17 — phiếu xử lý: đã đổi thì dòng hàng thay thế có Đổi sang hàng khác + Bỏ đổi (cam, `mdi-undo-variant`), dòng hàng gốc có Xóa; phiếu đề xuất đồng bộ icon/tooltip. Parse/compile 8/8 sạch.
Đang làm dở: không có.
Bước tiếp theo: user reload phiếu xử lý `?proposal_id=51` + đề xuất #50 kiểm tra nút.
Blocked:

---

### Checkpoint — 28/09/2026 (tổng SL đề xuất theo B)
Vừa hoàn thành: Task 2.14 — helper `proposalBuyQty()`; tổng SL đề xuất trên bảng + Excel phiếu đề xuất tính theo SL hàng thay thế (đề xuất #50: 3 → 6).
Đang làm dở: không có.
Bước tiếp theo: user xem lại đề xuất #50; chốt có sửa `purchase_orders/components/SupplyDocDetailModal.vue` (chưa hiểu đổi hàng) không.
Blocked:

---

### Checkpoint — 26/09/2026 (đảo vai phiếu xử lý)
Vừa hoàn thành: Task 2.13 — phiếu xử lý: hàng thay thế B làm dòng chính, hàng gốc A xuống dòng phụ “THAY CHO” (màn hình + Excel). Phiếu đề xuất giữ nguyên.
Đang làm dở: không có.
Bước tiếp theo: user xem lại phiếu xử lý lập từ đề xuất #50.
Blocked: wire số liệu nguồn thật; ẩn hẳn hay làm mờ hàng HĐ khác ở popup phiếu xử lý.

---

### Checkpoint — 26/09/2026 (dòng phụ mất số liệu nguồn)
Vừa hoàn thành: Task 2.12 — BE trả `swap_src` trong khối swap_*, FE phiếu xử lý kế thừa lại.
Đang làm dở: không có.
Bước tiếp theo: chốt Task wire số liệu nguồn thật (tồn kho / đang mua / vay / gửi / đổi) cho cả dòng chính lẫn dòng phụ.
Blocked: cách nhập SL khi dòng đã đổi; ẩn hẳn hay chỉ làm mờ hàng HĐ khác ở popup phiếu xử lý.

---

### Checkpoint — 26/09/2026 (fix popup phiếu xử lý không khóa HĐ)
Vừa hoàn thành: Task 2.11 — `supply_handlings/add.vue` truyền `locked-contract-id` + `exclude-keys` đúng tên prop cho `GoodsPickerModal`.
Đang làm dở: không có.
Bước tiếp theo: user build lại và thử kịch bản 10 ở Phase 3.
Blocked: vẫn chưa chốt cách nhập SL khi dòng đã đổi; và chưa chốt có ẩn HẴN hàng HĐ khác ở phiếu xử lý (dùng `source-contract-id`) thay vì chỉ làm mờ hay không.

---

### Checkpoint — 26/09/2026 (đồng bộ cột Mã nội bộ)
Vừa hoàn thành: cột “Mã nội bộ” ở bảng phiếu xử lý trình bày bằng bảng phiếu đề xuất — class `.col-code` (`nowrap` + `width:1%`) ở `GoodsTable.vue` và `HandlingGoodsTable.vue`. 8/8 file parse/compile sạch.
Đang làm dở: không có.
Bước tiếp theo: user tắt `npm run dev` → `npm run build` (Task 2.7), xem giao diện thật rồi chạy 9 kịch bản Phase 3.
Blocked: vẫn chưa chốt cách nhập SL khi dòng đã đổi (giữ 2 ô SL như hiện tại / SL B tự bám theo SL A).

---

### Checkpoint — 26/09/2026 (thiết kế lại khối Đổi)
Vừa hoàn thành: Task 2.10 — dựng demo 3 phương án (`demos/demo-doi-hang-cung-ung.html`), user chọn **PA A — khối cặp**, đã áp xong vào 2 bảng hàng + báo cáo Nhu cầu mua + Excel.
Đang làm dở: không có.
Bước tiếp theo: user tắt `npm run dev` → `npm run build` (Task 2.7), xem lại giao diện thật rồi chạy 9 kịch bản Phase 3.
Blocked: vẫn chưa chốt cách nhập SL khi dòng đã đổi (giữ 2 ô SL như hiện tại / SL B tự bám theo SL A).

---

### Checkpoint — 26/09/2026 (số liệu nguồn theo đúng từng hàng)
Vừa hoàn thành: Task 2.9 — đảo cách hiển thị “Số liệu nguồn” theo yêu cầu user: dòng chính giữ số của hàng gốc A (tồn kho, SL đang mua, SL còn lại HĐ), dòng phụ hiện số của hàng thay thế B. Sửa ở 2 bảng hàng, 2 màn add (cả export Excel), constants.js; spec + plan đã cập nhật.
Đang làm dở: không có — code Phase 2 đã đủ, 8/8 file parse/compile sạch.
Bước tiếp theo: user tắt `npm run dev` → `npm run build` (Task 2.7) rồi chạy 9 kịch bản Phase 3.
Blocked: còn **1 câu hỏi chưa chốt** — cách nhập SL khi dòng đã đổi hàng: giữ 2 ô SL (A để đối trừ HĐ, B để mua/giao) như hiện tại, hay để SL B tự bám theo SL A cho tới khi người lập sửa tay ô B.

---

### Checkpoint — 26/09/2026 (Phase 1)
Vừa hoàn thành: toàn bộ **Phase 1 — Backend** (Task 1.1 → 1.9). Verify bằng tinker (transaction + rollback) trên đề xuất DXCU-2026-0031: resource trả đủ `swap_*` (`swap_quantity` là float), `handledDetailByProduct` gom đúng `{"167_3349":10,"84_0":10}`, `swap_mismatch` bắt đúng trường hợp PXL không đổi trong khi đề xuất đã đổi, báo cáo Nhu cầu mua đứng tên hàng B (product_id=3349) kèm `swap_for_code`.
Đang làm dở: chưa bắt đầu Phase 2 — Frontend.
Bước tiếp theo: Task 2.1 — `GoodsPickerModal.vue` thêm `mode: 'swap'`.
Blocked:

---

### Checkpoint — 26/09/2026 (Phase 2 code)
Vừa hoàn thành: **Task 2.1 → 2.6** — 7 file FE đã sửa xong:
`supply_proposals/components/GoodsPickerModal.vue`, `supply_proposals/constants.js` (thêm `SWAP_SRC_KEYS`),
`supply_proposals/components/GoodsTable.vue`, `supply_proposals/add.vue`,
`supply_handlings/components/HandlingGoodsTable.vue`, `supply_handlings/add.vue`,
`utils/supply-excel-export.js`, `reports/purchase-demand/index.vue`.
Ghi chú: `inbox.vue` không có bảng hàng hóa nên bỏ mục đó khỏi Task 2.6.
Đang làm dở: không còn.
Bước tiếp theo: user tắt `npm run dev` → `npm run build` → test 8 kịch bản Phase 3.
Lưu ý: KHÔNG chạy `npm run build` khi dev server đang bật (hai tiến trình ghi đè `.nuxt` của nhau).
Blocked:

---

### Checkpoint — 26/09/2026 (chốt phạm vi đổi hàng)
Vừa hoàn thành: Task 2.8 — chỉ dòng `in_contract = true` mới đổi được hàng (ẩn nút ở 2 bảng, chặn trong `openSwapPicker` của 2 màn, thêm rule BE trong `ValidatesSwapProduct`, cập nhật spec). Parse/compile lại 8 file FE — sạch; `php -l` trait BE — sạch.
Đang làm dở: không còn.
Bước tiếp theo: user tắt `npm run dev` → `npm run build` → test 9 kịch bản Phase 3.
Blocked:

---

### Checkpoint — 26/09/2026 (bỏ trường Lý do đổi)
Vừa hoàn thành: bỏ hẳn `swap_reason` — FE (2 bảng hàng, 2 màn add, file Excel), BE (`ValidatesSwapProduct`, `NormalizesSwapProduct`, `ExposesSwapProduct`, 2 migration), spec. Đã `DROP COLUMN swap_reason` trên `thanhan_stag_07052026` (2 bảng, cột rỗng hoàn toàn trước khi xóa). Khối đổi hàng còn **7 cột** `swap_*`.
Đang làm dở: không còn.
Bước tiếp theo: chốt cách nhập SL hàng gốc A khi đã đổi (đang chờ user duyệt phương án "SL B tự bám theo SL A") → build → test Phase 3.
Blocked:
