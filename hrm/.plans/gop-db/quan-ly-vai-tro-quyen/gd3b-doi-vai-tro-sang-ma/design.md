# GĐ3b — Đổi các chỗ kiểm theo tên Vai trò sang mã quyền (ghi 01/11/2026)

Nguồn: `../gd3-kiem-quyen-theo-ma/has-role-chua-co-ma.csv` (dòng `xu_ly = chua_co_ma`, 169 chỗ: ERP 161, hrm-api 6, hrm-client 2) — mục A1 của `../gd3-kiem-quyen-theo-ma/van-de-ton.md`. Gộp luôn A2 (duyệt báo giá dự án) và A3 (xoá liên hệ KH).

## 1. Vì sao

- Code còn hỏi "người này có Vai trò tên *Giám đốc* không". Sau GĐ1, Vai trò là dữ liệu admin tự đặt tên trên màn Vai trò: đổi tên "Giám đốc" ⇒ người giữ mất đặc quyền **im lặng**, không lỗi nào báo.
- Quyền phải nằm ở mã, chỉnh được trên màn Phân quyền vai trò, như mọi quyền khác của GĐ3.
- Hiện BE vẫn chạy đúng (ERP `Employee::hasRole` và hrm-api `PermissionLookup::employeeHasRoleBaseName` so `base_name`), riêng hrm-client Dashboard Đào tạo so `roles[].name` (đã có tiền tố công ty) ⇒ khối quản lý ẩn với mọi người — lỗi thật do chuyển đổi.
- Làm **trước go-live TPE** (user chốt 01/11).

## 2. Mục tiêu / không làm / thất bại nếu

**Mục tiêu**
- 169 chỗ đổi sang kiểm mã. Sau khi xong, không còn chỗ nghiệp vụ nào gọi `isRole('<tên Vai trò nghiệp vụ>')` / `hasRole(...)` / `sendNotifyWithRole(...)` / so `roles[].name`.
- **Giữ nguyên đúng người được phép** ở mọi chỗ: lúc go-live, cấp mã mới vào chính các Vai trò đang mang tên tương ứng, cùng công ty — **trừ chỗ nguyên tắc chung (Q4, Q5, Q7) buộc đổi**; mọi chỗ đổi liệt kê ở 4.4, không có ngoại lệ nào khác.
- Sửa Dashboard Đào tạo (hrm-client) theo cùng cách.
- Đi kèm (do Q7 tắt phạm vi Tổng công ty ở 6 công ty): thêm phạm vi 3 (Công ty) vào Catalog 4 mã hiện chỉ có phạm vi 4 — `meeting.phieu_dat_phong_hop.view`, `sale.bao_cao_giu_hang.view`, `customer_care.thong_bao_hoan_thien_ho_so.view`, `customer_care.phieu_cho_giao_viec.view` — và kiểm code đọc 4 mã đó xử lý đúng phạm vi 3. Thiếu ⇒ người 6 công ty mất hẳn 4 quyền này. **Chặn go-live.**

**Không làm**
- Không mở rộng / thu hẹp quyền cho ai (kể cả khi mã có sẵn "gần giống", vd `sale.hop_dong_ban_giam_doc.approve` 53 cặp ≠ 25 cặp Vai trò Giám đốc ⇒ KHÔNG dùng lại, tạo mã mới).
- Không bật nhánh Trưởng phòng (xem 4.3).
- Không đổi các dòng `giu_khong_phai_kiem_quyen` (64) và `bo_dac_quyen` (11) của CSV — đã xử lý ở GĐ3.
- Không sửa logic nghiệp vụ bên trong nhánh (chỉ đổi điều kiện).

**Thất bại nếu** — dù test xanh:
- Bất kỳ cặp (nhân viên × công ty) nào qua/không qua khác trước ở bất kỳ chỗ nào (trừ ngoại lệ GĐ2c ở 4.4).
- Người đang thấy trang/nút bị 403 hoặc mất khối sau go-live.

## 3. Đã chốt với user

| # | Câu | Chốt |
|---|---|---|
| Q1 | Trưởng phòng (26 chỗ, 0 người giữ Vai trò tên đúng "Trưởng phòng") | Đổi sang mã + sửa code kiểm, **không cấp cho ai** ⇒ hành vi giữ nguyên (nhánh vẫn tắt) |
| Q2 | Độ chia mã | **Mỗi chức năng một mã** (không phải mỗi Vai trò một mã) |
| Q3 | Chức năng bậc thang TGĐ → GĐ → TP | **Một mã kèm phạm vi**: 4 Tổng công ty ⇔ TGĐ, 3 Công ty ⇔ GĐ, 2 Phòng ban ⇔ TP |
| Q4 | Công ty kiểm ở hrm-api (2 helper đang không lọc công ty) | **Theo đúng nguyên tắc chung: kiểm ở công ty đang làm** (`current_company_role`). User: *"sau đợt update phân quyền này tôi không chấp nhận còn ngoại lệ nào khác nguyên tắc chung"* |
| Q5 | Chỗ kiểm riêng một bậc | **Phạm vi lớn bao phạm vi nhỏ (`>=`) ở MỌI chỗ** — không so `==`. NV 100 (TGĐ thực tế) phải có tối thiểu mọi thứ của mức Công ty |
| Q6 | Dashboard Đào tạo | **Tách 2 mã**, mỗi khối giữ đúng bộ Vai trò nó kiểm trước GĐ1 |
| Q7 | "Gỡ" phạm vi Tổng công ty ngoài TPE | Hạ xuống Công ty bằng cấu hình GĐ2c (tắt 6 công ty ≠ 1) — xem GĐ2c design mục Q1 |

## 4. Thiết kế

### 4.1 Bảng chức năng → mã (tên mã là đề xuất của Claude, user duyệt khi đọc)

Mã khai trong Catalog hrm-api `app/Support/Permissions/Catalog/<phân hệ>.php` (ERP đọc từ DB). Kiểu và phạm vi theo luật `PermissionCatalog` (kind view|action|approve; scopes tập con 1..4).

| # | Chức năng | Mã đề xuất | Kiểu · phạm vi | Chỗ trong CSV (số thứ tự lọc `chua_co_ma`) | Nền tảng |
|---|---|---|---|---|---|
| F1 | Xem cơ cấu tổ chức mọi công ty / cả công ty (phòng ban, bộ phận, nhóm, hồ sơ NV, ô lọc phòng ban) | `human.co_cau_to_chuc_pham_vi.view` | view · [3,4] | 7–9, 39–42, 80, 98, 99 | erp |
| F2 | Ô lọc Công ty/Phòng/Bộ phận ở báo cáo kinh doanh | `sale.bao_cao_kinh_doanh_pham_vi.view` | view · [2,3,4] | 22–27, 103–116 | erp |
| F3 | Số liệu tổng hợp trang chủ ERP | `sale.trang_chu_so_lieu_pham_vi.view` | view · [2,3,4] | 12–17 | erp |
| F4 | Kho: báo cáo kho, tồn, vị trí, kho kế toán, tồn trên hàng hoá — mọi công ty | `warehouse.kho_moi_cong_ty.view` | view · [4] | 31–38, 62, 63, 66–71 | erp |
| F5 | Giữ hàng — mọi công ty | `warehouse.giu_hang_moi_cong_ty.view` | view · [4] | 64, 65, 158–161 | erp |
| F6 | Yêu cầu đặt hàng nội địa — mọi công ty | `purchase.yeu_cau_dat_hang_noi_dia_moi_cong_ty.view` | view · [4] | 18–21, 28 (builder đọc 28 `FirmContractController:1954` xem có cùng chức năng không; khác thì tách mã) | erp |
| F7 | Danh sách báo giá / hợp đồng / phụ lục theo phòng – theo công ty (cả `ServiceQuotationController:46` chặn trang, cờ `isManager` ở màn duyệt) | `sale.chung_tu_ban_hang_pham_vi.view` | view · [2,3] | 1–6, 29, 30, 49, 50, 53, 58–61, 72, 118, 131, 135, 151 | erp |
| F8 | Ban giám đốc trên màn duyệt chứng từ bán hàng / bảo hiểm (cờ `isBigBoss`, `is_giamdoc`, `is_bgd`, ẩn/hiện khối) | `sale.ban_giam_doc_chung_tu.approve` | approve | 81, 82, 84, 85, 89–97, 100, 117, 119–130, 132–134, 136–150, 152–155 | erp |
| F9 | Xem hỗ trợ hạch toán / giá vốn / quyết toán (cả bản in) | `sale.ho_tro_hach_toan_ban_giam_doc.view` | view · theo luật Catalog (cờ) | 75, 77, 78, 79, 101, 102, 156, 157 | erp |
| F10 | Duyệt vượt hạn mức hợp đồng (ERP + HĐ dự án TKT ở HRM) | `sale.hop_dong_vuot_han_muc.approve` | approve | 73, 74, 76, 162–164 | erp, hrm |
| F11 | Duyệt báo giá dự án — vế Vai trò TGĐ/GĐ (A2; vế mã giữ nguyên) | `sale.bao_gia_du_an_ban_giam_doc.approve` | approve | 54–57 | erp |
| F12 | Khách hàng: phạm vi quản lý KH + phạm vi xoá liên hệ khi sửa KH tổ chức (A3) | `sale.khach_hang_pham_vi.view` | view · [2,3] | 10, 11, 51, 52, 165–167 | erp, hrm |
| F13a | Phiếu bảo hành / sửa chữa / báo cáo bảo hành: GĐ thấy hết | `customer_care.phieu_bao_hanh_pham_vi.view` | view · [3] | 46 (nhánh GĐ) | erp |
| F13b | Phiếu bảo hành…: CSKH được xử lý (phạm vi chờ duyệt + nút) | `customer_care.phieu_bao_hanh_xu_ly.approve` | approve | 45, 47, 48, 86–88 | erp |
| F14 | Kế toán duyệt + nhận thông báo đề nghị thanh toán bảo hành | `customer_care.de_nghi_thanh_toan_bao_hanh_ke_toan.approve` | approve | 43, 44, 83 | erp |
| F15a | Dashboard Đào tạo — khối thứ nhất (`index.vue:642`, Vai trò TP / Quản lý / Quản lý đào tạo) | `training.dashboard_khoi_quan_tri.view` | cờ | 168 | hrm |
| F15b | Dashboard Đào tạo — khối thứ hai (`index.vue:651`, Vai trò TP / Quản lý) | `training.dashboard_khoi_quan_ly.view` | cờ | 169 | hrm |

Chỗ ở các file Blade/model trộn nhiều bậc (vd `HomeController` 2555–2574, `multiFilterJs`, `customer_care_frequency`) đổi thành đọc **một lần** `permissionScope(mã)` rồi so bậc.

### 4.2 Quy đổi điều kiện (giữ nguyên ngữ nghĩa)

- `if isRole('Tổng giám đốc') A elseif isRole('Giám đốc') B elseif isRole('Trưởng phòng') C else D`
  ⇒ `$s = permissionScope(mã)`; `s >= 4 ⇒ A`, `s == 3 ⇒ B`, `s == 2 ⇒ C`, còn lại `D`.
  Người giữ cả TGĐ và GĐ: cũ TGĐ thắng, mới phạm vi lớn nhất = 4 ⇒ giống nhau.
- `isRole('Giám đốc') || isRole('Ban giám đốc')` ⇒ `can(mã cờ)`.
- `isRole('Tổng giám đốc') || isRole('Giám đốc')` (bậc ≥ GĐ) ⇒ `permissionScope(mã) >= 3`.
- **Chỗ kiểm riêng một bậc** (vd `department-filter.blade.php:35` chỉ GĐ; các chỗ chỉ TP) ⇒ `>=` bậc đó (Q5). Không bao giờ `==`.
- **Nhánh không đạt phải fail-closed**: không có mã ⇒ chỉ thấy của mình / không thấy gì, KHÔNG được rơi vào truy vấn không lọc.
- `sendNotifyWithRole('Kế toán', …)` ⇒ gửi cho người giữ mã F14 tại công ty của phiếu (dùng helper gửi theo mã nếu đã có, chưa có thì thêm — builder kiểm).
- hrm-client: `currentEmployee.roles[].name` ⇒ `permission_codes` của user-profile (cách FE đang kiểm mã ở GĐ3).
- Công ty kiểm (đã soát code 01/11):
  - **ERP**: `can()` / `permissionScope()` đọc `info->company_id`, mà `EmployeeInfo::getCompanyIdAttribute()` (`app/Model/Common/EmployeeInfo.php:113`) trả **công ty đang chọn trong session** cho người đăng nhập thuộc > 1 công ty (chưa chọn ⇒ công ty đầu danh sách) — trùng đúng cách `Employee::hasRole` lấy công ty ⇒ đổi sang mã không lệch, không cần truyền `companyId`.
  - **hrm-api**: `PermissionLookup::employeeHasRoleBaseName` / `roleBaseNamesOf` (F10 `ContractService:1139`, F12 `CustomerService:2504`) hiện KHÔNG lọc công ty — chờ user chốt giữ "công ty bất kỳ" hay theo `current_company_role`.

### 4.3 Cấp lại lúc go-live (giữ đúng người)

Vai trò nguồn = `roles.status = 1` có `COALESCE(NULLIF(base_name,''), name)` đúng tên (so như `hasRole` hiện tại), **mọi công ty** trong DB gộp (không chỉ TPE — để etek/toyota cũng giữ nguyên).

| Vai trò nguồn | Rehearsal: số Vai trò · cặp NV×công ty | Được cấp |
|---|---|---|
| Tổng giám đốc | 2 (DTTDETEK, TPE) · 3 | F1, F2, F3 phạm vi 4; F4, F5, F6 phạm vi 4; F11 |
| Giám đốc | 6 · 25 | F1, F2, F3, F7, F12 phạm vi 3; F13a phạm vi 3; F8, F9, F10, F11 |
| Ban giám đốc | 0 | F8, F9 (nếu sau này có Vai trò tên này lúc chạy thì vẫn cấp) |
| Trưởng phòng | 0 | **không cấp** (chốt Q1) |
| Kế toán | 6 · 19 | F14 |
| Chăm sóc khách hàng | 1 (TPE) · 39 | F13b |
| Quản lý (và Trưởng phòng — 0) | 1 (EG) · 15 | F15a, F15b |
| Quản lý đào tạo | 2 (TPE, DTTDETEK) · 19 | F15a |

Cột "Được cấp" phải khớp đúng các nhánh ở 4.1 — builder lập lại từ code thật (từng chỗ dùng Vai trò nào) và sửa bảng này nếu lệch; bảng trên là bản Claude đọc từ CSV.

Cơ chế: **lệnh artisan mới ở hrm-api** (tên do builder đặt, vd `rbac:grant-role-name-codes`), có `--dry-run` + báo cáo CSV (vai trò, công ty, mã, phạm vi, số người), chạy lại nhiều lần không nhân bản. Chạy **sau** `rbac:convert` trong cửa sổ go-live (convert tách Vai trò theo công ty + đồng bộ Catalog ⇒ mã mới đã có). Cập nhật `../gd1-nen-du-lieu/cua-so-go-live-nhanh.md` + `runbook-go-live.md`.

Code mới lên mà chưa chạy lệnh cấp ⇒ mọi người mất các đặc quyền này ⇒ lệnh cấp là bước **bắt buộc** trong cửa sổ, có ở kịch bản lùi.

### 4.4 Chỗ đổi hành vi do nguyên tắc chung (đã chốt — ngoài danh sách này lệch = lỗi)

- GĐ2c: công ty bị tắt `allow_group_scope` ⇒ phạm vi 4 của TGĐ tính như 3 (TGĐ thành như GĐ ở F1–F6). **User chốt 01/11: go-live chỉ TPE (id 1) giữ phạm vi Tổng công ty, 6 công ty còn lại tắt** ⇒ TGĐ NV 1060 ở DTTDETEK (id 8) chỉ còn thấy công ty mình (ở F4–F6 tức là như người không có mã). Vẫn cấp phạm vi 4 cho mọi Vai trò TGĐ (dữ liệu đúng), cấu hình hạ lúc kiểm. Đây là chủ ý, đối chiếu 4.5 tính tập "cũ" sau khi áp cấu hình.
- F4–F6 chỉ có phạm vi 4: người không có mã chạy nhánh "công ty đang làm" như người không phải TGĐ hiện nay.
- Q5 `>=`: TGĐ (NV 100, 426 ở TPE; NV 1060 ở DTTDETEK) thấy thêm ô Phòng ban ở `department-filter` (trước chỉ GĐ). GĐ (phạm vi 3) qua các chỗ chỉ-TP của F7: 4 cờ `$scope.isManager` ở màn duyệt (`contract_addition_annexes`, `liquidation_contracts`, `liquidation_orders`, `service_contracts` approve) — **soát 01/11: biến gán nhưng không chỗ nào đọc (chỉ 1 dòng comment)** ⇒ không đổi gì thấy được; trang `serviceQuotation.ofDepartment` (không có link menu, chỉ vào bằng URL) mở cho GĐ, lọc theo `department_members` của họ.
- Q4: duyệt vượt hạn mức HĐ dự án TKT (`ContractService:1139`) và phạm vi xoá liên hệ KH (`CustomerService:2504`) chỉ tính mã ở công ty đang làm — người giữ GĐ ở công ty khác hết qua. **Đếm rehearsal 01/11 (Task 3, chỉ SELECT; công ty đang làm = `COALESCE(NULLIF(company_role,0), company_id)` vì 10/14 NV có `company_role` NULL): 14 NV giữ Vai trò Giám đốc, 1 người hết qua — NV 197 Trần Thị Hương (Giám đốc ở công ty 8, đang làm công ty 1).** Mới xét theo Vai trò; đo lại theo mã sau khi chạy lệnh cấp ở Task 12. **Đo theo mã 02/11 (rehearsal, sau lệnh cấp; `PermissionChecker` ở công ty đang làm): 12 NV đang hoạt động giữ Vai trò Giám đốc (14 cũ gồm 2 id mồ côi 21, 23 không có trong `employees`), đúng 1 người không qua F10/F12 = NV 197 (Vai trò GĐ ở công ty 8, đang làm công ty 1) — khớp dự báo.** SQL: `task-3-report.md` trong ledger SDD.
- **Lỗ fail-open có sẵn (từ 2021, không do GĐ3)**: `ServiceQuotation::searchByFilter` (ERP `app/Model/Sale/ServiceQuotation.php:265-267`) — `type=department` mà không phải TP thì KHÔNG lọc gì (chỉ `status != 0`), route `serviceQuotation.searchData` không gắn `checkPermission` ⇒ theo code, người đăng nhập bất kỳ gọi `?type=department` nhận báo giá dịch vụ mọi công ty. Rehearsal bảng `service_quotations` = 0 dòng nên chưa lộ được gì thật; prod chưa kiểm. Sửa cùng F7: không đạt ⇒ `created_by = mình` như nhánh mặc định. Builder rà các Datatable/Model khác của F7 có cùng kiểu rơi-không-lọc.

**Số liệu rehearsal 02/11 (Task 12, `hrm_erp_rbac_rehearsal`):** `permission:catalog-sync` thêm 17 mã (F1–F15) · sửa 846 (sort_order dồn + 4 mã [4]→[3,4] của Task 1) · ngừng dùng `admin.tai_khoan.manage` (đã bỏ khỏi Catalog 27/10). `rbac:grant-role-name-codes`: 18 Vai trò · thêm 85 · nâng 0 (0,67 s) — đúng bảng 4.2. `--verify`: 20 dòng lệch, tất cả của 2 employee_id không tồn tại (dòng `employee_has_roles` mồ côi, B.4b dọn lúc go-live) ⇒ **lệch thật 0**. Quét lại: `has_role` còn 7 dòng ERP, đều `giu_khong_phai_kiem_quyen`; `legacy_or_unknown` còn lại (hrm-api 16, client 519, ERP 233) không hit nào ở dòng GĐ3b sửa — tồn đọng GĐ3.

### 4.5 Kiểm chứng

- **Đối chiếu tương đương trên rehearsal** (bắt buộc, là tiêu chí xong): với từng chức năng, tập (NV × công ty × bậc) qua điều kiện cũ = tập qua điều kiện mới sau khi chạy lệnh cấp. Báo cáo ra CSV, lệch = 0 dòng.
- PHPUnit hrm-api + ERP (`tests/Feature/Rbac`): lệnh cấp (dry-run, idempotent, Vai trò đổi tên sau khi cấp vẫn giữ quyền), mỗi mã có ca có quyền + không quyền (memory always-test-permission-cases), các golden test hiện có phải xanh (tên quyền / truy vấn đổi ⇒ cập nhật bộ lọc như GĐ2c).
- Quét lại: `CallSiteScanner` thêm `isRole(` vào `ROLE_RE` (mục C của van-de-ton) ⇒ báo 0 chỗ nghiệp vụ còn lại.
- Playwright (CLAUDE.md): Dashboard Đào tạo (khối quản lý hiện với người giữ F15, ẩn với người không có — đo số khối trong DOM); ERP lấy mẫu ≥ 1 màn mỗi chức năng F1–F14 bằng tài khoản Giám đốc và tài khoản thường (đo DOM: ô lọc Công ty có/không, khối BGĐ có/không).
- E2E spec mới/cập nhật cho Dashboard Đào tạo; không tự chạy cả bộ (memory) — chạy khi user yêu cầu.

## 5. Ràng buộc

- 3 repo worktree `wt-rbac/*` nhánh `rbac`; rồi merge sang `gop_db` local như các đợt trước. Không push khi user chưa bảo (push ERP gop_db = deploy prod).
- Mỗi bước code / chạy lệnh vào DB phải xin phép riêng (CLAUDE.md). DB thử: `hrm_erp_rbac_test` (test), `hrm_erp_rbac_rehearsal` (đối chiếu).
- Blade ERP: tránh `@json(...)` chứa biểu thức phức tạp (memory erp-blade-json-directive-gotcha) — tính biến PHP trước rồi `@json($bien)`.
- Không có migration schema. Lệnh cấp chỉ ghi `role_has_permissions` (+ bảng phụ thuộc mà PermissionChecker cần, builder kiểm).

## 6. Để builder tự quyết

- Tên lệnh artisan, tên helper, cách gom file sửa.
- Tách thêm mã nếu đọc code thấy một nhóm 4.1 thực ra là 2 chức năng khác nhau (giữ nguyên tắc: mỗi chức năng một mã, cấp đúng người cũ) — ghi lại thay đổi vào file này.
- Có giữ hay gỡ `PermissionLookup::employeeHasRoleBaseName / roleBaseNamesOf` và `Employee::isRole` khi hết chỗ dùng.
