# Kế thừa giá bán theo hãng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development hoặc superpowers:executing-plans. Bước dùng `- [ ]`.
> ✅ User cho "làm" 24/10/2026 (phạm vi dưới). Trước đó: ⛔ Chưa có "làm". Trước Task 1 phải hỏi user riêng, nêu phạm vi: 2 repo HRM · nhánh `gop_db` · 2 migration (tên ở Task 1) chạy
> vào DB local `hrm_erp_21_10_prod` bằng `--path` · 1 quyền mới chạy `permission:sync` vào DB local. **Không commit** (user tự báo).

**Goal:** Công ty chọn hãng kế thừa giá ⇒ hàng do công ty khác tạo thuộc hãng đó mang bộ giá (6 giá + ĐMGG + giá hiệu lực) của
công ty quản lý, tự đồng bộ, không sửa được; hỏi giá hàng kế thừa tách sang công ty quản lý.

**Architecture:** Một nguồn luật `PriceInheritance` (suy ra lúc đọc từ 2 bảng cài đặt) + một lớp chép `InheritedPriceSync` gọi ở
mọi đường giá công ty quản lý THẬT SỰ áp + chặn ghi ở công ty kế thừa. Màn cài đặt mới bám khuôn Chính sách giá bán nội bộ. YCHG tách
phiếu lúc Gửi trong `PriceAskingRequestWriter::save`.

**Tech Stack:** Laravel 8 / PHP 7.4 (Modules/MasterData), Nuxt 2 / Vue 2 (V2Base*), PHPUnit (DatabaseTransactions trên DB .env), Playwright.

**Spec:** `design.md` (§1–§8, T1–T7) · `ton.md` (Q1–Q13) · mockup đã duyệt 24/10 `mockup-ke-thua-gia.html` (U1–U11 đầu file).

## Global Constraints

- Hàng kế thừa ⇔ `p.company_id ≠ c` ∧ `p.manufacture_id IS NOT NULL` ∧ (mode(c)=1 ∧ hãng ∈ danh sách(c) ∨ mode(c)=2 ∧ hãng ∉ danh sách(c)); công ty chưa có dòng cài đặt = mode 1 + rỗng. Công ty nguồn = `p.company_id`.
- mode: `1` = "Chọn hãng kế thừa giá theo công ty quản lý" · `2` = "Chọn hãng tự xây dựng giá bán".
- Giá trị chép theo `product_unit_id`: `product_unit_prices` 6 loại (`price`, `coefficient`, `sale_max_percent`, `is_manual_*_online`, cột `*_wait_approve` = giá trị mới, cờ `flag_*` = 0) + `product_expected_prices` status 2 (thay toàn bộ). **Không** chép `product_company_units.cost_price` / `buy_price`.
- Đồng bộ CHỈ khi giá nguồn thật sự áp, cùng transaction; công ty kế thừa không duyệt lại; không thông báo.
- Câu chặn ghi (423): `Hàng kế thừa giá từ <mã công ty>, không sửa giá ở công ty này.`
- Ghi chú lịch sử giá: `Kế thừa từ <mã công ty>` (đổi cài đặt: `Kế thừa từ <mã công ty> (đổi cài đặt)`); lịch sử hàng hoá khi Chuyển KD: `Kế thừa giá từ <mã công ty>`.
- Quyền mới: `Cài đặt giá bán theo hãng` · group `Hàng hoá` · type `8` (khai `$this->perm([...])`, không `id`).
- Hằng mới: `PriceAskingRequest::STATUS_TRANSFERRED = 11` "Đã chuyển công ty quản lý" màu `#6B7280`; nhóm dùng cùng mã 11.
- Đổi cài đặt bị chặn khi hàng chuyển sang kế thừa đang `pcc.status` 2/5 tại công ty: 422 liệt kê số YCHG.
- FE: V2Base*, `$confirm`, nút cách 12px (`mr-2 mb-2`), số `en-US`, badge `V2BaseBadge` màu do BE trả.

## Review Focus

1. Công ty quản lý THÊM ĐVT mới cho hàng sau khi đã có công ty kế thừa ⇒ công ty kế thừa phải có đủ bộ giá ĐVT đó ở lần đồng bộ kế tiếp (Task 3 test `propagate_bu_dvt_moi`).
2. Hàng đổi hãng (sửa `manufacture_id`) sau khi đã kế thừa ⇒ trạng thái kế thừa đổi theo luật ngay lúc đọc, không còn chép nếu hãng mới không kế thừa (Task 2 test `doi_hang_doi_trang_thai`).
3. Cron giá hiệu lực chạy công ty kế thừa trước công ty nguồn ⇒ không áp dòng bản chép, không ghi log trùng (Task 4 test `cron_bo_qua_ban_chep`).
4. Hai công ty kế thừa cùng một hàng, một công ty đang khoá (pcc 4) ⇒ chỉ công ty đang KD được chép; khôi phục sau đó chép giá mới nhất (Task 3 + Task 6).
5. Gửi YCHG có hàng kế thừa từ 2 công ty nguồn, 1 nguồn chưa phân công XNK ⇒ không tạo phiếu nào, 422 nêu hãng + công ty (Task 7).

---

### Task 1: CSDL + quyền

**Files:**
- Create: `hrm-api/database/migrations/2026_10_24_000001_create_manufacture_price_modes_tables.php`
- Create: `hrm-api/database/migrations/2026_10_24_000002_add_split_columns_to_price_asking_tables.php`
- Create: `hrm-api/Modules/MasterData/Entities/ProductPrice/ManufacturePriceMode.php`, `.../ManufacturePriceModeItem.php` (extends `BaseModel`)
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (dòng sau `Duyệt giá bán hàng hoá` :1679)
- Modify: `hrm-api/Modules/MasterData/Entities/PriceCalculation/PriceAskingRequest.php`, `PriceAskingRequestGroup.php` (STATUS_TRANSFERRED + TEXT/COLOR)

**Interfaces — Produces:** bảng `manufacture_price_modes(id, company_id UNIQUE, mode tinyint, created_by, updated_by, timestamps)` ·
`manufacture_price_mode_items(id, company_id, manufacture_id, created_by, updated_by, timestamps, UNIQUE(company_id, manufacture_id))` ·
`price_asking_requests.origin_request_id` + `price_asking_request_groups.transferred_request_id` (unsigned bigint NULL, index) ·
`ManufacturePriceMode::MODE_INHERIT = 1`, `MODE_OWN = 2`.

- [x] Kiểm `migrate:status` + `migrate --pretend --path=<2 file>`; nêu cho user, chờ "làm".
- [x] Viết 2 migration + 2 entity + hằng trạng thái; khai quyền; `php artisan permission:sync --dry-run` chỉ báo thêm đúng 1 quyền.
- [x] Chạy đúng 2 migration bằng `--path` + `permission:sync` vào DB local (sau khi user cho phép). Xoá cache quyền.

### Task 2: Luật kế thừa — `PriceInheritance`

**Files:** Create `hrm-api/Modules/MasterData/Services/ProductPrice/PriceInheritance.php` · Test `Modules/MasterData/Tests/Feature/PriceInheritanceTest.php`

**Interfaces — Produces:**
- `mode(int $companyId): int`
- `sourcesFor(array $productIds, int $companyId): array` — `[product_id => source_company_id]` chỉ cho hàng kế thừa.
- `sourceOf(int $productId, int $companyId): ?int`
- `inheritorsOf(array $productIds, int $sourceCompanyId, array $statuses = [3]): array` — `[product_id => [company_id…]]`, chỉ hàng có `p.company_id = $sourceCompanyId`.
- `sql(string $productAlias, string $companyExpr): string` — biểu thức boolean (bind 0 tham số; `$companyExpr` là cột/biểu thức SQL) dùng cho lọc danh sách + cron.

- [x] Test: 2 chế độ × trong/ngoài danh sách · hàng công ty mình tạo = không · hàng không hãng = không (T1) · công ty chưa cài = mode 1 rỗng · `doi_hang_doi_trang_thai` (đổi `manufacture_id` ⇒ kết quả đổi) · `inheritorsOf` lọc đúng status + đúng nguồn · `sql()` cho cùng kết quả với `sourcesFor` trên cùng fixture.
- [x] Chạy ⇒ FAIL; implement; chạy ⇒ PASS.

### Task 3: Chép + đồng bộ — `InheritedPriceSync`

**Files:** Create `hrm-api/Modules/MasterData/Services/ProductPrice/InheritedPriceSync.php` · Test `Tests/Feature/InheritedPriceSyncTest.php`

**Interfaces:**
- Consumes: `PriceInheritance` (Task 2), `ProductPriceSetWriter::ensureUnitSet/ensureProductSet`, `ProductPriceHistoryService::snapshot/logAction`.
- Produces:
  - `copy(int $productId, int $targetCompanyId, int $by, string $note): void` — một hàng (mọi ĐVT), dùng cho Chuyển KD / khôi phục.
  - `copyMany(array $productIds, int $targetCompanyId, int $by, string $note): int` — SQL theo lô 500 mã (UPDATE…JOIN `upp`, xoá + INSERT…SELECT `pep`), lịch sử ghi gộp theo lô; trả số mã.
  - `propagate(array $productUnitIds, int $sourceCompanyId, int $by): int` — tìm công ty kế thừa đang KD (`inheritorsOf`) rồi `copyMany` theo từng công ty.

- [x] Test: chép đủ 6 dòng + ĐMGG + cờ sửa tay, giữ `cost_price`/`buy_price` công ty đích · giá hiệu lực status 2 thay toàn bộ, status 1/3 công ty đích giữ · lịch sử 1 dòng/ĐVT đúng ghi chú · `propagate` bỏ công ty pcc 4 · `propagate` từ công ty KHÔNG phải nguồn (vd công ty kế thừa) ⇒ 0 · `propagate_bu_dvt_moi` (nguồn có ĐVT mới ⇒ đích có đủ 6 dòng) · gọi 2 lần liên tiếp ⇒ kết quả như 1 lần.
- [x] Implement; PASS.
- [x] **Đo**: `copyMany` toàn bộ hàng lấy về đang KD của công ty 2 (30,272 mã · ~184k dòng giá) trong transaction rồi rollback (tinker). Ghi thời gian vào Checkpoint. **> 30 s ⇒ dừng, hỏi user** (chạy nền + màn báo "đang áp") trước khi làm Task 5.

### Task 4: Gắn đồng bộ vào đường ghi giá + chặn ghi ở công ty kế thừa

**Files (Modify):**
- `Services/ProductPrice/ProductPriceUpdateService.php` — `update()`: sau nhánh không duyệt (sau `logUpdate`) gọi `propagate([$productUnitId], $companyId, $by)`; đầu hàm `assertNotInherited`.
- `Services/ProductPrice/ProductPriceApprovalService.php` — `approve()`: sau mỗi yêu cầu được áp gọi `propagate`; `approve`/`reject` của công ty kế thừa không phát sinh (guard ở submit).
- `Services/ProductPrice/ProductPriceApprovalSubmitter.php` — `submit()`: 423 nếu hàng kế thừa tại công ty.
- `Services/ProductPrice/ProductPriceWriter.php` — `apply()` (PTG không duyệt) gọi `propagate`.
- `Services/PriceCalculation/PriceCalculateWriter.php` — `submit()`: 423 cho dòng hàng kế thừa tại công ty phiếu.
- `Services/ProductPrice/ExpectedPriceApplier.php` — `pending()`: loại dòng `upp` của công ty mà hàng là kế thừa (`PriceInheritance::sql('p', 'upp.company_id')` phủ định); `process()`: sau áp, `propagate` theo nhóm (ĐVT × công ty).
- `Services/Product/ProductLifecycleService.php` — `tradeWithoutPrice()` ở công ty nguồn: sau `ensureProductSet` gọi `propagate`; công ty kế thừa: mã kế thừa bị bỏ qua, lý do `Hàng kế thừa giá — dùng Chuyển kinh doanh (kế thừa giá).`
- Test: `Tests/Feature/InheritedPricePropagationTest.php`

**Interfaces — Produces:** `PriceInheritance::assertNotInherited(int $productId, int $companyId): void` (abort 423 với câu ở Global Constraints).

- [x] Test mỗi đường: G4 lưu thẳng ⇒ đích đổi · G4 gửi duyệt ⇒ đích chưa đổi, duyệt xong ⇒ đổi · PTG áp ⇒ đổi · cron ⇒ đổi + `cron_bo_qua_ban_chep` · sửa/xoá giá hiệu lực ở nguồn ⇒ đích theo · G4 / gửi duyệt / PTG tại công ty kế thừa ⇒ 423 · trade-without-price tại nguồn ⇒ đích về 0.
- [x] Implement; PASS; chạy lại `ProductPriceScreenApiTest`, `ProductPriceApprovalApiTest`, `ExpectedPriceApplyTest`, `PriceCalculateApiTest`, `OwnerPriceFloorApiTest`, `ProductTradeWithoutPriceApiTest`.

### Task 5: API màn cài đặt

**Files:** Create `Services/ProductPrice/ManufacturePriceModeService.php` · `Http/Controllers/V1/ProductPrice/ManufacturePriceModeController.php` · Modify `Routes/api.php` · Test `Tests/Feature/ManufacturePriceModeApiTest.php`

**Interfaces — Produces (prefix `master-data/manufacture-price-modes`, middleware `checkPermission:Cài đặt giá bán theo hãng`, công ty = công ty đang làm):**
- `GET /` ⇒ `{mode, items: [{manufacture_id, code, name, trading_count, sources: [{company_code, count}], updated_by_name, updated_at}]}`
- `GET /manufacturers?search=` ⇒ như `internal-price-policies/manufacturers` nhưng cột số = hàng công ty khác tạo đang KD tại công ty, cờ `in_list`.
- `POST /preview` body `{mode, manufacture_ids[]}` ⇒ `{to_inherit: [{manufacture_id, name, count}], to_own: [...], total_inherit, total_own, blocked: [{code, id}]}`
- `PUT /` cùng body ⇒ kiểm lại; `blocked` ≠ rỗng ⇒ 422 `Không lưu được: hàng chuyển sang kế thừa đang trong yêu cầu hỏi giá đã gửi — <số phiếu, …>.`; ngược lại 1 transaction: lưu mode + đồng bộ danh sách + `copyMany` hàng chuyển sang kế thừa (ghi chú "(đổi cài đặt)") + huỷ yêu cầu Duyệt giá đang mở của các dòng đó (T3) + `catalog_histories` (table `manufacture_price_modes`, action create/update, diff mode + hãng thêm/bỏ, note số mã đổi giá).
- `GET /histories` ⇒ khuôn entity-history (`SystemInfoSection`).

- [x] Test: GET mặc định công ty chưa cài (mode 1, rỗng) · preview đếm đúng 2 chiều + blocked · PUT ghi + chép giá + huỷ duyệt chờ + lịch sử · PUT blocked ⇒ 422, không ghi gì · không quyền ⇒ 403 · công ty khác không đổi · validate `mode ∈ {1,2}`, `manufacture_ids` tồn tại.
- [x] Implement; PASS.

### Task 6: Chuyển kinh doanh (kế thừa giá) + khôi phục

**Files (Modify):** `Services/Product/ProductLifecycleService.php` (+ `tradeInherited(array $ids)`, `restore()` T4) · `Http/Controllers/V1/Product/ProductLifecycleController.php` · `Routes/api.php` (`POST products/trade-inherited`, middleware như `trade-without-price`) · `Entities/Product/Product.php` · `Transformers/Product/ProductListResource.php`, `ProductDetailResource.php` (+ `can_trade_inherited`, `price_source: {company_id, company_code}|null`; `can_trade_without_price` = false cho hàng kế thừa) · `Services/PriceCalculation/PriceAskingProductReader.php` (`blockReason`: hàng kế thừa status 1 ⇒ `Hàng kế thừa giá — dùng Chuyển kinh doanh (kế thừa giá).`) · Test `Tests/Feature/ProductTradeInheritedApiTest.php`

**Interfaces — Produces:** `tradeInherited(array $ids): array{trading: [{id, code}], skipped: [{id, code, message}]}` — khuôn `tradeWithoutPrice` (≤ 100, lockForUpdate, cùng các lý do bỏ qua) + lý do riêng: không phải hàng kế thừa `Hàng không thuộc hãng kế thừa giá.` · nguồn pcc 4 `Công ty quản lý đã ngừng kinh doanh hàng này.` (T2). Đạt ⇒ `InheritedPriceSync::copy` ⇒ pcc 3 ⇒ `logStatus(..., 'Kế thừa giá từ <mã>')`.

- [x] Test: đạt (giá = nguồn, giá vốn giữ, lịch sử) · nguồn giá 0 vẫn đạt (Q5) · các lý do bỏ qua · cờ list/detail đúng + không quyền ⇒ false · YCHG chọn hàng kế thừa status 1 ⇒ block · khôi phục hàng kế thừa đang khoá ⇒ chép giá nguồn mới nhất rồi về 3 (T4).
- [x] Implement; PASS; chạy lại `ProductLifecycleApiTest`, `ProductRestoreApiTest`, `ProductLockedScreenTest`.

### Task 7: Tách YCHG khi Gửi

**Files (Modify):** `Services/PriceCalculation/PriceAskingRequestWriter.php` (`save` / `validateInput` / `rebuildLines` + `splitInherited`) · `PriceAskingAccess.php` (`scopeVisible`, `isVisible`) · `PriceAskingRequestService.php` + Resource chi tiết (trả `origin_request: {id, code, company_name}`, nhóm `transferred_request: {id, code}`, `is_readonly_for_me`) · Test `Tests/Feature/PriceAskingSplitApiTest.php`

**Interfaces — Produces:** khi `$send`: tách dòng hàng kế thừa theo công ty nguồn ⇒ mỗi nguồn 1 `PriceAskingRequest` (`company_id` = nguồn, `created_by` = người gửi, `origin_request_id`, status 2, nhóm + XNK tra theo công ty nguồn qua `PriceAskingProductReader::rows($ids, $sourceCompanyId)`); nhóm ở phiếu gốc giữ lại với status 11 + `transferred_request_id`; phiếu gốc toàn kế thừa ⇒ status 11 (T6). Mọi kiểm (block, XNK) của mọi phiếu tách gộp vào 1 lần `ValidationException` trước khi ghi. Thông báo `submitted` cho từng phiếu tách theo công ty nguồn.

- [x] Test: phiếu lẫn hàng ⇒ gốc giữ hàng tự tính + nhóm 11 có link · 2 nguồn ⇒ 2 phiếu tách · toàn kế thừa ⇒ gốc 11 · nguồn chưa phân công XNK ⇒ 422, 0 phiếu mới · nguồn pcc 4 ⇒ 422 · người lập xem được phiếu tách (công ty khác), không thao tác được (403 ở PTKD/XNK) · người khác cùng công ty gốc không thấy phiếu tách · lưu nháp không tách.
- [x] Implement; PASS; chạy lại bộ test YCHG/YCTG/PTG hiện có.

### Task 8: FE màn Giá bán theo hãng sx

**Files:** Create `hrm-client/pages/finance/manufacture-price-modes/index.vue` (`layout: 'default-sidebar'`) + `components/finance/manufacture-price-mode/ModeHistoryModal.vue` (khuôn `PolicyHistoryModal`) · Modify `components/sale/settings/ManufacturerPickerModal.vue` (prop mới `endpoint` mặc định `internal-price-policies/manufacturers`, `countLabel`, `statusLabel` — mặc định giữ hành vi cũ) · `components/subsystem-menu/finance.js` (mục "Giá bán theo hãng sx" sau "Cập nhật giá bán", `isShow: ['Cài đặt giá bán theo hãng']`)

- [x] Dựng theo mockup U1–U7 (bám markup/class `.ipp-*` của `InternalPricePolicyPanel.vue`): radio chế độ, lưới, Chọn hãng, Bỏ khỏi danh sách/lưới, Huỷ thay đổi, Lưu cài đặt ⇒ `POST preview` ⇒ `$confirm` liệt kê thay đổi ⇒ `PUT`; 422 ⇒ toast; unsavedChangesMixin; Lịch sử.
- [x] Playwright MCP đo DOM (1440 + 1280): nút 32px cách 12px, chế độ đổi nhãn cột + dòng mô tả, popup xác nhận đúng số từ BE, không quyền ⇒ menu ẩn + vào URL bị 403.

### Task 9: FE màn hiện có

**Files (Modify):** `pages/finance/product-prices/index.vue` (+ component dòng) — dòng `price_source` ≠ null: badge `Kế thừa · <mã>` `#0EA5E9`, khoá mọi ô, ẩn Lưu / "+ Hiệu lực" / "Thêm lý do sửa giá", chữ xám dưới ĐVT (U8); ô lọc "Nguồn giá" trong Tìm kiếm nâng cao (BE `ProductPriceListService` nhận `price_source=own|inherited` dùng `PriceInheritance::sql`) · `utils/productLifecycle.js` + `components/product/ProductListPage.vue` + `pages/master-data/products/_id/index.vue` — action `trade_inherited` (icon `ri-links-line`, tiêu đề "Chuyển kinh doanh (kế thừa giá)", xác nhận + toast như mockup) ở dòng, thanh hàng loạt, footer chi tiết; `utils/product-list-screens.js` (`tradeInherited: true` cho `entering`, `company`) · `pages/sale/price-asking-requests/_id/*` — nhóm status 11: chip công ty quản lý + badge + link phiếu tách; phiếu tách: dải "Tách từ …", ẩn mọi nút thao tác với người lập (U10).

- [x] Implement; Playwright MCP đo DOM từng màn (cột khoá, icon, popup, link 2 chiều); console 0 lỗi.

### Task 10: Nghiệm thu

- [x] PHPUnit MasterData toàn bộ — đối chiếu 3 ca đỏ sẵn (`ExpectedPriceApplyTest::chot_chan…`, `TempProductVisibilityTest::catalog_tab…`, `PriceReaderWhitelistTest`); khai file đọc giá mới vào `tests/fixtures/price-readers.txt` nếu test whitelist đòi.
- [x] Viết e2e `HRM/e2e/tests/finance/manufacture-price-modes-ui.spec.ts` (có / không quyền) + `HRM/e2e/tests/master-data/products-trade-inherited-ui.spec.ts`; sửa spec cũ bị đổi giả định (`products-lifecycle-ui`, `product-prices-ui`). **Không chạy** tới khi user yêu cầu.
- [x] Dọn dữ liệu thử trên DB local (cài đặt công ty, giá đã chép, lịch sử) — đối chiếu mốc trước/sau.
- [x] Cập nhật `SO-CHOT-VA-TON.md`, `viec-con-lai.md`, Checkpoint.

## Sổ thực thi (ledger)
- Ruling: không commit, làm thẳng checkout chính `gop_db` (memory chuyen-doi-hang-hoa-nhanh-chung + user tự báo commit) — sai thì: user commit tay.
- Task 1: Ruling: migration đặt ở `Modules/MasterData/Database/Migrations/` (khuôn T1 Chính sách), không `database/migrations` như plan — chỉ là vị trí.
- Task 1: Ruling: entity `extends Model` (khuôn InternalPricePolicy — gán company/audit tay), có ghi lý do trên class — sai thì: đổi sang BaseModel.
- Task 1: Ruling: `permission:sync` thật sẽ thêm 13 quyền của người khác + sửa 715 dòng trên DB local ⇒ CHỈ chèn 1 dòng quyền "Cài đặt giá bán theo hãng" (id 101176, type 8, seed_order 853) + xoá cache; seeder đã khai, sync lần sau tự khớp — sai thì: chạy sync đầy đủ khi đồng đội đồng ý.
- Task 1: Ruling: `CLOSED_STATUSES` của nhóm gồm cả 11 — nhóm đã chuyển coi như đóng ở phiếu gốc (hàng không còn "đang trong YCHG" tại công ty gốc).
- Task 2: Ruling: `products.manufacture_id` NOT NULL, 0 hàng thiếu hãng ⇒ T1 không xảy ra; bỏ ca test "không hãng", giữ `is not null` trong SQL.
- Task 2: complete (PriceInheritanceTest 7/7).
- Task 3: Ruling: thêm nhãn `inherited` ⇒ "Kế thừa giá" vào `CatalogHistoryService::GATED_TABLES.product_prices.action_labels` (thuần thêm).
- Task 3: Ruling: `CatalogHistoryService::log` chỉ bỏ log rỗng với action `update` ⇒ InheritedPriceSync tự so ảnh chụp trước/sau.
- Task 3: Đo bản đầu (chép từng mã): 1.000 mã 6,7 s ⇒ ~200 s cho 30.272 mã ⇒ hỏi user ⇒ user chọn "Tối ưu SQL theo lô".
- Task 3: Ruling: refactor `ProductPriceHistoryService::snapshot()` thành `buildSnapshot()` dùng chung + thêm `snapshotMany()` (đầu ra giống hệt — test `snapshot_many_khop_snapshot_tung_dvt`).
- Task 3: Đo bản lô: 30.272 mã 17 s (giá phần lớn đã trùng) · ca xấu nhất (mọi giá lệch, 30.724 dòng lịch sử) 25 s — đạt < 30 s.
- Task 3: complete (InheritedPriceSyncTest 8/8).
- Task 4: Ruling: `InheritedPriceSync` nhận `?int $by` (cron chạy không người — `created_by` NULL, tránh FK employees).
- Task 4: Ruling: không viết ca riêng cho chặn PTG tại công ty kế thừa (phòng vệ — kịch bản bị chặn từ trước ở đổi cài đặt + tách YCHG); chặn PTG báo lỗi dòng `rows.i.product`.
- Task 4: complete (InheritedPricePropagationTest 7/7; bộ giá liên quan 120 ca: 1 đỏ sẵn `ExpectedPriceApplyTest::chot_chan…`).
- Task 5: Ruling: chặn đổi cài đặt khi hàng chuyển sang kế thừa nằm trong YCHG ĐÃ GỬI còn mở ở công ty — MỌI trạng thái hàng (không chỉ 2/5 như Q10): hàng Đang KD trong YCHG đang chạy cũng kẹt ở PTG (chặn 423) nếu cho đổi. Thêm `PriceAskingProductReader::openSentRequests()` (dùng lại `openRequestLines`, không tính Nháp) — sai thì: user thấy bị chặn rộng hơn câu chữ Q10.
- Task 5: Ruling: PUT không gắn `dueConfig` (như route Cập nhật giá); thêm bảng `manufacture_price_modes` vào `CatalogHistoryService::GATED_TABLES` (thuần thêm).
- Task 5: Ruling: fixture test tạo 2 hãng mới trong transaction (hãng có thật đã có hàng ở công ty 4 làm lệch số đếm).
- Task 5: complete (ManufacturePriceModeApiTest 6/6; cùng nhóm 28/28).
- Task 6: Ruling: cờ `price_source_id` tính bằng `PriceInheritance::sql` ngay trong query danh sách/chi tiết (`ProductService`) — không N+1; `tradableWithoutPriceAt` thêm điều kiện không kế thừa.
- Task 6: complete (ProductTradeInheritedApiTest 7/7; hồi quy hàng hoá + YCHG 168 ca: 1 đỏ sẵn `TempProductVisibilityTest::catalog_tab…`).
- Task 7: Ruling: nhóm YCHG có UNIQUE (phiếu × thương hiệu × hãng) ⇒ KHÔNG tách nhóm theo nguồn (tránh migration mới). Gửi: nhóm ở phiếu gốc toàn hàng kế thừa của 1 nguồn ⇒ 11 + `transferred_request_id` (giữ dòng để xem); nhóm lẫn (tự tính / nguồn khác) ⇒ rút dòng kế thừa khỏi phiếu gốc + lịch sử phiếu gốc "Chuyển <mã> sang <phiếu tách>" — sai thì: phiếu gốc không hiện dòng hàng đã chuyển của nhóm lẫn (vẫn có ở phiếu tách + lịch sử).
- Task 7: Ruling: quyền xem không cần sửa — `scopeVisible`/`isVisible` đã cho người lập (`created_by`) thấy phiếu mọi công ty; ghi vẫn chặn theo công ty phiếu.
- Task 7: complete (PriceAskingSplitApiTest 6/6; hồi quy YCHG/YCTG/PTG + nhóm mới 106/106).
- Task 8: Ruling: lịch sử dùng `SettingHistoryModal` + adapter `ManufacturePriceModeAdapter` (`setting-histories/manufacture_price_mode/{company}`) — đúng khuôn màn Chính sách giá nội bộ, bỏ endpoint `/histories` riêng của plan.
- Task 8: Ruling: `ManufacturerPickerModal` thêm prop `endpoint` / `countLabel` / `statusLabel` / `onGridText` (mặc định giữ hành vi cũ) + giữ `product_count` khi tick (lỗi dòng mới chọn hiện 0 mã — bắt được lúc kiểm Playwright).
- Task 8: Playwright MCP (NV 13, role tạm 104722 đã gỡ): 1440/1280 không cuộn ngang, nút 32px cách 12px (thanh công cụ + chân); Chọn hãng 3M ⇒ xác nhận ⇒ PUT 200 ⇒ lịch sử "Tạo mới"; đổi chế độ ở công ty 1 ⇒ toast chặn đúng 4 YCHG đang chạy; không quyền ⇒ menu ẩn, URL 404, API 403. Dữ liệu thử đã trả (giá mã 43217 khớp bản sao lưu, xoá cài đặt + lịch sử thử).
- Task 9: Ruling: khoá dòng hàng kế thừa ở Cập nhật giá dùng cơ chế `locked[p.id]` có sẵn của `ProductPriceTable` (khoá mọi ô, ẩn Lưu / Hiệu lực / lý do) + badge; ô lọc "Nguồn giá" ở Tìm kiếm nâng cao.
- Task 9: Ruling: nhóm YCHG ở form Thêm/Sửa toàn hàng kế thừa ⇒ "Gửi công ty quản lý: <mã>" và KHÔNG báo thiếu XNK (XNK xét ở công ty nguồn); danh sách YCHG thêm trạng thái lọc 11.
- Task 9: Playwright MCP: Cập nhật giá mã 43217 (kế thừa TPSG) 22/22 ô khoá, badge #0EA5E9; Nhập thông tin (route giả cờ) icon ri-links-line, xác nhận, POST đúng payload, toast, nút hàng loạt cách 12px; footer chi tiết khớp menu dòng; YCHG (route giả) nhóm đã chuyển + link phiếu tách, dải "Tách từ…" đúng màu.
- Task 10: PHPUnit MasterData 701 ca: 3 đỏ đều đã đỏ từ trước (`ExpectedPriceApplyTest::chot_chan…`, `TempProductVisibilityTest::catalog_tab…`, `PriceReaderWhitelistTest` chỉ còn file đồng đội `InventoryAuditReportService.php`); khai 2 file mới vào `price-readers.txt`. E2E 2 spec mới (`finance/manufacture-price-modes-ui`, `master-data/products-trade-inherited-ui`) biên dịch được (`--list` 6 ca) — CHƯA chạy.
- Final: reviewer độc lập (opus) — 1 Critical, 4 Important, 3 Minor. Sửa 1 lượt, mỗi lỗi test đỏ → xanh:
  - fixed PTKD duyệt phiếu gốc mở lại nhóm đã chuyển (bỏ nhóm CLOSED_STATUSES khỏi `ptkdApprove`) — `ptkd_duyet_phieu_goc_khong_mo_lai_nhom_da_chuyen`
  - fixed đóng giá hiệu lực ở nguồn không lan (propagate cả ACTION_CLOSE) — `dong_gia_hieu_luc_o_nguon_don_ban_chep_o_cong_ty_ke_thua`
  - fixed chép cả giá hiệu lực đang chờ duyệt flag 1 (lọc nguồn) — `gia_hieu_luc_dang_cho_duyet_o_nguon_khong_chep`
  - fixed đổi hãng ở công ty tạo mã làm công ty khác thành kế thừa: `InheritedPriceSync::afterSourceChange` (gọi trong `ProductWriteService`) huỷ duyệt chờ + chép giá; `approve()` chặn 423 hàng kế thừa — `doi_hang_lam_hang_thanh_ke_thua…`, `duyet_gia_cho_vao_hang_ke_thua_bi_chan_423`
  - fixed phiếu tách không đưa hàng ở nguồn 1 → 2 (`moveProducts` trong `splitInherited`) — `phieu_tach_dua_hang_nguon_dang_nhap_thong_tin_sang_cho_tinh_gia`
  - suite MasterData 707 ca: 3 đỏ sẵn (như trước).
- ~~Final: minor (deferred): `updatePrices` INNER JOIN — nguồn chưa có dòng giá thì đích giữ giá cũ thay vì 0~~ — **ĐÓNG 24/10 (user)**: không xảy ra được — Lấy về chặn khi công ty tạo chưa Đang KD (`ProductWriteService::takeSkipReason` L3), Đang KD luôn có dòng giá (không tính giá = dòng giá 0), khoá không xoá giá; DB local 0 mã. Không sửa.
- ~~Final: minor (deferred): `PriceInheritance::sql` với `products.company_id` NULL (1 hàng local) ra NULL ⇒ bị loại khỏi cron/lọc "Tự xây dựng"~~ — **ĐÓNG 24/10 (user)**: bỏ qua, user tự nhập `company_id` cho mã đó. Không sửa code.
- ~~Final: minor (deferred): nhóm phiếu gốc toàn kế thừa nhưng từ 2 nguồn chỉ link phiếu tách cuối~~ — **SỬA 24/10 (user: "sửa theo đề xuất, phải hiện đủ các phiếu con đã tách")**. Soi code thấy nặng hơn: lượt nguồn đầu coi nhóm là "lẫn" ⇒ XOÁ dòng hàng nguồn đó khỏi phiếu gốc. Sửa:
  - `PriceAskingRequestWriter::splitInherited`: nhóm "toàn kế thừa" xét trên hàng kế thừa của MỌI nguồn ⇒ giữ đủ dòng, 11.
  - `PriceAskingRequestService`: `transferred_request` → `transferred_requests` (mọi phiếu tách cùng thương hiệu × hãng theo `origin_request_id`, 1 query/lô cho cả danh sách lẫn chi tiết — bỏ N+1 cũ), sắp theo mã công ty.
  - `PriceAskingRequestForm.vue`: "Công ty quản lý: A, B" + mỗi phiếu tách 1 link.
  - Test: `nhom_toan_ke_thua_tu_2_nguon_giu_du_dong_va_hien_du_phieu_tach` RED (mất dòng) → GREEN; split 9/9; MasterData 708 ca, 3 đỏ sẵn. E2E mới `sale/price-asking-split-ui` (S1–S2, chặn response) 2/2. Playwright MCP 1440: 2 link cách 12px cùng hàng; 1280: tiêu đề nhóm xuống 2 dòng, không tràn. Ảnh `anh-mockup/v3-nhom-2-phieu-tach.png`.
- Final: Ruling: không chặn đổi hãng khi công ty kế thừa đang có hàng trong YCHG đã gửi (đã có N169(c) chặn đổi hãng khi hàng 2/5 ở bất kỳ công ty nào; ca còn lại — hàng Đang KD trong YCHG đang chạy — PTG sẽ báo 423) — sai thì: YCHG đó kẹt ở bước PTG, phải huỷ nhóm.
- Task 1: complete (2 migration batch mới chạy `--path --force` vào hrm_erp_21_10_prod; DB `.env` = 127.0.0.1).
- E2E 24/10 (user "Chạy e2e"): M3 đỏ — popup xác nhận chỉ nêu hãng có mã đang KD; thêm/bỏ hãng 0 mã thì popup không nêu gì (lệch mockup U3 "Thêm X / Bỏ Y"). Sửa `confirmMessage` (`pages/finance/manufacture-price-modes/index.vue`): luôn nêu hãng thêm/bỏ kèm số mã (0 cũng nêu), hãng đổi do đổi chế độ liệt kê như cũ; M2/M3 kiểm câu "Thêm …"/"Bỏ …". 2 spec mới 6/6 xanh.
- E2E: `products-catalog-popup-ui` import `utils/tempRoleFixture` không có trong `e2e/` (lệch bản có sẵn, không thuộc feature) ⇒ loại khỏi lượt chạy bộ liên quan.
- E2E bộ liên quan (19 spec hàng hoá/giá/YCHG/YCTG/PTG/báo giá, chromium + api, workers=1): 169 passed · 37 failed · 69 did not run · 5 skipped. 37 đỏ KHÔNG do feature: spec lệch code đã commit (E1 nút Tạo mới ở Đang KD — chốt 21/10), tài khoản "không quyền" nay có quyền (24 ca 403 danh mục/products-read), thiếu dữ liệu fixture (take/lifecycle A1), validate thuế suất 99,99, menu xe 6/10, logo đè nút (YCHG P6), YCTG checkbox, PTG TMĐT 2≠1, quotation-unpriced, product-history chèn role lỗi. Không ca nào chạm file feature sửa. DB sạch sau chạy.

### Checkpoint — 24/10/2026 (tối)
Vừa hoàn thành: e2e (2 spec mới + bộ liên quan), sửa popup xác nhận (M3), đóng 3 minor (1 đóng — không xảy ra; 2 user tự nhập company_id; 3 sửa). COMMIT: hrm-api `7c943033c` (40 file), hrm-client `1ab0006b6` (10 file). Chưa push.
Đang làm dở: —
Bước tiếp theo: push khi user cho phép; deploy prod = 2 migration + permission:sync + gán quyền "Cài đặt giá bán theo hãng".
Blocked: —

- 24/10/2026: đã push lên origin/gop_db (đi kèm push của session popup ảnh hàng hoá) — hrm-api 7c943033c (merge 2169b460e), hrm-client 1ab0006b6 (merge 0113bddb6). Còn lại: deploy prod (2 migration + permission:sync + gán quyền).
