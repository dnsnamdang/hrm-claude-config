# Design (tóm tắt) — HDSD màn Dự án tiềm năng

## Mục tiêu
Tài liệu HDSD Word chi tiết click-by-click cho màn `/assign/prospective-projects` (Dự án tiềm năng / dự án tiền khả thi), phục vụ đào tạo/bàn giao người dùng cuối.

## Phạm vi màn (đã khảo sát code + chụp thật)
- **Danh sách**: 19 cột, cấu hình cột riêng theo user; bộ lọc nhanh + 16 tiêu chí nâng cao; toolbar Tạo mới / Xuất Excel / Cấu hình cột; thao tác dòng Xem / Sửa / Tạo giải pháp (điều kiện) / Xoá (điều kiện).
- **Tạo mới/Sửa** (`add.vue`/`_id/edit.vue`): 7 nhóm — Thông tin KH, Thông tin dự án, Timeline, Phụ trách KD nội bộ (+Phòng hỗ trợ), Giải pháp, Liên kết dữ liệu, Nguồn vốn & tài chính. Validate chủ yếu ở BE (`ProspectiveProjectRequest`, 2 chế độ nháp/chính thức). Lưu nháp=status1, Lưu=status2 (sinh mã).
- **Chi tiết** (`_id/manager.vue`): 10 tab (Dự án, Yêu cầu, Giải pháp[+Điều chỉnh GP], Task, Issue, Meetings, Files, Hồ sơ, Báo giá, Thu thập thông tin). Footer: Sửa / Đóng dự án / Chốt giải pháp / Quay lại (tuỳ trạng thái & quyền KD phụ trách chính).
- **Nghiệp vụ quan trọng**: Đóng dự án (cascade GP/hạng mục/YCGP/YCBG/Báo giá → Đóng, notify), Chốt giải pháp (hồ sơ→Đã chốt, GP→Chốt, dự án→Thương thảo HĐ).
- **Vòng đời**: 12 trạng thái, phần lớn tự động theo GP/YCGP/Báo giá.

## Cấu trúc tài liệu (11 phần)
Tổng quan → P1 Danh sách & bố cục → P2 Tìm kiếm & lọc → P3 Cột & cấu hình → P4 Nút & thao tác → P5 Tạo mới (từng trường) → P6 Sửa → P7 Chi tiết & các tab → P8 Đóng dự án → P9 Chốt giải pháp → P10 Xóa → P11 Vòng đời trạng thái.

## Cách tái dựng
- Generator: `scratchpad/gen_hdsd_tkt.py` (python-docx + Pillow, python 3.14).
- Khung: `HDSD_DanhMuc/HDSD_KhachHang.docx` (copy → sửa bìa → lưu proto Caption SEQ → strip body từ "TỔNG QUAN PHẦN MỀM" giữ sectPr → rebuild H1/H2/H3/P/BULLET/TABLE/IMG/CAP → purge media mồ côi → updateFields=true → verify).
- Ảnh nguồn: `hdsd_prospective_projects_shots/` (11 ảnh).
- Output: `HDSD_luongchinh/HDSD_DuAnTienKhaThi.docx`.

## Còn thiếu / lưu ý
- Chưa có ảnh thật modal "Chốt giải pháp" (không có dự án nào ở trạng thái đủ điều kiện mà tài khoản test phụ trách) — mô tả theo code, có thể bổ sung ảnh sau.
