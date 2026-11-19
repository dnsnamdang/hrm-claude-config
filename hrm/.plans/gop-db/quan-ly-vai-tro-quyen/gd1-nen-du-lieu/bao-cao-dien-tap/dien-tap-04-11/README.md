# Diễn tập 04/11/2026 — dump prod 03/11 (`db_gop_3_11`)

- Code: worktree tạm `websites/wt-rbac-dien-tap/hrm-api` detached `7a466818b` (= gop_db local), `.env` trỏ db_gop_3_11, APP_ENV=local, CACHE file.
- Đã chạy (user cho phép, phương án 1): 7 migration `2026_11_01_000001..000005`, `2026_11_02_000001`, `2026_11_02_000010` lẻ `--path`. company_employees trùng = 0.
- `rbac:convert --dry-run` ⇒ **exit 1 ở bước 3**: 42 tên quyền guard `api` không thuộc danh mục (file `42-ten-chua-khai-catalog.tsv`).
  Đã rollback sạch (permission_aliases 0, permissions.code 0).
  - 35 tên = bản `api` của tên đã có `web` trong Catalog (prod sinh 23/10 + 03/11, HRM code origin/gop_db kiểm theo tên này: Assign, Finance…).
  - 7 tên mới hẳn: Xem phiếu hạch toán dịch vụ HDDV (3 phạm vi), Xem yêu cầu hạch toán dịch vụ HĐBH (4 phạm vi) — commit origin/gop_db chưa kéo.
  - Cả 42: 0 vai trò, 0 NV gắn.
- gop_db local chậm origin/gop_db: hrm-api 75, client 65, ERP 10 commit.
- Dừng chờ user cho phép sửa Catalog.

## Tiếp 04/11 (user "làm 1+2")
- hrm-api: merge origin/gop_db → `d1cab028a` (làm trong worktree tạm, rồi ff gop_db checkout chính). Gỡ: route nhắc việc lấy origin;
  PriceAskingAccess COST → `master_data.gia_von_hang_hoa.view`; seeder Timesheet giữ đã gỡ; bỏ mã `assign.nhac_han_cong_viec.configure`.
- Catalog: 42 tên `api` gắn vào mã có sẵn (`42-ten-da-gan-ma.tsv`), KHÔNG mã mới. HĐBH → `customer_care.yeu_cau_hach_toan_lam_dich_vu.view`
  (khớp ERP ServiceAccountingRequest); phiếu HDDV → `accounting.phieu_hach_toan_dich_vu_hddv.view` (ERP dùng 1 mã cho cả yêu cầu + phiếu).
  CHƯA commit ở: checkout chính gop_db, wt-rbac (rbac), worktree tạm.
- Dry-run lần 2: exit 0, chenh-lech-khac 0, 17 s (`tom-tat-dry-run.json`). Chạy thật: exit 0, 14,8 s.
- B.4b: thiếu company_employees 0 · mồ côi 12 dòng (cả 12 tài khoản đã xoá) đã xoá · mất quyền quản lý tài khoản 0.
- Khối 5: catalog-sync 0 thay đổi · roles không công ty 0 · rbac_role_map 283 · aliases 1.859.
- 5b: 18 Vai trò · thêm 85 (khớp 02/11). **Verify lệch 441 — cả 441 là cũ 0 → mới 1, 100% do vai trò Super Admin (12 NV)**:
  convert lần này đã có 17 mã GĐ3b trong Catalog ⇒ bước 5 "Super Admin đủ mã" cấp luôn (02/11 các mã này sync sau convert).
  ⇒ CHỜ USER CHỐT. Playwright chưa chạy.
- permission:scan: 33 legacy_or_unknown; các dòng có mã chạy qua alias. 5 tên không mã ("Quản lý danh mục khách hàng", "Xem danh sách hạng mục
  dự án theo…", "Xem danh sách loại HĐLĐ theo…", "Duyệt thông báo nội bộ", "Quản lý thân nhân") không có trong DB prod ⇒ lỗi có sẵn, ngoài luồng.
- hrm-client gop_db local chưa kéo origin (65 commit) — còn menu "Cấu hình nhắc hạn công việc" mà origin đã bỏ.
- **User chốt 04/11 (phương án 2): CHẤP NHẬN** Super Admin nhận đủ mọi mã kể cả 17 mã GĐ3b. Verify 5b sáng G: lệch chỉ được là dòng
  cũ 0 → mới 1 của NV giữ vai trò Super Admin (diễn tập 04/11: 441 dòng / 12 NV); dòng khác ⇒ dừng.
- Playwright HRM (API :8031 worktree tạm, client :3031 build `.nuxt-dientap`, Chrome hệ thống): NV 13 vào được Vai trò / Vai trò NV /
  Cấu hình phạm vi TCT (9 công ty, SAU khi thêm `RBAC_GROUP_SCOPE_ADMINS=13` — thiếu biến ⇒ 404, đúng mục A6) / khách hàng 10 dòng;
  NV 1027 (5 công ty): API đổi công ty ra số mã khớp DB 287/6/6/27/10, 3 màn quản trị 404, khách hàng 10 dòng; NV 663 (0 vai trò):
  0 mã, 3 màn quản trị 404, khách hàng 0 dòng. 0 API lỗi. ERP CHƯA smoke.
- Excel vai trò × quyền: `Vai tro va quyen sau chuyen doi - db_gop_3_11.xlsx` (282 vai trò, 19.526 dòng = 19.441 + 85 GĐ3b).
- 04/11 kéo origin/gop_db vào gop_db local (CHƯA push): hrm-api `d1cab028a` (+40), hrm-client `0db94d679` (+35; gỡ xung đột
  product-export-requests/index.vue: logic origin + mã accounting.ke_toan_kho.manage), ERP `833347637c` (+25, merge sạch, không migration).
  ERP mới có `can('Duyệt phiếu nhập kết quả')` theo tên → đi qua alias web (đã có). permission:scan client: không tên lạ nào do đợt merge.
  ⇒ Bảng SHA trong cua-so-go-live-nhanh.md phải cập nhật lại trước giờ G.
- **ERP smoke 04/11** (worktree `wt-rbac-dien-tap/TanPhatDev` @833347637c, `.env` → db_gop_3_11, php -S :8043; checkout ERP chính KHÔNG dùng vì
  bootstrap/cache/config.php trỏ DB prod). Phiên tạo bằng tinker — mỗi phiên 1 lần tinker (logout trong vòng lặp làm hỏng phiên).
  - 0 migration ERP chờ. Dropdown chức vụ người ký `Role::activeForDropdown()` = 282 (vụ 31/10 ra 0). 0 lỗi JS.
  - Hợp đồng bán `?type=all`: NV 13 (sale.hop_dong.view=4) 27.998 không lọc công ty; NV 1027 TPE (=3) 16.321, SQL `company_id=1 OR created_by`;
    NV 1027 TPHP / NV 663 (không mã) 0. Mở không kèm `type` = tab "Của tôi" (created_by) — không phải lỗi.
  - Menu đổi theo công ty: NV 1027 TPE 476 link /admin, TPHP 446 (30 mục chờ duyệt/hạch toán chỉ ở TPE); NV 13 488; NV 663 441.
  - `/admin/roles` ERP → chuyển sang HRM `/admin/roles`. Local lặp vô hạn vì `.env` ERP `HRM_URL_FE =` RỖNG ⇒ **go-live: kiểm `HRM_URL_FE`
    ở .env ERP prod có giá trị** (thiếu ⇒ màn Vai trò từ menu ERP lặp chuyển hướng).
- 04/11 commit Catalog 42 alias: gop_db hrm-api `aac684f92`, rbac `757b32e4b` (CHƯA push). ERP kéo thêm task 11833 → `84bec64416`.
