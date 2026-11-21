# Điều tra chấm công app "load mãi" — NV Sầm Văn Linh (TPE) — @cuong61n

Redmine: chưa có số · Trạng thái: đã điều tra xong, không phải lỗi hệ thống (21/11/2026)

- [x] 21/11/2026 — Nhận phản ánh Zalo: NV Sầm Văn Linh (TPE, ca CT Urenco) vào app chấm công từ đầu giờ không được, bật wifi vẫn không được, app load mãi.
- [x] 21/11/2026 — Đọc code luồng chấm công (TPE_APP `check_in_out` + `TimekeeperController::checkTimesheet/store`): không dùng wifi; chặn bởi mã chấm công, thiết bị, ca/allow_app, GPS, bán kính địa điểm.
- [x] 21/11/2026 — Kiểm PROD (chỉ đọc): NV id 1769, ssn 12611198, thiết bị đã duyệt (status 2), ca CT Urenco allow_app=1 có 3 địa điểm; nginx 08:35 các API chấm công phản hồi 200 bình thường. Lưu ý `timesheets.employee_info_id` chứa ssn, không phải id hồ sơ.
- [x] 21/11/2026 — Kết quả: lượt chấm lúc 07:47:19 hôm nay ghi nhận thành công (Urenco 3) ~3 phút sau lúc phản ánh; 41 lượt từ 02/11, các ngày trước đều chấm bình thường → nhiều khả năng mạng/GPS điện thoại chậm tại thời điểm đó, không phải lỗi BE. Không sửa code.
