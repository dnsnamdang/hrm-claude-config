# Xuất điều chuyển kho NỘI BỘ (type 6) — Design tóm tắt

> Phần của port PXK ERP→HRM. Nhóm "điều chuyển": type 5 (cùng thủ kho — XONG), **type 6 (nội bộ — feature này)**, type 7 (chi nhánh — sau).
> Nhánh: cả 2 repo `develop`. Làm **LOCAL**, không push/merge tới khi user yêu cầu.
> Nguồn ERP (read-only): `ERP/TanPhatDev`. Directive cứng: **làm GIỐNG ERP 1:1**, dữ liệu lưu đúng như ERP.

## 1. Mục tiêu
Port loại **XUAT_DIEU_KHO_NOI_BO = 6** (ERP `ExportModel.php:16`) sang HRM, nối trọn chuỗi
YCXH → ĐNXK → PXK (hạch toán xuất) → **tự sinh YCNH** → ĐNNK → PNK → hạch toán nhập → kết thúc.

## 2. Bản chất & khác type 5
- **Type 5** (cùng thủ kho): qua class `WarehouseTransfer`, PXK+PNK đồng thời 1 lượt → **có màn riêng** `/finance/warehouse-transfers` (ERP cũng có màn `warehouseTransfer`). **GIỮ NGUYÊN.**
- **Type 6** (nội bộ): 2 kho **khác thủ kho, cùng Công ty**; **KHÔNG** qua `WarehouseTransfer`; đi chứng từ thường, **tách nhiều bước**, chuỗi duyệt 2 đầu kho.

## 3. UI — KHÔNG tách màn (ERP không có màn riêng cho type 6)
- Dùng **màn YCXH dùng chung** (`product-export-requests`) với loại phiếu = 6. KHÔNG màn/menu mới.
- Chuỗi chứng từ nhập (YCNH/ĐNNK/PNK/hạch toán nhập) chạy trên các màn Finance ĐÃ PORT.
- Rule chốt với user: *"ERP không có màn thì HRM cũng không tách màn."*

## 4. Luồng + máy trạng thái YCXH (ProductExportRequest)
```
B1  Lập YCXH type 6 (màn YCXH dùng chung)  → validate: warehouse_id ≠ import_warehouse_id; 2 kho cùng Công ty
B2  ĐNXK → PXK kho NGUỒN                    → TRỪ tồn kho nguồn
B3  Hạch toán xuất (ProductExport):
      • YCXH → 14 CHO_DUYET_NHAP, is_completed=true
      • TỰ SINH YCNH type 6, status=2, warehouse_id=import_warehouse_id (kho đích),
        supplier_price = export_price × unit_coefficient            ← ĐIỂM NỐI còn thiếu ở HRM
B4  Thủ kho ĐÍCH lập ĐNNK (ref YCNH):  nháp → YCXH 15;  chờ duyệt → YCXH 16
B5  Duyệt ĐNNK (thủ kho kho đích)  → YCXH 17 DANG_NHAP_KHO_NHAP, YCNH → 4
B6  PNK kho ĐÍCH                    → CỘNG tồn kho đích, YCXH 18
B7  Hạch toán nhập (ProductImport)  → YCXH 19 → 5 DA_HACH_TOAN (kết thúc)
      • nhập < xuất → tự sinh "nhập trả lại điều chuyển" (loại 17) phần lệch
```
Trạng thái YCXH type 6: `14 → 15/16 → 17 → 18 → 19 → 5`. (Type 5 đi thẳng 5.)

## 5. Quyết định đã xác minh từ ERP (bằng chứng file:dòng ở spec)
| # | Điểm | Kết luận ERP (bám đúng) |
|---|---|---|
| D1 | **Bút toán** | **KHÔNG sinh AccountDetail** cả 2 phía — chỉ đổi tồn `accounting_stock` + mốc theo dõi. `getDataCreateDept` xuất/nhập đều KHÔNG có nhánh type 6 → `$accounts=[]`. `getPriceSetted` vẫn gồm type 6 (định giá vốn tồn, KHÔNG phải journal). ProductExport.php:589-874 / ProductImport.php:2074-2392 |
| D2 | **Prepick/Hold** | Trừ tồn kế toán vật lý mọi dòng; nếu phiếu có `export_from_hold/prepick > 0` thì trừ thêm HOLD/PREPICK theo `product_export_request.created_by`; prepick vẫn lọc `customer_id`; đi đường `updateWarehouse` thường (nhánh `else`), KHÔNG `WarehouseTransfer`. ProductExport.php:1345-1421 |
| D3 | **Duyệt ĐNNK** | Thủ kho kho đích `isWarehouseStocker(warehouse_id)` + status=2, **không gate theo type**; `canCancel` **loại trừ** type 6 (người tạo không tự hủy ĐNNK type 6). WarehouseImportRequest.php:423-425,472-475,552 |
| D4 | **receiver_id** | YCNH type 6 tự sinh **KHÔNG gán** `receiver_id`; chỉ notification→người hạch toán xuất. ProductExport.php:1896-1941 |

## 6. Hiện trạng HRM
**ĐÃ có + đã commit (phía nhập):** YCNH/ĐNNK/PNK/hạch toán nhập xử lý type 6; `ProductImportService::completeInternalTransfer()` + tự sinh "nhập trả lại" loại 17 (`createInternalTransferReturnRequest`); cộng tồn qua `PhysicalStockWriter`; status 14-19 (khai ở Assign `ProductExportRequest`).

**CÒN THIẾU (phía xuất + điểm nối):**
1. **Hằng loại type 6 phía XUẤT** — `WarehouseExportRequest` + `ProductExportRequest` (Assign): thêm `XUAT_DIEU_KHO_NOI_BO=6` + getTransferTypes + nhãn.
2. **Điểm nối (blocker)** — `ProductExportService`: sau hạch toán PXH type 6 → set YCXH về 14 + **tự sinh YCNH type 6** (port ERP `ProductExport.php:1876-1946`).
3. **FE** — thêm loại 6 vào dropdown "Loại phiếu" màn YCXH dùng chung + field kho đích (import_warehouse_id) khi type=6; validate kho nguồn≠đích, cùng công ty.

## 7. Ràng buộc
LOCAL trên `develop`; không đụng WIP đồng đội (ProductExportController/CustomerManagerService api; product-exports/create.vue client); không sửa ERP; quyền mới (nếu cần) ở `PermissionsTableSeeder` guard `api`; số định dạng quốc tế; nhãn "Người tạo/Ngày tạo"; FE dùng `V2Base*`.

## 8. Quyết định đã chốt (SKILL vs SPEC / lệch so với ERP)
- **F1 — ghi ngược exported_qty (ĐÃ VÁ, bám ERP 1:1):** `finalizeInternalTransferExport` phải ghi ngược
  `exported_qty += qty` / `base_exported_qty += export_qty` về `product_export_request_details` TRƯỚC khi
  set status YCXH — ERP `ProductExport::updateWarehouse:1856-1874` chạy vòng này vô điều kiện cho MỌI loại.
  Bản đầu thiếu (chỉ type 6, các finalize khác đều có) → final review bắt, đã thêm (commit `9e40d7c6f`),
  cộng dồn atomic copy pattern `finalizeGenericExport`.
- **F2 — KHÔNG bắn notification (lệch CÓ CHỦ Ý, nhất quán HRM):** ERP :1936-1945 tạo Notification + Redis
  publish tới người hạch toán. HRM KHÔNG port — **nhất quán với mọi finalize anh em** (`finalizeGenericExport`,
  `finalizeFirmContractExport` đều không bắn). Notification điều chuyển sẽ port chung một pass sau theo
  `notification-convention` của HRM (khác cơ chế Redis ERP), KHÔNG làm riêng cho type 6.
- **FE tách phase sau:** dropdown loại 6 + field kho đích (`import_warehouse_id`) + validate kho nguồn≠đích/cùng
  công ty trên màn YCXH dùng chung — cần brainstorm UI riêng (SKILL thắng SPEC về trình bày), KHÔNG gộp plan này.
