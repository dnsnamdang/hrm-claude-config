# GĐ2b — Màn Quản lý tài khoản + Màn Quản lý vai trò nhân viên

> Hồ sơ con của `../design.md` (mục 5.2, mục 6 "Quản lý tài khoản", mục 7 dòng 2). Ngày viết: 27/10/2026.
> Phần "màn người dùng" bị tách khỏi GĐ2 (`../gd2-man-quan-ly/design.md` §1). User chốt 26/10: *làm lại sau GĐ2
> nhưng phải xong trước khi lên prod*. Code trên `wt-rbac` nhánh `rbac` (3 repo), cùng cửa sổ lên prod với GĐ1–4.
> **[user chốt 27/10]** = user nói trong hội thoại 27/10. **[Claude chốt]** = Claude tự quyết, user duyệt khi đọc hồ sơ.

**Mockup:** `mockup.html` (cùng folder, mở thẳng bằng trình duyệt; dựng trên DOM + CSS thật của app). **User DUYỆT mockup vòng 3 ngày 27/10/2026.**

## 1. Vì sao

Hôm nay một tài khoản bị chỉnh ở **3 màn**, mỗi màn một phần và không màn nào gác quyền cho đúng:

| Màn hiện tại | Làm gì | Vấn đề |
|---|---|---|
| HRM `/human/employee` "Tài khoản nhân viên" | Tạo/sửa tài khoản: hồ sơ, email, mật khẩu, trạng thái, **công ty kiêm nhiệm**, suất ăn, hạn mức công nợ | API `human/employee` **không gác quyền** ở thêm/sửa/khoá/xoá (ai đăng nhập cũng gọi được); `index` nhận `is_all=1` là **bỏ qua phạm vi xem** |
| HRM `/timesheet/setting/employees` "Danh sách người dùng" | Cấp vai trò ở công ty gốc + "Phân công quản lý phòng ban" | Chỉ thấy công ty gốc; vai trò ở công ty kiêm nhiệm không sửa được ở đâu ngoài ERP |
| ERP `employees` "Quản lý tài khoản người dùng" | Tạo tài khoản, sửa theo từng công ty (công ty + chức vụ + phòng/bộ phận quản lý), xoá, đổi mật khẩu | Trùng chức năng với 2 màn HRM; gọi vai trò là "chức vụ" |

Sau GĐ1 vai trò thuộc đúng 1 công ty và quyền tính theo công ty đang làm việc, nên việc cấp vai trò phải theo
nguyên tắc 5.2: quản trị viên công ty chính khai công ty làm việc, quản trị viên từng công ty cấp vai trò của
công ty mình.

## 2. Chốt phạm vi **[user chốt 27/10]**

Tách thành **2 màn**, cả hai nằm ở phân hệ **Quản trị** (component + URL đúng phân hệ), mọi màn cũ đóng:

| | Màn 1 — Quản lý tài khoản | Màn 2 — Quản lý vai trò nhân viên |
|---|---|---|
| URL | `/admin/accounts` | `/admin/employee-roles` |
| Thay cho | HRM `/human/employee` | HRM `/timesheet/setting/employees` |
| Quyền | "Quản lý tài khoản nhân viên" (`human.tai_khoan_nhan_vien.manage`) + xem danh sách theo cấp (`human.tai_khoan_nhan_vien.view`) | "Quản lý phân quyền" (`admin.phan_quyen.manage`) |
| Nội dung | Thông tin tài khoản. **Không liên quan phân quyền** | Công ty làm việc, cấp/gỡ vai trò, phân công quản lý phòng ban, cấp vai trò hàng loạt |
| Chuẩn | skill `list-page` | skill `list-page` + khuôn mockup phân quyền đã chốt (`.plans/demo-man-hinh-ke-toan/demo/phan-quyen.html`) |

- **Công ty làm việc chuyển sang Màn 2** [user chốt 27/10]: Màn 1 bỏ ô "công ty kiêm nhiệm".
- **Cấp vai trò hàng loạt giữ lại** ở Màn 2 [user chốt 27/10].
- **Đóng**: ERP `employees` (màn danh sách/tạo/sửa/xoá/đổi mật khẩu) và 2 màn HRM cũ. URL cũ chuyển hướng sang màn mới.

**Không làm**
- Đổi các chỗ kiểm quyền theo tên sang mã (GĐ3). Màn mới vẫn gác bằng tên quyền như GĐ2 (`../gd2-man-quan-ly/design.md` §2).
- Hồ sơ nhân viên (`employee_infos`, màn `/human/employee_info`) — không đụng.
- App mobile.

## 3. Màn 1 — Quản lý tài khoản `/admin/accounts`

### 3.1 Route FE + menu
- `pages/admin/accounts/index.vue` (danh sách), `pages/admin/accounts/add.vue`, `pages/admin/accounts/_id/index.vue` (sửa).
  Form tách thành `pages/admin/accounts/components/AccountForm.vue` (viết lại từ
  `components/human-components/employee/EmployeeForm.vue`), popup lịch sử chuyển từ
  `pages/human/employee/components/EmployeeHistoryModal.vue`.
- Layout `subsystem` (menu dọc Quản trị). Menu Quản trị › Người dùng & phân quyền: mục "Tài khoản nhân viên"
  đổi link sang `/admin/accounts`, đổi nhãn thành **"Quản lý tài khoản"**, giữ nguyên `isShow` (5 tên quyền).
- `pages/human/employee/*` gỡ, thay bằng trang chuyển hướng `/human/employee[/…]` → `/admin/accounts[/…]`
  **[Claude chốt]** (giữ link cũ người dùng đã lưu). Gỡ mục ở `components/human-components/human-slidebar.vue`.

### 3.2 Phạm vi xem (BE)
- Mức theo quyền "Xem danh sách tài khoản nhân viên" (4 cấp). Giữ đúng hành vi `checkPermissionList` hiện tại
  (lọc theo `employee_infos.company_id / department_id / part_id`) **[Claude chốt]** — đây là màn hồ sơ tài khoản,
  không phải màn quyền.
- **Bỏ tham số `is_all`** ở API mới (đang là lỗ hổng bỏ qua phạm vi). Nơi khác còn gọi `human/employee?is_all=1`
  (popup chọn nhân viên…) giữ API cũ, rà và ghi danh sách ở plan.
- Không có cấp xem nào (kể cả người chỉ có "Quản lý tài khoản nhân viên"): chỉ thấy tài khoản có hồ sơ do **mình
  tạo** (`employee_infos.created_by`) — đúng code hiện tại (`checkPermissionList(..., true)` → nhánh `[4]`,
  `app/Helper/PermissionHelper.php:280`). **[Claude chốt]** giữ nguyên, không mở rộng quyền.
- Lưu ý: cấp Phòng ban / Bộ phận đọc `listManageDepartmentIds()` / `listManagePartIds()`, tức là dữ liệu
  **phân công quản lý phòng ban** do Màn 2 ghi (mục 4.4).

### 3.3 Danh sách (theo `list-page`)
- **Bộ lọc** `V2BaseSmartFilterPanel floating`:
  - Ô tìm nhanh: `Tìm theo mã nhân viên, tên, email` (Enter mới tìm).
  - Nâng cao **gọn 1 hàng** [user chốt 27/10]: Công ty → Phòng ban → Bộ phận (`V2BaseCompanyDepartmentFilter`,
    `inputCount` đúng số ô) · Trạng thái. "Địa điểm nhận suất ăn" khai trong schema nhưng mặc định ẩn (bật ở Cài đặt bộ lọc).
- **Cột** (mục 6 skill): hiện mặc định `STT · Mã NV (link) · Tên nhân viên · Email · Người tạo · Ngày tạo ·
  Người cập nhật gần nhất · Ngày cập nhật gần nhất · Trạng thái · Hành động` [user chốt 27/10 thêm 2 cột cập nhật].
  Ẩn sẵn: Phòng ban, Bộ phận, Công ty chính, Mã check in cơm, Địa điểm nhận suất ăn, Hạn mức công nợ xuất hàng.
  - Mã NV là `nuxt-link` sang `/admin/accounts/:id` khi có quyền quản lý; không có quyền thì chữ thường.
  - Trạng thái `V2BaseBadge` `brand` / `required` với `status_text` từ BE.
- **Hành động** (`V2BaseRowActions`): Sửa · Khoá / Mở khoá · ⋮ Lịch sử. Sửa + Khoá gate "Quản lý tài khoản nhân viên"
  (ẩn khi không có). **Bỏ "Xóa"** [Claude chốt]: `deleteEmployee` hiện chỉ đặt `status = 0`, trùng hẳn Khoá.
- **Thanh công cụ**: Thêm tài khoản (gate quản lý) · Xuất Excel (`exportFieldsMixin` + `ExportColumnRegistry`
  key `admin_accounts`) · Tuỳ chỉnh cột (`columnCustomizationMixin`, `columnScreenKey: 'admin_accounts'`).
- `filterStateMixin`: `localStorageKey: 'admin_accounts'`, `pathsToKeep: ['/admin/accounts']`.

### 3.4 Form Thêm / Sửa
- Giữ trường hiện có, xếp lại 3 khối `V2BaseFormSection` [user yêu cầu 27/10 "xếp khoa học, gọn"; bố cục theo mockup]:
  1. **Thông tin tài khoản**: cột trái ảnh đại diện (96px, **chỉ đọc** — đổi ảnh ở hồ sơ nhân viên, user chốt 27/10) + tên/mã/phòng ban; cột phải hàng 1 Hồ sơ nhân viên*
     (khoá khi sửa) · Email đăng nhập*; hàng 2 Công ty chính · Phòng ban (chỉ đọc, tự lấy theo hồ sơ) · Trạng thái*.
  2. **Mật khẩu**: Mật khẩu* · Nhập lại* (thêm); sửa: ô "Đổi mật khẩu" ở góc phải tiêu đề khối, tick mới nhập được.
  3. **Suất ăn & công nợ**: Địa điểm nhận suất ăn · Mã check in cơm (chỉ đọc) · Hạn mức công nợ xuất hàng.
  Mỗi hàng đủ 12 cột; giải thích đặt ở icon ⓘ cạnh nhãn (skill `info-icon-tooltip`), không dòng chú thích dưới ô.
- **Bỏ ô công ty kiêm nhiệm.** Khi **tạo** tài khoản, BE tự ghi `company_employees(employee, employee_infos.company_id)`
  (công ty chính) để tài khoản đăng nhập được ngay. Khi **sửa**, BE **không đụng** `company_employees` (bỏ
  `companies()->sync(company_ids)` — hiện đang xoá sạch rồi ghi lại).
- Form theo `form-validate` (FE chỉ định dạng, BE 422, hiện hết lỗi một lần) + `unsavedChangesMixin`.
  Lưu xong về danh sách (`list-page` 7.3). Lịch sử theo skill `entity-history`: màn sửa có khối `SystemInfoSection`
  ngoài card, sát dưới, thu gọn mặc định; danh sách ⋮ › Lịch sử mở popup `V2BaseModal` bọc chính khối đó.
- Đổi mật khẩu tăng `token_version` (giữ như cũ, đăng xuất phiên đang mở).

### 3.5 API (hrm-api)
- Nhóm mới `/admin/accounts` (`routes/api.php`, cạnh `/admin/roles`), controller
  `app/Http/Controllers/Api/V1/Admin/AccountController.php`, dùng lại logic `Modules\Human\Services\EmployeeService`
  (tách hàm khi cần, không copy).
  - `GET /` (danh sách) · `GET /export` · `GET /{id}` · `POST /` · `PUT /{id}` · `POST /{id}/lock` · `POST /{id}/unlock`.
  - Gate: đọc = có ít nhất 1 cấp xem hoặc quyền quản lý; ghi = `checkPermission:Quản lý tài khoản nhân viên`.
  - `show/update/lock` tài khoản **ngoài phạm vi xem** của người gọi ⇒ 404.
- Lịch sử: dùng lại `employee_histories` + `human/employee/{id}/histories` hiện có, chuyển sang
  `/admin/accounts/{id}/histories` cùng gate đọc.
- Route cũ `human/employee` (POST/PUT/updateStatus/DELETE): **gắn middleware quyền quản lý ngay** (vá lỗ hổng),
  giữ GET cho các popup đang gọi. Gỡ hẳn sau khi rà hết nơi gọi (ghi ở plan).

## 4. Màn 2 — Quản lý vai trò nhân viên `/admin/employee-roles`

### 4.1 Ai thấy ai, làm được gì **[Claude chốt, user duyệt 27/10]**
- Màn chỉ làm việc trong **công ty đang làm việc C** của người gọi (lấy từ `employee_infos.company_role`, không
  nhận `company_id` từ request — như `/admin/roles`).
- Danh sách = mọi tài khoản có `company_employees(employee, C)`, **kể cả tài khoản đang khoá** (có ô lọc Trạng thái).
- Với nhân viên E:
  - **C là công ty chính của E** (`employee_infos.company_id = C`): thêm/gỡ **công ty làm việc** của E, cấp/gỡ
    vai trò **của C**, sửa phân công quản lý phòng ban **trong C**.
  - **C là công ty kiêm nhiệm của E**: chỉ cấp/gỡ vai trò **của C** và phân công quản lý phòng ban **trong C**.
    Danh sách công ty làm việc chỉ đọc.
- **Gỡ công ty X** khỏi công ty làm việc của E ⇒ gỡ luôn mọi vai trò của E ở X và phân công quản lý phòng ban
  của E ở X. Trước khi lưu, hỏi xác nhận và liệt kê vai trò sẽ mất. Không được gỡ công ty chính.
- Không ai thấy hay sửa được vai trò của công ty khác C (khớp phản mục tiêu "rò quyền chéo công ty").

### 4.2 Route FE + menu
- `pages/admin/employee-roles/index.vue` (danh sách), `pages/admin/employee-roles/_id/index.vue` (chi tiết 1 nhân viên),
  component riêng trong `pages/admin/employee-roles/components/`.
- Menu: mục "Danh sách người dùng" đổi thành **"Vai trò nhân viên"** → `/admin/employee-roles`, `isShow: ['Quản lý phân quyền']`.
- `pages/timesheet/setting/employees/*` gỡ, thay bằng trang chuyển hướng sang `/admin/employee-roles[/:id]`.
  Gỡ luôn code chết `pages/timesheet/setting/employees/index.vue:290` (gọi route đã gỡ ở GĐ2).

### 4.3 Danh sách (theo `list-page`)
- **Bộ lọc**: tìm nhanh `Tìm theo mã nhân viên, tên, email` · nâng cao: Phòng ban → Bộ phận (trong C) ·
  Vai trò (chọn nhiều, vai trò của C) · Loại (Công ty chính / Kiêm nhiệm) · Trạng thái tài khoản ·
  "Chưa có vai trò nào" (Có/Không — để soát người làm ở C mà chưa được cấp gì) **[Claude chốt]**.
- **Cột** mặc định: `STT · Mã NV (link) · Email · Tên nhân viên · Phòng ban · Vai trò tại công ty này · Loại ·
  Người cập nhật · Cập nhật lúc · Hành động` [user chốt 27/10 Email sau Mã NV]. Ẩn sẵn: Bộ phận, Công ty chính,
  Công ty làm việc (danh sách tên), Trạng thái tài khoản.
  - Vai trò: chip theo `base_name`, tối đa 3 chip + "+n" (tooltip đủ tên). Bấm chip mở popup **"Quyền đang có"**
    của vai trò đó — dùng lại `pages/admin/roles/components/RolePermissionsViewModal.vue`.
  - "Người cập nhật / Cập nhật lúc" = lần cấp/gỡ gần nhất ở C (từ lịch sử), không phải `employees.updated_at`.
  - Không có cột Người tạo/Ngày tạo **[Claude chốt]**: màn này không tạo bản ghi; ghi chú ngoại lệ vào đầu file.
- **Hành động**: Sửa (sang chi tiết) · **Quyền đang được cấp** (mở popup 4.4b) · ⋮ Lịch sử (popup lịch sử chuẩn, adapter `employee_permission`).
- **Thanh công cụ**: Phân quyền hàng loạt · Xuất Excel · Tuỳ chỉnh cột.

### 4.4b Popup "Quyền đang được cấp" [user yêu cầu 27/10]
- Mở từ dòng danh sách và từ banner màn chi tiết. Tiêu đề phụ: `Mã - Tên · Vai trò tại <C>`.
- Thanh tab `V2BaseTabNavigation`: **mỗi vai trò của nhân viên tại C một tab** (nhãn = tên vai trò + số quyền + số quyền
  trùng), tab cuối **"Phòng ban đang quản lý"**.
- Tab vai trò: quyền nhóm theo phân hệ; cột Quyền · Mã quyền · Loại (Xem/Thao tác/Duyệt) · Phạm vi. **Quyền có ở từ 2 vai
  trò trở lên tô đỏ** + nhãn "Trùng: <vai trò kia>", đầu tab có dòng cảnh báo đếm số quyền trùng (quyền trùng vẫn có hiệu
  lực, phạm vi lấy mức cao hơn).
- Tab phòng ban: chia khối **Công ty chính — <mã>** và **Kiêm nhiệm — <mã>** (mỗi công ty kiêm nhiệm một khối), mỗi khối
  bảng Phòng ban · Bộ phận quản lý; "Quản lý tất cả phòng ban" hiện 1 dòng; chưa phân công thì ghi "Chưa phân công phòng ban nào".
  Lưu ý: tab này đọc phân công ở công ty KHÁC C (chỉ xem, không sửa) — theo yêu cầu user, phần quyền vẫn chỉ của C.
- API: `GET /admin/employee-roles/{id}/effective-permissions` (vai trò của C + quyền từng vai trò + phân công phòng ban mọi công ty làm việc).

### 4.4 Chi tiết `/admin/employee-roles/:id` [user chốt 27/10: 2 panel Chính – Phụ]
Bố cục 2 panel tỷ lệ **2 : 1** (`col-lg-8` / `col-lg-4`), khối Lịch sử full ngang bên dưới, `V2Footer` (Lưu · Quay lại):
- **Panel chính**
  1. **Vai trò tại C**: ô tìm vai trò theo tên + đếm số đang chọn; danh sách vai trò của C dạng ô tick (tên + mô tả + **số
     quyền**). Vai trò đã khoá hiện 🔒, không tick mới được (đang giữ thì vẫn hiện, gỡ được — skill `select-and-input-state`).
     **Bấm số quyền mở popup "Quyền đang có — <vai trò>"** = dùng lại `pages/admin/roles/components/RolePermissionsViewModal.vue`
     của GĐ2 (ô tìm theo tên/mã, nhóm Phân hệ › Chức năng, nhãn phạm vi, nút Phân quyền) [user yêu cầu 27/10].
  2. **Phân công quản lý phòng ban tại C**: chỉ đọc/ghi **dòng của C** (màn cũ cho chọn mọi công ty và mỗi lần lưu
     xoá sạch `employee_manage_departments` của nhân viên ở mọi công ty — sai nguyên tắc 5.2). UI: ô "Quản lý tất cả
     phòng ban của C" + bảng Phòng ban → Bộ phận (chọn nhiều). **[Claude chốt]** cờ "tất cả phòng ban" giữ đúng 2 nguồn
     mà `PermissionHelper.php:50-91` đang đọc:
     - C là công ty chính ⇒ `company_employees(E, C).all_department` (rehearsal: 28 dòng đang bật).
     - C là công ty kiêm nhiệm ⇒ dòng `employee_manage_departments(E, C, department_id NULL, all_department 1)` (rehearsal: 0 dòng).
     - Dòng phân công ở công ty khác công ty chính do màn cũ tạo (rehearsal: **32 dòng / 6 nhân viên**) **giữ nguyên**,
       từ nay chỉ quản trị viên công ty đó sửa — không dọn, vì đang có hiệu lực cho phạm vi xem.
- **Panel phụ**
  1. **Nhân viên**: ảnh, tên, `Mã · email`, phòng ban, nhãn "Công ty chính tại C" / "Kiêm nhiệm tại C", nút
     **"Quyền đang được cấp"** (popup 4.4b).
  2. **Công ty làm việc** (chỉ công ty chính sửa được): danh sách dọc `MÃ  Tên công ty`, công ty chính viền xanh + nhãn,
     không có ×; nút Thêm ở tiêu đề khối (chọn công ty đang hoạt động chưa có). Đổi xong chỉ ghi khi bấm Lưu.
  3. **Tổng hợp quyền hiệu lực tại C**: hợp các vai trò đang tick, đếm Xem/Thao tác/Duyệt + theo phân hệ (khuôn
     `rp-summary` của trang phân quyền); đổi tick là số đổi theo, chưa cần Lưu.
- **Lịch sử**: `SystemInfoSection` (skill `entity-history`), ngoài 2 panel, sát dưới, full ngang, thu gọn mặc định.
- `unsavedChangesMixin`. Lưu xong về danh sách.

### 4.4b Popup "Quyền đang được cấp" [user yêu cầu 27/10]
- Mở từ dòng danh sách và từ banner màn chi tiết. Tiêu đề phụ: `Mã - Tên · Vai trò tại <C>`.
- Thanh tab `V2BaseTabNavigation`: **mỗi vai trò của nhân viên tại C một tab** (nhãn = tên vai trò + số quyền + số quyền
  trùng), tab cuối **"Phòng ban đang quản lý"**.
- Tab vai trò: quyền nhóm theo phân hệ; cột Quyền · Mã quyền · Loại (Xem/Thao tác/Duyệt) · Phạm vi. **Quyền có ở từ 2 vai
  trò trở lên tô đỏ** + nhãn "Trùng: <vai trò kia>", đầu tab có dòng cảnh báo đếm số quyền trùng (quyền trùng vẫn có hiệu
  lực, phạm vi lấy mức cao hơn).
- Tab phòng ban: chia khối **Công ty chính — <mã>** và **Kiêm nhiệm — <mã>** (mỗi công ty kiêm nhiệm một khối), mỗi khối
  bảng Phòng ban · Bộ phận quản lý; "Quản lý tất cả phòng ban" hiện 1 dòng; chưa phân công thì ghi "Chưa phân công phòng ban nào".
  Lưu ý: tab này đọc phân công ở công ty KHÁC C (chỉ xem, không sửa) — theo yêu cầu user, phần quyền vẫn chỉ của C.
- API: `GET /admin/employee-roles/{id}/effective-permissions` (vai trò của C + quyền từng vai trò + phân công phòng ban mọi công ty làm việc).

### 4.4 Chi tiết `/admin/employee-roles/:id`
Bố cục theo khuôn mockup phân quyền (thẻ banner + thẻ nội dung, `V2Footer`):
1. **Banner**: ảnh + `Mã - Tên` + Phòng ban + nhãn "Công ty chính: …" / "Kiêm nhiệm tại: C" + ô cố định
   "Công ty: C" (như banner trang phân quyền).
2. **Công ty làm việc** (chỉ công ty chính sửa được): danh sách chip công ty, nút Thêm (chọn công ty đang hoạt động
   chưa có), × để gỡ (không có × ở công ty chính). Đổi xong chỉ ghi khi bấm Lưu.
3. **Vai trò tại C**: danh sách vai trò của C dạng ô tick (tên + mô tả + số quyền), lọc nhanh theo tên, vai trò
   đã khoá hiện 🔒 và không tick mới được (vai trò khoá đang giữ thì vẫn hiện, gỡ được — skill
   `select-and-input-state`). Bên phải: bảng **tổng hợp quyền hiệu lực tại C** (hợp các vai trò đang tick, đếm
   theo phân hệ, như `rp-summary` của trang phân quyền) để người cấp thấy trước người này sẽ có gì.
4. **Phân công quản lý phòng ban tại C**: chỉ đọc/ghi **dòng của C** (màn cũ cho chọn mọi công ty và mỗi lần lưu
   xoá sạch `employee_manage_departments` của nhân viên ở mọi công ty — sai nguyên tắc 5.2). UI: ô "Quản lý tất cả
   phòng ban của C" + bảng Phòng ban → Bộ phận (chọn nhiều). **[Claude chốt]** cờ "tất cả phòng ban" giữ đúng 2
   nguồn mà `PermissionHelper.php:50-91` đang đọc:
   - C là công ty chính ⇒ `company_employees(E, C).all_department` (rehearsal: 28 dòng đang bật).
   - C là công ty kiêm nhiệm ⇒ dòng `employee_manage_departments(E, C, department_id NULL, all_department 1)`
     (rehearsal: 0 dòng).
   - Dòng phân công ở công ty khác công ty chính do màn cũ tạo (rehearsal: **32 dòng / 6 nhân viên**) **giữ nguyên**,
     từ nay chỉ quản trị viên công ty đó sửa — không dọn, vì đang có hiệu lực cho phạm vi xem.
5. Khối **Lịch sử** (`SystemInfoSection`, `employee_permission`).
- Footer: Lưu · Quay lại. `unsavedChangesMixin`. Lưu xong về danh sách.

### 4.5 Phân quyền hàng loạt [user chốt 27/10: tuân thủ giao diện đang có]
- **Giữ nguyên popup đang có** `components/timesheet/setting/roles/BulkPermissionModal.vue` (+ `BulkPermissionFilter`,
  `BulkPermissionEmployeeList`) — chuyển về `pages/admin/employee-roles/components/`: trái "Đối tượng phân quyền" (Khối,
  Phòng ban, Bộ phận, Chức vụ, Chức danh + "Tất cả", NV bổ sung) + "Chọn vai trò"; phải danh sách nhân viên (lọc phụ,
  Tất cả / Đã chọn / Loại trừ, tick bỏ từng người, Xuất Excel); chân "Tổng SL NV sẽ cập nhật" + Áp dụng / Áp dụng và làm tiếp / Hủy.
  Chế độ hiện chỉ **Cấp** (phần Cấp/Thu hồi đang ẩn trong code — giữ như vậy).
- **Sửa lỗ hổng chéo công ty** (popup hiện liệt kê phòng ban/vai trò của mọi công ty, vd chi nhánh Hải Phòng, TPSG_…):
  mọi danh sách chọn và danh sách nhân viên chỉ lấy của **C** (nhân viên có `company_employees(·, C)`, phòng ban/bộ
  phận/khối của C, vai trò `roles.company_id = C` đang hoạt động); BE kiểm lại toàn bộ id gửi lên thuộc C (khác ⇒ 422).
  Tiêu đề popup thêm nhãn "Công ty: <C>" + 1 dòng ghi chú phạm vi. Nhãn "Chọn quyền" → **"Chọn vai trò"**.
- Dùng lại `BulkPermissionService`, chuyển route sang `/admin/employee-roles/bulk/*`, lấy công ty từ
  `current_company_role` (không phải claim JWT). Mỗi nhân viên được cấp ghi 1 dòng lịch sử (`company_id = C`).

### 4.6 API (hrm-api)
- Nhóm `/admin/employee-roles` (`routes/api.php`), `checkPermission:Quản lý phân quyền`, controller
  `app/Http/Controllers/Api/V1/Admin/EmployeeRoleController.php` + service `app/Services/Admin/EmployeeRoleService.php`.
  - `GET /` · `GET /export` · `GET /{employeeId}` (công ty làm việc, vai trò của C đang giữ, danh sách vai trò của C,
    phân công phòng ban ở C, cờ `is_main_company`) · `PUT /{employeeId}` (lưu 1 lần: `role_ids`, `company_ids` khi là
    công ty chính, `manage_departments`) · `POST /bulk/preview` · `POST /bulk/apply`.
  - Nhân viên không làm việc ở C ⇒ 404. `role_ids` có id không thuộc C hoặc vai trò khoá mới thêm ⇒ 422.
    `company_ids` gửi khi C không phải công ty chính ⇒ 403. Gỡ công ty chính ⇒ 422.
- Ghi vai trò qua `Employee::syncRolesInCompany($employeeId, C, $roleIds)` (đã ghi 2 `model_type` HRM + ERP).
  Gỡ công ty X: `syncRolesInCompany(E, X, [])` + xoá `employee_manage_departments` của E ở X, trong cùng transaction.
- Sau khi ghi: xoá cache quyền của E (spatie + cache `PermissionChecker` nếu có) để quyền đổi ngay; E đang đăng
  nhập thấy quyền mới ở lần gọi API kế tiếp.
- Lịch sử: mở rộng `EmployeePermissionAdapter` (`employee_permission`) — snapshot theo công ty C: vai trò,
  công ty làm việc, phân công phòng ban; mỗi lần lưu 1 dòng, ghi ai/lúc nào/trước/sau (mục 6 Lịch sử của design tổng).
- Gỡ: `Modules/Timesheet` route `timesheet/employees/*`, `timesheet/roles/list`, `timesheet/bulk-permissions/*`
  sau khi FE không còn gọi (giữ route chuyển hướng FE thôi).

## 5. Đóng màn ERP

- ERP `employees`: gỡ `index`, `create`, `store`, `edit`, `update`, `delete`, `doimatkhau` + view
  `common/employees/{index,create,edit}.blade.php`. Các route `employees/*` dùng chung để tra cứu
  (`searchData…`, `searchEmployee…`, `getDataEmployee`, `checkHasPermission`, `history`, `exportList`) — rà nơi gọi,
  còn dùng thì giữ.
- `employees` và `employees/{id}/edit` chuyển hướng `Route::redirect` (không dùng closure — bài học `route:cache` GĐ2)
  sang HRM `/admin/accounts`. Widget trang chủ ERP (`HomeController.php:916` link `employeeIndex?status=2`) đổi
  sang link HRM.
- Menu ERP (`sidebar.blade.php`, `topmenubar.blade.php`): "Quản lý tài khoản người dùng" → HRM `/admin/accounts`,
  thêm "Vai trò nhân viên" → HRM `/admin/employee-roles` cạnh mục "Vai trò".
- Quyền ERP "Quản lý tài khoản" (`admin.tai_khoan.manage`, chỉ ERP) không còn màn nào dùng — xem câu hỏi mở Q1.

## 6. Kiểm thử

- PHPUnit (hrm-api `tests/Feature/Rbac/`): mỗi API có ca **có quyền / không quyền / ngoài phạm vi (404)**; Màn 2
  thêm: công ty kiêm nhiệm không gửi được `company_ids` (403); vai trò công ty khác (422); gỡ công ty X gỡ cả vai
  trò ở X; lịch sử ghi đủ trước/sau; route cũ `human/employee` POST/PUT không quyền ⇒ 403 (vá lỗ hổng); `is_all`
  không còn bỏ qua phạm vi ở API mới.
- ERP: route chuyển hướng cache được (`prepareForSerialization`), menu trỏ HRM.
- Playwright MCP trên `hrm_erp_rbac_rehearsal` (DB đã convert), tài khoản namdangit (id 13) + 1 tài khoản không quyền:
  đo DOM (số dòng = API total, cột mặc định, chiều cao ô lọc, footer không đè), có quyền / không quyền ở cả 2 màn,
  một nhân viên kiêm nhiệm để thấy khác biệt công ty chính / kiêm nhiệm.
- e2e: `HRM/e2e/tests/admin/admin-accounts.spec.ts`, `admin-employee-roles.spec.ts` (viết, chạy khi user yêu cầu).

## 7. Đã kiểm trên rehearsal 27/10
- Tài khoản đang hoạt động thiếu dòng `company_employees` của công ty chính: **0** ⇒ không cần backfill; plan
  vẫn giữ 1 bước kiểm lại trên bản sao prod trước go-live (thiếu dòng nào là tài khoản đó không hiện ở Màn 2).
- `employee_permission_history`: 50 dòng, **không có cột công ty**; snapshot gồm phân công phòng ban của mọi công ty.

## 8. Câu hỏi đã chốt (27/10)

- ~~Q1~~ **[user chốt 27/10: B]** Quyền ERP "Quản lý tài khoản" (`admin.tai_khoan.manage`) **ngừng dùng** — không gộp,
  không sửa catalog/chuyển đổi GĐ1. Đóng màn ERP thì không còn chỗ nào kiểm quyền này; đánh dấu `deprecated` trong
  catalog khi gỡ màn. Báo cáo chuyển đổi liệt kê người có quyền ERP mà không có "Quản lý tài khoản nhân viên"
  (rehearsal: 1 người) để admin cấp lại nếu cần. Menu ERP trỏ HRM gate bằng 5 tên quyền của Màn 1.
- ~~Q2~~ **[user chốt 27/10]** Giữ cấp vai trò hàng loạt (mục 4.5), bỏ chế độ "Thay thế".
- ~~Q3~~ **[user chốt 27/10: A]** Thêm cột `company_id` (nullable + index) vào `employee_permission_history`
  (1 migration hrm-api, chạy riêng sau khi user cho phép). Mỗi lần lưu ở Màn 2 ghi 1 dòng mang `company_id = C`;
  quản trị viên C chỉ xem dòng của C. 50 dòng cũ (`company_id` NULL) chỉ quản trị viên công ty chính của nhân viên
  xem — như hiện nay. Cột "Người cập nhật / Cập nhật lúc" ở danh sách lấy dòng mới nhất có `company_id = C`.

## 9. Quyết định đã chốt khi code (27/10)

- Ảnh đại diện ở form tài khoản **chỉ đọc**, bỏ nút máy ảnh của mockup [user chốt 27/10] — ảnh thuộc `employee_infos`, đổi ở màn hồ sơ nhân viên.
- Sửa component dùng chung `V2BaseSmartFilterPanel.vue`: ô lọc khai `isVisible: false` trong schema = mặc định ẩn [user chốt 27/10 giữ].
- Cho chạy migration `2026_11_02_000001` vào cả `hrm_erp_rbac_rehearsal` để kiểm UI [user chốt 27/10].
- Route lịch sử tài khoản: `/admin/accounts/histories/{id}` (+ `/filter-options`) theo khuôn URL của `SystemInfoSection` [Claude chốt].
- Gỡ công ty X ở Màn 2 ghi thêm 1 dòng lịch sử `company_id = X` để quản trị viên X thấy vai trò bị gỡ [Claude chốt].
- Nhãn lịch sử vai trò nhân viên: "Vai trò" (thay "Quyền") [Claude chốt].
- Bật "Quản lý tất cả phòng ban" thì **giữ** các dòng phân công từng phòng ở C (≥6 module Finance/Assign/Training đọc thẳng bảng); bỏ tick mới thay dòng theo form. Cờ đọc đủ 2 nguồn như `PermissionHelper::employeeManagesAllDepartmentsIn` [Claude chốt].
- Dòng phân công không có bộ phận hiện "Chưa chọn bộ phận" (không phải "Tất cả bộ phận" — sai với quyền theo bộ phận) [Claude chốt].
- Tổng hợp quyền hiệu lực bỏ vai trò đang khoá (khớp `PermissionChecker`) [Claude chốt].
- Gỡ hẳn route ghi cũ `POST/PUT/DELETE human/employee` + `updateStatus` (rà hết nơi gọi) thay vì chỉ gắn quyền — route cũ còn `companies()->sync` bỏ qua mọi luật Màn 2 [Claude chốt].
- `admin.tai_khoan.manage` chỉ ghi chú "ngừng dùng" trong catalog, CHƯA đặt deprecated: quyền này vẫn gác ERP `employee.searchData` (popup chọn NV phiếu thu/chi) — chờ user.
- **27/10 (user cho làm): đã gỡ `employee.searchData` ở ERP (nhánh rbac, chưa commit).** Popup chọn NV chỉ hiện ở "Thu khác" (3) / "Chi khác" (10) + đối tượng Nhân viên; dropdown tạo của ERP (đo Playwright) và HRM đều KHÔNG có loại 3/10, rehearsal 0 phiếu loại 3/10 ⇒ chỉ là code chết. Đã bỏ: option "Nhân viên" ở select đối tượng 2 form, ô chọn NV từng dòng + `chooseEmployee` ở 2 class dòng, route + `EmployeesController@searchData`. Giữ: `formShow` (xem phiếu cũ), khối NV đầu phiếu chi (`searchAllEmployee`, route khác). HRM: popup dùng chung `components/modals/SelectEmployeesModal.vue` (`human/employee-infos/list`) nếu sau này mở lại loại 3/10. (xem dòng dưới)
- **27/10 (user cho làm): đã bỏ `admin.tai_khoan.manage` khỏi catalog hrm-api** (`Catalog/admin.php`), 3 tên cũ web "Quản lý tài khoản" / "… theo tổng công ty" / "… theo công ty" chuyển sang `dropped_legacy.php` (lý do `user_bo`) — để `rbac:convert` bỏ lượt gán thay vì DỪNG vì "tên cũ không thuộc danh mục". Route HRM `employee-infos/{id}/basic` gate tên cũ nằm trong khối comment, không chạy. Test Rbac hrm-api 238/238. Dry-run `permission:catalog-sync` trên rehearsal: ngừng dùng 1 (`admin.tai_khoan.manage`, 8 lượt gán vai trò — checker/màn quản trị đều lọc `deprecated_at`) + sửa 846 = CHỈ `sort_order` lùi 1 (đã đối chiếu, 0 lệch khác). CHƯA chạy sync thật vào DB nào.

## 10. Ghi chú triển khai
- Môi trường chạy `/admin/accounts` phải có `DB_*_TPE` (rule `exists` địa điểm suất ăn chạy kết nối `mysql_tpe`).
- **User chốt 27/10 (1A · 2A · 3A) — đã đưa vào `gd1-nen-du-lieu/runbook-go-live.md` mục B.4b**, chạy ngay sau `rbac:convert`: (1) kiểm tài khoản hoạt động thiếu `company_employees` công ty chính (rehearsal 0); (2) xuất CSV rồi XOÁ `employee_has_roles` mồ côi (rehearsal 12 dòng / 11 NV — cả 11 id không còn trong `employees`); (3) báo cáo người mất quyền quản lý tài khoản, admin tự cấp lại — SQL mới đọc `bak_rbac_*` (rehearsal **0 người**; SQL cũ ở `task-8-report.md` lỗi thời: tra theo mã đã bỏ + không lọc tài khoản khoá ⇒ ra nhầm NV 258 đã khoá; NV 256 có quyền mới qua Super Admin).
- Lưu Màn 2 ở công ty chính xoá dòng cờ NULL cũ khi bỏ tick "tất cả" (đúng luật 2 nguồn).
