# Fix — Note phiếu yêu cầu duyệt hàng tạm lưu thẻ HTML (do sync HRM)

## Nguyên nhân (đã truy)
HRM: field `note` báo giá nhập bằng CKEditor → HTML. Sync gửi `$quotation->note` nguyên HTML (`TmpProductSyncService:52`). ERP `TmpProductRequestSyncService:105` lưu thẳng `$request->note = $data['note']` (không strip). Tính năng cập nhật ghi chú ERP KHÔNG phải nguyên nhân (input text thuần).

## Fix (user chốt: strip_tags khi sync)
- [x] `TmpProductRequestSyncService.php` ~dòng 105: chuẩn hoá note về text thuần — tách đoạn `<br>`/`</p>` thành khoảng trắng, `strip_tags`, `html_entity_decode`, gộp khoảng trắng, trim; rỗng → null.
- [ ] User test: sync 1 báo giá có note HTML → note ERP ra text thuần.

## File
- `app/Services/Sale/TmpProductRequestSyncService.php`
