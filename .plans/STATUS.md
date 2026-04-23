# STATUS.md

## Đang làm
- Bomlist-Quotation → @dnsnamdang → .plans/Bomlist-Quotation/plan-phase13.md
  Trạng thái: Phase 13 (Email khách hàng) code DONE 14/16. Phase 12 vẫn DONE 58/64. Branch `tpe-develop-assign`.
  Phase 13 làm: migration `quotations.customer_email` + snapshot trong QuotationService + expose trong DetailQuotationResource + rule required|email|max:255 trong ProspectiveProjectRequest + CustomerInfoSection input Email + validate FE trong add/edit project + display trong quotation edit/show (Email cùng row Địa chỉ theo yêu cầu user). Manager.vue + _id/index.vue inherit qua CustomerInfoSection (không sửa trực tiếp).
  Session artifacts: (1) `docs/srs/bomlist-to-quotation-srs.html + .pdf` — SRS E2E với sơ đồ UC + Swimlane SVG; (2) `docs/srs/bomlist-to-quotation-testcases.xlsx` — 140 UI test cases / 12 sheets.
  Checkpoint: 2026-04-20 — Wrap up. Còn 8 task manual test user thực hiện (Phase 12 Task 48-53 + Phase 13 Task 15-16). Pending test theo testcases.xlsx filter Priority=High.


## Tạm dừng

- close-prospective-projects → @dnsnamdang → .plans/close-prospective-projects/plan.md
  Trạng thái: Code DONE 16/18 (2026-04-19). BE hoàn chỉnh (migration close_* fields + 5 status constants + `closeProject` service + notify helpers + FormRequest + Controller + Route + Transformer + entity relationships). FE hoàn chỉnh (CloseProjectModal component + manager.vue integrate button + banner đỏ post-close + ẩn action buttons khi đóng). Endpoint: `POST /api/v1/assign/prospective-projects/{id}/close`.
  Cascade: Project.status=11 + Solution.status=2 + SolutionModule.status=10 + PricingRequest.status=5 + Quotation.status=5. `quotation_histories` log `closed_by_project` với meta. Notify: creator solution + PM + NLG + TP/BGĐ pending.
  Checkpoint: 2026-04-19 — Code DONE. Task 17 (readonly polish trên quotation/solution edit) skip optional (BE đã validate save). Task 18 manual test user thực hiện: button "Đóng dự án" hiện cho creator + modal load reason + submit → toast + banner + cascade DB + notify table.

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
- question-form-industry-level → @manhcuong → .plans/question-form-industry-level/plan.md
  Hoàn thành: 2026-04-18. 8/8 Phase. Đổi cấp gán Câu hỏi & Mẫu phiếu thu thập từ Ứng dụng → Nhóm giải pháp, ràng buộc 1 nhóm giải pháp - 1 phiếu Published. 2 migration chạy sạch, BE 12 file + FE 16 file, 14 service test pass
- application-export-split-columns → @manhcuong → .plans/application-export-split-columns/plan.md
  Hoàn thành: 2026-04-17. Tách Excel xuất Ứng dụng từ 7 cột (gộp) → 12 cột riêng biệt. Chỉ sửa 1 file blade
- daily-report-testcase → @manhcuong → .plans/daily-report-testcase/plan.md
  Hoàn thành: 2026-04-15. 40 test case UI theo góc nhìn người dùng cho màn Nhập kết quả báo cáo tiến độ hàng ngày
- assignee-reject-start → @manhcuong → .plans/assignee-reject-start/plan.md
  Hoàn thành: 2026-04-10. 9/9 task + 13 manual test case. Assignee từ chối triển khai khi task chưa có kết quả (BE only, FE không đổi)
- category-multi-select → @manhcuong → .plans/category-multi-select/plan.md
  Hoàn thành: 2026-04-10. 56/56 task. Đổi 4 FK đơn trong Nhóm giải pháp & Ứng dụng sang multi-select qua 4 pivot. Bao gồm Phase 10 hot-fix downstream (7 file: Scope/CustomerScope relations, ProspectiveProject auto-fill, SurveyQuestions Resource, SolutionsWorkSummary report, optionsSelect store, FormMeta cascade)
- report-testcases → @manhcuong → .plans/report-testcases/plan.md
  Hoàn thành: 2026-04-09. 149 test cases cho 8 báo cáo module Assign
- solution-module-version-tracking → @manhcuong → .plans/solution-module-version-tracking/plan.md
  Hoàn thành: 2026-04-08. 6/6 task. Theo dõi chỉ số hoàn thành giải pháp theo version
- task-manager-by-employees → @junfoke → .plans/task-manager-by-employees/plan.md
  Hoàn thành: 2026-04-08. 9/9 task. Báo cáo phân bổ nguồn lực dạng Gantt theo NV (QLDA_BC_V2_11)
- solution-add-module-deploying → @manhcuong → .plans/solution-add-module-deploying/plan.md
  Hoàn thành: 2026-04-07. 3/3 task. PM thêm hạng mục khi đang triển khai + auto-approve