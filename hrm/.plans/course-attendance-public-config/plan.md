# Plan — Cấu hình màn điểm danh public

## Phase 1: Logo động + bỏ bắt buộc email

### FE (`pages/client/course-attendance/index.vue`)
- [x] Đổi `data.logo` mặc định `''`, bỏ import + biến `logoEtek` hardcode
- [x] Template: `<img v-if="logo" :src="logo" ...>` (fallback để trống)
- [x] Thêm `getLogo()`: dispatch `apiGetMethod('master-settings')`, tìm `category=='logo'` → set `this.logo = content` (try/catch)
- [x] Field email: đổi `v-validate="'required|email'"` → `v-validate="'email'"`, bỏ `<Required />` cạnh label Email

### BE (`StoreStudentAttendanceRequest.php`)
- [x] Rule `email`: bỏ `required` → `nullable|max:255|email|unique(...)`
- [x] Thêm `prepareForValidation()`: convert email `''` → `null`

### Kiểm thử (đã verify qua Playwright)
- [x] Màn public hiển thị logo theo setting-master (S3 URL); setting rỗng → không hiện logo (v-if)
- [x] Submit không nhập email → thành công (redirect /success, DB email=null)
- [x] Email không còn dấu `*`, các field name/phone/company giữ required

## Phase 2: Responsive logo mobile (quét QR bằng điện thoại)
- [x] Logo hardcode `height:80px` bị tràn ngang trên mobile → đổi sang class `.logo-img` với `max-width:100%; height:auto; max-height:80px` (mobile `max-height:60px`)
- [x] Thêm padding `12px` cho `.card-body` trên mobile cho thoáng
- [x] Verify: 390px & 320px không overflow ngang; desktop logo 80px căn giữa

### Checkpoint — 2026-07-09
Vừa hoàn thành: Logo động theo setting-master + bỏ bắt buộc email (FE + BE), verify end-to-end qua Playwright, dọn dữ liệu test.
Đang làm dở: (không)
Bước tiếp theo: (không) — feature hoàn tất, chờ user review.
Blocked:
