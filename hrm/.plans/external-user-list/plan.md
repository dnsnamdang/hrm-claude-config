# Quản lý học viên ngoài công ty — Plan

**Owner:** @junfoke

---

## Phase 1 — CRUD + Danh sách (BE + FE)

### BE

- [x] Migration thêm 4 field (`company`, `position`, `interests`, `auth_source`) vào `elearning_learners`
- [x] Tạo proxy model `ExternalUser` trong `Modules/Training/Entities/`
- [x] Tạo `ExternalUserController` (index, show, toggleStatus, export)
- [x] Thêm routes `/external-users` vào `Modules/Training/Routes/api.php`
- [x] Tạo `ExternalUserExport` + blade template `external_user_report.blade.php`
- [x] Thêm permission ID 1081 `Xem học viên ngoài` vào seeder

### FE (hrm-client)

- [x] Tạo `pages/training/external-user-list/index.vue` — V2Base pattern
  - [x] Filter: keyword, status, auth_source, from_date, to_date
  - [x] Table: STT, userInfo, phone, company, position, authSource, createdAt, status (badge + icon), actions
  - [x] Modal xem chi tiết: custom header, kv-style fields, tóm tắt học tập (placeholder)
  - [x] Khoá/mở tài khoản (toggleStatus + confirm modal)
  - [x] Export Excel

## Phase 2 — Profile elearning

### BE

- [x] Thêm `company`, `position`, `interests` vào `UpdateProfileRequest` rules
- [x] Cập nhật `AuthController::updateProfile` — nhận 3 field mới
- [x] Cập nhật `LearnerResource` — trả thêm `company`, `position`, `interests`, `auth_source`

### FE (elearning)

- [x] Cập nhật `ProfileView.vue`:
  - [x] Employee: tất cả field readonly + banner thông báo
  - [x] Learner: thêm 3 field mới (Công ty, Chức vụ, Lĩnh vực quan tâm)
  - [x] TextareaField component cho interests

---

### Checkpoint — 2026-05-26
Vừa hoàn thành: Phase 2 — profile elearning (BE + FE)
Đang làm dở: không
Bước tiếp theo: Test toàn bộ trên trình duyệt (HRM + Elearning)
Blocked: Cần chạy `php artisan migrate` + insert permission 1081
