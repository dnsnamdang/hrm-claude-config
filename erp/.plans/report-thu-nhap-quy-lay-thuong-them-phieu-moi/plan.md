# Report thu nhập quý: lấy "Thưởng thêm" từ phiếu năng suất quý (phiên bản mới)

## Vấn đề
Report admin/reports/commission-settlement-quarter không hiện "Thưởng thêm" của phiếu
BillProductivitySettlementQuarter (phiên bản mới) dù data hạch toán đúng (account 117/type2/work TT).

## Root cause
`getData()` union 2 nguồn getDataFirm + getDataWr — CẢ 2 đều bắt buộc account_details gắn hợp đồng
(`whereNotNull contractable_id` + contractable_type = FirmContract / WrServiceContract).
Phiếu mới post "Thưởng thêm" theo NHÂN VIÊN, KHÔNG gắn hợp đồng (contractable=NULL) → bị loại.
(Phiếu cũ BillCommissionSettlementQuarter post TT CÓ gắn contract nên hiện được.)

## Fix (hướng A — sửa report)
- [x] Thêm import BillProductivitySettlementQuarter vào service.
- [x] Thêm leftJoinSub `productivity` (account 117/type2/work TT từ phiếu mới, gom theo employee_id,
      reuse filterAcc — date/dept/permission, KHÔNG cần contract).
- [x] Cộng vào cột: `SUM(result.commission_bonus_quarter) + COALESCE(productivity.commission_bonus_quarter,0)`.
- [x] php -l sạch; mô phỏng dept 52 ra số/NV OK.
- [ ] User test trên dev/prod.

## Hạn chế (báo user)
- productivity là LEFT JOIN từ `result` (union firm/wr). NV nào CHỈ có thưởng thêm mà KHÔNG có
  hoa hồng hợp đồng trong kỳ → không có trong `result` → không hiện. Nếu cần hiện cả nhóm này
  phải thêm nhánh union đầy đủ (phức tạp hơn).
- Không double count: firm/wr loại NULL-contract; productivity chỉ lấy phiếu mới.

## Branch: master
