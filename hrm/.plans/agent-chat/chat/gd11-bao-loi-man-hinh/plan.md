# GĐ11 Báo lỗi màn hình — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.
> **Chưa được phép code.** Trước Task 1 phải hỏi user riêng: repo · nhánh · migration · gói npm `html2canvas` (CLAUDE.md gốc "Đụng source code phải được user cho phép RÕ RÀNG"). Không commit/push khi user chưa báo.

**Goal:** Tab "Báo lỗi" ở mép phải mọi màn hrm-client: bấm ⇒ chụp trang + gom lỗi API ⇒ popup ⇒ gửi thành một tin nhắn báo lỗi vào nhóm hỗ trợ của công ty (hoặc nhóm/người tự chọn).

**Architecture:** BE thêm 1 API `POST v1/assign/chat/bug-reports` (dùng chung cho app sau này) gọi lại `MessageService::send()` với `meta.bug_report`; cài đặt nhóm mặc định theo công ty ở bảng mới. FE: bộ ghi lỗi trong bộ nhớ cắm vào plugin axios / errorHandler, chụp trang bằng html2canvas, popup `V2BaseModal`, khối hiển thị trong `ChatMessageItem`.

**Tech Stack:** Laravel 8 (PHP 7.4 + 8.1), Nuxt 2.14 / Vue 2 / bootstrap-vue, webpack 4 build bằng Node 12, PHPUnit, Playwright (Node 20).

**Spec:** `design.md` (cùng thư mục) · mockup `mockup.html`.

**Worktree:** `websites/wt-nhom-trao-doi/{hrm-api,hrm-client}` (:8080 / :3080 / socket :8895), nhánh mới `gop_db-chat-bao-loi` tách từ `origin/gop_db` ở cả 2 repo. E2E ở `HRM/e2e/tests/assign/`.

## Global Constraints

- Quy mô 1.000–2.000 người; logic ở BE, web chỉ chụp + gom + hiển thị (README agent-chat §0).
- Mỗi công ty 1 nhóm mặc định (Q11). Gửi tới: nhóm của **công ty đang chọn** nếu là thành viên, không thì trống.
- Báo lỗi 1–1 KHÔNG tạo nhiệm vụ từ tin; không sửa `MessageService::forward()`, `taskSource()`, `WorkspaceMemberService` (Q12, Q11).
- Mã quyền mới: `assign.bao_loi_cai_dat.manage` — tên "Cài nhóm tiếp nhận báo lỗi", phân hệ Công việc, feature "Báo lỗi màn hình" (Q13).
- Loại: `system` = Lỗi hệ thống · `data` = Số liệu sai · `info` = Thông tin sai · `other` = Khác / góp ý.
- Bộ ghi lỗi: 10 lỗi API, 3 toast lỗi, 3 lỗi JS gần nhất; KHÔNG ghi body request, header, token.
- Chụp quá 5 giây hoặc lỗi ⇒ mở popup không ảnh. Chống spam: 10 báo cáo / người / giờ.
- Người báo / công ty / phòng: BE tự điền từ phiên đăng nhập.
- Tab: rộng 22px, mép phải, giữa chiều cao, `ri-bug-line` + chữ dọc "Báo lỗi", mờ ~70%, hover đậm; phím tắt Ctrl/⌘ + Shift + B. **Lớp (user 14/11)**: tab nổi trên mọi popup / panel / ngăn chat (z 9990, dưới dropdown 9999 + toast 10000), chỉ ẩn khi popup báo lỗi mở / đang chụp; popup báo lỗi mở chồng (9995), đóng thì popup dưới còn nguyên; ảnh chụp có popup đang mở.
- Quy ước HRM: `V2BaseModal`, `V2Base*`, `button-convention`, lỗi validate đỏ đồng thời, `BaseModel`, Catalog quyền + `permission:catalog-sync`, không khai `messages()` cho rule phổ biến, số theo `en-US`.

## Review Focus

1. **Chụp hỏng vì ảnh khác nguồn (logo S3, avatar) làm "bẩn" canvas hoặc trang quá nặng** ⇒ popup vẫn mở, gửi được chữ. Test ở Task 6 + e2e B4.
2. **URL màn có tham số nhạy cảm** (`token`, `access_token`, `password`, `key`, `secret`) ⇒ bị thay bằng `***` trước khi gửi, cả ở URL màn lẫn đường dẫn lỗi API. Test ở Task 5.
3. **Nhóm mặc định đã đóng, đã bị xoá, hoặc người dùng bị loại khỏi nhóm** ⇒ ô Gửi tới để trống, không gửi nhầm, BE trả 403 nếu cố gửi. Test ở Task 2 + Task 4.
4. **Tab với popup khác / ngăn chat** (user 14/11, thay quy tắc cũ "dưới nền mờ + ẩn khi ngăn mở") ⇒ tab nổi TRÊN mọi popup / TaskPanel / ngăn chat và bấm được; popup báo lỗi mở chồng lên popup đang mở, đóng thì popup dưới giữ nguyên dữ liệu; ảnh chụp có popup nền, không có tab / popup báo lỗi. Test e2e B6.
5. **Gửi bằng phím tắt khi đang gõ trong ô nhập** ⇒ Ctrl/⌘+Shift+B vẫn mở popup nhưng không chèn ký tự; không mở popup thứ 2 nếu đang mở. Test e2e B5.

---

### Task 1: Bảng cài đặt + model + mã quyền

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_11_19_000001_create_chat_bug_report_settings_table.php`
- Create: `hrm-api/Modules/Assign/Entities/Chat/ChatBugReportSetting.php`
- Modify: `hrm-api/app/Support/Permissions/Catalog/assign.php` (thêm mục sau `assign.tpe_agent_cai_dat.manage`)

**Interfaces:**
- Produces: bảng `chat_bug_report_settings` (`id`, `company_id` unsigned big int **unique**, `workspace_id` unsigned big int nullable, `created_by`, `updated_by`, timestamps); model `ChatBugReportSetting extends BaseModel`, fillable `company_id, workspace_id, created_by, updated_by`; mã quyền `assign.bao_loi_cai_dat.manage` (`kind` action, `scopes` [], `platforms` ['hrm']).

- [x] Đọc skill `permission-seeder` rồi khai mã quyền theo đúng khuôn mục `assign.tpe_agent_cai_dat.manage`.
- [x] `php artisan migrate --pretend --path=Modules/Assign/Database/Migrations/2026_11_19_000001_create_chat_bug_report_settings_table.php` ⇒ chỉ 1 câu CREATE TABLE + unique index. **Hỏi user trước khi chạy thật vào db_gop_6_11.**
- [x] Chạy `php artisan permission:catalog-sync` (local) ⇒ mã mới có trong bảng `permissions`; cấp tạm cho vai trò test của NV 13 khi chạy e2e, gỡ sau (memory local-dev-duoc-cap-quyen-de-test).

### Task 2: API cài đặt nhóm mặc định

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Chat/BugReportSettingService.php`
- Create: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/Chat/BugReportController.php`
- Create: `hrm-api/Modules/Assign/Http/Requests/Chat/SaveBugReportSettingRequest.php`
- Modify: `hrm-api/Modules/Assign/Routes/Chat/api.php` (nhóm route mới `v1/assign/chat/bug-reports`, đặt trong file này)
- Test: `hrm-api/Modules/Assign/Tests/Feature/Workspace/ChatBugReportSettingTest.php`

**Interfaces:**
- Consumes: Task 1.
- Produces:
  - `BugReportSettingService::forViewer(int $companyId, int $employeeId): array` ⇒ `['workspace_id'=>?int, 'workspace_name'=>?string, 'conversation_id'=>?int, 'is_member'=>bool, 'can_manage'=>bool]`. `conversation_id`/`is_member` chỉ có khi nhóm còn mở và người xem đang `canSend` hội thoại space của nhóm.
  - `BugReportSettingService::save(int $companyId, ?int $workspaceId): ChatBugReportSetting`.
  - `GET v1/assign/chat/bug-reports/settings` (auth:api) ⇒ `forViewer(current_company_role, auth id)`.
  - `PUT v1/assign/chat/bug-reports/settings` (auth:api + `checkPermission:assign.bao_loi_cai_dat.manage`), body `{workspace_id: int|null}`; rule: `nullable|integer`, nhóm phải tồn tại, `company_id` = công ty đang chọn, chưa đóng ⇒ sai trả 422 `workspace_id` "Không hợp lệ".
  - Công ty hiện tại lấy như `AgentSettingsController::company()` = `(int) auth()->user()->current_company_role`.

- [x] Viết test: `test_get_tra_rong_khi_chua_cai` · `test_put_khong_quyen_403` · `test_put_co_quyen_luu_va_get_tra_dung_nhom` · `test_put_nhom_cong_ty_khac_422` · `test_put_nhom_da_dong_422` · `test_get_nguoi_khong_phai_thanh_vien_is_member_false_conversation_null` · `test_get_nhom_da_dong_sau_khi_cai_tra_conversation_null` (Review Focus 3).
- [x] Chạy `php -d memory_limit=1G vendor/bin/phpunit Modules/Assign/Tests/Feature/Workspace/ChatBugReportSettingTest.php` ⇒ FAIL.
- [x] Viết service + controller + request + route.
- [x] Chạy lại ⇒ PASS.

### Task 3: Tin nhắn mang dữ liệu báo lỗi

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Chat/MessageService.php:79-142` (`send`)
- Modify: `hrm-api/Modules/Assign/Services/Chat/ChatPresenter.php:~133` (thêm khoá `bug_report`)
- Test: `hrm-api/Modules/Assign/Tests/Feature/Workspace/ChatBugReportMessageTest.php`

**Interfaces:**
- Produces: `MessageService::send($conversation, $me, $data)` nhận thêm `$data['bug_report']` (array đã làm sạch ở Task 4) ⇒ tin `type = text`, `meta = ['bug_report' => …]`. Kèm sticker/card ⇒ 422 `bug_report`. Presenter trả `bug_report` (null khi tin thu hồi hoặc không có). Route gửi tin thường (`SendMessageRequest`) KHÔNG nhận `bug_report`.

- [x] Test: `test_gui_tin_thuong_kem_bug_report_bi_bo_qua` (POST `conversations/{id}/messages` có `bug_report` ⇒ tin không có meta) · `test_presenter_tra_bug_report` · `test_thu_hoi_an_bug_report` · `test_chuyen_tiep_tin_bao_loi_khong_mang_bug_report` (khoá hành vi Q12).
- [x] Chạy ⇒ FAIL · sửa `send` + presenter · chạy ⇒ PASS.
- [x] Chạy lại bộ chat cũ: `ChatApiTest ChatForwardTest ChatTaskCardTest ChatSidePanelTest` ⇒ PASS (2 ca `WorkspaceTaskTest` fail sẵn trên gop_db, ghi nhận không tính).

### Task 4: API gửi báo lỗi

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Chat/BugReportService.php`
- Create: `hrm-api/Modules/Assign/Http/Requests/Chat/SubmitBugReportRequest.php`
- Modify: `BugReportController.php` (method `store`), `Routes/Chat/api.php`
- Test: `hrm-api/Modules/Assign/Tests/Feature/Workspace/ChatBugReportSubmitTest.php`

**Interfaces:**
- Consumes: Task 2 (không bắt buộc), Task 3 `send(... ['bug_report'=>…])`, `ConversationService::getOrCreateDirect(int $me, int $other)`, `ConversationAccess::canSend()`.
- Produces: `POST v1/assign/chat/bug-reports` (auth:api, `throttle:10,60`) ⇒ trả tin đã present (giống `ChatController::send`) + `conversation_id`.
  - Body: `target_type` in:conversation,employee · `target_id` integer · `category` in:system,data,info,other · `description` required string max:2000 · `files` array max:5 (`url` required, `name`, `type`, `size`) · `context.url` max:1000 · `context.title` max:255 · `context.api_errors` array max:10 (`method`,`path` max:500,`status` integer,`message` max:500,`at`) · `context.toasts` array max:3 (string max:300) · `context.js_errors` array max:3 (string max:500) · `context.device` max:255 · `context.client_version` max:100.
  - `BugReportService::submit(int $me, array $validated): ChatMessage` — conversation ⇒ phải `canSend` (không thì 403 "Bạn không gửi được tin vào hội thoại này"); employee ⇒ cùng điều kiện `sendDirect` (khác mình, cả 2 đang làm) rồi `getOrCreateDirect`. `meta.bug_report` = `category` + `context` + `reporter` {employee_id, fullname, code, department_name} + `company` {id, name} (BE tự lấy).
  - Không khai `messages()` cho rule phổ biến.

- [x] Test: `test_gui_vao_nhom_la_thanh_vien_tao_tin_co_bug_report` · `test_gui_vao_nhom_khong_phai_thanh_vien_403` · `test_gui_vao_nhom_da_dong_khong_gui_duoc` · `test_gui_rieng_tao_hoi_thoai_1_1` · `test_thieu_mo_ta_va_loai_bao_loi_dong_thoi_422` (cả `description` lẫn `category` trong `errors`) · `test_reporter_lay_tu_phien_khong_lay_tu_body` · `test_lan_thu_11_trong_gio_429`.
- [x] Chạy ⇒ FAIL · viết service/request/route · chạy ⇒ PASS.
- [x] Lint PHP 7.4 + 8.1 các file mới (`php -l`).

### Task 5: Bộ ghi lỗi trên trình duyệt

**Files:**
- Create: `hrm-client/utils/bugReport/errorRecorder.js`
- Modify: `hrm-client/plugins/axios.js` (trong `$axios.onError`), `hrm-client/plugins/api-error-guard.js` (lỗi không phải API), `hrm-client/plugins/toast` (global `error`)
- Test: ca e2e ở Task 9 (repo không có unit test JS)

**Interfaces:**
- Produces (ES module, không phụ thuộc Vue để app desktop dùng lại):
  - `recordApiError(error)` — lấy `method`, `path` (không query; giữ query nhưng che khoá nhạy cảm), `status`, câu lỗi từ `apiErrorMessage`, `at` (HH:mm:ss); giữ 10 bản mới nhất.
  - `recordToast(text)`, `recordJsError(err)` — 3 bản mới nhất mỗi loại.
  - `maskSensitive(url: string): string` — thay giá trị tham số `token|access_token|password|pass|key|secret|signature` (không phân biệt hoa thường) bằng `***`.
  - `snapshot(): {api_errors, toasts, js_errors}` (bản sao).

- [x] Viết module + cắm 3 chỗ. Không đổi hành vi toast/redirect hiện có.
- [x] Kiểm bằng Playwright MCP trên :3080: chặn 1 API trả 500 ⇒ `window.$nuxt` gọi `snapshot()` có 1 phần tử đúng status/path; URL `?token=abc&month=10` ⇒ `maskSensitive` ra `?token=***&month=10` (Review Focus 2).

### Task 6: Chụp trang

**Files:**
- Modify: `hrm-client/package.json` (`html2canvas` **1.4.1** chính xác — HỎI USER trước khi cài)
- Create: `hrm-client/utils/bugReport/pageCapture.js`

**Interfaces:**
- Consumes: `compressImage(file)` (`utils/chat/imageCompress.js`).
- Produces: `capturePage({ timeoutMs = 5000 } = {}): Promise<Blob|null>` — vẽ `document.body` theo khung đang thấy (`x/y = scroll`, `width/height = innerWidth/innerHeight`), bỏ phần tử có `data-bug-report-ignore`, `useCORS: true`, `imageTimeout` ngắn; lỗi / quá hạn ⇒ `null` (không ném). Import động (`await import('html2canvas')`) để không nặng bundle chung.

- [x] Kiểm build: `NODE_OPTIONS=--max-old-space-size=8192 npm run build` trên Node 12 ⇒ build qua (html2canvas dịch được trên webpack 4).
- [x] Đo trên :3080 màn `/human/banks` và một màn bảng dài: thời gian chụp, kích thước ảnh sau nén. Trang có ảnh S3 khác nguồn ⇒ vẫn trả Blob hoặc `null`, không treo (Review Focus 1).

### Task 7: Tab + popup báo lỗi + cài đặt

**Files:**
- Create: `hrm-client/components/bug-report/BugReportTab.vue` (tab + phím tắt + gắn `data-bug-report-ignore`)
- Create: `hrm-client/components/bug-report/BugReportModal.vue` (`V2BaseModal`)
- Create: `hrm-client/components/bug-report/BugReportTargetSelect.vue` (ô Gửi tới)
- Create: `hrm-client/components/bug-report/BugReportSettingModal.vue`
- Modify: `hrm-client/components/BasicSubsystem.vue` (gắn `BugReportTab` cạnh `ChatDrawer`, chỉ client)

**Interfaces:**
- Consumes: Task 2 GET/PUT settings, Task 4 POST, Task 5 `snapshot()`/`maskSensitive()`, Task 6 `capturePage()`, `openImageEditor(source, {mode:'edit'})`, `captureScreen()` (dự phòng), `compressImage()`, `$store.dispatch('uploadImage', fd)` (khuôn `ChatComposer.upload`), `chatApi(this.$axios)`, `GET chat/conversations` (lọc `can_send`) + `GET chat/directory` cho ô Gửi tới, store `chat/openDrawer({ conversationId })`.
- Produces: popup theo mockup §2; footer `Huỷ` (tertiary) · `Gửi báo lỗi` (primary, `ri-send-plane-2-line`); link "⚙ Cài nhóm tiếp nhận" chỉ hiện khi `can_manage`.

- [x] Đọc skill `modal-popup`, `button-convention`, `form-validate`, `select-and-input-state`, `unsaved-changes` (popup có nhập ⇒ `unsavedModalMixin`).
- [x] Tab: ~~z-index dưới modal (< 1040); ẩn khi `chat.drawer.open`~~ → (user 14/11) z-index 9990 trên mọi popup + ngăn chat, popup báo lỗi chồng 9995; không hiện ở layout print/auth/kiosk (tab chỉ nằm trong `BasicSubsystem`). Phím tắt: không mở popup thứ 2.
- [x] Luồng: bấm ⇒ ẩn tab ⇒ `capturePage()` ⇒ mở popup (ảnh có/không) ⇒ GET settings điền sẵn Gửi tới khi `conversation_id` có ⇒ Gửi: tải ảnh (nén) ⇒ POST ⇒ toast "Đã gửi báo lỗi tới <tên>" + "Xem" (ẩn khi không mở được chat) ⇒ đóng.
- [x] Khối ảnh: "Khoanh / che chỗ nhạy cảm" (`openImageEditor`), "Chụp lại" (đóng popup tạm ⇒ `capturePage` ⇒ mở lại, giữ dữ liệu đang nhập), "Thêm ảnh (dán / tải lên)" + dán Ctrl+V trong popup; khi `capturePage` trả null thêm nút "Chụp bằng trình duyệt" (`captureScreen`). Tối đa 5 ảnh.
- [x] `context.client_version`: thêm `env.CLIENT_BUILD` trong `hrm-client/nuxt.config.js` = `git rev-parse --short HEAD` lúc build (lỗi ⇒ chuỗi rỗng); `context.device` = trình duyệt · hệ điều hành · `innerWidth×innerHeight`.
- [x] Bấm Gửi thiếu Loại + Mô tả + Gửi tới ⇒ cả 3 ô đỏ cùng lúc; 422 từ BE map về đúng ô; 429 ⇒ toast câu BE trả.
- [x] Đo bằng Playwright MCP 1440 và 1366: toạ độ tab (rộng 22, sát mép phải, giữa chiều cao), không chồng nút phân trang/nút Lưu ở 3 màn mẫu.

### Task 8: Khối báo lỗi trong tin nhắn

**Files:**
- Create: `hrm-client/components/chat/ChatBugReportBlock.vue`
- Modify: `hrm-client/components/chat/ChatMessageItem.vue` (render khối khi `message.bug_report`)

**Interfaces:**
- Consumes: presenter `bug_report` (Task 3).
- Produces: tiêu đề "Báo lỗi" + `V2BaseBadge` loại (màu chuẩn: system `#DC2626` · data `#F59E0B` · info `#0EA5E9` · other `#64748B`) · mô tả (body sẵn có) · ảnh (tệp sẵn có) · link màn (mở tab mới, đúng URL đã che) · lỗi API đầu tiên · "Thông tin kỹ thuật" thu gọn (công ty, người báo, thiết bị, phiên bản, toàn bộ lỗi API/toast/JS).

- [x] Viết component; tin thường không đổi (đo lại 1 tin thường + 1 tin báo lỗi bằng MCP).
- [x] Chạy lại e2e `chat-giao-dien`, `chat-toolbar-zalo`, `chat-panel-phai` ⇒ pass (đọc dòng tổng kết, bộ chạy serial).

### Task 9: E2E

**Files:**
- Create: `HRM/e2e/tests/assign/bug-report.spec.ts`

- [x] Ca (tài khoản NV 13; ca không quyền dùng tài khoản e2e thường):
  - B1 Có nhóm mặc định + là thành viên: bấm tab ⇒ popup có ảnh, Gửi tới điền sẵn ⇒ gửi ⇒ tin xuất hiện trong nhóm có badge loại + link màn.
  - B2 Không là thành viên: Gửi tới trống; chọn 1 người ⇒ tin vào chat 1–1.
  - B3 Bấm Gửi để trống ⇒ 3 ô đỏ cùng lúc.
  - B4 Chặn html2canvas lỗi (giả `capturePage` trả null qua route chặn chunk) ⇒ popup không ảnh, vẫn gửi được.
  - B5 Phím tắt khi đang focus ô nhập ⇒ mở popup, ô nhập không thêm ký tự; bấm lần 2 không mở popup thứ 2.
  - B6 (user 14/11) Mở 1 popup khác / ngăn chat ⇒ tab vẫn nổi + bấm được (`elementFromPoint` giữa tab = tab), popup báo lỗi chồng lên, ảnh có popup nền, đóng thì popup nền còn dữ liệu.
  - B7 Có quyền: link "⚙ Cài nhóm tiếp nhận" hiện, lưu được · Không quyền: link không hiện, PUT trả 403.
- [x] Chạy `cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test bug-report --workers=1` ⇒ 7/7, rồi chạy lại toàn bộ bộ chat (`chat-*`, `workspace-*`, `topbar-shortcuts`) ⇒ đọc dòng tổng kết.
- [x] Hỏi trước khi chạy: :8080 có FIREBASE ⇒ gửi tin có thể bắn push thật (memory rehearsal-gui-push-that).

### Task 10: Ghi deploy + tài liệu

- [x] `plan.md` checkpoint; README agent-chat §1/§3 cập nhật; `.plans/STATUS.md` mục AGENT + CHAT.
- [ ] Ghi chú deploy TPE: migration `2026_11_19_000001_create_chat_bug_report_settings_table` · `build_tpe.sh` (tự `permission:catalog-sync`) · build client · cấp mã `assign.bao_loi_cai_dat.manage` ở `/admin/roles` · quản trị tạo nhóm "Hỗ trợ phần mềm" từng công ty + thêm thành viên + cài nhóm mặc định.

---

## Kết quả thực hiện (14/11/2026, Subagent-Driven, sổ chi tiết `ledger-sdd.md`)
- Nhánh `gop_db-chat-bao-loi` (api từ 70aacc60d · client từ f0a0e778b), worktree `wt-nhom-trao-doi`, **CHƯA commit** (api 14 file · client 11 file) + e2e `HRM/e2e/tests/assign/bug-report.spec.ts`.
- Task 1–9 xong, mỗi task qua review spec + chất lượng; review toàn nhánh (opus) ⇒ 1 đợt sửa 10 điểm ⇒ kiểm lại 10/10.
- User 14/11 bổ sung: tab NỔI TRÊN mọi popup / panel nhiệm vụ / ngăn Chat-Agent; ảnh chụp gồm popup đang mở; Esc của `TaskPanel.vue` nhường popup báo lỗi (user duyệt sửa 1 dòng).
- Sửa thêm: html2canvas không đọc màu `color(srgb …)` sinh từ `color-mix()` (V2BaseSegmented, panel nhiệm vụ) ⇒ chụp hỏng ⇒ đổi màu sang rgba trên bản sao trước khi chụp.
- Test: PHPUnit `--filter ChatBugReport` 21/118 OK · e2e bug-report 8 passed · hồi quy chat-drawer, chat-core, chat-giao-dien, chat-toolbar-zalo, chat-panel-phai, chat-bo-sung, chat-gd2-polish, chat-thong-bao-emoji, workspace-tasks, workspace-meetings, topbar-shortcuts đều pass (env :3080/:8080 — xem ledger Task 9).
- DB local db_gop_6_11: đã chạy migration `2026_11_19_000001`; chèn tay dòng quyền `assign.bao_loi_cai_dat.manage` (id 1000000939); role tạm `TMP_GD11_BaoLoi` (id 1000001125) cấp NV 13 — gỡ bằng `revoke_gd11_role_tam.php` (cùng thư mục, chạy: `php artisan tinker --execute="$(cat …)"` trong wt-nhom-trao-doi/hrm-api) khi user thử xong.

## Ghi chú deploy TPE
1. Kiểm `build_tpe.sh` cài gói client bằng npm hay yarn: `package-lock.json` đã có `html2canvas@1.4.1`, **`yarn.lock` CHƯA** ⇒ nếu `yarn --frozen-lockfile` sẽ fail.
2. Chưa chạy `nuxt build` lần nào (dev :3080 dùng chung .nuxt) ⇒ build thử trên Node 12 trước khi deploy.
3. api: migration `2026_11_19_000001_create_chat_bug_report_settings_table` (tạo bảng, không đổi dữ liệu) · `build_tpe.sh` tự `permission:catalog-sync` (mã mới) · không cần restart worker riêng.
4. Cấp mã "Cài nhóm tiếp nhận báo lỗi" ở `/admin/roles` · quản trị tạo nhóm hỗ trợ từng công ty + thêm thành viên + cài nhóm mặc định (popup báo lỗi ⇒ "⚙ Cài nhóm tiếp nhận").

## Đợt bổ sung (14/11 tối, user: "Mục 3 ⇒ bổ sung API", "còn lại ok", "làm")
- [x] API `GET v1/assign/chat/bug-reports/settings/workspaces?q=&page=` — nhóm còn mở của công ty đang chọn (kể cả không là thành viên), tìm tên, 20/trang, quyền `assign.bao_loi_cai_dat.manage`; PHPUnit +4 (`--filter ChatBugReport` 25 OK).
- [x] `BugReportSettingModal.vue` dùng API mới (bỏ đọc 3 trang + lọc công ty ở FE).
- [x] `nuxt.config.js` `env.CLIENT_BUILD` = git short hash ⇒ popup hiện phiên bản.
- [x] Chữ nút giữ theo skill (user ok).
- [x] E2E B7 cài nhóm không là thành viên + 403 khi không quyền; bug-report 8 passed, chat-drawer + topbar 8 passed. Review: Approved.
- [x] Chữ trên tab đổi "Báo lỗi" ⇒ "YC hỗ trợ" (user 14/11; tooltip "Yêu cầu hỗ trợ / báo lỗi màn hình này"); đo MCP: tab 22×72, chữ 11×47.6 không bị cắt.
- [x] User "Đổi tất cả": mọi chữ hiển thị "báo lỗi" ⇒ "yêu cầu hỗ trợ": tiêu đề popup "Yêu cầu hỗ trợ", nút "Gửi yêu cầu", toast "Đã gửi yêu cầu hỗ trợ tới …", khối tin "Yêu cầu hỗ trợ", popup cài đặt, câu 429; tên quyền "Cài nhóm tiếp nhận yêu cầu hỗ trợ" (Catalog + test + dòng DB local). Mã quyền/route/tên file giữ nguyên. PHPUnit 25 OK; MCP: tiêu đề + nút 1 dòng cao 32.
- "Chưa lưu" khi mở/đóng popup cài đặt: KHÔNG tái hiện được (thử Esc/Hủy/X/nền/chọn lại) ⇒ chưa sửa, chờ user mô tả nếu còn gặp.
- Còn lưu ý: phím tắt chưa thử trên Chrome thật (macOS Cmd+Shift+B) · trang cực nặng chụp lâu · popup cài đặt chỉ hiện 20 nhóm đầu, nhóm khác phải gõ tìm.

### Checkpoint — 14/11/2026 khuya (wrap up)
Vừa hoàn thành: GĐ11 "YC hỗ trợ" (báo lỗi màn hình) — code + review + e2e + đổi tên hiển thị + push gop_db (api 86fcb16ba · client 814664a79) + DEPLOY TPE (build_tpe.sh EXIT 0, migration 2026_11_19_000001 đã chạy, site 200). Role tạm local đã gỡ.
Đang làm dở: —
Bước tiếp theo: user cấp quyền "Cài nhóm tiếp nhận yêu cầu hỗ trợ" ở /admin/roles + tạo nhóm hỗ trợ từng công ty + cài nhóm mặc định; theo dõi yêu cầu thật trên prod. Còn lưu ý: phím tắt Cmd+Shift+B trên Chrome macOS chưa thử tay · trang cực nặng chụp lâu · popup cài đặt hiện 20 nhóm đầu (gõ để tìm).
Blocked: —
