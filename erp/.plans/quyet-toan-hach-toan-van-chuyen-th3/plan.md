# Testcase — Quyết toán HĐ: hạch toán tiền vận chuyển + bổ sung TH3

## Phạm vi
Bước "8. Hạch toán tiền vận chuyển" (`deliveryAccounting`) trong quyết toán HĐ HÃNG + HĐ DỊCH VỤ. Bổ sung **TH3**: khi TK 148 = 0, xét TK 230 và hạch toán phần chênh tiền vận chuyển.

## Nguồn tham chiếu (code hiện tại)
- HĐ hãng: `app/Services/Sale/Firm/Settlement/FirmSettlementContractAccountingService.php::deliveryAccounting` (~dòng 1606)
- HĐ dịch vụ: `app/Services/Sale/WarrantyRepair/Settlement/WrSettlementContractAccountingService.php::deliveryAccounting` (~dòng 1549)
- `getAmountDelivery(contractable, account_id)` (TK 148 / 230)

## Logic 3 trường hợp
- **TH1**: amount(148)>0 & giảm-giá-HĐ ≤ hạn mức → 5211/3351 = before_vat_delivery_cost.
- **TH2**: amount(148)>0 & giảm > hạn mức → 5211/3351 = min(amount148, before_vat_delivery_cost).
- **TH3 (mới)**: amount(148)=0 → amount(230); nếu amount230≠0 & (discount_product+repair_service+delivery_cost) ≤ hạn mức & before_vat_delivery_cost > amount230 → 5211/3351 = before_vat_delivery_cost − amount230.
- Luôn (khi amount148>0): 3351/35241 = amount148 (work TVC).
- Khác biệt Firm vs Wr: tên field hạn mức (discount_rate_total vs quota_discount_total).

## Output
- `generate-testcase.py` + `testcase.xlsx` — **30 TC**, P0 43%, 5 section, đủ 9 mục mô tả.

## 5 section
- I. Tổng quan bước hạch toán vận chuyển — 4 TC
- V. Các trường hợp TH1/TH2/TH3 (firm + dịch vụ) — 8 TC
- VI. Edge (điều kiện không hạch toán, biên >, bvdc=0) — 8 TC
- VII. Phụ lục bổ sung (cộng dồn amount) — 3 TC
- VIII. Đối chiếu bút toán & cô lập (cân Nợ=Có, note, type, recalc) — 7 TC

## Tasks
- [x] Khảo sát deliveryAccounting (Firm + Wr) + TH1/TH2/TH3 + amount 148/230
- [x] Generator + testcase.xlsx (30 TC)
- [ ] User review; xác nhận số liệu mẫu (amount/bvdc/hạn mức) + nhánh nào của 230 (annex dùng 148 hay 230)

### Checkpoint — 2026-06-30
Đã sinh testcase.xlsx (30 TC) cho hạch toán tiền vận chuyển trong quyết toán HĐ (bổ sung TH3). Chờ user review.
