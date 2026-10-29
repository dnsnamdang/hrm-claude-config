# Plan — Hàng bán thêm vẫn hiện lại ở phiếu giao việc nốt

## Tasks
- [x] T1: `WrServiceContractMerchandise::getAssigningMerchandiseQty()` — cộng `delivery_qty`
  thay vì `assign_task_qty` (dòng 104).
- [x] T2: `WrServiceContract::getForAssignTask()` loop merchandise (~2722-2731) — pre-fill
  `qty = available_qty > 0 ? available_qty : 0`.
- [x] T3: `WrServiceContract::getForAssignTask()` — lọc bỏ merchandise `available_qty <= 0`,
  gán `$result['merchandises']` (~2875).
- [x] T4: `php -l` 2 file — sạch.
- [x] T5: verify tinker trên erp_new:
  - HĐ 7854 SP 17684: assigning=7 (delivery), available=0 → ẩn đúng (trước fix hiện với qty=7).
  - HĐ 7814 SP 14260: chưa giao, available=12 → vẫn hiện (không ẩn nhầm).
  - 924 dòng merchandise: 756 còn hiện, 168 ẩn (đã giao đủ).

### Checkpoint — 2026-10-05
Vừa hoàn thành: 3 sửa đổi code + php -l + verify tinker. Fix hoạt động đúng.
Đang làm dở: (không)
Bước tiếp theo: user review/test trình duyệt; nếu OK thì yêu cầu commit (chưa commit).
Blocked: (không)

## Ghi chú
- NGOÀI phạm vi: validate duyệt KQ (Q2 bỏ), `->save()` thiếu ở WrApproveResultsController.
- Không commit/push khi chưa có yêu cầu. Không vá dữ liệu.
