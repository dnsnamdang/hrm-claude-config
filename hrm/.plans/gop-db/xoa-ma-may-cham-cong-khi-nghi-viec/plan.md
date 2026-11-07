# Nghỉ việc thì xoá mã trên máy chấm công khuôn mặt + máy cơm — @cuong61n

> Nguồn: phản ánh trên cổng chính TPE 07/11/2026 — 3 nhân sự nghỉ ở Công ty Đầu tư Tập đoàn ETEK (company 8) từ 02/11,
> chuyển về TPE (company 1) với mã mới; trên máy còn 2 hồ sơ cùng 1 khuôn mặt nên chấm không lên bảng công.
> Nhánh: `feat/xoa-ma-may-khi-nghi-viec` (hrm-api, checkout từ `origin/gop_db` 05a0eca9b), worktree `HRM/worktrees/face-leave-api`.

## Phase 1 — Xử lý sự cố trên PROD (07/11/2026)

- [x] Điều tra (07/11/2026): Đặng Thị Kim Ngân 11710155→11711196, Phạm Tuấn Vũ 12510949→12511197, Phạm Văn Quang 11910228→11911195. Tra ISAPI cả 6 máy FaceID TPE (24, 30–34): đủ cả mã cũ lẫn mã mới, mỗi mã 1 khuôn mặt → máy nhận ra mã CŨ, `attendance:fetch` ghi lượt quẹt vào hồ sơ ETEK đã nghỉ. Code chưa hề có bước xoá người trên máy Hikvision khi nghỉ việc (chỉ có `deleteUser` cho máy vân tay ZKTeco qua python).
- [x] Xoá 3 mã cũ trên máy (07/11/2026): 6 máy chấm công TPE + máy cơm `rice_conn_infos.id=1` (14.248.82.176:4382) — 21 lượt, tra lại NO MATCH; thêm mã cũ của Vũ còn trên 2 máy ETEK GREEN (36, 37) — đối chiếu đúng tên rồi xoá. Mã mới vẫn còn khuôn mặt trên cả 7 máy.
- [x] Chuyển 13 lượt chấm từ 03/11 (12 lượt máy FaceID của Ngân, Vũ + 1 lượt app của Quang) sang mã mới, `company_id` 8→1 (`timesheets` id liệt kê trong lệnh, 1 transaction). Gỡ 3 dòng `rice_employee_info_conn_infos` của mã cơm cũ.
- [x] Chạy lại bảng công `calc:many_timesheet 2026-11-03 2026-11-07` trên prod (07/11/2026, 7 phút 20 giây). Kiểm `timesheet_summaries`: Ngân + Vũ 03–06/11 đủ giờ vào/ra, 1 công/ngày (Vũ đi muộn 2–3 phút các ngày 03, 05, 06); Quang 03–07/11 1 công/ngày. Ngày 07/11 của Ngân/Vũ chưa có giờ ra nên đang 0 — cron `calc:timesheet` mỗi giờ sẽ tự tính sau khi chấm ra.
- [x] Kiểm suất cơm 05–06/11 bị đánh "đăng ký nhưng không ăn" (07/11/2026): tải đủ 1.273 lượt quẹt của máy cơm 03–07/11 (ISAPI AcsEvent) — 3 người chỉ quẹt ngày 03/11 (mã cũ, 11:42–11:58), ngày 05–06/11 KHÔNG quẹt máy cơm → trạng thái "không ăn" là đúng, không sửa.
- [x] Tra yêu cầu "đổi ca 3 người ở TPE về ca văn phòng PTT" (07/11/2026): Ngân (1767), Vũ (1768) ĐÃ ở ca `1.1.VP_PTT` (id 1, chi tiết 7) từ 03/11→01/11/2027; Quang (1766) đang ca `1.5.KD_HN` (id 6, chi tiết 9) — do Nguyễn Thị Duyên (#883) chủ động chuyển từ VP_PTT sang lúc 03/11 16:04 (shift_assignment_history 962/963). Ngày 02/11: công nằm ở hồ sơ ETEK cũ (104/183/1501 mỗi người 1 công, ca VP_ETEKGROUP), không mất. Hồ sơ cũ còn dòng tổng hợp 03/11 = 0 công (thừa, do lượt chấm đã chuyển sang mã mới). Chờ user chốt có đổi ca Quang không.
- [x] User yêu cầu đưa công 02/11 sang hồ sơ TPE (07/11/2026): bản sao dữ liệu cũ lưu scratchpad `backup_0211.txt`. Chuyển 6 lượt chấm 02/11 (timesheets 7504135, 7504272, 7504303, 7504984, 7505111, 7505270) sang mã mới, company 1; xoá 792 dòng phân ca còn lại từ 02/11 của 3 hồ sơ ETEK đã nghỉ (104/183/1501, ca VP_ETEKGROUP tới 01/10/2027); `delete:employee_timesheet` 02–03/11 cho 3 hồ sơ cũ (gồm cả dòng 03/11 = 0 công thừa); `add:employee_timesheet` ngày 02/11 theo ca TPE đang có (Ngân, Vũ ca 1 / chi tiết 7; Quang ca 6 / chi tiết 9 — giữ ca Duyên đã xếp). Kiểm: TPE 02/11 mỗi người 1 công (Vũ muộn 2 phút), hồ sơ ETEK không còn công 02/11.

## Phase 2 — Tự xoá mã trên máy khi nghỉ việc (BE hrm-api)

- [x] `Modules/Timesheet/Services/LeftEmployeeMachineCleanupService.php` (07/11/2026): hồ sơ status=0 → tìm mã chấm công (`employee_infos.ssn`) trên mọi máy Hikvision `conn_infos` (machine_type_id=2, status 1/2) và mã cơm hiện hành (`employees.rice_ssn`) trên `rice_conn_infos` status=1; chỉ xoá khi tên trên máy khớp họ tên hồ sơ (cho phép máy cắt cụt tên) và mã không thuộc hồ sơ chưa nghỉ khác; xoá xong gỡ dòng `employee_info_conn_infos` / `rice_employee_info_conn_infos`. Không lấy mã cơm cũ ở các dòng `rice_employee_infos` khác (dễ đã cấp lại cho người khác).
- [x] Job `RemoveLeftEmployeeFromMachinesJob` (queue mặc định, 3 lượt, thử lại sau 10 phút / 1 giờ nếu máy lỗi mạng) + trait `Modules/Timesheet/Traits/RemovesFromMachinesOnLeave` gắn vào 3 model ghi `employee_infos` (Human, App\Models — đường quyết định chấm dứt HĐLĐ, Timesheet): status đổi sang 0 thì đẩy job sau commit.
- [x] Lệnh `timesheet:remove-left-from-machines {--employee=*} {--days=2} {--all} {--dry-run}` + lịch 01:45 hằng ngày (`--days=2`) dọn bù cho cập nhật không qua model (query builder) / job lỗi.
- [x] Test local (07/11/2026) bằng `Http::fake` trong transaction rồi rollback — 16/16 PASS: hồ sơ đang làm bỏ qua; model Human + App\Models đẩy đúng 1 job, lưu lại không đổi status thì không đẩy; dry-run không xoá; máy đúng tên xoá, lệch tên bỏ qua, mất mạng báo lỗi không vỡ; máy cơm xoá theo mã cơm; mã trùng người đang làm (chấm công lẫn cơm) không xoá; job + lệnh artisan chạy được.
- [x] User cho push (07/11/2026): commit `0214e192b` nhánh `feat/xoa-ma-may-khi-nghi-viec`, fast-forward lên `gop_db`; deploy prod bằng `~/build_tpe.sh`.
- [x] Deploy prod 07/11/2026: `build_tpe.sh` dừng ở `php artisan migrate` (không có tty để trả lời câu hỏi môi trường production, thiếu `--force`); code đã kéo, không có migration chờ → chạy tay `route:cache`, `permission:catalog-sync`, `queue:restart`; opcache validate_timestamps=On; lịch 01:45 đã lên `schedule:list`.
- [x] Dry-run `--all` trên prod (07/11/2026, 8 phút 28 giây, file `/tmp/remove_left_dryrun_20261107.txt` trên hrm-prod): 118 hồ sơ đã nghỉ còn trên máy — 636 lượt sẽ xoá (máy chấm công TPE 24, 30–34: ~78 lượt/máy; ETEK GREEN 36, 37: 27–30; máy cơm 117), 1 lệch tên ("Lã Duy ThànhĐạt" trên máy cơm, thiếu dấu cách → bỏ qua), 0 lỗi mạng, 0 mã trùng người đang làm. Theo công ty: TPE 72, ETEK GREEN 33, ETEK đầu tư 8, TP Sài Gòn 3, CN Vinh 2. 66/118 hồ sơ không có ngày nghỉ.
- [ ] Chờ user cho dọn thật (`--all`, bỏ `--dry-run`).

### Checkpoint — 2026-11-07 10:55
Vừa hoàn thành: code + test local Phase 2
Đang làm dở: —
Bước tiếp theo: xin phép commit/push nhánh code; hỏi user có sửa suất cơm 05–06/11 không
Blocked:
