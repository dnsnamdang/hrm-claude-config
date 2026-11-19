# GĐ16 — Tạo nhanh nhắc việc từ tin nhắn chat (design ngắn) · @namdangit

> 15/11/2026 · trạng thái: CHỜ USER DUYỆT · việc nhỏ (chỉ hrm-client, không BE, không migration)

## Mục đích (user)
Trong nhóm, sếp nhắn "Tuấn ngày mai gọi cho anh Toàn bên đối tác về việc triển khai hợp đồng nhé" ⇒ Tuấn bấm
**Tạo nhắc việc** ngay trên tin, đặt ngày/giờ hạn ⇒ app mobile nhắc đúng lịch (cơ chế nhắc hạn "Việc của tôi" sẵn có).

## Mục tiêu / không làm / tránh
- Làm: nút trên tin ⇒ mở form "Tạo nhắc việc" có sẵn, điền trước nội dung ⇒ lưu thành nhắc việc cá nhân (`personal_todos`).
- KHÔNG làm (user chọn PA2 15/11): liên kết ngược về tin gốc (không cột mới, không migration); không nhắc giùm người khác;
  không tự đọc "ngày mai" trong tin để đặt hạn.
- Tránh: dựng popup nhắc việc thứ 2; để lộ cho thành viên khác rằng ai đã tạo nhắc việc từ tin.

## Phương án đã xét
1. **Dùng lại `TodoFormModal`** (đã được AgentWorkspace dùng lại) + thêm 2 prop điền sẵn tiêu đề / mô tả — **CHỌN**: 1 form duy nhất, đủ loại nhắc việc / ngày giờ hạn / các bước / liên hệ, sửa form là mọi nơi cùng đổi.
2. Popup mini riêng trong chat (tiêu đề + ngày giờ) — loại: trái quy tắc "không tự dựng popup mới", lệch form gốc.
3. Liên kết ngược về tin (PA1) — user không chọn.

## Thiết kế
- **Nút**: thanh thao tác của tin (`ChatMessageItem`), icon `ri-alarm-line`, tooltip "Tạo nhắc việc", đặt sau "Tạo nhiệm vụ".
  Hiện cho MỌI tin người xem đọc được, trừ tin đã thu hồi và tin hệ thống — kể cả người chỉ có quyền xem nhóm, chat 1–1,
  nhóm tắt tab Nhiệm vụ (nhắc việc là việc cá nhân, không cần quyền gửi tin).
- **Điền sẵn**: Tiêu đề = nội dung chữ của tin (@ lưu dạng chữ thường nên giữ nguyên, cắt 200 ký tự ở ranh giới từ; BE cho tối đa 500); tin chỉ có ảnh/tệp/sticker ⇒ "[Ảnh]" / tên tệp / "[Sticker]".
  Mô tả = `Từ tin của <người gửi> · <tên nhóm hoặc "Chat 1–1"> · <dd/mm/yyyy HH:mm>` + xuống dòng + toàn văn tin.
  Loại nhắc việc = loại mặc định như màn Việc của tôi; ngày/giờ hạn để trống cho người dùng chọn.
- **`TodoFormModal`** (component dùng chung của my-todo): thêm prop `presetTitle`, `presetDescription` — chỉ áp khi form TẠO
  (giống `presetContact` sẵn có). Không đổi hành vi các nơi đang dùng.
- **Lưu**: ChatPane (hoặc ChatShell/ChatDrawer — chỗ gắn modal 1 lần) gọi API có sẵn `POST assign/my-todo/todos`, theo đúng
  payload màn Việc của tôi (kể cả bước con + liên hệ mới). Danh sách loại nhắc việc tải khi bấm nút lần đầu (lazy).
  Lưu xong toast "Đã tạo nhắc việc", không ghi gì vào hội thoại.
- **Đa nền tảng**: không thêm logic BE; app mobile (khi có chat trên app) làm cùng kiểu bằng API sẵn có.

## Để người làm tự quyết
Vị trí gắn modal (1 lần cho cả trang chat + ngăn trượt), cách tách text tin (dùng helper chatFormat sẵn có), e2e chỉ khi user yêu cầu.
