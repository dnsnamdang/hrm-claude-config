# Fix — Invoice2: lập nhiều lần & sửa invoice với hàng bảo hành/KM/thừa thiếu chưa lập hết

## Bối cảnh
Lập Invoice từ BuyContract2. Lần lập SAU phải lấy đúng SL còn lại (`available_qty = qty - invoice_qty`). Khảo sát thấy:
- CREATE lần sau: ĐÚNG (`BuyContract2::getDataForInvoice` line 440 tính available tươi; FE filter >0 + clamp).
- **UPDATE: double-count `invoice_qty`** — `Invoice2Controller@update` gọi `syncProductGuarantees/Promotions/Discrepancies` (làm `invoice_qty += qty`) mà KHÔNG revert phần cũ trước (chỉ `delete()` có revert, và còn thiếu revert "thừa thiếu").
- **FE sửa invoice**: `addBuyContract2` chạy `calculateProductGuarantees()` cả khi edit (guard bị comment) → ghi đè dòng đã lưu bằng "remaining" (đã trừ cả phần invoice này) → dòng đã lập hết biến mất, SL sai; `syncQty()` không reconcile hàng bảo hành.

## Fix đã làm
### BE (data integrity — cả 3 loại)
- [x] `app/Model/Order/Invoice2.php`: thêm `revertProductGuaranteesQty()`, `revertPromotionsQty()`, `revertProductDiscrepanciesQty()` — trừ `qty` của các dòng con hiện tại khỏi `BuyContract2*.invoice_qty` (clamp ≥ 0).
- [x] `Invoice2Controller@update`: gọi 3 revert TRƯỚC `sync*` (đọc dòng cũ → trừ → sync re-add ⇒ `invoice_qty` đúng).
- [x] `Invoice2Controller@delete`: thay 2 revert inline (bảo hành+KM) bằng 3 method (DRY) + **bổ sung revert "thừa thiếu"** (trước đây thiếu → leak invoice_qty).

### FE (form sửa — hàng bảo hành, phần được báo)
- [x] `partials/classes/order/Invoice2.blade.php`:
  - `addBuyContract2`: guard `calculateProductGuarantees()` chỉ chạy khi CREATE; khi EDIT gọi `syncQtyGuarantees()` (giữ dòng đã lưu).
  - Thêm `syncQtyGuarantees()`: với mỗi dòng bảo hành đã lưu, set `available_qty = contract.available_qty (remaining) + _qty (own)` → clamp SL đúng, dòng đã lập hết vẫn hiện.
  - (Khuyến mại/thừa thiếu FE giữ nguyên hành vi cũ — chỉ sửa BE cho 2 loại này.)

## Giới hạn / lưu ý
- Revert dùng logic đơn giản (trực tiếp theo `buy_contract_*_id`), KHÔNG xử lý cascade tràn sang phụ lục (giống `delete()` cũ). Trường hợp over-invoice tràn phụ lục là edge case.
- `delete()` vẫn không xóa bản ghi `Invoice2ProductDiscrepancy` con (orphan) — gap có sẵn, chưa đụng (ngoài phạm vi).
- FE reconcile chưa cộng phần annex remaining cho bound (dùng contract chính + own) — đủ cho case phổ biến.

## Kiểm thử (user — chạy app)
- [ ] HĐ có hàng bảo hành SL=10. Lập invoice #1 lấy 4 → còn lại 6. Lập #2: form hiện 6 (đúng), sửa được, không vượt 6.
- [ ] SỬA invoice #1 (đang lấy 4): form hiện dòng bảo hành với SL=4, bound = 6+4=10 còn lại đúng (không bị mất dòng, không double-count). Đổi 4→5, lưu → còn lại 5.
- [ ] Xóa invoice có hàng bảo hành/KM/thừa thiếu → `invoice_qty` hoàn đúng (lập lại được full).
- [ ] Lập nhiều lần khuyến mại / thừa thiếu → SL còn lại đúng sau update.

### Checkpoint — 2026-06-10
Vừa hoàn thành: BE revert (update + delete, 3 loại) + FE reconcile hàng bảo hành; php -l sạch
Bước tiếp theo: user chạy thử các ca create/update/delete
Blocked:
