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
