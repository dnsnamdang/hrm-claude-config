# Bảng cân đối phát sinh công nợ nhân viên — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port màn ERP `account-detail.balance-debt-employee` sang HRM + In + Excel, drill-down sang Sổ chi tiết công nợ nhân viên.

**Architecture:** Tách phần chung với `EmployeeDebtDetailService` (quyền, phạm vi, ô lọc NV / TK / tiền tệ / số tiền, ngày, letterhead, validate) ra trait dùng chung; service mới `EmployeeDebtBalanceService` gom `account_details` theo NV × loại tiền bằng SQL (subquery tổng → lọc Chỉ tiêu → join NV → sắp xếp + phân trang SQL), dòng tổng theo loại tiền bằng 1 câu GROUP BY. FE theo khuôn màn Sổ chi tiết.

**Tech Stack:** Laravel (hrm-api Modules/Finance), Nuxt 2 / Vue 2 (hrm-client), PHPUnit trên DB gộp (DatabaseTransactions).

**Spec:** `hrm-claude-config/hrm/docs/superpowers/specs/gop-db/2026-11-03-bang-can-doi-cong-no-nhan-vien-design.md`

## Global Constraints

- Quyền tên y ERP: "Xem bảng cân đối phát sinh công nợ nhân viên của tổng công ty" / "… của công ty"; cuối seeder, `type` 8, group "Bảng cân đối phát sinh công nợ nhân viên", không id; `permission:sync`.
- 403 mọi endpoint khi không quyền; phạm vi công ty = `employee_company_id` mình OR `employee_id` mình (y Sổ chi tiết).
- Chỉ bút toán có `employee_id`; TK + con trực tiếp; Đến ngày `<= 23:59:59`; đầu kỳ = trước Từ ngày, mọi loại tiền.
- Phân trang 10; số chuẩn quốc tế; ô 0 để trống; không `sed -i`; đóng browser; commit khi user bảo.
- Nhánh `feat/bang-can-doi-cong-no-nv` rẽ từ `feat/so-chi-tiet-cong-no-nv` (2 repo, gỡ upstream).

## Review Focus

1. Dòng ngoại tệ: đầu kỳ + phát sinh = cuối kỳ cả nguyên tệ lẫn VNĐ (Task 2 `test_balance_formula_all_currencies`).
2. Cuối kỳ VNĐ của 1 dòng = cuối kỳ Sổ chi tiết cùng bộ lọc + `employee_id` + `currency_id` (Task 2 `test_matches_detail_closing`).
3. Chỉ tiêu + Số tiền lọc trên số đã gom, phân trang / tổng đúng sau lọc (Task 2 `test_filter_money_by`).
4. Kỳ dài TK lớn không lỗi / không lấy hết dòng về PHP (Task 3 `test_large_period`).
5. Refactor không đổi hành vi Sổ chi tiết (Task 1: chạy lại 15 test cũ).

---

### Task 1: Tách phần dùng chung (không đổi hành vi Sổ chi tiết)

**Files:** Create `hrm-api/Modules/Finance/Services/EmployeeDebt/Concerns/EmployeeDebtCommon.php`, `hrm-api/Modules/Finance/Http/Controllers/V1/Concerns/ValidatesEmployeeDebtFilters.php`; Modify `EmployeeDebtDetailService.php`, `EmployeeDebtDetailController.php`.

**Produces (trait `EmployeeDebtCommon`):** `abstract protected function permissions(): array` (`[PERM_ALL, PERM_COMPANY]`) · `scopeFlags(): array` · `canView(): bool` · `accountIds(int): array` · `static date($v): ?Carbon` · `static text(Request, string): string` · `applyScope(Builder): void` · `applyCommonFilters(Builder, Request): void` (employee/company/department/part/currency/account/money_from/money_to) · `accountOptions(): array` · `currencyOptions(): array` · `letterhead(): string` · `printInfo(Request): string` (Công ty · Phòng ban · Tài khoản · Mẫu · Từ ngày · Đến ngày) · `printFooter(): string` · `static isForeign(Request): bool`.
**Produces (controller trait):** `validateFilters(Request): void` (3 ô bắt buộc + Đến ≥ Từ, câu y Sổ chi tiết).

- [ ] Chuyển code, Sổ chi tiết `use` trait; chạy `EmployeeDebtDetailServiceTest` + `EmployeeDebtDetailApiTest` → 15/15 PASS (không sửa test).

### Task 2: Service bảng cân đối + quyền

**Files:** Create `Modules/Finance/Services/EmployeeDebt/EmployeeDebtBalanceService.php`; Modify seeder; Test `Modules/Finance/Tests/Feature/EmployeeDebtBalanceServiceTest.php` (fixture dùng lại `EmployeeDebtDetailTestCase`).

**Produces:** `PERM_ALL`, `PERM_COMPANY`; `const FILTER_MONEY_BY` (1..6 → nhãn spec 4.2); `aggregateQuery(Request): Builder` (1 dòng NV × loại tiền: `employee_id, currency_id, debt_begin, has_begin, debt_in, has_in` + bản `_exchange`, đã lọc Chỉ tiêu); `rows(Request, int $offset = 0, ?int $limit = null): Collection` (thêm `employee_code`, `employee_name`, `currency_name`, `begin`, `end`, `begin_exchange`, `end_exchange` ròng; xếp `employee_code`, `currency_id`); `count(Request): int`; `totals(Request): array` (mỗi loại tiền: các Σ + ròng); `search(Request): array` (`data`, `totals` — bỏ khi `with_summary=0`, `meta`).

- [ ] Test: `test_balance_formula_all_currencies` (USD: đầu kỳ Nợ 2 / Có 1 + trong kỳ Nợ 3 ⇒ begin 1, end 4; VNĐ tương ứng) · `test_groups_by_employee_and_currency` · `test_scope_company_or_self` · `test_filter_money_by` (6 chỉ tiêu, có Số tiền) · `test_money_filter_per_entry_before_grouping` · `test_matches_detail_closing` (so `EmployeeDebtDetailService::summary` cùng request + employee_id + currency_id) · `test_totals_per_currency`. Chạy FAIL → seeder 2 quyền + sync → viết service → PASS.

### Task 3: Controller + route + In + Excel BE

**Files:** Create `Http/Controllers/V1/EmployeeDebtBalanceController.php`; Modify `Routes/api.php` (`/employee-debt-balances`: `/`, `/meta`, `/export-rows`, `/print-list-data`); service thêm `meta`, `exportRows(Request, int $page)` (trang 2.000, dòng tổng đầu trang 1), `printHtml(Request, int $max)` (đếm trước). Test `EmployeeDebtBalanceApiTest.php`: 403 ×4, validate, phân trang 10 + `with_summary=0`, Excel cột theo Mẫu + dòng tổng, In có tiêu đề / letterhead `<img>`, `test_large_period` (cùng cỡ ca Sổ chi tiết).

### Task 4: FE màn + menu + drill-down

**Files:** Create `hrm-client/pages/finance/employee-debt-balances/index.vue` (+ `components/constants.js`); Modify `components/subsystem-menu/finance.js` (link mục có sẵn). Khuôn `pages/finance/employee-debt-details/index.vue`: bộ lọc spec 4.3, bảng tiêu đề 2 tầng (Nguyên tệ khi Mẫu 2, VNĐ), dòng tổng mỗi loại tiền, phân trang 10 (`with_summary=0` khi chuyển trang), In / Excel, link Mã NV → `/finance/employee-debt-details?reload=1&…&employee_id&currency_id` (tab mới, số tiền thuần). Playwright: số khớp tinker, drill-down khớp cuối kỳ, mẫu Ngoại tệ, Chỉ tiêu, In, Excel; xem ảnh; đóng browser.

### Task 5: Hoàn tất

- [ ] Chạy lại 4 file test (Detail ×2, Balance ×2); review toàn nhánh (reviewer mới); sửa Critical/Important theo TDD; STATUS + memory.

## Ngày 03/11/2026 (@junfoke)
- [x] 03/11/2026 — Làm chuyển đổi erp->hrm: Bảng cân đối phát sinh công nợ nhân viên - 100%. Khảo sát ERP (ERP không có In/Excel, API search không chặn quyền), viết spec, user duyệt: phạm vi công ty như Sổ chi tiết, đầu kỳ mọi loại tiền, làm thêm In + Excel.
- [x] 03/11/2026 — Code nhánh `feat/bang-can-doi-cong-no-nv` (rẽ từ Sổ chi tiết): mỗi dòng NV × loại tiền, mẫu VNĐ/Ngoại tệ, dòng Tổng mỗi loại tiền, bấm mã NV mở Sổ chi tiết đúng bộ lọc; không quyền → 403 cả API; tách phần chung 2 màn ra trait `EmployeeDebtCommon`. Seeder +2 quyền. 16 test (+15 test Sổ chi tiết vẫn qua).
- [x] 03/11/2026 — Review sửa: (I1) link mã NV lấy bộ lọc đã áp, không lấy ô vừa gõ; (I2) không có quyền Sổ chi tiết thì mã NV hiện chữ thường; ô Số tiền = 0 bỏ qua như ERP (cả 2 màn); NV thiếu hồ sơ không bị đẩy lên đầu; dọn tiêu đề thừa. Tốc độ TK 35241 6 tháng 4,6s → 1,6s.
- [x] 03/11/2026 — Bấm thử local: TK 141 01/01–31/10 khớp 3 số tổng màn Sổ chi tiết; drill-down NV 11510110 ra đúng; mẫu Ngoại tệ USD/EURO; In + Excel (175 dòng).
- [x] 03/11/2026 — Theo user: sửa lỗi Làm mới gọi API 2 lần (cả 2 màn), Playwright đếm mỗi thao tác 1 lần gọi.
- [x] 03/11/2026 — Commit api `9b12040ae`, client `f2831eb45`; merge develop + push (api `66ce147dd`, client `66a3d7d47`). Xung đột form Chuyến xe khác (với `ee75050e6`): giữ nhãn/placeholder bản QA + kiểu ô số đồng nhất. Gửi user link dev HRM/ERP 4 màn công nợ. Dev cần `permission:sync` + build client.
- [ ] Màn 4/4 Sổ chi tiết công nợ phải trả NCC — chờ user bảo làm.


## Ngày 06/11/2026 (@junfoke)
- [x] 06/11/2026 — Xuất testcase màn Bảng cân đối phát sinh công nợ nhân viên theo khuôn chuẩn mới: 106 TC, P0 45%. Kiểm số theo luồng phát sinh (TK tạm ứng 1411, kỳ T10: NV-A đầu kỳ Nợ 6,500,000 → cuối kỳ Nợ 9,200,000, đổi sang T11 thì cuối kỳ T10 thành đầu kỳ; ca NV dư Có, ngoại tệ, bút toán đảo), đối chiếu 2 hệ thống, số dư từng NV phải khớp màn Sổ chi tiết công nợ NV. File `testcase/testcase - Bang can doi phat sinh cong no nhan vien.xlsx`, script `testcase/gen_testcase_bang-can-doi-cong-no-nv.py`.

## Ngày 07/11/2026 (@junfoke)
- [x] 07/11/2026 — Fix phản hồi #12063: bản in Bảng cân đối đổi 2 dòng Từ ngày/Đến ngày thành 1 dòng "Thời gian: Từ … đến …" (phần in dùng chung với Sổ chi tiết công nợ NV). Api `18e72f6b9`.
- [x] 07/11/2026 — Fix phản hồi #12068: (1) dòng Tổng — chữ "Tổng" căn giữa ô gộp 3 cột (STT, Mã NV, Tên NV) cả màn hình lẫn bản in (trước nằm lẻ ở cột Tên NV, căn trái); (2) bản in — khối ký tên "Người lập / Kế toán trưởng" không còn bị đóng khung (đổi bảng → `div`, áp cả 3 bản in công nợ; test bằng CSS kẻ khung mọi ô như popup thật); (3) bộ lọc — gộp "Số tiền từ" + "Số tiền đến" thành 1 ô "Số tiền … → …" như Sổ chi tiết công nợ NV. Sửa `AccountDebtCommon.php`, `EmployeeDebtBalanceService.php`, client `employee-debt-balances/index.vue`. Commit "fix 12068" api `ebaa18a76` (merge `5a4e897a0`), client `72ff17b3a` — đã lên `origin/develop`.
- [ ] 07/11/2026 — Đang làm #12069: thứ tự dòng đã kiểm khớp ảnh ERP (chạy `rows()` bằng user 13); ô Nhân viên không tìm ra NV đã nghỉ "Trần Văn Chung" (10710037) → user đồng ý sửa component dùng chung `V2BaseCompanyDepartmentFilter` (thêm prop bật công tắc NV đã nghỉ, dùng cơ chế `toggleLocked`/`showLockedToggle` có sẵn), bật prop ở 2 màn công nợ NV. Chưa commit (client worktree `gop-db`: `V2BaseCompanyDepartmentFilter.vue`, `employee-debt-balances/index.vue`, `employee-debt-details/index.vue`; api `EmployeeDebtBalanceService.php`).

## Ngày 09/11/2026 (@junfoke)
- [x] 09/11/2026 — Fix phản hồi #12069: Bảng cân đối phát sinh công nợ NV xếp dòng như ERP (NV có bút toán sớm nhất đứng trước, thay vì theo mã NV); ô Nhân viên của component dùng chung `V2BaseCompanyDepartmentFilter` có nút ổ khoá "hiện NV đã nghỉ" (mặc định tắt ở mọi màn), prop `include-locked-employees` bật sẵn cho 2 màn công nợ NV — gõ "Chung" ra "🔒 HN_KHO_LN - Trần Văn Chung". Đã kiểm ảnh cả màn khác (Phát triển khách hàng: ổ khoá tắt). Commit develop api `fccff5a19`, client `e82f96858`.

## Ngày 10/11/2026 (@junfoke)
- [x] 10/11/2026 — Merge nhánh `feat/cong-no-khach-hang` vào develop: tách phần chung `AccountBalanceService`, màn NV kiểm quyền theo mã `accounting.bang_can_doi_phat_sinh_cong_no_nhan_vien.view`; số liệu, bản in, thứ tự dòng giữ nguyên (giữ cả #12069 #12068 #12063 khi giải xung đột). Api `df407199e`, client `39c427075`.
