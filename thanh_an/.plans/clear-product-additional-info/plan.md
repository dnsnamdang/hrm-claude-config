# Plan — Xóa ghi chú (Thông tin bổ sung) hàng hóa theo mã nội bộ

**Phụ trách:** @khoipv
**Ngày:** 2026-08-14

## Bối cảnh

Xóa dữ liệu cột **Ghi chú** trong tab **Thông tin bổ sung** của màn Hàng hóa
(`products.additional_info`) cho danh sách hàng hóa trong sheet
`SHEET CẦN XÓA GHI CHÚ` của file
`C:\Users\Admin\Downloads\danh_sach_hang_hoa_2026-08-14_12-27-53.xlsx`,
đối chiếu theo **mã nội bộ** (`products.internal_code`).

## Task

- [x] Xác định mapping: "Ghi chú" tab Thông tin bổ sung → `products.additional_info`
      (`AdditionalInfo.vue:761`, migration `2025_04_19_095123_add_additional_info_to_products_table.php`)
- [x] Đọc sheet 2 `SHEET CẦN XÓA GHI CHÚ` → cột E = Mã nội bộ, 1035 mã, không trùng
- [x] Đối soát DB (`thanhan_stag_07052026`): 1035/1035 mã khớp, 0 mã thiếu,
      1035 bản ghi đang có ghi chú, tất cả `type = 1`, không có bản ghi xóa mềm
- [x] Viết `database/seeders/ClearProductAdditionalInfoSeeder.php`
- [ ] User review seeder
- [ ] Chạy seeder trên staging
- [ ] Xác nhận kết quả

## Quyết định

- Danh sách 1035 mã nội bộ **nhúng thẳng trong seeder** → không phụ thuộc file
  Excel ở `Downloads`, chạy lại được trên máy khác / server.
- **Backup trước khi xóa**: dump `id + internal_code + additional_info` cũ ra
  `storage/app/backup/clear-product-additional-info-<timestamp>.json` để rollback được.
- **Không đụng `updated_at`** → không làm lệch "Ngày cập nhật" hiển thị trên màn hình.
- Không ghi `product_histories` (đây là thao tác dọn dữ liệu, không phải user sửa).

## Checkpoint — 2026-08-14

Vừa hoàn thành: Viết xong seeder `ClearProductAdditionalInfoSeeder`, đã đối soát dữ liệu.
Đang làm dở: Chờ user đọc lại seeder.
Bước tiếp theo: User duyệt → chạy `php artisan db:seed --class=ClearProductAdditionalInfoSeeder`
Blocked:
