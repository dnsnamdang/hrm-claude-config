# Video hướng dẫn app mobile — Meeting + thông báo thật (tóm tắt)

Người phụ trách: @namdangit · 01/11/2026 · Plan: `plan.md` cùng thư mục.

## Mục tiêu
Video HDSD tính năng app mobile **giống thật tối đa**, có cảnh **nhận thông báo đẩy thật** (không dựng, không giả lập):
server dev → Firebase (project `tan-phat-erp-hrm`) → Apple (APNs sandbox) → máy ảo iPhone.

## Phạm vi đợt 1
Luồng Meeting giữa 2 người, 2 điện thoại đặt cạnh nhau (≈4–5 phút):
chủ trì (namdangit) tạo họp → người tham gia (thuydt) nhận banner, bấm vào, xác nhận Có mặt → chủ trì tải lại thấy
"Có mặt" → đổi giờ (thông báo trên màn khoá, lịch cũ/mới) → chốt lịch (banner "Đã chốt lịch").

Ngoài phạm vi: cảnh "chủ trì nhận thông báo khi có người xác nhận" — code đó mới ở local gop_db, chưa lên dev
(feature `gop-db/meeting-xac-nhan-tham-gia-bao-chu-tri`). Lên dev rồi có thể quay bổ sung.

## Quyết định đã chốt
| # | Quyết định |
|---|---|
| 1 | Quay trên **cổng dev**, flavor **tpeDev**; được ghi/sửa data dev không giới hạn |
| 2 | Tài khoản namdangit@gmail.com (chủ trì) + thuydt.qttt@tanphat.com (người tham gia); thông tin trong video public được |
| 3 | Giọng edge-tts `vi-VN-HoaiMyNeural` (lời thoại gửi dịch vụ Microsoft — user đồng ý) |
| 4 | Quy ước nội dung theo skill `video-creator-docs` (câu chào/kết chuẩn, vào bằng menu, không đóng màn trước khi nói xong) |
| 5 | Điều khiển máy ảo bằng script gọi `mobilecli`, động cơ theo BƯỚC (lời xong mới sang bước); quay `simctl io recordVideo` 2 máy, ffmpeg ghép ngang |

## Điều kiện kỹ thuật (đã đo)
- Local KHÔNG gửi được push: `FIREBASE_CREDENTIALS` của hrm-api trỏ file không còn + thuộc project prod; tpeLocal Firebase riêng.
- Build simulator mặc định không nhúng `aps-environment` ⇒ phải chạy với `FLUTTER_XCODE_CODE_SIGNING_ALLOWED=YES … CODE_SIGN_IDENTITY=-`.
  Tự `codesign --entitlements` lại .app ⇒ máy ảo giết app (Code Signature Invalid).
- `apsd` trong máy ảo hay kẹt không kết nối ⇒ kickstart lại.
- Máy 16GB: 2 máy ảo + build làm cạn swap ⇒ khởi động lại Mac trước khi quay.
