# Báo cáo luân chuyển hàng hóa: tối ưu để không làm quá tải CPU DB

Không Redmine (prod sập chiều 04/11, anh Mạnh Cường tạm khoá route `6fd618dce3`) · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`
Liên quan: [arriving-qty-tan-goc](../arriving-qty-tan-goc/design.md), [fix-bao-cao-luan-chuyen-hang-dang-ve-phantom](../fix-bao-cao-luan-chuyen-hang-dang-ve-phantom/plan.md)

## Ngày 04/11/2026 (@junfoke)
- [x] 04/11/2026 — Phân tích slow log: 140/142 truy vấn chậm là cùng 1 câu "hàng đang về" (`ArrivingQtyService::tonFor`, ~11s/lần, trả 6.088 dòng — tính toàn bảng công ty × SP rồi lấy 1 số). Route `stock-incoming` bị 3 màn Phiếu đặt hàng / YCĐH gốc / Tiếp nhận YCĐH gọi **mỗi dòng SP một lần** ⇒ hàng chục câu toàn bảng song song (149 kết nối treo).
- [x] 04/11/2026 — `tonFor` / `tongFor` chỉ tính đúng SP cần (~0,9s → ~0,07s, khớp 200/200 cặp); báo cáo luân chuyển tính "hàng đang về" 1 lần/request vào bảng tạm có index (~7,4s → ~1,3s/trang); áp cùng cách cho BC tồn kho theo công ty và BC cảnh báo tồn kho (`Product.php`). Đối chiếu SQL gốc lệch 0.
- [x] 04/11/2026 — Phân trang 2 bước `paginateData()` (`StockTransferReportService`): bước 1 đếm + lấy id 50 SP của trang từ bảng SP đã lọc, bước 2 chạy báo cáo chỉ cho 50 SP đó; 92 chỗ lọc SP đổi sang `whereIn`; controller `searchData` dùng hàm mới. Đo local: trang 1 7,2s → 2,6s; trang 137 8,0s → 1,5s; lọc hãng + 2 năm 10,6s → 1,8s; 50/50 dòng × 53 cột khớp. Lọc "Còn tồn / Hết tồn" giữ đường cũ (chưa tối ưu, ~9,7s).
- [x] 04/11/2026 — Mở khoá báo cáo: bỏ middleware `block.routes` ở nhóm `stock-transfer/report` (`routes/web.php`), gỡ danh sách 16 route tạm khoá + đoạn trả 503 trong `BlockSpecificRoutes.php`.
- [x] 04/11/2026 — Commit `bbe5fa53f2` "fix xử lý báo cáo luân chuyển" (6 file), đã lên `origin/gop_db`.
- [ ] Sau deploy theo dõi slow log vài ngày; nếu còn câu ~10s là bộ lọc Còn tồn/Hết tồn hoặc tài khoản DB prod thiếu quyền tạo bảng tạm (log warning `ArrivingQtyService: không tạo được bảng tạm`).
