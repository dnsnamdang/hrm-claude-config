# Design — Chỉ Cung ứng nội bộ cần duyệt (đề xuất + phiếu xử lý)

- **Mục tiêu:** bỏ bước duyệt với mọi loại trừ Cung ứng nội bộ (type 2), áp cho cả phiếu đề xuất (BGĐ duyệt) lẫn phiếu xử lý (duyệt PXL).
- **Trước:** đề xuất type 2,3,4,5,6 → Chờ BGĐ duyệt; PXL mọi loại trừ type 1 → Chờ duyệt.
- **Sau:** chỉ type 2 qua duyệt. Đề xuất loại khác gửi → Chờ xử lý (3); PXL loại khác gửi chính thức → Đã duyệt/Đã xử lý (5).
- **Điểm sửa BE:**
  - `SupplyProposal::typeNeedsBoardApproval()` → chỉ `TYPE_NOI_BO`.
  - `SupplyHandling::typeNeedsApproval()` (mới, tách riêng khỏi đề xuất vì khác quyền/khác bước) → chỉ `TYPE_NOI_BO`; dùng ở `SupplyHandlingService::submitStatus()`.
  - `SupplyHandlingService::update()`: PXL từng bị từ chối duyệt sửa lại → `submitStatus(type)` thay vì ép Chờ duyệt.
- **Phiếu cũ đang dở dang** (đề xuất status 2 / PXL status 3 thuộc loại không còn cần duyệt): duyệt/từ chối chỉ kiểm tra trạng thái + quyền, KHÔNG kiểm tra loại → người duyệt xử lý nốt, không migration (user chốt 01/10/2026).
- **Hệ quả:** PXL loại 3–6 gửi chính thức là chốt 5 → không sửa/xóa được nữa (giống type 1).
- **FE:** không đổi logic (nút duyệt dựa `is_can_approve` / `can_approve` từ BE), chỉ sửa comment.
