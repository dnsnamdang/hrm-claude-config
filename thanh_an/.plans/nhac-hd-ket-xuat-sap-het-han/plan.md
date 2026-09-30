# Plan — Thông báo HĐ đã kết xuất sang cung ứng sắp hết hạn

@khoipv

## Phase 0 — Brainstorming
- [x] Khảo sát luồng kết xuất HĐ (`RenderedContractService`, `supply_rendered_at`)
- [x] Khảo sát cơ chế thông báo định kỳ (`app/Console/Commands/Notify*`, `Kernel::schedule`)
- [x] Khảo sát dữ liệu địa bàn KH (`customer_areas`) và phòng cung ứng (`departments`)
- [x] Xác nhận FE không phải sửa (`utils/mixins/CustomNotifyHeader.js`)
- [x] Chốt 7 quyết định với user
- [x] Viết spec chi tiết + tóm tắt design

## Phase 1 — Backend
- [x] Tạo `app/Console/Commands/NotifySupplyContractExpiration.php`
  - [x] Hằng `AREA_DEPARTMENTS` + `DAYS_BEFORE` + `RECEIVER_STATUSES`
  - [x] Options `--dry-run`, `--days=*`
  - [x] Query HĐ theo mốc ngày + `whereHas('customer')` lấy `customer_area_id` sống
  - [x] Loại HĐ đã đề xuất đủ bằng `fullyProposedContractIds()` (gọi 1 lần/lượt chạy)
  - [x] Lấy người nhận theo `employee_infos.department_id` + `status ∈ {1,2}`, cache theo địa bàn
  - [x] Gửi bằng `EmployeeInfoService::sendToAllContractNotification()` (console-safe)
  - [x] Log warning khi phòng không tồn tại / không có NV
- [x] Thêm lịch `dailyAt('08:30')` vào `app/Console/Kernel.php:36-37`
- [x] `php -l` sạch + `php artisan list` thấy `supply:notify-contract-expiration`

## Phase 2 — Kiểm thử (trên `thanhan_stag_07052026`)
- [x] `--dry-run` mặc định → 0 HĐ (không HĐ nào rơi đúng mốc 30/15/7/1 hôm nay)
- [x] `--dry-run --days=-53 --days=-55 --days=-21 --days=221` → đúng 2 HĐ Miền Bắc
- [x] Nhánh loại trừ **đã đề xuất đủ**: `HD-194/2026` (id 222, hết hạn 30/09, còn 6 ngày) nằm
      trong `fullyProposedContractIds() = [220,221,222]` → **không** bị nhắc ✓
- [x] Nhánh loại trừ **Miền Trung**: `HD-159/2026`, `HD-150/2026` (area 2) không vào danh sách ✓
- [x] Nhánh **Miền Nam thiếu phòng**: `HD-185/2026` (id 206, area 3) → log warning
      `khong co nhan su nhan {department_ids:[103,106]}`, bỏ qua, không lỗi ✓
- [x] Đối chiếu người nhận: 12 NV phòng 88 `status=1` — khớp 100% với SQL tay (danh sách
      "được lọc mà không nhận" = rỗng)
- [x] Gửi thật `--days=-21` → `notifications` 1208 → 1220, payload đúng `url`/`title`/`type`/`id`
- [x] Dọn dữ liệu test: xóa 12 `notifications` + 24 `jobs` (12 `SendNotification` +
      12 `BroadcastNotificationCreated`) → về đúng 1208 bản ghi ban đầu

## Phase 3 — Bàn giao
- [x] Báo user kết quả + việc cần làm trước khi lên production

### Checkpoint — 2026-09-24 12:00
Vừa hoàn thành: code + test xong toàn bộ Phase 1 & 2, đã dọn dữ liệu test trên DB dev.
Đang làm dở: không có.
Bước tiếp theo: user test UI trên môi trường có phòng ban mới (`103`/`106`), sau đó deploy —
nhớ chạy lại cron/supervisor để `Kernel::schedule` nạp lịch mới.
Blocked: không có. (Lưu ý: chỉ sửa BE, **không cần build lại client**.)

## Ghi chú vận hành

- **Không cần migration, không cần build FE.** Chỉ 1 file BE mới + 1 dòng `Kernel.php`.
- **DB dev lệch production:** `.env` cắm `thanhan_stag_07052026` chưa tách phòng Cung ứng
  HN/HCM → nhánh Miền Nam chỉ test được trên môi trường có `departments` 103/106.
- Muốn test không cần chờ tới ngày: `php artisan supply:notify-contract-expiration --dry-run --days=<N>`
  (nhận cả số âm để bắt HĐ đã quá hạn).

## Ngoài phạm vi / nợ

- Deep-link thông báo → HĐ cụ thể: màn `/supply/contract_render` không đọc `$route.query`.
- `quotations:notify-expiration` chưa từng chạy được (sai tên command + typo `whewre`) —
  xem §8 spec. Chưa sửa, chờ user quyết.
