# Fix: order_stock_progress mồ côi khi PI→HĐ→báo hàng về (báo cáo Luân chuyển sai)

## Vấn đề
Báo cáo Luân chuyển hàng hóa: cột "Hàng đang về" (tổng) đúng (7.000L, dùng arriving_qty), nhưng modal chi tiết (getStockTranfer) cộng ra 15.400L (sai) vì đọc `order_stock_progress.qty` đang bị "mồ côi".

## Root cause (data-integrity)
Luồng CHUẨN: Đơn → PI (theo HĐ nguyên tắc) → HĐ mua sinh TỪ PI (inland_buy_contract_news.inland_purchase_invoice_new_id) → Báo hàng về (InlandProductArrivedNew, gắn HĐ mua).
- Progress giai đoạn PI có `objectable_type=InlandPurchaseInvoice`, `objectable_id=PI_id`.
- Khi báo hàng về, `InlandProductArrivedNew.php` (3 chỗ: 387-392, 415-420, 440-445) tìm progress tiền nhiệm để TRỪ theo `objectable_id=inland_buy_contract_new_id` + `objectable_type=InlandBuyContractNew`.
- → Với đơn progress đang ở PI (không có progress HĐ riêng), query KHÔNG khớp → không trừ → **progress PI kẹt giá trị gốc ("mồ côi")**.
- arriving_qty vẫn đúng (giảm qua ProductImport khi nhập kho thật).
- Phạm vi: **775 progress PI mồ côi** toàn hệ thống (PI qty>0 + đã có Arrived).

## Hướng sửa (user chốt: fix cả GỐC, hướng B)
**B — Nới điều kiện tìm progress tiền nhiệm ở bước báo hàng về**: thay vì hard-code `objectable_id=contract_id + type=InlandBuyContractNew`, tìm progress tiền nhiệm của cùng orderable (qty>0) theo CẢ HAI type [InlandBuyContractNew, InlandPurchaseInvoice] (bỏ ràng buộc objectable_id theo contract). Lấy progress "tiền nhiệm gần nhất qty>0".

## Scope
- Phase 1: Fix code InlandProductArrivedNew.php (3 chỗ) — progress tương lai đúng.
- Phase 2: Data-fix dọn 775 progress PI mồ côi hiện có (UpdateDB, chạy prod sau review).
- Phase 3: Verify report Luân chuyển (product 7579 → 7.000 khớp) sau fix; nếu report vẫn lệch do multi-progress thì mới đụng getStockTranfer.

## Lưu ý
- CHỈ luồng INLAND (trong nước). Hàng ngoại (PurchaseInvoice/BuyContract2/Invoice2) CHƯA rà — ghi nhận, out scope.
- getStockTranfer 4 nhánh (4434/4637/4862/5094) dùng progress.qty — nếu progress đúng sau fix thì không cần sửa; verify ở Phase 3.
