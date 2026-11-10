# [Công việc] Thông báo: bổ sung thông báo khi có phiếu đề xuất công việc / đề xuất công tác chờ duyệt (#12093) — @cuong61n

Redmine #12093 (Nguyễn Huyền giao 10/11/2026, Web App). Nhận thông báo: tài khoản có quyền + xét phạm vi quản lý phòng ban. Nội dung theo `notification-convention`.

## Hiện trạng (rà 10/11)
- Đề xuất công việc (`JobRequestController`, prefix `PDX`): `store` đã bắn "Chờ duyệt"; `update` kiểm nhầm `$request->status` (FE gửi lại `status` CŨ của phiếu) → sửa nháp rồi Gửi duyệt KHÔNG bắn; bấm Duyệt thì lại bắn "Chờ duyệt" cho người duyệt và không báo "Đã duyệt" cho người tạo.
- Người nhận "Chờ duyệt" đang chọn theo phòng THỰC HIỆN, trong khi `canApprove()` cho người quản lý phòng ĐỀ XUẤT duyệt → gửi nhầm người.
- Duyệt xong (Chờ giao việc) chưa báo ai cho "Trưởng phòng giao đi công tác" (`assign.phieu_giao_cong_tac.create`).
- Đề xuất công tác (`AssignRequestController`): đã bắn "Chờ duyệt" khi gửi duyệt cho người có `assign.phieu_de_xuat_di_cong_tac.manage` (cùng quyền màn "chờ duyệt" đang lọc) — đúng; nhưng dùng prefix `PCT` (= "Phiếu công tác") thay vì `PDXCT` (= "Đề xuất công tác", đã khai nhãn + icon web/app).

## Hướng làm đã chốt (tự quyết theo task)
- [x] 10/11 `JobRequestController::update` dùng `status_request` (như `store`) cho nhánh Chờ duyệt / Đã duyệt.
- [x] 10/11 "Chờ duyệt" gửi người có `assign.phieu_de_xuat_cong_viec.approve` quản lý phòng ĐỀ XUẤT (khớp `canApprove`), link `/assign/job_requests/{id}/approve`.
- [x] 10/11 Duyệt xong → thêm "Chờ xử lý" cho người có `assign.phieu_giao_cong_tac.create` quản lý phòng THỰC HIỆN (khớp `canAssign`), link `/assign/job_requests/{id}/show`.
- [x] 10/11 `AssignRequestController`: đổi prefix `PCT` → `PDXCT`.
- [x] 10/11 Gom 2 hàm gửi dùng chung cho `store` + `update` (hết nhân đôi code).
- App: type `job_request` / `assign_request` chưa có màn trên app → thông báo vẫn hiện ở màn Thông báo, bấm báo "xem trên web" (chưa làm màn app).
- Ngoài phạm vi, ghi lại: `AssignJobController` có cùng kiểu kiểm `$request->status == 2` (cần xác nhận là `update` rồi sửa).

## Kiểm
- [x] 10/11 `php -l` 2 controller sạch; tinker (DB local, phiếu id 486, phòng đề xuất 111 / thực hiện 51): người duyệt = 6 tài khoản, người giao đi công tác = 13 tài khoản — hàm chọn người nhận chạy đúng, không lỗi.
- [x] 10/11 Test tích hợp gọi route thật qua 1 process + rollback (script scratchpad `t12093.php`, JWT nhiều tài khoản: người tạo / trưởng phòng duyệt / người chỉ có quyền giao / người không quyền), DB local, 0 dữ liệu còn lại. Kết quả:
  - Đề xuất công việc, lưu nháp → 0 thông báo (đúng).
  - Sửa nháp rồi Gửi duyệt (form gửi `status` cũ = 1, đúng như FE) → "Chờ duyệt" tới đúng 6 người duyệt phòng đề xuất, link `/approve`, người tạo không nhận. (Trước sửa: 0 thông báo.)
  - Người chỉ có quyền giao thử duyệt → 403, 0 thông báo; người không quyền thử duyệt → 403.
  - Trưởng phòng duyệt (form gửi `status` cũ = 2) → phiếu sang status 3; người tạo nhận "Đã duyệt"; 13 người có quyền giao đi công tác (phòng thực hiện) nhận "Chờ xử lý"; KHÔNG bắn lại "Chờ duyệt". (Trước sửa: bắn nhầm "Chờ duyệt", người tạo không được báo.)
  - Tạo mới + gửi duyệt luôn → 6 người duyệt; Từ chối → người tạo nhận "Từ chối".
  - Đề xuất công tác: tạo nháp → 0; sửa + gửi duyệt và tạo mới + gửi duyệt → 13 người có quyền `.manage`, prefix `PDXCT`, link `/assign/assign_requests/{id}`.
- Lưu ý khi viết test: controller đề xuất công việc trả 423 (cảnh báo đã đăng ký cơm) ngay trong transaction mà không rollback → phải truyền `is_confirm_reject_rice` khi test, và rollback tới mức 0 (đã dọn phiếu thử sót).
- [x] 10/11 Test PHẠM VI người nhận (script `t12093b.php`): 87 tài khoản giữ ≥1 trong 3 quyền + 12 NV không quyền; mỗi người gọi API thật bằng JWT riêng để xem THỰC SỰ làm được việc không (`canApprove` / `canAssign` / thấy phiếu ở tab Chờ duyệt), rồi so với danh sách được báo. 5 cặp phòng, 3 công ty (111→51, 95→50, 5→95 cty 1; 132→138 cty 9; 120→121 cty 8):
  - "Chờ duyệt" đề xuất công việc: khớp 100% ở cả 5 cặp (6 / 12 / 8 / 1 / 2 người) — không lọt sang phòng/công ty khác, không sót trưởng phòng nào.
  - "Chờ xử lý" (giao đi công tác): khớp 100% ở 3/5 cặp; 2 cặp còn lại lệch 1 người (Trịnh Thị Lợi): quản lý phòng 51/50 ở công ty 1 nhưng phiên đăng nhập hiện đang ở công ty 8 nên `manager_departments` rỗng → chưa bấm giao được cho tới khi đổi công ty. Thông báo vẫn đúng (cô ấy có quyền thật), giữ nguyên.
  - Phát hiện + sửa: danh sách người nhận có cả tài khoản NGHỈ VIỆC (`employees.status = 0`, ví dụ info 224, 1630) → thêm lọc `activeInfoIds()` ở cả 2 controller.
  - Đề xuất công tác: người nhận = người có `.manage` quản lý đúng phòng của phiếu (gồm cả người tích "Quản lý tất cả phòng ban" của công ty đó); đổi lấy phòng theo `$result->department_id` của phiếu (trước lấy theo phòng người đang thao tác / `$request->employee_info_id` do client gửi). Cố ý HẸP hơn tab "Chờ duyệt" (tab hiện cho ~20 người có quyền xem rộng, kể cả công ty khác) — thông báo chỉ gửi trưởng phòng/bộ phận tương ứng theo yêu cầu task.
- [ ] Chưa soi giao diện chuông web bằng trình duyệt (chỉ kiểm bản ghi thông báo + người nhận ở DB).

## Trạng thái
Đã deploy PROD 10/11/2026: commit `a0d21be27` (develop) / `93fb0c2a6` (cherry-pick sang `gop_db`, nhánh prod đang pull) đã push; trên VPS prod `git pull` fast-forward + `queue:restart`, `php -l` sạch. `build_tpe.sh` dừng ở bước migrate vì hỏi xác nhận (không có tty) — bỏ qua được vì thay đổi này không có migration / route / quyền mới.
