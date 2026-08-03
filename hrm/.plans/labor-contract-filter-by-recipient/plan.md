# Plan — Filter HĐLĐ lọc theo người được gán (recipient)

## Bối cảnh
Màn `/decision/labor-contract`: filter Công ty/Phòng ban/Bộ phận đang lọc theo org của **người tạo** (cột `company_id/department_id/part_id` do `BaseModel::boot` auto-set). Yêu cầu: đổi sang lọc theo org của **người được gán trong HĐLĐ** (recipient — cột `labor_contract_company_id/_department_id/_part_id`).

## Phase 1 — Bugfix

### BE (hrm-api)
- [x] Sửa `DecisionLaborContractService::index()` (dòng 43-50): đổi 3 điều kiện filter từ `decision_labor_contracts.company_id/department_id/part_id` sang `labor_contract_company_id/labor_contract_department_id/labor_contract_part_id`. Cover luôn `export()` (gọi lại `index()`) và trang print list (dùng chung endpoint).

### Verify
- [ ] Lọc Công ty/Phòng ban/Bộ phận trên `/decision/labor-contract` → ra HĐLĐ có người được gán thuộc org đó (không phải theo người tạo)
- [ ] Export Excel + Print list áp dụng đúng bộ lọc mới

## Phase 2 — Thêm cột danh sách

### FE (hrm-client)
- [x] `index.vue`: thêm cột "Phòng ban" (`labor_contract_department_name`) ngay sau cột Nhân viên; thêm cột "Ngày hết hạn hợp đồng" (`end_date`) ngay sau cột Ngày bắt đầu hợp đồng. API resource đã trả sẵn 2 field → không sửa BE.

### Verify
- [ ] Danh sách hiển thị đúng 2 cột mới đúng vị trí, có dữ liệu
