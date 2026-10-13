# Báo cáo commission-settlement-quarter (Bảng tổng hợp thu nhập từ bán hàng)

## Task hiện tại (2026-08-05)
Cột **"DS tiêu chuẩn tính thưởng năng suất tháng"** (`standard_month`): bỏ fallback lấy theo **HTHT** (hỗ trợ hạch toán) khi hợp đồng **không có quyết toán** → cho hiển thị rỗng/"-" giống cột quý.

### Nguyên nhân
`app/Services/Reports/CommissionSettlementQuarterReportService.php`:
- Nhánh Firm dòng 169: `standard_month = round(COALESCE(settlement_firm.commission_sale, firm_sa.commission_sale, 0))` → không có quyết toán rơi về `firm_sa` (HTHT).
- Nhánh Warranty dòng 327: `standard_month = round(COALESCE(settlement_firm.commission_sale, wr_sa.commission_sale, 0))` → tương tự.
- `standard_quarter` (170, 328) chỉ `round(settlement_firm.commission_sale)` → không fallback → hiện "-".

### Fix
Sửa cả 2 dòng standard_month thành `round(settlement_firm.commission_sale)` (giống standard_quarter — chỉ lấy từ quyết toán, không HTHT).

### Tasks
- [x] Trace: standard_month có HTHT fallback (firm_sa/wr_sa), standard_quarter thì không
- [x] Sửa dòng 169 (firm) + 327 (wr) bỏ fallback HTHT → `round(settlement_firm.commission_sale)`
- [x] php -l sạch
- [ ] User verify trên báo cáo: HĐ không quyết toán → cột tháng hiển thị "-" (không còn số HTHT); HĐ có quyết toán → không đổi

### Ghi chú
- Chỉ đụng cột hiển thị `standard_month`; KHÔNG đụng `commission_sale`/`month_employee_amount` (168/167, 326/325) hay các cột thưởng thực (commission_month/quarter).
- Service dùng chung cho list + detail + print + export → sửa 1 chỗ áp dụng cả 4.
