# application-scope-solution — Tóm tắt

**Mục tiêu**: Danh mục Ứng dụng (Assign) — bổ sung trường "Lĩnh vực kinh doanh khách hàng" + nâng "Nhóm giải pháp" sang chọn theo CẶP Cha:Con (tree), cập nhật list/filter/import/export.

**Phạm vi**: HRM (hrm-api Assign + hrm-client). KHÔNG ERP.

**Thuật ngữ (DB ngược tên)**: scopes=Nhóm ngành(cha), industries=Nhóm giải pháp(con); customer_scope_groups=Loại hình(cha), customer_scopes=Lĩnh vực(con).

**Quyết định lớn**:
1. Lưu CẶP: thêm `scope_id` vào pivot `application_industries` (Nhóm ngành:Nhóm giải pháp); thêm `customer_scope_group_id` vào `application_customer_scopes` (Loại hình:Lĩnh vực, pivot dead → wiring).
2. Form: 2 trường tree chọn cặp (component dùng chung MỚI `CascadeTreeSelect.vue`, port từ chip+tree của CustomerForm, KHÔNG sửa CustomerForm). Lĩnh vực bắt buộc trên form.
3. List: cột "Nhóm giải pháp"→"Nhóm ngành:Nhóm giải pháp"; thêm cột "Loại hình hoạt động KH" + "Lĩnh vực KD KH"="Loại hình:Lĩnh vực" (cặp, cách `,`). Filter mới: Loại hình + Lĩnh vực.
4. Import: cột Nhóm giải pháp (cặp [Mã nhóm ngành]:[Mã nhóm giải pháp]) + Lĩnh vực (cặp [Mã loại hình]:[Mã lĩnh vực], optional). Export 17 cột (distinct cha + map cặp Mã/Tên).

**Spec đầy đủ**: `docs/superpowers/specs/2026-06-25-application-scope-solution-design.md`

**Lưu ý**: `application_scopes` giữ sync distinct (filter Nhóm ngành); Loại hình distinct suy từ group_id pivot. Industry/Lĩnh vực thuộc nhiều cha → chọn cặp độc lập (như customer).
