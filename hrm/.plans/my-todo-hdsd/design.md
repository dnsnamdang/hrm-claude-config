# Design — HDSD màn "Lịch làm việc của tôi" (/assign/my-todo)

## Mục tiêu
Tài liệu HDSD Word cho người dùng cuối của màn "Lịch làm việc của tôi" — bảng điều khiển cá nhân tổng hợp Task/Issue/Phiếu giao việc/Phiếu công tác/Meeting/Nhắc việc cá nhân, làm tương tự `HDSD_CongViecCuaToi.docx`.

## Hiện trạng màn (khảo sát 03/07/2026)
- FE: `hrm-client/pages/assign/my-todo/` — index.vue + 9 component (FilterBar, MainList, GroupHeader, Item, SubItem, CalendarSidebar, TodoFormModal, TodoListFormModal, ListDetail). Tái dùng modal Task (CreateTaskModal/ImportResultModal/TaskHistoryModal) + Issue (CreateIssueModal/IssueHistoryModal).
- BE: `Modules/Assign` MyTodoController/Service — GET `assign/my-todo` tổng hợp 6 loại việc (task assignee loại trừ Nháp/Hoàn thành/Hủy; issue assignee loại trừ closed/completed/rejected; assign_job ĐÃ DUYỆT; assign_business ĐÃ LẬP PHIẾU CT; meeting LÊN LỊCH/CHỐT LỊCH participant; personal todo). CRUD lists/todos + toggle (cascade cha↔con) + reorder. Không permission riêng, dữ liệu tự giới hạn user đăng nhập.
- Điểm đáng chú ý khi viết HDSD:
  - Nút thao tác dòng CHỈ hiện khi hover; bộ nút theo loại + quyền (task: Xem/Sửa/Nhập KQ/Duyệt/Lịch sử; issue: Xem/Sửa/Xử lý/Lịch sử; personal: Sửa; meeting/phiếu: không nút, click mở tab mới).
  - Duyệt Task/Issue KHÔNG có nút riêng — chọn trạng thái trong ô Trạng thái (allowed_next_statuses theo vai trò) rồi Lưu.
  - Lọc "Đã xong" chỉ áp dụng nhắc việc cá nhân.
  - TodoFormModal: BE bắt buộc list_id khi tạo (FE hiển thị "-- Không có danh sách --" nhưng lưu sẽ lỗi toast chung) → HDSD dặn chọn danh sách.
  - Danh sách cá nhân KHÔNG có chọn màu (BE không có cột color); list mặc định "Mac dinh" tự tạo.
  - Toggle hoàn thành hỏi confirm (chỉ chiều chưa xong→xong); cha-con cascade 2 chiều.

## Cách dựng
- 2 agent Opus đọc code song song (components+BE / 5 modal tái dùng) → spec từng trường + nguyên văn label.
- Playwright MCP chụp 21 ảnh thật trên dev-hrm.eteksofts.com, tài khoản namdangit@gmail.com; tạo data demo cá nhân (2 nhắc việc, 1 danh sách + 2 việc + 2 bước con, tick 1 bước con); task/issue/meeting demo sẵn có (TASK CHECK/ISSUE CHECK DỰ ÁN HDSD 001, MEETING CHECK).
- Generator `gen_mytodo.py` (scratchpad) dùng `hdsd_p5_work/hdsd_lib.py`: copy khung `HDSD_DanhMuc/HDSD_VaiTroDuAn.docx`, sửa bìa "(Màn hình: Lịch làm việc của tôi)", strip body, build 9 phần, purge media, updateFields. Chạy từ ROOT project.

## Output
- `HDSD_luongchinh/HDSD_LichLamViecCuaToi.docx` — 12 Heading 1 (TỔNG QUAN + PHẦN 1..9), 20 hình + caption SEQ, 13 bảng, ~1.9MB, broken=0.
- Ảnh: `hdsd_mytodo_shots/` (21 file).
