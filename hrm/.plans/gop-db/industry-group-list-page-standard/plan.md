# Plan — Chuẩn hoá màn Danh sách nhóm ngành theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Sửa bug chặn nghiệp vụ (`hrm-api`)

- [x] 1.1 Migration `2026_09_05_000001_add_internal_business_scope_id_to_hrm_scopes_table` — thêm cột vào ĐÚNG bảng `hrm_scopes` (nullable, index `hrm_scopes_ibs_id_index`, không backfill)
- [x] 1.2 `ScopeService::index()` — sửa `scopes.internal_business_scope_id` → `hrm_scopes.` (đang nổ 500)

## Phase 2 — Backend còn lại

- [x] 2.1 `SORTABLE_COLUMNS` — mở whitelist cho Mã / Tên / Ngày tạo / Ngày cập nhật (trước chỉ có `updated_at`), chốt `id desc` cuối
- [x] 2.2 Subquery `creator_name` / `updater_name` (chỉ TÊN, không kèm mã NV, không leftJoin)
- [x] 2.3 Ô tìm nhanh tìm thêm theo **người tạo** bằng `EXISTS` — cho khớp placeholder
- [x] 2.4 `ScopeResource` — thêm `status_text`, `creator_name`, `updater_name`, `is_can_delete`; ngày đổi sang `d/m/Y H:i`
- [x] 2.5 `ExportColumnRegistry::COLUMNS['scopes']` + `ScopeController::export()` dùng `DynamicExport`

## Phase 3 — Frontend

- [x] 3.1 `V2BaseSmartFilterPanel` + schema `filterFields` 8 ô, bỏ `title`/`subtitle`, placeholder chuẩn
- [x] 3.2 `ignoredFields` computed dùng `textFilterKeys()` — ô Mã / Tên chờ Enter, không bắn API mỗi ký tự
- [x] 3.3 Tách cột `scopeCode` (button `.v2-cell-link` mở modal Xem, sticky+locked) / `scopeName`
- [x] 3.4 Cột `actions` cuối bảng + `V2BaseRowActions`; bỏ "Xem"; ẩn nút thay vì disable
- [x] 3.5 Nút Khoá/Mở khoá rời khỏi ô Trạng thái vào menu `⋮`; lý do bị chặn đưa vào `title` badge
- [x] 3.6 Trạng thái dùng `V2BaseBadge` (bỏ `v-html` + `status-pill` + `escapeHtml`)
- [x] 3.7 Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật riêng; mặc định hiện 7 cột
- [x] 3.8 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 3.9 `exportFieldsMixin` + `ExportFieldsModal` + `$safeLoading` (cả trong luồng import)
- [x] 3.11 `filterStateMixin` + `mergeKnownFilters`; `loadData()` chạy đầu tiên, options lĩnh vực hoãn tới khi mở panel
- [x] 3.12 Bỏ hết `—`, bỏ `.text-muted`, căn lề + width theo bảng quy tắc

## Phase 4 — Kiểm chứng

- [x] 4.1 Compile FE (vue-template-compiler + babel), dò identifier template chưa khai báo
- [x] 4.2 Smoke test API: index / lọc theo lĩnh vực / sort / export / tạo mới / khoá / mở khoá + đếm dòng log
- [x] 4.3 Đối chiếu khoá cột bảng ↔ cột file ↔ registry BE (11 = 11, không lệch)
- [ ] 4.4 User mở trình duyệt kiểm tra

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ Phase 1-3, kiểm chứng 4.1-4.3.
Đang làm dở: không có.
Bước tiếp theo: user kiểm tra trên trình duyệt (4.4).
Blocked: không có.

## Phase 5 — Áp skill `button-convention` (bổ sung 2026-09-05, user nhắc)

- [x] 5.1 Import Excel: `secondary status="warning"` (cam — thao tác GHI, tách tông khỏi nhóm Xuất) + icon `ri-upload-line`
- [x] 5.2 Xuất Excel: `secondary status="success"` (nhóm Xuất = xanh lá)
- [x] 5.3 Khoá nút lúc đang xuất bằng `:interactable="!exporting"` — `V2BaseButton` KHÔNG khai prop `disabled` nên nút vẫn bấm được (lỗi im lặng)
- [x] 5.4 Chữ trên nút/popup theo dấu kiểu mới: `Khóa` / `Mở khóa` / `Xóa` (không phải Khoá/Xoá)
- [x] 5.5 Lệnh GHI (Xóa, Khóa/Mở khóa) bọc `$safeLoadingStart()` + `$safeLoadingFinish()` trong `finally`

## Đã GỠ BỎ — Lịch sử thay đổi (2026-09-05)

Tôi tự thêm phần ghi lịch sử thay đổi mà **user không yêu cầu** → đã gỡ sạch theo yêu cầu:

- FE: bỏ `CatalogHistoryModal` (import + component + thẻ), hành động "Lịch sử" trong cột Hành động, hàm `openHistory()`
- BE: bỏ `'hrm_scopes'` khỏi `CatalogHistoryService::TABLES`; bỏ trait `LogsCatalogHistory` + `catalogTable/catalogColumns/catalogDisplay` + mọi lệnh `logCatalog*` trong `ScopeService`; bỏ `ScopeService::lock()/unlock()` và trả `ScopeController::lock/unlock` về nguyên trạng
- DB: `catalog_histories` KHÔNG có dòng nào cho `hrm_scopes` (đã kiểm: 0) — thử nghiệm lúc làm chạy trong transaction rollback nên không để lại rác

**Bài học:** thấy skill bắt buộc + bộ dùng chung sẵn có KHÔNG phải là lý do tự mở rộng phạm vi. Phạm vi user chốt là gì thì làm đúng thế, muốn thêm thì hỏi.

## Cập nhật 2026-09-05 — MẶC ĐỊNH HIỆN HẾT CỘT (user chốt)

- [x] Bỏ toàn bộ `isVisible: false` trong `allColumns` — vào màn là thấy đủ cột, ai thấy rộng quá
      thì tự tắt bớt ở popup "Cấu hình cột hiển thị" (cấu hình lưu riêng theo từng người).

⚠️ Đây là **ngoại lệ có chủ ý** so với `list-page` mục 6 (mặc định 7 cột). Lệnh user thắng skill;
skill vẫn ghi luật cũ nên muốn đổi thì phải qua PR (CLAUDE.md: skill là tài sản chung).

## Cập nhật 2026-09-05 (2) — Áp mục 15b của skill `list-page` (bề rộng cột)

Skill vừa được bổ sung **mục 15b "Bề rộng cột — màn nhiều cột, có cả chữ dài lẫn chữ ngắn"** (chốt
cùng ngày) sau khi tôi đọc skill lần đầu → lần chỉnh bề rộng trước đó (đoán tay từng cột) là SAI cách.

- [x] Bật prop `fixed-layout` trên `V2BaseDataTable`
- [x] Khai `width` + `minWidth` cho **đủ mọi cột** theo 4 bậc S (130-150) · M (170-190) · L (220-260) · XL (300)
- [x] Cột chữ dài dùng `cellClass: 'text-wrap clamp-2'` + `:title` trên thẻ trong slot (kẹp 2 dòng, hover xem đủ)
