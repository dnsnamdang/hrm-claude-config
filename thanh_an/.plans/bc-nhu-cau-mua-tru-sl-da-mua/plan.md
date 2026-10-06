# Plan — Báo cáo nhu cầu mua: trừ SL đã mua theo dòng

**Người phụ trách:** @khoipv
**Ngày bắt đầu:** 19/09/2026
**Spec chi tiết:** `docs/superpowers/specs/2026-09-19-bc-nhu-cau-mua-tru-sl-da-mua-design.md`
**Design tóm tắt:** `.plans/bc-nhu-cau-mua-tru-sl-da-mua/design.md`

## Chốt với user (19/09/2026)
- Phạm vi: **trừ theo dòng (đầy đủ)** — thêm liên kết cấp dòng nhu cầu ↔ dòng chứng từ mua
- Trạng thái trừ thật: **chỉ Đã duyệt (status 3)**
- Nháp (1) / Chờ duyệt (2): **không trừ** nhưng **phải hiển thị cho người dùng biết** (badge "đang chờ duyệt")
- Chứng từ tính: **cả HĐ mua và Đơn mua** ("là cả đi")

## Phase 1 — BE: hạ tầng cấp phát nhu cầu
- [x] 1.1 Migration tạo bảng `purchase_demand_allocations` (chỉ index, không khóa ngoại)
- [x] 1.2 Entity `PurchaseDemandAllocation` (+ hằng DOC_TYPE)
- [x] 1.3 Concern `AllocatesPurchaseDemand::syncDemandAllocations()` — đọc `purposes[]`, quy đổi ĐVT, ghi allocation
- [x] 1.4 Gọi trong `PurchaseContractService::syncProducts()`
- [x] 1.5 Gọi trong `PurchaseOrderService::syncProducts()`
- [x] 1.6 Migration backfill dữ liệu HĐ mua / đơn mua cũ từ JSON `purposes`

## Phase 2 — BE: báo cáo trừ số lượng
- [x] 2.1 `SupplyReportService::purchaseDemand()` select thêm `shp.id as handling_product_id`
- [x] 2.2 Hàm `allocationsByHandlingProduct()` — gom SL đã mua / chờ duyệt theo dòng nhu cầu
- [x] 2.3 Tính `bought_qty` / `pending_qty` / `remaining_qty` cho từng line (ĐVT gốc)
- [x] 2.4 Tổng cấp mã: `total_bought_qty` / `total_pending_qty` / `total_remaining_qty` (ĐVT quy đổi)
- [x] 2.5 Mặc định ẩn dòng đã mua đủ; filter `show_done=1` để hiện lại
- [x] 2.6 KPI: `so_ma_can_mua` đếm theo còn cần mua; thêm `tong_sl_con_can_mua`
- [x] 2.7 Controller nhận filter `show_done`

## Phase 3 — FE: màn báo cáo
- [x] 3.1 Cột mới: Nhu cầu / Đã mua / Còn cần mua + badge chờ duyệt
- [x] 3.2 Checkbox "Hiện cả dòng đã mua đủ"
- [x] 3.3 `buildContractLine` / `buildOrderLine` nạp **SL còn cần mua** + `handling_product_id`
- [x] 3.4 Bỏ filter "Chỉ mã chưa có HĐ mua" (BE đã lọc theo SL còn cần mua) → checkbox chuyển thành "Chọn mã để lập HĐ / đơn mua"
- [x] 3.5 Excel thêm 4 cột (Đã mua / Chờ duyệt / Còn cần mua / Chứng từ mua)

## Phase 4 — FE: popup chọn hàng
- [x] 4.1 `purchase_contracts/GoodsPickerModal` — `handling_product_id` + `handling_id` + SL còn cần mua
- [x] 4.2 `purchase_orders/GoodsPickerModal` — `handling_product_id` + SL còn cần mua

## Phase 5 — Kiểm thử
- [x] 5.1 `php -l` toàn bộ file BE sửa
- [x] 5.2 Test tinker trên staging: lập HĐ mua 1 phần → còn cần mua giảm đúng
- [x] 5.3 Test ĐVT lệch (đề xuất mL, mua Hộp)
- [x] 5.4 Test chứng từ nháp/chờ duyệt → không trừ, có badge

## Phát sinh trong lúc làm (ngoài plan gốc)
- [x] Line payload của báo cáo thiếu `handling_product_id` → đã bổ sung, nếu không FE không có khóa để gửi lại
- [x] Dữ liệu cũ: `purchase_*_products.unit_id` NULL → không quy đổi được. Đối chiếu dữ liệu thật thấy
      `purposes[].qty` của các phiếu này ghi theo ĐVT của chính dòng nhu cầu → nhận nguyên, không quy đổi
- [x] `purchaseDocMeta` đổi từ `number ?: code` sang `code ?: number` cho khớp cột "HĐ mua" sẵn có
- [x] Popup "Chứng từ mua gắn với dòng nhu cầu" (bấm số ở cột Đã mua / nhãn chờ duyệt)

## Checkpoint — 19/09/2026

### Checkpoint — 19/09/2026 14:00
Vừa hoàn thành: toàn bộ Phase 1 → 5. Migration đã chạy trên `thanhan_stag_07052026`
(backfill ghi 14 dòng, bỏ qua 0). Báo cáo đã trừ đúng: 24 dòng → còn 20 dòng cần mua.
3 file Vue compile sạch bằng `vue-template-compiler`, 8 file PHP `php -l` sạch.
Đang làm dở: không có.
Bước tiếp theo: user bấm thử trên UI (màn báo cáo + lập HĐ mua / đơn mua từ báo cáo),
sau đó chạy 2 migration trên môi trường thật.
Blocked: 

## Phase 6 — ROLLBACK theo yêu cầu user (19/09/2026)
User yêu cầu "back code phần này lại" sau khi đã code xong. **Toàn bộ code đã gỡ, DB đã trả về nguyên trạng.**
Các dấu `[x]` ở Phase 1-5 bên trên ghi lại việc ĐÃ TỪNG làm, hiện **không còn trong code**.

- [x] 6.1 `migrate:rollback` 2 bước: `2026_09_19_000004_backfill_...` rồi `2026_09_19_000003_create_purchase_demand_allocations_table` — đã verify `Schema::hasTable('purchase_demand_allocations') === false` và bảng `migrations` không còn bản ghi nào
- [x] 6.2 Xóa 4 file mới: 2 migration, `Entities/PurchaseDemandAllocation.php`, `Services/Concerns/AllocatesPurchaseDemand.php` (giữ lại thư mục `Services/Concerns/` vì còn `CalculatesPurchaseLineTotals` + `SyncsNoteToQuotation` của việc khác)
- [x] 6.3 Gỡ hook trong `PurchaseContractService` / `PurchaseOrderService` (import, `use` trait, 2 call site `syncDemandAllocations` mỗi file) — gỡ thủ công vì 2 file này còn nhiều thay đổi chưa commit KHÔNG thuộc tính năng này
- [x] 6.4 `git checkout` `SupplyReportService.php` (toàn bộ diff là của tính năng này)
- [x] 6.5 Gỡ filter `show_done` khỏi `SupplyReportController`
- [x] 6.6 `git checkout` `reports/purchase-demand/index.vue` + `purchase_orders/components/GoodsPickerModal.vue`
- [x] 6.7 Gỡ thủ công phần của tính năng trong `purchase_contracts/components/GoodsPickerModal.vue` (file này còn phần phân trang + đơn giá theo khách chưa commit)
- [x] 6.8 Quét lại: `php -l` sạch, không còn chuỗi `purchase_demand_allocations` / `PurchaseDemandAllocation` / `AllocatesPurchaseDemand` / `show_done` / `handling_product_id` / `remaining_qty` (của tính năng) trong 2 repo

### Checkpoint — 19/09/2026 (rollback)
Vừa hoàn thành: rollback toàn bộ tính năng "trừ SL đã mua theo dòng" (code + DB).
Đang làm dở: không.
Bước tiếp theo: nếu làm lại → đọc `docs/superpowers/specs/2026-09-19-bc-nhu-cau-mua-tru-sl-da-mua-design.md` (spec vẫn giữ nguyên, đủ để dựng lại từ đầu).
Blocked:

## Phase 7 — LÀM LẠI theo spec cũ (01/10/2026, user chọn phương án 1)
Code đã đổi nhiều từ 19/09 (đổi hàng A→B `swap_*`, sắp xếp `pushed_at`, cột Thay thế cho, chỉ nội bộ cần duyệt...)
→ dựng lại theo spec, đối chiếu code hiện tại, KHÔNG chép mù bản cũ.
- [x] 7.1 Khảo sát code hiện tại: query báo cáo (swap), `syncProducts()` 2 service, payload `purposes[]` 2 GoodsPickerModal, status HĐ mua/đơn mua
- [x] 7.2 BE: migration `2026_10_01_000001_create_purchase_demand_allocations_table` + entity `PurchaseDemandAllocation` + **service** `PurchaseDemandAllocationService` (thay trait — dùng chung cho 2 service + backfill). Dòng chứng từ đổi hàng (`swap_from_*`) → cấp phát theo hàng gốc + `swapOrigQty` (2 tầng quy ngược qua `swap_for_qty`)
- [x] 7.3 BE: hook vào `PurchaseContractService::syncProducts()` + `PurchaseOrderService::syncProducts()` (cả nhánh return sớm)
- [x] 7.4 BE: migration backfill `2026_10_01_000002_...` — staging: 5 chứng từ, ghi 17, bỏ qua 0
- [x] 7.5 BE: `SupplyReportService::purchaseDemand()` — bought/pending/remaining theo dòng + tổng mã + KPI + ẩn dòng đủ; controller nhận `show_done`
- [x] 7.6 FE báo cáo: cột Nhu cầu/Đã mua/Còn cần mua, badge chờ duyệt, popup chứng từ, checkbox, buildLine nạp SL còn cần mua, Excel
- [x] 7.7 FE 2 GoodsPickerModal: gửi `handling_product_id`, nạp SL còn cần mua
- [x] 7.8 Kiểm thử: php -l, migrate staging, tinker đối chiếu, compile Vue

### Checkpoint — 01/10/2026
Vừa hoàn thành: Phase 7 (làm lại) — BE bảng + service + hook 2 service + backfill (staging: 17 cấp phát, bỏ qua 0) + báo cáo bought/pending/remaining + show_done; FE báo cáo (3 cột Nhu cầu/Đã mua/Còn cần mua, nhãn chờ duyệt + lệch ĐVT, popup pdr-line-docs-modal, KPI Tổng SL còn cần mua, checkbox Hiện cả dòng đã mua đủ + Chọn mã để lập HĐ/đơn mua, Excel 4 cột, nạp SL còn cần mua) + 2 GoodsPickerModal (handling_product_id, remaining_qty, swap_for_qty co theo phần còn lại). Kiểm thử: php -l, tinker đối chiếu (round-trip trong transaction rollback), compile 3 file Vue.
Đang làm dở: —
Bước tiếp theo: build lại client, hard refresh, test UI: lập đơn mua/HĐ mua từ báo cáo → duyệt → dòng nhu cầu giảm/ẩn; chứng từ nháp → nhãn cam; tick Hiện cả dòng đã mua đủ.
Blocked:

## Phase 8 — Cột HĐ mua hiện cả Đơn mua (01/10/2026, user yêu cầu)
- [x] 8.1 BE: `SupplyReportService` thêm `purchaseOrdersByProduct()` — đơn mua ĐÃ DUYỆT chứa mã (theo product_id), trả `purchase_orders` mỗi dòng
- [x] 8.2 FE báo cáo: cột "HĐ / Đơn mua" hiện thêm chip đơn mua (link chi tiết + NCC), tooltip, Excel
- [x] 8.3 Kiểm thử: php -l, tinker, compile Vue

## Phase 9 — Đã mua tính cả chứng từ Nháp / Chờ duyệt (01/10/2026, user quyết)
Đổi quyết định #2: Nháp (1) / Chờ duyệt (2) / Đã duyệt (3) đều TRỪ nhu cầu; chỉ Từ chối (4) / Hủy (5) / đã xóa mới nhả ra.
- [x] 9.1 BE: `allocationsByHandlingProduct()` — bought = mọi chứng từ còn hiệu lực; pending = phần chưa duyệt (tập con, chỉ để hiển thị)
- [x] 9.2 FE báo cáo: nhãn cam "gồm N chưa duyệt", tooltip cột Đã mua, popup cột Trừ nhu cầu, ghi chú, Excel "Trong đó chưa duyệt"
- [x] 9.3 Kiểm thử + cập nhật spec/design
- [x] 9.4 FE: bỏ `cursor: help` (con trỏ dấu ?) trên nhãn cam / nhãn lệch ĐVT — user thấy khó chịu
- [x] 9.5 FE: bỏ tooltip "Đã trừ nhưng chứng từ chưa duyệt…" trên nhãn cam (xóa method `pendingTip`) — xem chứng từ qua popup bấm số Đã mua
- [x] 9.6 FE: trả lại bộ lọc "Chỉ mã chưa có HĐ / đơn mua" (bị mất khi đổi onlyNoHdMua → pickMode) — checkbox riêng `onlyNoDoc`, lọc FE theo purchase_contracts + purchase_orders rỗng, độc lập với pickMode
- [x] 9.7 FE: bỏ checkbox "Chọn mã để lập HĐ / đơn mua" (pickMode) — cột tick + nút Lập HĐ mua / Lập đơn mua luôn hiện
- [x] 9.8 Cột "HĐ / Đơn mua" hiện cả chứng từ Nháp / Chờ duyệt (khớp cột Đã mua — VD HC-SH-027 mua đủ bằng DMH-0004 nháp mà cột trống)
  - BE: `purchaseContractsByProduct` / `purchaseOrdersByProduct` lấy status 1/2/3 (+ status, status_name, approved; đã duyệt lên trước); `signed/remaining` + `remaining_on_po` chỉ tính HĐ đã duyệt; lọc NCC / HĐ mua chỉ khớp HĐ đã duyệt; hằng `LIVE_DOC_STATUSES` + `docStatusName()`
  - FE: nhãn trạng thái `.doc-st` cạnh mã; ô SL còn lại + popup chỉ HĐ đã duyệt (`approvedContracts`); Excel ghi `[Nháp]` / `[Chờ duyệt]`; lọc "Chỉ mã chưa có HĐ / đơn mua" giờ tính cả nháp
- [x] 9.9 FE: bộ lọc tự chạy khi thao tác (bỏ nút Áp dụng) — watcher `autoFilterKey` (mọi select + "Hiện cả dòng đã mua đủ"); ô từ khóa vẫn Enter; `reportSeq` chống response cũ đè; Đặt lại không tải 2 lần
- [x] 9.10 FE: header bảng 1 màu nền — bỏ `background: $nt-50` của hàng tiêu đề nhóm, dùng chung #f5f8f7 với hàng cột
- [x] 9.11 FE: bảng hàng hóa cuộn dọc trong khung (`max-height: calc(100vh - 180px)`), 2 hàng header sticky top (hàng 2 dùng `--gr-h` đo bằng `syncHeaderOffset`), viền header vẽ lại bằng inset
- [x] 9.12 FE: tăng chiều cao khung cuộn bảng hàng hóa `max-height: calc(100vh - 60px)` (cuộn trang tới bảng là bảng gần full màn)
- [x] 9.13 FE: bỏ đoạn ghi chú `.pdr-note` dưới bảng (template + CSS)
- [x] 9.14 FE: thêm khoảng trống dưới bảng hàng hóa (`.pdr-scroll` margin-bottom 24px)

### Checkpoint — 01/10/2026 (Phase 9)
Vừa hoàn thành: Đã mua tính cả chứng từ Nháp / Chờ duyệt (SupplyReportService::allocationsByHandlingProduct + text FE + Excel). Staging: KPI so_ma_can_mua 30 → 26, tong_sl_con_can_mua 1929 → 1198; VT-XN-001 shp11/36/37, HC-SH-3307, HC-SH-027, HC-SH-059 bị DMH-0003 (chờ duyệt) / DMH-0004 (nháp) trừ hết → ẩn khỏi danh sách
Đang làm dở: —
Bước tiếp theo: user build lại client + test UI màn báo cáo (nhãn cam "gồm N chưa duyệt", popup chứng từ, Excel)
Blocked:
