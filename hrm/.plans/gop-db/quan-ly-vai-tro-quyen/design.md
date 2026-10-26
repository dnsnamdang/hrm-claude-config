# Thiết kế lại quản lý Vai trò & Quyền (ERP + HRM)

> Tài liệu tổng quan cho feature lớn. Mỗi giai đoạn bên dưới khi bắt đầu sẽ có folder con riêng
> (`design.md` + `plan.md`). Không dựng sẵn folder rỗng.
> Ngày chốt: 25/10/2026. Tài liệu cũ `.plans/gop-db/thiet-ke-lai-phan-quyen/` và nhánh
> `permiss_manager` (worktree `wt-phan-quyen`) **bị huỷ**, user đã chốt bỏ hẳn vì theo logic khác.
> Chỉ dùng để tham khảo, không kế thừa code.

## 1. Mục đích

Người vận hành đang khổ với việc phân quyền vì 3 lý do:

1. **Không tìm được quyền.** Màn phân quyền của cả ERP (AngularJS) lẫn HRM (`components/setting/Permission.vue`)
   đều không có ô tìm kiếm. Không biết một quyền nằm ở phân hệ nào, nhóm nào.
2. **Logic công ty rối, và đã rò quyền.** Hiện một role gắn được nhiều công ty, và mỗi công ty mang
   một bộ quyền khác nhau (`role_has_permissions.company_id`). Muốn biết "A ở công ty X được làm gì"
   phải ghép 2 lớp công ty. Một số đường kiểm quyền không lọc công ty, nên có quyền ở A là qua cửa ở B.
3. **Quyền gắn với tên tiếng Việt.** Đổi 1 chữ là vỡ code. Seeder đồng bộ theo tên, đã từng gây trùng id
   khi merge nhánh, kéo nhầm quyền, phải chèn tay vào DB.

Hệ thống đang trong giai đoạn chuyển chức năng từ ERP sang HRM, nên ERP vẫn chạy thật trong khi HRM
đang test. Vì vậy quản lý quyền phải phục vụ **cả hai nền tảng cùng lúc**, từ **một màn duy nhất** ở
phân hệ **Quản trị** của HRM.

## 2. Hiện trạng (khảo sát 25/10/2026, DB local `hrm_erp_21_10_prod`)

| Hạng mục | ERP (TanPhatDev) | HRM (hrm-api / hrm-client) |
|---|---|---|
| spatie/laravel-permission | 3.18.0 | 5.5.16 |
| Guard | `web` (958 quyền, id 100001–101050, 77 role) | `api` (904 quyền, 715 có `code`, 62 role) |
| Khai quyền | `database/seeds/PermissionsTableSeeder.php` (958 dòng `perm`) | `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (917 dòng) |
| Đồng bộ | `app/Support/Permissions/PermissionSync.php`, khớp **theo tên** | bản sao y hệt, khớp **theo tên** |
| Kiểm quyền | `->can(` 3.397 · middleware `checkPermission:` 702 · `hasPermissionTo` 107 · `hasAnyPermission` 21 · `canInCompany` 19 · `hasRole('Super Admin')` 224 | BE: `isCurrentEmployeeHasPermission` 855 · `checkPermission:` 648 · `checkPermissionList*` 99. FE: `hasAPermission` 460 · `hasGroup` 32 · `hasMultiplePermission` 13 · menu `isShow` 227 |
| Kiểm theo | tên tiếng Việt | tên tiếng Việt (cột `code` có nhưng không dùng) |
| Công ty hiện tại | `session('current_company')` | `employee_infos.company_role` |
| Màn phân quyền | `common/roles/*.blade.php`, mỗi công ty 1 tab, không tìm kiếm | `pages/timesheet/setting/roles/*`, mỗi công ty 1 tab, không tìm kiếm |
| Nhóm quyền | `group` (137) + `group_category` (7) | `type` (17 phân hệ) + `group` |

Dữ liệu dùng chung một DB: `permissions`, `roles`, `role_has_permissions(permission_id, role_id, company_id)`,
`employee_has_roles(role_id, model_type, employee_id, company_id, position)`, `company_roles(company_id, role_id)`.
`employee_has_permissions` đang trống.

Những điểm đáng chú ý:
- 54 role mang quyền ở nhiều công ty, trong đó **52 role có bộ quyền khác nhau theo công ty**. 43 role
  đang được gán cho nhân viên ở hơn 1 công ty.
- 18 role chứa quyền của cả 2 guard. 136 dòng gán quyền `api` vào role `web`.
- 4 tên role bị trùng.
- **Rò quyền giữa các công ty** (đọc code, chưa thử thật):
  - ERP `Employee::hasAnyPermission` (`app/Employee.php:1456`) chỉ kiểm "có role nào ở công ty
    hiện tại mang quyền", rồi gọi `checkPermissionTo` không lọc công ty.
  - HRM `BaseModel.php:204`, `ApiController.php:159` và middleware `CheckPermission` đi qua
    `Employee::getAllPermissions()`, hàm này không lọc `company_id`.
- Phạm vi dữ liệu đang viết thẳng vào tên quyền. ERP có khoảng 470 quyền dạng "… theo tổng công ty / công ty /
  phòng ban / bộ phận / nhân viên", kiểm bằng chuỗi `if/else can()`. HRM viết vào đuôi mã
  (`.view.company`, `.view.all_company`).
- ERP: `Gate::before` cho Super Admin qua hết (`app/Providers/AuthServiceProvider.php:28`). JWT claim
  mang toàn bộ tên quyền (`app/Employee.php:533`).
- Menu Quản trị HRM đã có sẵn: `components/subsystems.js:196` (key `admin`) và `components/subsystem-menu/admin.js`
  ("Người dùng & phân quyền").

## 3. Mục tiêu · Ngoài phạm vi · Phản mục tiêu

**Mục tiêu**
- Một màn quản lý Vai trò & Quyền duy nhất ở phân hệ Quản trị HRM, phục vụ cả ERP và HRM.
- Tìm được bất kỳ quyền nào theo tên hoặc mã, và thấy ngay nó thuộc Nhóm phân hệ, Phân hệ, Chức năng nào.
- Mọi chỗ kiểm quyền ở ERP, hrm-api, hrm-client đều kiểm **theo mã** và **luôn theo công ty đang làm việc**.
- Quyền mới sinh ra từ code và đồng bộ khi deploy, không phải chèn tay, không trùng id.
- Mỗi vai trò thuộc đúng một công ty. Bỏ hẳn cơ chế một role mang quyền khác nhau ở nhiều công ty.
- Phạm vi dữ liệu là một thuộc tính khi gán quyền, không phải quyền riêng.

**Ngoài phạm vi**
- **Chức vụ** của phân hệ Nhân sự (vị trí công việc) không đổi gì. Feature này chỉ đổi tên khái niệm
  role thành **Vai trò** để khỏi lẫn với Chức vụ.
- Không xây công cụ cho quản trị viên tự tạo quyền.
- Không chặn chức năng HRM chưa test xong bằng quyền. Nếu cần chặn thì làm bằng menu hoặc phát hành chức năng.

**Phản mục tiêu** (chạy được về kỹ thuật vẫn tính là thất bại nếu dính 1 trong các điểm sau)
- Có bất kỳ người dùng nào **mất** hoặc **dư** quyền so với hiện tại sau chuyển đổi, trừ phần
  dư do lỗ rò công ty được bịt (phần đó cố ý mất).
- Còn bất kỳ đường kiểm quyền nào không lọc công ty.
- Quản trị viên công ty B nhìn thấy hoặc sửa được vai trò của công ty A, hoặc cấp/gỡ vai trò ở công ty A.
- Kiểm quyền "fail-open": mã sai hoặc chưa khai mà vẫn cho qua.
- Trên màn hình, trong tài liệu hay tên code mới còn chữ "chức vụ" để chỉ role.

## 4. Thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| **Vai trò** | Thay cho "role" / "chức vụ" (cũ). Một vai trò thuộc **một** công ty, gồm một tập quyền (kèm phạm vi). |
| **Chức vụ** | Khái niệm của phân hệ Nhân sự. Không liên quan đến feature này. |
| **Quyền** | Một hành động trên một đối tượng, định danh bằng **mã**. |
| **Mã quyền** | Chuỗi cố định, ví dụ `sale.quotation.approve`. Không đổi, không tái sử dụng. |
| **Phạm vi** | Cấp dữ liệu được áp khi gán quyền cho vai trò: Tổng công ty ⊃ Công ty ⊃ Phòng ban ⊃ Bộ phận. |
| **Nền tảng áp dụng** | ERP / HRM / Cả hai. Là nhãn của quyền. |
| **Công ty làm việc** | Danh sách công ty một tài khoản được làm việc. |
| **Công ty chính** | Công ty gốc của tài khoản. Quản trị viên công ty này quản lý danh sách công ty làm việc. |
| **Quản trị viên công ty X** | Người có quyền "Quản lý phân quyền" trong một vai trò thuộc công ty X. |

## 5. Nguyên tắc đã chốt với user

### 5.1 Vai trò ↔ công ty
- Mỗi vai trò thuộc **đúng một công ty**. Quyền gắn thẳng vào vai trò. Bỏ `company_id` trên từng dòng quyền.
- Hai công ty cùng cần "Kế toán" thì tạo 2 vai trò riêng.
- Chỉ kiểm trùng tên **trong cùng công ty**. Khi lưu, tên được **gắn tiền tố mã công ty**:
  `TPE_Kế toán`, `TPSG_Kế toán`.
- Dữ liệu cũ: role dùng chung nhiều công ty được **tự tách** thành nhiều vai trò, mỗi công ty một bản,
  giữ nguyên bộ quyền và người được gán ở công ty đó.

### 5.2 Người dùng ↔ công ty
- Danh sách công ty làm việc của một tài khoản do **quản trị viên công ty chính** khai, ở màn Quản lý tài khoản.
- Quản trị viên **công ty kiêm nhiệm không được tự kéo** người của công ty khác về.
- Khi công ty X đã có trong danh sách công ty làm việc, **quản trị viên công ty X** cấp hoặc gỡ vai trò
  của công ty X cho người đó. Họ chỉ thấy và chỉ thao tác được vai trò của công ty mình.
- Quyền hiệu lực = hợp các quyền của những vai trò người đó có **tại công ty đang làm việc**.

### 5.3 Mã quyền
- Kiểm quyền ở mọi nơi bằng **mã**, không bằng tên, không bằng id.
- Tên tiếng Việt, mô tả, nhóm chỉ để hiển thị, sửa thoải mái.
- Dạng mã: `phân_hệ.đối_tượng.hành_động`. Hành động lấy từ bộ cố định
  `view · create · update · delete · approve · export · print`, chỉ thêm từ mới khi thật cần.
  Mã **không** chứa phạm vi và **không** chứa nền tảng.

### 5.4 Danh mục quyền khai trong code
- Mỗi phân hệ khai quyền của mình trong code: mã, tên, Nhóm phân hệ, Phân hệ, Chức năng, loại
  (Xem / Thao tác / Duyệt), các cấp phạm vi được phép, quyền phụ thuộc, nền tảng áp dụng.
- Lệnh `permission:sync` chạy khi deploy, khớp theo **mã**: thêm mới, cập nhật thông tin hiển thị.
  Quyền bị bỏ khỏi khai báo thì **đánh dấu ngừng dùng, không xoá**.
- Không có màn tạo quyền. Quản trị viên chỉ ghép quyền vào vai trò.

### 5.5 Một mã chung cho ERP và HRM
- Một chức năng có ở cả 2 nền tảng thì dùng **chung một mã**. Cấp một lần là có hiệu lực ở cả 2.
- Mỗi quyền có nhãn **Nền tảng áp dụng**, lọc được trên màn hình. Khi tắt ERP chỉ cần đổi nhãn,
  không phải chuyển dữ liệu.
- Bỏ việc tách 2 bộ quyền theo guard `web`/`api`. Các cặp quyền trùng nghĩa giữa ERP và HRM nhập làm một.
- User **chấp nhận** hệ quả: trong lúc HRM còn đang test, ai có quyền ở ERP sẽ tự có quyền ở bản HRM
  của cùng chức năng.

### 5.6 Phạm vi dữ liệu
- **Gộp trong đợt này.** Các quyền "Xem … theo X" (khoảng 470 ở ERP, cùng các biến thể đuôi mã ở HRM) thành **một quyền**.
  Phạm vi chọn khi gán quyền cho vai trò.
- Mỗi quyền khai rõ những cấp được phép. Cấp cao bao gồm cấp thấp.
- Quyền Xem có phạm vi. Quyền Thao tác chỉ bật/tắt. Quyền Duyệt có phạm vi khi chức năng cần
  (như mockup).
- **Không có cấp "Cá nhân".** Người dùng **luôn xem được phiếu của chính mình**, đó là quyền nền, không cần
  cấp. Khi chuyển đổi, khoảng 58 quyền ERP dạng "… theo nhân viên / cá nhân / của mình" không còn mã riêng.
  Vai trò chỉ có biến thể đó thì không nhận phạm vi nào, nhưng người dùng vẫn thấy phiếu của mình như trước.
  **"Phiếu của mình" xác định qua `created_by`** (user chốt).
- Vai trò có quyền Xem mà không có biến thể "theo …" nào: **builder liệt kê ra khi làm, user quyết** phạm vi
  cho từng trường hợp. Không tự gán.
- **Quyền Thao tác không đi theo phạm vi Xem.** Ràng buộc ai được sửa/xoá bản ghi nào đã nằm riêng trong code
  của từng chức năng và giữ nguyên. Giai đoạn 4 chỉ đổi đường **đọc** (danh sách, xem chi tiết, báo cáo, dashboard)
  và quyền Duyệt có phạm vi. Không đụng vào ràng buộc ghi.
- **"Tổng công ty" = xem dữ liệu gộp mọi công ty**, dù vai trò chỉ thuộc một công ty. Công ty của
  vai trò quyết định *ai được cấp, cấp ở đâu*. Phạm vi quyết định *thấy dữ liệu tới đâu*.
- **Quản trị viên công ty nào cũng cấp được mọi phạm vi, kể cả "Tổng công ty"**, cho vai trò của công ty mình.
  Không có quyền riêng để cấp cấp này, không giới hạn "chỉ cấp tới mức mình có". User chấp nhận việc công ty B
  có thể mở dữ liệu gộp cho người của B. Cô lập giữa các công ty ở đây là cô lập **vai trò và việc cấp vai trò**,
  không phải cô lập dữ liệu khi đã có phạm vi Tổng công ty.

### 5.7 Super Admin
- **Bỏ qua-mặc-định ở cả 2 nền tảng.** Gỡ `Gate::before` của ERP. Khoảng 224 chỗ `hasRole('Super Admin')` đổi sang kiểm theo mã.
- Khi chuyển đổi, gán sẵn cho (các) vai trò Super Admin **đủ mọi mã quyền** hiện có, để không ai mất quyền.
- Từ đó trở đi, quyền mới **không** tự đến tay Super Admin, phải tick như mọi vai trò khác.

### 5.8 Triển khai
- Làm đủ 4 giai đoạn, **test ổn cả 4 rồi mới đưa lên prod một lần**. Không đưa lên từng giai đoạn.

## 6. Màn hình

Nền thiết kế: mockup `.plans/demo-man-hinh-ke-toan/demo/phan-quyen.html` (+ `assets/permissions.js`).
Bản ma trận `phan-quyen-matrix.html` không dùng. Màn đặt trong menu Quản trị (`components/subsystem-menu/admin.js`).

**Danh sách vai trò**
- Như mockup: STT, Vai trò, Quyền đang có (bấm mở popup), Trạng thái, Người sửa, Cập nhật, Thao tác
  (Phân quyền / Sửa / Lịch sử / Xoá).
- Chỉ hiện vai trò của **công ty đang làm việc** của quản trị viên.

**Màn gán quyền cho một vai trò**
- Băng tiêu đề hiện tên vai trò và công ty, công ty cố định, không chọn được.
- Bộ lọc: Nhóm phân hệ, Phân hệ, Chức năng, Loại quyền (Xem/Thao tác/Duyệt), **thêm Nền tảng (ERP/HRM)**.
- **Tìm nhanh** theo tên **và mã** (mockup mới tìm theo tên). Khi tìm, phân hệ chứa kết quả tự mở.
- Cây quyền: Nhóm phân hệ, rồi Phân hệ, rồi Chức năng, rồi Quyền. Mỗi dòng hiện **mã** cạnh tên và nhãn nền tảng.
  Quyền Xem/Duyệt có ô chọn phạm vi với những cấp hợp lệ.
- Có chọn hoặc bỏ cả nhóm, cả phân hệ. Có Mở tất cả / Thu gọn.
- Có bảng tổng hợp bên phải, đếm quyền đã phân.
- Quyền phụ thuộc: tick quyền Thao tác thì tự tick quyền Xem tương ứng.

**Quản lý tài khoản**
- Quản trị viên công ty chính khai danh sách công ty làm việc.
- Quản trị viên từng công ty cấp hoặc gỡ vai trò của công ty mình.

**Lịch sử**
- Ghi mọi thay đổi: quyền của vai trò, cấp/gỡ vai trò, thêm/gỡ công ty làm việc. Ghi ai, lúc nào, trước và sau.

Mọi nhãn trên màn hình dùng chữ **Vai trò**.

Màn phân quyền cũ của ERP (`common/roles/*`) và HRM (`pages/timesheet/setting/roles/*`, `pages/human/roles/*`) được gỡ.

## 7. Giai đoạn

| # | Giai đoạn | Nội dung chính |
|---|---|---|
| 1 | Nền dữ liệu + kiểm theo công ty | Khai danh mục quyền trong code, mã cho đủ khoảng 1.860 quyền, gộp cặp trùng ERP/HRM. `permission:sync` theo mã. Tách 52 role dùng chung thành vai trò theo công ty, thêm tiền tố. Vai trò mang `company_id`. Mọi đường kiểm quyền lọc công ty đang làm việc. |
| 2 | Màn quản lý mới | Danh sách vai trò, màn gán quyền, quản lý tài khoản (công ty làm việc + cấp vai trò), lịch sử. Gỡ màn cũ ở 2 nền tảng. |
| 3 | Kiểm quyền theo mã | Đổi khoảng 6.700 chỗ kiểm theo tên sang mã ở ERP, hrm-api, hrm-client (BE, FE, menu `isShow`, JWT claim, route middleware). Dùng bảng đối chiếu tên → mã + script, rồi soát tay. |
| 4 | Gộp phạm vi dữ liệu | Thay các chuỗi `if/else can('… theo X')` bằng một cách hỏi chung "phạm vi của quyền P cho người này là gì". Làm lần lượt từng phân hệ. |

Thứ tự trên là thứ tự làm. Cả 4 lên prod cùng lúc (mục 5.8).

| # | Folder con | Trạng thái |
|---|---|---|
| 1 | `gd1-nen-du-lieu/` | code Task 0–12 xong + review cuối + diễn tập trên bản sao prod 26/10 (worktree `wt-rbac`, nhánh `rbac`, CHƯA commit). Xem `gd1-nen-du-lieu/runbook-go-live.md`, `bao-cao-dien-tap/playwright.md` |
| 2 | (tạo khi bắt đầu) | chưa |
| 3 | (tạo khi bắt đầu) | chưa |
| 4 | (tạo khi bắt đầu) | chưa |

## 8. Chuyển đổi dữ liệu (yêu cầu kết quả, cách làm để builder quyết)

- **Quyền:**
  - Mỗi quyền hiện có ở cả 2 guard có đúng một đích: một mã mới, hoặc gộp vào mã khác.
  - Có **bảng đối chiếu** (tên cũ + guard cũ → mã mới + phạm vi) để user duyệt trước khi chạy. Bảng đối chiếu
    là tài liệu, nằm trong `.plans/`.
  - Các nhóm quyền "Xem theo X" gộp thành 1 mã. Vai trò đang có quyền nào thì nhận **phạm vi cao nhất** trong số các biến thể đã có.
- **Vai trò:**
  - Role chỉ có 1 công ty: gắn công ty đó.
  - Role nhiều công ty: tách thành mỗi công ty một vai trò, bộ quyền lấy theo `role_has_permissions` của công ty đó,
    người được gán lấy theo `employee_has_roles.company_id`.
  - Role chứa quyền cả 2 guard: gộp vào một vai trò.
  - Đặt tên theo quy tắc tiền tố mã công ty.
- **Kiểm chứng:** viết script so sánh quyền hiệu lực trước và sau chuyển đổi cho **từng tài khoản × từng công ty**.
  Chênh lệch phải bằng 0, trừ phần cố ý mất do bịt rò công ty. Phần đó liệt kê ra để user xem.
- Chạy được nhiều lần trên bản sao DB prod để tập dượt trước ngày lên.

### 8.1 Quyết định của Claude, user chưa duyệt riêng (soát khi đọc)

- **Mốc "trước" cho script so sánh** là quyền theo đúng công ty: vai trò người đó có tại công ty C, quyền
  của vai trò tại C (cách `canInCompany` đang kiểm). Mốc này không lấy theo hành vi rò hiện nay. Phần quyền
  người dùng đang được hưởng nhờ rò thì liệt kê riêng thành "mất do bịt rò".
- Phần **được thêm** do gộp mã ERP/HRM (mục 5.5) bị loại khỏi điều kiện "chênh lệch = 0", nhưng liệt kê
  riêng thành "thêm do gộp nền tảng".
- **Quyền phụ thuộc** (user chốt phương án C): chỉ là hành vi giao diện khi sửa (tick Thao tác thì tự tick Xem).
  Chuyển đổi dữ liệu **không** tự bù quyền Xem còn thiếu. Builder xuất danh sách **vai trò × quyền Thao tác đang thiếu
  quyền Xem** để user duyệt từng dòng: bù hay giữ (có thể cố ý cho sửa chỉ qua hộp chờ duyệt / link thông báo).
- **Danh sách công ty làm việc ban đầu** = các công ty người đó đang có vai trò (`employee_has_roles.company_id`)
  ∪ `employee_infos.company_id`. **Công ty chính** = `employee_infos.company_id`.
  Một công ty được phép nằm trong danh sách mà người đó chưa có vai trò nào ở đó.
- Role **không gắn công ty nào và không ai được gán**: không chuyển, liệt kê ra cho user quyết định.
- Mọi `hasRole('<tên>')` khác Super Admin đổi thành kiểm theo mã quyền ở giai đoạn 3, vì tên vai trò sẽ đổi
  (thêm tiền tố).
- Builder phải tự dò và chuyển hướng mọi **dữ liệu đang trỏ tới role id hoặc tên quyền** (bước duyệt, người
  nhận thông báo, bảng cấu hình…) sang vai trò mới của đúng công ty. Danh sách đã dò ghi vào hồ sơ giai đoạn 1.
- Builder phải kiểm cả **nơi dùng ngoài 3 repo** (app TPE_APP, SSO, help site) có đọc claim `roles` hoặc
  `permissions` trong JWT, hoặc tên vai trò/quyền không. Có thì đưa vào phạm vi hoặc giữ lớp tương thích.

## 9. Ràng buộc

- Mọi việc đụng source (code, migration, seeder, chạy vào DB, commit) phải hỏi user và nhận câu "làm"
  riêng, nêu rõ repo, nhánh, file/bảng, DB đích (CLAUDE.md gốc). Duyệt tài liệu này **không** phải lệnh code.
- 3 repo: `ERP/TanPhatDev`, `HRM/hrm-api`, `HRM/hrm-client`. Chung một DB.
- Task đụng giao diện phải kiểm bằng Playwright, đo bằng số từ DOM.
- Test phân quyền luôn có cả ca có quyền và ca không quyền (chống fail-open), và ca khác công ty.
- spatie cache quyền ở HRM là 24h. Đổi quyền phải xoá cache. ERP để cache 0s.
- spatie hai bên khác bản (3.18 và 5.5). Nếu cách làm phụ thuộc vào package thì phải chạy được trên cả 2 bản,
  hoặc thay bằng lớp kiểm quyền của mình.

## 10. Để builder quyết

- Cách lưu: thêm `company_id` vào `roles` hay bảng riêng. Giữ hay bỏ spatie. Cấu trúc bảng phạm vi gán quyền.
- Định dạng file khai báo quyền và nơi đặt nó, sao cho cả ERP lẫn HRM cùng đọc được **một nguồn**.
- Cách đặt mã cụ thể cho từng phân hệ, miễn theo quy tắc mục 5.3.
- Cách hiện thực câu hỏi "phạm vi của quyền P" ở BE và FE.
- Chia nhỏ từng giai đoạn thành task, viết test.
- Nhánh/worktree nào dùng cho đợt này. Lưu ý: đợt này không lên prod theo giai đoạn, nên không làm thẳng trên `gop_db`.

## 11. Rủi ro

- Khối lượng giai đoạn 3–4 rất lớn và trải 3 repo. Trong lúc làm, `gop_db` vẫn chạy tiếp các feature khác
  và sinh thêm chỗ kiểm theo tên, nên phải đối chiếu lại ngay trước khi lên.
- Gộp quyền ERP/HRM có thể ghép nhầm 2 quyền tên giống nhưng nghĩa khác. Bảng đối chiếu phải được user duyệt.
- Bịt rò công ty sẽ làm một số người mất quyền họ đang (vô tình) dùng. Cần danh sách để báo trước.
