# Báo cáo phát triển thị trường - Khách hàng — popup theo khuôn báo cáo kế hoạch & kết quả (07/10/2026)

Màn: `/assign/report/customer-market-development` · nhánh `gop_db` (cả 2 repo).
Hồ sơ gốc của feature (làm trên `tpe`, Phase 1→7): `.plans/bao-cao-phat-trien-thi-truong-khach-hang/`.
Khuôn tham chiếu: `employee-work-performance/plan.md` mục 06/10 (10) (12).

## Quyết định đã chốt (user 07/10/2026)

1. Popup: bấm **tên meeting** → panel chi tiết meeting DÙNG CHUNG (`ReportMeetingDetailDrawer`, `above-modal`):
   Người chủ trì · File đính kèm · Xem biên bản · Xem chi tiết (tab mới). BE nới `Meeting::canView` theo phạm vi
   quyền báo cáo này (dùng chung `canViewByReportScope`).
2. In + Excel popup **theo đủ khuôn mới**: tiêu đề theo chỉ tiêu · dòng đối tượng từ `key` · dòng điều kiện bỏ "Tất cả"
   · bộ cột = đúng bộ cột đang hiện trên popup · theo ô tìm + thứ tự đang sắp. Excel tải thẳng từ server
   (`drill/export`, `?token=`), bỏ blob FE. Bản in màn chính cũng bỏ "Tất cả".
3. Cột "Meeting KH" → **"Meeting kế hoạch"** (bảng, tooltip, bản in, Excel màn chính).
4. Cột "Ngày họp" → **"Thời gian meeting"** dạng Từ → Đến, gọn khi cùng ngày (`07/09/2026 13:00 → 15:00`, khác ngày
   ghi đủ 2 vế); áp cả popup thường, popup Huỷ, bản in, Excel; sắp theo giờ bắt đầu.
5. Cột Trạng thái: badge chữ + viền màu theo màu BE (`Meeting::STATUS_COLORS`), giống báo cáo kế hoạch.

## Tasks

- [x] BE: Meeting::canView + service (end_date, status_color, public permission helpers, q + sort cho In/Excel)
- [x] BE: PrintService (tiêu đề / đối tượng / điều kiện / bộ cột theo popup) + blade chi tiết; đổi tên cột bảng theo dõi
- [x] BE: `drill/export` (controller + route + Export + blade) + unit test đầu bản in
- [x] FE: DevelopmentDrillModal (Thời gian meeting, badge trạng thái, bấm tên → panel, In/Excel gửi cột + q + sort)
- [x] FE: DevelopmentTable đổi tên cột; index.vue dựng ReportMeetingDetailDrawer + Xem biên bản + tải Excel popup
- [x] Kiểm Playwright MCP (1366×800, tài khoản admin) + cập nhật e2e: `customer-market-development.spec.ts` (4 ca đổi nhãn /
      tiêu đề bản in / bỏ "Tất cả", sửa `ownFilters` → `filters` vốn đỏ sẵn, thêm 1 ca popup mới) · `report-meeting-drawer.spec.ts`
      ca 5 (nhân viên thường CHỈ có quyền 1187 xem được meeting trong báo cáo, không quyền vẫn 403). Spec biên dịch được,
      CHƯA chạy.
- [ ] User check · chạy e2e khi user yêu cầu

### Checkpoint — 2026-10-07
Vừa hoàn thành: 5 yêu cầu (panel meeting, In/Excel popup khuôn mới, "Meeting kế hoạch", "Thời gian meeting", badge Trạng thái).
Đo MCP: popup Năm nay 783 meeting · cột thời gian 0 ô cắt chữ · panel z 1060 > popup 1050, API 200 · bản in lọc Hoàn
thành + "khảo sát" + sắp giảm = 6 dòng đúng thứ tự, 13 cột như popup, không "Tất cả" · Excel .xlsx 13 cột, cột tiền số thật
`#,##0` · bản in node 3 cấp có dòng đối tượng. Unit `CustomerMarketDevelopmentPrintHeaderTest` 5 ca + 2 cũ xanh.
Bước tiếp theo: user kiểm trên app; chạy e2e khi được yêu cầu.
Blocked: —

## Đợt 2 — xử lý 3 vấn đề phát sinh (user chốt 07/10/2026: "xử lý luôn")

Đính chính: "3,208 KH mới" KHÔNG phải lỗi fail-open (memory đó là của báo cáo KHÁC `customer-development`). Đo: 3,208 = số
KH tạo năm 2026 ở DB ERP CŨ `erp2326` (dừng 27/07/2026); DB gộp có 3,809 (tới 15/09/2026) → cùng gốc với vấn đề 1.
Vấn đề 1: 714/783 meeting năm 2026 chưa có `province_id`, cả 714 tra được tỉnh từ `customers` trong DB gộp.

- [x] A1. MeetingMarketSnapshotService đọc `customers`/`provinces` DB gộp (bỏ `erp2326`)
- [x] A2. getNewCustomerRows + mapCreatorsToEmployees đọc DB gộp (`employees` gộp chứa trọn ERP: 1085/1085 khớp)
- [x] A3. BackfillMeetingProvinceSeeder đọc DB gộp + CHẠY vào DB local `hrm_erp` (user cho phép) · ghi deploy.md
- [x] A4. Gỡ 3 mốc @TODO-GOPDB · unit test
- [x] B1. BE phân trang bảng theo dõi (cắt dòng cấp 1, TỔNG + dải tổng hợp vẫn tính toàn kỳ) — viết lại Phase 7 trên nền gop_db
- [x] B2. BE popup: lọc `p_*` + `q` + sắp + phân trang + summary / allocations / filter_options / has_part
- [x] B3. FE: bảng theo dõi phân trang BE; popup dùng phân trang server của V2BaseReportModal
- [x] B4. Kiểm MCP (đo payload trước/sau) + cập nhật e2e (spec UI: ca lọc popup kiểu server, ca In danh sách, ca phân trang
      popup đổi tên biến; .api.spec Phase 7 nay khớp). Spec biên dịch được, CHƯA chạy.

### Checkpoint — 2026-10-07 (đợt 2)
Vừa hoàn thành: A1-A4 + B1-B4.
- Seeder vá chạy vào DB local `hrm_erp` (đã kiểm đích 127.0.0.1/hrm_erp, không config cache): 717 meeting được vá tỉnh,
  8 meeting vá tên/mã KH → còn 0 meeting thiếu tỉnh, 0 lệch với `customers`.
- Đo MCP (Năm nay): bảng tiêu chí Khách hàng 5 MB → 86 KB (50/4,214 dòng cấp 1, trang 2 STT 51→100, dòng TỔNG giữ 783);
  popup Kế hoạch meeting 74 KB, popup KH mới 2.1 MB → 263 KB (phần lớn là 3,809 tuỳ chọn ô Khách hàng); mở popup = 1
  request; lọc Hoàn thành 473/783, KPI tính toàn tập, dropdown không co; In + Excel popup 473 dòng khớp thứ tự; bản in
  màn chính vẫn đủ 4,214 dòng cấp 1 dù gửi page=1&per_page=20. Thị trường ra tỉnh thật (Hà Nội 259/473…).
- Unit: CustomerMarketDevelopment* 11/11 xanh (GopDb 2 · Pagination 2 · PrintHeader 5 · cũ 2).
Bước tiếp theo: user kiểm trên app; chạy e2e khi user yêu cầu.

### Deploy (production, nhánh gop_db)
1. Deploy code BE + FE như thường (KHÔNG có migration).
2. Chạy 1 lần: `php artisan db:seed --class="Modules\Assign\Database\Seeders\BackfillMeetingProvinceSeeder"` — vá tỉnh
   cho meeting cũ (chỉ ghi ô đang rỗng, chạy lại vẫn an toàn). Không chạy thì meeting cũ vẫn dồn "Chưa xác định thị trường".

## Ngoài phạm vi (ghi lại, chưa làm)

- ~~3 vấn đề phát sinh đợt 1~~ — đã xử lý ở Đợt 2 (đọc DB gộp + vá snapshot + phân trang BE).
- Bảng tiêu chí Thị trường Năm nay vẫn ~685 KB/trang: 37 dòng cấp 1 nằm gọn 1 trang nhưng mang trọn nhánh con (đúng thiết kế
  "không cắt cha lìa con"). Nếu cần nhẹ hơn thì phải tải nhánh con khi bung — chưa làm.

### Checkpoint — 2026-10-07 (wrap up)
Vừa hoàn thành: Đợt 1 (popup khuôn mới) + Đợt 2 (DB gộp, phân trang BE); ĐÃ COMMIT + PUSH gop_db (api e20e02e04, client c62d1a79b). Seeder vá tỉnh đã chạy DB local
Đang làm dở: —
Bước tiếp theo: deploy production + chạy BackfillMeetingProvinceSeeder 1 lần · chạy e2e (customer-market-development{,.api}, report-meeting-drawer) khi user yêu cầu · chờ user: thêm test drill? phòng có chia bộ phận theo dữ liệu hay danh mục?
Blocked: —

## Đợt 3 — "Meeting bị huỷ" chia theo nguồn huỷ (user chốt + "Làm" 07/10/2026)

Quyết định: giữ thẻ tổng "Meeting bị huỷ" + 2 số con bấm được: **Quá hạn huỷ tự động** (`meetings.auto_cancelled_at` có
giá trị — job #11014 tự huỷ khi quá hạn nhập biên bản, kể cả khi người dùng đã ghi lý do trước đó) / **Huỷ có lý do** (người
dùng huỷ, gồm cả huỷ tay không ghi lý do). 2 số luôn cộng bằng tổng. Chỉ ở khối tổng hợp — bảng theo dõi / bản in / Excel
màn chính giữ 1 cột Huỷ.

- [x] BE: dòng meeting thêm `is_auto_cancelled`; `summary` trả `cancelled_auto` / `cancelled_manual`; popup nhận 2 chỉ tiêu
      mới; PrintService nhãn tiêu đề ("DANH SÁCH MEETING QUÁ HẠN HUỶ TỰ ĐỘNG" / "… HUỶ CÓ LÝ DO").
- [x] FE: DevelopmentSummary 2 dòng số con dưới thẻ (tooltip ⓘ từng dòng); popup dùng bộ cột có "Lý do huỷ" cho cả 3 chỉ tiêu huỷ.
- [x] Đo MCP (Năm nay, 1366px): API 99 = 89 + 10; DOM đúng số, không cắt chữ, 3 thẻ cao bằng nhau 112px; popup tự huỷ 89 dòng
      (ghi chú "Tự động hủy: quá hạn…"), popup có lý do 10 dòng; cả 2 có cột Lý do huỷ, tiêu đề đúng.
- [x] PHPUnit `CustomerMarketDevelopmentCancelSplitTest` 3 ca + 4 bộ cũ xanh. E2E thêm 1 ca (biên dịch được, CHƯA chạy).
- [x] Góp ý: xếp 2 số con CÙNG DÒNG số chính ("99 12.6% · Quá hạn 89 · Có lý do 10") để khối không cao thêm — nhãn rút gọn
      Quá hạn / Có lý do (1366px không đủ chỗ cho nhãn đầy đủ: cần ~292px, thẻ chỉ ~195px), tên đầy đủ + giải thích dồn vào ⓘ
      của thẻ; lưới thẻ `minmax(max-content, 1fr)` để thẻ huỷ không ép nhãn thẻ khác xuống dòng. Đo 1280/1366/1920: mọi thẻ
      62px (bằng trước khi chia), khối 104px, nhãn 1 dòng, không tràn; bấm 2 số ra popup 89 / 10. E2E sửa theo (chưa chạy).
- [ ] User kiểm · commit khi user yêu cầu.

## Đợt 4 — "Nhu cầu thu thập được" đếm theo SỐ NHU CẦU (user chốt nội dung 07/10/2026 — CHƯA có lệnh code)

Hiện trạng (đo 07/10, Năm nay, DB local): chỉ tiêu `demand` đếm số MEETING có ≥ 1 nhu cầu (`has_demand`) = **151**; giá trị
(108.0 tỷ) đã cộng mọi nhu cầu. `attachInvestmentDemands()` có truy `COUNT(*) demand_count` theo meeting nhưng bỏ đi.
Số nhu cầu thật = **187** (141 meeting × 1 · 6 × 2 · 2 × 3 · 2 × 14). Popup "Nhu cầu đầu tư thu thập" đang là danh sách
meeting (151 dòng, cột "Nhu cầu đầu tư ghi nhận" gộp tên bằng dấu phẩy).

Logic đã chốt:
1. **Đếm theo số nhu cầu** (`meeting_investment_demands`), không theo số meeting có nhu cầu.
2. **Đổi ĐỒNG LOẠT**: thẻ tổng hợp, cột "Nhu cầu" bảng theo dõi, dòng TỔNG, bản in + Excel màn chính — cùng 1 cách đếm;
   dòng cha vẫn = tổng dòng con (số nhu cầu cộng được).
3. **Popup: 1 dòng = 1 nhu cầu** → bấm 187 ra đúng 187 dòng (giữ quy tắc số bấm = số dòng popup). Meeting có 3 nhu cầu
   thành 3 dòng cùng mã/tên meeting, mỗi dòng 1 nhu cầu + giá trị riêng. Sắp / lọc / phân trang / KPI / bản in / Excel popup
   theo tập dòng nhu cầu.
4. Nhãn phải nói rõ đơn vị là NHU CẦU (vd "Nhu cầu thu thập được" + ⓘ "Đếm theo số nhu cầu — 1 meeting có thể có nhiều nhu
   cầu"); có thể kèm "x meeting" ở dòng phụ — chốt khi làm mockup/đo bố cục (thẻ phải giữ 1 dòng số, cao 62px).

Phạm vi dự kiến khi có lệnh: BE `CustomerMarketDevelopmentService` (giữ `demand_count`, `metrics.demand` cộng
`demand_count`, `getDrillRows` metric `demand` tách dòng theo nhu cầu), PrintService + blade nếu đổi nhãn; FE
DevelopmentSummary / DevelopmentTable / DevelopmentDrillModal; PHPUnit + e2e. Không migration / seeder / quyền.


**CHỐT 07/10/2026 — phương án C:** đếm theo **SỐ NHU CẦU**, **chỉ meeting Hoàn thành** (Năm nay: 181 nhu cầu · 107.6 tỷ;
trước đây 151 meeting · 108.0 tỷ). Nhu cầu nằm ở meeting Lên lịch / Chốt lịch / Huỷ (6 meeting, 6 nhu cầu, 0.3 tỷ) KHÔNG
tính — khớp ⓘ "chỉ meeting hoàn thành mới ghi nhận được nhu cầu". Giá trị dự kiến cùng tập (chỉ Hoàn thành). Áp đồng
loạt: thẻ tổng hợp, cột Nhu cầu + Giá trị dự kiến bảng theo dõi, dòng TỔNG, bản in, Excel; popup 1 dòng = 1 nhu cầu.

- [x] User "Làm" (thẻ hiển thị "181 · 107.6 tỷ", ⓘ ghi rõ đơn vị). BE: `attachInvestmentDemands` lấy từng nhu cầu (1 query,
      gom ở PHP: `demand_count`, `demand_list`); `metrics.demand` = Σ số nhu cầu của meeting Hoàn thành, `investment` cùng tập,
      thêm `demand_meetings`; popup `demand` lọc Hoàn thành + `explodeDemands()` 1 dòng / nhu cầu (`row_key` = meeting-nhu cầu);
      `getDrillPage` KPI đếm meeting khác nhau, mọi dòng có `row_key`, bỏ `demand_list` khỏi payload. Bản in / Excel popup đi
      qua `getDrillRows` nên tự theo. FE: thẻ + dòng mục tiêu + ⓘ; tooltip cột Nhu cầu / Giá trị dự kiến; popup `row-key`,
      đơn vị "nhu cầu".
- [x] Đo MCP Năm nay: thẻ 181 · 107.6 tỷ (cao 62px), dòng TỔNG 181, popup "181 / 181 nhu cầu", KPI 145 meeting; tải đủ 181 dòng
      popup qua API: 145 meeting, tổng 107.631 tỷ = cây, khoá không trùng, meeting 246 ra 3 dòng 3 nhu cầu riêng giá.
      (11 tên nhu cầu có dấu phẩy là tên gốc danh mục, không phải gộp.)
- [x] PHPUnit `CustomerMarketDevelopmentDemandCountTest` 3 ca + 5 bộ cũ xanh. E2E API thêm 1 ca (chưa chạy).
- [ ] User kiểm · commit khi user yêu cầu.

## Đợt 5 — ô chọn cấp xem về tiêu đề cột theo khuôn chung (user "Làm" 07/10/2026)

- [x] DevelopmentTable.vue: bỏ thanh "Cấp xem" trên bảng (dựng 14/09 vì select `sm` 32px + dropdown bị khung cắt — cả 2 đã
      hết với khuôn `xs` 26px + dropdown gắn `<body>`); `V2BaseSelect size="xs"` trong `th` "Nội dung theo dõi", nhãn + ô cùng
      1 dòng (`flex-wrap: nowrap`), không ép height.
- [x] Đo MCP 1366/1920: ô 26×230px, chữ không tràn, căn giữa nhãn (lệch 0), 9 ô tiêu đề cao 38px; kỳ tháng (bảng 2 dòng)
      dropdown nằm ở body, 4/4 lựa chọn bấm trúng; chọn "Tất cả cấp" 38 → 1,576 dòng.
- [x] E2E: viết lại 2 ca "Bộ chọn cấp xem" (nằm trong th + helper levelSelect + dropdown bấm trúng + thao tác thật) — chưa chạy.
- [ ] User kiểm · commit khi user yêu cầu.

## Đợt 6 — popup Nhu cầu theo cột nhu cầu (user "Làm" 07/10/2026)

Chốt: bỏ cả Loại meeting + Trạng thái (cột + ô lọc) ở popup Nhu cầu — luôn 1 giá trị (đo: 145/145 meeting là "Họp tìm hiểu &
Giới thiệu sản phẩm", chỉ Hoàn thành); các popup khác (7 loại meeting) giữ nguyên. Giữ 2 cột nhu cầu hiện có.

- [x] BE: nhu cầu lấy thêm `internal_business_scope_name` → ô "Lĩnh vực › Nhóm ngành" (thiếu Lĩnh vực chỉ còn Nhóm ngành:
      34/181); `getDrillPage` trả `base_amount` / `amount`; sắp theo `investment` (+ giữ thứ tự nhu cầu trong cùng meeting);
      bản in: dòng "N nhu cầu · Tổng giá trị dự kiến" + dòng TỔNG; Excel: dòng TỔNG số thật `#,##0`, file `danh-sach-nhu-cau.xlsx`;
      nhãn điều kiện "Nhân viên chủ trì".
- [x] FE: popup Nhu cầu bộ cột STT · Nhu cầu đầu tư ghi nhận · Giá trị dự kiến (sắp được) · Tên meeting · Thời gian · Ngày tạo ·
      KH · Thị trường · Phòng ban · Bộ phận · NV chủ trì; ẩn ô lọc Loại meeting / Trạng thái; tiêu đề + dòng đếm kèm tổng giá
      trị; ô lọc "Nhân viên chủ trì: tất cả" ở MỌI popup (KH mới: "Người tạo KH: tất cả").
- [x] Đo MCP: tiêu đề "181 nhu cầu · Tổng giá trị dự kiến 107,630,675,520 đ", 11 cột đúng thứ tự, 5 ô lọc; 147 dòng 2 cấp;
      sắp giá trị giảm dần đúng. Excel tải thật: 181 dòng + TỔNG = tổng các dòng, cột tiền số thật. Bản in: tiêu đề "DANH SÁCH
      NHU CẦU ĐẦU TƯ THU THẬP", dòng tổng giá trị, 181 dòng + TỔNG.
- [x] PHPUnit DemandCount 5 ca (+ 5 bộ cũ) xanh. E2E UI thêm 1 ca (chưa chạy).
- [ ] User kiểm · commit khi user yêu cầu.

## Đợt 7 — giá trị hiện số tiền đầy đủ, bỏ đơn vị tỷ (user "Làm" 07/10/2026)

Ghi chú: 34 nhu cầu thiếu Lĩnh vực trên local là dữ liệu seed e2e (`e2e_care_report_seed.php` đọc bảng `scopes` ERP sau gộp
DB) — user chốt bỏ qua; dữ liệu thật 153/153 đủ Lĩnh vực.

- [x] FE DevelopmentSummary (dòng mục tiêu, thẻ Nhu cầu, ⓘ khối Kết quả) + DevelopmentTable (cột Giá trị dự kiến: TỔNG + dòng):
      `billion()` → `money()` số đầy đủ en-US (107,630,675,520). Bản in màn chính đã hiện đủ từ trước.
- [x] Excel màn chính: cột giá trị thêm `data-format="#,##0"` (trước là số trơn không phân cách).
- [x] Đo MCP 1280/1366/1920: thẻ 62px (mọi thẻ bằng nhau), nhãn 1 dòng, không tràn; cột tiền 126px, 0 ô cắt chữ / xuống dòng.
- [x] E2E: 2 chỗ bám "x.y tỷ" đổi sang số đầy đủ (chưa chạy).
- [ ] User kiểm · commit khi user yêu cầu.

## Đợt 8 — nhãn "Giá trị dự kiến (VND)" + bỏ ô lọc Trạng thái ở popup 1 trạng thái (user "Làm" 07/10/2026)

- [x] Nhãn cột giá trị → "Giá trị dự kiến (VND)" (user gõ "Giá trị kiến (VND)", xác nhận lại là thiếu chữ "dự"): bảng theo
      dõi, popup, bản in tổng hợp, Excel màn chính, bản in + Excel popup (DETAIL_COLUMNS). Đo 1366: tiêu đề 1 dòng (cột 149px).
- [x] Popup Hoàn thành + 3 popup Huỷ (Huỷ / Quá hạn / Có lý do): bỏ ô lọc Trạng thái (`SINGLE_STATUS_METRICS`), giữ cột
      Trạng thái ở popup Hoàn thành. Đo MCP: 2 popup không còn ô Trạng thái.
- [x] PHPUnit 6 bộ CMD xanh; e2e đổi 4 chỗ nhãn + thêm kiểm ô Trạng thái ở ca popup Huỷ (chưa chạy).
- [ ] User kiểm · commit khi user yêu cầu.

## Đợt 9 — popup "Chọn cột in" cho In báo cáo + In danh sách popup (user "Làm" 07/10/2026)

Chốt: In báo cáo — danh sách cột ĐỔI theo bản in (Bảng theo dõi 7 cột số, STT + Nội dung luôn in / Chi tiết 10 cột); In
danh sách popup — chỉ chọn cột (đúng cột đang hiện); Excel popup giữ đủ cột, không qua bước chọn.

- [x] FE PrintOptionsModal: thêm khối "Chọn cột in" theo khuôn meeting-by-employees (tick sẵn, Chọn tất cả bán chọn, bỏ hết
      báo đỏ không đóng, mở lại chọn hết, đổi bản in chọn lại hết); prop `columns-only` + `columns`; emit `{ mode, columns }`;
      nút In trước Hủy (button-convention). index.vue: 1 popup dùng chung (`drillPrint`), `onPrintChosen` gửi `cols`.
      DevelopmentDrillModal: "In danh sách" gửi kèm danh sách cột đang hiện.
- [x] BE: `SUMMARY_COLUMNS` + `summaryColumns()`; blade bảng theo dõi dựng cột động theo `cols` (không gửi = đủ 7 cột).
      Bản chi tiết vốn đã theo `cols`.
- [x] Đo MCP: In báo cáo 7 cột → bỏ Huỷ + Tỷ lệ HT → request `cols=plan,completed,new,demand,money`, bản in 7 cột; bản chi
      tiết 10 cột → chọn 3 → in đúng 3 + STT; bỏ hết → "Vui lòng chọn ít nhất 1 cột để in", không gọi in; popup Nhu cầu → chọn
      cột liệt kê đủ 10 cột đang hiện, nổi trên popup chi tiết, bỏ 3 → bản in 7 cột, popup chi tiết vẫn mở. Giao diện khớp
      khuôn mẫu (đo font, vị trí "Chọn tất cả").
- [x] PHPUnit `CustomerMarketDevelopmentPrintColumnsTest` 2 ca + 6 bộ cũ xanh. E2E sửa 2 ca in + thêm 1 ca chọn cột (chưa chạy).
- [x] Skill report-styles mục 5 ghi khuôn chọn cột cho In danh sách popup.
- [ ] User kiểm · commit khi user yêu cầu.

## Đợt 10 — cách in thành QUY TẮC + component dùng chung (user "Làm" 07/10/2026)

- [x] Component mới `hrm-client/components/report/V2BaseReportPrintModal.vue` (từ PrintOptionsModal của báo cáo này): props
      `modes` (mỗi mode tự khai `columns` + `fixedNote`) / `columns` (chế độ chỉ chọn cột cho popup drill) / `id` / `title` /
      `note` / `detailMode`; emit `print({ mode, columns })`. Báo cáo này dùng component chung (`printModes` ở index.vue),
      XOÁ `components/PrintOptionsModal.vue` riêng. 5 báo cáo cũ giữ bản riêng, chuyển dần khi sửa tới.
- [x] Đo lại MCP với component chung: 3 luồng (In báo cáo đổi bản in / bỏ hết báo đỏ / In danh sách popup Nhu cầu) cho kết
      quả giống hệt bản riêng. E2E đổi class `cmd-print-*` → `rpm-print-*` (id modal giữ `cmd-print-options-modal`).
- [x] Skill report-styles: mục 4b "In — QUY TẮC CHUNG" (FE + BE: whitelist SUMMARY_COLUMNS / DETAIL_COLUMNS, `cols`, Excel
      không qua chọn cột), bảng bố cục mục 5, biến thể 5b, kiểm mục 6, lỗi thường gặp; template: index.vue dùng
      `V2BaseReportPrintModal` + `printModes` + `drillPrint`, ItemListModal gửi `columns` khi In, xoá template PrintOptionsModal.
- [ ] User kiểm · commit khi user yêu cầu (gồm repo hrm-claude-config cho skill).
