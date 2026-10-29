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

## Bảng thông báo tổng hợp (chốt đề xuất 29/10/2026)
Ký hiệu: GIỮ = có sẵn, không đổi · MỚI = bổ sung · SỬA = có sẵn nhưng thiếu/sai.

| Loại | Thông báo | Hiện trạng | Đề xuất | Gửi cho | Lúc nào |
|---|---|---|---|---|---|
| Nhiệm vụ | Tạo mới / Chờ duyệt / Đã duyệt / Từ chối / Yêu cầu làm lại / Góp ý | có | GIỮ | như hiện tại | theo thao tác |
| Nhiệm vụ | Nhắc báo cáo tiến độ | có (task có lịch báo cáo) | GIỮ | người thực hiện | 08:30/11:30/14:30/17:30 |
| Nhiệm vụ | Sắp đến hạn | chưa | MỚI | người thực hiện | 1 ngày trước hạn |
| Nhiệm vụ | Quá hạn | chưa | MỚI (1 lần) | người thực hiện | sáng hôm sau ngày hạn |
| Vấn đề | Tạo mới / Chờ duyệt / Từ chối / Góp ý | có | GIỮ | như hiện tại | theo thao tác |
| Vấn đề | Sắp đến hạn / Quá hạn | chưa | MỚI | người xử lý | như Nhiệm vụ |
| Meeting | Tạo mới / Chốt lịch / Đổi lịch / Thêm-bớt người / Hủy | có | GIỮ | người dự họp | theo thao tác |
| Meeting | Nhắc nhập biên bản, tự hủy | có | GIỮ | người tạo | trước hạn biên bản |
| Meeting | Nhắc nhận phòng | có (họp có đặt phòng) | GIỮ | người đặt + người dự | trước giờ theo cấu hình phòng |
| Meeting | Sắp bắt đầu | chưa | MỚI — chỉ họp KHÔNG đặt phòng (họp đặt phòng đã có nhắc nhận phòng) | người dự họp | trước 15 phút |
| Nhắc việc cá nhân | Đến giờ | chưa | MỚI | chính người tạo | đúng giờ hạn (không có giờ → chỉ vào bản tin) |
| Nhắc việc cá nhân | Quá hạn | chưa | MỚI (1 lần) | chính người tạo | sáng hôm sau |
| Phiếu giao việc | Chờ duyệt / Đã duyệt / Từ chối | có — Đã duyệt chỉ gửi NGƯỜI TẠO | GIỮ + SỬA: duyệt thì gửi thêm "Tạo mới: được giao" cho người thực hiện | người thực hiện | lúc duyệt |
| Phiếu giao việc | Sắp đến hạn / Quá hạn | chưa | MỚI | người thực hiện | 1 ngày trước deadline (phiếu ≥ 2 ngày) / sáng hôm sau |
| Phiếu giao công tác | Chờ duyệt / Đã duyệt / Từ chối / Cập nhật | có — Đã duyệt chỉ gửi NGƯỜI TẠO | GIỮ + SỬA: duyệt thì gửi "Tạo mới: được cử đi công tác" cho người đi | người đi công tác | lúc duyệt |
| Phiếu giao công tác | Sắp đến hạn (mai đi) / Nhắc nhập KQ / Quá hạn | chưa | MỚI | người đi công tác | 16:00 hôm trước ngày đi / sáng hôm sau ngày về / sáng hôm sau nữa nếu vẫn chưa nhập |
| Phiếu giao việc (chấm công) | Tạo mới (khi duyệt) / Chờ duyệt / Đã duyệt / Từ chối | có — người làm đã nhận | GIỮ | như hiện tại | theo thao tác |
| Phiếu giao việc (chấm công) | Quá hạn (chưa nhập KQ) | chưa | MỚI (1 lần) | người làm | sáng hôm sau |
| Phiếu đi công tác (chấm công) | Chờ duyệt / Tạo mới / Hủy | có — người đi đã nhận | GIỮ | như hiện tại | theo thao tác |
| Phiếu đi công tác (chấm công) | Sắp đến hạn (mai đi) / Nhắc nhập KQ / Quá hạn | chưa | MỚI | người đi | như Phiếu giao công tác |
| Chung | Bản tin sáng | chưa | MỚI | mỗi người có việc hôm nay | 07:30, trừ Chủ nhật |
| Chung | Tổng quá hạn | chưa | MỚI | người còn việc quá hạn | 07:30 thứ Hai |

Không thay thế/bỏ thông báo nào đang có. Nhắc quá hạn chỉ 1 lần/việc; việc nào đã có thông báo riêng trong ngày thì bản tin chỉ đếm, không lặp tên.

## Cấu hình nhắc theo giờ (chốt 29/10/2026)
- Mỗi công ty, mỗi loại việc 2 số: **nhắc trước hạn** và **báo quá hạn sau hạn** (giờ; Meeting tính phút). Thay cho mốc cứng "1 ngày".
- Mặc định: Nhiệm vụ / Vấn đề / Phiếu giao việc 24h trước · 0h sau; Phiếu giao việc (chấm công) 2h · 0h; Phiếu giao công tác / Phiếu đi công tác (chấm công) 24h trước GIỜ ĐI · 0h sau ngày về; Meeting 15 phút trước giờ họp; Nhắc việc cá nhân đúng giờ hạn · 0h.
- **Gửi đúng mốc tính theo cấu hình, kể cả ban đêm** — user chốt KHÔNG có khung giờ yên lặng, không dời sang bản tin.
- Màn cấu hình theo khuôn /meeting/settings (chọn công ty → hub "Nhắc hạn công việc" → ô số + nút Lịch sử), đặt ở phân hệ Công việc.
- Bỏ điều kiện "phiếu ≥ 2 ngày": mốc nhắc rơi trước lúc phiếu được duyệt thì bỏ lượt đó.

## Số liệu prod (hrm_erp_gop, tạo từ 01/10/2025, đọc 29/10/2026) → mặc định nhắc
| Loại | n | Độ dài p50 / p90 | Lập phiếu so với lúc bắt đầu |
|---|---|---|---|
| Nhiệm vụ | 32 | 89h / 209h (29% < 24h) | tạo→hạn p50 74h |
| Phiếu giao việc | 96 | 23h / 52h (61% < 24h) | lập SAU khi bắt đầu, p50 −8h |
| Phiếu giao công tác | 5,716 | 25h / 123h | lập p50 0.8h SAU giờ đi; 84% lập < 2h trước giờ đi |
| Phiếu giao việc (chấm công) | 12,481 | 1.9h / 9h (51% < 2h) | 87% lập < 2h trước khi bắt đầu |
| Phiếu đi công tác (chấm công) | 1,686 | 12h / 106h | 52% lập < 2h trước giờ đi |
| Meeting | 2,701 | — | lập p50 16h trước giờ họp; 37% < 2h |
| Nhắc việc cá nhân | 100 | tạo→hạn p50 31h / p90 270h | — |
| Vấn đề | 0 có hạn | — | — |
Kết luận: 1 con số giờ cố định không hợp → đề xuất nhắc trước = 25% độ dài, tối thiểu 1h, tối đa 48h (cấu hình được); bỏ "nhắc trước giờ đi" của công tác (phiếu lập sau khi đi), dùng % rule để nhắc trước giờ VỀ (kịp gia hạn); Phiếu giao việc (chấm công) không nhắc trước, chỉ báo quá hạn chưa nhập KQ; Meeting giữ 15 phút. Chờ user chốt.
