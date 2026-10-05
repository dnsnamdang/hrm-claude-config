# Dữ liệu tạo/sửa khi chụp HDSD Quy trình vòng đời meeting (02/10/2026, DB local_hrm_erp, tài khoản namdangit / DNS Admin)

| id | Mã | Tên | Trạng thái cuối | Ghi chú |
|---|---|---|---|---|
| 52 | TPE.MET.NB.26.0067 | Họp triển khai kế hoạch kinh doanh quý IV/2026 | Hoàn thành (3) | Tạo qua UI: Lưu nháp → Sửa thêm Nguyễn Văn Bình (66), Ngô Thị Hằng (212) → Lưu và Lên lịch → Xác nhận tham dự "Có mặt" → Lưu và Chốt lịch → điểm danh → biên bản 1 dòng + 1 tài liệu + kết luận → Hoàn thành |
| 53 | TPE.MET.NB.26.0068 | Họp rà soát tiến độ thu hồi công nợ tháng 10 | Hủy (4) | Tạo qua UI Lưu và Lên lịch, hủy với lý do "Hủy do mình bận đột xuất" + ghi chú |
| 54 | TPE.MET.NB.26.0069 | Họp chuẩn bị hội nghị khách hàng cuối năm | ĐÃ XÓA | Tạo Lưu nháp rồi xóa qua UI (chụp hộp Xác nhận xóa) |

Sửa bằng SQL (chỉ trên meeting demo 52, để chụp được Hoàn thành + thông báo hạn biên bản):
- `UPDATE meetings SET start_date='2026-10-02 15:45:00', end_date='2026-10-02 16:00:00' WHERE id=52;` (ban đầu 05/10/2026 09:00–10:30; lần thử đầu đặt 13:30 bị chặn vì phải ≥ thời gian tạo)

Tác dụng phụ: hệ thống đã gửi thông báo lên lịch/chốt lịch/hủy cho DNS Admin, Nguyễn Văn Bình, Ngô Thị Hằng; file tài liệu `Ke_hoach_kinh_doanh_Q4_2026.docx` đã upload lên S3 thật (tanphat_hrm/ke-hoach-kinh-doanh-q4-2026docx-1790931910-mpwJ.docx).
Không đổi mật khẩu tài khoản nào.
