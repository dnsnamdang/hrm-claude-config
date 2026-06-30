# Fix lỗi 500 báo cáo Market Plan Department — Unknown column 'f.part_id'

## URL / Bối cảnh
- `/admin/reports/market-plan-department` (ReportController@marketPlanDepartmentSearchData)
- Payload có `part_id=27` → SQL lỗi `Unknown column 'f.part_id'`.

## Nguyên nhân
- `PlanDepartmentReportService::elementFilterSearch()` áp filter `f.part_id` (dòng 900 nhánh quyền `is_part`, dòng 916 filter theo `$request->part_id`).
- Hàm này dùng chung cho 2 nguồn: `firm_quotations as f` (CÓ part_id) và `wr_service_quotations as f` (KHÔNG có part_id).
- Khi query service chạy → `f.part_id` không tồn tại → 42S22. Report 500 mỗi khi có filter part hoặc user chỉ có quyền "bộ phận".
- Cả 6 subquery (3 firm + 3 service) đều `leftJoin('employees as e', e.id = f.created_by)` → `e.part_id` luôn có sẵn (employees có part_id; đã dùng ở dòng 841/856).

## Cách sửa (tối thiểu, 1 chỗ — `elementFilterSearch`)
- `part_id` KHÔNG nằm trên `employees` mà trên `employee_infos`; và `employee_infos as ef` chỉ được join ở vài query (510, 602) chứ không phải cả 6 → không có cột nào (`f`/`e`/`ef`) hợp lệ cho cả 6.
- Cột chung duy nhất ở mọi query là `f.created_by`. Nên lọc part qua **subquery người tạo thuộc bộ phận**:
  `whereIn('f.created_by', fn => select emp.id from employees emp join employee_infos einfo where einfo.part_id = ?)`.
- Áp tại 2 chỗ trong `elementFilterSearch`: nhánh quyền `is_part` + filter `$request->part_id`.
- KHÔNG đụng `filterSearch` (plan-side, alias `e` = `market_employee_plans` vốn CÓ `part_id`).
- Không thêm cột DB, không migration, không đụng 6 call-site.

## Tasks
- [x] Xác minh `wr_service_quotations` thiếu `part_id`, `firm_quotations` có; `part_id` thực ra ở `employee_infos`; `ef` không join đủ 6 query
- [x] Sửa `elementFilterSearch`: 2 chỗ part_id → subquery theo `f.created_by` thuộc part
- [x] `php -l` sạch
- [x] Verify tinker (user 13): 3 method searchData chạy OK, hết lỗi; part 27 rỗng (0 NV — đúng); part có data (part 10) trả rows>0
- [ ] User reload trang xác nhận

## Lưu ý
- Đổi sang `e.part_id` cũng làm nhánh firm lọc theo part-của-người-tạo thay vì part-trên-báo-giá. Chấp nhận được vì: (a) trước đây luôn crash khi có part filter nên không có hành vi đúng để phá; (b) part trên firm_quotation vốn set theo người tạo.
