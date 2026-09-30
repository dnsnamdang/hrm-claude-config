# Plan — Tối ưu performance API danh sách hợp đồng

**Phụ trách:** @khoipv
**Bối cảnh:** Vào màn lập phụ lục → dropdown "Chọn hợp đồng" gọi
`GET category/contracts?request_type=contract&per_page=1000000000&status=3&exclude_in_progress_annex=1`
mất ~16s.

## Số đo trước khi sửa (DB thanhan_stag_22092026, user id 33)

```
rows=477   queries=7949   time=16.33s   mem=162MB
```

| Số query | Nguồn |
|---|---|
| ~7208 | `isCurrentEmployeeHasPermission()` gọi 1802 lần, mỗi lần 4 query (firstOrNew + spatie roles/permissions). `ContractResource` gọi `canEdit/canDelete/canApprove/canAssign` mỗi dòng |
| 477 | `Contract::canAssign()` query `contract_assign_employees` từng dòng |
| 206 | `ContractResource::toArray()` gọi `BidPackageQuotation::...->get()` trong vòng lặp |
| 1 (271ms) | eager load 10.125 dòng `contract_products` chỉ để `sum('amount')` + `count()` |

Thêm: `contracts`, `contract_products`, `contract_annexes`, `contract_guarantees` chỉ có PRIMARY KEY.

## Ràng buộc từ user
- Danh sách hợp đồng chọn được phải **giữ nguyên y hệt** → tái dùng đúng query builder của `ContractService::index()` (bộ lọc + phân quyền theo cấp không đổi).
- **KHÔNG** sửa `isCurrentEmployeeHasPermission()` / `listManageEmployeeIdsByGroup()` (hàm dùng chung, chưa được xác nhận).

## Task

### Phase 1 — BE: endpoint slim cho dropdown phụ lục
- [x] `ContractService::selectableForAnnex()` — tái dùng `index($request)`, `setEagerLoads([])`, chỉ select id/code/number/name
- [x] `ContractController::selectableForAnnex()` + route `GET category/contracts/selectable-for-annex`
- [x] Đặt route TRƯỚC `GET /{contract}` để không bị nuốt

### Phase 2 — BE: bỏ N+1 trong ContractResource (màn danh sách HĐ chính)
- [x] Thêm relation `Contract::bidPackageQuotations()` + eager load trong `index()` → bỏ query trong vòng lặp
- [x] Thêm relation `Contract::assignEmployees()`, `canAssign()` dùng relation khi đã load (fallback query cũ)
- [x] `withSum('products','amount')` + `withCount('products')`, bỏ `with('products')` (resource fallback nếu thiếu)

### Phase 3 — DB index
- [x] Migration thêm index (chỉ index, không foreign key)

### Phase 4 — FE
- [x] Đổi 8 màn phụ lục sang endpoint mới

### Phase 5 — Verify
- [x] Đo lại, so danh sách id trả về trước/sau phải TRÙNG KHỚP 100%

## Kết quả đo sau khi sửa

| | queries | thời gian | RAM |
|---|---|---|---|
| Endpoint cũ `GET category/contracts` (477 dòng, full resource) — TRƯỚC | 7.949 | 16,33s | 162MB |
| Endpoint cũ — SAU (bỏ N+1 + withSum/withCount + index) | 7.229 | 9,66s | 92MB |
| **Endpoint mới `GET category/contracts/selectable-for-annex`** | **5** | **0,02s** | — |

Kiểm chứng: danh sách (id, number, name) trả về của endpoint mới **trùng khớp 100%** với endpoint cũ trên 5 user (33/36/99/34/153), mỗi user 477 dòng.
Regression `ContractResource`: 477/477 hợp đồng khớp `total_amount`, `sum_product_qty`, `projects`, `quotations`; `can_assign` khớp cả 2 nhánh (có/không có bản ghi `contract_assign_employees` status=1).

## Còn tồn (chưa làm, cần user quyết)

1. **7.229 query còn lại của endpoint cũ đều từ `isCurrentEmployeeHasPermission()`** (1.802 lần gọi × 4 query). Nằm ở `app/Helper/PermissionHelper.php` — hàm dùng chung, chưa được xác nhận nên KHÔNG sửa. Thêm static cache theo request (giống `listManageEmployeeInfoIdsByDepartment()` đã làm sẵn trong cùng file) sẽ kéo 9,66s → dưới 1s và nhanh toàn bộ màn danh sách của hệ thống.
2. ~~Bug nhánh quyền "nhóm nghiệp vụ"~~ — **ĐÃ FIX** (xem Phase 6).

3. **Cùng bug bọc nhóm OR** còn ở `ProjectService.php:157` và `QuotationService.php:160` (tên bảng đúng nên không lỗi 500, nhưng `orWhere` không bọc closure → OR vẫn phá vỡ điều kiện AND phía trước, rò dữ liệu ở màn Dự toán / Báo giá). Chưa sửa — ngoài phạm vi yêu cầu, cần user xác nhận vì sẽ đổi danh sách user nhánh này đang thấy.

### Phase 6 — Fix bug nhánh quyền "nhóm nghiệp vụ" (user xác nhận 23/09/2026)
- [x] `whereIn('contract.created_by', ...)` → `contracts.created_by` (thiếu chữ `s` → lỗi SQL 1054, user id=44 dính 500)
- [x] Bọc `whereIn(...)->orWhere(...)` vào closure `where(function ($query) {...})` theo pattern `BidPackageService:183`

  Không bọc thì SQL ra: `... AND contract.created_by IN (...) OR contracts.created_by = 44` — OR phá vỡ TOÀN BỘ điều kiện AND phía trước (`record_type`, `status`, `exclude_in_progress_annex`, mọi bộ lọc). Sửa mỗi chữ `s` sẽ hết 500 nhưng rò biên bản thương thảo + HĐ nháp của chính user vào mọi màn danh sách.

- [x] Verify user 44: trước = lỗi SQL 1054; sau = 11 dòng, `record_type` sai 0, `status` sai 0, HĐ còn phụ lục dở dang 0, dòng ngoài phạm vi quyền 0. `selectableForAnnex()` trùng id với `index()`.
- [x] Verify không regression: 5 user cũ (33/36/99/34/153) vẫn 477 dòng, trùng khớp snapshot trước khi sửa.

## Checkpoint — 23/09/2026

Vừa hoàn thành: BE (endpoint slim + bỏ N+1 + migration index), FE (8 màn phụ lục), fix bug nhánh quyền "nhóm nghiệp vụ" — đã đo và đối chiếu dữ liệu.
Đang làm dở: không có.
Bước tiếp theo: build lại client + hard refresh, mở 8 màn lập phụ lục kiểm tra dropdown "Chọn hợp đồng" vẫn đủ HĐ như cũ. Chạy `php artisan migrate` trên môi trường khác.
Blocked: chờ user quyết mục "Còn tồn" số 1 (cache hàm dùng chung) và số 3 (bug bọc nhóm OR ở ProjectService/QuotationService).

### Phase 7 — Resolve conflict merge `master` → `thanhan-dev` (24/09/2026, repo client)
- [x] Rà 9 file conflict: 8 file dropdown "Chọn hợp đồng" (phụ lục + phụ lục giảm giá) + `pages/contract/contract/approve.vue`
- [x] 8 file dropdown: giữ endpoint mới của `master` (`category/contracts/selectable-for-annex`, bỏ `per_page`) **gộp** dải trạng thái của `thanhan-dev` (`status=3,9,10,11`, commit `6337b366`)

  Base là `status=3`; hai nhánh sửa 2 thứ khác nhau trên cùng 1 dòng nên phải gộp, lấy 1 bên là mất thay đổi bên kia. `selectableForAnnex()` chỉ là `index()` bỏ eager load nên vẫn ăn tham số `status` dạng danh sách; `per_page` bỏ được vì service trả `->get()`, và master đã sửa sẵn `const { data, meta }` → `const { data }`.

- [x] `approve.vue`: `master` thêm cột **Mảng hàng hóa** (`item.array_product_names`), base và `thanhan-dev` đều chưa có → lấy nguyên phần thêm của master. BE đã có sẵn `array_product_names` trong `ContractResource:120`.
- [x] `git add` 9 file — cây làm việc hết trạng thái unmerged, không còn marker. **Chưa commit** (user tự commit).

⚠️ Sau khi commit merge FE: repo API `thanhan-dev` **cũng phải merge `master`** thì mới có route `category/contracts/selectable-for-annex` (hiện route này chỉ có trên `master`), không thì 8 màn lập phụ lục sẽ 404.

### Phase 8 — Resolve conflict merge `master` → `thanhan-dev` (24/09/2026, repo API)
- [x] 1 file conflict: `Modules/Category/Entities/Contract/Contract.php`, hàm `canAssign()` — hai nhánh sửa 2 thứ khác nhau trên cùng khối lệnh, **gộp cả hai**:
  - `thanhan-dev` (commit `8b9fa738`, 17/09): mở rộng dải trạng thái được phân công thêm `DA_KET_XUAT`, `CHO_DUYET_KET_XUAT`, `KHONG_DUYET_KET_XUAT`
  - `master` (commit `18bcabbb`): bỏ N+1 — dùng `relationLoaded('assignEmployees')` + `firstWhere('status', 1)` khi đã eager load, fallback về query cũ khi chưa
- [x] Kiểm chứng an toàn: relation `assignEmployees()` có sẵn (`Contract.php:507`) và `ContractService:61` eager load **không kèm ràng buộc** → `firstWhere('status', 1)` cho cùng kết quả với query cũ.
- [x] `php -l` sạch, `git add` — hết trạng thái unmerged. **Chưa commit** (user tự commit).
