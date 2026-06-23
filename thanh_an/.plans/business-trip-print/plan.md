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

## Phase 3 — Bổ sung tỉnh/thành công ty trước ngày (2026-06-18)
- [x] Modal `BusinessTripDecisionPrintModal.vue`: thêm `companyProvince`, fetch `human/company/{id}` lấy `province.text`, hàm `cleanProvinceName` cắt tiền tố "Thành phố/TP/Tỉnh"; ghép vào `approvedDateText` (giữ nguyên logic ngày)
- [x] Page `_id/print.vue` (dead): cập nhật tương tự cho đồng bộ
- [ ] Verify UI: mở popup In → đầu QĐ hiển thị "<Tỉnh>, ngày DD tháng MM năm YYYY" (chờ user chạy)

---

### Checkpoint — 2026-06-18
Vừa hoàn thành: Thêm tỉnh/thành công ty vào trước phần ngày ở bản in QĐ cử đi công tác (modal + page). Nguồn: `human/company/{id}` → `province.text` (DB đã lưu tên sạch); có hàm cắt tiền tố phòng hờ. Giữ nguyên logic ngày = ngày duyệt phiếu.
Đang làm dở: không
Bước tiếp theo: User mở popup In verify tỉnh/thành hiển thị đúng
Blocked:

### Checkpoint — 2026-06-16 (bổ sung)
Vừa hoàn thành:
- "Đi công tác tại" đổi sang lấy `description` (Nội dung công việc)
- Ngày trên đầu QĐ = NGÀY DUYỆT PHIẾU (không phải duyệt kết quả):
  - BE: migration thêm cột `approved_at` (backfill = `created_at` cho phiếu status ∈ 2,5,6,7); set `approved_at = now()` khi duyệt phiếu (`storeApprove`, nhánh `approve`); thêm fillable; expose `approved_at` ở DetailResource
  - FE: modal computed `approvedDateText` → `……, ngày DD tháng MM năm YYYY`
Đang làm dở: không
Bước tiếp theo: CHẠY MIGRATION `php artisan migrate`; rồi verify popup (ngày = ngày duyệt phiếu)
Blocked:
