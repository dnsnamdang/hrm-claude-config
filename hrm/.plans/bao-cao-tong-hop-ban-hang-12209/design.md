# BC tổng hợp bán hàng — UI (#12209)

Màn `/finance/sale-summary-report` (client `pages/finance/sale-summary-report/` + `components/sale-by-product-report/`
mode `summary`; api `SaleSummaryReportController` + `SaleByProductReportService::forSummary()`).
Bộ component `sale-by-product-report` DÙNG CHUNG với `/sale/sale-by-product-report` → mọi thay đổi chỉ bật ở mode summary,
màn theo mặt hàng giữ nguyên. Chỉ làm đúng 7 mục vé.

## Mục vé

| # | Mục | Cách làm |
|---|-----|----------|
| 1 | Công ty/PB/BP/NV lên hàng đầu | summary: ô `org` đứng đầu `filterFields` |
| 2 | Tùy chỉnh cột | `columnCustomizationMixin` + `ColumnCustomizationModal` (khoá STT, Hàng hóa), nút `ri-layout-column-line` trên panel |
| 3 | Icon và tên màn lệch | Căn lại tiêu đề trên thanh trên cùng (kiểm Playwright) |
| 4 | Thống kê 2 cụm | Khuôn `pages/transport/components/TransportReportSummary.vue`: **Tổng hợp bán hàng** (SL bán thực tế · Doanh số bán · Thành tiền net) + **Hiệu quả kinh doanh** (Thành tiền vốn · Chênh lệch · Lãi lỗ) |
| 5 | Phân cấp Nhóm mặt hàng → Hàng hóa | Dòng nhóm (caret, STT 1, tổng của nhóm) → dòng hàng (STT 1.1); dòng Tổng cộng |
| 6 | Mã hàng chữ nhỏ xám sau tên | Ô Hàng hóa: `Tên` + `mã` nhỏ xám; bỏ cột Mã riêng |
| 7 | Số là link mở popup chi tiết | Dòng hàng → popup chi tiết mặt hàng (`item-list`); dòng nhóm / ô thống kê → popup phát sinh mọi mặt hàng (`all-items`, lọc theo nhóm) |

## Quyết định

- Công thức số liệu GIỮ NGUYÊN (khớp ERP). "Lãi lỗ" vẫn là số tiền (mockup ghi % là minh hoạ).
- BE (chỉ mode summary): mỗi dòng thêm `group_id`, `group_name` (`products.group_id` → `groups`), `group_no`, `item_no`;
  sắp theo tên nhóm rồi mã hàng, hàng chưa có nhóm xuống cuối nhóm "Chưa phân nhóm". `groups` = tổng theo nhóm tính trên
  TOÀN BỘ kết quả lọc. Phân trang vẫn theo dòng hàng; nhóm cắt qua 2 trang thì trang sau hiện lại dòng nhóm (tổng cả nhóm).
- Mở thêm 3 route `all-items` cho `sale-summary-report` (đã có ở màn theo mặt hàng). Lọc nhóm "Chưa phân nhóm" = `group_none=1`.
- In / Excel: giữ khuôn phẳng hiện tại (vé không nêu).

## Kiểm tra

- phpunit `Modules/Finance/Tests/Feature/SaleSummaryReport*`.
- Playwright 127.0.0.1:3000: thứ tự lọc, Tùy chỉnh cột, tiêu đề, 2 cụm thống kê, cây nhóm, bấm số mở popup; màn
  `/sale/sale-by-product-report` không đổi.
