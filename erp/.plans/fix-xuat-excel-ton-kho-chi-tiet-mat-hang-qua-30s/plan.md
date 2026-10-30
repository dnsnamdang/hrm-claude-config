# Báo cáo tồn kho chi tiết theo mặt hàng: xuất Excel lỗi 500 (quá 30s)

Không Redmine (prod `warehouse_reports/stockCardDetail`) · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 30/10/2026 (@junfoke)
- [x] 30/10/2026 — Xử lý: xuất Excel (dưới 150 mặt hàng chạy ngay, không qua mail) lỗi "Maximum execution time of 30 seconds". Code cũ 2024, dữ liệu tăng: `Product::warehouseReportDetailSearchData` tải toàn bộ lịch sử log vị trí rồi `collect()->where()` lại cho mỗi hàng × công ty × lô, và truy vấn lại phiếu nhập/HĐ cho từng lô. Sửa: duyệt log 1 lần nhóm theo công ty + mặt hàng + dòng đầu từng lô, cache phiếu nhập/HĐ theo phiếu; kết quả giữ nguyên, màn xem cũng nhanh hơn. Commit `38ecb99187` — đã lên gop_db + develop_02.
- [ ] Chưa đo thời gian thật trên prod; còn chậm thì bật lại điều kiện ngày cho truy vấn log (hỏi user trước).
