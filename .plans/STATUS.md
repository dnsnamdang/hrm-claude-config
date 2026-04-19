# STATUS.md

## Đang làm
- close-prospective-projects → @dnsnamdang → .plans/close-prospective-projects/plan.md
  Trạng thái: Code DONE 16/18 (2026-04-19). BE hoàn chỉnh (migration close_* fields + 5 status constants + `closeProject` service + notify helpers + FormRequest + Controller + Route + Transformer + entity relationships). FE hoàn chỉnh (CloseProjectModal component + manager.vue integrate button + banner đỏ post-close + ẩn action buttons khi đóng). Endpoint: `POST /api/v1/assign/prospective-projects/{id}/close`.
  Cascade: Project.status=11 + Solution.status=2 + SolutionModule.status=10 + PricingRequest.status=5 + Quotation.status=5. `quotation_histories` log `closed_by_project` với meta. Notify: creator solution + PM + NLG + TP/BGĐ pending.
  Checkpoint: 2026-04-19 — Code DONE. Task 17 (readonly polish trên quotation/solution edit) skip optional (BE đã validate save). Task 18 manual test user thực hiện: button "Đóng dự án" hiện cho creator + modal load reason + submit → toast + banner + cascade DB + notify table.

## Tạm dừng

- Bomlist-Quotation → @dnsnamdang → .plans/Bomlist-Quotation/plan-phase12.md
  Trạng thái: Phase 12 code DONE 58/64. Toàn bộ BE + FE xong: VAT management (migrations + service computeTotals/recomputeTotals/applyBulkVat + 6 transition hook + controller + FormRequest + route + transformers + Excel gate + store/quotation.js + 2 component VatBulkApplyToolbar/VatFirstEntryPromptModal + edit.vue 3 cột VAT + toolbar + soft-prompt + row TỔNG + roll-up CHA + show/list/tab + ColumnCustomization); customer info (edit.vue thêm MST/Người liên hệ/SĐT liên hệ + show rename label + CustomerInfoSection required + project add/edit validate customer_contact_id); profit margin threshold (migration general_regulations.profit_margin_threshold + entity/controller/service + settings col-3 panel + nuxtClientInit commit vuex + marginColorClass 2 tier đỏ/xanh bỏ tier vàng).
  Checkpoint: 2026-04-19 — Wrap up. Còn lại 6 task manual test (Task 48-53) + test Batch 10-11 do user thực hiện. Docs PDF tại `docs/srs/bao-gia-flow.pdf`.

- training-elearning → @dnsnamdang → .plans/training-elearning/plan.md
  Trạng thái: Phase 0 done (3/3 task khảo sát BE + FE + deep dive). docs/training.md ~580 dòng / 13 sections. design.md đã enhance với gap analysis P1/P2/P3 + convention bắt buộc + risk note.
  Checkpoint: 2026-04-18 — Wrap up Phase 0. Chờ user gửi spec chung + spec từng màn + file demo HTML/Vue → tạo .plans/training-elearning-<feature>/ riêng cho mỗi màn → brainstorm + lên task BE+FE → code.

- notify-task-report → @dnsnamdang → .plans/notify-task-report/plan.md
  Trạng thái: 37/37 task done. Phase 12 + 13 vừa hoàn thành (bỏ cấu hình giờ + giảm spam + an toàn cron).
  Checkpoint: 2026-04-17 — Phase 13 done. 4 mốc gửi cố định 08:30/11:30/14:30/17:30, withoutOverlapping, fix N+1, deploy code trước rồi migrate sau. Chờ user deploy + test.

## Hoàn thành

- fix-handover → @dnsnamdang → .plans/fix-handover/plan.md
  Hoàn thành: 2026-04-18. 7/7 task. V2: fix sai message khi 2 tab cùng chọn 1 task (BE 422→423 + lookup task.code). V3: reject sau TP duyệt → chuyển task về TP + notify TP + log tên TP. Test OK.
- solution-save-and-approve → @manhcuong → .plans/solution-save-and-approve/plan.md
  Hoàn thành: 2026-04-07. 2/2 task. Button "Lưu và duyệt" khi has_modules=false
- solution-version-report → @manhcuong → .plans/solution-version-report/plan.md
  Hoàn thành: 2026-04-07. 15/15 task + 53 test cases. Báo cáo QLDA_BC_10 theo version
