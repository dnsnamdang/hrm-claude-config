# Design (tóm tắt) — Multi-select 3 bộ lọc màn Dự án tiền khả thi

## Mục tiêu
Màn `/assign/prospective-projects` (Quản lý dự án TKT → Dự án). Đổi 3 bộ lọc single-select → multi:
- **Loại hình hoạt động khách hàng** → multi-select dropdown (CheckboxMultiSelect)
- **Ứng dụng** → multi-select dropdown (CheckboxMultiSelect)
- **Lĩnh vực kinh doanh khách hàng** → treeview cha (Loại hình) → con (Lĩnh vực) (CascadeTreeSelect)

List tự lọc theo giá trị tick (deep watcher sẵn có).

## Quyết định chính (chốt user)
- **Ứng dụng** dùng **CheckboxMultiSelect** (chip + search + Chọn/Xóa tất cả).
- **Loại hình + Lĩnh vực** dùng **1 `CascadePairSelect`** — GIỐNG HỆT popup `/assign/application` (2 ô cạnh nhau: cha Loại hình + con Lĩnh vực, mapping cha→con tự lo qua explicitParents, value = mảng cặp `{parent_id, child_id}`). Quan hệ N-N qua `customer_scope_group_members`.
  - Loại hình chỉ là **helper thu hẹp Lĩnh vực** — list lọc theo Lĩnh vực (child) đã tick, KHÔNG lọc Loại hình đơn lẻ (user đồng ý).
- **Giữ cascade** với Ứng dụng (union theo mảng): Ứng dụng thu hẹp Loại hình/Lĩnh vực & ngược lại.

## Kỹ thuật
- BE `prospective_projects` có 3 cột trực tiếp `application_id`, `customer_scope_id`, `customer_scope_group_id`. `ProspectiveProjectService::index`: `where` → `whereIn((array)...)` (bỏ rỗng). Export reuse index → tự áp dụng.
- FE filters: 3 trường → mảng; Lĩnh vực lưu `customer_scope_pairs` (mảng cặp), derive `customer_scope_id = tập child_id` khi gửi API.
- Serialize: dùng `buildQuery` (`key[]=`) thay `buildQueryString` (`key=` — PHP chỉ nhận giá trị cuối). Đây là điểm mấu chốt.
- Cascade computeds/helpers viết lại array-aware (union). Option map `text→name` cho component.
- FIX UI: panel dropdown/treeview (position:absolute) bị `.advanced-filters { overflow:hidden }` (v2-styles) cắt → thêm scoped `.advanced-filters { overflow: visible }` (không !important, để animation collapse dùng inline overflow:hidden vẫn clip đúng).
- Chuẩn hoá localStorage cũ (scalar→array) + deep-clone initialState tránh share ref.

## Không đụng
Migration, permission, hàm dùng chung. Không sửa CheckboxMultiSelect/CascadeTreeSelect (dùng nguyên).

## Verify
- API: single==array-of-one (backward compat); app[]=100,101=23 (union whereIn).
- Playwright 4 AC pass, 0 lỗi console; network gửi `customer_scope_id[]`, `customer_scope_group_id[]=10&[]=21`.

Chi tiết: docs/superpowers/specs/2026-07-14-prospective-projects-multiselect-filters-design.md
