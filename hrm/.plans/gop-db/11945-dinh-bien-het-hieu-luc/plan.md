# QĐ ban hành/thay đổi định biên — trạng thái Hết hiệu lực 1 phần / Hết hiệu lực (#11945) — @cuong61n

Redmine: http://quanly.dnsmedia.vn/issues/11945 · Màn: Quyết định → Ban hành/thay đổi định biên (`/decision/manpower-planning`)
Yêu cầu: trong 1 QĐ, có ≥1 phòng ban đã bị QĐ "Thay đổi định biên" thay → "Hết hiệu lực 1 phần", tab phòng đó tên ĐỎ + tooltip "Đã thay đổi định biên"; mọi phòng đều bị thay → "Hết hiệu lực".
Nhánh: `gop_db` (worktree `worktrees/gop_db-api` + `gop_db-client`), chưa commit. Chung file với #11950 (`11950-loc-phong-ban-dinh-bien`).

## Quyết định đã chốt
- Trạng thái TÍNH ĐỘNG (không lưu DB), giống "Có hiệu lực" đang tính theo ngày hiệu lực. Mã: 9 = Hết hiệu lực 1 phần (`ManpowerPlanning::STATUS_PARTIALLY_EXPIRED`), 8 = Hết hiệu lực (`Decision::STATUS_EXPIRED`).
- Phòng D của QĐ X "đã bị thay đổi" khi có QĐ Y khác: loại Thay đổi định biên, đã duyệt, ngày hiệu lực ≤ hôm nay, chứa D, và hiệu lực SAU X (ngày lớn hơn; cùng ngày thì decision id lớn hơn). Chỉ áp khi X đang Có hiệu lực. (Tự suy từ spec — QĐ thay đổi chỉ áp vào định biên khi duyệt + tới ngày hiệu lực, xem `ManpowerPlanningController::toggleApprove`.)
- Tab phòng đã đổi tô ĐỎ theo spec (lệch CLAUDE.md "đỏ chỉ cho lỗi validate") — user chốt 30/10/2026 làm theo spec. Tooltip dùng `b-popover custom-class="info-popover"`.

## Phase 1
### BE (hrm-api)
- [x] 30/10/2026 `ManpowerPlanning`: hằng loại QĐ + trạng thái; `changedDepartmentCondition()` (điều kiện SQL EXISTS dùng chung), `changedDepartmentIds()`, `resolveExpireStatus()`.
- [x] 30/10/2026 `ManpowerPlanningService::index`: selectRaw `department_total` + `changed_department_total`; tự xử lý lọc trạng thái (`otherStatus`): 7 Có hiệu lực loại trừ QĐ đã hết hiệu lực (1 phần), thêm 9 và 8.
- [x] 30/10/2026 Resource danh sách trả `expire_status`; chi tiết trả `expire_status` + `is_manpower_changed` từng phòng; Excel export (`exports/manpower_planning.blade.php`) in 2 trạng thái mới.
- [x] 30/10/2026 Migration index (dùng chung file của #11950) thêm index `manpower_departments.department_id` — đã chạy lại local.
- [x] 30/10/2026 Test tinker (transaction + rollback): 1 phần (QĐ5: 2/3 phòng bị thay → 9, tab HN_KD2/HN_QTTT đổi, HN_KD1 không) · toàn bộ (QĐ4 2/2 → 8) · QĐ thay đổi hiệu lực tương lai → không tính · QĐ thay đổi bị từ chối → không tính · lọc 7/9/8/5 đúng. ĐẠT.
### FE (hrm-client)
- [x] 30/10/2026 `manpower-planning/index.vue`: `listStatus` thêm Hết hiệu lực 1 phần / Hết hiệu lực; ghi đè `getStatusText`/`getStatusClass` theo `expire_status` (1 phần badge-warning, hết badge-danger); bản in danh sách `utils/print/list-targets/decision.js` cũng in 2 trạng thái.
- [x] 30/10/2026 `components/FormComponent.vue`: tab phòng `is_manpower_changed` → tên đỏ + popover "Đã thay đổi định biên".
- [x] 30/10/2026 Test Playwright cổng 3002 (tạm duyệt QĐ 713/714 ở DB local rồi trả lại status=1, hiệu lực 2026-10-20): danh sách hiện "Hết hiệu lực 1 phần" / "Hết hiệu lực" · chi tiết QĐ có tab HN_KD2, HN_QTTT đỏ, HN_KD1 thường, rê chuột hiện "Đã thay đổi định biên" · lọc "Hết hiệu lực" ra đúng 1 QĐ, lọc "Có hiệu lực" loại QĐ đó. ĐẠT.
- [ ] Chưa test: file Excel xuất ra, bản In danh sách.
- [ ] Commit + push `gop_db`, deploy PROD (`php artisan migrate` + `route:cache`).
