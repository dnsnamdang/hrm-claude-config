# Xuất điều chuyển kho CHI NHÁNH (type 7) — Design tóm tắt

> Phần của port PXK ERP→HRM. Nhóm "điều chuyển": type 5 (cùng thủ kho — XONG), type 6 (nội bộ cùng công ty — XONG), **type 7 (chi nhánh, KHÁC công ty — feature này)**.
> Nhánh: cả 2 repo `develop`. Làm **LOCAL**, không push/merge tới khi user yêu cầu.
> Nguồn ERP (read-only): `ERP/TanPhatDev`. Directive cứng: **làm GIỐNG ERP 1:1**, dữ liệu lưu đúng như ERP.
> Khảo sát gốc: scratchpad `erp-type7-branch-transfer-survey.md` + `hrm-type7-coverage-survey.md`.

## 1. Mục tiêu
Port loại **XUAT_DIEU_CHUYEN_KHO_CHI_NHANH = 7** (ERP `ExportModel.php:17`) sang HRM, nối trọn chuỗi:
PYCCH → YCXH type 7 → ĐNXK → PXK (hạch toán xuất) → **tự sinh YCNH type 7** → ĐNNK → PNK → **PPBHĐC (phân bổ hàng)** → kết thúc.

## 2. Bản chất & khác type 5/6
- **Type 5** (cùng thủ kho): class `WarehouseTransfer`, **màn riêng** `/finance/warehouse-transfers`. XONG.
- **Type 6** (nội bộ): 2 kho khác thủ kho **CÙNG công ty**; YCXH kết thúc ở **14** (→15..19). XONG.
- **Type 7** (chi nhánh): 2 kho **KHÁC công ty** (nguồn ≠ đích); có **PYCCH** (Phiếu yêu cầu chuyển hàng) do NV công ty đích lập làm nguồn; có **hệ số chi nhánh** `branch_transfer_coefficient`; YCXH kết thúc ở **5 + is_completed** (KHÁC type 6); trạng thái "đang đi" phản chiếu sang **PYCCH** (1→4→5→6→7→8→11→12); có bước **phân bổ hàng PPBHĐC** (trừ nhập thẳng).

## 3. UI — KHÔNG tách màn cho YCXH/PXK/YCNH/PNK
- YCXH/PXK/YCNH/PNK dùng **màn chung** với loại=7 (ERP cũng vậy). KHÔNG màn riêng như type 5.
- 2 màn RIÊNG: **PYCCH** (`product-transfer-requests` — HRM **ĐÃ port**) + **PPBHĐC** (`transfer_product_allocations` — ERP không có menu, vào qua redirect/nút ở danh sách PNK; HRM **CHƯA port**).

## 4. Luồng + máy trạng thái
```
B0  NV công ty ĐÍCH lập PYCCH (ProductTransferRequest)          PYCCH: 2/3
B1  Lập YCXH type 7 (màn YCXH chung): chọn export_company_id (cty NGUỒN),
      kind_of_import (1 nhập thẳng / 2 nhập về kho), product_transfer_requests[] (cùng 1 người YC)
      → company_id YCXH = export_company_id (cty NGUỒN); gộp dòng theo product+unit  YCXH 2 · PYCCH 1
B2  Kế toán kho công ty NGUỒN duyệt YCXH                          YCXH 7 (9 nếu nhập thẳng) · PYCCH 4
B3  ĐNXK → PXK kho NGUỒN (có hệ số chi nhánh)                     YCXH 4→9 · PYCCH 5→6
B4  Hạch toán xuất PXK (ProductExport):            ← ĐIỂM NỐI còn thiếu (Phase A)
      • ghi ngược exported_qty/base_exported_qty về chi tiết YCXH
      • product_transfer_requests → status 7
      • YCXH → 5 ĐÃ HẠCH TOÁN + is_completed=true   (KHÁC type 6 = 14)
      • nếu CÓ SL thực xuất: tự sinh YCNH type 7 (import_company_id = cty người lập YCXH/đích,
        status 2, currency VNĐ, KHÔNG warehouse_id, received_time=now,
        is_import_direct=1 nếu kind_of_import==1; supplier_price = export_price × unit_coefficient × branch_transfer_coefficient)
      • trừ prepick theo NGƯỜI YÊU CẦU (PYCCH[0].created_by), BỎ lọc customer, tại cty NGUỒN
B5  Người tạo YCXH (đích) duyệt YCNH                              PYCCH 8   (bỏ qua nếu nhập thẳng)
B6  ĐNNK → PNK kho ĐÍCH → hạch toán nhập                          PYCCH 11
B7  PPBHĐC (TransferProductAllocation) — chỉ khi KHÔNG nhập thẳng:
      duyệt → cộng allocated_qty + tạo prepick cho người lập PYCCH tại cty ĐÍCH   PYCCH 12
```
Nhập thẳng (`kind_of_import==1` / `is_import_direct`): bỏ PPBHĐC + bỏ duyệt YCNH; trừ `ProductImportDirectDetail` theo `product_transfer_requests[0].created_by` ở cả 2 đầu.

## 5. Quyết định đã xác minh từ ERP (bằng chứng file:dòng ở survey)
| # | Điểm | Kết luận ERP (bám đúng) |
|---|---|---|
| D1 | **Bút toán hàng** | **KHÔNG** sinh AccountDetail hàng/công nợ liên công ty cả 2 đầu. `ProductExport::getDataCreateDept` KHÔNG có nhánh type 7 → `$accounts=[]` → posting empty-success (như 12/99/6). Chỉ có bút toán CHI PHÍ chuyến giao (DeliveryTrip: Nợ 33481/6427 / Có 3311) + bốc xếp thuê ngoài — tách phase sau. |
| D2 | **YCXH kết thúc** | **status 5 ĐÃ HẠCH TOÁN + is_completed** (KHÁC type 6=14). Trạng thái "đang đi" nằm ở **PYCCH** 1→4→5→6→7→8→11→12. |
| D3 | **YCNH tự sinh** | ngay lúc hạch toán PXK, chỉ khi có SL thực xuात. `import_company_id` = cty người lập YCXH (đích); status 2; VNĐ; KHÔNG `warehouse_id`; `received_time`=now; `is_import_direct`=1 nếu `kind_of_import==1`; `supplier_price = export_price × unit_coefficient × branch_transfer_coefficient`; duyệt bởi người lập YCXH; thông báo `receiver_id`=người lập YCXH. `generateCode` "PYCNH-". |
| D4 | **Prepick** | theo `product_transfer_requests[0].created_by` (KHÔNG phải YCXH created_by); BỎ lọc `customer_id`; tại cty NGUỒN (`company_id`=YCXH company_id); trừ theo expire_date ASC, lockForUpdate, ghi PrepickLog. Nhập thẳng → trừ `ProductImportDirectDetail`. |
| D5 | **PPBHĐC** | bước riêng SAU hạch toán PNK, chỉ khi !is_import_direct. `approve()`: cộng allocated_qty, tạo prepick cho người lập PYCCH tại cty ĐÍCH (`product_import->company_id`); PYCCH→12. Chỉ người tạo thấy, không menu. |
| D6 | **Giá vốn** | `canUpdateUnitCostPriceFromSupplierPrice()` luôn `false` → hệ số chi nhánh KHÔNG cập nhật giá vốn. VAT type 7 lấy `vat_percent` HIỆN TẠI của SP. |

## 6. Hiện trạng HRM (khảo sát coverage)
**ĐÃ có + đã commit:**
- YCXH type 7 tạo/sửa/xóa/chi tiết BE+FE (`ProductExportRequestService::createFromTransfer`, `syncProductTransferRequests`); dropdown/CREATABLE/DROPDOWN/FILTERABLE có 7; field `export_company_id`/`kind_of_import`/`product_transfer_requests[]`; FE form + `TransferRequestSearchModal`.
- Màn PYCCH (`product-transfer-requests`) + liên kết ngược.
- Hằng + scope + canApprove YCNH type 7 (`NHAP_DIEU_CHUYEN_KHO_CHI_NHANH=7`, duyệt theo người lập YCXH nguồn); validate SL nhập == SL đề nghị; đặt `product_transfer_requests.status=9` khi bắt đầu nhập.

**CÒN THIẾU (chia phase):**
- **Phase A (điểm nối XUẤT — blocker):** hằng tên type 7 phía xuất; posting type 7 empty-success; `finalizeBranchTransferExport` (ghi ngược exported_qty + PYCCH→7 + YCXH→5+is_completed + tự sinh YCNH type 7); trừ prepick requester/customer-blind + nhánh nhập thẳng.
- **Phase B (NHẬP đóng vòng) — ĐÃ CHỐT edit-site (khảo sát 2026-10-23):** mở loại 7 ở `ProductImportService` để lập/hoàn thành Phiếu nhập hàng + đóng PYCCH đúng mốc ERP. Chia 2 lát (user chốt "làm A trước xong làm B luôn"):
  - **Lát A (non-direct, qua kho):** (a) `buildDetailsByType` thêm `case NHAP_DIEU_CHUYEN_KHO_CHI_NHANH` vào nhóm `buildDetailsFromSource` (:1170) — `buildDetailsFromSource` KHÔNG cần sửa (type 7 ∉ KHAC → rơi `else` lấy `$reqProduct->supplier_price`, đã ×hệ số CN từ Phase A); (b) `resolveAccountingService` thêm type 7 vào nhóm `OtherProductImportAccountingService` (:1429) — **KHÔNG tạo service rỗng mới**: ERP `getDataCreateDept()` KHÔNG có case 6 lẫn 7, cả hai rơi `else` cuối = chỉ bút toán bốc xếp thuê ngoài (phiếu HRM lập tay không có tab đó → no-op/empty-success, y hệt type 6); (c) `editableTypes` thêm type 7 (:290, cho sửa nháp — parity type 6); (d) PYCCH chuẩn ERP: **THÊM →8** ở `WarehouseImportRequestService::createFromImportRequest` (:196, = ERP `ProductImportRequest::approve()`), **GỠ →9 lệch** ở `WarehouseImportWriteService::approveRequest` (:792-794, ERP KHÔNG đụng PYCCH lúc duyệt ĐNNK — **hàm dùng chung, đã flag user**), **THÊM →11** trong entity `ProductImport::updateWarehouse()` type-7 branch (= ERP :1795-1800); (e) `closeSourceImportRequest` dùng lại nguyên (YCNH→5 + imported_qty), `handleCompleted` KHÔNG đổi, `completeInternalTransfer` giữ type-6-only. accounting_stocks đã type-agnostic ở entity :618-681.
  - **Lát B (nhập thẳng):** trong entity `ProductImport::updateWarehouse()` type-7 branch, nếu `is_import_direct` → duyệt `$this->products` gọi `productImportDirectDetail($p, $employeeId, self::ERP_IMPORT_DETAIL_TYPE)` với `$employeeId` = `created_by` của PYCCH đầu tiên (= ERP :1801-1805); bỏ ĐNNK/PNK (nhập thẳng không lập); accounting_stocks vẫn ghi (block type-agnostic chạy mọi đường).
  - **PPBHĐC (allocation→status 12) = Phase C, HOÃN.**
- **Phase C (PPBHĐC):** port `TransferProductAllocation`(+Detail)+controller+**màn mới** (cần brainstorm UI riêng theo `erp-to-hrm-screen`) + `canCreateTransferProductAllocation`.
- **Phase D (vận chuyển + in):** DeliveryTrip type 7 (bút toán chi phí chuyến giao 33481/6427/3311 + object_pay); in cột %VAT PXK; biên bản.
- **Phase E (FE rà):** ĐNXK/PXH type 7 FE (chưa grep sâu); verify end-to-end.

## 7. Ràng buộc
LOCAL trên `develop`; không đụng WIP đồng đội (ProductExportController/CustomerManagerService api; product-exports/create.vue client); không sửa ERP; quyền mới (nếu cần) ở `PermissionsTableSeeder` guard `api`; số định dạng quốc tế; nhãn "Người tạo/Ngày tạo"; FE dùng `V2Base*`. PHP 7.4.

## 8. Bẫy port (từ survey — ghi để khỏi tái phạm)
1. **Nhập thẳng** rẽ nhánh lớn: bỏ PPBHĐC + bỏ duyệt YCNH; trừ `ProductImportDirectDetail` theo người lập PYCCH ở cả 2 đầu (company_id khác nhau).
2. PXK không có SL thực xuất → return sớm, KHÔNG sinh YCNH nhưng YCXH vẫn status 5, PYCCH đã set 7 (bám 1:1, đây là hành vi ERP).
3. `company_id` YCXH = cty NGUỒN (không phải cty người tạo); prepick nguồn lọc theo company_id này, prepick đích dùng `product_import->company_id`. Dễ nhầm công ty.
4. Prepick theo `created_by` của PYCCH + bỏ lọc customer; phải đồng bộ pending-prepick (Product/ProductTemplate bên ERP — kiểm HRM tương đương).
5. Hệ số chi nhánh × supplier_price nhưng `canUpdateUnitCostPriceFromSupplierPrice` luôn false → giá vốn KHÔNG đổi; VAT lấy vat_percent hiện tại.
6. YCNH tạo bởi người cty NGUỒN nhưng thông báo/duyệt thuộc người lập YCXH ở ĐÍCH; boot created lấy company theo `employee_create` của YCXH.
7. Notification ERP dùng Redis publish — HRM thay bằng cơ chế tương đương (hoãn chung một pass, nhất quán type 6 F2).
