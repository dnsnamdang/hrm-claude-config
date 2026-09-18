# Plan — Hủy cơm theo đơn xin nghỉ có phiếu DKSA dài ngày (Redmine #11476)

Nhánh: `tpe` (hrm-api + hrm-client). Phụ trách: @cuong61n

## Phase 1 — BE
- [x] `SheetRegistrationService`: thêm helper resolve rice_employee_info_id từ employee_info_id (có guard khi NV chưa có hồ sơ cơm)
- [x] `checkDuplicateTimeWithRiceRegistrationAttendance()` nhận employee_info_id của đơn nghỉ thay vì `auth()->riceUser()`
- [x] `rejectDuplicateTimeWithRiceRegistration()`: sau khi hủy `rice_registrations`, xử lý phiếu DKSA dài ngày — đơn nghỉ trùm trọn phiếu → phiếu về "Đã huỷ"; ngắn hơn → giữ "Đã đăng ký"
- [x] `AttendanceController@store`: truyền employee của đơn (đơn sửa/duyệt lấy theo `attendances.employee_id`)

## Phase 2 — FE
- [x] `pages/timesheet/attendance/add.vue` + `_id/index.vue`: gửi kèm `employees` (employee_info_id của đơn) khi gọi `reject-duplicate-time`

## Ghi chú
- Chưa làm (chờ chốt với khách): chuyển thời điểm hủy cơm sang bước trưởng phòng DUYỆT đơn (spec ảnh), và xử lý ngày nghỉ nằm ngoài phạm vi phiếu DKSA.

## Kiểm thử (17/09/2026, local)
- [x] Script `test_11476.php` (chạy `php test_11476.php` từ worktree hrm-api): 10 nhóm, **40/40 PASS**, tự tạo + tự dọn fixture
- [x] Đối chứng: chạy chính script đó trên code CŨ → **6 FAIL** (phiếu dài ngày không huỷ, 500 khi employee rác/chưa có hồ sơ cơm, soi nhầm người)
- [x] UI thật (FE :3005 + BE :8005): NV tự tạo đơn nghỉ → popup "Xác nhận huỷ cơm" → Hủy cơm → đúng ngày bị huỷ, phiếu dài ngày còn hiệu lực
- [x] UI thật: đơn nghỉ trùm trọn phiếu DKSA → phiếu về "Đã huỷ" + lý do, hiển thị đúng ở màn Phiếu đăng ký suất ăn
- [x] Admin gửi duyệt đơn của NV khác: code mới trả 423 (cảnh báo đúng người), code cũ trả 200 (bỏ lọt)

## Phase 3 — Popup huỷ cơm không hiện khi chưa có thực đơn (QA báo 17/09/2026)
- [x] Bỏ điều kiện `rice_menu_days` trong `checkDuplicateTimeWithRiceRegistrationAttendance()` — chỉ cần có ngày *Đã đăng ký* là cảnh báo
- [x] TC11 trong `test_11476.php`: có đăng ký cơm + không có thực đơn → vẫn cảnh báo và vẫn huỷ được (43/43 PASS; code trước đó FAIL đúng ca này)
- [x] Áp cùng cách cho `checkDuplicateTimeWithRiceRegistration()` (10 chỗ gọi: giao việc / công tác / đề xuất)
- [x] CHỐNG TÁI DIỄN: gom điều kiện vào `riceRegistrationsRegisteredInRange()` — cả 3 hàm cảnh báo lẫn hàm huỷ dùng chung, đổi điều kiện chỉ sửa 1 chỗ
- [x] TC12 (hàm dùng chung) + TC13 (bất biến: cảnh báo ⇔ huỷ luôn cùng tập ngày) — 53/53 PASS; code cũ FAIL TC12 và 500 khi employee rác
- [x] UI thật: khoảng 01–12/03/2027 không có thực đơn → popup VẪN hiện → huỷ đủ 12 ngày + phiếu dài ngày về Đã huỷ

## Dữ liệu đã sửa trên production (17/09/2026)
- Trịnh Thị Lợi (rice_employee_info 388): 167/167 ngày trong đơn nghỉ 01/07/2026–31/01/2027 về *Đã huỷ* + 167 dòng lịch sử; phiếu 1274/2025/PDKSA-TPE giữ *Đã đăng ký*
- Backup: `~/backup_11476_loi_20260917_105535.sql`, `~/backup_11476_loi_quakhu_20260917_110013.sql` (server erp_tpe)

## Phase 4 — Đổi luật huỷ phiếu ĐKSA dài ngày (chốt 17/09/2026)
**Quyết định đã chốt (lệch spec gốc #11476):** phiếu dài ngày phải về *Đã huỷ* khi **ngày kết thúc nghỉ >= ngày đăng ký cơm cuối cùng của phiếu**, không cần đơn nghỉ trùm trọn phiếu. Lý do: từ ngày bắt đầu nghỉ tới hết phiếu không còn ngày ăn nào, để phiếu "Đã đăng ký" gây hiểu nhầm (đúng ca chị Trịnh Thị Lợi). Nghỉ kết thúc TRƯỚC ngày cuối phiếu thì vẫn giữ hiệu lực.
- [x] `cancelLongSheetRegistrationInRange()`: bỏ điều kiện `$startTime > $sheetStart`, chỉ còn `$endTime < $sheetEnd` thì bỏ qua
- [x] TC14 trong `test_11476.php`: nghỉ 15/08–30/09 với phiếu 01/08–31/08 → phiếu huỷ, ngày trước 15/08 giữ nguyên; phiếu 01/08–31/10 vẫn hiệu lực — **60/60 PASS**, code cũ FAIL đúng 2 assertion này
- [x] Prod: phiếu 1274/2025/PDKSA-TPE của chị Lợi đã chuyển *Đã huỷ*, lý do "Huỷ cơm do nghỉ thai sản" (backup `~/backup_11476_loi_phieu1342_20260917_141238.sql`)
- [x] Đã push nhánh `tpe`: `eecbb6d90..6d54e9b1f` (chỉ BE, FE không đổi)
