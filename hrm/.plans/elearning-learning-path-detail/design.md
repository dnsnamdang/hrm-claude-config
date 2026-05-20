# Elearning — Learning Path Detail (Learner-facing)

## Mục tiêu

Tạo trang chi tiết lộ trình học tập phía elearning (learner-facing), bao gồm cả BE endpoint mới và FE page mới. Follow pattern SubjectDetailView đã triển khai.

## Scope

- **BE**: Tạo endpoint learner mới cho LP detail + enroll LP
- **FE**: Tạo LearningPathDetailView + 6 components con + store + constants
- **Không làm**: Certificate view/download, Bookmark/Save, Search global

## Quyết định chính

| # | Quyết định | Lý do |
|---|-----------|-------|
| 1 | Tạo endpoint learner riêng (không reuse admin) | Cần data learner-specific (progress, status, deadline) |
| 2 | Progress LP tính từ Subject tracking có sẵn | Không cần migration thêm, tận dụng MyCourse tracking |
| 3 | Enroll LP = auto enroll tất cả Subjects | UX đơn giản, 1 click tham gia toàn bộ |
| 4 | Mirror SubjectDetail 1:1 (không reuse components) | Consistent, dễ maintain, không cần refactor code hiện tại |
| 5 | Dùng ID (không slug) cho LP endpoint | LP hiện tại không có slug trong DB |

## Spec chi tiết

→ Xem `docs/superpowers/specs/2026-05-19-elearning-learning-path-detail-design.md`
