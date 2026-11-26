# SRS 6 màn nghiệp vụ (Meeting, Nhiệm vụ, Vấn đề, Bàn giao x3) — @namdangit

## Phase 1 — SRS (03/10/2026)
- [x] meeting — SRS - Tổng hợp meeting.docx
- [x] tasks — SRS - Nhiệm vụ.docx
- [x] issues — SRS - Vấn đề.docx
- [x] handover — SRS - Phiếu bàn giao.docx
- [x] handover-add — SRS - Tạo bàn giao.docx
- [x] handover-receiving — SRS - Chờ tiếp nhận bàn giao.docx
- [x] Chạy lại có Word cập nhật mục lục, kiểm, đẩy Drive folder 1VV_w8EfDbgOb4714ghxFoumlIFWUSQAf
- [x] Đã đẩy 6 file mới lên Drive (03/10/2026)

## Phase 2 — SRS 6 màn QLDA (05/10/2026)
- [x] prospective-projects — SRS - Dự án.docx
- [x] request-solution — SRS - Yêu cầu làm giải pháp.docx
- [x] solutions — SRS - Quản lý giải pháp.docx
- [x] bom-list — SRS - BOM giải pháp.docx
- [x] quotations — SRS - Báo giá.docx
- [x] pricing-requests — SRS - Yêu cầu tính giá bán.docx (SRS_NO_WORD, chờ chạy lại có Word)
- [x] Chạy lại có Word, kiểm, đẩy Drive folder 1VV_w8EfDbgOb4714ghxFoumlIFWUSQAf

## Phase 2 — SRS (05/10/2026)
- [x] prospective-projects — SRS - Dự án.docx (31 chức năng, chưa chạy Word cập nhật mục lục)
- [x] solutions — SRS - Quản lý giải pháp.docx (05/10/2026, chưa chạy Word cập nhật mục lục)

## Ngày 26/11/2026 (@junfoke)
- [x] 26/11/2026 — Sửa thẳng phần phân quyền 3 SRS trên Drive (Dự án, Yêu cầu làm giải pháp, Quản lý giải pháp) theo comment "phân quyền mới": 4 quyền V1–V4 "Xem danh sách … theo tổng công ty/công ty/phòng ban/bộ phận" đổi thành 1 quyền Xem chọn phạm vi khi gán (gán nhiều vai trò lấy phạm vi rộng nhất); quyền thao tác giữ nguyên tên. Tra code develop (3 agent): hành vi "không quyền chỉ thấy bản ghi mình tạo" vẫn đúng ở cả 3 màn. SRS Dự án: trả lời c Lệ màn Quản lý dự án đã có, không có quyền riêng (nút theo vai trò R1–R5 + Q1–Q6); có lần chèn nhầm đoạn vào ô FR-01 Ma trận — đã gỡ và kiểm lại. SRS YC làm giải pháp: cột Q1 chỉ là quyền xem, Tạo mới không cần quyền và không theo phạm vi (chỉ cho dự án TKT do mình tạo); ô FR-06 Ma trận chưa sửa được tự động. Tải từng file về so bản gốc: chỉ chỗ định sửa thay đổi, nhận xét còn nguyên.
  - Phát hiện khi tra code (chưa sửa): Dự án TKT BE không kiểm khi Xoá, xem chi tiết không lọc phạm vi, lưu cấu hình đóng dự án tự động không kiểm quyền, xuất Excel 1 báo giá không kiểm phạm vi; YCLGP Hủy "tạm thời chỉ người tạo"; mã "Quản lý giải pháp" chỉ dùng cho Đóng mà UI chưa có nút.
