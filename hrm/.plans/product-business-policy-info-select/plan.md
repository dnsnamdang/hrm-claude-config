# Plan — Icon Info + diễn giải ô "Chính sách kinh doanh" (Thêm/Sửa hàng hoá)

## Tasks
- [x] Task 1 — BE: thêm `description` vào option `business_policies` trong `ProductOptionService`
      (`formOptions()` dòng ~81 + `optionsForIds()` dòng ~123) qua tham số `extraCols`, không sửa hàm chung. ✅
- [x] Task 2 — FE: tạo wrapper `components/BusinessPolicySelect.vue` bọc `DescriptionInfoSelect`
      (copy pattern `components/MeetingTypeSelect.vue`), `infoLabel="Mô tả chính sách kinh doanh"`. ✅
- [x] Task 3 — FE: thay `V2BaseSelect` → `BusinessPolicySelect` trong `ProductFormAdmin.vue`,
      giữ nguyên `:invalid` / `keep-locked-options` / `@change`. ✅ (ProductFormAdmin.vue dùng chung cho cả Thêm + Sửa)
- [x] Task 4 — Kiểm Playwright: ✅ PASS cả 2 màn Thêm (`/master-data/products/create`) và Sửa
      (`/master-data/products/48464/edit`), tab Quản trị hàng hoá, ô Chính sách kinh doanh.

## Checkpoint — 2026-10-30
Hoàn thành: code Task 1-3 + verify Playwright Task 4.

Kết quả verify (cả màn Thêm lẫn Sửa, giống hệt nhau):
- "Bán sỉ (TEST)"       → icon ⓘ + tooltip `info-popover` = "Áp dụng cho đơn hàng từ 10 sản phẩm…" ✅
- "Bán trả góp (TEST)"  → icon ⓘ + tooltip = "Khách trả trước 30%…" ✅
- "Hàng thanh lý (TEST)"→ mô tả NULL → KHÔNG có icon (đúng, giống meeting) ✅
- Option khoá "Chính sách cũ (TEST-KHOÁ)" (status=2) → ẩn đúng vì bản ghi hiện KHÔNG dùng (chuẩn `select2LockedOption`).
- Icon = `ri-information-line`, tooltip `b-popover custom-class="info-popover"` → khớp chuẩn màn meeting / skill info-icon-tooltip.

Dữ liệu TEST chỉ ở DB local `erp_hrm_check` (4 chính sách CSKD.T01-T04), + grant quyền tạm cho emp13:
- `employee_has_permissions` (perm 101310, emp 13) — grant trực tiếp (KHÔNG đủ vì BE chỉ gom quyền theo role).
- `role_has_permissions` (perm 101310, role 18, company 1) — grant qua role (cái này mới hiệu lực trên FE).
- Đây là data local phục vụ test, KHÔNG commit, user tự xoá khi cần.

Blocked: (không) — feature DONE, chờ user chốt commit.
