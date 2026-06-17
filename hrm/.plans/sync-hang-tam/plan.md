# Plan — Đồng bộ hàng tạm trong báo giá HRM → ERP

> Design: `.plans/sync-hang-tam/design.md` · Spec: `docs/superpowers/specs/2026-06-06-sync-hang-tam-design.md`

_(Phase 1–4 ban đầu: xem checkpoint trong STATUS.md — đã commit branch sync_quotation.)_

---

## Phase 5 — Hàng tạm "Đang tạo" trước khi gửi duyệt (ERP-only)

> Spec: `docs/superpowers/specs/2026-06-08-tmp-product-draft-status-design.md`
> Plan chi tiết: `docs/superpowers/plans/2026-06-08-tmp-product-draft-status.md`

- [x] Task 1: const `STATUS_DRAFT=3` trong `TmpProduct`
- [x] Task 2: `TmpProductRequestSyncService::createFromHrm` → status=3 + bỏ notify
- [x] Task 3: `TmpProductRequest` STATUSES "Đang tạo" + getStatusAttribute + nhãn in
- [x] Task 4: route + `TmpProductsController::updateDraft` (Lưu / Lưu và gửi duyệt)
- [x] Task 5: nhãn status=3 + nút Sửa ở list `tmp_products`
- [x] Task 6: nhãn status=3 ở `my_tmp_products`
- [x] Task 7: form edit — 2 nút Lưu / Lưu và gửi duyệt + JS `saveDraft`
- [x] Task 8: filter status "Đang tạo" trên list
- [x] Task 8b: `TmpProduct::searchByFilter` — thêm `orWhere('created_by', current)` để người tạo luôn thấy hàng nháp của mình (đã xác nhận sửa hàm dùng chung)
- [x] Task 8c: gộp "Gửi duyệt lại" vào `updateDraft` — guard nhận status {0,3}; reset comment/approver khi gửi lại từ status=0; notify permission holders (A); nút "Gửi duyệt lại" gọi `saveDraft(1)`; xóa `resubmit()` + route + JS. Spec §10.
- [ ] Task 9: verify E2E thủ công (dev_erp_2) — gồm cả gửi duyệt lại hàng bị từ chối (lưu field + validate)
