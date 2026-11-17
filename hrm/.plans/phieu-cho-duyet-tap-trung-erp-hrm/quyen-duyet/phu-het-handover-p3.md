# Phủ hết — Biên bản bàn giao sơ bộ + Định mức thưởng P3 (Payroll) — @cuong61n

Ngày 17/11/2026. Kết luận: **DỪNG, KHÔNG đăng ký cả 2 loại** (theo chỉ dẫn "không gate nào thì đừng đoán, báo lại"). Không tạo Definition / không sửa model / không chạy seed / không đổi DB.
Quyết định user: làm đúng logic hiện tại, không thêm quyền, không siết BE.

## 1. Biên bản bàn giao sơ bộ (`handover_records`) — KHÔNG CÓ GATE

Màn FE `/customer-care/handover-records` (route 481-495 `Modules/CustomerCare/Routes/api.php`).

| Lớp | Bằng chứng | Kết quả |
|---|---|---|
| Route | `Routes/api.php:478-496`: comment "KHONG checkPermission: ERP man nay khong co quyen, user chot giu y ERP (04/11/2026)"; nhóm chỉ có `auth:api` (dòng 36) | không quyền |
| Controller `approve` | `Http/Controllers/V1/HandoverRecordController.php:191-210`: chỉ kiểm `status` ∈ {3,4} và lý do khi từ chối | không kiểm người |
| Service `approve` | `Services/HandoverRecordService.php:485-515`: docblock "Không kiểm người duyệt"; chỉ `canApprove()` = `status == CHO_DUYET` (dòng 195-198); khoá dòng + 409 nếu đã đổi | không kiểm người |
| Cờ nút `is_can_approve` | `HandoverRecordService.php:179-193` (`actionFlags`): chỉ theo trạng thái, danh sách và chi tiết cùng cờ | mọi người thấy nút khi Chờ duyệt |
| API danh sách | `filteredQuery` dòng 98-117: chỉ lọc `keyword`/`status`, "ERP không bó phạm vi (ai cũng thấy mọi biên bản)" | không lọc người / công ty / phòng |
| FE nút | `pages/customer-care/handover-records/components/HandoverRecordForm.vue:194,205,248` + `index.vue:353`: `v-if="form.is_can_approve"`, không đọc quyền / `approver_id` / người tạo | |
| Menu | `components/subsystem-menu/customer-care.js:146` và `:181` ("Phiếu CSKH"): không `codes`, không `isShow`, không `groups`; chú thích "ERP không có quyền → không isShow"; `middleware/checkPermission.js` không chặn thêm | ai đăng nhập cũng vào |
| `approver_id` | bắt buộc chọn ở form Gửi duyệt (FE `HandoverRecordForm.vue:16-27,626`; `StoreService:52,99`); chỉ dùng để **gửi thông báo chuông** (`HandoverRecordNotifier::notifyWaitingApproval`) và hiển thị cột "Người duyệt" — KHÔNG phải điều kiện bấm Duyệt | không phải gate |
| Người tạo | không có chặn tự duyệt | tự duyệt được |

Cấp: 1 cấp (status 2 "Chờ duyệt" → 3 Đã duyệt / 4 Từ chối; từ chối sửa lại gửi lại được). Công ty biên bản = công ty người tạo (không có cột company).
Dữ liệu local: `handover_records` = **0 dòng** (không có phiếu thử/thật).

Đề xuất cho người điều phối / user chọn 1 (đều là suy diễn ngoài code, nên chưa làm):
- A. Người duyệt = `approver_id` đích danh (đúng ý nghiệp vụ + thông báo, nhưng BE không ép: người khác vẫn duyệt được qua màn).
- B. Người duyệt = mọi nhân viên đang hoạt động (đúng hành vi thật, inbox sẽ rất nhiễu).
- C. Chờ vá BE (thêm kiểm `approver_id` ở `HandoverRecordService::approve`) rồi đăng ký theo A.
Lưu ý: A/B đều làm `approvers()` + `truth()` lệch hoặc quá rộng so với code gốc nên `approval-inbox:verify` chỉ cho A nếu `truth()` cũng mô phỏng cùng điều kiện; cần user chốt.

## 2. Định mức thưởng P3 (`p3_salaries`, "Thu nhập P3") — KHÔNG CÓ GATE, CHƯA BAO GIỜ Ở TRẠNG THÁI CHỜ TỪ UI

Trạng thái (`Entities/P3Salary.php:20-36`): 0 Đang tạo · 1 Chờ duyệt · 2 Đã duyệt · 3 Từ chối. Bảng không có cột người duyệt (cột: id, table_name, apply_date, status, company_id, department_id, created_by, part_id, updated_by, timestamps).

| Lớp | Bằng chứng | Kết quả |
|---|---|---|
| Route | `Modules/Payroll/Routes/api.php:152-159`: 6 route p3_salaries không `checkPermission` | không quyền |
| Controller / Service | `P3SalaryController.php:41-50,87-100` `approve()` chỉ là DANH SÁCH (mọi bản ghi status != 0, mọi công ty, không lọc quyền); `cancel_approve` và `store` đều gọi `P3SalaryService::save` ghi `status` do client gửi, không kiểm trạng thái hiện tại, người dùng, quyền (`P3SalaryRequest` không có rule `status`) | không gate; chuyển trạng thái chỉ qua API thô |
| FE nút Duyệt / Từ chối | `pages/payroll/salary-data/p3-salary/_id/approve.vue:11-23`: `v-if="p3SalaryData.status == 1"`; `approve.vue:~L52` "Huỷ duyệt" khi `status == 2`; không đọc quyền | chỉ theo trạng thái |
| Nút **Gửi duyệt** (nguồn duy nhất đưa phiếu vào trạng thái 1) | `_id/index.vue:17-19` bị **comment** (`<!-- ... Gửi duyệt ... -->`); modal `confirm-send-approve` + `submitApprove(1)` (dòng 128, 325) còn nối nhưng KHÔNG có nút nào mở; `components/modal/p3-salary-modal.vue:104-105` chỉ đặt `status = 0` | UI không đưa được lên 1 |
| Menu vào màn duyệt | `components/PayrollMenu.vue:128-130` mục "Duyệt đề xuất định mức thưởng P3" bị comment; `components/menu.js` chỉ có "Thu nhập P3" → `/payroll/salary-data/p3-salary` | màn `/approve` chỉ vào bằng gõ URL |
| Gate duy nhất còn lại | `menu.js:600-605` `groups: ['Định mức thưởng P3 (Hoa hồng/lương khoán)']` → `Topbar.showMenuChild` (dòng 148-158) / `PayrollMenu.hasGroup` (`utils/mixins/CheckPermission.js:26`): ẩn mục menu khi user không có quyền nào thuộc nhóm này. Nhóm = 4 quyền `payroll.dinh_muc_thuong_p3.{view,create,update,delete}` (bảng permissions id 46-49), **không có mã duyệt**. `middleware/checkPermission.js` chỉ xét `codes`/`isShow` nên **không chặn gõ URL** | chỉ là ẩn menu (UI), không chốt việc duyệt |
| Dữ liệu local | `p3_salaries`: 44 dòng, **toàn status 0**; **0 dòng status 1/2/3** | |

Kết luận: không có người duyệt (đích danh / mã quyền) nào được code dùng để chặn Duyệt / Từ chối; trạng thái chờ **không đặt được từ giao diện hiện tại** (chỉ đặt được bằng gọi thẳng `POST /api/v1/payroll/p3_salaries` với `status: 1`). Theo định nghĩa "màn cần duyệt" ở phụ lục, màn duyệt có tồn tại (route + nút Duyệt/Từ chối theo `status == 1`) nhưng không có bất kỳ luồng dẫn vào và không gate: dừng, chờ user quyết:
- A. Bỏ (luồng chết: nút Gửi duyệt + menu duyệt đều đã comment). Bằng chứng như trên.
- B. Đăng ký người duyệt = mọi người thấy menu "Thu nhập P3" (giữ ít ≥1 quyền thuộc nhóm P3, công ty đang làm) — là điều kiện hiển thị menu, KHÔNG ép ở BE; hiện chưa có phiếu nào để hiển thị. Nếu chọn B cần dev sau khi user chốt (và user quyết có mở lại nút Gửi duyệt hay không).

## 3. Việc đã làm / chưa làm
- Chỉ đọc code (BE + FE từng dòng) + query đếm dữ liệu local (`select` trên `p3_salaries`, `handover_records`). Không migrate, không ghi DB, không tạo file nào ngoài báo cáo này, không chạm Definition/Model/test.
- Không có chạy `seed-test`, nên không cần `clean-test --manifest=wave3-handover-p3.json`.
- Lỗi/lỗ hổng code gốc ghi nhận (không sửa): (1) BBBG sơ bộ không kiểm người duyệt, `approver_id` chỉ để thông báo; (2) P3 `store`/`cancel_approve` ghi `status` tuỳ ý từ client, không quyền, không kiểm trạng thái; (3) danh sách `p3_salaries/approve` không lọc công ty.

## 4. CẬP NHẬT 17/11/2026 — `handover_record` ĐÃ ĐĂNG KÝ (user chốt phương án A) — @cuong61n
- Người duyệt = `approver_id` đích danh (là employees.id: `HandoverRecordRequest` `exists:employees,id`, Notifier tra `employees`). BE không đổi.
- File: `Modules/ApprovalCenter/Definitions/CustomerCare/HandoverRecordDefinition.php`; trait `SyncsApprovalInbox` + `approvalInboxDocType()` thêm vào `Modules/CustomerCare/Entities/HandoverRecord/HandoverRecord.php`; test `tests/Feature/ApprovalCenter/CustomerCare/HandoverRecordDefinitionTest.php` (2 test xanh).
- Verify: 6 phiếu thử × 2000 mẫu = 77.940 cặp, 60 cặp duyệt thật, chênh lệch 0. Đột biến 4/5 bị bắt (đổi approver→created_by, bỏ so approver ở truth, 1 công ty, bỏ kiểm tồn tại); đột biến bỏ canApprove trong truth không bắt được vì phiếu đã duyệt không có trong bảng gom (tương đương).
- Chỗ ghi query builder: `HandoverRecordService::delete` (chỉ xoá Đang tạo / Từ chối, không phải phiếu chờ) nên không cần scheduleSync.
- Đã dọn: `approval-center:clean-test --manifest=wave3-handover.json`; `handover_records` = 0 dòng. Dòng bảng gom state=5 còn lại là lịch sử đóng.
- Chưa làm: gọi API thật + mở handler_path trên FE (người điều phối chạy e2e).
