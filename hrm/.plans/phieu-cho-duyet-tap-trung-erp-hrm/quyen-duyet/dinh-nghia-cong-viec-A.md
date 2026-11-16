# Định nghĩa loại phiếu — nhóm Công việc, phần A (Báo giá, Báo giá tổng, YC làm giải pháp, Hợp đồng TKT) — @cuong61n

16/11/2026. Definition: `hrm-api/Modules/ApprovalCenter/Definitions/Assign/{Quotation,SummaryQuotation,RequestSolution,Contract}Definition.php`.
Test: `hrm-api/tests/Feature/ApprovalCenter/Assign/{Quotation,RequestSolution,Contract}DefinitionTest.php` (Quotation test gồm cả báo giá tổng).

| doc_type | Màn gốc | Cấp | Gate | pending local | verify | đột biến |
|---|---|---|---|---|---|---|
| quotation | /assign/quotations/{id} (chi tiết) | 1 Chờ TP (status 2), 2 Chờ BGĐ (status 3) | TP: `presale.gia_bom_giai_phap_truong_phong.approve` + quotations.department_id ∈ manageDepartmentIdsOf (chặt). BGĐ: mã BGĐ + company_id = info.company_id (công ty HỒ SƠ). Cấp 1 tự duyệt (status 1) không vào hàng chờ | 15 | 9660 cặp, 0 chênh lệch | 4/4 |
| summary_quotation | /assign/summary-quotations/{id} | 1 (status 2 "Chờ duyệt") | cùng mã TP + department_id chặt; không BGĐ | 0 | 2736 cặp, 0 | 3/3 |
| request_solution | /assign/request-solution/{id} | 1 Chờ tiếp nhận (Tiếp nhận / Từ chối cùng cờ) | `presale.yeu_cau_lam_giai_phap.confirm` + receive_dept ∈ manage ∪ phòng của mình (isCanReceive) | 6 | 5628 cặp, 0 | 5/5 |
| contract | /assign/contracts/{id} | 1 TP (2), 2 Pháp chế (14), 3 BGĐ đích danh (15) | TP: mã + phòng ∈ listManageDepartmentIds chặt; Pháp chế: mã + current company = company_id; BGĐ: mã + current company + bgd_approver_id = tôi; loại người bị ẩn giá (hide_price) | 0 | 2580 cặp, 0 | 9/9 |

Quyết định: tách báo giá tổng thành loại riêng (gate/status khác, màn riêng). Hợp đồng: mã Pháp chế/BGĐ chưa ai được cấp ở DB local nên test tự cấp cho Vai trò (rollback).

## Chỗ ghi hàng loạt đã xử lý
`ProspectiveProjectService` (đóng dự án): `Quotation::whereIn()->update(status=Đóng)` và `RequestSolution::whereIn()->update(status=Đóng)` — thêm `ApprovalInboxService::scheduleSync` cho từng phiếu. `QuotationController:1409` chỉ đổi cột ERP, không đổi status. Hợp đồng: không có ghi hàng loạt.

## Lỗi / lưu ý code gốc
- RequestSolution: `receive`/`reject` ở BE không kiểm `receive_dept` (chỉ cờ FE isCanReceive).
- Hợp đồng: người có "Xem hợp đồng ẩn giá" mà HĐ ngoài phạm vi xem chỉ Từ chối được, không Duyệt được (đã phản ánh: không nằm trong danh sách duyệt).
- Hợp đồng `quotation_id` UNIQUE + FK nên phiếu thử cần báo giá chưa có HĐ.
- Rủi ro điều phối: trait dùng chung `AssignApprovalSupport.php` bị các fork đột biến đồng thời ghi đè lẫn nhau (đã gặp `if (true)` kẹt lại, đã khôi phục) — kiểm lại trước khi chốt.
