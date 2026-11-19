# Phương án vá #6 (xem Nhiệm vụ) + #17 (xem Vấn đề) — 11/11/2026, CHỜ USER DUYỆT, CHƯA CODE

## Quyết định đã chốt
- (11/11) Câu 1 — cách bật chặn: **chạy "chỉ ghi log" trước** (~1 tuần prod TPE, đọc log), rồi mới bật 403.
- (11/11) Câu 2 — trưởng đơn vị xử lý vấn đề: **cho xem ở màn CHI TIẾT** (thêm nhánh `Issue::canView`: vấn đề chưa có người xử lý, người xem là trưởng bộ phận xử lý / trưởng phòng xử lý — cùng cách xác định với `notifyHandlingDepartmentLead`). Màn danh sách GIỮ NGUYÊN.
- (11/11) Câu 3 — phiếu bàn giao (#18): **để đợt sau**. Đợt này chỉ #6 + #17, nhánh bàn giao HẸP (người tạo phiếu / người bàn giao / người nhận việc / quản lý phòng của phiếu).
- Tự chốt (kỹ thuật, theo khuôn có sẵn): nhánh (b) meeting dùng `Meeting::canView()`; nhánh (d) báo cáo bám đúng điều kiện drill của `EmployeeWorkPerformanceService` (khuôn `Meeting::canViewByEmployeeWorkPerformanceReport`), đọc lại drill trước khi viết; app mobile xử lý 403 là việc TPE_APP riêng, hỏi sau.

## 1. Hiện trạng (đã kiểm)
| API | Kiểm quyền | Tái hiện |
|---|---|---|
| `GET assign/tasks/{task}` → `TaskController::show` (`Modules/Assign/Http/Controllers/Api/V1/TaskController.php:156`) | Không có (route không middleware, chỉ route-model binding) | NV 39 (danh sách task 0 dòng) đọc task 532 ⇒ 200 |
| `GET assign/issues/{issue}` → `IssueController::show` (`IssueController.php:78`) | Không có, `Issue` không global scope | NV 39 (danh sách vấn đề 0 dòng) đọc vấn đề tạm 345 ⇒ 200 |
| `GET assign/handovers/{handover}` → `HandoverService::show` (`:736`) | Không thấy kiểm (đọc code + route) | **Chưa gọi thử** — DB local không có phiếu bàn giao. Ứng viên #18 |
| `GET assign/handovers` → `HandoverService::index` (`:62`) | Chỉ ẩn nháp người khác, KHÔNG lọc quyền / phạm vi (route không middleware) ⇒ ai cũng thấy mọi phiếu + danh sách việc trong phiếu | Đọc code (11/11); `pending` lọc phòng quản lý + chờ duyệt (`:135`), `receiving` lọc `receiver_id` = mình (`:265`) |

Hai màn danh sách đã có phạm vi đầy đủ (dùng lại được):
- Task: `TaskService::index` = luật nháp (nháp chỉ người tạo) + `applyPermissionScope` (`TaskService.php:190`): phạm vi 4 xem hết; tầng 1 = 5 vai trò (tạo / làm / duyệt / theo dõi / duyệt triển khai theo phòng quản lý) + cha↔con; tầng 2 = thành viên giải pháp / dự án; tầng 3 = `task_org_units` theo phạm vi 1–3.
- Issue: `IssueService::index` → `applyPermissionScope` (`IssueService.php:161`): 6 vai trò (tạo / phát hiện / xử lý / duyệt / theo dõi / phối hợp) + tầng 2 + tầng 3 `issue_org_units`.

## 2. Ai đang mở panel chi tiết NGOÀI phạm vi danh sách (vá ẩu sẽ chặn nhầm)
FE gọi chi tiết ở: TaskPanel (21 màn), `CreateIssueModal` (13 màn), app mobile (`work_task_detail_page.dart`, `work_issue_detail_page.dart`…), link thông báo `?open_task=` / `?open_issue=`.
Nhóm có thể KHÔNG nằm trong phạm vi danh sách:
1. **Báo cáo kế hoạch & kết quả làm việc theo NV** — `WorkDrillModal.vue:822` mở task + vấn đề cho người chỉ có quyền báo cáo (phạm vi `EmployeeWorkPerformanceService::applyEmployeeScope`). Meeting đã có nhánh tương tự `Meeting::canViewByEmployeeWorkPerformanceReport`.
2. **Biên bản meeting** — `MeetingReport.vue:1175` mở việc giao từ biên bản cho người xem được meeting (thành phần họp chưa chắc giữ vai trò nào của task).
3. **Bàn giao công việc** — `handover/_id/index.vue:152`, `receive.vue:133` mở task + vấn đề trong phiếu cho người duyệt / người nhận.
4. **Trưởng đơn vị xử lý vấn đề** (đã kiểm 11/11): vấn đề giao cho phòng/bộ phận, chưa có người xử lý ⇒ `IssueService::notifyHandlingDepartmentLead` (`:695`) báo cho `parts.part_lead_id` (không có thì `departments.department_lead_id`). `syncIssueOrgUnits` (`:250`) có ghi phòng/bộ phận xử lý vào `issue_org_units` ⇒ chỉ ai có quyền danh sách vấn đề theo phòng/bộ phận mới thấy. Trưởng đơn vị KHÔNG có quyền đó ⇒ nhận thông báo nhưng danh sách không có, sau khi vá sẽ 403. Các màn giải pháp / hạng mục: thành viên ⇒ tầng 2 đã phủ.

Agent (`/agent`) không thêm nhóm mới: công cụ đã lọc theo đúng `TaskService::index` / `IssueService::index` / MyTodo (việc của chính mình).

## 3. Thiết kế đề xuất
**BE (hrm-api)**
- `TaskService` / `IssueService`: tách phần phạm vi thành hàm public dùng chung (`applyListScope($query)` = luật nháp + `applyPermissionScope`), `index` gọi lại hàm đó ⇒ danh sách KHÔNG đổi hành vi.
- `Task::canView()` = một trong: (a) lọt `applyListScope` cho đúng id · (b) task từ meeting (`meeting_id`) và `Meeting::canView()` · (c) task nằm trong phiếu bàn giao mà người xem là người tạo phiếu / người bàn giao / người nhận việc đó / quản lý phòng của phiếu (khớp `pending`) — KHÔNG lấy "ai xem được phiếu" vì danh sách phiếu đang mở cho mọi người · (d) phạm vi báo cáo hiệu suất NV (theo đúng cách drill lọc — cần đọc lại drill trước khi viết).
- `Issue::canView()` = (a) + (c) + (d) (+ nhánh phòng xử lý nếu mục 2.4 cho thấy cần).
- `TaskController::show`, `IssueController::show`: `canView()` false ⇒ 403 "Bạn không có quyền xem nhiệm vụ / vấn đề này!" (khuôn `MeetingController::show`).
- Rà thêm các route GET con đọc dữ liệu task/issue theo id (bình luận, lịch sử, tệp, nhật ký tiến độ…) — cùng lỗ, gắn cùng kiểm tra.

**Triển khai an toàn (đề xuất)**: bước 1 **chỉ ghi log** — `canView()` false thì ghi `Log::warning` (người xem, id, route, referer) nhưng vẫn trả 200; lên prod TPE ~1 tuần, đọc log tìm ca hợp lệ bị sót; bước 2 mới bật chặn 403. Lý do: 21 + 13 màn web + app mobile + link thông báo, khó phủ hết bằng đọc code.

**FE (hrm-client)**: `CreateIssueModal::fetchIssueDetail` lỗi ⇒ hiện tại toast nhưng popup vẫn mở form trống ⇒ sửa: đóng popup (TaskPanel đã tự đóng). App mobile: kiểm 403 ở 2 trang chi tiết hiện thông báo đúng (việc TPE_APP — hỏi riêng).

**Kiểm**: PHPUnit có quyền / không quyền cho từng nhánh (a)–(d) + danh sách không đổi; e2e: NV thường bị chặn (và popup vấn đề đóng), các luồng hợp lệ (Agent, biên bản meeting, bàn giao, báo cáo drill, thông báo) vẫn mở được.

**Phạm vi code dự kiến**: hrm-api — `Task.php`, `Issue.php`, `TaskService.php`, `IssueService.php`, `TaskController.php`, `IssueController.php` (+ route con nếu có). hrm-client — `CreateIssueModal.vue`. Không migration, không quyền mới. Nhánh riêng tách từ `origin/gop_db` (không phụ thuộc nhánh Agent).
