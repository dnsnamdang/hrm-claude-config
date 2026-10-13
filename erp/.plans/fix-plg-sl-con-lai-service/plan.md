# Fix: PLG (phụ lục giảm) HĐ dịch vụ — "SL còn lại trên HĐ" của mục dịch vụ không trừ SL đã hoàn thành

## Vấn đề (user báo, HĐ 5052)
HĐ HDDV_TPE_HN_CSKH_26_0145 có mục dịch vụ "Sửa chữa/thay thế kép nối" SL 30.
PDKQ TPE.PDKQ.2026011447 đã tích hoàn thành 5 mục (is_completed=1, 5 dòng qty=1).
Làm PLG: cột "SL còn lại trên HĐ" hiển thị 30, đúng ra phải 25 (30 - 5 đã hoàn thành).

## Chẩn đoán (verify prod erp_new)
- Cột "SL còn lại trên HĐ" (form.blade dòng 304) = `service.contract_qty`.
- Tính ở `WrServiceContract::getForAnnex()` dòng 2480:
  `contract_qty = quantity - annex_qty - getAssigningQty($serial)`
- `getAssigningQty` (WrServiceContractProductService) đếm SL phiếu giao việc status ∈ {1 DANG_GIAO, 7 DANG_NHAP_KQ, 2 DA_NHAP_KQ, 8 DANG_DUYET_KQ}, `whereNull(parent_id)`.
- Data HĐ 5052: phiếu giao cha TPE.PGV.2026010894 status=3 (DA_DUYET_KET_QUA=đã duyệt KQ), qty 30. PDKQ con 11447 status=2, 30 dòng, **5 dòng is_completed=1**.
- → status 3 KHÔNG có trong whereIn → getAssigningQty=0 → contract_qty = 30 - 0 - 0 = 30 (SAI, đúng phải 25).

## Nguyên nhân gốc
Khi phiếu giao việc đã duyệt kết quả (status 3): SL đã HOÀN THÀNH (is_completed=1) không còn được đếm là "đang giao" nên KHÔNG bị trừ khỏi "SL còn lại" → SL đã làm xong vẫn hiển thị là có thể giảm.
(product dòng 2477 dùng getAssigningProcessQty CÓ nhánh đếm finish_percent==100; service getAssigningQty KHÔNG có.)

## Hướng sửa (đề xuất — CHỜ user xác nhận business rule)
Cách A: getForAnnex trừ thêm SL đã hoàn thành = tổng qty is_completed=1 (finish_percent=100) trong PDKQ đã duyệt của HĐ cho service đó.
Cách B: sửa getAssigningQty thêm status 3 (DA_DUYET_KET_QUA) nhưng chỉ đếm is_completed=1 (tránh trừ nhầm 25 chưa hoàn thành).
→ Kỳ vọng user: SL còn lại = 30 - 5(hoàn thành) = 25. (25 đã giao nhưng CHƯA hoàn thành vẫn giảm được.)

## Tasks
- [x] Chẩn đoán + verify prod (5 is_completed khớp)
- [ ] Chốt business rule với user (chỉ trừ đã-hoàn-thành, hay trừ cả đang-giao?)
- [ ] Sửa getForAnnex / getAssigningQty theo rule
- [ ] Verify HĐ 5052 → contract_qty=25
- [ ] Kiểm không phá product / warranty / các loại service khác

## ĐÃ SỬA (2026-07-29)
User chốt: trừ cả đang giao chưa xong + đã hoàn thành (giống product).
- getAssigningQty là HÀM DÙNG CHUNG (~15 nơi: giao việc/quyết toán/assembly = "SL đang giao") → KHÔNG sửa.
- Thêm method `WrServiceContractProductService::getCompletedResultQty()`: đếm SL is_completed=1 ở PDKQ con (parent_id NOT NULL) theo cost_name + HĐ. KHÔNG lọc serial (PDKQ con serial_old là index '1', khác serial thiết bị HĐ).
- Sửa `getForAnnex` dòng 2480 (choose_services): `contract_qty = quantity - annex_qty - getAssigningQty(serial) - getCompletedResultQty()`.
- Verify HĐ 5052 kép nối: quantity=30, completed=5 → lúc chưa có phụ lục (annex=0): SL còn lại=25 (trước fix=30). Sau khi đã giảm 25: =0 (đúng).
- KHÔNG đụng dòng 2506 (extend_products service = class khác, user không báo).

## Tasks
- [x] Chẩn đoán + verify prod (5 is_completed)
- [x] Chốt business rule (giống product)
- [x] Thêm getCompletedResultQty + sửa getForAnnex 2480
- [x] Verify contract_qty=25 (lúc chưa có phụ lục)
- [ ] User test browser màn PLG với HĐ có mục dịch vụ đã hoàn thành 1 phần
- [ ] CHƯA commit (chờ user xác nhận)

### Checkpoint — 2026-07-29
Vừa hoàn thành: fix "SL còn lại trên HĐ" mục dịch vụ ở màn PLG trừ thêm SL đã hoàn thành. php -l sạch. Verify HĐ 5052 logic đúng (25 lúc chưa có phụ lục).
Bước tiếp: user test browser + quyết commit.
Blocked: —
