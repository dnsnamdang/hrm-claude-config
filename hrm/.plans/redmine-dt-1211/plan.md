# Redmine fix-bug-dao-tao-danh-gia — vé Phản hồi + Mới (12/11/2026)

Nhánh: `fix/redmine-dt-1211` (worktree `HRM/hrm-client-dt`, `HRM/hrm-api-dt`) → push `develop`.

## Nhóm 1 — Phiếu yêu cầu hạch toán dịch vụ (`pages/finance/service-accounting-requests`)
- [x] #12102 popup Chọn hợp đồng: × xoá nhanh cho ô Số hợp đồng + Khách hàng (Loại HĐ đã có)
- [x] #12080 màn Sửa cho đổi Kiểu hạch toán + Hợp đồng (như ERP)
- [x] #12067 màn chi tiết: Số hợp đồng là link mở chi tiết HĐ tab mới
- [x] #12134 danh sách: cột Hành động rộng ra, icon không bị cắt

## Nhóm 2 — Bảng tổng hợp thu nhập từ bán hàng (`/sale/sales-income-summary`)
- [x] #12117 tìm nhanh; bố cục bộ lọc như màn khác; phân trang mặc định 10 chữ to; ô "-" để trống
- [x] #12118 chọn năm thì Kỳ bắt buộc (*); nút cấu hình cột
- [x] #12123 thiếu cột; phân trang 10 chữ to; × xoá ô tìm; nút lọc popup chi tiết HĐ
- [x] #12125 popup chi tiết HĐ theo NV: cột thừa/thiếu so ERP
- [x] #12126 Xuất Excel: giãn dòng/cột hiện đủ chữ

Đợt 2 đã push develop: api ec99664a9 / client 4ab883b08 (12/11/2026).
