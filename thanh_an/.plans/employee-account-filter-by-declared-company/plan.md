# Plan — Lọc công ty theo công ty kê khai trong tài khoản (màn Danh mục tài khoản nhân viên)

**Phụ trách:** @khoipv
**Ngày:** 2026-08-19

## Bối cảnh
Màn `human/employee` (Danh mục tài khoản nhân viên) đang lọc "Công ty" theo
`employee_infos.company_id` (công ty của **hồ sơ nhân sự**). Yêu cầu: lọc theo
**công ty kê khai bên trong tài khoản** (multiselect "Công ty" ở form
`human/employee/{id}` → `company_ids` → bảng nối `company_employees`).

## Quyết định đã chốt với user
1. **Phạm vi:** CHỈ màn danh sách tài khoản. Các popup chọn nhân viên
   (`AddEmployeeModal`, `AddEmployeeSingleModal`, `AddEmployeeAssignModal`,
   `AddEmployeeCreateContractModal`, `AddEmployeeCreateQuotationModal`,
   `customer_handover`) giữ nguyên lọc theo công ty hồ sơ.
   → Dùng **tham số mới `account_company_id`**, KHÔNG đụng nhánh `company_id` cũ
   (vì 2 modal cũng gọi chính endpoint `human/employee` index).
2. **Luật lọc:** thuần theo `company_employees` (KHÔNG OR với công ty hồ sơ).
   Tài khoản chưa kê khai công ty nào → không hiện khi có lọc công ty.
3. Bộ lọc "Phòng ban" giữ nguyên theo hồ sơ. Không migration, không quyền mới.

## Task

### Backend
- [x] BE1. `EmployeeService::getEmployees()` — thêm nhánh `account_company_id`
      → `whereHas('companies', fn($q) => $q->where('companies.id', $id))`.
      Giữ nguyên nhánh `company_id` cũ.
- [x] BE2. `EmployeeController::index()` — nhận thêm `account_company_id`.
      (KHÔNG thêm vào `modalSearchData()`.)

### Frontend
- [x] FE1. `pages/human/employee/index.vue` — trong `getEmployees()` map
      `formFilter.company_id` → param `account_company_id` (giữ v-model
      `company_id` để `CompanyDepartmentFilter` + dropdown Phòng ban vẫn chạy).
- [x] FE2. Xử lý tương tự cho `resetSearch()` (đảm bảo không gửi sai key).

### Verify
- [x] V1. `php -l` file BE, lint FE.
- [x] V2. Đối chiếu SQL: tài khoản hồ sơ cty A + kê khai cty B → lọc B ra, lọc A không ra.
- [x] V3. Regression: 5 popup chọn nhân viên vẫn lọc theo công ty hồ sơ (param `company_id` không đổi).

## Checkpoint

### Checkpoint — 2026-08-19
Vừa hoàn thành: BE1/BE2 + FE1/FE2 + V1/V2/V3. Code xong toàn bộ.
Kết quả verify (DB `thanhan_stag_07052026`, chạy thật qua `EmployeeService::getEmployees`):
- `account_company_id=3` → 23 bản ghi (khớp SQL `EXISTS company_employees`)
- `company_id=3` (nhánh cũ) → 7 bản ghi — KHÔNG đổi ⇒ 5 popup chọn nhân viên an toàn
- Không lọc → 164
- TK id=16 (hồ sơ cty 4, kê khai cty 3): lọc cty 3 RA, lọc cty 4 KHÔNG ra ⇒ đúng luật đã chốt
- 0/164 tài khoản chưa kê khai công ty ⇒ không tài khoản nào bị "mất tích"
- php -l 2 file BE sạch; node --check script FE sạch
Đang làm dở: (không)
Bước tiếp theo: user verify UI trên màn `human/employee` (mở Bộ lọc → chọn Công ty)
Blocked:
