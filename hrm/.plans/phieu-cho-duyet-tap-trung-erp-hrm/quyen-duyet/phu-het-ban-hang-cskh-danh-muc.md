# Phủ hết màn duyệt — Bán hàng / CSKH / Vận chuyển / Danh mục — @cuong61n (17/11/2026)

Chi tiết từng phần: `phu-het-ban-hang-a-ke-hoach-nv.md` · `phu-het-ban-hang-b-customer-care.md` · `phu-het-ban-hang-c-master-data-transport.md`.
Migration đã chạy trên DB local: `Modules/Finance/Database/Migrations/2026_11_14_000001_add_hrm_columns_to_employee_plans.php` (chỉ file này).
Đợt 2 thêm 9 loại mới: sale_plan_employee, market_plan_employee, division_market_department, warranty_repair_request, warranty_repair_handle_request, wr_service_quotation, assign_other_request, wr_service_annex, delivery_trip, price_calculate_request; sửa (tăng version): wr_service_contract (cấp 2 chờ tiếp nhận), other_delivery_trip (cấp 2 chờ hạch toán).
Chưa làm, chờ user chốt: handover_record (Biên bản bàn giao sơ bộ) — màn không có gate nào, xem file B mục 4.
