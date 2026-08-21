# Fix: Placeholder select V2 base lệch xuống dưới (không căn giữa dọc)

Người phụ trách: @khoipv

## Root cause

1. Block `<style lang="scss">` trong `V2BaseSelect.vue` + `V2BaseSelectInModal.vue` **không có `scoped`** nhưng dùng `::v-deep` → vue-loader không biên dịch `::v-deep` trong block thường → selector ra browser chứa pseudo-element lạ → browser **vứt toàn bộ rule**. Mọi rule căn chỉnh (padding: 0 cho `.select2-selection`, padding/line-height cho `.select2-selection__rendered`) chưa bao giờ có hiệu lực.
2. Style thật sự đang áp: select2 core (`line-height: 28px` trên `__rendered`) + `custom-theme.scss:76` (`padding-top: .2rem !important` trên `.select2-selection--single`), trong khi box bị ép cứng 26/32/34/40px → nội dung 3.2 + 28 = 31.2px > ruột box → chữ dồn xuống đáy. `V2BaseSelectRemote` dùng chung class `.v2-select` nên hưởng fix theo.

## Tasks

- [x] 1. `V2BaseSelect.vue`: bỏ toàn bộ `::v-deep` trong block style không scoped (rule trở thành global hợp lệ, specificity `.v2-select .select2-*` đủ đè theme)
- [x] 2. `V2BaseSelect.vue`: căn giữa dọc single select — `__rendered` dùng `line-height = height − 2px border` theo size (xs 24 / sm 30 / md 32 / lg 38), padding ngang `0 20px 0 10px` (chừa chỗ arrow), arrow nest dưới `--single` để đè `top: 5px` của theme. Sửa kèm: block xs cũ ghi nhầm height 32px → 26px (thống nhất với block global + JS heightMap)
- [x] 3. `V2BaseSelectInModal.vue`: tương tự task 1 + 2 (thêm line-height theo size vào block global cuối file)
- [x] 4. Verify: vue-template-compiler parse + node-sass compile 2 file OK; Playwright đo thật tại `/assign/prospective-projects` (dev server HMR): box 32px, placeholder topGap 8 / bottomGap 9.6 (căn giữa, trước đó dồn đáy); chọn giá trị → text căn giữa, nút clear × vẫn float phải; dropdown mở/chọn bình thường. Ảnh: `after-fix.png`

- [x] 5. Đồng bộ màu placeholder tất cả component V2 base về `#adb5bd` (= `$input-placeholder-color`/`$gray-500` của form-control tìm kiếm nhanh): V2BaseSelect (3 chỗ, gồm cả multiple search field) + V2BaseSelectInModal + V2BaseInput + V2BaseCodeInput + V2BaseCurrencyInput (bỏ opacity 0.6) + V2BaseDatePicker + V2BaseTextarea. Verify: compile 7 file OK + Playwright đo computed color quick-search / select2 / datepicker đều `rgb(173,181,189)`. Ảnh: `placeholder-color-after.png`

- [x] 6. Fix nút "Xóa tất cả" (×) ở **multiple mode** nhảy lên đầu (trước các tag) — phát hiện tại `/assign/customers/43711/edit` ô "Hãng xe". Root cause: select2 4.0.13 prepend `<span class="select2-selection__clear">` vào đầu `<ul.select2-selection__rendered>` rồi đẩy sang phải bằng `float: right`; nhưng task 1 làm "sống lại" rule `.v2-select .select2-selection--multiple .select2-selection__rendered { display: flex !important }` (V2BaseSelect.vue) → **float bị bỏ qua với flex item** → nút × hiển thị theo đúng thứ tự DOM, tức đứng đầu. Fix: ghim tuyệt đối vào mép phải (`position: absolute; right: 6px; top: 50%; translateY(-50%)`) + `padding-right: 28px` cho `__rendered` để tag không đè lên. Prefix `div.v2-select` để đè `padding` shorthand của các rule size `.v2-select--xs/sm/md/lg`. Sửa cả 2 file `V2BaseSelect.vue` + `V2BaseSelectInModal.vue` (Modal không có style multiple riêng, đang ăn ké rule của V2BaseSelect qua class chung `.v2-select`)
- [x] 7. Verify task 6 bằng Playwright trên dev server: `/assign/customers/43711/edit` (V2BaseSelectInModal) — × cách mép phải 6.8px, căn giữa dọc lệch 0px, tag "Honda" nằm bên trái; chèn 6 tag giả cho wrap 2 dòng → không đè lên tag. `/timesheet/timeworking/shift-history` (V2BaseSelect, ô "Nguồn phân ca") — cùng kết quả; bấm × xóa sạch tag và dropdown không bị bung kèm

### Checkpoint — 2026-08-10
Vừa hoàn thành: task 6 + 7 — fix nút "Xóa tất cả" (×) của select2 multiple bị nhảy lên đầu danh sách tag, sửa ở cả `V2BaseSelect.vue` và `V2BaseSelectInModal.vue`, đã verify Playwright 2 màn (form + filter).
Đang làm dở: (không có)
Bước tiếp theo: user kiểm tra thêm các màn khác có select multiple (filter danh sách, form modal) xem vị trí nút × đã đúng mép phải.
Blocked:

### Checkpoint — 2026-08-05
Vừa hoàn thành: 5 task — fix căn giữa dọc placeholder/text cho V2BaseSelect + V2BaseSelectInModal (V2BaseSelectRemote hưởng theo vì dùng chung class `.v2-select`) + đồng bộ màu placeholder mọi component V2 base về #adb5bd, đã verify Playwright.
Đang làm dở: (không có)
Bước tiếp theo: user kiểm tra lại các màn dùng nhiều V2 select (filter panel, form modal) xem có màn nào bị đổi diện mạo ngoài ý muốn do các rule `::v-deep` cũ "sống lại" (border #cbd5e1, focus xanh, tag multiple pill xanh — đều là style vốn được thiết kế nhưng trước đây không có hiệu lực).
Blocked:
