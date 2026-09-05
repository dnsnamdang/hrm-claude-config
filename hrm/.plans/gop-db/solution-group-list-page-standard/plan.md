# Plan — Chuẩn hoá màn Nhóm giải pháp theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `IndustriesService::SORTABLE_COLUMNS` — mở whitelist cho Mã / Tên / Ngày tạo / Ngày cập nhật, chốt `id desc` cuối
- [x] 1.2 Subquery `creator_name` / `updater_name` (chỉ TÊN, không leftJoin)
- [x] 1.3 Ô tìm nhanh tìm thêm theo **người tạo** bằng `EXISTS`
- [x] 1.4 `IndustriesResource` — thêm `status_text`, `creator_name`, `updater_name`, **`is_can_delete`** (entity đã có `isCanDelete()` nhưng Resource chưa trả); ngày `d/m/Y H:i`
- [x] 1.5 `ExportColumnRegistry::COLUMNS['industries']` (10 cột) + `export()` dùng `DynamicExport`, đuôi `.xlsx`

## Phase 2 — Frontend

- [x] 2.1 `V2BaseSmartFilterPanel` + schema `filterFields` 6 ô, placeholder chuẩn
- [x] 2.2 `ignoredFields` computed dùng `textFilterKeys()`
- [x] 2.3 Tách cột `industryCode` (button `.v2-cell-link` mở modal Xem, sticky+locked) / `industryName`
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions`; bỏ "Xem"; ẩn nút thay vì disable
- [x] 2.5 Nút Khóa/Mở khóa rời khỏi ô Trạng thái; lý do bị chặn đưa vào `title` badge
- [x] 2.6 Trạng thái dùng `V2BaseBadge` (bỏ `v-html` + `status-pill` + `renderStatus`)
- [x] 2.7 Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật riêng — hiện hết cột mặc định
- [x] 2.8 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal` + `$safeLoading` (cả trong luồng import)
- [x] 2.10 `filterStateMixin` + `mergeKnownFilters`; `loadData()` chạy đầu tiên, danh mục Nhóm ngành hoãn tới khi mở panel
- [x] 2.11 Mục 15b: `fixed-layout` + `width`/`minWidth` đủ 12 cột (2018px) + `clamp-2` + `:title`
- [x] 2.12 Button-convention: Import cam + `ri-upload-line`, Xuất xanh lá, `:interactable`, chữ `Khóa`/`Xóa`
- [x] 2.13 Lệnh GHI (Xóa, Khóa/Mở khóa, Import) bọc `$safeLoading` trong `finally`
- [x] 2.14 Bỏ hết `—`; link "Số ứng dụng" đổi `<a target="_blank">` → `nuxt-link` + `.v2-cell-link`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE + dò identifier template bằng AST
- [x] 3.2 Smoke test API: index (401 dòng) / sort `industryCode` / keyword "Ngô" ra 3 dòng nhờ tìm người tạo / export 200
- [x] 3.3 Đối chiếu cột bảng ↔ cột file ↔ registry BE (10 = 10, 12 cột đủ width+minWidth)
- [ ] 3.4 User mở trình duyệt kiểm tra

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ Phase 1-2, kiểm chứng 3.1-3.3.
Bước tiếp theo: user kiểm tra trên trình duyệt.
Blocked: không có.

## Lỗi tự phát hiện khi kiểm chứng

Bản viết lại gọi `this.$refs.industryModal?.loadData?.(id)` trong khi modal thực tế khai
**`loadIndustryData(id)`** → optional chaining nuốt lỗi im lặng, popup Xem/Sửa vẫn mở nhưng **rỗng**.
Compile và bộ dò identifier đều KHÔNG bắt được (gọi qua `$refs` là runtime).

Đã sửa, và rà lại toàn bộ 7 màn có popup của đợt này bằng cách đối chiếu tên hàm gọi qua `$refs`
với hàm thật khai trong component modal — 7/7 khớp.
