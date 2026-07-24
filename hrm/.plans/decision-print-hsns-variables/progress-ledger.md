# SDD Progress Ledger — decision-print-hsns-variables

Repo: hrm-api @ tpe-develop-assign (có WIP khác — diff theo file của task)
Plan: docs/superpowers/plans/2026-07-14-decision-print-hsns-variables.md

## Trạng thái
- [x] T1 Metadata — DONE (90 dòng, 15 is_date), subagent review spec ✅ + Approved
- [x] T2 Appoint/Transfer/SalaryChange value-fill — DONE, diff sạch (13 HSNS + 2 CAP_BAC/file, $info=instance sẵn có). Note: prepareContractData/exportWord (Transfer) CHƯA có bộ biến mới (ngoài scope print()); runtime verify ở T6.
- [x] T3 Retirement/Discipline value-fill — DONE, diff sạch (13 HSNS, $info đúng quan hệ)
- [x] T4 Termination/Suspend value-fill — DONE, subagent review spec ✅ + Approved (Suspend 2 khối, THOI_GIAN_HDLD_HIEN_TAI×3, quan hệ/cột verify runtime, null-safe)
- [x] T5 DecisionLaborContract/Appendix — DONE, diff sạch (DLC 2 khối $result/$data, Appendix optional($decisionContract))
- [x] T6 Verify — 10/10 php -l sạch; value-fill runtime OK Appoint#4 (13 HSNS+CAP_BAC+NGAY_SINH 2fmt) / Termination#56 (9 biến+THOI_GIAN_HDLD từ HĐLĐ#307) / DLC#678. Suspend chưa có data (code reviewed). Final whole-branch review: READY TO MERGE.

## Log
- T1 metadata review spec ✅+Approved (90 dòng, 15 is_date). T2/T3/T5 controller tự soi diff sạch. T4 subagent review ✅+Approved.
- FINAL whole-branch review (Opus): READY TO MERGE. Khớp metadata↔value-fill 1-1 mọi nhóm, không biến chết/mồ côi; field nguồn đúng; $result/$data đúng; THOI_GIAN_HDLD_HIEN_TAI đúng 3 lần; loại gộp bỏ qua đúng.
- FOLLOW-UP ngoài scope (không block): (1) TransferPersonnel exportWord/prepareContractData có BUG SẴN CÓ (build $result nhưng return $data) → export Word Transfer vốn hỏng từ trước + chưa có biến mới; spec chốt chỉ làm print(). (2) Termination NOI_CU_TRU (cũ) = full_address_residence trùng DIA_CHI_THUONG_TRU — bất nhất sẵn có, không đụng biến cũ.
- KẾT LUẬN: 10 file sửa (PrintTemplateVariable + 9 controller), php -l sạch, value-fill verify 3 nhóm. Không git/migration/permission.
