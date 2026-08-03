# Tinh chỉnh màn Danh sách Dự án tiền khả thi

- **Người phụ trách**: @manhcuong
- **Màn hình**: `/assign/prospective-projects` (Quản lý dự án TKT → Dự án)
- **Spec chi tiết**: `docs/superpowers/specs/2026-06-26-prospective-projects-list-refine-design.md`

## Mục tiêu
Tinh chỉnh bảng danh sách + tùy chỉnh cột + bộ lọc của màn dự án tiền khả thi.

## Scope
1. **Ẩn (chỉ FE)** cột & filter "Nhóm ngành" (`scope`) và "Nhóm giải pháp" (`industry`). BE giữ nguyên field/param.
2. **Đổi tên nhãn (FE)**:
   - "Lĩnh vực khách hàng" → "Lĩnh vực kinh doanh khách hàng" (cột `customerScope`)
   - "Nhóm lĩnh vực khách hàng" → "Loại hình hoạt động khách hàng" (cột + filter `customerScopeGroup`)
3. **Cột "Khách hàng cuối"** (`customerBenefit`): bổ sung dòng Người liên hệ (Tên • SĐT), định dạng như cột Khách hàng. Chỉ hiển thị khi `is_intermediary_customer = true`. SĐT đã được BE mask theo quyền.
4. **Bộ lọc mới**:
   - "Lĩnh vực kinh doanh khách hàng" (`customer_scope_id`) — bật lại dropdown đang comment.
   - "Khách hàng cuối" (`customer_benefit_id`) — autocomplete giống filter Khách hàng (+ thêm param BE).

## Quyết định đã chốt
- Nhóm ngành/Nhóm giải pháp: chỉ ẩn FE, không xóa BE.
- Khách hàng cuối: chỉ hiển thị khi là KH trung gian.
- Thêm cả trường lọc Khách hàng cuối (không chỉ cột).

## File chính
- FE: `hrm-client/pages/assign/prospective-projects/index.vue`
- BE: `hrm-api/Modules/Assign/Services/ProspectiveProjectService.php` (thêm param `customer_benefit_id`)

## Nhất quán với task trước
Cùng cách đổi tên đã áp dụng ở danh mục: `doi-ten-linh-vuc-kinh-doanh-kh`, `doi-ten-loai-hinh-hoat-dong-kh`. Masking SĐT theo `masking-sdt-khach-hang`.
