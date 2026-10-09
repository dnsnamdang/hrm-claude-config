# Fix: Bản in quyết toán NS quý KHÔNG khớp giao diện

## Triệu chứng
User: "in chưa đúng" — bản in các cột **Thưởng thêm / Phân chia / Tổng thu nhập** ở dòng NV nhỏ hơn giao diện.
(VD phiếu 11 — NV id=45: in = 1,113,533 / 70,217,118; giao diện = 1,645,295 / 70,748,880.)

## Nguyên nhân gốc (xác minh trên prod)
- **Giao diện** tính **LIVE** qua getter FE: `base_commission_bonus` = lũy tiến trên `sum_tns_luy_tien` (đã nới own+đóng góp TP/TBP) → thưởng thêm/phân chia/thu nhập theo công thức MỚI.
- **Bản in** (`buildExportData`) đọc **cột đã lưu** (`sum_commission_bonus_employee`, `sum_income_quarter`) — phiếu lưu TRƯỚC khi đổi công thức → số CŨ (own-only).
- → Không phải logic sai; in đọc số lưu cũ, giao diện tính lại. Cột "Tổng TNS lũy tiến" khớp sẵn (đóng góp đã lưu đúng).

## Fix (in tính live y hệt getter FE — KHÔNG đụng giao diện)
- [x] Model `BillProductivitySettlementQuarterEmployee`: thêm accessor `getBaseCommissionBonusAttribute` (tier bậc thang trên `sum_tns_luy_tien`, mirror getter FE).
- [x] `buildExportData` (Controller): 2 lượt — lượt 1 tính live NV bonus (nv/tbp/tp = base×rate) + gom đóng góp cho TBP theo part_id & TP toàn phiếu; lượt 2 dựng dòng: thưởng thêm/phân chia NV = live, dòng TBP/TP = tổng đóng góp NV cấp dưới, thu nhập = cost + own + phân chia(live); dòng tổng cộng dồn từ giá trị live.
- [x] Verify prod phiếu 11: NV45 in mới = 1,645,295 / 70,748,880 = giao diện. `php -l` sạch.
- [ ] User deploy + in lại đối chiếu giao diện.

## Đã revert (hướng sai trước đó)
- Đã revert thay đổi "dòng tổng Tổng TNS lũy tiến chỉ cộng NV" (cả FE getter + BE accessor) — vì đó là sửa LOGIC giao diện, không phải yêu cầu. Tổng "Tổng TNS lũy tiến" giữ = Σ tất cả dòng (309,059,871), khớp giao diện.

## File
- `app/Model/Accounting/BillProductivitySettlementQuarterEmployee.php` (accessor base_commission_bonus)
- `app/Http/Controllers/Accounting/BillProductivitySettlementQuartersController.php` (buildExportData)
