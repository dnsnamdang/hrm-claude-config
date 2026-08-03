# Testcase — Danh mục giá bốc xếp: đơn giá công ty & thuê ngoài theo Giờ (task_10308)

## Phạm vi
Màn Danh mục giá bốc xếp (ArrangeGood, common.delivery_arrange): bổ sung đơn giá THEO GIỜ — 'Đơn giá công ty / Giờ' (company_price_hour) + 'Đơn giá thuê ngoài / Giờ' (price_hour), cạnh đơn giá theo TẤN cũ (company_price / price). CRUD + validation + hiển thị 'tấn/giờ'. (Khác testcase `boc-xep-chi-phi-theo-gio-task10308` — đó là Tab bốc xếp tính chi phí trên phiếu.)

## Nguồn tham chiếu (task_10308, commit 4843dde4e8)
- Controller: `app/Http/Controllers/Warehouse/ArrangeGoodController.php` (index/searchData/store/edit/delete; store ép 0 khi tắt loại; editColumn giá 'tấn/giờ')
- Request: `app/Http/Requests/Common/ArrangeDeliveryRequest.php` (≥1 loại; price/company_price required_if is_weight + not_in:0; price_hour/company_price_hour required_if is_time)
- View: `resources/views/common/delivery_arrange/modalPopup.blade.php` (khối Tấn ng-show is_weight; khối Giờ ng-show is_time)
- Migration: `2026_05_15_000001_add_hourly_price_to_arrange_goods` (is_weight, is_time, company_price_hour, price_hour)
- Routes: `arrangeGood.*` (web.php ~5764)

## Output
- `generate-testcase.py` + `testcase.xlsx` — **30 TC**, P0 53%, 6 section, đủ 9 mục mô tả.

## 6 section
- I. Hiển thị trang & modal (2 khối Tấn/Giờ, type_name) — 5 TC
- IV. Danh sách định mức (cột giá 'tấn/giờ', chỉ-Tấn/chỉ-Giờ, audit) — 4 TC
- V. CRUD định mức (thêm Tấn/Giờ/cả hai, sửa, đổi loại, xóa) — 7 TC
- VI. Edge & validation (≥1 loại; required_if + not_in:0 từng đơn giá; số âm) — 7 TC
- VII. Store logic & cô lập (chỉ Tấn→giờ=0; chỉ Giờ→tấn=0; mở lại giữ đúng) — 3 TC
- VIII. E2E (định mức Giờ dùng ở phiếu; công ty vs thuê ngoài; báo cáo NCC; snapshot giá) — 4 TC

## Tasks
- [x] Khảo sát task_10308: ArrangeGoodController catalog + modal 4 đơn giá + validation
- [x] Generator + testcase.xlsx (30 TC)
- [ ] User review; xác nhận field type_name + rent_type (công ty/thuê ngoài) mapping đơn giá ở phiếu

### Checkpoint — 2026-06-30
Đã sinh testcase.xlsx (30 TC) cho Danh mục giá bốc xếp (đơn giá theo giờ — công ty + thuê ngoài), task_10308. Chờ user review.
