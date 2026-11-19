# Gọi thoại / video trong Chat (như Zalo) — ĐỀ XUẤT, LƯU TRIỂN KHAI SAU

> 14/11/2026: user bảo "lưu lại triển khai sau, tối ưu các vấn đề nhỏ trước". CHƯA chọn phương án, CHƯA thiết kế chi tiết.
> Bối cảnh: 1–2 nghìn người, đa nền tảng web Nuxt + app Flutter + desktop (memory agent-chat-quy-mo-va-da-nen-tang).

Nền chung mọi phương án: WebRTC (web/Flutter/desktop đều có thư viện). Báo gọi qua socket chat sẵn có (:8895 / pm2 hrm-tpe-socket),
lịch sử + cuộc gọi nhỡ = tin hệ thống trong hội thoại. Khác nhau ở máy chủ trung chuyển âm thanh/hình ảnh.

## Phương án
1. **Tự dựng LiveKit (khuyên chọn)** — mã nguồn mở, có SDK web/Flutter/desktop; 1–1 + gọi nhóm chung 1 máy chủ; chia sẻ màn hình
   sẵn; dữ liệu nằm trong công ty, không phí theo phút. Ước lúc đông vài chục cuộc gọi cùng lúc ⇒ 1 máy 4 nhân thường đủ (CHƯA đo).
   Cần: máy chủ IP công khai, mở cổng UDP, tên miền + TLS, máy chủ TURN (coturn) cho 4G / mạng chặn. CHƯA kiểm VPS prod đáp ứng.
2. **Gọi thẳng giữa 2 máy (P2P)** — rẻ nhất, chỉ cần TURN; nhóm chỉ ổn 3–4 người, mở rộng nhóm phải làm lại theo PA1.
3. **Thuê dịch vụ (Stringee, Agora…)** — nhanh nhất, không vận hành; phí theo phút (phải hỏi báo giá), dữ liệu qua bên thứ ba.

## Giai đoạn (áp cho mọi phương án)
- GĐ1: gọi thoại + video 1–1 trên web — nút gọi đầu hội thoại, màn chuông, tắt mic/camera, chuyển thoại↔video; tin
  "Cuộc gọi thoại · 3 phút" / "Cuộc gọi nhỡ" (tính chưa đọc); báo bận; nhiều tab/máy cùng đổ chuông, bắt ở đâu chỗ khác tắt.
- GĐ2: app mobile đổ chuông kể cả khi tắt app (iOS CallKit + VoIP push, Android thông báo toàn màn hình) — khó + tốn công nhất.
- GĐ3: gọi nhóm từ nhóm chat, chia sẻ màn hình (web/desktop).
- GĐ4 (khác Zalo): Agent AI ghi lại nội dung cuộc gọi, tóm tắt, đề xuất tạo nhiệm vụ.
- Lưu ý: web chỉ đổ chuông khi đang mở tab HRM.

## Khi làm tiếp
Hỏi user chọn PA 1/2/3 + chốt phạm vi GĐ1 ⇒ viết `design.md` + mockup màn gọi ⇒ plan. Đụng source phải hỏi riêng.
