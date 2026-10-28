# Giai đoạn 2 — Màn quản lý Vai trò & Quyền

> Hồ sơ con của `../design.md` (mục 6, mục 7 dòng 2). Ngày viết: 26/10/2026.
> User giao (26/10): "tự làm theo đề xuất của bạn và theo style chung của phần mềm, tôi duyệt lại sau",
> rồi "bạn tự duyệt rồi code luôn". Mọi điểm đánh **[Claude chốt]** là quyết định của Claude, user duyệt sau.
> Nền dữ liệu là GĐ1 (`../gd1-nen-du-lieu/design.md`): `roles.company_id` + `base_name`,
> `role_has_permissions.scope`, catalog `permissions.code/subsystem_group/subsystem/feature/kind/allowed_scopes/depends_on/on_erp/on_hrm`,
> `PermissionChecker`.

## 1. Phạm vi

**Làm trong GĐ2**
1. Màn **Danh sách vai trò** (công ty đang làm việc).
2. Popup **Thêm / Sửa vai trò**.
3. Màn **Phân quyền cho vai trò** (cây quyền + tìm nhanh + phạm vi + tổng hợp).
4. Popup **Quyền đang có** (xem nhanh từ danh sách) và popup **Lịch sử** của vai trò.
5. Khoá / Mở khoá, Xoá vai trò.
6. Gỡ màn phân quyền cũ: HRM `pages/timesheet/setting/roles/*`, `pages/human/roles/*`; ERP `common/roles/*`.
   Mục menu "Danh sách phân quyền" đổi thành "Vai trò" trỏ màn mới.

**Không làm trong GĐ2**
- **Màn người dùng** (công ty làm việc + cấp/gỡ vai trò): user chốt 26/10 *thiết kế lại sau GĐ2, nhưng phải
  xong trước khi lên prod*. GĐ2 không vá màn "Danh sách người dùng" cũ. Lịch sử cấp/gỡ vai trò, thêm/gỡ công ty
  làm việc thuộc phần đó.
- Đổi chỗ kiểm quyền theo tên sang theo mã ở các màn khác (GĐ3).

## 2. Menu, route, quyền

- Menu Quản trị › Người dùng & phân quyền: thay mục "Danh sách phân quyền" bằng **"Vai trò"** → `/admin/roles`.
- Route FE: `/admin/roles` (danh sách), `/admin/roles/:id/permissions` (phân quyền).
- Mọi API và màn gác bằng mã `admin.phan_quyen.manage` ("Quản lý phân quyền"). Thao tác không có phạm vi.
  - BE: `checkPermission:Quản lý phân quyền` (middleware GĐ1 đã kiểm qua `PermissionChecker` theo công ty đang
    làm việc, tên cũ tra alias ra mã). **[Claude chốt]** dùng tên cũ cho đến GĐ3, vì middleware nhận mã là việc GĐ3.
  - FE: `isShow` / `hasAPermission('Quản lý phân quyền')`, cùng lý do.
- **Cô lập công ty (phản mục tiêu mục 3):** mọi API lấy `company_id` từ công ty đang làm việc của người gọi
  (`employee_infos.company_role`), **không nhận `company_id` từ request**. Vai trò `id` thuộc công ty khác ⇒ 404
  (không lộ là có tồn tại). Áp cho xem, sửa, phân quyền, lịch sử, khoá, xoá.

## 3. Danh sách vai trò `/admin/roles`

Khuôn `list-page` (V2BaseDataTable + SmartFilterPanel), copy pattern màn danh mục đang chuẩn nhất.

- Băng tiêu đề: "Vai trò — <Tên công ty đang làm việc>".
- Tìm nhanh: `Tìm theo tên, mô tả vai trò`. Lọc: Trạng thái (Hoạt động / Đã khoá).
- Cột: STT · Vai trò (`base_name`, dòng phụ xám là mô tả) · Quyền đang có (số, bấm mở popup) · Số người giữ ·
  Trạng thái (`V2BaseBadge`, BE trả `status_text` + `status_color`) · Người cập nhật · Cập nhật lúc · Hành động.
- Hành động (menu ⋮): **Phân quyền** · Sửa · Lịch sử · Khoá / Mở khoá · Xoá. Ẩn hẳn nút không dùng được.
- Toolbar: **Thêm mới**.
- Không phân quyền theo cấp: danh sách luôn là mọi vai trò của công ty đang làm việc **[Claude chốt]**, vì quyền
  quản lý phân quyền không có phạm vi (catalog `scopes: []`).

## 4. Popup Thêm / Sửa vai trò

`V2BaseModal`, `unsavedModalMixin`, validate `form-validate`.

| Trường | Ghi chú |
|---|---|
| Tên vai trò * | Lưu vào `base_name`. `name` = `<mã công ty>_<base_name>` (quy tắc GĐ1). Trùng `base_name` trong cùng công ty ⇒ 422 `Đã tồn tại trên hệ thống`. Tối đa 150 ký tự. |
| Mô tả | `description`, tối đa 500. |
| Sao chép quyền từ | **Chỉ khi Thêm mới** **[Claude chốt]**. Chọn 1 vai trò của **cùng công ty**; vai trò mới nhận nguyên bộ quyền + phạm vi. Bỏ trống = vai trò rỗng. |

- Lưu xong về danh sách. Thêm mới xong hiện toast có lối "Phân quyền ngay" **[Claude chốt]**: nút trên toast thì
  lệch khuôn, nên **đi thẳng sang màn Phân quyền** khi không sao chép quyền (vai trò rỗng chưa dùng được), còn có
  sao chép thì về danh sách.
- `display_name` giữ nguyên giá trị cũ, không sửa ở màn mới (ERP đọc `display_name → base_name → name`, R22 GĐ1).
- Sửa vai trò đang khoá ⇒ 423 (quy tắc khoá CLAUDE.md HRM). Mở khoá trước.

## 5. Khoá / Mở khoá, Xoá

- **Khoá = vai trò ngừng hiệu lực** **[Claude chốt]**: người đang giữ mất các quyền của vai trò đó ngay. Hiện tại
  `PermissionChecker` không lọc `roles.status` (cả 283 vai trò đang `status = 1`), nên phải thêm điều kiện
  `r.status = 1` vào **cả 2 bản** checker (giữ giống từng byte). Đây là hướng fail-closed, không có vai trò nào
  đang khoá nên không đổi quyền hiệu lực của ai lúc chuyển đổi.
  - Popup xác nhận nói rõ: "N người đang giữ vai trò này sẽ mất các quyền của vai trò".
  - Vai trò khoá: ẩn Sửa, Phân quyền, Xoá; vẫn Xem quyền, Lịch sử, Mở khoá. BE chặn 423 ở sửa/phân quyền.
  - Xoá cache: sau khoá/mở khoá/lưu quyền gọi `PermissionChecker::flush()` + xoá cache spatie (HRM 24h).
- **Xoá**: chỉ khi **không còn ai giữ** vai trò (`employee_has_roles` = 0) **và** không có dữ liệu nào trỏ tới vai trò
  (bảng tham chiếu đã dò ở GĐ1 `Convert/role-references.php`). Còn thì ẩn nút Xoá, BE trả 422 kèm lý do.
  Xoá vật lý dòng `roles` + `role_has_permissions`, ghi lịch sử trước khi xoá. **[Claude chốt]**

## 6. Màn Phân quyền `/admin/roles/:id/permissions`

Bám mockup `.plans/demo-man-hinh-ke-toan/demo/phan-quyen.html`, đổi chữ "chức vụ" thành **Vai trò**.

- **Băng tiêu đề:** "Đang phân quyền cho vai trò **<base_name>** — <Tên công ty>". Công ty cố định.
- **Bộ lọc:** Nhóm phân hệ · Phân hệ · Chức năng · Loại quyền (Xem / Thao tác / Duyệt) · Nền tảng (ERP / HRM) ·
  ô **Tìm nhanh theo tên hoặc mã**. Có kết quả thì tự mở các nhánh chứa kết quả, tô vàng chữ khớp. Thêm
  "Chỉ hiện quyền đã chọn" **[Claude chốt]** để soát nhanh.
- **Cây:** Nhóm phân hệ → Phân hệ → Chức năng → Quyền. Dòng quyền: ô tick · tên · **mã** (chữ xám, font mono) ·
  nhãn loại · nhãn nền tảng (ERP / HRM / cả hai).
  - Quyền có `allowed_scopes` khác rỗng: ô chọn phạm vi chỉ gồm các cấp hợp lệ, mặc định cấp **cao nhất** khi tick
    **[Claude chốt]** (giống luật chuyển đổi "nhận phạm vi cao nhất"). Nhãn: Bộ phận / Phòng ban / Công ty / Tổng công ty.
  - Tick cả nhóm / cả phân hệ / cả chức năng: checkbox 3 trạng thái. Mở tất cả / Thu gọn.
  - **Quyền phụ thuộc** (`depends_on`): tick quyền Thao tác thì tự tick quyền Xem tương ứng (phương án C đã chốt).
    Bỏ quyền Xem khi còn quyền phụ thuộc vào nó ⇒ hỏi xác nhận bỏ luôn các quyền phụ thuộc. Chỉ là hành vi giao diện,
    BE không ép.
  - Quyền `deprecated_at` không hiện. Quyền ngừng dùng mà vai trò còn giữ thì BE vẫn giữ nguyên dòng, không xoá.
- **Bảng tổng hợp** bên phải (dính khi cuộn): tổng số quyền đã chọn, đếm theo loại, đếm theo phân hệ (bấm để nhảy
  tới), số thay đổi chưa lưu.
- **Footer** (`V2Footer`): Lưu · Bỏ chọn tất cả · Quay lại. Cảnh báo khi thoát lúc chưa lưu (`unsavedChangesMixin`).
- **Lưu:** gửi toàn bộ danh sách `{code, scope}`. BE kiểm: mã tồn tại và chưa ngừng dùng, `scope` thuộc `allowed_scopes`
  (quyền không có phạm vi ⇒ `scope` phải null). Ghi trong 1 transaction: xoá–chèn `role_has_permissions` của vai trò,
  ghi `company_id = roles.company_id` cho các truy vấn cũ còn đọc cột này. Ghi lịch sử dạng **diff** (thêm / bỏ / đổi
  phạm vi). Xoá cache. Lưu xong về danh sách.
- **Hiệu năng:** 1 API trả **cả catalog + các quyền đã gán** của vai trò (khoảng 900 quyền, chỉ các cột cần), FE dựng
  cây và lọc tại chỗ, không gọi API khi gõ tìm.

## 7. Popup Quyền đang có

Mở từ cột "Quyền đang có". Danh sách chỉ đọc, gom theo Phân hệ → Chức năng, mỗi dòng: tên · mã · phạm vi. Có ô tìm.
Nút "Phân quyền" ở footer (ẩn khi vai trò khoá).

## 8. Lịch sử

Dùng khung lịch sử có sẵn (`app/Services/SettingHistory`, adapter `RolePermissionAdapter`, bảng
`role_permission_history`), không tạo bảng mới. **[Claude chốt]**
- Sửa adapter: lọc theo `roles.company_id` thay cho `company_roles`; đọc được cả log cũ (snapshot) lẫn log mới (diff).
- Log mới: `create` (tên, mô tả, sao chép từ), `update` (trường đổi: cũ → mới), `permissions` (thêm / bỏ / đổi phạm vi,
  mỗi dòng ghi mã + tên lúc đó), `lock` / `unlock` (nhóm "Thay đổi trạng thái"), `delete`.
- Popup hiển thị theo skill `entity-history`.

## 9. API (hrm-api, prefix `/admin/roles`, middleware `auth:api` + `checkPermission:Quản lý phân quyền`)

| Method | Path | Việc |
|---|---|---|
| GET | `/admin/roles` | danh sách, phân trang, tìm, lọc trạng thái; kèm đếm quyền + đếm người giữ (`withCount`) |
| GET | `/admin/roles/options` | vai trò cùng công ty cho ô "Sao chép quyền từ" |
| POST | `/admin/roles` | thêm (kèm `copy_from_role_id`) |
| PUT | `/admin/roles/{id}` | sửa |
| DELETE | `/admin/roles/{id}` | xoá |
| POST | `/admin/roles/{id}/lock` · `/unlock` | khoá / mở khoá |
| GET | `/admin/roles/{id}/permissions` | catalog + quyền đã gán (cho màn phân quyền và popup Quyền đang có) |
| PUT | `/admin/roles/{id}/permissions` | lưu bộ quyền |
| GET | `setting-histories/role_permission/{id}` | lịch sử — endpoint chung có sẵn (`SettingHistoryModal`), không tạo route mới |

Module: đặt ở `Modules/Timesheet` cạnh `RoleService` cũ hay module mới? **[Claude chốt]** đặt trong `app/` theo nền
`app/Support/Permissions` (đây là lõi dùng chung cả 2 nền tảng, không thuộc phân hệ Chấm công):
`app/Http/Controllers/Api/Admin/RoleController.php` + `app/Services/Admin/RoleManagementService.php` + FormRequest.
Vai trò công ty khác ⇒ 404. Ngoại lệ (user chốt 27/10, chưa sửa): API lịch sử đi qua `SettingHistoryController` dùng chung
nên trả 403 (id không tồn tại cũng 403, không lộ thông tin).

## 10. Gỡ màn cũ

- hrm-client: xoá `pages/timesheet/setting/roles/*`, `pages/human/roles/*` và component chỉ các màn đó dùng
  (`components/setting/Permission.vue` + con, rà bằng grep trước khi xoá). Route cũ `/timesheet/setting/roles*`
  chuyển hướng sang `/admin/roles` **[Claude chốt]** để bookmark cũ không ra trang trắng.
- hrm-api: gỡ route `timesheet/roles` (trừ những gì màn người dùng cũ còn gọi — rà khi làm), `RoleService::save` đã ném
  `RetiredRoleScreenException` từ GĐ1.
- ERP: gỡ route + view `common/roles/*`, mục menu ERP trỏ sang URL màn HRM mới (mở tab HRM) **[Claude chốt]**.

**Thực tế đã gỡ (27/10):**
- hrm-client: xoá `pages/timesheet/setting/roles/**`, `pages/human/roles/**` (mỗi nơi để 1 trang chuyển hướng
  `middleware → redirect('/admin/roles')`), `components/setting/Permission.vue`,
  `components/timesheet/setting/roles/*` (BulkPermission*), action `saveRole` trong `store/actions.js`.
- hrm-api: nhóm `timesheet/roles` chỉ còn `GET /list` (màn người dùng cũ còn gọi); `Modules/Timesheet/.../RoleController`
  gọn còn `list()`; xoá `RolesListExport`, view `exports/roles_list.blade.php`, `RoleDetailResource`.
- ERP: xoá `Common/RolesController` + view `common/roles/`; `Route::any('roles/{any?}')` (tên `roleIndex`) chuyển hướng
  sang `{hrm_url_FE}/admin/roles`; breadcrumbs Roles bỏ; topmenubar/sidebar trỏ HRM, nhãn "Vai trò". `roles2` (danh mục
  chức vụ nhân sự) KHÔNG đụng.
- e2e cũ `HRM/e2e/tests/admin/permission-matrix-screens.spec.ts` (trỏ `/admin/roles/18`, màn ma trận chưa từng lên
  gop_db) đã lỗi thời — để nguyên, chưa xoá.

**Phát hiện khi kiểm Playwright trên DB đã chuyển đổi (27/10):**
- Sau `rbac:convert`, `role_has_permissions` KHÔNG còn `company_id` ⇒ ghi dòng quyền qua `grantRow()` (chỉ điền
  `company_id` khi cột còn — DB chưa chuyển đổi cột nằm trong PK).
- `b-form-checkbox` phát `input` khi prop đổi ⇒ đổi bộ lọc từng xoá cả nhánh đã chọn; `PermissionTree` chỉ phát khi giá
  trị khác trạng thái hiện tại.
- `.content-page` overflow:hidden giết sticky ⇒ cây quyền có vùng cuộn riêng, khung tóm tắt đứng cạnh.

## 11. Kiểm chứng

- PHPUnit (hrm-api): mỗi API có ca **có quyền / không quyền / vai trò công ty khác (404)**; lưu quyền với mã lạ,
  mã ngừng dùng, phạm vi không hợp lệ (422); khoá ⇒ người giữ mất quyền (qua `PermissionChecker`); xoá khi còn người giữ (422).
- ERP: test checker bỏ vai trò khoá (bản checker ERP).
- Playwright MCP trên `hrm_erp_rbac_test`, tài khoản `namdangit@gmail.com`: đo DOM — số dòng, số quyền đếm ở bảng tổng hợp
  khớp API, tìm theo mã mở đúng nhánh, ô phạm vi chỉ có cấp hợp lệ, footer không đè nội dung, tick Thao tác tự tick Xem.
- Spec e2e mới `e2e/admin-roles.spec.ts` (chưa chạy trừ khi user yêu cầu — memory "không tự chạy e2e").

## 12. Để builder quyết

Tên file, chia component, cách dựng cây ở FE (khuyến nghị dựng 1 lần thành map, lọc bằng cờ ẩn để giữ trạng thái mở),
khuôn bảng tổng hợp.
