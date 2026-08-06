# Design — Danh mục serial thiết bị làm dịch vụ (CSKH)

**Người phụ trách:** @junfoke — 2026-08-06
**Nhánh:** `gop_db`
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-08-06-customer-care-serial-catalog-design.md`

## Mục tiêu

Chuyển màn **Danh mục serial thiết bị làm dịch vụ** từ ERP sang HRM, phân hệ **CSKH**
(`/customer-care/serials`). Là màn danh mục thứ 5 của phân hệ này.

## Scope

**Có:** 1 màn danh sách read-only + Xuất Excel (dựng ở FE), 7 cột, 6 bộ lọc, 1 quyền mới (id 1126),
2 route `/v1/customer-care/serials{,/filter-options}`, điền link vào menu CSKH.

**Không:** mọi thao tác ghi serial (thêm/sửa/đổi/xóa) — chúng thuộc màn *Quản lý khách hàng →
tab Trang thiết bị*, HRM đã có bản tương đương trong `MasterData/CustomerManagerService`.

## Quyết định chính

1. **Read-only + thêm Xuất Excel** — ERP không có nút export, HRM thêm cho đồng bộ với 4 danh mục
   CSKH đã port. **Dựng file Ở FE** (ExcelJS + fetch theo lô 5000), không có route export ở BE:
   bảng 21.632 dòng, BE dựng mất ~25 giây → timeout khi lên server; FE mất 14 giây và không
   request nào chạm ngưỡng.
2. **7 cột / 6 bộ lọc** (ERP hiển thị 5 cột / 4 lọc) — bổ sung Người tạo, Người cập nhật,
   Ngày cập nhật. `Serial::searchByFilter` của ERP đã hỗ trợ sẵn 2 bộ lọc này nhưng blade không dùng.
3. **1 quyền `Xem danh mục serial thiết bị làm dịch vụ`** (id 1126, group
   `Danh mục dịch vụ bảo dưỡng`, type 24) — ERP không gắn quyền màn này. Khai trong
   `PermissionsTableSeeder`, không tạo migration.
4. **Dùng lại model `App\Models\TpSerial`**, không tạo Entity trùng bảng `serials`.
5. **Dropdown Người tạo/Người cập nhật lấy distinct từ bảng `serials`**, KHÔNG dùng
   `human/employee-infos/list-for-select` — endpoint đó trả id `employee_infos`, lệch hệ id với
   `serials.created_by` (= `employees.id`).
6. **FE dùng V2Base** như các danh mục CSKH đã chuyển.

## Gotcha

- `serials.created_by/updated_by` là **integer** (khác `note_maintenances` dùng varchar).
- `status`: **1 = Đang sử dụng, 2 = Ngưng sử dụng** (khác `costs` dùng 1/0).
- ERP `searchData` gọi `employee_update->info->fullname` không guard null → HRM phải null-safe.
- Bẫy sẵn có ở ERP (không sửa trong feature này): `update/change/delete` gọi
  `checkExistSerial()` nhưng bỏ qua giá trị trả về → không chặn được serial đã vào luồng.
- 4 bẫy phân trang V2 + bẫy `key` cột sort phải trùng tên trường BE.
- DB thực tế có **13 bản ghi `status` ngoài 1/2** (12 dòng `= 3`, 1 dòng `= 0`). Đang giữ đúng
  hành vi ERP: hiển thị "Ngưng sử dụng" nhưng bộ lọc gửi `status = 2` nên không bắt được
  → **chờ user chốt** có đổi thành `status != 1` không.

## Việc còn treo

- User rà bằng mắt `/customer-care/serials`.
- Chốt cách lọc cho 13 bản ghi `status` 0/3.
- Chưa đối chiếu bằng mắt với màn ERP (ERP local không chạy) — đã đối chiếu bằng SQL thay thế.
- 4 danh mục CSKH port trước vẫn xuất Excel ở BE, nên rà lại nếu dữ liệu phình to.
