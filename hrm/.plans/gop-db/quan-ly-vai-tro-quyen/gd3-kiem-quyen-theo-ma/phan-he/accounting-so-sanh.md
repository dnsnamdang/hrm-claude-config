# accounting — so sánh mốc trước / sau (GĐ3 Task 8.9)

- Trước: `accounting-truoc.json` (chụp 2 lần liên tiếp trên code HEAD, `ScopeSnapshot diff` = **0 ô khác**). Sau: `accounting-sau.json` (code đã đổi ERP + hrm-api).
- 462 ô = 77 route (72 ERP + 5 hrm-api) × 6 tài khoản (13 pv4 / 207 pv3 / 24 pv2 / 110 pv1 / 148 trộn / 311 không mã). Trạng thái HTTP: {200: 396, 500: 66}; ô trang "không có quyền"/lỗi (so_dong -1): 130.
- **Khớp 461 / 462 ô; lệch 1 ô:**

  - `erp.report.summary_sale.searchData.item` × `tron`: status 200→200, so_dong 7251→7251, ids_hash 3d8245ae98→7d3e6f3fa6

## Ô lệch: `erp.report.summary_sale.searchData.item` × tron (NV 148) — KHÔNG do quyền
- Cùng tổng 7251 dòng, chỉ khác băm NỘI DUNG trang đầu (ô này băm nội dung dòng vì dòng báo cáo không có id).
- Chạy lại đúng ô đó 2 lần trên code MỚI (pv3 + tron, `--only`): cả 2 lần tron = `3d8245ae98` = mốc trước (và = pv3, cùng phạm vi). ⇒ lệch thoáng qua: báo cáo sắp xếp theo cột có giá trị trùng, thứ tự dòng trang đầu không xác định khi MySQL đang tải nặng (lượt chụp sau chạy song song với PHPUnit hrm-api trên cùng máy chủ MySQL).
- Code mới ra cùng câu SQL với code cũ ở mọi mức (AccountingScopeConversionTest `pretend.report.summary_sale.item` 5 nhánh phân biệt, khớp golden).

## Bỏ khỏi mốc HTTP
- `Bỏ khỏi mốc HTTP (chạy > 60 s trên rehearsal, làm sập php -S): erp.account_details.searchData, erp.account_details.searchDataDebtCustomer, erp.account_details.searchDataBalance, erp.account_details.searchDataDebtEmployee, erp.account_details.searchDataBalanceEmployee, erp.account_details.searchDataAccountDetailBook, erp.account_details.searchData.supplier, erp.report.analysis_profit_contract.searchData — phủ bằng AccountingScopeConversionTest (DB::pretend).`

## Ô U8
- Không có (rehearsal 0 người có mã accounting có phạm vi mà scope NULL). Ca "có mã không phạm vi" / "khác công ty" phủ bằng PHPUnit (golden mức null / c2).
