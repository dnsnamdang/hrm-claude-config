# Cho phép xoá giá trị (dấu x) ở select màn Báo giá

- [x] FE: bật `allowClear` cho select Loại tiền tệ + Bảng giá (`pages/assign/quotations/_id/edit.vue`)
- [x] FE: `handleChangeCurrency` / `handleChangePriceType` bỏ qua confirm + không reprice khi user bấm x (select2 trả `''`)
- [x] FE: `validateForm()` bổ sung bắt buộc Bảng giá (trước đây không xoá được nên chưa cần)
