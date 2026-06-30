# Filter Mã hợp đồng cho báo cáo Tổng hợp bán hàng

## Mục tiêu
Thêm 1 ô text 'Mã hợp đồng' lọc báo cáo summary_sale theo mã HĐ (cả firm_contracts lẫn wr_service_contracts), LIKE %...%.

## Thay đổi
- FE summarySale.blade.php: input contract_code + form init + payload.
- BE SummarySaleReportService::getData: áp (f.code LIKE OR wr.code LIKE) cho 3 nhánh (xuất bán / bán-mượn / nhập trả lại qua whereExists phiếu xuất gốc).

## Tasks
- [x] BE: filter contract_code cho export + borrow + return (whereExists join f2/wr2 + f3/wr3). php -l sạch.
- [x] FE: input "Mã hợp đồng" + DEFAULT_FORM contract_code + payload (params=copy(form) → tự gửi).
- [ ] User verify browser (lọc 1 mã HĐ → chỉ ra SP của HĐ đó; nhập 1 phần mã vẫn ra do LIKE).

### Checkpoint — 2026-06-29
Code xong trên **master** (theo yêu cầu), php -l sạch, **chưa commit**. Sửa 2 file: `resources/views/reports/summarySale.blade.php` + `app/Services/Reports/SummarySaleReportService.php`. Bước tiếp: user test browser.
