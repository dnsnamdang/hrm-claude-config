# Chat + Agent trên app mobile — phân tích App / Web (17/11/2026)

> Trạng thái: PHÂN TÍCH, chờ user chốt. Chưa vẽ, chưa code.
> Nguồn: đọc code `origin/gop_db` (client 823561986 · api 07953fb30) + app TPE_APP `develop` 9fa648e.
> Yêu cầu user 17/11: bỏ bản thiết kế cũ (KG-01…24, mô hình "Không gian" 05/11) · thiết kế theo logic mới nhất gop_db ·
> trục chính là các NHÓM CHAT, Nhiệm vụ / Meeting / Vấn đề là tab tuỳ chỉnh · chat là phần độc lập, truy cập nhanh từ mọi màn
> (như ngăn trượt web) · giao diện dễ nhìn, thoáng · chỉ vẽ khi user chốt.

## 1. Hiện trạng

**Web (gop_db, đã chạy prod TPE):**
- Hội thoại: nhóm (thường / Dự án TKT / Xây dựng GP) + chat 1–1 (mọi NV mọi công ty). Dòng TPE SMART AGENT ghim đầu danh sách.
- Mở từ mọi trang bằng nút topbar → ngăn trượt `ChatDrawer` (đủ chức năng như trang `/assign/messages`).
- Nhóm: 3 vai trò Quản lý / Thành viên / Xem; tab Trò chuyện (luôn có) · Nhiệm vụ (bật/tắt) · Meeting (bật/tắt) · Thành viên;
  BE đã có sẵn `issues`, `files` trong `OPTIONAL_TABS` nhưng UI chưa bật (Vấn đề v2 đang làm — tab nhóm là Phase 3).
- Agent: 45 công cụ chỉ đọc, 12 loại khối kết quả, thẻ chọn khi trùng tên, thẻ mở panel, thẻ thiếu quyền; trả lời qua socket `agent` + poll.

**App (TPE_APP):** chưa có màn chat nào, chưa có thư viện socket. Push `chat_message` đang đẩy tới máy nhưng app rơi vào nhánh
"xem trên web". `PrimaryAppBar` tự gắn chuông thông báo ở MỌI màn. Mỗi phân hệ có khung riêng: thanh dưới (tab) + nút tròn giữa
(FAB) + drawer. App đã có: Nhiệm vụ (danh sách / chi tiết / form / kết quả), Vấn đề, Meeting hub, Việc của tôi / nhắc việc.

## 2. Đề xuất phân chia App / Web

Ký hiệu: ✅ có trên app · ◐ có nhưng rút gọn · ⛔ chỉ web.

### 2.1 Danh sách hội thoại
| Tính năng | App | Ghi chú |
|---|---|---|
| Danh sách nhóm + 1–1, khối Đã ghim, dòng Agent ghim đầu | ✅ | |
| Chip lọc Tất cả · Chưa đọc · Nhóm · Cá nhân + tìm | ✅ | chip 1 hàng, cuộn ngang nếu cần |
| Badge chưa đọc, @, chấm "đánh dấu chưa đọc", 🔕, mã công ty, đang soạn, bản nháp | ✅ | |
| Ghim / Đánh dấu đọc / Tắt thông báo / Rời nhóm | ✅ | nhấn giữ dòng → bottom sheet (thay menu ⋮) |
| Tin nhắn mới (Danh bạ mọi công ty) | ✅ | |
| Tạo nhóm | ⛔ / ◐ | **cần chốt — mục 4.4** |
| Cài đặt âm thanh / thông báo trình duyệt | ⛔ | app dùng cài đặt thông báo của máy |

### 2.2 Trong hội thoại
| Tính năng | App | Ghi chú |
|---|---|---|
| Tin chữ, trả lời, @ (≤200), @all, emoji, sticker, biểu cảm | ✅ | |
| `#` chèn nhiệm vụ (nhóm bật tab Nhiệm vụ) | ✅ | |
| Ảnh / tệp (≤10, 25MB) | ✅ | thêm **Chụp ảnh bằng camera** (riêng app) |
| Chỉnh ảnh trước khi gửi (cắt / vẽ / làm mờ) | ◐ | chỉ cắt + xoay (đợt sau có vẽ) — đề xuất |
| Chụp màn hình, kéo thả, dán ảnh, phím tắt | ⛔ | không có trên điện thoại |
| Thanh thao tác khi rê chuột | ✅ đổi dạng | **nhấn giữ tin → sheet**: hàng biểu cảm + Trả lời · Chia sẻ · Sao chép · Ghim · Tạo nhiệm vụ · Tạo nhắc việc · Sửa/Thu hồi (24h) · Xoá phía tôi |
| Thanh tin ghim (≤20) + tìm tin trong hội thoại | ✅ | |
| Thẻ nhiệm vụ, tin hệ thống (đổi trạng thái NV, lịch họp) | ✅ | bấm → mở **màn có sẵn của app** (chi tiết nhiệm vụ / meeting), không vẽ panel mới |
| Đã xem (1–1), đang soạn, trực tuyến | ✅ | |
| Khối báo lỗi (YC hỗ trợ) | ✅ xem | chỉ hiển thị, không gửi từ app (xem 2.5) |
| Bản nháp | ✅ | web lưu localStorage; app lưu trên máy (không đồng bộ) — đồng bộ qua API là việc BE riêng |
| Popup hồ sơ: Nhắn tin · Gọi · Email | ✅ | Gọi `tel:` trên app là bấm gọi thật — hợp app hơn web |

### 2.3 Nhóm trao đổi
| Tính năng | App | Ghi chú |
|---|---|---|
| Tab Trò chuyện · Nhiệm vụ · Meeting (chỉ hiện tab nhóm đã bật) | ✅ | Vấn đề thêm khi web xong Vấn đề v2 Phase 3 |
| Tab Nhiệm vụ: danh sách việc của nhóm, tạo nhiệm vụ | ✅ | dùng lại danh sách + form nhiệm vụ của app |
| Tab Meeting: Sắp họp / Đã họp / Đã huỷ, Tạo meeting | ✅ | dùng lại form meeting của app |
| Ảnh · Tệp · Link của nhóm | ✅ | gom vào màn **Thông tin nhóm** (không thành tab) |
| Thành viên: xem, tìm, Nhắn riêng | ✅ | trong màn Thông tin nhóm |
| Quản lý thêm người lẻ / đổi vai trò / mời ra **từng người** | ◐ | **cần chốt — mục 4.5** |
| Thêm theo phòng ban / cả công ty, chọn hàng loạt | ⛔ | |
| Sửa tên/mô tả/thời hạn, bật/tắt tab, gắn Dự án KH | ⛔ | thao tác cấu hình, ít dùng |
| Đóng / Mở lại nhóm | ⛔ | việc hệ quả lớn (chuyển lưu trữ, chỉ đọc) |
| Rời nhóm | ✅ | |
| Chế độ chỉ đọc (vai trò Xem, nhóm đóng, người nghỉ việc) | ✅ | dải báo thay ô soạn |

### 2.4 TPE SMART AGENT
| Tính năng | App | Ghi chú |
|---|---|---|
| Hỏi – đáp, chữ chạy dần, thẻ các bước (thu gọn) | ✅ | |
| Hội thoại mới + Lịch sử | ✅ | |
| Câu gợi ý màn chào + chip gợi ý | ✅ | gợi ý màn chào giảm còn 4 câu, 1 cột |
| Khối kết quả: tasks, meetings, meeting, rank, bars, pick, rooms, bookings, leave, requests, payslip | ✅ | dạng thẻ dọc, không bảng ngang |
| Khối `timesheet` (6 ô / hàng) | ◐ | 3 ô / hàng |
| Thẻ chọn khi trùng tên | ✅ | |
| Thẻ mở Nhiệm vụ / Vấn đề / Meeting / Phiếu / Nhắc việc | ✅ | mở màn có sẵn của app; KH / TKT / Giải pháp / đơn app chưa có màn ⇒ ghi "Xem trên web" |
| Thẻ thiếu quyền + "Hỏi trong phạm vi của tôi" | ✅ | |
| Dòng chi phí token / ₫ dưới mỗi câu | ⛔ | đề xuất bỏ trên app cho thoáng (đã có ở panel) |
| Panel "Phân quyền của Agent" | ◐ | sheet: Hạn mức hôm nay + Quyền liên quan; bỏ nhật ký |
| Thống kê, Cài hạn mức, Chọn model, Nhật ký lượt hỏi | ⛔ | quản trị, bảng nhiều cột |

### 2.5 Khác
| Tính năng | App | Ghi chú |
|---|---|---|
| Push FCM tin nhắn (trễ 20s, gộp theo hội thoại) | ✅ | bấm push **mở thẳng hội thoại** (app phải xử lý `data.type='chat_message'`) |
| YC hỗ trợ (tab báo lỗi mép phải, tự chụp trang + gom lỗi API) | ⛔ | đợt sau nếu cần: lắc máy để báo lỗi |
| Gọi thoại / video | ⛔ | user đã bảo làm sau |
| `@Agent` trong nhóm | ⛔ | web cũng chưa có |

## 3. Nguyên tắc giao diện "dễ nhìn, thoáng" (đề xuất)
- Màn danh sách: mỗi dòng 72px, avatar 48, tên 16 đậm + 1 dòng tin cuối 14 xám; không dòng phụ thứ 3.
- Header hội thoại 1 hàng: ‹ · avatar · tên (+ trạng thái / số thành viên) · 🔍 · ⓘ. Thông tin phụ dồn vào màn Thông tin.
- Dải tab nhóm chỉ hiện tab đã bật; nhóm chỉ có Trò chuyện thì KHÔNG có dải tab.
- Bong bóng chữ 16, khoảng cách giữa cụm tin 12; tin hệ thống là viên xám mờ ở giữa (như GĐ32).
- Ô soạn 1 hàng: [+] · ô nhập · 😊 · gửi. Mọi đính kèm / tạo nhanh nằm trong sheet [+].
- Thao tác dồn vào bottom sheet; nút trong sheet có icon, Huỷ / Đóng luôn cuối (quy ước app).
- Màu: accent theo app hiện tại; trạng thái nhiệm vụ lấy màu BE như web.

## 4. Điểm cần user chốt

### 4.1 Lối vào nhanh từ mọi màn
- **PA1 (đề xuất)** — icon 💬 có badge số chưa đọc đặt cạnh chuông trên `PrimaryAppBar` (thanh trên đã hiện ở mọi màn), bấm mở
  Chat **toàn màn** (đẩy lên, nút ‹ quay về đúng màn đang làm). Giống nút topbar web; không đè nút nào.
- PA2 — bong bóng chat nổi góc phải dưới. Luôn trong tầm ngón cái nhưng đè FAB giữa + footer nút của form/danh sách, phải tự ẩn ở
  nhiều màn.
- PA3 — thêm tab "Tin nhắn" vào thanh dưới. Mỗi phân hệ có thanh dưới riêng ⇒ phải thêm vào mọi phân hệ, thanh dưới đã đủ 4 tab + FAB.

### 4.2 Agent đặt ở đâu
- **PA1 (đề xuất)** — dòng ghim đầu danh sách Chat như web; không thêm icon riêng (header chỉ thêm 1 icon).
- PA2 — thêm icon 🤖 riêng trên header cạnh 💬 (1 chạm vào Agent, nhưng header có 3 icon).

### 4.3 Thành viên + Ảnh/Tệp/Link
- **PA1 (đề xuất)** — vào màn **Thông tin nhóm** (bấm tên nhóm / ⓘ): Thành viên · Ảnh · Tệp · Link · Rời nhóm. Dải tab chỉ còn
  việc: Trò chuyện · Nhiệm vụ · Meeting (· Vấn đề).
- PA2 — giữ Thành viên là 1 tab như web (dải tab dài hơn, tab cuối có thể khuất).

### 4.4 Tạo nhóm trên app
- **PA1 (đề xuất)** — chỉ web. Form có chọn theo phòng ban / cả công ty / 3 vai trò / gắn Dự án KH — dồn lên điện thoại sẽ dài và rối;
  tạo nhóm cũng không gấp như nhắn tin.
- PA2 — app tạo nhóm rút gọn: Tên + chọn người lẻ (người tạo là Quản lý, người được chọn là Thành viên); phần còn lại sửa trên web.

### 4.5 Quản lý thành viên trên app
- **PA1 (đề xuất)** — Quản lý thêm người lẻ, đổi vai trò, mời ra **từng người** (nhấn giữ dòng thành viên); hàng loạt + theo phòng ban chỉ web.
- PA2 — app chỉ xem + nhắn riêng; mọi thay đổi thành viên ở web.

### 4.6 Tab Vấn đề
- **PA1 (đề xuất)** — vẽ luôn tab Vấn đề trong nhóm (bám Vấn đề v2 đang làm, tab hiện khi nhóm bật), ghi rõ "phụ thuộc web Phase 3".
- PA2 — chưa vẽ, đợi web xong Phase 3.

## 5. Ngoài phạm vi thiết kế nhưng phải làm khi code app (ghi lại)
- App cần socket client (sự kiện `chat`, `presence`, `agent`) — hiện chưa có thư viện.
- Xử lý push `chat_message` mở thẳng hội thoại (hiện rơi vào "xem trên web").
- Bản nháp + cài đặt thông báo đang ở localStorage web ⇒ muốn đồng bộ web/app phải thêm API (nguyên tắc đa nền tảng README §0).
- Agent "Đề nghị cấp quyền" web mới là toast "giai đoạn sau" ⇒ app vẽ theo đúng hiện trạng.
- Màn đích của thẻ Agent: KH / Dự án TKT / Giải pháp / đơn — app chưa có màn ⇒ "Xem trên web".

## 6. Bộ màn dự kiến (sau khi chốt) — ~18 màn, đặt khu mới trong `meeting-mobile.pen`, xoá KG-01…24 cũ
1. Màn bất kỳ có icon 💬 + badge · 2. Danh sách hội thoại · 3. Nhấn giữ dòng → sheet · 4. Danh bạ / tin nhắn mới ·
5. Chat 1–1 · 6. Chat nhóm (tab) đủ trạng thái (ghim, trả lời, @, thẻ NV, tin hệ thống, đã xem) · 7. Nhấn giữ tin → sheet ·
8. Sheet [+] đính kèm / tạo nhanh · 9. Gợi ý @ và # · 10. Emoji / sticker · 11. Tab Nhiệm vụ của nhóm · 12. Tab Meeting ·
13. Thông tin nhóm (thành viên, ảnh/tệp/link) · 14. Hồ sơ người · 15. Chỉ đọc (vai trò Xem / nhóm đóng) ·
16. Agent màn chào · 17. Agent đang trả lời + khối kết quả + thẻ chọn · 18. Agent thẻ thiếu quyền + sheet hạn mức/lịch sử.
