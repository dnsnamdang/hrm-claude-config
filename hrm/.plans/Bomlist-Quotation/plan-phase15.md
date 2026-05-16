# Plan Phase 15 — Xoá báo giá

> **Ngày bắt đầu:** 2026-04-23
> **Người phụ trách:** @dnsnamdang
> **Branch:** `tpe-develop-assign`

**Goal:** Cho phép người tạo xoá báo giá khi status = "Đang tạo" (1). Revert pricing_request về `CHO_XD_GIA` (2) nếu không còn báo giá khác.

**Scope chốt với user (2026-04-23):**
- Điều kiện: `status === STATUS_DANG_TAO` + `creator_id === current_user`.
- Cascade: xoá `quotation_product_prices` + `quotation_histories`.
- Downstream: `pricing_request` → revert về `STATUS_CHO_XD_GIA` nếu không còn báo giá nào khác link vào.
- Button: màn Danh sách báo giá (`/assign/quotations`) + màn xem chi tiết (`/assign/quotations/:id`).

## BE
- [x] 1. `QuotationService::destroy(Quotation $q)`: ensureEditableByCreator + transaction xoá prices/histories/quotation; revert pricing_request → STATUS_CHO_XD_GIA nếu không còn quotation khác.
- [x] 2. `QuotationController::destroy($id)`.
- [x] 3. Route `DELETE /assign/quotations/{id}`.
- [x] 3b. `QuotationResource` expose `creator_id` để FE check quyền xoá ở list.

## FE
- [x] 4. `quotations/index.vue`: nút Xoá (ri-delete-bin-line text-danger) khi `item.status===1 && item.creator_id===currentUserId`. `$bvModal.msgBoxConfirm` + reload list.
- [x] 5. `quotations/_id/index.vue`: V2BaseButton danger "Xoá" khi `canEditByCreator`. Confirm + redirect về list.

## Test thủ công
- [ ] 6. Tạo báo giá mới → trang list hiện nút Xoá → click → confirm → biến mất; pricing_request revert về "Chờ xây dựng giá".
- [ ] 7. Báo giá status ≠ 1 → không có nút Xoá.
- [ ] 8. User khác creator → không có nút Xoá (và BE reject nếu call trực tiếp).
- [ ] 9. Xoá tại trang chi tiết → redirect về list; toast success.

## Checkpoint — 2026-04-23 (Khởi tạo)
Vừa hoàn thành: Nhận scope + confirm 3 điều kiện với user.
Bước tiếp theo: Implement task 1-5.
Blocked: Không.

## Checkpoint — 2026-04-23 (Code DONE)
Vừa hoàn thành: BE destroy service + controller + route; expose creator_id; FE nút Xoá ở list + detail + confirm modal.
Bước tiếp theo: User test task 6-9.
Blocked: Không.
