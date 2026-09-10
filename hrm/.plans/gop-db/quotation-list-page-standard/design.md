# Chuẩn hoá màn Danh sách báo giá theo skill `list-page`

- **Người phụ trách**: @khoipv · **Nhánh**: `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn hình**: `/assign/quotations`
- **Spec chi tiết**: `docs/superpowers/specs/gop-db/2026-09-07-quotation-list-page-standard-design.md`
- **Tiếp nối**: loạt 15 màn `assign-list-page-standard` · `project-phase` · `prospective-project` ·
  `product-project` · `pricing-request` · `contract` · `request-solution` · `solution-module` · `bom-list`

## Phạm vi

1. Bộ lọc → `V2BaseSmartFilterPanel` + schema `filterFields` (12 mục / 15 ô), giữ nguyên 3 select2
   remote (Dự án · Giải pháp · Khách hàng) và cascade Dự án → Giải pháp → Version.
2. Tách cột gộp "Mã BG • BOM" (mã + tên BOM + dòng phụ YCBG + **6 icon thao tác**) thành
   **Mã báo giá** (link) + **BOM list** + **Mã YCBG**; **cột Hành động ở cuối bảng**:
   Sửa · Xóa (2 nút chính) + Sao chép · In · Lịch sử phê duyệt trong `⋮`. Bỏ "Xem chi tiết".
3. Bảng **20 cột**, bật `fixed-layout`, khai đủ `width` = `minWidth`; thêm Giai đoạn dự án ·
   Người cập nhật · Ngày cập nhật.
4. `columnCustomizationMixin` + **chức năng Xuất Excel danh sách MỚI** (màn chỉ có xuất chi tiết
   1 báo giá, chưa từng xuất danh sách) qua popup Chọn trường + `DynamicExport`.
5. BE: whitelist sắp xếp + chốt `id desc`; **6/7 mã màu trạng thái** (và cả bộ báo giá tổng) quy về
   bảng 9 mã chuẩn; `updated_at` trả thô → format; thêm `updater_name`, `approval_level_color`,
   4 khoá phẳng cho file Excel.

## Lỗi CÓ SẴN sửa kèm

| Lỗi | Hậu quả |
| --- | --- |
| `handleReset()` gọi `this.loadData()` — hàm **không tồn tại** trên màn (tên đúng `fetchData`) | Bấm **Làm mới** ném TypeError: ô lọc bị xoá nhưng danh sách giữ nguyên kết quả cũ. **Cùng một lỗi copy-paste với màn `/assign/pricing-requests`** |
| `updated_at` trả THÔ từ Resource | Cột "Ngày cập nhật" (nếu bật) hiện chuỗi ISO `2026-07-27T04:29:05.000Z` |
| Cấp duyệt dùng 3 class CSS tự khai `.badge-level-*` nền đậm chữ trắng | Nền đậm là ngôn ngữ của NÚT BẤM (skill mục 3c-2); nay dùng `V2BaseBadge` + màu BE trả |

## Quyết định đã chốt

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã báo giá**, link `nuxt-link`; **phân nhánh** báo giá tổng (`/assign/summary-quotations/{id}`) vs báo giá thường |
| Hành động dòng | Sửa · Xóa chính; Sao chép · In · Lịch sử phê duyệt vào `⋮`; bỏ "Xem chi tiết" |
| Đồng bộ ERP | Đổi từ icon tự chế sang `V2BaseBadge` (Đã đồng bộ / Thất bại); nút "Thử lại" vốn đã bị `v-if="false"` nên gỡ khỏi ô |
| Mặc định cột hiển thị | **Hiện HẾT** (theo chốt của loạt màn trước) |
| Hành động "Lịch sử" | **Đã có sẵn** (Lịch sử phê duyệt) — không phải nợ như các màn khác |

## File chính

- BE: `Modules/Assign/Entities/Quotation.php` · `Modules/Assign/Services/QuotationService.php` ·
  `Modules/Assign/Transformers/QuotationResource.php` ·
  `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` · `Modules/Assign/Routes/api.php` ·
  `app/ExcelExport/ExportColumnRegistry.php`
- FE: `pages/assign/quotations/index.vue`

Không migration, không quyền mới.
