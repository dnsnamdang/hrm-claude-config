# Plan — Khai hợp đồng đầu kỳ: validate trùng mã theo công ty

Nguồn: user — "màn `admin/accounting/opening-contracts?type=all` fix khai báo hợp đồng
validate trùng nhau trong 1 công ty".

## Nguyên nhân
Rule `code => unique:opening_contracts,code` unique **toàn bảng** (bug gộp DB nhiều công ty).
Bảng `opening_contracts` không có cột `company_id`; công ty suy từ `created_by` → nhân viên →
`Company::getMembers($companyId)`. Chi tiết: `design.md`.

## Tasks
- [x] Task 1: `OpeningContractCreateRequest::rules()` — scope `code` unique theo công ty **người lập**
      (`auth()->user()->info->company_id` → `Company::getMembers()` → `Rule::unique(...)->where(whereIn created_by)`).
      Thêm `use App\Model\Common\Company;` + `use Illuminate\Validation\Rule;`. Message `code.unique` = "Đã tồn tại trong công ty".
- [x] Task 2: `OpeningContractUpdateRequest::rules()` — scope theo công ty **của HĐ đang sửa**
      (`$contract->employee_create->info->company_id`, fallback người đăng nhập) + `->ignore($id)`.
      Thêm `use App\Model\Accounting\OpeningContract;` + Company + Rule.
- [x] Task 3: `php -l` cả 2 file — không lỗi cú pháp.
- [x] Task 4: Commit (user tự commit — `080a1c32e6 "fix"` trên nhánh `gop_db`, 2 file, +37/-4).

## Ghi chú
- Fail-open: `companyId` null → `memberIds = []` → không chặn nhầm (xem design.md).
- KHÔNG backfill dữ liệu trùng cũ; KHÔNG thêm cột `company_id`; KHÔNG đụng FE/Blade.
- DB gộp trỏ remote (`hrm_erp_gop` / `hrm_erp_test`) → không tinker ghi dữ liệu để test.

## Checkpoint — 2026-10-14
Vừa hoàn thành: Fix 2 FormRequest scope unique mã HĐ đầu kỳ theo công ty; user đã commit
(`080a1c32e6`) trên nhánh `gop_db`.
Đang làm dở: không.
Bước tiếp theo: feature hoàn thành. (Chưa chạy test tay vì DB gộp trỏ remote; logic đã rà bằng đọc
code + `php -l`.)
Blocked: —
