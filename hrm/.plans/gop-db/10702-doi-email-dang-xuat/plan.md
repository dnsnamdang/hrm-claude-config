# #10702 — [App + Web Đăng nhập] Đổi email công ty không đăng xuất phiên đang dùng email cũ — @cuong61n (Redmine đang giao Trần Cư)

Cơ chế sẵn có: JWT mang `token_version`; middleware `Authenticate` so với DB, lệch → 401 (app: code 401 = tokenExpired → hộp thoại "Phiên đăng nhập đã hết hạn" → về Đăng nhập; web → /login). Trước đây chỉ tăng khi ĐỔI MẬT KHẨU.
Đường đổi email thật: web Hồ sơ nhân sự (EmployeeInfoForm, ô "Email công ty") → `EmployeeInfo` hook `updated` ghi `Employee::save()` email mới (form Tài khoản khoá ô email).

## Phase 1 — BE
- [x] `Modules/Human/Entities/Employee::boot` `updating`: email đổi (không phân biệt hoa thường) và chưa tăng sẵn (đổi mật khẩu cùng lúc) → `token_version + 1`. Gom mọi đường (hook hồ sơ + form tài khoản)
- [x] Câu 401 trong `Authenticate`: "…do email hoặc mật khẩu đăng nhập vừa được thay đổi…" (trước chỉ nói mật khẩu)
## Phase 2 — App
- [x] `_onTokenExpiredError`: `replaceAll([LoginRoute])` thay `replace` — trước để lại các màn của phiên cũ dưới màn Đăng nhập
## Test (local 19/10/2026, TK 305, đã trả nguyên trạng)
- [x] Web: admin đổi Email công ty ở Hồ sơ → token_version 1→2; phiên web 305 tải lại → /login ✓; token API cũ → 401 câu mới ✓; email cũ không đăng nhập được, email mới được ✓
- [x] App: 305 đang ở dashboard → mở màn có gọi API → "Phiên đăng nhập đã hết hạn" → Ok → màn Đăng nhập, ngăn xếp sạch ✓
- [x] Lưu hồ sơ KHÔNG đổi email → token_version giữ nguyên ✓
- Lưu ý: app chỉ đá khi màn gọi API có xử lý lỗi chung (dashboard nuốt lỗi 401 nên đứng yên tới lần bấm kế tiếp); TokenInterceptor của app đang tắt
## Test hồi quy luồng đăng nhập (user yêu cầu, 19/10/2026)
- [x] Model (transaction + rollback) 7/7: đổi email +1; chỉ đổi hoa/thường/khoảng trắng 0; lưu không đổi email 0; đổi email + mật khẩu cùng lúc +1; hồ sơ đổi email → tài khoản theo + +1; hồ sơ lưu không đổi email 0; tạo mới = mặc định 1
- [x] HTTP 16/16: login đúng/sai/email hoa+khoảng trắng, user-profile, refresh, tự đổi mật khẩu (token cũ 401, token mới OK, mk cũ chặn, mk mới vào), logout
- [x] EmployeeService::updateEmployee (form Tài khoản) 5/5: đổi mk +1, lưu không đổi 0, đổi email +1, đổi email+mk +1 (không tăng 2 lần)
- [x] Web Playwright: đăng nhập admin + NV thường OK; đổi email ở Hồ sơ → phiên NV về /login. App: đăng nhập admin OK, bị đá → màn Đăng nhập sạch ngăn xếp
- Ghi chú: form Tài khoản của TK 305 trên local không lưu được do `rice_ssn` trùng (dữ liệu, có sẵn) → test luồng này bằng service. Chưa test luồng Quên mật khẩu (cần mã gửi email) — code chỉ đổi mật khẩu, không đổi email nên hook không tác động
