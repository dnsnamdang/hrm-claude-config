# Plan — Serial hiển thị mã khách hàng LIVE (Cách A)

@junfoke · Repo `TanPhatDev` · nhánh `local_tri`

## Vấn đề
Màn "Danh sách Serial thiết bị làm dịch vụ" (`/admin/sale/serials`) hiển thị mã khách **lưu cứng** trên bảng `serials` (`customer_code`, `customer_name`). Khi khách **đổi mã**, serial vẫn hiện mã CŨ → tìm trong DM không ra.

Ca thật: serial TPE.5356 → customer_id 24178. Khách đổi mã `29HNOLBILBI-77` (cũ, kẹt trên serial) → `29TPHPLO-113` (mới, trong DM). Tìm DM theo mã cũ = rỗng, gây tưởng mất khách.

## Cách A (đã chốt với user)
Màn Serial hiển thị mã/tên khách **live** từ bảng `customers` (join `customer_id`), fallback về giá trị lưu cứng nếu khách bị xoá (serial mồ côi).

## Tasks
- [x] Thêm quan hệ `customer()` belongsTo vào `app/Model/Common/Serial.php`
- [x] `Serial::searchByFilter` eager load `customer` (select id, code, fullname) — tránh N+1
- [x] `SerialController@searchData` đổi `editColumn('customer')`: dùng `optional($serial->customer)->code ?? $serial->customer_code` (+ fullname tương tự)
- [x] `php -l` sạch 2 file
- [x] Verify tinker: serial TPE.5356 stored=`29HNOLBILBI-77` → LIVE=`29TPHPLO-113 - ĐỖ TUẤN ANH`
- [ ] User test browser trên dev + push

## Ghi chú
- Chỉ sửa HIỂN THỊ danh sách. KHÔNG động dữ liệu `serials` (không migrate). Mã cũ vẫn lưu để truy vết.
- Bộ lọc "Khách hàng" lọc theo `customer_id` — không ảnh hưởng.
- Nếu sau này cần đồng bộ triệt để (in ấn/lịch sử cũng lấy live, hoặc đổi mã KH tự cập nhật denormalized) → task riêng.

## Checkpoint — 2026-08-27
Vừa hoàn thành: Cách A xong (2 file), lint sạch, verify tinker đúng ca TPE.5356.
Bước tiếp theo: User test browser + push. Sau đó quay lại task mã NV báo cáo (dùng HrmEmployeeService).
