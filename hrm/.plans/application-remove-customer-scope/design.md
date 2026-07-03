# application-remove-customer-scope — Tóm tắt

**Mục tiêu**: Gỡ bỏ hoàn toàn trường "Lĩnh vực khách hàng" khỏi Danh mục Ứng dụng (list filter + cột, form thêm/sửa/chi tiết, import, export, mọi tham chiếu code BE+FE).

**Giữ nguyên**: catalog `customer_scopes` + màn `customer-scopes` (ERP tái dùng).

**Quyết định chính**:
- DB: giữ bảng pivot `application_customer_scopes` (orphan), chỉ ngừng dùng — không migration.
- Downstream: gỡ auto-fill lĩnh vực ở ProspectiveProject (giữ scope+industry); bỏ rule chặn khóa theo ứng dụng ở catalog Lĩnh vực KH.

**Acceptance Criteria**: AC1 list không filter+cột; AC2 form/import/export không trường; AC3 DB không còn ghi pivot.

**Spec chi tiết**: `docs/superpowers/specs/2026-06-09-application-remove-customer-scope-design.md`
