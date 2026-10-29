# #10079 — [App] Kiểm tra trước khi tạo phiếu gia hạn / kết thúc sớm cho phiếu công tác — @cuong61n

Spec: Google Sheet "Kiểm tra tạo GHKTS(Giao việc)" — DS phiếu giao công tác, trước khi vào form gọi `GET assign/extend-end-soon-request/check?assign_business_id&type` (1 gia hạn, 2 kết thúc sớm); `can_create=false` → hiện `message`, không vào form.

Hiện trạng 19/10/2026: ĐÃ LÀM — BE `ExtendEndSoonRequestController::checkPending` (route Modules/Assign/Routes/ExtendEndSoonRequest/api.php); app `onsite_work_item_view.dart::_checkAndOpenForm` (TuJobs 31/03/2026) + form tạo cũng check lại.
- [x] Bổ sung: bọc try/catch lời gọi check — trước đây lỗi mạng/server thì bấm không phản hồi gì; nay báo lỗi bằng snackbar
- [x] Test simulator (dựng tạm PCT-TEST-KC đang hiệu lực + admin trong DS nhân viên + 1 phiếu gia hạn chờ duyệt, đã trả lại): Gia hạn → "Phiếu công tác này đã có phiếu gia hạn "GHKTS-TEST10079" đang chờ duyệt…", không vào form ✓; Kết thúc sớm → check type=2 → mở form "Tạo gia hạn, kết thúc sớm" ✓; test lại sau khi thêm try/catch ✓
