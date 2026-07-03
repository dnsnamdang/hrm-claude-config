# Lập HĐ hãng từ báo giá HRM theo 2 cấp — phần HRM (hrm-api)

> Cross-system. **Spec đầy đủ ở repo ERP:** `ERP/.plans/lap-hd-hang-tu-bao-gia-hrm-2-cap/design.md`.
> Phía HRM chỉ là phần phụ — lộ thêm cấu trúc cha-con cho endpoint ERP đang gọi.

## Mục tiêu (HRM)
Để ERP dựng được hàng hoá 2 cấp khi lập HĐ từ báo giá HRM, endpoint tích hợp ERP→HRM phải trả thêm quan hệ cha-con.

## Thay đổi DUY NHẤT
`Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` → `erpContractData()` (~dòng 557–564):
thêm **`parent_id`** và **`product_type`** vào `QuotationProductPrice::where('quotation_id',$id)->...->get([...])` (đã có sẵn `id`, `qty_needed as quantity`, `quotation_group_id`).

## KHÔNG đổi
- DB (cột `parent_id`/`product_type`/`qty_needed` đã có sẵn từ migration `add_direct_quotation_support`).
- Cách tính tổng/giảm giá/VAT (tổng vốn đã loại hàng con — `if parent_id continue`).
- `erpEligible`, `erpMarkContract`.

## Ghi chú
- `child_ratio` KHÔNG tính bên HRM — ERP tự suy ra = `con.qty / cha.qty`.
- Báo giá direct (không BOM) vẫn lộ cha-con bình thường vì `parent_id` nằm trên `quotation_product_prices`.
