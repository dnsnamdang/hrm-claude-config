# Task 5 report — FE Màn 1 "Quản lý tài khoản" /admin/accounts (hrm-client)

Status: DONE_WITH_CONCERNS (không commit; không migration/seeder; dữ liệu thử `Zz` đã dọn sạch)

## File (wt-rbac/hrm-client, tất cả LF)
- Mới:
  - `pages/admin/accounts/index.vue` — danh sách (V2BaseSmartFilterPanel floating + V2BaseDataTable, filterStateMixin `admin_accounts`,
    columnCustomizationMixin `admin_accounts`, exportFieldsMixin + `downloadExcel(admin/accounts/export?fields=…)`, DedupeLoadMixin).
  - `pages/admin/accounts/add.vue`, `pages/admin/accounts/_id/index.vue` — trang vỏ (`default-sidebar`, PageTitleMixin, unsavedChildFormMixin;
    tiêu đề sửa `Sửa tài khoản: <mã NV>`).
  - `pages/admin/accounts/components/AccountForm.vue` — form 3 khối V2BaseFormSection (unsavedChangesMixin + formValidateMixin).
  - `pages/admin/accounts/components/AccountHistoryModal.vue` — vỏ mỏng gọi `CatalogHistoryModal` (V2BaseModal bọc SystemInfoSection)
    với `endpoint-base="admin/accounts"`, entity `histories` ⇒ GET `admin/accounts/histories/{id}` (+ `/filter-options`).
- Sửa:
  - `components/subsystem-menu/admin.js` — mục "Tài khoản nhân viên" → nhãn "Quản lý tài khoản", link `/admin/accounts`, giữ `isShow` 5 tên.
  - `components/human-components/human-slidebar.vue` — gỡ mục id 27 "Danh mục tài khoản nhân viên".
  - `pages/human/employee/index.vue`, `add.vue`, `_id/index.vue` — thành trang chuyển hướng (page `middleware` → `redirect(301, …)`,
    giữ `:id`).
  - **`components/V2BaseSmartFilterPanel.vue` (component dùng chung, +4/−2)** — `mergedFields` nhận `isVisible: false` trên field schema =
    mặc định ẩn (khi chưa có cấu hình đã lưu / key mới), cùng quy ước `isVisible:false` của cột. Không khai = hiện như cũ. Đã rà: không
    `filterFields` nào khác khai `isVisible` (chỉ cột bảng) ⇒ không đổi hành vi màn khác. Cần cho "Địa điểm nhận suất ăn ẩn mặc định".
- Xoá: `components/human-components/employee/EmployeeForm.vue` (+ thư mục rỗng), `pages/human/employee/components/EmployeeHistoryModal.vue`
  (chỉ 2 trang cũ import; đã grep không còn tham chiếu). Store action `addEmployee`/`updateEmployee` để nguyên (vô hại).

## Hành vi chính
- Danh sách: ô tìm nhanh "Tìm theo mã nhân viên, tên, email" (Enter mới tìm); nâng cao 1 hàng Công ty → Phòng ban → Bộ phận
  (`V2BaseCompanyDepartmentFilter`, `inputCount` = số ô thật theo cấp xem) · Trạng thái (1 Hoạt động / 0 Khoá); "Địa điểm nhận suất ăn"
  khai trong schema, mặc định ẩn (chỉ khi `use_rice`). Cờ cấp xem cho ô tổ chức suy từ `$store.state.permissions` (4 tên quyền xem) —
  fail-closed, chỉ quyết định ô nào hiện; phạm vi thật do BE.
- 10 cột mặc định đúng design 3.3; 6 cột ẩn (Phòng ban, Bộ phận, Công ty chính, Mã check in cơm, Địa điểm nhận suất ăn, Hạn mức công nợ
  xuất hàng — số `toLocaleString('en-US')`). Badge `V2BaseBadge :color="status_color"` + `status_text` BE.
- `canManage` = `permissions.can_manage` BE trả (mặc định false): ẩn Thêm mới, Sửa, Khoá/Mở khoá; Mã NV là `nuxt-link` khi có quyền, chữ
  thường khi không. Không có "Xóa". Khoá/Mở khoá qua `$confirm` → POST `/{id}/lock|unlock` → nạp lại. 403 khi tải danh sách → `/pages/extras/404`.
- Form: khối 1 ảnh 96px (ảnh hồ sơ, không có nút máy ảnh — xem concern 1) + tên/mã·phòng; Hồ sơ nhân viên* (ⓘ, khoá khi sửa; nguồn
  `human/employee-infos/getEmptyInfos`, nhãn `employeeOptionText`) · Email*; Công ty chính (ⓘ) · Phòng ban (chỉ đọc, tên lấy từ store theo hồ
  sơ) · Trạng thái*. Khối 2 Mật khẩu/Nhập lại (thêm: bắt buộc; sửa: ô "Đổi mật khẩu" ở `#actions` tiêu đề, ⓘ cảnh báo đăng xuất phiên).
  Khối 3 Địa điểm nhận suất ăn · Mã check in cơm (chỉ đọc, ⓘ) · Hạn mức (V2BaseCurrencyInput) — không `use_rice` thì chỉ còn Hạn mức col-12.
  FE chỉ chặn định dạng (`email|max:255`, mật khẩu `min:6`); bắt buộc/nghiệp vụ = 422 BE, hiện hết dưới từng ô. Lưu xong `markFormSaved()` →
  `/admin/accounts`. Màn sửa: `SystemInfoSection` ngoài card, thu gọn mặc định. Người không có "Quản lý tài khoản nhân viên" mở add/sửa ⇒ 404;
  detail 403/404 ⇒ 404. PUT gửi `rice_ssn` (gợi ý max+1 BE trả khi chưa có — giữ hành vi form cũ), không gửi `employee_info_id`/`company_ids`.

## Kiểm Playwright MCP (rehearsal, 1280×~1279 viewport mặc định MCP)
⚠️ API 8011 đang chạy THIẾU `DB_*_TPE` ⇒ `GET admin/accounts` và `rice/setting/location` trả 500 "Unsupported driver []" (kết nối `mysql_tpe`,
hook cơm model Employee). Không đụng 8011: tôi chạy **thêm** 1 bản `php -S 127.0.0.1:8012` (cùng code wt-rbac/hrm-api, `DB_DATABASE=rehearsal`
+ `DB_*_TPE` trỏ `hrm_erp_rbac_rehearsal`, như hrm-api chính trỏ DB gộp), Playwright `page.route` chuyển request 8011→8012; xong đã kill đúng PID
8012 (và server tĩnh 8773 dùng xem mockup). 8011/3011 giữ nguyên.

namdangit (id 13):
- Danh sách: footer bảng "Hiển thị 1–10 / 1244" = API `meta.total` 1244 (curl); 10 dòng/trang. Lọc Trạng thái = Khoá: request
  `status=0&page=1&per_page=10`, "1–10 / 592" = API 592, mọi badge "Khoá".
- 4 ô lọc nâng cao (Công ty, Phòng ban, Bộ phận, Trạng thái): cùng `top=171`, `height=32`, `width=263` mỗi ô.
- Tiêu đề cột hiện: STT, Mã NV, Tên nhân viên, Email, Người tạo, Ngày tạo, Người cập nhật gần nhất, Ngày cập nhật gần nhất, Trạng thái,
  Hành động (đúng 10). Popup cấu hình cột: 6 cột ẩn `false`, 10 cột trên `true`. Cài đặt bộ lọc: "Công ty – Phòng ban – Bộ phận:true",
  "Trạng thái:true", "Địa điểm nhận suất ăn:false".
- Hành động dòng: 3 nút ri-edit-line (href `/admin/accounts/36`), ri-lock-line, ri-history-line (V2BaseRowActions ≤3 nút thì bày hết, không ⋮).
  Thanh công cụ: Thêm mới · Xuất Excel · Cấu hình cột, khoảng cách 10px (gap của slot `actions-bottom`; lúc đầu có `mr-2` ra 22px nên bỏ — khuôn
  wr-service-contracts).
- Thêm: Lưu trống ⇒ 4 lỗi cùng lúc "Bắt buộc phải nhập" (Hồ sơ, Email, Mật khẩu, Nhập lại) từ 422. Chọn hồ sơ Zz ⇒ email tự điền, Công ty
  chính / Phòng ban / Mã check in cơm (99990001) điền, khoá. Email `zz-bad` ⇒ realtime "Định dạng email không hợp lệ". Lưu ⇒ về `/admin/accounts`
  (không hỏi chưa lưu), tìm `ZZ990001` ⇒ 1 dòng, Người tạo/cập nhật "DNS Admin", Hoạt động.
- Sửa (`/admin/accounts/12171`): tiêu đề trang + `document.title` "Sửa tài khoản: ZZ990001"; hồ sơ khoá đúng nhãn; ô mật khẩu khoá tới khi tick
  "Đổi mật khẩu" (sau tick `disabled=false`); Hạn mức gõ 50000000 hiện "50,000,000". Bấm Quay lại khi chưa lưu ⇒ popup "Thông tin chưa lưu …
  Thoát / Ở lại", Ở lại giữ URL. Lưu ⇒ về danh sách.
- Khoá: `$confirm` "Xác nhận khoá … Khoá / Hủy" ⇒ badge "Khoá", nút đổi thành "Mở khoá"; Mở khoá ⇒ "Hoạt động".
- Lịch sử (popup): tiêu đề "Lịch sử thay đổi: ZZ990001 - Zz Thử Tài Khoản", 5 dòng mới→cũ: Mở khóa, Khóa, Thay đổi thông tin (Hạn mức (trống)→
  50,000,000), Thay đổi thông tin (Mật khẩu → Đã đặt lại (quản trị)), Tạo mới.
- Footer màn sửa (Lịch sử mở, cuộn tới đáy): khối SystemInfoSection bottom 848 < V2Footer top 1229 (z-index 1001) ⇒ không đè. Mọi ô form cao 32px.
- Redirect: `/human/employee` → `/admin/accounts`, `/human/employee/12171` → `/admin/accounts/12171`, `/human/employee/add` → `/admin/accounts/add`.
- Menu Quản trị (panel rail): span "Quản lý tài khoản" trong `<a href="/admin/accounts">`.
Không quyền — id 27 Chu Khương Duy (công ty 1, không vai trò/quyền trực tiếp nào chứa "tài khoản nhân viên"):
- API (8012): GET `admin/accounts` 403, GET `admin/accounts/12171` 403, GET `histories/12171` 403, POST `/12171/lock` 403.
- FE: `/admin/accounts`, `/admin/accounts/12171`, `/admin/accounts/add` đều về `/pages/extras/404` ("KHÔNG TÌM THẤY TRANG YÊU CẦU") — chặn ở
  middleware `checkPermission` theo menu `isShow` (trang còn tự 404 khi API 403 / không có quyền quản lý).
- Nuxt log `nuxt3011.log`: 1 "Failed to compile" thoáng qua lúc index.vue ghi trước AccountHistoryModal.vue (file chưa tồn tại), các lần biên dịch
  sau sạch; cảnh báo `SubsystemMenuAdmin … admin.js` có sẵn từ trước khi sửa (dòng 3842 < lần sửa đầu).

## Dữ liệu thử (rehearsal) + dọn
- INSERT tay `employee_infos` id **12606** (code `ZZ990001`, fullname `Zz Thử Tài Khoản`, email `zz.acc990001@test.local`, company 1, dept 42,
  ssn `99990001`, status 1) — rehearsal không có hồ sơ active nào chưa có tài khoản (`getEmptyInfos` = []).
- Qua UI/API sinh ra: `employees` id **12171**, `company_employees` 1 dòng (employee 12171), `employee_history` 5 dòng, `rice_employee_infos`
  id **2080** (hook cơm).
- Dọn (đã chạy, kiểm lại = 0 ở cả 6 truy vấn):
  `delete from employee_history where employee_id=12171; delete from company_employees where employee_id=12171;
   delete from rice_employee_infos where id=2080 and employee_id=12171; delete from employees where id=12171 and email='zz.acc990001@test.local';
   delete from employee_infos where id=12606 and code='ZZ990001';`
  Đã quét mọi bảng có cột employee_id/employee_info_id/email/code/ssn — không còn vết. AUTO_INCREMENT các bảng trên đã nhích (không trả lại).
- File tạm chứa JWT ở `.playwright-mcp/` đã xoá; cấu hình mysql tạm ở scratchpad đã xoá.

## Self-review
- Self-check `grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/admin/accounts/ | grep -v V2Base` rỗng;
  không `toLocaleString('vi-VN')`; không cờ quyền `= true`.
- Màn mới dùng V2Base*, V2BaseModal (qua CatalogHistoryModal), `$confirm`, V2Footer, unsavedChangesMixin + unsavedChildFormMixin, ⓘ qua prop
  `hint` của V2BaseLabel / b-popover `info-popover` (tiêu đề khối Mật khẩu), badge màu BE, nút ẩn chứ không disable, số en-US.
- Request lúc vào danh sách: list + cấu hình cột + cấu hình bộ lọc (+ địa điểm cơm khi `use_rice`). Form thêm: getEmptyInfos + địa điểm (+ 1 GET
  hồ sơ khi chọn); form sửa: detail + địa điểm.

## Concerns
1. **API 8011 thiếu `DB_*_TPE`** ⇒ danh sách /admin/accounts và địa điểm cơm 500 trên môi trường kiểm hiện tại (cả sửa/lưu tài khoản qua hook cơm).
   Controller cần khởi động lại 8011 kèm `DB_CONNECTION_TPE/HOST/PORT/DATABASE(=hrm_erp_rbac_rehearsal)/USERNAME/PASSWORD_TPE` trước Task 9 / kiểm
   tiếp. Tôi không đụng 8011.
2. **Nút máy ảnh trên ảnh đại diện (mockup/design 3.4) CHƯA làm**: API Task 4 không nhận `image` (ảnh nằm ở `employee_infos.image`), form cũ cũng đã
   comment phần upload; upload local còn ghi vào S3 PROD. Hiện ảnh chỉ đọc từ hồ sơ. Cần user chốt: bỏ nút, hay thêm BE nhận ảnh.
3. Sửa component dùng chung `V2BaseSmartFilterPanel.vue` (opt-in `isVisible:false` cho field lọc) — nằm ngoài danh sách file brief nhưng cần để
   làm "ẩn mặc định"; tương thích ngược (đã rà).
4. Lệch nhỏ có chủ đích: placeholder mật khẩu "Tối thiểu 6 ký tự" (mockup ghi 8 nhưng BE `min:6`); Lịch sử ở danh sách hiện thẳng là nút thứ 3
   (V2BaseRowActions chỉ gom ⋮ khi > 3 nút); khối 3 khi không `use_rice` đổi tiêu đề "Công nợ" và Hạn mức col-12; footer màn sửa chỉ Lưu + Quay lại
   theo mockup (không có Khoá — đổi trạng thái bằng ô Trạng thái; khác "footer khớp hành động dòng" của list-page 7.2, theo mockup đã duyệt).
5. `AccountHistoryModal` là vỏ mỏng trên `CatalogHistoryModal` thay vì chép lại `EmployeeHistoryModal` (tránh popup lịch sử riêng).
6. Cờ cấp xem cho ô lọc tổ chức suy từ `$store.state.permissions` (BE không trả `is_all_company…`); người chỉ có quyền quản lý không thấy ô
   Công ty/Phòng/Bộ phận (fail-closed) — chỉ còn Trạng thái.
7. Lịch sử BE: 1 lần Lưu đổi cả mật khẩu + hạn mức ra 2 dòng "Thay đổi thông tin" riêng (hành vi Task 4, không phải FE).
