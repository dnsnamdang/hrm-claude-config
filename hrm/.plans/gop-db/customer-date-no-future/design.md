# customer-date-no-future — Chặn chọn ngày tương lai ở màn khách hàng

**Người phụ trách:** @khoipv
**Nhánh:** `gop_db` (cả `hrm-api` + `hrm-client`)
**Ngày:** 2026-08-13

## Mục tiêu

Các ô nhập ngày mang ý nghĩa "đã xảy ra trong quá khứ" ở màn khách hàng `/assign/customers`
không được phép chọn / nhập ngày lớn hơn ngày hiện tại.

## Phạm vi (user chốt)

3 ô nhập, đều nằm trong component dùng chung `components/assign-components/customer/CustomerForm.vue`
→ sửa 1 chỗ thì cả 5 màn cùng có hiệu lực (thêm · sửa · xem chi tiết readonly · quản lý KH · modal thêm nhanh):

| Ô nhập | Field | Vị trí |
| --- | --- | --- |
| Ngày cấp (CCCD/CMND) | `grant_date` | `CustomerForm.vue:368` |
| Sinh nhật (khách hàng) | `date_of_birth` | `CustomerForm.vue:464` |
| Sinh nhật (người liên hệ) | `contacts[].date_of_birth` | `CustomerForm.vue:1200` |

Ngoài phạm vi (user chốt): các ô ngày ở màn khác (hồ sơ nhân sự, hợp đồng…) — không rà đợt này.

## Quyết định

1. **Chặn 2 lớp (FE + BE)**, không chỉ FE. Lý do: `V2BaseDatePicker` để `editable` mặc định `true`
   nên user vẫn gõ tay được vào ô, xám lịch thôi là chưa chặn hết.
2. **Không sửa component dùng chung** `V2BaseDatePicker.vue` — nó đã có sẵn prop `disabledDate`
   (kiểu `Function`, mặc định `() => false`) và truyền thẳng xuống `disabled-date` của
   `vue2-datepicker`. Chỉ cần truyền prop từ `CustomerForm.vue`.
3. **Ngày hôm nay vẫn hợp lệ** — chỉ chặn từ ngày mai trở đi (`before_or_equal:today`).
4. **Không đụng dữ liệu cũ.** KH đang có ngày tương lai trong DB vẫn hiển thị bình thường;
   lần sửa tiếp theo BE sẽ chặn cho tới khi user sửa lại ngày đó. Không viết script data-fix.
5. Không migration, không permission mới, không đụng import Excel
   (file mẫu import KH 25 cột không có 2 trường ngày này).

## Thay đổi

**FE — `hrm-client/components/assign-components/customer/CustomerForm.vue`**
- Thêm method `disableFutureDate(date)`: trả `true` khi `date` > 00:00 hôm nay.
- Truyền `:disabled-date="disableFutureDate"` vào 3 `V2BaseDatePicker` nêu trên.

**BE — `hrm-api/Modules/Assign/Http/Requests/Customer/`**
- `SaveCustomerRequest.php` + `UpdateCustomerRequest.php`: thêm `before_or_equal:today` cho
  `grant_date`, `date_of_birth`, `contacts.*.date_of_birth`; thêm message tiếng Việt tương ứng.

## Spec chi tiết

`docs/superpowers/specs/gop-db/2026-08-13-customer-date-no-future-design.md`

## Rủi ro / lưu ý

- Ô ngày ở chế độ `readonly` (màn xem chi tiết) vốn đã `:disabled` nên prop mới không ảnh hưởng.
- `before_or_equal:today` của Laravel so theo timezone app (`config/app.php`), không phải timezone trình duyệt.
