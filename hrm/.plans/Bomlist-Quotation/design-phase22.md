# Design Phase 22: In báo giá

## Mục tiêu
Cho phép in/xem trước báo giá dạng HTML từ trang chi tiết báo giá, với tuỳ chọn cột hiển thị và ẩn/hiện cấp con.

## Phương án
Hoàn toàn FE — không cần API mới. Data đã load sẵn trên trang show (`this.item`, `this.products`, `this.serviceItems`). Ảnh banner lấy từ `$store.state.employee_company.header` (field `header` bảng `companies`).

## Flow
1. User mở trang chi tiết báo giá `/assign/quotations/{id}`
2. Bấm button **"In"** (hiện đang disabled) → mở **Modal 1: Chọn cột**
3. Chọn/bỏ chọn cột, toggle "Hiện hàng hoá cấp con" → bấm **"Xem trước"**
4. Mở **Modal 2: Preview** (full-screen, size="xl") hiển thị HTML báo giá
5. Bấm **"In"** trong modal → gọi `window.print()` với CSS `@media print`

## Layout trang in (theo mẫu Excel "Form bao gia sample.xlsx")

```
┌──────────────────────────────────────────────┐
│ [Ảnh banner công ty — companies.header]      │
│                                              │
│              BÁO GIÁ HÀNG HÓA               │
│                                              │
│ Kính gửi: {contact_name}  Báo giá số: {code}│
│ Tên đơn vị: {customer}    Dự án: {project}   │
│ Địa chỉ: {address}        Ngày: {created_at} │
│ ĐT/Email: {phone/email}   ĐDKD: {sales_name}│
│ Hiệu lực: {validity_days} Giao hàng: {days}  │
│ Bảo hành: {warranty}      Tiền tệ: {currency}│
│                                              │
│ Chúng tôi xin gửi đến quý KH báo giá...    │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ I. Nhóm A                               │ │
│ │ 1  │ Cha │ ... │ Giá bán │ VAT │ Tổng  │ │
│ │ 1.1│  Con│ ... │         │     │       │ │
│ │ II. Nhóm B                              │ │
│ │ ...                                      │ │
│ │ Dịch vụ bổ sung                         │ │
│ │ 1  │ DV-xxx │ ... │ Giá bán │ VAT │    │ │
│ │─────────────────────────────────────────│ │
│ │ TỔNG CỘNG │      │ xxx │       │ xxx   │ │
│ └──────────────────────────────────────────┘ │
│ Tổng VAT: xxx                                │
│ Tổng sau VAT: xxx                            │
│                                              │
│ Điều khoản thanh toán: {payment_terms}       │
│ Ghi chú: {sales_note}                       │
│                                              │
│       Ngày {dd} Tháng {mm} Năm {yyyy}       │
│          ĐẠI DIỆN KINH DOANH               │
│          {Tên NVKD chính}                    │
└──────────────────────────────────────────────┘
```

## Danh sách cột tuỳ chọn

| Key | Label | Mặc định |
|-----|-------|----------|
| stt | STT | ON |
| name | Tên hàng hoá | ON |
| code | Mã hàng hoá | ON |
| model | Model | ON |
| brand | Thương hiệu | ON |
| origin | Xuất xứ | ON |
| unit | Đơn vị tính | ON |
| specification | Thông số kỹ thuật | ON |
| qty | Số lượng | ON |
| quoted_price | Đơn giá bán | ON |
| amount | Thành tiền bán | ON |
| vat_percent | VAT (%) | ON |
| vat_amount | Tiền VAT | ON |
| after_vat | Thành tiền sau VAT | ON |

**Không hiện trên bản in** (nội bộ): Giá nhập, Thành tiền nhập, Tỷ suất LN.

**Checkbox bổ sung:**
- ☑ Hiện hàng hoá cấp con (mặc định ON)

## Nguồn dữ liệu

| Thông tin | Nguồn |
|-----------|-------|
| Banner công ty | `$store.state.employee_company.header` (URL ảnh từ bảng companies) |
| Mã, ngày, hiệu lực, giao hàng, bảo hành, tiền tệ | `this.item` (Quotation show API) |
| Khách hàng, MST, địa chỉ, ĐT, email, người LH | `this.item.customer_*` (snapshot trên quotation) |
| NVKD chính | `this.item.project.main_sale_employee_id` → resolve tên từ `$store.state.employees` |
| Sản phẩm + nhóm + cha-con | `this.products`, `this.groups` (đã load) |
| Dịch vụ bổ sung | `this.serviceItems` (đã load) |
| Tổng cộng | `this.totalSale`, `this.totalVat`, `this.totalAfterVat` (computed) |
| Điều khoản, ghi chú KD | `this.item.payment_terms`, `this.item.sales_note` |

## Quyết định kỹ thuật

1. **Không tạo API mới** — tất cả data đã có trên FE, chỉ cần render HTML + CSS print
2. **2 modal**: Modal 1 chọn cột (nhẹ, `size="md"`), Modal 2 preview (`size="xl"`)
3. **CSS `@media print`**: ẩn sidebar, topbar, footer bar, modal backdrop — chỉ in nội dung preview
4. **Dịch vụ bổ sung** nằm cuối bảng (giống trang show hiện tại)
5. **Cấp con** toggleable qua checkbox, con hiện "—" ở cột giá bán/VAT (giống logic show)
6. **Format tiền**: dùng `Intl.NumberFormat('vi-VN')` — dấu `.` ngăn cách hàng nghìn
7. **Thông số kỹ thuật**: strip HTML tags khi in (dùng `innerText` hoặc regex)
8. **Page**: landscape cho nhiều cột, `@page { size: A4 landscape; margin: 10mm; }`
