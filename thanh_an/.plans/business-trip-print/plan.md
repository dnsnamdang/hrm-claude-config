# Plan tổng quát — In QUYẾT ĐỊNH cử đi công tác (Business Trip)

**Người phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-06-16-business-trip-print-design.md`
**Plan chi tiết:** `docs/superpowers/plans/2026-06-16-business-trip-print.md`

## Phase 1 — Backend
- [x] Thêm `employee_account_id` vào `BusinessTripEmployeeResource.php`
- [ ] Verify API trả về field mới (chạy thật)

## Phase 2 — Frontend (popup — giống hệt jobassignment)
- [x] (Bản đầu) Sửa trang `_id/print.vue` sang layout QUYẾT ĐỊNH — *nay không dùng nữa, list không trỏ tới*
- [x] Tạo modal `components/modal/BusinessTripDecisionPrintModal.vue` (mirror `JobAssignmentDecisionPrintModal.vue`, map dữ liệu business_trip)
- [x] `index.vue`: nút In mở `$refs.printModal.open(item.id)` thay link `:to`; thêm import + đăng ký + đặt `<BusinessTripDecisionPrintModal ref="printModal" />`
- [ ] Verify UI (popup preview + nút In mở cửa sổ in, font Times New Roman) — chờ user chạy

---

### Checkpoint — 2026-06-16
Vừa hoàn thành: Chuyển sang popup giống hệt jobassignment — modal preview + handlePrint mở cửa sổ in, font/format y hệt
Đang làm dở: không
Bước tiếp theo: User chạy thật verify popup (có NV / không NV / nút In). Cân nhắc xóa page `_id/print.vue` cũ nếu không cần URL trực tiếp.
Blocked:
