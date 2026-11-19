# #12164 — BC theo dõi thực hiện hợp đồng: QA UI (19/11/2026)

Màn: Bán hàng › Báo cáo theo dõi thực hiện hợp đồng. Khuôn bám `pages/sale/bonus-month-report` (#12201).

## Mục vé

| Vé | Mục | Cách làm |
| --- | --- | --- |
| 12164 | 1. Khối thống kê | `components/MonitorContractStats.vue`: kỳ + 4 nhóm (Quy mô · Doanh số · DSTC · Công nợ). BE `summary` trả thêm `department_count` / `employee_count` / `contract_count` |
| 12164 | 2. Màu | Màu nhóm theo khuôn rsum (`SaleSummaryStats`); Còn nợ tông cam `#9a5326` (KHÔNG đỏ — đỏ chỉ cho lỗi validate) |
| 12164 | 3. Thu gọn / mở rộng cây | ĐÃ CÓ trước vé (nút ▸ dòng phòng / NV) |
| 12164 | 4. Đổi tên cột | ĐÃ CÓ trước vé |
| 12164 | 5. Lọc theo cấp | ĐÃ CÓ trước vé (select "Tất cả cấp" ở tiêu đề cột) |
| 12164 | 6. Bấm số → popup chi tiết | BE `GET finance/monitor-contract-implement/detail` (`MonitorContractDetailService`, dùng chung bộ đệm với bảng). Dòng Tổng / phòng / NV / khối thống kê → danh sách HĐ có giá trị ≠ 0; dòng HĐ (cột Thực thu, DS thực xuất theo HĐ, Công nợ) → bút toán. Popup `MonitorContractDetailModal.vue` |
| 12164 | 7. Cấu hình cột | `columnCustomizationMixin` + `ColumnCustomizationModal`, khoá `sale_monitor_contract_implement_cols`; STT + cột cây khoá. Colspan dòng tổng / phòng / NV tự co theo cột đang hiện |
| 12164 | 8. Nút In / Excel trên khung lọc | ĐÃ CÓ trước vé |
| 12164 | 9. Excel chọn trường | `ExportFieldsModal` (mặc định = cột đang hiện); `exportMonitorContractImplement(..., keys)` giữ thứ tự cố định, luôn có STT + Hợp đồng |

## Quyết định

- Mục 3/4/5/8 đã có trên develop trước khi vé được ghi — khả năng QA test bản trước deploy; không sửa.
- Ô ở dòng HĐ chỉ bấm được với cột có nguồn bút toán (`revenue_contract`, `income_money`, `income`, `incomed`, `income_remain`); cột DSTC / Giá trị HĐ là số tính, không có chứng từ để liệt kê.
- Tổng popup luôn bằng số đã bấm vì đọc cùng tập dữ liệu với bảng (test `thong ke va popup chi tiet khop o`).

## Kiểm tra

- `php artisan test Modules/Finance/Tests/Feature/MonitorContract*` — 15 pass.
- Playwright 01/01–31/12/2025 (8,506 HĐ): popup Còn nợ tổng 1,024,690,686,504 = khối thống kê; DS thực xuất theo HĐ 1,347,003,701,209 = khối thống kê; ô dòng HĐ ra popup bút toán, tổng khớp ô.
- Ẩn 3 cột → mọi dòng đủ 11 ô, không lệch.
- Excel chọn 4 trường → file đúng 4 cột, tiêu đề 2 tầng gộp đúng.
