# Fix — Báo cáo SL thị trường: "ngoài KH" lẫn tỉnh của "trong KH"

## Bug
Báo cáo `admin/reports/plan-department-by-employee`, cột "SL thị trường": dòng "Thực hiện NGOÀI KH" đếm cả tỉnh đã thuộc "Thực hiện TRONG KH" (out ⊆ in). Modal "Chi tiết thị trường" của ngoài KH hiện cả tỉnh của trong KH.

## Root cause (đã xác minh)
`PlanImplementSaleByEmployee.php`: phân loại tỉnh in/out theo cờ `fc.delivery_in_market` ở cấp từng hợp đồng rồi `JSON_ARRAYAGG`:
- `CASE WHEN delivery_in_market = 1 THEN province_id` → in_ary
- `CASE WHEN delivery_in_market = 0 THEN province_id` → out_ary
Cùng 1 tỉnh có cả HĐ in (=1) lẫn out (=0) → province_id lọt CẢ 2 mảng; không khử chéo. (`array_unique` chỉ khử trong từng mảng.)
Precedent đúng: code đã làm `array_diff(common, following)` cho khách hàng (dòng ~1800) nhưng quên làm cho province.

## Quy tắc (user xác nhận)
Tỉnh đã thuộc "trong KH" thì KHÔNG tính vào "ngoài KH" → `out_ary = array_diff(out_ary, in_ary)`.

## Fix (đã làm)
- [x] Chèn `$X['e_number_province_out_ary'] = array_values(array_diff(out_ary, in_ary))` ngay trước mỗi điểm `count(out_ary)` — 17 điểm, phủ mọi cấp: mergedItem(×2), item(×2), marketRow(inline), empTotals, co, employeeData(×2), departmentData(×4), companyData(×4). Chỉ động `e_number_province_out_ary`/`_out`; không đụng field doanh số/HĐ/khách hàng/`in_ary`/`province_ary`.
- [x] `php -l` sạch.
- [ ] User test browser: dòng "ngoài KH" chỉ còn tỉnh KHÔNG nằm trong "trong KH"; modal "Chi tiết thị trường" ngoài KH không còn tỉnh của trong KH; tổng/% thị trường nhất quán giữa cấp NV/phòng ban/công ty.

## Phạm vi
- 1 file: `app/Services/Reports/PlanImplementSaleByEmployee.php`. Không đụng controller/print/export (đọc cùng field nên tự đúng).
- Độc lập các thay đổi đang dở khác → commit tách riêng được.

## Fix #2 — Tỉnh "ma" (không tồn tại trong `provinces`)
Triệu chứng tiếp theo: dòng PHÒNG "ngoài KH" count=1 nhưng popup rỗng. Root cause: tỉnh out-only duy nhất còn lại là `province_id=45` — **không tồn tại trong bảng `provinces`** (tỉnh cũ đã sáp nhập/xóa). `searchProvincesSales` tra tên ra rỗng → popup trống dù count đếm 45.
Quyết định user: **(A)** lọc province không tồn tại khỏi count + array.
- [x] Thêm `pruneInvalidProvinces` + `pruneProvinceItem` (cache id tỉnh hợp lệ, lọc các mảng ĐÃ THỰC HIỆN `e_number_province*_ary` + tính lại count & % thị trường; đệ quy `employee`/`markets`; KHÔNG đụng mảng kế hoạch). Gọi tại 4 điểm `return $datas` của 3 entry method.
- [x] Sửa lỗi đệ quy vô hạn (replace_all lỡ đổi `return $datas` trong chính hàm prune) → dùng by-ref tránh OOM.
- [x] php -l sạch; verify tinker: DEPT out=0 (loại tỉnh 45), in_ary giữ nguyên, NV out hợp lệ ([41],[2,41,42],...) vẫn còn.
- [ ] User test browser: dòng PHÒNG "ngoài KH" = 0, popup rỗng nhất quán; popup các tỉnh hợp lệ (in / NV out) hiện đúng tên.
