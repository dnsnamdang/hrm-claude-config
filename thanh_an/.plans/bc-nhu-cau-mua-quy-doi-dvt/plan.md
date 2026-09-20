# Fix: Báo cáo tổng hợp nhu cầu mua cộng SL không quy đổi ĐVT

**Người phụ trách:** @khoipv
**Màn:** `supply/reports/purchase-demand` — Báo cáo tổng hợp nhu cầu mua
**Design (tóm tắt):** [design.md](design.md) · **Spec chi tiết:** [docs/superpowers/specs/2026-09-10-bc-nhu-cau-mua-quy-doi-dvt-design.md](../../docs/superpowers/specs/2026-09-10-bc-nhu-cau-mua-quy-doi-dvt-design.md)
**Phạm vi:** chủ yếu BE (`SupplyReportService::purchaseDemand`), FE chỉ thêm ghi chú + cờ cảnh báo. Không migration, không đụng quyền.

## Bug

HC-SH-3307 (product_id 3322, ĐVT chính = Hộp):
- PXL-2026-0010: 150 **Hộp**
- PXL-2026-0011: 600 **mL**
- Báo cáo hiện ra **750 Hộp** ❌ → đúng phải là **450 Hộp** (150 + 600 × 1/2)

**Root cause:** `SupplyReportService::purchaseDemand()` (dòng ~173) cộng thẳng `shp.alloc_mua`
của mọi dòng PXL bất kể `shp.unit_id`, còn `unit_name` lấy của **dòng đầu tiên** gặp được.
Không có bước quy đổi ĐVT nào.

Hệ số quy đổi nằm ở `product_package_informations.conversion_factor` (tính TỪ đơn vị cơ bản).
Công thức: `qty_M = qty_A × f(A) / f(M)`. Đã có sẵn helper
`SupplyProposalService::unitConversionMap()` + `groupUnitTarget()` — tái sử dụng, KHÔNG viết mới.

## Quy tắc nghiệp vụ (đã chốt với @khoipv)

1. **Chỉ quy đổi khi lệch ĐVT** — các dòng cùng 1 ĐVT thì giữ nguyên ĐVT gốc, cộng thẳng
   (kể cả khi đó không phải ĐVT chính). Từ 2 ĐVT trở lên mới quy về ĐVT chính (`products.unit_id`).
   → Đồng nhất với `groupUnitTarget()` đang dùng ở phiếu đề xuất.
2. **Cột SL từng dòng đề xuất hiển thị SL đã quy đổi** (600 mL → hiện 300 Hộp), để cộng dồn khớp tổng.
3. **Thiếu hệ số quy đổi:** user xác nhận dữ liệu đã đủ hệ số. Vẫn để nhánh phòng vệ:
   không quy đổi được → giữ số gốc + gắn cờ `unit_convert_failed` để FE cảnh báo, KHÔNG cộng bừa.

## Hiện trạng dữ liệu (stag_07052026)

- 8 dòng PXL có ĐVT khác ĐVT chính (5 mã hàng)
- **1 mã hàng** có >1 ĐVT trong PXL → chỉ HC-SH-3307 đang thực sự sai
- HC-SH-003 (pid 5): PXL giữ snapshot ĐVT "Hộp" nhưng dòng hệ số Hộp đã bị xóa mềm 2025-12-16
  → thiếu hệ số. Chỉ có 1 ĐVT trong PXL nên theo quy tắc 1 không cần quy đổi ⇒ không ảnh hưởng.

## Task

### Phase 1 — BE
- [x] 1. Inject `SupplyProposalService` vào `SupplyReportService` (constructor) để dùng `unitConversionMap()`
- [x] 2. Gom `unit_id` theo product_id từ `$records`, dựng `$unitPlanByProduct`
      (`unit_id`, `unit_name`, `rates[unit_id => hệ số]`, `converted`, `failed`)
- [x] 3. Áp `rate` vào `total_buy_qty` và `lines[].quantity`
- [x] 4. Bổ sung `unit_id` vào row (FE `buildContractLine`/`buildOrderLine` đang đọc `row.unit_id` — hiện luôn undefined)
- [x] 5. Thêm `unit_converted` / `unit_convert_failed` vào row cho FE

### Phase 2 — FE
- [x] 6. Hiện cờ cảnh báo cạnh ĐVT khi `unit_convert_failed`
- [x] 7. Cập nhật ghi chú cuối bảng: nêu rõ quy tắc quy đổi ĐVT

### Phase 3 — Verify
- [x] 8. Test script tái hiện: HC-SH-3307 ra 450 Hộp; các mã 1 ĐVT giữ nguyên số cũ
- [x] 9. Đối chiếu KPI `tong_sl_de_xuat_mua` trước/sau

### Checkpoint — 2026-09-10
Vừa hoàn thành: fix quy đổi ĐVT ở `SupplyReportService::purchaseDemand()` + hàm mới `buildUnitPlans()`; FE thêm cờ cảnh báo thiếu hệ số, tooltip số gốc, cập nhật ghi chú.
Kết quả verify (DB thanhan_stag_07052026, chạy qua tinker):
- HC-SH-3307: 750 Hộp ❌ → **450 Hộp** ✅ (150 Hộp + 600 mL × 1/2 = 300 Hộp)
- 17 mã còn lại giữ nguyên số cũ (chỉ 1 mã có >1 ĐVT trong PXL)
- KPI tổng SL đề xuất mua: 4205 → 3905 (giảm đúng 300)
- Nhánh phòng vệ thiếu hệ số: test bằng Reflection với product_id 5 (2 ĐVT, ĐVT Hộp đã bị xóa mềm khỏi hệ số) → `failed=1`, rates=1, KHÔNG cộng bừa ✅
- `php -l` sạch; `vue-template-compiler` compile sạch, 0 error/tip; cả 2 file giữ nguyên CRLF
Đang làm dở: (không)
Bước tiếp theo: @khoipv build lại client + hard refresh, xem mắt trên trình duyệt màn Báo cáo tổng hợp nhu cầu mua
Blocked:
