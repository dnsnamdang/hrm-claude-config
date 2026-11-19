# GĐ8 Chat — Giao diện mới (thoát kiểu Zalo)

> 13/11/2026 · @namdangit · Trạng thái: **MOCKUP + 6 tồn đã chốt (13/11), chờ user duyệt bản mô tả cuối rồi viết plan; chưa code** · Mockup: `mockup-v2.html` (v1 `mockup.html` — user không chọn)

## 1. Mục đích

Bố cục 3 cột đã ổn (hội thoại 360 · khung chat · panel phải 320). User muốn giao diện **hiện đại, ấn tượng hơn, thoát cảm giác
nhìn quá giống Zalo**, và sửa các điểm chưa ưng ở giao diện cũ.

## 2. Quyết định đã chốt (user)

| # | Nội dung | Chốt |
|---|---|---|
| D1 | Thanh lọc Tất cả / Chưa đọc / Nhóm / Cá nhân | **F2 — chip có icon** (chip đang chọn nền navy `#14417e`, icon xanh sáng; số chưa đọc chip đỏ) |
| D2 | Kiểu hiển thị tin | **A — dạng luồng** canh trái kiểu Slack/Linear: avatar + tên + vai trò + giờ, thân tin không bong bóng; tin mình tên màu teal · **14/11 user ĐỔI: kiểu bong bóng — tin mình bên PHẢI nền teal nhạt (không avatar/tên), tin người khác bên trái nền xám nhạt** (đi chung nhánh client `gop_db-chat-drawer` — GĐ10, chưa commit) |
| D3 | Đầu nhóm | **Bỏ** dải Trao đổi / Thành viên / Cấu hình. Chỉ **1 dải tab chủ đề: Nhiệm vụ · Meeting · Issue · Thành viên** (icon màu + số); **Cấu hình = 1 icon ⚙** |
| D4 | Về khung chat | **Không có tab "Trao đổi"**: chat là màn mặc định; **bấm vùng tên nhóm** ⇒ về chat; đang ở tab chủ đề ⇒ nút **"← Trò chuyện"** kèm số tin mới |
| D5 | Phương án v1 (Phẳng / Mềm nổi / Navy) | Không chọn |
| D6 (T1) | Tab Meeting / Issue chưa có màn | **Đợt này ẩn** — chỉ hiện Nhiệm vụ (khi nhóm bật) + Thành viên; làm xong màn thì bật |
| D8 (T3) | Lệnh `/` trong ô soạn | **Để sau** — đợt này không làm, bỏ gợi ý `/` khỏi ô soạn (đã có `#` chèn nhiệm vụ) |
| D9 (T4) | Nhãn cạnh tên người gửi | **Chỉ "Quản lý"** cho người quản lý nhóm (role = 1); thành viên / Xem không nhãn; 1–1 không nhãn. BE trả vai trò theo người, lấy 1 lần cho cả trang tin  — theo vai trò **HIỆN TẠI** (người bị hạ quyền / đã rời nhóm ⇒ tin cũ không còn nhãn) |
| D10 (T5) | Phím tắt tìm hội thoại | **Ctrl K / ⌘ K** đưa con trỏ vào ô tìm — CHỈ khi đang ở trang Tin nhắn / trang nhóm; ô tìm hiện gợi ý phím tắt |
| D11 (T6) | Đầu khung chat 1–1 | **Bỏ ⓘ** — chỉ giữ icon tìm tin nhắn (phòng ban · mã NV đã ở dòng phụ dưới tên; panel phải đã có Ảnh/Tệp/Link) |
| D7 (T2) | "n trả lời" (luồng trả lời riêng) | **Bỏ khỏi thiết kế** — giữ trả lời kiểu trích dẫn như hiện tại (không đổi BE) |

## 3. Đề xuất đi kèm trong mockup v2 (Claude — user chưa phản đối, cần xác nhận khi chốt tồn)

- Avatar **nhóm vuông bo 12px**, **người tròn**.
- TPE SMART AGENT ghim thành **thẻ navy phát sáng** đầu danh sách.
- Ô tìm nền xám + gợi ý phím tắt `Ctrl K`; nút **+ Mới** navy (thay 2 icon tin nhắn mới / tạo nhóm).
- Luồng tin: dòng **"Tin chưa đọc"** (đỏ), nhãn ngày dạng viên, **vai trò** cạnh tên, **thẻ nhiệm vụ** viền màu trái, thẻ tệp, chip cảm xúc, thanh thao tác nổi khi rê, "n trả lời · lần cuối hh:mm".
- Ô soạn 1 khối, gợi ý **`/` lệnh** (/nhiemvu · /meeting · /issue), dòng nhắc phím tắt dưới ô.
- Dòng hội thoại đang mở: nền trắng + viền mảnh + vạch teal 4px bên trái; số chưa đọc teal.

## 4. Lệch khuôn có chủ đích

Thanh lọc pill (V2BaseSegmented) và dải tab đầu nhóm (V2BaseMiniTab + V2BaseSegmented) là component dùng chung — **vẽ lại riêng cho
Chat theo yêu cầu user 13/11**, không đổi component dùng chung ở màn khác.

## 5. Tồn — hỏi user trước khi viết plan code (lần lượt)

- ~~T1~~ → D6.
- ~~T2~~ → D7.
- ~~T3~~ → D8.
- ~~T4~~ → D9.
- ~~T5~~ → D10.
- ~~T6~~ → D11. **Hết tồn.**
