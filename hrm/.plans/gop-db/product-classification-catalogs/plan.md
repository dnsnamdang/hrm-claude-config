# 6 danh mục quy hoạch lại hàng hóa (#11421) — Implementation Plan

**Goal:** Dựng 6 danh mục mới (Tính chất hàng hóa · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm ·
Chính sách kinh doanh · Đặc tính sản phẩm) trong phân hệ Danh mục chung của HRM.

**Architecture:** Không dựng framework mới. BE nhân khuôn `Modules/Assign` (Controller → Service →
Request → Resource → Entity) đặt trong `Modules/MasterData`; FE nhân khuôn
`pages/assign/customer-scopes/` (`index.vue` + `AddXxxModal.vue`). 7 bảng mới, không đụng bảng cũ.

**Tech Stack:** Laravel 8 + nwidart/laravel-modules (BE) · Nuxt 2 / Vue 2 + BootstrapVue (FE) · MySQL `gop_db`

**Spec:** [docs/superpowers/specs/gop-db/2026-09-18-product-classification-catalogs-design.md](../../../docs/superpowers/specs/gop-db/2026-09-18-product-classification-catalogs-design.md)

---

## Global Constraints

- **Nhánh:** `feat/11421-danh-muc-quy-hoach-hang-hoa`, tách từ `gop_db`, đã tạo ở **cả hai** repo.
- **KHÔNG commit, KHÔNG push** — user tự commit sau khi nghiệm thu từng phase.
- Mọi nhãn, thông báo, comment code viết **tiếng Việt**.
- **KHÔNG đụng** `scopes`, `chapters`, `job_groups`, `job_clusters`, `groups`, `attribute_groups`,
  `products`, `product_classifies`. Migration chỉ `create table`.
- **KHÔNG dùng** `DB_CONNECTION_SECOND` / `mysql2`.
- Trạng thái **1 = Hoạt động, 2 = Khóa** (chuẩn HRM), không dùng 0/1 kiểu ERP.
- Khuôn bắt buộc là **`pages/assign/customer-scopes/`** — không copy màn port gần nhất.
- Thông báo lấy **nguyên văn bảng QLDA**; nút không dùng được thì **ẩn**, không disable.
- Route tĩnh (`/getAll`, `/export`, `/import`) đặt **TRƯỚC** route `/{id}`.
- Xong mỗi phase: chạy khối grep tự kiểm trong `.claude/skills/erp-to-hrm-screen/SKILL.md`.

---

## Phase 1 — Nền CSDL và phân quyền (BE)

- [x] Task 1.1 — 6 migration `create` bảng danh mục (`product_natures`, `product_function_groups`,
      `product_families`, `product_types`, `business_policies`, `product_characteristics`) theo §4 spec
- [x] Task 1.2 — Migration bảng nối `product_type_attributes` (unique `product_type_id` +
      `attribute_id`, cascade delete theo `product_types`)
- [x] Task 1.3 — **12 quyền id 1574-1585**, `group = 'Danh mục hàng hóa'`, `type = 9` (phân hệ
      Danh mục chung): thêm vào `PermissionsTableSeeder` + INSERT tay vào bảng **`permissions`**
      (bảng SỐNG; `hrm_permissions` là bảng chết). Không dùng migration — theo tiền lệ các danh
      mục trước
- [x] Task 1.4 — 6 Entity trong `Modules/MasterData/Entities/ProductClassification/` (hằng
      `STATUS_ACTIVE = 1` / `STATUS_INACTIVE = 2`, quan hệ cha–con, quan hệ `attributes`,
      accessor tên người tạo/sửa). Docblock ghi rõ `product_families` = **Nhóm sản phẩm quy hoạch
      mới**, KHÔNG phải `groups` của ERP
- [x] Task 1.5 — Chạy `php artisan migrate` trên `gop_db` local, kiểm tra 7 bảng + 12 quyền có thật

## Phase 2 — API CRUD 6 danh mục (BE)

- [x] Task 2.1 — `ProductNature`: Service + Controller + Request + Resource + routes (đủ 10
      endpoint §5.2), validate `barcode_template_type in:1..6`
- [x] Task 2.2 — `ProductFunctionGroup`: như trên + rule cha `product_nature_id` phải `status = 1`
      + `getAll?product_nature_id=`
- [x] Task 2.3 — `ProductFamily`: như trên, cha là Nhóm chức năng
- [x] Task 2.4 — `ProductType`: như trên + `can_retail`, `serial_required`, `vat_percent_tax_rate_id`
      (`tax_rates`), `long_stock_days`, `ingredient`, `warning`, `user_manual`, sync `attribute_ids`
- [x] Task 2.5 — `BusinessPolicy` + `ProductCharacteristic` (2 danh mục đơn, chỉ code/name/description/status)
- [x] Task 2.6 — Chặn xóa khi còn cấp con (§5.4), thông báo nguyên văn QLDA; `lock` / `unlock`
- [x] Task 2.7 — Test PHPUnit: trùng tên, sai định dạng mã, cha đã khóa, chặn xóa khi có con,
      `getAll` chỉ trả `status = 1`

## Phase 3 — Màn danh sách + modal (FE)

- [x] Task 3.1 — Thêm nhóm menu **"Hàng hóa"** (6 mục, `isShow` theo quyền) vào
      `components/subsystem-menu/master-data.js`; kiểm không trùng link với phân hệ khác
- [x] Task 3.2 — `pages/master-data/product-natures/` (index + modal) — làm chuẩn cho 5 màn còn lại:
      4 mixin, `V2BaseSmartFilterPanel` + `floating`, `V2BaseBadge`, `switch (action)`,
      `localStorageKey`/`columnScreenKey` riêng, tooltip ⓘ
- [x] Task 3.3 — `product-function-groups` (thêm cột + ô lọc Tính chất hàng hóa, select cha lọc `status = 1`)
- [x] Task 3.4 — `product-families` (2 cấp cha, đổi cha reset cấp dưới, khai `resetKeys`)
- [x] Task 3.5 — `product-types` (3 cấp cha + các trường riêng; Thành phần / Cảnh báo / HDSD mặc
      định **ẩn** trong Cấu hình cột; multiselect Thuộc tính)
- [x] Task 3.6 — `business-policies` + `product-characteristics`
- [x] Task 3.7 — Chạy khối grep tự kiểm trên cả 6 thư mục feature, sửa hết vi phạm

## Phase 4 — Import / Xuất Excel

- [x] Task 4.1 — BE `export` qua `ExportColumnRegistry` + `DynamicExport` cho 6 danh mục (trả đủ
      trường, kể cả cột đang ẩn)
- [x] Task 4.2 — FE `ExportFieldsModal` cho 6 màn (không xuất thẳng khi bấm nút)
- [x] Task 4.3 — BE `import/validate` + `import`; danh mục có cấp cha nhận **mã cha**, không nhận tên
- [x] Task 4.4 — FE `V2BaseImportModal` + `CatalogImportMixin` + file mẫu cho 6 màn

## Phase 5 — Nghiệm thu

- [x] Task 5.1 — Bấm thật từng ô lọc, đối chiếu param Network với `searchByFilter`
- [x] Task 5.2 — Bấm thật từng nút hành động, kể cả trong menu "…"
- [x] Task 5.3 — Kiểm quyền: tài khoản chỉ có quyền Xem → không thấy nút Tạo mới / Sửa / Xóa
- [x] Task 5.4 — Kiểm luồng phân cấp: khóa cha → con không chọn được cha đó nữa, nhưng bản ghi cũ
      vẫn hiện đúng tên cha (🔒)
- [x] Task 5.5 — Đã chụp + XEM ẢNH 3 màn (Tính chất hàng hóa, Loại sản phẩm, Nhóm chức năng) + popup chọn trường xuất; 3 màn còn lại kiểm bằng đo DOM
- [x] Task 5.6 — Cập nhật `.plans/gop-db/STATUS.md` + checkpoint

---

## Checkpoint

### Checkpoint — 18/09/2026 (rà soát trước khi user đẩy code)
Rà một lượt: 11/11 test BE xanh · lint sạch toàn bộ PHP mới · khối grep tự kiểm của
`erp-to-hrm-screen` ra 0 vi phạm trên cả 6 màn · 6/6 danh mục trả 200 ở `list` / `getAll` /
`export` · vòng đời đầy đủ (tạo → sửa → khóa → chặn sửa → chặn xóa → mở khóa → xóa) chạy đúng ·
không còn `console.log` / `TODO` / `dd()` trong file mới.
Sửa thêm 1 chỗ: xóa bản ghi ĐANG KHÓA trước đây trả nhầm câu QLDA_015 "đang được sử dụng" →
tách thành "Không thể xóa <danh mục> đang ở trạng thái khóa. Hãy mở khóa trước." (QLDA_015 giữ
nguyên cho trường hợp còn danh mục con).

### Checkpoint — 18/09/2026 (sửa theo góp ý: checkbox "Có thể bán lẻ" lệch hàng)
Modal Loại sản phẩm tự dựng `custom-control custom-checkbox` + `d-flex align-items-end` nên
checkbox không thẳng hàng với các ô cùng dòng. Đổi sang khuôn chuẩn của
`pages/finance/accounts/components/AccountFormComponent.vue`: `<V2BaseLabel>&nbsp;</V2BaseLabel>`
làm nhãn rỗng + `.option-box { display:flex; align-items:center; min-height:31px }` +
component dùng chung `V2BaseCheckbox` với chữ truyền qua prop `label`.
⚠️ Chữ PHẢI truyền qua prop `label`, để text bên ngoài thì thẻ `<label>` rỗng của
`b-form-checkbox` phủ lên input và chặn click (ghi chú QA #11300 ở màn Tài chính).
Verify: đo DOM ra **lệch 0px** giữa tâm checkbox và tâm ô "Số ngày tính tồn lâu"; bấm thật thì
`checked = true` và `data.can_retail = true`.

### Checkpoint — 18/09/2026 (sửa theo góp ý: gộp ô lọc khoảng ngày)
User chỉ ra: 2 ô "Ngày tạo từ" / "Ngày tạo đến" tách rời là SAI quy tắc chung — khoảng ngày phải
gộp **một ô** `type: 'date-range'`. Đã sửa cả 6 màn: 1 field `created_range` +
`resetKeys: ['created_from','created_to']` + `inputCount: 1`; khai thêm khoá `created_range` vào
`initialStateForm` (Vue 2 không reactive với property chưa khai).
Verify trên FE cổng 3000 của user: khối lọc hiện 1 nhãn "Ngày tạo" với 2 ô `Từ ngày → Đến ngày`,
param gửi lên vẫn là `created_from=2026-09-18&created_to=2026-09-18` (không lẫn khoá ảo), bảng lọc
đúng. BE không phải sửa gì.

### Checkpoint — 18/09/2026 (Phase 4 xong — Import / Xuất Excel)
Vừa hoàn thành: **Phase 4 đủ 4 task** cho cả 6 màn.
BE: 6 bộ cột trong `ExportColumnRegistry` · `BaseCatalogController::export/validateImport/import` ·
trait dùng chung `Services/ProductClassification/Concerns/ImportsCatalogRows` · 18 route mới
(export + import/validate + import cho mỗi danh mục). Payload import dùng chung khoá **`rows`**.
FE: 6 màn gắn `exportFieldsMixin` + `CatalogImportMixin`, nút **Import Excel** (cam) và
**Xuất Excel** (xanh lá) đúng thứ tự Tạo mới → Import → Xuất → Cấu hình cột; file mẫu sinh tại FE
từ chính `importColumns` (`buildImportTemplate`).
Verify thật trên trình duyệt: popup "Chọn trường xuất file" tick sẵn 5/9 cột đang hiện → tải file
`.xlsx` đúng 5 cột · luồng import 4 bước chạy trọn (chọn file → Load lên bảng → Validate → Import),
2 dòng vào DB đúng trạng thái Hoạt động/Khóa; validate bắt đúng lỗi sai định dạng mã và mã cha
không tồn tại. 11/11 test BE vẫn xanh.
⚠️ **Lệch checklist, KHÔNG tự sửa**: `components/V2BaseImportToolbar.vue` chỉ bật nút Import khi
`invalidCount === 0`, tức còn dòng lỗi thì không import được — trong khi checklist
`erp-to-hrm-screen` mục F ghi "vẫn import được khi còn dòng lỗi (chỉ import dòng hợp lệ)". Đây là
component DÙNG CHUNG của mọi màn danh mục nên chờ user quyết; BE của cụm này đã xử lý sẵn trường
hợp import lẫn dòng lỗi (bỏ qua dòng lỗi, trả 207 kèm danh sách lỗi).
Import của Loại sản phẩm chỉ nhận trường đơn (mã cha, serial, có thể bán lẻ, số ngày tồn lâu);
thuộc tính / % VAT / 3 trường in tem nhập trong màn vì phụ thuộc danh mục khác.
Đang làm dở: (không) — còn lại là việc của user: rà soát rồi commit.
Bước tiếp theo: user nghiệm thu; nếu cần thì làm tài liệu SRS / test case.
Blocked: (không)

### Checkpoint — 18/09/2026 (Phase 3 xong + nghiệm thu bước đầu)
Vừa hoàn thành: nghiệm thu THẬT trên trình duyệt (FE repo chính ở `127.0.0.1:3002`, API repo chính
ở `127.0.0.1:8000`). Đã bấm tay: Tạo mới (lưu được, danh sách tự nạp lại, mới nhất trước) ·
validate 422 hiện lỗi inline · cây 3 cấp cha nối tầng ở màn Loại sản phẩm (chọn cha mới đổ được
con) · Khóa (toast "Khóa thành công.", badge đỏ, nút Sửa/Xóa **ẩn hẳn** đúng SRS, chỉ còn Mở khóa) ·
3 cột in tem mặc định ẩn (18/21 cột).
2 lỗi tự phát hiện và đã sửa: (1) khai `defaultHidden: true` vô tác dụng — `columnCustomizationMixin`
nhận `isVisible: false`; (2) id popup xác nhận của 5 màn còn mang tên màn gốc `*-product-nature`.
⚠️ Bài học khi test select2 bằng Playwright: **đừng set giá trị bằng jQuery** (`$(sel).val().trigger`)
— select2 mất đồng bộ với v-model và mọi thao tác sau đó đều sai, dễ kết luận nhầm là lỗi code.
Phải click combobox rồi click `li.select2-results__option`.
Môi trường: đã tắt server API cũ của worktree (PID 22152) và chạy lại cổng 8000 từ repo chính
(user duyệt). FE cổng 3000 vẫn là bản worktree; bản để xem tính năng mới là **3002**.
Dữ liệu mẫu để xem thử trên local: TCHH.0001 · TCHH.0002 · NCN.0001 · NSP.0001 · LSP.0001 (đang khóa).
Đang làm dở: Phase 4 (Import/Xuất Excel) chưa bắt đầu; Phase 5 còn nghiệm thu 4 màn còn lại.
Bước tiếp theo: Phase 4 Task 4.1.
Blocked: (không)

### Checkpoint — 18/09/2026 (Phase 3 xong)
Vừa hoàn thành: **Phase 3 đủ 7 task** — menu nhóm "Hàng hóa" (6 mục, gate theo quyền, không trùng
link phân hệ khác) + 6 màn `pages/master-data/<slug>/` (index.vue + modal) dựng theo khuôn
`pages/assign/customer-scopes/`, dùng chung `utils/product-classification.js`.
Verify: parse sạch 12 file `.vue` bằng vue-template-compiler + babel; khối grep tự kiểm của
`erp-to-hrm-screen` ra **0 vi phạm**; `localStorageKey` / `columnScreenKey` của 6 màn đều duy nhất.
BE bổ sung `CatalogOptionController` (2 endpoint nguồn `product-attributes/getAll`,
`tax-rates/getAll`) — đã gọi thử thật, trả 40 thuế suất và 444 thuộc tính.
⚠️ Đã sửa 1 lỗi chặn: controller con thu hẹp type-hint so với base gây fatal error PHP 7.4 —
base đổi sang các helper `respond*`, con khai action public có type-hint Entity.
⚠️ Chưa làm được ở Phase 3: tooltip ⓘ ở TIÊU ĐỀ MÀN (V2BaseDataTable không có slot cạnh title,
thêm slot là sửa component dùng chung → chờ user duyệt). Hiện tooltip nằm ở tiêu đề modal.
Đang làm dở: chưa bắt đầu Phase 4 (Import/Xuất Excel).
Bước tiếp theo: Phase 4 Task 4.1, hoặc nghiệm thu trình duyệt trước nếu user muốn.
Blocked: nghiệm thu Playwright cần API chạy từ repo chính — cổng 8000 hiện do server của worktree
`.worktrees/gop-db` giữ (đang chạy code nhánh khác nên route mới trả 404).
Đang tạm dùng server phụ `127.0.0.1:8002` chạy từ repo chính để kiểm API.

### Checkpoint — 18/09/2026 (Phase 2 xong)
Vừa hoàn thành: **Phase 2 đủ 7 task**. BE hoàn chỉnh cho cả 6 danh mục, dựng theo 4 lớp nền dùng
chung để 6 danh mục không chép code: `BaseCatalogModel` / `BaseCatalogService` /
`BaseCatalogRequest` / `BaseCatalogController` + trait `ChecksParentCatalog`.
Verify thật: **36/36 route** khớp đúng controller (kiểm bằng `Route::match`, vì `route:list` của
repo đang lỗi sẵn ở `PermissionHelper`); **11/11 test xanh**
(`Modules/MasterData/Tests/Feature/ProductClassificationCatalogTest.php`).
Bổ sung so với spec (theo SRS quy tắc chung mục 11, spec ban đầu thiếu): không xóa được bản ghi
**đang khóa**; chỉ **khóa** được khi không còn danh mục con đang hoạt động; chỉ **mở khóa** được
khi danh mục cha đang hoạt động. Thông báo chặn xóa dùng nguyên văn QLDA_015.
⚠️ Bẫy đã tránh: quan hệ thuộc tính của `ProductType` đặt tên `productAttributes()` — tên
`attributes()` đụng `$model->attributes` nội bộ của Eloquent, quan hệ sẽ không bao giờ lấy được.
Đang làm dở: chưa bắt đầu Phase 3 (FE).
Bước tiếp theo: Phase 3 Task 3.1 — thêm nhóm menu "Hàng hóa" vào `master-data.js`.
Blocked: (không)

### Checkpoint — 18/09/2026 (Phase 1 xong)
Vừa hoàn thành: **Phase 1 đủ 5 task**. 7 bảng đã `migrate` thật trên `gop_db` local
(`product_natures`, `product_function_groups`, `product_families`, `product_types`,
`business_policies`, `product_characteristics`, `product_type_attributes`); 12 quyền 1574-1585 đã
vào bảng `permissions`; 9 entity trong `Modules/MasterData/Entities/ProductClassification/`
(có lớp cha dùng chung `BaseCatalogModel` + 2 model chỉ đọc `ErpAttribute` / `ErpTaxRate`).
Đã verify bằng tinker: tạo/xóa bản ghi, `status_name`, `barcode_template_name`, `isCanDelete()`
chặn khi còn cấp con, `attributes` 444 dòng hoạt động, `tax_rates` 40 dòng.
Đổi so với spec ban đầu: tên bảng Nhóm sản phẩm là **`product_families`** (user chốt, tránh nhầm
với `groups` của ERP).
Đang làm dở: chưa bắt đầu Phase 2.
Bước tiếp theo: Phase 2 Task 2.1 — API CRUD Tính chất hàng hóa.
Blocked: (không)
