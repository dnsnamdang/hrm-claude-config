# Phase 2 — Bản đồ rủi ro 50 bảng trùng tên (ERP ↔ HRM)

> Sinh tự động từ migration (create+alter). Tỉ lệ = |cột nghiệp vụ chung| / min(|ERP|,|HRM|), loại cột audit.

## Tổng hợp (theo tỉ lệ cột thô)

- 🔴 cùng thực thể: **44**
- 🟡 trùng một phần: **3**
- 🟢 va chạm giả: **3**
- ❓ thiếu-data: **0**

> Lưu ý: tỉ lệ dùng `min(|ERP|,|HRM|)` nên bảng stub (1 cột nghiệp vụ) dễ bị đẩy lên 1.0 (vd `moving_norms` 12/1, `attachment_types` 1/7). Dùng bảng phân tầng theo VAI TRÒ dưới đây để lập roadmap, không dùng con số thô.

## ⭐ Phân tầng theo VAI TRÒ (dùng để lập roadmap Phase 2)

**T0 — Khung/Auth (KHÔNG merge; giữ riêng, prefix ERP `tp_`, drop khi ERP retire). Rủi ro dữ liệu = 0.**
`users`, `jobs`, `failed_jobs`, `password_resets`

**T1 — Va chạm GIẢ (khác schema → chỉ rename ERP `tp_`, không trộn rows). Rủi ro thấp.**
`quotations` (HRM Assign đã re-model riêng: 55 vs 57 cột, chỉ 11 chung), `files`, `notifications`, (`groups`, `job_request_employees` — trùng một phần, xử lý như rename + adapter)

**T2 — Danh mục/tham chiếu (cùng thực thể nhưng là catalog: dedupe + remap id, rủi ro thấp–trung).**
`provinces`, `districts`, `wards`, `nations`, `areas`, `hamlets`, `banks`, `bank_branches`, `majors`, `transport_types`, `moving_norm_road_types`, `moving_norm_roads`, `moving_norms`, `customer_activity_types`, `customer_business_fields`, `customer_has_vehicle_manufacts`, `attachment_types`, `print_templates`, `module_mappings`, `scopes`, `company_roles`

**T3 — Lõi tổ chức/nhân sự (cùng thực thể, FK phủ khắp hệ → RỦI RO CAO NHẤT, remap id lan rộng).**
`companies`, `departments`, `parts`, `teams`, `working_positions`, `employee_infos`, `employee_incomes`, `employee_manage_departments`, `company_employees`

**T4 — Nghiệp vụ KH/HĐ (cùng thực thể, gắn trực tiếp 4 mảng migrate).**
`customers`, `customer_contacts`, `customer_deputies`, `customer_has_bank_accounts`, `customer_contact_has_bank_accounts`, `delivery_places`, `settlement_contracts`, `settlement_contract_employees`, `job_requests`, `job_request_details`, `assign_business_tasks`

### Nhận định chiến lược
- **HRM về bản chất là một bản FORK/re-model một phần của ERP** (44/50 bảng trùng là cùng thực thể — master data, customers, employees, companies đã được copy dần sang HRM). Đây KHÔNG phải 2 hệ xa lạ.
- Nút thắt rủi ro cao nhất là **T3 (lõi tổ chức: companies/departments/employee_infos)** — vì `company_id`/`department_id`/`employee_id` là FK phủ gần như mọi bảng. Merge nhầm ở đây phá dữ liệu diện rộng.
- **Tin tốt:** phần lớn ~165 bảng của 4 mảng cần migrate (accounts, receipts, contracts, firm_contracts, service_contracts…) **KHÔNG nằm trong 50 bảng trùng** → bê sang giữ nguyên tên, không va chạm. Chỉ số ít (T4 + `quotations` rename) cần xử lý.

| Loại | Bảng | Cột ERP | Cột HRM | Chung | Tỉ lệ |
|---|---|---:|---:|---:|---:|
| 🔴 cùng thực thể | `areas` | 6 | 4 | 4 | 1.0 |
| 🔴 cùng thực thể | `attachment_types` | 1 | 7 | 1 | 1.0 |
| 🔴 cùng thực thể | `bank_branches` | 3 | 3 | 3 | 1.0 |
| 🔴 cùng thực thể | `banks` | 4 | 9 | 4 | 1.0 |
| 🔴 cùng thực thể | `company_employees` | 2 | 4 | 2 | 1.0 |
| 🔴 cùng thực thể | `company_roles` | 2 | 2 | 2 | 1.0 |
| 🔴 cùng thực thể | `customer_activity_types` | 2 | 2 | 2 | 1.0 |
| 🔴 cùng thực thể | `customer_business_fields` | 3 | 3 | 3 | 1.0 |
| 🔴 cùng thực thể | `customer_contact_has_bank_accounts` | 7 | 7 | 7 | 1.0 |
| 🔴 cùng thực thể | `customer_contacts` | 12 | 12 | 12 | 1.0 |
| 🔴 cùng thực thể | `customer_deputies` | 3 | 3 | 3 | 1.0 |
| 🔴 cùng thực thể | `customer_has_bank_accounts` | 8 | 8 | 8 | 1.0 |
| 🔴 cùng thực thể | `customer_has_vehicle_manufacts` | 2 | 2 | 2 | 1.0 |
| 🔴 cùng thực thể | `delivery_places` | 7 | 7 | 7 | 1.0 |
| 🔴 cùng thực thể | `employee_manage_departments` | 3 | 4 | 3 | 1.0 |
| 🔴 cùng thực thể | `failed_jobs` | 5 | 6 | 5 | 1.0 |
| 🔴 cùng thực thể | `hamlets` | 5 | 3 | 3 | 1.0 |
| 🔴 cùng thực thể | `job_request_details` | 2 | 2 | 2 | 1.0 |
| 🔴 cùng thực thể | `job_requests` | 13 | 16 | 13 | 1.0 |
| 🔴 cùng thực thể | `jobs` | 5 | 5 | 5 | 1.0 |
| 🔴 cùng thực thể | `majors` | 6 | 4 | 4 | 1.0 |
| 🔴 cùng thực thể | `module_mappings` | 8 | 8 | 8 | 1.0 |
| 🔴 cùng thực thể | `moving_norm_road_types` | 5 | 5 | 5 | 1.0 |
| 🔴 cùng thực thể | `moving_norm_roads` | 3 | 3 | 3 | 1.0 |
| 🔴 cùng thực thể | `moving_norms` | 12 | 1 | 1 | 1.0 |
| 🔴 cùng thực thể | `nations` | 7 | 6 | 6 | 1.0 |
| 🔴 cùng thực thể | `password_resets` | 2 | 2 | 2 | 1.0 |
| 🔴 cùng thực thể | `scopes` | 2 | 7 | 2 | 1.0 |
| 🔴 cùng thực thể | `teams` | 10 | 4 | 4 | 1.0 |
| 🔴 cùng thực thể | `transport_types` | 5 | 5 | 5 | 1.0 |
| 🔴 cùng thực thể | `users` | 4 | 4 | 4 | 1.0 |
| 🔴 cùng thực thể | `working_positions` | 2 | 8 | 2 | 1.0 |
| 🔴 cùng thực thể | `parts` | 15 | 8 | 7 | 0.88 |
| 🔴 cùng thực thể | `customers` | 51 | 43 | 37 | 0.86 |
| 🔴 cùng thực thể | `assign_business_tasks` | 6 | 18 | 5 | 0.83 |
| 🔴 cùng thực thể | `districts` | 6 | 6 | 5 | 0.83 |
| 🔴 cùng thực thể | `provinces` | 8 | 6 | 5 | 0.83 |
| 🔴 cùng thực thể | `wards` | 6 | 6 | 5 | 0.83 |
| 🔴 cùng thực thể | `departments` | 47 | 50 | 38 | 0.81 |
| 🔴 cùng thực thể | `employee_incomes` | 15 | 5 | 4 | 0.8 |
| 🔴 cùng thực thể | `print_templates` | 5 | 6 | 4 | 0.8 |
| 🔴 cùng thực thể | `companies` | 77 | 33 | 26 | 0.79 |
| 🔴 cùng thực thể | `employee_infos` | 75 | 94 | 48 | 0.64 |
| 🔴 cùng thực thể | `settlement_contracts` | 50 | 13 | 8 | 0.62 |
| 🟡 trùng một phần | `groups` | 17 | 8 | 4 | 0.5 |
| 🟡 trùng một phần | `job_request_employees` | 2 | 2 | 1 | 0.5 |
| 🟡 trùng một phần | `settlement_contract_employees` | 12 | 10 | 4 | 0.4 |
| 🟢 va chạm giả | `files` | 5 | 14 | 1 | 0.2 |
| 🟢 va chạm giả | `quotations` | 55 | 57 | 11 | 0.2 |
| 🟢 va chạm giả | `notifications` | 7 | 3 | 0 | 0.0 |
