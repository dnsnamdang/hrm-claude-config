# Fix batch: 4 phiếu xuất về xuất từ tồn kho (giống PXK-28762/29117)

## Bối cảnh (xác minh prod erp_new) — tất cả kho 4, cty 4, chưa có product_export
| PXK | request_id | dòng sửa | prod | prepick→0, giữ total |
|-----|-----------|----------|------|----------------------|
| PXK-28946 | 28894 | #71708 | 8004 Thiết bị cân bằng lốp | 1→0, total 1 |
| PXK-29052 | 29092 | #72170 | 22567 Tấm lót sàn nhựa | 7→0, total 7 |
| PXK-29096 | 28897 | #71713 | 5590 Dây áp lực 15m | 1→0, total 1 |
| PXK-29053 | 28971 | #71882 | 16136 Giá treo dụng cụ SST | 1→0, total 1 |

## Fix
- [x] Thêm `fixPxkBatchExportFromStock_20260720()` vào UpdateDB.php (zero export_prepick_qty+export_hold_qty, giữ total).
- [x] Chạy trên prod → mỗi phiếu sửa 1 dòng, verify 4/4 về tồn kho.
- [ ] User mở lại create từng phiếu → tạo phiếu xuất tồn kho OK.

## Không làm: không đụng prepick_details/logs, không sửa guard ProductExport.php.
