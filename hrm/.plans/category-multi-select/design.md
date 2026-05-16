# Design — Đổi danh mục Nhóm giải pháp & Ứng dụng sang multi-select

> 📄 **Spec chi tiết:** [`docs/superpowers/specs/2026-04-10-category-multi-select-design.md`](../../docs/superpowers/specs/2026-04-10-category-multi-select-design.md)

## Mục tiêu
Đổi 4 trường FK đơn trong 2 danh mục cấu hình của module Assign sang multi-select qua pivot table:
- **Nhóm giải pháp** (`industries`): `scope_id` → multi
- **Ứng dụng** (`applications`): `scope_id` + `industry_id` + `customer_scope_id` → multi

## Quyết định lớn
- **Drop hẳn** cột FK đơn cũ, migrate data sang pivot trong cùng 1 migration (option A)
- **4 pivot table mới**: `industry_scopes`, `application_scopes`, `application_industries`, `application_customer_scopes`
- **Filter list page** giữ single-select (BE chuyển sang `whereHas`)
- **Hiển thị cột bảng** comma-separated, Resource trả thêm trường `*_names`
- **Cascade form Application**: chọn nhiều Nhóm ngành → dropdown Nhóm giải pháp lọc kiểu union, auto-cleanup khi parent bị bỏ
- **Import Excel**: 1 cell, ngăn dấu phẩy: `NN.0001, NN.0002`
- **Validation** required = ít nhất 1
- **Lock/unlock STRICT**: tất cả parent đã chọn phải đang Active mới mở khoá child
- **Downstream** (Solution, ProspectiveProject, FormTemplate, …): ❌ **giả định cũ sai** — sau khi user chạy migration phát hiện 7 chỗ còn tham chiếu cột đã drop (xem Phase 10 trong plan.md). Đã fix: Scope/CustomerScope relations, ProspectiveProject auto-fill, SurveyQuestions Resource, SolutionsWorkSummary report eager-load + fallback, optionsSelect Vuex store, FormMeta cascade filter

## Các vùng code phải sửa
- BE: 2 Model, 4 Service (`IndustriesService`, `ApplicationService`, `ScopeService`, `CustomerScopeService`), 2 Request, 4 Resource
- FE: 2 modal (`industry-modal.vue`, `application-modal.vue`), 2 list page, helper import
- DB: 1 migration mới (4 pivot + backfill + drop cột)

## Rủi ro
- Production cần backup DB trước migration (down() lossy)
- Bản ghi cũ có FK NULL → sau migrate trở thành "không có giá trị" → cần PM rà thủ công
- Cascade auto-cleanup ở FE có thể gây mất chọn bất ngờ → có toast cảnh báo
