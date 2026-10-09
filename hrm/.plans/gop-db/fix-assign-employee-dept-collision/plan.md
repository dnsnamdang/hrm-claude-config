# Plan — Fix popup thương hiệu-hãng rỗng (Phân công NV phụ trách hãng, ERP)

Repo: ERP TanPhatDev · Nhánh: `gop_db`

## Phase 1 — Fix va chạm cột department_id ở dropdown phòng ban

- [x] Điều tra root cause (read-only prod gộp): xác định `departments.department_id`=43 do gộp DB
      thêm, `SELECT *` join ghi đè → dropdown gửi id sai
- [x] Sửa `AssignEmployeeController::create()` nhánh non-Super-Admin: thêm
      `->select('departments.id as department_id', 'departments.name')`
- [x] `php -l` controller — no syntax error
- [x] Verify tinker: sau fix option gửi `department_id=95`, `getDataDepartment` trả đúng
      WGF → ZHUHAI WINGFOX (phòng 95)
- [ ] User kiểm tra lại trên môi trường thật (đăng nhập non-Super-Admin, mở màn, popup có dữ liệu)

### Checkpoint — 2026-09-28
Vừa hoàn thành: fix 1 dòng `select()` cho `create()`; verify tinker end-to-end OK.
Đang làm dở: (không) — chờ user nghiệm thu trên UI thật.
Bước tiếp theo: nếu user yêu cầu mục B → quét các chỗ `SELECT *` join departments đọc department_id.
Blocked:

## Phase 2 — (TÙY CHỌN, chưa yêu cầu) Quét trọn họ lỗi
- [ ] Grep các chỗ join `employee_manage_departments`/`departments` bằng `SELECT *` rồi đọc
      `department_id`, fix qualify/select tương tự
