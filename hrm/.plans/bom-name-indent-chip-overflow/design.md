# Design — Sửa 2 lỗi UI

## 1. Tên hàng ở BOM LIST bị "tab" thụt vào ở dòng đầu
Nguyên nhân: tên đồng bộ từ ERP / import Excel dính khoảng trắng CỨNG (`&nbsp;` = U+00A0) ở đầu.
CSS `white-space: normal` chỉ bỏ được khoảng trắng THƯỜNG ở đầu dòng, khoảng trắng cứng vẫn vẽ ra
→ chỉ DÒNG ĐẦU bị thụt, dòng wrap và dòng "Ghi chú nội bộ" vẫn thẳng lề.
Xử lý: helper dùng chung `trimHardSpaces()` (`utils/helpers.js`), áp lúc nạp dòng (dữ liệu lưu lại
cũng sạch) và lúc hiển thị (phòng các đường thêm hàng khác).

## 2. Chip select chọn nhiều tràn ra ngoài ô
Nguyên nhân: `V2BaseSelect.vue` đảo vị trí dấu × bằng `flex-direction: row-reverse`. Với row-reverse,
main-start nằm bên PHẢI nên chip dài hơn ô thì phần thừa tràn sang TRÁI và bị ô cắt mất ĐẦU chữ
(`Sản phẩm ngừng kinh doanh` → `n phẩm ngừng kinh doanh`).
Xử lý: chip `display: inline-block` + `overflow: hidden` + `text-overflow: ellipsis`, dấu × ghim
`position: absolute` ở mép phải, padding-right chừa chỗ cho × theo từng size (xs/sm/md/lg).
Ảnh hưởng: TOÀN BỘ select chọn nhiều của hệ thống (`V2BaseSelect` + `V2BaseSelectInModal` dùng chung).
