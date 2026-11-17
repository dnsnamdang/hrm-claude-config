# Phủ hết màn duyệt — nhóm Tài chính / Kho (tổng hợp đợt 2) — @cuong61n

17/11/2026, nhánh `gop_db-main`, DB local `local_hrm_erp`. Chi tiết từng tiểu nhóm: `phu-het-tai-chinh-a.md` (kho nhập), `-b.md` (kho xuất / YCXH), `-c.md` (xuất mượn / tách-ghép / vận chuyển), `-d.md` (hạch toán dịch vụ / phiếu báo có / quyết toán quý), `-e.md` (kế hoạch NV / phân chia thị trường / rà đợt 1), `-dieu-chuyen-kho.md`.
Kết quả chạy: `vendor/bin/phpunit tests/Feature/ApprovalCenter/Finance` = **170 test, 14.717 assertion, xanh**. Dữ liệu thử đã dọn bằng `clean-test` (manifest `wave2-finance*.json`).

## 1. Bảng kiểm kê (mọi luồng Duyệt / Từ chối / Tiếp nhận của Finance + Assign-kho)

### Đăng ký MỚI đợt 2 (17 loại)
| doc_type | Màn | Cấp / gate tóm tắt | Chờ thật local | Verify (cặp / duyệt thật / chênh) | Đột biến |
|---|---|---|---|---|---|
| `warehouse_transfer` Điều chuyển kho | /finance/warehouse-transfers | 1 cấp: kế toán kho kho NGUỒN (bảng `warehouse_accountants`, RỖNG) + trong phạm vi xem 4 mức | 0 | 18.120 / – / 0 (+ test 1.380/8) | 7/7 |
| `warehouse_import_request` Đề nghị nhập kho (F6) | /warehouse/import-requests | thủ kho của kho (không mã, không công ty) | 30 | 33.480 / 2.370 / 0 | 6/6 |
| `warehouse_import` Phiếu nhập kho (F7) | /finance/warehouse-imports | mã KT kho + công ty gốc; loại 5 `approvable=false` | 32 | 8.550 / 1.499 / 0 | 5/6 (1 tương đương) |
| `product_import_direct_transfer` (F10) | /finance/product-import-direct-transfers | mã KT kho + công ty gốc | 1 | 1.575 / 326 / 0 | 4/4 |
| `exc_shortage_warehouse_import` Phiếu báo thừa/thiếu | /warehouse/exc-shortage-imports | mã duyệt + (người lập / công ty gốc / xem ≥ tổng công ty) | 3 | 1.953 / 411 / 0 | 6/6 |
| `warehouse_inventory_import` Phiếu nhập kho điều chỉnh kiểm kê | /warehouse/inventory-imports | mã KT kho, không công ty — **chờ user xác nhận giữ** | 0 | 1.350 / 450 / 0 | 4/4 |
| `product_export_request` YCXH (F25) | /finance/product-export-requests | 3 cấp: TP(st10) → BGĐ(st11) → KT kho(st2); loại 3 (mượn) ở st10/11 `approvable=false` | 23 | 14.529 / 1.194 / 0 | 14/14 |
| `warehouse_export` Phiếu xuất kho | /finance/warehouse-exports | mã KT kho + công ty gốc (cờ FE) | 114 | 57.000 / 5.250 / 0 | 6/6 |
| `warehouse_export_request` Đề nghị xuất kho | /finance/warehouse-export-requests | thủ kho + mã KT kho (loại 5 chỉ thủ kho) | 119 | 59.375 / 130 / 0 (+ 73.750/225) | 6/6 |
| `product_transfer_request` Yêu cầu chuyển hàng (F1) | /finance/product-transfer-requests | mã KT kho + công ty gốc | 24 | 14.250 / 562 / 0 | 6/6 |
| `borrow_export_request` Yêu cầu xuất mượn (F19) | /finance/borrow-export-requests | mã KT kho, không kiểm công ty | 1 | 3.325 / 525 / 0 | 8/8 |
| `split_export_request` / `join_export_request` | /finance/split-export-requests, join-export-requests | mã KT kho + công ty gốc | 0 / 2 | 2.850/272/0 · 3.800/350/0 | 8/8 |
| `delivery_request` Yêu cầu vận chuyển (F18) | /finance/delivery-requests | thủ kho của kho YCXH nguồn (mọi công ty) | 0 (bảng rỗng) | 3.540 / 260 / 0 | 8/8 |
| `buy_service_accounting_request` (F21) | /finance/buy-service-accounting-requests | mã hạch toán mua dịch vụ + công ty gốc | 2 | 4.320 / 456 / 0 | 7/8 |
| `wr_accounting_service_request` HDDV | /finance/wr-accounting-service-requests | mã + công ty gốc | 6 | 4.840 / 290 / 0 | 7/7 |
| `service_accounting_request` HĐBH | /finance/service-accounting-requests | mã, không công ty | 17 | 7.998 / 1.798 / 0 | 8/8 |

### SỬA đợt 1 (tăng version / thêm watch)
- `bill_payment_request` **v2**: thêm cấp 5 "Chờ tạo phiếu chi" (st6) vì chi tiết có nút Từ chối + Tạo phiếu chi/UNC (`finance.ke_toan_thanh_toan.manage`, công ty gốc) — chờ thật 40 → 133 (93 phiếu st6 phần lớn là phiếu cũ từ ERP). Verify 75.558 cặp / 2.146 / 0; đột biến 3/3. Thêm `scheduleSync` ở 4 chỗ ghi query builder (BillPaymentWriteService, BillPaymentApprovalFlowService ×2, BillPaymentAuthorizationWriteService).
- 8 loại thiếu `watchedTables` `company_employees` (người duyệt tính bằng `holders()` JOIN `company_employees`): `bill_income`, `bill_income_request`, `bonus_end_year_settlement`, `inventory_audit_report`, `position_inventory_result`, `prepick_cancel_request`, `product_import_request`, `self_inventory`.
- Xác nhận ĐỦ, không sửa: F11 `prepick_cancel_request`, F16 `borrow_sell_request` (st10/11/2), F22 `bill_income_request`, và 9 loại còn lại.

### Đã đăng ký bởi nhóm khác (đối chiếu, không làm lại)
`product_price_approval` (MasterData), `business_target_*`, `division_market_employee`, `division_market_department`, `sale_plan_employee`, `market_plan_employee` (Bán hàng — khớp code), `delivery_contract` / `delivery_cost_summary` / `other_delivery_trip` (Transport).

### BỎ — kèm bằng chứng
| Luồng | Lý do (file:dòng) |
|---|---|
| Phiếu báo có `bill_income_reports` (F3) | Chỉ Đang tạo → Đã duyệt, không trạng thái chờ; nháp chỉ người lập thấy (`BillIncomeReportService.php:73-76`, `BillIncomeReportAccess.php:30`); local 3.825/3.825 đã duyệt |
| Quyết toán thưởng năng suất QUÝ | `FORM_STATUSES=[1,3]` (`BillProductivitySettlementQuarter.php:39`), middleware chỉ cho người tạo duyệt (`CheckBillProductivitySettlementQuarterEditable.php:25`), duyệt đặt thẳng 1→3 (`...WriteService.php:96`) |
| Hàng đợi "chờ báo thừa thiếu" | chỉ hành động tạo (`ExcShortageService:46-70`, `import-discrepancies/index.vue:303`) |
| Phiếu nhập hàng (`product_imports`) | 2 trạng thái, không bước chờ (`ProductImport.php:58-71`) |
| Phiếu nhập hàng điều chỉnh kiểm kê | người lập tự "Lưu và duyệt" (`InventoryImport.php:14-29`) |
| Phiếu nhập lại / xuất lại / xuất điều chỉnh / PXH | không route duyệt/từ chối (`Assign/Routes/api.php:850-899`, `Finance/Routes/api.php:709-718,960-1000`) |
| ĐNXK `cancel` | chỉ nháp + người lập (`WarehouseExportRequestController.php:764`) |
| YCXH st14 | chỉ trạng thái theo dõi (`ProductExportService:1247`) |
| Kiểm kê vị trí `complete`, kiểm kê hàng hoá st4/5 | hàng đợi công việc (`canHandle`: `PositionInventoryResult.php:240`, `SelfInventory.php:240`), không Duyệt/Từ chối |
| Ủy nhiệm chi, kết chuyển, phiếu hạch toán, `accounting-prepick-cancels`, `borrow_exports`, `borrow_sells` | không bước duyệt / không trạng thái chờ riêng |

## 2. Việc tôi đã tự xử lý ở khâu điều phối
- `DeliveryRequestDefinition::watchedTables` bỏ `product_export_requests` (agent C thêm để bắt đổi kho; agent B phát hiện nó làm `ProductExportRequest::create()` NGOÀI giao dịch trả `id = 0` vì `ApprovalInboxRefresher` chạy truy vấn giữa INSERT và `lastInsertId()`). Test delivery vẫn xanh. **Nên điều phối xem lại `ApprovalInboxRefresher`** (file dùng chung): mọi bảng trong `watchedTables` có INSERT ngoài giao dịch đều dính; hiện còn `employee_infos`, `company_employees`… nên theo dõi.
- Dữ liệu thử còn lại trong bảng gom: 84 dòng `TEST.%` state 1 của 12 loại đợt 1 (mỗi loại 4) + 12 dòng state 5 (task_*_approval) — KHÔNG phải của đợt này (seed 16/11), để nguyên cho e2e.

## 3. "BE không chốt quyền" / lỗi code gốc cần chuyển người phụ trách
1. **Điều chuyển kho: gate đọc `warehouse_accountants` RỖNG ⇒ không ai duyệt được** (bảng sống `accounting_warehouse_accountants`); đọc cùng bảng chết còn ở `WarehouseImportWriteService:1343`, `ProductImportRequestService:796,1978`.
2. ĐNXK: FE hiện nút "Lập phiếu xuất kho" cho mọi thủ kho nhưng POST đòi thêm mã KT kho (52/60 thủ kho thiếu mã ⇒ 403).
3. PXK / ĐNXK: API chi tiết lọc theo quyền xem theo cấp ⇒ người duyệt thiếu quyền xem mở từ Trung tâm phê duyệt gặp 404. HĐBH `canView()` không tính `canAccounting()` ⇒ 211 cặp người duyệt bị 403.
4. YCXH loại 3 (mượn) st10/11: HRM không có người duyệt (1 phiếu local) — chỉ ERP.
5. Nhiều luồng không kiểm công ty phiếu (xem `dinh-nghia-tai-chinh.md` mục 5); route từ chối ĐNNK không chặn loại 11 ở BE; HĐBH nút hạch toán cần thêm mã `customer_care.hach_toan_dich_vu_hdbh.manage`; `bill-income-reports/approve` không đòi người lập; `ServiceAccountingRequest.contractable_type` NULL ở 12 dòng; docblock còn "Super Admin" (`PrepickExtendRequest.php:234`, `PrepickTransferRequest.php:265`, `ProductPrepickRequest.php:381`, `DeliveryRequest`).
6. Đề nghị thanh toán: danh sách loại st6 khỏi `is_can_approve`, chi tiết vẫn có nút Từ chối — hai màn lệch nhau. `PhysicalWarehouseService:201` xoá/ghi `warehouse_accountants`.

## 4. Điểm cần user quyết
1. Điều chuyển kho: đổi gate sang `accounting_warehouse_accountants` hay nạp `warehouse_accountants`? (đến khi đó phiếu vào hộp nhưng chưa ai thấy).
2. Đề nghị thanh toán st6: +93 phiếu cũ vào Phiếu chờ duyệt — có giới hạn theo ngày không?
3. Phân chia thị trường theo phòng ban: bản nháp "Đang tạo" cũng vào hàng chờ (BE không có bước gửi duyệt) — giữ?
4. `warehouse_inventory_import` (chỉ có nút "Tạo phiếu nhập hàng" của KT kho) — giữ không? PXK st7 "Đang hạch toán" còn nút Từ chối — có coi là chờ duyệt?
5. `sourceSubsystem`: các loại Kho đang đặt `warehouse`, hạch toán mua dịch vụ `sale`, còn lại `finance` — gom lại?
6. Hàng đợi "Chờ xử lý" kiểm kê có đưa vào không (hiện: không — việc công).
7. Xuất mượn: nút không kiểm công ty trong khi tab `for-approve` có — theo nút. Vận chuyển: thủ kho liệt kê ở mọi công ty.
