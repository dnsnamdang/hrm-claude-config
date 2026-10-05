# Brief đối chiếu testcase #10455 với màn hình thật

Mục tiêu: mọi TC trong file testcase phải khớp giao diện đang chạy — đường bấm menu, tên màn, chữ trên nút, nhãn trường, nhãn trong popup Lịch sử, tiêu đề popup, placeholder, câu thông báo (toast/lỗi dưới ô), định dạng giá trị cũ → mới, số cột/nhãn cột, hành vi (có sinh dòng lịch sử hay không).

Môi trường (nhánh task_10455, đã push):
- FE http://127.0.0.1:3005 (worktree /Users/manhcuong/Desktop/dns/HRM/worktrees/task_10455-client), BE http://127.0.0.1:8005 (worktree .../task_10455-api), DB local_hrm_erp (mysql -uroot -h127.0.0.1) — DB dùng chung.
- Playwright Python: /opt/homebrew/opt/python@3.14/bin/python3.14. Login: POST http://127.0.0.1:8005/api/v1/users/auth/login {email:'namdangit@gmail.com',password:'2025Dns@2'} → access_token; goto http://127.0.0.1:3005/login rồi localStorage.setItem('access_token', token). wait_until='domcontentloaded' + chờ selector. Không đổi mật khẩu namdangit; TK khác đặt tạm được, test xong trả hash cũ.
- Không git (không commit/push/stash/reset).

Cách làm:
1. Đọc generator nhóm mình + file xlsx đã sinh. Lập danh sách điểm cần đối chiếu (gom theo màn/popup).
2. Mở từng màn/popup bằng Playwright, thu chữ thật (innerText, placeholder, title, toast) + chụp ảnh vào thư mục nhóm. Với TC phải lưu dữ liệu mới thấy được (toast, dòng lịch sử, định dạng cũ → mới): làm THẬT trên 1 bản ghi/ô ít ảnh hưởng, ghi lại giá trị cũ trước, khôi phục sau, xoá dòng lịch sử do mình sinh ra (ghi id). Không cần chạy hết cả trăm TC từng trường — đủ để xác nhận NHÃN của mọi trường (đọc từ form + popup) và mỗi KIỂU định dạng/thông báo ít nhất 1 lần thật.
3. Sửa trong generator mọi chỗ lệch với giao diện (nhãn, chữ nút, đường menu, câu thông báo, kết quả mong đợi), giữ đúng quy tắc skill testcase-documenter (ngôn ngữ nghiệp vụ, không URL, không emoji, ô nhiều ý xuống dòng). Chạy lại generator của nhóm → kiểm tra thuật ngữ phải OK.
4. "Có lỗi thì tự fix": nếu chỗ lệch là do CODE SAI (vd nhãn popup khác form, toast sai chữ/sai màu, lịch sử không ghi/ghi rác, lỗi 500, vi phạm CLAUDE.md) và thuộc tính năng lịch sử / các màn này → sửa code trong worktree task_10455 (đọc CLAUDE.md + skill liên quan trước, Edit đúng đoạn, php -l, kiểm lại bằng Playwright), rồi viết TC theo hành vi đúng. Việc lớn / đổi nghiệp vụ / đụng hàm dùng chung rộng / cần khách chốt → KHÔNG tự sửa, liệt kê để hỏi. Không commit.
5. Báo cáo ngắn: số điểm đã đối chiếu, số TC đã sửa, danh sách lỗi code đã fix (file + kiểm lại), danh sách chưa fix cần user chốt, dữ liệu đã dọn.
