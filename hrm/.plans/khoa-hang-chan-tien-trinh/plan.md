# Khóa hàng — chặn khi còn phiếu dở (khoa-hang-chan-tien-trinh) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chặn thao tác "Khóa" một mặt hàng ở DM hàng hóa (HRM) khi mặt hàng còn phiếu dở trong luồng Mua/Nhập/Xuất, và hiện popup liệt kê đúng các phiếu đang giữ (gom theo luồng, mỗi dòng mã phiếu bấm được + người tạo + ngày tạo).

**Architecture:** Thêm guard `ProductInProgressGuard` (hrm-api) được `ProductLifecycleService::lock()` gọi sau các check hiện có, trước `setStatus(STATUS_STOPPED)`. Guard truy vấn bảng phiếu ERP qua connection `mysql` mặc định (ERP & HRM chung DB), lọc theo `product_id` + công ty đang đăng nhập + dòng còn dở + phiếu chưa Hủy/chưa Hoàn thành, trả về cấu trúc gom nhóm; có phần tử → `throw` 422 kèm `blocking_documents`. FE bắt 422 có `blocking_documents` → mở modal thay vì toast.

**Tech Stack:** hrm-api Laravel 8 / PHP 7.4 (query builder thuần, PHPUnit Feature test chạy trên DB dev với `DatabaseTransactions`); hrm-client Nuxt 2.14 / Vue 2 (modal dựng trên `V2BaseModal.vue`).

**Spec:** `HRM/.plans/khoa-hang-chan-tien-trinh/design.md` (thực: `hrm-claude-config/hrm/.plans/khoa-hang-chan-tien-trinh/design.md`) — plan này bám design; executor đọc cả hai.

## Global Constraints

- Làm việc bằng tiếng Việt. KHÔNG commit/push khi chưa có yêu cầu (mỗi task vẫn ghi bước commit để executor chạy khi được phép).
- KHÔNG sửa hàm dùng chung mà chưa hỏi; guard là class MỚI, chỉ thêm 1 lệnh gọi vào `ProductLifecycleService::lock()`.
- Ngữ nghĩa khóa giữ nguyên: set `product_company_coefficients.status = 4` (`ProductCompany::STATUS_STOPPED`) theo công ty đang đăng nhập. Chỉ chặn **Khóa** — KHÔNG đụng Xóa/Mở khóa/Khôi phục.
- "Dở" = tồn tại ≥1 phiếu có **dòng chi tiết của chính `product_id` này** mà phiếu **CHƯA Hủy và CHƯA Hoàn thành** (nháp/Đang tạo coi là dở → chặn). Chặn cả nháp của người khác.
- Phạm vi = **chỉ công ty đang đăng nhập** (`ProductLifecycleService::companyId()` = `current_company_role`). Biểu thức "công ty của phiếu" KHÁC nhau theo bảng — xác định riêng từng bảng, cùng hệ id với `companyId()`.
- Mọi bảng có `deleted_at` phải `whereNull('deleted_at')` (guard dùng query builder thuần, không có global scope soft-delete).
- Hằng trạng thái & cờ hoàn thành trong design mục 5 là recon — builder PHẢI mở từng Model ERP đọc lại `const STATUS_*` / tên cột cờ trước khi hardcode. Quy tắc: block = (∉ tập Hủy) AND (∉ tập Hoàn thành / cờ hoàn thành = 0).
- Cảnh báo tên cột: YCXH = `is_completed`, ĐNXK = `is_complete` (khác nhau); giá trị "Hủy" khác nhau giữa các Model (0/4/5/6).
- Cap mỗi nhóm popup: tối đa **50 phiếu/nhóm**, vượt thì thêm dòng tổng "… và N phiếu khác".
- URL ERP lấy từ config/env ERP base đang dùng (vd `HRM_*`/`ERP_BASE_URL`) — KHÔNG hardcode domain.
- Số hiển thị ngày định dạng theo chuẩn dự án; modal bám skill `modal-popup`, `list-page`, `button-convention`, `notification-convention`; nút không dùng được thì ẩn (không áp cho feature này vì nút Khóa vẫn hiện, chặn xảy ra sau khi bấm).

## Review Focus

- **Chặn sai công ty (Anti-goal #2):** phiếu dở của công ty B làm kẹt khóa hàng cho công ty A — pin ở Task 1–3 (mỗi flow test có case "phiếu công ty khác → KHÔNG xuất hiện").
- **Chặn oan vì phiếu đã Hủy/Hoàn thành (Anti-goal #1):** người dùng không bao giờ khóa được — pin ở Task 1–3 (case cancel + case done → KHÔNG xuất hiện).
- **Chặn oan vì mặt hàng KHÁC trên cùng phiếu:** phải xét theo DÒNG của đúng `product_id` — pin ở Task 1 (case phiếu chỉ chứa dòng sản phẩm khác → KHÔNG xuất hiện).
- **Phiếu xóa mềm vẫn bị đếm:** `whereNull('deleted_at')` — pin ở Task 1 (case dòng/phiếu `deleted_at != null` → KHÔNG xuất hiện).
- **Guard ném lỗi làm hỏng chính thao tác khóa:** bảng ERP thiếu/tên cột sai khiến query vỡ → khóa chết; guard phải "fail-safe về phía chặn có kiểm soát" chứ không 500 vô tri — pin ở Task 5 (case bảng không tồn tại → bỏ qua bảng đó, không fatal; dùng `Schema::hasTable`/`try` như `ProductUsageGuard::tableExists`).

---

### Task 1: Guard scaffold + hạ tầng config + luồng XUẤT

**Files:**
- Create: `hrm-api/Modules/MasterData/Services/Product/ProductInProgressGuard.php`
- Create: `hrm-api/Modules/MasterData/Tests/Feature/ProductInProgressGuardTest.php`

**Interfaces:**
- Consumes: (không) — chỉ query builder thuần trên connection `mysql`; tái dùng khuôn test `Concerns\ActsAsProductUser` + `DatabaseTransactions` (xem `ProductExportApiTest`).
- Produces (các task sau và Task 5 dựa vào):
  - `ProductInProgressGuard::blockingDocuments(int $productId, int $companyId): array` — trả `['purchase'=>Row[], 'import'=>Row[], 'export'=>Row[]]`; tất cả rỗng ⇒ cho khóa.
  - `Row` = `['code'=>string, 'created_by_name'=>string, 'created_at'=>string, 'url'=>string, 'target'=>'hrm'|'erp']`.
  - `ProductInProgressGuard::flowEntries(): array` = danh sách **entry**/bảng (method, KHÔNG dùng class `const` vì `url` là closure — PHP 7.4 const không chứa closure), mỗi entry các khóa: `flow`('purchase'|'import'|'export'), `doc`(slug loại phiếu), `parent`(bảng cha), `detail`(bảng chi tiết hoặc `null` nếu product_id nằm thẳng ở cha), `parent_key`, `detail_fk`, `product_col`, `company_expr`(cột hoặc closure dựng biểu thức công ty theo bảng), `exclude`(mảng status Hủy+Hoàn thành), `completed_flag`(tên cột cờ hoặc `null`), `line_pending`(cột tín hiệu dở theo dòng hoặc `null`), `code_col`, `created_by_col`, `created_at_col`, `soft_delete`(bool), `target`('hrm'|'erp'), `url`(closure `fn(int $id): string`).
  - Helper nội bộ tái dùng: `queryEntry(array $entry, int $productId, int $companyId): Row[]`; `resolveCreatorName(int $employeeId): string`; `capGroup(array $rows): array` (cap 50 + dòng "… và N phiếu khác").

- [ ] **Step 1: Viết test fail cho luồng XUẤT (YCXH + ĐNXK)** trong `ProductInProgressGuardTest.php` (dùng `DatabaseTransactions`, `ActsAsProductUser`, công ty 6 là công ty sạch). Seed tối thiểu từng case rồi assert `blockingDocuments($pid, 6)['export']`:

```php
// YCXH dở: product_export_requests + product_export_request_details, is_completed=0, status ∉ {5,6}, company khớp 6
//   => export có 1 Row, code đúng, target='hrm'
// YCXH is_completed=1            => export rỗng
// YCXH status=6 (Hủy)            => export rỗng
// YCXH công ty khác (export_company_id=1) => export rỗng  [Review Focus: sai công ty]
// YCXH chỉ chứa dòng product_id KHÁC    => export rỗng  [Review Focus: theo DÒNG]
// YCXH detail deleted_at != null (nếu bảng có soft delete) => export rỗng  [Review Focus: soft-delete]
// ĐNXK dở: warehouse_export_requests.is_complete=0, status ∉ done/cancel => export có Row, target theo mục 6
```

- [ ] **Step 2: Chạy test, xác nhận FAIL** — Run: `php artisan test Modules/MasterData/Tests/Feature/ProductInProgressGuardTest.php` — Expected: FAIL ("Class ProductInProgressGuard not found").

- [ ] **Step 3: Xác minh hằng từ Model & dựng entry XUẤT** — mở `ProductExportRequest`, `WarehouseExportRequest` (và Model PXK `ProductExport`, YC bán/mượn) đọc `const STATUS_*` + cột cờ (`is_completed` vs `is_complete`), cột công ty (`export_company_id` cho YCXH; PXK suy từ người tạo `info.company_id`), cột soft-delete. Ghi kết quả xác minh thành comment trong file. Điền entry luồng `export` vào `flowEntries()` (YCXH, ĐNXK, PXK, YC bán/mượn) theo design mục 5 (XUẤT) + mục 6 (URL). PXK/YC bán-mượn: chốt điều kiện "đã xong" rồi ghi vào comment.

- [ ] **Step 4: Implement `blockingDocuments()` + helpers** trong `ProductInProgressGuard.php`:
  - `blockingDocuments(int $productId, int $companyId): array` — gom `queryEntry()` cho mọi entry theo `flow`, mỗi flow `capGroup()`.
  - `queryEntry()`: JOIN cha↔chi tiết theo `parent_key`/`detail_fk` (hoặc query thẳng cha khi `detail=null`), `where product_col = $productId`, điều kiện công ty theo `company_expr` (= `$companyId`), `whereNotIn(status, exclude)`, nếu có `completed_flag` thì `where flag = 0`, nếu có `line_pending` thì lọc dòng còn dở, `whereNull('deleted_at')` khi `soft_delete`. Dùng `ProductUsageGuard::tableExists()`-style guard để bỏ qua bảng không tồn tại. Dựng Row: `code`, `resolveCreatorName(created_by)`, `created_at` format, `url($id)`, `target`.
  - `resolveCreatorName()`: join nhân viên/`users` theo cách service HRM hiện có (dùng lại helper sẵn có; nếu không resolve được → trả chuỗi rỗng, không fatal).

- [ ] **Step 5: Chạy test, xác nhận PASS** — Run: `php artisan test Modules/MasterData/Tests/Feature/ProductInProgressGuardTest.php` — Expected: PASS.

- [ ] **Step 6: Commit** — `git add Modules/MasterData/Services/Product/ProductInProgressGuard.php Modules/MasterData/Tests/Feature/ProductInProgressGuardTest.php && git commit` (feat: guard chặn khóa hàng — luồng xuất).

---

### Task 2: Luồng MUA

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductInProgressGuard.php` (thêm entry `flow='purchase'`)
- Modify: `hrm-api/Modules/MasterData/Tests/Feature/ProductInProgressGuardTest.php`

**Interfaces:**
- Consumes: hạ tầng `flowEntries()` + `queryEntry()` từ Task 1.
- Produces: các entry luồng mua điền vào cùng `blockingDocuments(...)['purchase']`.

- [ ] **Step 1: Viết test fail** cho 5 nhóm phiếu mua (YC đặt hàng gốc `root_order_requests`; đơn đặt hàng `order_requests`/`order_request2`; hóa đơn mua `purchase_invoices`/`inland_purchase_invoices`; HĐ mua `buy_contract2`/`inland_buy_contract_new`; `invoice2`). Mỗi loại ≥2 case: 1 phiếu dở → xuất hiện trong `['purchase']` với `target='erp'`; 1 phiếu Hủy/Hoàn thành → KHÔNG xuất hiện. Riêng HĐ mua thêm case: còn dòng chưa giao đủ (`qty - arrived_qty - arriving_qty > 0`) → chặn; đã giao đủ → không chặn.
- [ ] **Step 2: Chạy test, xác nhận FAIL** — Run: `php artisan test ...ProductInProgressGuardTest.php` — Expected: FAIL (thiếu entry purchase).
- [ ] **Step 3: Xác minh hằng + điều kiện "đã xong" HĐ mua từ Model**, điền entry `purchase` vào `flowEntries()` (exclude set + `line_pending` cho HĐ = biểu thức còn-phải-giao; URL `target='erp'` theo mục 6). Ghi xác minh thành comment.
- [ ] **Step 4: Chạy test, xác nhận PASS** — Run: `php artisan test ...ProductInProgressGuardTest.php` — Expected: PASS.
- [ ] **Step 5: Commit** — (feat: guard chặn khóa hàng — luồng mua).

---

### Task 3: Luồng NHẬP

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductInProgressGuard.php` (thêm entry `flow='import'`)
- Modify: `hrm-api/Modules/MasterData/Tests/Feature/ProductInProgressGuardTest.php`

**Interfaces:**
- Consumes: hạ tầng Task 1.
- Produces: entry luồng nhập trong `blockingDocuments(...)['import']`.

- [ ] **Step 1: Viết test fail** cho 4 nhóm (YCNH `product_import_requests`+`product_import_request_details` cờ `is_complete`; ĐNNK `warehouse_import_requests`; PNK `product_imports`; order import `order_import_requests`). Mỗi loại ≥2 case (dở → xuất hiện, `target` đúng theo mục 6; Hủy/Hoàn thành → vắng). YCNH thêm case `is_complete=1` → vắng.
- [ ] **Step 2: Chạy test, xác nhận FAIL** — Run: `php artisan test ...ProductInProgressGuardTest.php` — Expected: FAIL.
- [ ] **Step 3: Xác minh hằng từ Model** (chú ý ĐNNK done = có `change_stock_time`; PNK 3=nháp), điền entry `import` vào `flowEntries()`. Ghi xác minh thành comment.
- [ ] **Step 4: Chạy test, xác nhận PASS** — Run: `php artisan test ...ProductInProgressGuardTest.php` — Expected: PASS.
- [ ] **Step 5: Commit** — (feat: guard chặn khóa hàng — luồng nhập).

---

### Task 4: Mặt hàng xuất hiện GIÁN TIẾP (combo/công thức/phụ kiện/đặt mã lẻ)

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductInProgressGuard.php` (thêm bước tính id gián tiếp)
- Modify: `hrm-api/Modules/MasterData/Tests/Feature/ProductInProgressGuardTest.php`

**Interfaces:**
- Consumes: bản đồ vị trí sản phẩm của `ProductUsageGuard` (`FK_COLUMNS`/`CHILD_FK_COLUMNS`/`REVERSE_FK_COLUMNS`), và `queryEntry()` Task 1.
- Produces: `blockingDocuments()` tính thêm các dòng mà `product_id` xuất hiện **gián tiếp** (là thành phần của một dòng cha khác), rồi vẫn áp bộ lọc "phiếu còn mở + theo dòng".

- [ ] **Step 1: Viết test fail** — seed một phiếu dở mà dòng của nó tham chiếu `product_id` cần khóa qua bảng combo/công thức/phụ kiện (lấy đúng 1 cặp bảng từ bản đồ `ProductUsageGuard`); assert phiếu đó xuất hiện trong nhóm luồng tương ứng. Thêm case: tham chiếu gián tiếp nhưng phiếu đã Hoàn thành → KHÔNG xuất hiện (bộ lọc "còn mở" vẫn áp).
- [ ] **Step 2: Chạy test, xác nhận FAIL** — Run: `php artisan test ...ProductInProgressGuardTest.php` — Expected: FAIL.
- [ ] **Step 3: Implement** — dùng lại bản đồ `ProductUsageGuard` để map `product_id` → tập dòng/`parent_id` liên quan, rồi đưa các phiếu cha đó qua đúng bộ lọc trạng thái "còn mở" của flow entry tương ứng (không phát minh lại logic trạng thái). Khử trùng lặp phiếu đã có từ tham chiếu trực tiếp (theo `doc`+`code`).
- [ ] **Step 4: Chạy test, xác nhận PASS** — Run: `php artisan test ...ProductInProgressGuardTest.php` — Expected: PASS.
- [ ] **Step 5: Commit** — (feat: guard tính mặt hàng gián tiếp).

---

### Task 5: Gắn guard vào `ProductLifecycleService::lock()` + response 422 `blocking_documents`

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductLifecycleService.php` (trong `lock()`, sau check `STATUS_TRADING`, trước `setStatus(...STATUS_STOPPED)`)
- Create/Modify: `hrm-api/Modules/MasterData/Tests/Feature/ProductLockBlockingTest.php`

**Interfaces:**
- Consumes: `ProductInProgressGuard::blockingDocuments($productId, companyId())`.
- Produces: `PUT /api/v1/master-data/products/{id}/lock` trả **422** `{ message: 'Không thể khóa: hàng hóa đang trong tiến trình.', blocking_documents: {purchase,import,export} }` khi có phiếu dở; ngược lại khóa thành công như cũ.

- [ ] **Step 1: Viết test fail (Feature, gọi endpoint lock)** — (a) seed 1 phiếu xuất dở cho 1 sản phẩm Đang kinh doanh của công ty test → `putJson('/api/v1/master-data/products/{id}/lock')` ⇒ 422, JSON có `blocking_documents.export` ≥1; (b) sản phẩm không có phiếu dở ⇒ 200, `product_company_coefficients.status` = 4; (c) [Review Focus fail-safe] khi 1 bảng flow không tồn tại trong DB test → guard bỏ qua bảng đó, endpoint không 500.
- [ ] **Step 2: Chạy test, xác nhận FAIL** — Run: `php artisan test Modules/MasterData/Tests/Feature/ProductLockBlockingTest.php` — Expected: FAIL (lock vẫn trả 200 / chưa có `blocking_documents`).
- [ ] **Step 3: Implement** — trong `lock()`: sau check `STATUS_TRADING`, gọi `$groups = app(ProductInProgressGuard::class)->blockingDocuments($productId, $this->companyId());` nếu bất kỳ nhóm non-empty → `throw new HttpResponseException(response()->json(['message'=>self::MESSAGE_LOCK_IN_PROGRESS, 'blocking_documents'=>$groups], 422));` (thêm hằng `MESSAGE_LOCK_IN_PROGRESS`). Guard tự `Schema::hasTable`/try để không fatal khi thiếu bảng.
- [ ] **Step 4: Chạy test, xác nhận PASS** — Run: `php artisan test Modules/MasterData/Tests/Feature/ProductLockBlockingTest.php` — Expected: PASS.
- [ ] **Step 5: Commit** — (feat: chặn khóa hàng khi còn phiếu dở — wire service).

---

### Task 6: FE — bắt 422 `blocking_documents` + modal `ProductInProgressModal`

**Files:**
- Modify: `hrm-client/utils/productLifecycle.js` (nhánh catch của lock)
- Create: `hrm-client/components/product/ProductInProgressModal.vue` (dựng trên `components/modal/V2BaseModal.vue`)
- Modify: `hrm-client/components/product/ProductListPage.vue` và/hoặc `pages/master-data/products/_id/index.vue` (gắn modal vào chỗ gọi khóa tập trung)

**Interfaces:**
- Consumes: response 422 từ Task 5 (`error.response.data.blocking_documents`).
- Produces: khi lock trả 422 có `blocking_documents` → KHÔNG toast, phát sự kiện/ở trạng thái mở `ProductInProgressModal` với prop `blockingDocuments`.

- [ ] **Step 1: Grep khuôn sẵn có** — `grep -rn 'custom-class="info-popover"'` không liên quan; chạy `grep -rn "V2BaseModal" components/ pages/` và đọc 1 modal danh sách mẫu (skill `modal-popup`, `list-page`, `button-convention`) để bám chuẩn trước khi dựng. (Không có unit test FE trong repo → task này verify bằng chạy app/Playwright ở Step 4.)
- [ ] **Step 2: Sửa `productLifecycle.js`** — trong catch của hàm lock: nếu `status===422 && data.blocking_documents` → gọi callback/emit mở modal (truyền `data.blocking_documents`), return; các lỗi 422/423 khác giữ nguyên toast `message`.
- [ ] **Step 3: Tạo `ProductInProgressModal.vue`** — tiêu đề "Hàng hóa đang trong tiến trình — chưa thể khóa"; 3 khối Luồng mua / Luồng nhập / Luồng xuất, nhóm rỗng thì ẩn; mỗi khối bảng cột **Mã phiếu | Người tạo | Ngày tạo**; mã phiếu: `target==='hrm'` → `<nuxt-link>`/router nội bộ, `target==='erp'` → `<a :href target="_blank">`. Gắn modal vào `ProductListPage.vue`/`_id/index.vue`.
- [ ] **Step 4: Verify thủ công/Playwright trên app** — khóa 1 mặt hàng có phiếu dở → hiện modal đúng danh sách, link mở đúng nơi (HRM nội bộ / ERP tab mới); khóa mặt hàng không vướng → khóa thành công, không modal. Ghi kết quả vào checkpoint.
- [ ] **Step 5: Commit** — (feat: FE modal danh sách phiếu chặn khóa hàng).

---

## Ghi chú thực thi

- Test BE chạy trên **DB dev** qua `DatabaseTransactions` (KHÔNG phải sqlite/RefreshDatabase): bảng ERP tồn tại sẵn trong DB gộp; seed dòng tối thiểu bằng `DB::table()->insert()` (đủ cột NOT NULL), assert, rollback. Công ty 6 là công ty sạch (0 dòng hàng×công ty) — dùng làm fixture như `ProductExportApiTest`.
- Prod có đụng DB → **chỉ đọc**; mọi verify ghi/khóa chạy trên DB dev.
- Chưa được yêu cầu commit/push: các Step "Commit" chỉ chạy khi user cho phép; attribution `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

### Checkpoint — 2026-10-29
Vừa hoàn thành: Lập xong plan.md (6 task TDD) theo design đã duyệt.
Đang làm dở: (chưa code) — chờ user chọn cách thực thi.
Bước tiếp theo: User review plan → chọn Subagent-driven hay Native → bắt đầu Task 1.
Blocked: (không)
