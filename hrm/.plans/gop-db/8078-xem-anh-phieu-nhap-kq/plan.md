# #8078 — [App] Phiếu nhập kết quả: bấm vào ảnh không xem to được — @cuong61n

- [x] Kiểm 19/10/2026: ĐÃ SỬA từ 07/08/2026 (TPE_APP commit 602ef9f, có trên develop/tpe/thanhan/duclocson). Ảnh hạng mục đã gom về mục "File/ảnh đính kèm"; `AppLocalFileView` bấm vào ảnh → mở toàn màn hình (PhotoView, chụm phóng to, nút X đóng). Màn xem và màn duyệt dùng chung component (readOnly)
- [x] Test simulator: phiếu TPE.PNKQ.2026007047 (chờ duyệt kết quả) → bấm ảnh công trình mở toàn màn hình, X đóng về đúng phiếu ✓ (ảnh local là ảnh tạm, đã xoá; chụm 2 ngón không test được bằng mobile-mcp)
- Ghi chú: app hiện không có thao tác "Duyệt" phiếu nhập kết quả — duyệt làm trên web
