# Plan — Redmine #11134 Báo cáo vòng đời dự án TKT

@khoipv — nhánh `fix-bug-11092026`

## Phase 1 — BE: cơ cấu giai đoạn dự án

- [x] T1. `ProspectiveProjectsReportService`: thêm `getProjectPhaseNameMap()` (bảng `project_phases`)
- [x] T2. `groupProjects()`: cộng dồn `project_phase_counts_raw` ở 3 cấp (công ty / phòng ban / NVKD)
- [x] T3. `normalizeGroupedData()`: chuẩn hoá `project_phase_counts` + `project_phase_count`
- [x] T4. `calculateSummary()`: cơ cấu giai đoạn cho dòng Tổng
- [x] T5. `ProspectiveProjectsReportResource`: trả `project_phase_count(s)` ở 3 cấp + summary

## Phase 2 — FE: cột mới + đổi nhãn

- [x] T6. `index.vue`: tiêu đề trang + tab → "Báo cáo vòng đời dự án TKT"
- [x] T7. `index.vue`: `openSummary()` thêm chiều `phase`, đổi nhãn status → "Tiến trình dự án"
- [x] T8. `index.vue`: `buildRowsFromApi()` dựng `dimensionSummaryByBucket[*].phase`
- [x] T9. `ProspectiveProjectsTable.vue`: nhóm `DỰ ÁN TKT` colspan 2→3, thêm cột "Cơ cấu giai đoạn dự án",
      đổi nhãn "Cơ cấu tiến trình nội bộ" → "Cơ cấu tiến trình dự án", sửa colspan dòng rỗng
- [x] T10. `ProspectiveProjectsFilter.vue`: "Giai đoạn dự án" → "Giai đoạn dự án khách hàng";
      "Tiến trình nội bộ" → "Tiến trình dự án"
- [x] T11. `ProspectiveListModal.vue`: đổi 2 nhãn tương ứng

## Phase 3 — Tên báo cáo ở các nơi còn lại

- [x] T12. `menu-sidebar.js`: "Dự án TKT theo PB - NV KD" → "Báo cáo vòng đời dự án TKT"
- [x] T13. `print.vue`: tiêu đề bản in
- [x] T14. `prospective_projects_report.blade.php`: tiêu đề file Excel
- [x] T15. `PermissionsTableSeeder.php`: đổi `display_name` 3 quyền 1054–1056 (giữ nguyên `name`)
      + gửi user câu UPDATE cho DB đã seed

## Kiểm chứng

- [x] T16. Kiểm tra cú pháp PHP (`php -l`) + build/parse FE

### Checkpoint — 2026-09-11
Vừa hoàn thành: T1–T16 (BE cơ cấu giai đoạn + FE cột mới + đổi tên báo cáo/nhãn ở mọi nơi).
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt kiểm thử màn `/assign/report/prospective-projects`
(cột "Cơ cấu giai đoạn dự án", popup, bộ lọc, bản in, Xuất Excel) + chạy câu UPDATE `display_name`
3 quyền 1054–1056 trên DB đã seed (seeder chỉ áp dụng cho DB seed mới).
Blocked:

## Phase 4 — Fix lệch số: bảng đếm cả dự án CHA còn popup thì không

User báo: dòng NVKD Nguyễn Thị Thu Huyền hiện 7 dự án TKT, bấm vào popup chỉ có 6.
Đã xác minh trên dev (tháng 9/2026, công ty 1 / phòng 44 / NVKD 1172): dự án dư là
`HN_KD3.2026.DAC007` "Dự án cha 1" (id 441, `is_parent_project = true`).
Gốc: commit `a310c5d7a` (du an cha con) chỉ thêm `is_parent_project = false` vào
`getProjectList()` (popup), bỏ sót `buildQuery()` (bảng tổng hợp + Xuất Excel).

- [x] T17. `ProspectiveProjectsReportService::buildQuery()`: thêm `where('pp.is_parent_project', false)`
      → bảng tổng hợp / dòng công ty / dòng Tổng / file Excel khớp với popup
- [x] T18. `ProspectiveProjectsReportService::getFilterOptions()`: loại dự án cha khỏi baseQuery
      để option bộ lọc không chứa giá trị chỉ có ở dự án cha (chọn vào sẽ ra 0 dòng)
- [x] T19. Kiểm chứng: `php -l` + gọi lại 2 API trên dev, số dòng Huyền phải bằng nhau

### Checkpoint — 2026-09-12
Vừa hoàn thành: T17-T19 — `buildQuery()` và `getFilterOptions()` đã loại dự án cha
(`pp.is_parent_project = false`), khớp với `getProjectList()`.
Kiểm chứng trên DB local trong transaction rollback (set tạm 1 dự án thành dự án cha):
code cũ ra bảng 9 / popup 8 (lệch), code mới ra bảng 8 / popup 8 (khớp); dữ liệu đã rollback.
Đang làm dở: không.
Bước tiếp theo: deploy lên dev rồi mở lại `/assign/report/prospective-projects` — dòng
Nguyễn Thị Thu Huyền (tháng 9/2026) phải về 6, dòng phòng 44 về 6, dòng công ty TPE về 7,
popup "Cơ cấu tiến trình dự án" hết đếm "Thu thập thông tin dự án: 5" (còn 4), file Xuất Excel khớp theo.
Blocked:
