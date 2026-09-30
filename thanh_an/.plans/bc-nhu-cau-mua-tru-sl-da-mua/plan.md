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
