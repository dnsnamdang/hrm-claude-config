# Onboarding Auto-Enroll — Tóm tắt thiết kế

- **Người phụ trách:** @junfoke
- **Spec chi tiết:** docs/superpowers/specs/2026-06-15-onboarding-auto-enroll-design.md
- **Trạng thái:** Brainstorming DONE — chờ review spec → writing-plans

## Mục tiêu
Bổ sung phần **thực thi** cho tính năng Onboarding (UI cấu hình đã có sẵn ở `TabLearners.vue`, 3 cột config đã lưu trong `subjects`). Tự động gán khóa onboarding cho nhân viên mới.

## Quyết định chính (đã chốt với user)
- **Cơ chế:** lazy — gán khi NV vào "Không gian học tập" (`GET /api/v1/elearning/my/learning-space`), KHÔNG cron/event.
- **Ngày vào làm:** `enter_date` (EmployeeInfo).
- **Phạm vi:** mọi khóa `onboarding_enabled=1` → mọi NV mới (không lọc theo assignee).
- **NV mới:** `onboarding_new_employee_days=0` (luôn mới, gán cả NV cũ) HOẶC `today - enter_date ≤ days`.
- **Deadline:** thêm cột `due_date` vào `subject_enrollments`, = `enrolled_at + onboarding_must_finish_days` (null nếu days=0).
- **Thông báo:** 1 noti gộp qua `SendNotificationToEmployee` khi có ≥1 khóa mới gán.
- **Chỉ áp dụng user_type=employee** (learner ngoài bỏ qua vì không có enter_date).

## Thành phần
- Migration thêm `due_date` vào `subject_enrollments`.
- `OnboardingAutoEnrollService::runForCurrentEmployee()` (mới).
- Hook trong `MyLearningController@learningSpace` (chỉ employee, try/catch, dispatch noti).
- FE: không đổi.

## Ngoài scope
Cron/event tạo NV, nhắc hạn, learner ngoài, kết hợp assignee, auto-hủy khi hết "mới".
