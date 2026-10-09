# Design — YCXH: Xuất Excel + Cài đặt bộ lọc

**Feature:** Bổ sung 2 chức năng còn thiếu cho màn **Yêu cầu xuất hàng** (`/finance/product-export-requests`, module Assign): **Xuất Excel toàn bộ danh sách** và **Cài đặt bộ lọc**.

**Chuẩn tham chiếu (user chốt):** màn `/finance/prepick-transfer-requests` (module Finance) — bê nguyên pattern sang.

## Hiện trạng
- FE `pages/finance/product-export-requests/index.vue` đang dùng `V2BaseFilterPanel` tĩnh (không có popup cài đặt bộ lọc) và toolbar chỉ có "Tạo mới" + nút cấu hình cột. THIẾU: Xuất Excel + Cài đặt bộ lọc.
- BE `Modules/Assign/.../ProductExportRequestController` có `index()` (query inline + scope 4 cấp) nhưng CHƯA có `export()`.

## Quyết định đã chốt
- **Cài đặt bộ lọc**: đổi `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (`table="finance_product_export_requests"` + `:filter-fields="filterFields"`). Popup "Cài đặt bộ lọc" do chính `V2BaseSmartFilterPanel` render (nút bánh răng ở header) — lưu theo user ở bảng `filter_customizations`. KHÔNG cần migration (bảng + API `human/filter-customizations` đã có, 86 màn dùng).
- **Xuất Excel**: BE trả JSON thô `{rows, filter_text}` theo đúng bộ lọc + phạm vi quyền (KHÔNG phân trang); FE dựng file `.xlsx` bằng ExcelJS (đúng convention — như prepick). Popup chọn trường dùng `components/modal/export-fields-modal.vue`. Nút "Xuất Excel" = `V2BaseButton secondary status="success"`, icon `ri-file-excel-2-line` (theo màn chuẩn prepick — bám chuẩn Finance thay vì `ri-download-line` của button-convention để đồng bộ cụm màn Tài chính).
- **Icon nút xuất**: `ri-file-excel-2-line` (khớp màn chuẩn user chỉ định), không dùng `ri-download-line`.
- **Cột file Excel** (STT prepend tự động): Mã phiếu, Loại, Số hợp đồng, Khách hàng, Phòng ban, Người tạo, Ngày tạo, **Giá trị** (SỐ THẬT + numFmt `#,##0`, không đổ chuỗi), Trạng thái, Người duyệt, Ngày duyệt.
- **DRY BE**: tách bộ lọc của `index()` thành `applyFilters($query, $request)` dùng chung cho `index()` + `export()`. `export()` build rows thủ công (KHÔNG qua Resource) để tránh N+1 do gọi accessor `canEdit/canCancel/canDelete` trên toàn bộ dòng.
- **Route**: thêm `GET /assign/product-export-requests/export` khai TRƯỚC `/{id}` (route động nuốt route tĩnh).

## File đụng tới
- BE: `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` (tách `applyFilters` + thêm `export`), `Modules/Assign/Routes/api.php` (thêm route).
- FE: `pages/finance/product-export-requests/index.vue` (swap panel + filterFields + nút + modal + method), thêm `pages/finance/product-export-requests/components/export-excel.js`.

## Tái dựng / kiểm thử
- FE: mở màn → mở "Cài đặt bộ lọc" bật/tắt/kéo trường → reload thấy giữ cấu hình. Bấm "Xuất Excel" → chọn trường → tải file, mở kiểm cột "Giá trị" là số (SUM được).
