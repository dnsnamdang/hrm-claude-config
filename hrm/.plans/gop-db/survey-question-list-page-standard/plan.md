# Plan — Chuẩn hoá màn Ngân hàng câu hỏi khảo sát theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `SurveyQuestionService::SORTABLE_COLUMNS` — trước đây KHÔNG sort được cột nào (`orderByDesc('id')` cứng); nay Tiêu đề / Ngày tạo / Ngày cập nhật, chốt `id desc` cuối
- [x] 1.2 Subquery `creator_name` / `updater_name` (chỉ TÊN, không leftJoin)
- [x] 1.3 Ô tìm nhanh tìm thêm theo **người tạo** bằng `EXISTS` (trước chỉ tìm tiêu đề)
- [x] 1.4 `SurveyQuestion::DATA_TYPE_NAMES` + `dataTypeName()` — nguồn DUY NHẤT tên loại dữ liệu
- [x] 1.5 `SurveyQuestionsResource` — thêm `status_text`, `data_type_text`, `application_scope_text`, `creator_name`, `updater_name`; ngày đổi `formatDate` → `d/m/Y H:i`
- [x] 1.6 `ExportColumnRegistry::COLUMNS['survey_questions']` (10 cột) + `export()` dùng `DynamicExport`, đuôi `.xlsx`

## Phase 2 — Frontend (viết lại toàn bộ)

- [x] 2.1 Bỏ `b-table` / `b-dropdown` / `b-collapse` / `Select2` / `b-pagination` → `V2BaseSmartFilterPanel` + `V2BaseDataTable`
- [x] 2.2 Schema `filterFields` 3 ô (Ứng dụng / Loại dữ liệu / Trạng thái) + ô tìm nhanh, placeholder chuẩn
- [x] 2.3 `ignoredFields` computed dùng `textFilterKeys()`
- [x] 2.4 Cột định danh = **Tiêu đề câu hỏi**, `nuxt-link` vào chi tiết, sticky+locked
- [x] 2.5 Cột `actions` cuối bảng + `V2BaseRowActions` (thay `b-dropdown` 5 mục); bỏ "Xem"; ẩn nút thay vì disable
- [x] 2.6 Trạng thái dùng `V2BaseBadge` (bỏ `badge-success` / `badge-danger` tự gắn class)
- [x] 2.7 Thêm cột Người tạo / Ngày tạo / Mô tả — hiện hết cột mặc định
- [x] 2.8 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal` + `$safeLoading`
- [x] 2.10 `filterStateMixin` + `mergeKnownFilters`; `loadData()` chạy đầu tiên, danh mục Ứng dụng hoãn tới khi mở panel
- [x] 2.11 Mục 15b: `fixed-layout` + `width`/`minWidth` đủ 12 cột (tổng 2058px) + `clamp-2` + `:title`
- [x] 2.12 Button-convention: Tạo mới `primary` + `ri-add-line` (thay `b-button variant="success"`), Xuất xanh lá, `:interactable`
- [x] 2.13 Lệnh GHI (Xóa, Khóa, Mở khóa) bọc `$safeLoading` trong `finally`
- [x] 2.14 Giữ 3 popup xác nhận riêng của màn (có cảnh báo bản ghi đang được dùng)

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE + dò identifier template bằng AST
- [x] 3.2 Smoke test API: index / sort `questionTitle` / keyword / export 200; kiểm payload Resource bằng 1 bản ghi thử trong transaction rollback (`data_type_text` = "Radio 1 lựa chọn", `application_scope_text` = "Tất cả")
- [x] 3.3 Đối chiếu cột bảng ↔ cột file ↔ registry BE (10 = 10, 12 cột đủ width+minWidth)
- [ ] 3.4 User mở trình duyệt kiểm tra

⚠️ Bảng `survey_questions` **rỗng trên DB local** (0 dòng) nên chỉ kiểm chứng được bằng bản ghi thử
trong transaction; phần hiển thị thật cần user xem trên môi trường có dữ liệu.

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ Phase 1-2, kiểm chứng 3.1-3.3.
Bước tiếp theo: user kiểm tra trên trình duyệt.
Blocked: không có.
