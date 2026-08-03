# Đề xuất cung ứng — gộp 1 luồng trạng thái (design tóm tắt)

**Người phụ trách:** @khoipv · **Ngày:** 2026-08-01

## Mục tiêu
Bỏ mô hình 2 tầng `status` + `handle_status` (suy ra) → **1 luồng trạng thái duy nhất**.

## Bộ trạng thái mới
1 Nháp · 2 Chờ BGĐ duyệt · 3 Đã gửi · **7 BGĐ không duyệt** · **8 Từ chối xử lý** (mới, terminal) · 9 Đã xử lý.

- BGĐ từ chối đề xuất nội bộ → **BGĐ không duyệt** (giữ code 7, đổi tên hằng số).
- Người xử lý từ chối tiếp nhận → **Từ chối xử lý** (code 8), **đóng phiếu**, chỉ cho khi CHƯA có phiếu XL.
- Lập PXL đủ SL → **Đã xử lý** (auto, từ SupplyHandlingService); PXL xóa/từ chối duyệt hụt SL → revert **Đã gửi**.
- Bỏ "Chờ tiếp nhận / Đang xử lý / Đã xử lý xong": xử lý dở vẫn là "Đã gửi".

## Quyết định lớn
- Backfill data cũ: status=3 đã đủ SL → 9. "Từ chối mềm" cũ (bảng rejections) → giữ "Đã gửi".
- **Bỏ bảng** `supply_proposal_rejections` + entity `SupplyProposalRejection` (thao tác phá hủy, đã chốt).
- Thêm cột `rejected_by`, `rejected_at` vào `supply_proposals`; lý do dùng lại `reason_deny`.
- Sửa cả 2 module: SupplyProposal* + SupplyHandlingService (để auto-transition).

## Link
- Spec đầy đủ: `docs/superpowers/specs/2026-08-01-supply-proposal-single-status-design.md`
- Plan: `.plans/supply-proposal-single-status/plan.md`
