# Đề nghị xuất hóa đơn (export_bill_requests) — design

## Scope
Loạt feedback/fix cho màn **Đề nghị xuất hóa đơn** (module IncomeExpenditure, ERP TanPhatDev) —
màn đã tồn tại và đang được nhiều người cùng phát triển trên branch `de_nghi_xuat_hoa_don`.
Session này gom các yêu cầu tinh chỉnh + sửa bug của user, KHÔNG dựng lại màn từ đầu.

- Branch: `de_nghi_xuat_hoa_don` (git worktree `ERP/.worktrees/de_nghi_xuat_hoa_don`).
- Màn: Danh sách + form Tạo/Sửa/Xem + popup Chọn hợp đồng.
- Server dev: `php artisan serve` tại `http://127.0.0.1:8010`. DB local: `erp_hrm_check`
  (127.0.0.1:3306, root, không mật khẩu).

## Hiện trạng (2026-10-29)
Hoàn tất 13 task, Playwright-verified từng task, đã commit `81bb041094` + push
(`adaa92b9f7..81bb041094`). Chi tiết từng task + cách verify: xem `plan.md`.

## Các quyết định chung (chốt với user)
1. **File đính kèm giữ giới hạn 10MB/file** (không nới). "Không báo lỗi khi >30MB" là do UI
   không hiện lỗi quá cỡ, không phải thiếu giới hạn → fix ở FE (chặn khi chọn + hiện text lỗi
   theo từng file) + BE (message tiếng Việt cho `.max/.mimes/.file`).
2. **Xóa file đính kèm:** (a) áp dụng khi **Lưu**; (b) **bắt buộc còn ≥1 file**; (c) **KHÔNG**
   xóa file vật lý trên S3 — chỉ gỡ khỏi phiếu (gửi `old_attachments` = danh sách giữ lại).
3. **Popup Chọn hợp đồng giữ chọn 1 HĐ** (bỏ checkbox từng dòng — user "không cần tick").
4. **Lý do Không duyệt** lưu vào cột `comment` (migration thêm cột TEXT nullable), hiển thị lại
   trên màn chi tiết bằng **1 card "Ghi chú duyệt" chỉ-đọc** (`ng-if="form.comment"`) — bám
   sibling `AdditionAccountingRequest`, KHÔNG dựng bảng lịch sử duyệt nhiều dòng (module Thu chi
   không có convention đó).

## Nguyên tắc kỹ thuật đã áp
- **Bám sibling cùng module IncomeExpenditure** làm chuẩn: `AdditionAccountingRequestController`
  (reject có lý do + card ghi chú), `BillIncomeRequest`/`BillAdjustDeptRequest` (delete dùng
  `redirect()->back()` để giữ URL list).
- **Hàm dùng chung sửa có xác nhận user + scope hẹp:** sort popup chọn HĐ sửa
  `SearchContractService::searchAllContract` + `SearchController@searchAllContract` nhưng
  type-gated CHỈ nhánh `export_bill_request` (màn khác không ảnh hưởng). Các thay đổi còn lại
  đều khu trú trong controller/view của chính màn này (vd `data-text` nút xóa, `redirect()->back()`).
- **ExportBillRequest JS class** `extends BaseClass`: form fields tự gán lên instance trừ
  `no_set = ['handover_date','summary']` → `form.comment` tự có từ `@json($data)`.
- Cột thật trên `firm_contracts` là `contact_address` (KHÔNG có `contract_address`) — bug auto-fill
  địa chỉ do FE đọc nhầm tên cột.

## Lưu ý môi trường
- Bảng `notifications` DB local (gop_db) có schema Laravel chuẩn, THIẾU cột ERP custom
  (`url`, `receiver_id`, `content`, `status`, `created_by`) → `NotificationHelper::sendNotify`
  ném 500 ở local khi reject/approve. Đây là lệch schema môi trường local, **không phải bug code**;
  prod/test có đủ cột. Logic reject vẫn chạy + persist xong trước khi sendNotify ném (không bọc
  transaction) nên DB vẫn ghi đúng.
- Migration chạy local: cột `comment` + ~10 migration cột bill (firm_contract_tab_products,
  firm_contract_costs, wr_service_contract_*…) để endpoint hết 500.
