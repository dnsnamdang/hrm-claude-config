# YCXH loại 15 (Xuất khuyến mại HĐ hãng) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps dùng checkbox (`- [ ]`) để tracking.

**Goal:** Bật trọn chuỗi YCXH → ĐNXK → PXK → PXH + hạch toán cho loại xuất 15 (XUAT_KM_HD_HANG) trong HRM, bám đúng ERP.

**Architecture:** Dựng loại 15 như "anh em" loại 14 (cùng `firm_contract_id`, snapshot KH, cơ chế tab, chuỗi chứng từ). Khác 4 điểm: nguồn dòng = combo KM `firm_contract_combo_group_option_products` (giá 0), kho KM `promo_warehouse_id`, hạch toán chỉ giá vốn (Nợ 632 / Có 1561), điều kiện `canProductExportPromotion`. Không migration, không thêm quyền.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Nuxt 2 / Vue 2 / Bootstrap-Vue (hrm-client), MySQL (gộp DB — bảng ERP dùng chung), Playwright (Node 20) để e2e.

**Spec:** `docs/superpowers/specs/gop-db/2026-10-16-ycxh-xuat-khuyen-mai-type15-design.md`

## Global Constraints

- **`hrm_erp_gop` là DB PRODUCTION — CHỈ ĐỌC.** Mọi GHI/seed/migrate chỉ trên DB **local `erp_hrm_check`**.
- **KHÔNG migration** — mọi cột đã có sẵn (spec §4.1). Nếu phát hiện thiếu cột → DỪNG, báo user.
- **KHÔNG thêm quyền mới** — YCXH không gate theo loại; chỉ `CREATABLE_TYPE_IDS` + creator/nháp.
- Giá KM = 0 toàn bộ (`price`, `allocated_price`, `total_amount`, `rebate_price`) — BE ép 0, không tin FE.
- Nhánh `develop` cả 2 repo (con của `gop_db`). KHÔNG commit/push khi user chưa yêu cầu.
- `extends BaseModel` cho model mới; `auth()->id()` cho `created_by/updated_by` (KHÔNG `->info->id`).
- FE màn mới: `V2Base*`, nhóm kho dùng `V2BaseFormCard`; cờ quyền fail-closed (không literal `true`).
- Số định dạng quốc tế (`1,234,567.89`); hạch toán `round()` tới đồng (bám helper sẵn có).
- Bám connection mặc định — KHÔNG dùng `mysql2`/`DB_CONNECTION_SECOND`.

## Review Focus

- **Vượt SL combo khi gửi duyệt song song 2 phiếu** — tổng SL đang xuất (in-flight) + SL mới phải ≤ `take_qty − exported_qty`; nếu chỉ check `exported_qty` mà quên in-flight thì xuất kép. → Task 1.5.
- **Ghi ngược `exported_qty` cộng kép khi finalize PXH lại / hủy PXH** — phải idempotent + có chiều hoàn (revert) khi hủy. → Task 4.2.
- **`export_price` = 0 cho hàng KM** — giá BÁN = 0 nhưng giá VỐN (`export_price`) phải là cost thật từ layer tồn; nếu lấy nhầm giá bán 0 thì bút toán giá vốn = 0 (sai). → Task 5.1.
- **HĐ hết hiệu lực / sai người lập** — `canProductExportPromotion` phải chặn ở Gửi duyệt (422), không để lọt xuống tạo chứng từ. → Task 1.5.
- **Kho KM rỗng hoặc không thuộc `promo_warehouse_ids` của công ty** — chọn kho ngoài danh sách KM phải bị chặn, không cho xuất ra kho thường. → Task 1.2 + 2.2.

---

## Phase 1 — BE: bật tạo YCXH loại 15

### Task 1.1: Thêm 15 vào `CREATABLE_TYPE_IDS`

**Files:**
- Modify: `Modules/Assign/Entities/Warehouse/ProductExportRequest.php:73-84`

- [x] **Step 1:** Thêm `self::XUAT_KM_HD_HANG` (= 15) vào mảng `CREATABLE_TYPE_IDS` (đặt cạnh `XUAT_BAN_HD_HANG`).
- [x] **Step 2:** Verify: `php -r` hoặc tinker `ProductExportRequest::CREATABLE_TYPE_IDS` phải chứa 15.
- [x] **Step 3:** Smoke: gọi `POST /assign/product-export-requests` với `type=15` (payload tối thiểu, nháp) — KHÔNG còn 422 "loại không được phép" (sẽ rơi sang lỗi validate khác, chấp nhận ở bước này).

### Task 1.2: `rulesForType()` nhánh loại 15

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php:1211` (`rulesForType`)

**Interfaces:**
- Produces: validate cho `type=15`: `firm_contract_id` (required_if gửi duyệt, exists `firm_contracts,id`), `promo_warehouse_id` (required_if gửi duyệt), `products.*.contract_product_id` (= `id` dòng combo), `products.*.qty` (number_only, >0).

- [x] **Step 1:** Thêm nhánh `if ($type === ProductExportRequest::XUAT_KM_HD_HANG)` trong `rulesForType()`, clone nhánh loại 14 (`:1372` khu vực firm_tab) nhưng:
  - `promo_warehouse_id` thay cho `warehouse_id`: `['required_if:status,2', 'integer']` — danh sách hợp lệ kiểm ở service (Task 2.2) để đồng bộ công ty.
  - Giữ `firm_contract_id`, `firm_tab_ids.*` (exists theo `firm_contract_id`), `products.*.qty`.
  - Lưu nháp (status=3) nới `required` theo rule chung HRM.
- [x] **Step 2:** Verify `php -l` file controller sạch.
- [x] **Step 3:** Gửi `POST` type=15 thiếu `promo_warehouse_id` + status=2 → trả **422** đúng field `promo_warehouse_id`.

### Task 1.3: `createFromRequest()` rẽ nhánh loại 15

**Files:**
- Modify: `Modules/Assign/Services/ProductExportRequestService.php:320-327` (`createFromRequest`)

**Interfaces:**
- Consumes: `createFromFirmContractPromotion(array $data): ProductExportRequest` (Task 1.4).

- [x] **Step 1:** Thêm `elseif ($type === ProductExportRequest::XUAT_KM_HD_HANG) { $model = $this->createFromFirmContractPromotion($data); }` NGAY SAU nhánh `XUAT_BAN_HD_HANG` (`:320-321`).
- [x] **Step 2:** `php -l` sạch.

### Task 1.4: `createFromFirmContractPromotion()` + `writeFirmContractComboTabs()`

**Files:**
- Modify: `Modules/Assign/Services/ProductExportRequestService.php` (thêm method mới cạnh `createFromFirmContract` `:1123` và `writeFirmContractTabs` `:1206`)

**Interfaces:**
- Produces:
  - `createFromFirmContractPromotion(array $data): ProductExportRequest`
  - `writeFirmContractComboTabs(FirmContract $firmContract, ProductExportRequest $req, array $data, int $status, ?int $excludeRequestId, bool $checkQty = true): void`

- [x] **Step 1:** Viết `createFromFirmContractPromotion()` — clone `createFromFirmContract()` (`:1123-1186`), đổi:
  - `'type' => ProductExportRequest::XUAT_KM_HD_HANG`
  - thay `'warehouse_id'` bằng `'promo_warehouse_id' => $data['promo_warehouse_id'] ?? null` (KM không xuất thẳng → bỏ nhánh `is_export_direct`; `warehouse_id` để null).
  - `need_repair` ép 0 (KM không lắp đặt).
  - gọi `writeFirmContractComboTabs(...)` thay `writeFirmContractTabs(...)`.
  - gửi duyệt (status=2) gọi `assertFirmContractCanExportPromotion($firmContractId, $firmContract)` (Task 1.5) thay `assertFirmContractCanExport`.
- [x] **Step 2:** Viết `writeFirmContractComboTabs()` — clone `writeFirmContractTabs()` (`:1206-1278`) + `writeFirmContractTabLines()` (`:1283`), đổi nguồn dòng:
  - `products[].contract_product_id` = **`id` dòng `firm_contract_combo_group_option_products`** (không phải `firm_contract_tab_products.id`).
  - Query dòng từ `firm_contract_combo_group_option_products` thay `firm_contract_tab_products`; cột lưu tab: `firm_contract_tab_combo_product_id` = `id` dòng combo (thay `firm_contract_tab_product_id`).
  - Nhóm tab: dùng `combo_campaign_id` / tab tương ứng combo (bám cách ERP gắn tab combo; nếu combo không có parent tab rõ ràng thì gộp vào 1 tab theo `firm_contract.code`).
  - Dòng phẳng `product_export_request_details`: **giá = 0** toàn bộ (`standard_price/net_price/price_extra → 0`, `rebate_price = 0`), `firm_contract_tab_combo_product_id` = `id` combo.
- [x] **Step 3:** `php -l` sạch.
- [x] **Step 4:** Tinker (local `erp_hrm_check`): tạo YCXH type=15 nháp từ `firm_contract_id=10626` với 1 dòng combo → kiểm `product_export_requests` có `promo_warehouse_id` + `firm_contract_id`, `product_export_request_tab_products` có `firm_contract_tab_combo_product_id`, details giá 0.

### Task 1.5: Validate `canProductExportPromotion` + chặn vượt SL combo

**Files:**
- Modify: `Modules/Assign/Services/ProductExportRequestService.php` (thêm `assertFirmContractCanExportPromotion`, `assertComboLineQtyWithinRemaining`)
- Tham chiếu ERP: `FirmContract::canProductExportPromotion()` (`FirmContract.php:1325`); công thức còn-xuất `qty = take_qty − exported_qty − exporting_qty` (ERP `FirmContractProductExportService.php:58`).

**Interfaces:**
- Produces:
  - `assertFirmContractCanExportPromotion(?int $firmContractId, ?FirmContract $firmContract): void` — ném `ValidationException`/422 nếu HĐ null, status ≠ CÓ_HIỆU_LỰC, `created_by !== auth()->id()`, hoặc tổng combo còn-xuất = 0.
  - `assertComboLineQtyWithinRemaining(int $firmContractId, array $products, ?int $excludeRequestId): void` — mỗi dòng: `qty mới + in_flight(đang xuất, loại trừ $excludeRequestId) ≤ take_qty − exported_qty`; vượt → 422 message nghiệp vụ nêu rõ SL còn.

- [x] **Step 1:** Viết 2 method trên. In-flight đọc từ `product_export_request_details` / tab_products loại 15 pending (status ∈ {2,…}, ≠ hoàn tất/hủy), group theo `firm_contract_tab_combo_product_id`.
- [x] **Step 2:** Gọi `assertComboLineQtyWithinRemaining` trong `writeFirmContractComboTabs` khi `status === STATUS_CHO_DUYET` (mirror `:1229`).
- [x] **Step 3:** `php -l` sạch.
- [x] **Step 4:** Tinker: gửi duyệt phiếu với qty vượt `take_qty − exported_qty` → bắt 422; HĐ không hiệu lực → 422; sai người lập → 422.

---

## Phase 2 — BE: endpoint load dòng combo KM + danh sách kho KM

### Task 2.1: Endpoint load dòng combo KM (`firmContractPromotionLines`)

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` (thêm `firmContractPromotionLines(int $firmContractId, ?int $excludeRequestId = null): array`, cạnh `firmContractProductLines` `:540`)
- Modify: `Modules/Assign/Routes/api.php` (thêm route GET nạp payload type=15; hoặc mở rộng nhánh `firm_contract_id` ở `:474-497` nhận thêm `product_lines_promotion` khi `type=15`)
- Tham chiếu ERP: `FirmContractProductExportService::getDataForWarehouseExport()` nhánh `$type==1` (`:28-71`).

**Interfaces:**
- Produces: mảng dòng combo, mỗi dòng: `contract_product_id` (= `id` combo), `product_id`, `code`, `name`, `model_name`, `brand_name`, `unit_id`, `unit_name`, `contract_qty`, `exported_qty`, `in_flight_qty`, `remaining_qty` (= `take_qty − exported − in_flight`), `price=0`, `allocated_price=0`, `price_extra=0`, `total_amount=0`, `vat_percent`, `avatar`, `unit_coefficient`.

- [x] **Step 1:** Viết query: `firm_contract_combo_group_option_products` lọc `firm_contract_id` + `take_qty > 0` + `combo_campaign_id ∈` (combo_campaign_id của tab HĐ). Join `products` lấy `avatar`, `brand_id`.
- [x] **Step 2:** Tính `remaining_qty = take_qty − exported_qty − exporting_qty(in-flight)`; gộp key `product_id-unit_id-model_name` cộng dồn SL; giá = 0; `unit_coefficient = Product::getUnitCoefficient(product_id, unit_id)`; `avatar` qua `buildProductAvatarUrl()`.
- [x] **Step 3:** Gắn vào payload khi FE chọn HĐ hãng với `type=15` (nhánh `:494` trả `product_lines` — dùng method mới khi type=15).
- [x] **Step 4:** `php -l` sạch.
- [x] **Step 5:** Verify qua HTTP/tinker: `firm_contract_id=10626` trả đúng số dòng combo còn hàng, giá 0, `remaining_qty` khớp `take_qty − exported`.

### Task 2.2: Endpoint danh sách kho khuyến mại

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` (thêm `promoWarehouses(Request $request)`)
- Modify: `Modules/Assign/Routes/api.php` (route GET `promo-warehouses`)
- Tham chiếu ERP: `Warehouse::getPromoWarehouse()` (`Warehouse.php:656-662`).

**Interfaces:**
- Produces: danh sách `{ id (warehouse_id), text: "code - name" }` = kho thuộc `companies.promo_warehouse_ids` (JSON accounting_warehouse_id) của công ty user, map qua `accounting_warehouses.warehouse_id`, `warehouses.status=1`.

- [x] **Step 1:** Port `getPromoWarehouse()`: lấy `company_id` user (`auth()->user()->info->company_id`), đọc `companies.promo_warehouse_ids` (cast JSON/array), `accounting_warehouses whereIn id + company_id` → `pluck('warehouse_id')`, trả `warehouses whereIn id + status=1` dạng `CONCAT(code,' - ',name)`.
- [x] **Step 2:** Dùng helper này cùng validate Task 1.2 để chặn `promo_warehouse_id` ngoài danh sách (kho không thuộc công ty → 422).
- [x] **Step 3:** `php -l` sạch.
- [x] **Step 4:** Verify: user công ty có cấu hình KM → trả đúng kho; `promo_warehouse_id` lạ → bị chặn.

---

## Phase 3 — FE: form tạo/sửa YCXH loại 15

### Task 3.1: Form loại 15 (HĐ hãng + kho KM + bảng combo giá 0)

**Files:**
- Modify: màn tạo/sửa YCXH `hrm-client` (bám màn loại 14 hiện có — xác định file chính xác bằng `grep -rn "XUAT_BAN_HD_HANG\|firm_contract_id\|product-export-requests" pages/assign` khi thực thi).

- [x] **Step 1:** Thêm loại 15 vào dropdown chọn loại (đã nằm trong `DROPDOWN_TYPE_IDS` BE — chỉ cần FE render nhãn "Xuất khuyến mại").
- [x] **Step 2:** Khi `type === 15`: hiện select **HĐ hãng** (clone UI loại 14) + select **Kho khuyến mại** (`V2BaseSelect`, nguồn endpoint Task 2.2), bắt buộc. Nhóm kho/xuất-nhập dùng `V2BaseFormCard`.
- [x] **Step 3:** Bảng dòng hàng: load từ payload `product_lines` (type=15, Task 2.1). Cột giá hiển thị `0` và **không cho sửa**; cột SL cho nhập, chặn > `remaining_qty` (báo đỏ dưới ô, không tự kéo max — skill form-validate §3).
- [x] **Step 4:** Submit: payload `{ type:15, firm_contract_id, promo_warehouse_id, firm_tab_ids, products:[{contract_product_id, qty}], status }`. Lưu nháp nới required.
- [x] **Step 5:** Validate realtime `vee-validate` trên `V2Base*`; cờ quyền fail-closed; sau lưu `markFormSaved()` + `$router.push` về danh sách.
- [x] **Step 6:** Verify Playwright (xem Phase 6) — ở task này chỉ cần màn render + submit nháp thành công.

---

## Phase 4 — BE: ĐNXK pass-through + PXH trừ tồn + ghi ngược `exported_qty`

### Task 4.1: Pass-through combo xuống ĐNXK/PXK/PXH

**Files:**
- Modify: `Modules/Assign/Services/WarehouseExportRequestService.php` (`buildDetailAttributes()` — nơi pass-through loại 14) + pipeline PXK/PXH nếu cần.

**Interfaces:**
- Produces: `product_export_request_details` loại 15 mang đủ `firm_contract_tab_combo_product_id` + `promo_warehouse_id` xuống ĐNXK → PXK → PXH; kho xuất = `promo_warehouse_id`.

- [x] **Step 1:** Grep `buildDetailAttributes`/`firm_contract_tab_product_id` để xác định điểm map; bổ sung `firm_contract_tab_combo_product_id` vào tập cột pass-through (song song cột loại 14).
- [x] **Step 2:** Bảo đảm ĐNXK lấy kho = `promo_warehouse_id` của YCXH loại 15 (không rơi về `warehouse_id` null).
- [x] **Step 3:** `php -l` sạch.
- [x] **Step 4:** Tinker: tạo ĐNXK từ YCXH loại 15 → details có `firm_contract_tab_combo_product_id` + kho KM đúng.

### Task 4.2: PXH hoàn tất → ghi ngược `exported_qty` về combo (idempotent + revert)

**Files:**
- Modify: `Modules/Assign/Services/FirmContractExportStockService.php` (thêm nhánh combo cạnh logic loại 14 `:62,71,78,249,252`)
- Tham chiếu ERP: `ProductExport.php:1775-1790` (ghi ngược `exported_qty` combo).

**Interfaces:**
- Produces: khi PXH loại 15 finalize → `firm_contract_combo_group_option_products.exported_qty += SL xuất` (theo `id` combo đã lưu); khi hủy/revert PXH → trừ lại. Idempotent: finalize lại không cộng kép.

- [x] **Step 1:** Thêm method ghi ngược combo: group SL theo `firm_contract_tab_combo_product_id`, `increment('exported_qty', $qty)` atomic (bám bài học lost-update — KHÔNG `+= rồi save()`).
- [x] **Step 2:** Móc vào đúng điểm finalize PXH loại 15 (nơi loại 14 gọi ghi ngược `firm_contract_tab_products`); thêm chiều hoàn khi hủy PXH (`decrement`).
- [x] **Step 3:** Bảo đảm idempotent (cờ đã-ghi, hoặc tính từ trạng thái phiếu) — finalize lại không cộng lần 2.
- [x] **Step 4:** `php -l` sạch.
- [x] **Step 5:** Tinker: finalize PXH loại 15 → `exported_qty` combo tăng đúng; gọi lại không tăng thêm; hủy → trừ lại.

---

## Phase 5 — BE: hạch toán giá vốn loại 15

### Task 5.1: Nhánh loại 15 trong `getDataProductExportAccounting`

**Files:**
- Modify: `Modules/Assign/Services/ProductExportPostingService.php:268-309` (`getDataProductExportAccounting`)
- Tham chiếu ERP: `FirmContractProductExportService::getDataProductExportAccounting()` nhánh 15 (`:585-621`) → chỉ `costAccounting()` (`:666-679`), Nợ 632 / Có 1561.

**Interfaces:**
- Consumes: helper sẵn có `costAccounting(ProductExport $pxh, array &$accounts, int &$group, int $creditAcc)` (`:353`).

- [x] **Step 1:** Thêm `elseif ($type === ProductExportRequest::XUAT_KM_HD_HANG)` TRƯỚC nhánh `else` (`:304`):
  ```php
  } elseif ($type === ProductExportRequest::XUAT_KM_HD_HANG) { // 15: chỉ giá vốn Nợ632/Có1561
      $this->costAccounting($pxh, $accounts, $group, 1561);
  }
  ```
  (Tái dùng helper — `creditAcc=1561` cho ra: mỗi SP Có 1561 ref 632, tổng Nợ 632 ref 1561 = đúng ERP. Không doanh thu, không VAT, không support_accounting.)
- [x] **Step 2:** `php -l` sạch.
- [x] **Step 3:** Unit/tinker: dựng `ProductExport` type=15 có 2 SP (`export_price`, `qty`, `unit_coefficient`) → `getDataProductExportAccounting` trả `[true, accounts, '']` với đúng 2 vế Có 1561 (theo product) + 1 vế Nợ 632 = tổng, cân nợ-có. `export_price` lấy từ layer tồn (giá vốn), KHÔNG = 0 dù giá bán 0.

---

## Phase 6 — Verify e2e trọn chuỗi

### Task 6.1: Playwright chuỗi YCXH→ĐNXK→PXK→PXH loại 15

**Files:**
- Create/Modify: `e2e/tests/...` (bám bộ e2e sẵn có); chạy `cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test <spec>`.

- [x] **Step 1:** Tạo YCXH loại 15 từ `firm_contract_id=10626`: dropdown loại 15, chọn HĐ hãng, kho KM; bảng combo load giá 0; nhập SL ≤ còn-xuất; lưu nháp OK.
- [x] **Step 2:** Gửi duyệt: chặn đúng khi combo hết / HĐ hết hiệu lực / sai người lập / thiếu kho KM / SL vượt (báo đỏ dưới ô).
- [x] **Step 3:** Chạy tiếp ĐNXK → PXK → PXH; kiểm: trừ tồn **kho KM**, ghi ngược `exported_qty` về combo (truy DB local), bút toán **Nợ 632 / Có 1561** (không cụm doanh thu/VAT).
- [x] **Step 4:** Hồi quy nhanh loại 14/20/21 không vỡ (tạo 1 phiếu mỗi loại hoặc smoke API).
- [x] **Step 5:** Dọn rác test trên local nếu UI không tự xóa (bài học memory hrm-dnxk-cancel).

---

## Checkpoint

### Checkpoint — 2026-10-16 (khởi tạo plan)
Vừa hoàn thành: Brainstorming + spec (user duyệt) + plan chi tiết 6 phase.
Đang làm dở: chưa code task nào.
Bước tiếp theo: user review plan + chọn cách thực thi (subagent-driven / native) → bắt đầu Task 1.1.
Blocked: (trống)

### Checkpoint — 2026-10-16 ~17:45 (user yêu cầu dừng tạm)
Vừa hoàn thành:
- Phase 1–5 BE (hrm-api): bật tạo YCXH loại 15, endpoint kho KM, ĐNXK pass-through + ghi ngược `exported_qty` (D2), set `firm_contract_id` + combo tabs + in-flight guard (D3), hạch toán PXH Nợ632/Có1561 không doanh thu (E). Đều test tinker (transaction+rollback) trên HĐ10626 + review gộp APPROVED_WITH_NITS (0 Critical/Important).
- Phase 3 FE create (form loại 15) + Phase 3b FE detail readonly (hrm-client) + vá `show()` loại 15 (hrm-api). Review 3b APPROVED_WITH_NITS; Minor #1 (promo_warehouse_name) đã fix; #2/#3 ruling accept. Playwright màn Chi tiết THẬT (không mock) phiếu 39324: 5/5 field đúng, 0 console error.
Đang làm dở: KHÔNG — đang ở điểm dừng an toàn. Code CHƯA commit (hrm-api 4 file, hrm-client 3 file).
Bước tiếp theo (Phase 6 + final): (1) Playwright verify màn CREATE YCXH type15 + validate gửi duyệt + smoke regression 14/20/21; (2) final whole-branch review OPUS (loại trừ file session regulation-config); (3) dọn rác phiếu test 39324; (4) chờ user cho phép commit.
Blocked: (trống) — ledger chi tiết: scratchpad/sdd-type15/progress.md mục "ĐIỂM DỪNG".

### Checkpoint — 2026-10-16 (HOÀN TẤT TRỌN loại 15)
Vừa hoàn thành: TOÀN BỘ Phase 1–6.
- Phase 6 e2e đủ 4 bước: (1) tạo YCXH loại 15 từ UI Playwright POST 200 → PYCXH-39353 verify DB local; (2) validate gửi duyệt 7/7 guard PASS; (3) chuỗi ĐNXK→PXK→PXH verify tinker (ghi ngược exported_qty, in-flight, Nợ632/Có1561); (4) smoke show() 14/20/21/15/7/3 đều 200, nhánh dispatch đúng.
- Final whole-branch review OPUS: CHANGES_REQUESTED (0 Critical, 1 Important I-1, 3 Minor). I-1 (gate gửi duyệt loại 15 đếm nhầm chính phiếu khi update) ĐÃ FIX + VERIFY (t15-i1-fix.php) → re-review sonnet APPROVED 0 finding. 3 Minor ruling accept (M-3 verified resolved: ERP PXK đã copy combo id 149/149).
- Dọn rác test local XONG: xóa PYCXH-39324 + PYCXH-39353 (+ tab/tab_products/details), verify đã xóa. Chỉ DB local erp_hrm_check, KHÔNG đụng prod.
Đang làm dở: KHÔNG. Code CHƯA commit (hrm-api 8 file TYPE15 + FirmContractSearchModal đã commit 071da6eec; hrm-client 3 file TYPE15).
Bước tiếp theo: chờ user cho phép commit → sang LOẠI 4 (XUAT_TRA_NCC, nguồn ĐNNK).
Blocked: (trống).
