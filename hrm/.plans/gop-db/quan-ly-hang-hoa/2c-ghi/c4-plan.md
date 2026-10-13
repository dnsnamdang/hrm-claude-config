> ⚠️ **08/10 user cho "làm" kèm điều kiện: BỎ HẲN phần xoá S3 (V9 đổi thành KHÔNG xoá S3).** Mọi task/file/đo liên quan S3 (FileJanitor, `PRODUCT_S3_PURGE`, `Config/config.php`, `.env.example`, D1/D2/D4, S1) KHÔNG làm. N23/N24 (helper S3 gắn key production, URL path-style) vẫn giữ trong danh sách việc ngoài luồng.

# Đợt 2-C4 — Vòng đời: Xoá + Khoá/Mở khoá theo công ty — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (hoặc executing-plans). Bước dùng checkbox `- [ ]`.
> 08/10/2026 · @namdangit · CHỈ là tài liệu — chưa đụng source. Code chỉ bắt đầu khi user trả lời **"làm"** cho mục 0 (CLAUDE.md root), mỗi PHA xin riêng.

**Goal:** Công ty có quyền 1652 (1) **xoá** hàng *Đang nhập thông tin* — công ty tạo thì xoá cứng hàng + mọi bảng con + tệp S3 không còn ai dùng, công ty lấy về thì gỡ phần của mình; (2) **khoá** hàng *Đang kinh doanh* tại công ty mình (3 → 4 *Ngừng kinh doanh*) và **mở khoá** (4 → 3). Từng dòng, ở menu dòng + footer chi tiết.

**Architecture:** BE thêm `ProductLifecycleService` (destroy = `hardDelete` | `release`, `lock`, `unlock`), `ProductUsageGuard` (điều kiện chứng từ / tham chiếu), `ProductFileJanitor` (xoá S3 sau commit) + `ProductLifecycleController` với 3 route trong khối `products`; luật cờ đặt ở entity `Product` cạnh `editableAt`/`takeableAt`; đổi 403 → 423 cho hàng đang khoá. FE mở rộng `ProductListPage.vue` (3 action dòng theo cờ BE) + footer chi tiết + `edit.vue` (423).

**Tech Stack:** Laravel 8.83 + nwidart, PHP 7.4 (`/opt/homebrew/opt/php@7.4/bin/php`), PHPUnit `DatabaseTransactions` trên `hrm_erp` · Nuxt 2 / Vue 2, V2Base* · Playwright (MCP để kiểm + spec viết sẵn).

**Spec / luật (thứ tự ưu tiên):** `chot.md` mục *Chốt riêng đợt 2-C4* **V1–V9** (cao nhất, ĐÈ đề xuất khảo sát) > G6, G7, G9a, B3, L1–L7, D2 > `man-danh-muc-hang-hoa/design.md` §35b-4 > `c4-khao-sat-be.md` > `c4-khao-sat-fe.md` §4 (T1–T9) > mockup. Đáp án `c4-ton.md` Q1–Q9. Tiền đề #8 `SO-CHOT-VA-TON.md`: hệ số giá sẽ bỏ ⇒ dòng coef 1 sinh khi khoá (làm tròn nghìn ở popup ERP) chỉ là hệ quả tạm.

**Đã kiểm lại file:dòng khảo sát (08/10, worktree HEAD api `d3c6496a1` / client `5c2cfb823`, nhánh `feat/chuyen-doi-hang-hoa`, cây sạch):**
- BE (`hrm-api/Modules/MasterData/`): khối route `Routes/api.php:253-292` (POST `/` :283, `/take` :285, `GET /{product}/edit` :287, `PUT admin-data` :288, `PUT /{product}` :289, `GET /{product}` :291) · `ProductWriteService` `assertCanWrite` :95-99, `assertOwner` :103-115 (abort status 4 ở **:114**), `assertCanEditAdmin` :123-135 (abort status 4 ở **:134**), `writeTechAttachments` :387-431, `writeGalleries` :438-459 (avatar = ảnh đầu :455), `writeVideos` :461-471 · `Product.php` `companyStatusSql` :383, `ownerStatusSql` :400-407, `editableAt` :423-428, `takeableAt` :434-440, `companyRowFor` :445, `tradingCompanyNames` :456-473 · `ProductCompany.php` hằng `STATUS_STOPPED` :26, `STATUS_TEXT/COLOR` :29-41 · `ProductListResource.php:56-63` · `ProductDetailResource.php:39-44` · `ProductService` `show()` :117 (nạp `companies` chỉ công ty mình :140-143), `applyScreen` :174-205, list nạp mọi `companies` :278-281 · test 403-status-4: `ProductWriteApiTest.php:403-404`, `ProductTakeApiTest.php:452-453` (edit) + **:644-645** (admin-data — khảo sát ghi :479-482, thực ra :479 là ca `can_edit`, không đổi mã) · mock S3: `ProductWriteApiTest.php:30-37`, `ProductImageUploadTest.php:20-24`.
- FE (`hrm-client/`): `ProductListPage.vue` (1186 dòng) `#cell-actions` :309-310, ô lọc Trạng thái :583, cột actions :667, `hasActionsColumn` :701-703, `rowActionsOf` :790, `onRowAction` :799, `listSelected` :481/:826 · `utils/product-list-screens.js` (197) `warehouse` rowActions+takeBack :74-75, `trading` :131 · `_id/index.vue` (206) `V2Footer :menu` :41-42 · `V2Footer.vue` `menu.delete` :125, slot `#custom-actions` :160 · `_id/edit.vue` `onLoadError` chỉ bắt 403/404 → 423 rơi nhánh toast + form trắng · `utils/helpers.js` `saveErrorMessage` có nhánh 423 · `plugins/axios.js:32` interceptor toast 403 (không toast 423/422).
- e2e (`wt-chuyen-doi-hang-hoa/e2e/`): `products-form-ui.spec.ts` E4 `:427` (`['Sửa','Quay lại']`), E12b `:521-530` (`test.skip` :525) · `products-read-ui.spec.ts` `SCREENS.trading` `:27-28` (không có `'Hành động'`), `WRITE_BUTTONS` :32 · `utils/apiDb.ts` `API_REPO` :14, `runMysql` :23, `flushApiPermissionCache` :61.
- DB `hrm_erp` (SELECT 08/10): `product_company_coefficients` 1.105 dòng, **0** `status` NOT NULL; 172 FK trỏ `products` (0 CASCADE); 49 bảng có `product_id` không FK mà HRM có code đọc/ghi (mục 2.3).

**Phát hiện mới khi khảo sát thêm cho V9 (S3):**
1. Helper S3 của HRM là `App\Helper\CmcS3Helper` (`hrm-api/app/Helper/CmcS3Helper.php`, 293 dòng): **credentials CMC thật hard-code** trong constructor (:24-25) ⇒ mọi lời gọi không mock trong PHPUnit / local là gọi **bucket production `tanphat`**. Có sẵn `deleteByUrl($url, $allowedPrefix)` :236-249 (chỉ xoá key nằm trong prefix) + `keyFromUrl()` :170-189 — **chỉ hiểu URL virtual-host** `https://tanphat.s3.cloud.cmctelecom.vn/<key>`.
2. Ảnh hàng hoá lưu **URL path-style** `https://s3.cloud.cmctelecom.vn/tanphat/erp_products/…` (45.278/45.890 `products.avatar`, 29.656 `product_templates.avatar`) ⇒ `keyFromUrl` trả null ⇒ `deleteByUrl` âm thầm không xoá gì. Tài liệu kỹ thuật (`files.file_path`) là virtual-host `…/products/…` (10 dòng). `product_galleries.url` cũ là đường tương đối `/uploads/products/…` (ổ đĩa ERP, không phải S3). Upload ảnh 2-C1 (`ProductImageController` → `putFileProduct($file, 'erp_products')` :116-158) sinh **3 object**: gốc + `-thumbnail` (75px) + `-large` (200px); DB chỉ lưu URL gốc (`url`), ERP tự suy 2 bản kia. Kiểu URL `ObjectURL` mà HRM nhận được chưa có mẫu ở DB local (dữ liệu thử 2-C1 đã dọn) ⇒ phải xử lý **cả 2 kiểu**.
3. Có **23** `products.avatar` lưu thẳng URL `-thumbnail` và chứng từ chép avatar sang **20 cột `avatar`** (vd `firm_quotation_group_products` 458k dòng, 493.843 dòng `erp_products/`) — không index ⇒ kiểm "còn ai dùng" phải so **cả 3 biến thể × 2 kiểu URL**, đo 6 bảng lớn ≈ **4,3 s/1 URL** (1 câu `IN (…)` mỗi cột cho mọi URL ⇒ chi phí gần như không đổi theo số URL).
4. Laravel 8.83 `ManagesTransactions::commit()` chỉ chạy callback `DB::afterCommit` khi cấp transaction về **0** ⇒ trong PHPUnit `DatabaseTransactions` callback **không bao giờ chạy** ⇒ không test được. Khuôn meeting (`Modules/Assign/Services/MeetingService.php:918-935`) dùng `afterCommit` + `new CmcS3Helper()` (không mock được) — **không chép khuôn đó**.

---

## 0. Phạm vi xin phép (đưa user duyệt "làm" — mỗi PHA xin riêng)

| | |
|---|---|
| Repo | `hrm-api` + `hrm-client`, worktree `websites/wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}` |
| Nhánh | **`feat/p2c4-vong-doi`** tạo từ `feat/chuyen-doi-hang-hoa` (api `d3c6496a1`, client `5c2cfb823`) ở cả 2 repo, trong worktree. Xong từng pha: commit trên nhánh con (hỏi trước khi commit); xong cả đợt: merge `--no-ff` về `feat/chuyen-doi-hang-hoa` + push — **hỏi riêng**. ⛔ **KHÔNG merge / cherry-pick sang `gop_db`** (memory *khong-merge-vao-gop-db*) |
| BE — tạo (5) | `Services/Product/ProductLifecycleService.php` · `Services/Product/ProductUsageGuard.php` · `Services/Product/ProductFileJanitor.php` · `Http/Controllers/V1/Product/ProductLifecycleController.php` · `Tests/Feature/ProductLifecycleApiTest.php` |
| BE — sửa (7 + 2 test) | `Routes/api.php` (khối :253-292, 3 route) · `Entities/Product/Product.php` (cờ + luật khoá) · `Entities/Product/ProductCompany.php` (hằng câu báo + `isLocked`) · `Services/Product/ProductWriteService.php` (403 → 423 ở :114, :134) · `Services/Product/ProductService.php` (`show()` thêm cột đếm công ty khác đang dùng) · `Transformers/Product/ProductListResource.php` · `Transformers/Product/ProductDetailResource.php` · `Config/config.php` (khoá `product_s3_purge`) · `.env.example` (`PRODUCT_S3_PURGE=false`) — test: `Tests/Feature/ProductWriteApiTest.php` (:403-404) · `Tests/Feature/ProductTakeApiTest.php` (:452-453, :644-645) |
| FE — tạo (1) · sửa (4) | tạo `utils/productLifecycle.js` (câu hỏi + gọi API + toast dùng chung list/chi tiết) · sửa `utils/product-list-screens.js` · `components/product/ProductListPage.vue` · `pages/master-data/products/_id/index.vue` · `pages/master-data/products/_id/edit.vue` |
| e2e (không phải repo git — `wt-chuyen-doi-hang-hoa/e2e`, chép bản cuối về `HRM/e2e`) | tạo `tests/master-data/products-lifecycle.api.spec.ts`, `tests/master-data/products-lifecycle-ui.spec.ts`; sửa `products-form-ui.spec.ts` (E4, E12b), `products-read-ui.spec.ts` (`SCREENS.trading`, docblock, footer) |
| Migration / seeder / quyền mới | **KHÔNG** (V8: dùng 1652; cột `status` + 4 ô có sẵn ở `product_company_coefficients`). Không chạy `migrate`, không chạy seeder |
| Ghi DB local `hrm_erp` | (1) PHPUnit: chỉ trong `DatabaseTransactions` (rollback). (2) Kiểm Playwright MCP + e2e (khi user cho): **tạo 3–4 hàng thử qua `POST products`** (Cty 1, KHÔNG ảnh / video / tài liệu) rồi xoá chúng qua chính tính năng; **khoá/mở khoá 1 hàng ERP cũ của Cty 1 chưa có dòng** ⇒ sinh 1 dòng `product_company_coefficients` (coef 1) — ghi id trước, **DELETE đúng id** sau khi đo; gỡ: lấy về 1 mã Cty 4 (như 2-C2) rồi gỡ. (3) Role tạm `E2E C4 tạm - chỉ xem hàng công ty` (chỉ 1653) gán `e2e_cmd_noperm@test.local` + `cache:clear`, gỡ ở `afterAll`. **Hỏi riêng trước khi ghi (2)(3)** |
| S3 thật | ⛔ **KHÔNG đụng.** (a) PHPUnit: bind `Mockery::mock(CmcS3Helper::class)` ở `setUp` của MỌI test chạy đường xoá (mock strict — gọi hàm lạ là nổ), ca nào cũng assert danh sách key nhận được. (b) Công tắc `config('masterdata.product_s3_purge')` đọc `PRODUCT_S3_PURGE`, **mặc định `false`** ⇒ worktree / máy dev không có biến này thì janitor chỉ ghi log "bỏ qua", không gọi S3; test bật bằng `config([...=> true])`. (c) Fixture e2e/MCP tạo hàng **không tệp** + assert bằng SQL `avatar IS NULL`, 0 dòng `product_galleries`/`product_videos`/`files` trước khi bấm Xóa. (d) Kiểm sau cùng: `grep "ProductFileJanitor" storage/logs/laravel-*.log` chỉ có dòng "bỏ qua (tắt công tắc)" hoặc "không có tệp" |
| Không đụng | ERP · `CmcS3Helper.php` (dùng chung với meeting — chỉ GỌI, không sửa) · popup 2-C3 · form 2-C1/2-C2 (chỉ `edit.vue` bắt 423) · `tradingCompanyNames` (N18 để riêng — xem Q-D9) |

**3 pha, 15 task:**

| Pha | Task | Deliverable kiểm được |
|---|---|---|
| **P1 — BE** | B1–B9 | `ProductLifecycleApiTest` xanh (đủ ca mục 3); hồi quy 11 file test MasterData sản phẩm xanh (đã sửa 3 ca 403 → 423) |
| **P2 — FE** | F1–F4 | Playwright MCP đo DOM từng luồng (bảng 4.3) |
| **P3 — e2e + chốt** | E1–E2 | spec mới + sửa viết xong, `--list` OK (chạy khi user yêu cầu, `--workers=1`); review cuối; checkpoint |

---

## Global Constraints

- **V1** Khoá chỉ 3 → 4, mở khoá chỉ 4 → 3. Chủ hàng cũ chưa có dòng ⇒ INSERT `coefficient = 1` (`ProductCompany::NEUTRAL_COEFFICIENT`), `status = 4`, `created_by`; chủ có dòng ERP `status NULL` (suy ra 3) ⇒ UPDATE `status = 4`, **giữ `coefficient`**. Mọi thao tác GHI khi trạng thái mình = 4 ⇒ **423** (sửa đầy đủ, tab Quản trị, mở form sửa, xoá/gỡ, khoá lại); **mở khoá là ngoại lệ duy nhất**.
- **V2** "Chưa phát sinh chứng từ" = 0 dòng ở **149 cột FK ngoài** + **4 cột FK chiều ngược** + **49 bảng không FK** HRM đang dùng (mục 2.3) — danh sách là **hằng số trong code** + test so khớp `information_schema` (phát hiện FK/bảng mới). FK 1451 lúc `DELETE products` là chốt cuối ⇒ rollback + 422.
- **V3** Cờ `can_delete` ở danh sách/chi tiết là **cờ nhẹ** (trạng thái + chủ + chưa ai lấy về + quyền), KHÔNG chạy guard chứng từ; kiểm đầy đủ khi bấm ⇒ 422 kèm lý do.
- **V4** Công ty lấy về chỉ gỡ được khi trạng thái của mình = 1.
- **V5** Gỡ = dọn hết phần công ty mình: dòng công ty (dòng ERP `created_by IS NULL` ⇒ `status = NULL` + 4 ô quản trị NULL, **giữ `coefficient`**; dòng HRM sinh `created_by NOT NULL` ⇒ DELETE), `product_suppliers` + `product_business_catalogs` `WHERE company_id = mình`. KHÔNG đụng `products` + phần công ty khác. KHÔNG xoá S3.
- **V6** Hàng đang được hàng khác tham chiếu (máy dùng cho / phụ kiện / phụ kiện lắp đặt / sửa chữa / thành phần bộ) ⇒ chặn xoá + câu lý do riêng.
- **V7** Không hàng loạt — từng dòng (menu dòng + footer chi tiết).
- **V8** Quyền 1652 *Xây dựng thông tin hàng hoá* (middleware `checkPermission` + `assertCanWrite()` theo công ty đang làm việc — R22). Không quyền mới, không bypass super admin.
- **V9** Xoá cứng ⇒ xoá tệp S3 của hàng mà **không còn dòng nào trỏ tới** (sau khi xoá DB); làm **SAU commit**, lỗi S3 chỉ `Log::warning`, không làm hỏng xoá DB, response vẫn 200.
- `company_id` của dòng mới gán TAY = `auth()->user()->current_company_role` (`DB::table`, không qua hook `BaseModel::creating`).
- Xoá cứng `productables`: xoá **mọi `productable_type`** của `product_id` (cố ý — xoá cả hàng; comment rõ để reviewer không "sửa" thành kẹp type). Chiều ngược (`productable_type = 'App\Product' AND productable_id = id`) là dữ liệu hàng khác ⇒ CHẶN (V6), không xoá.
- Mọi đường ghi trong `DB::transaction` + `lockForUpdate` dòng `products` + mọi dòng `product_company_coefficients` của hàng (đua xoá/khoá ⇒ lượt 2 nhận 404/422/423 đúng trạng thái mới).
- Ghi `updated_by`, `updated_at` khi khoá/mở khoá/gỡ (CLAUDE.md HRM). Lịch sử khoá/mở khoá: **không ghi** — §14b hoãn lịch sử hàng hoá (lệch CLAUDE.md HRM :66, ghi ở rủi ro R9).
- 403/423 luôn TRƯỚC 422 (thứ tự xét ở mục 1.1).
- Test quyền 2 phía (có / không 1652 / 1652 chỉ ở công ty khác) — memory *always-test-permission-cases*.
- FE: V2Base*, `$confirm` (không `b-modal`/`msgBoxConfirm`), `V2BaseRowActions` icon, slot `#cell-<key>`, cờ hiển thị đọc từ BE (KHÔNG suy khoá/mở từ `status` thô — memory *danh-muc-bang-erp-khoa-bang-0*), không chờ `networkidle`, e2e `--workers=1`; KHÔNG tự chạy e2e (chỉ `--list`) nhưng BẮT BUỘC kiểm Playwright MCP + đo DOM trước khi báo xong.

Lệnh test BE: `cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/<File>.php [--filter <ca>]`. KHÔNG `config:cache` (memory *erp-local-config-cache*: kiểm `bootstrap/cache/config.php` không tồn tại trước khi chạy).

---

## 1. Hợp đồng API

Mọi route đặt trong khối `products`, `->where('product','[0-9]+')`, middleware `checkPermission:Xây dựng thông tin hàng hoá`, đứng TRƯỚC `GET /{product}` (:291). Controller `V1\Product\ProductLifecycleController`.

### 1.1 `DELETE /api/v1/master-data/products/{product}` (MỚI)

Không body. Thứ tự xét (dừng ở điều kiện đầu tiên vướng):

| # | Điều kiện | HTTP · `message` |
|---|---|---|
| a | không 1652 ở mọi công ty | **403** (middleware) |
| a' | 1652 chỉ ở công ty khác công ty đang làm việc | **403** "Bạn không có quyền xây dựng thông tin hàng hoá ở công ty đang làm việc." (`assertCanWrite`) |
| b | hàng không tồn tại (cả lượt xoá thứ 2) | **404** |
| c | `products.status ≠ 1` (D2) | **403** "Hàng hoá đã bị xoá ở ERP, không thao tác được." |
| d | không phải chủ VÀ dòng mình `status` NULL/không có | **403** "Công ty chưa dùng hàng hoá này." |
| e | trạng thái mình = 4 | **423** "Hàng hoá đang ngừng kinh doanh, vui lòng mở khoá trước khi cập nhật." |
| f | trạng thái mình ≠ 1 (chủ: **dòng thật** = 1; hàng ERP cũ suy ra 3 ⇒ chặn) | **422** "Chỉ xoá được hàng hoá đang ở trạng thái Đang nhập thông tin." |
| — | **Nhánh CHỦ** (`products.company_id = current_company_role`) ⇒ xoá cứng | |
| g | công ty khác có dòng `status` NOT NULL | **422** "Hàng hoá đã có công ty khác lấy về (<tên công ty, nối dấu phẩy>), không xoá được." |
| h | ERP 4 điều kiện (giữ nguyên câu ERP): `stocks.accounting_qty > 0` · mượn chưa trả (`product_export_request_details` ⨝ `product_export_requests.type = 3`, `base_exported_qty > borrow_returned_qty`) · `product_has_accessories.product_id = id` · `recipe_products.product_id = id` | **422** "Hàng có tồn kho!" · "Hàng đang mượn chưa trả hết!" · "Hàng nằm trong danh sách phụ kiện!" · "Hàng nằm trong công thức ghép bộ!" |
| i | V6 tham chiếu ngược khác: `product_has_install_accessories.product_id` · `product_has_repair_accessories.product_id` · `productables` (`productable_type = 'App\Product'`, `productable_id = id`) | **422** "Hàng nằm trong danh sách phụ kiện lắp đặt của hàng hoá khác!" · "…phụ kiện sửa chữa…" · "Hàng đang được khai là Máy dùng cho của hàng hoá khác!" (kèm ≤ 3 mã hàng tham chiếu: "(<mã>, <mã>…)") |
| j | V2 chứng từ: có dòng ở 149 cột FK ngoài hoặc 49 bảng không FK | **422** "Hàng hoá đã phát sinh chứng từ, không xoá được." |
| k | `QueryException` SQLSTATE 23000 / errno **1451** khi DELETE (lọt lưới j) | rollback ⇒ **422** cùng câu j + `Log::warning` tên ràng buộc (để bổ sung hằng) |
| ok | xoá 20 bước (mục 2.1) trong 1 transaction ⇒ sau commit gọi `ProductFileJanitor` (V9) | **200** `{ "data": { "id": 123, "code": "TP-0001", "mode": "deleted" } }` |
| — | **Nhánh CÔNG TY LẤY VỀ** ⇒ gỡ (V5); KHÔNG xét g–k (không đụng `products`) | **200** `{ "data": { "id", "code", "mode": "released", "company_name" } }` |

Lỗi 422 trả `{ message: <lý do>, errors: {} }` — KHÔNG có lỗi theo ô ⇒ FE đọc thẳng `message` (KHÔNG dùng `saveErrorMessage`, nhánh 422-không-field của nó đổi thành "tải lại trang").

### 1.2 `PUT /api/v1/master-data/products/{product}/lock` (MỚI)

| # | Điều kiện | HTTP |
|---|---|---|
| a, a', b, c, d | như 1.1 | 403 / 403 / 404 / 403 / 403 |
| e | trạng thái mình = 4 | **423** "Hàng hoá đang ngừng kinh doanh." (Q-D3) |
| f | trạng thái mình ∈ {1, 2} | **422** "Chỉ khoá được hàng hoá đang ở trạng thái Đang kinh doanh." |
| ok | = 3: dòng thật ⇒ UPDATE `status 4`; chủ chưa có dòng ⇒ INSERT coef 1 status 4 `created_by`; chủ có dòng ERP `status NULL` ⇒ UPDATE `status 4` giữ hệ số | **200** `{ data: { id, code, company_status: 4, status_text: "Ngừng kinh doanh", status_color: "#DC2626" } }` |

### 1.3 `PUT /api/v1/master-data/products/{product}/unlock` (MỚI)

KHÔNG qua guard 423. a–d như 1.1 · trạng thái mình ≠ 4 ⇒ **422** "Hàng hoá không ở trạng thái Ngừng kinh doanh." · = 4 ⇒ UPDATE `status 3`, KHÔNG xoá dòng HRM sinh lúc khoá (tiền đề #8) ⇒ **200** `{ data: { id, code, company_status: 3, status_text: "Đang kinh doanh", status_color: "#16A34A" } }`.

### 1.4 Cờ ở resource (SỬA — `ProductListResource` + `ProductDetailResource`, 1 luật ở entity)

| Cờ | Luật (đều AND `canBuild` = 1652 tại công ty đang làm việc, AND `products.status = 1`) |
|---|---|
| `can_delete` | trạng thái mình = 1 ∧ (**chủ** ∧ không công ty khác `status` NOT NULL) ∨ (**không phải chủ** — V4) — **cờ nhẹ V3**, không xét h–k |
| `delete_mode` | `'destroy'` (chủ) \| `'release'` (công ty lấy về) \| `null` khi `can_delete = false` — FE chọn câu hỏi/toast |
| `can_lock` | trạng thái mình = 3 (gồm 3 suy ra của chủ) |
| `can_unlock` | trạng thái mình = 4 |
| `can_edit` | GIỮ nguyên `editableAt` (đã loại 4) |

- Hàm entity: `Product::deletableAt(int $companyId, ?int $status, bool $othersUsing): bool`, `deleteModeAt(...)`, `lockableAt(?int $status)`, `unlockableAt(?int $status)`; `ProductCompany::isLocked(?int $status)`.
- Danh sách: `othersUsing` đọc từ `companies` đã nạp (mọi công ty — `ProductService.php:278-281`), không query thêm. Chi tiết: `show()` nạp `companies` chỉ công ty mình (:140-143) ⇒ thêm 1 `selectRaw('(select count(*) from product_company_coefficients x where x.product_id = products.id and x.company_id <> ? and x.status is not null) as others_using_count')`.

### 1.5 Đổi 403 → 423 (SỬA — V1)

`ProductWriteService::assertOwner` :114 và `assertCanEditAdmin` :134: `abort(403, …)` ⇒ `abort(423, 'Hàng hoá đang ngừng kinh doanh, vui lòng mở khoá trước khi cập nhật.')` (hằng `ProductCompany::LOCKED_MESSAGE`). Thứ tự giữ nguyên: công ty (403) → D2 (403) → khoá (423); `authorize()` của FormRequest chạy TRƯỚC validator ⇒ 423 vẫn đứng trước 422. Ảnh hưởng: `GET /{id}/edit`, `PUT /{id}`, `PUT /{id}/admin-data`.

---

## 2. Dữ liệu: xoá cứng, chứng từ, tham chiếu, S3

### 2.1 Xoá cứng — 20 bước theo thứ tự (nhánh chủ, 1 transaction)

Trước bước 1: gom URL tệp (mục 2.5) **trong transaction** (đọc sau `lockForUpdate`).

| # | Bảng | Khoá xoá | Ghi chú |
|---|---|---|---|
| 1 | `product_expected_prices` | `unit_price_id IN (giá của ĐVT hàng)` | FK → `product_unit_prices` |
| 2 | `product_unit_prices` | `product_unit_id IN (ĐVT hàng)` | 6 dòng/ĐVT (G2) |
| 3 | `product_units` | `product_id` | |
| 4 | `attribute_products` | `product_id` | |
| 5 | `recipe_products` | `base_product_id` | chiều ngược `product_id` đã chặn ở h |
| 6 | `product_has_accessories` | `base_product_id` | |
| 7 | `product_has_install_accessories` | `base_product_id` | |
| 8 | `product_has_repair_accessories` | `base_product_id` | |
| 9 | `files` | `` `table` = 'product_tech_attachments' AND table_id IN (…) `` | |
| 10 | `product_tech_attachments` | `product_id` | |
| 11 | `product_galleries` | `product_id` | |
| 12 | `product_videos` | `product_id` | |
| 13 | `productables` | `product_id` (**mọi type**) | không FK |
| 14 | `product_vehicle_model_has_life` | `product_id` | không FK |
| 15 | `product_company_coefficients` | `product_id` (mọi công ty — g đã bảo đảm chỉ còn dòng chủ / dòng ERP `status NULL` của công ty khác) | ⚠️ dòng hệ số cũ của công ty khác bị xoá cùng — hàng không còn, đúng |
| 16 | `product_suppliers` | `product_id` (mọi công ty) | |
| 17 | `product_business_catalogs` | `product_id` (mọi công ty) | |
| 18 | `product_barcodes`, `product_categories`, `product_prices`, `product_documents`, `product_features`, `product_histories`, `product_versions` | `product_id` | ERP ghi khi sửa ở ERP (N4) — là dữ liệu CỦA hàng, không phải chứng từ |
| 19 | `product_approve_prices` (theo `product_approve_id` cha) → `product_approves` | `product_id` | không FK |
| 20 | `products` | `id` | `DB::table` (Product không SoftDeletes, BaseModel không hook `deleting`) |

### 2.2 Chứng từ có FK (V2) — 149 cột ngoài + 4 cột chiều ngược

Chiều ngược (FK, nhưng xét ở h/i để có câu riêng): `product_has_accessories.product_id`, `recipe_products.product_id`, `product_has_install_accessories.product_id`, `product_has_repair_accessories.product_id`.

149 cột FK ngoài (`product_id` trừ khi ghi khác), hằng `ProductUsageGuard::FK_COLUMNS`:
accounting_stocks, beginning_accounting_stocks, beginning_stocks, borrow_export_product_details, borrow_export_products, borrow_export_request_product_details, borrow_export_request_products, borrow_sell_product_details, borrow_sell_products, borrow_sell_request_product_details, borrow_sell_request_products, buy_contract_product2, buy_contract_product_detail2, buy_contract_products, buy_request_products, combo_campaign_checkpoint_group_option_products, combo_campaign_products, combo_campaign_promotions, contract_annex_products, contract_combo_group_option_products, contract_combo_products, contract_product_promo_group_options, contract_products, contract_promotions, delivery_cost_asking_request_customer_products, final_rule_inland_buy_contract_products, firm_contract_combo_group_option_products, firm_contract_combo_products, firm_contract_promotions, firm_quotation_combo_group_option_products, firm_quotation_combo_products, firm_quotation_promotions, handover_acceptance_product_record_details, handover_acceptance_record_products, handover_record_products, hold_details, inland_buy_contract_product2, inland_buy_contract_product_detail2, inland_buy_contract_products, inland_order_request_product2, inland_order_request_product_buyers, inland_order_request_products, inland_order_summary_product2, inland_order_summary_product_detail2, inland_product_allocation_details, inland_product_arrived_notify_product_details, inland_product_arrived_notify_products, install_estimate_products, install_summary_install_accessories, install_summary_products, inventory_export_details, inventory_import_details, inventory_products, job_norms, join_export_request_product_recipes, join_export_request_products, manufacture_expect_price_except_products, order_import_request_product_details, order_import_request_products, order_request_product2, order_request_products, order_summary2_histories, order_summary_product2, order_summary_product_detail2, order_summary_product_details, order_summary_products, order_summary_promotion2, position_inventory_item_products, position_transfer_details, prepick_cancel_details, prepick_cancel_request_details, prepick_extend_request_details, prepick_transfer2_details, prepick_transfers, price_asking_request_products, price_calculate_products, price_calculate_request_products, price_calculate_result_products, product_accessories.accessory_id, product_accessories, product_allocation_details, product_arrived_notify_details, product_arrived_notify_product2, product_arrived_notify_product_detail2, product_export_details, product_export_request_accessories, product_export_request_combo_group_option_products, product_export_request_combo_products, product_export_request_detail_promo_group_options, product_export_request_details, product_import_details, product_import_request_details, product_prepick_request_details, product_transfer_details, product_transfer_request_products, project_analysis_group_products, project_analysis_tab_products, project_contract_group_products, project_contract_products, project_contract_tab_products, project_quotation_group_products, project_quotation_tab_products, promo_campaign_product_checkpoint_group_options, promo_campaign_products, quotation_product_promo_group_options, quotation_products, quotation_template_products, root_contract_products, rule_inland_buy_contract_products, rule_inland_product_arrived_notify_product_details, rule_inland_product_arrived_notify_products, service_contract_item_products, service_has_products, service_quotation_item_products, service_quotation_items, split_export_request_product_recipes, split_export_request_products, stock_position_details, stock_positions, stocks, summary_annex_product_details, summary_annex_products, tmp_position_transfer_details, tmp_warehouse_export_lot_details, tmp_warehouse_export_lots, tmp_warehouse_import_lot_details, tmp_warehouse_import_lots, transfer_product_allocation_details, warehouse_export_lot_details, warehouse_export_lots, warehouse_export_request_accessories, warehouse_export_request_details, warehouse_import_lot_details, warehouse_import_lots, warehouse_import_request_details, warehouse_prepick_request_details, warehouse_reexport_lot_details, warehouse_reexport_lots, warehouse_reimport_lot_details, warehouse_reimport_lots, warehouse_transfer_lot_exports, warehouse_transfer_lot_imports, warehouse_transfer_lots, warranty_repair_handle_request_products, warranty_repair_request_products, warranty_request_products.base_product_id, warranty_request_products, warranty_work_products.base_product_id, warranty_work_products.

(23 cột FK còn lại = bảng con của chính hàng ở 2.1 + 4 cột chiều ngược trên. Tổng 172 — test B3 so khớp: `FK_COLUMNS ∪ CHILD_FK ∪ REVERSE_FK = information_schema`.)

### 2.3 Bảng KHÔNG FK mà HRM đang đọc/ghi (V2) — 49 bảng, hằng `ProductUsageGuard::NO_FK_COLUMNS`

Cách lập (SELECT 08/10): cột `product_id`/`base_product_id` không FK, loại `product_template*`, `product_info*`, `recipe_product_(infos|templates)`, `tmp_product_*`, `*bak*`, `productables`, `product_vehicle_model_has_life`, `product_classifies`, `product_approve*` (còn 140 cột) ∩ tên bảng xuất hiện dạng chuỗi trong `hrm-api/{app,Modules}` ⇒ 49. Cột `product_id`, chỉ 3 bảng có index (đánh dấu ⓘ):

account_details (1,07 tr dòng), accounting_prepick_cancel_detail_customers, accounting_prepick_cancel_details, assign_task_progress, borrow_sell_request_tab_product_details, borrow_sell_request_tab_products, borrow_sell_tab_product_details, borrow_sell_tab_products, device_error_products, equipments_old, external_equipments ⓘ, firm_contract_tab_products ⓘ, firm_warranty_confirm_products, firm_warranty_products, inland_buy_contract_new_product_details, inland_buy_contract_promotions, inland_product_arrived_new_product_details, inland_product_arrived_new_promotions, order_stock_progress, prepick_details, product_arrived_notify_products, product_arrived_notify_promotions, product_export_detail_accounting, product_export_request_tab_products, product_import_detail_accountings, product_import_detail_customers, product_import_direct_details, product_import_direct_transfer_products, product_import_request_detail_customers, product_import_tab_products, serials, service_contract_items, wr_assign_task_extend_products, wr_assign_task_products, wr_import_result_products, wr_import_result_services, wr_service_contract_extend_product_service_items, wr_service_contract_extend_products, wr_service_contract_items, wr_service_contract_merchandises, wr_service_contract_product_item_device_errors, wr_service_contract_product_items, wr_service_contract_products, wr_service_quotation_extend_product_service_items, wr_service_quotation_extend_products, wr_service_quotation_merchandises, wr_service_quotation_product_item_device_errors, wr_service_quotation_product_items, wr_service_quotation_products ⓘ.

Cách quét: 1 câu `SELECT 1 FROM (… UNION ALL (SELECT 1 FROM <t> WHERE <c> = ? LIMIT 1) …) x LIMIT 1` cho FK (0,3–0,7 s) rồi 1 câu tương tự cho 49 bảng không FK (đo lại khi làm — phần lớn chi phí 2,8–9,4 s của 139 cột nằm ở `account_details`). Bảng không còn tồn tại ở DB (đổi tên/xoá) ⇒ bỏ qua bằng danh sách `SHOW TABLES` nạp 1 lần, KHÔNG nổ 500 (test B3 cảnh báo).

### 2.4 Tham chiếu chiều ngược (V6) — chặn, không tự gỡ

| Nguồn | Điều kiện | Câu báo |
|---|---|---|
| `product_has_accessories` (ERP đk 4) | `product_id = id` | "Hàng nằm trong danh sách phụ kiện!" |
| `recipe_products` (ERP đk 5) | `product_id = id` | "Hàng nằm trong công thức ghép bộ!" |
| `product_has_install_accessories` | `product_id = id` | "Hàng nằm trong danh sách phụ kiện lắp đặt của hàng hoá khác!" |
| `product_has_repair_accessories` | `product_id = id` | "Hàng nằm trong danh sách phụ kiện sửa chữa của hàng hoá khác!" |
| `productables` (không FK) | `productable_type = Productable::TYPE_PRODUCT` (`App\Product`) `AND productable_id = id` | "Hàng đang được khai là Máy dùng cho của hàng hoá khác!" |

Mỗi câu kèm ≤ 3 mã hàng đang tham chiếu (`products.code` của `base_product_id`/`product_id` bên kia) để người dùng biết đi gỡ ở đâu.

### 2.5 Tệp S3 (V9) — `ProductFileJanitor`

**Gom (trong transaction, trước bước 1):** `products.avatar` · `product_galleries.url` · `product_videos.url` · `files.file_path` (`table = 'product_tech_attachments'`). Mỗi URL quy về **khoá S3** theo cả 2 kiểu: virtual-host `https://tanphat.s3.cloud.cmctelecom.vn/<key>` và path-style `https://s3.cloud.cmctelecom.vn/tanphat/<key>` (janitor tự đổi path-style → virtual-host trước khi gọi `CmcS3Helper::deleteByUrl`, KHÔNG sửa helper). Bỏ qua: URL tương đối (`/uploads/…`, `images/noimage.png`), host lạ, khoá trong `tanphat_hrm/tmp/`, khoá ngoài 2 prefix cho phép.

| Loại | Prefix cho phép | Nhóm khoá xoá |
|---|---|---|
| Ảnh (avatar, gallery) | `erp_products/` | gốc + `<stem>-thumbnail.<ext>` + `<stem>-large.<ext>` (1 nhóm; URL đầu vào là `-thumbnail`/`-large` thì quy về stem gốc) |
| Video (`product_videos.url` — thường là link ngoài) | `erp_products/` | chỉ khoá đó (link YouTube… bị bỏ qua vì host lạ) |
| Tài liệu kỹ thuật | `products/` | chỉ khoá đó |

**"Còn ai dùng" (chạy SAU commit, đọc DB đã xoá):** với mọi biến thể (3 tên × 2 kiểu URL) của 1 nhóm, 1 câu `IN (…)` / `LIKE` mỗi cột dưới đây; có ≥ 1 dòng ⇒ giữ CẢ nhóm:
- Lớp hàng: `products.avatar`, `product_galleries.url`, `product_videos.url`, `product_templates.avatar`, `product_template_galleries.url`, `product_template_videos.url`, `product_infos.avatar`, `product_info_galleries.url`, `product_info_videos.url`, `tmp_products.avatar`, `tmp_product_galleries.url`, `tmp_product_videos.url`, `tmp_products.tech_attachments` (LIKE khoá), `files.file_path` (mọi `table`).
- Chứng từ chép avatar (20 cột `avatar`): contract_products, firm_contract_group_products, firm_contract_tab_products, firm_quotation_group_products, firm_quotation_tab_products, order_request_products, product_export_request_accessories, product_export_request_details, product_prepick_request_details, project_analysis_group_products, project_analysis_tab_products, project_contract_group_products, project_contract_products, project_contract_tab_products, project_quotation_group_products, project_quotation_tab_products, quotation_products, root_contract_products, service_contract_item_products, service_quotation_item_products · cột `product_videos` (text, LIKE): contract_products, project_contract_products, quotation_products, root_contract_products.
- KHÔNG quét cột `attachment(s)` của chứng từ (tệp riêng của chứng từ, thư mục khác).

**Chạy:** `ProductLifecycleService::destroy()` = `$urls = DB::transaction(fn …)` rồi **gọi tường minh** `$this->janitor->purge($urls)` sau khi `DB::transaction` trả về (KHÔNG `DB::afterCommit` — không chạy trong PHPUnit, phát hiện 4). Janitor: công tắc `config('masterdata.product_s3_purge')` false ⇒ `Log::info('ProductFileJanitor: bỏ qua (tắt công tắc)', keys)` + return; mọi lỗi (DB lúc kiểm, S3 lúc xoá) bắt trong janitor ⇒ `Log::warning` từng khoá, KHÔNG ném ra ⇒ response vẫn 200. Lấy helper bằng `app(CmcS3Helper::class)` (mock được). Gỡ (release) KHÔNG gọi janitor.

---

## 3. Task BE (PHA 1)

> Mọi task: viết test trước (đỏ đúng lý do) → code → xanh. `ProductLifecycleApiTest` dùng `DatabaseTransactions` + `ActsAsProductUser`; `setUp` bind mock strict `CmcS3Helper` ghi lại mọi `deleteByUrl` (`$this->s3Calls`) và `config(['masterdata.product_s3_purge' => true])`; fixture công ty A (chủ) / B (lấy về) / C (chưa dùng) như `ProductTakeApiTest`. Hàng thử tạo qua `POST /products` (2-C1) hoặc chèn tay.

### Task B1: Luật cờ ở entity + resource (V1, V3, V4)

**Files:** `Entities/Product/ProductCompany.php` (hằng `LOCKED_MESSAGE`, `isLocked`) · `Entities/Product/Product.php` (cạnh `editableAt` :423) · `Transformers/Product/ProductListResource.php` · `ProductDetailResource.php` · `Services/Product/ProductService.php` (`show()` + `others_using_count`).

- [ ] Test `co_xoa_khoa_mo_khoa_theo_trang_thai`: hàng A dòng chủ 1 ⇒ list `entering`/`company` + chi tiết: `can_delete true, delete_mode 'destroy', can_lock false, can_unlock false`; đổi dòng chủ 3 ⇒ `can_delete false, can_lock true`; 4 ⇒ `can_unlock true, can_edit false`; hàng ERP cũ không dòng (suy ra 3) ⇒ `can_lock true, can_delete false`.
- [ ] Test `can_delete_tat_khi_cong_ty_khac_da_lay_ve`: chèn dòng B `status 1` ⇒ A `can_delete false` ở list VÀ chi tiết (chi tiết dùng `others_using_count`); B thấy `can_delete true, delete_mode 'release'`.
- [ ] Test quyền: A không 1652 (chỉ 1653) ⇒ 3 cờ false; 1652 chỉ ở công ty khác ⇒ false; C (chưa dùng) ⇒ false; `products.status 0` ⇒ false.
- [ ] Code hàm entity (1.4) + 4 khoá resource. Đếm query `/company?per_page=100` không tăng (so trước/sau, ghi checkpoint).

### Task B2: 403 → 423 khi hàng đang khoá + sửa test cũ (V1)

**Files:** `Services/Product/ProductWriteService.php:114, :134` · `Tests/Feature/ProductWriteApiTest.php:403-404` · `Tests/Feature/ProductTakeApiTest.php:452-453, :644-645`.

- [ ] Sửa 3 ca test cũ trước (assert **423** + `message` = `LOCKED_MESSAGE`) ⇒ đỏ.
- [ ] Đổi 2 `abort` ⇒ xanh. Kiểm thứ tự: hàng status 4 + payload sai rule ⇒ vẫn 423 (không 422); hàng status 0 + status 4 ⇒ 403 (D2 trước).

### Task B3: `ProductUsageGuard` (V2, V6, ERP 4 đk)

**Files:** tạo `Services/Product/ProductUsageGuard.php`.

- [ ] Hằng `FK_COLUMNS` (149, mục 2.2), `CHILD_FK_COLUMNS` (19), `REVERSE_FK_COLUMNS` (4), `NO_FK_COLUMNS` (49, mục 2.3). Hàm `reason(int $productId): ?string` theo thứ tự h → i → j.
- [ ] Test `danh_sach_fk_khop_information_schema`: tập `FK ∪ CHILD ∪ REVERSE` = tập `KEY_COLUMN_USAGE … REFERENCED_TABLE_NAME = 'products'` của DB đang chạy (chênh ⇒ fail kèm tên cột).
- [ ] Test `bang_khong_fk_con_ton_tai`: mọi bảng `NO_FK_COLUMNS` có trong `SHOW TABLES` (thiếu ⇒ fail nêu tên; guard runtime vẫn bỏ qua).
- [ ] Test từng lý do (chèn tay 1 dòng rồi gọi guard): `stocks.accounting_qty 1` · mượn chưa trả · `product_has_accessories.product_id` · `recipe_products.product_id` · install · repair · `productables` App\Product (kèm mã hàng kia trong câu) · `quotation_products` (FK) · `serials` (không FK) ⇒ đúng câu; hàng sạch ⇒ null.

### Task B4: `DELETE` nhánh chủ — xoá cứng 20 bước

**Files:** tạo `Services/Product/ProductLifecycleService.php`, `Http/Controllers/V1/Product/ProductLifecycleController.php` · sửa `Routes/api.php` (route `DELETE /{product}`).

- [ ] Test `chu_xoa_cung_sach_20_bang`: A tạo hàng đủ dữ liệu (2 ĐVT ⇒ 12 dòng giá, thuộc tính, phụ kiện 3 loại, công thức, tài liệu kỹ thuật + `files`, 2 ảnh, 1 video, xe 3 loại + đời xe, nhóm máy, NCC, catalog, chèn tay 1 `product_expected_prices` + 1 `product_histories`) ⇒ `DELETE` 200 `mode deleted`; đếm **0 dòng** ở cả 20 bước cho `product_id` (đếm từng bảng); snapshot số dòng `productables` / `product_unit_prices` của hàng khác không đổi.
- [ ] Test chặn 403/404/423/422 theo bảng 1.1: không 1652 · 1652 chỉ ở công ty khác (R22) · id lạ 404 · xoá lần 2 ⇒ 404 · status 0 ⇒ 403 · dòng chủ 4 ⇒ 423 · hàng ERP cũ suy ra 3 ⇒ 422 · dòng chủ 3 ⇒ 422 · công ty B đã lấy về ⇒ 422 nêu tên B · guard (1 ca FK + 1 ca không FK + 1 ca V6) ⇒ 422; mọi ca: `products` + bảng con **không đổi** (snapshot).
- [ ] Test `fk_1451_rollback`: giả lập guard bỏ sót (mock `ProductUsageGuard::reason` trả null) + chèn 1 dòng FK chứng từ ⇒ 422 câu j, mọi bảng con còn nguyên (rollback), `deleteByUrl` **0 lần**.
- [ ] Code `hardDelete` (comment R3 ở bước 13), bắt `QueryException` errno 1451.

### Task B5: `DELETE` nhánh công ty lấy về — gỡ (V4, V5)

- [ ] Test `gỡ_dong_hrm`: B lấy về (INSERT `created_by`) + khai Quản trị (4 ô, NCC, catalog) ⇒ `DELETE` 200 `mode released`; dòng B **không còn**, NCC + catalog B = 0; `products`, dòng/NCC/catalog A giống hệt (snapshot); `deleteByUrl` 0 lần; `/warehouse?usage=unused` của B có lại mã.
- [ ] Test `gỡ_dong_erp_giu_he_so`: dòng B `created_by NULL`, `coefficient 1.03` ⇒ lấy về ⇒ khai 4 ô ⇒ gỡ ⇒ dòng còn, `status NULL`, 4 ô NULL, `coefficient 1.03`; lấy về lại được (L1).
- [ ] Test chặn: B dòng 3 ⇒ 422; 4 ⇒ 423; C chưa dùng ⇒ 403; B không 1652 ⇒ 403.

### Task B6: `ProductFileJanitor` — xoá S3 sau commit (V9)

**Files:** tạo `Services/Product/ProductFileJanitor.php` · sửa `Config/config.php` (`'product_s3_purge' => env('PRODUCT_S3_PURGE', false)`), `.env.example`.

- [ ] Test `xoa_ca_3_ban_anh_va_tai_lieu`: hàng có avatar = ảnh 1 (path-style `…/tanphat/erp_products/a-1-X.jpg`), gallery ảnh 2 (virtual-host), tài liệu `…/products/d.pdf` ⇒ xoá ⇒ `s3Calls` đúng tập: `erp_products/a-1-X{,-thumbnail,-large}.jpg`, `erp_products/<ảnh 2>{,-thumbnail,-large}`, `products/d.pdf` (prefix đúng từng loại), URL đều dạng virtual-host.
- [ ] Test `giu_tep_con_dung`: hàng khác cùng avatar (Sao chép kiểu ERP) · 1 dòng `firm_quotation_tab_products.avatar` = bản `-thumbnail` của ảnh 2 · `files` của bảng khác trỏ cùng tài liệu ⇒ 3 nhóm đó **không** có trong `s3Calls`; nhóm còn lại vẫn xoá.
- [ ] Test `bo_qua_url_khong_phai_s3`: `/uploads/products/x.jpg`, `images/noimage.png`, link YouTube, khoá `tanphat_hrm/tmp/…` ⇒ 0 lời gọi.
- [ ] Test `loi_s3_khong_hong_xoa_db`: mock `deleteByUrl` ném `S3Exception` ở khoá đầu ⇒ response **200**, DB đã xoá, các khoá sau vẫn được gọi, `Log::warning` 1 lần (`Log::spy()`).
- [ ] Test `cong_tac_tat`: `config(false)` ⇒ 0 lời gọi `deleteByUrl`, `Log::info` "bỏ qua".
- [ ] Test `rollback_khong_xoa_tep`: guard 1451 (B4) ⇒ 0 lời gọi (janitor chỉ chạy khi transaction trả về).
- [ ] Đo thời gian bước kiểm "còn ai dùng" với 10 ảnh trên DB local (ghi checkpoint; > 15 s ⇒ báo lead trước khi tiếp).

### Task B7: `PUT lock` / `PUT unlock` (V1)

**Files:** `ProductLifecycleService` (`lock`, `unlock`) · controller · `Routes/api.php` (2 route).

- [ ] Test `khoa_mo_khoa_dong_that`: A dòng 3 ⇒ lock 200 ⇒ 4, `coefficient` không đổi, `updated_by` = người bấm ⇒ unlock ⇒ 3.
- [ ] Test `khoa_hang_cu_chua_co_dong`: user `current_company_role ≠ info->company_id` ⇒ INSERT `company_id = current_company_role`, coef 1, status 4, `created_by`; unlock ⇒ dòng còn, status 3 (không xoá — tiền đề #8).
- [ ] Test `khoa_hang_co_dong_erp_status_null`: UPDATE 4, giữ `coefficient 1.03`, `created_by` vẫn NULL.
- [ ] Test chặn: lock 1/2 ⇒ 422 · lock 4 ⇒ 423 · unlock 3 ⇒ 422 · C ⇒ 403 · không 1652 / 1652 công ty khác ⇒ 403 · status 0 ⇒ 403 · id lạ 404; DB không đổi.
- [ ] Test `sau_khoa`: `/trading` không có, `/company` có badge `Ngừng kinh doanh` `#DC2626`, `/entering` không có; `PUT /{id}`, `PUT admin-data`, `GET /edit` ⇒ **423**; DELETE ⇒ 423; B `take` ⇒ skipped `owner_not_trading`; `catalogs/sync` thêm ⇒ 422, gỡ ⇒ 200; `trading_company_names` không có A.

### Task B8: Thứ tự route + hồi quy

- [ ] Đọc `app('router')->getRoutes()` (không `route:list` — nổ ngoài luồng): 3 route mới đứng trước `GET /{product}`, `DELETE /{product}` không đè `DELETE` nào khác.
- [ ] Chạy `ProductLifecycleApiTest` + hồi quy `ProductWriteApiTest`, `ProductTakeApiTest`, `ProductReadApiTest`, `ProductCatalogApiTest`, `ProductCompanyFoundationTest`, `ProductFormOptionsTest`, `BusinessCatalogTreeTest`, `ProductClassificationCatalogTest`, `ProductCodeGeneratorTest`, `ProductImageUploadTest`, `ProductNatureAutoPartsTest`, `ProductCatalogBaseTest` — ghi số ca vào Checkpoint.
- [ ] Kiểm DB sạch sau test: `product_company_coefficients` 1.105 dòng / 0 `status` NOT NULL; `grep -n "deleteByUrl" storage/logs/laravel-*.log` không có dòng mới (không gọi S3 thật).

### Task B9: Review BE

- [ ] `superpowers:requesting-code-review` cho diff BE; soát: không `DB::afterCommit`, không `new CmcS3Helper()`, không kẹp type ở bước 13, mọi `abort` 423 dùng 1 hằng, không N+1 ở list.

---

## 4. Task FE (PHA 2)

### 4.1 Tự chốt UI (từ `c4-khao-sat-fe.md` §4 T1–T9, chỉnh theo V1–V9)

| # | Chốt |
|---|---|
| T1 | `rowActionsOf` màn ≠ Kho: `[edit (can_edit), delete (danger, ri-delete-bin-line, can_delete), lock (ri-lock-line, can_lock) \| unlock (ri-lock-unlock-line, can_unlock)]`; Khóa/Mở khóa **không** `danger`; mọi `visible` AND `hasAPermission('Xây dựng thông tin hàng hoá')`. Kho dữ liệu giữ chỉ *Lấy về* |
| T2 | `trading`: cờ màn `lifecycle: true` ⇒ cột Hành động chỉ khi có 1652 (như Kho 2-C2); action duy nhất thực tế là Khóa |
| T3 | `$confirm` (hỏi TRƯỚC lớp tải): Xóa `destroy` *Xác nhận xóa* "Xóa hàng hoá <mã>? Hàng hoá, toàn bộ dữ liệu đi kèm và ảnh/tài liệu đã tải lên bị xóa hẳn, không khôi phục được." `textAccept 'Xóa'` `danger` · Xóa `release` "Gỡ hàng hoá <mã> khỏi <công ty>? Dữ liệu quản trị, nhà cung cấp và catalog của <công ty> bị xóa; hàng hoá vẫn còn ở công ty tạo." `textAccept 'Xóa'` `danger` · Khóa *Xác nhận khóa* "Khóa hàng hoá <mã> tại <công ty>? Hàng chuyển sang Ngừng kinh doanh, không sửa được tới khi mở khóa." `textAccept 'Khóa'` · Mở khóa *Xác nhận mở khóa* "Mở khóa hàng hoá <mã> tại <công ty>? Hàng trở lại Đang kinh doanh." `textAccept 'Mở khóa'` |
| T4 | Footer chi tiết: `menu.delete = !!product.can_delete` (nút có sẵn V2Footer) + `#custom-actions`: Khóa `primary status="warning"` `ri-lock-line` (`can_lock`), Mở khóa `primary status="success"` `ri-lock-unlock-line` (`can_unlock`) — cùng cờ BE với dòng |
| T5 | Sau khi làm: danh sách ⇒ toast, `$delete(listSelected, id)`, `loadData()` · Xóa ở chi tiết ⇒ toast + `$router.push(backUrl)` · Khóa/Mở khóa ở chi tiết ⇒ toast + tải lại `GET products/{id}` tại chỗ |
| T6 | Toast: `Đã xóa hàng hoá <mã>` · `Đã gỡ hàng hoá <mã> khỏi <công ty>` · `Đã khóa hàng hoá <mã> — trạng thái Ngừng kinh doanh` · `Đã mở khóa hàng hoá <mã> — trạng thái Đang kinh doanh`; 422/423 ⇒ toast nguyên văn `message` BE; 404 ⇒ "Dữ liệu đã thay đổi, vui lòng tải lại" + `loadData()`; 403 không toast (interceptor đã toast) |
| T7 | Không hàng loạt (V7) |
| T8 | Ô lọc Trạng thái màn công ty: hằng MỚI `PRODUCT_COMPANY_SCREEN_STATUS_OPTIONS` (1·2·3·4), KHÔNG sửa `PRODUCT_COMPANY_STATUS_OPTIONS` (popup catalog dùng chung) |
| T9 | Chữ nút *Xóa / Khóa / Mở khóa*; badge giữ *Ngừng kinh doanh* (BE) |
| T10 (mới) | `edit.vue` `onLoadError` 423 ⇒ toast `message` BE + `router.replace` sang chi tiết `/master-data/products/<id>?from=<backUrl>` (thấy badge + nút Mở khóa); Lưu nhận 423 ⇒ `ProductForm` đã toast `message` BE (giữ) |

### Task F1: Cấu hình màn + hằng lọc (T2, T8)

**Files:** `utils/product-list-screens.js`.
- [ ] `trading.lifecycle = true`; hằng `PRODUCT_COMPANY_SCREEN_STATUS_OPTIONS`; docblock nêu lối ghi 2-C4.

### Task F2: Action dòng + `utils/productLifecycle.js` (T1, T3, T5, T6)

**Files:** tạo `utils/productLifecycle.js` (`confirmAndRun(vm, kind, product, companyName)` trả `{ ok, data }`) · sửa `components/product/ProductListPage.vue` (`hasActionsColumn` :701 thêm nhánh `lifecycle`, `rowActionsOf` :790, `onRowAction` :799, ô lọc :583 dùng hằng mới).
- [ ] Gọi `apiDeleteMethod`/`apiPutMethod` (kiểm tên action store có sẵn khi làm), `$safeLoadingStart/Finish`; khuôn `takeBack` 2-C2.

### Task F3: Footer chi tiết + 423 ở form sửa (T4, T5, T10)

**Files:** `pages/master-data/products/_id/index.vue` (:41-45 + docblock :2-5) · `pages/master-data/products/_id/edit.vue` (`onLoadError`).

### Task F4: Kiểm tổng bằng Playwright MCP (bắt buộc trước khi báo xong)

Server worktree: api `php artisan serve` cổng mới (vd 8041) + Nuxt cổng mới (vd 3041) node 12 heap 8192; viewport 1280×800; tài khoản `e2e_assign` (Cty 1, có 1652); fixture tạo bằng API (không tệp — mục 0). Kill đúng PID theo cổng khi xong.

### 4.3 Bảng đo DOM (Playwright MCP — số lấy từ DOM / request, không nhìn ảnh)

| # | Ca | Đo |
|---|---|---|
| D1 | Nhập thông tin: hàng thử `can_delete` | số icon Xóa = số dòng API `can_delete true`; icon Xóa `getComputedStyle(color)` = đỏ danger (đo đúng giá trị thật); thứ tự icon Sửa → Xóa |
| D2 | Xóa ⇒ Hủy | popup `.modal.show` đúng tiêu đề + câu (có mã, "xóa hẳn"), nút [Xóa, Hủy], nút Xóa nền đỏ; Hủy ⇒ 0 modal, **0** request DELETE |
| D3 | Xóa ⇒ Đồng ý | đúng **1** `DELETE …/products/<id>` 200 `mode deleted`; toast đúng chữ; dòng biến mất; `meta.total` giảm 1; SQL: 0 dòng `products` id đó |
| D4 | Chặn 422 | hàng thử chèn tạm 1 dòng `serials` (không FK) ⇒ bấm Xóa ⇒ 1 DELETE 422, toast "Hàng hoá đã phát sinh chứng từ, không xoá được.", dòng còn; xoá dòng `serials` tạm |
| D5 | Gỡ (công ty lấy về) | mã Cty 4 vừa lấy về: popup câu "Gỡ … khỏi <công ty>"; 1 DELETE 200 `mode released`; toast "Đã gỡ …"; mã quay lại Kho `?usage=unused` |
| D6 | Khóa ở *Đang kinh doanh* | cột "Hành động" có (th nowrap, 1 dòng); icon Khóa; Đồng ý ⇒ đúng 1 request **`…/lock`** (chốt bằng ĐƯỜNG được gọi — memory *danh-muc-bang-erp-khoa-bang-0*); dòng biến mất; `meta.total` giảm 1 |
| D7 | *Dữ liệu công ty* lọc *Ngừng kinh doanh* | ô lọc có 4 lựa chọn; có dòng vừa khoá, badge `rgb(220, 38, 38)` nền `rgba(220,38,38,.1)`; **0** icon Sửa/Xóa/Khóa, 1 icon Mở khóa |
| D8 | Chi tiết hàng status 4 | footer = `['Mở khóa', 'Quay lại']`, Mở khóa nền xanh lá (`getComputedStyle`); bấm ⇒ đúng 1 request **`…/unlock`**; tại chỗ: badge *Đang kinh doanh*, footer có Sửa + Khóa, URL không đổi |
| D9 | Chi tiết hàng `can_delete` | footer có *Xóa* (danger); Xóa ⇒ URL về đúng `from` |
| D10 | Khớp dòng = chi tiết | cùng 1 hàng ở trạng thái 1, 3, 4: tập action menu dòng = tập nút footer (trừ Quay lại) |
| D11 | 423 ở form sửa | mở thẳng `/products/<id>/edit` của hàng đang khoá ⇒ toast message BE, URL về chi tiết; 0 form trắng |
| D12 | Ô lọc popup catalog không đổi | popup Xây dựng catalog tab Thêm vẫn 3 lựa chọn, tab trong tiểu mục 4 (hằng cũ không bị sửa) |
| N1 | **Không quyền 1652** (role tạm chỉ 1653) | *Dữ liệu công ty* + chi tiết: 0 icon Xóa/Khóa/Mở khóa, footer chỉ *Quay lại*; *Đang kinh doanh* 0 th "Hành động"; API trực tiếp `DELETE`/`lock`/`unlock` ⇒ 403, DB không đổi; console không lỗi JS |
| S1 | S3 | SQL trước khi xoá: hàng thử `avatar` NULL, 0 dòng `product_galleries`/`product_videos`/`files`; sau: log janitor chỉ "bỏ qua"/"không có tệp", 0 dòng `deleteByUrl` |

---

## 5. e2e (PHA 3)

### Task E1: Sửa spec hiện có

- [ ] `products-form-ui.spec.ts` E4 `:427`: hàng vừa tạo `can_delete` ⇒ `['Sửa', 'Xóa', 'Quay lại']` (đọc cờ API rồi so, không gán cứng).
- [ ] `products-form-ui.spec.ts` E12b `:521-530`: bỏ `test.skip` :525 (BE đã tắt `can_edit`); thêm đo menu dòng màn *Dữ liệu công ty* ẩn Sửa + có Mở khóa; footer = `['Mở khóa', 'Quay lại']`.
- [ ] `products-read-ui.spec.ts` `SCREENS.trading` `:27-28` thêm `'Hành động'` (tài khoản admin có 1652); docblock :5-16; ca footer :113-155 chốt "footer = cờ BE" (Xóa/Khóa/Mở khóa theo `can_*`). `WRITE_BUTTONS` giữ (icon dòng không phải nút chữ).
- [ ] Rà `products-take-ui.spec.ts`, `products-catalog-popup-ui.spec.ts`: không đổi (Kho giữ action, hằng popup không sửa) — ghi lý do vào checkpoint.

### Task E2: Spec mới (viết sẵn, `--list` OK; chạy khi user yêu cầu `--project=<api|chromium> --no-deps --workers=1`, truyền `API_BASE`, `BASE_URL`, **`API_REPO=<worktree>/hrm-api`**)

`tests/master-data/products-lifecycle.api.spec.ts` (serial; `beforeAll` tạo hàng thử bằng `POST products` không tệp + ghi id; `afterAll` DELETE theo id mọi thứ còn sót + gỡ role tạm + `flushApiPermissionCache()`):

| # | Ca |
|---|---|
| A1 | chủ xoá hàng thử ⇒ 200 `deleted`; `runMysql` đếm 0 dòng ở 20 bảng; `productables` loại khác của hàng khác không đổi |
| A2 | gỡ: lấy về 1 mã Cty 4 ⇒ DELETE ⇒ 200 `released`; dòng Cty 1 không còn; `products` + dòng Cty 4 giống hệt (so từng cột) |
| A3 | chặn: hàng thử + 1 dòng `serials` tạm ⇒ 422 câu j · khoá rồi xoá ⇒ 423 · hàng ERP cũ (suy ra 3) ⇒ 422 · status 0 ⇒ 403; DB không đổi |
| A4 | khoá hàng ERP cũ Cty 1 chưa có dòng ⇒ 200, SQL: 1 dòng coef 1 status 4; khoá lại ⇒ 423; mở khoá ⇒ 3; mở khoá lần 2 ⇒ 422; `afterAll` DELETE dòng đó theo id |
| A5 | sau khoá: `PUT /{id}`, `PUT admin-data`, `GET /edit` ⇒ **423**; list `company` `can_unlock true`, `can_edit false`; `trading` không có |
| A6 | **không quyền**: `e2e_cmd_noperm` + role tạm **chỉ 1653** (`E2E C4 tạm - chỉ xem hàng công ty`) + `cache:clear` ⇒ `GET company` 200 nhưng DELETE / lock / unlock 403; list 3 cờ false; DB không đổi |

`tests/master-data/products-lifecycle-ui.spec.ts` (serial): ca **D1–D3, D5–D11, N1** (+ khuôn: th "Hành động" nowrap ở `trading`, icon không vỡ hàng — memory *e2e-ui-phai-kiem-khuon-giao-dien*). Nút V2BaseButton chọn theo `hasText` chuẩn hoá khoảng trắng; `waitForResponse` theo **đường** `/lock` vs `/unlock`; KHÔNG `networkidle`; ô tick (nếu có) bấm toạ độ input.

- [ ] Đối chứng ca không quyền: cài tạm 1652 vào role tạm ⇒ A6 + N1 phải ĐỎ; bỏ lỗi ⇒ xanh (ghi checkpoint).
- [ ] `npx playwright test products-lifecycle --list` (Node 20) OK; chép 2 file mới + 2 file sửa về `HRM/e2e/tests/master-data/`.
- [ ] ⚠️ Bộ `serial`: đọc dòng tổng kết, "did not run" ≠ passed.

---

## 6. Rủi ro + việc ngoài luồng

### 6.1 Rủi ro đợt này

| # | Rủi ro | Né / test |
|---|---|---|
| R1 | **Xoá nhầm tệp S3 production** — `CmcS3Helper` hard-code credentials thật, DB local chứa URL thật của bucket `tanphat` | mock strict mọi PHPUnit; công tắc `PRODUCT_S3_PURGE` mặc định false; fixture e2e/MCP không tệp; khoá ngoài 2 prefix không xoá; tệp còn ai dùng thì giữ cả nhóm |
| R2 | `keyFromUrl` không hiểu path-style ⇒ janitor "xoá" mà không xoá gì, im lặng | janitor tự đổi path-style → virtual-host; test B6 assert khoá nhận được ở cả 2 kiểu |
| R3 | `DB::afterCommit` không chạy trong PHPUnit ⇒ test xanh mà tính năng chết (hoặc ngược lại) | gọi janitor tường minh sau `DB::transaction`; test rollback ⇒ 0 lời gọi |
| R4 | FK 172 cột không phủ 139 cột không FK ⇒ dòng mồ côi im lặng (vd `serials`) | guard 49 bảng + test `serials`; bảng mới không FK sau này ⇒ N20 |
| R5 | Guard chậm (2–9 s) + janitor kiểm 20 cột không index (~4–6 s) ⇒ 1 lượt xoá có thể ~15 s | chỉ từng dòng (V7), có lớp tải; đo ở B6 và D3, > 15 s báo lead |
| R6 | Xoá cứng **giải phóng `code`** (UNIQUE) ⇒ `ProductCodeGenerator` cấp lại mã cho hàng khác | chỉ xoá được khi chưa phát sinh chứng từ (j) ⇒ không chứng từ nào giữ mã; chấp nhận, ghi chú |
| R7 | Xoá `productables` mọi type — reviewer dễ "sửa" thành kẹp type | comment + test đếm 5 loại về 0 |
| R8 | Đổi 403 → 423 làm đỏ ca test cũ / FE nào bắt riêng 403 | B2 sửa 3 ca; FE `edit.vue` T10; `saveErrorMessage` đã có nhánh 423 |
| R9 | Lịch sử khoá/mở khoá (CLAUDE.md HRM :66) vs §14b hoãn lịch sử hàng hoá | theo §14b — ghi `updated_by/updated_at`; lịch sử làm cùng §14b |
| R10 | Khoá hàng cũ chưa có dòng ⇒ sinh dòng coef 1 ⇒ popup ERP của công ty tạo làm tròn nghìn kể cả sau mở khoá (Cty 1 tối đa 8.229 mã) | V1 + tiền đề #8 chấp nhận (tạm) |
| R11 | Đua: 2 người xoá / xoá + khoá cùng lúc | `lockForUpdate` `products` + dòng công ty; test lượt 2 ⇒ 404/423 |
| R12 | Dữ liệu thử MCP/e2e quên dọn (dòng coef 1 status 3 còn lại ⇒ giá ERP local làm tròn) | ghi id trước, DELETE theo id, checkpoint ghi "đã dọn: 0 dòng còn" |
| R13 | ERP (N2/N8) xoá-chèn dòng công ty khi lưu Hãng SX ⇒ hàng đang khoá tự "mở khoá" | đã ghi N2/N8 — 2-D chặn |

### 6.2 Việc ngoài luồng (nối tiếp N17; thêm vào `chot.md` khi user duyệt)

| # | Việc | Nguồn |
|---|---|---|
| N18 | `Product::tradingCompanyNames()` (`Product.php:456-473`) bỏ sót công ty tạo khi dòng chủ là dòng ERP `status NULL` (suy ra 3) ⇒ cột *Công ty đang kinh doanh* thiếu chủ ở 4 hàng Cty 4 (38930, 39426, 39432, 39802). Lỗi 2-B, thuộc luồng hàng hoá | khảo sát BE §5.2 |
| N19 | Popup HRM (Finance: Yêu cầu nhập hàng `ProductImportRequestService.php:1448`, Yêu cầu chuyển kho `ProductTransferRequestService.php:984`, Mượn bán `BorrowSellRequestService.php:457`; CustomerCare `ServiceService.php:990`) đọc `product_company_coefficients` chỉ lấy hệ số, không xét `status` ⇒ hàng Ngừng KD (4) vẫn chọn được ở HRM (N8 mở rộng sang HRM) | khảo sát BE §5.1 |
| N20 | 139 cột `product_id` không FK, 169/183 không index ⇒ mọi kiểm "đã dùng chưa" sau này chậm + dễ sót; cân nhắc index/FK khi dọn DB | khảo sát BE §3.3 |
| N21 | DB local còn 4 quyền cũ 1616–1619 (nhánh `feat/p1`) — dọn khi merge | khảo sát BE §6 |
| N22 (mới) | **Deploy prod phải đặt `PRODUCT_S3_PURGE=true`** (mặc định false để máy dev không xoá S3 thật) — thiếu thì V9 không chạy (chỉ để lại tệp mồ côi, không hỏng dữ liệu) | plan 2-C4 mục 0 |
| N23 (mới) | `CmcS3Helper` hard-code access/secret key CMC trong code (`app/Helper/CmcS3Helper.php:24-25`) ⇒ mọi môi trường (kể cả dev/test) ghi/xoá thẳng bucket production; nên chuyển sang `.env` + bucket riêng cho dev | khảo sát V9 08/10 |
| N24 (mới) | `CmcS3Helper::keyFromUrl` chỉ hiểu URL virtual-host, trong khi 45k avatar hàng hoá ERP là path-style ⇒ mọi chức năng HRM khác dùng `deleteByUrl`/`isTemporaryUrl` trên URL ERP đều âm thầm không chạy | khảo sát V9 08/10 |
| N25 (mới) | 23 `products.avatar` lưu thẳng bản `-thumbnail` (ERP suy thumbnail từ avatar ⇒ ra `…-thumbnail-thumbnail`, ảnh vỡ ở danh sách ERP) | đo 08/10 |

---

## 7. Điểm tự quyết chưa có chốt (đưa user xem khi duyệt plan — đều đổi được không tốn)

| # | Tự quyết | Lý do |
|---|---|---|
| Q-D1 | Công tắc `PRODUCT_S3_PURGE` **mặc định false** (prod phải bật — N22) | DB local chứa URL thật của bucket production + helper hard-code key thật ⇒ máy dev không được tự xoá S3 |
| Q-D2 | Xoá S3 theo **nhóm 3 bản** (gốc/-thumbnail/-large) và giữ cả nhóm nếu bất kỳ bản nào còn được trỏ, quét cả **20 cột avatar chứng từ** | ERP suy thumbnail từ avatar; chứng từ chép avatar sang dòng hàng |
| Q-D3 | Khoá hàng **đang 4** ⇒ **423** (khảo sát BE 5.1 ghi 422, 5.3 ghi 423) | CLAUDE.md HRM: bản ghi đang khoá ⇒ 423; một luật cho mọi thao tác ghi |
| Q-D4 | Gỡ (công ty lấy về) **không** xoá S3 | gỡ không xoá tệp nào của hàng |
| Q-D5 | Câu chặn V6 kèm **≤ 3 mã hàng** đang tham chiếu | người dùng biết gỡ ở đâu |
| Q-D6 | Câu chặn g nêu **tên công ty** đã lấy về | §35b-4 chặn nhưng không nói báo gì |
| Q-D7 | Response DELETE `mode: 'deleted' \| 'released'`; cờ resource `delete_mode: 'destroy' \| 'release'` | FE chọn câu hỏi trước khi bấm + toast sau khi bấm |
| Q-D8 | Controller riêng `ProductLifecycleController` (không nhồi vào `ProductWriteController`) | giữ file 2-C1/2-C2 gọn; 1 controller cho 3 route vòng đời |
| Q-D9 | **Không** sửa N18 trong đợt này | khảo sát ghi "nếu user cho" — để user quyết khi duyệt plan |
| Q-D10 | Mở thẳng `/edit` hàng đang khoá ⇒ toast + chuyển sang chi tiết (không đưa về 404) | 423 khác 403: người dùng có quyền, chỉ cần mở khoá |
| Q-D11 | Mở khoá **không** xoá dòng coef 1 đã sinh lúc khoá | V1 không nói; xoá thì mất 4 ô quản trị đã khai giữa chừng (tiền đề #8: hệ số sẽ bỏ) |
| Q-D12 | Bảng không FK đã đổi tên/xoá ⇒ guard bỏ qua lúc chạy (không 500), test báo đỏ | không để 1 bảng ERP đổi tên làm chết nút Xóa |

---

## 8. Checkpoint

<!-- Điền khi làm: ngày · vừa xong · đang dở · bước tiếp · blocked. Ghi số ca PHPUnit/e2e (đọc dòng tổng kết), id dữ liệu đã ghi + đã dọn, số lời gọi S3 (phải 0 ngoài mock). -->

### 08/10/2026 — PHA 1 BE xong (B1–B5, B7, B8; B6 BỎ theo V9 — không S3)

- Commit `006d0585f` trên `feat/p2c4-vong-doi` (hrm-api worktree), chưa push/merge.
- Tạo: `ProductLifecycleService`, `ProductUsageGuard`, `ProductLifecycleController`, `Tests/Feature/ProductLifecycleApiTest.php` (20 ca). KHÔNG tạo `ProductFileJanitor`, KHÔNG sửa `Config/config.php`/`.env.example`, không gọi `CmcS3Helper` (test bind mock strict không kỳ vọng hàm nào ⇒ 0 lời gọi).
- Sửa: `Product.php` (`othersUsingAt`, `deletableAt`, `deleteModeAt`, `lockableAt`, `unlockableAt`), `ProductCompany.php` (`LOCKED_MESSAGE`, `ALREADY_LOCKED_MESSAGE`, `isLocked`), `ProductWriteService` 403 → 423 (:114, :134), `ProductService::show()` (`others_using_count`), 2 resource, `Routes/api.php` (3 route trước `GET /{product}`); test cũ: `ProductWriteApiTest` (ca status 4 ⇒ 423 + payload rỗng vẫn 423 + status 0 ⇒ 403), `ProductTakeApiTest` 2 ca ⇒ 423.
- PHPUnit (đọc dòng tổng kết): Lifecycle 20/20 · Write 34/34 · Take 26/26 · Read 8/8 · Catalog 6/6 · Foundation 5/5 · FormOptions 4/4 · BusinessCatalogTree 12/12 · Classification 11/11 · CodeGen 9/9 · ImageUpload 4/4 · NatureAutoParts 2/2 · CatalogBase 6/6 ⇒ **147/147 xanh**.
- Query `/company?per_page=100`: 11 query trước = 11 sau, không đổi theo số dòng (ca `danh_sach_khong_tang_query_theo_so_dong`).
- Guard đo local: 49 bảng không FK ≈ 3,5 s, 149 FK ≈ 0,8 s / lượt xoá. Cả lượt test 20 ca ≈ 20 s.
- DB sau test: `product_company_coefficients` 1.105 dòng / 0 `status` NOT NULL; 0 hàng fixture còn sót; log 0 dòng `deleteByUrl`.
- Lệch nhỏ tự quyết: câu ERP h3/h4 (phụ kiện, công thức) cũng kèm ≤ 3 mã như i (theo mục 2.4), vd "Hàng nằm trong danh sách phụ kiện! (TP-1)". 404 trả `Item Not Found!` (findOrFail như các route khác).
- Phát hiện (ngoài luồng, đề xuất N26): DB local có **59.710 `product_histories` mồ côi** trỏ `product_version_id` > AUTO_INCREMENT `product_versions` ⇒ hàng sinh `product_versions` mới có thể trùng id ⇒ xoá cứng vướng FK 1451 ⇒ 422 "đã phát sinh chứng từ" (chốt cuối đúng, câu báo lệch). Ngoài ra `product_price_histories.product_version_id` FK → `product_versions` cũng chỉ bắt được ở 1451.
- Bước tiếp: PHA 2 FE (F1–F4) — xin "làm" riêng.

### 08/10/2026 — F4 kiểm trên app thật + chạy e2e (user cho "MCP + chạy e2e")

api 8031 (hrm-api `006d0585f`) + Nuxt 3031 (hrm-client `9ca80b35a`), viewport 1280×800, tài khoản `e2e_assign` (Cty 1, có 1652). Playwright MCP chết giữa chừng ("Connection closed" trước khi bấm Xóa — DB xác nhận chưa ghi) ⇒ đo tiếp bằng script Playwright (chromium thật, cùng bộ đo DOM/request). **Không lỗi app ⇒ không commit.** S1 bỏ (V9). D4 không đo ở MCP (dòng `serials` tạm nằm ngoài phạm vi ghi của MCP) — A3 spec API phủ.

| # | Số đo DOM / request | KQ |
|---|---|---|
| D1 | `/entering` 4 dòng API `can_delete true` = 4 icon Xóa; mọi dòng `['Sửa','Xóa']`; icon Xóa `color rgb(220, 38, 38)` | ĐẠT |
| D2 | popup "Xác nhận xóa": "Xóa hàng hoá BT3D--T4DT135H? Hàng hoá và toàn bộ dữ liệu đi kèm bị xóa hẳn…", nút [×, Xóa, Hủy], Xóa nền `rgb(220, 38, 38)`; Hủy ⇒ 0 `.modal.show`, **0** request ghi | ĐẠT |
| D3 | đúng 1 `DELETE …/51151` 200 `mode deleted` (4,7 s, guard); toast "Đã xóa hàng hoá BT3D--T4DT135H"; `meta.total` 4 → 3; dòng 0; SQL 0 dòng `products`/coef/ĐVT/catalog/thuộc tính | ĐẠT |
| D5 | lấy về 50061 (Cty 4) ⇒ dòng coef 4795; `/entering` cờ `release`; popup "Gỡ hàng hoá SG-VT-NM0102 khỏi CÔNG TY CỔ PHẦN… Dữ liệu quản trị…"; 1 DELETE 200 `released` + `company_name`; toast "Đã gỡ …"; dòng 0; Kho `?usage=unused` tìm mã ⇒ `can_take_back true`; SQL: 0 coef/NCC/catalog của mã, dòng `products` `diff` = giống hệt | ĐẠT |
| D6 | `/trading` hàng ERP cũ 50064 (CH-DCT8, chưa có dòng): 14 th đều `nowrap` cao 33px (có "Hành động"); menu `['Sửa','Khóa']`, icon Khóa xám `rgb(75, 85, 99)` (không danger); popup "Khóa hàng hoá CH-DCT8 tại …"; đúng 1 request **`PUT …/50064/lock`** (0 `/unlock`) 200 `company_status 4`; total 1 → 0; dòng 0; SQL sinh dòng id **4794** coef 1 status 4 `created_by 1180` | ĐẠT |
| D7 | `/company`: ô lọc Trạng thái 4 lựa chọn (Đang nhập thông tin · Chờ tính giá bán · Đang kinh doanh · Ngừng kinh doanh); lọc ⇒ request `company_status=4`, total 1, có 50064, mọi dòng = 4; badge `rgb(220, 38, 38)` nền `rgba(220, 38, 38, 0.1)`; menu dòng chỉ `['Mở khóa']` | ĐẠT |
| D8 | chi tiết 50064: cờ `[edit f, delete f, lock f, unlock t]`, footer `['Mở khóa','Quay lại']`, Mở khóa nền `rgb(22, 163, 74)`; bấm ⇒ đúng 1 **`PUT …/unlock`** 200; tại chỗ GET lại, toast "Đã mở khóa … — trạng thái Đang kinh doanh", URL không đổi, footer `['Sửa','Khóa','Quay lại']`, Khóa nền `rgb(217, 119, 6)` (đo trang mới — xem ghi chú transition) | ĐẠT |
| D9 | chi tiết 51152 (`can_delete`, `destroy`): footer `['Sửa','Xóa','Quay lại']`, Xóa nền đỏ; xoá ⇒ 1 DELETE 200 ⇒ URL về đúng `from` `/master-data/products/entering` | ĐẠT |
| D10 | trạng thái 1: dòng `[Sửa, Xóa]` = footer `[Sửa, Xóa]`; 3: `[Sửa, Khóa]` = `[Sửa, Khóa]`; 4: `[Mở khóa]` = `[Mở khóa]` | ĐẠT |
| D11 | `/50064/edit` đang khoá ⇒ GET `/edit` **423** câu BE; URL về `/master-data/products/50064?from=%2Fmaster-data%2Fproducts%2Fcompany`; 1 toast câu BE; 0 form; footer `['Mở khóa','Quay lại']` | ĐẠT |
| N1 | role tạm id **103580** (chỉ 1653) gán `e2e_cmd_noperm` (employee 1184) + `cache:clear`. API: `DELETE`/`lock`/`unlock` (51153 trạng thái 1, 50064 trạng thái 4) ⇒ **403** cả 4, DB không đổi; list cờ false. UI: `/company` 2 hàng 0 icon (menu `[]`), chi tiết footer `['Quay lại']`; `/trading` 200, 0 th "Hành động", 0 icon; 0 response API lỗi, console chỉ 404 ảnh `e2e.png` (có sẵn) | ĐẠT |

**e2e (bản sao `wt-chuyen-doi-hang-hoa/e2e`, Node 20, `--no-deps --workers=1 --retries=0`, truyền `API_BASE/BASE_URL/API_REPO`) — dòng tổng kết lượt cuối:**

| Spec | Kết quả |
|---|---|
| `products-lifecycle.api` (`--project=api`) | **6 passed**, 0 failed / skipped / did-not-run |
| `products-lifecycle-ui` (chromium) | **10 passed**, 0 failed / skipped / did-not-run (lượt 3) |
| `products-form-ui` (chromium) | **17 passed, 1 skipped** (E11b `test.skip` có sẵn — chưa có role chỉ xem danh mục tính chất), 0 failed / did-not-run (lượt 2) |
| `products-read-ui` (chromium) | **8 passed**, 0 failed / skipped / did-not-run |

Lỗi đều ở SPEC (đã sửa, chép về `HRM/e2e/tests/master-data/`):
1. `lifecycle.api` A3 hết giờ 30 s mặc định (7 lượt DELETE × guard ~4 s) ⇒ 3 ca sau "did not run" ⇒ thêm `beforeEach setTimeout(150000)`.
2. `lifecycle-ui` D7: `<select>` Trạng thái có sẵn trong DOM nhưng khối "Tìm kiếm nâng cao" `display:none` ⇒ spec chỉ mở khi `count()=0` nên bấm ô ẩn ⇒ xét `isVisible()` của ô select2 rồi mới bấm `.filter-toggle-btn`.
3. `lifecycle-ui` D8: Khóa đo được `rgb(43, 158, 67)` = đúng ~11 % đường chuyển từ xanh `rgb(22,163,74)` sang cam `rgb(217,119,6)` — Vue dùng lại thẻ `<button>` của Mở khóa, `V2BaseButton` có `transition: background-color .15s` ⇒ đo trang mới ra `rgb(217, 119, 6)` ⇒ không phải lỗi app; spec đổi sang `expect.poll`.
4. `lifecycle-ui` D11 + `form-ui` E12b (+ E4, `read-ui` 2 ca footer cho chắc): đọc footer ngay khi mới có "Quay lại" (chi tiết đang tải — ảnh lỗi là spinner) ⇒ `expect.poll(footerTexts)`.

**Đối chứng ca không quyền (cài lỗi tạm: role tạm thêm 1652, đã bỏ — `grep CAI-LOI-TAM` = 0):** A6 ĐỎ ở cờ list (`[false,false,false]` ⇒ nhận `true`); N1 ĐỎ ở cờ API, tắt thêm assert API ⇒ vẫn ĐỎ ở UI "icon Xóa Expected 0, Received 1". Bỏ lỗi ⇒ xanh trong lượt chạy đủ bộ.

**Dọn (SELECT chứng minh, so chụp trước):** MCP tạo 4 hàng thử 51151–51154 (không tệp: `avatar` NULL, 0 gallery/video/tài liệu) ⇒ xoá cả 4 qua chính tính năng (51151/51152 UI, 51153/51154 `DELETE` API sau N1); dòng coef 4794 (khoá 50064) ⇒ mở khoá rồi `DELETE … WHERE id=4794` ROW_COUNT 1, dòng `products` 50064 `diff` giống hệt; 50061 gỡ qua D5 (coef 4795 đã xoá bởi tính năng); role 103580 xoá 3 bảng + `cache:clear` ⇒ token noperm gọi `company` lại 403. Sau cùng: đếm 25 bảng (products 45.890 · coef **1.105 / 0 status NOT NULL** · `product_suppliers` 1.741 · `product_business_catalogs` 0 · ĐVT/giá/thuộc tính/productables/serials/roles/role_has_permissions/employee_has_roles…) + `CHECKSUM TABLE` 8 bảng (products, coef, suppliers, catalogs, roles, employee_has_roles, role_has_permissions, serials) **giống hệt trước khi chạy**; 0 hàng/fixture `E2EC1S`; role `E2E%tạm%` 0; `e2e_cmd_noperm` chỉ còn role 100126.
- S3: code 2-C4 không gọi `CmcS3Helper`; log `laravel-2026-10-08.log` chỉ 1 dòng `CmcS3Helper` lúc 07:08 (upload ảnh 2-C1, trước phiên này) ⇒ **0 lời gọi S3** trong đợt kiểm.
- Server: kill đúng PID theo cổng (artisan 61955 + php -S 61969, nuxt 61956) ⇒ 8031/3031 không còn LISTEN. Git 2 repo worktree sạch.

**Ghi chú (không sửa):** (1) `/company` với tài khoản không 1652 vẫn hiện cột "Hành động" trống (0 icon) — màn `trading` thì ẩn; thuần UI, đưa lead xem. (2) Toast nhân đôi không có (đo `.toasted-container .toasted` = 1). (3) MCP Playwright cần khởi động lại cho lần sau.
- Bước tiếp: chờ lead/user (review cuối, merge `feat/p2c4-vong-doi` → `feat/chuyen-doi-hang-hoa`; ⛔ không gop_db).

### 08/10/2026 — Sửa cột "Hành động" rỗng khi không có 1652 (user cho "Sửa cột Hành động rỗng trước")

- Commit `2bf90d755` trên `feat/p2c4-vong-doi` (hrm-client worktree), chưa push/merge. Sửa `ProductListPage.vue` `hasActionsColumn`: Kho theo `canTakeBack` (như cũ); màn khác = (`rowActions` || `lifecycle`) AND 1652 — mọi nút dòng (`rowActionsOf`) đều cần 1652 nên không quyền thì không có nút nào ⇒ không dựng cột. Comment `utils/product-list-screens.js` cập nhật.
- Rà 4 màn: `entering` BE gate 1652 (không quyền không vào được) · `warehouse` đã đúng (`canTakeBack`) · `trading` đã đúng (`lifecycle`) · **`company` là màn duy nhất lỗi**.
- Đo (script Playwright chromium, viewport 1280, api 8031 + Nuxt 3031; `e2e_cmd_noperm` + role tạm 103724 chỉ 1653 + `cache:clear`): **trước** `/company` 20 dòng, 1 th "Hành động", 0 nút (warehouse/trading 0 th). **Sau**: `/company` 0 th "Hành động", 0 nút; warehouse/trading vẫn 0. **Hồi quy `e2e_assign` (có 1652)**: company 1 th, 40 nút `[Sửa, Khóa]` · trading 1 th, 40 nút · warehouse 1 th, 2 nút `Lấy về` · entering 1 th (0 dòng dữ liệu).
- Spec: ca N1 `products-lifecycle-ui` thêm assert màn công ty 0 th "Hành động" + 0 `.v2-row-actions`; chép về `HRM/e2e/tests/master-data/`. Kết quả (`--no-deps --workers=1 --retries=0`): `products-lifecycle-ui` **10 passed** · `products-read-ui` **8 passed** — 0 failed/skipped/did-not-run.
- Dọn: role 103724 xoá 3 bảng + `cache:clear` (role của spec tự gỡ ở afterAll). SELECT: role `E2E%tạm%` 0 · `e2e_cmd_noperm` chỉ role 100126 · coef **1.105 / 0 status NOT NULL** · products 45.890 · fixture `E2EC1S`/`C4UI` 0. Server kill đúng PID (artisan 43433 + php -S 43448, nuxt 43434) ⇒ 8031/3031 không còn LISTEN. Git 2 repo worktree sạch.
