# Fix: Popup thương hiệu-hãng rỗng ở màn Phân công NV phụ trách hãng (ERP)

**Nhánh:** `gop_db` (repo ERP TanPhatDev) — @namdangit
**Loại:** Bug fix — họ lỗi gộp DB "thêm cột trùng tên → code cũ đọc nhầm cột".

## Hiện tượng
Màn `/admin/assign/employee/create` (ERP), popup "Danh sách thương hiệu hãng sản xuất"
rỗng ("Chưa có dữ liệu") dù cặp WGF – ZHUHAI WINGFOX CO.,LTD **đã** được phân về
PHÒNG DỰ ÁN TRỌNG ĐIỂM (phiếu TPE.PCPPTH.00546 đã duyệt). Xảy ra với **mọi user không phải
Super Admin**, mọi phòng — không riêng ca này.

## Root cause (đã chứng minh trên DB gộp, read-only)
`AssignEmployeeController::create()`, nhánh **không phải Super Admin** (dòng ~311) dựng dropdown
phòng ban bằng `EmployeeManageDepartment::join('departments', …)->get()` **KHÔNG có `select()`**
→ `SELECT *` gộp cột cả 2 bảng.

- Sau gộp DB, bảng `departments` (dùng chung) **mọc thêm** cột `department_id` — cột dấu vết phía
  HRM, mang hằng số **43** (= id phòng Nhân sự-Hành chính) cho 100/103 phòng. ERP gốc KHÔNG có cột
  này (không migration nào — ERP lẫn HRM — tạo nó).
- `departments` join sau nên `departments.department_id = 43` **ghi đè**
  `employee_manage_departments.department_id` (=95, phòng đúng) trong kết quả.
- View render `<option value="<% d.department_id %>">` = **43**, nhưng hiển thị tên phòng của id 95.
- Chọn phòng → FE gửi `department_id=43` xuống `getDataDepartment` → lọc
  `brand_department_id=43 OR buy_department_id=43` → phân công thật ở dept **95** → **rỗng**.

Nhánh Super Admin không dính vì có `->select('id as department_id', 'name')` tường minh.

**Kết luận:** `SELECT *` là cẩu thả tiềm ẩn (trước gộp chỉ có 1 cột `department_id` = của
`employee_manage_departments` = đúng), **chỉ phát bệnh sau khi gộp thêm cột trùng tên**. Không phải
lỗi dữ liệu phân công, không phải status brand/hãng, không phải chọn sai phòng.

## Bản vá
`app/Http/Controllers/Assign/AssignEmployeeController.php` — nhánh non-Super-Admin của `create()`:
thêm `->select('departments.id as department_id', 'departments.name')` (khớp ngữ nghĩa nhánh
Super Admin). Chỉ sửa code, KHÔNG ghi DB, KHÔNG đụng hàm dùng chung.

## Kiểm chứng (tinker, read-only, prod gộp)
- Trước fix: option "PHÒNG DỰ ÁN TRỌNG ĐIỂM" → `department_id=43`.
- Sau fix: `department_id=95`; gọi `getDataDepartment(95)` (auth emp 211 Bùi Thị Phương) →
  60 dòng; lọc brand=1519/manu=1365 → 1 dòng = **WGF → ZHUHAI WINGFOX CO.,LTD** (phòng 95). ✓

## Cùng họ lỗi (chưa xử lý — mục B user chưa yêu cầu)
Bất kỳ chỗ nào khác `SELECT *` join `departments` rồi đọc `department_id` cũng có thể dính (nhận 43
thay vì id phòng). Nếu cần quét trọn họ → làm ở lần sau.
