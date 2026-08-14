# Plan — Cài đặt bộ lọc (chọn trường hiển thị + kéo thả)

**Phụ trách:** @dnsnamdang · **Nhánh:** `gop_db` (worktree `gop_db-api` + `gop_db-client`)
Design: `.plans/gop-db/filter-customization/design.md` · Spec: `docs/superpowers/specs/gop-db/2026-08-12-filter-customization-design.md`

## Phase 1 — BE: bảng + API

### BE
- [x] Migration `2026_08_12_000000_create_filter_customizations_table` (created_by, table, config json, unique)
- [x] Entity `FilterCustomization` (khai `$table`, cast config => array)
- [x] Service `FilterCustomizationService` (updateOrCreate / getFilterCustomization theo user)
- [x] FormRequest `UpdateFilterCustomizationRequest` (table + config.*.key + config.*.isVisible)
- [x] Controller + 2 route `human/filter-customizations` (POST /, GET /detail), không thêm quyền
- [x] Chạy `php artisan migrate` (bảng `filter_customizations` đã tạo trên DB `local_hrm_erp`)

## Phase 2 — FE: component dùng chung

### FE
- [x] `components/modal/filter-customization-modal.vue` — checkbox + `vuedraggable`, footer Lưu / Khôi phục mặc định / Đóng
- [x] `components/V2BaseSmartFilterPanel.vue` — schema field, render V2Base*, slot `#field-<key>`, nút ⚙️ Cài đặt bộ lọc
- [x] Logic merge DB ↔ schema trong component (giữ vị trí/isVisible, bỏ key chết, append key mới)
- [x] Reset giá trị lọc của field bị ẩn (hỗ trợ `resetKeys` cho field gom nhiều key)
- [x] Chỉ dựng popup sau khi đọc xong cấu hình (`configLoaded`)

## Phase 3 — Áp dụng màn pilot `/assign/customers`

### FE
- [x] Thay `V2BaseFilterPanel` bằng `V2BaseSmartFilterPanel`, khai 15 field trong computed `filterFields`
- [x] 2 field qua slot: khối Công ty/PB/NV (`d-contents`) + `CascadePairSelect` (col 6)
- [x] Dọn import thừa (`V2BaseFilterPanel`, `V2BaseLabel`, `V2BaseSelect`, `V2BaseInput`)
- [x] Đổi class wrapper sang `smart-advanced-filters` để dropdown CascadePairSelect không bị cắt; bỏ rule scoped cũ ở page
- [x] Compile-check template + script 3 file (vue-template-compiler + @babel/parser)
- [x] Sửa lỗi prop `fields` bị `vee-validate` đè → đổi tên `filterFields` / `localFields`
- [x] Đưa nút Tìm kiếm / Làm mới lên cùng hàng ô tìm nhanh (theo demo)
- [x] Popup dạng lưới ngang 4 ô/hàng + `V2BaseCheckbox` + số thứ tự, nhãn dài cắt `…`
- [x] Test Playwright: toggle nâng cao, bỏ tick, kéo thả, Lưu, reload giữ cấu hình, Khôi phục mặc định, merge key mới/key chết, reset giá trị field bị ẩn
- [x] Đồng nhất padding (5px) + margin-bottom (0.5rem) mọi ô lọc — cột của V2BaseCompanyDepartmentFilter nằm trong `d-contents` nên rule gutter/`mb-*` của Bootstrap không với tới
- [x] Popup: `modal-body` padding 0.5rem, rộng 1180px, nhãn xuống dòng (bỏ `…`), ô tick căn giữa
- [x] Thêm ô lọc **Bộ phận** cho màn khách hàng (bỏ `:disable_part`, gửi `part_id` trong `buildApiFilters`)
- [x] Popup: STT / tay kéo / checkbox / chữ căn giữa tuyệt đối (lệch 0.0px cả ô 1 dòng lẫn 2 dòng)
- [x] Bỏ sort toàn bộ cột màn khách hàng (4 cột `sortable`, props `sortBy`/`sortDirection`, `@sort`, hàm `handleSort`); giữ `sort_by=id&sort_desc=true` mặc định gửi API
- [ ] User tự review lại UI trên trình duyệt

### Checkpoint — 2026-08-12
Vừa hoàn thành: code đủ Phase 1–3, tài liệu chuyển về `.plans/gop-db/` + `docs/superpowers/specs/gop-db/`.
Đang làm dở: chưa chạy migration, chưa test trình duyệt.
Bước tiếp theo: chạy `php artisan migrate` ở `worktrees/gop_db-api` → build FE → test trên `/assign/customers`.
Blocked:

### Checkpoint — 2026-08-13 (đợt 2)
Vừa hoàn thành: đồng nhất padding/giãn cách ô lọc; chỉnh popup theo góp ý (to hơn, không cắt chữ, căn giữa, body padding 0.5rem); thêm ô lọc Bộ phận.
Bước tiếp theo: user review UI.
Blocked:

### Checkpoint — 2026-08-13
Vừa hoàn thành: chạy migration; test Playwright toàn bộ luồng trên `/assign/customers` (:3002 + API :8003) — pass hết.
Lỗi đã tìm & sửa: prop tên `fields` bị `vee-validate` 2.x đè (nó gán `computed.fields` cho mọi component) → panel không render trường nào, nút "Tìm kiếm nâng cao" như bị liệt. Đổi thành `filterFields` / `localFields`.
Chỉnh UI theo demo: nút Tìm kiếm/Làm mới lên cùng hàng ô tìm nhanh; popup chuyển thành lưới ngang 4 ô/hàng dùng `V2BaseCheckbox`.
Bước tiếp theo: user review UI; nhân bản component sang các màn khác.
Blocked:

## Phase 4 — Chọn trường khi xuất file (màn `/assign/customers`)

Chốt: áp cho cả 3 nút Excel/CSV/PDF · nguồn trường = đúng 20 cột Excel đang xuất · không lưu lựa chọn · thứ tự cột = thứ tự tick, dùng `V2BaseSelectInModal` multiple.

### BE
- [x] `CustomerExportColumns` — bảng định nghĩa 20 cột (key → nhãn, độ rộng, cách lấy giá trị) + parse/validate param `fields` (bỏ key lạ/trùng, rỗng thì fallback)
- [x] `CustomerExcelExport` nhận danh sách cột động (headings/map/columnWidths/cột cuối tính theo số cột, bỏ hằng `LAST_COLUMN`)
- [x] `CustomerCsvExport` + `CustomerPdfExport` dùng chung bảng định nghĩa; blade PDF lặp `<th>/<td>` động + co cỡ chữ theo số cột
- [x] Controller 3 endpoint truyền `fields` xuống export
- [x] Bẫy: PHP 7.4 không cho `const` trong trait → dùng static method `shortColumnKeys()`

### FE
- [x] `components/modal/export-fields-modal.vue` (V2Base + skill modal-popup, `V2BaseSelectInModal` multiple)
- [x] Màn khách hàng: 3 nút xuất mở popup, gửi `fields` theo thứ tự tick
- [x] Bẫy: select2 multiple KHÔNG giữ thứ tự tick (trả theo thứ tự option gốc) → modal tự theo dõi `orderedKeys` + hiện dải "Thứ tự cột trong file"
- [x] Bẫy: lại dính tên prop `fields` bị vee-validate đè → đổi thành `columns`

### Checkpoint — 2026-08-13 (Phase 4)
Vừa hoàn thành: chọn trường xuất cho cả Excel/CSV/PDF, thứ tự cột theo đúng thứ tự tick. Verify: tick Trạng thái→Tỉnh/TP→Mã KH, file Excel ra đúng header `Trạng thái | Tỉnh/TP | Mã KH`, auto-filter thu về A3:C3.
Bước tiếp theo: user review UI + thử xuất thật.
Blocked:

## Phase 5 — Quy tắc cột sort trên màn danh sách

**Quy tắc chung (áp cho mọi màn danh sách):** cột được bật `sortable` khi thuộc 1 trong 3 nhóm
1. Cột **Mã - Tên** (cột nhận diện chính) — BE sắp theo mã.
2. Cột định dạng **tiền**.
3. Cột định dạng **ngày**.
Các cột còn lại (text mô tả, badge trạng thái, STT, Hành động…) KHÔNG cho sort.

Điều kiện kỹ thuật: key cột phải nằm trong whitelist `SORTABLE_COLUMNS` của service BE, nếu không BE tự quay về `id` và user bấm sort mà bảng không đổi.

### FE
- [x] `/assign/customers`: bật sort cho **Mã - Tên** (`customerInfo`) và **Ngày tạo** (`createdAt`); màn này không có cột tiền
- [x] Nối lại `:sortBy` / `:sortDirection` / `@sort` + `handleSort` (đã gỡ ở Phase trước khi bỏ sort toàn bộ)
- [x] Verify: bấm sort Mã - Tên → `sort_by=customerInfo`, dữ liệu xếp tăng dần theo mã; bấm Ngày tạo → `sort_by=createdAt`, dòng cũ nhất (25/05/2020) lên đầu

## Phase 6 — Quy tắc ô tìm kiếm nhanh

**Quy tắc chung (mọi màn danh sách):** ô tìm kiếm nhanh chỉ tìm theo **Mã**, **Tên** và **Người tạo**. Các tiêu chí khác (tên viết tắt, địa chỉ…) để trong Tìm kiếm nâng cao.

**Ngoại lệ màn khách hàng:** thêm **MST** và **SĐT** vào tìm nhanh (2 tiêu chí hay tra nhất ở màn này). Màn khác muốn thêm tiêu chí ngoài quy tắc chung thì cũng ghi rõ ngoại lệ như vậy.

### BE
- [x] `CustomerService`: `keyword` tìm `customers.code` + `customers.fullname` + `tax_code` + `mobile` + tên người tạo
- [x] Người tạo dùng `EXISTS` (không join) để không làm phình câu COUNT của phân trang — cùng lý do với `creatorNameSql()`
- [x] Bỏ `short_name` khỏi tìm nhanh (thu hẹp so với trước, đúng quy tắc)

### FE
- [x] Đổi placeholder ô tìm nhanh thành "Tìm theo mã KH, tên KH, MST, SĐT, người tạo..."

Verify đủ 5 tiêu chí: `19TPHPVI-262` → 1 KH (mã) · `ETEK` → 5 KH (tên) · `0108596557` → 2 KH (MST) · `0948365335` → 1 KH (SĐT) · `Nguyễn Tài Trung` → 47 KH (người tạo).

## Phase 7 — 2 lỗi "bấm nút không phản hồi" trên `/assign/customers`

1. **Nút "Cài đặt bộ lọc" chết khi API cấu hình chưa về.** Modal bị gate `v-if="configLoaded"` nên `$bvModal.show()` gọi vào modal chưa tồn tại — không lỗi, không phản hồi. Dev server `php -S` chạy đơn luồng nên request này hay xếp hàng sau query danh sách 17k dòng, cửa sổ lỗi khá dài.
   - [x] Bỏ gate `v-if`, luôn dựng sẵn modal; popup watch `fieldsProps` và chỉ đồng bộ khi ĐANG ĐÓNG (tránh xoá thao tác dở dang).
2. **Nút "Tìm kiếm nâng cao" kẹt `height: 0`.** Hook transition JS (`beforeEnter/enter/leave`) dùng `setTimeout(300ms)` cố định, không huỷ khi hiệu ứng bị ngắt. Bấm 2 lần liên tiếp → timeout lượt trước chạy muộn, ghi đè trạng thái, để lại inline `height: 0px; overflow: hidden` trong khi `display: block` và nhãn nút là "Ẩn tìm kiếm nâng cao" → mở mà không thấy gì.
   - [x] Bỏ hẳn hook JS chỉnh height, thay bằng transition CSS thuần (opacity + translateY) — không đụng height nên không thể kẹt.
   - Lưu ý: `V2BaseFilterPanel` cũ cũng còn nguyên lỗi này (code gốc mình copy sang), chưa sửa vì đang phục vụ nhiều màn.

Verify: bấm nhanh 3 lần × 6 vòng — trạng thái cuối luôn khớp nhãn nút (mở = 327px, đóng = 0px), không vòng nào kẹt.

## Phase 8 — Vào màn `/assign/customers` gọi API danh sách 2 lần

**Nguyên nhân: lệch KIỂU DỮ LIỆU.** API trả `meta.per_page` là **chuỗi** `"10"`, page gán thẳng vào `pagination.pageSize` vốn đang là **số** `10`. Computed `pageSizeValue` của `V2BaseDataTable` đọc giá trị này, thấy `10 -> "10"` là "đổi" nên watcher emit `page-size-change`, page chạy `handlePageSizeChange` → `loadData()` lần 2. Lần 2 xong giá trị đã là `"10"` nên không lặp tiếp — đúng 2 request, rất dễ tưởng là "code gọi 2 lần".

- [x] Ép `Number()` cho toàn bộ `meta` khi gán `pagination` (`current_page`, `per_page`, `total`, `last_page`, `from`, `to`)
- [x] Verify: vào màn chỉ còn **1 request**

**Đã thử và ĐÃ GỠ:** guard "pageSize trùng thì bỏ qua" trong `handlePageSizeChange` — `V2BaseDataTable` bind `v-model` vào computed có setter **ghi thẳng `pagination.pageSize` TRƯỚC khi emit**, nên lúc handler chạy 2 giá trị đã bằng nhau; guard khoá luôn chức năng đổi số dòng/trang (chọn 20 mà bảng vẫn 10 dòng, không có request nào).

### Sửa gốc ở `V2BaseDataTable` (component dùng chung — user đã đồng ý)

Ô "Số dòng/trang" có **HAI nguồn phát cùng một sự kiện**:
1. `v-model="pageSizeValue"` → setter ghi `pagination.pageSize` → watcher `pageSizeValue` emit `page-size-change`
2. `@change="handlePageSizeChange"` → emit `page-size-change` lần nữa

→ mỗi thao tác đổi số dòng/trang bắn 2 request. Watcher còn tệ hơn ở chỗ nó bám prop `pagination`, nên **mọi** thay đổi từ bên ngoài cũng emit — kể cả chỉ đổi kiểu dữ liệu (`10` → `"10"`), chính là nguồn request thừa lúc vào màn.

- [x] Bỏ watcher `pageSizeValue`, giữ `@change` (chỉ chạy khi user thao tác thật)
- [x] GIỮ watcher `currentPageValue`: `b-pagination` chỉ có `v-model`, không có handler nào khác để phát `page-change`

Verify sau khi sửa: vào màn **1** request · đổi số dòng/trang **1** request (bảng đúng 20 dòng) · chuyển sang trang 2 **1** request (`page=2&per_page=20`, đúng 20 dòng).
