# Duyệt KQ giao việc: cho phép trùng serial khi KHÁC lỗi thiết bị

## Bối cảnh / Sự cố
- HĐ dịch vụ: `HDDV_TPE_HN_KD3_26_0192_120` (wr_service_contracts.id = **7744**).
- Cùng 1 thiết bị `ETGN-EG-P0736FPC:02` (product_id = **40598**), cùng serial nhập `017559`, nhưng **2 lỗi thiết bị khác nhau**:
  - `device_error_id = 671` — "Tháo phòng sơn xe con..." → NKQ **8286** (assign_task 16844), đã duyệt, success 100%.
  - `device_error_id = 672` — "Lắp phòng sơn xe con..." → NKQ **8285** (assign_task 17016), success 100%.
- Khi **duyệt KQ** phiếu còn lại → bị chặn: *"Seri đã hoàn thành nhập kết quả, không được nhập tiếp!"*.

## Nguyên nhân gốc (đã xác minh trên prod erp_new)
Validate ở `WrApproveResultsStoreRequest` (bước DUYỆT) kiểm tra "serial đã hoàn thành" bằng query
`AssignTaskProgress` khớp theo **contract_id + product_id + serial + request_type + type + status**,
NHƯNG **thiếu chiều `device_error_id`**.

→ 2 công việc cùng contract/product/serial nhưng khác lỗi thiết bị bị coi là một. Phiếu "tháo" (671)
đã 100% → chặn nhầm phiếu "lắp" (672).

Bằng chứng đối chiếu:
- Code chạy ĐÚNG (`WrServiceContractProduct.php:163,188,211`) **luôn** có `->where('device_error_id', ...)`.
- Đường LƯU của chính controller (`WrApproveResultsController.php:508-527`, `WrImportResultsController`)
  cũng gom `assign_task_progress` theo `product_id` + `device_error_id`.
- Payload FE (`WrImportResultProduct.blade.php:307`, `WrImportResultProductApprove.blade.php:315`) đã
  gửi kèm `device_error_id` trong `product_repairs` / `product_warrantys`.

Chỉ riêng validate ở FormRequest bỏ sót chiều này.

## Hướng sửa (đúng ý user: "khác lỗi thiết bị thì vẫn cho trùng serial")
Thêm `->where('device_error_id', ...)` vào query completion-check của bước DUYỆT, chỉ khi dòng có
`device_error_id` (dùng `->when(!empty(...))` để không đổi hành vi với thiết bị không gắn lỗi).

Phạm vi sửa: `WrApproveResultsStoreRequest.php`
- Nhánh sửa chữa (product_repairs), query ~dòng 274.
- Nhánh bảo hành (product_warrantys), query ~dòng 350.

## KHÔNG đụng
- Bước NHẬP KQ (`WrImportResultRequest.php`): nhánh sửa chữa đã **bị vô hiệu** (block comment 628-640),
  nhánh bảo hành lọc theo product-only và **không** lọc serial → khác thiết kế, không phải nguyên nhân
  sự cố này. Không sửa để tránh regression (nếu cần đồng bộ sẽ chốt riêng với user).
- Nhánh lắp đặt hãng (`assembly`/`firm`/LAP_DAT) — luồng khác, không liên quan.
- **KHÔNG sửa dữ liệu prod** — dữ liệu hiện tại đúng, đây là lỗi logic validate.

## Kiểm thử
- Duyệt lại phiếu KQ 8285 (device_error 672) trên HĐ 7744 → không còn báo "Seri đã hoàn thành...".
- Thiết bị 1 lỗi, trùng serial thật (cùng device_error_id) → vẫn chặn như cũ.
