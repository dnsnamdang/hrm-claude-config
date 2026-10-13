# Fix lỗi "Column 'company_id' is ambiguous" khi JOIN bảng `customers` (gộp DB)

## Nguyên nhân
Gộp DB dùng chung bảng `customers` (bảng gốc của HRM, có sẵn cột `company_id` từ
migration HRM `2021_11_26_..._create_customers_table.php`). Trước gộp, bảng
`customers` phía ERP KHÔNG có `company_id` nên các query ERP JOIN `customers` rồi
dùng `where('company_id', ...)` trần vẫn chạy (chỉ 1 bảng trong join có cột đó).
Sau gộp, `customers.company_id` xuất hiện → trùng tên với `company_id` của bảng
còn lại trong join → MySQL 1052 ambiguous → HTTP 500.

Cột `customers.company_id` là schema hợp lệ của HRM (HRM Customer entity fillable +
quan hệ `company()`, CustomerService scope theo company). ERP KHÔNG dùng cột này
(scope KH qua bảng báo giá). → KHÔNG drop cột; fix bằng cách qualify tên bảng
(khôi phục đúng hành vi trước gộp, KHÔNG đổi logic, KHÔNG ghi data).

## Tasks
- [x] `Services/Warehouse/PrepickIndexReportService.php:160` — `getData()` subquery
      `$prepick` JOIN `prepick_details as pds` + `customers as cm`:
      `where('company_id', ...)` → `where('pds.company_id', ...)`
      (repro 500: /admin/warehouse/warehouse_infos/prepickIndex/exportPrepickIndex)
- [x] Push fix lên gop_db (commit `4c58462a12`)
- [x] Truy quét toàn ERP: query JOIN `customers` + `company_id` trần
      → 65 file nghi ngờ (mức file), phân tích mức query bằng 5 agent + đối chiếu schema.
      KẾT QUẢ: KHÔNG còn vị trí ambiguous runtime nào khác. Mọi query join `customers`
      đều đã qualify `company_id` (f./c./fc./ac./ei./pd./hd./result....). Màn hàng giữ
      là chỗ duy nhất bị vỡ. → không cần sửa thêm gì cho 500.
- [ ] User verify: mở màn báo cáo hàng giữ (prepickIndex + export) không còn 500

## Ghi chú truy quét (không phải lỗi 500 — để tham khảo, KHÔNG sửa nếu user không yêu cầu)
- `PlanImplementSaleReportByGroupCustomer.php:1613` — bare `where('company_id',...)` trong
  method `filterDate()` nhưng đây là DEAD CODE (không được gọi; filter thật là
  `filterSearch`/`elementFilterSearch` đã qualify). Nếu dọn: prefix `account_details.company_id`.
- `WarrantyRepairService.php:522` — `where('wr.company_id',...)` chạy trên Collection (sau
  `->get()`), key không khớp alias → lỗi LOGIC tiềm ẩn (kết quả có thể sai), KHÔNG gây 500.
- Nhiều query có ≥2 bảng cùng mang `company_id` (customers + employee_infos/company_costs...)
  nhưng đang qualify đúng → an toàn; chỉ nổ NẾU sau này ai thêm `company_id` trần vào.

### Checkpoint — 2026-09-28
Vừa hoàn thành: fix PrepickIndexReportService.php:160 (push `4c58462a12` gop_db) + truy quét toàn ERP.
Đang làm dở: chờ user verify màn hàng giữ.
Bước tiếp theo: user mở màn báo cáo hàng giữ + export xác nhận hết 500.
Blocked:

## Ghi chú
- Đã reproduce read-only trên DB gộp: query hiện tại → 1052 ambiguous;
  đổi `pds.company_id` → OK. KHÔNG ghi DB prod.
- Cùng họ lỗi với `.plans/fix-ambiguous-company-id-roles` (gộp thêm cột trùng tên).
