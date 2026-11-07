# QA UI — Màn "DM mẫu báo giá vận chuyển" (DeliveryQuotation)

Màn: `pages/transport/delivery-quotations` (Tạo mới / Sửa / Chi tiết dùng chung
`components/DeliveryQuotationForm.vue`). Các mục QA do user gửi qua ảnh chụp giao diện.

## Item 1 — Thêm dấu `*` vào các trường bắt buộc (2026-11-03) — DONE

**Hiện trạng:** Khối "Thông tin chung" đã đánh dấu đúng (`Ngày hiệu lực từ/đến`, `Số Km tính cước
vượt trội` có `*` qua `V2BaseLabel required`; `Áp dụng cho bảng giá hiệu lực` không `*` vì
`price_list_valid_id` nullable — chuẩn). **Thiếu `*` ở bảng cước theo tuyến đường.**

**Đối chiếu BE** (`DeliveryQuotationStoreRequest` / `UpdateRequest`) — cả 4 trường trong bảng cước
đều `required`:
- `roads.*.road_id` → required  → cột **Tuyến đường**
- `roads.*.km` → required        → cột **Số Km**
- `vehicles.*.vehicle_category_id` → required → header select **Chọn loại xe**
- `vehicles.*.payloads.*.vehicle_payload_id` → required → header select **Chọn trọng tải**

**Đã sửa** `DeliveryQuotationForm.vue`:
- [x] Header "Tuyến đường" + `<span v-if="!readonly" class="text-danger">*</span>`
- [x] Header "Số Km" + `*` (cùng pattern)
- [x] Ô header "Chọn loại xe" (V2BaseSelect) — thêm `*` đầu cell flex (`cell-vehicle`)
- [x] Ô header "Chọn trọng tải" (V2BaseSelect) — thêm `*` đầu cell flex (`cell-payload`)
- Pattern bám theo quy ước đánh dấu cột bắt buộc trong `<th>` dùng chung toàn hệ thống
  (`<span v-if="!readonly" class="text-danger">*</span>`), guard `!readonly` để màn Chi tiết
  (readonly=true) không hiện `*`.
- [x] Verify Playwright màn Tạo mới (`/transport/delivery-quotations/create`): cả 4 `*` đỏ
      hiện đúng; màn Chi tiết (`_id/index.vue`, readonly) KHÔNG hiện `*` (guard `!readonly`).

## Item 2 — Cắt bớt khoảng trắng trong màn hình (2026-11-03) — CHỜ USER QUYẾT

User gửi ảnh QA mục 2, mũi tên chỉ (a) khoảng trắng trên đầu giữa topbar (thanh xanh lượn sóng,
tiêu đề "Thêm mẫu báo giá vận chuyển") và khối "Thông tin chung", (b) lề trái.

**Điều tra (đo DOM + chụp so sánh):** khoảng cách của màn này ĐÚNG BẰNG màn chuẩn đã QA
(`/sale/price-asking-requests/add`), không dư riêng:

| | DeliveryQuotation create | YC hỏi giá (đã QA) |
|---|---|---|
| `.content-page` padding-top | 70px | 70px |
| `.content-page` padding-left | 5px | 5px |
| Khối đầu `section.top` | 70px | 70px |
| Khối đầu `section.left` | 68px | 68px |

→ Đây là **layout chung `default-sidebar`** (padding-top 70px chừa chỗ topbar cố định; wrapper
`v2-styles ... pt-2` + `container-fluid` giống hệt các màn khác). Cắt riêng màn này sẽ làm nó
LỆCH với mọi màn khác (phạm nguyên tắc "màn HRM phải giống các màn HRM khác"). Muốn giảm thật
phải sửa layout/wrapper DÙNG CHUNG → ảnh hưởng toàn bộ màn form → **phải hỏi user trước** (CLAUDE.md:
không tự sửa component/layout dùng chung).

- [x] **User chốt (2026-11-03): Hướng A — GIỮ NGUYÊN** để đồng bộ với mọi màn form khác.
      KHÔNG đổi code. Khoảng trắng là layout chung `default-sidebar`, không bóp riêng màn này.

## Item 3 — Ẩn nút Tìm kiếm, bấm thẳng ô chọn tuyến đường (2026-11-03) — DONE

User gửi ảnh QA mục 3, mũi tên chỉ nút kính lúp (`ri-search-line`) đứng cạnh ô "Chọn tuyến đường"
trong mỗi dòng bảng cước. Yêu cầu: **ẩn nút Tìm kiếm riêng, chỉ để ô — bấm thẳng vào ô mở popup
chọn tuyến** (gọn hơn, bớt 1 nút thừa mỗi dòng).

**Phạm vi:** chỉ ô `col-road` trong `DeliveryQuotationForm.vue` (screen-local, KHÔNG phải component
dùng chung) → sửa trực tiếp, không cần hỏi.

**Đã sửa** (`DeliveryQuotationForm.vue`):
- [x] Bỏ `V2BaseIconButton` (nút kính lúp `ri-search-line`) trong cell `col-road`.
- [x] Bọc `V2BaseInput` trong wrapper `.cell-road` gắn `@click="openRoadPicker(ri)"` (guard
      `!readonly`). Input giữ `disabled` cho đúng kiểu ô khoá dùng chung; wrapper bắt click.
- [x] SCSS: `.cell-road--pickable { cursor: pointer }` + input con `pointer-events: none` để click
      xuyên xuống wrapper (disabled input tự chặn click nên phải để wrapper nhận).
- [x] Verify Playwright màn Tạo mới: bấm vào ô → popup chọn tuyến mở; chọn tuyến → tên điền vào ô;
      màn Chi tiết (readonly) không mở popup khi bấm.

## Item 4 — Cố định kích thước cột khi thêm loại xe (2026-11-03) — DONE

User gửi ảnh QA mục "5": khi bấm **Thêm loại xe**, cột **Số Km** bị co nhỏ lại (chữ lỗi
"Không được nhỏ hơn 1." bị ngắt 3 dòng trong ô hẹp). Yêu cầu: **cố định bề rộng cột** để không
đổi khi thêm cột.

**Nguyên nhân:** bảng cước `.matrix-table` dùng `width:100% + table-layout:auto` ⇒ các cột chia
đều để lấp đúng 100% container. Thêm loại xe làm cột dồn lại → Số Km co dần (đo DOM: 330.3px @1 xe
→ 216.1px @3 xe).

**Phạm vi:** chỉ SCSS screen-local trong `DeliveryQuotationForm.vue` (bảng cước, không phải
component dùng chung) → sửa trực tiếp, không cần hỏi.

**Đã sửa** (`DeliveryQuotationForm.vue`, khối SCSS `.matrix-table`):
- [x] Đổi `table-layout: auto` → `table-layout: fixed`; khai `width` cố định cho từng cột
      (`col-road` 280px, `col-km` 120px, `col-vehicle`/`col-payload`/`col-payload-cell` 190px).
- [x] Cột Hành động cuối (nút × xoá tuyến) KHÔNG khai `width` → auto, tự hút phần dư. Khi tổng
      bề rộng vượt container, bảng tràn ngang vào `V2BaseTableScroll` (thanh cuộn trên+dưới),
      nên Số Km / Tuyến đường luôn giữ nguyên bề rộng.
- [x] Verify Playwright: `tableLayout='fixed'`; Số Km = **120px** cố định qua 1 / 3 / 7 loại xe
      (trước fix: 330→216px); 7 loại xe → bảng 1765px > container 1407px, tràn vào scroll thay vì
      bóp cột. Ma trận render đúng (rowspan Tuyến đường/Số Km + colspan loại xe vẫn chuẩn dưới
      fixed layout). Ảnh: `.playwright-mcp/item4-fixed-layout-7vehicles.png`.

## Item 5 — Thay icon xoá bằng icon thùng rác (2026-11-03) — DONE

User gửi ảnh QA mục "1": các nút xoá trong bảng cước đang dùng dấu `×` (xoá loại xe / trọng tải)
và `−` (xoá tuyến đường). Yêu cầu: **đổi sang icon thùng rác như các màn khác**.

**Đối chiếu:** icon thùng rác chuẩn toàn hệ thống là `ri-delete-bin-line` (254 chỗ dùng, nhiều
nhất).

**Đã sửa** (`DeliveryQuotationForm.vue`, 3 nút `V2BaseIconButton danger`):
- [x] Nút xoá loại xe (`removeVehicle`): `ri-close-line` → `ri-delete-bin-line`.
- [x] Nút xoá trọng tải (`removePayload`): `ri-close-line` → `ri-delete-bin-line`.
- [x] Nút xoá tuyến đường (`removeRoad`, cột Hành động): `ri-subtract-line` → `ri-delete-bin-line`.
- [x] Verify Playwright: cả 3 nút hiện icon thùng rác đỏ, không còn `ri-close-line`/`ri-subtract-line`
      trong ma trận. Ảnh: `.playwright-mcp/item1-trash-icons.png`.

## Item 6 — Cache thông báo lỗi khi xóa / thêm lại loại xe (2026-11-03) — DONE

User gửi ảnh QA mục "2": "Cache thông báo lỗi. Sửa tương tự khi xóa và thêm lại loại xe". Câu lỗi
(422 lần Lưu trước) của bảng cước bị **dính nhầm sang dòng khác** sau khi xóa / thêm lại một loại xe
(hoặc trọng tải / tuyến đường).

**Nguyên nhân:** `formError` đánh key theo **chỉ số dòng** (`vehicles.0.vehicle_category_id`,
`roads.1.km`, `vehicles.0.payloads.0...`). `errorOf()` đọc thẳng theo chỉ số. Khi `splice` xóa/thêm
một phần tử, chỉ số mảng dồn lại nhưng `formError` **không được dọn** → lỗi index cũ hiện trên dòng
đã dồn (hoặc dòng mới thêm vào ở chỉ số tái dùng). Tái hiện: 2 loại xe mỗi loại 1 lỗi, xóa loại #0 →
dòng còn lại (vốn #1) hiện lỗi của loại #0 đã xóa; cả 2 key cũ vẫn nằm trong `formError`.

**Phạm vi:** chỉ `DeliveryQuotationForm.vue` (screen-local) → sửa trực tiếp, không cần hỏi.

**Đã sửa** (`DeliveryQuotationForm.vue`):
- [x] Thêm helper `dropErrors(prefix)` — xóa mọi key `formError` thuộc nhánh mảng đó (`prefix` và
      `prefix.*`), gán lại object mới cho reactive.
- [x] Gọi `this.dropErrors('vehicles')` trong `addVehicle` / `removeVehicle` / `addPayload` /
      `removePayload`; `this.dropErrors('roads')` trong `addRoad` / `removeRoad`. Lỗi snapshot biến
      mất khi cấu trúc đổi; lần Lưu kế BE validate lại và trả lỗi đúng theo chỉ số mới.
- [x] Verify Playwright: inject lỗi index-keyed rồi `removeVehicle(0)` → dòng còn lại không còn lỗi
      "ma", `formError` sạch; `addVehicle` sau lỗi cũ → `formError` rỗng; `removeRoad(0)` tương tự.

## Item 7 — Popup "Thêm nhanh tuyến đường": ẩn chú thích + thêm icon nút (2026-11-03) — DONE

User gửi ảnh QA mục "1" trên popup **Thêm nhanh tuyến đường** (`QuickAddRoadModal.vue`): (a) dòng
chú thích xám "Thêm toàn bộ tuyến theo điểm xuất phát và tỉnh đã chọn." thừa → **ẩn**; (b) 2 nút
footer **Đóng** / **Áp dụng** chưa có icon đầu nút → **thêm icon** theo chuẩn button-convention.

**Phạm vi:** chỉ `QuickAddRoadModal.vue` (component popup screen-local của màn delivery-quotations)
→ sửa trực tiếp, không cần hỏi.

**Đã sửa** (`QuickAddRoadModal.vue`):
- [x] Bỏ `<div class="note-text">…</div>` chú thích + xóa luôn khối `<style>` chứa `.note-text`
      (không còn chỗ dùng).
- [x] Nút **Đóng** (`tertiary`): thêm `#prefix` icon `fas fa-arrow-left` (`margin-right:3px`) — đúng
      chuẩn nhóm Thoát/Hủy/Quay lại.
- [x] Nút **Áp dụng** (`primary`): thêm `#prefix` icon `ri-check-line` (`font-size:15px`) — đúng
      chuẩn nhóm Xác nhận/Duyệt/Áp dụng. Thứ tự footer: Đóng (trái) → Áp dụng chính... (theo mẫu
      modal: nút chính bên trái, nhưng ở đây giữ nguyên cụm hiện có; không đổi thứ tự vì QA chỉ yêu
      cầu icon).
- [x] Verify Playwright: mở modal → `noteGone: true`; nút Đóng có `fas fa-arrow-left`, nút Áp dụng
      có `ri-check-line`. Ảnh xác nhận: không còn dòng xám, 2 nút đủ icon.

## Item 8 — Popup "Chọn tuyến đường": ẩn chú thích (2026-11-03) — DONE

User gửi ảnh QA mục "2. Ẩn chú thích" trên popup **Chọn tuyến đường** (`RoadPickerModal.vue` — mở
khi bấm ô "Chọn tuyến đường" trong bảng cước). Dòng xám "Chọn một tuyến để thêm vào bảng cước." thừa
→ **ẩn**. (Khác popup Thêm nhanh ở Item 7.)

**Phạm vi:** chỉ `RoadPickerModal.vue` (component popup screen-local) → sửa trực tiếp, không cần hỏi.

**Đã sửa** (`RoadPickerModal.vue`):
- [x] Bỏ `<div class="mt-2 note-text">Chọn một tuyến để thêm vào bảng cước.</div>`.
- [x] Xóa khối `<style>` chứa `.note-text` (không còn chỗ dùng).
- [x] Verify Playwright: mở modal (`RoadPickerModal.open(0)`) → `noteGone: true`, `.note-text`
      không còn trong DOM; popup chỉ còn nhãn "Tuyến đường" + ô tìm + nút Đóng. Ảnh:
      `item8-road-picker-no-note.png`.

## Item 9 — Popup "Thêm nhanh tuyến đường": lỗi validate TOAST → message đỏ inline (2026-11-03) — DONE

User gửi ảnh QA mục "3. NHập lỗi đang báo ở dạng toast -> đổi thành message đỏ ở dòng bị lỗi" trên
popup **Thêm nhanh tuyến đường** (`QuickAddRoadModal.vue`). Bấm **Áp dụng** khi chưa chọn Điểm xuất
phát / Tỉnh thì hiện **toast cam** "Vui lòng chọn điểm xuất phát và tỉnh" → sai khuôn validate
(skill `form-validate`: lỗi của trường hiện ĐỎ INLINE ngay dưới ô, không dùng toast).

**Phạm vi:** chỉ `QuickAddRoadModal.vue` (popup screen-local) → sửa trực tiếp. Popup danh mục KHÔNG
có "Lưu nháp" → được phép gate `required` ở FE bằng vee-validate (ngoại lệ mục 1 skill form-validate).

**Đã sửa** (`QuickAddRoadModal.vue`):
- [x] Import + `mixins: [formValidateMixin]`, thêm component `V2BaseError`.
- [x] Mỗi `V2BaseSelectInModal` gắn `v-validate="'required'"` + `data-vv-name`
      (`start_point_id` / `province_id`) + `data-vv-as` ("Điểm xuất phát" / "Tỉnh/Thành") +
      `data-vv-value-path="currentValue"` + `:invalid="hasFieldError(...)"` (viền đỏ qua prop
      `invalid` của `v2ValidateMixin`, KHÔNG bind `:class="is-invalid"`) + `@input="clearFieldError(...)"`.
- [x] Dưới mỗi ô: `<V2BaseError :message="fieldError(...)" />` → hiện "Bắt buộc phải nhập" (câu chuẩn
      `locales/vi.json`, không tiền tố tên trường).
- [x] `apply()`: bỏ nhánh `toastWarning('Vui lòng chọn điểm xuất phát và tỉnh')`, thay bằng
      `await this.$validator.validateAll()` — sai thì return, lỗi tự hiện inline. (Giữ `toastWarning`
      cho lỗi tải danh mục / tải tuyến vì đó là lỗi hệ thống, không phải lỗi trường.)
- [x] `open()`: gọi `resetValidation()` để ErrorBag lần mở trước không dính lại.
- [x] Verify Playwright: mở popup → `apply()` khi trống → `fieldError('start_point_id')` =
      `fieldError('province_id')` = "Bắt buộc phải nhập", `hasFieldError` = true cả 2, KHÔNG toast.
      Ảnh `item9-quickadd-inline-error.png`: 2 ô viền đỏ + dòng lỗi đỏ có icon cảnh báo ngay dưới ô.

## Item 10 — Form chính: thêm nút "Lưu nháp" + "Lưu và tiếp tục" (2026-11-03) — DONE

User (ảnh "DM mẫu báo giá vận chuyển - Tạo mới - Validate", mục 1): "Thêm nút Lưu nháp và Lưu tiếp
tục: Cả 2 chỉ cần validate ngày hiệu lực, sau khi lưu chuyển thành trạng thái đang tạo".

**SKILL vs SPEC — user CHỐT hướng 1 (SKILL thắng SPEC, ghi design.md "Quyết định đã chốt"):**
- **Lưu nháp** = chỉ bắt buộc ngày hiệu lực (nới `required` của xe/trọng tải/tuyến/km_actual); rule
  ĐỊNH DẠNG vẫn chặn ở mọi kiểu lưu (`form-validate` mục 1). Lưu xong → về danh sách.
- **Lưu và tiếp tục** = validate ĐỦ như nút **Lưu** (spec ghi "chỉ validate ngày" nhưng skill
  button-convention/form-validate: Lưu-và-tiếp-tục = lưu đầy đủ, khác Lưu ở chỗ ở lại form tạo tiếp).
- Trạng thái "đang tạo" (`DANG_TAO = 3`): `store()` ĐÃ luôn set DANG_TAO, `update()` không đổi
  status → "sau khi lưu → đang tạo" thỏa sẵn.

**Đã sửa:**
- [x] FE `DeliveryQuotationForm.vue`: `footerMenu()` trả `submit_and_draft` + `submit_form`
      (+ `submit_and_continue` khi tạo mới; sửa thì không có "tiếp tục"). `V2Footer` bắt
      `@submitAndDraft` / `@submitForm` / `@submitAndContinue`. 3 nút emit thẳng, không popup xác
      nhận (không thuộc nhóm duyệt của V2Footer). Thứ tự nút do V2Footer tự xếp (Lưu nháp đầu).
- [x] FE: `buildPayload(draft)` gắn `is_draft: draft ? 1 : 0`; `submit/submitDraft/submitContinue`
      gọi chung `doSave({draft, stayOnForm})`; `stayOnForm=true` → `resetForm()` ở lại tạo tiếp,
      ngược lại `$router.push('/transport/delivery-quotations')`.
- [x] BE `DeliveryQuotationStoreRequest` + `DeliveryQuotationUpdateRequest`: `rules()` rẽ theo
      `is_draft` — nháp nới `required`→`nullable` cho vehicles/payloads/roads/km_actual, giữ nguyên
      ngày hiệu lực + mọi rule định dạng (`exists`/`numeric`/`date`/`max`).
- [x] BE `DeliveryQuotationService`: `km_actual ?? 0`; thêm `sanitizeDetails()` bỏ dòng con CHƯA đủ
      khoá ngoại trước `syncDetails` (bảng con `vehicle_category_id`/`vehicle_payload_id`/`road_id`
      đều NOT NULL, syncDetails không tự lọc null → nháp gửi mảng mặc định null FK sẽ nổ ràng buộc).
      No-op với bản lưu đầy đủ. Áp cả `store()` lẫn `update()`.
- [x] Verify (tinker, tài khoản test 403 trên POST/PUT UI nên verify tầng validator + service):
      - Nháp tối thiểu (chỉ ngày, xe/tuyến null) → validate PASS; `store()` OK, status=3 DANG_TAO,
        0 dòng xe con / 0 dòng tuyến con, KHÔNG nổ NOT NULL (chạy trong transaction rollback).
      - Lưu đầy đủ thiếu xe/tuyến → FAIL đủ 5 khoá (km_actual + vehicle + payload + road).
      - Nháp km_actual = "abc" → FAIL km_actual (rule định dạng luôn bật).
      - `sanitizeDetails`: null FK → `[]`/`[]`; đủ FK → giữ nguyên.

## Item 11 — Ghi chú: đồng bộ logic Thêm/Sửa (2026-11-03) — DONE

User (mục 2): "Khi thêm đang k bắt buộc nhập ghi chú nhưng khi sửa lại bắt buộc => đồng bộ lại
logic". Trước: StoreRequest `note=nullable` còn UpdateRequest `note=required` → lệch.

**Đã sửa:**
- [x] BE `DeliveryQuotationUpdateRequest.php`: `note` `required|max:1000` → `nullable|max:1000`
      (đồng bộ Store). Cập nhật docblock.
- [x] FE `DeliveryQuotationForm.vue`: nhãn `<V2BaseLabel :required="noteRequired">` →
      `<V2BaseLabel>Ghi chú` (bỏ dấu `*`); gỡ computed `noteRequired` không còn dùng.
- [x] Verify FE (create): ô Ghi chú không còn dấu `*`, `noteRequired` không còn tồn tại.
      Edit-mode: 403 trên tài khoản test (DNS Admin thiếu quyền màn này) chặn mở bản ghi qua UI,
      nhưng rule BE nay `nullable` ở CẢ Store lẫn Update (đã đọc xác nhận 2 file) → không còn bắt
      buộc ở chế độ sửa.

## Item 12 — Message ngày hiệu lực đến < ngày hiệu lực từ (2026-11-03) — DONE

User (mục 3): "Sửa lại thông báo khi nhập ngày hiệu lực đến < ngày hiệu lực từ". Trước: rule
`after_or_equal` ra câu mặc định "Không hợp lệ" — người lập không biết sai ở đâu.

**Đã sửa:**
- [x] BE thêm `messages()` ở CẢ `DeliveryQuotationStoreRequest.php` và
      `DeliveryQuotationUpdateRequest.php`:
      `'date_valid_to.after_or_equal' => 'Ngày hiệu lực đến phải sau hoặc bằng ngày hiệu lực từ'`.
      (Được phép khai `messages()` vì là câu NGHIỆP VỤ so sánh 2 ngày mà lang file không diễn đạt
      được — ngoại lệ CLAUDE.md.) FE `DeliveryQuotationForm.vue` đã có sẵn
      `<V2BaseError :message="errorOf('date_valid_to')" />` → câu 422 hiện inline đúng dưới ô.
- [x] Verify: UI submit trả 403 (tài khoản test thiếu quyền, validate không chạy) → verify trực
      tiếp bằng `Validator::make` với rule+messages, payload `date_valid_to < date_valid_from` →
      trả đúng "Ngày hiệu lực đến phải sau hoặc bằng ngày hiệu lực từ".

## Item 13 — Số Km âm: chặn nhập số âm (2026-11-03) — DONE

User (mục 4): "NHập số km là số âm đang báo lỗi k đúng -> chặn nhập số âm luôn". Trước: gõ "-92" ở
"Số Km tính cước vượt trội *" hiện nhầm "Bắt buộc phải nhập".

**Đã sửa** (`DeliveryQuotationForm.vue`) — theo pattern có sẵn của `V2BaseInput` (chặn phím `-`/`e`/
`+` ở `onKeydown`/`onPaste` khi input có `min` >= 0, Redmine #11377 BUG 2):
- [x] Ô `km_actual` (Số Km tính cước vượt trội): thêm `min="0"`.
- [x] Ô `road.km` (Km mỗi tuyến trong bảng cước): thêm `min="1"` (khớp rule BE `roads.*.km` min:1).
- [x] Các ô ma trận cước là `V2BaseInput disabled` (không nhập tay) → không cần min.
- [x] Verify Playwright: gõ "-92" vào `km_actual` → giá trị ô = "92" (phím `-` bị chặn ngay lúc
      gõ), KHÔNG còn hiện "Bắt buộc phải nhập". Synthetic keydown `-` → `minusKeyPrevented = true`.

## Item 14 — Danh sách thêm cột Trạng thái, Người cập nhật, Ngày cập nhật (2026-11-04) — DONE

- [x] BE `DeliveryQuotation`: hằng `DA_TONG_HOP`, `STATUS_META`, `statusMetaOf()`; `updatedAt` vào cột sort.
- [x] BE `DeliveryQuotationListResource`: `status_text` / `status_color`, `updater_name`, `updated_at`.
      `DeliveryQuotationController::index` eager load `employee_create.info`, `employee_update.info` (không N+1).
- [x] FE `pages/transport/delivery-quotations/index.vue`: cột `status` (`V2BaseBadge`, màu BE),
      `updatedByName`, `updatedAt` (sortable). Màu/chữ theo QĐ2 `design.md`.
- [x] Verify Playwright: BGVC-00089 "Đang tạo" badge `#64748B`; BGVC-00088/87 "Đã lập tổng hợp giá";
      Người cập nhật ra tên; Ngày cập nhật có giờ.

## Item 15 — Lịch sử ở danh sách + chi tiết (2026-11-04) — DONE

- [x] BE `DeliveryQuotationService`: ghi lịch sử store / update / destroy qua `LogsCatalogHistory`, khoá ảo
      `vehicle_rows` / `road_rows`; `logStatusSummarized()` ghi "Thay đổi trạng thái".
- [x] BE `DeliveryCostSummaryService::store`: lập THGVC → set mẫu báo giá `DA_TONG_HOP` + ghi log trạng thái.
- [x] BE `CatalogHistoryService::TABLES['delivery_quotations']` (nhãn 5 trường + 2 khoá ảo + status).
      ⚠️ Lần đầu đặt nhầm vào `GATED_TABLES` → endpoint chung trả 400 "Loại đối tượng không hợp lệ";
      đã chuyển sang `TABLES`.
- [x] FE danh sách: row action "Lịch sử" (`ri-history-line`) → `CatalogHistoryModal`.
- [x] FE chi tiết `_id/index.vue`: khối `SystemInfoSection` (`endpoint-base="catalog-histories"`).
- [x] Test script (tạo / không đổi / 7 ca sửa / đổi trạng thái / xóa) FAILS=0.
- [x] Verify Playwright: popup danh sách và khối chi tiết BGVC-00089 đều hiện 2 lần "Thay đổi thông tin"
      (Ghi chú + Tuyến đường sửa Km 24↔30) — dữ liệu test cố ý tạo trên DB local.

## Item 16 — Ngày tạo hiển thị kèm giờ (2026-11-04) — DONE

- [x] BE Resource format `created_at` `d/m/Y H:i`; FE nới cột Ngày tạo 150px.
- [x] Verify Playwright: "08/05/2026 15:45".

## Item 17 — Dropdown "Áp dụng cho bảng giá hiệu lực": ERP 3 bảng, HRM 7 bảng (2026-11-04) — DONE

- [x] Nguyên nhân: lookup HRM thiếu lọc công ty mà ERP có (`company_id` của người đăng nhập).
- [x] BE `DeliveryQuotationLookupController`: `scopeCurrentCompany()` + `include_ids` cho `priceLists`;
      `priceListData` cùng phạm vi.
- [x] BE `DeliveryQuotationStoreRequest` / `UpdateRequest`: `Rule::exists` theo phạm vi công ty
      (Update cho qua bảng giá phiếu đang dùng).
- [x] FE `DeliveryQuotationForm.vue`: `loadOptions(..., includePriceListIds)`; nhân bản xoá bảng giá ngoài phạm vi.
- [x] Test script FAILS=0 (9 ca: danh sách, include_ids, priceListData khác cty, store/update hợp lệ + bị chặn).
- [x] Verify Playwright `/create`: dropdown còn đúng BGHLVC-00007 / 00005 / 00002 (user cty 1);
      chi tiết BGVC-00088 vẫn hiện BGHLVC-00003 (cty 3) nhờ `include_ids`. Quyền test gán tạm local đã gỡ.

## Item 18 — Thiếu dòng "Giá cước vượt trội" trong ma trận (2026-11-04) — DONE

- [x] FE `DeliveryQuotationForm.vue`: thêm dòng `thead` thứ 3 "Giá cước vượt trội | - | ô khoá mỗi tải trọng"
      (+ ô cột hành động riêng khi không readonly vì ô hàng 1 chỉ `rowspan=2`). Không lưu dữ liệu — QĐ3.
- [x] Excel đã có sẵn dòng này, không sửa.
- [x] Verify Playwright: hiện ở Tạo mới và Chi tiết BGVC-00088.

## Item 19 — Số Km hiện "118,00" + cột trọng tải bị bóp hẹp (2026-11-04, phát hiện khi verify Item 17–18) — DONE

**Nguyên nhân:**
- Km: BE trả cột decimal `"118.00"`, ô `V2BaseInput type=number` hiện theo locale trình duyệt → máy tiếng Việt ra `118,00`.
- Cột hẹp: bảng `table-layout: fixed` lấy bề rộng theo HÀNG ĐẦU; ô loại xe ở hàng đầu có `colspan=N` mà chỉ khai
  `width: 190px` → N cột trọng tải chia nhau 190px (vd xe có 5 tải trọng → mỗi cột ~38px, chữ bị cắt).

- [x] FE `DeliveryQuotationForm.vue`: hàm `kmText()` chuẩn hoá km (`Number()` → `"118"`, `"15.5"`) ở 5 chỗ nạp
      dữ liệu (chi tiết / sửa / nhân bản / chọn bảng giá / chọn tuyến).
- [x] FE: thêm `<colgroup>` khai bề rộng TỪNG cột (Tuyến 280 · Km 120 · mỗi trọng tải 190 · cột hành động auto);
      bỏ `width` trên `th` colspan.
- [x] Verify Playwright chi tiết BGVC-00088: 11 cột trọng tải đều 190px, Số Km hiện `118`, `80`…;
      `/create`: Tuyến 280 / Km 120 / trọng tải 190, cột hành động hút phần dư như cũ. Quyền test gán tạm local đã gỡ.

## Item 20 — Màn Thêm/Sửa treo khi nhập ~50 tuyến (2026-11-06) — DONE

**Bối cảnh:** QA báo ticket "[ERP => HRM] Chi tiết mẫu báo giá vận chuyển - Xuất excel" có 2 ý:
- (1) `/transport/delivery-quotations/97` bấm "Xuất excel" lỗi → **QA xác nhận lại xuất được, không lỗi nữa**
  (không tái hiện được local: tinker export phiếu 39/59/81 tới 508 tuyến×14 cột đều OK 1.3–2.5s). KHÔNG sửa #1.
- (2) Thêm ~50 tuyến → gõ/bấm trong bảng ma trận bị treo. **Fix bằng ô tĩnh** (user chốt "Đồng ý dùng ô tĩnh").

**Nguyên nhân (2):** mỗi ô giá trang trí trong ma trận là 1 `V2BaseInput disabled placeholder="—"`. Component
V2Base* gắn mixin vee-validate (`v2ValidateMixin`) → mỗi instance đăng ký 1 field validate. 50 tuyến × ~14 cột
≈ 700+ instance vee-validate (cộng dòng "Giá cước vượt trội") → compile + theo dõi validate làm treo khi gõ.
Các ô này THUẦN TRANG TRÍ: không `v-model`, không gửi BE (ma trận rỗng để NCC điền trên file Excel xuất ra).

- [x] FE `DeliveryQuotationForm.vue`: thay ô trang trí `V2BaseInput disabled "—"` ở 2 chỗ bằng markup tĩnh
      `<div class="cell-placeholder">—</div>` + SCSS giả khung ô disabled:
      - hàng "Giá cước vượt trội" (thead)
      - thân ma trận (road × vehicle × payload)
      GIỮ V2Base cho ô thực: Số Km (`v-model`), ô Tuyến (click mở picker), select loại xe / trọng tải.
- [x] Self-check grep V2Base cho `pages/transport/delivery-quotations/` = RỖNG (không có element thô).
- [x] Verify Playwright `/create` với 50 tuyến × 3 loại xe × 5 trọng tải (= 15 cột giá, 765 ô trang trí):
      - DOM: 765 `.cell-placeholder` (div tĩnh), **0 input** trang trí; chỉ còn **101 V2BaseInput thực**
        (50 tuyến × [ô Tuyến + ô Km] + 1 ô header). Trước fix ~866 V2BaseInput → giảm 765 instance vee-validate.
      - Gõ 10 phím vào ô Km: mượt, không treo (avg 187ms/phím ở DEV chưa minify + HMR; prod thấp hơn nhiều).
      - Ảnh `bgvc-50-roads-static-cells.png`: ô "—" xám khớp hệt ô disabled cũ, ô Tuyến/Km vẫn là V2BaseInput.

## Item 21 — Nhóm Vận chuyển với NCC lề trang rộng hơn màn khác (2026-11-07)

Nguyên nhân: 12 file có wrapper `v2-styles min-vh-100 pt-2 > container-fluid` nhưng không import `v2-styles.scss`,
nên `.container-fluid` giữ padding Bootstrap và `pt-2` vẫn còn. Không sửa file dùng chung.

- [x] Thêm `@import '@/assets/scss/v2-styles.scss';` (scoped) vào 12 file: delivery-quotations (index, create, _id/index, _id/edit),
      valid-delivery-prices (index, _id/index), delivery-cost-summaries (index, create, _id/index, _id/edit),
      delivery-contracts (_id/index, components/DeliveryContractList).
- [x] Đo Playwright: x=68, y=70, rộng 1362 khớp màn mẫu `/transport/delivery-trips` trên 10 màn render được.
      Chưa đo được 4 màn do local thiếu quyền API: delivery-cost-summaries create, _id, _id/edit và valid-delivery-prices/_id.
