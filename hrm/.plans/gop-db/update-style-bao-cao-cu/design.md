# Update style các báo cáo cũ — tổng quan

**Nhánh:** `gop_db` (code ở nhánh checkout ra từ `gop_db`) · **Phụ trách:** @namdangit · Mở: 04/10/2026
**Khuôn:** skill `HRM/.claude/skills/report-styles` (mẫu = Báo cáo tổng hợp CSKH tiềm năng, `template/` commit `ae11073e9`)

## Mục tiêu

Chuyển lần lượt các báo cáo cũ của hrm-client sang 1 khuôn chung: bộ lọc nổi có In/Excel trên đầu → khối tổng hợp
`.rsum` → bảng cây `rsum-tb` (dòng TỔNG, ô chọn cấp bung, tiêu đề dính, cuộn ngang 2 thanh) → popup
`V2BaseReportModal`. Mỗi báo cáo là 1 folder con (mockup → design → plan → hỏi "làm" → code), chỉ tạo khi bắt đầu.

## Quy trình mỗi báo cáo (theo skill report-styles mục 5)

1. Liệt kê hiện trạng (bộ lọc, biểu đồ, cột, popup, In/Excel, cách BE phân trang).
2. Hỏi user các điểm NGHIỆP VỤ, lần lượt từng câu; điểm thuần UI thì tự chốt theo khuôn và ghi vào đầu mockup.
3. Mockup từ DOM + CSS thật → user duyệt.
4. design.md + plan.md → hỏi "làm" (repo · nhánh · file · có đụng BE/DB không) → code → kiểm Playwright.

## Theo dõi

| # | Báo cáo | Route | Folder | Trạng thái |
|---|---|---|---|---|
| 1 | Thời gian meeting theo dự án | `/assign/report/meeting-by-projects` | `meeting-by-projects/` | ĐÃ MERGE gop_db 05/10 (api 8de764f79, client 2f04d1dfb) |
| 2 | Thời gian meeting theo nhân viên | `/assign/report/meeting-by-employees` | `meeting-by-employees/` | ĐÃ MERGE gop_db 05/10 (api 9696baa26, client 6c0b509de) + bổ sung lọc trạng thái / popup loại / popup NV tham gia (api 60aa9bfa0, client 81b715269); e2e chưa chạy |
