# Phiếu Yêu cầu nhập hàng (ERP → HRM) — design tóm tắt

> Phụ trách: @junfoke · Bắt đầu: 2026-08-13 · Nhánh: `feat/finance-product-import-request` (checkout từ `gop_db`, cả 2 repo)
> Worktree: `hrm-api/.worktrees/finance-product-import-request` + `hrm-client/.worktrees/finance-product-import-request`
> Khuôn mẫu bám theo: `.plans/gop-db/finance-product-transfer-request/` (@khoipv)

## Mục tiêu

Port màn ERP "Phiếu Yêu cầu nhập hàng" (`admin/warehouse/product_import_requests/all`,
7 bảng `product_import_requests` + details + detail_customers + tabs + tab_products + versions + histories)
sang HRM phân hệ **Tài chính**, nhóm **Nhập hàng** (slot xám `finance.js:95` — `{ label: 'Yêu cầu nhập hàng' }`).
Theo sơ đồ v1.6 dòng 535: `ERP > Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > Yêu cầu nhập hàng`.

**HRM là bản thay thế lâu dài** — 2 cổng chạy song song cùng bảng trên DB gộp, **KHÔNG đổi schema**.

## Hiện trạng ERP

| Thành phần | Số liệu |
| --- | --- |
| `Warehouse\ProductImportRequestsController` | 1.530 dòng |
| `Model\Warehouse\ProductImportRequest` (+6 model con) | 1.892 dòng |
| Blade | 5.221 dòng (`form` 1.533 · `show` 2.099 · `create` 491 + 5 màn list) |
| Trạng thái | 12 |
| Loại phiếu (`type`) | 8 loại tạo tay + 4 loại sinh tự động |
| Màn danh sách | 5 (`index`, `all`, `forManager`, `forDepartmentManager`, `forAccounting`) |
| Mẫu in | `ReportTemplate::YEU_CAU_NHAP_HANG = 44` |

### 5 màn danh sách = 1 query, khác đúng 1 nhánh `where`

Tất cả chạy chung `ProductImportRequest::searchByFilter()` (`app/Model/Warehouse/ProductImportRequest.php:1249-1330`),
rẽ nhánh theo `$request->type`:

| `type` | Màn ERP | Lọc | Lối vào ERP |
| --- | --- | --- | --- |
| `all` | all | Phạm vi theo 4 quyền cấp; ẩn phiếu "Đang tạo" của người khác | Menu **Khởi tạo > Hàng hóa** + **Kế toán > HH-DV-VC** |
| `for_approve` | index?type=for_approve | `status = 2` + cùng công ty | Menu **Chờ duyệt** + widget dashboard KE_TOAN_KHO |
| `managerApprove` | forManager | `status = 10` (BKS) / `11` (BGĐ) theo quyền | Widget dashboard XUAT_NHAP_HANG |
| `departmentManagerApprove` | forDepartmentManager | `status = 12` + phòng ban mình quản lý | Widget dashboard |
| `accounting` | forAccounting | `status != 0` và `!= Đang tạo`, gate "Kế toán kho" | **Đã bỏ khỏi menu** (chỉ còn `topmenubar_old`) |
| *(rỗng)* | index | `created_by = mình` | **Đã comment khỏi menu** |

## Quyết định đã chốt (user 2026-08-13)

1. **1 mục menu duy nhất** — fill slot xám `finance.js:95`, KHÔNG thêm mục "Chờ duyệt" riêng.
2. **1 màn danh sách duy nhất** nhận query `?type=`, mặc định `all`; port thêm 3 preset
   `for_approve` / `managerApprove` / `departmentManagerApprove` để luồng duyệt trọn vẹn trong HRM.
   **Bỏ** `accounting` (menu ERP đã bỏ) và `index` mặc định (menu đã comment).
   Ai có quyền duyệt thì **hiện thêm hành động duyệt tương ứng** ngay trên màn, không tách màn.
3. **Form tạo/sửa: 8 loại** đúng như `IMPORT_TYPES` (`public/js/constant.js:223`) —
   2 Nhập hàng mua ngoài · 3 mượn trả lại · 4 bán trả lại · 9 bán(khi mượn) trả lại ·
   11 mua nước ngoài (mới) · 14 nhập hàng gửi · 15 mua trong nước (TỰ DO + HÃNG) · 99 khác.
   **Danh sách + chi tiết phải hiển thị được 12 loại** (`ALL_IMPORT_TYPES` — thêm 6 điều chuyển nội bộ,
   7 điều chuyển chi nhánh, 8 nhập ghép, 10 nhập tách; 4 loại này sinh tự động, không tạo tay).
4. **Quyền: dùng lại quyền ERP + thêm bản ghi `guard_name='api'` trùng tên** (xem mục Phân quyền).
5. **HRM chỉ ghi status do người dùng thao tác**: 3 (Đang tạo), 2 (Chờ duyệt), 10/11/12 (chờ BKS/BGĐ/TP),
   6 (Đã hủy). Status 1, 4, 5, 7, 8, 9 do chuỗi kho–kế toán ERP đẩy → HRM chỉ hiển thị.

## Phân quyền — bẫy guard `web` vs `api`

Trên DB gộp `gop_db`, quyền ERP là `guard_name = 'web'`, quyền HRM là `'api'`:

| id | Tên quyền | guard | Dùng ở đâu |
| --- | --- | --- | --- |
| 100874 | Xem yêu cầu nhập hàng theo tổng công ty | web | phạm vi `type=all` |
| 100875 | Xem yêu cầu nhập hàng theo công ty | web | phạm vi `type=all` |
| 100876 | Xem yêu cầu nhập hàng theo phòng ban | web | phạm vi `type=all` |
| 100877 | Xem yêu cầu nhập hàng theo bộ phận | web | phạm vi `type=all` |
| 100984 | Trưởng phòng duyệt yêu cầu nhập hàng | web | `departmentManagerApprove`, duyệt status 12 |
| 100339 | Ban kiểm soát duyệt giá nhập hàng trả lại | web | `managerApprove`, duyệt status 10 |
| 100340 | BGD duyệt giá nhập hàng trả lại | web | `managerApprove`, duyệt status 11 |
| 100080 / **1136** | Kế toán kho | web / **api** | duyệt status 2, reject — **bản api đã có sẵn** |

**Cách xử lý — theo precedent `finance-product-transfer-request`, KHÔNG dùng middleware:**
kiểm quyền **trong Entity**, query thẳng pivot `permissions` → `employee_has_permissions` /
`employee_has_roles` + `role_has_permissions`, so khớp theo **TÊN**, **không lọc `model_type`,
không lọc `guard`**. Thêm memoize tĩnh theo request (ListResource gọi cờ quyền cho từng dòng).
Kèm theo vẫn thêm bản ghi quyền `guard_name='api'` **trùng tên** vào `PermissionsTableSeeder`
(spatie unique theo cặp `name + guard_name` nên không đụng bản ERP) để quyền hiện đúng tab
phân hệ Tài chính (`type = 8`) ở màn Phân quyền HRM.

⚠️ **KHÔNG** dùng middleware `checkPermission` — trên DB gộp role gán từ ERP lưu
`model_type='App\Employee'`, spatie lọc theo class HRM nên bỏ sót → user có quyền thật vẫn 403
(đã verify ở `finance-product-transfer-request` D8).
⚠️ **KHÔNG** dùng `App\Helpers\ErpPermissionHelper` / middleware `erpPermission` — precedent
`Modules/Finance/Services/CompanyAccountService.php` đã cấm dùng lại (helper còn đọc qua `mysql2`,
thuộc mục tiêu 0 của `gop-db/design.md` là gỡ bỏ).
⚠️ **Resolve tên quyền phải `pluck()` TẤT CẢ id trùng tên rồi `whereIn`**, KHÔNG `value('id')` —
sau khi thêm bản api trùng tên, `value('id')` chỉ bắt id nhỏ (bản HRM) → user giữ quyền qua role
ERP cũ mất quyền (bài học D17 của precedent).
⚠️ **Super admin (role id 18)** phải xử lý tường minh — ERP có `Gate::before` bypass mọi `->can()`,
bản port không có. Nhưng Super admin chỉ thay thế vế **quyền**, các vế so `company_id` giữ nguyên.
⚠️ **KHÔNG** đổi `guard_name` bản ERP sang `api` — màn ERP cũ dùng `->can()` guard web sẽ mất quyền.
⚠️ Chỉ đổi `type`/`group` bản ghi ERP là **không đủ** — FE `store.state.permissions` chỉ nạp guard api.

### Lỗ hổng phạm vi cần vá khi gộp màn

`canView()` (`ProductImportRequest.php:1451`) **có** cho xem nếu user có quyền BKS/BGĐ,
nhưng nhánh `type=all` của `searchByFilter` **không** — chỉ lọc theo 4 quyền cấp 100874-877.
Khi gộp 5 màn về 1, người duyệt (BKS/BGĐ/TP) không có quyền cấp sẽ **không thấy phiếu cần duyệt**
ở preset `all`. → nhánh `all` phải `orWhere` thêm tập phiếu mà user có quyền duyệt
(status 10/11/12 theo đúng điều kiện của `managerApprove` / `departmentManagerApprove`).

## Điểm kỹ thuật chính

- BE `Modules/Finance`, routes `/v1/finance/product-import-requests`. **KHÔNG dùng `mysql2`**.
- Không đổi schema; 7 bảng giữ nguyên tên ERP trên DB gộp.
- Cờ hành động trả theo từng dòng/chi tiết từ Entity: `canView` `canEdit` `canCancel` `canApprove`
  `canApproveByManager` `canControlBoardApprove` `canBoardOfManagerApprove` `canDeny` `canProductImport`
  — port nguyên, không tự chế điều kiện.
- Mẫu in: `ReportTemplate` id **44** + `fillReport()`.
- Đính kèm PDF trên S3 (`CmcS3Helper`); ⚠️ ERP `deleteFile` unlink `public_path` trong khi file ở S3 —
  kiểm tra và sửa như precedent đã làm.
- Thông báo: ERP bắn qua `NotificationHelper::sendNotifyWithPermission('Trưởng phòng duyệt yêu cầu nhập hàng', …)`
  — 2 cổng cùng reo vì chung bảng notification ERP.
- Phiếu YCNH được tạo từ ~5 nguồn upstream qua `?type=` (thông báo hàng về, hàng về nội địa, đơn mua…)
  và đẩy xuống Đề nghị nhập kho / Trả lại NCC / Phiếu nhập hàng. Các nút "Tạo YC nhập hàng" bên ERP
  **vẫn trỏ về ERP** — chấp nhận, giống precedent.
- FE đọc skill `button-convention`, `modal-popup`, `form-validate`, `unsaved-changes`;
  áp 4 bài học phân trang màn danh sách V2; menu 1 link = 1 phân hệ (gotcha `resolveSubsystem`).

## 6 phase

1. BE nền — Entity + Resource + `searchByFilter` 4 preset + quyền
2. FE danh sách — 1 trang, preset `?type=`, bộ lọc 12 loại
3. Form tạo/sửa — **tách 3a / 3b**, xem mục dưới

4. Chi tiết + 4 luồng duyệt (Kế toán kho / BKS / BGĐ / TP) + từ chối + lịch sử
5. In (mẫu 44) + Export Excel + đính kèm S3
6. Verify — HTTP + Playwright + đối chiếu 2 cổng

## ⚠️ Phát hiện 2026-08-14 — form KHÔNG phải form nhập tự do

Cả 8 loại đều **bắt buộc chọn 1 chứng từ nguồn**; hàng hoá kéo từ chứng từ đó xuống, người dùng
KHÔNG tự thêm dòng hàng. Mỗi loại lấy từ một module ERP khác nhau:

| Chứng từ nguồn | Bảng ERP | Loại | Số phiếu thật trên `gop_db` |
| --- | --- | --- | --- |
| **Phiếu YC xuất hàng** | `product_export_requests` | 3, 4, 14, 99 | **6.592** |
| Báo hàng về nội địa mới | `inland_product_arrived_news` | 15 | 2.145 |
| Phiếu báo hàng về | `product_arrived_notifies` | 2 | 714 |
| Hợp đồng mua / YC nhập khẩu | `buy_contract2`, `order_import_requests` | 11 | 634 |
| Phiếu YC xuất bán hàng mượn | `borrow_sell_requests` | 9 | 83 |

Mỗi nguồn cần 1 hàm dựng dữ liệu riêng (`getDataFor*` bên ERP, 13-98 dòng) + 1 popup tìm kiếm
riêng ở FE. DB đã gộp nên HRM đọc thẳng bảng nguồn, **không phải port cả module ERP**.

2 ràng buộc lấy từ code ERP:
- Loại **11 (mua nước ngoài mới)**: `canEdit()`/`canCancel()` loại trừ → **chỉ có luồng tạo**,
  không sửa/huỷ.
- Loại 9 chỉ 83 phiếu, phiếu mới nhất 09/07/2026 → ít dùng.

### Chia phase (user chốt 2026-08-14)

- **Phase 3a**: khung form + 4 loại dùng chung nguồn `product_export_requests` (3, 4, 14, 99)
  = 6.592/11.000 phiếu. Có khung chạy được sớm để duyệt trước khi nhân bản.
- **Phase 3b**: 4 loại còn lại (15, 2, 11, 9) — mỗi loại 1 nguồn + 1 popup.
