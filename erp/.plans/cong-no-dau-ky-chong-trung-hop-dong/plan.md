# Plan — Chống trùng hợp đồng khi khai công nợ đầu kỳ (theo công ty)

## Mục tiêu
1 hợp đồng chỉ được khai báo công nợ đầu kỳ đúng 1 lần trong cùng 1 công ty.
Khóa trùng mới = `(company_id, deptable_type, deptable_id)` (bỏ `account_id` khỏi điều kiện trùng).
Áp dụng cho 2 màn: Công nợ đầu kỳ Khách hàng + Nhà cung cấp.

## Tasks
- [x] Màn KH — `DeclareDebtBeginningController::store()`: thay check trùng account-level bằng check contract-per-company + chống trùng trong cùng submit
- [x] Màn KH — `DeclareDebtBeginningController::update()`: đổi check trùng sang contract-per-company (loại trừ chính bản ghi)
- [x] Màn NCC — `DeclareDebtSupplierBeginningController::store()`: load `deptable` để lấy company_id, thay check trùng + chống trùng trong cùng submit
- [x] Màn NCC — `DeclareDebtSupplierBeginningController::update()`: thêm mới check trùng contract-per-company (loại trừ chính bản ghi)
- [x] FE: thêm span hiển thị lỗi `contract_id` ở cột "Số hợp đồng" của 2 màn (index.blade.php) — vì trước đó chỉ hiện lỗi account_id
- [x] Kiểm tra lint/syntax PHP (cả 2 controller: No syntax errors)

## Tasks bổ sung — Sửa nhãn chú thích mã loại HĐ trong modal Import Excel (2026-10-14)
- [x] `accounting/declare-debt-beginning/index.blade.php` (175-177): sửa 3 nhãn SAI theo đúng 3 luồng mua
  - HDMNN `BuyContract2` (orders/buy_contract2?type=all, nhóm "Mua hàng nhập khẩu"): "HĐ mua nước ngoài" → **"HĐ mua nhập khẩu"**
  - HDMN `InlandBuyContract` (orders/inland_buy_contracts = "mua hàng ngoài"): "HĐ mua trong nước" → **"HĐ mua ngoài"**
  - HDMTN `InlandBuyContractNew` (inland_buy_contract_new type=firm "theo hãng" + type=free "tự do"): "HĐ mua trong nước mới" → **"HĐ mua trong nước (theo hãng / tự do)"**
- [x] Xác nhận "HĐ hãng (dự án)" (HDHNTDA) là HĐ BÁN `FirmContract`, khác luồng mua; "hợp đồng hãng" bên MUA đã gộp trong HDMTN (cùng bảng, mã duy nhất theo id → không cần mã riêng)
- [x] Màn NCC `declare-debt-supplier-beginning` không có khối chú thích này → không sửa
- [x] Không đụng code validate/import — chỉ là text hiển thị

## Tasks bổ sung — Thêm chú thích mã loại HĐ vào modal Import Excel màn NCC (2026-10-15)
- [x] `accounting/declare-debt-suppilier-beginning/index.blade.php` (dưới ô "Chọn file", sau `<input type=file>`): thêm khối `<small class="form-text text-muted mt-1">` liệt kê 4 mã loại HĐ mà import NCC chấp nhận (khuôn copy từ màn KH dòng 169-178)
  - HDMNN – HĐ mua nhập khẩu (`BuyContract2`)
  - HDMN – HĐ mua ngoài (`InlandBuyContract`)
  - HDMTN – HĐ mua trong nước (theo hãng / tự do) (`InlandBuyContractNew`)
  - HDMDK – HĐ mua đầu kỳ (`BuyDebtContractBeginning`)
- [x] Câu intro ghi rõ cột Loại Hợp đồng **BẮT BUỘC** (parser `DeclareDebtSupplierBeginningImport.php:50` để trống → lỗi), KHÁC màn KH ("để trống tự nhận")
- [x] Chỉ sửa text hiển thị trong blade — KHÔNG đụng BE/import/validate; `php -l` No syntax errors
- [ ] Verify bằng Playwright trên màn NCC: CHƯA chạy — ERP local (:8001) + prod đều sau login session, không có credential ERP để tự đăng nhập. Markup copy verbatim từ màn KH đang chạy → rủi ro render ~0. Chờ user tự mở popup Import Excel xác nhận.

## Ghi chú
- `company_id` lấy giống hook `created()`: `$deptable->employee_create->info->company_id`
- Thông báo lỗi gắn vào field `items.$key.contract_id`: "Hợp đồng này đã được khai báo công nợ đầu kỳ trong công ty"
- KHÔNG đụng import Excel, FE/Blade, KHÔNG backfill dữ liệu trùng cũ
- DB hiện trỏ `hrm_erp_gop` remote → không tinker ghi dữ liệu
