# Khôi phục Quận/Huyện theo quốc gia (địa chỉ)

Người phụ trách: @junfoke — Bắt đầu 2026-09-08 — Nhánh: `tpe` (cả `hrm-api` và `hrm-client`)

## Bối cảnh

Việt Nam bỏ cấp huyện nên HRM đã gỡ Quận/Huyện khỏi mọi màn địa chỉ. Nhưng địa chỉ của các
nước khác **vẫn có cấp quận/huyện**, nên gỡ hẳn là sai. ERP không gỡ mà **ẩn theo quốc gia**.

## Quy tắc chốt (bê từ ERP)

`nation_id = 1` là Việt Nam.

| Quốc gia | Luồng chọn |
| --- | --- |
| Việt Nam | Quốc gia → Tỉnh → **Xã (lọc theo `province_id`)** → Thôn |
| Nước khác | Quốc gia → Tỉnh → **Quận/Huyện** → **Xã (lọc theo `district_id`)** → Thôn |

- Ô Quận/Huyện **ẩn hẳn (`v-if`)** khi là Việt Nam — không disable.
- Đổi Quốc gia → xoá tỉnh/quận/xã/thôn. Đổi Tỉnh → xoá quận/xã/thôn. Đổi Quận → xoá xã/thôn.
- Mở Sửa bản ghi cũ có `district_id`: load districts theo tỉnh trước, rồi wards theo quận —
  nếu không sẽ mất giá trị đang chọn.
- Hằng số `NATION_VN_ID` để ở `utils/address.js`, không rải số `1` khắp nơi như ERP.

Nguồn tham chiếu ERP: `TanPhatDev/app/Http/Controllers/Common/LocationController.php:26-42`
và `TanPhatDev/resources/views/partials/suppliers/supplierForm.blade.php:244-345`.

## Phạm vi (user chốt 2026-09-08)

1. **Danh mục Quận/Huyện** — dựng lại màn đã bị bỏ (làm TRƯỚC). Copy pattern
   `pages/human/wards/` (nhánh `tpe` dùng style cũ `b-table` + `Select2`, KHÔNG copy bản V2
   ở nhánh `gop_db`).
2. **Khách hàng (Giao việc, bản V2)** — `components/assign-components/customer/CustomerForm.vue`,
   gồm cả khối Địa điểm giao hàng.
3. **Khách hàng (Nhân sự, bản cũ)** — `components/human-components/customer/CustomerForm.vue`.
4. **Hồ sơ nhân sự** — 8 file `employee_info/*` (Form/Edit/Show × chính / my-info-request /
   request-update), cả khối Hộ khẩu và Chỗ ở.

**Ngoài phạm vi**: màn Công ty (`company/CompanyForm.vue`), dữ liệu danh mục (dùng data cũ có sẵn).

## Quyết định

- **Hồ sơ nhân sự không thêm cột `nation_id`**: `employee_infos` chỉ có `national` (quốc tịch,
  text). Quốc gia của địa chỉ **suy ra từ tỉnh đang chọn** (API trả kèm `nation_id`).
- **`districts` thiếu cột `status` / `created_by` / `updated_by`** → viết migration bổ sung
  (`status` mặc định 1) để màn danh mục có Khoá/Mở khoá + cột Người cập nhật như các danh mục
  anh em. **KHÔNG tự chạy migrate** — user tự chạy.
- BE module Giao việc **đã có sẵn đủ endpoint** (`/assign/customers/districts|provinces|wards`,
  đọc DB ERP `mysql2`) — chỉ FE chưa dùng. Không sửa BE Assign.
- `AddressController` (dùng chung Nhân sự): khôi phục `level = 2`; `level = 3` nhận thêm
  `district_id` (tương thích ngược); `level = 1` trả kèm `nation_id`.

## Chi tiết

Xem `docs/superpowers/specs/2026-09-08-address-district-by-nation-design.md`.
