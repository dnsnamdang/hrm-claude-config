# Plan — TPE_APP kiểm quyền theo mã (`permission_codes`) thay tên cũ

> Lập 03/11/2026. Căn cứ: `danh-gia-anh-huong.md` (cùng thư mục). **Chưa code** — mỗi bước đụng source phải xin "làm" riêng
> (repo TPE_APP · nhánh · file). Hỏi nhánh trước khi sửa (develop ↔ tpe liên thông; duclocson, thanhan độc lập).

## Mục tiêu

App đọc `permission_codes` `{mã: phạm vi 1..4 | null}` (đã có trong phản hồi login + user-profile của hrm-api `gop_db`) để
kiểm quyền, **lùi về tên cũ** khi backend chưa có trường này (backend khách hàng khác chưa deploy `rbac`). Sau khi bản app mới
phủ hết người dùng TPE mới được gỡ tên cũ / `permission_aliases` ở server.

## Thiết kế

- **Model:** thêm `permissionCodes: Map<String, int?>` vào `RemoteEmployeeInfoData` / `EmployeeInfo` (domain),
  `LoginResponse`, decoder `getProfile()` (`user_api_service_profile_ext.dart`: đọc `json['permission_codes']` cạnh
  `json['permissions']`). Map rỗng ⇔ backend cũ. Lưu kèm `currentUser` trong `AppPreferences` như `permissions`.
- **Một cửa kiểm quyền** `AppPermission` (vị trí theo skill `app-*`, hỏi trước nếu đặt ở `utils/`/`custom_view/` vì là dùng chung):
  - `can(code, {legacy})` — có mã (bất kỳ phạm vi) ⇒ true; `permissionCodes` rỗng ⇒ so `legacy` (tên cũ) như hiện tại.
  - `scope(code, {legacyByScope})` — trả 1..4 | null; backend cũ ⇒ suy từ tên cũ theo phạm vi cao nhất.
  - Bảng hằng mã đặt 1 chỗ, mỗi mã kèm tên cũ để lùi.
- **Thay 9 file gọi** (đủ theo `danh-gia-anh-huong.md` mục 2):

| File | Đang so tên | Đổi sang |
|---|---|---|
| `ui/module_shell/module_menus.dart` | `PD-…` ×4, `XN-…`, `Quản lý phiếu đi công tác`, chuỗi con `giao công tác` / `Quản lý phiếu giao việc` / `Duyệt đề nghị thanh toán công tác phí` | `can('timesheet.don_xin_nghi.approve')`… ; `giao công tác` ⇒ `can(assign.danh_sach_phieu_giao_cong_tac.view) || can(assign.phieu_giao_cong_tac.approve)`; `assign.phieu_giao_viec.manage`; mục thanh toán CTP: giữ theo tên (chỉ Thành An) |
| `ui/dashboard_nhan_vien/dashboard_nhan_vien_page.dart` | như trên + `Dashboad quản lý` | như trên + `timesheet.dashboard_quan_ly.view` |
| `ui/dashboard_nhan_vien/bloc/dashboard_nhan_vien_bloc.dart`, `…_state.dart` | `Dashboad quản lý`, `PD-…` | như trên |
| `domain/.../entity/employee_info.dart` | `hasPermission` getter (PD-…, `giao công tác`) | như trên |
| `ui/ds_phieu_giao_cong_tac/bloc/ds_phieu_giao_cong_tac_state.dart` | 4 tên "Xem danh sách phiếu giao công tác theo …" | `scope('assign.danh_sach_phieu_giao_cong_tac.view')` ≥ 4/3/2/1 |
| `custom_view/filter_org_scope.dart` (+ 3 nơi gọi: meeting list filter, work issue, work task) | `OrgScopePermissions.of('meeting'/'issue'/'task')` | nhận mã `meeting.danh_sach_meeting.view` / `assign.danh_sach_issue.view` / `assign.danh_sach_task.view`, so phạm vi; lấy quyền từ `currentUser` thay vì `ApiUserProfileData.permissions` của static-data |
| `ui/quan_ly_dk_com/long_term_rice/long_term_rice_registration.dart` | 3 tên suất ăn | `scope('rice.phieu_dang_ky_suat_an.view')` ≥ 4/3/2 |

- **Giữ nguyên theo tên** (chỉ bản Thành An, backend riêng, không có mã ở backend TPE): `PD-Đăng ký tăng ca`, `Duyệt đề nghị thanh toán công tác phí`.

## Thứ tự triển khai

1. Code + test trên `develop` (TPE). Unit test `AppPermission`: có mã / không mã / map rỗng lùi tên cũ / phạm vi cộng dồn.
2. Kiểm simulator như `danh-gia-anh-huong.md` mục 4 (NV 36 không có khối duyệt, NV 34 có đủ) trên **2 backend**: rehearsal
   (có `permission_codes`) và backend chưa `rbac` (lùi tên cũ).
3. Phát hành bản app; theo dõi tỉ lệ máy đã cập nhật (cơ chế bắt buộc cập nhật — Q2).
4. Chỉ sau khi bản cũ hết dùng: server được gỡ tên cũ khỏi `permissions` / gỡ `permission_aliases` guard api cho app.

## Quyết định đã chốt (03/11/2026)

- **Q1 — đóng.** Mục "Duyệt đề nghị thanh toán công tác phí" chỉ thuộc bản Thành An (`env.isThanhAnGroup`, backend riêng;
  hrm-api TPE không có API `working-fee`) ⇒ giữ kiểm theo tên, không đổi.
- **Q2 — đo qua `fcm_tokens`.** Không thêm cơ chế bắt buộc cập nhật. Trước khi gỡ tên cũ ở server: đếm `fcm_tokens.device_info`
  trên prod (ghi `ios|android - <phiên bản>(<build>)` từng máy; dump prod 21/10: `2.3.5(99)` 683 dòng, `2.3.4(98)` 32 dòng) —
  chỉ gỡ khi số máy còn bản chưa đọc `permission_codes` đạt ngưỡng user chốt lúc đó. Server giữ tên cũ tới lúc ấy.
- **Q3 — `develop` rồi đồng bộ `tpe`.** Làm trên `develop`, đồng bộ sang `tpe` như thường lệ (03/11 hai nhánh cùng `e317e11`).
  Nhờ lùi về tên cũ khi không có `permission_codes`, app các khách hàng `tpe` (etek, etekPower, Kasaco, Toyota Sông Lam, ZITEC,
  ORI) không đổi hành vi ⇒ trước phát hành phải thử thêm 1 backend chưa `rbac`. Lưu ý: checkout local `develop` đang ở
  `3b57558`, sau `origin/develop` — pull trước khi code.
