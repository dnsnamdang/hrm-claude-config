# Phase C — PPBHĐC (Phân bổ hàng điều chuyển chi nhánh, type 7) — Design

> Nối tiếp `design.md` §6 (D5) + Phase A/B đã xong. Bước CUỐI của chuỗi nhập type 7 non-direct:
> PYCCH **11 Đã nhập hàng** → (PPBHĐC duyệt) → **12 Đã phân bổ**.
> Nguồn ERP (read-only): `app/Model/Warehouse/TransferProductAllocation.php` + `TransferProductAllocationsController.php`.
> Directive cứng: GIỐNG ERP 1:1, dữ liệu lưu đúng như ERP. LOCAL trên `develop`.

## 1. Bản chất
PPBHĐC = **TransferProductAllocation** — phiếu do NV công ty ĐÍCH lập sau khi Phiếu nhập hàng type 7 (non-direct)
hoàn thành, để **phân bổ số đã nhập về đúng người yêu cầu** (người lập PYCCH), ghi `allocated_qty` lên
PYCCH và **giữ hàng (prepick)** cho người đó tại kho/công ty ĐÍCH. KHÔNG có bút toán.
- Chỉ áp dụng type 7 **non-direct** (nhập thẳng `is_import_direct` đã trừ `ProductImportDirectDetail` ở Phase B, bỏ qua PPBHĐC).
- Nhập về kho → hàng nằm chung tồn kho đích; PPBHĐC chia về từng người YC.

## 2. Hiện trạng HRM (khảo sát 2026-10-23)
**ĐÃ chừa sẵn (không phải làm lại):**
- Bảng `transfer_product_allocations` + `transfer_product_allocation_details` **đã tồn tại trong DB chung `erp_hrm_check`** (ERP dùng) → **KHÔNG migration** (quy tắc gop_db: ghi thẳng bảng ERP cũ).
- `ProductTransferRequest::STATUSES` đã khai **id=12 'Đã phân bổ'** (:110-114, type success).
- `allocated_qty` đã `$fillable` ở `ProductTransferRequestProduct.php:31` + `ProductTransferRequestProductDetail.php:24`; trả về `ProductTransferRequestDetailResource.php:51,58`.
- Prepick port đầy đủ: `PrepickStockService` (nơi DUY NHẤT ghi `prepick_details`/`prepick_logs`).
- FE chi tiết PYCCH đã render cột "Được nhận" khi `status===12` (`pages/finance/product-transfer-requests/_id/index.vue:44,316-318`).

**CÒN THIẾU (toàn bộ tầng GHI phân bổ — làm mới):**
- Entity `TransferProductAllocation` + `TransferProductAllocationDetail` (map bảng sẵn có).
- Service phân bổ (`approve()` logic) — ghi `allocated_qty`, ghi prepick đích, set PYCCH→12.
- Controller + routes + (quyền).
- FE màn PPBHĐC (lập + duyệt + chi tiết).

## 3. Logic `approve()` — bám ERP `TransferProductAllocation::approve()` :179-263 (1:1)
Trong 1 transaction, duyệt từng detail (BỎ QUA `allocate_qty <= 0`):
1. **Cộng allocated_qty** (KHÔNG idempotent — ERP guard bằng `canEdit` status==3):
   - `ProductTransferRequestProductDetail` (khớp `request_id`+`detail_id`): `allocated_qty += allocate_qty` (:190-191).
   - `ProductTransferRequestProduct` (khớp `request_id`+`product_id`): `allocated_qty += allocate_qty` (:193-194).
2. **Tìm lô** `WarehouseImportLot` theo `product_import->warehouse_import_id` + product + unit (:196-199); `prepick_qty = allocate_qty × lot->unit_coefficient` (:200).
3. **Ghi giữ hàng (prepick)** qua `PrepickStockService` (HRM) — tương đương ERP ghi PrepickDetail/PrepickLog:
   - `company_id = product_import->company_id` = **công ty ĐÍCH** (:212) ⚠️ KHÔNG phải cty nguồn/PTR.
   - `employee_id = ptr.created_by` (người lập PYCCH = người giữ).
   - `customer_id`, `expire_date` từ detail.
4. **Set status=12** cho **TẤT CẢ** `product_transfer_requests` của `product_export_request_id` (:246-249) — không chỉ các dòng được phân bổ.
5. Notification + Redis (:251-262) → **hoãn chung pass F2** (nhất quán type 6, lệch cố ý — như Phase A/B).
6. **KHÔNG bút toán.** Nhánh `Stock->prepick_qty` (:203-207) ERP comment out → **KHÔNG kích hoạt**.

`generateCode` → **PPBHĐC-xxxxx** (:105-108). `canView`/`canEdit`: chỉ `created_by` + `status==3` (:110-116).
`canCreateTransferProductAllocation()` (ProductImport.php:892-898): hard-block `type!=7` và `is_import_direct`.

## 4. Bảng (đã tồn tại — chỉ map entity)
- `transfer_product_allocations`: id, code (unique), product_import_id (FK), product_export_request_id (FK), note, status int (3=Đang tạo, 1=Đã duyệt — hardcode ERP), created_by/updated_by, timestamps.
- `transfer_product_allocation_details`: id, parent_id (FK), product_id (FK), employee_id (FK=người giữ), allocate_qty decimal(12,2), prepick_qty decimal(12,2) nullable, expire_date date, customer_id (FK), request_id (FK=product_transfer_requests), detail_id (FK=product_transfer_request_product_details).

## 5. Bẫy port (bắt buộc giữ)
1. `company_id` prepick = `product_import->company_id` (ĐÍCH), KHÔNG lấy từ PTR/PXK (nguồn).
2. `employee_id` = `ptr.created_by` (ràng người giữ), KHÔNG phải người lập PPBHĐC.
3. status=12 set cho MỌI PTR của PXK, không chỉ dòng được phân bổ.
4. `+= allocate_qty` KHÔNG idempotent → chặn duyệt lại bằng `canEdit` status==3 (y ERP).
5. `code` random rồi `generateCode` phải CÙNG transaction với store.
6. KHÔNG bật lại nhánh `Stock->prepick_qty` đã comment.
7. Màn CHỈ type 7 non-direct (không dùng chung type 6; type 6 nội bộ không có PPBHĐC).
8. Mang theo 2 bug ERP đã vá ở phase trước nếu chạm hàm chung (lọc company_id + root_objectable) — kiểm lại khi port prepick đích.

## 3b. Create / Store / Validate / Sync (bám ERP controller + model)
**Guard lập phiếu** `ProductImport::canCreateTransferProductAllocation()` (ERP :892-898) → tất cả đúng mới cho:
`type == 7` · ProductImport `status == 1` (Phiếu nhập hàng ĐÃ hoàn thành — map HRM = DA_HOAN_THANH) · người đăng nhập == `product_import.created_by` · `!is_import_direct` · **chưa có** `TransferProductAllocation` nào cho `product_import_id` (1 phiếu/lần nhập).

**Load data màn lập** `ProductImport::getDataForTransferProductAllocation($importId)` (ERP :578-608): trả `warehouse_import.products` (lô đã nhập) + `requests` (ProductTransferRequestProduct theo mọi PYCCH của PXK, kèm `allocated_qty`/`customers`/người lập) + `product_export_request` + `product_import`. Dùng để FE dựng bảng phân bổ (mỗi SP × từng người YC × từng dòng customer/detail).

**store()** (ERP controller :82-174): validate (rule bên dưới) → tạo `TransferProductAllocation` (`product_import_id`, `product_export_request_id` = từ `product_import.product_import_request.product_export_request_id`, `note`, `status` 1|3, `code = randomString(16)` rồi `generateCode()` CÙNG transaction) → `validateDetails($products)` (rollback nếu false) → `syncDetails($products)` → nếu `status==1` gọi `approve()`. **update()** (:190-272) = parity, chỉ khi `canEdit` (created_by + status==3).

**validateDetails** (ERP model :118-156): mỗi (product_id+unit_id): từng dòng customer `allocate_qty <= detail.qty - detail.allocated_qty`; tổng allocate của SP phải **== đúng** `min(group.qty - group.allocated_qty, lot.qty)` (ERP: `if ($qty > $max || $qty > $import->qty || ($qty < $max && $qty < $import->qty)) return false` → phải khớp CHÍNH XÁC phần còn lại hoặc tồn lô).
**syncDetails** (:158-177): xóa hết detail cũ rồi tạo lại, BỎ QUA `allocate_qty == 0`.

**Rule store/update** (ERP :83-98): `product_import_id` exists; `products[]`; `product_id`/`unit_id` exists; `requests[].employee_id`/`request_id` exists; `customers[].customer_id` exists; `allocate_qty` numeric 0..999999999; `expire_date` date `after_or_equal:tomorrow`; `detail_id` exists product_transfer_request_product_details; `status in:1,3`.

## 6. QUYẾT ĐỊNH ĐÃ CHỐT (user, 2026-10-23) — A / A / A
- **Q1 → A:** nút **"Phân bổ hàng"** trên **chi tiết Phiếu nhập hàng** (ProductImport) type 7 non-direct khi `status==1` (hoàn thành) + `canCreate` → mở màn/popup lập phiếu phân bổ. KHÔNG menu riêng (bám ERP).
- **Q2 → A:** gate y ERP bằng method `canCreate/canView/canEdit` (người tạo + status), **KHÔNG thêm quyền mới**. (Lệch quy ước `erp-to-hrm-screen` là CỐ Ý — directive "làm giống erp".)
- **Q3 → A:** làm trọn FE Phase C (lập + duyệt + chi tiết), đóng vòng type 7 non-direct end-to-end.

## 7. Ràng buộc
LOCAL `develop`; không đụng WIP đồng đội; không sửa ERP; không migration (bảng sẵn có); PHP 7.4; FE `V2Base*`; "Người tạo/Ngày tạo"; số định dạng quốc tế; prepick chỉ ghi qua `PrepickStockService`.
