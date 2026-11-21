# Plan — Báo cáo so sánh số liệu bán hàng theo thời gian chi tiết theo khu vực

## Phase 1 — BE (hrm-api, Modules/Sale)
- [x] Service `CompareContractByProvinceReportService` (tham số + 422, tập 1311, hợp đồng ứng viên, doanh thu hàng hóa / dịch vụ / phụ lục, gom tháng, filter-options)
- [x] Print service + blade in + Excel export + blade Excel (tiêu đề 2 tầng, chọn nhóm cột)
- [x] Controller + route `v1/sale/reports/compare-contract-by-province` + `checkPermission` mã mới
- [x] Catalog `sale.php`: mã mới (scopes 1-4, platforms hrm)
- [x] Đối chiếu ERP chạy thật trên DB local (3 chỉ tiêu) + SQL độc lập giải thích từng khoản lệch; phạm vi; 422; 403; tối ưu (~15,8s → ~2,6s)

## Phase 2 — FE (hrm-client)
- [x] `pages/sale/compare-contract-by-province-report/index.vue` + CcpSummary + CcpTable
- [x] Menu `sale-hub.js` → link + quyền
- [x] Verify trình duyệt 1366px: mở màn chưa chọn tỉnh, chọn 2 nhóm tỉnh, Đến tháng < Từ tháng (không gọi API), In bỏ 1 nhóm cột (3 chỉ tiêu kiểm qua API)

## Phase 3 — Bàn giao
- [x] Commit nhánh feat, cập nhật STATUS

### Checkpoint — 2026-11-18 (xong, chưa push)
Vừa hoàn thành: BE + FE + verify. ERP chạy thật trên DB local: SL khách / SL HĐ khớp từng tháng; giá trị lệch đúng bằng các lỗi đã
sửa (SQL độc lập HN 8/2025: hàng hóa 162,493,873,773.60 = HRM, × dòng quyết toán = ERP; dịch vụ UNION = ERP, UNION ALL + phụ lục = HRM).
403 với TK không quyền. Quyền local chỉ chèn tạm rồi đã gỡ — DB local CHƯA catalog-sync. Commit api `f83969b1d`, client `2965ae963`.
Bước tiếp theo: user check → push + merge `develop` (conflict 1 dòng `sale-hub.js`, giữ cả 2 link). Deploy `permission:catalog-sync` + cấp mã.
Blocked:

### Checkpoint — 2026-11-18 (đã lên develop)
Vừa hoàn thành: push nhánh feat + merge `develop` (api `370229d99`, client `56c226264`) — merge trong worktree tạm từ `origin/develop`
(worktree `develop` local có commit chưa push + file sửa dở của người khác, không đụng). Conflict `sale-hub.js` giữ cả 2 link.
Bước tiếp theo: user check trên dev; deploy `permission:catalog-sync` + cấp mã ở `/admin/roles`.
Blocked:

## Ngày 20/11/2026 (@junfoke)
- [ ] 20/11/2026 — Đang xử lý lỗi QA #12245 – #12249 (chung với plan `bc-so-sanh-bh-khu-vuc-theo-thoi-gian`). Riêng màn này: SL KH và SL HĐ đã khớp ERP, chỉ cột Giá trị lệch vì ERP join dòng quyết toán làm nhân doanh thu nhiều lần, UNION làm rơi dòng trùng và đảo biến phụ lục ⇒ user chốt giữ cách tính HRM, phản hồi QA kèm số đối chiếu. Phần giao diện / bộ lọc đang sửa, chưa commit.

## Ngày 21/11/2026 (@junfoke)
- [x] 21/11/2026 — Lỗi #12245 – #12249 xong, lên `develop` (client `3b79eb4f0`, api `375bc2142`) — phần chung 2 màn ghi ở plan `bc-so-sanh-bh-khu-vuc-theo-thoi-gian`. Riêng màn này (#12248, #12249): thêm phân trang; số 0 hiện "0", tỷ lệ hiện "0%" như ERP, đồng bộ cả bản in + Excel; popup bấm số ở khối tóm tắt chạy ~5s ở local (bằng thời gian chạy chính báo cáo).
