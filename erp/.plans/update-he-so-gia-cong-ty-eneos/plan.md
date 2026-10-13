# Update hệ số giá công ty — hàng thương hiệu ENEOS

## Yêu cầu
Set `product_company_coefficients.coefficient` cho toàn bộ hàng ENEOS:
- CN Hải Phòng (company_id=2): **1.02**
- CN Vinh (company_id=3): **1.03**
Phạm vi: **tất cả 422 hàng ENEOS** (brand_id=307), **ghi đè** hàng đã có hệ số khác.

## Đã làm (prod erp_new)
- [x] `UpdateDB::updateEneosCompanyCoefficient()` — upsert: update hàng đã có + insert hàng chưa có.
      Transaction + idempotent. `php -l` sạch.
- [x] Chạy prod: Company 2 → update 132 + insert 290; Company 3 → update 120 + insert 302.
- [x] Verify: 422/422 hàng có coefficient đúng (cty2=1.02, cty3=1.03), 0 hàng sai.

## Ghi chú
- Chỉ cập nhật bảng hệ số `product_company_coefficients`. Nếu giá công ty được vật chất hoá/cache ở
  bảng giá khác (product_prices…) và cần tính lại theo hệ số mới → cần bước recalc riêng (chưa làm).
