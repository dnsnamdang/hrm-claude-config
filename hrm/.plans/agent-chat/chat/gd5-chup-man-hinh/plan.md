# GĐ5 chat — Chụp màn hình + Chỉnh ảnh + Nén ảnh

> 13/11/2026. User hỏi "chụp màn hình như Zalo" → demo `../demo-chup-man-hinh/index.html` → tư vấn: lõi là BỘ CHỈNH ẢNH dùng chung
> cho mọi đường vào (dán / đính kèm / 📷 / app desktop sau) + nén ảnh (quy mô 1–2 nghìn người). User: "làm".
> Phạm vi: chỉ hrm-client, nhánh `gop_db-chat-chup-man-hinh` (tách origin/gop_db d178b590c), worktree wt-nhom-trao-doi. Không BE/DB, không gói mới.

## Đã làm
- [x] `utils/chat/imageEditor.js` — JS thuần trên canvas (không Vue ⇒ app desktop dùng lại; nút HTML thô có chủ đích vì module không phụ thuộc V2Base). `openImageEditor(source, {mode})` ⇒ `{blob, action}`/null. mode `capture`: kéo chọn vùng (bấm đúp = cả ảnh) ⇒ Đính kèm / Gửi; mode `edit`: vùng = cả ảnh ⇒ Xong. Khung · mũi tên · bút · chữ · làm mờ · 4 màu · hoàn tác · chọn lại vùng · sao chép · Esc huỷ · Enter xong. Xuất theo độ phân giải gốc.
- [x] `utils/chat/screenCapture.js` — getDisplayMedia ⇒ canvas 1 khung (app desktop thay bằng chụp của hệ điều hành).
- [x] `utils/chat/imageCompress.js` — PNG/JPEG/WebP/BMP > 300 KB ⇒ WebP 0.9, cạnh dài ≤ 2560; GIF/SVG/nhỏ giữ nguyên; bản nén không nhỏ hơn ⇒ giữ gốc. Đo ảnh chụp thật 2880×1800: PNG 102 KB → WebP 45 KB.
- [x] `ChatComposer`: mọi ảnh thêm vào (dán / chọn / kéo thả) nén trước khi tải; ảnh chờ gửi có ảnh nhỏ + nút ✏️ Chỉnh ảnh (chỉnh xong tải lại); nút 📷 (tooltip mẹo Win+Shift+S) ⇒ chụp ⇒ chỉnh ⇒ "Gửi" = tin riêng chỉ có ảnh (giữ chữ + tệp đang soạn) / "Đính kèm" = vào ô soạn.
- [x] `ChatPane`: `send-files` + cờ `keepDraft` (gộp chung với sticker, không gửi lên API).
- [x] E2E E9 (chặn `files/upload`, giả nguồn màn hình bằng canvas.captureStream) — bộ chat-thong-bao-emoji 9/9 + chat-core/bo-sung/toolbar-zalo/gd2 29/29.
- Lỗi bắt được nhờ e2e: bước chọn vùng kẹp toạ độ theo chính vùng đang kéo (0×0) ⇒ không chọn được vùng — sửa kẹp theo khung ảnh.

## Chưa kiểm
- Hộp chọn màn hình thật của trình duyệt (headless không chụp được) — user thử tay trên :3080.

### Checkpoint — 13/11/2026 ~18:00
Vừa hoàn thành: code + e2e GĐ5; commit + rebase lên gop_db mới (rbac 994cf90bd) + push: hrm-client gop_db 994cf90bd..08fec9dd1.
Bước tiếp theo: deploy TPE (chỉ build client).
