# GĐ14 — Bấm vào người trong chat ⇒ popup thông tin cá nhân + Nhắn tin

> 15/11/2026 · @namdangit · design ngắn — user DUYỆT 15/11 ("duyệt theo đề xuất") · chưa có lệnh code

## 1. Mục đích

Trong khung chat, bấm vào 1 người ⇒ xem nhanh thông tin liên lạc / công việc và nhắn tin riêng ngay, như Zalo
"Thông tin tài khoản".

## 2. Đã chốt với user

| # | Câu hỏi | Chốt |
|---|---|---|
| P1 | Popup hiện gì | Thông tin công việc có sẵn **+ chức vụ, điện thoại, email** |
| P2 | Ai xem được SĐT / email | **Mọi người dùng chat** (như danh bạ chat — mọi NV mọi công ty), không thêm quyền |
| P3 | Chỗ bấm + nội dung popup | Theo đề xuất (mục 4) |
| P4 | Hình thức | **`V2BaseModal` nhỏ giữa màn** (khuôn popup bắt buộc), không popover |

## 3. Phương án đã cân nhắc

1. **V2BaseModal (CHỌN)** — đúng khuôn `HRM/CLAUDE.md`, ngăn chat hẹp ~400px vẫn không cắt mép.
2. Popover cạnh avatar — nhẹ hơn nhưng dễ tràn / bị cắt trong ngăn trượt; dự án chưa có khuôn thẻ hồ sơ. Loại.

## 4. Thiết kế

**Nguồn dữ liệu (đo DB local 15/11, 650 NV đang làm):**
- Chức vụ = `employee_infos.employee_work_position_id` → `working_positions.name` (624/650 có) — cùng nguồn cột
  "Chức vụ" màn Hồ sơ nhân sự.
- Điện thoại = `employee_infos.telephone` (650/650) · Email = `employee_infos.email` (650/650, email công ty).
- KHÔNG hiện `personal_telephone`, `personal_email`.
- Còn lại dùng `EmployeeProfiles` (ảnh, tên, mã, công ty, phòng ban, bộ phận, `is_active`) + `ChatPresence::of`
  (trực tuyến / lần cuối).

**BE:** `GET /api/v1/assign/chat/profile/{employeeId}` (middleware như `directory`) — 1 người, 2 query (profile + chức
vụ/liên lạc) + Redis presence. Trả: `employee_id, fullname, code, image, company_name, department_name, part_name,
work_position_name, telephone, email, is_active, online, last_seen_at, is_me, conversation_id` (1–1 sẵn có, null nếu
chưa). Không tìm thấy ⇒ 404.

**FE:**
- `components/chat/ChatProfileModal.vue` trên `V2BaseModal` size sm: header avatar + tên + chấm trực tuyến /
  "Hoạt động … trước" / nhãn "Đã nghỉ việc"; thân: Mã NV · Chức vụ · Phòng ban – Bộ phận · Công ty · Điện thoại ·
  Email (ô trống ⇒ "—"; SĐT/email có nút sao chép); footer: **Nhắn tin** (ẩn khi là mình / đã nghỉ việc) + Đóng.
- Gọi API khi mở, nhớ trong store `chat` theo phiên (bấm lại không gọi).
- Nhắn tin ⇒ đóng popup, mở chat 1–1 bằng đúng luồng nút "Nhắn tin" tab Thành viên (store `chat/openDrawer`
  `{conversationId, directTo}`; ở trang `/assign/messages` dùng luồng `ChatShell.openDirect`).
- Chỗ bấm: avatar + tên người gửi (`ChatMessageItem`), chữ `@Tên` trong tin, avatar + tên tab Thành viên
  (`MembersPanel`). Con trỏ tay khi rê.

**Ngoài phạm vi:** sửa hồ sơ, gọi điện từ popup, app mobile (API dùng chung để app dùng sau).

## 5. Kiểm

- PHPUnit: trả đủ trường + chức vụ đúng tên; NV khác công ty xem được; không trả SĐT/email cá nhân; mình ⇒
  `is_me`; id không tồn tại ⇒ 404; chưa đăng nhập ⇒ 401.
- Playwright đo DOM: bấm avatar / tên / `@Tên` / thành viên ⇒ mở popup đúng người; nút Nhắn tin mở đúng hội thoại 1–1;
  bấm mình ⇒ không có nút; bấm 2 lần chỉ 1 request.
