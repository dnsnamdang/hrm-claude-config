# Plan — Báo cáo so sánh số liệu bán hàng theo khu vực chi tiết theo thời gian

## Phase 1 — BE (hrm-api, Modules/Sale)
- [x] Service `CompareContractByTimeReportService` (tham số + 422, kỳ, phạm vi 4 mức, gom theo khách → tỉnh, so 2 kỳ, filter-options)
- [x] Print service + blade in + Excel export + blade Excel (tiêu đề 2 tầng, chọn nhóm cột)
- [x] Controller + route `v1/sale/reports/compare-contract-by-time` + `checkPermission` mã mới
- [x] Catalog `sale.php`: mã mới (scopes 1-4, platforms hrm)
- [x] Kiểm số liệu bằng SQL độc lập (năm / quý / tháng, lọc tỉnh), phạm vi 4 mức, 422, 403 khi không quyền, tối ưu truy vấn

## Phase 2 — FE (hrm-client)
- [x] `pages/sale/compare-contract-by-time-report/index.vue` + CctSummary + CctTable
- [x] Menu `sale-hub.js` → link + quyền
- [x] Verify trình duyệt 1366px: mặc định năm, đổi quý, cuộn ngang / tiêu đề dính, In bỏ 1 nhóm cột, Excel

## Phase 3 — Bàn giao
- [x] Commit nhánh feat, cập nhật STATUS

### Checkpoint — 2026-11-17 (xong, chưa push)
Vừa hoàn thành: BE + FE + verify (đối chiếu SQL Hà Nội 2025: 755 KH / 3.530 HĐ / 514,955,580,285.75; 403 với TK không quyền).
Quyền local chỉ chèn tạm 1 mã để test rồi đã gỡ — DB local CHƯA catalog-sync.
Bước tiếp theo: user check → push + merge `develop`. Deploy `permission:catalog-sync` + cấp mã ở `/admin/roles`.
Blocked:

### Checkpoint — 2026-11-17 (đã lên develop)
Vừa hoàn thành: push nhánh feat + merge `develop` (api `44d2720bc`, client `5ee6aa610`; merge kéo theo các commit gop_db chưa có ở develop — user đồng ý).
Bước tiếp theo: QA test trên dev; deploy cần `permission:catalog-sync` + migration `notification_mutes` (từ gop_db) + cấp mã ở `/admin/roles`.
Blocked:

## Ngày 17/11/2026 — sau khi lên develop (@junfoke)
- [x] 17/11/2026 — Xử lý build dev lỗi sau merge: `CctTable.vue` import `SaleByProductPagination.vue` theo đường dẫn cũ `pages/sale/sale-by-product-report/components/` trong khi commit `03852b483` (16/11, người khác) đã chuyển bộ component sang `components/sale-by-product-report/` — merge không xung đột nên git không báo, webpack hỏng cả bản build. Sửa đường dẫn, quét toàn bộ import `@/...` không còn file mất. Client `aedd37637` (develop, đã push).
- [ ] Nhánh `feat/bc-so-sanh-bh-khu-vuc-theo-thoi-gian` (worktree `bc-so-sanh-khu-vuc`) vẫn còn đường dẫn cũ ở `CctTable.vue` dòng 95 — kéo develop về hoặc sửa trước khi merge tiếp / lên gop_db.
