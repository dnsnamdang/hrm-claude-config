# Plan — Fix 504 màn sửa YCXH type=14 (N+1 accessor exporting_qty)

Feature nhỏ (1 phase). Repo: `ERP/TanPhatDev`, nhánh `gop_db`. Chỉ sửa code, KHÔNG ghi DB.

## Task

- [x] **Task 1 — Short-circuit accessor `getExportingQtyAttribute()`**
  - File: `app/Model/Sale/Firm/Contract/FirmContractTabProduct.php` (dòng 118).
  - Đổi chữ ký `getExportingQtyAttribute()` → `getExportingQtyAttribute($value = null)`.
  - Đầu hàm: nếu `array_key_exists('exporting_qty', $this->attributes) && $this->attributes['exporting_qty'] !== null` → `return (float) $this->attributes['exporting_qty'];` (dùng giá trị đã select/gán sẵn, tránh N+1).
  - Giữ NGUYÊN 2 query SUM cũ làm fallback (khi load model bình thường, không select cột).

- [x] **Task 2 — Căn statuses subquery cho khớp accessor**
  - File: `app/Model/Warehouse/ProductExportRequest.php` (dòng 524).
  - `->whereIn('per.status', [7, 2])` → `->whereIn('per.status', [2, 7, 10, 11])`.
  - Dữ liệu type=14 hiện chỉ có status 7 & 2 → KHÔNG đổi số; chỉ đúng nghĩa + phòng tương lai.

- [x] **Task 3 — Verify read-only qua tinker**
  - `php -l` 2 file: sạch.
  - `getDataForEdit(41795)` sau fix (DB remote `hrm_erp_gop`): **21 query / 1 SUM / 2795ms** (trước: 773 query / 752 SUM / ~131000ms). N+1 đã hết (chỉ còn 1 SUM lẻ hợp lệ ở chỗ khác). 2.8s gồm latency remote :33062 → trên prod (DB local) còn nhanh hơn nhiều, dưới xa timeout nginx.
  - Accessor fallback: giữ nguyên logic SUM cũ khi `attributes` không có key `exporting_qty` → 6+ caller khác không đổi hành vi.

## Rủi ro & an toàn
- 6+ nơi khác gọi accessor (FirmContract, service borrow/export) load model bình thường → không có key `exporting_qty` trong attributes → `array_key_exists`=false → chạy SUM y như cũ. AN TOÀN.
- Các model nhận gán `exporting_qty` ở getDataForEdit (ProductExportRequestTabProduct, ProductExportRequestDetail) KHÔNG có accessor này → gán bình thường.

## Checkpoint — 2026-09-28
Vừa hoàn thành: cả 3 task. 2 edit code (accessor short-circuit + căn statuses), php -l sạch, verify read-only 21 query/2.8s (từ 773/131s).
Đang làm dở: —
Bước tiếp theo: user test browser mở màn sửa YCXH 41795 trên dev/prod xác nhận; nếu OK → chốt commit nhánh gop_db (chờ yêu cầu).
Blocked:
