# Nhóm khách hàng trên form KH — Tóm tắt

- Nhánh: `gop_db` · Người làm: @khoipv · Ngày: 2026-08-10
- Spec: `docs/superpowers/specs/gop-db/2026-08-10-customer-form-group-design.md`

## Mục tiêu

Bổ sung trường **Nhóm khách hàng** vào form khách hàng HRM (`/assign/customers/add` và các màn dùng
chung form), tương đương ERP `partials/customers/customerForm.blade.php`.

## Quyết định

| # | Quyết định |
| --- | --- |
| 1 | **Chọn nhiều**, **không bắt buộc** — bám đúng ERP (`ng-model="customer.groups" multiple`, ERP không có rule required) |
| 2 | Không thêm nút "tạo nhanh nhóm" như ERP — HRM chưa có màn quản lý nhóm KH, để sau |
| 3 | Sửa ở component dùng chung `CustomerForm.vue` → 5 màn cùng có: add · edit · xem chi tiết (readonly) · quản lý KH · modal thêm nhanh |
| 4 | BE **không phải sửa luồng ghi**: `CustomerService::save()` đã sync pivot `customer_has_groups`, `show()` đã trả `group_ids` |

## Lỗi có sẵn được sửa kèm

`syncErpSubEntities()` gọi `syncGroups($tp, (array) ($request->groups ?? []))` **vô điều kiện** —
xoá hết pivot rồi ghi lại. Form HRM trước đây **không hề gửi `groups`** ⇒ mỗi lần sửa khách hàng là
**xoá sạch nhóm KH** mà ERP đã gán. Đã dựng test tái hiện (mục 4 của kịch bản verify).

Vì vậy `buildPayload()` **luôn** gửi `groups`, kể cả khi người dùng không đụng tới ô này.

## Phạm vi

Không migration, không permission mới, không sửa `CustomerService`.
