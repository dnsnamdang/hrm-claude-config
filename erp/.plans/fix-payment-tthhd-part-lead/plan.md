# Fix: trưởng bộ phận không thấy HĐ khi đề nghị chi thưởng thực hiện HĐ (payment_TTHHD)

**Mục tiêu:** Trưởng bộ phận (part lead) thấy được HĐ để lập đề nghị thanh toán loại "chi thưởng thực hiện hợp đồng".

## Bối cảnh
- Màn: `admin/income-expenditure/bill_payment_requests/create`, API `modal_data/searchAllContract?type=payment_TTHHD`.
- Hàm: `SearchContractService::extrated()` nhánh `payment_TTHHD` (firm_contract).
- Case: user Nguyễn Minh Quân (emp 122) không thấy HĐ `HĐ_TPE_HN_KDTM_26_0614_PVT 1368` (id=19810).

## Root cause
Filter cũ chỉ cho HĐ hiện khi user là:
1. nhân sự trong `firm_support_accounting_employees` (FSAE), HOẶC
2. trưởng phòng (`departments.department_lead_id = user`) khớp `fsad.department_id`.

Thiếu **trưởng bộ phận**. FSAD lưu `objectable_type=Part, objectable_id=<part_id>` và có cột `*_part_lead_percent` (trưởng BP hưởng 20%). Quân là `parts.part_lead_id` của part 27 (thuộc phòng 47) — đúng part trong FSAD của HĐ 19810 — nhưng filter không xét part lead → HĐ bị loại.

## Tasks
- [x] ~~(Sai hướng) thêm part-lead vào FSAE~~ → user phản hồi lấy HĐ **theo hạch toán**, không theo nhân sự hỗ trợ HT.
- [x] Revert part-lead, bỏ import `Part`, `FirmSupportAccountingEmployee`, `WrSupportAccountingEmployee`.
- [x] Nhánh `payment_TTHHD` lấy `$firm_ids`/`$wr_ids` từ **`account_details`**: `account_id = (3351)` + `work_id = (TTHHD)` + `employee_id = user`, resolve id qua `accounts.identify_number='3351'` (=117) và `works.code='TTHHD'` (=12) để không hardcode.
- [x] Giữ filter status/type sẵn có (loại HĐ Đang tạo/Chờ duyệt/Từ chối/Hủy; type [1,4,7,8] firm, [1,2] wr).
- [x] Verify (prod erp_new): Quân(122) → 4 HĐ, có 19810 ✅; user không có hạch toán → 0 HĐ. `php -l` sạch.

## Logic chuẩn (chốt)
HĐ hiện trong popup chọn HĐ lập đề nghị "chi thưởng thực hiện HĐ" (`type=payment_TTHHD`) ⇔ user đăng nhập có **dòng hạch toán** trong `account_details` gắn với HĐ đó: `account_id` = TK **3351** (id 117) + `work_id` = công việc **TTHHD** (id 12) + `employee_id` = user. Áp cho cả firm_contract (contractable_type=FirmContract) và wr_contract (WrServiceContract).

### Checkpoint — 2026-06-16
Vừa hoàn thành: đổi logic payment_TTHHD sang lọc theo account_details (TK 3351 + work TTHHD + employee_id). Verify Quân thấy 19810.
Bước tiếp theo: user test trên UI.
Blocked:

## Yêu cầu mới (2026-06-17): KẾT HỢP cả 2 logic (union)
User: lấy HĐ payment_TTHHD = **hợp** của 2 nguồn, HĐ hiện nếu khớp BẤT KỲ:
1. Hạch toán: `account_details` TK 3351 + work TTHHD + employee_id = user (logic hiện tại).
2. Logic cũ: nhân sự hỗ trợ HT (`FirmSupportAccountingEmployee`/`WrSupportAccountingEmployee`) HOẶC trưởng phòng (`departments.department_lead_id = user`) khớp `fsad.department_id`.

Giữ nguyên filter status/type ngoài (firm: bỏ [Đang tạo/Chờ duyệt/Từ chối/Hủy], type [1,4,7,8]; wr: bỏ [Đang tạo/Chờ duyệt/Hủy], type [1,2]).

### Tasks
- [x] Re-add import `FirmSupportAccountingEmployee`, `WrSupportAccountingEmployee`
- [x] payment_TTHHD: `firm_ids`/`wr_ids` = `array_unique(array_merge(accounting, old))` cho cả firm & wr
- [ ] `php -l` sạch + user test UI

### Checkpoint — 2026-06-17
Vừa hoàn thành: union logic hạch toán + logic cũ trong nhánh payment_TTHHD.
Bước tiếp theo: user test UI.
Blocked:
