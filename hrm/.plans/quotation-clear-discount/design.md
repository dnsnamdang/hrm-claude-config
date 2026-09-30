# Design — Xóa dữ liệu giảm giá hàng loạt ở Báo giá (Redmine #10900)

> Người phụ trách: @junfoke — Nhánh: `task_10900` (tách từ `tpe`), CHỈ repo `hrm-client`.

## Mục tiêu

Bổ sung 1 nút trên thanh công cụ phía trên bảng "Chi tiết sản phẩm" ở màn Tạo mới / Cập nhật Báo giá,
cho phép xóa toàn bộ dữ liệu giảm giá đang nhập chỉ bằng 1 thao tác thay vì sửa tay từng dòng.

## Phạm vi

- CHỈ Frontend. Không đụng BE, không migration: các giá trị giảm giá vốn chỉ được ghi xuống DB khi
  user bấm Lưu, payload đã có sẵn đủ trường.
- 1 file: `pages/assign/quotations/_id/edit.vue` (màn Tạo mới `create.vue` `extends` file này nên
  không phải sửa riêng).

## Hành vi đã chốt

| Phương thức GG | Tên nút | Việc thực hiện |
| --- | --- | --- |
| GG mặt hàng (`discountMethod = 1`) | **Xóa giảm giá** | `discount_percent`, `discount_amount` của mọi dòng hàng hóa + dịch vụ về 0 |
| GG tổng (`discountMethod = 2`) | **Xóa phân bổ** | `allocated_discount_amount` của mọi dòng + phân bổ dòng Chi phí vận chuyển về 0 |

- Popup xác nhận theo đúng câu chữ spec, dùng `this.$confirm({ danger: true })` (render
  `components/modal/base-confirm-modal.vue` — khuôn xác nhận dùng chung).
- Mọi giá trị liên quan (Đơn giá sau GG, Thành tiền bán, VAT, Tổng giá trị báo giá, Tỷ suất lợi
  nhuận) là **computed**, tự tính lại — không phải gọi hàm tính tay.

## Quyết định (user chốt 2026-09-11)

1. **Nút hiện nhưng disable khi toàn bộ GG = 0** — theo đúng spec khách, chấp nhận lệch quy ước
   nội bộ "nút không dùng được thì ẩn hẳn" trong trường hợp này. (Riêng khi **không có quyền**
   "Cho phép thêm giảm giá trong báo giá" thì vẫn **ẩn hẳn** như toàn hệ thống — quyền và điều kiện
   nghiệp vụ là 2 chuyện khác nhau.)
2. **"Xóa phân bổ" chỉ đưa cột Phân bổ GG về 0, GIỮ NGUYÊN bảng khoản GG tổng.** Sau thao tác, báo
   giá hiện dòng cảnh báo lệch "Đã phân bổ 0 / Tổng GG X" và nút "Phân bổ tự động" quay lại — đúng
   ý spec là chỉ xóa phân bổ.
3. Phân bổ GG của dòng **Chi phí vận chuyển** (`shippingAllocatedDiscount`) cũng về 0 — spec không
   nhắc nhưng để sót thì "xóa phân bổ" vẫn còn số dư, dòng cảnh báo lệch sẽ sai.

## Lỗi có sẵn sửa kèm

`clearAllDiscountData()` (chạy khi user **đổi phương thức giảm giá**) đang bỏ sót
`shippingAllocatedDiscount` → đổi từ GG tổng sang phương thức khác vẫn còn phân bổ của dòng vận
chuyển, làm lệch tổng tiền. Sửa luôn trong lần này vì cùng một chỗ.

## Không làm

- Không đụng logic phân bổ tự động (`applyAutoAllocation`, `handleAllocateDiscount`).
- Không xóa các khoản GG tổng user đã nhập (xem quyết định 2).
- Không thêm API/endpoint mới.
