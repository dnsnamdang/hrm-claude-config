# Check — BC tổng hợp nhu cầu mua có đúng chỉ gồm hàng "Chốt mua thêm" từ PXL?

**Người phụ trách:** @khoipv
**Ngày:** 12/11/2026

## Task
- [x] 1. Đọc query `SupplyReportService::purchaseDemand` (nguồn dữ liệu báo cáo)
- [x] 2. Kiểm cách ghi `alloc_mua` khi lưu PXL (Tạo + Sửa) theo ma trận Nguồn × Phương án
- [x] 3. Đối chiếu dữ liệu DB `thanhan_stag_07052026`: `alloc_mua` vs Σ ô `alloc_buy_*`

## Kết quả
**Đúng** — báo cáo chỉ lấy dòng PXL có SL "Chốt mua thêm".
- Query: `supply_handling_products` where `alloc_mua > 0`, PXL `status = 5` (Đã duyệt), chưa xóa (`SupplyReportService.php:64-70`).
- `alloc_mua` = Σ các ô dòng "Chốt mua thêm" (`alloc_buy_ban/xgui/tgui/xvay/xkho`), suy lại ở `SupplyHandlingService::normalizeMatrix` (dòng 368), gọi ở cả `store` (288) và `update` (587). Ô nguồn Hàng tồn kho / Khách đang vay dồn vào `alloc_<pa>` khác, không vào `alloc_mua`.
- Phiếu cũ trước ma trận: migration `2026_10_23_000001` coi alloc_mua cũ là "Chốt mua thêm".
- DB: 53 dòng PXL đã duyệt, 51 dòng có mua; **0 dòng lệch** giữa alloc_mua và Σ alloc_buy_*.
- Bộ lọc thêm của báo cáo: PXL Nháp / Chờ duyệt / Từ chối KHÔNG lên; mặc định ẩn dòng đã mua đủ; dòng đổi hàng hiện hàng thay thế (B).

### Checkpoint — 12/11/2026
Vừa hoàn thành: soát xong, kết luận đúng
Đang làm dở: —
Bước tiếp theo: chờ user (nếu thấy 1 mã cụ thể lên sai thì gửi mã/PXL để tra)
Blocked:
