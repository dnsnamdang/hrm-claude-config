# Brief Đợt 3 — SRS + HDSD + Testcase cho 7 PHIẾU NGHIỆP VỤ HRM

Làm bằng tiếng Việt. KHÔNG commit git, KHÔNG upload Drive, KHÔNG sửa code app (`hrm-api`, `hrm-client`), KHÔNG sửa thư viện /
skill dùng chung, KHÔNG sửa file của màn khác. Nghi lỗi code → chỉ GHI vào báo cáo cuối (mỗi dòng: mô tả · TC liên quan).

Tài liệu viết cho **HRM theo code hiện tại** (`develop`), KHÔNG mô tả / đối chiếu ERP. Testcase cũ có phần đối chiếu ERP → rà lại.

## 7 phiếu (thư mục tính từ `hrm-claude-config/hrm/.plans/gop-db/`)

| STT | Tên tài liệu (tên file) | Route FE | Menu (`hrm-client/components/subsystem-menu/`) | Feature (design/plan) | Đầu ra | TC cũ |
|---|---|---|---|---|---|---|
| 167 | Khai báo đầu kỳ công nợ | `/finance/declare-debt-beginnings` | `finance.js` | `finance-declare-debt-beginning/` | `finance-declare-debt-beginning/docs/kh/` | `gen_testcase.py` + `testcase HRM - Khai bao dau ky cong no.xlsx` |
| 168 | Khai báo đầu kỳ công nợ nhà cung cấp | `/finance/declare-debt-supplier-beginnings` | `finance.js` | như trên | `finance-declare-debt-beginning/docs/ncc/` | `testcase HRM - Khai bao dau ky cong no nha cung cap.xlsx` |
| 202 | Phiếu huỷ hàng giữ kế toán | `/finance/accounting-prepick-cancels` | `finance.js` | `finance-accounting-prepick-cancel/` | `…/docs/` | `gen_testcase.py` + `testcase - Phieu huy hang giu ke toan.xlsx` |
| 283 | Khai báo tồn kho đầu kỳ | `/warehouse/beginning-stocks` | `warehouse.js` | `ton-kho-dau-ky/` | `…/docs/` | — |
| 178 | Phiếu nhập kho | `/finance/warehouse-imports` | `finance.js` + `warehouse.js` (1 màn 2 phân hệ — ghi cả 2 đường) | `phieu-nhap-kho/` | `…/docs/` | — |
| 204 | Phiếu điều chuyển hàng | `/finance/product-transfers` | `finance.js` | `finance-product-transfer/` (+ `khao-sat.md`) | `…/docs/` | — |
| 63 | Yêu cầu mua dịch vụ | `/finance/buy-service-requests?type=all` | `sale-hub.js` (+ kiểm `finance.js`) | `buy-service-request/` | `…/docs/` | — |

Đọc `design.md` + `plan.md` của feature trước (quyết định đã chốt, lỗi Redmine đã sửa). Đường dẫn trong tài liệu: "Menu: Phân hệ
<tên hiển thị> => … => <mục menu>" lấy nhãn THẬT từ file menu / màn hub. Không URL.

## Đầu ra mỗi phiếu (thư mục Đầu ra)
`SRS - <Tên>.docx`, `HDSD_<Tên>.docx`, `testcase - <Tên>.xlsx`, `out/*.pdf`, script sinh, ảnh `hdsd_shots/`, `icons/`, `uml/` (local).

## Khuôn — form quốc gia cho màn PHIẾU (TPE Pass)
- Màn phiếu mẫu ĐÃ DUYỆT (bản trên Drive): STT 27 Phiếu chuyển hàng nhập thẳng — `finance-product-import-direct-transfer/form_qg/`
  (`out/*.docx` = cấu trúc SRS/HDSD phiếu chuẩn để bám; `gen_hdsd.py` dùng `phieu-theo-form-quoc-gia/hdsd_phieu_lib.py`).
  Đọc kỹ `phieu-theo-form-quoc-gia/BRIEF_AGENT.md` + `CHECKLIST.md` (mọi góp ý TPE cho SRS/HDSD phiếu).
- Bộ đã duyệt hôm nay (dựng SRS từ đầu trên khuôn quốc gia, chạy Windows): `danh-muc-kho/docs/` (`_lib_win.py`, `_capture_login.js`,
  `warehouses/` 5 script) và `danh-muc-kho/docs/BRIEF_AGENT.md` (font, Use Case, Word finalize, chụp an toàn, tự kiểm). Phiếu ở đây
  CHƯA có bản Drive → SRS dựng mới (không vá), bám cấu trúc SRS màn 27. Cần hàm mới thì viết trong thư mục mình, KHÔNG sửa lib chung.
- Skill: `hrm-claude-config/hrm/.claude/skills/srs-documenter/SKILL.md`, `hdsd-documenter/SKILL.md`, `testcase-documenter/SKILL.md`.

### SRS — điểm riêng của PHIẾU (ngoài checklist TPE)
- Chức năng theo đúng code: Xem danh sách, Tìm kiếm/lọc, Thêm mới (lập phiếu, chọn chứng từ nguồn nếu có), Sửa, Xem chi tiết, Xoá,
  Gửi duyệt / Duyệt / Từ chối / Huỷ (nếu có), In, Xuất Excel, Lịch sử, Tùy chỉnh cột, Cài đặt bộ lọc, Import (nếu có).
- BẮT BUỘC có **luồng trạng thái**: bảng Trạng thái | Ý nghĩa | Thao tác được phép | Ai làm; sơ đồ luồng (PNG) nếu > 2 trạng thái.
- Mỗi thao tác đổi trạng thái: Điều kiện ban đầu ghi trạng thái phiếu; bước "Ghi nhận lịch sử"; tác động sang chứng từ/số liệu khác
  (vd trừ hàng giữ, sinh bút toán, cập nhật tồn) — ghi theo code.
- Phần 2: quyền + PHẠM VI DỮ LIỆU (ai xem phiếu của ai). Phần 5: màn đọc/dùng dữ liệu phiếu (grep, không bịa).

### HDSD — GỌN form quốc gia (như màn 27 và danh mục kho)
Bìa · MỤC LỤC · TỔNG QUAN (Thuật ngữ · Cập nhật tài liệu 1.0 | 02/11/2026 | Đội phát triển phần mềm | Phát hành lần đầu · Quyền sử
dụng · Sơ đồ chức năng tổng quan) · PHẦN 1 TRUY CẬP VÀ TÌM KIẾM · mỗi thao tác 1 PHẦN ("Bước n" + icon inline + 1 ảnh; lập phiếu nêu
rõ trường bắt buộc / tùy chọn / tự điền). Giữ ý nghiệp vụ quan trọng dưới dạng bước (vd "Lưu nháp chưa trừ hàng").

### Testcase (form 17 cột, `tc_engine.py`)
Có TC cũ → chép generator sang thư mục đầu ra, rà theo code hiện tại (bỏ case ERP / gọi thẳng API, sửa nhãn nguyên văn, thêm case
thiếu). Chưa có → viết mới. Nhóm bắt buộc: quyền + phạm vi · danh sách/lọc · lập phiếu (validate từng trường) · sửa/xoá theo trạng
thái · luồng duyệt đủ nhánh · tác động số liệu (tồn/công nợ/hàng giữ thay đổi đúng) · in/xuất · lịch sử. Giọng tester, không emoji,
không thuật ngữ code. Báo số case giữ/sửa/thêm/bỏ (nếu có TC cũ).

## Chụp ảnh — dev-hrm headless riêng (`_capture_login.js` / `pw_dev.js`)
- AN TOÀN tuyệt đối: dev là dữ liệu dùng chung — KHÔNG bấm xác nhận Lưu / Lưu nháp / Gửi duyệt / Duyệt / Từ chối / Huỷ / Xoá / Import.
  Mở form → điền thử để chụp → Đóng/Huỷ/Quay lại (xác nhận "Thoát" ở hộp chưa lưu là được). Hộp xác nhận: chụp có nội dung → Huỷ.
- Cần phiếu ở từng trạng thái (Nháp / Chờ duyệt / Đã duyệt…) → tìm phiếu có sẵn trên dev; thiếu thì chỉ đổi tạm trên trình duyệt
  (không ghi dữ liệu) và GHI RÕ ảnh nào giả lập trong báo cáo. Lịch sử: chọn phiếu CÓ lịch sử.
- Kiểm quyền tài khoản trước; thiếu nút vì thiếu quyền → báo, đừng chụp ảnh thiếu nút.

## Tự kiểm + báo cáo cuối
Như danh mục kho (render PDF, XEM bằng Read: bìa, mục lục, luồng trạng thái, Thêm mới, Duyệt, Phần 4, Phần 5 SRS; bìa, tổng quan,
Phần 1, Lập phiếu HDSD; font Times New Roman, chữ bảng 13pt, mục lục sạch). Báo cáo NGẮN: đường dẫn 3 file + số trang; số TC (giữ/
sửa/thêm/bỏ); nghi lỗi code; chỗ chưa chắc; ảnh giả lập.

## Bổ sung sau màn mẫu (user duyệt 02/11/2026)
- MÀN MẪU PHIẾU ĐÃ DUYỆT: `finance-declare-debt-beginning/docs/kh/` (5 script) + phần chung `xuat-tai-lieu-chuyen-doi/_lib_phieu.py`
  (`build_srs`, `draw_state_flow`, `finalize_and_check`…) và `_capture_phieu.js` (`confirmShot`, `leaveUnsaved`, `fakeJson`/`mockJson`,
  `menuIcons`, `rowAction`, `run`). CHÉP KHUÔN Y HỆT, chỉ đổi dữ liệu + phần riêng. KHÔNG sửa `_lib_phieu.py`, `_capture_phieu.js`,
  `danh-muc-kho/docs/_lib_win.py`, thư mục `docs/kh/` (agent khác dùng song song) — cần thêm thì viết trong thư mục mình.
- Luồng trạng thái phiếu KHÔNG qua duyệt: trình bày như mẫu (trạng thái do hệ thống tự xác định + Đã xóa, bảng + sơ đồ) — user duyệt.
- Phiếu CÓ duyệt: bảng + sơ đồ đủ mọi trạng thái/nhánh theo code.
- Ảnh giả lập (lịch sử, ô form điền tạm trên trình duyệt, trạng thái thiếu trên dev) được chấp nhận — ghi rõ trong báo cáo.
