# Plan — Vá remap FK employees bị sót khi gộp DB

Nhánh: `gop_db` (hrm-api). Phụ trách: @junfoke

## Phase 1 — Xác minh danh sách cột (BE)

- [x] Quét vét cạn 3.374 cột int + 1.801 cột chuỗi + cột JSON trên 640 bảng HRM-origin
- [x] Xác minh 11 cột nhóm A (bỏ sót hoàn toàn) bằng code — đều là FK `employees.id`
- [x] Loại 3 dương tính giả (`provinces.crm_id`, `parts.part_lead_id`, `department_changes.new_department_lead_id`)
- [x] Phát hiện nhóm C: 40 cột `CLASSIFY_COLS` bị bộ phân loại loại nhầm
- [x] Xác minh ngữ nghĩa 40 cột nhóm C (`employees.id` hay `employee_infos.id`) bằng quan hệ model
- [x] Chốt danh sách cột cần remap, ghi vào design.md

## Phase 2 — Seeder vá (BE)

- [x] Dựng lại `local_hrm_erp.hrm_employees` từ snapshot `hrm_prod_6_6` (1.085 dòng, 454 NV đổi id)
- [x] Viết `FixMissedEmployeeFkSeeder`: dựng `emp_id_map` từ `hrm_employees`, remap đúng danh sách cột đã chốt
- [x] Hỗ trợ 3 dạng lưu: int, varchar chứa số, JSON `[{"id":…}]`
- [x] DRY mặc định (`GOP_DB_APPLY=1` mới ghi), in số dòng trước/sau từng cột
- [x] Không drop `hrm_employees` khi kết thúc
- [x] Chạy DRY, đối chiếu số dòng với kết quả quét

## Phase 3 — Sửa gốc ReconcileEmployeesSeeder (BE)

- [x] Thay danh sách tên cột cứng bằng dò theo dữ liệu (mọi cột int/varchar trong bảng HRM-origin)
- [x] Bỏ ngưỡng 100% cứng của bộ phân loại → dùng tỉ lệ + danh sách loại trừ tường minh
- [x] Bổ sung xử lý cột JSON chứa id nhân viên
- [x] Thêm cờ chống chạy lại (không dựa vào sự tồn tại của `hrm_employees`)
- [x] In danh sách cột sẽ remap để người duyệt trước khi apply
- [x] Cập nhật `HUONG-DAN-CHAY.md`

## Phase 4 — Tài liệu

- [x] Viết `design.md` (tóm tắt) + `docs/superpowers/specs/gop-db/2026-08-04-fix-employee-fk-remap-design.md` (chi tiết)
- [x] Cập nhật `.plans/gop-db/STATUS.md`

## Phase 5 — Lỗi nền tảng phát hiện khi chạy thử (BE)

- [x] `GopDbHelper::run()` trùng tên `Seeder::run()` → đệ quy vô hạn, 5/7 seeder GopDb chưa từng chạy được
- [x] Đổi tên trait method thành `exec()`, sửa 44 chỗ gọi trong 5 seeder
- [x] Phân loại 24 cột ứng viên do bộ dò mới nêu ra → thêm vào `$DENY_COLS`

## Phase 6 — Kiểm thử thật (BE)

- [x] Nhân bản 33 bảng liên quan sang schema `gopdb_fixtest`, chạy `GOP_DB_APPLY=1` trên bản sao
- [x] Số dòng: 0/33 bảng thay đổi
- [x] Checksum từng cột: 0 cột ngoài danh sách bị đụng
- [x] 33 cột đích: 0 dòng sai map, 0 dòng bị hoá NULL/0 (930+22+13 dòng `=0` là dữ liệu bẩn có sẵn)
- [x] Cột JSON: giữ nguyên số phần tử, tên người, kiểu chuỗi/số của id; chỉ khoá `id` đổi
- [x] 🐛 Sửa: `JSON_UNESCAPED_UNICODE` làm lệch quy ước escape của app → bỏ, khớp `json_encode` mặc định
- [x] 🐛 Bổ sung: chốt chặn chạy lần hai bằng mốc `gop_db_steps` (trước đó chỉ cảnh báo)
- [x] Test chạy 2 lần liên tiếp: lần 2 bị chặn, dữ liệu không đổi
- [x] FK mồ côi `prospective_projects.main_sale_employee_id`: 14 → 0

## Phase 7 — Remap có điều kiện (BE)

- [x] User chỉ ra `rice_employee_infos.employee_id` cần vá, chỉ với `rice_companies.parent_id = 1`
- [x] Xác minh: nhóm `parent_id=1` khớp 927/927 `hrm_employees`; nhóm khác chỉ 92% (hệ thống riêng ETEK)
- [x] Thêm cơ chế `$COND_COLS` (JOIN điều kiện) vào cả 2 seeder, bỏ khỏi `$NEED_DECISION`/`$DENY_COLS`
- [x] Test: 448 dòng đổi, nhóm ngoài `parent_id=1` nguyên vẹn 0 dòng bị đụng
- [x] Kiểm chứng chéo: sau vá, `employees.employee_info_id` khớp 100% `rice_employee_infos.employee_info_id`

## Phase 8 — Đọc code FRONTEND (user yêu cầu) (BE+FE)

- [x] User chỉ ra mới chỉ phân tích BE → đọc lại `hrm-client` cho toàn bộ nhóm chưa kết luận
- [x] `store/actions.js:103` + `Employee::getAll()` → `$store.state.employees[].id` = `employees.id`
- [x] `meeting_employees.employee_id` = employees.id (GeneralInfo.vue:661 + MeetingController:441 `select e.id`) — 39 dòng
- [x] `appendix_labor_contracts.employee_id` = employees.id (InfoFormComponent.vue:181 gọi route bind `Employee`) — 34 dòng
- [x] `personal_todo_lists/personal_todos.user_id` = employees.id (MyTodoController:54 `auth()->id()`) — 39 + 1 dòng
- [x] `meeting_reports.executor_id/proposer_id` → remap có điều kiện `type = 1` (PopupStaff.vue:331) — 17 + 4 dòng
- [x] `insurance_register_type_employees.employee_id` → chỉ DÒNG ĐẦU mỗi (phiếu, loại BH); dòng sau là người thân
      (SingleEmployeeInsurance.vue:86 chỉ hiện select người thân từ idx>=1) — 169 dòng
- [x] Kiểm chứng chéo BH: dòng đầu sau map khớp `insurance_registers.created_by` **718/718** (trước map chỉ 549/718)
- [x] Phát hiện thêm `increase_seniority_employees.employee_id` (bảng đang rỗng nên lượt quét dữ liệu bỏ qua) — khai sẵn
- [x] `$NEED_DECISION` còn RỖNG — không còn cột nào chờ quyết định
- [x] Mở rộng `$COND_COLS` thành mảng có `prepare` / `join` / `where`; đồng bộ sang seeder tổng

## Phase 9 — Kiểm thử lại toàn bộ sau khi mở rộng (BE)

- [x] Nhân bản 44 bảng, chạy thật: 42 cột / 20.231 dòng
- [x] Số dòng: 0/44 bảng thay đổi
- [x] Checksum **1.005 cột** ngoài danh sách: 0 cột bị đụng
- [x] 42 cột đích: 0 sai map, 0 dòng ngoài điều kiện bị đụng, 0 dòng hoá NULL/0
- [x] Đối chiếu độc lập: BH 718/718 khớp `created_by`; rice 927/927 khớp `employee_info_id`
- [x] JSON: 0 khác biệt ngoài khoá `id`, 0 bản ghi hỏng
- [x] `employees` / `hrm_employees` không bị sửa dòng nào
- [x] Không ghi nhầm sang schema gốc; DRY xác nhận không ghi gì
- [x] Chạy lần 2 bị chặn (nếu gỡ chốt sẽ hỏng thêm **4.021 dòng**)

### Checkpoint — 2026-08-04
Vừa hoàn thành: FixMissedEmployeeFkSeeder (42 cột / 20.231 dòng, gồm 4 cột remap có điều kiện) + sửa gốc ReconcileEmployeesSeeder
(dò theo dữ liệu, fail-closed, mốc `gop_db_steps`, cột JSON) + sửa lỗi đệ quy `run()` của GopDbHelper.
Đã dựng `local_hrm_erp.hrm_employees` từ `hrm_prod_6_6` (1.085 dòng, 454 NV đổi id).
Đã kiểm thử thật trên schema nhân bản `gopdb_fixtest` (đã xoá sau khi test): không đụng cột ngoài danh sách,
không sai map, không sinh NULL/0, chạy lần 2 bị chặn. CHƯA chạy trên `local_hrm_erp` — chờ user backup.
Bước tiếp theo: user backup `local_hrm_erp` → chạy `GOP_DB_APPLY=1 php artisan db:seed --class=…FixMissedEmployeeFkSeeder`.
Blocked: (không còn) — `$NEED_DECISION` đã rỗng sau khi đọc code frontend.
