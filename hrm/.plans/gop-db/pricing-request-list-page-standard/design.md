# Chuẩn hoá màn Danh sách yêu cầu xây dựng giá theo skill `list-page`

- **Người phụ trách**: @khoipv · **Nhánh**: `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn hình**: `/assign/pricing-requests` (+ màn chi tiết `/{id}` và màn sửa `/{id}/edit` sửa kèm)
- **Spec chi tiết**: `docs/superpowers/specs/gop-db/2026-09-07-pricing-request-list-page-standard-design.md`
- **Tiếp nối**: loạt 15 màn `assign-list-page-standard` · `project-phase` · `prospective-project` · `product-project`

## Mục tiêu

Đưa màn về đúng khuôn `list-page`, đồng thời **sửa 3 lỗi có sẵn làm chức năng chết** phát hiện
trong lúc rà (chi tiết ở mục dưới).

## Phạm vi

1. Bộ lọc → `V2BaseSmartFilterPanel` + schema `filterFields` (5 ô), bỏ `title`/`subtitle`,
   placeholder theo công thức "Chọn <trường>".
2. Bảng 16 cột, bật `fixed-layout`, khai đủ `width` = `minWidth`; ô tham chiếu (BOM list, Dự án TKT)
   ghép `MÃ - Tên` cùng 1 dòng.
3. **Cột Hành động ở cuối bảng** (`V2BaseRowActions`): Sửa · Xóa · Tạo báo giá. Bỏ hành động "Xem"
   và gỡ dãy icon nhét dưới Mã YCBG.
4. **Mã YCBG thành `nuxt-link` vào màn chi tiết thật** (trước là `<a href="#">` mở popup — không
   mở được tab mới, lại trùng chức năng với nút "Xem chi tiết" ngay bên dưới).
5. Thêm cột **Ngày tạo · Người cập nhật · Ngày cập nhật**; ngày định dạng ở BE (`d/m/Y H:i`).
6. `columnCustomizationMixin` + popup **Chọn trường xuất file** + **chức năng Xuất Excel mới**
   (màn này trước đây KHÔNG có xuất file).
7. BE: whitelist sắp xếp + chốt `id desc`; tìm nhanh thêm Người yêu cầu; 6 mã màu trạng thái quy về
   bảng 9 mã chuẩn; khoá phẳng cho file Excel.

## 3 lỗi CÓ SẴN sửa kèm (đều làm chức năng chết, không phải lỗi hiển thị)

| Lỗi | Hậu quả |
| --- | --- |
| `handleReset()` gọi `this.loadData()` — hàm KHÔNG tồn tại (tên đúng `fetchData`) | Bấm **Làm mới** ném TypeError: ô lọc bị xoá nhưng danh sách giữ nguyên kết quả cũ |
| FE tính `canEdit` bằng `item.created_by` — khoá mà Resource **không hề trả về** | Nút **Sửa nháp** không bao giờ hiện ở danh sách |
| Màn chi tiết + màn sửa đọc `$store.state.auth?.user?.id` — store **không có khoá đó** (module `auth` chỉ khai `currentUser`) | Màn **Sửa khoá toàn bộ form** và báo "Yêu cầu đã gửi, không thể sửa" ngay cả với phiếu nháp của chính mình → không sửa được phiếu nháp bằng bất kỳ đường nào |

Cách sửa chung: máy chủ trả cờ `is_can_edit` / `is_can_delete` tính từ
`PricingRequest::isDraftOwnedByCurrentUser()` — **một nguồn duy nhất** dùng chung với
`PricingRequestService::ensureDraftAndOwner()`, cho cả 3 màn.

## Quyết định đã chốt

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã YCBG**, link `nuxt-link` vào `/assign/pricing-requests/{id}` |
| Popup chi tiết cũ | Bỏ khỏi màn danh sách (component vẫn dùng ở 3 màn khác) |
| Hành động Xóa | **Thêm mới** ở danh sách + chi tiết — endpoint `DELETE` đã có sẵn nhưng FE chưa bao giờ gọi |
| Mặc định cột hiển thị | **Hiện HẾT** (theo chốt của loạt màn trước) |
| Hành động "Lịch sử" | **Chưa làm** — module Assign chưa có `LogsCatalogHistory` |

## ⚠️ Việc CẦN USER QUYẾT (chưa sửa)

Người có quyền **"Xây dựng giá bán theo công ty/phòng"** không nhìn thấy phiếu **nháp của chính
mình**: nhánh phạm vi trong `PricingRequestController::index()` thay hẳn điều kiện "của tôi" bằng
`whereIn('status', [2..6])`, mà nháp là status 1. Người đó tạo YCBG xong sẽ mất luôn phiếu khỏi
danh sách. Sửa thì chỉ cần thêm `orWhere('created_by', auth()->id())` vào nhóm ngoài, nhưng đó là
**đổi phạm vi dữ liệu** nên để user quyết.

## File chính

- BE: `Modules/Assign/Http/Controllers/Api/V1/PricingRequestController.php` ·
  `Modules/Assign/Entities/PricingRequest.php` · `Modules/Assign/Transformers/PricingRequestResource.php` ·
  `Modules/Assign/Transformers/DetailPricingRequestResource.php` · `Modules/Assign/Routes/api.php` ·
  `app/ExcelExport/ExportColumnRegistry.php`
- FE: `pages/assign/pricing-requests/index.vue` · `_id/index.vue` · `_id/edit.vue`

Không migration, không quyền mới.
