# Design (tóm tắt): Sao chép / Export / Import Báo giá

> Spec đầy đủ: `docs/superpowers/specs/2026-07-16-baogia-copy-export-import-design.md`

## Trạng thái triển khai — 2026-07-16: ✅ HOÀN TẤT (29/29 task, chờ merge)

Cả 3 tính năng đã code xong, mỗi task qua review độc lập + Approved, final whole-branch review **SẴN SÀNG MERGE** (0 finding cấp hệ thống chặn merge). **Chưa commit** (theo CLAUDE.md) — toàn bộ ở working tree worktree `baogia_copy_export_import`. **Chưa test end-to-end trên browser thật** (chưa login được vào BE); verify bằng: lint PHP 7.4, SFC parse + webpack bundle 0 error, và script tinker chạy trên DB thật (bọc `beginTransaction`/`rollBack`) cho mọi nhánh BE.

**Cần BA/user chốt trước khi release** (đều là quyết-định-treo, không phải defect): xem cuối file.

- **Phụ trách**: @manhcuong
- **Ngày**: 2026-07-16
- **Worktree**: `/Users/manhcuong/Desktop/dns/HRM-worktree-baogia/{hrm-api,hrm-client}` — nhánh `baogia_copy_export_import` (từ `origin/tpe`)
- **Màn hình**: QLDA TKT → Quản lý báo giá · Chi tiết dự án → Tab Báo giá · Xem chi tiết BG · Cập nhật BG

## Mục tiêu

1. **Sao chép** — làm mới hoàn toàn (chưa có gì).
2. **Export** — thêm 2 nút (trống / hiện tại) theo bộ 24 cột file mẫu.
3. **Import** — **viết lại** (bản hiện tại scope hẹp hơn nhiều).

## Hiện trạng

| Chức năng | Trạng thái |
|---|---|
| Sao chép | **Chưa có gì** |
| Export | Có 1 nút "Xuất Excel" (bản để xem/gửi, bộ cột khác) → giữ nguyên, thêm 2 nút |
| Import | **Đã có** nhưng chỉ "cập nhật giá cho BG từ BOM": BG độc lập → crash null; dòng lạ → nuốt im lặng; không có khu vực GG tổng, không parse cây STT |

## 9 quyết định lớn

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Scope Sao chép | **Full URD**, trừ Rule 1 (hoãn) |
| 2 | Luồng Import | **Đổ vào lưới FE** → user bấm Lưu. BE chỉ validate, **không ghi DB** ⇒ không cần endpoint `import` |
| 3 | Nút Export | Giữ "Xuất Excel" cũ + 2 nút URD, **gộp 3 vào dropdown** (footer đã 8 nút) |
| 4 | Đổi dự án trên V2 | **Chỉ bản sao chép** (`copied_from_quotation_id` + status 1) |
| 5 | Quyền Sao chép | **Tái dùng gate `store()`**, không thêm quyền mới |
| 6 | BG từ BOM | **Giữ khoá cấu trúc** — chỉ import giá |
| 7 | Rule 1 (ngừng KD) | **Hoãn**, chờ ERP |
| 8 | Đối chiếu Loại GG | **`code` trước, fallback `name`** |
| 9 | Tách import ở FE | **Modal tự chứa logic + emit** (Vue 2 thuần, không có composition-api) |

## 4 phát hiện quan trọng khi khảo sát

1. 🔴 **"Hàng ngừng kinh doanh" KHÔNG tồn tại trong ERP** — query thật 45.548 dòng `mysql2.products`: `product_type` có 15 giá trị đều là phân loại vật tư (`product`, `accessories`, `tool`, `weld_materials`…), **không có giá trị nào nghĩa là ngừng KD**. `status` có 0/1/2/5 nhưng **không có mapping nào trong code HRM**. Grep "ngừng kinh doanh"/"discontinued" 2 repo → **0 kết quả**. API search ERP **không trả `status`**. ⇒ Giả định URD sai so với dữ liệu thật → **Rule 1 hoãn, cần ERP trả lời**.

2. 🔴 **BG từ BOM read-only về cấu trúc — CÓ CHỦ Ý**, chặn 3 tầng: `QuotationService:979` `if (!$productId) continue;` (nuốt im lặng); nhánh BOM **không có delete-not-in**; `validateParentChildRules:830` early-return + comment *"type=1: con thừa hưởng từ BOM, không thêm con mới ở báo giá"*; FE `edit.vue:306-313` ẩn nút Thêm. Mở khoá còn kéo theo `assertParentSalePriceFloor`/`assertParentImportFloor` dùng `join('bom_list_products')` ⇒ dòng `bom_list_product_id=null` **bị INNER JOIN loại khỏi validate giá cha-con** → lỗ hổng. ⇒ **Giữ khoá**, URD cần BA làm rõ.

3. **Vận chuyển không phải dòng hàng hoá** — URD cột `Loại` có "Chi phí vận chuyển", nhưng DB lưu ở **5 field header `quotations`** (`shipping_cost`, `shipping_vat_percent`, `shipping_discount`, `shipping_allocated_discount`, `shipping_import_price`). ⇒ Map dòng Excel → header, tối đa 1 dòng.

4. **`amount_value` là nguồn sự thật của giảm giá**, không phải `percent_value` — `allocateDiscount:2268-2275` chỉ `sum('amount_value')`. Quan trọng cho Rule 6 (copy giữ % → tính lại tiền).

## DB

1 migration: `quotations` + `copied_from_quotation_id` (unsignedBigInteger nullable) — truy vết nguồn gốc **và** gate đổi dự án. **Không bọc DDL trong transaction**.

Không cần cột nào cho Import (không ghi DB) hay Rule 1 (hoãn).

## API

| Method | Route | Ghi chú |
|---|---|---|
| GET | `/{id}/copy-preview` | Diff ERP; rỗng → FE bỏ popup |
| POST | `/{id}/copy` | Tạo V2, trả `{id, code}` |
| GET | `/export-blank-template` | ⚠️ **Phải đặt TRƯỚC `GET /{id}`** (cùng 1 segment) |
| GET | `/{id}/export-quotation-data` | 24 cột + khu vực GG |
| POST | `/{id}/import-excel/validate` | Trả rows chuẩn hoá; lỗi = **all-or-nothing** (422) |

Class mới: `QuotationImportService` (không nhét vào `QuotationService` — đã 2742 dòng) · `Modules/Assign/Export/QuotationExcelExport` (FromView, đúng convention 157/157).

## FE

**Mới**: `QuotationCopyPreviewModal.vue` · `QuotationImportModal.vue` (tự chứa logic + emit `import-applied`, **không đụng `V2BaseImportModal`** — 13 màn khác dùng chung).

**Sửa**: `_id/index.vue` (dropdown Export + nút Sao chép) · `index.vue` + `ProspectiveProjectQuotationsTab.vue` (nút Sao chép) · `edit.vue` (~15 dòng: nhúng modal + `onImportApplied`; đổi dự án nếu là bản sao chép).

**Dọn code cũ**: gỡ luồng import-prices (nút + `V2BaseImportModal` + 5 handler ở `edit.vue`; 3 method BE `validateImportPrices`/`importPrices`/`exportImportTemplate` + 3 route). Giữ lại = 2 đường code song song.

## Phân quyền

Không thêm quyền mới. Nút Sao chép gate lặp logic `store()`: nguồn từ YCBG ⇒ `Xây dựng giá bán theo công ty/phòng` theo `implementation_type`; tự lập ⇒ Sale phụ trách dự án.

⚠️ `isCurrentEmployeeHasPermission` check qua **ROLE** (`role_has_permissions`), không qua quyền gán trực tiếp — nhớ khi test.

## Xung đột với URD (cần báo BA)

| URD nói | Chốt |
|---|---|
| Rule 1: quét "Loại hàng hóa" ERP tìm "ngừng kinh doanh" | **Hoãn** — dữ liệu thật không có |
| BG kế thừa BOM cho Sales chèn dòng | **Giữ khoá** — code cố ý chặn 3 tầng |
| Master Data lạ → tự động Insert | **Chặn + báo lỗi** — theo quyết định #3 của feature BOM (tránh bơm rác ERP) |
| "Chi phí vận chuyển" là 1 dòng hàng | **Map sang 5 field header**, tối đa 1 dòng |
| "Loại GG" đối chiếu theo tên | **`code` trước, fallback `name`** |
| STT ví dụ `2.1.3` (3 cấp) | **Tối đa 2 cấp**, báo lỗi |

## Ngoài scope

Rule 1 (chờ ERP) · Chèn dòng vào BG từ BOM (chờ BA) · Auto-insert Master Data · 2 bug `V2BaseButton` (`type="danger"` ở `_id/index.vue:643`; `:disabled` thay `:interactable` ở `edit.vue:998,1002`) · Gom status BG hardcode 5 nơi FE · Bug `total_sale` = 0 với BG tự nhập (`QuotationResource:16-23`)

## Lưu ý khi code

- ⚠️ **DB không chạy strict mode** (`sql_mode = NO_ENGINE_SUBSTITUTION`) — chuỗi dài hơn cột **bị cắt âm thầm**, insert vẫn thành công ⇒ validate độ dài ở tầng ứng dụng là lớp bảo vệ **duy nhất** (`note` 500, `Nhóm hàng` 255).
- ⚠️ **Bẫy tên trùng**: `product_type` HRM = **số** (1=Hàng hoá/2=Dịch vụ); `product_type` ERP = **chuỗi** enum. Khác nhau hoàn toàn.
- Lint BE bằng `/opt/homebrew/opt/php@7.4/bin/php -l` (máy mặc định PHP 8.1, production 7.4).
- Round-trip Export→Import **không byte-identical** (STT chuẩn hoá lại, 7 cột công thức tính lại) — kỳ vọng đúng là **import lại không lỗi**.

## Cần BA/user chốt trước release (gom cuối phiên triển khai)

**Quyết định treo (không chặn merge, cần chốt nghiệp vụ):**
1. **Round-trip nút "Xuất Excel" cũ** trong `edit.vue` (`/export-excel`, format BOM cũ) đặt cạnh nút "Import Excel" (parser 2-khối mới) → luồng Xuất→sửa→Import ở màn edit báo "File không đúng mẫu". File đúng để round-trip export từ **màn danh sách** (`/export-quotation-data`). → Wire lại nút export format-mới vào edit.vue, hay gỡ nút cũ?
2. **`[STT]` trong message khối GG tổng** = số dòng Excel (đang tạm chốt) vs STT cây — spec §7.4 tự mâu thuẫn với ví dụ §7.3.
3. **Tên file export lệch 1 ngày** quanh nửa đêm khi browser khác múi giờ server (FE ghép `dayjs()` vs BE `date()`). Đường sạch = expose `Content-Disposition` trong `config/cors.php` (**config dùng chung — cần user duyệt**).
4. **~15 chuỗi message validate import tự đặt** (giới hạn độ dài, cận trên, "không hợp lệ"…) — cần BA duyệt câu chữ.
5. **Reallocate vs giữ phân bổ giảm giá tay của V1** khi sao chép (đang tạm chốt: LUÔN reallocate).
6. **`solution_id` / `pricing_request_id` sau khi đổi dự án** — giữ hay xoá?
7. **Message "phải lớn hơn 0"** hiện cho cả `'35,600,000'` (FE gửi formatted) lẫn `'#REF!'` (công thức vỡ) — cần message thứ 3 kiểu "không phải là số hợp lệ".
8. **Trùng `discount_type_id` 2 dòng** khi import: BE chấp nhận nhưng picker FE loại id đã dùng → dòng 2 hiện ô Loại GG trống, không báo lỗi.
9. **Heuristic "Dịch vụ & Chi phí khác"** phân biệt `quotation_product_prices.product_type=2` vs `quotation_service_items` — chưa xác nhận được bằng data thật (0 dòng `product_type=2`).
10. **Dialog/hint đổi dự án + confirm ghi đè import** — câu chữ tiếng Việt cần BA duyệt.

**Vẫn chờ (đã treo từ đầu):**
- **Rule 1 (hàng ngừng KD)** — chờ ERP: mapping `products.status` 0/1/2/5 + bổ sung `status` vào API search. Thiết kế đã chừa chỗ ở `getCopyPreview()`.
- **Chèn dòng vào BG kế thừa BOM** — chờ BA (code cố ý khoá 3 tầng; import hiện báo lỗi rõ thay vì nuốt im lặng).

## Bug CÓ SẴN phát hiện khi thi công (ngoài scope — báo user, task riêng)
1. **`strtoupper('VNĐ') ≠ 'VND'`** (byte-based) → 8/8 báo giá VNĐ đi vào nhánh "ngoại tệ", đúng nhờ ăn may `exchange_rate=1`. Set rate VNĐ ≠ 1 → mọi giá vỡ. Ở `create():105`, `create-from-BOM():697`, `update():899`, `resolveCurrentExchangeRate()`. Sửa phải sửa đồng thời cả 4.
2. **`ensureAllPricesPositive()` INNER JOIN `bom_list_products`** → NO-OP với MỌI BG type=2 (tự lập). Gate "giá bán > 0" hiện chỉ còn hiệu lực với BG-từ-BOM. Đo: BG#1 0/9, BG#5 0/85, BG#6 0/94, BG#9 0/41.
3. **`HH-00001` cấp trùng** khi `upsertDirectProducts()` xoá-tạo-lại: dòng trống mã đứng trước dòng round-trip `HH-00001` được cấp trùng mã.
4. **`store():178` trả 422 cho chính `abort(403)` của nó** (`HttpException::getCode()=0`, status ở `getStatusCode()`) — code chết.
5. **Total cache stale**: mọi `update()` (kể cả chỉ đổi `note`) làm tổng tiền nhảy → số tổng đang lưu của một số BG đang sai.
6. **`POST /{id}/allocate-discount` chết**: gọi với BG tự lập → `$quotation->bomList->products()` null-pointer (`Error`, không phải `Exception`) → `catch(Exception)` không bắt → 500. FE không gọi route này.

## Giới hạn kiểm thử (chưa test được, cần data/môi trường thật)
- Chưa test end-to-end trên **browser thật** (chưa login được vào BE) — FE verify bằng SFC parse + webpack bundle 0 error; 1 lần render modal Sao chép không-login qua `?redirect_page=1`.
- **Báo giá ngoại tệ** (8/8 BG đều VNĐ rate=1), **`discount_method=2`** (0 BG), **`pricing_requests`** (0 row), **cha-tạm-có-con** (0 trong data) — mọi nhánh này chỉ test bằng data ép trong transaction/in-memory, chưa chạy trên data sản xuất thật.
