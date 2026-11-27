# ERP — Bản đồ re-point quyền gộp "Kế toán kho" → 36 mã-cờ

> Nguồn: quét tĩnh `grep "accounting.ke_toan_kho.manage" app resources/views routes` = **154 chỗ**
> (81 Model · 27 Controller · 26 view · 19 route · 1 `Employee.php`). Đối chiếu design §5 (GATE MAP) + §6 (CROSS-CUTTING).
> Mã đích đầy đủ = `accounting.ke_toan_kho_<slug>.<kind>` (5 báo cáo đầu `.view`, 31 còn lại `.manage`).
> Cột "dạng": gate = `->can()`/`checkPermission:` · notify = `sendNotifyWith*Permission` · filter = `getForFilterByCurrentUser`/`getAccoungtingWarehouses` · menu = blade điều kiện hiện mục · dashboard = đếm trên HomeController.
> OR-set = cổng-gộp: giữ OR của TẤT CẢ mã thành viên (design §6).

## Nhóm I — Báo cáo kho (5 mã `.view`) — Task 2

| file:line | dạng | mã đích | §5 | ghi chú |
|---|---|---|---|---|
| routes/web.php:1574-1575 | route gate | #1 `the_kho.view` | I | Thẻ kho |
| routes/web.php:1576-1579 | route gate | #2 `bc_ban_hang.view` | I | BC bán hàng |
| routes/web.php:1580-1581 | route gate | #3 `bc_nhap_mua.view` | I | BC nhập mua |
| routes/web.php:1582-1583,1590,1594 | route gate | #4 `bc_kho.view` | I | BC kho (3 route trong nhóm) |
| routes/web.php:1599 | route gate | #5 `bc_ton_lau.view` | I | BC tồn lâu |

⚠️ Nhóm warehouse-reports CHỈ một số route gắn gate — rà từng dòng khi re-point, đừng bọc cả group.

## Nhóm II — Nhập hàng (Task 3)

| file:line | dạng | mã đích | §5 | ghi chú |
|---|---|---|---|---|
| app/Model/Warehouse/ProductImportRequest.php:1276,1479,1484,1506,1519 | gate | #7 `yc_nhap_hang` | II | YC nhập hàng |
| app/Http/Controllers/Warehouse/WarehouseImportRequestsController.php:235 | gate | #7 | II | |
| routes/web.php:1403 | route (forAccounting) | #7 | II | ProductImportRequest forAccounting |
| resources/views/warehouse/product_import_requests/forAccounting.blade.php:74 | filter | #7 | II/§6 | `getForFilterByCurrentUser('accounting.ke_toan_kho.manage')` → đổi sang mã #7 |
| app/Model/Warehouse/ProductImport.php:844,855 | gate | #8 `phieu_nhap_mua` | II | Phiếu nhập mua |
| app/Model/Warehouse/WarehouseImport.php:1369,1402,1419 | gate | #9 `phieu_nhap_kho` | II | Phiếu nhập kho |
| routes/web.php:1459 | route (forAccounting) | #9 | II | WarehouseImport forAccounting |
| app/Model/Warehouse/OrderImportRequest.php:698 | gate (OR) | #10 `yc_nhap_theo_don` **OR** `ke_toan_mua_hang` | II | giữ nhánh OR ke_toan_mua_hang (§6) |
| app/Model/Warehouse/CustomDeclaration.php:544 | gate (OR) | #11 `to_khai_hai_quan` **OR** `ke_toan_mua_hang` | II | giữ nhánh OR ke_toan_mua_hang (§6) |

## Nhóm III — Xuất hàng (Task 4)

| file:line | dạng | mã đích | §5 | ghi chú |
|---|---|---|---|---|
| app/Model/Warehouse/ProductExportRequest.php:2294,2419,2642,2652,2669,2672,2679,2682,2750,2766,2771 | gate | #12 `de_nghi_xuat_kho` | III | ĐN xuất kho (11 chỗ) |
| app/Model/Warehouse/ProductExport.php:1214 | gate | #13 `phieu_xuat` | III | Phiếu xuất |
| app/Model/Warehouse/WarehouseExport.php:1091,1103,1111,1135 | gate | #14 `phieu_xuat_kho` | III | (1102 là COMMENT name-gate, bỏ qua) |
| app/Http/Controllers/Warehouse/WarehouseExportRequestsController.php:311 | gate | #14 | III | |
| app/Model/Warehouse/SplitExportRequest.php:319,327,360 | gate | #15 `yc_tach_xuat` | III | YC tách xuất |
| app/Model/Warehouse/JoinExportRequest.php:347,382 | gate | #16 `yc_gop_xuat` | III | YC gộp xuất (355 là COMMENT, bỏ qua) |

## Nhóm IV — Chuyển hàng / phân bổ (Task 5)

| file:line | dạng | mã đích | §5 | ghi chú |
|---|---|---|---|---|
| app/Model/Warehouse/ProductTransferRequest.php:220,222,334,366 | gate | #17 `yc_chuyen_hang` | IV | YC chuyển hàng |
| app/Http/Controllers/Warehouse/ProductTransfersController.php:117 | gate | #17 | IV | |
| app/Http/Controllers/Warehouse/ProductTransferRequestsController.php:223,326 | notify | #17 | IV/§6 | người nhận thông báo theo chứng từ |
| app/Model/Warehouse/ProductImportDirectTransfer.php:112,170,175 | gate | #18 `dieu_chuyen_nhap_thang` | IV | ĐC nhập thẳng |
| app/Http/Controllers/Warehouse/ProductImportDirectTransferController.php:162,233 | notify | #18 | IV/§6 | |
| app/Model/Order/ProductAllocation.php:118,148 | gate | #19 `phan_bo_hang` | IV | Phân bổ hàng |
| app/Model/Order/InlandProductAllocation.php:136 | gate | #20 `phan_bo_noi_dia` | IV | Phân bổ nội địa |
| app/Model/Warehouse/TransferProductAllocation.php:111 | gate | #21 `phan_bo_dieu_chuyen` | IV | Phân bổ điều chuyển |

## Nhóm V — Kiểm kê (Task 6)

| file:line | dạng | mã đích | §5 | ghi chú |
|---|---|---|---|---|
| app/Model/Warehouse/Inventory/InventoryAuditReport.php:432 | gate | #22 `bien_ban_kiem_ke` | V | Biên bản kiểm kê |
| app/Http/Controllers/Warehouse/InventoryAuditReportsController.php:37 | gate | #22 | V | |
| **app/Http/Controllers/Warehouse/AccountingInventoriesController.php:200** | gate (view-flag) | #22 `bien_ban_kiem_ke` | V/§5-gap | ⚠️ RULING — xem mục Rulings |
| app/Model/Warehouse/Inventory/WarehouseInventoryImport.php:92,265 | gate | #23 `nhap_dieu_chinh_kiem_ke` | V | Nhập ĐC kiểm kê |
| app/Http/Controllers/Warehouse/WarehouseInventoryImportsController.php:190,260 | notify | #23 | V/§6 | |
| app/Model/Warehouse/Inventory/WarehouseInventoryExport.php:89,264 | gate | #24 `xuat_dieu_chinh_kiem_ke` | V | Xuất ĐC kiểm kê |
| app/Http/Controllers/Warehouse/WarehouseInventoryExportsController.php:199,275 | notify | #24 | V/§6 | |
| app/Http/Controllers/Warehouse/SelfInventoriesController.php:417 | notify | #25 `tu_kiem_ke` | V/§6 | Tự kiểm kê |

## Nhóm VI — Hàng mượn (Task 7)

| file:line | dạng | mã đích | §5 | ghi chú |
|---|---|---|---|---|
| app/Model/Warehouse/BorrowSellRequest.php:655,781,795 | gate | #26 `yc_ban_hang_muon` | VI | YC bán hàng mượn |
| app/Http/Controllers/Warehouse/BorrowSellRequestsController.php:438 | notify | #26 | VI/§6 | |
| app/Model/Warehouse/BorrowSell.php:407 | gate | #27 `ban_hang_muon` | VI | Bán hàng mượn |
| routes/web.php:1161 | route group | #27 | VI | nhóm borrow-sell |
| app/Model/Warehouse/BorrowExportRequest.php:247,319,326 | gate | #28 `yc_xuat_hang_muon` | VI | (275 là COMMENT, bỏ qua) |
| app/Http/Controllers/Warehouse/BorrowExportRequestController.php:291 | notify | #28 | VI/§6 | |
| app/Model/Warehouse/BorrowExport.php:185 | gate | #29 `xuat_hang_muon` | VI | Xuất hàng mượn |
| routes/web.php:1189 | route group | #29 | VI | nhóm borrow-export |
| app/Model/Warehouse/BorrowExtendRequest.php:89,92,93,176,190,243 | gate | #30 `yc_gia_han_hang_muon` | VI | YC gia hạn |
| routes/web.php:1992 | route (forAccounting prepickExtendRequest) | #30 | VI | |
| app/Http/Controllers/HomeController.php:1006,1020 | dashboard | #30 (giữ OR với duyệt finance.hang_muon) | VI/§6 | 2 đếm gia hạn |

## Nhóm VII — Thanh toán giao hàng (Task 8)

| file:line | dạng | mã đích | §5 | ghi chú |
|---|---|---|---|---|
| app/Model/Warehouse/DeliveryPaymentRequest.php:433,480,486,537 | gate | #31 `yc_thanh_toan_giao_hang` | VII | YC TT giao hàng |
| app/Model/Warehouse/EmployeeDeliveryPayment.php:97,137,143,225 | gate | #32 `thanh_toan_giao_hang_nv` | VII | TT giao hàng NV |
| app/Model/Common/OtherDeliveryPaymentRequest.php:253,297,303,353 | gate | #33 `yc_thanh_toan_giao_hang_khac` | VII | YC TT giao hàng khác |

## Nhóm VIII — Giao việc / dịch vụ kế toán (Task 9)

| file:line | dạng | mã đích | §5 | ghi chú |
|---|---|---|---|---|
| app/Model/Customers/WrAssignTask.php:405,438,523,540 | gate | #34 `ket_qua_giao_viec` | VIII | KQ giao việc |
| app/Http/Controllers/Customercare/WrApproveResultsController.php:396,1162 | notify | #34 | VIII/§6 | |
| app/Http/Controllers/HomeController.php:1380 | dashboard | #34 | VIII/§6 | đếm KQ giao việc |
| app/Model/Customers/WrAccountingServiceRequest.php:145,189 | gate | #35 `yc_lam_dich_vu_ke_toan` | VIII | YC làm DV kế toán |
| app/Http/Controllers/Customercare/WrAccountingServiceRequestsController.php:155,203 | notify | #35 | VIII/§6 | |

## Nhóm IX — Hạch toán bổ sung (Task 10)

| file:line | dạng | mã đích | §5 | ghi chú |
|---|---|---|---|---|
| app/Http/Controllers/IncomeExpenditure/AdditionAccountingRequestController.php:244,332 | notify | #36 `yc_hach_toan_bo_sung` | IX | YC hạch toán bổ sung |

## Nhóm §6 — Cross-cutting (Task 11)

### Beginning stock (tồn đầu kỳ)
| file:line | dạng | mã đích | ghi chú |
|---|---|---|---|
| routes/web.php:1687 | route gate (group beginning_accounting_stocks) | #6 `ton_dau_ky` | rà từng route trong group |

### Dashboard HomeController (đếm)
| file:line | dạng | mã đích | ghi chú |
|---|---|---|---|
| HomeController.php:1030 | dashboard gate-gộp | **OR(#17,#23,#24)** bọc ngoài; mỗi đếm theo mã riêng | 3 đếm: YC chuyển hàng(#17) · nhập ĐC kiểm kê(#23) · xuất ĐC kiểm kê(#24) |
| HomeController.php:2201 | dashboard | #18 `dieu_chuyen_nhap_thang` | đếm phiếu ĐC nhập thẳng cần duyệt (status=2) |
| HomeController.php:1006,1020 | dashboard | #30 (giữ OR) | (đã liệt kê Nhóm VI) |
| HomeController.php:1380 | dashboard | #34 | (đã liệt kê Nhóm VIII) |

### Menu (blade điều kiện hiện mục) — re-point từng mục theo màn nó mở
| file:line | mã đích | ghi chú |
|---|---|---|
| topmenubar.blade.php:1043,2246,2252,2257,2262,2266,2272,2275,2284,2288,2309,2313,2329,2334 | theo màn từng mục | 14 chỗ; vài chỗ OR-chain với thu_kho / xuat_hang_vuot_han_muc / is_warehouse_accountant / duyệt hàng mượn → chỉ ĐỔI operand `ke_toan_kho`, GIỮ các operand OR khác (§6) |
| topmenubar_old.blade.php:1147,1311,1357,1801,1827,1873,3051,3070,3084,3103,3227 | theo màn từng mục | 11 chỗ; 1147/1357 OR is_warehouse_accountant |

### Helper gom kho kế toán
| file:line | dạng | mã đích | ghi chú |
|---|---|---|---|
| app/Employee.php:2906 `getAccoungtingWarehouses($companyId)` | filter helper | **RULING** — xem mục Rulings | 1 caller: PrepickTransfer2.php:263 (notify) |

## GIỮ NGUYÊN (không re-point) — lưới chặn hồi quy

| chỗ | lý do |
|---|---|
| app/Console/Commands/BorrowWarning.php:108 `Redis::publish("ke_toan_kho".$w,…)` | kênh Redis coarse GIỮ (design §6); `test_redis_channel_ke_toan_kho_giu_nguyen` canh |
| app/Console/Commands/PrepickWarning.php:113 (idem) | như trên |
| `Employee::isWarehouseAccountant()` (Employee.php:282) | cờ `is_warehouse_accountant` query bảng WarehouseAccountant — KHÔNG đổi (§6) |
| 4 comment name-gate: HomeController.php:1105 · BorrowExportRequestController.php:275 · JoinExportRequest.php:355 · WarehouseExport.php:1102 | chú thích `//`, không phải cổng sống → `test_khong_con_cong_kiem_theo_ten` đã bỏ qua |
| blade `getForFilterByCurrentUser('finance.*'/'warehouse.*')` | ĐÃ dùng mã MỚI (không phải ke_toan_kho) — KHÔNG trong phạm vi |

## RULINGS (ghi trong ledger + nêu ở báo cáo cuối)

1. **AccountingInventoriesController.php:200 → #22 `bien_ban_kiem_ke`.** `AccountingInventory` là màn kiểm kê-kế-toán ĐỘC LẬP còn sống (route group `accounting_inventories` web.php:1699-1711 + menu riêng), TÁCH khỏi `InventoryAuditReport` (#22) nhưng cùng họ Nhóm V kiểm kê. Màn này KHÔNG được liệt trong design §5 → là lỗ hổng §5 do quét tĩnh bắt được. Chỉ có 1 cổng ke_toan_kho = `show():200` (cờ xem của kế toán, `$permission='accounting'`). Quyết: map về #22 (cùng họ kiểm kê). **Cost nếu sai:** kế toán được cấp #23/#24/#25 nhưng KHÔNG #22 sẽ mất quyền xem `accounting_inventories/show`; giảm thiểu vì lệnh cấp-lại tự cho đủ 36 mã cho holder hiện tại.
2. **getAccoungtingWarehouses (Employee.php:2906) → OR tất cả 36 mã.** Helper gom "mọi kho mà người này làm kế toán", generic, 1 caller PrepickTransfer2.php:263 (chọn người nhận thông báo điều chuyển). Vì không gắn 1 màn cụ thể, giữ ngữ nghĩa "bất kỳ kế toán kho nào" = người có BẤT KỲ mã nào trong 36 → OR 36 mã. **Cost nếu sai:** nếu caller thực ra chỉ cần 1 màn, OR 36 sẽ rộng hơn cần thiết (gửi thông báo cho nhiều người hơn) — vô hại nghiệp vụ, chốt lại ở Task 11 sau khi đọc ngữ cảnh PrepickTransfer2.
3. **test_khong_con_cong_kiem_theo_ten GREEN từ đầu (lệch plan "cả 2 FAIL").** ĐÃ kiểm tới gốc: 4 chỗ 'Kế toán kho' trong ngữ cảnh cổng đều là COMMENT `//`; ERP thuần code-based (không name-gate sống, khớp §7.1). Test giữ nguyên làm lưới chặn hồi quy. **Cost nếu sai:** không có — test vẫn chặn nếu ai thêm name-gate mới.
