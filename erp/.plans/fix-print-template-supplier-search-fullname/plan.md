# Fix: form mẫu in — select NCC không tìm thấy theo tên đầy đủ (vd TOYOTA MOTOR ASIA)

## Root cause (đã xác minh prod erp_new)
- Kiến trúc: KHÔNG dùng bảng `suppliers` cũ. Model `Supplier` = `protected $table='customers'` +
  `newQuery()` thêm `where('is_supplier', true)`. Bảng `customers` chứa cả KH lẫn NCC (cờ is_supplier/is_customer).
- "TOYOTA MOTOR ASIA (SINGAPORE) PTE LTD" = customer id **43002**, code **TMAS**, status=1, **is_supplier=1**
  → CÓ trong list NCC (`Supplier::where('status',1)` = 9353 dòng, có 43002).
- NHƯNG option chỉ hiển thị `short_name` = "TMAS". Select2 client-side tìm theo text option → gõ
  "TOYOTA MOTOR ASIA" (fullname) không match "TMAS" → tưởng không có NCC.
- (Chẩn đoán đầu tiên "TOYOTA không phải supplier" là SAI — do query nhầm bảng `suppliers` cũ vô dụng.)

## Fix (đã code, CHƯA deploy)
- [x] `PrintTemplateController@create` + `@edit`: thêm `fullname` vào select suppliers.
- [x] `print_templates/form.blade.php`: option hiện `<% s.short_name %> - <% s.fullname %>` → search được
  theo cả mã tắt lẫn tên đầy đủ. `php -l` sạch. Verify: 43002 render "TMAS - TOYOTA MOTOR ASIA (SINGAPORE) PTE LTD".
- [ ] Deploy FE + `php artisan view:clear` trên prod; user test lại select.

## Ghi chú (không bắt buộc)
- List preload 9353 option trong select2 client-side khá nặng — về lâu dài nên đổi sang select2-ajax
  search server-side (theo short_name + fullname + code). Chưa làm trong lần này.
