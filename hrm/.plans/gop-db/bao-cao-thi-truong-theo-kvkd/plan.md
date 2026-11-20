# Báo cáo thị trường theo KVKD — Implementation Plan (#12091 + #11888)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development hoặc superpowers:executing-plans. Checkbox `- [ ]`.

**Goal:** Chiều thị trường của 8 báo cáo CSKH trước bán đổi sang Tỉnh → Khu vực kinh doanh (KVKD).
**Architecture:** 1 helper BE `CustomerBusinessArea` (join/resolve KVKD theo phường/xã của KH, tỉnh theo luật L1) + 1 util FE
`utils/business-area-options.js`; từng báo cáo sửa service + FE của riêng nó, giữ nguyên khuôn/quy ước sẵn có của màn đó.
Phát triển thị trường thêm snapshot `meetings.business_area_*`.
**Tech Stack:** Laravel 8 / PHP 7.4 / MySQL (DB gộp), Nuxt 2 / Vue 2, PHPUnit (DB local thật + `DatabaseTransactions`), Playwright MCP.
**Spec:** `docs/superpowers/specs/gop-db/2026-11-20-bao-cao-thi-truong-theo-kvkd-design.md` (đọc kèm; mục 3 = luật L1–L6, 4.3 = bảng R1–R8).
**Mockup R5:** `.plans/gop-db/bao-cao-thi-truong-theo-kvkd/mockup-11888-phan-chia-thi-truong.html`.

## Global Constraints
- Code ở nhánh `task_12091` (hrm-api + hrm-client). **Không commit / push** — user tự commit (CLAUDE.md). Bước "commit" trong task = báo lại danh sách file.
- Không dùng `DB_DATABASE_SECOND` / `mysql2` (CLAUDE.md gop_db mục 3).
- Nhãn: "Chưa xác định khu vực" (R1–R4, R6–R8) · "Chưa xác định thị trường" (giữ) · cột/ô lọc "Khu vực kinh doanh" (bảng hẹp: "Khu vực KD").
- Số theo chuẩn `1,234,567`; ô rỗng để trống; ô lọc floating không placeholder trùng nhãn (CLAUDE.md).
- Báo cáo: theo skill `report-styles`; Excel BE theo skill `export-excel`; in theo skill `print-page`; ô chọn theo `select-and-input-state`.
- Test BE tự tạo KVKD trên **phường/xã chưa thuộc KVKD nào** (UNIQUE `business_area_wards.ward_id`), trong `DatabaseTransactions`.
- Chạy test: trong repo đang checkout `task_12091`: `php artisan test --filter <Tên>`.

## Review Focus
1. KH có phường/xã thuộc KVKD ở **tỉnh khác** tỉnh KH ⇒ KVKD phải nằm dưới tỉnh của KVKD, không dưới tỉnh KH (Task 1 + từng báo cáo có 1 test).
2. Lọc "Chưa xác định khu vực" phải theo **cặp tỉnh** — chọn tỉnh A + chưa xác định không được kéo KH tỉnh B (Task 3, 5, 6).
3. KVKD đã khoá: R1–R4/R6–R8 vẫn hiện tên; R5 loại hẳn (Task 7).
4. Phát triển thị trường: dòng giả trong test cũ không có `business_area_*` ⇒ đọc `?? null`, test cũ không vỡ (Task 4).
5. Đếm tổng / phân trang đi đường nhanh SQL phải tính cả lọc KVKD (Meeting theo TT, `getTotalMeetings`) (Task 5).

---

## Phase 0 — Chuẩn bị
- [x] Checkout `task_12091` ở **repo chính** hrm-api + hrm-client (user chốt 20/11), `git status` sạch, `merge --ff-only origin/gop_db` nếu gop_db đã đi tiếp.
- [x] DB local: tạo dữ liệu thử tay (3 KVKD ở 2 tỉnh, 1 KVKD khoá, 1 KH lệch tỉnh) bằng script trong scratchpad — dùng cho kiểm FE, xoá sau.

## Phase 1 — Nền dùng chung

### Task 1: Helper BE `CustomerBusinessArea`
**Files:** Create `hrm-api/Modules/Assign/Support/CustomerBusinessArea.php` · Test `hrm-api/tests/Unit/CustomerBusinessAreaTest.php`
**Interfaces — Produces** (spec 4.1):
- `const UNKNOWN_NAME = 'Chưa xác định khu vực'`
- `join($q, string $customerAlias = 'c', string $as = 'ba')` — leftJoin `business_area_wards {$as}w` + `business_areas {$as}`, không lọc status
- `provinceExpr(string $customerAlias = 'c', string $as = 'ba'): string` → `COALESCE({$as}.province_id, {$customerAlias}.province_id)`
- `whereArea($q, $areaId, string $as = 'ba')` — số ⇒ `= ?`; `null`/`'__none__'`/`0` ⇒ `IS NULL`
- `resolve(array $customerIds): array` — `[customer_id => ['province_id','province_name','business_area_id','business_area_name','business_area_locked']]`, 1 query/1000 id
- [x] Test (fail trước): `test_kh_lech_tinh_lay_tinh_cua_kvkd` (KH tỉnh A, xã thuộc KVKD tỉnh B ⇒ province_id = B) · `test_kh_khong_thuoc_kvkd` (area null, tỉnh KH) · `test_kvkd_khoa_van_ra_ten` (`business_area_locked = true`) · `test_where_area_null_lay_kh_chua_xac_dinh`.
- [x] Viết helper → test pass.

### Task 2: Util FE `business-area-options.js`
**Files:** Create `hrm-client/utils/business-area-options.js`
**Interfaces — Produces:** `fetchBusinessAreas(store, provinceId = null)` (gọi `assign/customers/business-areas?filter_usage=customer_picker[&province_id]`, trả mảng `{id,name,province_id,is_locked}`) · `areasOfProvince(list, provinceIds)` · `dropStaleArea(filters, list, areaKey = 'business_area_id', provinceKey = 'province_id')`.
Pattern copy: `components/modals/ChooseErpCustomerModal.vue:206-281` (ô Tỉnh + KVKD, tải KVKD theo tỉnh).
- [x] Viết util; kiểm qua màn đầu tiên dùng nó (Task 8).

## Phase 2 — Phát triển thị trường + snapshot (R4)

### Task 3: Snapshot KVKD của meeting
**Files:** Create `hrm-api/database/migrations/2026_11_20_000001_add_business_area_columns_to_meetings_table.php` · Modify `Modules/Assign/Services/MeetingMarketSnapshotService.php:35-72`, `Modules/Assign/Entities/Meeting/Meeting.php:43-77`, `Modules/Assign/Database/Seeders/BackfillMeetingProvinceSeeder.php` · Test `tests/Unit/MeetingAreaSnapshotTest.php`
**Interfaces:** Consumes `CustomerBusinessArea::resolve`. Produces cột `meetings.business_area_id` (index `meetings_business_area_id_index`), `meetings.business_area_name`; `resolveForCustomer()` trả thêm 2 khoá; tỉnh theo L1.
- [x] Test: `test_luu_meeting_ghi_cap_tinh_kvkd` · `test_doi_khach_hang_resolve_lai` · `test_meeting_cu_thieu_kvkd_luu_lai_tu_bu` · `test_seeder_vá_meeting_thieu_kvkd_va_thieu_tinh` · `test_kh_khong_kvkd_de_null`.
- [x] Migration idempotent (khuôn `2026_09_14_000001`) → `php artisan migrate` local.
- [x] Hook: điều kiện `empty(province_id) || empty(business_area_id) || isDirty('customer_id')`, ghi cặp. Seeder: `$needsFix` thêm `whereNull('business_area_id')`, update theo cặp.
- [x] Test pass; chạy seeder local, đếm meeting còn thiếu. (20/11: 37 test xanh; seeder local vá 535 meeting thiếu tỉnh, 13s)

### Task 4: Báo cáo Phát triển thị trường — dim `area`
**Files:** Modify `Modules/Assign/Services/Report/CustomerMarketDevelopmentService.php` (CRITERIA :70-86, DIM_LABEL :89, getFilteredQuery :289, attachOrganisation :415, getNewCustomerRows :476-522, dimensionOf :676, drill :1003-1392, describeNodePath :1428), `CustomerMarketDevelopmentPrintService.php` (DETAIL_COLUMNS :60-80, describeFilters :358), `Export/CustomerMarketDevelopmentDrillExport.php:22` · FE `pages/assign/report/customer-market-development/index.vue` (criteriaOptions :241, filter :140/:281, loadProvinces :376), `components/DevelopmentDrillModal.vue` (FILTER_FIELDS :281, ALLOC_DIMS :297, DIM_LABEL :302, FIELD_MAP :323, columns :538) · Test `tests/Unit/CustomerMarketDevelopmentAreaTest.php` + chạy lại `tests/Unit/CustomerMarketDevelopment*Test.php`.
**Interfaces:** `UNKNOWN_AREA_KEY = '__no_area__'`; dims `mk` = `['market','area','dept','part','host']`, `dp` = `['dept','part','host','market','area']`; head thêm "Khu vực kinh doanh"; request `business_area_id`, drill `p_business_area_id`; khoá area trong drill/chip luôn kèm province (Review Focus 2).
- [x] Test: `test_cay_mk_co_cap_kvkd_duoi_tinh` · `test_kvkd_chua_xac_dinh_xep_cuoi` · `test_loc_business_area_id` · `test_kh_moi_theo_L1`.
- [x] Code BE → test mới + cũ pass.
- [x] FE + kiểm Playwright (ảnh: tiêu chí Thị trường bung tới KVKD; popup có chip/cột KVKD; Excel popup mở được).

## Phase 3 — Các báo cáo có sẵn chiều thị trường

### Task 5: Kết quả meeting theo thị trường (R3)
**Files:** `Modules/Assign/Services/Report/MeetingByMarketService.php` (resolveCustomerProvinces :228-262 → dùng `CustomerBusinessArea::resolve`, bỏ `DB_DATABASE_SECOND`; attachProvinceInfo :469; getSortedFlatMeetings :526-560; getTotalMeetings :839; buildGroupedStructure :667; getSummary :864; getFlatRowsForExport :576), `resources/views/exports/assign/meeting_by_market_report.blade.php` · FE `meeting-by-market/index.vue`, `components/MeetingByMarketTable.vue` (allRows :431, collapse :389-550), `components/MeetingByMarketSummary.vue` · Test `tests/Feature/MeetingByMarket/AreaTest.php` (mới).
**Interfaces:** request `business_area_id` (`'__none__'` = chưa xác định, đi kèm `province_id`); cây `groups[].areas[].customers[].meetings[]`; summary thêm `by_business_area: [{province_name, business_area_id, business_area_name, total}]`.
- [x] Test: `test_cay_tinh_kvkd_kh` · `test_loc_kvkd_dem_tong_dung` (đường nhanh :842) · `test_khong_doc_db_erp_cu` · `test_excel_co_cot_kvkd`.
- [x] BE → FE (loại dòng `area`, thu gọn riêng, STT) → Playwright ảnh.

### Task 6: Tổng hợp nhu cầu làm dịch vụ (R2)
**Files:** `Modules/Assign/Services/Report/ServiceDemandReportService.php` (FILTERS :33, scopedQuery :80-128, joinedQuery :131, withRowColumns :164, ordered :177, toRow :220, index :257-310, filterOptions :364-434), `resources/views/exports/assign/service_demand_report.blade.php` + `service_demand_list.blade.php`, `resources/views/prints/assign/service_demand_summary.blade.php` + `service_demand_detail.blade.php` · FE `service-demand/index.vue`, `components/DemandTable.vue`, `DemandSummary.vue`, `DemandListModal.vue` · Test sửa `tests/Feature/ServiceDemand/ReportApiTest.php`.
**Interfaces:** shape `groups[{province_id, province_name, …, areas[{business_area_id, business_area_name, needs, quotations, contracts, customers[]}]}]`; summary thêm `business_areas` (không đếm nhóm chưa xác định); popup tham số `ar` (0 = chưa xác định, như `pv`); filter-options thêm `business_areas[{id,name,parent_id}]`; phân trang vẫn theo tỉnh.
- [x] Sửa assert cũ (khoá summary/group/row/filter-options, tiêu đề Excel) + test mới `test_ar_0_chi_lay_kh_chua_kvkd_trong_tinh`.
- [x] BE (4 nơi cây cứng: service, 2 blade, FE) → FE level 3 + STT i.j.k → Playwright ảnh + Excel/in.

### Task 7: Kết quả CSKH tiềm năng (R1)
**Files:** `Modules/Assign/Services/Report/PotentialCustomerCareService.php` (DRILL_COLUMNS :50-60 `'ward'` → `'barea' => 'business_area_id'`, attachCustomerMarket :272-312 → helper + bỏ `DB_DATABASE_SECOND`, applyMarketFilter :381, buildSections :599, applyDrillFilters :867, crossStats $hiddenOf :935, describe* :1038/:1100, filterOptions :1161), `Transformers/PotentialCustomerCareResource/CustomerDemandRowResource.php:32`, `Export/PotentialCustomerCareDemandExport.php` + blade `potential_customer_care_demands`, print `potential_customer_care_detail` · FE `potential-customer-care/index.vue` (:221, :407-444, :506, :555), `components/CareTrackingTable.vue` (SECTION_DIMS :221, LEVEL_LABELS :227), `components/DemandListModal.vue` (:172, :263, :288, :410, :538, :563, :591) · Test `tests/Unit/PotentialCustomerCareAreaTest.php`.
- [x] Test: `test_phan_thi_truong_tinh_roi_kvkd` · `test_loc_business_area_id` · `test_drill_key_market_barea`.
- [x] BE → FE → Playwright ảnh (phần II, ô lọc, popup, Excel chi tiết).

### Task 8: Phân chia thị trường (R5, #11888 — theo mockup)
**Files:** `Modules/Assign/Services/Report/DivisionMarketReportService.php` (viết lại baseQuery :242-287 nguồn phiếu NV; getData :44-92 phân trang 15 tỉnh; orderedRows :341; buildTree :357; mapRow :393; printTable :111; applyFilters :289; buildFilterOptions :206, cache `_v3`) · FE `division-market/index.vue`, `components/export-excel.js` · Test `tests/Feature/DivisionMarket/ReportTest.php` (mới, dựng chuỗi `dmde→dme→dmep→dmew` + KVKD).
**Interfaces:** cây `provinces[{province_id, province_name, area_count, areas[{business_area_id, name, ward_count, ward_names[], departments[{id, name, employee_count, employees[{employee_label, phone, in_charge, vehicle_name}]}]}]}]`; filter `business_area_ids[]` thay `ward_ids[]`.
- [x] Đọc mockup (mở file HTML, chụp màn "Phân chia thị trường" + "Ghi chú") — bám bố cục, STT, ô "Hiển thị đến cấp".
- [x] Test: `test_chi_lay_phieu_nv_da_duyet` · `test_kvkd_khoa_bi_loai` · `test_tinh_theo_kvkd` · `test_phu_trach_tat_ca_hang_la_min` · `test_loc_kvkd_fallback_phieu_cu` · `test_phan_trang_15_tinh`.
- [x] Đo thời gian query trên DB local (id_ward VARCHAR) — >2s thì thêm index trước khi tiếp.
- [x] BE → FE → Playwright ảnh so với mockup + Excel + In. (20/11: user chốt dựng cây theo mockup; giữ tìm nhanh; Cấu hình cột còn 3 cột dữ liệu)

## Phase 4 — Thêm lọc Tỉnh + KVKD (R6–R8)

### Task 9: Tổng hợp CSKH tiềm năng (R6)
**Files:** `PotentialCustomerTrackingService.php` (join sau `c` :135 + :200, `applySqlFilters` :270, dòng KH `salesNodes` :507, `filterOptions` :656), `PotentialCustomerTrackingPrintService.php` (describeFilters :182, DETAIL/SUMMARY_COLUMNS), 2 blade export + 2 blade print · FE `potential-customer-tracking/index.vue` (filterFields :341), `TrackingTable.vue` (COLS :242), `ItemListModal.vue` (COLUMNS :142) · Test thêm vào `tests/Feature/PotentialCustomerTracking/ReportApiTest.php` (fixture thêm ward/KVKD).
- [x] Test `test_loc_tinh_kvkd_loai_dong_khong_gan_kh` · `test_cot_kvkd_o_dong_kh`. BE → FE → Playwright.

### Task 10: Phát triển KH theo NVKD (R7)
**Files:** `CustomerDevelopmentReportService.php` (helper where dùng ở `ppRowsForGroup` :207-242 — nhóm care thêm join `customers`, KHÔNG thêm `customer_type`; `customersWithoutPp` :248; `enrichCustomerRows` :467 thêm `business_area_name`; `getFilterOptions` :86 không cần — FE dùng util) · FE `customer-development/index.vue` (filterFields :103, buildParams :252), `components/CustomerDevelopmentDetailModal.vue` (cột :134) · Test `tests/Feature/CustomerDevelopment/AreaFilterTest.php`.
- [x] Test `test_loc_kvkd_ca_nhom_dev_va_care` · `test_popup_co_cot_kvkd`. BE → FE → Playwright.

### Task 11: DS đăng ký KH toàn công ty (R8)
**Files:** `CustomerRegisterService.php` (join :43, select :45-61, applyFilters :69-109), `Transformers/CustomerRegisterResource/CustomerRegisterResource.php:20-35`, `app/ExcelExport/ExportColumnRegistry.php:947-955` · FE `customer-registers/index.vue` (filterFields :181, tableColumns :211, exportFields :233) · Test `tests/Feature/CustomerRegister/AreaFilterTest.php`.
- [x] Test `test_loc_tinh_theo_L1` · `test_excel_co_cot_kvkd`. BE → FE → Playwright.

## Phase 5 — Nghiệm thu
- [ ] Chạy toàn bộ test liên quan: `php artisan test --filter "CustomerBusinessArea|MeetingAreaSnapshot|CustomerMarketDevelopment|MeetingByMarket|ServiceDemand|PotentialCustomerCare|DivisionMarket|PotentialCustomerTracking|CustomerDevelopment|CustomerRegister"`.
- [ ] 2 lệnh tự kiểm định dạng số (CLAUDE.md) rỗng; `grep -rn DB_DATABASE_SECOND` trong 7 service đã sửa rỗng.
- [ ] Playwright: 8 màn, mỗi màn ảnh lưới + ô lọc + Excel/in; đóng browser.
- [ ] Xoá dữ liệu thử local; viết SQL kiểm prod sau deploy (dán trong chat).
- [ ] Cập nhật STATUS + checkpoint; báo user danh sách file để commit.

### Checkpoint — 2026-11-20 (chiều, xong code 8 báo cáo)
Vừa hoàn thành: Task 1–11 (BE + FE), Playwright có ảnh cả 8 màn. Test mới 26 bài xanh (helper 5 · snapshot 6 · Phát triển TT 4 ·
CSKH 2 · Meeting TT 3 · Nhu cầu DV 1 · Phân chia TT 2 · DS đăng ký 1) + test cũ Phát triển TT/CSKH 39 xanh, ServiceDemand/ReportApiTest
đã cập nhật khoá mới. Test fail còn lại đều CÓ SẴN trên gop_db (đã so bằng stash): Agent PhatTrienThiTruong 5, Rbac/PresaleScopeCodes 5,
ServiceDemand quyền 4, PotentialCustomerTracking 15 (fixture role vướng FK `roles_company_id` trên DB local).
Phân chia TT: user chốt dựng cây rsum theo mockup (component `DivisionMarketTree.vue`), giữ tìm nhanh, Cấu hình cột còn 3 cột dữ liệu.
Task 9 (Tổng hợp CSKH) + Task 10 (Phát triển KH theo NVKD): lọc + cột KVKD trên màn/popup; Excel/bản in CHƯA thêm cột KVKD; Task 10 chưa
có PHPUnit riêng (đã kiểm tinker + trình duyệt). Test file mới đều trong `.git/info/exclude` (không đẩy).
Đang làm dở: —
Bước tiếp theo: user xem + quyết (1) có thêm cột KVKD vào Excel/in của Tổng hợp CSKH & Phát triển KH không; (2) review toàn nhánh;
(3) dọn dữ liệu thử local (`scratchpad/cleanup12091.php`) khi user xem xong; (4) user commit.

### Checkpoint — 2026-11-20 (giữa ngày)
Vừa hoàn thành: Phase 0–2 + Task 5, 6 (BE + FE + Playwright có ảnh). Helper `CustomerBusinessArea` + util `business-area-options.js`;
snapshot `meetings.business_area_*` (migration đã chạy local bằng `--path`, seeder chạy local); 4 báo cáo Phát triển TT / Meeting theo TT / Nhu cầu DV xong.
Test BE mới đều xanh; test fail còn lại là lỗi CÓ SẴN trên gop_db (đã so bằng stash): Agent PhatTrienThiTruong 5 bài (TaskScopeGuard),
Rbac/PresaleScopeCodes 5 bài + ServiceDemand 4 bài quyền (DB local thiếu cột role_has_permissions.company_id).
Dữ liệu thử local: 5 KVKD `[TEST12091]` (id 43–47) + sao lưu tỉnh meeting ở scratchpad (`cleanup12091.php` để trả lại).
Verify FE: chạy `npx nuxt dev -c nuxt.verify.config.js` (file local-only, thêm transpile quill — build mới lỗi quill 2).
Đang làm dở: —
Bước tiếp theo (cập nhật chiều 20/11): Task 7 XONG (BE+FE+ảnh). Task 8 BE XONG (test 2/2, query 0,6s) — FE CHỜ user chốt: dựng lại cây rsum theo mockup hay giữ bảng gộp ô (#12169 cấu hình cột, #11581 tìm nhanh). ⚠️ FE Phân chia TT đang vỡ tới khi làm FE (BE đổi `wards`→`areas`). Sau đó Task 9–11.

### Checkpoint — 2026-11-20
Vừa hoàn thành: khảo sát 8 báo cáo, số liệu prod, spec + design + plan; tạo nhánh `task_12091` (chưa checkout); gộp #11888 (lưu mockup).
Đang làm dở: —
Bước tiếp theo: user duyệt plan + chốt các điểm mở → Phase 0.
Blocked: — (20/11 user chốt: L1 ok · KVKD khoá vẫn hiện ok · R5 xếp KVKD theo tên · R5 giữ tự tải · checkout ở repo chính; cách làm: tự làm tuần tự + review cuối)
