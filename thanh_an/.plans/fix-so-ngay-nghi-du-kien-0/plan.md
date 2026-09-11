# Fix: Số ngày nghỉ dự kiến = 0 (đơn xin nghỉ) — @khoipv

## Hiện tượng
Đơn **1619** (demothanhan.dnsmedia.vn) — Lê Bảo Trân, Phòng Cung ứng,
Nghỉ không lương, 31/08/2026 08:00 → 17:30, `total_days` lưu = **0** (đúng ra là 1).

## Điều tra — đã kiểm chứng trên chính server demo
- [x] Luồng: `add.vue:302 calcIntendDay()` → `GET timesheet/attendance/calculate-intend-day`
      → `AttendanceController.php:215` → `AttendanceTrait.php:170 sumDate()`
- [x] Gọi API demo với đúng 2 mốc thời gian của đơn 1619 → **total_days = 1** ⇒ BE tính ĐÚNG
- [x] `GET /timesheet/attendance/1619` → `total_days: 0` ⇒ số 0 nằm trong DB, do FE gửi lên
- [x] Màn xem đơn KHÔNG gọi lại `calculate-intend-day` ⇒ chỉ hiển thị giá trị đã lưu
- [x] Loại trừ ngày lễ: bảng `holidays` không có bản ghi nào ngày 31/08/2026
- [x] Loại trừ cuối tuần: 31/08/2026 là thứ 2
- [x] Tái hiện thao tác tạo đơn bằng Playwright — bắt được request trung gian:
      | # | tham số | kết quả |
      |---|---|---|
      | 1 | `end=2026-08-31 0:00:00` (vừa bấm chọn ngày, chưa chọn giờ) | **0** — 97ms |
      | 2 | `end=2026-08-31 17:00:00` | 1 — **613ms** |
      | 3 | `end=2026-08-31 17:30:00` | 1 — 122ms |
- [x] `sumDate()` trả 0 khi `end <= start` (vòng `while` không chạy lần nào)
- [x] Gõ tay giờ vào ô date-picker cũng bắn `@change` → không phải nguyên nhân

## Kết luận
Mỗi lần date-picker `@change` (chọn ngày, chọn giờ, chọn phút) đều bắn 1 request riêng.
Request đầu tiên (`end = 0:00`) trả **0**. `calcIntendDay()` gán thẳng
`this.form.total_days = rs.total_days` mà không hủy/bỏ qua response cũ,
nên nếu response 0 về sau response đúng thì 0 ghi đè. Độ trễ API đo được
dao động 97–613ms ngay trong phiên test ⇒ đảo thứ tự là hiện thực.

## Việc cần làm
- [ ] FE `add.vue:302` + `_id/index.vue:420`: chống race cho `calcIntendDay()`
      (tăng `requestId`, bỏ qua response cũ) — bắt buộc
- [ ] FE: bỏ qua/không gọi API khi `attendance_end_at <= attendance_start_at`,
      hiện cảnh báo thay vì gán 0
- [ ] BE `AttendanceRequest.php:73`: bật lại rule `total_days` (đang bị comment)
      → chặn lưu đơn 0 ngày. **Cần hỏi @khoipv rule cụ thể trước khi sửa**
- [ ] BE: tính lại `total_days` ở `AttendanceService::save()` thay vì tin FE (phòng thủ nhiều lớp)
- [ ] Sửa dữ liệu đơn 1619 → `total_days = 1`
- [ ] **Cần hỏi** `GeneralRegulation::getOfCurrentCompany()` đã comment mất phần lọc
      `company_id`, và `AttendanceWatchRegulation::isWeekend()/congWeekend()` nhận
      `$current_company_id` nhưng vẫn gọi `GeneralRegulation::first()`
      → mọi công ty dùng quy định công ty id=1 (basis=5). Đây là hàm dùng chung → hỏi trước khi sửa

## Ghi chú nghiệp vụ (không phải bug)
Đơn 1602, 1615 ngày **29/08/2026 (thứ 7, tuần thứ 5 → lẻ)** cũng ra 0 —
đúng theo `basis_for_calculating_weekend = 5` (nghỉ CN + thứ 7 lẻ).
Đã kiểm chứng: 22/08 (thứ 7 chẵn) = 1, 29/08 (thứ 7 lẻ) = 0.
Cần xác nhận lại quy định này có đúng ý nghiệp vụ không.

## Đối chứng các đơn lân cận (chốt: không phải lỗi hệ thống)
| Đơn | Người | Loại nghỉ | Thời gian | total_days | Đánh giá |
|---|---|---|---|---|---|
| 1617 | Nguyễn Quốc Đàn | Nghỉ phép | 31/08 08:00→17:30 | 1 | đúng |
| 1618 | Trần Thị Hoa | Nghỉ không lương | 31/08 13:30→17:30 | 0.5 | đúng |
| **1619** | **Lê Bảo Trân** | **Nghỉ không lương** | **31/08 08:00→17:30** | **0** | **SAI** |
| 1615 | Trần Thị Hoa | Nghỉ không lương | 29/08 (T7 lẻ) 13:30→17:30 | 0 | đúng theo cấu hình |
| 1602 | Nguyễn Thị P.Linh | Nghỉ không lương | 29/08 (T7 lẻ) 08:00→17:30 | 0 | đúng theo cấu hình |

⇒ Cùng ngày 31/08 + cùng khung giờ (1617) vẫn ra 1; cùng loại nghỉ (1618) vẫn ra 0.5.
⇒ Không phải lỗi loại nghỉ, không phải lỗi ngày. Quét 200 đơn gần nhất: chỉ 1619 sai.
⇒ Lỗi phụ thuộc thời điểm nhập ⇒ race condition, không phải lỗi tất định.

## Checkpoint — 2026-08-28
Vừa hoàn thành: chốt root cause đơn 1619 (race ở FE `calcIntendDay`)
Đang làm dở: chưa sửa code
Bước tiếp theo: chờ @khoipv duyệt phương án fix (nhất là 2 mục cần hỏi)
Blocked: không có

---

## Tái hiện thành công trên DEV (28/08/2026)

Môi trường: `https://dev-thanhan.dnsmedia.vn/timesheet/attendance/add`
Cách làm: hook `XMLHttpRequest.send` để **làm chậm có chủ đích 8 giây** request `calculate-intend-day` đầu tiên (mô phỏng lúc API trả chậm), rồi thao tác đúng như người dùng: nhập Từ ngày → chọn ngày 31 → chọn giờ 17 → chọn phút 30.

### Thứ tự response thực tế nhận được

| # | Query gửi lên | total_days trả về | Thời điểm về |
|---|---|---|---|
| 1 | `start=2026-08-31 8:00:00` → `end=2026-08-31 17:00:00` | 1 | 0.00s |
| 2 | `start=2026-08-31 8:00:00` → `end=2026-08-31 17:30:00` | 1 | 3.83s |
| 3 | `start=2026-08-31 8:00:00` → `end=2026-08-31 0:00:00` | **0** | **4.02s ← về sau cùng, ghi đè** |

Request #3 là request phát sinh **ngay khi click chọn ngày 31** (lúc đó giờ vẫn là `0:00` mặc định).
Vì `end (0:00) < start (8:00)` nên vòng `while` trong `sumDate()` không chạy lần nào → trả 0.
Nó về **sau cùng** nên ghi đè kết quả đúng.

### Trạng thái UI sau khi thao tác xong

```
Từ ngày:                      31/08/2026 8:00
Đến ngày:                     31/08/2026 17:30
Tổng số ngày nghỉ dự kiến:    0        ← SAI
```

Ảnh chụp: `bug-1619-tai-hien.png`

### Đã lưu và xác minh xuống DB

Bấm **Lưu** → BE **không chặn**, đơn được tạo thành công:

| id | attendance_start_at | attendance_end_at | total_days |
|---|---|---|---|
| **1571** | 2026-08-31 08:00:00 | 2026-08-31 17:30:00 | **0** |

Giống hệt đơn 1619 trên demo. **Root cause được xác nhận 100%.**
(Đơn 1571 trên dev là đơn test, lý do ghi rõ "TEST tai hien bug... co the xoa" — có thể xóa.)

### Checkpoint — 28/08/2026
Vừa hoàn thành: Tái hiện + lưu thành công trên dev, chứng minh race condition ở `calcIntendDay()` là nguyên nhân, và BE không có lớp chặn nào.
Đang làm dở: (không)
Bước tiếp theo: Chờ duyệt 4 hạng mục fix trong mục "Việc cần làm".
Blocked: Chờ xác nhận của @khoipv về hạng mục 2, 3, 4.

---

## Đã sửa code (28/08/2026)

### FE — sửa race condition (nguyên nhân gốc)

`hrm-thanhan-client/pages/timesheet/attendance/add.vue`
`hrm-thanhan-client/pages/timesheet/attendance/_id/index.vue`

- [x] Thêm biến `calc_intend_day_seq: 0` vào `data()`
- [x] `calcIntendDay()`: đánh số thứ tự mỗi request, response về mà `seq` không còn là số mới nhất thì **bỏ qua** → response chậm không ghi đè kết quả đúng nữa
- [x] `calcIntendDay()`: **không gọi API** khi `attendance_end_at <= attendance_start_at` (trường hợp vừa click chọn ngày, giờ còn 0:00) → cắt luôn nguồn sinh ra số 0

```js
if (moment(this.form.attendance_end_at).isSameOrBefore(moment(this.form.attendance_start_at))) {
    this.form.total_days = 0
    return
}
const seq = ++this.calc_intend_day_seq
this.$store.dispatch('apiGet', `${api_url}${params}`).then((response) => {
    if (seq !== this.calc_intend_day_seq) {
        return
    }
    this.form.total_days = response.data.data.total_days
})
```

### BE — lớp phòng thủ, tự tính lại total_days

`hrm-thanhan-api/Modules/Timesheet/Http/Requests/AttendanceRequest.php`

- [x] Thêm `recalculateTotalDays()` (private), gọi trong `prepareForValidation()`
- [x] Ghi đè `$this['total_days']` bằng kết quả `sumDate()` tính ở BE → **không tin giá trị FE gửi lên nữa**
- [x] Chạy ở `prepareForValidation()` nên cả `LeaveDayRule` / `LeaveDayNPRule` / `LeaveDayNBRule` lẫn dữ liệu lưu xuống DB đều dùng số đúng
- [x] Truyền `$employeeInfo` vào `sumDate()` để không phụ thuộc `auth()` (quan trọng khi người duyệt sửa đơn của người khác)
- [x] Thiếu dữ liệu / ngày ngược / không tìm thấy nhân sự → trả lại giá trị FE, để rule validate báo lỗi như cũ

**KHÔNG bật lại rule `total_days => required|numeric|min:0|lte:usable_leave_days`** (vẫn để comment).
Lý do: rule chặn `total_days = 0` sẽ **chặn nhầm đơn nghỉ cuối tuần hợp lệ** (đơn 1615, 1602 nghỉ thứ 7 lẻ có `total_days = 0` là đúng theo `basis_for_calculating_weekend = 5`). Và `usable_leave_days` không tồn tại trong request nên `lte` vô tác dụng.

### Kiểm chứng BE ở local (DB `thanhan_stag_07052026`)

| Trường hợp | Khoảng thời gian | sumDate trả về | |
|---|---|---|---|
| T2 cả ngày | 31/08 08:00 → 17:30 | **1** | ✅ đúng (đơn 1619 lẽ ra phải là số này) |
| Ngược (bug) | 31/08 08:00 → 00:00 | 0 | ✅ đã chặn từ FE, BE không tính nhánh này |
| T2 nửa ngày | 31/08 13:30 → 17:30 | **0.5** | ✅ |
| T7 lẻ (cuối tuần) | 29/08 08:00 → 17:30 | **0** | ✅ đúng — chứng minh không được bật rule chặn 0 |
| 2 ngày | 06/08 08:30 → 07/08 17:30 | **2** | ✅ |

Đã xác minh `$request['total_days'] = X` trong `prepareForValidation()` có đi vào `$request->only(['total_days'])` ở controller → lưu đúng xuống DB.

### Không làm (đã thống nhất với @khoipv)

- **Sửa data đơn 1619**: @khoipv tự sửa tay.
- **Lỗi bỏ qua `company_id`** trong `GeneralRegulation::getOfCurrentCompany()` và 5 hàm của `AttendanceWatchRegulation` (luôn dùng `GeneralRegulation::first()` → mọi công ty dùng quy định của công ty id=1): **tách thành task riêng**, ảnh hưởng rộng tới chấm công / tính lương / ngày công chuẩn, cần test kỹ.

### Checkpoint — 28/08/2026
Vừa hoàn thành: Sửa xong FE (2 file) + BE (1 file), kiểm chứng logic tính ngày ở local.
Đang làm dở: (không)
Bước tiếp theo: Deploy lên dev và test lại kịch bản làm chậm request — kỳ vọng ô "Tổng số ngày nghỉ dự kiến" giữ nguyên 1.
Blocked: Chưa test được end-to-end vì code sửa nằm ở local, dev/demo đang chạy bản cũ.

---

## Rà soát ảnh hưởng (28/08/2026) — có phát hiện, đã sửa bổ sung

### 1. FE: `moment()` không parse được chuỗi giờ không đệm 0 — ĐÃ SỬA

`value-type` của date-picker là `YYYY-MM-DD H:mm:ss` → chuỗi dạng `2026-08-31 8:00:00`.
`moment('2026-08-31 8:00:00')` **không** khớp ISO/RFC2822, moment rơi về `new Date()` và in deprecation warning ra console. Chrome vẫn ra đúng nhưng không đảm bảo trên browser khác (Safari cũ trả Invalid Date → guard mất tác dụng).

→ Sửa dùng format tường minh ở cả 2 file:
```js
const date_format = 'YYYY-MM-DD H:mm:ss'
if (moment(this.form.attendance_end_at, date_format).isSameOrBefore(moment(this.form.attendance_start_at, date_format))) {
```

### 2. BE: tính lại total_days sẽ ghi đè dữ liệu lịch sử — ĐÃ SỬA

Đo trên DB local (`thanhan_stag_07052026`, 400 đơn gần nhất):

```
Tổng kiểm tra: 400 | Khớp: 332 | LỆCH: 68 (17%) | Bỏ qua: 0
```

Ví dụ lệch:

| id | Thời gian | DB đang lưu | BE tính lại | Loại nghỉ |
|---|---|---|---|---|
| 1373 | 07/05 15:30 → 17:30 | 0.25 | 0.5 | Nghỉ không lương |
| 1335 | 17/04 08:00 → 18/04 17:30 | 2 | 1 | Nghỉ phép |
| 1230 | 21/02 08:00 → 12:00 | 0.5 | 0 | Nghỉ phép |
| 1284 | 23/03 08:00 → 24/03 17:30 | 0 | 2 | Nghỉ không lương |

Nguyên nhân lệch: công thức `sumDate()` và quy định cuối tuần (`basis_for_calculating_weekend`) đã thay đổi theo thời gian, đơn cũ lưu theo công thức lúc đó.

**Rủi ro**: FE khi mở đơn để sửa KHÔNG tự tính lại `total_days` (`mounted()` chỉ gán `this.form = response.data.data`). Nếu ai mở 1 trong 68 đơn này và lưu lại — kể cả chỉ sửa mỗi lý do — BE sẽ âm thầm ghi đè số ngày nghỉ. Đơn đã duyệt còn kéo theo số ngày phép đã trừ bị đổi.

→ Sửa: **chỉ tính lại khi thời gian nghỉ thay đổi**. Sửa đơn mà `attendance_start_at` / `attendance_end_at` không đổi → giữ nguyên `total_days` đã lưu.

```php
if (!empty($attendance)
    && $this->isSameDateTime($attendance->attendance_start_at, $this['attendance_start_at'])
    && $this->isSameDateTime($attendance->attendance_end_at, $this['attendance_end_at'])) {
    return $attendance->total_days;
}
```

Thêm helper `isSameDateTime()` so sánh qua `Carbon::parse()->format()` để không phụ thuộc định dạng chuỗi.
Vẫn chặn được bug vì race chỉ phát sinh khi người dùng thao tác chọn ngày/giờ → thời gian có thay đổi.

### Kiểm chứng lại sau khi sửa (đơn #1373, DB lưu 0.25, công thức mới ra 0.5)

| Kịch bản | Kết quả | |
|---|---|---|
| Sửa đơn, **giữ nguyên** thời gian | giữ **0.25** | ✅ không phá dữ liệu cũ |
| Sửa đơn, **đổi** thời gian | tính lại **0.5** | ✅ |
| Sửa đơn, gửi lại cùng giờ khác định dạng | giữ **0.25** | ✅ so sánh chuẩn |
| **Tạo mới**, FE gửi sai 0 (đúng bug 1619) | lưu **1** | ✅ bug bị chặn |

### 3. Đã kiểm tra, KHÔNG ảnh hưởng

- **`AttendanceRequest` chỉ dùng ở 1 chỗ**: `AttendanceController::store()` (dòng 190). Không có controller/mobile endpoint nào khác dùng.
- **Luồng duyệt đơn không bị đụng**: `storeApprove()` dùng `AttendanceApproveRequest`, chỉ lấy `only(['id','attendance_status','reason_of_approver'])` — không có `total_days`. Trong luồng duyệt chỉ có đúng 1 chỗ *đọc* `total_days` là `AttendanceController.php:151` (`>= 2` thì chuyển sang Chờ BGĐ duyệt), nhưng nó đọc từ DB nên đơn cũ không đổi; đơn mới chỉ đổi trong ca race hiếm, và riêng ca của đơn 1619 (0 → 1) thì cả hai đều `< 2` nên luồng duyệt giữ nguyên. **Kết luận: không ảnh hưởng luồng duyệt.**
- **`calcIntendDay()` chỉ tồn tại ở 2 file** đã sửa, không có màn nào khác gọi `calculate-intend-day`.
- **Kiểu cột `attendances.total_days` = `double NULL`** → chứa được 0.5 / 0.25.
- **`is_calc_holiday` BE lấy từ DB khớp với giá trị FE lấy từ `LeaveTypeListResource`** (`getListLeaveTypeByEmployee` chỉ ghi đè `usable_leave_days` cho loại Nghỉ phép, không đụng `is_calc_holiday`).
- **Rule validate hiện có không bị phá**: chạy thử toàn bộ 8 loại nghỉ × (ngày thường / thứ 7 lẻ) — kết quả giống hệt trước khi sửa. Riêng **Nghỉ không lương** là loại duy nhất cho phép `total_days = 0` (khớp thực tế đơn 1615, 1602). Các loại khác đã sẵn bị `LeaveDayRule` chặn với thông báo "Ngày nghỉ phải lớn hơn 0".

### 4. Ảnh hưởng có chủ đích (không phải lỗi)

- **`sumDate()` chạy thêm 1 lần lúc lưu.** Vòng lặp theo từng ngày, mỗi ngày có query `Holiday::isHoliday()` + `GeneralRegulation::first()`. Với đơn nghỉ dài (thai sản ~180 ngày) là vài trăm query. Không phát sinh mới về bản chất — endpoint `calculate-intend-day` đã làm y hệt mỗi lần chọn ngày — nhưng thao tác lưu sẽ chậm hơn với đơn dài. Nếu cần tối ưu thì cache `GeneralRegulation` và load trước danh sách ngày lễ, tách task riêng.
- **Khi người duyệt sửa đơn hộ nhân viên khác**: BE tính theo `employee_info` của **chủ đơn** (đúng), còn FE hiển thị số tính theo người đang đăng nhập. Hai số có thể lệch nếu ngày lễ chỉ áp dụng cho một số nhóm nghiệp vụ. BE đúng hơn, nhưng cần biết để không nhầm là lỗi.

### Checkpoint — 28/08/2026
Vừa hoàn thành: Rà soát ảnh hưởng, phát hiện và sửa 2 vấn đề (moment parse, ghi đè dữ liệu lịch sử). Kiểm chứng lại toàn bộ ở local.
Đang làm dở: (không)
Bước tiếp theo: Deploy dev, chạy lại kịch bản làm chậm request để xác nhận ô hiện 1.
Blocked: Chưa test end-to-end được vì dev/demo đang chạy bản cũ.
