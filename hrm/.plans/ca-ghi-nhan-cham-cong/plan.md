# Ca ghi nhận lịch sử chấm công — Plan

> Design: `.plans/ca-ghi-nhan-cham-cong/design.md` · Spec: `docs/superpowers/specs/2026-08-29-ca-ghi-nhan-cham-cong-design.md`
> Nhánh `tpe` (api + client) · @cuong61n

## Phase 1 — Nền tảng

### BE
- [x] Migration `add_is_attendance_only_to_working_shifts_table` (boolean, default 0, after `is_business_trip`) — không bọc DB::transaction
- [x] `WorkShift::$fillable` thêm `is_attendance_only`
- [x] `WorkShift::attendanceOnlyIds()` — static cache theo request
- [x] `ShiftDetailEmployeeDate::scopeExcludeAttendanceOnly()` — bọc `whereNull()->orWhereNotIn()` (bẫy NULL)
- [x] `CreateWorkShiftRequest` thêm rule `is_attendance_only`, giữ nguyên rule địa điểm/máy
- [x] `WorkShiftService::store()/update()` reset mọi trường tính công về 0 + xoá `punishment_rules` khi cờ bật

### FE
- [x] Checkbox "Ca chỉ ghi nhận lịch sử chấm công" + icon ⓘ tooltip ở đầu form `add-working-shift/_id`
- [x] Ẩn khối Nghỉ giữa ca / Số giờ-Số công / Đi muộn về sớm / Quên chấm công / Tăng ca-Ca đêm-Phụ cấp cơm / bảng phạt khi tick
- [x] Reset field bị ẩn về mặc định khi tick
- [x] Cảnh báo khi bật/tắt cờ trên ca đã có bản ghi phân ca

## Phase 2 — Chặn sinh timesheet_details (2 điểm)

### BE
- [x] `WorkShiftDetailService:471-477` lọc `excludeAttendanceOnly()` trước dispatch `CreateEmployeeByDateWorkingShift`; mảng rỗng thì bỏ dispatch
- [x] `ShiftDetailEmployeeDateController:91-107` bỏ qua tạo `TimesheetSummary`/`Detail` khi ca là attendance-only
- [x] **(kéo từ Phase 3)** `TimesheetService:822` — `getWorkshift` nhánh 2. Bắt buộc phải làm cùng Phase 2:
      `createTimesheetDetail` được **cron hằng ngày** gọi và đi qua hàm này, thiếu nó thì test Phase 2 pass giả

## Phase 2b — Vá lỗ hổng phân quyền (phát sinh, user duyệt)

### BE
- [x] Gắn `checkPermission:Quản lý ca làm việc` cho `POST /timesheet/timeworking`, `DELETE /{id}`, `PUT /{id}/toggle-lock`
- [x] Kiểm trước khi vá: cả 8 người từng tạo ca đều có quyền id 8 qua role → không chặn nhầm ai

## Phase 3 — Loại trừ khỏi phép tính (16 điểm)

### BE — Eloquent (13)
- [x] `TimesheetService:822` — `getWorkshift` nhánh 2 *(đã làm ở Phase 2)*
- [x] `LateEarlyOutService:268` — bản copy của `getWorkshift`
- [x] `TimesheetSummaryService:1468` — preload công định mức
- [x] `DashboadService:166` — vắng mặt không lý do
- [x] `AttendanceTrait:201` — `sumDate`, số ngày trừ phép
- [x] `AttendanceWatchRegulation:71` — `standard()`
- [x] `AttendanceWatchRegulation:170` — `$any`
- [x] `AttendanceWatchRegulation:179` — `$representative`
- [x] `AttendanceWatchRegulation:204` — `$representativeCount`
- [x] `AttendanceWatchRegulation:215` — `isWeekend()`
- [x] `AttendanceWatchRegulation:355` — `isWeekendLamThem()`
- [x] `AssignBusinessService:1671`
- [x] `StoreRiceSubsidy:45` — tiền cơm

### BE — raw query (3)
- [x] `TaskManagerByEmployeesReportService:330` — đã join `ws` → `where('ws.is_attendance_only', 0)`
- [x] `RequestSolutionService:543` — dùng `attendanceOnlyIds()`, bọc NULL
- [x] `RequestSolutionService:806` — như trên

## Phase 4 — Mở cổng chấm công (4 điểm)

### BE
- [x] `TimesheetService::getAttendanceOnlyShift($employeeInfo, $date)` + `getWorkshiftForAttendance()` (gộp ưu tiên ca thường → ca ghi nhận, dùng chung cho cả 4 điểm)
- [x] `TimekeeperController::checkTimesheet:109` — fallback khi không có ca thường
- [x] `TimekeeperController::store:407` — fallback + giữ nguyên `allow_app` và `checkCheckin()`
- [x] `TimesheetService::placeToCheckInOut:475` — lấy `place` của ca ghi nhận
- [x] `TimesheetService::allPlaceToCheckInOut:367` — như trên

## Phase 5 — Ký hiệu CC

### BE
- [x] Preload `$ccMap` trong `getDataTimesheet()` — join `timesheets` qua `employee_infos.ssn` (KHÔNG phải id), 1 query cho cả kỳ
- [x] ⚠️ Chèn `'CC'` **NGOÀI** vòng lặp `$timesheet_summaries` (spec ghi sai chỗ — xem ghi chú kiểm thử)
- [x] **(phát sinh)** `TimeSheetDetailModal.vue`: thêm `v-if` cho khối "Làm thêm" — thiếu guard làm popup vỡ

## Phase 6 — Nghiệm thu

- [x] Chụp 4 con số trước: công định mức · tổng công lương · số suất cơm · `COUNT(timesheet_details)`
- [x] Phân ca thử vào Chủ nhật → chạy lại → **4 con số y hệt**
- [x] Kiểm chiều ngược: NV có `working_shift_id IS NULL` — công định mức không giảm
- [x] Chấm công app: được phân → 200; ngoài bán kính → "Vị trí chấm công không hợp lệ"; `allow_app=0` → báo đúng
- [x] Chấm bằng máy chấm công vào được `timesheets`
- [x] Ca hiện trong dropdown `/shift-detail/add` + lưới `/shift-detail/general`; trùng ca ra 424
- [x] Ô Chủ nhật hiện `CC`; bấm mở popup thấy giờ + ảnh; Excel + bản in có `CC`; phân mà không chấm thì ô trống

## Kiểm thử Phase 1 — 2026-08-29 · **74 PASS / 0 FAIL**

Môi trường: nhánh `tpe`, FE :3000 (PID xác minh trỏ `hrm-client`), BE :8000 (`hrm-api/public`), DB `hrm_prod_local`.
3 tài khoản, 3 mức quyền: **TK1** `namdangit@gmail.com` (Super admin, cty 1, đủ quyền) ·
**TK2** `phuongdtk.nssg@tanphat.com` (Admin/HCNS CN Sài Gòn, cty **4**, có "Quản lý ca làm việc", chỉ xem theo công ty) ·
**TK3** `duyck.kd1@tanphat.com` (Kinh doanh, **không có quyền nào** về ca làm việc).

| Nhóm | Nội dung | KQ |
|---|---|---|
| 1 | Migration: cột tạo đúng, 36 ca cũ đều `= 0` | 2/2 |
| 2 | Helper + scope (tinker): loại đúng ca có cờ, giữ ca thường, không đụng 428.354 dòng thật, chạy được cả khi query có JOIN, xoá ca thì scope thành no-op | 10/10 |
| 3 | API lưu ca (3 tài khoản): reset đủ **22 trường** về 0, không tạo luật phạt dù FE gửi `modal_data`, ca thường giữ nguyên giá trị, bật cờ trên ca cũ thì xoá luật phạt, tắt cờ thì nhận lại giá trị, validate địa điểm giữ nguyên 422, cờ sai kiểu 422, không gửi cờ mặc định 0, `show` trả `is_attendance_only` + `has_shift_assignment`, TK2 lưu ra đúng `company_id = 4` | 39/40 |
| 4 | UI form (3 tài khoản): checkbox + icon ⓘ + tooltip, tick ẩn đúng 3 khối và cột trái giãn `col-7 → col-12`, bỏ tick hiện lại, giữ đủ 4 ô bắt buộc, lưu ra DB đúng, mở lại tick sẵn, ca đã phân thì hiện popup xác nhận và bấm Huỷ không đổi cờ, TK3 bị đẩy 404, TK2 dùng được | 39/39 |
| 5 | Ca có cờ **vẫn hiện** ở danh sách ca và **vẫn chọn được** ở dropdown `/shift-detail/add` (yêu cầu #7) · lịch sử ca ghi nhận dòng "Ca chỉ ghi nhận lịch sử chấm công: Có" | 8/8 |
| 6 | Hồi quy: 0 ca thật bị sửa, 0 ca thật bật cờ, `timesheet_details` 477.798 và `timesheet_summaries` 522.069 **không đổi**; đã dọn sạch toàn bộ dữ liệu test | 4/4 |

**Mốc số liệu nền cho Phase 6** (chụp lúc chưa có ca ghi nhận nào):
`shift_detail_employee_dates` = 428.354 · `timesheet_details` = 477.798 · `timesheet_summaries` = 522.069 · `working_shifts` = 36.

### Phát hiện trong lúc test

1. ⚠️ **Cảnh báo "bẫy NULL" ở bản spec đầu là BÁO ĐỘNG GIẢ** — `shift_detail_employee_dates.working_shift_id`
   khai **NOT NULL**, đếm thật 428.354 dòng cho **0 dòng** NULL/`0`. Cột nullable là `shift_detail_id`,
   đã nhầm hai cột. Đã sửa spec + design + STATUS + comment trong code; giữ `whereNull()` làm phòng vệ.
2. 🐞 **Lỗ hổng CÓ SẴN, không do feature này**: route `POST /timesheet/timeworking` (và `DELETE`,
   `PUT toggle-lock`) chỉ gắn `auth:api`, **không có `checkPermission`** → TK3 không có quyền
   "Quản lý ca làm việc" vẫn tạo/sửa ca được qua API (FE chặn ở `mounted`, BE thì không).
   Quyền id 8 đã tồn tại sẵn trong seeder. **Chờ user quyết có vá không.**
3. ⓘ `WorkShiftListResource` không trả `is_attendance_only` → màn danh sách ca không phân biệt được
   loại ca. Không nằm trong scope đã chốt; nêu ra để cân nhắc thêm badge.

### Checkpoint — 2026-08-29
Vừa hoàn thành: **Phase 1 code + kiểm thử xong, 74/74 PASS**. Migration đã chạy trên `hrm_prod_local`.
Ngoài plan: `WorkShiftDetailResource` trả `has_shift_assignment`; `WorkingShiftHistoryModal.vue` thêm nhãn cờ.
Đang làm dở: không có.
Bước tiếp theo: **Phase 2** — 2 điểm chặn sinh `timesheet_details`
(`WorkShiftDetailService:471-477` và `ShiftDetailEmployeeDateController:91-107`).
Blocked: chờ user quyết mục "Phát hiện #2" (vá lỗ hổng checkPermission hay để nguyên).

## Kiểm thử Phase 2 + 2b — 2026-08-29 · **57 PASS / 0 FAIL**

### Phase 2b — vá phân quyền (21 PASS)
TK3 (không quyền) bị chặn **403** ở cả 3 route ghi và **không** ghi được gì vào DB · TK3 vẫn `GET` được
danh sách/chi tiết/getAllList (không chặn nhầm route xem) · TK1 và TK2 (có quyền) tạo/khoá/xoá bình thường,
logic Phase 1 còn nguyên · không token vẫn là **401** chứ không phải 403.

### Phase 2 — chặn sinh timesheet_details (32 PASS, 3 đường + 1 unit, đều có ĐỐI CHỨNG)

| Đường | Ca ghi nhận | Đối chứng ca thường |
|---|---|---|
| A — `/shift-detail/add` → job | phân ca thành công, **không dispatch job**, 0 `timesheet_summary`, 0 `timesheet_detail` | **có** dispatch job |
| B — cron `create:timesheet_detail` | **không** tạo summary/detail | **có** tạo, trỏ đúng ca thường |
| C — lưới Tổng hợp phân ca | phân ca thành công, **không** tạo summary/detail | **có** tạo cả hai |
| unit — `getWorkshift()` | trả `NULL` (cả ngày hôm nay `has_shift_detail=true` lẫn ngày tương lai) | vẫn trả đúng ca |

Hồi quy: `timesheet_details` 477.798 · `timesheet_summaries` 522.069 · `shift_detail_employee_dates` 428.354 ·
`working_shifts` 36 · hàng đợi `jobs` về đúng 372 — **không đổi so với mốc nền**.

### ⚠️ Bắt được PASS GIẢ trong lượt test đầu

Lượt đầu chọn nhân viên bằng `employees.status = 1`, nhưng cả 2 chốt chặn của đường A và B lọc theo
**`employee_infos.status = 1`** (cột khác). NV 1321 và 1513 có `employee_infos.status = 0` → bị loại từ đầu,
nên TC7.1 và TC9 "PASS" **không phải nhờ bản vá**. Phát hiện được vì **ca đối chứng cũng fail**.
Đã chạy lại với 3 nhân viên `employee_infos.status = 1` (1466, 1468, 1599) và thêm **TC0 kiểm tiền đề**
(status + `enter_date <= hôm nay`) vào đầu bộ test để không tái diễn.

### Checkpoint — 2026-08-29 (Phase 2)
Vừa hoàn thành: **Phase 2b (vá quyền) + Phase 2 (3 điểm chặn), 57/57 PASS**, dữ liệu test dọn sạch.
Đang làm dở: không có.
Bước tiếp theo: **Phase 3** — còn **15 điểm** loại trừ khỏi phép tính (12 Eloquent + 3 raw query),
điểm `TimesheetService:822` đã làm ở Phase 2.
Blocked: không có.

## Kiểm thử Phase 3 — 2026-08-29 · **33 PASS / 0 FAIL**

### Rà phủ (audit tự động)
Quét toàn bộ 41 query đọc `shift_detail_employee_dates` trong `Modules/`, `app/`, `database/`:
**18 đã loại trừ** (15 điểm Phase 3 + 3 điểm Phase 2) · **23 cố ý giữ** = 7 seeder chạy một lần +
16 đường hiển thị/phân ca. Đã soi tay từng chỗ trong 23 chỗ giữ, đặc biệt:
`WorkShiftDetailService:391` (nguồn cảnh báo trùng ca 424 — phải giữ để quyết định #4 chạy) và
`WorkShiftService:128` (`checkCanDelete` — phải đếm cả phân ca của ca ghi nhận).

### Gom về một đầu mối
Thêm `WorkShift::applyExcludeAttendanceOnly($query, $column)` dùng cho **query raw** (`DB::table`),
và cho `ShiftDetailEmployeeDate::scopeExcludeAttendanceOnly()` uỷ quyền vào đó → điều kiện
`is_attendance_only` chỉ tồn tại ở **một chỗ duy nhất** trong toàn hệ thống.

### Kết quả (mỗi phép đo đều có ĐỐI CHỨNG NGƯỢC)

| TC | Nội dung | Ca ghi nhận | Đối chứng |
|---|---|---|---|
| 11 | `AttendanceWatchRegulation::standard()` | công định mức 10, không phải 14 | NV đối chứng cũng 10 |
| 12 | `isWeekend()` | CN có ca ghi nhận **vẫn là ngày nghỉ** | ngày thường vẫn = false |
| 13 | `isWeekendLamThem()` | CN vẫn tính ngày nghỉ (hệ số tăng ca đúng) | ngày thường đúng |
| 14 | Báo cáo giao việc `SUM(labour_hour)` | 80h (10×8), không cộng 4 CN | NV đối chứng 80h |
| 15 | Hạn phản hồi phiếu giải pháp (raw) | đếm 10 ngày, 0 ngày CN lọt vào | — |
| 16 | Tiền cơm | CN không phát sinh suất | ngày thường **có** suất |
| 17 | Công tác/giao việc | không nhận ca ghi nhận | vẫn nhận ca thường |
| 18 | Dashboard vắng mặt | không bị tính "phải đi làm" | ngày thường tính đủ 2 NV |
| 19 | Đường hiển thị | lưới phân ca **vẫn thấy đủ 14 bản ghi** | 4 trong đó là ca ghi nhận |
| 21 | `sumDate()` — số ngày trừ phép | 11 → **11** (không đổi) | đổi sang ca thường → **tăng** |

### ⭐ Nghiệm thu công định mức qua API thật (`timesheet/timesheet_summaries`, 10 PASS)

Đúng endpoint mà màn `/timesheet/timesheet_details` gọi, lọc theo mã nhân viên:

| Bước | `cong_dinh_muc` |
|---|---|
| 10 ngày ca thường | **10** |
| + 4 Chủ nhật ca GHI NHẬN | **10** ← không đổi |
| đổi 4 CN đó sang ca THƯỜNG | **14** ← phép đo có tác dụng |

Toàn bộ 6 chỉ tiêu (`cong_dinh_muc`, `tong_cong_tinh_luong`, `cong_lam_viec`, `nghi_khong_ly_do`,
`lam_them`, `vdm`) đều y hệt trước/sau. Bước thứ ba là **bằng chứng phép đo đủ nhạy** — thiếu nó thì
"không đổi" có thể chỉ là do đo sai chỗ.

### ⚠️ Bắt thêm 2 PASS GIẢ nữa (đều nhờ đối chứng ngược)
1. Lượt đầu gọi bảng công với `limit=200` nhưng 2 NV test **không nằm trong 200 dòng đầu** →
   `None == None` thành "PASS". Sửa: lọc bằng `keyword=<mã NV>` + thêm **TC20.0 kiểm tiền đề**
   bắt buộc lấy được đúng dòng và `cong_dinh_muc` khác `None`.
2. Insert `working_shifts` bằng SQL thô thất bại (thiếu cột NOT NULL) → id rỗng → mọi bước sau
   chạy rỗng mà vẫn "PASS". Sửa: tạo ca qua **API thật** như các lượt trước.

### Hồi quy
`working_shifts` 36 · cờ bật 0 · `shift_detail_employee_dates` 428.354 · `timesheet_details` 477.798 ·
`timesheet_summaries` 522.069 · `jobs` 372 — **không đổi so với mốc nền**. Dữ liệu test đã dọn sạch.

### Checkpoint — 2026-08-29 (Phase 3)
Vừa hoàn thành: **Phase 3 xong 15/15 điểm, 33/33 PASS**, kèm audit phủ 41 query.
Đang làm dở: không có.
Bước tiếp theo: **Phase 4** — mở cổng chấm công (`getAttendanceOnlyShift` + 4 điểm gọi bổ sung).
Blocked: không có.

## Kiểm thử Phase 4 — 2026-08-29 · **25 PASS / 0 FAIL**

Chấm công **thật qua API** bằng tài khoản nhân viên (`thinhbt.kddau@tanphat.com`, NV 1466),
công ty 1 có `max_distance = 200m`, ca khai địa điểm tại `21.028511, 105.804817`.

| TC | Tình huống | Kết quả |
|---|---|---|
| 22 | **Đối chứng âm** — chưa phân ca gì | 422 "Chưa có ca làm việc hoặc đăng ký làm thêm" |
| 23 | Phân ca GHI NHẬN → `checkTimesheet` | **200** — cổng đã mở |
| 24 | Ca ghi nhận `allow_app = 0` | 422 "Ca làm việc không cho phép chấm công bằng điện thoại" |
| 25 | Chấm công cách **~13m** | **200**, có bản ghi trong `timesheets`, ghi bằng `ssn` đúng schema |
| 26 | Chấm công cách **~5km** | 422 "Vị trí chấm công không hợp lệ", **không** ghi bản ghi nào |
| 27 | Sau khi chấm | **0** `timesheet_summary`, **0** `timesheet_detail` — không rò sang tính công |
| 28 | **Đối chứng** — ca THƯỜNG | vẫn `checkTimesheet` 200 và chấm công 200 như cũ |
| 29 | Máy chấm công (Hikvision + ZKTeco) | **0 tham chiếu** tới ca/phân ca, **0 dòng bị sửa** — khớp spec mục 2.4 |
| 30 | `getAttendanceOnlyShift` chỉ nhận ca có cờ | ca thường → NULL; ca ghi nhận → đúng ca; `getWorkshift` vẫn NULL |
| 31 | Dữ liệu **lệch** (có cả 2 ca cùng ngày) | `getWorkshiftForAttendance` ưu tiên **ca thường** |
| 32 | Chưa có ca nào bật cờ | trả NULL an toàn, không lỗi |

Điểm cốt lõi được chứng minh: **cổng chấm công mở, nhưng kiểm tra vị trí và `allow_app` vẫn nguyên vẹn**
(yêu cầu #4), và bảng công tuyệt đối không sinh gì.

### Ghi nhận trong lúc test (không thuộc feature này)
1. Ca THƯỜNG muốn chấm công thì **phải có sẵn `timesheet_detail`** của ngày đó (cron/job sinh) —
   `getWorkshift()` với ngày ≤ hôm nay đọc `timesheet_details` chứ không đọc bảng phân ca.
   Đây là hành vi CÓ SẴN; lượt test đầu tôi thiết kế sai đối chứng vì quên điều này.
   Ca ghi nhận **không** vướng ràng buộc đó nhờ đường tra riêng.
2. 🐞 **Bug có sẵn**: `TimekeeperController::store` dòng 427 đọc thẳng `$timekeeper['timesheet_type']`
   trong khi `$request->only([...])` bỏ qua key không gửi → thiếu tham số là `Undefined index`
   rồi trả 400 "Chấm công thất bại" thay vì 422 có thông báo. App luôn gửi nên không lộ.
3. ⓘ `checkCheckin()` trả `true` khi danh sách địa điểm rỗng — nghĩa là gửi `timesheet_type` khác
   `'workshift'` thì **không kiểm vị trí**. Đã có sẵn từ trước; là lý do spec yêu cầu ca ghi nhận
   BẮT BUỘC khai địa điểm.

### Hồi quy
`working_shifts` 36 · cờ bật 0 · `shift_detail_employee_dates` 428.354 · `timesheet_details` 477.798 ·
`timesheet_summaries` 522.069 · `jobs` 372 — không đổi. 0 bản ghi chấm công test còn sót.

### Checkpoint — 2026-08-29 (Phase 4)
Vừa hoàn thành: **Phase 4 xong, 25/25 PASS**. Chấm công app hoạt động với ca ghi nhận, vị trí vẫn được kiểm.
Đang làm dở: không có.
Bước tiếp theo: **Phase 5** — ký hiệu `CC` trên `/timesheet/timesheet_details`
(preload `$ccMap` join `timesheets` qua `employee_infos.ssn`, chèn vào `$item_day`).
Blocked: không có.

## Kiểm thử Phase 5 — 2026-08-29 · **19 PASS / 0 FAIL**

### ⚠️ Spec mục 5.5 ghi SAI chỗ chèn — sửa khi code
Spec bảo chèn `'CC'` vào `$item_day` trong vòng lặp dựng ô (`:1525-1601`). Nhưng vòng lặp đó là
`foreach ($timesheet_summaries ...)` — **chỉ chạy cho ngày CÓ `TimesheetSummary`**, mà ca ghi nhận
cố ý không sinh bản ghi đó. Chèn theo spec thì `CC` **không bao giờ hiện**.
Đã chuyển sang gắn **sau** vòng lặp, ngay trước `array_push($data, $item)`, và xử lý cả trường hợp
ô đã có nội dung thì nối `<br>CC`.

### Tối ưu ngoài spec
Spec đề xuất một query join `timesheets` qua `employee_infos.ssn`. Thực tế `getDataTimesheet()`
**đã nạp sẵn `$timesheets` cho cả kỳ** ở đầu hàm → tái dùng, chỉ thêm **1 query** cho bảng phân ca.
Vẫn phải map `id → ssn` vì `timesheets.employee_info_id` chứa **ssn**.

### Kết quả API (11 PASS)
Cột ngày Chủ nhật có sẵn trong `label` (`TimeWorking::getLabelTimeWorkingNew` sinh đủ mọi ngày) ·
phân ca + **có** chấm công → ô = `CC` · phân ca **không** chấm → ô **trống** · nhân viên khác không bị
gán nhầm · ca thường + chấm công → **không** có `CC` · chấm nhiều lần trong ngày → vẫn **một** chữ `CC` ·
`cong_dinh_muc` không đổi · xoá phân ca → `CC` mất nhưng **bản ghi `timesheets` giữ nguyên**.

### Kết quả UI (8 PASS, đã xem bằng mắt)
Màn `/timesheet/timesheet_details` tháng 08/2026, NV 12510705:
**`CC` ở cột CN 09** (có chấm công) · **cột CN 16 trống** (phân ca nhưng không chấm) ·
**Công định mức = 26 không đổi** · bấm ô `CC` mở popup: tab "Tổng hợp" **không** hiện số công,
tab "Dữ liệu chấm công" hiện đủ **08:05** và **17:35**, địa điểm, hình thức "App điện thoại".

Excel dùng **chung endpoint và chung chuỗi ô** (`item[definition.key]`), `formatDisplay` đổi `<br>` → xuống dòng
⇒ `CC` tự sang Excel, không cần code riêng.

### 🐞 Bug CÓ SẴN phải sửa vì chặn quyết định #3
`TimeSheetDetailModal.vue` — khối **"Làm thêm"** đọc `timesheetSummary.overtime_hour` mà **không có `v-if`**,
trong khi `TimesheetSummaryService::detail()` trả `null` cho ngày không có bảng công →
`TypeError: Cannot read properties of null` và **popup không mở**. Lỗi này có từ trước (bấm ô trống
bất kỳ đều vỡ), nhưng quyết định #3 yêu cầu bấm ô `CC` phải xem được giờ chấm nên bắt buộc sửa.
Đã thêm `v-if="timesheetSummary"` — file CRLF, đã giữ nguyên (296 → 299 CR, đúng +3 dòng).

⚠️ Kết luận ở Phase 1 rằng "popup không phải sửa dòng nào" là **SAI** — lúc đó tôi soi các `v-if`
sẵn có mà bỏ sót đúng khối này. Chỉ lộ ra khi bấm thật trên UI.

### Hồi quy
`working_shifts` 36 · cờ bật 0 · `shift_detail_employee_dates` 428.354 · `timesheet_details` 477.798 ·
`timesheet_summaries` 522.069 · `timesheets` 751.558 · `jobs` 372 — không đổi. Dữ liệu test đã dọn sạch.

### Checkpoint — 2026-08-29 (Phase 5)
Vừa hoàn thành: **Phase 5 xong, 19/19 PASS**, đã nhìn tận mắt `CC` trên màn và popup giờ chấm.
Đang làm dở: không có.
Bước tiếp theo: **Phase 6** — nghiệm thu tổng (4 con số trước/sau trên 1 phòng ban 1 tháng,
kiểm chấm công máy, xuất Excel + bản in có `CC`).
Blocked: không có.

## Kiểm thử Phase 6 — Nghiệm thu tổng · 2026-08-29 · **58 PASS / 0 FAIL**

### ⭐ TC40 — Nghiệm thu quy mô THẬT: cả phòng ban, cả tháng
Phòng **52 (PHÒNG KD VẬT TƯ THIẾT BỊ BÔI TRƠN)** — **21 nhân viên**, tháng 08/2026,
**504 bản ghi phân ca thật** đang có sẵn.

| Bước | Kết quả |
|---|---|
| Chụp mốc | tổng công định mức cả phòng **508.0** · `timesheet_details` 477.798 · `timesheet_summaries` 522.069 |
| Phân ca ghi nhận **21 NV × 5 Chủ nhật = 105 bản ghi** | phân thành công |
| Đo lại **21 NV × 16 chỉ tiêu = 336 phép so** | **0 lệch** |
| Tổng công định mức | **508.0 → 508.0** |
| `timesheet_details` / `timesheet_summaries` | không đổi |
| **Đối chứng ngược** — tắt cờ ca thành ca thường | tổng công định mức **TĂNG**, đổi trên **cả 21/21 NV** |

16 chỉ tiêu so gồm: công định mức, tổng công tính lương, công làm việc, công tác, nghỉ phép, nghỉ chế độ,
nghỉ không lý do, nghỉ không lương, nghỉ lễ hưởng lương, làm thêm, đi muộn, về sớm, số lần đi muộn,
số lần về sớm, trừ đi muộn về sớm, công ca đêm.

### TC41 — Tiền cơm (chạy lệnh cron thật)
`php artisan rice:store-rice-subsidy 2026-08-09 2026-08-09` → **0 suất cơm** phát sinh cho 21 NV được
phân ca ghi nhận. Đã dọn bản ghi do test tạo, bảng về đúng 22.459.

### TC42 — Máy chấm công
Ghi thẳng vào `timesheets` đúng cách `FetchAttendanceCommand` làm (ssn + `machine_type_id`), **không cần
phân ca, không bị chặn** → ô Chủ nhật hiện **CC**. NV khác cùng phòng không chấm → ô trống.

### TC43 — Lưới Tổng hợp phân ca
`GET timesheet/shift_details/general` (tham số `day[]`) → **200**, lưới **có** ca ghi nhận và nhân viên
được phân. Đúng yêu cầu #7: dùng nguyên màn sẵn có.

### TC45 — Xuất Excel (tải file thật)
Bấm "Xuất excel" trên màn → tải `bảng chấm công chi tiết tháng 08-2026.xlsx`, giải nén XML thấy
**`<t>CC</t>`** và mã nhân viên. `CC` sang Excel không cần code riêng.
ⓘ Màn `timesheet_details` **không có nút In** → mục "bản in" trong spec không áp dụng cho màn này.

### Hồi quy cuối
`working_shifts` 36 · cờ bật 0 · `shift_detail_employee_dates` 428.354 · `shift_details` 27 ·
`timesheet_details` 477.798 · `timesheet_summaries` 522.069 · `timesheets` 751.558 ·
`rice_registration_rice_supports` 22.459 · `jobs` 372 — **tất cả về đúng mốc nền**.

---

## TC44 — Quyết định #4 (chặn trùng ca): ĐÃ VÁ theo hướng (a), user chốt

### Vấn đề tìm được
| Cách phân lần đầu | `shift_detail_id` | Ca khác đè lên | Trước khi vá |
|---|---|---|---|
| qua `/shift-detail/add` | có giá trị | qua `/shift-detail/add` | ✅ 424 "Cảnh báo trùng ca" |
| qua **lưới Tổng hợp phân ca** | **NULL** | qua `/shift-detail/add` | ❌ 200, phân ca cũ bị **xoá âm thầm** |

Nguyên nhân (bug CÓ SẴN): `WorkShiftDetailService:393` dùng `where('shift_detail_id','!=',$id)`.
SQL cho `NULL != 58` ra `NULL` ⇒ dòng không lọt vào kết quả ⇒ không phát hiện trùng, rồi bước xoá
(`:431-438`) gỡ luôn bản ghi cũ. Ảnh hưởng **mọi ca** phân qua lưới, không riêng ca ghi nhận.
Đáng lưu ý vì ca ghi nhận thường phân theo từng ngày lẻ → đường tự nhiên là dùng lưới.

### Bản vá
Bọc lại thành `where(fn($q) => $q->whereNull('shift_detail_id')->orWhere('shift_detail_id','!=',$id))`.
Giữ nguyên: bỏ qua dòng của chính bảng phân ca đang lưu · bộ lọc "trùng tên ca thì không cảnh báo" ·
cửa `is_replace` để user xác nhận rồi ghi đè.

### Bán kính ảnh hưởng — đo trên dữ liệu THẬT
- Toàn bảng: **1.616 / 428.354 dòng** có `shift_detail_id = NULL` = **0,38%**
- Ngày **≥ hôm nay**: **0 / 130.624** dòng NULL
- `CreateWorkShiftDetailRequest` bắt buộc `start_at >= hôm nay` ⇒ mọi lần lưu chỉ đụng ngày tương lai
⇒ **Bản vá KHÔNG thể sinh cảnh báo mới trên dữ liệu đang có.** Chỉ đổi hành vi với dòng NULL tạo từ nay
về sau (tức phân ca qua lưới) — đúng trường hợp cần chặn.

### Kiểm thử bản vá — **22 PASS / 0 FAIL**
| # | Ca | Kết quả |
|---|---|---|
| A | 2 lần đều qua `/shift-detail/add` | 424, danh sách nêu đúng tên ca ghi nhận |
| B | lần đầu qua **lưới** (NULL) → ca thường đè | **424** (trước khi vá là 200 im lặng) |
| R1 | NV chưa có phân ca gì | 200, không cảnh báo giả |
| R2 | SỬA chính bảng phân ca đó | 200, không tự cảnh báo về dòng của mình |
| R3 | phân lại **cùng một ca** | 200, bộ lọc trùng tên ca vẫn chạy |
| R4 | ca khác đè → 424; `is_replace=true` | 200, user vẫn ghi đè được sau xác nhận |
| R5 | phân cho **cả phòng 21 NV** ở khoảng ngày trống | 200, ghi 231 bản ghi, không NULL, không cảnh báo giả |
| R6 | bán kính trên dữ liệu thật | 0 dòng NULL ở ngày ≥ hôm nay |

⚠️ Lượt R5 đầu tiên "FAIL" là do tôi chọn nhầm khoảng ngày **đã có 4.554 bản ghi phân ca thật**
(`null_sd = 0`) → cảnh báo 424 ở đó đến hoàn toàn từ dòng có `shift_detail_id` thật, tức **hành vi y hệt
trước khi vá**, không phải hồi quy. Đã chạy lại ở khoảng sau ngày phân ca xa nhất (2027-07-01).

### Checkpoint — 2026-08-29 (Phase 6)
Vừa hoàn thành: **Phase 6 nghiệm thu tổng xong**, 336 phép so trên 21 NV không lệch, Excel thật có CC.
Đang làm dở: không có.
Bước tiếp theo: chạy test case nghiệm thu với người dùng thật, rồi commit.
Blocked: không có.

## Kiểm thử E2E toàn trình qua GIAO DIỆN (Playwright, chạy hiện màn hình) — 2026-08-29 · **47 PASS / 0 FAIL**

Chạy `headless=False, slow_mo=450` để xem trực tiếp thao tác. 12 ảnh chụp ở `scratchpad/e2e/`.
Đi trọn hành trình người dùng, **không dùng SQL để dựng dữ liệu ở các bước chính**:

| Bước | Làm gì qua UI | Kết quả |
|---|---|---|
| 1 | Mở form Tạo ca, tick cờ, điền, bấm Lưu | 3 khối Tính công / Cài đặt / Nghỉ giữa ca ẩn đúng lúc tick; DB cờ=1, **mọi hệ số tính công = 0** |
| 2 | Vào danh sách Ca làm việc | ca mới hiện bình thường |
| 3 | Lưới **Tổng hợp phân ca** → lọc Phòng ban + Nhân viên → bấm "+" ô ngày → popup chọn ca → Đồng ý | ca ghi nhận **có trong danh sách chọn ca**; ghi 1 bản ghi đúng ngày hôm nay, `shift_detail_id = NULL`; lưới hiện ca vừa phân |
| 4 | (kiểm DB) | **0** `timesheet_summary`, **0** `timesheet_detail` |
| 5 | Đăng nhập **tài khoản nhân viên**, chấm công qua API app | tiền kiểm 200 · chấm **sai vị trí → 422 "Vị trí chấm công không hợp lệ"** · chấm **đúng vị trí → 200**, lưu đúng 1 bản ghi |
| 6 | Bảng công chi tiết → thấy **CC** → bấm ô → tab "Dữ liệu chấm công" | popup hiện đúng lượt chấm: App điện thoại · Toà nhà Tân Phát · 29/08/2026 09:24:36 |
| 7 | Đo công định mức trước/sau | **26 → 26 không đổi**; đối chứng đổi sang ca thường → **26 → 1** |
| 8 | Phân ca thường đè lên ngày đã có ca ghi nhận | **424 "Cảnh báo trùng ca"**, nêu đúng tên ca ghi nhận (đường lưới `shift_detail_id=NULL` — chính ca mà bản vá xử lý) |
| 9 | Bấm "Xuất excel", tải file | file `.xlsx` thật chứa `<t>CC</t>` |
| 10 | Đăng nhập TK không quyền | bị đẩy 404 ở form; API trả **403** |

### 2 FAIL ở lượt đầu đều là LỖI KỊCH BẢN TEST, không phải lỗi sản phẩm
1. Khẳng định `cong_dinh_muc == 0` là **sai**: nhân viên đó không có ca thường nào trong tháng nên
   `calcStandardWithCache` rơi xuống nhánh dự phòng tính theo ngày nghỉ, ra **26** — và **26 trước cũng
   bằng 26 sau**, tức đúng hành vi mong muốn. Đã đổi sang phép so trước/sau + đối chứng ngược (26 → 1).
2. Bấm tab "Dữ liệu chấm công" bằng selector text chung không ăn; đổi sang `.nav-link` thì popup hiện đủ.

Ngoài ra 3 lần phải sửa kịch bản mới chạy được (không phải lỗi sản phẩm): nút Lưu là `btn-success` chữ
"Lưu" chứ không phải `.save-btn`; nút tìm kiếm của lưới là `button.search-button` (bấm `.btn-success`
trúng nhầm nút "Phân ca theo ngày"); popup chọn ca là **bảng bấm vào dòng**, không phải select2.

### Hồi quy sau E2E
36 ca · 0 cờ bật · 428.354 phân ca · 27 bảng phân ca · 477.798 `timesheet_details` · 522.069 `summaries` ·
751.558 `timesheets` · 372 job · **0 bản ghi rác**.

## 🐞 Bổ sung sau khi user dùng thật — 2026-08-29 · **8 PASS / 0 FAIL**

### Lỗi 1 — App KHÔNG chọn được ca để chấm công (điểm thứ 5 của luồng chấm công, Phase 4 bỏ sót)
User phân ca thành công nhưng trên app không có mục ca nào để chọn.
**Nguyên nhân**: `TimekeeperController::listTimesheetTypes` (dòng 148) — endpoint app gọi để dựng
danh sách ca/phiếu cho nhân sự **chọn trước khi chấm** — vẫn dùng `getWorkshift()`, hàm cố ý mù với
ca ghi nhận ⇒ không đẩy mục `workshift` nào vào danh sách.
Phase 4 chỉ vá 4 điểm (`checkTimesheet`, `store`, `placeToCheckInOut`, `allPlaceToCheckInOut`) và
test bằng cách **gọi thẳng** `POST /timekeeper`, nên không chạm tới đường app dựng danh sách chọn.
**Sửa**: dùng `getWorkshiftForAttendance()`. Đã rà lại **toàn bộ 6 nơi gọi `getWorkshift`**:
4 chỗ còn lại (validate tăng ca ×2, validate đơn đi muộn/về sớm, sinh bảng công) **đúng là phải mù**.

### Lỗi 2 — App gọi nhầm tên loại ca
Danh sách trả về `"Ca hành chính: <tên ca>"` do tiền tố gán cứng ⇒ nhân sự tưởng ngày đó có tính công.
**Sửa**: ca có cờ thì đổi tiền tố thành `"Ca ghi nhận chấm công: "`.

### Lỗi 3 — Popup bảng công để trống mục "Ca làm việc" (user phát hiện)
`TimesheetSummaryService::detail()` lấy tên ca qua `timesheet_details`, mà ca ghi nhận không sinh
bảng công ⇒ mục "Ca làm việc" trống trơn, không biết ngày đó phân ca nào.
**Sửa**: nếu không có bảng công thì tra thẳng bảng phân ca để vẫn hiện Tên ca / Mã ca / Giờ ca;
thêm dòng ghi chú xám *"Ca này chỉ ghi nhận lịch sử chấm công — không tính công cho ngày này."*
Các dòng Thời gian hợp lệ / Chốt điểm danh / Đi muộn / Về sớm vẫn ẩn (không có bảng công) — đúng bản chất.

### Kiểm thử (đều có đối chứng)
| Ca | Kết quả |
|---|---|
| NV có ca ghi nhận → danh sách app | **có** mục ca, đúng tên, kèm địa điểm |
| NV không phân ca gì | app **không** có mục ca |
| NV có ca **thường** | vẫn hiện, vẫn gắn nhãn "Ca hành chính" |
| Nhãn ca ghi nhận | "Ca ghi nhận chấm công: …", không còn gọi nhầm "Ca hành chính" |
| Popup bảng công, ca ghi nhận | hiện Tên ca / Mã ca / Giờ ca + ghi chú xám |
| Popup bảng công, ca thường | vẫn trả đúng ca + dữ liệu chốt điểm danh, **không** hiện ghi chú |

### Bài học
Phase 4 test **gọi thẳng API chấm công**, không đi qua đường app **dựng danh sách để chọn**.
Lỗi chỉ lộ khi user thao tác thật trên app. Với luồng có client riêng (mobile), phải liệt kê
**mọi endpoint client gọi** chứ không chỉ endpoint thực hiện hành động.

## Tài liệu HDSD — 2026-08-29

**File**: `.plans/ca-ghi-nhan-cham-cong/HDSD_Ca ghi nhan lich su cham cong.docx` — 25 trang, 19 ảnh chụp thật, 10 bảng.
**Generator**: `.plans/ca-ghi-nhan-cham-cong/gen_hdsd.py` (được version control).
**Ảnh nguồn**: `hdsd_ca_ghi_nhan_shots/` — 20 ảnh, CHỈ để local, `.gitignore` đã chặn (đã kiểm `git status`: không có `.png` nào).

Cấu trúc: Tổng quan (thuật ngữ · lịch sử tài liệu · giới thiệu · **bảng 8 quyền** · luồng tổng thể 5 bước)
→ Phần 1 Tạo ca → Phần 2 Phân ca (2 lối vào + cảnh báo trùng ca) → Phần 3 Nhân sự chấm công
→ Phần 4 Ký hiệu CC + popup → Phần 5 Sửa/Xoá/Lịch sử → Phần 6 Quy tắc nghiệp vụ + FAQ.

### Cách dựng
Ảnh chụp bằng **Playwright MCP**, thao tác THẬT trên hệ thống: tạo ca qua form, phân ca qua lưới
Tổng hợp phân ca (bấm dấu +, chọn ca, xác nhận), nhân sự chấm công thật qua API app, xem CC trên
bảng công, mở popup 2 thẻ, xem lịch sử ca, và kích hoạt cảnh báo trùng ca rồi bấm Huỷ.

⚠️ **Engine của team chạy Windows** (`hdsd_engine.py` cập nhật mục lục bằng PowerShell + Word COM).
Máy này là macOS → `gen_hdsd.py` **kế thừa `HdsdBuilder` và ghi đè đúng một hàm** `_update_fields_by_word`
bằng AppleScript, **KHÔNG sửa file trong `.claude/skills/`** (tài sản chung, phải qua PR).
Từ khoá đúng của Word for Mac: `update field` (cho field), `update` + `update page numbers`
(cho table of contents / table of figures), `repaginate`.

### Kiểm chứng trước khi giao
- Đã **đọc lại mục lục thật** trong file: đúng 9 tiêu đề cấp 1 và 24 tiêu đề cấp 2 của tài liệu này,
  số trang thật, **không còn dòng nào của file khung**.
- Danh mục hình ảnh: 19 hình, đánh số tự động.
- Style so với `HDSD_MAU.docx`: Heading có định dạng tay **2/2**, run trong ô bảng **0/0**,
  mọi ảnh nội dung rộng đúng **6.0 inch**.
- `git status`: chỉ thấy `.docx`, `gen_hdsd.py`, `design.md`, `plan.md` — **0 file ảnh**.
- Đã dọn `__pycache__` sinh ra trong thư mục skill chung.

### Dữ liệu demo CỐ Ý GIỮ LẠI để user tự test app
Ca **`CC.LE` — "Ca ghi nhận chấm công ngày lễ"** (id 119) · phân cho **Bùi Thị Thịnh (1466)** và
**Trần Anh Tuấn (1599)** ngày 29/08/2026 · 2 lượt chấm công của Bùi Thị Thịnh.
Xoá khi không cần: `DELETE` theo `working_shifts.code = 'CC.LE'` và bản ghi phân ca / chấm công liên quan.
