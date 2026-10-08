---
name: erp-to-hrm-screen
description: Dùng khi chuyển/port một màn hình từ ERP (Laravel + AngularJS, TanPhatDev) sang HRM (Nuxt + Vue, hrm-client) — kể cả khi chỉ dựng lại 1 phần màn, thêm màn danh sách/chi tiết/form theo mẫu ERP, hoặc rà lại màn đã port xem có lệch quy chuẩn UI không.
---

# Chuyển màn ERP → HRM

## Vấn đề skill này giải

Màn ERP viết bằng AngularJS + Blade, không có quy chuẩn UI thống nhất. Khi port sang HRM, lỗi
lặp lại nhiều nhất **không phải lỗi nghiệp vụ** mà là lỗi UI: quên mixin ghi nhớ bộ lọc, tự dựng
badge riêng, nút sai màu/sai thứ tự, thiếu Cấu hình cột, thông báo tự chế câu mới, cột căn lề lung tung.

Skill này khoá 3 thứ lại:
1. **Quy trình 6 bước** — làm đúng thứ tự thì không sót phần nào.
2. **Khuôn màn mẫu** — copy pattern từ màn Danh mục khách hàng, không tự phát minh.
3. **Checklist tự kiểm** — chạy trước khi báo xong.

## Nguyên tắc gốc

> **Màn HRM phải trông như các màn HRM khác, KHÔNG phải như màn ERP gốc.**
> ERP là nguồn của **nghiệp vụ** (cột nào, lọc gì, hành động nào, ai được làm).
> HRM là nguồn của **giao diện** (component nào, màu gì, thứ tự nào).
> Bê nguyên UI của ERP sang là sai, kể cả khi "ERP đang làm thế".

---

## Quy trình 6 bước

### Bước 1 — Khảo sát màn ERP gốc (chỉ lấy nghiệp vụ)

Đọc file ERP và ghi ra **bảng nghiệp vụ**, chưa động tới code HRM:

| Cần ghi | Lấy ở đâu trong ERP |
|---|---|
| Danh sách cột + ý nghĩa | blade `datatable` / `columns` trong file js |
| Trường lọc + kiểu (text/select/date/range) | form filter trong blade |
| Hành động mỗi dòng + **điều kiện hiện/ẩn** | cột action trong blade + `if` quyền |
| Quyền dùng cho từng hành động | `@can` / `hasPermission` trong blade + controller |
| Trạng thái & nhãn tiếng Việt | hằng số/`status_text` ở model |
| Xuất/In/Import có không | nút trên toolbar |
| Vị trí trong menu ERP (tất cả các chỗ) + tham số trên link | `grep "route('<TenRoute>.index'" resources/views/layouts/topmenubar.blade.php` |

⚠️ **Ghi cả điều kiện ẩn nút**, không chỉ tên nút. Lỗi hay gặp nhất là port nút nhưng bỏ điều kiện.

Đọc code ERP, đừng suy từ giao diện/nhãn (đều đã dính thật):
- ERP gán sai link ≠ ERP không có chức năng — mở route + controller + blade rồi mới kết luận (#11192).
- Đọc `ng-click` của nút, không suy từ nhãn: "Không duyệt" ở màn tạo phiếu xuất giữ là `submit(3)` = lưu nháp (#11370).
- Số hiện trên ERP mà DB = 0 → tìm trong class JS (vd `if (!this._extend_qty) this._extend_qty = …`), đừng đi tìm bug BE (#11276).
- QA báo "không sửa được X" → xem blade ERP ô đó là input hay chữ trước khi sửa; nhiều khi ERP cũng không cho (#11278).
- Không tự thêm nút/chức năng ERP không có, TRỪ bộ bắt buộc của HRM (Xuất Excel, Cấu hình cột, Lịch sử,
  Lưu và tiếp tục). Muốn thêm gì khác thì hỏi user; nhãn nút phải đúng việc nó làm.
- **ERP thường có NHIỀU action cho cùng một truy vấn, khác phạm vi theo vị trí menu** — vd
  `expiringBorrow` (phân hệ Thông báo, chỉ phiếu `created_by = mình`) và `accountingExpiringBorrow`
  (Kế toán kho, cả công ty). Port nhầm bản cá nhân thì màn hụt dữ liệu (6 phiếu thay vì 74). Chọn
  action ứng với **mục menu chính** (link có `all` — xem Bước 2).
- **Cột / bảng ERP "nói dối"** — kiểm bằng dữ liệu thật trước khi join hoặc tin cột lưu sẵn: `supplier_id`
  trỏ `customers.id` (model `Supplier` của ERP khai `$table = 'customers'`, bảng `suppliers` rỗng);
  `supplier_name` lưu sẵn toàn NULL; `cost_id` kiểu varchar join `costs.id` kiểu số. Thêm các bẫy bảng
  ERP khác: `.plans/gop-db/design.md` mục "Bẫy khi port".
- **Đối chiếu quyền bên ERP bằng tài khoản Super Admin là vô nghĩa** — `Gate::before` cho qua mọi quyền,
  không bao giờ thấy trường hợp thiếu quyền. Test âm bằng tài khoản thường (hoặc tinker
  `Auth::guard('web')->setUser(...)` rồi gọi thẳng controller).

### Bước 2 — Chốt phân hệ, route, quyền, phạm vi dữ liệu

- Màn thuộc phân hệ nào (theo sheet quy hoạch phân hệ — xem "Đặt mục menu" dưới) → route `/<phân-hệ>/<slug>`.
- Có cần phân quyền theo cấp (công ty / phòng ban / bộ phận) không → **hỏi user**, đừng tự quyết.

#### Quyền: TẠO QUYỀN MỚI ở HRM (user chốt 06/10/2026)

- **Không dùng lại quyền ERP.** Tạo quyền mới `guard_name = 'api'` rồi gắn middleware
  `checkPermission:<Tên quyền>` bình thường như CLAUDE.md quy định. Lý do dùng lại quyền ERP bị hỏng
  (docblock `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php`):
  - quyền ERP mang `guard_name = web` → `hasPermissionTo($name)` (không truyền guard) ném `PermissionDoesNotExist`;
  - vai trò gán từ thời ERP nằm trong `employee_has_roles` với `model_type = App\Employee`, mà
    `checkPermission` đọc qua `getAllPermissions()` của spatie (lọc theo `model_type` của model HRM) →
    **bỏ sót**, người có quyền thật vẫn 403;
  - trùng TÊN quyền giữa bản ERP và bản HRM.

  Quyền mới do admin gán lại trong HRM nên không dính 3 bẫy trên. Màn cũ đang tự gate bằng trait
  `ChecksEmployeePermission` (không gắn middleware) là cách chữa cháy khi còn dùng quyền ERP — màn mới
  không chép.
- **Khai vào seeder chung** `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (lần build nào
  cũng chạy lại seeder này). KHÔNG tạo seeder quyền riêng cho từng màn (kiểu
  `BuyServiceRequestPermissionSeeder` — màn cũ, đừng chép).
- **`type` của quyền = `permissionType` của PHÂN HỆ CHÍNH** của màn (tra trong
  `hrm-client/components/subsystems.js`), không theo module chứa code — màn Bán hàng nằm ở
  `Modules/Finance` vẫn là `type` của Bán hàng. Màn phân quyền (`components/setting/Permission.vue`) gom
  quyền theo `type` → thiếu `type` là quyền **không hiện ở phân hệ nào**, admin không gán được; sai `type`
  là quyền nằm nhầm phân hệ.
- **Không tự gán quyền mới cho vai trò cũ** — admin tự phân quyền lại khi chuyển sang HRM.

#### Phân hệ chính & phạm vi dữ liệu

Một màn có thể nằm ở nhiều phân hệ. Bên ERP, các lối vào khác nhau phân biệt bằng **tham số trên URL**
(`?type=all`, `?permission=all`, `?type=waiting`…):
- **Phân hệ chính** = phân hệ có mục menu trỏ màn danh sách với tham số **`all`**. Quyền của màn khai
  `type` theo phân hệ này, và **phạm vi dữ liệu dựa vào quyền ở phân hệ chính**.
- Các phân hệ khác là **lối vào phụ** với tham số riêng (vd `?type=waiting` = danh sách phiếu chờ mình
  duyệt). Giữ nguyên tham số khi khai menu HRM; chỉ thêm tham số khi trang thật sự đọc
  `$route.query.type` (đừng tự gắn `?type=all` cho trang không đọc nó).
- Màn con dùng chung controller/service với màn cha (vd chỉ khác cờ `expiring_only`) → **cờ phải
  `merge` ở BE** (override `scoped()` ở controller con), đừng để FE gửi — quên 1 lần là màn con thành
  bản sao màn cha mà không báo lỗi gì.

Quy tắc phạm vi đã dính QA:
- Phiếu người xem **đã đóng dấu duyệt/từ chối** vẫn phải hiện với họ (đừng chỉ "người lập thấy" —
  #11519, #11239).
- Super admin / quyền tổng công ty không bị bó `company_id` của người đăng nhập (#11529). Ô lọc **Công ty**
  chỉ hiện với người xem được mọi công ty: BE trả `meta.is_all_company`, FE dựa vào đó; BE chỉ đọc
  `company_id` của request trong nhánh "xem mọi công ty", người khác khoá cứng công ty mình (#11524).
- **Không port tham số xem chéo công ty** kiểu `?company=` của ERP mà không UI nào gửi — để lại là lỗ
  xem chéo công ty.
- `where('company_id', $companyId)` với `$companyId = null` → Laravel dịch thành `IS NULL`, kéo ra phiếu
  rác không thuộc công ty nào. Null thì `whereRaw('1 = 0')`; so "cùng công ty" phải loại trường hợp 2
  vế cùng null.
- "Theo phòng ban" của HRM (phòng quản lý + phòng đang ngồi) rộng hơn ERP là **chủ ý** — ghi vào spec
  để QA khỏi báo nhầm.

#### Đặt mục menu: SHEET QUY HOẠCH trước, ERP để tham chiếu (user chốt 06/10/2026)

Thứ tự nguồn:
1. **Sheet quy hoạch phân hệ** (Google Sheet 5 nhóm, chốt 04/09/2026 — cách đọc gạch ngang / màu nền:
   `.plans/gop-db/quy-hoach-lai-menu-phan-he/design.md`) **+ bảng lỗi TPE**. Đây là nơi quyết định màn
   nằm ở phân hệ / nhóm nào và tên mục menu.
2. **Menu ERP** để tham chiếu: tên màn gốc, tất cả các chỗ đặt màn, **tham số trên link**.
3. **Một màn nằm ở nhiều phân hệ là bình thường** (chốt 25/09/2026) — vd Báo giá ở cả Bán hàng lẫn
   CSKH trước bán. Phân biệt lối vào bằng tham số trên link như mục trên.

Tên màn KHÔNG nói lên nó thuộc phân hệ nào. Màn "Báo giá dịch vụ" nghe như thuộc CSKH nhưng menu
ERP đặt nó ở **Kinh doanh → Báo giá → "Báo giá dịch vụ sửa chữa - bảo dưỡng - bảo trì" → "Danh sách
báo giá"**. Đặt nhầm thì người làm báo giá tìm mãi không ra (đã dính thật, user phải chỉ).

Cách quét mọi vị trí của route trong menu ERP:

```bash
grep -n "route('<TenRoute>.index'" resources/views/layouts/topmenubar.blade.php
```

Với mỗi kết quả, lần ngược lên tìm `ruby-list-heading` (tên nhóm) và `<a href="#">` (tên phân hệ).
Hai điều rút ra từ lần rà 5 màn của luồng dịch vụ:

1. **Một màn có thể nằm ở NHIỀU nhóm menu.** "Yêu cầu sửa chữa - bảo hành" xuất hiện ở 4 chỗ:
   Hàng hóa → Lắp đặt-BH-SC · Lắp đặt-BH-SC · CSKH → Kiểm tra bảo hành sửa chữa · **và** Kinh doanh
   → Báo giá. Bỏ bớt chỗ nào là một nhóm người dùng mất đường vào quen thuộc.
2. **Giữ nguyên tham số trên link.** Cùng màn nhưng ERP trỏ `?permission=waiting_create_quotation`
   ở nhóm Báo giá và `?permission=all` ở nhóm CSKH — hai phạm vi dữ liệu khác nhau (skill
   `list-page` §3d). Copy link mà bỏ tham số là hỏng ý nghĩa mục menu.

**File menu bên HRM — KHÔNG chỉ có 1 nguồn.** Menu Bán hàng sinh từ `components/subsystem-menu/sale-hub.js`
(cả hub lẫn cây bên trái), nhưng các phân hệ khác nằm ở `components/subsystem-menu/*.js`,
`components/default-menu/*.js`, `components/menu.js`, `components/menu-sidebar.js`, và có chỗ viết cứng
(`SettingSlidebar.vue`). Dời màn sang phân hệ khác → grep link ở **tất cả** các file này. Nhiều nhóm đã
khai sẵn tên màn từ trước — **kiểm xem có sẵn chưa rồi hãy thêm mới**, đừng tạo mục trùng do sơ suất.

Khi khai mục menu:
- **Màn trong `sale-hub.js` (Bán hàng) có 3 dạng** (docblock đầu file): chuỗi trần = chưa có link, bấm báo
  "đang phát triển" · `{ n, erpPath }` = màn còn bên ERP (cây menu bên trái mở ERP ở tab mới, hub vẫn báo
  "đang phát triển") · `{ n, link }` = màn HRM đã port. Port xong thì đổi `erpPath` → `link`.
  Các phân hệ khác (`subsystem-menu/*.js`, `menu.js`…) dùng khuôn `{ label, icon, link, isShow, subItems }`;
  mục **không có `link`** render xám mờ. Cờ `external` / `erpGhost` trong `subsystems.js` là cờ cấp
  **PHÂN HỆ** (cả phân hệ nằm bên ERP), không dùng cho từng mục.
- **Khai màn ở phân hệ thứ 2 thì bê nguyên `isShow`** (quyền) từ phân hệ chính — thiếu là lộ menu cho
  người không có quyền. Cây Bán hàng đọc map `SALE_LINK_PERMISSIONS`; mục mới nên khai `isShow` ngay
  trong mục.
- **KHÔNG đổi nhãn mục menu đã có** khi không được yêu cầu: nhãn là một phần của `menuKey`
  (`utils/menuVisibility.js`) — đổi nhãn là mất cấu hình bật/tắt đã lưu; nhãn menu cũng là **tiêu đề
  tab trình duyệt** (`screenTitleOf` trong `subsystems.js`). Giữ tên ngắn — nhãn dài tràn menu ngang.

### Bước 3 — Dựng khung theo khuôn màn mẫu

Đọc `references/khuon-man-mau.md` rồi dựng 4 file theo đúng cấu trúc:
`index.vue` (danh sách) · `add.vue` · `_id/edit.vue` · `_id/index.vue` + 1 `XxxForm.vue` dùng chung.

**Trước khi tự viết bất kỳ thành phần UI nào** (badge, tooltip, popup, upload, kéo thả, phân trang,
biểu đồ…) → grep xem project đã có chưa. Đã có ≥ 1 màn làm đúng thì bám theo màn đó và ghi vào
`plan.md`: "copy pattern từ `<file:dòng>`".

### Bước 3b — Hàm nghiệp vụ DÙNG CHUNG: tách ra để màn sau xài lại, y như ERP

ERP tuy lộn xộn về UI nhưng phần **nghiệp vụ thì gom rất tốt**: `Product::getAccountingStockDetail()`,
`Product::getStockByContract()`, `ProductStockService::getStockQty()`… được **hàng chục màn gọi
chung**. Khi port sang HRM, nếu mỗi màn tự chép một bản thì vài tháng sau các bản lệch nhau và
không ai biết bản nào đúng.

**Nguyên tắc (user chốt 2026-08-22): port màn nào cũng phải hỏi "hàm này màn khác có xài lại không?"**

Cách làm:

1. **Trước khi viết** một phép tính nghiệp vụ (tồn kho, tồn giữ, công nợ, giá, quy đổi đơn vị,
   phạm vi quyền…) → **grep xem HRM đã port hàm đó chưa**:
   ```bash
   grep -rn "in_stock\|getAccountingStockDetail" hrm-api/Modules/*/Services/
   ```
   Đã có rồi thì **gọi lại**, tuyệt đối không chép.

2. **Nếu hàm đã có nhưng đang `private` / bị khoá trong service của màn khác** → **tách ra service
   dùng chung**, đừng chép bản thứ hai. Đây là sửa file màn khác đang chạy nên **phải hỏi user
   trước** (CLAUDE.md), và **test lại màn cũ** ngay sau khi tách.

3. **Nếu là hàm mới**, đặt nó ở service theo *chủ đề nghiệp vụ*, KHÔNG theo tên màn:
   - đúng: `AccountingStockService` (tồn kho), `PrepickStockService` (tồn hàng giữ)
   - sai: `PrepickExtendRequestService::tinhTonKho()` — tên màn thì màn khác không ai dám gọi

4. **Docblock của service dùng chung phải liệt kê "Nơi đang dùng"** — để lần sau sửa còn biết
   phải thử lại những màn nào.

5. Service dùng chung là **chỗ DUY NHẤT** được chạm bảng của nó. Ví dụ đã áp:
   `PrepickStockService` là nơi duy nhất ghi `prepick_details` / `prepick_logs`.

**Ví dụ thật (2026-08-22, màn Yêu cầu gia hạn hàng giữ):** cần cột "Có thể giữ" = `in_stock`. Grep
ra `ProductTransferRequestService::accountingStockDetail()` đã port đúng hàm ERP nhưng để `private`.
→ tách sang `AccountingStockService::detail()`, màn Chuyển hàng gọi qua constructor injection, màn
gia hạn gọi lại. Nếu chép bản thứ hai thì đã có **2 bản 170 dòng** cùng tính tồn kho.

⚠️ **Đừng nhầm 2 khái niệm tồn** — đặt tên service cho rõ ngay từ đầu:
| Service | Là gì | Bảng |
|---|---|---|
| `AccountingStockService` | tồn **KHO** — hàng còn trong kho | `accounting_stocks` |
| `PrepickStockService` | tồn **HÀNG GIỮ** — đang giữ cho khách | `prepick_details` |

### Bước 4 — Áp quy tắc chung SRS

Đọc `references/srs-quy-tac-chung.md` — bảng tra đầy đủ: cột mặc định, sort, tìm kiếm, phân trang,
căn lề, màu nút, màu trạng thái, thứ tự nút, định dạng dữ liệu, bộ thông báo QLDA_001…025.

**Thông báo phải lấy nguyên văn từ bảng QLDA**, không tự chế câu mới.

### Bước 5 — Đối chiếu ngược với ERP

Mở song song màn ERP và màn HRM vừa dựng, đối chiếu **từng dòng bảng ở bước 1**:
- Đủ cột chưa? Cột ERP có mà HRM không có → thêm vào, mặc định **ẩn** trong Cấu hình cột nếu ít dùng.
- Đủ trường lọc chưa?
- Đủ hành động chưa, **và điều kiện hiện/ẩn có khớp không**?
- Đọc ERP ở **nhánh/cổng đang chạy thật** và xem `git log` của bảng/blade ERP: ERP vẫn đổi sau khi
  HRM port xong (vd 26/08/2026 ERP thêm cột Quá hạn / Ngày BGNT vào khai báo đầu kỳ công nợ — HRM
  thiếu tới khi QA bắt). Đối chiếu cả ô ERP **không** có: HRM thừa ô lọc / cột cũng bị QA báo lỗi.

### Bước 5b — Đối chiếu NGANG với 2-3 màn HRM đã qua QA (bắt buộc)

Phần lớn lỗi UX/UI QA báo sau khi port là **"màn này làm khác các màn khác"**, không phải lỗi
nghiệp vụ. Checklist dưới không thể liệt kê hết mọi chi tiết, nên trước khi báo xong:

1. Chọn 2-3 màn **cùng loại** đã qua QA (cùng phân hệ, cùng kiểu phiếu duyệt/danh mục/báo cáo).
2. Với mỗi khối của màn mới (header khối đầu, khối file đính kèm, bảng chi tiết, footer nút, lịch
   sử, popup chọn, xuất Excel, bản in, câu toast…), mở màn mẫu xem nó dùng **component/helper nào**
   rồi dùng ĐÚNG cái đó — không tự dựng bản mới dù "trông giống".
3. Ghi vào báo cáo/STATUS: "đã bám màn X ở khối Y". Không chỉ ra được màn mẫu = chưa đối chiếu.

Khi QA chốt một quy ước MỚI trong lúc sửa lỗi: cập nhật luôn skill này + dùng skill
`new-screens-sweep` rà đồng loạt các màn khác, đừng chỉ sửa màn bị báo.

### Bước 6 — Chạy checklist tự kiểm + verify trình duyệt

Chạy hết checklist bên dưới, rồi mở trình duyệt bấm thật. **Không báo xong khi chưa bấm thật.**

- **Chụp ảnh** danh sách / form / chi tiết rồi đặt cạnh màn chuẩn cùng phân hệ. Đọc DOM đủ cột/nút vẫn
  có thể sai cả vỏ trang (thiếu `layout: 'default-sidebar'` ở `index.vue` → mega menu ngang kiểu ERP).
- Bấm thử ô lọc bằng Playwright: chờ **≥ 3 giây** sau mỗi lần đổi (API dev chậm, đọc sớm ra kết quả của
  lần lọc trước). Nghi ô lọc không ăn → gọi thẳng API (curl) so `total` trước khi kết luận.
- QA báo "thiếu ô lọc / thiếu ô Công ty so với ERP" → kiểm `filter_customizations` và quyền HRM
  (`employee_has_permissions` / `employee_has_roles`) của **chính tài khoản test** trước khi sửa code.
- Trang nội dung ngắn có **khoảng xám lớn dưới nội dung, trước footer** → KHÔNG phải lỗi của màn: layout
  `default-sidebar` ép `body` cao bằng menu trái (đo ngày 10/08/2026: `body` min-height 1550px > `.content-page`
  1219px). Kiểm lại bằng cách so `getComputedStyle(document.body).minHeight` với chiều cao `.content-page`
  trước khi kết luận. Đừng sửa padding/chiều cao form để "lấp" (user đã chốt để nguyên; muốn sửa là sửa
  layout dùng chung, phải hỏi).

---

## Checklist tự kiểm (chạy trước khi báo xong)

### A. Màn danh sách
- [ ] Có đủ 4 mixin: `PageTitleMixin`, `CheckPermission`, `filterStateMixin`, `columnCustomizationMixin`
- [ ] `localStorageKey`, `columnScreenKey` và prop `table` của `V2BaseSmartFilterPanel` **duy nhất**,
      không trùng màn khác (màn con `extends` màn cha → `:table="columnScreenKey"`, #11515)
- [ ] Có `columnCustomizationMixin` thì phải đặt `<ColumnCustomizationModal v-if="columnFieldsLoaded">`
      trong template + gọi `loadColumnFields()` ở `mounted` — mixin không tự render, thiếu là nút Cấu hình
      cột bấm không có gì (#11513). Cột ẩn mặc định khai `isVisible: false`
- [ ] Cấu hình cột lưu ở bảng key-value **`user_column_settings`** (1 dòng / user / `screen_key`) — thêm màn
      mới **KHÔNG cần migration**, chỉ cần `columnScreenKey` mới (`[a-z0-9_]`, duy nhất). KHÔNG thêm cột vào
      bảng cũ `column_customizations` (kiểu cũ mỗi màn 1 cột JSON + `$casts` — đã bỏ, dữ liệu đã chuyển sang)
- [ ] Cột mặc định có: STT, Mã, Tên, Người tạo, Ngày tạo, Trạng thái (nếu có), Hành động (+ Khách hàng /
      Loại phiếu nếu màn có) → skill `list-page` §6
- [ ] Mọi nhãn (cột, ô lọc, trường form, cột xuất FE + `ExportColumnRegistry` BE, bản in, popup chọn) là
      **"Người tạo" / "Ngày tạo"** — CẤM "Người lập" / "Ngày lập" bê từ ERP (#11240, #11271, #11400) → `list-page` §6
- [ ] Mã và Tên là **2 cột riêng**; cột Mã là `<nuxt-link>` thật (chuột phải mở tab mới được)
- [ ] Sắp xếp mặc định **giảm dần theo ngày tạo**
- [ ] Bảng trống hiện dòng "Không có dữ liệu phù hợp", không phải bảng rỗng
- [ ] Sort bật cho cột mã / tên / tiền / ngày; sort cột mới hủy sort cột cũ
- [ ] `V2BaseDataTable` có `@sort` thì **bắt buộc truyền `:sortBy` + `:sortDirection`** (thiếu là không bao
      giờ sắp giảm dần, mũi tên đứng im); `key` cột sortable trùng đúng tên trường BE trong
      `SORTABLE_COLUMNS` — lệch thì BE âm thầm sort theo `id` (#11091, #11098, #11343)
- [ ] Phân trang mặc định 10, chọn được 5/10/20/50/100, đổi số dòng nhảy về trang 1
- [ ] Không gọi API lặp: `page`/`per_page` KHÔNG nằm trong `filters`; meta gán qua `Number()` và đọc
      camelCase (`currentPage`/`perPage`) với fallback giá trị hiện tại (không fallback `1`); deep watcher
      `filters` so với **bản sao sâu tự giữ** (`oldVal` trùng object với `newVal`). Kiểm bằng đếm request
      trên tab Network: vào màn / đổi trang / đổi số dòng / sort đều chỉ 1 request
- [ ] Ô lọc dạng chọn tự tìm ngay khi chọn; ô gõ tay chờ Enter/nút Tìm kiếm
- [ ] **Bật `floating`** trên `V2BaseSmartFilterPanel` — mọi ô lọc cao 32px, nhãn nằm giữa ô khi
      rỗng và bay lên đè viền trên khi có dữ liệu (chuẩn chốt 07/09/2026, mẫu: màn Dự án TKT)
- [ ] Field gom nhiều ô (khối tổ chức, cặp cha-con...) đã khai `resetKeys` — panel dựa vào đó để
      biết nhãn có phải bay lên không
- [ ] Placeholder **không lặp lại nhãn** (`Chọn <X>` / `Nhập <X>` là SAI khi bật floating — nhãn
      đã nói rồi). Chỉ giữ khi nói thêm điều nhãn không nói: `Gõ để tìm khách hàng...`, `dd/mm/yyyy`
- [ ] Ô tìm nhanh: `Tìm theo <các trường BE thực sự lọc>` — không `Tất cả`, không `Chọn...`, không để trống.
      Ô tìm nhanh chỉ quét **mã / tên / nội dung của chính phiếu**; Người tạo / Người duyệt / Nhân viên
      luôn là **select ở bộ lọc nâng cao**, không gõ tìm nhanh (user chốt 06/10/2026, #11373)
- [ ] Options của bộ lọc nâng cao nạp trễ (khi mở panel) thì cũng phải nạp khi panel được **khôi phục ở
      trạng thái MỞ** từ localStorage (`if (!filterCollapsed) loadFilterOptions()` ở `mounted`) — đường đó
      không qua `toggleFilterPanel`, thiếu là dropdown rỗng, mất nhãn giá trị đang lọc
- [ ] Danh sách nhúng trong **TAB** (component con, `v-if`) không có `beforeRouteLeave` → `filterStateMixin`
      không lưu được bộ lọc khi đổi tab; tự lưu localStorage bằng khoá riêng của tab (#11390,
      `pages/assign/my-job/components/CustomerDemandsTab.vue`)
- [ ] Bảng danh sách dạng **cây 2 tầng** (dòng cha bấm mở dòng con): chép khuôn
      `pages/finance/prepick-stocks/index.vue` — nút tròn `.group-toggle-btn`, dòng con nền `#ecfdf3`, vạch
      trái `#86efac`, selector đủ nặng để ăn cả `td.sticky-col` (#11513 "đồng bộ bảng, icon, màu")
- [ ] **Có ô tìm nhanh + 2 nút Tìm kiếm / Làm mới nằm ngay hàng trên cùng** khi vừa vào màn (chưa bấm
      "Tìm kiếm nâng cao"). Grep `show-quick-search="false"` trong feature phải ra RỖNG — ERP không có ô
      này thì thêm param `keyword` ở BE (skill `list-page` mục ô tìm nhanh)
- [ ] Ô lọc tìm-từ-server (Khách hàng / NCC / Sản phẩm) dùng **`V2BaseSelectRemote`** kèm
      `height="32px"` + `minimumInputLength` + `initialOption`, KHÔNG tự chế autocomplete
- [ ] Mọi ô trong khối lọc đo ra **bằng nhau, chuẩn hiện hành `32px`** (biến `--ff-h`; hạ từ 36px
      ngày 22/09/2026 — xem skill `list-page`). Lệch hàng là quên truyền `height`
- [ ] Nút **Làm mới** xóa hết điều kiện **và tải lại danh sách** — `handleReset` gọi thẳng `loadData()`
      (+ `resetLoadDedupe?.()`), đừng trông vào watcher (watcher bỏ qua khi chỉ `keyword` đổi)
- [ ] Ô lọc nâng cao không lặp cột mà ô tìm nhanh đã quét; bỏ ô lọc thì dọn luôn giá trị cũ trong
      localStorage (`mergeKnownFilters`) kẻo bảng bị lọc ngầm → `list-page`
- [ ] **Bấm thật TỪNG ô lọc** rồi xem bảng có đổi không — đối chiếu param trên tab Network với
      `searchByFilter` của BE. Ô lọc sai tên key **không báo lỗi gì**, nhìn giao diện y như đúng
- [ ] Khối tổ chức khai đúng `company_id` / `department_id` / `part_id` / `employee_id` trong
      `initialStateForm` (Vue 2 không reactive với property chưa khai)
- [ ] Vào chi tiết rồi quay lại → **bộ lọc còn nguyên**
- [ ] Có nút Cấu hình cột; STT / Mã / Hành động **không tắt được**
- [ ] Panel lọc là **`V2BaseSmartFilterPanel` + schema `filterFields`** (KHÔNG phải
      `V2BaseFilterPanel` + slot `#advanced-filters` tự dựng tay) → mới có popup "Cài đặt bộ lọc"
- [ ] > 3 trường lọc → có popup "Cài đặt bộ lọc"; **≤ 3 trường** → hiện thẳng, bỏ khối nâng cao (quy ước
      HRM; văn bản SRS chỗ ghi "< 3" chỗ ghi "> 3" — theo dòng này)
- [ ] Bảng **tự dựng** `<table>` (báo cáo nhiều tầng tiêu đề, bảng trong popup chọn) KHÔNG có sẵn
      style của `V2BaseDataTable` (CSS của nó là `scoped`, không áp sang) → phải tự đảm bảo đủ 4 thứ
      giống màn danh sách: header dính khi cuộn (`thead` sticky), hover dòng `var(--sale-row-hover)`,
      icon sort xám `#9ca3af` 12px, ô "Số dòng/trang" chữ 12-13px cao 30px (QA #11558, #11569, #11572).
      Ưu tiên dùng `V2BaseDataTable` nếu bảng chỉ 1 tầng tiêu đề.

### B. Nút & hành động
- [ ] Mọi nút có **icon + text** (nút chỉ icon → dùng `V2BaseIconButton`)
- [ ] Thứ tự toolbar danh sách: Thêm mới → Import → Xuất → Cấu hình cột
- [ ] Thứ tự cột thao tác: Sửa → Xóa → menu "…"
- [ ] > 3 hành động → chỉ hiện 2 nút chính + nút "Hành động khác"
- [ ] **Bấm thật TỪNG nút trong cột Hành động** (kể cả nút trong menu "…") — `V2BaseRowActions`
      emit **chuỗi key**, handler phải `switch (action)`; so `action.key` là nút im ru mà không
      báo lỗi gì. Nút khai `to:` vẫn chạy nên nhìn qua tưởng màn không lỗi
- [ ] Nút không dùng được thì **ẩn hẳn** (`visible`/`v-if`), KHÔNG hiện xám
- [ ] Hành động ở màn **chi tiết khớp hệt** màn danh sách — cả danh sách nút lẫn điều kiện ẩn/hiện
- [ ] Nút màn chi tiết/form nằm trong `V2Footer`, không tự dựng khối nút
- [ ] `V2Footer` lệch quy tắc ở 3 cờ: `menu.print` ra nút In **primary**, `menu.reject_approve` ghi
      "Không duyệt", `menu.approve` tự bật popup xác nhận chung (màn tự `$confirm` thành 2 popup, validate
      chạy sau popup) → đưa In / Từ chối / Duyệt / Xóa vào slot `#custom-actions` (Xóa cũng vào slot để giữ
      thứ tự chính → phụ → nguy hiểm → Quay lại) (#11096, #11104) → `button-convention` §6c
- [ ] Nút ghi dữ liệu: `$safeLoadingStart/Finish` (trong `finally`) + `:interactable="!submitting"` + guard
      `if (this.submitting) return` — bấm đúp từng tạo bản ghi trùng (#11555–#11560) → `button-convention` §6b
- [ ] Hành động **Duyệt ở cột Hành động danh sách** chỉ điều hướng: `to:` mở màn chi tiết +
      `visible: item.is_can_approve`, icon `ri-checkbox-circle-line`, KHÔNG duyệt thẳng từ danh sách (#11273)
- [ ] Thao tác xong (Lưu nháp / Lưu / Gửi duyệt / Duyệt / Từ chối / Hủy / Xóa) → `markFormSaved()` rồi
      `$router.push(<danh sách>)`; "Quay lại" (`url-back`) trỏ về **nơi user đi vào** (#11107, #11192,
      #11193, #11236) → `list-page` §7.3
- [ ] Màu nút đúng nhóm — **nguồn duy nhất là skill `button-convention` mục 2b**, đừng nhớ theo
      checklist này: Tạo mới / Lưu / **Duyệt / Gửi duyệt** = `primary` teal (KHÔNG `status`, KHÔNG
      xanh lá, KHÔNG cam); **Lưu nháp** = `secondary` trắng + `ri-save-3-line`; Gửi duyệt icon
      `ri-send-plane-line`; Khóa = `primary status="warning"`; Xóa/Từ chối = `status="danger"`;
      Import = `secondary status="warning"`; Xuất = `secondary status="success"`.
      (Dòng cũ ghi "Duyệt = xanh lá, Gửi duyệt = cam" là SAI — đã gây lỗi QA #11548.)

### C. Hiển thị dữ liệu
- [ ] Trạng thái dùng `V2BaseBadge`, text từ `status_text` / `status_name` của BE (không map
      số→chữ ở FE), variant lấy qua helper chung `utils/statusBadgeVariant.js` — KHÔNG tự viết
      `statusPillClass()` + `<span class="status-pill">` cho từng màn
- [ ] **Màu trạng thái đúng nhóm SRS**: Nháp/Đang tạo = **XÁM**, Chờ duyệt = vàng, Đã duyệt = xanh,
      Từ chối/Không duyệt/Khóa = đỏ. Kiểm cả hằng `STATUSES` ở BE — ERP hay gán "Đang tạo" là
      `danger` (đỏ), bê nguyên sang là sai
- [ ] Căn lề đúng: STT/badge/hành động = giữa; số & tiền = phải; chữ & ngày = trái
- [ ] Ngày `dd/mm/yyyy`, ngày+giờ `dd/mm/yyyy HH:mm` (BE trả sẵn, FE không format lại)
- [ ] Số & tiền theo **chuẩn quốc tế `1,234,567.89`** — `,` ngăn nghìn, `.` phần thập phân
      (chốt 2026-08-26, thay cho kiểu Việt Nam chốt ngày 2026-08-22). Chi tiết:
      `print-page/SKILL.md` §2d (bản in) · `export-excel/SKILL.md` §1a (file Excel)
- [ ] Ô rỗng để **TRỐNG HẲN** (chốt 2026-08-22) — KHÔNG chèn `—`, `-`, `N/A`, `(không có)`.
      Trong `.vue` viết `{{ x || '' }}` (giữ `|| ''` để số `0` vẫn ra trống như hành vi cũ).
      ⚠️ Không đụng dấu `-` dùng làm **ký tự phân cách** (`name + '-' + position`). Xem
      `list-page/SKILL.md` §3b-3
- [ ] Chữ trong ô để **thường**, kể cả cột Mã — không `font-weight-bold`
- [ ] Chữ đỏ **chỉ** dùng cho lỗi validate / nút nguy hiểm / giá trị cũ trong lịch sử. Không dùng
      `.text-muted` cho chữ phụ trong khối `v2-styles` (bị ép thành đỏ) → `list-page` §3b-2 / §3b-2b
- [ ] Link sang chứng từ khác: màn đích **đã port sang HRM** thì `nuxt-link` tới HRM, KHÔNG link sang ERP
      (#11514); màn đích thuộc luồng khác (Quay lại bên đó cố định về list của nó) → `target="_blank"
      rel="noopener"` (#11373); trong form readonly bọc `.v2-linked-field` → `list-page` §7b
- [ ] Link sang màn **CHƯA port**: dùng helper `utils/erp-link.js` (`erpUrl`, mở tab mới), KHÔNG tự ghép
      `process.env.ERP_URL`. Nhiều loại chứng từ → bảng map HRM/ERP có sẵn: `utils/contract-link.js` +
      `components/finance/declare-debt/ContractCodeLink.vue`, `utils/stock-voucher-link.js` — port xong màn
      nào thì chuyển dòng đó sang HRM. Link/nút trỏ màn chưa port **vẫn hiện** (ngoại lệ có chủ ý của
      "không dùng được thì ẩn", chốt 21/08)
- [ ] Link sang bản ghi người xem **có thể không có quyền** (vd tên khách hàng): BE trả cờ `can_view_*`
      tính 1 lượt cho cả trang (`CustomerService::visibleIds()`, cấm N+1), FE chỉ dựng link khi cờ bật,
      còn lại là chữ thường — nếu không, bấm vào nhận 403 rồi bị đá về danh sách
- [ ] Cột **Người duyệt / Ngày duyệt** của phiếu duyệt nhiều cấp lấy theo **cấp đóng dấu CUỐI** (cả duyệt
      lẫn từ chối — `lastApproval()`, `COALESCE` các cột thời gian), không chỉ cặp cột cấp cuối; sort, lọc
      và Excel dùng chung nguồn đó (#11519: phiếu bị TP từ chối hiện 2 ô trống)
- [ ] Bảng chi tiết giữ đúng **tiêu đề 2 tầng / gộp của ERP** (nhóm "Số lượng" → Có thể giữ / Đề nghị /
      ĐVT…); cột gộp ghi đủ 2 nghĩa ("Người mượn / Tên hàng") (#11244, #11203, #11524, #11515). Cột cần
      chắc rộng khai `min-width` (`width` bị bảng co — ĐVT 150px còn ~70px, #11348)
- [ ] Ô ERP có thì HRM có, **kể cả khi thường rỗng** (#11186); ô chỉ rỗng vì loại phiếu không áp dụng
      (vd Hợp đồng khi loại "Xuất giữ khác") thì **ẩn hẳn**, không để ô xám trống (#11370)

### D. Form (thêm mới / chỉnh sửa)
- [ ] Lỗi validate hiện **ngay dưới ô nhập**, dạng `Tên trường – Nội dung lỗi`
- [ ] Còn lỗi thì **không gọi API lưu**; nhiều lỗi thì con trỏ nhảy về ô lỗi đầu tiên
- [ ] **Ô bắt buộc validate ở CẢ FE lẫn BE** (user chốt 06/10/2026): bấm Lưu / Gửi duyệt mà để trống →
      **mọi** ô bắt buộc báo đỏ **cùng lúc** (không phải chỉ 1 ô, các ô khác im — #11521, #11377), BE vẫn
      kiểm lại y hệt và trả 422. Form không có nháp (popup danh mục…) → FE luôn bắt đủ → `form-validate` §1
- [ ] **Lưu nháp chỉ nới `required`**: giữ đúng 1 trường đại diện — Tên, hoặc trường user chốt cho màn
      (vd Kho vật lý ở Phiếu điều chuyển hàng, Loại yêu cầu ở YCXH; thường là cột NOT NULL không default).
      Rule **định dạng** và ràng buộc nghiệp vụ vẫn chặn cả khi nháp. Bấm Lưu / Gửi duyệt thì bật lại đủ
      `required` ở FE; BE quyết theo `status` → `form-validate` §1
- [ ] Giới hạn `max:` ở FE khớp **độ dài cột DB** và rule BE (màn Tỉnh/TP để `max:50` trong khi cột 10 ký tự)
- [ ] Bảng nhiều dòng: đổi/xoá/thêm dòng thì dọn lỗi 422 theo chỉ số dòng (`utils/rowFieldErrors.js`),
      không `formError = {}` (#11312) → `form-validate` §3b
- [ ] Bảng render từ computed sinh **bản sao dòng** (`{...row}`) thì KHÔNG `v-model` vào bản sao — dùng
      `:value` + `@input` rồi `$set` vào `form.xxx[row.index]` (#11314, #11315, #11321)
- [ ] `@input` của `V2BaseSelect` có options nạp sau: bỏ qua khi options còn rỗng và khi giá trị không đổi
      (v-select2 tự bắn `change` chuỗi rỗng khi nhận options mới → xoá mất giá trị đã lưu, #11322)
- [ ] Ô số lượng / tiền **chặn thẳng** chữ, ký tự đặc biệt, số âm bằng helper `utils/number-input.js`
      (`sanitizeNumberEvent`, `:value` + `@input.native`, KHÔNG `v-model`); **vượt trần thì báo đỏ**, không
      tự kéo về trần/sàn (#11192, #11215, #11255, #11373) → `select-and-input-state` §4b
- [ ] Không tự xoá dòng user đã thêm mà chưa điền — báo đỏ đúng dòng để user điền hoặc bấm Xoá
- [ ] Dropdown danh mục chỉ liệt kê danh mục **đang hoạt động**…
- [ ] …nhưng màn Sửa/Chi tiết vẫn hiện đúng tên danh mục **đã khóa** đang gắn với bản ghi (🔒)
- [ ] Options select phải chứa **giá trị đang gắn** cả khi nằm ngoài phạm vi người xem (kho công ty khác,
      danh mục khoá) — gửi `include_ids`, không thì nhìn như phiếu mất dữ liệu → `select-and-input-state` §1
- [ ] Ô cố ý khoá trong form: `V2BaseInput`/`V2BaseCurrencyInput` `:disabled` (KHÔNG `.field-line` — đó là
      kiểu chữ trong bảng) + ⓘ qua prop `hint` của `V2BaseLabel`, câu nói **vì sao khoá + làm gì để đạt
      mục đích**. Màn Chi tiết (cả form readonly) không gắn ⓘ → `info-icon-tooltip`
- [ ] Có `unsavedChangesMixin` + gọi `markFormSaved()` sau khi lưu thành công. KHÔNG gọi `markFormSaved()`
      lúc mở màn (tắt cảnh báo vĩnh viễn); form không nằm ở `formSubmit` thì override
      `unsavedSnapshotSource()` → `unsaved-changes` §2b
- [ ] Dữ liệu **user chọn** nhưng ghi vào form sau một lần `await` (chọn phiếu từ popup, tải tệp lên) vẫn
      phải tính là "chưa lưu": gán `this.unsavedLastActionAt = Date.now()` ngay trước khi ghi, và
      `unsavedSnapshotSource()` gồm cả `pendingFiles` (#11538) → `unsaved-changes` §3
- [ ] Chưa đổi gì mà bấm Hủy → **không** hiện popup confirm
- [ ] Date picker: click ra lịch **và** gõ tay được, định dạng `dd/mm/yyyy`
- [ ] Ngày có trần/sàn (hạn giữ, hạn trả, không chọn quá khứ) chặn ngay trên lịch bằng prop
      `disabled-date` của `V2BaseDatePicker`; parser nhận cả `d/m/Y` lẫn `Y-m-d` nếu BE trả 2 kiểu (#11520)
- [ ] Tải tệp: chặn dung lượng ở FE trước khi gửi + khai message `attachments.*.uploaded` tiếng Việt (PHP
      `upload_max_filesize` chặn trước Laravel, trả câu tiếng Anh — #11313); `.xls` đời cũ trượt
      `mimes:xls` → so đuôi `getClientOriginalExtension()` bằng closure
- [ ] Bố cục: không lồng `.container-fluid` ở cả trang vỏ lẫn form con (đệm đôi 12px); không tự khai
      `padding-bottom` chừa footer (V2Footer đã gắn `has-v2-footer`); khối form bám khuôn của màn cùng nhóm
      (`.form-card` hay `V2BaseFormSection`) — đo `getBoundingClientRect` cạnh màn mẫu (#11356, #11540)
- [ ] Popup chọn hàng / bản ghi: hàng đã thêm loại ở **BE** (`exclude_*_ids` → `total` và "Hiển thị 1–N/N"
      đúng), không lọc ở FE; truyền `existingProducts` đúng khuôn `{key, groupId, parentRowId}`; màn không
      có cộng dồn dùng `duplicateMode="block"`; thứ tự ô lọc khớp thứ tự cột; `size="xl"` chỉ rộng hơn khi
      màn ≥ 1200px (#11279, #11349, #11524, #11543) → `modal-popup` §4b/§4c
- [ ] Popup chọn: số dòng/trang **mặc định 10, chọn được 10 / 20 / 50 / 100** (user chốt 06/10/2026,
      #11524) — hằng `PICKER_PAGE_SIZE_OPTIONS` / `PICKER_DEFAULT_PAGE_SIZE` ở `utils/pickerPagination.js`,
      không gõ số tay (`modal-popup` §4b). Cột Mã / Ngày tạo / ngày nghiệp vụ **sort được** (#11533 — khuôn bảng gọn tự dựng:
      `.sortable-header` ở `pages/finance/borrow-extend-requests/components/BorrowPickerModal.vue`); dòng
      không còn thao tác được thì **ẩn khỏi popup**, đừng cho chọn rồi báo lỗi
- [ ] Ô chọn mà **xoá giá trị phải hỏi xác nhận** (vd đổi nhân viên khi đã có hàng): select2 mở dropdown
      ngay sau nút x, đè lên popup xác nhận → chặn `select2:opening` ngay sau `select2:unselecting`
      (khuôn `bindEmployeeClearNoOpen` ở `AccountingPrepickCancelForm.vue`) → `select-and-input-state`
- [ ] Bảng con trong form khi rỗng **vẫn vẽ bảng**, dòng "Không có dữ liệu" nằm trong bảng (`colspan`),
      chữ xám `#6b7280` — không thay bằng `<div>` ngoài bảng, không `.text-muted` (ra đỏ)
- [ ] **Góc phải header khối đầu tiên** có dòng `Tên người tạo - dd/mm/yyyy HH:mm` ở CẢ Thêm / Sửa /
      Chi tiết — dùng component `components/CreatorInfoLine.vue` (`name`, `created-at`, `is-create`),
      KHÔNG tự viết span/computed riêng (Redmine #11575: ~40 màn mỗi màn một kiểu "·", "—",
      "Người tạo:", chỉ ngày, 11px…). Màn Thêm = người đăng nhập + giờ hiện tại; Sửa/Chi tiết = người
      tạo phiếu, BE trả `d/m/Y H:i` và **tên thuần** (nhiều resource ERP có `creator_name` = "Tên - Mã
      phòng" → thêm field mới, không sửa field cũ). Màn chuẩn: `pages/finance/bill-adjust-depts`.
      Góc phải header này **KHÔNG đặt badge trạng thái** (#11533) — trạng thái nằm ở nơi khác của form.
- [ ] Màn Thêm có nút **"Lưu và tiếp tục"** (`saveAndContinueMixin` ở form + `saveAndContinuePageMixin`
      + `:key="formKey"` ở trang vỏ; xem `pages/finance/buy-service-requests/create.vue`)
- [ ] Mọi ô chọn (`V2BaseSelect`) có **nút x xoá nhanh** — KHÔNG truyền `:allowClear="false"`, kể cả ô
      bắt buộc (QA báo lặp lại ở #11555, #11569)
- [ ] Mọi ô nhập/chọn trên FORM có placeholder `Nhập <X>` / `Chọn <X>` (QA #11557, #11562). (Luật
      "placeholder không lặp nhãn" ở mục A chỉ áp cho ô lọc floating.)
- [ ] Ô **Ghi chú / Diễn giải** dài: `col-12` + `V2BaseTextarea :rows="2"`, màn Chi tiết `disabled`
      (khuôn `bill-adjust-dept-requests`) — không để `V2BaseInput` ngắn nửa dòng
- [ ] Ô chọn nạp options lâu: cờ `isLoadingX` → `:placeholder="isLoadingX ? 'Đang tải...' : 'Chọn …'"`
      + `:disabled="isLoadingX"` (khuôn `CustomerForm.vue`). Loading cả trang/khối:
      `<div class="spinner-border text-primary" role="status">` — `ri-loader-4-line ri-spin` đứng
      yên vì dự án không có CSS `ri-spin` toàn cục.
- [ ] **File đính kèm** của màn tài chính: khối `pages/finance/bill-payment-requests/components/AttachmentSection.vue`
      (`:files` URL đã lưu + `:pending-files` + `api-base`), BE có `GET /{id}/attachment-sizes`
      (`BillPaymentAttachmentService::sizes()`) + `DELETE /{id}/files?file_url=` — KHÔNG dùng
      `V2BaseAttachmentSection` (không biết dung lượng file đã lưu → cột Dung lượng ra trống, #11549).
      Đổi/xoá file phải **ghi lịch sử** bằng trait `Services/Concerns/BuildsAttachmentHistoryChange.php`
      (snapshot lưu danh sách URL, không lưu SỐ file — đếm số thì thay 1 file bằng 1 file không ra log, #11540).
      Cần xem trước file trước khi lưu (viewer không đọc `blob:`) → FE `POST /upload-files` ngay lúc chọn
      tệp, lúc lưu gửi `attachment_urls[]`; FormRequest chặn `starts_with:<URL_PREFIX thư mục S3 của màn>`
      để client không nhét URL lạ (#11348, `ProductTransferFormRequest`).

### E. Chi tiết
- [ ] Số phiếu hiện ngay dưới/sau tiêu đề màn
- [ ] Tiêu đề `Chi tiết <đối tượng>: <mã>` — không có mã thì để trần, không lấy tên thay
- [ ] Mở URL id không tồn tại / không có quyền (404 / 403) → `this.$router.replace({ path:
      '/pages/extras/404' })`, **KHÔNG toast** rồi đẩy về danh sách → `list-page` §7 mục 1b.
      Interceptor `plugins/axios.js` đã tự toast 403 — request chi tiết gửi header `X-Silent-Errors`
      (khuôn `meeting/GeneralInfo.vue`) và khối Lịch sử chỉ dựng SAU khi nạp chi tiết xong, nếu không ra
      3 toast trùng (#11546).
      📌 Một số màn cũ (#11296, #11365, #11373, #11546) đang làm kiểu toast + về danh sách
      (`handleMissingRecord`) — khi động tới màn đó thì chuyển về chuẩn 404
- [ ] Thao tác trên phiếu đã bị người khác đổi trạng thái → BE trả **409** với câu
      `"Trạng thái đã bị thay đổi. Vui lòng load lại trang"` (nguyên văn
      `GuardsCatalogStatus::$statusConflictMessage`, QA chốt #11549) — KHÔNG trả 403 "không có quyền"
- [ ] Duyệt / thao tác dựa trên số liệu chép lúc lập phiếu → kiểm lại với **dữ liệu HIỆN TẠI** trong
      transaction, `lockForUpdate` phiếu cha rồi validate lại (#11520: phiếu gia hạn "27/09 → 27/09" vẫn
      duyệt được vì phiếu khác vừa được duyệt xen giữa)

#### E1. Lịch sử thay đổi — ĐỌC `entity-history/ui-base.md` TRƯỚC KHI VIẾT MARKUP

Đây là khối sinh lỗi lặp nhiều nhất khi port. **Không tự dựng UI**, dùng lại component có sẵn:
`components/assign/SystemInfoSection.vue` (khối trong màn chi tiết) và
`components/assign/customer/CustomerHistoryModal.vue` (popup ở màn danh sách).

- [ ] Làm **ĐỦ 2 NƠI** như màn Khách hàng: popup mở từ menu ⋮ ở màn **danh sách** *và* khối
      "Lịch sử" ở màn **chi tiết**. Làm 1 nơi rồi báo xong là thiếu
- [ ] Hai nơi hiển thị **y hệt nhau** (bố cục, chữ, màu, bộ lọc, thứ tự)
- [ ] Khối ở màn chi tiết **thu gọn mặc định** nhưng **dựng sẵn** (`v-show`, không `v-if`) sau khi nạp
      chi tiết xong — để badge số mốc lịch sử hiện ngay khi vào màn (#11373, user duyệt đánh đổi thêm 1
      request)
- [ ] Sắp **MỚI → CŨ** (BE `orderByDesc('changed_at')`)
- [ ] 4 ô lọc: Loại hành động · Người thực hiện · Từ ngày · Đến ngày. **Bấm "Tìm kiếm" mới lọc**
      (2 state `filters` / `appliedFilters`), "Làm mới" reset chứ không gọi lại API
- [ ] "Loại hành động" = **đúng 3 nhóm cố định** `create` Tạo mới / `update` Thay đổi thông tin /
      `status` Thay đổi trạng thái — giống nhau ở MỌI màn. Lọc bằng `log.action_group`
- [ ] 2 ô lọc lấy từ API `filter-options`, **KHÔNG suy từ log đang tải**. `performers` = toàn bộ
      nhân sự cùng công ty người tạo bản ghi, dạng `MÃ PHÒNG - Tên NV` (dòng log trên timeline thì
      **chỉ in tên**, phòng ban in riêng bên cạnh)
- [ ] Lọc ngày theo `created_at_raw` (`Y-m-d`), lọc người theo `actor_id`
- [ ] Một mục log theo thứ tự cố định: thời gian → tên hành động → người thực hiện → thay đổi → ghi chú
- [ ] Giá trị **cũ đỏ `#dc2626` → mới xanh `#16a34a`**, tên bản ghi bị sửa xám `#475569`;
      giá trị trống in `(trống)`; không có người thực hiện in `Hệ thống`
- [ ] Bảng con (danh sách thiết bị, người liên hệ…) in theo **3 nhóm có nhãn chữ**: thêm mới → đã
      xóa → sửa thông tin. Không dùng ký hiệu `~ - +`. Dòng sửa chỉ liệt kê trường đã đổi
- [ ] **Mọi** giá trị log đi qua `SiValue` (6 vị trí, kể cả `r.detail` và `m.name`) — bỏ sót là
      đường dẫn tệp hiện nguyên URL dài
- [ ] Đủ 4 trạng thái: đang tải / lỗi tải (+ nút Thử lại) / chưa có log / lọc không ra
- [ ] Khóa – Mở khóa – Duyệt – Từ chối đều **ghi log**, action lạ tự rơi vào nhóm `status`
- [ ] Mốc **"Tạo mới"** chỉ hiện thời gian + "Tạo mới" + người thực hiện, KHÔNG liệt kê từng trường (vẫn
      lưu snapshot đủ) (#11186); nhãn mốc sửa = **"Thay đổi thông tin"**
- [ ] Ghi chú / giá trị dài trong log: `overflow-wrap: anywhere` + `min-width: 0` — không để popup Lịch sử
      cuộn ngang (#11198)

### F. Import / Xuất
- [ ] Import dùng `V2BaseImportModal`; có file mẫu tải về được
- [ ] Validate trước khi import; dòng lỗi đỏ sửa được tại chỗ, dòng hợp lệ xanh và khóa
- [ ] Hiện trạng component (khác câu SRS "vẫn import khi còn dòng lỗi"): `V2BaseImportToolbar` **khoá nút
      Import khi còn dòng lỗi** — user phải sửa dòng lỗi hoặc bấm "Bỏ dòng lỗi" rồi mới Import. HDSD /
      testcase ghi theo hành vi này. BE vẫn viết kiểu chịu được dòng lỗi (bỏ qua dòng lỗi) để khi
      component đổi thì không phải sửa lại
- [ ] Xuất file: mở popup **chọn trường** (`ExportFieldsModal`) trước, KHÔNG xuất thẳng khi bấm nút;
      thứ tự cột trong file theo đúng thứ tự user tick
- [ ] BE trả **đủ** các trường có trong popup — kể cả cột đang ẩn ở màn danh sách, nếu không user
      tick xong ra cột trống
- [ ] Trường trong popup khai ở **CẢ** FE `exportFields` **và** BE (`ExportColumnRegistry` nếu dùng
      `DynamicExport`, hoặc `columnDefinitions()` của class export riêng); không `'always' => true` trừ STT
      (user bỏ tick vẫn ra cột, lệch thứ tự); cột boolean trả thêm khoá chữ `*_text`; popup tick sẵn cột
      đang hiện (`exportFieldsMixin.visibleExportFields`) (#11574, #11346) → `list-page` §14b
- [ ] Nút xuất bị khóa khi đang xuất + có dòng tiến độ
- [ ] File Excel **tự dựng bằng ExcelJS ở FE** (báo cáo, file tồn…) phải có đủ như file danh sách
      chuẩn — dùng helper, đừng chép tay:
      letterhead dòng 1 = `fetchCompanyLetterhead(store)` + `insertLetterhead()` (cùng export từ
      `utils/export/listExportFile.js`; ERP lấy header công ty NGƯỜI ĐĂNG NHẬP);
      mã số theo từng ô = `numberFormatOf(value)` (gắn cứng `#,##0.##` cho số nguyên → Excel in
      "2,000." cụt đuôi, #11569); khối ký "Ngày… / Người lập / (Ký, họ tên)" = `addExcelSignatureBlock`
      (`utils/export/excel-signature-block.js`); tiêu đề + cột + dòng Tổng cộng khớp file ERP; số 0
      để ô trống nếu ERP để trống
- [ ] File mẫu import KHÔNG có dòng mô tả dưới tiêu đề nếu file mẫu ERP không có (dòng đó bị đọc
      thành dữ liệu lỗi, #11560/#11563) — mô tả cột đặt ở icon ⓘ bảng xem trước

### F2. In
- [ ] Nút In mở **popup xem trước** `ReportPrintPreviewModal`, không mở trang riêng → `print-page` §0
- [ ] In danh sách: ô "Thời gian" ghi "Tất cả" khi không lọc ngày, cột ngày kèm giờ, chốt trần số dòng
      → `print-page` §4d / §4e
- [ ] Khối ký 1 người: dòng "Ngày … tháng … năm …" nằm **trong chính ô ký**, cùng trục với "Người lập /
      (Ký, họ tên)", sát lề phải, tên in đậm, không kẻ viền (#11253 qua 3 vòng) → `print-page` §3b
- [ ] Cột mẫu in khai `%` + `table-layout: fixed`, KHÔNG khai `px` (tổng px > bề ngang A4 → cột co giãn
      bị bóp, chữ rơi dọc)
- [ ] Logo/ảnh vỡ trên bản in → `curl` kiểm URL trước; 404 là lỗi dữ liệu, báo user, đừng đổi nguồn ảnh (#11431)

### G. Thông báo & xác nhận
- [ ] Toast thành công/thất bại dùng **đúng câu** trong bảng QLDA, kết thúc bằng dấu chấm
      (`"<Hành động> thành công."`); lỗi 422 lấy câu cụ thể của BE qua `utils/api-error-message.js`
      → `apiErrorMessage(error, fallback)`, không toast câu chung "The given data was invalid."
- [ ] Chỉ dùng toast `success` (xanh) / `error` (đỏ) cho thao tác trên phiếu — KHÔNG `warning` (cam)
      cho trường hợp "bỏ qua dòng / hết số lượng" (#11552: màn duy nhất trong nhóm dùng cam)
- [ ] "Bạn chưa nhập đầy đủ thông tin." (QLDA_001) **chỉ** khi thiếu ô bắt buộc; lỗi khác (vượt số có thể
      hủy…) toast đúng câu lỗi cụ thể, kèm tên hàng (#11524)
- [ ] **Một thao tác = đúng 1 thông báo**: popup dùng chung và màn không cùng toast cho một việc (#11349);
      nhưng chọn nguồn mà không có dữ liệu thì VẪN toast lý do — đừng gỡ toast "cho đỡ trùng" (#11370)
- [ ] Mọi popup xác nhận dùng `base-confirm-modal` / `$confirm()`, không tự khai `b-modal`
- [ ] Thông báo nghiệp vụ (chuông/push) theo template
      `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}`, tên ≤ 50 ký tự và in đậm,
      tổng ≤ 120 ký tự, deep-link kèm ID

### H. Bản ghi đã khóa
- [ ] BE chặn `update`/`destroy` bằng **423 LOCKED** (middleware nếu controller nhận `FormRequest`)
- [ ] FE **ẩn** nút Sửa/Xóa khi khóa; vào màn Sửa bằng URL trực tiếp → đá về Chi tiết
- [ ] Có lối **Mở khóa**, và Khóa/Mở khóa đều **ghi lịch sử**

### H2. Màn DANH MỤC — Xóa / Khóa / Trạng thái (user chốt 26/09/2026, khuôn Quận/Huyện)
Đã phải sửa lại cả loạt màn (Nguồn vốn, Đường/Phố, Cấp DV BD, Ghi chú KT, Chi nhánh NH, Vụ việc, Mã
phí, Chi phí, Gói BD) vì làm sai những điểm dưới — màn mới phải đúng ngay từ đầu.
- [ ] **KHÔNG xoá mềm** (đổi status / `deleted_at` / "đã dùng thì Xóa thành Khóa"). Xóa = **xoá hẳn**,
      chỉ khi bản ghi đang Hoạt động VÀ **chưa được dùng**; đã dùng → ẩn nút Xóa (`is_can_delete`) +
      BE chặn 400 `"<Đối tượng> đang được sử dụng, không thể xóa."`
- [ ] "Đã dùng" = có dòng ở **MỌI bảng có cột id trỏ tới** (không tính cột lưu tên bằng chữ). Khai 1
      hằng `USAGE_REFERENCES` trên Entity + `usedIds(array $ids)` (1 query/bảng/trang, cấm N+1).
      ⚠️ Tên cột lừa: `wr_accounting_service_items.service_id` thực ra trỏ `costs` — kiểm bằng dữ liệu
      (giá trị có khớp bảng đích không) trước khi xếp. Bảng "dữ liệu của chính bản ghi" (vd hàng hoá
      gắn gói) không tính là đã dùng — liệt kê cho user chốt.
      ⚠️ **Prod có khoá ngoại mà DB `gop_db` local không có** → local xoá chạy, lên prod lỗi SQL 1451 (vd
      màn Tỉnh/TP — `Province` khai lệch tên `USED_BY_COLUMNS`, màn mới vẫn đặt `USAGE_REFERENCES`). Ngoài `usedIds()` thêm lưới an toàn: `catch (QueryException $e)`
      với `$e->errorInfo[1] === 1451` → trả đúng câu "… đang được sử dụng, không thể xóa." (`ProvinceService`)
- [ ] Có **Khóa / Mở khóa**, và **cho Khóa cả khi đang được dùng** (không cấm khoá vì đã hạch toán).
      Route `PUT /{id}/lock|unlock` (KHÔNG dùng GET); service kiểm trạng thái hiện tại → đã ở trạng thái
      đích thì 400 `"Trạng thái đã bị thay đổi. Vui lòng load lại trang"` (đừng báo thành công lần 2).
- [ ] Popup/form Tạo–Sửa có **ô Trạng thái** (mặc định Hoạt động); danh sách hiện **cả bản ghi Khóa**
      + cột badge + bộ lọc Trạng thái. Bản ghi Khóa chỉ còn Mở khóa + Lịch sử.
- [ ] Nút Khóa / Mở khóa nằm **trong cột Hành động** (`getRowActions`, icon `ri-lock-line` /
      `ri-lock-unlock-line`) — chuẩn hiện hành, KHÔNG đặt trong cột Trạng thái như vài màn cũ
      (khuôn `references/khuon-man-mau.md` mục Cột Hành động).
- [ ] Middleware route theo thứ tự **`checkPermission` TRƯỚC `recordNotLocked`** — ngược lại thì user
      thiếu quyền nhận 423 thay vì 403 (dính ở Cấp DV, Ghi chú KT, Chi phí).
- [ ] Route model binding không tìm thấy bản ghi (người khác vừa xoá) đang trả toast tiếng Anh
      `"Item Not Found!"` / `"not found bank"` → phải ra câu tiếng Việt
      `"Trạng thái đã bị thay đổi. Vui lòng load lại trang"`.
- [ ] Danh mục bị Khóa: select ở màn khác ẩn đi nhưng bản ghi cũ đang dùng vẫn hiện đúng tên + 🔒
      (CLAUDE.md mục danh mục khoá) — kiểm cả **Import** của màn tiêu thụ (hay quên, vẫn nhận giá trị Khóa)
      và API select dùng chung (vd `AddressController`, `CustomerService::hamlets`).
- [ ] Sửa code xong → cập nhật luôn HDSD/SRS/testcase (xoá mềm → xoá cứng, thêm Khóa, ô Trạng thái).

---

## Bẫy hay dính khi port

| Bẫy | Hậu quả | Cách tránh |
|---|---|---|
| **Chép lại phép tính nghiệp vụ đã có ở màn khác** | 2 bản cùng 1 công thức, vài tháng sau lệch nhau, không ai biết bản nào đúng | Grep trước khi viết; hàm đã có mà `private` thì **tách ra service dùng chung** (hỏi user trước) — xem Bước 3b |
| **Copy màn HRM đã port trước đó làm khuôn** | Nhân bản y nguyên cái sai — 1 lỗi UI thành N màn lỗi | Khuôn chuẩn là **Danh mục khách hàng**, không phải màn gần nhất mình vừa làm. Muốn copy màn khác thì chạy checklist cho **màn nguồn** trước |
| Dùng `V2BaseFilterPanel` + tự dựng `#advanced-filters` | Mất popup "Cài đặt bộ lọc", user không ẩn/sắp xếp được ô lọc | `V2BaseSmartFilterPanel` + schema `filterFields` cho MỌI màn > 3 ô lọc |
| Bấm "Xuất Excel" là tải file luôn | Vi phạm quy tắc "user chọn trường xuất" | Mở `ExportFieldsModal` trước, truyền `selectedFields` xuống hàm dựng file |
| Bê nguyên nhãn/màu trạng thái của ERP | "Đang tạo" hiện ĐỎ như phiếu bị từ chối | Đối chiếu hằng `STATUSES` với bảng màu SRS; nháp phải xám |
| Mỗi màn tự viết `statusPillClass()` | Badge lệch nhau giữa các màn | `V2BaseBadge` + helper `utils/statusBadgeVariant.js` |
| Port nút nhưng bỏ điều kiện ẩn/hiện của ERP | User không đủ điều kiện vẫn bấm được | Bước 1 ghi cả điều kiện, bước 5 đối chiếu lại |
| Nút bị `interactable: false` + `disabledTitle` (rule CŨ) | Nút xám nằm chình ình, vi phạm rule hiện hành | Đổi sang `visible`. Màn cũ đầy pattern này — copy là dính |
| Sửa màn danh sách mà quên khối Trạng thái trong **Form** | Danh sách 1 kiểu badge, chi tiết 1 kiểu | Grep `status-pill` / `statusPillClass` trong **cả thư mục feature** |
| Danh sách gate `perm && isActive`, chi tiết chỉ gate `perm` | 2 màn lệch số nút | Đọc điều kiện từ **cùng 1 nguồn** (cờ BE `is_can_edit`) |
| Trùng `columnScreenKey` / `localStorageKey` với màn khác | 2 màn ghi đè cấu hình của nhau | Đặt theo slug màn, grep kiểm trùng |
| Tự dựng `<span class="status-pill">` | Badge lệch hẳn các màn khác | `V2BaseBadge` |
| STT tính `index + 1` | Sai từ trang 2 | `getNumericalOrder(currentPage, pageSize, index)` |
| Cột Mã để `@click` trên `<div>` | Không mở được tab mới (vi phạm SRS) | `<nuxt-link>` |
| `V2BaseRowActions` so `action.key` | **Nút bấm im ru, không lỗi console** — và nút khai `to:` vẫn chạy nên rất dễ nghiệm thu nhầm là "màn chạy được" | Nó emit **chuỗi key** → `switch (action)`. Khuôn đúng: `pages/assign/customers/index.vue::handleRowAction`. ⚠️ Menu hành động **tự dựng tay** thì `action.key` lại đúng — chỉ sai khi qua `V2BaseRowActions` |
| `V2BaseButton` truyền `disabled` | Không có prop đó → nút vẫn bấm được | Nút không dùng được → ẩn bằng `visible`/`v-if`. Nút **đang gửi request** thì khoá bằng `:interactable="!submitting"` (đây là cách đúng, không phải rule cũ) — `button-convention` §6b |
| Truyền prop không tồn tại cho `V2Base*` | Rơi vào `$attrs`, **không báo lỗi**: `V2BaseIconButton icon="…"` ra ô rỗng (icon phải nằm trong slot `<i>`); `V2BaseButton danger` ra màu XANH (đúng là `primary status="danger"`); `defaultHidden` không ẩn cột (đúng là `isVisible: false`) | Component render trống / sai màu → mở file component đọc `props` trước, đừng đoán tên prop (#11346, #11348) |
| Option `V2BaseSelect` không phải `{ id, name }` | `id` undefined → select2 lấy nhãn làm value: dropdown mở được mà **bấm không chọn được**, popup xuất "Đang chọn 1/9" | Map trước `.map(c => ({ id: c.key, name: c.label }))`; select2 trả **chuỗi** → so `String(a) === String(b)` |
| Khai `company` / `department` / `part` trong `initialStateForm` | **Ô lọc Công ty/Phòng ban chọn xong không có gì xảy ra.** Hỏng 2 lần: Vue 2 không reactive với property chưa khai → deep watcher không bắn; và tên gửi lên không khớp param BE | `V2BaseCompanyDepartmentFilter` ghi vào **`company_id` / `department_id` / `part_id` / `employee_id`** — khai đúng 4 key này (kể cả key không dùng làm bộ lọc, vì watcher của nó vẫn reset). BE đọc cùng tên |
| Để ô "Bộ phận"/"Nhân viên" hiện mà BE không lọc theo | Ô lọc chết, user chọn mãi không ra | `:disable_part` / `:disable_employee` — đối chiếu `searchByFilter` của BE xem thật sự lọc theo cấp nào |
| `$axios` tải file thiếu `Authorization` | Xuất Excel 401 | Tự gắn token cho request export |
| Bê nguyên `title` cho panel lọc | Mỗi màn một tiêu đề khác nhau | Bỏ prop, dùng mặc định "Bộ lọc danh sách" |
| Tắt ô tìm nhanh vì "ERP không có" (`:show-quick-search="false"`) | Panel chuyển sang kiểu màn báo cáo: mất ô tìm nhanh VÀ nút Tìm kiếm / Làm mới chỉ hiện sau khi bấm "Tìm kiếm nâng cao" (dính thật: Danh sách hàng mượn + Hàng sắp hết hạn mượn, 24/09/2026) | Không bao giờ tắt ở màn danh sách. BE thiếu `keyword` thì thêm vào BE — xem `list-page` |
| Quên bật `floating` | Khối lọc trông như màn cũ: nhãn nằm TRÊN ô, chiếm thêm một dòng, trong khi các màn mới nhãn nằm trong ô và bay lên viền | Thêm prop `floating` — panel lo hết phần còn lại |
| Tự chế autocomplete "gõ để tìm" | Chưa gõ gì đã báo "Không tìm thấy…"; dropdown quên `position:absolute` đẩy vỡ layout | `V2BaseSelectRemote` + `minimumInputLength` — nó lo sẵn 3 trạng thái chưa-đủ-ký-tự / đang-tìm / không-có |
| Đè CSS ô lọc bằng `!important` mà không tính specificity | **Local đúng, lên dev/prod sai** — thứ tự gộp CSS khi build khác dev nên rule bằng điểm đổi phe | Selector phải **nặng ký hơn** rule của `V2BaseSelect`; kiểm chứng bằng cách nhét vào đầu `<head>` rồi đo `getComputedStyle` |
| Vỏ bọc field tự mở stacking context (`z-index` trên wrapper) | Dropdown của mọi control bên trong bị nhốt — header dính của bảng (z-index 6) vẽ đè lên | Không đặt `z-index` trên wrapper; hạ z-index của thứ cần đè thay vì nâng wrapper |
| Tự dựng khối "Lịch sử" ở màn chi tiết cho nhanh | Mỗi màn một kiểu timeline, dropdown "Loại hành động" mỗi màn một danh mục — user không đối chiếu được | Dùng lại `SystemInfoSection.vue`, đọc `entity-history/ui-base.md`. Xem mục E1 |
| Chỉ làm lịch sử ở màn chi tiết, quên popup ở màn danh sách | Nghiệm thu xong user quay lại yêu cầu bổ sung | Chuẩn màn Khách hàng là **2 nơi** |
| Suy 2 ô lọc lịch sử từ log đang tải | Dropdown chỉ có 1-2 dòng, user tưởng mất dữ liệu | Gọi `filter-options`, fallback 3 nhóm hard-code |
| Đổi route mà quên dữ liệu đã lưu URL trong DB | Màn bị đá 404 | Grep xem đường dẫn có bị lưu DB / so khớp ở BE không; redirect FE **không** cứu được |
| Cache danh mục vào Vuex rồi không làm mới | Thêm Nhóm ngành xong, dropdown ở màn khác vẫn là danh sách cũ tới khi F5 (#11377 BUG7) | Màn danh mục thêm/sửa/khoá xong thì gọi action xoá cache của danh mục đó (khuôn `clearInvestmentScopes` ở `store/optionsSelect.js`) → `select-and-input-state` |
| Bê bảng/cột ERP mà không đọc `.plans/gop-db/design.md` mục "Bẫy khi port" | Cột polymorphic lưu tên class ERP, cột do ERP ghi bị HRM ghi đè, thiếu cột phụ ERP vẫn ghi, NOT NULL không default, path `/uploads/…` 404… | Đọc mục đó trước khi viết model/service cho bảng ERP |
| Tự dựng thứ đã có helper | Mỗi màn một kiểu | Có sẵn: `utils/mixins/lockedCatalogOptionsMixin.js` (giữ danh mục khoá trong select form Sửa/Xem) · `utils/historyFormat.js` (giá trị trong popup lịch sử) · `utils/confirmInfoHtml.js` (popup xác nhận kèm bảng thông tin, tự escape) · `components/SubtextSelect.vue` (select có dòng phụ xám) · `utils/import-multi-sheet-helper.js` (import nhiều sheet) · `components/V2BaseImageField.vue` (ô ảnh) · 2 màn giống nhau (Khách hàng / NCC) dùng chung List/Form + file config: `components/finance/declare-debt/*` + `utils/finance/declareDebtConfigs.js` |

---

## Tự kiểm nhanh bằng grep (chạy trên CẢ thư mục feature, không chỉ index.vue)

```bash
# Mỗi dòng kết quả là 1 vi phạm cần sửa
grep -rn "status-pill\|statusPillClass"   <thư-mục-feature>   # phải dùng V2BaseBadge
grep -rn "interactable:\|disabledTitle"   <thư-mục-feature>   # nút phải ẩn bằng visible
grep -rn "action\.key ==="                <thư-mục-feature>   # V2BaseRowActions emit CHUỖI -> nút chết
grep -rn "V2BaseFilterPanel"              <thư-mục-feature>   # phải là V2BaseSmartFilterPanel
grep -rn 'show-quick-search="false"\|:showQuickSearch="false"' <thư-mục-feature>   # cấm ở màn danh sách
grep -rn "advanced-filters"               <thư-mục-feature>   # bộ lọc dựng tay
grep -rn "showCustomerList\|filtered.*= \[\]"  <thư-mục-feature>   # autocomplete tự chế -> V2BaseSelectRemote
grep -rn "V2BaseSelectRemote" <thư-mục-feature> | grep -v 'height='   # thiếu height -> ô lùn 32px
grep -rn "thành công'"                    <thư-mục-feature>   # câu toast tự chế, so với bảng QLDA
grep -rn "log.action !=="                 <thư-mục-feature>   # lịch sử phải lọc theo action_group
grep -rn "actionOptions"                  <thư-mục-feature>   # dựng từ log = sai, phải từ filter-options
grep -rn "<V2BaseIconButton[^>]*icon=\|<V2BaseButton[^>]* danger\b\|defaultHidden" <thư-mục-feature>   # prop không tồn tại
grep -rn "Người lập\|Ngày lập"            <thư-mục-feature>   # nhãn phải là Người tạo / Ngày tạo
grep -L "layout:"  <thư-mục-page>/*.vue <thư-mục-page>/_id/*.vue          # thiếu layout -> sai vỏ trang
grep -L "v2-styles.scss" <thư-mục-page>/index.vue <file-Form>.vue        # thiếu import -> vỡ bộ lọc nâng cao
grep -rn "process.env.ERP_URL"            <thư-mục-feature>   # link ERP tự ghép -> utils/erp-link.js
grep -rLE "pickerPagination" <thư-mục-feature>/components/*{Search,Picker}*Modal.vue   # popup CHỌN chưa dùng hằng số dòng chung
grep -rn "text-muted"                     <thư-mục-feature>   # ra chữ ĐỎ -> dùng xám #6b7280
```

Nếu grep ra sạch mà mắt vẫn thấy lệch → mở màn **Danh mục khách hàng** đặt cạnh và so từng khối.

## Khi phát hiện project đang có nhiều kiểu khác nhau

**Nêu ra cho user chọn kiểu chuẩn. KHÔNG tự chọn rồi làm tiếp, cũng KHÔNG tự sửa đại trà các màn cũ.**

## Tài liệu liên quan

| Nội dung | Đọc thêm |
|---|---|
| Bảng tra quy tắc chung (SRS) | `references/srs-quy-tac-chung.md` |
| Khuôn 4 màn + component/mixin | `references/khuon-man-mau.md` |
| Quyền theo cấp, `V2Footer`, badge | `.claude/skills/list-page/SKILL.md` |
| Nút, màu, icon | `.claude/skills/button-convention/SKILL.md` |
| Popup, modal, select trong modal | `.claude/skills/modal-popup/SKILL.md` |
| Validate form màn mới | `.claude/skills/form-validate/SKILL.md` |
| Cảnh báo thoát khi chưa lưu | `.claude/skills/unsaved-changes/SKILL.md` |
| Select / ô nhập ở mọi màn | `.claude/skills/select-and-input-state/SKILL.md` |
| Lịch sử thay đổi | `.claude/skills/entity-history/SKILL.md` |
| Thông báo nghiệp vụ | `.claude/skills/notification-convention/SKILL.md` |
| Import Excel | `.claude/skills/import-excel/SKILL.md` |
| Xuất Excel (BE + ExcelJS) | `.claude/skills/export-excel/SKILL.md` |
| Nút In / bản in | `.claude/skills/print-page/SKILL.md` |
| Icon ⓘ + tooltip | `.claude/skills/info-icon-tooltip/SKILL.md` |
