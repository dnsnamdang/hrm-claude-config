# Phụ lục — Số liệu cột 49 bảng trùng (ERP vs HRM)

Nguồn: ERP = dev_erp_2 (DB thật); HRM = hrm-api migrations (create+alter). HRM chưa verify bằng DB thật.

| Bảng | ERP cột | HRM cột | Cột chung | % ERP có ở HRM |
|---|---|---|---|---|
| notifications | 11 | 5 | 1 | 9% |
| files | 8 | 26 | 1 | 12% |
| settlement_contracts | 54 | 16 | 11 | 20% |
| moving_norms | 17 | 4 | 4 | 23% |
| groups | 21 | 11 | 6 | 28% |
| quotations | 59 | 80 | 17 | 28% |
| settlement_contract_employees | 15 | 11 | 5 | 33% |
| companies | 76 | 36 | 28 | 36% |
| employee_incomes | 19 | 11 | 7 | 36% |
| customer_has_vehicle_manufacts | 5 | 2 | 2 | 40% |
| job_request_employees | 5 | 3 | 2 | 40% |
| parts | 17 | 10 | 7 | 41% |
| provinces | 14 | 11 | 6 | 42% |
| teams | 11 | 6 | 5 | 45% |
| attachment_types | 6 | 9 | 3 | 50% |
| hamlets | 8 | 4 | 4 | 50% |
| wards | 13 | 11 | 7 | 53% |
| areas | 11 | 6 | 6 | 54% |
| assign_business_tasks | 9 | 19 | 5 | 55% |
| districts | 9 | 11 | 5 | 55% |
| scopes | 7 | 9 | 4 | 57% |
| company_employees | 5 | 7 | 3 | 60% |
| company_roles | 5 | 5 | 3 | 60% |
| customer_activity_types | 5 | 3 | 3 | 60% |
| job_request_details | 5 | 3 | 3 | 60% |
| print_templates | 10 | 8 | 6 | 60% |
| customer_deputies | 8 | 5 | 5 | 62% |
| employee_infos | 80 | 130 | 51 | 63% |
| nations | 11 | 11 | 7 | 63% |
| bank_branches | 6 | 4 | 4 | 66% |
| customer_business_fields | 6 | 6 | 4 | 66% |
| employee_manage_departments | 6 | 8 | 4 | 66% |
| moving_norm_roads | 6 | 6 | 4 | 66% |
| customer_contact_has_bank_accounts | 10 | 7 | 7 | 70% |
| working_positions | 7 | 11 | 5 | 71% |
| customer_has_bank_accounts | 11 | 8 | 8 | 72% |
| delivery_places | 12 | 9 | 9 | 75% |
| moving_norm_road_types | 8 | 8 | 6 | 75% |
| customers | 52 | 53 | 40 | 76% |
| module_mappings | 13 | 10 | 10 | 76% |
| majors | 9 | 7 | 7 | 77% |
| departments | 52 | 55 | 41 | 78% |
| transport_types | 10 | 9 | 8 | 80% |
| banks | 11 | 15 | 9 | 81% |
| customer_contacts | 17 | 14 | 14 | 82% |
| job_requests | 18 | 19 | 16 | 88% |
| failed_jobs | 6 | 7 | 6 | 100% |
| jobs | 7 | 7 | 7 | 100% |
| password_resets | 3 | 3 | 3 | 100% |
