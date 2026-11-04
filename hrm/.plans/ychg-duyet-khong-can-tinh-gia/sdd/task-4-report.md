# Task 4 report — ptkdApprove xử lý dòng 9

File: Modules/MasterData/Services/PriceCalculation/PriceAskingRequestWriter.php (ptkdApprove + 2 private helper `resolveNoPriceLines`, `promoteNoPriceLine`).

## Đồng giá 6 loại
`promoteNoPriceLine` dựng 6 dòng giá (TYPE_ORDER) price=sale, coefficient = cost>0 ? sale/cost : 0, và set 3 cờ `is_manual_*_online=true` => `ProductPriceWriter::resolvePrices` KHÔNG tự tính loại 6 (Bán lẻ × hệ số TMĐT) mà giữ nguyên `sale`. Sau đó `apply()` (cost = resolver cost, ĐVT = product_units khớp unit_id resolver, fallback ĐVT gốc). Test assert cả 6 loại = sale (TH1 0, TH2 150, ngoại tệ 75000; cost 100/50000). Không nhân tỷ giá lại.

## Promote + atomic
Toàn bộ trong DB::transaction sẵn có. Trước khi ghi gì: gom id status 9 (lines + con recipe), `resolveNoPriceLines` → có dòng null thì ném ValidationException['temp_products' => ["<mã>, <mã>: chưa đủ điều kiện duyệt không cần tính giá"]] ⇒ rollback sạch. Sau đó (cùng chỗ moveProducts 7→2): với mỗi dòng 9: apply giá, trackStatus update pcc 9→3 (where status=9), ensureProductSet, log `temp_approve_no_price`. Dòng 9 KHÔNG qua moveProducts(7→2); luồng 7/8 giữ nguyên.
Nhóm: nhóm có ≥1 dòng 9 và mọi dòng ∈ {9,8} => không cần XNK (tách khỏi $groups trước khi resolve XNK), đóng STATUS_PRICED (4) qua markGroupClosed (log 'Duyệt không cần tính giá'), rồi refreshHead => phiếu STATUS_PRICED(4) nếu mọi nhóm đóng; còn nhóm thường => ASKING(10). Nhóm toàn 8 vẫn CANCELLED như cũ.
Revert site `:684` (ptkdReject) đã xử lý 9→6 ở Task 3, không đụng.

## Audit hạ nguồn
Không có chỗ nào giả định hàng status 3 phải có Phiếu tính giá: ProductLifecycleService (restore) và ProductWriteService đã đưa hàng lên TRADING không qua PTG; picker/QuotationTempGate/ProductService chỉ lọc pcc.status=3; ProductUsageGuard chỉ dùng price_calculate_* để chặn xoá khi hàng ĐÃ dùng. Không cần guard. (Không tìm thấy ERP sync gắn status 3 với PTG trong hrm-api.)

## Tests
`php artisan test Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php` => 21 passed (13 cũ + 8 mới).
`php artisan test Modules/MasterData/Tests/Feature/PriceAskingTempProductTest.php` => 16 passed.
Lưu ý: implement viết trước khi chạy test nên không quan sát được bước "fail" thật.

## Concerns
- apply() -> writePrices xoá giá hiệu lực tương lai (expected) chưa áp của hàng tại công ty (expected_prices=[]) — hàng tạm mới nên thường không có.
- Hệ số (coefficient) = sale/cost là suy diễn; không ràng buộc ở brief.

## Fix round 1 (cost leak)
Note lịch sử `temp_approve_no_price` trước đây chứa "giá nhập X, giá bán Y" và trả nguyên văn ở chi tiết phiếu (PriceAskingRequestService histories) => lộ giá nhập không gate. Đã đổi thành `"<mã>: duyệt không cần tính giá"` (không giá). Thêm test `test_no_price_history_note_does_not_leak_cost` (GET chi tiết phiếu, body không chứa giá nhập; note == chuỗi chỉ mã); đã chạy trên code cũ => FAIL (xác nhận bắt được leak), sau fix => PASS. Thêm comment giải thích hệ số sale/cost. (Lưu ý: `retail_price` = giá bán là field có sẵn của chi tiết phiếu, không phải giá nhập.)
