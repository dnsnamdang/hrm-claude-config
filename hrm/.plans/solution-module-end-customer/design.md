# Khách hàng cuối cho màn Hạng mục dự án

**Tóm tắt** — chi tiết: `docs/superpowers/specs/2026-06-26-solution-module-end-customer-design.md`.

## Mục tiêu
Hiện "Khách hàng cuối" (kế thừa từ dự án TKT) ở tab Thông tin màn quản lý hạng mục (`/assign/solution-modules/{id}/manager`), khi `is_intermediary_customer=TRUE` + có `customer_benefit_id`.

## Quyết định
- Màn Hạng mục chỉ có 1 màn (manager) → 1 file FE `ProjectInfoTab.vue`.
- Thêm **card mới "KHÁCH HÀNG CUỐI"** ngay dưới "THÔNG TIN KHÁCH HÀNG" (user chốt), cấu trúc 5 dòng tương tự.
- Dữ liệu đọc động qua `module→solution→prospectiveProject`, không snapshot.

## Phạm vi
- BE: `SolutionModuleService::getDetailWithRelations()` thêm 8 key customer_benefit_*/is_intermediary_customer.
- FE: `ProjectInfoTab.vue` thêm card KHÁCH HÀNG CUỐI.
- Ngoài phạm vi: danh sách hạng mục, DB, permission, git.
