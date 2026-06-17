# Fix — Invoice2 (BuyContract2): hàng bảo hành không sửa được SL & khai hải quan

## Triệu chứng
Lập Invoice từ HĐ mua hàng nước ngoài (BuyContract2), section "3. Hàng bảo hành": không sửa được **số lượng (SL)** và không bỏ tick được **"Khai hải quan"**.

## Root cause (chỉ là khóa FE, hạ tầng đã sẵn sàng)
`resources/views/orders/invoice2/form.blade.php` section "3. Hàng bảo hành" (~532-624):
- SL render text `<% product.qty %>` (dòng 592) thay vì input.
- Checkbox khai hải quan per-row `disabled` hardcode (dòng 608).

Trong khi:
- JS class `Invoice2ProductGuarantee`: có setter `qty` (clamp max = `contract_available_qty`), `amount` là getter tự tính theo `_qty`; `submit_data` GỬI `qty` + `customs_declaration`.
- BE `Invoice2::syncProductGuarantees()` NHẬN và LƯU cả `qty` + `customs_declaration`.
- BuyContract2 form thì SL + customs của hàng bảo hành vốn editable.
- Hàng khuyến mại trong cùng form: SL editable (input) → cho thấy khóa warranty là bất nhất/thiếu sót, không phải rule rõ ràng.

## Fix
- [x] Dòng 592: `<% product.qty %>` → `<input class="form-control" type="text" ng-model="product.qty">` (amount tự cập nhật qua getter; setter đã clamp ≤ SL hợp đồng).
- [x] Dòng 608: bỏ `disabled` ở checkbox `product.customs_declaration` (cho bỏ tick từng dòng).
- Giữ nguyên: section "4. Hàng thừa thiếu" (686/702) và "2. Khuyến mại" (514) — đúng phạm vi user báo (chỉ hàng bảo hành).
- Chưa bật check-all header customs (dòng 556) — cần handler ng-change propagate; bỏ tick per-row đã đáp ứng yêu cầu.

## Lưu ý / cần xác nhận
- "Khai hải quan" là dữ liệu liên quan thủ tục hải quan → xác nhận nghiệp vụ cho phép sửa SL + bỏ khai hải quan hàng bảo hành là đúng ý.
- BE validate `product_guarantees.*.qty` = required|min:1 (không nhập 0/trống).

## Kiểm thử (user — chạy app)
- [ ] Lập invoice từ BuyContract2 có hàng bảo hành → sửa được SL (không vượt SL hợp đồng), Thành tiền cập nhật theo.
- [ ] Bỏ tick "Khai hải quan" từng dòng hàng bảo hành → lưu, mở lại đúng trạng thái đã lưu.
- [ ] Hàng thừa thiếu / khuyến mại giữ nguyên hành vi cũ.

### Checkpoint — 2026-06-10
Vừa hoàn thành: mở input SL + bỏ disabled customs cho hàng bảo hành (form.blade.php 592, 608)
Bước tiếp theo: user chạy thử + xác nhận nghiệp vụ
Blocked:
