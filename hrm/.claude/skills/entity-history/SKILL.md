---
name: entity-history
description: Use when làm bất kỳ tính năng "lịch sử thay đổi / lịch sử chỉnh sửa / audit log ai sửa gì, giá trị cũ → giá trị mới, lúc nào" cho một màn/entity — tạo mới, sửa cách hiển thị, đổi text/màu/bộ lọc của popup lịch sử, hoặc thêm mục Lịch sử vào màn chi tiết.
---

# Skill: Entity History (Lịch sử thay đổi)

Chuẩn hoá cách làm tính năng "Lịch sử thay đổi" (audit log ai sửa gì, giá trị cũ → giá trị mới, lúc nào) cho một màn/entity.
⚠️ **Đừng nhầm 2 chiều**: trong 1 dòng log là **giá trị cũ (đỏ) → giá trị mới (xanh)**;
còn **thứ tự danh sách luôn MỚI → CŨ** (mới nhất lên đầu, §4) — chốt từ 2026-08-12, áp cho mọi entity.
Áp dụng khi user yêu cầu: "bổ sung lịch sử chỉnh sửa", "lịch sử thay đổi", "log ai sửa", "audit" cho bất kỳ màn nào.

> **UI: KHÔNG tự thiết kế.** Mọi popup / mục lịch sử phải theo đúng base đã chốt ở màn Khách hàng
> (bố cục, text, màu, bộ lọc) — spec đầy đủ + markup copy-paste: **`ui-base.md`** cùng thư mục.
> Đọc `ui-base.md` TRƯỚC khi viết dòng markup đầu tiên.
>
> **PHẠM VI: luôn làm ĐỦ 2 NƠI như màn Khách hàng** — popup ở màn DANH SÁCH *và* mục "Lịch sử" ở
> màn CHI TIẾT. Làm 1 nơi rồi báo xong là thiếu; user sẽ phải quay lại yêu cầu bổ sung (xem §5).

**Mẫu chuẩn (đọc code trước khi làm):**

| Phần | File mẫu |
| --- | --- |
| **UI base (BẮT BUỘC)** | `hrm-client/components/assign/customer/CustomerHistoryModal.vue` (popup) + `hrm-client/components/assign/SystemInfoSection.vue` (mục trong màn chi tiết) |
| Đọc log + chuẩn hoá DTO | `hrm-api/Modules/Assign/Services/SystemLogService.php` (`getLogs`, `finalize`, `customerChanges`, `recordListChange`) |
| Ghi log (subset-diff + khoá dạng bảng) | `hrm-api/Modules/Assign/Services/CustomerHistoryService.php` |
| Migration | `hrm-api/Modules/Timesheet/Database/Migrations/2026_07_10_000001_create_general_regulation_history_table.php` |
| Biến thể đơn giản (1 màn, 1 action) | `GeneralRegulationService` + `hrm-client/components/setting/general/GeneralHistoryModal.vue` |

---

## 0. Câu hỏi PHẢI chốt với user trước khi code

1. **Track trường nào?** Chỉ trường trên màn đó, hay mọi cột? (endpoint save có thể được màn khác dùng chung → trường của màn khác KHÔNG được sinh log)
2. **Ai được xem?** Mặc định: KHÔNG permission riêng (ai vào được màn thì xem được lịch sử). Chỉ thêm permission khi user yêu cầu (sửa `PermissionsTableSeeder`, không migration).
3. **Có action nào ngoài `update` không?** (create / khóa / mở khóa / đổi trạng thái / duyệt / từ chối)
   → action nào có ô lý do hoặc ghi chú thì phải hiện trên lịch sử (§4.1)
   → nhưng bộ lọc "Loại hoạt động" thì KHÔNG liệt kê chúng: luôn đúng 3 nhóm cố định (§0a)
4. **Có bảng con dạng danh sách không?** (người liên hệ, tài khoản ngân hàng, địa điểm...) → bắt buộc dùng **khoá dạng bảng** ở §3.

## 0a. Bộ lọc "Loại hoạt động" — CỐ ĐỊNH 3 NHÓM, mọi màn như nhau

Dropdown "Loại hoạt động" (khối Lịch sử ở màn chi tiết **và** popup Lịch sử ở màn danh sách)
luôn có **đúng 3 lựa chọn này, không hơn không kém, không đổi chữ, không gắn tên đối tượng**:

| value | Nhãn hiển thị |
| --- | --- |
| `create` | **Tạo mới** |
| `update` | **Thay đổi thông tin** |
| `status` | **Thay đổi trạng thái** |

❌ SAI (kiểu cũ, mỗi entity một danh mục): "Tạo khách hàng", "Chỉnh sửa thông tin",
"Cập nhật ảnh / tài liệu / video", "Khóa khách hàng", "Gửi duyệt", "Nghiệm thu hạng mục"…
→ mỗi màn ra một dropdown khác nhau, user không đối chiếu được giữa các màn.

**Nhóm chỉ dùng cho BỘ LỌC. Nhãn chi tiết của từng dòng vẫn giữ nguyên trên timeline**
(vẫn hiện "Khóa khách hàng", "Duyệt", "Từ chối"…) → lọc thì đồng nhất, xem thì không mất thông tin.

### Cách ánh xạ (BE)
`SystemLogService` khai sẵn, **không tự khai lại ở từng entity**:
- `ACTION_GROUP_LABELS` — 3 nhãn trên
- `ACTION_GROUP_MAP` — action cụ thể → nhóm:
  - `create` / `created` / `store` → `create`
  - `update` / `updated` / `update_media` → `update`
  - `change_status` / `lock` / `unlock` / `submitted` / `resubmitted` / `approved` / `rejected` /
    `item_accepted` / `item_rejected` / `completed` → `status`
- `groupOfAction()` — action **chưa khai** mặc định vào `status` (phần lớn action đặc thù còn lại
  đều là chuyển trạng thái phiếu) ⇒ entity mới thêm sau vẫn lọc được ngay, không phải sửa map.
- `finalize()` gắn `action_group` cho MỌI dòng log → tự áp cho cả 10 loại đối tượng.
- `getFilterOptions()` trả 3 nhóm này cho **mọi `$type`**.

### Ô "Người thực hiện" — phải liệt kê ĐỦ nhân sự, KHÔNG suy từ log (chốt 2026-08-15)

`getFilterOptions()` **luôn phải trả `performers`** = nhân viên **cùng công ty với người tạo bản
ghi** (format `MÃ PHÒNG - Tên`, sắp theo tên), giống hệt màn Khách hàng. Áp cho MỌI loại đối tượng,
kể cả danh mục nhỏ.

- ❌ SAI (kiểu cũ): trả `performers: []` rồi để FE tự suy từ log đang tải. Log của 1 bản ghi thường
  chỉ có 1-2 người → dropdown chỉ hiện 1-2 dòng, user tưởng hệ thống thiếu dữ liệu. Đây là lỗi
  user đã phải chỉ ra.
- Suy công ty: `created_by` của bản ghi → `employees.employee_info_id` → `employee_infos.company_id`.
- Bảng không có `created_by`, hoặc bản ghi cũ để trống → **trả TẤT CẢ nhân sự**, còn hơn để rỗng.
- **Logic nằm ở ĐÚNG 1 CHỖ: `App\Services\HistoryPerformerOptions`** (`forCompany()` +
  `companyOfCreator()`). Cả `SystemLogService` (entity lớn) lẫn `CatalogHistoryService` (danh mục)
  đều gọi helper này — đổi quy tắc (vd lọc theo công ty người ĐANG ĐĂNG NHẬP thay vì người tạo bản
  ghi) thì **sửa 1 file duy nhất**, đừng copy logic sang service khác.
- Màn danh mục: endpoint `catalog-histories/{table}/{id}/filter-options` phải truyền đủ `{table}` +
  `{id}` (thiếu id thì không suy được công ty).
- Kiểm nhanh: số option của ô "Người thực hiện" ở màn danh mục phải **bằng** màn Khách hàng
  (`assign/system-logs/customer/{id}/filter-options`) — lệch là đang suy từ log.

### FE
- `actionOptions()` lấy từ `filter-options`; fallback là **3 nhóm hard-code**, KHÔNG suy từ log
  (suy từ log = mỗi bản ghi ra một dropdown khác nhau, đúng thứ cần bỏ).
- Lọc bằng `log.action_group`, có fallback `log.action` cho BE cũ:
  `if (f.action && (log.action_group || log.action) !== f.action) return false`
- Sửa **cả 2 nơi** (`SystemInfoSection.vue` + popup lịch sử của entity) — xem §5.1.

## 1. Chọn biến thể

- **Subset-diff (MẶC ĐỊNH)**: BE diff sẵn, `old_value`/`new_value` = JSON **chỉ gồm trường thay đổi**. FE render thẳng.
- **Full-snapshot**: lưu snapshot đầy đủ, FE tự diff. Chỉ dùng khi màn cũ đã làm vậy.

## 2. DB

Bảng `<entity>_history` (số ít):

- `id`, `<entity>_id` (unsignedBigInteger, index), `company_id` (nullable, index — nếu entity scope theo công ty)
- `action` (string), `old_value`/`new_value` (text nullable, JSON), `changed_by` (nullable), `changed_at` (timestamp `useCurrent`), `timestamps()`
- KHÔNG FK cứng, KHÔNG SoftDeletes. Migration có PHPDoc trên `up()`/`down()`.

## 3. BE — ghi log (Service, KHÔNG dùng Observer)

Snapshot lưu **GIÁ TRỊ HIỂN THỊ** (tên tỉnh, tên nhóm, "Có/Không") chứ không lưu id → log tự chứa,
đổi tên danh mục sau này không làm sai log cũ.
Chụp snapshot tracked TRƯỚC `fill()` → save → diff → có thay đổi mới insert 1 dòng
(`changed_by = auth()->id()`, JSON `JSON_UNESCAPED_UNICODE`). Không đổi gì → không ghi.
PHP 7.4: không `?->`.

**Trường thường:** `[khoá => chuỗi]`, chuẩn hoá trước khi so (rỗng/null → null, boolean → '0'/'1',
số → chuỗi số). Không chuẩn hoá = log rác `"5" → 5`.

**Khoá dạng danh sách đơn giản** (nhóm KH, hãng xe, ảnh): mảng chuỗi, diff theo phần tử thêm/bỏ.

**Khoá dạng BẢNG** (người liên hệ, tài khoản ngân hàng — có nhiều cột): mỗi phần tử là **bản ghi**
`['__key' => ..., 'Nhãn' => 'giá trị', ...]`, bỏ trường rỗng.

- `__key` = khoá ghép cặp bản ghi trước/sau. Bảng lưu theo kiểu **upsert theo id** → dùng id;
  bảng **xóa hết rồi tạo lại** mỗi lần lưu → dùng khoá tự nhiên (số TK, id cha + số TK).
- Bảng con nhiều cấp (TK cá nhân của người liên hệ) → **tách thành khoá riêng** kèm cột nhận diện
  chủ sở hữu, KHÔNG nhét vào chuỗi của bản ghi cha. Nhét vào = thêm 1 TK là in lại nguyên dòng dài.

## 4. BE — đọc log: DTO chuẩn (FE base ăn theo đúng hợp đồng này)

Sắp xếp **MỚI → CŨ** (`orderByDesc('changed_at')->orderByDesc('id')` + usort giảm dần).
(Quy ước cũ "ASC cũ → mới" đã BỎ từ 2026-08-12.)

Mỗi dòng log trả:

```
id, action, action_label, action_color, actor_code, actor_name, department_name,
note, changes[], created_at ('d/m/Y H:i'), created_at_raw ('Y-m-d H:i:s')
```

`changes[]` có 2 dạng — FE base xử lý sẵn cả hai:

```php
// a) Trường thường
['field' => 'Tên khách hàng', 'old' => 'CTY A', 'new' => 'CTY B']

// b) Khoá dạng danh sách / bảng
[
  'field'   => 'Tài khoản công ty',
  'old' => '...', 'new' => '...',            // chuỗi gộp, cho nơi hiển thị 1 dòng
  'removed' => ['Số TK: 111 — Chủ TK: A'],   // bản ghi bị XÓA (in đủ)
  'added'   => ['Số TK: 222 — Chủ TK: B'],   // bản ghi THÊM MỚI (in đủ)
  'changed' => [                             // bản ghi còn đó nhưng SỬA
    ['name' => 'ffff', 'fields' => [
      ['field' => 'Chủ TK', 'old' => 'gggg', 'new' => 'Nguyễn Văn C'],
    ]],
  ],
]
```

**Quy tắc vàng:** bản ghi bị sửa CHỈ liệt kê trường đã đổi. In lại cả bản ghi ở `removed` + `added`
là sai — user không nhìn ra đổi cái gì.

`created_at_raw` là bắt buộc: bộ lọc ngày của FE cắt 10 ký tự đầu chuỗi này.

### 4.1. Lý do / ghi chú của thao tác — PHẢI hiện hết trên lịch sử

**Thao tác nào có ô lý do hoặc ghi chú thì lịch sử phải hiện đúng nội dung đó.** Áp cho mọi loại:
từ chối, duyệt (nếu có ô ghi chú duyệt), hủy, đóng, khóa, hủy chốt, trả lại...

- Ghi vào `note` của dòng log (hoặc `meta['reason']` — `SystemLogService::mergeNote()` tự gộp cả hai).
- FE base render `note` thành khối ghi chú nền vàng cuối mục log (xem `ui-base.md` §4). Không cần sửa FE.
- **Lý do đã lưu ở bảng chính thì vẫn phải đẩy vào log.** Lưu `reject_reason` / `closed_reason` /
  `reason_deny` trên bảng entity mà dòng log chỉ có "Trạng thái: cũ → mới" là **THIẾU** — user mở
  lịch sử không biết vì sao bị từ chối.
- Nhánh đổi trạng thái thường ghi log riêng (`change_status`) nên rất hay quên: kiểm tra lại đúng
  nhánh đó, đừng chỉ nhìn nhánh `update`.
- Bảng log chưa có cột `note`/`meta` → thêm cột `note` (text nullable), KHÔNG nhồi lý do vào
  `new_value` snapshot.
- Thao tác **không có** ô nhập lý do thì không tự bịa dòng ghi chú; muốn có thì chốt với user
  (thêm ô nhập FE + cột BE) trước khi làm.

## 5. FE

Đọc **`ui-base.md`** và copy theo.

### 5.1. BẮT BUỘC làm đủ 2 nơi (như màn Khách hàng)

| Nơi | Cách vào | Component |
| --- | --- | --- |
| **Màn DANH SÁCH** | menu ⋮ của từng dòng → mục `Lịch sử` (icon `ri-history-line`, KHÔNG gắn permission riêng) | **`components/modal/CatalogHistoryModal.vue`** (màn danh mục) · `CustomerHistoryModal.vue` (entity lớn có log riêng) |
| **Màn CHI TIẾT** | khối "Lịch sử" trong thân trang, mặc định thu gọn, lazy load lần mở đầu | `SystemInfoSection.vue` (`entity-type` + `entity-id`) |
| **Popup XEM của màn danh mục** | khối "Lịch sử" **cuối popup**, thu gọn sẵn | `SystemInfoSection.vue` — nhúng thẳng vào modal Xem |

### Màn DANH MỤC — dùng bộ dùng chung, KHÔNG viết mới (chốt 2026-08-15)

Nhóm danh mục (tiền tệ, vụ việc, mã phí, quốc gia, tỉnh/huyện/xã, ngân hàng, tài khoản…) đã có sẵn
đủ bộ, thêm màn mới chỉ cần **khai báo**, không viết bảng log / adapter / popup riêng:

| Lớp | Dùng cái gì |
| --- | --- |
| **DB** | bảng chung `catalog_histories` (`table_name` + `table_id`) — KHÔNG tạo `<entity>_history` mới |
| **BE ghi log** | `use App\Services\Concerns\LogsCatalogHistory` trong service: khai `catalogTable()`, `catalogColumns()`, (tuỳ chọn) `catalogDisplay()`; gọi `logCatalogCreate` / `logCatalogUpdate` / `logCatalogStatus` / `logCatalogDelete` |
| **BE đọc** | `App\Services\CatalogHistoryService` + endpoint chung `GET /api/v1/catalog-histories/{table}/{id}` — nhớ khai bảng + nhãn cột tiếng Việt vào `CatalogHistoryService::TABLES` (whitelist) |
| **FE popup ở danh sách** | `<CatalogHistoryModal ref="historyModal" modal-id="history-<màn>" record-prefix="Vụ việc" />` rồi `this.$refs.historyModal.open('<table>', item.id, '<mã> - <tên>')` |
| **FE khối ở chi tiết / popup Xem** | `<SystemInfoSection entity-type="<table>" :entity-id="id" endpoint-base="catalog-histories" />` |

Entity lớn đã có bảng log riêng (khách hàng, báo giá, phiếu…) thì GIỮ nguyên `SystemLogService`.
Entity từng có log kiểu version (`<x>_versions` + `<x>_histories`, vd `accounts`) đọc qua
`CatalogHistoryService::LEGACY_VERSION_TABLES` để log cũ vẫn hiện — không phải chuyển dữ liệu.

**`CatalogHistoryModal` dựng trên `V2BaseModal`** (khuôn popup dùng chung — skill `modal-popup`
mục 0): header/body/footer theo đúng chuẩn, không tự khai style riêng.

⚠️ `SystemInfoSection` khi nằm TRONG popup (`hide-header`) tự bật `si-borderless`: bỏ viền + bỏ
`overflow` của vùng nội dung. Bỏ `overflow` là bắt buộc — để nguyên thì cụm bộ lọc `sticky` dính
theo khối này (khối không cuộn) nên **trôi mất** khi user cuộn popup.

⚠️ **Ở màn chi tiết, Lịch sử là KHỐI TRONG THÂN TRANG — KHÔNG phải nút ở `V2Footer`** (chốt
2026-08-15, khuôn `/assign/customers/{id}`). Footer chỉ chứa hành động thao tác (Sửa, Khóa, Xóa,
Quay lại). Đặt nút "Lịch sử" ở footer là sai: nội dung lịch sử thuộc về trang, không phải hành động.

⚠️ **Danh mục Thêm/Sửa/Xem bằng modal cũng phải có khối Lịch sử trong popup Xem** (chốt 2026-08-15).
Quy ước cũ "chi tiết mở dạng modal thì ẩn khối Lịch sử" đã BỎ.

**Padding vùng nội dung của khối Lịch sử = `5px`** — dùng đúng một trị số này ở mọi màn (`.si-body`),
không màn nào tự nới rộng.

- Cùng 1 endpoint, cùng bố cục, cùng text/màu/bộ lọc, cùng thứ tự mới → cũ. User đối chiếu 2 màn với nhau.
- Chỉ được làm 1 nơi khi entity **không có** màn còn lại (VD chỉ có màn cài đặt, không có danh sách) — và phải nói rõ lý do khi báo cáo.
- (BỎ từ 2026-08-15) Quy ước cũ "màn chi tiết mở dạng modal thì ẩn khối Lịch sử" không còn áp dụng: popup Xem của danh mục vẫn phải có khối Lịch sử ở cuối.

### 5.2. Tóm tắt hiển thị

- 2 nơi hiển thị dùng **cùng một bố cục**: popup (mở từ menu ⋮ màn danh sách) và mục "Lịch sử" trong màn chi tiết.
- Timeline chấm tròn màu theo `action_color`; mỗi mục: **thời gian → tên hành động → "Người thực hiện: ..." → khối thay đổi**.
- Màu: cũ **#dc2626 (đỏ)**, mới **#16a34a (xanh)**, nhãn/tên bản ghi **#475569**. Dòng sửa `~` phải tô cũ đỏ / mới xanh BÊN TRONG, không để một màu.
- Bộ lọc client-side 4 ô: **Loại hành động / Người thực hiện / Từ ngày / Đến ngày** + nút Tìm kiếm, Làm mới.
- Gọi API bằng `$store.dispatch('apiGetMethod', ...)`, KHÔNG thêm Vuex action riêng.
- Component tự giữ state (loading/items/filters) — không đụng state màn cha (màn auto-save sẽ bắn POST oan).

## 6. Bẫy thường gặp

- Endpoint save dùng chung với màn khác → trường ngoài whitelist đổi thì KHÔNG được sinh log.
- Đổi định dạng dòng snapshot (thêm nhãn, thêm cột) → **lần sửa đầu tiên sau deploy sẽ nhiễu 1 lần**
  (log cũ khác định dạng). Phải báo trước cho user, đừng tự sửa dữ liệu log cũ.
- Đổi N trường trong 1 lần lưu → 1 dòng log N key (không tách dòng).
- Sắp xếp: mới → cũ, ở CẢ 2 nơi hiển thị.

## 7. Verify bắt buộc trước khi báo xong

1. `php -l` + tinker: đổi 1 trường → 1 log đúng subset; không đổi → không log; trường ngoài whitelist → không log;
   boolean `true` vs `"1"` → không log rác; đổi 2 trường → 1 dòng 2 key; thứ tự trả về mới → cũ;
   **thêm 1 bản ghi con → chỉ 1 dòng `+`**; **sửa 1 cột của bản ghi con → chỉ 1 dòng `~` đúng cột đó**.
2. FE: compile template (`vue-template-compiler`) + render thật (`vue-server-renderer`) so output **popup và mục chi tiết giống hệt nhau**;
   test 3 bộ lọc (loại hành động / người thực hiện / khoảng ngày) trả đúng; mở/đóng modal không tự bắn POST.
   (hrm-client KHÔNG có ESLint config chạy được trên Node 14 — đừng dùng eslint làm cổng verify.)
3. Dọn log test bằng tinker (`where('id','>',$maxTrướcTest)->delete()`), khôi phục giá trị đã đổi.
   KHÔNG xoá log thật của user.

---

## Checklist khi tạo/review

- [ ] Đã chốt với user: trường track / quyền xem / loại action / có bảng con không
- [ ] Bảng `<entity>_history` đúng cột mẫu, migration có PHPDoc
- [ ] Snapshot lưu giá trị hiển thị; bảng con dùng bản ghi `[nhãn => giá trị] + __key`
- [ ] DTO trả đủ `action_label/action_color/action_group/actor_*/department_name/created_at/created_at_raw`
- [ ] **Bộ lọc "Loại hoạt động" đúng 3 nhóm cố định** (Tạo mới / Thay đổi thông tin / Thay đổi trạng thái) — giống hệt mọi màn khác, và nhãn chi tiết trên timeline vẫn giữ nguyên (§0a)
- [ ] Sắp xếp mới → cũ
- [ ] `changed[]` chỉ chứa trường đã đổi (không in lại cả bản ghi)
- [ ] **Mọi thao tác có lý do/ghi chú (từ chối, hủy, đóng, duyệt kèm ghi chú…) đều hiện đủ trên lịch sử** (§4.1)
- [ ] **Đã làm ĐỦ 2 nơi**: popup ở màn danh sách (menu ⋮) + khối "Lịch sử" ở màn chi tiết (§5.1)
- [ ] FE theo đúng `ui-base.md`: bố cục, text, màu, bộ lọc — cả popup lẫn mục màn chi tiết
- [ ] Verify đủ mục 7
