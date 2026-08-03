# Fix: main_company_id = 0 lọt qua validate `required` (gói thầu)

Phụ trách: @khoipv

## Bối cảnh
- Bản ghi bid_package (vd id 352) có `main_company_id = 0`, `joint_bid = NULL`.
- Khi sửa, form nạp `main_company_id = 0`; rule `required` của Laravel coi `0` là có giá trị → lọt validate dù thực chất chưa chọn công ty thực hiện.
- Rule nghiệp vụ đúng: KHÔNG liên doanh (joint_bid != 1) → bắt buộc chọn công ty thực hiện.

## Task
- [x] BE1: Sửa rule `main_company_id` trong `StoreBidPackageRequest` → `required|integer|gt:0` (nhánh không liên doanh)
- [x] BE2: Thêm `prepareForValidation()` chuẩn hoá `main_company_id` rỗng/`0` → `null`
- [x] BE3: Thêm message tiếng Việt cho `main_company_id` (required/gt/integer)
- [x] DATA: UPDATE bản ghi `main_company_id = 0` → `NULL` (đã dọn 4 bản: 291, 299, 347, 350; 352 đã tự chọn công ty = 3)
- [x] Kiểm tra: `php -l` pass, DB không còn bản ghi = 0

### Checkpoint — 2026-07-03
Vừa hoàn thành: sửa xong BE (rule + prepareForValidation + message) và dọn data
Đang làm dở: (không)
Bước tiếp theo: user test lại trên UI — mở gói thầu không liên doanh, để trống công ty thực hiện → phải báo lỗi "Vui lòng chọn công ty thực hiện"
Blocked:
