# Nhắc hạn "Việc của tôi" (Mytodo) — @cuong61n

Nhánh: `hrm-api` / `hrm-client` develop · `TPE_APP` develop. Chốt với user 29/10/2026.

## Mục tiêu
Hệ thống chưa nhắc hạn cho Nhiệm vụ, Vấn đề, 4 loại phiếu, Nhắc việc cá nhân; người dự họp chưa được nhắc trước giờ họp.
Thêm nhắc hạn + bản tin sáng, gửi qua đường thông báo sẵn có `EmployeeInfoService::sendNotification`
(lưu DB → chuông web + màn Thông báo app; Redis socket → chuông web realtime; job SendNotification → push điện thoại).

## Quyết định đã chốt
1. **Hạn = lúc người nhận phải xong phần việc của mình (nhập kết quả)**, không lấy ngày bắt đầu:
   | Loại | Hạn | Nhắc |
   |---|---|---|
   | Phiếu giao việc (assign_jobs) | `deadline` | sáng ngày bắt đầu (bản tin) + trước deadline 1 ngày nếu phiếu ≥ 2 ngày |
   | Phiếu giao công tác (assign_requests type 2) | ngày về `to_time` (sau gia hạn/kết thúc sớm) | chiều hôm trước ngày đi + sáng hôm sau ngày về nhắc nhập KQ |
   | Phiếu giao việc (chấm công) (job_assignment_notes) | giờ kết thúc dự kiến muộn nhất | sáng ngày làm (bản tin) |
   | Phiếu đi công tác (chấm công) (business_trip_assigns) | ngày về (sau gia hạn/kết thúc sớm) | chiều hôm trước ngày đi + sáng hôm sau ngày về |
2. **Quá hạn = qua hạn mà chưa nhập kết quả, KHÔNG cộng thêm ngày** (cách A, kể cả phiếu công tác).
3. Phiếu đang chạy (qua ngày bắt đầu, chưa tới hạn) hiện "Đang diễn ra · còn n ngày", không tính quá hạn; thẻ ghi đủ "Đi … → về …".
4. Phiếu duyệt sau mốc nhắc → bỏ lượt nhắc trước.
5. **Quá hạn báo riêng đúng 1 lần** (sáng hôm sau ngày hạn). Quá hạn cũ chỉ là 1 con số cuối bản tin, không liệt kê tên.
6. **Bản tin sáng 07:30**, 1 thông báo/người, chỉ gửi khi hôm nay có việc (hạn hôm nay, họp hôm nay, đi công tác hôm nay/mai); không gửi Chủ nhật; ngày chỉ còn quá hạn cũ thì không gửi.
7. **Sáng thứ Hai** gửi 1 bản tổng quá hạn ("Bạn còn n việc quá hạn").
8. Tiền tố: bản tin / tổng quá hạn dùng `[VIỆC]`; nhắc từng phiếu dùng mã phiếu làm tiền tố. Nhóm hành động: `Sắp đến hạn` / `Quá hạn` / `Nhắc báo cáo` (đúng 14 giá trị skill notification-convention).
9. Tên loại: Phiếu giao việc · Phiếu giao công tác · Phiếu giao việc (chấm công) · Phiếu đi công tác (chấm công) — cả 4 còn dùng song song.

## Lỗi phát hiện, sửa kèm
- Danh sách lấy NGÀY BẮT ĐẦU làm hạn (assign_job/assign_business/ts_job/ts_business) trong khi lịch vẽ tới hạn chót.
- Danh sách lọc phiếu giao công tác status 4 (chỉ có ở phiếu đề xuất) → phiếu giao công tác không bao giờ hiện ở tab danh sách (đúng phải là status 3 Đã duyệt).
