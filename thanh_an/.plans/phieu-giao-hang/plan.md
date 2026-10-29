# Phiếu giao hàng (giai đoạn 1) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> Người phụ trách: @khoipv · Bắt đầu: 28/10/2026
> Design: `.plans/phieu-giao-hang/design.md` · **Spec: `docs/superpowers/specs/2026-10-28-phieu-giao-hang-design.md`** (đọc cả spec trước khi làm task bất kỳ)

**Goal:** Đơn mua đã duyệt gửi được phiếu giao hàng cho bộ phận giao hàng; người có quyền `Giao/nhận hàng hóa` tiếp nhận / trả lại, người phụ trách cập nhật tiến độ + chi phí rồi Hoàn thành (chỉ đổi trạng thái phiếu).

**Architecture:** BE thêm 4 bảng + 4 entity + 1 service `PurchaseDeliveryNoteService` + 1 controller trong `Modules/Supply`. FE thêm màn danh sách + chi tiết `pages/supply/delivery_notes` (chuẩn V2 Cung ứng) và khối `DeliveryNoteBlock.vue` trên màn chi tiết đơn mua.

**Tech Stack:** PHP 7.4 / Laravel 8, MySQL · Nuxt 2 (Vue 2), Bootstrap-Vue, V2Base components.

## Global Constraints
- **Không commit / push git** (CLAUDE.md) — bước cuối mỗi task là đánh `[x]` ở plan này, không có bước commit.
- Migration **chỉ index, không khóa ngoại**.
- Quyền mới: id **526**, name/display_name **`Giao/nhận hàng hóa`**, group `Cung ứng`, type 7, guard `api`.
- Thông báo gửi / gửi lại phiếu → thành viên nhóm nghiệp vụ `group_permissions.name = 'Kho'` (`is_department = 1`, `status = 1`). Trả lại / hoàn thành → user `sent_by`.
- Status phiếu: `2` Chờ tiếp nhận · `3` Bị trả lại · `4` Đang xử lý · `5` Hoàn thành · `6` Đã hủy.
- Mã phiếu `PGH-<năm>-<####>` (cùng thuật toán `PurchaseOrderService::generateCode`).
- Hoàn thành **không** ghi gì về đơn mua; nút xác nhận tay trên đơn mua giữ nguyên.
- FE: đọc skill `list-page` (A), `modal-popup`, `form-validate`, `select-and-input-state`, `button-convention` (A) trước khi code. Label bắt buộc dùng `<Required />`. Ô lọc select chọn 1. Số từ API luôn ép `Number()` trước khi cộng (bẫy decimal → string).
- Không có `is_can_delete` / xóa phiếu, không phân quyền theo cấp, không xuất Excel.

## Cách kiểm BE (không có test suite — **không** dùng RefreshDatabase vì DB local là staging)
Mỗi task BE có script kiểm ở scratchpad `C:\Users\Admin\AppData\Local\Temp\claude\D--laragon-www-dns\10d39492-e034-42c7-bd6c-9e5c778126e2\scratchpad\pgh\`, bootstrap Laravel (`require vendor/autoload.php; $app = require bootstrap/app.php; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();`), toàn bộ chạy trong `DB::beginTransaction()` … `DB::rollBack()`, dùng `auth()->setUser(User::find(..))` để giả user, in `PASS`/`FAIL <tên>` cho từng assert. Chạy: `cd hrm-thanhan-api && php <script>`. Kỳ vọng: không có dòng `FAIL`.
Script dùng chung `_boot.php` (bootstrap + hàm `check(bool $ok, string $name)` + `makeOrder(array $opts): PurchaseOrder` tạo đơn status 3 với dòng hàng / purposes / điểm giao theo `$opts`).

## Review Focus
1. **Hai người bấm Tiếp nhận cùng lúc** → chỉ một người thành phụ trách, người sau 422 "đã được X tiếp nhận" — test `receive_twice` ở Task 3.
2. **Dòng `purposes` chỉ có tên khách, `customer_id` null** → vẫn khớp đúng điểm giao theo tên (trim) — test `remaining_match_by_name` ở Task 2.
3. **Đơn giao KH có dòng nội bộ (không có khách trong purposes)** → dòng đó không vào phiếu, không làm lỗi — test `remaining_skip_internal` ở Task 2.
4. **Không có nhóm `Kho` / nhóm rỗng** → gửi phiếu vẫn thành công, chỉ `Log::info` — test `send_without_kho_group` ở Task 2.
5. **Số lượng / tiền FE là chuỗi decimal** (`"11.000"`) → tổng Còn phải gửi, tổng chi phí cộng đúng số — kiểm ở Task 6/7 bước verify UI (`Number()`), BE ép `(float)` / `(int) round()`.

---

## Phase 0 — Thiết kế
- [x] 1. Đọc demo + spec demo + code đơn mua (điểm giao, purposes, quyền, thông báo, file)
- [x] 2. Viết spec + design tóm tắt; builder check; chốt thông báo nhóm Kho + Trả lại sau tiếp nhận + Hủy phiếu bị trả lại
- [x] 3. User duyệt spec → lên plan chi tiết (file này)

## Phase 1 — BE

### Task 1: Bảng, entity, quyền
**Files:**
- Create: `Modules/Supply/Database/Migrations/2026_10_28_000001_create_purchase_delivery_notes_tables.php` (4 bảng, cột đúng spec §4.1–4.4, `notes` có softDeletes, `code` unique, index theo spec)
- Create: `Modules/Supply/Database/Migrations/2026_10_28_000002_add_permission_giao_nhan_hang_hoa.php` (`DB::table('permissions')->insertOrIgnore([...id 526...])` + `app()[PermissionRegistrar::class]->forgetCachedPermissions()`; down xóa id 526)
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm dòng 526 sau 523, comment `// Phân hệ Cung ứng - Phiếu giao hàng`)
- Create: `Modules/Supply/Entities/PurchaseDeliveryNote.php`, `PurchaseDeliveryNotePoint.php`, `PurchaseDeliveryNoteItem.php`, `PurchaseDeliveryNoteCost.php`
- Modify: `Modules/Supply/Entities/PurchaseOrder.php` (thêm `deliveryNotes(): HasMany`)

**Interfaces — Produces:**
- `PurchaseDeliveryNote`: const `STATUS_WAITING=2, STATUS_RETURNED=3, STATUS_PROCESSING=4, STATUS_DONE=5, STATUS_CANCELED=6`, `OPEN_STATUSES=[2,4]`, `STATUSES` (id → tên), `PRIORITY_NORMAL=1, PRIORITY_URGENT=2`; quan hệ `purchaseOrder()`, `points()` (orderBy sort), `items()`, `costs()` (orderBy sort), `owner()`/`sender()` → `App\Models\User`; accessor `is_ncc` (`ship_method !== tu_lay`).
- `PurchaseDeliveryNotePoint`: `STATUS_WAITING=1, STATUS_DONE=2`, `ISSUE_REASONS` (`ncc_short` NCC giao thiếu · `damaged` Hỏng vỡ · `kh_reject` KH từ chối một phần · `wrong_spec` Sai quy cách · `other` Khác), `items()`.
- `PurchaseDeliveryNoteCost`: `COST_TYPES` (`rent, fuel, toll, parking, loading, allowance, other` → tên spec §4.4), `PAY_TO` (`self, vc, ncc`), cast `files => array`.
- Mọi entity `protected $guarded = []` như `PurchaseOrderProduct`.

- [x] **Step 1:** Viết migrations + seeder line + 4 entity + quan hệ `PurchaseOrder::deliveryNotes()`.
- [x] **Step 2:** `php -l` từng file mới → `No syntax errors`.
- [x] **Step 3:** `php artisan migrate` (local) → 2 migration chạy OK; `php artisan migrate:rollback --step=2` rồi `migrate` lại → OK (down chạy được).
- [x] **Step 4:** Script `pgh/t1_entities.php`: `check(Permission::find(526)->name === 'Giao/nhận hàng hóa', 'perm_526')`; tạo note + point + item + cost trong transaction, `check($note->points()->count()===1 && $note->costs->first()->files === [['link'=>'x','ten_file'=>'a.jpg']], 'relations_cast')` → không FAIL.
- [x] **Step 5:** Đánh `[x]`.

### Task 2: Còn phải gửi + Gửi / Gửi lại / Hủy
**Files:**
- Create: `Modules/Supply/Services/PurchaseDeliveryNoteService.php`

**Interfaces — Produces (service methods, mọi lỗi nghiệp vụ `throw new \Exception('<thông điệp tiếng Việt>')`, controller bắt → 400/422):**
- `generateCode(): string` — `PGH-<Y>-<####>`.
- `deliverablePairs(PurchaseOrder $order): array` — danh sách cặp `['key' => 'kho' | 'id:<cid>' | 'name:<tên>', 'delivery_point_id' => ?int, 'purchase_order_product_id' => int, 'qty' => float]`. Về kho: 1 cặp/dòng, `qty = order_qty`. Giao KH: từ `purposes[]` (khóa như `pointKeyOf` FE: `customer_id` ưu tiên, thiếu thì `trim(customer ?? customer_name)`; `qty = buyQty ?? qty`), cộng dồn theo (khóa, dòng), khớp `purchase_delivery_points` cùng khóa; **bỏ** cặp không khớp điểm nào và cặp thuộc điểm đã xác nhận tay (`status = 2`).
- `remainingPairs(PurchaseOrder $order, ?int $exceptNoteId = null): array` — như trên + `remaining = qty − Σ qty_delivered (note status 5) − Σ qty_plan (note status 2,4)`, làm tròn 3 số, chỉ giữ `remaining > 0`.
- `summary(PurchaseOrder $order): array` — `{lines:[{purchase_order_product_id, product_name, unit_name, order_qty, sending, delivered, remaining}], open_notes:[{id, code, status, owner_name}], returned_note: ?{id, code, return_reason, returned_by_name, returned_at, pickup_date, priority, note}, can_send: bool, cannot_send_reason: ?string}`.
- `send(PurchaseOrder $order, array $data): PurchaseDeliveryNote` — `$data = {pickup_date, priority, note}`; trong `DB::transaction` + `PurchaseOrder::lockForUpdate()->find()`; điều kiện spec §6.1; tạo note (snapshot `ship_method`, `dest`), points (kho: `warehouse_id`, `address = warehouse_address`; KH: snapshot từ `purchase_delivery_points`), items (snapshot `product_id/product_name/unit_name`, `qty_plan = remaining`); `notifyKho($note)`.
- `resend(PurchaseDeliveryNote $note, array $data): PurchaseDeliveryNote` — chỉ status 3; xóa points/items, tạo lại từ `remainingPairs`; hết SL → Exception `Đơn không còn số lượng cần gửi — hãy hủy phiếu`; status 2, `owner_id = null`; `notifyKho`.
- `cancel(PurchaseDeliveryNote $note): PurchaseDeliveryNote` — chỉ status 3 → 6, `canceled_by/at`.
- `notifyKho(PurchaseDeliveryNote $note): void` — try/catch; employee_info_ids từ nhóm Kho; rỗng → `Log::info`; `EmployeeInfoService::sendToAllNotification($ids, ['url' => '/supply/delivery_notes/'.$id, 'title' => 'Có phiếu giao hàng '.$code.' cần tiếp nhận', 'type' => 'purchaseDeliveryNote', 'id' => $id, 'employeeInfo' => <EmployeeInfo người gửi>])` (Timesheet `EmployeeInfoService`, cùng cách `PurchaseOrderService::sendNotification`).
- `notifySender(PurchaseDeliveryNote $note, string $title): void` — gửi tới `employee_info_id` của user `sent_by`.

- [x] **Step 1: Script kiểm** `pgh/t2_send.php` với các case (đơn tạo bằng `makeOrder`):
  - `remaining_kho`: đơn về kho 2 dòng (10, 5) → `remainingPairs` = 2 cặp `[10, 5]`.
  - `remaining_kh`: đơn giao KH, dòng A purposes khách 1 (6) + khách 2 (4), 2 điểm → 2 cặp `(id:1, A, 6)`, `(id:2, A, 4)`.
  - `remaining_match_by_name`: purposes `customer_id` null, `customer = ' BV X '`, điểm `customer_name = 'BV X'` → khớp 1 cặp.
  - `remaining_skip_internal`: đơn KH có dòng purposes rỗng → dòng đó không có cặp.
  - `remaining_skip_manual_point`: điểm `status = 2` → cặp của điểm đó bị bỏ.
  - `send_holds_qty`: `send()` lần 1 → note status 2, items `qty_plan` = 10/5; `remainingPairs` sau đó rỗng; `send()` lần 2 → Exception.
  - `send_requires_approved`: đơn status 2 → Exception.
  - `send_blocked_by_returned`: note status 3 tồn tại → `send()` Exception.
  - `resend_recalc`: note bị trả lại, một note khác đã giữ dòng 5 → `resend` tạo lại chỉ dòng 10.
  - `resend_empty`: không còn SL → Exception chứa `hãy hủy phiếu`.
  - `cancel_releases`: `cancel` note status 3 → status 6, `summary()['can_send'] === true`.
  - `remaining_after_short_delivery`: note status 5, item `qty_plan 10, qty_delivered 7` → remaining 3.
  - `send_without_kho_group`: đổi tạm tên nhóm Kho trong transaction → `send()` vẫn tạo phiếu.
- [x] **Step 2:** Chạy → FAIL (class chưa có).
- [x] **Step 3:** Viết các method trên trong `PurchaseDeliveryNoteService.php`.
- [x] **Step 4:** Chạy → không FAIL.
- [x] **Step 5:** Đánh `[x]`.

### Task 3: Tiếp nhận / Trả lại
**Files:** Modify `Modules/Supply/Services/PurchaseDeliveryNoteService.php`
**Interfaces — Produces:**
- `receive(PurchaseDeliveryNote $note): PurchaseDeliveryNote` — transaction + `lockForUpdate`; status ≠ 2 → Exception `Phiếu đã được <tên owner> tiếp nhận` (status 4/5) hoặc `Phiếu không còn ở trạng thái chờ tiếp nhận`; set `owner_id`, `received_at`, status 4.
- `returnNote(PurchaseDeliveryNote $note, string $reason): PurchaseDeliveryNote` — cho phép khi status 2, hoặc status 4 + owner = auth + `picked_at` null + không point nào status 2; → status 3, `return_reason`, `returned_by/at`, `owner_id = null`; `notifySender($note, 'Phiếu giao hàng <code> bị trả lại')`.
- `canReturn(PurchaseDeliveryNote $note): bool`, `isOwner(PurchaseDeliveryNote $note): bool` (dùng lại ở resource).

- [x] **Step 1:** Script `pgh/t3_receive.php`: `receive_ok` (status 4, owner = user A); `receive_twice` (user B gọi sau → Exception chứa tên A); `return_waiting` (status 2 → 3, owner null, qty nhả: `remainingPairs` có lại); `return_processing_ok` (owner A, chưa làm gì → 3); `return_processing_after_pick` (`picked_at` set → Exception); `return_not_owner` (user B trả phiếu A đang xử lý → Exception).
- [x] **Step 2:** Chạy → FAIL.
- [x] **Step 3:** Viết code.
- [x] **Step 4:** Chạy → không FAIL.
- [x] **Step 5:** Đánh `[x]`.

### Task 4: Lấy hàng, giao / nhận điểm, chi phí, hoàn thành
**Files:** Modify `Modules/Supply/Services/PurchaseDeliveryNoteService.php`
**Interfaces — Produces** (mọi method gọi `assertEditable($note)`: owner = auth và status 4, sai → Exception `Chỉ người phụ trách được cập nhật phiếu đang xử lý`):
- `pickup(PurchaseDeliveryNote $note, array $data): PurchaseDeliveryNote` — `$data = {items:[{id, qty_picked}], picked_at, pickup_note}`; NCC giao → Exception; đã có point status 2 → Exception `Sửa điểm đã giao trước khi sửa lấy hàng`; `0 ≤ qty_picked ≤ qty_plan`, ít nhất 1 > 0; thiếu → `pickup_note` bắt buộc.
- `deliverPoint(PurchaseDeliveryNote $note, PurchaseDeliveryNotePoint $point, array $data): PurchaseDeliveryNote` — `$data = {items:[{id, qty_delivered}], signer, delivered_at, issue_reason, issue_note}`; tự lấy: cần `picked_at`, cap = `qty_picked`; NCC giao: cap = `qty_plan`, ghi `qty_picked = qty_delivered`; thiếu (< `qty_plan`) → `issue_reason` bắt buộc, `other` → `issue_note` bắt buộc; `dest = kh` → `signer` bắt buộc; point status 2.
- `reopenPoint(PurchaseDeliveryNote $note, PurchaseDeliveryNotePoint $point)` — point về 1, xóa `qty_delivered` (NCC giao: cả `qty_picked`), `signer/delivered_at/issue_*`.
- `saveCosts(PurchaseDeliveryNote $note, array $data)` — `$data = {no_cost, costs:[{cost_type, description, amount, pay_to, files}]}`; xóa hết + insert lại; có dòng thì `no_cost = 0`.
- `complete(PurchaseDeliveryNote $note)` — kiểm spec §6.5, gom lỗi vào mảng → Exception message nối `; ` (controller trả 422 kèm `errors.missing = [...]`); status 5, `completed_at`, `has_diff`; `notifySender($note, 'Phiếu giao hàng <code> đã hoàn thành')`.
- `expectedCost(PurchaseOrder $order): int` — `tu_lay` → `self_cost`; khác → `ncc_fee + carrier_fee`.

Validate dạng field (`items.0.qty_picked`, `costs.1.amount`…) đặt ở FormRequest Task 5; service giữ các kiểm tra nghiệp vụ chéo (cap theo SL, lý do khi thiếu, điều kiện hoàn thành).

- [x] **Step 1:** Script `pgh/t4_progress.php`: `pickup_over` (qty_picked > plan → Exception); `pickup_short_needs_note`; `pickup_ncc_rejected`; `deliver_before_pick` (tu_lay → Exception); `deliver_cap_picked` (giao > thực lấy → Exception); `deliver_short_needs_reason`; `deliver_kh_needs_signer`; `deliver_ncc_sets_picked` (NCC giao: `qty_picked === qty_delivered`); `pickup_locked_after_deliver`; `reopen_point`; `costs_replace` (lưu 2 dòng rồi 1 dòng → còn 1, `no_cost` 0); `complete_missing` (chưa giao điểm + không chi phí → message chứa cả 2 mục); `complete_ok_has_diff` (giao thiếu 1 dòng → status 5, `has_diff` 1); `not_owner_blocked` (user B gọi `saveCosts` → Exception); `complete_does_not_touch_po` (status đơn mua + `purchase_delivery_points.status` không đổi).
- [x] **Step 2:** Chạy → FAIL.
- [x] **Step 3:** Viết code.
- [x] **Step 4:** Chạy → không FAIL.
- [x] **Step 5:** Đánh `[x]`.

### Task 5: API — danh sách, chi tiết, controller, routes
**Files:**
- Modify: `PurchaseDeliveryNoteService.php` — `getList(Request $request): Builder` (lọc spec §7, tab: `waiting`=2, `processing`=4, `mine`= owner auth + status 4, `done`=5, `returned`=3, `all`=mọi status), `tabCounts(Request $request): array` (cùng bộ lọc trừ tab, khóa = tên tab).
- Create: `Modules/Supply/Transformers/PurchaseDeliveryNote/PurchaseDeliveryNoteResource.php` (dòng danh sách: `id, code, status, status_name, has_diff, priority, ship_method, dest, purchase_order_id, purchase_order_code, supplier_name, destination_text, item_count, pickup_date (d/m/Y), owner_name, can_receive, can_return`) và `DetailPurchaseDeliveryNoteResource.php` (spec §7 dòng GET chi tiết; kèm `expected_cost`, `other_notes_cost` = Σ chi phí các phiếu khác của đơn trừ status 3/6, cờ `can_receive, can_return, can_edit, can_complete, is_owner`).
- Create: `Modules/Supply/Http/Requests/PurchaseDeliveryNote/SendDeliveryNoteRequest.php` (`pickup_date` required date, `priority` in:1,2, `note` nullable string), `ReturnDeliveryNoteRequest.php` (`reason` required), `PickupDeliveryNoteRequest.php`, `DeliverPointRequest.php`, `SaveCostsRequest.php` (rule field theo spec §6.4; message tiếng Việt).
- Create: `Modules/Supply/Http/Controllers/Api/V1/PurchaseDeliveryNoteController.php` (extends `ApiController`, cùng pattern `PurchaseOrderController`: try/catch → `responseJson($e->getMessage(), 400)`; `complete` lỗi điều kiện → 422 kèm `missing`).
- Modify: `Modules/Supply/Routes/api.php` — group `purchase-delivery-notes` (quyền theo bảng spec §7; show cho phép 526 **hoặc** 522 → kiểm trong controller bằng `auth()->user()->can(...)`) + 3 route dưới `purchase-orders/{purchaseOrder}`: `GET delivery-summary`, `POST delivery-notes` (522).

- [x] **Step 1:** `php -l` các file; `php artisan route:list --path=supply/purchase-delivery-notes` → đủ 11 route; `--path=delivery-summary` / `delivery-notes` → có.
- [x] **Step 2:** Script `pgh/t5_api.php` gọi qua HTTP kernel (`$app->make(Kernel::class)->handle(Request::create(...))` với `auth()->setUser`, transaction rollback): `list_tabs` (counts đúng sau khi tạo 1 phiếu 2 + 1 phiếu 4 của user A: `waiting=1, processing=1, mine=1`); `show_522_only` (user chỉ có 522 → 200); `show_no_perm` (→ 403); `send_validation` (thiếu `pickup_date` → 422 có key `pickup_date`); `complete_422_missing`.
- [x] **Step 3:** Chạy → không FAIL.
- [x] **Step 4:** Đánh `[x]`.

## Phase 2 — FE (`hrm-thanhan-client`)

### Task 6: Menu, hằng số, màn danh sách
**Files:**
- Modify: `utils/MenuSupply.js` — mục `{ label: 'Phiếu giao hàng', link: '/supply/delivery_notes', isShow: 'Giao/nhận hàng hóa' }` (cấp 1, sau nhóm *Mua hàng*).
- Create: `pages/supply/delivery_notes/constants.js` — `NOTE_STATUS`, `NOTE_STATUS_OPTIONS` (+ variant badge), `TABS` (`waiting, processing, mine, done, returned, all` + nhãn spec §8), `PRIORITY_OPTIONS`, `ISSUE_REASON_OPTIONS`, `COST_TYPE_OPTIONS`, `PAY_TO_OPTIONS` (`self` Công ty tự chi · `vc` Đơn vị vận chuyển · `ncc` NCC); `SHIP`/`DEST` import lại từ `pages/supply/purchase_orders/constants.js`.
- Create: `pages/supply/delivery_notes/index.vue` — theo skill `list-page` phần A, lấy `pages/supply/purchase_orders/index.vue` làm mẫu; middleware chặn quyền `Giao/nhận hàng hóa`; tab có số đếm từ `counts`; cột + bộ lọc spec §8; cột Thao tác: *Tiếp nhận* (`can_receive`, hỏi xác nhận) và *Trả lại* (`can_return`, popup lý do bắt buộc theo skill `modal-popup`) — dùng chung component `ReturnNoteModal.vue`.
- Create: `pages/supply/delivery_notes/components/ReturnNoteModal.vue` (V2BaseModal, textarea lý do `<Required />`, emit `submit(reason)`).

- [x] **Step 1:** Viết code.
- [x] **Step 2:** `npx eslint pages/supply/delivery_notes utils/MenuSupply.js` → không lỗi.
- [x] **Step 3:** Báo user test UI: menu hiện với quyền 526; tab đếm đúng; Tiếp nhận → phiếu sang tab Đang xử lý + Của tôi; Trả lại không nhập lý do → báo lỗi.
- [x] **Step 4:** Đánh `[x]`.

### Task 7: Màn chi tiết / cập nhật phiếu
**Files:**
- Create: `pages/supply/delivery_notes/_id/index.vue` — 1 trang theo demo (bản 28/10): thông tin phiếu → Tiến độ → Chi phí → footer. Banner *Chỉ xem — người phụ trách: X* khi `!is_owner && status 4`. Footer: status 2 → Trả lại / Tiếp nhận; status 4 + owner → Trả lại (khi `can_return`) / *Hoàn thành giao hàng*; còn lại chỉ Quay lại.
- Create: `pages/supply/delivery_notes/components/PickupBlock.vue` (chỉ `tu_lay`; bảng SL thực lấy, thời gian lấy, ghi chú khi thiếu; PUT `pickup`).
- Create: `pages/supply/delivery_notes/components/PointCard.vue` (1 điểm: hàng + SL yêu cầu / thực giao, lý do thiếu, người ký nhận khi KH, thời gian; nút *Xác nhận đã giao* / *Xác nhận kho đã nhận hàng* / *Xác nhận khách đã nhận hàng*; *Sửa* khi đã xác nhận).
- Create: `pages/supply/delivery_notes/components/CostTable.vue` (bảng nhiều dòng theo skill `form-validate`; mặc định `pay_to` theo spec §6.4; chọn `rent` → `vc`; upload file dùng component upload S3 có sẵn của dự án — tìm theo cách `supply_proposals` upload `files`; tổng + badge vượt / trong dự kiến (ẩn khi `expected_cost = 0`), dòng phụ "các phiếu khác"; tick "không phát sinh chi phí"; nút Lưu chi phí).
- Lỗi 422 từ API map vào ô theo skill `form-validate`; Hoàn thành thiếu điều kiện → toast liệt kê `missing`, tô đỏ dòng chi phí lỗi.

- [x] **Step 1:** Viết code.
- [x] **Step 2:** `npx eslint pages/supply/delivery_notes` → không lỗi.
- [x] **Step 3:** Báo user test UI cả 4 phương thức (`ncc_kho`, `ncc_kh`, `tu_lay` về kho, `tu_lay` giao KH): lấy hàng thiếu bắt ghi chú; giao thiếu bắt lý do; KH bắt người ký; Sửa điểm; chi phí cộng đúng số (không nối chuỗi); Hoàn thành thiếu điều kiện báo đủ mục; hoàn thành xong khóa sửa; user khác thấy banner chỉ xem.
- [x] **Step 4:** Đánh `[x]`.

### Task 8: Khối phiếu giao hàng trên đơn mua
**Files:**
- Create: `pages/supply/purchase_orders/components/DeliveryNoteBlock.vue` — props `orderId`; tự gọi `GET supply/purchase-orders/{id}/delivery-summary`; nút *Gửi bộ phận giao hàng* (disabled + `v-b-tooltip` = `cannot_send_reason`); banner đỏ khi `returned_note` (lý do, người trả, thời gian) + nút *Sửa & gửi lại* (mở cùng modal, điền sẵn) + *Hủy phiếu* (hỏi xác nhận); bảng tiến độ SL mua · Đang giao · Đã giao · Còn phải gửi; dòng ngắn các phiếu đang mở (mã link `/supply/delivery_notes/:id` + người phụ trách); tooltip ⓘ giải thích luồng.
- Create: `pages/supply/purchase_orders/components/SendDeliveryNoteModal.vue` — Hình thức vận chuyển (chỉ hiển thị), Ngày lấy hàng `<Required />` (vue2-datepicker), Ưu tiên (select chọn 1), Ghi chú; emit `submit({pickup_date, priority, note})`.
- Modify: `pages/supply/purchase_orders/_id/index.vue` — trong slot `#notice`, đặt `<DeliveryNoteBlock>` trên thẻ *Giao nhận hàng* khi `isEffective` và user có quyền 522 hoặc 526; nút gửi / sửa / hủy chỉ khi có 522.

- [x] **Step 1:** Viết code.
- [x] **Step 2:** `npx eslint` 3 file → không lỗi.
- [x] **Step 3:** Báo user test UI: đơn đã duyệt gửi được phiếu; gửi xong nút disabled "Đơn không còn số lượng cần gửi"; phiếu bị trả lại → banner + Sửa & gửi lại / Hủy; hủy xong gửi lại được; đơn chưa duyệt không hiện khối.
- [x] **Step 4:** Đánh `[x]`.

## Phase 3 — Wrap up
- [x] 9. Cập nhật checkpoint plan này, STATUS.md, `demos/README.md` (ghi demo đã lên bản thật giai đoạn 1).

### Sửa sau review cuối (opus, 28/10/2026)
- [x] C1 — Nhãn trạng thái sai do tra `STATUSES` theo chỉ số mảng → thêm `PurchaseDeliveryNote::statusInfo()/statusName()`, 2 Resource tra theo id (test `c1_status_label_2..6`)
- [x] I2 — 2 đơn gửi cùng lúc trùng mã phiếu → `send()` thử lại tối đa 3 lần khi lỗi 1062 trên cột `code` (test `i2_retry_dup_code`)
- [x] I3 — Gửi lại phiếu bị trả lại vẫn giữ chi phí / `no_cost` / lấy hàng của người phụ trách cũ → `resend()` xóa chi phí, reset `no_cost`, `picked_at`, `pickup_note` (test `i3_resend_clears_costs`, `i3_resend_clears_no_cost`)
- [x] M2 (nâng Important) — Link file chi phí nhận `javascript:` → rule `regex:/^https?:\/\//i` (test `m2_reject_js_link`, `m2_accept_https_link`)
- [x] I1 — Đang nhập dở chi phí / điểm giao / lấy hàng bị xóa khi khối khác lưu → watcher theo chữ ký dữ liệu riêng của từng khối (`serverSig`, `pointSig`, `pickupSig`); kiểm bằng vuecheck (không có test FE)
- Minor để sau: M1, M3, M4, M5, M6 (xem tin nhắn tổng kết)

### Checkpoint — 28/10/2026
Vừa hoàn thành: Task 0–8 + sửa C1/I1/I2/I3/M2 sau review; test BE t1..t6 ALL PASS (script trong scratchpad `pgh/`)
Đang làm dở: không
Bước tiếp theo: user chạy migration + seed quyền 526, test UI (4 phương thức + khối trên đơn mua + kịch bản I1), rồi tự commit 2 repo; giai đoạn 2 = bước 4 (Hoàn thành ghi về đơn mua)
Blocked:

## Phase 4 — Bỏ quyền `Giao/nhận hàng hóa` (user yêu cầu 28/10/2026)
> Menu Phiếu giao hàng ai cũng vào được; ai cũng tiếp nhận / trả lại / xử lý phiếu; thông báo vẫn chỉ gửi nhóm Kho. Gửi / sửa và gửi lại / hủy vẫn cần quyền `Lập đơn mua hàng`.
- [x] 10. BE: bỏ `checkPermission:Giao/nhận hàng hóa` ở route `purchase-delivery-notes/*` + `delivery-summary`; bỏ `PERM_HANDLE` trong service + DetailResource (`can_receive` / `can_return` không xét quyền)
- [x] 11. BE: xóa migration `2026_10_28_000002_add_permission_giao_nhan_hang_hoa` + dòng seeder id 526; gỡ quyền 526 khỏi DB local (chạy down + xóa dòng `migrations`)
- [x] 12. FE: menu bỏ `isShow`; khối phiếu giao hàng trên đơn mua hiện khi đơn đã duyệt (không xét quyền); bỏ `PERM_HANDLE` trong constants
- [x] 13. Chạy lại test t1..t6 + vuecheck; cập nhật spec / design

### Checkpoint — 28/10/2026 (Phase 4)
Vừa hoàn thành: Gỡ hẳn quyền `Giao/nhận hàng hóa` (526) — BE route / service / DetailResource / seeder / migration 000002 (đã down + xóa file); FE menu bỏ `isShow`, constants bỏ `PERM_HANDLE`, khối phiếu giao hàng trên đơn mua hiện khi đơn đã duyệt. Test t1..t6 ALL PASS (sửa test: list/show/receive không quyền → 200, cancel không 522 → 403); vuecheck OK; spec + design + STATUS đã cập nhật.
Đang làm dở: —
Bước tiếp theo: User test UI (gửi phiếu từ đơn DMH-2026-0001 → vào menu Phiếu giao hàng → tiếp nhận → cập nhật → hoàn thành) rồi tự commit. Sau đó giai đoạn 2 (Hoàn thành ghi về đơn mua).
Blocked:

## Phase 5 — Chuyển Phiếu giao hàng sang phân hệ Giao hàng (user yêu cầu 28/10/2026)
> Ô "Giao hàng" ở trang chủ / Topbar đang trỏ `#`. Chuyển màn FE sang prefix `/delivery`, menu riêng `MenuDelivery.js`. API BE giữ nguyên `/v1/supply/purchase-delivery-notes` (module Supply) — chỉ đổi link trong thông báo.
- [x] 14. FE: dời `pages/supply/delivery_notes` → `pages/delivery/delivery_notes`; sửa import tương đối, link, breadcrumb, `pathsToKeep`, khoá lưu bộ lọc / cột (`delivery_notes`)
- [x] 15. FE: tạo `utils/MenuDelivery.js`; bỏ mục khỏi `MenuSupply.js`; `layouts/default.vue` thêm nhánh `delivery`; ô Giao hàng ở `components/Topbar.vue` + `pages/index.vue` trỏ `/delivery/delivery_notes`
- [x] 16. FE: `purchase_orders` (DeliveryNoteBlock, SendDeliveryNoteModal) sửa import + link sang `/delivery/delivery_notes`
- [x] 17. BE: link thông báo `/supply/delivery_notes/{id}` → `/delivery/delivery_notes/{id}`; chạy lại test + vuecheck; cập nhật spec / design / STATUS

### Checkpoint — 2026-10-28 (Phase 5)
Vừa hoàn thành: chuyển Phiếu giao hàng sang phân hệ Giao hàng — `pages/delivery/delivery_notes` (URL `/delivery/delivery_notes`), `utils/MenuDelivery.js`, nhánh `delivery` trong `layouts/default.vue`, ô Giao hàng ở `Topbar.vue` + `pages/index.vue` trỏ màn danh sách, bỏ mục khỏi `MenuSupply.js`; khoá bộ lọc/cột đổi thành `delivery_notes`; link thông báo BE đổi sang `/delivery/delivery_notes/{id}`. API giữ `/v1/supply/purchase-delivery-notes`. Test t1–t6 ALL PASS, vuecheck OK.
Đang làm dở:
Bước tiếp theo: user test tay trên trình duyệt (hard refresh / chạy lại dev vì có thư mục pages mới); sau đó bước 4 — ghi kết quả giao về đơn mua.
Blocked:

## Phase 6 — Dashboard phân hệ Giao hàng (user yêu cầu 28/10/2026)
> Giống `pages/supply/dashboard` (trang khung, chưa có số liệu).
- [x] 18. FE: tạo `pages/delivery/dashboard/index.vue`; `MenuDelivery.js` thêm mục đầu "Tổng quan" → `/delivery/dashboard`; ô Giao hàng ở `Topbar.vue` + `pages/index.vue` trỏ `/delivery/dashboard/` (như ô Cung ứng)

### Checkpoint — 2026-10-28 (Phase 6)
Vừa hoàn thành: dashboard phân hệ Giao hàng `pages/delivery/dashboard/index.vue` (khung trống như Cung ứng); menu Giao hàng có "Tổng quan" đứng đầu; ô Giao hàng ở trang chủ / Topbar trỏ `/delivery/dashboard/`. vuecheck OK.
Đang làm dở:
Bước tiếp theo: user test tay; sau đó giai đoạn 2 — ghi kết quả giao về đơn mua.
Blocked:

## Phase 7 — Bỏ tab màn danh sách phiếu giao hàng (user yêu cầu 28/10/2026)
> Vào màn hiện TẤT CẢ phiếu, mới nhất trước (id desc, bỏ ưu tiên Gấp lên đầu); lọc trạng thái qua ô Trạng thái của bộ lọc.
- [x] 19. BE: bỏ `TABS` / `applyTab` / `tabCounts`, `getList` sắp `id desc`; controller bỏ `counts`; sửa test t5
- [x] 20. FE: bỏ `V2BaseTabNavigation`, `tab` khỏi bộ lọc, `counts`, `TABS` trong constants; cập nhật spec §7–8 / design

### Checkpoint — 2026-10-28 (Phase 7)
Vừa hoàn thành: bỏ tab màn danh sách phiếu giao hàng — BE `getList` trả tất cả, `orderByDesc(id)`, bỏ `TABS`/`applyTab`/`tabCounts` + `counts` ở controller; FE bỏ `V2BaseTabNavigation`, khoá `tab`, `counts`, `TABS`; lọc trạng thái qua ô Trạng thái. Test t5 thay case tab bằng `list_all_newest_first` / `list_ignores_tab` / `list_filter_status` — t1–t6 ALL PASS, vuecheck OK.
Đang làm dở:
Bước tiếp theo: user test tay; sau đó giai đoạn 2 — ghi kết quả giao về đơn mua.
Blocked:

## Phase 8 — Bỏ ô lọc Số dòng hàng (user yêu cầu 28/10/2026)
- [x] 21. FE: bỏ ô lọc `item_count` (field + slot + khoá từ/đến + ignoredFields); cột Số dòng hàng trên bảng giữ nguyên
- [x] 22. FE: bỏ ô lọc Chênh lệch (`has_diff`) — cờ Có chênh lệch ở cột Trạng thái giữ nguyên

### Checkpoint — 2026-10-28 (Phase 8)
Vừa hoàn thành: bỏ ô lọc Số dòng hàng (field, slot, khoá `item_count_*`, import V2BaseCurrencyInput) và ô lọc Chênh lệch (`has_diff`, `HAS_DIFF_OPTIONS`) ở màn danh sách phiếu giao hàng; cột Số dòng hàng + cờ Có chênh lệch ở cột Trạng thái giữ; BE không đổi (tham số `item_count_from/to` thừa, không ai gửi). vuecheck OK.
Đang làm dở:
Bước tiếp theo: user test tay; sau đó giai đoạn 2 — ghi kết quả giao về đơn mua.
Blocked:

## Phase 9 — Gọn màn chi tiết đơn mua đã duyệt (user yêu cầu 28/10/2026)
> Bỏ khối "Phiếu giao hàng" (tiến độ theo dòng) + khối "Giao nhận hàng / Chờ nhận hàng" (xác nhận tay); nút "Gửi bộ phận giao hàng" xuống V2Footer.
- [x] 23. FE `purchase_orders/_id/index.vue`: bỏ 2 khối; tự tải `delivery-summary`, nút Gửi bộ phận giao hàng ở `#custom-actions` của V2Footer (ẩn khi `can_send` false); phiếu bị trả lại → giữ thông báo lý do (như khối Lý do từ chối) + nút Sửa và gửi lại / Hủy phiếu ở footer; xoá `DeliveryNoteBlock.vue` (không còn ai dùng)

### Checkpoint — 2026-10-28 (Phase 9)
Vừa hoàn thành: màn chi tiết đơn mua bỏ khối Phiếu giao hàng + khối Giao nhận hàng (kèm nút xác nhận tay, modal xác nhận, style `po-recv`); nút Gửi bộ phận giao hàng ở `#custom-actions` V2Footer (ẩn khi `can_send` false); phiếu bị trả lại → banner lý do ở `#notice` + footer Sửa và gửi lại / Hủy phiếu; xoá `DeliveryNoteBlock.vue`; spec §9 + design cập nhật. vuecheck OK.
Đang làm dở:
Bước tiếp theo: user test tay; sau đó giai đoạn 2 — ghi kết quả giao về đơn mua.
Blocked:

## Phase 10 — Đổi nhãn "Hình thức vận chuyển" → "Phương thức giao hàng" (user yêu cầu 28/10/2026)
- [x] 24. FE: popup Gửi bộ phận giao hàng, chi tiết phiếu, cột + ô lọc màn danh sách phiếu đổi nhãn thành "Phương thức giao hàng" (khớp ShipTab đơn mua); key `ship_method` giữ nguyên

### Checkpoint — 2026-10-28 (Phase 10)
Vừa hoàn thành: đổi nhãn sang "Phương thức giao hàng" ở SendDeliveryNoteModal, `delivery_notes/_id`, `delivery_notes/index` (cột + bộ lọc). vuecheck OK.
Đang làm dở:
Bước tiếp theo: user test tay; sau đó giai đoạn 2 — ghi kết quả giao về đơn mua.
Blocked:

## Phase 11 — Gửi xong quay về danh sách đơn mua (user yêu cầu 28/10/2026)
- [x] 25. FE `purchase_orders/_id/index.vue`: popup Gửi bộ phận giao hàng / Sửa và gửi lại thành công → `router.push('/supply/purchase_orders')` (như Duyệt / Từ chối); gửi lỗi vẫn ở lại + tải lại delivery-summary

### Checkpoint — 2026-10-28 (Phase 11)
Vừa hoàn thành: gửi / gửi lại phiếu giao hàng thành công → quay về danh sách đơn mua. vuecheck OK.
Đang làm dở:
Bước tiếp theo: user test tay; chờ user chốt dữ liệu đơn DMH-2026-0001 thiếu ship_method (sửa data / chặn BE); sau đó giai đoạn 2.
Blocked:

## Phase 12 — Đơn mua đổi trạng thái khi gửi bộ phận giao hàng (user yêu cầu 29/10/2026)
> User chốt 29/10: tên **"Đã gửi giao hàng"** (id 7, `#2563EB`); hủy hết phiếu → về Đã duyệt; mọi báo cáo / điều kiện coi 7 như Đã duyệt.
- [x] 26. Chốt câu hỏi với user
- [x] 27. BE Entity `PurchaseOrder`: `STATUS_SENT_DELIVERY = 7`, `STATUSES`, `APPROVED_STATUSES` += 7, `DELIVERABLE_STATUSES` [3, 7], `is_can_confirm` dùng `DELIVERABLE_STATUSES`
- [x] 28. BE `PurchaseDeliveryNoteService`: `cannotSendReason` cho 3/7; `createNote` + `resend` → `markOrderSent` (3 → 7); `cancel` khóa đơn trước phiếu + `revertOrderIfNoNotes` (7 → 3 khi không còn phiếu chưa hủy)
- [x] 29. BE coi 7 như Đã duyệt: `SaleContractRemainService::LIVE_STATUSES`, `SupplyReportService::LIVE_DOC_STATUSES`, `PurchaseContractService` lịch sử giá (nguồn đơn mua)
- [x] 30. Migration `2026_10_29_000001_sync_purchase_order_sent_delivery_status` (đơn 3 có phiếu chưa hủy → 7) — đã chạy local: DMH-2026-0003 → 7
- [x] 31. FE `purchase_orders/constants.js`: `STATUS.SENT_DELIVERY`, `STATUS_OPTIONS` thêm "Đã gửi giao hàng"; `_id/index.vue` `isEffective` gồm 7
- [x] 32. Test `t7_order_status.php` 13/13 PASS; hồi quy t1–t6 ALL PASS; vuecheck OK
- [x] 33. Cập nhật spec §6.1 / §6.3b / §6.6 + design.md

### Checkpoint — 2026-10-29 (Phase 12)
Vừa hoàn thành: đơn mua có trạng thái 7 "Đã gửi giao hàng" — gửi phiếu thì 3 → 7, hủy hết phiếu thì về 3; báo cáo / điều kiện coi 7 như Đã duyệt. Test BE + vuecheck OK.
Đang làm dở:
Bước tiếp theo: user test tay; chờ user chốt dữ liệu đơn DMH-2026-0001 thiếu ship_method (sửa data / chặn BE); sau đó giai đoạn 2 (ghi kết quả giao về đơn mua — lúc đó đơn 7 → 6).
Blocked:

## Phase 13 — Nút "Gửi bộ phận giao hàng" ở màn danh sách đơn mua (user yêu cầu 29/10/2026)
> Dòng đơn gửi được (đơn 3/7, còn SL phải gửi, không có phiếu bị trả lại) + quyền Lập đơn mua hàng → cột Hành động có nút gửi, mở cùng popup `SendDeliveryNoteModal`. Phiếu bị trả lại vẫn xử lý ở màn chi tiết.
- [x] 34. BE `PurchaseDeliveryNoteService::canSend()` (public, bọc `cannotSendReason`; đơn ngoài 3/7 trả false không truy vấn)
- [x] 35. BE `PurchaseOrderResource`: thêm `is_can_send_delivery`, `ship_method`, `dest`
- [x] 36. FE `purchase_orders/index.vue`: action `send_delivery` (ri-send-plane-line) + `SendDeliveryNoteModal`; gửi xong tải lại danh sách
- [x] 37. Test BE t8 8/8 PASS + hồi quy t1–t7 ALL PASS; vuecheck OK; cập nhật spec §6.1

### Checkpoint — 2026-10-29 (Phase 13)
Vừa hoàn thành: nút "Gửi bộ phận giao hàng" ở cột Hành động danh sách đơn mua (cờ BE `is_can_send_delivery` theo `with_send_flag`, cùng popup `SendDeliveryNoteModal`).
Đang làm dở:
Bước tiếp theo: user test tay; chờ user chốt DMH-2026-0001 thiếu ship_method; giai đoạn 2 khi user yêu cầu.
Blocked:

## Phase 14 — Bỏ khối "Nhận tại kho công ty" ở form đơn mua (user yêu cầu 29/10/2026)
> Bỏ Kho nhận / Địa chỉ kho / Thủ kho tiếp nhận / Ngày giờ nhận khỏi form đơn mua — sang bên giao hàng người tiếp nhận cập nhật sau. Cột DB giữ nguyên (đơn cũ vẫn còn dữ liệu), chỉ bỏ nhập + bỏ bắt buộc.
- [x] 38. FE `ShipTab.vue`: xóa khối `dest === DEST.KHO` + dọn computed/method/prop không còn dùng
- [x] 39. FE `PurchaseOrderForm.vue`: bỏ truyền `warehouses` / nạp danh mục kho nếu chỉ phục vụ khối này
- [x] 40. BE `StorePurchaseOrderRequest`: `warehouse_id`, `receive_at` thôi bắt buộc khi giao về kho
- [x] 41. Kiểm: php -l, vuecheck, hồi quy t1–t8; cập nhật spec + STATUS

### Checkpoint — 2026-10-29 (Phase 14)
Vừa hoàn thành: bỏ khối "Nhận tại kho công ty" khỏi form đơn mua (`ShipTab.vue` xóa khối + `warehouseOptions`/`warehouse`/`keeperOptions`/`onWarehouse`/prop `warehouses`/`V2BaseDatePicker`; `PurchaseOrderForm.vue` thôi nạp danh mục kho); BE `warehouse_id`, `receive_at` thành nullable. Test t9 4/4 PASS + hồi quy t1–t8 ALL PASS; vuecheck OK.
Đang làm dở:
Bước tiếp theo: user test tay; hỏi user có cần ô nhập kho nhận / ngày giờ nhận ở màn phiếu giao hàng cho người tiếp nhận không (hiện chưa có); chờ user chốt DMH-2026-0001 thiếu ship_method.
Blocked:

## Phase 15 — Gọn tab Giao nhận đơn mua: bỏ Đơn vị VC nhận tiền, Người đi nhận hàng; khoản chi không bắt buộc (user yêu cầu 29/10/2026)
> "Bỏ cái Đơn vị vận chuyển nhận tiền", "chi phí vận chuyển không bắt buộc nhập" (bảng Các khoản chi), "Bên chịu phí vận chuyển vẫn bắt buộc", "Người đi nhận hàng cũng bỏ". Cột DB giữ nguyên (đơn cũ còn dữ liệu, form vẫn gửi lại giá trị cũ).
- [x] 42. FE `ShipTab.vue`: xóa ô "Đơn vị vận chuyển nhận tiền" (`carrier_name` + datalist `CARRIERS`), xóa ô "Người đi nhận hàng" (`pickup_employee_id`, prop `employees`, `employeeOptions`); nhãn "Các khoản chi" bỏ dấu bắt buộc
- [x] 43. FE `PurchaseOrderForm.vue`: `costs` mặc định rỗng (bỏ `ensureCosts`/`defaultCost` tự thêm dòng), thôi nạp danh sách nhân viên
- [x] 44. FE `PaymentTab.vue`: bỏ cột "Đơn vị nhận" ở khối chi phí trả đơn vị vận chuyển
- [x] 45. BE `StorePurchaseOrderRequest`: bỏ lỗi "thêm ít nhất một khoản chi" + lỗi `carrier_name`; `pickup_employee_id` nullable; dòng khoản chi đã thêm vẫn phải đủ tên / số tiền > 0 / nơi trả; `cost_payer` vẫn bắt buộc khi không tự lấy
- [x] 46. Kiểm: test t10 6/6 PASS (lần đầu FAIL do test dùng nhầm `cost_payer=1` — công ty chịu là 2), hồi quy t1–t9 ALL PASS, vuecheck 3 file OK

### Checkpoint — 2026-10-29 (Phase 15)
Vừa hoàn thành: bỏ "Đơn vị vận chuyển nhận tiền" (tab Giao nhận + cột "Đơn vị nhận" tab Thanh toán), bỏ "Người đi nhận hàng"; bảng Các khoản chi không bắt buộc; Bên chịu phí vẫn bắt buộc. Test t10 6/6 + t1–t9 PASS.
Đang làm dở:
Bước tiếp theo: user test tay; còn treo 2 câu: (1) có cần ô nhập kho nhận / ngày giờ nhận ở màn phiếu giao hàng không; (2) DMH-2026-0001 thiếu ship_method.
Blocked:

## Phase 16 — Bỏ cột "Số dòng hàng" ở danh sách phiếu giao hàng (user yêu cầu 29/10/2026)
- [x] 47. FE `pages/delivery/delivery_notes/index.vue`: xóa cột `item_count` + slot `#cell-item_count` (ô lọc đã bỏ ở Phase 8; BE vẫn trả `item_count`, không ảnh hưởng)
- [x] 48. Kiểm: vuecheck

### Checkpoint — 2026-10-29 (Phase 16)
Vừa hoàn thành: bỏ cột Số dòng hàng ở danh sách phiếu giao hàng.
Đang làm dở:
Bước tiếp theo: user test tay; còn treo 2 câu (ô kho nhận ở màn phiếu giao hàng; DMH-2026-0001 thiếu ship_method).
Blocked:

## Phase 17 — Badge Phương thức giao hàng phân biệt NCC giao về kho / giao thẳng KH (user góp ý 29/10/2026)
> User: "có NCC giao tại kho cty và NCC giao thẳng cho khách mà? bạn để mỗi NCC giao thì sao phân biệt được?" — `shipBadge` gộp `ncc_kho` + `ncc_kh` thành "NCC giao".
- [x] 49. FE `delivery_notes/constants.js`: `shipBadge` tách 3 nhãn — NCC giao về kho (#0EA5E9) · NCC giao thẳng KH (#2563EB) · Cty tự lấy (#7C3AED)
- [x] 50. FE `delivery_notes/_id/index.vue`: badge hiện đủ tên phương thức (bỏ chữ lặp sau badge)
- [x] 51. Kiểm: vuecheck

### Checkpoint — 2026-10-29 (Phase 17)
Vừa hoàn thành: badge phương thức giao hàng ở danh sách + chi tiết phiếu giao hàng phân biệt 3 phương thức.
Đang làm dở:
Bước tiếp theo: user test tay; còn treo 2 câu (ô kho nhận ở màn phiếu giao hàng; DMH-2026-0001 thiếu ship_method).
Blocked:

## Phase 18 — Màn chi tiết phiếu giao hàng dùng base chung V2 (user góp ý 29/10/2026)
> User: "delivery/delivery_notes/396 UI bạn chưa sử dụng các base chung của v2 à?" + "phần này Phiếu giao hàng PGH-2026-0002 để dạng v2baseinput như đơn mua hàng cho tôi chứ?"
- [x] 52. FE `_id/index.vue`: khối thông tin `dn-info` tự dựng → `row` + `col-md-4 form-col` với `V2BaseLabel` + `V2BaseInput disabled` (như GeneralTab đơn mua); Ghi chú → `V2BaseTextarea disabled`
- [x] 53. FE `_id/index.vue`: footer tự dựng → `V2Footer` (nút Tiếp nhận / Hoàn thành / Trả lại ở `#custom-actions`); câu nhắc chuyển lên banner
- [x] 54. FE bảng `dn-table` (index + PointCard + PickupBlock + CostTable) → bọc `V2BaseTableScroll` + class `v2-form-table`; bỏ `.dn-cost-wrap`
- [x] 55. Kiểm: vuecheck

### Checkpoint — 2026-10-29 (Phase 18)
Vừa hoàn thành: màn chi tiết phiếu giao hàng — khối thông tin đổi sang V2BaseLabel + V2BaseInput disabled (9 ô col-md-4: Đơn mua hàng [icon mở đơn], Nhà cung cấp, Phương thức giao hàng, Ngày lấy hàng [badge Gấp], Người gửi, Ngày gửi, Người phụ trách, Ngày tiếp nhận, Tổng số lượng) + Ghi chú cung ứng V2BaseTextarea disabled; footer → V2Footer (Tiếp nhận / Hoàn thành giao hàng / Trả lại cung ứng ở #custom-actions, Quay lại do V2Footer lo); câu nhắc chuyển thành banner; 5 bảng bọc V2BaseTableScroll + v2-form-table. vuecheck OK, grep HTML thô sạch.
Đang làm dở:
Bước tiếp theo: user test tay /delivery/delivery_notes/396; còn treo 2 câu (ô kho nhận ở màn phiếu giao hàng; DMH-2026-0001 thiếu ship_method).
Blocked:

## Phase 19 — Gọn khối thông tin chi tiết phiếu giao hàng (user yêu cầu 29/10/2026)
> User: "bỏ cái trạng thái Đang xử lý, Gấp, Tổng số lượng, chỗ ngày gửi bỏ giờ đi cho tôi"
- [x] 56. FE `_id/index.vue`: bỏ badge trạng thái trên tiêu đề khối (giữ badge "Có chênh lệch"); bỏ badge Gấp cạnh Ngày lấy hàng; bỏ ô Tổng số lượng (+ computed allItems/totalQty/productCount, PRIORITY)
- [x] 57. FE `_id/index.vue`: ô Ngày gửi chỉ hiện ngày (computed `sentDate` cắt phần giờ của `H:i d/m/Y`; BE giữ nguyên)
- [x] 58. Kiểm: vuecheck

### Checkpoint — 2026-10-29 (Phase 19)
Vừa hoàn thành: bỏ badge trạng thái + Gấp + ô Tổng số lượng; Ngày gửi bỏ giờ.
Đang làm dở:
Bước tiếp theo: user test tay; còn treo 2 câu (ô kho nhận ở màn phiếu giao hàng; DMH-2026-0001 thiếu ship_method).
Blocked:

## Phase 20 — Ô "Thời gian nhận/giao" từng điểm chỉ lấy ngày (user yêu cầu 29/10/2026)
> User: "chỗ thời gian nhận bỏ giờ đi cho tôi"
- [x] 59. FE `constants.js`: thêm `fmtDate` (DD/MM/YYYY) + `todayDate` (YYYY-MM-DD)
- [x] 60. FE `PointCard.vue`: nhãn "Thời gian nhận/giao" → "Ngày nhận/giao"; V2BaseDatePicker bỏ `type="datetime"`, value-type `YYYY-MM-DD`, format `DD/MM/YYYY`; mặc định hôm nay; dữ liệu cũ cắt 10 ký tự; dòng tóm tắt "Nhận lúc HH:mm…" → "Ngày nhận: dd/mm/yyyy"
- [x] 61. BE `DeliverPointRequest`: câu lỗi "Thời gian…" → "Ngày giao / nhận…" (rule `date` giữ nguyên, cột vẫn timestamp, lưu 00:00:00)
- [x] 62. Kiểm: vuecheck + php -l

### Checkpoint — 2026-10-29 (Phase 20)
Vừa hoàn thành: ô ngày giao/nhận từng điểm chỉ chọn ngày.
Đang làm dở:
Bước tiếp theo: user test tay; còn treo 2 câu (ô kho nhận ở màn phiếu giao hàng; DMH-2026-0001 thiếu ship_method).
Blocked:

## Phase 21 — Tiêu đề card thông tin → "Thông tin chung" (user yêu cầu 29/10/2026)
- [x] 63. FE `_id/index.vue`: tiêu đề V2BaseFormSection "Phiếu giao hàng {code}" → "Thông tin chung" (mã phiếu vẫn ở PageHeader/breadcrumb; giữ badge "Có chênh lệch")

### Checkpoint — 2026-10-29 (Phase 21)
Vừa hoàn thành: đổi tiêu đề card thông tin.
Đang làm dở:
Bước tiếp theo: user test tay; hỏi user có bỏ giờ ở ô Ngày tiếp nhận không; còn treo 2 câu (ô kho nhận; DMH-2026-0001 thiếu ship_method).
Blocked:

## Phase 22 — Ô Đơn mua hàng: bỏ icon, mã đơn là link như danh sách (user yêu cầu 29/10/2026)
- [x] 64. FE `_id/index.vue`: bỏ icon ri-external-link-line ở nhãn; ô giữ khung V2BaseInput disabled, mã đơn là `nuxt-link.v2-cell-link` đặt đè vào vị trí chữ (class `.dn-link-field`); bỏ CSS `.dn-label-link`
- [x] 65. Kiểm: vuecheck

### Checkpoint — 2026-10-29 (Phase 22)
Vừa hoàn thành: ô Đơn mua hàng hiện mã đơn dạng link.
Đang làm dở:
Bước tiếp theo: user test tay; còn hỏi: bỏ giờ ở Ngày tiếp nhận?; ô kho nhận; DMH-2026-0001 thiếu ship_method.
Blocked:

## Phase 23 — Khoảng cách dòng khối Thông tin chung (user báo 29/10/2026)
- [x] 66. FE `_id/index.vue`: thêm `.form-col { margin-bottom: 10px }` (scoped) giống GeneralTab đơn mua — trước đó các dòng ô dính sát
- [x] 67. Skill `form-validate` mục 1c: ghi quy tắc lưới ô `row` + `col-md-4 form-col` phải tự khai margin 10px; màn chi tiết chỉ xem dựng bằng V2Base* disabled; ô tham chiếu là link `v2-cell-link` (mẫu `.dn-link-field`)
- [x] 68. Kiểm: vuecheck

### Checkpoint — 2026-10-29 (Phase 23)
Vừa hoàn thành: khoảng cách dòng ô thông tin + cập nhật skill form-validate.
Đang làm dở:
Bước tiếp theo: user test tay; còn hỏi: bỏ giờ ở Ngày tiếp nhận?; ô kho nhận; DMH-2026-0001 thiếu ship_method.
Blocked:

## Phase 24 — Kho nhận ở phiếu giao hàng + Ngày tiếp nhận bỏ giờ (user yêu cầu 29/10/2026)
Quyết định: ô Kho nhận nhập ở thẻ điểm "Kho công ty" khi xác nhận nhận / bàn giao kho (bắt buộc) — người tiếp nhận cập nhật, đúng lý do đã bỏ khối kho khỏi đơn mua (Phase 14). Khối Thông tin chung có ô Kho nhận chỉ xem (chỉ hiện khi hàng về kho). Danh mục kho dùng lại `GET supply/purchase-orders/warehouses` (chỉ auth); kho đã khóa mà điểm đang dùng thì FE tự chèn option để không mất giá trị.
- [x] 69. BE entity `PurchaseDeliveryNotePoint::warehouse()`; controller detail load `points.warehouse`; resource trả `warehouse_name`
- [x] 70. BE `DeliverPointRequest` + `deliverPoint()`: điểm về kho bắt buộc `warehouse_id` (kho tồn tại, đang hoạt động hoặc đúng kho đang lưu) → lưu `warehouse_id` + snapshot `address`; sửa câu lỗi "Thời gian" → "Ngày giao / nhận"
- [x] 71. FE `PointCard.vue`: select Kho nhận (bắt buộc) ở điểm kho; tên điểm = tên kho; gửi `warehouse_id`
- [x] 72. FE `_id/index.vue`: ô Kho nhận (chỉ xem) ở Thông tin chung; tên điểm ở khối Lộ trình = tên kho; Ngày tiếp nhận bỏ giờ
- [x] 73. Kiểm: php -l, test BE, vuecheck

### Checkpoint — 29/10/2026 (Phase 24)
Vừa hoàn thành: Kho nhận chọn ở thẻ điểm kho khi xác nhận (bắt buộc, lưu kèm địa chỉ kho); Thông tin chung có ô Kho nhận chỉ xem; Ngày tiếp nhận bỏ giờ. php -l OK; test t11_warehouse 8/8 PASS; t4/t5 cập nhật thêm `warehouse_id` → ALL PASS; vuecheck OK
Đang làm dở:
Bước tiếp theo: user test UI
Blocked:

## Phase 25 — Màn chi tiết phiếu giao hàng cùng khung với đơn mua hàng (user yêu cầu 29/10/2026)
User: "màn phiếu giao hàng này tôi thấy vẫn chưa đúng với màn đơn mua hàng về card các thứ?"
Ruling: lấy khung `PurchaseOrderForm.vue` làm chuẩn — banner trạng thái nằm TRÊN card (như khối lý do từ chối), 1 card `tp-card p-0` chứa `V2BaseTabNavigation` + thân tab + `V2Footer`. Tab mặc định = Thông tin chung (giống đơn mua). Giữ tiêu đề section "Thông tin chung" theo yêu cầu cũ của user.
- [x] 74. FE `_id/index.vue`: banner (Bị trả lại / chỉ xem / Hoàn thành / câu nhắc / còn thiếu) chuyển lên trên card, kiểu vạch màu trái 4px như `.po-reject-notice`
- [x] 75. FE `_id/index.vue`: 1 card có tab — Thông tin chung · Lộ trình và hàng hóa (chưa tiếp nhận) / Tiến độ giao hàng (đang xử lý, hoàn thành) · Chi phí (chỉ khi đã tiếp nhận); tab đang chọn mất thì về Thông tin chung
- [x] 76. Kiểm: vuecheck OK; icon tab có trong remixicon 2.4

### Checkpoint — 29/10/2026 (Phase 25)
Vừa hoàn thành: màn chi tiết phiếu giao hàng chuyển sang 1 card có tab giống chi tiết đơn mua hàng
Đang làm dở:
Bước tiếp theo: user test UI; hỏi có đổi tiêu đề section thành "Thông tin phiếu giao hàng" (khỏi trùng tên tab) không
Blocked: DMH-2026-0001 thiếu `ship_method` — chờ user chọn sửa dữ liệu test hay chặn ở BE

## Phase 26 — Bỏ tab, xếp dọc các khối (user yêu cầu 29/10/2026)
User: "thôi cho tab dọc cho tôi đi, vì nó ít thông tin"
Ruling: hiểu là bỏ thanh tab, các khối Thông tin chung → Lộ trình và hàng hóa / Tiến độ giao hàng → Chi phí xếp dọc trong cùng 1 card (giữ banner trên card + V2Footer cuối card như Phase 25).
- [x] 77. FE `_id/index.vue`: gỡ `V2BaseTabNavigation`, `TAB`, `activeTab`, `tabs`, `currentTab`; các khối hiện cùng lúc theo thứ tự dọc
- [x] 78. Kiểm: vuecheck

### Checkpoint — 29/10/2026 (Phase 26)
Vừa hoàn thành: màn chi tiết phiếu giao hàng bỏ tab, các khối xếp dọc trong 1 card
Đang làm dở:
Bước tiếp theo: user test UI
Blocked: DMH-2026-0001 thiếu `ship_method` — chờ user quyết

## Phase 27 — Bỏ khối "Còn thiếu để hoàn thành" (user yêu cầu 29/10/2026)
Ruling: chỉ gỡ khối cảnh báo trên màn chi tiết; BE vẫn chặn Hoàn thành khi thiếu, bấm nút thì toast "Chưa thể hoàn thành: …" như cũ.
- [x] 79. FE `_id/index.vue`: gỡ banner `detail.missing`
- [x] 80. Kiểm: vuecheck

### Checkpoint — 29/10/2026 (Phase 27)
Vừa hoàn thành: bỏ khối "Còn thiếu để hoàn thành" ở màn chi tiết phiếu
Đang làm dở:
Bước tiếp theo: user test UI
Blocked: DMH-2026-0001 thiếu `ship_method` — chờ user quyết

## Phase 28 — Thu gọn thanh tiêu đề khối (user yêu cầu 29/10/2026, Screenshot_6)
Nguyên nhân: `_type.scss` đặt `h6 { margin: 10px 0 }`; `V2BaseFormSection` chỉ có `mb-0` nên tiêu đề vẫn cách trên 10px → thanh tiêu đề cao thừa.
Ruling: ghi đè trong màn (`::v-deep .v2-form-section > .section-header h6 { margin-top: 0 }`), không sửa component dùng chung khi chưa hỏi.
- [x] 81. FE `_id/index.vue`: bỏ margin-top của tiêu đề khối
- [x] 82. Kiểm: vuecheck

### Checkpoint — 29/10/2026 (Phase 28)
Vừa hoàn thành: thu gọn thanh tiêu đề các khối ở màn chi tiết phiếu giao hàng
Đang làm dở:
Bước tiếp theo: user test UI; hỏi có sửa luôn ở `V2BaseFormSection` (dùng chung) không
Blocked: DMH-2026-0001 thiếu `ship_method` — chờ user quyết

## Phase 29 — Xem trước file đính kèm chi phí (user yêu cầu 29/10/2026)
Ruling: dùng lại `FilePreviewModal` + `openFilePreviewModal` (utils/file-preview) như Phiếu xử lý cung ứng / FileTable đề xuất; bấm tên tệp mở popup xem trước thay vì mở tab mới. Phiếu giao hàng chỉ có file ở bảng Chi phí.
- [x] 83. FE `CostTable.vue`: tên tệp thành nút mở `FilePreviewModal` (kèm icon con mắt)
- [x] 84. Kiểm: vuecheck

### Checkpoint — 29/10/2026 (Phase 29)
Vừa hoàn thành: bấm tệp đính kèm ở bảng Chi phí mở popup xem trước
Đang làm dở:
Bước tiếp theo: user test UI
Blocked: DMH-2026-0001 thiếu `ship_method` — chờ user quyết

## Phase 30 — Hoàn thành xong quay về danh sách (user yêu cầu 29/10/2026)
- [x] 85. FE `_id/index.vue` `doComplete()`: thành công → toast + về `/delivery/delivery_notes` (giống Gửi bộ phận giao hàng ở đơn mua)
- [x] 86. Kiểm: vuecheck

### Checkpoint — 29/10/2026 (Phase 30)
Vừa hoàn thành: Hoàn thành phiếu giao hàng xong quay về màn danh sách
Đang làm dở:
Bước tiếp theo: user test UI
Blocked: DMH-2026-0001 thiếu `ship_method` — chờ user quyết

### Checkpoint — 29/10/2026 (wrap up sau Phase 30)
Vừa hoàn thành: Phase 24–30 (Kho nhận, bố cục 1 card xếp dọc, bỏ khối "Còn thiếu", thu gọn tiêu đề khối, xem trước tệp chi phí, Hoàn thành về danh sách). Đã cập nhật STATUS.md + spec mục 6 (Kho nhận) và mục 8 (bố cục màn chi tiết).
Đang làm dở: không
Bước tiếp theo: user test UI màn `/delivery/delivery_notes/:id` → trả lời câu treo → commit (migration `2026_10_28_000001` + `2026_10_29_000001`) → giai đoạn 2 (Hoàn thành ghi kết quả về đơn mua) khi user yêu cầu
Blocked: chờ user quyết — (a) sửa `V2BaseFormSection` dùng chung bỏ margin-top h6 cho mọi màn? (b) Trả lại phiếu xong có quay về danh sách không? (c) DMH-2026-0001 thiếu `ship_method`: sửa dữ liệu test / chặn BE / cả hai?

### Checkpoint — 29/10/2026 (đã push)
Vừa hoàn thành: commit + push nhánh `thanhan-dev` theo yêu cầu user — API `74bc1144`, Client `70c6e001`
Đang làm dở: không
Bước tiếp theo: chạy 2 migration trên server; giai đoạn 2 khi user yêu cầu
Blocked: câu treo (a)(b)(c) ở checkpoint trên

## Phase 31 — Bỏ khối "Chi phí vận chuyển" ở form đơn mua (user yêu cầu 29/10/2026)
Quyết định (Claude, theo cách làm Phase 14): chỉ ẩn khối ở FE (cả Bên chịu phí + bảng Các khoản chi). Chi phí thật nhập ở phiếu giao hàng. Đơn cũ đã có `cost_payer` / `costs` → form vẫn giữ và gửi lại khi sửa, không mất dữ liệu, tiền thanh toán NCC của đơn cũ không đổi. Đơn mới: không có khoản chi → ncc_fee/carrier_fee/self_cost = 0.
- [x] 87. FE `ShipTab.vue`: gỡ khối Chi phí vận chuyển + code/prop/import/style chỉ khối đó dùng
- [x] 88. FE `PurchaseOrderForm.vue`: gỡ binding cost của ShipTab + 3 handler onCostPayerChange/onCostAdded/onCostRemoved
- [x] 89. BE `StorePurchaseOrderRequest`: `cost_payer` thôi bắt buộc (nullable, giữ rule `in`) — không còn ô để hiện lỗi
- [x] 90. Kiểm: vuecheck + php -l + test lưu đơn ncc_kho không gửi cost_payer

### Checkpoint — 29/10/2026 (Phase 31)
Vừa hoàn thành: bỏ khối Chi phí vận chuyển ở form đơn mua (ShipTab gỡ template + prop/import/style thừa; Form gỡ binding + 3 handler, vẫn giữ `costs`/`selfCosts`/`feeTotals` + payload cho đơn cũ); BE `cost_payer` nullable. vuecheck OK, php -l OK, test t12 7/7 PASS. Spec mục 6 đã ghi.
Đang làm dở: không
Bước tiếp theo: user test UI tạo / sửa đơn mua (tab Giao nhận) rồi tự commit (Client: ShipTab.vue, PurchaseOrderForm.vue; API: StorePurchaseOrderRequest.php)
Blocked: câu hỏi treo (a) sửa `V2BaseFormSection` chung, (b) Trả lại phiếu có về danh sách không, (c) DMH-2026-0001 thiếu `ship_method`

## Phase 32 — Cho nhập VAT ở bảng hàng hóa đơn mua, giống HĐ mua (user yêu cầu 29/10/2026)
Quyết định (Claude): làm y kiểu HĐ mua. Ô VAT (%) nhập tay 0–100, dòng mới gợi ý sẵn theo danh mục (`products.tax`); dòng đã lưu giữ số đã nhập, danh mục không đè nữa. Dòng lấy theo HĐ mua thì khóa ô VAT (giống ô Đơn giá/CK), lấy theo VAT của dòng HĐ. BE ưu tiên số FE gửi, không gửi mới lấy theo danh mục. Không sửa trait dùng chung `CalculatesPurchaseLineMoney`, chỉ thêm hàm riêng trong `PurchaseOrderService`.
- [x] 91. BE `PurchaseOrderService`: thêm `orderLineVat()` (ưu tiên `vat_percent` FE gửi), dùng ở `calcTotalAmount` + `syncProducts`
- [x] 92. BE `StorePurchaseOrderRequest`: rule `products.*.vat_percent` nullable|numeric|min:0|max:100 + message giống HĐ mua
- [x] 93. FE `purchase_orders/components/ProductsTab.vue`: ô VAT thành `V2BaseInput` (giống HĐ mua), `vatOf` ưu tiên giá trị đã có, thêm `onVatInput`, style ô
- [x] 94. Kiểm: vuecheck + php -l + test BE lưu đơn có VAT tự nhập, VAT > 100 bị 422, dòng không gửi VAT lấy theo danh mục
- [x] 95. Rà lại (user "check kỹ"): đổi hàng / bỏ đổi hàng phải xóa `vat_percent` để gợi ý lại VAT theo hàng mới (giống HĐ mua `ProductsTab.vue:1739,1755`) — trước đây taxMap luôn đè nên không lộ
- [x] 96. Rà tiếp BE: Resource/Transformer đơn mua có tính lại VAT theo `tax` không; dòng theo HĐ mua có bị ép giá/VAT ở BE không

### Checkpoint — 29/10/2026 (Phase 32)
Vừa hoàn thành: cột VAT (%) bảng hàng hóa đơn mua thành ô nhập tay (V2BaseInput 0–100, giống HĐ mua). Dòng mới gợi ý theo danh mục, dòng đã lưu giữ số đã nhập, dòng theo HĐ mua khóa. BE `orderLineVat()` ưu tiên số FE gửi (không gửi → theo danh mục) ở cả tổng tiền đơn lẫn lưu dòng; rule + message `products.*.vat_percent` giống HĐ mua. vuecheck OK, php -l OK, test t13 11/11 PASS.
Rà lại (task 95–96): sửa lỗi đổi hàng / bỏ đổi hàng giữ VAT hàng cũ → nay xóa `vat_percent` để gợi ý lại theo hàng mới (giống HĐ mua). BE: Resource trả đúng VAT đã lưu, chỉ form lưu đơn gọi `calcTotalAmount`/`syncProducts`; dòng theo HĐ mua chỉ khóa ở FE (BE không ép giá / CK / VAT theo HĐ — như trước, chưa đổi). t12 + t13 PASS, vuecheck OK.
Đang làm dở: không
Bước tiếp theo: user test UI tạo / sửa đơn mua (cột VAT, đổi hàng) rồi tự commit (Client: ProductsTab.vue + 2 file Phase 31; API: PurchaseOrderService.php, PurchaseContractService.php (chỉ sửa comment), StorePurchaseOrderRequest.php)
Blocked: câu hỏi treo (a) sửa `V2BaseFormSection` chung, (b) Trả lại phiếu có về danh sách không, (c) DMH-2026-0001 thiếu `ship_method`

## Phase 33 — Chọn HĐ mua ở đơn mua chờ lâu + nút chọn hàng đổi chậm (user báo 29/10/2026)

Nguyên nhân (đo local): `GET contract-pool/{id}` ~13 s, 2,3 MB — kèm `extras` = 3.815 dòng hàng HĐ bán chưa đề xuất toàn công ty (`unproposedActiveContractGoods()` ~5 s + `SaleContractRemainService` gắn SL còn lại cho cả 3.815 dòng). Nút "Chọn hàng từ nhu cầu mua / HĐ mua" đọc `pool` nên chỉ đổi chữ khi API này về. Index `product_package_informations.product_id` thử tạm: không cải thiện rõ → bỏ.

- [x] 97. BE `PurchaseOrderSourceService::contractPool()`: bỏ tính `extras` (chỉ form đơn mua gọi endpoint này)
- [x] 98. FE `GoodsPickerModal`: chế độ theo HĐ → hiện ngay dòng HĐ, nạp `unproposed-goods` khi mở popup (như chế độ đơn lẻ), lọc bỏ mã đã có trong HĐ, chặn kết quả cũ khi đóng/mở lại
- [x] 99. FE `PurchaseOrderForm.loadPool`: cờ `poolLoading` + chặn kết quả cũ khi đổi HĐ liên tục; `ProductsTab` nút chọn hàng đổi chữ ngay theo HĐ đang chọn, khóa trong lúc tải
- [x] 100. Kiểm: đo lại contract-pool, vuecheck, php -l, test BE pool không còn extras

### Checkpoint — 29/10/2026 (Phase 33)
Vừa hoàn thành: task 97–100. Đo lại (HĐ #3): `contract-pool` 13 s / 121 query / 2,3 MB → **60 ms / 6 query / 2 KB** (không còn key `extras`). FE: `PurchaseOrderForm` có `poolLoading` + `poolSeq` (đổi HĐ liên tục chỉ nhận kết quả HĐ cuối); `ProductsTab` nút chọn hàng đổi chữ ngay theo `form.purchase_contract_id`, khóa + spinner khi đang tải; `GoodsPickerModal` chế độ theo HĐ hiện ngay dòng HĐ, nạp ngầm `unproposed-goods` (lọc mã đã có trong HĐ, như BE cũ) kèm dòng "Đang tải thêm hàng HĐ bán chưa đề xuất...", `loadSeq` bỏ kết quả của lượt mở cũ. php -l OK, vuecheck 3 file OK, EOL bình thường.
Đang làm dở: không
Bước tiếp theo: user test UI chọn HĐ mua ở form đơn mua. Còn chậm ~5–6 s khi mở popup chọn hàng (cả 2 chế độ) do `PurchaseContractService::unproposedActiveContractGoods()` — hàm dùng chung (popup HĐ mua cũng gọi) → chờ user đồng ý mới tối ưu.
Blocked: 

### Checkpoint — 29/10/2026 (wrap up)
Vừa hoàn thành: Phase 31 (bỏ chi phí vận chuyển ở form đơn mua), Phase 32 (VAT nhập tay + rà lại), Phase 33 (chọn HĐ mua nhanh, nút chọn hàng đổi ngay) — tất cả task `[x]`. Đã commit + push `thanhan-dev` theo yêu cầu user (API 26004c34, Client 9ec82dc2).
Đang làm dở: không
Bước tiếp theo: user test UI đơn mua (tạo / sửa / chi tiết: không còn khối chi phí vận chuyển, ô VAT, chọn / đổi HĐ mua, popup chọn hàng theo HĐ) → user tự commit. Chờ trả lời: tối ưu `unproposedActiveContractGoods()` dùng chung; BE có tự áp VAT dòng HĐ không; sửa comment `utils/purchase-pricing.js:96`.
Blocked: 
