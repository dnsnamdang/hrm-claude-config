# Plan — YCXH loại "Xuất bán hàng" (type 14) + chuẩn hoá Lưu nháp

> **Cho người thực thi:** đọc kèm spec `docs/superpowers/specs/gop-db/2026-10-05-ycxh-xuat-ban-hang-type14-design.md`.
> Nhánh `gop_db` (CẢ `hrm-api` + `hrm-client`). Verify bằng `php -l` / tinker read-only / Playwright
> `http://127.0.0.1:3000` (module này KHÔNG có unit-test harness). Đánh `[x]` mỗi bước khi xong.

**Mục tiêu:** Mở loại 14 "Xuất bán hàng" (nguồn HĐ hãng `firm_contracts`) tạo được phiếu YCXH, và cho
Lưu nháp mọi loại chỉ cần chọn "Loại yêu cầu".

**Kiến trúc:** BE mở `CREATABLE_TYPE_IDS`, nới `rulesForType()` nháp, thêm nhánh `createData()` +
`createFromFirmContract()` đọc `firm_contract_tab_products` (mô phỏng mẫu 20/21). FE thêm nhóm loại 14,
modal chọn HĐ hãng, nạp dòng, nới `validateForm` nháp.

**Nhánh:** `gop_db` · **Người phụ trách:** @namdangit

## Global Constraints (từ CLAUDE.md — áp cho MỌI task)

- **Nhánh `gop_db`:** KHÔNG `DB_CONNECTION_SECOND`/`mysql2`; bảng trùng tên ưu tiên bản ERP; không migration mới.
- **Hàm dùng chung:** sửa/tách hàm đang dùng ở màn khác → **HỎI user trước** (áp cho T6 nếu đụng service sẵn có).
- **BE validate:** FormRequest/`validate()` chỉ khai `rules()`, KHÔNG khai `messages()` (dùng lang vi sẵn);
  rethrow `ValidationException` (không catch `Exception` chung).
- **FE validate:** chỉ trường **Tên** gắn `required` ở FE; required khác do BE trả 422 → map `formError`.
  Lưu nháp KHÔNG được chặn trường ngoài "Loại yêu cầu".
- **FE component:** mọi element form dùng `V2Base*`; select trong modal dùng `V2BaseSelectInModal`;
  nút trong `V2Footer`; popup trên `V2BaseModal`/`base-confirm-modal`.
- **Cờ quyền fail-closed:** mặc định `false`, KHÔNG hard-code `= true`.
- **Nút không dùng được → ẨN (`v-if`/`visible`), không disable.**
- **Số:** chuẩn quốc tế `1,234,567.89` (FE `toLocaleString('en-US')`, BE `number_format`).
- **Không tự sửa giá trị user nhập;** vượt trần báo đỏ dưới ô, giữ nguyên số.
- **KHÔNG commit/push** khi chưa có yêu cầu.

---

## Phase 1 — Chuẩn hoá Lưu nháp (mọi loại chỉ cần "Loại yêu cầu")

### T1 — [BE] `rulesForType()`: nháp không đòi HĐ (20/21) + loại 19 giữ nguyên

**File:** `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php`
(hàm `rulesForType`, khối `$isContract` dòng ~536-542).

- [ ] **B1.** Trong khối `if ($isContract) { if (!$isUpdate) {...} }`, đổi:
  ```php
  // CŨ:
  $rules['emplement_contract_id'] = 'required|integer|exists:hrm_contracts,id';
  // MỚI (nháp nullable, gửi duyệt required — đồng bộ cách loại 19 làm ở ~dòng 551-554):
  $rules['emplement_contract_id'] = ($isDraft ? 'nullable' : 'required')
      . '|integer|exists:hrm_contracts,id';
  ```
  (Giữ nguyên `is_export_direct`/`need_repair` nullable trong khối này.)
- [ ] **B2.** `php -l` file controller → không lỗi cú pháp.
- [ ] **B3.** Verify tinker read-only (DB local): gọi `(new ...Controller)` không khả thi vì cần Request;
  thay bằng kiểm bằng Playwright ở T15 (nháp 20/21 không còn 422 đòi HĐ). Ghi chú: chưa chạy được ở T1.

### T2 — [FE] `validateForm()`: nháp mọi loại chỉ cần "Loại yêu cầu"

**File:** `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue`
(hàm `validateForm(status)` ~dòng 1566).

- [ ] **B1.** Bọc khối đòi HĐ loại HĐ để CHỈ chạy khi KHÔNG nháp. Hiện tại (~1576-1583):
  ```js
  if (this.isContractType && !this.form.emplement_contract_id) { /* set lỗi */ return false }
  // ...
  if (isDraft) return true
  ```
  Sửa thành: đưa `if (isDraft) return true` LÊN NGAY SAU kiểm `type`, trước mọi kiểm nguồn; HOẶC
  đổi điều kiện khối HĐ thành `if (!isDraft && this.isContractType && !this.form.emplement_contract_id)`.
  Chọn cách 2 (ít xáo trộn thứ tự nhất).
- [ ] **B2.** Đảm bảo nhánh `isDraft` chỉ còn yêu cầu `this.form.type` (dòng ~1571 giữ nguyên).
- [ ] **B3.** Verify Playwright (gộp ở T15): nháp loại 20/21 + 14 chỉ cần chọn loại → lưu được.

---

## Phase 2 — Loại 14: Backend

### T3 — [BE] Mở loại 14 ở `store()`

**File:** `hrm-api/Modules/Assign/Entities/Warehouse/ProductExportRequest.php` (`CREATABLE_TYPE_IDS` ~dòng 73-82).

- [ ] **B1.** Thêm `self::XUAT_BAN_HD_HANG` (14) vào mảng `CREATABLE_TYPE_IDS` (append cuối, giữ thứ tự cũ).
- [ ] **B2.** `php -l` → sạch.
- [ ] **B3.** Verify: `store()` loại 14 không còn trả 422 "Loại yêu cầu không được phép tạo." (kiểm ở T15).

### T4 — [BE] `rulesForType()` khối loại 14

**File:** controller `rulesForType()` (sau khối loại 19, trước khối `$isDraft` return).

- [ ] **B1.** Thêm biến đầu hàm: `$isFirmContract = $type === ProductExportRequest::XUAT_BAN_HD_HANG;`
- [ ] **B2.** Thêm khối (áp cả nháp & gửi duyệt, chỉ khi `!$isUpdate` cho `firm_contract_id`):
  ```php
  if ($isFirmContract) {
      if (!$isUpdate) {
          $rules['firm_contract_id'] = ($isDraft ? 'nullable' : 'required')
              . '|integer|exists:firm_contracts,id';
      }
      $rules['is_export_direct'] = 'nullable|boolean';
      $rules['need_repair'] = $isDraft ? 'nullable|in:0,1' : 'required|in:0,1';
  }
  ```
- [ ] **B3.** Trong khối gửi duyệt không-transfer (~583-591), cho loại 14 cũng đòi `contract_product_id`:
  đổi `if ($isContract)` thành `if ($isContract || $isFirmContract)` cho rule
  `$rules['products.*.contract_product_id'] = 'required|integer'`.
- [ ] **B4.** Thêm vào khối gửi duyệt rule riêng loại 14:
  ```php
  if ($isFirmContract) {
      $rules['firm_tab_vat_percent'] = 'required|numeric';
      $rules['warehouse_id'] = 'required_unless:is_export_direct,1|nullable|integer';
  }
  ```
- [ ] **B5.** `php -l` → sạch.

### T5 — [BE] Xác minh cấu trúc `firm_contracts` + `firm_contract_tab_products`

**Mục đích:** chốt tên cột thật trước khi viết query (ERP khác HRM; cột KH/giá/qty có thể khác mẫu 20/21).

- [ ] **B1.** `grep DB_ hrm-api/.env` xác nhận đang trỏ DB local (theo memory `erp-local-env-points-to-prod-db`).
- [ ] **B2.** Tinker read-only: `DB::table('firm_contracts')->first()` và
  `DB::table('firm_contract_tab_products')->first()` → ghi lại tên cột thật vào plan (B3).
- [ ] **B3.** Chốt map cột (điền sau khi chạy B2):
  - KH trên `firm_contracts`: `customer_id` / `customer_name` / `customer_tax_code` /
    `customer_address` / `customer_contact_name` / `customer_contact_phone` (xác nhận).
  - Dòng `firm_contract_tab_products`: `firm_contract_id`, `parent_id`(tab), `product_id`, `unit_id`,
    `quantity`, `standard_price`, `net_price`, `sale_max_percent`, `vat_percent` (xác nhận).
  - Trạng thái hiệu lực HĐ hãng: hằng `CO_HIEU_LUC` = ? (tra `ERP .../FirmContract.php` + entity HRM
    `Modules/Finance/Entities/Contract/FirmContract.php` SELECTABLE_STATUSES=[3,9,10]).
  - **Enum in-flight HRM** (đối chiếu, có thể khác ERP `[2,7,10,11]` / `!=3,5` / `=2`): xác nhận với
    `product_export_requests`, `warehouse_export_request_tab_products`, `borrow_sell_request_tab_products`.

### T6 — [BE] Service SL-còn-xuất cho HĐ hãng (trừ in-flight 3 nguồn + quỹ cha-con)

**File:** `hrm-api/Modules/Assign/Services/FirmContractExportStockService.php` *(tạo mới)* —
nơi DUY NHẤT đọc 3 bảng in-flight cho HĐ hãng; docblock liệt kê "Nơi đang dùng".

> ⚠️ Trước khi tạo mới: `grep -rn "borrow_sell_request_tab_products\|warehouse_export_request_tab_products"
> hrm-api/Modules/*/Services/` xem đã có service tính SL-còn-xuất HĐ hãng chưa (vd
> `PrepickExportContractService`). Nếu có hàm tái dùng được nhưng đang `private`/khoá → **HỎI user**
> trước khi tách (Global Constraints).

- [ ] **B1.** `remainingByContractProduct(int $firmContractId, ?int $excludeRequestId = null): array`
  trả `[contract_product_id => ['needed','exported','in_flight','remaining']]`:
  - `needed` = SUM `firm_contract_tab_products.quantity` theo dòng.
  - `exported` = SUM `product_export_request_tab_products.qty` join `product_export_requests` where
    `tp.emplement_contract_id=$id AND tp.type=14 AND r.status != STATUS_DA_HUY_PHIEU`,
    `whereNotNull contract_product_id` (loại trừ `$excludeRequestId` nếu có).
  - `in_flight` = tổng 3 nguồn (dùng enum chốt ở T5-B3):
    (1) `product_export_request_tab_products` need_export + status đang xử lý;
    (2) `warehouse_export_request_tab_products` status đang chạy;
    (3) `borrow_sell_request_tab_products` status đang mượn.
  - `remaining` = `max(0, needed - exported - in_flight)` **sau quỹ cha-con** (B2).
- [ ] **B2.** Quỹ cha-con: port `calcChildAwareRemaining()` / `getInFlightQtyByKey()`
  (ERP `FirmContractProductExportService` :437, :501) — SL con bị chặn bởi SL còn của cha.
- [ ] **B3.** `php -l` → sạch. Verify tinker: gọi với 1 `firm_contract_id` thật, so số với màn ERP
  `getDataForWarehouseExport` cùng HĐ (read-only, KHÔNG ghi DB).

### T7 — [BE] `createData()` nhánh type=14

**File:** controller `createData(Request)` (~dòng 326-370) + hàm mới `firmContractProductLines()`.

- [ ] **B1.** Thêm nhánh: `if ($type === 14 && $request->filled('firm_contract_id'))`:
  - `$fc = DB::table('firm_contracts')->find($fcId);` → `contract` snapshot (id, code, customer_name,
    tax_code, contact_name, contact_phone, address — theo map T5-B3).
  - `product_lines` = `$this->firmContractProductLines($fcId)`.
  - `vat_options` = các mức `vat_percent` distinct trong `firm_contract_tab_products` của HĐ.
  - vẫn trả `warehouses` + `transition_types`.
- [ ] **B2.** Viết `firmContractProductLines(int $firmContractId, ?int $excludeRequestId = null): array`
  (mô phỏng `contractProductLines()` ~376-428, đổi nguồn sang HĐ hãng): join units/product_models/brands,
  ghép `remaining` từ `FirmContractExportStockService` (T6). Trả mỗi dòng: `contract_product_id`,
  `parent_id`, `code`, `name`, `model_name`, `brand_name`, `unit_id`, `unit_name`, `product_id`,
  `qty_needed`, `exported_qty`, `in_flight_qty`, `remaining_qty`, `contract_qty`, `quoted_price`
  (standard_price), `unit_price_after_discount` (net_price), `vat_percent`.
- [ ] **B3.** `php -l` → sạch.

### T8 — [BE] `createFromRequest()` dispatch 14 → `createFromFirmContract()`

**File:** `hrm-api/Modules/Assign/Services/ProductExportRequestService.php`
(`createFromRequest` ~281-304; thêm hàm `createFromFirmContract`).

- [ ] **B1.** Trong `createFromRequest()`, thêm nhánh TRƯỚC nhánh 20/21:
  ```php
  if ($type === ProductExportRequest::XUAT_BAN_HD_HANG) {
      $model = $this->createFromFirmContract($data);
  } elseif (in_array($type, [XUAT_SAN_XUAT_HOP_DONG, XUAT_BAN_HOP_DONG], true)) { ... }
  ```
- [ ] **B2.** Viết `createFromFirmContract(array $data): ProductExportRequest` (mô phỏng
  `createFromContract` ~665-730 + `writeContractLines` ~738-819, đọc `firm_contract_tab_products`):
  - Tạo `product_export_requests`: `type=14`, `status` theo input, code `PYCXH-{id}`, `firm_contract_id`,
    `warehouse_id` (null nếu export_direct), `is_export_direct`, `need_repair`, `transition_type`
    (fallback 1), `total_km_expected`, customer_* copy từ `firm_contracts` (map T5-B3), tổ chức + created_by.
  - 1 tab đại diện (`product_export_request_tabs`): `emplement_contract_id=firm_contract_id`,
    `emplement_contract_type` = FirmContract class (hoặc null — chốt ở T5/T8 theo cách tab lưu),
    `name` = code HĐ.
  - Ghi `product_export_request_tab_products` + `product_export_request_details` cho mỗi dòng chọn
    (`products[]` → qty theo user; không gửi → tất cả qty = needed). Map giá: niêm yết=standard_price,
    sau giảm=net_price, vat=vat_percent.
- [ ] **B3.** `php -l` → sạch.

### T9 — [BE] Business-check khi Gửi duyệt loại 14 (2 check thiết yếu)

**File:** `createFromFirmContract()` (chỉ chạy khi `status == CHO_DUYET`/2).

- [ ] **B1.** Check 1 — `canProductExport`: HĐ hãng `status == CO_HIEU_LUC` **và**
  `firm_contracts.created_by == auth()->id()`. Sai → `throw ValidationException::withMessages([...])`
  (message nghiệp vụ: "Hợp đồng không còn hiệu lực hoặc bạn không phải người lập hợp đồng.").
- [ ] **B2.** Check 2 — SL-còn-xuất: với mỗi dòng chọn, `qty <= remaining_qty`
  (từ `FirmContractExportStockService`, truyền `excludeRequestId` khi sửa). Vượt →
  `ValidationException` nêu rõ SP/dòng (giữ nguyên số user nhập).
- [ ] **B3.** Thêm comment TODO rõ ràng cho 3 check phụ SKIP (bật lại sau):
  ```php
  // TODO(gop_db ycxh-type14): bật lại 3 check phụ khi port đủ —
  // (1) hạn mức công nợ khách; (2) lệch giá xuất vs giá HĐ; (3) support_accounting.
  ```
- [ ] **B4.** `php -l` → sạch. Verify ở T15 (Playwright: vượt SL / HĐ hết hiệu lực / sai người lập đều chặn).

### T10 — [BE] (nếu cần) endpoint liệt kê HĐ hãng đủ điều kiện cho FE chọn

- [ ] **B1.** Kiểm xem đã có endpoint liệt kê `firm_contracts` dùng được cho FE chưa
  (`grep -rn "firm-contracts\|firmContracts" hrm-api/Modules/Assign/Routes`). Có → tái dùng, bỏ qua T10.
- [ ] **B2.** Chưa có → thêm `GET assign/firm-contracts` (search server-side, limit, trả id+code+customer_name,
  lọc HĐ của người đăng nhập + còn hiệu lực) + route. `php -l` sạch.

---

## Phase 3 — Loại 14: Frontend

### T11 — [FE] Nhóm loại 14 + computed

**File:** `ProductExportRequestForm.vue` (consts ~841-847, computed `isSaleType` ~1001).

- [ ] **B1.** Thêm `const FIRM_CONTRACT_TYPES = [14]` cạnh `CONTRACT_TYPES`.
- [ ] **B2.** Thêm computed `isFirmContractType() { return FIRM_CONTRACT_TYPES.includes(Number(this.form.type)) }`.
- [ ] **B3.** `isSaleType`: thêm 14 → bật cột giá. Kiểm `DELIVERY_TYPES`/`showExportDirect` đã gồm 14 chưa
  (BE `getHasDeliveryTypes()` có 14) → nếu thiếu, thêm 14 để hiện khối vận chuyển.

### T12 — [FE] Modal chọn HĐ hãng

**File:** `hrm-client/pages/finance/product-export-requests/components/FirmContractSearchModal.vue` *(mới)*
— clone `ContractSearchModal.vue`, đổi endpoint sang HĐ hãng (T10) + nhãn "Chọn hợp đồng hãng".

- [ ] **B1.** Clone cấu trúc `ContractSearchModal.vue`; select trong modal dùng `V2BaseSelectInModal`;
  popup trên `V2BaseModal`.
- [ ] **B2.** Gọi endpoint HĐ hãng (search server-side có `limit`, debounce ≥300ms — Global Constraints
  hiệu năng). Emit `select(contract)`.
- [ ] **B3.** Grep kiểm pattern đã có (`grep -rn "V2BaseSelectRemote\|ContractSearchModal" hrm-client/pages/finance`)
  để bám đúng khuôn, ghi "copy pattern từ <file:dòng>".

### T13 — [FE] Nạp dòng loại 14 + nhóm VAT + `need_repair`

**File:** `ProductExportRequestForm.vue` (`loadContractLines`/`buildContractLines` ~1311-1338 làm mẫu).

- [ ] **B1.** `loadFirmContractLines()`: `GET assign/product-export-requests/create-data?type=14&firm_contract_id=<id>`.
- [ ] **B2.** `buildFirmContractLines()`: dựng bảng dòng (STT, checkbox "Cần xuất", Tên+Thương hiệu, Model,
  Mã, ĐVT, Hợp đồng/Đã xuất/Đang xuất/Còn được xuất/Đề nghị, giá niêm yết/bán/thành tiền/giảm/VAT/sau VAT).
  Số format `toLocaleString('en-US')`. Ô "Đề nghị" vượt `remaining_qty` → báo đỏ dưới ô, KHÔNG tự kéo về max.
- [ ] **B3.** Nhóm theo VAT (`firm_tab_vat_percent`): select mức VAT → lọc dòng tab tương ứng.
- [ ] **B4.** Radio "Cần lắp đặt" (`need_repair` 0/1), CHỈ hiện khi `isFirmContractType` (dùng `V2Base*`).
- [ ] **B5.** Bảng tràn ngang bọc `V2BaseTableScroll` (Global Constraints).

### T14 — [FE] `onTypeChange()` xử lý loại 14

**File:** `ProductExportRequestForm.vue` (`onTypeChange` ~1218).

- [ ] **B1.** Khi đổi sang 14 → reset `firm_contract_id` + dòng hàng, hiện khối chọn HĐ hãng, ẩn khối HĐ HRM.
- [ ] **B2.** Khi rời khỏi 14 → ẩn khối HĐ hãng + radio `need_repair`.
- [ ] **B3.** `onContractSelected` cho loại 14 → gọi `loadFirmContractLines()`.

---

## Phase 4 — Verify

### T15 — Playwright (`http://127.0.0.1:3000`) + php -l tổng

- [ ] **B1.** Đảm bảo API `:8000` + client `:3000` chạy; MCP mở `http://127.0.0.1:3000` (không `localhost`).
- [ ] **B2.** KB1: Loại 14 + chỉ chọn loại + Lưu nháp → phiếu "Đang tạo", KHÔNG toast đỏ.
- [ ] **B3.** KB2: Loại 20/21 + chỉ chọn loại + Lưu nháp → lưu được, không đòi HĐ.
- [ ] **B4.** KB3: Loại 14 chọn HĐ hãng → dòng hàng tự nạp, "Còn được xuất" đúng (so màn ERP).
- [ ] **B5.** KB4: Loại 14 Gửi duyệt — SL vượt → chặn; HĐ hết hiệu lực → chặn; sai người lập → chặn;
  hợp lệ → "Chờ duyệt".
- [ ] **B6.** `php -l` lại toàn bộ file BE đã sửa.

---

## Self-review (writing-plans) — đã rà

- **Spec coverage:** §1-9 của spec đều có task (nháp→T1/T2; mở store→T3; rule 14→T4; cột→T5; SL→T6;
  createData→T7; service tạo→T8; check→T9; endpoint→T10; FE→T11-T14; verify→T15). ✅
- **Placeholder:** không có TBD; chỗ "xác minh cột" đã thành task T5 có bước tinker cụ thể. ✅
- **Type consistency:** `firmContractProductLines()`, `FirmContractExportStockService::remainingByContractProduct()`,
  `createFromFirmContract()`, `FIRM_CONTRACT_TYPES`/`isFirmContractType` dùng nhất quán giữa các task. ✅
- **Phụ thuộc:** T6→T7/T9 (service SL); T5→T6/T7/T8 (tên cột). Thứ tự task đã phản ánh.

### Checkpoint — 2026-10-05
Vừa hoàn thành: viết design + spec + plan chi tiết (15 task, 4 phase) + STATUS entry; đọc xác nhận
code anchor (`createFromContract`/`writeContractLines`, `rulesForType`, dispatcher).
Đang làm dở: (không có — chưa code)
Bước tiếp theo: user chọn cách thực thi (subagent-driven / inline) → bắt đầu T1.
Blocked: (không có)
