# Di trú dữ liệu 1 công ty (one-time, ánh xạ ID liền mạch) — Tóm tắt

> Spec chi tiết: `docs/superpowers/specs/2026-06-17-di-tru-du-lieu-cong-ty-design.md`

## Mục tiêu
Đưa toàn bộ dữ liệu nghiệp vụ chính của 1 công ty (chạy cùng codebase, DB `local_hrm_green`)
sang DB đang chạy thật `hrm_prod_local`, thành **một `company_id` mới**, không đụng data cũ.
ONE-TIME cutover (nguồn tắt sau khi chuyển).

## Sự thật từ DB (đã đo 2026-06-17 — QUAN TRỌNG)
- Nguồn **chỉ 1 công ty**: `id=1 — ETEK GREEN`. Đích là hệ Tân Phát (8 công ty), **đã có sẵn ETEK GREEN ở `company_id=7`** (chỉ 3 NV + 2 PB test).
- Quyết: **tạo công ty mới** (id mới); **pre-step đổi tên dòng id=7 cũ** (vì `companies.name` unique) để công ty mới lấy tên gốc.
- **Đăng nhập ở bảng `employees`** (123), KHÔNG phải `users` (rỗng).
- **Phân quyền dùng `employee_has_roles`/`employee_has_permissions`** (KHÔNG có spatie `model_has_*`). `permissions` (580) khớp 100% đích → map identity.
- **`files` rỗng** → không migrate files; ảnh NV là cột path trên `employee_infos` (chung bucket → tự sống).
- **Đụng email `namdangit@gmail.com`** (cả employees + employee_infos) → bỏ qua bản nguồn, giữ đích.
- Nhiều bảng config rỗng ở nguồn (salary_generals, tax_generals, regulation_*, rice_*, assign_configs...). Có data: hồ sơ NV 124, salary_compositions 49, salary_templates 1, holidays 18, leave_types 7, số dư phép 287, lương 77...
- Chi tiết hiện trạng từng bảng: xem §12 trong spec.

## Phạm vi
- **Đưa sang:** hồ sơ nhân sự + tổ chức, cấu hình nghiệp vụ per-company, phân quyền/tài khoản,
  số dư đầu kỳ nhân sự (lương hiệu lực, người phụ thuộc, thuế, BH, số dư phép), bản ghi `files`.
- **KHÔNG đưa:** data giao dịch lịch sử theo kỳ (chấm công/bảng lương kỳ cũ); object S3 (chung bucket → link cũ sống).

## Quyết định lớn
- **Remap ID = Hướng B (ánh xạ ID liền mạch theo từng bảng)** — lý do bỏ Hướng A (offset): KHÔNG để id nhảy bậc (offset band cao buộc AUTO_INCREMENT nhảy ~102M). Mỗi bảng: id mới = nối tiếp sau `max(id)` đích; lưu bảng `migration_id_map(table, old_id, new_id, run_id)` để dịch FK + rollback.
- Bảng **dùng chung** (tỉnh/huyện/xã, banks, system_salary_compositions, majors, areas, permissions) → map theo natural key, KHÔNG chèn.
- **users không trùng email** → chèn thẳng (có tiền-kiểm).
- **roles** (bảng global) → luôn chèn role mới + đổi tên (hậu tố tên công ty).
- **Bắt buộc chạy trong cửa sổ bảo trì** (id cấp sát max, không cho chèn đồng thời).
- Đọc nguồn qua **connection thứ 2** `mysql_source` khai trong `.env`/`config/database.php`.
- Thực thi bằng **artisan command** `company:migrate-in` có `--dry-run`, chạy trên copy DB đích trước, backup trước khi chạy thật.

## Điểm cần nhớ khi triển khai
- FK bảng OWNED → bảng OWNED khác: tra `migration_id_map`; FK → bảng SHARED: tra map natural-key (dễ sai nhất → cần bản đồ "cột FK → bảng nào" chính xác).
- Chèn bảng cha trước bảng con (để có map khi dịch FK); `SET FOREIGN_KEY_CHECKS=0` khi chèn.
- Phân quyền: pivot dùng cột `employee_id`; `role_has_permissions` per-company (PK composite + company_id); `employee_infos.company_role` cần remap.
- Phase 0 quét tự động `Schema::hasColumn('company_id')` để không sót bảng config.
- Kiểm `titles` (mâu thuẫn company_id model vs migration) ở Phase 0.

## Các pha
0. Catalog & classification (OWNED/SHARED + FK→shared) — quan trọng nhất
1. Hạ tầng: connection nguồn + khung command + backup
2. Shared mapping (natural key) + đối soát
3. Core: companies → tổ chức → employees → số dư → config → files
4. Phân quyền: users/roles/company_roles/role_has_permissions/model_has_*
5. Verify & cutover
