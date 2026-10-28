# Soát lại điều kiện "Chờ" — §1.5 · §1.6 · §1.7 · §1.8 · §1.9 (recheck B)

> Ngày 22/10/2026. Chỉ đọc code (`ERP/TanPhatDev`, `HRM/hrm-api`, `HRM/hrm-client`) và chạy SELECT trên `hrm_erp_21_10_prod` (dump 21/10). Không sửa `flows-dot1.md`.
> Số đếm tính theo điều kiện dữ liệu đầy đủ (status + type + phiếu con + phiếu kế tiếp…). Điều kiện theo người dùng (quyền, phòng, công ty đang làm, người duyệt đích danh) không tính vào số. Mốc >30 ngày: trước 22/09/2026. Cột dùng làm mốc ghi trong từng dòng.
> HC = `ERP/TanPhatDev/app/Http/Controllers/HomeController.php` (hàm `approveList`).

## Tóm tắt

- **Không dòng nào bị thổi số** như ca `wr_information_request`. Đã soát 63 dòng, số "mới" theo code đều bằng số cũ. Ở các bước "lập chứng từ" (kho, hàng giữ, huỷ giữ, mua dịch vụ), khi lập phiếu kế tiếp thì `status` của phiếu nguồn đã chuyển đi. DB xác nhận: 0 phiếu đang chờ mà đã có phiếu con.
- **Không bảng nào có `deleted_at`** và không model nào dùng SoftDeletes.
- **Nghi rác, cần nghiệp vụ xác nhận:**

  | doc_type | Số | Vấn đề | Số nếu bỏ rác |
  |---|---:|---|---:|
  | `inland_buy_contract` | 29 | 27 phiếu có mã đuôi "ĐỂ XÓA" (phiếu chờ duyệt không xoá được nên người dùng đổi tên) | **2** |
  | `assign_department_ballot` | 7 | cả 7 phiếu đều quá 30 ngày; 3 phiếu đã có phiếu duyệt mới hơn cho cùng thương hiệu × hãng | — |
  | `exc_shortage_warehouse_import` | 10 | 3 phiếu từ 10–11/2025; 7 phiếu tạo trong 13 phút ngày 24/09, gắn với phiếu nhập kho đã xong | — |
  | `product_prepick_request` cấp 1 | 2 | #1939 quá hạn giữ từ 25/07 | 1 |
  | `prepick_transfer2` cấp 1 | 1 | #208 chờ từ 10/2025, lô nguồn về 0 | 0 |

- **Tồn đọng lớn nhưng là dữ liệu thật:** `root_order_request` cấp 2 có 209 phiếu, 129 phiếu chờ quá 30 ngày (theo `received_time`).

### Dòng đổi điều kiện (số không đổi, chỉ ghi chặt hơn)

1. `root_order_request` cấp 2: `status=3 AND EXISTS assign_histories (company_id=send_company_id, brand, manufacture, employee_date_to IS NULL, buy_employee_id NOT NULL)`. Vẫn 209.
2. `inland_buy_contract`: `status=2 AND type IN (1..5)` theo màn list. Thẻ HC thiếu type 3, hiện không có phiếu nào.
3. `warehouse_export`: thêm `type<>5` (HC:1124). Popup HRM `warehouseExportSources` thiếu điều kiện này. Vẫn 70.
4. `warehouse_import`: thêm `type<>5` + ĐNNK trỏ tới YCNH nguồn còn tồn tại (HRM ProductImportService.php:1968-1990). Thẻ HC:1140 thiếu cả hai. Vẫn 12.
5. `product_prepick_request` cấp 3: thêm `NOT EXISTS warehouse_prepick_requests`. Vẫn 3.
6. `prepick_cancel_request`: thêm `NOT EXISTS prepick_cancels` (tuỳ chọn). Vẫn 1.
7. `position_inventory_result`: phải giữ `type=1`. Bỏ đi sẽ ra 13 phiếu kế hoạch đã xong.

### Cột gate của danh mục ghi sai hoặc thiếu

- `buy_contract_annex2`: bảng không có `company_id`, không có thẻ HC. Muốn lọc công ty phải join `buy_contract2`.
- `delivery_cost_asking_request`: gate thật là người duyệt đích danh (`approver_id`), nếu không có thì quyền `Mua hàng`. Không lọc theo company.
- `product_import_request` cấp 1:
  - Loại 6: chỉ người tạo được duyệt.
  - Loại 7: thêm người lập YCXH nguồn.
- `product_export_request` cấp 1 loại 7: phạm vi công ty theo `export_company_id`.
- Thẻ HC không lọc công ty ở `product_export_request` cấp 3, `product_import_request` cấp 3/4, `borrow_sell_request` cấp BGĐ và `root_order_request` cấp 2 (theo `send_company_id`).
- `inventory_audit_report` không có thẻ HC, chỉ có route `forApprover`.

---

## Soát lại số "Chờ" — mục 1.5 Đặt mua hàng + 1.6 Mua dịch vụ

> Soát ngày 22/10/2026, DB `hrm_erp_21_10_prod` (bản dump 21/10), chỉ chạy SELECT. Mốc ">30 ngày" là trước `2026-09-22`.
> Đường dẫn ERP tính từ `ERP/TanPhatDev/`, HRM tính từ `HRM/hrm-api/`. HC = `app/Http/Controllers/HomeController.php` (hàm `approveList`).
> **Soft-delete:** cả 20 bảng trong 2 mục này **không có cột `deleted_at`**, model ERP cũng không dùng `SoftDeletes`, nên không có điều kiện xoá mềm.
> Các điều kiện theo người dùng (quyền, phòng quản lý, công ty đang làm, người duyệt đích danh) không tính vào số đếm. Chúng chỉ được ghi trong cột điều kiện để đối chiếu.

### 1.5 Đặt mua hàng

| doc_type | cấp | điều kiện cũ | điều kiện thật (SQL-ish) | bằng chứng (file:line) | số cũ | số mới | >30 ngày (cột mốc) | kết luận |
|---|---|---|---|---|---:|---:|---|---|
| `root_order_request` | 1 | `status=2` | `status=2` (người dùng: quyền TP + `department_id` ∈ phòng quản lý thuộc công ty đang làm; nút duyệt xét phòng của **người lập**) | HC:1667-1698; `app/Model/Order/RootOrderRequest.php:367-374` (for-approved), `:600-610` (canDepartmentApprove) | 5 | 5 | 0 (`department_received_time`) | giữ |
| `root_order_request` | 2 | `status=3` | `status=3` AND có `assign_histories` (company_id=`send_company_id`, brand_id, manufactures_id, `employee_date_to IS NULL`) với **bản mới nhất** có `buy_employee_id` NOT NULL | `RootOrderRequest.php:334-343,375-377` (list lọc thêm `send_company_id`), `:585-597` (canApprove lấy bản phân công mới nhất); HC:1668-1689 (thẻ **không** lọc `send_company_id`) | 209 | 209 | **129** (`received_time`, thời điểm TP duyệt) | giữ. Điều kiện phân công không loại phiếu nào: cả 209 đều có NV mua hàng đang làm (`employees.status=1`). Đây là tồn đọng thật nhưng rất cũ (sớm nhất 08/2025), cần nghiệp vụ xác nhận |
| `inland_order_request` | 1 | `status=6` | `status=6` (người dùng: quyền + `department_id` ∈ phòng quản lý) | HC:1290-1297; `app/Model/Order/InlandOrderRequest.php:163-165`, `:600-603` | 8 | 8 | 7 (`updated_at`, vì không có cột thời điểm gửi) | giữ. 7/8 phiếu cũ, sớm nhất 11/02/2026 |
| `inland_order_request` | 2 | `status=2` | `status=2` (người dùng: `created_by` ∈ thành viên công ty người duyệt) | HC:1299-1310; `InlandOrderRequest.php:159-161`, `:593-598` | 2 | 2 | 2 (`received_time`, do TP duyệt ghi, `InlandOrderRequestsController.php:860`) | giữ |
| `inland_order_summary_new` | 1 | `status=5` (type 1,2) | `status=5 AND type IN (1,2)` + company | HC:1774-1800; `app/Model/Order/InlandOrderSummaryNew.php:368-373`, `:926-928` | 24 | 24 | 0 (`received_time`) | giữ. Cả 24 phiếu do 1 người lập lúc 17:31–17:57 ngày 21/10 (thao tác thật) |
| `inland_purchase_invoice` | 1 | `status=2` | `status=2 AND type IN (1,2)` + company | HC:1748-1772; `app/Model/Order/InlandPurchaseInvoice.php:353-355`, `:665-667` | 5 | 5 | 0 (`send_approve_time`) | giữ (cả 5 phiếu đều type 1) |
| `inland_buy_contract` | 1 | `status=2` (type 1–5) | `status=2` + company. Thẻ HC chỉ đếm type 1, 2, 4, 5 (**không có type 3** Đơn hàng). Màn list `for-approved` và nút duyệt không lọc type | HC:1712-1830; `app/Model/Order/InlandBuyContractNew.php:854-856`, `:1040-1043` | 29 | 29 (code) / **2** (bỏ phiếu "ĐỂ XÓA") | 25 (`received_time`). Bỏ rác: 0 | **nghi rác cần nghiệp vụ**. 27/29 phiếu có mã đuôi `… ĐỂ XÓA` (id 1154–2362, người lập 590 / 1134, từ 04/2026). Phiếu Chờ duyệt không xoá được nên người dùng đổi tên để đánh dấu. Chỉ còn 2 phiếu thật (2398, 2400) |
| `rule_inland_buy_contract` | 1 | `status=2` | `status=2` + company | HC:1724-1733; `app/Model/Order/RuleInlandBuyContract.php:168-169`, `:264-266` | 0 | 0 | – | giữ |
| `inland_buy_contract_old` | 1 | `status=2` | `status=2` + `approver_id` = người duyệt (đích danh) + quyền | HC:1313-1321; `app/Model/Order/InlandBuyContract.php:707-709` | 3 | 3 | 1 (`updated_at`, vì không có cột thời điểm gửi) | giữ. Phiếu 540 (03/2026) đã nằm 7 tháng. Người duyệt của cả 3 phiếu đều còn làm |
| `inland_buy_contract_annex` | 1 | `status=2` | `status=2` + `approver_id` đích danh | HC:1323-1331; `InlandBuyContractAnnex.php:759-761` | 0 | 0 | – | giữ |
| `inland_buy_contract_annex2` | 1 | `status=2` | `status=2` + `approver_id` đích danh | HC:1333-1341; `InlandBuyContractAnnex2.php:425-427` | 0 | 0 | – | giữ |
| `buy_contract2` | 1 | `status=2` | `status=2` + company (gồm cả type 2 = PL bổ sung) | HC:1258-1265; `app/Model/Order/BuyContract2.php:1059-1063`, `:1249-1251` | 1 | 1 | 0 (`received_time`) | giữ |
| `buy_contract_annex2` | 1 | `status=2` | `status=2`. **Không lọc công ty**: bảng không có `company_id`, list `forApprover` chỉ lọc status, nút duyệt cũng không xét công ty. **Không có thẻ ở HC** | `app/Model/Order/BuyContractAnnex2.php:241-243`, `:299-301` | 1 | 1 | 1 (`updated_at`, 01/06/2026) | giữ. Danh mục ghi "company" là sai: muốn lọc công ty phải join `buy_contract2.company_id` |
| `order_summary2` | 1 | `status=5` | `status=5` + company | HC:1240-1246; `OrderSummary2.php:379-382`, `:1041-1043` | 0 | 0 | – | giữ |
| `purchase_invoice` | 1 | `status=2` | `status=2`. Nút duyệt xét **công ty của người lập** (không xét `company_id`). HC có 2 thẻ: `Duyệt PI mua hàng nhập khẩu` (lọc company) và `Duyệt PI` (không lọc) | HC:1249-1276; `PurchaseInvoice.php:368-370`, `:670-672` | 0 | 0 | – | giữ |
| `custom_declaration` | 1 | `status=2` | `status=2` + company | HC:1278-1288; `CustomDeclaration.php:457-459`, `:570-573` | 0 | 0 | – | giữ |
| `order_import_request` | 1 | `status=2` | `status=2` + công ty của người lập | HC:1343-1354; `OrderImportRequest.php:718-721` | 0 | 0 | – | giữ |
| `delivery_cost_asking_request` | 1 | `status=2` | `status=2`. Nút duyệt: nếu có `approver_id` thì người duyệt đích danh, nếu không thì quyền `Mua hàng`. Thẻ HC **không lọc công ty** | HC:1367-1374; `DeliveryCostAskingRequest.php:122`, `:231-232` | 0 | 0 | – | giữ. Gate trong danh mục ("company") chưa đúng, nên ghi `approver hoặc permission` |
| `assign_department_ballot` | 1 | `status=2` | `status=2` + company | HC:2329-2337; `app/Model/Order/AssignDepartmentBallot/AssignDepartmentBallot.php:65-66`, `:211-213` | 7 | 7 | **7** (`created_at`; `received_time` toàn `0000-00-00`) | **nghi rác cần nghiệp vụ**. Cả 7 phiếu đều cũ (10/2025 → 21/09/2026). 3 phiếu (279, 316, 337) đã có phiếu duyệt **mới hơn** cho cùng thương hiệu × hãng. Phiếu 339 trùng hãng với 337. Code không loại các phiếu này |

### 1.6 Mua dịch vụ

| doc_type | cấp | điều kiện cũ | điều kiện thật (SQL-ish) | bằng chứng (file:line) | số cũ | số mới | >30 ngày (cột mốc) | kết luận |
|---|---|---|---|---|---:|---:|---|---|
| `buy_service_request` | 1 | `status=2` | `status=2` (thẻ ERP và scope HRM `for-approve`: `department_id` ∈ phòng quản lý; nút duyệt ERP/HRM không lọc phòng) | HC:2424-2448; ERP `app/Model/Sale/BuyServiceRequest.php:293-300`; HRM `Modules/Finance/Entities/BuyServiceRequest/BuyServiceRequest.php:479-497` | 0 | 0 | – | giữ |
| `buy_service_request` | 2 | `status=3` | `status=3` + `company_id` = công ty đang làm | HC:2426-2430; ERP `BuyServiceRequest.php:288-291`; HRM `BuyServiceRequest.php:500-504` | 0 | 0 | – | giữ |
| `buy_service_contract` | 1 | `status=2` | `status=2` + company (nút duyệt). Thẻ HC lọc theo cấp quyền xem (tổng công ty / công ty / phòng) | HC:2451-2475; `app/Model/Sale/BuyServiceContract.php:322-325` | 0 | 0 | – | giữ |
| `buy_service_accounting_request` | 1 | `status=2` | `status=2` + company. Đã kiểm "chứng từ kế tiếp đã lập": 0 bản ghi `buy_service_accountings` trỏ về 2 phiếu này | HC:2477-2487; ERP `BuyServiceAccountingRequest.php:288-291`; HRM `Modules/Finance/Entities/BuyServiceAccountingRequest/BuyServiceAccountingRequest.php:269-272, 302-307, 394-400` | 2 | 2 | 0 (`updated_at`: 09/10 và 19/10) | giữ |

### Dòng đổi điều kiện

Không dòng nào phải sửa điều kiện vì số sai. Các điều kiện đã có trong code đều không làm giảm số đếm. Có 2 chỗ nên ghi điều kiện chính xác hơn trong danh mục:

- `root_order_request` cấp 2: `status=3 AND EXISTS(assign_histories ah WHERE ah.company_id=r.send_company_id AND ah.brand_id=r.brand_id AND ah.manufactures_id=r.manufacture_id AND ah.employee_date_to IS NULL AND ah.buy_employee_id IS NOT NULL)`. Bản phân công được xét là bản mới nhất theo `created_at`. Số vẫn là 209.
- `inland_buy_contract` cấp 1: `status=2 AND type IN (1,2,3,4,5)` theo màn list. Thẻ HC chỉ đếm `type IN (1,2,4,5)`. Hiện không có phiếu type 3 nào đang chờ nên số không đổi.

Hai dòng **nghi rác** (cần nghiệp vụ xác nhận, không sửa được bằng điều kiện code):

- `inland_buy_contract`: 27/29 phiếu có mã `LIKE '%ĐỂ XÓA%'`. Nếu loại chúng bằng `code NOT LIKE '%ĐỂ XÓA%'` thì còn **2**. Cách loại này dựa trên một quy ước đặt tên, nên cần nghiệp vụ chốt: dọn dữ liệu (huỷ các phiếu này) hay loại chúng khỏi hộp chờ.
- `assign_department_ballot`: cả 7 phiếu đều >30 ngày, trong đó 3 phiếu đã có phiếu duyệt mới hơn cho cùng thương hiệu × hãng. Đề xuất nghiệp vụ huỷ các phiếu này. Không nên thêm điều kiện "chưa có phiếu mới hơn" khi code gốc không có.

### Ghi chú bất ngờ

1. **Thẻ ERP lệch với màn list (`root_order_request` cấp 2):** thẻ `approveList` khớp phân công theo `brand_id` + `manufacture_id` nhưng không lọc `send_company_id`. Màn `for-approved` và `canApprove` thì có lọc. Kết quả: NV phụ trách cùng thương hiệu × hãng ở công ty khác được đếm phiếu trên thẻ nhưng mở ra không duyệt được. Trên toàn bảng hiện chưa lệch (209 = 209). `send_company_id` gồm công ty 1: 163, công ty 4: 44, công ty 9: 2.
2. **`root_order_request` cấp 2 tồn đọng lớn:** 129/209 phiếu đã chờ quá 30 ngày (theo `received_time`), dồn cho 9 NV mua hàng. 112/209 phiếu là phiếu con (có `parent_id`) sinh ra từ thao tác "chuyển người nhận đơn". Không thấy dấu hiệu rác: không có tên "xoá/test", phiếu nào cũng có hàng.
3. **`inland_buy_contract` ("ĐỂ XÓA"):** quy ước đổi tên này cũng gặp ở các trạng thái khác: 17 phiếu đã duyệt và 1 phiếu đang tạo cũng mang đuôi đó. Model không có hàm xoá hay huỷ cho phiếu đang Chờ duyệt, nên người dùng chỉ đổi tên được.
4. **`buy_contract_annex2`:** không có thẻ ở `approveList`, không lọc công ty. Phiếu chờ duy nhất (id 2) đã nằm từ 01/06/2026, trong khi HĐ cha (658) đã duyệt (`status=1`).
5. Với các cấp có handler HRM (`buy_service_request`, `buy_service_accounting_request`), scope HRM khớp ERP ở điều kiện dữ liệu (chỉ xét status, cộng company hoặc phòng theo người dùng). Không có điều kiện ẩn kiểu `WrServiceQuotation`.

---

## 1.7 Kho — xuất · nhập · chuyển (soát lại điều kiện chờ, 22/10/2026)

DB `hrm_erp_21_10_prod` (dump 21/10), chỉ SELECT. Mốc ">30 ngày" = trước `2026-09-22`.
Kiểm chung cho cả 13 bảng:
- Không bảng nào có cột `deleted_at`, nên không cần lọc xoá mềm.
- `approved_time` đều NULL ở mọi dòng đang chờ, nên cột mốc thực tế là `updated_at`.
- Mọi dòng `status=2` của bước "lập chứng từ" đều **chưa có** chứng từ kế tiếp (0 dòng):
  - YCXH → ĐNXK / phiếu xuất kho / phiếu xuất hàng
  - YCNH → ĐNNK / phiếu nhập hàng
  - ĐNXK → phiếu xuất kho / phiếu xuất hàng
  - Phiếu xuất kho → phiếu xuất hàng
  - ĐNNK → phiếu nhập kho
  - Phiếu nhập kho → phiếu nhập hàng
  - YCCH → YCXH (`product_transfer_requests.product_export_request_id` NULL)
  - Xuất ghép / xuất tách → ĐNXK hoặc phiếu xuất hàng
- Mọi dòng chờ đều có dòng hàng con (`*_details.parent_id`).

⇒ Ở nhóm kho, khi lập chứng từ kế tiếp thì `status` chuyển sang 3 (Đang tạo) hoặc giá trị sau đó, tức là **không** có chuyện "status=2 treo mãi". Khác với ca `wr_information_request`.

| doc_type | cấp | điều kiện cũ | điều kiện thật (SQL-ish) | bằng chứng (file:line) | số cũ | số mới | >30 ngày (cột mốc) | kết luận |
|---|---|---|---|---|---:|---:|---|---|
| `product_export_request` | 1 | `status=2` | `status=2`. Có 2 nhánh:<br>• `is_export_direct=0` → lập ĐNXK. Công ty: loại 7 so `export_company_id`, loại khác so `company_id`.<br>• `is_export_direct=1` → lập phiếu xuất thẳng (canProductExport).<br>Thẻ ERP lọc `company_id` = công ty user cho mọi loại | ERP HomeController.php:1111-1117; ERP Model/Warehouse/ProductExportRequest.php:2634 (canApprove), :2653 (canProductExport), :2717 (has_warehouse); HRM Assign WarehouseExportRequestController.php:794; HRM Assign Entities/Warehouse/ProductExportRequest.php:358 | 16 | 16 (14 ĐNXK + 2 xuất thẳng) | 0 (updated_at) | **giữ**. Lưu ý phạm vi công ty: loại 7 (3 phiếu) nên dùng `export_company_id`, thẻ ERP dùng `company_id`. Ở dữ liệu hiện tại 2 cột trùng nhau |
| `product_export_request` | 2 | `status=10` | `status=10`. Tách 2 nhánh `type=3` (mượn) và `type<>3`, theo phòng quản lý | ERP HomeController.php:1495-1531; ProductExportRequest.php:2378 (for_approve) | 1 | 1 (type 3) | 0 (updated_at) | **giữ** |
| `product_export_request` | 3 | `status=11` | `status=11`, tách theo `type=3` / `<>3`. Thẻ ERP **không** lọc công ty, danh sách `for_approve` thì lọc `company_id` | ERP HomeController.php:1512-1520; ProductExportRequest.php:2378+ | 0 | 0 | — | **giữ** (registry dùng scope company, theo danh sách) |
| `product_import_request` | 1 | `status=2` | `status=2`, cùng công ty. Hai đường:<br>• `is_import_direct=0` → lập ĐNNK (canApprove). Loại 7: người lập YCXH nguồn cũng duyệt được. Loại 6: **chỉ người tạo** duyệt.<br>• `is_import_direct=1` → lập phiếu nhập thẳng | ERP HomeController.php:1128-1133; ERP ProductImportRequest.php:1478, :1493; HRM ProductImportRequest.php:1077, :1145; HRM ProductImportService.php:2076-2092 | 27 | 27 (19 ĐNNK + 8 nhập thẳng) | 1 (updated_at, PYCNH 13558 từ 04/09) | **giữ**. Ghi chú gate: 1 phiếu loại 6 chỉ người tạo xử lý được. 10 phiếu loại 7 có thêm người lập YCXH nguồn |
| `product_import_request` | 2 | `status=12` | `status=12`. Thẻ ERP lọc `department_id ∈` phòng quản lý. HRM không lọc phòng | ERP HomeController.php:1550-1558; ERP ProductImportRequest.php:1487 | 9 | 9 | 1 (updated_at, id 11119 từ 20/06) | **giữ** |
| `product_import_request` | 3 | `status=10` | `status=10`. Thẻ ERP **không** lọc công ty | ERP HomeController.php:1533-1548 | 0 | 0 | — | **giữ** |
| `product_import_request` | 4 | `status=11` | `status=11`. Thẻ ERP không lọc công ty | ERP HomeController.php:1533-1548 | 0 | 0 | — | **giữ** |
| `warehouse_export_request` | 1 | `status=2` | `status=2 AND warehouse_id ∈ kho user làm thủ kho`. Nếu `type=5` (cùng thủ kho), nút là "Lập phiếu điều chuyển" (canCreateTransfer) thay vì "Lập phiếu xuất kho". Hiện không có dòng type 5 | ERP HomeController.php:1220-1229; ERP WarehouseExportRequest.php:540, :1043, :1048 | 84 | 84 | 6 (updated_at; cũ nhất 08/05/2026: 2 type 3 mượn, 3 type 10 tách, 1 type 7) | **giữ**. 6 phiếu cũ có phiếu cha vẫn ở trạng thái hợp lệ (YCXH=1, YC tách=7). Có thể đưa nghiệp vụ xem nhưng không loại khỏi đếm |
| `warehouse_export` | 1 | `status=2` | **ERP**: `status=2 AND type<>5 AND company_id=công ty user`.<br>**HRM** popup "Chọn phiếu xuất kho": `status=2 AND company_id`, **không** loại `type=5` | ERP HomeController.php:1119-1125; ERP WarehouseExport.php:859-862, :1085; HRM Assign ProductExportController.php:1004-1012 | 70 | 70 (ERP = HRM, không có dòng type 5) | 0 (updated_at) | **sửa điều kiện**: thêm `type<>5` cho khớp thẻ/danh sách ERP. Số không đổi. ⚠ Picker HRM lệch ERP (thiếu `type<>5`) |
| `warehouse_import_request` | 1 | `status=2` | `status=2 AND warehouse_id ∈ kho user làm thủ kho` | ERP HomeController.php:1231-1237; ERP WarehouseImportRequest.php:329, :423; HRM WarehouseImportWriteService.php:113-125, :508 | 50 | 50 | 9 (updated_at; cũ nhất 07/04/2026, 5 phiếu loại 6) | **giữ**. 9 phiếu tồn lâu, YCNH cha đều ở status 1. Nên hỏi nghiệp vụ, nhưng không có căn cứ dữ liệu để loại |
| `warehouse_import` | 1 | `status=2` | **ERP**:<br>• Thẻ: `status=2 AND company_id` (không loại type 5).<br>• canApprove: thêm `type<>5`.<br>**HRM** picker: `status=2 AND type<>5 AND company_id` AND ĐNNK có `product_import_request_id` + YCNH tồn tại | ERP HomeController.php:1136-1141; ERP WarehouseImport.php:1067, :1358; HRM ProductImportService.php:1968-1990; HRM WarehouseImport.php:261 | 12 | 12 (ERP thẻ = ERP gate = HRM picker; 0 dòng type 5, 0 dòng thiếu YCNH) | 0 (updated_at) | **sửa điều kiện**: ghi đủ `type<>5` và điều kiện có YCNH nguồn. Số không đổi |
| `product_transfer_request` | 1 | `status=2` | `status=2 AND company_id=công ty user` (canApprove ERP/HRM). Thẻ và preset `can_request` ERP lọc `created_by ∈ company_members` (công ty của người tạo) | ERP HomeController.php:1028-1035; ERP ProductTransferRequest.php:214, :330; HRM ProductTransferRequest.php:265 | 9 | 9 (company_id trùng công ty người tạo ở cả 9 dòng) | 2 (updated_at; PYCCH-07456 06/08, PYCCH-07463 07/08, công ty 8) | **giữ**. Registry nên theo `company_id` như canApprove |
| `join_export_request` | 1 | `status=2` | `status=2 AND company_id` | ERP HomeController.php:1201-1207; ERP JoinExportRequest.php:217, :344 | 1 | 1 | 0 (updated_at) | **giữ** |
| `split_export_request` | 1 | `status=2` | `status=2 AND company_id` | ERP HomeController.php:1209-1216; ERP SplitExportRequest.php:324 | 1 | 1 | 0 (updated_at 05/10) | **giữ** |
| `product_import_direct_transfer` | 1 | `status=2` | `status=2 AND company_id` | ERP HomeController.php:2196-2205; ERP ProductImportDirectTransfer.php:110; HRM ProductImportDirectTransfer.php:196, :335, :443 | 1 | 1 | 0 (updated_at) | **giữ** |
| `exc_shortage_warehouse_import` | 1 | `status=2` | `status=2 AND company_id` (canApprove/canProcess chỉ xét status + quyền) | ERP HomeController.php:524-533; ERP ExcShortageWarehouseImport.php:75, :94 | 10 | 10 | 3 (updated_at = created_at; 02/10/2025, 20/11/2025, 22/11/2025). 7 phiếu còn lại tạo **cùng lúc** 24/09/2026 13:47–14:00, gắn với phiếu nhập kho từ 08/2025–09/2026 | **nghi rác cần nghiệp vụ**: 3 phiếu tồn gần 1 năm. 7 phiếu tạo dồn trong 13 phút cho phiếu nhập kho cũ (có vẻ nhập bù). Phiếu nhập kho gốc đều đã lập phiếu nhập hàng. Điều kiện đếm giữ nguyên |
| `inventory_discrepancy_handling_import` | 1 | `status=4` | `status=4 AND company_id` (4 = CHO_DUYET; 2 = DA_GUI_NCC, không phải chờ duyệt) | ERP HomeController.php:536-545; ERP InventoryDiscrepancyHandlingImport.php:77-81, :112 | 0 | 0 | — | **giữ** |
| `delivery_request` | 1 | `status=2` | `status=2` + thủ kho các kho trên YCXH nguồn. Bảng rỗng | HRM DeliveryRequest.php:415 | 0 | 0 | — | **giữ** |

#### Dòng đổi điều kiện

- `warehouse_export` cấp 1:
  - Điều kiện mới: `status = 2 AND type <> 5 AND company_id = :company` (5 = `XUAT_DIEU_CHUYEN_CUNG_THU_KHO`, khớp thẻ ERP HomeController.php:1124 và `searchData type=approve` WarehouseExport.php:859-862). Số vẫn 70.
  - ⚠ Lệch hệ thống: popup HRM `ProductExportController::warehouseExportSources` (:1004-1012) **không** loại type 5. Hiện không ảnh hưởng vì 0 dòng type 5.
- `warehouse_import` cấp 1:
  - Điều kiện mới: `status = 2 AND type <> 5 AND company_id = :company AND EXISTS(warehouse_import_requests r JOIN product_import_requests p ON p.id = r.product_import_request_id WHERE r.id = warehouse_imports.warehouse_import_request_id)`. Số vẫn 12.
  - ⚠ Lệch hệ thống: thẻ ERP (HomeController.php:1140) không loại type 5 và không đòi YCNH nguồn. Hiện cả 3 cách đều ra 12.
- Không dòng nào khác đổi điều kiện. Tổng số "Chờ" của §1.7 giữ nguyên.

#### Ghi chú phạm vi (không đổi số)

- `product_export_request` cấp 1 loại 7: phạm vi công ty theo `export_company_id` (ERP canProductExport/isCompanyWarehouseAccountant; HRM canReject). Thẻ ERP dùng `company_id`.
- `product_import_request` cấp 1:
  - Loại 6: chỉ người tạo được duyệt (ERP ProductImportRequest.php:1483).
  - Loại 7: thêm người lập YCXH nguồn (ERP :1481).
  - Nên ghi vào gate.
- `product_export_request` cấp 3 và `product_import_request` cấp 3/4: thẻ ERP không lọc công ty. Danh sách `for_approve` / registry nên lọc theo công ty.

---

## Soát lại điều kiện "Chờ" — §1.8 Hàng mượn · hàng giữ và §1.9 Kiểm kê

> Soát 22/10/2026, chỉ đọc. Đã chạy SELECT trên `hrm_erp_21_10_prod` (dump 21/10).
> **Không bảng nào trong 2 mục này có cột `deleted_at`** (đã kiểm `information_schema.COLUMNS`), nên không có điều kiện xoá mềm.
> Mốc ">30 ngày" tính đến 22/10/2026, tức trước 22/09/2026.
> Viết tắt: HC = `ERP/TanPhatDev/app/Http/Controllers/HomeController.php`; FE = `HRM/hrm-api/Modules/Finance/Entities`; FS = `HRM/hrm-api/Modules/Finance/Services`; EM = `ERP/TanPhatDev/app/Model/Warehouse`.

**Kết luận chung:** cả hai mục **không giống ca `wr_information_request`**. Ở ERP, cả thẻ chờ duyệt (`approveList`) lẫn bộ lọc danh sách đều chỉ lọc theo `status` (+ company / phòng ban theo người dùng). Ở HRM, các scope `waiting_approve` / `orWhereApprovable` / `canApprove*` cũng vậy. Bước "phiếu kế tiếp đã lập" đã nằm sẵn trong `status`: phiếu xuất giữ nháp đẩy YC về 5, phiếu huỷ giữ đã lập đẩy YC về 1. Đã đối chiếu bằng DB: không có YC nào ở status chờ mà đã có phiếu con.
Vì vậy **không dòng nào đổi số**. Chỉ có 2 phiếu cần nghiệp vụ xem có phải rác không, và 2 dòng nên ghi rõ thêm điều kiện cho chặt.

### 1.8 Hàng mượn · hàng giữ

| doc_type | cấp | điều kiện cũ | điều kiện thật (SQL-ish) | bằng chứng (file:line) | số cũ | số mới | >30 ngày (cột mốc) | kết luận |
|---|---|---|---|---|---:|---:|---|---|
| `borrow_export_request` | 1 | `status=2` | `status=2 AND company_id=<cty>`. Bảng chỉ có status 1/4 | HC:1143-1149; EM/BorrowExportRequest.php:247-248 | 0 | 0 | 0 | giữ |
| `borrow_sell_request` | 1 (KT kho) | `status=2` | `status=2 AND company_id=<cty>`. Bảng chỉ có status 1/4 | HC:1151-1175 (vế `orWhere company+status 2`); EM/BorrowSellRequest.php:657-675 | 0 | 0 | 0 | giữ |
| `borrow_sell_request` | 2 (TP) | `status=10` | `status=10 AND department_id ∈ phòng quản lý` (gate theo người) | HC:1152-1159; EM/BorrowSellRequest.php:659-667 | 0 | 0 | 0 | giữ |
| `borrow_sell_request` | 3 (BGĐ) | `status=11` | `status=11`. ⚠ ERP **không lọc công ty** ở cả thẻ lẫn danh sách | HC:1161-1163; EM/BorrowSellRequest.php:668-670 | 0 | 0 | 0 | giữ |
| `borrow_extend_request` | 1 (TP) | `status=4` | `status=4 AND department_id ∈ phòng QL AND company_id=<cty>` | HC:1007-1015; EM/BorrowExtendRequest.php:89-103; FE/BorrowExtend/BorrowExtendRequest.php:244-256 | 0 | 0 | 0 | giữ |
| `borrow_extend_request` | 2 (BGĐ) | `status=5` | `status=5 AND company_id=<cty>` | HC:1019-1021; FE/BorrowExtend/BorrowExtendRequest.php:227-232 | 1 | 1 | 0 (`manager_approved_time` 21/10) | giữ. #3235: YCXH 43033 vẫn `borrow_status=2`, chưa trả hàng ⇒ hợp lệ |
| `borrow_extend_request` | 3 (KT kho) | `status=2` | `status=2 AND company_id=<cty>` | HC:1016-1018; EM/BorrowExtendRequest.php:91-94; FE/BorrowExtend/BorrowExtendRequest.php:219-224 | 1 | 1 | 0 (`board_of_manager_approved_time` 21/10) | giữ. #3234: YCXH 19218 còn mượn (xuất 1, trả 0) |
| `product_prepick_request` | 1 (TP) | `status=6` | `status=6 AND department_id ∈ phòng QL AND company_id=<cty>` | HC:963-973; EM/ProductPrepickRequest.php:642-659; FE/PrepickExport/ProductPrepickRequest.php:377-392 | 2 | 2 | **1** (`created_at`, chưa ai duyệt; `updated_at` = `created_at`) | **nghi rác cần nghiệp vụ**: #1939 (PYCXG-01939, cty 4, loại 99) chờ TP từ 26/06/2026, `expire_date` 25/07/2026 đã qua. Bước BGĐ bắt buộc ngày giữ là ngày tương lai, nên phiếu này đi tiếp cũng vướng |
| `product_prepick_request` | 2 (BGĐ) | `status=4` | `status=4 AND company_id=<cty>` | HC:967-969; FE/PrepickExport/ProductPrepickRequest.php:366-371 | 1 | 1 | 0 (`manager_approved_time` 20/10) | giữ |
| `product_prepick_request` | 3 (KT lập phiếu xuất giữ) | `status=2` | `status=2 AND company_id=<cty> AND NOT EXISTS(warehouse_prepick_requests w WHERE w.product_prepick_request_id=p.id)` (+ có dòng `need_export=1 AND qty>0` để chép sang) | HC:964-966; FS/WarehousePrepickRequestService.php:201-226, 330-347 (chặn "đã có phiếu xuất giữ"); :22-25 (lập nháp ⇒ YC về 5, xoá ⇒ về 2) | 3 | 3 | 0 (`board_of_manager_approved_time` 16/10, 21/10, 21/10) | **sửa điều kiện** (ghi rõ, số không đổi): cả 3 phiếu chưa có phiếu xuất giữ và có 9 dòng cần xuất |
| `warehouse_prepick_request` | 1 (BKS) | `status=4` | `status=4 AND company_id=<cty>`. Thẻ ERP còn gộp `status=3 AND created_by=<tôi>` cho "Trưởng phòng kế toán", nhưng đó là phiếu nháp của chính mình, không phải bước chờ | HC:2133-2158; EM/WarehousePrepickRequest.php:266-274 | 0 | 0 | 0 | giữ. Bảng chỉ có status 1/3 |
| `prepick_transfer2` | 1 (TP) | `status=5` | `status=5 AND company_id=<cty> AND to_employee.department_id ∈ phòng QL` (phòng của **NV nhận**) | HC:938-956; EM/PrepickTransfer2.php:147-165; FE/PrepickTransfer/PrepickTransferRequest.php:259-275, 498-511 | 1 | 1 | **1** (`created_at` 27/10/2025, chưa ai duyệt) | **nghi rác cần nghiệp vụ**: #208 (ĐCHG-00208, cty 4) treo gần 1 năm. Lô nguồn 8801 còn `qty=0`, hết hạn 21/11/2025. Tồn giữ của NV 263 cho hàng 5310 là 0, nên bước KT chắc chắn bị chặn "không đủ số lượng" (FS/PrepickTransferRequestService.php:914-936) |
| `prepick_transfer2` | 2 (BGĐ) | `status=4` | `status=4 AND company_id=<cty>` | HC:944-946; FE/PrepickTransfer/PrepickTransferRequest.php:247-252 | 0 | 0 | 0 | giữ |
| `prepick_transfer2` | 3 (KT) | `status=2` | `status=2 AND company_id=<cty>`. Lúc duyệt mới xét tồn giữ còn đủ (`availableQty`) | HC:941-943; FE/PrepickTransfer/PrepickTransferRequest.php:239-244; FS/PrepickTransferRequestService.php:914-936 | 1 | 1 | 0 (`board_of_manager_approved_time` 21/10) | giữ. #1749: lô 63593 còn qty 1. Lưu ý lô hết hạn giữ 21/10 |
| `prepick_extend_request` | 1 (TP) | `status=5` | `status=5 AND department_id ∈ phòng QL AND company_id=<cty>` | HC:982-997; EM/PrepickExtendRequest.php:373-395 | 0 | 0 | 0 | giữ |
| `prepick_extend_request` | 2 (BGĐ) | `status=4` | `status=4 AND company_id=<cty>` | HC:990-992 | 1 | 1 | 0 (`manager_approved_time` 21/10) | giữ. #1987: lô 69977 còn qty 2 |
| `prepick_extend_request` | 3 (KT) | `status=2` | `status=2 AND company_id=<cty>` | HC:987-989; FE/PrepickExtend/PrepickExtendRequest.php:211 | 3 | 3 | 0 (mốc = `board_of_manager_approved_time` nếu có, không thì `manager_approved_time`; đều 21/10) | giữ. Mọi dòng `need_extend=1` đều còn lô đủ `qty`. Lưu ý #1983/#1984 có lô hết hạn đúng 22/10 |
| `prepick_cancel_request` | 1 (lập phiếu huỷ giữ) | `status=2` | `status=2 AND company_id=<cty>`. Tương đương `NOT EXISTS prepick_cancels`: DB cho thấy status 1 ⇔ đã có `prepick_cancels`, status 2/3 ⇔ chưa có | HC:1086-1093; EM/PrepickCancelRequest.php:166-167; FE/PrepickCancel/PrepickCancelRequest.php:214, 317, 375 | 1 | 1 | 0 (`updated_at` 20/10; không có cột duyệt trước) | giữ. #4617 chưa có phiếu huỷ, lô 64919 còn qty 3 ≥ 3 |

**Chỗ ERP và HRM khác nhau (số không lệch trên dữ liệu hiện tại):**
- `borrow_extend_request` cấp TP: ERP `canTPApprove` không so công ty, HRM siết thêm `company_id` (FE/BorrowExtend/BorrowExtendRequest.php:238-243). Thẻ ERP thì có lọc công ty. Hiện cả hai cùng ra 0.
- `borrow_sell_request` cấp BGĐ: ERP không lọc công ty. Hiện có 0 phiếu.
- `borrow_export_request`, `prepick_cancel_request`: danh mục ghi "HRM không lọc công ty", còn thẻ ERP lọc `company_id`. Số toàn bảng như nhau (0 và 1).

### 1.9 Kiểm kê

| doc_type | cấp | điều kiện cũ | điều kiện thật (SQL-ish) | bằng chứng (file:line) | số cũ | số mới | >30 ngày (cột mốc) | kết luận |
|---|---|---|---|---|---:|---:|---|---|
| `self_inventory` | 1 (BKS) | `status=2` | `status=2 (CHO_KT_DUYET)`. Thẻ ERP lọc thêm `company_id`, danh sách ERP và HRM thì không | HC:2025-2030; EM/SelfInventory.php:610-611; FE/SelfInventory/SelfInventory.php:220-223 | 0 | 0 | 0 | giữ. Bảng có status 0/3/6/7 |
| `position_inventory_result` | 1 (BKS) | `type=1 AND status=2` | `type=1 (KIEM_KE) AND status=2 (KK_CHO_DUYET) AND company_id=<cty>` | HC:2017-2023; EM/PositionInventory.php:779-780 | 0 | 0 | 0 | giữ. 13 dòng `status=2` đều là `type=0` (kế hoạch, `HOAN_THANH`), không phải chờ, nên **bắt buộc giữ `type=1`** |
| `warehouse_inventory_import` | 1 | `status=1` | `status=1 (CHO_DUYET) AND company_id=<cty>` | HC:1036-1044; EM/Inventory/WarehouseInventoryImport.php:267-268 | 0 | 0 | 0 | giữ. Cả 40 dòng đều status 4 |
| `warehouse_inventory_export` | 1 | `status=1` | `status=1 (CHO_DUYET) AND company_id=<cty>` | HC:1046-1053; EM/Inventory/WarehouseInventoryExport.php:266-267 | 0 | 0 | 0 | giữ. Cả 67 dòng đều status 4 |
| `inventory_audit_report` | 1 | `status=1` | `status=1 (CHO_DUYET)` + quyền duyệt. **Không có thẻ trong `approveList`**, chỉ có route `inventoryAuditReport.forApprover` | EM/Inventory/InventoryAuditReport.php:102, 435; routes/web.php:1971 | 0 | 0 | 0 | giữ. Bảng rỗng |

### Dòng đổi điều kiện

1. `product_prepick_request` cấp 3. Điều kiện mới: `status=2 AND NOT EXISTS (SELECT 1 FROM warehouse_prepick_requests w WHERE w.product_prepick_request_id = product_prepick_requests.id)`. Số vẫn là 3. Thêm vế này để khớp với chặn trong `WarehousePrepickRequestService::dataFromRequest/store`, và để an toàn khi `status` lệch với phiếu con.
2. `prepick_cancel_request` cấp 1 (tuỳ chọn, ghi cho chặt). Điều kiện mới: `status=2 AND NOT EXISTS (SELECT 1 FROM prepick_cancels c WHERE c.prepick_cancel_request_id = prepick_cancel_requests.id)`. Số vẫn là 1.
3. `position_inventory_result`: giữ đúng `type=1 AND status=2`, không rút gọn thành `status=2` (rút gọn sẽ ra 13).

### Cần nghiệp vụ xác nhận (không đổi điều kiện)

- `product_prepick_request` #1939 (PYCXG-01939): chờ TP từ 26/06/2026, hạn giữ 25/07/2026 đã qua.
- `prepick_transfer2` #208 (ĐCHG-00208): chờ TP từ 27/10/2025, lô nguồn đã về 0 nên không bao giờ duyệt xong được.

Nếu xác nhận là rác thì số "Chờ" thực tế bằng: YC xuất giữ cấp TP **1**, Điều chuyển hàng giữ cấp TP **0**.
