# Brief Đợt 2 — SRS + HDSD + Testcase cho 5 BÁO CÁO HRM

Làm bằng tiếng Việt. KHÔNG commit git, KHÔNG upload Drive, KHÔNG sửa code app (`hrm-api`, `hrm-client`), KHÔNG sửa thư viện /
skill dùng chung, KHÔNG sửa file của màn khác. Nghi lỗi code → chỉ GHI vào báo cáo cuối (không ghi vào NGHI_LOI.md, không sửa).

Tài liệu viết cho **HRM theo code hiện tại** (`develop`; repo chính đang ở nhánh con chứa code này). KHÔNG mô tả ERP, không
đối chiếu ERP. Được ĐỌC tài liệu ERP cũ để hiểu luồng số liệu (xem "Nguồn tham khảo"), nhưng nội dung phải khớp code HRM.

## 5 báo cáo

| Mã | Tên tài liệu (dùng làm tên file) | Route FE | Menu (code: `hrm-client/components/subsystem-menu/`) | Thư mục đầu ra | Plan feature |
|---|---|---|---|---|---|
| stock | Báo cáo hàng có thể bán theo công ty | `/lookup/stock-companies` | `lookup.js` | `lookup-stock-companies/docs/` | `lookup-stock-companies/` |
| transport | BC chi phí vận chuyển theo NV kinh doanh | `/sale/transport-cost-by-staff` | `sale-hub.js` + `transport.js` (1 màn ở 2 phân hệ — ghi cả 2 đường) | `sale-transport-cost-by-staff/docs/` | `sale-transport-cost-by-staff/` |
| compare | Bảng đối chiếu công nợ 1 khách hàng | `/sale/customer-debt-compare` | `sale-hub.js` | `sale-customer-debt-reports/docs/compare/` | `sale-customer-debt-reports/` |
| by-employee | BC tổng hợp công nợ KH theo nhân viên | `/sale/customer-debt-by-employee` | `sale-hub.js` | `sale-customer-debt-reports/docs/by-employee/` | `sale-customer-debt-reports/` |
| details | BC chi tiết công nợ KH | `/sale/customer-debt-details` | `sale-hub.js` | `sale-customer-debt-reports/docs/details/` | `sale-customer-debt-reports/` |

Thư mục tính từ `hrm-claude-config/hrm/.plans/gop-db/`. Đọc `design.md` + `plan.md` của feature trước (quyết định đã chốt, lỗi đã sửa).
Đường dẫn trong tài liệu: "Menu: Phân hệ <tên hiển thị> => … => <tên mục menu>" — lấy nhãn hiển thị THẬT từ file menu + màn hub.

## Đầu ra mỗi báo cáo (trong thư mục đầu ra)
- `SRS - <Tên tài liệu>.docx`, `HDSD_<Tên tài liệu>.docx`, `testcase - <Tên tài liệu>.xlsx`, `out/*.pdf`
- script sinh (`capture.js`, `gen_srs.py`, `gen_hdsd.py`, `gen_testcase.py`), ảnh `hdsd_shots/`, `icons/`, `uml/` (chỉ local)

## Khuôn — bám bộ 7 danh mục kho ĐÃ DUYỆT
- Mẫu đã duyệt: `danh-muc-kho/docs/warehouses/` (5 script) + thư viện chung `danh-muc-kho/docs/_lib_win.py`,
  `danh-muc-kho/docs/_capture_login.js`. Chép khuôn, viết phần riêng của báo cáo trong thư mục mình. Cần hàm mới thì viết trong
  thư mục mình, KHÔNG sửa `_lib_win.py` (agent khác dùng song song).
- Đọc kỹ: `danh-muc-kho/docs/BRIEF_AGENT.md` (quy tắc chung: khuôn quốc gia, font, Use Case, Word finalize, chụp dev an toàn, tự
  kiểm) · `phieu-theo-form-quoc-gia/CHECKLIST.md` (góp ý TPE) · `hrm-claude-config/hrm/.claude/skills/srs-documenter/SKILL.md` —
  ĐẶC BIỆT các mục về **màn báo cáo**: bảng "Cách lấy dữ liệu và giải thích chỉ tiêu" (mỗi cột/chỉ tiêu: lấy từ chứng từ nào, điều
  kiện, cách tính, thời điểm số liệu), "Danh sách popup mở từ số liệu", bảng chi tiết báo cáo mỗi cột 1 dòng, tên đối tượng là tên
  nghiệp vụ, góp ý BA chị Thuỷ · `hdsd-documenter/SKILL.md` · `testcase-documenter/SKILL.md`.

### SRS
Form quốc gia (Phần 1–5) như danh mục kho, chức năng theo đúng màn: Xem báo cáo, Tìm kiếm/lọc, (Xem chi tiết/popup), Xuất Excel,
In, Tùy chỉnh cột… — chỉ những gì code có. Mọi chức năng đủ 2 bảng "Mô tả chi tiết giao diện" + "Danh sách event". Phần 2 quyền +
PHẠM VI DỮ LIỆU (ai xem được số của ai) theo code. Phần 5: màn khác dùng chung dữ liệu/tham chiếu (grep, không bịa).

### HDSD (user chốt 02/11): GỌN form quốc gia + thêm 1 PHẦN "ĐỌC BÁO CÁO"
- Khung gọn như danh mục kho: Bìa · MỤC LỤC · TỔNG QUAN (Thuật ngữ · Cập nhật tài liệu 1.0 | 02/11/2026 | Đội phát triển phần
  mềm | Phát hành lần đầu · Quyền sử dụng · Sơ đồ chức năng tổng quan) · PHẦN 1 TRUY CẬP VÀ TÌM KIẾM (bộ lọc, Bước n + icon) · mỗi
  thao tác 1 PHẦN.
- THÊM 1 PHẦN "ĐỌC BÁO CÁO" (đặt ngay sau PHẦN 1): ảnh thật của bảng báo cáo có số liệu + bảng ngắn `Cột | Ý nghĩa / lấy số từ
  đâu` (chứng từ nguồn, điều kiện tính, dòng tổng cộng thế nào) + 1 ví dụ cộng số đọc TỪ CHÍNH ẢNH (vd dòng tổng = tổng các dòng
  con). Ngoại lệ duy nhất cho quy tắc "không bảng / không văn xuôi" của bản gọn. Câu ngắn, không thuật ngữ code.

### Testcase (form 17 cột, engine `hrm-claude-config/hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`)
- Nhóm: phân quyền + phạm vi dữ liệu · giao diện · bộ lọc (từng ô, kết hợp, mặc định, ngày ngược chiều) · số liệu (mỗi cột, dòng
  tổng, làm tròn, định dạng `1,234,567`) · **luồng phát sinh**: lập chứng từ gốc trên HRM rồi kiểm số trên báo cáo tăng/giảm đúng
  (khuôn ý tưởng `hrm-claude-config/erp/.plans/erp-bao-cao-cong-no-khach-hang/common.py` → `data_change_tcs`; chỉ dùng chứng từ HRM lập
  được, chứng từ chỉ lập ở ERP thì ghi Tiền điều kiện "có sẵn") · popup chi tiết · Xuất Excel / In · hiệu năng (thời gian tải khi
  không lọc).
- Đã có TC cũ cho màn ERP (chỉ tham khảo, không chép nguyên): `erp/.plans/erp-bao-cao-chi-phi-van-chuyen-theo-nvkd/`,
  `erp/.plans/erp-bao-cao-cong-no-khach-hang/`. Giọng tester, không emoji, không thuật ngữ code, Expected nêu số/câu nguyên văn.

## Nguồn tham khảo luồng số liệu (đọc được, KHÔNG chép nội dung ERP vào tài liệu)
- Công nợ: `sale-customer-debt-reports/kich-ban-nghiem-thu/` (kịch bản nghiệm thu HRM-ERP), docblock "Giữ y ERP / Khác ERP" đầu các
  service `hrm-api/.../CustomerDebt/*`, HDSD + TC ERP trong `hrm-claude-config/erp/.plans/erp-bao-cao-cong-no-khach-hang/`.
- Chi phí vận chuyển: `hrm-claude-config/erp/.plans/erp-bao-cao-chi-phi-van-chuyen-theo-nvkd/`.

## Chụp ảnh — dev-hrm, headless riêng (như danh mục kho)
- `_capture_login.js` / `pw_dev.js`. Báo cáo là màn CHỈ ĐỌC — được bấm Tìm kiếm, mở popup, Xuất Excel (file tải về để trong thư
  mục mình), mở trang In (không bấm In ra máy in). Vẫn KHÔNG bấm Lưu/Xoá/Duyệt bất kỳ phiếu nào.
- Chọn bộ lọc cho ra SỐ LIỆU THẬT (không chụp bảng rỗng): thử kỳ/khách hàng/nhân viên có phát sinh. Báo cáo tải chậm → chờ đủ
  (networkidle + có dòng), ghi lại thời gian tải khi không lọc (đưa vào TC hiệu năng).
- Tài khoản dev có thể là Super admin — chụp thêm góc nhìn phạm vi hẹp nếu code có phân cấp thì ghi rõ trong báo cáo, không cần ảnh.

## Tự kiểm trước khi báo xong
Như danh mục kho (render PDF và XEM bằng Read: bìa, mục lục, Xem báo cáo + bảng cách lấy dữ liệu, Phần 4, Phần 5 SRS; bìa, tổng
quan, Phần 1, PHẦN Đọc báo cáo của HDSD; font Times New Roman, chữ bảng 13pt, mục lục không còn chữ khuôn).

## Báo cáo cuối (ngắn)
Đường dẫn 3 file + số trang; số TC theo nhóm; danh sách nghi lỗi code / số liệu nghi sai (mỗi dòng: mô tả · TC liên quan);
chỗ chưa chắc; ảnh nào phải giả lập (nếu có).
