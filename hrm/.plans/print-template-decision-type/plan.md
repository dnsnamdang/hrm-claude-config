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

## Phase 3 — Verify
- [x] BE verify tinker: QĐ no-subtype→1 nhóm chung(11); QĐ+tiếp nhận→2 nhóm(11+1); QĐ+kỷ luật→2 nhóm(11+19); QĐ+giải thể→1 nhóm; HĐLĐ vẫn 3 nhóm; getDecisionTypes 21; getVariables qua resource OK; php -l sạch
- [x] Test UI (Playwright, namdangit): chọn Quyết định → select "Loại quyết định" hiện + panel chỉ nhóm chung (11); chọn kỷ luật → panel 32 dòng (chung 11 + riêng 19); lưu → DB id56 type=2 decision_type=employee_disciplines
- [x] Test UI: đổi loại sang "Biên bản xử lý" → ẩn select loại quyết định + reset decision_type='' + panel đổi sang biến Biên bản
- [x] Test UI: Quyết định bỏ trống loại → submit báo lỗi inline "Bắt buộc phải chọn loại quyết định" (FE + BE 422); có loại → 200
- [x] Test UI edit: mẫu đã lưu prefill decision_type + select2 + panel đúng (32 dòng); đã dọn record test id56
