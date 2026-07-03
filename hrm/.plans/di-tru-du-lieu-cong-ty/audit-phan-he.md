# Audit thiết lập theo phân hệ — Di trú công ty (nguồn → đích)

> Mục đích: trả lời "khi chuyển data nguồn về đích, cái nào CHUYỂN ĐƯỢC (riêng theo công ty), cái nào DÙNG CHUNG của đích cũ (global)". Cập nhật 2026-06-20.

## Nguyên tắc phân loại (3 nhóm)

| Nhóm | Ý nghĩa | Số bảng | Cách xử lý |
|------|---------|---------|-----------|
| **OWNED** (riêng theo công ty) | Có `company_id` → cấu hình/dữ liệu của riêng công ty | **94** | **CHUYỂN** sang đích thành company_id mới (id liền mạch + map FK) |
| **SHARED** (dùng chung) | Danh mục toàn hệ thống, KHÔNG có company_id | **9** | **DÙNG CỦA ĐÍCH** — map natural-key, KHÔNG chèn |
| **SKIP** (giao dịch/global config) | Giao dịch theo kỳ HOẶC config global (không company_id) | **185** | **KHÔNG chuyển** |

**SHARED (9)** = `nations, provinces, districts, wards` (địa lý), `banks`, `majors`, `areas`, `permissions`, `system_salary_compositions`. → Công ty mới dùng chung danh mục địa lý/ngân hàng/quyền của đích.

**Quy tắc vàng**: bảng **CÓ `company_id`** = riêng → chuyển; **KHÔNG `company_id`** = chung → dùng của đích. (Đã verify: master_settings/print_templates/meeting_types/bom_price_approval_configs đều không có company_id → global → skip đúng.)

---

## Đánh giá theo phân hệ

### 1. Chấm công (Timesheet) — `/timesheet/setting`
| Thiết lập | Bảng | Nhóm | Trạng thái cty9 |
|-----------|------|------|-----------------|
| Ca làm việc | working_shifts (+details) | OWNED | ✅ chuyển |
| Phân ca (mẫu) | shift_details | OWNED | ✅ chuyển (8) |
| Phân ca chi tiết (membership + roster) | shift_detail_employees, shift_detail_employee_dates | OWNED* | ✅ **Phase 6f** (101 + 25025 roster tương lai) |
| Ngày lễ | holidays | OWNED | ✅ chuyển |
| Loại nghỉ phép | leave_types | OWNED | ✅ chuyển |
| Quy định theo dõi chấm công | attendance_watch_regulations | OWNED | ✅ chuyển |
| Đi muộn/về sớm | late_early_outs | OWNED | ✅ chuyển |
| Miễn chấm công | timekeeping_exemptions | OWNED | ✅ chuyển (2) — **Phase 6g fix crash + orphan** |
| Cắt phép | truncated_leaves (+excepts) | OWNED | ✅ chuyển |
| Tăng ca (quy định) | overtime_regulations | OWNED | ✅ chuyển |
| Địa điểm / kết nối chấm công | locations, location_conn_infos, conn_infos | OWNED | ✅ chuyển |
| Thiết bị chấm công | devices | OWNED | ✅ chuyển |
| **Số dư phép** | employee_attendances | OWNED | ✅ chuyển (có guard recompute — Phase 6b) |
| Chấm công kỳ cũ (kết quả) | timesheet_summaries, timesheets, attendances | SKIP | ❌ không chuyển (giao dịch) — đúng |
| Cấu hình hệ thống chung | master_settings | SKIP (global) | dùng của đích |

### 2. Lương (Payroll) — `/payroll/setting`
| Thiết lập | Bảng | Nhóm | Trạng thái |
|-----------|------|------|-----------|
| Thành phần lương | salary_compositions | OWNED | ✅ chuyển |
| Mẫu bảng lương | salary_templates | OWNED | ✅ chuyển |
| Cấu hình bảo hiểm | insurance_configs | OWNED | ✅ chuyển |
| Số dư lương hiệu lực | employee_salary_histories (+allowances/missions) | OWNED | ✅ chuyển |
| Thành phần lương HỆ THỐNG | system_salary_compositions | SHARED | dùng của đích |
| Bảng lương kỳ cũ | salary, salary_employees, payments... | SKIP | ❌ giao dịch — đúng |

### 3. Nhân sự (Human) — `/human` + cơ cấu tổ chức
| Thiết lập | Bảng | Nhóm | Trạng thái |
|-----------|------|------|-----------|
| Khối/Phòng/Bộ phận/Nhóm | departments, parts, teams, groups | OWNED | ✅ chuyển |
| Chức danh / vị trí / ngạch / năng lực | titles, working_positions, ranks, competencies | OWNED | ✅ chuyển |
| Định biên | department_manpowers (+con) | OWNED | ✅ chuyển |
| Hồ sơ nhân sự + con | employee_infos, educations, relationships, working_histories... | OWNED | ✅ chuyển (123; loại 1 DNS Admin trùng email — đúng) |
| Loại HĐ (danh mục) | labor_contracts | OWNED | ✅ chuyển |
| Khen thưởng (danh mục) | reward_conditions, reward_modes, attachment_types... | OWNED | ✅ chuyển |
| **Khách hàng + Lĩnh vực KH + Nhóm ngành** | customers, customer_scopes, scopes, industries, industry_scopes | OWNED* | ✅ **Phase 6d** (1+59+19+117+118) |
| Chuyên ngành / khu vực | majors, areas | SHARED | dùng của đích |
| Địa lý (tỉnh/huyện/xã/quốc gia) | provinces/districts/wards/nations | SHARED | dùng của đích |
| Ngân hàng | banks | SHARED | dùng của đích |

### 4. Phân quyền — `/timesheet/setting/roles`
| Thiết lập | Bảng | Nhóm | Trạng thái |
|-----------|------|------|-----------|
| Vai trò | roles | OWNED | ✅ chuyển (4, hậu tố " (ETEK GREEN)") |
| Gán quyền cho vai trò | role_has_permissions | OWNED (id-less) | ✅ chuyển — **Phase 6e hạ "tổng công ty"→"theo công ty"** |
| Gán vai trò cho NV | employee_has_roles | OWNED (id-less) | ✅ chuyển (22) |
| Tài khoản đăng nhập | employees | OWNED | ✅ chuyển (122) |
| **Danh mục quyền** | permissions | SHARED | dùng của đích (khớp 100% theo name) |

### 5. Đào tạo (Training)
| Thiết lập | Bảng | Nhóm | Trạng thái |
|-----------|------|------|-----------|
| Danh mục đào tạo (loại/môn/giảng viên/đề thi) | training_types, subjects, teachers, exam_kits, questions... | OWNED | ✅ chuyển (cờ MIGRATE_TRAINING=true) |
| Khóa học/kết quả thi/đánh giá (giao dịch) | courses, exam_test_results, evaluation_* | SKIP | ❌ giao dịch — đúng |

### 6. Giao việc (Assign) / CRM
| Thiết lập | Bảng | Nhóm | Trạng thái |
|-----------|------|------|-----------|
| Danh mục KH/Ngành (xem mục 3) | customer_scopes, scopes, industries | OWNED* | ✅ Phase 6d |
| Dự án/giải pháp/báo giá/meeting (giao dịch) | prospective_projects, solutions, quotations, meetings... | SKIP | ❌ giao dịch — đúng (cty nguồn không dùng workflow: 0 dự án) |

### 7. Quyết định (Decision)
| Thiết lập | Bảng | Nhóm | Trạng thái |
|-----------|------|------|-----------|
| Bảo hiểm/phúc lợi (config) | benefit_generals... | OWNED phần config | ✅ |
| Quyết định/HĐLĐ/phụ lục (giao dịch) | decisions, decision_labor_contracts, appendix_labor_contracts | SKIP | ❌ giao dịch — đúng |
| Mẫu in | print_templates | SKIP (global) | dùng của đích |

\* OWNED* = ban đầu skip, đã chuyển sang owned trong các phase fix.

---

## Các GAP đã phát hiện & xử lý

| # | Gap | Nguyên nhân | Xử lý |
|---|-----|-------------|-------|
| Phase 6 | NP còn lại thổi phồng | "đã dùng" tính từ timesheet_summaries (skip) | fold vào number_day_leave_outside |
| Phase 6b | Cron update:attendance đạp số dư | recompute từ timesheet_summaries rỗng | guard leave_recompute_skip |
| Phase 6d | /human/customers + danh mục KH/Ngành rỗng | bỏ nhầm theo cụm "CRM" | đưa 6 bảng sang owned (MIGRATE_CRM) |
| Phase 6e | NV di trú xem chéo công ty khác | quyền "tổng công ty" (query không lọc) | hạ → "theo công ty" |
| Phase 6f | Phân ca rỗng | con của shift_details bị skip | đưa membership + roster tương lai |
| **Phase 6g** | **Miễn chấm công crash (500)** | (1) resource không guard null employee; (2) dòng của DNS Admin bị loại → orphan FK NULL | fix resource null-guard + xóa orphan + **engine cascade loại child theo người bị loại** (personOwnerFkColumns) |

### 8. Cơm (Rice) — `/rice` — ĐẶC BIỆT: đã tập trung ở DB TPE
Khác mọi phân hệ trên: **mọi bảng `rice_*` nằm ở DB TPE** (connection `mysql_tpe`), KHÔNG ở DB nguồn HR. Phân vùng theo `rice_companies.parent_id` (TPE=1, ETEK GREEN=2...), KHÔNG bằng DB riêng.

| Khía cạnh | Xử lý |
|-----------|-------|
| rice_* trong di trú HR | SKIP — đúng (không ở DB nguồn HR) |
| Liên kết rice ↔ HR mới | **Re-link riêng** (Phase 6h): command `company:relink-rice` dịch FK HR cũ→mới qua migration_id_map + re-tag parent 2→1, company_id→9 |
| Đã re-link | rice_company (1), rice_employee_infos (50), rice_departments (5), rice_registrations (350), rice_menu_day_companies (4) → link sống về cty9 |
| Config (settings/menus) | **DÙNG CONFIG TPE — tự động**: rice_settings GLOBAL (query theo column_name, không company_id); rice_menus/menu_days CENTRAL (company_id=1); menu thường global theo ngày. ETEK GREEN vốn đã dùng chung config trung tâm này (cùng mysql_tpe). Company 9 tự thừa hưởng → KHÔNG cần migrate config |
| Vận hành khi gộp | gỡ domain cổng thành viên khỏi `RICE_REGISTER_DOMAINS`; ssn dải 10001(TPE)/30001(EG) tránh đụng; rà `USE_COMMON_CATALOG` cho working position |

→ **Bài học cho công ty thành viên SAU**: ngoài di trú HR, phải chạy thêm `company:relink-rice --rice-parent=<portal cũ> --new-parent=1 --run=<runId> --new-company=<id mới>` để gộp cơm vào tenant TPE.

## Kết luận
- **94 bảng OWNED**: đối chiếu nguồn↔đích KHỚP 100% (chỉ lệch DNS Admin trùng email bị loại — đúng chủ ý). Mọi thiết lập per-company đã chuyển.
- **9 bảng SHARED**: dùng danh mục dùng-chung của đích (địa lý/bank/quyền/ngành nghề) — đúng thiết kế.
- **185 bảng SKIP**: giao dịch theo kỳ + config global (không company_id) — không chuyển, đúng.
- Engine fix Phase 6g (cascade loại child theo người bị loại) ngăn orphan cho công ty di trú SAU.
