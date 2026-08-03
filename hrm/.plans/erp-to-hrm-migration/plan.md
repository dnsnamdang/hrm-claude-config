# Plan — ERP → HRM Migration (Umbrella)

## Phase 0 — Tư vấn & chốt chiến lược (đang làm)
- [x] Khảo sát quy mô ERP + hiện trạng HRM (xem design.md)
- [x] Chốt chiến lược dữ liệu: **gộp 1 pháp nhân, đích = 1 schema HRM duy nhất (B)**; ERP repoint sang DB HRM; bỏ connection phân tán
- [x] Chốt ERP: retire dần từng domain (Strangler)
- [x] Phân loại 50 bảng trùng tên (xem phase2-risk-map.md): 44 cùng thực thể / 3 phần / 3 giả
- [x] Chốt T3 lõi tổ chức đã đồng bộ sẵn → merge = retire copy ERP + gỡ sync
- [x] Đối chiếu dữ liệu bất đồng bộ T3 giữa HRM↔ERP (**XONG 2026-07-27 trên DB production** — xem `reconcile-t3-report.md` + `idmap-employees-drift.csv`)
- [ ] Chốt biến thể còn dùng (thường/firm/zt-ztec/project/inland) + thứ tự ưu tiên 4 mảng
- [ ] Viết spec chi tiết + roadmap phân rã theo domain

## Harness đối chiếu bất đồng bộ (đã dựng, sẵn sàng chạy lại)
- Cả 2 DB local cùng server 127.0.0.1:3306 — HRM=`hrm_tpe`, ERP=`erp2326` → **đối chiếu chéo schema bằng SQL trực tiếp** (không cần Laravel; tinker HIỆN KHÔNG boot được vì `Modules/Accounting/module.json` lỗi JSON do merge conflict chưa resolve).
- Password DB local trong `hrm-api/.env` (`DB_PASSWORD`), tạo `my.cnf` tạm cho `mysql --defaults-extra-file` để tránh lỗi ký tự `!`.
- **Natural key phát hiện được:** companies→`tax_code` (tốt hơn `code`; match tax_code ERP-only=0), departments→`code`, parts→`name` (`code` chỉ có ở HRM), employees→`email`, employee_infos→`code`. `module_mappings` (HRM) **rỗng** → sync KHÔNG map qua bảng này.
- Bảng cần đối chiếu: provinces, districts, wards, employee_infos, employees, companies, departments, parts.

### Checkpoint — 2026-07-27 (WRAP UP)
Vừa hoàn thành: Phase 0 sizing + chốt kiến trúc (gộp 1 pháp nhân → 1 schema HRM; ERP repoint; prefix `tp_`; Strangler 2 phase). Phân loại 50 bảng trùng (phase2-risk-map.md). Dựng harness đối chiếu chéo schema + tìm natural key. Viết SPEC đầy đủ: `docs/superpowers/specs/2026-07-27-erp-to-hrm-migration-design.md`.
Đang làm dở: đối chiếu bản ghi bất đồng bộ T3 — DB local **lẫn nhiều bản test** ("Công ty test", "Phòng ban 01/001"…) nên số liệu chưa tin được.
Bước tiếp: user kéo DB chuẩn từ production về local → (1) verify cơ chế sync HRM→ERP trong code để chốt đúng field mapping; (2) chạy lại harness đối chiếu; (3) xuất danh sách bản ghi lệch (id 2 bên) làm đầu vào bảng ánh xạ id merge T3.
Blocked: chờ DB production về local.

## Sau khi có DB chuẩn — việc cần làm (ĐÃ XONG 2026-07-27)
1. [x] Xác minh cơ chế sync HRM→ERP (field mapping) trong code → **companies/departments/parts/employee_infos: giữ nguyên id (identity); employees: match theo `employee_info_id`; teams/working_positions/employee_incomes/company_employees/employee_manage_departments: KHÔNG sync.** Chi tiết file:line trong `reconcile-t3-report.md`.
2. [x] Chạy lại đối chiếu per-table trên DB production.
3. [x] Xuất danh sách bản ghi lệch → `idmap-employees-drift.csv` (454 dòng) + `orphans-departments-erp.csv` (3 dòng).

## KẾT QUẢ ĐỐI CHIẾU T3 (chốt 2026-07-27)
- **4 entity id-aligned tuyệt đối** (companies 8, parts 25, employee_infos 1101, departments 84 khớp id) → erp_id=hrm_id, KHÔNG remap.
- **employees**: match 100% qua email/employee_info_id (2 key trùng khít); **454/1085 lệch id** → bảng ánh xạ id DUY NHẤT cần cho merge T3. Mọi FK `employee_id` phía ERP phải remap qua map này.
- **departments** dư 3 orphan ở ERP: `TEST5` (test sót), 2× `TTDT` (dup) → cần drop/xử.
- pivot `company_employees` (1104/1008), `employee_manage_departments` (235/126): không sync → rebuild/dedupe theo canonical id khi merge.

### Checkpoint — 2026-07-27 (đối chiếu T3 DONE)
Vừa hoàn thành: chạy harness đối chiếu T3 trên **DB production** (hrm_tpe⊕erp2326); verify cơ chế sync trong code (agent Explore). Chốt: chỉ `employees` cần ánh xạ id (454 dòng); 4 entity kia id-aligned. Xuất 2 CSV deliverable + `reconcile-t3-report.md`.
Đang làm dở: —
Bước tiếp: (1) user quyết cách xử 3 orphan departments ERP; (2) tiếp câu treo — chốt biến thể còn dùng (thường/firm/zt-ztec/project/inland) + thứ tự ưu tiên 4 mảng; (3) khi vào phase domain thì đối chiếu T4 (customers…). Harness + my.cnf sẵn trong scratchpad session.
Blocked: —
