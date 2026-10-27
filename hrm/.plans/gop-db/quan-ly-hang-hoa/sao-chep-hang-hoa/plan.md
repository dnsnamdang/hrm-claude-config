# Sao chép hàng hoá — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Nút "Sao chép" mở form tạo hàng hoá điền sẵn từ một hàng đang có ở công ty mình; Lưu đi đúng `POST products`.

**Architecture:** BE thêm `GET products/{id}/copy-data` (dữ liệu form đã làm sạch: bỏ id, lọc hàng kèm/máy bị chặn, bỏ
danh mục khoá, chép tệp tài liệu sang thư mục tạm S3) + cờ `can_copy` + `copy_from_id` ở `POST products` để ghi lịch sử.
FE: `create.vue?copy_from=` ⇒ `ProductForm` nạp `copy-data` thay `emptyForm`, hiện khối cảnh báo; nút ở 3 màn danh sách
+ footer chi tiết.

**Tech Stack:** Laravel 6 nwidart (`hrm-api/Modules/MasterData`), PHPUnit; Nuxt 2 / Vue 2 (`hrm-client`), Playwright MCP.

**Spec:** [design.md](design.md) (chốt S1–S9 + mục 6 Claude tự chốt) · nền: [khao-sat.md](khao-sat.md)

## Global Constraints

- Nhánh: `feat/sao-chep-hang-hoa` checkout từ `origin/gop_db`, ở **cả** hrm-api và hrm-client (user chốt 24/10). ERP không đụng.
- Không migration, không seeder, không quyền mới — dùng quyền "Xây dựng thông tin hàng hoá" có sẵn.
- Không chép giá. Bản sao: `products.company_id` = công ty đang làm, pcc 1, mã `ProductCodeGenerator` (đường tạo có sẵn).
- Ghi chú lịch sử đúng chữ: `Nhân bản từ <mã gốc>`.
- Tiêu đề trang khi nhân bản: `Nhân bản hàng hoá`. Nhãn nút: `Nhân bản` (S10 — button-convention), icon `ri-file-copy-line`.
- 403 chung của `copy-data`: `Không nhân bản được hàng hoá này.`
- PHPUnit KHÔNG chạy lên `hrm_erp_21_10_prod` (DB nguồn sẽ đưa đi — memory phpunit-chay-tren-db-env-de-lai-rac):
  chạy bằng `DB_DATABASE=<bản sao test> php artisan test …` / `vendor/bin/phpunit` với env đè; hỏi user DB test trước Task 1.
- Local S3 trỏ bucket PROD ⇒ test BE mock `CmcS3Helper`; Playwright giả lập `copy-data`/upload bằng `page.route` khi
  cần, không bấm thật vào tệp tài liệu.
- Không commit — để nguyên chưa commit, user tự báo (memory khong-hoi-commit-user-tu-bao). Không `git stash`.
- FE: theo `button-convention`, `select-and-input-state` (🔒), `unsaved-changes`; đo DOM bằng Playwright trước khi báo xong.

## Review Focus

1. Hàng gốc có hàng kèm/máy đã gắn từ trước nay bị khoá ⇒ bản sao phải lưu được (đã lọc), không 422 — test ở Task 3.
2. Tiểu mục catalog nhánh đã đóng trên hàng gốc ⇒ bị bỏ + báo, lưu không 422 — test ở Task 3.
3. Lưu bản sao không đổi tên ⇒ 422 trùng tên (không phải 500, không tạo bản ghi) — test ở Task 4.
4. Gửi `copy_from_id` vào đường hàng tạm (`TempProductRequest`) ⇒ bị bỏ qua, không ghi chú — test ở Task 4.
5. Bản sao không mang `id` con nào (ĐVT, tài liệu, tệp, video) ⇒ lưu không cướp dòng của hàng gốc (bug video ERP) — test ở Task 4.

---

### Task 0: Nhánh + môi trường (chờ user cho phép rõ — CLAUDE.md)

- [x] Hỏi: tạo nhánh trong checkout chính (đổi nhánh ảnh hưởng session khác đang dùng `gop_db`) hay worktree
  `websites/wt-sao-chep-hang-hoa/{hrm-api,hrm-client}` (copy thật `vendor`/`node_modules`, kiểm autoload theo
  memory worktree-vendor-symlink-autoload-bug, cổng Nuxt/API riêng). Hỏi DB chạy PHPUnit.
- [x] `git fetch origin gop_db && git switch -c feat/sao-chep-hang-hoa origin/gop_db` ở 2 repo. Kiểm `git status` sạch.

### Task 1: `CmcS3Helper::copyToTemporary`

**Files:** Modify `hrm-api/app/Helper/CmcS3Helper.php` (cạnh `promoteTemporary` :207) · Test: `hrm-api/Modules/MasterData/Tests/Unit/CmcS3HelperCopyToTemporaryTest.php` (tạo)

**Interfaces — Produces:** `copyToTemporary(string $url): string|false` — chép object (cùng bucket) sang
`TEMPORARY_FOLDER/<uniqid>_<basename>`, ACL `public-read`, trả URL mới (đi qua được `isTemporaryUrl`); `false` khi
`keyFromUrl` null hoặc S3 404.

- [x] Test (S3Client Mockery gán vào thuộc tính client qua reflection): `chep_sang_tmp_ten_moi` (assert `copyObject` nhận
  `Key` bắt đầu `tanphat_hrm/tmp/`, khác key nguồn; kết quả `isTemporaryUrl` = true) · `url_ngoai_bucket_tra_false` ·
  `nguon_404_tra_false`. Chạy ⇒ FAIL.
- [x] Viết hàm. Chạy ⇒ PASS.

### Task 2: Tách luật chặn hàng kèm/máy dùng chung

**Files:** Create `Modules/MasterData/Services/Product/KitStatusGuard.php` · Modify `Http/Requests/Product/ProductRequest.php` `checkKitStatus` (:374-) · Test `Tests/Feature/ProductWriteHardeningTest.php` (giữ xanh) + `Tests/Feature/KitStatusGuardTest.php` (tạo)

**Interfaces — Produces:** `KitStatusGuard::reasons(array $productIds, int $companyId): array` — `[productId => thông báo]`
cho hàng bị chặn (đã xoá · hàng tạm · khoá tại công ty), CÙNG 3 câu thông báo hiện tại; id hợp lệ/không tồn tại không có
trong kết quả.

- [x] Test `KitStatusGuardTest`: 3 ca bị chặn ra đúng câu · hàng Đang KD không có trong kết quả. FAIL.
- [x] Viết `reasons()` bằng đúng query đang ở `checkKitStatus`; `checkKitStatus` gọi lại nó (giữ luật "dòng đã gắn trước giữ").
- [x] Chạy `KitStatusGuardTest` + `ProductWriteHardeningTest` + `ProductWriteApiTest` ⇒ PASS.

### Task 3: `GET products/{id}/copy-data`

**Files:** Create `Services/Product/ProductCopyService.php` · Modify `Http/Controllers/V1/Product/ProductWriteController.php` (thêm `copyData` cạnh `edit` :36) · `Routes/api.php` (cạnh `/{product}/edit` :549, middleware `checkPermission:` . `$build`) · Test `Tests/Feature/ProductCopyApiTest.php` (tạo; khuôn setUp/payload/`ActsAsProductUser` như `ProductWriteApiTest`)

**Interfaces:**
- Consumes: `KitStatusGuard::reasons`, `CmcS3Helper::copyToTemporary`, `ProductOptionService::formOptions` (cờ `is_locked`),
  `CatalogBranchGuard::closedErrors`, `ProductFormResource`, `Product::editableAt`.
- Produces: JSON = khuôn `ProductFormResource` (scope full) **không** có `id`, `code`, `company_status`, `pricing_lock_message`,
  `edit_scope`, `owner_company_id`, `owner_company_name`, `has_vehicle_data`, không `id` trong `units/tech_attachments(.files)/
  galleries/videos/attributes/recipes/accessories/install_accessories/repair_accessories`; giữ `option_ids`; thêm
  `copy_source: {id, code, name}` và `dropped: {kits: [{group, code, name, reason}], locked: [{field, name}], files: [{name}],
  galleries: int, videos: [string]}`. FE hiển thị nguyên các mảng này.

- [x] Test (FAIL trước):
  - `co_quyen_tra_form_khong_id_kem_copy_source` — tạo hàng qua `POST` như `ProductWriteApiTest`, gọi copy-data: không key
    `id`/`code`, mọi dòng con không `id`, `copy_source.code` = mã gốc, `admin.supplier_ids/job_cluster_ids` bằng gốc.
  - `khong_quyen_1652_bi_403` · `hang_cong_ty_khac_chua_lay_ve_403` · `ngung_kd_403` · `hang_tam_403` · `hang_da_xoa_403`
    — đều câu `Không nhân bản được hàng hoá này.`
  - `hang_lay_ve_sao_chep_duoc` (công ty mình chỉ lấy về, không phải chủ) ⇒ 200.
  - `loai_hang_kem_va_may_bi_chan` — gắn thẳng DB 1 phụ kiện rồi khoá (pcc 4) + 1 máy đã xoá ⇒ không còn trong form, có trong `dropped.kits`.
  - `bo_danh_muc_khoa` — đặt `brands.status` khác 1 cho thương hiệu của gốc ⇒ `brand_id` null, `dropped.locked` có tên;
    tiểu mục catalog nhánh đóng ⇒ bỏ khỏi `admin.job_cluster_ids`.
  - `avatar_vao_galleries` (galleries rỗng, avatar `https://…`) · `avatar_noimage_bo_qua` (`/images/noimage.png` ⇒ galleries rỗng)
    · `qua_10_anh_cat_10` (`dropped.galleries` = số bị cắt) · `video_hong_bo` .
  - `tai_lieu_chep_sang_tmp` — mock `copyToTemporary` trả URL `/tmp/`; tệp nguồn trả `false` ⇒ vào `dropped.files`.
  - `copy_data_khong_ghi_db` — đếm `products`, `catalog_histories` trước/sau bằng nhau.
- [x] `ProductCopyService::prefill(Product $product, int $companyId): array` + `copyData($product)` ở controller:
  `assertCanWrite()`; `editableAt(companyId, pcc.status)` sai hoặc hàng tạm ⇒ `abort(403, …)`; load quan hệ như `edit()`
  (dùng chung danh sách — tách hằng/hàm, không chép); dựng `ProductFormResource` với scope `full`; làm sạch theo design §3.1.
  Ô đơn khoá ⇒ null; ô nhiều ⇒ bỏ phần tử; ĐVT khoá ⇒ `unit_id` null giữ dòng; thuộc tính có `unittech_id` khoá ⇒ null.
- [x] Chạy `ProductCopyApiTest` ⇒ PASS.

### Task 4: `POST products` nhận `copy_from_id` ⇒ ghi lịch sử

**Files:** Modify `Http/Requests/Product/ProductRequest.php` `rules()` (:58 — NGOÀI `commonRules`), `Services/Product/ProductWriteService.php` `store`/`storeWithRetry` (:94-128), `ProductWriteController::store` (:29) · Test `Tests/Feature/ProductCopyApiTest.php`

**Interfaces — Produces:** `ProductWriteService::store(array $data, int $companyStatus = STATUS_ENTERING_INFO, ?int $copyFromId = null): Product`.
Controller lấy `copy_from_id` từ `validated()`, bỏ khỏi `$data` trước khi gọi.

- [x] Test (FAIL trước): `luu_ban_sao_ghi_lich_su_sao_chep_tu` (đổi tên, gửi payload copy-data + `copy_from_id` ⇒ 200, mã mới
  ≠ gốc, `catalog_histories` action `create` note `Nhân bản từ <mã gốc>`, pcc 1 + `info_entered_at` not null, mọi giá 0) ·
  `ban_sao_khong_doi_ten_422` (không tạo dòng) · `ban_sao_khong_cuop_dong_con_cua_goc` (số dòng ĐVT/tài liệu/tệp/video/ảnh của
  gốc không đổi sau khi lưu bản sao) · `copy_from_id_khong_ton_tai_422` · `hang_tam_bo_qua_copy_from_id` (gửi vào
  đường tạo hàng tạm ⇒ note null).
- [x] Sửa rule + chữ ký + truyền tới `logCreate((int) $product->id, $copyFromId ? 'Sao chép từ ' . $code : null)`.
- [x] Chạy `ProductCopyApiTest`, `ProductWriteApiTest`, `TempProductApiTest`, `PriceAskingTempProductTest`, `ProductHistoryApiTest` ⇒ PASS.

### Task 5: Cờ `can_copy`

**Files:** Modify `Transformers/Product/ProductListResource.php` (:75), `ProductDetailResource.php` (:46) · Test `ProductCopyApiTest`

- [x] Test: `can_copy_theo_quyen_va_trang_thai` — danh sách + chi tiết: có quyền & Đang KD ⇒ true; không quyền ⇒ false;
  Ngừng KD ⇒ false. FAIL.
- [x] `'can_copy' => $canBuild && $this->resource->editableAt($companyId, $status)` ở cả 2. PASS.
- [x] Chạy cả thư mục `Modules/MasterData/Tests` một lượt, đối chiếu số đỏ sẵn (STATUS ghi "2 đỏ sẵn") — không thêm đỏ mới.

### Task 6: FE form sao chép

**Files:** Modify `hrm-client/pages/master-data/products/create.vue`, `components/product/form/ProductForm.vue` (`init` :278, `save` :503), `components/product/form/productFormModel.js` (`toPayload`)

**Interfaces:** Consumes `GET products/{id}/copy-data` (Task 3). `ProductForm` prop mới `copyFromId: Number|null`.
`toPayload(form, { copyFromId })` thêm `copy_from_id` khi có.

- [x] `create.vue`: `copyFromId` = số từ `$route.query.copy_from`; `pageTitle` = `Sao chép hàng hoá` khi có; truyền prop.
- [x] `ProductForm.init()`: nhánh `mode === 'create' && copyFromId` ⇒ gọi copy-data, tách `option_ids`, `copy_source`,
  `dropped` ra khỏi dữ liệu form (không lọt payload), đổ form như nhánh edit (attributes `checked: true`), `loadOptions(optionIds)`.
  Lỗi ⇒ toast message BE + `$router.replace(backUrl)`.
- [x] Khối cảnh báo đầu form (tra khối thông báo đang có trong `ProductForm`/các form V2 trước, dùng lại khuôn đó):
  dòng 1 `Đang sao chép từ <mã> — <tên>. Đổi Tên / Model / Thương hiệu / Hãng sản xuất để không trùng hàng gốc. Giá không được sao chép.`;
  các dòng sau liệt kê `dropped.*` (chỉ hiện nhóm có phần tử).
- [x] `unsaved-changes`: ~~form điền sẵn coi là pristine~~ — đổi 25/10 (user chốt minor #5): form nhân bản đã nạp xong luôn tính là chưa lưu ⇒ thoát hiện popup chung "Thông tin chưa lưu" (override `isFormDirty` ở `ProductForm.vue`, không sửa mixin).

### Task 7: FE nút Sao chép

**Files:** Modify `hrm-client/components/product/ProductListPage.vue` (`rowActionsOf` nhánh mặc định :1118, `onRowAction` :1143), `pages/master-data/products/_id/index.vue` (V2Footer `#custom-actions` :56-80)

- [x] Menu dòng: `{ key: 'copy', title: 'Sao chép', icon: 'ri-file-copy-line', visible: can && !!item.can_copy }` ngay sau
  `edit`; nhánh mặc định chỉ phục vụ entering/trading/company (kiểm lại `product-list-screens.js`, màn khác không lộ nút).
  `onRowAction('copy')` ⇒ `/master-data/products/create?copy_from=${item.id}&from=${encodeURIComponent(this.screen.path)}`.
- [x] Footer chi tiết: nút `Sao chép` theo `button-convention` (màu/thứ tự), hiện khi `product.can_copy && hasAPermission('Xây dựng thông tin hàng hoá')`,
  `from` giữ query `from` hiện có của trang chi tiết.

### Task 8: Kiểm bằng Playwright MCP + cập nhật e2e

- [x] Dựng môi trường theo memory chay-moi-truong-dev-hrm (cổng riêng nếu worktree). Tài khoản: có quyền + không quyền
  (memory kiem-playwright-khi-khong-co-tai-khoan-e2e / local-dev-duoc-cap-quyen-de-test — gỡ role tạm + xoá cache sau).
- [x] Đo DOM: số mục "Sao chép" trong menu ⋮ ở 3 màn (có quyền > 0, không quyền = 0, dòng Ngừng KD = 0, màn Hàng tạm/
  Kho dữ liệu/Đang khoá = 0); footer chi tiết có nút; bấm ⇒ URL đúng, tiêu đề `Sao chép hàng hoá`, đếm ô có giá trị
  (Tên, Model, Loại SP, ĐVT, NCC…) khớp hàng gốc, khối cảnh báo hiện; Lưu không đổi tên ⇒ ô Tên báo lỗi; đổi tên Lưu ⇒
  sang chi tiết mã mới, lịch sử có `Sao chép từ`. Ca có `dropped` giả lập bằng `page.route` trả `copy-data`.
- [x] Thêm ca vào spec e2e hàng hoá (HRM/e2e — kiểm bản mới nhất theo memory e2e-hrm-lech-ban-worktree): có quyền +
  không quyền. KHÔNG tự chạy cả bộ trừ khi user yêu cầu.

### Task 9: Đóng việc

- [x] Review code (skill code-reviewer / superpowers:requesting-code-review) trên diff 2 repo.
- [x] Cập nhật `design.md` nếu lệch khi làm; `.plans/gop-db/STATUS.md` + bảng trạng thái `quan-ly-hang-hoa/design.md`;
  đánh dấu G8/T9 (`2c-ghi`) và task C4.3 (`man-danh-muc-hang-hoa/plan.md:577`) là thay bằng hồ sơ này.
- [x] Báo user: 2 nhánh, các file đổi, kết quả PHPUnit + Playwright (số đo). Không commit.

## Checkpoint

- 24/10/2026: khảo sát + design (S1–S9) + plan xong. Chờ user duyệt plan + cho phép code (Task 0).

### Checkpoint — 24/10/2026 (code xong, CHƯA commit)
Vừa hoàn thành: Task 0–9 trên worktree `websites/wt-sao-chep-hang-hoa/{hrm-api,hrm-client}` nhánh `feat/sao-chep-hang-hoa`
(từ origin/gop_db api 2169b460e · client 0113bddb6). Sổ chi tiết + phán quyết: [progress.md](progress.md).
PHPUnit trên DB `hrm_erp_test_saochep` (bản dump `hrm_erp_21_10_prod`): ProductCopyApiTest 23 · KitStatusGuard 2 · CmcS3Helper 4 + bộ
ghi hàng hoá cũ xanh; cả MasterData 734 ca chỉ 3 đỏ SẴN trên gop_db. Playwright MCP đo đủ (progress.md). Review opus: 2 Important + 1
nâng cấp đã sửa RED→GREEN; 6 Minor để sau.
Đang làm dở: —
Bước tiếp theo: user xem diff ⇒ commit/push (user tự báo); chạy e2e `products-copy-ui` + 3 spec đã sửa khi user yêu cầu;
dọn sau: DROP DB `hrm_erp_test_saochep`, gỡ worktree, dừng server :8011/:3011.
Blocked: —
