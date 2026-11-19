# Ảnh hưởng của phân quyền mới (GĐ1 → GĐ3b) tới app mobile TPE_APP

> Đánh giá 03/11/2026 trên: TPE_APP nhánh `develop` (`3b57558`, App 2.2.6+153) · hrm-api `gop_db` local `7a466818b`
> (đã gồm `rbac` + GĐ3b) · DB `hrm_erp_rbac_rehearsal` (bản prod đã chạy `rbac:convert` + cấp mã GĐ3b) · dump `hrm_erp_21_10_prod`.

## Kết luận

**App KHÔNG phải sửa code để chạy với phân quyền mới.** Server giữ tương thích ngược: `permissions[].name` vẫn là **tên quyền
cũ**. Có vài thay đổi hành vi (mục 3) và 1 rủi ro dài hạn (mục 5) — kế hoạch xử lý ở `plan-chuyen-sang-ma.md`.

## 1. App đọc quyền thế nào

- Nguồn: `permissions[]` trong phản hồi `POST v1/users/auth/login` và `GET v1/users/auth/user-profile`
  (`user_api_service_profile_ext.dart:12`, `user_repository_impl.dart:178`), cộng `employee_info.permissions`.
- App so **tên tiếng Việt**: `permissions.map((e) => e.name).contains('<tên>')`, `ApiUserProfileData.hasPermission(name)`
  (so bằng `==`) và 3 chỗ so **chuỗi con** `containsIgnoreCase(...)`.
- Meeting đọc thêm `v1/assign/customers/my-permissions` (cờ do server tính — hình dạng không đổi).
- App KHÔNG đọc `roles` để kiểm quyền; không có chỗ đổi công ty đang làm.

## 2. Server sau đổi vẫn trả tên cũ

- `AuthNewController::userProfile()` / `buildLoginResponse()` → `CurrentPermission::listFor(nhân viên, công ty đang làm)`:
  từ các mã người dùng có ở công ty đang làm, tra ngược `permission_aliases` (guard `api`) ra tên cũ. Comment
  `AuthNewController.php:406-408` ghi rõ app TPE_APP so `permissions[].name` nên `name` PHẢI là tên cũ.
- Thêm trường `permission_codes` `{mã: phạm vi|null}` — app chưa đọc, json_serializable bỏ qua.
- Tên cũ có phạm vi: `PermissionChecker::legacyNames()` trả mọi tên có `min_scope ≤ phạm vi đang có` (**cộng dồn**).

### Đối chiếu 31 tên + 3 chuỗi con app dùng (rehearsal)

| Tên app dùng | Mã | Ghi chú |
|---|---|---|
| `PD-Đơn xin nghỉ` | `timesheet.don_xin_nghi.approve` | |
| `PD-Đăng ký đi muộn về sớm` | `timesheet.dang_ky_di_muon_ve_som.approve` | |
| `PD-Đăng ký làm thêm` | `timesheet.dang_ky_lam_them.approve` | |
| `PD-Đăng ký tăng ca` | — | chỉ bản Thành An (backend riêng); không có ở DB TPE kể cả trước đổi |
| `PD-Đề nghị tra soát công` / `XN-…` | `timesheet.de_nghi_tra_soat_cong.approve` / `.confirm` | |
| `Dashboad quản lý` (sai chính tả, giữ nguyên) | `timesheet.dashboard_quan_ly.view` | |
| `Quản lý phiếu đi công tác` | `assign.phieu_di_cong_tac.manage` | |
| `Xem danh sách phiếu giao công tác theo {tổng công ty/công ty/phòng ban/bộ phận}` | `assign.danh_sach_phieu_giao_cong_tac.view` @4/3/2/1 | |
| `Xem danh sách {meeting/issue/task} theo …` (ghép động `OrgScopePermissions.of`) | `meeting.danh_sach_meeting.view`, `assign.danh_sach_issue.view`, `assign.danh_sach_task.view` @4/3/2/1 | |
| `Xem phiếu đăng ký suất ăn theo {tổng công ty/công ty/phòng ban}` | `rice.phieu_dang_ky_suat_an.view` @4/3/2 | |
| chuỗi con `giao công tác` | khớp 5 tên (4 tên danh sách + `Trưởng phòng duyệt phiếu giao công tác` = `assign.phieu_giao_cong_tac.approve`) | |
| chuỗi con `Quản lý phiếu giao việc` | `assign.phieu_giao_viec.manage` | |
| chuỗi con `Duyệt đề nghị thanh toán công tác phí` | — | chỉ bản Thành An (`env.isThanhAnGroup`, backend riêng); hrm-api TPE không có API `working-fee` ⇒ đúng thiết kế, không phải lỗi |

⇒ 29/31 tên + 2/3 chuỗi con tra ra mã; 2 chỗ còn lại chỉ dùng cho bản Thành An (backend riêng) — không liên quan backend TPE.

## 3. Thay đổi hành vi người dùng app sẽ thấy

1. **Phạm vi cộng dồn** — có "theo công ty" thì server trả thêm "theo phòng ban/bộ phận". Số NV TPE có tên phạm vi thấp tăng
   (vd "meeting theo bộ phận" 11 → 43, "suất ăn theo công ty" 18 → 36). App luôn xét mức cao nhất trước
   (`filter_org_scope.dart:42-60`, `long_term_rice_registration.dart:58-61`) ⇒ giao diện không đổi; dữ liệu do server lọc theo mã.
2. **Quyền theo công ty đang làm** (`company_role`, chọn trên web, lưu DB) — app không có chỗ đổi công ty ⇒ đổi công ty trên web
   thì menu app đổi ở lần tải hồ sơ sau. Rehearsal: 0 NV hoạt động thiếu dòng `company_employees` ở công ty đang làm (không ai
   bị mất trắng quyền); 1 NV đang làm khác công ty hồ sơ — ô lọc tổ chức của app lọc phòng ban theo `currentUser.companyId`
   (công ty hồ sơ) trong khi quyền tính theo công ty đang làm ⇒ lệch nhẹ.
3. **GĐ2c tắt phạm vi Tổng công ty cho 6 công ty ≠ TPE** — NV các công ty đó mất tên "… theo tổng công ty" ⇒ mất ô lọc toàn tập
   đoàn trên app (đúng chủ đích). NV TPE không đổi.
4. **Dữ liệu server trả theo mã, app thấy y như web** — đặt phòng họp phạm vi Công ty thấy thêm phiếu đặt PHÒNG thuộc công ty
   (GĐ3b 1b); xoá khách hàng theo phạm vi mã F12; người nhận thông báo/push tính theo mã + công ty.

### Số NV TPE (công ty 1) có từng tên — trước (dump 21/10) → sau (rehearsal)

Phần lớn bằng hoặc tăng (do cộng dồn). Lệch ±1 người (vd NV 50 mất, NV 787/1084/196/256 thêm) truy ra là **2 bản chụp DB khác
nhau** (dump 21/10 có vai trò tạm local "TẠM local - FULL quyền (NV 50)"; rehearsal là dump prod mới hơn, vai trò
`TPE_Super Admin` công ty 1 mang quyền tra soát) — **chưa so được trên cùng 1 bản chụp**; cổng đối chiếu đầy đủ là báo cáo
chênh lệch của `rbac:convert --dry-run` lúc diễn tập.

## 4. Kiểm thử app thật trên rehearsal (03/11/2026)

- hrm-api `gop_db` chạy `php -S 127.0.0.1:8002` với DB rehearsal; app bản `tpeLocal` (`com.tanphat.app`) trên máy ảo iPhone 18 Pro,
  `--dart-define=APP_API_BASE_URL=http://127.0.0.1:8002/api/` (`--use-application-binary` ⇒ phải hot restart mới ăn define).
- 3 tài khoản đặt mật khẩu tạm (user cho phép), xong **trả lại** hash cũ + `login_count` + `password_changed_at`; dòng
  `fcm_tokens` app tạo đã tự xoá khi đăng xuất. Bảng rehearsal bị ghi trong lúc thử: chỉ `employees`, `fcm_tokens` — đều đã trả.

| Tài khoản | Tên app-liên quan server trả (login) | Đo trên app | Kết quả |
|---|---|---|---|
| NV 36 Nguyễn Trung Phong (Giám đốc, 1 công ty) | 294 tên; không có `PD-`/`XN-`/`Dashboad`; có meeting/issue @4..1 | Đơn từ: chỉ khối "ĐƠN CỦA TÔI" 4 mục; menu trái không có khối duyệt | ĐẠT |
| NV 34 Đào Thị Thúy (6 công ty, đang làm công ty 1) | 890 tên; đủ 4 `PD-` + `XN-` + `Dashboad quản lý` + giao việc/công tác | Đơn từ: "ĐƠN CỦA TÔI" 4 mục + "PHÊ DUYỆT" 4 mục; mở "Duyệt đơn xin nghỉ" ra 10 đơn, không 403 | ĐẠT |
| NV 4589 (e2e) | 677 tên, cùng bộ tên app-liên quan như NV 34 (trừ task) | không đo UI (trùng ca NV 34) | — |

## 5. Rủi ro dài hạn

App phụ thuộc hoàn toàn vào việc server còn trả **tên cũ** (kể cả tên sai chính tả `Dashboad quản lý`). Code server ghi kiểm theo
tên cũ là tạm (`CurrentPermission::has` "tạm, gỡ ở Task 12"). Gỡ `permission_aliases` hoặc đổi tên quyền mà app chưa đọc
`permission_codes` ⇒ app **ẩn menu im lặng**. ⇒ Chuyển app sang mã TRƯỚC khi gỡ tên cũ: `plan-chuyen-sang-ma.md`.

## 6. Phạm vi bản app

Chỉ bản trỏ backend TPE: `tpeProd` (hrm.eteksofts.com), `tpeDev` (dev-hrm), `tpeLocal`. Các bản etek / etekPower / etekGreen /
Thành An / Đức Lộc Sơn / Kasaco… chạy backend riêng — không ảnh hưởng tới khi backend đó deploy `rbac`.
