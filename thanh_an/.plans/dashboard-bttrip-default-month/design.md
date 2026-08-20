# Design (tóm tắt) — Mặc định BC số ngày công tác về tháng hiện tại

Phụ trách: @khoipv — 2026-08-19 · Loại: bug fix (FE only)
Spec đầy đủ: `docs/superpowers/specs/2026-08-19-dashboard-bttrip-default-month-design.md`

## Mục tiêu

Màn `timesheet/dashboard` hiện 2 con số "công chuẩn" lệch nhau ngay cạnh nhau (`0 / 23` ở card trên vs `Số ngày công chuẩn: 24` ở card dưới) → user tưởng tính sai. Làm cho card dưới mặc định tính đúng kỳ đang xem.

## Root cause

Không phải lỗi tính toán — **hai card tính cho hai kỳ khác nhau**:

- Card trên (`cong_dinh_muc`, API `timesheet/dashboad`) → luôn tháng hiện tại.
- Card dưới (`standard`, API `timesheet/reports/business-trip-assign-day-report`) → theo bộ lọc, mà bộ lọc mặc định là `from_month: '01'` và thiếu `to_month`, nên BE lấy `$to_month = $request->to_month ?? $request->from_month` = `'01'` → tính cho **tháng 1**.

Kiểm chứng (`basis_for_calculating_weekend = 5` → `floor(ngày − T7/2 − CN)`): T01/2026 = 24, T08/2026 = 23 — khớp đúng 2 số user thấy.

## Quyết định lớn

- Chọn **PA1**: đổi mặc định bộ lọc về tháng hiện tại. (PA2 "ghi rõ kỳ vào label" và PA3 "cả hai" — user không chọn.)
- **Chỉ gen giá trị cho `from_month`**; `to_month` khai báo `''` (để trống) — user chốt không tự gen ô "Đến tháng". Vẫn phải khai báo key trong `data()` vì Vue 2 không reactive với key thêm sau; `buildQueryString` lọc bỏ giá trị rỗng nên không gửi lên, BE tự fallback `$to_month = $request->to_month ?? $request->from_month`.
- Không đụng BE, không migration, không quyền mới. Đúng 1 file FE.

## Scope

**Sửa:** `hrm-thanhan-client/components/dashboad/BusinessTripAssignDayReport.vue:140-145` — `from_month` = `String(new Date().getMonth() + 1).padStart(2, '0')`, `to_month: ''`.

**Không sửa:**
- `pages/timesheet/report/business_trip_assign_day_report.vue` (màn báo cáo riêng, `formFilter: {}` rỗng — không ảnh hưởng).
- `AttendanceWatchRegulation::standard` (hàm dùng chung, tính đúng).

## Hệ quả cần user xác nhận

Biểu đồ + bảng công tác giờ hiển thị dữ liệu **tháng hiện tại** thay vì tháng 1. Nếu muốn biểu đồ xem cả năm mà chỉ số công chuẩn theo tháng → là yêu cầu khác, phải tách `standard` khỏi kỳ lọc (hoặc quay lại PA2).

## Phát hiện phụ (đã báo user, chưa sửa)

1. Rule `'to_month' => 'nullable|gte:from_month'` vô hiệu — Laravel so sánh `mb_strlen`, mọi tháng đều 2 ký tự nên luôn pass (`from_month=12, to_month=01` vẫn qua). Bug có sẵn.
2. `BusinessTripAssignDayReport.vue` gọi API 2 lần mỗi lần đổi lọc (`watch` deep + `@change`).

## Trạng thái

Code xong, verify tĩnh/tính toán/validation PASS. **Chờ user verify UI** rồi tự commit.
