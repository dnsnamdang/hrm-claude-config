# Plan — Onboarding Auto-Enroll

> Plan chi tiết (code đầy đủ): docs/superpowers/plans/2026-06-15-onboarding-auto-enroll.md
> Spec: docs/superpowers/specs/2026-06-15-onboarding-auto-enroll-design.md

## Trạng thái

CODE DONE Task 1–4 (2026-06-15, subagent-driven). 11/11 unit test pass, lint sạch. Chờ user chạy migrate + verify browser (Task 5).

## Phase 1 — Backend

### BE
- [x] Task 1: Migration thêm cột `due_date` vào `subject_enrollments`
- [x] Task 2: Unit test logic ngày (`isNewEmployee`, `computeDueDate`) — 11 test pass
- [x] Task 3: `OnboardingAutoEnrollService` (lọc khóa onboarding publish + xác định NV mới + tạo enrollment)
- [x] Task 4: Hook `MyLearningController@learningSpace` (chỉ employee) + dispatch noti gộp
- [x] Task 5: Verify thủ công — user xác nhận PASS (2026-06-15): auto-enroll chạy, thông báo hiện, hạn "Còn 10 ngày" + độ khó hiển thị đúng.

### FE
- Không thay đổi (khóa vừa gán tự xuất hiện trong response learning-space).

---

### Checkpoint — 2026-06-15
Vừa hoàn thành: Task 1–4 (BE core + hook controller). 3 file mới + 1 file sửa. 11/11 unit test pass, `php -l` sạch. Review spec + chất lượng pass (đã fix: guard date rác `'0000-00-00'` + truyền `$now` xuyên suốt; xác nhận `TpEmployee->info` tồn tại nên noti an toàn).
Đang làm dở: (không) — chờ user.
Bước tiếp theo: User chạy `cd hrm-api && php artisan migrate` rồi verify 6 kịch bản Task 5 trên browser.
Blocked:

**File đã đụng:**
- Tạo: `hrm-api/Modules/Training/Database/Migrations/2026_06_15_100000_add_due_date_to_subject_enrollments.php`
- Tạo: `hrm-api/Modules/Training/Services/Subject/OnboardingAutoEnrollService.php`
- Sửa: `hrm-api/Modules/Elearning/Http/Controllers/Api/V1/MyLearningController.php`

### Checkpoint — 2026-06-15 (revise trigger + bugfix)
Vừa hoàn thành: (1) Bỏ guard chặn sớm theo enter_date trong `enrollForEmployee` → ngưỡng=0 gán cho mọi NV kể cả enter_date null. (2) Thêm `OnboardingAutoEnrollService::runAndNotify(Request)` — enroll + ghi DB notification ĐỒNG BỘ (BaseNotification, không queue) + Redis publish realtime best-effort. (3) Chuyển trigger: gọi `runAndNotify` trong `NotificationController::index` (chuông gọi ở MỌI trang → noti hiện ngay sau đăng nhập, không cần mở Góc học tập) + giữ ở `MyLearningController`. Bỏ method private cũ + job queued. Lint sạch 3 file.
Bước tiếp theo: USER chạy `php artisan migrate` (cột due_date) + restart backend local (opcache) + đảm bảo khóa onboarding ở trạng thái Hoạt động, rồi test lại.
Blocked: Nghi vấn chính khiến chưa chạy: migration due_date chưa chạy (create ném lỗi bị nuốt) HOẶC khóa đang Nháp HOẶC backend local chưa nạp code mới.

### Checkpoint — 2026-06-15 (VERIFIED + wire deadline/level)
Vừa hoàn thành: User verify PASS — auto-enroll chạy khi vào app (trang chủ), thông báo hiện ở chuông, click → góc học tập. Fix bổ sung trong session:
- Wire `due_date` vào hiển thị hạn: `DeadlineHelper::resolve()` (ưu tiên due_date, fallback complete_within_days) dùng ở `MyLearningService` (Tôi đang học) + `SubjectDetailController` (màn chi tiết) + cast `due_date` trên model → khóa onboarding hiện "Còn 10 ngày".
- Fix độ khó thẻ "Tôi đang học": BE trả `$s->level_name` (nhãn) thay vì số; FE StudyCard đổi icon `ri-bar-chart-box-line` + ẩn khi không có level.
Bước tiếp theo: (tùy chọn) review tổng + merge. FE elearning cần build trong Docker.

**File đụng thêm (session fix):**
- `hrm-api/Modules/Elearning/Support/DeadlineHelper.php` (+resolve)
- `hrm-api/Modules/Elearning/Services/MyLearningService.php` (deadline resolve + level_name)
- `hrm-api/Modules/Elearning/Http/Controllers/Api/V1/SubjectDetailController.php` (deadline resolve)
- `hrm-api/Modules/Training/Entities/SubjectEnrollment.php` (cast due_date)
- `elearning/src/components/my-learning/StudyCard.vue` (icon + ẩn level rỗng)
