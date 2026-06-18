# Fix: tiền VAT vận chuyển không về 0 khi xóa thành tiền về 0

## Bối cảnh

Màn báo giá dịch vụ (`/admin/sale/firm-quotations/{id}/edit`) → section "Thông tin thanh toán" → dòng **Vận chuyển**. Khi user sửa "Thành tiền" vận chuyển về **0**, ô **tiền VAT vẫn giữ giá trị cũ** (vd 53) → Tổng VAT sai.

## Root cause

Directive dùng chung `inputGroupPercent` (`public/js/angular/app.directive.js:724-746`). Watcher `$watch('value')` thiếu nhánh xử lý `value = 0`:
- Khi `value` về 0 mà `percent` (8) và `amount` (53) cũ vẫn truthy:
  - Early-return dòng 725 `!value && (!percent || !amount)` = false → bỏ qua.
  - Dòng 737 `percent && value && !initComponent` = `8 && 0 && true` = false → nhảy `else`, chỉ set cờ, **không ghi lại amount**.
- → `amount` (tiền VAT) kẹt ở giá trị cũ.

## Fix (Cách A — sửa directive dùng chung)

`app.directive.js:725` — đổi điều kiện early-return: ở chế độ tính tiền VAT (không phải `reCalculatePercent`), khi `value = 0` luôn ghi `amount = 0`:

```js
// cũ
if(!scope.value && (!scope.percent || !scope.amount)) {
    scope.amount = 0;
    return;
}
// mới
if (!scope.value && !scope.reCalculatePercent) {
    scope.amount = 0;
    return;
}
```

**Lý do an toàn cho các màn khác:**
- Non-reCalc: chỉ thay đổi đúng case bug (value=0 + percent&amount cũ truthy) → giờ zero đúng. Các case value=0 còn lại vốn đã zero.
- reCalc mode: điều kiện mới `!reCalc` = false → **không bao giờ** đi vào nhánh zero → giữ nguyên hành vi cũ.

## Tasks

- [x] Sửa `public/js/angular/app.directive.js:725` theo trên
- [ ] Verify repro trên browser (xem mục Test)

## Test (repro thủ công — không có JS test framework)

1. Mở 1 báo giá dịch vụ có **thành tiền vận chuyển > 0** (tiền VAT hiển thị, vd 53).
2. Sửa "Thành tiền" vận chuyển → **0**.
3. Kỳ vọng: ô **tiền VAT vận chuyển = 0**, "Thành tiền sau thuế" dòng vận chuyển = 0, **Tổng VAT** không còn dính phần thừa.
4. Đổi ngược lại thành tiền > 0 → tiền VAT tính lại đúng `thành tiền × % / 100` (không hồi quy).
5. Regression: kiểm 1 màn khác cũng dùng `input-group-percent` (vd dòng VAT khác trên cùng báo giá) vẫn tính đúng khi đổi giá trị.

### Checkpoint — 2026-06-15
Vừa hoàn thành: Sửa `app.directive.js:725` (early-return zero amount khi value=0, non-reCalc)
Đang làm dở: chờ user verify browser
Bước tiếp theo: user test repro 5 bước (mục Test)
Blocked:
