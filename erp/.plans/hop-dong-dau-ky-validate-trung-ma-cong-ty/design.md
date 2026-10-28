# Khai báo hợp đồng đầu kỳ — validate trùng mã theo công ty

## Mục tiêu
Màn `admin/accounting/opening-contracts` (Khai báo đầu kỳ → Hợp đồng đầu kỳ): số hợp đồng
(`code`) chỉ cần **duy nhất trong phạm vi 1 công ty**, KHÔNG phải duy nhất toàn bảng.

## Bối cảnh / Nguyên nhân
- DB gộp nhiều công ty (nhánh `gop_db`). Rule cũ `code => unique:opening_contracts,code`
  khoá unique **toàn bảng** → 2 công ty khác nhau không được trùng mã HĐ đầu kỳ, trong khi
  nghiệp vụ cho phép mỗi công ty tự quản mã của mình.
- Bảng `opening_contracts` **KHÔNG có cột `company_id`**. Công ty của bản ghi suy ra từ
  người lập: `created_by` → nhân viên → `info.company_id` → `Company::getMembers(companyId)`
  (danh sách id nhân viên cùng công ty).

## Giải pháp
Thu hẹp phạm vi unique về đúng các nhân viên cùng công ty, dùng `Rule::unique(...)->where()`
lọc `created_by IN (memberIds)`.

- **Tạo mới** (`OpeningContractCreateRequest`): công ty = công ty của **người đang đăng nhập**
  (`auth()->user()->info->company_id`).
- **Sửa** (`OpeningContractUpdateRequest`): công ty = công ty **của hợp đồng đang sửa**
  (`$contract->employee_create->info->company_id`), fallback về công ty người đăng nhập nếu
  không tìm thấy; thêm `->ignore($id)` để không tự báo trùng chính nó.

## Fail-open an toàn
Nếu `companyId` null (tinker/no-auth/dữ liệu khuyết) → `memberIds = []` → `whereIn('created_by', [])`
không khớp dòng nào → **không chặn nhầm** (nới lỏng chứ không chặn oan). Rule `required` của `code`
vẫn giữ nên không bỏ lọt trống.

## Phạm vi KHÔNG đụng
- Không thêm cột `company_id` vào `opening_contracts`.
- Không backfill / dọn dữ liệu trùng mã cũ.
- Không đổi message rule phổ biến ở lang (giữ `messages()` cũ của 2 request — chỉ ghi `code.unique`
  = "Đã tồn tại trong công ty" cho rõ nghĩa công ty).
- Không đụng FE/Blade (màn đã hiện lỗi `code` sẵn qua `invalid-feedback`).

## File chạm
- `app/Http/Requests/Accounting/OpeningContractCreateRequest.php`
- `app/Http/Requests/Accounting/OpeningContractUpdateRequest.php`

## Quan hệ
Cùng họ với feature `cong-no-dau-ky-chong-trung-hop-dong` (khoá trùng theo công ty khi gộp DB) —
nhưng khác màn, khác file: feature kia là **khai công nợ đầu kỳ** KH/NCC
(`DeclareDebtBeginningController` + `DeclareDebtSupplierBeginningController`), feature này là
**khai hợp đồng đầu kỳ** (`OpeningContract*Request`).
