# Rà lại số phiếu chờ — mục 1.10 · 1.11 · 1.12 · 1.13 của flows-dot1.md (nhóm C)

> Soạn 22/10/2026. Chỉ đọc code + SELECT trên `hrm_erp_21_10_prod`. KHÔNG sửa `flows-dot1.md`.
> Code soát: `ERP/TanPhatDev` (gop_db), `HRM/hrm-api` (gop_db).
> Mốc ">30 ngày" = trước **2026-09-22** (22/10 − 30). Cách tính mốc ghi ở từng dòng:
> - `appr` = cột thời điểm duyệt/gửi của bước trước (vd `manage_approved_time`, `approved_time`, `send_request_time`, `send_date`, `send_approve_date`).
> - `upd` = `updated_at` (dùng khi bảng không có cột thời điểm theo cấp; có thể bị lệch nếu phiếu được sửa vặt sau khi sang cấp).
>
> Không bảng nào trong 4 mục có cột `deleted_at` ⇒ không có điều kiện xoá mềm.
> Các card ERP lấy ở `ERP/TanPhatDev/app/Http/Controllers/HomeController.php` hàm `approveList()` (:493), viết tắt `HC:dòng`.

## 1.10 Thu chi

| doc_type · cấp | Điều kiện cũ | Điều kiện thật (bằng chứng) | Số cũ | Số mới | >30 ngày | Kết luận |
|---|---|---|---:|---:|---:|---|
| `bill_payment_request` · 1 TP | `status=2` | `status=2` + `company_id` = cty user + `department_id` ∈ phòng user quản lý (ERP `BillPaymentRequest.php:346-357`, card `HC:1567-1578`; HRM `Entities/BillPaymentRequest/BillPaymentRequest.php:426-445` y hệt) | 8 | 8 | 0 (upd) | Giữ |
| `bill_payment_request` · 2 KT công nợ | `status=3` | `status=3` + company (như trên :358) | 60 | 60 | 15 (appr = `manage_approved_time`) | Giữ |
| `bill_payment_request` · 3 KT trưởng | `status=4` | `status=4` + company (:361) | 70 | 70 | 24 (upd — bảng không có cột thời điểm KT công nợ duyệt) | Giữ. 24 phiếu đứng >30 ngày, cũ nhất tạo 06/12/2025 |
| `bill_payment_request` · 4 BGĐ | `status=5` | `status=5` + company (:364) | 1 | 1 | 0 (upd) | Giữ |
| `bill_payment_request` · 5 KT TT lập phiếu chi/UNC | `status=6` | `status=6` + company (:367). Đã kiểm: 0/56 phiếu đã có `bill_payments` hoặc `bill_payment_authorizations` trỏ về ⇒ không có phiếu "đã lập chứng từ nhưng chưa đổi trạng thái" | 56 | 56 | 6 (upd) | Giữ |
| `bill_payment` · 1 Thủ quỹ | `status=2` | `status=2` + company (ERP `BillPayment.php:241-250`) | 2 | 2 | 0 (upd) | Giữ |
| `bill_payment` · 2 KT trưởng (nhánh B) | `status=5` | `status=5` + company (:247) | 0 | 0 | 0 | Giữ |
| `bill_income` · 1 Thủ quỹ | `status=2` | `status=2` + company (card `HC:1462-1468`) | 0 | 0 | 0 | Giữ |
| `bill_income_request` · 1 KT lập phiếu thu | `status=2` | `status=2` + company (card `HC:1419-1427`; list ERP `for-accounting` `BillIncomeRequest.php:182-184` chỉ lọc công ty, không lọc trạng thái; HRM `BillIncomeRequest.php:296-299`). 0/3 phiếu đã có `bill_incomes` | 3 | 3 | 0 (upd) | Giữ |
| `bill_adjust_dept_request` · 1 KT lập phiếu điều chỉnh | `status=2` | `status=2` + **công ty hiện tại của NGƯỜI LẬP** = cty user (ERP list `BillAdjustDeptRequest.php:200-204` `whereHas('employee_create.info')`; HRM `BillAdjustDeptRequest.php:236-252` giống; card `HC:1429-1437` lại so `company_id` của phiếu). 0/26 đã có `bill_adjust_depts` | 26 | 26 | 7 (appr = `send_approve_date`) | Giữ số. Ghi chú gate: phạm vi công ty theo người lập, không theo cột `company_id` — 2 nguồn ERP đang lệch nhau |
| `addition_accounting_request` · 1 KT lập phiếu điều chỉnh | `status=2` | `status=2` VÀ ( `type≠7` + `company_id`=cty user **HOẶC** `type=7` + có dòng `addition_accounting_request_departments` (`parent_id`) có `support_department_id` thuộc cty user ) (ERP `AdditionAccountingRequest.php:273-295`, card `HC:1439-1458`; HRM `AdditionAccountingRequest.php:329-338`). 0/39 đã có `bill_adjust_depts` | 39 | **38** | 12 (appr = `send_date`) | Sửa điều kiện: 1 phiếu type 7 (`PYCHTBS-002017`, id 2017, tạo 03/08/2026) không có phòng hỗ trợ nào ⇒ không ai nhìn thấy/xử lý được. Nghi rác, cần nghiệp vụ |

## 1.11 Hạch toán · quyết toán

| doc_type · cấp | Điều kiện cũ | Điều kiện thật (bằng chứng) | Số cũ | Số mới | >30 ngày | Kết luận |
|---|---|---|---:|---:|---:|---|
| `settlement_contract` · 1 TP | `status=2` | `parent_id IS NULL` (list luôn lọc, `SettlementContract.php:396`) + `status=2` + `department_id` ∈ phòng user quản lý + company (list `waiting` :494-503; gate `canDepartmentApprove` :637-640). Card `HC:1600-1610` lại lọc `created_by ∈ department_members` (lệch list) | 18 | 18 | 0 (upd; `approved_time` rỗng ở cả 18) | Giữ số, bổ sung `parent_id IS NULL` vào điều kiện (hiện mọi phiếu chờ đều là gốc nên số không đổi) |
| `settlement_contract` · 2 BGĐ | `status=3` | `parent_id IS NULL` + `status=3` + `valid_approver_id` = user + company (`HC:1621-1630`, gate :641) | 0 | 0 | 0 | Giữ, thêm `parent_id IS NULL` |
| `settlement_contract` · 3 KT | `status=4` | `parent_id IS NULL` + `status=4` + company (list :495-497; gate :643). Không có điều kiện con/hạn mức nào khác | 204 | 204 | 2 (appr = `approved_time`) | Giữ. 204 phiếu đều tạo từ 30/07/2026, chỉ 2 phiếu >30 ngày ⇒ tồn đọng thật của KT, không phải rác |
| `service_accounting_request` · 1 | `status=2` | `status=2` + công ty của NGƯỜI LẬP = cty user (list `wait_approve` `ServiceAccountingRequest.php:218-222`, card `HC:1407-1416`) | 11 | 11 | 0 (appr = `approved_at`, rỗng ⇒ upd) | Giữ |
| `monthly_commission_accounting_request` · 1 | `status=2` | `status=2` (card `HC:1471-1477`, không lọc công ty) | 0 | 0 | 0 | Giữ (bảng rỗng) |
| `bill_commission_settlement_quarter` · 1 | `status=2` | `status=2` | 0 | 0 | 0 | Giữ |
| `bill_productivity_settlement_quarter` · 1 | `status=2` | `status=2` | 0 | 0 | 0 | Giữ |
| `bill_commission_settlement_month` · 1 | `status=2` | `status=2` | 0 | 0 | 0 | Giữ (bảng rỗng) |
| `bill_bonus_business` · 1 | `status=2` | `status=2` | 0 | 0 | 0 | Giữ (bảng rỗng) |
| `bonus_end_year_settlement` · 1 | `status=2` | `status=2` | 0 | 0 | 0 | Giữ (bảng rỗng) |
| `business_payment_profile` · 1 | `assign_business` type 2, `status=2` | như cũ (`AssignBusiness::HO_SO_THANH_TOAN=2`, `CHO_DUYET=2`) | 0 | 0 | 0 | Giữ. Bảng chỉ có 163 dòng `type=1, status=1` |
| `insurance_principle_accounting_request` · 1 | `status=2` | `status=2` | 0 | 0 | 0 | Giữ (bảng rỗng) |

## 1.12 Bảo hành · sửa chữa · CSKH

| doc_type · cấp | Điều kiện cũ | Điều kiện thật (bằng chứng) | Số cũ | Số mới | >30 ngày | Kết luận |
|---|---|---|---:|---:|---:|---|
| `warranty_repair_request` · 1 (C1) | `status=2` + chưa có handle request | `status=2` + `department_reception_id` = phòng user (list `waiting_handle` ERP `WarrantyRepairRequest.php:271-278`; card `HC:1832-1845`; HRM `WarrantyRepairRequestService.php:384-393`) + chưa có `warranty_repair_handle_requests` (gate HRM `WarrantyRepairRequest::canHandleRequest()` ~:286-305). Đã kiểm: 137/137 có phòng tiếp nhận, 0/137 đã có phiếu xử lý | 137 | 137 | **110** (appr = `send_request_time`) | Giữ số, **nghi tồn đọng cần nghiệp vụ**: 41 phiếu gửi từ 2025, 110/137 đứng >30 ngày. Phòng KTCN 78, KT Vinh 27, CSKH 19 |
| `warranty_repair_handle_request` · 1 (C2) | `status=2` | `status=2`, không lọc công ty/phòng (list `waiting_information` ERP `WarrantyRepairHandleRequest.php:277-282`; gate `canCreateRepairInformation` :169-172; HRM `WarrantyRepairHandleRequestService.php:259`). 0/27 đã có phiếu CCTT (`wr_service_quotations type=0`). Trạng thái 4 "Chờ CCTT bổ sung" có hằng số nhưng 0 dòng | 27 | 27 | **27** (appr = `send_request_time`; mới nhất 25/08/2026) | Giữ số, **nghi rác cần nghiệp vụ**: cả 27 phiếu đứng >30 ngày (10 từ 2025), và YC gốc của cả 27 đều đã ở trạng thái 7 "Đã xử lý xong" ⇒ nhiều khả năng đã làm xong ngoài luồng |
| `wr_information_request` · 1 (C3) | (đã sửa) `type=0, status=2` + có TB sửa chữa hoặc bảo dưỡng | Xác nhận: list HRM `WrServiceQuotationService.php:364-385` (= card ERP `HC:1908-1923`) + `warranty_repair_requests.created_by` = user. Gate nút (`WrServiceQuotation::resolveCanCreateQuotation` :411-436) rộng hơn list một chút: nhận thêm phiếu chỉ có `wr_service_quotation_costs.repair_price>0` (+4 phiếu, list không hiện), và loại phiếu có TB sửa chữa gắn >1 lỗi (0 phiếu bị loại) | 188 | **188** (gate: 192) | **174** (appr = `approved_time`) | Giữ 188. Lưu ý 174/188 đứng >30 ngày ⇒ vẫn nên hỏi nghiệp vụ có dọn không |
| `wr_service_contract` · 1 HĐ (C4) | `type=1, status=2` | `type=1, status=2` + (`department_id` ∈ phòng user quản lý HOẶC `approver_id`=user) + company (card `HC:613-628`) | 0 | 0 | 0 | Giữ |
| `wr_service_contract` · PL bổ sung | `type=3, status=2` | như cũ + điều kiện hạn mức | 1 | 1 | 0 (upd) | Giữ |
| `wr_service_contract` · PL giảm | `type=4, status=2` | `type=4, status=2` + (`department_id` ∈ phòng quản lý HOẶC `approver_id`) (card `HC:1958-1968`) | 0 | 0 | 0 | Giữ |
| `wr_service_contract_reception` · 1 (C5) | `type=1, status=3` + có `department_reception_id` + chưa có `wr_assign_tasks` (trừ st9) | **Đây là gate nút "Từ chối tiếp nhận" của HRM** (`HRM WrServiceContract.php:455-480`, chính docblock ghi là đã BỎ phần đếm số lượng), không phải màn chờ giao việc. Màn thật ERP "Phiếu chờ giao việc" (`WrAssignTasks.wait` → `WarrantyRepairContracts.searchData?type=assign-task`, `WrServiceContract.php:941-957`; card `HC:1847-1871`): `type=1, status=3` + `department_reception_id` ∈ phòng user quản lý (list) / = phòng user (card) + `id ∈ getQuantityHasRepair()` (`WrServiceContract.php:1068-1180`): còn ít nhất 1 dòng `wr_service_contract_products (handle_type=1)` / `..._product_services` / `..._extend_product_services` có `SL − annex_qty − assign_qty − SL đang giao (wr_assign_tasks gốc, status ∈ {1,7,2,8})` > 0 | 243 | **428** | **390** (appr = `approved_time`) | **Sửa điều kiện.** Chỉ 125 HĐ nằm ở cả 2 tập: 118 HĐ trong số 243 cũ không còn công/dịch vụ nào để giao (không thực sự chờ), còn 303 HĐ đã giao một phần nhưng vẫn còn số lượng thì bị bỏ sót. 168/428 HĐ duyệt từ 2025 ⇒ **nghi tồn đọng cần nghiệp vụ** (phần còn lại có thể không bao giờ giao) |
| `wr_import_result` · 1 | `status=2` | `status=2` + company (list `wait_approve_result` `WrImportResult.php:277-279`; gate `canApproveResult` :355-358; card `HC:1884-1894`). Phiếu giao việc cha của cả 290 đều ở status 2 "Đã nhập kết quả" (khớp) | 290 | 290 | **151** (upd; bảng không có cột thời điểm gửi) | Giữ số, **nghi tồn đọng**: 151 >30 ngày, 38 từ 2025 |
| `wr_assign_task_result` · 1 BKS | `parent_id` not null, `status=4` | như cũ (card `HC:1896-1906`, không lọc công ty) | 0 | 0 | 0 | Giữ (bảng không có status 4) |
| `wr_accounting_service_request` · 1 | `status=2` | `status=2` + company (card `HC:1387-1393`) | 3 | 3 | 0 (upd) | Giữ |
| `assembly_request` · 1 TP | `status=6` | `status=6` (`CHO_TP_DUYET`) + department | 0 | 0 | 0 | Giữ (bảng không có status 6) |
| `firm_warranty_request` · 1 | `status=2` | `status=2` + NV mua hàng hiện hành theo `brand_id`×`manufacture_id`×`send_company_id` (gate `canApprove` `FirmWarrantyRequest.php:400-411`). List `for-approved` (:196-198) lọc brand IN / hãng IN riêng rẽ theo công ty user, hơi rộng hơn gate. 11/11 có người phụ trách tại `send_company_id`; 0/11 đã có thư BH | 11 | 11 | 8 (upd) | Giữ |
| `firm_warranty` · 1 xác nhận hãng đã nhận | `status=2` | `status=2` + company (list `for-approved` `FirmWarranty.php:195-197`). 0/7 đã có `firm_warranty_confirms` | 7 | 7 | **7** (upd; tạo từ 10/02/2026) | Giữ số, **nghi tồn đọng**: cả 7 phiếu >30 ngày |
| `firm_warranty_confirm` · 1 | `status=2` | `status=2` + company | 0 | 0 | 0 | Giữ |

## 1.13 Vận chuyển

Tất cả 9 dòng: điều kiện `status=2` (riêng `summary_shipping_price` cấp 2 là `status=3`, `other_delivery_trip` là `status=5`), đếm lại đều **0**. Bảng có dữ liệu nhưng 0 phiếu chờ: `summary_shipping_prices` (419 dòng), `other_delivery_trips` (437), `delivery_cost_summaries` (68), `delivery_contracts` (22). Bảng rỗng: `summary_order_shipping_prices`, `delivery_payment_requests`, `employee_delivery_payments`, `other_delivery_payment_requests`. Card ERP không có điều kiện con nào làm thay đổi số 0. ⇒ **Giữ cả 9 dòng.** Không cần dò sâu thêm vì số 0 không thể giảm.

## Các dòng đổi điều kiện / số

1. **`wr_service_contract_reception` (C5): 243 → 428.** Điều kiện cũ là gate nút từ chối tiếp nhận của HRM, không phải màn chờ giao việc. Điều kiện thật: `type=1, status=3`, có phòng tiếp nhận, và `id ∈ getQuantityHasRepair()` (còn số lượng chưa giao). 390/428 HĐ đứng >30 ngày ⇒ cần nghiệp vụ xác nhận.
2. **`addition_accounting_request`: 39 → 38.** Phiếu `type=7` phải có phòng hỗ trợ. 1 phiếu mồ côi (id 2017) không ai thấy được.
3. **`settlement_contract` (3 cấp):** thêm `parent_id IS NULL`. Số không đổi.
4. **`wr_information_request` (C3):** xác nhận 188. Gate của nút rộng hơn list 4 phiếu (nhánh `costs.repair_price>0`). Danh mục nên bám list (188).

## Phát hiện thêm (ngoài các dòng có sẵn — cần quyết có đưa vào danh mục không)

Card ERP "Phiếu chờ giao việc" (`HC:1847-1871`) cộng **5 nguồn**. Danh mục mới có nguồn HĐ (C5). Còn thiếu:
- **PL bổ sung chờ giao việc:** `wr_service_contracts type=3, status=3` + `getQuantityHasRepair` + phòng tiếp nhận ⇒ **24** (22 phiếu >30 ngày).
- **HĐ bảo hành chờ giao việc:** `type=2, status=2 (BH_DA_DUYET)` + phòng tiếp nhận. Card đếm **4.544**. List thật (`WrWarrantysController::searchDataWaiting` :105-109) có thêm `is_assign=1` ⇒ **561** (503 phiếu >30 ngày). Card và list đang lệch nhau ⇒ cần nghiệp vụ chốt.
- **YC lắp đặt chờ giao việc** (`assembly_requests status=1` + còn SL) và **YC khác chờ giao việc** (`assign_other_requests status=1`): chưa đếm. Hai luồng này thuộc phạm vi luồng lắp đặt, không nằm trong 1.12.

## Dòng nghi rác / tồn đọng cần nghiệp vụ

| doc_type | Số | >30 ngày | Dấu hiệu |
|---|---:|---:|---|
| `warranty_repair_handle_request` (C2) | 27 | 27 | YC gốc đã "Đã xử lý xong", mới nhất 25/08 |
| `firm_warranty` | 7 | 7 | Gửi NCC từ 02/2026, chưa có phiếu xác nhận |
| `wr_service_contract_reception` (C5) | 428 | 390 | 168 HĐ từ 2025 vẫn còn SL chưa giao |
| `wr_information_request` (C3) | 188 | 174 | — |
| `wr_import_result` | 290 | 151 | 38 phiếu từ 2025 |
| `warranty_repair_request` (C1) | 137 | 110 | 41 phiếu từ 2025 |
| `addition_accounting_request` | 1 | 1 | type 7 không có phòng hỗ trợ |
