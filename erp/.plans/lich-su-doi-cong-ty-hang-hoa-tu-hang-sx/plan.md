# Plan — Ghi lịch sử company cho hàng hoá khi đổi công ty Hãng SX

## Tasks
- [x] Sửa vòng lặp cascade trong `ManufacturesController@update`:
      chỉ ghi history khi `old != new`, tạo `ProductVersion` + `createHistoryRecord('company_id', old, new)`.
- [x] Đảm bảo import đủ (`ProductVersion`, `Carbon`) trong controller.
- [x] Kiểm tra lại: hàng không đổi company không sinh version rỗng (nhánh else save trần).
- [ ] Test qua thao tác thật (user thực hiện trên môi trường).

## Checkpoint — 2026-10-14
Vừa hoàn thành: code xong logic ghi lịch sử company khi cascade đổi công ty Hãng SX.
Đang làm dở: không.
Bước tiếp theo: user test thao tác thật, kiểm tra `product_histories` sinh đúng số dòng.
Blocked: không.
