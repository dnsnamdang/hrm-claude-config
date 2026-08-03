# Cho phép chọn Loại tiền tệ khi lập báo giá — Design

> Phụ trách: @dnsnamdang · Branch: `tpe-develop-assign`
> Màn: Quản lý dự án TKT → Quản lý báo giá (Tạo mới + Cập nhật).

## Mục tiêu
- Trường "Loại tiền tệ*" **tự kế thừa** từ dự án TKT khi tạo báo giá (đã có qua `selectProject`).
- **Cho phép chọn lại** loại tiền tệ khác từ dropdown — **CHỈ ở lần lập MỚI** (form Sửa KHÓA, không cho đổi — theo note bổ sung của user).
- Lưu đúng loại tiền tệ người dùng chọn.

## Hiện trạng
- Select tiền tệ đang hard `:disabled="true"` → không đổi được (dù đã có sẵn `handleChangeCurrency` với confirm "giá đã nhập sẽ không đổi").
- `selectProject` đã set `form.currency_id = p.currency_id` (kế thừa dự án).
- `isCreateMode = $route.params.id === 'new'` (tạo mới true, sửa false).

## Quyết định
| Vấn đề | Quyết định |
|---|---|
| Cho đổi khi nào | CHỈ khi tạo mới: `:disabled="!isCreateMode"` (form Sửa khoá) |
| Kế thừa dự án | Giữ nguyên `selectProject` (đã set currency theo dự án) |
| Đổi tiền tệ | Wire `@change="handleChangeCurrency"` (đã có confirm giá không đổi) |
| Làm tròn | Đồng bộ với feature VNĐ: đổi tiền tệ → `roundingMode = isVndCurrency ? '0' : null` |
| Lưu | `form.currency_id` đã nằm trong payload create/update (BE lưu sẵn) |

## Phạm vi
- FE-only: `pages/assign/quotations/_id/edit.vue` (create.vue extends). Không BE/migration.

## Acceptance
- Mở form Tạo báo giá cho dự án USD → field hiển thị USD tự động.
- Click field → chọn lại VND/EUR... từ dropdown được (chỉ tạo mới).
- Form Sửa → field khoá, không đổi.
- Lưu → currency đúng lựa chọn, hiển thị đúng khi mở lại.
