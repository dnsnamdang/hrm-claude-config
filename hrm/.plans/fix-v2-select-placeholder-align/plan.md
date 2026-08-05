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

### Checkpoint — 2026-08-05
Vừa hoàn thành: 5 task — fix căn giữa dọc placeholder/text cho V2BaseSelect + V2BaseSelectInModal (V2BaseSelectRemote hưởng theo vì dùng chung class `.v2-select`) + đồng bộ màu placeholder mọi component V2 base về #adb5bd, đã verify Playwright.
Đang làm dở: (không có)
Bước tiếp theo: user kiểm tra lại các màn dùng nhiều V2 select (filter panel, form modal) xem có màn nào bị đổi diện mạo ngoài ý muốn do các rule `::v-deep` cũ "sống lại" (border #cbd5e1, focus xanh, tag multiple pill xanh — đều là style vốn được thiết kế nhưng trước đây không có hiệu lực).
Blocked:
