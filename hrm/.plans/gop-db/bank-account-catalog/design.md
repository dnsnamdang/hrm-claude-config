# Danh mục tài khoản ngân hàng (ERP → HRM) — design tóm tắt

- Người phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo)
- Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-03-bank-account-catalog-design.md`

## Mục tiêu

Port màn ERP "Quản lý danh mục tài khoản ngân hàng" (`admin/accounting/account-banks`, model `CompanyAccount`,
bảng `company_accounts` — 40 dòng, 59 file ERP tham chiếu) sang HRM phân hệ **Tài chính**, menu Danh mục
(slot xám có sẵn `finance.js:42`). 2 màn chạy song song trên cùng bảng, KHÔNG đổi schema.

## Quyết định đã chốt (user 2026-08-03)

1. **Tối giản như ERP**: list + lọc + Thêm/Sửa + khóa qua Trạng thái. KHÔNG Xóa (ERP cũng không có),
   KHÔNG export/import/in/lịch sử → không cần hỏi `is_can_delete`.
2. **Scope công ty như ERP**: chỉ thấy + ghi TK công ty user login, `company_id` gán tự động.
   KHÔNG phân quyền theo cấp.
3. **1 quyền như ERP**: `Quản lý danh mục tài khoản ngân hàng` (seeder type=8, group "Danh mục tài chính"
   có sẵn; insert tay DB local, KHÔNG chạy seeder).
4. **Chuẩn base module Assign**: BE ApiController + Service + ListResource; FE V2Base theo
   `pages/assign/industry-groups/index.vue`. Code đặt ở `Modules/Finance` + `pages/finance/account-banks`.

## Điểm kỹ thuật chính

- Entity `CompanyAccount` kế thừa Model THUẦN (không BaseModel — bảng không có created_by/updated_by);
  giữ hook uppercase account_name/bank_name như ERP; bank_name/bank_branch denormalized fill từ id khi lưu.
- `companies` là bảng DÙNG CHUNG trên DB gộp (không có hrm_companies) → company_id không lệch id;
  lấy company user login qua employee_infos, KHÔNG dùng ErpPermissionHelper (mysql2 sai trên gop_db).
- Routes `/v1/finance/account-banks`: index/options/store/update/show — tất cả gắn
  `checkPermission:Quản lý danh mục tài khoản ngân hàng`. Dropdown tiền tệ dùng `finance/currencies/getAll` có sẵn.
- 4 lỗi ERP chủ động sửa khi port: lọc số TK exact → like; update thiếu required currency; BE không check
  chi nhánh thuộc ngân hàng; message unique ghi nhầm "Tên tài khoản".
- FE áp dụng đủ 4 bài học phân trang Phase 8 finance-account-catalog + bug `$nextTick` trước `$bvModal.show()`.
