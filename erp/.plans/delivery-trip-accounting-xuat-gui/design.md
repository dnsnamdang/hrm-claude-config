# Hạch toán chuyến xe — bổ sung loại "Xuất gửi"

- **Ngày:** 2026-06-08
- **Phạm vi:** ERP (TanPhatDev) — Warehouse / Hạch toán chuyến xe
- **Trạng thái:** Đã sửa (1 dòng)

## Vấn đề
Màn `admin/warehouse/delivery_trip_accounting/{id}` khi hạch toán không sinh bút toán cho phiếu xuất loại **Xuất gửi** (`ExportModel::XUAT_GUI = 12`). Trong `DeliveryTripAccountingService::accountingDelivery()`, chuỗi `if/else if` theo `product_export_request->type` không có nhánh cho XUAT_GUI → activity rơi tự do: không tạo bút toán, không cộng `$total_cost_transition`. (Preview `getTable` vẫn hiển thị vì không lọc theo loại.)

## Yêu cầu
Hạch toán "Xuất gửi" **giống y hệt** "Xuất mượn", không khác biệt (không gắn hợp đồng, không tài khoản riêng).

## Giải pháp
Thêm `ExportModel::XUAT_GUI` vào nhánh xuất mượn trong `accountingDelivery()`:

```php
} else if (in_array($product_export_request->type, [ExportModel::XUAT_MUON, ExportModel::KHAC, ExportModel::XUAT_GUI])) {
```

Logic nhánh này (tái dùng nguyên):
- `is_company_sp = 1` (công ty hỗ trợ) → Nợ **6427** / Có 3311.
- ngược lại (nhân viên chịu phí) → Nợ **33481** / Có 3311, gắn `Employee` (created_by) + `Department` (phòng ban người tạo).
- cộng `total_cost_transition` vào tổng.

## Phạm vi & loại trừ
- Chỉ sửa `app/Services/DeliveryTripAccounting/DeliveryTripAccountingService.php` (1 dòng).
- Không migration, không FE, không đụng `OtherDeliveryTripAccountingService`.
- `getTable` (preview) không cần sửa.

## Kiểm thử
`admin/warehouse/delivery_trip_accounting/16` → hạch toán → bút toán có dòng cho phiếu xuất gửi (6427 hoặc 33481 tùy `is_company_sp`); tổng cước khớp với preview.
