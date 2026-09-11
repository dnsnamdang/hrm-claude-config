# Chuẩn hoá màn Danh sách hợp đồng theo skill `list-page`

- **Người phụ trách**: @khoipv · **Nhánh**: `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn hình**: `/assign/contracts`
- **Spec chi tiết**: `docs/superpowers/specs/gop-db/2026-09-07-contract-list-page-standard-design.md`
- **Tiếp nối**: loạt 15 màn `assign-list-page-standard` · `project-phase` · `prospective-project` ·
  `product-project` · `pricing-request`

## Phạm vi

1. Bộ lọc → `V2BaseSmartFilterPanel` + schema `filterFields` (5 mục / 8 ô), bỏ `title`/`subtitle`,
   placeholder theo công thức "Chọn <trường>".
2. **Cột Hành động ở cuối bảng** (`V2BaseRowActions`): Sửa · Xóa · Duyệt · Thanh lý. Bỏ icon
   "Xem chi tiết" nhét cạnh mã; **Mã hợp đồng thành `nuxt-link`** vào màn chi tiết.
3. Bảng **15 cột**, bật `fixed-layout`, khai đủ `width` = `minWidth`; thêm 5 cột mới
   (Ngày hết hiệu lực · Giá trị phát sinh · Người tạo · Ngày tạo · Người/Ngày cập nhật).
4. `columnCustomizationMixin` (màn này **chưa từng có** cấu hình cột) + popup **Chọn trường xuất
   file** + **chức năng Xuất Excel mới** (màn này **chưa từng có** xuất file).
5. BE: cờ thao tác `is_can_*` (quyền AND trạng thái) lấy từ Entity — cùng nguồn với `ContractService`;
   10 mã màu trạng thái quy về bảng 9 mã chuẩn; chốt `id desc` khi sắp xếp; ngày format ở BE.

## Quyết định đã chốt

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã hợp đồng**, link `nuxt-link` vào `/assign/contracts/{id}` |
| "Duyệt" / "Thanh lý" trên dòng | Khai `to` → **điều hướng sang chi tiết**, không xử lý tại chỗ (skill mục 1: người duyệt phải đọc nội dung trước khi quyết) |
| "Không duyệt" | **Không đưa vào danh sách** (skill mục 1) — chỉ có ở màn chi tiết |
| Hành động Xóa | Thêm ở danh sách, gate bằng `is_can_delete` (quyền `Xóa hợp đồng` AND trạng thái Đang tạo) |
| Bộ lọc trạng thái | Liệt kê **đủ 10 trạng thái** — bản cũ chỉ có 4 nên không lọc được các bước xuất hàng / quyết toán dù dữ liệu thật đang có cả 10 |
| Mặc định cột hiển thị | **Hiện HẾT** (theo chốt của loạt màn trước) |
| Hành động "Lịch sử" | **Chưa làm** — module Assign chưa có `LogsCatalogHistory` (hợp đồng có bảng `contract_histories` riêng, dùng ở màn chi tiết) |

## Điểm đáng chú ý

- **Cờ thao tác gộp QUYỀN + TRẠNG THÁI ở máy chủ.** `ContractResource` hỏi 4 quyền đúng **một lần
  cho cả trang** (biến static), không phải 4 lượt truy vấn mỗi dòng. Điều kiện trạng thái lấy từ
  Entity (`isEditableStatus` / `is_can_delete` / `isApprovableStatus` / `isLiquidatableStatus`) —
  chính là điều kiện `ContractService` chặn ở máy chủ, nên nút trên giao diện và luật nghiệp vụ
  không thể lệch nhau. Đối chiếu với màn chi tiết: điều kiện hiện nút của 2 màn **khớp nhau** (mục 7.2).
- **"Làm mới" gọi API 2 lần** ở bản cũ (vừa để deep watcher bắn, vừa tự gọi `fetchData`) — đã chặn
  bằng cờ `_restoringFilters`.

## File chính

- BE: `Modules/Assign/Entities/Contract/Contract.php` ·
  `Modules/Assign/Transformers/ContractResource.php` ·
  `Modules/Assign/Http/Controllers/Api/V1/ContractController.php` · `Modules/Assign/Routes/api.php` ·
  `app/ExcelExport/ExportColumnRegistry.php`
- FE: `pages/assign/contracts/index.vue`

Không migration, không quyền mới.
