# Plan — Fix order_stock_progress mồ côi (báo cáo Luân chuyển)

Nhánh: `fix_bao_cao_luan_chuyen_progress` (ERP TanPhatDev, từ master).

## Phase 1 — Fix GỐC (InlandProductArrivedNew.php)
- [x] Task 1.1: Nới điều kiện tìm progress tiền nhiệm ở 3 chỗ báo-hàng-về (dòng 387-392, 415-420, 440-445): whereIn objectable_type [InlandBuyContractNew, InlandPurchaseInvoice] + qty>0, bỏ ràng buộc objectable_id theo contract. Verify: mô phỏng đơn PI→arrived → progress PI bị trừ đúng. php -l sạch. Commit local.

## Phase 2 — Data-fix progress mồ côi
- [x] Task 2.1: Thêm method UpdateDB dọn 775 progress PI mồ côi (giảm qty PI về đúng SL còn ở giai đoạn = đã trừ phần Arrived). Verify BEFORE/AFTER trên vài đơn (2909/3166/3876) + tổng. CHƯA chạy prod (chờ user duyệt điều kiện).

## Phase 3 — Verify report
- [x] Task 3.1: Sau fix + data-fix (chạy thử trên bản staging hoặc verify tính toán), kiểm getStockTranfer product 7579 → tổng chi tiết = 7.000 (khớp báo cáo). Nếu vẫn lệch do multi-progress → sửa 4 nhánh getStockTranfer (4434/4637/4862/5094).

### Checkpoint — 2026-07-29
Vừa hoàn thành: điều tra root cause (progress PI mồ côi, 775 dòng), user chốt hướng B + SDD, tạo nhánh + plan.
Bước tiếp: dispatch Task 1.1 (fix InlandProductArrivedNew).
Blocked: —

### Checkpoint — 2026-07-29 (FEATURE XONG)
Vừa hoàn thành: fix gốc (InlandProductArrivedNew 3 chỗ) + data-fix method (đã CHẠY prod erp_new: 748 sửa/27 đúng/51 clamp) + verify report=7.000 (từ 15.400). getStockTranfer không cần sửa. Nhánh fix_bao_cao_luan_chuyen_progress HEAD 766481656c, 2 commit, CHƯA push/merge.
Bước tiếp: user test browser (mở lại báo cáo Luân chuyển product 7579 → chi tiết 7.000) + quyết push/merge. Tuỳ chọn: rà luồng HÀNG NGOẠI (PurchaseInvoice/BuyContract2/Invoice2) có cùng bug progress mồ côi không (chưa rà).
Blocked: —
