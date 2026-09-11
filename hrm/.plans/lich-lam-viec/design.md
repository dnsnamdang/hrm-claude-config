# Spec — Đổi tab "Lịch meeting" thành "Lịch làm việc" (6 loại công việc)

- **Feature**: `lich-lam-viec`
- **Ngày**: 2026-09-10
- **Người phụ trách**: @dnsnamdang
- **Branch**: `feature/lich-lam-viec`, tách từ `tpe` (cả `hrm-api` + `hrm-client`)
- **Màn đích**: `hrm-client/pages/assign/my-todo/index.vue`, tab thứ 2
- **Mockup nguồn**: `.plans/gop-db/ke-hoach-phat-trien-thi-truong/ke-hoach-phat-trien-thi-truong-mockup.html`
  (bản 09/08/2026, tiêu đề "Lịch công việc" — KHÔNG phải `...-mockup-meeting.html` vốn là mockup của bản chỉ-meeting đang chạy)
- **Feature tiền nhiệm**: `lich-meeting-tab` (`.plans/lich-meeting-tab/` + `docs/superpowers/specs/2026-08-14-lich-meeting-tab-design.md`) — design này thay thế phần lịch của nó

---

## 1. Mục tiêu & scope

Tab lịch hiện chỉ hiện **meeting**. Đổi thành lịch làm việc tổng hợp **6 loại**, giữ nguyên bố cục Tháng/Tuần đã có.

**Trong scope**

- Đổi nhãn tab `📅 Lịch meeting` → `📅 Lịch làm việc`.
- Lịch hiển thị 6 loại: Phiếu công tác · Phiếu giao việc · Meeting · Task · Issue · Nhắc việc cá nhân.
- Endpoint BE mới `GET assign/my-todo/calendar` gom 6 nguồn, lọc overlap theo khoảng ngày ở tầng DB.
- Thẻ tô **màu theo LOẠI**, kèm **chấm + chữ trạng thái thật** của loại đó.
- Việc kéo dài nhiều ngày vẽ thành **thanh trải ngang** theo khoảng thật của từng loại.
- Thanh tóm tắt đổi ngữ cảnh: chưa lọc loại → đếm theo 6 loại; đã chọn 1 loại → tách theo bộ trạng thái thật của loại đó.
- Lọc bằng **6 chip bật/tắt theo loại**; ô "Trạng thái" đổ động theo loại đang chọn.
- Bấm thẻ: drawer cho 3 loại phiếu, popup sẵn có cho 3 loại còn lại (mục 8.4).
- Đổi tên các component không còn chỉ phục vụ meeting (mục 8.5) + sửa e2e theo tên mới.

**Ngoài scope**

- Tab `✅ Công việc của tôi`: **không sửa gì** bên trong — kể cả `MyTodoService::getAll()`.
- Menu sidebar giữ nguyên nhãn "Lịch làm việc của tôi" và URL `/assign/my-todo`.
- Bộ lọc **Thị trường** trong mockup: **KHÔNG làm** (giữ quyết định đã chốt ở feature tiền nhiệm — phạm vi màn là "việc của tôi", không phải báo cáo).
- Tạo việc mới trực tiếp từ ô lịch.
- Kéo–thả đổi ngày trên lịch.
- Responsive/mobile (hoãn, như feature tiền nhiệm).

---

## 2. Phạm vi "việc của tôi" — theo từng loại

Giữ **đúng** định nghĩa mà tab danh sách đang dùng (`MyTodoService`), để hai tab không bao giờ lệch nhau. Phần này tách thành helper dùng chung, không chép lại.

| Loại | `type` | Điều kiện thuộc về tôi | Nguồn hiện có |
|---|---|---|---|
| Task | `task` | `assignee_id = auth id` | `getAssignedTasks()` |
| Issue | `issue` | `assignee_id = auth id` | `getAssignedIssues()` |
| Phiếu giao việc | `assign_job` | có trong `employees` theo `employee_info_id` | `getAssignJobs()` |
| Phiếu công tác | `assign_business` | `type = PHIEU_CONG_TAC (2)` và có trong `employees` theo `employee_id` | `getAssignBusinesses()` |
| Meeting | `meeting` | có tên trong **Thành phần — Phía Công ty** | `MeetingCalendarCriteria` |
| Nhắc việc cá nhân | `personal` | `user_id = auth id`, `parent_id IS NULL` | `getPersonalTodosNormalized()` |

**Meeting dùng `MeetingCalendarCriteria`, KHÔNG dùng `MyTodoService::getMeetings()`.** Hai chỗ này hiện khác nhau: `getMeetings()` lọc thêm `status IN (LEN_LICH, CHOT_LICH)`, còn lịch phải hiện đủ 5 trạng thái. Quyết định "chỉ xét Thành phần phía Công ty, không xét chủ trì, không xét người tạo" đã chốt ở Phase 9 của feature tiền nhiệm — giữ nguyên.

---

## 3. Phạm vi trạng thái — hiện HẾT

Lịch **không lọc bỏ trạng thái nào**, kể cả việc đã xong / đã huỷ / chưa duyệt. Đây là **khác biệt có chủ ý** so với tab danh sách (tab đó loại bỏ task `DRAFT/DONE/CANCELLED`, issue `closed/completed/rejected`, phiếu giao việc ngoài `DA_DUYET`, phiếu công tác ngoài `DA_LAP_PHIEU_CONG_TAC`).

Lý do: lịch dùng để nhìn lại cả quá khứ; mockup cũng hiện thẻ "Đang tạo", "Chờ duyệt", "Không duyệt", "Huỷ". Việc đã kết thúc được **làm mờ** thay vì ẩn (mục 6).

---

## 4. Mô hình dữ liệu — item chuẩn hoá

Mọi loại trả về cùng một shape:

```
type            'task' | 'issue' | 'assign_job' | 'assign_business' | 'meeting' | 'personal'
id              int
code            string|null      mã phiếu (task/giao việc/công tác/meeting), null với issue/personal
title           string
subtitle        string|null      khách hàng / dự án / danh sách — dòng phụ trên thẻ
start           'Y-m-d H:i:s'
end             'Y-m-d H:i:s'
all_day         bool             true khi loại/bản ghi không có giờ
status          int|string       giá trị thật của loại (int, riêng issue là string)
status_text     string           nhãn tiếng Việt thật của loại
status_group    'todo' | 'doing' | 'done' | 'stopped'
is_overdue      bool
url             string|null      trang chi tiết đầy đủ
```

`subtitle` lấy đúng cột thật của từng loại:

| Loại | `subtitle` | `code` |
|---|---|---|
| Phiếu công tác | `customer_name` | `code` |
| Phiếu giao việc | `customer_name`, rỗng thì `place` | `code` |
| Meeting | `customer_name` | `code` |
| Task | tên giải pháp (`solution.name`) | `code` |
| Issue | tên giải pháp theo `solution_id`, không có thì `null` | `null` |
| Nhắc việc cá nhân | tên danh sách chứa nó | `null` |

`code`, `url`, `status_text` lấy lại từ `MyTodoService` (`getTitle` / `getUrl` / `getStatusText`) — bổ sung, không viết lại.

---

## 5. Khoảng thời gian & cách đặt lên lưới

| Loại | start | end | all_day khi |
|---|---|---|---|
| Phiếu công tác | `from_time` | `to_time` (thiếu → `from_time`) | không có phần giờ |
| Phiếu giao việc | `time_start_request` | `deadline` (thiếu → start) | không có phần giờ |
| Meeting | `start_date` | `end_date` (thiếu → `start_date`) | không có phần giờ |
| Task | `start_date` (thiếu → `due_date`) | `due_date` | `due_time` rỗng |
| Issue | `due_date` ?? `deadline` | như start (1 ngày) | `due_time` rỗng |
| Nhắc việc cá nhân | `due_date` | như start (1 ngày) | `due_time` rỗng |

**Quy tắc bắt buộc**

- **Không xác định được `start` → item bị loại khỏi lịch.** Task/Issue/Nhắc việc chưa đặt hạn sẽ không lên lưới (người dùng xem chúng ở nhóm "KHÔNG HẠN" của tab danh sách). Không hiện khay phụ, không đếm vào thanh tóm tắt.
- `end < start` (dữ liệu bẩn) → coi `end = start`, không để vẽ thanh âm.
- **Cách xác định `all_day`**:
  - Task · Issue · Nhắc việc cá nhân → `due_time` rỗng.
  - Phiếu công tác · Phiếu giao việc · Meeting (cột `dateTime`) → phần giờ của **cả** `start` và `end` đều là `00:00:00`.
- `all_day = true` → lưới Tuần đặt vào **hàng "Cả ngày"** đã có sẵn (`WeekGrid.vue:31`); lưới Tháng vẽ như thẻ thường.
- `start` khác ngày `end` → vẽ **thanh nhiều ngày**, tái dùng nguyên `calendar-lanes.js` (đã xử lý lane + cắt đoạn theo tuần + mũi tên tràn).
- Truy vấn theo **overlap**: `start <= to_date AND end >= from_date` — không phải `start BETWEEN`, nếu không việc bắt đầu trước kỳ sẽ biến mất khỏi lưới.

---

## 6. Màu theo loại + nhóm trạng thái

### 6.1 Màu loại

| Loại | Token | Hex | Nguồn |
|---|---|---|---|
| Phiếu công tác | `--type-cong_tac` | `#0d9488` | mockup |
| Meeting | `--type-meeting` | `#4f46e5` | mockup |
| Task | `--type-task` | `#ea580c` | mockup |
| Issue | `--type-issue` | `#e11d48` | mới |
| Phiếu giao việc | `--type-giao_viec` | `#ca8a04` | mới |
| Nhắc việc cá nhân | `--type-personal` | `#64748b` | mới |

Nền/viền thẻ theo đúng công thức mockup đang dùng: nền `alpha 0.13`, viền `alpha 0.38`. Mỗi loại có **icon riêng** để không phân biệt chỉ bằng màu.

### 6.2 Gộp 6 bộ trạng thái về 4 nhóm

Thẻ luôn hiện **chữ trạng thái thật**; nhóm chỉ quyết định màu chấm + làm mờ.

| Nhóm | Màu chấm | Hiệu ứng | Thành viên |
|---|---|---|---|
| `todo` Chưa bắt đầu | `#94a3b8` | — | Task 1 Nháp, 2 Chờ duyệt, 3 Cần làm · Issue `new`, `assigned` · Giao việc 1 Đang tạo, 2 Chờ duyệt · Công tác 1 Đang tạo, 2 Chờ duyệt · Meeting 0 Đang tạo, 1 Lên lịch · Cá nhân chưa xong |
| `doing` Đang chạy | `#3b82f6` | — | Task 4 Đang làm, 6 Review · Issue `in_progress`, `reopened` · Giao việc 3 Đã duyệt, 5 Đã nhập KQ · Công tác 3 Đã duyệt, 4 Đã lập phiếu CT, 5 Đã nhập KQ · Meeting 2 Chốt lịch |
| `done` Đã xong | `#22c55e` | **mờ** | Task 8 Hoàn thành · Issue `resolved`, `completed`, `closed` · Giao việc 6 Đã duyệt KQ · Công tác 7 Đã duyệt KQ · Meeting 3 Hoàn thành · Cá nhân đã xong |
| `stopped` Dừng · Huỷ | `#ef4444` | **mờ**, gạch ngang tiêu đề (trừ Tạm dừng) | Task 5 Tạm dừng, 7 Từ chối, 9 Huỷ, 10 Từ chối bắt đầu · Issue `rejected` · Giao việc 4 Từ chối · Công tác 6 Không duyệt · Meeting 4 Hủy |

Bảng gộp đặt ở **BE** (`status_group` trả sẵn) để FE không phải biết 6 bộ trạng thái.

Phân biệt trong nhóm `stopped`: **gạch ngang tiêu đề** chỉ áp cho việc đã kết thúc hẳn (Huỷ · Từ chối · Từ chối bắt đầu · Không duyệt). Task **Tạm dừng** chỉ làm mờ, KHÔNG gạch ngang — vì nó còn có thể chạy tiếp.

### 6.3 Quá hạn

`is_overdue = true` khi `end < hôm nay` **và** `status_group ∈ {todo, doing}`. Thẻ hiện badge đỏ "Quá hạn" như mockup. Việc thuộc `done`/`stopped` không bao giờ tính quá hạn.

---

## 7. Backend

### 7.1 Endpoint

```
GET assign/my-todo/calendar
  from_date  'Y-m-d H:i:s'  bắt buộc
  to_date    'Y-m-d H:i:s'  bắt buộc
  types[]    mảng type      tùy chọn, rỗng = tất cả
  status     giá trị thật   tùy chọn, chỉ có nghĩa khi types[] đúng 1 phần tử
```

Trả `data` = mảng item mục 4, **không phân trang**, đã sắp theo `start` tăng dần.

### 7.2 File

- `Modules/Assign/Services/MyTodo/WorkCalendarService.php` — **mới**. Mỗi loại một method `fetch<Type>(range)` trả collection item chuẩn hoá; `getAll()` gom + sắp xếp.
- `Modules/Assign/Http/Controllers/Api/V1/MyTodoController.php` — thêm method `calendar()`.
- `Modules/Assign/Routes/api.php` — thêm route vào nhóm `/assign/my-todo` sẵn có.
- Phần "việc của tôi" (mục 2) tách thành scope/trait dùng chung giữa `MyTodoService` và `WorkCalendarService`.

### 7.3 Vì sao không dùng lại `MyTodoService::getAll()`

- `getAll()` **không lọc ngày ở DB** — nạp toàn bộ việc còn mở rồi lọc bằng collection. Nhét range vào vẫn nạp hết.
- Nó cố tình loại bỏ các trạng thái kết thúc; lịch cần hiện hết (mục 3). Nới điều kiện ở đó là sửa thẳng vào tab danh sách đang chạy ổn.
- Nó chỉ có `due_date` (một mốc), lịch cần `start`/`end`.

### 7.4 Endpoint chi tiết cho drawer

Không viết mới — tái dùng: `GET assign/meeting/{id}` (đang dùng) · `GET assign/assign_business/{id}` · `GET assign/assign_jobs/{id}`.

---

## 8. Frontend

### 8.1 Thanh tóm tắt (`CalendarSummaryBar`)

- Chưa chọn loại nào → 6 ô đếm theo loại, **hiện đủ 6 ô kể cả khi bằng 0**, đếm trên tập **đang hiển thị của kỳ đang xem** (giữ nguyên cách đếm overlap hiện tại, không đếm theo mỗi `start`).
- Đã chọn đúng 1 loại → tách theo **bộ trạng thái thật** của loại đó.

### 8.2 Thanh lọc (`CalendarFilterToolbar`)

- 6 **chip bật/tắt theo loại**, mỗi chip có chấm màu loại; bấm chip đang bật → tắt về "tất cả".
- Ô "Trạng thái": khi đang bật nhiều loại thì **vô hiệu hoá** (như mockup); bật đúng 1 loại thì đổ đúng bộ trạng thái của loại đó.
- ⚠️ Mọi option select phải dùng **id kiểu string**: `V2BaseSelect` build option bằng `opt.id || opt.value || opt.code` nên id số `0` (Meeting "Đang tạo") bị coi là falsy và rơi mất — lỗi này đã gặp ở feature tiền nhiệm.

### 8.3 Thẻ (`WorkItemCard`)

Icon loại + tiêu đề · dòng phụ `subtitle` · dòng dưới: khoảng giờ hoặc chữ **"Cả ngày"** + chấm màu nhóm + chữ trạng thái thật · badge "Quá hạn" khi cần.

### 8.4 Bấm thẻ

| Loại | Hành vi |
|---|---|
| Meeting | Drawer sẵn có — giữ nguyên gate quyền: nút "Sửa" ẩn khi `canEdit = false`, "Xem biên bản" theo quyền hiện hành |
| Phiếu công tác | Drawer cùng khuôn (mục 8.4.1), nút "Mở chi tiết" → `/assign/assign_business/{id}` |
| Phiếu giao việc | Drawer cùng khuôn (mục 8.4.1), nút "Mở chi tiết" → `/assign/assign_jobs/{id}` |
| Task | `createTaskModal.view({ id })` — popup tab danh sách đang dùng |
| Issue | `createIssueModal.open({ id }, true)` — popup tab danh sách đang dùng |
| Nhắc việc cá nhân | `TodoFormModal` như `onEditPersonalTodo` |

3 popup ở cuối **đã được khai báo sẵn** trong `index.vue`; tab lịch gọi qua ref của trang cha, không khai báo trùng.

#### 8.4.1 Bộ trường của drawer, theo loại

Dùng chung khuôn `WorkItemDetailDrawer` (header màu theo LOẠI + mã + khoảng thời gian + trạng thái), thân đổ đúng bộ trường:

| Loại | Trường trong thân drawer |
|---|---|
| Meeting | giữ nguyên bộ hiện có: Mục tiêu/Nội dung · Loại meeting · Hình thức + địa điểm/link · Khách hàng + người liên hệ · Thành phần công ty/khách · Kết luận · Người tạo |
| Phiếu công tác | Khách hàng (`customer_name`) · Nội dung công việc (`job_note`) · Ghi chú (`note`) · Thời gian đi (`time_to_go`) · Trưởng nhóm (`leaderEmployee`) · Nhân sự tham gia (`employees`) · Người tạo |
| Phiếu giao việc | Khách hàng (`customer_name`) · Địa điểm (`place`) · Người liên hệ (`contact_name` + `contact_phone_number`) · Tên việc (`job_name`) · Mô tả (`job_description`) · Phòng yêu cầu / phòng thực hiện · Số giờ (`total_hour`) · Nhân sự tham gia (`employees`) · Lý do từ chối (`reason_deny`, chỉ khi có) · Người tạo |

Mọi trường phải null-check — bản hiện tại từng 500 vì thiếu null-check ở `Employee::find()`.

### 8.5 Đổi tên file

Trong `pages/assign/my-todo/components/calendar/`:

| Cũ | Mới |
|---|---|
| `MeetingCalendarTab.vue` | `WorkCalendarTab.vue` |
| `MeetingCard.vue` | `WorkItemCard.vue` |
| `MeetingMultiDayBar.vue` | `WorkItemMultiDayBar.vue` |
| `MeetingDetailDrawer.vue` | `WorkItemDetailDrawer.vue` |
| `DayMeetingsPopover.vue` | `DayItemsPopover.vue` |
| `calendar-status.js` | `calendar-status.js` (giữ tên, đổi nội dung: thêm màu loại + nhóm trạng thái) |

Giữ nguyên tên: `MonthGrid.vue`, `WeekGrid.vue`, `CalendarHeader.vue`, `CalendarFilterToolbar.vue`, `CalendarSummaryBar.vue`, `calendar-lanes.js`, `calendar-week-helpers.js`.

Thêm mới `work-item-types.js`: nhãn · màu · icon · thứ tự 6 loại (một nguồn duy nhất cho chip, summary, thẻ, drawer).

Đổi tên làm hỏng selector của e2e hiện có → sửa kèm trong cùng phase.

---

## 9. Quyết định đã chốt

| # | Quyết định | Ghi chú |
|---|---|---|
| 1 | Giữ 2 tab, chỉ đổi **nhãn tab** | Menu sidebar + URL giữ nguyên |
| 2 | **6 loại**, gồm cả Nhắc việc cá nhân | Mockup chỉ có 3 loại — cố ý làm rộng hơn mockup |
| 3 | Lấy lại **Phiếu giao việc** mà mockup đã bỏ ngày 08/08/2026 | Yêu cầu mới của user, đè quyết định cũ |
| 4 | Hiện **hết** trạng thái, kể cả chưa duyệt / đã xong / huỷ | Khác tab danh sách, có chủ ý |
| 5 | Màu theo **loại**, chấm theo **trạng thái** | Không tô màu theo trạng thái như bản meeting cũ |
| 6 | Việc nhiều ngày **trải thanh** theo khoảng thật | |
| 7 | Việc **chưa có hạn**: ẩn khỏi lịch, không có khay phụ | |
| 8 | Drawer cho 3 loại phiếu; 3 loại còn lại dùng **popup sẵn có** | |
| 9 | **Bỏ** bộ lọc Thị trường của mockup | Giữ quyết định của feature tiền nhiệm |
| 10 | **Đổi tên** component không còn chỉ phục vụ meeting | Chấp nhận sửa e2e kèm |

---

## 10. Rủi ro & gotcha đã biết

- **Bộ e2e chạy `serial`**: một ca đỏ làm mọi ca sau in "did not run", không phải "passed". Phải đọc dòng tổng kết.
- **`V2BaseSelect` nuốt id số 0** — dùng id string cho mọi option (mục 8.2).
- **`fetchRange` phải khớp lưới**: `MonthGrid` luôn vẽ 6 hàng cố định (42 ô) từ `monthGridStart`; range gọi API phải dùng chung hàm đó, nếu không hàng cuối thiếu dữ liệu. Đã từng lỗi ở feature tiền nhiệm.
- **Summary đếm theo overlap**, không theo mỗi `start` — nếu không sẽ lệch số so với lưới.
- **Nuxt manifest stale sau đổi nhánh**: đổi tên component + đổi nhánh dễ ra lỗi "Can't resolve component". Restart Nuxt + xoá `.nuxt/components` trước khi kết luận là lỗi code.
- **Lệch schema local vs production**: thiếu cột ở DB local thường là DB hỏng — kiểm migration trước khi sửa code.
- **Số lượng bản ghi**: 6 truy vấn cho một kỳ 6 tuần. Phải đo thời gian phản hồi trên dữ liệu thật; nếu chậm thì thêm index theo cột ngày, không cắt bớt dữ liệu.

---

## 11. Kiểm chứng

Theo `CLAUDE.md` — task đụng giao diện bắt buộc mở Playwright kiểm trên trình duyệt thật trước khi báo hoàn thành, **đo bằng số lấy từ DOM**:

1. Đếm số thẻ mỗi loại trên lưới, so với số ở thanh tóm tắt — phải bằng nhau **ở view Tuần**.
   ⚠️ **Ở view Tháng KHÔNG thể bằng nhau, và đó là đúng**: lưới luôn vẽ 6 hàng cố định (42 ô) nên gồm cả ngày
   của tháng liền kề, còn thanh tóm tắt chỉ đếm đúng tháng thật (nhãn kỳ ghi "Từ 01/08 – 31/08"). Việc nằm ở ô
   tháng bên cạnh sẽ hiện trên lưới mà không được đếm. Hành vi này kế thừa từ bản chỉ-meeting, không phải lỗi.
   Yêu cầu "bằng nhau ở cả Tháng và Tuần" trong bản spec đầu là SAI — đã sửa lại ngày 2026-09-11.
2. Đo `getComputedStyle` màu viền/nền thẻ của cả 6 loại — đúng token mục 6.1, và 6 màu phân biệt được.
3. Đo `opacity` + `text-decoration` của thẻ nhóm `done` / `stopped`.
4. Đo toạ độ + chiều rộng thanh nhiều ngày, xác nhận trải đúng số ngày và cắt đúng khi tràn tuần.
5. Việc `all_day` phải nằm trong hàng "Cả ngày" của lưới Tuần — đo bằng toạ độ, không nhìn ảnh.
6. Bấm đủ 6 loại: 3 loại ra drawer đúng bộ trường, 3 loại ra đúng popup sẵn có.
7. Task/Issue/Nhắc việc **không có hạn** phải vắng mặt trên lưới nhưng vẫn còn ở tab danh sách.
8. **Phân quyền cả 2 chiều**: người không dự họp mà có quyền cấp cao vẫn KHÔNG thấy meeting đó; người dự họp mà không có quyền cấp nào vẫn thấy. Tương tự với phiếu/task không thuộc về mình.
9. Bổ sung/cập nhật ca e2e cho hành vi mới, rồi chạy **toàn bộ** bộ test của màn và đọc dòng tổng kết.
