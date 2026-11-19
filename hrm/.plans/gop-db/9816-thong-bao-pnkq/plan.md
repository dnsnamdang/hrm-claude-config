# #9816 — [APP CSKH] Phiếu nhập kết quả: Không duyệt / Duyệt không có thông báo về app — @cuong61n

Nguyên nhân: duyệt/không duyệt làm ở ERP (`WrApproveResultsController`). ERP chỉ ghi thông báo kiểu `App\Employee` (app đọc `EmployeeInfo`) và không có FCM; nhánh duyệt không báo người nhập; app chưa xử lý loại thông báo này.
User chốt 19/10/2026: hướng (a) — ERP gọi HRM, HRM gửi thông báo + push (dùng chung EmployeeInfoService::sendNotification).

## Phase 1 — HRM (hrm-api)
- [x] `POST v1/assign/wr_import_results/{id}/notify-result` {status: approved|rejected, reason?} (auth:api) — người nhận = người tạo phiếu (employees.id → employee_info_id), nội dung `buildNotificationContent('PNKQ', 'Đã duyệt'|'Từ chối', mã phiếu, 'Lý do: …')`, type `wrImportResult`, url `/assign/assign_import_result/{id}`
## Phase 2 — ERP (TanPhatDev, gop_db)
- [x] `notifyHrmImportResult()` gọi HRM bằng JWT SSO (cookie/session `jwt_token`), timeout 5s, lỗi chỉ log
- [x] `unApprove`: sau commit báo "Từ chối" + lý do (approve_comment)
- [x] `store` / `update`: sau commit báo "Đã duyệt" khi phiếu LẦN ĐẦU chuyển sang DA_DUYET_KET_QUA (tránh báo 2 lần chờ hạch toán → đã hạch toán)
## Phase 3 — App
- [x] case `wrImportResult` ở notification_bloc, app_bloc (bấm push), new_notification_view_model → `NhapKetQuaCongViecMainRoute(viewOnly)`
## Test (local 19/10/2026)
- [x] API: 7047 rejected → notifications EmployeeInfo 487 "[PNKQ] Từ chối: <b>TPE.PNKQ.2026007047</b>. Lý do: …" ✓; status sai → 422 ✓
- [x] ERP→HRM: gọi notifyHrmImportResult(7010, rejected) bằng token SSO → HRM ghi thông báo cho admin ✓ (thiếu token → log cảnh báo, không lỗi)
- [x] App: Thông báo hiện dòng mới (mã in đậm) → bấm mở chi tiết PNKQ 7010 ✓
- Chưa test: push FCM thật lên điện thoại (simulator không nhận FCM); bấm Duyệt/Không duyệt trên giao diện ERP (test qua hàm helper)
