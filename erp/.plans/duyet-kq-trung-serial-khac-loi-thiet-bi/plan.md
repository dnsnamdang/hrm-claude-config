# Plan — Duyệt KQ: cho phép trùng serial khi khác lỗi thiết bị

## Phase 1 — Fix validate bước DUYỆT (WrApproveResultsStoreRequest)
- [x] Điều tra nguyên nhân gốc, xác minh trên prod erp_new (contract 7744, serial 017559, device_error 671/672)
- [x] Xác nhận payload FE có `device_error_id`; đường lưu controller đã gom theo device_error_id
- [x] Thêm scope `device_error_id` vào query completion-check nhánh **sửa chữa** (product_repairs) — dòng ~274
- [x] Thêm scope `device_error_id` vào query completion-check nhánh **bảo hành** (product_warrantys) — dòng ~350
- [x] Kiểm tra lint/cú pháp PHP (php -l) — No syntax errors

### Checkpoint — 2026-09-22
Vừa hoàn thành: Fix validate bước DUYỆT thêm chiều `device_error_id` (nhánh sửa chữa + bảo hành), php -l OK, giữ LF. Đã phân tích rủi ro regression (unique index / trait checkValidateSerial / đường lưu / when-empty) — an toàn. Đã commit `bf80285476` + push `master`.
Đang làm dở: (không) — chờ user xác nhận test lại trên UI phiếu 8285 sau deploy.
Bước tiếp theo: User duyệt lại phiếu KQ 8285; nếu muốn đồng bộ bước NHẬP KQ thì chốt riêng.
Blocked:

## Ngoài phạm vi (chờ user chốt nếu cần)
- [ ] Đồng bộ tương tự cho bước NHẬP KQ (`WrImportResultRequest` / `WrImportResultAppRequest`) — hiện
      nhánh sửa chữa đã bị vô hiệu, nhánh bảo hành lọc product-only.
