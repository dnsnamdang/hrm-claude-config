# Chat — GĐ43 Đổi ảnh đại diện cá nhân + ảnh nhóm (chưa có số Redmine) — @cuong61n

> Yêu cầu 25/11/2026: thêm chức năng đổi avatar chat cá nhân (hình TRÒN) và avatar nhóm (dạng THẺ = thẻ trước của
> ChatIdCard). Trọng tâm UX: popup/màn căn khung ảnh — kéo khung tới vùng muốn lấy, co giãn giữ tỉ lệ, phóng ảnh
> (user 25/11: KHÔNG cần xem trước ở từng chỗ ảnh sẽ hiện). Thiết kế trước trên Pencil để user duyệt rồi mới code.

## Phase 0 — Rà code + thiết kế (25/11/2026)

- [x] 25/11 — Rà code web (`components/chat/ChatIdCard.vue`, `ChatAvatar.vue`, `ConversationRow`, `ChatPane`, `WorkspaceView`,
  `SettingsPanel`, `CreateWorkspaceModal`, `ChatProfileModal`), app (`ui/chat/widget/chat_id_card.dart`, `conversation_row.dart`,
  `info/workspace_info_page.dart`, `workspace/workspace_form_page.dart`, `chat_room_page._headerAvatar`), BE (`Workspace` fillable,
  `ChatConversation`, `EmployeeProfiles` lấy `employee_infos.image`, upload S3 `Human FileController@uploadImage` → `CmcS3Helper`).
  Code chat ở worktree `gop_db-client` (cổng 3002, nhánh `gop_db`) GIỐNG `hrm-client` gốc (`diff -rq components/chat` rỗng).
  Kết luận: `ChatIdCard` web + app đã chừa sẵn prop `groupImage` (chưa có chức năng chọn); ảnh người đang lấy thẳng ảnh hồ sơ
  nhân sự; chưa có cột ảnh nhóm trong `workspaces`; chưa có thư viện crop ở web (chỉ `utils/chat/imageEditor.js` canvas thuần)
  và app (chỉ `image_picker`).
- [x] 25/11 — Vẽ Pencil `~/Downloads/meeting-mobile_v2.pen` (file user đang mở), 4 khung mới:
  1. `CHAT · Đổi ảnh đại diện — WEB (nhóm)`: V2BaseModal 760px, vùng ảnh 728×420, khung thẻ 6:7 bo góc kéo được + 4 tay cầm,
     lưới 3×3, thanh phóng + ô "Kết quả" 36×42, nút Chọn ảnh khác / Xoá ảnh nhóm, footer Lưu · Quay lại.
  2. `… WEB (cá nhân)`: cùng khuôn, khung TRÒN, nút "Dùng lại ảnh hồ sơ nhân sự".
  3. `CHAT · Lối vào đổi ảnh — WEB`: ① rê chuột ảnh ở đầu màn nhóm (máy ảnh) · ② dòng "Ảnh nhóm" tab Cấu hình ·
     ③ ô ảnh đầu popup Tạo nhóm (thẻ chữ tắt theo tên) · ④ cá nhân: menu ⋮ cột hội thoại + popup hồ sơ của chính mình.
  4. `CHAT · Đổi ảnh — APP`: ① Thông tin nhóm có nút máy ảnh + bottom sheet Chụp / Thư viện / Xoá · ② form nhóm ô ảnh đầu form ·
     ③ màn "Căn ảnh" toàn màn hình (khung kéo, chụm phóng, Huỷ/Xong) · ④ Hồ sơ của tôi (khung tròn).
- [x] 25/11 — User duyệt: "bắt đầu làm luôn, làm đúng như design". 2 điểm chưa chốt lấy theo đề xuất: (a) ảnh cá nhân là ảnh
  CHAT RIÊNG (bảng `chat_profiles`, null ⇒ ảnh hồ sơ); (b) ảnh nhóm chỉ Quản lý + nhóm đang mở. User thêm 25/11: **đổi cả
  BIỆT DANH cá nhân** (hiện thay họ tên ở tên hội thoại / người gửi; @mention + label vẫn họ tên) và **mở popup phải nạp sẵn
  ảnh đang dùng**.

## Phase 1 — BE (worktree `gop_db-api`, nhánh `gop_db-chat-doi-anh` từ `gop_db`, :8003) — XONG 25/11
- [x] 25/11 — Migration `2026_11_29_000001_add_image_to_workspaces_table` (`workspaces.image` varchar 500 null) +
  `2026_11_29_000002_create_chat_profiles_table` (`employee_id` PK = employees.id, `image`, `nickname` ≤ 50, audit). Đã migrate local.
- [x] 25/11 — Entity `Chat/ChatProfile` (BaseModel), `Workspace` fillable `image`; `WorkspaceService::setImage()` bắn `WorkspaceActivity updated
  changes.image` ⇒ `SyncWorkspaceChat` ghi tin hệ thống "X đã đổi / bỏ ảnh nhóm" + socket như sửa tên.
- [x] 25/11 — `Services/Chat/ChatImageService`: upload S3 thư mục riêng `tanphat_hrm/chat-avatars` (CmcS3Helper::putFile), xoá file cũ
  khi thay/bỏ (deleteByUrl đúng prefix), `setMyImage/clearMyImage/setMyNickname`, `fetchBytes()` đọc lại ảnh S3 cho popup (S3 không CORS).
- [x] 25/11 — Request `Chat/UploadChatImageRequest` (`image` required|image|mimes jpg,jpeg,png,webp|max 5120) + `UpdateChatProfileRequest`
  (`nickname` nullable|max:50) — không khai messages(), dùng lang file.
- [x] 25/11 — Route: `POST/DELETE workspaces/{id}/image` (`CheckWorkspaceAccess:manager,open`) · `POST/DELETE chat/me/avatar` ·
  `PATCH chat/me/profile` · `GET chat/image-source?url=`. Controller: `WorkspaceController::setImage/deleteImage`,
  `ChatController::setMyAvatar/deleteMyAvatar/updateMyProfile/imageSource`.
- [x] 25/11 — Presenter: `EmployeeProfiles` leftJoin `chat_profiles` ⇒ `image` = COALESCE(chat, hồ sơ) + `hr_image`, `chat_image`,
  `nickname`, `display_name`; `ChatPresenter::person` + `ChatProfileService` trả thêm; `ConversationService` select `w.image` ⇒
  `workspace.image`, tiêu đề 1–1 = display_name; `WorkspaceResource.image`.
- [x] 25/11 — Kiểm bằng curl :8003 (TK namdangit): POST ảnh nhóm 71 ⇒ URL S3 `chat-avatars/…` + danh sách có `workspace.image`;
  POST avatar ⇒ `image` = ảnh chat, `hr_image` giữ; file không phải ảnh ⇒ 422 "Phải là file ảnh"; nickname 51 ký tự ⇒ 422 lang
  file; DELETE cả 2 ⇒ về null, tin hệ thống "đã đổi / đã bỏ ảnh nhóm"; `image-source` URL ngoài bucket ⇒ 404.

## Phase 2 — Web (worktree `gop_db-client`, nhánh `gop_db-chat-doi-anh`, :3002) — XONG 25/11
- [x] 25/11 — `components/chat/ChatImageCropModal.vue` (MỚI, V2BaseModal + `unsavedModalMixin`): ảnh cố định fit × zoom, KHUNG kéo
  được (thẻ 6:7 bo 25% | tròn), 4 tay cầm co giãn giữ tỉ lệ (clamp trong ảnh), lưới 3×3, lăn chuột / thanh trượt phóng, ô "Kết quả"
  36×42 / 48 vẽ canvas realtime, nút Chọn ảnh (khác) / Xoá ảnh | Dùng lại ảnh hồ sơ, ô Biệt danh (vee-validate max:50) khi
  `show-nickname`; xuất JPEG 360×420 / 256×256; prop `current-image` ⇒ mở là nạp sẵn ảnh đang dùng (blob: dùng thẳng, S3 ⇒
  `chatApi.getBlob('chat/image-source')`). Kiểm loại/≤ 5MB ở FE báo đỏ dưới ô.
- [x] 25/11 — Lối vào: ① `WorkspaceView` đầu nhóm rê chuột ⇒ máy ảnh (chỉ `abilities.can_manage` + nhóm mở), bấm mở popup (không về chat);
  ② `SettingsPanel` dòng "Ảnh nhóm" (ChatIdCard thẻ + Đổi ảnh / Xoá ảnh, emit lên WorkspaceView); ③ `CreateWorkspaceModal` ô ảnh 72×84
  đầu form (chữ tắt theo tên, tải lên sau khi tạo); ④ `ConversationList` menu ⋮ "Đổi ảnh đại diện / biệt danh" ⇒ `openChatProfile(me,
  {edit:true})` (ChatShell + ChatDrawer provide 2 tham số) ⇒ `ChatProfileModal` của mình: rê ảnh hiện máy ảnh, popup tròn + biệt danh;
  tên hiện `display_name`, dòng "Họ tên: …" khi có biệt danh.
- [x] 25/11 — Hiển thị: `ConversationRow` ⇒ `ChatIdCard group-image`; `ChatAvatar` nhóm có `image` ⇒ 1 ảnh (không ghép 2×2) — dùng ở
  đầu nhóm, `ChatPane` head, `ForwardModal`; `ChatMessageItem` + `ChatPane` head 1–1 dùng `display_name || fullname`.
  Xoá ảnh nhóm ⇒ `$confirm` (textAccept Xoá); lưu xong `store chat/patch` ⇒ dòng hội thoại đổi thẻ ngay.
- [x] 25/11 — Kiểm Playwright :3002 (TK namdangit): ⋮ ⇒ popup nạp sẵn ảnh cũ, kéo khung (+120,+30), co góc SE (292→234), đặt
  biệt danh "Cường Dev" ⇒ POST avatar 200 + PATCH profile 200, popup hồ sơ hiện "Cường Dev / Họ tên: DNS Admin"; đầu nhóm 71 rê ⇒
  máy ảnh ⇒ chọn ảnh ⇒ Lưu ⇒ đầu nhóm + thẻ trước dòng hội thoại = ảnh mới (S3 ~5s); tab Cấu hình ⇒ Xoá ảnh ⇒ confirm ⇒ về chữ tắt
  "VĐ"; popup Tạo nhóm ô ảnh chữ tắt "B2" + máy ảnh. Console 0 lỗi. Chưa có eslint trong repo (npx kéo bản 10 không chạy Node 14).
- [x] 25/11 — Tạo nhóm kèm ảnh: POST workspaces 200 ⇒ POST workspaces/1835/image 200 ⇒ vào nhóm 1835 đầu nhóm hiện ảnh (nhóm thử
  `[TEST-GD43] Nhóm thử ảnh` ở DB local).
- [x] 25/11 — User phản hồi: dòng "Ảnh nhóm" ở Cấu hình phải giống design, bỏ hiệu ứng nghiêng khi rê ⇒ thay `ChatIdCard` bằng thẻ tĩnh
  `.sp__thumb` 36×42 bo 9 (ảnh hoặc chữ tắt gradient), đo lại: thẻ 36×42, cách nút Đổi ảnh 12px, thẳng hàng với nút.
- [x] 25/11 — User: "lúc bấm đổi ảnh thì nên hiện ảnh cũ" ⇒ prop `current-image` + endpoint `chat/image-source` (S3 không CORS);
  Playwright: mở ⋮ ⇒ popup có sẵn ảnh (blob) + biệt danh đang dùng.

## Phase 3 — App (TPE_APP, nhánh `chat-doi-anh` tách từ `develop`, 25/11/2026 — @cuong61n)

- [x] 25/11 — Model: `ChatConversation.workspaceImage` (`workspace.image`), `ChatWorkspace.image`, `ChatProfile.isMe / hrImage / chatImage`
  (`ui/chat/model/chat_models.dart`, `ui/chat/info/profile_sheet.dart`). Biệt danh: user chốt 25/11 BỎ, để sau — đã gỡ hết
  `nickname / display_name`, tên vẫn `fullname`.
- [x] 25/11 — API `ChatApiService`: `setWorkspaceImage` / `deleteWorkspaceImage` (multipart `image`), `setMyAvatar` / `deleteMyAvatar`,
  `imageSource(url)` (bytes ảnh đang dùng qua `chat/image-source`, `raw: true` + `ResponseType.bytes`).
- [x] 25/11 — Hiển thị ảnh nhóm: `ChatIdCard.of` nối `groupImage` (thẻ trước ở danh sách); `ChatAvatar` (conversation_row) nhóm có ảnh ⇒
  1 ảnh vuông bo thay ô icon màu (đầu phòng chat, Thông tin nhóm, chia sẻ…), thêm `image:` ghi đè khi màn có bản mới.
- [x] 25/11 — Màn "Căn ảnh" `ui/chat/widget/chat_image_crop_page.dart` (mockup ③): ảnh đứng yên, khung thẻ 6:7 bo 25% / tròn kéo
  được, 4 tay cầm co giãn giữ tỉ lệ (bắt góc theo điểm chạm thật qua `Listener`, bán kính 30), lưới 3×3, chụm 2 ngón + thanh trượt
  phóng 1–4×, ô Kết quả 36×42 / tròn 48, Huỷ / Xong; cắt bằng `dart:ui` canvas ⇒ JPEG q90 360×420 (nhóm) / 256×256 (cá nhân)
  qua gói `image`.
- [x] 25/11 — Luồng chọn ảnh `ui/chat/widget/chat_image_flow.dart`: sheet "Ảnh nhóm" / "Ảnh đại diện" (Chụp ảnh · Chọn từ thư viện ·
  Căn lại ảnh hiện tại · Xoá ảnh nhóm / Dùng lại ảnh hồ sơ nhân sự), `pickAndCropChatImage` (image_picker ⇒ Căn ảnh), nút
  `ChatCameraBadge`, `chatErrorText`.
- [x] 25/11 — ① Thông tin nhóm (`info/workspace_info_page.dart`): máy ảnh góc ảnh 72 (chỉ `abilities.can_manage` = Quản lý + nhóm
  mở, cùng cờ nút Sửa) ⇒ sheet ⇒ API; xoá ảnh hỏi `showAppConfirm` đỏ; xong `onChanged` ⇒ phòng chat nạp lại đầu khung.
- [x] 25/11 — ② Form tạo / sửa nhóm (`workspace/workspace_form_page.dart`): ô ảnh 72×84 bo 18 đầu form, chưa có ảnh ⇒ chữ tắt
  theo tên nhóm (gõ tên đổi theo), máy ảnh góc dưới phải; Tạo ⇒ POST workspaces rồi POST image (lỗi ảnh chỉ toast, nhóm vẫn tạo);
  Sửa ⇒ PUT rồi POST / DELETE image khi đổi / bỏ.
- [x] 25/11 — ④ Tab "Cá nhân" của Chat = hồ sơ của tôi (`ui/chat/profile/chat_my_profile_page.dart`, thay màn "Đang phát triển"):
  header + hero chung 1 `ChatHeaderBg` (user 25/11: nền liền mạch), ảnh tròn 80 + máy ảnh, họ tên · chức danh · mã phòng · mã NV,
  dòng trạng thái ảnh (tự chọn / hồ sơ nhân sự), khối THÔNG TIN (ĐT, email, phòng ban, công ty); đổi ảnh ⇒ danh sách tải lại.
- [x] 25/11 — Test simulator iPhone 15 (flavor tpeLocal, `--dart-define=APP_API_BASE_URL=http://127.0.0.1:8003/api/` trỏ worktree
  gop_db-api), 51 bước `step.sh` không lỗi Flutter, tài khoản namdangit: nhóm 71 / hội thoại 74 — đổi ảnh từ thư viện (POST image 200,
  Thông tin nhóm + đầu phòng + thẻ danh sách đổi ngay, tin hệ thống "đã đổi ảnh nhóm"); Căn lại ảnh hiện tại (GET image-source
  200) + kéo khung / kéo góc co giãn / thanh phóng; Xoá ảnh nhóm (hộp xác nhận ⇒ DELETE 200 ⇒ về ô icon); form Sửa chọn ảnh ⇒
  Lưu (PUT + POST image); Tạo nhóm "[TEST-GD43] Nhom app anh" kèm ảnh (POST workspaces 2881 + POST image, vào thẳng phòng chat có
  ảnh); tab Cá nhân đổi ảnh tròn (POST me/avatar 200) rồi Dùng lại ảnh hồ sơ (DELETE 200). Thành viên thường (monnv.kd2, id 50,
  đã đặt mật khẩu local Test@123): BE `abilities.can_manage=false` + POST image ⇒ 403 — app ẩn máy ảnh theo đúng cờ này (chưa
  đăng nhập lại trên app để chụp).
- [ ] Chưa làm: bấm máy ảnh ở hồ sơ của mình từ sheet hồ sơ (CH-16) — chỉ có ở tab Cá nhân; Android chưa chạy thử; chưa commit.
- Ghi chú: `make gen` không cần (không route / DI mới — màn Căn ảnh đẩy bằng `MaterialPageRoute`). Nhánh `chat-doi-anh` đang chứa thêm
  file sửa dở của phiên khác (`common_view/scaled_to_width.dart`, `internal_notification_detail/*`) — không thuộc GĐ43.

## Phase 4 — Cải thiện thêm (user 25/11 chọn 2 mục)
- [x] 25/11 — Hiện ngay ảnh vừa cắt trong lúc chờ S3 (3–5s): `saveImage` (WorkspaceView) / `saveMe` (ChatProfileModal) đóng popup ngay,
  gán `blob:` của bản cắt vào `workspace.image` + store `chat/patch` / `p.image`, tải xong thay URL S3, lỗi trả ảnh cũ + toast;
  `ChatAvatar` / `ChatIdCard` `usable()` nhận thêm `blob:`.
- [x] 25/11 — e2e `e2e/tests/chat/chat-avatar.spec.ts` (6 ca, PNG sinh tại chỗ, tự dọn ảnh cuối bài): Quản lý đổi ảnh (kéo khung, co góc
  giữ 6:7, blob: hiện ngay rồi URL S3, thẻ dòng hội thoại) · Cấu hình xoá ảnh + tin hệ thống · tệp > 5MB / tệp giả / Esc hỏi chưa lưu ·
  cá nhân nạp sẵn ảnh, lưu, dùng lại ảnh hồ sơ · thành viên thường không thấy máy ảnh + API 403. Chạy:
  `cd e2e && BASE_URL=http://127.0.0.1:3002 API_URL=http://127.0.0.1:8003 npx playwright test tests/chat/chat-avatar` (Node 20.11.1
  — máy không có v20.20.1 như CLAUDE.md ghi) ⇒ 6/6 pass (1,3 phút).
- [x] 25/11 — User: thẻ ở dòng Ảnh nhóm nhìn bé hơn ở hội thoại ⇒ nâng 36×42 → 60×70 bo 15, chữ tắt 18px (đo 60×70).

## Đẩy code + deploy (user bảo 25/11: "đẩy build prod TPE web đi, app đẩy lên nhánh develop github")
- [x] 25/11 — API: commit `ce975a34f` trên `gop_db-chat-doi-anh` → merge `gop_db` → push origin gop_db. Client: `f6b7c01f0` → gop_db → push.
  App TPE_APP: `3b9d77f` (chỉ 11 file GĐ43, để nguyên 4 file sửa dở của phiên khác) → merge `develop` → push origin develop.
- [ ] 25/11 — Prod TPE: `~/build_tpe.sh` (log `~/build_tpe_20261125.log`) — kết quả ghi bên dưới.
