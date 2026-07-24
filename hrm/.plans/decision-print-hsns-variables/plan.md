# decision-print-hsns-variables — Plan

Spec: `docs/superpowers/specs/2026-07-14-decision-print-hsns-variables-design.md`
Plan chi tiết: `docs/superpowers/plans/2026-07-14-decision-print-hsns-variables.md`

## Phase 1 — Metadata
- [x] T1. PrintTemplateVariable.php: thêm biến Nhóm A (13×5 loại) + B (CAP_BAC×3) + C (9 biến×2 loại) + D (THOI_GIAN_HDLD_HIEN_TAI vào LABOR_CONTRACT_COMMON); biến ngày kèm is_date

## Phase 2 — Value-fill
- [x] T2. Appoint + Transfer + SalaryChange: 13 HSNS + 2 CAP_BAC
- [x] T3. Retirement + EmployeeDiscipline: 13 HSNS
- [x] T4. Termination (1 khối) + Suspend (2 khối): 9 biến (gồm THOI_GIAN_HDLD_HIEN_TAI)
- [x] T5. DecisionLaborContract (2 khối $result/$data) + Appendix: THOI_GIAN_HDLD_HIEN_TAI

## Phase 3 — Verify
- [x] T6. php -l + tinker in thử value-fill mỗi nhóm (khôi phục template) + Playwright picker + wrap up

### Checkpoint — 2026-07-14
Vừa hoàn thành: Toàn bộ T1–T6. 10 file BE sửa (PrintTemplateVariable + 9 controller), php -l sạch, final review READY. Value-fill verify runtime: Appoint#4, Termination#56, DLC#678 đúng (khôi phục template).
Đang làm dở: (không)
Bước tiếp theo: user hard-refresh + in thử browser các loại QĐ. Follow-up tùy chọn: fix bug sẵn có TransferPersonnel::prepareContractData (export Word) nếu cần.
Blocked:

## Phase 2 — Rà soát & bổ sung ngày còn sót (2026-07-14, inline Opus)
Audit toàn bộ cột ngày mọi loại → thêm các gap (user chọn cả 4 nhóm). Đổi `formatDateVICapital`: "Ngày"→"ngày" (user yêu cầu chữ thường).
- [x] P2-1. Metadata: DECISION_COMMON +NGAY_DUYET/NGAY_TAO/NGAY_XEM_XET; LABOR_CONTRACT_MAIN +NGAY_KY/NGAY_QUYET_DINH; LABOR_CONTRACT_APPENDIX +NGAY_KY/NGAY_HIEU_LUC; EMPLOYEE_DISCIPLINE +THOI_GIAN_DINH_CHI_TU/DEN; BIEN_BAN +NGAY_DUYET/NGAY_LAP_BIEN_BAN; HOP_DONG_DAO_TAO +NGAY_LAP_HD_DAO_TAO (tất cả is_date)
- [x] P2-2. Value-fill: DecisionService (NGAY_DUYET=approved_at/NGAY_TAO=created_at/NGAY_XEM_XET=reviewed_at); DecisionLaborContract 2 khối (NGAY_KY/NGAY_QUYET_DINH từ decision); Appendix (NGAY_KY=signing_date/NGAY_HIEU_LUC=effective_date); EmployeeDiscipline (DINH_CHI_TU/DEN=suspension_date_from/to); TroubleShooting (NGAY_DUYET=approved_at/NGAY_LAP_BIEN_BAN=created_at); TrainingContract (NGAY_LAP_HD_DAO_TAO=created_at)
- [x] P2-3. Verify: php -l 8 file sạch; picker OK toàn bộ biến mới; runtime print() Phụ lục#411 (NGAY_KY/NGAY_HIEU_LUC) + QĐ ký HĐLĐ#678 (NGAY_KY/NGAY_QUYET_DINH) + DecisionService#689 (NGAY_DUYET/TAO/XEM_XET) đúng, khôi phục template. BỎ tăng thâm niên (last_seniority_date ý nghĩa không rõ). Discipline suspension chưa có data (null-safe).

### Checkpoint — 2026-07-14 (Phase 2)
Vừa hoàn thành: bổ sung ngày còn sót + đổi "ngày" thường. File sửa Phase 2: PrintTemplateVariable, Helper (ngày thường), DecisionService, DecisionLaborContract, Appendix, EmployeeDiscipline, TroubleShooting, TrainingContract.
Bước tiếp theo: user hard-refresh + in thử.
Blocked:
