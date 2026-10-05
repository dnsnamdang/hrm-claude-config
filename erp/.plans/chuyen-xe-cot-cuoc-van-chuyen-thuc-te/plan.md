# Plan — Cột Cước vận chuyển thực tế ở DS chuyến xe (#11355)

Nhánh: `task_11355` (từ `master`). Repo: `TanPhatDev`. @junfoke

## Phase 1 — Màn Chuyến xe chở hàng (delivery_trips)
- [x] `resources/views/warehouse/delivery_trips/all.blade.php`: thêm cột `total_cost_transition` (title "Cước vận chuyển thực tế") giữa `warehouse_exports` và `status`
- [x] Cùng file: thêm 2 ô lọc `total_cost_transition_from` / `total_cost_transition_to` (`search_type: "currency"`)
- [x] `DeliveryTripController@searchData`: `editColumn('total_cost_transition')` → `number_format`, null → rỗng
- [x] `DeliveryTrip::searchByFilter`: 2 tham số from/to (`str_replace(',','')` rồi `>=` / `<=`)

## Phase 2 — Màn Chuyến xe khác (other_delivery_trips)
- [x] ⚠️ View đúng là **`common/other_delivery_trips/index.blade.php`** — `OtherDeliveryTripController@all()` render `.index`, KHÔNG phải `all.blade.php` (file `all.blade.php` là code chết, đã sửa nhầm rồi revert)
- [x] Thêm cột trước `status` + 2 ô lọc from/to
- [x] `OtherDeliveryTripController@searchData`: `editColumn` number_format
- [x] `OtherDeliveryTrip::searchByFilter`: xử lý from/to

## Phase 3 — Verify
- [x] `php -l` sạch 4 file PHP
- [x] `git diff --stat` gọn 6 file / 32 dòng thêm → line ending (CRLF) nguyên vẹn
- [x] Browser localhost:8011 (DB `erp_dev_30_01_26`):
  - Chuyến xe chở hàng: header đúng thứ tự …Phiếu | **Cước vận chuyển thực tế** | Trạng thái…; số `495,000` có phân cách; sort asc (rỗng→120,000→…) / desc (1,899,700→…); lọc 200,000–800,000 ra đúng khoảng; lọc 495,000–495,000 ra đúng 4 phiếu (2 đầu mút inclusive)
  - Chuyến xe khác: header …Nhà cung cấp | **Cước vận chuyển thực tế** | Trạng thái…; sort 2 chiều đúng; lọc 700,000–2,000,000 ra 5 phiếu (2,000,000 nằm trong, 677,600 bị loại)
- [ ] User test lại trên môi trường dev/prod
- [ ] Commit + merge `task_11355` → `master` (user tự làm)

### Checkpoint — 2026-09-08
Vừa hoàn thành: code + verify browser cả 2 màn.
Đang làm dở: không.
Bước tiếp theo: user review, commit và merge `task_11355` vào `master`.
Blocked: không.

## Ghi chú phát sinh (KHÔNG thuộc scope, cần user quyết)
- Nhánh `master` đang **vỡ sẵn**: `HandoverAcceptanceProductRecordsController::EXPORTED_STATUSES` (dòng 53-63) dùng `ProductExportRequest::CHO_DUYET_NHAP` … `DANG_HACH_TOAN_NHAP` (14–19) nhưng các hằng số đó **chỉ có trên `develop_01`** (commit `929e06f90b`), chưa vào `master` → app không boot được (mọi route 404, `php artisan route:list` cũng lỗi). Để test tôi đã vá tạm 6 hằng số rồi **hoàn nguyên** — file `ProductExportRequest.php` hiện sạch. Cần user xử lý riêng (đưa hằng số sang master hoặc merge phần thiếu).
