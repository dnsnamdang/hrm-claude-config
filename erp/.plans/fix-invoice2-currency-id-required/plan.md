# Fix: Lập Invoice2 từ hợp đồng mua nhập khẩu báo lỗi "currency_id bắt buộc"

## Triệu chứng
`buy_contract2/765/show` → lập Invoice → validate `currency_id required` fail, dù hợp đồng có tiền tệ.

## Root cause (xác minh trên prod)
- Contract 765: `currency='USD'` (CODE), `currency_id=2`.
- Class JS `Invoice2` (dòng 747) nạp currency_id **sai nguồn**:
  ```js
  self.currency_id = self.currencyByCodes[self.contract?.currency] || null;
  ```
- `currencyByCodes = Currency::getByCode()` — thực chất `pluck('id', 'name')` → map theo **TÊN** (`'Đô la Mỹ' => 2`), KHÔNG theo code.
- Tra `currencyByCodes['USD']` (code) → không có key → `null` → validate fail.
  (Hàm `getByCode()` bị đặt tên sai — nên là pluck theo `code`, nhưng đang theo `name`.)

## Fix
- [x] `Invoice2.blade.php:747`: ưu tiên `self.contract?.currency_id` (đã có sẵn = 2), fallback `currencyByCodes[currency]` cho data cũ lưu currency = tên.
- [ ] User test: lập Invoice2 từ HĐ 765 (currency USD) → currency_id auto = 2, không còn lỗi validate.

## File
- `resources/views/partials/classes/order/Invoice2.blade.php`

## Ghi chú
- KHÔNG sửa `Currency::getByCode()` (hàm dùng chung) — chỉ fix tại điểm nạp của Invoice2. Nếu muốn dọn hàm misnamed cần rà soát các nơi gọi khác trước.
