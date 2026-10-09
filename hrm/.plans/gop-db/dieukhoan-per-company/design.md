# Thiết kế: Điều khoản báo giá / thanh toán per-company + config per-company

Ngày: 2026-09-24 · Branch: `gop_db` · Repo: HRM (`hrm-api` + `hrm-client`), có sửa ERP (`ERP/TanPhatDev`).

## Bối cảnh

Màn "Khai Quy chế – Cấu hình" (regulation-config) của HRM gộp cấu hình ERP. ERP có 2 màn quản lý điều khoản (`quotation_terms` theo loại báo giá, `payment_method_terms` theo phương thức thanh toán) là **master-data toàn cục** (không `company_id`, không hẹn ngày). User muốn port 2 màn này vào regulation-config **nhưng tách theo công ty** (mỗi công ty một danh sách riêng), khác ERP hiện tại.

Mở rộng: user chốt chuyển **toàn bộ ~17 field đang global** (hiển thị trong khung "Theo công ty" nhưng thực chất dùng chung — `store='config'`) sang per-company, fake data cho mọi công ty giống bản global hiện có, và sửa code ERP đọc theo công ty.

### Quyết định đã chốt với user
1. **Cách 1** — dữ liệu tách riêng theo công ty (thêm `company_id`), KHÔNG giữ global. (Đi ngược tiền lệ gop_db "global giữ global" — user chấp nhận có chủ đích.)
2. **3a** — 8+11 dòng điều khoản cũ (đều do Tân Phát tạo, created_by 34/36) backfill về **công ty id 1** (Tân Phát mẹ). Công ty khác bắt đầu trống.
3. **4a** — sửa cả chiều ĐỌC bên ERP để lọc theo công ty.
4. Config storage: **Phương án A** — thêm `company_id` vào bảng `configs` + nhân bản row cho mỗi công ty + sửa `getConfig()` lọc theo công ty (1 chỗ gốc), thay vì sửa tay 76 điểm đọc.
5. **Chia 2 giai đoạn**, giao G1 trước.
6. **Bỏ qua** 2 key config chết khi migrate G2: `quotation_footer` (0 điểm đọc — đã giữ global ở Part A), `coefficient_cost_price_service` (0 điểm đọc cột config).
7. Modal thêm/sửa điều khoản dùng **rich-text (CKEditor)** cho `content`.
8. Quyền: **dùng chung gate màn regulation-config** ("Cài đặt cấu hình"), không tách permission riêng như ERP (id 169/174).

### Dữ liệu hiện trạng (DB `erp_hrm_check`, dùng chung ERP+HRM)
- `quotation_terms`: 8 dòng · cột `[id,title,content,type,created_by,updated_by,created_at,updated_at]` · KHÔNG `company_id`.
- `payment_method_terms`: 11 dòng · cột `[id,title,content,payment_method_id,created_by,updated_by,created_at,updated_at]` · KHÔNG `company_id`.
- `configs`: **singleton 1 row, 49 cột, KHÔNG `company_id`**; phát tán nguyên object qua 3 kênh (AppServiceProvider share `$config`; `layout/app.blade.php:286` `CONFIG=@json`; 12 partial `this.config=@json(getConfig())`).
- 8 công ty (id 1-8); Tân Phát mẹ = id 1.

### Enum (mirror ERP)
- Loại báo giá (`quotation_terms.type`): 1 Báo giá bán hàng · 2 Báo giá thúc đẩy bán · 3 Báo giá gói dịch vụ · 4 Báo giá dự án · 7 Báo giá sửa chữa và vật tư thay thế. (Nguồn: `ERP .../app/Model/Common/QuotationTerm.php::TYPES`.)
- Phương thức thanh toán (`payment_method_terms.payment_method_id`): 1 Thanh toán khi giao hàng · 2 Thanh toán gối đầu · 3 Thanh toán ngay · 4 Thanh toán theo tháng. (Nguồn: `ERP public/js/constant.js:259` `RULE_CONTRACT_PAYMENT_METHODS`.)

---

## GIAI ĐOẠN 1 — 2 thư viện điều khoản per-company (giao trước)

Phạm vi: chỉ MÀN QUẢN LÝ (CRUD) trong regulation-config + sửa chiều đọc ERP lọc công ty. KHÔNG đụng luồng lập báo giá/hợp đồng HRM (chưa port).

### 1.1 Schema
- Migration HRM `Modules/MasterData/Database/Migrations/`:
  - `quotation_terms`: `ADD company_id BIGINT UNSIGNED NULL, INDEX`.
  - `payment_method_terms`: `ADD company_id BIGINT UNSIGNED NULL, INDEX`.
  - Nullable để ERP-tolerant; sau backfill mọi dòng đều có giá trị.
- Backfill trong `up()`: `UPDATE ... SET company_id = 1 WHERE company_id IS NULL`.
- `down()`: drop cột (KHÔNG xoá dữ liệu điều khoản).

### 1.2 Backend (hrm-api)
- Model `Modules/MasterData/Entities/QuotationTerm.php`, `PaymentMethodTerm.php`:
  - `$table` trỏ bảng ERP có sẵn; `$fillable = [title, content, type|payment_method_id, company_id]`.
  - Hằng `TYPES` / `PAYMENT_METHODS` (mirror ERP) — dùng cho options FE + validate.
- Service/CRUD per-company: thêm nhóm method vào `RegulationConfigService` (hoặc service mới `RegulationTermService`) — `listTerms(tabKey, companyId)`, `createTerm`, `updateTerm(id, companyId)` (ownership check `company_id===companyId`, abort 403 nếu khác), `deleteTerm(id, companyId)` (ownership check). Gán `company_id`, `created_by`/`updated_by` = actor.
  - Lý do viết riêng (không tái dùng SHAPE_GRID): grid hiện hard-code `Regulation::class` + scope Department.
- Controller `RegulationConfigController`: thêm route CRUD cho tab dạng "library":
  - `GET  master-data/regulation-config/{tabKey}` (mở rộng `show` nhận tab library → trả `{fields, rows}` lọc theo company đang chọn).
  - `POST/PUT/DELETE master-data/regulation-config/{tabKey}/terms[/{id}]`.
  - Gate: `guard('Cài đặt cấu hình')` như các route khác.
  - Resolve companyId: dùng lại cơ chế regulation-config đang dùng cho scope company (theo tài khoản đăng nhập).
- Registry `RegulationTabRegistry`: thêm 2 tab `dieukhoan_baogia`, `dieukhoan_thanhtoan` với shape mới `SHAPE_LIBRARY` (scope company, no_hen, không staging version), fields = đặc tả cột (title/type|payment_method/content-rich). Cập nhật API filter (`scalarCompanyKeys`... bỏ qua shape LIBRARY như đã bỏ qua GRID).
- Lịch sử: KHÔNG ghi `regulation_config_histories` (bám ERP). Chỉ `created_by`/`updated_by`.

### 1.3 Frontend (hrm-client)
- `components/regulation-config/data.js`: 2 tab mới trong `DATA.company.groups`, `subsystem: 'sale'`, type mới `'library'` (hoặc tái dùng `'grid'` với cờ `noHen`+`companyScope`). Cột: `title` (text), discriminator (select enum), `content` (rich).
- `RegulationConfigScreen.vue`:
  - Thêm 2 tab vào const phân loại phù hợp (tách khỏi GRID_DEPT_TABS vì scope company); nạp qua endpoint mới; render bảng danh sách + nút Sửa/Xoá.
  - Modal thêm/sửa: input `title`, select enum, **rich editor CKEditor** cho `content` (bổ sung vào modal — hiện modal grid chỉ input thường).
  - Không hiện nút "Lưu cấu hình" đầu trang cho 2 tab này (CRUD từng dòng), không cột hẹn ngày.
- Tab hiển thị dưới phạm vi "Theo công ty" ở `/sale/regulation-config` (cần có công ty đang chọn).

### 1.4 ERP (chiều đọc — `ERP/TanPhatDev`)
- `app/Model/Common/QuotationTerm.php::getForSelect($type)`: thêm `->where('company_id', <current_company>)`.
- `app/Model/Common/PaymentMethodTerm.php::getForSelect()`: thêm `->where('company_id', <current_company>)`.
- **Điểm cần khoá khi viết plan**: cách ERP xác định "công ty đăng nhập hiện tại" (helper/session/auth). Xác minh nguồn chuẩn trước khi sửa.
- **BỎ 2 màn admin điều khoản bên ERP** (chốt 1-ii): từ giờ chỉ quản lý điều khoản qua HRM. Gỡ ở ERP: route group `quotation_terms` + `payment_method_terms` (`routes/web.php:5551-5571`), 2 mục menu (`topmenubar.blade.php:2002-2003`), 2 controller (`QuotationTermsController`/`PaymentMethodTermsController`), 2 thư mục view (`common/quotation_terms/`, `common/payment_method_terms/`). GIỮ 2 model (ERP vẫn dùng `getForSelect` để tiêu thụ). → Không còn nguồn tạo dòng `company_id` NULL từ ERP.

### 1.5 Test
- BE feature test: tạo/sửa/xoá term theo company; cách ly (company A không thấy/không sửa được term company B → 403).
- Playwright: đăng nhập, vào `/sale/regulation-config`, 2 tab điều khoản, thêm/sửa/xoá 1 dòng, rich editor lưu đúng HTML.
- Regression ERP (thủ công/tinker): `getForSelect` lọc đúng công ty; dropdown báo giá ERP cho Tân Phát vẫn thấy 8+11 dòng cũ.

### 1.6 Rủi ro & lưu ý G1
- Bảng dùng chung ERP: thêm cột an toàn (nullable), nhưng phải test ERP không vỡ.
- Bỏ 2 màn admin ERP (1-ii): kiểm tra không còn chỗ nào ERP link tới route đã gỡ (tránh 404); giữ 2 model để `getForSelect` chạy.
- CKEditor trong modal grid là hạng mục FE mới, cần dựng cẩn thận.

---

## GIAI ĐOẠN 2 — 17 field config sang per-company

> **Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-09-24-config-per-company-g2-design.md` (schema/migration/API/validation/business-rule/edge-case/testing đầy đủ). Mục này chỉ là tóm tắt.

Phương án A + 5 quyết định đã CHỐT với user (2026-09-24):
1. **Schema**: `configs` ADD `company_id`; backfill row singleton → công ty 1; nhân bản row cho **MỌI công ty trong bảng `companies`** (không hardcode 1-8), clone kèm `contract_rows` → hành vi ngày đầu không đổi. Migration idempotent, đặt ở HRM.
2. **`Config::getConfig($column = null, $companyId = null)`** — resolve: `$companyId` param → `auth()->user()->info->company_id` → **fallback công ty 1** (auth null hoặc công ty chưa có row). 1 chỗ gốc → 166 điểm đọc + 3 kênh share (`AppServiceProvider`, `app.blade.php:286`, các partial `@json`) tự đúng công ty. Đổi 4 điểm `Config::first()` thô sang `getConfig()`.
3. **ConfigsController (ERP) → per-company (hướng A)**: edit/update đọc-ghi row công ty đăng nhập; giữ màn admin, mỗi công ty tự sửa config mình. Guard: công ty chưa có row thì tạo row mới, không ghi đè công ty 1.
4. **Console command** (BorrowWarning/PrepickWarning): lặp per-company, `getConfig('warning_day', $companyId)`, scope dữ liệu cảnh báo theo công ty — **điểm regression trọng yếu** (dễ gửi trùng).
5. **17 field regulation-config**: chuyển từ SCOPE_GLOBAL(scope_id=0)/configs-singleton sang **cơ chế company-scope sẵn có** — version `scope_type='company'`, `scope_id=companyId`, ghi `configs WHERE company_id`; lịch sử + hẹn-ngày theo pattern `store='company'`. `subtableFkValue` contract_rows resolve config_id theo công ty.
6. **2 cột chết** `quotation_footer` + `coefficient_cost_price_service`: **ẨN** khỏi UI HRM (FE data.js). GIỮ cột + write-path ERP; KHÔNG drop (DB dùng chung, phơi qua `CONFIG=@json`).
7. **hrm-client KHÔNG đụng** — client chỉ nhận cửa sổ ngày BE tính sẵn, không đọc key config ERP.

Cụm nóng cần test regression: `warning_day` (kho + 2 console), `quotation_valid_days`, `coefficient_ecommerce_price`, `customer_register_expiry`, cụm `is_*`+`department_groups`+`customer_groups` (báo giá firm). Kiểm chứng: công ty 1 y hệt trước G2; công ty khác đọc cùng giá trị công ty 1 tới khi cấu hình riêng.

---

## Ngoài phạm vi
- Port luồng lập báo giá/hợp đồng HRM (tiêu thụ điều khoản) — feature khác.
- G2 (chi tiết): đã có spec `docs/superpowers/specs/gop-db/2026-09-24-config-per-company-g2-design.md`.
- Port 23 cột config còn lại vào UI HRM; auto-tạo row config khi tạo công ty mới — ngoài phạm vi G2 (xem mục 11 spec).
