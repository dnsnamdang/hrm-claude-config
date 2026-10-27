# Plan — Báo cáo tổng hợp nhu cầu mua: sửa theo demo (bỏ tab Đã có HĐ mua)

**Người phụ trách:** @khoipv
**Ngày bắt đầu:** 21/10/2026
**Demo gốc:** `demos/demo-bc-tong-hop-nhu-cau-mua.html` (chỉ lấy tab **Cần đi mua**)
**Spec chi tiết:** `docs/superpowers/specs/2026-10-21-bc-nhu-cau-mua-theo-demo-design.md`
**Design tóm tắt:** `.plans/bc-nhu-cau-mua-theo-demo/design.md`

## Chốt với user (21/10/2026)
- **Bỏ tab "Đã có HĐ mua"** → bỏ hẳn thanh tab, chỉ còn nội dung "Cần đi mua" (dòng còn cần mua > 0) + dòng gợi ý trên bảng
- **Đã mua tính cả HĐ mua + đơn mua** (giữ như hiện tại, KHÁC demo) — tránh mua trùng khi Lập đơn mua từ báo cáo
- Bộ lọc / nút **theo demo**: Nhóm hàng · Loại đề xuất · Khách hàng · NCC · Hợp đồng mua (NCC / HĐ lọc theo đúng dòng đã gắn chứng từ đó); bỏ 2 ô tick "Hiện cả dòng đã mua đủ" / "Chỉ mã chưa có HĐ / đơn mua"; bỏ nút giả "Tạo yêu cầu giao hàng"

## Phase 1 — FE `pages/supply/reports/purchase-demand/index.vue`
- [x] 1.1 KPI theo demo: Mã hàng cần đi mua · Phiếu xử lý có Mua thêm · Dòng cần đi mua · Tổng SL còn cần mua (bỏ "Mã hàng theo dõi")
- [x] 1.2 Bộ lọc: bỏ 2 ô tick (field + slot + state `showDone` / `onlyNoDoc`); "Mục đích mua" → "Loại đề xuất"; NCC (HĐ mua) → NCC
- [x] 1.3 Thanh thao tác: bỏ nút + popup "Tạo yêu cầu giao hàng"; Lập HĐ mua / Lập đơn mua hiện số mã đã tick `(n)`
- [x] 1.4 Dòng gợi ý (hint) trên bảng như demo
- [x] 1.5 Bảng theo demo: bỏ cột Tồn kho · HĐ / Đơn mua · SL còn lại HĐ mua · Mục đích; nhóm cột "Nhu cầu mua thêm (từ phiếu xử lý cung ứng)" = Phiếu xử lý · Cần mua thêm · Đã mua · Còn cần mua; nhóm "Thông tin đề xuất" 6 cột; chip "Σ còn cần mua" dưới tên hàng khi mã có ≥ 2 dòng; tooltip cột theo demo
- [x] 1.6 Bỏ popup "HĐ mua với NCC còn hiệu lực" (cột SL còn lại HĐ mua đã bỏ); giữ popup chứng từ mua của dòng (bấm số Đã mua)
- [x] 1.7 Thông báo bảng rỗng theo demo ("Không còn hàng nào cần đi mua" / "Không có dòng nào khớp điều kiện lọc")
- [x] 1.8 Xuất Excel khớp cột mới (bỏ Tồn kho / HĐ-Đơn mua / SL còn lại HĐ mua / Mục đích; Nhu cầu → Cần mua thêm)

## Phase 2 — BE `SupplyReportService::purchaseDemand()` (hàm dùng chung với 2 popup chọn hàng HĐ mua / đơn mua — user đã đồng ý 21/10/2026)
- [x] 2.1 Bỏ tham số `show_done` (luôn ẩn dòng đã mua đủ) — controller bỏ nhận
- [x] 2.2 `purchaseDocMeta()` trả thêm `supplier_id` / `supplier_name` → `purchase_docs` của dòng có NCC
- [x] 2.3 Lọc `ncc` / `hd_mua` theo DÒNG (dòng có chứng từ của NCC / HĐ đó), thay vì theo mã + HĐ đã duyệt
- [x] 2.4 Options NCC / HĐ mua lấy từ chứng từ còn hiệu lực (Nháp / Chờ duyệt / Đã duyệt), NCC gồm cả đơn mua; HĐ chưa duyệt ghi kèm trạng thái
- [x] 2.5 Bỏ dữ liệu không còn dùng: `purchase_contracts` / `purchase_orders` / `remaining_on_po` của row + KPI `so_ma_theo_doi`
- [x] 2.6 Kiểm tra 2 popup chọn hàng (HĐ mua / đơn mua) không đọc các field đã bỏ

## Phase 3 — Kiểm tra
- [x] 3.1 `php -l` + gọi thử service qua tinker (lọc NCC / HĐ, KPI)
- [x] 3.2 Cập nhật `demos/README.md` (ghi chú màn thật đã làm theo demo, bỏ tab 2)

## Phase 4 — Chỉnh sau review (21/10/2026)
- [x] 4.1 Bỏ dòng gợi ý (hint) trên bảng theo yêu cầu user (task 1.4 bỏ)

## Phase 5 — Lọc "Đã mua đủ" (23/10/2026)
User yêu cầu: thêm lọc hàng đã mua đủ, khi lọc thì CHỈ hiện dòng đã mua đủ. Mặc định (không chọn) vẫn chỉ hiện dòng còn cần mua.
"Đã mua đủ" = dòng có Còn cần mua ≤ 0 — cách tính Đã mua giữ nguyên (gồm cả HĐ / đơn Nháp, Chờ duyệt).
- [x] 5.1 BE: `purchaseDemand()` nhận `buy_status` (`done` = chỉ dòng đã mua đủ; rỗng / `remaining` = như cũ) — 2 popup chọn hàng không truyền → không đổi; controller nhận `buy_status`
- [x] 5.2 BE: KPI thêm `so_ma` (số mã đang hiện) + `tong_sl_da_mua`
- [x] 5.3 FE: ô lọc "Tình trạng mua" (Còn cần mua / Đã mua đủ)
- [x] 5.4 FE: chế độ Đã mua đủ — KPI đổi nhãn (Mã hàng đã mua đủ · Phiếu xử lý · Dòng đã mua đủ · Tổng SL đã mua), ẩn nút Lập HĐ mua / Lập đơn mua + ô tick, ẩn chip "Σ còn cần mua", câu bảng rỗng riêng
- [x] 5.5 FE: Excel theo chế độ đang lọc (tên file / sheet có "đã mua đủ")
- [x] 5.6 `php -l` + chạy thử service qua tinker

Ghi chú Phase 5:
- Ô lọc key `buy_status`, đặt cuối danh sách; cấu hình bộ lọc đã lưu tự append ô mới (isVisible true)
- Chế độ Đã mua đủ: ô tick vẫn giữ cột (tránh lệch cột dính trái), chỉ ẩn checkbox
- Chạy thử DB dev: mặc định 27 mã / 38 dòng (không đổi); `done` → 6 mã / 12 dòng, mọi dòng còn cần mua = 0
- Dữ liệu dev có dòng mua dư (HC-SH-025 PXL-2026-0002 cần 2.000 mL, HĐ mua HDM-2026-0002 gắn 792.000 mL; VT-XN-001 PXL-2026-0001 cần 5, 3 đơn mua gắn 15) → KPI "Tổng SL đã mua" lớn hơn tổng cần mua

### Ghi chú khi làm
- Popup chứng từ của dòng (bấm số Đã mua) thêm cột **NCC**; Excel cột "Chứng từ mua" ghi HĐ/ĐM + NCC
- "Σ còn cần mua": các dòng cùng ĐVT → cộng số gốc; lệch ĐVT → dùng `total_remaining_qty` (ĐVT khối); không quy đổi được → ẩn
- Option "Hợp đồng mua" hiện `số HĐ - tên (trạng thái nếu chưa duyệt) · NCC`
- Đã chạy thử service (DB dev): 27 mã / 38 dòng; lọc NCC 2950 → 1 dòng; lọc HĐ 3 → 1 dòng; NCC không tồn tại → 0
- Cấu hình bộ lọc đã lưu có key cũ `show_done` / `only_no_doc` → panel tự bỏ key không còn trong schema

### Checkpoint — 21/10/2026
Vừa hoàn thành: Phase 1–3 (FE + BE + README demos)
Đang làm dở: —
Bước tiếp theo: user test trên trình duyệt màn /supply/reports/purchase-demand + 2 popup chọn hàng ở HĐ mua / đơn mua
Blocked:

## Phase 6 — Thêm lại cột "HĐ mua / Đơn mua" (24/10/2026)
User yêu cầu: bảng có thêm cột chứng từ mua của từng dòng. Chỉ FE (dữ liệu `line.purchase_docs` BE đã trả sẵn); Excel đã có cột "Chứng từ mua" → giữ nguyên.
- [x] 6.1 FE: cột "HĐ mua / Đơn mua" trong nhóm "Nhu cầu mua thêm" (sau Còn cần mua) — mỗi chứng từ 1 dòng: nhãn HĐ/ĐM + số chứng từ (link mở tab mới) + NCC; chứng từ chưa duyệt ghi kèm trạng thái
- [x] 6.2 FE: colspan nhóm 4 → 5, colspan bảng rỗng 15 → 16

## Phase 7 — "Đã mua" chỉ tính ĐƠN MUA (24/10/2026)
User chốt: Đã mua = đã có đơn mua hàng. Hàng mới lập HĐ mua, chưa lên đơn mua → CHƯA tính vào Đã mua (vẫn còn cần mua).
- Màn báo cáo: KHÔNG thêm cột "Đã lập HĐ"; HĐ mua chỉ hiện ở cột "HĐ mua / Đơn mua" để tham khảo
- 2 popup chọn hàng (HĐ mua / đơn mua): đổi theo logic mới (chỉ đơn mua trừ nhu cầu) + thêm cột "HĐ mua" để tham khảo
- Đơn Nháp / Chờ duyệt vẫn tính vào Đã mua, kèm nhãn cam (giữ như cũ)
- Bẫy: đơn lập từ HĐ mua THƯƠNG MẠI đang bị tước `purposes` trước khi ghi cấp phát (HĐ đã trừ) → nếu chỉ đếm đơn thì đơn này không bao giờ được tính. Đơn vẫn lưu purposes (buyQty theo SL đơn) → bỏ đoạn tước + backfill.

- [x] 7.1 BE `PurchaseOrderService::syncProducts()`: bỏ đoạn tước purposes dòng rút từ HĐ mua TM → đơn nào cũng ghi cấp phát
- [x] 7.2 BE migration backfill: ghi lại cấp phát cho đơn mua có dòng rút từ HĐ mua (từ JSON purposes đã lưu)
- [x] 7.3 BE `SupplyReportService::allocationsByHandlingProduct()`: cấp phát HĐ mua KHÔNG cộng vào bought / pending, vẫn đưa vào `purchase_docs` (cờ `counted = false`) để hiện tham khảo; cập nhật docblock
- [x] 7.4 FE báo cáo: tooltip cột Đã mua; popup chứng từ của dòng — cột "Trừ nhu cầu" với HĐ mua ghi "Không (chỉ tham khảo)", câu ghi chú cuối popup
- [x] 7.5 FE popup chọn hàng HĐ mua: thêm cột "HĐ mua" (HĐ mua đã gắn dòng nhu cầu)
- [x] 7.6 FE popup chọn hàng đơn mua (chế độ từ báo cáo nhu cầu): thêm cột "HĐ mua"; sửa colspan / tfoot
- [x] 7.7 `php -l` + chạy migration + tinker so số trước / sau

Ghi chú Phase 7:
- DB dev: mặc định vẫn 27 mã / 39 dòng; chế độ "Đã mua đủ" vẫn 6 mã / 12 dòng nhưng tổng SL đã mua 795.266 → 3.266 (HDM-2026-0002 792.000 không còn trừ, chỉ hiện tham khảo `counted=false`)
- Migration `2026_10_24_000001_resync_order_allocations_from_purchase_contracts` đã chạy ở dev (dev chưa có đơn rút từ HĐ mua → 0 đơn). Môi trường khác cần chạy `php artisan module:migrate Supply`
- Hệ quả đã chấp nhận: popup chọn hàng không còn trừ theo HĐ mua → dòng đã có HĐ mua vẫn chọn lại được (cột "HĐ mua" để người dùng biết)
- Đổi hàng: SL trừ nhu cầu lấy `swapOrigQty` trong purposes của đơn (đã sửa được ở tab hàng hóa đơn)
- Order popup: 2 ô chế độ isFree gộp vào `<template v-if="isFree">`; colspan 13 / 14, tfoot 9 + 1 + (3 | 4)

### Checkpoint — 24/10/2026
Vừa hoàn thành: Phase 7 ("Đã mua" chỉ tính đơn mua + cột HĐ mua tham khảo ở 2 popup)
Đang làm dở: —
Bước tiếp theo: build client, test UI màn báo cáo + 2 popup chọn hàng; chạy migration ở môi trường khác
Blocked:
