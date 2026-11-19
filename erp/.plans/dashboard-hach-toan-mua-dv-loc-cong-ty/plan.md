# Dashboard Phê duyệt — "YC hạch toán mua dịch vụ cần duyệt" thấy phiếu công ty khác

@junfoke · Repo `TanPhatDev`, nhánh `gop_db` · 12/10/2026

## Hiện tượng
Nguyễn Hải Yến (emp 1189, ETEK GREEN company_id 9 trên prod) thấy ô "Yêu cầu hạch toán mua dịch vụ cần duyệt (1)".
Prod: phiếu chờ duyệt duy nhất id 65 thuộc company 1 (TPE).

## Nguyên nhân
- `HomeController::approveList` đếm BuyServiceAccountingRequest CHO_DUYET không lọc công ty.
- `BuyServiceAccountingRequest::searchByFilter` type=for-approve cũng không lọc công ty.
- Trong khi `canView()` chỉ cho xem phiếu CHO_DUYET cùng công ty → thấy trong DS nhưng không mở được.

"Hàng tạm cần duyệt" / "Hàng không được duyệt giá bán" = danh mục hàng dùng chung tập đoàn (tmp_products không có company_id) → đúng thiết kế, không sửa.

## Task
- [x] Lọc `company_id = info->company_id` ở count dashboard + tab Chờ duyệt
- [x] php -l sạch
- [ ] Commit + deploy prod, nhờ chị Yến kiểm lại (ô phải biến mất)
