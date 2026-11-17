# Phủ hết màn duyệt — Bán hàng (A): Kế hoạch nhân viên + Phân chia thị trường phòng ban — @cuong61n

Ngày 17/11/2026. Migration đã chạy trên DB local (chỉ file này): `Modules/Finance/Database/Migrations/2026_11_14_000001_add_hrm_columns_to_employee_plans.php` (thêm `form_version`, `customer_number`, `export_sale_value` + index).

## 1. Loại mới

| doc_type | Màn (FE) | Cấp | Gate | Pending thật local | Verify | Đột biến | Trạng thái |
|---|---|---|---|---|---|---|---|
| `sale_plan_employee` | `/finance/sale-plan-employees/{id}` (lối `?type=for-approve`) | 1 Chờ TP duyệt (Duyệt/Từ chối) · 2 TP đã duyệt (Gửi BGĐ) | mã `sale.ke_hoach_ban_hang_nhan_vien.approve` ở công ty đang làm + (có dòng `employee_manage_departments` đúng phòng phiếu — mọi công ty — hoặc đang ngồi cùng phòng) + khác người lập + `form_version=2`; cấp 2 thêm `canView` (xem bên dưới) | 0 (toàn phiếu ERP form_version 1) | verify 4.032 cặp / 47 dương / 0 chênh; PHPUnit 28.000 cặp, 93 dương | 6/6 bị bắt | xong |
| `market_plan_employee` | `/finance/market-plan-employees/{id}` | như trên, mã `sale.ke_hoach_phat_trien_thi_truong_nhan_vien.approve` | như trên | 0 | 4.008 cặp / 47 dương / 0; PHPUnit 27.720 cặp, 191 dương | dùng chung bộ test (6/6) | xong |
| `division_market_department` | `/finance/division-market-departments/{id}` | 1 Đang tạo (nút Duyệt) | mã `sale.phan_chia_thi_truong_phong_ban.approve` (công ty đang làm) + xem được phiếu (Xem tổng công ty · người lập · Xem công ty + công ty GỐC = công ty phiếu) | 0 (13 phiếu đều đã duyệt) | 3.784 cặp / 160 dương / 0; PHPUnit 8.280 cặp, 256 dương | 4/4 | xong |

Chi tiết cấp:
- **Cấp 2 của KH nhân viên**: `send-director` dùng `findOr404` → `service->find` → `canView()`. canView cho người không phải người lập: được xem nếu là người duyệt cấp TP (`department_approver_id`), `approved_by`, quyền Xem (`sale.ke_hoach_ban_hang.view` / `…phat_trien_thi_truong.view`) phạm vi Tổng công ty / Công ty (so công ty GỐC) / Phòng ban (phòng ngồi hoặc phòng quản lý), phòng/bộ phận mình quản lý (`manageDepartmentIdsOf/managePartIdsOf` ở công ty đang làm). Test cố ý dựng người có mã duyệt, cùng phòng nhưng không quyền Xem ⇒ chỉ có ở cấp 1, không có ở cấp 2.
- **Cấp BGĐ (status 4/5) KHÔNG đăng ký**: HRM không có màn BGĐ duyệt — `Modules/Finance/Routes/api.php` (khối `foreach` sale-plan/market-plan) chỉ có `approve`, `reject`, `send-director`, `cancel`; `EmployeePlan::abilities()` không có cờ BGĐ; `EmployeePlanService::sendDirector` ghi chú "chưa có màn BGĐ duyệt — spec §5". Phiếu `Chờ BGĐ duyệt` rời bảng gom với outcome "đã duyệt" (người = `department_approver_id`).
- **Phiếu ERP (`form_version=1`) KHÔNG vào**: `canApprove()/canSendDirector()` đòi `isHrmForm()`; HRM chỉ xem. 3 quyền: tất cả 1.250 phiếu ERP hiện tại.
- **Từ chối** (cấp 1): 2 → 1, lý do `department_approver_comment`, `department_approver_id` bị xoá ⇒ không biết ai từ chối (outcome `actor_id` = null).
- Người lập luôn bị loại (isHeadOfPlan: `!isOwner()`), nên `excludeOwn()` để mặc định.
- Model: trait `SyncsApprovalInbox` đặt trên lớp cha `EmployeePlan` (boot theo từng lớp con), `approvalInboxDocType()` trả `static::APPROVAL_DOC_TYPE` (const khai ở `SaleEmployeePlan` / `MarketEmployeePlan`).

## 2. `division_market_department` — lập luận đăng ký
Phiếu chỉ có 1 Đang tạo → 2 Đã duyệt; không có "Gửi duyệt", không có "Từ chối" (route: `/{id}/approve`, `/{id}/un-approve`). Nút **Duyệt** (list `DivisionMarketDepartmentListResource` `is_can_approve`, form chi tiết `header.is_can_approve`; `DivisionMarketDepartmentForm.vue:385`) hiện trên mọi phiếu "Đang tạo" cho người có mã duyệt xem được phiếu ⇒ theo phụ lục (nghi ngờ thì đăng ký) coi "Đang tạo" = hàng chờ người có mã duyệt. **Lưu ý cho người điều phối**: bản nháp người lập chưa xong cũng vào danh sách (BE không có cờ "đã gửi"); nếu muốn thu hẹp thì cần thêm bước Gửi duyệt ở BE. Hủy duyệt đưa phiếu về Đang tạo ⇒ vào lại (lần gửi mới).
BE không chốt quyền: endpoint approve chỉ có `checkPermission` mã duyệt (không canView, không công ty phiếu) — người duyệt lấy theo điều kiện giao diện.

## 3. Rà 3 loại đợt 1 (business_target_department, business_target_employee, division_market_employee)
Đã đọc lại `HasBusinessTargetAccess` và `DivisionMarketDepartmentEmployee`: trạng thái chờ duy nhất là 2 / 3, người duyệt pending ⇒ `canView` luôn đúng (cả 2 `canView` có nhánh "pending + canApprove"), không có cấp/nhánh thiếu. KHÔNG sửa, không tăng version.

## 4. Chỗ ghi bằng query builder
`EmployeePlanService` dòng ~455 `$class::query()->whereKey($id)->update(totals)` chỉ ghi cột tổng (không trạng thái / người) nên không cần `scheduleSync`. Mọi chuyển trạng thái (send/approve/reject/sendDirector/cancel) qua `$entity->save()`. `DivisionMarketDepartment` approve/unApprove qua `save()`.

## 5. File
- Definition: `Definitions/Sale/{SaleEmployeePlan,MarketEmployeePlan,DivisionMarketDepartment}Definition.php`, `Definitions/Sale/Support/EmployeePlanApproval.php`.
- Model: `Finance/Entities/EmployeePlan/{EmployeePlan,SaleEmployeePlan,MarketEmployeePlan}.php`, `Finance/Entities/DivisionMarket/DivisionMarketDepartment.php`.
- Test: `tests/Feature/ApprovalCenter/Sale/{EmployeePlanDefinitionTest,DivisionMarketDepartmentDefinitionTest}.php`.

## 6. Việc cần người điều phối
- Chuyển người phụ trách module Finance: endpoint duyệt phiếu phân chia thị trường theo phòng ban không kiểm xem/công ty (BE không chốt quyền).
- Chưa có phiếu HRM (`form_version=2`) nào ở local ⇒ hộp thư thật đang trống ở 2 loại KH nhân viên; seed qua `approval-center:seed-test`.
- Lưu ý khi chạy kiểm thử: file Definition `DivisionMarketDepartmentDefinition.php` bị ghi đè bởi một tiến trình khác (phiên bản dựa trên trait `ApprovesByPermissionInHomeCompany`, tương đương) giữa chừng; bản hiện tại là bản đã được test/đột biến.
