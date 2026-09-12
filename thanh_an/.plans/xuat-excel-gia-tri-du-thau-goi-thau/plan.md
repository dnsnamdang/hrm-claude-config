# Xuất excel — bổ sung cột "Giá trị dự thầu" (màn danh sách gói thầu)

**Người phụ trách:** @khoipv
**Ngày tạo:** 2026-09-10

## Bối cảnh

Màn danh sách gói thầu (`pages/bid_package/bid_package/index.vue`) có cột "Giá trị dự thầu"
(`bid_packages.total_amount`) nhưng luồng **Xuất excel** (chọn cột → `getBidPackagesByField`)
không có cột này.

Cách làm: copy pattern đã áp dụng cho màn **Hợp đồng** (`app/ExcelExport/ContractExport.php`):
ghi **số thuần** ra ô + `setFormatCode('#,##0')` trong `AfterSheet`, tính chữ cái cột động theo
các cột người dùng tích chọn → Excel hiển thị `1.234.567` và vẫn `SUM` được.

Không tái dùng id 14 (BE vẫn map `product_group_name`) → dùng **id 30**.

## Phase 1 — Backend (`hrm-thanhan-api`)

- [x] `Modules/Category/Http/Controllers/Api/V1/BidPackageController.php` — thêm
      `'total_amount' => $data->total_amount ?? 0` vào mảng `$result[]` của `getBidPackagesByField()`
- [x] `app/ExcelExport/BidPackageExport.php` — chuyển `$arrayField` thành `const ARRAY_FIELD`,
      thêm `30 => 'total_amount'`
- [x] `app/ExcelExport/BidPackageExport.php` — thêm `const DISPLAY_ORDER` (đúng thứ tự blade)
      + `getTotalAmountColumnLetter()`
- [x] `app/ExcelExport/BidPackageExport.php` — `registerEvents()` set number format `#,##0`
      cho vùng ô cột giá trị dự thầu
- [x] `resources/views/exports/bid_package_report.blade.php` — thêm header "Giá trị dự thầu"
      + ô dữ liệu (số thuần, căn phải), đặt sau "Số lượng mặt hàng", trước "Kết quả thầu"

## Phase 2 — Frontend (`hrm-thanhan-client`)

- [x] `pages/bid_package/bid_package/index.vue` — `fieldsExport`: thêm
      `{ id: 30, value: 30, text: 'Giá trị dự thầu' }` sau id 27
- [x] `pages/bid_package/bid_package/index.vue` — `checkAllField()`: mảng đang dừng ở 28
      (thiếu luôn 29 "Kết quả thầu") → bổ sung `29, 30`

## Phase 3 — Verify

- [x] Xuất file chỉ tích "Giá trị dự thầu" → đúng cột (B), đúng số
- [x] Xuất "Chọn tất cả" → có đủ cả "Kết quả thầu" và "Giá trị dự thầu" (verify bằng `getTotalAmountColumnLetter()`: 30 cột → cột AC)
- [x] Xuất kèm bộ lọc → số khớp cột trên màn danh sách (@khoipv chốt hoàn thành 2026-09-10)
- [x] Bôi vùng cột trong Excel → `SUM` ra kết quả (render thử `.xlsx`: ô E3/E4 kiểu `integer`, format `#,##0`)

## Checkpoint

### Checkpoint — 2026-09-10
Vừa hoàn thành: Toàn bộ Phase 1 (BE) + Phase 2 (FE) + verify render offline.
- BE: `BidPackageController::getBidPackagesByField()` trả thêm `total_amount`;
  `BidPackageExport` chuyển sang `const ARRAY_FIELD` (+ `30 => 'total_amount'`) & `const DISPLAY_ORDER`,
  thêm `getTotalAmountColumnLetter()` + format `#,##0` trong `AfterSheet`;
  blade thêm cột "Giá trị dự thầu" (số thuần, căn phải) sau "Số lượng mặt hàng".
- FE: `fieldsExport` thêm id 30; `checkAllField()` bổ sung `29, 30` (trước đó dừng ở 28 → "Chọn tất cả" thiếu cả "Kết quả thầu").
- Verify offline: đối chiếu thứ tự cột blade (thead == tbody == DISPLAY_ORDER, 30/30 khớp);
  chạy `getTotalAmountColumnLetter()` với 5 bộ fields (chỉ id 30 → B; [1,2,27,30] → E; 1..30 → AC; không tích → null; rỗng → null);
  render thật file `.xlsx` rồi đọc lại: giá trị lưu kiểu `integer` với format `#,##0`.

Đang làm dở: (không)
Bước tiếp theo: @khoipv xuất thử trên trình duyệt với dữ liệu thật + bộ lọc, đối chiếu số với cột trên màn danh sách.
Blocked:

### Checkpoint — 2026-09-10 (đóng feature)
Vừa hoàn thành: @khoipv chốt chuyển feature sang mục "Hoàn thành" trong STATUS.md.
Đang làm dở: (không)
Bước tiếp theo: (không) — nhớ build lại client + hard refresh khi deploy.
Blocked:
