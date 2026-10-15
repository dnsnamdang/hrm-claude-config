# Review T1 + T2 — A3 (2-E) hrm-api — 14/10/2026 (chỉ đọc)

Phạm vi: commit `b0283c3a8` (quyền 1654), `90044a08a` (export-rows 5 màn), `9a7130e05` (bước 14' ép trùng mã) trên
`wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/cdhh-2e-excel`. Commit `9096a1cdc` (bỏ `catalogs_text` ở entering/temp) là chủ ý,
không soát. Cách soát: đọc diff và code liên quan (`ProductService::index`, `ProductListResource`, `CatalogBranch`, `AdminData`,
`PermissionService`, `CheckPermission`, `ProductWriteService::storeWithRetry`, FE `utils/export/listExportFile.js`), chạy SELECT trên
`hrm_erp_giacty`/`hrm_erp`. **Không chạy PHPUnit**, vì test ghi DB trong transaction mà vai reviewer không được ghi DB.

**Kết luận: không có lỗi Critical hay Important. Chỉ có 6 điểm Minor, không cái nào chặn T3.**

## Đã kiểm, đạt

| Hạng mục | Căn cứ |
|---|---|
| Gate 1654 chặn mặc định (fail-closed), xét theo công ty đang làm | `ProductExportController.php:38` gọi `isCurrentEmployeeHasPermission`, hàm này lọc `role_has_permissions.company_id = current_company_role` (`app/CommonServices/PermissionService.php:37-43`). Middleware `checkPermission:…1654` đứng trước làm lớp chặn thô. Cả hai lớp đều không có nhánh bỏ qua cho Super admin hay role 18. |
| Quyền màn giống route danh sách | `Routes/api.php:446-458` so với `:438-442`: company `1652\|1653`, entering `1652`, còn warehouse/trading/temp không có gate xem. |
| Bộ lọc, phạm vi và thứ tự giống hệt danh sách | `ProductExportService.php:101` gọi lại nguyên `ProductService::index($request, $screen)`. Các tham số thêm (`page`, `limit`, `fields`) không trùng tên với tham số lọc nào trong `applyScreen`/`applyCatalogFilters`/`applyFilters`. Thứ tự sắp luôn chốt thêm `products.id desc`, nên lật trang không lặp dòng, không mất dòng. |
| Không lọt giá vốn hay giá bán | Registry 5 màn không có key hay nhãn nào về giá. `cell()` chỉ trả các key có trong whitelist, và câu SELECT của `index()` cũng không lấy cột giá. Có test chốt việc này. |
| Không lọt dữ liệu ngoài phạm vi công ty | Catalog lọc `product_business_catalogs.company_id = công ty đang làm` (`:182`). `status_text` lấy theo `pcs` của công ty đang làm. YCHG và lý do không duyệt dùng subquery có `company_id` (`ProductService::withTempColumns`). Cột "Công ty đang kinh doanh" (chỉ màn Kho) cho ra đúng những gì màn danh sách đang hiện. |
| Catalog lấy đúng Tiểu mục, đúng nhánh còn hiệu lực | Dùng `JobCluster::query()`, nên global scope `business_catalog_tree` (cây mới) giống quan hệ `businessCatalogs.jobCluster` mà màn đang dùng. Nhánh cũ bị bỏ qua, khớp `CatalogBranch::many()`. Thứ tự sắp theo `pbc.id`, cũng là thứ tự PK của eager load. Tiểu mục bị khoá vẫn hiện, đúng chú thích "khoá chỉ chặn xếp hàng mới". |
| Giá trị từng ô bám đúng màn | Bảo hành và SL tồn tối thiểu theo luật `AdminData::source` (dòng của công ty mình, không có thì lùi về cột chung). Cây phân loại và các danh mục dùng cùng model nên cùng scope. Test `gia_tri_o_khop_man_danh_sach…` so 19 cột với `ProductListResource`. |
| Phân trang và trần | `page ≥ 1`, `limit` thuộc [1, 5000], mặc định 2000. STT tính theo offset. Phần tử đầu mỗi dòng là STT, khớp `listExportFile.js:308`. Hợp đồng `{headings, widths, rows, total}` khớp `fetchExportRows`. |
| Không N+1 | Lấy dữ liệu bằng `setEagerLoads([])->toBase()`, rồi mỗi nhóm danh mục nạp bằng 1 `whereIn` cho cả trang, và chỉ nạp nhóm có cột được chọn. Cây phân loại 1 query kèm 3 query eager. Report đo được 8–10 query/trang, 0,42–0,55 s cho 5.000 dòng. Đếm tổng bằng `getCountForPagination`: Laravel bỏ bindings của select khi đếm, nên các subquery có binding ở màn temp vẫn an toàn. |
| Seeder idempotent, an toàn cho prod | Không truncate. Mỗi lượt chạy là 1 transaction, khoá dòng bằng `lockForUpdate`. Id bị quyền khác chiếm, hoặc tên đã nằm ở id khác, thì ném lỗi và không ghi gì. Không gán role nào. Có xoá cache spatie. Đã SELECT: `hrm_erp_giacty` có đúng 1 dòng 1654, tên đúng, type 9, nhóm Hàng hoá, 0 dòng `role_has_permissions`. `hrm_erp` chưa có 1654 và chưa có tên trùng. Seeder trên `gop_db`, `origin/gop_db`, `feat/cdhh-2c-xe`, `feat/p2d1-mau-tem` và `feat/cdhh-p4-5-out-of-stock` không có `'id' => 1654`. Runbook mục 6 bước 1 đã có lệnh chạy. |
| Test ép trùng mã đi qua đường retry thật, không pass giả | Đã SELECT: chỉ mục UNIQUE `products_code_unique` có trên DB test. Hàng chiếm mã được chèn bên ngoài savepoint của A, nên `save()` lượt 1 đụng UNIQUE thật (23000), rồi `storeWithRetry` mới gọi generator lần 2. Test chốt `count($spy->codes) === 2` và mã lưu bằng `<mã>:01`, không có cách nào xanh nếu không đi qua nhánh catch. Ca 2 chốt đúng `CODE_RETRY` lượt, message có `products_code_unique`, không để lại hàng dở. Generator gián điệp được tiêm qua container (constructor `ProductWriteService`), nên chắc chắn là service thật dùng nó. |
| EOL | 9 file đụng tới đều là LF, 0 CR. Numstat của `PermissionsTableSeeder` là `2 +/1 -`, chỉ có dòng comment và dòng 1654. |

## Critical

Không có.

## Important

Không có.

## Minor

**M1. Gate quyền màn company/entering đọc quyền ở mọi công ty (lỗi có sẵn, export kế thừa).**
`Routes/api.php:452-457` dùng middleware `checkPermission`. Middleware này đọc `getAllPermissions()`, không lọc theo công ty
(`app/Http/Middleware/CheckPermission.php:33-38`).
- Kịch bản: NV có 1653 ở Cty B, có 1654 ở Cty A, và đang làm việc ở Cty A.
- Hệ quả: NV xuất được file "Dữ liệu hàng hoá công ty" của Cty A, dù ở Cty A không có quyền xem màn đó.
- Màn danh sách `/company` đang hở y hệt, nên export chỉ đúng như brief yêu cầu ("giống route danh sách"). Theo §35b, thông tin
  hàng hoá không bảo mật, nên ảnh hưởng thấp.
- Đề xuất: ghi vào danh sách ngoài luồng. Nếu muốn chặt hơn thì thắt cả route danh sách lẫn export bằng
  `isCurrentEmployeeHasPermission(1652|1653)`. Đừng chỉ thắt riêng export, vì như thế sẽ lệch với màn.

**M2. Ca "1654 ở công ty khác ⇒ 403" không chứng minh được lớp nào đã chặn.**
`ProductExportApiTest.php:166` chỉ `assertStatus(403)`. Hiện tại ca này đúng là đi qua controller: `teams=false`, nên middleware thấy
1654 của Cty 1 và cho qua. Nhưng nếu sau này controller bị gỡ check, mà middleware lại được đổi sang đọc theo công ty, ca vẫn xanh
dù đã mất một lớp. Đề xuất: thêm `->assertJsonFragment(['message' => '…ở công ty đang làm việc'])`, hoặc assert message khác message
của middleware.

**M3. Chưa có test chốt "bộ lọc export = bộ lọc list".**
Code dùng chung `index()` nên rủi ro thấp, nhưng chưa ca nào truyền một bộ lọc thật rồi so `total` của export với `meta.total` của
list, ví dụ `company_status`, `job_cluster_id`, `uncatalogued`, `usage=unused`. Nên thêm 1 ca, vì nếu sau này ai tách nhánh lọc riêng
cho export thì không test nào bắt được.

**M4. `limit` không phải số thì về 1 chứ không về mặc định.**
`ProductExportService.php:96`: `limit=abc` → `"abc" ?: 2000` = `"abc"` → `(int)` = 0 → `max(1, 0)` = 1. FE luôn gửi số nên vô hại,
chỉ lệch với mô tả trong report ("0/âm về mặc định / 1"). `page` cũng không có trần trên, nên `page` rất lớn sinh OFFSET lớn và trả
mảng rỗng. Vô hại.

**M5. `open_requests_text` dựa trên `GROUP_CONCAT` (có sẵn, kế thừa từ list).**
`PriceAskingProductReader::openRequestsSql` không đặt `group_concat_max_len`, nên chuỗi bị cắt ở 1024 byte. Mỗi phiếu khoảng 20–25
byte, nên phải có trên khoảng 40 YCHG mở cùng chứa 1 hàng tạm thì mới bị cắt, gần như không xảy ra. Màn danh sách cũng bị y như vậy.
Chỉ ghi lại để biết.

**M6. Chưa có test cho một số đường.**
Chưa có ca cho: cột `trading_company_names` nhiều dòng ở Kho; màn entering có dữ liệu thật đi hết các cột (giacty đang có 0 dòng);
và ca "Super admin role 18 không có 1654 ⇒ 403". Code không có nhánh bypass nên ca cuối thuần là để chốt hành vi. Có thể bổ sung ở
T4.

## Ghi chú

- Report §5 đo hiệu năng ở tầng service, chưa gồm HTTP, JWT và middleware. T4 nên đo lại qua cổng 8031 bằng role tạm.
- `PermissionService` lấy role qua `employee->roles` (mọi công ty) rồi lọc theo `role_has_permissions.company_id`, chứ không lọc
  `employee_has_roles.company_id`. Đây là ngữ nghĩa chung của cả hệ thống, không thuộc đợt này.
