# #12017 — Nhập điều chuyển kho chi nhánh: tự giữ hàng cho KD, bỏ phiếu phân bổ

Redmine: http://quanly.dnsmedia.vn/issues/12017 — sửa cả ERP (gop_db + develop_02) và HRM (develop).

## Hiện trạng
- FE YCXH điều chuyển CN đã chặn "1 YCXH = 1 người yêu cầu" (đã làm trước đây).
- Duyệt PNH loại 7 (không nhập thẳng) → YCCH status 11, rồi KT CN phải lập phiếu phân bổ
  (TransferProductAllocation) mới ghi giữ hàng → còn sót bước này.

## Quyết định
- Lúc duyệt PNH loại 7 (`!is_import_direct`): với từng dòng PNH (product + đơn vị của lô) chia SL
  cho các dòng khách của YCCH theo thứ tự id, mỗi dòng tối đa `qty − allocated_qty`.
- Ghi giữ: NV = người lập YCCH, KH = khách dòng YCCH, công ty = công ty của PNH,
  hạn = ngày duyệt + `configs.max_prepick_date` của công ty PNH. SL giữ = SL × hệ số lô.
- Nguồn giữ (log) = dòng PNH (`ProductImportDetail`) → báo cáo/lịch sử giữ hiện phiếu nhập.
- Cộng allocated_qty ở YCCH, YCCH → status 12 (như duyệt phân bổ cũ), báo chuông người lập YCCH.
- SL nhập dư so với YCCH = tồn tự do.
- Bỏ luồng phân bổ: `canCreateTransferProductAllocation()` luôn false (ẩn nút), ERP bỏ redirect
  "Hãy phân bổ hàng". Màn phân bổ cũ giữ để xem lịch sử.

## Tasks
- [x] T1 Tự giữ trong `ProductImport::updateWarehouse()` nhánh loại 7
- [x] T2 Bỏ nút/redirect tạo phân bổ
- [x] T3 (HRM) PrepickDocumentResolver thêm `ProductImportDetail` → Phiếu nhập kho
- [x] T4 Test

### Checkpoint — 2026-11-10
Vừa hoàn thành: T1–T4 cả ERP (worktree TanPhatDev-12017) và HRM (worktree hrm-api-12017).
Kiểm: ERP chạy tự giữ trên PNH 12298 (rollback) đúng; HRM Type7BranchTransferAllocationTest 6/6 + Type7BranchTransferImportTest 4/4. PrepickTrackingApi/Scope fail 3 test có sẵn từ trước (code gốc cũng fail).
Bước tiếp theo: chờ user cho commit/push (ERP → gop_db + develop_02, HRM → develop).
Blocked:
