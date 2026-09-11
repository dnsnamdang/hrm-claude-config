# Bug: Bảng phân ca tổng hợp trống ngày 09/09/2026 (@khoipv)

Màn: `timesheet/timeworking` (tab Nhân viên) — demothanhan.dnsmedia.vn

## Task

- [x] Tái hiện trên demo bằng Playwright (đăng nhập DNS Admin)
- [x] Đọc API `GET /api/v1/timesheet/timeworking/list?tab=1` — xác nhận 09/09/2026 rỗng
- [x] Truy vết code `TimeWorkingService::getListEmployee()` — tìm nhánh rẽ theo ngày
- [x] Đối chiếu dữ liệu `timesheet_summaries` / `timesheet_details` ngày 07–10/09
- [x] Quét `created_at` theo id nhân viên để tìm mốc cron dừng
- [x] Kết luận root cause
- [ ] Chốt hướng sửa với @khoipv (xem mục Đề xuất)

## Root cause

1. `Modules/Timesheet/Services/TimeWorkingService.php:149` —
   `if ($date <= $now)` → với **ngày hôm nay và quá khứ**, tên ca lấy từ
   dữ liệu chấm công đã sinh (INNER JOIN `working_shifts` ⋈ `timesheet_details`
   ⋈ `timesheet_summaries`), **không** đọc từ cấu hình phân ca `shift_detail_dates`.
   Ngày tương lai mới đọc thẳng cấu hình → đó là lý do 10/09 trở đi vẫn hiện bình thường.

2. Bản ghi `timesheet_details` cho ngày N do cron
   `php artisan create:timesheet_detail` (không tham số → `Carbon::now()->addDays(1)`)
   sinh lúc **23:00 giờ VN đêm hôm trước** (`WorkShiftDetailService::createTimesheetDetail`,
   vòng lặp `EmployeeInfo::where('status',1)->get()` theo id tăng dần).

3. **Đêm 08/09/2026 cron chạy được ~25 giây rồi dừng giữa chừng.**
   Bằng chứng `timesheet_details.created_at` cho ngày 09/09:
   - id ≤ 26 → `2026-09-08T16:00:24..25Z` (= 23:00:24 VN) — cron tạo
   - id ≥ 27 → không có gì, mãi tới `2026-09-09T01:41:57Z` (lần @khoipv chạy tay sáng nay)
   - Đêm trước đó (07/09) cron chạy **đủ** tới id 76 lúc `16:00:48Z` → bình thường mất ~50s

   ⇒ Nhân viên id ≥ 27 (đa số danh sách) không có `timesheet_detail` ngày 09/09
   → INNER JOIN không ra dòng → ô trống.

## Trạng thái sau khi @khoipv chạy lại (09/09 08:42 VN)

Đã đầy: 116/120 nhân viên có ca ở cả 07, 08, 09, 10, 11/09.
4 người còn trống là do không có cấu hình ca (getWorkshift trả null), không phải lỗi này.

## Chưa xác định

Vì sao cron dừng ở nhân viên id=27 (Huỳnh Thị Cam Thảo, NV.00027) —
hồ sơ người này không có gì bất thường (status 1, company_id 4, enter_date 2021-11-10),
và đêm 07/09 vẫn xử lý được. Cần xem trên server demo:
- `storage/logs/laravel-2026-09-08.log` quanh 23:00
- log cron / output redirect của lệnh `create:timesheet_detail`
→ phân biệt: exception dữ liệu vs. bị kill (timeout / OOM).

## Phát hiện thêm: cron nằm ngoài repo

`create:timesheet_detail` và `calc:timesheet` **không** được đăng ký trong
`app/Console/Kernel.php` (schedule chỉ có `activitylog:clean`, `contracts:*`,
`quotations:*`, `projects:*`) và cũng không có trong `routes/console.php`
hay script deploy nào trong repo → đang chạy bằng **crontab hệ thống trên server demo**.

Hệ quả: không đi qua Laravel scheduler nên **không có `withoutOverlapping`,
không `onFailure`, không log** — cron chết giữa chừng thì im lặng hoàn toàn,
đúng với những gì xảy ra đêm 08/09. Muốn biết lịch thật phải xem `crontab -l` trên demo.

## Đề xuất (chờ @khoipv chốt)

- **A. Chống vỡ (khuyến nghị):** bọc `try/catch` + `Log::error` quanh thân vòng lặp
  trong `createTimesheetDetail()` — 1 nhân viên lỗi không kéo đổ cả 120 người còn lại.
- **B. Fallback khi thiếu dữ liệu:** ở `getListEmployee()`, nếu ngày ≤ hôm nay mà
  không tìm thấy `timesheet_detail` thì rơi về cấu hình phân ca (nhánh `else`)
  thay vì trả rỗng. Lưu ý: đây là **hàm dùng chung**, cần @khoipv xác nhận trước khi sửa.
- **D. Đưa 2 lệnh vào `app/Console/Kernel.php`** như các cron khác của dự án
  (`->dailyAt('23:00')->timezone('Asia/Ho_Chi_Minh')`), gỡ khỏi crontab hệ thống —
  để có `onFailure()` báo lỗi và `withoutOverlapping()`. Là thay đổi hạ tầng chạy nền,
  cần @khoipv chốt.
- **C. Giám sát:** cron kiểm tra sau 23:05 — đếm `timesheet_details` ngày mai
  so với số nhân viên active, lệch thì cảnh báo.

## Checkpoint — 2026-09-09

Vừa hoàn thành: xác định root cause (cron `create:timesheet_detail` đêm 08/09 dừng ở id 27)
Đang làm dở: chưa sửa code, chưa xem được log server demo
Bước tiếp theo: @khoipv chốt hướng A/B/C; lấy `laravel-2026-09-08.log` trên demo để biết cron chết vì gì
Blocked: không truy cập được log server demo từ máy local

---

## Vòng điều tra 2 — truy tìm "vì sao cron không chạy hết"

Đã loại trừ được thêm, tất cả đều có bằng chứng:

- [x] **Không phải do đợt phân ca tạo lúc 14:30 ngày 08/09** — `shift_details` id 81
  ("Ca riêng Kho HN trực _T10.26", company 4) có kỳ hiệu lực **01/10→31/10/2026**,
  nằm ngoài điều kiện `start_at <= 2026-09-09 <= end_at` trong `getWorkshift()`.
- [x] **Không phải ranh giới công ty** — id 24, 25, 26, 27, 28, 29 đều `company_id = 4`.
- [x] **Không phải ranh giới phòng ban / bộ phận** — id 18, 19 đã có `part_id = 2`
  trước đó, nên `part_id = 7` của id 27 không phải trường hợp đầu tiên.
- [x] **Không phải do dữ liệu riêng của nhân viên 27** — id 27 (Huỳnh Thị Cam Thảo,
  `enter_date` 2021-11-10, `status` 1, `updated_at` 04/06/2026) không có gì bất thường;
  cron xử lý id 27 bình thường các ngày 26/08, 28/08, 01–04/09, 07/09, 08/09.
- [x] **Không phải hiện tượng lặp lại** — quét toàn bộ 120 nhân viên × các ngày
  01–11/09: không ngày nào khác bị đứt. Các ô trống còn lại chỉ là 4–6 nhân viên
  cố định (id 77, 165, 166, 179, và 186/187 trước 07/09) do chưa có cấu hình ca.
- [x] **Không phải `getWorkshift()` trả null** — nếu trả null thì vòng lặp bỏ qua
  im lặng, nhưng ngày 10/09 (đọc thẳng từ cấu hình) vẫn ra ca cho toàn bộ id 27–129
  ⇒ cấu hình có khớp, nghĩa là vòng lặp thật sự bị **cắt ngang**, không phải bị bỏ qua.

### Vì sao không thể chỉ đích danh nguyên nhân — đã tìm ra

Truy cập được log viewer trên demo: `GET /api/v1/logs`
(`routes/api.php:62`, `rap2hpoutre/laravel-log-viewer`, **không có middleware auth**).

Kết quả:
- `config/logging.php` → channel mặc định `stack` → `single` → `storage/logs/laravel.log`.
- Trên demo, `storage/logs/` chỉ có: `.gitignore`, `laravel-2024-05-18.log`
  (log của dự án khác, dừng ở 18/05/2024), `error.log` (chỉ CKFinder, mới nhất 14/06/2026),
  và **`laravel.log` RỖNG**.
- ⇒ **Không tồn tại bất kỳ log ứng dụng nào của ngày 08/09/2026.**

Cộng với 3 điều đã biết:
1. `createTimesheetDetail()` không có `try/catch`, không `Log::error`;
2. 2 lệnh cron nằm ngoài `app/Console/Kernel.php` nên không có `onFailure`/`withoutOverlapping`;
3. crontab hệ thống nhiều khả năng không redirect `>> file 2>&1`.

**Kết luận:** hệ thống hiện **không ghi lại gì khi cron chết**. Đây mới là root cause
thực sự cần sửa — sự cố đêm 08/09 chỉ là triệu chứng đầu tiên lộ ra. Bản thân lần
đứt đó là một gián đoạn tiến trình không tất định (bị kill / mất kết nối DB / lock),
và tín hiệu đó đã mất vĩnh viễn vì không nơi nào lưu.

- [ ] **A** (bọc try/catch + Log::error) — nâng lên mức **bắt buộc**, chờ @khoipv duyệt
- [ ] **C/D** (giám sát + đưa cron vào Kernel) — cần thiết để lần sau còn tra được
- [ ] Cân nhắc thêm: `/api/v1/logs` đang mở công khai, không auth → **rủi ro bảo mật**, nên chặn

### Checkpoint — 2026-09-09 (vòng 2)
Vừa hoàn thành: loại trừ toàn bộ giả thuyết dữ liệu/cấu hình; xác định hệ thống không có log
Đang làm dở: chưa sửa code
Bước tiếp theo: @khoipv chốt A (+C/D) rồi mới sửa
Blocked: không thể chỉ đích danh tín hiệu làm chết tiến trình vì log không tồn tại
