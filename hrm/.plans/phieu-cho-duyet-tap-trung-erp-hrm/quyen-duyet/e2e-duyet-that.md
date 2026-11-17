# Duyệt THẬT từng loại phiếu bằng giao diện (e2e) — @cuong61n

Ngày chạy: 17/11/2026 · Môi trường: local (API `php -S` :8000, client :3000, DB `local_hrm_erp`) · Registry: **128 loại**.
Khác đợt trước (chỉ kiểm danh sách + mở màn gốc): đợt này người duyệt THẬT bấm nút Duyệt trên màn gốc rồi so DB.

## 1. Kết quả tổng

| | Số loại |
|---|---|
| **XANH** — duyệt thật xong, đủ (a)(b)(c) | **71** |
| **BỎ QUA có lý do** | **53** (22 dữ liệu thử mỏng · 22 "duyệt" = lập chứng từ kế tiếp · 1 form riêng · 1 chốt chặn nghiệp vụ · 7 seedTest không dựng được phiếu chờ) |
| **ĐỎ** — lỗi thật của màn gốc, KHÔNG sửa, ghi ở mục 3 | **4** (`decision_renew_labor_contract`, `trouble_shooting_report`, `payment_business_request`, `meeting_room_booking` chưa xác minh) |
| Ca nghịch (người KHÔNG phải người duyệt), 107 loại có phiếu thử | 102 xanh · **5 đỏ** (3 lỗ hổng phân quyền BE đã tái hiện + 2 màn lỗi 5xx) |

Tiêu chí XANH của 1 loại (spec `approve.spec.ts`):
- **(a)** bảng gom `approval_inbox_items`: sau khi duyệt phiếu RỜI trạng thái chờ (state ≠ 1) hoặc sang cấp kế với `step`/`status_text` mới; mở lại Phiếu chờ duyệt thì UI khớp DB (phiếu biến mất khỏi inbox người duyệt, hoặc còn với đúng chữ cấp mới); người duyệt không còn là người duyệt cấp hiện tại thì phiếu không hiện.
- **(b)** bảng GỐC đổi ít nhất 1 cột ngoài `updated_at/by` (hoặc dòng gốc chuyển/tiêu thụ sang bảng khác) và `describe()` của Definition đổi.
- **(c)** không pageerror / console error (trừ ồn nền đã biết) / HTTP 5xx; mọi lời gọi ghi (POST/PUT/PATCH/DELETE và GET `…/approve`) trả 2xx.
Luồng: phiếu thử → người duyệt thật của phiếu đăng nhập → Phiếu chờ duyệt lọc đúng loại (tìm theo mã nếu không nằm trang 1) → "Xem & duyệt" → màn gốc → nút duyệt (footer, hoặc icon trên dòng với màn danh sách, hoặc popup 2 lớp xác nhận) → kiểm DB.

**Kết luận về Trung tâm phê duyệt: không phát hiện lỗi của chính TT phê duyệt ở 71 loại đã duyệt thật** — không có ca phiếu "không rời inbox", cấp sai hay UI lệch DB. Các lỗi tìm được đều ở màn gốc / dữ liệu thử / seedTest (mục 3, 4).

## 2. Bảng từng loại

| Loại phiếu (doc_type) | Duyệt thật | Nút đã bấm | Kết quả duyệt / lý do | Ca nghịch (người lạ) |
|---|---|---|---|---|
| addition_accounting_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Lập phiếu kế toán" (lập chứng từ mới). | XANH |
| assign_business | BỎ QUA |  | [DỮ LIỆU THỬ] Màn "Lưu và duyệt" là form sửa: phiếu thử thiếu Từ ngày / Đến ngày / Giờ xuất phát / Địa điểm… (bắt buộc). | XANH |
| assign_business_result | BỎ QUA |  | [DỮ LIỆU THỬ] Như assign_job: phiếu thử không có nhân viên thực hiện nên "Duyệt kết quả" bị chặn ở FE. | XANH |
| assign_job | BỎ QUA |  | [DỮ LIỆU THỬ] Phiếu giao việc thử không có Nhân viên thực hiện / công khoán: màn chặn "Tổng tỉ lệ hưởng công khoán phải bằng 100%" (bấm Duyệt không gọi API). | XANH |
| assign_job_result | BỎ QUA |  | [DỮ LIỆU THỬ] Như assign_job: phiếu thử không có nhân viên thực hiện nên "Duyệt kết quả" bị chặn ở FE. | XANH |
| assign_other_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu giao việc" (lập phiếu mới). | XANH |
| assign_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Lập phiếu công tác" (tạo phiếu mới, phải nhập hàng loạt trường), không có nút Duyệt. | XANH |
| attendance | XANH | TP duyệt | phiếu thử không nằm ở trang 1 (tổng 18 phiếu) → tìm bằng ô từ khoá; phiếu vẫn còn trong inbox với cấp "Chờ NSHC duyệt" | XANH |
| attendances_extend_request | XANH | icon Duyệt (i.fa-calendar-plus) | duyệt bằng hành động trên dòng danh sách; phiếu đã rời inbox của người duyệt | XANH |
| bill_adjust_dept_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu kế toán" (lập chứng từ mới). | XANH |
| bill_income | BỎ QUA |  | [DỮ LIỆU THỬ] Màn chặn: "Chưa chọn phiếu đề nghị thu", chưa có dòng phân bổ (Số tài khoản có, Số tiền duyệt/thực thu bắt buộc) — phiếu thu thử không có chi tiết. | XANH |
| bill_income_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu thu" (lập chứng từ mới). | XANH |
| bill_payment | BỎ QUA |  | [DỮ LIỆU THỬ] Popup Duyệt phiếu chi chặn "Phiếu chi phải có ít nhất 1 dòng chi tiết" — phiếu chi thử không có dòng chi tiết. | XANH |
| bill_payment_request | XANH | Duyệt | phiếu thử không nằm ở trang 1 (tổng 120 phiếu) → tìm bằng ô từ khoá; phiếu vẫn còn trong inbox với cấp "Chờ kế toán công nợ duyệt" | XANH |
| bonus_distribution | XANH | DUYỆT | phiếu đã rời inbox của người duyệt | XANH |
| bonus_end_year_settlement | XANH | Duyệt | phiếu đã rời inbox của người duyệt | XANH |
| borrow_export_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu xuất hàng mượn" (lập chứng từ mới có dòng hàng). | XANH |
| borrow_extend_request | BỎ QUA |  | [ĐIỀU KIỆN NGHIỆP VỤ] API approve trả 423 "Phòng ban bạn quản lý có nhân viên hàng giữ quá hạn, hàng mượn quá hạn…" — chốt chặn nghiệp vụ ĐÚNG của màn (người duyệt này có hàng quá hạn trong dữ liệu local), không phải lỗi duyệt. | XANH |
| borrow_sell_request | XANH | TP duyệt | phiếu vẫn còn trong inbox với cấp "Chờ kế toán kho" | XANH |
| business_target_department | XANH | Duyệt | phiếu đã rời inbox của người duyệt | XANH |
| business_target_employee | XANH | Duyệt | phiếu đã rời inbox của người duyệt | XANH |
| business_trip_assign | XANH | DUYỆT | phiếu thử không nằm ở trang 1 (tổng 219 phiếu) → tìm bằng ô từ khoá; phiếu đã rời inbox của người duyệt | XANH |
| business_trip_employee_request | XANH | icon Duyệt (i.fa-calendar-plus) | duyệt bằng hành động trên dòng danh sách; phiếu đã rời inbox của người duyệt | XANH |
| buy_service_accounting_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Hạch toán" → mở form lập phiếu hạch toán. | XANH |
| buy_service_request | XANH | Trưởng phòng duyệt | phiếu đã rời inbox của người duyệt | XANH |
| capacity_evaluate | BỎ QUA |  | Dữ liệu thử local không dựng được: no_pending_item (seedTest() không tạo được phiếu chờ có người duyệt đang làm việc) | - |
| capacity_evaluate_planning | XANH | Duyệt | phiếu vẫn còn trong inbox với cấp "Chờ BGĐ duyệt" | XANH |
| contract | BỎ QUA |  | Dữ liệu thử local không dựng được: no_active_approver_in_company (seedTest() không tạo được phiếu chờ có người duyệt đang làm việc) | - |
| course | BỎ QUA |  | [DỮ LIỆU THỬ] API duyệt trả 422 "object_training bắt buộc" (Đối tượng đào tạo): khoá học thử thiếu trường này. | XANH |
| course_register | XANH | Duyệt | phiếu thử không nằm ở trang 1 (tổng 50 phiếu) → tìm bằng ô từ khoá; phiếu đã rời inbox của người duyệt | ĐỎ: (2) màn gốc hiện nút duyệt "Duyệt" cho người không có quyền duyệt (mở thẳng URL) |
| course_request | BỎ QUA |  | [DỮ LIỆU THỬ] API duyệt trả 422 "object_training bắt buộc" (Đối tượng đào tạo): đề nghị mở khoá thử thiếu trường này. | XANH |
| course_student_attendance | BỎ QUA |  | [FORM RIÊNG] Duyệt điểm danh là bấm vào từng ô "X (Chờ duyệt)" trong bảng điểm danh học viên của khoá học rồi chọn Duyệt / Không duyệt trong popup — thao tác trên lưới điểm danh, chưa tự động hoá được bằng luồng chung (cần spec riêng theo b | XANH |
| decision_accept_personnel | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_appoint_personnel | XANH | Chuyển ban giám đốc duyệt | phiếu đã rời inbox của người duyệt | - |
| decision_assign_training | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_department_change | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_department_dissolution | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_department_establishment | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_employee_discipline | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_increase_seniority | XANH | Chuyển ban giám đốc duyệt | phiếu đã rời inbox của người duyệt | - |
| decision_manpower_planning | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_regulation_general | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_regulation_salary | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_renew_labor_contract | ĐỎ |  | MÀN GỐC LỖI khi mở (BE trả 5xx nên không dựng được nút Duyệt): 500 GET http://127.0.0.1:8000/api/v1/decision/renew-labor-contract/39 | XANH |
| decision_retirement | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_reward | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_salary_bonus | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_salary_change | XANH | Chuyển ban giám đốc duyệt | phiếu đã rời inbox của người duyệt | - |
| decision_suspend_labor_contract | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_termination_labor_contract | XANH | Chuyển ban giám đốc duyệt | phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| decision_transfer_personnel | XANH | Chuyển ban giám đốc duyệt | phiếu đã rời inbox của người duyệt | - |
| delivery_contract | XANH | Duyệt | phiếu đã rời inbox của người duyệt | XANH |
| delivery_cost_summary | BỎ QUA |  | [DỮ LIỆU THỬ] API approve trả 422 "vehicles bắt buộc": tổng hợp chi phí thử không có xe. | XANH |
| delivery_request | BỎ QUA |  | [DỮ LIỆU THỬ] API approve trả 422 "Phiếu yêu cầu xuất hàng không hợp lệ" (objectable_id): phiếu đề nghị giao hàng thử không gắn phiếu yêu cầu xuất hàng thật. | XANH |
| delivery_trip | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Hạch toán chuyến xe" → mở form lập phiếu hạch toán (nhập xe, chi phí). | XANH |
| discount_type | XANH | Duyệt | duyệt bằng hành động trên dòng danh sách; phiếu đã rời inbox của người duyệt | - |
| division_market_department | XANH | Duyệt | phiếu đã rời inbox của người duyệt | XANH |
| division_market_employee | XANH | Duyệt | phiếu đã rời inbox của người duyệt | XANH |
| employee_info_update_request | BỎ QUA |  | [DỮ LIỆU THỬ] POST human/employee-update-requests/{id} trả 422 (Ảnh đại diện, Họ và đệm… bắt buộc): phiếu thử không có đủ hồ sơ. | XANH |
| exc_shortage_warehouse_import | BỎ QUA |  | [DỮ LIỆU THỬ] Form báo hàng thừa/thiếu thiếu "Phiếu nhập kho" (bắt buộc) và không có dòng hàng nên "Xử lý" không gọi API. | XANH |
| extend_end_soon_request | XANH | Duyệt | phiếu thử không nằm ở trang 1 (tổng 96 phiếu) → tìm bằng ô từ khoá; phiếu đã rời inbox của người duyệt | XANH |
| handover | BỎ QUA |  | Dữ liệu thử local không dựng được: no_active_approver_in_company (seedTest() không tạo được phiếu chờ có người duyệt đang làm việc) | - |
| handover_item | XANH | Tiếp nhận tất cả (1) | phiếu đã rời inbox của người duyệt | XANH |
| handover_record | XANH | Duyệt | phiếu đã rời inbox của người duyệt | ĐỎ: (2) màn gốc hiện nút duyệt "Duyệt" cho người không có quyền duyệt (mở thẳng URL) |
| insurance_register | XANH | Duyệt | phiếu đã rời inbox của người duyệt | XANH |
| inventory_audit_report | BỎ QUA |  | [DỮ LIỆU THỬ] Màn chặn 422 "Chưa có hàng thừa, thiếu. Vui lòng bấm Lấy dữ liệu" — phiếu thử không có chi tiết kiểm kê. | XANH |
| issue | BỎ QUA |  | [DỮ LIỆU THỬ] Duyệt = đổi trạng thái trong popup "Chi tiết Vấn đề" (form có nhiều trường bắt buộc: Loại vấn đề, Mức độ ưu tiên, Mức độ ảnh hưởng, Nguồn phát hiện…); phiếu thử để trống các trường đó. | XANH |
| job_assignment_note | XANH | DUYỆT | phiếu thử không nằm ở trang 1 (tổng 491 phiếu) → tìm bằng ô từ khoá; phiếu đã rời inbox của người duyệt | XANH |
| job_request | XANH | Duyệt | phiếu đã rời inbox của người duyệt | - |
| join_export_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo đề nghị xuất kho" (lập chứng từ mới); phiếu thử không có hàng hoá. | XANH |
| late_early_out | XANH | Duyệt | phiếu thử không nằm ở trang 1 (tổng 24 phiếu) → tìm bằng ô từ khoá; phiếu đã rời inbox của người duyệt | XANH |
| late_early_out_change_end_request | XANH | icon Duyệt (i.fa-calendar-plus) | duyệt bằng hành động trên dòng danh sách; phiếu đã rời inbox của người duyệt | XANH |
| market_plan_employee | XANH | Duyệt | phiếu vẫn còn trong inbox với cấp "TP đã duyệt" | XANH |
| meeting_room_booking | ĐỎ | Duyệt | bấm duyệt nhưng KHÔNG có lời gọi ghi nào tới API (nút không làm gì / thiếu trường bắt buộc: không có toast); (a) bảng gom KHÔNG đổi sau khi duyệt: vẫn state=1 step=1 "Chờ duyệt"; (b) bảng gốc không đổi cột nào (ngoài updated_at/by) | XANH |
| meeting_room_service_request | BỎ QUA |  | Dữ liệu thử local không dựng được: no_active_approver_in_company (seedTest() không tạo được phiếu chờ có người duyệt đang làm việc) | - |
| other_delivery_trip | XANH | Duyệt | phiếu thử không nằm ở trang 1 (tổng 11 phiếu) → tìm bằng ô từ khoá; phiếu vẫn còn trong inbox với cấp "Chờ hạch toán" | XANH |
| overtime_assignment | XANH | Duyệt | phiếu đã rời inbox của người duyệt | - |
| overtime_requirement | XANH | Duyệt | phiếu đã rời inbox của người duyệt | - |
| payment_business_request | ĐỎ |  | màn gốc không có nút Duyệt nào cho người duyệt này | XANH |
| payment_profile | BỎ QUA |  | [DỮ LIỆU THỬ] POST …/payment-profile/{id}/approve trả 400 (thiếu "Thời gian đi" và "Nhân viên") — phiếu thử không có dữ liệu này. | ĐỎ: HTTP 5xx khi người lạ mở màn: 500 GET http://127.0.0.1:8000/api/v1/assign/payment-business-request/978 |
| position_inventory_result | XANH | Duyệt kết quả | phiếu đã rời inbox của người duyệt | XANH |
| prepick_cancel_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu hủy hàng giữ" (lập chứng từ mới có dòng hàng). | XANH |
| prepick_extend_request | BỎ QUA |  | [DỮ LIỆU THỬ] Màn chặn "Phải giữ lại ít nhất 1 hàng hóa cần gia hạn" — phiếu thử không có hàng hoá. | XANH |
| prepick_transfer_request | XANH | BGĐ duyệt | phiếu vẫn còn trong inbox với cấp "Chờ KT duyệt" | XANH |
| price_asking_group | XANH | Duyệt | phiếu đã rời inbox của người duyệt | - |
| price_asking_request | XANH | Duyệt | phiếu đã rời inbox của người duyệt | - |
| price_calculate_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tính giá" → màn tính giá nhập hàng hoá / chi phí rồi mới gửi kết quả. | XANH |
| product_export_request | XANH | BGĐ duyệt | phiếu thử không nằm ở trang 1 (tổng 19 phiếu) → tìm bằng ô từ khoá; phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| product_import_direct_transfer | BỎ QUA |  | [DỮ LIỆU THỬ] API approve trả 422 "Phiếu không có dòng hàng hóa nào để chuyển" — phiếu thử không có dòng hàng. | XANH |
| product_import_request | XANH | Trưởng phòng duyệt | phiếu thử không nằm ở trang 1 (tổng 36 phiếu) → tìm bằng ô từ khoá; phiếu vẫn còn trong inbox với cấp "Chờ duyệt" | XANH |
| product_prepick_request | XANH | TP duyệt | phiếu vẫn còn trong inbox với cấp "Chờ KT duyệt" | XANH |
| product_price_approval | XANH | Duyệt | bảng gốc: dòng phiếu đã chuyển sang bảng khác / bị tiêu thụ sau duyệt (state bảng gom = 5); phiếu đã rời inbox của người duyệt | - |
| product_transfer_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Người xử lý chỉ có "Tổng hợp" / "Không duyệt"; luồng thật là tổng hợp rồi lập phiếu chuyển kho — không có nút Duyệt. | XANH |
| prospective_project_extension | XANH | Duyệt | duyệt bằng hành động trên dòng danh sách; phiếu đã rời inbox của người duyệt | XANH |
| quotation | XANH | BGĐ duyệt | phiếu thử không nằm ở trang 1 (tổng 16 phiếu) → tìm bằng ô từ khoá; phiếu đã rời inbox của người duyệt | - |
| request_solution | BỎ QUA |  | [DỮ LIỆU THỬ] Popup "Tiếp nhận yêu cầu làm GP" bắt buộc Ngày dự kiến xong GP, nhưng ô ngày bị giới hạn bởi "Ngày KH cần giải pháp" (phiếu thử để trống) nên không chọn được ngày hợp lệ → API receive trả 422 close_solution_date. | XANH |
| request_update_timesheet | XANH | Duyệt | phiếu thử không nằm ở trang 1 (tổng 12 phiếu) → tìm bằng ô từ khoá; phiếu đã rời inbox của người duyệt | XANH |
| sale_plan_employee | XANH | Duyệt | phiếu vẫn còn trong inbox với cấp "TP đã duyệt" | XANH |
| self_inventory | XANH | Duyệt kết quả | phiếu đã rời inbox của người duyệt | XANH |
| self_notification | BỎ QUA |  | Dữ liệu thử local không dựng được: no_active_approver_in_company (seedTest() không tạo được phiếu chờ có người duyệt đang làm việc) | - |
| service_accounting_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Hạch toán dịch vụ" → mở form "Lập phiếu hạch toán dịch vụ" (chọn phiếu yêu cầu, tài khoản, chi phí) rồi mới Lưu và duyệt. | XANH |
| settlement_contract | XANH | TP Duyệt | phiếu vẫn còn trong inbox với cấp "Chờ KT duyệt" | XANH |
| solution | BỎ QUA |  | [DỮ LIỆU THỬ] Màn duyệt là form "Lưu và duyệt": phiếu thử thiếu Ngày cần xong GP, Ứng dụng, Nhóm ngành, Nhóm giải pháp… (bắt buộc). | XANH |
| solution_adjustment_request | BỎ QUA |  | [DỮ LIỆU THỬ] seedTest() chọn giải pháp MỒ CÔI (dự án tiền khả thi đã xoá): sau đồng bộ phiếu thử không còn ở trạng thái chờ duyệt, màn gốc báo 404. Cần seedTest() chọn giải pháp có dự án tồn tại. | - |
| solution_module_review_profile | XANH | Duyệt | duyệt bằng hành động trên dòng danh sách; phiếu đã rời inbox của người duyệt | XANH |
| solution_review_profile | XANH | Duyệt | duyệt bằng hành động trên dòng danh sách; phiếu đã rời inbox của người duyệt | XANH |
| split_export_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo đề nghị xuất kho" (lập chứng từ mới); phiếu thử không có hàng hoá. | XANH |
| summary_quotation | XANH | Duyệt | phiếu đã rời inbox của người duyệt | XANH |
| task_extension_request | XANH | Đồng ý | phiếu đã rời inbox của người duyệt | - |
| task_result_approval | XANH | Duyệt kết quả | phiếu đã rời inbox của người duyệt | XANH |
| task_start_approval | XANH | Duyệt triển khai | phiếu đã rời inbox của người duyệt | XANH |
| timekeeping_device | XANH | Duyệt | duyệt bằng hành động trên dòng danh sách; phiếu đã rời inbox của người duyệt | XANH |
| training_planning | XANH | Duyệt | phiếu đã rời inbox của người duyệt | ĐỎ: (2) màn gốc hiện nút duyệt "Duyệt" cho người không có quyền duyệt (mở thẳng URL) |
| training_request | XANH | Trưởng phòng duyệt | phiếu vẫn còn trong inbox với cấp "Chờ quản lý đào tạo duyệt" | XANH |
| trouble_shooting_report | ĐỎ |  | MÀN GỐC LỖI khi mở (BE trả 5xx nên không dựng được nút Duyệt): 500 GET http://127.0.0.1:8000/api/v1/decision/trouble-shooting-report/278 | ĐỎ: HTTP 5xx khi người lạ mở màn: 500 GET http://127.0.0.1:8000/api/v1/decision/trouble-shooting-report/278 |
| warehouse_export | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu xuất hàng" (lập chứng từ mới có dòng hàng / serial). | XANH |
| warehouse_export_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu xuất kho" (lập chứng từ mới có dòng hàng). | XANH |
| warehouse_import | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu nhập hàng" (lập chứng từ mới có dòng hàng). | XANH |
| warehouse_import_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu nhập kho" (lập chứng từ mới có dòng hàng); phiếu thử không có dòng hàng. | XANH |
| warehouse_inventory_import | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu nhập hàng" (lập chứng từ mới có dòng hàng). | XANH |
| warehouse_transfer | BỎ QUA |  | [DỮ LIỆU THỬ] POST approve trả 400 "No query results for model WarehouseExport": phiếu chuyển kho thử không gắn phiếu xuất kho thật. | XANH |
| warranty_repair_handle_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu cung cấp thông tin" (lập phiếu mới). | XANH |
| warranty_repair_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Tạo phiếu xử lý yêu cầu" (lập phiếu mới) hoặc "Chuyển phòng tiếp nhận"; không có nút Duyệt một chạm. | XANH |
| wr_accounting_service_request | BỎ QUA |  | [LẬP CHỨNG TỪ KẾ TIẾP] Nút xử lý là "Hạch toán chi phí" → mở form lập phiếu hạch toán chi phí. | XANH |
| wr_import_result | BỎ QUA |  | [DỮ LIỆU THỬ] API approve trả 422 (customer_id, thời gian dự kiến… bắt buộc): kết quả nhập thử không đủ thông tin. | XANH |
| wr_service_annex | BỎ QUA |  | Dữ liệu thử local không dựng được: no_pending_item (seedTest() không tạo được phiếu chờ có người duyệt đang làm việc) | - |
| wr_service_contract | XANH | Duyệt hiệu lực | phiếu đã rời inbox của người duyệt | XANH |
| wr_service_quotation | BỎ QUA |  | Dữ liệu thử local không dựng được: no_active_approver_in_company (seedTest() không tạo được phiếu chờ có người duyệt đang làm việc) | - |

Ký hiệu cột "Duyệt thật": XANH · ĐỎ · BỎ QUA (lý do ở cột kế bên, có nhãn). Cột "Kết quả duyệt": với XANH là ghi chú (phiếu rời inbox / còn ở cấp kế). Ca nghịch "-" = không có phiếu thử để chạy (loại bị bỏ qua / không dựng được).

Nhãn lý do bỏ qua:
- **[DỮ LIỆU THỬ]** `seedTest()` chỉ dựng phiếu "mỏng" (không dòng hàng, thiếu trường bắt buộc…) nên CHÍNH màn gốc chặn duyệt bằng validate (hành vi đúng của màn, không phải lỗi duyệt). Muốn kiểm phải bổ sung dữ liệu thử ở `seedTest()`.
- **[LẬP CHỨNG TỪ KẾ TIẾP]** "Duyệt" của loại này = mở form lập chứng từ khác (nhập kho, xuất kho, hạch toán, phiếu công tác…) do người duyệt nhập hàng hoá / kho / ngày giờ — không có nút Duyệt một chạm; cần spec riêng theo từng form.
- **[FORM RIÊNG]** `course_student_attendance`: duyệt từng ô "X (Chờ duyệt)" trong lưới điểm danh học viên.
- **[ĐIỀU KIỆN NGHIỆP VỤ]** `borrow_extend_request`: API trả 423 "Phòng ban bạn quản lý có nhân viên hàng giữ quá hạn…" — chốt chặn đúng của màn.
- **Dữ liệu thử local không dựng được** (7 loại: `contract`, `handover`, `wr_service_annex`, `wr_service_quotation`, `self_notification`, `meeting_room_service_request`, `capacity_evaluate`): sau seed không có phiếu chờ nào có NGƯỜI DUYỆT đang làm việc đúng công ty (hoặc phiếu thử bị đồng bộ thành "không còn chờ").

## 3. Lỗi tìm được (KHÔNG sửa code, chuyển người phụ trách)

### 3.1 Lỗ hổng phân quyền BE — người KHÔNG phải người duyệt vẫn duyệt được (đã tái hiện bằng UI + DB)
Cách tái hiện: `node bin/debug-stranger.js <doc_type>` (đăng nhập 1 nhân viên không là người duyệt của bất kỳ phiếu nào — `pick-non-approver.php`, mở thẳng URL màn gốc, bấm Duyệt) hoặc spec `negative.spec.ts`.
| Loại | Endpoint | Bằng chứng |
|---|---|---|
| `handover_record` (Biên bản bàn giao) | `PUT customer-care/handover-records/{id}/approve` | người lạ (employee 24) bấm Duyệt → 200 "Duyệt thành công.", bảng gom `state=2 resolved_by=24` (phiếu 99) |
| `course_register` (Đăng ký khoá học) | `PUT training/course-registers/{id}/toggle-approve` | 200, `status 5 → 10`, `resolved_by=24` (phiếu 15652) |
| `training_planning` (Kế hoạch đào tạo) | `PUT training/training-planning/{id}/toggle-approve` | 200, `resolved_by=24` (phiếu 296) |
FE còn hiện nút Duyệt cho người lạ vì màn gốc không dựa vào `approvers()` của TT phê duyệt; điều kiện thật phải kiểm ở BE (khớp ghi chú sẵn có "endpoint duyệt không kiểm quyền" trong plan.md). 102/107 loại còn lại: người lạ không thấy phiếu trong inbox + màn gốc không có nút/hành động duyệt + bảng gom không đổi.

### 3.2 Màn gốc lỗi HTTP 500 khi mở phiếu (người duyệt không thấy nút Duyệt)
| Loại | URL mở (từ "Xem & duyệt") | Lỗi (laravel.log) | Ghi chú |
|---|---|---|---|
| `decision_renew_labor_contract` | `/decision/renew-labor-contract/39/approve` → `GET decision/renew-labor-contract/39` 500 | `Attempt to read property "competencies" on null` — `Modules/Decision/Transformers/RenewLaborContract/DetailRenewLaborContractResource.php:95` | `$this->rank` null (phiếu thử không có ngạch/bậc). Có thể xảy ra với dữ liệu thật thiếu rank |
| `trouble_shooting_report` | `/decision/category/trouble-shooting-reports/278/approve` → `GET decision/trouble-shooting-report/278` 500 | `Undefined variable $violators` — `Modules/Decision/Http/Controllers/V1/TroubleShootingReportController.php:125` | `$violators` chỉ khai trong vòng lặp thành viên có nhóm "Người vi phạm"; phiếu không có thành viên → biến chưa khai. Lỗi code thật |
| `capacity_evaluate` | `/training/capacity-evaluate/446/approve` → `GET training/capacity-evaluate/446` 500 | `Attempt to read property "from_date" on null` — `Modules/Training/Transformers/CapacityEvaluate/DetailCapacityEvaluateResource.php:22` | quan hệ null (phiếu thử). Kết quả JSON loại này bị ghi đè "không dựng được phiếu" ở lần chạy cuối vì sau đó phiếu thử bị đồng bộ thành không còn chờ |
| `payment_business_request` | `/assign/payment_business_request/978/show` — toast "Lỗi máy chủ", chỉ còn nút Hủy | `Attempt to read property "info" on null` — `Modules/Assign/Transformers/PaymentBusinessRequest/PaymentBusinessRequestTransformer.php:102` | người duyệt (cấp TP duyệt) không có nút Duyệt. `payment_profile` mở màn "đề nghị thanh toán" liên quan cũng gọi `GET assign/payment-business-request/978` → 500 |

### 3.3 Chưa xác minh được
- `meeting_room_booking`: bấm icon ✓ "Duyệt" trên dòng phiếu trong `/meeting/bookings` (đúng dòng `TEST-AC-62E4104BDC`) KHÔNG phát sinh lời gọi API nào, không có popup/ toast, phiếu vẫn "Chờ duyệt". Nghi: nút bị phần tử khác che / cần thao tác khác; chưa xác định là lỗi FE hay do cách bấm của spec. Cần người điều phối bấm thử tay (tài khoản `thuydt.qttt@tanphat.com` / `Test@123`).

## 4. Việc dành cho người điều phối / người phụ trách seedTest
1. **Phân hệ bị tắt ở "Cài đặt phân hệ"** (Tài chính, Kho… nhiều loại): phiếu vẫn nằm trong Phiếu chờ duyệt nhưng bấm vào ra `/feature-unavailable?reason=hidden` (đã có trong "Việc còn lại" của plan.md). Để kiểm các loại này tôi thêm TẠM các tài khoản thử vào bảng `menu_full_access_employees` (spec tự thêm lúc bắt đầu và gỡ khi xong; đã chạy `full-access.php restore`, bảng về 0 dòng). Muốn tắt: `NO_FULL_ACCESS=1`.
2. **Nâng `seedTest()` để duyệt được thật**: thêm ≥ 1 dòng hàng cho phiếu kho/tài chính (22 loại [DỮ LIỆU THỬ]), điền trường bắt buộc (nhân viên thực hiện + công khoán của giao việc, ngày giờ phiếu công tác, đối tượng đào tạo, ảnh/họ tên hồ sơ…), `solution_adjustment_request` đừng chọn giải pháp mồ côi (dự án đã xoá → màn 404 + phiếu rời inbox ngay), `request_solution` điền "Ngày KH cần giải pháp" (nếu không popup tiếp nhận không cho chọn ngày).
3. 7 loại seedTest không dựng được phiếu chờ có người duyệt đang làm việc đúng công ty (xem mục 2). Cần xem lại `approvers()` hoặc dữ liệu seed.
4. 22 loại "duyệt = lập chứng từ kế tiếp": nếu muốn kiểm tự động cần spec riêng cho từng form (nhập hàng / kho / hạch toán). Chưa làm.
5. Điều kiện hiển thị menu không dùng chung với `approvers()`: nên cho Trung tâm phê duyệt biết phân hệ nào đang tắt để ẩn phiếu hoặc ghi chú.

## 5. Spec, công cụ và cách chạy
Thư mục `HRM/e2e/` (Node 20, `playwright test … --project=chromium --no-deps`, LUÔN qua `python3 bin/locked.py …`):
- `tests/approval-center/approve/approve.spec.ts` — duyệt thật, **1 test/loại** sinh từ registry (không có 128 file giống nhau).
- `tests/approval-center/approve/config.ts` — **bảng cấu hình theo loại**: `skip` (lý do), `button`, `rowKeys`/`rowIcon` (màn danh sách), `inModal`, `pick`, `note`…; hiện có 100 dòng.
- `tests/approval-center/approve/negative.spec.ts` — ca nghịch: người lạ không thấy phiếu (API inbox), mở thẳng URL màn gốc không có nút/hành động Duyệt, bảng gom không bị đổi.
- `utils/approve.ts` (watch lỗi/ghi, tìm nút duyệt, popup xác nhận nhiều lớp, hành động trên dòng danh sách, đăng nhập nhanh), `utils/php/pick-for-manifest.php` (chọn phiếu thử + người duyệt thật, đặt mật khẩu `Test@123`), `utils/php/item-state.php` (bảng gom + dòng gốc + `describe()`), `utils/php/full-access.php` (thêm/gỡ xem đủ menu tạm).
- `bin/approve-report.py [--md]` tổng hợp `approve-results/*.json` (mỗi loại 1 file, kèm nút đã bấm, lời gọi ghi, trạng thái trước/sau, cột bảng gốc đổi); `bin/debug-page.js`, `bin/debug-click.js`, `bin/debug-stranger.js` để soi từng loại; ảnh ở `e2e/screenshots/approve-<doc_type>.png`.
Chạy: `ONLY=a,b python3 bin/locked.py npx playwright test tests/approval-center/approve/approve.spec.ts --project=chromium --no-deps` (hoặc `negative.spec.ts`); `RESEED=1` dọn + tạo lại phiếu thử; `CLEAN=1` dọn khi xong. Mỗi loại ~40–60 giây (API 1 worker) → 128 loại ≈ 1,5–2 giờ; chạy theo lô ~30 loại.
Phiếu thử: manifest `wave3-e2e-approve.json` (`approval-center:seed-test --count=2 --manifest=wave3-e2e-approve.json`). **ĐỂ LẠI** (nhiều phiếu đã bị duyệt thật) cho người điều phối xem; dọn bằng `php artisan approval-center:clean-test --manifest=wave3-e2e-approve.json`.

## 6. Tác động lên DB local (đã ghi)
- Đặt mật khẩu `Test@123` cho ~25 người duyệt thật + 1 nhân viên "người lạ" (`tuannd.kd1@tanphat.com`); KHÔNG đụng namdangit/id 13.
- Duyệt thật các phiếu thử (TEST-APPROVAL-CENTER…) ⇒ trạng thái bảng gốc + bảng gom + lịch sử + thông báo của phiếu thử đã đổi; 3 phiếu bị người lạ duyệt (mục 3.1).
- `menu_full_access_employees`: thêm tạm rồi gỡ (0 dòng).
