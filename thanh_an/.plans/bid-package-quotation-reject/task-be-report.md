# Backend Implementation Report — Từ chối lập gói thầu

**Ngày:** 2026-06-23
**Người thực hiện:** AI implementer
**Phạm vi:** Phase 1 — Backend, Task 1 đến Task 6

---

## Danh sách file đã sửa

| File | Thay đổi |
|------|---------|
| `Modules/Category/Entities/Quotation/Quotation.php` | Task 1: Thêm `const TU_CHOI_LAP_GOI_THAU = 20`; Task 2: Thêm method `canRejectBid()` |
| `Modules/Category/Entities/Project/Project.php` | Task 1: Thêm `const TU_CHOI_LAP_GOI_THAU = 19` |
| `Modules/Category/Services/QuotationService.php` | Task 3: Thêm method `rejectBid()` sau `render()` |
| `Modules/Category/Http/Controllers/Api/V1/QuotationController.php` | Task 4: Thêm method `rejectBid()`; Task 6: Thêm `20 => 'Từ chối lập gói thầu'` vào 3 statusMap |
| `Modules/Category/Routes/api.php` | Task 4: Thêm route `PUT /{quotation}/reject-bid` |
| `Modules/Category/Transformers/QuotationResource/QuotationResource.php` | Task 5: Thêm `'can_reject_bid' => $this->canRejectBid()` |
| `Modules/Category/Http/Controllers/Api/V1/ProjectController.php` | Task 6: Thêm `19 => 'Từ chối lập gói thầu'` vào 3 statusMap |

---

## Kết quả php -l

Chạy trong thư mục `hrm-thanhan-api`:

```
No syntax errors detected in Modules/Category/Entities/Quotation/Quotation.php
No syntax errors detected in Modules/Category/Entities/Project/Project.php
No syntax errors detected in Modules/Category/Services/QuotationService.php
No syntax errors detected in Modules/Category/Http/Controllers/Api/V1/QuotationController.php
No syntax errors detected in Modules/Category/Routes/api.php
No syntax errors detected in Modules/Category/Transformers/QuotationResource/QuotationResource.php
No syntax errors detected in Modules/Category/Http/Controllers/Api/V1/ProjectController.php
```

**Tất cả 7 file: PASS**

---

## Kết quả route:list

```
PUT  api/v1/category/quotations/{quotation}/reject-bid  QuotationController@rejectBid
```

Route đăng ký thành công, đúng method và path.

---

## Kiểm tra `use` imports trong QuotationService.php

Tất cả các class cần thiết đã có sẵn trong file:
- `use Modules\Human\Entities\Employee;` ✓ (dòng 21)
- `use Modules\Category\Entities\Project\Project;` ✓ (dòng 17)
- `use Modules\Category\Entities\Quotation\HistoryApprovedQuotation;` ✓ (dòng 25)
- `use Modules\Timesheet\Services\EmployeeInfoService;` ✓ (dòng 16)
- `use Illuminate\Http\Request;` ✓ (dòng 6)

Không cần thêm import nào.

---

## Ghi chú về Task 6 — ProjectController

Plan đề cập 3 hàm cần sửa trong ProjectController (dòng 382, 561, 785 theo plan gốc). Thực tế:
- **Map 1** (`detailReport` khoảng dòng 375): Dòng 16 và 17 nằm trên 2 dòng riêng → đã sửa riêng.
- **Map 2** (`summaryReport` khoảng dòng 555): 16+17 cùng dòng.
- **Map 3** (`lifecycleDetail` khoảng dòng 779): 16+17 cùng dòng → Map 2 và 3 giống nhau, dùng `replace_all`.

Cả 3 map đều đã được thêm `19 => 'Từ chối lập gói thầu'`.

> Lưu ý: Plan gốc ghi 3 hàm là `detailReport`, `summaryReport`, `exportDetailReport`. Khi rà soát thực tế, map thứ 3 trong ProjectController là `lifecycleDetail`, không phải `exportDetailReport`. Tuy nhiên đây là mapping đúng theo nội dung file — cả 3 hàm có statusMap đều đã được cập nhật.

---

## Điểm nghi ngờ / lệch so với plan

1. **Không có điểm lệch nghiêm trọng.** Tất cả code trong plan khớp với code thực tế.
2. **QuotationService `render()` kết thúc đúng dòng 777** — đã thêm `rejectBid()` ngay sau, đúng vị trí.
3. **3 statusMap QuotationController** — cả 3 đều có cùng dạng `19 => 'Hủy hợp đồng',` → dùng `replace_all` để thêm `20 => 'Từ chối lập gói thầu'` vào cả 3 đồng thời, đúng.
4. **Method `canRejectBid()`** thêm ngay sau `canCreateBidPackage()`, logic giống nhau (status=7 + quyền "Lập gói thầu") — đúng spec.

---

## STATUS: DONE
