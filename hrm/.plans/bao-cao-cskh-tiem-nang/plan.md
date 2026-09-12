# Plan — Báo cáo kết quả chăm sóc khách hàng tiềm năng

> Design: `.plans/bao-cao-cskh-tiem-nang/design.md` · Nhánh `bao_cao_cskh_tiem_nang` (api + client, tách từ `tpe`).
> Repo **không có unit test BE** (`Modules/Assign/Tests` rỗng) → verify bằng Playwright e2e + kiểm tay.

---

## Phase 1 — Người chủ trì meeting (Task 1)

Thêm trường **Người chủ trì** cho meeting, thay cho việc suy chủ trì từ người tạo.

### Task 1.1 — BE: migration + entity

- [x] **Step 1:** Migration `Modules/Assign/Database/Migrations/2026_08_25_000001_add_host_employee_id_to_meetings_table.php`: `host_employee_id` `unsignedBigInteger nullable` after `end_date` + index; backfill `UPDATE meetings SET host_employee_id = created_by`. `down()` gỡ index rồi gỡ cột.
- [x] **Step 2:** `Modules/Assign/Entities/Meeting/Meeting.php`: thêm `host_employee_id` vào `$fillable` + quan hệ `host()` → `Modules\Human\Entities\Employee` (kèm `info` để lấy `fullname`).
- [x] **Step 3:** Chạy `php artisan migrate` trên DB local `hrm_tpe`, kiểm 45 meeting cũ đều có `host_employee_id = created_by`.

### Task 1.2 — BE: request + controller + resource

- [x] **Step 1:** `MeetingCreateApiRequest` + `MeetingUpdateApiRequest`: rule `host_employee_id => required|integer|exists:employees,id` + message tiếng Việt "Vui lòng chọn Người chủ trì.".
- [x] **Step 2:** `MeetingController::store()` và `::update()`: thêm `'host_employee_id'` vào `$request->only([...])` (2 chỗ).
- [x] **Step 3:** Trả `host_employee_id` + `host_name` (fallback tên người tạo nếu null) ở **`MeetingTransformer`** — ⚠️ màn chi tiết/sửa dùng class này, KHÔNG dùng `MeetingResource` (`MeetingResource` chỉ phục vụ các endpoint DANH SÁCH; nhét thêm vào đó sinh N+1 mà màn danh sách không cần).
- [x] **Step 4 (verify):** gọi API tạo/sửa meeting bằng curl hoặc e2e, kiểm cột ghi đúng và resource trả đúng.

### Task 1.3 — BE: repoint chỗ đang hiển thị chủ trì

- [x] **Step 1:** `Modules/Assign/Services/Report/MeetingByMarketService.php:396`: `host_name` đọc `host_employee_id`, fallback `created_by` khi null. Kiểm cả nhánh export (`:532`) dùng chung hàm này.
- [x] **Step 2 (verify):** mở `/assign/report/meeting-by-market`, cột "Người chủ trì" vẫn ra tên (không rỗng, không đổi so với trước vì đã backfill).

### Task 1.4 — BE: bổ sung `company_id` cho nguồn nhân viên đang hoạt động

- [x] **Step 1:** `app/Http/Controllers/Api/AuthNewController::userProfile()` — thêm `employee_infos.company_id` vào `select` của `$list_employee_infos` (đang lọc sẵn `employee_infos.status = 1`).
- [x] **Step 2 (verify):** gọi `/api/v1/users/auth/user-profile`, kiểm `list_employee_infos[].company_id` có mặt.

### Task 1.5 — FE: store key nhân viên cùng công ty + đang hoạt động

- [x] **Step 1:** `store/actions.js` — thêm `commit(SET_STATE, { key: 'activeCompanyEmployeeOptions', ... })`: lọc `list_employee_infos` theo `company_id === employee_company.id`, bỏ bản ghi không có `employee_id`, map `{ id: employee_id, text: 'code - fullname' }`, sort theo tên. Đặt cạnh `currentEmployeeCompany` để dễ đối chiếu, kèm comment nêu rõ vì sao không dùng `currentEmployeeCompany` (nguồn đó không lọc trạng thái).
- [x] **Step 2 (verify):** in `$store.state.activeCompanyEmployeeOptions` ở console, so số lượng với `currentEmployeeCompany` (phải ≤).

### Task 1.6 — FE: ô chọn Người chủ trì

- [x] **Step 1:** `pages/assign/meeting/components/GeneralInfo.vue` — chèn `<b-col md="12">` ngay **sau** hàng Bắt đầu/Kết thúc và **trước** checkbox "Meeting theo dự án": `V2BaseLabel` "Người chủ trì" + `Required`, `V2BaseSelect` (select2 có sẵn ô tìm kiếm) bind `form.host_employee_id`, `:disabled="isShow"`, `V2BaseError` cho `formError['host_employee_id']`.
- [x] **Step 2:** computed `hostOptions` = `activeCompanyEmployeeOptions`, **merge option đang chọn** nếu `form.host_employee_id` không có trong danh sách (chủ trì cũ đã nghỉ việc) — lấy tên từ `form.host_name` (rule "danh mục khoá vẫn phải hiện ở bản ghi đang dùng").
- [x] **Step 3:** `MeetingForm.vue` — thêm `host_employee_id: null` vào `resetForm()`, gán mặc định `= $store.state.current_employee.id` cho màn tạo mới (đặt cạnh `addCurrentEmployeeToCompanyMembers()`).
- [x] **Step 4 (verify):** tạo meeting mới → ô Người chủ trì tự điền người đang đăng nhập; đổi sang người khác, lưu, mở lại màn Sửa thấy đúng người đã chọn; màn Xem chi tiết ô bị khoá.

### Task 1.7 — E2E

- [x] **Step 1:** `e2e/tests/assign/meeting-host.api.spec.ts` (5 ca): thiếu chủ trì → **400** + message tiếng Việt; chủ trì không tồn tại → 400; lưu chủ trì khác người tạo → detail trả đúng, `creator` giữ nguyên; báo cáo thị trường đọc theo chủ trì mới; chủ trì đã nghỉ việc vẫn trả `host_name`.
- [x] **Step 2:** `e2e/tests/assign/meeting-host.spec.ts` (4 ca UI): vị trí ô (col-md-12, giữa "Kết thúc" và "Meeting theo dự án"); mặc định = người đăng nhập; danh sách ≤ `currentEmployeeCompany`; màn Xem ô bị khoá.
- [x] **Step 3 (verify):** `npx playwright test meeting-host` — 5 API + 4 UI đều xanh (chạy bằng Node 20: `PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH"`, Node mặc định của máy là 12 cho Nuxt).

> ⚠️ Ghi chú: endpoint meeting dùng `App\Http\Requests\ApiBaseRequest` nên lỗi validate trả **HTTP 400** (errors nằm trong `data`), KHÔNG phải 422 như `assign/scopes`.

---

## Phase 2 — Select nhu cầu KH ở dự án TKT (Task 2)

Gắn 1 **nhu cầu khách hàng** (1 dòng nhóm ngành trong biên bản khảo sát) cho 1 dự án TKT.

### Task 2.1 — BE: vòng đời nhu cầu

- [x] **Step 1:** Migration `2026_08_25_000002_add_tracking_columns_to_meeting_investment_demands_table.php`: `status` (1 Đang theo dõi / 2 Đã lập dự án TKT / 3 Không tiếp tục), `prospective_project_id` (không FK), `closed_at` + 2 index (`status, closed_at` cho báo cáo; `prospective_project_id`).
- [x] **Step 2:** `MeetingInvestmentDemand`: `$fillable` + cast `closed_at`, 3 hằng trạng thái + `STATUS_TEXT`/`STATUS_COLOR` (9 mã màu chuẩn), accessor `status_text`/`status_color`, quan hệ `prospectiveProject()`. `toArray()` format thêm `closed_at` về `Y-m-d` (cùng lý do timezone như `expected_start_date`).
- [x] **Step 3:** `MeetingService::syncInvestmentDemands()` đổi từ **xoá-ghi-lại** sang **upsert theo `(meeting_id, scope_id)`**; chỉ xoá dòng bị bỏ chọn. Thêm `guardDemandsNotLinked()` chặn bỏ nhu cầu đã gắn dự án (ValidationException).
- [x] **Step 4:** `MeetingController` (store/update/destroy) rethrow `ValidationException` trước `catch (\Exception)` — nếu không lỗi nghiệp vụ thành 500.

### Task 2.2 — BE: endpoint + gắn/gỡ

- [x] **Step 1:** `GET /assign/prospective-projects/customer-demands?customer_id=&include_id=` (đặt TRƯỚC route wildcard) + `CustomerDemandOptionResource` (nhãn `text` do BE dựng sẵn).
- [x] **Step 2:** `ProspectiveProjectService::listSelectableCustomerDemands()` — đúng KH, meeting loại `HOP_TIM_HIEU_GIOI_THIEU_SP` đã **Hoàn thành**, `has_investment_demand = 1`, **chủ trì = người đăng nhập**, nhu cầu còn "Đang theo dõi"; `include_id` giữ nhu cầu đang gắn.
- [x] **Step 3:** `ProspectiveProjectService::syncCustomerDemand()` gọi ở cuối `store()` + `update()`: gỡ nhu cầu cũ (về Đang theo dõi, xoá `closed_at`), gắn nhu cầu mới (`status = 2`, `closed_at = hôm nay`). Guard: không tồn tại / đã bị dự án khác gắn / khác khách hàng → 422. **Không gửi field** = giữ nguyên liên kết.
- [x] **Step 4:** `ProspectiveProjectRequest`: `customer_demand_id => nullable|integer` (cả bộ rule thường lẫn bộ dự án cha).
- [x] **Step 5:** `DetailProspectiveProjectResource` trả `customer_demand_id` + object `customer_demand` (truy ngược từ `meeting_investment_demands`, KHÔNG thêm cột cho `prospective_projects`).
- [x] **Step 6:** `ProspectiveProjectController` rethrow `ValidationException` trước `catch (Exception)`.

### Task 2.3 — FE

- [x] **Step 1:** `CustomerBlock.vue`: prop `show-demand-select`, ô `V2BaseSelect` "Nhu cầu khách hàng" đặt ngay **sau** select Người liên hệ; `demandOptions` nạp qua `apiGetMethod` (query ở `params`), watcher `customerIdForDemand` nạp lại khi đổi KH và **không** xoá lựa chọn ở lần hydrate đầu.
- [x] **Step 2:** `CustomerInfoSection.vue` bật `:show-demand-select="true"` CHỈ cho khối KH trực tiếp.
- [x] **Step 3:** `add.vue` + `_id/edit.vue`: khai `customer_demand_id: null` trong `formSubmit` (Vue 2 không reactive với key thêm sau), `ref="customerInfo"`, và `confirmMissingCustomerDemand()` chạy đầu `submitForm()` — cảnh báo bằng `$confirm` (component chung `base-confirm-modal`), không chặn.

### Task 2.4 — E2E

- [x] **Step 1:** Fixture `hrm-api/database/e2e_customer_demand_seed.php` (idempotent): 1 meeting Hoàn thành + 2 nhu cầu cho KH của dự án fixture, 1 meeting KH khác, 1 meeting **còn sửa được** (Chốt lịch, lịch họp tương lai) + thành viên tham dự.
- [x] **Step 2:** `customer-demand-link.api.spec.ts` — 11 ca (options, gắn/đổi/bỏ, include_id, detail truy ngược, không gửi field, 2 guard, upsert giữ vết theo dõi, chặn bỏ nhu cầu đã gắn ở biên bản).
- [x] **Step 3:** `customer-demand-link.spec.ts` — 4 ca UI (vị trí ô, chỉ ở KH trực tiếp, round-trip chọn–lưu–mở lại, cảnh báo + bấm Hủy không lưu).
- [x] **Step 4 (verify):** `npx playwright test customer-demand-link` — 11 API + 4 UI xanh.

## Phase 3 — Màn báo cáo

Màn `/assign/report/potential-customer-care`. **Ngoài scope phase này**: Xuất Excel, bản In, nút phóng to popup.

### Task 3.1 — BE: cron đóng nhu cầu quá hạn

- [x] **Step 1:** `app/Console/Commands/Assign/CloseExpiredCustomerDemandsCommand.php` — signature `assign:close-expired-customer-demands {--dry-run}`. Đóng nhu cầu `status = 1` có `expected_start_date < hôm nay`: `status = 3`, **`closed_at = expected_start_date`** (không phải ngày chạy). `expected_start_date` rỗng → bỏ qua. Idempotent, log số dòng.
- [x] **Step 2:** Đăng ký `dailyAt('01:20')` trong `app/Console/Kernel.php` (cạnh các job assign khác).
- [x] **Step 3 (verify):** chạy `--dry-run` rồi chạy thật trên dữ liệu seed, đối chiếu DB.

### Task 3.2 — BE: quyền

- [x] **Step 1:** `PermissionsTableSeeder` — 3 quyền id **1179/1180/1181**, nhóm "Báo cáo kết quả chăm sóc khách hàng tiềm năng".
- [x] **Step 2:** Insert thủ công trên DB local (seeder truncate cả bảng permissions) + gán cho role **Super admin id 18**, `role_has_permissions.company_id = 1`.

### Task 3.3 — BE: service tính số liệu

- [x] **Step 1:** `Modules/Assign/Services/Report/PotentialCustomerCareService.php`: query tập nhu cầu (meeting loại 7, Hoàn thành, `has_investment_demand = 1`) + `applyPermissionFilter()` copy khuôn `MeetingByMarketService` (fallback: chỉ meeting mình chủ trì / mình dự).
- [x] **Step 2:** Resolve Tỉnh + Phường/xã của KH **batch qua `mysql2`** (không join xuyên DB), memo theo request như `MeetingByMarketService`.
- [x] **Step 3:** Tính 2 khối (I.1/I.2/I, II.1/II.2/II) + 3 hộp KPI theo đúng công thức trong `design.md`.
- [x] **Step 4:** Dựng bảng theo dõi 3 phần (Lĩnh vực▸Nhóm ngành · Tỉnh▸Phường/xã · Phòng ban▸Nhân viên), mỗi dòng: số nhu cầu · giá trị dự kiến · chuyển đổi thành công · tỷ lệ thành công · không tiếp tục · tỷ trọng giá trị.
- [x] **Step 5:** Drill-down: resolve key (`all·carried·arisen·closed·converted·expired·field:·sector:·market:·ward:·dept:·emp:` + hậu tố `@won`/`@lost`) → danh sách nhu cầu chi tiết.

### Task 3.4 — BE: controller + routes

- [x] **Step 1:** `PotentialCustomerCareReportController` + 3 route `assign/report/potential-customer-care{,/filter-options,/demand-list}` (đặt TRƯỚC `meeting-by-market`). Route KHÔNG gắn `checkPermission` — phân quyền nằm trong service để giữ fallback "chỉ meeting của mình".
- [x] **Step 2 (verify):** dựng seed dữ liệu demo nhiều kỳ/lĩnh vực/thị trường rồi đối chiếu tay từng chỉ tiêu.

### Task 3.5 — FE

- [x] **Step 1:** `pages/assign/report/potential-customer-care/index.vue` + components (`CareResultFilter`, `CareSummaryBlocks`, `CareTrackingTable`, `DemandListModal`).
- [x] **Step 2:** Menu "Kết quả CSKH tiềm năng" trong `components/menu-sidebar.js` (dưới "Kết quả meeting theo thị trường"). ⚠️ File CRLF — không phá line ending.
- [x] **Step 3:** Cờ quyền FE mặc định `false`, chỉ set từ `$store.state.permissions`.

### Task 3.6 — E2E

- [x] **Step 1:** `hrm-api/database/e2e_care_report_seed.php` — 6 nhu cầu phủ đủ I.1/I.2/II.1/II.2 + 1 dòng đóng từ KỲ TRƯỚC (phải bị loại). Export ánh xạ id → nhóm chỉ tiêu; **không** khẳng định tổng tuyệt đối vì DB test còn fixture feature khác.
- [x] **Step 2:** `potential-customer-care.api.spec.ts` — 10 ca: id đúng nhóm · loại dòng đóng kỳ trước · đẳng thức I/II · KPI = tử/mẫu · 3 phần cùng TỔNG CỘNG + tỷ trọng = 100% · tiêu chí đổi bảng · `@won`/`@lost` · thống kê chéo · filter-options · **fail-closed**.
- [x] **Step 3:** `potential-customer-care.spec.ts` — 5 ca UI: bố cục màn · nút Ẩn/Hiện chi tiết · bấm số ra popup đúng số dòng · chip lọc nhanh · đổi tiêu chí.
- [x] **Step 4 (verify):** `npx playwright test potential-customer-care` — 10 API + 5 UI xanh.

### Task 3.7 — Rà lại style theo mockup (user trả lại 2 lần)

- [x] **Step 1:** Trích CSS thật trong `<style>` của mockup (tokens `:root` + các khối `.rsum-*` / `.drill-*`) thay vì tự đặt palette.
- [x] **Step 2:** Viết lại `CareSummaryBlocks` / `CareTrackingTable` theo đúng class + giá trị mockup; tách `format.js`, `ShareBar.vue`, `DrillNum.vue`, `KpiBoxes.vue` dùng chung.
- [x] **Step 3:** Bổ sung đủ ⓘ ở dải tổng hợp (dòng meta · 2 khối · 4 ô chỉ tiêu con · tiêu đề KPI) — nội dung bullet copy từ mockup, số liệu ghép động.
- [x] **Step 4:** Chuẩn hoá ⓘ theo `.claude/skills/info-icon-tooltip` (chuẩn phân hệ Assign) — `ri-information-line` 14px `#94a3b8` + `font-weight: normal` + `b-popover custom-class="info-popover"` `placement="bottom"`.
- [x] **Step 5:** Viết lại popup theo mockup: header gradient navy→teal, đủ 7 ô lọc trên 1 hàng, khối KPI thu nhỏ, "Phân bổ nhu cầu theo cơ cấu", thứ tự cột bám khối phân bổ, footer.
- [x] **Step 6:** BE bổ sung `kpis` cho `demand-list` (rỗng với nhóm "không tiếp tục") + rút gọn nhãn cơ cấu `Lĩnh vực KD`.
- [x] **Step 7 (fix bug):** `th` sticky cùng `z-index` che nút "Hiện chi tiết" → nâng z-index riêng ô tiêu đề.
- [x] **Step 8 (verify):** e2e cập nhật selector theo class mới; `potential-customer-care` 10 API + 5 UI xanh; spec khảo sát chạy riêng 21/21 xanh.

### Task 3.8 — Bổ sung theo phản hồi user (2026-08-25)

- [x] **Step 1:** Popup: nút **thu gọn khối tổng hợp** (dùng lại `.rsum-toggle` của màn chính), ẩn KPI + phân bổ, chỉ hiện khi có khối để thu.
- [x] **Step 2:** Fix popup **tràn chiều cao**: khoá `max-height: 92vh` + flex cột (header/footer đứng yên, chỉ thân cuộn), bỏ `max-height: 56vh` của bảng để không cuộn lồng cuộn, thêm `centered`.
- [x] **Step 3:** Nút **phóng to toàn màn hình** (`.care-drill-dialog--full`) — phải ghi đè cả `margin` và `min-height` của `.modal-dialog(-centered)` bootstrap, nếu không popup vẫn hở 4 mép.
- [x] **Step 4 (verify):** e2e ca 6 (không tràn viewport + thu gọn) và ca 7 (phóng to/thu nhỏ) — `potential-customer-care` 10 API + 7 UI xanh.

### Task 3.9 — Rà soát bộ lọc + khối phân bổ (2026-08-25)

- [x] **Step 1:** Cascade trong **popup** (trước chỉ có ở màn báo cáo): Lĩnh vực ▸ Nhóm ngành · Tỉnh/TP ▸ Phường/xã · Phòng ban ▸ Nhân viên — lọc theo `parent_id` BE trả sẵn, KHÔNG gọi thêm API; đổi ô cha thì xoá giá trị ô con (`resetChildOf`).
- [x] **Step 2:** Màn báo cáo gộp 2 lưới rời thành **1 lưới** (`Kỳ 3 + Tiêu chí 3 + khối lọc 6 = 12 cột`), hết cảnh mỗi hàng chỉ đầy nửa.
- [x] **Step 3:** Bỏ ô **"Bộ phận"** bằng prop `disable_part` — mockup PIVOT v10 đã bỏ và BE không lọc theo `part_id`.
- [x] **Step 4:** Thứ tự ô lọc popup: 3 cặp cha ▸ con liền nhau, Trạng thái cuối (`field·sector·market·ward·dept·emp·status`).
- [x] **Step 5:** Tiêu đề popup tách 2 phần — câu dẫn mờ `rgba(255,255,255,.72)`, **tên đối tượng** trắng đậm 800.
- [x] **Step 6:** Khối "Phân bổ nhu cầu theo cơ cấu" theo đúng `.drill-sum*`: **1 container cuộn chung** cho cả 3 cơ cấu (trước là 3 container → 3 thanh cuộn, hàng không thẳng cột), nhãn 96px sticky, `.care-drill-sum__chips` `nowrap`.
- [x] **Step 7 (verify):** e2e ca 8 phủ cascade cả 2 nơi + đã bỏ ô Bộ phận + đúng thứ tự 7 ô lọc. `potential-customer-care` **21/21 xanh**.

### Task 3.10 — Fix bộ lọc vỡ layout (2026-08-25)

User báo "bộ lọc báo cáo đang lỗi style → vỡ layout". Soi ra **2 lỗi cùng nằm ở khối lọc
Công ty/Phòng ban/Nhân viên**, đều do dùng sai `V2BaseCompanyDepartmentFilter` (khuôn đúng:
`pages/assign/report/meeting-by-market/index.vue:105`).

- [x] **Step 1 (vỡ lưới):** bỏ `<div class="col-md-6 mb-2">` bọc ngoài component. Component tự bọc
  `.d-contents` chứa các `col-md-3` để hoà vào `form-row` cha — bọc thêm 1 `col-*` làm 3 ô thành
  **cột-trong-cột**, co còn 1/8 lưới rồi xếp dọc, hở hẳn nửa hàng bên phải.
- [x] **Step 2 (bind hụt — lỗi NGHIỆP VỤ, không chỉ là style):** component **không hề có `$emit`**,
  nó ghi THẲNG vào object truyền qua prop `form`. Bind cũ `:company-id` + `@update:companyId` là
  bind vào prop/emit không tồn tại → chạy im lặng nhưng **chọn Phòng ban/Nhân viên không lọc gì cả**.
  Đổi sang `:form="filters"` + `wrapper-class="d-contents"`.
- [x] **Step 3:** khai `part_id: null` trong `initialFilters` — component ghi `form.part_id` trong
  watcher, Vue 2 không theo dõi được key thêm sau (BE không lọc theo `part_id`, chỉ để object đủ key).
- [x] **Step 4:** Từ ngày / Đến ngày `col-md-2` → `col-md-3` để hàng đầu của kỳ "Tuỳ chỉnh" đủ đúng
  12 cột (Kỳ 3 + Từ 3 + Đến 3 + Tiêu chí 3), trước đó hở 2 cột cuối hàng.
- [x] **Step 5 (e2e):** thêm ca 9 `potential-customer-care.spec.ts` — (a) không có cột lồng trong cột
  trong `.advanced-filters` + ô "Phòng ban" rộng bằng ô "Kỳ báo cáo"; (b) chọn 1 phòng ban rồi bấm
  Tìm kiếm thì request báo cáo phải mang `department_id`. Ca 8 (cascade) KHÔNG bắt được 2 lỗi này
  vì nó đọc thẳng `vm.filters`, không đi qua DOM lẫn request.
- [x] **Step 6 (verify):** đã revert tạm về code cũ để chứng minh ca 9 **fail** đúng chỗ
  (`toHaveCount(0)` nhận 3), rồi khôi phục — `npx playwright test potential-customer-care`
  **22/22 xanh** (10 API + 12 UI).

> ⚠️ Rút ra: `V2BaseCompanyDepartmentFilter` là component **kiểu ghi-vào-prop**, không phải
> `.sync`/`v-model`. Dùng ở màn mới thì copy nguyên cụm 4 dòng ở `meeting-by-market`, đừng tự suy
> ra tên prop/emit — sai kiểu này Vue không cảnh báo gì.

---

## Phase 4 — Xuất Excel + Bản In (2026-08-26)

4 đầu ra theo mockup: toolbar màn báo cáo có `In báo cáo` + `Xuất Excel`; footer popup drill-down có
`In danh sách` + `Xuất Excel danh sách`. Tất cả bám ĐÚNG bộ lọc đang áp dụng (popup bám thêm `drill`
+ bộ lọc riêng của popup).

> **Quyết định đã chốt với user (2026-08-26):**
> - Bản In dùng **khuôn popup xem trước** của skill `print-page` mục 8 → phải **port 3 file dùng chung
>   từ nhánh `gop_db`** (nhánh này tách từ `tpe` nên KHÔNG có sẵn — cùng kiểu bẫy "skill lệch repo").
> - Chọn kiểu in bằng **modal 2 radio theo mockup** (không dùng dropdown/2 nút rời).
> - **Excel KHÔNG letterhead**, bản In thì CÓ — bám đúng báo cáo anh em `meeting-by-market` (export của
>   nó cũng không letterhead) và tránh phải port thêm trait `EmbedsCompanyLetterhead` (`Modules/Finance`
>   không tồn tại trên nhánh này).
> - Excel bảng theo dõi **kèm khối tổng hợp + 3 KPI ở đầu file** (bản in theo mockup cũng kèm KPI).
> - **KHÔNG thêm quyền mới** — 4 route mới gate trong service như `index`/`demandList` để giữ fallback
>   "chỉ meeting của mình".

### Task 4.1 — FE: port khuôn popup xem trước bản in từ `gop_db`

- [x] **Step 1:** `git show origin/gop_db:<path>` lấy NGUYÊN VĂN 3 file (không sửa 1 chữ, để merge về
  `gop_db` sau không đụng độ): `components/print/ReportPrintPreviewModal.vue`,
  `utils/print/reportPrintStyle.js`, `utils/mixins/reportPrintPreviewMixin.js`.
- [x] **Step 2 (verify):** kiểm phụ thuộc của 3 file đó có đủ trên nhánh này — `buildQueryString`
  (`utils/url-action.js`), `V2BaseButton`, `markSignatureSpace`/`buildReportPrintCss`
  (`utils/print/reportPrintStyle.js` tự chứa). Thiếu cái nào thì port kèm.

### Task 4.2 — BE: Excel bảng theo dõi

- [x] **Step 1:** `PotentialCustomerCareService::getTrackingRowsForExport(Request)` — phẳng hoá
  `index()` thành mảng dòng: khối tổng hợp (I/I.1/I.2/II/II.1/II.2) + 3 KPI + từng phần bảng theo dõi
  2 cấp (cha in đậm, con thụt đầu dòng).
- [x] **Step 2:** `Modules/Assign/Export/PotentialCustomerCareExport.php` — `FromView` + `ShouldAutoSize`
  (khuôn `MeetingByMarketExport`), blade `resources/views/exports/assign/potential_customer_care_report.blade.php`.
- [x] **Step 3:** Số **thô** + `data-format` theo skill `export-excel` mục 1: tiền `#,##0`, tỷ lệ
  `0.0%` (giá trị là phân số, KHÔNG nhân 100), số đếm `#,##0`. TUYỆT ĐỐI không `number_format` ở
  nhánh Excel.
- [x] **Step 4:** Route `GET assign/report/potential-customer-care/export` + controller `export()`
  (`Excel::download`, tên file `bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.xlsx`).

### Task 4.3 — BE: Excel danh sách nhu cầu (popup)

- [x] **Step 1:** `PotentialCustomerCareDemandExport` + blade `potential_customer_care_demands.blade.php`
  — **13 cột CỐ ĐỊNH** (Lĩnh vực KD · Nhóm ngành · Tỉnh/TP · Phường/xã · Phòng · Kinh doanh chủ trì ·
  Khách hàng · Giá trị đầu tư dự kiến · Thời gian triển khai · DV sửa chữa · Meeting · Trạng thái ·
  Dự án TKT). KHÔNG dùng thứ tự cột động của popup (đổi theo cơ cấu đang xem) — file xuất ra phải
  luôn đủ và cùng bố cục.
- [x] **Step 2:** Route `GET assign/report/potential-customer-care/demand-list/export` — dùng lại
  `service->demandList($request)` nên bám đúng `drill` + bộ lọc popup.

### Task 4.4 — BE: bản In (2 chế độ)

- [x] **Step 1:** Port trait letterhead sang `Modules/Assign/Services/Concerns/PrintsCompanyLetterhead.php`
  (nguyên văn từ `gop_db`, chỉ đổi namespace) — dùng `currentCompanyLetterhead()` vì báo cáo không gắn
  với 1 chứng từ nào để bám `company_id`.
- [x] **Step 2:** `PotentialCustomerCarePrintService` dựng HTML A4 ngang cho 2 chế độ:
  `summary` (khối tổng hợp + KPI + bảng theo dõi) và `detail` (13 cột, từng nhu cầu).
- [x] **Step 3:** Route `GET assign/report/potential-customer-care/print-list-data?mode=summary|detail`
  trả ĐÚNG contract của mixin: `{ data: { template: '<html>' } }`.
- [x] **Step 4:** Route riêng cho popup: `print-list-data` nhận cả `drill` + bộ lọc popup khi
  `mode=detail` gọi từ popup drill-down.

### Task 4.5 — FE: nút + modal chọn kiểu in ở màn báo cáo

- [x] **Step 1:** `index.vue` slot `#header-actions`: 2 nút `V2BaseButton secondary size="sm" class="btn-compact"`
  — `ri-printer-line` "In báo cáo" + `ri-download-line` "Xuất Excel" (copy khuôn `meeting-by-market/index.vue:20`).
- [x] **Step 2:** `components/PrintOptionsModal.vue` — `b-modal` 520px, 2 radio `.print-option` theo
  mockup (tiêu đề + dòng mô tả), footer `Huỷ` / `In`. Dựng trong feature vì `base-confirm-modal`
  không có slot nội dung và CLAUDE.md cấm tự sửa component dùng chung.
- [x] **Step 3:** Nối `reportPrintPreviewMixin` + `ReportPrintPreviewModal` (thẻ popup phải nằm TRONG
  thẻ gốc của template — đặt sau `</div>` cuối là lỗi "exactly one root element").
- [x] **Step 4:** Tải Excel bằng **link trực tiếp `?token=`** + `Content-Disposition` của server,
  KHÔNG fetch-blob (blob + `<a download>` ra file UUID không đuôi trên Safari/webview).

### Task 4.6 — FE: 2 nút trong footer popup drill-down

- [x] **Step 1:** `DemandListModal.vue` `.care-drill-footer` thêm `In danh sách` + `Xuất Excel danh sách`,
  emit `print` / `export` lên `index.vue` (popup không tự gọi API — bộ lọc gốc nằm ở cha).
- [x] **Step 2:** Popup xem trước mở ĐÈ lên popup drill-down → kiểm z-index + không kẹt scroll-lock
  của bootstrap khi đóng 1 trong 2.

### Task 4.7 — E2E

- [x] **Step 1:** `potential-customer-care-export.api.spec.ts` — content-type `.xlsx`, có
  `Content-Disposition` kèm tên file; **đọc lại file bằng PhpSpreadsheet** kiểm ô tiền/tỷ lệ là kiểu
  `n` (không phải `s`); Excel danh sách bám đúng `drill`; ca **fail-closed**.
- [x] **Step 2:** `print-list-data` cả 2 mode trả HTML có `<img>` letterhead + số dòng khớp bộ lọc.
- [x] **Step 3:** UI: 2 nút toolbar, modal 2 radio, popup xem trước hiện nội dung, 2 nút trong footer
  popup drill-down.
- [x] **Step 4 (verify):** `npx playwright test potential-customer-care` — **30/30 xanh**
  (16 API + 14 UI).

> ⚠️ 2 điều học được khi dựng file Excel (bổ sung cho skill `export-excel`):
> 1. **HTML reader CẮT SẠCH khoảng trắng đầu ô** — thụt đầu dòng cấp con bằng dấu cách là mất hết.
>    Dùng ký tự thật (`— `) làm dấu phân cấp.
> 2. **STT dạng "1.10" bị ép về SỐ 1.1** nên trùng với "1.1" thật. `data-format` KHÔNG cứu được:
>    reader chỉ `setFormatCode`, còn kiểu ô do `DefaultValueBinder` quyết theo nội dung
>    (`Reader/Html.php:590`). Đã bỏ hẳn STT ở dòng cấp con.
> Cả 2 lỗi này nhìn file bằng mắt KHÔNG thấy — chỉ lộ khi đọc lại bằng PhpSpreadsheet.

---

### Task 4.8 — Bản in của popup phải soi đủ nội dung popup (2026-08-26)

User: "In popup cần thể hiện đủ thông tin đang lọc + khối summary + KPI". Bản in `mode=detail` trước
đó chỉ có bảng chi tiết — in ra không biết tập này lọc theo gì, tỷ lệ chuyển đổi bao nhiêu.

- [x] **Step 1:** `PotentialCustomerCareService::describeDrillFilters()` — mô tả 7 ô lọc RIÊNG của
  popup + ô tìm kiếm. Nhận vào tập **đã lọc** để lấy tên (mọi dòng còn lại đều mang đúng giá trị
  đang lọc); không gọi lại `applyDrillFilters()` vì hàm đó private và chạy lại tốn thêm 1 lượt
  resolve tỉnh/phường qua kết nối DB thứ hai. `drill_status` đọc `MeetingInvestmentDemand::STATUS_TEXT`.
- [x] **Step 2:** `renderDetail()` truyền thêm `kpis` (`listKpis`) + `crossStats` — tính TRÊN CHÍNH
  tập đang xem, đúng như popup, không phải của cả kỳ.
- [x] **Step 3:** Blade danh sách dựng lại phần đầu theo đúng thứ tự popup: nhãn ô số đã bấm →
  bộ lọc màn báo cáo → "Lọc trong danh sách: …" → tổng (n nhu cầu · giá trị) → bảng KPI 3 cột →
  bảng "Phân bổ nhu cầu theo cơ cấu" → bảng chi tiết.
- [x] **Step 4 (e2e):** ca 6 mới ở `potential-customer-care-export.api.spec.ts` phủ đủ 5 phần
  (nhãn + bộ lọc popup + tổng + KPI khớp popup + cơ cấu khớp popup). Ca 5 cũ đếm `<tbody>` ĐẦU TIÊN
  nên chèn 2 bảng lên trước là hỏng — đổi sang helper `dataTableRowCount()` bám bảng có cột "STT".
- [x] **Step 5 (verify):** `npx playwright test potential-customer-care` — **31/31 xanh**.

---

### Task 4.9 — Gộp nút Xoá lọc vào hàng lọc của popup (2026-08-26)

- [x] **Step 1:** Bỏ hẳn khối `.care-drill-subbar` — nút Xoá lọc đang chiếm trọn 1 dòng riêng trong
  khi hàng lọc gói sang dòng 2 vẫn còn thừa nửa dòng. Chuyển nút vào `.care-drill-filters` ngay sau
  ô lọc cuối (`.care-drill-filters__item--action`, `width: auto` để không ăn 190px như ô lọc).
- [x] **Step 2:** "Thu gọn" + số đếm gom vào `.care-drill-filters__meta` với `margin-left: auto` —
  flex-wrap tính auto theo DÒNG đang đứng nên chúng bám mép phải của dòng cuối hàng lọc, popup bớt
  hẳn 1 dòng chiều cao cho bảng chi tiết.
- [x] **Step 3 (fix flaky):** thêm `e2e/utils/careFixture.ts` — 2 spec (`…api.spec.ts` và
  `…-export.api.spec.ts`) dùng chung `e2e_care_report_seed.php`, playwright chạy 2 worker song song
  nên 2 tiến trình seed cùng lúc đâm unique key (`Duplicate entry '51-24' for key
  'meeting_investment_scopes.mis_meeting_scope_unique'`). Seed idempotent nhưng kiểm-rồi-ghi KHÔNG
  nguyên tử. Khoá bằng `fs.mkdirSync` (nguyên tử ở mức OS) + dọn khoá mồ côi sau 60s.
- [x] **Step 4 (verify):** chạy `npx playwright test potential-customer-care` **3 lần liên tiếp** —
  31/31 xanh cả 3 lần (trước khi khoá thì rớt ngẫu nhiên ở ca 1).

---

### Task 4.10 — Thu hẹp sidebar còn 220px (NGOÀI phạm vi feature, 2026-08-26)

Yêu cầu rời của user trong cùng session; ghi ở đây để không mất vết, KHÔNG thuộc feature CSKH.

- [x] **Step 1:** `assets/scss/config/default/_variables.scss` — `$leftbar-width: 260px → 220px`.
  Đây là **một chỗ duy nhất** cho toàn hệ thống: `.left-side-menu` (cả cây UBold lẫn rail MISA
  `.sale-cats`), `margin-left` của `.content-page`, `_layouts.scss`, `_left-menu.scss` đều đọc biến
  này. Đã grep: không có chỗ nào hardcode `260px` trong `assets/scss/` ngoài file config.
- [x] **Step 2:** `components/TrainingFooter.vue` — `left: 260px → 220px` (file `.vue` không nạp
  biến SCSS của theme nên phải sửa tay; để nguyên thì footer hở 40px so với mép sidebar).
- [x] **Step 3 (verify):** đo thật bằng Playwright trên `assign` + `training`: `.left-side-menu`
  = 220px, `.content-page` `margin-left` = 220px, không tràn ngang. Panel bay ra của sidebar MISA
  (`.misa-detail`) bám sát mép rail (`gap = 0`) vì offset của nó đo runtime theo rail.
- [x] **Step 4 (verify):** `npx playwright test tests/assign --project=chromium` — 50 pass / 2 fail
  (`internal-business-scope` ca "Xoá bản ghi vừa tạo" và `quotation-unit-select`). **2 ca này rớt
  SẴN từ trước**: đã `git stash` bỏ thay đổi sidebar rồi chạy lại, vẫn rớt y hệt → không liên quan.

> Phân hệ dùng sidebar: chỉ **Assign** và **Training** (`layouts/default-sidebar.vue` là layout DUY
> NHẤT có sidebar). Human / Timesheet / Payroll / Decision dùng thanh điều hướng NGANG, không có
> sidebar nên không đổi gì.

---

## Phase 5 — Testcase (2026-08-26)

### Task 5.1 — Sinh testcase.xlsx theo skill `testcase-documenter`

- [x] **Step 1:** `.plans/bao-cao-cskh-tiem-nang/gen_testcase.py` — chỉ chứa 3 khối CONFIG
  (DESCRIPTION_BLOCK / ROLE_TCS / SECTIONS) rồi gọi `build()` của
  `.claude/skills/testcase-documenter/assets/tc_engine.py`. KHÔNG nhân bản code dựng Excel.
- [x] **Step 2:** 9 mục mô tả viết đủ, mục 2/3 liệt kê từng điều kiện, mục 7 chép NGUYÊN VĂN 3 tên
  quyền tiếng Việt, mục 8 diễn giải công thức bằng lời, mục 9 gom 9 bẫy dễ sai nhất của màn.
- [x] **Step 3:** 8 ca `TC-ROLE` phủ đủ 3 quyền + ca "không có quyền nào" (fallback chỉ thấy meeting
  của mình) + 2 ca gọi thẳng chức năng bỏ qua giao diện + ca ẩn nút "+ Tạo mới".
- [x] **Step 4:** 10 section nghiệp vụ đánh La Mã, đặt tên theo đúng cấu trúc màn này
  (khối tổng hợp & KPI · bảng theo dõi · cửa sổ chi tiết · vòng đời nhu cầu · Xuất Excel / In).
- [x] **Step 5 (verify):** chạy generator — bộ kiểm tra thuật ngữ in **"OK - khong con thuat ngu ky
  thuat"**; **167 TC**, P0 111 ca (**66%**, yêu cầu ≥ 40%), **không trùng TC ID**.
- [x] **Step 6 (verify):** đọc lại file bằng openpyxl: đủ 9 dòng mô tả · 2 khối summary đúng range ·
  **có dòng header 17 cột ở dòng 17** (file mẫu của team thiếu) · 11 dòng section · K/L/M mặc định
  "Not Executed" + danh sách chọn · O/P/Q để trống + danh sách chọn · **không khoá dòng tiêu đề**.

> Ngôn ngữ: toàn bộ file viết bằng nhãn hiển thị thật trên màn, KHÔNG có tên bảng/cột, mã lỗi kỹ
> thuật hay đường dẫn chức năng — người đọc là QA và bộ phận nghiệp vụ.

---

### Task 5.2 — Sinh SRS theo skill `srs-documenter` (form mới 4 chương)

- [x] **Step 1:** `.plans/bao-cao-cskh-tiem-nang/gen_srs.py` dùng `srs_docx_lib` + `srs_uml_render`
  của skill. ⚠️ `srs_uml_render` trỏ cứng font Windows (`C:\Windows\Fonts\segoeui.ttf`) — máy đang
  làm là macOS nên generator **ghi đè biến font sang Arial hệ thống**, KHÔNG sửa file dùng chung
  trong `.claude/skills/`.
- [x] **Step 2:** Chụp 9 ảnh thật vào `bao-cao-cskh_shots/` (đã bị `.gitignore` chặn theo đúng skill:
  ảnh nhúng sẵn trong .docx, không đẩy lên repo).
- [x] **Step 3:** 8 chức năng FR-01…FR-08 (xem báo cáo · lọc · danh sách chi tiết · lọc trong danh
  sách · in · xuất Excel · tạo dự án TKT · tác vụ tự đóng nhu cầu hết hạn). 2 chức năng CHỈ ĐỌC
  (FR-01, FR-03) bỏ mục "Biểu đồ Usecase" và lùi số mục con 1 bậc, đúng bản mẫu.
- [x] **Step 4:** Phần 2 phân quyền tách 2 nhóm: Q1 (thao tác) và V1/V2/V3 (phạm vi dữ liệu), ma
  trận có thêm cột "Không có quyền nào" để thể hiện fallback chỉ thấy meeting của mình.
- [x] **Step 5:** Phần 4 gồm **14 quy tắc nghiệp vụ** BR-01…BR-14, mọi rule truy vết được về code.
- [x] **Step 6 (verify):** self-check của thư viện: **28 bảng · 207 đoạn · 16 ảnh nhúng · 0 sơ đồ vẽ
  bằng ký tự**; assert không còn mục đã bỏ của form cũ (Tổng quan, Mini-Spec, Tiêu chí nghiệm thu,
  Ngoài phạm vi, Chức năng liên quan, Route (FE), Menu:); đánh số chương mục liên tục.
- [x] **Step 7 (verify):** trích ảnh nhúng ra xem lại — sơ đồ tổng quan và sơ đồ từng chức năng
  hiện **đủ dấu tiếng Việt** (ụ ị ọ ề ă), không bị mất dấu như lỗi font đã ghi trong skill.

> ⚠️ **Mục lục chưa được cập nhật số trang**: thư viện cập nhật trường mục lục bằng PowerShell +
> Word, chỉ chạy trên Windows. Mở file trên Word rồi bấm chuột phải vào mục lục ▸ Update Field ▸
> Update entire table là xong (ghi chú này đã có sẵn trong file).

---

## Phase 6 — Seeder dữ liệu demo chạy trên VPS (2026-08-26)

Yêu cầu rời sau khi feature đã merge: cần bộ dữ liệu demo để nghiệm thu / trình diễn trên VPS.

> **Quyết định đã chốt với user:** (1) làm bằng **artisan command** (có tham số, có `--dry-run`,
> có `--clean`), không dùng seeder class hay script tinker; (2) **chỉ ĐỌC** khách hàng có sẵn của
> ERP, tuyệt đối không ghi sang DB ERP; (3) quy mô vừa — ~120 nhu cầu trải 6 tháng.

### Task 6.1 — Artisan command sinh dữ liệu demo

- [x] **Step 1:** `app/Console/Commands/Assign/SeedCareReportDemoCommand.php`, signature
  `assign:seed-care-demo {--months=6} {--demands=120} {--clean} {--dry-run} {--force}`. Đặt cạnh
  `CloseExpiredCustomerDemandsCommand` để cùng chỗ với các lệnh khác của phân hệ.
- [x] **Step 2 (an toàn):** mọi bản ghi sinh ra mang tiền tố mã **`DEMO-CSKH-`** (meeting và dự án
  TKT) — đây là thứ DUY NHẤT `--clean` bám vào để xoá, nên không thể chạm dữ liệu thật. In tên DB
  đang trỏ tới rồi hỏi xác nhận trước khi ghi (`--force` để bỏ qua khi chạy trong script).
- [x] **Step 3:** Nguồn dữ liệu: khách hàng lấy từ ERP qua `mysql2` **chỉ bằng lệnh đọc**; người
  chủ trì lấy nhân viên đang hoạt động thuộc nhiều phòng ban; nhóm ngành lấy các nhóm đang hoạt
  động CÓ lĩnh vực cha (để phần "Theo lĩnh vực" không gom hết vào "Chưa xác định").
- [x] **Step 4:** Rải trạng thái ~50% Đang theo dõi / 30% Đã lập dự án TKT / 20% Không tiếp tục,
  ngày đóng rải qua các tháng để kỳ Tháng này / Quý này / Năm nay đều có số khác 0.
- [x] **Step 5:** Nhu cầu "Đã lập dự án TKT" tạo kèm 1 dự án tiền khả thi demo rồi gắn vào, để cột
  "Dự án TKT" trong cửa sổ chi tiết có dữ liệu.
- [x] **Step 6:** Idempotent — upsert theo mã, chạy lại nhiều lần không nhân đôi.
- [x] **Step 7 (verify):** `--dry-run` → chạy thật trên `hrm_tpe` → mở màn báo cáo đối chiếu bảng
  tóm tắt in ra với 2 khối tổng hợp → chạy lại lần 2 xác nhận số KHÔNG đổi → `--clean` xác nhận về
  0 và dữ liệu thật còn nguyên.
- [x] **Step 8 (verify):** chạy lại `npx playwright test potential-customer-care` — **31/31 xanh**
  với dữ liệu demo đã nằm trong DB (spec vốn không so tổng tuyệt đối nên không vỡ).

> ⚠️ **2 lỗi tự gây ra khi chạy thử, đã sửa** — ghi lại vì cả hai đều không ném lỗi, chỉ lộ khi
> đối chiếu số:
> 1. Lấy khách hàng bằng `orderBy(province_id)->limit(4000)` rồi mới nhóm theo tỉnh → 4.000 dòng đầu
>    nằm trọn trong MỘT tỉnh, kết quả chỉ ra **3 khách hàng / 1 tỉnh**. Phải lấy danh sách tỉnh
>    trước rồi truy từng tỉnh (10 tỉnh × 3 khách = 30).
> 2. Dùng CHUNG một chỉ số để vừa chọn trạng thái vừa quyết định kéo ngày đóng về kỳ hiện tại →
>    toàn bộ nhu cầu "Không tiếp tục" dồn vào tháng này, ô KPI "Thất bại / tổng nhu cầu đóng" vọt
>    lên **64,9%**, bản demo trông như hệ thống tính sai. Tách 2 quyết định độc lập → còn **45,9%**.

> ℹ️ Trên DB local, phần "Theo lĩnh vực" chỉ ra **2 dòng cha** vì 24 nhóm ngành đang hoạt động chỉ
> trỏ vào 2 lĩnh vực kinh doanh nội bộ (dù danh mục có 6). Đây là hạn chế DỮ LIỆU, không phải lỗi
> lệnh — muốn demo phần này nhiều dòng hơn thì gán lĩnh vực cha cho các nhóm ngành trước khi chạy.

---

### Task 6.2 — Loại meeting hệ thống trên môi trường mới (2026-08-26)

User báo lệnh demo lỗi trên VPS vì chưa có loại meeting "Họp tìm hiểu & Giới thiệu sản phẩm".

- [x] **Step 1:** Rà repo — **KHÔNG cần viết seeder mới**, đã có sẵn
  `Modules/Assign/Database/Seeders/SystemMeetingTypesSeeder.php` (dùng `updateOrCreate` theo `code`
  nên chạy lại nhiều lần không nhân bản). Đã xác nhận file có trên `origin/tpe` nên VPS chỉ cần
  `git pull` là có.
- [x] **Step 2:** Chạy thử trên local — tạo/cập nhật đúng bản ghi
  (`id=7 · Họp tìm hiểu & Giới thiệu sản phẩm · has_customer=1 · status=1`).
- [x] **Step 3 (nguyên nhân gốc):** lệnh `assign:seed-care-demo` báo thiếu loại meeting nhưng
  KHÔNG nói cách khắc phục — đó là lý do phải đi tìm. Bổ sung 2 dòng hướng dẫn ngay trong thông báo
  lỗi: câu lệnh chạy seeder loại meeting, và cách xử lý khi thiếu nhóm ngành có lĩnh vực cha
  (`php artisan migrate` hoặc gán tay ở Danh mục ▸ Nhóm ngành).
- [x] **Step 4 (verify):** đổi tạm mã loại meeting để ép vào nhánh lỗi → thông báo in ra đúng câu
  lệnh, không bị hỏng dấu gạch chéo ngược; khôi phục lại mã cũ và chạy `--dry-run` xác nhận lệnh
  hoạt động bình thường.

> **Thứ tự dựng dữ liệu demo trên môi trường MỚI** (thiếu bước nào cũng ra lỗi khó đoán):
> 1. `php artisan migrate`
> 2. `php artisan db:seed --class="Modules\Assign\Database\Seeders\SystemMeetingTypesSeeder" --force`
> 3. Insert thủ công 3 quyền 1179–1181 rồi gán role (`role_has_permissions` cần `company_id`)
> 4. `php artisan assign:seed-care-demo --dry-run` rồi bỏ `--dry-run`
> 5. Bật cron `assign:close-expired-customer-demands`

---

## Phase 7 — Rà soát tooltip ⓘ theo mockup (2026-08-28)

Yêu cầu của user: đối chiếu lại TOÀN BỘ mockup đã duyệt
`.plans/gop-db/ke-hoach-phat-trien-thi-truong/bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`,
tooltip icon ⓘ trên màn phải giống mockup **cả nội dung lẫn cách trình bày**; kiểu icon/popover
bám theo các báo cáo khác đã làm trong phần mềm.

> **Quyết định đã chốt:** giữ nguyên chuẩn `.claude/skills/info-icon-tooltip` (`ri-information-line`
> 14px `#94a3b8` + `b-popover custom-class="info-popover"`) như mockup KHÔNG dùng (mockup tự vẽ
> vòng tròn chữ `i` + tooltip CSS nền `#0f2537`). Lấy của mockup phần **nội dung + bố cục bên trong
> tooltip**: dòng tiêu đề IN HOA đậm + các gạch đầu dòng.

### Task 7.1 — Đối chiếu và bổ sung tooltip còn thiếu

- [x] **Step 1:** Kiểm đếm mockup — **20 vị trí** có ⓘ (mục đích báo cáo · 2 ô lọc · dòng meta ·
  2 khối + 4 ô chỉ tiêu con · tiêu đề KPI + 3 hộp KPI · 3 tiêu đề cột · 3 dòng tiêu đề phần);
  màn đang thiếu **6** (mục đích báo cáo, 2 ô lọc, 3 dòng tiêu đề phần I/II/III).
- [x] **Step 2:** Mục đích báo cáo — thêm ⓘ cạnh tiêu đề panel lọc. `V2BaseFilterPanel` chưa có
  chỗ cắm nên bổ sung slot `title-suffix` (thêm mới, không đổi hành vi màn nào khác); prop
  `subtitle` của panel vốn đã bị comment trong component nên nội dung mục đích trước đó KHÔNG
  hiển thị ở đâu cả.
- [x] **Step 3:** 2 ô lọc "Kỳ báo cáo" / "Tiêu chí theo dõi" — dùng `V2BaseLabel :hint`
  (`V2BaseFieldHint`, chuẩn dùng chung cho nhãn trường), không tự chế dấu `?` như mockup.
- [x] **Step 4:** 3 dòng tiêu đề phần của bảng theo dõi — computed `sectionTips` bám theo `tones`
  nên lọc còn 1 tiêu chí vẫn ra đúng nội dung phần đó.

### Task 7.2 — Sửa nội dung tooltip đã có cho khớp mockup

- [x] **Step 1:** Dòng meta "MỤC TIÊU BÁO CÁO" — thay 3 gạch đầu dòng tự viết bằng đúng nội dung
  mockup (thêm dòng nguồn dữ liệu + dòng kỳ đang xem).
- [x] **Step 2:** 3 hộp KPI — thêm tiêu đề "CÔNG THỨC", đổi sang gạch đầu dòng, bổ sung dòng ghi
  chú cuối của từng hộp (hộp 1 đổi câu khi dùng trong popup drill vì mẫu số là danh sách đang lọc).
- [x] **Step 3:** 3 tooltip tiêu đề cột của bảng theo dõi — từ đoạn văn xuôi đổi sang khuôn tiêu đề
  IN HOA + gạch đầu dòng, đủ ý như mockup.
- [x] **Step 4 (verify):** chạy trên dev (`localhost:3000`) bằng Playwright, hover từng ⓘ và đọc
  nội dung popover thật: mục đích báo cáo · 2 ô lọc · dòng meta · KPI màn chính · KPI trong popup
  drill · tiêu đề phần · 3 tiêu đề cột — tất cả ra đúng nội dung mới, 0 lỗi console.

> ⚠️ **2 chỗ CỐ Ý không copy nguyên văn mockup vì mockup mô tả sai luật đã code** (đã ghi chú
> ngay trong file component):
> 1. Ô "Chăm sóc thất bại": mockup ghi *"Hạn theo dõi = tháng dự kiến triển khai + số tháng cấu
>    hình hệ thống"*. Thực tế `CloseExpiredCustomerDemandsCommand` đóng nhu cầu khi **quá
>    `expected_start_date`**, không cộng thêm tháng cấu hình nào.
> 2. Ô "Nhu cầu mang sang từ kỳ trước": mockup có dòng *'trong bảng, các dòng này gắn nhãn "Kỳ
>    trước"'* — bảng theo dõi thật KHÔNG có nhãn đó.

---

### Task 7.3 — Bảng không xuống dòng, cho cuộn ngang (2026-08-28)

User: mọi cột ở CẢ màn báo cáo lẫn popup không được bẻ chữ (nội dung lẫn tên cột) — dài thì cho cuộn.

- [x] **Step 1:** `CareTrackingTable.vue` — `table-layout: fixed` → `auto` + `white-space: nowrap`
  cho `th`/`td`. Width ở `<colgroup>` từ nay là mức TỐI THIỂU, cột nào dài thì tự nới.
- [x] **Step 2:** `DemandListModal.vue` — bỏ `overflow-wrap: anywhere`, thêm `nowrap`, bỏ
  `min-width: 1740px` cứng, `width` khai ở `<th>` đổi thành `min-width`.
- [x] **Step 3:** Thêm **thanh cuộn ngang phía TRÊN** cho cả 2 bảng (CLAUDE.md: bảng tràn ngang
  phải có thanh cuộn ở cả trên lẫn dưới). `components/V2BaseTableScroll.vue` mà skill nhắc tới
  KHÔNG tồn tại trên nhánh này → copy pattern `topScroll`/`bottomScroll` của
  `meeting-by-employees/components/MeetingByEmployeesTable.vue`. Thanh cuộn mảnh 6px, tự ẩn khi
  bảng vừa khung.
- [x] **Step 4 (bẫy đã dính):** đo bề rộng bảng bằng `watch` + `$nextTick` là **KHÔNG đủ** — lúc đó
  trình duyệt chưa dàn xong cột (popup còn đang chạy hiệu ứng mở, dữ liệu dòng chưa về) nên đo ra
  1366px trong khi bảng thật 2397px → thanh cuộn trên ngắn hụt và bị ẩn nhầm. Phải dùng
  `ResizeObserver` bám vào chính thẻ `<table>` và khung cuộn.
- [x] **Step 5 (verify):** chạy trên dev — màn báo cáo ở 1100px: bảng 1198px > khung 853px, thanh
  cuộn trên hiện đúng bề rộng; popup: bảng 2397px > khung 1361px, kéo thanh trên 600px thì thanh
  dưới chạy theo đúng 600px; `white-space` của ô = `nowrap` ở cả 2 bảng; 0 lỗi console.

---

### Task 7.4 — Chip phân bổ trong popup phải đổ giá trị vào ô lọc (2026-08-28)

User: bấm chip ở khối "Phân bổ nhu cầu theo cơ cấu" thì bảng đã lọc theo, nhưng **ô lọc vẫn trống**
nên không biết đang lọc theo gì để bỏ ra.

**Nguyên nhân gốc:** `DemandListModal.vue` giữ **state `chips` riêng** song song với `filters`;
lúc emit thì `chips` ghi đè lên tham số lọc (`if (this.chips.field) active.drill_field_id = ...`)
nhưng KHÔNG bao giờ ghi vào `this.filters` → select2 không có gì để hiển thị. Mockup không có
state thứ hai: bấm chip là gán thẳng vào ô lọc (`sel.value = sel.value === id ? '' : id`) rồi
`drillCascades()`, trạng thái bật/tắt của chip suy ra từ chính giá trị ô lọc.

- [x] **Step 1:** Xoá hẳn state `chips`; thêm `chipParam()` map cơ cấu → tham số lọc
  (`field → drill_field_id` · `market → drill_province_id` · `dept → drill_department_id`).
- [x] **Step 2:** `toggleChip()` ghi thẳng vào `filters` (bấm lại chip đang bật thì trả về `null`)
  + gọi `resetChildOf()` để xoá ô con — đúng như khi người dùng tự chọn ở ô lọc.
- [x] **Step 3:** `isChipActive()` đọc từ `filters`; `isFiltered` và `resetLocal()` bỏ tham chiếu
  tới `chips`; bỏ đoạn ghi đè lúc emit.
- [x] **Step 4 (an toàn):** chip chỉ xuất hiện cho cơ cấu KHÔNG bị ẩn — BE `crossStats()` loại cơ
  cấu đang xem bằng đúng bảng map mà FE `showFilter()` dùng (`sector→field`, `ward→market`,
  `emp→dept`), nên ghi vào `filters` không bao giờ rơi vào ô đang ẩn (ô ẩn bị loại khi emit).
- [x] **Step 5 (verify):** chạy trên dev — bấm chip "Công nghiệp": ô Lĩnh vực hiện "Công nghiệp",
  chip sáng, danh sách còn 95; bấm lại chip: ô lọc trống, chip tắt, về 104. Chiều ngược lại: chọn
  "Thành phố Hà Nội" ở ô lọc → chip thị trường tự sáng, danh sách còn 22. 0 lỗi console.

> ℹ️ **Điểm còn tồn** — user chốt **BỎ QUA**: chip "Chưa xác định" (id rỗng) không biểu diễn được
> bằng ô lọc vì BE bỏ qua tham số rỗng. Trước đây cũng đã không bấm được, không phải lỗi mới.

---

### Task 7.5 — Header popup: "N / M nhu cầu" với M là tổng TRƯỚC bộ lọc (2026-08-28)

User chốt sửa luôn điểm tồn số 2 của Task 7.4.

**Nguyên nhân gốc:** `demandList()` của service áp luôn bộ lọc riêng của popup rồi mới trả về, nên
controller lấy `total = $demands->count()` chính là số dòng SAU khi lọc → header luôn ra "22 / 22"
và câu "đang lọc trong N nhu cầu" vô nghĩa. Mockup dùng 2 tập khác nhau:
`renderDrillBody()` có `all = drillDemands(key)` (chưa lọc) và `rows = drillFiltered()` (đã lọc),
rồi in `rows.length + ' / ' + all.length`.

- [x] **Step 1 (BE):** Tách `demandListBase()` (danh sách của ô drill, CHƯA áp bộ lọc popup) khỏi
  `demandList()`; `applyDrillFilters()` đổi `private` → `public` để controller ghép 2 bước mà chỉ
  gom nhóm chỉ tiêu 1 lần.
- [x] **Step 2 (BE):** Controller trả `total` = `$base->count()`; `total_amount` / `rows` / `kpis`
  / `cross_stats` **vẫn tính trên danh sách ĐÃ lọc** (đúng mockup: số tiền là của phần đang xem).
  `PotentialCustomerCarePrintService` vẫn gọi `demandList()` nên bản in không đổi.
- [x] **Step 3 (FE):** Dòng tóm tắt đảo lại cho khớp mockup —
  `{{ rows.length }} nhu cầu · <tiền> · Kỳ … · đang lọc trong {{ total }} nhu cầu`;
  `isFiltered` đổi từ "có ô lọc nào được chọn" sang `rows.length !== total` (mockup:
  `rows.length !== all.length`) để chọn giá trị mà không cắt dòng nào thì không hiện đuôi thừa.
- [x] **Step 4 (test):** Bổ sung 4 assertion vào e2e ca 4 (`potential-customer-care.spec.ts`):
  ô lọc hiện đúng tên chip vừa bấm · `care-drill-count` = `N / M` · dòng tóm tắt có
  "đang lọc trong M nhu cầu" · bỏ chip thì ô lọc trống và về `M / M`.
- [x] **Step 5 (verify):** **31/31 e2e xanh**. Đã kiểm test có "răng": cố tình trả `total` về số
  đã lọc → ca 4 FAIL đúng như mong đợi, khôi phục lại thì xanh. Kiểm tay trên dev: chưa lọc
  "104 / 104 nhu cầu" không có đuôi; bấm chip Hà Nội → "22 nhu cầu · 53.900.000.000 đ · Kỳ … ·
  đang lọc trong 104 nhu cầu" và badge "22 / 104 nhu cầu".

---

### Task 7.6 — Popup: bấm "Xoá lọc" làm mất chế độ phóng to (2026-08-28)

User: phóng to popup → lọc → bấm Xoá lọc → popup tự thu nhỏ lại.

**Nguyên nhân gốc:** `clearFilters()` gọi chung `resetLocal()`, mà hàm này ngoài bộ lọc còn set
`fullscreen = false` và `summaryCollapsed = false` (nó vốn dành cho lúc MỞ popup mới). Mockup tách
đôi rõ ràng: `resetDrillFilters()` chỉ xoá ô tìm kiếm + các select, còn `openDrill()` mới bỏ class
`minutes-modal--full`.

- [x] **Step 1:** Tách `resetFilters()` (keyword + filters) khỏi `resetLocal()` (trạng thái xem +
  gọi lại `resetFilters()`); `clearFilters()` dùng `resetFilters()`, watcher `drillKey` giữ
  `resetLocal()`.
- [x] **Step 2 (test):** Nối tiếp e2e ca 7: phóng to → bấm chip lọc → bấm Xoá lọc → khẳng định
  danh sách về đủ dòng, chip tắt, nút vẫn là "Thu nhỏ popup" và `.care-drill-dialog--full` còn đó.
- [x] **Step 3 (verify):** **31/31 xanh**. Test có "răng": trả `clearFilters()` về gọi
  `resetLocal()` → ca 7 FAIL, khôi phục thì xanh. Kiểm tay trên dev: phóng to → lọc "Thành phố
  Hà Nội" (22/104) → Xoá lọc → vẫn full màn hình, về 104/104, ô lọc trống.

> ℹ️ Lệch mockup còn lại (CHƯA sửa, chờ user quyết): mockup `openDrill()` bỏ chế độ phóng to ở
> **mọi lần mở**, còn bản hiện tại chỉ reset khi `drillKey` ĐỔI — đóng rồi mở lại ĐÚNG con số cũ
> thì popup vẫn giữ phóng to. Mở con số khác thì vẫn về khổ thường.

---

### Task 7.7 — Popup: bấm số trong hộp KPI không có tác dụng (2026-08-28)

User: khối KPI trên popup, bấm vào con số không ra gì.

**Nguyên nhân gốc:** `KpiBoxes.vue` vẽ con số bằng `DrillNum` (thẻ `<button>`, có gạch chân + con
trỏ tay) và `$emit('drill')`. Màn chính nối sự kiện này (`CareSummaryBlocks` → `index.openDrill`)
nên bấm được; còn `DemandListModal` dùng lại đúng component đó nhưng **quên nối `@drill`** → nút
nhìn như bấm được mà không có gì xảy ra.

- [x] **Step 1:** `DemandListModal` nối `@drill="onKpiDrill"`; `index.vue` nối `@drill="openDrill"`
  cho chính popup (trước đó popup chỉ emit filter/print/export/close).
- [x] **Step 2:** `onKpiDrill()` lọc sâu vào ĐÚNG tập của KPI, giữ nguyên chỉ tiêu đang xem:
  `<key hiện tại>@won` (2 hộp chuyển đổi) / `@lost` (hộp thất bại) — cùng cơ chế với cột "Chuyển
  đổi thành công" / "Không tiếp tục" của bảng theo dõi. Bấm lại khi đã ở đúng tập thì bỏ qua.
- [x] **Step 3:** Thêm cờ `keepView` — drill phát sinh NGAY TRONG popup chỉ xoá bộ lọc, KHÔNG kéo
  popup từ phóng to về khổ thường (nối tiếp Task 7.6).
- [x] **Step 4 (test):** e2e ca 12 mới: phóng to → bấm số hộp KPI 1 → số dòng = tử số, tiêu đề
  popup đổi thành nhãn KPI, badge `N / N`, mọi dòng đều "Đã lập dự án TKT", popup VẪN phóng to.
- [x] **Step 5 (verify):** **32/32 xanh**. Test có "răng": gỡ `@drill` khỏi `KpiBoxes` trong popup
  → ca 12 FAIL, nối lại thì xanh. Kiểm tay: bấm hộp 3 (17/37) → còn 17 dòng "Không tiếp tục",
  tiêu đề "Thất bại / tổng nhu cầu đóng".

- [x] **Step 6 (user chốt 2026-08-28):** Đang lọc sâu thì **bỏ hẳn khối KPI** (nó nói về tập CHA,
  để lại chỉ gây hiểu nhầm) và thay bằng dải **"← Quay lại"** + dòng "Đang xem sâu trong: <chỉ tiêu
  cũ>". Nút theo `.claude/skills/button-convention` — nhóm Quay lại là `tertiary size="sm"` + icon
  `ri-arrow-left-line`. Trước đó BE đã tự trả `kpis: []` cho nhánh `@lost`, nhưng nhánh `@won` vẫn
  còn KPI nên phải ẩn ở FE bằng chính cờ `backTo`.
- [x] **Step 7:** `backTo` bị xoá khi mở chỉ tiêu mới (`resetLocal`) VÀ khi đóng popup — nếu không,
  mở lại đúng key cũ (vd bấm cột "Chuyển đổi thành công" ra `all@won`) sẽ thấy nút "Quay lại" treo
  lại từ lần trước. Bấm Quay lại cũng đặt `keepView` nên không thu nhỏ popup.
- [x] **Step 8 (verify):** e2e ca 12 kiểm thêm: sau khi lọc sâu thì `.drill-kpibox .rsum-kpi` = 0,
  dải Quay lại hiện đúng tên chỉ tiêu cũ; bấm Quay lại thì tiêu đề/badge về như cũ, KPI hiện lại đủ
  3 hộp, dải Quay lại biến mất, popup vẫn phóng to. **32/32 xanh.**

---

### Task 7.8 — Cột "Meeting thu thập nhu cầu" trong popup (2026-08-28)

User hỏi 3 việc: data đã thật chưa · chưa bấm được để xem chi tiết meeting · chưa có nhãn kỳ trước.

**(1) Data THẬT** — `PotentialCustomerCareService::getDemands()` `join('meetings', …)` lấy
`meetings.code / name / start_date`, không có chỗ nào chế dữ liệu. (Số trên DB local đang là bản
ghi do `assign:seed-care-demo` sinh, mã `DEMO-CSKH-*` — dữ liệu demo nhưng đi đúng đường thật.)

**(2) Bấm mở panel chi tiết meeting**

- [x] **Step 1:** Rà repo trước — panel đã có sẵn:
  `pages/assign/my-todo/components/calendar/MeetingDetailDrawer.vue` (props `show` + `meetingId`,
  tự gọi `assign/meeting/{id}`). Dùng lại nguyên, KHÔNG viết panel thứ hai.
- [x] **Step 2:** Cột Meeting đổi tên meeting thành link; bấm -> popup emit `open-meeting`,
  màn cha **đóng popup danh sách rồi mới mở panel** — đúng mockup
  (`closeModal('drill'); openMeetingDrawer(...)`) và cũng là bắt buộc kỹ thuật: panel có
  `z-index` 1040/1041, thấp hơn `.modal` 1050 của bootstrap-vue, mở chồng lên là bị che.
- [x] **Step 3:** Nối nốt 2 nút trong panel để không thành nút chết: `@edit` -> điều hướng
  `/assign/meeting/{id}/edit` (giống màn Lịch của tôi); `@view-report` -> dùng lại
  `reportPrintPreviewMixin.loadPrintPreview('assign/meeting/{id}/print', …)` + đúng cái
  `ReportPrintPreviewModal` màn báo cáo đã có, không dựng popup in thứ hai.

**(3) Nhãn "Kỳ trước"**

- [x] **Step 4 (BE):** `groupByIndicator()` gán `is_carried` thẳng lên model (`filter()` giữ
  nguyên tham chiếu nên gán trên nhóm `carried` là gán luôn vào `all`), Resource trả thêm
  `is_carried`. KHÔNG tính lại điều kiện ở FE để 2 nơi không thể lệch nhau.
- [x] **Step 5 (FE):** Dòng phụ của ô Meeting: `<mã> · Họp <ngày>` + chip **"Kỳ trước"** (viền
  vàng `#fcd34d`, chữ `#b45309`) khi `is_carried`.
- [x] **Step 6:** Bản in danh sách + Excel danh sách cũng ghi `(kỳ trước)` sau tên meeting —
  mockup có trong hàm `val()` dùng cho export.
- [x] **Step 7 (verify):** e2e ca 13 mới — số link meeting = số dòng; **số chip "Kỳ trước" phải
  bằng ĐÚNG ô "Tổng nhu cầu còn hiệu lực theo dõi" của khối tổng hợp** (81/104 trên DB local);
  bấm link thì popup đóng, panel mở và có nội dung thật. **33/33 xanh.**

> ⚠️ Trên DB local thiếu print template `BIEN_BAN_CUOC_HOP` nên nút "Xem biên bản" trong panel sẽ
> báo lỗi tải — lỗi dữ liệu môi trường, không phải lỗi code (xem ghi chú cũ ở STATUS).

---

### Task 7.9 — Panel chi tiết meeting quá ít thông tin (2026-08-28)

User: panel mở từ cột Meeting rất ít thông tin, không có thành phần tham gia, không có nút xem
biên bản.

**Chẩn đoán (đã đo bằng API thật, không đoán):**
`MeetingDetailDrawer.vue` **vốn ĐÃ có** đủ khối "Khách hàng & người liên hệ", "Thành phần tham dự"
(chip công ty + chip khách hàng), "Nội dung / Mục tiêu", "Kết luận & ghi chú" và nút "Xem biên bản"
(hiện khi `reports.length > 0`). Tất cả đều `v-if` theo dữ liệu. Gọi thẳng `assign/meeting/{id}`:

| Meeting | company_members | customer_members | reports | customer_name |
| --- | --- | --- | --- | --- |
| TPE.MET.NB.26.0001 (tạo bằng UI) | 19 | 0 | 2 | – |
| TPE.MET.NB.26.0009 | 27 | 0 | 5 | – |
| DEMO-CSKH-001 · E2E-CARE-* (seed) | **0** | **0** | **0** | **null** |

=> Panel rỗng vì **dữ liệu seed mỏng**, không phải component thiếu khối. Mọi meeting mà báo cáo
này với tới trên DB local đều là bản ghi seed.

**Cái THIẾU THẬT so với mockup:** khối **"Nhu cầu thu thập được"** (dữ liệu của chính DÒNG NHU CẦU,
API meeting không thể có) và nút **"Tạo dự án TKT"**.

- [x] **Step 1 (user chốt):** sửa component dùng chung `MeetingDetailDrawer.vue` (đã hỏi trước theo
  CLAUDE.md), footer lấy bộ "mockup + Xem biên bản".
- [x] **Step 2:** Thêm 2 prop **truyền bằng DỮ LIỆU**, không dùng slot: `extraBlocks`
  (`[{ title, fields: [{ label, value, full?, color? }] }]`, `color` -> badge chấm màu) và
  `extraActions` (`[{ key, label, primary? }]` + emit `extra-action`).
  ⚠️ Lý do không dùng slot: style của drawer là `scoped`, nội dung slot biên dịch ở scope CHA nên
  KHÔNG ăn được `.drawer-block` / `.btn-primary` của con — slot sẽ ra khối trần không style.
  Thay đổi thuần bổ sung: prop mặc định `[]`, màn Lịch của tôi không đổi hành vi.
- [x] **Step 3:** Báo cáo truyền khối "Nhu cầu thu thập được" 10 trường (Khách hàng · Thị trường /
  Phường xã · Kinh doanh chủ trì · Lĩnh vực · Nhóm ngành · Trạng thái nhu cầu (badge) · Tổng giá
  trị đầu tư · Thời gian triển khai · DV sửa chữa · Dự án TKT) — lấy từ CHÍNH dòng đã bấm nên
  panel luôn có nội dung kể cả khi cuộc họp chưa nhập gì. `open-meeting` nay emit cả `row`.
- [x] **Step 4:** Nút "Tạo dự án TKT" — hiện khi `can_create_project` VÀ nhu cầu chưa có dự án VÀ
  còn "Đang theo dõi" (đúng điều kiện của nút "+ Tạo mới" ở cột Dự án TKT trong popup, fail-closed).
- [x] **Step 5 (verify):** e2e ca 13 kiểm thêm 10 nhãn của khối mới. **33/33 xanh.** Chạy tay:
  panel hiện đủ khối; bật tạm cờ quyền thì footer ra đúng nút "Tạo dự án TKT".

> ℹ️ **Còn tồn — chờ user quyết:** muốn panel trông "đầy" khi demo trên VPS thì phải bổ sung
> `SeedCareReportDemoCommand` sinh thêm thành phần tham dự / khách hàng / nội dung / biên bản cho
> meeting demo (kèm dọn dẹp trong `--clean`). Chưa làm vì đụng lệnh sinh dữ liệu.

---

### Task 7.10 — Popup: căn giữa cột Trạng thái + sắp xếp 5 cột cơ cấu (2026-08-28)

- [x] **Step 1:** Cột "Trạng thái" thêm `cellClass: 'care-drill-table__center'` — đúng mockup
  (`td class="drill-table__center"` cho badge trạng thái), chỉ căn giữa Ô, tiêu đề giữ nguyên.
- [x] **Step 2:** 5 cột cơ cấu (Lĩnh vực · Nhóm ngành · Thị trường/Phường xã · Phòng · Kinh doanh
  chủ trì) gắn `sortable: true`. Tiêu đề bấm được, **copy khuôn `.sortable-header` của
  `V2BaseDataTable`**: icon `ri-arrow-up-down-line` khi chưa sắp, `ri-arrow-up-line` /
  `ri-arrow-down-line` khi tăng/giảm; bấm lại là đảo chiều (không có trạng thái "bỏ sắp").
- [x] **Step 3:** Sắp xếp **TẠI CHỖ** ở FE (`sortedRows`), không gọi lại API — popup vốn đã tải
  trọn tập của ô số đã bấm. 2 điểm phải nhớ:
  · Cột "Thị trường / Phường xã" hiện 2 dòng nên khoá sắp xếp phải ghép `province_name` +
    `ward_name` (`sortFields`), nếu chỉ lấy 1 trường thì thứ tự không khớp chữ đang nhìn thấy.
  · `localeCompare(…, 'vi')` để Đ/Ê/Ơ đứng đúng bảng chữ cái; ô trống luôn xuống cuối ở CẢ 2 chiều.
- [x] **Step 4:** `resetLocal()` xoá luôn trạng thái sắp xếp khi mở chỉ tiêu khác; "Xoá lọc" thì
  KHÔNG đụng (sắp xếp không phải bộ lọc).
- [x] **Step 5 (verify):** e2e ca 14 mới — đúng 5 cột có nút sắp xếp, `text-align` ô Trạng thái =
  `center`, bấm tăng dần thì mảng khớp `localeCompare('vi')`, bấm lần 2 ra đúng thứ tự đảo ngược,
  icon đổi đúng. **34/34 xanh** (chạy 2 lần).

---

### Task 7.11 — BUG 4 (cột Dự án TKT) + BUG 5 (thứ tự danh sách) (2026-08-28)

**BUG 4a — nút "+ Tạo mới" không bao giờ hiện. NGUYÊN NHÂN GỐC:** màn gate bằng
`hasAPermission('Quản lý dự án tiền khả thi')` — **quyền này KHÔNG TỒN TẠI** trong
`PermissionsTableSeeder`. Đã đo trên tài khoản 563 quyền: tên đó `false`, còn 4 quyền thật
`Xem danh sách dự án tiền khả thi theo tổng công ty|công ty|phòng ban|bộ phận` đều `true`.

- [x] **Step 1:** `can_create_project` đổi sang OR của 4 quyền có thật. Chọn nhóm này vì phân hệ
  Dự án TKT **không có** quyền "tạo" riêng, và nút "Thêm mới" ở `/assign/prospective-projects`
  vốn không gate — ai xem được danh sách thì tạo được. Vẫn fail-closed (không hard-code `true`).
- [x] **Step 2:** Nút bổ sung icon `ri-add-line` qua `#prefix` + bỏ dấu "+" trong chữ, theo
  `.claude/skills/button-convention` (mọi `V2BaseButton` phải có icon).

**BUG 4b — mã dự án chưa bấm được**

- [x] **Step 3:** Ô có `prospective_project_id` -> render `<a>` mở
  `/assign/prospective-projects/{id}/manager` ở **tab mới** (giữ nguyên báo cáo + popup đang xem,
  cùng cách với nút Tạo mới).
- [x] **Step 4 (bẫy):** Ban đầu dùng chung class `care-drill-meeting` cho cả link meeting lẫn link
  dự án -> e2e ca 13 đếm ra 122 thay vì 104 và ca 15 bấm nhầm link meeting. Tách thành
  `.care-drill-link` (style dùng chung) + `.care-drill-meeting` / `.care-drill-project` (định danh).

**BUG 4c — "dữ liệu dự án chỉ là demo":** đã kiểm bằng API, dữ liệu **LẤY THẬT** từ bảng
`prospective_projects` (vd `id=183` trả về đầy đủ qua `/assign/prospective-projects/183`). Chỉ là
các bản ghi đó do `assign:seed-care-demo` sinh nên mã/tên mang chữ "demo" và phần lớn trường rỗng.
Không phải lỗi code — cùng gốc với ghi chú ở Task 7.9.

**BUG 5 — danh sách đang cũ→mới**

- [x] **Step 5:** Query đổi `orderBy('meetings.start_date')` -> `orderByDesc` + `orderByDesc(id)`
  (thứ tự xác định, không phụ thuộc MySQL).
- [x] **Step 6 (bẫy, đã dính):** Đổi mỗi query là CHƯA ĐỦ — `groupByIndicator()` ghép
  `carried->concat($arisen)` nên danh sách ra **2 cụm** (kỳ trước trước, trong kỳ sau), nhìn vẫn
  như sắp sai. Thêm helper `sortNewestFirst()` và áp cho cả `all` lẫn `closed`.
- [x] **Step 7 (verify):** e2e ca 15 mới — ô có mã dự án đều bấm được, chỉ nhu cầu "Đã lập dự án
  TKT" mới có link, mọi nhu cầu "Đang theo dõi" đều có nút Tạo mới, ngày họp theo thứ tự giảm dần,
  bấm mã dự án mở đúng tab `/assign/prospective-projects/{id}/manager`. **35/35 xanh.**

> ℹ️ Phát hiện khi viết test: fixture e2e có **2 nhu cầu** (`E2E-CARE-CUR`, `E2E-CARE-PREV`) để
> trạng thái "Đã lập dự án TKT" mà KHÔNG gắn dự án nào -> ô hiện `—`. Là dữ liệu fixture bất
> thường, không phải lỗi màn; test vì vậy bám theo "ô có mã dự án hay không", không bám trạng thái.

---

### Task 7.12 — "Tạo mới" chưa chọn sẵn Khách hàng + Nhu cầu (2026-08-28)

**Nguyên nhân gốc:** báo cáo đã gửi `?customer_id=&demand_id=` từ đầu, nhưng
`pages/assign/prospective-projects/add.vue` **không đọc `$route.query`** cho 2 tham số này (chỉ
xử lý `parent_id`) -> mở ra form trắng.

- [x] **Step 1:** Thêm `applyCustomerFromQuery()` vào `add.vue`, gọi trong `mounted()` ngay sau
  `applyParentFromQuery()` — bám đúng khuôn sẵn có của chính màn đó.
- [x] **Step 2:** Không tự map tay thông tin KH mà **gọi lại `CustomerInfoSection.handleCustomerEvent()`**
  (luồng chọn KH thật, tự gọi `assign/customers/{id}?all_business=1` để lấy mã/MST/địa chỉ/loại
  hình…) -> 2 đường vào không thể lệch dữ liệu.
- [x] **Step 3 (thứ tự BẮT BUỘC):** set `customer_demand_id` **TRƯỚC** khi nạp KH. `CustomerBlock`
  nạp options nhu cầu ngay lúc `customer_id` đổi và truyền `include_id` = nhu cầu đang gắn; set
  sau thì option không chứa id đó -> select hiện rỗng dù form giữ đúng giá trị.
- [x] **Step 4 (bẫy quyền, đã đo):** `assign/customers/{id}` trả **403** "Bạn không có quyền xem
  khách hàng này" với tài khoản không có quyền ERP xem KH (Redmine #10903) -> `handleCustomerEvent`
  rơi về object truyền vào, mà object đó chỉ có `id` nên ô Khách hàng TRỐNG. Báo cáo nay gửi kèm
  `customer_name` + `customer_code` làm dữ liệu dự phòng.
- [x] **Step 5 (verify):** e2e ca 16 mới — bấm "Tạo mới" mở tab có đủ `customer_id`/`demand_id`,
  `customer_name` bên màn tạo khớp ĐÚNG tên KH của dòng đã bấm, `customer_demand_id` > 0 và ô
  "Nhu cầu khách hàng" hiện đúng nhu cầu. **36/36 xanh.**

- [x] **Step 6 (user báo lại: nhu cầu có, KH vẫn trống):** làm cho việc điền **không phụ thuộc
  thứ tự** nữa, 3 nhịp: (1) `updateForm` điền ngay `customer_id/name/code` + `customer_demand_id`
  ngay khi mở màn, không chờ API; (2) gọi `handleCustomerEvent` để làm giàu; (3) **gán lại** 4
  trường gốc sau khi await. Lý do nhịp (3): `handleCustomerEvent` dựng payload từ bản chụp
  `formSubmit` TRƯỚC lúc await, nên bất kỳ khối nào emit `update` trong lúc chờ API (`ProjectInfo`,
  `ProgressFinance`, `loadScopeOptions`…) đều có thể đè mất phần khách hàng — đúng triệu chứng
  "nhu cầu có, KH trống".
- [x] **Step 7 (verify):** e2e ca 16 kiểm thêm **giao diện**: đọc `input.value` (property) và
  khẳng định có ô hiện đúng tên KH — trước đó chỉ kiểm state nên loại lỗi này lọt lưới.
  (Selector `input[value=…]` KHÔNG dùng được: Vue bind `:value` nên thuộc tính HTML không đổi.)
  **36/36 xanh.**

- [x] **Step 8 (user chốt 2026-08-28):** Vào bằng link có param thì **KHOÁ** cả 2 ô, không cho
  chọn lại — đổi KH ở đây là nhu cầu đang gắn thành của khách khác (`CustomerBlock` tự xoá nhu cầu
  khi đổi KH). Cờ `lockCustomerFromQuery`:
  · Ô Khách hàng: dùng lại prop `lock-direct-customer` CÓ SẴN của `CustomerInfoSection` (đúng khuôn
    `MeetingProject.vue` — KH kế thừa từ nơi khác), placeholder "Khách hàng theo nhu cầu đã chọn".
    `openPicker()` đã tự chặn khi `lockPicker`, ô vốn `readonly` nên bấm không mở popup chọn KH.
  · Ô Nhu cầu khách hàng: **thêm prop mới** `lock-demand` xuyên `CustomerInfoSection` →
    `CustomerBlock` (`:disabled="isShow || !val('id') || lockDemand"`). Trước đó không có đường nào
    khoá riêng ô này.
- [x] **Step 9 (verify):** e2e ca 16 kiểm thêm: select Nhu cầu có class `select2-container--disabled`,
  ô Khách hàng mang đúng placeholder khoá, bấm vào ô Khách hàng KHÔNG mở popup chọn KH. **36/36 xanh.**

> ⚠️ `CustomerBlock.vue` là file **CRLF** — sửa bằng script Python phải mở `newline=''` cho cả đọc
> lẫn ghi. Lần này đã lỡ ghi ra LF (diff phình 1482 dòng), phát hiện bằng `git diff --stat` rồi
> chuyển lại CRLF ngay, diff về đúng 9 dòng.

> ℹ️ Với tài khoản thiếu quyền ERP xem KH, các ô MST / Địa chỉ / SĐT / Email vẫn hiện `-` (API 403).
> Giống hệt khi chọn KH bằng modal, không phải lỗi của luồng này.

---

## Phase 8 — Seeder demo: dựng đúng cây Lĩnh vực ▸ Nhóm ngành + trải rộng Thị trường (2026-08-28)

User báo demo trên VPS (`HRM_TPE_CMC / hrm_erp_test`) **dồn hết nhu cầu vào lĩnh vực "Khác"** nên
khách hàng không soi được phần "Theo lĩnh vực".

**Nguyên nhân gốc (đo bằng 2 ảnh chụp bảng của user + DB local):** migration tạo lĩnh vực "Khác"
rồi gắn TOÀN BỘ nhóm ngành cũ vào đó. Cả 22 nhóm ngành hệ thống `NN.0001`–`NN.0022` vì thế dồn về
đúng MỘT lĩnh vực ở mọi môi trường — VPS là "Khác" (`LVKDNB.KHAC`), local là "Công nghiệp"
(`LVKDNB.IDUS`, id 24). Không phải seeder tạo ra chúng: seeder cũ **chưa từng ghi** vào 2 bảng
danh mục, nó chỉ *dùng lại* thứ có sẵn nên môi trường nào demo nấy.

Phương án user chốt (3 lựa chọn đã trình): **gán 22 nhóm ngành THẬT vào 7 lĩnh vực THẬT** của khách
(`LVKDNB.0001`–`0007`), không đẻ thêm bộ danh mục demo song song.

### Task 8.1 — BE: bảng ánh xạ + bước gán lĩnh vực

- [x] **Step 1:** Hằng `SCOPE_FIELD_MAP` — 22 nhóm ngành xếp vào 7 lĩnh vực: Công nghiệp (6) ·
  Môi trường (4) · Ngành ô tô (3) · Giải pháp quản trị số (4) · Tiện ích công cộng (2) ·
  Năng lượng và hạ tầng (2) · Giáo dục đào tạo (1).
  ⚠️ Khớp lĩnh vực theo **TÊN đã chuẩn hoá**, KHÔNG theo mã — mã lĩnh vực mỗi môi trường một kiểu
  (`LVKDNB.IDUS` local vs `LVKDNB.0001` VPS), trong khi mã nhóm ngành `NN.*` thì giống nhau.
  `normalizeName()` bỏ dấu (`Str::ascii`) + bỏ ký tự không phải chữ/số → `"Giáo dục & Đào tạo"`
  ≡ `"Giáo dục đào tạo"`.
- [x] **Step 2:** `planScopeFieldMapping()` dựng kế hoạch (chưa ghi) để bảng xác nhận in được số
  dòng sẽ đổi. **CHỐT CHẶN:** chỉ gán khi 22 nhóm ngành đang dồn về đúng 1 lĩnh vực (hoặc chưa có);
  nếu đã nằm ở ≥ 2 lĩnh vực nghĩa là khách tự phân loại rồi → bỏ qua + in cảnh báo, KHÔNG đè.
- [x] **Step 3:** `applyScopeFieldMapping()` + `resolveFieldId()` — lĩnh vực nào môi trường chưa có
  thì tạo mới (`code` = `LVKDNB.<SLUG>`, cắt 40 ký tự, đụng UNIQUE thì thêm số đuôi). Chạy SAU bước
  hỏi xác nhận; xong phải `fetchScopes()` **đọc lại** vì `$source['scopes']` lấy trước đó còn giữ
  lĩnh vực cũ, dùng tiếp là nhu cầu demo ghi tên "Khác" vào cột denormalize.
- [x] **Step 4:** Cờ `--no-map-scopes` để tắt; bảng xác nhận thêm dòng "Nhóm ngành sẽ gán lại lĩnh
  vực"; `--clean` in rõ **KHÔNG hoàn tác** việc gán (đó là sửa danh mục cho đúng, không phải rác demo).
- [x] **Step 5 (verify):** `--dry-run` báo 16 dòng sẽ đổi (6 nhóm đã đúng "Công nghiệp" nên không
  đếm) → chạy thật → chạy LẦN 2 ra "đã được phân vào 7 lĩnh vực — bỏ qua", không ghi đè. Nhu cầu
  demo nhóm theo lĩnh vực ra **7 dòng** với đúng 6/4/4/3/2/2/1 nhóm ngành.
- [x] **Step 6 (verify — mô phỏng ĐÚNG tình trạng VPS trên local):** dựng lĩnh vực `LVKDNB.KHAC`
  "Khác" rồi dồn cả 22 nhóm ngành vào (khớp hệt ảnh chụp VPS của user) → `--dry-run` báo **22 dòng
  sẽ đổi** → chạy thật: gán đúng 22, **KHÔNG tạo lĩnh vực thừa** (dùng lại 7 cái có sẵn), "Khác"
  về 0 nhóm ngành. Xoá bản ghi "Khác" dựng để mô phỏng sau khi kiểm (không bản ghi nào tham chiếu).

### Task 8.2 — BE: nguồn nhóm ngành phải giống nhau mọi môi trường

- [x] **Step 1:** `fetchScopes()` ưu tiên đúng bộ 22 nhóm ngành hệ thống; chỉ khi môi trường thiếu
  (< 3) mới lấy tất cả. Trước đó local lôi cả nhóm ngành rác của e2e (`NN.E2E1/2`) vào demo → dòng
  "E2E Lĩnh vực khảo sát" 12 nhu cầu, demo local ≠ demo VPS đúng thứ Phase này muốn dẹp.
- [x] **Step 2:** Con trỏ chọn nhóm ngành chạy **liên tục** (`$scopeCursor++`) thay vì `($i * 4 + $j)`.
  Công thức cũ chỉ sinh 6 gốc (0,4,8,12,16,20) mà mỗi meeting tiêu thụ 2-4 giá trị → chỉ chạm
  **18/24 nhóm ngành**, 6 nhóm không bao giờ tới lượt nên lĩnh vực cha hiện thiếu nhóm ngành
  (Công nghiệp ra 4/6, Môi trường 2/4, Giải pháp quản trị số 2/4).
  Seed của `pickLifecycle()` giữ nguyên `($i * 4 + $j)` — tách khỏi việc chọn nhóm ngành, đúng
  nguyên tắc "trạng thái và mốc đóng quyết định độc lập" đã ghi ở docblock hàm đó.

### Task 8.3 — BE: trải rộng phần "Theo thị trường"

- [x] **Step 1:** `PROVINCE_LIMIT` 10 → **15 tỉnh** (user chốt 15, bản đầu để 20); mỗi tỉnh lấy khách **khác phường/xã**
  (`unique('ward_id')`) — `limit(3)` theo id trước đây hay trúng cùng phường/xã nên mở cấp 2
  "Tỉnh ▸ Phường/xã" chỉ ra một dòng con.
- [x] **Step 2 (bug đi kèm):** xếp khách hàng **xen kẽ vòng tròn theo tỉnh**. Meeting chọn khách
  bằng `$customers[$i % count]`, danh sách cũ xếp gom-theo-tỉnh nên 40 meeting chỉ tiêu thụ 40 khách
  ĐẦU = 13 tỉnh đầu tiên, 7 tỉnh cuối trắng meeting và biến mất khỏi báo cáo.
- [x] **Step 3 (verify):** "Theo thị trường" ra **15 tỉnh** (45 khách hàng), mỗi tỉnh 2 phường/xã.

### Task 8.4 — E2E

- [x] **Step 1 (bug lộ ra nhờ data mới):** `potential-customer-care-export.api.spec.ts` ca 6 fail —
  `cross_stats` có nhãn `"Giáo dục & Đào tạo"` mà bản in không chứa. **Sản phẩm KHÔNG sai:** bản in
  là HTML dựng bằng Blade `{{ }}` nên `&` thành `&amp;`, trình duyệt hiện đúng. Lỗi ở assertion so
  chuỗi THÔ với HTML. Thêm helper `esc()` và bọc `customer_name`, `kpi.label`, `stat.label`,
  `item.label`. Trước đây mọi nhu cầu đều ở "Công nghiệp" nên chưa có tên nào chứa `&` để lộ.
- [x] **Step 2 (verify):** `npx playwright test potential-customer-care.api potential-customer-care-export.api`
  — **18/18 xanh**.
- [x] **Step 3 (verify UI):** `npx playwright test potential-customer-care.spec` — **19/19 xanh**
  (Nuxt node 12 + heap 8192, Playwright chạy bằng node 20). Bộ UI không hardcode tên/số danh mục,
  mọi số đều lấy động từ API nên trải rộng dữ liệu không làm vỡ ca nào.

---

## Phase 9 — Popup drill-down giật khi mở (2026-08-28)

User báo: popup mở lên bị giật vì **lấy kích thước của lượt mở trước**, load data xong lại chỉnh
lại theo data.

### Task 9.1 — Tái hiện + đo trước khi sửa

- [x] **Step 1:** Viết test tái hiện (chặn `**/demand-list?**` để bắt trạng thái popup ĐÚNG lúc vừa
  hiện), mở chỉ tiêu 32 dòng → đóng → mở chỉ tiêu 2 dòng. Số đo:
  popup mở ra **32 dòng + 28 chip + 3 KPI của lượt trước, cao 662px**; data về còn
  **2 dòng + 4 chip, cao 568px** → lệch **94px**.
- [x] **Step 2:** Đo độ trễ `demand-list`: **314–773ms ngay trên local** → phương án "nạp xong mới
  mở popup" bị loại, nút sẽ cảm giác chết.

### Task 9.2 — Nguyên nhân gốc + sửa

**Nguyên nhân gốc:** `index.vue::openDrill()` bật `drill.visible = true` **TRƯỚC** rồi mới
`await fetchDrill()`, mà `rows`/`kpis`/`crossStats`/`total` (đều là prop của popup) **không được
dọn**. Trong lúc chờ API popup vẽ nguyên nội dung lượt trước — sai số liệu trong chớp mắt, và số
dòng cũ quyết định luôn chiều cao. Cộng thêm `.care-drill-content { max-height: 92vh }` khiến chiều
cao chạy theo số dòng.

- [x] **Step 1:** `resetDrillData()` dọn `rows/crossStats/kpis/total/totalAmount` + bật
  `drill.loading` **trước** khi `visible = true`; gọi cả ở `onDrillFilter` (lọc lại trong popup
  cũng không được giữ dòng cũ). `fetchDrill()` tắt `loading` ở `finally`.
- [x] **Step 2:** Popup nhận prop `loading`: dòng rỗng hiện "Đang tải…" thay vì "Không có nhu cầu
  nào khớp bộ lọc" (nếu không sẽ báo sai trong lúc chờ); dòng phụ header và ô đếm `N / M` ẩn đi
  thay vì khoe `0 / 0`.
- [x] **Step 3:** `.care-drill-content`: `max-height: 92vh` → **`height: 92vh`**. Khoá cứng thì số
  dòng không còn quyết định kích thước → popup đứng yên tuyệt đối.
  ⚠️ Đã cân nhắc phương án dựng khung xương theo số dòng (mọi chỗ `$emit('drill')` đều có sẵn
  `count`) nhưng khung xương không khớp chiều cao thật (ô Khách hàng 2 dòng, ô khác 1 dòng) nên vẫn
  còn lệch — bỏ.
- [x] **Step 4:** Hệ quả của Step 3: danh sách ngắn để lại khoảng trắng, nội dung lửng lơ giữa
  khung. Cho `.modal-body` thành flex-column, `.care-drill-scroll` giãn (`flex: 1 1 auto`), footer
  `flex-shrink: 0` → footer ghim đáy, hộp trông có chủ đích. KHÔNG đổi phần tử nào chịu trách nhiệm
  cuộn (giữ `overflow-y: auto` ở `.modal-body`) để không sinh cuộn lồng cuộn.

### Task 9.3 — E2E

- [x] **Step 1:** Gộp test tái hiện thành **ca 17** của `potential-customer-care.spec.ts`: chặn API,
  khẳng định popup vừa mở **0 dòng dữ liệu cũ · 0 chip · 0 KPI**, dòng rỗng đúng chữ "Đang tải…", và
  **chiều cao lúc mở = chiều cao sau khi có data**.
- [x] **Step 2 (verify):** trước khi sửa ca này FAIL (32 dòng cũ, 662→568); sau khi sửa
  **20 UI + 18 API = 38/38 xanh**.

---

## Phase 10 — Footer đè nội dung + phân trang popup (2026-08-28)

### Task 10.1 — Sửa footer trong suốt, nút đè lên nội dung (HỒI QUY của Task 9.2 Step 4)

**Nguyên nhân gốc:** bước ghim footer để `.modal-body` vừa `overflow-y: auto` vừa flex-column,
`.care-drill-scroll` lại `min-height: 0` → bảng dài **tràn khỏi ô flex mà không bị cắt** và chạy
xuyên qua footer đang ghim. Đo được: bảng cao **1674px, đáy y=2052** trong khi thân popup chỉ
760px và footer ở **y=803**.

- [x] **Step 1:** Chuyển phần tử cuộn dọc từ `.modal-body` xuống `.care-drill-wrap`
  (`.modal-body` → `overflow: hidden`, `.care-drill-wrap` → `overflow: auto` + `flex: 1 1 auto`).
- [x] **Step 2:** `.care-drill-scroll` đổi `min-height: 0` → `min-height: 120px` để khối lọc +
  phân bổ cao không bóp vùng bảng còn 0 trên màn hình thấp.
- [x] **Step 3 (lợi kèm theo):** `thead th { position: sticky; top: 0 }` trước đây ghim theo thân
  popup nên cuộn là **mất tên cột**; nay ghim đúng trong khung bảng.
- [x] **Step 4 (verify):** đáy vùng bảng **713** < đỉnh footer **803** (trước: 2052 vs 803).

### Task 10.2 — Phân trang cho popup

- [x] **Step 1:** Dùng lại `V2BasePagination` có sẵn (khuôn `QuotationProductSearchModal`), đặt
  thành một hàng riêng ngay trên hàng nút. **Client-side**: popup đã nhận trọn tập từ một request;
  chip lọc, sắp xếp, In danh sách, Xuất Excel vẫn chạy trên TOÀN TẬP → không đổi API, không đổi
  nội dung file xuất / bản in.
- [x] **Step 2:** Mặc định **20 dòng/trang**, tuỳ chọn `[20, 50, 100]`. STT đánh số **liên tục
  theo toàn tập** (`pageOffset + index + 1`), trang 2 bắt đầu từ 21.
- [x] **Step 3:** `safePage` KẸP trang trong `[1, pageCount]` — bộ lọc cắt danh sách ngắn lại mà
  `page` còn giữ số cũ thì sẽ ra trang trắng. Về trang 1 khi: mở popup mới (`resetFilters`), đổi
  bộ lọc/chip (`onFilterChange`), đổi cột sắp xếp (`toggleSort`). Đổi số dòng/trang cũng về 1.
- [x] **Step 4:** Sang trang mới thì cuộn bảng về đầu, không thì đang ở giữa trang cũ nhìn như
  chưa đổi gì.

### Task 10.3 — E2E

- [x] **Step 1:** Ca **18** — popup nhiều dòng: đáy `.care-drill-wrap` ≤ đỉnh `.care-drill-footer`,
  footer nằm trong popup, và cuộn xuống đáy vẫn thấy `thead`.
- [x] **Step 2:** Ca **19** — 104 dòng: trang 1 có 20 dòng và `Hiển thị 1-20 / 104`; sang trang 2
  STT bắt đầu **21**; đang ở trang 2 mà bấm chip thì về trang 1.
- [x] **Step 3 (cập nhật ca cũ theo hành vi mới):** thêm `onPage1(n) = min(n, 20)` bọc **13**
  assertion đếm dòng hiển thị. Ca **13** phải CỘNG DỒN qua các trang (nhãn "Kỳ trước" rải khắp
  danh sách, tập 104 dòng > cả mức 100/trang). Ca **14** đổi sang mở chỉ tiêu ≤ 20 dòng — phép
  kiểm "giảm dần = đảo của tăng dần" chỉ đúng khi cả tập nằm trên MỘT trang.
- [x] **Step 4 (verify):** **22 UI + 18 API = 40/40 xanh**.

> ⚠️ `b-pagination` render **`<button class="page-link">`**, KHÔNG phải `<a>`, và gắn
> `aria-label="Go to page N"` nên cả `li a` lẫn `getByRole('button', { name: 'N' })` đều KHỚP RỖNG.
> Phải bám text: `.b-pagination button.page-link` + regex `^N$`. Ca 19 lọt lưới một lượt vì ca 13
> fail trước nó trong chế độ `serial` nên nó chỉ hiện "did not run".

---

## Phase 11 — Panel chi tiết meeting mở ĐÈ lên popup (2026-08-28)

User báo: bấm xem chi tiết meeting trong popup thì popup bị đóng. Việc đóng vốn **cố ý** từ
Task 7.9 (panel `z-index` 1041 nằm dưới `.modal` 1050 nên mở đè sẽ bị popup che), nhưng hệ quả là
`@close` của panel chỉ tắt panel, KHÔNG mở lại popup -> mất danh sách, phải drill lại từ đầu.

User chốt (3 lựa chọn đã trình): **để cả hai cùng mở**, panel trượt ra đè lên popup.

### Task 11.1 — Nâng panel lên trên modal, CÓ ĐIỀU KIỆN

- [x] **Step 1:** `MeetingDetailDrawer.vue` thêm prop **`above-modal`** (mặc định `false`) → gắn
  class `above-modal` lên `.drawer-backdrop` (z-index 1059) và `.ticket-drawer` (1060), nằm trên
  `.modal` 1050 và `.modal-backdrop` 1040 của bootstrap-vue.
  ⚠️ KHÔNG nâng z-index toàn cục: panel này **dùng chung** với `my-todo/calendar`, nơi nó mở khi
  không có modal nào. Thay đổi là thuần cộng thêm, không bật prop thì hành vi y hệt trước.
- [x] **Step 2:** `index.vue::openMeetingDrawer()` bỏ dòng `this.drill.visible = false`; truyền
  `above-modal` cho panel.
- [x] **Step 3:** `b-modal` của popup thêm **`no-enforce-focus`** — focus-trap mặc định của
  bootstrap-vue kéo focus ngược về modal, panel nằm ngoài cây DOM của modal nên sẽ không thao tác
  được.
- [x] **Step 4 (verify):** panel hiện đè lên popup, đóng panel thì popup còn nguyên **đúng trang
  1/104, đúng bộ lọc** (không gọi lại API nên không nháy).

### Task 11.2 — E2E

- [x] **Step 1:** Ca **13** sửa lại theo hành vi mới: bỏ `expect('.care-drill-content').toBeHidden()`,
  đổi thành khẳng định popup **vẫn mở**, và so `z-index` thực tế của `.ticket-drawer` phải **lớn hơn**
  `.modal.show` — nếu không panel sẽ bị popup che, đúng lý do khiến bản đầu phải đóng popup.
- [x] **Step 2 (verify):** **22 UI + 18 API = 40/40 xanh**.

---

## Phase 12 — Nghi viền bảng bản in bị đôi — KHÔNG PHẢI LỖI (2026-08-28)

User báo bản in viền bảng bị double, nhìn rất đậm; popup xem trước trong app thì bình thường, bấm
In chuyển sang khung xem trước của Chrome mới đậm.

**Kết luận: KHÔNG có viền đôi. Không sửa gì.** Đo trên CHÍNH file PDF user lưu từ khung xem trước
của Chrome, dựng ảnh 257 dpi rồi lấy mặt cắt qua đường kẻ:
`255 255 255 232 51 51 140 255` — **một** vệt, dày ~2.7 px ảnh = đúng **1 px CSS**. Viền đôi thì
phải ra 2 cụm đậm cách nhau khe trắng, dày ~5.3 px. Toàn trang: 13 kẻ dọc + 15 kẻ ngang, đều
0.75–1.12 px CSS, **không cặp nào cách nhau < 8 px**.

Cũng đã đo và thấy CSS giống hệt nhau ở cả 3 nơi (popup xem trước · tài liệu in media screen ·
tài liệu in media print): `border-collapse: collapse`, ô 1px `#333`, khoảng cách 2 ô = 0. CSS in
vốn dùng CHUNG một nguồn `utils/print/reportPrintStyle.js`, chỉ khác gốc selector
(`.report-print-content` vs `body`).

**Vì sao nhìn đậm** (3 yếu tố, không phải lỗi CSS):
1. Khung xem trước Chrome hiển thị PDF ở tỉ lệ thu nhỏ; trình xem PDF luôn vẽ đường mảnh tối thiểu
   1 điểm ảnh màn hình → đường 1px bị kéo dày lên. Đây đúng là lý do "popup app không bị, preview
   trình duyệt mới bị".
2. Trên giấy bảng nén rất chặt (chữ 10px, ô cao ~11px, 13 cột trong 277mm) nên mật độ mực cao hơn
   hẳn popup xem trước rộng ~1140px.
3. Viền `#333` khá đậm, hàng tiêu đề còn có nền xám `#f5f5f5`.

> ⚠️ Một giả thuyết đã bị BÁC BỎ, đừng đi lại: nghi Chrome thu nhỏ trang do nội dung tràn khổ giấy.
> Đo ra `@page A4 landscape, margin 12mm 10mm` → vùng in được 277mm, bó nội dung vào đúng 1047px
> thì `TRAN: false` — bảng vừa khít, Chrome không cần thu nhỏ vì chiều rộng.

Nếu sau này user vẫn muốn nhẹ mắt hơn: đổi màu viền `#333` → `#666` (và/hoặc hạ `0.75pt`) trong
`utils/print/reportPrintStyle.js`. **Phải hỏi trước** — file đó dùng chung cho TẤT CẢ bản in báo
cáo (meeting-by-market, prospective-projects, task-manager…).

**Cách đo lại** (dùng cho mọi nghi vấn về bản in): chặn `print()` + `close()` của cửa sổ do
`window.open` mở để giữ lại đúng tài liệu sắp in → `page.pdf()` → `qlmanage -t -s 3000` dựng ảnh →
PIL đếm bề dày vệt mực. Máy chưa cài poppler nên `Read` không mở trực tiếp PDF được.

---

## Phase 13 — Lịch sử meeting với khách hàng trong popup drill-down (2026-08-31)

**Nhánh:** `bao_cao_cskh_lich_su_meeting`, tách từ `tpe` ở CẢ `hrm-api` và `hrm-client`.

**Yêu cầu user:** cột **Khách hàng** của popup chi tiết nhu cầu (`DemandListModal`) thêm nút mở
popup xem **lịch sử các cuộc meeting với khách hàng đó**. Lấy theo phân quyền; bấm từng meeting mở
chi tiết ở **tab trình duyệt khác**; sắp xếp **cũ → mới**.

**Quyết định đã chốt (hỏi user 2026-08-31):**

| # | Chốt |
|---|------|
| 1 | Phạm vi: **mọi loại meeting** với KH đó nhưng **chỉ trạng thái Hoàn thành** (`meetings.status = 3`). Không bó theo loại 7 như báo cáo — đây là "lịch sử", không phải mẫu số báo cáo |
| 2 | Quyền: **dùng lại nguyên `PotentialCustomerCareService::applyPermissionFilter()`** — 4 cấp, fallback = chủ trì **HOẶC** là thành viên. User ban đầu ghi "chỉ chủ trì" nhưng đã chốt đồng bộ với báo cáo, vì siết chặt hơn sẽ làm popup ẩn mất chính meeting đang hiện ngoài bảng (user dự họp nhưng không chủ trì) — trông như lỗi |
| 3 | Nút: **icon `ri-history-line`** cạnh tên KH (`V2BaseIconButton size="xs"`), KHÔNG biến tên KH thành link (dễ tưởng mở hồ sơ khách hàng) |
| 4 | 6 cột: `STT · Mã + Tên meeting · Thời gian họp (Từ–Đến) · Người chủ trì · Người liên hệ KH · Nhu cầu` |
| 5 | Cột Nhu cầu chỉ hiện **Có / Không** (user đổi ý, bỏ phương án Lĩnh vực + Giá trị dự kiến) → BE chỉ cần `withCount`, không trả chi tiết nhu cầu |
| 6 | Bỏ cột Loại meeting → BE **không phải join `meeting_types`** |

### Task 13.1 — BE: service + resource

- [x] **Step 1:** `PotentialCustomerCareService::customerMeetings(Request)` — `Meeting::query()`
  lọc `customer_id` + `status = Meeting::HOAN_THANH`, `withCount('investmentDemands')`,
  gọi `$this->applyPermissionFilter($query)` **nguyên vẹn** (hàm chỉ tham chiếu cột đã qualify
  `meetings.*`, mà query này chính là bảng `meetings` → chạy được, KHÔNG cần join thêm).
- [x] **Step 2:** Sắp `orderBy('meetings.start_date')` rồi `orderBy('meetings.id')` — **cũ → mới**,
  thứ tự phải xác định khi trùng ngày.
- [x] **Step 3:** phân trang theo `per_page` FE gửi (mặc định 20, **trần `MAX_PER_PAGE = 100`**);
  resolve tên người chủ trì **batch** đúng khuôn
  `attachOrganisation()` (id còn nhưng mất tên → "Chưa xác định người chủ trì").
- [x] **Step 4:** Resource `CustomerMeetingRowResource`: `id · code · name · start_date · end_date
  · host_name · customer_contact_name · has_demand`. Không trả trạng thái (đã lọc cứng Hoàn thành).

### Task 13.2 — BE: controller + route

- [x] **Step 1:** `PotentialCustomerCareReportController::customerMeetings(Request)`.
- [x] **Step 2:** `GET assign/report/potential-customer-care/customer-meetings`, KHÔNG gắn
  `checkPermission` — giống 6 route còn lại của màn, gate nằm trong service để giữ fallback.

### Task 13.3 — FE: popup lịch sử

- [x] **Step 1:** `components/CustomerMeetingHistoryModal.vue` mới. Header có dòng nhận diện
  `Khách hàng: <mã> - <tên>` chữ **xám `#6b7280`** (chốt 2026-08-15: đỏ chỉ dành cho lỗi validate).
- [x] **Step 2:** Tên meeting là thẻ `<a target="_blank" rel="noopener">` **thật** trỏ
  `/assign/meeting/{id}/show` — không `router.push`, để chuột giữa / Ctrl+click cũng đúng.
- [x] **Step 3:** Phân trang `V2BasePagination` (khuôn Task 10.2).
- [x] **Step 4:** Trạng thái rỗng dùng xám `#6b7280` — `.text-muted` trong hrm-client là **màu ĐỎ**.

### Task 13.4 — FE: nút ở cột Khách hàng + nối vào màn

- [x] **Step 1:** `DemandListModal.vue` cột `customer`: thêm `V2BaseIconButton size="xs"` icon
  `ri-history-line` (component đã import sẵn ở file này), emit `open-customer-history`.
- [x] **Step 2:** `index.vue` hứng event, mở modal mới, đặt cùng cấp `MeetingDetailDrawer`.

### Task 13.5 — Kiểm chứng Playwright + E2E

- [x] **Step 1:** ⚠️ Đo `z-index` **2 modal chồng nhau** — Phase 11 đã vỡ đúng chỗ này (panel 1041
  nằm dưới `.modal` 1050). Đóng popup lịch sử thì popup drill-down phải còn nguyên trang + bộ lọc.
- [x] **Step 2:** Đo từ DOM: thứ tự `start_date` **tăng dần**, `href` + `target="_blank"` đúng id.
- [x] **Step 3:** E2E API: ca fail-closed (user không quyền chỉ thấy meeting mình chủ trì/dự) +
  ca thứ tự cũ → mới.
- [x] **Step 4:** E2E UI: mở popup từ icon, đếm dòng, kiểm link.
- [x] **Step 5:** Chạy lại **TOÀN BỘ** spec của màn (đang 36/36 xanh). Bộ test chạy `serial` —
  phải đọc dòng tổng kết, "did not run" KHÔNG phải "passed".

### Task 13.6 — Cột meeting: bỏ mã, thêm icon xem biên bản (2026-09-01)

**Yêu cầu user:** cột "Mã + Tên meeting" chỉ còn **tên meeting**; chỗ đang hiện mã đổi thành
**icon xem biên bản**, bấm mở popup xem biên bản.

- [x] **Step 1 (BE):** `customerMeetings()` thêm `withCount('reports')`; Resource trả `has_report`.
- [x] **Step 2 (FE):** đổi tiêu đề cột thành "Tên meeting", bỏ dòng mã.
- [x] **Step 3 (FE):** thay dòng mã bằng icon `ri-file-text-line`, emit `view-report` kèm id.
      **ẨN HẲN icon khi `has_report = false`** — `/print` trả 400 nếu meeting chưa lập biên bản
      (cùng điều kiện `reports.length > 0` của `MeetingDetailDrawer`), và quy tắc dự án là nút
      không dùng được thì ẩn chứ không hiện xám.
- [x] **Step 4 (FE):** `index.vue` nối `@view-report` vào `openMeetingReport()` có sẵn — dùng lại
      đúng popup xem trước bản in mà panel chi tiết meeting đang dùng, không tạo popup mới.
- [x] **Step 5:** ⚠️ **z-index tầng 3.** `.report-print-modal` KHÔNG khai z-index (mặc định 1050)
      nên popup biên bản sẽ nằm DƯỚI popup lịch sử (1062) → mở ra như không có gì xảy ra. Phải
      nâng lên trên, đo lại bằng Playwright đúng cách đã làm ở Task 13.5.
- [x] **Step 6:** Cập nhật ca e2e 20 (cột đổi) + bổ sung khẳng định cho icon biên bản, chạy lại
      TOÀN BỘ spec của màn.

**Kết quả:** cột 2 nay là "Tên meeting"; dòng mã cũ thay bằng icon `ri-file-list-2-line`
(`title="Xem biên bản"`) — icon + chữ copy nguyên khuôn cột Biên bản của `pages/assign/meeting/index.vue:1171`,
không tự chế icon mới cho cùng hành động. Nối vào `openMeetingReport()` sẵn có nên dùng CHUNG popup
xem trước bản in với panel chi tiết meeting.

**Z-INDEX 3 TẦNG** — đo thật: `1050` popup nhu cầu < `1062` popup lịch sử < `1064` popup biên bản.
`.report-print-modal` không khai z-index (mặc định 1050) nên nếu không nâng thì popup biên bản mở
THẬT mà bị che hoàn toàn — nhìn y hệt nút chết. Rule đặt trong `CustomerMeetingHistoryModal.vue`
chứ KHÔNG sửa `components/print/ReportPrintPreviewModal.vue` (file dùng chung, trên `gop_db` còn
nhiều màn khác gọi tới) — xung đột do popup lịch sử tạo ra thì nó tự gánh.

**Sửa kèm chữ sai của Task 13.4**: `title="Xem lịch sử meeting với khách hàng"` → `"Lịch sử meeting
với khách hàng"`. Bảng chữ chuẩn của skill `button-convention` cấm biến thể "Xem lịch sử"; giữ hậu
tố "meeting với khách hàng" để không lẫn với hành động **Lịch sử** (nhật ký thay đổi).

### Task 13.7 — Sửa ca e2e 15 hỏng do sang tháng (KHÔNG phải lỗi Phase 13)

Chạy full suite sau Task 13.6 thì ca **15** đỏ và **6 ca sau in "did not run"** (bộ test chạy
`serial`) — trong đó có cả 2 ca mới 20 & 21, nghĩa là chúng KHÔNG được kiểm trong lượt chạy đầy đủ.

- [x] **Step 1 (chứng minh không phải do mình):** `git stash` sạch cả 2 repo rồi chạy lại ca 15 →
      **vẫn đỏ y hệt**. Lỗi có sẵn, lộ ra do hôm nay sang 01/09 nên kỳ báo cáo đổi sang tháng 9.
- [x] **Step 2 (nguyên nhân gốc):** đo qua API — kỳ tháng 9 có **70 dòng, 0 dòng gắn dự án**; 2 dòng
      trạng thái "Đã lập dự án TKT" chính là fixture nhưng `prospective_project_id = null`.
      Fixture **tự mâu thuẫn**: trạng thái bảo đã lập dự án mà không có dự án nào. Ca 15 đòi "phải
      có nhu cầu đã gắn dự án" nên trước giờ chỉ **PASS NHỜ ĂN MAY** vào dữ liệu demo
      (`assign:seed-care-demo`) tình cờ còn dự án rơi vào kỳ tháng 8.
- [x] **Step 3:** `careDemand()` nhận thêm tham số `?int $projectId`; `carried_won` gắn dự án TKT
      đầu tiên trong DB. `arisen_won` CỐ Ý để trống để ca 15 vẫn đối chiếu được 2 nhánh.
- [x] **Step 4:** chạy lại full suite → **44/44 xanh**, không còn dòng "did not run".

> Bài học: ca test dựa vào dữ liệu demo/thật thay vì fixture của chính nó là **bom hẹn giờ theo
> lịch** — xanh nhiều tháng rồi đỏ đúng ngày sang kỳ mới. Fixture phải tự cung cấp đủ dữ liệu cho
> điều kiện mà nó khẳng định.

### Kết quả Phase 13

**BE** (`hrm-api`): `PotentialCustomerCareService::customerMeetings()` + `resolvePerPage()` +
`attachHostNames()` · `CustomerMeetingRowResource` (mới) · `PotentialCustomerCareReportController::customerMeetings()` ·
1 route. **KHÔNG migration, KHÔNG quyền mới** — dùng lại 3 quyền 1179/1180/1181 sẵn có.

**FE** (`hrm-client`): `components/CustomerMeetingHistoryModal.vue` (mới) · `DemandListModal.vue`
(icon + emit + style) · `index.vue` (import/components/data/template/method).

**E2E: 44/44 xanh** (trước Phase 13 là 36) — thêm 3 ca API (11 thứ tự + cột · 12 phân trang + trần
`per_page` + guard `customer_id` rỗng · 13 fail-closed) và 2 ca UI (20 popup lịch sử · 21 icon xem
biên bản + z-index 3 tầng).

### 2 lỗi tự bắt được khi làm — đáng nhớ

1. ⚠️ **`->select([...])` gọi SAU `->withCount()` xoá luôn subquery đếm.** `select()` THAY THẾ cả
   select list chứ không cộng thêm, nên `investment_demands_count` biến mất và cột Nhu cầu ra
   **"Không" ở 100% dòng mà không có lỗi nào báo ra** — chỉ lộ khi smoke test endpoint bằng dữ
   liệu thật. Đặt `select()` TRƯỚC `withCount()` (hoặc dùng `addSelect`).
2. ⚠️ **BE hardcode `paginate(self::DEFAULT_PER_PAGE)` khiến ô "Số dòng/trang" của FE thành nút
   chết.** FE gửi `per_page` nhưng BE bỏ qua; đổi 20 → 50 → 100 không có gì thay đổi và cũng
   không có lỗi. Đã thêm `resolvePerPage()` có trần.

### Bẫy khi VIẾT E2E cho popup nạp bằng AJAX (dính 2 lần liên tiếp)

`await expect(modal).toBeVisible()` đúng NGAY LÚC khung modal vừa mở — lúc đó `tbody` còn rỗng.
Đếm dòng ở thời điểm đó ra **0**, rồi mọi khẳng định sau đều so với 0 (lần 2 còn tệ hơn: nhánh
"danh sách rỗng" chạy nhầm trong khi popup thật ra có dữ liệu). Phải **chờ nội dung** trước khi
đếm: `toHaveCount(<số đã biết>)` cho bảng nhu cầu, và
`expect(locator('.care-hist-state', { hasText: 'Đang tải' })).toHaveCount(0)` cho popup lịch sử.

### Ghi chú kỹ thuật

- **z-index**: bootstrap-vue **KHÔNG** tự nâng z-index cho modal mở sau — đo được cả 2 popup đều
  `1050`, popup lịch sử chỉ tình cờ nằm trên nhờ đứng SAU trong DOM. Đã ghim `.care-hist-modal`
  ra **1062** (trên `above-modal` 1060 của panel chi tiết meeting ở Phase 11) và có ca e2e khẳng
  định `hist_z > drill_z` + `elementFromPoint` giữa popup thuộc về popup lịch sử.
- **Icon KHÔNG làm mờ chờ hover**: bản đầu để `opacity .35` rồi sáng lên khi rê chuột — tự bỏ, vì
  đây là lối vào DUY NHẤT của tính năng và thiết bị cảm ứng không có hover.
- Link meeting là **thẻ `a` thật** (`href` + `target="_blank"` + `rel="noopener"`), KHÔNG
  `router.push` — để chuột giữa / Ctrl+click cho cùng kết quả với bấm thường.

---

## Phase 14 — Tiêu chí theo dõi "Khách hàng" (2026-09-06)

Spec đầy đủ: `docs/superpowers/specs/2026-09-06-cskh-tieu-chi-khach-hang-design.md`
Nhánh: `tpe-cskh-tieu-chi-khach-hang` (tách từ `tpe`, CẢ 2 repo). KHÔNG migration / quyền / cron mới.

Yêu cầu user: bộ lọc select search chọn khách hàng + bảng theo dõi có phần
**Khách hàng ▸ Phòng ban ▸ Bộ phận (nếu có) ▸ Nhân viên**.

### Task 14.0 — Tạo nhánh
- [x] `git checkout -b tpe-cskh-tieu-chi-khach-hang` ở `hrm-api` và `hrm-client` (KHÔNG `git stash` — repo dùng chung với session khác)

### Task 14.1 — BE: nguồn phòng ban / bộ phận theo NGƯỜI CHỦ TRÌ
- [x] `attachOrganisation()` gắn thêm `host_department_id/name` (từ `employee_infos.department_id`) và `host_part_id/name` (`employee_infos.part_id` → tên batch từ bảng `parts`)
- [x] Giữ luật đang có: id còn nhưng không resolve được tên → **xoá luôn id** (tránh 2 dòng "Chưa xác định" cạnh nhau)
- [x] KHÔNG đụng `department_id` / `department_name` của meeting (phần III phải giữ nguyên số)
- [x] `Employee::with('info')` đã load sẵn → chỉ thêm 2 query batch, không N+1

### Task 14.2 — BE: đệ quy hoá `buildSection()`
- [x] Đổi sang nhận **mảng level** `['prefix' => …, 'of' => fn($d) => [id, name], 'skipWhenAllEmpty' => bool]`
- [x] `buildLevel()` đệ quy: gom nhóm → `buildRow()` (không đổi) → `children`, `shareBase` = tổng tiền nhóm cha, sắp theo `amount` giảm dần ở mọi cấp
- [x] `skipWhenAllEmpty`: cả nhánh rỗng ở level đó → bỏ qua level, đệ quy thẳng xuống level sau
- [x] Chuyển 3 phần I/II/III sang khung mới với mảng 2 level — **output phải y hệt hiện nay, kể cả `drill_key`**
- [x] Trả thêm `sections[].key` (`field|market|dept|customer`) để FE thôi nhận dạng phần bằng chuỗi tiếng Việt trong `title`

### Task 14.3 — BE: phần IV + tiêu chí mới
- [x] `buildSections()` dựng phần `customer` khi `criteria ∈ ['all','customer']`, levels: `customer ▸ hdept ▸ hpart (skip) ▸ emp`
- [x] `getDemands()`: lọc `meetings.customer_id` khi `filled('customer_id')`

### Task 14.4 — BE: `drill_key` tổ hợp
- [x] `resolveDrillBase()` tách theo `+`, lọc **AND** từng phần tử; key 1 phần tử chạy như cũ (tương thích ngược)
- [x] Map cột: `customer→customer_id`, `hdept→host_department_id`, `hpart→host_part_id`, `emp→host_employee_id` (dùng lại)

### Task 14.5 — BE: danh mục lọc + mô tả bộ lọc
- [x] `filterOptions()` trả thêm `customers` (`text` = `mã - tên`), `host_departments`, `parts` (`parent_id` = host_department) — vẫn chỉ mục CÓ dữ liệu trong kỳ
- [x] `describeFilters()` thêm nhãn Khách hàng + tiêu chí "Khách hàng"; `describeDrillFilters()` thêm 3 ô mới

### Task 14.6 — BE: khối "Phân bổ theo cơ cấu"
- [x] Giữ 3 chiều cũ; drill theo `hdept`/`hpart` thì **ẩn chiều "Phòng ban"** (chiều đó đọc `department_id` của meeting, khác nguồn → 2 con số vênh nhau)

### Task 14.7 — BE: Resource
- [x] `CustomerDemandRowResource` trả thêm `host_department_id/name`, `host_part_id/name`

### Task 14.8 — BE: Excel + bản in
- [x] Làm phẳng cây ở PHP thành `{ level, stt: '1.2.1', … }`, blade lặp 1 vòng (KHÔNG `@include` đệ quy)
- [x] Sửa `prints/assign/potential_customer_care_{summary,detail}.blade.php` + `exports/assign/potential_customer_care_report.blade.php`
- [x] `exports/assign/potential_customer_care_demands.blade.php` + `columnWidths()`: thêm cột **Bộ phận** (16 → 17 cột)

### Task 14.9 — FE: bộ lọc
- [x] `criteriaOptions` thêm `{ id: 'customer', name: 'Khách hàng' }`
- [x] Ô lọc riêng: `V2BaseSelectRemote` gọi `assign/prospective-projects/search-customers?q=`, `minimumInputLength: 2`, `initialOption` giữ nhãn KH đã chọn
- [x] Lưới đủ 12 cột: Kỳ (3) + Tiêu chí (3) + Khách hàng (**6**)
- [x] `onCriteriaChange()` xoá `customer_id` khi đổi sang tiêu chí khác (kể cả `all`)
- [x] Tên KH giữ ở biến riêng NGOÀI `filters` (`buildParams()` gửi nguyên `filters` lên mọi endpoint)

### Task 14.10 — FE: bảng theo dõi đệ quy
- [x] Tách `components/CareTrackingRow.vue` tự gọi chính nó theo `children`
- [x] `expanded` đổi khoá sang **đường dẫn** `${sIndex}-${path}`; STT `1` → `1.2` → `1.2.1` → `1.2.1.3`; thụt lề 34/54/74px
- [x] `tones` đọc `section.key`; phần `customer` thêm tông màu thứ 4 (xanh dương cùng hệ)
- [x] `allExpanded` / nút "Hiện chi tiết" đếm dòng-có-con ở **mọi cấp**
- [x] `sectionTips` thêm nội dung phần IV, ghi rõ "phòng ban / bộ phận theo hồ sơ người chủ trì"

### Task 14.11 — FE: popup chi tiết
- [x] `DIMENSION_COLUMNS.customer` = Phòng ban chủ trì · Bộ phận · Kinh doanh chủ trì
- [x] `drillType` suy từ **phần tử ĐẦU** của `drill_key` (để `emp:` không lẫn cơ cấu giữa phần III và IV)
- [x] Bộ ô lọc: mở từ phần IV → Khách hàng · Phòng ban chủ trì · Bộ phận · Nhân viên chủ trì · Trạng thái; mở từ I/II/III → giữ 6 ô cũ; vẫn ẩn ô của cấp đang xem + các cấp cha, ô ẩn KHÔNG tham gia lọc

### Task 14.12 — Fixture (làm TRƯỚC khi viết test)
- [x] `hrm-api/database/e2e_care_report_seed.php`: ≥2 khách hàng; chủ trì **có** `part_id` và chủ trì **không có**, thuộc ≥2 phòng ban → cover cả nhánh 4 cấp lẫn nhánh 3 cấp

### Task 14.13 — E2E API
- [x] `criteria=customer` trả section `key=customer`, cây đúng thứ tự 4 cấp
- [x] Nhánh phòng ban không ai có bộ phận → **bỏ cấp**
- [x] `drill_key` tổ hợp lọc AND đúng
- [x] `customer_id` thu hẹp đúng tập
- [x] `filter-options` trả `customers` / `host_departments` / `parts` (có `parent_id`)
- [x] **Hồi quy**: `criteria=all` giữ nguyên số + `drill_key` của 3 phần cũ
- [x] Fail-closed: không quyền vẫn chỉ thấy nhu cầu từ meeting của mình ở phần IV

### Task 14.14 — E2E UI
- [x] Chọn tiêu chí Khách hàng → ô select search hiện, chọn được KH, bảng lọc đúng
- [x] Bảng ra đủ cấp; bung/thu từng cấp; "Hiện chi tiết" bung hết mọi cấp
- [x] Bấm số ở cấp sâu → popup đúng tập, có cột Bộ phận, đúng bộ ô lọc

### Task 14.15 — Kiểm chứng + chạy lại toàn bộ
- [x] Playwright thủ công **đo bằng DOM**: STT theo cấp, thụt lề từng cấp, số cột popup, không chồng lấn footer
- [x] Chạy lại **toàn bộ 4 spec** của màn; bộ test `serial` → phải đọc dòng tổng kết, không nhìn "không thấy chữ failed"

### Task 14.16 — Sửa 2 ca đỏ có trước Phase 14 (user yêu cầu)

- [x] `meeting-host.api` "Báo cáo meeting theo thị trường đọc theo chủ trì": nguyên nhân KHÔNG phải "ngoài kỳ" (chẩn đoán đầu của tôi sai — `?period=` là "Tất cả", không lọc kỳ) mà là **meeting fixture `customer_id = NULL`**, còn báo cáo có `whereNotNull('customer_id')` vì nhóm theo tỉnh của KHÁCH HÀNG. Ca nay tự gán 1 khách hàng khi meeting chưa có và `afterAll` trả lại đúng giá trị cũ (kể cả cũ là rỗng).
- [x] `customer-demand-link` ca 1: ô "Nhu cầu khách hàng" luôn ở CUỐI khối, nhãn trước nó phụ thuộc LOẠI KH — doanh nghiệp thì "Người liên hệ", **cá nhân thì "Email khách hàng"** (khối Người liên hệ `v-if="!isIndividual"` ẩn hẳn). KH của dự án fixture `E2E-ASSIGN-PRJ` là cá nhân (`customers.id = 8`, `customer_type = 1`). Ca nay đối chiếu theo đúng loại KH đang mở, không đổi component.
- [x] Chạy chốt **79/79 xanh** trên cả 6 spec của feature (2 spec CSKH API + UI, export, meeting-host API + UI, customer-demand-link API + UI)

Ảnh: `.plans/bao-cao-cskh-tiem-nang/screenshots/2026-09-06-bang-4-cap-theo-khach-hang.png`

### Task 14.17 — Khối tổng hợp mặc định THU GỌN (user chốt 2026-09-06)

- [x] Màn báo cáo: `CareSummaryBlocks.collapsed` mặc định `true` — chỉ còn dòng meta (kỳ · số nhu cầu · tổng giá trị), bảng theo dõi lên ngay đầu màn (đo được: khối tổng hợp 48px, bảng ở `top = 209px`)
- [x] Popup chi tiết: `summaryCollapsed` mặc định `true` + `resetLocal()` trả về `true` khi mở popup mới (bảng chi tiết ở `top = 208px` thay vì 370px)
- [x] Cập nhật e2e: 2 helper `expandSummary(page)` / `expandDrillSummary(modal)`; 8 chỗ bấm số trong khối tổng hợp và 4 chỗ dùng chip/KPI của popup phải mở khối trước; ca 1 nay khẳng định mặc định thu gọn; ca 6 đảo chiều (mặc định "Mở rộng"); ca 17 mở khối ở lượt 1 để phép so "chip lượt trước phải biến mất" còn ý nghĩa
- [x] **79/79 xanh** trên cả 6 spec

⚠️ Bẫy khi viết helper: nút "Mở rộng" của popup chỉ render khi số liệu đã về (`v-if="hasSummary"`), đọc `count()` ngay lúc vừa mở là 0 nên helper lặng lẽ không bấm gì và khối vẫn thu gọn → phải `waitFor({ state: 'visible' })`; ca cố ý đo lúc API còn bị giữ thì truyền timeout ngắn.

Ảnh: `.plans/bao-cao-cskh-tiem-nang/screenshots/2026-09-06-summary-mac-dinh-thu-gon.png`

### Task 14.18 — Cột ngày meeting sắp xếp được ở MỌI popup (user chốt 2026-09-06)

- [x] **Popup chi tiết nhu cầu** — cột "Meeting thu thập nhu cầu" sortable, sắp theo **NGÀY HỌP** (`meeting_start_date`) chứ không theo tên meeting. `sortedRows` thêm nhánh `sortType: 'date'` + helper `dateSortKey()` đổi `dd/MM/yyyy HH:mm` thành số so sánh được.
- [x] **Popup lịch sử meeting** — cột "Thời gian họp" sortable, **sắp Ở BACKEND**: popup phân trang server-side nên đảo tại chỗ chỉ đúng trong 20 dòng đang xem. BE `customerMeetings()` nhận `sort_dir` (`asc` mặc định, giá trị lạ rơi về `asc`), order theo `start_date` + khoá phụ `id` cùng chiều. FE gửi `sort_dir`, về trang 1 khi đảo chiều, mở lại popup thì về mặc định cũ→mới.
- [x] E2E: ca 14 nay đòi **6 cột** sortable + kiểm sort theo MỐC THỜI GIAN; ca UI 26 mới (bắt request để chứng minh `sort_dir` đi qua BE); ca API 21 mới (desc đảo cả tập TRƯỚC khi phân trang: `per_page=1&sort_dir=desc` phải trả meeting mới nhất của cả tập).
- [x] **81/81 xanh** trên cả 6 spec

⚠️ **KHÔNG so ngày bằng chuỗi**: `"05/08/2026" > "30/07/2026"` theo thứ tự chữ nhưng lại là ngày TRƯỚC — bảng sắp sai mà nhìn vẫn "có thứ tự", và ca test so chuỗi cũng xanh theo. Cả code lẫn e2e đều quy về mốc `yyyyMMddHHmm`.
⚠️ 2 ca cũ (15, 16) đỏ vì đọc bảng lúc còn dòng "Đang tải…" (1 ô `colspan` → `td[i]` undefined, `page.evaluate` nổ). Thêm helper `waitDrillRows(modal)` và bỏ dòng trạng thái trước khi đọc — đổi thứ tự click (mở khối tổng hợp trước) làm lệch nhịp cũ.

### Task 14.19 — Nén dải tổng hợp + tiêu đề cột hoa chữ đầu (user chốt 2026-09-06)

**Đo trước/sau ở viewport 874px:**

| | Trước | Sau |
|---|---|---|
| Dải tổng hợp khi mở rộng | 296px (**34%** màn) | **186px (21%)** |
| Bảng theo dõi bắt đầu ở | `top = 457px` | **`top = 343px`** |
| Khối 2 chỉ tiêu | 110px | 61px |
| Khối 3 hộp KPI | 109px (21px là dòng tiêu đề) | 63px |

- [x] Bỏ dòng tiêu đề "Kết quả KPI" (`:show-title="false"`) — chiếm hẳn 1 hàng trong khi 3 hộp đã tự nói rõ; nội dung tooltip tổng đã nằm trong tooltip công thức + ghi chú của từng hộp
- [x] 2 ô chỉ tiêu con của mỗi khối dồn về **1 dòng chữ** (bỏ viền/nền ô, thêm dấu `:` sau nhãn bằng CSS) — **giữ nguyên tên class** `__items`/`__item`/`__label`/`__value` vì e2e đang bám vào chúng
- [x] Nén padding/font: `.type-summary-bar` 10/13/12 → 7/12/8 · `.rsum-blk` 9/13/10 → 6/11/7 · số tổng 22 → 18px · giá trị ô con 17 → 13,5px · `.rsum-kpi` 9/13/10 → 6/11/7 · giá trị KPI 24 → 18px · thanh KPI 5 → 4px
- [x] **Tiêu đề cột bảng: viết hoa CHỮ ĐẦU** (`text-transform: none`, `letter-spacing: 0`, `font-weight` 800 → 700) ở cả bảng theo dõi và bảng popup; khai rõ `white-space: nowrap` cho `th` để tiêu đề không bao giờ xuống dòng (đo lại: header 1 dòng — 37px ở màn, 34px ở popup)
- [x] Đổi luôn **dòng tiêu đề phần** (`.rsum-tb__sec`) sang hoa chữ đầu cho nhất quán — nó vẫn nổi nhờ nền + màu + in đậm. Nhãn khối tổng hợp cũng bỏ uppercase.
- [x] **84/84 xanh** (29 UI + 55 của 4 spec còn lại)

Ảnh: `.plans/bao-cao-cskh-tiem-nang/screenshots/2026-09-06-summary-nen-gon.png`
⚠️ Bản in + Excel KHÔNG đổi: chúng viết hoa bằng `mb_strtoupper()` trong blade, độc lập với CSS màn hình.

### Kết quả Phase 14

**20 task (14.0 – 14.19) xong. 84/84 e2e xanh** trên cả 6 spec của feature:
`potential-customer-care` API 21 + export API 8 + UI 29, `meeting-host` API 6 + UI, `customer-demand-link` API + UI.
Lệnh chạy: `cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test potential-customer-care.api.spec.ts potential-customer-care-export.api.spec.ts potential-customer-care.spec.ts meeting-host customer-demand-link`

Yêu cầu bổ sung sau nghiệm thu (14.16 – 14.19): sửa 2 ca đỏ có sẵn · khối tổng hợp mặc định thu gọn ·
cột ngày meeting sắp xếp được ở mọi popup · nén dải tổng hợp 296px → 186px + tiêu đề cột hoa chữ đầu.

Thay đổi ngoài dự kiến (chi tiết ở spec mục 9–12):
- FE **KHÔNG** tách `CareTrackingRow.vue` đệ quy — Vue 2 không cho nhiều thẻ gốc mà mỗi cấp là 1 `<tr>`, nên làm phẳng cây trong computed `renderSections` (cùng cách BE làm cho bản in).
- `drill_key` của dòng CON đổi shape: `sector:2` → `field:1+sector:2`. Kết quả trả về KHÔNG đổi (đã đo 11 key cũ + 16 key mới, mỗi key trả đúng con số hiện trên bảng).
- Excel danh sách 16 → **18 cột** (thêm cả "Phòng ban chủ trì" cạnh "Bộ phận"); bản in danh sách thêm 1 cột.
- `filterOptions` trả thêm `host_employees` (ô Nhân viên chủ trì trong popup phải cascade theo phòng ban của HỒ SƠ chủ trì).

**3 lỗi tự bắt được khi kiểm bằng Playwright / chạy test:**
1. Popup mở từ phần IV hiện cột **"Kinh doanh chủ trì" 2 LẦN** (nhóm cột `dept` và `customer` dùng chung cột đó) — Vue chỉ cảnh báo "Duplicate keys detected: 'host'" ở console, màn vẫn chạy. Đã khử trùng theo `key`.
2. `V2BaseSelectRemote` phát `@change` **chỉ có giá trị, không có nhãn** → phải dùng `@select` để giữ tên KH, nếu không lần vẽ lại ô hiện trống dù vẫn đang lọc.
3. Luật ẩn ô lọc trong popup phải đọc **mọi tiền tố** trong `drill_key`, không chỉ tiền tố đầu — nếu không, mở popup ở cấp sâu vẫn hiện ô lọc của cấp đã bị khoá cứng.

**4 việc phải làm ở FIXTURE mới chạy được test:**
1. Tách người chủ trì khỏi người tạo làm báo cáo trả **RỖNG** (user E2E không có quyền cấp công ty, trước giờ thấy dữ liệu nhờ nhánh fallback "meeting của chính mình") → fixture phải seed `meeting_employees`.
2. Quyền 1179–1181 **chưa gán cho role nào** trên DB local → khối lọc tổ chức không render, ca cũ số 9 đỏ. Fixture nay tự gán (`role_has_permissions` cần `company_id = 1`).
3. `e2e_provision.php` không ghi `employee_infos.email` (cột có UNIQUE) → `Duplicate entry ''`, **cả bộ test không chạy**. Đã sửa provision.
4. Fixture tự cấp > 20 nhu cầu (2 meeting × 13 nhóm ngành) cho ca phân trang, và xuất mã + tên KH (ERP có 4 khách trùng tên "TRẦN QUANG TRUNG").

**Ca cũ phải sửa theo:** API ca 5, UI ca 1/5 (3 → 4 phần) · UI ca 15 (lọc theo trạng thái thay vì đọc trang 1) · UI ca 21 + 25 (bỏ so chữ hoa cứng — tiêu đề viết hoa bằng CSS) · Export ca 4 (letterhead chấp nhận path tương đối, máy dev không có `ERP_URL`).

### Checkpoint — 2026-09-07 (ĐÃ COMMIT — Phase 14)

**ĐÃ COMMIT (user tự commit 2026-09-07):**
- `hrm-api` `7bddb9fb1` — 11 file, +536/−149
- `hrm-client` `f29eaaf35` "update kq cskh" — 6 file, +421/−164

Cả 2 nhánh `tpe-cskh-tieu-chi-khach-hang`, cây làm việc **sạch**, mỗi repo đúng **1 commit** so với `tpe`.
⚠️ **CHƯA PUSH và CHƯA MERGE về `tpe`** — nhánh chưa có upstream ở cả 2 repo.
⚠️ `HRM/e2e/` không thuộc repo nào → 4 file spec (`potential-customer-care{,-export}.api.spec.ts`,
`potential-customer-care.spec.ts`, `meeting-host.api.spec.ts`, `customer-demand-link.spec.ts`) chỉ
có trên máy này. Fixture `e2e_care_report_seed.php` + `e2e_provision.php` thì ĐÃ nằm trong commit
của `hrm-api`.

Vừa hoàn thành: **20/20 task Phase 14** — tiêu chí "Khách hàng" (BE đệ quy hoá `buildSection`, phần IV 4 cấp theo hồ sơ chủ trì, `drill_key` tổ hợp, Excel + bản in làm phẳng cây; FE select search KH, bảng nhiều cấp, popup thêm cột Bộ phận + bộ ô lọc riêng) + 4 yêu cầu sau nghiệm thu (sửa 2 ca đỏ có sẵn · khối tổng hợp mặc định thu gọn · cột ngày meeting sort được ở mọi popup · nén dải tổng hợp + tiêu đề cột hoa chữ đầu). **84/84 e2e xanh**, đã kiểm chứng bằng Playwright và đo bằng DOM ở từng bước.
Đang làm dở: (không)
Bước tiếp theo: push nhánh + merge về `tpe` ở CẢ 2 repo. Deploy chỉ cần code: KHÔNG migration, KHÔNG quyền mới, KHÔNG cron.
Blocked: (không)

File trong commit — `hrm-api` (11): `PotentialCustomerCareService`, `PotentialCustomerCarePrintService`, `PotentialCustomerCareExport`, `PotentialCustomerCareDemandExport`, `CustomerDemandRowResource`, 2 blade `prints/assign/potential_customer_care_*`, 2 blade `exports/assign/potential_customer_care_*`, `database/e2e_care_report_seed.php`, `database/e2e_provision.php`.
`hrm-client` (6): `index.vue`, `CareTrackingTable.vue`, `DemandListModal.vue`, `CustomerMeetingHistoryModal.vue`, `CareSummaryBlocks.vue`, `KpiBoxes.vue`.

### Checkpoint — 2026-09-06 (Phase 14 — tiêu chí Khách hàng)

Vừa hoàn thành: toàn bộ 16 task Phase 14 (BE đệ quy hoá + phần IV + drill_key tổ hợp + Excel/bản in, FE bộ lọc select search + bảng 4 cấp + popup, fixture, 6 ca API + 4 ca UI mới). **55/55 e2e xanh.** Đã kiểm chứng bằng Playwright: đo STT/thụt lề từng cấp (34/54/74px), cột popup, lưới bộ lọc 12 cột.
Đang làm dở: (không)
Bước tiếp theo: user nghiệm thu trên máy (nhánh `tpe-cskh-tieu-chi-khach-hang` ở cả 2 repo, CHƯA commit). Sau khi duyệt: commit + merge về `tpe`.
Blocked: (không)

### Checkpoint — 2026-09-02 (ĐÃ MERGE + PUSH — kết thúc Phase 13)

Vừa hoàn thành: user merge cả 2 nhánh về `tpe` và push. **Phase 13 khép lại.**

| Repo | `tpe` sau merge | Đồng bộ origin |
|---|---|---|
| `hrm-api` | `93634433f` | 0/0 |
| `hrm-client` | `2fa39cb29` | 0/0 |

**Đã chạy lại TOÀN BỘ bộ test trên cây `tpe` sau merge: 44/44 xanh** (23 API + 21 UI), không có
ca nào "did not run". Route `customer-meetings` xác nhận có mặt trên `tpe`.

**Xử lý conflict lúc merge FE** — đúng 1 file, `components/V2BaseFloatingField.vue` (add/add), và
KHÔNG phải file của Phase 13: nó là component của session khác bị `git stash` của tôi cuốn vào
commit `f2b65b4b6` hôm 01/09. Đã lấy **nguyên bản `tpe`** (406 dòng) thay vì bản trên nhánh
(354 dòng), vì bản `tpe` mới hơn và chứa 5 sửa lỗi mà bản kia chưa có:

| `tpe` giữ | nhánh bỏ |
|---|---|
| `tags`: nhãn nghỉ giữa ô cho đồng bộ các select khác | nhãn float vĩnh viễn (quyết định cũ) |
| `--ff-accent: #1976d2` kèm ghi chú `custom-theme.scss:120` đè mất `#16a34a` | `#0a99a7` |
| `z-index: 0` mở stacking context — chặn Select2 (`z-index: 9999`) vẽ đè lên nhãn | thiếu |
| Rule sàn `36px` chống nháy 100ms khi select2 dựng lại | thiếu |
| `font-weight: 400` cho nhãn chưa float | thiếu |

Đã đối chiếu từng dòng: bản trên nhánh không có gì riêng mà `tpe` thiếu. Nhờ resolve như vậy,
merge FE cuối cùng **chỉ mang đúng 3 file Phase 13** (+415/-1), không đẩy việc dở của ai lên `tpe`.
Merge API không conflict (đã dò trước: 5 file nhánh sửa thì `tpe` không đụng file nào từ merge-base
`27432a213`).

Đang làm dở: không có.
Bước tiếp theo: (tuỳ chọn) cập nhật SRS + testcase — vẫn ở bản 26/08, chưa có Phase 7→13.
Blocked: không có.

> ⚠️ **Nợ kỹ thuật còn lại**: `HRM/e2e/` không nằm trong repo nào nên 5 ca test của Phase 13
> (API 11–13, UI 20–21) + bản sửa ca 15 CHỈ có trên máy này, không theo code lên git.

---

### Checkpoint — 2026-09-01 (ĐÃ COMMIT)

Vừa hoàn thành: user tự commit cả 2 repo. **Phase 13 khép lại về mặt code.**

| Repo | Nhánh | Commit | Nội dung |
|---|---|---|---|
| `hrm-api` | `bao_cao_cskh_lich_su_meeting` | `49d1c9a33` | 5 file, +200/-3 — service · resource · controller · route · fixture e2e |
| `hrm-client` | `bao_cao_cskh_lich_su_meeting` | `f2b65b4b6` | 9 file, +953/-118 |

Cả 2 repo working tree sạch với phần việc của Phase 13. **CHƯA push, CHƯA merge về `tpe`.**
`hrm-client` hiện đã checkout ngược về `tpe` nên file của feature không còn trên đĩa — bình thường.

⚠️ **CẦN BIẾT TRƯỚC KHI MERGE — commit FE gói lẫn việc của session khác.** Hậu quả kéo dài của sự
cố `git stash` ghi ở checkpoint trước: lúc commit, working tree `hrm-client` còn 6 file đang dở của
session khác nên chúng bị cuốn vào `f2b65b4b6` cùng 3 file của Phase 13:

- **Của Phase 13 (3 file)**: `pages/assign/report/potential-customer-care/components/CustomerMeetingHistoryModal.vue` (mới, +371) ·
  `.../components/DemandListModal.vue` (+23) · `.../potential-customer-care/index.vue` (+22)
- **KHÔNG phải của Phase 13 (6 file)**: `components/V2BaseFloatingField.vue` (mới, +354) ·
  `components/V2BaseCompanyDepartmentFilter.vue` · `components/V2BaseFilterPanel.vue` ·
  `components/V2BaseSelect.vue` · `components/V2BaseSelectInModal.vue` ·
  `pages/assign/prospective-projects/index.vue` (+255/-…)

6 file đó là việc **đang làm dở** của session khác (panel bộ lọc + floating label). Merge nguyên
`f2b65b4b6` về `tpe` sẽ đẩy một bản chụp NỬA CHỪNG của họ lên nhánh chính. Trước khi merge nên
tách: `git checkout -b <nhánh sạch> tpe` rồi `git checkout f2b65b4b6 -- <3 file của Phase 13>`.
Bản thân 6 file đó cũng vẫn đang được sửa tiếp trên working tree `tpe` (nay còn thêm
`CheckboxMultiSelect.vue`, `CascadePairSelect.vue`) → sẽ đụng nhau khi merge.

`stash@{0}` của `hrm-client` vẫn giữ, chưa drop — nội dung nay đã nằm cả trong commit lẫn working
tree nên xoá được khi session kia xác nhận không cần nữa.

⚠️ **E2E KHÔNG ĐƯỢC VERSION**: `HRM/e2e/` không nằm trong repo nào (`ERP-HRM/` và `HRM/` đều không
phải git repo, `e2e/` không có `.git`). 5 ca test viết cho Phase 13 (API 11–13, UI 20–21) và bản
sửa ca 15 **chỉ tồn tại trên đĩa máy này** — không đi kèm commit, máy khác pull code về sẽ không có.

Đang làm dở: không có.
Bước tiếp theo: tách commit FE cho sạch → push → merge `tpe`. Tuỳ chọn: cập nhật SRS + testcase
(đang dừng ở bản 26/08, chưa có Phase 7→13).
Blocked: không có.

---

### Checkpoint — 2026-09-01 (Task 13.6 + 13.7 — cột Tên meeting, icon xem biên bản)

Vừa hoàn thành: **Task 13.6** (bỏ mã meeting, thêm icon Xem biên bản) và **Task 13.7** (sửa ca e2e
15 hỏng do sang tháng). **44/44 e2e xanh.** Vẫn nhánh `bao_cao_cskh_lich_su_meeting`, CHƯA commit.

File đụng thêm so với checkpoint 31/08:
- `hrm-api/.../PotentialCustomerCareService.php` — `withCount(['investment_demands', 'reports'])`
- `hrm-api/.../CustomerMeetingRowResource.php` — thêm `has_report`
- `hrm-api/database/e2e_care_report_seed.php` — thêm biên bản cho `E2E-CARE-PREV`; `careDemand()`
  nhận `?int $projectId`, `carried_won` gắn dự án TKT
- `hrm-client/.../CustomerMeetingHistoryModal.vue` — cột "Tên meeting", icon biên bản, z-index 1064
- `hrm-client/.../DemandListModal.vue` — sửa chữ tooltip theo `button-convention`
- `hrm-client/.../index.vue` — nối `@view-report`
- `e2e/tests/assign/potential-customer-care.api.spec.ts` — `has_report` trong ca 11
- `e2e/tests/assign/potential-customer-care.spec.ts` — ca 20 kiểm tiêu đề cột, **ca 21 mới**

⚠️ **SỰ CỐ GIT — đã xử lý, cần user biết:** lúc chứng minh ca 15 không phải lỗi mình, tôi chạy
`git stash push -u` ở `hrm-client` và **nuốt luôn công việc đang dở của một session khác** đang
sửa cùng repo (6 file: `V2BaseCompanyDepartmentFilter` · `V2BaseFilterPanel` · `V2BaseFloatingField`
· `V2BaseSelect` · `V2BaseSelectInModal` · `pages/assign/prospective-projects/index.vue`).
Đã khôi phục: 5 file lấy lại từ stash; riêng `V2BaseCompanyDepartmentFilter.vue` giữ **bản working
tree mới hơn** (297 dòng, session kia sửa tiếp sau lúc stash) chứ KHÔNG đè bằng bản 293 dòng trong
stash. **`stash@{0}` vẫn giữ nguyên, không drop** để đối chiếu/khôi phục. Bản sao hiện trạng lưu ở
scratchpad của session.
→ **Bài học: KHÔNG `git stash` ở repo dùng chung khi có thể có session khác đang làm.** Muốn so với
code sạch thì dùng `git worktree` riêng hoặc `git stash push -- <đúng file của mình>`.

Đang làm dở: không có.
Bước tiếp theo: user nghiệm thu; cân nhắc cập nhật SRS + testcase (đang dừng ở 26/08).
Blocked: không có.

---

### Checkpoint — 2026-08-31 (Phase 13 — lịch sử meeting với khách hàng)

Vừa hoàn thành: **Phase 13, 5 task**. Nhánh mới `bao_cao_cskh_lich_su_meeting` ở CẢ 2 repo
(tách từ `tpe`, cây sạch trước khi tách). **CHƯA commit, CHƯA push.**

File đụng tới — BE 4, FE 3, e2e 2:
- `hrm-api/Modules/Assign/Services/Report/PotentialCustomerCareService.php` (+3 method, +1 hằng số)
- `hrm-api/Modules/Assign/Transformers/PotentialCustomerCareResource/CustomerMeetingRowResource.php` (mới)
- `hrm-api/Modules/Assign/Http/Controllers/Api/V1/PotentialCustomerCareReportController.php`
- `hrm-api/Modules/Assign/Routes/api.php` (1 route)
- `hrm-client/pages/assign/report/potential-customer-care/components/CustomerMeetingHistoryModal.vue` (mới)
- `hrm-client/pages/assign/report/potential-customer-care/components/DemandListModal.vue`
- `hrm-client/pages/assign/report/potential-customer-care/index.vue`
- `e2e/tests/assign/potential-customer-care.api.spec.ts` (+3 ca)
- `e2e/tests/assign/potential-customer-care.spec.ts` (+1 ca)

Đang làm dở: không có.
Bước tiếp theo: user nghiệm thu trên trình duyệt → nếu đạt thì gộp về `tpe`; cân nhắc cập nhật
SRS + testcase (đang dừng ở bản 2026-08-26, chưa có Phase 7→13).
Blocked: không có.

> **Deploy**: Phase 13 KHÔNG có migration, KHÔNG có quyền mới, KHÔNG có cron — chỉ cần deploy code.

---

### Checkpoint — 2026-08-28 (Phase 8 — seeder demo dựng đúng cây lĩnh vực + thị trường)

Vừa hoàn thành: **Phase 8, 4 task**. Sửa DUY NHẤT 2 file:
`hrm-api/app/Console/Commands/Assign/SeedCareReportDemoCommand.php` (+233/-20) và
`e2e/tests/assign/potential-customer-care-export.api.spec.ts` (helper `esc()`).

Kết quả trên `hrm_tpe`: nhu cầu demo trải **7 lĩnh vực** (33/22/20/16/11/11/6 nhu cầu, đúng
6/4/4/3/2/2/1 nhóm ngành) thay vì dồn 1 dòng; **20 tỉnh** mỗi tỉnh 2 phường/xã thay vì 10 tỉnh
1 phường/xã. **37/37 e2e xanh** (18 API + 19 UI).

3 điều đáng nhớ:
· Không phải seeder tạo ra danh mục lệch — nó chỉ *dùng lại* thứ môi trường có, mà migration đã
  dồn toàn bộ nhóm ngành vào một lĩnh vực ("Khác" ở VPS, "Công nghiệp" ở local).
· Mã lĩnh vực KHÔNG dùng để khớp được (local `LVKDNB.IDUS` vs VPS `LVKDNB.0001`); mã nhóm ngành
  `NN.*` thì ổn định.
· Bản in escape HTML nên tên chứa `&` phải so bằng `&amp;` — assertion so chuỗi thô là sai, sản
  phẩm đúng.

Đang làm dở: (không)

Bước tiếp theo: **chưa commit** (user chưa yêu cầu). Trên VPS chạy theo thứ tự:
`git pull` → `php artisan assign:seed-care-demo --clean --force` → `php artisan assign:seed-care-demo --dry-run`
(kiểm dòng "Nhóm ngành sẽ gán lại lĩnh vực" phải ra **22**) → bỏ `--dry-run`.

Blocked: (không)

---

### Checkpoint — 2026-08-28 (Phase 7 — nghiệm thu UI, 6 task)

Vừa hoàn thành: **Phase 7 — 6 task từ phản hồi nghiệm thu của user**, đã commit + push ở CẢ 2 repo
(`hrm-client` 15be9a288 "fix loi bao cao ket qua cskh tiem nang" · `hrm-api` 575de2e41
"fix bao cao ket qua cskh tiem nang", nhánh `tpe`, cây làm việc sạch).

- 7.1–7.2 Rà lại toàn bộ mockup: bổ sung 6 tooltip ⓘ còn thiếu (mục đích báo cáo · 2 ô lọc · 3 dòng
  tiêu đề phần) + sửa nội dung 6 tooltip đã có cho đúng khuôn "tiêu đề IN HOA + gạch đầu dòng".
- 7.3 Bảng báo cáo + bảng popup: `nowrap` toàn bộ ô và tên cột, thêm thanh cuộn ngang **phía trên**
  (tự ẩn khi bảng vừa khung); phải dùng `ResizeObserver` mới đo đúng bề rộng.
- 7.4–7.5 Popup: chip "Phân bổ" đổ giá trị vào ô lọc (bỏ state `chips` song song); header đổi thành
  `N / M nhu cầu` với M là tổng TRƯỚC bộ lọc (BE tách `demandListBase()`).
- 7.6–7.7 Popup: "Xoá lọc" không còn thu nhỏ popup (tách `resetFilters` khỏi `resetLocal`); số
  trong hộp KPI bấm được để lọc sâu, kèm bỏ khối KPI + nút "Quay lại".
- 7.8–7.9 Cột Meeting: link mở panel chi tiết + nhãn "Kỳ trước" (BE trả `is_carried`); panel dùng
  lại `MeetingDetailDrawer` + 2 prop mới `extraBlocks`/`extraActions` để chèn khối "Nhu cầu thu
  thập được" và nút "Tạo dự án TKT".
- 7.10–7.12 Popup: căn giữa cột Trạng thái, 5 cột cơ cấu sắp xếp được; cột Dự án TKT có link + nút
  "Tạo mới" (quyền cũ `Quản lý dự án tiền khả thi` KHÔNG tồn tại nên nút chết); danh sách mới nhất
  lên trước; màn tạo dự án tự chọn sẵn KH + nhu cầu rồi **khoá** cả 2 ô.

**36/36 e2e của màn báo cáo xanh** (20 API + 16 UI) — thêm 5 ca mới (12→16) so với 31 ca của Phase 5.

Đang làm dở: (không)

Bước tiếp theo: user nghiệm thu lại màn. 2 việc còn treo chờ user quyết:
(1) làm giàu `assign:seed-care-demo` (thêm thành phần tham dự / khách hàng / nội dung / biên bản cho
meeting demo) để panel chi tiết meeting không trông rỗng khi demo trên VPS;
(2) mockup bỏ chế độ phóng to popup ở MỌI lần mở, bản hiện tại chỉ reset khi đổi chỉ tiêu.

Blocked: (không)

### Checkpoint — 2026-08-27 (Task 6.2 — loại meeting hệ thống trên môi trường mới)

Vừa hoàn thành: **Task 6.2**. User báo lệnh `assign:seed-care-demo` lỗi trên VPS vì thiếu loại
meeting "Họp tìm hiểu & Giới thiệu sản phẩm".

Kết luận: **KHÔNG cần viết seeder mới** — repo đã có sẵn
`Modules/Assign/Database/Seeders/SystemMeetingTypesSeeder.php` (`updateOrCreate` theo `code`, chạy
lại nhiều lần không nhân bản), và file đã có trên `origin/tpe` nên VPS chỉ cần `git pull`. Đã chạy
thử trên local: tạo đúng `id=7 · Họp tìm hiểu & Giới thiệu sản phẩm · has_customer=1 · status=1`.

Nguyên nhân gốc đã xử lý: thông báo lỗi của lệnh demo chỉ nói "thiếu loại meeting" mà không chỉ
cách khắc phục, nên phải đi tìm thủ công. Đã bổ sung câu lệnh khắc phục ngay trong thông báo (cả
nhánh thiếu loại meeting lẫn nhánh thiếu nhóm ngành có lĩnh vực cha), và kiểm bằng cách đổi tạm mã
loại meeting để ép vào nhánh lỗi — câu lệnh in ra đúng, dấu gạch chéo ngược không bị nuốt; sau đó
khôi phục mã cũ và chạy `--dry-run` xác nhận lệnh hoạt động bình thường.

Đang làm dở: (không)

Bước tiếp theo: **commit + push `app/Console/Commands/Assign/SeedCareReportDemoCommand.php`**
(đang là thay đổi DUY NHẤT chưa commit của cả 2 repo), rồi trên VPS chạy đủ 5 bước theo thứ tự ghi
ở Task 6.2 để dựng dữ liệu trình diễn.

Blocked: (không)

---

### Checkpoint — 2026-08-26 (Phase 6 — seeder demo, ĐÃ PUSH)

Vừa hoàn thành: **Task 6.1 — lệnh `assign:seed-care-demo`** sinh dữ liệu demo chạy được trên VPS.
User đã commit (`2f37c01af seeder test bao cao cskh tiem nang`) và push; đã xác minh lại: `HEAD`
khớp `origin/tpe` ở cả 2 repo và file `app/Console/Commands/Assign/SeedCareReportDemoCommand.php`
đã có mặt trên `origin/tpe`.

Kết quả chạy thật trên `hrm_tpe`: 40 meeting · 119 nhu cầu · 34 dự án TKT demo, trải 6 tháng /
10 tỉnh / 13 phòng ban / 24 nhóm ngành. Màn báo cáo ra 104 nhu cầu trong kỳ · 253,1 tỷ,
KPI 19,2% / 54,1% / 45,9%.

Đã kiểm chứng: idempotent (chạy 3 lần số không đổi) · `--clean` chỉ xoá đúng bản ghi mang tiền tố
`DEMO-CSKH-` (meeting thật 51→51, dự án thật 146→146, nhu cầu thật 11→11, không để lại nhu cầu trỏ
vào dự án đã xoá) · không ghi gì sang DB ERP · `npx playwright test potential-customer-care`
**31/31 xanh** khi dữ liệu demo đang nằm trong DB.

Đang làm dở: (không)

Bước tiếp theo: chạy lệnh trên VPS để dựng dữ liệu trình diễn —
`php artisan assign:seed-care-demo --dry-run` xem trước rồi bỏ `--dry-run` để ghi. Muốn phần
"Theo lĩnh vực" nhiều dòng cha hơn thì gán lĩnh vực kinh doanh nội bộ cho các nhóm ngành TRƯỚC khi
chạy (hiện 24 nhóm ngành chỉ trỏ vào 2 lĩnh vực).

Blocked: (không)

---

### Checkpoint — 2026-08-26 (ĐÃ MERGE + PUSH — kết thúc feature)

Vừa hoàn thành: user đã commit, merge cả 2 repo vào `tpe` và push. Đã xác minh lại:
`git merge-base --is-ancestor bao_cao_cskh_tiem_nang HEAD` trả về đúng ở **cả `hrm-api` lẫn
`hrm-client`**; `HEAD` khớp `origin/tpe` ở cả 2; cây làm việc sạch; các file của feature
(`pages/assign/report/potential-customer-care/`, `components/print/`, `utils/print/`,
`Modules/Assign/Export/PotentialCustomerCare*Export.php`) đều đã có mặt trên `tpe`.

Toàn feature: **5 phase** — Người chủ trì meeting · Gắn nhu cầu ở dự án TKT · Màn báo cáo ·
Xuất Excel + Bản in · Tài liệu (testcase + SRS). **31/31 e2e của màn báo cáo xanh**
(17 API + 14 UI); tổng cả feature 26 + 17 = 43 ca API và 14 ca UI.

Đang làm dở: (không)

Bước tiếp theo: chờ QA chạy bộ 167 testcase và user nghiệm thu SRS. **Khi deploy môi trường khác
BẮT BUỘC làm đủ 3 việc**: (1) chạy 2 migration; (2) insert thủ công 3 quyền id 1179–1181 rồi gán
vào role — `role_has_permissions` cần `company_id`, seeder truncate cả bảng nên KHÔNG chạy seeder
trên môi trường đang có dữ liệu; (3) bật cron `assign:close-expired-customer-demands`.

Blocked: (không)

---

### Checkpoint — 2026-08-26 (Excel + Bản in)

Vừa hoàn thành: Phase 4 — Xuất Excel (bảng theo dõi + danh sách popup) và Bản in (2 chế độ, popup xem trước A4 ngang có letterhead), + Task 4.8 cho bản in popup mang đủ bộ lọc/KPI/phân bổ. Port 3 file khuôn in dùng chung từ `gop_db` sang nhánh này. **31/31 e2e xanh** (17 API + 14 UI).
Đang làm dở: (không)
Bước tiếp theo: user nghiệm thu Excel + bản in. Còn lại của feature: SRS + testcase.xlsx. Khi deploy: chạy 2 migration + insert thủ công quyền 1179–1181 rồi gán role (`role_has_permissions` cần `company_id`) + bật cron `assign:close-expired-customer-demands`.
Blocked: (không)

### Checkpoint — 2026-08-25 (bộ lọc)

Vừa hoàn thành: Task 3.10 — sửa khối lọc Công ty/Phòng ban/Nhân viên: bỏ div `col-md-6` bọc ngoài (vỡ lưới) + đổi sang `:form="filters"` (bind cũ không có tác dụng, chọn phòng ban không lọc gì), Từ/Đến ngày lên `col-md-3`, thêm e2e ca 9 đã chứng minh fail trên code cũ. **22/22 e2e xanh** (10 API + 12 UI).
Đang làm dở: (không)
Bước tiếp theo: user nghiệm thu lại bộ lọc. Sau đó theo thứ tự: (1) Xuất Excel bảng theo dõi + danh sách popup, (2) bản In (in bảng theo dõi / in danh sách chi tiết), (3) SRS + testcase.xlsx. Khi deploy: chạy 2 migration + insert thủ công quyền 1179–1181 rồi gán role (`role_has_permissions` cần `company_id`) + bật cron `assign:close-expired-customer-demands`.
Blocked: (không)

### Checkpoint — 2026-08-25

Vừa hoàn thành: Task 3.9 — rà soát bộ lọc (cascade ở cả màn báo cáo lẫn popup, sắp xếp lại lưới, bỏ ô Bộ phận), tiêu đề popup nổi tên đối tượng, khối phân bổ theo đúng mockup. Toàn feature: 3 phase + 3 đợt chỉnh theo phản hồi, **26 e2e API + 18 e2e UI xanh**.
Đang làm dở: (không)
Bước tiếp theo: chờ user nghiệm thu UI. Nếu làm tiếp thì theo thứ tự: (1) Xuất Excel bảng theo dõi + danh sách popup, (2) bản In (2 lựa chọn: in bảng theo dõi / in danh sách chi tiết), (3) SRS + testcase.xlsx. Khi deploy: chạy 2 migration + insert thủ công quyền 1179–1181 rồi gán role (`role_has_permissions` cần `company_id`) + bật cron `assign:close-expired-customer-demands`.
Blocked: (không)