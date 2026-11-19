# GĐ33 — Rời nhóm trao đổi (17/11/2026) @namdangit

## Mục đích
Mọi người trong nhóm trao đổi tự rời được nhóm, không phải nhờ Quản lý. Hiện chỉ Quản lý rời được (menu ⋮ dòng của mình ở
tab Thành viên, API `DELETE members/{id}` chỉ cho Quản lý + nhóm còn mở) ⇒ Thành viên / Xem không có lối ra.

## Phạm vi (user chốt 17/11)
- Làm cho nhóm trao đổi thường (gồm nhóm tiếp nhận YC hỗ trợ — là nhóm thường). **Nhóm gắn Dự án KH tính sau**: không hiện
  nút, API trả 422.
- **Nhóm đã đóng vẫn rời được.**
- Ngoài phạm vi: chat 1–1 (không phải nhóm), đổi luật "Mời ra" của Quản lý.

## Luật (giữ chốt chặn có sẵn — Claude đề xuất, user chưa phản đối)
- Quản lý cuối cùng không rời được (cả nhóm đã đóng — nếu không, nhóm không còn ai mở lại) ⇒ 422 "Nhóm phải còn ít nhất 1 Quản lý".
- Còn nhiệm vụ chưa xong của nhóm ⇒ 422 "đang làm n nhiệm vụ chưa xong — chuyển người làm trước" (FE hiện khối lỗi + link như tab Thành viên).
  Nhóm đóng thì việc đã huỷ ⇒ không vướng.
- Rời xong: tin hệ thống "X đã rời nhóm" (có sẵn), hội thoại nhóm biến mất khỏi danh sách của người rời, về trang Tin nhắn.
  Vào lại: Quản lý thêm lại như thường.

## Approaches
- **A (user chọn)** — API riêng `POST workspaces/{id}/leave`, middleware thành viên (không đòi nhóm mở), dùng lại
  `WorkspaceMemberService::remove()` (2 chốt + sự kiện member_removed). "Mời ra" giữ nguyên.
- B — nới `DELETE members/{id}` cho tự mời mình ra: ít code nhưng phải nới middleware Quản lý dùng chung ⇒ dễ lọt Thành viên
  mời người khác ra. Bỏ.

## Giao diện
"Rời nhóm" (icon `ri-logout-box-r-line`, nhóm nguy hiểm) ở 3 chỗ, đều qua popup xác nhận chung `$confirm`:
1. Menu ⋮ dòng hội thoại nhóm (ConversationRow) — trang Tin nhắn + ngăn trượt.
2. Mục Cấu hình (⚙) của nhóm, khối Trạng thái nhóm (cạnh Đóng / Mở lại) — mọi vai trò.
3. Dòng của chính mình ở tab Thành viên — nay hiện cho mọi vai trò (trước chỉ Quản lý), gọi API mới.
Không hiện ở nhóm gắn Dự án KH. Popup: "Bạn sẽ không còn xem được chat của nhóm <tên>. Quản lý thêm lại sau vẫn được."

## Kiểm
PHPUnit: Thành viên / Xem rời được · Quản lý cuối bị chặn · còn việc bị chặn · nhóm đóng rời được · nhóm Dự án KH 422 ·
người ngoài 403 · tin "đã rời nhóm" + mất hội thoại. e2e mới `chat-roi-nhom.spec.ts` cho 3 lối vào + ca chặn + ca không quyền;
chạy lại bộ chat liên quan.

## Để người làm tự quyết
Tên hàm/route chi tiết, cách FE cập nhật danh sách sau khi rời (dùng luồng conversation.updated removed_ids có sẵn nếu được).
