# Tư vấn mở rộng tham số công cụ Agent — 11/11/2026

Rà API dùng chung của 7 đối tượng (hrm-api worktree, nhánh `gop_db-tpe-smart-agent`), so với công cụ Agent đang có,
đề xuất tham số / công cụ mới để trả lời được nhiều câu hơn. CHƯA sửa code.

Nguyên tắc chung khi mở rộng (xem `huong-dan-them-cong-cu.md`):
- Gọi lại **service có sẵn** (đã có phân quyền theo phạm vi), không viết query mới khi service đã lọc được.
- Tham số "của tôi" luôn `auth()->id()`; giá trị cố định khai `enum`.
- Ưu tiên **thêm tham số** vào công cụ có sẵn; chỉ tạo công cụ mới khi là đối tượng khác.
- Chi phí: mỗi công cụ mới ~300 token trong cache ≈ +0.05 ₫/câu (Haiku 5.5). 5 công cụ mới ≈ +0.25 ₫/câu.

---

## 1. Nhiệm vụ — `TaskService::index` (`Modules/Assign/Services/TaskService.php:28-148`)

Service đã có: company/department/part, keyword (tên, mã, khách hàng dự án), status, task_type, from/to (ngày cập nhật),
deadline_from/to, prospective_project_id, meeting_id, meeting_report_id, solution_id, solution_module_id, assignee_id,
created_by, priority (1 Bình thường/2 Cao/3 Khẩn cấp), approver_id, watching_id, overdue, tags. Phân quyền
`assign.danh_sach_task.view` nằm trong service.

| Công cụ | Đang có | Đề xuất thêm | Câu hỏi mở được |
|---|---|---|---|
| `viec_cua_toi` | vai_tro lam/theo_doi, overdue, hạn, status | `vai_tro`: **giao** (created_by), **duyet** (approver_id) · `uu_tien` (priority) · `tu_khoa` (keyword) | "Việc tôi giao còn ai chưa xong?", "Việc nào chờ tôi duyệt kết quả?", "Việc khẩn cấp của tôi", "Việc báo giá cầu nâng tới đâu?" |
| `viec_cua_nhan_vien` | nhan_vien_id, chi_qua_han, tu_ngay/den_ngay | `trang_thai`, `uu_tien`, `tu_khoa` | "Anh Nam còn việc nào đang làm?", "Việc khẩn cấp của chị Lan" |
| `viec_qua_han` | pham_vi, phong_ban_id, khoảng hạn | `uu_tien` | "Việc khẩn cấp quá hạn của phòng" |
| **MỚI** `thong_ke_viec` | — | Đếm theo trạng thái trong phạm vi (toi/phong/cong_ty), khoảng hạn — query `TaskService::index` + `groupBy status` | "Tháng này phòng tôi hoàn thành bao nhiêu việc, còn bao nhiêu đang làm?" (chưa có endpoint đếm theo trạng thái toàn phạm vi) |

## 2. Vấn đề — `IssueService::index` (`Modules/Assign/Services/IssueService.php:36-153`) — CHƯA có công cụ

Service có: company/department/part, keyword (tiêu đề, mã, người tạo), status (new/assigned/in_progress/resolved/closed/
reopened/completed/rejected), project_id, solution_id, module_id, assignee_id, handling_department_id/part_id,
priority (low/medium/high/critical), created_by (= creator_id), approver_id, watching_id, detected_by, issue_type,
from/to (ngày TẠO). Phân quyền `assign.danh_sach_issue.view` trong service. **Không có** lọc quá hạn / hạn xử lý.

| Đề xuất | Tham số | Câu hỏi mở được |
|---|---|---|
| **MỚI** `van_de` | `pham_vi` toi/phong/cong_ty · `vai_tro` (toi: xu_ly / tao / theo_doi / duyet / phat_hien) · `trang_thai` · `uu_tien` · `tu_khoa` · `qua_han` (tự lọc trong Agent: due_date + due_time < now, trạng thái chưa xong — giống `overdue_total` ở `IssueController:35-39`) · `tu_ngay/den_ngay` (ngày tạo) | "Vấn đề nào tôi đang xử lý?", "Phòng tôi còn bao nhiêu vấn đề khẩn cấp chưa đóng?", "Vấn đề quá hạn của dự án X" |
| **MỚI** `chi_tiet_van_de` (hoặc gộp vào `van_de` với `ma`) | `ma` (issue_code) | "Vấn đề VD-0012 tới đâu rồi?" |

## 3. Meeting — `MeetingMineCriteria` / `MeetingCriteria`

| Công cụ | Đang có | Đề xuất thêm | Câu hỏi mở được |
|---|---|---|---|
| `lich_meeting` (MineCriteria, role=all) | tu_ngay/den_ngay | `vai_tro` chu_tri/thanh_vien (role host/member) · `trang_thai` (Lên lịch/Chốt lịch/Hoàn thành/Hủy) · `chua_co_bien_ban` (quick=pending_report) · `tu_khoa` | "Cuộc họp tôi chủ trì tuần sau", "Họp nào đã xong mà chưa có biên bản?", "Lịch họp về phần mềm" |
| **MỚI** `meeting_cua_phong` (MeetingCriteria + quyền `meeting.danh_sach_meeting.view`) | — | `phong_ban_id`, khoảng ngày, `trang_thai`, `khach_hang` (customer_id qua tra cứu), `co_bien_ban` | "Tuần này phòng KD có bao nhiêu cuộc họp với khách?", "Họp với khách hàng ABC gần nhất khi nào?" |

Lưu ý: `MeetingCriteria` lọc `to_date` theo `end_date` (cuộc họp phải nằm trọn trong khoảng), khác `MineCriteria` (theo `start_date`).

## 4. Phiếu công tác — `AssignRequest` type=2 — CHƯA có công cụ

- Của tôi: `MyJobService::getAssignBusinessList` (`MyJobService.php:974-1078`): keyword (mã), business_type
  (1 kỹ thuật/2 khác), status, customer_id, contract_code, parent_code, from_time/to_time.
- Theo phạm vi: `AssignBusinessService::searchByFilter` — **bắt buộc truyền `type=all`** (không truyền thì không áp phạm vi).
  Quyền `assign.danh_sach_phieu_giao_cong_tac.view`.
- Trạng thái: 1 Đang tạo · 2 Chờ duyệt · 3 Đã duyệt · 5 Chờ duyệt KQ · 6 Không duyệt · 7 Đã duyệt KQ · 8–11 hồ sơ/đề nghị thanh toán.

| Đề xuất | Tham số | Câu hỏi mở được |
|---|---|---|
| **MỚI** `phieu_cong_tac` | `pham_vi` toi/phong/cong_ty · `tu_ngay/den_ngay` (from_time/to_time) · `trang_thai` · `loai` (kỹ thuật/khác) · `khach_hang` (tên) | "Tuần sau tôi đi công tác đâu?", "Phiếu công tác của tôi duyệt chưa?", "Hôm nay phòng tôi ai đang đi công tác?", "Phiếu công tác chờ thanh toán" |

## 5. Phiếu giao việc — `AssignJob` (`AssignJobService::searchByFilter`) — CHƯA có công cụ

- Có: company/department (+ phòng thực hiện/yêu cầu), part, employee_info_id (= NGƯỜI TẠO), code, job_request_code,
  customer, status (1 Đang tạo/2 Chờ duyệt/3 Đã duyệt/4 Từ chối/5 Đã nhập KQ/6 Đã duyệt KQ). Quyền
  `assign.danh_sach_phieu_giao_viec.view`.
- **Thiếu**: lọc "phiếu giao cho tôi" (người thực hiện ở `assign_job_employees`) và lọc theo hạn (`deadline`) ⇒ làm thêm
  trong query của Agent (không sửa service dùng chung).

| Đề xuất | Tham số | Câu hỏi mở được |
|---|---|---|
| **MỚI** `phieu_giao_viec` | `pham_vi` toi (người thực hiện)/phong/cong_ty · `trang_thai` · `khach_hang` · `tu_ngay/den_ngay` (deadline) | "Tôi còn phiếu giao việc nào chưa nhập kết quả?", "Phiếu giao việc chờ duyệt của phòng", "Việc lắp đặt cho khách X tới đâu?" |

## 6. Bảng công

| Công cụ | Đang có | Đề xuất | Câu hỏi mở được |
|---|---|---|---|
| `bang_cong_nhan_vien` | 1 NV, tháng | giữ | — |
| **MỚI** `bang_cong_phong` | — | `TimesheetSummaryController::index` logic (department_id/part_id/keyword, khoảng ngày, quyền `timesheet.bang_cham_cong_chi_tiet.view` ≥ 2) · `sap_xep` theo đi muộn / nghỉ không lý do / làm thêm · tối đa 20 NV | "Tháng này phòng tôi ai đi muộn nhiều nhất?", "Ai nghỉ không lý do tháng 10?" |
| `tinh_hinh_di_lam_hom_nay` | phong_ban_id | trả thêm số theo từng phòng (`dimuon_ve_som_theo_phong`, `ko_di_lam_theo_phong_ban`), `khong_co_ca`, `cong_tac_chi_tiet` (dữ liệu `hcns` đã có, chỉ chưa đưa ra) | "Phòng nào hôm nay vắng nhiều nhất?", "Hôm nay ai đi công tác?" |
| `cham_cong_theo_ngay` | tu_ngay/den_ngay (của tôi) | giữ | — |

Không dùng `timekeeper_report` cho Agent cho tới khi vá SQL thô (ghi chú lỗ hổng #10).

## 7. Phép + các loại đơn

| Công cụ | Đang có | Đề xuất | Câu hỏi mở được |
|---|---|---|---|
| `phep_con_lai` | của tôi, năm nay | giữ | — |
| **MỚI** `phep_cua_phong` | — | `ReportService::attendance_report` (year, department_id, part_id, keyword; quyền `timesheet.bao_cao_phep.view` ≥ 2) — có cả phép dùng theo từng tháng | "Phòng tôi ai còn nhiều phép nhất?", "Anh Nam năm nay nghỉ phép mấy ngày?" |
| `don_cua_toi` | loai, trang_thai, khoảng ngày **tạo** | thêm khoảng **thời gian nghỉ** (attendance_start_at/end_at — giao khoảng), `loai_nghi` (leave_type) | "Đơn nghỉ tuần sau của tôi duyệt chưa?" (hiện lọc theo ngày tạo nên dễ trả sai) |
| `don_cho_toi_duyet` | loai | `nhan_vien` (tên), `phong_ban_id`, khoảng thời gian | "Đơn của chị Lan chờ tôi duyệt" |
| **MỚI** `don_cua_phong` | — | `index` có `applyViewScope` (quyền `timesheet.don_xin_nghi.view` …) · loai · trạng thái · khoảng thời gian nghỉ · phong_ban_id | "Tuần này phòng tôi ai xin nghỉ?", "Ai đăng ký làm thêm thứ 7?" |

Lưu ý: tham số `employee_id` ở các service đơn nghĩa là `created_by` (id user), không phải `employee_infos.id`.

## 8. Nhắc việc cá nhân — "Việc của tôi" (my-todo) — CHƯA có công cụ

- Bảng `personal_todos` (`Modules/Assign/Entities/MyTodo/PersonalTodo.php`): title, description, due_date, due_time,
  start_date/start_time, is_completed, completed_at, list_id (danh sách: Cá nhân / Công ty / tự tạo), contact_id
  (danh bạ cá nhân), parent_id (việc con). Của riêng từng người: `MyTodoOwnershipScope::personalTodos` = `user_id = tôi`,
  không có phân quyền xem của người khác.
- API dùng chung: `GET v1/assign/my-todo` → `MyTodoService::getAll($filters, auth()->id())`
  (`Modules/Assign/Services/MyTodo/MyTodoService.php:1201`), lọc: `type` · `status` / `status_groups`
  (todo/doing/done/stopped) · `date` / `date_from` / `date_to` (theo hạn) · `is_overdue` · `list_id` · `month`.
- Điểm đáng chú ý: `getAll` **gộp sẵn 6 loại** của chính người hỏi — nhiệm vụ, vấn đề, phiếu giao việc, phiếu công tác,
  meeting, nhắc việc cá nhân (`type` = task/issue/assign_job/assign_business/meeting/personal), đã chuẩn hoá cùng 1 dạng.

| Đề xuất | Tham số | Câu hỏi mở được |
|---|---|---|
| **MỚI** `nhac_viec_cua_toi` (getAll với `type=personal`) | `trang_thai` chua_xong/da_xong · `tu_ngay/den_ngay` (hạn) · `qua_han` · `danh_sach` (tên danh sách ⇒ list_id) · `tu_khoa` (lọc tiêu đề trong Agent) | "Hôm nay tôi có nhắc việc gì?", "Tuần này tôi phải gọi cho ai?", "Nhắc việc nào của tôi quá hạn?", "Việc trong danh sách Công ty chưa xong" |
| Cân nhắc thêm: `viec_tong_hop_cua_toi` (getAll không giới hạn type) | `loai` (6 loại) · trạng thái · khoảng hạn · quá hạn | "Hôm nay tôi có việc gì?" chỉ còn **1 lần gọi** thay vì 2–3 (viec_cua_toi + lich_meeting) ⇒ rẻ hơn và trả lời đủ cả vấn đề / phiếu / nhắc việc; khớp đúng màn "Việc của tôi" người dùng đang thấy |

---

## Thứ tự đề xuất

| Ưu tiên | Việc | Lý do |
|---|---|---|
| **1** | `don_cua_phong` + sửa `don_cua_toi` lọc theo thời gian nghỉ | Câu quản lý hỏi hằng ngày ("ai nghỉ"); `don_cua_toi` hiện lọc theo ngày tạo dễ trả sai |
| **1** | `viec_cua_toi`: vai_tro giao/duyet + uu_tien + tu_khoa | Rẻ (chỉ thêm tham số), mở nhiều câu |
| **1** | `van_de` (công cụ mới) | Phân hệ Công việc chưa có gì về Vấn đề |
| **1** | `nhac_viec_cua_toi` (công cụ mới; cân nhắc làm luôn `viec_tong_hop_cua_toi`) | User yêu cầu 11/11; dữ liệu riêng của chính người hỏi, không cần phân quyền ⇒ làm nhanh, an toàn |
| **2** | `phieu_cong_tac` | Câu "ai đang đi công tác / tôi đi đâu" |
| **2** | `lich_meeting` thêm vai_tro/trang_thai/chưa có biên bản | Rẻ |
| **2** | `phep_cua_phong`, `bang_cong_phong`, mở rộng `tinh_hinh_di_lam_hom_nay` | Câu cho trưởng phòng / HCNS |
| **3** | `thong_ke_viec`, `meeting_cua_phong`, `phieu_giao_viec` | Ít người hỏi hơn |

Mỗi việc: test có quyền + không quyền, thêm câu eval, `agent:eval` không tụt điểm câu cũ (~800 ₫/lần).

## Lỗ hổng phát hiện thêm khi rà

Đã ghi vào `.plans/gop-db/va-lo-hong-quyen-doc/ghi-chu.md` (#9–#14) — vá ở đợt riêng. Công cụ Agent mới KHÔNG gọi các
endpoint đó (gọi service + tự kiểm quyền như các công cụ hiện có).
