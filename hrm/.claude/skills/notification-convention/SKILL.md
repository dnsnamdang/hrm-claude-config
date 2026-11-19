---
name: notification-convention
description: Use when tạo/sửa bất kỳ thông báo nghiệp vụ nào (chuông web, màn Thông báo app, push màn hình chờ điện thoại, toast socket) ở BE hoặc FE — chuẩn nội dung, prefix, nhóm hành động, cách viết ghi chú, tiêu đề push ≤ 28 ký tự, loại nhạy cảm, type/id để bấm mở đúng màn, gửi socket qua NotificationSocket. Đọc cả khi push bị cắt "…", bấm thông báo mở nhầm màn / không mở, toast không hiện hoặc câu khác điện thoại.
---

# Skill: Notification Convention (Thông báo nghiệp vụ)

Áp dụng cho **mọi màn**, mọi module: khi nghiệp vụ có bắn thông báo cho người dùng
(tạo mới, duyệt, từ chối, nhắc hạn, bình luận…) thì nội dung + hành vi bấm phải theo chuẩn dưới đây.

> Chỉ nói về **thông báo nghiệp vụ**. Lỗi validate / toast kết quả thao tác
> ("Bạn chưa nhập đầy đủ thông tin", "Cập nhật thành công"…) xem mục 8.
>
> Bản gửi khách (5 sheet, ví dụ thật): `.plans/app-nhiem-vu-van-de/Nguyên tắc hiển thị thông báo.xlsx`.
> Trang xem đủ 167 loại ở 3 nơi: `.plans/app-nhiem-vu-van-de/thong-bao-3-noi.html`.

---

## 0. Tóm tắt 1 phút — người viết code CHỈ làm 3 việc

1. Dựng dữ liệu bằng `NotificationMeta::build(module, PREFIX, Nhóm hành động, Tên, Ghi chú)` — **không nối chuỗi tay**.
2. Kèm `url` (có ID), `type` **đúng loại đối tượng**, `id` = **id của chính phiếu** đó.
3. Gửi qua `EmployeeInfoService::sendNotification` / `sendToAllNotification` — **không** `notify()` + `Redis::publish` tự viết.

Mọi thứ còn lại (tiêu đề màn hình chờ, câu danh sách, toast web, ẩn thông tin nhạy cảm, cắt độ dài) do
`App\Support\NotificationMeta` + `App\Support\NotificationSocket` dựng **cùng một câu cho cả 3 nơi**. FE web và app
**chỉ hiển thị**, không tự ghép câu.

---

## 1. Cấu trúc dữ liệu lưu (bắt buộc)

```
[{PREFIX}] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}
```

| Thành phần | Quy tắc |
|---|---|
| `[PREFIX]` | Mã loại đối tượng, viết hoa (mục 3) |
| `{Nhóm hành động}` | Đúng 1 giá trị ở mục 2 |
| `{Tên đối tượng}` | **Tên riêng**, ≤ 50 ký tự (tự cắt): có mã → mã (`PNK-2026-00012`); có tiêu đề → tiêu đề; đơn không mã gửi người duyệt → `Người - Loại`, gửi chính chủ → `Loại + thời gian`. **Cấm lặp tên loại** (`Đơn xin nghỉ - …`, `Phiếu nhập kho PNK-…`) — loại đã nằm ở prefix |
| `{Ghi chú}` | Đủ **ai · khi nào · lý do** (mục 4). Tổng ≤ 180 ký tự; bị cắt thì bản đủ nằm ở `note_full` (nút Xem thêm) |

Ví dụ:
- `[MET] Tạo mới: Họp chốt phương án TKT. Thời gian: 14:00 12/08. Hình thức: Online`
- `[BG] Từ chối: BG-2026-00093. Người từ chối: DNS Admin. Lý do: Giá thấp hơn mức sàn`

Không viết câu tự do kiểu "Nguyễn A đã trả lời bình luận của bạn trong task X" — quy về
`[TASK] Góp ý: {Tên task}. Người trả lời: Nguyễn A. Nội dung: …`. Thông báo cũ câu tự do (hệ thống không tách được)
vẫn hiện, tiêu đề màn hình chờ chỉ là `Thông báo mới` (`FALLBACK_TITLE`) — sửa tới đâu chuẩn hoá tới đó.

---

## 2. Nhóm hành động (chỉ dùng các giá trị này)

`Tạo mới` · `Cập nhật` · `Chờ duyệt` · `Đã duyệt` · `Từ chối` · `Không duyệt` · `Yêu cầu làm lại` ·
`Góp ý` · `Sắp đến hạn` · `Quá hạn` · `Hủy` · `Tạm dừng` · `Tiếp tục` · `Thay đổi lịch` · `Nhắc báo cáo` ·
`Chờ tính giá` · `Chờ xử lý` · `Lỗi`

- `Không duyệt` chỉ khi chứng từ có trạng thái tên đúng "Không duyệt" (vd YCTG); còn lại dùng `Từ chối`.
- `Chờ xử lý` (phiếu chờ bộ phận tiếp nhận), `Lỗi` (job đồng bộ / lấy dữ liệu thất bại) — thêm 02/11/2026.
- **Thêm nhóm mới** = phải khai câu tương ứng ở `NotificationMeta::PUSH_TITLE_PHRASES` (câu thường + câu ngắn) VÀ
  màu ở `utils/notificationDisplay.js` `notificationActionColor` (web). Chưa khai thì tiêu đề màn hình chờ đọc máy móc.

## 3. Prefix + nhãn loại đối tượng

Prefix = mã viết tắt loại đối tượng, ưu tiên trùng mã phiếu trong hệ thống (`TASK`, `MET`, `GP`, `ISSUE`, `DXN`,
`PNK`…). Không có sẵn → đề xuất 3–5 ký tự và **hỏi user**.

### 3a. ⚠️ Prefix MỚI → BẮT BUỘC khai nhãn ở `NotificationMeta::OBJECT_LABELS`

Tiêu đề màn hình chờ / danh sách / toast là câu "Loại đối tượng + hành động" ("Đơn xin nghỉ bị từ chối"), loại tra từ
`OBJECT_LABELS`. Prefix chưa khai: phiếu 5 phân hệ app → ghép tên phân hệ; phiếu nhóm Khác (Kho, Vận chuyển, Tài chính,
CSKH…) → tiêu đề chỉ còn `Từ chối`, người nhận không biết phiếu gì (đã dính 30/10/2026 với 6 màn port ERP).

1. Thêm `'PREFIX' => 'Tên loại'` đúng nhóm (khoá HOA, không ngoặc). Nhãn ≤ 25 ký tự; **≤ 18 thì câu "… chờ duyệt"
   mới vừa 1 dòng**, dài hơn thì hệ thống tự rút (mục 5). Thêm dòng nhãn KHÔNG cần hỏi.
2. Loại cần câu riêng (họp "sắp bắt đầu" chứ không "sắp đến hạn") → `PUSH_TITLE_PHRASES_BY_PREFIX`.
3. Loại nhạy cảm → `SENSITIVE_PREFIXES` (mục 6).
4. Icon ô bên trái màn Thông báo app: thêm prefix vào `TPE_APP/app/lib/ui/notification/notification_icon.dart`
   (`_byPrefix`, icon Material + màu nhóm) VÀ web `hrm-client/utils/notificationIcon.js` (Remix, cùng màu). Chưa khai thì app dùng icon phân hệ; nhóm Khác → loa chung.

---

## 4. Viết ghi chú — dạng `Nhãn: giá trị`, hệ thống tự viết lại cho tự nhiên

Ghi chú LƯU ở dạng có nhãn (máy tách được), các đoạn cách nhau `. `. `friendlyNote()` viết lại khi HIỂN THỊ
(màn hình chờ, toast, danh sách) — vì vậy **phải dùng đúng nhãn dưới đây**, viết nhãn khác thì câu ra cứng như biểu mẫu:

| Lưu | Hiển thị |
|---|---|
| `Người từ chối: A. Lý do: …` · `Người duyệt: A. Ý kiến: …` (cả `hủy`/`xử lý`/`không duyệt`, `Ghi chú`) | `A: …` |
| `Người bình luận: A. Nội dung: …` (cả `trả lời`/`nhắc`) | `A: …` |
| `A nhắc đến bạn trong bình luận. Nội dung: …` | `A nhắc đến bạn: …` |
| `Người gửi: A` | `Từ A` |
| `Người giao: A` / `Người lập: A` | `Người giao A` |
| `Thời gian:` `Hình thức:` `Nội dung:` `Công việc:` `Ghi chú:` `Loại công:` | bỏ nhãn |
| `Địa điểm:` `Nơi làm:` `Nơi đến:` | `tại …` |
| `Mức ưu tiên: Cao` | `Ưu tiên cao` |
| `Mã: PGV-1` | bỏ (mã đã là tên) |
| `Lý do: …` / `Ý kiến: …` đứng riêng | giữ nguyên dấu `:` |
| `Hạn: 25/10` / nhãn khác | `Hạn 25/10` |

Quy tắc:
- **Chữ tự do người dùng gõ (lý do, nội dung, ý kiến) luôn đặt CUỐI** — cắt độ dài cắt từ cuối.
- Ai (khi người nhận không phải chính họ) · thời gian / khoảng ngày / số tiền · người xử lý · lý do. Vd
  `[DXN] Chờ duyệt: Nguyễn Văn An - Phép năm. 23/10 – 24/10/2026 (2 ngày). Lý do: Về quê`.
- Ngày giờ dùng helper `NotificationMeta::day/dayTime/range/money` — không tự format.
- Số theo chuẩn quốc tế (`1,234,567`).

---

## 5. Ba nơi hiển thị — cùng một câu

| Nơi | Tiêu đề | Thân | Ai dựng |
|---|---|---|---|
| **Màn hình chờ điện thoại** (FCM) | câu "Loại + hành động", **≤ 28 ký tự, không bao giờ bị "…"** | tên + ghi chú tự nhiên, cắt trọn đoạn ≤ 120 | `NotificationMeta::push()` |
| **Toast web** (socket) | = tiêu đề màn hình chờ | = thân màn hình chờ | `NotificationSocket::publish()` → gói `toast` + `id`; FE `utils/notificationToast.js` |
| **Danh sách thông báo** (chuông web + màn Thông báo app) | chấm màu hành động + `headline` (≤ 40) — **không hiện mã prefix** | tên in đậm + `note_text` (đầy đủ, 2 dòng + Xem thêm) | `NotificationMeta::display()` |

Tiêu đề màn hình chờ chọn theo thứ tự (đo iPhone: 32 ký tự đã bị cắt vì dòng còn chừa chữ giờ):
1. `push_title` truyền riêng nếu ≤ 28 → dùng; **dài hơn thì bị BỎ** (rơi về câu khuôn).
2. Câu thường `PUSH_TITLE_PHRASES` ("Đơn xin nghỉ đang chờ duyệt") → quá 28 thì câu ngắn ("… chờ duyệt").
3. Vẫn quá → tiêu đề chỉ tên loại, hành động xuống đầu thân ("Đang chờ duyệt: …").
4. Không tách được (câu tự do cũ) → `Thông báo mới`.

`push_title` / `push_body` riêng chỉ dùng khi câu khuôn không hợp (bản tin sáng, check-in cơm…) và **tự giữ ≤ 28**.
Ví dụ đã chốt: "Xin kết thúc sớm công tác", "Bảo hành chờ tiếp nhận", "Lỗi lấy dữ liệu chấm công".

Toast web: thẻ trắng góc phải trên, **vạch trái** màu hành động (chữ tiêu đề KHÔNG tô màu — đỏ chỉ cho lỗi validate),
6 giây, rê chuột thì giữ, bấm = mở phiếu + đánh dấu đã đọc. Dòng danh sách: chữ headline xám đậm `#374151`, màu chỉ ở chấm.

---

## 6. Loại nhạy cảm — màn hình chờ không lộ nội dung

`SENSITIVE_PREFIXES` (đơn nghỉ, đi muộn về sớm, lương, bảo hiểm, quyết định, hồ sơ tự khai, thu chi / công nợ):
màn hình chờ + toast chỉ còn người hoặc mã + `Mở ứng dụng để xem chi tiết`; danh sách (đã mở khoá) vẫn hiện đủ.
HĐLĐ sắp hết hạn **không** nhạy cảm (user 02/11/2026 — hiện "còn N ngày"). Thêm loại có lương / tiền / sức khoẻ /
hồ sơ cá nhân → khai vào danh sách này.

**Lời nhắc thay ghi chú phải chỉ ĐÚNG nơi xem được** (user chốt 06/11/2026) — `NotificationMeta::privateHint()`:

| Nơi hiện | Điều kiện | Câu |
|---|---|---|
| Push điện thoại | prefix có trong `APP_SCREEN_PREFIXES` (app ĐÃ có màn) | `Mở ứng dụng để xem chi tiết` |
| Push điện thoại | loại mới chỉ làm trên **web**, app chưa có màn | `Xem chi tiết trên web` |
| Toast web (`NotificationSocket`, `push($data, true)`) | mọi loại nhạy cảm | `Bấm để xem chi tiết` |

Lý do: trước đây mọi loại đều ghi "Mở ứng dụng…", nhưng Quyết định / bảo hiểm / hồ sơ / thu chi chưa có màn trên app —
bấm vào app lại báo "chưa có trên app, xem trên web", 2 câu nói ngược nhau.

- **Làm loại nhạy cảm mới chỉ có trên web** → chỉ khai `SENSITIVE_PREFIXES`, **KHÔNG** thêm vào `APP_SCREEN_PREFIXES`
  (tự ra "Xem chi tiết trên web").
- ⚠️ **Sau này làm màn đó trên app** (thêm `case` trong `notification_router.dart`) → **PHẢI thêm prefix vào
  `APP_SCREEN_PREFIXES`** cùng lúc. Quên thì push vẫn bảo xem trên web dù app đã mở được. Hiện có: `DXN`, `DMVS`, `BL`.

---

## 7. Bấm vào mở đúng màn — `type` + `id` + `url`

- `url` (web) dẫn thẳng màn xử lý, **luôn kèm ID** (`/assign/tasks?open_task=123`). Không trỏ về danh sách trống.
- `type` = **loại của đúng đối tượng**. CẤM mượn type của loại khác vì "đã có sẵn" — đã sửa ~30 chỗ mượn
  `lateInEarlyOutApprove` / đơn nghỉ / khen thưởng khiến app mở nhầm màn (02/11/2026).
- `id` = id của **chính phiếu đó** (không phải id nhân viên). Thông báo bình luận kèm `comment_id`.
- App (TPE_APP) mở theo `type`/`id` ở `ui/notification/notification_router.dart`. Type chưa có màn trên app → app vẫn
  mở + báo "Nội dung này chưa có trên app, vui lòng xem chi tiết trên web" — type mới mà app có màn thì thêm `case`
  (skill `app-notification`).
- Trường thêm vào `data` phải nằm trong allowlist của `EmployeeInfoService::sendNotification` (đã có `push_title`,
  `push_body`, `comment_id`), không thì bị lọc mất.

---

## 7b. Số trên icon app (badge) + đánh dấu đã đọc khi bấm push (06/11/2026)

- Push luôn gửi kèm **số chưa đọc** của người nhận (iOS `aps.badge`, Android `notification_count`) —
  `App\Support\NotificationBadge::unreadCount()` + `FCMService::setBadge()`, đã nối sẵn trong `SendNotification` và
  `Rice\SendMobileNotification`. Đếm cùng cách số chuông (2–3 ms trên bảng 637k dòng PROD, chạy trong job nền).
- Đường gửi mới tự dispatch job push → đặt `$notificationData['notification_id'] = $notification->id` (id dòng
  `notifications`) trước khi dispatch: app dùng để đánh dấu đã đọc khi bấm push, và job cộng thêm 1 nếu dòng chưa kịp ghi.
- Tự gọi `FCMService` ngoài 2 job trên → `setBadge(NotificationBadge::unreadCount($infoId, $notificationId))`.
- Phía app: skill `app-notification` mục 2c.

## 8. Cách implement

**BE** — chỉ dùng helper chung:

```php
EmployeeInfoService::sendNotification($employeeInfoId, NotificationMeta::build(
    NotificationMeta::CHAM_CONG, 'DXN', 'Đã duyệt', 'Đơn nghỉ 21/10 – 22/10', 'Người duyệt: Nguyễn Hữu Học'
) + ['url' => '/timesheet/attendance/123', 'type' => 'attendance', 'id' => 123]);
// nhiều người nhận: EmployeeInfoService::sendToAllNotification($ids, $data)
```

- Luồng **tự gửi** không qua `sendNotification` (job riêng, Rice, Payroll, đồng bộ khuôn mặt…) PHẢI gửi socket bằng
  `NotificationSocket::publish($employeeInfoId, $data, $notification->id)` — đặt `$notification->id = Str::uuid()` trước
  `notify()` để toast bấm mở được đúng dòng. **Cấm `Redis::publish('user_notification_…')` tay** (toast thiếu câu, thiếu id).
- Gọi từ Console Command / cron phải truyền người gửi (auth null → mất thông báo im lặng).
- Server dev / prod chạy **PHP 8**: không dùng `array_filter($x, 'strlen')` (null → Deprecated) — dùng `NotificationMeta::filled`.
- Đổi `NotificationMeta` / job gửi xong, trên server phải `php artisan queue:restart` (worker giữ code cũ).

**FE web**: chỉ hiển thị field BE trả (`headline`, `note_text`, `toast`). Danh sách: `components/notification/NotificationItem.vue`;
toast: `utils/notificationToast.js` (gọi từ `components/BasicSubsystem.vue`); màu hành động: `utils/notificationDisplay.js`.

**App**: model đọc `headline` / `note_text`; xem skill `app-notification`.

---

## 9. Không nhầm với thông báo kiểm tra dữ liệu (Validation)

| Tình huống | Cách hiển thị |
|---|---|
| Trống dữ liệu / sai định dạng / vượt độ dài / trùng dữ liệu | Lỗi **inline dưới trường** (không popup) |
| Ràng buộc nhiều trường | Toast/alert chung + inline nếu xác định được trường |
| Không đủ quyền | `QLDA_012` — "Bạn không có quyền thực hiện chức năng này." |
| Không thể xóa do đang được sử dụng | `QLDA_015` — "Không thể xóa do dữ liệu đang được sử dụng." |
| Lỗi hệ thống | `QLDA_010` — "Đã xảy ra lỗi hệ thống. Vui lòng thử lại." |

---

## Checklist trước khi báo xong task có thông báo

- [ ] Dựng bằng `NotificationMeta::build()`; nhóm hành động nằm trong mục 2
- [ ] Tên là tên riêng, không lặp tên loại; ghi chú dùng đúng nhãn mục 4, chữ tự do để cuối
- [ ] Prefix mới đã khai `OBJECT_LABELS` (loại nhạy cảm → `SENSITIVE_PREFIXES`)
- [ ] Loại nhạy cảm: app có màn mở được thì thêm vào `APP_SCREEN_PREFIXES`, chưa có thì KHÔNG (mục 6)
- [ ] Tự dispatch job push → có `notification_id` trong `$notificationData` (mục 7b)
- [ ] `type` đúng loại đối tượng, `id` = id phiếu, `url` có ID
- [ ] `push_title` riêng (nếu có) ≤ 28 ký tự
- [ ] Gửi qua `sendNotification` / `NotificationSocket::publish`, không `Redis::publish` tay
- [ ] 2 lệnh tự kiểm (chạy từ `HRM/`) đều in RỖNG:
      `python3 .claude/skills/notification-convention/scripts/check_prefix_labels.py`
      `python3 .claude/skills/notification-convention/scripts/check_push_titles.py`
- [ ] Xem thử câu ra ở 3 nơi: tinker `NotificationMeta::push($data)` và `NotificationMeta::display($data)`
