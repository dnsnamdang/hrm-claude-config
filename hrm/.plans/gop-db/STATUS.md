# STATUS.md — Phần GỘP DATABASE (nhánh `gop_db`)

> File này chỉ theo dõi các feature làm trên nhánh `gop_db` (hoặc nhánh checkout ra từ `gop_db`).
> Feature trên nhánh khác → ghi ở `.plans/STATUS.md`.

## ⚠️ Nền tảng — đọc TRƯỚC khi làm việc trên nhánh `gop_db`

**`.plans/gop-db/design.md`** — nhánh `gop_db` (cả 2 repo) gộp DB ERP + HRM thành DB duy nhất `local_hrm_erp`.
Ảnh hưởng tới MỌI feature làm trên nhánh này: bảng trùng tên ưu tiên bản ERP (bản HRM đổi tên `hrm_*`, 24 bảng),
`roles`/`permissions`/`files`/`groups` là của **ERP** — dữ liệu HRM nằm ở `hrm_*`;
riêng **`employees` + `employee_infos` đã gộp chung từ 2026-08-03** → `auth()->user()->id` là id nhân viên
duy nhất, `hrm_employees` là bảng cũ bỏ đi (xem mục 0b của design.md);
`mysql2` vẫn trỏ DB ERP CŨ (nguồn bug id lệch); kèm 7 gotcha bắt buộc biết khi port màn ERP → HRM.
Việc gộp DB **không có migration trong repo** → không tái tạo được từ code, phải xin dump.

**Quy tắc bắt buộc (chi tiết ở `CLAUDE.md` mục "Phần GỘP DATABASE"):**
- Nhận biết bằng **nhánh git đang đứng**, không đoán theo tên feature: đang ở `gop_db` hoặc nhánh checkout ra từ `gop_db` → áp dụng quy tắc này
- Tài liệu: feature làm trên nhánh đó nằm trong **`.plans/gop-db/[feature]/`**, spec chi tiết ở `docs/superpowers/specs/gop-db/`
- Code: chỉ làm **trên nhánh `gop_db`** hoặc nhánh **checkout ra từ `gop_db`**, merge trả về `gop_db`
- KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND` cho tính năng mới

## Tài liệu TC + HDSD theo form mẫu của team (2026-08-13)

Sinh lại **testcase** theo form mẫu chuẩn (17 cột, 2 khối summary DNS/TP) và **HDSD Word**
cho **7 màn chuyển phân hệ của @junfoke** — tổng **623 test case** và **7 file HDSD**.
Ảnh HDSD chụp thật trên cổng dev `hrm-crm.eteksofts.com` (22 ảnh, chỉ để local).

| Màn hình | TC | P0 | HDSD |
| --- | --- | --- | --- |
| Danh mục tiền tệ | 117 | 49% | 17 trang |
| Danh mục tài khoản | 128 | 66% | 16 trang |
| Danh mục loại tài khoản | 104 | 61% | 16 trang |
| Cấp dịch vụ bảo dưỡng | 75 | 56% | 11 trang |
| Danh mục ghi chú kiểm tra bảo dưỡng | 75 | 55% | 11 trang |
| Danh mục serial thiết bị làm dịch vụ | 67 | 63% | 11 trang |
| Cập nhật nhanh giá dịch vụ | 57 | 63% | 11 trang |

Đóng gói thêm 2 engine dùng chung vào skill (trước đây mỗi feature phải nhân bản ~1.300 dòng):
`.claude/skills/testcase-documenter/assets/tc_engine.py` và
`.claude/skills/hdsd-documenter/assets/hdsd_engine.py`.
Generator của từng màn nằm cùng thư mục tài liệu (`gen_testcase*.py`, `gen_hdsd*.py`).

Đã xóa 2 file `testcase.xlsx` bản cũ (format 15 cột, gộp nhiều màn) ở `finance-account-catalog` và
`customer-care-maintenance-catalogs` — user chốt 2026-08-13, thay bằng file tách theo từng màn.

## Tài liệu SRS + Testcase (2026-08-07)

Đã sinh `srs.html` + `srs.docx` + `testcase.xlsx` cho **6 màn nghiệp vụ của @junfoke**
(tổng 438 test case, P0 54-62%).
Bám code thật: validation lấy từ Request class, schema từ Entity, API từ Routes, business rule từ Service.

| Feature | TC | Feature | TC |
| --- | --- | --- | --- |
| finance-account-catalog | 98 | customer-care-cost-catalog | 82 |
| finance-currency-catalog | 68 | customer-care-serial-catalog | 58 |
| customer-care-maintenance-catalogs | 74 | customer-care-service-price-config | 58 |

**Chưa sinh:** `bank-account-catalog` và `customer-care-services-catalog` (của @khoipv — chủ feature tự làm);
nhóm hạ tầng/refactor (tach-phan-he-erp-hrm, bo-sung-menu-phan-he, chuyen-code-phan-he,
customer-cut-mysql2, banks-cut-mysql2) — không phải màn nghiệp vụ.

⚠️ **2 việc phát hiện khi soát code để viết tài liệu:**

1. `PermissionsTableSeeder` khai TRÙNG quyền tiền tệ: id 1115/1116 và 1117/1118 cùng `name` cùng guard `api`
   → chạy seeder trên DB sạch sẽ nổ lỗi trùng khóa. Cần bỏ 1 cặp.
2. `bank-account-catalog` (@khoipv) có design.md + plan.md, code đã xong nhưng **chưa có mục trong STATUS.md này**
   → nhờ @khoipv bổ sung.

## Đang làm

- **finance-bill-adjust-dept — Phiếu kế toán (ERP `bill_adjust_dept` → HRM)** → @khoipv →
  `.plans/gop-db/finance-bill-adjust-dept/design.md` · `plan.md` ·
  spec `docs/superpowers/specs/gop-db/2026-08-28-finance-bill-adjust-dept-design.md`
  Trạng thái: **CODE XONG BE + FE (52/54 task) — CHỜ USER MỞ TRÌNH DUYỆT** (2026-08-28).
  BE 20 file mới + 4 file sửa · FE 9 file mới + 1 file sửa (menu) · 0 bảng mới · 2 quyền mới
  (id 1551-1552) · 4 morphMap bổ sung.
  Kiểm chứng: **150 phiếu ERP / 403 dòng bút toán / 33 cột khớp tuyệt đối với sổ cái ERP**;
  phạm vi quyền khớp SQL 6/6 NV; vòng đời đầy đủ chạy trong transaction rồi rollback;
  4/5 luật validate chặn đúng; 10 endpoint smoke test 200; FE 9/9 compile sạch.
  **ĐÃ TEST PLAYWRIGHT + ĐỐI CHIẾU TRỰC TIẾP VỚI ERP (2026-08-28)**: 20/20 bộ lọc khớp tuyệt đối;
  bấm thật danh sách / sort / phân trang / ghi nhớ lọc / 3 popup / cửa vào từ Phiếu YCĐC /
  duyệt-ghi-sổ / xoá / in / xuất Excel. **Tìm và sửa 7 lỗi** (ô lọc NVKD chết, Excel danh sách
  mất 9/11 cột, cột Phòng ban sai nguồn, bản in lệch ERP 6 điểm, ô chỉ-đọc còn là input, popup
  xuất không đóng, popup hợp đồng trả id thay vì tên). Chứng minh được ô lọc "STK ngân hàng"
  của ERP nổ HTTP 500. Chi tiết ở `plan.md` Phase 10.
  Còn lại: phần chưa kiểm chứng được (nhánh code chết + 2 cửa vào chưa có màn nguồn + phiếu ngoại tệ).
  Mắt xích cuối của luồng đã port dở: Đề nghị điều chỉnh công nợ / Hạch toán bổ sung → **Phiếu kế
  toán → ghi sổ cái `account_details`**. User chốt *"làm hệt ERP"*: đủ 5 cửa vào tạo phiếu, quyền
  xem 2 cấp, sửa/xóa = Đang tạo + đúng người lập, ô chọn hợp đồng bán lấy **cả `hrm_contracts` lẫn
  `firm_contracts`**.
  ⚠️ Feature này **gỡ ràng buộc "HRM không ghi sổ cái"** mà `finance-bill-adjust-dept-request` từng
  chốt (quyết định #3) — sổ cái dùng chung với cổng ERP, sai/trùng là lệch số kế toán thật.
  Nền: 12.628 phiếu · 33.409 dòng chi tiết · 0 bảng mới · 2 quyền mới · 4 morphMap phải bổ sung.

- thiet-ke-lai-phan-quyen → @namdangit → .plans/gop-db/thiet-ke-lai-phan-quyen/plan.md
  Trạng thái: **PHASE 0 XONG — MOCKUP CHỐT (verify Playwright), CHƯA PORT VÀO hrm-client THẬT** (2026-08-14).
  Mục tiêu: thiết kế lại màn phân quyền, đưa về phân hệ "Quản trị hệ thống"; gọn/khoa học + tìm kiếm + gom nhóm. Phase 1 = UI (không đụng DB), Phase 2 = BE restructure (sau).
  Mô hình chốt: Loại (Xem/Thao tác/Duyệt) × Phạm vi (Tổng cty→Bộ phận, cấp cao gồm cấp thấp; Duyệt mặc định Công ty; Thao tác không phạm vi); phân quyền theo 1 công ty của user; phân hệ = card → chức năng = bảng (Loại|Tên quyền|Phạm vi); bộ lọc phân tầng + loại quyền; panel tổng hợp 8:4 + chip theo phân hệ; danh sách có popup "Quyền đang có"; Lưu ở cuối form.
  Mockup: `.plans/demo-man-hinh-ke-toan/demo/phan-quyen.html` + `assets/permissions.js` (+ menu trong `assets/app.js`, card trong `index.html`). Spec: `docs/superpowers/specs/gop-db/2026-08-14-thiet-ke-lai-phan-quyen-design.md`.
  Bước tiếp: Phase 1 — port sang hrm-client (admin.js → màn danh sách → form) + BE store 1 công ty. Trước khi code chốt: (a) cách xác định "công ty của user", (b) quy ước map dữ liệu thật 617 permission → loại×cấp.

- menu-quan-ly-cong-viec → @namdangit → .plans/gop-db/menu-quan-ly-cong-viec/plan.md
  Trạng thái: **IMPLEMENT XONG + VERIFY PLAYWRIGHT 1440 — ĐÃ COMMIT + PUSH lên `gop_db`** (2026-08-10).
  Mục tiêu: đưa phân hệ Quản lý công việc (`assign`) + Đào tạo (`training`) sang sidebar hub navy+teal như các phân hệ mới.
  **Phase 2 (Đào tạo):** thêm `'training'` vào `HUB_SUBSYSTEMS` (training không có nút lẻ → chỉ 1 dòng). Verify `/training/courses`: rail "ĐÀO TẠO" + 12 nhóm, panel bung OK. Cùng file `hub.js`.
  Đã làm: (1) thêm `'assign'` vào `HUB_SUBSYSTEMS`; (2) 3 màn lẻ cấp 1 (my-todo/my-job/tasks daily-report) → nút rail đi thẳng qua `deriveHubNavLinks`+`hubNavLinksFor` (hub.js) + render trong `SaleHubSidebar.vue`, KHÔNG đổi mảng groups; (3) 6 nhóm ERP xám mờ tự động. Dashboard overview ngoài phạm vi.
  Verify: assign my-todo rail navy+teal + 3 nút lẻ + highlight đúng; click nhóm bung panel (12 chức năng); nhóm ERP xám; regression Bán hàng (/sale/dashboard) 0 error, không nút lẻ.
  File đụng: `components/subsystem-menu/hub.js`, `components/sale/SaleHubSidebar.vue`.
  Bước tiếp: user review giao diện → OK thì commit 2 file lên `gop_db`.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-menu-quan-ly-cong-viec-design.md | Tóm tắt: .plans/gop-db/menu-quan-ly-cong-viec/design.md

- ke-hoach-phat-trien-thi-truong → @namdangit → .plans/gop-db/ke-hoach-phat-trien-thi-truong/plan.md
  Trạng thái: **THÊM FILE BÁO CÁO THỨ 2 — "Báo cáo tổng hợp nhu cầu khách hàng" (Task 60→66)** (wrap up 2026-08-20, verify Playwright 1440, 0 lỗi console). Desktop DONE, chờ user review; RESPONSIVE vẫn hoãn.
  **File MỚI:** `bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html` (xem qua `python3 -m http.server 8952` trong thư mục feature) — layout bám ảnh Excel "Báo cáo tổng hợp nhu cầu khách hàng", style tái dùng nguyên token + component của file báo cáo meeting. Nội dung: **toolbar 7 bộ lọc** (Kỳ xem theo thời gian bắt đầu họp · Lĩnh vực KD · Khách hàng · cascade Công ty ▸ Phòng ban ▸ Bộ phận ▸ Kinh doanh chủ trì) · **KPI** (tổng nhu cầu / tổng giá trị đầu tư / khách hàng / chưa có dự án TKT) + 3 khối phân bổ · **bảng outline 3 cấp** `I` Lĩnh vực KD → `1` Thị trường → `1.1` Khách hàng, 10 cột, sticky header + TỔNG CỘNG · **2 chế độ cột** (CHI TIẾT 10 cột ↔ TỔNG HỢP 4 cột, ẩn hết cột rỗng) · nút **"+ TẠO MỚI"** cột Dự án TKT → popup tạo dự án (mã `TKT.YYYY.<viết tắt KH>`) → trạng thái **"Đã lập dự án TKT"** · **click tên meeting → drawer chi tiết meeting** (khung `.ticket-drawer` của file báo cáo meeting, 4 khối + nút Tạo dự án TKT) · Xuất Excel + In báo cáo (tổng hợp/chi tiết, A4 ngang) bám chế độ đang xem · data demo **26 nhu cầu / 18 KH / 4 lĩnh vực / 3 thị trường**.
  Treo thêm: chốt Lĩnh vực KD có cần **chọn nhiều** không (hiện select đơn theo yêu cầu "dùng đúng select như file mẫu", ảnh Excel ghi "select chọn nhiều").
  **File báo cáo ĐỘC LẬP:** `bao-cao-ket-qua-meeting-theo-thi-truong.html` (xem qua `python3 -m http.server 8931` trong thư mục feature). File `...-mockup-meeting.html` nay chỉ còn **2 tab** (Công việc của tôi · Lịch meeting) — tab 3 đã gỡ.
  **Task 44→59 (2026-08-19):** bảng OUTLINE 3 cấp `I / 1 / 1.1` (bỏ rowspan) + cột STT · **2 chế độ cột**: TỔNG HỢP (mặc định tới cấp Khách hàng, mỗi phòng ban 1 cột + Tổng, ẩn cột chi tiết; dòng meeting hiện dấu tick, dòng nhóm hiện số) ↔ CHI TIẾT (13 cột) · cột **Phòng ban** (của người chủ trì) + bộ lọc cascade **Công ty ▸ Phòng ban ▸ Người chủ trì** (lọc phòng/công ty → chỉ hiện cột phòng đó ở bảng/summary/Excel/bản in) · **sắp xếp mọi cột dữ liệu** (từ "Thời gian" sang phải, asc→desc→mặc định; giữ cấu trúc nhóm) · **sticky** hàng tiêu đề + dòng TỔNG CỘNG (dời lên đầu bảng) · click cả dòng meeting → panel chi tiết (drawer của Lịch meeting) · click số ở dòng TỔNG CỘNG → **popup danh sách meeting** kèm nút In + Xuất Excel riêng · **nút In báo cáo** (popup chọn In tổng hợp / In chi tiết, A4 ngang, bám bộ lọc) · **dải tổng hợp thiết kế lại** (4 ô KPI + thanh xếp chồng trạng thái + thanh ngang phòng ban/thị trường), bộ lọc chuyển LÊN TRÊN dải này + nút Ẩn/Hiện tổng hợp · bỏ hẳn nhận dạng "KH mới", tên meeting chữ thường, tăng tương phản 3 cấp màu · **data demo 30 meeting / 11 KH / 3 thị trường** (Hà Nội 14 · TP.HCM 8 · Đà Nẵng 8), phòng ban cân đối 11/11/8.
  Treo: chốt tên 2 công ty demo (tạm Tân Phát ETEK / Tân Phát Sài Gòn) · xử lý bản copy lệch `quan_ly_cong_viec_ca_nhan.html`.
  **Task 43 (2026-08-11):** cột Khách hàng nâng thành ô gộp `rowspan` (đặt sau Thị trường, bỏ khỏi từng dòng meeting, header vẫn 13 cột) → nhóm meeting theo khách hàng; meeting trong 1 KH xếp **cũ→mới**; KH mới vẫn nổi đầu; ô gộp giữ badge KH mới + nút "Xem lịch sử meeting"; Xuất Excel đồng bộ thứ tự. Chỉ sửa `...-mockup-meeting.html` (bản copy `quan_ly_cong_viec_ca_nhan.html` nay đã LỆCH). Helper mới: `groupTicketsByCustomer()`/`buildCustomerGroupCellHtml()`.
  → File chính `...-mockup-meeting.html` (bản copy `quan_ly_cong_viec_ca_nhan.html`): **3 tab** — (1) **Công việc của tôi** (My To Do, tab đầu mặc định: Task/Issue/Cá nhân, nhóm theo thời gian thu gọn/mở rộng đúng màn thật) · (2) **Lịch meeting** (màu nền thẻ theo trạng thái, nút Thêm meeting, drawer nút theo trạng thái) · (3) **Kết quả meeting theo thị trường** (bảng + lọc Thị trường/Trạng thái/Loại/Kỳ + Xuất Excel + KH mới phát triển + cột Dự án TKT + chấm công GPS chỉ Hoàn thành + summary lưới text). Bản `...-mockup.html` (gốc 3 loại) giữ nguyên.
  File: `ke-hoach-phat-trien-thi-truong-mockup.html` (self-contained). Style navy+teal đồng bộ menu Bán hàng.
  **PIVOT v2:** bỏ tab → **1 màn LỊCH phiếu công việc** (Tháng/Tuần). 4 loại phiếu thẻ màu: Phiếu công tác (teal) · Meeting (xanh dương) · Phiếu giao việc (tím) · Task (cam), mỗi thẻ = màu loại + giờ + badge trạng thái (Chờ duyệt/Đang thực hiện/Hoàn thành/Từ chối). 32 phiếu mock.
  Toolbar: Tháng/Năm · Phòng ban · Nhân viên · Người theo dõi · Thị trường · **Loại phiếu · Trạng thái** · Tìm kiếm + **Xóa lọc** — TẤT CẢ lọc thật (re-render lịch + 4 box đếm theo loại). Click thẻ → popover → "Xem chi tiết" → drawer đầy đủ. Đã BỎ footer Đánh giá/Ghi chú.
  v1 (2 tab: accordion thị trường + KPI trạng thái KH) giữ làm phụ lục trong spec.
  **Phase 6 (bám style thật + visual):** khảo sát UI thật `/sale/quotations` → dựng lại filter theo `V2BaseFilterPanel` (card trắng + header teal + quick search + [Tìm kiếm]/[Làm mới] + khối nâng cao lưới 4 cột), lọc AND chạy đúng; 4 box compact; calendar nâng cấp header teal + phân biệt cuối tuần/hôm nay.
  **Phase 7 (tinh chỉnh — feedback lần 2):** (1) chip góc phải = **lọc nhanh theo loại**. (2) **Summary ngữ cảnh**: Loại=Tất cả→box; Loại=1 loại→dải breakdown. (3) **De-bold** chữ ô ngày. (4) **Thiết kế lại** hôm nay/T7/CN tinh tế.
  **Phase 8 (bám dữ liệu THẬT — khảo sát app):** BỎ Phiếu giao việc → **3 loại** (Phiếu công tác/Meeting/Task). Mỗi loại dùng **trường + trạng thái THẬT** khảo sát từ `/assign/assign_business`, `/assign/meeting`, `/assign/tasks`: Công tác(6 tt)/Meeting(4)/Task(4+Quá hạn). Card/popover/drawer đổ đúng bộ trường riêng theo loại; badge màu semantic. Filter Trạng thái **động theo loại**; summary breakdown theo bộ trạng thái thật của loại. Verify Playwright 1440. (Data spec: mục 3B/5B/9B.)
  Concern nhỏ chờ user: khi lọc đồng thời Loại + 1 Trạng thái, dải breakdown chỉ còn 1 mục ≠0.
  **Phase 9 (single-user + gọn filter):** BỎ card bộ lọc trên; màn theo dõi **1 user** (topbar "Lịch công việc — Nguyễn Văn A"); chỉ giữ **Thị trường + Trạng thái** trong **header card calendar**.
  **Phase 10 (màu + card + data + summary):** (1) Task KHÔNG lọc theo Thị trường (chip Task → disable Thị trường). (2) Đổi màu 3 loại tương phản mạnh: công tác `#0d9488` / meeting `#4f46e5` / task `#ea580c`. (3) Thẻ item: dòng1 **icon tròn loại** + tiêu đề, dòng2 **thời gian "Từ - Đến"** + badge trạng thái. (4) Data demo chuẩn: ngày tương lai KHÔNG Hoàn thành/Quá hạn. (5) Summary chọn 1 loại thành **stat-card ấn tượng** (số lớn + pills trạng thái). Verify Playwright 1440.
  **Phase 11 (drawer):** Bỏ popover — click thẻ mở **thẳng drawer**; redesign drawer ấn tượng (header banner gradient theo loại + khối card per-type, meeting có link Meet); **thu nhỏ font + nén gọn** drawer (460px). Verify Playwright 1440.
  **Bổ sung filter:** "Loại meeting" (`#filter-meeting-type`) chỉ hiện khi chọn Meeting (Tất cả + 8 loại distinct), lọc thật, ẩn/reset khi đổi loại — cùng cơ chế disable Thị trường cho Task.
  **Phase 12 (phiếu nhiều ngày):** thêm `endDate` + phiếu multi-day 3 loại (có vắt tuần). View Tháng: **thanh trải** theo lane toàn cục, cắt theo tuần, bo góc/mũi tên ‹› khi còn tiếp, DOM 6 khối tuần (lane layer + day layer chung grid → thẳng hàng). View Tuần: span cột dải "Cả ngày". Drawer "Từ dd/MM – dd/MM", đếm 1 lần/phiếu. Sau đó: multi-day NẰM DƯỚI số ngày, "+N khác" chỉ khi >3, nền transparent bớt chói, **border chia ngày rõ** (liền mạch qua 3 lớp). Verify Playwright 1440.
  **Phase 13 (biến thể CHỈ-MEETING):** clone `...-mockup-meeting.html` (bản gốc 3 loại giữ nguyên) rồi rút gọn về chỉ Meeting: bỏ 3 chip/legend/logic loại, filter luôn hiện Thị trường+Trạng thái(meeting)+Loại meeting, summary luôn stat-card Meeting, topbar "Lịch Meeting", màu indigo, giữ multi-day/drawer/border. Verify Playwright 1440.
  **2 file mockup:** `...-mockup.html` (3 loại, meeting = **tím** indigo) + `...-mockup-meeting.html` (chỉ Meeting, màu = **xanh ngọc** `#06b6d4`). Đã thêm Tên khách hàng trên thẻ (cả 2). Chạy qua http.server (vd port 8912).
  **Bản meeting — 2 TAB:** (1) **Lịch meeting** (calendar như cũ) · (2) **Meeting theo thị trường** = **BẢNG** meeting-centric (theo mẫu mới): header 2 tầng navy, gộp rowspan **Thị trường**; cột: Meeting(Tên/Loại/Thời gian/Địa điểm) · Người chủ trì · Thành phần tham gia(Khách hàng/Thành phần công ty/Thành phần bên KH) · Kết quả meeting(Trạng thái/Biên bản họp-Lý do huỷ). Mỗi meeting 1 dòng; địa điểm online→"Trực tuyến"+link. Field `ketQua`, `nguoiChuTri`, `bienBan`.
  **Bảng tab2 tinh chỉnh (Task 32):** header 2 hàng đồng màu navy; Thị trường = **tỉnh/thành** (bỏ vùng miền + bỏ meeting nội bộ khỏi tab2); chỉ click **Tên meeting** (link) mở drawer; trạng thái dạng **badge**; meeting **Hoàn thành → nút "Xem biên bản" → popup biên bản** đúng mẫu app thật (bảng Nội dung-vấn đề/Phương án xử lý/Người đề xuất/Người thực hiện/Hạn dự kiến + Kết luận cuộc họp); summary thêm **thống kê theo thị trường**.
  **Tinh chỉnh (Task 33):** summary 2 nhóm "Theo trạng thái" + "Theo thị trường" cùng 1 hàng; header bảng tab2 = màu header lịch (teal); +3 meeting Hoàn thành có thị trường (4 nút "Xem biên bản"); thành phần Cty/KH = **chip avatar**; drawer chi tiết: nhãn + tiêu đề khối **chữ thường** (bỏ uppercase), font nhỏ, ít bold.
  **Task 34:** Thành phần công ty = chip **avatar**; Thành phần bên KH = tên + **chức vụ**; ô Khách hàng có nút **"Xem lịch sử meeting"** → popup liệt kê các lần meeting với KH đó.
  **Phase 15 (2026-08-10):** (Task 35) popup lịch sử meeting sort mới→cũ + cột nhân sự + header teal chung + nút Xem biên bản. (36) header bảng 1 cấp + cột "Phiếu công tác/Lịch sử chấm công" (popup chấm công GPS tab theo người) + hover row đậm hơn. (37) lọc Thị trường/Trạng thái/Loại + **Kỳ** (Hôm nay/Tuần/Tháng/Quý/Năm/Tuỳ chọn) + **Xuất Excel**. (38) nút "Thêm meeting" quick-add + drawer nút theo trạng thái (Sửa/Duyệt/Xem biên bản). (39) **KH mới phát triển** (badge+highlight, đưa lên đầu) + cột **Dự án TKT** (chỉ Hoàn thành). (40) summary nhóm Tổng hợp (dự án/KH mới/tỷ lệ HT) + đổi **lưới text** (bỏ chip); chấm công CHỈ meeting Hoàn thành; đổi tên tab2 → "Kết quả meeting theo thị trường". (41) thêm tab **Công việc của tôi** (My To Do) làm tab đầu + đổi tên màn **"Quản lý lịch làm việc cá nhân"** + topbar gọn; group thu gọn/mở rộng đúng `TodoGroupHeader.vue`/`TodoMainList.vue`; chỉ Task/Issue/Cá nhân. (42) lịch meeting **màu nền thẻ theo trạng thái**.
  Bước tiếp: user review desktop → chỉnh → chốt (có tách file riêng cho "Công việc của tôi"?) → responsive → port Vue + đồng bộ My To Do với data thật.
  Spec: docs/superpowers/specs/gop-db/2026-08-08-ke-hoach-phat-trien-thi-truong-design.md | Tóm tắt: .plans/gop-db/ke-hoach-phat-trien-thi-truong/design.md

- menu-ban-hang → @namdangit → .plans/gop-db/menu-ban-hang/plan.md
  Trạng thái: **PORT STYLE "CHỐT" VÀO CODE THẬT — DONE + VERIFY PLAYWRIGHT** (wrap up 2026-08-08). Client nhánh `update_sidebar_menu` (con `gop_db`), API `menu_phan_he_2026`. Tất cả CHƯA commit.
  Áp style navy+teal (port từ mockup chi-tiet-bao-gia) cho **14 phân hệ hub** (`HUB_SUBSYSTEMS`) qua `.sale-theme`, KHÔNG sửa V2 chung:
  · Sidebar navy + ribbon lụa (bg data-URI) + box tên phân hệ sát đỉnh nổi bật + icon phân hệ tô trắng glow + **màu icon menu theo mockup** (palette `CAT_COLORS`).
  · Topbar navy gradient + **wave line sáng mép dưới** (`::after`). Header bảng **#20d9ea** (gradient nhẹ + viền + `nowrap`). Tiêu đề card teal.
  · Panel menu: icon ngữ cảnh cấp 2 (`SCAT_ICONS` trong `SaleHubSidebar.vue`) + nền gradient + accent **xanh** đồng bộ (override `--acc`).
  · Form báo giá (tạo/sửa/xem): Thông tin chung lưới ô + "Loại tiền tệ" 1 dòng + **chip Bảng giá (xanh) / Giảm giá (cam)** + Giảm giá đưa lên header card "Chi tiết báo giá".
  File đụng: `assets/scss/sale-theme.scss`, `components/sale/SaleHubSidebar.vue`, `pages/sale/quotations/_id/index.vue` (client) + `Modules/Assign/Routes/api.php` (API — **alias route `sale/quotations`** fix 404 "không tìm được báo giá": FE gọi sale/quotations nhưng BE chỉ có assign/quotations).
  Bước tiếp: user review 14 phân hệ hub + form báo giá → OK thì báo @junfoke + commit/merge về `gop_db`; BE làm migration route `sale/*` đúng bài (thay cho alias tạm).
  Spec: docs/superpowers/specs/gop-db/2026-08-04-menu-ban-hang-design.md | Tóm tắt: .plans/gop-db/menu-ban-hang/design.md

- mockup-chi-tiet-bao-gia → @namdangit → .plans/gop-db/mockup-chi-tiet-bao-gia/plan.md
  Trạng thái: **MOCKUP ĐÃ QUA 6 PHASE TINH CHỈNH UI — chờ duyệt/định hướng tiếp** (2026-08-06, nhánh `gop_db`).
  File mockup HTML tĩnh mô phỏng màn Chi tiết báo giá thật (`/assign/quotations/80` = BG-2026-00080, *Đang tạo*):
  `chi-tiet-bao-gia-mockup.html`, self-contained (inline CSS + SVG, không CDN). Đủ 8 khối + menu flyout đầy đủ (port từ menu-mockup).
  Đã tinh chỉnh qua các phase (xem plan.md P0–P6):
  · **Màu nhận diện = NỀN màn chọn phân hệ** (navy `#0a1c3d→#1e57a0` + chủ đạo `#2E71C3`), KHÔNG dùng màu nhóm tím.
  · Topbar + sidebar navy hiện đại: glow mềm, active pill phát sáng, icon menu mỗi mục 1 màu.
  · Nền sidebar: **bó ~44 đường sóng ribbon** (SVG sinh bằng script, giống ảnh minimalistic gradient wave user gửi).
  · Card Thông tin chung **thu gọn được** (chevron → summary 1 hàng → đẩy bảng lên).
  · Tiêu đề card teal `#0a99a7`; header bảng teal nhạt + chữ teal (phương án B); button primary/outline/ghost.
  Verify bằng Playwright (qua http.server, Playwright chặn file://). Chạy tại `http://127.0.0.1:8899/`.
  Mục đích: SÂN THỬ NGHIỆM UI — CHƯA áp vào code thật; việc áp vào Vue thật thuộc `update-style-ban-hang`.
  Bước tiếp: tinh chỉnh bó sóng/animation/responsive, hoặc chốt để chuyển sang áp code thật.
  Spec: docs/superpowers/specs/gop-db/2026-08-06-mockup-chi-tiet-bao-gia-design.md | Tóm tắt: .plans/gop-db/mockup-chi-tiet-bao-gia/design.md

- update-style-ban-hang → @namdangit → .plans/gop-db/update-style-ban-hang/plan.md
  Trạng thái: **✅ DESIGN + SPEC + PLAN ĐÃ DUYỆT — chưa code (chờ chạy Phase 0 / note phần đầu tiên)** (2026-08-06, nhánh `gop_db`).
  Đổi style màn Bán hàng thật (`pages/assign/*`, dùng component V2 chung) theo **MISA**, **Cách A**: gate `.sale-theme` ở `default-sidebar.vue` (`isSaleSubsystem`) + 1 file `assets/scss/sale-theme.scss` (tokens teal từ demo kế toán). Chỉ Bán hàng, portable sau. KHÔNG sửa V2 dùng chung. Working mode: tăng dần theo ảnh MISA user note, verify Playwright.
  Plan: Phase 0 (Task 0.1–0.4 setup scaffold, cụ thể) + Phase 1+ backlog (bảng/filter/nút/badge/card/topbar — cụ thể hoá khi user note).
  Bước tiếp: chạy **Phase 0** → chờ user note phần đầu tiên (ảnh MISA + tên thành phần).
  Spec: docs/superpowers/specs/gop-db/2026-08-05-update-style-ban-hang-design.md | Tóm tắt: .plans/gop-db/update-style-ban-hang/design.md

- redesign-man-chon-phan-he → @namdangit → .plans/gop-db/redesign-man-chon-phan-he/plan.md
  Trạng thái: **CODE DONE + ĐÃ VERIFY TRÊN APP THẬT** (2026-08-03, nhánh `menu_phan_he_2026`). Còn: báo @junfoke + merge về `gop_db`.
  Thiết kế lại giao diện màn chọn phân hệ (`pages/index.vue`) sang **bố cục BÔNG HOA** trên nền xanh gradient tối:
  **nhụy tròn** ở giữa (hexagon TP pulse + vòng conic 4 màu xoay + **3 nhị** = lõi Thông tin NS/Danh mục/Quản trị, BỎ ERP),
  **4 cánh** = 4 nhóm nghiệp vụ (panel kính mờ, mũi nhọn hướng tâm, màu riêng, tagline, bỏ số thứ tự), gân sáng nối tâm→cánh,
  hiệu ứng glass/glow/float/hover. CHỈ đổi trình bày, registry vẫn là nguồn dữ liệu. Đã sửa: `subsystems.js` (`tagline`/`desc`/`erpGhost`/`erpLink`),
  `pages/index.vue` (viết lại bố cục hoa), `layouts/system.vue` (nền tối; chỉ index.vue dùng).
  ⚠️ 2 điểm đã xử lý: (1) **ghi đè có chủ đích** quyết định "ẩn hẳn" Mua hàng/Kho/Vận chuyển của `bo-sung-menu-phan-he` →
  hiện BÌNH THƯỜNG (không mờ) + desc riêng, click hiện toast "Tính năng đang phát triển" (chờ ERP làm xong gắn `erpLink`) — **CẦN BÁO @junfoke**.
  (2) Remix Icon: đã đo codepoint 26/26 LỆCH giữa v2.4.0 bundled & v4.3.0 CDN → **không dùng `ri-*`**, badge dùng SVG `image` tô trắng (`brightness(0) invert(1)`),
  nút Đăng xuất inline SVG. Verify desktop bằng mockup dùng chính SVG dự án (nhiều vòng, user đã duyệt concept).
  **Đã polish nhiều vòng (v3):** điểm sáng spark thay hexagon; **2 vòng nhụy xoay ngược chiều**; lá almond + **viền ánh sáng** (mask-composite); fit **1 màn không scroll** + greeting sát top;
  **icon nhóm** (gom vào `SUBSYSTEM_GROUP_META.icon`, dùng chung màn hoa + switcher); tăng tương phản chữ; box-shadow lá chỉ khi hover; nền lá mờ hơn.
  **Popup chuyển phân hệ (SubsystemSwitcher)** cũng đồng bộ: mỗi nhóm full-width + phân hệ 3 cột, badge tròn màu nhóm, icon nhóm, ghim **sát mép phải + sát topbar**, shortLabel, ghost→toast, bỏ nhóm ERP + bỏ số thứ tự.
  File thêm: `components/SubsystemSwitcher.vue`, `components/BasicSubsystem.vue` (CSS ghim dropdown).
  Bước tiếp: **user chạy hrm-client (Node 14)** soi 2 màn thật (chọn phân hệ sau login + popup icon lưới topbar): animation, hover, sát topbar/phải, toast; test cờ use_rice/use_erp/is_use_decision.
  ⚠️ Môi trường phiên làm là Node 12 → chưa chạy Nuxt dev để test end-to-end.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-redesign-man-chon-phan-he-design.md | Tóm tắt: .plans/gop-db/redesign-man-chon-phan-he/design.md

- finance-prepick-stock-list → @junfoke → .plans/gop-db/finance-prepick-stock-list/plan.md
  Trạng thái: **XONG PHASE 0-8** (2026-08-21) — Phase 8 là đợt vá QA redmine 11116. Nhánh `feat/finance-prepick-stock-list`.
  Port màn **Danh sách hàng giữ** sang Tài chính / nhóm Giữ hàng — báo cáo CHỈ ĐỌC, bảng 3 tầng
  Hàng hoá → Nhân viên → Khách hàng, không migration.
  Bước tiếp: user đối chiếu 2 cổng trên dev + test quyền `Xem phiếu hàng giữ theo phòng ban`.
  Chi tiết + gotcha: plan.md

- wr-service-quotation (chứng từ 3) → @namdangit → .plans/gop-db/wr-service-quotation/plan.md
  Trạng thái: **HOÀN THÀNH CODE + ĐÃ TEST BE VÀ GIAO DIỆN** (2026-08-21). Chưa sinh testcase /
  mô tả nghiệp vụ. Cột "Giá vốn" khoá sau quyền `Xem giá vốn hàng hoá` (user chốt) — đã cấp quyền
  đó cho vai trò Super admin trên DB local để test.
  Port màn ERP "Phiếu cung cấp thông tin làm báo giá" — chứng từ THỨ 3 của dây chuyền dịch vụ.
  Phạm vi user chốt 2026-08-21: **chỉ chứng từ 3** (chứng từ 4 Báo giá dịch vụ để đợt sau), tiền
  **tính ở giao diện như ERP**, khối Phiếu bảo hành **giữ dữ liệu nhưng chưa dựng màn**.
  BE: 11 entity + service + notifier + print service + request + controller + 2 resource,
  13 route, 3 quyền mới (id 1515–1517), **KHÔNG migration** (12 bảng ERP đã có trên DB gộp).
  FE: 11 file `pages/customer-care/wr-information-requests/` + `utils/wrServiceQuotationMoney.js`
  + 1 mục menu; nút "Tạo phiếu cung cấp thông tin" ở chứng từ 2 đã nối sang màn này.
  ⚠️ Bảng dữ liệu **dùng chung với Báo giá dịch vụ** qua cột `type` — mọi truy vấn phải kèm `type`.
  Verify: toàn luồng chạy thật trên DB gộp (danh sách/lọc/xuất/in · prefill · lưu nháp · gửi đi kèm
  thông báo đúng người · từ chối · xoá trả trạng thái 2 chứng từ trước); module tính tiền FE đối
  chiếu **39 phiếu thật** khớp tuyệt đối với bản tính ở máy chủ; 11 file `.vue` compile sạch.
  Test GIAO DIỆN trên cổng 3002: lập phiếu · sửa số lượng · thêm dịch vụ · thêm thiết bị bảo dưỡng
  + gói · chuyển Sửa chữa ↔ Bảo hành · lưu · in · xoá · cảnh báo chưa lưu — **tìm và sửa 2 lỗi**:
  thiếu cờ quyền giá vốn ở màn lập mới, và **Lưu nháp luôn thất bại** vì cột `quotation_term`
  NOT NULL nhận `null` (đã thêm `fillDefaults()`).
  ⚠️ Nút "Tạo báo giá dịch vụ" chưa điều hướng được (chứng từ 4 chưa port) — tạm báo toast.

- warranty-repair-handle-request → @namdangit → .plans/gop-db/warranty-repair-handle-request/plan.md
  Trạng thái: **HOÀN THÀNH CODE + ĐÃ TEST + ĐÃ GIAO TÀI LIỆU** (2026-08-21).
  Tài liệu kèm theo: `testcase.xlsx` (87 TC), `Mô tả nghiệp vụ - Phiếu xử lý yêu cầu.docx`,
  testcase bản ERP ở `erp/.plans/warranty-repair-handle-request-erp/` (57 TC).
  Nút "Tạo phiếu cung cấp thông tin" nay đã nối sang chứng từ 3 (không còn báo toast).
  Port màn ERP "Phiếu xử lý yêu cầu" (`/admin/customer-care/warranty_repair_handle_requests`) —
  chứng từ THỨ 2 của dây chuyền dịch vụ, lập từ Phiếu yêu cầu kiểm tra sửa chữa – bảo hành.
  Đã khảo sát: 6 trạng thái · 4 quyền · 3 bảng (`warranty_repair_handle_requests` 5.259 dòng) ·
  mỗi dòng thiết bị chọn LỖI THIẾT BỊ (nhiều) + HÀNH ĐỘNG (Tư vấn điện thoại / CCTT làm báo giá).
  Mọi dòng đều "Tư vấn điện thoại" → phiếu và phiếu yêu cầu gốc đều thành "Đã tư vấn điện thoại";
  ngược lại → "Chờ CCTT", báo cho người có QUYỀN "Tạo phiếu cung cấp thông tin", phiếu yêu cầu gốc
  thành "Đã xử lý".

- warranty-repair-request → @namdangit → .plans/gop-db/warranty-repair-request/plan.md
  Trạng thái: **HOÀN THÀNH CODE + ĐÃ TEST + ĐÃ GIAO TÀI LIỆU** (2026-08-20).
  Code đã chuyển về đúng phân hệ CSKH (`Modules/CustomerCare`, `/customer-care/warranty-repair-requests`,
  menu CSKH → Kiểm tra bảo hành sửa chữa). Tài liệu kèm theo: `testcase.xlsx` (97 TC),
  `Mô tả nghiệp vụ - …docx` (11 chương), testcase bản ERP ở `erp/.plans/warranty-repair-request-erp/`.
  Port màn ERP "Yêu cầu kiểm tra sửa chữa – bảo hành" (`/admin/customer-care/warranty_repair_requests`)
  — chứng từ ĐẦU TIÊN của dây chuyền 9 chứng từ phân hệ Dịch vụ.
  Scope user chốt: **full như ERP** (3 tab · CRUD · Chuyển phòng tiếp nhận · Từ chối · In phiếu ·
  In danh sách · Xuất Excel), giữ đủ **9 trạng thái**, bảng thiết bị đủ **3 nguồn** tp/tpc/ncck,
  **copy nguyên tên quyền ERP**.
  BE: 8 file `Modules/CustomerCare` + 12 route + 4 quyền (id 1177–1180). **KHÔNG có migration** —
  2 bảng `warranty_repair_requests` (5.625 dòng) / `warranty_repair_request_products` đã có sẵn.
  FE: 9 file `pages/customer-care/warranty-repair-requests/` + 1 mục menu.
  Dùng lại đồ có sẵn: popup KH `ChooseErpCustomerModal`, thiết bị KH
  `assign/customers/{id}/equipment`, 2 mẫu in ERP `report_templates` 277/278.
  Verify: 3 tab + Resource + 2 mẫu in chạy thật trên DB gộp; 9 file `.vue` compile sạch.
  ⚠️ Nút "Tạo phiếu xử lý yêu cầu" chưa điều hướng được (màn đó chưa port) — tạm báo toast.
  📌 Session này còn sửa **tài sản chung**: bổ sung quy tắc "BE trả `status_color`" + bảng 9 mã màu
  chuẩn vào `.claude/skills/list-page/SKILL.md` (mục 3c-1, 3c-2) và `CLAUDE.md` → cần PR riêng.

- customer-export-file (Phase 7) → @khoipv → .plans/gop-db/customer-export-file/plan.md
  Trạng thái: **XONG CODE, CHỜ USER TEST TRÌNH DUYỆT** (2026-08-17). Chuyển việc dựng file
  CSV/Excel/PDF của `/assign/customers` từ BE sang **build ở FE** theo yêu cầu user.
  BE thêm `GET assign/customers/export-rows` (JSON theo trang, dùng chung bảng cột với 3 endpoint
  xuất file cũ — 2.000 dòng/lượt ~0,85s, RAM 60MB). FE thêm `utils/export/customerExportFile.js`
  (ExcelJS + jsPDF/autoTable + font DejaVu subset 78KB, import động).
  ⚠️ Team phải `npm install` sau khi kéo nhánh (thêm `jspdf` + `jspdf-autotable`).
  ⚠️ Chưa đo được thời gian DỰNG file ở trình duyệt với 17.5k dòng — nhất là PDF (~600 trang).
  3 endpoint export cũ của BE vẫn giữ nguyên, chưa xoá.

- finance-prepick-cancel → @junfoke → .plans/gop-db/finance-prepick-cancel-request/plan.md
  Trạng thái: **XONG PHASE 0-12** (2026-08-22) — Phase 10 vá QA redmine 11094/11149/11150/11151/11152/11154,
  Phase 11 bỏ tab preset (1 màn = `all` của ERP, nút duyệt theo quyền), Phase 12 rà màn Phiếu hủy
  theo quy tắc chung (bỏ tự kéo số về trần, duyệt xong về danh sách, nút In trắng, 4 icon ⓘ).
  Nhánh `feat/finance-prepick-cancel`. Port 2 màn `Yêu cầu hủy hàng giữ` + `Phiếu hủy hàng giữ` sang
  Tài chính / nhóm Giữ hàng — **màn đầu tiên của HRM ghi tồn kho thật** (duyệt = trừ FIFO
  `prepick_details` + ghi `prepick_logs`). 2 migration (2 bảng lịch sử).
  Bước tiếp: user bấm tay trên dev + test bằng tài khoản `Quản lý giữ hàng` không phải Super admin;
  giữ 6 bảng `bak_*_20260815` tới lúc đó.
  Chi tiết + gotcha: plan.md

- finance-product-import-direct-transfer → @junfoke → .plans/gop-db/finance-product-import-direct-transfer/plan.md
  Trạng thái: **XONG PHASE 0-9** (2026-08-21) — Phase 8 vá 9 bug QA redmine 11092-11108, Phase 9 bỏ tab preset.
  Port màn "Phiếu chuyển hàng nhập thẳng" sang Tài chính / nhóm Điều chuyển; 1 migration (bảng lịch sử).
  Bước tiếp: user so cạnh nhau 2 cổng trên dev + test bằng tài khoản Kế toán kho không phải Super admin.
  Chi tiết + gotcha: plan.md

- finance-product-import-request → @junfoke → .plans/gop-db/finance-product-import-request/plan.md
  Trạng thái: **XONG PHASE 1-15** (2026-08-21) — gồm 16 bug tester redmine 11074-11089, các đợt phản hồi bổ sung,
  Phase 15 bỏ tab preset + 2 nút mở sang ERP (màn Kho chưa port).
  Port màn "Phiếu Yêu cầu nhập hàng" sang Tài chính; 8 loại phiếu + 4 luồng duyệt, 0 migration.
  Còn nợ: `V2Footer` dùng chung vẫn để nút In xanh + chữ "Không duyệt" (lệch chuẩn, ảnh hưởng mọi màn).
  Bước tiếp: user review trên dev rồi đóng 16 issue Redmine.
  Chi tiết + gotcha: plan.md

- history-action-groups → @dnsnamdang → .plans/gop-db/history-action-groups/plan.md
  Trạng thái: **CODE DONE + ĐÃ TEST (2026-08-15)**. Chuẩn hoá bộ lọc "Loại hoạt động" của khối/popup
  Lịch sử về **đúng 3 nhóm cố định dùng chung cho cả 10 màn**: `create` Tạo mới · `update` Thay đổi
  thông tin · `status` Thay đổi trạng thái. Trước đây mỗi entity tự khai danh mục riêng (KH 5 loại,
  task 3, phiếu bàn giao 8) + nhãn gắn tên đối tượng nên mỗi màn một dropdown.
  Mấu chốt: **nhóm chỉ dùng để LỌC, nhãn chi tiết từng dòng vẫn giữ trên timeline** → không màn nào
  mất khả năng lọc (7 hành động của Phiếu bàn giao đều là chuyển trạng thái → gom vào `status`).
  BE: `SystemLogService` thêm `ACTION_GROUP_LABELS`/`ACTION_GROUP_MAP`/`groupOfAction()`, `finalize()`
  gắn `action_group` cho mọi log, `getFilterOptions()` trả 3 nhóm cho mọi type.
  ⚠️ Bẫy đã tránh: mở cố định cả `performers` thì `performerOptions()` không lọc được công ty cho 9 loại
  còn lại → liệt kê **toàn bộ 783 nhân viên**; nên `performers` vẫn chỉ trả cho `customer`.
  FE: `SystemInfoSection.vue` + `CustomerHistoryModal.vue` lọc theo `action_group`, options hard-code 3 nhóm.
  Đã ghi vào tài sản chung: skill `entity-history` §0a + `CLAUDE.md` (nguyên tắc **bản ghi đã khoá thì
  không cho sửa/xoá — chặn ở BE bằng 423, FE chỉ ẩn nút**).
  Bước tiếp: user review. **Chưa port sang `tpe-develop-assign`** (nhánh đó cũng có khối Lịch sử) — chờ chốt.

- unsaved-changes-catalogs → @junfoke → .plans/gop-db/unsaved-changes-catalogs/plan.md
  Trạng thái: **CODE DONE, CHƯA TEST TRÌNH DUYỆT** (2026-08-12). Popup "Thông tin chưa lưu" khi thoát
  form — đợt 1: 14 màn danh mục CSKH + Tài chính, thêm 2 mixin mới, không sửa mixin cũ.
  Bước tiếp: ~147 form trang + ~180 modal của các phân hệ cũ (đợt 2/3).
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-12-filter-customization-design.md

- filter-customization → .plans/gop-db/filter-customization/plan.md
  Trạng thái: **CODE DONE Phase 1–3 — chờ chạy migration + user test** (2026-08-12, nhánh `gop_db`, cả 2 repo).
  Cho user tự chọn trường lọc hiển thị + **kéo thả sắp xếp vị trí** (popup "Cài đặt bộ lọc"), giống "Tuỳ chỉnh cột" nhưng cho bộ lọc; mặc định hiện đủ. UX tham chiếu demo kế toán `demo 3/assets/app.js` (`setupFilterSettings` chưa kéo thả + `setupColumnConfig` có kéo thả) → ghép 2 cái, lưu BE thay localStorage.
  Chốt: bảng mới **generic** `filter_customizations (created_by, table, config json)` unique(created_by, table) — KHÔNG copy schema cột-mỗi-màn của `column_customizations` (Entity đó 25 cột trong `$casts`, thêm màn là phải migration); khoá màn = tên bảng chính (`'customers'`); `config = [{key,isVisible}]`, thứ tự mảng = thứ tự hiển thị, không lưu label; bỏ tick = **ẩn hẳn + reset giá trị lọc** (tránh lọc ngầm); không có field locked; **component mới**, KHÔNG sửa `V2BaseFilterPanel`.
  BE (`gop_db-api`): migration + `FilterCustomization` (có khai `$table`) + Service + FormRequest + Controller + 2 route `human/filter-customizations`, không thêm quyền.
  FE (`gop_db-client`): `components/V2BaseSmartFilterPanel.vue` (schema field + slot escape hatch `#field-<key>` + `wrapperClass`/`hideLabel`/`resetKeys` cho field gom nhiều control) + `components/modal/filter-customization-modal.vue` (checkbox + vuedraggable). **Merge DB ↔ schema nằm trong component**: key mất khỏi FE → bỏ hẳn, key mới → append cuối và hiện ⇒ bổ sung trường lọc sau này không lỗi.
  Pilot: `pages/assign/customers/index.vue` — 15 field khai báo bằng `filterFields`, khối Công ty/PB/NV và CascadePairSelect đi qua slot. Class wrapper đổi `advanced-filters` → `smart-advanced-filters` để dropdown CascadePairSelect không bị cắt (rule scoped cũ ở page đã bỏ).
  Spec: docs/superpowers/specs/gop-db/2026-08-12-filter-customization-design.md
  Bước tiếp: chạy `php artisan migrate` (module Human) → build FE → user test popup Cài đặt bộ lọc trên `/assign/customers`.

- customer-list-empty-placeholder → .plans/gop-db/customer-list-empty-placeholder/plan.md
  Trạng thái: **CODE DONE — CHỜ USER TEST TRÌNH DUYỆT** (2026-08-12, nhánh `gop_db`, 2 file).
  Ô "không có dữ liệu" ở màn `/assign/customers` hiển thị không đồng nhất: mọi cột ra `—` (em dash),
  riêng **SĐT ra `-`** vì `CustomerListResource` tự chèn sẵn chuỗi `'-'` từ BE (cả khi trống lẫn khi
  bị che do không phải KH của mình) → FE nhận chuỗi khác rỗng nên `|| '—'` không chạy.
  Fix: BE trả `null`, placeholder do FE quyết định; popup chọn KH thêm slot fallback `#cell()`
  (7 cột trước đây để ô trắng, riêng SĐT ra `-`) → tất cả về `—`.
  Giữ nguyên `'-'` trong file xuất CSV/Excel (`CustomerExportFormatter::taxCodeOrMobile`) — theo mẫu ERP,
  ngữ cảnh file bàn giao khác màn hình. Không migration, không quyền mới.

- list-page-action-column → @junfoke → .plans/gop-db/list-page-action-column/plan.md
  Trạng thái: **CODE DONE — CHỜ USER VERIFY UI** (2026-08-12). Chuẩn hoá cột "Hành động" màn danh sách
  (mẫu `/assign/customers`) + component dùng chung `V2BaseRowActions.vue`.
  Chi tiết + gotcha: plan.md

- fix-employee-fk-remap → @junfoke → .plans/gop-db/fix-employee-fk-remap/plan.md
  Trạng thái: **CODE DONE, DRY PASS — CHƯA CHẠY THẬT** (2026-08-04). Vá 42 cột / 20.231 dòng FK
  `employees` bị `ReconcileEmployeesSeeder` bỏ sót khi gộp DB (trỏ SAI NGƯỜI, hỏng im lặng).
  ⚠️ TUYỆT ĐỐI không chạy lại `ReconcileEmployeesSeeder` trên DB đã gộp khi `hrm_employees` còn tồn tại
  (164 id vừa là id HRM cũ của người này vừa là id ERP mới của người khác).
  Bước tiếp: user backup DB → chạy `GOP_DB_APPLY=1` cho `FixMissedEmployeeFkSeeder`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-04-fix-employee-fk-remap-design.md | Tóm tắt: .plans/gop-db/fix-employee-fk-remap/design.md

- customer-cut-mysql2 → .plans/gop-db/customer-cut-mysql2/plan.md
  Trạng thái: **HOÀN TẤT + ĐÃ TEST** (2026-08-01, nhánh `gop_db`). Khách hàng còn ĐÚNG 1 luồng `/assign/customers`.
  Gồm: cắt hết `mysql2` khỏi luồng KH (35 file) · xoá 6 bảng `hrm_customer_*` + migration `2026_08_01_000001_drop_hrm_customer_tables` (đã test round-trip) ·
  gỡ toàn bộ tầng sync 2 chiều · xoá màn `/human/customers` + `/timesheet/setting/customers` · chuyển 10 picker sang luồng mới · thêm `GET assign/customers/search`.
  Test: 52/52 endpoint HTTP + 12 màn browser + luồng ghi (tạo/sửa/thêm liên hệ, có rollback). **7 lỗi thật đã sửa** (xem plan.md Phase 11-12).
  ⚠️ Đọc trước khi làm tiếp trên nhánh này: `.plans/gop-db/design.md`.

## Hoàn thành

- finance — sửa nhanh 3 màn Phiếu thu / Phiếu chi / Ủy nhiệm chi → @khoipv →
  `.plans/gop-db/finance-bill-income/plan.md` · `.plans/gop-db/finance-bill-payment/plan.md` ·
  `.plans/gop-db/finance-bill-payment-authorization/plan.md`
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-28). Commit `gop_db`: client `5e4d559` · api `d00a4c0`.
  Icon nút Duyệt 2 màn danh sách về `ri-checkbox-circle-line` · Ủy nhiệm chi: mặc định Loại chi
  "Chi trả nhà cung cấp", Lưu nháp chỉ bắt buộc Loại chi (nới RULING U-UNC-3) · Phiếu thu: bỏ popup
  duyệt, "Số tiền thực thu" vào bảng chi tiết màn xem, duyệt không ghi đè `sum_money` (hết lệch cột
  "Số tiền" so ERP, không nắn dữ liệu cũ) · Phiếu chi màn Tạo bám lại ERP: Số phiếu đề nghị lên đầu,
  xếp lại 10 trường, Loại chi 5 → 7, thêm 3 khối chỉ đọc (Đối tượng nhận tiền / Tài khoản nhận tiền /
  Ngân hàng trung gian). Không migration. Màn Đề nghị thanh toán: user chốt KHÔNG sửa.

- finance-bill-payment-request → @khoipv → .plans/gop-db/finance-bill-payment-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-26).
  Phase 11 sửa xuất Excel loại chi 12: `paidMoneyForDetail()` chọn `billable_type` theo dòng
  (hết lệch 254 ô / 70 phiếu; ăn sang màn chi tiết + màn in — 3 đầu ra 1 số) · ô tiền ghi **CHUỖI**
  kiểu VN qua `WithCustomValueBinder` (user chốt, đánh đổi: mất SUM/lọc/pivot) · letterhead nhúng
  `companies.header` theo `company_id` của phiếu + trải hết bề rộng bảng.
  BE 3 file + 1 blade · không migration · không đụng FE.
  📄 Bộ tài liệu bàn giao (Phase 15 — 2026-08-28): `testcase - Phiếu đề nghị thanh toán.xlsx`
  (191 TC) · `HDSD_Phiếu đề nghị thanh toán.docx` (54 trang, 30 ảnh thật) ·
  `SRS - Phiếu đề nghị thanh toán.docx` (67 trang, FR-01…FR-15, BR-01…BR-18).
  3 generator kèm theo; ảnh nguồn `dntt_chi_shots/` chỉ để local, không commit.

- finance-addition-accounting-request → @khoipv → .plans/gop-db/finance-addition-accounting-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-26).
  Port màn ERP "Phiếu yêu cầu hạch toán bổ sung" sang phân hệ Tài chính, route
  `/finance/addition-accounting-requests` — 6 loại tạo mới + loại 7 chỉ xem/in, dừng ở *Chờ duyệt*.
  BE 17 file mới · FE 10 file mới · 24 route · 4 quyền id **1177–1180** · **0 migration** (dùng chung
  5 bảng ERP). Vá **10 lỗi/lỗ hổng của ERP** (nặng nhất: route xoá là **GET** không gate ·
  `store()` gán thẳng `status`) + 7 lỗi FE chỉ Playwright bắt được.
  Spec: docs/superpowers/specs/gop-db/2026-08-25-finance-addition-accounting-request-design.md

- finance-bill-income-request → @khoipv → .plans/gop-db/finance-bill-income-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-26).
  Port màn ERP "Phiếu đề nghị thu tiền" (7 phase, xong 2026-08-14) + 6 đợt sửa sau nghiệm thu:
  cấu hình cột hiển thị + 2 cột Người/Ngày cập nhật · bỏ hẳn "Người nộp" (cột · ô lọc · bản in),
  đổi nhãn "Lý do nộp" → "Lý do thu" · popup Chọn khách hàng: SĐT khớp từ **đầu số**, ẩn dòng bị che
  SĐT (`hide_masked_mobile`), ô MST và ô SĐT lọc **độc lập** (`tax_code_only`, MST khớp đầu mã).
  ⚠️ Đánh đổi user đã chốt: gõ mảnh giữa/đuôi SĐT-MST **không ra kết quả** — phải gõ đủ số.
  Spec: docs/superpowers/specs/gop-db/2026-08-13-finance-bill-income-request-design.md
  📄 Bộ tài liệu bàn giao (Phase 14 — 2026-08-28): `testcase - Phiếu đề nghị thu tiền.xlsx`
  (156 TC) · `HDSD_Phiếu đề nghị thu tiền.docx` (40 trang, 25 ảnh thật) ·
  `SRS - Phiếu đề nghị thu tiền.docx` (50 trang, FR-01…FR-12, BR-01…BR-17).
  3 generator kèm theo; ảnh nguồn `dntt_shots/` chỉ để local, không commit.

- finance-bill-adjust-dept-request → @khoipv → .plans/gop-db/finance-bill-adjust-dept-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-24). Cả 18 phase đã
  nghiệm thu xong. Phase 18: màn tạo/sửa `finance/bill-adjust-dept-requests/create` khi bấm **Lưu nháp**
  chỉ bắt buộc **Loại phiếu**; Diễn giải / bảng chi tiết / tỷ giá / khách hàng chỉ bắt khi **Gửi duyệt**.
  15 phase gốc + Phase 16 sửa
  6 điểm màn danh sách sau nghiệm thu (Tùy chỉnh cột · 2 cột Ngày/Người cập nhật · 3 cột ngày
  `dd/mm/yyyy HH:mm` · mở sort Mã phiếu + 3 cột ngày · đổi nhãn Ngày tạo/Người tạo · nút Excel xanh lá)
  + Phase 17 viết lại `_id/print.vue` bám nguyên mẫu ERP (report_template 209, khổ 297mm, Times New Roman,
  6 ô chữ ký; bù `pdf.css` trong `options.styles` vì `hrm-client/static/css/` không có).
  BE 3 file + 1 blade · FE 2 file · không migration.
  📌 Còn nợ: file Excel phiếu vẫn lệch ERP (chờ user chốt có đồng bộ không) · nút "Chọn nhanh hợp đồng" ·
  SRS/testcase/HDSD · dọn 6 phiếu `TEST.DNDCCN.*`.
  Spec: docs/superpowers/specs/gop-db/2026-08-17-finance-bill-adjust-dept-request-design.md | Tóm tắt: .plans/gop-db/finance-bill-adjust-dept-request/design.md

- finance-bill-income-report (Phiếu báo có ERP → HRM) → @khoipv → .plans/gop-db/finance-bill-income-report/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-24).
  Mục tiêu: port `admin/income-expenditure/bill_income_report` sang HRM phân hệ Tài chính,
  route `/finance/bill-income-reports` + `/summarize-money`.
  Phạm vi: danh sách · tạo/sửa/xóa nháp · duyệt **kèm ghi bút toán sổ cái** · chi tiết + cờ "Không báo
  tiền về" · 3 loại thu · Tổng hợp tiền về ngân hàng + xuất Excel chọn trường · Import Excel sao kê ·
  Lịch sử thay đổi. **KHÔNG có thay đổi schema** (lịch sử dùng bảng chung `catalog_histories`).
  Điểm đáng chú ý: bút toán do HRM sinh **khớp 100%** với bút toán ERP đã ghi (7 phiếu thật / 38 bút
  toán / 24 cột denormalize). 3 quyền mới id 1539-1541 (guard `api`, tên trùng ERP).
  Spec: `docs/superpowers/specs/gop-db/2026-08-24-finance-bill-income-report-design.md`.

- finance-3-man-sua-theo-phan-hoi (2026-08-22) → @khoipv → **HOÀN THÀNH — user xác nhận xong**.
  Plan: `finance-bill-income-request` (8.8-8.11) · `finance-bill-income` (K, L, M) ·
  `finance-bill-payment-request` (5 task phụ) — sửa theo phản hồi trên 3 màn đã nghiệm thu.
  **Lịch sử thay đổi** cho Đề nghị thu tiền + Đề nghị thanh toán (popup ⋮ + khối Lịch sử, ghi vào
  `catalog_histories`, không migration/permission mới); mở rộng `CatalogHistoryService` hỗ trợ khoá
  dạng BẢNG (diff `~ / - / +`) — thuần thêm, đã test hồi quy màn danh mục cũ.
  **Đề nghị thu tiền:** cột + ô lọc Người nộp, dòng Tổng cộng, mở 2 tab trả **409** thay vì báo thiếu
  quyền, bỏ nút Xem chi tiết. **Phiếu thu:** in/Excel lấy `bill_incomes.payer`, preview khớp bản in,
  mã phiếu đề nghị mở tab mới. **Đề nghị thanh toán:** Lưu nháp bỏ bắt buộc chi tiết/file/ngân hàng,
  loại chi 6+CK tự đổ ngân hàng người lập, loại chi 6 port nguồn hợp đồng `bonus-contracts`.
  Đụng 7 file `hrm-api` + 7 file `hrm-client`. Bước tiếp: commit lên `gop_db` (lúc nghiệm thu chưa commit).

- finance-bill-payment (Phiếu chi — logo bản in) → @khoipv → .plans/gop-db/finance-bill-payment/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21).
  Áp cùng cách xử lý logo như Phiếu thu (dùng nguyên `companies.header`, lấy công ty theo
  `bill_payments.company_id`) → 162/1.305 phiếu hết in nhầm logo công ty khác.
  Sửa 1 file `BillPaymentPrintService.php`; `BillPaymentExport` đã có sẵn trait letterhead.

- finance-bill-income (Phiếu thu — logo bản in/Excel) → @khoipv → .plans/gop-db/finance-bill-income/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21). Xong code + data local.
  Logo bản in/Excel phiếu thu chuyển sang dùng chung cách của màn Báo giá (dùng nguyên
  `companies.header`, chỉ ghép `ERP_URL` khi giá trị còn tương đối) và lấy công ty theo
  `bill_incomes.company_id` thay vì công ty người tạo → 133 phiếu `TPSG.*` hết mất logo,
  497 phiếu về đúng logo công ty trên phiếu. Sửa 1 file `BillIncomePrintService.php`.
  **Chuẩn hoá dữ liệu dùng chung**: 8 dòng `companies.header` + 8 dòng `companies.logo` trên
  `gop_db` local đổi từ `/uploads/...` sang `https://erp.eteksofts.com/uploads/...` — vì file ảnh
  nằm trên đĩa ERP, gộp DB không kéo file sang, mà domain HRM không phục vụ `/uploads` (404).
  Hưởng lợi cả màn Báo giá (đang mất logo trên `gop_db` vì lý do y hệt).
  ⚠️ **Dev/production chưa chạy 2 câu UPDATE** — rollback ở
  `.plans/gop-db/finance-bill-income/rollback-companies-header-logo.sql`.

- customer-permission-to-master-data → @khoipv → .plans/gop-db/customer-permission-to-master-data/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21). Chuyển nhóm quyền khách hàng sang
  phân hệ **Danh mục chung** (11 quyền id 1517-1526 + giữ 167), chỉ sửa `PermissionsTableSeeder.php`.
  ⚠️ Seeder vẫn còn lỗi trùng id 1117/1118 (dòng ~1130) → phải bỏ 1 cặp mới seed được trên DB sạch.

- finance-bill-income + finance-bill-payment (xuất Excel) → @khoipv → .plans/gop-db/finance-bill-income/plan.md (F1-F5) · .plans/gop-db/finance-bill-payment/plan.md (G1-G6)
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21). Vá 3 lỗi file Excel (thiếu logo,
  cột hẹp, "number formatted as text") cho Phiếu thu + Phiếu chi, cả 3 bố cục 1/4/12: số thô +
  `data-format="#,##0"`, `WithColumnWidths`, trait `EmbedsCompanyLetterhead`.
  Quy tắc gói thành skill `.claude/skills/export-excel/SKILL.md` — **tài sản chung, cần PR**.

- finance-bill-payment-authorization → @khoipv → .plans/gop-db/finance-bill-payment-authorization/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận xong** (2026-08-21). Port màn **Phiếu ủy nhiệm chi**
  (`/finance/bill-payment-authorizations`) — cặp song sinh chuyển khoản của Phiếu chi.
  BE 11 file mới + 3 sửa · FE 6 mới + 1 sửa menu · 2 quyền api 1515-1516 · không migration.
  Test Playwright 25/25 · replay sổ cái 62/63 · dọn dữ liệu test 8/8 chỉ số về baseline.
  🚨 **6 ruling cố ý giữ điểm hở (U-UNC-1…6)** — đọc §8 spec trước khi "sửa lỗi", nặng nhất là
  U-UNC-1 giữ nguyên lỗi cộng dồn của ERP (bút toán Có = tiền DÒNG CUỐI, lệch 111,3 tỷ / 433 phiếu).
  ⚠️ Có sửa file dùng chung `PaymentEmployeeTable.vue` (thêm prop `excludeFields`) và vá lỗi 403
  chọn đề nghị cho cả Phiếu chi lẫn Phiếu thu (2 endpoint mới gate bằng `isAccountant()`).
  📌 Còn lại: nhánh loại 4 + bảng phân bổ phiếu xuất hàng chưa có dữ liệu thật · SRS/testcase/HDSD.
  Spec: docs/superpowers/specs/gop-db/2026-08-20-finance-bill-payment-authorization-design.md | Tóm tắt: .plans/gop-db/finance-bill-payment-authorization/design.md

- finance-bill-payment → @khoipv → .plans/gop-db/finance-bill-payment/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Port màn ERP
  `admin/income-expenditure/bill_payments` (Phiếu chi tiền) sang HRM phân hệ Tài chính, 23/23 task,
  đủ 5 loại chi: nhánh A (1/2/6/12) lập từ đề nghị duyệt 1 cấp · nhánh B (loại 4 Chi thu nhập nhân viên)
  lập trực tiếp, duyệt 2 cấp KT trưởng → Thủ quỹ, ghi sổ cái gộp theo `identify_number`.
  1 màn danh sách duy nhất, in 2 liên 3 mẫu ERP, xuất Excel, chuông.
  BE 21 file mới + 7 sửa · FE 9 mới + 2 sửa · 18/18 unit test PASS · không migration.
  Sổ cái diff từng trường với ERP: nhánh A khớp 20/20 phiếu, nhánh B 5/5.
  📌 Còn treo: 5 điểm chờ user quyết + 1 lỗi feature CŨ (Phiếu thu in "đồng đồng",
  `BillIncomePrintService:155`) — xem design.md.
  Spec: docs/superpowers/specs/gop-db/2026-08-19-finance-bill-payment-design.md | Tóm tắt: .plans/gop-db/finance-bill-payment/design.md

- cut-erp-sync → @khoipv → .plans/gop-db/cut-erp-sync/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Dọn phần đồng bộ HRM → ERP
  trong module Nhân sự sau khi gộp DB (các khối `use_erp` ghi lại chính bảng vừa ghi, có nguy cơ đè
  nhầm tài khoản). Gỡ 5 khối `boot()` · sync password/status ở `EmployeeService` · `setConnection('mysql2')`
  ở 2 model · 6 lệnh `Config::set(database.default)` ở `AuthController` · 2 job sync → no-op.
  Giữ có chủ đích `Group`↔`TpGroup`, nhánh `use_crm`, các chỗ `use_erp` chỉ đọc.
  Diff 13 file, -557/+105 · không migration · không đụng FE.
  📌 Bug tiềm ẩn CHƯA sửa: `Group::boot()` gọi `TpGroup::find($model->code)` → có thể thêm dòng thừa
  vào `department_groups`.
  Spec: docs/superpowers/specs/gop-db/2026-08-19-cut-erp-sync-design.md | Tóm tắt: .plans/gop-db/cut-erp-sync/design.md

- employee-create-bank-null → @khoipv → .plans/gop-db/employee-create-bank-null/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Fix lỗi 500
  `Creating default object from empty value` khi tạo mới nhân viên có nhập tài khoản ngân hàng
  (`EmployeeInfoService.php:1317`) — `TpEmployeeInfo` chạy connection `mysql2` nằm ngoài transaction
  nên không đọc được dòng `employee_infos` vừa INSERT. Sửa 3 file BE, không migration, không đụng FE.
  📌 Nợ kỹ thuật cố ý: nhánh `use_erp` / model `Tp*` vẫn đọc-ghi qua connection thừa (đã xử ở cut-erp-sync).
  Spec: docs/superpowers/specs/gop-db/2026-08-19-employee-create-bank-null-design.md | Tóm tắt: .plans/gop-db/employee-create-bank-null/design.md

- finance-bill-income → @khoipv → .plans/gop-db/finance-bill-income/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Port màn ERP
  `admin/income-expenditure/bill_incomes` (Phiếu thu tiền) sang HRM phân hệ Tài chính, 18/18 task:
  BE đầy đủ (entity, quyền, lọc, CRUD, dựng + ghi bút toán sổ cái, duyệt/hủy, in 2 liên, Excel);
  FE 1 màn danh sách gộp 4 chế độ (bỏ `?mode=`) + form + chi tiết + trang in + menu.
  Task 17 đối chiếu ngược ERP: 11/11 cột · 10/10 ô lọc, sửa 2 lệch (thiếu nút Sửa/Xóa ở chi tiết,
  danh sách chưa dùng mixin CheckPermission). Verify: phpunit 36 tests OK · php -l sạch · parse 8/8 Vue ·
  baseline DB khớp tuyệt đối.
  📌 Ruling U4 (user chốt 2026-08-19): đồng bộ ngược trạng thái sang Phiếu đề nghị thu tiền GIỮ NGUYÊN
  LOGIC ERP — 3 điểm hở (xóa không trả trạng thái · hủy là ngõ cụt · lưu nháp không đổi trạng thái)
  KHÔNG phải bug, đừng sửa ở lượt review sau.
  📌 Còn lại: 1 lượt review tổng toàn nhánh + phân loại ~45 minor đã park · chưa kiểm chứng 2 nhánh phân bổ
  (DB 0 dòng) và in phiếu loại thu 3 · 4 file sửa ở Task 17 chưa commit.
  Spec: docs/superpowers/specs/gop-db/2026-08-18-finance-bill-income-design.md

- customer-export-file (Phase 7) → @khoipv → .plans/gop-db/customer-export-file/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-20). Chuyển việc dựng file
  CSV/Excel/PDF của `/assign/customers` từ BE sang build ở FE: BE thêm `GET assign/customers/export-rows`
  (JSON theo trang, 2.000 dòng/lượt ~0,85s, RAM 60MB) · FE thêm `utils/export/customerExportFile.js`
  (ExcelJS + jsPDF/autoTable + font DejaVu subset 78KB, import động).
  ⚠️ Team phải `npm install` sau khi kéo nhánh (thêm `jspdf` + `jspdf-autotable`).
  📌 3 endpoint export cũ của BE vẫn giữ nguyên, chưa xoá.


- finance-bill-payment-request → @khoipv → .plans/gop-db/finance-bill-payment-request/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-18). Đã commit:
  `hrm-api` `decc26df7` · `hrm-client` `ba4518877` (đợt sửa UI danh sách 2026-08-18);
  port gốc xong 2026-08-15, commit `hrm-api` `6eed9d2a6` · `hrm-client` `8c0ffb424`.
  Port màn ERP "Phiếu đề nghị thanh toán" → `/finance/bill-payment-requests` (phân hệ Tài chính),
  **duyệt 5 cấp**, 4 loại chi. 8 phase / 29 task · 17 route BE · 12 file FE · 9 quyền id 1153–1161 ·
  dùng chung bảng ERP `bill_payment_requests`. Đợt sửa UI gồm 6 việc màn danh sách (bỏ nút Xem chi tiết ·
  popup Cấu hình cột · 2 cột Người/Ngày cập nhật · chuẩn hoá 3 cột ngày · đổi tiêu đề cột KH/NCC ·
  sửa sắp xếp cột) — chi tiết + số liệu đo ở Checkpoint cuối `plan.md`.
  ⚠️ Có sửa component dùng chung `components/V2BaseSelectRemote.vue` (18 màn) — chỉ Việt hoá chữ
  Select2, không đổi hành vi (user chốt 2026-08-18).
  ⚠️ DB local còn dữ liệu test: `employee_manage_departments` id 368 · `departments.id = 111` ·
  8 phiếu `TEST.DNTT-CHI.*` (seeder có câu lệnh dọn).
  📌 Chưa làm: SRS / testcase / HDSD · chưa đối chiếu trực tiếp giao diện ERP.
  📌 Nợ ghi sổ (KHÔNG tự làm): `bill_payment_request_details` thiếu index `bill_payment_request_id`
  — bảng dùng chung ERP+HRM, muốn thêm phải hỏi user.
  🔧 **Đang sửa tiếp (2026-08-24)**: bổ sung cột **"Số tiền chi"** cho bảng chi tiết màn xem (thiếu
  từ đợt port — Task 7.1 Bước 2 có ghi nhưng chưa làm). BE đọc `payment_money_approve` sang uỷ nhiệm
  chi / phiếu chi gắn với phiếu. Code xong, **chờ user test trình duyệt, chưa commit**.
  Đã làm luôn cho **màn IN + file Excel** (đối chiếu ERP: cả 2 đầu ra bên đó đều có cột này);
  tiêu đề cột Excel đổi `Số tiền duyệt` → `Số tiền chi` cho khớp ERP.
  🔧 **Đang sửa tiếp (2026-08-24, đợt 2)**: bug user báo — màn tạo mới, **loại chi 12** (CP vận chuyển
  NCC) chọn NCC **nước ngoài** (`customer_type = 3`, ca `KORSOL`) thì khối ngân hàng trắng trơn và
  **không gửi duyệt được**. Nguyên nhân ở **nguồn dữ liệu**: `party-banks` chỉ đọc
  `customer_has_bank_accounts` + cột cũ trên `customers`, còn tài khoản NCC nước ngoài nằm ở
  **`supplier_banks`** — bảng này chỉ nhánh hiển thị "NCC nước ngoài" (loại chi 1) mới dùng. ERP dính y hệt.
  **User chốt giữ nguyên giao diện cũ** (khối trong nước 5 ô), chỉ sửa BE: `partyBanks()` thêm nguồn
  dự phòng `supplier_banks` khi 2 nguồn kia rỗng (map cả danh sách → NCC nhiều tài khoản vẫn có
  dropdown chọn), `StoreRequest` nới đúng 3 ô Chi nhánh/Tỉnh-TP mà bảng đó không có.
  BE 2 file · FE 0 thay đổi hành vi · không migration. Code xong, **chờ user test trình duyệt, chưa commit**.
  📌 Nợ ghi sổ (cần user quyết): bản in loại 12 + NCC nước ngoài thừa 3 dòng Phí/IBAN/Swift toàn `—` ·
  mở lại phiếu NCC nước ngoài loại 1 ở màn xem/sửa bị mất khối ngân hàng (lỗi có sẵn).
  🔧 **Đang sửa tiếp (2026-08-24, đợt 3)** — XUẤT EXCEL + MÀN IN, 3 việc:
  · **Yêu cầu user:** cột "Số tiền chi" chỉ in khi phiếu ở trạng thái **Duyệt phiếu chi** (status 8);
    dòng Tổng cộng **gộp** các cột mô tả đầu bảng (STT + [chuyến xe] + [NCC] + [hợp đồng]) thành 1 ô.
  · **Bug user báo:** cột "Nhà cung cấp" trống trên Excel/bản in phiếu 4197. Gốc: FE lưu phiếu chỉ gửi
    `supplier_id`, KHÔNG gửi `*_code`/`*_name` (`BillPaymentRequestForm.vue` :1436) → snapshot dòng chi
    tiết luôn NULL với phiếu tạo từ HRM (1/1593 dòng, phần còn lại là dữ liệu port từ ERP).
    Màn danh sách + màn chi tiết đã có fallback sẵn, chỉ nhánh in/Excel thì không → đã thêm fallback
    sang quan hệ trong `detailObjectName()` + `objectName()`.
  · **Bám lại cấu trúc ERP** (user chốt qua 4 câu hỏi): tiêu đề bảng **2 dòng** (ô đơn vị tiền ở dòng
    dưới) · phiếu **ngoại tệ dùng bảng riêng** của ERP (2 cặp nguyên tệ/VND, bỏ 3 cột duyệt theo cấp,
    lấy cấp duyệt cao nhất > 0) · đổi nhãn `KT trưởng/BGD` + `Số hợp đồng nhập mua` / `Số đơn hàng/Hợp đồng` ·
    **bỏ cột Khách hàng/Nhân viên** (3 nhánh `type_*_cash()` của ERP xét khoá không tồn tại → luôn false,
    là code chết) · thêm dòng "Nhà cung cấp:" đầu phiếu cho loại 12 và loại 1 + HĐ + CK ·
    định dạng số `#,##0.##` khớp `formatCurrency($n, 2)`, riêng 2 cột quy đổi VND dùng `#,##0`.
  Toàn bộ cờ bố cục gom vào `BillPaymentRequestPrintResource::columns` làm nguồn duy nhất cho cả FE lẫn Excel.
  BE 3 file (`PrintResource`, `Service`, blade export) + `BillPaymentRequestExport` · FE 1 file (`_id/print.vue`) ·
  không migration. Verify: đối chiếu bộ cột FE↔BE trên **15 phiếu** đủ loại 1/2/6/12 × TM/CK × VND/RUPEE/IDR
  × 7 trạng thái — **lệch 0**; dựng file .xlsx thật đọc lại bằng PhpSpreadsheet (merge tiêu đề, dòng đơn vị,
  kiểu ô số đều đúng). Code xong, **chờ user test trình duyệt, chưa commit**.
  📌 Nợ ghi sổ đợt 3 (cần user quyết): (1) snapshot `*_code`/`*_name` dòng chi tiết vẫn không được ghi khi
  lưu phiếu → phiếu không giữ tên đối tượng tại thời điểm lập, nên vá ở BE; (2) loại chi 6 có 0/537 dòng
  gắn `employee_id` (đối tượng ở cấp phiếu); (3) nhánh loại 1 không hợp đồng + loại chi 3 chưa test được
  (DB 0 dòng); (4) khối 5 chữ ký vẫn chiếm cứng 10 cột, chưa rải `colspan` theo số cột bảng.
  Spec: docs/superpowers/specs/gop-db/2026-08-14-finance-bill-payment-request-design.md | Tóm tắt: .plans/gop-db/finance-bill-payment-request/design.md

- form-validate-base → @khoipv → .plans/gop-db/form-validate-base/plan.md
  Trạng thái: **HOÀN THÀNH — user test đủ 23/23 màn** (2026-08-14).
  Gắn được `v-validate` thẳng lên `V2Base*` → lỗi hiện realtime. 2 mixin mới (`v2ValidateMixin`,
  `formValidateMixin`), 7 component base, 7 rule mới ở `plugins/vee-validate.js` (thuần thêm).
  Theo skill `form-validate`: FE chỉ `required` ô **Tên**, còn lại BE trả 422; **message BE chuẩn hoá
  đúng bằng câu FE nói** (14 FormRequest).
  Còn lại (không chặn): PR cập nhật `.claude/skills/form-validate/SKILL.md` (bỏ `data-vv-value-path`).
  Spec: docs/superpowers/specs/gop-db/2026-08-14-form-validate-base-design.md | Tóm tắt: .plans/gop-db/form-validate-base/design.md

- device-errors-load-data → @khoipv → .plans/gop-db/device-errors-load-data/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-13). Màn `customer-care/device-errors` hiện
  "không có dữ liệu" oan do `loading` khởi tạo `false` và 2 API dropdown chạy tuần tự trước `loadData()`.
  Sửa 1 file FE, không đụng BE.
  Spec: docs/superpowers/specs/gop-db/2026-08-13-device-errors-load-data-design.md

- pagination-100-rows → @khoipv → .plans/gop-db/pagination-100-rows/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-13). Thêm option **100** dòng/trang: sửa đúng
  1 chỗ — default `pageSizeOptions` của `components/V2BaseDataTable.vue` (user chốt sửa thẳng component
  dùng chung, 93 file cùng ăn). BE không phải sửa.
  ⚠️ Muốn thêm `200`/`500` sau này phải sửa BE trước — 3 chỗ cap `min(100, …)` sẽ âm thầm ghim lại 100.
  📌 Repo có **2 component phân trang song song** default lệch nhau (`V2BaseDataTable` vs `V2BasePagination`).
  Spec: docs/superpowers/specs/gop-db/2026-08-13-pagination-100-rows-design.md

- customer-date-no-future → @khoipv → .plans/gop-db/customer-date-no-future/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-13). Chặn ngày tương lai ở 3 ô ngày màn KH,
  **2 lớp** (FE `:disabled-date` + BE `before_or_equal:today`) vì `V2BaseDatePicker` cho gõ tay.
  📌 Không phải sửa component dùng chung — `disabledDate` đã có sẵn prop. Sửa 1 chỗ `CustomerForm.vue`
  → 5 màn cùng ăn. KH đang có ngày tương lai vẫn hiện, chỉ chặn từ lần sửa sau.
  Spec: docs/superpowers/specs/gop-db/2026-08-13-customer-date-no-future-design.md

- chuyen-menu-nhom-giai-phap → @khoipv → .plans/gop-db/chuyen-menu-nhom-giai-phap/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận** (2026-08-12). Đưa **Nhóm giải pháp** + **Ứng dụng** từ
  Bán hàng sang **Danh mục dùng chung** (chỉ menu, 3 file `subsystem-menu/*`).
  📌 Lần sau **không đề xuất tách** `/assign/customer-scope-groups` lên cấp 1 — đã thử, user đổi ý, đã hoàn tác.
  ⚠️ Nợ chung với đợt Nhóm ngành: 4 quyền vẫn `group = 'Danh mục'` nên màn Phân quyền vẫn xếp ở tab Giao việc.
  Spec: docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-giai-phap-design.md

- chuyen-menu-nhom-nganh → @khoipv → .plans/gop-db/chuyen-menu-nhom-nganh/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-12). Đưa **Nhóm ngành** từ Bán hàng sang
  **Danh mục dùng chung** (chỉ menu, 3 file).
  ⚠️ KHÔNG đổi `type` quyền 983/998: `Permission.vue` gom khối chỉ theo `group`, đổi sẽ kéo nhầm cả
  29 quyền Giao việc.
  📌 Bẫy khi test: tài khoản dev đang đăng nhập có **0 quyền** → mọi màn gated bị đẩy về 404.
  Spec: docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-nganh-design.md

- customer-history → @khoipv → .plans/gop-db/customer-history/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-12). Lịch sử thay đổi KH ở cả màn danh sách
  (modal) và chi tiết (`SystemInfoSection`), dùng lại base của báo giá: bảng `customer_history` +
  endpoint chung `GET /assign/system-logs/{type}/{id}`. Không permission riêng.
  🐛 Phát hiện khi test, CHƯA sửa gốc: `CustomerForm.buildPayload()` gửi cố định `district_id: null`
  ⇒ **mỗi lần lưu KH cũ là xoá Quận/Huyện trong DB** (mới chỉ ẩn khỏi log qua `CUSTOMER_HIDDEN_FIELDS`).
  Spec: docs/superpowers/specs/gop-db/2026-08-11-customer-history-design.md

- customer-lock → @khoipv → .plans/gop-db/customer-lock/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-12). Khóa/Mở khóa KH (`status` 0/1), gate bằng
  quyền ERP `Xóa khách hàng`, không thêm permission/migration. 2 route POST (ERP dùng GET).
  📌 Popup chọn KH dùng chung đã lọc `status: 1` sẵn; các ô LỌC vẫn hiện KH khóa (user chốt).
  Spec: docs/superpowers/specs/gop-db/2026-08-11-customer-lock-design.md

- customer-care-service-price-config → @junfoke → .plans/gop-db/customer-care-service-price-config/plan.md
  Trạng thái: **HOÀN THÀNH — user test trình duyệt xong** (2026-08-12), nhánh `gop_db`.
  Chuyển "Cập nhật nhanh giá dịch vụ" từ ERP sang CSKH — màn danh mục thứ 6 của phân hệ.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-06-customer-care-service-price-config-design.md | Tóm tắt: .plans/gop-db/customer-care-service-price-config/design.md

- customer-column-config → @khoipv → .plans/gop-db/customer-column-config/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-11). Cấu hình cột hiển thị cho
  `/assign/customers` (18 cột, lưu DB qua `column-customizations`), khoá STT + Mã-Tên bằng cách không
  truyền vào modal dùng chung.
  ⚠️ 4 cột cần 5 leftJoin làm COUNT chậm 3,7 lần → gate sau cờ `with_extra_columns`.
  ⚠️ Modal chung dùng `:value="column.key"` ⇒ cột hiện mặc định PHẢI khai `isVisible: '<đúng key>'`.
  📌 Ghi nhận không sửa: `ColumnCustomizationService` nhét thẳng `$request->table` vào tên cột SQL.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-column-config-design.md

- customer-form-group → @khoipv → .plans/gop-db/customer-form-group/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-11). Thêm trường **Nhóm khách hàng** vào
  `CustomerForm.vue` (5 màn cùng ăn) + nối dữ liệu thật cho cột "Nhóm KH" ở danh sách.
  🐛 Sửa kèm lỗi MẤT DỮ LIỆU có sẵn: `syncGroups()` xoá-rồi-ghi vô điều kiện trong khi form chưa bao
  giờ gửi `groups` ⇒ mỗi lần sửa KH trên HRM là xoá sạch nhóm do ERP gán.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-form-group-design.md

- customer-export-file → @khoipv → .plans/gop-db/customer-export-file/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-11). 3 nút Xuất CSV / Excel / PDF cho
  `/assign/customers`, dùng quyền ERP có sẵn. Sửa 3 lỗi của bản ERP (thiếu header, CSV không BOM,
  mất số 0 đầu). 17.542 KH: CSV ~13s · XLSX ~44s (mẫu chuẩn HRM), RAM đỉnh 266 MB.
  ⚠️ Team phải `composer install` sau khi kéo nhánh (thêm `barryvdh/laravel-dompdf ^1.0`).
  ⚠️ **CÒN NỢ**: PDF không xuất nổi toàn bộ 17.544 KH (dompdf memory exhausted, fatal không bắt được);
  chọn 1 trong 3 hướng: chặn số dòng / nâng `memory_limit` riêng / đẩy queue + mail.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-export-file-design.md

- customer-import-excel → @khoipv → .plans/gop-db/customer-import-excel/plan.md
  Trạng thái: **HOÀN THÀNH — user test xong** (2026-08-11). Import Excel 25 cột cho `/assign/customers`
  (`V2BaseImportModal` 4 bước, gọi lại `CustomerService::save()`); danh mục tra theo tên, KHÔNG tự tạo
  mới; trùng MST/CCCD báo lỗi, chỉ tạo mới.
  Spec: docs/superpowers/specs/gop-db/2026-08-10-customer-import-excel-design.md

- customer-care-serial-catalog → @junfoke → .plans/gop-db/customer-care-serial-catalog/plan.md
  Trạng thái: **CODE DONE + ĐÃ VERIFY (BE + trình duyệt)** (2026-08-06). Chuyển "Danh mục serial thiết bị
  làm dịch vụ" (21.632 dòng) sang CSKH — 1 màn READ-ONLY + Xuất Excel, quyền 1126.
  Còn treo: user rà bằng mắt; chốt cách lọc 13 bản ghi `status` 0/3.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-06-customer-care-serial-catalog-design.md | Tóm tắt: .plans/gop-db/customer-care-serial-catalog/design.md

- chuyen-code-phan-he → @junfoke → .plans/gop-db/chuyen-code-phan-he/plan.md
  Trạng thái: **XONG 3 phân hệ + Phase 17-19 (chuẩn hub 14/17 phân hệ), ĐÃ VERIFY TRÌNH DUYỆT** (2026-08-06).
  Giai đoạn 2 của `tach-phan-he-erp-hrm`: đưa CODE về đúng phân hệ (Danh mục chung 10 màn, BHXH 7 màn,
  Bán hàng 27 màn — 98 cặp redirect giữ URL cũ, 6 migration quyền).
  Còn nợ: 7 màn địa lý-ngân hàng chưa có permission; bộ quyền KH cũ của HRM (166-169) còn song song.
  Bước tiếp: các phân hệ còn lại chưa tới lượt chuyển code.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-04-chuyen-code-phan-he-master-data-insurance-design.md
  và docs/superpowers/specs/gop-db/2026-08-06-hub-menu-customer-care-finance-design.md | Tóm tắt: .plans/gop-db/chuyen-code-phan-he/design.md

- customer-docs → @junfoke → .plans/gop-db/customer-docs/plan.md
  Trạng thái: **DONE** (2026-08-15) — bộ 3 tài liệu (TC 235 case / SRS / HDSD 38 trang) cho màn
  Danh mục khách hàng `/assign/customers` (code do @khoipv làm).
  Chi tiết + gotcha: plan.md

- customer-care-cost-catalog → @junfoke → .plans/gop-db/customer-care-cost-catalog/plan.md
  Trạng thái: **BE + FE DONE, verify BE xong** (2026-08-03). Chuyển "Danh mục dịch vụ sửa chữa và chi phí
  khác" (`costs`, `kind_of=2`) sang CSKH; Phase 5 cắt luôn `erp-cost-catalog` sang luồng mới.
  ⚠️ Còn nhiều chỗ dùng `mysql2` ngoài phạm vi danh mục chi phí (AssignBusinessController, QuotationService…).
  Bước tiếp: user verify bằng mắt `/customer-care/costs`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-03-customer-care-cost-catalog-design.md | Tóm tắt: .plans/gop-db/customer-care-cost-catalog/design.md

- finance-product-transfer-request → @khoipv → .plans/gop-db/finance-product-transfer-request/plan.md
  Trạng thái: **HOÀN THÀNH — user xác nhận** (2026-08-07), đã commit `hrm-api 3a0acce08` ·
  `hrm-client ed0abb049`. Port màn ERP "Phiếu yêu cầu chuyển hàng" sang Tài chính, 2 cổng song song
  cùng bảng, HRM chỉ ghi status 2↔3. SQL DEPLOY đã chạy môi trường thật (quyền 1129–1133).
  ⚠️ **CHƯA mở task, còn nợ team**: middleware `CheckPermission` hỏng trên `gop_db` (spatie bỏ sót role
  gán từ ERP do `model_type` mismatch) → cần TASK RIÊNG rà mọi route đang gắn `checkPermission`.
  **Đợt chỉnh 2026-08-13 (Phase 8) — CHỜ USER TEST**: chuẩn hoá footer 2 màn sang `V2Footer`
  (nhãn "Lưu nháp"/"In"/"Quay lại", popup xác nhận khi Gửi duyệt; mất icon spinner ở 3 nút).
  Spec: docs/superpowers/specs/gop-db/2026-08-05-finance-product-transfer-request-design.md

- customer-care-services-catalog → @khoipv → .plans/gop-db/customer-care-services-catalog/plan.md
  Trạng thái: **CODE DONE P1–P5, user xác nhận** (2026-08-05). Port "Danh mục gói bảo dưỡng"
  (207 dòng + 5 bảng con) sang `/customer-care/services`: 12 route, form 5 khối, in template 191.
  🐛 Đã sửa 2 lỗi CRITICAL `key_word` shape `{text}` (88/207 gói có nguy cơ hỏng màn báo giá DV ERP).
  ⚠️ Bug HỆ THỐNG chưa sửa (file chung, cần báo team): `V2BaseSelect.vue:59` rớt option `id = 0`.
  ⚠️ **Khi DEPLOY phải chạy tay 3 SQL** (chi tiết `sdd-progress.md` Task 1.5).
  **Đợt chỉnh 2026-08-13 (Phase 11j–11l) — CHỜ USER TEST**: Excel hết cảnh báo "Number stored as text",
  đổi chữ "dịch vụ" → "gói bảo dưỡng", form dùng `V2Footer` (nút Lưu mất icon spinner — user đã chốt).
  Tồn: checklist "Verify tổng thể" cuối plan.md chưa tick.
  **Phase 12 (2026-08-17) — BỘ TÀI LIỆU BÀN GIAO XONG**: `testcase.xlsx` (171 TC, P0 63%, engine
  17 cột), `SRS - Danh mục gói bảo dưỡng.docx` (form 4 chương, FR-01…FR-11, 37 trang),
  `HDSD_Danh muc goi bao duong.docx` (31 trang) — sinh lại được bằng `gen_testcase.py` /
  `gen_srs.py` / `gen_hdsd.py`. Chờ user chốt 2 điểm: xuất Excel + in + xem danh sách hiện KHÔNG
  gắn quyền, và xuất Excel không áp bộ lọc màn hình (giữ nguyên như ERP).
  Spec: docs/superpowers/specs/gop-db/2026-08-04-customer-care-services-catalog-design.md | Ledger: .plans/gop-db/customer-care-services-catalog/sdd-progress.md

- bo-sung-menu-phan-he → @junfoke (Phase 11: @khoipv) → .plans/gop-db/bo-sung-menu-phan-he/plan.md
  Trạng thái: **CODE DONE + KIỂM THỬ TỰ ĐỘNG PASS** (Phase 0-9: 2026-08-03; Phase 11 dọn nhãn menu
  Danh mục chung: 2026-08-12). Khai 355 mục menu trên 14 phân hệ, chỉ đụng `hrm-client`.
  ⚠️ Bug đã phát hiện, CHƯA SỬA (không thuộc feature): mục "Khách hàng" khai TRÙNG ở `master-data.js`
  và `sale.js` → `/assign/customers` luôn ra sidebar Danh mục chung.
  Bước tiếp: Phase 10 — verify trình duyệt thật.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-01-bo-sung-menu-phan-he-design.md | Tóm tắt: .plans/gop-db/bo-sung-menu-phan-he/design.md

- customer-care-maintenance-catalogs → @junfoke → .plans/gop-db/customer-care-maintenance-catalogs/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE)** (2026-08-03). 2 màn ĐẦU TIÊN của phân hệ CSKH: "Cấp dịch vụ
  bảo dưỡng" + "Danh mục ghi chú kiểm tra bảo dưỡng", quyền 1115-1118.
  Còn nợ: `ErpPermissionHelper` + `Modules/Assign` vẫn qua `mysql2`.
  Bước tiếp: user verify `/customer-care/levels` + `/customer-care/note-maintenances`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-03-customer-care-maintenance-catalogs-design.md | Tóm tắt: .plans/gop-db/customer-care-maintenance-catalogs/design.md

- finance-currency-catalog → @junfoke → .plans/gop-db/finance-currency-catalog/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE + cron)** (2026-08-03) — màn thứ 3 của phân hệ Tài chính.
  Kèm chuyển cron tỷ giá sang HRM (`finance:update-exchange-rate`, 03:00) và đã tắt lịch bên ERP.
  ⚠️ Trước khi lên thật: `hrm-api/.env` chưa cấu hình mail nên `emailOutputTo` chưa gửi được.
  Bước tiếp: user verify bằng mắt `/finance/currencies`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-08-03-finance-currency-catalog-design.md | Tóm tắt: .plans/gop-db/finance-currency-catalog/design.md

- finance-account-catalog → @junfoke → .plans/gop-db/finance-account-catalog/plan.md
  Trạng thái: **PHASE 1-6 + 8 CODE DONE + VERIFIED** (2026-08-01) — 2 màn "Danh mục tài khoản" +
  "Danh mục loại tài khoản"; màn đầu tiên của phân hệ Tài chính nên dựng luôn khung `Modules/Finance`.
  Bước tiếp: Phase 7 đối chiếu 2 cổng (cần bật ERP local) + tạo 2 file mẫu Excel trong `hrm-client/static/`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-07-30-finance-account-catalog-design.md | Tóm tắt: .plans/gop-db/finance-account-catalog/design.md

- tach-phan-he-erp-hrm → @junfoke → .plans/gop-db/tach-phan-he-erp-hrm/plan.md
  Trạng thái: **XONG GIAI ĐOẠN 1 (khung phân hệ + menu)** (2026-07-30), đã test thật 9 màn trên dev.
  Quy hoạch lại 24 phân hệ / 5 nhóm theo Sơ đồ tổng thể v1.6; dựng base 17 phân hệ mới.
  Bước tiếp: user test 17 màn edit/detail. Giai đoạn 2 = `chuyen-code-phan-he`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-07-30-tach-phan-he-erp-hrm-design.md | Tóm tắt: .plans/gop-db/tach-phan-he-erp-hrm/design.md
