# Plan — Nội dung thông báo đủ thông tin cơ bản

## Phase 1 — Hạ tầng
### BE
- [x] NotificationMeta: MAX_TOTAL 180, note_full, day/dayTime/range/money; EmployeeInfoService cho note_full đi qua
### FE
- [x] App: Xem thêm dùng note_full
- [x] Web: NotificationItem dùng note_full
### Docs
- [x] Skill notification-convention + CLAUDE.md: 120 → 180, note_full

## Phase 2 — Viết lại từng thông báo (BE)
- [x] Timesheet + Payroll + Human + Decision + Console
- [x] Assign
- [x] Finance
- [x] Training + Rice + Meeting + CustomerCare + MasterData
- [x] Rà chéo: php -l, grep còn title nối tay, test build() thực tế vài loại
- [ ] Bảng câu cũ → câu mới gửi user
- [x] Sửa thêm: build() không chấm thêm sau tên đã cắt '...'; khảo sát đào tạo + hoãn kỳ ĐGNL + 2 notifier tính giá (PTG/YCTG, giữ nhóm hành động N187)
- [x] Test: php -l 115 file; phpunit MasterData/Assign/Finance/CustomerCare/Human — fail còn lại là lỗi có sẵn ngoài phạm vi; e2e đơn xin nghỉ (rollback) ra đúng câu + note_full
- [x] Sửa: 7 chỗ kết quả duyệt/từ chối gửi nhầm người duyệt → gửi người tạo (PCT, PGV ×3, PDX ×3); báo giá tổng đổi employees.id → employee_info_id; phiếu giao việc gửi người duyệt 1 lần (không lặp theo nhân sự)
- [x] Push: tiêu đề `Nhóm hành động · Loại đối tượng` (NotificationMeta::OBJECT_LABELS) — vì tên chỉ còn mã phiếu
- [x] Test app: gửi 85 thông báo mẫu (mọi prefix) tới namdangit qua sendNotification thật; danh sách + chip + Xem thêm (note_full) đúng; push giả lập simctl hiện khay thông báo đúng
- [x] Push không lộ thông tin nhạy cảm trên màn hình chờ (SENSITIVE_PREFIXES): đơn nghỉ / lương / bảo hiểm / HĐLĐ / QĐ / hồ sơ / thu chi chỉ hiện người hoặc mã + "Mở ứng dụng để xem chi tiết"
- [ ] Chờ user quyết: prefix mới, gửi nhầm người nhận (7 chỗ), báo giá tổng sai loại id, module CSKH/HSTK/BL, thả cảm xúc giữ emoji

## Phase 3 — Sửa lỗi phát sinh
- [x] (29/10/2026) **Fix sập màn Yêu cầu tính giá / Tính giá trên dev** — mở `/sale/price-calculate-requests/add?group_id=4417` báo lỗi. Nguyên nhân: commit `2f543d6b4` (23/10) khai `private function actorName($label)` ở `PriceCalculateRequestNotifier` + `PriceCalculateNotifier`, trùng tên với `private static actorName()` của lớp cha `PriceAskingNotifier` → PHP 7.4 (dev/prod) fatal "Cannot make static method … non static" ngay lúc nạp class, mọi API dùng notifier trả 500 (log dev 10:35–11:05, user 867). PHP 8 local không lỗi nên không phát hiện khi test. Sửa: đổi tên hàm ở 2 lớp con thành `actorLine()`. Kiểm: PHP 7.4 tái hiện fatal ở bản cũ, bản sửa nạp OK; tinker trên dev new 2 class OK, log không còn lỗi mới. Đã push `develop` commit `a617dccd9`, deploy dev 29/10/2026 (`~/build_tpe.sh`). gop_db không có commit `2f543d6b4` nên không dính.
- [x] (06/11/2026) **Push loại nhạy cảm chỉ đúng nơi xem được** — @cuong61n. Nghiệp vụ: trước đây mọi loại nhạy cảm đều ghi "Mở ứng dụng để xem chi tiết", nhưng Quyết định / bảo hiểm / hồ sơ / thu chi chưa có màn trên app (bấm vào app báo "chưa có trên app, xem trên web") → 2 câu ngược nhau. Nay: app đã có màn (DXN, DMVS, BL) → "Mở ứng dụng để xem chi tiết"; app chưa có màn → "Xem chi tiết trên web"; toast web → "Bấm để xem chi tiết". Kỹ thuật: `NotificationMeta` thêm `APP_SCREEN_PREFIXES` + `privateHint()`, `push($data, $forWeb)`; `NotificationSocket` truyền `true`. Ghi quy tắc vào skill `notification-convention` mục 6 + checklist, `app-notification` mục 2 + checklist, comment nhắc ở `default` của `TPE_APP/.../notification_router.dart`. Kiểm: tinker `push()` 4 loại (DXN/BL ra câu app, QD/PC ra câu web, web toast ra "Bấm để xem chi tiết", loại thường PGV không đổi), `php -l` OK. Trạng thái: sửa local hrm-api (develop) + TPE_APP, chưa commit/push.
- [x] (06/11/2026) **Số đỏ trên icon app khớp số chưa đọc trong app** — @cuong61n. Nghiệp vụ: trước đây không ai đặt số trên icon app (BE không gửi `aps.badge`, app chỉ xoá về 0 khi "Đọc tất cả" của Thành An) → icon lệch hẳn số chuông. Nay 1 nguồn duy nhất = số chưa đọc BE: push gửi kèm số (cả khi app tắt), app đặt lại số khi mở app / quay lại app / đăng nhập / nhận push lúc đang mở / đọc trong màn Thông báo; đăng xuất xoá số. Đo PROD: đếm chưa đọc 2–3 ms (bảng 637.023 dòng, có index) → không làm chậm. Kỹ thuật BE: `App\Support\NotificationBadge`, `FCMService::setBadge()` (tự xoá sau mỗi lần gửi), `SendNotification` + `Rice\SendMobileNotification` gửi badge; `EmployeeInfoService::sendNotification` + `Training\SendNotificationToEmployee` truyền `notification_id`. App: `lib/helper/app_icon_badge.dart`, `NotificationBellButton` giữ số dùng chung + gộp request, `AppDelegate.swift` thêm `setBadgeCount`, `MyApp` (AppLifecycleListener), `AppBloc` (InitLoad, onMessage), `LoginBloc`, `UserRepositoryImpl.logout`, `RemoteExceptionHandler`. Skill: `app-notification` mục 2c, `notification-convention` mục 7b.
- [x] (06/11/2026) **"Đọc tất cả" mà vẫn còn số chưa đọc** (anh Nam báo, ảnh 12:47) — @cuong61n. Điều tra PROD (EmployeeInfo 6): nút đã đánh dấu 229 thông báo lúc 12:47:14 nhưng chỉ ở phân hệ Công việc (chip đang chọn) → Chấm công 618, Khác 691… vẫn chưa đọc, đầu màn + chuông vẫn ~1.354; tab "Chưa đọc" còn giữ dòng vừa đọc. Ban đầu user chốt "luôn đọc hết mọi phân hệ", sau đó (cùng ngày) user bảo **sửa lại theo cách cũ**: "Đọc tất cả" chỉ đọc phân hệ của chip đang chọn (chip "Tất cả" = mọi phân hệ) — `NotificationBloc._onMarkAllPressed` giữ nguyên như trước, nút hiện theo số chưa đọc của chip. Giữ phần sửa: tab Chưa đọc đọc xong thì tải lại cho trống, chuông + icon cập nhật ngay theo tổng còn lại. Test lại: chip Công việc (2) / tổng 9 → Đọc tất cả → Công việc 0, tổng 7, DB 7, icon 7.
- [x] (06/11/2026) **Bấm push đánh dấu thông báo đó đã đọc** — @cuong61n. Trước đây bấm push mở phiếu nhưng dòng chuông vẫn chưa đọc. BE gửi `notification_id` trong data push; app `AppBloc._markPushRead` gọi `mark_as_read` (cả lúc app tắt hẳn — đọc từ `takeLaunchNotification`/`getInitialMessage`).
- [x] (06/11/2026) **Màn Thông báo tự tải lại khi có thông báo mới lúc đang mở màn** — @cuong61n. Nghe số dùng chung, lệch số đang hiện thì tải lại (push đến / quay lại app sau khi đọc trên web).
- [x] (06/11/2026) **Test luồng số chưa đọc / đã đọc** — @cuong61n. BE (tinker, FCM giả không gửi thật): badge = số chưa đọc; job chạy trước khi dòng được ghi → +1; không `notification_id` → bằng số chưa đọc; singleton không dính badge sang push khác; job Cơm có badge; QĐ ra "Xem chi tiết trên web". App (simulator iPhone 15 iOS 17.5, tpeLocal, 56 bước, 0 lỗi Flutter): mở app → icon 22 · đọc trên web rồi quay lại → 20 · push lúc app ở nền → icon 21 · bấm push → mở đúng họp + DB đã đọc + chuông 20 · tab Chưa đọc + chip Công việc bấm "Đọc tất cả" (bản đọc hết, sau đã trả về cách cũ) → DB 0, mọi chip 0, danh sách trống, chuông + icon 0 · push lúc đang mở app → chuông tự lên 1 · push lúc đang ở màn Thông báo → màn tự tải lại · vuốt đọc rồi Home ngay → icon đúng · bấm 1 dòng → giảm · app tắt hẳn bấm push → mở đúng màn + đã đọc + icon đúng · đăng xuất → icon 0, quay lại app không gọi API thừa · đăng nhập → icon đúng · bấm đúp "Đọc tất cả" → 1 request. Lỗi tìm ra khi test và đã sửa: màn chọn phân hệ không đồng bộ icon (chuyển sang gốc app), vuốt đọc rồi Home icon chưa đổi, màn Thông báo không tự tải lại, hook đăng nhập/đăng xuất cũ không bao giờ chạy, quay lại app lúc đã đăng xuất gọi 401. CHƯA test: Android (emulator đang do phiên khác dùng), TK Thành An (màn nhóm), lỗi mạng khi "Đọc tất cả". Dữ liệu test local đã xoá, trả lại 6 chưa đọc ban đầu. Trạng thái: sửa local hrm-api (develop) + TPE_APP, chưa commit/push, chưa deploy.

### Checkpoint — 22/10/2026
Vừa hoàn thành: viết lại ~230 thông báo trên 115 file hrm-api theo khuôn tên riêng + ghi chú đủ ai · khi nào · loại · lý do (≤ 180, note_full)
Đang làm dở: —
Bước tiếp theo: user quyết các mục "Chờ user quyết"; (tuỳ chọn) bảng câu cũ → câu mới cho khách
Blocked:
