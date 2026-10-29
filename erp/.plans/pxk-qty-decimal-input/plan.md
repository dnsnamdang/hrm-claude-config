# Fix: ô "Yêu cầu xuất" (qty) phiếu YC xuất kho không nhập được dấu thập phân

## Bối cảnh / Triệu chứng
- Màn **Tạo phiếu yêu cầu xuất hàng** (`/admin/warehouse/product_export_requests/create`), loại **Xuất khác (type 99)** và các loại khác dùng chung class detail.
- Ô **Yêu cầu xuất** (`ng-model="product.qty"`, `form.blade.php:1363` cho type 99): gõ `6.9` ra `69` — dấu `.` bị xoá ngay khi gõ, không nhập được số thập phân.
- Reproduce bằng Playwright gõ phím thật (bỏ qua bộ gõ) trên sản phẩm chọn từ popup: `6.9` → DOM `69`. KHÔNG phải bộ gõ TV, prod == local.

## Nguyên nhân gốc (ĐÃ XÁC ĐỊNH)
File: `resources/views/partials/classes/warehouse/ProductExportRequestDetail.blade.php`
- Class `ProductExportRequestDetail`: `qty` là getter/setter.
- Commit `a0afdc04f5` (04/01/2025, "fix") comment out cơ chế `qty_dot` (vốn giữ dấu `.` đang gõ dở trong view):
  - getter dòng 43: `// if (this.qty_dot) return ... this._qty + this.qty_dot : 0;`
  - setter dòng 53-54: `// let match_dot = ...; // this.qty_dot = ...;`
- Hệ quả: gõ `6.` → setter `roundNumber("6.",2)=6` (SỐ) → getter trả `6` → AngularJS re-render `"6"` vào ô, xoá dấu `.` trước khi kịp gõ phần thập phân.
- Commit đó còn bỏ `numberWithCommas` (getter) + `parseNumberString` (setter) để NGỪNG format dấu phẩy ngàn — chủ đích, KHÔNG khôi phục phần này.

## Hướng sửa (minimal, chỉ khôi phục qty_dot)
Trong `ProductExportRequestDetail.blade.php`:
- Getter: bỏ comment dòng `if (this.qty_dot) return !isUndefined(this._qty) ? this._qty + this.qty_dot : 0;` (giữ dòng 44 `roundNumber` nguyên — KHÔNG đưa lại numberWithCommas).
- Setter: bỏ comment 2 dòng `match_dot` + `this.qty_dot = ...`. Giữ dòng `this._qty = value ? roundNumber(value, 2) : 0;` (roundNumber đã tự gọi parseNumberString nên không cần thêm parseNumberString).

Trace xác nhận: `6`→"6"; `6.`→match `.`→qty_dot="."→getter `6+"."="6."` (giữ dấu); `6.9`→qty_dot=null→`6.9`. ✓

## Phạm vi ảnh hưởng
- Class DÙNG CHUNG cho mọi loại phiếu YC xuất kho (các ô qty line 650/804/874/1075/1206/1285/1363/1439). Khôi phục qty_dot sửa decimal cho TẤT CẢ các loại bị regression — đúng ý muốn.
- Cần user xác nhận vì là class dùng chung.

## Tasks
- [x] Trace + xác định nguyên nhân gốc (reproduce Playwright native typing; git blame commit a0afdc04f5)
- [x] Khôi phục cơ chế `qty_dot` trong getter + setter `qty` (user chốt "ok" 2026-10-26)
- [x] Verify bằng Playwright: gõ `6.9`→`6.9`, `6.09`→`6.09`, `6.0`→`6.0`, `12.5`→`12.5` — DOM + model đều giữ đúng dấu thập phân (trước fix `6.9`→`69`)
- [x] Cập nhật memory (đã flip kết luận từ "IME" sang root cause thật)
