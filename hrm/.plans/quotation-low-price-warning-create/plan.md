# Cảnh báo giá bán <= 1.000 đ thiếu ở màn TẠO MỚI báo giá

- [x] FE `quotations/_id/edit.vue`: `openSubmit()` rẽ sớm sang `openSubmitOnCreate()` nên bỏ qua check `lowPriceItems` → thêm check vào `openSubmitOnCreate()` sau khi validate payload
- [x] FE: tách `previewSubmitOnCreate()` khỏi `openSubmitOnCreate()` và cho `onLowPriceContinue()` gọi lại khi ở chế độ tạo mới
