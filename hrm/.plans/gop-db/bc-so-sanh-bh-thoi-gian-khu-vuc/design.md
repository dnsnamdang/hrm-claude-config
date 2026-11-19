# Báo cáo so sánh số liệu bán hàng theo thời gian chi tiết theo khu vực — design (@junfoke, 2026-11-18)

Port ERP `report.compareContractByProvince` → HRM `/sale/compare-contract-by-province-report` (Bán hàng › Tổng hợp & so sánh). Chỉ đọc.
Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-18-bc-so-sanh-bh-thoi-gian-khu-vuc-design.md`.

So từng tháng (năm, từ tháng → đến tháng) giữa nhóm tỉnh cố định và nhóm tỉnh so sánh: SL khách, SL hợp đồng, giá trị (doanh thu tính
lại) — hợp đồng có hiệu lực / đang / đã quyết toán, đã phát sinh công nợ TK 1311, theo ngày duyệt.

## Quyết định đã chốt (user 18/11/2026)
1. Quyền: mã mới `sale.bao_cao_so_sanh_so_lieu_ban_hang_theo_thoi_gian_chi_tiet_theo_khu_vuc.view` (4 mức), bắt buộc ở route.
2. Chênh lệch = so sánh − cố định (có dấu), tỷ lệ = chênh lệch / cố định × 100 (giống màn theo khu vực chi tiết theo thời gian).

## Khác ERP (sai rõ) — chi tiết + bằng chứng ở spec mục 3
Bỏ join quyết toán nhân doanh thu · đếm HĐ theo (bảng, id) · phụ lục dịch vụ mỗi loại 1 lần · dòng hàng `UNION ALL` · hỗ trợ kế toán
1 bản ghi · cột "Tháng" · chặn Đến tháng < Từ tháng · in đủ dòng · không bảng tạm.
