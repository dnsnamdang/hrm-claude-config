# Plan: Training — Elearning (Umbrella)

## Trạng thái
- Bắt đầu: 2026-04-18
- Tiến độ Phase 0: 3/3 task done (khảo sát BE + FE + deep dive)
- Các phase tiếp theo: chờ user mô tả spec từng feature (dự kiến mai 2026-04-19)

## Phase 0 — Khảo sát codebase + lập tài liệu nền

[x] Task 0: Khảo sát toàn diện module Training, tổng hợp thành `docs/training.md` (codebase map: 10 bounded contexts, 21 endpoint groups, workflow course offline, asset/gap cho elearning, top 10 file để onboard, roadmap sơ bộ). Đã sửa CLAUDE.md từ `Tranning` → `Training`.
[x] Task 0.1: Verify FE thực tế có 51 folder ở `pages/training/`, cập nhật §5 docs/training.md với map đầy đủ FE.
[x] Task 0.2: Deep dive — dispatch 2 Explore agents song song (BE workflow + DB schema, FE pattern + reusable components). Bổ sung §8-12 vào docs/training.md (workflow chi tiết Capacity Evaluate/Survey/Planning/Course Evaluation/Career; Lesson tracking_completion full JSON schema; Question 10 loại; Permission model 16 nhóm; Service pattern; FE patterns V2 components/store/UI conventions; 17 quirks BE + FE).

## Phase 1+ — Triển khai từng feature elearning

> Mỗi feature sẽ tách plan riêng `.plans/training-elearning-<feature-slug>/` với design.md + plan.md. Khi user cung cấp file demo HTML/Vue + spec, sẽ:
> 1. Tạo folder plan riêng cho feature
> 2. Brainstorm + viết design.md
> 3. Lên plan.md với task BE + FE
> 4. Code → test → wrap up

### Feature backlog (sẽ thêm khi user mô tả)
- [ ] Feature 1: <chờ user>
- [ ] Feature 2: <chờ user>
- ...

## Checkpoint

### Checkpoint — 2026-04-18 (Phase 0 done)
Vừa hoàn thành: Phase 0 — khảo sát toàn diện module Training (BE + FE):

**Round 1**: dispatch Explore agent → báo cáo về 10 bounded contexts BE, endpoint groups, workflow course offline, gap cho elearning. Tạo `docs/training.md`. Sửa CLAUDE.md `Tranning` → `Training`.

**Round 2**: verify FE thực tế CÓ và rất nặng (51 folder). Bổ sung §5 vào docs.

**Round 3 (deep dive)**: dispatch 2 agents song song (BE workflow + DB sâu, FE pattern + components). Bổ sung §8-12 (~140 dòng):
- §8: Workflow chi tiết Capacity Evaluate / Survey / Request→Planning / Course Evaluation / Career
- §9: Lesson `tracking_completion` JSON schema đầy đủ 18 trường + Question 10 loại + ExamTestResultDetail
- §10: Permission model 16 nhóm + Service pattern (BaseService, KHÔNG dùng Repository)
- §11: FE patterns (V2 components, store action, UI conventions, mixin)
- §12: 17 quirks BE+FE (đặc biệt: hardcoded dev email, tracking_completion chỉ CONFIG, exam offline-only, LessonForm 116KB monolith, layout exam_todo cũ)

`docs/training.md` cuối cùng: 13 sections, ~580 dòng — đủ để session sau onboard nhanh.

Đang làm dở: không có (Phase 0 done hoàn toàn)

Bước tiếp theo (mai 2026-04-19):
1. User gửi **spec chung** big update elearning + **spec chi tiết từng màn** + file demo HTML/Vue
2. Với mỗi feature: tạo `.plans/training-elearning-<feature-slug>/` riêng → brainstorm design → lên task BE+FE → code
3. Phase 1 đề xuất start: bảng `lesson_progress` + endpoint complete/quiz-submit (gap P1 must-have)

Blocked: không có
