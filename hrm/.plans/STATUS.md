# STATUS.md

## Đang làm

- copy-form-template → @khoipv → .plans/copy-form-template/plan.md
  Trạng thái: CODE DONE (2026-06-05). BE 3 file (service + controller + route) + FE 2 file (index.vue + add.vue). php -l PASS, tinker verify logic lọc OK. Chờ user verify browser 5 kịch bản. KHÔNG migration, KHÔNG sửa transformer dùng chung.
  Spec: docs/superpowers/specs/2026-06-05-copy-form-template-design.md | Design: .plans/copy-form-template/design.md
  Scope: Thêm nút "Sao chép" ở list assign/form-templates → vào form Tạo mới đã prefill từ mẫu gốc (Hướng A). Tên + Nhóm ngành (scope_id) giữ nguyên; Nhóm giải pháp (industry_id) để trống (chọn lại); status=Nháp; Section sao chép 100% giữ position. Câu hỏi application_scope=1 (Tất cả)→CLONE, =2 (Theo nhóm giải pháp)→BỎ QUA (tra qua survey_question_id→SurveyQuestion). BE: +1 route copy-data + controller method + service prepareCopyData + CopyFormTemplatesResource. FE: +action copy (index.vue) + nhánh prefill ?copyFrom (add.vue). Dùng chung quyền "Quản lý danh mục mẫu phiếu thu thập thông tin", không migration, không sửa transformer dùng chung.

- elearning-home-need-to-learn → @khoipv → .plans/elearning-home-need-to-learn/plan.md
  Trạng thái: CODE DONE (2026-06-04). Phase 1 BE + Phase 2 FE xong, lint + test runtime endpoint qua tinker PASS. Chờ user verify browser (Phase 3).
  Spec: .plans/elearning-home-need-to-learn/design.md
  Scope: Section "Bạn cần học" trang chủ elearning (3001) lấy data thật (khóa học + lộ trình, trộn, tối đa 4, mới nhất trước). Khách=public, nhân viên HRM=đang dùng. BE 1 endpoint mới (public/home-content + optional auth, tái dùng SubjectBrowseResource + LearningPathBrowseResource) + FE 3 file (stores/elearning.js + HomeView.vue + LearnCard.vue mở rộng type='path'). Cùng quy tắc visibility với elearning-learning-path-visibility.
  Checkpoint: 2026-06-04 — Data thực: guest=0 khóa public+2 lộ trình public; employee=27 khóa+5 lộ trình (top 4). Phase 4: fix bug thời lượng — 2 resource dùng chung (SubjectBrowseResource + LearningPathBrowseResource) trước cộng ceil(duration/60) từng bài → phồng (NPK 30s→3 phút); sửa cộng tổng giây rồi mới quy đổi + thêm field duration_seconds, card dùng formatLessonDuration (mm:ss) khớp trang chi tiết. Ảnh hưởng cả màn list /lo-trinh-hoc-tap, /khoa-hoc (số liệu chính xác hơn). Bước tiếp: user chạy elearning verify khách vs SSO HRM + thời lượng card + click card điều hướng.

- skills-v2-redesign → @khoipv → .plans/skills-v2-redesign/plan.md
  Trạng thái: CODE DONE (2026-06-03, 2 file FE). Chờ user verify browser (Task 3).
  Spec: docs/superpowers/specs/2026-06-03-skills-v2-redesign-design.md | Plan: docs/superpowers/plans/2026-06-03-skills-v2-redesign.md
  Scope: CHỈ FE hrm-client. Đổi giao diện màn training/skills cho giống learning-path (V2BaseFilterPanel + V2BaseDataTable + BaseConfirmModal), gộp cột, toggle khóa inline. Giữ modal thêm/sửa (restyle V2 + validate inline), giữ Excel/In/Lịch sử/Khóa. Không đổi BE/API/permission. Giữ tham số & shape response API cũ.
  Checkpoint: 2026-06-03 — Rewrite index.vue + add_skill_modal.vue xong, review prop/slot V2 đạt (không lỗi runtime). Bước tiếp: user chạy npm run dev + duyệt browser theo Task 3.
- elearning-completion-criteria → @junfoke → .plans/elearning-completion-criteria/plan.md
  Trạng thái: CODE DONE Hướng A + SCORM viewed (+min giây mở) + Hướng B (2026-06-04). Chờ user rebuild + verify browser. KHÔNG migration.
  Spec: docs/superpowers/specs/2026-06-04-elearning-completion-criteria-enforcement-design.md
  Scope: Khớp form cấu hình tiêu chí hoàn thành với enforcement thật. (A) Form tạo bài text/file thêm "Min thời gian đọc (giây)" (trường BE thực dùng), gắn nhãn "(chưa áp dụng)" cho field % + các tiêu chí scroll/dwell/seek/active-tab/allow-download chưa enforce (giữ, vẫn nhập được). (B) SCORM thêm option viewed (mở là xong, cho gói content single-page; đã bỏ browsed sau test vì browse-mode gần như không xảy ra) + sửa completionHint màn học cho viewed. 6 file, KHÔNG migration. Hướng B (implement scroll/dwell/seek-block...) để sau. Tiếp nối elearning-tracking-fix + scorm-lms-runtime.

- elearning-sequential-lock → @junfoke → .plans/elearning-sequential-lock/plan.md
  Trạng thái: CODE DONE (2026-06-03). Chờ verify browser trong Docker (Node ≥18).
  Scope: Fix khoá bài học khi vào học. (1) Khoá "Học tuần tự" (subjects.linear_required) không enforce → tạo LessonLockResolver (nguồn chân lý chung BE), transformer + service dùng chung. (2) Prerequisite ALL/ANY trên từng bài (đã có sẵn, dọn về resolver). (3) Defense-in-depth: chặn heartbeat/scorm-commit bài đang khoá (423). (4) FE: disable click bài khoá + disable nút Trước/Sau (hasPrev/hasNext) + sửa badge tiền ĐK. (5) Fix bài kế không mở khi hoàn thành (phải F5) → recomputeLocks() client mirror resolver, gọi trong handleHeartbeatResponse. Tiếp nối learning-session-api + elearning-tracking-fix.

- elearning-learning-path-seamless → @junfoke → .plans/elearning-learning-path-seamless/plan.md
  Trạng thái: CODE DONE (2026-06-03, 13/13 task / 6 phase, subagent-driven). BE 5 file + FE 8 file. Không migration. Chờ user verify browser (Docker Node ≥18) 8 kịch bản.
  Spec: docs/superpowers/specs/2026-06-03-elearning-learning-path-seamless-design.md
  Plan: docs/superpowers/plans/2026-06-03-elearning-learning-path-seamless.md
  Scope: Học liền mạch lộ trình — context ?lp trong màn học, Quay lại về lộ trình, resume xuyên khoá, lock cấp khoá (linear_required), modal 3 biến thể (khoá tiếp theo / hoàn thành lộ trình / khoá lẻ), chứng chỉ lộ trình (mirror cert khoá, không migration). Tiếp nối elearning-learning-path-detail (đã fix Phase 10: trạng thái bài + % trung bình khoá + nút Vào học/Tiếp tục học).

- elearning-course-completion → @junfoke → .plans/elearning-course-completion/plan.md
  Trạng thái: CODE DONE (13/13 task, 4 phase — 2026-06-03). Chờ verify browser trong Docker (Node ≥18).
  Spec: docs/superpowers/specs/2026-06-03-elearning-course-completion-design.md
  Plan: docs/superpowers/plans/2026-06-03-elearning-course-completion.md
  Checkpoint: 2026-06-03 — Implement xong qua subagent-driven. BE 4 file (CertificateService + CertificateController + route /subjects/{slug}/certificate + certificate_enabled vào LearningSessionResource). FE 9 file: store certificate.js, CertificateView+CertificateCanvas+route /certificate/:slug+print CSS, courseCompletionSignal trong learningSession, CourseCompleteModal tích hợp SubjectLearnView, map certificateEnabled (subjectDetail), DetailEnrollCard đổi "Chứng nhận"→"Chứng chỉ"+nút "Xem lại nội dung", ContentDetailView nối router, nút "Chứng chỉ" sidebar màn học. Phương án A (endpoint riêng), chứng chỉ render web in qua window.print. Bước tiếp: user chạy dev server Docker → verify 4 kịch bản (100%→modal; có cert→in được; không cert→khám phá/xem lại; vào thẳng /certificate chưa xong→403). Defer: nút cert ở My Learning, PDF/email BE, QR, cert cho LearningPath.

- project-implementation-types → @dnsnamdang → .plans/project-implementation-types/plan.md
  Trạng thái: Phase A+B done. Phase C đã pivot sang quotation-redesign. Branch `tpe-develop-assign`.
  Checkpoint: 2026-05-27 — Phase C scope mở rộng → tách thành feature riêng quotation-redesign.

- quotation-redesign → @dnsnamdang → .plans/quotation-redesign/plan.md
  Trạng thái: Brainstorm DONE, spec DONE. Chờ user review spec → lên plan.
  Spec: docs/superpowers/specs/2026-05-27-quotation-redesign-design.md
  Checkpoint: 2026-05-27 — Spec đầy đủ: DB migration + BE refactor + FE tách component. Branch `tpe-develop-assign`. Bước tiếp: user review spec → writing-plans.

- solution-manager-assignment → @dnsnamdang → .plans/solution-manager-assignment/plan.md
  Trạng thái: Code DONE. Phân công PM/Leader + lịch sử + notification + confirm. SRS + Testcase đã tạo.
  Checkpoint: 2026-05-17 — Phase 1+2 done. BE 7 file, FE 3 file. 28 test cases. Bước tiếp: deploy.
- elearning-tracking-fix → @junfoke → .plans/elearning-tracking-fix/plan.md
  Trạng thái: CODE DONE (2026-06-02, ~12 file: 1 BE + FE). Chờ verify browser trong Docker (Node ≥18). Scope: (1) hiển thị thời gian 3:12, (2) completionHint theo config, (3) video tracking thật IFrame Player API (free), (4) tối ưu heartbeat (keepalive + dừng khi done), (5) fix status chậm (optimistic learning) + toast bắn nhầm khi quay lại bài đã xong (dùng just_completed), (6) toàn vẹn tracking: chống tua video (SEEK_THRESHOLD, cho 2x) + rời tab khi đọc tài liệu (useReadingTracker + ReadingGateOverlay "Tiếp tục học"). Tiếp nối learning-session-api + elearning-lesson-viewer. Defer: idle-trong-tab, enforce scroll/dwell, Redis/queue (chỉ khi scale nghìn).

- scorm-preview-runtime → @junfoke → .plans/scorm-preview-runtime/plan.md
  Trạng thái: CODE DONE (2026-06-01). Chờ user restart dev server + verify trên browser (upload gói SCORM → preview hết lỗi objective).
  Spec: docs/superpowers/specs/2026-06-01-scorm-preview-runtime-design.md
  Scope: CHỈ FE hrm-client. Port runtime SCORM (scorm-again + proxy same-origin) sang panel preview màn quản lý bài học (LessonForm.vue type=4) để hết lỗi "could not find objective". Rút gọn: KHÔNG tracking/resume/commit BE. Proxy bằng Nuxt serverMiddleware. Tiếp nối scorm-lms-runtime (elearning) + scorm-upload.

- scorm-lms-runtime → @junfoke → .plans/scorm-lms-runtime/plan.md
  Trạng thái: DONE — chạy đúng end-to-end trên browser (completion + resume + popup). Chờ note OPS cấu hình nginx prod + merge.
  Spec: docs/superpowers/specs/2026-05-30-scorm-lms-runtime-design.md (mục 11 = các fix khi debug) | Plan: docs/superpowers/plans/2026-05-30-scorm-lms-runtime.md
  Scope: Học bài SCORM (type=4) trên elearning. Reverse-proxy S3 same-origin (window.parent.API) + scorm-again v3 (1.2+2004) + ScormPlayer.vue + endpoint scorm-commit + 9 cột scorm_* (resume + completion theo cấu hình bài). Tiếp nối scorm-upload.
  Checkpoint: 2026-05-30 — Verify PASS với gói Run-Time SCORM 2004 (scorm.com): "Đã xong" + resume. Fix phát sinh: host tanphat.s3, :key chống kẹt bài, proxy inject window.confirm=()=>true + no-store chặn 2 native confirm, popup resume riêng. OPS: nginx /scorm-proxy + sub_filter inject + no-store (spec mục 2&11). elearning cần Node ≥18; scorm-again cài trong container.

- customer-scope-group → @manhcuong → .plans/customer-scope-group/plan.md
  Trạng thái: CODE DONE (Phase 1-7). Chờ chạy migration + test browser (Phase 8).
  Spec: docs/superpowers/specs/2026-05-28-customer-scope-group-design.md
  Scope: Chèn tầng trung gian "Nhóm lĩnh vực khách hàng" giữa Lĩnh vực ⟷ Ứng dụng (bỏ pivot trực tiếp application_customer_scopes). Màn Nhóm full CRUD + import/export + 2 permission (id 1093/1094). Sửa Ứng dụng (Lĩnh vực→Nhóm), Lĩnh vực (Số ứng dụng→Số nhóm), Dự án tiềm năng (thêm customer_scope_group_id, cascade Ứng dụng→Nhóm→Lĩnh vực, 2 luồng chọn). Downstream MeetingProject resolve qua nhóm. Migrate dữ liệu cũ.
  Checkpoint: 2026-05-29 — ĐỔI MÔ HÌNH (Phase 10): Nhóm LVKH giờ là CHA của Lĩnh vực (1-n), Lĩnh vực bắt buộc chọn Nhóm cha; Ứng dụng↔Lĩnh vực giữ n-n. Migration 2026_05_29_000001 đã chạy (thêm customer_scopes.customer_scope_group_id, khôi phục application_customer_scopes, drop 2 pivot n-n). BE+FE đã revert/sửa toàn bộ (R1-R7). Verify: Eloquent + API getAll + FE compile 200. Còn lại: click-through UI thủ công + file mẫu import Lĩnh vực cần thêm cột GroupCode.

- learning-session-api → @junfoke → .plans/learning-session-api/plan.md
  Trạng thái: Code DONE (13/13 task). Chờ chạy migration + test API thật trên browser.
  Spec: docs/superpowers/specs/2026-05-28-learning-session-api-design.md
  Scope: BE (migration enrollment_lesson_progress + entity + service + controller + routes) + FE (sửa store + viewers + bỏ nút Hoàn thành). Heartbeat 30s + auto-mark done + comment bài học.

- elearning-lesson-viewer → @junfoke → .plans/elearning-lesson-viewer/plan.md
  Trạng thái: Code DONE (14/14 task). Browser test passed. Chờ kết nối API thật (→ learning-session-api).
  Spec: docs/superpowers/specs/2026-05-28-elearning-lesson-viewer-design.md
  Scope: FE elearning — màn học đầy đủ (viewer YouTube+PDF+HTML, sidebar outline, tracking giả lập, prerequisite, focus mode, tabs, mock data). SCORM mở rộng sau.

- external-user-list → @junfoke → .plans/external-user-list/plan.md
  Trạng thái: Brainstorming DONE, spec viết xong. Chờ user review spec → lên plan → implement.
  Spec: docs/superpowers/specs/2026-05-25-external-user-list-design.md
  Scope: Migration (4 field mới elearning_learners) + BE Training (controller + route + export) + FE hrm-client (index.vue list page)

- subject-enrollment → @junfoke → .plans/subject-enrollment/plan.md
  Trạng thái: Spec done, chờ duyệt → lên plan → implement.
  Spec: docs/superpowers/specs/2026-05-21-subject-enrollment-design.md
  Scope: BE (migration + model + service + controller + route) + FE (store + composable + placeholder page + button update)

- elearning-learning-path-detail → @junfoke → .plans/elearning-learning-path-detail/plan.md
  Trạng thái: Code DONE (70 task, 11 phases). Đã migrate. Chờ verify browser (Docker, Node ≥18).
  Spec: docs/superpowers/specs/2026-05-19-elearning-learning-path-detail-design.md
  Checkpoint: 2026-06-03 (6) — Phase 11: hiển thị cấp Chương (learner PathOutline + builder TabInfo, BE trả chapters[]/loose_lessons + chapter_id), quy đổi giờ-phút toàn bộ (helper formatMinutes), badge tổng "X khoá/chương • Y bài • giờ-phút" + gộp nút "Mở tất cả", fix trạng thái bài/chương màn chi tiết môn (BE đính learn_status từ EnrollmentLessonProgress + FE deriveChapterStatus), placeholder overview "Chưa có thông tin". Bước tiếp: verify browser 4 điểm (chương→bài+thời lượng, builder hiện chương, bài xong hiện "Đã xong"/chương "Đạt", overview rỗng placeholder). Defer: status chương exam chưa tính kết quả thi.

- Bomlist-Quotation → @dnsnamdang → .plans/Bomlist-Quotation/plan.md
  Trạng thái: Phase 30 CODE DONE. Branch `tpe-develop-assign`.
  Phase 30 (2026-05-28): BOM ẩn giá ERP, báo giá load giá ERP + quy đổi tỷ giá, validity_date, tab báo giá dự án TKT, icon cảnh báo thay đổi giá, toolbar CK+TSLN màn xem.
  Checkpoint: 2026-05-28 — Phase 30 done. Bước tiếp: chạy migration validity_date + test thủ công.

- firm-order-contact-select → @nguyentrancu97 → .plans/firm-order-contact-select/plan.md
  Trạng thái: Implementing. Select người liên hệ cho đơn hàng nguyên tắc thay vì copy từ HĐNT (TanPhatDev)
- delivery-trip-actual-cost-validate → @nguyentrancu97 → .plans/delivery-trip-actual-cost-validate/plan.md
  Trạng thái: Implementing. Validate total_cost_transition theo CP xăng + cầu đường + công tác phí + CP khác (TanPhatDev)
- delivery-trip-accounting-cost-validate → @nguyentrancu97 → .plans/delivery-trip-accounting-cost-validate/plan.md
  Trạng thái: Implementing. Áp dụng logic validate cước cho phiếu hạch toán + enable edit header + tick is_company_sp (TanPhatDev)
- xuat-ghep-tu-hang-giu → @nguyentrancu97 → .plans/xuat-ghep-tu-hang-giu/plan.md
  Trạng thái: Brainstorming PAUSED 2026-04-28. Đã chốt 7 quyết định (hiển thị tồn/giữ qua API stockOfProducts, validate `qty ≤ in_stock + prepick_qty`, cascade nhập ghép giữ toàn bộ thành phẩm, customer per-parent, hạn giữ = today + Config.max_prepick_date, xuất thẳng tái sử dụng pattern export_prepick_qty/hold_qty/total_qty + FIFO consume). Còn 6 câu hỏi mở (Q6-Q11): customer_id cấp nào, validate hạn giữ, approval, pending lock prepick, popup filter, edit/cancel. (TanPhatDev)
  Checkpoint: 2026-04-28 — Paused tại Q6 (customer_id lưu cấp parent vs recipe + cascade khi YCXG có >1 customer).

## Tạm dừng

- training-elearning → @dnsnamdang → .plans/training-elearning/plan.md
  Trạng thái: Phase 0 done (3/3 task khảo sát BE + FE + deep dive). docs/training.md ~580 dòng / 13 sections. design.md đã enhance với gap analysis P1/P2/P3 + convention bắt buộc + risk note.
  Checkpoint: 2026-04-18 — Wrap up Phase 0. Chờ user gửi spec chung + spec từng màn + file demo HTML/Vue → tạo .plans/training-elearning-<feature>/ riêng cho mỗi màn → brainstorm + lên task BE+FE → code.

- notify-task-report → @dnsnamdang → .plans/notify-task-report/plan.md
  Trạng thái: 37/37 task done. Phase 12 + 13 vừa hoàn thành (bỏ cấu hình giờ + giảm spam + an toàn cron).
  Checkpoint: 2026-04-17 — Phase 13 done. 4 mốc gửi cố định 08:30/11:30/14:30/17:30, withoutOverlapping, fix N+1, deploy code trước rồi migrate sau. Chờ user deploy + test.

## Hoàn thành

- quotation-finalize → @khoipv → .plans/quotation-finalize/plan.md
  Hoàn thành: 2026-06-04. 8 task (6 BE + 2 FE), verify browser PASS. Tab "Báo giá" màn assign/prospective-projects/{id}/manager: nút Chốt báo giá (Đã duyệt 4 → Trúng thầu 7) + Hủy chốt (7 → 4, bắt buộc lý do). Mỗi dự án 1 báo giá trúng thầu (BE chặn + báo lỗi nếu đã có). Nút chỉ hiện khi đúng trạng thái + isSaleOfProject. BE: +status 7, +2 history action, +finalize/unfinalize service, +2 route (không middleware/permission/migration — chỉ ghi history): Quotation.php, QuotationHistory.php, QuotationUnfinalizeRequest.php (mới), QuotationService.php, QuotationController.php, Routes/api.php. FE: ProspectiveProjectQuotationsTab.vue (2 icon-button + modal lý do hủy chốt validate inline). Spec: .plans/quotation-finalize/design.md

- termination-filter-include-resigned → @khoipv → .plans/termination-filter-include-resigned/plan.md
  Hoàn thành: 2026-06-02. Dropdown "Nhân viên" màn decision/termination-labor-contract/index hiển thị cả người đã nghỉ việc (Hướng A: endpoint riêng `GET decision/termination-labor-contract/employee-options` trả toàn bộ employee_infos bất kể status; FE bind vào data local `employeeFilterOptions` thay vì state global). BE 2 file (controller method + route) + FE 1 file (index.vue). Không đụng state global lẫn hàm dùng chung. Spec: .plans/termination-filter-include-resigned/design.md

- print-template-delete → @khoipv → .plans/print-template-delete/plan.md
  Hoàn thành: 2026-06-02. Xóa mềm mẫu in màn decision/category/print_templates (cột status, xóa = set status 0, list lọc status=1). Nút Xóa chỉ hiện khi can_delete=true; chặn xóa nếu mẫu đang dùng ở 9 bảng FK (decisions, department_establishments, department_dissolutions, trouble_shooting_reports, decision_labor_contracts, appendix_labor_contracts, training_contracts, self_notifications, suspend_labor_contracts.print_template_agreement_id) HOẶC code ∈ PrintTemplate::PROTECTED_CODES (BIEN_BAN_CUOC_HOP, HOP_DONG_DAO_TAO, PHU_LUC_HOP_DONG_LAO_DONG, QUYET_DINH_DIEU_CHINH_LUONG, HOP_DONG_LAO_DONG_CHINH_THUC_KHONG_THOI_HAN — mẫu hệ thống bị code hardcode tra cứu theo code). BE: migration cột status + entity PROTECTED_CODES + service getUsedTemplateIds/isPrintTemplateInUse/deletePrintTemplate (can_delete precompute theo lô tránh N+1) + controller delete($id) 4 nhánh (not_found/protected/in_use/ok) + Resource trả status+can_delete. FE: index.vue nút Xóa v-if="item.can_delete" + đọc message lỗi BE + dọn code chết, popup xác nhận tái dùng confirm-delete-selected. Branch `tpe` (đã migrate DB dev). Spec: docs/superpowers/specs/2026-06-02-print-template-delete-design.md

- employee-account-change-history → @khoipv → .plans/employee-account-change-history/plan.md
  Hoàn thành: 2026-06-02. Lịch sử thay đổi cho màn human/employee (quản lý tài khoản đăng nhập NV), mirror pattern task_history của module Assign. BE: migration bảng employee_history (employee_id, action create/update/change_status, old_value/new_value JSON, changed_by, changed_at) + entity EmployeeHistory + quan hệ Employee::history() + EmployeeService logHistory()/buildHistorySnapshot() ghi snapshot khi create/update (theo dõi email, status, rice_setting_location_id, company_ids, cờ password_changed — KHÔNG lưu giá trị mật khẩu) + endpoint GET /human/employee/{id}/histories + resource formatHistory (resolve ID→tên, enum→nhãn, format ngày). FE: nút "Lịch sử" mỗi dòng pages/human/employee/index.vue + modal timeline diff old/new. Spec: docs/superpowers/specs/2026-06-01-employee-account-change-history-design.md

- forgot-password → @manhcuong → .plans/forgot-password/plan.md
  Hoàn thành: 2026-06-01. Quên mật khẩu từ màn login. Link "Quên mật khẩu?" → màn forgot_password (email + captcha ảnh BE mews/captcha) → BE check tài khoản (TH1 tồn tại+status=1 gửi mail link reset token 30p, TH2 không/khóa báo "Không tìm thấy tài khoản") → màn reset_password (rule 7-20+4 yếu tố) → verify token (≤30p, dùng 1 lần, bảng password_resets) → đổi mật khẩu + set password_changed_at. BE: mews/captcha ^3.4, ForgotPasswordRequest/ResetPasswordRequest, AuthNewController captcha/forgotPassword/resetPassword, ResetPasswordMail + blade, 3 route public. FE: 3 store action, link login, 2 màn forgot/reset_password, whitelist authenticated.js. LƯU Ý deploy: composer install trên PHP 7.4. Spec: docs/superpowers/specs/2026-06-01-forgot-password-design.md

- force-change-password → @manhcuong → .plans/force-change-password/plan.md
  Hoàn thành: 2026-06-01. Bắt buộc đổi mật khẩu từ lần login thứ 2 nếu chưa từng đổi (chỉ tài khoản mới tạo). Chặn FE (route guard) + BE (middleware MustChangePassword). Tái dùng màn /change_password (chế độ bắt buộc + banner + nút Đóng=logout). DB: thêm login_count + password_changed_at vào employees (backfill now() cho tài khoản cũ). Rule mật khẩu mới: 7-20 ký tự, đủ 4 yếu tố, khác 123456@. Refactor updatePass sang UpdatePasswordRequest/ValidationException. Spec: docs/superpowers/specs/2026-06-01-force-change-password-design.md

- customer-scope-group → @manhcuong → .plans/customer-scope-group/plan.md
  Hoàn thành: 2026-06-01. Nhóm lĩnh vực khách hàng là CHA của Lĩnh vực (1-n), Lĩnh vực bắt buộc chọn Nhóm cha; Ứng dụng↔Lĩnh vực giữ n-n. Màn Nhóm full CRUD + import/export + 2 permission (id 1093/1094). Migration 2026_05_29_000001 (thêm customer_scopes.customer_scope_group_id, khôi phục application_customer_scopes, drop 2 pivot n-n). Downstream MeetingProject resolve qua nhóm. Spec: docs/superpowers/specs/2026-05-28-customer-scope-group-design.md

- bulk-permission → @manhcuong → .plans/bulk-permission/plan.md
  Hoàn thành: 2026-06-01. Popup "Phân quyền hàng loạt" trên /timesheet/setting/roles — cấp/thu hồi permission hàng loạt cho NV theo Khối/PB/BP/CV/CD, scope current_company, dùng V2Base. KHÔNG đụng Role. Defer lịch sử (#10455). Spec: docs/superpowers/specs/2026-05-27-bulk-permission-design.md

- request-solution-adjustment → @manhcuong → .plans/request-solution-adjustment/plan.md
  Hoàn thành: 2026-06-01. BE 8 files + FE 3 files. Fix: BaseConfirmModal @event, cột Hành động luôn hiện, cột Version, popup chi tiết dạng bảng, notification URL /manager, FileAttachmentTable readonly (disabled prop), sort id desc. Phase 8: review logic cascade khi Tiếp nhận YCĐC — gửi YCĐC không đổi trạng thái dự án TKT, tiếp nhận cascade dừng YCXD giá + Báo giá chưa duyệt. Spec: docs/superpowers/specs/2026-05-06-request-solution-adjustment-design.md | SRS: docs/srs/solution-adjustment-request-SRS.html | Testcases: docs/srs/solution-adjustment-request-testcases.xlsx

- my-todo → @dnsnamdang → .plans/my-todo/plan.md
  Hoàn thành: 2026-05-16. Phase 1-5 + 7-9 done. Nhắc việc cá nhân + lịch làm việc (cascade toggle, sub-items, confirm modal).
- fix-handover → @dnsnamdang → .plans/fix-handover/plan.md
  Hoàn thành: 2026-05-16. V6 done. Bàn giao công việc — tiếp nhận tất cả + filter cascade + submitted_at.
- close-prospective-projects → @dnsnamdang → .plans/close-prospective-projects/plan.md
  Hoàn thành: 2026-05-16. Phase 17C done. Chốt dự án tiềm năng — hồ sơ trình duyệt + đổi trạng thái YC làm GP.

- google-login → @junfoke → .plans/google-login/plan.md
  Hoàn thành: 2026-05-26. Đăng nhập Google bằng GIS (Google Identity Services). Migration (password nullable + google_id + avatar_url) + BE endpoint auth/google (verify token, tìm/tạo learner, auth_source='google') + FE composable useGoogleAuth + nút Google trên LoginView + RegisterView + avatar fallback. Spec: docs/superpowers/specs/2026-05-26-google-login-design.md

- project-implementation-types → @manhcuong → .plans/project-implementation-types/plan.md
  Hoàn thành: 2026-05-24. Bổ sung 3 phương án triển khai dự án TKT (1=Tự triển khai, 2=Theo phòng, 3=Liên phòng ban). Type=1: KD tự làm GP không qua YC, Solution skip duyệt PM/Leader, Hồ sơ TĐ auto-approve. Type=2: lock receive_dept = phòng KD phụ trách. Type=3 giữ nguyên (backward-compat). 2 migration + ~15 file BE/FE. Spec: docs/superpowers/specs/2026-05-23-project-implementation-types-design.md

- solution-module-show-closed → @manhcuong → .plans/solution-module-show-closed/plan.md
  Trạng thái: Brainstorming DONE (2026-05-22). Design + plan + spec đã viết. Đang implement BE.
  Spec: docs/superpowers/specs/2026-05-22-solution-module-show-closed-design.md
  Checkpoint: 2026-05-22 — Sửa SolutionModuleService::index() để hạng mục thuộc Solution status=Đóng vẫn hiện ra. Bước tiếp: edit dòng 121-123, user test.

- add-member-no-modules → @manhcuong → .plans/add-member-no-modules/plan.md
  Trạng thái: Code DONE (2026-05-22). Phase 1 BE + Phase 2 FE xong, đã spec-review PASS. Chờ user test 9 case.
  Spec: docs/superpowers/specs/2026-05-22-add-member-no-modules-design.md
  Checkpoint: 2026-05-22 — BE: AddMemberRequest (nullable), SolutionService::addMember (DB::transaction + rẽ nhánh has_modules, insert solution_module_members hoặc solution_members, check trùng, throw ValidationException), SolutionController::addMember (catch ValidationException → responseUnprocessableEntity). FE: HumanResourceTab.vue title động, v-if has_modules cho field Hạng mục, availableMembersOptions 2 nhánh, openAddMemberModal/submitAddMember conditional. Bước tiếp: user test 9 case ở spec section 6.

- improve-testcase-baocao → @manhcuong → .plans/improve-testcase-baocao/plan.md
  Trạng thái: Phase 1-3 DONE (2026-05-22). File Testcase_baocao.xlsx đã sửa. Backup giữ .bak. Chờ user review file.
  Checkpoint: 2026-05-22 — 10 sheet báo cáo đều có khối "MÔ TẢ BÁO CÁO" 9 dòng đầu + cột mới "Giải thích nghiệp vụ" + cột "KQ thực tế" đã dịch jargon. Script ở `tools/improve_testcase_baocao.py`. Bước tiếp: user xem file rồi quyết định cleanup (.bak + sheet-data.md).

- personnel-report-contract-status → @manhcuong → .plans/personnel-report-contract-status/plan.md
  Trạng thái: Brainstorming DONE (2026-05-21). Design + plan đã viết. Chờ code.
  Checkpoint: 2026-05-21 — Bổ sung logic trạng thái HĐLĐ theo ngày còn lại (effective/expiring_soon/expired/none) + cập nhật FE text/badge + cột HĐLĐ trong Excel export. Bước tiếp: code BE accessor.

- solution-employee-cross-department → @manhcuong → .plans/solution-employee-cross-department/plan.md
  Trạng thái: Brainstorming DONE (2026-05-20). Spec + design + plan đã viết. Chờ verify payload BE rồi bắt đầu code.
  Spec: docs/superpowers/specs/2026-05-20-solution-employee-cross-department-design.md
  Checkpoint: 2026-05-20 — Mở rộng PM/Leader/Member dropdown ra toàn công ty (cùng `current_company`, `status=1`), đồng bộ cho cả modal "Tiếp nhận yêu cầu giải pháp". BE mở rộng `checkPermissionList` để leader/member phòng khác xem được Solution.

- elearning-auth → @manhcuong → .plans/elearning-auth/plan.md
  Trạng thái: Code DONE v2 (2026-05-20). Phase 0→7 hoàn thành. Chờ: chạy migration + test thủ công 15 TC.
  Spec: docs/superpowers/specs/2026-05-20-elearning-auth-design.md
  Spec cũ (deprecated): docs/superpowers/specs/2026-05-12-elearning-auth-design.md
  Checkpoint: 2026-05-20 — BE 18 files (2 migration, 2 entity, 1 middleware, 6 request, 1 service, 1 controller, 2 resource, 1 mail, 1 blade, module scaffold, config auth, Kernel, modules_statuses) + FE elearning 8 files (api util, store, router, 5 view) + FE hrm-client 1 file (pages/sso/elearning.vue) + env. Bước tiếp: chạy `php artisan migrate` + test 15 TC.

- course-rebuild-subject → @manhcuong/@junfoke → .plans/course-rebuild-subject/plan.md
  Trạng thái: Code DONE P1-P9 (2026-04-22). Phase 13+14 bug fix 2026-04-28.
  Checkpoint: 2026-04-28 — P14 (đang tiếp): fix mã auto-gen BE, override_completion reset, modal info bài học + trạng thái ghi đè, format tiêu chí hoàn thành (giây+%), labels tiếng Việt mapping/prerequisite, DRAFT canDelete, assignee pill auto-open, confirm lock modal. Phase 10 manual test còn 10 test case.

- my-job-assign-business-tab → @manhcuong → .plans/my-job-assign-business-tab/plan.md
  Spec: docs/superpowers/specs/2026-04-20-my-job-assign-business-tab-design.md
  Hoàn thành: 2026-04-21. Phase 1–2 (BE) + Phase 4–8 (FE). BE: routes + service + Resource + Export + Helper. FE: index.vue wiring + AssignBusinessTab.vue đầy đủ (filter 8 ô, bảng 8 cột, 13 row actions dropdown, column customization, ExportModal, ConfirmDelete, ConfirmCancelApprove). Test OK.

- customer-development-report → @manhcuong → .plans/customer-development-report/plan.md
  Hoàn thành: 2026-05-19. Testcases báo cáo QLDA_BC_10 đã bổ sung trong Testcase \_baocao.xlsx. Spec: docs/superpowers/specs/2026-05-18-customer-development-report-design.md
- optimize-getall-manager-context → @manhcuong → .plans/optimize-getall-manager-context/plan.md
  Hoàn thành: 2026-05-11. Tối ưu API getAll khi tạo Task/Issue từ màn Manager: BE thêm filter id vào 2 service, FE truyền id param + lock select. 6 file (2 BE + 4 FE). Spec: docs/superpowers/specs/2026-05-11-optimize-getall-manager-context-design.md
- task-status-notification → @khoipv → .plans/task-status-notification/plan.md
  Hoàn thành: 2026-05-07. 8 case thông báo push (Redis+FCM) khi task đổi trạng thái. Code đã có sẵn trong TaskService::handleStatusNotification(). Spec: docs/superpowers/specs/2026-05-07-task-status-notification-design.md
- learning-path → @khoipv → .plans/learning-path/plan.md
  Hoàn thành: 2026-05-04. Phase 1-7 (24 task). CRUD lộ trình học (3 bảng DB, 4 tab FE: thông tin+builder khoá học, kết quả, người học, chứng chỉ). Danh sách V2Base với lock/unlock, bộ lọc nâng cao 7 ô, popup bài thi + điều kiện học. Spec: docs/superpowers/specs/2026-04-29-learning-path-design.md
- progress-percent-auto-from-log → @manhcuong → .plans/progress-percent-auto-from-log/plan.md
  Hoàn thành: 2026-05-05. Mode B ImportResultModal: Tiến độ hoàn thành tự động từ log gần nhất có giá trị (computed latestLogProgressPct). BE validate tiến độ tăng dần + bắt buộc 100% khi chuyển sang REVIEW/DONE. Spec: docs/superpowers/specs/2026-05-04-progress-percent-auto-from-log-design.md

- issue-completion-flow → @khoipv → .plans/issue-completion-flow/plan.md
  Hoàn thành: 2026-04-28. 22/22 task. Thêm 2 trạng thái completed/rejected vào flow Issue + branching logic approver (duyệt/từ chối) + notification cho approver khi resolved và assignee khi rejected. BE: 1 migration + entity + service + resource + controller. FE: index + modal. Spec: docs/superpowers/specs/2026-04-28-issue-completion-flow-design.md
- add-description-column-list → @khoipv → .plans/add-description-column-list/plan.md
  Hoàn thành: 2026-04-28. 8/8 task. Thêm cột "Mô tả" vào 7 màn danh sách module Giao việc (industry-groups, customer-scopes, solution-groups, application, project_items, project_role, meeting_type). Chỉ FE, không sửa BE/API.
- progress-version-snapshot → @manhcuong → .plans/progress-version-snapshot/plan.md
  Hoàn thành: 2026-04-29. BE snapshot progress version + filter module theo version hiện tại + FE hiển thị version hiện tại và tiến độ trên danh sách giải pháp.
  Checkpoint: 2026-04-29 — user test OK.

- subjects-list-ui → @junfoke → .plans/subjects-list-ui/plan.md
  Hoàn thành: 2026-04-25. Fix 3 bug logic (`exportExcel` formFilter→filters, `lockItem`/`unlockItem` getData→loadData, `getTrainingTypes` method xung đột computed) + 1 bug CSS (`::v-deep` row-actions hover) + thêm nút lock/unlock toggle trong cột Trạng thái + status pill dùng global `tpl-status-*` class từ `v2-styles.scss`. Xóa dead code `onEditClick`/`eventHandler`. Chỉ 1 file: `hrm-client/pages/training/subjects/index.vue`.
- merge-module-review-profiles → @manhcuong → .plans/merge-module-review-profiles/plan.md
  Hoàn thành: 2026-04-25. 7/7 task. Gộp hồ sơ trình duyệt hạng mục vào tab Hồ sơ giải pháp. BE: mở rộng `getSolutionReviewProfiles()` merge 2 query (solution + module) + manual paginate + transform + auto-force type theo filter. FE: 3 filter mới (Loại/Hạng mục/Version HM) + 2 cột mới + deep watcher auto-search + row actions phân loại + tích hợp `ModuleApprovalModal` để PM duyệt hồ sơ hạng mục. Lọc bỏ draft. Spec: docs/superpowers/specs/2026-04-25-merge-module-review-profiles-design.md
- scorm-upload → @khoipv → .plans/scorm-upload/plan.md
  Hoàn thành: 2026-04-22. 14/14 task. Spec: docs/superpowers/specs/2026-04-22-scorm-upload-design.md. BE: `CmcS3Helper::putLocalFile` + `UploadScormRequest` + `LessonService::handleScormUpload` (ZipArchive extract → parseScormManifest → upload S3 recursive với MIME chuẩn → cleanup tmp) + Controller `uploadScorm` + route `POST /training/lessons/upload-scorm`. FE: `LessonForm.vue` block SCORM thêm `V2BaseFile(.zip)` + spinner + info card + `onUploadScormZip` / `clearScormPackage`; submit type=4 gửi thêm `package_path / package_title / file_size / file_name`. Giới hạn 1GB, 2000 files. Known issue pending: cross-origin SCORM API (S3 ≠ LMS domain) — để lại cho feature sau `scorm-lms-runtime`.
  Phase 4 fix (2026-06-02, @junfoke): (4.1-4.3) parser manifest robust — dò identifierref đệ quy qua item lồng nhau + xml:base + fallback quét đệ quy → hết 422 với gói SCORM.com "Randomized Testing"; (4.4) launch URL đổi path-style → virtual-hosted (tanphat.s3.cloud.cmctelecom.vn/<key>) → hết 403 AccessDenied khi preview qua /scorm-proxy; (4.5) bỏ default scorm_min_score=60 → null (gói nội dung không chấm điểm vẫn hoàn thành) + hint UI; (4.6) prune tracking_completion khi submit chỉ giữ key đúng loại bài. Lesson tạo trước fix cần gỡ gói + tải lại rồi lưu lại.
- ke-toan-module-scaffold → @manhcuong → .plans/ke-toan-module-scaffold/plan.md
  Hoàn thành: 2026-04-22. Scaffold phân hệ Kế toán (module mới). BE `Modules/Accounting/` đầy đủ structure + `module.json` + `composer.json` + `AccountingServiceProvider` + `RouteServiceProvider` + `Routes/api.php` (`GET /dashboard`) + `DashboardController` + đăng ký `modules_statuses.json`. FE: layout riêng `layouts/accounting.vue` + sidebar `accounting-components/accounting-slidebar.vue` + topbar `AccountingMenu.vue` (dùng `<BasicSubsystem />`) + `custom-accounting.scss` + `icon_ke_toan.svg` placeholder + Vuex flag `is_use_accounting` (master-setting `use_accounting`) + checkbox "Sử dụng kế toán" tại `/timesheet/setting/setting-master` + tile `BasicSubsystem.vue`/`pages/index.vue` + `pages/accounting/index.vue`+`dashboard.vue`. Tài liệu tổng quan: `docs/accounting.md`. Spec: `docs/superpowers/specs/2026-04-21-ke-toan-module-scaffold-design.md`.
- overdue-task-unified-predicate → @manhcuong → .plans/overdue-task-unified-predicate/plan.md
  Hoàn thành: 2026-04-21. Thêm `Task::scopeOverdue` + áp ở `TaskController::index` + `SolutionService::getCategoriesWithLateTasks`/`getPeopleWithLateTasks` + `SolutionModuleService::getPeopleWithLateTasks`. Đồng bộ `late_tasks_count` + card Overview với logic `overdue_total` tab Task (status NOT IN [1,8,9], CONCAT due_date+due_time). Review pass 0 Critical/Important. Test OK.
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
- pi-approved-price → @nguyentrancu97 → .plans/pi-approved-price/plan.md
  Hoàn thành: 2026-04-13. Cột giá đề xuất + đơn giá duyệt + chênh lệch + notification cho PI nhập khẩu / trong nước (TanPhatDev, 11 files + 1 migration)
- price-request-filter-columns → @nguyentrancu97 → .plans/price-request-filter-columns/plan.md
  Hoàn thành: 2026-04-13. 11/11 task. Thêm filter + cột thương hiệu, hãng SX vào 3 danh sách YCHG/YCTG/Phiếu TG (TanPhatDev, 9 files)
- bill-settlement-remove-checkbox → @nguyentrancu97 → .plans/bill-settlement-remove-checkbox/plan.md
  Hoàn thành: 2026-04-13. 4/4 task. Xoá UI checkbox chọn nhân viên form Quyết toán thưởng NS quý (TanPhatDev)
- bill-income-report-fix-accounting → @nguyentrancu97 → .plans/bill-income-report-fix-accounting/plan.md
  Hoàn thành: 2026-04-29. 4/4 task. Lọc + chạy lại hạch toán phiếu báo có sai. 3 method thêm vào `database/seeds/UpdateDB.php`: `findInvalidBillIncomeReports()`, `fixCustomerSupplierSwap()`, `rerunBillIncomeReportAccounting($ids)`. User chạy 4 step tinker + verify giảm error (TanPhatDev)
- bill-income-supplier-export → @nguyentrancu97 → .plans/bill-income-supplier-export/plan.md
  Hoàn thành: 2026-04-29. 13/13 task. Phiếu báo có loại NCC: thay search HĐ mua trực tiếp bằng search phiếu xuất hàng (3 type 1/2/15) → auto-fill HĐ mua. 8 BE + 1 migration + 3 FE. Test 7 case pass (TanPhatDev)
- pi-inland-supplement-annex → @nguyentrancu97 → .plans/pi-inland-supplement-annex/plan.md
  Hoàn thành: 2026-04-29. 12/12 task. Lập phụ lục bổ sung cho PI trong nước (firm type=4 + free type=5, KHÔNG migration). 2 BE + 5 FE. Test 6 case pass (TanPhatDev)
- delivery-trip-accounting-cost-validate → @nguyentrancu97 → .plans/delivery-trip-accounting-cost-validate/plan.md
  Hoàn thành: 2026-04-29. 10/10 task. Validate cước phiếu hạch toán + enable edit header + tick is_company_sp. 1 migration + controller + JS class + 3 view. Test 5 case pass (TanPhatDev)
- delivery-trip-actual-cost-validate → @nguyentrancu97 → .plans/delivery-trip-actual-cost-validate/plan.md
  Hoàn thành: 2026-04-29. 10/10 task. Validate `total_cost_transition` theo CP xăng + cầu đường + công tác phí + CP khác (xe Tân Phát). JS class + 2 view. Test 6 case pass (TanPhatDev)
- firm-order-contact-select → @nguyentrancu97 → .plans/firm-order-contact-select/plan.md
  Hoàn thành: 2026-04-29. Select người liên hệ cho đơn hàng nguyên tắc thay vì copy từ HĐNT (TanPhatDev). User xác nhận đã làm xong (plan.md không có task chi tiết)
