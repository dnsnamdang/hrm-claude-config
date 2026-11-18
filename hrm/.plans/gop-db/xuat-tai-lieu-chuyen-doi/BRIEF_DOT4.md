# Brief Đợt 4 (18/11/2026) — SRS + HDSD + Testcase cho 12 màn HRM "Đã test"

Làm bằng tiếng Việt. KHÔNG commit git, KHÔNG upload Drive, KHÔNG sửa code app (`hrm-api`, `hrm-client`), KHÔNG sửa lib / skill
dùng chung, KHÔNG sửa file của màn khác. Nghi lỗi code → chỉ GHI vào báo cáo cuối (mỗi dòng: mô tả · TC liên quan).
Tài liệu viết cho **HRM theo code hiện tại** (`develop`, đã deploy dev-hrm), KHÔNG mô tả / đối chiếu ERP.

(Màn 225 "Công nợ đầu kỳ theo khách hàng - hợp đồng" = cùng màn 167 Khai báo đầu kỳ công nợ, tài liệu 167 đã có cả 2 đường menu →
KHÔNG làm lại.)

## 12 màn (thư mục tính từ `hrm-claude-config/hrm/.plans/gop-db/`)

| STT | Tên tài liệu (tên file) | Loại | Route FE | Menu (`hrm-client/components/subsystem-menu/`) | Feature đọc design/plan | Đầu ra | TC cũ |
|---|---|---|---|---|---|---|---|
| 97 | Danh sách đăng ký khách hàng toàn công ty | bao_cao | `/assign/report/customer-registers` | `presale.js` | `presale-customer-registers/` | `presale-customer-registers/docs/` | `gen_testcase.py` (khuôn cũ) |
| 108 | Báo cáo phân chia thị trường | bao_cao | `/assign/report/division-market` | `presale.js` | `presale-division-market-report/` (code vừa làm lại — theo code hiện tại) | `presale-division-market-report/docs/` | — |
| 181 | Danh sách cần hạch toán chi phí vận chuyển nhanh | phieu (danh sách việc cần làm + thao tác hạch toán; nếu chỉ xem thì bao_cao) | `/finance/fast-delivery-accountings` | `finance.js` | `hach-toan-cpvc-nhanh/` | `hach-toan-cpvc-nhanh/docs/` | `hach-toan-cpvc-nhanh/testcase/` |
| 222 | Sổ chi tiết công nợ phải thu khách hàng | bao_cao | `/finance/customer-ledger-details` | `finance.js` | `cong-no-khach-hang/` | `cong-no-khach-hang/docs/so-chi-tiet/` | — |
| 229 | Sổ chi tiết công nợ nhân viên | bao_cao | `/finance/employee-debt-details` | `finance.js` | `so-chi-tiet-cong-no-nv/` | `so-chi-tiet-cong-no-nv/docs/` | — |
| 287 | Phiếu nhập kho điều chỉnh kiểm kê | phieu | `/warehouse/inventory-imports` | `warehouse.js` | `phieu-nhap-kho-dieu-chinh-kiem-ke/` (+ `redmine-11841-nhap-kho-dieu-chinh-kiem-ke/`) | `phieu-nhap-kho-dieu-chinh-kiem-ke/docs/` | — |
| 288 | Phiếu nhập kho chờ báo thừa, thiếu | phieu (danh sách chờ lập phiếu báo) | `/warehouse/import-discrepancies` | `warehouse.js` | `nhap-kho-con-lai/` | `phieu-bao-hang-thua-thieu-nhap-kho/docs/cho-bao/` | — |
| 289 | Phiếu báo hàng thừa, thiếu nhập kho | phieu | `/warehouse/exc-shortage-imports` | `warehouse.js` | `phieu-bao-hang-thua-thieu-nhap-kho/`, `nhap-kho-con-lai/` | `phieu-bao-hang-thua-thieu-nhap-kho/docs/phieu/` | — |
| 309 | Báo cáo cẩu hàng bốc xếp theo nhà cung cấp | bao_cao | `/transport/arrange-reports/by-supplier` | `transport.js` | `van-chuyen-bao-cao/` | `van-chuyen-bao-cao/docs/cau-hang-ncc/` | — |
| 310 | Báo cáo cẩu hàng bốc xếp theo nhân viên | bao_cao | `/transport/arrange-reports/by-employee` | `transport.js` | `van-chuyen-bao-cao/` | `van-chuyen-bao-cao/docs/cau-hang-nv/` | — |
| 319 | Báo cáo hiệu quả gộp xe vận tải | bao_cao | `/transport/trip-gross-reports/by-vehicle` | `transport.js` | `van-chuyen-bao-cao/` | `van-chuyen-bao-cao/docs/hieu-qua-gop-xe/` | — (`van-chuyen-bao-cao/testcase/` là màn KHÁC: chi tiết hiệu quả gộp theo chuyến — chỉ tham khảo) |
| 321 | Báo cáo chi tiết chuyến xe | bao_cao | `/transport/trip-detail-report` | `transport.js` | `van-chuyen-bao-cao/` | `van-chuyen-bao-cao/docs/chi-tiet-chuyen-xe/` | — |

Một màn nằm ở nhiều phân hệ → grep cả các file menu khác, ghi đủ các đường ("Hoặc Menu: …"). Nhãn menu lấy NGUYÊN VĂN từ file menu.

## Khuôn — đã được user duyệt, CHÉP Y HỆT
- **Báo cáo**: đọc `xuat-tai-lieu-chuyen-doi/BRIEF_DOT2.md` (SRS form quốc gia + quy tắc màn báo cáo của srs-documenter; HDSD gọn +
  PHẦN "ĐỌC BÁO CÁO"). Mẫu đã duyệt: `sale-customer-debt-reports/docs/compare/`, `lookup-stock-companies/docs/`.
- **Phiếu**: đọc `xuat-tai-lieu-chuyen-doi/BRIEF_DOT3.md` (kể cả mục "Bổ sung sau màn mẫu"). Mẫu đã duyệt:
  `finance-declare-debt-beginning/docs/kh/` + phần chung `xuat-tai-lieu-chuyen-doi/_lib_phieu.py`, `_capture_phieu.js`.
- Thư viện / quy tắc chung (font, Use Case, Word finalize, chụp an toàn, tự kiểm): `danh-muc-kho/docs/BRIEF_AGENT.md`,
  `danh-muc-kho/docs/_lib_win.py`, `_capture_login.js`.
- **SRS** tự đối chiếu tab "SRS" của `hrm-claude-config/hrm/.claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx`
  (163 mục nội dung cần có) — mục nào áp dụng mà thiếu thì bổ sung.

## TESTCASE — KHUÔN CHUẨN MỚI (03/11/2026), ĐỌC KỸ, KHÔNG theo phần TC trong BRIEF_DOT2/DOT3 hay các gen_testcase cũ
- Đọc `hrm-claude-config/hrm/.claude/skills/testcase-documenter/SKILL.md` (đã sửa theo tab "13. DM quốc gia").
- Sinh bằng `assets/tc_chuan.py` → `build_chuan(..., loai='bao_cao'|'phieu')`; `assets/check_tc.py` phải **0 lỗi**.
- Tham chiếu: `assets/TC_MAU_QUOC_GIA.xlsx` (bắt chước câu chữ) + tab "Testcase" của `assets/CHECKLIST_TC_SRS.xlsx` (mỗi dòng áp dụng được
  có ≥ 1 case). Mẫu đã làm đúng khuôn: `sale-customer-debt-reports/docs/compare/gen_testcase.py` (báo cáo),
  `finance-declare-debt-beginning/docs/kh/gen_testcase.py` (phiếu).
- Có TC cũ → giữ case nghiệp vụ, xếp lại đúng nhóm. Cột KQ thực tế / DNS check để TRỐNG.

## Chụp ảnh — dev-hrm headless riêng; AN TOÀN tuyệt đối
Không bấm xác nhận Lưu / Lưu nháp / Gửi duyệt / Duyệt / Từ chối / Huỷ / Xoá / Import / Hạch toán. Báo cáo được Tìm kiếm, mở popup,
Xuất Excel, xem trước In. Thiếu dữ liệu / trạng thái → đổi tạm trên trình duyệt + ghi rõ ảnh giả lập. Xong XOÁ file `.dev_state.json`
trong thư mục đầu ra (chứa phiên đăng nhập).

## Báo cáo cuối (NGẮN)
Mỗi màn: đường dẫn 3 file + số trang SRS/HDSD; số TC + check_tc 0 lỗi?; nghi lỗi code (mô tả · TC); chỗ chưa chắc; ảnh giả lập.
