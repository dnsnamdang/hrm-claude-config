# Design — Danh mục Lĩnh vực kinh doanh nội bộ

> Tóm tắt. **Spec đầy đủ**: `docs/superpowers/specs/2026-08-22-linh-vuc-kinh-doanh-noi-bo-design.md`

## Mục tiêu

Thêm danh mục **Lĩnh vực kinh doanh nội bộ** cho phân hệ Dự án & Giao việc: màn danh sách dạng bảng +
modal Tạo / Sửa / Xem, mã theo định dạng cố định, tên không được trùng, metadata ghi tự động.

- Menu: Danh mục › **Lĩnh vực kinh doanh nội bộ** (ngay trước "Nhóm ngành")
- Route: `/assign/internal-business-scopes` · Bảng: `internal_business_scopes`
- Nhánh: **`linh-vuc-noi-bo`** (tách từ `tpe`, cả `hrm-api` + `hrm-client`) — không thuộc `gop_db`

## Quyết định lớn (chốt với user 2026-08-22)

| # | Quyết định |
| --- | --- |
| 1 | Phạm vi **đầy đủ như `customer_scopes`**: lọc nâng cao, Trạng thái + Khoá/Mở khoá, Xoá, Xuất Excel, Import Excel |
| 2 | Chỉ 2 trường nghiệp vụ **Mã + Tên** (+ Trạng thái). **Không** có Mô tả |
| 3 | Danh mục thuần, **chưa gắn** vào Khách hàng / Dự án / Giải pháp |
| 4 | **2 quyền phẳng** (Quản lý / Xem) → **không** thêm `company_id`/`department_id`/`part_id` vào bảng |
| 5 | Bảng hiện **9 cột đầy đủ** (có Người/Ngày cập nhật) |
| 6 | **Tạm bỏ hành động Lịch sử** (bộ `catalog_histories` dùng chung chưa tồn tại ở nhánh này) |

## Mã & Tên

- Mã: `LVKDNB.` + hậu tố **1–4 ký tự** `[A-Za-z0-9_]`, tự viết hoa khi lưu, unique.
- Tên: bắt buộc, ≤255, **check trùng khi bấm Lưu** → 422, hiện lỗi inline, không đóng modal.
- Metadata (người/ngày tạo, người/ngày cập nhật) ghi tự động theo tài khoản, không có ô nhập.

## Nợ kỹ thuật đã biết (chỉnh sau khi gộp DB)

Skill `list-page` mô tả 6 thành phần dùng chung **không tồn tại trong repo này** (đã kiểm toàn bộ
nhánh local + remote): `V2BaseSmartFilterPanel`, `V2BaseRowActions`, popup Cấu hình cột
(`columnCustomizationMixin`), popup Chọn trường xuất file (`export-fields-modal` +
`ExportColumnRegistry` + `DynamicExport`), bộ Lịch sử danh mục (`catalog_histories` +
`LogsCatalogHistory` + `CatalogHistoryModal`), `V2BaseModal`.

→ User chốt: **trước mắt làm theo mẫu `customer_scopes`**, sau khi gộp DB xong sẽ điều chỉnh.

Các quy tắc list-page **vẫn áp ngay** vì không cần hạ tầng mới: tách cột Mã / Tên · Mã là link mở
modal Xem · bỏ nút Xem · cột Hành động ở cuối · auto-search deep watcher · `V2BaseBadge` +
`status_text` · ngày `d/m/Y H:i` · Người tạo chỉ hiện tên · sort whitelist · sắp theo độ khớp ·
căn lề + width chuẩn · nút không dùng được thì ẩn hẳn · cờ quyền fail-closed · `loadData()` bắn đầu
tiên + `loadSeq`.

## Quy tắc chốt thêm trong lúc làm

- **Validate báo ĐỒNG THỜI mọi trường**: bấm Lưu 1 lần phải hiện hết lỗi của mọi ô sai (cả Mã và Tên
  đều gắn vee-validate; lỗi BE 422 map theo từng field). Lỗi hiện bằng `V2BaseError` + viền đỏ
  `is-invalid`, focus ô lỗi đầu tiên; lỗi BE của ô nào tự mất khi user sửa lại chính ô đó.
- **File mẫu Import**: `hrm-client/static/Mau_import_LinhVucKinhDoanhNoiBo.xlsx` (sinh bằng
  PhpSpreadsheet) — dòng 1 header, dòng 2 hướng dẫn (`skipRows=1`), dòng 3-4 mẫu import được thật.
  Nút Import của `V2BaseImportModal` chỉ bật khi **không còn dòng lỗi**.

## Phạm vi kỹ thuật

- **BE** (`hrm-api`): 1 migration + Entity + Service + Controller + Request + 2 Resource + Export
  class + blade; sửa `Routes/api.php` và `PermissionsTableSeeder.php` (quyền id 1177 / 1178).
- **FE** (`hrm-client`): `pages/assign/internal-business-scopes/{index.vue, AddScopeModal.vue}` +
  chèn mục menu vào `components/menu-sidebar.js`.
- **E2E** (`e2e/`): `pages/InternalBusinessScopePage.ts` + `tests/assign/internal-business-scope.spec.ts`
  (10 ca UI) + `tests/assign/internal-business-scope.api.spec.ts` (7 ca API) + fixture
  `hrm-api/database/e2e_internal_scope_fixture.php` cho user KHÔNG có quyền. **19/19 PASS**.

## Danh sách file (bàn giao)

**hrm-api** — `database/migrations/2026_08_22_000001_create_internal_business_scopes_table.php` ·
`Modules/Assign/Entities/InternalBusinessScope/InternalBusinessScope.php` ·
`Modules/Assign/Services/InternalBusinessScopeService.php` ·
`Modules/Assign/Http/Controllers/Api/V1/InternalBusinessScopeController.php` ·
`Modules/Assign/Http/Requests/InternalBusinessScope/InternalBusinessScopeRequest.php` ·
`Modules/Assign/Transformers/InternalBusinessScopeResource/{,Detail}InternalBusinessScopeResource.php` ·
`Modules/Assign/Exceptions/LockedRecordException.php` · `app/ExcelExport/InternalBusinessScopeExport.php` ·
`resources/views/exports/internal_business_scopes.blade.php` · `database/e2e_internal_scope_fixture.php` ·
sửa `Modules/Assign/Routes/api.php` + `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.

**hrm-client** — `pages/assign/internal-business-scopes/{index.vue, AddScopeModal.vue}` ·
`static/Mau_import_LinhVucKinhDoanhNoiBo.xlsx` · sửa `components/menu-sidebar.js`.

**e2e** — `pages/InternalBusinessScopePage.ts` · `tests/assign/internal-business-scope.spec.ts` ·
`tests/assign/internal-business-scope.api.spec.ts`.

Ảnh chụp màn hình thật: `.plans/linh-vuc-kinh-doanh-noi-bo/screenshots/` (danh sách 9 cột, modal Xem,
lỗi trùng tên, validate đồng thời, dòng đã khoá, menu, import).
