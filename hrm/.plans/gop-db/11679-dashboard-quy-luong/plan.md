# #11679 Dashboard Thông tin NS — box Quỹ lương dự kiến — @manhcuong

- [x] BE: `DashboadService::human()` box "Quỹ lương dự kiến (chưa bao gồm thưởng năng suất)" = cột "Lương BHXH" dòng công ty của Bảng nhân sự và quỹ lương; chọn bản lương y hệt báo cáo (NV status=1, start_date mới nhất <= hôm nay, KHÔNG xét end_date, has_insurance=1) qua `sumInsuranceSalaryLikeSalaryReport()` — không dùng `Helper::getEmployeeSalaryHistoryIds` vì nó bỏ bản quá end_date nên lệch báo cáo
- [x] Test Playwright local (:3002/:8003, DB local_hrm_erp) 20/10/2026: 6/6 công ty box = báo cáo (TPE 3,327,459,000); đã đẩy gop_db commit 34305ef8f
