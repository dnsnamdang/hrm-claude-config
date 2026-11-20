# Agent — Công việc theo nhân viên — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Agent trả lời được câu hỏi đếm / xếp hạng / so sánh / chi tiết việc THEO NGƯỜI (5 loại việc), số khớp báo cáo "Kế hoạch & kết quả làm việc theo nhân viên".

**Architecture:** Công cụ Agent mới `cong_viec_theo_nhan_vien` gọi lại `EmployeeWorkPerformanceService` (luật phạm vi NV) + `WorkAssignmentCollector` (gom cặp việc × người, 4 nhóm). Bộ gom thêm tuỳ chọn `openOnly` (chỉ việc chưa xong) cho chế độ "đang tồn". Đếm theo người + "hoàn thành trễ" nằm ở `Modules/Agent/Support/WorkByEmployee.php`. FE thêm thẻ `work_rank`; chi tiết dùng lại thẻ `tasks`.

**Tech Stack:** Laravel (PHP 7.4/8.1), PHPUnit với `DatabaseTransactions` trên DB local `db_gop_6_11`; Nuxt 2 / Vue 2.

**Spec:** `HRM/docs/superpowers/specs/agent-chat/2026-11-19-agent-cong-viec-theo-nhan-vien-design.md`

**Nơi làm:** worktree `websites/wt-tpe-agent/{hrm-api,hrm-client}`, nhánh mới `gop_db-agent-cong-viec-theo-nhan-vien` tách từ `origin/gop_db` ở cả 2 repo. Không migration, không seeder. Server :8070/:3070 chạy từ worktree này (đổi nhánh ⇒ server chạy theo).

## Global Constraints

- Quyền người khác: mã `assign.bao_cao_ke_hoach_ket_qua_lam_viec.view`, tên "Xem báo cáo kế hoạch & kết quả làm việc" (id local 1612). `pham_vi=toi` không cần quyền. KHÔNG bypass super admin.
- Chỉ công ty đang làm việc (`TaskScopeGuard::companyId()`), không có cấp tập đoàn.
- 5 loại tham số ↔ khoá cặp của báo cáo: `nhiem_vu`→`task`, `van_de`→`issue`, `meeting`→`meeting`, `phieu_cong_tac`→`trip`, `phieu_giao_viec`→`job`.
- 4 nhóm lấy NGUYÊN từ `bucketOf()` (`done`/`doing`/`late`/`cancel`) — không map lại trạng thái; meeting qua ngày chưa Hoàn thành + việc nháp/chờ duyệt vẫn tính như báo cáo (chốt §2.6).
- `tre_han` = `qua_han` + `hoan_thanh_tre`; `hoan_thanh_tre` chỉ Nhiệm vụ (`COALESCE(submitted_at, completed_at)` > `due_date` + `COALESCE(due_time,'23:59:59')`) và Vấn đề (`COALESCE(resolved_at, completed_at)` > hạn của cặp).
- Kỳ: có `tu_ngay`/`den_ngay` ⇒ chế độ `ky`. Không có ⇒ `xep_theo` ∈ {qua_han, dang_lam, chua_xong} hoặc không xếp ⇒ `dang_ton`; `xep_theo` ∈ {hoan_thanh, tre_han, tong} ⇒ tháng này. Kỳ mặc định ⇒ `ky_mac_dinh: true` + `mo_ta_ky`, câu trả lời BẮT BUỘC nêu kỳ ở câu đầu.
- `dang_ton`: chỉ NV đang làm việc (`working`); bỏ cặp meeting / phiếu công tác có `start` > hôm nay.
- Top mặc định 10, tối đa 20 (`ListLimit`); hoà ⇒ `qua_han` giảm dần rồi tên tăng dần.
- Mô tả công cụ ≤ 1000 ký tự (`desc.php`).
- Không đổi hành vi báo cáo: `collect()` mặc định y như cũ; toàn bộ test `EmployeeWork*` phải xanh.

## Review Focus

1. Trạng thái `NULL` / lạ: báo cáo xếp vào TODO ⇒ `openOnly` phải GIỮ (lọc bằng `whereNotIn(done+stopped) OR status IS NULL`, không dùng `whereIn(todo+doing)`). Test ở Task 1.
2. Người có quyền cấp Bộ phận hỏi "phòng tôi": thu hẹp về bộ phận, cờ `thu_ve_bo_phan: true`. Test ở Task 2.
3. Một người nêu tên NGOÀI phạm vi quyền ⇒ denied, không lộ số (kể cả 0). Test ở Task 2.
4. `thu_tu=it_nhat` phải có người 0 việc (danh mục NV trong phạm vi, không suy từ cặp). Test ở Task 3.
5. Phạm vi lớn: công ty 1 (~1.000 NV) chế độ `dang_ton` chạy < 3 giây và không N+1 (đếm query). Test ở Task 3.

---

### Task 1: Bộ gom — chế độ "chỉ việc chưa xong" + mở `allowedEmployeeIds`

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/EmployeeWorkPerformance/WorkAssignmentCollector.php` (`collect()` dòng 122, 5 hàm `from*`)
- Modify: `hrm-api/Modules/Assign/Services/Report/EmployeeWorkPerformanceService.php:88` (`private` → `public`, thêm docblock "Agent dùng chung")
- Test: `hrm-api/tests/Feature/EmployeeWorkPerformance/OpenOnlyCollectTest.php`

**Interfaces:**
- Produces: `WorkAssignmentCollector::collect(Request $request, array $empIds, Carbon $from = null, Carbon $to = null, bool $openOnly = false): array` · `EmployeeWorkPerformanceService::allowedEmployeeIds(Request $request): array` (đọc `company_id`, `department_id`, `part_id`, `employee_id`).

- [x] **Step 1: Viết test fail** — `OpenOnlyCollectTest` (DatabaseTransactions, NV 13, `Carbon::setTestNow('2031-03-15')`, chèn fixture 2031 cho 1 NV: task DONE, task CANCELLED, task IN_PROGRESS hạn 2031-03-01, task status NULL hạn 2031-03-20, meeting HUY):
  - `test_mac_dinh_khong_doi`: `collect(..., from 2031-03-01, to 2031-03-31)` = đúng 5 cặp như trước (đếm theo bucket: done 1, cancel 2, late 1, doing 1).
  - `test_open_only_bo_done_va_stopped`: cùng kỳ + `openOnly=true` ⇒ chỉ còn 2 cặp (late 1, doing 1), cặp status NULL có mặt.
  - `test_open_only_ky_rong`: `from 2000-01-01`, `to 2100-12-31`, `openOnly=true` ⇒ có task IN_PROGRESS hạn 2031-03-01 (`late`).
- [x] **Step 2:** `php -d memory_limit=1G vendor/bin/phpunit tests/Feature/EmployeeWorkPerformance/OpenOnlyCollectTest.php` ⇒ FAIL (tham số chưa có).
- [x] **Step 3:** Thêm `$openOnly` truyền xuống 5 hàm `from*`; khi `true` mỗi query thêm `where(fn($q) => $q->whereNotIn('status', WorkItemStatusGroup::statusesOf($helperType, [DONE, STOPPED]))->orWhereNull('status'))` với `$helperType` = khoá helper (`meeting/task/issue/assign_business/assign_job`). Đổi `allowedEmployeeIds` sang `public`.
- [x] **Step 4:** Chạy test mới ⇒ PASS; chạy `tests/Unit/EmployeeWork*` + `tests/Feature/EmployeeWorkPerformance` ⇒ toàn bộ PASS.
- [x] **Step 5:** Dừng ở đây, KHÔNG commit (user tự báo commit) — chỉ đánh dấu task xong trong plan.

### Task 2: `WorkByEmployeeScope` — quyền, phạm vi NV, kỳ

**Files:**
- Create: `hrm-api/Modules/Agent/Support/WorkByEmployeeScope.php`
- Test: `hrm-api/Modules/Agent/Tests/Feature/Tools/CongViecTheoNhanVienScopeTest.php` (khuôn `TongHopGiaiPhapScopeTest`: `actAs()`, `grant()` tạm trong transaction; NV 13 scope 3, 157 quản lý phòng 52, 179 phòng 52, 1345 không quyền)

**Interfaces:**
- Produces:
  - `const CODE = 'assign.bao_cao_ke_hoach_ket_qua_lam_viec.view'`, `const NAME = 'Xem báo cáo kế hoạch & kết quả làm việc'`, `const LOAI = ['nhiem_vu'=>'task','van_de'=>'issue','meeting'=>'meeting','phieu_cong_tac'=>'trip','phieu_giao_viec'=>'job']`
  - `static permissionNeed(array $input): ?PermissionNeed`
  - `static employeeIds(array $input): array` → `['ids'=>int[], 'pham_vi_text'=>string, 'thu_ve_bo_phan'=>bool]` (gọi `allowedEmployeeIds` với Request dựng tay; `toi` ⇒ `[auth employee id]`)
  - `static period(array $input): array` → `['che_do'=>'ky'|'dang_ton', 'from'=>Carbon, 'to'=>Carbon, 'ky_mac_dinh'=>bool, 'mo_ta_ky'=>string]` (`dang_ton` ⇒ from 2000-01-01, to 2100-12-31; mô tả "toàn bộ việc đang tồn tới hôm nay (dd/mm/YYYY)"; tháng mặc định ⇒ "tháng mm/YYYY (chưa nêu kỳ nên lấy tháng này)")

- [x] **Step 1: Viết test fail:**
  - `test_hang_so`: CODE/NAME khớp bảng `permissions`.
  - `test_toi_khong_can_quyen`: 1345, `pham_vi=toi` ⇒ `permissionNeed` null, ids = [1345].
  - `test_cong_ty_can_cap_cong_ty`: 1345 ⇒ PermissionNeed scope 3; 157 grant 2 ⇒ PermissionNeed; 13 ⇒ null.
  - `test_phong_ngoai_quan_ly_bi_chan`: 157 grant 2, `phong_ban_id` = phòng khác 52 ⇒ PermissionNeed.
  - `test_cap_bo_phan_thu_ve_bo_phan`: NV đầu tiên có bản ghi quản lý bộ phận (bảng quản lý bộ phận mà `listManagePartIds()` đọc), grant 1 (bộ phận), `pham_vi=phong` ⇒ null, `thu_ve_bo_phan` true, ids ⊆ NV bộ phận 179 quản lý.
  - `test_nguoi_ngoai_pham_vi_bi_chan`: 157 grant 2, `pham_vi=nguoi`, `nhan_vien_ids=[NV phòng khác]` ⇒ PermissionNeed (genericDenied).
  - `test_ky`: có tu/den ⇒ `ky`, `ky_mac_dinh` false; không có + `xep_theo=qua_han` ⇒ `dang_ton` true; không có + `xep_theo=hoan_thanh` ⇒ tháng này, `ky_mac_dinh` true, `mo_ta_ky` chứa "chưa nêu kỳ".
- [x] **Step 2:** `php -d memory_limit=1G vendor/bin/phpunit Modules/Agent/Tests/Feature/Tools/CongViecTheoNhanVienScopeTest.php` ⇒ FAIL.
- [x] **Step 3:** Viết `WorkByEmployeeScope` — câu từ chối theo khuôn `XepHangHoanThanhTool::permissionNeed()` (gợi ý hỏi phạm vi hẹp hơn).
- [x] **Step 4:** Chạy test ⇒ PASS.
- [x] **Step 5:** Dừng ở đây, KHÔNG commit (user tự báo commit) — chỉ đánh dấu task xong trong plan.

### Task 3: `WorkByEmployee` — đếm theo người, hoàn thành trễ, xếp hạng

**Files:**
- Create: `hrm-api/Modules/Agent/Support/WorkByEmployee.php`
- Test: `hrm-api/Modules/Agent/Tests/Feature/Tools/CongViecTheoNhanVienStatsTest.php`

**Interfaces:**
- Consumes: Task 1 `collect(..., $openOnly)`, Task 2 `employeeIds()` / `period()`.
- Produces:
  - `static rows(array $empIds, array $period, array $loai): array` → mỗi NV `['nhan_vien_id','ten','phong','bo_phan','tong','dang_lam','qua_han','hoan_thanh','hoan_thanh_tre','tre_han','dung_huy','theo_loai'=>[loai=>['tong','dang_lam','qua_han','hoan_thanh']]]`, gồm cả NV 0 việc (lấy từ `employeeProfiles()`); `dang_ton` ⇒ bỏ NV không `working`, bỏ cặp meeting/trip có `start` > hôm nay.
  - `static rank(array $rows, string $xepTheo, string $thuTu, int $n): array` → `['items'=>…, 'so_nguoi_trong_pham_vi', 'so_nguoi_co_viec', 'so_nguoi_co_qua_han']` (`nhieu_nhat` bỏ dòng có chỉ số = 0; `it_nhat` giữ).
  - `static pairsOf(int $empId, array $period, array $loai, ?string $nhom): array` (cặp cho chế độ chi tiết; `$nhom` ∈ qua_han|dang_lam|hoan_thanh|tre_han|null).

- [x] **Step 1: Viết test fail** (`setTestNow('2031-03-15')`, fixture 2031 cho 3 NV cùng phòng 52):
  - `test_dem_theo_nguoi_khop_bao_cao`: kỳ 2031-03 ⇒ `rows()` từng NV == `WorkMetrics::of(cặp của NV, false)` (done/doing/late/cancel).
  - `test_hoan_thanh_tre`: task DONE `submitted_at` 2031-03-11 hạn 2031-03-10 ⇒ `hoan_thanh_tre` 1; task DONE đúng hạn ⇒ 0; issue resolved sau hạn ⇒ 1; meeting HOAN_THANH ⇒ không tính.
  - `test_dang_ton_bo_lich_tuong_lai_va_nguoi_nghi`: meeting start 2031-03-20 không vào; NV `status != 1` có task tồn không có dòng.
  - `test_rank_tie_break`: 2 NV cùng `dang_lam` ⇒ NV nhiều `qua_han` hơn đứng trước; bằng nữa ⇒ theo tên.
  - `test_it_nhat_co_nguoi_0_viec`: `thu_tu=it_nhat` ⇒ có dòng `tong` 0.
  - `test_hieu_nang_cong_ty`: NV 13, công ty 1, `dang_ton`, `DB::enableQueryLog()` ⇒ < 25 query, < 3 giây.
- [x] **Step 2:** Chạy test ⇒ FAIL.
- [x] **Step 3:** Viết `WorkByEmployee` — đếm trong bộ nhớ trên cặp; `hoan_thanh_tre`: 1 query `tasks` + 1 query `issues` theo `doc_id` của cặp `done` (không query trong vòng lặp).
- [x] **Step 4:** Chạy test ⇒ PASS.
- [x] **Step 5:** Dừng ở đây, KHÔNG commit (user tự báo commit) — chỉ đánh dấu task xong trong plan.

### Task 4: Công cụ `cong_viec_theo_nhan_vien` + đăng ký + prompt

**Files:**
- Create: `hrm-api/Modules/Agent/Tools/CongViecTheoNhanVienTool.php`
- Modify: `hrm-api/Modules/Agent/Tools/AgentToolRegistry.php` (thêm cạnh `XepHangHoanThanhTool::class`)
- Modify: mô tả `ThongKeQuaHanTheoPhongTool`, `ViecCuaPhongTool`, `ViecQuaHanTool`, `ViecCuaNhanVienTool` (thêm "Not for per-person counts/rankings (cong_viec_theo_nhan_vien)")
- Modify: `hrm-api/Modules/Agent/Services/AgentPrompt.php` (luật 21 sau luật 20, dòng ~41)
- Test: `hrm-api/Modules/Agent/Tests/Feature/Tools/CongViecTheoNhanVienTest.php`

**Interfaces:**
- Consumes: Task 2, Task 3.
- Produces: tên `cong_viec_theo_nhan_vien`; input `pham_vi` (toi|nguoi|phong|cong_ty), `nhan_vien_ids` int[], `phong_ban_id`, `xep_theo` (qua_han|dang_lam|chua_xong|hoan_thanh|tre_han|tong), `thu_tu` (nhieu_nhat|it_nhat), `loai` string[], `chi_tiet` bool, `so_luong`, `tu_ngay`, `den_ngay`.
  - `data`: `che_do`, `ky_mac_dinh`, `mo_ta_ky`, `pham_vi_text`, `thu_ve_bo_phan`, `xep_hang`|`nguoi`|`viec`, các `so_nguoi_*`, `ghi_chu_tre_han` (khi `xep_theo=tre_han` hoặc hỏi người: "Hoàn thành trễ chỉ tính Nhiệm vụ và Vấn đề (3 loại còn lại không lưu thời điểm hoàn thành)").
  - `block` xếp hạng / người: `['type'=>'work_rank','metric'=>xep_theo|null,'items'=>[{id,label,department,value,qua_han,ask}],'source'=>"Kế hoạch & kết quả làm việc · <pham_vi_text> · <mo_ta_ky>",'link_more'=>'/assign/report/employee-work-performance']`; `ask` = "Việc <nhóm> của <tên>" (nhóm theo `xep_theo`).
  - `block` chi tiết: `type 'tasks'` dòng dựng bằng `ViecTongHopCuaToiTool::card(...)` với `type` FE: task→`task`, issue→`issue`, meeting→`meeting`, trip→`assign_business`, job→`assign_job`; tối đa 20 + `con_lai`.
  - `matrixRow()` = `['label'=>'Công việc theo nhân viên','need'=>['code'=>CODE,'scope'=>1]]`.

- [x] **Step 1: Viết test fail:**
  - `test_mo_ta_duoi_1000`: `mb_strlen(description) <= 1000`; 4 mô tả công cụ cũ chứa `cong_viec_theo_nhan_vien`.
  - `test_xep_hang_qua_han_cong_ty`: NV 13, không kỳ ⇒ `che_do` dang_ton, `ky_mac_dinh` true, `mo_ta_ky` chứa "đang tồn", `block.type` work_rank, ≤ 10 dòng, `value` giảm dần.
  - `test_top_n`: `so_luong` 25 ⇒ cắt 20.
  - `test_mot_loai_meeting_thang_nay`: `xep_theo=tong`, `loai=['meeting']`, không kỳ ⇒ kỳ tháng này, `mo_ta_ky` chứa "chưa nêu kỳ".
  - `test_so_sanh_hai_nguoi`: `pham_vi=nguoi`, 2 id ⇒ `data.nguoi` 2 dòng, đủ 4 nhóm + `theo_loai`.
  - `test_chi_tiet_qua_han`: `chi_tiet=true`, 1 id, `xep_theo=qua_han` ⇒ block `tasks`, mọi dòng `deadline_state_text` "Quá hạn", `type` thuộc 5 khoá FE.
  - `test_khong_quyen`: 1345 `pham_vi=cong_ty` ⇒ `ToolResult` denied.
  - `test_prompt_co_luat_21`: `AgentPrompt` chứa "cong_viec_theo_nhan_vien" và "nêu rõ kỳ".
- [x] **Step 2:** `php -d memory_limit=1G vendor/bin/phpunit Modules/Agent/Tests/Feature/Tools/CongViecTheoNhanVienTest.php` ⇒ FAIL.
- [x] **Step 3:** Viết công cụ + đăng ký + sửa 4 mô tả + luật 21. Luật 21 gồm: ai / người nào nhiều (ít) việc quá hạn / đang làm / hoàn thành / trễ / họp / công tác nhất, top N người, phòng X bao nhiêu người có việc quá hạn, anh X đang có bao nhiêu việc, so sánh người ⇒ `cong_viec_theo_nhan_vien` (KHÔNG đếm tay từ danh sách việc); người nêu tên ⇒ `tim_nhan_vien` trước; câu ĐẦU nêu `mo_ta_ky` (nhất là khi `ky_mac_dinh`) và `pham_vi_text`; `thu_ve_bo_phan` ⇒ nói rõ "trong bộ phận anh/chị quản lý"; có `ghi_chu_tre_han` thì nêu; xếp hạng ⇒ 1–2 câu nêu người đứng đầu + số, chi tiết trong thẻ; quá hạn lớn do meeting ⇒ nêu số meeting riêng. Ranh giới: so sánh PHÒNG ⇒ `thong_ke_qua_han_theo_phong`; TỈ LỆ đúng hạn ⇒ `xep_hang_hoan_thanh`; "nhiệm vụ của anh X" ⇒ `viec_cua_nhan_vien`.
- [x] **Step 4:** Chạy test mới ⇒ PASS; chạy cả bộ `Modules/Agent/Tests` (413 + mới) ⇒ toàn bộ PASS; `desc.php CongViecTheoNhanVienTool ThongKeQuaHanTheoPhongTool ViecCuaPhongTool ViecQuaHanTool ViecCuaNhanVienTool` ⇒ mọi mô tả ≤ 1000.
- [x] **Step 5:** Dừng ở đây, KHÔNG commit (user tự báo commit) — chỉ đánh dấu task xong trong plan.

### Task 5: Thẻ `work_rank` (hrm-client)

**Files:**
- Modify: `hrm-client/components/agent/AgentResultBlock.vue` (nhánh mới sau nhánh `rank` dòng ~112; style cạnh `.agr-rank`)

**Interfaces:**
- Consumes: block `work_rank` của Task 4.
- Produces: mỗi dòng `data-testid="agent-work-rank-row"`; bấm dòng ⇒ `$emit('pick', { kind: 'employee', id: x.id, label: x.ask })` (dùng lại luồng `pick` có sẵn: `AgentWorkspace.pick()` gửi câu `label` kèm `pick_employee_id`), tắt khi `pickDisabled`. Thẻ `rank` cũ KHÔNG đổi.

- [x] **Step 1:** Vẽ dòng: hạng · avatar · tên (dòng phụ phòng) · số `value` + đơn vị theo `metric` · "n quá hạn" đỏ khi `qua_han > 0` (ẩn khi `metric = qua_han`); link "Mở báo cáo" từ `link_more`; `source` như các thẻ khác.
- [x] **Step 2: Kiểm Playwright** :3070 (tài khoản namdangit, NV 13) hỏi "Top 10 người có nhiều việc quá hạn nhất": đo DOM — số `agent-work-rank-row` = số dòng trong `data`, không chồng lấn (bounding box từng dòng không giao nhau), `scrollWidth <= clientWidth` của thẻ, chữ đỏ quá hạn `getComputedStyle().color`; bấm 1 dòng ⇒ lượt hỏi mới có câu "Việc quá hạn của …" và thẻ `tasks`. Hỏi 1 câu ra thẻ `rank` cũ ("Ai hoàn thành đúng hạn nhiều nhất tháng này") ⇒ vẫn hiện như trước.
- [x] **Step 3:** Dừng ở đây, KHÔNG commit (user tự báo commit) — chỉ đánh dấu task xong trong plan.

### Task 6: Hỏi thật + đối chiếu số + ghi chép

**Files:**
- Create: `HRM/.plans/agent-chat/agent/scripts/work_parity.php` (đối chiếu: với NV 13, kỳ tháng 10/2026, mỗi NV `WorkByEmployee::rows()` == dòng NV trên `EmployeeWorkPerformanceService::getData()` cùng kỳ)
- Modify: `HRM/.plans/agent-chat/agent/scripts/README.md`, plan này, memory `agent-chat-trang-thai.md`

- [x] **Step 1:** `php -d memory_limit=1G <scripts>/work_parity.php` ⇒ 0 lệch.
- [x] **Step 2:** `hoi_that.php` với NV 13 đủ bộ câu spec §2.1 + 3 câu ban đầu ⇒ mỗi câu gọi `cong_viec_theo_nhan_vien`, câu đầu nêu kỳ, không đếm tay; ghi kết quả từng câu vào plan.
- [x] **Step 3:** Ghi checkpoint cuối plan + memory (chưa commit/push — user tự báo).

## Checkpoint
- 19/11: plan viết xong, chờ user duyệt + cho phép code (phạm vi ở trên).
- 19/11 CODE XONG, CHƯA COMMIT (nhánh `gop_db-agent-cong-viec-theo-nhan-vien` cả 2 repo, base api 729a7ced6 · client b37aa3b41, đã bỏ upstream). Bộ Agent PHPUnit 439/439 (chạy 2G — 1G hết bộ nhớ cả trên origin/gop_db gốc); OpenOnlyCollectTest 3/3 + unit EmployeeWork* 45/45 (feature EmployeeWorkPerformance 16 lỗi FK fixture có sẵn). Đối chiếu báo cáo tháng 10 + 11: 408 NV, lệch 0. Playwright :3070 đo thẻ work_rank đạt. Review opus: 2 Important + 2 Minor nâng hạng đã sửa có test. Chi tiết + rulings: `ledger.md`.
- CHỜ USER: (1) quyết "đang tồn" bị phiếu công tác cũ chi phối (7,738 phiếu qua ngày chưa duyệt KQ); (2) commit / merge / deploy.
- 19/11 (sau): user chốt TẠM LOẠI phiếu công tác khỏi công cụ (WorkByEmployeeScope::LOAI còn 4 loại, có ghi_chu_loai). Bộ Agent chạy lại xanh, đối chiếu báo cáo (bỏ loại phiếu công tác) lệch 0. Vẫn CHƯA COMMIT.
- 19/11 ĐÃ DEPLOY PROD TPE: commit api 4c34c40e6 · client 303e02284 (nhánh gop_db-agent-cong-viec-theo-nhan-vien, đã push) ⇒ merge gop_db api a519d1282 · client fb4f109b4 (bộ Agent 440/440 trên bản merge) ⇒ build_tpe.sh EXIT 0, Nothing to migrate, prod = a519d1282 / fb4f109b4, site 200. Log có "pm2 Unknown command argument" của script (lần gọi sai trước lệnh restart đúng), client tpe vẫn online.
