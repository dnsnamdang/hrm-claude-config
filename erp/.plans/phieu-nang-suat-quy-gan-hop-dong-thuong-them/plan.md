# Phiếu quyết toán thưởng năng suất quý mới: gán thưởng thêm vào 1 HĐ (Cách B)

## Mục tiêu
Khi hạch toán, khoản thưởng thêm (account 117/work TT) của phiếu BillProductivitySettlementQuarter
phải GẮN với 1 hợp đồng (contractable) → downstream (báo cáo thu nhập, kết chuyển) vốn lọc theo HĐ mới hiện.

## Phát hiện
- Thưởng thêm chỉ ở mức NV (sum_commission_bonus_employee); per-contract commission_bonus_employee = 0.
- Nhưng bảng bill_productivity_settlement_quarter_contracts đã lưu DANH SÁCH HĐ mỗi NV
  (contractable_id/type/code + sum_commission_employee).

## Đã sửa (branch master, php -l sạch)
- [x] BillProductivitySettlementQuarter::saveAccounting: mỗi NV chọn HĐ có sum_commission_employee LỚN NHẤT
      (relation contracts()), gán contractable_id/type/code vào bút toán Có 3351/Work=9 (→ account 117).
      Fallback NULL nếu NV không có HĐ.

## Lưu ý
- Cách chọn HĐ: lớn nhất theo hoa hồng (deterministic). Nếu muốn random/ khác → đổi orderBy.
- 4 phiếu prod đã hạch toán trước đó vẫn contractable NULL → cần CHẠY LẠI hạch toán để áp
  (xóa account_details cũ + saveAccounting lại). Hỏi user cách chạy lại.
- Đã revert hướng sửa report/kết chuyển trước đó (Cách A) — giờ dùng Cách B ở phiếu.
## Branch: master

## Cập nhật — đồng bộ với Cách B (tránh double-count)
- [x] BỎ fix Cách A ở CommissionSettlementQuarterReportService (leftJoinSub 'productivity' + COALESCE + import).
      Vì Cách B đã gắn HĐ → getDataFirm/getDataWr tự lấy thưởng thêm; nếu giữ leftJoinSub sẽ cộng 2 lần.
- [x] Kết chuyển (ClosingEntry) đã revert Cách A trước đó → giờ tự lấy được nhờ Cách B (contractable đã set).
- Tóm lại: chỉ còn 1 điểm sửa gốc = phiếu gắn HĐ; report & kết chuyển KHÔNG cần đụng.
