# Kiểm toán chéo — luồng duyệt HRM vs Trung tâm phê duyệt (17/11/2026) — @cuong61n

Phạm vi: chỉ đọc. Quét độc lập (không dựa kết luận báo cáo): route BE `Modules/*/Routes` (270 route khớp approve/deny/reject/refuse/confirm/receive/accept/waiting/pending/cancel), page FE (`find pages -name '*approve*|*waiting*|*pending*|…'`, grep `Từ chối|Không duyệt`), mọi API FE gọi động từ duyệt, menu `components/menu*.js` + `subsystem-menu/*.js`, Entity có `const *WAIT*|PENDING|CHO_DUYET|REJECT*`. `ApprovalDefinitionRegistry::all()` = **127 doc_type** (đã lưu cùng thư mục scratchpad của phiên).
Ghi chú: `php artisan route:list` đang vỡ do `Modules/Decision/Routes/web.php:17` trỏ `DecisionController@index` không tồn tại (không thuộc phạm vi, chỉ nêu).

## A. Kết luận ngắn

- Các luồng có route duyệt thật + page FE đều đã có doc_type, trừ **2 luồng SÓT** (mục B) và **1 luồng treo chưa quyết** (P3).
- Không có doc_type nào trỏ `handler_path` tới page FE không tồn tại. Kiểm bằng script dựng lại chuỗi `handler_path` từng Definition rồi dò `hrm-client/pages` (xử lý `_id`): 0 MISS. Bốn mẫu động (`BaseDecisionDefinition.php:201`, `SplitJoinExportApprovalSupport.php:95`, `BusinessTargetApproval.php:69`, `EmployeePlanApproval.php:99`) kiểm tay: đủ `approve.vue` cho 19 `type_url` của Decision (`Decision.php:134-152`, kể cả `regulations/general|salary/_id/approve.vue`), `finance/{split,join}-export-requests/_id/index.vue`, `finance/{business-target-*,sale-plan-employees,market-plan-employees}`. Các path có hậu tố (`/show`, `/approve`, `/manager?active_tab=`) đều có file (`assign/{extend-end-soon-request,payment_business_request,payment_profile,settlement_contract}/_id/show.vue`, `assign/solution-modules/_id/manager.vue`, `human/self-notification/_id/approve.vue`, `timesheet/business_trip_assigns/_id/approve.vue`).

## B. SÓT (cần đăng ký hoặc cần user chốt)

| # | Luồng | Route BE | Page FE | Bằng chứng | Đề xuất gate |
|---|---|---|---|---|---|
| S1 | Biên bản bàn giao sơ bộ `handover_records` (CSKH) | `PUT customer-care/handover-records/{id}/approve` — `CustomerCare/Routes/api.php:495`, không middleware | `pages/customer-care/handover-records/*` (Duyệt + `RejectModal.vue`) | Không có Definition (`ls Definitions/CustomerCare`). `HandoverRecord.php:23-26` 2 = Chờ duyệt; BE chỉ kiểm trạng thái (`HandoverRecordService.php:185-188`), báo cáo `05-ban-hang-cskh-danh-muc.md` A8 và `phu-het-cong-viec-C.md:26` đều ghi "cần điều phối". Đây là nút Duyệt/Từ chối cho người khác người lập ⇒ THUỘC phạm vi phải đăng ký (BRIEF dòng 11), không được bỏ chỉ vì BE không chốt quyền. | Người duyệt = `approver_id` trên phiếu (cột đã bắt buộc, `HandoverRecordRequest.php:48`). Nếu user muốn "ai cũng duyệt được" như ERP thì dừng và hỏi (BRIEF dòng 26). Ghi docblock "BE không chốt quyền". |
| S2 | Thu nhập P3 `p3_salaries` (Payroll) | `POST payroll/p3_salaries` (nhận `status` từ body), `GET payroll/p3_salaries/approve`, `POST …/cancel_approve` — `Payroll/Routes/api.php:152-158`, không `checkPermission` | `pages/payroll/salary-data/p3-salary/approve.vue`, `_id/approve.vue:17-24` (nút Duyệt/Từ chối khi `status==1`) | Báo cáo `phu-het-cham-cong-nhan-su-luong-meeting.md:47,57-63` để "CHƯA ĐĂNG KÝ, báo điều phối". Bằng chứng UI đã tắt: mục menu bị comment `PayrollMenu.vue:128`, nút Gửi duyệt bị comment `_id/index.vue:16-18`; DB local 44/44 bảng "Đang tạo". Nghiêng về luồng chết nhưng màn duyệt vẫn truy cập được bằng URL và route BE còn sống nên chưa thể loại có bằng chứng đủ chắc. | Cần user chốt. Nếu giữ: thêm mã `payroll.dinh_muc_thuong_p3.approve` vào Catalog (hiện chỉ có view/create/update/delete, `Catalog/payroll.php:89-137`), gate route, người duyệt = người giữ mã tại `p3_salaries.company_id`. Nếu bỏ: ghi chính thức "luồng đã gỡ khỏi UI" kèm 2 dòng comment trên. |

## C. Bảng kiểm kê (nhóm theo module; ĐỦ = đã có doc_type, LOẠI-ĐÚNG = loại có bằng chứng đã tự kiểm lại)

### Assign / CustomerCare
| Luồng | Route BE | Page FE | doc_type / lý do loại | KL |
|---|---|---|---|---|
| Yêu cầu giải pháp | `Assign/api.php:451-455` | `assign/request-solution/pending.vue` | request_solution | ĐỦ |
| Điều chỉnh giải pháp | `:438-439` | solutions manager | solution_adjustment_request | ĐỦ |
| Hồ sơ trình duyệt GP/Module | `:506,994` | `PendingApprovalCard/Modal.vue` | solution_review_profile, solution_module_review_profile, solution | ĐỦ |
| Gia hạn DA tiềm năng | `:536-542` | prospective-projects | prospective_project_extension | ĐỦ |
| Báo giá / BG tổng hợp | `:627-632, 644, 697-702` | quotations/pending-approval | quotation, summary_quotation | ĐỦ |
| YCXH / ĐNXK / PXH | `:792-799, 846, 886-887` | finance/* | product_export_request, warehouse_export_request, warehouse_export | ĐỦ |
| Hợp đồng, Giảm giá, Handover | `:944-959, 1177, 1576-1582` | contracts, handover/pending | contract, discount_type, handover, handover_item | ĐỦ |
| Gia hạn/bắt đầu/KQ task | `:1200-1202` + task | `assign/tasks` | task_extension_request, task_start_approval, task_result_approval | ĐỦ |
| PGV/Đề xuất CV/Công tác/KQ | `:1363,1507,1518,1523` | assign_jobs, job_requests, assign_business, *_approve_result | assign_job(_result), job_request, assign_business(_result), assign_request | ĐỦ |
| Ext-end-soon / DNTT / Hồ sơ TT / Quyết toán HĐ | `Assign/Routes/{ExtendEndSoonRequest,PaymentBusinessRequest,PaymentProfile,SettlementContract}/api.php` | `_id/show.vue` | extend_end_soon_request, payment_business_request, payment_profile, settlement_contract | ĐỦ |
| Duyệt bình luận task | `Assign/api.php:1216` | không có nơi gọi (grep FE rỗng) | LOẠI-ĐÚNG | LOẠI-ĐÚNG |
| Meeting xác nhận tham dự | `Assign/Routes/Meeting/api.php:51` | assign/meeting | LOẠI-ĐÚNG: tự phục vụ (comment `:49-50`). Báo cáo đã xin user chốt | LOẠI-ĐÚNG (user chốt) |
| BOM list | không có route duyệt | bom-list | LOẠI-ĐÚNG: `STATUS_CHO_DUYET` chỉ do đồng bộ từ hồ sơ trình duyệt | LOẠI-ĐÚNG |
| Yêu cầu lắp đặt bàn giao | chỉ `Assign/api.php:1320-1327` (tab + in) | menu không link (`menu-sidebar.js:266`) | LOẠI-ĐÚNG: `CHO_TP_DUYET/TU_CHOI` của `AssemblyRequest.php:26-28` không có chỗ nào ghi trong HRM | LOẠI-ĐÚNG |
| BB bàn giao nghiệm thu | `CustomerCare/api.php:441-458` | handover-acceptance-records | LOẠI-ĐÚNG: `CHO_DUYET=3` (`HandoverAcceptanceRecord.php:27`) không nơi nào đặt, FE chỉ có 1/2 (`handoverActions.js:15-16`) | LOẠI-ĐÚNG |
| YC bảo hành/xử lý/TT/HĐ DV/Import KQ/Giao việc khác | `CustomerCare/api.php:271-475` | customer-care/* | warranty_repair_request, warranty_repair_handle_request, wr_service_quotation, wr_service_contract/annex, wr_import_result, assign_other_request | ĐỦ |
| BG dịch vụ `wr-quotations`, PBH, PGV CSKH | không route duyệt | wr-quotations... | LOẠI-ĐÚNG: tự duyệt (`WrServiceQuotation.php:93-94`; báo cáo trích dòng 84-86 là lệch, nội dung đúng), không route (`Routes/api.php:502-524`) | LOẠI-ĐÚNG |
| **BB bàn giao sơ bộ** | `CustomerCare/api.php:495` | handover-records | chưa có | **SÓT S1** |

### Finance / Warehouse / Transport / Sale / MasterData
| Luồng | doc_type / lý do | KL |
|---|---|---|
| 37 phiếu tài chính-kho-vận (bill_*, borrow_*, prepick_*, product_*/warehouse_*, delivery_*, self/position inventory, exc_shortage, split/join, buy/accounting service, division/business-target/plan, bonus end year, transport 4 loại) | đã đăng ký, mọi route approve/reject/deny của `Finance/api.php` và `Transport/api.php` khớp | ĐỦ |
| price_asking_request/group, price_calculate_request, product_price_approval | đã đăng ký | ĐỦ |
| Phiếu báo có `bill_income_reports` | LOẠI-ĐÚNG: danh sách ẩn phiếu Đang tạo của người khác (`BillIncomeReportService.php:52-77`); `canApprove` không đòi người lập (`BillIncomeReportAccess.php:72-76`) nhưng UI chỉ cho người lập thấy ⇒ tự duyệt. Ghi nhận lỗ BE nhỏ như báo cáo | LOẠI-ĐÚNG (user chốt) |
| Quyết toán thưởng NS quý | LOẠI-ĐÚNG: `STATUS_WAITING_APPROVE=2` chỉ khai báo, không nơi nào đặt | LOẠI-ĐÚNG |
| Phiếu xuất giữ `warehouse_prepick_requests` | LOẠI-ĐÚNG nhưng báo cáo phu-het chưa ghi: nhánh BKS "ERP đã tắt, HRM không sinh" (`WarehousePrepickRequest.php:32,44-45`); "Duyệt giữ hàng"/"Không duyệt" trên form là KT lập tự bấm (`WarehousePrepickRequestForm.vue:300-330`, "Không duyệt" = lưu nháp) | LOẠI-ĐÚNG (bổ sung ghi chú) |
| `warehouse_inventory_exports` CHO_DUYET=1 | LOẠI-ĐÚNG nhưng báo cáo chưa ghi rõ: chỉ có hành động "Tạo phiếu xuất hàng" (`WarehouseInventoryExport.php:144-148`), route `Finance/api.php:975-993` không có approve/reject | LOẠI-ĐÚNG (bổ sung ghi chú) |
| `borrow_exports` CHO_DUYET=2, PXH/PN lại, YCXH st14, UNC | LOẠI-ĐÚNG: route `:2227-2238` không có duyệt; trạng thái chỉ do service ghi (`BorrowExportService.php:220`) | LOẠI-ĐÚNG |
| `ProductExpectedPrice`/`regulation_scheduled_versions` pending | LOẠI-ĐÚNG: chờ ngày hiệu lực, cron áp | LOẠI-ĐÚNG |

### Timesheet / Human / Payroll / Meeting / Training / Decision / Insurance
| Luồng | doc_type / lý do | KL |
|---|---|---|
| attendance (+ nshc), extend, late-early, change-end, OT req/assign, request-update, device, job-assignment-note, business-trip assign/extend | đã đăng ký; mọi `/approve` ở `Timesheet/api.php` khớp; `overtime-allocation` dùng chung trang duyệt OT | ĐỦ |
| admin-request-update-workings, self-jobassignment, job-assignment-employee/approve, storeResult | LOẠI-ĐÚNG (lọc theo chính người dùng; đoạn lọc đã comment `AdminRequestUpdateTimeSheetService.php:54-63`) | LOẠI-ĐÚNG |
| employee_info_update_request, self_notification | đã đăng ký | ĐỦ |
| bonus_distribution | đã đăng ký | ĐỦ |
| **P3 salary** | xem S2 | **SÓT/treo S2** |
| Ứng lương, thu nhập khác | LOẠI-ĐÚNG (không cột trạng thái / TODO) | LOẠI-ĐÚNG |
| meeting_room_booking, meeting_room_service_request | đã đăng ký | ĐỦ |
| QR check-in, hủy phiếu | LOẠI-ĐÚNG | LOẠI-ĐÚNG |
| Training: course(_request/_register/_student_attendance), training_request/planning, capacity_evaluate(_planning) | đã đăng ký | ĐỦ |
| questions/{id}/deny, exam_test_results/{id}/deny, training-contract/toggle-approve, appendix-labor-contract/toggle-approve | LOẠI-ĐÚNG, tự kiểm: `QuestionController`, `ExamResultController`, `TrainingContractController` không có `deny`/`toggleApprove`; `Decision/Routes/api.php:451-461` không có route toggle-approve cho phụ lục ⇒ FE `appendix-labor-contract/_id/approve.vue:119,152` gọi 404 | LOẠI-ĐÚNG (route chết) |
| examiners/approveExamResultOffline | LOẠI-ĐÚNG: người nhập điểm tự chốt | LOẠI-ĐÚNG |
| 19 loại Quyết định, trouble_shooting_report, insurance_register | đã đăng ký (`manpower_plannings_changes` không có route) | ĐỦ |
| insurance-out-company, benefits | LOẠI-ĐÚNG (danh mục / thuộc QĐ) | LOẠI-ĐÚNG |
| Rice (reject-regular/party, reject-register, reject-company…) | LOẠI-ĐÚNG, báo cáo CHƯA ghi: tự hủy đăng ký trong khung giờ (`PersonalRegistrationController.php:135-156`, `checkPassTime`) và quản lý hủy thực đơn (`Rice/api.php:92`); không có người duyệt phiếu của người khác | LOẠI-ĐÚNG (bổ sung ghi chú) |
| KPI (menu "Phê duyệt kết quả KPI") | không link, không page | không phải màn | LOẠI-ĐÚNG |

## D. Việc nên làm tiếp

1. Chốt S1 (đề xuất đăng ký theo `approver_id`) và S2 (giữ hay gỡ).
2. Bổ sung vào báo cáo phu-het: Rice, `warehouse_prepick_requests`, `warehouse_inventory_exports` (3 dòng loại có bằng chứng ở trên).
3. Sửa dòng trích sai `WrServiceQuotation.php:84-86` thành `:93-94`.
