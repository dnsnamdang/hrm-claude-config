# Duyệt nhanh / hàng loạt ở "Chờ tôi duyệt" — bảng rà từng loại (17/11/2026) — @cuong61n

Quyết định điều phối: chỉ bật loại mà ở màn gốc bấm Duyệt KHÔNG phải nhập thêm gì (không form, không chọn người/ngày/kho, không lý do/số liệu bắt buộc); mỗi lần hàng loạt MỘT loại phiếu, tối đa 50 phiếu; Từ chối vẫn mở màn gốc.
Điều kiện bật: (a) payload cố định, (b) endpoint của màn gốc TỰ chặn người thiếu quyền / sai trạng thái (BE là chốt chặn thật), (c) người dùng không nhập gì thêm.

Cơ chế (không viết lại nghiệp vụ duyệt): mỗi phiếu → kiểm phiếu còn trong "Chờ tôi duyệt" của người bấm + đúng cấp + `truth()` của Definition, rồi gọi ĐÚNG route duyệt của màn gốc bằng sub-request (cùng user, cùng header) nên middleware, FormRequest::authorize, controller, thông báo, lịch sử của màn gốc chạy nguyên. Mã: `Modules/ApprovalCenter/Support/QuickApproveRegistry.php` (khai loại), `QuickApproveRunner.php`, `Http/Controllers/Api/V1/QuickApproveController.php`, `Routes/api/quick-approve.php`.
Mỗi phiếu 1 giao dịch riêng (DB::beginTransaction; màn gốc trả lỗi / không chuyển cấp thì rollback). Thành công = HTTP 2xx, thân không `success=false`/`code>=400`, và phiếu thật sự rời cấp cũ.

## A. BẬT duyệt nhanh (49 loại / các cấp ghi trong cột Cấp)

| doc_type | Cấp bật | Endpoint màn gốc | Payload | BE tự chặn (file:dòng) |
|---|---|---|---|---|
| attendance | 1; 2 (NSHC) | POST timesheet/attendance/approve; POST timesheet/attendance/{id}/nshc-approve | `{id, attendance_status:2}`; - | AttendanceApproveRequest::authorize → can_approve; Attendance::canNSHCApprove (Entities/Attendance.php:243) |
| late_early_out | 1 | POST timesheet/late-in-early-out/approve | `{id, late_early_out_status:2}` | LateEarlyOutApproveRequest (AuthorizesApproveAction) → can_approve |
| overtime_requirement | 1 | POST timesheet/overtime-requirement/approve | `{id, overtime_requirement_status:2}` | như trên |
| overtime_assignment | 1 | POST timesheet/overtime-assignment/approve | `{id, overtime_assignment_status:2}` | như trên (OvertimeAssignmentController.php:126 vượt trần giờ → 422, báo lỗi) |
| request_update_timesheet | 1, 2 | POST timesheet/request-update-working/storeApprove | `{id, status:'approve'}` | trait authorize → can_approve; cấp do BE suy (RequestUpdateTimeSheetService.php:260-281) |
| bonus_distribution | 1 | POST payroll/bonus-distributions/{id}/approve | - | Controller :108 mã `payroll.bang_chia_thuong.approve`; Service :163 trạng thái |
| meeting_room_booking | 1 | PUT meeting/room-bookings/{id}/approve | - | MeetingRoomBookingService::approve :755-795 |
| business_target_department / _employee | 1 | POST finance/business-target-{departments,employees}/{id}/approve | - | BusinessTargetBaseController::transition (canApprove, assertStatus) + checkPermission |
| division_market_employee | 1 | POST finance/division-market-employees/{id}/approve | - | transition canApprove; assertWithinLimit → 422 báo lỗi |
| sale_plan_employee, market_plan_employee | 1 | POST finance/{sale,market}-plan-employees/{id}/approve | - | canApprove + checkPermission (cấp 2 "Gửi BGĐ" không bật) |
| delivery_request | 1 | POST finance/delivery-requests/{id}/approve | - | DeliveryRequest::canApprove :430; DeliveryRequestWriteService.php:196 |
| borrow_extend_request | 1,2,3 | POST finance/borrow-extend-requests/{id}/approve | - | BorrowExtendRequestService::approve :453 rẽ cấp theo status |
| prepick_extend_request, prepick_transfer_request | 1,2,3 | POST finance/prepick-{extend,transfer}-requests/{id}/approve | - | Service::approve (:694-760 / :748-830) |
| borrow_sell_request | 1 (TP), 2 (BGĐ) | POST …/{id}/manager-approve ; …/board-of-manager-approve | - | canManagerApprove :167, canBoardOfManagerApprove :178 (cấp 3 là lập phiếu xuất: không bật) |
| product_prepick_request | 1 (TP) | POST finance/product-prepick-requests/{id}/approve | - | Service::approve :839-866 (cấp BGĐ cần "Giữ đến ngày": không bật) |
| product_import_request | 1 (TP) | POST finance/product-import-requests/{id}/department-manager-approve | `{status:2}` | canApproveByManager :1109 (BKS/BGĐ cần giá mua duyệt: không bật) |
| product_import_direct_transfer, self_inventory, position_inventory_result, warehouse_transfer | 1 | POST finance/…/{id}/approve | - | canApprove / lockOrConflict / isAccountantOf (WarehouseTransferController.php:399) |
| product_export_request | 2 (BGĐ) | POST assign/product-export-requests/{id}/manager-approve | - | canBoardOfManagerApprove + checkPermission; vượt hạn mức công nợ → 409 báo lỗi, mở phiếu |
| delivery_contract | 1 | POST transport/delivery-contracts/{id}/approve | `{status:1}` | checkPermission warehouse.gia_van_chuyen.approve + service :1073-1090 |
| other_delivery_trip | 1 | POST transport/other-delivery-trips/{id}/approve | - | canApprove (OtherDeliveryTripController.php:254-261) |
| discount_type | 1 | GET assign/discount_types/{id}/approve | - | checkPermission + isCanApprove (DiscountTypeController.php:112) |
| extend_end_soon_request | 1 | POST assign/extend-end-soon-request/{id}/approve | - | ExtendEndSoonRequest::canApprove :121 |
| issue | 1 | PATCH assign/issues/{id}/status | `{status:'completed'}` | IssueService::changeStatus :510 (chỉ approver) |
| prospective_project_extension, quotation | 1 (TP), 2 (BGĐ) | POST …/{id}/tp-approve ; …/{id}/bgd-approve | - | Service kiểm quyền + phòng/công ty + status |
| summary_quotation | 1 | POST assign/summary-quotations/{id}/approve | - | checkPermission + ensureCanApprove :790 |
| task_extension_request | 1 | POST assign/tasks/extension-requests/{id}/approve | - | TaskExtensionService::approve → canDecide |
| solution_review_profile, solution_module_review_profile | 1 | POST assign/solutions/{sid}/manager/review-profiles/{id}/decision ; assign/solution-modules/{mid}/…/decision | `{action:'approve'}` | SolutionService.php:2706 / SolutionModuleService.php:1396 |
| wr_service_contract | 1 | POST customer-care/wr-service-contracts/{id}/approve | - | is_can_approve (WrServiceContractController.php:331) — cấp 2 tiếp nhận không bật |
| 13 loại Quyết định: department_establishment/change/dissolution, manpower_planning, regulation_salary, regulation_general, accept_personnel, appoint_personnel, renew_labor_contract, salary_change, increase_seniority, retirement, suspend_labor_contract | 1 (xem xét→status 3), 2 (duyệt→status 5) | PUT decision/<loại>/{id chi tiết}/toggle-approve (regulation_general: regulations/general) | `{status:3}` / `{status:5}` | checkPermission middleware + DecisionService::toggleApprove :329-335. Runner chỉ gửi 3/5 và tự kiểm cấp nên không nhảy cấp được; bổ nhiệm/điều chỉnh lương/tăng thâm niên thiếu mẫu in PLHĐ → 422 báo lỗi |

## B. KHÔNG bật (lý do)

| Nhóm / loại | Lý do |
|---|---|
| assign_business, assign_business_result, assign_job, assign_job_result, assign_request, job_request, solution, course, course_request, training_request | Duyệt = lưu cả form qua update (đi kèm nhập số liệu / validate) |
| contract, payment_business_request, payment_profile, settlement_contract | Người duyệt phải nhập số liệu hạch toán / số duyệt từng dòng, hoặc chọn BGĐ |
| task_start_approval, task_result_approval | Duyệt = PUT cập nhật task phải echo title/priority → ghi đè dữ liệu task nếu sai; hoãn |
| handover | BE thiếu kiểm phòng của phiếu (chỉ truth) |
| handover_record | Route không kiểm approver/quyền, chỉ kiểm status |
| handover_item, request_solution, meeting_room_service_request | Bước tiếp nhận, không phải duyệt (request_solution cần nhập ngày/PM) |
| solution_adjustment_request | accept() không kiểm gì ở BE |
| assign_other_request, warranty_repair_handle_request, warranty_repair_request, wr_service_annex, wr_service_quotation, wr_import_result | Không có bước duyệt thuần: hành động là lập chứng từ khác / tiếp nhận (wr_import_result lập phiếu duyệt kết quả có kiểm serial) |
| bill_income, bill_payment, bill_payment_request, inventory_audit_report, bonus_end_year_settlement, delivery_cost_summary, buy_service_request (cấp KS) | Bắt buộc nhập số tiền duyệt / chi tiết / nhận xét từng dòng |
| buy_service_request (cấp TP) | BE chỉ kiểm mã quyền, không kiểm phòng (MỘT PHẦN) — để mở phiếu |
| addition_accounting_request, bill_adjust_dept_request, bill_income_request, borrow_export_request, buy_service_accounting_request, wr_accounting_service_request, service_accounting_request, exc_shortage_warehouse_import, join_export_request, split_export_request, prepick_cancel_request, product_transfer_request, warehouse_export, warehouse_export_request, warehouse_import, warehouse_import_request, warehouse_inventory_import, delivery_trip | "Duyệt" là LẬP chứng từ kế tiếp (hạch toán / phiếu kho / lập đề nghị) hoặc chỉ có "Không duyệt" |
| attendances_extend_request, business_trip_assign, business_trip_employee_request, job_assignment_note, device, late_early_out_change_end_request, course_register, training_planning, capacity_evaluate, capacity_evaluate_planning, course_student_attendance | BE không tự kiểm quyền/trạng thái (authorize luôn true hoặc không kiểm) — chỉ truth() ở Definition, không đủ chắc |
| employee_info_update_request, insurance_register | Duyệt = lưu cả hồ sơ / nhập số tiền duyệt |
| self_notification | toggleApprove không kiểm gì, phát thông báo toàn công ty |
| decision_reward | Người duyệt nhập số tiền từng dòng; controller ghi trước khi kiểm quyền |
| trouble_shooting_report | Service không kiểm quyền/status |
| decision_transfer_personnel, decision_termination_labor_contract | Cần tham số ngầm `department_dissolution_id` để đúng hiệu ứng phụ |
| decision_employee_discipline, decision_salary_bonus, decision_assign_training | Route không có middleware, quyền chỉ kiểm trong service (hoãn cho chắc) |
| price_asking_request, price_calculate_request, price_asking_group, product_price_approval | Cần xử lý hàng tạm / lập phiếu / id cha; hoãn |
| sale: division_market_department | changeStatus không kiểm canApprove (MỘT PHẦN) |
| cấp 2 của sale_plan_employee/market_plan_employee ("Gửi BGĐ"), cấp BGĐ product_prepick_request, cấp BKS/BGĐ product_import_request, cấp 1/3 product_export_request | Bước khác duyệt hoặc cần nhập thêm |

Ghi chú: danh sách A là khai báo trong `QuickApproveRegistry`; muốn thêm loại chỉ thêm 1 mục + 1 dòng ở bảng này. Test `moi_loai_bat_duyet_nhanh_co_definition_va_route_that` bắt khai sai URL.
