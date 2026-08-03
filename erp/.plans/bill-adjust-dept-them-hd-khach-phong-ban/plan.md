# Bill Adjust Dept: thêm chọn HĐ/khách + phòng ban — Implementation Plan

> Subagent-driven. Project Laravel 6 + Blade + AngularJS 1.3.9, không có test framework → verify = `php -l` + tinker + browser. Không commit khi chưa được yêu cầu.

**Goal:** Màn `bill_adjust_dept/create`: chọn thêm Phòng ban làm đối tượng, bỏ cột "Số phiếu yc xuất hàng" (FE), thêm HĐ mua dịch vụ + Đơn bảo hiểm vào chọn HĐ.

## Trạng thái: CODE XONG cả 3 task (chưa commit), chờ user test browser

- [x] **Task 1 — Bỏ cột "Số phiếu yc xuất hàng" (FE):** xóa th/td ở `form.blade.php` + `formShow.blade.php`. Giữ JS/BE/`exportable_*`. Hàng tổng colspan=5 (cụm tiền) không lệch. Review ✅.
- [x] **Task 2 — Phòng ban làm đối tượng:** `SearchController@searchObject` thêm union `departments` (status=1 + company của user) qua flag `include_department`; `BillAdjustDeptDetail::chooseCustomer` gửi `include_department=1`. Verified `type_object === Department::class`. Không cần whitelist (Department đã wire sẵn ở `BillAdjustDept.php:632` → `obj_department_id`). Review ✅.
- [x] **Task 3 — Thêm HĐ mua DV + Đơn bảo hiểm (hướng A: chỉ thêm):** `SearchContractService` thêm query `$insurance_principle_form` + return riêng `bill_adjust_dept` = union mặc định + insurance; `extrated` thêm filter status (buy_service DA_DUYET=3, insurance DA_DUYET=2 + company); thêm `insurance_principle_form` vào 3 list lọc supplier_id. `SearchController@searchAllContract` map type→class (`InsurancePrincipleForm::class`, objectable=Supplier, contract_link route `insurance.principleForm.show`). FE không cần sửa. **Reviewer subagent: Spec ✅, không regression**, chỉ Minor.

## Minor findings (tùy chọn, để final review / user quyết)
- `objectable_name`/`objectable_code` (SearchController ~2305/2318) hard-code tra bảng `customers` → với HĐ supplier-based (gồm buy_service + insurance) tên/mã NCC có thể hiển thị rỗng ở 1 số chỗ. **Là hành vi CŨ** (đã vậy với buy_contract_2, buy_service...), không do task này. Cần kiểm tra khi test browser nếu muốn hiển thị tên NCC.
- Có thể null-coalesce `auth()->user()->info->company_id` (convention sẵn có, không bắt buộc).
- Block return `bill_adjust_dept` sao chép union mặc định (chỉ thêm 1 dòng) — cleanup tùy chọn.

## Verify đã chạy
- `php -l` sạch toàn bộ file BE.
- tinker: departments status=1 có company = 62; type_object khớp Department::class; BuyServiceContract::DA_DUYET=3, InsurancePrincipleForm::DA_DUYET=2. (Insurance count=0 ở dev_erp_2 local — chưa seed, không phải lỗi code.)

## Còn lại
- [ ] User test browser 3 mục trên `bill_adjust_dept/create` (đối tượng phòng ban; không còn cột YCXH; chọn HĐ mua DV + đơn bảo hiểm theo NCC).
- [ ] (nếu OK) commit theo yêu cầu user.

### Checkpoint — 2026-06-23
Vừa hoàn thành: code 3 task qua subagent-driven, review từng task (Task 3 có reviewer subagent), php -l sạch. Chưa commit.
Bước tiếp theo: user test browser. Lưu ý kiểm hiển thị tên NCC cho dòng insurance/buy_service (Minor #1).
Blocked:
