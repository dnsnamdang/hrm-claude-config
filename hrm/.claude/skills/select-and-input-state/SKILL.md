---
name: select-and-input-state
description: Use when làm việc với select / ô nhập liệu ở BẤT KỲ màn nào (form, modal, chi tiết, bộ lọc) — không riêng màn danh sách. Bắt buộc đọc khi gặp một trong các triệu chứng/ngữ cảnh: select danh mục MẤT giá trị đã chọn sau khi danh mục bị khoá / ngừng hoạt động; cần đánh dấu 🔒 cho option đã khoá; ô nhập bị disabled/readonly hiển thị sai màu hoặc vẫn bấm được; chip của select chọn nhiều sai khuôn; viền xanh / quầng sáng khi focus ô nhập; FE dùng trường hoặc endpoint mới mà BE chưa deploy kịp.
---

# Select & trạng thái ô nhập liệu — quy tắc dùng chung toàn hệ thống

> **Phạm vi**: MỌI màn có select hoặc ô nhập — màn danh sách, màn form Tạo/Sửa, màn chi tiết, modal/popup, bộ lọc. Trước đây 5 mục này nằm trong `list-page/SKILL.md` mục 9–13, khiến người làm màn form/modal không có đường nào tìm ra (đã gây lỗi thật: sửa màn `meeting/{id}/edit` mà bỏ sót quy tắc 🔒). Nay tách riêng, `list-page` chỉ còn con trỏ sang đây.
>
> Skill liên quan: `modal-popup` (select trong modal bắt buộc `V2BaseSelectInModal`), `form-validate`, `button-convention`.

---

## 1. Danh mục bị KHOÁ trong select — tự động, không phải khai gì

Nghiệp vụ (CLAUDE.md): dropdown chỉ liệt kê danh mục **còn hoạt động**, NHƯNG giá trị mà bản ghi đang chọn thì **vẫn phải hiện** dù danh mục đó đã khoá — không thì mở màn Sửa thấy ô trống, lưu lại là **mất dữ liệu**.

### BE — 2 việc

```php
// 1. Nhận `include_ids` = id đang được chọn, giữ lại dù đã khoá
$query->where(function ($q) use ($includeIds) {
    $q->where('status', 1);
    if (count($includeIds)) $q->orWhereIn('id', $includeIds);
});

// 2. Trả kèm cờ is_locked, GIỮ NGUYÊN tên (không nối "(đã khoá)" vào name)
return ['id' => $x->id, 'name' => $x->name, 'is_locked' => (int) $x->status !== 1];
```

Khuôn: `CustomerService::customerGroups()`, `MeetingTypeService::getAll($includeIds)`.

`include_ids` nhận cả chuỗi `1,2` lẫn mảng — controller tự chuẩn hoá:

```php
$includeIds = $request->input('include_ids', []);
if (!is_array($includeIds)) $includeIds = explode(',', (string) $includeIds);
$includeIds = array_values(array_filter(array_map('intval', $includeIds)));
```

### FE — chỉ 2 việc, KHÔNG phải khai gì để hiện 🔒

1. Gọi API danh mục kèm `include_ids` = các id đang chọn.
2. Nạp **lại** danh mục **sau khi có dữ liệu bản ghi** — lượt gọi ở `mounted` chưa biết bản ghi đang chọn id nào:

```js
if ((this.form.groups || []).length) this.loadCustomerGroups()   // trong loadDetail()
```

Màn mà dữ liệu detail đổ vào `form` qua prop (không có `loadDetail` để móc vào) thì dùng watcher — bắt đúng lượt load đầu tiên:

```js
'form.meeting_type_id'(newId, oldId) {
    if (!newId || oldId) return                                   // chỉ lượt load đầu
    if (!this.meeting_types.some((t) => t.id == newId)) this.getMeetingType()
}
```

Phần hiển thị đã nằm trong `utils/select2LockedOption.js`, được **`V2BaseSelect` và `V2BaseSelectInModal` gọi sẵn**: options có cờ `is_locked` là tự gắn `🔒 ` trước tên **trong danh sách chọn**; chip/giá trị đã chọn giữ tên gốc. Không có option nào khoá thì không đổi gì.

⚠️ Đừng làm 3 thứ sau:

- **Nối `"(đã khoá)"` hay `"🔒 "` vào `name`** — chip cũng dính, và text lệch làm hỏng tìm kiếm/so sánh giá trị.
- **Dựng thẻ `<i class="ri-lock-line">`** — select2 escape HTML nên phải render DOM qua template, dài dòng mà không đẹp hơn emoji.
- **Viết `templateResult` riêng ở từng màn** — đã có sẵn trong component. Màn nào tự khai `templateResult` thì helper nhường, nên vẫn override được khi thật sự cần.

⚠️ **Wrapper tự khai `templateResult` thì PHẢI tự gắn 🔒.** Helper cố ý nhường quyền, nên select nào đi qua một wrapper có `templateResult` riêng sẽ **im lặng mất dấu khoá**. Hiện có `DescriptionInfoSelect.vue` (ruột của `MeetingTypeSelect`, `ProjectPhaseSelect` — khai `templateResult` để render icon Info). Wrapper kiểu này dùng lại hằng chung, chỉ gắn ở dropdown:

```js
import { LOCKED_OPTION_PREFIX } from '@/utils/select2LockedOption'
// trong templateResult:
const prefix = this.lockedIds.has(String(data.id)) ? LOCKED_OPTION_PREFIX : ''
```

Viết wrapper mới có `templateResult` → thêm luôn 2 dòng này, đừng để lần sau phát hiện bằng bug.

⚠️ **Kiểm tra helper có tồn tại trên nhánh đang làm chưa**: `utils/select2LockedOption.js` sinh ra ở nhánh `gop_db` (commit `7cae2dc02`) rồi mới port sang nhánh khác. Không thấy file → `git log --all --oneline -- utils/select2LockedOption.js` rồi port đúng bản của team, KHÔNG tự viết lại.

---

## 2. Chip của select chọn nhiều

Giá trị đã chọn ở select `multiple` (`V2BaseSelect` / `V2BaseSelectInModal`) hiển thị **một khuôn chip duy nhất** trong toàn dự án — trùng với chip tự dựng `.csp-chip` (ô "Loại hình hoạt động khách hàng" ở `CustomerForm`):

| Thuộc tính | Giá trị |
| --- | --- |
| Nền / viền / chữ | `#eff6ff` / `#bfdbfe` / `#1e40af` |
| Bo góc | `5px` (KHÔNG bo tròn dạng pill) |
| Chữ | `11px`, `font-weight: 500`, `line-height: 18px` |
| Padding | `1px 7px` — giữ nguyên ở mọi `size`, size `sm` KHÔNG được ghi đè |
| Hover chip | nền `#dbeafe`, viền `#93c5fd` |
| Nút `×` trên chip | đứng **SAU** chữ, `13px`, `opacity .6`, không khung/không nền; hover `opacity 1` + đỏ `#dc3545` |

Đã set sẵn trong `V2BaseSelect.vue` (style global theo `.v2-select`, `V2BaseSelectInModal` dùng chung class nên ăn theo). Khi thêm size mới hoặc biến thể select: **không khai lại `font-size`/`padding` cho `.select2-selection__choice`**.

---

## 3. Ô nhập liệu bị KHOÁ (disabled / readonly) — một kiểu duy nhất

| Thuộc tính | Giá trị |
| --- | --- |
| Nền | `#f1f5f9` |
| Chữ | `#475569` (đọc rõ — màn chi tiết là nơi user ĐỌC dữ liệu) |
| Viền | `#e2e8f0` |
| Con trỏ | `not-allowed` |
| `opacity` | **1** — KHÔNG làm mờ |

Rule chung đặt ở `assets/scss/v2-styles.scss`, phủ đủ: `.v2-input:disabled`, `.v2-textarea:disabled`, `input/textarea/select.form-control:disabled`, `.mx-input:disabled` (datepicker), `.v2-code-input.is-disabled`, `.csp-control.is-disabled` (ô chip tự dựng), `.select2-container--disabled .select2-selection`.

**Khi viết component mới có trạng thái khoá: KHÔNG tự đặt màu nền/chữ riêng** — chỉ khai `cursor`. Trước khi chuẩn hoá, mỗi component tự đặt một kiểu (input để trắng, textarea/datepicker `#f1f5f7`, select2 `#f1f5f9` + `opacity .6`, ô chip `#e9ecef`) → 5 kiểu khác nhau trên cùng một form.

⚠️ 2 bẫy đã trả giá:

- **`opacity` làm hỏng khả năng đọc** ở màn chi tiết, và chip trong ô bị chồng màu. Dùng màu chữ nhạt thay cho `opacity`.
- **Selector nặng ký đè rule chung**: `V2BaseSelect` có `div.v2-select .select2-container.select2-container--default .select2-selection--multiple { background: #fff !important }` — đặc hiệu hơn rule chung nên ô select nhiều lựa chọn khi khoá vẫn trắng. Phải thêm `:not(.select2-container--disabled)` vào selector đó. Khi thấy 1 ô "không chịu đổi màu", tìm rule đè bằng cách duyệt `document.styleSheets` và lọc `el.matches(r.selectorText)`.

**Chip bên trong ô bị khoá cũng chuyển XÁM**, dùng chung cho cả chip của select2 (`.select2-selection__choice`) lẫn chip tự dựng (`.csp-chip`):

| Thuộc tính | Giá trị |
| --- | --- |
| Nền | `#e2e8f0` — **đậm hơn nền ô** (`#f1f5f9`) để chip không chìm thành một khối xám |
| Chữ | `#475569` |
| Viền | `#cbd5e1` |
| Nút `×` | ẩn (`display: none`) |

⚠️ **Ô tự dựng bằng `<div>` (không phải thẻ input) phải TỰ CHẶN thao tác khi khoá.** CSS `cursor: not-allowed` chỉ đổi con trỏ; `<div>` không có thuộc tính `disabled` của trình duyệt nên handler vẫn chạy — bấm vào ô khoá vẫn mở dropdown chọn. Chặn ngay đầu handler:

```js
toggleDropdown() {
    if (this.readonly) return   // hoặc this.disabled
    …
}
```
Nhớ chặn ở **mọi** handler: mở dropdown, xoá chip, chọn item, xoá tất cả.

⚠️ Phải phủ cả **thẻ con bên trong chip** (`.csp-chip *`, `.select2-selection__choice *`): chip dạng "Loại hình : Lĩnh vực" có `.csp-chip-group` tô xanh `#2563eb` riêng — không phủ thì nền chip đã xám mà chữ vẫn xanh.

---

## 4. Trạng thái focus của ô nhập liệu

Ô nhập / select / textarea khi được click vào **KHÔNG đổi màu viền sang xanh** (xanh lá thương hiệu hay xanh dương mặc định Bootstrap) và **không có quầng sáng** — chỉ đậm viền xám lên `#94a3b8`.

Đã xử lý sẵn ở 2 tầng, màn mới không phải khai gì:

- 10 component base: `V2BaseInput`, `V2BaseTextarea`, `V2BaseCodeInput`, `V2BaseDatePicker`, `V2BaseSelect`, `V2BaseSelectInModal`, `V2BaseFilterPanel`, `V2BaseSmartFilterPanel`, `SearchPicker`, `MultiSearchPicker`
- `assets/scss/v2-styles.scss`: rule chung `.form-control:focus, input:focus, select:focus, textarea:focus` — bắt cả input dùng `.form-control` thuần

Khi viết component mới có ô nhập: **cấm** đặt `border-color: #16a34a` / `box-shadow: rgba(22, 163, 74, …)` trong khối `:focus`.

**Nút xóa (×) trong ô lọc/select:** hover **không tô nền** (`background: transparent`), chỉ đổi ký tự × sang đỏ `#dc2626`. Không dùng nền `#fee2e2` hay bất kỳ nền nào. Đã sửa sẵn trong `V2BaseSelect` + `V2BaseSelectInModal`.

---

## 5. FE mới + BE cũ — luôn có đường lùi

Trên môi trường thật, FE và BE **không phải lúc nào cũng deploy cùng lúc**. Code FE dùng trường/endpoint mới phải chạy được cả khi BE chưa cập nhật, nếu không màn sẽ "trống trơn" mà không có lỗi nào hiện ra.

2 chỗ hay dính nhất:

- **Trường mới trong dữ liệu**: đừng để logic chỉ dựa vào 1 trường mới. Dùng chuỗi lùi dần, vd khoá nhận diện người thực hiện: `actor_id` → `actor_code` → `actor_name`; hiển thị: `actor_dept_code` → `actor_code` → chỉ tên.
- **Endpoint mới**: `catch` rồi **fallback về cách tính cũ**, đừng để mảng rỗng. Và fallback đó **không được dùng trường mới** — nếu không thì fallback cũng chết theo.

```js
performerKey(log) {
    if (log.actor_id) return String(log.actor_id)      // BE mới
    return String(log.actor_code || log.actor_name || '')  // BE cũ vẫn lọc được
},
```

Với mục 1 ở trên: BE chưa có `include_ids` thì tham số thừa bị bỏ qua, FE không vỡ — nhưng option khoá vẫn mất. Đây là lý do BE phải đi trước hoặc deploy cùng lượt.

Verify bằng cách **giả lập BE cũ ngay trên trình duyệt**: xoá trường mới khỏi dữ liệu rồi kiểm tra màn còn chạy không.

```js
vm.items = vm.items.map(({ actor_id, actor_dept_code, ...rest }) => rest)
vm.options = { actions: [], performers: [] }   // giả lập endpoint mới chưa có
```

---

## Tự kiểm trước khi báo xong

- [ ] Select danh mục ở màn Sửa: khoá danh mục đang được chọn → mở lại màn, giá trị **vẫn hiện đúng tên gốc**, lưu lại không mất dữ liệu
- [ ] Mở dropdown: option đã khoá có `🔒 ` đứng trước tên; chip/giá trị đã chọn **không** dính emoji
- [ ] Đã gọi lại API danh mục **sau khi** có dữ liệu bản ghi (không chỉ ở `mounted`)
- [ ] Select đi qua wrapper tự khai `templateResult` → đã tự gắn `LOCKED_OPTION_PREFIX`
- [ ] Ô disabled: nền `#f1f5f9`, chữ `#475569`, không `opacity`, không bấm được (kể cả ô dựng bằng `<div>`)
- [ ] Focus ô nhập: không viền xanh, không quầng sáng
