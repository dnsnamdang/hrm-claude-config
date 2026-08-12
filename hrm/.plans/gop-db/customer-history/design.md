# Lịch sử thay đổi Khách hàng (`/assign/customers`) — @khoipv

## Mục tiêu

Bổ sung chức năng **Xem lịch sử** cho khách hàng ở **màn danh sách** (`/assign/customers`) và
**màn chi tiết** (`/assign/customers/{id}`), dùng lại đúng base đang chạy cho báo giá
(`/assign/quotations/271`).

## Base tái sử dụng

| Lớp | Base có sẵn | Cách dùng cho KH |
| --- | --- | --- |
| Endpoint | `GET /assign/system-logs/{type}/{id}` (`SystemLogController`) | thêm `type = customer`, KHÔNG thêm route mới |
| Chuẩn hoá log | `SystemLogService` (adapter/DTO chung: `action_label`, `action_color`, `actor_*`, `changes[]`, `note`) | thêm adapter `customerLogs()` |
| FE modal | `components/assign/quotation/QuotationHistoryModal.vue` (timeline, cũ ĐỎ → mới XANH) | copy sang `components/assign/customer/CustomerHistoryModal.vue`, đọc DTO của `system-logs` |
| Vị trí nút | báo giá: icon `ri-history-line` ở cột thao tác DS + nút `Lịch sử` màn chi tiết | làm y hệt cho KH |

## Quyết định đã chốt với user (2026-08-11)

1. **Track tất cả**: thông tin chính (bảng `customers`) + danh sách con (người liên hệ, người đại
   diện, TK ngân hàng, nhóm KH, loại hình hoạt động, lĩnh vực kinh doanh, hãng xe, địa điểm giao
   hàng) + file/ảnh/video/tài liệu tab "Thông tin khác".
2. **Action**: `create` (kể cả tạo qua import Excel), `update`, `update_media`, `lock`, `unlock`.
   KH tạo trước khi có tính năng (chưa có log) → dựng tạm 2 dòng từ cột audit
   (`created_by/created_at`, `updated_by/updated_at`) như BOM/Meeting đang làm.
3. **Không permission riêng** — vào được màn KH là xem được lịch sử (giống báo giá).

## Quyết định kỹ thuật

- **Bảng mới `customer_history`** (KH ghi thẳng vào `customers` của DB gộp, chưa có bảng log nào).
- **Ghi log trong Service, KHÔNG dùng Observer** (đúng skill `entity-history`): hook tại
  `CustomerService::save()` / `setStatus()` / `updateMedia()` / `deleteAttachmentFile()`.
- **Subset-diff**: `old_value`/`new_value` chỉ chứa các khoá thực sự đổi → bảng không phình.
  Riêng `create` lưu snapshot đầy đủ ở `new_value`.
- **Snapshot lưu GIÁ TRỊ HIỂN THỊ, không lưu id** (tên tỉnh/huyện/xã/thôn, tên KH cha, tên NV đại
  lý, tên nhóm ngành...) → log tự chứa, đọc lại không cần join, đổi tên danh mục sau này không làm
  sai lịch sử cũ.
- `changed_by = auth()->id()` (id nhân viên HRM, thống nhất với `task_history`), KHÔNG dùng ERP
  employee id. Riêng dòng dựng từ cột audit của `customers` phải map ERP employee id → nhân sự
  tương ứng (`employees.employee_info_id`).

## Phạm vi file

- BE: migration `customer_history` · `Entities/CustomerHistory.php` ·
  `Services/CustomerHistoryService.php` · hook trong `CustomerService` · adapter trong
  `SystemLogService`.
- FE: `components/assign/customer/CustomerHistoryModal.vue` ·
  `pages/assign/customers/index.vue` (nút icon trong cột thao tác) ·
  `pages/assign/customers/_id/index.vue` (nút "Lịch sử" trên màn chi tiết).

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-11-customer-history-design.md`
