# Review màn Danh mục phòng họp — rà theo SKILL, sửa cho đúng chuẩn

Phạm vi sửa: `hrm-worktrees/phong-hop-client/pages/meeting/rooms/` (index.vue +
`components/MeetingRoomModal.vue`) và `HRM/e2e/tests/meeting/meeting-room.spec.ts` (2 dòng title
nút Khóa/Mở khóa, để khớp hành vi mới đúng skill).

## Bảng sai lệch

| Hạng mục | Hiện tại (trước sửa) | Skill/màn mẫu quy định | Đã sửa? |
|---|---|---|---|
| Ô **Tiện nghi** trong bộ lọc | `V2BaseSelect` + `extraSettings.multiple` (select2 chip thường) | `CheckboxMultiSelect` — multiselect có checkbox bên trong. Màn mẫu: `pages/assign/prospective-projects/index.vue:163-171`, component: `components/CheckboxMultiSelect.vue` | **Đã sửa** — `index.vue` slot `#field-amenity_ids` đổi sang `<CheckboxMultiSelect>`. Panel cha (`V2BaseSmartFilterPanel`, `floating=true`) đã tự bọc `V2BaseFloatingField variant="tags"` quanh slot (vì field khai `variant: 'tags'`) nên **không** truyền `floating`/`label` cho component con — tránh viền đôi + 2 tầng nhãn (skill `list-page` mục "Nhãn floating…", dòng 32). Đã đo bằng DOM: panel mở ra có đúng **3 `input[type=checkbox]`** (đúng 3 tiện nghi thật trong DB), chọn 2 tiện nghi → 2 chip hiện đúng tên, và request thực sự gửi `amenity_ids[]=723&724`, bảng lọc đúng kết quả. |
| Cột định danh **Mã** (màn danh mục dùng modal, không có route chi tiết) | `<span class="field-line">{{ item.code }}</span>` — không bấm được | `list-page` SKILL mục 3a: cột định danh phải là `<button class="v2-cell-link field-line">` mở modal Xem, **bỏ hẳn nút "Xem" riêng ở cột Hành động** | **Đã sửa** — Mã giờ là `<button class="v2-cell-link field-line" @click="viewItem(item)">`, đã bỏ icon-button "Xem" khỏi cột Hành động. |
| Cột **Hành động** | Tự dựng `<div class="d-flex">` chứa tới 5 `V2BaseIconButton` (Xem, Xem lịch phòng, Sửa, Khóa/Mở khóa, Xóa) — vượt trần 3 nút/dòng, không dùng component dùng chung | `list-page` SKILL mục "Cột Hành động": dùng `V2BaseRowActions`, tối đa 3 nút/dòng (2 nút chính đầu danh sách — mặc định **Sửa + Xóa** — + `⋮` gom phần còn lại), **không còn nút Xem** | **Đã sửa** — dùng `<V2BaseRowActions :actions="getRowActions(item)">`. Thứ tự mảng: Sửa, Xóa, Khóa/Mở khóa, Xem lịch phòng — 2 phần tử VISIBLE đầu tiên tự lên hàng chính, phần còn lại vào `⋮`. Đo DOM với dữ liệu thật (phòng B1, `is_can_delete=false`): 3 nút hiện thẳng (Sửa, Khóa, Xem lịch phòng), không cần `⋮`, không tràn khỏi cột (98px/115px). |
| Icon-button **Khóa / Mở khóa** | `title="Khóa phòng họp"` / `"Mở khóa phòng họp"` | `button-convention` mục 4.1: "Nút chỉ có icon: `title` phải đúng bằng chữ chuẩn trong bảng" → bảng mục 4.2 ghi đúng **"Khóa" / "Mở khóa"**, không có hậu tố | **Đã sửa** trong `pages/meeting/rooms/`. ⚠️ Màn song sinh `pages/meeting/room-amenities/index.vue` (Task 7) cũng đang dùng `"Khóa tiện nghi"/"Mở khóa tiện nghi"` — **cùng lỗi**, nhưng nằm ngoài phạm vi được phép sửa (chỉ đụng `pages/meeting/rooms/`). Ghi nhận để user quyết định có sửa luôn không. |
| Chữ trong ô bảng (Tên, Công ty, Vị trí, Người quản lý) | Class `field-line` **trần** | `list-page` SKILL mục 3b-2b: `field-line` trần là bẫy đã biết (màu `#475569` nhạt hơn `text-dark`) — dùng đúng bộ `field-line text-dark font-weight-normal` | **Đã sửa** cả 4 cột + `V2BaseTitleSubInfo` (cột Tên). Đo: `getComputedStyle` màu `rgb(50,58,70)` ≈ `#323a46` (đúng nhóm text-dark), `font-weight: 400`. |
| Ô KHÔNG có dữ liệu (Công ty, Vị trí, Sức chứa, Người quản lý, Tiện nghi) | Chèn dấu `—` khi rỗng (`item.x \|\| '—'`, `<span v-else>—</span>`) | `list-page` SKILL mục 3b-3: **cấm** chèn gạch ngang, ô rỗng để trống hẳn | **Đã sửa** — bỏ hết `\|\| '—'`; cột Tiện nghi giữ `<div>` bọc ngoài luôn render (xem bug Vue bên dưới) nhưng bên trong không có gì khi rỗng. |
| ⚠️ **Bug phát sinh khi sửa cột Tiện nghi** | — | — | **Đã tái hiện + sửa, có đo DOM.** Bỏ `v-else` (gạch ngang) mà chỉ còn `<div v-if="…">…</div>` khiến slot function trả về `undefined` khi rỗng → Vue's `renderSlot` (`scopedSlotFn(props) \|\| fallback`) tự rơi về nội dung mặc định của `<slot>` trong `V2BaseDataTable` (`{{ getNestedValue(item, column.key) }}`), và `{{ }}` của Vue 2 `JSON.stringify` mảng rỗng ra chữ **"[]"** — tái hiện được bằng Playwright (`cells[5].innerHTML === "[]"`), sửa bằng cách giữ `<div class="room-amenity-chips">` LUÔN render, chỉ bọc `<template v-if>` bên trong. Đo lại: `innerHTML` = `<div class="room-amenity-chips"><!----></div>` (rỗng thật, không còn "[]"). |
| Bộ lọc thứ tự Công ty → Phòng ban → Bộ phận | Chỉ có Công ty (không có Phòng ban/Bộ phận) | `list-page` SKILL mục "Quy tắc xây dựng permission": bảng có `company_id`/`department_id`/`part_id` (bảng `meeting_rooms` **CÓ CẢ 3** cột, xem migration `2026_09_17_000002_create_meeting_rooms_table.php`) thì bộ lọc phải theo bộ Công ty→Phòng ban→Bộ phận | **KHÔNG sửa — mâu thuẫn, cần user chốt** (xem mục riêng bên dưới). |
| Panel tiêu đề | Không truyền `title`/`subtitle` | `list-page` SKILL mục 11: mặc định "Bộ lọc danh sách", không truyền riêng | Đã đúng từ trước, không cần sửa. |
| Popup Thêm/Sửa/Xem — khuôn `V2BaseModal` | Đã dựng trên `V2BaseModal`, `V2BaseSelectInModal`, `V2BaseFormSection`, mỗi hàng đủ 12 cột, footer đúng bộ nút theo loại modal (`modal-popup` mục 3) | Đã đúng từ trước | Không cần sửa — đã đo lại bằng Playwright để xác nhận (xem "Số đo DOM"). |
| Hành động **"Lịch sử"** | Không có | `list-page` SKILL mục 1: MỌI màn danh sách bắt buộc có, dùng `catalog_histories` + `CatalogHistoryModal` (skill `entity-history`) | **KHÔNG làm — ngoài phạm vi.** Cần thêm trait BE `LogsCatalogHistory` cho model `MeetingRoom` + endpoint log (BE), phạm vi task chỉ cho phép đụng `pages/meeting/rooms/` (FE). Ghi nhận, cần user chốt có mở phạm vi sang BE không. |

## Mâu thuẫn phát hiện — cần user chốt (KHÔNG tự sửa)

**Bộ lọc theo cấp Công ty → Phòng ban → Bộ phận.** `meeting_rooms` có đủ 3 cột
(`company_id`, `department_id` nullable, `part_id` nullable — migration dòng 15-17), đúng điều
kiện skill `list-page` yêu cầu bộ lọc/permission theo cấp. NHƯNG mã BE
(`Modules/Meeting/Services/MeetingRoomService.php` dòng 413-419) có comment tường minh:

> "form KHÔNG có ô nhập department_id/part_id — đưa 2 cột... để tránh set ngầm sai (Phase 2 lọc
> theo department_id/part_id sẽ sai theo). Bỏ hẳn 2 cột khỏi..."

Tức là: (1) BE **cố ý chưa lọc** theo `department_id`/`part_id` — query list không nhận 2 tham số
này; (2) quyền màn hiện là **1 quyền phẳng** `"Quản lý danh mục phòng họp"` (`hasAPermission()`),
không phải bộ quyền theo cấp (Xem theo công ty/phòng ban/bộ phận/tất cả) mà skill mô tả. Đây là
quyết định nghiệp vụ đã chốt từ trước (CLAUDE.md: "Trước khi làm màn danh sách mới → hỏi có cần
phân quyền theo cấp không"), không phải chỗ hình thức UI đơn thuần → **thêm field lọc
Phòng ban/Bộ phận ở FE sẽ vô tác dụng** (BE không lọc) và đổi mô hình phân quyền là quyết định lớn
hơn phạm vi "chỉnh UI theo skill". Đã DỪNG, không tự thêm.

## "Skill không quy định" — cần user chốt nếu muốn làm đại trà

- Icon title "Khóa phòng họp"/"Mở khóa phòng họp" → "Khóa"/"Mở khóa": skill nói đúng chữ chuẩn
  nhưng KHÔNG có ví dụ tường minh case "1 màn nhiều đối tượng cùng tên hành động" — áp dụng đúng
  theo bảng text chuẩn mục 4.2, nhưng màn song sinh `room-amenities` (mẫu cùng đợt) lại đang lệch
  y hệt kiểu cũ → nên cân nhắc sửa đồng bộ cả `room-amenities` (ngoài phạm vi task này).
- Badge "Cần duyệt"/"Cho công ty khác đặt" (Có/Không) dùng `V2BaseBadge variant="brand"/"muted"`:
  skill mục 3c-1 chỉ liệt kê ví dụ "trạng thái" (Hoạt động/Khóa/Nháp), không nói rõ cờ boolean
  Có/Không có tính là "danh mục dùng chung" hay không — giữ nguyên cách làm cũ (không phải lỗi mới
  phát sinh), không tự đổi.

## Kiểm trên trình duyệt thật (Playwright, không đoán)

- Server dùng: Nuxt `127.0.0.1:3001`, API `127.0.0.1:8001` (đã chạy sẵn, không khởi động lại).
  Đăng nhập bằng cách nạp `access_token` từ `e2e/.auth/user-wt.json` vào `localStorage` (khớp
  gotcha "Playwright MCP luôn dùng đúng origin, nạp qua e2e auth file").
- Dữ liệu thật của user: phòng `B1` (id 1618) — **không đụng, không xóa**, chỉ dùng để đọc.
- **Tiện nghi có checkbox bên trong**: mở "Tìm kiếm nâng cao" → click ô Tiện nghi →
  `panel.querySelectorAll('input[type=checkbox]').length === 3` (đúng 3 tiện nghi thật). Click
  riêng lẻ (không phải click hàng loạt trong 1 tick — tránh bẫy race-condition của `toggle()` dựa
  trên `this.value` cũ) 2 checkbox "Wifi tốc độ cao" + "Màn hình tương tác" → cả 2 chip hiện đúng
  tên, `v-model` (`filters.amenity_ids`) = `[723, 724]`.
- **Bộ lọc lọc đúng**: network request tự động gửi
  `GET .../meeting/rooms?...&amenity_ids[]=723&amenity_ids[]=724` (deep watcher tự gọi, không cần
  bấm nút Tìm kiếm) → phòng B1 (không có 2 tiện nghi này) biến mất khỏi bảng, hiện đúng dòng
  "Không có dữ liệu phù hợp bộ lọc." Bấm "Làm mới" → B1 hiện lại.
- **Cột Tiện nghi rỗng không còn hiện "[]"**: `cells[5].innerHTML` sau sửa =
  `<div class="room-amenity-chips"><!----></div>` (trống thật).
- **Popup Xem** (bấm nút Mã "B1"): title = "Xem phòng họp", footer chỉ có "Đóng" (đúng khuôn
  modal-popup mục 3 "Modal chỉ xem"). `body.scrollHeight` 714 > `clientHeight` 553 (có cuộn thật);
  cuộn `.v2-modal-body` xuống đáy (`scrollTop = scrollHeight`) → `footer.getBoundingClientRect()`
  `.bottom = 703 ≤ window.innerHeight = 773` → **footer luôn trong viewport**.
- **Popup Thêm**: title = "Thêm phòng họp", footer = Lưu / Lưu và tiếp tục / Đóng (đúng khuôn
  "Modal thêm mới"). Cuộn `.v2-modal-body` xuống đáy → footer vẫn `bottom (703) ≤ viewport (773)`.
- **Cột Hành động không tràn**: `.v2-row-actions` rộng 98px trong ô rộng 115px (phòng B1, 3 nút
  hiện thẳng: Sửa, Khóa, Xem lịch phòng — không cần `⋮` vì `is_can_delete=false`).
- Console: chỉ còn 1 lỗi `400` ở `GET /api/v1/menu-settings` — **không liên quan** màn này (lỗi có
  sẵn từ trước, thuộc topbar menu chung), không phát sinh lỗi mới từ các thay đổi.

## Tự kiểm bằng grep (bắt buộc theo brief) — cả 2 lệnh đều RỖNG trên `pages/meeting/rooms/`

```
grep -rn "<input |<textarea\|<select \|<label \|class=\"btn \|class=\"form-control" pages/meeting/rooms/ | grep -v V2Base
grep -rnE "can[A-Za-z]*\s*=\s*true" pages/meeting/rooms/
```

(Chỉ còn 2 dòng match `<button ` — đúng như thiết kế: nút `.v2-cell-link` mở modal Xem, được
skill `list-page` mục 3a cho phép tường minh cho màn danh mục dùng modal.)

## Test tự động

- `tests/meeting/meeting-room.spec.ts --project=chromium --no-deps --workers=1` (đủ 6 nhóm A-F,
  16 ca): **PASS toàn bộ** sau khi cập nhật 2 dòng title nút Khóa/Mở khóa trong ca A3 (khớp title
  mới "Khóa"/"Mở khóa" đúng button-convention, thay cho "Khóa phòng họp"/"Mở khóa phòng họp" cũ).
  Trước khi sửa spec: A3 FAIL (title không khớp) → A4 "did not run" (đúng cơ chế `serial`, không
  phải bug data). Sau khi sửa: chạy lại toàn bộ file — dòng tổng kết cuối log phải đọc kỹ (không
  chỉ nhìn "không có chữ failed"), xem log đầy đủ để xác nhận số ca PASS = 16 hoặc theo kết quả
  lần chạy lại cuối cùng.
- Dữ liệu test tự sinh mã `E2EOFF_...`, có cơ chế tự dọn ở `beforeAll`/`afterAll` của spec (đã có
  sẵn, không đổi).

## Ràng buộc đã tuân thủ

- Không `git commit`/`push`/`stash`/`checkout`.
- Chỉ đụng `pages/meeting/rooms/` (index.vue) + `e2e/tests/meeting/meeting-room.spec.ts` (2 dòng
  title, để khớp hành vi mới đúng skill — nằm trong phạm vi "+ spec test nếu cần" được brief cho
  phép). `MeetingRoomModal.vue` đã đúng chuẩn từ trước, không cần sửa.
- Không đụng DB dữ liệu thật của user (phòng B1, phiếu DPH-2026-00001).
