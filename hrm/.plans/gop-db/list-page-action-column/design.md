# Chuẩn cột Hành động cho màn danh sách — màn mẫu `/assign/customers`

@junfoke — nhánh `gop_db`

## Mục tiêu

Chuẩn hoá UI màn danh sách để các màn sau copy theo. Màn mẫu: **Danh sách khách hàng** (`/assign/customers`).

## Quy ước chốt

1. **Cột "Hành động" nằm cuối bảng.** Không còn nút thao tác nhét trong ô đầu (dưới tên bản ghi).
2. **Tối đa 3 nút / dòng.** Nhiều hơn 3 → giữ **2 hành động chính** (thường là Sửa + Xóa; màn nào không có Xóa thì là Khóa/Mở khóa) + **1 nút "⋮"** mở menu dọc chứa phần còn lại.
3. **Bỏ hành động "Xem".** Tên bản ghi ở cột đầu là **link** vào màn chi tiết.
4. **Cột "Trạng thái" mặc định đứng ngay trước cột Hành động.** Trong ô trạng thái chỉ hiển thị badge — nút Khóa/Mở khóa chuyển sang cột Hành động.
5. **Icon dùng `V2BaseIconButton`** (khuôn `pages/customer-care/device-errors/index.vue`), size `md`.
6. **Cột gộp mã + tên: header mặc định `Mã - Tên`**, dựng bằng `V2BaseTitleSubInfo`. Hai cột đầu (STT + Mã - Tên) khai `sticky: true` để ghim trái khi cuộn ngang (khuôn `assign/prospective-projects`); STT khai `width` + `minWidth` BẰNG NHAU (`48px`, cột chỉ chứa 1-3 chữ số), cột `Mã - Tên` đặt `minWidth: 300px` vì `getStickyColumnStyle` cộng dồn width các cột sticky trước đó để tính `left`.
7. **Hành động chuyển trang phải là `<nuxt-link>`** (khai `to` trong action) để chuột phải mở tab mới được — áp dụng cả nút trong menu "⋮".

## Quy tắc căn lề cột (áp cho MỌI màn danh sách)

**Nguyên tắc gốc: header căn CÙNG lề với ô dữ liệu của nó.** `V2BaseDataTable` đã tự lấy `column.align` cho cả `<th>` lẫn `<td>` → chỉ khai `align` một chỗ trong `tableColumns`, không tự viết `text-center` / `text-right` cho riêng header.

| Loại dữ liệu                                                            | `align`  | Vì sao                                        |
| ----------------------------------------------------------------------- | -------- | --------------------------------------------- |
| STT                                                                     | `center` | cột hẹp, số ngắn, đọc như nhãn thứ tự         |
| Chữ: tên, mã bản ghi, MST, SĐT, email, địa chỉ, ghi chú, tên người…     | `left`   | mắt quét theo mép trái, dễ dò tên             |
| Số đếm / số lượng / tiền / % / định mức                                 | `right`  | hàng nghìn thẳng cột, so sánh độ lớn bằng mắt |
| Ngày, giờ                                                               | `left`   | định dạng cố định, đi liền cụm cột chữ        |
| Badge trạng thái, icon, checkbox chọn dòng, cờ Có/Không                 | `center` | khối hình khép kín, căn giữa cân ô            |
| Cột **Hành động**                                                       | `center` | nhóm nút nằm giữa ô, ô cuối bảng              |

Kèm theo:

- Cột số/tiền: format bằng helper (`toLocaleString`), ô trống hiển thị `—` và vẫn căn phải.
- Cột chữ dài (địa chỉ, ghi chú): `cellClass: 'text-wrap'` + `minWidth` để bảng auto-layout không bóp hẹp.
- Cột `center` nên khai `width` cố định (STT `48px`, Trạng thái `130px`, Hành động `140px`) — căn giữa trong ô co giãn trông lệch.
- KHÔNG dùng `align: 'right'` cho mã số dạng định danh (MST, SĐT, số CCCD, số tài khoản): là chuỗi, không so sánh độ lớn.

## Màu title link

Theo khuôn "mã phiếu" ở `mockup-report.html` (class `.lnk`): navy `#28539d` + `font-weight: 600` + gạch chân **nét đứt** `#b7c4cf` + mũi tên `↗` 11px; hover chữ `#088f84`, viền `#0aa699`. Sửa thẳng trong `V2BaseTitleSubInfo` (bỏ `color: #111 !important` cũ), áp cho cả 6 chỗ đang dùng `linkUrl`. Không dùng `!important` để phần `isLightColor` (mã bản ghi) vẫn giữ xám `#6c757d`.

## Component dùng chung

`components/V2BaseRowActions.vue`

```vue
<V2BaseRowActions :actions="getRowActions(item)" @action="handleRowAction({ action: $event, item })" />
```

Mỗi action: `{ key, title, icon, to?, danger?, interactable?, disabledTitle?, visible? }`.
Thứ tự mảng quyết định nút nào là hành động chính (2 phần tử đầu).

**Gotcha:** bảng `V2BaseDataTable` có `overflow` nên menu để trong ô sẽ bị cắt → component tự `appendChild` menu ra `document.body` lúc `mounted` và định vị `position: fixed` theo toạ độ nút "⋮" (tự lật lên trên / thụt vào khi chạm mép), tự dọn node khi `beforeDestroy`.

## Áp dụng ở màn khách hàng

- Hành động chính: **Sửa** (nuxt-link, theo quyền sửa) + **Khóa/Mở khóa** (theo quyền xóa KH như ERP).
- Menu "⋮": **Quản lý** (nuxt-link) + **Lịch sử** (modal).
- Cột `status` đổi khoá thành `customerStatus` và dời xuống cuối `allColumns` — cố ý, để cấu hình cột đã lưu của user (`column_customizations.customers`) coi đây là cột MỚI và chèn đúng vị trí mới.
- Cột `actions` KHÔNG nằm trong `allColumns` → không vào modal Cấu hình cột, luôn chốt cuối bảng.
