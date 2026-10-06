# Phase 2 — Khảo sát màn hàng hoá bên ERP (20–21/09/2026)

> Đo thật trên DB gộp `hrm_erp` và mã nguồn `ERP/TanPhatDev`. Dùng làm nền cho mockup.
> Trạng thái: khảo sát xong, **chờ tài liệu yêu cầu của khách** để dựng mockup.

## 1. Quy mô — vì sao màn này khác mọi màn đã port

| Thứ | Số đo |
|---|---|
| Cột bảng `products` | **59** |
| Số dòng `products` | 45.890 (chưa tính `deleted_at`) |
| **Bảng khác có FK trỏ vào `products`** | **171** |
| `ProductsController` | 4.623 dòng |
| `app/Product.php` (model) | 8.122 dòng |
| `form.blade.php` / `formEdit.blade.php` | 95 KB mỗi file |
| Khối trong form tạo/sửa | 17 |
| Cột màn danh sách | 29 (8 hiện mặc định) |
| Cột bộ xuất Excel (khai riêng) | 45 |

171 bảng tham chiếu nghĩa là **đây là bảng trung tâm của ERP**, không phải danh mục lá như 11 màn
Phase 1. Giống Phase 1 ở chỗ **không di trú dữ liệu** (HRM ghi thẳng vào bảng ERP đang chạy), nhưng
khác ở chỗ mọi sai lệch khi ghi sẽ lan ra hàng trăm màn ERP.

## 2. 17 khối của form tạo/sửa hàng hoá (ERP)

| # | Khối | Trường chính |
|---|---|---|
| 1 | Thông tin hàng hóa | Tính chất hàng hóa · Model · Loại hàng hóa · Tên hàng hóa · Tên thường gọi · Tên tiếng Anh · Barcode · Định mức công lắp đặt · Hệ số công nghệ · Bảo hành · Ghi chú |
| 2 | Tài liệu kỹ thuật | bảng tệp đính kèm |
| 3 | Thông số cơ bản | Trọng lượng (kg) · Kích thước (cm) · Nhóm hàng hóa + bảng thuộc tính động |
| 4 | Phụ tùng – Phụ kiện | Nhóm máy · Máy |
| 5 | Phụ tùng ô tô | Hãng xe · Loại xe · Model xe · Đời xe (+ "áp dụng tất cả đời xe") |
| 6 | Phụ kiện tùy chọn mua thêm | bảng chọn hàng hoá |
| 7 | Vật tư phục vụ sửa chữa – bảo dưỡng | bảng chọn hàng hoá |
| 8 | Vật tư phục vụ lắp đặt | bảng chọn hàng hoá |
| 9 | Công thức lắp ráp | bảng định lượng (BOM) |
| 10 | Phụ kiện tiêu chuẩn | text |
| 11 | Đặc điểm | text |
| 12 | Hệ số giá theo công ty | bảng theo công ty |
| 13 | Khác | % giảm giá thanh lý |
| 14 | Giá theo đơn vị | Đơn vị · Đơn vị cơ bản · Hệ số quy đổi · Giá vốn · Giá mua ngoài · hệ số/định mức đàm phán |
| 15 | Nguồn gốc | Thương hiệu · Xuất xứ · Hãng sản xuất · Code đặt hàng · Nhà cung cấp · Công ty |
| 16 | Đặt hàng | Tên khai hải quan · HS Code · % VAT · Thuế NK (có/không CO) · Thuế chống bán phá giá · SL tối thiểu nhập mua · Thuế BVMT + hệ số |
| 17 | Kho hàng · Ảnh · Video | SL tồn kho tối thiểu · ảnh đại diện + ảnh mô tả · video |

Khối 14 (Giá) đụng quyền **"Quản lý giá"** — giá vốn là dữ liệu nhạy cảm, phải gate cả BE lẫn FE.

## 3. Màn danh sách — 29 cột

Mặc định hiện: Ảnh · Tên hàng hóa · Thông số cơ bản · Model · Thương hiệu · Giá · Mã hàng hóa ·
Trạng thái · Ngày sửa · Tính chất hàng hóa · Loại hàng hóa · Xuất xứ · Hãng sản xuất · % VAT.
Ẩn mặc định: Nhóm · Tồn kho · Định mức công · các bảng giá (buôn/đại lý/khác) · Tên tiếng Anh ·
Người tạo/Người sửa · Code đặt hàng · Ghi chú · Công thức lắp ráp · Phụ kiện mua thêm/lắp đặt ·
Ngày tạo · Định mức giảm giá.

Người dùng tự cấu hình cột, lưu ở `localStorage` key `product-columns` (bộ xuất Excel lưu riêng ở
`product-export-columns`) — **không lưu server**, đổi máy là mất.

## 4. 🔴 Hai phát hiện đổi cục diện

### 4.1 "Tính chất hàng hóa" bên ERP KHÔNG phải danh mục

`products.product_type` là **enum chuỗi cứng**, không có FK:

| Giá trị | Số hàng hoá |
|---|---|
| `product` | 12.358 |
| `accessories` | 11.817 |
| `tool` | 9.184 |
| `tool_and_device` | 5.447 |
| `supplies` | 3.314 |
| `product_wait_build` | 1.369 |
| `weld_materials` | 808 |
| `lubricant` | 609 |

"Loại hàng hóa" là `products.product_cate` — cột **JSON nhiều giá trị**, cũng là khoá chuỗi cứng
(`["hang_nhap_theo_yeu_cau"]`, `["hang_ban_not_ton_kho"]`…).

⚠️ Trùng tên tiếng Việt với danh mục Phase 0 nhưng **là thứ khác**: Phase 0 có *Tính chất hàng hóa*
(`product_natures`) và *Loại sản phẩm* (`product_types`) — chú ý "Loại **sản phẩm**" ≠ "Loại **hàng
hóa**".

### 4.2 `products` chưa nối vào cây phân loại mới

- Không có cột nào trong `product_nature_id` / `product_function_group_id` / `product_family_id` /
  `product_type_id` / `business_policy_id` / `product_characteristic_id`.
- `group_id` (nhóm hàng hoá cũ — thuộc nhóm **BỎ** ở Phase 5): **45.890/45.890 dòng đều có giá trị**.
- Phase 0 ghi rõ *"Gắn hàng hóa vào cây mới"* nằm **ngoài phạm vi đợt đó** → rơi vào Phase 2.

Hệ quả: Phase 2 không chỉ là dựng lại UI. Phải chốt thêm **thêm cột FK vào `products`** và **quy đổi
45.890 hàng hoá** từ enum cũ + `group_id` sang cây 4 cấp, trong khi ERP vẫn đang đọc/ghi cột cũ.

⚠️ 6 bảng Phase 0 trên DB local **đang 0 dòng** (mới chạy migration, chưa có dữ liệu nghiệp vụ) —
chưa kiểm được trên dữ liệu thật của khách.

## 5. Câu còn treo

Tài liệu Phase 0 nhắc **"TASK 3 màn Danh mục hàng hóa 6 tab"**, trích từ tài liệu yêu cầu của khách
(#11421) — bản gốc không có trong repo. User xác nhận **sẽ đưa tài liệu** (21/09/2026); mockup bám
theo tài liệu đó.
