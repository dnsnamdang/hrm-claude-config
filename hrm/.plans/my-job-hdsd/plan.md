# Plan — HDSD màn "Công việc của tôi"

Người phụ trách: @manhcuong
Output: `HDSD_luongchinh/HDSD_CongViecCuaToi.docx` (Word, format HDSD chuẩn)
Tài khoản chụp ảnh: huyenntt.qttt@tanphat.com — link: /assign/my-job

## Phase 1: Khảo sát & chụp ảnh
- [x] Đọc index.vue + 14 component các tab (qua agent Explore)
- [x] Đăng nhập dev-hrm + chụp ảnh thật từng tab/modal (Playwright) → `hdsd_myjob_shots/`
  - [x] 01 Tổng quan (thẻ cảnh báo + bảng hôm nay), 14 biểu đồ
  - [x] 02-03 Modal "Danh sách Issue" (lọc thường + nâng cao)
  - [x] 04-05 Tab Giải pháp (bảng + lọc nâng cao)
  - [x] 06-08 Tab Task (bảng + lọc nâng cao + lọc nhanh "Tôi làm")
  - [x] 09 Tab Issue
  - [x] 10 Tab Meeting
  - [x] 11-12 Tab Phiếu công tác (bảng + menu hành động)
  - [x] 15 Modal "Tuỳ chỉnh cột"
  - [~] Tab Chờ duyệt — user YÊU CẦU TẠM BỎ, không viết

## Phase 2: Dựng tài liệu Word
- [x] Generator python-docx (`scratchpad/gen_myjob.py`): copy catalog HDSD_KhachHang làm khung (cover+TOC+TOF+styles+updateFields), strip body, purge media mồ côi (27→14 ảnh, 6.2MB→2.1MB)
- [x] TỔNG QUAN: thuật ngữ, bảng cập nhật tài liệu, giới thiệu, đường dẫn, quyền & phạm vi dữ liệu
- [x] PHẦN 1: Truy cập & bố cục chung (thanh tab, nút Quay lại)
- [x] PHẦN 2: Tab Tổng quan (4 thẻ cảnh báo click→modal + lọc nâng cao, bảng hôm nay, 4 biểu đồ)
- [x] PHẦN 3: Tab Giải pháp (lọc, 18 cột, Tạo mới/Xuất Excel/Cấu hình cột, thao tác dòng)
- [x] PHẦN 4: Tab Task (lọc nâng cao, lọc nhanh 4 phạm vi + Quá hạn, thao tác dòng)
- [x] PHẦN 5: Tab Issue (lọc, thao tác Xem/Sửa/Xử lý/Lịch sử/Xóa)
- [x] PHẦN 6: Tab Meeting (lọc, thao tác Xem/Sửa/In/Tạo phiếu CT/Xóa, biên bản)
- [x] PHẦN 7: Tab Phiếu công tác (menu hành động đầy đủ, Xuất Excel chọn cột)
- [x] Chèn 14 ảnh + caption SEQ, xác minh mở được file (refs=14 broken=0)

## Phase 3: Hoàn thiện
- [x] Rà soát click-by-click đầy đủ từng hành động nhỏ
- [x] Cập nhật STATUS.md + design.md
- [~] Tab Chờ duyệt: user yêu cầu tạm bỏ — nếu cần sau này thêm PHẦN 8

## Output
- File: `HDSD_luongchinh/HDSD_CongViecCuaToi.docx` (2.1MB, 10 Heading 1, 14 hình)
- Ảnh nguồn: `hdsd_myjob_shots/` (15 ảnh, ảnh 13 = Chờ duyệt chưa dùng)

## Phase 4: Mở rộng chi tiết form từng thao tác (user yêu cầu "đầy đủ từng trường + mặc định")
- [x] 5 agent Opus đọc song song: form Task (Create/ImportResult/History), Issue (Create/History), Giải pháp (add/edit), Meeting (create/edit), Phiếu công tác (add + màn duyệt/nhập KQ/từ chối)
- [x] Chụp thêm form thật: 20 Giải pháp add, 21 Meeting create, 22 Phiếu CT add, 23 Task popup, 24 Task nâng cao, 25 Issue popup, 26 modal Xuất Excel
- [x] Mở rộng generator: thêm mục Tạo mới/Sửa/Duyệt/Nhập kết quả/Lịch sử/Xóa cho từng tab, bảng trường (Bắt buộc + Giá trị mặc định) + box "Giá trị điền sẵn"
- [x] Build lại + purge: 3.0MB, 21 ảnh, 8 bảng, 21 caption, refs=21 broken=0

### Checkpoint — 30/06/2026 (bản 2 — đầy đủ form)
Vừa hoàn thành: bản HDSD đầy đủ — mỗi tab có mục Tạo mới với bảng từng trường + giá trị mặc định (vd Task: Nháp/hạn hôm nay/17:00/người duyệt+theo dõi=chính mình; Issue: Lỗi phần mềm/Trung bình/Cá nhân/Tự phát hiện/SLA 1 ngày; Meeting: người tạo tự thêm Phía Công ty; Phiếu CT: kỹ thuật/trưởng nhóm đầu) + Sửa/Duyệt/Nhập kết quả/Lịch sử/Xóa. Ảnh form thật 20-26.
Đang làm dở: không
Bước tiếp theo: chờ user review; còn có thể bổ sung ảnh các màn Sửa/Duyệt/Nhập kết quả riêng (hiện mô tả bằng chữ) hoặc tab Chờ duyệt nếu cần.
Blocked: 
