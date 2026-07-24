# BC bảo lãnh — chế độ xem theo thời gian cập nhật bảo lãnh

## Mục tiêu

Màn `contract/reports/guarantee_contract`: thêm checkbox **"Xem theo cập nhật mới nhất"** trong bộ lọc. Khi bật, báo cáo chuyển sang **danh sách phẳng từng dòng bảo lãnh** sắp theo thời gian lưu tab bảo lãnh (dự thầu/thực hiện HĐ) mới nhất lên đầu — không gom theo khách hàng, cùng 1 KH có thể xuất hiện nhiều hàng rời rạc.

## Quyết định lớn (đã chốt với user 2026-07-09)

1. **Đơn vị sort = từng dòng bảo lãnh** (không rowspan, không block chứng từ) — bảo lãnh dự thầu và thực hiện của cùng chứng từ có thể nằm xa nhau.
2. **UI = checkbox trong bộ lọc**, cạnh "Số chứng thư trống", lưu localStorage cùng filter state.
3. **Cột mới "Thời gian cập nhật"** (`dd/mm/yyyy HH:mm`) sau "Tên khách hàng", chỉ hiện ở chế độ mới.
4. **Phương án A**: thêm param `view_mode=latest_update` vào `GET category/reports/guarantees`, BE trả danh sách phẳng qua resource mới `ReportGuaranteeFlatResource`; response mặc định giữ nguyên.
5. Excel xuất theo đúng chế độ đang xem.
6. **Không migration** — lưu tab bảo lãnh là xóa-tạo-lại nên `updated_at` của dòng bảo lãnh = lần lưu tab gần nhất; sort `updated_at` DESC + `id` DESC.

## Phạm vi file

- BE: `ReportService.php` (nhánh không groupBy), `ReportsController.php` (chọn resource), resource mới `Reports/ReportGuaranteeFlatResource.php`.
- FE: `pages/contract/reports/guarantee_contract/index.vue` (checkbox, nhánh render bảng phẳng, cột mới, Excel).

Người phụ trách: @khoipv
Spec chi tiết: `docs/superpowers/specs/2026-07-09-bc-bao-lanh-xem-theo-cap-nhat-design.md`
