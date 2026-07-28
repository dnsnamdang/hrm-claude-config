# Plan — HDSD tab "Quản lý dự án" (màn Cấu hình chung /assign/settings)

Người phụ trách: @manhcuong
Output: `HDSD_luongchinh/HDSD_CauHinhQuanLyDuAn.docx`
Tài khoản chụp ảnh: namdangit@gmail.com — https://dev-hrm.eteksofts.com/assign/settings (tab Quản lý dự án)

## Phase 1: Khảo sát & chụp ảnh
- [x] Agent Opus đọc FE index.vue (2044 dòng, tab Quản lý dự án ~768-1217) + BE route→controller→service→entity→migration + NƠI TIÊU THỤ: priority → project_phase_modal (bắt buộc chọn) + RequestSolutionService::calculateNeedReceiveDate (hạn tiếp nhận = sent_date + response_days/hours, bỏ lễ) + filter Solution/MyJob; deadline-config → MyJobService (Sắp tới hạn task/meeting/solution/issue) + SolutionService/SolutionModuleService (ngưỡng task trễ, max(threshold,1))
- [x] Chụp 6 ảnh → `hdsd_settings_project_shots/`
  - [x] 01 tab ưu tiên tổng quan, 02 cột Hành động, 03 dòng đang sửa (Lưu/Huỷ), 04 Thêm dòng ("Chưa lưu"), 05 confirm "Xác nhận xóa" (xóa dòng nháp — không đụng dữ liệu thật), 06 tab Cấu hình hạn

## Phase 2: Dựng tài liệu Word
- [x] Generator `gen_settings_project.py` (hdsd_lib, khung HDSD_VaiTroDuAn, bìa "(Màn hình: Cấu hình chung — tab Quản lý dự án)")
- [x] TỔNG QUAN (thuật ngữ 6 dòng, quyền menu 'Cấu hình phân hệ giao việc/ công tác', ưu tiên GLOBAL vs cấu hình hạn THEO CÔNG TY)
- [x] PHẦN 1 truy cập/bố cục (2 tab con lưu độc lập, khác 2 tab lớn dùng Lưu chung)
- [x] PHẦN 2 mức độ ưu tiên: bảng cột (tên ≤20 unique, ngày/giờ phản hồi, màu #RRGGBB) + Thêm dòng (default 0/0/#16a34a) + Sửa (Lưu/Huỷ) + kéo thả STT + Xóa (chặn khi hạng mục đang dùng "Dữ liệu đang được sử dụng...") + mục tác động (hạng mục, hạn tiếp nhận yêu cầu GP, không hồi tố, response_days=0 → không đặt hạn)
- [x] PHẦN 3 cấu hình hạn: bảng 6 trường + tooltip nguyên văn + mặc định 0 + min 1 cho ngưỡng task trễ + toast + tác động (my-job Sắp tới hạn, cảnh báo task trễ, theo công ty)
- [x] Build + verify: 6 Heading 1, 6 hình + 6 caption, 4 bảng, updateFields, broken=0, ~0.5MB

## Phase 3: Hoàn thiện
- [x] Cập nhật plan.md + design.md + STATUS.md

### Checkpoint — 03/07/2026
Vừa hoàn thành: HDSD_CauHinhQuanLyDuAn.docx (TỔNG QUAN + 3 phần), đủ tác động nghiệp vụ 2 tab con.
Đang làm dở: không
Bước tiếp theo: chờ user review.
Blocked:

## Output
- File: `HDSD_luongchinh/HDSD_CauHinhQuanLyDuAn.docx` (~0.5MB, 6 Heading 1, 6 hình, 4 bảng)
- Ảnh nguồn: `hdsd_settings_project_shots/` (6 ảnh)
- Generator: scratchpad phiên (`gen_settings_project.py`) — chạy từ ROOT project HRM/
