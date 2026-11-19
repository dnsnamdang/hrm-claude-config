# Agent — Kết quả dự án TKT theo báo cáo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `ket_qua_du_an_tkt` trả đúng số + cây + chi tiết của báo cáo "Kết quả thực hiện dự án TKT"; `thong_ke_du_an_tkt` thêm 5 chiều; Agent trả lời theo luật "hỏi gì trả lời đó, mở rộng sau, không có đáp án thì dừng".

**Architecture:** Tách phần kiểm quyền / phạm vi / trải cây dùng chung của công cụ thị trường (`MarketDevScope`, `MarketDevTree`) thành lớp cơ sở dùng `static::` (late static binding); thêm `TktResultScope` / `TktResultTree` cho mã quyền báo cáo TKT. Công cụ gọi thẳng `ProspectiveProjectResultReportService` (`getProjects`, `metricsOf`, `buildTree`, `summary`, `projectList`), không query riêng. FE tổng quát hoá thẻ cây theo cột BE gửi.

**Tech Stack:** Laravel 8 (PHP 7.4 + 8.1), PHPUnit; Nuxt 2 / Vue 2; Playwright (Node 20).

**Spec:** `HRM/docs/superpowers/specs/agent-chat/2026-11-17-agent-ket-qua-du-an-tkt-design.md`

Repo / nhánh: worktree `websites/wt-tpe-agent/{hrm-api,hrm-client}`, nhánh `gop_db-agent-ket-qua-du-an-tkt` (từ origin/gop_db). Không migration, không ghi DB ngoài transaction test.

## Global Constraints

- Mã quyền `presale.bao_cao_ket_qua_du_an_tkt.view`, tên "Xem báo cáo kết quả dự án TKT"; scope 2 phòng/bộ phận quản lý · 3 công ty · 4 tổng công ty (hỏi sâu công ty khác, `tap_doan`).
- Số của công cụ PHẢI bằng service báo cáo cùng tham số; không đọc cột `status` hiện tại (bẫy R7 — dùng `status_at_end`).
- Chặn quyền TRƯỚC khi gọi service (service không quyền âm thầm thu về dự án của mình).
- Mặc định `pham_vi` = phạm vi rộng nhất người hỏi được xem (scope ≥3 ⇒ cong_ty, 2 ⇒ phòng/bộ phận quản lý, còn lại ⇒ toi).
- Hỏi gì trả lời đó: `hien_thi=so_lieu` (hỏi "bao nhiêu") ⇒ đáp án là con số; `danh_sach` (hỏi "danh sách / những dự án nào") ⇒ đáp án là bảng. Không có đáp án (tổng 0, không tìm thấy, bị chặn) ⇒ không `bo_sung`, không block.
- Dữ liệu gửi model gọn: trần cây 60 dòng (`da_cat`, `so_dong_chua_hien`), không gửi `key`, không gửi cột Giá trị HĐ; chi tiết trần `ListLimit` 50.
- Mô tả công cụ tiếng Anh, tham số tiếng Việt không dấu; số theo chuẩn `1,234,567.5`.
- Giữ nguyên hành vi `phat_trien_thi_truong` (42 ca `PhatTrienThiTruongTest` phải xanh sau refactor).

## Review Focus

1. Kỳ quá khứ (tháng trước) — số phải theo trạng thái cuối kỳ, không theo hôm nay → ca parity với `last_month` (Task 3).
2. Người scope 2 không quyền phòng khác hỏi phòng khác / NV phòng khác → denied, không ra "0 dự án" (Task 2).
3. Hỏi 1 người có 0 dự án → chỉ câu "không có", không thẻ, không theo tiến trình (Task 3).
4. `tap_doan` → tổng = Σ từng công ty, `so_khach_hang` distinct trên hợp (Task 3).
5. Thẻ thị trường cũ (`market_tree` không có `cols`) hiển thị như trước (Task 5).

---

### Task 1: Lớp cơ sở dùng chung + giữ nguyên hành vi thị trường

**Files:**
- Create: `hrm-api/Modules/Agent/Support/ReportScopeGuard.php`, `hrm-api/Modules/Agent/Support/ReportTree.php`
- Modify: `hrm-api/Modules/Agent/Support/MarketDevScope.php`, `MarketDevTree.php`, `Modules/Agent/Tools/TimPhongBanTool.php`, `TimNhanVienTool.php`
- Test: `Modules/Agent/Tests/Feature/Tools/PhatTrienThiTruongTest.php` (chạy lại, không sửa kỳ vọng)

**Interfaces — Produces:**
- `abstract class ReportScopeGuard` với `const CODE`, `const NAME` (lớp con khai), các hàm static chuyển nguyên từ MarketDevScope, đổi `self::CODE/NAME/scope()` → `static::`: `scope(): int`, `phamVi(array): string`, `check(array): ?PermissionNeed`, `dateError(array): ?string`, `targetCompanyId(int $nv,int $bp,int $pb): ?int` (đổi private→protected), `companyLabel(int): string`, `phongTarget(array): array` (protected), `managedPartIds()`, `part(int)`, `ownManagedPartId()`, `id(array,string)` (protected).
- `ReportScopeGuard::groupWideAny(array $input): bool` = `toan_tap_doan` bật VÀ scope ≥4 ở MỘT trong `[MarketDevScope::CODE, TktResultScope::CODE]`; `goiYToanTapDoan(array,int)` dùng điều kiện tương ứng, thông điệp: "Không có trong công ty đang làm; câu về phát triển thị trường / kết quả dự án TKT thì thử lại với toan_tap_doan=true." tim_phong_ban / tim_nhan_vien gọi 2 hàm này (mô tả tham số `toan_tap_doan` nêu cả `ket_qua_du_an_tkt`).
- `MarketDevScope extends ReportScopeGuard` giữ `CRITERIA`, `PERIODS`, `STATUSES`, `request()`; `MarketDevScope::groupWide` giữ làm alias của `groupWideAny` (test cũ gọi).
- `abstract class ReportTree` có `flatten(array $tree, ?int $soCap, int $max = 60, ?int $rootTotal = null): array` chuyển nguyên, đọc `static::LOAI`, `static::LOAI_CO_ID`, `static::METRICS`, `static::LEAF_DIM` (dim dừng khi so_cap null — thị trường `'host'`). `MarketDevTree extends ReportTree` khai 4 hằng như cũ.

- [x] Step 1: chạy `php vendor/bin/phpunit Modules/Agent/Tests/Feature/Tools/PhatTrienThiTruongTest.php` + `TimPhongBanToolTest.php` ghi số ca xanh (mốc).
- [x] Step 2: tách lớp cơ sở như trên (cắt-dán, `self::`→`static::` cho hằng/hàm lớp con khai lại).
- [x] Step 3: chạy lại 2 file test — cùng số ca, xanh hết.
- [x] Step 4: commit `refactor(agent): tách ReportScopeGuard / ReportTree dùng chung cho báo cáo`.

### Task 2: `TktResultScope` + `TktResultTree` (quyền + ánh xạ tham số)

**Files:**
- Create: `hrm-api/Modules/Agent/Support/TktResultScope.php`, `TktResultTree.php`
- Test: Create `Modules/Agent/Tests/Feature/Tools/KetQuaDuAnTktReportTest.php`

**Interfaces — Produces:**
- `TktResultScope extends ReportScopeGuard`: `CODE = 'presale.bao_cao_ket_qua_du_an_tkt.view'`, `NAME = 'Xem báo cáo kết quả dự án TKT'`, `CRITERIA = ['phong_ban' => 'dept', 'thi_truong' => 'market', 'linh_vuc' => 'scope']`, `PERIODS = ['this_month','last_month','this_quarter','last_quarter','this_year','last_year']`, `KET_QUA = ['thanh_cong' => 'won', 'that_bai' => 'lost', 'dang_trien_khai' => 'open']`, `CHI_TIEU = ['tong' => 'total','lap_truoc_ky' => 'created_before','lap_trong_ky' => 'created_in','thanh_cong' => 'won','that_bai' => 'lost','dang_trien_khai' => 'open','dong_trong_ky' => 'closed']`.
- `TktResultScope::period(array $input): array` → `[Carbon $from, Carbon $to]` hoặc `['error' => …]` (chuyển nguyên `KetQuaDuAnTktTool::period`, kèm `dateError`).
- `TktResultScope::request(array $input, ?int $companyId = null): array` → `[Request, meta]`; Request gồm `period=custom, from, to, criteria, company_id` (tham số hoặc công ty đối tượng / đang làm), `employee_id | part_id | department_id` (như MarketDevScope::request, `toi` ⇒ employee_id = người hỏi), `customer_id`, `status` (tien_trinh dùng `DuAnTktTool::STEP`), `result`, `province_id` (khớp tên bằng `MeetingMarketScope::matchProvinces`, "chưa xác định" ⇒ không lọc được: meta `tinh_khong_loc`), `scope_id` (tên lĩnh vực → `internal_business_scopes.id`, khớp LIKE, nhiều ⇒ lấy đầu + meta), `industry_id` (tên nhóm ngành → `hrm_scopes.id`). meta: `pham_vi_text`, `thu_ve_bo_phan`, `tinh*`, `cong_ty_khac`.
- `TktResultScope::companyIds(): array` — `tap_doan`: id mọi công ty có dự án TKT (`prospective_projects.company_id` distinct, có tên trong `companies`).
- `TktResultTree extends ReportTree`: `LOAI = ['dept'=>'phong_ban','part'=>'bo_phan','emp'=>'nhan_vien','province'=>'thi_truong','scope'=>'linh_vuc','industry'=>'nhom_nganh','company'=>'cong_ty']`, `LOAI_CO_ID = ['phong_ban','bo_phan','nhan_vien']`, `METRICS = ['total','open','closed','won','lost','success_rate','expected_amount']`, `LEAF_DIM = 'emp'`.

- [x] Step 1: test quyền (dữ liệu tạo trong transaction như `PhatTrienThiTruongTest`): toi không quyền ⇒ null; phong không quyền ⇒ PermissionNeed code đúng; scope 2 phòng quản lý ⇒ null, phòng khác ⇒ denied; cong_ty scope 2 ⇒ denied; tap_doan scope 3 ⇒ denied scopeNeeded 4; NV công ty khác scope 3 ⇒ denied, scope 4 ⇒ null; mặc định không tham số scope 3 ⇒ phamVi cong_ty.
- [x] Step 2: test `request()`: map đủ từng tham số ra đúng khoá service; tu_ngay không năm hợp lệ / ngày sai ⇒ error.
- [x] Step 3: chạy — FAIL; viết 2 lớp; chạy — PASS.
- [x] Step 4: commit `feat(agent): TktResultScope — quyền + tham số báo cáo kết quả dự án TKT`.

### Task 3: Nâng cấp `KetQuaDuAnTktTool`

**Files:**
- Modify: `hrm-api/Modules/Agent/Tools/KetQuaDuAnTktTool.php`, `Modules/Agent/Tests/Feature/Tools/KetQuaDuAnTktTest.php` (sửa kỳ vọng cũ theo khuôn mới)
- Test: `KetQuaDuAnTktReportTest.php` (tiếp)

**Interfaces — Consumes:** Task 2. **Produces:** công cụ `ket_qua_du_an_tkt` (tên giữ nguyên, tổng số công cụ không đổi).

Tham số thêm theo spec §5.1: `tieu_chi, pham_vi (+tap_doan), bo_phan_id, tinh, khach_hang_id, tien_trinh, ket_qua, linh_vuc, nhom_nganh, so_cap, chi_tieu, so_luong, hien_thi (so_lieu|danh_sach)`. `permissionNeed()` = `TktResultScope::check`.

Chế độ (theo thứ tự xét):
1. Tổng 0 dự án ⇒ `ToolResult::ok(['tra_loi' => ['tong' => 0], 'pham_vi', 'ky', + meta lỗi lọc nếu có], 0, null)` — không `bo_sung`, không block.
2. `chi_tieu` ⇒ `projectList` (Request + `metric`, `drill_key=''`, `per_page=so_luong`): data `{chi_tieu, tra_loi:{tong, tong_dau_tu}, dong:[{ma,ten,khach_hang,nvkd,tien_trinh_cuoi_ky,ngay_lap,dau_tu}]}`, block `tasks` (khuôn item của `projectList()` hiện có, link `/assign/prospective-projects/{id}/manager`).
3. Người (`toi`/`nhan_vien_id`): data `{hien_thi, tra_loi:{tong, lap_trong_ky, lap_truoc_ky, dang_trien_khai, thanh_cong, that_bai, ty_le_thanh_cong, dau_tu_du_kien}, bo_sung:{theo_tien_trinh:[{ten,so}] (theo bước tăng dần, theo status_at_end), so_du_an_trong_the}}`; block `tasks` gồm TOÀN BỘ dự án tới trần 50 (`con_lai` khi vượt); `danh_sach` ⇒ block thêm `nhom: {title:'Theo tiến trình', unit:'dự án', items:[{label,value}]}` (FE vẽ dưới danh sách, Task 5).
4. Phòng / công ty / tập đoàn: `{tieu_chi, tra_loi:{tong, dang_trien_khai, dong_trong_ky, thanh_cong, that_bai, ty_le_thanh_cong, dau_tu_du_kien}, tong_hop:{lap_truoc_ky, lap_trong_ky, so_khach_hang}, cay:[TktResultTree rows, bỏ key], da_cat, so_dong_chua_hien}`; block `{type:'market_tree', cols:[…6 cột Tổng/Đang TK/TC/TB/Tỷ lệ/Đầu tư DK…], summary_line, rows, link:'/assign/report/prospective-project-results', so_dong_an}` (khuôn block thị trường). `danh_sach` ở phạm vi này ⇒ như chế độ 2 với `chi_tieu=tong`, block danh sách + `nhom` theo tiến trình.
- `tap_doan`: lặp `companyIds()`, gọi `getProjects` từng công ty (Request mới mỗi lần — service cache theo đối tượng Request), cây gốc thêm node `company` (metrics = `metricsOf` của công ty); tổng = `metricsOf` của tập gộp; `so_khach_hang` distinct trên tập gộp.

- [x] Step 1: test parity: với dữ liệu fixture, cho 3 tiêu chí × {this_month, last_month}: `tra_loi` == `report()['total']`, cây (trước cắt) == `buildTree` cùng Request (so ten + total/won/lost từng dòng).
- [x] Step 2: test chi tiết: mỗi `chi_tieu` số dòng == `projectList()['total']`.
- [x] Step 3: test người: tong == số item block; `theo_tien_trinh` cộng lại == tong; tổng 0 ⇒ block null, không `bo_sung`; `danh_sach` ⇒ block có `nhom`.
- [x] Step 4: test cắt cây > 60 ⇒ `da_cat`; `tap_doan` scope 4 tổng == Σ từng công ty; scope 3 ⇒ denied.
- [x] Step 5: chạy FAIL → viết → PASS; chạy cả `Modules/Agent/Tests` (ghi lại ca đỏ không liên quan, vd `AgentQuotaServiceTest` float).
- [x] Step 6: commit `feat(agent): ket_qua_du_an_tkt theo đúng báo cáo — tiêu chí, cây, chi tiết, hỏi gì trả lời đó`.

### Task 4: `thong_ke_du_an_tkt` thêm 5 chiều

**Files:** Modify `hrm-api/Modules/Agent/Tools/ThongKeDuAnTktTool.php`; Test `Modules/Agent/Tests/Feature/Tools/KdTruocBanToolsTest.php` (hoặc file đang chứa ca thong_ke_du_an_tkt — grep).

- `GROUPS` thêm `thang` (DATE_FORMAT(created_at,'%m/%Y'), sắp theo thời gian), `nhom_giai_phap` (`industry_id` → `industries.name`), `ung_dung` (`application_id` → `applications.name`), `linh_vuc_kh` (`customer_scope_id` → bảng của lĩnh vực KD khách hàng — tra model `ProspectiveProject` quan hệ của cột này), `loai_hinh` (`customer_scope_group_id` → bảng tương ứng). Rỗng ⇒ "Chưa xác định". Mô tả: `linh_vuc` = lĩnh vực công ty KD (cha nhóm ngành), "lĩnh vực của khách hàng" ⇒ `linh_vuc_kh`; số theo quyền danh sách dự án; câu kết quả / thành công / thất bại trong kỳ ⇒ `ket_qua_du_an_tkt`.
- [x] Step 1: test mỗi chiều: tổng các nhóm == tổng không nhóm; nhãn đúng bảng danh mục (không phải hrm_scopes).
- [x] Step 2: FAIL → viết → PASS → commit `feat(agent): thong_ke_du_an_tkt thêm theo tháng, nhóm giải pháp, ứng dụng, lĩnh vực KD khách hàng, loại hình`.

### Task 5: Prompt + eval

**Files:** Modify `hrm-api/Modules/Agent/Services/AgentPrompt.php`, mô tả `DuAnTktTool` (1 câu hướng sang 2 công cụ kia), `Tests/fixtures/eval/questions.json`.

- Luật 6 thêm câu: "Hỏi gì trả lời đó: dòng đầu là đáp án đúng dạng câu hỏi (hỏi bao nhiêu ⇒ con số; hỏi danh sách ⇒ 1 câu dẫn, bảng ở thẻ); phần mở rộng sau đáp án. Kết quả không có đáp án (0 kết quả, không tìm thấy, bị chặn) thì chỉ nói điều đó, không thêm số liệu mở rộng."
- Luật 16 (dự án TKT): kết quả / số dự án trong kỳ / thành công / thất bại / tỉ lệ / theo phòng, NV, tỉnh, lĩnh vực công ty KD ⇒ `ket_qua_du_an_tkt` (tieu_chi theo chủ thể; hien_thi theo dạng câu; bỏ trống pham_vi khi không nêu chủ thể; toan_tap_doan như luật 15; câu nối tiếp giữ lọc; hỏi sâu 1 số ⇒ chi_tieu; có `bo_sung` thì nêu sau đáp án, không chép danh sách). Nhóm giải pháp / ứng dụng / lĩnh vực của khách hàng / loại hình / theo tháng / tiến trình hiện tại / lý do đóng ⇒ `thong_ke_du_an_tkt`. Danh sách lọc (sắp đóng, đứng im, top ngân sách) ⇒ `du_an_tkt`.
- Eval thêm ~10 câu (226…): "Anh A có bao nhiêu dự án trong tháng 10", "Danh sách dự án của anh A tháng 10", "Tháng này phòng nào nhiều dự án TKT nhất", "Quý này tỉnh nào nhiều dự án", "Dự án theo lĩnh vực công ty năm nay", "Dự án theo nhóm giải pháp", "Dự án theo ứng dụng", "Dự án thất bại tháng trước là những dự án nào", "Kết quả dự án TKT toàn tập đoàn quý này", "Lĩnh vực của khách hàng nào nhiều dự án nhất".
- [x] Step 1: sửa; chạy `Modules/Agent/Tests` (test prompt / đếm) xanh; commit `feat(agent): luật hỏi gì trả lời đó + định tuyến dự án TKT`.

### Task 6: FE thẻ

**Files:** Modify `hrm-client/components/agent/AgentMarketTree.vue` (nhận `block.cols`; thiếu ⇒ bộ cột meeting cũ; `block.link` thiếu ⇒ link báo cáo thị trường như cũ), `AgentResultBlock.vue` (nhánh `tasks`: vẽ `block.nhom` dạng bars ngay dưới danh sách, dùng lại markup nhánh `bars`; dòng "còn N dự án" khi `block.con_lai`).
Bố cục giữ phương án B user đã chọn cho thẻ thị trường (không mockup mới — chỉ đổi bộ cột).
- [x] Step 1: Playwright (spec `e2e/tests/agent/agent-market.spec.ts` thêm 2 ca giả lập bằng page.route: cây TKT 6 cột, danh sách + "Theo tiến trình") — đo số cột, thứ tự thẻ, không tràn ngang ngăn Agent; ca thị trường cũ giữ nguyên.
- [x] Step 2: commit `feat(agent): thẻ cây theo cột BE + nhóm theo tiến trình dưới danh sách`.

### Task 7: Kiểm cuối

- [x] Restart :8070 AGENT_FAKE=1 (user cho 18/11), chạy `agent-chat`, `agent-chat-pin`, `agent-market` — đọc dòng tổng kết; trả :8070 về thường.
  - 18/11: agent-chat 22/23 (ca :900 "mở panel" fail ở bước Vấn đề — spec đã theo Vấn đề v2 `60849bd82` có trên origin/gop_db, nhánh này chưa có ⇒ không phải lỗi đợt này; chạy lại sau khi merge gop_db) · agent-chat-pin 6/6 · agent-market 6/6. Đã xoá 4 vấn đề tạm 5486–5489 do ca fail để sót; 6 vấn đề tạm cũ (1049,1050,1093,1094,3047,3048) có từ 15–17/11, chưa xoá.
- [x] Eval Haiku thật các câu mới + bộ câu TKT/thị trường cũ; đối chiếu 2–3 câu với màn báo cáo local cùng lọc.
- [x] Cập nhật checkpoint plan + README §3b + memory.

### Checkpoint — 17/11/2026 khuya
Vừa hoàn thành: Task 1–6 + kiểm cuối (trừ e2e chat). hrm-api 11 commit b9faa6266..89996d7d4, hrm-client 2 commit fe8b42f97..9a5b2c3f2, nhánh gop_db-agent-ket-qua-du-an-tkt (wt-tpe-agent), CHƯA push. PHPUnit Agent 357 OK; e2e agent-market 6 passed; eval thật toàn bộ 236 câu 225/236 công cụ (trượt: lương tắt local #79–84, đã biết #41/#43/#52, mới #152 #212 — parked); hỏi thật 3 khuôn (bao nhiêu / danh sách / không có) đúng ý user.
Đang làm dở: —
- **18/11/2026 — ĐÃ DEPLOY TPE** (merge gop_db api `3ae239a02` · client `883eaed3c`; không migration). Thử prod: NV 13 (scope 4) "Kết quả dự án TKT tháng 10 theo phòng ban" ⇒ ket_qua_du_an_tkt ok, 459 dự án, 34.6₫; NV 157 (không quyền) ⇒ phạm vi tôi, 0, 1 câu.
Bước tiếp theo: phần Giải pháp (user chốt 18/11: "tham gia GP" = cả 4 vai trò PM / thành viên GP / leader hạng mục / thành viên hạng mục, đếm distinct, chia theo vai trò); chạy lại e2e agent-chat :900 trên nhánh mới tách từ gop_db.
Blocked: không.
Parked: #152 câu không kỳ đi ket_qua; #212 dừng sau meeting_cua_phong; e2e 1024px bảng cols; linh_vuc_kh theo KH trực tiếp; tap_doan chi tiết gọi getProjects 2 lần; detail() thiếu ghi_chu định nghĩa; test người chỉ có scope 4 quyền TKT dùng toan_tap_doan.

---

# Phần 2 — Agent Giải pháp theo báo cáo "Tổng hợp GP theo phòng ban" Implementation Plan (18/11/2026)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Công cụ mới `tong_hop_giai_phap` trả đúng số + cây + chi tiết của báo cáo "Tổng hợp GP theo phòng ban"; `thong_ke_giai_phap` đếm NV tham gia đủ 4 vai trò; prompt định tuyến câu GP.

**Architecture:** `GpSummaryScope` / `GpSummaryTree` kế thừa `ReportScopeGuard` / `ReportTree` (khuôn TKT). Công cụ gọi thẳng `SolutionsWorkSummaryByDepartmentReportService::getReport` / `getModalSolutionList` với Request dựng từ tham số — không query riêng. Tập đoàn: service đã hỗ trợ (không truyền company_id + scope 4 ⇒ mọi công ty, gốc cây = công ty) ⇒ KHÔNG lặp từng công ty như TKT. FE không sửa (thẻ `market_tree` có `cols` + `tasks` có `nhom` đã có từ 17/11).

**Tech Stack:** Laravel 8 (PHP 7.4 + 8.1), PHPUnit; Playwright (Node 20).

**Spec:** `HRM/docs/superpowers/specs/agent-chat/2026-11-18-agent-tong-hop-giai-phap-design.md`

Repo / nhánh: worktree `websites/wt-tpe-agent/hrm-api` (client không đổi), nhánh MỚI `gop_db-agent-tong-hop-giai-phap` tách từ `origin/gop_db` (`3ae239a02` trở lên). Không migration, không quyền mới, không ghi DB ngoài transaction test.

## Global Constraints

- Mã quyền `presale.bao_cao_tong_hop_gp.view`, tên lấy từ bảng permissions (Catalog `presale.php:354`); phạm vi 1–4. Chặn quyền TRƯỚC khi gọi service (service không quyền âm thầm thu về GP mình tạo).
- Mặc định `pham_vi` = rộng nhất được xem (≥3 ⇒ cong_ty, 2 ⇒ phòng/bộ phận quản lý, còn lại ⇒ toi). `toi` ⇒ employee_id = người hỏi (kỹ sư chính). `tap_doan` ≥4 ⇒ không truyền company_id. Đối tượng công ty khác ⇒ ≥4 + truyền company_id của đối tượng.
- Số của công cụ PHẢI bằng `getReport` / `getModalSolutionList` cùng tham số (bỏ Nháp, kỳ theo ngày tạo GP, phòng = phòng hiện tại của kỹ sư chính).
- Kỳ mặc định `this_month` (như màn). PERIODS như TKT + `tu_ngay`/`den_ngay`.
- Chỉ tiêu ⇒ list_kind: tong=all · da_lam=totalGpDone · dung_han=gpOnTime · tre_han=gpLate · chot=gpChot · yc_tiep_nhan=requestAccepted.
- Cột thẻ cây (`cols`): Tổng GP (gp_non_draft) · Đã làm (total_gp_done) · Đúng hạn (gp_on_time) · Trễ hạn (gp_late) · Chốt (gp_chot) · Tỷ lệ chốt (chot_rate_percent, kiểu percent). Link `/assign/report/solutions-work-summary-by-department`. Không gửi khối báo giá / hợp đồng.
- Hỏi gì trả lời đó: `tra_loi` / `bo_sung.theo_tien_trinh` (status_breakdown_display); tổng 0 ⇒ `GHI_CHU_KHONG_CO` kiểu TKT ("Không có giải pháp: …"), không block.
- NV tham gia = hợp distinct theo GP của: `solutions.pm_id` · `solution_members.member_id` (status=1) · `solution_modules.leader_id` · `solution_module_members.member_id` (status=1, `SolutionMemberStatus::ACTIVE`).
- "Đang tham gia" không nêu kỳ ⇒ bỏ GP thuộc `GiaiPhapTool::GP_FINISHED`; nêu kỳ ⇒ giữ logic kỳ hiện có.
- Mô tả công cụ tiếng Anh, tham số tiếng Việt không dấu; số `1,234,567.5`; giữ xanh toàn bộ `Modules/Agent/Tests`.

## Review Focus

1. Trưởng phòng (scope 2) hỏi phòng mình: service lọc theo phòng NGƯỜI TẠO GP, cây xếp theo phòng KỸ SƯ CHÍNH ⇒ có thể ra dòng phòng khác — số vẫn phải = báo cáo cùng người dùng, ghi_chu nói rõ (Task 2).
2. Scope 2 hỏi phòng không quản lý / NV phòng khác ⇒ denied, không ra "0 giải pháp" (Task 1).
3. 1 người vừa PM vừa leader hạng mục cùng GP ⇒ tính 1 GP, có ở cả 2 vai trò (Task 3).
4. GP has_modules=1 có thành viên ở `solution_module_members` nhưng không ở `solution_members` ⇒ vẫn được đếm (Task 3).
5. `tap_doan` ⇒ tổng = Σ các nút công ty; không quyền 4 ⇒ denied (Task 2).

### Task 1: `GpSummaryScope` + `GpSummaryTree`

**Files:** Create `Modules/Agent/Support/GpSummaryScope.php`, `GpSummaryTree.php`; Modify `ReportScopeGuard.php` (thêm mã vào `GROUP_WIDE_CODES`, câu `GOI_Y_TOAN_TAP_DOAN` thêm "/ tổng hợp giải pháp"); Test `Tests/Feature/Tools/TongHopGiaiPhapScopeTest.php`.

**Interfaces — Produces:**
- `GpSummaryScope extends ReportScopeGuard`: `CODE`, `NAME`, `SUBJECT = 'tổng hợp giải pháp'`, `PERIODS`, `CHI_TIEU` (map ở Global Constraints), `TIEN_TRINH` (khoá không dấu ⇒ `Solution::STATUS_*`, bỏ Nháp), `period(array $input): array` (mặc định this_month ⇒ `['from_date','to_date']` Y-m-d), `request(array $input): array` (params cho service: from_date, to_date, company_id (bỏ khi tap_doan), department_id, part_id, employee_id, customer_id, scope_id, industry_id, application_id, solution_status, project_status + `meta` cờ `*_khong_khop` khi tên danh mục không khớp — khuôn `TktResultScope::danhMuc`).
- `GpSummaryTree extends ReportTree`: `LOAI` (company / department / employee theo node của `buildTreeFromNodes`), `LOAI_CO_ID = ['phong_ban','nhan_vien']`, `METRICS = ['gp_non_draft','total_gp_done','gp_on_time','gp_late','gp_chot','chot_rate_percent']`, `LEAF_DIM` theo khoá node NV của cây báo cáo (đọc `buildTreeFromNodes` dòng 863–957).
- [x] Step 1: test quyền: không quyền + `toi` ⇒ null (cho phép); không quyền + `phong` ⇒ denied tên quyền; scope 2 phòng quản lý ⇒ null, phòng khác ⇒ denied; scope 3 `tap_doan` ⇒ denied; scope 4 `tap_doan` ⇒ null; NV công ty khác ⇒ cần 4. Test `request()`: this_month ⇒ from/to đầu–cuối tháng; `tap_doan` ⇒ không có company_id; tên nhóm GP sai ⇒ cờ khong_khop.
- [x] Step 2: FAIL → viết → PASS; `PhatTrienThiTruongTest` + `KetQuaDuAnTkt*Test` vẫn xanh → commit `feat(agent): GpSummaryScope + GpSummaryTree theo báo cáo tổng hợp GP`.

### Task 2: Công cụ `tong_hop_giai_phap`

**Files:** Create `Modules/Agent/Tools/TongHopGiaiPhapTool.php`; Modify `Tools/AgentToolRegistry.php`; Test `Tests/Feature/Tools/TongHopGiaiPhapTest.php`.

**Interfaces — Consumes:** Task 1. **Produces:** tool name `tong_hop_giai_phap`; tham số theo spec §5.1 (`ky, tu_ngay, den_ngay, pham_vi, phong_ban_id, bo_phan_id, nhan_vien_id, toan_tap_doan, khach_hang_id, nhom_nganh, nhom_giai_phap, ung_dung, tien_trinh, tien_trinh_du_an, so_cap, chi_tieu, hien_thi, so_luong`).

Khuôn `KetQuaDuAnTktTool` (đọc trước): chế độ tổng hợp (cây + `tra_loi` + `bo_sung.theo_tien_trinh`, block `market_tree` có `cols` + `link`), chế độ chi tiết khi có `chi_tieu` hoặc `hien_thi=danh_sach` (`getModalSolutionList` với `rollup_key` của nút được hỏi hoặc `grand`, block `tasks` + `nhom` theo tiến trình + `con_lai`, unit "giải pháp", link mỗi GP `/assign/solutions/{id}` — kiểm route FE thật), tổng 0 ⇒ ghi_chu dừng, không block. `ghi_chu` định nghĩa: kỳ theo ngày tạo GP; phòng = phòng hiện tại của kỹ sư chính (leader hạng mục đầu, không có ⇒ người tạo); quyền theo phòng người tạo GP; Tổng GP đã làm = từ Đã duyệt GP trở đi; tỷ lệ chốt = GP chốt / tổng GP.
- [x] Step 1: test parity (dữ liệu local, transaction): `tong`, cây 2 cấp, `chi_tieu=tre_han` = `getReport`/`getModalSolutionList` cùng Request; `tap_doan` tổng = Σ nút công ty; 0 kết quả ⇒ ghi_chu, không block; `hien_thi=danh_sach` ⇒ `tra_loi` chỉ tổng; registry có tool.
- [x] Step 2: FAIL → viết → PASS → commit `feat(agent): tong_hop_giai_phap theo báo cáo Tổng hợp GP theo phòng ban`.

### Task 3: `thong_ke_giai_phap` — NV tham gia 4 vai trò

**Files:** Modify `Modules/Agent/Tools/ThongKeGiaiPhapTool.php`; Test `Tests/Feature/Tools/LamGiaiPhapTest.php` (thêm ca).

- `nhom_theo=thanh_vien`: tập người/GP = hợp 4 nguồn (Global Constraints); mỗi nhóm thêm `vai_tro: {pm, thanh_vien_gp, leader_hang_muc, thanh_vien_hang_muc}`; 1 GP chỉ +1 vào `solutions` của người đó. Note đổi: "A solution is counted once per participant (PM, solution member, module leader, module member)".
- `pham_vi=nguoi` / `toi`: điều kiện "tham gia" mở rộng cùng hợp 4 nguồn (toi giữ thêm created_by).
- Không nêu kỳ + (`nhom_theo=thanh_vien` hoặc pham_vi nguoi/toi) ⇒ bỏ GP `GP_FINISHED`, ghi `period: 'đang làm (chưa xong)'`. Có kỳ ⇒ như cũ.
- Mô tả công cụ: thêm "participants = PM + members + module leaders + module members"; phòng làm GP / tiến trình / tỷ lệ chốt ⇒ `tong_hop_giai_phap`.
- [x] Step 1: test: người PM + leader cùng GP ⇒ 1 GP, vai_tro pm=1 leader=1; thành viên hạng mục (has_modules=1) được đếm; GP Đóng không tính khi không kỳ; tổng distinct đúng trên dữ liệu tạo trong transaction.
- [x] Step 2: FAIL → viết → PASS; `LamGiaiPhapTest` cũ xanh → commit `feat(agent): thong_ke_giai_phap đếm người tham gia đủ 4 vai trò`.

### Task 4: Prompt + eval

**Files:** Modify `Modules/Agent/Services/AgentPrompt.php`, mô tả `GiaiPhapTool` (1 câu hướng sang 2 công cụ thống kê), `Tests/fixtures/eval/questions.json`.
- Luật định tuyến GP (thêm vào luật 16 hoặc luật 17 mới) theo spec §5.4.
- Eval ~10 câu (237…): "Tháng này phòng nào làm nhiều giải pháp nhất", "Tiến trình giải pháp tháng này", "Tỷ lệ chốt giải pháp năm nay theo phòng", "Giải pháp trễ hạn tháng trước là những GP nào", "Anh A đang tham gia bao nhiêu giải pháp", "Ai tham gia nhiều giải pháp nhất", "Phòng X tháng 10 làm bao nhiêu GP", "Tổng hợp giải pháp toàn tập đoàn quý này", "Danh sách GP đã chốt tháng này", "Tôi đang tham gia mấy giải pháp" — tên người/phòng lấy từ DB local có dữ liệu GP thật.
- [x] Step 1: sửa; `Modules/Agent/Tests` xanh; eval thật câu mới (`HRM/.plans/agent-chat/agent/scripts/eval_nhom.php 237-246`) đúng công cụ; commit `feat(agent): định tuyến câu giải pháp sang tong_hop_giai_phap / thong_ke_giai_phap`.

### Task 5: Kiểm cuối

- [x] Hỏi Haiku thật 3 khuôn (bao nhiêu / danh sách / không có) cho GP; đối chiếu 2 câu với màn báo cáo local cùng lọc (Playwright đo số trên DOM).
- [x] e2e: agent-market (thẻ cây cols) + agent-chat + agent-chat-pin (restart :8070 AGENT_FAKE — HỎI user trước), gồm ca :900 Vấn đề v2 nay đã có code.
- [x] Eval toàn bộ; cập nhật checkpoint plan + README §3b + memory.

### Checkpoint — 18/11/2026 sáng
Vừa hoàn thành: Phần 2 Task 1–5 + review toàn nhánh + 1 đợt sửa (+1 sửa residual). hrm-api nhánh `gop_db-agent-tong-hop-giai-phap` (wt-tpe-agent) 52b93ae17..525a451c9, 10 commit, CHƯA push; hrm-client không đổi code (worktree chuyển sang nhánh cùng tên @883eaed3c). PHPUnit Agent 394 OK; eval thật 25/25 câu GP + hồi quy; e2e agent-chat + agent-chat-pin + agent-market 35/35 (gồm ca :900 Vấn đề v2); hỏi thật: phòng nhiều GP nhất / danh sách trễ hạn năm nay (34, 1 câu dẫn + định nghĩa) / Hà Mạnh Cường tham gia 1 GP (thẻ 1 dòng) / ai tham gia nhiều nhất (cả công ty) / 0 kết quả 1 câu.
Đang làm dở: —
- **18/11/2026 — ĐÃ DEPLOY TPE** api `9e8361620` (merge gop_db; client giữ 883eaed3c; không migration). Thử prod NV 13: "Năm nay phòng nào làm nhiều GP nhất" ⇒ tong_hop_giai_phap, Ô tô 1 = 10 GP (197₫, lượt đầu ghi cache); "Ai tham gia nhiều GP nhất" ⇒ thong_ke_giai_phap thanh_vien cả công ty, 11 người (35₫).
Bước tiếp theo: —
Blocked: —
Parked: I1 người scope<3 không quản lý phòng hỏi "ai tham gia nhiều nhất" ra "thiếu quyền" (không rơi về toi); lệch chữ luật 16 vs ghi_chu không có (ghi_chu thắng); TKT chi_tieu+danh_sach có thể cũng gửi gạch đầu dòng (chưa kiểm); hỏi 1 người / danh sách gọi service 2–3 lần (chậm, không sai); test parity skip khi "năm nay" chưa có GP (đầu 2027 đọc dòng tổng kết); báo cáo gốc tính GP Đóng quá ngày kết thúc là trễ hạn (34/35) — vấn đề ngoài luồng của báo cáo, không sửa.

### Checkpoint — 18/11/2026 (sửa tồn)
Vừa hoàn thành: 2 tồn — (1) thong_ke_giai_phap thanh_vien không nêu phạm vi: scope ≥3 ⇒ công ty, xem được phòng mình ⇒ phòng, còn lại ⇒ GP của tôi (trước: "thiếu quyền"); 0 kết quả ở phạm vi mặc định ⇒ ghi_chu dừng 1 câu, cấm gọi lại phạm vi rộng hơn. (2) ket_qua_du_an_tkt chi_tieu + danh_sach ⇒ chỉ 1 câu dẫn + thẻ có nhóm tiến trình đếm đủ tập (đi trang projectList 200/trang). hrm-api nhánh `gop_db-agent-gp-tkt-ton` 9e8361620..1de105f1d (2 commit), ĐÃ PUSH + MERGE gop_db 18/11 (`4b1447069`), CHƯA deploy. PHPUnit Agent 395 OK; hỏi thật: "Dự án TKT thất bại tháng trước là những dự án nào" ⇒ 1 câu dẫn + thẻ; NV 62 "Ai tham gia nhiều GP nhất" ⇒ 1 câu nêu phạm vi của mình.
Bước tiếp theo: khi user báo deploy ⇒ deploy TPE (chỉ api, không migration). Lưu ý: deploy của bất kỳ ai từ giờ cũng kéo bản này lên.
Blocked: chờ user.
