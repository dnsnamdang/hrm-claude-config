# SDD Progress Ledger — decision-date-format-variants

BASE branch: hrm-api @ tpe-develop-assign (có WIP khác — diff theo từng file của task)
Plan: docs/superpowers/plans/2026-07-14-decision-date-format-variants.md

## Trạng thái task
- [x] T1 Helper — DONE, review sạch (spec ✅ + quality Approved)
- [x] T2 Metadata picker — DONE (42 cờ đúng), review spec ✅ + Approved. MINOR (final-review triage): expandDateVariables sinh item ngày chỉ có name+description, mất template_type_id/group/type — không ảnh hưởng hiện tại (type=null, group đã gom trước).
- [x] T3 DecisionService common — DONE, controller tự soi diff sạch (so/chu/chu đúng)
- [x] T4 Controller "chu" — DONE (Appoint, Transfer 2 khối, Retirement, IncreaseSeniority so/chu), diff sạch
- [x] T5 Controller inline "so" — DONE (Accept, Renew, Suspend 2 khối, Termination 174=chu/187=so), diff sạch; null date giờ để trống thay vì in hôm nay (fix nhẹ, tốt)
- [x] T6 Discipline + DecisionRegulationSalary — DONE, subagent review spec ✅ + Approved. MINOR (final-review): nhánh else NGAY_SA_THAI (dismissal_date null) chỉ set base='', thiếu _SO/_CHU — clearNull() xoá placeholder rớt nên không lộ template.
- [x] T7 HĐLĐ (DecisionLaborContract 2 khối $result/$data + Appendix) — DONE, subagent review spec ✅ + Approved. Minor: ngày null giờ trả null thay '' (render rỗng, đồng nhất T5).
- [x] T8 HĐ đào tạo + Biên bản — DONE, diff sạch. FIX kèm (user duyệt): đổi value-fill NGAY_KY_HDLĐ→NGAY_KY_HĐLĐ khớp metadata picker (bug lệch key có sẵn) — biến này giờ mới đổ được giá trị + có _CHU/_SO.
- [x] T9 Verify end-to-end — 17/17 file php -l sạch; picker OK 6 loại mẫu (variants có, bare ẩn, non-date giữ); value-fill Decision#689 đúng (bare giữ format cũ, _CHU/_SO đúng). Playwright browser để user tự xác nhận.

## Log
- T1–T8 review từng task sạch (spec ✅). Chi tiết Minor ở từng dòng task trên.
- FINAL whole-branch review (Opus): tìm 1 IMPORTANT — RegulationGeneralController::print (mẫu Quy chế chung, loại QĐ, subfolder V1/Regulations/) bị SÓT khỏi inventory ban đầu → NGAY_QUYET_DINH ẩn khỏi picker nhưng chỉ set bare → regression. ĐÃ FIX: thêm use Helper + đổi dòng 165 sang fillDateVariants('so'). Verify data thật: gốc=07/07/2026, _CHU=Ngày 07 tháng 07 năm 2026, _SO=07/07/2026.
- Rà bổ sung toàn cây controller Decision (gồm subfolder): không còn site ngày cờ nào bare-only ngoài 4 site 'keep' cố ý ở DecisionLaborContract; composite đủ _CHU/_SO.
- MINOR còn lại (không chặn, chấp nhận): (a) NGAY_KY/NGAY_HIEU_LUC ở 2 controller Quy chế không được fill — pre-existing (2 controller này không gọi setValuePrintDecision), không phải regression feature; (b) nhánh else NGAY_SA_THAI/NGAY_KY_HĐLĐ chỉ set base='' thiếu _SO/_CHU — clearNull() xoá placeholder rớt nên không lộ; (c) expandDateVariables rớt key template_type_id/group/type ở item ngày — vô hại (type=null).
- KẾT LUẬN: READY. 18 file sửa, php -l sạch toàn bộ, picker + value-fill verify OK.
