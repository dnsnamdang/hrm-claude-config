# Plan — Validate đơn giá công tác phí khi gửi duyệt DNTT

Nhánh: `tpe` (client) / `tpe` (api). Fix nhỏ, chỉ FE.

## Yêu cầu
Màn Đề nghị thanh toán (DNTT), tab "Công tác phí": khi bấm **Lưu và gửi duyệt** (status=2),
nếu có nhân viên ở bảng **A: Ngày công tác thực tế** (`business_trip_reals`) chưa có đơn giá công tác phí
(`price_regulation` rỗng/0) → hiển thị toast **"Chưa có đơn giá công tác phí"** và KHÔNG cho gửi duyệt.
Nút **Lưu** (nháp, status=1) vẫn cho lưu bình thường.

Phạm vi (đã chốt với user): chỉ check `business_trip_reals`, mọi NV trong danh sách phải có đơn giá > 0
(không xét số ngày). Bỏ qua tab hỗ trợ (`business_trip_supports`).

## Tasks
- [x] Điều tra: xác định field đơn giá = `price_regulation` (BusinessTravelExpensesTab.vue), nguồn từ AssignConfig
- [x] Chốt phạm vi validate với user
- [x] FE `create.vue`: thêm check trong `submitForm(status)` khi `status == 2`
- [x] FE `_id/edit.vue`: thêm check tương tự trong `submitForm(status)` khi `status == 2`
- [ ] Test tay: NV thiếu đơn giá → chặn + toast; đủ đơn giá → gửi duyệt bình thường; nút Lưu nháp không bị chặn
