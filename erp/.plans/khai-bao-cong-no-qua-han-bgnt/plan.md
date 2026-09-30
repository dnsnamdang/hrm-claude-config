# Plan — Khai báo công nợ đầu kỳ (KH): thêm "Công nợ quá hạn" + "Ngày BGNT"

Nhánh `master` (ERP) · @namdangit · màn `admin/accounting/declare-debt-beginning`

Thêm 2 trường **per-row** vào modal Thêm/Sửa công nợ đầu kỳ:
- `is_overdue` — checkbox "Công nợ quá hạn", mặc định KHÔNG tích
- `acceptance_handover_date` — datepicker dd/mm/yyyy "Ngày BGNT", cho quá khứ + hôm nay (chặn tương lai), **bắt buộc nếu tích quá hạn**

## Tasks
- [x] Migration `add_overdue_bgnt_to_declare_debt_beginning_table` (guard hasColumn): `is_overdue` boolean default 0, `acceptance_handover_date` date nullable — đã migrate
- [x] Model `DeclareDebtBeginning`: fillable +2, `$dates` += acceptance_handover_date, cast is_overdue boolean
- [x] `DeclareDeptStoreRequest`: rules `items.*.is_overdue` nullable|boolean; `items.*.acceptance_handover_date` nullable|required_if quá hạn|date + message
- [x] `DeclareDeptUpdateRequest`: rules tương tự (modal Sửa dùng chung form)
- [x] Controller `store()` + `update()`: set `is_overdue` + `acceptance_handover_date` (normalize: bỏ tích → date=null)
- [x] View `index.blade.php`: 2 cột header (Quá hạn / Ngày BGNT) + ô nhập per-row (checkbox + dateForm max-today), submit map +2 field, `onOverdueChange` clear ngày khi bỏ tích, selectContract default is_overdue=false, nhánh `.edit` đổ lại 2 field từ dataEdit
- [x] Migrate (DB dev_erp_2) + `php -l` sạch + test Validator required_if per-row (checked-nodate→lỗi, checked-date→ok, unchecked→ok)

## Import Excel + file mẫu
- [x] `DeclareDebtBeginningImport`: `$start_row` 2→4 (2 dòng lưu ý + header), đọc thêm `$row[7]` (quá hạn), `$row[8]` (BGNT); validate quá hạn ∈ {1,2}, parse BGNT dd/mm/yyyy (hỗ trợ serial Excel + text), chặn tương lai, bắt buộc BGNT khi quá hạn=2; set `is_overdue` + `acceptance_handover_date` khi tạo declare; thêm helper `parseDate()`
- [x] File mẫu `public/samples/ImportExcel_Congnodaukikhachhang.xlsx`: tạo lại 9 cột — Row1+2 lưu ý (đỏ, đậm), Row3 header (STT, Mã KH*, Mã HĐ*, Loại HĐ, Số TK*, Loại dư, Công nợ*, Công nợ quá hạn* [1-không/2-có], Ngày BGNT [dd/mm/yyyy]), Row4 ví dụ
- [x] `php -l` sạch import class + verify đọc lại file mẫu đúng 4 dòng

## Danh sách + In + Xuất Excel (theo form mới)
- [x] `searchData()`: editColumn `is_overdue` → "Có"/"Không", `acceptance_handover_date` → d/m/Y (rỗng nếu null)
- [x] Blade list `columns:`: thêm 2 cột "Quá hạn" + "Ngày BGNT" sau "Dư có"
- [x] Model `printListData()`: thêm 2 cột (header + row) sau "Dư có" → 14 cột (dùng chung cho in + xuất Excel)
- [x] `exportList()`: COLSPAN 12 → 14 (khớp số cột mới)
- [x] `php -l` sạch; `searchByFilter` select `*` (không giới hạn cột) nên FE nhận đủ 2 cột mới

## Báo cáo công nợ quá hạn: nhặt thêm từ khai báo đầu kỳ (is_overdue=1) — phương án A
Bối cảnh (đã nghiên cứu): HĐ khai đầu kỳ rớt khỏi báo cáo quá hạn vì thiếu `payment_overdue_date` (chỉ set qua quy trình bàn giao trong hệ thống = `handover_date + over_date`) → `number_overdue=0` bị lọc; và nhiều loại HĐ/tài khoản nằm ngoài phạm vi quét (chỉ firm/wr + account 22). Ngày BGNT đóng vai trò `handover_date`.
Phương án A: `number_overdue = DATEDIFF(date_to, Ngày BGNT)`, `begin = dept_value` (dấu theo Dư nợ/Dư có), debt=has=0; attribution theo **người tạo HĐ** (khớp company/department/part đã lưu trên bản ghi khai báo).
- [x] `HandleDebtOverDueService::getDeclareOverDueRows($request,$permissions)`: gom `DeclareDebtBeginning where is_overdue=1`, BGNT<date_to, net>0, overdue>0; build row cùng shape nguồn chính (18 field); áp filter request (contract_code/customer/company/department/part/employee) + phân quyền mirror nguồn chính (company/department/part OR HĐ do mình tạo)
- [x] `getData()`: merge nguồn mới — dedup theo khoá `contractable_id-contractable_type` (chỉ thêm HĐ chưa có ở nguồn chính, tránh cộng đôi); nhánh detail `concat`, nhánh total cộng sum (khởi tạo object 0 nếu total null)
- [x] Import `DeclareDebtBeginning` + `Carbon` vào service
- [x] `php -l` sạch; verify chuỗi quan hệ `deptable.employee_create.info.department` resolve qua tinker (dev_erp_2, 1 bản ghi is_overdue=1); tự chảy ra cả xem/In/Xuất Excel (dùng chung getData→render/getTable)

## Fix phát sinh (QA)
- [x] **Datepicker Ngày BGNT không mở lịch** — root cause: viết attribute `dateForm` (camelCase) → browser lowercase thành `dateform`, Angular chuẩn hoá không khớp directive `dateForm` (129 chỗ khác đều viết kebab `date-form`) → directive không link, datetimepicker không init. Fix: đổi `dateForm` → `date-form`. Kèm đổi `ng-disabled="!item.is_overdue"` → `ng-if="item.is_overdue"` để input được tạo mới (enabled, visible) đúng lúc tick → directive link trên input hợp lệ; bỏ tick hiện "—".

### Checkpoint — 2026-08-26 (hoàn thành code)
Vừa hoàn thành: toàn bộ BE + FE. Migration chạy trên dev_erp_2 (2 cột đã tồn tại). php -l sạch 5 file.
Validator test qua tinker khớp yêu cầu: tích quá hạn mà trống BGNT → báo lỗi "Bắt buộc nhập khi công nợ quá hạn"; tích + ngày hợp lệ → ok; không tích → ngày không bắt buộc.
Đang làm dở: không có.
Bước tiếp theo: user QA trên UI (tạo/sửa 1 bản ghi công nợ đầu kỳ: tích/bỏ tích quá hạn, chọn ngày quá khứ).
Blocked:
