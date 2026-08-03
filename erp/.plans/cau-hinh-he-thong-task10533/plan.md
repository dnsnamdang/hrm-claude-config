# Testcase — Cấu hình hệ thống (task_10533): toàn màn

## Phạm vi (theo mô tả task_10533)
1. Update cấu hình VAT vận chuyển (tab Kho — `vat_delivery_trip_percent`)
2. Update cấu hình loại hàng hóa không hiển thị trên các phiếu (tab Danh mục — `hidden_product_types` → `config_hidden_product_types`)
3. Chỉnh form cấu hình theo file đính kèm → **tái cấu trúc form thành 7 tab**, lưu từng tab độc lập (`updateTab('{tab}')`)
4. Lịch sử chỉnh sửa cấu hình (`config_histories`, API `configs/histories/{tab}`)
5. Xem chi tiết lịch sử (old_value → new_value, người sửa, thời gian)

## 7 tab + field (nhánh task_10533, ConfigsController)
- general: logo, title, description
- category: max_borrow_date, max_prepick_date, consignment_holding_time, max_prepick_date_project_contract, warning_day, product_types, hidden_product_types
- business: customer_is_following, customer_taken_care, quotation_valid_days, project_quotation_valid_days, customer_register_expiry, customer_groups, department_groups, ràng buộc HĐ (is_*)
- warehouse: vat_delivery_trip_percent
- xnk: environment_tax
- accounting: coefficient_ecommerce_price, debt_calculation_date
- cskh: serial_product_types, contract_rows

## Output
- `generate-testcase.py` + `testcase.xlsx` — **48 TC**, P0 42%, 5 section, đủ 9 mục mô tả.

## 5 section
- I. Hiển thị & truy cập (form 7 tab) — 8 TC
- V. Lưu cấu hình theo từng tab (general/category/VAT/ẩn hàng/business/xnk/accounting/cskh) — 12 TC
- VI. Edge & validation theo từng tab (required/numeric/min/max/integer/date + hidden rows + contract_rows + rule nhóm-vs-tính-chất) — 15 TC
- VII. Lịch sử & xem chi tiết (#4/#5: old→new, per-tab, updater, tab không hợp lệ) — 6 TC
- VIII. Cô lập tab & E2E (lưu tab độc lập; ẩn hàng / VAT / ngày mượn-giữ / hiệu lực báo giá áp xuống nghiệp vụ) — 7 TC

## Tasks
- [x] Khảo sát task_10533: 7 tab + FIELD_LABELS + getValidationRules từng tab + updateTab + histories(tab)
- [x] Generator + testcase.xlsx (48 TC) — đã thay testcase hẹp cũ (vat+ẩn hàng) bằng bản toàn màn
- [ ] User review; xác nhận file đính kèm form để khớp thứ tự/nhãn tab (mục #3, #5)

### Checkpoint — 2026-06-29
Đã sinh testcase.xlsx (48 TC) phủ toàn màn cấu hình task_10533 (7 tab + lịch sử + xem chi tiết). Folder hẹp cũ `cau-hinh-vat-vc-loai-hang-an` đã xóa. Chờ user review (đối chiếu file đính kèm).
