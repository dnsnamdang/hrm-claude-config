# Plan — Fix vòng lặp SSO HRM ↔ ERP

Phụ trách: @namdangit

## Bối cảnh
Đăng nhập từ `HRM/login?redirect_page=<ERP>` bị load đi load lại, không vào được ERP; chỉ hết khi xoá session/cookies. Nguyên nhân: `nuxtClientInit` tự động bắn token đang lưu sang ERP mỗi khi có `redirect_page`, không có bộ ngắt vòng lặp; ERP từ chối → bật ngược → HRM lại bắn → loop vô tận. Các catch lỗi SSO của ERP nuốt exception (không log) nên không thấy lý do từ chối.

## Phase 1 — Loop-breaker phía HRM + bật log ERP

### FE (hrm-client)
- [x] `store/actions.js` `nuxtClientInit`: thêm guard chống auto-redirect lặp — ghi dấu (sessionStorage) redirect_page + thời điểm lần auto-redirect gần nhất; nếu sắp bắn lại đúng redirect_page đó trong < ngưỡng giây (vừa bị bật về) → coi như ERP từ chối token → xoá `access_token`, xoá dấu, KHÔNG redirect (để form login hiện ra)
- [x] Xoá dấu guard sau khi auto-redirect thành công 1 lần (để lần SSO hợp lệ sau không bị chặn nhầm)

### BE (ERP - TanPhatDev)
- [x] `SSOController::callback` + `ssoLogout`: log lý do khi không có/không hợp lệ token
- [x] `Auth/LoginController::showLoginForm`: bật lại `Log::error($e)` trong catch (đang bị comment)
- [x] `CheckSSOTokenMiddleware`: log khi redirect về HRM (thiếu token / không tìm thấy user / exception)

## Checkpoint
### Checkpoint — 2026-06-17
Vừa hoàn thành: Phân tích root-cause + chốt hướng fix (Option A) + implement loop-breaker HRM + bật log ERP
Đang làm dở: (trống)
Bước tiếp theo: User test lại luồng SSO; nếu vẫn lặp, đọc log ERP mới để biết lý do ERP từ chối token
Blocked:
