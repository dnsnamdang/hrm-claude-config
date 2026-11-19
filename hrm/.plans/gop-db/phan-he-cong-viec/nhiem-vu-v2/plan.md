# Plan — Nhiệm vụ v2 (web panel + app NV2)

Design: `design.md` cùng thư mục. Chưa có lệnh code — mỗi phase hỏi riêng phạm vi rồi mới làm.

## Phase 1 — BE `hrm-api` (`gop_db`)
- [x] 1.1 Vá `TaskService::update`: kiểm `canEdit()` (trừ luồng đổi trạng thái/nhập kết quả theo `allowed_next_statuses` + `canImportResult`), cho phép gửi rỗng để xoá giá trị (dùng `$request->has()` thay `??`).
- [x] 1.2 Vá `store`: `status` chỉ nhận Nháp(1)/2/3/4; `start_date` trống ⇒ ngày giao.
- [x] 1.3 `PATCH assign/tasks/{task}/field` — body `{field, value}`, whitelist trường (title, description, due_date+due_time, start_date, estimated_hours, priority, assignee_id, approver_id, watchers, tags, solution/project/module/meeting, progress rule, recurring, links), kiểm `canEdit`, ghi lịch sử qua `historyService()`.
- [x] 1.4 Migration `task_extension_requests` + model + `TaskExtensionRequestController` (gửi / đồng ý / từ chối / huỷ) + thông báo + lịch sử; `DetailTaskResource` trả `pending_extension`, `can_request_extension`, `can_decide_extension`.
- [x] 1.5 Test phpunit cho 1.1–1.4 (có ca không quyền) + chạy test Assign hiện có.

### Ghi chú Phase 1 (làm 08/11/2026)
- Người không có `canEdit` gọi PUT: các trường thông tin bị **bỏ qua im lặng** (không 403) vì popup xem/duyệt cũ gửi lại cả form chưa đổi; giữ `status` + `reject_reason`; người làm giữ thêm kết quả + tick/ghi chú checklist đã có (`TaskService::keepOnlyNonEditorFields`).
- Trường không bắt buộc của PUT (`description`, `project_id`, `meeting_id`, `meeting_report_id`, `solution_id`, `solution_module_id`, `due_date`, `due_time`, `approver_id`): gửi rỗng ⇒ NULL. `start_date` để trống ⇒ giữ mốc cũ (sửa) / ngày giao (tạo).
- POST `status` chỉ nhận 1/2/3/4. **Chưa** khoá "Đang thực hiện (4) chỉ khi tự giao cho mình" — web hiện cho chọn 4 khi giao người khác; khoá ở Phase 2 cùng công tắc "Bắt đầu ngay".
- API mới: `PATCH assign/tasks/{task}/field` (field: title, description, priority, start_date, due{due_date,due_time,reason}, estimated_hours, assignee_id, approver_id, watchers, tags, link{solution_id,solution_module_id,project_id,meeting_id}, progress_report, recurring, linked) · `POST assign/tasks/{task}/extension-requests` · `POST assign/tasks/extension-requests/{id}/approve|reject|cancel`. Mọi API trả `DetailTaskResource` mới nhất; chi tiết có thêm `pending_extension`, `can_request_extension`, `can_decide_extension`, `can_cancel_extension`.
- Lịch sử: đổi hạn ghi lý do vào `note`; đề nghị gia hạn ghi dòng "Thay đổi thông tin" với trường "Đề nghị gia hạn" (giữ 3 nhóm lọc cố định).
- Migration đã chạy vào `db_gop_6_11` (local): `Modules/Assign/Database/Migrations/2026_11_10_000001_create_task_extension_requests_table.php`.
- Test: `Modules/Assign/Tests/Feature/Task/TaskV2ApiTest.php` 17/17 xanh; `tests/Unit/EmployeeWork*` 8/8, `MyTodo` 9/9; quét DB không còn rác.

## Phase 2 — Web `hrm-client` (`gop_db`)
- [x] 2.1 `components/assign/task/TaskPanel/*` — khung panel trượt phải, header (pill trạng thái ▾, ưu tiên, 👁 theo dõi, liên kết, ⋮, ×), dải nút theo vai trò.
- [x] 2.2 Tab Chi tiết: lưới trường bấm-để-sửa (popover formPop) theo `can_edit`; Mô tả; Checklist tick; Nhiệm vụ con; Tệp; Thiết lập (Lặp lại, Báo cáo tiến độ, Liên kết).
- [x] 2.3 Tab Kết quả & tiến độ (thay ImportResultModal): Báo kết quả, Cập nhật tiến độ (% luỹ kế), Nhật ký tiến độ, duyệt / từ chối kết quả.
- [x] 2.4 Tab Bình luận (dùng lại comment-thread hiện có) + tab Lịch sử (system-logs/task).
- [x] 2.5 Form Tạo / Sửa toàn bộ theo mockup (bỏ Không gian — N4), footer Giao việc · Giao & tạo tiếp · Lưu nháp · Huỷ; validate báo đồng thời.
- [x] 2.6 Đổi hạn (người giao) / Đề nghị gia hạn + thanh duyệt đề nghị.
- [x] 2.7 Thay 20 chỗ gọi (giữ API `create/edit/view/open`), xoá CreateTaskModal + ImportResultModal.
- [x] 2.8 Kiểm Playwright: cả 20 chỗ mở được panel; luồng tạo → giao → bắt đầu → báo kết quả → duyệt; đề nghị gia hạn; tài khoản không quyền; cập nhật spec e2e.

### Ghi chú Phase 2 (làm 08/11/2026)
- Code: `hrm-client/components/assign/task/panel/` — `TaskPanel.vue` (khung + API công khai create/edit/view/open, sự kiện saved/reload), `TaskDetailTab.vue`, `TaskResultTab.vue`, `TaskForm.vue`, `TaskFieldPopover.vue`, `taskPanelHelpers.js`, `task-panel.scss`. 19 file gọi đổi sang `TaskPanel`; `$refs.importResultModal.open()` → `$refs.createTaskModal.open()`. Đã xoá `CreateTaskModal.vue` + `ImportResultModal.vue`.
- BE thêm trong Phase 2 (user chốt N6/N7): `POST assign/tasks/{task}/watch` + cờ `is_watching`; tạo ở Đang thực hiện chỉ khi tự giao (422); Lưu nháp chỉ bắt buộc Tên, Giao việc bắt buộc thêm Hạn; Nháp → Giao việc qua PUT bắt đủ người làm/hạn/số giờ; luật "% = 100" chỉ chạy khi thật sự BÁO hoàn thành (không chạy khi duyệt KQ / giữ nguyên trạng thái); priority trống khi nháp ⇒ Bình thường. Test BE 23/23.
- Lớp: panel 1035 (dưới lớp bọc b-modal 1040 ⇒ popup mở từ panel nổi lên); mở đè lên popup ⇒ 1059 + `ask()` nâng hộp xác nhận lên 1075; Esc bắt ở pha capture (không đóng popup nền).
- Kiểm Playwright MCP (1440): tạo + báo lỗi đồng thời 4 ô, giao, sửa nhanh hạn/ưu tiên + lịch sử, nháp → giao (3 ô lỗi), checklist/nhiệm vụ con/tệp (upload giả lập — local ghi S3 prod), Sửa toàn bộ, người làm: gia hạn/bắt đầu/tiến độ/báo KQ, người giao: đồng ý gia hạn/duyệt KQ, người ngoài (NV 34) không nút + tự theo dõi, panel trong popup TaskUpcoming (z, Esc, xác nhận), tạo từ tab Nhiệm vụ của giải pháp (khoá Giải pháp, tự điền Dự án). Dữ liệu thử đã dọn.
- E2E: spec mới `e2e/tests/assign/task-panel-v2.spec.ts` (6 ca, có ca không quyền); sửa `work-calendar-popup`, `my-todo-list-drawer`, `employee-work-performance` theo panel. **Chưa chạy bộ e2e** (chỉ chạy khi user yêu cầu).
- (08/11 sau góp ý) ĐÃ XỬ LÝ điểm mở 1: bỏ hết `<button>` thô trong panel — `V2BaseStatusMenu` (MỚI, ghi skill button-convention 6e), `V2BaseChip`, `V2BaseQuickAddButton`, `V2BaseIconButton`, `V2BaseRowActions`, `V2BaseTabNavigation`, `V2BaseSegmented`. Form: ô chọn người xếp 50/50 (Người duyệt | Người theo dõi), Thiết lập ghép [Báo cáo | Lặp lại] + hàng chi tiết đủ 12 cột; danh sách chọn người luôn có người đang đăng nhập + người đang gắn (NV 13 không nằm trong `tasks/employees`); select2 trả chuỗi → so `Number()`.
- (08/11) Chip Mức độ ưu tiên giống mockup: `V2BaseSegmented` + class `tkp-prio-seg` (đè CSS chỉ trong panel, KHÔNG sửa component gốc) — chưa chọn nền nhạt cùng màu, đang chọn nền đậm chữ trắng + ✓ (`prioritySegments()`); ô sửa nhanh ưu tiên rộng 420px.
- (08/11) ĐÃ XỬ LÝ điểm mở 2: sửa nhanh Báo cáo tiến độ / Lặp lại / Liên kết ở tab Chi tiết (popover) + khối Liên kết trong form (`TaskLinksEditor`, tìm qua `assign/tasks?keyword=` có phân trang). BE (user cho phép): quan hệ `TaskLink::linkedTask` + `linked_tasks[].linked_task_code/title/status_*` (nạp kèm ở loadDetail). Test BE 25/25. Ô sửa nhanh tự đặt lại vị trí khi đổi cao (ResizeObserver), dropdown select2 gắn body + `body.tkp-pop-open` nâng z.
- (08/11) Rà theo mockup — đã áp (không đụng V2Base): nút đầu tô đậm / sau viền, giữ thứ tự BE, nhãn + icon theo `actLabel`; icon trước chữ trên viên trạng thái (`STATUS_ICONS`, prop `icon` của V2BaseStatusMenu); Mô tả bỏ dòng trống (pre-line); banner gia hạn "cũ → mới" + “lý do”; nhiệm vụ con có icon trạng thái + avatar; Thiết lập thứ tự Lặp lại · Báo cáo · Liên kết, liên kết là link mở nhiệm vụ + chú thích kiểu; tab Kết quả: ô số liệu chỉ khi có kết quả, thứ tự Tiến độ · Số giờ được giao · Số giờ làm thực tế · Hiệu suất (<100% tô cam), "X gửi lúc", rỗng có nút Nhập kết quả, khối Duyệt kết quả cho người duyệt, "+ Cập nhật tiến độ" dưới nhật ký; form: Thêm nhanh checklist / nhiệm vụ con (3 dòng trống).
- (08/11) E2E `--workers=1`: `task-panel-v2.spec.ts` **9/9 xanh** (sau khi sửa spec: escape `$` trong tinker, chờ 422 vì API local chậm, chờ modal hết fade, viên trạng thái có icon). 3 spec cũ: chưa chạy tới ca nhiệm vụ — `employee-work-performance` seed hỏng có sẵn (bảng `roles` DB gộp bắt `company_id` FK, seed không truyền); `my-todo-list-drawer` đỏ ở ca MEETING trước ca task (serial); `work-calendar-popup` ca task bị skip vì fixture không tìm được giải pháp không hạng mục để tạo task, ca nhắc việc cá nhân không thấy thẻ. Đều là dữ liệu/fixture, chưa vá (ngoài luồng).
- Còn mở: (2) Thiết lập (Báo cáo/Lặp lại/Liên kết) ở tab Chi tiết chỉ đọc — đổi qua Sửa toàn bộ; form mới không có ô Liên kết nhiệm vụ (giữ nguyên liên kết cũ khi lưu); (3) Esc khi có popup mở SAU panel-đè-popup sẽ đóng panel trước.
- Ngoài luồng (note, không sửa): cột Tag ở `/assign/tasks` hiện "[]"; banner gia hạn dùng `requested_by_name` mới thêm ở BE.

## Phase 3 — App `TPE_APP` (`develop`)
- [x] 3.1 Model/API: PATCH field, đề nghị gia hạn, cờ mới.
- [x] 3.2 Danh sách NV2-01…03 (chip Tất cả · Của tôi · Quá hạn · Chờ tôi duyệt; gom theo Trạng thái/Hạn trên trang đã tải; 💬).
- [x] 3.3 Chi tiết 3 tab NV2-04/05/08/21 + nút theo trạng thái NV2-09…20 + sheet NV2-06/07/22–29.
- [x] 3.4 Báo kết quả / Cập nhật tiến độ NV2-30/31.
- [x] 3.5 Form Tạo / Sửa NV2-10/11/13/32–37.
- [x] 3.6 Bình luận NV2-12.
- [x] 3.7 Bấm thử trên máy ảo (tpeLocal, namdangit) từng luồng.

### Checkpoint — 08/11/2026 (Phase 1)
Vừa hoàn thành: Phase 1 BE (vá PUT/POST, PATCH 1 trường, đề nghị gia hạn + migration chạy local, 17 test).

### Checkpoint — 08/11/2026 (Phase 2)
Vừa hoàn thành: Phase 2 web — TaskPanel thay 2 popup ở 19 file gọi, BE bổ sung N6/N7 + luật nháp; kiểm Playwright MCP đủ vai trò; spec e2e mới + sửa 3 spec.
Đang làm dở: —
Bước tiếp theo: (1) user xem 3 điểm còn mở; (2) chạy bộ e2e nếu user yêu cầu; (3) hỏi riêng phạm vi Phase 3 (app TPE_APP develop).
Blocked: chưa có lệnh code Phase 3

### Checkpoint — 08/11/2026 (Phase 3 — chi tiết)
Vừa hoàn thành: 3.1 + 3.3 — `work_task_detail_page.dart` viết lại (3 tab, sửa 1 trường qua sheet `work_edit_sheet.dart`,
đề nghị / duyệt / huỷ gia hạn, theo dõi, checklist, đáy tối đa 2 nút + bước còn lại vào ⋮ và sheet trạng thái).
Bấm thử simulator: người giao (task 168) + người làm (task 198 tạo tay trên DB local, người giao id 50).
Đang làm dở: 3.2 danh sách NV2-01…03.
Bước tiếp theo: 3.2 → 3.5 form → 3.4/3.6 rà lại màn có sẵn.
Blocked:

### Checkpoint — 08/11/2026 (Phase 3 — danh sách)
Vừa hoàn thành: 3.2 — danh sách gom nhóm (Trạng thái / Người làm / Hạn / Dự án, gom trên trang đã tải, ≤ 5 dòng/nhóm
+ "Xem thêm"), menu phạm vi Tất cả · Của tôi · Quá hạn · Chờ tôi duyệt (số tải lúc mở menu), sheet Cách xem lưu
`human/filter-customizations` bảng `tasks_view` dạng `{key,isVisible}` (`group:` / `sort:` / `field:`), 4 lọc vai trò
chuyển vào bảng lọc ("Vai trò của tôi"), luật L2 nộp trước hạn không tính quá hạn (tính ở app).
BE: `overdue=1` cho `GET assign/tasks` (+1 test, 26/26 xanh) — user cho phép 08/11.
Chưa làm theo bản vẽ: nút hành động nhanh trên dòng (list API không trả bước chuyển); "Số file" trong Cách xem (list
API không trả số file). Số "n quá hạn" đầu danh sách là của BE, vẫn tính việc đã nộp đúng hạn (lệch L2).
Đang làm dở: —
Bước tiếp theo: 3.5 form Tạo/Sửa NV2-10/11/13/32–37.
Blocked:

### Checkpoint — 08/11/2026 (Phase 3 — form)
Đã commit trước bước này: hrm-api `9b57baace`, hrm-client `f3055c8e1`, TPE_APP `54c4cf5` (chưa push).
Vừa hoàn thành: 3.5 — `work_task_form_page.dart` viết lại: bỏ Đơn giản/Nâng cao + Trạng thái khởi tạo; "Cần duyệt
triển khai" (2/3), tự giao → "Bắt đầu ngay" (4, nút "Tạo & bắt đầu"); [Lưu nháp | Giao việc ▴ Giao & tạo tiếp];
Sửa: [Đóng | Lưu thay đổi] giữ trạng thái; sửa nháp: [Lưu nháp | Giao việc]; kiểm đồng thời Người làm · Hạn · Số giờ +
dải đỏ; "+ Ngày bắt đầu"; chip ưu tiên màu BE; hàng "+ Checklist · + Nhiệm vụ con · + Tệp"; Thiết lập có thứ báo cáo /
ngày trong tháng / Xem trước; KHÔNG gửi recurring/linked. Chi tiết: dòng khoá "Có nhiệm vụ con — không sửa được nhiệm vụ cha".
Bấm thử simulator: tạo tự giao + bắt đầu ngay (id 255), sửa toàn bộ id 168 (giữ tệp/lặp lại/liên kết), lưu nháp (257) →
mở lại Giao việc, nhiệm vụ chung 2 người + cần duyệt + Giao & tạo tiếp (258/259).
Chưa thử: đính kèm tệp (upload local ghi S3 PROD — không thử thật).
Bước tiếp theo: 3.4 Báo kết quả / tiến độ NV2-30/31 → 3.6 Bình luận NV2-12.
Blocked:

### Checkpoint — 08/11/2026 (Phase 3 — báo kết quả / tiến độ / bình luận)
Vừa hoàn thành: 3.4 — `work_task_result_page.dart` tách 2 chế độ: Báo kết quả (NV2-30: dòng "Sau khi gửi: … · X duyệt",
bỏ ô chọn trạng thái, bắt buộc giờ thực tế + kết quả, chặn checklist chưa xong, dải "Còn n lỗi: …", [Đóng | Gửi kết quả])
và Cập nhật tiến độ (NV2-31: ngày hôm nay khoá, giờ hôm nay *, % luỹ kế * ≥ lần trước và < 100, nội dung; giữ trạng thái;
giờ hôm nay cộng vào actual_hours do BE không tự cộng). 3.6 — màn Bình luận có sẵn đủ (dải Xem nhiệm vụ, trả lời, @, tệp).
Bấm thử simulator trên task 198: tiến độ 1.5 giờ / 40% → nhật ký + actual_hours 1.5; báo kết quả bị chặn đúng 2 lỗi →
tick đủ → Hoàn thành - Chờ duyệt (hiệu suất 533%); bình luận + Xem nhiệm vụ + badge 💬.
Điểm mở: NV2-12 "dòng hệ thống trong luồng bình luận" (đổi trạng thái / nộp / đổi hạn…) — web CommentThread cũng chưa có,
cần BE + web + app; chưa làm.
Đang làm dở: — (Phase 3 xong phần màn; chưa commit TPE_APP các bước form + kết quả)
Bước tiếp theo: user xem lại; điểm mở NV2-12; nút hành động nhanh trên dòng danh sách (cần list API trả bước chuyển).
Blocked:

### Checkpoint — 08/11/2026 (Phase 3 — 2 điểm mở)
User cho phép (08/11): (A) hành động nhanh trên dòng, (B) dòng hệ thống trong luồng bình luận — BE + web + app.
Vừa hoàn thành:
- (A) BE `Task::quickAction()` + `TaskResource.quick_action` (1 bước tiến tới theo vai trò: Bắt đầu · Làm tiếp ·
  Báo kết quả · Duyệt kết quả · Duyệt triển khai; quyền duyệt triển khai cache theo người xem). App: nút tròn 32 trên
  💬; Báo kết quả → màn Báo kết quả, bước khác → xác nhận + PUT. Nút xác nhận chữ > 10 ký tự → "Đồng ý" (`workConfirmText`,
  sửa luôn tràn 2px ở chi tiết).
- (B) BE trait `CommentModeration::commentSystemEvents()` mặc định rỗng, `TaskCommentController` ghi đè đọc `task_history`
  (subset: tạo · đổi trạng thái · đổi hạn · đề nghị / từ chối / huỷ gia hạn) trong khoảng thời gian của trang → khoá
  `system_events`. Web `CommentThread.vue` trộn theo thời gian (ghim vẫn đầu). App `task_comments_page.dart` đọc nguyên body
  qua `WorkApiService.getRaw()` (hàm mới, chỉ thêm) — vẫn 1 request.
- Test BE: TaskV2ApiTest 28/28 (thêm 2 ca). Kiểm: Playwright MCP panel web task 198; simulator danh sách + bình luận.
Chưa kiểm: bình luận Vấn đề trên app/web với dữ liệu thật (DB local không có vấn đề nào; đã gọi controller qua tinker
→ `system_events: []`, khuôn cũ giữ nguyên). Log lịch sử cũ dạng snapshot (is_subset = 0) không hiện thành dòng hệ thống.
Bước tiếp theo: user xem; commit khi user báo.
Blocked:

### Checkpoint — 08/11/2026 (commit + e2e)
Commit: hrm-api `be9fe9311`, hrm-client `9b900d01a`, TPE_APP `0a11e1f` (chưa push).
E2E `HRM/e2e/tests/assign/task-panel-v2.spec.ts` thêm ca 7 (dòng hệ thống trong bình luận + bình luận mới nằm sau)
+ afterAll dọn `comments`. Chạy cả bộ --workers=1: 10 passed (3 setup + 7 ca), dữ liệu ZZE2E dọn sạch.
Đã push 08/11: hrm-api gop_db `643e0849f..be9fe9311`, hrm-client gop_db `6de64b621..9b900d01a`, TPE_APP develop `59641ca..0a11e1f`.
Bước tiếp theo: lên server cần chạy migration `2026_11_10_000001_create_task_extension_requests_table`.
Blocked:

### Checkpoint — 08/11/2026 20:00 (wrap up)
Vừa hoàn thành: Phase 1 BE + Phase 2 web + Phase 3 app (chi tiết, danh sách gom nhóm, form, báo kết quả / tiến độ,
hành động nhanh, dòng hệ thống trong bình luận) — đã commit + push 3 repo; e2e task-panel-v2 10 passed.
Ngoài lề: user hỏi vì sao update prod báo "sửa 257 quyền" — đã giải thích (merge Hợp đồng bán chèn 2 quyền ở vị trí
684/940 → 254 quyền chỉ lệch sort_order; 3 sửa thật). Đề xuất tách đếm "đổi thứ tự" trong CatalogSync — CHƯA có lệnh code.
Đang làm dở: —
Bước tiếp theo: deploy cần chạy migration `2026_11_10_000001_create_task_extension_requests_table`; dọn task demo local
(168, 198, 255, 257, 258, 259 + nhiệm vụ con của 255) nếu user muốn; build app thử máy thật.
Blocked:

### Checkpoint — 08/11/2026 (test app)
`fvm flutter test` bộ cũ 137/137 xanh. Thêm `app/test/ui/work/work_task_v2_test.dart` 14 ca (gom nhóm 4 kiểu, luật L2,
cột hạn, Cách xem toConfig/fromConfig + cấu hình lạ, nút xác nhận, thời gian tương đối, icon trạng thái) — đã thử đảo luật
L2 thì ca L2 đỏ. Cả bộ 151/151 xanh. Chưa commit.
Chưa có test: thứ tự nút chính ở chi tiết (hàm `_rank` private trong State — muốn test phải tách ra hàm dùng chung).

### Checkpoint — 08/11/2026 (bỏ dòng hệ thống trong bình luận)
User chọn phương án 3: bỏ hẳn + sửa Pen. Đã trả về bản trước commit: hrm-api `CommentModeration.php` + `TaskCommentController.php`
(từ 643e0849f), gỡ ca test BE (27/27 xanh); hrm-client `CommentThread.vue` (từ 6de64b621); TPE_APP `task_comments_page.dart`
+ `work_api_service.dart` (từ 59641ca). E2E bỏ ca 7 → 9 passed. App test 151/151. Pen NV2-12: xoá node `sys`, ghi chú
"[08/11 — bỏ] KHÔNG chèn dòng hệ thống…", đã save. Chưa commit (kèm file test app `work_task_v2_test.dart`).

### Checkpoint — 08/11/2026 (rà app theo Pen 100%)
User chốt: làm hết nhóm A (lệch giao diện); B1–B5 theo thiết kế (tiêu đề "Nhiệm vụ", chip 💬 có số, thanh công cụ danh sách
1 hàng + 🔍 mở ô tìm, Xoá mờ kèm lý do trong ⋯, chọn người bằng sheet NV2-23); C: bỏ Sao chép liên kết (xoá cả Pen: 24 icon +
mục menu), API trả số file.
API (chưa commit): `files_count` ở danh sách (withCount attachments); `status_note` (lý do tạm dừng / nhận xét duyệt) → ghi
chú lịch sử + thông báo; thêm thông báo Tạm dừng cho bên còn lại; giữ `status_note` cho người không có quyền sửa. 29/29 test.
App (chưa commit): viết lại chi tiết (đầu màn phẳng, dải theo trạng thái Nháp / duyệt triển khai / tạm dừng / từ chối /
hoàn thành, tab gạch chân, avatar, sheet Tạm dừng / Duyệt / Từ chối, đáy nút theo bề rộng chữ, menu ⋯ riêng), danh sách
(thanh công cụ, ⓘ nhóm, icon trạng thái mới, Cách xem 4 ô + Số file), form (dòng phẳng, chip ưu tiên, nút tách), Báo kết
quả / Tiến độ (chip tên, ô khoá, viền đỏ checklist, chip tệp, "Nội dung đã làm" bắt buộc), sheet đáy [Chính | Đóng].
Widget mới `work_people_sheet.dart` (sheet chọn người + WorkAvatar). App test 151/151.
Demo DB local: task 198 đổi approver_id = 13 rồi duyệt xong (Hoàn thành).


### Checkpoint — 08/11/2026 (nút app + kiểm 3 trạng thái trên simulator)
- [x] Nút dùng chung toàn app (`custom_view/primary_button.dart`, user chốt "Toàn app"): chữ 14.5 w600 cố định (bỏ 15.sp),
  icon 17, cách 7, đệm ngang 14; chữ KHÔNG cắt "…" — thiếu chỗ thì `FittedBox(scaleDown)`. Test mới
  `app/test/custom_view/primary_button_label_test.dart` (3 ca, máy 402×874 + font Roboto thật).
- [x] Đáy chi tiết Nhiệm vụ: đo bề rộng chữ thật, không đủ 1 hàng → 2 hàng (nút trắng chia đều trên, nút chính cả hàng dưới).
- [x] Banner Từ chối / Tạm dừng: người thao tác là mình → "Bạn"; từ "Chờ phê duyệt triển khai" → "từ chối triển khai"
  (từ Chờ bắt đầu vẫn "từ chối nhận việc").
- [x] Sheet nhập liệu (`work_edit_sheet.dart` + các sheet ở chi tiết): sửa ô đang đỏ → tắt lỗi ô đó ngay.
- [x] Kiểm trên simulator với data demo 456 (Từ chối kết quả), 457 (Từ chối triển khai), 458 (xin gia hạn → Đạt duyệt → hạn
  19/11). App test 154/154, BE TaskV2ApiTest 29/29, e2e task-panel-v2 9 passed.
Đang làm dở: —
Bước tiếp theo: user trả lời — trạng thái "Từ chối triển khai" có giữ nút "Làm tiếp" (BE cho vào thẳng Đang thực hiện)
không; commit/push khi user yêu cầu (hrm-api, hrm-client, TPE_APP đều còn thay đổi chưa commit); dọn demo 456–458.
Blocked:

### Checkpoint — 08/11/2026 (chặn đi tắt Từ chối triển khai + push)
- [x] User chốt bỏ "Làm tiếp" ở Từ chối triển khai, sửa BE: `Task::getAllowedNextStatuses` case REJECTED_START — người giao
  chỉ còn Chờ phê duyệt triển khai; thêm Chờ bắt đầu (Giao lại) khi là người làm từ chối nhận việc. Phân biệt bằng
  `Task::wasRejectedAtStartApproval()` (dòng lịch sử change_status gần nhất, cũ = "Chờ phê duyệt triển khai"). Web/app đọc
  nút từ BE nên tự theo. Test BE +2 ca → 31/31. App: màn 457 chỉ còn [Gửi duyệt triển khai].
- [x] Commit + push: hrm-api `d80c68dd8`, hrm-client `4b347f17b` (gop_db); TPE_APP `17d29d7` (develop).
Đang làm dở: —
Bước tiếp theo: deploy nhớ chạy migration task_extension_requests; data demo 456–458 user chốt GIỮ.
Blocked:

### Checkpoint — 08/11/2026 (wrap up)
Vừa hoàn thành:
- [x] App: phân hệ Công việc lên đầu màn chọn phân hệ + bảng Chuyển phân hệ (`custom_view/module_switcher.dart`,
  nguồn chung 2 nơi) — kiểm simulator, push TPE_APP develop `9fa648e`.
- Code đã push hết: hrm-api `d80c68dd8`, hrm-client `4b347f17b` (gop_db); TPE_APP `9fa648e` (develop).
Đang làm dở: hướng dẫn build bản app mới — user dừng ở câu hỏi chọn app/nền tảng.
  Đã kiểm máy: fvm 3.41.7 OK; 1 chứng chỉ ký iOS; THIẾU `~/.asc_api.env`, `~/.asc_pw`, keystore `~/.keystores/tanphat.jks`.
  Version hiện tại: tpeDev 2.2.6 (162) · tpeProd 2.3.8 (104); nhánh `tpe` thiếu 7 commit so với develop.
  Skill `app-build-release` không có trên đĩa (chỉ còn trong git hrm-claude-config commit 54b72f2).
Bước tiếp theo: hỏi lại app cần build — tpeDev (develop, server dev, chỉ iOS) hay tpeProd (merge develop→tpe; prod CHƯA deploy
  API Nhiệm vụ v2 + migration task_extension_requests ⇒ phải deploy API trước) — rồi hướng dẫn từng bước: bump version
  (xcconfig + build.gradle) → pub get → pod install → make fix_pod_release → make build_<flavor>_ipa → upload (hỏi trước).
Blocked: chờ user chọn app / nền tảng.
