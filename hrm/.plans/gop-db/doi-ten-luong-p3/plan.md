# Đổi "Lương P3" → "Định mức thưởng P3" (gop_db) — @manhcuong

- [x] Code FE/BE: đổi mọi text hiển thị (36 file) + seeder quyền/thành phần lương + hasGroup menu
- [x] Migration `2026_10_13_000001_rename_luong_p3_to_dinh_muc_thuong_p3` (permissions 46-49, system_salary_compositions, salary_compositions, salary_template_compositions, p3_salaries, salary_employee_data) — đã chạy local
- [x] Deploy prod 13/10/2026 (api cc8fdac14, client 9a1dd7874) — migrate chạy OK, DB hrm_erp_gop sạch "Lương P3"
- [x] "Lương theo năng suất (P3)" → "Thưởng theo hiệu quả P3", "P3 cố định" → "ĐM thưởng P3" (form các loại quyết định, import, seeder, export) + migration `2026_10_13_000002_rename_p3_co_dinh_to_dm_thuong_p3` — đã chạy local
- [x] Đẩy gop_db (api d20170a26, client 833494213) — [ ] deploy prod chưa làm
