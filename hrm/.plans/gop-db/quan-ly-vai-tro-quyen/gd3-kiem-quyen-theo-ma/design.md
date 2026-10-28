# Giai đoạn 3 (gộp GĐ4) — Kiểm quyền theo mã + gộp phạm vi dữ liệu

> Thuộc `../design.md`. Brainstorm 27/10/2026 với user. **User chốt gộp GĐ3 và GĐ4 thành một giai đoạn,
> làm theo từng phân hệ** (thay cho thứ tự GĐ3 → GĐ4 ở mục 7 design tổng).
> Điểm ghi **[Claude chốt]** là quyết định của Claude, user soát khi đọc. Chưa code. Đụng source phải hỏi riêng.

## 1. Vì sao

Sau GĐ1–GĐ2b, mọi đường kiểm quyền ở ERP và hrm-api đã đi qua `PermissionChecker` và lọc theo công ty
đang làm việc. Nhưng code vẫn gọi bằng **tên tiếng Việt cũ**, dịch sang mã qua `permission_aliases`. Như vậy
đổi một chữ vẫn vỡ code, dev mới vẫn viết theo tên, và các chuỗi `if/else can('… theo X')` vẫn rải khắp nơi.

Đích: **dev chỉ viết kiểm quyền bằng mã, đúng chuẩn; viết sai thì bị báo ngay khi đang làm**, và quy tắc
nằm trong CLAUDE.md để mọi session Claude tự làm đúng.

## 2. Quyết định của user (27/10/2026)

| # | Chốt |
|---|---|
| U1 | Mọi chỗ kiểm quyền ở **ERP, hrm-api, hrm-client, TPE_APP** viết bằng **mã** (`phân_hệ.đối_tượng.hành_động`). Không tên, không id. |
| U2 | Dev viết sai phải bị **cảnh báo ngay khi làm**. Quy tắc tạo quyền + kiểm quyền đưa vào **CLAUDE.md**. |
| U3 | Trên **prod**, gặp tên cũ hoặc mã không có trong danh mục (gõ sai, đã ngừng dùng) ⇒ **chặn + ghi log**. Không đi qua bí danh. |
| U4 | **Gộp GĐ3 + GĐ4**, làm **theo từng phân hệ**: mỗi chỗ chỉ sửa một lần — đổi sang mã và gộp chuỗi phạm vi cùng lượt. |
| U5 | **Không đưa gì lên `gop_db` sớm.** Không merge định kỳ. **Merge `gop_db` → `rbac` một lần ở cuối**, dọn phần phát sinh, rồi lên prod. |
| U6 | **ERP đổi đầy đủ** như HRM (mã + gộp phạm vi), kể cả chức năng đã có bản HRM. |
| U7 | **TPE_APP sửa đồng thời**: app đọc mã thay cho tên; API không giữ trường tên cũ cho app. |
| U8 | **Giữ cửa vào màn như cũ** (phương án a): chỉ người **có mã Xem** (bất kỳ phạm vi nào, kể cả không phạm vi) mới vào được màn/route đọc; có mã mà không phạm vi ⇒ chỉ thấy phiếu `created_by = tôi`. Người không có mã vẫn bị chặn (403 / ẩn menu) như hiện nay. Báo cáo/dashboard tổng hợp: không phạm vi ⇒ **rỗng**. Đây là cách hiểu chính thức của "quyền nền" ở design tổng 5.6. |
| U9 | **Gộp nốt ~25 mã còn mang phạm vi trong tên** (17 Xem, 5 Thao tác, 3 Duyệt — vd "Duyệt chỉ tiêu kinh doanh theo phòng ban / theo nhân viên", `sale.bao_cao_giao_chi_tieu_kinh_doanh_theo_phong_ban.view`) thành mã có phạm vi. Sửa Catalog + `rbac:convert` + dịch dữ liệu gán; **user duyệt bảng đối chiếu mới** trước khi chạy. |
| U9 (sửa 27/10) | Đã rà (`gop-ma-pham-vi.csv`): 27 mã — 18 Xem đã gộp phạm vi từ GĐ1 (chữ trong tên là chiều nhóm báo cáo); 9 Thao tác/Duyệt là **2 loại phiếu khác nhau** (chỉ tiêu, phân chia thị trường, xây dựng giá bán), gộp bằng phạm vi bao trùm sẽ làm dư quyền ⇒ **user chọn GIỮ TÁCH cả 9**. Không còn mã phạm vi nào phải gộp. |

Các nguyên tắc ở design tổng vẫn giữ nguyên: mục 5.6 (phạm vi, "phiếu của mình" = `created_by`, quyền
Thao tác không đi theo phạm vi Xem), mục 5.7 (Super Admin không qua-mặc-định), mục 5.8 (4 giai đoạn lên prod một lần).

## 3. Quy mô (đếm 27/10 trên `wt-rbac`, thô, builder đếm lại chính xác)

- Danh mục: **891 mã**, gánh **1.761 tên cũ**; **1.129 tên cũ mang phạm vi** (`min_scope`), rải trên **314 mã**.
  Đây là các chỗ không đổi máy móc được — phải gộp chuỗi phạm vi.
- Chỗ gọi kiểm quyền bằng chuỗi (grep thô): ERP ~3.600 · hrm-api ~3.000 · hrm-client ~5.000 lượt
  (`hasAPermission` / `hasGroup` / `hasMultiplePermission` / `isShow`).
- Chữ "Super Admin" trong code: ERP 12 (đã gỡ qua-mặc-định ở GĐ1, chỉ còn comment), hrm-api + hrm-client 76.
- Danh mục theo phân hệ (số mã): master_data 135 · sale 98 · purchase 88 · finance 70 · customer_care 67 ·
  assign 60 · warehouse 58 · training 58 · payroll 50 · accounting 45 · presale 39 · decision 37 · human 31 ·
  timesheet 30 · rice 11 · meeting 8 · admin 5 · lookup 1.

## 4. Thiết kế

### 4.1 Cách gọi chuẩn (thay mọi cách cũ)

**BE (ERP + hrm-api)** — trên `PermissionChecker` (đã có `has(code)`, `scope(code)`):
- Có quyền không: `Perm::has('sale.quotation.approve')` (người đăng nhập, công ty đang làm việc).
- Phạm vi: `Perm::scope('sale.quotation.view')` → `1..4` hoặc `null`.
- Middleware route: `checkPermission:sale.quotation.update` (nhận **mã**; nhiều mã nối `|`).
- Lọc dữ liệu theo phạm vi (thay chuỗi `if/else`): một hàm dùng chung, tạm gọi `DataScope::apply($query, $code, $columns)`:
  - 4 Tổng công ty: không lọc · 3 Công ty: lọc công ty đang làm việc · 2 Phòng ban / 1 Bộ phận: lọc theo cột
    người phụ trách/người tạo thuộc phòng/bộ phận của người đăng nhập.
  - **Có mã nhưng không phạm vi**: chỉ bản ghi `created_by = tôi` (U8). Báo cáo/dashboard tổng hợp: rỗng.
  - **Không có mã**: không tới được đây — route/menu đã chặn (U8). Nếu vẫn bị gọi tới thì trả rỗng (fail-closed).
  - `DataScope` phải tách **có quyền** (`has`) khỏi **phạm vi** (`scope`), vì `scope()` trả `null` cho cả
    "không có quyền" lẫn "có quyền không phạm vi". **[Claude chốt]**
  - Mã **không khai phạm vi** (`allowed_scopes` NULL/rỗng) không đi qua `DataScope`, chỉ kiểm `has()` như cũ. **[Claude chốt]**
  - `$columns` khai cột công ty / cột người (mặc định `company_id` + `created_by`). Màn lọc theo cột khác
    (người phụ trách, NVKD, `em_info1..5`…) truyền cột riêng hoặc callback; trường hợp quá đặc thù được giữ
    nhánh riêng nhưng vẫn đọc phạm vi qua `Perm::scope()`.
- Tên `Perm` / `DataScope` là tên tạm. **Builder đặt tên và chỗ để**, nhưng `DataScope` + facade phải
  **giống hệt từng byte ở 2 repo** như `PermissionChecker` (PHP 7.4, Laravel 6 và 8).

**FE (hrm-client)**:
- API profile trả quyền dạng **map mã → phạm vi**: `{ "sale.quotation.view": 2, "sale.quotation.approve": null }`
  (null = có quyền, không có phạm vi). Thay cho danh sách `{name, code}` hiện nay.
- Một helper dùng chung: `hasAPermission(code)`, `permissionScope(code)`. Menu `isShow` dùng mã.
  `hasGroup` / `hasMultiplePermission` đổi sang mã hoặc gỡ nếu chỉ còn là vỏ. **[Claude chốt]**
- FE chỉ là lớp trải nghiệm; mọi chặn thật ở BE (CLAUDE.md, fail-closed).

**JWT claim** (ERP `getJWTCustomClaims`, hrm-api): `permissions` = map mã → phạm vi, `roles` bỏ hoặc
chỉ để hiển thị. **[Claude chốt]** — builder kiểm lại nơi nào còn đọc claim.

**TPE_APP**: đổi các chỗ đọc `permissions[].name` (`employee_info.dart:27–42`,
`dashboard_nhan_vien_page.dart:177–294,456,466,763,765`, `dashboard_nhan_vien_state.dart:26–30`) sang mã,
theo đúng định dạng map mới. Làm trên nhánh TPE_APP riêng. Theo `TPE_APP/CLAUDE.md`.

### 4.2 Chặn và cảnh báo (U2, U3)

- **Prod**: `has()` / `scope()` / middleware gặp chuỗi **không phải mã còn hiệu lực trong danh mục**
  (tên tiếng Việt, mã gõ sai, mã `deprecated_at`) ⇒ trả *không có quyền* + **ghi log** (kênh riêng, kèm mã,
  file/route gọi, người, công ty). Không ném lỗi 500 cho người dùng. **[Claude chốt]**
- **Local + testing** (`APP_ENV` khác production): ném **exception** rõ ràng (`Mã quyền không tồn tại: …`)
  để dev thấy ngay khi bấm màn / chạy test. **[Claude chốt]**
- FE: helper gặp chuỗi không có dạng mã (có dấu cách, có chữ hoa, có dấu tiếng Việt) ⇒ `console.error` ở
  dev, trả `false`. **[Claude chốt]**
- Hết giai đoạn: `hasLegacy()`, `legacyNames()`, `CurrentPermission::GUARD` và mọi đường đọc
  `permission_aliases` **ra khỏi code chạy**. Bảng `permission_aliases` giữ lại cho dữ liệu chuyển đổi
  (`rbac:convert`) và tra cứu. `holders()` / `holdersAnyCompany()` (danh sách người nhận thông báo) chỉ nhận mã.
- **Script quét** (chạy được cho cả 3 repo + TPE_APP), báo:
  1. chỗ gọi kiểm quyền bằng chuỗi không phải mã còn hiệu lực (tên cũ, mã sai, mã ngừng dùng);
  2. chuỗi `if/else` theo phạm vi còn sót (gọi nhiều biến thể phạm vi của cùng một mã);
  3. `hasRole('<tên>')` còn sót;
  4. quyền khai ở seeder cũ (`PermissionsTableSeeder` HRM/ERP) mà chưa có mã trong `Catalog/*.php`.
  Kết quả = 0 ở cả 4 mục là điều kiện lên prod. Script đi kèm lệnh chạy trong CLAUDE.md để dev tự kiểm.

### 4.3 Super Admin và `hasRole`

- hrm-api + hrm-client: đổi các chỗ còn kiểm "Super Admin" (76 lượt) sang mã quyền tương ứng. Super Admin
  có quyền vì được gán đủ mã (đã làm ở GĐ1), không còn nhánh qua-mặc-định ở đâu.
- Mọi `hasRole('<tên>')` khác (ERP ~13, hrm-api ~10) đổi sang kiểm theo mã (design tổng 8.1) — tên vai trò
  đã có tiền tố công ty, không còn dùng để kiểm.
- Chỗ nào không tìm được mã tương ứng: liệt kê ra cho user quyết (thêm mã mới hay gộp vào mã có sẵn).

### 4.4 CLAUDE.md + skill (U2)

- Viết lại mục **Permission** trong `HRM/CLAUDE.md` (hiện dạy seeder theo tên + `RENAMED`/`REMOVED` — sai sau GĐ1)
  và mục tương ứng ở `ERP/CLAUDE.md`:
  - **Tạo quyền**: khai trong `hrm-api/app/Support/Permissions/Catalog/<phân_hệ>.php` (mã, tên, nhóm, phân hệ,
    chức năng, loại, phạm vi được phép, phụ thuộc, nền tảng); không khai seeder; không bao giờ đổi/tái dùng mã;
    bỏ quyền = đánh dấu ngừng dùng.
  - **Kiểm quyền**: chỉ bằng mã qua helper chuẩn (BE, FE, middleware, menu); lọc dữ liệu theo phạm vi chỉ qua
    `DataScope`; cấm `can('<tên tiếng Việt>')`, cấm `hasRole(...)` để kiểm quyền.
  - **Tự kiểm**: lệnh chạy script quét, phải ra 0.
- Viết lại skill `permission-seeder` (hoặc thay bằng skill mới về danh mục quyền) cho khớp.
- Cập nhật các skill khác đang ví dụ `isCurrentEmployeeHasPermission('<tên>')` / `checkPermission:<tên>`
  (builder grep `.claude/skills/`).
- CLAUDE.md / skill là tài sản chung (sửa qua PR) — builder chuẩn bị nội dung, user quyết cách đưa vào.
  Nội dung chỉ có hiệu lực khi `rbac` lên prod (U5): giữ trên nhánh `rbac` của `hrm-claude-config` hoặc bản
  nháp trong folder này cho tới ngày merge. **[Claude chốt]**

### 4.5 Làm theo từng phân hệ (U4)

Mỗi phân hệ là một lượt trọn vẹn, xong mới sang phân hệ sau:
1. Script quét liệt kê mọi chỗ của phân hệ ở cả 3 repo (+ TPE_APP nếu có).
2. Đổi chỗ kiểm có/không sang mã; đổi middleware route; đổi FE + menu.
3. Đường **đọc** có chuỗi phạm vi (danh sách, chi tiết, báo cáo, dashboard, export) và **Duyệt có phạm vi**:
   thay bằng `DataScope`. Ràng buộc ghi (ai sửa/xoá bản ghi nào) **không đụng** (design tổng 5.6).
4. Test BE: mỗi mã có ca **có quyền / không quyền / khác công ty**; đường đọc có thêm ca **từng mức phạm vi**
   + ca "không quyền vẫn thấy phiếu của mình".
5. Kiểm Playwright các màn của phân hệ (đo số dòng, menu hiện/ẩn) bằng tài khoản nhiều mức phạm vi.
6. Script quét phân hệ đó ra 0.

Việc gộp ~25 mã (U9) làm ở phần nền, **trước** phân hệ thí điểm: lập bảng đối chiếu (mã cũ → mã mới + phạm vi,
vai trò đang giữ nhận phạm vi cao nhất như GĐ1), user duyệt, rồi sửa Catalog + `rbac:convert`, diễn tập lại
so sánh quyền hiệu lực trước/sau trên bản sao prod.

Thứ tự phân hệ: **[Claude chốt]** bắt đầu bằng một phân hệ nhỏ có đủ dạng (có chuỗi phạm vi, có màn ở cả ERP lẫn
HRM) làm **thí điểm** để chốt `DataScope` và helper; sau đó đi theo cỡ. Phần nền dùng chung (helper, chặn,
script, profile/JWT, TPE_APP) làm **trước** phân hệ thí điểm. Builder đề xuất phân hệ thí điểm cụ thể.

Trong lúc chuyển dở, phân hệ chưa tới lượt vẫn gọi theo tên cũ ⇒ **chế độ chặn bật theo từng phân hệ hoặc bật ở
cuối**; builder chọn cách, miễn trên nhánh `rbac` các phân hệ chưa đổi vẫn chạy được để test. **[Claude chốt]**

### 4.6 Merge cuối (U5)

1. Mọi phân hệ xong trên `rbac`.
2. Merge `gop_db` → `rbac` **một lần**. Chạy script quét: đổi hết chỗ mới phát sinh, bổ sung mã cho quyền mới
   khai bằng seeder cũ, dịch dữ liệu `rbac:convert` cho quyền mới.
3. Quét lại tới khi 4 mục = 0; chạy toàn bộ test Rbac 2 repo + e2e; diễn tập lại trên bản sao prod
   (runbook GĐ1).
4. Phát hành TPE_APP cùng đợt (U7).

## 5. Ngoài phạm vi

- Ràng buộc ghi của từng chức năng (ai sửa/xoá bản ghi nào).
- Thêm quyền mới / đổi nghiệp vụ quyền. Chỉ đổi **cách gọi**. Ngoại lệ: chỗ không tìm được mã (4.3) do user quyết,
  và việc gộp ~25 mã còn mang phạm vi trong tên (U9).
- Mở cửa màn cho người không có mã Xem (U8 chọn giữ cửa).
- Màn quản lý vai trò (GĐ2/2b đã xong), trừ chỗ chính màn đó còn gác bằng tên cũ.
- Đưa bất kỳ phần nào lên `gop_db` trước ngày merge cuối.

## 6. Phản mục tiêu

- Còn một chỗ kiểm theo tên/id mà script quét không bắt được.
- Có người **dư** hoặc **thiếu** dữ liệu xem được so với trước, ngoài các thay đổi đã chốt (bịt rò công ty, "phiếu của mình").
- Mã sai mà vẫn cho qua (fail-open), hoặc mã sai làm sập màn của người dùng trên prod (500).
- Một chỗ bị sửa 2 lần vì tách bước.

## 7. Kiểm chứng (builder chi tiết hoá)

- So sánh **trước/sau theo dữ liệu**: với một tập tài khoản × công ty × mức phạm vi, gọi các API danh sách/báo cáo
  của phân hệ trên nhánh trước đổi và sau đổi, số dòng và id trả về phải giống nhau (trừ chênh đã chốt).
- Log "mã không hợp lệ" sau diễn tập trên bản sao prod = 0 dòng.

## 8. Rủi ro

- **Merge cuối lớn**: `gop_db` chạy thêm càng lâu, đợt dọn ở bước 4.6 càng nặng (U5 đã chấp nhận).
- **TPE_APP bản cũ**: app không có cơ chế bắt cập nhật (grep 27/10 không thấy force-update). Người chưa cập nhật
  app sẽ **mất menu Phê duyệt / Giao việc / Dashboard quản lý** kể từ ngày lên prod (U7 không giữ trường tên cũ).
- **Gộp phạm vi sai cột**: mỗi màn lọc theo cột người khác nhau; đổi sang `DataScope` sai cột là lộ/mất dữ liệu
  mà không có lỗi nào báo. Bù bằng so sánh trước/sau theo dữ liệu (mục 7).
- Khối lượng ~11.000 lượt gọi qua 3 repo: phải có script hỗ trợ đổi phần máy móc, soát tay phần phạm vi.

## 9. Để builder quyết

- Tên, chỗ đặt, chữ ký của `Perm` / `DataScope` / helper FE; cách khai cột cho `DataScope`.
- Kênh log và định dạng log khi chặn.
- Cách bật chế độ chặn trong lúc chuyển dở (4.5).
- Phân hệ thí điểm và thứ tự phân hệ; chia task; script đổi máy móc.
- Định dạng chính xác của map quyền trong profile/JWT (miễn đủ mã + phạm vi).
