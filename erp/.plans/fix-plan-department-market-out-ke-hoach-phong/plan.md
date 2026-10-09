# Fix: SL thị trường "ngoài KH" tính sai ở cấp phòng (Nghệ An) — Cách B1

## Bug
Báo cáo `admin/reports/plan-department-by-employee`. Dòng tổng phòng "SL thị trường thực hiện ngoài KH" đếm nhầm tỉnh thuộc kế hoạch phòng.
- Gộp cấp phòng chỉ `out_ary = array_diff(out_ary, in_ary)` → chỉ khử tỉnh ĐÃ có NV bán trong KH.
- Tỉnh thuộc **kế hoạch phòng** nhưng kỳ đó chưa NV nào bán trong KH → lọt sang "ngoài KH".
- Ca gốc: phòng 5 (Thiết bị ô tô 2), tháng 1/2026, Nghệ An hiện = ngoài KH.

## Quyết định: Cách B1 (đã xác nhận nhất quán với code hiện tại)
- Bằng chứng: tiền/KH/SL in-out gộp cấp phòng = CỘNG DỒN theo phân công cá nhân (dòng 257-258/320-321), array_diff chỉ đụng ĐẾM TỈNH (dòng 1885). → Ca "NV không phân công bán ở tỉnh thuộc KH phòng" hiện đã giữ tiền của NV đó ở "ngoài KH".
- **B1: chỉ sửa ĐẾM TỈNH** ở cấp phòng + công ty + tổng: khử khỏi `e_number_province_out_ary` các tỉnh thuộc **kế hoạch phòng** (đưa vào `_in_ary`). KHÔNG đụng tiền/KH/SL. KHÔNG áp cấp cá nhân.

## Tasks
- [x] Verify BEFORE: phòng 5 in=10/out=3, Nghệ An(20) ở OUT & thuộc KH phòng → BUG xác nhận. Phòng 50 (đối chứng): Nghệ An ở out nhưng KHÔNG thuộc KH phòng.: chạy report tháng 1/2026, xác nhận phòng 5 có Nghệ An trong e_number_province_out_ary
- [x] Nguồn 'tỉnh KH phòng' = number_province_ary (mẫu số kế hoạch). "tỉnh thuộc kế hoạch phòng" (mảng plan province theo phòng — number_province_ary?)
- [x] Sửa getProcessSales (dòng ~1885): thêm khử out theo number_province_ary, CHỈ khi $condition∈{department_id,company_id} (không áp created_by/province_id). Hàm merge dùng chung mọi cấp nên phải guard theo condition. khử out theo plan-province-phòng tại các điểm gộp cấp phòng/công ty/tổng
- [x] php -l sạch
- [x] Verify AFTER: phòng 5 in=12/out=1 (Nghệ An + 1 tỉnh nữa vào in), tổng in+out=13 giữ nguyên (% không đổi). Phòng 50 KHÔNG đổi (0/18). Tiền/KH/SL không đụng.: Nghệ An hết ngoài KH; các tỉnh khác + tiền không đổi
- [ ] User reload xác nhận

## Nguồn tham chiếu
- Memory: erp-plan-department-market-out-kh-bug
- File: app/Services/Reports/PlanImplementSaleByEmployee.php (điểm merge ~1492, ~1885, ~4183, ~4963)
- Test: DB erp_new, Auth::loginUsingId(13), getPlanDepartmentReportSearchData
