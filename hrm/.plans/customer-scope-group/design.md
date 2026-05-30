# Design — Nhóm lĩnh vực khách hàng (tóm tắt)

**Spec đầy đủ**: [docs/superpowers/specs/2026-05-28-customer-scope-group-design.md](../../docs/superpowers/specs/2026-05-28-customer-scope-group-design.md)

## Mục tiêu
Chèn tầng trung gian **"Nhóm lĩnh vực khách hàng"** giữa Lĩnh vực khách hàng và Ứng dụng. Bỏ quan hệ trực tiếp Lĩnh vực ⟷ Ứng dụng.

```
Lĩnh vực  ⟷  Nhóm lĩnh vực  ⟷  Ứng dụng     (cả hai đều n-n)
```

## Quyết định cốt lõi
1. **Bỏ** pivot trực tiếp `application_customer_scopes` (migrate trước khi drop).
2. Màn "Nhóm" là danh mục **đầy đủ** (copy pattern customer-scopes): CRUD modal, mã tự sinh `NLVKH.xxxx`, trạng thái, khóa/mở khóa, import/export, 2 permission.
3. Ứng dụng: form/list/filter đổi từ Lĩnh vực → **chỉ Nhóm**.
4. Lĩnh vực: cột "Số ứng dụng" → **"Số nhóm"**; khóa/xóa theo số nhóm.
5. **Dự án tiềm năng**: giữ cả 2 cấp — thêm `customer_scope_group_id`, giữ `customer_scope_id`. Cascade `Ứng dụng → Nhóm → Lĩnh vực`.
   - Luồng xuôi: Nhóm ngành → Nhóm giải pháp → Ứng dụng → Nhóm LVKH → Lĩnh vực.
   - Luồng ngược: Lĩnh vực → Nhóm → Ứng dụng → (suy ra ngành/giải pháp).
6. Migrate: mỗi lĩnh vực có ứng dụng → tạo 1 nhóm tương ứng, gắn lĩnh vực + ứng dụng cũ; backfill `customer_scope_group_id` cho prospective project.

## DB
- **+** `customer_scope_groups`
- **+** pivot `customer_scope_group_members` (Nhóm⟷Lĩnh vực)
- **+** pivot `application_customer_scope_groups` (Ứng dụng⟷Nhóm)
- **+** cột `prospective_projects.customer_scope_group_id`
- **drop** `application_customer_scopes`

## Out of scope
- Không gộp nhóm thông minh, không lịch sử nhóm, không đụng phía Scope/Industry.
