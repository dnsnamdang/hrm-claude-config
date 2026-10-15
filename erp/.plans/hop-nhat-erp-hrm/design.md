# Hợp nhất ERP + HRM — Gộp DB (bước nền)

> Dự án cross-project. Tài liệu đặt ở `ERP/.plans/` vì khảo sát chạy từ context ERP.
> Mục tiêu cuối: 1 project (HRM), 1 DB. Chiến lược: **gộp DB trước** → migrate code ERP→HRM dần → app ERP tắt.

## 1. Mục tiêu & chiến lược (chốt với user 2026-07-27)

- **Gộp DB trước**: dồn bảng ERP vào schema chung với HRM.
- Sau gộp, **app ERP chỉ đổi `DB_DATABASE` là chạy** → điều kiện: **mọi bảng ERP giữ NGUYÊN tên + đủ cột + dữ liệu**.
- Sau đó migrate code ERP→HRM dần; mỗi chức năng xong → tắt route ERP tương ứng.
- Khi ERP tắt hẳn → dọn nốt (bỏ bảng thừa, thống nhất).

## 2. Số liệu khảo sát (dev_erp_2 vs hrm-api migrations)

- **ERP: 1.234 bảng · HRM: 617 bảng · 49 bảng TRÙNG TÊN.**
- 1.185 bảng ERP **không trùng** → đưa thẳng vào schema chung, an toàn.
- Vấn đề nằm ở **49 bảng trùng tên** — xử lý sao để (a) ERP không gãy, (b) HRM không gãy, (c) không trộn nhầm dữ liệu.

## 3. Nguyên tắc "gộp chuẩn"

| # | Nguyên tắc |
|---|---|
| N1 | **ERP giữ nguyên** tên + cột + dữ liệu (để "đổi connection là chạy"). |
| N2 | Bảng trùng **cùng nghĩa + id khớp** → **1 bản dùng chung** (giữ superset cột; ERP thường là superset). |
| N3 | Bảng trùng **khác nghĩa / id KHÔNG khớp** → **tách**: giữ bản ERP nguyên tên, **đổi tên bản HRM** (`hrm_*`) + sửa code HRM (app đích, dễ sửa hơn). |
| N4 | Bảng **framework runtime** (jobs/notifications/…) → cấu trúc giống nhưng **dữ liệu mỗi app riêng** → tách theo app (config table / connection). |
| N5 | **Verify id khớp** cho mọi bảng thuộc N2 trước khi merge (chưa làm — máy hiện không nối được HRM DB). |

## 4. Phân loại 49 bảng trùng (dựa % cột chung + nghĩa)

### Nhóm A — Danh mục / tổ chức: **DÙNG CHUNG** (N2), verify id
Cùng nghĩa, id nhiều khả năng chung (org id đã dùng chung theo ghi nhận trước). Giữ superset cột.
- **Địa lý**: `provinces, districts, wards, hamlets, areas, nations`
- **Tổ chức**: `companies, departments, parts, teams, groups, working_positions, company_employees, company_roles, employee_manage_departments`
- **Ngân hàng/danh mục**: `banks, bank_branches, majors, scopes, transport_types, attachment_types, print_templates, module_mappings, moving_norms, moving_norm_roads, moving_norm_road_types`

→ Với nhóm này: ERP giữ nguyên; HRM trỏ vào **cùng bảng** (nếu id khớp) và bổ sung cột HRM thiếu vào bảng chung (superset).

### Nhóm B — Khách hàng / nhân sự: **CẦN VERIFY id + nghĩa** (rủi ro trộn nhầm)
Giống cột nhiều (76-82%) nhưng phải chắc **cùng tập bản ghi / id khớp**, nếu không → tách.
- `customers` (ERP52/HRM53, chung 40) — ERP=khách bán hàng, HRM=CRM: **verify id có chỉ cùng KH không**
- `customer_contacts, customer_deputies, customer_activity_types, customer_business_fields, customer_has_bank_accounts, customer_contact_has_bank_accounts, customer_has_vehicle_manufacts, delivery_places`
- `employee_infos` (ERP80/HRM130 — HRM superset), `employee_incomes`

→ **Chưa quyết**. Nếu id/tập bản ghi khớp → dùng chung (N2). Nếu lệch → tách (N3, `hrm_*`).

### Nhóm C — Nghiệp vụ: **NGHI KHÁC NGHĨA → nhiều khả năng TÁCH** (N3)
Cột lệch nhiều hoặc nghiệp vụ 2 hệ khác nhau.
- `quotations` (ERP59/HRM80, chung 17 = 28%) — báo giá ERP vs báo giá HRM: **gần chắc khác nghĩa → tách**
- `settlement_contracts` (20%), `settlement_contract_employees`
- `assign_business_tasks` (ERP9/HRM19), `job_requests, job_request_details, job_request_employees`

→ Mặc định **tách** (`hrm_*`) trừ khi verify cho thấy cùng nghĩa.

### Nhóm D — Framework runtime: **TÁCH theo app** (N4)
Cấu trúc ~giống nhưng dữ liệu mỗi app riêng.
- `jobs, failed_jobs, notifications, password_resets, files`

→ Cách: mỗi app cấu hình bảng riêng — ví dụ HRM giữ `jobs`, ERP dùng `erp_jobs` (config `queue.connections.database.table`); `notifications`/`files` tương tự. **Hoặc** đổi tên phía HRM. Quyết theo bên nào ít sửa hơn.

## 5. KẾT QUẢ VERIFY ID KHỚP (2026-07-27, dev_erp_2 ↔ dev_hrm_2 cùng server 127.0.0.1)

| Bảng | ERP | HRM | id chung | Khớp thực thể? | Quyết định |
|---|---|---|---|---|---|
| companies | 7 | 10 | 7 | ✅ cùng cty (khác tên viết tắt) | **DÙNG CHUNG** (union cột+rows) |
| departments | 78 | 102 | 78 (77% tên) | ✅ cùng phòng | **DÙNG CHUNG** |
| provinces | 44 | 45 | 44 (100%) | ✅ hoàn hảo | **DÙNG CHUNG** |
| customers | 38.135 | 19.803 | 19.803 (HRM ⊂ ERP) | ✅ id space chung | **DÙNG CHUNG** (verify fullname trước) |
| banks | 16 | 11 | 11 (64%) | ⚠️ **2 id đụng khác ngân hàng** | **TÁCH/remap** |
| employee_infos | 976 | 884 | 881 (97%) | ⚠️ **~30 id đụng khác người** | **remap 30 id lệch** rồi mới chung |
| quotations | 14 | 41 | 14 (**0%**) | ❌ **id đụng khác báo giá hoàn toàn** | **BẮT BUỘC TÁCH** (`hrm_quotations`) |

**Kết luận then chốt**: danh mục tổ chức/địa lý **id thật sự dùng chung** (HRM sync id từ ERP) → gộp chung an toàn. NHƯNG bảng nghiệp vụ (`quotations`) và một số danh mục (`banks`) **id đụng nhưng khác thực thể** → **gộp mù = trộn nát dữ liệu**. Bắt buộc tách/remap các bảng này.

→ Còn verify: các bảng Nhóm B còn lại (`customer_*`, `settlement_*`, `job_request*`) + fullname `customers` — chạy tương tự trên cùng server.

## 6. Rủi ro / lưu ý

- **Cấu trúc cột lệch**: gộp "dùng chung" phải union cột (thêm cột HRM thiếu vào bảng ERP superset, nullable) — nếu không 1 trong 2 app thiếu cột.
- **id đụng**: nếu 2 hệ có id trùng nhưng khác thực thể (nhất là customers, quotations) → **cấm merge**, phải tách + có thể remap.
- **FK**: bảng ERP tham chiếu bảng chung; nếu bản HRM đổi tên thì FK/code HRM phải theo.
- **Framework**: nếu để 2 app chung `jobs`/`notifications` → lẫn queue/thông báo 2 hệ. Bắt buộc tách runtime.

## 7. Bước tiếp theo

1. **Verify id khớp** Nhóm A + B trên môi trường nối được HRM (chốt bảng nào dùng-chung / tách).
2. Chốt quy ước tên cho bảng tách (đề xuất prefix `hrm_` cho bản HRM).
3. Viết **script gộp** (idempotent, chạy staging trước): tạo schema chung, import bảng ERP, xử lý 49 trùng theo phân loại, union cột nhóm dùng-chung.
4. Đổi `DB_DATABASE` app ERP → test regression. Sửa code HRM cho các bảng đã đổi tên.

## 8. PHÂN LOẠI CUỐI 49 bảng (sau verify id toàn bộ — 2026-07-27)

> Số liệu đầy đủ: `verify-49-idmatch.txt`. Lưu ý: cột định danh phải chọn đúng (nhiều bảng HRM không có `code` → phải so `fullname`/`name`), nếu không sẽ âm tính giả.

### D1 — DÙNG CHUNG (id khớp thực thể cao, remap phần lệch nhỏ)
| Bảng | Khớp | Ghi chú |
|---|---|---|
| provinces, wards, districts, areas | 98-100% | danh mục chuẩn, chung thẳng |
| companies | 100% (code) | HRM +3 cty; union rows+cột |
| departments | 86% | cùng phòng (tên viết khác) |
| parts | cùng bộ phận | lệch chỉ do tiền tố "BP " |
| bank_branches | 87% | |
| customers | **97% (fullname)** | remap ~670 id đụng khác khách |
| employee_infos | **97% (fullname)** | remap ~30 id đụng khác người |

→ Cách gộp: giữ superset cột (ERP), thêm cột HRM thiếu (nullable); union rows; **remap các id đụng-khác-thực-thể** trước khi merge.

### D2 — id KHÔNG đụng → gộp union rows an toàn (HRM rỗng hoặc id rời)
`attachment_types, customer_activity_types, customer_business_fields, customer_contact_has_bank_accounts, customer_has_bank_accounts, customer_has_vehicle_manufacts, delivery_places, employee_incomes, groups, hamlets, majors, module_mappings, moving_norm_road_types, teams, working_positions`

### D3 — ❌ TÁCH: id đụng KHÁC thực thể hoàn toàn (nghiệp vụ 2 hệ khác nhau)
| Bảng | Bằng chứng |
|---|---|
| quotations | ERP `NV.00177…` vs HRM `BG-2026…` (0%) |
| job_requests, job_request_details | 1% / 17% |
| settlement_contracts | 0% |
| print_templates | 0% (mẫu in 2 hệ khác) |
| customer_contacts, customer_deputies | 0% (fullname/name có nghĩa) |
| scopes, transport_types, nations | 0% / 0% / 25% — cần soát nhanh |

→ Cách xử lý: **đổi tên bản HRM → `hrm_*`** + sửa code HRM. ERP giữ nguyên.

### D4 — REVIEW thủ công (bảng pivot/quan hệ, không cột định danh)
`assign_business_tasks, company_employees, company_roles, employee_manage_departments, job_request_employees, settlement_contract_employees, moving_norm_roads, moving_norms`
→ Xem FK trỏ đâu: nếu trỏ bảng D1 (chung id) → có thể chung; nếu trỏ bảng D3 → tách theo.

### D5 — FRAMEWORK runtime (tách theo app)
`jobs, failed_jobs, notifications, password_resets, files`
→ HRM giữ tên gốc; ERP dùng `erp_jobs`/config riêng để không lẫn queue/thông báo/file 2 hệ.

## 9. Kết luận cho quyết định gộp

- **Phần lớn danh mục (D1+D2) gộp chung được** — đúng như bạn nhận định. Chỉ cần remap vài trăm id lệch ở customers/employee_infos.
- **Nhóm D3 (nghiệp vụ) BẮT BUỘC tách** — gộp mù sẽ trộn nát báo giá / phiếu 2 hệ.
- Script gộp phải theo đúng D1-D5, **không gộp đồng loạt**.

## 10. KẾT QUẢ VERIFY D4 (pivot, so theo FK — 2026-07-27)

| Bảng | id chung | FK khớp | Quyết định |
|---|---|---|---|
| assign_business_tasks | 46 | 0% | ❌ TÁCH |
| company_employees | 827 | 4/827 (0%) | ❌ TÁCH (id đụng nhiều nhưng quan hệ khác) |
| company_roles | 34 | 21% | ❌ TÁCH |
| employee_manage_departments | 29 | 0% | ❌ TÁCH |
| job_request_employees | 47 | 0% | ❌ TÁCH (theo `job_requests`) |
| settlement_contract_employees | 1 | 0% | ❌ TÁCH (theo `settlement_contracts`) |
| moving_norm_roads | 2 | 0% | ❌ TÁCH |
| moving_norms | 1 | 100% | DÙNG CHUNG (chỉ 1 bản ghi) |

→ **7/8 pivot phải TÁCH** (`hrm_*`). Bảng quan hệ 2 hệ là 2 tập độc lập dù id đụng.

## 11. TỔNG KẾT CUỐI — 49 bảng trùng (verify 100%)

| Xử lý | Số bảng | Bảng |
|---|---|---|
| **DÙNG CHUNG** (id khớp, remap phần lệch) | ~13 | provinces, wards, districts, areas, companies, departments, parts, bank_branches, customers, employee_infos, moving_norms… |
| **Union an toàn** (id không đụng) | ~15 | attachment_types, delivery_places, groups, hamlets, majors, teams, working_positions… |
| **TÁCH `hrm_*`** (id đụng khác thực thể) | ~18 | quotations, job_requests(+details/employees), settlement_contracts(+employees), print_templates, customer_contacts, customer_deputies, scopes, transport_types, nations, banks, company_employees, company_roles, employee_manage_departments, assign_business_tasks, moving_norm_roads… |
| **Framework** (tách runtime) | 5 | jobs, failed_jobs, notifications, password_resets, files |

**Kết luận**: ~28 bảng gộp chung được, **~23 bảng phải tách/remap**. Script gộp bắt buộc theo phân loại này. Verify 49/49 hoàn tất.

## 12. KHẢO SÁT LẠI TRÊN PRODUCTION (erp_new ↔ hrm_pro, 2026-07-28)

> Dev khác prod nhiều → khảo sát lại trên bản prod (cả 2 đưa về local cùng server, JOIN thật). File: `xu-ly-bang-trung-PROD.xlsx`, `verify-58-prod.tsv`.

**Quy mô prod**: erp_new **1.216** bảng · hrm_pro **639** · **58 trùng tên** (dev chỉ 49).
Prod có thêm bảng trùng quan trọng: `employees, roles, permissions, employee_has_roles, role_has_permissions, migrations, province_mappings, ward_mappings, module_mappings`.

**Phân bố xử lý (58 bảng)**: 15 DÙNG CHUNG · 14 GỘP THẲNG · 23 TÁCH · 6 FRAMEWORK.

**Khác biệt chính so với dev:**
- `customers` **100%** khớp fullname (dev 97%), `employee_infos` **100%** (dev 97%) → dùng chung sạch, ít/không cần remap.
- `customer_contacts`, `customer_deputies`: prod **id chung = 0** → **GỘP THẲNG an toàn** (dev bị đụng phải tách) — ĐẢO NGƯỢC.
- Bảng **mapping** `module_mappings` (ERP 229k), `province_mappings`/`ward_mappings` (100%): ánh xạ id CRM/ERP/HRM → **giữ chung**, không tách.
- `employees` (mới): 79% khớp `employee_info_id` → dùng chung + remap ~168 id lệch.
- `roles`, `permissions`, `role_has_permissions`, `employee_has_roles` (auth): khớp 0% / id không đụng → **tách** (`hrm_*`).
- Nhóm TÁCH nghiệp vụ giữ nguyên: `quotations` 0%, `settlement_contracts` 0%, `job_requests` 1%, `print_templates` 0%, pivot `company_employees`…

**→ Số liệu PROD là bản chính thức để viết script gộp** (dev chỉ tham khảo).

### Checkpoint — 2026-07-28
Vừa hoàn thành: khảo sát lại PROD (erp_new+hrm_pro đưa về local cùng server); verify JOIN thật 58 bảng; build `xu-ly-bang-trung-PROD.xlsx` + `verify-58-prod.tsv`; cập nhật phân loại theo prod (15 chung/14 gộp/23 tách/6 framework).
Bước tiếp: chốt prefix `hrm_` + schema đích → viết script gộp staging (chạy trên local erp_new+hrm_pro trước).
Blocked: chờ user chốt prefix + schema đích.

## 13. QUYẾT ĐỊNH QUEUE (jobs/failed_jobs) — Cách 1: DÙNG CHUNG bảng (2026-07-29)

User chọn dùng chung bảng `jobs`/`failed_jobs` với `QUEUE_CONNECTION=database`, phân biệt app bằng **queue name**:
- **HRM** `config/queue.php`: default queue database `'default'` → `'hrm'` (mọi job HRM chưa set name tự vào 'hrm'; 2 job riêng rice_notifications/sync_faces giữ nguyên). ĐÃ SỬA.
- **ERP** `config/queue.php`: default queue `'default'` → `'erp'`; 2 job hardcode onQueue('default') → 'erp' (DispatchUpdateProductTaxRateChunkJob, DispatchUpdateTaxProductFromGroupChunkJob). ĐÃ SỬA.
- Không cần audit từng dispatch (config default cover hết; đã grep: không có onQueue('default') sót, không onQueue động, không Mail/Notification set queue riêng).

**Worker trên server (BẮT BUỘC tách theo queue name):**
```
ERP: php artisan queue:work database --queue=erp
HRM: php artisan queue:work database --queue=hrm,rice_notifications,sync_faces
```
→ Worker mỗi app chỉ nhặt job queue của mình, không nhặt nhầm class app kia.

**Cập nhật phân loại framework** (khác checkpoint cũ):
- `jobs` → **DÙNG CHUNG** (union, phân biệt cột queue). KHÔNG tách hrm_jobs nữa.
- `failed_jobs` → dùng chung được (cột queue), nhưng id đụng (ERP 65k/HRM 400) → lúc gộp remap id HRM hoặc giữ ERP (log rác). Retry phải chạy đúng app.
- `notifications`, `migrations`, `files`, `password_resets` → VẪN tách hrm_* (payload class riêng / migration riêng).

→ merge_prod.php cần cập nhật: jobs bỏ khỏi nhóm TÁCH, cho vào nhóm dùng-chung (union rows theo queue). (CHƯA sửa script — ghi nhận để cập nhật khi chốt chạy prod.)

## 14. ĐÁNH GIÁ LẠI (2026-07-29) — mục tiêu: BUILD SCHEMA RIÊNG ĐỂ CHECK, log không giữ data

User làm rõ: gộp để build trên schema/instance riêng để CHECK (không đẩy prod); dữ liệu bảng LOG không cần giữ.

### Phân loại lại 58 bảng trùng (góc nhìn check + bỏ log)
- **Gộp thẳng — union theo id, không đụng (26)**: 8 bảng rỗng ≥1 bên (areas, hamlets, majors, teams, working_positions, employee_incomes, employee_has_permissions, customer_contact_has_bank_accounts) + 18 bảng id khớp/không-đụng (customers, companies, departments, wards, employee_infos, provinces, banks, parts, districts, customer_contacts, customer_deputies, groups, moving_norm*, province_mappings, ...).
- **Log — BỎ DATA, chỉ structure (4)**: jobs, failed_jobs, notifications, password_resets. (notifications HRM 711k → bỏ; nếu cần test thì giữ ERP.)
- **migrations — GỘP DATA union theo TÊN (không theo id)**: chỉ 10 tên trùng / 3970+1598. Giữ ERP + thêm 1588 tên HRM chưa có, id mới. An toàn vì bản check không chạy migrate.
- **TÁCH hrm_* — data 2 bên id đụng khác thực thể (~24)**: quotations, roles, permissions, role_has_permissions, employee_has_roles, settlement_contracts(+employees), job_requests(+details/employees), company_employees, company_roles, employee_manage_departments, module_mappings, ward_mappings, customer_activity_types, customer_business_fields, customer_has_*, delivery_places, print_templates, scopes, transport_types, nations, attachment_types, moving_norm_roads, assign_business_tasks, employees(79% khớp→remap).

### files — TÁCH hrm_files (KHÔNG gộp mù)
files 2 bên TRÙNG TÊN nhưng KHÁC BẢN CHẤT: ERP dùng morph (fileable_type=class / fileable_id / path); HRM dùng table/table_id + 17 cột (attachment_type_id, solution_version_*, file_path...). Cách trỏ entity khác nhau → không union được. Với bản check: TÁCH hrm_files.

### DANH SÁCH "CẦN HỢP NHẤT CODE SAU" (không gộp mù ở tầng DB — để giai đoạn migrate code)
Các bảng trùng-tên-KHÁC-bản-chất: muốn dùng chung THẬT phải sửa code + migrate data về 1 cơ chế:
- **files**: HRM đổi table/table_id → morph ERP (sửa ~18 chỗ HRM + model File + migrate 25 dòng + superset cột). ERP dùng morph 99 chỗ → giữ ERP làm chuẩn.
- **notifications**: payload chứa class Notification riêng mỗi app → hợp nhất khi thống nhất notification.
- **quotations / settlement_contracts / job_requests**: nghiệp vụ 2 hệ khác → hợp nhất khi migrate module tương ứng.
- **roles / permissions / role_has_permissions**: auth 2 hệ (spatie) → thống nhất khi hợp nhất phân quyền.
→ Nguyên tắc: gộp DB (giờ) = tách hrm_* để CHECK nhanh. Hợp nhất (dần) = từng bảng đổi code HRM về cấu trúc ERP rồi bỏ hrm_*.

### QUEUE (đã sửa code 2026-07-29) — Cách 1 dùng chung bảng jobs
- HRM config default queue → 'hrm'; ERP → 'erp' (+2 job hardcode 'default'→'erp'). Worker: ERP --queue=erp, HRM --queue=hrm,rice_notifications,sync_faces. jobs/failed_jobs dùng chung, phân biệt cột queue.

### Checkpoint — 2026-07-29 (đánh giá lại)
Vừa hoàn thành: đánh giá lại 58 bảng theo mục tiêu build-check + bỏ-log; xác định migrations gộp được (union tên), files phải tách + hợp nhất code sau; sửa queue Cách 1 (chung bảng jobs).
Bước tiếp: cập nhật merge_prod.php theo đánh giá mới (log bỏ data, migrations union-tên, files tách) rồi build lại schema check. CHƯA làm.
Blocked: —

## 15. BUILD TEST — CÁCH A: lớp VIEW (2026-07-29, ĐÃ LÀM ở local)

User chốt: build test bằng **lớp view** thay vì sửa ~150 điểm code HRM (inventory 2026-07-29: employees ~130 điểm/~75 file, +auth/join rủi ro, +là công tạm sẽ revert khi hợp nhất thật).

**Cơ chế:** schema `hrm_view` chứa 639 view 1-1. 23 bảng TÁCH → view trỏ `<merged>.hrm_*`; còn lại passthrough `<merged>.<tên>`. HRM đổi `DB_DATABASE=hrm_view` (0 dòng code). ERP giữ `DB_DATABASE=<merged>`. View SELECT * 1-1 → CRUD + auto_increment chạy.

**Đã smoke-test local (erp_hrm_check):** đọc count khớp 100%; INSERT/UPDATE/DELETE + LAST_INSERT_ID qua view OK; JOIN 6 view (auth+phân quyền) resolve đúng.

**Deliverable:** `build_hrm_views.sh` (portable), `hrm-view-tables.txt` (snapshot 639 tên bảng HRM — cần vì sau merge hrm_pro rỗng), `HUONG-DAN-VIEW.md` (các bước deploy + .env + worker + giới hạn).

**Giới hạn (bản test OK):** truncate/DDL/migrate không chạy trên view (bản check không seed/migrate); notifications dùng structure ERP (rà nếu test thông báo); view SELECT * đóng băng cột (ALTER bảng đích → chạy lại script). Lớp view là TẠM cho giai đoạn CHECK — hợp nhất thật thì DROP hrm_view.

**Còn lại:** A7 deploy server test (2 DB cùng server → merge → build view → .env 2 app → worker tách queue → boot smoke-test).

## 16. FIX: bảng `notifications` — cấu trúc ERP≠HRM làm HRM login lỗi (2026-07-29)

Triệu chứng: login HRM xong bị "đá ra" ngay. Log: `Unknown column 'notifications.notifiable_type'` khi `$employee_info->unreadNotifications()->count()` (AuthNewController:312) chạy lúc login.
Nguyên nhân: ERP tùy biến bảng `notifications` (url/content/receiver_id/seen...) KHÁC cấu trúc Laravel của HRM (type/notifiable_type/notifiable_id/data/read_at). Merge_prod cũ xếp `notifications` vào nhóm LOG_DROP → giữ cấu trúc ERP, bỏ data HRM → HRM (Notifiable trait) query cột không tồn tại → 500 → FE logout.
Quyết định (user chốt): thông báo KHÔNG cần giữ data → gộp thành 1 bảng `notifications` **cấu trúc HRM, rỗng**.
Đã fix:
- Schema check `erp_hrm_check`: rebuild `notifications` theo cấu trúc HRM (CREATE LIKE hrm_pro) + TRUNCATE (rỗng); bỏ bản ERP.
- `merge_prod.php`: chuyển `notifications` từ LOG_DROP → KEEP_HRM (giữ bảng HRM, drop ERP) + `$EMPTY_AFTER_KEEP=['notifications']` (truncate sau khi giữ). jobs/failed_jobs/password_resets vẫn LOG_DROP (Laravel chuẩn, cấu trúc 2 hệ giống nhau).
Verify: login flow query (unread/permission/list_employee_infos) cho user 13 chạy sạch.
Bài học chung: các bảng trùng tên KHÁC cấu trúc mà HRM-primary (notifications, files) phải giữ cấu trúc HRM; nhóm LOG chỉ an toàn cho bảng Laravel-chuẩn (jobs/failed_jobs/password_resets).

### CẬP NHẬT (2026-07-29): notifications → TÁCH (không phải giữ-cấu-trúc-HRM)
User chốt TÁCH (vì ERP dùng notifications ở RẤT NHIỀU luồng — NotificationHelper, không phải "vài chức năng"):
- `notifications` = cấu trúc ERP (giữ nguyên) → ERP chạy, KHÔNG sửa code ERP.
- `hrm_notifications` = cấu trúc HRM (Laravel), rỗng → HRM trỏ tới.
- HRM code (đã làm): thêm `app/Models/DatabaseNotification.php` (extends Illuminate DatabaseNotification, $table='hrm_notifications'); override `notifications()` ở 2 model notifiable (`app/Models/EmployeeInfo`, `Modules/Timesheet/Entities/EmployeeInfo`) trỏ model mới; `DeleteOldNotification.php` DB::table('notifications')→'hrm_notifications'.
- `merge_prod.php`: notifications chuyển vào $TACH + $EMPTY_AFTER_TACH (truncate hrm_notifications sau tách). LOG_DROP còn jobs/failed_jobs/password_resets.
- Verify: HRM notifications()→hrm_notifications (unread=0); ERP notifications 78719 dòng còn cột receiver_id. php -l sạch.
→ files + notifications: cùng kiểu "trùng tên khác cấu trúc" → đều TÁCH hrm_*.
