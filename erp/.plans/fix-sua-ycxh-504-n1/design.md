# Fix 504 màn sửa Phiếu YC xuất hàng (YCXH type=14) — N+1 accessor exporting_qty

## Mục tiêu
Màn sửa YCXH `/admin/warehouse/product_export_requests/{id}/edit` với phiếu **type = XUAT_BAN_HD_HANG (14)** đang **504 Gateway Time-out** (repro: phiếu 41795, prod-like DB `hrm_erp_gop`). Làm màn mở được nhanh, không đụng dữ liệu.

## Root cause (đã xác minh 100% qua tinker read-only)
- `ProductExportRequest::getDataForEdit($id)` nhánh type=14 (dòng 493–619) đã tối ưu bằng `leftJoinSub` tính sẵn `exporting_qty` trong 1 query (dòng 502–556) và **comment loop materialize cũ** (575–577).
- **Nhưng** model `FirmContractTabProduct` có accessor `getExportingQtyAttribute()` (dòng 118) tự chạy 2 query `SUM` (bảng `product_export_request_tab_products` + `warehouse_export_request_tab_products`) mỗi lần đọc `->exporting_qty`. Eloquent **ưu tiên accessor hơn cột đã select** → tối ưu leftJoinSub bị vô hiệu.
- HĐ 24620 (của phiếu 41795) có **188 sản phẩm**, mỗi sản phẩm đọc `exporting_qty` **2 lần** (dòng 594 + 598/602) → 188×2 = **376 lần gọi accessor = 376 SUM perd (88s) + 376 SUM werd (43s) = 752 query / 131s** → vượt timeout nginx.

### Số đo
| | Query | Thời gian |
|---|---|---|
| Chưa fix (getDataForEdit) | 773 (752 là SUM) | ~131.000 ms |
| Mô phỏng fix (đọc raw) | 1 | ~564 ms |

## Quyết định đã chốt
1. **Hướng fix: sửa accessor** (user chốt 2026-09-28). Short-circuit `getExportingQtyAttribute()` khi giá trị `exporting_qty` đã được select/gán sẵn → trả luôn, không chạy SUM.
   - An toàn với 6 nơi khác dùng accessor (FirmContract, các Service borrow/export): chúng không select cột `exporting_qty` → `array_key_exists` = false → chạy SUM y như cũ.
2. **Căn statuses subquery `[7,2]` → `[2,7,10,11]`** (dòng 524) cho khớp accessor. Dữ liệu hiện tại type=14 chỉ có status 7 và 2 (không có 10/11) nên **không đổi số nào**; chỉ để đúng nghĩa nghiệp vụ + phòng tương lai.

## Phạm vi thay đổi
- `app/Model/Sale/Firm/Contract/FirmContractTabProduct.php` — accessor `getExportingQtyAttribute()` (dòng 118).
- `app/Model/Warehouse/ProductExportRequest.php` — subquery `whereIn('per.status', ...)` dòng 524.

## Không làm
- KHÔNG ghi DB (chỉ đọc để verify).
- KHÔNG đổi ý nghĩa số liệu hiển thị (giá trị exporting_qty giữ nguyên).
