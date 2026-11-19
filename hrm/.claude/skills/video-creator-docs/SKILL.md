---
name: video-creator-docs
description: Use when user asks to make a screen-recorded tutorial VIDEO (video hướng dẫn sử dụng, quay màn hình, video demo tính năng, video HDSD) for an ERP TPE / hrm-client screen — Playwright tự thao tác theo kịch bản, chú thích tiếng Việt trên màn, giọng đọc AI tiếng Việt, xuất mp4. Also when re-recording or fixing such a video (popup tắt trước khi nói xong, thiếu chức năng, không có tiếng, giọng máy, file quá nặng để gửi).
---

# Video hướng dẫn sử dụng — ERP TPE (chốt 30/10/2026)

Quay bằng **Playwright tự thao tác theo kịch bản** (không quay tay), ghép **giọng đọc AI tiếng Việt**, xuất **mp4**. Mẫu chạy
thật: `assets/record-mau-phan-quyen.js` (video phân quyền, 79 bước, 8'27") + `assets/build.py`. Bắt đầu bằng cách copy 2 file
này rồi thay mảng `steps`.

## 1. Quy ước nội dung (user đã chốt — bắt buộc)

| # | Quy ước |
|---|---|
| 1 | **Câu mở đầu cố định:** `Xin chào. Các bạn đang xem video hướng dẫn sử dụng Phần mềm quản trị ERP TPE.` — rồi 1 câu nói video hướng dẫn những gì |
| 2 | **Câu kết cố định:** `Cảm ơn các bạn đã xem video!` (trước đó 1 câu tóm tắt "Đó là các chức năng chính của …") |
| 3 | **Vào màn bằng MENU như người dùng thật**, không `goto` URL (trừ trang chủ lúc chuẩn bị). Ví dụ phân hệ Quản trị: trang chủ → bấm **Quản trị** ở vòng tròn giữa → rê chuột thanh menu trái → nhóm → chức năng. Màn con mở bằng đúng nút trên giao diện (biểu tượng khiên ở cột Hành động, bấm mã ở danh sách…) |
| 4 | **Nói ĐỦ mọi chức năng có trên màn hình** — mọi nút thanh công cụ (Cài đặt bộ lọc, Tìm kiếm nâng cao, Tìm kiếm, Làm mới, Thêm mới, Cấu hình cột, Xuất Excel…), mọi popup (mở ra, giới thiệu từng phần, rồi đóng), menu ⋮ của dòng, phân trang, các khối trên màn chi tiết, footer. Thiếu "Cài đặt bộ lọc" từng bị user bắt lỗi ⇒ **luôn kiểm kê trước khi viết kịch bản** (mục 3) |
| 5 | **Màn hình / popup KHÔNG được đóng trước khi nói xong câu giới thiệu về nó.** Đóng popup là **một bước riêng có lời** ("Bấm Đóng để quay lại." / "Ở đây mình bấm Hủy.") |
| 6 | **Mặc định chỉ xem, không bấm Lưu** (popup thêm/sửa/xác nhận đều Đóng/Hủy). Lời đọc nói rõ "Trong video này mình không lưu, để giữ nguyên dữ liệu." Muốn quay luồng lưu thật ⇒ hỏi user + dùng DB demo |
| 7 | Rời màn còn thay đổi chưa lưu ⇒ hộp "Thông tin chưa lưu" hiện ra: **biến thành 1 bước hướng dẫn** (nói hệ thống hỏi lại, bấm Thoát), đừng để nó chặn kịch bản |
| 8 | Lời thoại câu ngắn, văn nói ("Muốn xem nhanh…, bạn bấm vào…"), gọi **đúng chữ trên giao diện** |

## 2. Quy ước kỹ thuật

- **Khung hình** 1600×900, chú thích chữ trắng nền tối ở đáy (`#__cap`), nhãn chương xanh góc phải trên (`#__chap`), **chấm đỏ
  chuột giả** (headless không có con trỏ), **khung vàng** tô phần đang nói (`mark()`), ~2–4 giây.
- **Động cơ đồng bộ theo BƯỚC** (`steps = [{ ch, cap?, say, act? }]`): `act` chạy lúc bắt đầu bước, bước sau chỉ bắt đầu khi lời
  của bước trước đọc xong (+ nghỉ 0,35s). Mỗi bước 1 file lời ⇒ mốc lời = mốc bước ⇒ hình luôn khớp lời. **Không** dùng kiểu
  "cảnh dài chạy song song lời" — thao tác chạy nhanh hơn lời, popup bị đóng khi đang nói (lỗi user bắt 30/10).
  Thao tác "bấm sau khi nói" ⇒ đặt vào `act` của bước KẾ TIẾP.
- **Giọng đọc:** `edge-tts` giọng **`vi-VN-HoaiMyNeural`** (nữ, tự nhiên), `--rate=+4%`. Giọng nam `vi-VN-NamMinhNeural` lỗi
  không trả tiếng (30/10) — đừng dùng. Dịch vụ hay từ chối khi gọi dồn ⇒ **đọc TỪNG CÂU, thử lại có chờ (≤16 lần, chờ tăng dần),
  cache theo md5 câu** (`tts-cache/`), ghép câu với khoảng lặng 0,25s. Cài: `python3 -m venv ttsenv && ttsenv/bin/pip install edge-tts`.
  ⚠️ Lời thoại được gửi lên dịch vụ Microsoft — chỉ chữ hướng dẫn, KHÔNG nhét dữ liệu khách/nhân viên vào lời; lần đầu hỏi user.
  Phương án offline: `say -v Linh` (giọng máy, user chê không tự nhiên).
- **Âm thanh xuất:** AAC **stereo 48kHz** 192k, `volume=1.15,alimiter=limit=0.89` (đỉnh ≈ -1 dB). Mono 44,1kHz bị khung xem
  trước của app phát im lặng (user báo "chưa có tiếng" dù file có tiếng).
- **Video:** H.264 `crf 22`, `yuv420p`, `+faststart`. Đoạn tải trang lúc chuẩn bị ghi vào `cuts` rồi **cắt khỏi video**, lời dời
  theo mốc mới (`build.py`).
- **Gửi file:** giới hạn gửi 30MB ⇒ thêm bản nén `-crf 27 -preset slow` đặt tên `*-ban-nhe.mp4`; bản đầy đủ giữ trong thư mục.
- **Nơi lưu:** `.plans/<feature>/video/` (`gop_db` ⇒ `.plans/gop-db/<feature>/video/`): `huong-dan-<tên>.mp4`, bản nhẹ,
  `record.js`, `build.py`. Quay lại = sửa `steps` + chạy lại (lời đã cache ⇒ vài phút).
- **Công cụ:** Playwright lấy từ `HRM/e2e/node_modules`, chạy Node 20:
  `NODE_PATH=<HRM>/e2e/node_modules PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" node record.js` rồi `python3 build.py`.
  Cần `ffmpeg` (`brew install ffmpeg`). Đăng nhập: JWT tài khoản test cấp qua tinker (không ghi DB), nhúng bằng `addInitScript`.
  Đóng trình duyệt Playwright MCP trước khi quay (Nuxt dev mở 3 tab là treo).

## 3. Quy trình

1. **Hỏi** (1 lần): môi trường/DB quay (dữ liệu thật sẽ hiện tên/email — có chia sẻ ra ngoài không?), có lưu thật không, giọng.
2. **Kiểm kê màn** bằng Playwright MCP: liệt kê mọi `button`/`[title]` hiển thị, ô tìm nhanh, ô lọc nâng cao, cột, hành động
   dòng, menu ⋮, nội dung từng popup (mở rồi đọc `.modal.show`), các khối màn chi tiết. Ghi thành checklist ⇒ mỗi mục ≥1 bước.
3. **Viết `steps`** theo checklist + quy ước mục 1. Mỗi popup = bước mở (giới thiệu) → các bước giới thiệu phần bên trong → bước đóng.
4. **Quay** (chạy nền, ~1 phút quay/1 phút video + thời gian tạo lời lần đầu). Đọc log: bước nào in `Bước N lỗi` là thao tác hỏng
   ⇒ sửa locator, quay lại.
5. **Kiểm trước khi gửi** (đo, đừng đoán):
   - khung hình **0,4s trước mỗi bước đóng popup** ⇒ popup phải còn mở;
   - khung hình đầu mỗi chương / sau mỗi lần chuyển trang ⇒ không còn vòng xoay tải;
   - câu chào đầu, câu kết; `ffmpeg -af volumedetect` có tiếng, đỉnh < 0 dB; `ffprobe` audio 2 kênh 48kHz.
   - Ghép khung thành lưới (`xstack`) để xem 1 lần.
6. Gửi bản nhẹ (SendUserFile), mở Finder bản đầy đủ (`open -R`), dặn **mở bằng QuickTime** để nghe tiếng.

## 4. Bẫy đã gặp

| Triệu chứng | Nguyên nhân / cách làm |
|---|---|
| Bấm nhầm ô lọc đầu trang | `row.locator('.a, .b')` — dấu phẩy trần bị tách thành selector TOÀN TRANG ⇒ dùng `row.locator(':is(.a, .b)')` |
| Không tìm thấy dòng theo tên | `td` có khoảng trắng/xuống dòng quanh chữ ⇒ regex `^Tên$` trượt; dùng `getByRole('button', { name, exact: true })` (ô tên là nút) |
| `getByText(/^Tiêu đề…/)` không ra | text có icon/khoảng trắng ⇒ dùng chuỗi thường trong vùng hẹp: `page.locator('.er-main').getByText('Tiêu đề')` |
| Click ô tick báo "không nhìn thấy" | label của `V2BaseCheckbox` không chữ đo 0×0 ⇒ `locator.evaluate(e => e.click())` |
| `scrollIntoViewIfNeeded` treo 30s | phần tử cao hơn khung nhìn ⇒ `evaluate(e => e.scrollIntoView({ block: 'center' }))`; `block: 'start'` bị thanh trên che |
| Nút "Tìm kiếm" khớp 2 nút | "Tìm kiếm nâng cao" cũng chứa chữ ⇒ `button.v2-btn--primary` hoặc regex `/^\s*Tìm kiếm\s*$/` |
| Ô select2 option "— Không … —" không chọn được | select2 ẩn option `id=''` (coi là placeholder) — xem memory select2 |
| Hộp xác nhận chặn chuyển menu | `unsavedChangesMixin` ⇒ bước riêng bấm `Thoát` (quy ước 7) |
| Lời TTS lỗi `NoAudioReceived` ngẫu nhiên | do gọi dồn, không phải nội dung ⇒ đọc từng câu + thử lại + cache |
| "Chưa có tiếng" | mono/44,1k hoặc khung xem trước tắt tiếng ⇒ stereo 48k + mở QuickTime |
| Gửi file bị từ chối | > 30MB ⇒ bản nén crf 27 |
| Chữ "QUẢN TRỊ" không bấm được | CSS viết hoa, DOM là "Quản trị" ⇒ `getByText(/^\s*Quản trị\s*$/i)` |
