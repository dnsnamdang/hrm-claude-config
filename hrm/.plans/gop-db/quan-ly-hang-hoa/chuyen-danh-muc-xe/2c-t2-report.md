# Report T2 — HRM FE Phase 2c (hrm-client) — 14/10/2026

**Trạng thái: DONE_WITH_CONCERNS** (xem §7).

Repo `wt-chuyen-doi-hang-hoa/hrm-client`, nhánh `feat/cdhh-2c-xe` (không merge, không push). Không sửa BE.
Nuxt 3031 / API 8031 đang chạy sẵn, KHÔNG restart.

## 1. Commit

| Hash | Nội dung |
|---|---|
| `7d2daca61` | 4 màn FE + menu nhóm "Xe" (10 file, menu `git diff --numstat` = 23 thêm / 0 xoá; file mới LF như khuôn) |

## 2. File

- `components/subsystem-menu/master-data.js` — nhóm "Xe" (`subItems`) thêm 4 mục sau "Tải trọng xe": Biển số xe · Lái xe ngoài · Danh mục xe · Nhiên liệu; `isShow` = cặp `Quản lý/Xem danh mục {biển số xe|lái xe ngoài|xe|nhiên liệu}` đúng chuỗi T1.
- `pages/master-data/license-plates/{index.vue, AddLicensePlateModal.vue}` — entity-type `license_plates`.
- `pages/master-data/external-drivers/{index.vue, AddExternalDriverModal.vue}` — entity-type `drives`; popup 6+3+3 / 4+4+4.
- `pages/master-data/fuels/{index.vue, AddFuelModal.vue}` — entity-type `fuels`; Giá dùng `V2BaseCurrencyInput` (precision 2), cột Giá `toLocaleString('en-US')`.
- `pages/master-data/vehicles/{index.vue, AddVehicleModal.vue, components/VehicleRemoteMultiSelect.vue}` — entity-type `vehicles`.

Quyết định:
- **Form xe = popup `size="xl"`** (không trang riêng): 10 màn nhóm Xe đều list-page + popup qua `vehicleCatalogScreenMixin`/`vehicleCatalogModalMixin`; 13 ô, không bảng con/tab ⇒ dùng lại nguyên bộ Xem/Sửa/Lịch sử/Lưu & Tiếp tục. Mỗi hàng đủ 12 cột (đo: 7 hàng đều = 12).
- **Tài xế công ty**: component mới `VehicleRemoteMultiSelect` (select2 `multiple` + `ajax.transport`, khuôn `V2BaseSelectRemote`) gọi `/vehicles/options/employees?keyword=` — endpoint giới hạn 50 dòng, công ty 1 có 402 NV nên KHÔNG nạp sẵn được. Đặt trong `pages/**/components/` (Nuxt bỏ qua, không thành route).
- **NCC**: `V2BaseSelectRemote` gọi `/vehicles/options/suppliers` (10.094 NCC đang hoạt động), `initialOption` khi Sửa. Lưu `customers.id` theo T1.
- Lái xe ngoài: `V2BaseSelectInModal` `:extraSettings="{ multiple: true }"` từ `external-drivers/getAll?include_ids[]=`; hiển thị "Tên - SĐT".
- Dây chuyền Hãng → Loại → Model lọc ở máy khách; xoá con trong `@change` (chỉ thao tác tay), không `watch` — nạp bản ghi Sửa không bị xoá oan. Bộ lọc danh sách xoá con trong `handleFilterChange` cùng nhịp (1 request).
- Payload chỉ mang ô của loại đang chọn (Tân Phát ⇒ company_id+department_id, NCC ⇒ owner; driver_type 1 ⇒ drivers, 2 ⇒ company_drivers) — BE tự null + dọn bảng nối.
- Giá trị đã khoá khi Sửa: `withLockedParent` cho hãng/loại/model/dòng/tải trọng/nhiên liệu; biển số + lái xe qua `include_ids`; công ty/bộ phận thiếu trong store ⇒ chèn kèm 🔒; NCC/NV qua initial option có 🔒.
- Popup Tạo mới mở NGAY, không chờ 2 request biển số/lái xe (lúc đầu await ⇒ popup chậm vài giây, e2e bắt được).
- Mặc định tạo mới: Xe nhà cung cấp + Lái xe ngoài (ERP `create.blade.php`: `is_tanphat = false`).
- Bộ cột mặc định đúng brief; thêm STT ở cả 4 màn (khuôn repo); "Người cập nhật/Ngày cập nhật" vẫn có trong Cấu hình cột nhưng `isVisible: false`. Lọc thêm Người tạo + Ngày tạo ở màn Xe; Lái xe ngoài lọc Tên · SĐT · CCCD · Số GPLX · Trạng thái · Người tạo · Ngày tạo.
- Định dạng số: `,` ngăn nghìn theo HRM/CLAUDE.md (chuẩn quốc tế, chốt 26/08) — brief ghi "định dạng số VN", CLAUDE.md thắng.

## 3. Đo bằng Playwright (MCP, DOM + request thật, e2e_assign, viewport 1440)

| Đo | Biển số | Lái xe ngoài | Nhiên liệu | Danh mục xe |
|---|---|---|---|---|
| Bộ cột (th) | STT · Biển số xe · Ghi chú · Trạng thái · Người tạo · Ngày tạo · Hành động | STT · Họ tên · SĐT · Năm sinh · CCCD · Số GPLX · Trạng thái · Người tạo · Ngày tạo · Hành động | STT · Tên nhiên liệu · Giá · Trạng thái · Người tạo · Ngày tạo · Hành động | STT · Biển số xe · Chủ xe · Hãng xe · Loại xe · Model xe · Dòng xe · Tải trọng · Nhiên liệu · Tài xế · Trạng thái · Người tạo · Ngày tạo · Hành động |
| Không lọc: dòng trang 1 / tổng | 10 / 163 | 10 / 72 | 4 / 4 | 10 / 137 |
| Lọc Trạng thái = Hoạt động: request | `status=1&…` | `status=1&…` | `status=1&…` | `status=1&…` |
| Tổng khi lọc Hoạt động (mốc DB) | **161** ✔ | **69** ✔ | **4** ✔ | **134** ✔ |

Màn Xe — ô lọc (request bắt thật): `license_plate=29` → 104 · `owner=Tân Phát` → 27 · Hãng Hino ⇒ `vehicle_manufact_id=141` (Loại xe 320 → 6 option, Model 1280 → 19) · + Loại HINO ⇒ `…&vehicle_brand_id=1308` (Model → 8, tổng 36) · đổi Hãng sang Acura ⇒ `vehicle_manufact_id=111` **không còn** `vehicle_brand_id`.
Nhiên liệu: cột Giá `26,150 · 19,500 · 21,490 · 27,460`; ô nhập gõ `1234567` hiện `1,234,567`, lưu ra danh sách `1,234,567`.

Form (thao tác thật, rồi dọn):
- Biển số: Lưu trống ⇒ "Bắt buộc phải nhập"; tạo `E2E2C-T2-01` lên danh sách; tạo trùng ⇒ ô báo "Đã tồn tại" (422 hiện tại ô).
- Lái xe ngoài: Lưu trống ⇒ **5** `.v2-error` cùng lúc; hàng [6,3,3] [4,4,4], mỗi hàng 1 dòng; năm sinh `19x5` ⇒ "Năm sinh phải gồm đúng 4 chữ số".
- Nhiên liệu: Lưu trống ⇒ 2 lỗi (Tên, Giá); tạo → xoá OK.
- Xe — Lưu trống ⇒ **9** lỗi cùng lúc (Biển số, Nhiên liệu, Hãng, Loại, Model, Dòng, Tải trọng, Nhà cung cấp, Lái xe ngoài); radio mặc định NCC + Lái xe ngoài; ô Biển số 29 option (biển còn trống); Loại xe disabled + 0 option trước khi chọn Hãng; Hino ⇒ 6 loại, HINO ⇒ 8 model; đổi sang Isuzu ⇒ Loại = "", Model = "" + disabled, Loại còn 9 option; bấm "Xe Tân Phát" ⇒ ô NCC biến mất, có Công ty (5 option) + Bộ phận (disabled tới khi chọn công ty, rồi 25 option); đổi "Tài xế công ty" ⇒ ô lái xe ngoài biến mất, ô NV gõ "Nguyễn" bắn `options/employees?keyword=Nguyễn`. POST payload: `is_tanphat:true, company_id:1, department_id:5, driver_type:2, company_drivers:[95]` (không có owner/drivers) ⇒ 200; DB `vehicle_company_drivers` có 1 dòng info_id 95.
- Sửa xe: hiện đủ 11 ô tên (biển, nhiên liệu, hãng, loại, model, dòng, tải trọng, công ty, bộ phận, "10610026 - Bùi Duy Trước"); đổi NCC (gõ HOANG ⇒ `options/suppliers?keyword=HOANG`) + Lái xe ngoài ⇒ PUT `is_tanphat:false, owner:40362, driver_type:1, drivers:[152]` (không company_*) ⇒ 200; dòng danh sách đổi "A HOÀNG / Xe nhà cung cấp", Tài xế "E2E2C Lai xe T2".
- Khoá biển số + lái xe thử (gọi `/license-plates/210/lock`, `/external-drivers/152/lock`) rồi mở Sửa xe ⇒ "🔒 E2E2C-T2-01", "🔒 E2E2C Lai xe T2 - 0900000222".
- Xem xe ⇒ "Xem chi tiết xe", Lịch sử gọi `catalog-histories/vehicles/156`. Khoá ⇒ `/vehicles/156/lock`, Mở khoá ⇒ `/vehicles/156/unlock` (200), Xoá ⇒ 200, dòng biến mất. Mở khoá lái xe/biển số gọi đúng `/unlock`, xoá 200.
- Quyền: chỉ Xem (role tạm bỏ 4 quyền Quản lý) ⇒ 4 màn: 0 nút "Tạo mới", cột Hành động chỉ còn "Lịch sử", tổng vẫn đúng. Không quyền ⇒ hub nhóm Xe còn 6 link, vào `/master-data/vehicles` bị đẩy `/pages/extras/404`. Đủ 8 quyền ⇒ hub nhóm Xe **10 link** (đếm DOM).

**Lỗi tái hiện được + đã sửa trong đợt**: ô Lái xe ngoài khai `multiple` trơn ⇒ select2 trả CHUỖI `"151"` ⇒ `buildPayload` nổ `(list || []).map is not a function`, bấm Lưu không bắn request, không toast (đo: `data.drivers = "151"`). Sửa: `:extraSettings="{ multiple: true }"` (khuôn repo) + `toIds` chấp nhận giá trị đơn. Ca e2e "sửa … gửi MẢNG drivers" chốt hành vi này (chưa chạy thử đột biến).

## 4. E2E (`wt-chuyen-doi-hang-hoa/e2e`, ngoài git) — node 20, `--no-deps --workers=1 --retries=0`, `API_BASE=…8031 BASE_URL=…3031`

- **Mới** `tests/master-data/vehicles-ui.spec.ts` (6 ca, serial; biển số + lái xe thử tạo bằng API, xe tạo bằng FORM; dọn SQL ở before/afterAll): **6 passed, 0 failed, 0 did not run**.
- **Sửa** `product-catalog-common.api.spec.ts`: thêm `license-plates`, `external-drivers` (kèm 4 ô bắt buộc), `fuels` (kèm price) vào `CATALOGS`. Kết quả cả file: **121 passed / 19 failed / 0 did not run**. 21 ca của 3 màn mới đều xanh. 19 đỏ là SẴN CÓ, không dính 2c: 17 ca "không có quyền → 403" của màn cũ (tài khoản `e2e_assign_nocost` 1181 trên DB này đang CÓ quyền Xem/Quản lý các danh mục đó) + 2 ca Thuế suất (`makeName` sinh 9xx.xx > trần 99,99 ⇒ 422).
- **Sửa** `product-catalog-ui.spec.ts`: thêm 3 màn vào ca bố cục popup 12 cột; ca menu nhóm Xe đổi 6 → 10 link. Cả file: **25 passed / 2 failed / 1 did not run**; chạy lại 2 ca đỏ: `fuels` bố cục **passed** (lần đầu hết giờ 30s lúc dev server dựng trang), `Loại sản phẩm — mẫu in tem` **vẫn đỏ** (popup Tạo mới không mở — màn `product-types`, không dính file nào của đợt này; chưa điều tra, ghi ngoài luồng) ⇒ 1 ca sau nó "did not run".

## 5. Role tạm

`TMP-2C-T2` id **120627** (công ty 1, 8 quyền 1699–1706, gắn NV 1180). Đã gỡ (employee_has_roles, role_has_permissions, roles = 0 dòng) + `cache:forget spatie.permission.cache`.

## 6. Số dòng bảng sau khi xong (đúng mốc)

`license_plates` 163 · `drives` 72 · `vehicles` 137 · `fuels` 4 · `vehicle_drivers` 110 · `vehicle_company_drivers` 74 · bản ghi `E2E%` ở 3 bảng: 0 · `catalog_histories` của 4 bảng: 0 (đã xoá 69 dòng lịch sử của bản ghi thử đã xoá, theo `table_id` > max id hiện tại).
⚠️ Spec common API chạy CRUD cả 15 màn cũ ⇒ để lại `catalog_histories` của bản ghi E2EPC đã xoá ở các bảng cũ (hành vi sẵn có của spec, không dọn).

## 7. Lo ngại / lệch brief

1. Form chưa validate phía FE (theo khuôn 2b: dựa 422 của BE, BE trả mọi ô cùng lúc). Bấm Lưu trống vẫn đi 1 request.
2. Ô Công ty lấy `$store.state.companies` (đo 5 công ty với e2e_assign, DB có 8) — nếu người dùng cần gắn xe cho công ty ngoài danh sách của mình thì không chọn được; BE không chặn.
3. Ô Tài xế công ty không lọc theo công ty của xe (gọi endpoint chỉ với `keyword`) — 50 dòng/lần, phải gõ để tìm.
4. Popup Tạo mới mở trước khi danh sách biển số về; mở dropdown quá sớm (<1s) sẽ thấy rỗng.
5. 2 xe hoạt động dùng chung 1 biển (T1 §7.4) — sửa 1 trong 2 xe sẽ 422 biển số; FE chỉ hiện câu lỗi ở ô.

## 8. Ngoài luồng (ghi nhận, không vá)

- **N-g** e2e `product-catalog-ui` ca "Loại sản phẩm — mẫu in tem": popup Tạo mới không mở trên cổng 3031 (e2e_assign có đủ quyền loại sản phẩm).
- **N-h** e2e `product-catalog-common.api`: 17 ca 403 đỏ vì `e2e_assign_nocost` đang có quyền danh mục cũ trên `hrm_erp_giacty`; 2 ca Thuế suất đỏ do giá trị sinh vượt trần 99,99.
- **N-i** Bất kỳ `V2BaseSelectInModal` nào khai `multiple` trơn (không `extraSettings`) sẽ trả chuỗi thay vì mảng — chỉ màn này dính (đã sửa); chưa rà màn khác.

---

## Vòng sửa 1 (theo `2c-review-t2.md` + BE fix1 `eda8ebbff`) — 14/10/2026

**Commit:** `43cc3c7fe` (hrm-client, `feat/cdhh-2c-xe`). Sửa 2 file: `AddVehicleModal.vue` (+42/−12), `VehicleRemoteMultiSelect.vue` (+24/−1). Không đụng BE, không đụng `V2BaseSelectRemote`.

### Đã sửa
- **I1** (chọn cách b, giữ cache): ô NCC (`@select` → `onSupplierSelect`) và ô Tài xế công ty (`@selected-options` → `onCompanyDriverOptions`) ghi nhãn giá trị đang chọn vào `supplierInitial` / `companyDriverInitial`. Ô bị `v-if` huỷ rồi dựng lại sẽ gieo lại đúng giá trị đó. Không xoá giá trị khi đổi radio: payload vốn chỉ gửi ô của loại đang chọn, giữ lại thì đổi nhầm rồi đổi về không mất dữ liệu.
  - **Tái hiện trước khi sửa** (tạm gỡ 2 binding, Playwright đo DOM): chọn NCC → Tân Phát → NCC thì ô hiện placeholder "Gõ mã hoặc tên…", nhưng payload vẫn có `owner: 43873`. Chọn NV "12611000 - Nguyễn Văn Bá" → Lái xe ngoài → Tài xế công ty thì **0 chip**, nhưng payload vẫn có `company_drivers: [1556]`.
  - **Sau khi sửa**: ô NCC hiện "29TPHXDA-243 - A HOÀNG" và payload `owner: 40362` (đúng NCC đó). Ô NV có 1 chip "12611000 - Nguyễn Văn Bá" và payload `company_drivers: [1556]`.
  - **Thử đột biến**: gỡ `@selected-options` thì ca e2e "tạo xe" đỏ ở `toHaveCount(1)` (nhận 0). Ca có giá trị thật.
- **I2**: `loadExternalDrivers` gọi `master-data/vehicles/options/external-drivers?include_ids[]=` và chỉ dựa `is_locked`. Đo: 69 option, 63 có hậu tố " - SĐT" (6 lái xe không có SĐT), mẫu "A Cang - 0977079657".
- **M2**: nhãn tài xế công ty thống nhất "Mã NV - Họ tên" (`code` + `fullname`), cả lúc tìm lẫn lúc mở Sửa.
- **M4**: công ty ngoài phạm vi `$store.state.companies` không gắn 🔒 nữa. Bộ phận thiếu trong store thì vẫn 🔒.
- **M6**: `mounted` cho mỗi nguồn `.catch(() => [])` riêng.
- **M1** (chỉ trong `VehicleRemoteMultiSelect`): `transport` trả `{ abort() }`. Hệ quả: (1) gõ tiếp thì kết quả của từ khoá cũ về muộn bị bỏ; (2) khi lỗi, select2 hiện "Không tải được dữ liệu" thay vì TypeError.

### E2E (node 20, `--no-deps --workers=1 --retries=0`, cổng 3031/8031)
- `vehicles-ui.spec.ts`: **8 passed / 0 failed / 0 did not run**. Thêm 2 ca:
  - Ca I1 ở form Tạo mới: đổi loại tài xế qua lại, chip giữ nguyên và `payload.company_drivers` = id của chip.
  - Ca I1 ở form Sửa: đổi chủ xe qua lại, ô NCC hiện lại đúng tên và `payload.owner` = id đang hiện.
  - Ca Sửa đo **mọi** ô select2 đang hiện (11 ô) đều có giá trị, không chỉ Hino.
  - `afterAll` dọn `catalog_histories` theo id biển số / lái xe / xe. Id xe lấy từ response POST.
  - Describe quyền mới (tài khoản nocost): **không quyền** ⇒ vào `/master-data/license-plates` và `/master-data/vehicles` bị đẩy sang 404. **Chỉ Xem** (role tạm `E2E2C-XEM-*` gồm 4 quyền Xem, `cache:forget spatie.permission.cache`) ⇒ 0 nút "Tạo mới", cột Hành động chỉ còn `['Lịch sử']`. Role tạm tự gỡ ở `beforeAll`/`afterAll`.
  - Comment đầu spec ghi rõ dữ liệu DB dev mà spec phụ thuộc (Hino/HINO/Isuzu, "CONG TY", "a").
- `product-catalog-ui.spec.ts`: thêm describe "3 màn xe 2c phẳng". Mỗi màn có 1 ca đo:
  - bộ cột;
  - Lịch sử gọi `/catalog-histories/{license_plates|drives|fuels}/{id}`;
  - Mở khoá gọi `/unlock`;
  - riêng Nhiên liệu: hiện `1,234,567` và mọi giá trên trang khớp `^\d{1,3}(,\d{3})*(\.\d+)?$`.

  Dữ liệu thử tạo bằng API, dọn kèm lịch sử. Kết quả cả file: **29 passed / 1 failed / 1 did not run**. Ca đỏ là "Loại sản phẩm — mẫu in tem" (N-g, có từ trước, không thuộc 2c); ca "did not run" là ca đứng sau nó.

### Role tạm / dữ liệu
- Role tạm đo tay `TMP-2C-T2-FIX1` id **121147** (8 quyền 1720–1727, NV 1180): đã gỡ, đã `cache:forget`.
- Role `E2E2C-XEM-*` của spec: 0 dòng.
- Số dòng bảng: `license_plates` 163 · `drives` 72 · `vehicles` 137 · `fuels` 4 · `vehicle_drivers` 110 · `vehicle_company_drivers` 74.
- `catalog_histories` của 4 bảng: 0.

### Ngoài luồng thêm
- **N-j** `V2BaseSelectRemote` (dùng chung, ~10 màn) vẫn mang bệnh M1: `transport` không trả `$request` ⇒ lỗi mạng làm dropdown kẹt ở "Đang tìm..." (TypeError), kết quả từ khoá cũ có thể đè kết quả mới. Chưa sửa theo chỉ đạo.
- M3 (`loadPlateOptions` không có seq), M5 (dữ liệu ERP có Loại không thuộc Hãng), M7 (không validate FE), M8 (tài xế công ty không lọc theo công ty) — chưa làm, giữ ở §7.
