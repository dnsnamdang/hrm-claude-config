# App: nhận chia sẻ từ app khác, gửi ngay trong cửa sổ share (như Zalo) — @cuong61n

Spec đầy đủ: `docs/superpowers/specs/2026-11-20-app-share-extension-design.md` (đọc đầu phiên).

- **Yêu cầu (user, 20/11/2026):** bấm Chia sẻ ở app khác (ảnh, file/PDF, văn bản, link) → TPE_APP nằm trong bảng share kèm hàng phòng chat gần đây như Zalo; chọn phòng → cửa sổ nhỏ (xem trước + lời nhắn + Gửi), gửi xong đóng, không mở app.
- **Phạm vi:** iOS + Android, đợt 1 chỉ flavor **TpeProd** (`com.tanphat.soft.app`). Các flavor khác làm sau.
- **Cách làm đã chốt:** gửi ngay trong cửa sổ share (cách 2). iOS: Share Extension Swift + App Group + Keychain dùng chung + `INSendMessageIntent` cho hàng gợi ý. Android: `ShareReceiverActivity` (Flutter, engine cache dùng chung) + Sharing Shortcuts.
- **Quyết định kỹ thuật chính:** extension KHÔNG tự refresh token (refresh token xoay vòng; PROD `JWT_TTL=null` nên access token không hết hạn theo thời gian). BE không đổi.
- **Chờ user:** ai tạo App ID extension / App Group / bật Siri + App Groups + Keychain Sharing / làm mới profile, khi nào.
