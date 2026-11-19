# #11567 (web) + #11568 (app) — Duyệt ngay tại màn Quản lý đơn — @cuong61n

Nhánh: hrm-api / hrm-client `develop` (con của `gop_db`), TPE_APP `develop`. CHƯA commit.

## Quyết định đã chốt (17/10/2026)
- Cách duyệt: **làm như màn Phê duyệt hiện tại** — menu hành động của dòng có "Duyệt" / "Từ chối", bấm mở màn chi tiết duyệt sẵn có (không duyệt tại chỗ). Lệch lựa chọn ban đầu "duyệt ngay trên dòng" vì skill list-page/button-convention cấm Từ chối ở danh sách → user chốt theo màn Phê duyệt.
- Phạm vi: Phân công làm thêm CÓ (dùng màn duyệt của Đăng ký làm thêm; thực tế phiếu phân công luôn lưu thẳng Đã duyệt nên hầu như chỉ hiện "Từ chối"), Tra soát công admin BỎ (không có luồng duyệt). App không có màn Phân công / Phiếu YC làm thêm / Tra soát admin → app làm 4 loại.
- Siết BE: cờ can_approve/can_reject = quyền PD/XN + phạm vi phòng quản lý (khớp query màn Phê duyệt) + trạng thái; API duyệt chặn 403 theo chính cờ đó.

## Phase 1 — BE
- [x] `Modules/Timesheet/Support/ApproveScope` — phạm vi quản lý, cache RequestCache
- [x] Siết can_approve/can_reject: Attendance (+ canNSHCApprove), LateEarlyOut (sửa nhầm quyền isNotTP), OvertimeAssignment (phân công xét theo phòng ban), OvertimeRequirement; RequestUpdateTimeSheet chuyển cờ từ show() vào Entity
- [x] 5 List Resource trả `can_approve` / `can_reject`
- [x] Trait `AuthorizesApproveAction` → 403 ở API duyệt LEO / OA / OR / RUT
- [x] Vá: từ chối gửi `'reject'` (app) không bắt nhập lý do ở LEO / OA / OR
- [x] Verify tinker (cờ chỉ bật trong phạm vi màn Phê duyệt, ngoài phạm vi = 0) + curl (403 ngoài phạm vi, 422 thiếu lý do, list có cờ, ~0,3s)

- [x] Vá (lộ ra khi test 17/10): AttendanceApproveRequest chỉ chặn khi status là số → app gửi 'approve'/'reject' lọt qua; chuyển sang trait chung
- [x] Vá: 5 request duyệt nhận status bất kỳ (tra soát gửi giá trị lạ = từ chối không lý do) → thêm `in:approve,reject,2,3` (tra soát `in:approve,reject`)
- [x] Test BE ma trận 4 tài khoản (A TP phòng 80 · B TP phòng khác · C NSHC · D nhân viên lập phiếu): 61/61 đạt — script scratchpad `matrix.py`

## Phase 2 — FE web
- [x] Mục Duyệt / Từ chối trong menu bánh răng 6 màn: attendance, late-in-early-out, overtime-assignment, overtime-allocation, overtime-requirement, request-update-working
- [x] 5 màn `_id/approve.vue`: `backListUrl` (?from=) → Quay lại / duyệt xong về đúng màn QL đơn
- [x] Test Playwright 4 tài khoản: 44/44 đạt (hiện/ẩn mục theo quyền, Quay lại/duyệt xong về QL đơn, từ chối có lý do, hồi quy màn Phê duyệt)

## Phase 3 — App
- [x] `custom_view/approve_action_tiles.dart` + 4 danh sách: bấm phiếu được duyệt mở chế độ duyệt; menu "..." có Duyệt / Từ chối
- [x] `dart analyze` sạch 5 file
- [x] Theme chung: `ListTileThemeData(minLeadingWidth: 24, horizontalTitleGap: 12)` ở `ui/app/my_app.dart` — user chốt thu gọn khoảng cách icon–chữ menu toàn app (ảnh hưởng mọi ListTile, gồm menu trái)
- [x] Test app (mobile-mcp) iOS: A duyệt ĐMVS / từ chối làm thêm có lý do / duyệt đơn nghỉ (→ chờ NSHC) / duyệt tra soát cấp 1; C duyệt tra soát cấp 2; D không có Duyệt/Từ chối, mở chế độ xem; B không thấy phiếu phòng khác; hồi quy menu Phê duyệt — đạt
- [x] Test app Android (Pixel 4 API 29): A duyệt ĐMVS + từ chối làm thêm có lý do, menu "..." đúng — đạt

## Phase 4
- [x] Chuyển #11567, #11568 sang "Đang tiến hành"

### Checkpoint — 2026-10-19
Vừa hoàn thành: commit + push GitHub `develop` cả 3 repo — hrm-api bd3d9866a (kèm commit "fix bug" eb62b1d4d của user, user đồng ý push chung), hrm-client 73c591228, TPE_APP 68d2b71. Chưa kéo về server.
Đang làm dở: không.
Bước tiếp theo: deploy dev/prod khi user yêu cầu; build app mới để phát hành.
Blocked:

### Checkpoint — 2026-10-17 (tối)
Vừa hoàn thành: test xong BE 61/61 · web 44/44 · app iOS (4 tài khoản) + Android. ĐÃ DỌN hết trạng thái tạm bên dưới (phiếu thử, mật khẩu, build_config, Podfile, xcscheme); simulator/máy ảo đã tắt.
Đang làm dở: không.
Bước tiếp theo: commit khi user cho phép (hrm-api, hrm-client nhánh develop; TPE_APP develop).
Blocked:

### Checkpoint — 2026-10-17 (chiều) — ĐÃ DỌN
Trạng thái tạm (đã dọn xong lúc tối):
- TPE_APP `build_config.dart` flavor develop trỏ `http://127.0.0.1:8000/api/` → `git checkout -- app/lib/shared/lib/src/build_config/build_config.dart`
- Mật khẩu tạm `Test11567@` cho employees 435 vannt.ktsg (A) · 522 phuongdtk.nssg (C) · 433 thuyvt.ktsg (D) · 504 hoant.khosg (B) — hash cũ lưu ở scratchpad phiên 86b62489…/pw_backup.tsv, khôi phục bằng UPDATE employees SET password=<hash cũ>
- Phiếu thử (NV Vương Thị Thùy, đánh dấu TEST11567): attendances 13369 (gửi duyệt) 13370 (chờ NSHC) · late_early_outs 202 · overtime_assignments 5543 (đk) 5544 (phân công đã duyệt) · overtime_requirements 199 · request_update_timesheet 22732 (gửi duyệt) 22733 (chờ NSHC) — xoá + timesheets place='Tra soát công' id>7401758 + jobs id>2267 + notifications gắn các id này (script scratchpad cleanup.py)
Bước tiếp theo: test app 10 nhóm case (A/B/C/D × 4 màn QL đơn: hiện "..." Duyệt/Từ chối đúng cờ, bấm mở chế độ duyệt, duyệt/từ chối thật kiểm DB, hồi quy menu Phê duyệt) → dọn trạng thái tạm → báo user.
Blocked:
