# Dữ liệu đã tạo cho SRS Vấn đề (DB local_hrm_erp của gop_db-api)

Tạo qua API :8003 bằng tài khoản admin (employees.id 13), script `seed_data.py` → `seed_result.json`.
Tất cả gắn giải pháp 955 / dự án 152, hạng mục 955 hoặc 956; người theo dõi 970, người phối hợp 781.

| issues.id | Mã | Trạng thái cuối | Ghi chú |
|---|---|---|---|
| 3 | ISS-202610-0003 | new | Phòng ban xử lý 55, chưa có người phụ trách |
| 4 | ISS-202610-0004 | assigned | assignee 13, approver 148; có 1 bình luận (comments.id 2) |
| 5 | ISS-202610-0005 | in_progress | Hạn đã qua 2 ngày → Quá hạn |
| 6 | ISS-202610-0006 | resolved | assignee + approver = 13 (chụp Duyệt / Từ chối) |
| 7 | ISS-202610-0007 | completed | không người duyệt (chụp Mở lại) |
| 8 | ISS-202610-0008 | rejected | lý do từ chối có ghi |
| 9 | ISS-202610-0009 | closed | |
| 10 | ISS-202610-0010 | reopened | |

Bảng bị ghi kèm theo luồng chuẩn: `issue_watchers`, `issue_supporters`, `tags`/`issue_tags`, `issue_histories`,
`issue_org_units`, `comments`, thông báo (notifications) cho trưởng phòng 55 / người duyệt.
Không sửa / xoá bản ghi có sẵn (issue 1, 2 và 13, 14 do phiên khác tạo — giữ nguyên).
