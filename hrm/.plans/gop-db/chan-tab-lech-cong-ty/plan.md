# Chặn tab lệch công ty đang làm — plan

> Fix lỗ hổng 27/10/2026 · @namdangit · hrm-api + hrm-client nhánh `gop_db` · không migration/seeder
> Design: `design.md` · spec: `docs/superpowers/specs/gop-db/2026-10-27-chan-tab-lech-cong-ty-design.md`

## Bối cảnh

Công ty đang làm (`current_company_role`, `TpEmployee::getCurrentCompanyRoleAttribute`) đọc `employee_infos.company_role`
mỗi request ⇒ DÙNG CHUNG mọi tab / thiết bị của tài khoản. Đổi công ty ở topbar (`BasicSubsystem.vue` → `saveCompanyId`
→ `POST human/employee-infos/{id}/update-company-role`) chỉ tải lại tab đang bấm. Tab khác vẫn hiện công ty cũ nhưng
request chạy theo công ty mới ⇒ ghi nhầm công ty.

Lộ ra ở Cập nhật giá bán (prod): TPE sửa giá mã SGCB-SGGC032 (TPE quản lý) bị "Không được thấp hơn giá Đại lý cấp 1 của
TPE (300,300)" — BE coi là công ty lấy về vì tài khoản đã đổi công ty ở tab khác. Giá ≥ sàn thì GHI THẲNG vào công ty kia.

Quyết định (user 27/10): 1 tài khoản = 1 công ty tại 1 thời điểm; lệch là lỗ hổng, KHÔNG làm "mỗi tab 1 công ty".

## Cơ chế

1. FE gửi `X-Company-Id` = `store.state.current_company` (nạp 1 lần lúc tải trang) ở MỌI request `$axios` tới API của mình.
2. BE middleware `EnsureSameCompany` (nhóm `api`): header lệch `current_company_role` ⇒ 409 `company_changed: true`, không
   chạy controller. Bỏ qua: không header (app mobile, client cũ, `import axios` thô, link tải file), `users/auth/*`,
   `master-settings*`, API đổi công ty.
3. FE nhận 409 `company_changed` ⇒ popup không đóng được, chỉ nút "Tải lại trang".
4. Đổi công ty ⇒ báo các tab khác qua sự kiện `storage` (localStorage) ⇒ hiện ngay popup ở bước 3.

## Task

### BE
- [x] `app/Http/Middleware/EnsureSameCompany.php` + đăng ký nhóm `api` trong `app/Http/Kernel.php`
- [x] Test `tests/Feature/EnsureSameCompanyTest.php`: khớp / lệch (GET + POST) / không header / API đổi công ty / chưa đăng nhập

### FE
- [x] `plugins/company-guard.js` (client): gắn header, bắt 409, nghe `storage`
- [x] `components/modal/CompanyChangedModal.vue` dựng trên `V2BaseModal`, không đóng được
- [x] `BasicSubsystem.vue` `saveCompanyId`: phát tín hiệu cho tab khác + không tự bật popup ở chính tab đang đổi
- [x] `plugins/api-error-guard.js`: 409 `company_changed` không toast trùng

### Commit
- [x] Commit + push `gop_db`: hrm-api `bf24b5f5b`, hrm-client `4eb26ea7d` (user yêu cầu 27/10)

### Kiểm
- [x] Playwright MCP 2 tab: đổi công ty tab 2 ⇒ tab 1 hiện popup ngay; lưu giá tab 1 ⇒ 409, DB giá không đổi
- [x] Màn có polling (meeting) không bật popup sai khi chưa đổi công ty
- [x] Spec e2e mới (không tự chạy cả bộ — chỉ chạy khi user yêu cầu)

## Ngoài luồng (note lại, chưa sửa)
- `update-company-role` nhận `{employeeInfo}` bất kỳ, không kiểm là của chính user, không kiểm user có quyền ở công ty đó
  ⇒ user A đổi được công ty đang làm của user B / tự chọn công ty không được gán.

### Checkpoint — 27/10/2026
Vừa hoàn thành: BE middleware + 5 test (xanh) · FE plugin/popup/BasicSubsystem · Playwright MCP 2 tab: lưu giá tab cũ ⇒ 409,
popup z20000 không đóng được (Esc/nền/$bvModal.hide), 0 toast, DB giá 0 đổi; tín hiệu storage khác công ty ⇒ popup ngay
0 request, cùng công ty ⇒ không; meeting polling 25s 0 popup; domain ngoài không header. OwnerPriceFloorApiTest 8/8 xanh.
Spec e2e `HRM/e2e/tests/shared/company-switch-guard.spec.ts` (G1–G4) đã viết, tsc sạch.
Đang làm dở: —
Bước tiếp theo: user review; deploy cả 2 repo cùng lúc.
Blocked:
Ghi chú local: API đổi công ty trả 500 ở local (`findRiceCompany` → kết nối `mysql_tpe` chưa cấu hình) dù đã ghi company_role.

### Checkpoint — 27/10/2026 (chạy e2e)
Vừa hoàn thành: e2e company-switch-guard 4/4 xanh, chạy 2 lượt liên tiếp (G1 chặn ghi · G2 tải lại · G3 đổi công ty THẬT qua
topbar · G4 domain ngoài). Phát hiện + sửa khi chạy: hàm Lưu của màn tự toast câu 409 đè popup ⇒ `company-guard.js` tắt mọi
toast khi popup đã bật (`muteToastsWhenCompanyChanged`). Cấu hình local: thêm `DB_*_TPE` vào `hrm-api/.env` (trỏ DB gộp) ⇒
API đổi công ty hết 500. Nuxt dev local: mở 3 tab là tab tải lại treo ⇒ spec giữ tối đa 2 tab.
Đang làm dở: —
Bước tiếp theo: user review; deploy 2 repo cùng lúc (FE cần restart Nuxt vì đổi nuxt.config).
Blocked:

### Checkpoint — 27/10/2026 (wrap up)
Vừa hoàn thành: commit + push `gop_db` cả 2 repo (hrm-api `bf24b5f5b`, hrm-client `4eb26ea7d`); design.md + spec chi tiết.
Đang làm dở: —
Bước tiếp theo: deploy prod 2 repo cùng lúc + restart Nuxt. Chờ user quyết có làm lỗ hổng `update-company-role` (mục Ngoài luồng).
Blocked:
