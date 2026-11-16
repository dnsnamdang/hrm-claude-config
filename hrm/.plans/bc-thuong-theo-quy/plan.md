# Plan — Port "Báo cáo thưởng theo quý" ERP → HRM

Design: `.plans/bc-thuong-theo-quy/design.md` · Nhánh `feature/bc-thuong-theo-quy` (worktree `wt-bonus-quarter-api`, `wt-bonus-quarter-client`). Làm native (user "làm đi").

## Tasks
- [x] 1. BE `Modules/Finance/Services/BonusQuarter/BonusQuarterScope.php` (CODE `accounting.bao_cao_thuong_nang_suat_thang.view`)
- [x] 2. BE `BonusQuarterReportService`: rows (UNION firm/wr bám ERP 1:1, filter `sc.date_accounting`), tree 3 cấp, totals, search (phân trang theo phòng), detailRows, periods
- [x] 3. BE `BonusQuarterPrintTable` (bố cục bản in ERP, '-' cho 0)
- [x] 4. BE `BonusQuarterReportController` + routes `finance/bonus-quarter-report/{meta,/,detail,export,print-list-data}`; catalog thêm `hrm`
- [x] 5. BE feature test (quyền own/company/all + validate ngày + popup ngoài phạm vi)
- [x] 6. FE page `pages/sale/bonus-quarter-report/index.vue` + popup + Excel + In; menu sale-hub
- [x] 7. Đối số ERP SQL quý 2/2026 trên erp_hrm_check (6 tổng + 1 phòng + 1 NV)
- [x] 8. Playwright kiểm màn
- [x] 9. Hỏi user commit/merge/push; cập nhật memory

## Kết quả Playwright (16/11/2026, Q2/2026, Tổng công ty)
- Kỳ 2 tự điền 01/04–30/06 + khoá ô ngày; Tìm kiếm 200, 22 phòng/3 trang; dòng Tổng cộng = đối chiếu ERP (5,517,864,721).
- Bỏ tích "Hiện chi tiết HĐ": 0 dòng HĐ, giữ 10 phòng/106 NV; bật lại đủ 5,422 dòng HĐ.
- Popup NV 10510014: /detail 200, 601 HĐ, tổng 107,778,931 = 2 phòng của NV (93,164,396 + 14,614,535) — đúng ERP (popup chỉ truyền employee_id + bộ lọc, không lọc phòng). Excel chi tiết OK.
- Xuất Excel chính: 7,968 dòng, ô số thật numFmt `#,##0;-#,##0;"-"`, Tổng cộng khớp.
- In: cả kỳ 7,777 dòng → component in chung chặn trần 2,000 dòng (hướng dẫn dùng Excel); lọc Số HĐ `HĐ_TPE_HN_KD2_26` (598 HĐ, trim đúng) in ra khổ ngang 3 cấp đúng. Letterhead local 404 = môi trường.
- Trang 2: STT tiếp tục từ 11, dòng tổng giữ nguyên. Nút In ↔ Xuất Excel cách 12px. Console chỉ lỗi socket :8891 sẵn có.
