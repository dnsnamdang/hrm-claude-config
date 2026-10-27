# Soát lại điều kiện chờ — nhóm A (§1.1, 1.2, 1.3, 1.4, 1.14 của flows-dot1.md)

> Soạn 22/10/2026. Chỉ đọc code (`ERP/TanPhatDev`, `HRM/hrm-api` — nhánh `gop_db`) + SELECT trên `hrm_erp_21_10_prod`. Không sửa `flows-dot1.md`.
> Mốc ">30 ngày" = trước 22/09/2026. Mốc bắt đầu cấp ghi ở từng dòng (ưu tiên cột thời điểm chuyển cấp; không có thì `updated_at`/`created_at`).
> Không bảng nào trong nhóm này có cột `deleted_at` (đã kiểm `information_schema`) ⇒ không có điều kiện xoá mềm.
> Các dòng số cũ = 0 và bảng thật sự 0 dòng ở trạng thái đó: điều kiện chặt hơn không thể làm tăng số ⇒ chỉ kiểm hằng số trạng thái có đúng, không đào thêm.

## 1.1 Hợp đồng · báo giá · bàn giao

| doc_type · cấp | Điều kiện cũ | Điều kiện thật (bằng chứng) | Số cũ | Số mới | >30 ngày | Kết luận |
|---|---|---|---:|---:|---:|---|
| `firm_contract` · 1 (type≠7) | `status=2, type≠7` | `status=2` + `type ∈ {1,2,3,4,5,6,8,9,10}` (mọi type ≠7 đều có thẻ) + `company_id` = công ty user (`HomeController.php:631-910`, thẻ "Hợp đồng bán hàng chờ duyệt"… ). Không có điều kiện thêm ở cấp phiếu. Gate thật (`FirmContract.php:1128-1160`): có `approver_id` ⇒ đúng người đó; không có ⇒ quản lý phòng `department_id` **và** `is_market=0` **và** (`departments.max_value_contract` trống hoặc ≥ `total_after_vat`, trừ PL giảm/ĐHNT); ĐHNT khi phòng user tắt `department_lead_approve_principle_order` ⇒ ai cũng duyệt được. Thẻ approveList còn bọc thêm `can('Duyệt hợp đồng')` | 11 | **14** (type1:8, type2:3, type3:1, type8:2) | 1 (mốc `updated_at`; HĐ 26042, 15/08) | **Sửa số** (11 sai, đếm lại 14). Điều kiện chờ giữ; gate chi tiết nên bổ sung `is_market=0` + hạn mức `max_value_contract` |
| `firm_contract` · 1 (type=7 HĐNT) | `status=2, type=7` | `status=2, type=7` (`HomeController.php:695-737`, tách `is_zt` NULL/1 chỉ để chọn route). Gate thật (`FirmContract.php:1131-1146`): có `approver_id` ⇒ `Duyệt hợp đồng nguyên tắc` **hoặc** `Ban giám đốc duyệt hợp đồng` (không cần là approver); không có ⇒ quản lý phòng `department_id` + `is_market=0` + `Duyệt hợp đồng nguyên tắc`. Danh mục ghi "permission, company" là thiếu nhánh quản lý phòng | 3 | 3 | 1 (HĐNT 25817, `updated_at` 12/08) | Giữ số. **Sửa gate**: không có approver thì phải là quản lý phòng + quyền |
| `principle_contract_extend` · 1 | `status=11` | `type=7, status=11`, **không lọc công ty** (`HomeController.php:924-933`); gate `FirmContract.php:1318` | 0 | 0 | 0 | Giữ (nên thêm `type=7` vào điều kiện cho rõ) |
| `project_quotation` · 1 | `status=4` | `CHO_DUYET=4` (`ProjectQuotation.php:40`) | 0 | 0 | 0 | Giữ (bảng chỉ có status 3) |
| `project_quotation` · 2 | `status=2` | `CHO_HIEU_LUC=2`; thẻ approveList: `status=2 AND approver_id = user` (`HomeController.php:549-556`) | 0 | 0 | 0 | Giữ |
| `liquidation_record` · 1 | `status=2` | `status=2` + `company_id` = công ty user + **`created_by ∈ department_members` của người duyệt** (NV phòng mình quản lý + phòng mình) (`LiquidationRecord.php:258-261` tab `waiting`; `canView` `:181-185`; `Employee.php:168`) | 3 | 3 | **3** (cả 3 lập 09/05/2026, `updated_at` = `created_at`; HĐ gốc vẫn `status=3`) | Giữ số, **sửa gate** (thêm phạm vi phòng người lập). **Nghi rác cần nghiệp vụ**: 3 biên bản cùng 1 người lập (943) treo 5,5 tháng |
| `hand_over_work` · 1 | `status=2` | `CHO_TP_DUYET=2`, quản lý phòng `department_id` (`HandOverWork.php:147-150`). Không có thẻ approveList | 0 | 0 | 0 | Giữ |
| `hand_over_work` · 2 | `status=4` + còn dòng `is_acceptance=0` | Đúng như cũ (`HandOverWork.php:152-165`) | 5 | 5 | **5** (mốc `updated_at`: 1 phiếu 02/10/2025, 4 phiếu 06/05/2026) | Giữ điều kiện. **Nghi rác cần nghiệp vụ**: cả bảng chỉ có 5 phiếu, đều treo ở bước tiếp nhận, không phòng nhận nào tiếp nhận |
| `service_export_request` · 1 | `status=2` | `status=2` + **công ty của NGƯỜI LẬP** = công ty user (`whereHas employee_create.info.company_id`, `HomeController.php:1401-1403`), không theo `company_id` phiếu | 0 | 0 | 0 | Giữ số; gate phạm vi ghi lại "công ty người lập" |

## 1.2 Kế hoạch · chỉ tiêu kinh doanh

| doc_type · cấp | Điều kiện cũ | Điều kiện thật (bằng chứng) | Số cũ | Số mới | >30 ngày | Kết luận |
|---|---|---|---:|---:|---:|---|
| `sales_employee_plan` · 1 | `status=2` | Thẻ: `status=2` + `department_id` (phòng của KH) ∈ phòng user quản lý trong công ty đang làm (`HomeController.php:2088-2096`). Gate nút (`SalesEmployeePlan.php:521-530`) xét phòng **người lập** | 1 | 1 | **1** (KH năm **2023**, `received_time` 20/12/2023) | Giữ điều kiện. **Nghi rác cần nghiệp vụ**: KH năm 2023 treo ~22 tháng; nghiệp vụ nên đóng/huỷ, hoặc thêm điều kiện `year >= năm hiện tại` |
| `sales_department_plan` · 1 | `status=2` | `status=2` + `company_id` (`HomeController.php:2106-2110`) | 0 | 0 | 0 | Giữ |
| `sales_company_plan` · 1 | `status=2` | `status=2` + `company_id` (`:2120-2124`) | 0 | 0 | 0 | Giữ |
| `market_employee_plan` · 1 | `status=2` | `CHO_TP_DUYET=2` + phòng quản lý (`HomeController.php:2050`) | 0 | 0 | 0 | Giữ |
| `market_department_plan` · 1 | `status=2` | `CHO_DUYET=2` | 0 | 0 | 0 | Giữ |
| `market_company_plan` · 1 | `status=2` | `CHO_DUYET=2` | 0 | 0 | 0 | Giữ |
| `business_target_company` · 1 | `status=2` | `CHO_DUYET=2` | 0 | 0 | 0 | Giữ |
| `business_target_for_department` · 1 | `status=2` | `CHO_DUYET=2` + `company_id` (`HomeController.php:500-514`) | 0 | 0 | 0 | Giữ |
| `division_market_employee` · 1 | `status=3` | `CHO_DUYET=3`, `DA_DUYET=2` (`DivisionMarketDepartmentEmployee.php:34-37`; thẻ `HomeController.php:2491`) | 0 | 0 | 0 | Giữ (bảng có 14 phiếu, đều `status=2` = đã duyệt) |

Ghi chú: KH NV `status=3` (TP đã duyệt, 10 KH bán hàng + 13 KH thị trường) là đang chờ gộp vào KH phòng — không phải bước duyệt trên phiếu NV, đúng là không đưa vào.

## 1.3 Dự án · giải pháp · báo giá BOM (HRM Assign)

| doc_type · cấp | Điều kiện cũ | Điều kiện thật (bằng chứng) | Số cũ | Số mới | >30 ngày | Kết luận |
|---|---|---|---:|---:|---:|---|
| `bom_quotation` · 1 | `is_summary=0, status=2` | `is_summary=0` + `status=2` + `department_id ∈ phòng quản lý` (`QuotationService.php:4398-4445` `applyPendingApprovalScope`, dùng chung cho list + màn chi tiết; nút `ensureTpCanApprove :4977`) | 35 | 35 | **20** (mốc = lần cuối `quotation_histories.to_status=2`) | Giữ. Đã kiểm: không báo giá mới hơn cùng dự án + giải pháp; dự án gốc: 31 ở "Dự toán", 1 ở "Thương thảo giá", **3 đã lùi về "Thu thập thông tin"** (BG #17, #22, #108 — nghi lỗi thời). 20/35 treo >30 ngày — nên báo nghiệp vụ, chủ yếu phòng 55 và 47 |
| `bom_quotation` · 2 | `is_summary=0, status=3` | `status=3` + `company_id` (`:4436-4442`) | 0 | 0 | 0 | Giữ |
| `summary_quotation` · 1 | `is_summary=1, status=2` | `SUMMARY_STATUS_CHO_DUYET=2` (`Quotation.php:116`) | 0 | 0 | 0 | Giữ |
| `prospective_project_extension` · 1 | `status=1` | `status=1` + `department_id ∈ phòng quản lý` (`ProspectiveProjectExtensionService.php:250-287` `pendingQuery`) | 1 | 1 | 0 (lập 19/10) | Giữ |
| `prospective_project_extension` · 2 | `status=2` | `status=2` + `company_id` | 0 | 0 | 0 | Giữ |
| `hrm_contract` · 1 | `status=2` | — (bảng rỗng) | 0 | 0 | 0 | Giữ |
| `handover` · 1 | `status=2` | — (bảng rỗng) | 0 | 0 | 0 | Giữ |
| `handover_item` · 1 | `receive_status=0` + cha `status=3` | — (bảng rỗng) | 0 | 0 | 0 | Giữ |
| `request_solution` · 1 | `status=2` | `status=2` + nhánh theo `prospective_projects.implementation_type` (nối qua `project_key`): **3 (liên phòng) hoặc NULL ⇒ `receive_dept ∈ phòng quản lý`; 2 (theo phòng) ⇒ `receive_dept` = phòng CỦA user** (không cần quản lý) (`RequestSolutionService.php:169-221`) | 9 | 9 | **9** (mốc `sent_date`; mới nhất 11/09) | Giữ số, **sửa gate** (thêm nhánh type 2 = phòng của user). **Nghi rác cần nghiệp vụ**: cả 9 treo >40 ngày; #14 (dự án đã lùi về "Thu thập thông tin") và #27 (dự án đã sang "Dự toán") lệch trạng thái dự án |
| `solution_adjustment_request` · 1 | `status=1` | `status=1` (`SolutionAdjustmentRequest.php:84-110`; gate PM giải pháp hoặc quản lý `request_solutions.receive_dept`) | 1 | 1 | **1** (lập 21/08) | Giữ. **Nghi rác cần nghiệp vụ**: giải pháp #33 đã sang "Đã duyệt giá" (13), báo giá BG-2026-00169 đã lập sau yêu cầu 5 phút ⇒ yêu cầu điều chỉnh có lẽ đã lỗi thời |
| `solution_review_profile` · 1 | `status='pending'` | Bảng không có giá trị `pending` (có approved 11, draft 2, expired 1, finalized 1) | 0 | 0 | 0 | Giữ |
| `solution_module_review_profile` · 1 | `status='pending'` | bảng rỗng | 0 | 0 | 0 | Giữ |
| `solution` · 1 | `status=3` | `STATUS_CHO_PM_DUYET=3` (`Solution.php:16`), gate `pm_id` | 1 | 1 | **1** (`updated_at` 04/09) | Giữ. YC giải pháp gốc `status=6` (đang thực hiện), dự án "Đang làm giải pháp" ⇒ chờ thật |
| `solution` · 2 | `status=5` | `STATUS_CHO_LEADER_DUYET=5` | 0 | 0 | 0 | Giữ |
| `solution` · 3 | `status=9` | `STATUS_CHO_DUYET_GIAI_PHAP=9` | 0 | 0 | 0 | Giữ |
| `task` · 1 | `status=2` | `PENDING_APPROVAL=2` + `Duyệt triển khai task` + phòng của người xử lý ∈ `listManageDepartmentIdsWithOwn()` (**gồm cả phòng của chính user**) (`Task.php:253-278`) | 0 | 0 | 0 | Giữ số; gate ghi rõ "phòng quản lý + phòng mình" |
| `task` · 2 | `status=6` | `REVIEW=6` + `approver_id` = user (`Task.php:280-283`) | 2 | 2 | **2** (`submitted_at` 15/07 và 27/07) | Giữ. Treo ~3 tháng, nên báo nghiệp vụ |
| `issue` · 1 | `status='resolved'` | 0 dòng | 0 | 0 | 0 | Giữ |
| `hrm_settlement_contract` · 1, 2 | `status=2` / `3` | 0 dòng | 0 | 0 | 0 | Giữ |

## 1.4 Hàng hoá · hỏi giá · tính giá

| doc_type · cấp | Điều kiện cũ | Điều kiện thật (bằng chứng) | Số cũ | Số mới | >30 ngày | Kết luận |
|---|---|---|---:|---:|---:|---|
| `price_asking_request` · 1 | `status=2` | `status=2` + `company_id` = công ty đang làm + quyền PTKD (`PriceAskingAccess.php:119-122` `canPtkd`). Không có màn danh sách chờ riêng | 5 | 5 | 0 (sớm nhất 19/10) | Giữ |
| `price_asking_temp_product` · 1 | `pcc.status=6` | `pcc.status=6` **+ hàng nằm trong 1 YCHG (`price_asking_request_products.parent_id`) đang `status=2`** + `pcc.company_id` = công ty phiếu (`PriceAskingRequestService.php:458-482` `tempForm`: `can_approve = phiếu ở Chờ PTKD && isTemp`) | 1 | 1 | 0 (21/10) | **Sửa điều kiện** (thêm phiếu cha `status=2`); số không đổi. Lưu ý: `isTemp` gồm 6/7/8 — PTKD đổi ý được, nhưng "chờ" chỉ là 6 |
| `price_asking_request_group` · 1 | `status=5` (cha ∈ ASKING) | `g.status=5` + cha ∈ `ASKING_STATUSES` (10,1,5,7) + công ty phiếu = công ty đang làm + XNK phân công hiện hành (`assign_histories`, `employee_date_to IS NULL`) = user + quyền XNK (`PriceAskingAccess.php:145-165` `groupActions`) | 24 | 24 | **11** (mốc = `price_asking_requests.approved_time` — lúc PTKD duyệt; `xnk_approved_at` trống) | Giữ. Cả 24 nhóm đều có XNK phân công còn hiệu lực. Không dùng `updated_at` của nhóm: bị backfill 20–21/10 nên ra 0 nhầm |
| `price_asking_request_group` · 2 | `status=1` | `g.status=1` + cha ∈ `ASKING_STATUSES` + **chưa có YCTG** (`NOT EXISTS price_calculate_requests.group_id = g.id`) + `g.company_id` + XNK hiện hành (`PriceCalculateRequestService.php:175-194` `pendingGroups`; `groupActions :163`) | 51 | 51 | **37** (mốc `g.xnk_approved_at`; sớm nhất 03/06) | **Sửa điều kiện** (thêm "chưa có YCTG"); số không đổi. 37/51 treo >30 ngày (48 nhóm có cha status=1 = phiếu cũ ERP) — **nghi tồn đọng từ ERP cần nghiệp vụ** dọn |
| `price_calculate_request` · 1 | `status=2` | `status=2` + `company_id` + **chưa có PTG** (`NOT EXISTS price_calculates`) + nhóm chưa đóng (`g.status NOT IN (4,9,6)` hoặc không có nhóm) (`PriceCalculateService.php:183-200` `pendingRequests`; `PriceCalculateAccess.php:123-127` `canCalculate`) | 5 | 5 | 0 (20–21/10) | **Sửa điều kiện** (thêm 2 điều kiện); số không đổi |
| `product_price_approval` · 1 | có dòng | Có dòng + `pa.company_id` = công ty đang làm (`ProductPriceApprovalService.php:264-272`) | 1 | 1 | 0 (12/10) | Giữ |

## 1.14 Họp

| doc_type · cấp | Điều kiện cũ | Điều kiện thật | Số cũ | Số mới | >30 ngày | Kết luận |
|---|---|---|---:|---:|---:|---|
| `meeting_room_booking` · 1 | `status=1` | bảng `meeting_room_bookings` rỗng trên DB này | 0 | 0 | 0 | Giữ (không kiểm thêm được vì không có dữ liệu) |

---

## Dòng đổi số / đổi điều kiện / đổi gate

**Đổi số:**
1. `firm_contract` cấp 1 (type≠7): **11 → 14** (đếm sai, không phải do điều kiện).

**Đổi điều kiện chờ (số không đổi trên dump này, nhưng phải khai đúng khi làm registry):**
2. `price_asking_temp_product`: thêm `EXISTS price_asking_request_products → price_asking_requests.status=2` cùng công ty.
3. `price_asking_request_group` cấp 2: thêm `NOT EXISTS price_calculate_requests.group_id`.
4. `price_calculate_request`: thêm `NOT EXISTS price_calculates` + nhóm chưa đóng (`g.status NOT IN (4,9,6)`).
5. `principle_contract_extend`: thêm `type=7` cho rõ.

**Đổi gate (ai thấy phiếu):**
6. `firm_contract` HĐNT: không có approver ⇒ quản lý phòng + `Duyệt hợp đồng nguyên tắc`; có approver ⇒ ai có quyền HĐNT/BGĐ.
7. `firm_contract` type≠7: thêm `is_market=0` + hạn mức `max_value_contract`.
8. `liquidation_record`: thêm `created_by ∈ department_members`.
9. `request_solution`: dự án `implementation_type=2` ⇒ `receive_dept` = phòng của user.
10. `service_export_request`: công ty xét theo người lập.
11. `task` cấp 1: phòng quản lý **gồm cả phòng mình**.

**Nghi rác, cần nghiệp vụ xác nhận:**
- `liquidation_record` 3 phiếu (09/05/2026)
- `hand_over_work` cấp 2: 5 phiếu (cả bảng)
- `sales_employee_plan` 1 KH năm 2023
- `request_solution` 9 phiếu (#14, #27 lệch trạng thái dự án)
- `bom_quotation` cấp 1: 3 báo giá (#17, #22, #108) có dự án đã lùi về "Thu thập thông tin"; 20/35 treo >30 ngày
- `solution_adjustment_request` #1 (giải pháp đã duyệt giá)
- `price_asking_request_group` cấp 2: 37/51 nhóm treo >30 ngày, phần lớn là phiếu cũ ERP
