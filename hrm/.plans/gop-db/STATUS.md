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

## Đang làm

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
  **File MỚI:** `bao-cao-tong-hop-nhu-cau-khach-hang.html` (xem qua `python3 -m http.server 8952` trong thư mục feature) — layout bám ảnh Excel "Báo cáo tổng hợp nhu cầu khách hàng", style tái dùng nguyên token + component của file báo cáo meeting. Nội dung: **toolbar 7 bộ lọc** (Kỳ xem theo thời gian bắt đầu họp · Lĩnh vực KD · Khách hàng · cascade Công ty ▸ Phòng ban ▸ Bộ phận ▸ Kinh doanh chủ trì) · **KPI** (tổng nhu cầu / tổng giá trị đầu tư / khách hàng / chưa có dự án TKT) + 3 khối phân bổ · **bảng outline 3 cấp** `I` Lĩnh vực KD → `1` Thị trường → `1.1` Khách hàng, 10 cột, sticky header + TỔNG CỘNG · **2 chế độ cột** (CHI TIẾT 10 cột ↔ TỔNG HỢP 4 cột, ẩn hết cột rỗng) · nút **"+ TẠO MỚI"** cột Dự án TKT → popup tạo dự án (mã `TKT.YYYY.<viết tắt KH>`) → trạng thái **"Đã lập dự án TKT"** · **click tên meeting → drawer chi tiết meeting** (khung `.ticket-drawer` của file báo cáo meeting, 4 khối + nút Tạo dự án TKT) · Xuất Excel + In báo cáo (tổng hợp/chi tiết, A4 ngang) bám chế độ đang xem · data demo **26 nhu cầu / 18 KH / 4 lĩnh vực / 3 thị trường**.
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

- customer-cut-mysql2 → .plans/gop-db/customer-cut-mysql2/plan.md
  Trạng thái: **HOÀN TẤT + ĐÃ TEST** (2026-08-01, nhánh `gop_db`). Khách hàng còn ĐÚNG 1 luồng `/assign/customers`.
  Gồm: cắt hết `mysql2` khỏi luồng KH (35 file) · xoá 6 bảng `hrm_customer_*` + migration `2026_08_01_000001_drop_hrm_customer_tables` (đã test round-trip) ·
  gỡ toàn bộ tầng sync 2 chiều · xoá màn `/human/customers` + `/timesheet/setting/customers` · chuyển 10 picker sang luồng mới · thêm `GET assign/customers/search`.
  Test: 52/52 endpoint HTTP + 12 màn browser + luồng ghi (tạo/sửa/thêm liên hệ, có rollback). **7 lỗi thật đã sửa** (xem plan.md Phase 11-12).
  ⚠️ Đọc trước khi làm tiếp trên nhánh này: `.plans/gop-db/design.md`.

- bo-sung-menu-phan-he → @junfoke → .plans/gop-db/bo-sung-menu-phan-he/plan.md
  Trạng thái: **CODE DONE + KIỂM THỬ TỰ ĐỘNG PASS** (2026-08-01) — Phase 0-8 xong.
  Khai 355 mục menu trên 14 phân hệ theo sheet `Gộp phân hệ ERP-HRM` (10 mục link thật sang ERP, 345 mục xám mờ),
  kèm ẩn 3 phân hệ Mua hàng / Kho / Vận chuyển. Chỉ đụng `hrm-client`. Kiểm thử bằng cách render THẬT `Sidebar.vue`
  qua `vue-server-renderer`; regression 11 bộ menu cũ cho kết quả render-identical với bản `git show HEAD`.
  Phase 8 đã sửa trực tiếp sheet gộp (đã sao lưu bản gốc trước khi sửa).
  Bước tiếp: **Phase 9 — verify browser thật, CHƯA LÀM** (độ mờ mục xám, sidebar Bán hàng 184 mục / Tài chính 104 mục).
  8 gotcha + bài học (ẩn phân hệ làm khuất màn phân hệ khác, bẫy khớp dòng trong sheet, `Sidebar.vue` chỉ render `router-link`…): xem plan.md.
  Spec: docs/superpowers/specs/gop-db/2026-08-01-bo-sung-menu-phan-he-design.md | Tóm tắt: .plans/gop-db/bo-sung-menu-phan-he/design.md

- customer-care-maintenance-catalogs → @junfoke → .plans/gop-db/customer-care-maintenance-catalogs/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE)** (2026-08-03) — chuyển "Cấp dịch vụ bảo dưỡng" (`levels`)
  + "Danh mục ghi chú kiểm tra bảo dưỡng" (`note_maintenances`) từ ERP sang **phân hệ CSKH**; là 2 màn ĐẦU TIÊN của
  phân hệ này (`Modules/CustomerCare` trước đó rỗng, chưa có quyền `type=24` nào).
  BE 13 file + 16 route `/v1/customer-care`, quyền 1115-1118, FE 2 màn danh sách + 2 modal.
  Sửa 2 lỗi ERP: `levels` chỉ kiểm 1/6 bảng khi xóa, `note_maintenances` không chặn xóa gì.
  ⚠️ Phát sinh: **ERP + HRM đã gộp chung `employees` / `employee_infos`** → gỡ toàn bộ lớp map ERP employee id
  khỏi Finance + CSKH (Phase 1 trong plan.md). Còn nợ: `ErpPermissionHelper` + `Modules/Assign` vẫn qua `mysql2`.
  Bước tiếp: user verify bằng mắt `/customer-care/levels` + `/customer-care/note-maintenances`.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-customer-care-maintenance-catalogs-design.md | Tóm tắt: .plans/gop-db/customer-care-maintenance-catalogs/design.md

- finance-currency-catalog → @junfoke → .plans/gop-db/finance-currency-catalog/plan.md
  Trạng thái: **CODE DONE + VERIFIED (BE + cron)** (2026-08-03) — màn thứ 3 của phân hệ Tài chính.
  Bám sát ERP (danh sách + modal CRUD + xóa + lọc + Xuất Excel), không đổi schema `currencies`.
  8 route, quyền 1113/1114. Chuyển luôn cron tỷ giá sang HRM (`finance:update-exchange-rate`, 03:00)
  và **đã tắt lịch bên ERP** → HRM là nơi duy nhất chạy tự động.
  Sửa 4 lỗi của cron ERP, nặng nhất: đồng tiền đứng ĐẦU file XML không bao giờ được cập nhật (AUD đứng im ~16 tháng).
  ⚠️ Trước khi lên thật: `hrm-api/.env` chưa cấu hình mail nên `emailOutputTo` chưa gửi được.
  Bước tiếp: user verify bằng mắt `/finance/currencies`.
  Spec: docs/superpowers/specs/gop-db/2026-08-03-finance-currency-catalog-design.md | Tóm tắt: .plans/gop-db/finance-currency-catalog/design.md

- finance-account-catalog → @junfoke → .plans/gop-db/finance-account-catalog/plan.md
  Trạng thái: **PHASE 1-6 + 8 CODE DONE + VERIFIED** (2026-08-01) — 2 màn "Danh mục tài khoản" +
  "Danh mục loại tài khoản" từ ERP sang phân hệ **Tài chính**; là màn đầu tiên của phân hệ nên phải dựng luôn khung
  `Modules/Finance` + `components/subsystem-menu/finance.js`.
  Port trọn bộ: CRUD + khóa/mở + lịch sử + Xuất/Import Excel + In danh sách (template DB id 459).
  26 route, quyền 1107-1110 (`type=8`). Verify HTTP thật 33 case + browser Playwright toàn luồng, DB trả nguyên trạng.
  Bước tiếp: Phase 7 đối chiếu 2 cổng (cần bật ERP local) + tạo 2 file mẫu Excel trong `hrm-client/static/`.
  Toàn bộ gotcha/bài học (4 lỗi FE khi chạy thật, 4 bài học phân trang, icon phải lấy từ codebase,
  tên `group` permission phải duy nhất…): xem plan.md.
  Spec: docs/superpowers/specs/gop-db/2026-07-30-finance-account-catalog-design.md | Tóm tắt: .plans/gop-db/finance-account-catalog/design.md

## Hoàn thành

- tach-phan-he-erp-hrm → @junfoke → .plans/gop-db/tach-phan-he-erp-hrm/plan.md
  Trạng thái: **XONG GIAI ĐOẠN 1 (khung phân hệ + menu) — 2026-07-30.** Đã test thật 9 màn trên dev. Tồn: user test 17 màn edit/detail. Giai đoạn 2 (di chuyển code màn sang route mới) chưa bắt đầu — xem Phase 7 trong plan.md.
  Scope: Quy hoạch lại phân hệ ERP + HRM theo Sơ đồ tổng thể v1.6 → 24 phân hệ / 5 nhóm. Dựng base 17 phân hệ mới (BE 17 module skeleton, FE registry `components/subsystems.js` + menu + dashboard stub + icon SVG), dựng lại màn chọn phân hệ + menu chuyển nhanh, phân hệ mới đi menu dọc (`layouts/subsystem.vue`).
  ⚠️ GOTCHA: (1) mỗi link chỉ được thuộc ĐÚNG 1 phân hệ, trùng là `resolveSubsystem` trả sai. (2) layout dùng SidebarMenu phải có method `toggleMenu`, thiếu thì bấm thu gọn menu ra trang 404. (3) item menu không có `subItems` phải khai `isShow: true`, quên thì sidebar rỗng. (4) dự án nạp 2 bản Remix Icon xung đột codepoint → icon phân hệ dùng SVG tự vẽ.
  Spec: docs/superpowers/specs/gop-db/2026-07-30-tach-phan-he-erp-hrm-design.md | Tóm tắt: .plans/gop-db/tach-phan-he-erp-hrm/design.md
