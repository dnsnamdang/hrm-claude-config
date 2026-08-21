# Plan — Mặc định bộ lọc BC số ngày công tác về tháng hiện tại

Phụ trách: @khoipv — 2026-08-19

## Bối cảnh

Màn `timesheet/dashboard`:
- Card trên hiển thị `Tháng 8 · 0 / 23 Công` (`cong_dinh_muc`, API `timesheet/dashboad`, luôn tính **tháng hiện tại**).
- Card dưới `Số ngày công chuẩn: 24` (`standard`, API `timesheet/reports/business-trip-assign-day-report`, tính **theo bộ lọc**).

Root cause: `BusinessTripAssignDayReport.vue` khởi tạo `from_month: '01'` và không có `to_month`
→ BE `ReportsController::businessTripAssignDayReport` lấy `$to_month = $request->to_month ?? $request->from_month` = `'01'`
→ tính công chuẩn cho **tháng 01**, không phải tháng hiện tại.

Kiểm chứng (`general_regulations.basis_for_calculating_weekend = 5` → `floor(ngày − T7/2 − CN)`):
- 01/2026: floor(31 − 2.5 − 4) = **24** ✅ khớp số dưới
- 08/2026: floor(31 − 2.5 − 5) = **23** ✅ khớp số trên

## Task

- [x] FE1 — `components/dashboad/BusinessTripAssignDayReport.vue`: `formFilter.from_month` mặc định = tháng hiện tại (2 chữ số) thay vì `'01'`
- [x] FE2 — Khai báo sẵn `to_month: ''` trong `data()` — **để RỖNG, không tự gen giá trị** (user chốt 2026-08-19). Chỉ khai báo key để Vue 2 reactive; `buildQueryString` (`utils/url-action.js:13`) lọc bỏ giá trị rỗng nên không gửi lên, BE tự lấy `$to_month = $request->to_month ?? $request->from_month`
- [x] V1a — Verify tĩnh: audit toàn client chuỗi "Số ngày công chuẩn" → chỉ 2 nơi. `pages/timesheet/report/business_trip_assign_day_report.vue:177` dùng `formFilter: {}` (trống, user tự chọn kỳ) → KHÔNG ảnh hưởng, không sửa
- [x] V1b — Verify tính toán: mô phỏng `AttendanceWatchRegulation::standard` với `basis_for_calculating_weekend = 5` (bản ghi `GeneralRegulation::first()`, id=1) → T08/2026 = 23, T01/2026 = 24, khớp đúng 2 số user thấy trên UI
- [x] V1c — Verify validation BE: `to_month` mới gửi lên qua rule `nullable|gte:from_month` → pass (cùng 2 ký tự)
- [x] V2 — **User verify UI**: mở `timesheet/dashboard` (hard refresh), card dưới phải hiện `Số ngày công chuẩn: 23` khớp card trên; đổi filter sang tháng khác vẫn tính đúng

## Phạm vi KHÔNG làm

- Không đổi label card (phương án 2 user chưa chọn)
- Không sửa BE `AttendanceWatchRegulation::standard` (hàm dùng chung, đang tính đúng)
- Không sửa việc gọi API 2 lần (watcher deep + `@change`) — đã báo user, chờ ý kiến

## Phát hiện phụ (đã báo user, CHƯA sửa — chờ ý kiến)

1. **Rule `gte` không có tác dụng** — `BusinessTripAssignDayReportSearchRequest.php:19`: `'to_month' => 'nullable|gte:from_month'`. Cả 2 là string không có rule `numeric` nên Laravel so sánh `mb_strlen`; mọi tháng đều 2 ký tự → luôn pass, kể cả `from_month=12, to_month=01`. Bug có sẵn, ngoài phạm vi.
2. **Gọi API 2 lần** — `BusinessTripAssignDayReport.vue` vừa có `watch formFilter` (deep) vừa có `@change="getData()"` trên các date-picker.

### Checkpoint — 2026-08-19
Vừa hoàn thành: FE1 + FE2 + V1a/V1b/V1c — `BusinessTripAssignDayReport.vue:140-145`: `from_month` = tháng hiện tại (`String(new Date().getMonth() + 1).padStart(2, '0')`), `to_month: ''` để rỗng theo yêu cầu user. Verify tĩnh + tính toán + validation đều PASS.
Đang làm dở: (không)
Bước tiếp theo: V2 — user mở `timesheet/dashboard` (hard refresh) verify card dưới hiện `Số ngày công chuẩn: 23` khớp card trên, rồi tự commit.
Blocked: (không)

**Lưu ý cần user quyết khi verify:** biểu đồ công tác giờ chỉ còn dữ liệu tháng hiện tại (trước đây là tháng 01). Nếu muốn biểu đồ xem cả năm mà chỉ số công chuẩn theo tháng → là yêu cầu khác, phải tách `standard` khỏi kỳ lọc (hoặc dùng phương án 2: ghi rõ kỳ vào label).
