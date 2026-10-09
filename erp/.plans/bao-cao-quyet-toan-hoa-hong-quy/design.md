# Báo cáo Bảng tổng hợp quyết toán hoa hồng quý — Fix cột DS tiêu chuẩn

## Bối cảnh
Báo cáo `commission-settlement-quarter` (`app/Services/Reports/CommissionSettlementQuarterReportService.php`).

- **Dòng hiển thị** lấy từ `account_details` (account_id=117), lọc theo `ac.invoiceable_date_accounting`
  (ngày hạch toán **hoa hồng**) trong `filterAcc()`.
- **Cột "DS tiêu chuẩn tính thưởng năng suất tháng/quý"** (`standard_month`, `standard_quarter`
  = `round(settlement_firm.commission_sale)`) lấy từ subquery quyết toán, lọc **riêng** theo
  `settlement_contracts.date_accounting`.

## Bug
Khi hoa hồng và quyết toán của cùng 1 HĐ **lệch tháng hạch toán**, cột DS bị mất:
- Ví dụ HĐ 6234 (HĐ_TPSG_KV2_25_0056), NV Nguyễn Văn Bình (id 66):
  hoa hồng hạch toán **tháng 8**, quyết toán TPSG.QTHD.02018 hạch toán **31/07**, DS = 697.256.251.
- Lọc tháng 7: dòng HĐ không hiện (không có hoa hồng tháng 7) → DS mất.
- Lọc tháng 8: dòng hiện nhưng cột DS trống (quyết toán ở tháng 7, ngoài filter tháng 8).
- → DS 697M không hiển thị được ở bất kỳ tháng nào.

## Quyết định (2026-09-05) — Hướng A
Cho cột DS **bám theo dòng hoa hồng**: bỏ filter `sc.date_accounting >= date_from / <= date_to`
trong các subquery quyết toán. Dòng nào hiện (có hoa hồng trong kỳ) thì lấy DS của phiếu quyết
toán type=2 tương ứng, không phụ thuộc phiếu quyết toán hạch toán tháng nào.

### Căn cứ an toàn (ground-truth trên erp_new)
- **R1 = 0**: không cặp (HĐ, NV) nào có >1 phiếu quyết toán type=2 → mỗi cặp đúng 1 phiếu →
  LEFT JOIN không nhập nhằng khi bỏ filter ngày.
- **R2 = 2457**: có 2457 cặp hoa hồng trải nhiều tháng → nếu lọc từng tháng, DS lặp lại mỗi tháng
  có hoa hồng của cặp đó. Chấp nhận được vì đây là báo cáo QUÝ (lọc trọn quý mỗi HĐ chỉ 1 dòng).

## Phạm vi sửa
4 subquery trong service (Firm + WrService, nhánh NV lẫn nhánh trưởng phòng):
- `getDataFirm`: `settlement_firm` (dòng 110-111) + `settlement_firm_lead` (dòng 141-142)
- `getDataWr`: `settlement_firm` (dòng 268-269) + `settlement_firm_lead` (dòng 298-299)

**Giữ nguyên**: cột "Thưởng năng suất tính lũy tiến" (subquery `progressive`,
`bill_commission_settlement_quarter.date_accounting`, dòng 413-417) — nguồn khác, ngoài phạm vi.
