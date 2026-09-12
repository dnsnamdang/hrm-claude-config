# Design (tóm tắt) — Fix quy đổi ĐVT ở Báo cáo tổng hợp nhu cầu mua

**Người phụ trách:** @khoipv · **Ngày:** 2026-09-10 · **Loại:** Bug fix
**Spec chi tiết:** [docs/superpowers/specs/2026-09-10-bc-nhu-cau-mua-quy-doi-dvt-design.md](../../docs/superpowers/specs/2026-09-10-bc-nhu-cau-mua-quy-doi-dvt-design.md)

## Mục tiêu

Báo cáo tổng hợp nhu cầu mua (`supply/reports/purchase-demand`) đang cộng số lượng đề xuất mua
của cùng 1 mã hàng **bất kể đơn vị tính**, cho ra số sai. Fix: quy đổi ĐVT trước khi cộng.

Ca lỗi gốc — HC-SH-3307 (product_id 3322, ĐVT chính = Hộp, 1 Hộp = 2 mL):

| PXL | ĐVT | SL | Trước | Sau |
|---|---|---|---|---|
| PXL-2026-0010 | Hộp | 150 | | 150 |
| PXL-2026-0011 | mL | 600 | | 300 |
| **Tổng** | | | **750 Hộp** ❌ | **450 Hộp** ✅ |

## Scope

- **BE:** `Modules/Supply/Services/SupplyReportService.php` (1 file)
- **FE:** `pages/supply/reports/purchase-demand/index.vue` (1 file, chỉ hiển thị/cảnh báo)
- **Không** migration, **không** đụng API contract cũ (chỉ thêm field), **không** đụng phân quyền

## Các quyết định lớn

1. **Chỉ quy đổi khi lệch ĐVT.** Cả khối cùng 1 ĐVT → giữ nguyên ĐVT gốc và cộng thẳng, kể cả
   khi đó không phải ĐVT chính. Từ 2 ĐVT trở lên mới quy về ĐVT chính (`products.unit_id`).
   → Giữ nguyên hiển thị quen thuộc cho 17/18 mã hàng, đồng nhất với `groupUnitTarget()` ở phiếu đề xuất.
2. **Cột SL từng dòng hiển thị số ĐÃ quy đổi**, số gốc trên phiếu đưa vào tooltip.
   → Cộng dồn bằng mắt luôn khớp tổng.
3. **Thiếu hệ số quy đổi → không cộng bừa.** Giữ số gốc + cờ `unit_convert_failed` để FE cảnh báo (⚠).
4. **Tái sử dụng `SupplyProposalService::unitConversionMap()`**, không viết helper quy đổi mới.
5. **Bổ sung `unit_id` vào row** — bug ngầm phát hiện kèm: FE `buildContractLine`/`buildOrderLine`
   đọc `row.unit_id` nhưng BE chưa bao giờ trả → tạo Đơn mua / HĐ mua từ báo cáo bị mất ĐVT.

## Kết quả

HC-SH-3307: 750 → 450 Hộp · 17 mã còn lại không đổi · KPI tổng SL đề xuất mua 4205 → 3905.
