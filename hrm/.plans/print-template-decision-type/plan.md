# Plan — print-template-decision-type

## Phase 1 — BE

### Database & Model
- [x] Migration thêm cột `decision_type` (string nullable, after `type`) vào `print_templates` (không bọc DB::transaction) — ĐÃ CHẠY
- [x] `PrintTemplate::$fillable` thêm `decision_type`

### Biến (PrintTemplateVariable)
- [x] Grep usage `PRINT_TEMPLATE_VARIABLES`/`::QUYET_DINH` — chỉ controller dùng (an toàn)
- [x] Thêm hằng `DECISION_COMMON_VARIABLES` (11 biến chung)
- [x] Thêm hằng `DECISION_TYPE_VARIABLES` theo `Decision::TYPE` (đủ các loại, theo bảng audit trong spec)
- [x] `buildVariablesForTemplateType($templateTypeId, $decisionType=null)`: QUYET_DINH build từ common + type; loại khác giữ nguyên (+ helper `buildDecisionVariables`)
- [x] Helper `decisionTypeOptions()` trả `[{id,text}]` từ `Decision::TYPE` (21 loại)

### API & Validation
- [x] `PrintTemplateVariableController::getVariables` nhận thêm `decision_type`
- [x] `getDecisionTypes()` + route `GET human/print-template-variables/get-decision-types`
- [x] `PrintTemplateRequest`: `decision_type` required_if type==2 + message

## Phase 2 — FE

- [x] add.vue: form thêm `decision_type`; nạp `decisionTypes`; computed `isDecisionType`; select "Loại quyết định" v-if; truyền decision_type vào get-variables; watch decision_type; reset khi đổi type; lỗi inline
- [x] _id/edit.vue: tương tự + prefill decision_type khi load mẫu

## Phase 2b — Tinh chỉnh biến
- [x] Bỏ biến `TRINH_DO` khỏi loại "Hợp đồng lao động" trong PrintTemplateVariable (dùng `TRINH_DO_HOC_VAN`); verify tinker không còn TRINH_DO, vẫn còn TRINH_DO_HOC_VAN; php -l sạch

## Phase 4 — Tổng quát hoá sub-type cho HĐLĐ (cùng cơ chế Quyết định)
Lý do: type 1 "Hợp đồng lao động" dùng chung cho HĐLĐ chính (DecisionLaborContractController) + Phụ lục HĐLĐ (AppendixLaborContractController); 6 biến trước/sau chỉ thuộc Phụ lục.
- [x] Đổi cột `decision_type` → `sub_type` (generic): rollback + đổi tên migration `2026_06_30_000001_add_sub_type...` + chạy lại; Model fillable
- [x] PrintTemplateVariable: thêm LABOR_CONTRACT_MAIN/APPENDIX + LABOR_CONTRACT_SUB_TYPES + LABOR_CONTRACT_COMMON_VARIABLES + LABOR_CONTRACT_SUB_TYPE_VARIABLES; rỗng hoá block type 1 cũ; buildSubTypeVariables() chung; buildVariablesForTemplateType($type,$subType) xử lý type 1 & 2, khác giữ nguyên
- [x] subTypeOptions($templateTypeId) generic (type2→Decision::TYPE 21, type1→2 sub-type HĐLĐ, khác→[]); thay getDecisionTypes → getSubTypes(Request) + route get-sub-types
- [x] getVariables dùng $request->sub_type; PrintTemplateRequest sub_type required_if:type,1,2 (QUYET_DINH + HOP_DONG_LAO_DONG)
- [x] FE add+edit: form.sub_type; computed hasSubType (type 1||2) + subTypeLabel động; onTypeChanged() nạp lại subTypes theo get-sub-types?template_type_id + reset sub_type nếu không hợp lệ; watch sub_type→loadVariables; prefill sub_type
- [x] Verify tinker + Playwright: HĐLĐ chính groups=THÔNG TIN CHUNG+"Hợp đồng lao động", KHÔNG còn 6 biến trước/sau, có TONG_THU_NHAP; Phụ lục có đủ 6 biến trước/sau + SO_PL_HDLD; đổi HĐLĐ→QĐ auto-reset sub_type + label "Loại quyết định" + 21 options; BE 422 khi type=1 thiếu sub_type, 200 khi có (DB id57 sub_type=appendix_labor_contract); đã dọn test; php -l sạch

## Phase 5 — Thêm biến cho QĐ tiếp nhận (catalog + fill thật)
- [x] Catalog: thêm 27 biến vào DECISION_TYPE_VARIABLES[accept_personnels] (QL trực tiếp + chức vụ QL, BO_PHAN/CHUC_DANH/CHUC_VU/CAP_BAC, P1/P2/P3, HINH_THUC_P3, TY_LE_HUONG_LUONG, TONG_THU_NHAP, TONG_LUONG_BHXH, TONG_THU_NHAP_100%, PC_DT/XX/K, THOI_GIAN_TIEP_NHAN_TU/DEN, HSNS: NGAY_SINH/GIOI_TINH/CMTND/NOI_CAP/NGAY_CAP/DIA_CHI_THUONG_TRU/CHUYEN_NGANH/TRINH_DO_HOC_VAN)
- [x] Fill thật trong AcceptPersonnelController::print: cột accept (employee_info_manager_name, recipient_part_name, working_position_name, employee_role_name, rank_name, p1/p2/p3_salary, according_fixed_p3→Khoán/Cố định, salary_percentage, total_salary, total_social_insurance_salary, enter_date/enter_date_to) + supportPayments/salaryAllowances (PC_DT/XX/K) + TONG_THU_NHAP_100% tự tính (TN + P1+P2+P3 + sum hỗ trợ + sum phụ cấp) + HSNS từ recipientEmployeeInfo (Carbon format, listAcademicLevels, employee_educations->last()->specialty). PHP 7.4 không dùng ?->
- [x] Verify tinker record id=88: TONG_THU_NHAP_100% 9.1M × 85% = TONG_THU_NHAP 7,735,000 khớp; HSNS/ngày/giới tính/CCCD/chuyên ngành đúng; php -l sạch; catalog accept 28 biến

## Phase 6 — Thêm biến cho HĐLĐ chính
- [x] Catalog: thêm CAP_BAC, BO_PHAN, HINH_THUC_P3, TY_LE_HUONG_LUONG vào LABOR_CONTRACT_SUB_TYPE_VARIABLES[labor_contract]
- [x] Fill DecisionLaborContractController::print: CAP_BAC=rank_name, BO_PHAN=labor_contract_part_name, HINH_THUC_P3=according_fixed_p3?Cố định:Khoán, TY_LE_HUONG_LUONG=((float)salary_percentage).'%'
- [x] Verify controller print() id=672 code200 (CB/P3=Khoán/TYLE=100%); catalog đủ 4; php -l sạch

## Phase 7 — Làm rõ mô tả biến (whose data)
- [x] Biến chung `TEN_PHONG_BAN` → "Phòng ban ban hành QĐ" (phân biệt phòng ban QĐ vs phòng ban nhân sự)
- [x] Đồng bộ mọi loại QĐ: `PHONG_BAN/BO_PHAN/CHUC_VU/CHUC_DANH/NGUOI_QUAN_LY_*_TRUOC/SAU_THAY_DOI` → thêm "của nhân sự (trước/sau thay đổi)"
- [x] Block chấm dứt HĐLĐ: rút gọn đồng bộ; giữ thu nhập/BHXH `*_TRUOC/SAU_THAY_DOI` nguyên (không mơ hồ). php -l sạch

## Phase 8 — Fix P3 & làm rõ TONG_THU_NHAP (QĐ tiếp nhận)
- [x] Fix CHUC_VU_NGUOI_QUAN_LY_TRUC_TIEP: dùng employee_manager_working_position_name (chức vụ) thay employee_manager_rank_name (cấp bậc, đang NULL)
- [x] Fix P3: LUONG_P3 chỉ hiện khi according_fixed_p3=1; HINH_THUC_P3 = Cố định/Khoán(by_contract)/rỗng; bỏ p3_salary cũ khi không tích cờ nào
- [x] TONG_THU_NHAP_100% chỉ cộng P3 khi cố định (dùng $p3Amount). Verify id=88 (cố định) + id=83 (không tích) qua fillReport; php -l sạch
- [x] TONG_THU_NHAP_100% BỎ cộng lương thâm niên (theo yêu cầu) = P1+P2+P3 cố định + phụ cấp + hỗ trợ

## Phase 9 — Bổ sung biến theo yêu cầu + bỏ mã tên người
- [x] Helper global `stripCodePrefix()` trong FormatHelper (bỏ tiền tố "MÃ - Tên"); refactor AcceptPersonnelController dùng helper chung (bỏ private method)
- [x] Catalog: Thành lập PB thêm `PHONG_BAN_THANH_LAP`; Giải thể thêm `PHONG_BAN_GIAI_THE`; Tiếp nhận thêm `PHONG_BAN_TIEP_NHAN`
- [x] Catalog: Gia hạn HĐLĐ thêm toàn bộ biến giống Tiếp nhận (org/lương/P1-P3/tổng/HSNS) — 29 biến
- [x] Catalog: Tạm hoãn + Chấm dứt HĐLĐ thêm biến dùng chung: CHUC_VU, PHONG_BAN, BO_PHAN, NGUOI_QUAN_LY_TRUC_TIEP, CHUC_VU_NGUOI_QUAN_LY_TRUC_TIEP, NGAY_SINH, NOI_CU_TRU, TRINH_DO_HOC_VAN, CCCD (suspend đã có sẵn NGAY_SINH/NOI_CU_TRU/CCCD)
- [x] Fill: Establishment PHONG_BAN_THANH_LAP=department_name; Dissolution PHONG_BAN_GIAI_THE=department->name; Accept PHONG_BAN_TIEP_NHAN=recipient_department_name
- [x] Fill: Renew print() nhân bản logic Accept (renew_* + renewEmployeeInfo + support/allowance)
- [x] Fill: Suspend + Termination thêm biến dùng chung (org từ *_department/part_name, QLTT, HSNS từ employeeInfo)
- [x] Bỏ mã mọi biến tên người (QLTT, NV nhận bàn giao, người tạm hoãn...) qua stripCodePrefix; php -l sạch 8 file
- [x] Verify tinker (dữ liệu thật): EST id8 PBTL=PHÒNG TỔNG HỢP; ACC id89 PBTN=PHÒNG QUẢN TRỊ THÔNG TIN + QL="Bùi Hữu Hanh" (đã bỏ mã); TERM id41 đủ 9 biến dùng chung. Renew/Suspend/Dissolution chưa có record để chạy số (code mirror pattern đã verify)

## Phase 10 — Fix bug mẫu in HĐLĐ chính
- [x] TONG_THU_NHAP_BANG_CHU thừa "đồng": convertNumberToWords (n2c dùng ICU vi SPELLOUT) đã tự kèm "đồng" → bỏ `. ' đồng'` ở print() + prepareContractData() (HĐLĐ), lan sang Appendix + SalaryChange cùng lỗi
- [x] PHAN_CONG_NHIEM_VU không lấy được: cột thật là `mission_name` (không phải `name`) → sửa map
- [x] CHUC_DANH sai nguồn: đổi `CHUC_DANH=employee_role_name`, bổ sung `CHUC_VU=working_position_name` (trước đây CHUC_DANH gán nhầm working_position_name, CHUC_VU chưa gán) — đồng bộ chuẩn QĐ tiếp nhận
- [x] php -l sạch 3 file; verify record 673: CD=Nhân viên phần mềm, CV=Nhân viên Công nghệ, BC="Ba triệu đồng" (1 đồng), NV liệt kê đủ

## Phase 11 — Bổ sung biến HĐLĐ + PLHĐ
- [x] HĐLĐ (MAIN): thêm SO_TIEN_HT_XANG_XE, SO_TIEN_HT_DIEN_THOAI, SO_TIEN_HT_AN_TRUA (từ support_payments) — catalog + fill
- [x] PLHĐ (APPENDIX) 3.1 Cá nhân: LOAI_QD, TEN_NHAN_VIEN(bỏ mã), GIOI_TINH, QUE_QUAN, NGAY_CAP_CMTND, NOI_CAP_CMTND, CHUYEN_NGANH, TRINH_DO_HOC_VAN, BANG_CAP, NOI_CU_TRU, DIA_CHI_THUONG_TRU, QUOC_TICH, DIEN_THOAI, MAIL + công ty (DAI_DIEN/CHUC_VU_DAI_DIEN/DIA_CHI/DIEN_THOAI/EMAIL/MST/STK/NGAN_HANG)
- [x] PLHĐ 3.2 Nhân sự: PHONG_BAN/BO_PHAN/CHUC_VU/CHUC_DANH _TRUOC/_SAU_THAY_DOI; CAP_BAC_TRUOC_TD/SAU_TD; LUONG_TN_TRUOC_TD
- [x] PLHĐ 3.3 Thu nhập: LUONG_TN_SAU_TD, SO_THANG_TN_TRUOC/SAU_TD, NGUOI_QL_TRUC_TIEP_TRUOC/SAU_THAY_DOI, LUONG_P1/P2/P3_TRUOC/SAU_TD, PC_DT/XX/K_TRUOC/SAU_TD, SO_TIEN_HT_XANG_XE/DIEN_THOAI/AN_TRUA _TRUOC/SAU_TD (6 biến TONG_* đã có sẵn) — catalog APPENDIX 65 biến
- [x] Fill AppendixLaborContractController: cá nhân từ appendix cols + employeeRelation->info (gender/email/nơi cấp/chuyên ngành/điện thoại); org/lương từ old_/new_; PC từ salary_allowances old/new; HT từ support_payments old_or_new (closure supportAmt/allowanceAmt); tên người/phòng ban bỏ mã. STK/NGAN_HANG_CONG_TY để rỗng (companies không có cột)
- [x] php -l sạch 3 file; verify: HĐLĐ id6 HT_DIEN_THOAI=300k; PLHĐ 409 đủ cá nhân/công ty/org (QLS="Bùi Thị Hồng Ngân" bỏ mã); PLHĐ id3 HT_DIEN_THOAI_TRUOC_TD=300k (lookup old/new đúng)
- [x] FIX: PC_DT/PC_XX (HĐLĐ + PLHĐ) đang lấy nhầm từ support_payments → đổi lấy đúng salary_allowances ('Phụ cấp điện thoại'/'Phụ cấp xăng xe'). Phụ cấp ≠ hỗ trợ. Verify HDLD id8 PC_DT=0 vs HT_DT=300k; id646 PC_DT=PC_XX=300k (từ phụ cấp) vs HT=0
- [x] Bỏ biến 1 giá trị khỏi PLHĐ (LUONG_P1/P2/P3, LUONG_TN, SO_THANG_TN, PC_DT/XX/K): lọc trong buildVariablesForTemplateType khi subType=appendix (HĐLĐ chính GIỮ NGUYÊN) + xoá fill trong AppendixLaborContractController. Verify catalog: HĐLĐ chính còn đủ 8, PLHĐ rỗng; print 409 biến cũ rỗng, biến _TRUOC/_SAU_TD vẫn chạy

## Phase 12 — Fix biến thiếu HĐLĐ/PLHĐ + test toàn bộ mẫu in QĐ
- [x] HĐLĐ: bổ sung fill QUE_QUAN (place_of_birth), DIEN_THOAI (personal_telephone), MAIL (email), DIEN_THOAI_CONG_TY (company->phone), EMAIL_CONG_TY (company->email). STK/NGAN_HANG_CONG_TY để rỗng (companies KHÔNG có cột)
- [x] PLHĐ: bug SO_PL_HDLD/SO_HD_TRONG_PLHD/SO_QD_TRONG_PLHD chưa map → thêm fill (code / decision_labor_contract_code / decision_code). Verify 409: PL=409/2026/PLHĐ-TPE, HD=494/.../HĐLĐ, QD=087/.../QĐĐC
- [x] Harness test tự động 18 loại QĐ + HĐLĐ + PLHĐ (scratchpad/print_test*.php): build template chứa tất cả biến catalog → chạy print() → soi biến rỗng. Kết luận: mọi biến rỗng còn lại đều do DATA NULL (record draft: decision code chưa cấp; old/new_part_name, employee_manager null; P3=0) hoặc KHÔNG có nguồn (STK/NGAN_HANG). KHÔNG còn biến nào thiếu map ngoài các fix trên
- [x] php -l sạch
- [x] Kiểm tra TĨNH (static_check.php) phủ 100% loại có controller: soi từng biến catalog có được gán trong controller/DecisionService không → 0 biến thiếu map cho TẤT CẢ 16 loại có biến riêng (kể cả 6 loại chưa có record: department_changes/renew/retirement/suspend/increase_seniority/salary_bonus)
- [x] Kết luận coverage: 20 loại có controller print → biến map đủ 100%. Loại catalog rỗng (manpower_planning/change, regulation_general/salary) chỉ dùng biến chung (setValuePrintDecision). Riêng termination_and_suspend_labor_contracts CHỈ là type label — không entity/bảng/controller/route print (chưa triển khai luồng in, ngoài phạm vi)

## Phase 13 — Bỏ STK_CONG_TY / NGAN_HANG_CONG_TY
- [x] Bỏ 2 biến khỏi catalog HĐLĐ chính + PLHĐ (LABOR_CONTRACT_SUB_TYPE_VARIABLES) và fill trong DecisionLaborContractController + AppendixLaborContractController (companies không có cột nguồn). php -l sạch, verify catalog đã bỏ

## Phase 3 — Verify
- [x] BE verify tinker: QĐ no-subtype→1 nhóm chung(11); QĐ+tiếp nhận→2 nhóm(11+1); QĐ+kỷ luật→2 nhóm(11+19); QĐ+giải thể→1 nhóm; HĐLĐ vẫn 3 nhóm; getDecisionTypes 21; getVariables qua resource OK; php -l sạch
- [x] Test UI (Playwright, namdangit): chọn Quyết định → select "Loại quyết định" hiện + panel chỉ nhóm chung (11); chọn kỷ luật → panel 32 dòng (chung 11 + riêng 19); lưu → DB id56 type=2 decision_type=employee_disciplines
- [x] Test UI: đổi loại sang "Biên bản xử lý" → ẩn select loại quyết định + reset decision_type='' + panel đổi sang biến Biên bản
- [x] Test UI: Quyết định bỏ trống loại → submit báo lỗi inline "Bắt buộc phải chọn loại quyết định" (FE + BE 422); có loại → 200
- [x] Test UI edit: mẫu đã lưu prefill decision_type + select2 + panel đúng (32 dòng); đã dọn record test id56

## Phase 14 — Command thay mẫu in hàng loạt cho decisions
- [x] BE: command `decision:replace-print-template {print_template_id} {type}` — validate mẫu in tồn tại + type hợp lệ (Decision::TYPE), đếm số record, confirm, update `print_template`/`print_template_id`/`print_template_type_id` cho mọi decisions cùng type (không đụng updated_at, bỏ qua đã xóa mềm)
- [x] Verify: php -l sạch; artisan list nhận command; dry-run 3 case (id sai → lỗi, type sai → in danh sách type hợp lệ, id 11 + accept_personnels → đếm 84 record, confirm No không ghi)

## Phase 15 — Chuẩn hóa tên phòng ban + biến TONG_THU_NHAP_100% (branch tpe-format-tenphongban, worktree)
- [x] Helper `formatDepartmentName()` (FormatHelper.php): bỏ mã → lowercase toàn bộ → nếu bắt đầu "phòng " thì "Phòng " + hoa chữ cái đầu phần còn lại, ngược lại chỉ hoa chữ cái đầu. VD "PHÒNG QUẢN TRỊ THÔNG TIN" → "Phòng Quản trị thông tin"; "QUẢN TRỊ THÔNG TIN" → "Quản trị thông tin"
- [x] Áp dụng formatDepartmentName cho MỌI biến tên phòng ban ở mẫu in QĐ: DecisionService (TEN_PHONG_BAN + DOI_TUONG_THUC_THI) + 15 controller (Accept/Appoint/Transfer/SalaryChange/Termination/Suspend/Retirement/EmployeeDiscipline/TrainingContract/Appendix/DepartmentDissolution/DepartmentChange/DepartmentEstablishment/Renew/DecisionLaborContract) — thay removeDepartmentCode/stripCodePrefix trên dòng phòng ban + wrap dòng raw
- [x] HĐLĐ: bổ sung biến TONG_THU_NHAP_100% (đã có trong catalog, controller chưa fill). Thêm method `calcTotalIncomeFullRate()` = (thâm niên+P1+P2+P3 nếu cố định) + Σphụ cấp actual + Σhỗ trợ actual (bỏ nhân salary_percentage). Fill cả print() và prepareContractData()
- [x] Verify: php -l sạch 17 file; unit test formatDepartmentName 10 case đúng; fillReport thay đúng {{TONG_THU_NHAP_100%}} không đụng {{TONG_THU_NHAP}}; công thức 100% khớp dữ liệu thật (id666/638/627/626 tỷ lệ 85%: total_salary = TONG_THU_NHAP_100% × 85%)
- [x] FIX picker: nhóm HĐLĐ chính (LABOR_CONTRACT_SUB_TYPE_VARIABLES[MAIN]) thiếu TONG_THU_NHAP_100% → thêm biến vào MAIN (dòng 233) + làm rõ mô tả TONG_THU_NHAP "(đã nhân tỷ lệ hưởng lương)". php -l sạch. Đã merge + push origin/tpe (806ce1cff)
