---
name: app-notification
description: Thông báo trên TPE_APP — nội dung do hrm-api dựng (NotificationMeta, skill notification-convention), app hiển thị ở màn Thông báo + đẩy về điện thoại (FCM), bấm vào mở đúng màn theo data.type / data.id (ui/notification/notification_router.dart — dùng chung cho bấm push và bấm dòng ở màn Thông báo), nhắc hạn Việc của tôi (work_reminder.<loại>), thử thông báo đẩy trên simulator (simctl push). Dùng khi BE thêm loại thông báo mới, bấm thông báo không mở / mở nhầm màn, thông báo hiện "xem trên web", cần xem thông báo trên màn hình khoá.
---

# Thông báo — TPE_APP

## 1. Ai làm gì

| Phần | Ở đâu |
|---|---|
| Nội dung `[PREFIX] Nhóm hành động: <b>Tên</b>. Ghi chú` (≤ 180 ký tự, `note_full`) | hrm-api — `NotificationMeta::build()`, theo skill HRM `notification-convention` |
| Gửi: lưu DB (chuông web + màn Thông báo app) + socket (web realtime) + push FCM | `EmployeeInfoService::sendNotification($infoId, $data + ['url','type','id'], $command)` |
| Tiêu đề / nội dung push | `NotificationMeta::push()` → tiêu đề là CÂU tự nhiên (vd "Nhiệm vụ sắp đến hạn", "Đơn xin nghỉ bị từ chối", "Bình luận mới về nhiệm vụ" — `PUSH_TITLE_PHRASES`, chốt 30/10/2026), nội dung phần còn lại; data có `push_title` / `push_body` thì dùng nguyên (bản tin sáng liệt kê việc theo giờ) |
| Bấm mở màn | app `ui/notification/notification_router.dart` → `openNotificationTarget()` theo `data.type`, `data.id` — **1 bảng duy nhất** cho cả bấm push (AppBloc, `fromPush: true`) lẫn bấm dòng ở màn Thông báo. Trước 30/10/2026 có 2 bảng riêng, bảng của push thiếu 18 loại (bấm push chỉ mở app) — KHÔNG thêm `switch` thứ 2 |

App KHÔNG tự ghép câu thông báo. Tiền tố có dấu sẽ bị `strtoupper` của `NotificationMeta::build` làm hỏng → tiền tố
chỉ dùng chữ không dấu (`VIEC`, `TASK`, `PGV`, `PCT`, `MET`).

## 2. Loại thông báo ↔ màn mở (BẮT BUỘC khi BE thêm loại mới)

- BE thêm `type` mới → **phải thêm `case` trong `openNotificationTarget()`**, nếu không bấm vào chỉ hiện "Vui lòng xem chi
  tiết trên web". Kiểm cả 2 nơi trước khi báo xong.
- `type` phải nói đúng đối tượng. KHÔNG mượn type của luồng khác (bẫy thật: thông báo Phiếu giao việc / Phiếu
  giao công tác dùng `lateInEarlyOutApprove` → app mở màn duyệt Đi muộn về sớm; phần "Tạo mới" đã đổi sang
  `assign_job` / `assign_business` 29/10/2026, các thông báo Chờ duyệt / Đã duyệt cũ của 2 phiếu này vẫn còn sai).
- `data.id` = id đối tượng cần mở (không phải id người nhận).
- ⚠️ **Thêm màn cho loại NHẠY CẢM** (prefix nằm trong `NotificationMeta::SENSITIVE_PREFIXES` — Quyết định `QD`,
  bảo hiểm `DKBH`, hồ sơ `HSTK`, thu chi `DNTT`/`PT`/`PC`/`PBC`/`PKT`/`DCCN`/`HTBS`…) → ngoài `case` ở router **PHẢI
  thêm prefix vào `NotificationMeta::APP_SCREEN_PREFIXES`** (hrm-api). Chưa thêm thì push màn hình chờ vẫn ghi
  "Xem chi tiết trên web" thay vì "Mở ứng dụng để xem chi tiết" (chốt 06/11/2026, skill `notification-convention` mục 6).
- Nhắc hạn Việc của tôi: `type = work_reminder.<loại>` (task, issue, assign_job, assign_business, ts_job,
  ts_business, meeting, personal, digest) → `openWorkItemById(loại, id)` (`ui/my_todo/my_todo_actions.dart`).
  Loại chưa có màn trên app (issue) → snackbar "chưa có trên app"; personal / digest → mở Việc của tôi.

## 2a. Icon theo loại (02/11/2026)

- Ô icon bên trái dòng thông báo theo PREFIX (`ui/notification/notification_icon.dart`): loại có trong Việc của tôi lấy
  đúng icon + màu `WorkType` (Nhiệm vụ, Vấn đề, Meeting, phiếu giao việc / công tác, nhắc việc); loại khác icon riêng theo
  nhóm (kho, tài chính, đào tạo…). Prefix chưa khai → icon phân hệ; nhóm Khác / không rõ → loa `campaign_outlined` navy.
- Web dùng chung bảng (hình Remix): `hrm-client/utils/notificationIcon.js` — thêm prefix thì sửa CẢ 2 nơi.
- Mở chuông từ trong 1 phân hệ → màn Thông báo chọn sẵn chip phân hệ đó (`AppModule.current`), "Tất cả" để xem hết.
- Mapper `fetchNotifications`: `data.id` có thể là chuỗi (vd `runId` đồng bộ khuôn mặt) — luôn `int.tryParse`, ép
  kiểu là cả danh sách "Không tải được thông báo".

## 2b. Bấm push khi app TẮT HẲN (iOS UIScene) — đã vỡ 1 lần, đừng gỡ

- App chạy UIScene (`ios/Runner/SceneDelegate.swift`) nên iOS đưa thông báo mở app qua
  `connectionOptions.notificationResponse`, KHÔNG qua launchOptions → `FirebaseMessaging.getInitialMessage()` LUÔN null
  (firebase_messaging 15.x). Triệu chứng: app đang tắt, bấm push chỉ mở tới "Chọn phân hệ"; app chạy nền thì vẫn đúng.
- Cách đang chạy (02/11/2026): SceneDelegate giữ `userInfo` → `AppDelegate.launchNotification` → Dart gọi kênh `hrm/tp`
  `takeLaunchNotification` trong `AppBloc` khi getInitialMessage rỗng; chờ navigator ≤ 10s + 600ms rồi mới mở;
  chặn mở trùng 15s (firebase vẫn có thể bắn thêm `onMessageOpenedApp` cho cùng lần bấm).
- Android: thông báo hiện lúc app đang mở (`LocalPushNotificationHelper.notify`) bấm vào cũng đi `openNotificationTarget`.
- Loại app chưa có màn: vẫn mở app (màn đang đứng / Chọn phân hệ) + `AppToast.info` 6s "Nội dung này chưa có trên app,
  vui lòng xem chi tiết trên web" (user chốt 02/11/2026 — không mở trình duyệt, không đỏ như lỗi).
- Thử: `xcrun simctl terminate` app → `simctl push` (payload có `gcm.message_id`) → chạm banner NGAY (≤ 2s, banner tự
  tắt; chạm thông báo trong Trung tâm thông báo của simulator không ăn) → chờ ~15s (bản debug khởi động chậm) → chụp màn.

## 2c. Số chưa đọc: chuông ↔ icon app ↔ màn Thông báo — MỘT nguồn (chốt 06/11/2026)

Nguồn duy nhất = số chưa đọc BE (`unreadNotificationCount` của `users/auth/user-profile` =
`$employeeInfo->unreadNotifications()->count()`). App KHÔNG tự cộng / trừ số trên icon.

| Lúc nào | Ai đặt số | Ở đâu |
|---|---|---|
| Push đến (kể cả app tắt hẳn) | BE gửi kèm `aps.badge` (iOS) + `notification_count` (Android) | `App\Support\NotificationBadge` → `FCMService::setBadge()` trong `SendNotification` / `Rice\SendMobileNotification` |
| Mở app · quay lại app · đăng nhập | `NotificationBellButton.refreshAll()` | `MyApp` (`AppLifecycleListener`), `AppBloc._onInitLoad`, `LoginBloc` |
| Push đến lúc đang mở app | `refreshAll()` trong `onMessage` | `AppBloc` |
| Đọc 1 dòng / vuốt đọc / Đọc tất cả | màn Thông báo đẩy tổng mới lên `NotificationBellButton.setCount()` | `NotificationPage` (BlocListener) |
| Bấm push | gọi `mark_as_read` theo `data.notification_id` rồi `refreshAll()` | `AppBloc._markPushRead` |
| Đăng xuất / phiên hết hạn | `AppIconBadge.set(0)` | `UserRepositoryImpl.logout`, `RemoteExceptionHandler` |

- `NotificationBellButton` giữ số DÙNG CHUNG (`count` — `ValueListenable`) cho mọi nút chuông + icon; `refreshAll()` gộp
  các lần gọi trùng thành 1 request. Màn Thông báo nghe `count`, lệch số đang hiện thì tự tải lại (push mới lúc đang mở màn).
- `AppIconBadge` (`lib/helper/app_icon_badge.dart`): iOS đặt số qua kênh `hrm/tp` `setBadgeCount` (AppDelegate), về 0
  thì xoá khay; Android không đặt được số (launcher tự đếm theo khay / Android gốc chỉ chấm) → về 0 thì xoá khay.
- **"Đọc tất cả" chỉ đọc hết PHÂN HỆ của chip đang chọn** (chip "Tất cả" = mọi phân hệ) — user chốt GIỮ cách này
  06/11/2026 sau khi đã thử đổi sang "luôn đọc hết". Nút hiện theo số chưa đọc của chip đang chọn; đọc xong chuông + icon
  còn số của phân hệ khác là ĐÚNG. Đọc xong ở tab "Chưa đọc" thì tải lại cho trống.
- Đường gửi push mới: truyền `notification_id` (id dòng `notifications`) vào `$notificationData` trước khi dispatch —
  thiếu thì bấm push không đánh dấu đã đọc, và số trên icon có thể thiếu 1 nếu job chạy trước khi dòng được ghi.
- Thử số trên icon ở simulator MỚI: Cài đặt → app → Notifications phải BẬT (mặc định Tắt → push/badge không hiện).

## 3. Nhắc hạn (BE `WorkReminderService`, chốt 29/10/2026)

- Từ 02/11/2026 MỖI NGƯỜI tự cấu hình (app: Cài đặt → Thông báo → Nhắc việc, cùng chỗ với Thông báo cơm · web popup ở Việc của tôi, API
  `assign/work-reminder-preferences`): bật/tắt từng loại + nhắc trước (Tự động = 25% độ dài việc, 15 phút – 1 ngày;
  mọi mốc ≤ 1 ngày). Tắt = vẫn vào chuông, KHÔNG push (`no_push`); quá hạn luôn push. Màn cấu hình theo
  công ty `/assign/work-reminder-settings` + quyền "Cấu hình nhắc hạn công việc" đã BỎ (02/11/2026, quyền ở REMOVED). Quá hạn báo ĐÚNG 1 lần (Nhắc việc cá nhân: 07:30 sáng
  hôm sau); bản tin sáng 07:30 MỖI NGÀY kể cả CN, chỉ khi hôm đó có việc (có công tắc riêng); tổng quá hạn sáng thứ Hai.
- Chạy `assign:send-work-reminders` (5 phút) + `assign:send-work-digest`; thử bằng `--at="Y-m-d H:i"`.
- Chi tiết + bảng từng loại: `HRM/.plans/mytodo-nhac-han/design.md`.

## 4. Thử trên simulator

- Simulator local không nhận FCM → dựng đúng tiêu đề / nội dung BE sẽ gửi rồi đẩy thẳng:
  ```bash
  # payload: {"aps":{"alert":{"title":"…","body":"…"},"sound":"default"},"gcm.message_id":"x","type":"…","id":"…"}
  xcrun simctl push <device> com.tanphat.app payload.json
  ```
  Lấy title/body bằng tinker `NotificationMeta::push(NotificationMeta::stripSender($data))` từ dòng `notifications`.
- Xem màn hình khoá: Simulator → Cmd+L rồi push; kéo lên xem nhóm.
- Bấm thử từng loại trong màn Thông báo của app → mở đúng màn (chi tiết đúng bản ghi).

## Checklist

- [ ] Nội dung dựng ở BE theo `notification-convention`, tiền tố không dấu
- [ ] `type` riêng đúng đối tượng + `case` trong `openNotificationTarget()` (thử bấm cả push lẫn dòng ở màn Thông báo); `id` là id đối tượng
- [ ] Loại nhạy cảm vừa có màn trên app → đã thêm prefix vào `NotificationMeta::APP_SCREEN_PREFIXES` (push ra "Mở ứng dụng để xem chi tiết")
- [ ] Bấm thử trên app mở đúng màn; push hiện đúng trên màn hình khoá
- [ ] Đường gửi push mới có `notification_id` + số trên icon đúng (mục 2c): push đến → icon = số chưa đọc; bấm push → giảm 1
