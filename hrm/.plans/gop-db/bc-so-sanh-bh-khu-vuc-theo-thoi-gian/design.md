# Báo cáo so sánh số liệu bán hàng theo khu vực chi tiết theo thời gian — design (@junfoke, 2026-11-17)

Port ERP `report.compareContractByTimes` → HRM `/sale/compare-contract-by-time-report` (Bán hàng › Tổng hợp & so sánh). Chỉ đọc.
Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-17-bc-so-sanh-bh-khu-vuc-theo-thoi-gian-design.md`.

## Quyết định đã chốt (user 17/11/2026)
1. Trạng thái HĐ: Có hiệu lực / Đang quyết toán / Đã quyết toán (ERP lọc nhầm status 2 = Chờ duyệt / phiếu bảo hành).
2. Phụ lục bổ sung / giảm: như ERP — mỗi phụ lục 1 hợp đồng, cộng dương.
3. Quyền: mã mới `sale.bao_cao_so_sanh_so_lieu_ban_hang_theo_khu_vuc_chi_tiet_theo_thoi_gian.view` (4 mức), bắt buộc ở route.
4. Mốc thời gian: ngày tạo hợp đồng như ERP.

## Khác ERP (sai rõ) — chi tiết ở spec mục 3
Chỉ đọc quý / tháng của kiểu so sánh đang chọn · tỷ lệ trống khi kỳ cố định = 0 · xếp theo mã tỉnh · nhãn bản in "hợp đồng".
