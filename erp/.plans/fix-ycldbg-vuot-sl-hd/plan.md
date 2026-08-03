# Plan — Fix ycldbg vượt SL hợp đồng

Nhánh đề xuất: `fix-ycldbg-vuot-sl-hd` (tách từ nhánh đang chạy).
Phụ trách: @namdang

## Phase 5 — Fix follow-up: ycldbg in-flight giao thiếu vẫn cho đẻ ycldbg mới — XONG (sửa thẳng master)

Bug user báo: ycldbg #1 (SL 3) → PGV giao SL 2 (chưa nhập KQ) → vẫn tạo được ycldbg mới SL 1. Đúng phải: phần thiếu (1) làm bằng PGV#2 của chính ycldbg #1, KHÔNG đẻ ycldbg mới → available phải = 0.

Root cause: nhánh "in-flight" của `getInstallableAvailableQty` cộng `assign_task_qty` (SL đã đưa vào PGV = 2) thay vì `reqQty` (3) → nhả nhầm 1.

- [x] Đổi mô hình tiêu thụ mỗi ycldbg sang `used += max(0, reqQty − released)`, `released = (SL đã nhập KQ stage>=4) − (SL đạt 100%)`. Bỏ nhánh in-flight/pending/dropped + `$pendingStatuses`. (`FirmContract::getInstallableAvailableQty`)
- [x] `php -l` sạch
- [x] Verify dev_erp_2: cross-check helper khớp công thức tay (cid=202/pid=39071 → −2); ca reported ycldbg(3)+PGV(2) → available=0
- [ ] User test browser lại đúng kịch bản (ycldbg 3 → PGV 2 → KHÔNG tạo được ycldbg mới; PGV#2 SL1 vẫn được) + ca <100% vẫn cho làm lại
- [ ] Commit master khi user duyệt

## Phase 0 — Chuẩn bị & xác minh phạm vi (read-only) — XONG

- [~] (Bỏ — theo yêu cầu) Quét DB toàn bộ HĐ/mã lỗi tương tự
- [x] Chốt unit_id: KHÔNG lọc unit (per product). Chốt bộ lọc exported: GIỮ `need_repair=1 OR created_at<2025-11-16`, áp cả 2 cổng
- [x] Chốt phân biệt đã-nhập-KQ vs đang-chờ: `current_stage >= IMPORT_RESULT(4)` + `assign_task_qty > 0`
- [x] Verify công thức mới trên ca gốc 9816/32799 → available = 0 (chặn đúng). Xem design.md "QUYẾT ĐỊNH CUỐI"

## Phase 1 — Helper dùng chung (nguồn chân lý) — XONG

- [x] Viết `FirmContract::getInstallableAvailableQty($firmContractId, $productId, $exclYcldbgId)` (static, model `FirmContract`)
  - [x] `exported` = SUM(warehouse_exported_qty) per product, lọc `need_repair=1 OR created_at<2025-11-16`
  - [x] `used` theo "consumption per ycldbg": đã nhập KQ→delivered(can_request_qty); in-flight→assign_task_qty; chờ giao việc (status 1/3/6)→reqQty; đã giao việc nhưng bỏ mã→0
  - [x] Chỉ progress thật `assign_task_qty>0` (loại dòng "ma" — D1); luôn giữ ycldbg chờ (D2)
- [x] Bỏ `exists()`/`hasAssignTaskProgress`

## Phase 2 — Đấu nối 2 cổng vào helper — XONG

- [x] `AssemblyRequestStoreRequest::getAvailableQty()` ủy quyền helper; xóa 5 private method chết; thêm import `FirmContract`
- [x] `FirmContractController@getDataForFirmContractAssemblyProduct()` gọi helper + guard `$seenProductIds` tránh trùng mã (giữ shape response cho blade)
- [x] Import `AssignTaskProgress` + `DB` vào model `FirmContract`

## Phase 3 — Test & verify — XONG (trên prod erp_new, read-only)

- [x] `php -l` 3 file → sạch
- [x] Verify tinker:
  - [x] (1) chưa có ycldbg (cid4/7714) → available = exported(3) ✓
  - [x] (2) đã giao 100% (9816/32799) → available = 0 ✓
  - [x] (3) đã giao <100% (ycldbg 1111 giao 0%) → tiêu thụ 0 (nhả) ✓
  - [x] (4) nhiều ycldbg trộn (9816/32799) → tổng = 1, không vượt ✓
  - [x] (5) ycldbg đang chờ giao việc (cid232/19545) → giữ trọn quỹ = 0 ✓; excl self → 1 ✓
- [x] Tái hiện ca gốc: HĐ 9816 + mã 32799 → available = 0 ✓
- [ ] User test browser luồng tạo ycldbg (chưa làm)

## Phase 4 — (defer) Vá dữ liệu cũ

- [ ] (CHƯA LÀM — theo yêu cầu để nguyên) Xác định + xử lý ycldbg 1111 / PGV 11082 thừa khi có quyết định

---

### Checkpoint — 2026-06-26 (code xong)
Vừa hoàn thành: Code Phase 1–3. Helper `FirmContract::getInstallableAvailableQty` + đấu nối 2 cổng (`FirmContractController@getDataForFirmContractAssemblyProduct`, `AssemblyRequestStoreRequest::getAvailableQty`). `php -l` sạch 3 file. Verify tinker 5 ca trên prod (read-only) đều đúng: ca gốc 9816/32799 = 0, ca chưa-có-ycldbg = exported, ca đang-chờ-giao-việc giữ trọn quỹ, update-self nhả lại.
File sửa: `app/Model/Sale/Firm/Contract/FirmContract.php` (+import AssignTaskProgress, DB; +helper), `app/Http/Controllers/Sale/Firm/FirmContractController.php` (loop dùng helper + guard trùng mã), `app/Http/Requests/AssemblyRequestStoreRequest.php` (getAvailableQty ủy quyền, xóa 5 private chết, +import FirmContract).
Đang làm dở: chưa commit.
Bước tiếp theo: User test browser luồng tạo/sửa ycldbg (đặc biệt mã đã giao 100% phải biến mất khỏi form + chặn khi cố lưu). Sau đó cân nhắc Phase 4 (vá data ycldbg 1111/PGV 11082 thừa).
Blocked: (trống)
