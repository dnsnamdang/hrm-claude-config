# Tách quyền "Kế toán kho" thành 36 quyền theo từng màn/phiếu — Design

> Phạm vi: **ERP + HRM** (quyền dùng chung qua Catalog). Tài liệu này là design chốt để lập plan.
> Ngày: 2026-11-26.

## 1. Ý định & lý do (why)

Hiện có **một** quyền `accounting.ke_toan_kho.manage` (nhãn "Kế toán kho") gác **~252 chỗ ở ERP + ~105 chỗ ở HRM**: vừa là gate vào màn, vừa là vai "người kế toán kho duyệt/hạch toán" trên rất nhiều loại phiếu, vừa là đích gửi thông báo/realtime/dashboard.

**Vấn đề người dùng gặp:** khi phân quyền, cái tên "Kế toán kho" quá chung chung — admin không biết tích nó thì người đó làm được *màn/phiếu nào*, và muốn cho đúng **một** màn/phiếu thì không có quyền nào đủ hẹp. Hệ quả: hoặc cấp thừa (all-or-nothing), hoặc không dám cấp.

**Mục tiêu:** tách thành nhiều quyền tên rõ, **mỗi loại phiếu / mỗi màn = 1 quyền riêng**, để cấp đúng từng chỗ. Người dùng đã chốt phương án tách **mịn nhất** (phương án a) = **36 quyền**.

## 2. Goals / Non-goals / Anti-goals

**Goals**
- 36 quyền mới, mỗi quyền gác đúng 1 màn/phiếu, tên tiếng Việt rõ ("Kế toán kho — <phiếu/màn>").
- Mỗi quyền mới là quyền **dùng chung `['erp','hrm']`** (cùng nghiệp vụ ở 2 app).
- **Không ai mất quyền sau khi tách**: mọi vai trò/nhân viên đang có "Kế toán kho" được cấp tự động **cả 36 quyền** (giữ nguyên hiện trạng). Admin thu hẹp sau tuỳ ý.
- Mọi gate/thông báo/dashboard/menu hiện trỏ về quyền cũ phải trỏ lại đúng quyền mới tương ứng.

**Non-goals**
- Không đổi *nghiệp vụ* (ai duyệt được gì về mặt luồng vẫn như cũ, chỉ đổi "khoá" kiểm).
- Không port thêm màn HRM mới (chỉ sửa chỗ đang dùng quyền).
- Không đụng cờ `is_warehouse_accountant` (độc lập, xem §6).

**Anti-goals (coi là thất bại dù code chạy)**
- Sau deploy, một người đang làm kế toán kho bị chặn ở bất kỳ phiếu nào họ vốn làm được.
- Sót một chỗ gate khiến quyền cũ vẫn còn tác dụng ở phiếu đã tách (khoá "ma").
- Quét sót chỗ tham chiếu quyền **bằng tên** chứ không bằng code (xem rủi ro §7).

## 3. Constraints

- Catalog là nguồn sự thật duy nhất: `hrm-api/app/Support/Permissions/Catalog/accounting.php`. Mỗi code khai 1 lần, có `platforms`, `legacy`.
- Đồng bộ Catalog→DB qua `php artisan permission:catalog-sync` (dùng `CatalogSync`): thêm/sửa/`deprecated_at`, **không xoá cứng**; alias ở bảng `permission_aliases`.
- DB **dùng chung** ERP+HRM (đã gộp). Spatie: pivot `role_has_permissions`, `employee_has_permissions` (model_has_permissions), `employee_has_roles`.
- Prod chạy `permission:catalog-sync` qua `~/build_tpe.sh` trên VPS HRM.
- ERP = Laravel 6 (`develop_02`), check bằng `->can('<code>')` / middleware `checkPermission:<code>` / `Employee::withPermission` / `NotificationHelper::sendNotifyWithPermission`. HRM = Laravel 8, check `isCurrentEmployeeHasPermission/hasAPermission('<code>')` + Approval Center Definitions + `permissionApprovers('warehouse_accountant', …)`.
- Không Super Admin bypass ở HRM (ERP có Gate::before).

## 4. Approaches đã cân nhắc

- **(1) Tách mịn theo từng màn/phiếu — 36 quyền. ✅ CHỌN.** Rõ nhất, cấp đúng từng chỗ. Giá: sửa ~252+105 chỗ 2 app + migration cấp lại quyền prod. *Người dùng chốt phương án này (a).*
- **(2) Gộp theo nhóm — ~9 quyền.** Gọn, code nhẹ hơn. Loại: chưa đạt "đúng từng màn" người dùng cần.
- **(3) Chỉ tách vài màn đang vướng.** Rẻ nhất. Loại: người dùng muốn tách toàn bộ.
- **(4) Giữ 1 quyền, chỉ làm rõ tên + hiển thị màn nào ở trang phân quyền.** ~0 rủi ro. Loại: vẫn all-or-nothing, không cấp lẻ được.

## 5. Danh sách 36 quyền & bản đồ gate (how — phần quyết định)

**Quy ước code (call của mình, có thể chỉnh):** `accounting.ke_toan_kho_<slug>.<kind>`, nhãn `"Kế toán kho — <tên>"`, `subsystem_group='Kinh doanh - Tài chính'`, `subsystem='Kế toán'`. Màn báo cáo dùng `kind=view`, phiếu/hành động dùng `kind=manage`. `platforms=['erp','hrm']` toàn bộ.

### Nhóm I — Màn báo cáo/tra cứu (hiện chỉ ERP gate route)
| # | Code (`accounting.…`) | Nhãn | Gate ERP | Gate HRM |
|---|---|---|---|---|
| 1 | `ke_toan_kho_the_kho.view` | Thẻ kho kế toán | `web.php:1574-1575` | — (chưa port) |
| 2 | `ke_toan_kho_bc_ban_hang.view` | BC bán hàng (kế toán) | `web.php:1576-1579` | — |
| 3 | `ke_toan_kho_bc_nhap_mua.view` | BC nhập mua (kế toán) | `web.php:1580-1581` | — |
| 4 | `ke_toan_kho_bc_kho.view` | BC kho kế toán | `web.php:1582-1583,1590,1594` | — |
| 5 | `ke_toan_kho_bc_ton_lau.view` | BC hàng tồn lâu (in) | `web.php:1599` | — |
| 6 | `ke_toan_kho_ton_dau_ky.manage` | Tồn kho đầu kỳ kế toán | `web.php:1687` (group) | — |

> ⚠️ Group `warehouse_reports` **chỉ một số** route bị gate; route anh em (1584-1587, 1589, 1591-1593, 1595-1598) KHÔNG gate — tách phải rà **từng dòng**, không gán cả group.

### Nhóm II — Nhập kho
| # | Code | Nhãn | Gate ERP | Gate HRM |
|---|---|---|---|---|
| 7 | `ke_toan_kho_yc_nhap_hang.manage` | YC nhập hàng | `ProductImportRequest.php:1276,1479,1484,1506,1519`; `WarehouseImportRequestsController.php:235`; route `web.php:1403` | `ProductImportRequest.php:39,1021,1038,1096,1144,1192`; `ProductImportRequestDefinition.php:70,147,151` |
| 8 | `ke_toan_kho_phieu_nhap_mua.manage` | Phiếu nhập mua | `ProductImport.php:844,855` | `ProductImport.php:64,445,469`; `ProductImportService.php:1667,2207,2318` |
| 9 | `ke_toan_kho_phieu_nhap_kho.manage` | Phiếu nhập kho (+ YC nhập kho) | `WarehouseImport.php:1369,1402,1419`; route `web.php:1459` | `WarehouseImport.php:92,201,247,340`; `WarehouseImportDefinition.php:64,117`; `WarehouseImportRequest.php:35,158` |
| 10 | `ke_toan_kho_yc_nhap_theo_don.manage` | YC nhập theo đơn ⚠️OR | `OrderImportRequest.php:698` (**OR** `ke_toan_mua_hang`) | — |
| 11 | `ke_toan_kho_to_khai_hai_quan.manage` | Tờ khai hải quan ⚠️OR | `CustomDeclaration.php:544` (**OR** `ke_toan_mua_hang`) | — |

### Nhóm III — Xuất kho / xuất hàng
| # | Code | Nhãn | Gate ERP | Gate HRM |
|---|---|---|---|---|
| 12 | `ke_toan_kho_de_nghi_xuat_kho.manage` | ĐN/YC xuất hàng | `ProductExportRequest.php:2294,2419,2642,2652,2669,2672,2679,2682,2750,2766,2771` | `ProductExportRequestDefinition.php:41,81,210`; `ProductExportController.php:1049,1155,1713,1732`; FE `product-export-requests/index.vue:754,763`, `ProductExportRequestForm.vue:2850,2860` |
| 13 | `ke_toan_kho_phieu_xuat.manage` | Phiếu xuất | `ProductExport.php:1214` | FE `product-exports/index.vue:471` |
| 14 | `ke_toan_kho_phieu_xuat_kho.manage` | Phiếu xuất kho (+ YC xuất kho) | `WarehouseExport.php:1091,1103,1111,1135`; `WarehouseExportRequestsController.php:311` | `WarehouseExportDefinition.php:34,68,120`; `WarehouseExportRequestDefinition.php:34,68,83,155`; `WarehouseExportRequestController.php:594,751,766,910`; routes `Assign/api.php:839-847,886-889`; `WarehouseExportRequestResource.php:36` |
| 15 | `ke_toan_kho_yc_tach_xuat.manage` | YC tách xuất | `SplitExportRequest.php:319,327,360` | `SplitJoinExportRequestCommon.php:35,108`; `SplitExportRequestDefinition.php`; `SplitJoinExportApprovalSupport.php:58,107,135`; `SplitJoinExportRequestController.php:22,229`; route `Finance/api.php:2321-2329` |
| 16 | `ke_toan_kho_yc_gop_xuat.manage` | YC gộp xuất | `JoinExportRequest.php:347,382` | `JoinExportRequestDefinition.php` (cùng Common/Support như #15) |

### Nhóm IV — Điều chuyển & phân bổ
| # | Code | Nhãn | Gate ERP | Gate HRM |
|---|---|---|---|---|
| 17 | `ke_toan_kho_yc_chuyen_hang.manage` | YC chuyển hàng | `ProductTransferRequest.php:220,222,334,366`; `ProductTransfersController.php:117`; notify `ProductTransferRequestsController.php:223,326` | `ProductTransferRequest.php:31,225,263`; `ProductTransfer.php:61,213`; `ProductTransferRequestDefinition.php:64,108`; `ProductTransferRequestService.php:706` |
| 18 | `ke_toan_kho_dieu_chuyen_nhap_thang.manage` | Điều chuyển nhập thẳng | `ProductImportDirectTransfer.php:112,170,175`; notify `…Controller.php:162,233` | `ProductImportDirectTransfer.php:47,168,209,250`; `ProductImportDirectTransferDefinition.php:60,115,142`; `ProductImportDirectTransferService.php:673` |
| 19 | `ke_toan_kho_phan_bo_hang.manage` | Phân bổ hàng | `ProductAllocation.php:118,148` | — |
| 20 | `ke_toan_kho_phan_bo_noi_dia.manage` | Phân bổ nội địa | `InlandProductAllocation.php:136` | — |
| 21 | `ke_toan_kho_phan_bo_dieu_chuyen.manage` | Phân bổ điều chuyển | `TransferProductAllocation.php:111` | `TransferProductAllocation.php:46,159` |

### Nhóm V — Kiểm kê
| # | Code | Nhãn | Gate ERP | Gate HRM |
|---|---|---|---|---|
| 22 | `ke_toan_kho_bien_ban_kiem_ke.manage` | Biên bản kiểm kê | `InventoryAuditReport.php:432`; `InventoryAuditReportsController.php:37` | `InventoryAuditReport.php:133` (`PERMISSION_CREATE`) |
| 23 | `ke_toan_kho_nhap_dieu_chinh_kiem_ke.manage` | Nhập kho điều chỉnh kiểm kê | `WarehouseInventoryImport.php:92,265`; notify `…ImportsController.php:190,260` | `WarehouseInventoryImport.php:59,109`; `WarehouseInventoryImportDefinition.php:60,101`; `WarehouseInventoryImportWriteService.php:365` |
| 24 | `ke_toan_kho_xuat_dieu_chinh_kiem_ke.manage` | Xuất kho điều chỉnh kiểm kê ⚠️**theo tên** | `WarehouseInventoryExport.php:89,264`; notify `…ExportsController.php:199,275` | `WarehouseInventoryExport.php:48` (hằng = **tên** `'Kế toán kho'`); `WarehouseInventoryExportWriteService.php:394` — grep theo code **không bắt được** |
| 25 | `ke_toan_kho_tu_kiem_ke.manage` | Tự kiểm kê (chỉ thông báo) | notify `SelfInventoriesController.php:417` | `SelfInventoryWriteService.php:742` |

### Nhóm VI — Hàng mượn
| # | Code | Nhãn | Gate ERP | Gate HRM |
|---|---|---|---|---|
| 26 | `ke_toan_kho_yc_ban_hang_muon.manage` | YC bán hàng mượn | `BorrowSellRequest.php:655,781,795`; notify `BorrowSellRequestsController.php:438` | `BorrowSellRequest.php:63,150,164,271,415`; `BorrowSellRequestDefinition.php:67,92,133`; `BorrowSellRequestService.php:534,628,654` |
| 27 | `ke_toan_kho_ban_hang_muon.manage` | Bán hàng mượn | `BorrowSell.php:407`; route group `web.php:1161` | `BorrowSell.php:35,97,285,292` |
| 28 | `ke_toan_kho_yc_xuat_hang_muon.manage` | YC xuất hàng mượn | `BorrowExportRequest.php:247,319,326`; notify `BorrowExportRequestController.php:291` | `BorrowExportRequest.php:62,227`; `BorrowExportRequestDefinition.php:60,106`; `BorrowExportRequestNotifyService.php:47` |
| 29 | `ke_toan_kho_xuat_hang_muon.manage` | Xuất hàng mượn | `BorrowExport.php:185`; route group `web.php:1189` | `BorrowExport.php:57,172` |
| 30 | `ke_toan_kho_yc_gia_han_hang_muon.manage` | YC gia hạn hàng mượn | `BorrowExtendRequest.php:89,92,93,176,190,243`; route `web.php:1992`; dashboard `HomeController.php:1006,1020` | `BorrowExtendRequest.php:70,229,288,459`; `BorrowExtendRequestDefinition.php:150`; menu FE `finance.js:713` |

### Nhóm VII — Thanh toán giao hàng (ERP)
| # | Code | Nhãn | Gate ERP | Gate HRM |
|---|---|---|---|---|
| 31 | `ke_toan_kho_yc_thanh_toan_giao_hang.manage` | YC thanh toán giao hàng | `DeliveryPaymentRequest.php:433,480,486,537` | — |
| 32 | `ke_toan_kho_thanh_toan_giao_hang_nv.manage` | Thanh toán giao hàng NV | `EmployeeDeliveryPayment.php:97,137,143,225` | — |
| 33 | `ke_toan_kho_yc_thanh_toan_giao_hang_khac.manage` | YC thanh toán giao hàng khác | `OtherDeliveryPaymentRequest.php:253,297,303,353` | — |

### Nhóm VIII — Hạch toán dịch vụ (CSKH)
| # | Code | Nhãn | Gate ERP | Gate HRM |
|---|---|---|---|---|
| 34 | `ke_toan_kho_ket_qua_giao_viec.manage` | Kết quả giao việc (hạch toán DV) | `WrAssignTask.php:405,438,523,540`; notify `WrApproveResultsController.php:396,1162`; dashboard `HomeController.php:1380` | (port tương ứng nếu có) |
| 35 | `ke_toan_kho_yc_lam_dich_vu_ke_toan.manage` | YC làm dịch vụ kế toán | `WrAccountingServiceRequest.php:145,189`; notify `WrAccountingServiceRequestsController.php:155,203` | (port tương ứng nếu có) |

### Nhóm IX — Khác
| # | Code | Nhãn | Gate ERP | Gate HRM |
|---|---|---|---|---|
| 36 | `ke_toan_kho_yc_hach_toan_bo_sung.manage` | YC hạch toán bổ sung (chỉ thông báo) | notify `AdditionAccountingRequestController.php:244,332` | `AdditionAccountingRequest.php:242` |

## 6. Các mặt cắt ngang (không phải "màn" nhưng phải xử)

- **Menu (ERP `topmenubar.blade.php` + `topmenubar_old.blade.php`)**: mỗi `@if ->can('…ke_toan_kho…')` đổi sang code mới của **đúng** màn mục đó mở. Nhiều mục là OR với quyền khác (`thu_kho`, `xuat_hang_vuot_han_muc`, `is_warehouse_accountant`) → chỉ thay toán hạng `ke_toan_kho`, giữ phần OR còn lại.
- **Realtime Redis channel `ke_toan_kho<warehouse_id>`** (publish ở ProductImportRequest/WarehouseImport/WarehouseExport/Prepick*/BorrowWarning/PrepickWarning; subscribe `server_node/server.js:61`): **call của mình** — giữ **1 channel theo kho** (coarse) vì đây chỉ là tín hiệu "có phiếu mới, refresh"; *gate quyết định* vẫn là quyền mới per-phiếu ở BE. Không tách channel (tránh đụng server_node + phát sinh N channel). Ghi rõ để reviewer soi.
- **Chỗ gate "gộp" nhiều phiếu dưới 1 `->can()`** (nhánh đếm dashboard trải nhiều loại phiếu, menu OR-chain mở nhiều màn, tab/list query trả nhiều loại YC): **call của mình** — thay bằng **OR của tất cả code thành viên** của nhóm đó, KHÔNG chọn đại 1 code. Lý do: giữ đúng "không ai mất thấy/đếm" — người có bất kỳ code con nào vẫn thấy mục gộp. (Chỗ gate đơn-phiếu thì map 1-1 như §5.)
- **Người nhận thông báo** (`sendNotifyWithPermission` / `Employee::withPermission` / `Employee::getAccoungtingWarehouses` ERP; `employeeInfoIdsHavingPermission`/`notifyByPermission`/`permissionApprovers('warehouse_accountant',…)` HRM): mỗi lời gọi đổi sang code mới đúng phiếu, để chỉ người được cấp phiếu đó mới nhận.
- **Dashboard đếm phiếu chờ** (`HomeController.php:1006,1030,1380,2201`): mỗi nhánh đếm đổi sang code mới tương ứng.
- **`Warehouse::getForFilterByCurrentUser('…ke_toan_kho…')`** (ERP forAccounting blade, HRM tương tự): đổi sang code mới của màn đó.
- **`is_warehouse_accountant` (ERP `Employee.php:282`)**: **GIỮ NGUYÊN** — tra bảng `WarehouseAccountant`, độc lập quyền này. Chỉ đứng cạnh trong vài `@if` menu cũ; khi thay toán hạng `->can(...)` thì nhánh `is_warehouse_accountant` để y nguyên.
- **Gate OR `ke_toan_mua_hang`** (#10, #11): giữ nhánh OR, chỉ thay nhánh `ke_toan_kho` bằng code mới.

## 7. Rủi ro chính

1. **Tham chiếu theo TÊN `'Kế toán kho'` (không phải code)** — #24 `WarehouseInventoryExport` (HRM). Grep theo code bỏ sót. **Bắt buộc** grep thêm chuỗi tên `'Kế toán kho'` ở cả 2 repo trước khi kết luận quét đủ.
2. **Group route gate một phần** (Nhóm I): gán nhầm cả group sẽ gate luôn route lẽ ra mở → rà từng dòng.
3. **Mất quyền prod nếu thứ tự deploy sai**: code mới deploy trước khi grants được cấp → user bị chặn. Trình tự ở §8 bắt buộc đúng.
4. **Chỗ gate dùng chung model ERP↔HRM**: cùng model nhưng path khác (ERP `app/Model/...` vs HRM `Modules/Finance/Entities/...`) — không nhầm repo.
5. **Sót chỗ gate sau khi deprecate** → **fail-closed, an toàn** (đã kiểm code): `PermissionCode.php:92` + `PermissionChecker.php:192,263` đều lọc `whereNull('deprecated_at')`, nên `->has('ke_toan_kho.manage')` sau khi deprecate trả **false** → người dùng **bị chặn (lỗi ồn ào)** chứ không âm thầm được mở. Chỗ HRM gọi theo **tên** `'Kế toán kho'` qua alias cũng trỏ về code đã deprecate → cũng fail-closed. ⇒ **Chỉ chạy bước deprecate (§8.6) sau khi §11 grep xác nhận không còn tham chiếu nào.**

## 8. Trình tự triển khai (prod dùng chung DB)

1. **Catalog**: thêm 36 code mới vào `accounting.php` (`platforms:['erp','hrm']`, `legacy` trỏ tên tiếng Việt mới nếu cần). Giữ code cũ `ke_toan_kho.manage` **chưa** deprecate.
2. `php artisan permission:catalog-sync` → tạo 36 permission rows.
3. **Script migration** (artisan command **mới**, mô phỏng khuôn `RbacGrantRoleNameCodesCommand` nhưng chọn theo *ai đang giữ quyền* chứ không theo tên vai trò — khuôn cũ chỉ ghi `role_has_permissions` theo tên role nên **không** tái dùng trực tiếp được):
   - Nguồn: **cả 2** pivot — `role_has_permissions` (vai trò) **và** `employee_has_permissions` (cấp trực tiếp cho nhân viên). Mục tiêu "không ai mất quyền" phụ thuộc việc copy **cả hai**.
   - Với mỗi dòng pivot đang trỏ `permission_id` của `ke_toan_kho.manage` → nhân thành **36 dòng mới**, **sao y mọi cột khác** (role_id/employee_id, `model_type` — `App\Employee` ở ERP vs model Employee HRM, `company_id`/team, scope nếu có), **chỉ đổi `permission_id`** sang 36 code mới. (Quyền cũ `scopes=[]` nên không có bậc scope phải lo.)
   - Idempotent: dòng (owner, permission_id) đã tồn tại thì bỏ qua, không nhân đôi. Nếu prod không có dòng `employee_has_permissions` nào thì nhánh đó no-op.
   - Ghi `role_permission_history` cho mỗi role đổi (như khuôn cũ). Có `--dry-run/--verify/--report`. Chạy dry-run → verify (số owner nhận đủ 36 = số owner đang giữ quyền cũ) → ghi.
4. **Deploy code ERP + HRM** đã trỏ gate sang code mới (code cũ vẫn còn grant nên không ai mất quyền trong lúc deploy lệch nhịp).
5. **Verify** cả 2 app: người cũ vẫn làm được mọi phiếu; tích thử 1 code lẻ → chỉ mở đúng phiếu đó.
6. **Dọn**: sau khi 2 app chạy ổn **và** §11 grep xác nhận hết tham chiếu, deprecate `ke_toan_kho.manage` trong Catalog + `catalog-sync` (set `deprecated_at`; grants cũ thành vô hiệu) và gỡ alias tên `'Kế toán kho'`. Không xoá cứng (giữ dòng để truy vết lịch sử). *Vì fail-closed (rủi ro §7.5), bước này là "van an toàn": sót chỗ nào sẽ lộ ngay bằng user bị chặn, không âm thầm.*

## 9. Việc để builder tự quyết (minor)
- Slug/nhãn chính xác từng code (theo quy ước §5; chỉnh cho xuôi tiếng Việt).
- Thứ tự `order` trong Catalog để 36 code đứng cạnh nhau.
- Chia bao nhiêu commit; nhưng **phải** tách theo plan ở §10.

## 10. Đề xuất chia plan (scope check)
Việc này là 3 tiểu dự án tương đối độc lập — nên lập **3 plan**, làm tuần tự:
- **Plan 1 — Nền quyền (hrm-api):** 36 entry Catalog + command migration cấp-lại-quyền + catalog-sync. Chạy/kiểm trên DB test.
- **Plan 2 — ERP re-point (TanPhatDev):** đổi toàn bộ gate/menu/notify/dashboard/route/report ERP sang code mới. (`develop_02`)
- **Plan 3 — HRM re-point (hrm-api + hrm-client):** đổi Definitions/routes/services/FE + **xử chỗ theo-tên #24**.

Mỗi plan ra phần mềm chạy được độc lập (Plan 1 tạo quyền + giữ code cũ → không vỡ; Plan 2/3 chuyển từng app).

**Completeness là việc BẮT BUỘC đầu mỗi plan re-point (không phải lỗ hổng design):** §5 liệt kê file:line *đại diện*; con số ~252 ERP + ~105 HRM đến từ grep toàn repo ở đợt recon trước (lưu ở tool-result phiên này). Task đầu của Plan 2 và Plan 3 là **dựng danh sách chỗ dùng ĐẦY ĐỦ** = grep **cả theo code** `ke_toan_kho.manage` **và theo chuỗi tên** `'Kế toán kho'`, rồi **map từng chỗ về đúng 1 trong 36** (chỗ gộp → OR, theo §6), có review. Chỗ nào còn bỏ trên code cũ sau bước deprecate = gate chết (anti-goal §2) — nên bước map-đầy-đủ này là điều kiện ra của plan, không phải tuỳ builder.

## 11. Verify mong đợi (chung)
- Dry-run migration: số role/employee nhận 36 code = số đang có quyền cũ; report khớp.
- Sau re-point: grep `ke_toan_kho.manage` (code) **và** chuỗi tên `'Kế toán kho'` ở cả 2 repo → chỉ còn ở Catalog (định nghĩa) + alias, **không còn** ở gate/menu/notify.
- Playwright: 1 tài khoản chỉ cấp **một** code lẻ → vào/duyệt được đúng phiếu đó, các phiếu khác bị chặn.
