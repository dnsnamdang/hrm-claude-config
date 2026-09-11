# Plan — Chuẩn hoá màn Danh sách giai đoạn dự án theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `ProjectPhaseService::SORTABLE_COLUMNS` — mở whitelist cho Mã / Tên / Ngày tạo / Ngày cập nhật (trước chỉ có `updatedAt`), chốt `id desc` cuối
- [x] 1.2 Subquery `creator_name` / `updater_name` (chỉ TÊN, không kèm mã NV, không leftJoin)
- [x] 1.3 Ô tìm nhanh tìm thêm theo **người tạo** bằng `EXISTS`
- [x] 1.4 Thêm bộ lọc `code`, `name`, `priority_level_id`; đổi tham số sort sang `sort_by` + `sort_desc`
- [x] 1.5 `ProjectPhaseResource` — `status_text`, `creator_name`, `updater_name`, ngày `d/m/Y H:i`, `is_can_lock_update` / `is_can_unlock_update`; `is_can_delete` tính từ subquery đếm thay vì `isCanDelete()` (bỏ 1 query mỗi dòng)
- [x] 1.6 `DetailProjectPhaseResource` — ngày bỏ giây
- [x] 1.7 `ExportColumnRegistry::COLUMNS['project_phases']` (10 cột) + `ProjectPhaseController::export()` dùng `DynamicExport` (ra `.xlsx`)
- [x] 1.8 Nới middleware route `export`: `Quản lý…|Xem danh mục giai đoạn dự án` (skill mục 3b-5)

## Phase 2 — Frontend

- [x] 2.1 `V2BaseSmartFilterPanel` + schema `filterFields` 8 ô, bỏ `title`/`subtitle`, placeholder chuẩn
- [x] 2.2 `ignoredFields` computed dùng `textFilterKeys()`
- [x] 2.3 Tách cột `phaseCode` (button `.v2-cell-link` mở modal Xem, sticky + locked) / `phaseName`
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions`; bỏ "Xem"; ẩn nút thay vì disable
- [x] 2.5 Nút Khóa/Mở khóa rời khỏi ô Trạng thái vào menu `⋮`
- [x] 2.6 Trạng thái dùng `V2BaseBadge` (bỏ `v-html` + `status-pill` + `renderStatus` + `escapeHtml`)
- [x] 2.7 Tách 4 cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật; mặc định hiện HẾT cột
- [x] 2.8 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal`; `$safeLoading` thay `$nuxt.$loading` (cả luồng import)
- [x] 2.10 `filterStateMixin` + `mergeKnownFilters` (`assign_project_phases`)
- [x] 2.11 `loadData()` chạy đầu tiên trong `created()`; danh mục Mức độ ưu tiên hoãn tới khi mở panel lọc; chống response về trễ bằng `loadSeq`
- [x] 2.12 `fixed-layout` + `width`/`minWidth` đủ 12 cột, cột chữ dài `clamp-2` + `:title`
- [x] 2.13 Gỡ code chọn nhiều dòng / xoá hàng loạt (toolbar đã comment từ trước)
- [x] 2.14 Lệnh GHI (Xóa, Khóa/Mở khóa) bọc `$safeLoadingStart()` + `$safeLoadingFinish()` trong `finally`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE + dò identifier template bằng AST (chỉ còn biến slot-scope `item` / `index`)
- [x] 3.2 Smoke test API qua HTTP kernel: index / sort `phaseCode` / keyword / export (200 + xlsx)
- [x] 3.3 Đọc lại file xuất: đúng cột đã tick, đúng thứ tự, có dòng tiêu đề
- [x] 3.4 Đối chiếu khoá cột bảng ↔ `exportFields` ↔ registry BE (10 = 10)
- [ ] 3.5 User mở trình duyệt kiểm tra

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ Phase 1-2, kiểm chứng 3.1-3.4.
Đang làm dở: không có.
Bước tiếp theo: user kiểm tra trên trình duyệt (`/assign/project_phase`).
Blocked: không có.

## Việc CỐ Ý không làm

- **Hành động "Lịch sử"** (skill bắt buộc với mọi màn danh sách): bỏ, giống 2 màn mẫu nhóm ngành /
  ứng dụng — module `Assign` chưa có trait `LogsCatalogHistory` + bảng log. Muốn có thì mở việc riêng.
- **Cột "Số dự án đã gán" không làm link** sang danh sách dự án tiềm năng: màn đó không đọc query
  string để nạp bộ lọc → sẽ là link chết.
- 4 file mồ côi `project_phase/add.vue`, `_id/index.vue`, `_id/show.vue`,
  `components/ProjectPhaseForm.vue` (menu không trỏ tới, màn dùng modal) — để nguyên, không thuộc
  phạm vi lần sửa này.
