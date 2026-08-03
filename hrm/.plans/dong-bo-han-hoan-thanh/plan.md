# dong-bo-han-hoan-thanh — Plan (rút gọn)

Plan chi tiết: `docs/superpowers/plans/2026-07-24-dong-bo-han-hoan-thanh.md`
Spec: `docs/superpowers/specs/2026-07-24-dong-bo-han-hoan-thanh-design.md`

## Phase 1 — BE Training (branch tpe-develop-elearning)
- [x] Task 1: Migration `is_onboarding` + backfill (gộp) + cast Entity SubjectEnrollment
- [x] Task 2: OnboardingAutoEnrollService set `is_onboarding=1`, bỏ ghi due_date + computeDueDate
- [x] Task 3: Nới validate `onboarding_must_finish_days` → nullable (SubjectBuilderRequest)

## Phase 2 — BE Elearning (branch tpe-develop-elearning)
- [x] Task 4: DeadlineHelper `forSubject` / `forPath` (+ addDays); đã dọn compute/resolve dead code
- [x] Task 5: MyLearningService — map is_onboarding + 4 điểm đọc, bỏ computeDeadline
- [x] Task 6: PublicBrowseController::buildDeadlineMap dùng forSubject/forPath
- [x] Task 7: SubjectDetailController + LearningPathDetailController deadline
- [x] Task 8: HallOfFameService::onTimeRate tính đúng hạn dynamic (join subjects)

## Phase 3 — FE
- [x] Task 9: hrm-client TabLearners relabel (mặc định + ghi đè NV mới)
- [x] Task 10: hrm-client TabResult đồng bộ nhãn
- [x] Task 11: FE elearning cập nhật comment dedup (myLearning.js) — merge nay là no-op an toàn

## Phase 4 — Verify
- [x] Task 12: php -l toàn bộ BE sạch; helper verify tinker live (forSubject/forPath đúng); final review 0 Critical/Important
- [ ] (User) Verify browser sau khi migrate

## Việc user PHẢI làm
- `php artisan migrate` (hrm-api) — tạo cột is_onboarding + backfill. TRƯỚC khi test luồng (nếu không, mọi query đọc is_onboarding sẽ lỗi cột thiếu).
- Verify browser portal elearning: hạn khoá onboarding nhất quán giữa tab "Đang học" / "Nội dung bắt buộc" / chi tiết / browse; đổi complete_within_days → hạn dời theo (dynamic).
- FE hrm-client/elearning: Docker/dev tự build.

## Checkpoint — 2026-07-24
Vừa hoàn thành: Toàn bộ 12 task (BE Training + BE Elearning + FE hrm-client + FE elearning). Final review sạch, đã dọn dead code DeadlineHelper::compute/resolve.
Đang làm dở: (không)
Bước tiếp theo: User chạy `php artisan migrate` rồi verify browser.
Blocked: (không)
