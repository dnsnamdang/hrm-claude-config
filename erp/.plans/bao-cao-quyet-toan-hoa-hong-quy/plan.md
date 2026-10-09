# Plan — Fix cột DS tiêu chuẩn báo cáo quyết toán hoa hồng quý

Xem `design.md` cho bối cảnh + quyết định Hướng A.

## Task
- [x] T1: Bỏ filter `sc.date_accounting` trong `settlement_firm` của `getDataFirm`
- [x] T2: Bỏ filter `sc2.date_accounting` trong `settlement_firm_lead` của `getDataFirm`
- [x] T3: Bỏ filter `sc.date_accounting` trong `settlement_firm` của `getDataWr`
- [x] T4: Bỏ filter `sc2.date_accounting` trong `settlement_firm_lead` của `getDataWr`
- [x] T5: Verify trên erp_new — `php -l` sạch; subquery sau fix trả DS 697.256.252 cho (6234,66); trước fix + lọc tháng 8 = 0 dòng (đúng bug cũ); HĐ đồng bộ (25268/20934/25083) giữ nguyên 1.710.000 / 14.386.500 / 20.524.779 (không regression)
- [ ] User QA trên browser: mở lại báo cáo, lọc tháng 8, xác nhận HĐ_TPSG_KV2_25_0056 (Bình) hiện DS 697.256.252

## Checkpoint — 2026-09-05
Vừa hoàn thành: Fix Hướng A — sửa 4 subquery quyết toán trong `CommissionSettlementQuarterReportService.php` (bỏ filter `date_accounting`), fix trực tiếp trên master theo yêu cầu user. Verify SQL trên erp_new PASS. Chưa commit git (theo quy tắc).
Đang làm dở: (không)
Bước tiếp theo: User QA trên browser.
Blocked: (không)
