# Chuẩn hoá màn Danh sách BOM List theo skill `list-page`

- **Người phụ trách**: @khoipv · **Nhánh**: `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn hình**: `/assign/bom-list`
- **Spec chi tiết**: `docs/superpowers/specs/gop-db/2026-09-07-bom-list-list-page-standard-design.md`
- **Tiếp nối**: loạt 15 màn `assign-list-page-standard` · `project-phase` · `prospective-project` ·
  `product-project` · `pricing-request` · `contract` · `request-solution` · `solution-module`

## Phạm vi

1. Bộ lọc → `V2BaseSmartFilterPanel` + schema `filterFields` (10 mục / 12 ô), giữ nguyên cascade
   Dự án TKT → Giải pháp → Hạng mục và select2 remote Khách hàng.
2. Tách cột gộp "Mã • Tên BOM" (mã + tên + 2 dòng phụ + tối đa 6 icon thao tác) thành **Mã BOM**
   (link) + **Tên BOM**; **cột Hành động ở cuối bảng**: Sửa · Xóa (2 nút chính) + Sao chép · In ·
   Lịch sử trong menu `⋮`. Bỏ hành động "Xem chi tiết".
3. Bảng **17 cột**, bật `fixed-layout`, khai đủ `width` = `minWidth`; tách 3 thông tin vốn nằm
   trong dòng phụ / ô gộp thành cột riêng: **Phòng của người tạo**, **Người cập nhật**, **Ngày cập nhật**.
4. `columnCustomizationMixin` + **popup "Chọn trường xuất file"** thay cho cách xuất cũ.
5. BE: whitelist sắp xếp + chốt `id desc`; **6/6 mã màu trạng thái** quy về bảng 9 mã chuẩn;
   ngày bỏ giây; cờ `is_can_edit` / `is_can_delete`; export chuyển `DynamicExport` + registry.

## Điểm đáng chú ý

- **Xuất Excel trước đây không hỏi user chọn cột**: FE tự dựng JSON `columns` từ các cột đang hiện
  rồi gửi xuống, blade `exports.bom_list_list` phải **tự map từng khoá cột của bảng**
  (`code_name`, `project`, `solution`…) — đổi tên cột trên lưới là file ra rỗng ở đúng cột đó.
  Nay dùng `ExportColumnRegistry` + `DynamicExport` như mọi màn khác, key = key của Resource.
- **Ngày tạo / cập nhật hiện cả giây** (`Helper::formatDateTime()` mặc định `d/m/Y H:i:s`).
- **Bấm sort và "Làm mới" gọi API 2 lần** (tự gọi + deep watcher).
- **2 request `per_page=10000`** (dự án TKT + giải pháp) chạy ngay khi vào màn dù panel lọc đang
  thu gọn → hoãn tới khi mở panel (vẫn nạp sớm nếu bộ lọc đã lưu có dự án/giải pháp, để hiện đúng nhãn).
- Màn này **đã có sẵn hành động "Lịch sử"** (`BomListLogModal`) — khác 8 màn `assign/*` trước đó
  đều phải bỏ qua vì module Assign chưa có `LogsCatalogHistory`.

## Quyết định đã chốt

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã BOM**, link `nuxt-link` vào `/assign/bom-list/{id}` |
| Hành động dòng | Sửa · Xóa chính; Sao chép · In BOM List · Lịch sử vào `⋮`; bỏ "Xem chi tiết" |
| Điều kiện Sửa / Xóa | Cờ BE `is_can_edit` / `is_can_delete` (khớp `BomListService::update/destroy`), Xóa còn AND quyền "Tạo BOM List" như bản cũ |
| Mặc định cột hiển thị | **Hiện HẾT** (theo chốt của loạt màn trước) |

## File chính

- BE: `Modules/Assign/Entities/BomList.php` · `Modules/Assign/Services/BomListService.php` ·
  `Modules/Assign/Transformers/BomListResource/BomListListResource.php` ·
  `Modules/Assign/Http/Controllers/Api/V1/BomListController.php` ·
  `app/ExcelExport/ExportColumnRegistry.php`
- FE: `pages/assign/bom-list/index.vue`

Không migration, không quyền mới.
