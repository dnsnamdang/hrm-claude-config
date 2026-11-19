# Agent `phat_trien_thi_truong` — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.
> 17/11 user "làm 1" = cho phép Task 1–4 (api), cách subagent-driven. Task 6 FE / Task 7 hỏi thật phải hỏi lại.

**Goal:** Agent trả lời câu hỏi thị trường / kế hoạch đi khách hàng bằng đúng số và đúng khuôn của báo cáo "Phát triển thị trường - Khách hàng".

**Architecture:** Công cụ mới `phat_trien_thi_truong` (hrm-api `Modules/Agent`) gọi thẳng `CustomerMarketDevelopmentService::getData($req, false)` / `getDrillPage($req)`. Ánh xạ tham số + guard quyền tách ra `Support/MarketDevScope.php`; làm phẳng cây ở `Support/MarketDevTree.php`. FE thêm 2 loại thẻ `market_tree`, `market_list` trong `AgentResultBlock.vue`.

**Tech Stack:** PHP 7.4/8.1 · Laravel 8 · PHPUnit · Nuxt 2 / Vue 2 · Playwright (Node 20).

**Spec:** `docs/superpowers/specs/agent-chat/2026-11-17-agent-phat-trien-thi-truong-design.md` (tóm tắt `design.md` cùng folder).

## Global Constraints

- Nhánh mới tách từ `origin/gop_db`: api + client `gop_db-agent-phat-trien-thi-truong`, worktree `websites/wt-tpe-agent` (kiểm `git status` sạch trước khi đổi nhánh; :8070/:3070 chạy theo nhánh). Không migration, không quyền mới.
- KHÔNG sửa `CustomerMarketDevelopmentService` (chỉ gọi hàm public). Cần thêm hàm ⇒ hỏi user (hàm dùng chung).
- Mã quyền: `presale.bao_cao_phat_trien_thi_truong_khach_hang.view`, tên hiển thị "Xem báo cáo phát triển thị trường - khách hàng".
- Mô tả công cụ (definition description) ≤ 600 ký tự, tiếng Anh; tham số tiếng Việt không dấu.
- Số theo chuẩn `1,234,567.5`; không nêu SĐT khách.
- PHPUnit: `/opt/homebrew/opt/php@8.1/bin/php -d memory_limit=3G vendor/bin/phpunit Modules/Agent/Tests`. Chép `agent-eval-*.csv` ra ngoài trước khi chạy (AgentEvalCommandTest xoá chúng).
- Dữ liệu thử trong test: meeting kỳ 03/2031 (ngoài dữ liệu thật), `DatabaseTransactions`, mã `AGPT-*`.
- E2E Agent cần :8070 `AGENT_FAKE=1` ⇒ HỎI user trước khi restart :8070.

## Review Focus

1. Người KHÔNG có quyền hỏi "phòng X" ⇒ phải denied, không được ra số meeting của chính họ (service tự thu về mức self). → Task 1 ca `phong_khong_quyen_bi_chan`.
2. Người chỉ quản lý BỘ PHẬN hỏi "phòng tôi" ⇒ tự thu về bộ phận, `data.thu_ve_bo_phan=true`. → Task 1 ca `quan_ly_bo_phan_thu_ve_bo_phan`.
3. Phòng không chia bộ phận ⇒ service bỏ cấp Bộ phận ⇒ dòng cây có `loai` đúng, `so_cap` vẫn đếm đúng. → Task 2 ca `phong_khong_chia_bo_phan`.
4. Kỳ tương lai (`tuan_sau`) ⇒ HT / Huỷ / Nhu cầu = 0, kết quả không lỗi, kế hoạch vẫn đếm. → Task 2 ca `ky_tuong_lai`.
5. Tỉnh "chưa xác định" ⇒ lọc `__no_province__`; tên tỉnh không khớp ⇒ trả ok 0 dòng kèm `tinh_khong_khop`, không lỗi. → Task 1 ca `tinh_chua_xac_dinh_va_khong_khop`.

---

### Task 1: Ánh xạ tham số + guard quyền (`MarketDevScope`)

**Files:**
- Create: `hrm-api/Modules/Agent/Support/MarketDevScope.php`
- Test: `hrm-api/Modules/Agent/Tests/Feature/Tools/PhatTrienThiTruongTest.php`

**Interfaces:**
- Produces:
  - `MarketDevScope::CODE`, `MarketDevScope::NAME`
  - `MarketDevScope::check(array $input): ?PermissionNeed` — bảng §5.2 spec (toi · phong · cong_ty · tap_doan · bo_phan_id · nhan_vien_id).
  - `MarketDevScope::request(array $input): array{0: \Illuminate\Http\Request, 1: array $meta}` — `$meta` = `['pham_vi_text' => 'công ty TPE'|'toàn tập đoàn'|'phòng …'|'bộ phận …'|'của anh/chị', 'thu_ve_bo_phan' => bool, 'tinh_khong_khop' => bool]`.
  - Map: `tieu_chi` thi_truong/khach_hang/phong_ban → `criteria` mk/cus/dp (mặc định `phong_ban` nếu có phong_ban_id/bo_phan_id/nhan_vien_id/pham_vi toi, ngược lại `thi_truong`); `ky` hom_nay/tuan_nay/tuan_sau/thang_nay/thang_sau/quy_nay/nam_nay → today/week/nextweek/month/nextmonth/quarter/year; `tu_ngay`/`den_ngay` → `custom`; `trang_thai` len_lich/chot_lich/hoan_thanh/huy → 1/2/3/4; `tinh` qua `MeetingMarketScope::matchProvinces` (chưa xác định ⇒ `__no_province__`; khớp nhiều tỉnh ⇒ lấy tỉnh đầu, khớp 0 ⇒ `province_id=-1` + `tinh_khong_khop`); `company_id` = `TaskScopeGuard::companyId()` trừ `tap_doan`; `toi` ⇒ `employee_id = auth()->id()`.
  - Guard bộ phận: scope ≥3 qua; scope 2 qua khi `part_id ∈ listManagePartIds()` hoặc phòng của bộ phận ∈ `listManageDepartmentIds()`; người scope 2 không quản lý phòng mình nhưng quản lý 1 bộ phận trong phòng ⇒ `pham_vi=phong` mặc định thu về bộ phận đó (`thu_ve_bo_phan=true`).

- [x] **Step 1: Viết test quyền + ánh xạ (đỏ)** — dùng khuôn `MeetingListToolsTest` (`actAs`, `RequestCache::flush`, `PermissionChecker::flush`). Probe trước bằng script bootstrap ai có scope 4/3/2/không có mã này trên `db_gop_6_11`, ghi vào docblock; thiếu người cho ca nào ⇒ cấp role tạm (memory local-dev-duoc-cap-quyen-de-test), gỡ sau.
  - `toi_khong_can_quyen`: NV không mã ⇒ `check(['pham_vi'=>'toi'])` null; request có `employee_id` = mình.
  - `phong_khong_quyen_bi_chan`: NV không mã, `pham_vi=phong` ⇒ PermissionNeed `code === CODE`.
  - `phong_quan_ly_scope2_qua` / `phong_khac_scope2_bi_chan` (scopeNeeded 3).
  - `cong_ty_can_scope3`, `tap_doan_can_scope4`; `tap_doan` ⇒ request KHÔNG có `company_id`; mặc định có `company_id` = công ty đang làm.
  - `quan_ly_bo_phan_thu_ve_bo_phan`: role tạm scope 2 + quản lý 1 bộ phận ⇒ request có `part_id`, `meta.thu_ve_bo_phan=true`.
  - `nhan_vien_phong_khac_bi_chan`, `nhan_vien_khac_cong_ty_chan_chung` (`generic=true`).
  - `tinh_chua_xac_dinh_va_khong_khop`; `ky_va_khoang_ngay` (tuan_sau ⇒ nextweek; tu_ngay+den_ngay ⇒ custom).
- [x] **Step 2:** chạy `--filter PhatTrienThiTruongTest` ⇒ FAIL (class chưa có).
- [x] **Step 3:** viết `MarketDevScope` theo Interfaces; tái dùng `PresaleScopeGuard::checkDepartment/checkCompany/genericDenied`.
- [x] **Step 4:** chạy lại ⇒ PASS.
- [x] **Step 5:** commit `feat(agent): MarketDevScope — ánh xạ tham số + quyền báo cáo phát triển thị trường`.

### Task 2: Công cụ — chế độ tổng hợp (cây)

**Files:**
- Create: `hrm-api/Modules/Agent/Support/MarketDevTree.php`, `hrm-api/Modules/Agent/Tools/PhatTrienThiTruongTool.php`
- Modify: `hrm-api/Modules/Agent/Tools/AgentToolRegistry.php` (thêm vào `DEFAULT_TOOLS` ngay sau `MeetingTheoThiTruongTool::class`), `PayrollToolsTest.php:170,182`, `PersonalToolsTest.php:241` (+1: 45→46, 47→48, 47→48)
- Test: `PhatTrienThiTruongTest.php`

**Interfaces:**
- Consumes: `MarketDevScope::check`, `MarketDevScope::request`.
- Produces:
  - `MarketDevTree::flatten(array $tree, ?int $soCap, int $max = 60): array{rows: array, da_cat: bool, so_dong_cap1: int}` — mỗi dòng `['cap'=>int,'loai'=>'thi_truong|khach_hang|phong_ban|bo_phan|nhan_vien','ten'=>string,'key'=>string] + metrics` (khoá metrics giữ nguyên tên service: plan, completed, cancelled, completion_rate, customers, new_customers, demand, investment). Cấp gốc chỉ 1 dòng ⇒ không tính vào `so_cap`. `so_cap=null` ⇒ bung tới hết cấp `nhan_vien`, riêng `criteria=dp` + có lọc phòng/bộ phận/NV ⇒ bung thêm cấp thị trường. Vượt `$max` ⇒ cắt từ cấp sâu nhất trước, `da_cat=true`.
  - `PhatTrienThiTruongTool::name() === 'phat_trien_thi_truong'`; `run()` (không `chi_tieu`) ⇒ `ToolResult::ok(['ky'=>['from','to'],'tieu_chi','pham_vi'=>meta.pham_vi_text,'tong'=>total,'tong_hop'=>summary,'cay'=>rows,'so_dong_cap1','da_cat', 'thu_ve_bo_phan'?, 'ghi_chu'=>[…]], count(rows), ['type'=>'market_tree','summary'=>…,'items'=>rows,'criteria_head'=>…,'link'=>'/assign/report/customer-market-development','source'=>…])`.
  - `ghi_chu` cố định: "KH mới = khách hàng TẠO trong kỳ, tính cho người tạo, không theo lọc loại/trạng thái" · "Số lượng KH đếm khác nhau, dòng cha có thể nhỏ hơn tổng dòng con" · "Nhu cầu = số nhu cầu trong biên bản meeting Hoàn thành".
  - `matrixRow()` ⇒ `['label'=>'Phát triển thị trường - khách hàng (phòng / công ty)','need'=>['code'=>CODE,'scope'=>2]]`.

- [x] **Step 1: Test (đỏ)** — seed 6 meeting 03/2031 (2 tỉnh, 2 NV, 1 huỷ tự động, 1 HT có nhu cầu) + 1 KH tạo trong kỳ:
  - `khop_so_bao_cao`: với 3 `tieu_chi` × (`tu_ngay/den_ngay` 03/2031), `data.tong == (new CustomerMarketDevelopmentService)->getData(<cùng Request>, false)['total']` và mỗi dòng cấp 1 khớp metrics node tương ứng.
  - `cap_goc_mot_dong_khong_tinh`: `tieu_chi=phong_ban`+`phong_ban_id` ⇒ có dòng `loai=nhan_vien` và `loai=thi_truong`.
  - `phong_khong_chia_bo_phan`: dòng dưới phòng có `loai=nhan_vien` (không có `bo_phan`).
  - `ky_tuong_lai`: `ky=tuan_sau` với meeting tuần sau ⇒ `tong.plan>0`, `completed=0`.
  - `cat_60_dong`: `MarketDevTree::flatten` với cây giả 30×5 ⇒ 60 dòng, `da_cat=true`, đủ 30 dòng cấp 1 nếu ≤60.
  - `denied_khong_goi_service`: NV không mã hỏi phòng ⇒ outcome denied, `queriesOn('meetings')` rỗng.
  - Sửa 3 số đếm registry.
- [x] **Step 2:** chạy ⇒ FAIL.
- [x] **Step 3:** viết `MarketDevTree` + `PhatTrienThiTruongTool` (definition: description ≤600 ký tự nêu "customer meetings = market development plan; for 'kế hoạch đi thị trường/đi khách hàng' of a person/department; follows report criteria; chi_tieu ⇒ detail list"; schema theo bảng §5.1 + `ListLimit::schema(50)`); đăng ký registry.
- [x] **Step 4:** chạy `PhatTrienThiTruongTest` + `PayrollToolsTest` + `PersonalToolsTest` ⇒ PASS; test độ dài mô tả có sẵn ⇒ PASS.
- [x] **Step 5:** commit `feat(agent): công cụ phat_trien_thi_truong — cây theo tiêu chí báo cáo`.

### Task 3: Công cụ — chế độ chi tiết

**Files:**
- Modify: `PhatTrienThiTruongTool.php`
- Test: `PhatTrienThiTruongTest.php`

**Interfaces:**
- Produces: `run()` có `chi_tieu` ⇒ `getDrillPage(<request + metric + key=ALL + per_page=ListLimit::of($input,50,20) + page=1>)`. Map `chi_tieu`: ke_hoach→plan, hoan_thanh→completed, huy→cancelled, huy_qua_han→cancelled_auto, huy_co_ly_do→cancelled_manual, khach_hang→customers, kh_moi→new, nhu_cau→demand, lap_truoc_ky→pre, lap_trong_ky→inp.
  - data: `['chi_tieu','tong'=>pagination.total,'dong'=>[…]]`; cột theo §3 spec (popup): meeting ⇒ code, name, start_date, type, status_name, province_name, department_name, part_name, host_name, customer_name (+ cancel_reason_name, cancel_note, is_auto_cancelled khi huy*); khach_hang ⇒ customer_name, province_name, host_name, meetings, completed_count, cancelled_count, last_date; kh_moi ⇒ code, name, province_name, host_name, created_at; nhu_cau ⇒ demand_names, investment, name, start_date, customer_name, host_name.
  - block: meeting-type ⇒ `['type'=>'meetings','items'=>…]` theo đúng khuôn `MeetingListRows` (để có link panel), thêm `reason` khi huy*; còn lại ⇒ `['type'=>'market_list','kind'=>'customers|new|demand','columns'=>[['id','label']…],'items'=>…,'link'=>…]`.

- [x] **Step 1: Test (đỏ)**: `chi_tiet_huy_co_ly_do` (đúng dòng, có reason), `chi_tiet_khach_hang_dem_khac_nhau` (tong == metrics.customers), `chi_tiet_kh_moi`, `chi_tiet_nhu_cau_moi_dong_mot_nhu_cau` (tong == metrics.demand), `so_luong_cat_dong` (`so_luong=2` ⇒ 2 dòng, `tong` vẫn đủ).
- [x] **Step 2:** FAIL. **Step 3:** cài đặt. **Step 4:** PASS + toàn bộ `Modules/Agent/Tests` (ghi số pass/fail; 3 ca phòng họp đỏ có sẵn do DB local).
- [x] **Step 5:** commit `feat(agent): phat_trien_thi_truong chế độ chi tiết theo chỉ tiêu`.

### Task 4: Định tuyến — prompt luật 15 + mô tả công cụ liên quan

**Files:**
- Modify: `hrm-api/Modules/Agent/Services/AgentPrompt.php` (thêm luật 15 sau luật 14), `Tools/MeetingTheoThiTruongTool.php`, `Tools/MeetingCuaPhongTool.php`, `Tools/LichMeetingTool.php` (description: "market / customer-visit plan questions ⇒ phat_trien_thi_truong"), `Tests/fixtures/eval/questions.json`
- Test: test prompt có sẵn trong `AgentRunnerTest` (nếu kiểm nguyên văn system) + `AgentEvalCommandTest` (≥75 câu)

- [x] **Step 1:** luật 15 (nội dung §5.5 spec, ngắn): "kế hoạch đi thị trường / đi khách hàng / phát triển thị trường của NV|phòng" ⇒ phat_trien_thi_truong tieu_chi=phong_ban; tỉnh là chủ thể ⇒ thi_truong; KH là chủ thể ⇒ khach_hang; tuần sau/tháng sau ⇒ ky; hỏi sâu 1 con số ⇒ chi_tieu, giữ lọc lượt trước; nêu phạm vi trong câu dẫn; `thu_ve_bo_phan` ⇒ nói rõ; `da_cat` ⇒ mời mở báo cáo; ==…== cho huỷ quá hạn.
- [x] **Step 2:** sửa 3 mô tả, giữ ≤600 ký tự (test độ dài PASS).
- [x] **Step 3:** thêm 8 câu eval `expect_tools: ["phat_trien_thi_truong"]` (kèm `tim_phong_ban`/`tim_nhan_vien` khi có tên): kế hoạch tuần sau phòng KDTM · kế hoạch tháng này của anh Nhân · thị trường Hà Nội tháng này · KH nào gặp nhiều nhất quý này · cuộc huỷ tháng này là cuộc nào · KH mới tháng này · nhu cầu thu thập tháng này · toàn tập đoàn tháng này; 5 câu cũ `meeting_theo_thi_truong` soát lại kỳ vọng (câu thống kê "tỉnh nào nhiều meeting nhất" ⇒ chuyển sang công cụ mới nếu luật 15 bao).
- [x] **Step 4:** PHPUnit Agent PASS (trừ 3 ca có sẵn).
- [x] **Step 5:** commit `feat(agent): luật 15 định tuyến câu hỏi thị trường + eval`.

### Task 5: Mockup thẻ `market_tree` / `market_list` (tài liệu, không phải source)

**Files:**
- Create: `.plans/agent-chat/agent/phat-trien-thi-truong/mockup.html`

- [x] **Step 1:** đo style thật của thẻ `bars`/`meetings` trong ngăn Agent (getComputedStyle trên :3070) + bảng `rsum-tb` của báo cáo; mockup 3 thẻ: cây tiêu chí `phong_ban` (Phòng ▸ BP ▸ NV ▸ Thị trường), `thi_truong`, chi tiết `khach_hang`; ở 2 bề rộng: ngăn Agent và trang `/agent`. Cột hiển thị: Meeting · HT · Huỷ · Tỷ lệ · KH · KH mới · Nhu cầu · Giá trị.
- [x] **Step 2:** user chốt 17/11 phương án **B** (5 cột Meeting · HT · Huỷ · KH · KH mới · Nhu cầu; Tỷ lệ HT + Giá trị là dòng phụ dưới tên; không cuộn ngang).

### Task 6: FE thẻ kết quả

**Files:**
- Modify: `hrm-client/components/agent/AgentResultBlock.vue` (2 nhánh `v-else-if` mới sau `rank`; nhánh `meetings` thêm dòng lý do huỷ khi `m.reason`)
- Create (nếu khối dài > ~80 dòng): `hrm-client/components/agent/AgentMarketTree.vue`, `AgentMarketList.vue`
- Test: `e2e/tests/agent/agent-market.spec.ts` (mới) — chạy trên API `AGENT_FAKE=1` với kịch bản trả block giả

**Interfaces:**
- Consumes: block `market_tree` (`summary`, `items[{cap,loai,ten,key,plan,completed,cancelled,completion_rate,customers,new_customers,demand,investment}]`, `criteria_head`, `link`, `source`), `market_list` (`kind`, `columns`, `items`, `link`).

- [x] **Step 1:** e2e đỏ: thẻ `[data-testid=agent-market-tree]` có đúng số dòng, dòng cấp 2 thụt lề > cấp 1 (đo `getBoundingClientRect().left`), số định dạng `1,234,567`, link "Mở báo cáo" đúng href; `market_list` đúng cột theo `kind`; ngăn Agent không tràn ngang trang (scrollWidth của ngăn ≤ clientWidth, bảng tự cuộn trong khối).
- [x] **Step 2:** cài đặt theo mockup đã chốt; số dùng `toLocaleString('en-US')`; không `.text-muted`.
- [x] **Step 3:** Playwright đo DOM cả ngăn Agent và `/agent`; chạy toàn bộ `agent-chat` + `agent-chat-pin` + spec mới, đọc dòng tổng kết (serial ⇒ "did not run" ≠ passed).
- [x] **Step 4:** commit `feat(agent): thẻ market_tree / market_list`.

### Task 7: Kiểm thật + tài liệu

- [x] **Step 1:** Haiku thật local (script `agent/scripts/hoi_that`, NV 13 + 1 trưởng phòng scope 2 + 1 NV không quyền) cho 8 câu eval với kỳ tuỳ chọn có dữ liệu (≤ 06/11/2026); kiểm `agent_tool_calls.input` đúng `tieu_chi/ky/chi_tieu`; đối chiếu số với màn báo cáo cùng lọc (Playwright mở `/assign/report/customer-market-development`, đọc dòng TỔNG).
- [x] **Step 2:** `agent:eval --only=<8 câu mới + 5 câu cũ>` ⇒ đúng công cụ ≥ 12/13; ghi kết quả.
- [x] **Step 3:** cập nhật `agent/huong-dan-them-cong-cu.md` (nếu có mục danh sách công cụ), README §3b, STATUS checkpoint; ghi chú deploy: không migration, build client, `queue:restart` (build_tpe tự làm).

---

### Checkpoint — 17/11/2026 tối (Task 1–7 xong)
Vừa hoàn thành:
- api nhánh `gop_db-agent-phat-trien-thi-truong` (wt-tpe-agent/hrm-api) 84c8d11b4..8e9d017e8 (12 commit) · client cùng tên ab194e229 — CHƯA push.
- User chốt thêm 17/11: Tổng công ty hỏi sâu công ty khác (tim_* `toan_tap_doan`, chỉ scope 4); meeting chỉ ghi ngày, ngày không năm = năm nay; mockup B; P1 mặc định phạm vi rộng nhất; user tự cấp quyền báo cáo mới cho vai trò đang có quyền cũ.
- Kiểm: PhatTrienThiTruongTest 42/42; Agent PHPUnit 332 ca, 1 fail ngoài luồng (AgentQuotaServiceTest so float với chi tiêu tháng trên DB local). Haiku thật 16 lượt: số khớp màn báo cáo 9/9, eval 13/13 (trước đợt P1–P6). e2e agent-market 4/4; agent-chat + pin: 22 passed · 2 failed · 9 did not run — 2 ca đỏ do SPEC CŨ (pin:206 đọc title nhưng GĐ15 đổi sang v-b-tooltip; chat:976 tìm "Chỉnh sửa nhắc việc cá nhân", TodoFormModal nay "Chỉnh sửa nhắc việc").
- DB local db_gop_6_11: đã chạy 2 migration (notification_mutes, meeting_rooms.sort_order) — user cho phép.
Đang làm dở: —
Cập nhật 17/11 khuya: đã sửa 2 spec cũ (user cho phép) ⇒ e2e agent-chat + pin + market: 32 passed + 1 flaky (chat:797, qua khi thử lại), 0 failed. Eval Haiku thật sau P1–P6: 14/14 công cụ + kind, 669₫.
Bước tiếp theo: user báo push/merge gop_db + deploy TPE (api + client cùng lúc; không migration).
Blocked:

- **17/11/2026 — ĐÃ DEPLOY TPE** (api `b9faa6266` · client `fe8b42f97`; kèm #12217 của người khác + 2 migration self_notifications/personal_todos). Việc tay: cấp quyền "Xem báo cáo phát triển thị trường - khách hàng" cho các vai trò.
- 17/11 tối: câu #116 tốn 186₫ KHÔNG do công cụ — câu đầu mỗi lượt eval trả phí ghi cache prompt (~140₫); đổi thứ tự 219,116,116 ⇒ 219 = 185.8₫, 116 = 43.1 / 46.1₫. Dữ liệu công cụ ~11.5k ký tự (60 dòng cây), ngang các câu khác. Không cần sửa.
- 17/11 tối: ĐÃ cấp quyền "Xem báo cáo phát triển thị trường - khách hàng" trên prod (qua RoleManagementService::savePermissions, có lịch sử) cho 4 vai trò có quyền cũ mà thiếu quyền mới: TPE_Admin_TPE (Tổng công ty), TPE_Trưởng phòng KD DATKT, ETEK POWER_Trưởng phòng giá DATKT, ETEK POWER_Trưởng phòng kinh doanh (Phòng ban). Hỏi thử prod bằng namdangit "Kế hoạch đi thị trường tháng này thế nào?" ⇒ gọi phat_trien_thi_truong, ok, 743 cuộc / 491 xong / 66.1%, 187.6₫ (câu đầu, có phí ghi cache); lượt thử đã xoá.
- 17/11 tối: thử prod bằng NV 157 (vai trò TPE_Trưởng phòng KD DATKT, phạm vi Phòng ban, phòng 52): "Kế hoạch đi thị trường tháng này thế nào?" ⇒ chỉ số PHÒNG KD VẬT TƯ THIẾT BỊ BÔI TRƠN (29 cuộc / 21 xong / 72.4%), 35₫; "…của toàn công ty" ⇒ denied (pham_vi cong_ty), nói rõ thiếu quyền phạm vi Công ty + gợi ý xem phòng mình, 20.9₫. Lượt thử đã xoá.
