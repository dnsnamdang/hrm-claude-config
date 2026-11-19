# #12213 — Bảng tổng hợp thu nhập từ bán hàng: UI báo cáo mới (19/11/2026)

Màn: Bán hàng › Bảng tổng hợp thu nhập từ bán hàng (`pages/sale/sales-income-summary`). Khuôn bám `pages/sale/bonus-month-report` (#12201) + `pages/sale/monitor-contract-implement` (#12164).

## Mục vé

| Vé | Mục | Cách làm |
| --- | --- | --- |
| 12213 | Khối thống kê | `components/SalesIncomeStats.vue` (CSS `.rsum` khuôn `MonitorContractStats`): kỳ + 6 nhóm Quy mô · Doanh số tiêu chuẩn · Thưởng năng suất (tháng/quý/lũy tiến) · Thưởng khác · Tổng thu nhập · Bị trừ. BE `search()` → `total` thêm `department_count` / `employee_count` (đếm trên toàn tập đã lọc) |
| 12213 | Bảng | `components/SalesIncomeTable.vue`: dòng TỔNG cam, dòng phòng thu gọn/mở rộng, dòng NV; mỗi tiêu đề cột có ⓘ mô tả; `ReportPagination` |
| 12213 | Bấm số → popup | Số ở dòng NV mở popup chi tiết HĐ sẵn có (`openDetail`) |
| 12213 | Nút trên khung lọc | `#header-actions`: Cấu hình cột · In báo cáo · Xuất Excel; `#title-suffix`: ReportInfoTip "MỤC ĐÍCH BÁO CÁO" |
| 12213 | Cấu hình cột | `columnCustomizationMixin`; STT + Phòng ban/Nhân viên khoá |
| 12213 | Excel chọn trường | `ExportFieldsModal` (mặc định = cột đang hiện); `exportSalesIncomeSummary(..., keys)` giữ thứ tự cố định, luôn có STT + Nhân viên |
| 12213 | Bộ lọc | Đơn vị tổ chức lên đầu; bấm Tìm kiếm hiện "Đang tải dữ liệu..." ngay; bỏ tp-card / title / title-icon cũ |

## Quyết định

- Chỉ số ở dòng NV bấm được: API chi tiết cần `employee_id`. Khối thống kê, dòng TỔNG, dòng phòng chỉ hiển thị.
- Bị trừ quá hạn > 0 tô cam `#9a5326`, không dùng đỏ.
- Id cột Excel trùng id cột bảng (`stt`, `employee`, key tiền) → không cần map khoá.

## Kiểm tra

- `php artisan test` SalesIncome — 10 pass.
- Playwright 01/01/2025–30/11/2026: 22 phòng · 175 NV; khối Tổng thu nhập 26,546,825,699 = dòng TỔNG.
- Bấm số NV 11010063 → popup "Chi tiết hợp đồng của 11010063 - Nguyễn Thành Bộ".
- Ẩn cột Thưởng năng suất tháng → bảng còn 12 cột, mọi dòng 12 ô; popup Excel mặc định bỏ tích đúng cột đó.
- Excel chọn 2 trường → file có STT · Nhân viên · Tổng thu nhập · Bị trừ quá hạn, dòng Tổng cộng khớp.
