# Dọn quyền trùng nghĩa — nhóm "Mua hàng → Đặt hàng nước ngoài mới"

## Bối cảnh

Nhóm quyền `group_category='Mua hàng'`, `group='Đặt hàng nước ngoài mới'` (guard `web`, 51 quyền)
có **6 loại đối tượng** từng dùng bộ quyền cũ, sau đó được thêm bộ mới 3 cấp chuẩn
("theo tổng công ty / công ty / phòng ban", id 100773–100790, tạo cùng đợt). Việc chuyển đổi
làm dở: màn **danh sách (`searchData`) đã chuyển sang bộ mới**, nhưng hàm xem 1 bản ghi
(`canView`) bị bỏ quên còn trỏ **bộ cũ**; 3 bộ cũ khác thì chết hẳn (không còn code tham chiếu).

Đây là **sai sót lịch sử của ERP** (không phải trùng do gộp DB — tất cả đều guard `web`).

### Bảng đối chiếu (id runtime = guard web, +100000)

| Loại | Bộ cũ | Tình trạng | Bộ mới 3 cấp |
| --- | --- | --- | --- |
| Đơn hỏi hàng - PO | 100366, 100367 | **CHẾT** (0 code) | 100776/100777/100778 |
| Phiếu báo hàng về | 100395 | **CHẾT** (0 code) | 100785/100786/100787 |
| Luồng đặt hàng NK | 100396 | **CHẾT** (0 code) | 100773/100774/100775 |
| Hợp đồng mua hàng NK | 100361, 100362 | sống — `ImportRecord::canView():1023` | 100782/100783/100784 |
| PI | 100368 ("Xem tất cả PI") | sống — `PurchaseInvoice::canView():626` | 100779/100780/100781 |
| Tờ khai hải quan | 100666, 100667 (typo "khải") | ✅ **TEAM ĐÃ FIX** (`d3bdd16f54` + migration `MergeDuplicateCustomDeclarationViewPermissions`) | 100788/100789/100790 |

## Quyết định (user chốt "tự quyết theo đề nghị")

- **Q1 = (a)** `canView` mirror theo `searchData` của **chính từng màn**, giữ đúng độ chặt sẵn có:
  - Hợp đồng NK: giữ **lỏng** (khớp `BuyContract2::canView():1208` — chỉ đổi tên quyền, KHÔNG đổi hành vi).
  - PI + Tờ khai: **3 cấp có so công ty/phòng ban** (khớp `searchData` của chúng), đồng thời vá lỗi
    "thấy danh sách mà không mở được chi tiết".
- **Q2 = (a)** 3 bộ CHẾT: **chỉ xóa** quyền + assignment, KHÔNG cấp thêm quyền mới (giữ nguyên hiện trạng,
  vì quyền chết vốn không có tác dụng → không đổi hành vi thực tế).
- **Q3 = có** — gỡ 9 entry cũ khỏi `PermissionsTableSeeder.php`.

### Ánh xạ di trú role (chỉ áp cho 3 bộ SỐNG)

| Quyền cũ | → Quyền mới tương đương |
| --- | --- |
| Xem hợp đồng mua hàng nhập khẩu của công ty (100361) | Xem hợp đồng mua hàng nhập khẩu theo công ty (100783) |
| Xem hợp đồng mua hàng nhập khẩu của tổng công ty (100362) | Xem hợp đồng mua hàng nhập khẩu theo tổng công ty (100782) |
| Xem tất cả PI (100368) | Xem PI nhập khẩu theo tổng công ty (100779) |
| ~~Tờ khai (100666/100667)~~ | ✅ TEAM lo bằng migration — KHÔNG đưa vào script của tôi |

Di trú = với mỗi dòng `role_has_permissions` trỏ quyền cũ → insert dòng tương ứng quyền mới
(**giữ nguyên `company_id`**, bỏ qua nếu role đã có), rồi xóa dòng cũ.
Xóa 9 quyền cũ = 5 quyền sống (sau di trú) + 3 bộ chết (100366/100367/100395/100396 — chỉ xóa assignment).

## Tasks

### Code (nhánh gop_db, KHÔNG commit tới khi user yêu cầu)

- [x] `ImportRecord::canView():1023` — đổi tên quyền cũ → bộ mới, giữ cấu trúc `hasAnyPermission`
      (khớp `BuyContract2::canView():1208`)
- [x] `PurchaseInvoice::canView():626` — thay `can('Xem tất cả PI')` bằng khối 3 cấp mirror
      `searchData():353-358` (tính `$departments` như 340-342)
- [x] `CustomDeclaration::canView():544-545` — thay 2 dòng typo bằng khối 3 cấp mirror
      `searchData():441-446` (thêm cấp phòng ban, tính `$department_ids` như 427-430)
- [x] `PermissionsTableSeeder.php` — ghi chú 9 entry cũ (361, 362, 366, 367, 368, 395, 396, 666, 667)
- [x] `php -l` 4 file sạch

### Data (script UpdateDB — CHỉ chạy khi user xác nhận cuối)

- [x] Viết lại `UpdateDB::cleanupForeignOrderDuplicatePermissions_20261001($dryRun=true)` trên code SAU pull:
      BỎ 2 dòng tờ khai (team migration lo), THÊM xử lý `employee_has_permissions` (học từ migration team)
- [x] Verify DRY-RUN (read-only) trên erp_new — kết quả: migratedRole=30, migratedEmp=0, dupRole=12,
      deletedAssign=103, deletedPerms=7 (rollback, không ghi)
- [x] **ĐÃ CHẠY THẬT** `(false)` trên erp_new (2026-10-01, user chốt): migratedRole=30, dupRole=12,
      deletedAssign=103, deletedPerms=7. Verify orphan=0 (perms còn lại=0, role/emp orphan=0);
      quyền mới nhận grants: 100783=14, 100782=12, 100779=21. Grep code: 0 tham chiếu tên quyền cũ còn sót.

### Reconcile sau khi pull code mới (2026-10-01)

- [x] Pull cả 3 repo (HRM-api ff; HRM-client merge giữ #11402; ERP ff tới `3d65cfa7d0`)
- [x] Tờ khai hải quan: TEAM đã fix (`d3bdd16f54` + migration) → BỎ phần tôi sửa, dùng bản team
- [x] Khôi phục `ImportRecord.php` (hợp đồng NK) + `PurchaseInvoice.php` (PI) — team không đụng
- [x] Seeder: giữ 666/667 của team, thêm comment 361/362, 366/367/368, 395/396
- [x] php -l sạch 4 file

## Checkpoint — 2026-10-01
Vừa hoàn thành: pull 3 repo; reconcile với fix tờ khai của team (bỏ phần trùng); dựng lại 5-loại-còn-lại
trên code mới (2 canView + seeder + script UpdateDB có thêm employee_has_permissions); DRY-RUN khớp số liệu.
Đang làm dở: chờ user xác nhận để chạy script GHI DB thật `(false)`.
Bước tiếp theo: user OK → `(new \UpdateDB)->cleanupForeignOrderDuplicatePermissions_20261001(false)` → verify orphan = 0 → cân nhắc commit.
Blocked: CHƯA GHI DB (chờ xác nhận).
