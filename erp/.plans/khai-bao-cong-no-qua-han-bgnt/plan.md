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

## Fix "Loại hợp đồng" sai cho FirmContract nhóm nguyên tắc (QA 2026-09-05)
Bối cảnh: HĐ `DHNT_...` (Đơn hàng nguyên tắc / phụ lục nguyên tắc, type 7-10) hiển thị "Loại hợp đồng" = "Hợp đồng dự án". Root cause: `DeclareDebtBeginning::getDeptAbleType()` nhánh FirmContract chỉ tách [1,2,3]→"Hợp đồng hãng", còn lại (kể cả nguyên tắc 7-10) rơi vào else → "Hợp đồng dự án". Chốt PA1: 3 rổ.
- [x] `getDeptAbleType()` nhánh FirmContract: 1,2,3→"Hợp đồng hãng"; 7,8,9,10→"Hợp đồng nguyên tắc"; còn lại (4,5,6)→"Hợp đồng dự án" — php -l sạch
- [x] sibling cùng bug: `DeclareDebtSupplierBeginning::getDeptAbleType()` (công nợ đầu kỳ NCC) dòng 281-286 — sửa đồng bộ 3 rổ; php -l sạch; verify type 8 → "Hợp đồng nguyên tắc"

## Fix đổi khách hàng không reset HĐ đã chọn (QA 2026-09-05)
Bối cảnh: chọn khách A + HĐ của A → đổi sang khách B → danh sách HĐ (`$scope.items`) không reset → lưu ra công nợ của B nhưng HĐ vẫn là của A. Root cause: `<select select2-customers-in-modal ng-model="customer_id">` không có handler reset `items` khi đổi khách; native `change` chỉ update `customer_id`.
- [x] `index.blade.php`: thêm `$(document).on('select2:select select2:clear', '.select2-customers-in-modal', ...)` reset `$scope.items=[]` + `errors=null` khi người dùng đổi/xoá khách; dùng event select2 (không phải native change) nên KHÔNG kích khi edit()/clearData() `.trigger('change')`; guard `editId` (form Sửa khoá khách)
- [x] defense-in-depth BE `store()`: mỗi HĐ item → `find(deptable_id)`, nếu không tồn tại hoặc `customer_id` lệch request customer_id → thêm vào `$errors["items.$key.contract_id"]` + `continue` (KHÔNG throw ValidationException vì catch(\Exception) của method sẽ nuốt); đổi message `responseErrors` rỗng → "Không thể khai báo, vui lòng kiểm tra lại."; guard `class_exists` + `isset(customer_id)` (bỏ qua loại HĐ không có cột). Verify 5 loại HĐ khách (firm/opening/wr_service/service/contracts) đều có customer_id; php -l sạch

## Fix import KH crash im lặng khi Loại HĐ không khớp mã HĐ (QA 2026-09-05)
Bối cảnh: file import điền Loại HĐ = "HDDK" (OpeningContract) nhưng mã HĐ là `HĐDA_/DHNT_` (FirmContract) → `$contract=null` → import "không được mà không báo lỗi gì". Root cause: `DeclareDebtBeginningImport::collection()` THIẾU null-check `$contract` (bản NCC dòng 90-93 đã có, bản KH viết sót) → chạy tiếp `$contract->id` (dòng 156) → PHP warning → Laravel ném ErrorException (ngoài try-catch nội bộ) → controller `catch` dính `dd($e)` (debug leftover) → dump HTML rồi die → FE không parse được JSON → không hiện lỗi. (KHÔNG phải do quá hạn=1 + điền ngày BGNT — path đó dòng 151-153 tự null ngày, vô hại.)
- [x] `DeclareDebtBeginningImport`: sau chuỗi if/else loại HĐ, thêm 2 guard trước khi lookup account — (1) `contractType` không thuộc {HDMNN,HDMN,HDMTN,HDDK,HDHNTDA,HDDV} → logError "Loại hợp đồng không hợp lệ"; (2) `!$contract` → logError "Mã hợp đồng không tồn tại hoặc không khớp loại hợp đồng đã chọn" + continue; đồng bộ với sibling NCC
- [x] `DeclareDebtBeginningController::import()` catch: bỏ `dd($e)` (debug leftover nuốt lỗi thành HTML dump) → `DB::rollBack()` + `responseErrors('Đã có lỗi xảy ra! '.$e->getMessage())`; sibling NCC controller đã đúng sẵn (không đụng)
- [x] php -l sạch import + controller KH; xác nhận sibling NCC import đã có null-check + controller NCC không có dd (không cần sửa)
- Lưu ý user: file mẫu của user đang điền SAI cột Loại HĐ — mã `HĐDA_/DHNT_` là FirmContract nên phải điền **HDHNTDA** (không phải HDDK); sửa lại rồi import lại

## Cách A — Loại HĐ import tự nhận (không bắt buộc) (QA 2026-09-05)
User chốt Cách A: bỏ yêu cầu điền mã Loại HĐ khó nhớ (HDHNTDA...), hệ thống tự dò mã HĐ qua các bảng. Kiểm tra DB dev_erp_2: HĐ khách (opening/firm/wr) tiền tố khác nhau → 0 trùng mã; chỉ 2 mã trùng ở 2 bảng HĐ mua (test rác, không liên quan). → an toàn, vẫn giữ cột Loại HĐ làm fallback phân biệt khi hiếm hoi trùng.
- [x] `DeclareDebtBeginningImport`: thêm hằng `CONTRACT_TYPE_MAP` (mã→model) + helper `findContractByCode($class,$code)` (chỉ select id, FirmContract giữ whereNull is_zt). Logic mới: Loại HĐ có điền → validate ∈ map rồi tìm đúng loại; để trống → dò mã qua tất cả loại, 0 match→"không tồn tại", >1 match→"trùng nhiều loại, điền Loại HĐ để phân biệt", đúng 1→dùng. Bỏ `contractType` khỏi check bắt buộc + skip-empty. Thay khối if/else 6 nhánh (unused heavy select/with) bằng logic gọn
- [x] File mẫu `public/samples/ImportExcel_Congnodaukikhachhang.xlsx`: header D3 → "Loại hợp đồng (không bắt buộc - để trống tự nhận)" + wrap text; bỏ ví dụ D4 (minh hoạ để trống được). KHÔNG thêm dòng → giữ start_row=4
- [x] php -l sạch; test tinker auto-detect trên mã thật: firm→HDHNTDA, opening→HDDK, wr→HDDV (mỗi mã unique 1 loại), mã sai→không tìm thấy

### Checkpoint — 2026-09-05
Vừa hoàn thành: fix nhãn "Loại hợp đồng" nhóm nguyên tắc (PA1, 3 rổ) tại `DeclareDebtBeginning.php:358-366`. php -l sạch.
Đang làm dở: không.
Bước tiếp theo: user QA trên UI (dev-erp.dnsmedia.vn) — HĐ prefix DHNT/HĐNT phải hiện "Hợp đồng nguyên tắc".
Blocked: HĐ trong ảnh nằm trên DB dev-erp.dnsmedia.vn, DB local (erp_hrm_check) không có bản ghi → chưa verify được bằng tinker local.

## Fix quá hạn chỉ áp dụng Dư nợ (QA 2026-09-05)
Bối cảnh: form cho tích "quá hạn" + điền Ngày BGNT ngay cả khi kiểu dư = **Dư có**. Sai nghiệp vụ: công ty chỉ tính quá hạn cho **Dư nợ** (KH nợ tiền công ty). Root cause: `is_overdue`/`acceptance_handover_date` không bị ràng buộc theo `type_dept` ở cả 3 đường ghi (FE form + BE store/update + import Excel). Chốt: quá hạn chỉ hợp lệ khi `type_dept=1` (Dư nợ).
- [x] FE `index.blade.php`: checkbox quá hạn `ng-disabled="item.type_dept != 1"`; ô Ngày BGNT `ng-if` gộp thêm `type_dept == 1`; dropdown Dư nợ/Dư có gọi `setTypeDept(item,val)` — chuyển Dư có → bỏ tick + xoá ngày
- [x] BE `store()` + `update()`: `is_overdue = (type_dept==1) && !empty(is_overdue)`; ngày BGNT chỉ giữ khi is_overdue (defense in depth)
- [x] Import `DeclareDebtBeginningImport`: nếu "Dư có" mà đánh dấu quá hạn → logError "Chỉ công nợ Dư nợ mới được đánh dấu quá hạn" + continue (không âm thầm đổi)
- [x] `php -l` sạch 3 file

### Checkpoint — 2026-09-05 (fix quá hạn chỉ áp dụng Dư nợ)
Vừa hoàn thành: FE (disable checkbox + ẩn ngày + setTypeDept reset khi đổi Dư có) + BE store/update (ép is_overdue theo type_dept) + import (logError Dư có mà quá hạn). php -l sạch 3 file.
Đang làm dở: không.
Bước tiếp theo: user QA trên UI — chọn Dư có thì checkbox quá hạn bị khoá; đang tích quá hạn (Dư nợ) mà đổi sang Dư có thì tự bỏ tick + mất ô ngày.
Blocked: không.

## Fix chặn trùng khi Sửa (QA 2026-09-05)
Bối cảnh: user hỏi "1 tài khoản chỉ khai công nợ 1 lần cho 1 hợp đồng, đã validate chưa". Rà 3 đường ghi: store (controller:144-154) + import (import:172-181) đã chặn trùng theo `account_id + customer_id + deptable_id + deptable_type`; **update() chưa có check nào** → sửa bản ghi rồi đổi `account_id` sang TK đã khai của cùng HĐ sẽ tạo trùng.
- [x] `update()`: thêm query chặn trùng đầu vòng lặp — cùng key (account/customer/deptable) `where('id','!=',$declare->id)`, trùng → `DB::rollBack()` + `responseErrors` key `items.$key.account_id` = "Đã khai báo đầu kỳ cho tài khoản này"; đổi `foreach` sang `$key => $item` để build key lỗi
- [x] `php -l` sạch controller

### Checkpoint — 2026-09-05 (chặn trùng khi Sửa)
Vừa hoàn thành: bổ sung chặn trùng "1 TK/1 HĐ khai 1 lần" ở update() (store + import đã có sẵn). php -l sạch.
Đang làm dở: không.
Bước tiếp theo: user QA — sửa 1 bản khai, đổi TK sang TK đã khai của cùng HĐ → phải báo "Đã khai báo đầu kỳ cho tài khoản này".
Blocked: không.

## Fix import chỉ cho HĐ Có hiệu lực (QA 2026-09-05)
Bối cảnh: user báo import công nợ vẫn cho HĐ đã quyết toán (`HDDV_TPE_HN_KD2_26_0007_...`). Điều tra: chỉ HDDV (WrServiceContract, DA_QUYET_TOAN=5) và HDHNTDA (FirmContract, DA_QUYET_TOAN=10) có khái niệm quyết toán; HDDK + 3 loại HĐ mua không có. User chốt: **đổi sang allowlist — import CHỈ cho HĐ đang Có hiệu lực** (CO_HIEU_LUC: HDDV=3, HDHNTDA=3). Loại không có vòng đời hiệu lực (HDDK, HĐ mua) không kiểm tra.
- [x] `DeclareDebtBeginningImport`: thêm const `CONTRACT_EFFECTIVE_STATUS` = [FirmContract=>CO_HIEU_LUC(3), WrServiceContract=>CO_HIEU_LUC(3)]
- [x] Sau khi resolve `$contract`/`$type`: nếu `$type` thuộc map mà `status != CO_HIEU_LUC` → logError "Hợp đồng không ở trạng thái Có hiệu lực — chỉ được khai báo công nợ đầu kỳ cho hợp đồng đang có hiệu lực" + continue (báo theo dòng)
- [x] `findContractByCode`: select thêm `status` chỉ cho 2 loại trong map (HDDK không có cột status → không select thừa)
- [x] `php -l` sạch import
- [x] Áp cùng rule ở form thêm `store()` (user xác nhận "có"): sau check "HĐ thuộc KH", đọc `DeclareDebtBeginningImport::CONTRACT_EFFECTIVE_STATUS` (dùng chung, 1 nguồn sự thật) — nếu loại thuộc map mà `$deptable->status != CO_HIEU_LUC` → `$errors["items.$key.contract_id"]` = lỗi hiệu lực + continue. `php -l` sạch controller.

- [x] Lọc popup chọn HĐ ở form (user xác nhận "ok lọc luôn dropdown"): root cause = modal truyền `d.type='declare_debt_beginning'` (đã có comment ý định lọc) nhưng `SearchContractService::searchAllContract` KHÔNG có nhánh cho type này → rơi vào return mặc định (trả tất cả HĐ kể cả đã quyết toán). Fix: thêm `if ($request->type == 'declare_debt_beginning')` ngay trước return mặc định → `$firm_contract->where('status', FirmContract::CO_HIEU_LUC)` + `$warranty_repair_contracts->where('status', WrServiceContract::CO_HIEU_LUC)`. Type riêng modal này → KHÔNG ảnh hưởng ~10 caller khác của searchAllContract (settlement, hand_over, service export…). `php -l` sạch.

### Checkpoint — 2026-09-05 (import + form thêm + dropdown chỉ HĐ Có hiệu lực)
Vừa hoàn thành: chặn HĐ không Có hiệu lực (HDDV/HDHNTDA status≠3) ở 3 lớp: (1) import lỗi từng dòng, (2) form store() lỗi inline ô HĐ, (3) popup chọn HĐ chỉ hiện HĐ Có hiệu lực (SearchContractService nhánh type='declare_debt_beginning'). php -l sạch 3 file (import, controller, service).
Đang làm dở: không.
Bước tiếp theo: user QA — (1) popup chọn HĐ không còn hiện HĐ HDDV/HDHNTDA đã quyết toán/hết hiệu lực; (2) import + form thêm vẫn chặn (defense in depth). Chưa commit.
Blocked: không.

## Loại HĐNT khỏi khai báo công nợ đầu kỳ (QA 2026-09-05)
Bối cảnh: user báo popup chọn HĐ vẫn hiện HĐNT (`HĐNT_TPE_HN_KD2_26_0007_TESTQTC5`). Bản chất: Hợp đồng nguyên tắc KHÔNG theo dõi công nợ trực tiếp → không được khai báo công nợ đầu kỳ. `FirmContract::type` (khác `status`): 7=HĐNT (HOP_DONG_NGUYEN_TAC), 8=ĐHNT, 9/10=phụ lục nguyên tắc. User chốt: **"cứ bỏ hdnt thôi đã, áp cả 2"** → chỉ loại type=7, áp cả popup + import + form store.
- [x] Popup `SearchContractService` nhánh `declare_debt_beginning`: thêm `$firm_contract->where('firm_contracts.type', '!=', FirmContract::HOP_DONG_NGUYEN_TAC)` (qualify vì SELECT có alias "firm_contract" as type)
- [x] Import `DeclareDebtBeginningImport`: `findContractByCode` select thêm `type` cho FirmContract; sau check hiệu lực → nếu `$type===FirmContract::class && $contract->type==HOP_DONG_NGUYEN_TAC` → logError "Không khai báo công nợ đầu kỳ cho Hợp đồng nguyên tắc (HĐNT)" + continue
- [x] Controller `store()`: thêm `use FirmContract`; sau check hiệu lực → nếu `deptable_type===FirmContract::class && $deptable->type==HOP_DONG_NGUYEN_TAC` → `$errors["items.$key.contract_id"]` = lỗi HĐNT + continue
- [x] `php -l` sạch 3 file

### Checkpoint — 2026-09-05 (loại HĐNT)
Vừa hoàn thành: loại HĐNT (FirmContract type=7) khỏi 3 đường: popup chọn HĐ (SearchContractService) + import (logError từng dòng) + form store (lỗi inline). Chỉ type=7, chưa đụng ĐHNT/phụ lục (8/9/10). php -l sạch 3 file.
Đang làm dở: không.
Bước tiếp theo: user QA — popup không còn hiện HĐNT; import/form nhập HĐNT vẫn bị chặn (defense in depth). Chưa commit. Nhắc: các thay đổi loạt này đang LOCAL/chưa deploy — QA trên server cần deploy trước.
Blocked: không.
