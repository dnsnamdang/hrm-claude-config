# Design — HRM hiển thị link Mã phiếu yêu cầu duyệt hàng tạm → mở chi tiết bên ERP

## Mục tiêu
Sau khi bấm "Gửi duyệt hàng tạm" (đồng bộ sang ERP), banner trên tab Báo giá (dự án trúng thầu) hiển thị **Mã phiếu yêu cầu duyệt hàng tạm** dạng link; click mở trang chi tiết phiếu bên ERP (tab mới).

## Hiện trạng
- HRM `TmpProductSyncService::sendApproval()` gọi ERP `/api/v1/tmp-product-requests/sync-from-hrm`, nhận `$result` gồm `map`, **`request_id`**, **`request_code`**. Hiện chỉ dùng `map` (set `erp_tmp_product_id` từng dòng) + `tmp_sync_status='syncing'`; **CHƯA lưu request_id/code**.
- Banner build ở `QuotationController::buildTmpSyncSummary()` → trả `quotation_id/code`, `status`, `unsent`, `sent_total`, `approved`.
- FE `ProspectiveProjectQuotationsTab.vue`: banner dùng `tmpSync.*`. Pattern deep-link ERP đã có: `erp_contract_url` build ở BE (line 472) bằng `config('app.erp_url', env('ERP_URL'))`; Vue chỉ dùng `:href` (line 51).
- Bảng: `quotations` (Module Assign). `config('app.erp_url')` = `env('ERP_URL', 'http://127.0.0.1:8001')`.
- URL ERP chi tiết phiếu: `{erpBase}/admin/sale/tmp_product_requests/{request_id}/show`.

## Thiết kế
### DB (migration, bảng `quotations`)
- `erp_tmp_product_request_id` — unsignedBigInteger nullable
- `erp_tmp_product_request_code` — string nullable

### BE
1. `TmpProductSyncService::sendApproval()` — trong transaction hiện có, lưu:
   `$quotation->erp_tmp_product_request_id = $result['request_id'] ?? null;`
   `$quotation->erp_tmp_product_request_code = $result['request_code'] ?? null;`
2. `QuotationController::buildTmpSyncSummary()` — thêm vào mảng trả về:
   - `request_id` = `$won->erp_tmp_product_request_id`
   - `request_code` = `$won->erp_tmp_product_request_code`
   - `request_url` = khi có id → `rtrim(config('app.erp_url', env('ERP_URL','')),'/') . '/admin/sale/tmp_product_requests/'.$won->erp_tmp_product_request_id.'/show'`; ngược lại `null`
   (dùng đúng pattern `$erpBase` như `erp_contract_url`)

### FE (`ProspectiveProjectQuotationsTab.vue`, banner)
Khi `tmpSync.request_code` có giá trị → hiển thị dòng:
`Mã phiếu: <a :href="tmpSync.request_url" target="_blank" rel="noopener">{{ tmpSync.request_code }}</a>`
(đặt trong banner "Đồng bộ hàng tạm sang ERP", cạnh badge trạng thái)

## Quyết định
- Lưu id+code trên `quotations` (giống `erp_firm_contract_id`) — để link sống sau reload + trỏ đúng phiếu (ERP không có API tra phiếu theo hrm_quotation_id).
- Tái dùng `config('app.erp_url')` — không thêm config mới.

## Edge cases
- ERP không trả `request_id` (bản ERP cũ) → cột null, banner không hiện link (chỉ hiện text như cũ). Không lỗi.
- Gửi duyệt lại (nếu có) → ghi đè id/code mới nhất.

## Không làm
- Không đụng luồng `pullStatus`, không đổi ERP (ERP đã trả sẵn request_id/code).

## Branch
`sync_quotation` (hrm-api + hrm-client — cả 2 đang ở nhánh này).
