# Plan: Port "Quyết toán thưởng năm" ERP → HRM

**Spec:** `.plans/quyet-toan-thuong-nam/design.md`
**Worktree:** `HRM/.worktrees/hrm-api-qtn` + `HRM/.worktrees/hrm-client-qtn`, nhánh `feature/quyet-toan-thuong-nam` (từ `origin/develop` @ 802d2694f / cc9d474a7).
**Khuôn HRM:** `finance/bill-payments` (luồng duyệt) + `finance/bill-adjust-depts` (generateCode lock, lịch sử) + `assign/settlement_contract` (mixin tính toán). Màn anh em: `.plans/qt-thuong-ns-quy-moi/`.

## Trạng thái
- Bắt đầu: 2026-11-04 · Tiến độ: T1-T4 + T5 + T6-BE(lịch sử) xong; còn T6-FE + Phase 5

### Checkpoint — 2026-11-04 (sau T1)
Vừa hoàn thành: **T1** — 4 entity + Calculator thuần + Service đọc DB + unit test.
- Files (worktree `hrm-api-qtn`): `Modules/Finance/Entities/BonusEndYearSettlement/{BonusEndYearSettlement,BonusEndYearSettlementDetail,BonusEndYearSettlementFile,SalesDepartmentPlan}.php`; `Modules/Finance/Services/BonusEndYearSettlement/{BonusEndYearSettlementCalculator,BonusEndYearSettlementService}.php`; `Modules/Finance/Tests/Unit/BonusEndYearSettlementCalculatorTest.php`.
- Verify: 13/13 phép tính thuần PASS (chạy standalone vì worktree không có vendor). Checkpoint DB (erp_hrm_check): dept 5/2025 registered=79,652,539,002 + actual=67,195,803,805 (SQL port) → DSTC bonus=604,762,234. TK doanh thu resolve đúng 511+con & 5211/5212/5213 (không gồm 521 cha), khớp danh sách ERP. Cột account_details (employee_department_id/account_id/money_value_exchange/type/invoiceable_date_accounting) đều có.
- Lưu ý: `company_bonus_end_year_configs` hiện CHƯA có dòng settlement_type=1 (DSTC) trên DB local → admin cấu hình sau; không ảnh hưởng 2 hàm doanh thu.
Bước tiếp theo: **T2** — CRUD + phạm vi (4 cấp) + chống trùng + FormRequest + Resource + Controller + routes + 5 quyền seeder + form-options.
Blocked: (không)

### Checkpoint — 2026-11-04 (sau T2)
Vừa hoàn thành: **T2** — Controller + Read/Write Service + Resource + FormRequest + routes `checkPermission` + 5 quyền seeder + form-options (đã dựng ở các lượt trước). Lượt này: viết + chạy feature test, đối chiếu ERP scope, sửa docblock `index()`.
- Files lượt này (worktree `hrm-api-qtn`): `Modules/Finance/Tests/Feature/BonusEndYearSettlementScopeTest.php` (MỚI, 9 test); `Modules/Finance/Http/Controllers/V1/BonusEndYearSettlementController.php` (sửa docblock `index()` — bỏ câu "ẩn phiếu Đang tạo của người khác" cho khớp ERP).
- Verify: 9/9 PASS (~76s, DatabaseTransactions trên `erp_hrm_check`, năm 2099 + mã `QTN-TEST-*`). Sau test DB sạch: n_2099=0, n_perms=0, n_testcodes=0.
- Phát hiện: ERP `BonusEndYearSettlement::searchByFilter` (model) chỉ gate 4 cấp quyền qua `created_company_id`/`created_department_id`/`created_by`, KHÔNG có mệnh đề status → KHÔNG ẩn phiếu nháp của người khác. Bản port `scopeVisibleTo` đã đúng 1:1 (giữ nguyên, không thêm status clause).
Bước tiếp theo: **T3 Duyệt** — processApprove (status 2→3 + approved_by/at + cập nhật approval_rate/total_approved từng phòng; reject→4; KHÔNG ghi sổ) + entity-history + feature test.
Blocked: (không)

### Checkpoint — 2026-11-04 (sau T3)
Vừa hoàn thành: **T3 Duyệt** — logic duyệt/không duyệt + feature test.
- Files lượt này (worktree `hrm-api-qtn`): `WriteService::approve()` (MỚI — transaction, khẳng định lại status==2 bằng ValidationException, status→3/4 + approved_by/at + updated_by, duyệt thì chốt approval_rate(mặc định 100)/total_approved(mặc định 0) từng dòng theo id+settlement_id); `Controller::approve()` (MỚI — findOrFail + `canApprove()` 403, đọc `is_approve` + `details`); route `POST /{id}/approve` `checkPermission:BGĐ duyệt quyết toán thưởng năm`; docblock class controller (bỏ câu "duyệt chưa có ở đây"); `Tests/Feature/BonusEndYearSettlementApproveTest.php` (MỚI, 5 test).
- Verify: 5/5 PASS (duyệt đổi status+ghi tỉ lệ; mặc định 100/0 khi thiếu số; không duyệt→4 không đụng dòng phòng; chặn duyệt khi ≠status2 = ValidationException; canApprove false khi thiếu quyền BGĐ). Scope test 9/9 vẫn PASS. DB sạch sau test: n_2099=0, n_testcode=0, n_perm_api=0.
- **ĐÍNH CHÍNH tách scope T3**: ERP `processApprove` KHÔNG ghi sổ và ERP cũng KHÔNG có lịch sử cho màn này. Phần **entity-history** là bổ sung bắt buộc của HRM nhưng phải làm **đủ 2 nơi** (popup danh sách + khối ở màn chi tiết) theo skill — mà FE (T5/T6) chưa dựng. Làm history BE-only lúc này là antipattern skill cảnh báo → **dời entity-history sang làm cùng FE (T6)**. T3 chỉ còn logic duyệt + test.

### Checkpoint — 2026-11-04 (sau T4)
Vừa hoàn thành: **T4 Xuất Excel danh sách** — endpoint `export-rows` trả JSON theo trang cho FE tự dựng file.
- Files lượt này (worktree `hrm-api-qtn`): `ReadService` thêm `EXPORT_NUMERIC_COLUMNS` + `exportColumns()` + `exportRows()` (dùng lại `searchByFilter`+`withSum`+`LIST_RELATIONS`+`BonusEndYearSettlementListResource`; COUNT chỉ trang đầu; STT chạy tiếp; cột tiền float/null, `year` chuỗi); `Controller::exportRows()` (page/limit≤5000/fields CSV); route `GET /export-rows` đặt TRƯỚC `/{id}`, KHÔNG gate quyền riêng; `Tests/Feature/BonusEndYearSettlementExportTest.php` (MỚI, 5 test).
- Verify: export 5/5 PASS; toàn suite QTN 19/19 PASS (scope 9 + approve 5 + export 5). DB sạch: n_2099=0, n_testcode=0.
- Bám khuôn finance list (`BillAdjustDeptService::exportRows`) chứ KHÔNG `ExportColumnRegistry` (cái đó dùng ở Assign/Meeting; các màn Finance list đều dùng `exportColumns()` `[key,label,width]`).
Bước tiếp theo: **T5** — Frontend danh sách + menu (`index.vue` + `finance.js`), nối nút Xuất Excel vào `utils/export/listExportFile.js` gọi `export-rows`.
- ⚠️ **Nợ phải sửa ở T5 (bug sẵn trong ListResource)**: `approved_by_name` LUÔN trả `null` vì `approved_by` vừa là cột int vừa là tên quan hệ → `$item->approved_by` trả về int, `optional(int)->info` = null. Sửa bằng `$item->getRelation('approved_by')` (hoặc đổi tên quan hệ, vd `approver`). T4 không dính vì export chỉ dùng `approved_at`. Khi làm cột/ô lọc "Người duyệt" ở T5 phải fix cùng.
Blocked: (không)

## Global constraints
- Ghi bảng ERP có sẵn trên DB gộp `erp_hrm_check`, **KHÔNG migration tạo bảng**. Model `extends Model` (không BaseModel) → service tự gán `created_by/updated_by = auth()->id()` mọi đường ghi.
- Màn **không ghi account_details** (không bút toán). `account_details`/`sales_department_plans` chỉ ĐỌC.
- Màn cấu hình quỹ thưởng **đã port** (regulation-config tab `thuongnam`) → chỉ đọc `CompanyBonusEndYearConfig`, không làm lại.
- 5 quyền mới type 8 qua `$this->perm([...])` (không `id`) trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, group `Quyết toán thưởng năm`.
- Nhãn "Người tạo"/"Ngày tạo". Số định dạng quốc tế `1,234,567.89` (`number_format`). Badge trạng thái do BE trả `status_text`+`status_color`. Status 1 "Đang tạo" = xám.
- FE màn mới chỉ dùng `V2Base*`, popup `V2BaseModal`, confirm `$confirm`, nút trong `V2Footer`, `unsavedChangesMixin`, 4 mixin danh sách + `ColumnCustomizationModal`, filter `floating`. Thao tác xong quay về danh sách.

## Phase 1 — Backend: Entity + nguồn số
- [x] **T1 Entity + Service tính toán** — 4 model (`BonusEndYearSettlement`, `...Detail`, `...File`, `SalesDepartmentPlan`) trong `Modules/Finance/Entities/...`. Port `BonusEndYearSettlementService`: getRegisteredRevenue (sales_department_plans status=3), getActualRevenue (account_details TK 511/521x + con, type2−type1), calculateBonusFundDSTC, calculateBonusFundProfit, calculateReserveFund (xác nhận nhánh value), calculateRemaining, calculateDepartmentDetail, getDepartmentsBySettlementType (đọc CompanyBonusEndYearConfig). **Hàm tính thuần tách riêng** để test. Test unit: DSTC ≥/< đăng ký, profit×rate, reserve trần maxRisk, remaining.

## Phase 2 — Backend: CRUD + quyền + duyệt
- [x] **T2 CRUD + phạm vi + chống trùng** — Service list/scope (3 cấp + own qua `scopeVisibleTo`, meta.is_all_company), show/canView, store/update (generateCode lock `{cty}.QTN.{year}.{5số}`, syncDetails BE tính lại cột auto, handleAttachments S3 `bonus_end_year_settlement`, checkDuplicateDepartments giao khoảng ngày status {1,2,3}), FormRequest, Resource (status_text/color, settlement_type_text, is_can_edit/delete/approve), Controller, routes `checkPermission`, 5 quyền seeder, form-options (công ty theo quyền, năm, loại). Feature test (9/9 PASS): scope 4 cấp, unique chống trùng (giao/không giao ngày), canView người tạo/người duyệt/ngoài phạm vi, store tự gán audit + giữ ô người dùng nhập.
  - ⚠️ **ĐÍNH CHÍNH đối chiếu ERP (05/11/2026):** ERP `searchByFilter` **KHÔNG lọc theo trạng thái** → người xem cấp công ty/phòng/tổng công ty VẪN thấy phiếu Đang tạo (status 1) của người khác. Giả định ban đầu "status 1 ẩn với người khác" là SAI; bản port giữ đúng ERP (không ẩn nháp), test khẳng định điều này. Đã sửa docblock `index()` cho khớp.
- [x] **T3 Duyệt** — processApprove: chỉ status 2; approve→3 + approved_by/at + cập nhật approval_rate/total_approved từng phòng; reject→4. **Không ghi sổ.** `WriteService::approve()` (transaction + rethrow ValidationException) + `Controller::approve()` (`canApprove()` 403) + route `POST /{id}/approve` gate quyền BGĐ. Feature test 5/5 PASS: duyệt đổi status + ghi tỉ lệ (và mặc định 100/0), không duyệt→4 không đụng dòng, chặn khi ≠status2, canApprove false khi thiếu quyền BGĐ.
  - ⚠️ **entity-history DỜI sang T6 (làm cùng FE):** skill bắt làm đủ 2 nơi (popup danh sách + khối màn chi tiết); FE chưa dựng nên làm BE-only lúc này là antipattern. ERP vốn không có lịch sử cho màn này.

## Phase 3 — Backend: Xuất Excel
- [x] **T4 Xuất Excel danh sách** — `GET bonus-end-year-settlements/export-rows` trả JSON theo trang (2.000/lượt, trần 5.000) cho FE tự dựng file (`utils/export/listExportFile.js`). Bám khuôn `BillAdjustDeptService::exportRows` (KHÔNG dùng `ExportColumnRegistry` — khuôn finance list dùng `exportColumns()` `[key,label,width]`). Cột: Mã · Công ty · Năm · Loại QT · Tổng quỹ thưởng · Quỹ còn lại · Tổng duyệt · Người tạo · Ngày tạo · Ngày duyệt · Trạng thái. 3 cột tiền là `EXPORT_NUMERIC_COLUMNS` trả float (ô số thật), `year` giữ chuỗi (không ngăn nghìn). Dùng lại `BonusEndYearSettlementListResource` + `withSum` của ReadService → không N+1. STT chạy tiếp qua trang; COUNT chỉ ở trang đầu. Không gate quyền riêng (cùng phạm vi `index`). Route đặt TRƯỚC `/{id}`.
  - Code: ReadService `exportColumns()`+`exportRows()`+`EXPORT_NUMERIC_COLUMNS`; Controller `exportRows()`; Routes api.php. Test: `BonusEndYearSettlementExportTest` 5/5 PASS (headings/widths, float vs string, fields rỗng→full, thứ tự tick, STT qua trang + count trang đầu). Toàn suite QTN 19/19 PASS.

### Checkpoint — 2026-11-05 (reconcile: phiên trước đã làm quá T4 mà KHÔNG ghi checkpoint)
Phiên làm việc trước đã dựng thêm (tất cả CHƯA commit, nằm trong worktree):
- **BE lịch sử (T6 phần BE) XONG**: `BonusEndYearSettlementHistoryService.php` + nối đủ vào WriteService (`logCreate` store:89, `logUpdate`+`logStatusChanged` update:132-133 & approve:201-202, `logDelete` delete:227) + cấu hình cột ở `app/Services/CatalogHistoryService.php` (bảng `bonus_end_year_settlements`, 2 khoá ảo `details_rows`/`attachment_rows`).
- **T5 FE danh sách XONG (chưa kiểm)**: `pages/finance/bonus-end-year-settlements/index.vue` (814 dòng) + link menu `components/subsystem-menu/finance.js`.
- Routes BE đã có đủ: index/show/store/update/destroy/approve/form-options/get-departments(calculate)/export-rows/export-columns/upload-files.
Baseline test XANH tại worktree (vendor có sẵn, chạy trực tiếp `vendor/bin/phpunit <path>` vì phpunit.xml chỉ gồm ./tests): Scope 9 + Approve 5 + Export 5 + Calculator 10 = **29/29 PASS**.
Ruling: dùng `.plans/.../plan.md` làm sổ (ledger) chính theo đúng lệ port HRM (màn anh em quý cũng vậy), KHÔNG tạo SDD ledger riêng — nếu sai chỉ tốn công đồng bộ 1 lần.
Ruling (T6, 2026-11-05): hợp đồng FILE đính kèm đổi sang **mảng URL chuỗi** để khớp component dùng chung `V2BaseAttachmentSection` (màn quý cũng dùng url-strings) — sửa 2 chỗ BE `BonusEndYearSettlementWriteService`: `uploadFiles()` trả về url phẳng (`$uploaded[] = $url;`), `syncFiles()` đối sánh theo `file_path` (không theo `id`). Lý do: contract cũ (id + object) sẽ khiến FE lưu `[object Object]` và khi SỬA (keepIds rỗng) xoá sạch file đang giữ trên S3 rồi tạo link chết. Schema DB (`file_name`+`file_path`) GIỮ NGUYÊN; FE buildPayload map `url => {file_name: basename(url), file_path: url}`. Cost nếu sai: phải khôi phục lối id-based + sửa lại component (nhưng component là dùng-chung nên hướng url-strings an toàn hơn). Đã chạy lại 29/29 BE test PASS sau sửa.
Còn lại thực tế: **T6 FE** (add/_id-index/_id-edit + form component + ApproveModal + hiển thị Lịch sử 2 nơi) → rồi **Phase 5 kiểm**.

## Phase 4 — Frontend
- [x] **T5 Danh sách + menu** — `index.vue` (814 dòng) + link menu `finance.js`. Do phiên trước dựng; cần kiểm Playwright ở Phase 5. Cột STT/Mã(link)/Công ty/Năm/Loại QT/Người tạo/Ngày tạo/Trạng thái/Tổng quỹ/Hành động; lọc Công ty(is_all_company)/Năm/Loại/Trạng thái/Người tạo/Người duyệt/Phòng ban/Ngày duyệt(range)/Quỹ(range); 4 mixin, floating, ColumnCustomizationModal, export FE.
- [x] **T6 Form tạo/sửa + chi tiết/duyệt** — `add.vue`/`_id/edit.vue`/`_id/index.vue` + `BonusEndYearSettlementForm.vue`: header (Công ty/Năm/Loại/Từ-Đến ngày/Ngày HT/Ghi chú/File), nút "Lập quyết toán" gọi calculate, **bảng chi tiết theo phòng cột đổi theo loại** (readonly cột auto, input cột tay), cột duyệt (Tỷ lệ %/Tổng được hưởng) khi canApprove||status3; `ApproveModal` (duyệt/không duyệt) bám `ApproveBillPaymentModal`; V2Footer (Lưu nháp/Lưu và gửi duyệt/Quay lại); unsavedChangesMixin. **+ entity-history (dời từ T3)**: ghi + hiển thị lịch sử tạo/sửa/duyệt/từ chối, làm **đủ 2 nơi** (popup ở T5 danh sách + khối Lịch sử ở `_id/index.vue`) theo skill `entity-history`; đổi trạng thái duyệt = dòng `change_status` riêng.

## Phase 5 — Kiểm (Bước 5, 5b, 6)
- [x] Đối chiếu ERP từng dòng bảng nghiệp vụ + ngang `bill-payments`/`settlement_contract`; checklist skill `erp-to-hrm-screen`; Playwright: tạo → lập QT (3 loại) → lưu/gửi duyệt → BGĐ duyệt chỉnh tỉ lệ → kiểm DB → sửa/xóa → xuất/lịch sử. Chụp ảnh đặt cạnh màn chuẩn. (Playwright 3 loại + bug preview: checkpoint T6; đối chiếu ERP 1:1 + review toàn nhánh: checkpoint Final Review dưới.)

## Checkpoint
- Sau T1: xác nhận số DSTC đăng ký + thực đạt khớp ERP trên 1 phòng thật (tinker so sánh).

### Checkpoint — 2026-11-05 (T6 XONG — kiểm Playwright 3 loại + fix bug preview)
Vừa hoàn thành: **T6 Form tạo/sửa + chi tiết/duyệt + entity-history** — FE do phiên trước dựng, phiên này KIỂM bằng Playwright MCP (127.0.0.1:3010) trọn vòng đời và sửa 1 bug thật phát hiện khi kiểm.
- **Kiểm Playwright trọn vòng đời (3 loại quyết toán):**
  - Loại 1 DSTC: phiên trước đã kiểm đủ (tạo → lập → lưu → duyệt → sửa → xóa).
  - Loại 2 Lợi nhuận phòng: phiên này kiểm đủ — lập (profit 100M → quỹ 8M@8% → dự phòng 800K → còn lại 7.2M); lưu nháp (TPE.QTN.2026.00002, id 160, status 1); danh sách hiện Sửa/Xóa/Lịch sử (không Duyệt); veto-parity bản đã duyệt (chỉ Lịch sử); popup Lịch sử danh sách hiện "Tạo mới"; màn Sửa load + recompute đúng (sau fix); sửa lưu DB (risk_debt 1M → còn lại 6.2M); xóa có confirm → mất khỏi DB + danh sách.
  - Loại 3 Lợi nhuận công ty: phiên này kiểm — `generate()` nạp đúng phòng 54 "PHÒNG LOGISTIC (LN)" rate 12%/dự phòng 5%/trần 20M; nhập lợi nhuận 50M qua đúng đường `BonusEndYearDepartmentTable.onInput` → recomputeRow: quỹ 6M = 50M×12%, dự phòng 300K = 6M×5%, còn lại 5.7M. Khớp công thức.
- **BUG THẬT phát hiện + sửa (TDD RED→GREEN):** màn Sửa loại lợi nhuận, gõ 1 ô là preview sập quỹ thưởng/dự phòng về 0 (còn lại âm) vì `BonusEndYearSettlementDetailResource::detailRow()` KHÔNG trả `bonus_rate`/`reserve_fund_percent`/`max_risk_reserve_fund` (3 cột này nằm ở `company_bonus_end_year_configs`, bảng chi tiết không lưu) → `recomputeRow` đọc rate=0. BE lưu lại vẫn đúng (`recomputeDetailForSave` đọc lại config) nên chỉ là lỗi preview, nhưng sai + dọa người dùng.
  - Fix: Resource nạp `configByDepartment()` (1 query/phiếu theo company_id+settlement_type, keyBy department_id) và gắn 3 cột vào mỗi dòng; `detailRow` nhận thêm tham số config. File: `Modules/Finance/Transformers/BonusEndYearSettlementResource/BonusEndYearSettlementDetailResource.php`.
  - Test MỚI: `Modules/Finance/Tests/Feature/BonusEndYearSettlementDetailResourceTest.php` (2 test, DatabaseTransactions trên `erp_hrm_check`, dept giả 990042/990099): dòng có config trả đúng 8/10/30M; dòng không config trả 0/0/0.
- **Verify cuối T6:** toàn suite QTN **31/31 PASS, 78 assertions** (Scope 9 + Approve 5 + Export 5 + DetailResource 2 + Calculator 10). tests: `vendor/bin/phpunit <5 file>` → 31/31.
- Ruling: port HRM giữ code CHƯA commit (lệ workspace) → ledger ghi file + kết quả test thay cho commit sha.
- Ruling (bug preview là khiếm khuyết tìm thấy khi kiểm, không phải task mới): sửa ngay trong T6 + phủ test, vì là defect của deliverable T5/T6 (Resource dùng chung cho cả màn xem lẫn sửa).
Task 6: complete (uncommitted per port convention, tests: vendor/bin/phpunit 5 QTN files → 31/31 pass 78 assertions)
Bước tiếp theo: **Phase 5** — đối chiếu ERP từng dòng + checklist `erp-to-hrm-screen` + review toàn nhánh (reviewer model mạnh nhất).
Blocked: (không)

### Checkpoint — 2026-11-05 (FINAL REVIEW — review toàn nhánh trên Opus, 1 fix Important)
Reviewer fresh-context (Opus) rà cả 2 worktree (`hrm-api-qtn` + `hrm-client-qtn`), đối chiếu ERP gốc 1:1, soi các input class test chưa chạm. Re-grade theo HẬU QUẢ, rồi xử lý:

**Important #2 (ĐÃ FIX, TDD RED→GREEN):** `getDepartments` (endpoint dựng khung phòng cho màn Lập) KHÔNG gate quyền, KHÔNG scope công ty → nhân viên bất kỳ (kể cả công ty khác / không quyền Tạo) truyền `company_id` tuỳ ý để đọc doanh thu đăng ký + thực đạt từng phòng của công ty khác. Vi phạm defense-in-depth (CLAUDE.md: endpoint dữ liệu nhạy cảm phải gate ở BE). ERP là 1-công-ty nên controller gate cả màn bằng 1 quyền; port HRM tách route riêng mà bỏ gate → vỡ giả định khi lên DB gộp đa công ty.
  - Fix: thêm `BonusEndYearSettlement::currentCanCreateForCompany(int $companyId)` (public static) = `currentCanCreate()` VÀ (`canViewAllCompany()` HOẶC `companyId === currentCompanyId()`); khớp đúng phạm vi `companiesForSelect()`. Controller `getDepartments` kiểm đầu hàm → 403 nếu fail. (`currentCompanyId()` là protected trong trait nên gói trong method public của entity thay vì gọi thẳng ở controller.)
  - File: `Modules/Finance/Entities/BonusEndYearSettlement/BonusEndYearSettlement.php` (+method), `Modules/Finance/Http/Controllers/V1/BonusEndYearSettlementController.php` (+gate đầu `getDepartments`).
  - Test MỚI: `BonusEndYearSettlementScopeTest` +3 (không quyền tạo→false cả công ty mình; chỉ quyền tạo→true công ty mình/false công ty khác; +xem tổng công ty→true mọi công ty). RED (3 error undefined method) → GREEN. Suite QTN sau fix: Scope 12 + Approve 5 + Export 5 + DetailResource 2 + Calculator 10 = **34/34 PASS, 83 assertions**.
Final: fixed getDepartments ungated cross-company revenue leak — test_can_create_for_company_* (×3) RED→GREEN, suite 34/34.

**Critical #1 (RULING — không fix, là việc tích hợp của user):** cả 2 nhánh trễ develop (api 37 commit / client 27) và 3 file DÙNG CHUNG feature này sửa (`Modules/Finance/Routes/api.php`, `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, `components/subsystem-menu/finance.js`) đều đã bị develop đổi (thêm HĐ bán đầu kỳ, Sổ công nợ NCC, QT thưởng NS quý mới, service-accounting). Nhánh này có **0 commit** (lệ port giữ working-tree) nên edit QTN nằm trên BẢN CŨ của 3 file → khi tích hợp, 3-way merge sẽ CONFLICT ở `finance.js` và nếu resolve nhầm về phía nhánh sẽ XOÁ MẤT 3 feature đã ship.
  - Ruling: KHÔNG tự rebase/merge — rơi đúng vào "four stops" của executing-plans (merge/rebase lên nhánh chung) VÀ lệnh thường trực "Không xử lý commit hay đẩy code lên git". Cost nếu bỏ qua: tích hợp cẩu thả làm mất route + quyền + menu của 3 feature đã ship. BẮT BUỘC báo user: trước khi gộp, cập nhật 2 worktree theo develop hiện tại rồi hợp nhất 3 file đó GIỮ cả entry mới của develop LẪN entry QTN. (`CatalogHistoryService` develop không đụng → không conflict.)

**Minor (deferred, không fix):**
- Final: minor (deferred): `remainingBonus` ép `(int)` ở Calculator:80 (ERP để nguyên) — FE `Math.trunc` khớp BE, chỉ cắt lẻ sub-đồng, là chủ ý (tiền = đồng nguyên).
- Final: minor (deferred): `Account::selfAndChildIds` gộp account qua mọi công ty (ERP dùng `->first()`); vô hại vì `AccountDetail` đã lọc `employee_department_id`, chỉ lệch nếu 2 công ty trùng `identify_number` cây con khác nhau.
- Final: minor (deferred): `getDepartments` ngày rỗng → `whereDate('>=', '')` khớp rỗng → `actual_revenue = 0` không báo lỗi; FE luôn gửi ngày nên chỉ là hành vi phòng thủ (gọi trực tiếp rỗng ra 0 thay vì 422).

**Reviewer xác nhận SẠCH:** nợ kỹ thuật `approved_by_name` null ĐÃ GIẢI QUYẾT (relation đổi tên `approver()`, cả List + Detail Resource populate đúng); parity công thức FE/BE khít; defense-in-depth lưu (`recomputeDetailForSave`); veto-parity danh sách↔chi tiết; route ghi gated; không N+1.

Review toàn nhánh: XONG. Mergeable sau khi user tự xử lý tích hợp #1 (bắt buộc). #2 đã fix. Minors để user quyết.
