# Testcase — Tab bốc xếp: chi phí vận chuyển theo thời gian (task_10308)

## Phạm vi
Phiếu xuất kho (warehouse_exports) + Phiếu xuất hàng (product_exports) — Tab BỐC XẾP: bổ sung tính chi phí THEO THỜI GIAN (số giờ × đơn giá/giờ) bên cạnh theo TRỌNG LƯỢNG (tấn × đơn giá/tấn). Gồm cả cấu hình Định mức bốc xếp (ArrangeGood).

## Nguồn tham chiếu (nhánh task_10308, commit `4843dde4e8 task boc xep`)
- Controller: `app/Http/Controllers/Warehouse/ArrangeGoodController.php`
- Request: `app/Http/Requests/Common/ArrangeDeliveryRequest.php` (is_weight/is_time required, price required_if is_weight, price_hour required_if is_time, ≥1 loại)
- Model: `app/Model/Warehouse/ArrangeGood.php`
- Migration: `2026_05_15_000001_add_hourly_price_to_arrange_goods` (is_weight, is_time, company_price_hour, price_hour); `..._000002_add_is_weight_to_arrange_deliveries`
- JS class: `partials/classes/warehouse/WarehouseExportArrangeDelivery.blade.php` (total_money = price × số lượng; is_weight/is_time loại trừ)
- Views: product_exports (create/form/show), warehouse_exports, delivery_arrange/modalPopup

## Logic chính
- is_weight (Tấn): price/company_price; is_time (Giờ): price_hour/company_price_hour. 2 loại loại trừ, ≥1.
- total_money = đơn giá áp dụng × số lượng (tấn hoặc giờ). vat_price = total × vat/100. after = total + vat.

## Output
- `generate-testcase.py` + `testcase.xlsx` — **30 TC**, P0 47%, 5 section, đủ 9 mục mô tả.

## 5 section
- I. Hiển thị tab bốc xếp (xuất kho + xuất hàng, nhãn Tấn/Giờ) — 4 TC
- V. Tính chi phí (Tấn × giá; Giờ × giá_giờ; toggle; định mức set giá; VAT; nhiều dòng; lưu/mở lại) — 9 TC
- VI. Edge & validation (≥1 loại; required_if price/price_hour; company_price...) — 7 TC
- VII. Định mức bốc xếp ArrangeGood (cấu hình is_weight/is_time + price/price_hour; hiển thị 'tấn/giờ') — 5 TC
- VIII. E2E & cô lập (tổng phiếu/công nợ; đổi giờ realtime; xuất kho≡xuất hàng) — 5 TC

## Tasks
- [x] Khảo sát task_10308: ArrangeGood/ArrangeDelivery + is_time/price_hour + validation + JS cost
- [x] Generator + testcase.xlsx (30 TC)
- [ ] User review; xác nhận công thức cost theo giờ + chỗ áp vào tổng phiếu/công nợ

### Checkpoint — 2026-06-29
Đã sinh testcase.xlsx (30 TC) cho Tab bốc xếp tính chi phí theo thời gian (task_10308). Chờ user review.
