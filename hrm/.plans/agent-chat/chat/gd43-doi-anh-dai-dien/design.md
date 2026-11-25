# Chat — GĐ43 Đổi ảnh đại diện cá nhân + ảnh nhóm — @cuong61n

> Yêu cầu 25/11/2026. Mockup Pencil: `~/Downloads/meeting-mobile_v2.pen`, 4 khung `CHAT · Đổi ảnh …` (web nhóm · web cá nhân ·
> lối vào web · 4 màn app). Plan + kết quả kiểm: `plan.md`.

## Mục tiêu
- Nhóm trao đổi có ẢNH NHÓM riêng — là **thẻ trước** của `ChatIdCard` (36×42, tỉ lệ 6:7) ở danh sách hội thoại; đầu nhóm / app dùng
  cùng ảnh (vuông bo). Chưa có ảnh ⇒ vẫn thẻ chữ tắt tên nhóm như cũ.
- Cá nhân có ảnh đại diện CHAT riêng (hình TRÒN); không đụng ảnh thẻ trên hồ sơ nhân sự. (Biệt danh: user 25/11 bảo để sau, đã gỡ.)
- Trọng tâm UX: popup / màn **căn khung ảnh** — ảnh đứng yên, kéo khung tới vùng muốn lấy, co giãn giữ tỉ lệ, phóng ảnh, ô Kết quả
  nhỏ; mở popup là nạp sẵn ảnh đang dùng. User 25/11: KHÔNG cần xem trước ở từng chỗ ảnh sẽ hiện.

## Quyết định đã chốt
- 25/11: avatar cá nhân TRÒN; avatar nhóm = THẺ trước ChatIdCard; bỏ cột xem trước, dồn diện tích cho căn khung.
- 25/11 (user duyệt "làm đúng như design", 2 điểm lấy theo đề xuất): ảnh cá nhân lưu bảng mới `chat_profiles` (employee_id PK,
  image, nickname), `image` trả ra = COALESCE(ảnh chat, ảnh hồ sơ); ảnh nhóm cột `workspaces.image`; chỉ **Quản lý + nhóm đang mở**
  đổi/xoá ảnh nhóm (guard route `CheckWorkspaceAccess:manager,open`).
- Biệt danh: ĐÃ LÀM rồi GỠ theo user 25/11 ("để sau làm"); nếu làm lại: cột `chat_profiles.nickname`, BE trả `display_name` = nickname ?: fullname, FE chỉ đổi ở tên hội thoại / người gửi / đầu khung / popup hồ sơ, giữ `label` + @mention theo họ tên.
- Ảnh cắt ở client (web canvas / app dart:ui) ⇒ BE chỉ kiểm loại + ≤ 5 MB, lưu S3 thư mục riêng `tanphat_hrm/chat-avatars`, thay/bỏ
  thì xoá file cũ. Kích thước: nhóm 360×420 JPEG, cá nhân 256×256 JPEG.
- S3 không trả CORS ⇒ web lấy lại ảnh đang dùng qua `GET chat/image-source?url=` (chỉ cho URL đúng bucket + prefix `tanphat_hrm/`).
- Đổi / bỏ ảnh nhóm ghi tin hệ thống "X đã đổi ảnh nhóm" / "đã bỏ ảnh nhóm" + socket qua `WorkspaceActivity updated` như sửa tên.

## Phương án đã cân nhắc
1. **Ảnh riêng cho chat (chọn)** — bảng `chat_profiles`; ảnh hồ sơ nhân sự là ảnh thẻ phải qua HR duyệt, không nên cho tự đổi.
2. Đổi thẳng `employee_infos.image` — đơn giản nhưng phá luồng duyệt hồ sơ, ảnh thẻ bị thay bằng ảnh tự chọn. Loại.
3. Thư viện crop (cropperjs / image_cropper) — thêm phụ thuộc, khó khớp khuôn thẻ 6:7 + tay cầm theo design. Tự dựng canvas thuần
   (web `ChatImageCropModal.vue`, app màn Căn ảnh) để app desktop sau này dùng lại được. Chọn tự dựng.

## Phạm vi
- BE: 2 migration, entity ChatProfile, ChatImageService, 2 Request, 6 route, presenter (EmployeeProfiles / ChatPresenter /
  ConversationService / ChatProfileService / WorkspaceResource).
- Web: `ChatImageCropModal.vue` + 4 lối vào (đầu nhóm, Cấu hình, Tạo nhóm, menu ⋮ / popup hồ sơ của mình) + hiển thị ảnh nhóm ở
  ConversationRow / ChatAvatar / ChatPane / ForwardModal, display_name ở tin nhắn.
- App: ChatIdCard.groupImage, ChatAvatar nhóm, Thông tin nhóm + form nhóm + màn Căn ảnh + Hồ sơ của tôi (xem plan.md Phase 3).

## Ngoài phạm vi
- Lịch sử thay đổi ảnh theo entity-history (chỉ tin hệ thống trong nhóm). Thông báo chuông. Ảnh nhóm cho nhóm Dự án KH tự sinh
  (vẫn đổi được như nhóm thường nếu là Quản lý).
