# Design — Danh mục Lý do thất bại nhu cầu khách hàng (Redmine #11465)

> Feature: `demand-failure-reason-catalog` · @junfoke · Nhánh `task_11465`
> **Tách từ `task_11377`** (chuỗi 11386 → 11377 → 11465). Merge phải theo đúng thứ tự đó.

## Mục tiêu

Danh mục để Sales chọn lý do khi **đóng nhu cầu khách hàng** thủ công (#11386 Phần 3).
Trước đây định chốt cứng 4 lựa chọn trong code — khách đã mở task riêng nên làm danh mục thật.

## Cấu trúc dữ liệu (theo spec)

| Trường | Kiểu | Ràng buộc |
| --- | --- | --- |
| Nguyên nhân thất bại | nvarchar(255) | **Bắt buộc**, **unique** |
| Mô tả | nvarchar(1000) | Không bắt buộc — hướng dẫn cụ thể cho Sales khi chọn |
| Trạng thái | 1 Hoạt động / 2 Khoá | theo chuẩn danh mục |
| Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật | tự động | |

**Không có cột Mã** — spec không yêu cầu. Theo skill `list-page` §3a: bảng không có mã thì cột định
danh là **TÊN**, và tên là link mở popup Xem.

## Quyết định

1. **Bám khuôn danh mục `internal-business-scopes`** — màn danh mục mới nhất, đã theo đúng quy ước
   hiện hành (modal Thêm/Sửa/Xem, khoá/mở khoá, `V2BaseMetaInfo`, cờ `is_can_edit` / `is_can_delete`).
   Bỏ phần Mã và phần Import/Export (spec #11465 không yêu cầu).
2. **API danh sách lý do đang hoạt động** (`getAll`) phục vụ popup đóng nhu cầu của #11386 Phần 3.
3. **Không xoá được lý do đã dùng** — nhu cầu đã đóng trỏ tới nó; xoá là mất lý do của bản ghi cũ.
   Chỉ cho Khoá để thôi hiện ở dropdown.

## Ghi chú kỹ thuật

- Skill `list-page` nhắc bộ dùng chung `CatalogHistoryModal` + trait `LogsCatalogHistory` + bảng
  `catalog_histories`, nhưng nhánh `tpe` **CHƯA CÓ** 3 thứ đó (skill đi trước code). Làm theo đúng
  cách các màn danh mục đang chạy.
- Tên bảng: `customer_demand_failure_reasons`.
