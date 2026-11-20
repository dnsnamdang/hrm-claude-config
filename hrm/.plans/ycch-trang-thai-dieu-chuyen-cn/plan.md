# YCCH (Phiếu YC chuyển hàng) trạng thái theo ĐNXK/PXK — điều chuyển kho chi nhánh (type 7)

Nguồn: QA 20/11/2026 — YCXH 47731 "Đã đề nghị" mà YCCH 8635 "Đang đề nghị". Kết luận: đúng ERP
(YCCH không có trạng thái "Đã đề nghị"; ĐNXK 42182 chưa duyệt). Phát hiện HRM lệch ERP ở 2 bước sau.

ERP: duyệt YCXH → YCCH 4 · duyệt ĐNXK (WarehouseExportRequest::approve:1146) → 5 · duyệt PXK
(WarehouseExport::approve:1312) → 6 · hoàn tất PXH (ProductExport:1950) → 7.

- [x] `ProductExportRequest::syncBranchTransferRequestStatus(int)` — chỉ type 7
- [x] `WarehouseExportService::approveExportRequest` → YCCH 5
- [x] `ProductExportService::createFromWarehouseExport` cascade (port WarehouseExport::approve) → YCCH 6 (trước finalize → 7)
- [x] Test `Modules/Assign/Tests/Feature/Type7BranchTransferStatusSyncTest.php` (RED→GREEN); suite Type7/WarehouseExport/Pxk xanh
- [x] Push: develop 5205e0758, gop_db 24e2d357e (local develop b6f5e37ec)

### Checkpoint — 2026-11-20
Vừa hoàn thành: đã push develop + gop_db.
Bước tiếp theo: QA kiểm lại YCCH khi duyệt ĐNXK.

## Đợt 2 — thêm trạng thái 14 "Đã đề nghị" (QA 20/11 chiều, user chốt)
- [x] YCCH thêm status 14 "Đã đề nghị": gửi ĐNXK (YCXH→1) ⇒ YCCH 14; ĐNXK về nháp / thủ kho trả lại / huỷ ⇒ lùi 4; duyệt ĐNXK ⇒ 5; duyệt PXK ⇒ 6
- [x] HRM: test 4 ca (gửi→14, nháp giữ 4 rồi gửi→14, huỷ→4, nhãn 14), suite type 7 + ĐNXK 29 test xanh — commit `ccda9676b` nhánh `fix/ycch-da-de-nghi` (worktree tách origin/develop), CHƯA push
- [x] ERP develop_02: nhãn 14, `send()`, `cancel()`, 2 chỗ trả ĐNXK về nháp/trả lại → YCCH 4 — commit `a5b327111d`, ĐÃ lên origin/develop_02 (đi cùng đợt push YC đặt hàng cuối ngày; không có test tự động; tinker trên hrm_erp_test phiếu 8232 lên 14 rồi rollback)
- [ ] Push HRM develop (ccda9676b) + cherry-pick gop_db 2 repo — chờ user (ERP develop_02 đã lên)
- [ ] Dữ liệu cũ lệch (YCXH đã đề nghị mà YCCH vẫn 4): 18 phiếu hrm_erp_test (gồm 8232), 13 phiếu hrm_erp_gop — chờ user quyết có update 4→14 không

### Checkpoint — 2026-11-20 17:20 (wrap up tự động)
Vừa hoàn thành: đợt 2 trạng thái 14 "Đã đề nghị" code xong cả HRM + ERP (hrm-client không cần sửa, đọc STATUSES từ API).
Đang dở: HRM `ccda9676b` (nhánh fix/ycch-da-de-nghi) CHƯA push; ERP `a5b327111d` đã có trên origin/develop_02 → ERP develop_02 đã có trạng thái 14 trong khi HRM develop chưa.
Bước tiếp theo: user quyết (1) push HRM develop + gop_db 2 repo; (2) có update dữ liệu YCCH lệch lên 14 không, DB nào.
Blocked: chờ user.
