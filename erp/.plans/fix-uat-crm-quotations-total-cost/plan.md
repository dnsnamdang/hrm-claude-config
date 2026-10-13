# Fix uat_crm crash: quotations.total_cost sau gộp DB

## Bối cảnh
Gộp DB: `quotations` nhóm KEEP_HRM → giữ cấu trúc HRM (không có `total_cost`), drop ERP's. App `uat_crm` (dòng dõi ERP TanPhatDev) `App\Employee::getDashboardInfosAttribute()` query `Quotation::...SUM(total_cost)` mỗi lần load dashboard → crash. Báo giá ERP + chức năng dính KHÔNG dùng nữa (user chốt).
Local không lỗi vì ERP local trỏ DB gốc chưa merge (erp.eteksofts/erp_new còn total_cost); server uat_crm trỏ DB merge.

## Quyết định: (A) bỏ code chết
Cho `$week_quotation`/`$day_quotation` (Quotation ERP chết) trả 0/rỗng, không query bảng quotations nữa. Giữ FirmQuotation/Contract/FirmContract (vẫn sống, còn total_cost).

## Tasks
- [ ] Sửa app/Employee.php getDashboardInfosAttribute: 5 nhánh week_quotation → (object)[sl=0,gt=0]; final quotation → collect([])
- [ ] php -l
- [ ] User deploy sang uat_crm (nếu là repo riêng thì áp fix tương tự)
