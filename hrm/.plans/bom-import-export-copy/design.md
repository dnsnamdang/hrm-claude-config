# Design (tóm tắt): Import / Export / Sao chép BOM List

> Spec đầy đủ: `docs/superpowers/specs/2026-07-15-bom-import-export-copy-design.md`

- **Phụ trách**: @manhcuong
- **Ngày**: 2026-07-15
- **Màn hình**: Quản lý dự án TKT → BOM Giải pháp (`/assign/bom-list`)

## Mục tiêu

1. **Import** — siết validate theo đặc tả (hiện quá lỏng).
2. **Export** — xuất đúng mẫu, round-trip import lại được.
3. **Sao chép BOM** — làm mới hoàn toàn (chưa tồn tại).

## Hiện trạng

| Chức năng | Trạng thái |
|---|---|
| Import | **Đã có** nhưng lệch đặc tả (cột, validate, tự tạo master data ERP, dòng dịch vụ rơi sai bảng) |
| Export | **Đã có** (`BomExportModal` + `BomListExport`), cần đổi cột + bổ sung dịch vụ |
| Sao chép | **Chưa có gì** |

## 9 quyết định lớn

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Vị trí nút Sao chép | Chỉ trang **Danh sách BOM** → điều hướng trang Tạo mới đã điền sẵn. Bỏ "giữa các phiên bản giải pháp" |
| 2 | Bộ cột | **12 cột đúng file mẫu**; bỏ "Giá nhập", thêm "Ghi chú" |
| 3 | Master Data lạ | **Chặn + báo lỗi** (`autoCreate: true → false`) |
| 4 | UI "Chờ xác nhận" | **Modal riêng cho BOM**, không đụng `V2BaseImportModal` (11 màn khác dùng) — *lý do chi tiết bên dưới* |
| 5 | Đích import | **Ghi thẳng DB, replace-all** (giữ nguyên) |
| 6 | Dòng "Dịch vụ & Chi phí khác" | Ghi `bom_list_service_items`; đối chiếu **Tên hàng** với `costs.name`, không khớp → chi phí tự do (`cost_id=null`), không báo lỗi — *đính chính 2026-07-15, xem dưới* |
| 7 | STT nhiều cấp | **Giới hạn 2 cấp** + báo lỗi rõ (DB chỉ lưu được 2 cấp) |
| 8 | Nút Import màn Tạo mới | **Hiện + disabled + tooltip** thay vì ẩn |
| 9 | Route validate trùng | **Bỏ** `POST /import/validate-data` |

## 3 phát hiện quan trọng khi khảo sát

1. **Import đang tự tạo master data ERP** — `resolveLookupId(..., autoCreate: true)` (`BomListService.php:645-648`) âm thầm thêm Model/Thương hiệu/Xuất xứ/ĐVT lạ vào `product_models`/`brands`/`origins`/`units`. Đặc tả yêu cầu ngược lại → **đổi hành vi production**, cần báo user khi release.
2. **Dòng dịch vụ rơi sai bảng** — import ghi `product_type=2` vào `bom_list_products`, nhưng FE render khối "Dịch vụ & Chi phí khác" từ `bom_list_service_items` (`BomBuilderEditor.vue:987`); `mapProductsToGroups()` không lọc `product_type` → dòng dịch vụ hiện nhầm trong lưới Hàng hoá.
3. **`costs` ERP không có cột `code`** *(đính chính quyết định #6, phát hiện khi code Task 1-3)* — cột thật: `id, name, en_name, type, status, kind_of, rate_value_capital, revenue_calculation, vat_percent`. Code sẵn có match `costs` bằng **name** (`ErpCostController:33`, `QuotationErpSyncService:136`); quét 359 bảng ERP có cột `code` tìm `SRV-%`/`TEMP-SRV%` → 0 kết quả. Chốt lại: đối chiếu theo **tên**, không khớp → **chi phí tự do** (`cost_id=null`, không báo lỗi) — đối xứng với hàng hoá (khớp ERP → hàng ERP; không khớp → hàng tạm). Nếu báo lỗi thì chính file mẫu (`TEMP-SRV-CRANE`) cũng không import nổi. `cost_id` nullable, bảng 0 dòng → không rủi ro dữ liệu cũ.
4. **"Hàng hoá dự án" không phải bảng** — là UNION runtime trong `ProductProjectController:71-100`: BOM **tổng hợp + đã duyệt** (dòng cha) ∪ báo giá **tự lập + Đã duyệt/Trúng thầu** (dòng cha). Hàng tạm = `erp_product_id IS NULL`. Đây là tập đối chiếu luật "mã tạm trùng". (`ProductProjectService.php` là **code chết** — trỏ entity không tồn tại.)

## Vì sao modal import BOM không dùng `V2BaseImportModal`?

*(User đã hỏi lại câu này sau khi code xong → chứng tỏ lý do chưa tìm thấy được từ code. Đã ghi comment đầu `BomImportModal.vue`. Chốt lại: **giữ modal riêng**.)*

`V2BaseImportModal` thiếu **3 thứ bắt buộc** của luồng import BOM, cả 3 đều ở **tầng hiển thị** (kiểm chứng được):

| # | Thiếu gì | Bằng chứng | BOM cần gì |
|---|---|---|---|
| 1 | Khoá theo **DÒNG**, không theo **Ô** | `V2BaseImportTable.vue:61-62,73,85-86` — `:readonly="isRowReadonly(row)"` | Trên **cùng 1 dòng**: Tên/Model/Thương hiệu/Xuất xứ/ĐVT/Thông số **khoá** (dữ liệu chuẩn ERP — tài liệu mục 2.4), nhưng STT/Nhóm/Số lượng/Ghi chú **vẫn sửa được**. Server trả `locked_fields` theo từng dòng. |
| 2 | Chỉ **2** trạng thái dòng | `V2BaseImportTable.vue:200` — `return row.__isValid ? 'row-valid' : 'row-invalid'` | Trạng thái **thứ 3** "Chờ xác nhận" (vàng) + 2 nút hành động trên dòng |
| 3 | Không có `pendingCount` | `V2BaseImportModal.vue:207-208` chỉ có `importValidCount`/`importInvalidCount` | Luật *"dòng vàng chưa chọn → chặn Import **kể cả khi đã tích Bỏ qua dòng lỗi**"* không biểu diễn nổi bằng 2 biến |

Sửa component dùng chung để thêm 3 thứ đó = **đụng 11 màn** (solution-groups, customer-scopes, applications, project_role…) → phải regression cả 11.

**Vẫn dùng chung, KHÔNG nhân bản**: `parseExcelFile()` từ `utils/import-helper.js` (tầng parse), `V2BaseButton`/`V2BaseInput`.
**Nợ kỹ thuật đã biết**: `normKey()` trong modal là **bản sao thứ 2** của logic trong `import-helper.js` (reviewer verify khớp 17/17 ca thật). Muốn gỡ thì tách `normKey` ra util dùng chung — rẻ, rủi ro thấp.

## Phát hiện trong lúc code Phase 1 (đều do đo, không phải suy luận)

5. 🔴 **DB KHÔNG chạy strict mode** — `sql_mode = NO_ENGINE_SUBSTITUTION`, `config('database.connections.mysql.strict') = false`. Chuỗi dài hơn cột bị **cắt âm thầm**, insert vẫn trả về thành công. Đo thật: ghi mã 60 ký tự vào `bom_list_service_items.code` (varchar(50)) → DB lưu 50 ký tự, `failed=0`, **HTTP 200**, không báo gì. ⇒ Giả định "insert quá dài → lỗi → dòng failed → 207 → user biết" là **SAI**; validate ở tầng ứng dụng là lớp bảo vệ **duy nhất**. Đã thêm luật độ dài cho luồng import BOM.
   **Ngoài scope, đáng rà cấp dự án**: mọi màn ghi dữ liệu user nhập mà không validate `max` đều có nguy cơ mất dữ liệu âm thầm.
6. **`import()` vứt bỏ `resolved`** — gọi validate xong chỉ giữ cờ `isValid`, để `importProducts()` tra cứu lại từ đầu ⇒ 2 đường tra cứu độc lập, user xem preview một đằng DB lưu một nẻo; và dòng `pending_confirm` (`isValid=false`) bị **âm thầm loại bỏ**. Sửa xong: đường ghi `mysql2` = **0 query** (code cũ gọi `resolveLookupId` 4 lần/dòng = N+1 thật).
7. **`skip_invalid` + cha bị skip → con mồ côi** mất CẢ `parent_id` LẪN `bom_list_group_id`, chỉ báo "Đã bỏ qua 1 dòng lỗi" → thêm cascade skip + tách bộ đếm (con bị cascade **không phải** dòng lỗi).
8. **VAT dịch vụ hardcode 0** trong khi **497/504** cost dịch vụ có `vat=8` → cùng 1 cost thêm bằng tay lưu 8, import lưu 0 = lệch cột tiền. Đã lấy từ `resolved.vat_percent` (0 query thêm).
9. **`resolved` dùng key `*_id`** (để `toNullableInt()` không nuốt tên thành null) nhưng FE cần **tên** cho ô khoá — đổ vào sẽ hiện "40" thay vì "Cái". BE trả thêm `*_name` (tốn 0 query: `preloadMasterData()` vốn đã fetch `id + name` rồi vứt tên lúc `map`).

## Xung đột task ↔ tài liệu (đã xử lý)

| Điểm | Task nói | Tài liệu nói | Chốt |
|---|---|---|---|
| Vị trí Sao chép | Màn chi tiết BOM | Trang Danh sách BOM (mục 4.2) | Theo tài liệu |
| Phạm vi Sao chép | "hoặc giữa các phiên bản giải pháp" | Không mô tả | Bỏ khỏi scope |
| STT | — | Ví dụ `2.1.3` (3 cấp) | DB chỉ 2 cấp → báo lỗi, không làm phẳng ngầm |
| Cột đầu file | — | Import ghi `Loại *`, export ghi `Phân loại *` | Dùng `Loại *` cả hai; nhận `Phân loại` qua alias |
| Mục 3.3 (định dạng export) | — | **Để trống** | Lấy sheet `export_bomlist` làm chuẩn |

## DB

1 migration: `bom_lists` + cột `copied_from_bom_list_id` (unsignedBigInteger nullable) — truy vết nguồn gốc khi sao chép. Không bọc DDL trong transaction.
Cột `note` (cho cột "Ghi chú" mới) **đã có sẵn** từ feature `product-project-note-sync` → không cần migration.

## Phân quyền

Không thêm quyền mới. Nút Sao chép gate bằng `Tạo BOM List` (id 1034).

## Ngoài scope

- Sao chép giữa phiên bản giải pháp · STT 3+ cấp (đòi `syncProducts` đệ quy) · dọn `ProductProjectService.php` chết · gắn `checkPermission` cho routes BOM · `syncSubBomRelations` không chặn vòng lặp A→B→A
