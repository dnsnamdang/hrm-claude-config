# Plan — Seeder xoá data 7 danh mục module Giao việc

Phụ trách: @namdangit

## Mapping màn FE -> bảng
- Lĩnh vực kinh doanh KH -> `customer_scopes`
- Loại hình hoạt động KH -> `customer_scope_groups`
- Nhóm ngành -> `scopes`
- Nhóm giải pháp -> `industries`
- Ứng dụng -> `applications`
- Ngân hàng câu hỏi khảo sát -> `survey_questions`
- Phiếu thu thập thông tin -> `form_templates`

## Quyết định
- Chỉ xoá 7 danh mục + bảng con/pivot nội bộ; KHÔNG xoá data nghiệp vụ tham chiếu (để mồ côi, FK off)
- Truncate (reset ID về 1)
- Xoá thẳng không guard môi trường

## Task
- [x] Map chính xác 7 màn FE -> bảng DB (FE gọi API khác tên màn)
- [x] Viết `Modules/Assign/Database/Seeders/ClearAssignCatalogsSeeder.php` (xoá/truncate)
- [x] Tắt FK check + truncate có guard `hasTable`
- [x] Viết `PrefixOldAssignCatalogsSeeder.php` (gắn tiền tố old_ + khoá, thay vì xoá)
  - code+name: customer_scopes, customer_scope_groups, scopes, industries, applications
  - title: survey_questions; name: form_templates
  - khoá: form_templates=3 (LOCKED), còn lại=2 (INACTIVE)
  - chỉ xử lý bản ghi created_at < 2026-06-29 13:00:00 (giờ VN) — chừa data import mới
  - idempotent: bỏ qua dòng đã có old_ / đã khoá
- [ ] Chạy thực tế trên dev để xác nhận
