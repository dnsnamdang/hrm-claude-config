# Sửa SRS + bổ sung testcase theo feedback tester 07/10/2026 — @namdangit

Phạm vi: phần Chuyển đổi ERP→HRM + phân hệ Quản lý dự án (bảng theo dõi `Checklist HDSD_SRS_TESTCASE`).
Code căn cứ: nhánh `origin/develop` (hrm-client 950ad946e · hrm-api a961edd8a) — có luồng import #11588.

## Quyết định đã chốt (user 07/10/2026)
- Testcase: CHỈ chèn dòng mới vào đúng nhóm, cột check để trống. Riêng ý 3 (Expected TC mở màn từ menu) và ý 4 (thêm bước "Tìm kiếm nâng cao") được SỬA dòng cũ, xoá trống ô check của dòng đã sửa.
- SRS ý 1: Import có dòng không còn hợp lệ → không import dòng nào, giữ popup, tô đỏ từng dòng lỗi kèm lý do (Redmine #11588, develop).
- SRS ý 4 (điều kiện Khoá/Mở khoá): BỎ, không sửa.
- Ý 3 SRS (Người/Ngày cập nhật gần nhất, Người/Ngày tạo bản ghi): áp cho MỌI SRS (84 file). Các ý import (1, 2, 5): mọi SRS danh mục.

## SRS
- [x] Tải 84 SRS theo ID (drive/) + metadata ModTime
- [x] Agent soạn nội dung import (bảng cột file mẫu, luồng #11588, ghi lịch sử Tạo mới) cho từng SRS danh mục → specs/<id>.json (37 file)
- [x] patch_srs.py: vá mục Import + mô tả Người/Ngày tạo/cập nhật → out/ (82 docx, 252 ô ý 3; câu sai ngoài phạm vi chỉ báo, không sửa)
- [ ] Đẩy theo ID (kiểm ModTime) — không thêm heading nên không cần cập nhật mục lục
- [ ] 2 Google Doc gốc (Quy tắc chung, DV sửa chữa) sửa qua Playwright

## Testcase
- [x] Dump tab danh mục 2 workbook (chuyển đổi 22 tab, QLDA 17 tab)
- [x] Agent soạn case mới (ý TC 1,2,5,6,7 + import #11588) + sửa ý 3,4 → tc/plans_*/*.json
- [ ] Chèn/sửa lên Google Sheet qua Playwright (từ dưới lên, kiểm trước/sau)

### Checkpoint — 07/10/2026 17:50 (user bảo TẠM DỪNG)
Vừa hoàn thành: Testcase chuyển đổi đã ghi 15 tab (01,02,03,04,05,06,07,08,10,11,12,19,20,21,22) — chèn case + sửa ô ý 3/4, kiểm đầu/cuối khớp. SRS: 80 docx vá xong ở out/, đã đẩy 23/68 file lên Drive.
Đang làm dở: đẩy SRS (dừng giữa chừng, Tỉnh/TP bị Drive 403 rate limit) — danh sách còn lại batch_push_rest.txt.
Bước tiếp theo: (1) `python3 push.py $(cat batch_push_rest.txt)` (2) ghi tab chuyển đổi 09,13,14,15,16,17,18 bằng .playwright-mcp/tcw2/multi_cd_d2.js, multi_cd_e2.js (cần `python3 -m http.server 8766` trong tc/ops) (3) 17 tab QLDA: ops/qlda_* đã sinh, cần runner multi cho qlda (tab 06 & 16 lệch cột đã xử lý trong build_ops) (4) Google Doc "DV sửa chữa & chi phí" sửa tay qua Playwright theo out/1XN4….log (5) báo user QUESTIONS.md.
Blocked:

### Checkpoint — 07/10/2026 21:20 — HOÀN THÀNH
Vừa hoàn thành: Testcase chuyển đổi 22/22 tab + Testcase QLDA 17/17 tab (chèn case mới, sửa ý 3/4, kiểm đầu/cuối khớp); SRS 68/68 docx đẩy Drive theo ID; Google Doc "DV sửa chữa & chi phí" sửa tay (ý 3, bước 7 lịch sử, dòng sự kiện phụ, event Import, câu file mẫu, bảng 6 cột).
Đang làm dở: —
Bước tiếp theo: user chốt các câu hỏi trong QUESTIONS.md; code #11588 cho module Giao việc + Gói BD + KH ERP chưa có.
Blocked:

## Sự cố mất nhận xét (12/10/2026) — do upload đè .docx đợt 06/10 + 07/10
- [x] Xác định nguyên nhân: upload đè = "chỉnh sửa bên ngoài Google Tài liệu" → Google xoá nhận xét; ghi bộ nhớ cấm lặp lại
- [x] Gom 50 chuỗi email comments-noreply (Gmail hangtechqa) → 265 nhận xét / 10 tài liệu → comments_recover/Nhan_xet_khoi_phuc.xlsx
- [x] Bỏ 24 nhận xét còn sống trên file (HDSD khu vực, một phần Tài khoản/Công việc/Khu vực/Quận-Huyện…) — tránh trùng
- [x] Gắn lại 241 nhận xét vào 9 SRS (tài khoản hangtechqa, ghi "[Khôi phục] <người> – <giờ>"), nhận xét đã giải quyết gắn xong đánh dấu giải quyết; kiểm 9/9 file đủ số
- Ghi chú: ~40 nhận xét đoạn gốc đã đổi → gắn vào dòng bảng/mục chứa đoạn cũ hoặc cạnh nhận xét liền trước, nội dung có ghi "(Đoạn được nhận xét gốc: …)"
- [x] (12/10 chiều) User báo nhận xét đặt chưa đúng chỗ → xác định lại vị trí gốc theo bản cũ (agent chọn 108 chỗ mơ hồ theo nội dung nhận xét), user chốt: KHÔNG CHẮC thì chỉ hiện nội dung (gắn ở dòng tiêu đề "Màn hình: …" kèm đoạn gốc)
- [x] Chuyển 185 nhận xét: 95 bôi đúng đoạn gốc (chuỗi duy nhất), 146 về tiêu đề tài liệu; kiểm 9/9 file đủ số, nội dung chữ không đổi
- [x] (12/10 tối) User chọn hướng 2: 152 nhận xét không chắc chuyển từ tiêu đề tài liệu về dòng tiêu đề MỤC chứa đoạn gốc (vd '2.3 Thêm mới tài khoản'), kèm đoạn gốc; kiểm 9/9 file đủ số, 0 nhận xét còn ở tiêu đề tài liệu
