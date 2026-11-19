# sale — so sánh mốc trước / sau (GĐ3 Task 8.16)

- Trước: `sale-truoc.json` — chụp 2 lần trên cây = snap-8.15c (HEAD rbac hrm-api dd62184a3 · TanPhatDev e612efd1ce · hrm-client db0899edf) trước khi sửa:
  2.121 ô, **2 ô khác** giữa 2 lần — `erp.report.bySalesStaffSearchData` (cty4, pv2): cùng `so_dong`, khác `ids_hash` ⇒ báo cáo không ORDER BY ("không thứ tự", không sửa query).
- Sau: `sale-sau.json` (sau khi đổi code 3 repo). 14 ô `erp.report.marketPlanAreaDepartmentSearchData` / `erp.report.marketPlanAreaMonth` chụp lại riêng
  (lượt đầu status 0/500 do PHPUnit golden chạy đồng thời làm nghẽn php -S); chụp lại không tải ⇒ khớp.
- Lệnh: `tools-8.15/sosanh.py sale-truoc.json sale-sau.json` (so status + so_dong + ids_hash + cờ) ⇒ **lệch 0**.

## Kết quả
- 2.121 ô (303 route × 7 tài khoản: ERP 281 route, hrm-api 22): **2.121/2.121 khớp, 0 lệch**. Không ô U8 (rehearsal: 0 dòng `role_has_permissions` mã sale có phạm vi mà scope null).
- Trạng thái trước = sau: {200: 1857, 500: 162, 403: 95, 422: 7}.
- 119/303 route khác nhau giữa các tài khoản (mốc có nghĩa); phần còn lại là bảng rỗng trên rehearsal (contracts, quotations, service_contracts…), trang không lọc theo quyền, hoặc lỗi sẵn.
- Ô lỗi sẵn cả trước lẫn sau (500, 28 route — tham số báo cáo / lỗi SQL "Out of sort memory" của rehearsal / trang `…/all` lỗi sẵn): contract_annex/quotations/service_contract_annex/service_contract_addition_annex `page.all`, division_department `page.forApprover`, market/sales_department_plan searchData (một phần TK), 15 báo cáo searchData (revenueContract, bonusBusinessContract, marketCommodity, marketPlanDepartment/GroupCustomers/DepartmentGroupCustomers/DetailDepartmentGroupCustomers/CompareByProvince/AreaDepartment/ProvinceTimes, handleDebtBad/OverDue, revenueStandardContract, compareContractByProvince), customerDebtDetailsData / customerDebtDetailByEmployeeData, quotation_count.print.
- 5 báo cáo > 45–60 s bỏ khỏi mốc HTTP (phủ bằng golden): marketPlanAreaMonthSearchData, marketPlanDepartmentByCustomerSearchData, salePlanAreaByTimeSearchData, planDepartmentByGroupCustomerSearchData, salesDepartmentGroupCustomerSearchData. Chậm nhất còn lại: `erp.market_company_plan.show` 117 s (6 id) — vẫn trả 200.

## Số tiêu biểu (so_dong trước = sau)
- `erp.settlement_contract.searchData.all`: pv4=16841, pv3=11109, pv2=1444, pv1=612, tron=0, cty4=0, khong_ma=0
- `erp.market_employee_plan.searchData.none`: pv4=587, pv3=0, pv2=64, pv1=4, tron=0, cty4=0, khong_ma=0
- `erp.sales_company_plan.searchData.none`: pv4=10, pv3=0, pv2=4, pv1=4, tron=0, cty4=4, khong_ma=0
- `erp.report.monitorContractImplementSearchData`: pv4=16605, pv3=9864, pv2=1450, pv1=569, tron=9864, cty4=0, khong_ma=0
- `erp.report.revenueStandardEmployeeSearchData`: pv4=27, pv3=13, pv2=17, pv1=8, tron=13, cty4=0, khong_ma=0
- `erp.home.approveList`: pv4=100, pv3=37, pv2=22, pv1=16, tron=0, cty4=0, khong_ma=2
- `api.customer_debt_details`: pv4=25345, pv3=25345, pv2=2084, pv1=794, tron=0, cty4=3204, khong_ma=0
- `api.transport_cost.index`: pv4=22, pv3=15, pv2=1, pv1=1, tron=0, cty4=2, khong_ma=15
- `api.bsa.index.all`: pv4=59, pv3=59, pv2=0, pv1=0, tron=0, cty4=0, khong_ma=0

## Phủ thêm bằng golden (code cũ ↔ code mới, cấp theo TỪNG mã)
- ERP `tests/Feature/Rbac/SaleScopeConversionTest` (8 test phần): 624 ca (109 searchByFilter × loại, 231 canX × 13 trạng thái × 3 biến thể, 30 hàm báo cáo/Datatable/dịch vụ,
  104 trang blade/middleware/menu qua HTTP — cờ + băm tập link + showSelection, 149 JSON báo cáo/danh sách qua HTTP — tổng + băm dòng + băm SQL nghiệp vụ (khoảng ngày năm 2000), approveList)
  × mức none/flat/mix/only:mã/mã@s4…s1/null/c2 = **4.997 ô**. Golden sinh ở cây HEAD (2 lần trùng), ca bổ sung sinh bằng `RBAC_LEGACY_SRC` (bản HEAD 108 file app/ — đối chứng: khớp golden HEAD mọi ô cũ kể cả trang). Code mới: 8/8 phần xanh.
- hrm-api `tests/Feature/Rbac/SaleScopeConversionTest`: 78 ca × mức = 665 ô (Entity mua dịch vụ ×3, YC vận chuyển, WrServiceContract, báo cáo công nợ KH ×3, chi phí VC theo NVKD, PrepickTrackingScope, PriceViewScope ×3, CustomerManagerService firm ×2, HĐ dự án TKT) — xanh; đối chứng `RBAC_LEGACY_SRC` xanh; đột biến CustomerDebtScope ⇒ đỏ 18 ô.
- Ca thiếu tài khoản thật (chỉ golden): mã phạm vi null, mã ở công ty khác (c2), từng mã riêng, mức bộ phận.
