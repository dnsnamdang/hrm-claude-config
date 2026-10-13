# Phase 4 — Spec triển khai code (BE + FE)

> Nghiệp vụ / giao diện đã chốt ở `design.md` (mockup). File này CHỈ ghi phần **đưa vào code**:
> đường dẫn, hợp đồng API, ánh xạ DB, phân quyền và những chỗ code thật **lệch với mockup**.
> Mockup: `bao-cao-ke-hoach-lam-viec-nhan-vien.html`.

## 1. Vị trí màn

| | |
|---|---|
| **Tên màn** | Báo cáo kế hoạch & kết quả làm việc theo nhân viên |
| **Route FE** | `/assign/report/employee-work-performance` |
| **Thư mục FE** | `pages/assign/report/employee-work-performance/` |
| **Prefix API** | `/api/v1/assign/report/employee-work-performance` |
| **Module BE** | `Modules/Assign` |
| **Menu** | 2 nơi (user chốt 2026-09-21): `components/subsystem-menu/presale.js` nhóm *Báo cáo* **và** `components/menu-sidebar.js` (`menuItemsAssign`) nhóm *Báo cáo* |

Để ở `/assign/report/` cho cùng chỗ với 16 báo cáo hiện có — 8 báo cáo khác của phân hệ CSKH trước
bán cũng nằm ở đây, `pages/presale/` mới chỉ có `dashboard`.

`subsystems.js` đã ghi rõ 1 link được khai ở 2 phân hệ (thanh bên nhớ phân hệ user đang làm việc),
nên khai 2 nơi KHÔNG phải lỗi trùng.

## 2. Phân quyền (user chốt 2026-09-21)

**3 cấp, KHÔNG có cấp "tổng công ty", KHÔNG có fallback "chỉ xem việc của mình".**

| Quyền | Phạm vi thấy được |
|---|---|
| `Xem báo cáo kế hoạch & kết quả làm việc theo công ty` | mọi phòng ban trong công ty đang xem |
| `Xem báo cáo kế hoạch & kết quả làm việc theo phòng ban` | phòng ban user quản lý (`listManageDepartmentIds()`) |
| `Xem báo cáo kế hoạch & kết quả làm việc theo bộ phận` | bộ phận user quản lý (`listManagePartIds()`) |

- **Không có quyền nào trong 3 → KHÔNG được xem** (khác 3 báo cáo anh em trong presale, vốn rơi về
  mức `self`). BE trả **403**; FE ẩn mục menu (`isShow`) và chặn vào màn bằng URL trực tiếp.
- **`company_id` là BẮT BUỘC** — mọi truy vấn đều phải có 1 công ty. Thiếu → **422**
  `Bắt buộc phải nhập` (message chuẩn của lang file, KHÔNG tự viết).
- Công ty được phép xem = công ty user đang làm việc (`auth()->user()->current_company_role`).
  Gửi `company_id` khác → **403**. Lý do: `spatie` lưu quyền theo từng công ty
  (`role_has_permissions.company_id`), quyền ở công ty A không nói gì về công ty B.

### ⚠️ Không dùng `V2BaseCompanyDepartmentFilter` cho ô Công ty

`components/V2BaseCompanyDepartmentFilter.vue:8` chỉ render ô **Công ty** khi
`permissions.is_all_company === true`. Màn này không có cấp đó nên ô Công ty sẽ **không bao giờ
hiện** nếu giao cho component.

Cách làm: khai **ô `company_id` riêng** trong `filterFields` (`type: 'select'`, `allowClear: false`,
options từ `$store.state.companies` lọc theo công ty user có vai trò, mặc định
`current_company_role`), rồi vẫn dùng `V2BaseCompanyDepartmentFilter` cho **Phòng ban / Bộ phận /
Nhân viên** với `permissions.is_all_company = false`.

Truyền **cùng một object** `this.filters` vào prop `form` của component: watcher
`form.company_id` (dòng 365) sẽ tự xoá `department_id / part_id / employee_id` khi đổi công ty.
KHÔNG bọc thêm `col-*` quanh component (nó tự khai `.d-contents`, bọc thêm là vỡ lưới).

## 3. Ánh xạ 5 nguồn sang DB thật (đã đối chiếu `hrm_erp` ngày 2026-09-21)

| Loại | Bảng chính | Bảng người tham gia | Khoá người | Khoảng thời gian |
|---|---|---|---|---|
| Meeting | `meetings` | `meeting_employees` | `employee_id` → `employees.id` | `start_date` → `end_date` |
| Task | `tasks` | — (`assignee_id`) | `assignee_id` → `employees.id` | `start_date` → `due_date` + `due_time` |
| Issue | `issues` | — (`assignee_id`) | `assignee_id` → `employees.id` | `detected_at` → `due_date` + `due_time` — xem §4c |
| P. công tác | **`assign_requests` lọc `type = 2`** (`AssignRequest::PHIEU_CONG_TAC`) | `assign_request_employees` | `employee_id` → `employees.id` | `from_time` → `to_time` |
| P. giao việc | `assign_jobs` | `assign_job_employees` | **`employee_info_id` → `employee_infos.id`** | `time_start_request` → `deadline` |

### 4 cái bẫy đã đo được, KHÔNG suy từ mockup

1. **`assign_job_employees` dùng `employee_info_id`, KHÔNG phải `employee_id`.** Đã kiểm:
   545/545 dòng khớp `employee_infos.id`. Muốn ra `employees.id` (khoá của cây tổ chức và của
   `auth()->id()`) phải join `employees.employee_info_id`. Dùng nhầm là gán việc cho **nhân viên
   khác** mà không có lỗi nào báo — đúng cái bẫy CLAUDE.md cảnh báo về `employee_infos.id`.
   Điều kiện "việc của tôi" đã có sẵn ở `MyTodoOwnershipScope::assignJobs()` — bám theo.
2. **`meeting_employees` chứa CẢ người phía khách hàng.** `type = 2` là khách (741/2387 dòng có
   `employee_id = NULL`). Bắt buộc lọc `type = 1` / `employee_id IS NOT NULL`, nếu không dòng
   khách hàng rơi vào nhóm "chưa xác định" và thổi phồng số lượt tham gia.
3. **❌ SỬA 2026-09-21 — bảng của "P. công tác" là `assign_requests`, KHÔNG phải `assign_business`.**
   Bản đầu của spec này ghi `assign_business` (chép từ mockup) và **sai**. Repo có 2 bộ bảng:

   | | `assign_business` (model `TpAssignBusiness`) | `assign_requests` (model `AssignRequest`) |
   |---|---|---|
   | Số phiếu | 163 | **6.902** (`type = 2`) |
   | `from_time` mới nhất | **14/04/2024** — đã chết | **16/09/2026** — đang sống |
   | Ai dùng | chỉ có hàm `sync*()` đẩy một chiều | `AssignBusinessService` (màn `/assign/assign_business`), `MyTodoService`, `WorkCalendarService` |
   | Hằng trạng thái | — | `WorkItemStatusGroup` map khoá `'assign_business'` sang **`AssignRequest::`** |

   `assign_business` là **snapshot ERP-legacy đã dừng đồng bộ từ 04/2024**. Dùng nó thì báo cáo
   mất 97% phiếu công tác mà vẫn "chạy được".
   Người chủ trì = `assign_request_employees.is_leader = 1`.
   `assign_requests` CÓ đủ `company_id` / `department_id` / `part_id`, nhưng cây tổ chức của báo cáo
   **vẫn lấy theo NGƯỜI ĐƯỢC TÍNH** (`employee_infos` của từng người trong đoàn), không đọc cột trên
   phiếu — đúng luật chung ở cuối mục này.
4. **Tên hiển thị của phiếu công tác**: `assign_requests` không có cột tên. Lấy giá trị không rỗng
   đầu tiên trong `job_note` → `customer_name` → `place`, hết thì rơi về `code`. Trên DB local chỉ
   **535/6.902** phiếu có 3 cột đó, tức ~92% sẽ hiện mã phiếu — đúng hiện trạng dữ liệu, không bịa.

5. **`tasks` không có `start_time`** (chỉ có `due_time`). Giờ bắt đầu của Task luôn `00:00` —
   đúng như mục "NỢ BACKEND" ở `design.md`. KHÔNG bịa giờ ở BE.

### Cây tổ chức lấy theo NGƯỜI ĐƯỢC TÍNH

Phòng ban / Bộ phận của một dòng = `employee_infos.department_id` / `part_id` của **người tham
gia**, KHÔNG phải cột trên chứng từ. Nhờ vậy một meeting do phòng khác chủ trì vẫn hiện ở phòng của
người có dự — đúng luật đã chốt ở `design.md` mục "Luật POPUP chi tiết" điểm 4.

## 4. Tái sử dụng — 3 helper đã có sẵn, KHÔNG viết lại

| Helper | Dùng để làm gì |
|---|---|
| `Modules\Assign\Services\MyTodo\WorkItemPeriod::of($entity, $type)` | quy 5 loại về cùng cặp `start` / `end` để tính giao nhau với kỳ |
| `Modules\Assign\Services\MyTodo\WorkItemStatusGroup::of($type, $status)` | quy 5 bộ trạng thái về 4 nhóm `todo / doing / done / stopped` |
| `Modules\Assign\Services\MyTodo\MyTodoOwnershipScope` | điều kiện "người này có tham gia phiếu" của từng loại |

### 4a. `WorkItemPeriod` trả `null` thì rơi về `created_at`

`WorkItemPeriod::of()` trả `null` khi task/issue **chưa đặt hạn** (`due_date` rỗng) — màn lịch cố ý
loại chúng đi. Báo cáo khối lượng thì **không được để rơi mất việc**: null → lấy
`[created_at, created_at]`. Ghi chú thẳng trong code, đừng để người sau tưởng copy thiếu.

### 4c. Issue: NỚI `start` về `detected_at` NGOÀI helper, không sửa helper (chốt 2026-09-21)

`WorkItemPeriod::of($e, 'issue')` gọi `fromDueDate($entity, **null**, $due)` → `start = due_date`,
tức `start == end` và **`detected_at` không hề được dùng**. Với màn lịch thì đúng (issue là một mốc
hạn), nhưng với báo cáo khối lượng thì sai: một sự vụ phát hiện tháng 1, hạn tháng 3 sẽ **không**
xuất hiện ở kỳ tháng 2, và thanh thời gian ở popup dài đúng 0 ngày.

§3 và §4 mâu thuẫn ở đúng chỗ này. Cách xử lý: **collector tự nới `start` về `detected_at`** khi
`detected_at` sớm hơn, ngay sau khi gọi helper — **KHÔNG sửa `WorkItemPeriod`**.

Lý do không sửa helper: nó đang phục vụ màn *Việc của tôi* và lịch làm việc, có cả baseline e2e
(`my-todo-ownership.baseline.json`). Đổi nó là đổi hành vi của một tính năng khác để phục vụ báo cáo
này — cái giá không tương xứng, và nằm ngoài phạm vi Phase 4.

Hệ quả phải chấp nhận: báo cáo đếm 1 issue ở NHIỀU kỳ hơn so với màn lịch hiển thị. Đó là đúng ý
đồ "khối lượng theo kỳ" và đã được ghi ở đây để người sau không tưởng là lệch.

### 4b. 4 nhóm trạng thái của báo cáo dựng TRÊN `WorkItemStatusGroup`

```
stopped            -> cancel   (Dừng / Huỷ / Từ chối)
done               -> done     (Đã hoàn thành)
end < TODAY        -> late     (Quá hạn)   ; xét SAU cancel và done
còn lại            -> doing    (Đang thực hiện)
```

⚠️ **`TODAY` là ĐẦU NGÀY, không phải `now()`.** Mọi việc cả ngày có `end` = `00:00:00` của ngày hạn
(`WorkItemPeriod` gọi `startOfDay()`), nên so với `Carbon::now()` thì **việc hạn HÔM NAY bị tính quá
hạn ngay từ 00:00:01 và suốt cả ngày** — thổi phồng đúng chỉ số mà màn này bán. Phải
`Carbon::now()->startOfDay()`. Bộ test phải có ca `end == hôm nay` với `$today` MANG GIỜ, nếu không
ca này không bao giờ bị bắt.

⚠️ **Lệch với mockup ở đúng 1 chỗ**: `WorkItemStatusGroup` xếp `Task::PAUSED` (Tạm dừng) và
`Meeting::DANG_TAO` vào nhóm `stopped` / `todo`, còn mockup gom "Tạm dừng" vào *Đang thực hiện*.
Theo CLAUDE.md, bảng này là **nguồn duy nhất** nên **theo helper**, và đổi nhãn nhóm thứ 4 trên màn
từ *"Huỷ / Từ chối"* thành **"Dừng / Huỷ / Từ chối"** cho khớp nội dung thật.

## 5. Cơ chế đếm (nhắc lại cho BE — chốt 2026-09-21)

| Cấp | Cách đếm |
|---|---|
| Nhân viên | `COUNT(*)` trên các cặp `(phiếu × người)` — có tham gia là +1 |
| Bộ phận · Phòng ban · dòng TỔNG · dải tổng hợp | `COUNT(DISTINCT <loại>#<id phiếu>)` — 1 phiếu nhiều người vẫn là 1 |

- Khoá phiếu phải **kèm loại** (`meeting#12`, `task#12`) vì 5 bảng có id trùng nhau.
- Mỗi node trả thêm `seats` = số lượt tham gia, để FE ghi tooltip *"N phiếu · M lượt tham gia"*.
- **Dòng cha nhỏ hơn tổng dòng con** và **cộng các phòng > dòng TỔNG** — không phải lỗi. E2E phải
  assert đúng chiều này (`cha <= tổng con`), đừng chép ca `cha == tổng con` của báo cáo anh em.
- Bật *Chỉ tính việc chủ trì* → mỗi phiếu còn 1 người ⇒ 2 cách đếm trùng nhau, `seats == total`.

## 6. Hợp đồng API

Tất cả đều `GET`, đều nhận chung bộ tham số lọc:

```
company_id     (BẮT BUỘC)  department_id  part_id  employee_id
period         today|week|month|quarter|year|custom   start_date  end_date
types          csv: meeting,task,issue,trip,job       (mặc định đủ 5)
               ⚠️ FE LUÔN gửi khoá `types`. BE phân biệt bằng `has()` chứ KHÔNG phải `filled()`:
               không gửi khoá  -> đủ 5 loại
               gửi `types=`    -> CHƯA BẬT LOẠI NÀO -> bảng RỖNG (không phải hiện hết)
bucket         done|doing|late|cancel                 (rỗng = tất cả)
host_only      0|1     busy_only  0|1
```

| Endpoint | Trả về |
|---|---|
| `/employee-work-performance` | `{ period, permission_level, summary, total, tree }` |
| `/employee-work-performance/drill` | `{ data: [...] }` — thêm `key`, `metric` |
| `/employee-work-performance/export` | file `.xlsx` |
| `/employee-work-performance/print-list-data` | `{ data: { template: '<html>' } }` |

⚠️ Tên `print-list-data` và khoá `template` là **contract** của
`utils/mixins/reportPrintPreviewMixin.js` — đổi tên là popup nhận rỗng, không báo lỗi gì.

### Hình dạng 1 node của `tree`

```json
{
  "key": "n/dept:12/emp:345",
  "dim": "dept|part|emp",
  "id": 12,
  "name": "PHÒNG KINH DOANH THƯƠNG MẠI",
  "path": [{ "dim": "dept", "id": 12, "name": "..." }],
  "metrics": { "meeting": 105, "task": 269, "issue": 108, "trip": 76, "job": 101,
               "total": 659, "done": 320, "doing": 188, "late": 112, "cancel": 39,
               "seats": 1040, "by_doc": true, "completion_rate": 48.6 },
  "children": []
}
```

- **3 trường cho DRAWER** (bổ sung 2026-09-21 — bản đầu của spec này QUÊN, khiến ô *Trạng thái chứng
  từ* và *Tiến độ* hiện `—` ở mọi dòng):
  - `status` — giá trị **thô** của chứng từ
  - `status_text` — nhãn tiếng Việt, qua helper `EmployeeWorkPerformance\WorkStatusLabel::of()`.
    Helper này **cố ý trùng lặp** bảng nhãn của `MyTodoService::getStatusText()` — không sửa file đó
    vì nó đang phục vụ màn *Việc của tôi*. Cùng nguyên tắc đã dùng với `WorkItemPeriod` (§4c).
  - `progress` — `int|null`, **CHỈ Task có** (`tasks.progress_pct`). Đã kiểm
    `information_schema.columns`: `issues` / `assign_jobs` / `assign_requests` / `meetings` **không có**
    cột tương đương → 4 loại kia trả `null`, drawer hiện `—` **có chủ đích**.
  ⚠️ 2 ô *Trạng thái* (4 nhóm theo dõi) và *Trạng thái chứng từ* (gốc) phải **KHÁC NHAU** ở nhiều ca —
  đó là lý do chúng cùng tồn tại. Đo được: Task `Quá hạn`/`Cần làm` · Meeting `Dừng-Huỷ-Từ chối`/`Hủy`
  · Trip `Quá hạn`/`Đã duyệt` · Job `Đã hoàn thành`/`Đã duyệt KQ`.

- **Icon sort của popup**: `design.md` chốt "2 mũi tên chồng nhau", nhưng vỏ dùng chung
  `V2BaseReportModal` tự vẽ icon riêng và đang phục vụ **3 popup báo cáo đang sống**, không có slot
  riêng cho `<th>`. **Chấp nhận lệch** (chốt 2026-09-21) — giữ icon của vỏ, không sửa vỏ dùng chung.

- `by_doc` = `dim !== 'emp'` — FE dựa vào nó để quyết định có ghi *"N phiếu · M lượt"* vào tooltip
  hay không, KHÔNG tự suy từ `dim` (BE đổi luật thì FE khỏi phải sửa theo).
- Cấp **Bộ phận chỉ dựng cho phòng CÓ chia bộ phận** — phòng không chia thì nhảy thẳng
  Phòng ban ▸ Nhân viên, **không đẻ dòng "Chưa phân bộ phận"** (copy `buildTree()` của
  `CustomerMarketDevelopmentService.php:666`, nó đã bỏ cấp rỗng sẵn).

- ⚠️ **Người chưa gán bộ phận trong phòng CÓ chia bộ phận: treo THẲNG dưới Phòng ban**, không gom
  vào một node "Chưa phân bộ phận". Mockup đã chốt và cài sẵn luật này
  (`bao-cao-ke-hoach-lam-viec-nhan-vien.html:3183-3188`, biến `loose`).
  Khuôn gốc `CustomerMarketDevelopmentService.php:689` CÓ dòng fallback sinh node đó — **phải bỏ khi
  copy**. Bỏ node KHÔNG được làm mất người: họ chuyển thành node `emp` con trực tiếp của `dept`.

- ⚠️ **Hệ quả tới bộ CHỌN CẤP XEM (phát hiện 2026-09-21 khi chạy trên dữ liệu thật)**: một phòng
  có thể có **CẢ bộ phận LẪN nhân viên lẻ** làm con trực tiếp — vd `PHÒNG QUẢN TRỊ THÔNG TIN` có
  con `BP Phát triển phần mềm` (`dim=part`) và con `Nguyễn Thị Lệ` (`dim=emp`) cùng cấp.
  Thuật toán `applyLevel()` của khuôn gốc xét `children[0].dim` để quyết định bung **cả node**, nên ở
  nấc *Đến Bộ phận* nó làm **lòi nhân viên lẻ ra cùng lúc với bộ phận** — trái luật
  *"không lòi nhân viên ra sớm"* đã chốt ở `design.md`.
  Dữ liệu demo của mockup (10 phòng) không có ca này nên luật chưa từng bị kiểm.
  **Chốt: lọc theo `dim` của TỪNG CON khi bung**, không quyết định theo `children[0]`:
  - phòng chỉ có nhân viên → *Đến Bộ phận* **dừng ở Phòng ban**
  - phòng có cả hai → *Đến Bộ phận* chỉ hiện **bộ phận**, nhân viên lẻ ẩn tới *Tất cả cấp*

- **Người chưa gán PHÒNG BAN thì khác**: cấp `dept` là cấp trên cùng, không có chỗ nào để treo vào,
  nên **giữ 1 node "Chưa phân phòng ban"** — xoá trắng là mất người im lặng. Node này có
  `id` kiểu **CHUỖI** (`'__no_dept__'`), nên hợp đồng API khai `id: int|string`; Task 5 khi parse
  `key`/`path` phải chịu được giá trị chuỗi, cast ẩu sang int là popup trả 0 dòng mà không báo gì.

### Dòng của `drill`

Popup mở từ cấp cha gộp **1 dòng / phiếu**; BE trả sẵn `mates` để FE hiện `+N`:

```json
{ "type": "meeting", "code": "MT-260012", "name": "...",
  "emp_id": 345, "emp_name": "Nguyễn Minh Hoàng", "role": "host",
  "department_id": 12, "department_name": "...", "part_id": null, "part_name": null,
  "start": "2026-09-26 17:00", "end": "2026-09-26 19:00", "bucket": "done",
  "status": 3, "status_text": "Hoàn thành", "progress": null,
  "mates": [{ "emp_id": 345, "emp_name": "...", "role": "host",
              "department_id": 12, "part_id": null }] }
```

- Người **đại diện** là người chủ trì nếu người đó nằm trong phạm vi đang xem, nếu không lấy người
  đầu tiên.
- **Lọc trước trên từng cặp rồi mới gộp** — làm ngược lại thì lọc theo 1 nhân viên vẫn kéo cả
  những người khác trong phiếu ra (đã đo trên mockup: 107 → 26 dòng, 0 dòng còn `+N`).
- `by_doc = true` ⇒ **bỏ cột Vai trò** ở popup (1 dòng mang nhiều vai trò).

## 7. Hiệu năng

`meetings` 856 · `assign_jobs` 353 · `assign_business` 163 · `tasks` 19 · `issues` 0 trên DB local,
production lớn hơn nhiều. Ràng buộc:

- **5 truy vấn, không hơn** (1 / loại), đã `whereIn` sẵn danh sách `employee_id` trong phạm vi
  quyền; `with()` bảng người tham gia. **Cấm N+1**.
- Phẳng hoá thành cặp bằng PHP trong bộ nhớ (như `CustomerMarketDevelopmentService` đang làm) —
  gộp/đếm ở SQL không tái dùng được cho cả cây lẫn popup.
- `company_id` bắt buộc đã tự chặn truy vấn toàn hệ thống.
- Kiểm index trước khi bàn giao: `meetings.start_date`, `assign_business.from_time`,
  `assign_jobs.time_start_request`, `tasks.due_date`, `issues.due_date`.

## 8. Ngoài phạm vi Phase 4

- Không bổ sung cột `tasks.start_time` (nợ backend, ghi ở `design.md` Task 4).
- Không làm màn `/print` riêng — dùng popup `ReportPrintPreviewModal` như báo cáo anh em.
- Chưa làm responsive (bám hiện trạng 16 báo cáo còn lại).
