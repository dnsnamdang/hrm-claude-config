# customer-scope-multi-select — Tóm tắt

**Mục tiêu**: Trên form Khách hàng (thêm/sửa/xem/quản lý/danh sách + Thêm nhanh KH ở Dự án TKT) — đổi nhãn 2 trường + tooltip (i), chuyển quan hệ Customer ↔ Loại hình / Lĩnh vực từ 1-1 → 1-N (multi-select), lọc chéo động 2 chiều (OR + auto-clear), và TreeView 2 cấp cho Lĩnh vực kinh doanh.

**Phạm vi**: ERP (`TanPhatDev`, nguồn) + HRM (`hrm-api` sync/BE + `hrm-client` FE). Catalog KHÔNG đổi schema.

**Nhãn mới**:
- "Nhóm lĩnh vực khách hàng" → **"Loại hình hoạt động khách hàng"** — tooltip: "Là tập hợp cùng loại hình hoạt động sản xuất kinh doanh tương đồng về mặt công nghệ."
- "Lĩnh vực khách hàng" → **"Lĩnh vực kinh doanh khách hàng"** — tooltip: "Khách hàng sản xuất kinh doanh sản phẩm dịch vụ cụ thể."

**Quyết định lớn**:
1. TreeView 2 cấp: Loại hình (cha) → Lĩnh vực (lá, checkbox). N-N, không đổi schema catalog.
2. Pivot mới (`customer_activity_types`, `customer_business_fields`) ở cả ERP + HRM; **BỎ HẲN cột đơn vật lý** `customers.customer_scope_group_id`/`customer_scope_id` (drop sau backfill). Downstream không vỡ nhờ resource customer detail **emit field primary computed** (= phần tử đầu pivot) + mảng `*_ids[]`. Blast radius rộng (TKT/meeting/solution auto-fill từ customer, searchCustomer modal, filter list 2 hệ) — xem mục 11 spec.
3. Auto-clear: sửa A → dọn B; sửa B → "tự bỏ A theo" (loại hình hết lĩnh vực con được tích thì bỏ). Mỗi thao tác 1 chiều, 1 lượt.

**Spec đầy đủ**: `docs/superpowers/specs/2026-06-25-customer-scope-multi-select-design.md`

**Lưu ý kiến trúc**: Customer master ở ERP (DB `mysql2`); HRM ghi thẳng ERP rồi sync về. Catalog ở HRM, ERP đọc qua `CustomerScopeReader`. Pivot nằm trong transaction ERP, sync best-effort sang HRM.
