# Xuất tài liệu SRS + HDSD + Testcase các màn chuyển đổi ERP→HRM "Đã test" — @junfoke

Nguồn danh sách: sheet theo dõi chuyển đổi (cột Trạng thái = "Đã test", người làm Trí). Giao lên Drive folder
"Chuyển đổi ERP => HRM" (`1f6lwBkUC0cm_9VGxYdaoBDrJP5RS26q6`): `SRS/`, `HDSD/`, tab mới trong `TESTCASE/Testcase chuyển đổi.xlsx`
(chèn bằng `danh-muc-kho/docs/chen_tab_testcase.ps1`). Sheet Checklist là Google Sheet gốc → user tự điền.
Viết cho HRM theo code hiện tại, không đối chiếu ERP. Nghi lỗi code chỉ GHI vào `NGHI_LOI.md`, xuất xong tài liệu mới kiểm.

## Đợt 1 — 7 danh mục kho (xong 02/11/2026)
- [x] Kho vật lý, Kho kế toán, Nhà kho, Dãy, Khoang, Vị trí, Kiện — chi tiết `../danh-muc-kho/plan.md` Phase 8; tab TC 44–50
- [ ] User điền Checklist dòng 259–265

## Đợt 2 — 5 báo cáo (02/11/2026)
Khuôn (user chốt 02/11): SRS form quốc gia + quy tắc màn báo cáo của srs-documenter; HDSD GỌN form quốc gia + thêm 1 PHẦN
"Đọc báo cáo" (mỗi cột lấy số từ đâu, ảnh thật). Brief: `BRIEF_DOT2.md`. Hoãn 97, 108 (đang sửa code).
- [x] 94 Báo cáo hàng có thể bán theo công ty — `lookup-stock-companies/docs/`
- [x] 133 BC chi phí vận chuyển theo NV kinh doanh — `sale-transport-cost-by-staff/docs/`
- [x] 138 Bảng đối chiếu công nợ 1 khách hàng — `sale-customer-debt-reports/docs/compare/`
- [x] 139 BC tổng hợp công nợ KH theo nhân viên — `sale-customer-debt-reports/docs/by-employee/`
- [x] 140 BC chi tiết công nợ KH — `sale-customer-debt-reports/docs/details/`
- [x] Đẩy Drive 5 SRS (39–46 tr) + 5 HDSD (11–15 tr, có PHẦN Đọc báo cáo) + tab TC 51–55 (385 TC), không ảnh giả lập — 02/11
- [ ] User điền Checklist dòng 82, 121, 126, 127, 128

## Đợt 3 — 7 phiếu nghiệp vụ (xong 02/11/2026)
Brief: `BRIEF_DOT3.md`; màn mẫu 167 (user duyệt cách trình bày luồng trạng thái phiếu không duyệt); phần chung `_lib_phieu.py`, `_capture_phieu.js`.
- [x] 167 Khai báo đầu kỳ công nợ (SRS 56 / HDSD 21 / 82 TC) · 168 … nhà cung cấp (59 / 19 / 81) · 202 Phiếu huỷ hàng giữ kế toán
      (47 / 17 / 129) · 283 Khai báo tồn kho đầu kỳ (51 / 15 / 67) · 178 Phiếu nhập kho (78 / 26 / 89) · 204 Phiếu điều chuyển hàng
      (55 / 19 / 65) · 63 Yêu cầu mua dịch vụ (71 / 24 / 75)
- [x] Đẩy Drive 7 SRS + 7 HDSD + tab TC 56–62 (lần 1 dừng vì có người sửa file giữa chừng → tải lại, chèn lại, 0 ô cũ đổi)
- [x] Xoá 18 file phiên đăng nhập dev `.dev_state.json` agent để lại trong `docs/` (đã gitignore)
- [ ] User điền Checklist dòng 155, 156, 190, 266, 166 (+ 268 nhóm Kho), 192, 57

## Làm lại 19 testcase theo khuôn chuẩn tab "13. DM quốc gia" (03/11/2026)
Được báo TC 02/11 không giống chuẩn chung. Khuôn: `TC_CHUAN.md` + `_tc_chuan.py` (bọc tc_engine, không sửa engine) + `check_tc.py`;
mẫu `mau/`. Nguyên nhân gốc: skill `testcase-documenter` đang quy định nhóm TC-ROLE đầu tab — lệch tab Quốc gia (chờ user cho sửa skill).
- [x] Đối chiếu tab Quốc gia + checklist "Mẫu tài liệu.xlsx" → khuôn + script kiểm (chạy thử khớp tab Quốc gia)
- [x] `chen_tab_testcase.ps1 -Replace`: thay tab giữ tên/vị trí, trỏ lại dòng Tổng hợp (K16)
- [x] 7 agent viết lại 19 file (giữ case nghiệp vụ, bổ sung checklist): 1.714 → 3.419 case (kho 1.434 · báo cáo 591 · phiếu 1.394), check_tc 0 lỗi cả 19; bản cũ giữ `gen_testcase_v1.py` (gen mới đọc case từ đó — KHÔNG xoá, KHÔNG chạy v1)
- [x] User chốt: KQ thực tế / DNS check để TRỐNG; sửa luôn skill. Thay 19 tab 44–62 trên Drive (-Replace, 0 ô đổi ở 43 tab cũ, Tổng hợp trỏ K16, ID giữ) — 03/11
- [x] Sửa skill `testcase-documenter`: SKILL.md theo khuôn Quốc gia; assets `TC_MAU_QUOC_GIA.xlsx`, `CHECKLIST_TC_SRS.xlsx`, `tc_chuan.py`, `check_tc.py`; `tc_engine.py` ROMAN tới XX. `.plans` `_tc_chuan.py`/`check_tc.py` chỉ còn trỏ sang skill

## Sau cùng
- [ ] Rà `NGHI_LOI.md` cùng user: kiểm lỗi thật hay không → sửa code
