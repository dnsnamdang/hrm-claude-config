# Báo cáo BHXH theo năm hiện đóng BH từ trước tháng bắt đầu đóng (#chưa có số Redmine) — @cuong61n

Nguồn: kế toán báo qua chat 28/11/2026 — `/human/report/insurance_report_year`: Trần Ngọc Sơn (12610998, PHÒNG LOGISTIC) đóng BHXH từ T6/2026 nhưng báo cáo hiện số tiền từ T4/2026 (tháng tiếp nhận, chưa tick "Có tham gia BHXH"). Bảng lương T4–T5 không trừ BHXH (đúng).
Nhánh: `gop_db` (worktree `HRM/worktrees/gop_db-api` + `gop_db-client`). Chưa commit/push (chờ user).

## Phase 1 — Điều tra (28/11/2026)

- [x] 28/11/2026 — Đối chiếu dữ liệu prod (DB `hrm_erp_gop`, employee_info_id 1554): LSL id 2599 từ 01/04/2026 `has_insurance = 0` nhưng `insurance_salary = 7.000.000` (BE vẫn tính lương BHXH từ các thành phần tick "Tham gia bảo hiểm"); LSL 2678 từ 01/06/2026 `has_insurance = 1`; LSL 3139 từ 01/12/2026 (gia hạn HĐ). DB local `local_hrm_erp` có y hệt → tái hiện được ở local (T4, T5 = 2.240.000).
- [x] 28/11/2026 — Lần code tới gốc: `SalaryService::insurance_report_year` lọc NV theo `has_insurance` của bản LSL **mới nhất**, rồi `EmployeeSalaryHistory::getEmployeeData()` lấy bản LSL hiệu lực từng tháng nhưng **không kiểm `has_insurance`** → nhân thẳng `insurance_salary` × tỷ lệ. Báo cáo BHXH **tháng** và tính lương (`CO_DONG_BAO_HIEM`) đều đọc cờ này nên chỉ báo cáo năm sai. DB local có 312 bản LSL `has_insurance = 0` mà `insurance_salary > 0` → ảnh hưởng rộng (40/613 NV đổi số ở local khi sửa).
- [x] 28/11/2026 — Phát hiện thêm khi đọc hàm: bộ lọc `company_id` / `department_id` / `keyword` **gán đè** danh sách id đã lọc theo quyền → quản lý phạm vi Phòng ban gõ từ khoá / chọn phòng khác là thấy NV ngoài phạm vi. Đã xác nhận bằng code cũ ở API :8000: tài khoản `duytn.kd2` (phạm vi Phòng ban, quản lý Ô tô 2) lọc `department_id=54` thấy 14 NV phòng Logistic.

## Phase 2 — Sửa (28/11/2026)

### BE (`hrm-api`, nhánh gop_db)
- [x] 28/11/2026 — `Modules/Payroll/Services/SalaryService.php::insurance_report_year` viết lại:
  - Mỗi tháng lấy bản LSL hiệu lực tại ngày đầu tháng (start_date ≤ ngày, end_date null hoặc ≥ ngày; trùng start_date lấy id lớn hơn — giữ đúng luật cũ), **chỉ tính tiền khi bản đó `has_insurance = 1`**; NV được đưa vào báo cáo khi có ≥ 1 tháng đóng BH trong khoảng (không còn nhìn bản mới nhất).
  - Bộ lọc công ty / phòng ban / từ khoá / loại phòng ban là điều kiện AND trên query đã giới hạn theo phạm vi quyền (vá lỗ hổng lọt dữ liệu).
  - Hiệu năng: 3 query (NV + toàn bộ LSL trong khoảng + cấu hình BH theo công ty) ghép trong bộ nhớ, thay cho `EmployeeInfo::find` + 2 query × NV × tháng (~13.500 query). Đo local 613 NV × 11 tháng: **~6,0s → ~0,55s**.
  - Trả thêm `totals` từng NV, `month_totals` + `total` từng phòng và toàn công ty để FE không cộng lại trong template; `from_date`/`to_date` chuẩn hoá về đầu tháng (trước đây 15/01→10/11 bị thiếu tháng cuối), `to < from` thì chỉ 1 tháng.
- [x] 28/11/2026 — `Modules/Payroll/Entities/EmployeeSalaryHistory::getEmployeeData()` (không còn nơi nào gọi, giữ lại) thêm điều kiện `has_insurance` cho đúng nghĩa.
- [x] 28/11/2026 — Export (`InsuranceReportYearExport` + blade) dùng chung service nên tự đúng theo; không sửa blade.

### FE (`hrm-client`, nhánh gop_db) — `pages/human/report/insurance_report_year.vue`
- [x] 28/11/2026 — Bảng đổi từ `b-table-simple/b-td` sang `<table>` thuần cùng class (`table b-table table-bordered` trong `.b-table-sticky-header`) → giữ nguyên hình thức + tiêu đề dính, nhưng 34.000 ô không còn là component Vue. Render sau khi API trả: **3,2s → 0,7s**. Dòng tổng dùng số BE trả sẵn.
- [x] 28/11/2026 — Hết 2 Vue warn cũ ("permissions already defined in data" → đổi tên `scopeFlags`; `index` không tồn tại ở key dòng tổng công ty). Bỏ dòng "Số trang: 1" (màn không phân trang). Thêm dòng "Không có nhân viên tham gia bảo hiểm trong khoảng thời gian đã chọn" màu xám `#6b7280` khi rỗng. Placeholder ô tìm → "Tìm theo mã, tên nhân viên" (BE lọc code + fullname). `getData` vẫn bọc `$nextTick` (lúc `mounted` `$nuxt.$loading` chưa sẵn).
- [x] 28/11/2026 — Xuất Excel truyền đủ bộ lọc đang xem (trước thiếu từ khoá + loại phòng ban → file khác màn hình).

## Phase 3 — Kiểm thử (28/11/2026)

- [x] So JSON trước/sau toàn công ty (613 NV): 40 NV đổi số, đều là tháng có bản LSL `has_insurance = 0` (đối chiếu DB 4 ca: Vũ Viết Kiên, Võ Thế Đức, Trần Huy Hoàng, Nguyễn Văn Thế Anh); 1 NV bị loại (Nguyễn Thị Hải — LSL đóng BH đã hết hạn 12/2024, trước hiện 1 dòng toàn 0), 1 NV thêm (Bùi Hải Ninh — LSL 01/2024 tick BH, lương BHXH 0). Tổng tháng/tổng phòng/tổng công ty BE = cộng từng NV.
- [x] API ca biên: đảo ngày, giữa tháng, 1 tháng, 23 tháng (0,66s), từ khoá không khớp, lọc phòng / công ty / loại phòng ban 0 và 1 và rỗng.
- [x] Quyền (tài khoản local, mật khẩu Test@123 đặt cho employees 25 và 35): `duytn.kd2` phạm vi Phòng ban chỉ thấy 2 phòng mình quản lý; lọc từ khoá / phòng 54 / công ty 4 → rỗng (code cũ lọt). `cannt.kd1` không quyền → chỉ thấy chính mình.
- [x] E2E Playwright **10/10 pass** (`e2e/tests/insurance-report-year/insurance-report-year.spec.ts`, chạy bằng `e2e/playwright.gopdb.config.ts` lên bản worktree :3002/:8003 để không đụng `.auth/user.json` của bản :3000): API số liệu NV mẫu + tổng; UI 4 dòng/NV, T04–T05 trống, T06+ 2.240.000, không Vue warn, tiêu đề sticky, số căn phải, render < 2,5s; lọc theo mã; đổi Từ/Đến tháng = 06/2026 → 1 cột; từ khoá không khớp → dòng trống xám; Xuất excel tải `.xls` đúng tham số; 2 test phạm vi quyền.
- [x] Ảnh trước/sau: scratchpad phiên (`before-year-report.png`, `after-year-report.png`) — giao diện giữ nguyên, chỉ mất "Số trang: 1".

## Phase 4 — Dựng lại UI theo khuôn `report-styles` + cột Mã NV + rà Excel (28/11/2026, user yêu cầu "để hết ra 1 màn hơi giật, sửa lại UI cho đẹp")

Chốt với user 28/11/2026: cây Phòng ban ▸ Nhân viên (dòng NV = Tổng cộng, bấm mũi tên bung 3 dòng NLĐ / NSDLĐ / Lương BH) · khối tổng hợp giữ logic cũ · thêm cột Mã NV · **KHÔNG làm In** (báo cáo lẫn popup — ngoại lệ văn bản của skill mục 4c) · đủ popup drill + Excel.

### BE (`hrm-api`, nhánh gop_db)
- [x] 28/11 — `Modules/Payroll/Services/Report/InsuranceReportYearService.php` (mới): `compute()` (3 query, cache theo request) → `index()` phân trang theo PHÒNG (20/trang, `per_page` trần 500), `summary` toàn tập (NV, phòng, 4 tổng tiền, tổng theo tháng + số NV đóng từng tháng), `itemList()` / `popupRows()` (phạm vi `drill_department_id`, ô tìm `q` mã/tên/phòng, `sort`/`dir` 8 cột, phân trang server), `describeFilters()`, `drillTitle()`; helper Excel `excelNumber/excelFormat/isNumericCode/roman`. Logic tiền giữ y bản sửa sáng (chỉ tháng có tick BHXH).
- [x] 28/11 — Controller mới `InsuranceReportYearController` (index · item-list · export · item-list/export); route cũ `/insurance_report_year` + `/export` trỏ sang controller mới, thêm 2 route item-list. Gỡ `SalaryService::insurance_report_year` + 2 action cũ trong `SalaryController` (không còn nơi gọi; `insurance_report_month` giữ nguyên).
- [x] 28/11 — Excel báo cáo `app/ExcelExport/InsuranceReportYearExport.php` viết lại bằng **FromArray + style theo vùng** (FromView với 40.000 ô style inline mất 18s → **1,2s**), có letterhead, freeze pane, 4 dòng/NV như khuôn kế toán; cột **Mã nhân viên** mới; **mã toàn chữ số là ô SỐ** (numFmt `0`, ≤ 15 chữ số, không 0 đầu) để kế toán VLOOKUP với bảng mã dạng số; tiền là số thật `#,##0`. Blade cũ `exports/insurance_report_year.blade.php` xoá. Excel danh sách popup `InsuranceReportYearListExport` + blade `insurance_report_year_list` (FromView, nhỏ) cùng quy tắc mã/tiền.
- [x] 28/11 — Đã kiểm file bằng PhpSpreadsheet đọc lại: ô mã `n` (số) numFmt `0`, ô tiền `n` numFmt `#,##0`, mã có chữ (NV.00484) / 0 đầu giữ chuỗi; vị trí dòng đúng cả khi có / không logo (Maatwebsite nối mảng sau dòng logo → quy theo `getHighestRow()`).

### FE (`hrm-client`, nhánh gop_db)
- [x] 28/11 — `pages/human/report/insurance_report_year.vue` viết lại theo khuôn: `V2BaseSmartFilterPanel floating` (ô tìm nhanh mã/tên chờ Enter; Công ty – Phòng ban qua `V2BaseCompanyDepartmentFilter` có 🔒; Từ tháng / Đến tháng `V2BaseDatePicker type=month`; Loại phòng ban) — ô chọn đổi là lọc luôn (deep-watch gom 300ms), `#header-actions` chỉ **Xuất Excel**; `reportSeq`, giữ báo cáo cũ khi lỗi, làm mờ khi tải lại; Excel tải bằng link `?token=`.
- [x] 28/11 — Component mới `pages/human/report/insurance-report-year/` : `components/InsuranceSummary.vue` (khối `.rsum` 2 khối, số NV bấm được), `components/InsuranceTable.vue` (bảng cây `rsum-tb` 3 cấp, cột STT · Mã NV · Phòng ban/Nhân viên (ô chọn cấp 1/2/3) · Số NV (bấm) · tháng · Tổng cộng; `V2BaseTableScroll` 2 thanh cuộn, min-width theo số tháng, phân trang theo phòng), `components/InsuranceDrillModal.vue` (V2BaseReportModal, phân trang server, tìm, sắp xếp, footer Xuất Excel danh sách + Đóng), `DrillNum.vue` copy khuôn, `api.js`, `format.js`.
- [x] 28/11 — Playwright MCP soát mắt 1920px: bộ lọc 4 ô/hàng, khối tổng hợp, cây, bung 3 dòng chi tiết, popup; 0 lỗi console.

### Kiểm thử
- [x] 28/11 — E2E **14/14 pass** (`e2e/tests/insurance-report-year/insurance-report-year.spec.ts`, config `playwright.gopdb.config.ts`): API (NV mẫu T4–T5 = 0, summary = cộng mọi trang 67 phòng, 32% lương BH trừ cty chưa cấu hình, ca biên ngày, item-list lọc/sắp/phân trang/tổng) · UI (bộ lọc + khối tổng hợp + dòng TỔNG + 20 phòng/trang + cột Mã NV + không console error; số tổng hợp = TỔNG = API; bung/thu mũi tên, 3 dòng chi tiết NLĐ+NSDLĐ = Tổng, ô chọn cấp 1/2/3, ô chọn cấp 26px cùng hàng nhãn; ô tìm gõ không gọi API / Enter lọc / × xoá tải lại; đổi Đến tháng / Từ tháng → số cột, chọn Loại phòng ban tự tải, Xóa lọc về mặc định; popup toàn bộ / theo phòng, tìm, sắp xếp server, Xuất Excel danh sách tải `.xlsx`, không nút In; Xuất Excel báo cáo link có token < 8s; 1366px mọi tiêu đề 1 dòng, th dính, ≥ 2 thanh cuộn ngang) · quyền (quản lý Phòng ban chỉ thấy phòng mình, lọc vượt phạm vi rỗng kể cả item-list; không quyền chỉ thấy mình).

### Chưa làm / cần user quyết
- **Xuất Excel dựng ở FE (ảnh kế toán gửi: mã NV căn trái, phải Enter mới VLOOKUP được)** — ảnh đó KHÔNG phải màn này: export BE kiểu `FromView` đã tự ra ô số với mã toàn chữ số (đã thử nghiệm); ô chữ căn trái là file dựng ở FE bằng ExcelJS (`utils/export/listExportFile.js` — 97 màn dùng, + `dom-table-to-excel.js`…) ghi chuỗi nguyên văn. Sửa "tất cả" = đổi util dùng chung (chuỗi toàn chữ số, không 0 đầu, ≤ 15 ký tự → số) — cần user duyệt vì ảnh hưởng 97 màn (số serial / số tài khoản sẽ thành số).

## Ghi nhận dữ liệu (không sửa code, báo kế toán nếu cần)
- CN Hải Phòng (company 2) **chưa có cấu hình tỷ lệ BH** (`insurance_configs`) → 16 NV có lương BHXH nhưng tiền = 0 (hành vi cũ giữ nguyên).
- 3 NV tick BHXH nhưng lương BHXH = 0 từ 01/2026 (12310448 Bùi Hải Ninh, 102511210 Đỗ Tất Thành, 102011167 Nguyễn Đình Kiên — 2 người sau cty 10) → hiện dòng toàn 0.
- NV có HĐ đóng BH hết hạn (vd Võ Thế Đức, Nguyễn Văn Thế Anh tới 30/09/2026) rơi về bản LSL cũ không tick → T10–T11 = 0 theo đúng dữ liệu.
- Export vẫn là `FromView` → ~6s cho 613 NV (PhpSpreadsheet dựng 2.520 dòng), chưa tối ưu trong lần này.

## Phase 5 — Đẩy prod (28/11/2026, user bảo "đẩy lên prod")
- [x] 28/11 — Commit + push `gop_db`: api `65ab12ae6`, client `8db056ee5` (merge thêm 2 commit origin của người khác: my-todo calendarSummary, chat-call toàn màn hình).
- [x] 28/11 ~15:00 — `~/build_tpe.sh` trên hrm-prod exit 0: api prod `65ab12ae6`, client prod `8db056ee5` (route:cache xong; FE build + tráo `.nuxt`, pm2 `hrm-client-tpe` online; cảnh báo build chỉ là postcss `end value` của các màn timesheet cũ). Kiểm: 3 route mới trên https://hrm.eteksofts.com trả 401 khi chưa đăng nhập (route tồn tại), chunk JS chứa popup mới đã có trong `.nuxt/dist/client`, site 200. Chưa đăng nhập prod bằng tài khoản thật để soi số liệu — user tự mở màn kiểm với kế toán.

## Phase 6 — Kế toán báo thiếu NV đã nghỉ việc (28/11/2026 chiều)
- [x] 28/11 — Điều tra prod: Nguyễn Văn Thái 11510114 `status = 0`, `leave_date` NULL → rớt ngay điều kiện `status = active OR leave_date > from`. Có QĐ chấm dứt HĐLĐ #44 đã duyệt (status 5) `termination_date_start = 2026-05-14` nhưng luồng duyệt không ghi `leave_date` (bug Decision đã biết — có sẵn `BackfillLeaveDateFromTerminationSeeder`, chưa chạy trên prod). Dry-run seeder trên prod: **34 NV** thiếu leave_date có QĐ; trong đó 19 NV TPE còn LSL đóng BH 2026 (toàn bộ số bị sót đều thuộc nhóm có QĐ). Prod còn 136 NV status 0 không leave_date và không QĐ nào — không có LSL đóng BH hiệu lực 2026 nên không ảnh hưởng báo cáo.
- [x] 28/11 — Sửa code `InsuranceReportYearService::employeesQuery`: `leftJoinSub` QĐ chấm dứt đã duyệt cuối cùng, `COALESCE(leave_date, termination_date_start)` dùng cho cả điều kiện lấy NV lẫn điểm cắt tháng sau khi nghỉ (commit api `52b14a5f7`, CHƯA push). Local: 613 → 630 NV (+17, không mất ai), tổng +180.668.480; Thái T1–T5 = 3.504.000 (10,95tr × 32%), T6+ = 0.
- [x] 28/11 — Kiểm: tính độc lập Python từ DB (có fallback QĐ) = API 630/630 NV, 0 lệch tháng, tổng bằng nhau; 0 NV nghỉ còn tiền ở tháng sau ngày nghỉ. E2E thêm ca Thái → **15/15 pass**.
- [ ] Chờ user: (1) push + deploy fix lên prod; (2) chạy thật `BackfillLeaveDateFromTerminationSeeder` trên prod (ghi `leave_date` 34 NV — dữ liệu hồ sơ, ảnh hưởng mọi báo cáo khác đang lọc theo leave_date, vd báo cáo BHXH tháng); (3) mở ticket Decision: duyệt QĐ chấm dứt không ghi `leave_date` ở một số luồng.

### Checkpoint — 28/11/2026 16:10
Vừa hoàn thành: Phase 4 — UI khuôn report-styles + cột Mã NV + Excel FromArray 1,2s + e2e 14/14.
Đang làm dở: —
Bước tiếp theo: user quyết 3 việc ở Phase 6; rồi mở màn trên prod cùng kế toán đối chiếu Trần Ngọc Sơn (T4–T5 = 0) + xuất Excel thử VLOOKUP cột Mã NV; user quyết việc sửa util Excel FE dùng chung (97 màn); báo kế toán 3 ghi nhận dữ liệu; có số Redmine thì đổi tên thư mục.
Blocked: chưa có số Redmine (đổi tên thư mục khi có).
