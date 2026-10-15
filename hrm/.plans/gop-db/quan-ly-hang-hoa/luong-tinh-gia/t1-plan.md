# T1 — Chính sách giá bán nội bộ (plan, 11/10/2026)

> Nguồn: design `design.md` §3.2 + §4 + §7 · thiết kế màn §28 (`man-danh-muc-hang-hoa/design.md:1849–2022`) · mockup đã chốt
> màn `sc-cf` (trong `mockup-luong-tinh-gia.html`, giữ nguyên bản Phase 2) · chốt D13, D13a–d, P1 (`ton.md`).
> ✅ **User cho "LÀM" 11/10/2026** — đúng phạm vi mục 0, kể cả chạy 3 migration + seeder 1656 vào `hrm_erp_giacty`.

## Checkpoint
- [x] nhánh · [x] migration + seeder (chạy giacty) · [x] BE + PHPUnit · [x] FE menu + trang hub + panel + popup (hrm-client 8d28f7489) · [~] Playwright đo (đã đo trên API GIẢ LẬP — còn đo trên BE thật) · [x] e2e spec (chưa chạy) · [ ] merge LOCAL

## 0. Phạm vi xin "làm"

| | |
|---|---|
| Repo | hrm-api + hrm-client tại worktree `websites/wt-chuyen-doi-hang-hoa` |
| Nhánh | `feat/t1-chinh-sach-gia-noi-bo` checkout từ nhánh chung `feat/chuyen-doi-hang-hoa`; xong merge LOCAL về nhánh chung (không push tới khi user cho; KHÔNG đụng gop_db) |
| DB | `hrm_erp_giacty`: chạy 3 migration mới + seeder riêng quyền 1656 (chèn 1 dòng, không chạy cả seeder chính); sao lưu 3 bảng trước (bảng mới — chỉ cần ghi batch) |
| Không đụng | ERP, luồng chứng từ (T2+), G4/G5 |

## 1. CSDL (Modules/MasterData/Database/Migrations, guard hasTable)

| Bảng | Cột | Ràng buộc |
|---|---|---|
| `internal_price_policies` | id · owner_company_id · manufacture_id · base_type tinyint (1 giá vốn · 2 giá bán) · status tinyint (1 hoạt động · 2 khoá — P1) · created_by/updated_by · timestamps | UNIQUE(owner_company_id, manufacture_id); index(owner_company_id, status) |
| `internal_price_policy_targets` | id · policy_id FK cascade · target_company_id · percent_import_lot decimal(5,2) · percent_stock decimal(5,2) · created_by/updated_by · timestamps | UNIQUE(policy_id, target_company_id); CHECK 0–100 ở BE |
| `internal_price_policy_settings` | id · owner_company_id UNIQUE · coefficient_mode tinyint (1 theo công ty · 2 chung) · audit | |

Lịch sử: `catalog_histories` qua `CatalogHistoryService::log/logUpdate/logStatus` (entity = policy cha).

## 2. Quyền

Seeder riêng `InternalPricePolicyPermissionSeeder` (khuôn `ProductPricePermissionSeeder`): chèn **1656 "Cấu hình chính sách giá bán nội bộ"**, type 8, guard api; idempotent, id/tên bị chiếm thì dừng, không gán role. Kiểm `uniq -d` seeder + DB trước khi chạy. Test cấp quyền qua role tạm (memory: quyền chỉ đọc qua role, xoá cache spatie).

## 3. BE — `Modules/MasterData` (cạnh ProductPrice), prefix `master-data/internal-price-policies`, mọi route gate 1656, công ty = `CompanyHelper` công ty đang làm việc (không tin id FE)

| Endpoint | Việc |
|---|---|
| `GET /` | lưới của công ty bán: chính sách (kèm targets, cập nhật gần nhất theo từng công ty mua), lọc: tìm hãng · công ty mua · chỉ công ty đã khai · gồm hãng khoá; + settings `coefficient_mode` + danh sách công ty mua (mọi công ty trừ công ty bán, thứ tự theo `companies` — công ty đầu dùng cho Hệ số chung) |
| `GET /manufacturers` | popup chọn hãng: 1.071 hãng, tìm mã/tên, 80 dòng/lượt, cờ "đã có trên lưới", **số mã hàng của công ty bán** theo hãng (0 ⇒ "chưa có hàng" — D13b), hãng khoá gắn 🔒 |
| `PUT /{manufacture}` | lưu MỘT hãng: base_type + targets; validate đồng thời mọi ô (0 ≤ % ≤ 100, 2 số lẻ; khai 1 ô bỏ ô kia ⇒ lỗi ô trống; 2 ô trống ⇒ xoá target đó — D13c); coefficient_mode = chung ⇒ BE ép mọi target = target công ty đầu; ghi lịch sử từng thay đổi |
| `POST /bulk` | "Lưu N hãng đã đổi" — mỗi hãng một transaction, trả lỗi theo hãng |
| `PATCH /{id}/lock` · `/unlock` | khoá / mở khoá (P1), log nhóm Thay đổi trạng thái |
| `PUT /settings` | đổi coefficient_mode (log) |
| `GET /{id}/preview` | xem trước giá (mẫu hàng của hãng) — giá vốn chỉ trả khi có 1092 |
| `GET /{id}/histories` | lịch sử theo hãng (khuôn entity-history) |
| `GET /export` · `POST /import/validate` · `POST /import` | Excel theo skill import-excel / export-excel; import chỉ nạp dòng hợp lệ lên lưới (FE vẫn phải Lưu) |
| `GET /lookup?product_id=&company_id=` | tra chính sách cho (hàng, công ty mua) — dùng ở T4/T5; hãng khoá ⇒ coi như không có |
| SettingHistory adapter `internal_price_policy` | nút Lịch sử của hub (toàn bộ thay đổi của công ty bán) |

PHPUnit (Modules/MasterData/Tests): CRUD + validate đồng thời + hệ số chung + khoá/mở khoá + chặn công ty khác (403/không thấy) + không quyền 403 + lookup bỏ qua hãng khoá + lịch sử ghi đủ 3 nhóm.

## 4. FE — hrm-client

| Việc | Chi tiết |
|---|---|
| Menu | `sale-hub.js`: thêm mục **Cấu hình** cuối rail phân hệ Bán hàng ⇒ `/sale/settings`, isShow `['Cấu hình chính sách giá bán nội bộ']` (khuôn `meeting.js:119`; xác minh `SaleHubSidebar` có hỗ trợ mục link trực tiếp — chưa có thì thêm nhánh tối thiểu) |
| Trang | `pages/sale/settings/index.vue` chép khuôn `pages/meeting/settings/index.vue` (`.dtop` + cột hub `.subcats` + panel `.subdetail`, nút Lịch sử theo hub). 1 hub: **Chính sách giá bán nội bộ** (component `components/sale/settings/InternalPricePolicyPanel.vue`) |
| Panel | lưới §28d: hãng gộp dòng (STT · Hãng · Cách tính · Công ty mua · NK% · TK% · Cập nhật gần nhất · Hành động: Lưu / Xem trước / Lịch sử / Khoá-Mở khoá / Bỏ khỏi lưới cho hãng chưa lưu); thanh tiêu đề: Cách khai báo (Hệ số theo công ty / chung + ⓘ) · Chọn hãng · Import (cam) · Xuất (xanh lá); bộ lọc 1 hàng; ô đổi tô vàng; nút chân "Lưu N hãng đã đổi"; unsaved popup (chặn đổi menu + đổi công ty); không cuộn ngang; hàng ghim 38px; màu định danh công ty mua |
| Popup | Chọn hãng (giữ tick khi đổi từ khoá — bẫy §28d-bis) · Xem trước giá · Lịch sử (CatalogHistoryModal / entity-history) · Import (`V2BaseImportModal`) · xác nhận Khoá |
| Hãng khoá | dòng xám + 🔒, khoá mọi ô, nút Mở khoá |

## 5. Kiểm (bắt buộc trước khi báo xong)

- Playwright MCP đo DOM ở 1440 + 1280: không tràn ngang trong panel hub, hàng 38px đều, ô gộp phủ khít, tô vàng ô đổi, validate báo đồng thời, hệ số chung lan + khoá ô, popup chọn hãng giữ tick, unsaved popup chặn 2 lối rời, khoá/mở khoá, tooltip ⓘ không tràn.
- So trực tiếp với mockup `sc-cf` (memory: e2e UI phải kiểm khuôn).
- e2e (sửa/thêm spec, không tự chạy cả bộ trừ khi user yêu cầu — memory): có quyền + **không quyền** (menu ẩn, URL 404/403, API 403).
- PHPUnit MasterData chạy lại toàn bộ trên giacty.

## 6. Tự chốt (thuần UI / suy ra) — báo user khi xin "làm"

1. Thứ tự công ty mua theo thứ tự bảng `companies` (bỏ công ty bán); công ty đầu là nơi khai khi "Hệ số chung".
2. Có 2 lối lịch sử: nút **Lịch sử** của hub (mọi thay đổi của công ty bán, khuôn Meeting) + nút **Lịch sử** theo hãng trong lưới (§28d).
3. Hub `/sale/settings` đợt này chỉ có 1 nhóm "Chính sách giá bán nội bộ"; KHÔNG dời "Cấu hình duyệt giá" / "Khai Quy chế – Cấu hình" (đang ở nhóm Quy chế – Thiết lập) — muốn gom thì mở việc riêng.
4. Chính sách hãng đang khoá coi như không có ở `lookup` (YCTG/PTG hiện "Chưa cấu hình").

## 7. Hợp đồng API (chốt để BE và FE làm song song)

Prefix `api/v1/master-data/internal-price-policies` (theo cách khai group `Modules/MasterData/Routes/api.php` như `product-prices`),
middleware `checkPermission:Cấu hình chính sách giá bán nội bộ`. Công ty bán = `CompanyHelper` công ty đang làm việc — mọi id công ty
FE gửi lên đều bị bỏ qua / kiểm. Response bọc theo khuôn controller G4 (`ProductPriceController`): `{ data: ... }`, lỗi validate 422
`{ message, errors: { "<path>": ["..."] } }` (báo đồng thời mọi ô). Route tĩnh đứng TRƯỚC route `{id}`.

### 7.1 `GET /` — lưới
Query: `search` (mã/tên hãng) · `target_company_id` · `only_declared` (0/1) · `include_locked` (0/1, mặc định 1).
```json
{ "data": {
  "owner": { "id": 1, "name": "TÂN PHÁT" },
  "coefficient_mode": 1,                       // 1 theo công ty · 2 chung
  "targets": [ { "id": 2, "name": "CN HẢI PHÒNG …" }, ... ],   // công ty đang hoạt động (companies.status = 1) trừ owner, thứ tự id
  "policies": [ {
    "id": 12, "manufacture": { "id": 77, "code": "MLER", "name": "Muller", "locked": false },  // locked = manufactures.status<>1 (🔒)
    "base_type": 1, "status": 1,               // status 1 hoạt động · 2 khoá
    "rows": [ { "target_company_id": 2, "percent_import_lot": "1.00", "percent_stock": "2.00",
                "updated_at": "23/09/2026 14:05:32", "updated_by": "Nguyễn Văn An" } ]   // chỉ target đã khai
  } ]                                          // sắp theo updated_at mới nhất trước
} }
```

### 7.2 `GET /manufacturers` — popup chọn hãng
Query `search`, `limit` (mặc định 80). `{ data: { total: 1071, matched: 37, items: [ { id, code, name, locked, product_count, on_grid } ] } }`
`product_count` = số hàng mà công ty bán đang quản lý (`products.company_id` = owner, chưa xoá) theo `products.manufacture_id`.

### 7.3 `PUT /{manufacture_id}` — lưu một hãng (tạo mới nếu chưa có)
Body `{ "base_type": 1, "rows": [ { "target_company_id": 2, "percent_import_lot": "1", "percent_stock": "2" }, ... ] }`
- Mỗi row: cả 2 ô trống ⇒ xoá target đó (nếu có) · 1 ô trống ⇒ lỗi `rows.{i}.percent_*` "Vui lòng nhập tỷ lệ" · số 0–100, ≤ 2 số lẻ.
- `target_company_id` phải là công ty mua hợp lệ (≠ owner). Policy đang khoá ⇒ 423 "Chính sách hãng đang khoá".
- `coefficient_mode = 2` ⇒ BE ép mọi row khai = row của công ty mua đầu danh sách (nếu row đầu trống ⇒ lấy row khai đầu tiên).
- Ghi lịch sử từng thay đổi (tạo / đổi cách tính / đổi % / bỏ công ty ⇒ `logStatus` nhóm Thay đổi trạng thái).
- Trả lại policy dạng 7.1.

### 7.4 `POST /bulk` — `{ items: [ { manufacture_id, base_type, rows } ] }` ⇒ `{ data: { saved: [policy...], errors: { "<manufacture_id>": {path:[msg]} } } }` (mỗi hãng 1 transaction, hãng lỗi không chặn hãng khác)
### 7.5 `PATCH /{id}/lock` · `PATCH /{id}/unlock` — khoá / mở khoá, log Thay đổi trạng thái; trả policy
### 7.6 `PUT /settings` — `{ coefficient_mode }`; log; trả `{ data: { coefficient_mode } }`
### 7.7 `GET /{id}/preview` — xem trước giá: lấy tối đa 5 hàng của hãng do owner quản lý (đang KD, có giá công ty owner)
`{ data: { base_type, items: [ { product: {id, code, name}, unit, cost_price|null, prices: { "1": 53500000, ... "6": ... },
  targets: [ { target_company_id, import_lot: {...}, stock: {...} } ] } ] } }` — theo giá vốn: `import_lot/stock = { cost: x }`; theo giá bán:
`{ "1": x, ..., "6": x }`; tròn trăm. `cost_price` + mọi số suy từ giá vốn = null khi không có quyền 1092.
### 7.8 `GET /{id}/histories` (+ `/filter-options`) — khuôn entity-history như `product-prices/histories/{product}` của G4
### 7.9 `GET /export` (cùng query 7.1) ⇒ file xlsx · `POST /import/validate` (file) ⇒ `{ data: { rows: [ {manufacture_code, target_company, base_type, percent_import_lot, percent_stock, errors:{field:msg}} ], valid, invalid } }` — CHỈ validate, không ghi; FE nạp dòng hợp lệ lên lưới rồi user bấm Lưu. File mẫu `GET /import/template`.
### 7.10 `GET /lookup?product_id=&company_id=` — (dùng T4/T5) chính sách của công ty quản lý hàng cho công ty mua: `{ data: null | { owner_company_id, manufacture_id, base_type, percent_import_lot, percent_stock, updated_at, updated_by } }`; policy khoá ⇒ null. Endpoint này gate riêng ở T4 (không gate 1656) — T1 chỉ viết service `InternalPricePolicyLookup::for(productId, buyerCompanyId)` + test, CHƯA mở route.
### 7.11 Lịch sử hub — SettingHistory adapter type `internal_price_policy` (permissions `['Cấu hình chính sách giá bán nội bộ']`, authorize: id = công ty đang làm việc) đọc log mọi policy của owner.

## Kết quả BE (11/10/2026)

- Nhánh `feat/t1-chinh-sach-gia-noi-bo` (hrm-api worktree), chưa merge/push.
- DB `hrm_erp_giacty`: 3 migration batch 433/434/435; seeder `InternalPricePolicyPermissionSeeder` chèn 1 dòng 1656 (type 8, nhóm "Hàng hoá"). Dòng 1656 khai thêm ở `PermissionsTableSeeder` (+2 dòng, 0 xoá).
- Code: `Modules/MasterData/{Entities,Services,Http/Controllers/V1}/InternalPricePolicy/*`, `Exports/InternalPricePolicyExport.php`, route group `internal-price-policies`, `CatalogHistoryService::GATED_TABLES` (+2 bảng), adapter `SettingHistory/Adapters/InternalPricePolicyAdapter.php`. Lookup = `InternalPricePolicyLookup::for()` (chưa mở route).
- PHPUnit: `InternalPricePolicyApiTest` 18 ca + `InternalPricePolicyPermissionSeederTest` 4 ca; đột biến bỏ kẹp công ty (findOwned / lưới) + luôn thấy giá vốn đều bị bắt.
- LỆCH hợp đồng §7 (FE cần biết):
  1. `GET /import/template` KHÔNG làm — skill import-excel bắt FE tự dựng file mẫu bằng `buildImportTemplate` (cột: Mã hãng · Công ty mua · Cách tính · Nhập khẩu (%) · Tồn kho (%)).
  2. `POST /import/validate` nhận `rows` JSON (V2BaseImportModal tự đọc file) HOẶC `file` .xlsx; mỗi dòng trả thêm `row`, `manufacture_id`, `target_company_id`, `base_type_value` (1/2), `is_valid`; `errors` = {field: "msg"} (chuỗi, không mảng). `target_company` nhận tên công ty hoặc id. Không có `POST /import`.
  3. Lỗi 423 trong bulk nằm ở `errors[<manufacture_id>].policy`.
  4. Policy trả thêm `updated_at` (mốc cha). Histories theo hãng: `GET /{id}/histories` + `GET /{id}/histories/filter-options`.
  5. `PUT /settings` CHỈ lưu chế độ (không lan dữ liệu); hệ số chung áp lúc lưu hãng (PUT/bulk lấy dòng đang lưu phủ bởi dòng gửi lên rồi ép) và ở Lookup (đọc dòng nguồn cho mọi công ty mua).

## Kết quả FE (11/10/2026)

- Commit hrm-client `8d28f7489` (nhánh `feat/t1-chinh-sach-gia-noi-bo`). File: `components/subsystem-menu/{sale-hub,sale}.js` ·
  `pages/sale/settings/index.vue` · `components/sale/settings/{InternalPricePolicyPanel,ManufacturerPickerModal,PricePreviewModal,PolicyHistoryModal,PolicyRowActions}.vue` + `internalPricePolicyModel.js` (hàm thuần).
- Menu: `sale-hub.js` khai NHÓM CÓ `link` (mục 1 cấp, khuôn `operation-hub.js`) — `hub.js` đã sẵn nhánh lọc nhóm `link` → nút rail; phải thêm
  nhánh `group.link` vào `sale.js::buildSaleTree` (12 dòng, khuôn `operation.js::buildTree`) để mục có trong cây registry ⇒ middleware
  `checkPermission` chặn URL. **KHÔNG sửa `SaleHubSidebar.vue`.** (`sale.js` ngoài danh sách file được giao — sửa vì bắt buộc cho gate URL.)
- Theo lệch hợp đồng BE: import gửi `rows` JSON, đọc `is_valid`/`base_type_value`/`manufacture_id`/`target_company_id`; file mẫu dựng
  bằng `buildImportTemplate` (5 cột); "Import" chỉ nạp dòng hợp lệ lên lưới; lỗi bulk `policy` hiện dưới tên hãng; lịch sử hãng gọi
  `{id}/histories` qua `SystemInfoSection` (đảo vai entityType=id, entityId='histories').
- Xem trước giá: số tính TẠI FE theo tỷ lệ đang hiện trên lưới (kể cả chưa lưu) từ `cost_price`/`prices` của 7.7; chỉ hãng đã lưu.
- Chặn đổi công ty: `BasicSubsystem.vue::saveCompanyId` không có hook ⇒ panel bắt cú bấm mục công ty ở pha CAPTURE (bám DOM
  `.topbar-dropdown` có `.fe-repeat`). Popup rời menu dùng `unsavedChildFormMixin` (chữ chuẩn, không có dòng "Còn N hãng"); popup đổi
  công ty có dòng "Còn N hãng chưa lưu".
- Đo Playwright (API giả lập, 1280 + 1440): lưới không cuộn ngang, dòng 38px, 0 tiêu đề cắt, 0 ô mất viền phải; tô vàng; validate 5 ô
  đỏ/0 request; bulk 1 POST; hệ số chung lan từ dòng khai đầu + ô kế thừa xám; picker giữ tick; khoá ⇒ PATCH /lock, dòng xám 🔒;
  popup chưa lưu ở menu + đổi công ty (0 request đổi công ty khi Ở lại). Không quyền (thật): rail không có "Cấu hình", URL ⇒ 404.
- e2e: `HRM/e2e/tests/sale/internal-price-policy.spec.ts` (P1–P7 có quyền qua role tạm 1656 + N1 không quyền) — CHƯA chạy.
- Chưa làm / để agent chính: đo lại trên BE thật (preview, lịch sử hãng, lịch sử hub, import file thật, export ?token=).


## Ghép + nghiệm thu (agent chính, 11/10/2026)

- Đo Playwright MCP trên BE THẬT (Nuxt 3031 + API 8031, giacty, e2e_assign + role tạm 1656 — đã gỡ): chọn hãng giữ tick qua đổi từ khoá ·
  lưới 2 hãng × 4 công ty mua đang hoạt động · validate báo đồng thời, 0 request khi còn lỗi · lưu đúng 1 `POST /bulk`, DB khớp
  (MLER TPHP 1/2 · TPV 1.5/2 · BOCH TPSG 3/4) · hệ số chung lan từ dòng khai đầu tiên, ô kế thừa khoá · khoá/mở khoá `PATCH lock/unlock`,
  dòng 🔒 khoá mọi ô · lịch sử theo hãng + xem trước (không 1092 ⇒ giá vốn "—") · popup chưa lưu chặn đổi menu ·
  1440 + 1280: không cuộn ngang, dòng 38px, 0 ô/tiêu đề bị cắt, viền phải đủ · KHÔNG quyền: rail không có "Cấu hình", URL ⇒ 404, API 403.
- 🐞 Bắt khi ghép: (1) trình duyệt MCP còn `page.route` giả lập của agent FE ⇒ màn hiện dữ liệu giả — gỡ `unrouteAll` mới đo thật;
  (2) tên công ty mua là tên pháp lý dài ⇒ cột bị cắt "CÔNG TY CỔ P…" 2 dòng như nhau ⇒ BE trả `code`, lưới/xem trước hiện mã (TPHP, TPV, TPSG, DTTDETEK);
  (3) ô vừa đổi VÀ sai chỉ thấy viền vàng ⇒ CSS cho viền đỏ thắng; (4) câu validate tự viết ⇒ chuẩn lang (CLAUDE.md HRM);
  (5) spec e2e chèn `roles.company_id` (cột đã gỡ trên DB gộp) ⇒ sửa.
- PHPUnit MasterData **358/358** (trước 332). Dữ liệu test đã dọn (0 policy / 0 history / 0 role tạm).
- Commit: api `f42e3c093` + `121388b18`, client `8d28f7489` + `8c5a5cb3f`; **merge LOCAL** api `d50ccd8b5`, client `c10f4148c` (chưa push).
- e2e spec `HRM/e2e/tests/sale/internal-price-policy.spec.ts` (8 ca) CHƯA chạy — chạy cho worktree phải truyền `BASE_URL=http://127.0.0.1:3031 API_BASE=http://127.0.0.1:8031 API_REPO=<worktree hrm-api>`.

## Sửa 11/10 — đổi vị trí màn (user)
User xem app: trang Cấu hình dạng hub làm panel co hẹp ⇒ chuyển sang menu **Quy chế - Thiết lập › Quy chế kinh doanh**, trang riêng
`/sale/internal-price-policies`. Gỡ `/sale/settings` + mục rail Cấu hình, trả `sale.js` về trước T1. Đo: bảng 957 → 1.157px (1440),
không cuộn ngang 1440/1280, dòng 38px; menu dẫn đúng màn (flyout "Quy chế kinh doanh" 4 chức năng). Spec e2e sửa URL + kiểm menu (chưa chạy).
Commit client `2086b9468`, merge LOCAL `ee302cedf`.
- Sửa tiếp 11/10 (user): bỏ tiêu đề + mô tả trong card (trùng topbar); mô tả vào ⓘ `pageTitleInfo` trên topbar; nút Lịch sử về cuối thanh nút
  lưới qua slot `#toolbar-end`. Đo 1440/1280: card không còn tiêu đề trùng, popover ⓘ đúng câu, 4 nút cùng hàng cách 12px, không tràn ngang.
  Commit client `0c48522d4`, merge LOCAL `345da2201`.
- Sửa tiếp 11/10 (user): hàng lọc phủ 100% bề ngang — Tìm hãng / Công ty mua giãn 3:2, phần thừa phải 0px (1440 + 1280). Client `0450fc8f7` (merge LOCAL).
- Ghi nhận khi kiểm: user lưu hãng 3M với 0 công ty mua ⇒ BE cho tạo policy rỗng (chỉ cách tính); hãng đó không còn "Bỏ khỏi lưới", chỉ Khoá được — hỏi user có cần chặn lưu khi chưa khai công ty nào.
- **e2e 11/10 (user yêu cầu)**: `internal-price-policy.spec.ts` chạy worktree (`BASE_URL=:3031 API_BASE=:8031 API_REPO=wt…/hrm-api --project=chromium --no-deps --workers=1`).
  Lượt 1: 7 passed + 1 flaky (P5 đo màu nền ô khoá giữa transition 0.15s của V2BaseInput ⇒ sửa spec `expect.poll`). Lượt 2 + 3 (`--retries=0`): **8/8 passed**.
  Spec bổ sung dọn `catalog_histories` do tài khoản test ghi từ lúc chạy (lượt 1–2 sót 16 dòng, đã xoá tay). Sau chạy: 0 role tạm, chỉ còn hãng 3M + 5 dòng lịch sử của user.

### Checkpoint — 2026-10-11 (wrap up)
Vừa hoàn thành: T1 xong (BE f42e3c093/121388b18 · FE 8d28f7489/8c5a5cb3f/2086b9468/0c48522d4 + style hàng lọc) — merge LOCAL nhánh chung api `d50ccd8b5`, client `0450fc8f7`; PHPUnit MasterData 358/358; e2e 8/8.
Đang làm dở: không.
Bước tiếp theo: user trả lời ca hãng chưa khai công ty mua (3M) · push khi user cho · gỡ role tạm `T1_UAT_NAMDANG` khi user kiểm xong · plan T2.
Blocked: —

## T1b — P2 chặn hãng chưa khai công ty mua (11/10/2026, user cho "làm")
Phạm vi: worktree `wt-chuyen-doi-hang-hoa`, nhánh con `feat/t1b-chan-hang-rong` (2 repo) từ nhánh chung; không migration/seeder.
- [x] BE `InternalPricePolicyService::save`: sau validate ô, xét trạng thái CUỐI (dòng đã lưu phủ bởi body; hệ số chung đã lan), chỉ tính công ty mua đang hoạt động — 0 công ty ⇒ 422 `rows: ["Phải nhập tỷ lệ cho ít nhất 1 công ty mua"]` (bulk: `errors[hãng].rows`). Còn ô sai ⇒ chỉ báo lỗi ô.
- [x] PHPUnit: ca mới `chan_luu_hang_khong_con_cong_ty_mua_nao_xet_tren_trang_thai_cuoi`; đổi ca hệ số chung "không khai ⇒ để trống" thành chặn; ca lưới lọc chèn policy rỗng bằng DB (dữ liệu cũ kiểu 3M); ca lịch sử hub đếm theo chênh lệch (công ty 1 có sẵn lịch sử user tạo tay 11:03). MasterData **359/359** (giacty).
- [x] FE: `validateEntry` thêm lỗi cấp hãng `_` (MSG_NO_TARGET); dấu * đỏ ở Cách tính / Nhập khẩu / Tồn kho (`.ipp-req`); div lỗi dưới tên hãng thêm class `field-error` để `scrollToFirstError` bắt; `revealErrors` bỏ qua khoá `_` (không gỡ bộ lọc vô cớ); gõ ô có giá trị ⇒ gỡ lỗi `_`; toast "ô" → "lỗi". Cột Nhập khẩu 112→120, Tồn kho 98→106 (dấu * làm 2 tiêu đề bị cắt 5–6px — đo ra khi kiểm).
- [x] Playwright MCP (BE thật 8031 + Nuxt 3031, e2e_assign + role tạm 107390 — đã gỡ): chọn 2 hãng mới, bấm Lưu ⇒ 0 request ghi, lỗi dưới tên cả 2 hãng (đỏ 11.5px, nằm trong ô), tự cuộn tới lỗi khi đang ở đáy; 1440 + 1280: 0 tiêu đề cắt, không cuộn ngang, dòng 38px, 0 ô mất viền phải; gõ 1 ô ⇒ lỗi hãng đó mất, hãng kia giữ; xoá trắng + Lưu ⇒ lỗi quay lại. Hãng 3M (0 công ty): PUT đổi cách tính ⇒ 422, DB không đổi. Đổi select2 bằng automation không ăn ⇒ ca 3M chỉ kiểm qua API.
- [x] e2e: thêm ca **P2b** vào `HRM/e2e/tests/sale/internal-price-policy.spec.ts` — CHƯA chạy (chỉ chạy khi user yêu cầu).
- [ ] Commit 2 repo + merge LOCAL về `feat/chuyen-doi-hang-hoa` — vướng git (Xcode license chưa đồng ý sau cập nhật máy).
- Môi trường 11/10: máy mất `libffi` (php@7.4 không chạy) + mất Rosetta 2 (node 12 x86 không chạy) — user đã cài lại.
