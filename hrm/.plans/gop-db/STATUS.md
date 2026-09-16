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

- quy-hoach-lai-menu-phan-he → @junfoke → .plans/gop-db/quy-hoach-lai-menu-phan-he/plan.md
  Trạng thái: **CODE DONE CẢ 5 NHÓM + VERIFY BROWSER khung menu** (16/09/2026).
  Sắp xếp lại nhóm/phân hệ/menu `hrm-client` theo 5 sheet của sơ đồ chốt 04/09/2026 —
  tách 3 phân hệ mới (Meeting, CSKH trước bán, An toàn 5S), đổi tên hàng loạt, dời chức năng.
  ⚠️ Đọc sheet phải xem **màu nền + gạch ngang** (CSV không mang): gạch = bỏ/chuyển đi, vàng = làm sau.
  Đã tách `/human/settings` thành 3 màn mới (Tính lương / Quản trị hệ thống / Bảo hiểm) và cho
  menu ngang hiện xám mờ mục chưa có màn (sửa `Topbar.vue`).
  Thêm 4 phân hệ: Meeting · An toàn 5S · CSKH trước khi bán · Tra cứu - thông báo.
  ⚠️ 3 lỗi do menu mới đã sửa: màn chọn phân hệ vỡ khi phân hệ thiếu `image`, cánh hoa cắt mất
  phân hệ thứ 9, menu ngang tràn. Bước tiếp: verify từng màn con.
  Spec: docs/superpowers/specs/gop-db/2026-09-16-quy-hoach-lai-menu-phan-he-design.md | Tóm tắt: .plans/gop-db/quy-hoach-lai-menu-phan-he/design.md

- bao-cao-ke-hoach-lam-viec-nhan-vien → @namdangit → .plans/gop-db/bao-cao-ke-hoach-lam-viec-nhan-vien/plan.md
  Trạng thái: **MOCKUP HTML XONG — VERIFY PLAYWRIGHT 1600×900, CONSOLE 0 LỖI (08/09/2026)**. Chưa động vào code thật.
  Màn báo cáo **MỚI**, không thay `meeting-by-employees` hay `task-manager-by-employees`. Theo dõi **khối lượng công việc** của Phòng ban ▸ Bộ phận ▸ Nhân viên, gom **5 nguồn** đang nằm rải rác: `meetings` · `tasks` · `issues` · `assign_business` · `assign_jobs`. Định nghĩa chỉ tiêu bám đúng hằng số trạng thái trong `hrm-api/Modules/Assign` (có bảng tra trong `design.md`).
  Style port nguyên khối từ `../bao-cao-phat-trien-thi-truong-khach-hang/`; danh mục tổ chức dùng chung bộ **2 công ty · 10 phòng ban · 2 bộ phận · 43 nhân viên** của màn đó.
  **5 quyết định lõi:** 10 cột (5 loại + Tổng · Đã HT · Tỷ lệ HT) · tính vào kỳ theo **GIAO NHAU (overlap)**, không theo ngày tạo · 1 đầu việc tính cho **MỌI người tham gia** (đếm cặp chứng từ × người nên dòng cha luôn = tổng dòng con) · nháp + huỷ/từ chối **vẫn nằm trong Tổng** ⇒ tách **4 nhóm trạng thái chia hết tổng** · **bỏ mọi chỉ số bình quân**.
  Kỳ mặc định 09/2026: **1.040 đầu việc · 37/43 NV có việc · hoàn thành 51,0%**.
  ⚠️ **Nợ backend:** `tasks` có `due_time` nhưng **KHÔNG có `start_time`** → muốn giờ bắt đầu của Task đúng như mockup thì phải bổ sung cột, nếu không BE chỉ trả `00:00`.
  ⚠️ **Bẫy đã trả giá (chi tiết ở `design.md` mục "Gotcha"):** `.drill-table { min-width: 1740px }` là số cứng của bảng **14 cột** màn mẫu — port sang bảng ít cột hơn thì nó ép giãn và khiến **mọi chỉnh `colgroup` vô tác dụng**; `scrollWidth` của phần tử chứa icon ⓘ luôn bị tooltip `::after` thổi phồng nên **không dùng để kết luận chữ bị cắt** (đo bằng `Range` thay thế); đặt `overflow:hidden` lên nhãn có icon ⓘ sẽ **cắt mất tooltip**.
  ℹ️ Feature nằm trong `.plans/gop-db/` để ở cạnh cụm mockup báo cáo anh em (design.md trỏ đường dẫn tương đối sang đó), **nhưng 2 repo đang đứng ở nhánh `tpe`** — không phải nhánh con của `gop_db`. Mockup không đụng code repo nên không ảnh hưởng; khi port sang Vue thật cần chốt lại nhánh.
  **Bước tiếp theo:** chờ user chốt mockup → SRS + testcase (nếu cần) → port Vue `pages/assign/report/` → API BE.

- theo-doi-thuc-hien-hop-dong → @namdangit → .plans/gop-db/theo-doi-thuc-hien-hop-dong/plan.md
  Trạng thái: **PHASE 1 XONG — MOCKUP HTML 7 TAB + VERIFY PLAYWRIGHT 1440×900 (02/09/2026)**. Chưa động vào code thật.
  Nguồn: `THEO DÕI THỰC HIỆN HỢP ĐỒNG.docx` (họp 25/08/2026). Màn **mới, độc lập** với `/assign/contracts/{id}`.
  6 tab: Thông tin chung · **Cung ứng** · **Giao hàng & nghiệm thu** · Tài chính (4 tab con) · Thiết kế & giám sát · Bảo hành.
  Khảo sát: module HĐ **đã có sẵn** 4 trạng thái + `sign_date`/`effective_date`/`expiry_date`/`execution_deadline_days`/`EFFECTIVE_COND_*`/`EXEC_BASE_*` + `ContractPaymentTermsTable` + guard `getCanExportAttribute` → mockup bám vào, không vẽ lại.
  Nghiệp vụ lõi tab Cung ứng: `Giữ hàng + Đang đi mua ≥ SL ký` cho từng mã, chưa đủ thì tô đỏ + **chặn tạo YC xuất hàng**.
  ⚠️ Phát hiện lỗi có sẵn ở `mockup-chi-tiet-bao-gia`: `thead` sticky **không bao giờ dính** vì `.tblwrap{overflow-x:auto}` không cuộn dọc (đo `theadTop: -124`) — cần sửa kèm khi port sang code thật.
  **Vòng 2 (02/09/2026):** sidebar thu gọn rail 62px (burger bật/tắt) · **bỏ stepper** (màn chỉ áp dụng HĐ *Có hiệu lực*) · rút nhãn tab bỏ số thứ tự (7 tab vừa khít, dư 0px) · **thiết kế lại khối tổng hợp 7 tab theo mockup `bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`** (card `.rsum` có Thu gọn + box tint `.rsum-blk` + hàng `.rsum-kpi` border-left, track 5px). Sửa lỗi số liệu: tổng *Đang đi mua* 218→**217**, *Đã phân bổ* 1.676→**1.675** (cân đúng 1.675+92=1.767=tổng SL ký).
  **Vòng 3 (02/09/2026):** tab Thông tin chung **bỏ hết summary tài chính** (chỉ theo dõi ở tab Tài chính) · gỡ trùng lặp với thanh tiêu đề (mã HĐ / khách hàng / trạng thái / giá trị / số ngày còn lại — đo được 0 lần trong tab) · **chia lưới thông tin HĐ thành 4 nhóm chủ đề** (6·6·3·3 ô, không nhóm nào lẻ ô).
  **Vòng 4 (02/09/2026):** card đổi tên **Thông tin chung** với 4 nhóm *Thông tin hợp đồng (9 ô) · Thông tin khách hàng (6) · Hiệu lực & thời hạn (9) · File đính kèm (bảng 4 file)* · card timeline → **Tiến độ thực hiện theo các mốc thời gian** · **bỏ hết note điều hướng sang tab khác** (đo 0 lần toàn trang). Không còn bảng nào phải cuộn ngang ở cả 7 tab.
  **Vòng 5 (02/09/2026):** nhóm *Thông tin hợp đồng* 12 ô (**Số hợp đồng đứng đầu**), *Thông tin khách hàng* 9 ô (**Mã KH · Tên KH · MST lên trước**) — **nới nguyên tắc gỡ trùng lặp**: trường định danh vẫn nằm trong nhóm của nó · **tô màu nhận diện 7 tab** (`--tc`/`--tcl`: xanh dương · teal · cam · xanh lá · tím · hồng · hổ phách), chiều cao 7 tab đồng đều 35px, không tràn khung.
  **Vòng 6 (03/09/2026):** bỏ meta *Người lập/Tạo lúc* · thanh tiêu đề thêm **KD phụ trách** · bỏ 4 trường *Mẫu in · Người nhận cảnh báo · Cảnh báo giao hàng · Cảnh báo hết hiệu lực* → nhóm 10·9·6 ô (ô *Thời gian bảo hành* tràn hết hàng để không lẻ dòng; gộp *Ngày bàn giao mặt bằng* vào *Mốc tính thời hạn*).
  **Vòng 7 (03/09/2026):** **mở ô nhập tay** đúng các trường tài liệu ghi bắt buộc — Thông tin chung 6 ô (Ngày ký · Điều kiện hiệu lực · Ngày có hiệu lực · Mốc tính thời hạn · Ngày đạt mốc · Thời hạn thực hiện) + **Ngày hết hiệu lực khoá `TỰ TÍNH`** kèm công thức; Tài chính 5 ô (lý do vượt dự toán — dòng chưa nhập viền đỏ; ngày đạt mốc + nút đính kèm biên bản); Thiết kế 2 ô; Giao hàng 6 ô. **Không** mở nhập ở tab Cung ứng (SL sinh từ phiếu giữ / đơn mua).
  **Vòng 8 (03/09/2026):** **bỏ tab *Hàng hoá ký***, gộp dịch vụ vào tab **Cung ứng & dịch vụ** (2 bảng: phương án cung ứng 9 mã + *Dịch vụ đã ký* 4 gói với % tiến độ & trạng thái hạch toán) → còn **6 tab**; timeline **bỏ chip Đúng hạn ở mốc Ký hợp đồng** (chỉ kiểm soát đúng hạn từ các mốc sau khi ký). ⚠️ Tự bắt lỗi: card dịch vụ chèn rơi ngoài `pane#p3` (hiện ở mọi tab) — đã sửa.
  **Chốt 03/09/2026:** **bỏ hẳn đơn giá / thành tiền / VAT từng đầu mục** — màn theo dõi chỉ giữ số lượng ở cấp đầu mục, tiền chỉ ở cấp tổng (thanh tiêu đề + tab Tài chính).
  **Vòng 9 (03/09/2026):** bảng cung ứng — header có viền đồng nhất thân bảng · dòng *Đang đi mua* thêm **số YCĐH** (PO xuống dòng phụ) · dòng *Giữ hàng* thêm **Hạn giữ** (có chip cảnh báo sắp hết hạn) · cột **Đã về kho → Tồn kho khả dụng** (đổi cả nội dung thành số tồn dùng được, để quyết Giữ hàng hay Đặt hàng) · dòng đủ phương án bỏ nút *Sửa phương án* · bảng chi tiết thêm tiêu đề 8 cột. ⚠️ Tự bắt lỗi: cùng số PO ghi 2 NCC khác nhau giữa tab Cung ứng và Tài chính — đã gán lại theo bảng công nợ NCC.
  **Vòng 10 (03/09/2026):** **logic Hiệu lực & thời hạn chạy thật** — *Kể từ ngày ký* → ngày hiệu lực = ngày ký; *Theo bảo lãnh* → hiện thêm **Số bảo lãnh + Ngày bảo lãnh duyệt**, hiệu lực lấy theo ngày bảo lãnh; *Theo đặt cọc lần đầu* → lấy ngày phiếu thu đặt cọc đầu tiên (nguồn ở tab Tài chính, **nối sau**). Ngày có hiệu lực + Ngày hết hiệu lực đều là ô `TỰ TÍNH` có dòng nguồn/công thức động. Chạy thử 8 kịch bản Playwright.
  **Vòng 11 (03/09/2026):** tab Cung ứng — hàng KPI đổi sang **“Tình hình đặt mua”** (Tổng đặt mua 4 đơn mua · **Số lượng đã về kho 121** · **Số lượng đang mua 96**, 2 ô sau bấm ra **popup chi tiết từng mã**); thêm 2 cột **SL đã xuất / SL còn lại**, dựng lại bảng để **mọi cột sau tính theo SL còn lại** (mã đã giao đủ → trạng thái *Đã xuất đủ*). Cân bằng số học 9/9 dòng, 0 lỗi; tổng 1.767/1.458/309/1/216/217/92.
  **Vòng 12 (03/09/2026):** dòng *Giữ hàng* tình trạng **chỉ còn Còn hạn / Quá hạn** (suy từ Hạn giữ) · **bỏ toàn bộ 7 dòng ghi chú quy tắc** (toàn trang 0 lần chữ “Quy tắc”) · **popup dựng lại theo khung `.ticket-drawer` của mockup Báo cáo CSKH tiềm năng** (drawer trượt phải, header gradient + icon tròn + chip trắng mờ) · khối *Hàng hoá cần cung ứng* đổi **Đã phân bổ → Số lượng đã giao 1.458 (82,5%)**, sửa luôn số cũ 1.675 đã lỗi thời.
  **Vòng 13 (03/09/2026):** popup đổi từ drawer trượt phải sang **`.minutes-modal` căn giữa màn hình** (đúng khung popup của mockup mẫu) · bảng trong popup **cuộn được + tiêu đề cột dính** (`max-height:56vh`) · **Tồn kho khả dụng ≤ 0 thì bỏ nút *Giữ hàng***, chỉ còn *Đặt hàng*.
  **Vòng 14 (03/09/2026):** **tab Tài chính chia 4 tab con** — *Giá trị & thanh toán* · *Công nợ NCC* · *Công nợ KH* · *Dự toán*, mỗi tab con có **thống kê + cảnh báo riêng**; bổ sung **bảng phiếu chi NCC** (7 dòng) và **bảng phiếu thu KH** (6 dòng); tách bảng công nợ cũ thành *điều khoản* (tab 1) và *tình hình thu* (tab 3). Cân bằng số học khớp 100% (phiếu chi = đã trả · phiếu thu = đã thu · tổng 5 đợt = giá trị HĐ).
  **Vòng 15 (03/09/2026):** **tab Giao hàng & nghiệm thu lên vị trí 3** · cột *Nội dung giao* rút thành `N mã · M đơn vị` **bấm ra popup chi tiết mã + SL trong đợt** · demo **1 đợt nhiều PXK** (đợt 2: PXK-1326 + PXK-1331) · cột *Đã giao* **bấm ra popup serial** (mã vật tư không quản lý serial thì popup nói rõ). 12 popup bấm thử toàn bộ, 0 lỗi. ⚠️ Tự bắt 2 lỗi: link serial gắn nhầm cột *SL ký* ở 3 dòng; đợt 3 còn 5 ngày chứ không phải 6.
  **Vòng 16 (03/09/2026):** header popup **dùng chung 1 gradient xanh** `#0a1c3d → #0e7490` (đúng `.minutes-modal__header` của mockup CSKH), bỏ màu theo ngữ cảnh — đo 12/12 popup chỉ còn 1 gradient.
  **Vòng 17 (03/09/2026):** đổi nhãn tab **“Cung ứng & dịch vụ” → “Cung ứng”** (nội dung giữ nguyên).
  **[06/09 wrap up]** Mockup chốt ở **vòng 17**. Mở bằng `file://` (file tự chứa, 0 tham chiếu ngoài) hoặc HTTP **cổng cố định 8700**. Thư mục có thêm `QLHD_mockup.html` = bản sao user tự đặt tên.
  **CÒN:** (a) user duyệt UI mockup vòng 17; (a2) nối ngày đặt cọc thật từ phiếu thu ở tab Tài chính (đang hard-code) + chốt có bỏ ô *NV kinh doanh* trong nhóm HĐ không (đã có ở tiêu đề); (b) mockup nhóm A (trường + luồng 7 trạng thái trong form HĐ) và nhóm C (3 báo cáo) — user chốt làm sau; (c) màn danh sách HĐ đang thực hiện — làm sau.

- **catalog-import-export — Import + Export cho các màn Danh mục đã chuyển ERP → HRM** → @junfoke →
  `.plans/gop-db/catalog-import-export/design.md` · `plan.md` ·
  spec `docs/superpowers/specs/gop-db/2026-09-10-catalog-import-export-design.md`
  Trạng thái: **XONG TOÀN BỘ 20/20 TASK, CHỜ NGHIỆM THU** (2026-09-11). Nhánh
  `feat/catalog-import-export` (tách từ `gop_db`), **chưa commit**.
  Kết quả: **13 màn có Import**, **9 màn có thêm Export**. Mỗi màn đã chạy thật: validate ra đúng
  số dòng hợp lệ/lỗi với đúng thông báo, import ghi đúng DB + Lịch sử thay đổi, không đẻ danh mục
  cha, export khớp `total` của danh sách; dữ liệu thử đều đã xoá.
  Không dựng framework mới: mixin `FinanceImportMixin` đổi tên thành `CatalogImportMixin` dùng chung,
  file mẫu **sinh động tại FE** từ chính `importColumns` qua hàm mới `buildImportTemplate()`.
  Có 19 unit test PHPUnit (`CurrencyImportValidationTest` 10, `ProvinceImportValidationTest` 9).
  ⚠️ **GOTCHA phải biết khi sửa tiếp** (chi tiết trong `plan.md`):
  · 3 lớp `ApiController` khác nhau — **9/13 controller KHÔNG có `responseBadRequest()`**;
  · `nations` không có cột `code`, mã nằm ở `country_code`;
  · khoá chống trùng thật: Tiền tệ/Quốc gia/Ngân hàng/Ghi chú BD trùng **2 khoá**, Tỉnh/TP theo
    (quốc gia+khu vực), Phường/xã theo (tỉnh+tên), Costs theo nhóm `type IS NULL`;
  · cột trạng thái trên bảng đặt key riêng (`workStatus`, `nationStatus`…) nên phải khai
    `exportFieldKeyMap`, không thì popup rớt cột Trạng thái.
  🐞 **Đã sửa 3 lỗi CÓ SẴN gặp dọc đường** (ngoài phạm vi feature, user duyệt sửa):
  · `NationService` sort `nations.code` → cột thật `country_code`, bấm sắp xếp cột Mã quốc gia trả
    500 (nay 200);
  · màn Phường/xã **chưa bao giờ ghi được Lịch sử thay đổi** — `wards.id` không AUTO_INCREMENT
    nhưng model khai `incrementing = true` nên `getKey()` = 0 làm `logCatalogCreate()` thoát sớm;
  · N+1 `Ward::canDelete()` (1 query/dòng) khiến API danh sách Phường/xã mất 23s/5.000 dòng →
    gom 1 query còn **3s**; đã đối chiếu 200 bản ghi, 0 sai lệch kết quả `can_delete`.

- **prod-cutover — Đưa `gop_db` lên PROD (1 nhánh, 2 môi trường)** → @namdangit →
  `.plans/gop-db/prod-cutover/design.md` · `plan.md` ·
  spec `docs/superpowers/specs/gop-db/2026-09-04-prod-cutover-design.md`
  Trạng thái: **SPEC XONG (Phase 0), CHƯA CODE** (2026-09-04).
  Kịch bản: ERP chạy code `master`, HRM chạy `gop_db`, **dùng chung 1 DB gộp**; PROD và dev
  **chung 1 nhánh** — PROD chỉ mở 7 phân hệ HRM đã nghiệm thu, dev thấy đủ để port tiếp.
  ⚠️ **Khảo sát phát hiện bản gộp `local_hrm_erp` đang có lỗi dữ liệu THẬT, âm thầm**:
  FK của ERP **2.313 → 10** (556 bảng có FK còn 7); **736 dòng ERP trỏ NHẦM sang vai trò HRM**
  + 1.820 mồ côi sau khi `ReconcileAuthSeeder` dời `roles.id +100000` mà chỉ remap 4/15 bảng —
  gồm `companies.deputy_role` sai ở **8/8 công ty** (VD: đáng lẽ "Tổng giám đốc" → đang trỏ
  "Quản lý Giải pháp DATKT SG"); `MergeProdSeeder` **DROP 14 bảng ERP** thay bằng bản HRM
  (`majors` 156 dòng → **0**, `areas` → **1/20**, ERP `master` vẫn dùng cả hai);
  `notifications` bị TRUNCATE (154k + 688k → **299**); nhóm `SHARE` ghi đè chéo theo id làm
  **77 khách hàng** bị ghi dữ liệu của khách khác.
  Nguồn lỗi nằm trong `Modules/Timesheet/Database/Seeders/GopDb/` → chạy pipeline đó lên PROD
  sẽ tái hiện y hệt. **Phải vá pipeline + dựng cổng nghiệm thu trước khi cut-over.**
  Đã chốt: cấu hình bật/tắt phân hệ **lưu trong DB (runtime)**, cắt **theo phân hệ** + chặn
  link lẻ; nhánh PROD hiện tại là `tpe`; ranh giới = 17 thư mục `pages/` mới + 3 màn
  (`/assign/contracts`, `/human/districts`, `/human/hamlets`); mức chặn BE **hoãn**.
  **PROD CHƯA gộp DB** (user xác nhận 2026-09-04) → còn kịp vá pipeline trước khi chạy thật.
  ✅ Đã có **cổng nghiệm thu**: `php artisan gopdb:health-check` (`app/Console/Commands/GopDb/HealthCheckCommand.php`)
  — CHỈ SELECT, chạy trên PROD an toàn. `--mode=pre` cảnh báo cái gì sắp mất, `--mode=post` đo cái gì đã hỏng,
  exit code 0/1/2 cắm được vào pipeline deploy. Danh sách nhóm bảng đọc từ `MergeProdSeeder` bằng Reflection.
  Bước tiếp: Phase 1 (vá pipeline gộp) hoặc Phase 3 (ẩn menu PROD) — chờ chọn.
- **finance-product-transfer — Phiếu điều chuyển hàng (ERP `product_transfers` → HRM)** → @junfoke →
  `.plans/gop-db/finance-product-transfer/khao-sat.md` · `design.md` · `plan.md`
  Trạng thái: **MỚI KHẢO SÁT XONG — chưa có dòng code nghiệp vụ nào** (2026-09-04).
  Nhánh riêng `feat/finance-product-transfer` (hrm-api + hrm-client, tách từ `gop_db`).
  Màn ERP `Warehouse\ProductTransfersController`, mã `PDCH-`, bảng đã có sẵn 309 phiếu trên DB gộp
  (không cần migration bảng chính). Chuyển hàng giữa 2 **kho kế toán** trong cùng 1 kho vật lý;
  2 trạng thái, "Duyệt" = hạch toán ngay (ghi `accounting_stocks` + `accounting_stock_logs` + bút toán
  Nợ 156/Có 156), hạch toán rồi khoá vĩnh viễn.
  ⚠️ GOTCHA: mục menu "Phiếu điều chuyển hàng" TRƯỚC ĐÂY bị gán nhầm link sang màn **Phiếu yêu cầu
  chuyển hàng** (`product-transfer-requests`) — 2 màn KHÁC nhau, ERP để ở 2 nhóm menu khác nhau.
  Đã trả về đúng chỗ 2026-09-04 (Task 0.2). Đừng gán link màn khác vào mục đó nữa.
  ⚠️ GOTCHA: **KHÔNG** mở rộng `AccountingStockService` cho màn này — `in_acc_warehouse` chỉ là SUM
  thô của kho kế toán đang chọn, không trừ pending; màn tự query. (Bản khảo sát đầu ghi sai.)
  Chốt với user: sửa 13 lỗi ERP theo chuẩn HRM · tách 2 method FIFO khỏi
  `WarehouseExportAccountingService` (chỉ 1 caller) · CÓ làm lịch sử thao tác (ERP không có) ·
  KHÔNG làm huỷ phiếu/đảo bút toán.
  Bước tiếp theo: viết spec → Phase 1 tách FIFO + test hồi quy màn Phiếu xuất hàng.

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
- finance-prepick-expiring → @junfoke → .plans/gop-db/finance-prepick-expiring/plan.md
  Trạng thái: **XONG — ĐÃ MERGE VÀO `gop_db`** (2026-09-04), cả 2 repo ahead origin/gop_db 2 commit,
  **chưa push** (user tự đẩy lên dev).
  Nhánh `feat/finance-prepick-expiring` (cả 2 repo, tách từ `gop_db`), worktree
  `.worktrees/finance-prepick-expiring` — tái sử dụng worktree cũ của finance-product-import-request.
  Port màn "Hàng sắp hết hạn giữ" bản KẾ TOÁN (`warehouseInfo.accountingExpiringPrepick`) sang
  Tài chính / nhóm Giữ hàng. Dùng lại ~90% `PrepickStockReportService` — chỉ thêm cờ `expiring_only`.
  ⚠️ User chốt **GIỮ NGUYÊN điều kiện ngày ngược nghĩa của ERP** (lô đã quá hạn trong `warning_day`
  ngày qua, KHÔNG phải sắp tới hạn) → cột Trạng thái không bao giờ ra "Trong hạn". Đừng sửa nhầm.
  Không migration (dùng lại quyền 100427 + 100839/840/841). Đã nghiệm thu: bấm thật trên trình duyệt,
  5 nhánh phân quyền qua HTTP, và đối chiếu bộ cột/bộ lọc + ngữ nghĩa cửa sổ ngày trên ERP dev.
  ⚠️ Merge có 2 xung đột đều do nhánh export-request vào trước, đã gộp cả 2 phía:
  `PrepickExtendRequestService` (thêm cả `PrepickApprovalRouteService` lẫn `PrepickConfigService`)
  và `subsystem-menu/finance.js` (giữ cả link màn mới lẫn 2 link Yêu cầu/Phiếu xuất giữ).
  ⚠️ `vendor` của worktree `.worktrees/gop-db` là SYMLINK sang checkout chính -> chạy PHP ở đó là
  nạp code nhánh khác, số liệu sai. Test code sau merge phải làm ở worktree có vendor riêng.
- finance-prepick-export-request → @junfoke → .plans/gop-db/finance-prepick-export-request/plan.md
  Trạng thái: **XONG BE + FE, ĐÃ VERIFY PLAYWRIGHT LUỒNG ĐẦY ĐỦ** (lập YCXG → duyệt 3 cấp → lập
  PXG → duyệt → sinh lô giữ hàng đúng). Nhánh `feat/finance-prepick-export-request` (cả 2 repo,
  tách từ `gop_db`) — **chưa commit**.
  Port CẶP màn "Yêu cầu xuất giữ" + "Phiếu xuất giữ" sang Tài chính / nhóm Giữ hàng, đủ 6 loại.
  ⚠️ Hai màn phải đi CÙNG ĐỢT: PXG duyệt là nơi DUY NHẤT sinh lô `prepick_details` mà 4 màn giữ
  hàng đã port đang tiêu thụ.
  ⚠️ Có đụng 2 thứ dùng chung: `AccountingStockService` (thêm `in_promotion`) và tách
  `PrepickApprovalRouteService` — đã test lại Gia hạn + Điều chuyển, lệch 0/300 phiếu.
  ⛔ Chưa nghiệm thu được loại 1-4: local 0 phiếu (4 bản dump ERP đều vậy, nghi nhánh code chết).
  **Vòng QA 04-05/09/2026 (#11302 · #11304 · #11308 · #11311 · #11312 · #11313)**: đã sửa 11 điểm —
  link YCXG mở tab mới; lịch chặn ngày quá khứ/quá trần; mẫu in đổi width px sang %; khối Lịch sử
  có Thu gọn/Xem lịch sử (cả 2 màn); gộp 2 tầng header "Số lượng"; bổ sung Mã KH/SĐT/Địa chỉ/ĐC
  giao hàng/Phòng ban ở màn Thêm; cột "Có thể giữ" mất số (buildQueryString sinh `product_ids=`
  không có `[]`); chặn SL đề nghị vượt tồn ngay lúc gửi duyệt; xoá lỗi cũ khi đổi hợp đồng; chặn
  tệp > 13 MB ngay ở FE. **Chưa chạy thử trên trình duyệt** (code chưa deploy lên dev).
  **Vòng QA 05/09 đợt 2 (#11314 · #11315)** — ô ĐVT: (a) select dùng `v-model` trên BẢN SAO dòng của
  `visibleRows` nên ĐVT chọn xong không vào `form.products`, payload vẫn gửi đơn vị cũ; (b) BE trả
  "Có thể giữ" theo ĐƠN VỊ GỐC, thiếu phép chia hệ số của ERP `updateInStock()`; (c) FE tự điền
  ĐVT đầu danh sách nên "không chọn" vẫn lưu được. Đã sửa cả 3, thêm nhãn ĐVT kèm hệ số, nạp lại
  danh sách ĐVT ở màn Sửa, và trừ tồn khuyến mại cho khớp bước Duyệt giữ hàng.
  **Vòng QA 07/09 (#11321 · #11322)** — #11321 (2 thùng duyệt ra 2 lọ) đã hết nhờ bản 05/09, kiểm
  trực tiếp trên dev. #11322 (bấm Sửa mất ĐVT) là lỗi MỚI do bản 05/09 lộ ra: select2 tự bắn
  `change` rỗng lúc options chưa nạp xong -> handler xoá sạch ĐVT/đơn giá của phiếu dù màn vẫn
  hiện "Lọ". Đã chặn ở `onUnitChange` (bỏ qua khi chưa có options + bỏ qua cú change lặp).
  **Vòng QA 09/09 (#11365 · #11368 · #11370)** — #11368: cấp duyệt của dòng từ chối nay đọc từ
  bảng lịch sử (trạng thái ngay trước hành động) thay vì gán vào dòng cuối có dấu duyệt.
  #11365: URL id sai -> toast tiếng Việt + đưa về danh sách (câu "Item Not Found!" nằm ở
  `Handler` dùng chung, chưa đụng). #11370: ẩn ô khoá rỗng (Hợp đồng/Địa chỉ), bỏ toast trùng với
  dòng trống của bảng; nút "Không duyệt" của ERP là bản sao nút Lưu (cùng `submit(3)`) nên KHÔNG
  port — chờ user trả lời QA.
  Bước tiếp: chạy migration `2026_09_03_000001_...` trên dev · gỡ 3 quyền tạm của emp 781 ·
  commit (chi tiết ở cuối Phase 13 của plan.md).
  Chi tiết + gotcha: plan.md | Tóm tắt: .plans/gop-db/finance-prepick-export-request/design.md
  Spec: docs/superpowers/specs/gop-db/2026-09-03-finance-prepick-export-request-design.md

- org-filter-locked-options → @namdangit → .plans/gop-db/org-filter-locked-options/plan.md
  Trạng thái: **XONG BE + FE, ĐÃ VERIFY PLAYWRIGHT trên :3002/:8003** (2026-08-24). Chưa commit.
  Mục tiêu: bộ lọc chung `V2BaseCompanyDepartmentFilter` (Công ty/Phòng ban/Bộ phận/Nhân viên) có công tắc 🔒 theo TỪNG ô để hiện cả mục đã khoá; mặc định vẫn chỉ hiện mục đang hoạt động.
  BE: `OrgOptionController` + route `GET /api/v1/org-options?type=company|department|part|employee` (trả full kèm `is_locked`); `Employee::getAll($onlyActive = false)` + `userProfile()` gọi `getAll(true)` → store.employees bỏ nhân sự đã nghỉ.
  FE: prop `keepLockedOptions` cho `V2BaseSelect`/`V2BaseSelectInModal`; component lazy load khi bật công tắc, KHÔNG cache danh mục khoá vào Vuex; tắt công tắc vẫn giữ giá trị đang chọn.
  Bước tiếp: commit lên `gop_db`.

- thiet-ke-lai-phan-quyen → @namdangit → .plans/gop-db/thiet-ke-lai-phan-quyen/plan.md
  Trạng thái: **PHASE 1 XONG — ĐÃ CÓ MÀN THẬT TRÊN `hrm-client` + `hrm-api`, VERIFY PLAYWRIGHT 1440** (2026-09-02). Chưa commit.
  Màn: `/admin/roles` (danh sách chức vụ) + `/admin/roles/{id}` (ma trận). Menu: Quản trị hệ thống → Phân quyền. 3 route cũ (`timesheet/setting/roles`, `.../add/{id}`, `human/roles`) đã redirect sang màn mới.
  **Mở rộng phạm vi so với kế hoạch cũ: phục vụ CẢ HRM LẪN ERP** (DB đã gộp). Danh sách gộp 120 chức vụ + cột `Hệ`; form ma trận nạp đúng bộ quyền theo `guard` của chức vụ — KHÔNG cho gán chéo guard (quyền `web` gán vào role `api` sẽ ăn bên HRM nhưng câm bên ERP vì spatie lọc guard), BE chặn bằng validate.
  **Mô hình chốt: 1 DÒNG = 1 `group`** (đo 3 cách trên 1.687 quyền: suy tên 848 dòng · suy+gộp 721 · theo `group` **288**). Ô gói nhiều quyền gốc thành nút `n/N` mở popup nên KHÔNG mất độ mịn: 285 ô checkbox + 200 ô popup. Bất biến `selfCheck()`: **1.687/1.687 quyền có chỗ, không rơi dòng nào**.
  Phân hệ quyền ERP: map `group_category` → registry (`Danh mục`→9 · `Kinh doanh`→23 · `Kho`→21 · `Kế toán`→25 · `Mua hàng`→20 · `CSKH`→24 · `Cấu hình hệ thống`→10). Quyền `api` `type = NULL` (78 quyền Chấm công) quy về type 1 ở BE — trước đó chúng KHÔNG hiện trên màn phân quyền cũ.
  `approve_scope`: `hrm-api/config/permission_scopes.php` khoá theo **permission ID**, khai sẵn **20 bản ghi** (17 quyền ERP + 3 bản HRM của chức năng đã chuyển: `Duyệt hợp đồng` 100041/1141, `TP duyệt đề nghị thanh toán` 100203/1154, `TP duyệt yêu cầu nhập hàng` 100984/1166). 122 quyền duyệt còn lại hiện nhãn `Toàn công ty` + viền đứt ⚠ "chưa khai".
  Verify 18 ca đo bằng số từ DOM/DB, 0 lỗi console — gồm cả **ca không có quyền** (matrix/lưu đều `403`) và **ca chặn chéo guard** (DB không đổi). 3 lỗi tự phát hiện & sửa: sticky chết do `#wrapper`/`.content-page` `overflow:hidden`; dải phân hệ đặt `top` nhầm trên `<tr>`; cột "Quyền đang có" lệch 82 vì đếm cả dòng trỏ quyền đã xoá.
  **[03/09/2026] Màn danh sách chức vụ chuyển sang CHUẨN LIST-PAGE** (1 file FE `pages/admin/roles/index.vue`, chưa commit): `V2BaseFilterPanel` (tìm nhanh + lọc *Hệ*) · `V2BaseDataTable` (title, columns, rowActions, `getNumericalOrder`, cột *Chức vụ* là link mở ma trận, `V2BaseBadge` cho *Hệ*) · `V2BaseButton` trong slot `#actions` · thêm `PageTitleMixin`, gỡ 138 dòng CSS `rl-*`. Sửa kèm lỗi có sẵn: `exportExcel` bỏ sót `guard` nên xuất Excel không theo bộ lọc Hệ. **KHÔNG bật sortable** vì `RoleService::index` chỉ nhận `keyword`+`guard`, sắp xếp cứng `roles.id desc`. ⚠️ Tự bắt 2 lỗi: `V2BaseBadge variant="secondary"` không hợp lệ (25 warning console → đổi `brand`/`muted`); `pageSize=25` không có trong `pageSizeOptions [5,10,20,50,100]` → đổi về 10. Verify Playwright 1440: 0 class `rl-*` còn lại, lọc/tìm/làm mới/phân trang/đổi số dòng/popup/2 nút hành động đều đúng, console 0 lỗi. **Còn treo:** chạy ca không có quyền bằng tài khoản thứ hai.
  **[03/09/2026] Màn phân quyền 1 chức vụ chuyển sang CHUẨN PHÂN HỆ** (3 file, chưa commit): tiêu đề bỏ khối tự chế `pr-head`, đẩy lên **topbar qua `PageTitleMixin`** (`pageTitle` + `pageTitleInfo`) · bộ lọc ma trận `pm-filter` → **`V2BaseFilterPanel`** (tìm nhanh + 3 lọc nâng cao bằng `V2BaseSelect`), tách *Mở tất cả/Thu gọn* và *Cấp hàng loạt* ra thanh `.pm-tools` riêng (thao tác, không phải điều kiện lọc) · nút *Lưu* từ `GrantedPanel` xuống **`V2Footer` sticky** (`submit_form` + `url-back`) — vì `V2Footer` không có disabled nên chốt `!dirty` chuyển vào trong `save()` (toast cảnh báo, không bắn request rỗng), gỡ nút chết + 2 prop `saving`/`dirty` ở `GrantedPanel` · **màu phân hệ về MỘT tông** (`SUBSYSTEM_HUE`, bỏ bảng 12 `HUES`). Verify Playwright 1440: 0 class `pr-*` còn lại · 7 dải phân hệ đo được **1 màu nền / 1 màu chữ / 1 màu viền** · cuộn hết xuống hở 16px **không bị footer đè** (`body.has-v2-footer` padding 66px) · bấm Lưu khi chưa sửa ra toast đúng (chứng minh footer gọi đúng `save()`) · tick 84→104 rồi bỏ tick về 84 · console 0 lỗi. **Còn treo:** chưa chạy POST lưu thật (tránh sửa quyền chức vụ 100123 trên DB local).
  **[03/09/2026] Bố cục màn phân quyền:** bộ lọc **trải trọn chiều ngang** (1195/1205px), panel *Quyền đã phân* **chia màn cùng cấp với bảng** — panel đưa vào slot `side` của `PermissionMatrix`, trong component tách `.pm-split` 2 cột (`.pm-col-main` = công cụ + bảng · `.pm-col-side` = panel), gỡ `.pr-grid`. ⚠️ Tự gây & tự bắt lỗi: `align-items: start` làm cột phải co bằng chiều cao panel → **`position: sticky` của panel mất khoảng dính**, đo được `panelTop: -469` khi cuộn; sửa thành `stretch`. Verify: 2 cột cùng `top=182` không chồng nhau · `thead` dính 60 · panel dính 96→64 khi cuộn · cuộn hết hở 16px không bị footer đè · console 0 lỗi.
  **[06/09 wrap up]** Kiểm lại sau khi session khác sửa thêm `pages/admin/roles/index.vue` + `_id.vue` (05/09 11:15–11:16, khả năng là Phase 2 `code`): **toàn bộ phần chuẩn hoá 2 màn vẫn nguyên và chạy đúng** — list-page 7 cột + phân trang 1–10/119, màn ma trận bộ lọc full width 1267/1277px, 2 cột cùng cấp, 7 dải phân hệ 1 màu, footer 2 nút; **0 class tự chế còn sót**, console 0 lỗi cả 2 màn. Vẫn **CHƯA COMMIT**.
  ⚠️ **Seeder chạy lại 2026-09-02**: quyền `api` 597 → 722. Seeder **xoá 3 quyền khách hàng cũ** (166/168/169) không tạo lại → **49 dòng gán của 12 chức vụ thành mồ côi** (Super admin 15, Admin_TPE 6…). Bộ thay thế là `Quản lý khách hàng` type 9 (id 1517–1522). **Chưa có migration chuyển đổi** — cần quyết định viết migration hay cấp lại tay.
  ⚠️ **2 việc RIÊNG vẫn treo, không phụ thuộc Phase 1:** (a) **89 quyền "ma"** — gate trỏ vào quyền không tồn tại trong seeder nên vĩnh viễn trả `false` (HRM 28/44 chỗ · ERP 61/120 chỗ), danh sách ở `.plans/gop-db/thiet-ke-lai-phan-quyen/gate-quyen-ma.md`; (b) seeder khai **trùng tên** `Quản lý danh mục tiền tệ` (id 1115 và 1117) + `Xem danh mục tiền tệ` (1116 và 1118) — DB hiện KHÔNG có `unique(name,guard_name)` nên seeder chạy lọt, nhưng 2 bản trùng vẫn hiện 2 dòng giống hệt trên màn.
  **[09/09/2026] ĐÃ COMMIT (tài liệu trước đó ghi "chưa commit" là SAI):** `hrm-api` `38f616746` "step 1" (51 file, +2555/−267) · `hrm-client` `b6b4b0763` "step1" (30 file, +2873/−56), cùng ngày 06/09 16:36, nhánh `permiss_manager` (con của `gop_db`), mỗi repo 1 commit ahead, cây sạch, **chưa push**.
  **[09/09/2026] PHASE 3 HOÀN THÀNH 13/13 TASK — 18 commit local, CHƯA PUSH.** `hrm-api` 14 commit (`38f6167..3afdefb9d`+) · `hrm-client` 4 commit (`b6b4b0763..45decc4df`), cây sạch cả 2 repo, nhánh `permiss_manager`.
  **Nghiệm thu:** `permission:audit` 720 quyền khai · **8/10 chốt sạch** (còn chốt1=21 quyền ma, chốt5=37 quyền duyệt — nợ có sẵn) · `phpunit tests/` **67/67** · **seeder chạy THẬT 2 lượt trên `hrm_erp`: checksum KHÔNG ĐỔI**, `api=720 web=965 role_has_permissions=15087` nguyên vẹn · `/admin/roles/8` = **176 quyền (16/135/16/9)** khớp tuyệt đối baseline · ca fail-closed đúng.
  **Kết quả cốt lõi:** seeder permission trước đây KHÔNG AI DÁM CHẠY (3 seeder Finance ghi thẳng trong docblock "KHÔNG chạy file đó" vì nó `delete()` sạch rồi tạo lại — từng làm 49 dòng gán của 12 chức vụ thành mồ côi) nay **chạy nhiều lần vô hại trên DB thật**. Kiến trúc: lớp cơ sở `PermissionSeeder` (7 luật kiểm TĨNH trước khi chạm DB, `updateOrInsert` theo id, không bao giờ xoá, cuối lượt BÁO quyền lạ chứ không xoá) + `TimesheetPermissionSeeder` (78 quyền) + `LegacyPermissionSeeder` (642 quyền/11 phân hệ) + orchestrator ~30 dòng. Chốt 2 hạ **2→0**, thêm chốt **8/9/10**, tất cả đã chứng minh "biết đỏ" bằng tiêm lỗi thật.
  **Gate nay hiểu CẢ `name` LẪN `code`:** 21 file BE (14 bản sao `isCurrentEmployeeHasPermission` + middleware + trait Finance) — KHÔNG gom 14 bản làm một vì chúng khác ngữ nghĩa thật (2 bản lọc `current_company_role`, 12 bản dùng `getAllPermissions()`). Reviewer quét **toàn bộ 1.685 quyền × 2 nhân viên × 2 nhánh dữ liệu**: gọi bằng tên vẫn true, bằng code cũng true, **LOST = 0**. Sau đó 78 hằng số `TimesheetPermission` đổi sang code, **không đụng 253 chỗ gọi**; đối chiếu 78/78 khớp DB.
  ⚠️ **LỖI NGHIÊM TRỌNG chỉ Playwright mới bắt được:** 12 task + >20 lượt review + 67/67 test xanh đều KHÔNG thấy — mở trình duyệt thì **menu Chấm công trả 404 cho người có đủ 78/78 quyền**. `components/menu.js` khai `isShow` bằng hằng số (nay là code), `middleware/checkPermission.js:51` chỉ so `.name`. Vòng sửa 1: 11 file. Re-review tìm thêm `pages/timesheet/dashboard/index.vue` tự định nghĩa hàm kiểm quyền riêng → **4 thẻ thống kê bị ẩn IM LẶNG**; vòng 2 chữa nốt + phòng ngừa `hub.js` (dùng chung 16 phân hệ). **Bài học: "vào được trang" KHÔNG chứng minh gate bên trong còn sống — phải đo nội dung render ra DOM.**
  ⚠️ **4 lỗi trong chính spec/plan, do review bắt:** (a) `MD5(GROUP_CONCAT(...))` bị MySQL cắt ở **1024 byte** trong khi chuỗi thật **302.131 byte** → mọi phép "khớp" trước đó là GIẢ, phải `SET SESSION group_concat_max_len` cùng kết nối; (b) chú thích "mảng PHP không cho trùng khoá" SAI — PHP nuốt im lặng dòng trùng id, đã đổi sang soi mã nguồn + **fail-closed khi mất khả năng soi**; (c) test mẫu dùng model không implement `Authenticatable`; (d) `expectsOutputToContain()` chỉ có từ Laravel 9.
  ⛔ **3 seeder Finance CỐ Ý KHÔNG đăng ký vào orchestrator** (ngược bản spec đầu, đã sửa spec+plan): `AdditionAccountingRequestPermissionSeeder` khai id **1177–1180**, mà trên DB đó là 4 quyền phân hệ Giao việc (`type=4`), **1179/1180 mỗi cái có 2 dòng gán thật** (role 18, 100124) → gọi vào là âm thầm đổi ý nghĩa quyền đang dùng. Cả 3 **không kế thừa `PermissionSeeder`** (kế thừa `Seeder` trơn + `const PERMISSIONS`) nên **10 chốt không bảo vệ chúng** — đây là đường DUY NHẤT còn lại có thể phá dữ liệu quyền. Xử lý đúng: cấp lại id theo dải finance **2700–2799** rồi mới đăng ký (task riêng).
  🔎 **[10/09/2026] NGHIỆM THU VỚI USER — 2 lỗi phát hiện thêm, ĐÃ SỬA** (`hrm-client` `1be777456` + `80ca37862`, nâng client lên 7 commit). User hỏi *"quyền Phân ca chưa thấy ở bản mới"*. Kết quả điều tra: **KHÔNG mất quyền** (78/78 quyền Chấm công đều trong ma trận, 3 quyền phân ca 412/413/414 đủ cả) nhưng **UI giấu mất**: BE gom 3 quyền thành 1 mục "Phân ca" 3 cấp → FE có quy tắc `>1 mục → nút n/N` nên *1 mục 3 cấp* rơi vào nhánh **checkbox trơn KHÔNG NHÃN, KHÔNG TOOLTIP**, mà lại nằm ở cột "Quyền khác" — cột duy nhất không suy được tên từ tiêu đề. Đo toàn hệ: **23 ô** kiểu này, 1 ô giấu nhiều cấp.
  ⚠️ **Lỗi thứ hai nghiêm trọng hơn: tự hạ cấp quyền âm thầm.** `itemPatch()` khi bật mục có phạm vi thì thêm cấp **hẹp nhất** + xoá các cấp còn lại. Ngữ nghĩa 3 quyền phân ca là **thang loại trừ** (gate xét công ty → phòng ban → bộ phận, trúng trước thì dừng), nhưng dữ liệu thật có **12/15 cặp (chức vụ × công ty) đang giữ CẢ 3 cấp** (Super admin 5 công ty, Admin_TPE, Admin_CN Sài Gòn/Vinh/Hải Phòng, HCNS_CN Sài Gòn) → một cú **"Cấp tất cả"** hạ quyền phân ca của họ **từ toàn công ty xuống chỉ bộ phận**, KHÔNG mở popup nên không ai biết. (Mở màn rồi bấm Lưu mà không đụng gì thì an toàn — có chốt `dirty`.)
  **Đã sửa theo 2 hướng user chốt:** (1) mọi checkbox đơn có **tooltip tên quyền gốc**, mục **nhiều cấp** đổi thành **nút `n/N`** mở popup chọn phạm vi — đo thật role 19: nút `3/3`, tooltip *"Phân ca — 3 cấp: Công ty · Phòng ban · Bộ phận"*; (2) **không tự hạ cấp** — bật lại mục ĐÃ có quyền thì giữ nguyên cấp đang có, chỉ mục CHƯA có quyền mới mặc định cấp hẹp nhất. Áp cho **cả hai** đường: `PermissionMatrix.itemPatch()` và `ItemListModal.toggle()` (nút bật-tất-cả trong popup — lỗ hổng thứ hai). `pickLevel()` giữ nguyên vì đó là user chủ động chọn bậc.
  🔴 **[10/09/2026] LỖ HỔNG CÓ SẴN phát hiện khi trả lời user — CHƯA SỬA, chờ quyết:** quyền **"Quản lý ca làm việc" (id 8)** chỉ có tác dụng ở FE (ẩn/hiện nút Thêm mới · Sửa · Khoá · Mở khoá · Xoá ở `/timesheet/timeworking/working-shift`, và chặn vào màn thêm/sửa ca). **BE KHÔNG kiểm quyền này ở đâu cả** — grep cả tên lẫn code trong `hrm-api` ra 0 chỗ, và nhóm route `Modules/Timesheet/Routes/api.php:80-89` chỉ có `auth:api`, không `checkPermission` → **ai đăng nhập được cũng gọi thẳng API để thêm / xoá / khoá ca làm việc**. Vi phạm 2 quy định CLAUDE.md ("FE không được coi là đã chặn"; route store/update/destroy/toggle phải gắn `checkPermission`). **KHÔNG do Phase 3** (Phase 3 không đụng route, `git log` xác nhận). Vá đề xuất: gắn `checkPermission:CA_LAM_VIEC_MANAGE` cho 3 route ghi, giữ route đọc; rà 9 chức vụ đang giữ quyền trước khi siết. (Lưu ý đính chính: hệ thống KHÔNG có quyền tên "Quản lý phân ca"; id 8 là quyền ĐỊNH NGHĨA ca làm việc, còn 412/413/414 là quyền XẾP nhân viên vào ca — hai việc khác nhau.)
  📌 **Quy tắc id quyền MỚI (chốt Phase 3):** `2000 + (type−1)×100`, rộng 100 (timesheet 2000–2099 · payroll 2100–2199 · human 2200–2299 · assign 2300–2399 …); dải **1565–1999 để trống** làm đệm cho nhánh chưa merge. Quyền cũ giữ nguyên id lộn xộn. `permission_scopes.php` nay khoá **hai kiểu**: 11 quyền HRM theo `code`, 17 quyền ERP theo `id`.
  **Việc PHẢI làm trước khi tách phân hệ tiếp theo:** (1) sửa **14 dòng Transformer** Training/Assign (`getAllPermissions()->pluck('name')` truyền xuống `canXxx()`) — chưa hỏng vì 0 dòng chạm quyền Chấm công, nhưng vỡ ngay khi đổi hằng số của chính 2 module đó; (2) **37 quyền duyệt chưa khai `approve_scope`** (chốt 5) — nợ DUY NHẤT cấp quyền RỘNG hơn dự kiến, ngược fail-closed.
  ⚠️ `.env` đã đổi `DB_DATABASE` `hrm_tpe` → **`hrm_erp`** (DB gộp). Dump an toàn 643K + bản `.env` cũ nằm trong scratchpad session.
  Spec Phase 3: docs/superpowers/specs/gop-db/2026-09-09-seeder-permission-cau-truc-design.md (mục **7b** = lý do không đăng ký Finance) · Plan: mục "Phase 3" cuối `.plans/gop-db/thiet-ke-lai-phan-quyen/plan.md` · Ảnh: `.plans/gop-db/thiet-ke-lai-phan-quyen/screenshots/2026-09-09-phase3-admin-roles-8.png`
  Lịch sử: **[09/09/2026] mở Phase 3** — brainstorm + spec + plan 13 task. 6 quyết định chốt: seeder phục vụ **cả cài mới lẫn đồng bộ DB đang chạy** · quyền DB không còn khai thì **chỉ BÁO, không xoá** · upsert khoá theo **`id`** (đo được: 590 id chung giữa `hrm_tpe` và `hrm_erp`, **0 id lệch tên**), `code` là khoá duy nhất thứ hai · **1 file seeder / phân hệ** đặt trong module · id quyền mới theo công thức **2000 + (type−1)×100**, chừa trống 1565–1999 làm đệm · gate nhận **cả name lẫn code**, sửa **cả 14 bản sao + middleware + trait Finance + 3 hàm FE**, KHÔNG gom 14 bản (2 bản lọc `current_company_role`, 12 bản dùng `getAllPermissions()` — khác ngữ nghĩa thật).
  Quyền cũ **giữ nguyên 100%** đợt này (user tự rà lại theo từng màn sau); ngoại lệ duy nhất là bỏ 2 dòng khai trùng tiền tệ 1117/1118 — không bỏ thì seeder không chạy nổi.
  ⚠️ 3 cái bẫy đã ghi vào spec/plan: (a) `PermissionAuditService::declaredPermissions()` đọc seeder bằng **regex `Permission::create`** → tách file mà quên sửa là báo 78 quyền ma GIẢ, mốc kiểm chứng "722 quyền khai, chốt 1 vẫn 21"; (b) 644 quyền legacy phải khai thêm **`code` + `type` theo dòng**, không thì DB cài mới có `code = NULL` (unique cho phép nhiều NULL → **không nổ**, chỉ âm thầm chết mọi gate theo code); (c) bỏ `delete()` phải làm **cùng lượt** với tách file, không thì ai chạy seeder cũ sẽ xoá sạch 78 quyền Chấm công.
  ⚠️ `.env` đang trỏ `DB_DATABASE=hrm_tpe` — DB HRM thuần (593 quyền, **chưa có cột `code`**). DB gộp đúng là **`hrm_erp`** (965 web + 720 api, code backfill đủ). Task 1 đổi `.env` + `mysqldump` 2 bảng trước khi chạy gì.
  Số nền đo 09/09: audit 722 quyền khai · chốt 1 = 21 quyền ma (Assign 8 · Decision 6 · Training 5 · Human 2, **Chấm công 0**) · chốt 2 = 2 · chốt 5 = 37 · phpunit **7/7 xanh**. Còn dùng chuỗi tên quyền: BE Assign 235 · Training 156 · Human 79 · Payroll 35 · Decision 33 · Rice 16 · Finance 5; FE 365 chỗ.
  Spec Phase 3: docs/superpowers/specs/gop-db/2026-09-09-seeder-permission-cau-truc-design.md · Plan: mục "Phase 3" cuối `.plans/gop-db/thiet-ke-lai-phan-quyen/plan.md`
  Bước tiếp: user rà màn thật → chốt hình → viết e2e tự động; rà gate 122 quyền duyệt để khai `approve_scope`.

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
  Trạng thái: **XONG PHASE 0-13** (2026-09-04) — Phase 10 vá QA redmine 11094/11149/11150/11151/11152/11154,
  Phase 11 bỏ tab preset (1 màn = `all` của ERP, nút duyệt theo quyền), Phase 12 rà màn Phiếu hủy
  theo quy tắc chung (bỏ tự kéo số về trần, duyệt xong về danh sách, nút In trắng, 4 icon ⓘ),
  Phase 13 vá QA redmine 11295/11296.
  Nhánh `feat/finance-prepick-cancel`. Port 2 màn `Yêu cầu hủy hàng giữ` + `Phiếu hủy hàng giữ` sang
  Tài chính / nhóm Giữ hàng — **màn đầu tiên của HRM ghi tồn kho thật** (duyệt = trừ FIFO
  `prepick_details` + ghi `prepick_logs`). 2 migration (2 bảng lịch sử).
  **Tài liệu bàn giao ĐỦ CẢ 2 MÀN** — mỗi màn 1 bộ 3 file: màn Yêu cầu hủy hàng giữ (05/09)
  `SRS - Yeu cau huy hang giu.docx` + `HDSD_Yeu cau huy hang giu.docx` + `testcase.xlsx`;
  màn Phiếu hủy hàng giữ (09/09) `SRS - Phieu huy hang giu.docx` (33 trang) +
  `HDSD_Phieu huy hang giu.docx` (26 trang) + `testcase - Phieu huy hang giu.xlsx` (111 TC).
  ⚠️ GOTCHA màn Phiếu hủy khác màn Yêu cầu: chỉ 2 cấp phạm vi (không có cấp phòng ban),
  không có Sửa/Xóa, và có 2 lối vào màn lập phiếu.
  Bước tiếp: user bấm tay trên dev + test bằng tài khoản `Quản lý giữ hàng` không phải Super admin;
  giữ 6 bảng `bak_*_20260815` tới lúc đó. BA đọc duyệt 3 tài liệu màn Phiếu hủy.
  Chi tiết + gotcha: plan.md

- finance-product-import-direct-transfer → @junfoke → .plans/gop-db/finance-product-import-direct-transfer/plan.md
  Trạng thái: **XONG PHASE 0-9 + ĐỦ 3 TÀI LIỆU BÀN GIAO** (2026-09-03) — Phase 8 vá 9 bug QA redmine 11092-11108,
  Phase 9 bỏ tab preset; 28/08 sinh testcase 157 TC + HDSD 29 trang; 03/09 bổ sung SRS 45 trang và
  sửa lại TC/HDSD mục ô Số lượng theo hành vi mới (lọc ký tự ngay khi gõ, không còn báo đỏ).
  Port màn "Phiếu chuyển hàng nhập thẳng" sang Tài chính / nhóm Điều chuyển; 1 migration (bảng lịch sử).
  Tài liệu: `testcase - Phieu chuyen hang nhap thang.xlsx` | `HDSD_Phieu chuyen hang nhap thang.docx` |
  `SRS - Phiếu chuyển hàng nhập thẳng.docx` (13 chức năng FR-01..FR-13, 17 quy tắc nghiệp vụ)
  ⚠️ GOTCHA: bản in phiếu bị tràn khối ký ra ngoài khung giấy; ô rỗng danh sách còn hiện dấu `—`.
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

- khai-quy-che-cau-hinh → @namdangit → .plans/gop-db/khai-quy-che-cau-hinh/plan.md
  Trạng thái: **Slice 1 (Công nợ versioning) + Slice 2 (tổng quát hoá + 2 tab scalar chietkhau/kythuat)
  + Slice 3a (hạ tầng scope `global` → bảng `configs` singleton, chứng minh qua tab baogia ở tầng service/cron)
  ĐỀU ĐÃ CODE + test XONG. Final whole-branch review (opus) từng slice CLEAN/SẠCH, không finding chặn** (2026-09-14).
  Chờ USER QA trình duyệt + quyết định commit (git chưa được uỷ quyền).
  Test Slice 3a: 4 suite xanh — GlobalScope 4/4 · Congno 14/14 byte-identical · Scalar 5/5 · Registry 6/6 (CR=0 cả 8 file).
  Slice 3a thực thi bằng SDD, ledger: `hrm-api/.superpowers/sdd/2026-09-14-khai-quy-che-slice3a-global-scope-infra/progress.md`.
  Kiến trúc: `RegulationTabRegistry` (registry-driven, per-field store config/company) + `RegulationConfigService` generic
  theo `tab_key` + scope (company→`companies`/`company_regulation_histories`; global→`configs`/`regulation_config_histories` MỚI)
  + controller/route generic `regulation-config/{tabKey}` (mới cho scope company) + FormRequest rule động.
  Slice 3a thêm: 2 migration (3 cột `companies` cho hanghoa/dieukhoan 3b + bảng `regulation_config_histories`).
  Backlog Slice sau (từ review, non-blocking): [Slice 3b] snapshot-wipe — global version ghi TRỌN 10 field config,
  field thiếu = null xoá cột → controller/FE 3b PHẢI round-trip đủ 10 field config; getTabConfig trả kèm `payload`
  cho modal hẹn; field non-API bị drop âm thầm ở modal hẹn; congnoLoading race.
  Data-hygiene ĐÃ XONG (user chốt "làm như ERP có"): đã `UPDATE configs SET customer_register_expiry=30`
  (khớp ERP ConfigSeeder); 5 cột nullable vốn đã NULL đúng ERP-fresh, is_equipment=1 giữ nguyên.
  Đã fix test (backup đủ 10 cột store=config) nên không làm bẩn DB thêm.
  Spec hoàn thiện 13 tab: `docs/superpowers/specs/gop-db/2026-09-14-khai-quy-che-hoan-thien-cac-tab-design.md`.
  Plan Slice 2: `docs/superpowers/plans/gop-db/2026-09-14-khai-quy-che-slice2-generalize-scalar-tabs.md`.
  Plan Slice 3a: `docs/superpowers/plans/gop-db/2026-09-14-khai-quy-che-slice3a-global-scope-infra.md`.
  **Slice 3d — tab `khac` (scope PHÒNG BAN) XONG BE + FE** (2026-09-14): thêm scope `department` (ghi thẳng 3 cột
  `departments` risk_fund/profit_percent/max_value_contract của 1 phòng ban; lịch sử → `regulation_config_histories`
  scope_type='department' scope_id=department_id, KHÔNG dùng company_regulation_histories vì cột buộc company_id).
  BE: `RegulationConfigService` (SCOPE_DEPARTMENT + storeForScopeType + applyVersion/applyDueVersions/updateVersion/
  recomputeDiffChain nhánh department) · controller (`departments()` endpoint + resolveScopeId/refreshScopeId/
  assertDepartmentInCompany, tab scope=department đọc/ghi theo department_id, gate PB thuộc công ty hiện tại) ·
  route `regulation-config-departments` · FormRequest thêm `department_id`. Test: RegulationKhacDepartmentTest 3/3 +
  registry unit (khac=department scalar) — full MasterData suite 61 passed. FE: `index.vue` fetchTab/applyTabToModel/
  onSave/curTabIsApi/watch curGroup scope-aware (DEPT_API_TABS=['khac'], gửi department_id GET+POST, đổ vào
  model.department.groups); picker phạm vi thay mock SCOPE_UNITS bằng phòng ban THẬT (endpoint mới, selectedDeptId int,
  re-fetch khi đổi phòng); `data.js` nhãn khac khớp registry BE. CR=0 index.vue+data.js.
  **Slice 3d — tab `themquy` (ladder, scope PHÒNG BAN) XONG BE + FE** (2026-09-14): `departments.conditions_quarter_bonus`
  (json bậc thang GIỮ ĐÚNG khoá ERP money_from/money_to/percent + comparator) + `rate_reward_progressive_tp/tbp/nv`.
  **Ruling B**: lịch sử → `RegulationConfigHistory` scope=department (KHÔNG dual-write bảng audit ERP
  `department_condition_quarter_bonus_histories` — test assert count=0). BE: registry themquy (type=json input='ladder',
  item_rules percent 0-100, 3 decimal) + FormRequest `validateQuarterBonusLadder` (per-row from<to + ∑tp/tbp/nv=100).
  FE `index.vue`: DEPT_API_TABS=['khac','themquy']; verbar inline "Ngày áp dụng" + pending-queue cancel-only (ẩn nút sửa
  vì ladder không dùng modal hẹn); bảng bậc thang V2BaseSelect(ladderFromOps/ToOps)+V2BaseCurrencyInput(money rỗng=INF)+
  V2BaseInput%; addLadderRow/removeLadderRow; applyTabToModel/collectTabValuesFromModel nhánh themquy (ladder+progressive);
  ladderRateValid tô đỏ #dc2626 + chặn onSave; cancelPending nhận cả DEPT_API_TABS. `data.js` mock ladder → object khoá ERP.
  Test: RegulationThemquyDepartmentTest 3/3 + registry unit `registers_themquy_as_department_ladder_tab` — MasterData suite
  65 passed. CR=0 index.vue+data.js.
  **Slice 3d — tab `hoahong` (GRID per-dòng, scope PHÒNG BAN) XONG BE + FE (2026-09-15) → Slice 3d ĐÓNG**:
  tab phức tạp nhất, mỗi dòng lưới = 1 bản ghi `regulations` (objectable_type App\Model\Common\Department,
  objectable_id=department_id), KHÔNG staging version — 2 cột nullable effective_date/status ghi THẲNG `regulations`.
  BE: migration đã chạy; registry SHAPE_GRID 18 field metadata (loại khỏi mọi helper scalar); controller show() rẽ
  getGridConfig + storeGridRow/updateGridRow/destroyGridRow (gate currentCompanyId + assertDepartmentInCompany, ownership
  403, actorId=auth()->id()), route version rẽ 404 cho tab grid; RegulationCommissionRowRequest (condition_sale_type
  required_if type=1; value_end gt start; ∑department/part/employee=100 VÀ ∑*_bonus_contract=100; conditions_commissions
  [from_day<to_day, receive_percent 0..100]); ScheduleRegulationVersionRequest guard isGridTab; service statusForEffective/
  fillGridRow (sale_type=0 khi type≠1, after_commission_type ép=1)/presentGridRow (is_applied/is_pending/status_text)/
  getGridConfig/CRUD/applyDueGridRows (cron flip pending→applied theo dòng); history buildGridHistoryDiff numeric-aware
  TRƯỚC save (đã FIX bug false-diff decimal Laravel-8). Routes POST/PUT/DELETE `regulation-config/{tabKey}/grid[/{rowId}]`.
  Test: RegulationHoahongGridTest 10/10 + registry unit `registers_hoahong_as_department_grid_tab` — full MasterData suite
  **76/76**. CR=0 (4 file BE LF nguyên trạng). NOT committed (rule gop_db).
  **FE grid wiring hoahong XONG (2026-09-15)** — đủ 6 bước bàn giao: GRID_DEPT_TABS=['hoahong'] (ngoài DEPT_API_TABS);
  fetchGridTab GET `.../hoahong?department_id=` → applyGridConfig {fields→gridFieldOptions, rows OBJECT}; tbody row-object
  (gridOptLabel/gridNetText/fmtPercent/fmtDate + pill is_pending/is_applied, cột Thao tác gate canEditRegulation); modal reg
  bind 18 key BE + effective_date (condition_sale_type chỉ khi Number(condition_type)===1, condition_compare_type disabled
  'Giá net', conditions_commissions sub-table); openReg/saveReg (guard 2 nhóm ∑=100, POST/PUT `.../grid[/{id}]`, map 422
  inline)/deleteReg ($confirm→apiDelete `.../grid/{id}?department_id=`); import V2BaseCheckbox. **Ruling**: KHÔNG gọi
  markFormSaved (trang KHÔNG dùng unsavedChangesMixin — sibling scalar-tab onSave cũng không). CR=0 index.vue+data.js (LF).
  Chưa QA trình duyệt (code chưa deploy dev).
  **Slice 3f — Lịch sử quy chế THẬT (①A) + Dirty-guard rời trang (②A) XONG (2026-09-15) → Slice 3f ĐÓNG**:
  ①A thay mock `HIST` ở FE bằng endpoint BE thật `GET /v1/master-data/regulation-config-history?scope=company|department[&department_id=]`
  (gate `checkPermission:Cài đặt cấu hình` + `guard()` 403 + `currentCompanyId()`; scope ∉ {company,department}→422;
  department bắt buộc department_id + assertDepartmentInCompany). `RegulationConfigService::getHistory()` GỘP 4 nguồn/scope,
  sort created_at desc (tie-break `_seq` ổn định vì PHP 7.4 usort không stable), cắt 50 SAU sort, trả MẢNG VỊ TRÍ 6 phần tử
  `[timeStr, whoName, contentStr, scopeAppliedName, noteStr, isScheduledBool]`. Nguồn: company =
  `regulation_config_histories`(company scope_id + global 0) + `company_regulation_histories`(company_id) +
  `regulation_scheduled_versions` pending(company+global); department = `regulation_config_histories`(department) +
  `regulation_histories`(department_id, logs json) + scheduled pending(department). Format: time `d/m/Y H:i`,
  who="code - fullname" (join employees↔employee_infos 1 query, KHÔNG N+1), content "{label}: {old} → {new}" nối "; ",
  number_format QUỐC TẾ, bool→Có/Không, null/''→"—", >3 field → 3 + " …(+N)", scheduled prefix "Hẹn phiên bản mới — ".
  ②A: `index.vue` dùng `unsavedChangesMixin` (unsavedSnapshotSource→this.model), `guardLeaveDirty()` $confirm khi đổi
  tab/scope/phòng ban lúc đang sửa → xác nhận thì `revertCurrentTab()` re-fetch bỏ edit dở RỒI `markFormPristine()`
  (KHÔNG markFormSaved — cảnh báo vẫn bật cho lần sửa sau); reset baseline sau onSave/onCancel/saveVer/cancelPending/
  saveReg/deleteReg; beforeRouteLeave built-in. `data.js` gỡ export HIST + SCOPE_UNITS (CURRENT_COMPANY giữ, còn dùng).
  Review độc lập (opus) APPROVED không blocker (2 MEDIUM + 3 LOW + 2 NIT) → fix round 1 xử M1(sort stable)/M2(revert thật)/
  L1($type company field)/L2(null-safe created_at)/L3(3 test HTTP 403/422). Test: RegulationHistoryTest 6 (3 service + 3 HTTP)
  → full MasterData suite **82/82 PASS**. CR=0 cả 6 file (4 BE + 2 FE). NOT committed (rule gop_db).
  **FEATURE KHÉP VỀ MẶT CODE**: đủ 14 tab đều BE (registry 14 key) + FE (API_TABS 11 company + DEPT_API_TABS khac/themquy +
  GRID_DEPT_TABS hoahong) + test — KHÔNG còn tab mock. Slice 3b/3c (mixed/json/subtable) đã gộp vào wiring registry chung
  (đóng cùng 3d), Slice 3e (rà quyền + số quốc tế + line-ending + review cuối whole-branch) đã `[x]` hết. Lịch sử thật (①A)
  + dirty-guard (②A) có đủ.
  Chưa làm (đều NGOÀI PHẠM VI theo spec mục 11 — YAGNI): bước duyệt phiên bản (change_approver), diff JSON per-dòng,
  lưu version_id trên chứng từ, version-hoá 2 field fixed (Thuế vận tải/Ngày khai báo công nợ đầu kỳ), due_configs matrix.
  Backlog nhỏ non-blocking (LOW/NIT): comment double-limit-50, test HTTP cap-50/join>3 ở tầng service.
  Bước tiếp: user QA trình duyệt toàn màn (chưa deploy dev) → quyết định commit/merge về gop_db.
  --- (lịch sử) ---
  **UI mock XONG · MAPPING ERP XONG · đang brainstorm cơ chế "hẹn ngày áp dụng"** (2026-09-09).
  Gộp 1 màn HRM `/master-data/regulation-config` 3 miền cấu hình/quy chế ERP: (1) Cấu hình chung công ty
  (11 nhóm form), (2) Quy chế kinh doanh theo phòng ban (hoa hồng/lũy tiến/khác), (3) MỚI: "hẹn ngày áp dụng".
  Hướng A (port bảng ERP có sẵn). UI đã xong (mock): `pages/master-data/regulation-config/index.vue` + `data.js`
  + menu master-data. **Mapping ERP (đã dò 2026-09-09)**: Miền 1 = `configs` (singleton toàn hệ thống) +
  `companies`/`company_rule_commissions` (company_id) + `due_configs`/`company_due_configs` (công nợ); Miền 2 =
  `regulations` (polymorphic objectable_type Department/Part) + cột trực tiếp trên `departments`.
  ⚠️ **Phát hiện then chốt**: ERP KHÔNG có versioning theo ngày hiệu lực — chỉ overwrite + audit-log diff
  (`company_regulation_histories`, `regulation_histories`, `due_config_histories`). → "Hẹn ngày áp dụng" là phần
  HRM thiết kế mới hoàn toàn. Bước tiếp: chốt schema versioning → viết spec đầy đủ → duyệt → code (slice đầu:
  Cấu hình chung). Spec: docs/superpowers/specs/gop-db/2026-09-09-khai-quy-che-cau-hinh-design.md

- xuat-ban-hang-muon → @namdangit → .plans/gop-db/xuat-ban-hang-muon/plan.md
  Trạng thái: **CODE DONE Phase 1 (SDD) — FINAL REVIEW CLEAN, chờ USER QA + quyết định commit** (2026-09-04). Review tổng nhánh ra 1 defect D1 (escalation vượt hạn mức không kích hoạt) → đã fix (BE tự tính giá trị phiếu server-side `computeAmounts()` + persist cột `sum_amount_*`) → scoped re-review PASS. Port luồng "xuất bán
  hàng mượn" ERP → HRM (Module Finance) cho cả 3 loại HĐ (Firm/WrService/HĐ mới `hrm_quotation_id` — HĐ mới đi
  chung nhánh Firm). **Phase 1** = phiếu YC xuất bán hàng mượn (`BorrowSellRequest`, `PYCXBHM`), KHÔNG hạch toán/tồn.
  Execute qua subagent-driven (ledger `.plans/gop-db/xuat-ban-hang-muon/sdd/progress.md`). **XONG toàn bộ 13 task**:
  T1–T8 BE, T9 api.js, T10 list, T11a BE 2 endpoint nguồn + siết canBorrowSell (fix R-T11a-FIX-1), T11b FE create
  page (create.vue + 2 picker modal + BorrowSellRequestForm), T12 FE detail/print/deny/history, T13 unit test
  Calculator PASS + doc. Mọi task review SPEC PASS / QUALITY APPROVED, KHÔNG load-bearing defect. **CHƯA commit** (chờ user).
  Còn lại: (1) review tổng nhánh (broad whole-branch, model mạnh) — đang chạy; (2) **USER QA trên browser**:
  đăng nhập từng cấp quyền tạo Firm/WrService/HĐ mới, vượt/không vượt hạn mức (TP→BGD), duyệt/từ chối, in,
  xác nhận `account_details`/tồn KHÔNG đổi + regression type-9 (Nhập bán mượn trả lại); (3) hỏi user commit.
  Footprint chưa commit — hrm-api: `Modules/Finance/{Entities/BorrowSellRequest,Services/BorrowSellRequest,
  Http/Controllers/V1/BorrowSellRequestController,Http/Requests/BorrowSellRequest,Transformers/BorrowSellRequestResource,
  Tests/Unit/BorrowSellRequestCalculatorTest}` + `Routes/api.php` + hợp nhất type-9 (xoá
  `Entities/ProductImportRequest/BorrowSellRequest.php`, sửa `ProductImportRequestService.php`,
  `Entities/Concerns/ChecksEmployeePermission.php`); hrm-client: `pages/finance/borrow-sell-requests/*` +
  `components/subsystem-menu/finance.js`.
  **Phase 2** = `BorrowSell` (phiếu BÁN thực tế, `PXBHM-`) + hạch toán bán: **CODE DONE 14/14 task (SDD) + final whole-branch review XONG (SHIP-with-nits) đã adjudicate** (2026-09-07). Ledger `sdd/progress-phase2.md`, report `sdd/final-review-report.md`. BE đã commit 10 commit (c562527e0^..8b9e77bd6). Final review: 0 Blocker/0 High/1 Medium(F1)/3 Low. **F1 FIXED** (updateWarehouse nhánh WrService bổ sung cộng `exported_qty` cấp-2 lồng — map 3 FQN→bảng + increment atomic + unit test 4/4; Firm sub-claim = false-positive nhánh tabs/KM đã bỏ) — **CHƯA commit** (2 file: BorrowSellService.php + BorrowSellStoreTest.php). F2 park (FU-6 comment sai vị trí gate), F3/F4 đóng by-design. Delta additive objectable_id/type (uncommitted). FE uncommitted (quy ước Phase 1 FE): `pages/finance/borrow-sells/**` + nút "Lập phiếu bán" + menu link. QA V1-V8 PASS. Bước tiếp: **chờ user cho phép commit BE fix F1 + QA browser** (FE giữ uncommitted; Phase 1 BE staged không đụng).

- product-import-list → @namdangit → .plans/gop-db/product-import-list/plan.md
  Trạng thái: **CODE DONE Phase 1-4 — chờ user QA** (2026-08-28). Bổ sung cho màn **Phiếu nhập hàng**
  (`/finance/product-imports`, `Modules/Finance`): (1) **bộ quyền 4 cấp** hiện trong màn Phân quyền —
  id **1543-1546** guard `api` group "Phiếu nhập hàng" (tổng công ty / công ty / phòng ban / bộ phận),
  đã thêm id 1546 vào `PermissionsTableSeeder` + chèn thẳng 4 dòng vào DB gộp (trước đó 1543-1545 có trong
  seeder nhưng CHƯA có trong DB nên nhóm quyền không hiện); (2) **bộ lọc** viết lại mirror màn Phiếu xuất
  hàng — `V2BaseCompanyDepartmentFilter` (công ty/phòng ban/bộ phận/người lập) + loại + trạng thái + khoảng
  ngày lập + keyword; (3) **tuỳ chỉnh cột** (`ColumnCustomizationModal` table `finance_product_imports`) +
  cột **Người lập** (`creator_name`).
  BE: `ProductImport` thêm nhánh **bộ phận** vào `applyViewScope()`/`canView()` (`isPartManager`/`managePartIds`
  mirror `ProductImportRequest`); `searchByFilter()` nhận thêm company/department/part/employee/start_date/end_date
  + `->with('creator.info')`; route mới `GET finance/product-imports/filter-options`. `php -l` sạch.
  **Phase 5 (2026-08-28)**: BỎ role-18 bypass — trước đó `canView()` + `isBigBoss/isBoss/isManager/isPartManager`
  có vế `currentEmployeeIsSuperAdmin()` khiến role 18 (DNS admin) tự thấy hết, song song với 4 quyền → user
  chốt bỏ, để 4 quyền điều khiển hoàn toàn. Vẫn GIỮ trait `ChecksEmployeePermission` làm hàm đọc quyền (query
  theo TÊN quyền mọi guard — ĐÚNG cho gop_db, khớp với FE `hasAPermission`; KHÔNG đổi sang helper global
  `isCurrentEmployeeHasPermission` vì nó bị bug model_type='App\Employee' trên DB gộp).
  ⚠️ Hệ quả: **role 18 KHÔNG còn tự thấy hết** — phải gán "Xem phiếu nhập hàng theo tổng công ty" qua màn
  Phân quyền (nhóm "Phiếu nhập hàng" nay đã hiện). Còn giữ 2 nhánh nghiệp vụ hợp lệ ngoài 4 quyền: kế toán
  kho cùng công ty (chi tiết) + người tạo phiếu (`created_by`).
  Bước tiếp: user QA trên UI (lọc theo cấp tổ chức, tuỳ chỉnh cột, cột Người lập) + gán 4 quyền cho các role
  qua màn Phân quyền.

- de-nghi-nhap-kho → @namdangit → .plans/gop-db/de-nghi-nhap-kho/plan.md
  Trạng thái: **P1 (Backend) XONG · P2 (Frontend) XONG — chờ user QA** (2026-08-25). Port màn **Đề nghị nhập kho** (ERP
  `WarehouseImportRequest`, mã `PDNNK`) — tầng 2 luồng nhập kho 3 tầng (cha `ProductImportRequest`/PYCNH đã port).
  Scope A: chỉ chứng từ (Lập từ YCNH + list + chi tiết + Thủ kho duyệt + Từ chối + Hủy + In); KHÔNG đụng tồn/hạch toán (tầng 3 tách sau).
  Mirror sibling **Đề nghị xuất kho** (Module Assign) sang **Module Finance**. Bộ status WIR riêng (1..7),
  đổi status cha YCNH inline theo ERP: lập→7, gửi→1, thủ kho duyệt→4, từ chối→7, hủy→6 (giết YCNH — đúng ERP nhập).
  GÁC tầng 3: tabs cha-con, `warehouse_exported_qty` type 4/9, `WarehouseImportRequestDetailAccounting`, tồn/sổ.
  Spec: `docs/superpowers/specs/gop-db/2026-08-25-de-nghi-nhap-kho-design.md`.
  Bước tiếp: **user QA trên trình duyệt** (login Kế toán kho lập/sửa/hủy; thủ kho duyệt/từ chối) rồi đóng feature (tầng 3 tách sau). FE đã xong: 4 trang `pages/finance/warehouse-import-requests/` + rewire nút ở màn YCNH.

- nhap-ban-tra-lai-hd21 → @namdangit → .plans/gop-db/nhap-ban-tra-lai-hd21/plan.md
  Trạng thái: **Phase 1 CODE DONE · Phase 2 SPEC XONG — chờ user review spec** (2026-08-27). Phase 2 = màn **Phiếu nhập hàng
  (ProductImport)** HRM (chưa từng có bên HRM), khung generic mở rộng mọi loại nhập, đợt này xử lý type 4 loại 21.
  Spec Phase 2: `docs/superpowers/specs/gop-db/2026-08-27-product-import-hrm-design.md` (2 đường vào: A qua kho ERP redirect / B nhập thẳng).
  Phase 1 BE+FE xong: migration `emplement_contract_*`,
  `searchForImportType`/`dataForSaleReturn`/`guardBusinessRules`/`fillFromExportRequest` nhánh loại 21, modal +cột "Số HĐ".
  Verify bằng DB smoke test dữ liệu thật (phiếu 35676/HĐ13). CHỜ: chưa có phiếu xuất loại-21 status=5 để E2E store()→duyệt TP.
  Mở luồng **Nhập hàng bán trả lại** (import type 4 `BAN_TRA_LAI`) cho hàng bán theo **HĐ HRM loại 21** (`XUAT_BAN_HOP_DONG`),
  bắt chước nguyên quy tắc loại **xuất bán hãng 14 ERP**, chỉ đổi nguồn HĐ ERP (`firm_contract`) → HĐ HRM (`Contract` polymorphic).
  Đã xác nhận: HĐ 21 có đủ tương đương type 14 (`support_accounting` chung bảng `firm_support_accountings`,
  quyết toán qua `Contract.status` 11/12, dòng `product_export_request_tab_products` có `qty/exported_qty/returned_qty`);
  khác: HRM PER không có status 13 (loại 21 hoàn tất = status **5**), query quyết toán dùng khóa thường.
  **Phase 1** = nửa trước (lập+validate+duyệt giá), tận dụng code type-4 đã port. **Phase 2** = màn ProductImport (nhập kho thực+returned_qty+hạch toán) — SPEC XONG.
  **PENDING**: type 9 (bán mượn trả) loại 21 — chờ phiếu xuất bán hàng mượn loại 21.
  Bước tiếp: user review spec Phase 2 → writing-plans → code (Entities → Service → hạch toán → Controller/FE → nút entry → E2E).

- hop-dong-xuat-hang → @namdangit → .plans/gop-db/hop-dong-xuat-hang/plan.md
  Trạng thái: **HẠCH TOÁN XUẤT HÀNG (task 9.15) — BE DONE + TEST E2E PASS** (2026-08-20, nhánh `hop-dong` con của `gop_db`).
  Phiếu xuất hàng HĐ HRM loại **20** (xuất sản xuất) + **21** (xuất bán) khi Hoàn tất (status=1): trừ tồn kế toán+vật lý,
  tính giá vốn FIFO (ghi đè export_price), ghi sổ `account_details` bám sát ERP "bán hàng theo hãng".
  - Loại 21: đủ 8 cụm (doanh thu 1311/5111/33311, giảm trừ 5213/33311/1311, giá vốn **Nợ632/Có155** — dùng 155 thay 1561,
    thưởng 5211/35241, TNCN 35241/3335, hoa hồng tháng/quý 6411/35241, quỹ rủi ro 6411/35241).
  - Loại 20: chỉ giá vốn **Nợ1541/Có1561**; auto sinh phiếu nhập cha **Nợ155/Có1541** (khép vòng WIP→thành phẩm).
  - **Accuracy gate**: đối chiếu phiếu bán-hãng ERP thật (PXH id=4) → khớp TỪNG ĐỒNG. Cost engine khớp 6 ca thật (P2).
  - **E2E**: dựng data mới (kho+tồn+BOM), chạy trọn `ProductExportService::createFromWarehouseExport(status=1)` → cả 2 loại cân đối ΣNợ=ΣCó lệch 0.
  Files: `Modules/Assign/Services/{ProductExportPostingService,WarehouseExportAccountingService,ProductExportService,ContractParentImportService}.php`,
  `Modules/Finance/Entities/Account/{AccountDetail,AccountDetailRef}.php`.
  **HOÃN** (tách feature): DebtRemindersJob (cần model `ContractStateDelivery` HRM chưa có), hạch toán bốc xếp (arrange_delivery).
  Bước tiếp: FE màn tạo/hoàn tất phiếu xuất hàng (2 nút Lưu nháp status=3 / Hoàn tất status=1 → `POST /assign/warehouse-exports/{id}/product-exports`) — CHƯA có.

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

- bom-list-list-page-standard — chuẩn hoá màn Danh sách BOM List (`/assign/bom-list`) theo skill `list-page` → @khoipv → .plans/gop-db/bom-list-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 6/6 mã màu trạng thái nằm ngoài bảng 9 mã chuẩn quy về đúng nhóm; thêm `isCanEdit()`/`isCanDelete()` khớp guard của service; whitelist `SORTABLE_COLUMNS` + chốt `id desc` (trước `orderBy($request->sort_field)` trần); ngày bỏ giây; registry `bom_lists` 23 cột + `exportList()` chuyển sang `DynamicExport` — bỏ blade phải tự map từng khoá cột (đổi tên cột trên lưới là file ra rỗng đúng cột đó). FE: `V2BaseSmartFilterPanel`, tách cột gộp `code_name` và gỡ tối đa 6 icon thao tác khỏi ô mã, cột Hành động cuối bảng (Sửa · Xóa + `⋮` Sao chép · In · Lịch sử), thêm 3 cột Phòng của người tạo · Người/Ngày cập nhật, `fixed-layout` 17 cột đủ `width` = `minWidth`, `columnCustomizationMixin`, lần đầu có popup chọn trường xuất file, 2 request `per_page=10000` hoãn tới khi mở panel lọc, `loadSeq`, `handleSort`/`handleReset` hết bắn 2 request. Kiểm chứng trên 11 BOM thật: index 200 (32 query/10 dòng), 2 khoá sort đúng + key lạ về mặc định, export .xlsx 18 dòng = 11 dữ liệu + 7 dòng khung, `exportFields` ↔ registry 23 = 23. Màn đã có sẵn hành động Lịch sử (`BomListLogModal`) nên không nợ như các màn khác. Spec: docs/superpowers/specs/gop-db/2026-09-07-bom-list-list-page-standard-design.md

- contract-list-page-standard — chuẩn hoá màn Danh sách hợp đồng (`/assign/contracts`) theo skill `list-page` → @khoipv → .plans/gop-db/contract-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 10/10 mã màu trạng thái quy về bảng 9 mã chuẩn; 4 cờ `is_can_edit`/`is_can_delete`/`is_can_approve`/`is_can_liquidate` = quyền AND trạng thái, hỏi quyền **1 lần cho cả trang** thay vì 4 truy vấn mỗi dòng; thêm `updater_name` + 3 ngày dạng chữ; tách `buildListQuery()` dùng chung index/export + whitelist sort nhận cả khoá `*_text` của FE và **chốt `id desc`**; registry `contracts` 13 cột + route/`export()` mới. FE: `V2BaseSmartFilterPanel` (nhóm Công ty/Phòng ban/Bộ phận/Người lập gom 1 field `org`); **bộ lọc trạng thái liệt kê đủ 10 trạng thái** — bản cũ chỉ 4 nên không lọc được các bước xuất hàng / quyết toán dù dữ liệu thật có đủ; Mã hợp đồng thành `nuxt-link`; cột Hành động cuối bảng (Sửa · Xóa · Duyệt · Thanh lý, "Không duyệt" không đưa vào); thêm 5 cột; `fixed-layout` 15 cột đủ `width` = `minWidth`; **lần đầu có cấu hình cột hiển thị và nút Xuất Excel**; `loadSeq`. Kiểm chứng trên 42 hợp đồng thật: index 200 (47 query/10 dòng), 4 khoá sort đúng, export .xlsx 49 dòng, `exportFields` ↔ registry 13 = 13; cờ thao tác đúng theo từng trạng thái và **fail-closed** với tài khoản không có 4 quyền; điều kiện hiện nút ở danh sách khớp màn chi tiết. Chưa làm: hành động Lịch sử (module Assign chưa có `LogsCatalogHistory`; hợp đồng có bảng `contract_histories` riêng dùng ở màn chi tiết). Spec: docs/superpowers/specs/gop-db/2026-09-07-contract-list-page-standard-design.md

- meeting-list-page-standard — chuẩn hoá màn Danh sách meeting (`/assign/meeting`) theo skill `list-page` → @khoipv → .plans/gop-db/meeting-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. 🐞 3 lỗi có sẵn: `MeetingController::index()` dùng biến `$sortMapping` **không tồn tại**; `MeetingCriteria` chạy trước nên `orderByDesc('updated_at')` ở đó luôn thắng, mọi `orderBy` của controller chỉ là khoá phụ (bấm sort cột Tên/Mã không ăn); meeting của nhân viên đã xoá quan hệ gây **500** vì thiếu null-guard `creator`. Ô lọc **Nhân viên** ghi vào `employee_id` mà BE không đọc (ô lọc chết) → tắt, thay bằng ô Người tạo đúng khoá; `initialStateForm` sửa `company_name` → `company_id` (bấm "Làm mới" trước đây không xoá được ô Công ty). BE thêm `STATUS_COLORS` + `MODES` (trước `STATUS` chỉ có tên class CSS `text-brand`, không dùng được cho badge), whitelist sort 9 khoá, registry `meetings` 21 cột + export `.xls` → `.xlsx` cột động, eager load 8 quan hệ + bỏ `TpCustomer::find(null)` → **175 → 70 truy vấn/10 dòng**. FE: panel 11 mục/13 ô; tách ô gộp `meetingInfo` (mã + tên + 3 dòng phụ + 6 icon) thành 6 cột; cột Hành động cuối bảng; **bỏ toàn bộ `v-html` + 4 hàm dựng HTML + listener `document.addEventListener('click')`**; thêm cột Địa điểm; `fixed-layout` 18 cột đủ `width` = `minWidth`; lần đầu có popup chọn trường xuất file; `loadData()` là request đầu tiên (bản cũ chờ `customers/search?limit=20000` xong mới nạp danh sách). Kiểm chứng trên 37 meeting thật: 70 query, 4 trạng thái đúng bảng màu, 4 khoá sort + 3 bộ lọc đều ăn, export .xlsx 44 dòng, `exportFields` ↔ registry 21 = 21. ⚠️ `MeetingResource` còn dùng chung ở `MyJobController`/`SolutionController`/`SolutionModuleController` → 3 màn đó hưởng lây khoá mới + định dạng ngày. Spec: docs/superpowers/specs/gop-db/2026-09-07-meeting-list-page-standard-design.md

- pricing-request-list-page-standard — chuẩn hoá màn Danh sách yêu cầu xây dựng giá (`/assign/pricing-requests`) theo skill `list-page` → @khoipv → .plans/gop-db/pricing-request-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. 🐞 3 chức năng CHẾT có sẵn: nút "Làm mới" gọi `this.loadData()` — hàm không tồn tại nên ném TypeError, ô lọc bị xoá mà danh sách giữ nguyên kết quả cũ; nút "Sửa nháp" ở danh sách **không bao giờ hiện** vì FE so `item.created_by` mà Resource không trả khoá đó (`Number(undefined)` = NaN); màn **Sửa** và màn **chi tiết** khoá toàn bộ form với MỌI phiếu do đọc `$store.state.auth?.user?.id` không tồn tại — nay cả 3 chỗ đọc cờ `is_can_edit` của máy chủ. BE: whitelist sort 10 khoá + chốt `id desc`, tách `buildListQuery()` dùng chung index/export, tìm nhanh thêm Người yêu cầu bằng EXISTS, 6 mã màu về bảng chuẩn, Resource trả khoá phẳng + `is_can_edit`/`is_can_delete`, registry `pricing_requests` 20 cột + route export đặt TRƯỚC `/{id}`. FE: panel 5 ô, Mã YCBG thành `nuxt-link`, cột Hành động cuối bảng (Sửa · Xóa · Tạo báo giá) — **thêm hành động Xóa lần đầu** (endpoint `DELETE` có sẵn, FE chưa từng gọi), thêm 3 cột, `fixed-layout` 16 cột đủ `width` = `minWidth`, lần đầu có cấu hình cột + Xuất Excel; màn chi tiết thêm nút Xóa cho khớp danh sách. Kiểm chứng: bảng `pricing_requests` đang rỗng → dựng dữ liệu thật trong transaction rồi rollback; 5 khoá sort đúng, tìm nhanh theo mã và theo tên người yêu cầu đều ăn, export .xlsx kể cả khi 0 dòng, `exportFields` ↔ registry 20 = 20; cờ quyền 3 chiều fail-closed. ⚠️ **Chờ user quyết (chưa sửa)**: người có quyền "Xây dựng giá bán theo công ty/phòng" KHÔNG thấy phiếu nháp của chính mình — nhánh phạm vi ở `index()` thay điều kiện "của tôi" bằng `whereIn('status', [2..6])` mà nháp là status 1; sửa là đổi phạm vi dữ liệu người dùng nhìn thấy nên không tự quyết. Spec: docs/superpowers/specs/gop-db/2026-09-07-pricing-request-list-page-standard-design.md

- product-project-list-page-standard — chuẩn hoá màn Danh sách hàng hoá làm dự án (`/assign/product-project`) theo skill `list-page` → @khoipv → .plans/gop-db/product-project-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. 🐞 2 lỗi có sẵn: `sort_field` bị **bỏ qua hoàn toàn** — bấm sort cột nào cũng chỉ đổi chiều theo ngày tạo (nay whitelist 3 khoá + `resolveSortKey()`); `dedupUnionRows()` không chốt khoá cuối nên 2 dòng cùng giá trị có thứ tự không xác định → lật trang thấy bản ghi lặp/mất (nay chốt `row_id desc`). BE thêm `erp_sync_status_color` (3 mã chuẩn) + `product_attributes_text` (hạ HTML TSKT về chữ cho file Excel), registry `product_projects` 19 cột, export `.xls` → `.xlsx` cột động. FE: `V2BaseSmartFilterPanel` 7 ô; `fixed-layout` 17 cột đủ `width` = `minWidth` **đo trên 181 dòng thật** (max + phân vị 95, không ước lượng); ô tham chiếu ghép `MÃ - Tên`; thêm cột Ngày tạo; Trạng thái đồng bộ bỏ `.pp-chip` tự chế sang `V2BaseBadge`; `columnCustomizationMixin`; lần đầu có popup chọn trường xuất file; `loadData()` bắn đầu tiên + `loadSeq`; bỏ 15 chỗ `'—'` và 4 khối CSS chết; màu chữ trong ô đồng bộ màn mẫu `/assign/customers` (rà cùng đợt 4 màn: customers 18 ô · solutions 21 · prospective-projects 10 · product-project 13). Kiểm chứng: index 200 với 181 dòng, 3 khoá sort đúng + key lạ về mặc định, export .xlsx thật, `fields=` còn đúng 3 cột, `exportFields` ↔ registry 19 = 19. ⚠️ **Màn chỉ đọc, không có cột Hành động** (routes chỉ có index + export + picker); TSKT trong file Excel nối dòng bằng " · " vì blade dùng chung `exports/dynamic.blade.php` in bằng `{{ }}` — muốn xuống dòng thật phải sửa file chung của 18 màn, cần hỏi trước. Spec: docs/superpowers/specs/gop-db/2026-09-07-product-project-list-page-standard-design.md

- prospective-project-list-page-standard — chuẩn hoá màn Danh sách dự án tiền khả thi (`/assign/prospective-projects`) theo skill `list-page` → @khoipv → .plans/gop-db/prospective-project-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: whitelist sort 13 khoá + chốt `id desc` (trước `orderBy($request->sort_field)` trần); subquery `creator_name`/`updater_name` không leftJoin; `STATUS_COLORS` + `PARENT_STATUS_COLORS` theo bảng 9 mã chuẩn; ngày `d-m-Y` → `d/m/Y H:i` và **bỏ khoá trùng `customer_need_solution_date`** đang ghi đè bản đã format; gỡ N+1 + eager load 12 quan hệ → **147 → 56 query/10 dòng**; 3 danh mục cứng chuyển từ FE/blade về hằng trên Entity; registry `prospective_projects` 32 cột + export ép `tree = false` để file phẳng có cả dự án con. FE: tách cột gộp `projectInfo`, thêm 7 cột, cột Hành động cuối bảng (Sửa · Xóa + `⋮` Tạo giải pháp · Tạo yêu cầu làm GP), `V2BaseBadge` thay 5 rule CSS `.pj-status-*`, `columnCustomizationMixin` thay ~80 dòng viết tay, lần đầu có popup chọn trường xuất file, giữ nguyên cây cha–con. Phase 4 theo phản hồi user cùng ngày: cột Khách hàng/Khách hàng cuối 240 → 260px, dòng phụ đổi xám `#6b7280` (`.text-muted` bị 4 file scss toàn cục ép thành ĐỎ), cột Mã 170 → 210px vì mã dài tới 26 ký tự, **gộp NV KD phụ trách + Phòng ban + Bộ phận thành 1 cột** (bảng 29 → 27 cột, file xuất vẫn giữ 3 cột riêng), thử ghim cột Tên rồi bỏ theo yêu cầu user. Kiểm chứng: 27/27 cột đủ `width` = `minWidth`, `exportFields` ↔ registry 32 = 32 và 32/32 khoá có thật trong Resource, sort 3 khoá đúng + chuỗi tiêm SQL về mặc định, export 109 KB, `fields=` còn 3 cột. ⚠️ **Bộ lọc giữ nguyên `V2BaseFilterPanel`** (user chốt 2026-09-07) nên 3 quy tắc của skill chưa áp cho màn này. Spec: docs/superpowers/specs/gop-db/2026-09-07-prospective-project-list-page-standard-design.md

- quotation-list-page-standard — chuẩn hoá màn Danh sách báo giá (`/assign/quotations`) theo skill `list-page` → @khoipv → .plans/gop-db/quotation-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 6/7 mã màu trạng thái báo giá + bảng trạng thái báo giá tổng quy về bảng 9 mã chuẩn, thêm `APPROVAL_LEVEL_COLORS`; whitelist `QUOTATION_SORTABLE_COLUMNS` + `applyQuotationSort()` chốt `id desc`; Resource `updated_at` format lại (trước trả THÔ chuỗi ISO) + `updater_name` + 4 khoá phẳng `bom_code`/`bom_name`/`project_code`/`project_name` (blade xuất file không đọc được mảng lồng); registry `quotations` 20 cột + route `exportList()` mới đặt TRƯỚC `/{id}` — ⚠️ khác hẳn `exportExcel()` sẵn có là xuất CHI TIẾT 1 báo giá để sửa rồi nạp lại. FE: `V2BaseSmartFilterPanel`, tách cột gộp `code_name` và gỡ 6 icon thao tác khỏi ô mã, cột Hành động cuối bảng (Sửa · Xóa + `⋮` Sao chép · In · Lịch sử phê duyệt), thêm 3 cột, Cấp duyệt + Đồng bộ ERP đổi sang `V2BaseBadge` (bỏ 3 class `.badge-level-*` nền đậm chữ trắng), `fixed-layout` 20 cột đủ `width` = `minWidth`, **lần đầu có nút Xuất Excel danh sách**, `loadSeq`. 🐞 Sửa lỗi "Làm mới" ném TypeError (`this.loadData()` không tồn tại, tên đúng là `fetchData`) — rà bằng grep phát hiện **màn thứ ba cùng lỗi là `/assign/quotations/pending-approval`**, đã sửa luôn. Kiểm chứng trên 75 báo giá thật: index 200 (57 query/10 dòng), 5 trạng thái đúng bảng màu, `updated_at` = `27/07/2026 16:55`, 3 khoá sort đúng, export .xlsx 82 dòng, `exportFields` ↔ registry 20 = 20. ⚠️ `/assign/quotations/pending-approval` và `/assign/summary-quotations` dùng chung `QuotationResource` nên hưởng lây phần sửa. Spec: docs/superpowers/specs/gop-db/2026-09-07-quotation-list-page-standard-design.md

- request-solution-list-page-standard — chuẩn hoá màn Danh sách yêu cầu làm giải pháp (`/assign/request-solution`) theo skill `list-page` → @khoipv → .plans/gop-db/request-solution-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 5 mã màu lệch bảng chuẩn quy về đúng nhóm (đáng chú ý "Yêu cầu bổ sung" `#DC2626` → `#F59E0B` — đỏ là ngôn ngữ của từ chối, không phải "cần bổ sung"); thêm 3 quan hệ + `isCanEdit()`/`isCanDelete()`; whitelist sort + chốt `id desc`; Resource trả `solution_code`/`solution_pm_name`/`solution_pm_phone` — **2 cột trên bảng vốn in cứng dấu gạch**; Người tạo/cập nhật chỉ còn TÊN, ngày bỏ giây; registry `request_solutions` 24 cột + export `.xls` → `.xlsx`. Hiệu năng đo bằng số: bỏ `find()` từng dòng, bỏ `->load()` thừa, cache static quyền + `departmentsManager()` → **115 → 54 truy vấn và 5,4s → 0,28s** trên 10 dòng. FE: panel gom nhóm `org`, tách cột gộp `request` + gỡ 4 icon thao tác khỏi ô mã, cột Hành động cuối bảng (Sửa · Xóa · Làm giải pháp · Hủy yêu cầu), 2 cột Mã GP / PM làm GP render dữ liệu thật, thêm 4 cột người/ngày, `fixed-layout` 22 cột đủ `width` = `minWidth`, `columnCustomizationMixin` + popup chọn trường xuất file, `loadData()` bắn đầu tiên + `loadSeq`, xoá hàm chết `deleteOne()` dùng `confirm()` trình duyệt + toast giả "(demo)". Kiểm chứng trên 18 yêu cầu thật: 4 khoá sort đúng, export .xlsx 25 dòng, `exportFields` ↔ registry 24 = 24, cờ quyền fail-closed với người khác. ⚠️ `/assign/request-solution/pending` dùng chung Resource nên hưởng lây (giao diện màn đó đã chuẩn hoá 2026-09-08). Spec: docs/superpowers/specs/gop-db/2026-09-07-request-solution-list-page-standard-design.md

- solution-module-list-page-standard — chuẩn hoá màn Danh sách hạng mục dự án (`/assign/solution-modules`) theo skill `list-page` → @khoipv → .plans/gop-db/solution-module-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. BE: 2 mã màu lệch bảng chuẩn ("Chờ duyệt hồ sơ trình duyệt" `#F59E0B` → `#D97706` vì `#F59E0B` là nhóm Cảnh báo, khác nghĩa; "Đã duyệt" `#10B981` → `#16A34A`); whitelist sort + chốt `id desc`; eager load `employee_create.info`/`employee_update.info`; Resource trả `creator_name`/`updater_name`/`updated_at` chỉ lấy `fullname`; registry `solution_modules` 13 cột + route/`export()` mới đặt TRƯỚC `/{solutionModule}`. FE: `V2BaseSmartFilterPanel`, tách cột gộp `solutionModuleInfo` + gỡ 3 icon thao tác khỏi ô mã, cột Hành động cuối bảng (Sửa · Lưu và duyệt) — **bỏ hành động "Quản lý" trùng với link ở cột Mã** và bỏ `@row-click` điều hướng; thêm 4 cột người/ngày; `fixed-layout` 13 cột đủ `width` = `minWidth` (Mã hạng mục lấy bậc L 260px vì mã dài tới 35 ký tự); **lần đầu có cấu hình cột và nút Xuất Excel**; `loadData()` bắn ĐẦU TIÊN — bản cũ `await loadFilterOptions()` tải `assign/solutions/getAll?per_page=10000` xong mới nạp bảng, chỉ để đổ options cho 1 ô lọc trong panel đang thu gọn (nay hoãn tới khi mở panel, `per_page` hạ còn 1.000). Kiểm chứng trên dữ liệu thật (5 hạng mục, tài khoản test thấy 3): index 200 trả đủ trường mới, `status_color` đúng bảng, 2 khoá sort đảo đúng + key lạ về `created_at desc`, export .xlsx 10 dòng, `exportFields` ↔ registry 13 = 13. ⚠️ **Không tài khoản nào đang có 4 quyền "Xem danh sách hạng mục dự án theo tổng công ty / công ty / phòng ban / bộ phận"** (kiểm bằng SQL) — mọi người chỉ thấy hạng mục mình liên quan; không phải lỗi đợt này nhưng nghiệp vụ cần thì phải gán quyền. Spec: docs/superpowers/specs/gop-db/2026-09-07-solution-module-list-page-standard-design.md

- task-list-page-standard — chuẩn hoá màn Danh sách task (`/assign/tasks`) theo skill `list-page` → @khoipv → .plans/gop-db/task-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-07). Nhánh `gop_db` cả 2 repo, chưa commit, không migration, không quyền mới. 🐞 `TaskService` sắp xếp bằng `orderBy($request->sort_field, $request->sort_dir)` nhận thẳng chuỗi từ URL → nay whitelist 12 khoá + chốt `id desc`. BE: 5/10 mã màu trạng thái về bảng chuẩn + thang màu ưu tiên RIÊNG; Resource thêm `status_color`, `priority_name`/`priority_color`, `deadline_state_text`/`_color`, ngày bỏ giây, `updated_by_name` bỏ tiền tố mã nhân viên; bỏ N+1 (3 chỗ `Employee::find()->info`, `->load('priorityLevel')` chạy từng dòng phá luôn eager load) + hằng `LIST_RELATIONS` 15 quan hệ dùng chung index/export → **325 → 67 truy vấn/10 dòng**; registry `tasks` 27 cột + export thay `TaskExport` blade 13 cột cứng. FE: panel 15 mục/17 ô; tách ô gộp `taskInfo` (mã + tên + 3 dòng phụ + chip tag + 6 icon) thành 7 cột; cột Hành động cuối bảng (Sửa · Xóa + `⋮` Nhập kết quả · Duyệt · Lịch sử); bỏ 4 hàm tô màu tự chế → `V2BaseBadge` với màu BE trả; thêm 5 cột (Tình trạng hạn · Tag · Ngày tạo · Người/Ngày cập nhật); `fixed-layout` 22 cột đủ `width` = `minWidth` + bỏ đoạn tự gán `sticky: index < 3` (cột kéo đi đâu cũng ghim → offset `left` sai); lần đầu có popup chọn cột xuất file và **lọc nhiều tag mới gửi được hết** (trước `buildQueryString` chỉ gửi tag cuối); `loadSeq` + `suppressFilterWatch`; **xoá ~450 dòng code chết**. ⚠️ Khối lọc nhanh chuyển từ slot `toolbar` sang `left-actions` — `toolbar` thay cả khối tiêu đề nên **màn đang mất tiêu đề bảng**. Kiểm chứng trên 14 task thật: 67 truy vấn (trước 325), 4 trạng thái + 3 mức ưu tiên đúng thang màu, 4 khoá sort + 3 bộ lọc đều ăn, export .xlsx 21 dòng / 28 cột, `exportFields` ↔ registry 27 = 27. ⚠️ `TaskResource` còn dùng ở `MyJobController` và báo cáo → hưởng lây khoá mới + định dạng ngày. Spec: docs/superpowers/specs/gop-db/2026-09-07-task-list-page-standard-design.md

- finance-prepick-transfer-request — port màn **Phiếu yêu cầu điều chuyển hàng giữ** (ERP `warehouse/prepick_transfer2` → HRM `/finance/prepick-transfer-requests`) → @junfoke → .plans/gop-db/finance-prepick-transfer-request/design.md · plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + Playwright bấm thật 2026-08-25, vá QA redmine 11279/11296 ngày 2026-09-04). Nhánh riêng `feat/finance-prepick-transfer-request` (cả 2 repo, tách từ `gop_db`). Dùng chung bảng ERP `prepick_transfer2` + `prepick_transfer2_details` giữ nguyên schema, **chỉ 1 migration thêm bảng lịch sử của HRM** (`2026_08_24_000001_create_prepick_transfer_request_history_table`, đã chạy); không tạo quyền mới. Đủ luồng: danh sách + bộ lọc, form lập/sửa, chi tiết + 3 cấp duyệt, in, xuất Excel, đính kèm, lịch sử. Kiểm chứng Playwright: 10 cột đúng thứ tự, 3 badge đúng mã màu chuẩn, cột Hành động đổi theo trạng thái, 4 bộ lọc đối chiếu SQL khớp từng con số (16 = 16 · 230 = 230 · 2 = 2), sort + phân trang + cấu hình cột + popup Lịch sử đều đúng, mọi lần test đều hoàn nguyên DB và đối chiếu 4 bảng `bak_*_20260824` **0 chênh lệch**. 🐞 Bắt được bug `markFormSaved()` gọi ngay sau khi nạp dữ liệu → cờ `unsavedIgnore` bật vĩnh viễn nên cảnh báo "chưa lưu" không bao giờ hiện; **đã vá luôn cho 2 màn đang chạy** (Gia hạn + Phiếu hủy hàng giữ) và bỏ 43 chỗ `|| '—'` + 7 `placeholder="—"` ở 3 màn Giữ hàng cũ. Thêm util dùng chung `utils/scrollToFirstError.js` (bấm Lưu là nhảy tới đúng dòng lỗi) gom 4 khối cuộn viết tay của nhóm Giữ hàng. QA 11279: một hàng đang giữ cho 2 khách/2 hạn phải thêm được 2 dòng — popup đổi từ loại theo `product_id` sang **loại theo LÔ** (`exclude_lot_ids[]`), 2 màn Hủy/Gia hạn giữ nguyên cách cũ. Tồn: xoá 4 bảng `bak_*_20260824` sau khi user nghiệm thu. Spec: docs/superpowers/specs/gop-db/2026-08-24-finance-prepick-transfer-request-design.md

- bom-list-customer-filter-remote — sửa lỗi ô lọc Khách hàng màn BOM List → chưa ghi người phụ trách → .plans/gop-db/bom-list-customer-filter-remote/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code 2026-08-19). Bỏ `assign/customers/search?limit=20000` ở `pages/assign/bom-list/index.vue` — nạp 43k khách hàng làm **BE PHP fatal "Allowed memory size exhausted"**; đổi ô lọc sang `V2BaseSelectRemote` + `fetchCustomers(q, limit=30)` theo khuôn `/sale/warranty-repair-requests`; giữ nhãn KH khi tự điền theo dự án TKT hoặc quay lại màn (`customerInitialOption` + localStorage). Không migration, không quyền mới.

- fe-build-toi-uu — giảm thời gian `yarn run build` của `hrm-client` mỗi lần deploy lên `hrm-crm.eteksofts.com` → chưa ghi người phụ trách → .plans/gop-db/fe-build-toi-uu/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong Phase 1 (đo 2026-08-17). Bật `build.cache` + `build.parallel` trong `nuxt.config.js` (trước cả 2 đang bị comment); đo thật trên bản clone `gop_db-client` (Node 14.21.3, 10 core): **baseline 223s → dựng cache 195s → sửa 2 file 134s → sửa 1 file 96s**; kiểm chứng cache không trả bundle cũ bằng chuỗi marker. Còn lại: cập nhật `~/build_hrm_crm.sh` trên server (bỏ qua build khi không có file FE đổi; chỉ `yarn install --frozen-lockfile` khi `package.json`/`yarn.lock` đổi; **bỏ `npm install` vì trộn npm với yarn làm xoá `node_modules/.cache`**) — file này nằm ngoài repo. Phase 2 chờ user quyết: gỡ 11 thư viện 0 import, gộp 4 bộ chart về `apexcharts`, đổi `node-sass@4` → dart-sass.

- quotation-pending-approval-list-page-standard — chuẩn hoá màn Báo giá chờ duyệt (`/assign/quotations/pending-approval`) theo skill `list-page` → @khoipv → .plans/gop-db/quotation-pending-approval-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-08). BE 4 file · FE 1 file, không migration, không quyền mới; dùng chung `QuotationResource` + `applyListFilters()` với màn `/assign/quotations` nên phần truy vấn hưởng sẵn. Sửa 3 lỗi có sẵn: whitelist sort thiếu đúng khoá MẶC ĐỊNH của màn (`sort_field = 'submitted_at'` không có trong `QUOTATION_SORTABLE_COLUMNS` → âm thầm rơi về `created_at desc`) cùng `customer_name`/`price_approval_level`/`status` — bổ sung 6 khoá; Resource trả `submitted_at` thô trong khi các mốc khác đã format ở BE; registry `quotations` thiếu hẳn khoá `submitted_at` nên cả 2 màn báo giá không xuất được cột Ngày gửi duyệt. Thêm `pendingApprovalExport()` + route export gắn cùng middleware quyền với route danh sách. FE: `V2BaseSmartFilterPanel` 6 mục (bản cũ 2 ô trong khi BE nhận sẵn 12 khoá lọc), tách cột gộp "Mã BG • BOM" và gỡ nút thao tác khỏi ô mã, cột Hành động cuối bảng (Duyệt + Lịch sử phê duyệt), Cấp duyệt bỏ 2 class badge tự chế sang `V2BaseBadge`, `fixed-layout` 17 cột đủ `width` = `minWidth`, lần đầu có xuất Excel, `columnCustomizationMixin`, `loadSeq`, `$safeLoading*`, `fetchData()` bắn ngay thay vì chờ 2 request không liên quan. Bỏ 2 cột "Người duyệt"/"Ngày duyệt" — ⚠️ bài học đo đạc: đếm thô `status IN (3,4)` ra 38 dòng (38 có `approved_at`) suýt cho kết luận ngược, chạy đúng `getPendingApproval()` với tài khoản có quyền duyệt mới ra 13 dòng (0 `approved_at`, 13/13 `submitted_at`); các màn "chờ duyệt" còn lại phải chạy đúng hàm service của màn chứ không đếm `WHERE status = X`. Spec: docs/superpowers/specs/gop-db/2026-09-08-quotation-pending-approval-list-page-standard-design.md

- handover-pending-list-page-standard — chuẩn hoá màn Phiếu bàn giao chờ duyệt (`/assign/handover/pending`) theo skill `list-page` → @khoipv → .plans/gop-db/handover-pending-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-08). BE 3 file · FE 1 file, không migration, không quyền mới; màn thứ 3 (cuối) của cụm phiếu bàn giao, trước giờ là nhánh code song song nên không hưởng gì từ 2 đợt chuẩn hoá 2026-09-07. Sửa 3 lỗi có sẵn: bộ lọc "Ngày gửi duyệt từ/đến" lọc nhầm cột `updated_at` thay vì `submitted_at` (mà `updated_at` đổi mỗi lần sửa phiếu nên khoảng ngày người dùng chọn ra sai phiếu); `pending()` chốt cứng `orderBy('created_at','desc')` nên màn không sắp xếp được cột nào dù `applyHandoverSort()` whitelist 13 khoá đã có sẵn cùng service (⚠️ service này đặt tên `applyHandoverSort`, không phải `applySort`); nút Xuất Excel là nút chết — gọi lại chính API danh sách rồi báo "đang phát triển", nay dùng `DynamicExport` + registry `handovers` chung với màn danh sách. FE: `V2BaseSmartFilterPanel` 8 mục (trước không có auto-search), ô Giải pháp bỏ `disabled` cứng thành ô chọn thật cascade theo Dự án, Mã phiếu đổi sang `nuxt-link` và gỡ nút thao tác khỏi ô đó, cột Hành động cuối bảng (Duyệt + Lịch sử), lần đầu có sắp xếp cột / cấu hình cột / giữ bộ lọc / popup chọn trường xuất file, `fixed-layout` 15 cột đủ `width` = `minWidth`, `loadSeq`, `$safeLoading*`. Bỏ hẳn 6 khoá vì trạng thái của màn quyết định (`approver_name`/`approved_at`/`reject_reason` và 3 con số nhận/từ chối/chờ luôn 0/0/tổng). ⚠️ Bảng `handovers` RỖNG trên DB dev → kiểm chứng bằng 3 phiếu giả trong transaction rồi rollback; chưa thử 4 bộ lọc đi qua `items` (câu lọc giữ nguyên bản cũ). Spec: docs/superpowers/specs/gop-db/2026-09-08-handover-pending-list-page-standard-design.md

- request-solution-pending-list-page-standard — chuẩn hoá màn Yêu cầu làm giải pháp chờ duyệt (`/assign/request-solution/pending`) theo skill `list-page` → @khoipv → .plans/gop-db/request-solution-pending-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile trên dữ liệu thật 2026-09-08). BE 3 file · FE 1 file, không migration, không quyền mới; dùng chung `RequestSolutionResource` với màn `/assign/request-solution` nhưng trước giờ là nhánh code song song. Sửa 6 lỗi có sẵn: `pending()` đẩy thẳng `$request->sort_field` vào `orderBy()` (không whitelist, không chốt `id desc`) dù `applySort()` có sẵn cùng service; thiếu 5 eager load mà `index()` đã bổ sung → 4 cột luôn rỗng + N+1; không có quyền thì `pending()` trả mảng `[]` còn `exportPending()` gọi `->get()` trên đó → fatal 500; FE `canReceive()` hard-code `return true` dù entity đã có `isCanReceive()`; `handleFilterChange()` nhận sai kiểu payload nên nhét 2 khoá rác `key`/`value` vào filters rồi gửi lên API; `handleSort`/`handleReset` bắn 2 request mỗi thao tác. Export chuyển từ `RequestSolutionPendingExport` (.xls cột cứng) sang `DynamicExport` + registry `request_solutions` dùng chung. FE: `V2BaseSmartFilterPanel` 5 mục, tách cột gộp "Mã • Tên yêu cầu" và gỡ 4 icon thao tác khỏi ô đó, cột Hành động cuối bảng chỉ còn Tiếp nhận + Yêu cầu bổ sung thông tin (bỏ Xem, bỏ Từ chối và Hủy yêu cầu — 2 hành động phủ quyết chỉ đặt ở màn chi tiết), `fixed-layout` 19 cột đủ `width` = `minWidth`, lần đầu có cấu hình cột + popup chọn trường xuất file, `loadSeq`, `$safeLoading*`. Bỏ hẳn 3 cột (Người tiếp nhận YC · Mã GP · PM làm GP) và ô lọc `receiver_by` vì rỗng theo ĐỊNH NGHĨA của màn — `receive_id` chỉ ghi từ trạng thái Đã tiếp nhận trở đi. Spec: docs/superpowers/specs/gop-db/2026-09-08-request-solution-pending-list-page-standard-design.md

- issue-list-page-standard — chuẩn hoá màn Quản lý Issue (`/assign/issues`) theo skill `list-page` → @khoipv → .plans/gop-db/issue-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-08). BE 6 file · FE 1 file, không migration, không quyền mới. Sửa 3 lỗi có sẵn: `IssueService::index()` đẩy thẳng `$request->sort_field` vào `orderBy()` — gõ tay tên cột lạ trên thanh địa chỉ là 500, nay có `SORTABLE_COLUMNS` 5 khoá + chốt `orderByDesc('issues.id')`; bản đồ nhãn "Loại issue"/"Nguồn phát hiện" viết lại ở FE thiếu 3 giá trị nên issue mang giá trị đó in ra mã thô (nay dùng chung `DetailIssueResource::ENUM_MAPS` đổi `private` → `public`); `creator.info` + `employee_update.info` không eager load → N+1 ngay trên câu danh sách. Thêm `issue_type_text`/`detected_from_text`/`due_status_text` + màu/`tags_text` ở Resource, `creator_name` đọc đúng quan hệ mà bộ lọc dùng, ô tìm nhanh thêm người tạo bằng `EXISTS`, `Issue::STATUS_DATA` sửa 4 mã màu về bảng 9 màu chuẩn, registry `issues` 25 cột + export chuyển từ `IssueExport` (.xls cột cứng) sang `DynamicExport`. FE: `V2BaseSmartFilterPanel` 13 mục (thêm ô Loại issue mà BE nhận `issue_type` từ lâu), tách cột gộp "Mã-Tên issue" và gỡ 5 nút thao tác khỏi ô Mã, cột Hành động cuối bảng (Sửa · Xóa + `⋮` Xử lý · Lịch sử), thêm 6 cột gồm cả Ngày tạo (cột bắt buộc trước không có), `fixed-layout` 25 cột đủ `width` = `minWidth`, lần đầu có popup chọn trường xuất file, `columnCustomizationMixin`, `loadSeq` + `suppressFilterWatch` (4 nút lọc nhanh trước bắn 2 request mỗi lần bấm), `$safeLoading*`. ⚠️ Bảng `issues` RỖNG trên DB dev → kiểm chứng bằng issue giả trong transaction rồi rollback. Spec: docs/superpowers/specs/gop-db/2026-09-08-issue-list-page-standard-design.md

- finance-addition-accounting-request — sửa màn Phiếu yêu cầu hạch toán bổ sung theo yêu cầu user (Phase 11) → @khoipv → .plans/gop-db/finance-addition-accounting-request/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + smoke test API 18/18 pass 2026-09-07). BE 5 file · FE 5 file, không migration, không quyền mới. Yêu cầu user: màn Tạo bỏ 2 ô "Người tạo"/"Phòng ban" — người lập chuyển sang góc phải header card "Thông tin chung" dạng `Người lập - Ngày lập` như ERP; dropdown Loại yêu cầu đủ 7 loại chọn được y hệt ERP (`EDITABLE_TYPES` nay gồm cả loại 7, và ERP cũng không có nhánh form riêng cho loại này). Lòi ra 2 lỗi nặng ngoài yêu cầu ban đầu: 2 FormRequest dùng `$this->get()` mà FE gửi JSON body → `type`/`object_type`/`status` luôn null nên rule rẽ theo loại KHÔNG BAO GIỜ chạy — loại 2/6 (1.894/1.937 phiếu) không lập nổi vì bị đòi `money` + `note` là 2 trường màn hình không có, và từ chối không cần nhập lý do; vá xong thì nhánh lưu nháp lần đầu được chạy, lộ tiếp `exchange_rate` là cột NOT NULL → lưu nháp bỏ trống tỷ giá là 500. ⚠️ Hệ quả đã biết của loại 7 nhập tay (giống hệt ERP): 3 bảng riêng của loại 7 rỗng nên màn Chi tiết/In vẫn rẽ sang layout Phối hợp kinh doanh, phiếu không có phòng hỗ trợ nên người chỉ có quyền xem cấp công ty không thấy nó trong danh sách và 2 nút Từ chối / Lập phiếu kế toán không hiện. Còn nợ: rà nốt 18 FormRequest khác cùng lỗi `$this->get()` (Finance 7 · CustomerCare 7 · Payroll 4). Spec: docs/superpowers/specs/gop-db/2026-08-25-finance-addition-accounting-request-design.md

- handover-receiving-list-page-standard — chuẩn hoá màn Phiếu bàn giao chờ tiếp nhận (`/assign/handover/receiving`) theo skill `list-page` → @khoipv → .plans/gop-db/handover-receiving-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-07). BE 4 file sửa + 1 file mới (`ReceivingHandoverResource.php`) · FE 1 file, không migration, không quyền mới. Lỗi gốc: đơn vị dòng sai nên phân trang hỏng — màn hiển thị theo PHIẾU nhưng API trả từng CÔNG VIỆC đã phân trang rồi FE gom `handover_id` bằng JS, hệ quả là số dòng mỗi trang không đều, cột "Số công việc" chỉ đếm phần việc rơi vào trang đó, 1 phiếu hiện lại ở trang sau với con số khác, `meta.total` và ô "Tổng" sai theo 2 kiểu, và con số đếm không phân biệt người nhận; nay `HandoverService::receivingHandovers()` trả thẳng `Handover` + 4 `withCount` dùng lại đúng closure lọc → `my_total_items`/`my_accepted_items`/`my_rejected_items`/`my_pending_items` (`Handover::items()` không có điều kiện `receiver_id`, quên là đếm cả việc của người khác). 2 lỗi khác: nút Xuất Excel là nút chết (nay có route + `receivingExport()` + registry `handover_receiving` 15 cột) và ô lọc Giải pháp bị `disabled` cứng. Thêm whitelist sắp xếp 7 khoá + chốt `id desc`, ô tìm nhanh thêm mã phiếu. FE: bỏ đoạn gom `handover_id` bằng JS, `V2BaseSmartFilterPanel` 6 mục, Mã phiếu đổi sang `nuxt-link` và gỡ nút thao tác khỏi ô đó, cột Hành động cuối bảng (Tiếp nhận + Lịch sử), thêm 4 cột, nhãn ô đếm ghi rõ "Công việc của tôi", `fixed-layout` 14 cột đủ `width` = `minWidth`, lần đầu có cấu hình cột / giữ bộ lọc / sắp xếp cột, ô "Tổng" lấy `pagination.total`. ⚠️ Dùng Resource riêng chứ không đụng `HandoverResource` của 2 màn kia vì ngữ nghĩa đếm khác; 2 bảng `handovers` + `handover_items` RỖNG trên DB dev → kiểm chứng bằng dữ liệu giả trong transaction rồi rollback. Spec: docs/superpowers/specs/gop-db/2026-09-07-handover-receiving-list-page-standard-design.md

- handover-list-page-standard — chuẩn hoá màn Danh sách phiếu bàn giao (`/assign/handover`) theo skill `list-page` → @khoipv → .plans/gop-db/handover-list-page-standard/plan.md
  Hoàn thành: 2026-09-10 — user xác nhận đã xong (code + kiểm chứng API/compile 2026-09-07). BE 6 file · FE 1 file sửa + 1 file mới (`HandoverHistoryModal.vue`), không migration, không quyền mới. Sửa 3 lỗi có sẵn: `handleFilterChange(filters)` nhận sai kiểu payload nên mỗi lần đổi ô lọc lại nhét 2 khoá rác `key`/`value` vào filters và gửi lên API trong khi ô lọc thật không được gán giá trị; `HandoverService::index()` sắp xếp bằng chuỗi nhận thẳng từ URL, không whitelist, không chốt `id desc` (nay 13 khoá); ô lọc Bộ phận ghi vào `part_id` mà bảng `handovers` không có cột đó → ô lọc chết, đã tắt. BE thêm: màu Từ chối `#B91C1C` → `#DC2626` (giữ "Đã duyệt" `#2563EB` vì duyệt xong phiếu mới BẮT ĐẦU giao/nhận việc), chuyển nguyên điều kiện Sửa/Xóa từ FE về BE thành `isCanEdit()`/`isCanDelete()`, Resource thêm `updated_by_name` + 2 cờ quyền + 4 mốc thời gian bỏ giây, bổ sung eager load, và route + `export()` + registry `handovers` 19 cột — màn này trước giờ không có xuất Excel. FE: `V2BaseSmartFilterPanel` 5 mục, tách ô gộp "Mã phiếu • Nhân viên BG" thành 4 cột, cột Hành động cuối bảng (Sửa · Xóa + Lịch sử trong `⋮`, bỏ Xem) với popup `HandoverHistoryModal` bọc `SystemInfoSection` dùng chung với màn chi tiết, thêm 5 cột, `fixed-layout` 18 cột đủ `width` = `minWidth`, lần đầu có cấu hình cột hiển thị / xuất Excel / giữ bộ lọc, nút toolbar chuyển sang slot `actions` (slot `toolbar` thay cả khối tiêu đề nên màn đang mất tiêu đề). ⚠️ Sửa `HandoverResource` dùng chung nên 2 màn `/assign/handover/pending` + `/receiving` hưởng lây khoá mới và ngày bỏ giây; bảng `handovers` RỖNG trên DB dev → kiểm chứng bằng 5 phiếu giả trong transaction rồi rollback. Spec: docs/superpowers/specs/gop-db/2026-09-07-handover-list-page-standard-design.md

- assign-list-page-standard (loạt 15 màn) — chuẩn hoá danh sách `assign/*` theo skill `list-page` → @khoipv → .plans/gop-db/<màn>-list-page-standard/plan.md (solution, industry-group, application, customer-scope, meeting-type, survey-question, attachment-type, internal-business-scope, solution-group, customer-scope-group, project-item, project-role, form-template, reason-project-failure, discount-type)
  Hoàn thành: 2026-09-05 — user xác nhận đã xong. FE theo skill đầy đủ + BE mức tối thiểu (whitelist sort, tên người tạo/cập nhật bằng subquery, popup chọn trường xuất file qua `ExportColumnRegistry` + `DynamicExport`); hành động dòng = Sửa + Xóa là 2 nút chính, còn lại vào `⋮`; cố ý KHÔNG làm "Lịch sử thay đổi" và cấu hình cột mặc định hiện HẾT cột (2 ngoại lệ user chốt so với skill); bề rộng cột theo mục 15b, bảng bật `fixed-layout`. Không migration, không quyền mới. Sửa luôn loạt lỗi CÓ SẴN gặp dọc đường: `scopes` vs `hrm_scopes` ở màn nhóm ngành (500 ở Create/Edit/lọc, cả local lẫn dev) và `InternalBusinessScope::isCanLockUpdate()` cùng họ; thiếu cờ `is_can_delete`/`is_can_edit`/`is_can_lock_update` ở vài Resource; `ignoredFields` khai cả trong `data` lẫn `computed` (Vue 2 che computed); cột chết "Dùng ở dự án" ở màn vai trò dự án; 2 lỗi N+1 ở `FormTemplatesResource` (`whenLoaded()` trả object nên LUÔN truthy → nạp lười cả cây section từng dòng; `questions_count` đếm bằng cách nạp hết câu hỏi) — 4 query/dòng về 0; `ReasonProjectFailureResource` 43 query về 7; `DiscountTypeResource` cùng lỗi đó, ảnh hưởng cả `getAll` của dropdown báo giá; màn Loại giảm giá chưa từng có Xuất Excel nên thêm mới route + controller export; `$refs...?.loadData?.()` và id modal sai tên ở 2 màn (popup không mở, im lặng). Kiểm chứng mỗi màn: compile SFC + AST đối chiếu định danh template, cột bảng ↔ trường xuất FE ↔ registry BE, mọi cột đủ `width` + `minWidth`, smoke test API (index/sort/keyword/export).

- project-phase-list-page-standard — chuẩn hoá màn Danh sách giai đoạn dự án theo skill `list-page` → @khoipv → .plans/gop-db/project-phase-list-page-standard/plan.md
  Hoàn thành: 2026-09-05 — user xác nhận đã xong; làm theo khuôn 2 màn user chỉ định (nhóm ngành + ứng dụng), BE 6 file sửa · FE 1 file viết lại, không migration. BE: whitelist sort 4 cột; subquery người tạo/cập nhật; tìm nhanh thêm người tạo (EXISTS); thêm lọc Mã/Tên/Mức độ ưu tiên; `status_text` + ngày `d/m/Y H:i`; `is_can_delete` tính từ subquery đếm (bỏ 1 query/dòng); export chuyển sang `DynamicExport` (`.xls` → `.xlsx`, cột động) và nới quyền route export cho người chỉ có quyền xem. FE: `V2BaseSmartFilterPanel` 8 ô; tách cột Mã (link mở modal Xem) / Tên; cột Hành động cuối bảng với `V2BaseRowActions` (bỏ "Xem", Khoá/Mở khoá rời khỏi ô Trạng thái); `V2BaseBadge`; 4 cột Người tạo/Ngày tạo/Người cập nhật/Ngày cập nhật; cấu hình cột + nhớ bộ lọc + popup chọn trường xuất file; `fixed-layout` đủ 12 cột; gỡ code chọn nhiều dòng. Cố ý bỏ hành động Lịch sử (module Assign chưa có `LogsCatalogHistory`, giống 2 màn mẫu). Kiểm chứng: compile + AST, smoke test API, đọc lại file xuất, đối chiếu cột bảng ↔ file ↔ registry 10 = 10.

- borrow-export-request — Yêu cầu xuất hàng mượn, port ERP `borrow_export_requests` → HRM → @khoipv → .plans/gop-db/borrow-export-request/design.md · plan.md
  Hoàn thành: 2026-09-05 — user xác nhận đã xong (code + test Playwright toàn luồng 2026-09-04). BE 12 file mới + 4 file sửa · FE 7 file mới + 2 file sửa (menu) · 0 bảng mới · KHÔNG migration · 3 QUYỀN MỚI guard `api` id 1565-1567 (trùng tên quyền ERP guard `web` 100890-100892). User chốt: port đầy đủ như ERP; nút "Tạo phiếu xuất hàng mượn" báo "chưa triển khai" (màn `borrow_exports` chưa port); chỉ 2 mục menu — bỏ mục `Chờ duyệt → Hàng mượn` của ERP, người duyệt lọc bằng ô Trạng thái (preset `for-approve` giữ chạy cho link cũ). Tách `BorrowStockService` dùng chung để tính "Đang mượn" cho 3 luồng tranh cùng lượng hàng (port `ProductExportRequestDetail::getReturningQty()` mà HRM chưa từng có). ⚠️ Sửa CÓ CHỦ Ý 3 chỗ so với ERP: màu trạng thái (nháp xám / chờ duyệt vàng thay vì đỏ hết); bỏ dòng ép cứng `company_id` cuối `searchByFilter()` (nó triệt tiêu quyền "tổng công ty"); `canView()` cộng 3 nhánh quyền cấp (ERP cho trưởng phòng thấy phiếu ở danh sách nhưng bấm vào ra `not_found`). ⚠️ Khối File đính kèm dùng LẠI `AttachmentSection.vue` của màn Đề nghị thanh toán — component chung được thêm 3 prop (`apiBase`/`allowedExtensions`/`maxSizeMb`) với mặc định đúng giá trị cũ nên màn Đề nghị thanh toán không đổi hành vi. Kiểm chứng trên dữ liệu thật: 11 endpoint (10× 200, 1× 422 đúng nghiệp vụ); phạm vi danh sách ↔ `canView()` khớp 100% trên 60 nhân viên; vòng đời ghi 7/7 chạy trong transaction rồi rollback sạch; bản in lấy letterhead theo `company_id` trên phiếu; `export-request-data` không lộ giá vốn. Playwright bấm thật tìm và sửa 4 lỗi: sort "Ngày duyệt" chết do FE gửi `approved_time` còn BE khai `approvedTime`; tiêu đề tab hiện nguyên thẻ HTML của badge; tên người lập trống ở màn Tạo (sai khoá store, đúng là `current_employee_info.fullname`); toast lỗi upload ra tiếng Anh (câu tiếng Việt nằm trong `errors`, không phải `message`). Vòng đời ghi chạy thật rồi dọn sạch, DB về đúng 292 phiếu / 686 dòng / 990 chi tiết. Chưa kiểm chứng được: đổi ĐVT khi hàng có nhiều đơn vị (dữ liệu thật chỉ 1 ĐVT/hàng) và bản in trên máy in thật. Còn nợ 2 việc chờ user quyết: `ProductExportRequest::dataForBorrowReturn()` của màn Yêu cầu nhập hàng thiếu phép trừ `returning_qty` so với ERP (đề xuất trả nhiều hơn số thực còn mượn); gộp 3 bản chép `manageableDepartmentIds()` ở nhóm Prepick về trait dùng chung (đã đưa lên trait, chưa gỡ bản cũ). Spec: docs/superpowers/specs/gop-db/2026-09-04-borrow-export-request-design.md

- finance-bill-payment-authorization — bộ tài liệu bàn giao (SRS + testcase + HDSD) màn Phiếu ủy nhiệm chi → @khoipv → .plans/gop-db/finance-bill-payment-authorization/plan.md (mục "Phase T")
  Hoàn thành: 2026-09-05 — sinh 3 tài liệu cùng thư mục feature, kèm 3 generator `gen_srs.py`/`gen_testcase.py`/`gen_hdsd.py` commit cùng chỗ để tái sinh: `SRS - Phiếu ủy nhiệm chi.docx` (form chuẩn 2026-08-28, 4 chương, 11 chức năng FR-01…FR-11, 38 bảng, 23 ảnh, 43 trang), `testcase.xlsx` (149 TC, P0 63%, 20 TC phân quyền + 10 section La Mã, bộ kiểm tra thuật ngữ sạch), `HDSD_Phiếu ủy nhiệm chi.docx` (13 Heading 1, 13 bảng, 23 ảnh, 38 trang, có mục hướng dẫn riêng cho từng quyền). 25 ảnh thật ở `unc_shots/` chỉ để local, KHÔNG commit; chụp bằng tài khoản DNS Admin trên cổng dev, chỉ mở form/hộp thoại rồi Hủy nên không ghi dữ liệu.

- finance-prepick-extend-request — port màn **Yêu cầu gia hạn hàng giữ** (ERP → HRM `/finance/prepick-extend-requests`) → @junfoke → .plans/gop-db/finance-prepick-extend-request/design.md · plan.md
  Hoàn thành: 2026-09-04 — user test tay 2026-08-24 ("tạm ổn"), Phase 10 vá QA redmine 11276/11277/11278/11296 xong 2026-09-04. Nhánh riêng `feat/finance-prepick-extend-request` (cả 2 repo, tách từ `gop_db`); dùng chung bảng ERP, **chỉ 1 migration thêm bảng lịch sử của HRM** (`2026_08_22_000001_create_prepick_extend_request_history_table`, đã chạy), **không tạo quyền mới** (đọc qua `ChecksEmployeePermission`). Đủ luồng: danh sách, form thêm/sửa, chi tiết + duyệt 3 cấp TP → BGĐ → KT, lịch sử, in (khổ ngang theo user chốt), xuất Excel, đính kèm theo mẫu `BillPaymentAttachmentService` (S3 `prepick_extend_request`, ≤ 13 MB). Playwright chạy thật luồng Lưu nháp → Gửi duyệt → TP duyệt → (BGĐ) → KT duyệt, đối chiếu `prepick_details` + `prepick_logs` trước/sau bằng SQL; 6 lệnh grep tự kiểm của skill sạch. QA: **11276** cột "Cần gia hạn" mặc định = số ĐANG GIỮ (ERP làm việc này trong class JS nên nhìn DB thấy 0 mà màn ERP vẫn hiện số); **11277** lịch chọn "Hạn giữ mới" mất cột Chủ nhật — gốc ở component dùng chung `V2BaseDatePicker` ghim `left` không kẹp mép phải màn hình, đã kẹp trong `[8px, innerWidth - popupWidth - 8px]` (⚠️ sửa file dùng chung); **11278** thêm nút Sửa/Xóa cho phiếu nháp ở màn Chi tiết. 📏 Phần "giá trị vượt ngưỡng" của 11278 **KHÔNG PHẢI LỖI — tester báo nhầm**: đối chiếu code ERP thì ERP cũng không chặn tạo phiếu vượt ngưỡng (ngưỡng tiền chỉ dùng để RẼ NHÁNH DUYỆT) và cũng không cho TP/BGĐ/KT sửa số lượng lúc duyệt; chạy thật `needBoardApproveByLines()` trên `gop_db` cho đúng kết quả — lô của tài khoản test toàn hàng giá 1đ nên tester không dựng được dữ liệu đủ tiền. Tồn: soát nốt checklist A→H của skill và xoá 4 bảng `bak_*_20260822`. Spec: docs/superpowers/specs/gop-db/2026-08-22-finance-prepick-extend-request-design.md

- finance-addition-accounting-request (port gốc) — port màn ERP **Phiếu yêu cầu hạch toán bổ sung** sang phân hệ Tài chính, route `/finance/addition-accounting-requests` → @khoipv → .plans/gop-db/finance-addition-accounting-request/plan.md
  Hoàn thành: 2026-08-26 — user xác nhận xong. 6 loại tạo mới + loại 7 chỉ xem/in, dừng ở *Chờ duyệt*. BE 17 file mới · FE 10 file mới · 24 route · **4 quyền id 1177–1180** · **0 migration** (dùng chung 5 bảng ERP). Vá **10 lỗi/lỗ hổng của ERP** — nặng nhất: route xoá là **GET** không gate, `store()` gán thẳng `status` — cùng 7 lỗi FE chỉ Playwright bắt được. (Đợt sửa theo yêu cầu user sau đó là mục Phase 11 hoàn thành 2026-09-10 ở trên.) Spec: docs/superpowers/specs/gop-db/2026-08-25-finance-addition-accounting-request-design.md

- catalog-docs (loạt 10 màn danh mục) — bộ tài liệu SRS + HDSD + Testcase cho 6 màn Địa lý · 3 màn Tài chính · 1 màn Công việc-lỗi thiết bị → @junfoke → .plans/gop-db/geo-catalogs-docs/plan.md · finance-catalogs-docs/plan.md · device-error-catalog-docs/plan.md
  Hoàn thành: 2026-08-20 — user chốt phạm vi 2026-08-17, giao **30 file = 10 SRS + 10 HDSD + 10 testcase, tổng 587 TC** (Địa lý 327 · Tài chính 147 · Lỗi thiết bị 113), kèm generator `gen_srs.py`/`gen_testcase.py`/`gen_hdsd.py` + file cấu hình commit cùng thư mục để tái sinh. ⚠️ **Phát hiện phải nêu trong tài liệu: 6 màn địa lý (`/human/nations` · `areas` · `provinces` · `districts` · `wards` · `hamlets`) KHÔNG gắn quyền ở bất kỳ endpoint nào** — kể cả Thêm/Sửa/Xóa/Khóa, ai đăng nhập cũng sửa được danh mục dùng chung toàn hệ thống; ngược lại 3 màn Tài chính (`works` · `cost-debts` · `source-capitals`) mỗi màn đúng 1 quyền cho cả xem lẫn sửa. Nghiệp vụ đáng nhớ của màn lỗi thiết bị: **trùng tên xét theo TỪNG LOẠI** (6 loại) nên đổi ô Loại khi sửa sẽ kiểm tra lại trùng tên trong loại mới; nút Xóa cần CẢ HAI điều kiện đang Hoạt động VÀ chưa phát sinh chứng từ; 4 ô để trống thì hệ thống tự điền, trong đó 2 ô lấy theo cấu hình công ty nên **hai người ở hai công ty khác nhau ra kết quả tính khác nhau** — đúng thiết kế. ⚠️ Lúc chụp ảnh, bảng `catalog_histories` chưa migrate trên local nên cửa sổ Lịch sử phải chụp ở cổng dev.

- dong-bo-quy-tac-chung — đồng bộ bộ quy tắc chung (đã chốt ở màn Khách hàng) sang **20 màn danh mục** → @dnsnamdang → .plans/gop-db/dong-bo-quy-tac-chung/plan.md
  Hoàn thành: 2026-08-17 — bắt đầu 2026-08-15, user soi lại nhiều đợt và chốt bổ sung 3 lần giữa chừng. Áp 2 quy tắc nghiệp vụ (lọc "Loại hoạt động" của Lịch sử = 3 nhóm cố định; **bản ghi đã khoá không cho sửa/xoá — chặn ở BE bằng 423 qua middleware dùng chung**, FE ẩn nút + chặn vào thẳng URL `/edit`) và 15 quy tắc giao diện của skill `list-page`/`button-convention` cho: 6 màn CSKH (`device-errors`, `services`, `levels`, `note-maintenances`, `costs`, `service-price-config`, `serials`) · 6 màn địa lý · 3 màn tài chính + `banks`/`account-banks`/`product-transfer-requests`. Kèm 4 hạ tầng dùng chung mới: **lịch sử thay đổi cho 18 màn danh mục** (bảng `catalog_histories` + trait `LogsCatalogHistory` + `CatalogHistoryModal`), popup chuẩn hoá, **popup "Chọn trường xuất file" cho 10 màn có nút Xuất**, và bộ lọc "Người thực hiện" trong lịch sử. 🐞 Lỗi gốc đáng nhớ tìm ra khi user báo "cột Người cập nhật vẫn trống": `Nation` kế thừa `Model` THUẦN nên không có hook audit → `nations.updated_by` luôn NULL; còn `Area`/`Province`/`Ward` giữ 2 hook đồng bộ ERP thời chưa gộp DB — sau khi gộp, `TpArea` trỏ về CHÍNH bảng `areas` nên hook ghi đè và đóng dấu `updated_by` bằng **id bảng `employee_infos`** trong khi cột lưu `employees.id` → join ra rỗng. Đã gỡ hẳn 3 hook + set tay `created_by`/`updated_by` trong `NationService`, đo lại bằng tinker. Có migration (bảng `catalog_histories` + 2 migration bổ sung người tạo cho danh mục tài chính). Đợt cuối rà lại 20/20 màn theo toàn bộ skill + xử lý phản hồi Redmine #11073 (ghi chú #12–#27).

- finance-bill-adjust-dept-request — Phiếu yêu cầu điều chỉnh công nợ → @khoipv → .plans/gop-db/finance-bill-adjust-dept-request/plan.md
  Hoàn thành: 2026-09-03 — user nghiệm thu đã xong (18 phase gốc xác nhận 2026-08-24; mở lại 2026-09-03 fix 4 việc, 2 FE + 2 BE, không migration). Phase 20: đổi khách hàng/NCC ở một dòng phải XOÁ hợp đồng cũ — ERP xoá ở 4 chỗ (`BillAdjustDeptRequestDetail`/`DetailItem` × `chooseCustomer`/`chooseSupplier`), HRM thiếu hẳn nên phiếu lưu xuống DB là cặp "KH A + hợp đồng của KH B", `contractable_id` trỏ sai, bước tạo phiếu kế toán ghi sổ nhầm công nợ (lỗi dữ liệu, không phải hiển thị). Phase 21: lệch tổng tiền báo inline ở cột Số tiền bên "Điều chỉnh đến" (dòng cuối của nhóm) kèm số thiếu/thừa, trước chỉ 1 toast chung nên bảng nhiều nhóm không biết nhóm nào. Phase 22 + 22b + 22c: lỗi 422 của BE đổ về đúng từng ô (`details.1.items.0.customer_new_id` → ô Khách hàng dòng "đến" nhóm 1, viền đỏ); dịch câu lỗi `gt`/`integer`/`array`/`string`/`boolean` ngay trong Request (user chốt KHÔNG sửa `lang/vi/validation.php` dùng chung); toast rút về "Vui lòng kiểm tra dữ liệu nhập", chỉ lỗi không có chỗ inline (vd `status`) mới đọc nguyên văn. Phase 22d: Từ chối xong về màn danh sách — `changeStatus()` (dùng chung Gửi duyệt + Từ chối) thêm cờ `backToList`, Gửi duyệt vẫn `$router.go(0)`; popup lý do chỉ đóng khi thành công (trước lỗi cũng đóng, mất lý do vừa gõ). Kiểm chứng Playwright bấm Gửi duyệt thật: 422 hiện đúng ô, 2 ô Số tiền báo "Phải lớn hơn 0", 4 ca toast ra câu chung, nhóm khớp tiền không báo gì. Chưa kiểm chứng: phiếu NCC ngoại tệ (16 cột) · màn sửa phiếu có dữ liệu thật. Còn nợ: Excel phiếu lệch ERP · nút "Chọn nhanh hợp đồng" · SRS/testcase/HDSD · dọn 6 phiếu `TEST.DNDCCN.*` · `lang/vi/validation.php` còn ~52 khoá tiếng Anh. ⚠️ Bài học: lượt đầu user báo "vẫn chưa được" là do HMR Nuxt 2 giữ component cũ, code đã đúng — sửa FE mà trình duyệt không đổi thì Ctrl+Shift+R trước khi nghi code. Spec: docs/superpowers/specs/gop-db/2026-08-17-finance-bill-adjust-dept-request-design.md

- finance-bill-income-report — bộ tài liệu bàn giao (SRS + HDSD + testcase) → @khoipv → .plans/gop-db/finance-bill-income-report/plan.md (mục "Phase T")
  Hoàn thành: 2026-09-05 — sinh 3 tài liệu cho màn Phiếu báo có + màn phụ Tổng hợp tiền về ngân hàng, kèm 3 generator commit cùng chỗ: `SRS - Phieu bao co.docx` (form 2026-08-28, 4 phần, 16 chức năng FR-01…FR-16, 14 quy tắc nghiệp vụ, 58 trang), `HDSD_Phieu_bao_co.docx` (8 phần + TỔNG QUAN, click-by-click từng trường + giá trị điền sẵn + mục hướng dẫn theo từng quyền, 44 trang), `testcase.xlsx` (204 TC, P0 54%, 13 section La Mã + 13 TC phân quyền gồm 5 TC gọi thẳng chức năng bỏ qua giao diện). Ảnh chụp thật 27 tấm trong `bir_shots/` — KHÔNG commit. ⚠️ Cổng dev hrm-crm thiếu 3 chunk giao diện nên không mở được màn Tạo/Sửa/Chi tiết; ảnh form + popup + chi tiết + màn tổng hợp phải chụp trên bản chạy local (cùng DB gộp). Cấu hình cột của tài khoản DNS Admin đã đưa về mặc định để ảnh đúng chuẩn.

- finance-bill-income-report — sửa lỗi màn Phiếu báo có (Phase F) → @khoipv → .plans/gop-db/finance-bill-income-report/plan.md (mục "Phase F")
  Hoàn thành: 2026-09-03 — user xác nhận đã xong. 9 việc báo trong 1 phiên: tách cột Số tài khoản / Tên tài khoản ở bảng chi tiết (trước đó cả 2 cột đều in "số - tên"); nút Duyệt màn chi tiết về teal #1abc9c; nút thứ 2 của form đổi nhãn "Lưu và duyệt" (cờ `save_and_approve`, trước khai nhầm `save_and_submit_approve`); toast mở phiếu đã bị xóa ở tab khác → "Không tìm thấy dữ liệu" (chỉ với 404); dựng lại file mẫu import (viền, tiêu đề teal, ngày dd/mm/yyyy, ô tiền `#,##0`); nút Quay lại màn Điều chỉnh công nợ về đúng phiếu qua `?back_url=`. 3 lỗi validate: cột Số tiền chưa bao giờ báo bắt buộc (`min:0` + FE quy ô rỗng thành 0 → đổi `gt:0`, dữ liệu thật 10.207 dòng không có dòng nào money=0); ô Diễn giải đầu phiếu thiếu `:invalid` + `<V2BaseError>` nên chỉ ra toast chung → nối lỗi inline; nới trần Diễn giải 255 → 500 ký tự cả 2 ô. CÓ MIGRATION `2026_09_03_000001_widen_note_on_bill_income_reports_table` (đã chạy, 0 dòng ảnh hưởng); cột chi tiết là TEXT nên chỉ thêm rule. ⚠️ Bảng dùng chung 2 cổng — diễn giải > 255 ký tự hiện nguyên vẹn bên ERP, chưa rà bố cục màn/bản in ERP.

- ⚠️ base-confirm-modal — sửa COMPONENT DÙNG CHUNG, cả team cần biết → @khoipv → components/modal/base-confirm-modal.vue
  Hoàn thành: 2026-09-03 — user chốt sửa ở component chung thay vì vá từng màn. Popup xác nhận tự bật `danger` (nút đỏ + icon cảnh báo) khi `text-accept` bắt đầu bằng "Xóa"/"Xoá", trừ "Xóa trắng"; prop `danger` đổi mặc định false → null (chưa chỉ định) nên màn nào truyền thẳng `:danger` vẫn được tôn trọng. Lý do: ~101 chỗ hỏi xóa qua popup này quên truyền `danger`. Đã chạy hàm suy luận trên toàn bộ `text-accept` đang có: chỉ nhóm "Xóa" đổi màu, Khóa/Mở khóa/Duyệt/Xác nhận/Xóa trắng giữ nguyên.

- finance-bill-payment-request — nới validate Lưu nháp → @khoipv → .plans/gop-db/finance-bill-payment-request/plan.md (mục "Nới validate LƯU NHÁP")
  Hoàn thành: 2026-09-03 — user xác nhận đã xong. Lưu nháp (`status = 1`) chỉ còn bắt buộc Loại chi; bỏ `required` của lý do chi, hình thức TT, tiền tệ, tỷ giá, ngày chốt, đối tượng nhận tiền và toàn bộ `details.*`, rule định dạng giữ nguyên. Sửa BE 2 file (`BillPaymentRequestStoreRequest` — Update kế thừa; `BillPaymentRequestService::masterPayload()`), FE không đụng vì mọi thông báo "Bắt buộc nhập" đều do BE trả. Không migration. Quyết định này THAY ràng buộc 2026-08-22 (dòng chi tiết đã thêm phải đủ hợp đồng + số tiền). Nút Lưu và gửi duyệt (`status = 2`) không đổi. ⚠️ 4 cột `reason`/`type_payment`/`type_money_id`/`exchange_rate` NOT NULL không default → service phải đổ mặc định (TM · VNĐ · tỷ giá 1 · lý do rỗng), thiếu là lưu nháp trả 500.

- finance-bill-payment-authorization — lịch sử thay đổi màn Ủy nhiệm chi (Phase L) → @khoipv → .plans/gop-db/finance-bill-payment-authorization/plan.md (mục "Phase L")
  Hoàn thành: 2026-09-03 — VERIFIED Playwright. Màn này trước đó CHƯA có gì (không nằm trong whitelist, BE chỉ ghi log cho màn Đề nghị, FE trống) → bổ sung đầy đủ như 2 màn phiếu trước, dùng bảng chung `catalog_histories` + trait `LogsCatalogHistory`, FE `CatalogHistoryModal` + `SystemInfoSection`. Không quyền riêng, không migration. Khác 2 màn kia: UNC không có Gửi duyệt / Duyệt / Hủy (RULING U-UNC-6) — chỉ Lưu (status 1) và Lưu và duyệt (status 3) nên dòng `change_status` chỉ sinh ở `update()`; bảng không có cột tổng; dòng chi tiết nhận diện bằng hợp đồng / nhân viên, không có khách hàng - NCC.

- finance-bill-payment — lịch sử thay đổi màn Phiếu chi tiền (Phase L) → @khoipv → .plans/gop-db/finance-bill-payment/plan.md (mục "Phase L")
  Hoàn thành: 2026-09-03 — VERIFIED Playwright. Trước đó chỉ log đổi trạng thái; nay đầy đủ: tạo / sửa / bảng chi tiết theo từng dòng / duyệt kèm số chi / hủy kèm lý do / xóa. Không migration. ⚠️ Điểm rủi ro đã kiểm: `BillPaymentDetailResource` ĐỌC NGƯỢC `catalog_histories` (bảng `bill_payments` không có cột `note`) để dựng `cancel_reason` / `cancel_note` / `approve_note` — đã chụp baseline 2 dòng log thật trước/sau khi sửa whitelist, diff rỗng.

- finance-bill-income — lịch sử thay đổi màn Phiếu thu tiền (Phase L) → @khoipv → .plans/gop-db/finance-bill-income/plan.md (mục "Phase L")
  Hoàn thành: 2026-09-03 — VERIFIED Playwright. Làm theo skill `entity-history` §5.1 + màn danh sách khách hàng, phạm vi ĐẦY ĐỦ như màn Phiếu báo có (không theo bản rút gọn của Phiếu chi tiền): tạo mới / thay đổi thông tin / bảng chi tiết theo từng dòng / duyệt kèm số thực thu (tách 2 dòng log) / hủy kèm lý do / xóa. Không quyền riêng, không migration — bảng chung `catalog_histories` + trait `LogsCatalogHistory`, FE `CatalogHistoryModal` (popup màn danh sách) + `SystemInfoSection` (khối trong màn chi tiết).

- finance-bill-income-report — Phiếu báo có, port ERP `bill_income_report` → HRM → @khoipv → .plans/gop-db/finance-bill-income-report/design.md + plan.md
  Hoàn thành: 2026-09-03 — user xác nhận đã xong (nghiệm thu 2026-08-24, Phase 8 xong code 2026-08-28). Port `admin/income-expenditure/bill_income_report` sang phân hệ Tài chính, route `/finance/bill-income-reports` + `/summarize-money`. Phạm vi: danh sách; tạo/sửa/xóa nháp; duyệt kèm ghi bút toán sổ cái; chi tiết + cờ "Không báo tiền về"; 3 loại thu; Tổng hợp tiền về ngân hàng + xuất Excel chọn trường; Import Excel sao kê; Lịch sử thay đổi. KHÔNG thay đổi schema (lịch sử dùng bảng chung `catalog_histories`); 3 quyền mới id 1539-1541 (guard `api`, tên trùng ERP). Bút toán HRM sinh khớp 100% bút toán ERP đã ghi (7 phiếu thật / 38 bút toán / 24 cột denormalize). Phase 8 sửa theo phản hồi, chỉ màn danh sách: "Ngày lập/Người lập" → "Ngày tạo/Người tạo"; "Diễn giải" → "Ghi chú" (cột + ô lọc, áp cả màn Tổng hợp tiền về ngân hàng); thêm cột Người cập nhật (BE trả `updated_by_name`) + Ngày cập nhật mặc định ẩn trong popup Cấu hình cột — 2 file BE + 2 file FE, không migration, không quyền mới. Spec: docs/superpowers/specs/gop-db/2026-08-24-finance-bill-income-report-design.md

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
  **Bộ tài liệu bàn giao (Phase N, 2026-09-03)**: `testcase.xlsx` **152 TC** (P0 70%, form 17 cột),
  `HDSD_Phiếu chi tiền.docx` **47 trang**, `SRS - Phiếu chi tiền.docx` **57 trang** (form 2026-08-28,
  14 chức năng FR-01→FR-14, 17 quy tắc BR). 25 ảnh chụp thật → `pc_shots/` (chỉ để local);
  riêng màn IN chụp trên cổng LOCAL vì trang in tự bật hộp thoại in và khoá phiên điều khiển.
  **KHÔNG ghi gì vào DB dev** — dev đã sẵn phiếu Đang tạo + Chờ chi tiền; các popup Duyệt/Hủy/Xóa
  chỉ mở để chụp rồi Đóng.
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
  **Bộ tài liệu bàn giao (Phase M, 2026-09-03)**: `testcase.xlsx` **169 TC** (P0 61%, form 17 cột),
  `HDSD_Phiếu thu tiền.docx` **44 trang**, `SRS - Phiếu thu tiền.docx` **52 trang** (form 2026-08-28,
  13 chức năng FR-01→FR-13, 16 quy tắc BR). 26 ảnh chụp thật → `pt_shots/` (chỉ để local); 3 ảnh mục
  Lịch sử chụp trên cổng LOCAL vì cổng dev chưa deploy Phase L. Đã tạo + xóa 1 phiếu nháp
  `TPE.PT0926.00001` trên dev để chụp Sửa/Xóa (dữ liệu trả nguyên trạng 2.379 phiếu);
  **KHÔNG bấm Duyệt/Hủy trên phiếu thật** vì 2 thao tác đó không hoàn tác được.
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
  **Bộ tài liệu bàn giao (Phase 9, 2026-09-03)**: `testcase.xlsx` **188 TC** (P0 50%, form 17 cột —
  đã XÓA bản 15 cột cũ ngày 07/08 theo yêu cầu user), `HDSD_Phiếu yêu cầu chuyển hàng.docx`
  **48 trang**, `SRS - Phiếu yêu cầu chuyển hàng.docx` **52 trang** (form 2026-08-28, 14 chức năng
  FR-01→FR-14, 16 quy tắc BR). 31 ảnh chụp thật trên `hrm-crm.eteksofts.com` → `pycch_shots/`
  (chỉ để local). 3 generator `gen_testcase.py` / `gen_hdsd.py` / `gen_srs.py` commit kèm.
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
  Trạng thái: **PHASE 1-10 CODE DONE + VERIFIED** (2026-09-04; Phase 10 đưa form Tạo/Sửa về bố cục
  ERP — redmine 11300) — 2 màn "Danh mục tài khoản" +
  "Danh mục loại tài khoản"; màn đầu tiên của phân hệ Tài chính nên dựng luôn khung `Modules/Finance`.
  Bước tiếp: Phase 7 đối chiếu 2 cổng (cần bật ERP local) + tạo 2 file mẫu Excel trong `hrm-client/static/`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-07-30-finance-account-catalog-design.md | Tóm tắt: .plans/gop-db/finance-account-catalog/design.md

- tach-phan-he-erp-hrm → @junfoke → .plans/gop-db/tach-phan-he-erp-hrm/plan.md
  Trạng thái: **XONG GIAI ĐOẠN 1 (khung phân hệ + menu)** (2026-07-30), đã test thật 9 màn trên dev.
  Quy hoạch lại 24 phân hệ / 5 nhóm theo Sơ đồ tổng thể v1.6; dựng base 17 phân hệ mới.
  Bước tiếp: user test 17 màn edit/detail. Giai đoạn 2 = `chuyen-code-phan-he`.
  Chi tiết + gotcha: plan.md | Spec: docs/superpowers/specs/gop-db/2026-07-30-tach-phan-he-erp-hrm-design.md | Tóm tắt: .plans/gop-db/tach-phan-he-erp-hrm/design.md
