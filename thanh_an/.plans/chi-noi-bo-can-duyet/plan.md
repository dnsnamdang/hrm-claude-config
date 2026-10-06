# Chỉ Cung ứng nội bộ cần duyệt (đề xuất + phiếu xử lý)

@khoipv — Bắt đầu 01/10/2026

## Yêu cầu
- Chỉ phiếu đề xuất loại Cung ứng nội bộ mới cần BGĐ duyệt.
- Phiếu xử lý của các loại khác nội bộ cũng không cần duyệt.

## Phase 1 — BE phiếu đề xuất
- [x] `SupplyProposal::typeNeedsBoardApproval()` chỉ còn `TYPE_NOI_BO` + sửa comment
- [x] `getIsCanApproveAttribute()`, `SupplyProposalService::approve()` / `rejectByBoard()`: bỏ điều kiện loại, chỉ check trạng thái Chờ BGĐ duyệt (+ quyền)
- [x] Sửa comment "nội bộ / khách lẻ chờ BGĐ" trong `SupplyProposalService`

## Phase 2 — BE phiếu xử lý
- [x] Thêm `SupplyHandling::typeNeedsApproval($type)` (chỉ `TYPE_NOI_BO`)
- [x] `SupplyHandlingService::submitStatus()` dùng hàm trên
- [x] `SupplyHandlingService::update()`: nhánh sửa phiếu bị từ chối → `submitStatus($model->type)`
- [x] `SupplyHandling::canApprove()`: bỏ điều kiện loại, chỉ check Chờ duyệt + quyền; sửa comment `is_can_edit`

## Phase 3 — FE
- [x] Sửa comment sai ở `pages/supply/supply_handlings/add.vue` (nút duyệt)

## Phase 4 — Kiểm tra
- [ ] Đề xuất khách lẻ / HĐ… gửi → Chờ xử lý; lập PXL → Đã xử lý, đề xuất tính lại SL
- [ ] Nội bộ: đề xuất + PXL vẫn qua duyệt như cũ

### Checkpoint — 01/10/2026
Vừa hoàn thành: BE đề xuất + PXL chỉ nội bộ cần duyệt; guard duyệt bỏ check loại; sửa comment FE. php -l OK; tinker: typeNeedsBoardApproval/typeNeedsApproval chỉ true với type 2, submitStatus(1,3,6)=5, submitStatus(2)=3
Đang làm dở: —
Bước tiếp theo: test UI Phase 4 (gửi đề xuất khách lẻ/HĐ → Chờ xử lý; lập PXL → Đã xử lý; nội bộ vẫn qua duyệt)
Blocked:
