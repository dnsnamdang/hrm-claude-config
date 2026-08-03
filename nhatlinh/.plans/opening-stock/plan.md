# Plan — Nhập tồn đầu cho kho (Opening Stock)

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:subagent-driven-development (khuyến nghị) hoặc superpowers:executing-plans để triển khai task-by-task. Steps dùng checkbox (`- [ ]`).
> Design tóm tắt: `design.md` · Spec đầy đủ: `docs/superpowers/specs/2026-07-06-opening-stock-design.md`
> @manhcuong · Repo API: `nhatlinh-api` (Modules/Warehouse) · Repo Client: `nhatlinh-client`

**Goal:** Thêm loại phiếu nhập `receipt_type = 5` "Nhập tồn đầu" (giá tay, chặn cứng khi duyệt nếu hàng đã có movement trong kho, import Excel dòng hàng vào form).

**Architecture:** Tái dùng 100% màn/workflow/permission phiếu nhập kho. Chặn cứng ở `WhReceiptService::approve()` (mirror `assertReturnRemaining`). Import Excel = `V2BaseImportModal` 4 bước + endpoint validate BE, dòng hợp lệ đổ vào bảng form (KHÔNG ghi DB tại bước import).

**Ràng buộc chung (mọi task):**
- KHÔNG migration, KHÔNG permission mới, KHÔNG commit git.
- BE rethrow `ValidationException` (không catch chung), FE lỗi inline `is-invalid`/`invalid-feedback` + flag `touched`.
- Route static đặt TRƯỚC route wildcard `/{id}`.
- Verify BE bằng `php -l` + tinker smoke test; FE user test trình duyệt (node cũ không build CI).

---

## Phase duy nhất — BE + FE

### Backend (nhatlinh-api)

- [x] **T1. Entity + Request: khai báo loại nhập 5** ✔ review Approved
  - Modify: `Modules/Warehouse/Entities/WhReceipt.php` — thêm dưới `RECEIPT_TYPE_PRODUCTION`:
    ```php
    const RECEIPT_TYPE_OPENING = 5; // Nhập tồn đầu (khai báo tồn ban đầu khi triển khai)
    ```
    và thêm `['id' => 5, 'name' => 'Nhập tồn đầu']` vào cuối `RECEIPT_TYPES`.
  - Modify: `Modules/Warehouse/Http/Requests/WhReceiptRequest.php`:
    - `'receipt_type' => 'nullable|integer|in:1,2,3,4,5'`
    - Chặn trùng mã hàng trong cùng phiếu khi type=5 — thêm vào `rules()`:
      ```php
      $rules = [ /* ...rules hiện có... */ ];
      if ((int) $this->input('receipt_type') === 5) {
          $rules['items.*.product_id'] .= '|distinct';
      }
      return $rules;
      ```
      + message: `'items.*.product_id.distinct' => 'Mã hàng bị trùng trong phiếu tồn đầu — mỗi mã chỉ 1 dòng'`.
  - Verify: `php -l` 2 file; tinker `WhReceipt::RECEIPT_TYPES` có id 5; POST store type=5 với 2 dòng trùng product_id → 422 distinct, 2 dòng khác nhau → tạo OK (accessor `receipt_type_name` = "Nhập tồn đầu").

- [x] **T2. `assertOpeningStock` + hook approve()** ✔ review Approved sau 2 vòng fix race: thêm Product lock (sort id) + `lockForUpdate` trên chính query stock_movements (current read, thoát snapshot RR — mirror đủ pattern assertEnough); smoke 3 kịch bản pass
  - Modify: `Modules/Warehouse/Services/WhReceiptService.php`:
    - Trong `approve()`, sau nhánh `RECEIPT_TYPE_PRODUCTION`, thêm:
      ```php
      // Nhập tồn đầu: chỉ cho hàng CHƯA có bất kỳ phát sinh nào trong kho
      if ((int) $receipt->receipt_type === WhReceipt::RECEIPT_TYPE_OPENING) {
          $this->assertOpeningStock($receipt);
      }
      ```
    - Method mới (mirror style `assertReturnRemaining`, đặt cạnh nó):
      ```php
      // ---------------------------------------------------------------
      // assertOpeningStock — phiếu Nhập tồn đầu chỉ được duyệt khi các mã hàng
      // CHƯA có bất kỳ stock_movements nào trong kho (tồn đầu = khai báo ban đầu).
      // Chạy trong transaction của approve, TRƯỚC postMovement.
      // ---------------------------------------------------------------
      public function assertOpeningStock(WhReceipt $receipt): void
      {
          if (!$receipt->relationLoaded('items')) {
              $receipt->load('items');
          }
          $productIds = $receipt->items->pluck('product_id')->unique()->values();

          $existedIds = StockMovement::where('warehouse_id', $receipt->warehouse_id)
              ->whereIn('product_id', $productIds)
              ->distinct()
              ->pluck('product_id');

          if ($existedIds->isEmpty()) {
              return;
          }

          $codes = Product::whereIn('id', $existedIds)->orderBy('code')->pluck('code')->all();
          Validator::make([], [])->after(function ($v) use ($codes) {
              $v->errors()->add(
                  'items',
                  'Không thể duyệt: các mã hàng sau đã có phát sinh trong kho, không được nhập tồn đầu: '
                  . implode(', ', $codes)
              );
          })->validate();
      }
      ```
      (import `Modules\Category\Entities\Product` — kiểm tra namespace Product đang dùng trong service/module, dùng đúng class sẵn có.)
  - Verify smoke tinker (bọc transaction như pattern service):
    1. Chọn 1 product CHƯA có movement ở 1 kho test → tạo phiếu type=5 (qty 10) → submit → approve → `inventories` (kho, product) = 10, movement type 1 `source_type='receipt'`.
    2. Tạo phiếu tồn đầu thứ 2 cùng kho cùng mã → approve → 422, message chứa mã hàng.
    3. Phiếu type=3 "Nhập khác" vẫn duyệt bình thường (không bị chặn) — regression.

- [x] **T3. Endpoint validate import** ✔ review Approved (1 vòng fix: `->distinct()` tầng DB cho query movements). Minor ghi nhận: chưa guard `!is_array($row)` từng dòng; `is_numeric` không nhận "1,5"; note rỗng → null
  - Modify: `Modules/Warehouse/Services/WhReceiptService.php` — method `validateOpeningImport(array $rows, int $warehouseId): array`:
    - Với mỗi row (key FE gửi: `code, name, unit, quantity, unit_price, note`) trả `['index','row'=>index+2,'isValid','errors'=>[]]` + khi hợp lệ kèm data resolve `product_id, product_code, product_name, unit_id, unit_name, conversion_rate, quantity, quantity_base (= quantity*conversion_rate), unit_price (mặc định 0), note`.
    - Rules (theo spec mục 3.4): code bắt buộc + tồn tại `products.code` (case-insensitive, trim, KHÔNG tự tạo); unit bắt buộc + là tên đơn vị thuộc `product_units` của product (case-insensitive, so theo `units.name`); quantity bắt buộc numeric > 0; unit_price trống→0, có thì numeric ≥ 0; code trùng trong file → lỗi từ dòng thứ 2 trở đi ("Mã hàng trùng với dòng N"); product đã có `stock_movements` trong `$warehouseId` → lỗi "Mã hàng đã có phát sinh trong kho, không được nhập tồn đầu".
    - Query gộp trước vòng lặp (1 query products theo codes + eager `productUnits.unit`, 1 query movements distinct product_id) — không query trong loop.
    - Return `['rows'=>..., 'total'=>n, 'validCount'=>..., 'invalidCount'=>...]`.
  - Modify: `Modules/Warehouse/Http/Controllers/Api/V1/WhReceiptController.php` — method `validateImport(Request $request)`:
    ```php
    public function validateImport(Request $request)
    {
        try {
            $rows = $request->input('rows');
            $warehouseId = (int) $request->input('warehouse_id');
            if (!is_array($rows) || empty($rows) || !$warehouseId) {
                return $this->responseJson('Dữ liệu validate rỗng hoặc thiếu kho', Response::HTTP_BAD_REQUEST);
            }
            $result = $this->service->validateOpeningImport($rows, $warehouseId);
            return $this->responseJson(
                "Validate xong: {$result['validCount']} hợp lệ, {$result['invalidCount']} lỗi",
                Response::HTTP_OK,
                $result
            );
        } catch (\Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
    ```
    (KHÔNG dùng `$request->validate()` — theo skill import-excel.)
  - Modify: `Modules/Warehouse/Routes/api.php` — trong group `/receipts`, đặt TRƯỚC `Route::get('/{id}', ...)`:
    ```php
    Route::post('/import/validate', [WhReceiptController::class, 'validateImport'])
        ->middleware('checkPermission:Thêm/sửa phiếu nhập kho');
    ```
  - Verify: `php -l`; tinker/curl có auth: rows gồm đủ case (mã sai, ĐVT sai, SL 0, giá âm, trùng mã, mã đã có movement, dòng hợp lệ) → từng dòng đúng lỗi kỳ vọng, dòng hợp lệ đủ field resolve, quantity_base = quantity × conversion_rate.

- [x] **T4. Endpoint file mẫu import** ✔ review Approved. Minor ghi nhận: pattern `tempnam().'.xlsx'` rò rỉ file 0-byte (kế thừa từ BomListController — cân nhắc sửa đồng loạt sau, cần hỏi)
  - Modify: Controller — method `importTemplate()`: dựng bằng PhpSpreadsheet Writer (pattern skill import-excel — tham chiếu `Modules/Assign/.../ProjectPhaseController.php::importTemplate`), font Times New Roman, header đậm nền xám: `Mã hàng * | Tên hàng (tham khảo) | ĐVT * | Số lượng * | Đơn giá | Ghi chú`, 2 dòng ví dụ (`SP.0001 / Cái / 100 / 50000`), `response()->download()` tên `Mau_nhap_ton_dau.xlsx`, xoá file temp sau download (`deleteFileAfterSend`).
  - Modify: routes — TRƯỚC `/{id}`:
    ```php
    Route::get('/import-template', [WhReceiptController::class, 'importTemplate'])
        ->middleware('checkPermission:Thêm/sửa phiếu nhập kho');
    ```
  - Verify: `php -l`; curl có auth tải file → mở được bằng Excel/soffice, đúng 6 cột header.

### Frontend (nhatlinh-client)

- [x] **T5. WhReceiptForm — nhánh loại 5 "Nhập tồn đầu"** ✔ review Approved (1 vòng fix: msgBoxConfirm → BaseConfirmModal; hidden-listener revert bắt X/ESC/backdrop, không double-handle). Gộp template nhánh `3 || 5`, khác biệt gate `=== 5`. Chọn kho lần đầu không hỏi confirm (by design)
  - Modify: `components/warehouse/receipt/WhReceiptForm.vue`:
    - Dropdown Loại nhập: thêm `{ id: 5, name: 'Nhập tồn đầu' }` (option 1 vẫn disabled).
    - Template `v-else-if="form.receipt_type === 5"`: clone nhánh `=== 3` (bảng dòng: mã/tên hàng, ĐVT theo `product_units`, SL, Đơn giá currency-format, Thành tiền, Ghi chú, xoá dòng; modal chọn hàng hoá; Tổng tiền) — đổi các ref/id modal để không đụng nhánh 3. Thêm nút **"Import Excel"** (icon ri-file-excel-2-line, theo skill button-convention) cạnh nút chọn hàng hoá; bấm khi `!form.warehouse_id` → toast "Vui lòng chọn kho trước khi import".
    - Thêm hàng từ modal chọn hàng hoá khi type=5: mã đã có trong bảng → bỏ qua + toast "đã có trong phiếu" (behavior modal sẵn có).
    - Watcher/confirm: đổi `form.warehouse_id` khi type=5 và bảng có dòng → BaseConfirmModal "Đổi kho sẽ cần kiểm tra lại tồn đầu, tiếp tục?" (không xoá dòng; hủy → revert kho cũ, mirror guard race đã dùng ở WhIssueForm).
    - Payload submit giữ cấu trúc hiện tại (`receipt_type: 5`, items có `unit_price`); logic tính Thành tiền/Tổng tiền dùng chung computed nhánh 3.
    - Edit mode: load lại phiếu type=5 hiển thị đúng nhánh (mirror `d.receipt_type || 3` hiện có).
  - Đọc trước: `.claude/skills/button-convention/SKILL.md` + `.claude/skills/modal-popup/SKILL.md`.
  - Verify: dev server — tạo/sửa/xem phiếu type=5, validate inline (thiếu kho/dòng/SL), lưu → gửi duyệt → duyệt OK; duyệt lần 2 cùng mã → toast lỗi 422 hiện danh sách mã; loại 2/3/4 không regression.

- [x] **T6. Import modal + store actions** ✔ review Approved, 0 Critical/Important. Component mới WhReceiptOpeningImportModal + 2 store action (download viết riêng gọi $axios trực tiếp vì apiGetMethod không forward responseType — verified). Minor: prop warehouseId thiếu null type (console warning); .filter(Boolean) bỏ âm thầm dòng lệch cache (hiếm)
  - Modify: `components/warehouse/receipt/WhReceiptForm.vue` (hoặc tách `WhReceiptOpeningImportModal.vue` trong cùng thư mục nếu form quá dài — ưu tiên tách, mirror `BomBuilderImportModal.vue`):
    - Dùng `V2BaseImportModal`: `modal-id="import-opening-stock-modal"`, title "Import tồn đầu", `template-file-name="Mau_nhap_ton_dau.xlsx"`, `skip-rows=0`.
    - `importColumns`: `code` (Mã hàng, aliases: 'Mã hàng','Ma hang'), `name` (Tên hàng (tham khảo)), `unit` (ĐVT, aliases 'ĐVT','DVT','Đơn vị tính'), `quantity` (Số lượng, aliases 'Số lượng','So luong','SL'), `unit_price` (Đơn giá, aliases 'Đơn giá','Don gia'), `note` (Ghi chú). Required: code, unit, quantity.
    - `@validate-data` → POST `warehouse/receipts/import/validate` body `{ warehouse_id, rows }` → gắn `importRows/importValidatedRows/importValidCount/importInvalidCount/currentStep=3` qua `$refs` (đúng events flow skill import-excel; map lỗi qua `utils/import-error-helper.js`).
    - `@import-data` → dòng hợp lệ (BE đã resolve `product_id/unit_id/conversion_rate/quantity_base`) → merge vào bảng form: trùng `product_id` với dòng đã có → **ghi đè SL/đơn giá/ghi chú**, còn lại append; hide modal + toast "Đã thêm N dòng".
    - `@download-template` → GET `warehouse/receipts/import-template` (arraybuffer → tải file).
  - Modify: `store/warehouse-receipt.js` — thêm 2 action `validateOpeningImport(payload)` + `downloadOpeningTemplate()` (mirror action export arraybuffer sẵn có của module).
  - Verify: dev server — tải file mẫu; upload file đủ case lỗi → step 3 hiện lỗi đúng dòng, dòng hợp lệ khoá; Import → bảng form nhận đúng dòng (trùng mã ghi đè); lưu phiếu → duyệt → tồn đúng.

### Test & bàn giao

- [x] **T7. E2E Playwright + regression** ✔ review Approved. Spec `e2e/tests/warehouse/opening-stock.api.spec.ts` (đuôi .api.spec.ts để vào project `api` theo testMatch) — 3/3 PASS; regression warehouse 40 pass/2 fail known-issue. Phát hiện 2 bug pre-existing API kho Category (response lồng `data.original.id`; thiếu default status) — KHÔNG patch, chờ quyết
  - Create: `e2e/tests/warehouse/opening-stock.spec.js` (pattern spec API warehouse sẵn có, user `e2e_warehouse@test.local`):
    1. API: tạo product E2E mới (hoặc product *.E2E chưa có movement) → tạo phiếu type=5 → submit → approve → GET báo cáo tồn/inventory thấy đúng SL.
    2. API: tạo phiếu tồn đầu thứ 2 cùng kho cùng mã → approve → expect 422 + message chứa mã hàng.
    3. API: validate import — body có dòng mã sai + dòng hợp lệ → expect isValid đúng từng dòng.
  - Run: `cd e2e && npx playwright test tests/warehouse/opening-stock.spec.js` → PASS; chạy lại suite warehouse cũ không regression.
  - Cập nhật plan.md checkpoint + STATUS.md (wrap up).

---

### Checkpoint — 2026-07-07 (CODE HOÀN THÀNH TOÀN BỘ — SẴN SÀNG BÀN GIAO)
Vừa hoàn thành: **7/7 task BE+FE+E2E, review Approved từng task + FINAL REVIEW toàn feature: Ready to merge YES** (chưa commit, trên main cả 2 repo).
- Final review (model cao nhất) soi seam cross-task: contract import khớp 3 phía (BE↔modal↔V2BaseImportModal), guard đổi kho không giẫm modal import, luồng end-to-end đổi-kho-sau-import chặn đúng ở BE. 3 finding fix-now ĐÃ FIX + re-verify: (1) import trùng mã ghi đè thêm ĐVT (unit_id+conversionRate — SL đi kèm ĐVT trong file, spec đã cập nhật); (2) guard `!is_array($row)` trong validateOpeningImport; (3) prop warehouseId default null.
- E2E: `e2e/tests/warehouse/opening-stock.api.spec.ts` 3/3 PASS; regression warehouse khớp baseline (2 fail selector known-issue cũ).
Đang làm dở: — (code xong 100%)
Bước tiếp theo (user):
1. Test trình duyệt: form loại "Nhập tồn đầu" (chọn hàng + ĐVT + giá → lưu → gửi duyệt → duyệt; duyệt lần 2 cùng kho/mã → 422 hiện danh sách mã); Import Excel (tải mẫu → upload → validate hiện lỗi từng dòng → import đổ bảng, trùng mã ghi đè cả ĐVT; chưa chọn kho → toast; đổi kho khi có dòng → confirm); regression loại nhập 2/3/4.
2. Commit 2 repo khi đạt — LƯU Ý 2 file untracked dễ sót: `nhatlinh-client/components/warehouse/receipt/WhReceiptOpeningImportModal.vue` + `e2e/tests/warehouse/opening-stock.api.spec.ts`.
3. Deploy (KHÔNG migration/permission mới): `route:clear` + `route:cache` nếu server bật route cache; rebuild Nuxt; xác nhận quyền 1124-1126 đã seed production.
Blocked: —
**Backlog đề xuất (pre-existing, NGOÀI feature — cần user quyết, lập task riêng):**
- (5a — ưu tiên) `assertReturnRemaining` lock header nhưng đọc issuedBase/returnedBase bằng SUM plain dưới REPEATABLE READ — cùng lỗ hổng race đã fix ở assertOpeningStock, pattern fix sẵn trong file.
- (5b) `tempnam().'.xlsx'` rò rỉ file 0-byte mỗi lần tải template — 2 nơi: WhReceiptController (mới, copy pattern) + BomListController (gốc).
- (5c) 2 bug API kho Category: WarehouseService::updateOrCreate trả response lồng `data.original.id`; POST /category/warehouses thiếu default `status` → lỗi SQL. E2E đang phải workaround.
- Minor trong feature (không chặn): T3 is_numeric không nhận "1,5" locale VN + note rỗng→null + whereRaw không dùng index; T6 .filter(Boolean) bỏ âm thầm dòng lệch cache + modal kẹt step 4 nếu cache rỗng (đường gần như không xảy ra); T7 thiếu assert product_name + cleanup lồng test 2 + rác 2 kho+2 phiếu E2E/lần chạy; T5 toast trùng mã dead-code; T2 message thiếu mã nếu product xoá cứng; BE message "Mã hàng không tồn tại" khi code trống (FE đã chặn required).

### Checkpoint cũ — 2026-07-06 (tạm dừng theo yêu cầu user)
Vừa hoàn thành: **BE T1-T4 xong 100%, đều qua review Approved** (subagent-driven, mỗi task implementer + reviewer riêng, fix theo review):
- T1 Entity+Request (loại 5 + distinct), T2 assertOpeningStock (2 vòng fix race: Product lock + locking read movements — smoke 3 kịch bản pass), T3 validate import (6 rule, contract 10 field resolve, smoke đủ case, fix distinct), T4 file mẫu import (verify đọc lại file OK).
- Toàn bộ CHƯA commit, nằm trên `main` nhatlinh-api (3 file: WhReceipt.php, WhReceiptRequest.php, WhReceiptService.php + WhReceiptController.php + Routes/api.php).
Đang làm dở: **T5 (FE form nhánh loại 5)** — subagent code XONG (+73/−10 dòng `components/warehouse/receipt/WhReceiptForm.vue`, uncommitted trên main nhatlinh-client) nhưng bị dừng TRƯỚC bước verify tĩnh + CHƯA review, report chưa ghi (`scratchpad/sdd/task-5-report.md` không tồn tại).
Bước tiếp theo: (1) verify tĩnh + review diff T5 (brief: `<scratchpad>/sdd/task-5-brief.md`, diff = `git diff HEAD -- components/warehouse/receipt/WhReceiptForm.vue`) → fix nếu có finding; (2) T6 modal import + store (brief đã soạn sẵn: `sdd/task-6-brief.md`); (3) T7 E2E.
Blocked: —
Ghi chú resume: ledger + brief/report tại scratchpad session cũ `/private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-nhatlinh/86253d2e-a7b4-49c8-aba3-1f919ec884fc/scratchpad/sdd/` (scratchpad theo session — nếu session mới không còn thì brief T5/T6 tái tạo từ plan.md mục T5/T6 là đủ). Minor findings chờ final review: (a) pre-existing `assertReturnRemaining` đọc SUM plain dưới RR (lỗ hổng snapshot tương tự T2 — NGOÀI scope, cần user quyết); (b) pre-existing `tempnam().'.xlsx'` rò rỉ file 0-byte (kế thừa BomListController — sửa phải sửa 2 nơi, cần hỏi); (c) T3: chưa guard `!is_array($row)`/không nhận số "1,5" locale VN/note rỗng→null; (d) T1: style `$rules[...] .=`; (e) T2: message thiếu code nếu product bị xoá cứng.
