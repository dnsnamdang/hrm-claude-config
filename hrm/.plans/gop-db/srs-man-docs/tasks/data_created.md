# Dữ liệu tạo cho SRS Nhiệm vụ (DB local_hrm_erp, nhánh gop_db)

Tạo ngày 03/10/2026 bằng `make_data.py` (gọi API :8003, tài khoản admin `employees.id = 13`).
Không sửa/xoá dữ liệu có sẵn; không đụng nhiệm vụ của phiên khác (15–24, 951–976).

| Bảng `tasks` id | Mã | Tên | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 977 | TPE.TASK.NB.26.0977 | Soạn hồ sơ năng lực gửi Trường CĐ Cơ giới và Thủy Lợi Đồng Nai | Nháp | 3 checklist, 2 tag, người làm Đỗ Đăng Hiếu — dùng chụp Sửa / Xem / Xóa |
| 978 | TPE.TASK.NB.26.0978 | Chuẩn bị tài liệu hướng dẫn vận hành cầu nâng 2 trụ | Đang thực hiện | người làm = admin — chụp Nhập kết quả; có 1 bình luận do admin viết |
| 979 | TPE.TASK.NB.26.0979 | Lập bảng khối lượng vật tư điện xưởng 3S Hyundai An Khánh | Hoàn thành - Chờ duyệt | đã nhập kết quả 7 giờ / 100% — chụp Duyệt kết quả |
| 980 | TPE.TASK.NB.26.0980 | Theo dõi tiến độ lắp đặt thiết bị xưởng Ford Hưng Yên | Đang thực hiện | bật Yêu cầu báo cáo tiến độ hằng ngày + 4 dòng nhật ký 29/09–02/10 |
| 981 | TPE.TASK.NB.26.0981 | Khảo sát hiện trạng điện xưởng 2S Phương Anh | Chờ phê duyệt triển khai | chụp Duyệt triển khai |
| 982 | TPE.TASK.NB.26.0982 | Triển khai bản vẽ bố trí thiết bị xưởng 3S Hyundai An Khánh | Chờ bắt đầu | nhiệm vụ cha có 2 nhiệm vụ con |
| 983, 984 | TPE.TASK.NB.26.0983/0984 | Vẽ mặt bằng bố trí khu sửa chữa chung / Vẽ mặt bằng khu đồng sơn | Chờ bắt đầu | nhiệm vụ con của 982 (hệ thống tự sinh) |
| 985, 986 | TPE.TASK.NB.26.0985/0986 | Cập nhật kế hoạch làm việc tuần 41 lên hệ thống | Chờ bắt đầu | 1 Nhiệm vụ chung → 2 nhiệm vụ (Đỗ Đăng Hiếu, Bùi Thị Mai) |

Bảng phụ sinh kèm: `task_checklists`, `task_tags`/`tags` (Hồ sơ thầu, Đồng Nai, Đào tạo, Bóc tách khối lượng, Lắp đặt, Bản vẽ),
`task_watchers`, `task_children`, `task_progress_report_rules`, `task_progress_logs` (task 980), `task_histories`,
`task_org_units`, `comments` (1 bình luận trên task 978), thông báo gửi cho người liên quan.
