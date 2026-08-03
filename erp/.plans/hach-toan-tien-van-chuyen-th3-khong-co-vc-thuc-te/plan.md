# Plan — Bổ sung hạch toán tiền vận chuyển TH3 cho quyết toán HĐ DỊCH VỤ

## Bối cảnh
`WrSettlementContractAccountingService::deliveryAccounting()` (quyết toán HĐ dịch vụ - WrServiceContract, dòng 1549) hạch toán tiền vận chuyển. Hiện có TH1 + TH2, **THIẾU TH3** (bản HĐ hãng `FirmSettlementContractAccountingService` có TH3 nhưng đang comment ở dòng 1660-1669).

- TH1 (1566): `getAmountDelivery(148) != 0` → 3351/35241 + 5211/3351 (theo giảm giá so `quota_discount_total`)
- TH2 (1589-1601): 148=0 → `$amount=getAmountDelivery(230)`; nếu 230≠0 & giảm giá & before>amount → book chênh `before_vat_delivery_cost - amount` vào 5211/3351
- TH3 (CẦN THÊM): 148=0 & 230=0 → không có vận chuyển thực tế → book TOÀN BỘ `before_vat_delivery_cost` vào 5211/3351

## Nghi vấn bug kế bên (cần hỏi)
- Dòng 1593: trong vòng lặp annex của nhánh else, dùng `getAmountDelivery($annex->id, 148)` thay vì **230** (main contract dùng 230 ở 1590). Bản HĐ hãng dùng 230 cho annex. → có thể là bug, ảnh hưởng điều kiện TH2/TH3.

## Cần chốt với user
- [ ] TH3 book toàn bộ `before_vat_delivery_cost` VÔ ĐIỀU KIỆN (như comment bản HĐ hãng) hay có điều kiện giảm giá như TH2?
- [ ] Bút toán: Nợ 5211 / Có 3351, Work TVC — đúng?
- [ ] Có sửa luôn bug dòng 1593 (148→230) không?
- [ ] Chỉ sửa bản DỊCH VỤ, hay bật luôn TH3 bản HĐ hãng (đang comment)?

## Quyết định (user)
- Thêm TH3 vào HĐ dịch vụ GIỐNG y hệt HĐ hãng (book toàn bộ before_vat_delivery_cost, vô điều kiện).
- HĐ hãng: user đã tự bỏ comment TH3 (không cần tôi sửa).
- Không sửa nghi vấn dòng 1593 (148 vs 230) trong lần này.

## Tasks
- [x] Định vị: TH3 thiếu ở WrSettlementContractAccountingService (1549)
- [x] Chốt nghiệp vụ với user
- [x] Thêm TH3 vào WrSettlementContractAccountingService::deliveryAccounting (else if $amount==0 → book full before_vat_delivery_cost vào 5211/3351, Work TVC) — giống bản HĐ hãng
- [x] php -l sạch
- [ ] User test browser: quyết toán HĐ dịch vụ không có chuyến xe → có bút toán 5211/3351 = tiền VC trước thuế

### Checkpoint — 2026-06-23
Vừa hoàn thành: Thêm TH3 vào WrSettlementContractAccountingService::deliveryAccounting giống bản HĐ hãng; php -l sạch.
Đang làm dở: không.
Bước tiếp theo: User test browser quyết toán HĐ dịch vụ không có chuyến xe.
Blocked:

### Checkpoint — 2026-06-23 (bổ sung)
Đã sửa bug dòng 1593: annex `getAmountDelivery(..., 148)` → `230` cho khớp HĐ hãng. php -l sạch.
Còn lại: user test browser quyết toán HĐ dịch vụ (có phụ lục + không chuyến xe).

## Phạm vi
- `app/Services/Sale/WarrantyRepair/Settlement/WrSettlementContractAccountingService.php` (~1589-1602)
