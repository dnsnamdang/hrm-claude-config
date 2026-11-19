# Video hướng dẫn app mobile — Meeting + thông báo thật

Người phụ trách: @namdangit · Bắt đầu 01/11/2026 · Skill nền: `.claude/skills/video-creator-docs` (web) — app dùng lại phần lời đọc + dựng.

## Chốt với user (01/11)
- Quay trên **cổng dev** (dev-hrm.eteksofts.com), app flavor **tpeDev**, được ghi/sửa data dev không giới hạn.
- 2 máy ảo đặt cạnh nhau: trái **namdangit** (chủ trì, máy `D0C0E274-8590-4D39-9196-CD5D535338DD`),
  phải **thuydt.qttt@tanphat.com** (người tham gia, máy `FE6D3E86-49A0-4D92-AFDD-58C5DAF761BB` "iPhone 18 Pro - Thuy"). Thông tin hiện trong video public được.
- Thông báo phải là **push thật** (đã thông 01/11 — cách làm ở memory `video-app-mobile-quay-tren-dev`).
- Giọng edge-tts HoaiMy: user đồng ý ("ok tiếp tục" sau khi hỏi).
- Thông báo "báo chủ trì khi có người xác nhận" CHƯA có trên dev (code local gop_db chưa commit) ⇒ chủ trì xem bằng kéo tải lại.

## Kịch bản (user duyệt 01/11)
1. Mở đầu (câu chào chuẩn) · 2. namdangit Meeting → Tạo meeting → điền → thêm thuydt → Lưu Lên lịch; máy phải banner "Cuộc họp mới"
3. thuydt bấm banner → mở cuộc họp → Xác nhận tham gia: Có mặt · 4. namdangit kéo tải lại tab Nhân sự tham gia thấy "Có mặt"
5. namdangit đổi giờ → máy phải đang khoá nhận thông báo lịch cũ/mới · 6. Chốt lịch → banner "Đã chốt lịch" · 7. Kết (câu kết chuẩn)

## Kỹ thuật
- Điều khiển bằng script gọi `mobilecli` (`~/.npm/_npx/e41f45e886283da6/node_modules/@mobilenext/mobilecli-darwin-arm64/mobilecli-darwin-arm64 io tap|text|swipe|button --device <UDID>`), động cơ theo BƯỚC như skill web (lời đọc xong mới sang bước).
- Quay: `xcrun simctl io <UDID> recordVideo` cả 2 máy cùng lúc → ffmpeg ghép ngang + chú thích + lời.
- Chạy app: `FLUTTER_XCODE_CODE_SIGNING_ALLOWED=YES FLUTTER_XCODE_CODE_SIGNING_REQUIRED=YES FLUTTER_XCODE_CODE_SIGN_IDENTITY=- fvm flutter run --debug -t lib/main.dart --flavor tpeDev --dart-define=FLAVOR=tpeDev -d <UDID>` (từ `TPE_APP/app`).
- Sau khởi động máy: `xcrun simctl boot` 2 máy, mở DeviceHub, kiểm `apsd` có "Connected on 1 interfaces" (kẹt thì kickstart apsd).

## Task
- [x] Thử push thật lên máy ảo (16:01 01/11, banner "Cuộc họp đổi lịch")
- [x] Tạo máy ảo thứ 2
- [ ] Khởi động lại Mac (swap 24,3/24,6GB — app không phản hồi)
- [ ] Cài app 2 máy, đăng nhập (máy 1 đã đăng nhập namdangit; máy 2 đăng nhập thuydt)
- [ ] Kiểm kê màn Tạo meeting / chi tiết / xác nhận / đổi giờ / chốt lịch trên app → toạ độ, nhãn
- [ ] Viết steps + lời → tạo lời TTS → script quay → dựng → kiểm (khung đóng popup, tiếng, đỉnh dB) → bản nhẹ

### Checkpoint — 01/11/2026 19:35
Vừa hoàn thành: video 2 "Đặt phòng họp khi tạo meeting" `video/huong-dan-dat-phong-hop.mp4` (3'53", 9,7MB) + bản nhẹ — phòng tầng 3 duyệt tự động (kèm dịch vụ nước uống) → Đổi phòng sang VIP1 cần duyệt → Thúy nhận push, duyệt trong app → chủ trì nhận push "đã được duyệt", mở phiếu. Quay 2 lần (lần 1: ô tìm kiếm danh sách còn chữ cũ ⇒ mở nhầm cuộc họp).
Đang làm dở: —
Bước tiếp theo: user xem 2 video, góp ý
Blocked: —
Dữ liệu dev: ĐÃ BẬT "cần duyệt" cho Phòng VIP1 (để lại cho các video sau; tắt bằng POST v1/meeting/rooms require_approval=false). Còn lại cuộc họp TPE.MET.NB.26.2263 "Họp kế hoạch quý IV" (Lên lịch, 02/11 09:23) + phiếu DPH-2026-00004 Phòng VIP1 Đã duyệt.

### Checkpoint — 01/11/2026 18:15
Vừa hoàn thành: video đợt 1 `video/huong-dan-meeting-app.mp4` (3'20", 9,2MB) + bản nhẹ; lần quay thứ 5 dùng được (4 lần trước hỏng do bấm theo toạ độ — nay bấm theo OCR). Cảnh màn khoá bỏ (vuốt bị banner chặn) — lời bước 29/31 đã sửa cho khớp hình.
Đang làm dở: —
Bước tiếp theo: user xem video, góp ý → sửa `S` trong record.py, `prep.py && record.py && build.py`
Blocked: —
Dữ liệu dev: cuộc họp quay 2259 "Họp triển khai kế hoạch tháng 11" (Chốt lịch 03/11 21:07); các lần hỏng đã huỷ (2305–2310).

### Checkpoint — 01/11/2026 16:40 (wrap up)
Vừa hoàn thành: push thật lên máy ảo; máy ảo 2 "iPhone 18 Pro - Thuy" đã cài app tpeDev có quyền push (chưa đăng nhập); design.md
Đang làm dở: kiểm kê màn Tạo meeting trên máy 1 (dừng vì cạn RAM); máy 2 chưa cài agent mobilecli ("Agent is not installed") — MCP/mobilecli gọi lần đầu sẽ tự cài hoặc `mobilecli agent install --device <UDID>`
Bước tiếp theo: user khởi động lại Mac → boot 2 máy + DeviceHub → chạy app 2 máy (lệnh mục Kỹ thuật) → đăng nhập thuydt (pass user cung cấp, không ghi ra file) → kiểm kê → viết lời gửi user xem → quay
Blocked: chờ user khởi động lại Mac
Dữ liệu dev đã tạo: cuộc họp thử 2305 "Thử thông báo app" (thuydt chủ trì, namdangit tham gia, đang Chốt lịch 02/11 14:00) — có thể huỷ sau khi quay.

### Checkpoint — 01/11/2026 16:30
Vừa hoàn thành: thông push thật trên máy ảo; tạo máy ảo 2 (đang cài app thì máy cạn RAM)
Đang làm dở: kiểm kê màn Tạo meeting (máy 1 bấm "+ Tạo meeting" không phản hồi do thiếu RAM)
Bước tiếp theo: sau khởi động lại → boot 2 máy → chạy app 2 máy (lệnh ở trên) → đăng nhập thuydt máy 2 → kiểm kê
Blocked: chờ user khởi động lại Mac

## Đợt 3 — Video "Việc của tôi" + Nhắc việc cá nhân (08/11/2026)
Quyết định đã chốt (user 08/11):
- Máy ảo **iOS** iPhone 18 Pro (`D0C0E274-…`), flavor `tpeLocal`, app debug build lại từ đầu trước khi quay, API local
  **cổng 8001** (4 luồng): `fvm flutter run --debug -t lib/main.dart --flavor tpeLocal --dart-define=FLAVOR=tpeLocal
  --dart-define=APP_API_BASE_URL=http://127.0.0.1:8001/api/ -d D0C0E274-8590-4D39-9196-CD5D535338DD`.
  Đã so với Android (profile mượt hơn) nhưng iOS khớp bản vẽ Pen + dùng lại bộ quay `record.py` (mobilecli + simctl + OCR).
- Phạm vi: **toàn bộ nghiệp vụ màn "Việc của tôi"** + **sử dụng Nhắc việc cá nhân**.
- Dữ liệu: DB local, dữ liệu thật — video nội bộ, được hiện tên NV/KH. Tài khoản namdangit (id 13, "DNS Admin").
- **Lưu thật** trên DB local (tạo / sửa / tick bước / xong / gắn liên hệ / xoá nhắc việc).
- Giọng edge-tts `vi-VN-HoaiMyNeural` (lời chỉ có chữ hướng dẫn).
- [x] Kiểm kê chức năng (code) → 11 khu vực (agent 08/11)
- [ ] Chuẩn bị dữ liệu đủ các nhóm
- [x] Viết kịch bản → `video/kich-ban-viec-cua-toi.md` (82 bước, 10 chương); user chốt mục đích: giới thiệu Việc của tôi +
  FULL Nhắc việc cá nhân, các phiếu khác làm video sau
- [ ] Quay `record_mytodo.py` → build → kiểm khung hình → gửi

### Checkpoint — 08/11/2026 23:10
Vừa hoàn thành: kịch bản `video/kich-ban-viec-cua-toi.md`; công cụ dựng lại ở scratchpad (`video-tools/ocr`, `video-tools/ttsenv`
— scratchpad mất khi hết phiên ⇒ dựng lại: `swiftc -O video/ocr.swift -o <dir>/ocr`, `python3 -m venv <dir>/ttsenv &&
<dir>/ttsenv/bin/pip install edge-tts`).
Đang làm dở: —
Bước tiếp theo (user chốt QUAY THỨ HAI 09/11): build lại app từ đầu (lệnh ở mục Đợt 3) → dựng dữ liệu theo ngày quay (cuối
file kịch bản) → viết `video/record_mytodo.py` từ `record.py` (1 máy, OCR bấm theo chữ) → quay thử từng chương dò toạ độ →
quay chính → build.py → kiểm khung hình → gửi bản nhẹ.
Blocked: —

### Bổ sung 08/11/2026 23:30 — user thêm 3 ý
- Kịch bản 92 bước: nhắc gọi khách + liên hệ NHẬP TAY (ch.6), liên hệ CHỌN TỪ DANH BẠ MÁY (ch.6b), bấm Gọi ở màn chi tiết nhắc việc (ch.8).
- Cảnh GỌI: máy ảo iOS báo "Không mở được ứng dụng gọi điện" ⇒ user chốt quay ~10s trên **iPhone thật** rồi ghép vào bước Gọi.
  TestFlight tpeDev 162 (06/11) CHƯA có nút Gọi (code 08/11) + trỏ server dev (chưa có API danh bạ) ⇒ cài thẳng qua cáp:
  `fvm flutter run --release -t lib/main.dart --flavor tpeLocal --dart-define=FLAVOR=tpeLocal
  --dart-define=APP_API_BASE_URL=http://192.168.2.4:8001/api/ -d <iPhone>` (API 8001 nghe 0.0.0.0; iPhone cùng Wi-Fi; IP LAN đổi
  thì lấy lại `ipconfig getifaddr en0`). User bật Ghi màn hình iOS → mở nhắc việc "Gọi điện cho khách…" → Gọi → màn gọi → Kết thúc.
- Vấn đề ngoài luồng (note, chưa sửa): mở chi tiết nhắc việc từ màn Liên hệ, 1–2s đầu hiện "Không hạn" + thiếu khối Liên hệ
  (dữ liệu tạm truyền sang) rồi mới đúng — user chốt ĐỂ NGUYÊN, khi dựng video CẮT khoảng đó (bước mở chi tiết từ màn Liên hệ:
  chờ OCR thấy khối "LIÊN HỆ" rồi mới tính mốc bắt đầu bước, đoạn trước ghi vào `cuts`).

### Bổ sung 08/11/2026 23:55
- Kịch bản bản 2 (127 bước, 11 chương) sau khi đối chiếu tài liệu + code (agent, đã tự kiểm lại: thứ tự nhóm Quá hạn cuối, thêm
  loại tự chọn + đóng sheet, giờ hạn trống, Lưu sửa tự đóng chi tiết, nhắc cá nhân không có "Tự động", tick hết bước tự xong,
  tra KH ≥ 9 số tối đa 5, Gần đây 8).
- Cảnh gọi: user gửi `video/goi-that-iphone.mp4` (9s, 1290×2796 60fps, gọi từ THẺ, khách "A Hoà Tân Phát") — user chốt dùng
  luôn ở chương 7 ⇒ KHÔNG cần cài app lên iPhone nữa.

### Chốt 09/11/2026 00:05 — thông báo trong video
- User: được ghi DB dev local thoải mái ⇒ Báo lịch lãnh đạo bấm **Đồng ý** thật (bước 60–61 sửa lại: Đồng ý → toast
  "Đã lưu và thông báo cho toàn công ty"); dựng sẵn lịch vắng cho chương Lịch lãnh đạo.
- "Video cần hiển thị thông báo đầy đủ": toast có sẵn; chuông: chạy tay `php artisan assign:send-work-reminders` (nhắc việc
  hạn ~15') và `assign:send-work-digest` (bản tin sáng) đúng lúc quay rồi mở chuông → bấm thông báo → Việc của tôi.
- Banner đẩy iOS: user chọn (a) giả lập bằng `xcrun simctl push D0C0E274-… com.tanphat.app payload.apns`, nội dung chép
  ĐÚNG title/body dòng notifications trong DB. Payload cần `gcm.message_id` + các khoá data giống FCM của server để
  FirebaseMessaging nhận là tin FCM (onMessageOpenedApp → `notification_router.dart`) — mai thử 1 lần trước khi quay
  (bấm banner phải mở đúng màn).
- [x] 08/11 23:45 thử banner: build app có ký (`FLUTTER_XCODE_CODE_SIGNING_ALLOWED=YES FLUTTER_XCODE_CODE_SIGNING_REQUIRED=YES
  FLUTTER_XCODE_CODE_SIGN_IDENTITY=- fvm flutter run …`) + Cài đặt máy ảo › Ứng dụng › TPE_LOCAL › Thông báo › BẬT (mặc định
  Tắt ⇒ simctl push báo "Source is not authorized"). Gói APNs dựng bằng `video/tools/push_payload.php` (đúng title/body
  NotificationMeta::push + type/id/notification_id/gcm.message_id) → banner hiện đúng chữ, bấm banner mở đúng màn chi tiết.
- Bộ quay mới: `video/vc.py` (1 máy, bấm theo OCR, cuts, clip) + `video/build_app.py` (bố cục 1 máy + mục lục chương);
  công cụ ở `~/.cache/tpe-video-tools` (ocr + ttsenv), bản thô/cache ở `~/.cache/tpe-video-work`.

### Checkpoint — 09/11/2026 ~01:00 (tự triển khai theo yêu cầu user)
- [x] Dựng dữ liệu `video/tools/prep_mytodo.py` (00:00): 4 nhiệm vụ Đạt→tôi (Hôm nay/Ngày mai/T6/tuần sau), meeting 3074
  "Họp giao ban phòng kinh doanh tuần 46" 14:00 (tôi attendance_status=0 = chưa xác nhận — KHÔNG phải null), nhắc việc 1080–1085
  (Mua VPP, Chị Lan quá hạn có liên hệ, Gửi hồ sơ năng lực đã xong, 2 lịch lãnh đạo). Kết quả: ~/.cache/tpe-video-work/prep_mytodo.json.
- [x] `video/record_mytodo.py` 138 bước / 15 chương, bấm theo OCR; `video/tools/reset.sh` (+ reset_mytodo.php) dọn dữ liệu
  chạy thử về trạng thái sau prep (SINCE 2026-11-09 00:05) + hot restart app.
- Đã đo/ghi nhận khi dò: Bộ lọc là chip (không dropdown); Xóa lọc nằm ngoài màn ⇒ dùng Bộ lọc › Làm mới; xoá ô nhập =
  `mobilecli io keys cmd+a backspace`; ô chọn ngày 2 kiểu (sheet "Chọn ngày hạn" lưới 7×49px + Material ở Ngày bắt đầu lãnh
  đạo); bánh xe giờ: 35–50px = 1 hàng; danh bạ máy hiện "Họ Tên" (Bell Kate); bật lịch lãnh đạo thì HẠN nhắc việc = ngày kết
  thúc lịch ⇒ tách cảnh lãnh đạo ra nhắc việc riêng "Đi công tác TP Hồ Chí Minh…".
- Đang làm: chạy thử trọn 138 bước → sửa → reset → quay chính → build → kiểm khung hình.

### Checkpoint 09/11/2026 — Video "Việc của tôi" HOÀN THÀNH (user duyệt "đã ok")
- File (thư mục video/): `huong-dan-viec-cua-toi.mp4` (16m26s, 42MB) · `-ban-nhe.mp4` (22,6MB, crf 31) · `-x1.25.mp4` (13m09s, 37MB).
- Quay lại: `tools/reset.sh` → `python3 record_mytodo.py` → `NAME=mytodo OUT=huong-dan-viec-cua-toi python3 build_app.py < /dev/null`.
- Bẫy: đoạn 085 (ghép clip iPhone thật) làm ffmpeg treo trong thread pool, chạy lẻ 2,5s ⇒ dựng tay đoạn đó rồi chạy lại build (bỏ qua đoạn đã có).
- Bản 1,25x: audio sau concat copy có khe timestamp ⇒ phải `aresample=async=1` ra wav rồi mới `atempo=1.25` (nếu không tiếng dài hơn hình ~2 phút).
- Còn treo: hướng dẫn build app TPE mới (chờ user chọn tpeDev / tpeProd).
