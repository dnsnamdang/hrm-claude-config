# Sửa tỷ lệ đề xuất %DS cho phòng hỗ trợ — màn Hỗ trợ hạch toán HĐ phối hợp

## Bối cảnh / sự cố
Màn duyệt **Hỗ trợ hạch toán** của HĐ hãng phối hợp thực hiện (nhiều phòng, không phân chia thị trường),
ví dụ `/admin/sale/firm-contracts/28755/support-accounting`:
- "Tỷ lệ đề xuất %DS" = field `commission_sale_percent` (dòng "Doanh số tính thưởng năng suất được ghi nhận").
- Hiện **chỉ sửa được %DS của phòng tạo HĐ (phòng chính, `is_main=true`)**.
- Phòng hỗ trợ (`is_main=false`) chỉ hiển thị text read-only → không nhập được.
- Auto-chia hiện tại: sửa phòng chính → `(100 − main) / n` chia **đều** cho mọi phòng hỗ trợ.
- **Không** có ràng buộc tổng %DS các phòng = 100%.

## Gốc rễ
Không phải `ng-disabled`/so sánh `department_id`. Nguyên nhân duy nhất: `departments-support.blade.php`
render `commission_sale_percent` dạng text, **không có `<input>`**. BE đã nhận & lưu
`departments_support.*.commission_sale_percent` (request dòng 54, cột DB
`firm_support_accounting_departments.commission_sale_percent`) — chỉ thiếu ô nhập FE.

## Yêu cầu (user chốt — hướng A)
1. Sửa được %DS của nhiều phòng; **phòng hỗ trợ CUỐI** = ô auto-tính phần còn lại (khoá).
   → HĐ 1 chính + 2 hỗ trợ: sửa chính + hỗ trợ[0] (2 phòng), hỗ trợ[1] tự tính.
2. Cho phòng hỗ trợ (trừ phòng cuối) sửa tỷ lệ đề xuất.
3. Validate tổng %DS tất cả phòng = 100% (cả FE chặn submit + BE defense-in-depth).

## Phạm vi
- **Chỉ FE + 1 validate BE.** KHÔNG đổi DB, KHÔNG đổi service `calculate()`/`getAccountingInfo()`.
- KHÔNG gắn `commission_sale_percent` vào `getKeysChanged` (không ép "chuyển duyệt" khi đổi %DS) —
  thuộc feature `fix-keychanged-support-accounting-chuyen-duyet`, tránh lẫn scope.

## Thiết kế chi tiết
### FE1 — `resources/views/sale/firm/accounting/departments-support.blade.php` (~dòng 9)
Ô `commission_sale_percent` của phòng hỗ trợ tách 2 trường hợp:
- `isPreview || $last` → text read-only (như cũ).
- `!isPreview && !$last` → `<input ng-model="ds.commission_sale_percent"
  ng-change="form.onChangeCommissionSalePercent()" only-number decimal-upto="2" max-value="100">`.

### FE2 — `resources/views/partials/classes/sale/firm/contract/FirmSupportAccounting.blade.php` (`onChangeCommissionSalePercent`, ~dòng 74)
Thay chia-đều bằng: phòng hỗ trợ cuối = `100 − (phòng chính + các phòng hỗ trợ còn lại)`, kẹp ≥ 0.

### FE3 — cùng file, `isInvalidData()` (~dòng 236)
Thêm chặn submit đầu khối `if (data.approver_id || data.status)`: nếu tổng %DS (main + supports)
làm tròn ≠ 100 → `toastr.warning('Tổng tỷ lệ Doanh số tính thưởng năng suất của các phòng phải là 100%.')`
+ `return true`.

### BE — `app/Http/Requests/Sale/Firm/Contract/FirmContractApproveRequest.php`
Thêm `withValidator`: tổng `department_main.commission_sale_percent +
departments_support.*.commission_sale_percent` (làm tròn) phải = 100, lỗi gắn vào
`department_main.commission_sale_percent`.

## An toàn
- Branch `gop_db`. DB = PROD `hrm_erp_gop` → chỉ đọc/dry-run, KHÔNG ghi DB.
- Không sửa hàm dùng chung; thay đổi khu trú trong luồng support-accounting HĐ hãng.
