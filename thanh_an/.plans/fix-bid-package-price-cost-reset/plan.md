# Fix: Giá vốn bị mất khi đổi giá min/max ở màn thêm gói thầu (@khoipv)

## Bối cảnh
- Màn: `bid_package/bid_package/add` — tạo gói thầu từ báo giá (vd BG-326)
- Triệu chứng: chọn báo giá → giá vốn hiển thị đúng; đổi dropdown "Giá bán min"/"Giá bán max" → giá vốn mất.

## Root cause
- `GeneralComponent.vue > updatePrice(skipPriceCost = false)`: khi `skipPriceCost = false` sẽ tính lại `price_cost`
  từ danh mục `pro.prices` theo `is_price_capital == 1`.
- Hàng tạo từ báo giá có giá vốn **nhập tay**, danh mục không có dòng `is_price_capital` tương ứng → `price_cost = ''`.
- `addQuotation` gọi `updatePrice(true)` (giữ giá vốn), nhưng dropdown min/max gọi `@input="updatePrice()"` (không skip) → ghi đè rỗng.
- Luồng dự án (`addProject`) khởi tạo `price_cost = 0` và phụ thuộc `updatePrice()` để nạp giá vốn từ danh mục → không được phá.

## Tasks
- [x] Trace luồng dữ liệu giá vốn (BE `DetailQuotationResource`/`DetailProductResource` + FE)
- [x] Xác định điểm phân biệt 2 luồng: `formSubmit.quotation_id`
- [x] Fix: chỉ tính lại `price_cost` khi `!skipPriceCost && !this.formSubmit.quotation_id`
- [ ] Test tay: tạo gói thầu từ BG-326, đổi min/max → giá vốn còn nguyên
- [ ] Test tay: tạo gói thầu từ dự án, đổi min/max → giá vốn nạp từ danh mục bình thường

## Ghi chú / theo dõi thêm
- `ProductComponent.vue > updatePrice(gIndex, pIndex, skipPriceCost)` cũng tính lại `price_cost` khi đổi đơn vị/thêm hàng.
  Khi đổi đơn vị của hàng từ báo giá, giá vốn có thể bị tính lại từ danh mục — chưa nằm trong phạm vi bug này, cần xác nhận với user nếu phát sinh.

### Checkpoint — 2026-06-22
Vừa hoàn thành: Fix `updatePrice` trong `GeneralComponent.vue` (thêm điều kiện `!this.formSubmit.quotation_id`)
Đang làm dở: chờ user test tay 2 kịch bản
Bước tiếp theo: user kiểm thử trên BG-326
Blocked:
