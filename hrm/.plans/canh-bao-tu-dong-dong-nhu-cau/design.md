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
| Cảnh báo khi N <= M | **Thông báo**: bỏ qua (đúng spec) · **Màn danh sách**: vẫn tô cam | 2 luồng khác nhau - xem mục dưới |
| Đổi N ở danh mục | Nhu cầu đã có **giữ hạn cũ** (N chụp lúc tạo) | **Lệch spec, khách chốt lại** - xem mục dưới |
| Người nhận cảnh báo | Phụ trách nhu cầu **+ người tạo + người chủ trì** cuộc họp | Spec ghi 2 vai đầu; thêm người chủ trì vì cuộc họp có thể do người khác tạo hộ |
| Nội dung thông báo | Theo khuôn `notification-convention` | Skill thắng spec về hình thức trình bày |

## Quyết định đã chốt (30/09/2026)

### 1. SPEC LÀ NGUỒN - phản hồi QA KHÔNG phải căn cứ đổi nghiệp vụ

Bài học đắt nhất của feature này. QA báo "N = M không hiện cảnh báo" **3 lần** (18/09, 28/09,
30/09). Hai lần đầu trả lời đúng spec; lần thứ ba đã bỏ điều kiện `N > M` theo QA, rồi **phải
phục hồi ngay trong ngày** khi đọc lại spec:

> "Xử lý ngoại lệ (Logic Rule): Nếu N <= M ... Hệ thống tự động bỏ qua bước gửi thông báo cảnh
> báo này **để tránh xung đột mốc thời gian**." (mô tả Redmine #11377)

Spec quy định ngoại lệ này **có nêu lý do**, không phải sót. Và QA test theo bộ `testcase.xlsx`
- tài liệu do chính bên phát triển viết lại từ code - nên phản hồi của QA không thể dùng làm căn
cứ đổi nghiệp vụ. Muốn đổi nghiệp vụ phải qua người viết yêu cầu.

### 1b. ⚠️ NGOẠI LỆ `N <= M` CHỈ ÁP CHO THÔNG BÁO, KHÔNG ÁP CHO MÀN DANH SÁCH

Sai lầm tốn nhiều công nhất của feature này. Trong mô tả Redmine, ngoại lệ `N <= M` là **gạch
con của "Luồng 1 - Gửi thông báo nghiệp vụ"**, câu chữ là *"bỏ qua bước **gửi thông báo**
cảnh báo này"*. Mục "Ràng buộc tại Giao diện" của spec **không** đặt điều kiện nào cho cột hạn.

Ngày 22/09 khi sửa BUG 8, tôi bê điều kiện của cron sang màn danh sách. Hậu quả kéo dài 10 ngày:

- Nhu cầu có N nhỏ sắp tự đóng mà trên màn hình **không có dấu hiệu gì**.
- Mỗi dòng một N khác nhau, nên người test thấy *"chỉ hiện đúng một mốc ngày"* - đặt M = 2 thì
  dòng còn 2 ngày hiện, dòng còn 1 ngày lại ẩn (vì N của nó <= M). Nhìn như vùng cảnh báo không
  tích luỹ, trong khi thực ra nó vẫn tích luỹ đúng.
- QA báo đi báo lại; hai lần tôi trả lời "đúng spec" và một lần bỏ nhầm cả điều kiện ở cron.

**Luật đúng, mỗi nơi một kiểu - CỐ Ý:**

| | Điều kiện |
| --- | --- |
| Cột hạn màn danh sách (`attachDueDate`) | `M > 0 && today >= dueDate - M` - **không** có `N > M` |
| Thông báo chuông (`warningDays` của cron) | `N > M` - đúng ngoại lệ spec |

Cột hạn trả lời câu "nhu cầu còn mấy ngày nữa tự đóng" - đúng với mọi nhu cầu. Thông báo chuông
là một hành động riêng, có ngoại lệ riêng. **Đánh đổi phải chấp nhận**: nhu cầu `N <= M` được tô
cam trên màn hình nhưng không ai nhận chuông.

**Cách kiểm nhanh khi nghi ngờ** (chỉ đọc, không ghi DB): gọi thẳng `attachDueDate()` qua
Reflection với nhu cầu dựng trong bộ nhớ, nhiều N và nhiều mốc ngày - đừng chép lại công thức
bằng tay rồi mô phỏng, lần đầu tôi làm vậy và kết luận sai.

**Vấn đề còn tồn tại, chưa xử lý:** M mặc định = 3 mà nhiều lĩnh vực cũng đặt N = 3 - những nhu
cầu đó không bao giờ có thông báo chuông, và không có gì trên giao diện cho người quản trị biết.
Đề xuất **validate chặn lưu khi N <= M** ở form cấu hình. Đây là **rule mới ngoài spec**, chờ
người viết yêu cầu đồng ý.

### 2. Hạn nhu cầu theo N CHỤP LÚC TẠO - lệch spec, khách đã chốt lại

Spec không nói gì về việc N thay đổi; đọc theo nghĩa chữ thì hạn tính tại chỗ theo N hiện tại
của lĩnh vực (thiết kế ban đầu). Khách chốt lại theo hướng chụp snapshot, đúng TC 004 của QA:
đổi N thì **nhu cầu đã có giữ nguyên hạn**, chỉ nhu cầu tạo sau mới theo N mới.

Cột `meeting_investment_demands.due_days_snapshot`, một cửa duy nhất là
`MeetingInvestmentDemand::effectiveDueDays()`. `NULL` = bản ghi cũ chưa backfill, rơi về N hiện
tại; **phân biệt với snapshot = 0** (cố ý không đặt thời hạn) nên cột phải nullable.

**Đánh đổi:** không còn gia hạn được nhu cầu đang chạy bằng cách sửa N. Cần gia hạn thì phải làm
chức năng riêng - chưa có trong spec.

### 3. Người nhận cảnh báo - gửi đủ 3 vai

Spec ghi "Nhân sự phụ trách Nhu cầu / Người tạo cuộc họp" nhưng cron chỉ gửi cho người chủ trì
cuộc họp, bỏ hẳn người phụ trách nhu cầu. Nay gửi cho cả 3, loại trùng:
`currentOwnerId()` (phụ trách nhu cầu, đã tính cả trường hợp bàn giao #11386) ·
`meeting.created_by` · `meeting.host_employee_id`. Gửi thêm người chủ trì vì cuộc họp có thể do
người khác tạo hộ (user chốt).
