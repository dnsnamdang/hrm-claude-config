# admin — so sánh mốc trước / sau (Task 8.2, 28/10/2026)

- Input: `admin-routes.json` — 22 route (11 hrm-api, 11 ERP) × 4 tài khoản = 88 ô.
- Tài khoản (rehearsal, công ty 1): `du_ma` 13 (đủ 5 mã admin.*), `chi_phan_quyen` 144 (chỉ `admin.phan_quyen.manage`),
  `khong_ma` 207, `khong_ma2` 337 (không mã admin.*).
- Admin không có đường đọc lọc theo phạm vi (mọi mã min_scope NULL) ⇒ mốc = status/trang không quyền (-1) + số dòng + băm nội dung.
- Mốc trước chụp 2 lần: khác 0 ô (ổn định).
- **Sau vs trước: khác 0 ô / 88.** Không ô U8 (không mã nào có phạm vi).

| nhóm | du_ma | chi_phan_quyen | khong_ma / khong_ma2 |
|---|---|---|---|
| api admin/roles*, employee-roles*, timesheet/permissions, setting-histories (7+2 route) | 200 | 200 | 403 |
| api menu-settings GET (đối chứng, không gác) | 200 | 200 | 200 |
| erp roles2 index/searchData | 200 | 200 | -1 (not_found) |
| erp api-keys, tutorials, configs, due_configs | 200 | -1 | -1 |
| erp approveList ô HE_THONG "Tài khoản chưa phân quyền" | 1 | NULL | NULL |
