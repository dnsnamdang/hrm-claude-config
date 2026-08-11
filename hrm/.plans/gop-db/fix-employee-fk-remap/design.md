# Design (tóm tắt) — Vá remap FK employees bị sót khi gộp DB

Nhánh `gop_db` · @junfoke · 2026-08-04
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-04-fix-employee-fk-remap-design.md`

## Vấn đề

Khi gộp DB, `employees` của HRM bị thay bằng `employees` của ERP → **454/1085 nhân viên đổi id**.
`ReconcileEmployeesSeeder` chịu trách nhiệm remap FK, nhưng nó dò cột theo **danh sách tên cột cứng**:

- `AUDIT_COLS` (35 tên) — remap thẳng
- `CLASSIFY_COLS` (4 tên: `employee_id`, `user_id`, `emp_id`, `executor_id`) — remap nếu **100%** giá trị nằm trong `hrm_employees`

Hai lỗ hổng:

1. Mọi cột FK employee tên "lạ" không bao giờ được đụng: `main_sale_employee_id`, `actor_id`, `pm_id`,
   `member_id`, `salary_change_employee_id`, `transfer_employee_id`, `new_employee_manager_id`, `handover_employee_id`…
2. Ngưỡng 100% quá cứng: chỉ cần vài dòng trỏ nhân viên đã xoá là **loại cả cột** (40 cột rơi vào diện này).

Ngoài ra seeder chỉ xử lý cột kiểu số — bỏ qua cột `varchar` chứa id và cột JSON chứa mảng id.

**Vì sao không ai phát hiện**: phần lớn id sai vẫn lọt vào dải id hợp lệ nên **trỏ sang người khác một cách
im lặng** (Sale mất quyền thao tác báo giá của chính mình, người lạ lại có quyền), không sinh lỗi FK.

## Quy mô (đo trên `local_hrm_erp`)

**20.231 dòng** trên 42 cột. Nặng nhất: `course_student_attendances` 11.557 · `course_students` 1.988 ·
`payment_profile_employees` 1.564 · `assign_request_employees` 1.549 · `payment_business_request_fees` 660.

## Quyết định

1. **Không sửa dữ liệu bằng tay** — làm bằng seeder git-backed, DRY mặc định, giống nhóm GopDb sẵn có.
2. **Nguồn map**: dựng lại `hrm_employees` từ snapshot `hrm_prod_6_6` (1.085 dòng, khớp 1085/1085
   `employee_info_id` với DB gộp — đúng bản dùng khi gộp; `hrm_prod_local` chỉ 1.081 nên KHÔNG dùng).
3. **Phân loại cột phải do người làm, không để máy đoán**. Dải id nhân viên trùng dải id của hầu hết
   bảng danh mục nên tỉ lệ trùng cao không chứng minh được gì — `salary_changes.new_department_id`
   đạt 95% "khớp employees" nhưng là id phòng ban. Căn cứ dùng để chốt là **code**: quan hệ model
   (`belongsTo(Employee)`), `->where('employees.id', …)`, hoặc so với `auth()->user()->id`.
4. **Seeder tổng chuyển sang fail-closed**: dò dữ liệu trên MỌI cột int/varchar của bảng HRM-origin,
   cột nào chưa nằm trong `$FORCE_COLS`/`$DENY_COLS` thì **in ra và DỪNG**, không remap gì.
   Bỏ sót về sau sẽ báo lỗi thay vì im lặng.
5. **Chống chạy lại**: mốc trong bảng `gop_db_steps`, không dựa vào sự tồn tại của `hrm_employees` nữa
   (bảng đó nay được nạp lại để vá). Remap 2 lần là thảm hoạ: **164 id vừa là id HRM cũ của người này
   vừa là id ERP mới của người khác**.

## Lỗi phát sinh đã sửa

**Toàn bộ pipeline GopDb chưa từng chạy được.** `GopDbHelper::run(string $sql)` trùng tên với
`public function run()` mà Laravel gọi; trong PHP method của class thắng method của trait → mọi
`$this->run("SQL")` gọi lại chính seeder = đệ quy vô hạn, không câu SQL nào được thực thi.
Chưa ai phát hiện vì trên DB đã gộp seeder luôn rơi vào nhánh SKIP.
→ Đổi tên trait method thành `exec()`, sửa 44 chỗ gọi trong 5 seeder.

## Kết quả

- `FixMissedEmployeeFkSeeder` — vá 42 cột đã xác minh (int / varchar / JSON / có điều kiện), giữ lại `hrm_employees`.
- `ReconcileEmployeesSeeder` — dò theo dữ liệu + fail-closed + mốc chống chạy lại + xử lý cột JSON.
- Không còn cột nào chờ quyết định (`$NEED_DECISION` rỗng).

## Bài học: phải đọc cả code FRONTEND

Vòng phân tích đầu chỉ dựa vào BE nên 6 cột bị xếp "chưa kết luận". Đọc thêm `hrm-client` thì **cả 6 đều
kết luận được**, và lộ thêm 1 cột nữa (`increase_seniority_employees.employee_id`, bảng đang rỗng nên
lượt quét dữ liệu bỏ qua). FE là nơi biết chắc id nào được gửi lên: nguồn của mỗi picker
(`store/actions.js:103` → `Employee::getAll()` → `employees.id`) và cờ phân loại kèm theo
(`PopupStaff.vue:331` gán `type=1/2`) chính là căn cứ mà BE không thể hiện rõ.

## Remap có điều kiện

`rice_employee_infos.employee_id` **chỉ trỏ `employees.id` với một phần dữ liệu**: nhóm công ty Tân Phát
(`rice_companies.parent_id = 1`) khớp 927/927 với `hrm_employees`, còn nhóm ETEK chỉ 92% vì là hệ thống
riêng. Remap cả cột sẽ hỏng nhóm ETEK → thêm cơ chế `$COND_COLS` nhận thêm mệnh đề JOIN điều kiện.
448 dòng được vá; đã kiểm chứng chéo: sau vá `employees.employee_info_id` khớp 100%
`rice_employee_infos.employee_info_id`.

Ba cột khác cũng chỉ đúng một phần:

| Cột | Điều kiện | Dòng |
|---|---|---:|
| `meeting_reports.executor_id` | `executor_type = 1` (nhân sự công ty; type=2 là id khách mời) | 17 |
| `meeting_reports.proposer_id` | `proposer_type = 1` | 4 |
| `insurance_register_type_employees.employee_id` | dòng ĐẦU mỗi (phiếu, loại BH); dòng sau là `employee_relationships.id` | 169 |

Kiểm chứng chéo bảo hiểm: sau khi map, dòng đầu khớp `insurance_registers.created_by` **718/718**
(trước khi map chỉ 549/718) — `created_by` đã được remap đúng ở lần gộp nên là mốc độc lập.

## Còn nợ

- Trên production **bắt buộc giữ dump HRM trước khi gộp** — mất là không dựng lại map được.
