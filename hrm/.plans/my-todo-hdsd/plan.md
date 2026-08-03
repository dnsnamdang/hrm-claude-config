# Plan — HDSD màn "Lịch làm việc của tôi"

Người phụ trách: @manhcuong
Output: `HDSD_luongchinh/HDSD_LichLamViecCuaToi.docx` (Word, format HDSD chuẩn — tương tự HDSD_CongViecCuaToi.docx)
Tài khoản chụp ảnh: namdangit@gmail.com (DNS ADMIN update) — cổng dev: https://dev-hrm.eteksofts.com/assign/my-todo

## Phase 1: Khảo sát & chụp ảnh
- [x] Đọc index.vue + 9 component my-todo + BE MyTodoController/Service (agent Opus #1)
- [x] Đọc 5 modal tái dùng: CreateTaskModal / ImportResultModal / TaskHistoryModal / CreateIssueModal / IssueHistoryModal (agent Opus #2)
- [x] Đăng nhập dev-hrm (namdangit) + tạo data demo cá nhân (2 nhắc việc + 1 danh sách "Việc cần nhớ tuần này" + 2 việc + 2 bước con) — task/issue/meeting demo có sẵn từ đợt HDSD trước
- [x] Chụp 21 ảnh thật → `hdsd_mytodo_shots/`
  - [x] 12 tổng quan có dữ liệu, 02 danh sách nhóm mở, 03/04 hover nút Task/Issue
  - [x] 05/06 dropdown lọc Loại + Trạng thái
  - [x] 07/08 form Tạo nhắc việc (trống + đã điền), 21 form Sửa, 11 confirm hoàn thành
  - [x] 09 form Tạo danh sách, 10 chi tiết danh sách (việc + bước con)
  - [x] 13 lọc theo ngày trên lịch (flat mode)
  - [x] 14 Chi tiết Task, 15 Nhập kết quả Task, 16 dropdown trạng thái Task, 17 Lịch sử Task
  - [x] 18 Chi tiết Issue, 19 chế độ Xử lý Issue (dropdown trạng thái), 20 Lịch sử Issue

## Phase 2: Dựng tài liệu Word
- [x] Generator `scratchpad/gen_mytodo.py` — dùng `hdsd_p5_work/hdsd_lib.py` (copy khung HDSD_VaiTroDuAn, strip body, caption SEQ, purge media, updateFields)
- [x] TỔNG QUAN: thuật ngữ (10 dòng), bảng cập nhật, giới thiệu + đường dẫn, quyền & phạm vi (dữ liệu cá nhân)
- [x] PHẦN 1: Truy cập & bố cục + bảng 4 thẻ thống kê
- [x] PHẦN 2: Nhóm theo hạn (bảng 7 nhóm) + thành phần dòng việc + click theo loại + bảng nút thao tác Task/Issue/Cá nhân
- [x] PHẦN 3: Tìm kiếm realtime + lọc Loại/Trạng thái + nút làm mới
- [x] PHẦN 4: Lịch tháng (chấm, hôm nay, đổi tháng) + lọc theo ngày
- [x] PHẦN 5: Nhắc việc cá nhân — Tạo (bảng trường + mặc định) / Sửa / Hoàn thành (confirm + cascade bước con) / Xóa
- [x] PHẦN 6: Danh sách cá nhân — sidebar + kéo thả / Tạo (bảng trường) / Chi tiết (thêm nhanh, bước con, nhóm Đã hoàn thành) / Sửa / Xóa
- [x] PHẦN 7: Task — Xem / Sửa / Nhập kết quả (bảng trường + báo cáo tiến độ) / Duyệt qua ô Trạng thái / Lịch sử / bảng trạng thái
- [x] PHẦN 8: Issue — Xem / Sửa / Xử lý (trạng thái + lý do từ chối + chứng cứ) / Lịch sử / bảng trạng thái
- [x] PHẦN 9: Meeting / Phiếu giao việc / Phiếu công tác (điều kiện xuất hiện + mở tab mới)
- [x] Build + verify: 12 Heading 1, 20 hình + 20 caption, 13 bảng, updateFields=true, broken=0, ~1.9MB

## Phase 3: Hoàn thiện
- [x] Cập nhật plan.md + design.md + STATUS.md

### Checkpoint — 03/07/2026
Vừa hoàn thành: file HDSD_LichLamViecCuaToi.docx hoàn chỉnh 9 phần, 20 ảnh thật dev-hrm, bảng trường + giá trị mặc định cho mọi form (nhắc việc, danh sách, nhập kết quả Task, xử lý Issue).
Đang làm dở: không
Bước tiếp theo: chờ user review file Word; data demo cá nhân trên dev (2 nhắc việc + danh sách "Việc cần nhớ tuần này") để nguyên phục vụ ảnh — có thể xóa tay nếu muốn.
Blocked:

## Output
- File: `HDSD_luongchinh/HDSD_LichLamViecCuaToi.docx` (~1.9MB, 12 Heading 1, 20 hình, 13 bảng)
- Ảnh nguồn: `hdsd_mytodo_shots/` (21 ảnh; 01_overview không dùng — thay bằng 12)
- Generator: scratchpad phiên làm việc (`gen_mytodo.py`) — chạy từ ROOT project: `/opt/homebrew/opt/python@3.14/bin/python3.14 gen_mytodo.py` (import `hdsd_p5_work/hdsd_lib.py`)
