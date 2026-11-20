# App nhận chia sẻ (share extension) — @cuong61n

> Trạng thái: user ĐÃ DUYỆT thiết kế (20/11/2026). Plan chi tiết: `docs/superpowers/plans/2026-11-20-app-share-extension.md`. Đang làm Android (Task 1–4 xong, Task 5–6 còn), iOS chưa bắt đầu.

## Phase 0 — Thiết kế
- [x] 2026-11-20 Khảo sát hiện trạng (share_plus chỉ gửi ra; iOS 1 target, chưa App Group; Android chưa intent-filter; token `encrypted_shared_preferences`, refresh xoay vòng; PROD JWT_TTL=null; nginx 50M)
- [x] 2026-11-20 Viết spec + người đọc độc lập soát, xử lý 8 câu hỏi
- [x] 2026-11-20 User duyệt spec
- [ ] Chờ user: ai tạo App ID extension / App Group / bật Siri + App Groups + Keychain Sharing / làm mới profile (chặn phần iOS chạy máy thật)

## Phase 1 — Android (không cần ký) — dự kiến
- [ ] `ShareReceiverActivity` + intent-filter SEND/SEND_MULTIPLE, màn Flutter cửa sổ share, gửi qua `ChatApiService`
- [ ] Sharing Shortcuts (hàng phòng gợi ý)

## Phase 2 — iOS Mốc 1 (extension + danh sách phòng trong cửa sổ) — dự kiến
## Phase 3 — iOS Mốc 2 (hàng gợi ý `INSendMessageIntent`) — dự kiến
## Phase 4 — Cập nhật quy trình build TestFlight (2 profile) — dự kiến

## Tiến độ code (2026-11-20) — @cuong61n
- [x] Task 1 `lib/ui/share/share_payload.dart` + test (8): gộp tiêu đề+link, tệp, phòng chọn sẵn
- [x] Task 2 `lib/ui/share/share_sender.dart` + test (10): upload + gửi, giới hạn 10 tệp / 50MB, nhớ tệp đã upload, chống gửi trùng, ánh xạ 401/4xx/mạng
- [x] Task 3 `lib/ui/share/share_window_page.dart` + `lib/main_share.dart` + test (7) — tổng 25 test `test/ui/share` qua; `shareMain` khai trong `lib/main.dart` (engine chỉ tìm hàm vào ở thư viện gốc)
- [x] Task 4 Android `ShareReceiverActivity.kt` + `src/tpeProd/AndroidManifest.xml` + `ShareTheme`: build tpeProd OK; flavor etek build OK và KHÔNG có activity. Chạy emulator Android 10 (trỏ API local qua `--flavor tpeProd --dart-define=FLAVOR=tpeLocal --dart-define=APP_API_BASE_URL=http://10.0.2.2:8003/api/`): chia sẻ văn bản+link → tin 618 phòng 74 đúng người/nội dung; chia sẻ ảnh → tin 619, 620 kèm tệp (bảng `files`), cửa sổ tự đóng, không mở app.
- [x] Sửa lỗi gặp khi test: (1) engine báo "Could not resolve main entrypoint" vì hàm vào ở thư viện không phải gốc; (2) một tệp không đọc được làm mất cả phần chữ → giờ lỗi từng tệp, phần còn lại giữ.
- [ ] Task 5 Sharing Shortcuts (hàng phòng gợi ý Android) — chưa làm
- [ ] Task 6 ma trận Android còn thiếu: nhiều ảnh (SEND_MULTIPLE), 11 tệp, tệp >50MB, chưa đăng nhập, mất mạng giữa chừng, app tắt hẳn, chọn từ hàng gợi ý
- [ ] Task 7–10 iOS + ký + build TestFlight — chưa làm (cần Apple Developer)
- Lưu ý: API local đẩy tệp lên S3 thật (`tanphat.s3.cloud.cmctelecom.vn`) — đã có 2 ảnh test 2,7KB (`qa-share-0png…`, `qa-share-1png…`).
- Lưu ý: emulator Android `Pixel_4_API_29` trước đó chạy ẩn (`-no-window`) từ phiên cũ; 20/11 khởi động lại có cửa sổ để user xem.
