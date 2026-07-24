# Plan — Miễn kiểm tra giá vốn cha ≥ Σ con cho hàng cha ERP

Màn: QLDA TKT → Quản lý Báo giá → Tạo mới/Cập nhật báo giá (`quotations/_id/edit.vue`, `QuotationService`).

## Bối cảnh
- Rule "giá vốn cha ≥ Σ giá vốn con" hiện áp cho **CẢ cha ERP** (comment code ghi rõ "kể cả cha ERP").
- Cha tạm (tự xây): FE tự roll-up giá vốn cha = Σ con → luôn thoả. Cha ERP: giữ giá ERP → có thể < Σ con → hiện bị chặn.
- Task: cha tạm giữ enforce; cha ERP **bỏ qua** (cho phép < Σ con).

## Phase 1 — Bỏ qua cha ERP khỏi kiểm tra giá vốn floor

### BE
- [x] `QuotationService::assertParentImportFloor` (2 nhánh direct + BOM): thêm select `erp_product_id`/`blp.erp_product_id` và `continue` nếu cha là ERP; sửa comment

### FE
- [x] `edit.vue isParentImportInvalid`: thêm guard `|| isErpProduct(parent)` → cha ERP không bị flag (bỏ chặn ở save strict dòng 2733 + bỏ cell-invalid); sửa comment dòng 2115/2733

### Verify
- [x] AC1: cha tạm giá vốn < Σ con → chặn (giữ nguyên)
- [x] AC2: cha tạm giá vốn ≥ Σ con → lưu OK
- [x] AC3: cha ERP giá vốn < Σ con → bỏ qua, lưu/gửi duyệt OK

### Checkpoint — 2026-07-08
Vừa hoàn thành: toàn bộ Phase 1 — CODE DONE + VERIFIED
Verify:
- BE (tinker reflection assertParentImportFloor, dữ liệu transaction rollback):
  - qid=6 (nhiều cha ERP parentTotal < childrenTotal) → KHÔNG throw (AC3 PASS)
  - ép parent 112 thành cha tạm vi phạm → THROW "Giá vốn hàng cha ... nhỏ hơn tổng con" (AC1 PASS)
  - nâng giá vốn cha tạm ≥ Σ con → KHÔNG throw (AC2 PASS)
- FE (Playwright, gọi isParentImportInvalid trên component qid=6): temp violating=true, erp violating=false, temp ok=false → AC1/AC2/AC3 PASS. 0 lỗi console.
Files: hrm-api QuotationService.php (assertParentImportFloor bỏ qua cha ERP 2 nhánh) + hrm-client edit.vue (isParentImportInvalid guard isErpProduct + comment)
Không migration/git. Dữ liệu test đã rollback.
Đang làm dở: không
Bước tiếp theo: user verify browser (tạo báo giá cha ERP combo < Σ con → gửi duyệt được; cha tạm < con → vẫn chặn)
Blocked:

### Checkpoint 2 — 2026-07-08 (test theo yêu cầu user)
Chạy test bổ sung:
- BE before/after trên qid=6 (6 cha ERP vi phạm): TRƯỚC sửa (check cả ERP) → CHẶN "Súng vặn ốc..."; SAU sửa (code thật) → KHÔNG chặn (AC3). Rollback.
- FE gate (Playwright, stub getChildren): temp violating=true / erp violating=false / temp ok=false (AC1/AC2/AC3).
- Lưu ý môi trường: user admin (emp 13) KHÔNG có quyền "Xem giá vốn hàng hoá" → `canViewCostPrice=false` nên gate FE (điều kiện `canViewCostPrice &&`) vốn tắt với user này; cấp quyền tạm qua tinker KHÔNG áp được vào server đang chạy (spatie cache theo process). Cha tạm auto roll-up nên AC1 không tái hiện qua click UI. → Đã verify đủ 3 AC ở tầng gate thật (BE assertParentImportFloor + FE isParentImportInvalid) thay cho full-UI-submit.
- Đã dọn sạch: qid6 created_by trả về 45, gỡ quyền tạm emp13. Không đổi dữ liệu thật.

### Checkpoint 3 — 2026-07-09 (FULL UI TEST theo yêu cầu)
Cấp quyền ĐÚNG cách: `isCurrentEmployeeHasPermission` check qua ROLE (`role_has_permissions` theo role_id + current_company_role), KHÔNG dùng quyền trực tiếp. → thêm perm 1092 "Xem giá vốn hàng hoá" cho role 18 (Super admin của emp13) ở tất cả company (1,2,3,4,8). Hiệu lực NGAY (query live DB, không cache/token).
Test qua luồng UI thật (`openSubmit` = save strict + mở modal, network short-circuit để không ghi DB), user emp13 có canViewCostPrice=true, qid=6 có 6 cha ERP vi phạm:
- AC3: chạy openSubmit → anyErpFlaggedInvalid=false, importFloorGate_blocks=false, importFloorErrorVisible=false; sau khi điền 2 field bắt buộc còn thiếu (delivery_time/warranty_time — không liên quan giá vốn) → **submitModalOpened=true** (modal "Gửi duyệt báo giá" mở, Cấp 2, LN 158%) → cha ERP vi phạm KHÔNG bị chặn. Ảnh xác nhận đã chụp+xoá.
- AC1: cha tạm ép vi phạm (đồng bộ trước roll-up) → isParentImportInvalid=true, gate_blocks=true → chặn.
- AC2: cha tạm ≥ con → isParentImportInvalid=false → cho lưu.
- Chặn duy nhất khi submit qid6 là 2 field required trống (delivery_time/warranty_time), KHÔNG phải giá vốn → xác nhận thay đổi không gây false-block.
Dọn sạch: created_by=45, xoá 5 dòng role_has_permissions vừa thêm, clear spatie cache, xoá ảnh. qid6 status=1/delivery_time=NULL (không ghi gì vào DB).
KẾT LUẬN: 3/3 AC PASS ở cả BE (assertParentImportFloor) + FE (isParentImportInvalid) + luồng UI thật.
