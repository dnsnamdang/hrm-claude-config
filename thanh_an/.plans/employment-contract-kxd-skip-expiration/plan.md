# Bỏ validate Ngày hết hạn khi loại HĐ là "không xác định" (_kxđ)

Phụ trách: @khoipv

## Bối cảnh
Màn `human/employment-contract/add` (và edit — dùng chung component). Khi loại hợp đồng
là loại "không xác định" (hậu tố `_kxđ` trong tên master `labor_contracts`) thì
trường **Ngày hết hạn** không còn bắt buộc.

## Task
- [x] FE: `EmploymentContract.vue` — thêm computed `isIndefiniteContract` khớp tên loại HĐ chứa `kxđ` / `không xác định`
- [x] FE: bỏ `required` trên `expiration_date` và ẩn `<Required />` khi là loại KXĐ
- [x] FE: watcher xoá lỗi `expiration_date` khi đổi sang loại KXĐ
- [x] BE: `StoreEmployeeContractRequest` — `expiration_date` dùng `Rule::requiredIf` (không bắt buộc khi KXĐ). Dùng `mb_strpos` (PHP 7.4 không có `str_contains`)
- [x] BE: `EmploymentContractController@print` — guard khi `expiration_date` null (DEN_NGAY & SO_THANG để trống, không gọi Carbon::createFromFormat trên chuỗi rỗng)

## Ghi chú
- Loại KXĐ nhận diện theo TÊN master (dữ liệu động, không hardcode id). DB stag id=7 = "Hợp đồng lao động_kxđ".
- Cả `store` và `update` dùng chung request → add + edit đều áp dụng.

### Checkpoint — 2026-07-22
Vừa hoàn thành: FE + BE bỏ validate Ngày hết hạn cho loại KXĐ
Đang làm dở: (không)
Bước tiếp theo: user kiểm thử trên UI
Blocked:
