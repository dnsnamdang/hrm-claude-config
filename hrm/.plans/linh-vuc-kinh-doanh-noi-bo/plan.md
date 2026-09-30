# Plan — Danh mục Lĩnh vực kinh doanh nội bộ

**Spec:** `docs/superpowers/specs/2026-08-22-linh-vuc-kinh-doanh-noi-bo-design.md`
**Design tóm tắt:** `.plans/linh-vuc-kinh-doanh-noi-bo/design.md`
**Nhánh:** `linh-vuc-noi-bo` (đã checkout từ `tpe` ở CẢ `hrm-api` + `hrm-client`)

**Goal:** Danh mục Lĩnh vực kinh doanh nội bộ (bảng `internal_business_scopes`) với màn danh sách 9
cột + modal Tạo/Sửa/Xem, mã `LVKDNB.XXXX`, tên không trùng, metadata tự ghi.

**Kiến trúc:** Copy khuôn `customer_scopes` (Entity → Service → Controller → Resource → Routes ở
`Modules/Assign`; FE `pages/assign/...` + modal), bỏ phần nhóm n-n và Mô tả, áp thêm các quy tắc
`list-page` không cần hạ tầng mới.

## Ràng buộc toàn cục (áp cho MỌI task)

- PHP 7.4 (không `?->`, không union type) · Laravel 8 · Nuxt 2 / Vue 2 / Bootstrap-Vue 2.15 · Node 14.21.3 cho client.
- Model mới **BẮT BUỘC `extends BaseModel`**; `created_by`/`updated_by` phải nằm trong `$fillable`.
- `auth()->id()` là `employees.id` — KHÔNG dùng `auth()->user()->info->id`.
- Cờ quyền FE **fail-closed**, mặc định `false`, cấm gán literal `true`.
- Nút không dùng được thì **ẩn hẳn**, không disable.
- Chữ trong ô bảng để **thường**, không in đậm.
- Ngày giờ hiển thị **`d/m/Y H:i`** (không giây). Người tạo/cập nhật chỉ hiện **tên**.
- Đỏ chỉ dùng cho lỗi validate.
- Không commit / không push (theo CLAUDE.md) trừ khi user yêu cầu.

---

## Phase 1 — Backend

### Task 1: Migration + Entity

**Files**
- Create `hrm-api/database/migrations/2026_08_22_000001_create_internal_business_scopes_table.php`
- Create `hrm-api/Modules/Assign/Entities/InternalBusinessScope/InternalBusinessScope.php`

- [x] **B1.** Viết migration đúng schema spec §2.1 (`code` string(50) unique, `name` string(255) index, `status` tinyInteger default 1, `created_by`/`updated_by` unsignedBigInteger nullable, `timestamps`). KHÔNG thêm company_id/department_id/part_id. KHÔNG bọc trong `DB::transaction`.
- [x] **B2.** Viết Entity theo spec §2.2: `extends BaseModel`, `$table`, hằng `STATUS_ACTIVE/STATUS_INACTIVE/CODE_PREFIX/CODE_SUFFIX_MAX`, `$fillable = ['code','name','status','created_by','updated_by']`, các method `isActive/isLocked/isCanEdit/isCanDelete`, accessor `status_text`, `created_by_name`, `updated_by_name` (chỉ `fullname`, null-safe kiểu PHP 7.4).
- [x] **B3.** Chạy `php7.4 artisan migrate` → bảng tồn tại: `php7.4 artisan tinker --execute="dump(Schema::hasTable('internal_business_scopes'));"` phải ra `true`.
- [x] **B4.** Tạo thử 1 bản ghi bằng tinker với user đăng nhập giả (`Auth::loginUsingId(<id>)`) → `created_by`/`updated_by` khác NULL. Xoá bản ghi thử sau khi kiểm.

### Task 2: FormRequest

**Files**
- Create `hrm-api/Modules/Assign/Http/Requests/InternalBusinessScope/InternalBusinessScopeRequest.php`

- [x] **B1.** `extends Modules\Training\Http\Requests\BaseRequest`. `prepareForValidation()`: `strtoupper(trim($code))` + `trim($name)`.
- [x] **B2.** Rules theo spec §3.1/§3.2:
  `code` → `required`, `regex:/^LVKDNB\.[A-Za-z0-9_]{1,4}$/`, `unique:internal_business_scopes,code,{id}`, closure chặn trường hợp chỉ có prefix (`LVKDNB.`) trả `Bắt buộc phải nhập`.
  `name` → `required`, `max:255`, `not_regex:/[,:]/`, `unique:internal_business_scopes,name,{id}`.
  `status` → `nullable|in:1,2`.
- [x] **B3.** `messages()` đúng câu chữ trong spec §3.1 (bảng câu lỗi) và §3.2.
- [x] **B4.** `$this->id` lấy từ body (luồng `POST /`) và fallback `$this->route('internalBusinessScope')` (luồng `PUT`).

### Task 3: Service

**Files**
- Create `hrm-api/Modules/Assign/Services/InternalBusinessScopeService.php`

- [x] **B1.** `index(Request $request)`: `select` cột cần + eager load `employee_create.info:id,fullname`, `employee_update.info:id,fullname`; lọc `keyword` (mã, tên, **người tạo bằng `EXISTS`**), `code`, `name`, `status`, `created_by`, `updated_by`, `updated_from`, `updated_to`; whitelist sort `code/name/createdAt/updatedAt`; mặc định `id DESC`.
- [x] **B2.** `applyRelevanceOrder()` theo spec §5.3 — chỉ chạy khi từ khoá ≥ 2 ký tự VÀ `sort_by` rỗng; nhớ `IF(LOCATE(...)=0, 9999, LOCATE(...))` và `id DESC` cuối cùng.
- [x] **B3.** `getAll()`: chỉ `status = STATUS_ACTIVE`, `orderBy('name')`.
- [x] **B4.** `updateOrCreate($request)` (tạo mới hoặc sửa theo `id` trong body) + `update($request, $scope)`; **gọi `assertNotLocked($scope)` trước khi ghi**.
- [x] **B5.** `assertNotLocked($scope, $action)` → ném exception mang HTTP 423 với message `Bản ghi đang bị khoá, vui lòng mở khoá trước khi cập nhật.` / `... trước khi xoá.`
- [x] **B6.** `destroy($scope)` (có `assertNotLocked`), `lock($scope)`, `unlock($scope)` — dùng `$scope->save()` để hook audit chạy.
- [x] **B7.** `validateImportData(array $rows)` + `importScopes(array $rows)` theo spec §4.4 (chấm: sai định dạng mã, trùng mã trong file, trùng mã DB, thiếu tên, trùng tên; trả `rows[]/validCount/invalidCount/total`).

### Task 4: Resource + Controller + Routes + Permission

**Files**
- Create `hrm-api/Modules/Assign/Transformers/InternalBusinessScopeResource/InternalBusinessScopeResource.php`
- Create `hrm-api/Modules/Assign/Transformers/InternalBusinessScopeResource/DetailInternalBusinessScopeResource.php`
- Create `hrm-api/Modules/Assign/Http/Controllers/Api/V1/InternalBusinessScopeController.php`
- Modify `hrm-api/Modules/Assign/Routes/api.php` (thêm block ngay TRÊN `/assign/customer-scopes`)
- Modify `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- [x] **B1.** 2 Resource trả đúng bộ field spec §4.2, ngày dùng `Helper::formatDateTime($x, 'd/m/Y H:i')`.
- [x] **B2.** Controller: `index`, `getAll`, `show`, `updateOrCreate`, `update`, `delete`, `lock`, `unlock`, `export`, `validateImport`, `import` — khuôn `CustomerScopeController`, **rethrow `ValidationException`** (không nuốt thành 400), bắt exception khoá → trả 423.
- [x] **B3.** Routes theo bảng spec §4 (middleware `checkPermission:` đúng tên quyền; route xem gắn cả 2 quyền).
- [x] **B4.** Thêm 2 permission id 1177 / 1178 vào seeder (spec §5.2) rồi chạy lại seeder trên DB local; kiểm `select id,name from permissions where id in (1177,1178)`.
- [x] **B5.** Smoke test API bằng `curl` với JWT: `GET /api/v1/assign/internal-business-scopes` trả 200 và `data: []`; `POST` tạo 1 bản ghi hợp lệ → 200; `POST` mã sai định dạng → 422; `POST` tên trùng → 422; khoá rồi `PUT` → 423.

### Task 5: Export Excel

**Files**
- Create `hrm-api/app/ExcelExport/InternalBusinessScopeExport.php`
- Create `hrm-api/resources/views/exports/internal_business_scopes.blade.php`

- [x] **B1.** Export class khuôn `CustomerScopeExport` (`FromView` + `Exportable` + `forData`).
- [x] **B2.** Blade copy `customer_scopes.blade.php`, cột: STT, Mã, Tên, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật (bỏ cột Loại hình + Mô tả).
- [x] **B3.** Gọi `GET /export` bằng curl → tải được file, mở bằng `openpyxl`/Excel kiểm đúng cột + đúng bộ lọc.

---

## Phase 2 — Frontend

### Task 6: Menu

**Files**
- Modify `hrm-client/components/menu-sidebar.js` (mảng `Danh mục`, chèn TRƯỚC mục "Nhóm ngành" ở dòng ~318)

- [x] **B1.** Thêm mục `{ label: 'Lĩnh vực kinh doanh nội bộ', link: '/assign/internal-business-scopes', isShow: ['Quản lý danh mục lĩnh vực kinh doanh nội bộ', 'Xem danh mục lĩnh vực kinh doanh nội bộ'] }`.

### Task 7: Màn danh sách

**Files**
- Create `hrm-client/pages/assign/internal-business-scopes/index.vue`

- [x] **B1.** Khung trang + `V2BaseFilterPanel` **không truyền title/subtitle**, ô tìm nhanh + 6 ô nâng cao với placeholder theo spec §6.4.
- [x] **B2.** `V2BaseDataTable` 9 cột theo bảng spec §6.3 (đúng `align`/`width`/`sortable`/`sticky`).
- [x] **B3.** Ô Mã render `<button class="v2-cell-link field-line">` mở modal Xem; ô Trạng thái dùng `V2BaseBadge` + `status_text`; ô trống hiện `—`.
- [x] **B4.** Cột Hành động ở cuối: Sửa / Khoá-Mở khoá / Xoá với điều kiện `visible` theo spec (ẩn hẳn, không disable).
- [x] **B5.** Auto-search deep watcher (`ignoredFields: ['keyword']`, reset về trang 1), `handleReset`/`handleSort` không tự gọi `loadData()`.
- [x] **B6.** `created()` bắn `loadData()` trước, `loadPermissions()` sau; dùng `$safeLoadingStart/$safeLoadingFinish`; `loadSeq` chống race; options người tạo/cập nhật chỉ nạp khi mở panel nâng cao.
- [x] **B7.** Xác nhận Xoá / Khoá bằng `BaseConfirmModal`; sau khi khoá/mở khoá cập nhật state tại chỗ.
- [x] **B8.** Xuất Excel tải trực tiếp `?token=` (khuôn `report/meeting-by-market/index.vue:385`), KHÔNG dùng blob.
- [x] **B9.** `<style lang="scss">` có `@import '@/assets/scss/v2-styles.scss';`.

### Task 8: Modal Tạo / Sửa / Xem

**Files**
- Create `hrm-client/pages/assign/internal-business-scopes/AddScopeModal.vue`

- [x] **B1.** Copy khuôn `pages/assign/industry-groups/AddScopeModal.vue`, bỏ ô Mô tả và 2 ô đếm.
- [x] **B2.** 1 hàng 3 ô: Mã (`V2BaseCodeInput prefix="LVKDNB." maxlength=4`), Tên, Trạng thái (`V2BaseSelectInModal`, disable khi bản ghi đang Khoá).
- [x] **B3.** vee-validate cho ô Tên (`v-validate="'required|max:255'"`, `data-vv-name`, `data-vv-as`, `data-vv-value-path="currentValue"`); lỗi BE 422 map vào `formError` hiện dưới đúng ô.
- [x] **B4.** Footer: Lưu · Lưu & Tiếp tục (chỉ khi tạo) · Đóng. Chế độ Xem chỉ còn Đóng.
- [x] **B5.** `V2BaseMetaInfo` chip ở header + block Người tạo/Ngày tạo ở cuối body khi sửa/xem.

### Task 9: Import Excel

**Files**
- Modify `hrm-client/pages/assign/internal-business-scopes/index.vue`

- [x] **B1.** Gắn `V2BaseImportModal` với 2 cột Mã / Tên (kèm `aliases`), `template-file-name="Mau_import_LinhVucKinhDoanhNoiBo.xlsx"`, `existing-data-key="code"`.
- [x] **B2.** Nối 2 handler `@validate-data` → `POST /import/validate`, `@import-data` → `POST /import`; nút Import chỉ hiện khi `canManage`.

---

## Phase 3 — Kiểm thử & bàn giao

### Task 10: Chạy thật + kiểm audit

- [x] **B1.** Bật API (`php7.4 artisan serve --port=8000`) + client (`node 14`, heap 8192) rồi mở `/assign/internal-business-scopes`.
- [x] **B2.** Tạo → Sửa 1 bản ghi, mở lại danh sách: **cột Người cập nhật / Ngày cập nhật phải có giá trị** (cách duy nhất phát hiện thiếu audit). Kiểm SQL `select code,created_by,updated_by from internal_business_scopes`.
- [x] **B3.** Khoá 1 bản ghi → nút Sửa/Xoá biến mất; gọi `PUT` bằng curl → 423.
- [x] **B4.** Import file mẫu 3 dòng (1 hợp lệ, 1 sai mã, 1 trùng tên) → 1 thành công / 2 lỗi.

### Task 11: Playwright E2E

**Files**
- Create `e2e/pages/InternalBusinessScopePage.ts`
- Create `e2e/tests/assign/internal-business-scope.spec.ts`

- [x] **B1.** Page object: selector bảng, ô tìm nhanh, nút Tạo mới, các ô trong modal, nút Lưu/Đóng, nút hành động theo dòng.
- [x] **B2.** Spec 13 ca theo spec §8.1 (gồm ca **trùng tên** và 2 ca **phân quyền**).
- [x] **B3.** `npx playwright test --list` chạy được (không lỗi TS/config).
- [x] **B4.** Chạy thật `npm test -- internal-business-scope` với FE + API đang bật; đính kèm ảnh chụp màn hình danh sách + modal lỗi trùng tên.

### Task 12: Wrap up

- [x] **B1.** Đánh dấu `[x]` các task trong file này + ghi checkpoint.
- [x] **B2.** Cập nhật `.plans/STATUS.md` (mục "Đang làm").
- [x] **B3.** Báo user kết quả + phần còn nợ (6 thành phần chuẩn list-page + hành động Lịch sử).

---

## Phase 4 — Sửa theo phản hồi user (2026-08-22, sau khi bàn giao lần 1)

### Task 13: Validate báo ĐỒNG THỜI lỗi của mọi trường

**Files**: Modify `hrm-client/pages/assign/internal-business-scopes/AddScopeModal.vue` · `e2e/pages/InternalBusinessScopePage.ts` · `e2e/tests/assign/internal-business-scope.spec.ts`

- [x] **B1.** Khai rule riêng `lvkdnb_code` bằng `Validator.extend` ngay trong modal (tên rule riêng, KHÔNG sửa `plugins/vee-validate.js` dùng chung); trả 2 câu lỗi khác nhau cho "trống hậu tố" và "sai định dạng".
- [x] **B2.** Gắn `v-validate` cho ô Mã (trước chỉ có ô Tên) → `validateAll()` chạy 1 lượt, mọi ô sai báo cùng lúc.
- [x] **B3.** Đổi hiển thị lỗi sang component chung `V2BaseError` + viền đỏ `is-invalid` (bù style cho `V2BaseCodeInput` bằng `::v-deep`, không sửa component chung).
- [x] **B4.** Focus ô lỗi đầu tiên (Mã → Tên) cho cả lỗi FE lẫn lỗi BE 422.
- [x] **B5.** Ưu tiên hiển thị theo skill `form-validate`: `errors.first(x) || formError.x`.
- [x] **B6.** E2E: đổi selector sang `.v2-error__text`, thêm ca "Bấm Lưu form trống → 2 lỗi đồng thời + 2 ô viền đỏ".

### Task 14: File mẫu Import Excel

**Files**: Create `hrm-client/static/Mau_import_LinhVucKinhDoanhNoiBo.xlsx` · Modify `pages/assign/internal-business-scopes/index.vue` · `e2e/pages/InternalBusinessScopePage.ts` · `e2e/tests/assign/internal-business-scope.spec.ts`

- [x] **B1.** Sinh file mẫu bằng PhpSpreadsheet (script `scratchpad/gen_template_lvkdnb.php`): dòng 1 header, dòng 2 hướng dẫn, dòng 3-4 mẫu import được thật.
- [x] **B2.** Nối `@download-template` + đưa tên file qua computed `importTemplateFile`.
- [x] **B3.** Test thật: tải mẫu → upload → Load lên bảng → Validate (1 hợp lệ / 1 trùng) → sửa dòng lỗi → Import OK → dọn dữ liệu test.
- [x] **B4.** E2E: thêm thao tác import vào page object + ca "tải được file mẫu và nạp đúng 2 dòng mẫu".

---

## Phát sinh trong lúc làm (khác plan ban đầu)

1. **Thứ tự rule của ô Mã**: closure kiểm "chỉ có tiền tố" phải đặt TRƯỚC `regex`, vì `BaseRequest`
   chỉ trả lỗi ĐẦU TIÊN của mỗi field — để sau thì user bỏ trống hậu tố lại nhận câu lỗi định dạng.
2. **Lỗi 422 của BE không tự mất khi user sửa lại ô** → thêm watcher `data.name` / `data.code` xoá
   `formError` tương ứng, nếu không lỗi cũ che mất validate realtime.
3. **Nút "Làm mới" không nạp lại danh sách**: deep watcher bỏ qua khi `keyword` đổi (nằm trong
   `ignoredFields`) mà Làm mới thì xoá cả keyword → thêm cờ `skipFilterWatch` + tự gọi `loadData()`
   đúng 1 lần trong `handleReset`.
4. **Permission ghi thẳng vào DB local** (`role_has_permissions` có cột `company_id`, phải để `= 1`
   như các quyền khác) — KHÔNG chạy `PermissionsTableSeeder` vì seeder `truncate` cả bảng
   `permissions`. File seeder vẫn được cập nhật để môi trường khác chạy đúng.
5. **Line ending**: `components/menu-sidebar.js` là file CRLF — lần sửa đầu bằng script Python làm
   hỏng toàn bộ line ending (923 dòng diff giả), đã `git checkout` trả lại và sửa lại với
   `newline=''`. Diff cuối cùng đúng +8 dòng.
6. **Fixture E2E cho ca KHÔNG có quyền**: tạo file riêng `hrm-api/database/e2e_internal_scope_fixture.php`
   (role "E2E No Catalog" + user `e2e_nocatalog@test.local`), KHÔNG sửa `e2e_provision.php` dùng chung.
   Fixture dùng `insertOrIgnore` vì Playwright chạy 2 worker song song.
7. **Validate phải báo ĐỒNG THỜI mọi trường** (user phản hồi 2026-08-22): ban đầu chỉ ô Tên gắn
   vee-validate nên bấm Lưu chỉ chặn ở Tên, lỗi Mã sang lượt sau mới hiện. Đã gắn validate cho CẢ
   2 ô (rule riêng `lvkdnb_code` khai bằng `Validator.extend` trong modal), đổi sang component lỗi
   chung `V2BaseError` + viền đỏ `is-invalid` + focus ô lỗi đầu tiên. Thêm 1 ca E2E riêng.
8. **Thiếu file mẫu Import** (user phản hồi 2026-08-22): `template-file-name` trỏ tới file chưa tồn
   tại và chưa nối `@download-template`. Đã sinh `hrm-client/static/Mau_import_LinhVucKinhDoanhNoiBo.xlsx`
   bằng PhpSpreadsheet (header + dòng hướng dẫn + 2 dòng mẫu) và nối handler tải file. Test thật:
   tải mẫu → upload → Load lên bảng → Validate (1 hợp lệ / 1 trùng) → sửa dòng lỗi → Import OK.
9. Bug CÓ SẴN của repo (không thuộc feature): `php artisan route:list` chết vì
   `Modules/Decision/Routes/web.php` thiếu namespace controller → phải verify route bằng server thật.

## Checkpoint

### Checkpoint — 2026-08-22 (wrap up)
Vừa hoàn thành: 14/14 task — BE + FE + E2E + 2 đợt sửa theo phản hồi (validate báo đồng thời mọi
trường; bổ sung file mẫu Import Excel). **19/19 test Playwright PASS** (7 API + 10 UI + 2 setup),
verify UI thật bằng Playwright MCP, dữ liệu test đã dọn (DB chỉ còn 2 bản ghi demo AUTO/ELEC).
Đang làm dở: không.
Bước tiếp theo: user rà giao diện + nghiệm thu. Khi đưa lên môi trường khác: chạy migration
`2026_08_22_000001_create_internal_business_scopes_table` + tạo 2 quyền id 1177/1178 (seeder đã có,
nhưng `PermissionsTableSeeder` truncate cả bảng `permissions` nên môi trường đang chạy phải insert
thủ công) + gán quyền cho role. Chưa commit theo quy tắc project.
Blocked: không.

## Việc chưa làm (chờ user quyết)

- Chuyển file mẫu Import sang sinh bằng endpoint API (đúng skill `import-excel`) thay vì file tĩnh —
  hiện bám theo 8 màn danh mục cùng menu.
- 5 quy tắc `list-page` còn nợ (SmartFilterPanel · popup Cấu hình cột · popup Chọn trường xuất file ·
  hành động Lịch sử · `V2BaseModal`) — làm sau khi gộp DB, theo quyết định của user.
- SRS `.docx` và `testcase.xlsx`: chưa tạo (chỉ tạo khi được yêu cầu).

---

## Phase 5 — Đổi tên hiển thị (2026-08-27)

Danh mục đổi tên **"Lĩnh vực kinh doanh nội bộ" → "Lĩnh vực Công ty kinh doanh"**.
GIỮ NGUYÊN: URL `/assign/internal-business-scopes`, bảng `internal_business_scopes`, cột
`internal_business_scope_id`, tiền tố mã `LVKDNB.`, id quyền 1177/1178, tên file mẫu Import.

- [x] **B1.** Đổi mọi chuỗi hiển thị FE (menu, tiêu đề bảng/modal, nhãn, placeholder, confirm, toast,
      nhãn cột Import) — 6 file `hrm-client`.
- [x] **B2.** Đổi câu lỗi validate + thông báo import + header Excel BE — 9 file `hrm-api`.
      Tên file xuất: `danh_sach_linh_vuc_kinh_doanh_noi_bo.xls` → `danh_sach_linh_vuc_cong_ty_kinh_doanh.xls`.
- [x] **B3.** Đổi header trong `static/Mau_import_LinhVucKinhDoanhNoiBo.xlsx` và
      `Mau_import_NhomNganh.xlsx`; **giữ tên cũ trong `aliases`** để file mẫu cũ vẫn nạp được.
- [x] **B4.** Đổi **tên quyền** 1177/1178 → `Quản lý / Xem danh mục lĩnh vực Công ty kinh doanh`
      ở `Routes/api.php`, `PermissionsTableSeeder.php`, `e2e_internal_scope_fixture.php`,
      `menu-sidebar.js` (`isShow`), `index.vue` (`hasAPermission`).
- [x] **B5.** Cập nhật DB local `hrm_tpe`: `UPDATE permissions SET name/display_name` cho id 1177,1178
      + `php artisan cache:clear` (xoá cache quyền của spatie). Đã quét toàn DB: không còn chuỗi cũ.
- [x] **B6.** Cập nhật text mong đợi trong 4 spec E2E + `InternalBusinessScopePage.ts`.

### ⚠️ Bắt buộc khi lên môi trường khác (staging/production)

Tên quyền lưu trong DB, KHÔNG tự đổi theo code. Chạy trước/cùng lúc với deploy, nếu không sẽ
**mất menu + 403 toàn bộ màn**:

```sql
UPDATE permissions SET name='Quản lý danh mục lĩnh vực Công ty kinh doanh',
       display_name='Quản lý danh mục lĩnh vực Công ty kinh doanh' WHERE id=1177;
UPDATE permissions SET name='Xem danh mục lĩnh vực Công ty kinh doanh',
       display_name='Xem danh mục lĩnh vực Công ty kinh doanh' WHERE id=1178;
```

Sau đó `php artisan cache:clear`. KHÔNG chạy `PermissionsTableSeeder` (seeder `truncate` cả bảng
`permissions`).

## Phase 6 — Tài liệu (2026-08-27)

- [x] **B1.** SRS: `docs/srs/linh-vuc-cong-ty-kinh-doanh.md` (13 mục — use case, business rule,
      data model, API spec, UI spec, edge case, deploy, nợ kỹ thuật).
- [x] **B2.** Testcase: `docs/srs/linh-vuc-cong-ty-kinh-doanh-testcases.xlsx` (**201 ca**, 16 nhóm)
      + bản markdown để review trong git + script sinh `docs/srs/generate_testcase_lvctkd.py`.

### Checkpoint — 2026-08-27 (đổi tên + tài liệu)

Vừa hoàn thành:
- **Phase 5 — Đổi tên hiển thị** "Lĩnh vực kinh doanh nội bộ" → "Lĩnh vực Công ty kinh doanh", gồm cả
  **tên quyền** 1177/1178. Sửa 6 file `hrm-client` + 9 file `hrm-api` + 5 file `e2e`, header 2 file
  xlsx mẫu, tên file xuất Excel. Giữ nguyên URL / bảng / cột / tiền tố `LVKDNB.` / tên file mẫu.
  Giữ tên cũ trong `aliases` của cột Import → file mẫu cũ vẫn nạp được.
  DB local `hrm_tpe` đã `UPDATE permissions` + `artisan cache:clear`.
- **Phase 6 — Tài liệu**: SRS `.md` + `.docx` (pandoc, 23 bảng, có TOC) và 201 testcase (16 nhóm)
  ở `docs/srs/`, kèm script sinh lại.

Kiểm chứng đã chạy: PHP 7.4 `-l` sạch toàn bộ file BE sửa · `node --check` cho `menu-sidebar.js`
(CRLF nguyên vẹn, diff đúng 3 dòng) · so khớp byte-for-byte tên quyền trong DB với 5 chỗ dùng trong
code · quét toàn bộ cột varchar/text của `hrm_tpe` → không còn chuỗi tên cũ.

Đang làm dở: không. Code đã được user commit và gộp vào `tpe`.

Bước tiếp theo:
- Chạy lại Playwright sau đổi tên (máy hiện tại chưa cài `e2e/node_modules`) — 19 ca đã sửa text
  mong đợi nhưng CHƯA chạy thật.
- Khi deploy: chạy 2 câu `UPDATE permissions` ở Phase 5 cùng lúc với deploy code.

Blocked: không.

### Việc chưa làm (cập nhật 2026-08-27)

- Chạy lại bộ E2E sau khi đổi tên (chưa verify bằng test thật).
- 5 quy tắc `list-page` còn nợ + file mẫu Import sinh bằng endpoint API — chờ gộp DB.
- Bản `.pdf` / `.html` của SRS (nếu cần gửi ngoài) — một lệnh pandoc.

## Phase 7 — Gỡ conflict merge `tpe` → `tpe-develop-assign` (2026-09-18)

File: `hrm-client/pages/assign/internal-business-scopes/AddScopeModal.vue` (4 vùng conflict).
Hai phía lệch nhau về hướng validate: `tpe` bỏ hẳn validate FE theo khuôn Nhóm ngành, còn nhánh
`tpe-develop-assign` đang thêm ô "Thời gian hiệu lực nhu cầu" (#11377) có validate FE.

- [x] **B1.** Ô Mã: giữ `maxlength="4"` của nhánh dev, bỏ `v-validate` theo `tpe`.
- [x] **B2.** Bỏ rule FE `lvctkd_code` (`Validator.extend`) — `import { Validator }` đã bị `tpe` gỡ,
      giữ lại là `Validator is not defined`. Mã/Tên để BE chốt như khuôn Nhóm ngành.
- [x] **B3.** Giữ CẢ HAI computed vì khác mục đích: `isCannotLock` (`tpe`, disable ô Trạng thái khi
      còn Nhóm ngành đang dùng) và `isLocked` (#11377, bám `savedStatus`, disable ô số ngày khi bản
      ghi đã Khóa).
- [x] **B4.** Giữ watch `data.demand_due_days` để xóa lỗi 422 cũ khi user sửa ô.
- [x] **B5.** `submitForm` chỉ còn validate riêng `demand_due_days` — auto-merge đã lấy bản `tpe`
      (bỏ `validateAll`) nên không còn gì chặn ô này ở FE.
      *Đính chính:* lúc kiểm tra, `hrm-api` local còn đứng ở `fix-bug-11092026` và chưa pull nên
      tưởng BE thiếu rule. Thực tế BE ĐÃ có `demand_due_days => required|integer|min:0|max:3650`
      (commit `c0f3974d2` / `ace1f47ec`). Rule FE khớp đúng rule BE, giữ lại làm lớp chặn sớm.

- [x] **B6.** BE — gỡ conflict `Modules/Assign/Http/Requests/InternalBusinessScope/InternalBusinessScopeRequest.php`:
      lấy bản `tpe` cho rule `code` (`required` → `size` → `regex`, bỏ closure kiểm tiền tố), đúng
      khuôn `Scope\ScopeRequest` của Nhóm ngành. Closure thành thừa vì gõ mỗi tiền tố cũng rơi vào
      `size` → vẫn báo "Vui lòng nhập 4 ký tự". Giữ nguyên rule + message `demand_due_days` của #11377
      (nằm ngoài vùng conflict).

Kiểm chứng: `vue-template-compiler` + `@babel/parser` parse sạch `AddScopeModal.vue` và `index.vue`;
không còn conflict marker trong repo. CHƯA mở trình duyệt chạy thử.

### Checkpoint — 2026-09-18

Vừa hoàn thành: gỡ conflict merge `tpe` → `tpe-develop-assign` ở CẢ 2 repo.
- `hrm-client/pages/assign/internal-business-scopes/AddScopeModal.vue` — 4 vùng conflict (B1–B5).
- `hrm-api/Modules/Assign/Http/Requests/InternalBusinessScope/InternalBusinessScopeRequest.php` —
  1 vùng conflict (B6).

Nguyên nhân gốc của conflict: `tpe` chốt hướng **bỏ validate FE cho Mã/Tên** (bám khuôn danh mục
Nhóm ngành, để BE chốt rule), trong khi `tpe-develop-assign` đang thêm ô "Thời gian hiệu lực nhu
cầu" (#11377) có validate FE. Nguyên tắc gỡ: **hướng chung lấy `tpe`, phần riêng của #11377 giữ
nguyên**, và giữ cả 2 computed `isCannotLock` / `isLocked` vì chúng phục vụ 2 ô khác nhau.

Kiểm chứng đã chạy:
- `vue-template-compiler` + `@babel/parser` parse sạch `AddScopeModal.vue` và `index.vue`.
- `php -l` sạch 3 file BE đang thay đổi (Request / Entity / Service).
- Không còn conflict marker nào ở `hrm-client/{pages,components,store}` và `hrm-api/Modules`.

Đang làm dở: không.

Bước tiếp theo:
1. Mở trình duyệt chạy thử màn Lĩnh vực Công ty kinh doanh — trọng tâm: ô Trạng thái khi bản ghi
   còn Nhóm ngành đang dùng (`isCannotLock`), ô số ngày khi bản ghi đã Khóa (`isLocked`), lỗi
   422 của Mã (gõ thiếu ký tự / sai ký tự / trùng mã).
2. ✅ Đã xong — user tự `git add` + commit merge: `hrm-client` `54dbb54de` · `hrm-api` `4225a9eed`.
3. Cân nhắc: có gỡ nốt `v-validate` của `demand_due_days` ở FE để bám tuyệt đối khuôn "FE không
   validate" không — BE đã có rule khớp y hệt. Mặc định đang GIỮ làm lớp chặn sớm.

Blocked: không.
