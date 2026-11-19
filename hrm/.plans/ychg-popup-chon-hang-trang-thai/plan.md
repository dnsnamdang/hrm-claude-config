# YCHG popup "Chọn hàng hoá" — thêm cột Trạng thái HH công ty quản lý + Trạng thái (09/11/2026)

Yêu cầu: popup Chọn hàng hoá (YCHG `/sale/price-asking-requests/add`, `V2ProductPickerModal scope="price_asking"`)
hiện thêm 2 cột ở bảng, bộ lọc, cấu hình cột — giống màn Kho dữ liệu hàng hoá.

- Trạng thái = `product_company_coefficients.status` tại công ty chứng từ.
- Trạng thái HH công ty quản lý = status tại `products.company_id` (giống `owner_status` màn Kho dữ liệu).
- Chữ + màu lấy `ProductCompany::STATUS_TEXT/STATUS_COLOR` (BE quyết).
- Popup dùng chung ~25 màn ⇒ FE chỉ bật cho `scope === 'price_asking'`; BE là cột/tham số tuỳ chọn.

## Tasks
- [x] BE `ProductPickerService`: cột tuỳ chọn `company_status`, `owner_status` (+ `_text`, `_color`)
- [x] BE: tham số lọc `company_status`, `owner_status` (ProductPickerRequest PARAMS + rules)
- [x] BE: feature test
- [x] FE `ProductPickerPanel`: 2 cột (mặc định hiện), badge, cấu hình cột — chỉ price_asking
- [x] FE `ProductPickerAdvancedFilters`: 2 select lọc — chỉ price_asking
- [x] Verify Playwright local

## Checkpoint 09/11/2026
- Xong 6 task. phpunit: test mới 2/9 + 4 file hồi quy picker đều OK.
- Playwright local: 2 cột hiện badge, lọc "Trạng thái = Hàng tạm" ra 3 dòng, cấu hình cột có đủ 2 cột.
- API ở worktree nhánh fix/ychg-picker-trang-thai; client chưa commit trên develop. Chưa commit/push.
- Đã push develop: api 2c69cfb88, client 559b6997b (09/11). Chưa gop_db.
