# #12205 — BC thưởng theo quý: HRM lệch số phòng/NV so với ERP

## Kết luận (user chốt 19/11)
ERP cắt trang theo DÒNG HĐ (per_page 10) TRƯỚC rồi mới gộp Phòng → NV ⇒ tổng phòng/NV = tổng HĐ của trang đang xem.
Đây là **ý đồ nghiệp vụ** ⇒ ERP giữ nguyên; HRM sửa theo ERP.

## Lịch sử
- 18/11 sửa nhầm ERP (gộp trước, cắt trang theo phòng): develop_02 8e8a18eaf1, gop_db e61876bb78.
- 19/11 đã revert: develop_02 063a9b1be4, gop_db d8741d1135.
- HRM `BonusQuarterReportService::search()` đổi sang cắt trang theo dòng gốc rồi `tree()`; `pagination.total` = số dòng HĐ;
  `total` vẫn toàn bộ. Export/In vẫn toàn bộ cây (như ERP in/xuất per_page khổng lồ). Test
  `test_paginates_by_contract_rows_before_grouping_like_erp` (kiểm ngược: code cũ đỏ).
