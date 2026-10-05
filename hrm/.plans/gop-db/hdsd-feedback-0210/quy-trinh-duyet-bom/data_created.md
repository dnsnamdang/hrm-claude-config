# Dữ liệu đã tạo (DB local_hrm_erp, nhánh gop_db) — HDSD Quy trình phê duyệt BOM list

Tạo bằng SQL (clone dòng có sẵn, file work/seed.sql) — tài khoản DNS Admin (employees.id=13) đóng mọi vai trò:
- prospective_projects id=150, mã HN_DA.UD.0137.2026.DA091 "Cung cấp thiết bị thực hành khí nén – thủy lực cho Trường CĐ Cơ giới và Thủy lợi" (clone từ id 148; main_sale/created_by = 13)
- solutions id=953, mã ..._GP01 (pm_id=13, created_by=13, has_modules=1, status 7 → nay 11 Đã duyệt giải pháp)
- solution_versions id=954; solution_modules id=954 (..._GP01_HM01 "Xây dựng danh mục thiết bị", leader 13); solution_module_versions id=6

Tạo qua giao diện:
- bom_lists 23 BOM-2026-00023 (thành phần; lỡ lưu thành tổng hợp → SQL sửa bom_list_type=1) → Đã được tổng hợp
- bom_lists 24 BOM-2026-00024 (tổng hợp HM) → Không duyệt
- bom_lists 26 BOM-2026-00026 (Sao chép từ 24, thêm van điện từ) → Đã duyệt
- bom_lists 27 BOM-2026-00027 (tổng hợp cấp GP) → Đã duyệt
- solution_module_review_profiles 1 (rejected, có lý do), 2 (approved)
- solution_review_profiles 18 HS.TD.HN_DA.UD.0137.2026.DA091_GP01.1 (approved)
- prospective_projects 150 tự đồng bộ sang status 5.
Không đổi mật khẩu tài khoản nào. Không sửa/xoá dữ liệu có sẵn.
(BOM 25, 28 trong bảng là của agent khác.)
