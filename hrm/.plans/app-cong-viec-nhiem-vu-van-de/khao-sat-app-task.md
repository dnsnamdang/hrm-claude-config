# Khảo sát phần Task trên app TPE_APP (hiện trạng trước khi thiết kế "Nhiệm vụ / Vấn đề")

- Repo: `TPE_APP` · nhánh `develop` · commit `8f6adfa` (App 2.2.6 (156)).
- Gốc đường dẫn bên dưới: `TPE_APP/app/lib/`. Chỉ đọc code, không chạy app.
- Mọi kết luận có `file:dòng`. Phần "Nhận xét" (mục 7) là đánh giá dựa trên code, có ghi rõ căn cứ.

## Mục lục

1. [Cấu trúc điều hướng](#1-cấu-trúc-điều-hướng)
2. [Từng màn](#2-từng-màn)
   - 2.1 [Danh sách Task](#21-danh-sách-task--uitasktask_list_pagedart)
   - 2.2 [Chi tiết Task](#22-chi-tiết-task--uitasktask_detail_pagedart)
   - 2.3 [Bình luận Task](#23-bình-luận-task--uitasktask_comments_pagedart)
   - 2.4 [Cập nhật / Báo cáo tiến độ task](#24-cập-nhật--báo-cáo-tiến-độ-task--uibao_cao_tien_do_taskbao_cao_tien_do_task_pagedart)
   - 2.5 [Việc của tôi (Mytodo) — chỗ chạm Task/Vấn đề](#25-việc-của-tôi-mytodo--chỗ-chạm-taskvấn-đề)
3. [Trạng thái, màu, ưu tiên, bộ lọc](#3-trạng-thái-màu-ưu-tiên-bộ-lọc)
4. [API app gọi](#4-api-app-gọi)
5. [Những gì app chưa có (thấy rõ từ code)](#5-những-gì-app-chưa-có-thấy-rõ-từ-code)
6. [Widget dùng chung có thể tái sử dụng](#6-widget-dùng-chung-có-thể-tái-sử-dụng)
7. [Nhận xét UX hiện trạng](#7-nhận-xét-ux-hiện-trạng)
8. ["Vấn đề" (issue) trên app hiện nay](#8-vấn-đề-issue-trên-app-hiện-nay)

---

## 1. Cấu trúc điều hướng

### 1.1 Khung phân hệ Công việc — `ui/module_shell/module_shell_pages.dart`

`CongViecShellPage` (`:90`) dựng `ModuleShell` (4 tab + nút giữa + drawer):

| Vị trí | Nội dung | Dòng |
|---|---|---|
| Tab 1 | **Việc của tôi** → `MyTodoPage` | `:138` |
| Tab 2 | **Tasks** → `TaskListPage` | `:139-143` |
| Tab 3 | **Phiếu** → `ModuleHubPage(congViecPhieu)` | `:144-151` |
| Tab 4 | **Phê duyệt** → `ModuleHubPage(congViecPheDuyet)` | `:152-160` |
| Nút giữa (FAB) | "Tạo mới" → `showCongViecCreateMenu` (Nhắc việc cá nhân · Meeting · Phiếu giao việc chấm công · Phiếu đi công tác chấm công) | `:124-135`, `ui/my_todo/create_menu_sheet.dart:9-17` |
| Drawer CTA | "Tạo phiếu giao việc" | `:170-174` |
| Badge drawer | số task cần báo cáo hôm nay (`fetchDailyReportCount`) qua `BaoCaoTienDoTaskPage.badgeNotifier` | `:104-111`, `:162-164` |

Ghi chú dòng `:137`: "Tiến độ" đã bỏ khỏi tab (chốt 29/10/2026), chuyển vào menu trái.

### 1.2 Drawer — `ui/module_shell/module_menus.dart:218-232` (`congViecDrawerSections`)

- Nhóm không tiêu đề: `Việc của tôi` (tab 0) · `Tasks` (tab 1) · `Báo cáo tiến độ task` (push `BaoCaoTienDoTaskRoute`, có badge).
- Nhóm "Phiếu": `congViecPhieu(user)` (phiếu giao việc, đi công tác, …).
- Nhóm "Phê duyệt": `congViecPheDuyet(user)` (`:181-215`) — **không có mục duyệt task** (chỉ gia hạn/kết thúc sớm, giao công tác, thanh toán công tác phí).

### 1.3 Các lối vào màn Task

| Từ | Đến | Dòng |
|---|---|---|
| Tab "Tasks" | `TaskListPage` | `module_shell_pages.dart:142` |
| Dashboard nhân viên (drawer cũ khi ngoài khung) "Công việc của tôi › Tasks" | `TaskListRoute` | `ui/dashboard_nhan_vien/dashboard_nhan_vien_page.dart:98-103` |
| Dashboard nhân viên "Cập nhật tiến độ task" | `BaoCaoTienDoTaskRoute` | `dashboard_nhan_vien_page.dart:106-112` |
| Thẻ task trong danh sách | `TaskDetailPage(taskId, solutions, projects, modules)` (pushWidget) | `ui/task/task_list_page.dart:805-813` |
| Việc của tôi — bấm thẻ loại `task` | `TaskDetailRoute(taskId)` (KHÔNG truyền danh mục) | `ui/my_todo/my_todo_actions.dart:25-26` |
| Thông báo nhắc hạn `work_reminder.task` | `TaskDetailRoute(taskId)` | `my_todo_actions.dart:49-50` |
| Chi tiết task — nút 💬 trên app bar | `TaskCommentsPage(taskId, initialCount)` | `ui/task/task_detail_page.dart:135-143` |
| Thông báo `task_comment` / `task_comment_react` | `TaskCommentsPage(taskId, scrollToCommentId)` — vào thẳng bình luận, không qua chi tiết | `ui/notification/bloc/notification_bloc.dart:299-307` |
| Push `task-daily-report` | `BaoCaoTienDoTaskRoute` | `ui/app/bloc/app_bloc.dart:255-257` |
| Thông báo `task_progress_report_reminder` | `BaoCaoTienDoTaskRoute` | `notification_bloc.dart:322-323` |

Route khai báo: `navigation/routes/app_router.dart:145` (TaskListRoute), `:222` (TaskDetailRoute). `TaskCommentsPage` không có route, chỉ `pushWidget`.

Sơ đồ:

```
Công việc (shell)
├─ Tab Việc của tôi ──(thẻ task)──────────────► Chi tiết Task ──(💬)──► Bình luận
│                    └(thẻ issue)──► snackbar "Chi tiết vấn đề chưa có trên app…"
├─ Tab Tasks ──► Danh sách Task ──(thẻ)──────► Chi tiết Task ──(💬)──► Bình luận
├─ Drawer › Báo cáo tiến độ task ────────────► Cập nhật tiến độ task (không đi tiếp đâu)
└─ FAB Tạo mới (không có Task / Vấn đề)
Thông báo bình luận ─────────────────────────► Bình luận (bỏ qua chi tiết)
```

---

## 2. Từng màn

### 2.1 Danh sách Task — `ui/task/task_list_page.dart`

**Header**: `PrimaryAppBar(text: 'Danh sách Task')` (`:652-654`) — nằm trong shell nên nút trái là ☰ (`custom_view/module_shell.dart:38-39`).

**Dải lọc** (`ListFilterBar`, `:669-686`): ô tìm "Tìm theo mã, tên task" (debounce 400ms, `:671-676`) + nút lọc có số tiêu chí + chip tiêu chí đang bật (bấm thân chip mở lại đúng trường, ✕ bỏ) + "Xoá lọc".

**Hàng chip nhanh** (`:694-710`, cuộn ngang):
- `Quá hạn: N` (đỏ, chỉ hiển thị — không bấm được) (`:759-778`). N đếm trên `_tasks` **đã tải** (`:660`), không phải tổng server.
- 4 nút vai trò, chọn 1 hoặc bỏ (`:574-585`): `Tôi làm` (assignee_id=me) · `Tôi giao` (created_by=me) · `Tôi theo dõi` (watching_id=me) · `Tôi duyệt` (approver_id=me). Chưa chọn thì **chỉ hiện icon tròn 36px, không có chữ**; chọn rồi mới hiện nhãn (`:600-646`).

**Bảng lọc** (`showFilterSheet`, `:365-379`; trường ở `:216-291`) — ghi chú `:212-215` nói khớp web `my-job/components/TasksTab.vue`:
- Cơ bản: Trạng thái (picker 1) · Mức độ ưu tiên (chip 1) · Giải pháp · Dự án · Người thực hiện (avatar) · Ngày cập nhật (khoảng ngày).
- "Thêm tiêu chí" (`advanced: true`): Hạng mục/Module (lọc tầng theo Giải pháp, `:250-265`) · Người tạo · Người duyệt kết quả · Hạn hoàn thành · Tag (chọn nhiều).
- Nút "Xem N task" đếm bằng API `per_page=1` (`:334-363`).
- Danh mục nạp 1 lần lúc vào màn (4 API song song, `:133-204`); Người thực hiện/Người tạo/Người duyệt dùng chung 1 danh sách nhân viên (`:184-186`).

**Danh sách**: phân trang 10 dòng (`:55`), sort `created_at desc` (`:461-462`), cuộn gần cuối tự tải (`:388-396`), lỗi tải thêm → `AppDialog` "Tải thêm thất bại" (`:398-432`), dòng chữ "Kéo để tải thêm..." (`:746-750`), skeleton / lỗi / rỗng (`:713-744`).

**Thẻ task** (`_buildTaskCard`, `:780-927`), từ trên xuống:
1. Mã task (15 w700) + chip ưu tiên VIẾT HOA (`priorityLevel` BE hoặc map 1/2/3) (`:821-847`)
2. Tên task (`:849-851`)
3. `🕒 Hạn: dd/MM/yyyy` + nhãn `Quá hạn` (đỏ) hoặc `Còn N ngày` / `Còn trong ngày` (xanh) (`:853-887`)
4. Badge trạng thái (chữ BE `status_text`, màu bảng cục bộ) (`:889-893`, `:566-572`)
5. Tên giải pháp (`:895-896`)
6. Kẻ ngang + `👤 Người thực hiện` · `➤ Người duyệt` (`:898-922`)

**Hành động**: chỉ bấm thẻ → chi tiết. Không tạo, không vuốt, không menu ⋮, không đổi trạng thái.

### 2.2 Chi tiết Task — `ui/task/task_detail_page.dart`

**Header**: `PrimaryAppBar('Chi tiết Task')` + 1 nút `AppBarGlassButton` 💬 có badge đếm bình luận (đếm cả cây con) (`:127-164`, `:115-125`). Tải lại khi quay về từ màn con (`RouteObserver`, `:48-68`).

Dữ liệu: `fetchTaskById` → `Map<String,dynamic>` thô (`:84`), sau đó gọi thêm `fetchTaskComments` chỉ để đếm (`:102-113`).

**Các khối** (mỗi khối là `Card + ExpansionTile`, tất cả mở sẵn), thứ tự `:990-1294`:

| # | Khối | Nội dung | Dòng |
|---|---|---|---|
| 1 | Thông tin chung | Mã task · Tên task · Hạn hoàn thành (dải cam) · Trạng thái (badge) · Mức độ ưu tiên (chip) | `:578-670` |
| 2 | Giải pháp & Dự án | Mã-Tên giải pháp · Dự án · Hạng mục/Module (fallback qua danh mục truyền từ list) | `:1000-1023` |
| 3 | Nhân sự | Người thực hiện · Người duyệt · Người theo dõi | `:1024-1057` |
| 4 | Thời gian | Ngày bắt đầu · Hạn hoàn thành · Tạo lúc · Cập nhật (+ Số giờ được giao nếu status<4) | `:1058-1091` |
| 5 | Checklist | `x/y hoàn thành` + danh sách ô tick **chỉ xem** | `:1092-1146` |
| 6 | Task con | bảng 4 cột Tên/mã · Người làm · Hạn · Trạng thái — **không bấm được** | `:1147-1261` |
| 7 | Mô tả | text thuần `description` | `:1262-1268` |
| 8 | Tệp đính kèm | 2 tab "File đính kèm giao task" / "File kết quả thực hiện"; bảng STT · TÊN FILE · HÀNH ĐỘNG (chỉ nút Tải → mở bằng `OpenFile`) | `:205-403`, `:717-755` |
| 9 | Kết quả thực hiện (khi `estimated_hours != null` hoặc status ≥ 4) | status<4: chỉ Số giờ được giao. status≥4: Nhật ký tiến độ theo ngày (bảng Ngày · Giờ · % · Ghi chú, khi có `progress_report.is_active`) + Số giờ được giao / thực tế / Tiến độ % (thanh) + Kết quả tổng hợp | `:405-576`, `:902-919` |
| 10 | Thiết lập | Người duyệt kết quả · Người theo dõi · Thẻ (Tags) · Lặp lại (diễn giải `recurring`) · Báo cáo tiến độ (diễn giải `progress_report`) · Người tạo · Người cập nhật | `:1282-1294`, `:833-898` |

Có sẵn trang xem ảnh toàn màn `_DetailFullScreenImagePage` (`:1304-1333`) nhưng hàm mở nó đang `// ignore: unused_element` (`:703-715`).

**Hành động**: chỉ (a) mở bình luận, (b) tải/mở file. **Không có** sửa, xoá, đổi trạng thái, bắt đầu/tạm dừng/hoàn thành, duyệt/từ chối, nhập kết quả, tick checklist, thêm task con, đính kèm file. Model `RemoteTaskData` có cờ `can_edit/can_delete/can_import_result/can_approve` (`data/.../model/remote_task_data.dart:42-45`) nhưng UI không dùng (grep `canEdit|canApprove|canImportResult` trong `ui/` chỉ ra `task_comments_page` — biến nội bộ khác nghĩa).

### 2.3 Bình luận Task — `ui/task/task_comments_page.dart`

- Header `PrimaryAppBar('Bình luận (N)')` (`:1340-1343`). Mở từ chi tiết hoặc thẳng từ thông báo (có `scrollToCommentId` → cuộn + highlight, `:129-170`).
- Danh sách cây lồng nhiều cấp, thụt lề + vạch nối (`_IndentPainter`) (`:236-275`). Thẻ bình luận: avatar · tên · thời gian · nội dung (khối nền xám) · tệp đính kèm (ảnh xem toàn màn, file tải + mở) · tóm tắt reaction · hàng hành động (`:278-337`, `:388-461`).
- Hàng hành động (`:463-523`): `Trả lời` · `😊 Thả cảm xúc` (8 emoji `👍 ❤️ 😂 😮 😢 🎉 🔥 👏`, `:36`) · `Sửa` · `Xóa` — Sửa/Xóa chỉ khi `commentator_id == employee đang đăng nhập` (`:464-466`).
- Sửa = bottom sheet nhập lại text (`:784-950`); Xóa = hộp xác nhận (`:952-1000`).
- Ô soạn dưới đáy (`:1005-1147`): dải "Trả lời {tên}" có ✕ khi đang trả lời; nút 📎 → sheet 3 lựa chọn Thư viện ảnh / Chụp ảnh / Chọn file (`:1149-1214`); chip tệp đang chờ; ô "Viết bình luận..."; nút gửi.
- Bắt buộc có chữ — gửi chỉ tệp bị chặn "Vui lòng nhập nội dung bình luận." (`:714-718`).
- Không có @nhắc tên (grep `mention` không ra), không có định dạng giàu.
- Model nội bộ `TaskComment / TaskCommentReactor / TaskCommentAttachment` khai trong chính file (`:1384-1520`).

### 2.4 Cập nhật / Báo cáo tiến độ task — `ui/bao_cao_tien_do_task/bao_cao_tien_do_task_page.dart`

- Tên không thống nhất: drawer "Báo cáo tiến độ task" (`module_menus.dart:224`), app bar "Cập nhật tiến độ task" (`:445`), dashboard cũ "Cập nhật tiến độ task" (`dashboard_nhan_vien_page.dart:106`), hộp chưa lưu "Báo cáo tiến độ" (`:391`).
- Nguồn: `GET tasks/daily-report` — task IN_PROGRESS của user cần báo cáo hôm nay kèm `progress_rows` (`task_api_service.dart:275-285`).
- **Thẻ tổng hợp** (`:476-533`): "Hôm nay, dd/MM/yyyy" + nút mở/thu tất cả + 3 ô số: Tổng task · Chờ báo cáo · "Đã hoàn thành" (= số đã báo cáo hôm nay, `:481`).
- **Thẻ task** (`_TaskCard`, `:652+`; header `:780-888`): ▼ + mã + badge Đã/Chưa báo cáo · tên · dòng "Hạn báo cáo: HH:mm hôm nay" / "Đã báo cáo lúc HH:mm hôm nay" (lấy từ `task.dueTime`, `:812-833`) · chip trạng thái + ưu tiên + chu kỳ (Hàng ngày/tuần/tháng) · nút "Báo cáo" khi đang thu gọn và chưa báo cáo (`:861-880`).
- **Thân thẻ mở** (`:890-925`): thanh "Tiến độ tổng: x%" + bảng dòng tiến độ: các ngày đã qua có số · hôm nay/dòng sửa được (nhãn HÔM NAY / ĐÃ NỘP, ô Số giờ, Tiến độ %, Ghi chú) · 1 dòng tương lai (`:927-1060`).
- Kiểm tra (`validate`, `:146-166`): giờ 0–24, % 0–100, **tổng % các dòng ≤ 100**. Lỗi báo từng task một qua snackbar, dừng ở lỗi đầu (`:280-287`).
- **Footer** (`:584-650`): "N chưa báo cáo" + `Đóng` + `Lưu tất cả` (lưu lô `daily-report/save`, xử lý thành công một phần `:304-345`).
- Chặn thoát khi chưa lưu (`PopScope` + `showUnsavedChangesDialog`, `:389-430`).
- Rỗng: "Tất cả đã hoàn thành! — Không có task nào cần báo cáo hôm nay." (`:561-568`).
- Không bấm sang chi tiết task được (grep `TaskDetail` trong file không có).

### 2.5 Việc của tôi (Mytodo) — chỗ chạm Task/Vấn đề

- `ui/my_todo/widget/work_item_card.dart:15-25`: loại `task` hiển thị nhãn **"Nhiệm vụ"** (cam `#EA580C`, icon `check_box_outlined`); loại `issue` nhãn **"Vấn đề"** (đỏ hồng `#E11D48`, icon `bug_report_outlined`).
- Bộ lọc "Loại" của Mytodo liệt kê đủ `WorkType.all` gồm cả Vấn đề (`ui/my_todo/my_todo_list_view.dart:95-100`).
- Dữ liệu: `GET v1/assign/my-todo?type=&status=pending|done|all` và `GET v1/assign/my-todo/calendar` (`data/.../my_todo_api_service.dart:42-75`); model `WorkItem` (`data/.../model/work_item.dart`) — chữ + màu trạng thái/vai trò do BE quyết (`:5`, `statusColorOf` ở `work_item_card.dart:34-51`).
- Bấm thẻ `task` → `TaskDetailRoute` (`my_todo_actions.dart:25-26`); bấm `issue` rơi vào `default` → snackbar "Chi tiết vấn đề chưa có trên app, vui lòng xem trên web." (`:36-37`, `:59-60`).
- FAB "Tạo mới" ghi rõ: "Nhiệm vụ / Vấn đề / … app chưa có màn tạo → chưa đưa vào" (`create_menu_sheet.dart:12`).

---

## 3. Trạng thái, màu, ưu tiên, bộ lọc

### 3.1 Trạng thái task — `ui/task/task_status_helper.dart:6-53`

| id | Chữ | Chữ/icon | Nền chip |
|---|---|---|---|
| 1 | Nháp | `#9E9E9E` | `#F5F5F5` |
| 2 | Chờ phê duyệt triển khai | `#1565C0` | `#E3F2FD` |
| 3 | Chờ bắt đầu | `#1976D2` | `#E3F2FD` |
| 4 | Đang thực hiện | `#E65100` | `#FFF3E0` |
| 5 | Tạm dừng | `#FF6F00` | `#FFF8E1` |
| 6 | Hoàn thành - Chờ duyệt | `#00695C` | `#E0F2F1` |
| 7 | Từ chối kết quả | `#C62828` | `#FFEBEE` |
| 8 | Hoàn thành | `#2E7D32` | `#E8F5E9` |
| 9 | Hủy | `#B71C1C` | `#FFEBEE` |
| 10 | Từ chối triển khai | `#BF360C` | `#FBE9E7` |
| khác | `fallbackText` / "Không rõ" | `#616161` | `#F5F5F5` |

`kTaskStatusOptions` (`:67-78`) = 10 mục trên cho bộ lọc. Danh sách ưu tiên chữ BE `status_text`, chỉ lấy màu cục bộ (`task_list_page.dart:566-572`).

**Lệch bảng ở khối Task con** (`task_detail_page.dart:1197-1205`) dùng map riêng 7 mục: `2 = 'Chờ duyệt'`, `6 = 'Hoàn thành'`, `7 = 'Đã huỷ'` — trái nghĩa với bảng chuẩn (6 = Hoàn thành - Chờ duyệt, 7 = Từ chối kết quả, 8/9/10 không có → rơi về `status_text`).

Mytodo dùng màu BE kiểu Bootstrap (`success/primary/warning/danger/info` hoặc hex) → bảng màu khác hẳn (`work_item_card.dart:34-51`).

### 3.2 Mức độ ưu tiên — 3 bộ màu khác nhau

| Màn | Bình thường | Cao | Khẩn cấp | Dòng |
|---|---|---|---|---|
| Danh sách | `AppColors.priorityNormal*` | `priorityHigh*` | `priorityUrgent*` | `task_list_page.dart:789-798` |
| Chi tiết | `#29B24B` (xanh) | `#F5963C` | `#D60E0E` | `task_detail_page.dart:660` |
| Báo cáo tiến độ | `#64748B` (xám) | `#F97316` | `#EF4444` | `bao_cao_tien_do_task_page.dart:744-747` |

### 3.3 Bộ lọc — `ui/task/task_filter_option.dart`

Chỉ là class `FilterOption {id, text}` + `fromJson` dò nhãn theo thứ tự `fullname → name → text → tag → label → code`, ghép `code - name` khi có mã (`:21-56`). Dùng để chuyển danh mục API sang `FilterSheetOption` của `custom_view/filter_sheet.dart`. Danh sách trường lọc xem mục 2.1.

---

## 4. API app gọi

Tất cả trong `data/lib/src/repository/source/remote/api/api_services/app_server/task_api_service.dart` (client `authAppServerClient`, tiền tố `v1/assign/`).

| Method | Path | Tham số | Trả về | Dùng ở |
|---|---|---|---|---|
| GET | `solutions/getAll` | `per_page=100000` | list Map (`id, name, code, modules[]{id,name,code}`) | Lọc Giải pháp + Module (`task_list_page.dart:141,147-170`) |
| GET | `prospective-projects/getAll` | `per_page=100000` | list Map | Lọc Dự án |
| GET | `tasks/employees` | `per_page=100000` | list Map (`id, fullname/name, code`) | Lọc Người thực hiện/tạo/duyệt |
| GET | `tasks/tags/getAll` | — | list Map | Lọc Tag |
| GET | `my-job/task-list` (`:48-98`) | `page, per_page, keyword, sort_field, sort_dir, status, assignee_id, created_by, watching_id, approver_id, solution_id, prospective_project_id, tags[], priority, solution_module_id, from_date, to_date, deadline_from, deadline_to` | `DataListResponse<RemoteTaskData>` (+ `meta.total`, `current_page/last_page`) | Danh sách + đếm nút "Xem N task" |
| GET | `tasks/{id}` (`fetchTaskById`, `:130-137`) | — | Map thô | Chi tiết |
| GET | `tasks/{id}/comments` | — | list Map cây (`children`) | Đếm + màn bình luận |
| POST | `tasks/{id}/comments` (multipart) | `comment, parent_id?, files[]` | Map | Gửi bình luận/trả lời |
| POST | `tasks/{id}/comments/{cid}/react` | `emoji` | Map | Thả cảm xúc |
| PUT | `tasks/{id}/comments/{cid}` | `comment, rate?` | Map | Sửa bình luận (`rate` app không gửi) |
| DELETE | `tasks/{id}/comments/{cid}` | — | Map | Xoá bình luận |
| GET | `tasks/daily-report` | — | list Map (`id, code, title, status, status_name, status_color, priority, priority_name, project_name, due_date, due_time, progress_pct, total_progress_pct, is_reported_today, report_rule{cycle_type…}, progress_rows[]{report_date, hours, progress_pct, note, is_today, is_past, is_future, is_editable}`) | Báo cáo tiến độ (`bao_cao…:117-136, 61-75`) |
| POST | `tasks/daily-report/save` | `tasks: [{task_id, progress_logs:[{report_date, hours, progress_pct, note}]}]` | Map `{success, errors[]{task_id, error}}` | Lưu tất cả |
| GET | `tasks/daily-report/count` | — | Map `{count}` | Badge drawer/dashboard |
| POST/DELETE | `fcm-tokens` | `token, device_info?` | Map | Đăng ký push nhắc báo cáo |

API khai báo nhưng **không màn nào gọi** (grep trong `ui/`): `fetchTaskDetail` (`my-job/task-list/{id}`), `fetchTaskDetailById` (`tasks/{id}` → model), legacy `tasks/report`, `tasks/{id}/report`, `tasks/report/batch` (`:100-128`, `:317-364`).

**Trường chi tiết `tasks/{id}` app đọc** (`task_detail_page.dart:815-978`): `code, title, start_date, due_date, due_time, status, status_text, priority, updated_at, created_at, recurring{is_active, repeat_type, repeat_interval, end_type, end_date, max_occurrences}, progress_report{is_active, cycle_type, send_time, week_days[]}, tags[], estimated_hours, actual_hours, progress_percent, result_text, progress_logs[]/daily_logs[], result_attachments[], watchers[], modules[], project{}, solution{}, assignee{}, approver{}, attachments[]/list_file[]/files[], checklists[]{title,is_done}, subtasks[]/children[], checklist_count, child_task, created_by_name, updated_by_name, solution_module_id, solution_code/_name, project_code/_name, solution_module_code/_name, approver_result_name, description`. Nhiều trường đọc theo kiểu "thử nhiều tên" (vd `progress_logs ?? daily_logs`, `attachments ?? list_file ?? files`) → hợp đồng API chưa chốt rõ.

**Model `RemoteTaskData`** (`data/.../model/remote_task_data.dart:8-46`): danh sách dùng `id, code, title, priority, priorityLevel, status, status_text, solution_name, assignee_name, approver_name, due_date, due_time`. Không dùng: `description, project_id, parent_id, solution_id/code, prospective_project_*, solution_employee_name, module_name, assignee_id, approver_id, projectPhases, created_by_name, updated_by_name, start_date, created_at, updated_at, checklists_number, children_number, linked_number, in_progress, can_edit, can_delete, can_import_result, can_approve`.

---

## 5. Những gì app chưa có (thấy rõ từ code)

| Thiếu | Căn cứ |
|---|---|
| Tạo Nhiệm vụ / Vấn đề | `create_menu_sheet.dart:12`; không có API POST `tasks` trong `task_api_service.dart` |
| Sửa / xoá task | Không có API PUT/DELETE `tasks/{id}`; cờ `can_edit/can_delete` không dùng |
| Đổi trạng thái (bắt đầu, tạm dừng, hoàn thành, huỷ, gửi duyệt) | Không có API; chi tiết không có nút nào |
| Duyệt triển khai / duyệt kết quả / từ chối | Không có API; cờ `can_approve` không dùng; drawer Phê duyệt không có mục task (`module_menus.dart:181-215`) |
| Nhập kết quả thực hiện (result_text, actual_hours, file kết quả) | Chỉ hiển thị (`task_detail_page.dart:405-576`); `can_import_result` không dùng. Tiến độ ngày chỉ nhập được ở màn Báo cáo tiến độ, và chỉ task IN_PROGRESS có lịch báo cáo |
| Tick checklist, thêm/sửa checklist | Chỉ icon tĩnh (`:1114-1140`) |
| Mở task con / task liên kết | Dòng task con không bấm được (`:1186-1255`); `linked_number` không dùng |
| Đính kèm file vào task (giao / kết quả) | Chỉ tải xuống |
| Xem ảnh đính kèm task trong app | Hàm có nhưng `unused_element` (`:703-715`) |
| @nhắc tên trong bình luận, gửi tệp không kèm chữ | `task_comments_page.dart:714-718`; không có `mention` |
| Toàn bộ "Vấn đề" | Xem mục 8 |
| Lọc nhanh "Quá hạn" | Chip quá hạn chỉ hiển thị, không bấm (`task_list_page.dart:759-778`) |
| Sắp xếp | Cố định `created_at desc` (`:461-462`) |

---

## 6. Widget dùng chung có thể tái sử dụng

| Nhu cầu | Widget / hàm | File |
|---|---|---|
| Khung phân hệ, tab, FAB | `ModuleShell`, `ModuleTab`, `ModuleFab` | `custom_view/module_shell.dart` |
| Drawer phân hệ | `ModuleDrawer`, `DrawerSection`, `DrawerEntry` | `custom_view/module_drawer.dart`, `ui/module_shell/module_menus.dart` |
| Màn hub nhiều mục | `ModuleHubPage` | `ui/module_shell/module_hub_page.dart` |
| Header | `PrimaryAppBar`, `AppBarGlassButton` | `custom_view/primary_app_bar.dart` |
| Ô tìm + nút lọc + chip tiêu chí | `ListFilterBar` | `custom_view/list_filter_bar.dart` |
| Bảng lọc 2 nấc (chip, khoảng ngày, dòng chọn ›, ô chữ, đếm "Xem N …") | `showFilterSheet`, `FilterChipsField`, `FilterDateRangeField`, `FilterPickerField`/`FilterPickerSection` (có `parentKey` lọc tầng, `avatar`), `FilterTextField`, `FilterValues`, `filterActiveChips` | `custom_view/filter_sheet.dart` |
| Rỗng / lỗi | `AppEmptyWidget(filtered:)`, `AppErrorWidget(onRetry:)` | `custom_view/app_empty_widget.dart` |
| Skeleton | `ContentSkeleton`, `ListFooterSkeleton` | `custom_view/skeleton.dart` |
| Thẻ | `AppCard` | `custom_view/app_card.dart` |
| Badge trạng thái | `StatusBadge` | `common_view/status_badge.dart` |
| Hộp thoại / xác nhận / chưa lưu | `AppDialog`, `showAppConfirm`, `showUnsavedChangesDialog`, `UnsavedChangesGuard` | `custom_view/app_dialog.dart`, `custom_view/unsaved_changes_guard.dart` |
| Nhập lý do (từ chối, huỷ, tạm dừng) | `ReasonInputDialog` | `custom_view/reason_input_dialog.dart` |
| Mục Duyệt/Từ chối trong sheet ⋮ | `approveActionTiles(canApprove, canReject)` | `custom_view/approve_action_tiles.dart` |
| Nút | `PrimaryButton`, `SecondaryButton` | `custom_view/primary_button.dart` |
| Đang tải | `AppSpinner`, `PageLoadingBar` | `common_view/common_progress_indicator.dart`, `custom_view/page_loading_bar.dart` |
| Đoạn chữ dài "Xem thêm" (mô tả) | `ExpandableText` | `custom_view/expandable_text.dart` |
| Chọn nhân sự kiểu mới (toàn trang, tìm, phân trang server, chọn 1/nhiều) | `MeetingEmployeePickerPage`; bản 1 người `pickEmployee()` | `ui/meeting/picker/meeting_employee_picker_page.dart`, `ui/chon_nv/employee_picker.dart` |
| Danh sách tìm có phân trang server (khuôn mọi màn chọn) | `MeetingSearchList<T>`, `SearchPage`, `MeetingSearchListController` | `ui/meeting/picker/meeting_search_list.dart` |
| Chọn dự án TKT | `MeetingProjectPickerPage` | `ui/meeting/picker/meeting_project_picker_page.dart` |
| Bộ thành phần form/xem (hub row, section, dòng xem, nhãn, lỗi, ô chọn, ô chữ, segmented, dòng người, thẻ nhóm, banner 3 màu, lỗi tải) | `MeetingHubRow`, `MeetingSection`, `MeetingViewRow`, `MeetingFieldLabel`, `MeetingFieldError`, `MeetingSelectRow`, `MeetingTextField`, `MeetingSegmented`, `MeetingPersonRow`, `MeetingGroupCard`, `MeetingBanner`, `MeetingLoadError` | `ui/meeting/widget/meeting_widgets.dart` |
| Soạn thảo giàu định dạng (HTML như CKEditor web) — cho Mô tả | `MeetingRichEditor` | `ui/meeting/widget/meeting_rich_editor.dart` |
| Xem / tải tệp đính kèm (ảnh xem trong app, file mở bằng OS, chia sẻ) | `MeetingFileActions` | `ui/meeting/widget/meeting_file_actions.dart` |
| Thẻ việc đa loại + nhãn/màu loại (Nhiệm vụ, Vấn đề…) | `WorkType`, `statusColorOf`, thẻ trong `work_item_card.dart` | `ui/my_todo/widget/work_item_card.dart` |
| Sheet "Tạo mới" (chỗ thêm Nhiệm vụ / Vấn đề) | `showCongViecCreateMenu` | `ui/my_todo/create_menu_sheet.dart` |
| Bình luận cây + reaction + đính kèm | toàn bộ `TaskCommentsPage` (đang gắn cứng `tasks/{id}/comments`) | `ui/task/task_comments_page.dart` |

---

## 7. Nhận xét UX hiện trạng

Dựa trên code, chưa đối chiếu trên máy thật.

**Điều hướng & đặt tên**
1. Cùng một thứ có 3 tên: tab/drawer "Tasks", app bar "Danh sách Task"/"Chi tiết Task" (tiếng Anh lẫn Việt) và Mytodo "Nhiệm vụ" (`work_item_card.dart:16`). Màn báo cáo cũng 3 tên (mục 2.4).
2. Thông báo bình luận nhảy thẳng vào màn Bình luận (`notification_bloc.dart:302`); từ đó không có lối sang chi tiết task (màn bình luận không có nút xem task).
3. Màn Báo cáo tiến độ không mở được chi tiết task; chi tiết task không có lối "Báo cáo tiến độ" → 2 màn rời nhau dù cùng một task.
4. Mở chi tiết từ Mytodo/thông báo không truyền danh mục module (`my_todo_actions.dart:26`) → Hạng mục/Module rơi về đường fallback (`task_detail_page.dart:964-978`); kết quả có thể khác khi mở từ danh sách.

**Danh sách**
5. Hàng lọc nhanh có 4 nút vai trò chỉ là icon khi chưa chọn (`task_list_page.dart:631-641`) — người dùng phải đoán nghĩa icon; trong khi bộ lọc lớn lại có Người thực hiện/Người tạo/Người duyệt trùng chức năng → 2 cơ chế lọc người chồng nhau (`:346-349` gộp bằng `??`, chọn ở bảng lọc đè chip vai trò im lặng).
6. "Quá hạn: N" đếm trên số dòng đã tải (10/trang, `:660`) nên số thay đổi khi cuộn; tính cả task đã Hoàn thành/Huỷ vì `_isTaskOverdue` không xét trạng thái (`:549-553`); chip không bấm lọc được.
7. Thẻ 6 tầng thông tin (mã+ưu tiên / tên / hạn+nhãn còn-quá hạn / badge trạng thái / giải pháp / người làm·người duyệt) — trạng thái nằm riêng 1 dòng, giải pháp rỗng vẫn chiếm dòng (`:895-896` không kiểm rỗng). Mã đứng trên tên (ngược khuôn Meeting "tên trước mã", `meeting_card.dart:7-8`).
8. Ưu tiên "BÌNH THƯỜNG" vẫn hiện chip ở mọi thẻ → nhiễu; nhãn viết hoa toàn bộ.
9. Dòng chữ "Kéo để tải thêm..." luôn hiện ở đáy khi còn trang (`:746-750`) trong khi đã có tự tải khi cuộn.

**Chi tiết**
10. 10 khối `ExpansionTile` mở sẵn hết, cuộn rất dài; thứ tự đặt Mô tả và Tệp ở gần cuối, sau Checklist/Task con.
11. Lặp dữ liệu: Hạn hoàn thành ở "Thông tin chung" và "Thời gian"; Người duyệt ở "Nhân sự" và "Người duyệt kết quả" ở "Thiết lập"; Người theo dõi ở cả "Nhân sự" và "Thiết lập" (`:1055`, `:1287`).
12. Dùng bảng kiểu web trên mobile: Task con 4 cột (`:1170-1184`), Nhật ký tiến độ 4 cột (`:460-471`), Tệp đính kèm có header "STT · TÊN FILE · HÀNH ĐỘNG" (`:295-309`) — chật ở màn hẹp; tên file bọc trong ô viền giống input + dòng "Đã chọn: …" (chữ của form upload, `:355-366`).
13. Màu trạng thái task con dùng bảng riêng sai nghĩa (mục 3.1) → task con "Hoàn thành - Chờ duyệt" hiện "Hoàn thành", "Từ chối kết quả" hiện "Đã huỷ".
14. Màu ưu tiên 3 màn 3 kiểu (mục 3.2); "Bình thường" xanh lá ở chi tiết nhưng xám ở báo cáo.
15. Mô tả hiện text thuần (`:1266`) — nếu web lưu HTML (CKEditor) sẽ lộ thẻ; cần kiểm dữ liệu thật.
16. Không có thanh hành động nào; người dùng không biết mình được làm gì với task (dù BE đã trả cờ `can_*`).

**Bình luận**
17. Hàng hành động 4 chữ màu khác nhau (xanh phân hệ / xám / cam / đỏ, `:470-511`) trên mọi bình luận, kể cả reply lồng sâu → rối; Sửa/Xóa nên vào menu nhấn giữ hoặc ⋮.
18. Thụt lề tăng theo độ sâu không giới hạn (`depth * _indentSpacing`, `:245`) → reply sâu bị ép hẹp.
19. Không gửi được ảnh không kèm chữ (`:714-718`) — bất tiện khi chụp hiện trường.

**Báo cáo tiến độ**
20. Dòng "Hạn báo cáo: HH:mm hôm nay" / "Đã báo cáo lúc HH:mm" đều lấy `task.dueTime` (`:812-833`) — giờ hạn của task, không phải giờ báo cáo (`report_rule.send_time`) hay giờ đã nộp; "Đã báo cáo lúc" hiển thị giờ sai nghĩa.
21. Ô thống kê "Đã hoàn thành x/y" thực ra là "đã báo cáo hôm nay" (`:481`, `:527`) — dễ hiểu nhầm là task hoàn thành.
22. Lỗi kiểm tra chỉ báo task đầu tiên bằng snackbar rồi dừng (`:280-287`) — trái quy ước "báo lỗi đồng thời mọi ô".

---

## 8. "Vấn đề" (issue) trên app hiện nay

Kết quả grep `issue|vấn đề|van_de` trong `app/lib` (bỏ file sinh mã):

| Chỗ | Nội dung |
|---|---|
| `ui/my_todo/widget/work_item_card.dart:17` | `WorkType('issue', 'Vấn đề', Icons.bug_report_outlined, Color(0xFFE11D48))` |
| `ui/my_todo/my_todo_actions.dart:36-37`, `:59-60` | Bấm việc loại `issue` (từ danh sách hoặc thông báo nhắc hạn) → snackbar "Chi tiết vấn đề chưa có trên app, vui lòng xem trên web." |
| `ui/my_todo/create_menu_sheet.dart:12` | Ghi chú: Nhiệm vụ / Vấn đề chưa có màn tạo |
| `data/.../my_todo_api_service.dart:42` | `fetchItems(type: 'issue')` hợp lệ — Mytodo đã nhận được việc loại issue từ BE |
| `data/.../model/work_item.dart:4` | Liệt kê 6 loại có `issue` |
| `ui/notification/notification_template.dart:61` | Thông báo có từ khoá `issue` được xếp chung nhóm biểu tượng với task/job/… (chỉ chọn icon) |

Kết luận: app **chưa có** màn danh sách, chi tiết, tạo, bình luận nào cho Vấn đề; chưa có API service/model riêng cho issue. Vấn đề chỉ xuất hiện như một dòng trong "Việc của tôi" và bấm vào là báo xem trên web.
