---
name: entity-history
description: Use when làm tính năng "lịch sử thay đổi / lịch sử chỉnh sửa / audit log ai sửa gì, giá trị cũ → giá trị mới, lúc nào" cho một màn/entity ở dns (hrm-thanhan) — thêm lịch sử cho phiếu / danh mục mới, sửa cách hiển thị, thêm mục Lịch sử ở ⋮ danh sách hoặc khối Lịch sử ở màn chi tiết / popup Xem.
---

# Entity History (Lịch sử thay đổi) — bản dns

> Port từ skill `entity-history` của hrm (`hrm-claude-config/hrm/.claude/skills/entity-history/` — đọc
> `SKILL.md` + `ui-base.md` bên đó khi cần lý do gốc của từng quy tắc). Bản dns ghi theo **code đã chạy
> thật** ở phân hệ Kho (26/11/2026, spec `docs/superpowers/specs/2026-11-26-lich-su-thay-doi-kho-design.md`).

⚠️ Hai chiều đừng nhầm: trong 1 dòng log là **cũ (đỏ) → mới (xanh)**; thứ tự danh sách luôn **MỚI → CŨ**.

## 0. Chốt với user trước khi code

1. **Track trường nào?** Mặc định như hrm: **mọi trường đầu phiếu + mọi bảng con** (hàng hóa, lô/HSD, seri, file đính kèm…).
2. **Ai được xem?** Mặc định: **ai vào được màn là xem được** — không thêm quyền. Cần quyền riêng → seeder (`feedback_permission_seeder_only`), không migration.
3. **Có thao tác nào ngoài Lưu?** (Gửi / Thu hồi / Trả lại / Duyệt / Khóa / Mở khóa) → mỗi thao tác 1 action riêng; thao tác có ô lý do / ghi chú thì lưu vào `note` (§3d).
4. **Làm ĐỦ 2 nơi** (§5): ⋮ "Lịch sử" ở màn danh sách **và** khối Lịch sử ở màn chi tiết / popup Xem. Chỉ làm 1 nơi khi entity không có nơi kia — nói rõ khi báo cáo.

## 1. Khác biệt dns so với hrm

| hrm | dns |
| --- | --- |
| `CatalogHistoryService` (giữ bảng nhãn cột `TABLES`) + trait `LogsCatalogHistory` | **`App\CommonServices\EntityHistoryService`** — engine dùng chung, **không giữ nhãn cột**: snapshot do module dựng sẵn với **khóa = nhãn tiếng Việt** |
| `SystemLogService` cho entity lớn | Mỗi module tự có service đọc (vd `Modules/Warehouse/Services/WarehouseHistoryService.php`) gọi `toDto()` |
| Route `catalog-histories/{table}/{id}` | Route theo module: `warehouse/histories/{type}/{id}` + `/filter-options` (`Modules/Warehouse/Routes/api.php`) |
| `components/assign/SystemInfoSection.vue` · `SystemInfoValue.vue` · `components/modal/CatalogHistoryModal.vue` | **`components/history/SystemInfoSection.vue` · `SystemInfoValue.vue` · `EntityHistoryModal.vue`** |
| `performers` = toàn bộ nhân sự cùng công ty người tạo (`HistoryPerformerOptions`) | `performers` = **người có trong log** của bản ghi (`EntityHistoryService::filterOptions`). Muốn đổi → sửa 1 chỗ đó, hỏi user trước (hàm dùng chung) |
| `apiGetMethod({ url, params })` | Store dns **chỉ nhận URL chuỗi** → `SystemInfoSection.historyRequest()` tự ghép `params` thành query string |
| Khối ở chi tiết dựng sẵn bằng `v-show` để badge hiện ngay | dns: thu gọn mặc định, nạp khi mở; màn cha gọi `$refs.history.refresh()` sau thao tác sinh log |

## 2. DB — chọn nơi lưu

| Loại | Lưu ở đâu |
| --- | --- |
| **Phiếu / chứng từ đã có bảng log riêng** (`warehouse_receipt_logs`, `warehouse_export_request_logs`…) | Thêm 2 cột `old_value` / `new_value` (`longText nullable`, JSON) vào bảng log đó. Dòng log cũ không có 2 cột vẫn hiện bình thường (chỉ không có chi tiết) |
| **Danh mục** (kho, kho kế toán, sau này các danh mục khác) | Bảng chung **`catalog_histories`** (`table_name` + `table_id`, `action`, `old_value`, `new_value`, `note`, `changed_by`, `changed_at`) — KHÔNG tạo `<entity>_history` mới. Bảng đã có (tạo trong migration `Modules/Warehouse/.../2026_11_26_000003_add_history_values_to_warehouse_logs.php`) |

Migration **chỉ index, không khóa ngoại** (`feedback_no_foreign_keys`), có `hasTable` / `hasColumn` để chạy lại an toàn.

## 3. BE — ghi log (trong Service, KHÔNG Observer)

### 3a. Snapshot = giá trị HIỂN THỊ, khóa = nhãn tiếng Việt

Mỗi service có `historySnapshot($model): array`, **đọc lại từ DB** (đúng dữ liệu đã lưu). Lưu chữ hiển
thị (tên kho, tên NV, "Hoạt động"/"Khóa"), không lưu id → đổi tên danh mục sau này không làm sai log cũ.

```php
use App\CommonServices\EntityHistoryService as H;

return [
    'Ngày nhập kho'           => H::date($receipt->import_date),   // d/m/Y, rỗng → null
    'Số nhà kho'              => H::num($w->num_houses),           // bỏ .000 thừa — chống log rác "5.000 → 5"
    'Thủ kho'                 => H::employeeNames($stockerIds),    // tên NV nối ', '
    'Trạng thái'              => WarehouseReceipt::statusInfo($receipt->status)['name'],
    'Danh sách file đính kèm' => H::fileRows($receipt->attachments), // khóa bảng, GIỮ nguyên đường dẫn
    'Danh sách hàng hóa'      => $itemRows,                        // khóa bảng (§3b)
];
```

Mẫu: `WarehouseReceiptService::historySnapshot()` (phiếu có 3 bảng con) · `WarehouseService::historySnapshot()` (danh mục).

### 3b. Bảng con = khóa dạng BẢNG

Giá trị là **mảng bản ghi**; engine tự tách **thêm / xóa / sửa theo từng dòng**, dòng sửa chỉ in trường đổi.
TUYỆT ĐỐI không tự ghép chuỗi cả bảng rồi nhét vào 1 khóa.

```php
$itemRows[] = [
    H::ROW_KEY   => (string) $it->id,          // __key ghép cặp trước/sau
    H::ROW_NAME  => $code . ' - ' . $name,     // __name: tên hiện ở đầu dòng
    H::ROW_BRIEF => ['Hàng hóa'],              // __brief: dòng thêm/xóa chỉ giữ cột "thuộc về" (true = chỉ in tên)
    'SL nhập kho'       => H::num($it->qty_in),
    'Lý do nhập ít hơn' => ...,
];
```

- `__key`: bảng **upsert theo id** → dùng id. Bảng **xóa hết tạo lại** mỗi lần lưu (vd lô của PNK) → khóa
  tự nhiên (`item_id|số lô`; lô trống ghép theo thứ tự `#1`, `#2`). Khóa lỡ chứa ô bị sửa → sửa 1 ô ra "xóa 1 + thêm 1".
- Bảng nhiều cấp → **tách khóa riêng** (`Danh sách chi tiết lô / HSD` tách khỏi `Danh sách hàng hóa`) kèm cột chỉ cha.
- Mọi cột tiền tố `__` là khóa điều khiển → tên cột thật không được bắt đầu bằng `__`.
- Phần chi tiết của dòng nối bằng `'; '`, không dùng gạch ngang.
- Bỏ cột số liệu khỏi dòng thêm/xóa bằng `__brief`, dòng SỬA vẫn liệt kê đủ trường đổi.

### 3c. Ghi

```php
// Phiếu có bảng log riêng
$before = $this->historySnapshot($receipt);          // CHỤP TRƯỚC khi fill / sync bảng con
// ...lưu...
[$old, $new] = app(EntityHistoryService::class)->diff($before, $this->historySnapshot($receipt));
// update mà không đổi gì → KHÔNG ghi; action khác (send/approve…) vẫn ghi dù diff rỗng
WarehouseReceiptLog::create([... 'action' => $action, 'note' => $note,
    'old_value' => $h->encode($old), 'new_value' => $h->encode($new), 'created_by' => ...]);

// Danh mục
$h->logCatalog(self::HISTORY_TABLE, $id, 'create');
$h->logCatalogUpdate(self::HISTORY_TABLE, $id, $before, $this->historySnapshot($m));            // update
$h->logCatalogUpdate(self::HISTORY_TABLE, $id, $before, $after, null, $isActive ? 'unlock' : 'lock');
```

- Ghi **trong cùng transaction** với thao tác lưu.
- Tạo mới phiếu: ghi `create` (không cần diff). Lưu kèm chuyển trạng thái (Lưu + Gửi, Lưu + Duyệt) → **1 dòng
  mang action của thao tác** (`send` / `approve`), diff gồm cả trường sửa lẫn `Trạng thái` — nhãn dòng nói rõ thao tác.
- Chỉ đổi trạng thái (Thu hồi / Trả lại) → dòng chỉ có `Trạng thái: cũ → mới` + `note`.
- Thao tác **không đổi `status`** (đổi người phụ trách, chuyển phòng…) → action `update`, nhóm "Thay đổi thông tin".
- PHP 7.4: không `?->`.

### 3d. Lý do / ghi chú phải hiện trên lịch sử

Thao tác có ô lý do / ghi chú (Gửi kèm ghi chú, Trả lại, Từ chối, Hủy…) → lưu vào `note` của dòng log, kể cả
khi lý do đã lưu ở bảng chính. FE tự hiện khối ghi chú nền vàng. Thao tác không có ô lý do thì không bịa.

## 4. BE — đọc log

Service đọc của module (mẫu `WarehouseHistoryService`):

- `logs($type, $id)`: switch theo `$type` (chuỗi gạch ngang: `receipt`, `export-request`, `warehouse`,
  `accounting-warehouse`). Bản ghi không có → 404; **kiểm quyền xem như màn chi tiết** (`ensureCanSeeReceipt`…) → 403.
  - Bảng log riêng → map dòng về `['id','action','old_value','new_value','note','actor_id','at']` rồi `toDto($rows, $labels)`.
  - Danh mục → `catalogLogs(self::HISTORY_TABLE, $id)`.
- `filterOptions($type, $id)` = `$history->filterOptions($this->logs(...))`.
- Nhãn action riêng của màn truyền qua `$labels` (vd PNK `send` → "Gửi nhập thông tin", `approve` → "Duyệt nhập kho";
  ĐNXK `send` → "Gửi kho"). Nhãn/màu mặc định ở `EntityHistoryService::ACTION_LABELS` / `ACTION_COLORS`.
- Bộ lọc "Loại hoạt động" cố định **3 nhóm** `create` Tạo mới · `update` Thay đổi thông tin · `status` Thay đổi
  trạng thái — engine tự gán `action_group`, action lạ mặc định vào `status`. Không gắn tên đối tượng vào nhãn.

DTO (FE ăn theo đúng hợp đồng này, giống hrm):
`id, action, action_label, action_group, action_color, actor_id, actor_dept_code, actor_code, actor_name,
department_name, note, changes[], created_at 'd/m/Y H:i', created_at_raw 'Y-m-d H:i:s'` — sắp **mới → cũ**.

Thêm entity mới vào module đã có: thêm `case` vào `logs()` + `TYPES`. Module khác chưa có: tạo service +
controller + route `histories/{type}/{id}` riêng của module, FE truyền `endpoint-base="<module>/histories"`.

## 5. FE — đủ 2 nơi, dùng component có sẵn, KHÔNG tự dựng timeline

| Nơi | Cách làm |
| --- | --- |
| **Màn danh sách** — ⋮ | Cuối `getRowActions`: `{ key: 'history', title: 'Lịch sử', icon: 'ri-history-line' }` (không gắn quyền). Handler `this.$refs.historyModal.open('<type>', item.id, <nhãn>)`. Đặt 1 lần `<EntityHistoryModal ref="historyModal" modal-id="<type>-history-modal" />` (id riêng từng màn) |
| **Màn chi tiết** (trang) | `<SystemInfoSection v-if="!isNew && detail && detail.id" ref="history" entity-type="<type>" :entity-id="detail.id" class="mt-2" />` — khối riêng **ngoài card nội dung**, sát dưới, full ngang; **không** là nút ở `V2Footer` |
| **Màn chi tiết có tab** | Tab Lịch sử: `<SystemInfoSection v-if="activeTab === 'logs'" ref="history" ... :default-opened="true" :hide-header="true" />` |
| **Popup Xem danh mục** | Cuối body, trước `#footer`: `<SystemInfoSection v-if="isView && recordId" entity-type="<type>" :entity-id="recordId" class="mt-2" />` |

- **Nhãn bản ghi ở tiêu đề popup**: phiếu → số phiếu (`item.code`); danh mục → **chỉ tên** (`item.name || item.code`),
  không ghép `mã - tên` (chốt hrm 28/09/2026).
- Sau thao tác sinh log mà vẫn ở lại màn (Lưu ở chế độ xem, Thu hồi, tải lại chi tiết) → gọi
  `this.$nextTick(() => this.$refs.history && this.$refs.history.refresh())`.
- Endpoint khác `warehouse/histories` → prop `endpoint-base`. Dòng bảng con dài muốn xuống dòng từng phần → `multiline-rows`.
- Component tự giữ state (loading / items / filters), không đụng state màn cha. Gọi API bằng `apiGetMethod`, không thêm Vuex action.
- Giá trị log luôn render qua `SystemInfoValue` (tự bóc HTML, cắt dài + "Xem thêm", đường dẫn file → link xem trước).
  Không tự `{{ }}` / `v-html` giá trị log ở component riêng.
- Màn đang có timeline tự viết (`.rc-timeline`, `.er-timeline`, `LOG_ICONS`…) → thay bằng `SystemInfoSection` và xóa code + CSS cũ.
- Sửa `components/history/*` = sửa component dùng chung → **hỏi user trước** (CLAUDE.md).

## 6. Bẫy thường gặp

- Chụp snapshot **sau** khi fill → diff rỗng, mất log.
- Không chuẩn hóa số / ngày / rỗng → mỗi lần lưu lại đẻ 1 dòng rác. Luôn qua `H::num()` / `H::date()`; engine coi `''` = `null`.
- Ép `(string)` mảng bản ghi → log ra chữ `Array`.
- Gán "cột ảo" lên model Eloquent → `save()` ném "Unknown column". Giữ ở biến của service.
- Cắt đường dẫn file còn tên tệp ở BE → không mở được file. `H::fileRows()` đã giữ `Đường dẫn` + `__name` + `__brief`.
- Đổi định dạng snapshot (thêm/đổi nhãn) → lần lưu đầu sau deploy sinh 1 dòng nhiễu; báo trước user, không sửa log cũ.
- Bảng con có `product_id` nhưng không có cột tên → tra danh mục lấy tên, kẻo dòng log trắng tên.

## 7. Verify trước khi báo xong

1. **Script PHP bootstrap riêng** (`require vendor/autoload.php` + `bootstrap/app.php`; `php artisan tinker <file>`
   KHÔNG chạy file), mỗi ca bọc `DB::beginTransaction()` … `DB::rollBack()`, in `tên ca | số dòng log | DTO`:
   - đổi **từng trường** của bảng chính, **từng cột** của mỗi bảng con (lấy danh sách từ `describe <bảng>`);
   - thêm 1 dòng / xóa 1 dòng mỗi bảng con → đúng 1 dòng "thêm mới" / "đã xóa", đúng tên;
   - đổi nhiều trường 1 lần → 1 dòng log nhiều khóa;
   - không đổi gì / lưu lại lần 2 → **không ghi log**;
   - mỗi thao tác trạng thái (gửi / thu hồi / trả lại / duyệt / khóa / mở khóa) → đúng nhãn + `note`.
2. FE: compile template + parse script (`vue-template-compiler` + `@babel/parser`, chạy với cwd = `hrm-thanhan-client`
   — client không có eslint chạy được trên Node 14) rồi curl các trang trên :3001 xem build không lỗi.
3. Script e2e đọc lịch sử: mở khối (`.si-header` nếu `.si-body` đang ẩn) rồi đọc `.si-body`. **Chỉ chạy Playwright khi user bảo.**

## Checklist

- [ ] Đã chốt: trường track / quyền xem / các thao tác / 2 nơi hiển thị
- [ ] Nơi lưu đúng §2 (bảng log riêng + `old_value`/`new_value`, hoặc `catalog_histories`); migration không FK
- [ ] `historySnapshot()` đọc lại DB, khóa = nhãn tiếng Việt, giá trị hiển thị, chuẩn hóa qua `H::num` / `H::date`
- [ ] Bảng con là khóa dạng BẢNG có `__key` / `__name` (+ `__brief` khi cần), bảng nhiều cấp tách khóa
- [ ] Chụp trước – diff sau, cùng transaction; `update` không đổi → không ghi
- [ ] Lý do / ghi chú của thao tác nằm ở `note`
- [ ] Service đọc: 404 / kiểm quyền xem như màn chi tiết; nhãn action riêng qua `$labels`; mới → cũ
- [ ] FE đủ 2 nơi bằng `components/history/*`; tiêu đề popup: số phiếu / tên danh mục; màn cha gọi `refresh()`
- [ ] Đã xóa timeline tự viết cũ + CSS
- [ ] Đã chạy script verify từng trường (§7)
