# Plan — HDSD màn hình Meeting (/assign/meeting)

## Mục tiêu
Tạo tài liệu HDSD Word CHI TIẾT cho màn Meeting: đủ mọi chức năng, click-by-click, từng trường + giá trị mặc định, ảnh chụp thật.

## Tasks
- [x] Khảo sát source: FE list, FE form tạo/sửa + components, FE xem/in/khảo sát, BE (route/service/request/entity/migration/permission) — 4 agent Opus
- [x] Chụp ảnh thật bằng Playwright (11 ảnh trong `hdsd_meeting_shots/`)
- [x] Dựng file Word chi tiết: `HDSD_luongchinh/HDSD_ManHinh_Meeting.docx`
  - Generator: `hdsd_p5_work/gen_meeting_screen.py` (dùng `hdsd_lib.HDSD`, khung từ `HDSD_DanhMuc/HDSD_VaiTroDuAn.docx`)
  - Chạy lại: `/opt/homebrew/opt/python@3.14/bin/python3.14 hdsd_p5_work/gen_meeting_screen.py`
- [x] Verify: 11 ảnh (broken=0), 11 bảng, 8 PHẦN, 18 H2, 7 H3, 11 caption
- [ ] (Chờ user) Có ghi đè/gộp vào file quy-trình cũ `QLDA_1_HDSD_QuanLyMeeting.docx` không

## Cấu trúc tài liệu (8 PHẦN)
1. Truy cập & bố cục danh sách (tìm nhanh, 13 tiêu chí lọc, cột, toolbar, thao tác dòng)
2. Tạo mới (từng trường + box mặc định, popup chọn nhân viên, dự án TKT, khách hàng, nút lưu→trạng thái, mã tự sinh)
3. Điểm danh
4. Ghi biên bản & kết luận (biên bản, tài liệu đính kèm, kết luận)
5. Dự án tiền khả thi & phiếu thu thập thông tin
6. Xem chi tiết / Sửa / Hoàn thành / Hủy / Xóa (điều kiện theo trạng thái)
7. In biên bản & in phiếu khảo sát
8. Xuất Excel & tạo phiếu công tác khác

Ngoài ra TỔNG QUAN: giới thiệu, thuật ngữ, 5 trạng thái + luồng, phân quyền 4 cấp.

## Checkpoint — 2026-07-10 (bản 3 — đầy đủ mọi trường hợp, ghi vào file cũ)
Vừa hoàn thành:
- Tạo cuộc họp demo (TPE.MET.NB.26.0010, id 11) để chụp 8 ảnh case thật (22-29): lỗi validate inline, dòng nháp đủ 5 icon, hộp Xác nhận xóa, footer sửa nháp, chip điểm danh (chế độ sửa, trạng thái Đã chốt), hộp Xác nhận huỷ + ô lý do, thông báo chặn Hoàn thành khi chưa có biên bản, modal Tuỳ chỉnh cột.
- Dọn demo: đã Hủy cuộc họp demo (status 4) — không xóa được vì đã chốt lịch.
- GHI THẲNG nội dung vào file cũ: HDSD_luongchinh/QLDA_1_HDSD_QuanLyMeeting.docx (thay nội dung quy-trình cũ). Đã xóa file HDSD_ManHinh_Meeting.docx.
File cuối: QLDA_1_HDSD_QuanLyMeeting.docx — 27 ảnh (broken=0), 27 caption, 9 bảng, 8 PHẦN, 15 H3, 4.08MB. Generator: hdsd_p5_work/gen_meeting_screen.py (output đã trỏ vào QLDA_1).
Ảnh: hdsd_meeting_shots/ (29 ảnh).
Đang làm dở: (không)
Bước tiếp theo: xong. Còn 2 màn chưa chụp được (mô tả bằng chữ): bản đồ chọn địa điểm (mở Google Map ngoài), phiếu thu thập thông tin (cần dự án TKT có bộ câu hỏi) — bổ sung nếu user cần.
Blocked:
