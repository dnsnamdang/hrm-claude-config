# Design — Cảnh báo & tự động đóng nhu cầu khách hàng theo Lĩnh vực Công ty kinh doanh

> Redmine **#11377**. Tóm tắt lại từ code đã bàn giao (nhánh `task_11377`, đã merge vào
> `tpe-develop-assign`) để làm nền cho bộ testcase. Không phải spec viết trước khi code.

## Mục tiêu

Nhu cầu khách hàng thu thập trong cuộc họp mà không lập thành Dự án TKT thì hệ thống tự nhắc rồi tự
đóng, thay vì treo vô thời hạn.

```
T = thời điểm cuộc họp phát sinh nhu cầu chuyển sang Hoàn thành  (meetings.completed_at)
N = "Thời gian hiệu lực nhu cầu (ngày)"   — khai ở TỪNG Lĩnh vực Công ty kinh doanh
M = "Cảnh báo trước khi đóng nhu cầu"     — tham số chung theo công ty, mặc định 3

Cảnh báo tại  T + N − M   (CHỈ khi N > M)
Tự đóng tại   T + N
```

## Phạm vi 3 màn

| Màn | Thay đổi |
| --- | --- |
| Danh mục › Lĩnh vực Công ty kinh doanh | Ô **N** trong popup Tạo/Sửa/Xem (bắt buộc, số nguyên 0–3650, có icon ⓘ) + cột **"Thời gian hiệu lực (ngày)"** trên bảng; N = 0 hiện chữ "Không thời hạn" |
| Cấu hình chung › Quản lý dự án › Cấu hình hạn | Ô **M** "Cảnh báo trước khi đóng nhu cầu" (mặc định 3, ≥ 0), vào nhóm trường được ghi Lịch sử cấu hình hạn |
| Nhu cầu khách hàng (+ tab "Nhu cầu của khách hàng" ở Công việc của tôi) | Cột **"Thời gian hết hạn nhu cầu"**: tô CAM + icon khi vào vùng cảnh báo, ghi chú `(còn X ngày)` / `(hết hạn hôm nay)` / `(quá hạn X ngày)`; không có hạn thì "Không thời hạn". Nút **Tạo Dự án TKT** ẩn khi nhu cầu đã đóng |

## Quyết định kỹ thuật đáng nhớ

1. **Mốc T trước nay không tồn tại** — `meetings` chỉ có `status` / `end_date` / `updated_at`, không có
   bảng lịch sử. Thêm cột `meetings.completed_at`, ghi bằng hook `saving()` của Entity (có 2 đường đổi
   trạng thái + cron auto-huỷ, đặt ở controller là sẽ có đường quên ghi). Chỉ ghi **lần đầu** chuyển
   Hoàn thành → sửa lại biên bản không đẩy lùi hạn. Backfill dữ liệu cũ = `end_date`.
2. **Không lưu cứng ngày hết hạn** — tính tại chỗ từ `completed_at + N`. N sửa được bất cứ lúc nào;
   lưu cứng thì đổi N xong dữ liệu cũ vẫn giữ hạn cũ mà không ai biết.
3. **N mặc định 0 = không đặt thời hạn**, cố ý KHÔNG backfill số dương — bật tính năng lên không được
   tự đóng oan nhu cầu nào.
4. **`closed_at` = đúng ngày hết hạn (T + N)**, không phải ngày cron chạy → cron chạy bù muộn không
   làm lệch số liệu kỳ.
5. **`expiry_warned_at`** chặn bắn cảnh báo lại mỗi ngày.
6. **N ≤ M → bỏ hẳn bước cảnh báo** (đúng yêu cầu: tránh xung đột mốc thời gian).
7. **Chặn lập Dự án TKT từ nhu cầu đã đóng ở BE**, không dựa vào FE ẩn nút — nhu cầu có thể bị cron
   đóng ngay lúc user đang mở form.

## File chính

**hrm-api** — `database/migrations/2026_09_14_000001_add_demand_due_days_to_internal_business_scopes_table.php` ·
`Modules/Assign/Database/Migrations/2026_09_14_000002_add_demand_expiry_columns.php` ·
`Entities/Meeting/{Meeting,MeetingInvestmentDemand}.php` · `Entities/InternalBusinessScope/InternalBusinessScope.php` ·
`Http/Requests/InternalBusinessScope/InternalBusinessScopeRequest.php` · `Services/{CustomerDemandService,MyJobService,ProspectiveProjectService}.php` ·
`Transformers/CustomerDemandResource/CustomerDemandListResource.php` · `Modules/Timesheet/Entities/GeneralRegulation.php` ·
`app/Console/Commands/Assign/CloseExpiredCustomerDemandsCommand.php` (cron `assign:close-expired-customer-demands`, chạy 01:20 hằng ngày).

**hrm-client** — `pages/assign/internal-business-scopes/{index.vue, AddScopeModal.vue}` ·
`pages/assign/settings/index.vue` + `components/DeadlineConfigHistoryModal.vue` ·
`components/assign/CustomerDemandList.vue`.

## Điểm lệch so với yêu cầu gốc (cần chốt lại với người viết yêu cầu)

| Yêu cầu ghi | Hệ thống đang làm | Ghi chú |
| --- | --- | --- |
| Badge trạng thái "Đã đóng" | Hiển thị **"Đóng"** | Nhãn có sẵn của màn Nhu cầu khách hàng (#11386) |
| Nút Tạo Dự án TKT "làm mờ kèm tooltip" | **Ẩn hẳn** | Quy ước dự án: nút không dùng được thì ẩn, không hiện mờ |
| M là "tham số toàn cục" | Lưu **theo công ty** trong Cấu hình chung | Bảng cấu hình vốn theo công ty; công ty chưa khai thì dùng mặc định 3 |
