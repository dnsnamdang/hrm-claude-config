# Design (tóm tắt) — Báo cáo kết quả chăm sóc khách hàng tiềm năng

- **Người phụ trách**: @dnsnamdang · **Ngày**: 2026-08-25
- **Nhánh**: `bao_cao_cskh_tiem_nang` (api + client), tách từ `tpe` — **KHÔNG** phải `gop_db` nên tài liệu để ở `.plans/`, dùng `mysql2` bình thường.
- **Mockup đã chốt**: `.plans/gop-db/ke-hoach-phat-trien-thi-truong/bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html` (design v6 → v15 + DATA DEMO v2 trong `design.md` cùng folder)
- **Plan**: `.plans/bao-cao-cskh-tiem-nang/plan.md`

## Mục tiêu

Màn báo cáo theo dõi kết quả chăm sóc KH tiềm năng: tổng hợp **nhu cầu đầu tư** thu thập được qua meeting "Họp tìm hiểu & Giới thiệu sản phẩm", theo dõi tỷ lệ chuyển đổi nhu cầu → **dự án TKT**, bóc tách theo Lĩnh vực/Nhóm ngành · Thị trường · Phòng ban/Nhân viên.

## Hiện trạng đã có (không phải làm lại)

| Thứ | Nguồn |
|---|---|
| Câu 1/4 khảo sát | `meetings.has_investment_demand`, `has_maintenance_demand` |
| Lĩnh vực KH quan tâm | `meeting_investment_scopes` |
| **Nhu cầu (1 dòng = 1 nhóm ngành)** | `meeting_investment_demands` (`internal_business_scope_id/_name`, `scope_id/_name`, `expected_amount`, `expected_start_date`) |
| Loại meeting | `meeting_types` id 7, code `HOP_TIM_HIEU_GIOI_THIEU_SP` |
| Thị trường | ERP `erp2326.customers.province_id/ward_id` (43.050/43.514 KH có ward), `wards.province_id` trực tiếp → cascade 2 cấp chạy được ngay |
| Dự án TKT | `prospective_projects` |
| Danh mục | `internal_business_scopes` (Lĩnh vực) → `scopes` (Nhóm ngành, có `internal_business_scope_id`) |
| Khuôn BE để copy | `Modules/Assign/Services/Report/MeetingByMarketService.php` (phân quyền 3 cấp, resolve tỉnh batch qua `mysql2`, bộ lọc Kỳ) |
| Khuôn FE để copy | `pages/assign/report/prospective-projects/` (index + filter + table + `ProspectiveListModal` + `print.vue`) |

## Quyết định đã chốt

| # | Chốt |
|---|------|
| 1 | Nhu cầu là **thực thể có vòng đời**: thêm 3 cột vào `meeting_investment_demands` — `status`, `prospective_project_id`, `closed_at`. KHÔNG tạo bảng theo dõi riêng, KHÔNG suy hoàn toàn |
| 2 | **3 trạng thái**: `1` Đang theo dõi · `2` Đã lập dự án TKT · `3` Không tiếp tục. Gộp "Hết hạn theo dõi" vào "Không tiếp tục" |
| 3 | **Mốc đóng = đúng `expected_start_date`** (tới ngày dự kiến triển khai mà chưa có dự án → đóng). Bỏ hằng `TRACK_MONTHS = 3` của mockup |
| 4 | Đóng nhu cầu do **cron** `assign:close-expired-customer-demands` (dailyAt 01:20), **`closed_at = expected_start_date`** chứ không phải ngày chạy cron (để cron chạy trễ/chạy bù không làm lệch kỳ). `expected_start_date` rỗng → không bao giờ tự đóng |
| 5 | Gắn nhu cầu ↔ dự án làm ở **form dự án TKT** (Task 2), không phải ở báo cáo. Báo cáo chỉ còn nút "+ Tạo mới" điều hướng sang màn tạo dự án |
| 6 | **1 dự án gắn đúng 1 nhu cầu**; nhu cầu đã gắn dự án khác thì ẩn khỏi select; đổi/bỏ chọn lúc Sửa → nhu cầu cũ trả về `status = 1`, xoá `closed_at` + `prospective_project_id` |
| 7 | Meeting có trường **Người chủ trì** riêng (`meetings.host_employee_id`), thay cho việc suy từ `created_by`; **đổi luôn** chỗ đang hiển thị chủ trì ở báo cáo meeting theo thị trường |
| 8 | Phân quyền 3 cấp copy `MeetingByMarketService::applyPermissionFilter()` (tổng công ty / công ty / phòng ban; không quyền → chỉ meeting của mình) |
| 9 | Engine báo cáo: **1 query lấy tập nhu cầu → resolve tỉnh/phường batch qua `mysql2` → gom nhóm trong PHP**, trả bảng + KPI + 2 khối trong 1 response (không `GROUP BY` xuyên DB, và bảo đảm bảng · KPI · popup luôn khớp) |
| 10 | ~~Phase 1 chưa làm Xuất Excel, bản In, nút phóng to popup~~ → **đã làm hết**: nút phóng to ở Phase 3; Xuất Excel + Bản In ở Phase 4 (2026-08-26) |
| 11 | Liên kết nhu cầu ↔ dự án lưu **một chiều** trên `meeting_investment_demands.prospective_project_id`; `prospective_projects` KHÔNG có cột đối ứng (tránh đồng bộ 2 chiều). Detail dự án truy ngược ra |
| 13 | **Popup lịch sử meeting với KH** (Phase 13, mở từ icon `ri-history-line` ở cột Khách hàng của popup drill-down): lấy **mọi loại meeting** với KH đó nhưng **chỉ trạng thái Hoàn thành**, sắp **cũ → mới**, bấm mở `/assign/meeting/{id}/show` ở **tab mới**. Quyền dùng lại NGUYÊN `applyPermissionFilter()` của báo cáo (4 cấp, fallback chủ trì **hoặc** là thành viên) — user ban đầu ghi "chỉ chủ trì" nhưng đã chốt đồng bộ, vì siết hơn sẽ ẩn mất chính meeting đang hiện ngoài bảng |
| 14 | Cột popup lịch sử: `STT · Tên meeting · Thời gian họp (Từ–Đến) · Người chủ trì · Người liên hệ KH · Nhu cầu (Có/Không)`. Không có cột Trạng thái (đã lọc cứng Hoàn thành) và không có cột Loại meeting |
| 15 | (2026-09-01) Cột 2 **bỏ mã meeting**, chỗ đó đặt **icon Xem biên bản** (`ri-file-list-2-line`, copy khuôn `pages/assign/meeting/index.vue:1171`) mở popup xem trước bản in dùng chung với panel chi tiết meeting. Icon **ẩn hẳn** khi `has_report = false` — `/print` trả 400 nếu meeting chưa lập biên bản |
| 12 | Bỏ nhu cầu **đã gắn dự án** ở màn biên bản bị **chặn** (422) kèm hướng dẫn gỡ ở màn Dự án TKT — xoá im lặng sẽ làm báo cáo mất nhu cầu ở mẫu số nhưng vẫn đếm dự án là "chuyển đổi thành công" |

## Công thức báo cáo (kỳ `[from, to]`, lọc theo `meetings.start_date`)

Nguồn: `meeting_investment_demands` ⋈ `meetings` với `meeting_type_id = 7`, `has_investment_demand = 1`, `meetings.status = 3` (Hoàn thành).

| Chỉ tiêu | Định nghĩa |
|---|---|
| I.1 Còn hiệu lực theo dõi | `start_date < from` và (`closed_at IS NULL` hoặc `closed_at >= from`) |
| I.2 Phát sinh trong kỳ | `start_date ∈ [from, to]` |
| **I** Tổng nhu cầu trong kỳ | I.1 + I.2 |
| II.1 Chuyển đổi thành công | `status = 2` và `closed_at ∈ [from, to]` |
| II.2 Không tiếp tục | `status = 3` và `closed_at ∈ [from, to]` |
| **II** Bị đóng trong kỳ | II.1 + II.2 |
| 3 hộp KPI | `II.1/I` · `II.1/II` · `II.2/II` |

Cột bảng theo dõi: `STT · Nội dung theo dõi · Số nhu cầu · Giá trị dự kiến · Chuyển đổi thành công · Tỷ lệ thành công · Không tiếp tục · Tỷ trọng giá trị`.
*(Mockup đặt tên cột thứ 7 là "Hết hạn theo dõi" — đổi thành "Không tiếp tục" cho khớp bộ 3 trạng thái. Đã confirm với user.)*

## Gotcha bắt buộc xử lý

- ⚠️ `MeetingService::syncInvestmentDemands()` (`MeetingService.php:142`) đang **xoá sạch rồi ghi lại** mỗi lần lưu biên bản → phải đổi sang **upsert theo `(meeting_id, scope_id)`** (đã có unique sẵn), giữ nguyên `status` / `prospective_project_id` / `closed_at`. Không sửa thì sửa biên bản là mất trắng liên kết dự án.
- ⚠️ Cột mới của `meetings` **phải có trong `$request->only([...])`** ở `MeetingController::store()/update()`, nếu không sẽ mất im lặng (đúng cái bẫy đã ghi ở feature khảo sát nhu cầu).
- ⚠️ `components/modal/V2BaseModal.vue` mà CLAUDE.md nhắc tới **KHÔNG tồn tại** trên nhánh này → popup bám khuôn thật đang chạy `ProspectiveListModal.vue`.
- ⚠️ Nguồn nhân viên: `store.currentEmployeeCompany` lọc đúng công ty nhưng `Employee::getAll()` **không lọc trạng thái**; `store.list_employee_infos` lọc `status = 1` nhưng **không select `company_id`** → phải bổ sung `company_id` rồi dựng store key dùng chung.
- ⚠️ Màn **chi tiết/sửa meeting** dùng `MeetingTransformer`, **không** phải `MeetingResource` (`MeetingResource` chỉ phục vụ các endpoint DANH SÁCH). Thêm field cho màn chi tiết mà sửa nhầm `MeetingResource` thì key không xuất hiện trong response, còn thêm vào đó thì sinh N+1 cho màn danh sách vốn không cần.
- ⚠️ Endpoint meeting kế thừa `App\Http\Requests\ApiBaseRequest` → lỗi validate trả **HTTP 400** (errors nằm trong `data`), KHÔNG phải 422 như `assign/scopes`.
- ⚠️ `MeetingService::syncCompanyMembers()` cũng **xoá sạch rồi ghi lại** từ payload: trường nào không gửi lại (điển hình `attendance_status`) bị reset về 0. Mọi script/test gọi API update meeting phải gửi NGUYÊN VẸN từng thành viên — đã dính thật khi viết e2e Task 1, làm hỏng fixture điểm danh của `meeting-investment-survey.spec.ts` (triệu chứng: bấm Hoàn thành bị toast "Vui lòng hoàn thành điểm danh…" chặn trước khi tới validate).
- ⚠️ Guard khi gắn nhu cầu chỉ kiểm **đúng khách hàng** + **chưa bị dự án khác gắn**; KHÔNG kiểm lại "meeting đã Hoàn thành / đúng loại" (điều kiện đó chỉ lọc ở danh sách chọn). Cố tình gọi API với id nhu cầu của meeting chưa hoàn thành vẫn gắn được — chấp nhận, vì nhu cầu đó vẫn đúng khách hàng và không phá số liệu.
- ⚠️ Meeting **đã Hoàn thành thì BE chặn sửa (423)**, và meeting chưa hoàn thành mà quá ngày họp cũng bị chặn ("quá hạn nhập biên bản"). Fixture e2e cần bản "còn sửa được" phải để lịch họp ở **tương lai**.
- ⚠️ `company_members` là rule `required|array` → **mảng rỗng cũng trượt validate**. Seed meeting mà quên thành viên tham dự thì fixture không sửa lại được qua API.
- ⚠️ `responseSuccess($message, $data)` nhận **message ở tham số đầu** — truyền thẳng data vào đó thì mất sạch dữ liệu mà vẫn trả 200. Endpoint trả danh sách dùng `responseJson('success', 200, $data)`.
- ⚠️ `apiGetMethod` (Vuex) trải thẳng key lạ vào axios config → query string phải đặt ở **`params`**, không phải `payload`.
- ⚠️ `database/e2e_meeting_survey_seed.php` **clone nguyên dòng meeting nguồn**, chỉ ghi đè vài cột → cột mới thêm vào bảng `meetings` sẽ kéo theo giá trị của meeting nguồn. Đã ghi đè `host_employee_id = creator` cho fixture xác định; cột mới sau này nhớ làm tương tự.

- ⚠️ `components/V2BaseCompanyDepartmentFilter.vue` **ghi thẳng vào object truyền qua prop `form` và KHÔNG có `$emit`**, đồng thời tự bọc `.d-contents` chứa các `col-md-3`. Bind kiểu `:company-id` + `@update:companyId` chạy im lặng nhưng bộ lọc không có tác dụng; bọc thêm 1 `div.col-*` bên ngoài thì 3 ô thành cột-trong-cột và vỡ lưới. Khuôn đúng: `pages/assign/report/meeting-by-market/index.vue`.
- ⚠️ Khuôn "bản in mở bằng popup" của skill `print-page` mục 8 (`ReportPrintPreviewModal` + `reportPrintStyle` + `reportPrintPreviewMixin` + trait letterhead) **chỉ tồn tại trên `gop_db`** — nhánh tách từ `tpe` phải port nguyên văn. `Modules/Finance` cũng không có nên trait Excel `EmbedsCompanyLetterhead` không dùng được → Excel để không letterhead cho khớp `meeting-by-market`.
- ⚠️ HTML reader của PhpSpreadsheet **cắt sạch khoảng trắng đầu ô** (thụt đầu dòng phải dùng ký tự thật) và **ép "1.10" thành số 1.1** nên STT cấp con bị trùng; `data-format` KHÔNG cứu được vì chỉ set format code, kiểu ô do `DefaultValueBinder` quyết. Cả 2 lỗi chỉ lộ khi đọc lại file bằng PhpSpreadsheet.
- ⚠️ 2 spec e2e dùng chung `e2e_care_report_seed.php` mà playwright chạy 2 worker song song → seed đồng thời đâm unique key. Phải seed qua khoá thư mục `e2e/utils/careFixture.ts`.
- ⚠️ Sinh dữ liệu demo hàng loạt: **lấy mẫu theo nhóm phải truy từng nhóm**, đừng `orderBy(cột nhóm)->limit(N)` rồi mới `groupBy` — ERP có hơn 43.000 khách hàng nên 4.000 dòng đầu nằm trọn trong MỘT tỉnh, kết quả chỉ ra 3 khách của 1 tỉnh. Và **trạng thái với mốc thời gian phải quyết định độc lập nhau**: dùng chung một chỉ số làm toàn bộ nhu cầu "Không tiếp tục" dồn vào tháng hiện tại, KPI thất bại vọt lên 64,9% trông như tính sai.
- ⚠️ **`->select([...])` gọi SAU `->withCount()` xoá luôn subquery đếm** — `select()` THAY THẾ cả select list. Hậu quả im lặng: cột Nhu cầu ra "Không" ở 100% dòng, không exception, không log. Đặt `select()` TRƯỚC `withCount()`.
- ⚠️ **Ca test dựa vào dữ liệu DEMO/THẬT thay vì fixture của chính nó là bom hẹn giờ theo lịch** — ca e2e 15 xanh nhiều tháng rồi đỏ đúng ngày sang kỳ mới (01/09), vì nó đòi "phải có nhu cầu đã gắn dự án" mà fixture lại để `prospective_project_id = null`. Fixture phải tự cung cấp đủ dữ liệu cho điều kiện nó khẳng định.
- ⚠️ **KHÔNG `git stash` ở `hrm-api`/`hrm-client`** — user hay chạy nhiều session song song trên cùng repo; `stash push -u` nuốt luôn việc đang dở của session khác (đã xảy ra 01/09) và các file đó còn bị cuốn vào commit sau đó. Cần so với code sạch thì dùng `git worktree` hoặc `stash push -- <đúng file của mình>`.
- ⚠️ **bootstrap-vue KHÔNG tự nâng z-index cho modal mở sau** — 2 popup chồng nhau đều `1050`, cái sau chỉ nằm trên nhờ thứ tự DOM. Modal mở đè phải tự ghim z-index (popup lịch sử: `1062`, trên `above-modal` 1060 của panel meeting).
- ⚠️ **E2E popup nạp bằng AJAX**: `toBeVisible()` của modal đúng ngay lúc khung vừa mở, `tbody` còn rỗng → đếm dòng ra 0 và mọi khẳng định sau so với 0. Phải chờ nội dung (`toHaveCount(<số đã biết>)` hoặc chờ dòng "Đang tải…" biến mất) rồi mới đếm.
- ⚠️ `srs_uml_render` của skill `srs-documenter` trỏ cứng font Windows — chạy trên macOS phải ghi đè biến font trong generator của feature, KHÔNG sửa file dùng chung trong `.claude/skills/`. Mục lục .docx cũng chỉ tự cập nhật số trang được trên Windows.

## Thứ tự triển khai

1. ~~**Task 1 — Người chủ trì meeting**~~ ✅ (tiền đề: đổi nguồn "Kinh doanh chủ trì" của báo cáo)
2. ~~**Task 2 — Select nhu cầu KH ở dự án TKT**~~ ✅ (tiền đề: đường gắn nhu cầu ↔ dự án; kéo theo migration 3 cột + fix `syncInvestmentDemands`)
3. ~~**Phase 3 — Màn báo cáo**~~ ✅ — cron + 3 quyền + service/controller + màn `/assign/report/potential-customer-care` + popup drill-down
4. ~~**Phase 4 — Xuất Excel + Bản In**~~ ✅ (2026-08-26) — 2 class `FromView` + 2 blade export; bản in dùng khuôn popup xem trước **port từ `gop_db`** (3 file FE + trait letterhead BE), route `print-list-data?mode=summary|detail`
5. ~~**Phase 5 — Tài liệu**~~ ✅ (2026-08-26) — testcase 167 TC (P0 66%) + SRS form mới 4 chương
6. ~~**Phase 6 — Seeder dữ liệu demo**~~ ✅ (2026-08-26) — lệnh `assign:seed-care-demo` chạy được trên VPS: chỉ ĐỌC khách hàng ERP, bản ghi mang tiền tố `DEMO-CSKH-` để `--clean` dọn chính xác, idempotent, có `--dry-run`

7. ~~**Phase 13 — Lịch sử meeting với khách hàng**~~ ✅ (2026-08-31, bổ sung 2026-09-01) — icon ở cột Khách hàng của popup drill-down mở popup liệt kê meeting đã Hoàn thành với KH đó; cột 2 chỉ hiện **tên meeting** kèm icon **Xem biên bản** (chỉ khi đã lập biên bản); endpoint `customer-meetings`; KHÔNG migration / quyền / cron mới

> **Trạng thái cuối: TẤT CẢ đã merge vào `tpe` và push — Phase 1–8 (2026-08-26/28), Phase 13
> (2026-09-02, `hrm-api` `93634433f` · `hrm-client` `2fa39cb29`).**
> **44/44 e2e của màn báo cáo xanh** (23 API + 21 UI), chạy lại trên `tpe` sau merge.

## Ghi chú triển khai Phase 3

- **Popup**: có nút **phóng to toàn màn hình** (`.care-drill-dialog--full`, bám `.minutes-modal--full` của mockup) + nút **thu gọn khối tổng hợp**; modal khoá `max-height: 92vh`, chỉ thân cuộn nên không tràn viewport.
- **Quyền**: id `1179` (tổng công ty) · `1180` (công ty) · `1181` (phòng ban). Seeder truncate cả bảng `permissions` → môi trường đang chạy phải **insert thủ công** rồi gán vào role (`role_has_permissions` cần `company_id`; Super admin ở DB local là role id 18).
- **Cron**: `assign:close-expired-customer-demands`, `dailyAt('01:20')`, có `--dry-run`. Đóng nhu cầu `status = 1` quá `expected_start_date`, ghi `closed_at = expected_start_date`.
- **Route** `assign/report/potential-customer-care*` KHÔNG gắn `checkPermission` — gate theo cấp nằm trong service để giữ fallback "chỉ thấy nhu cầu từ meeting của chính mình". Đã có e2e ca fail-closed (user không quyền → 0 dòng).
- **Tỷ trọng giá trị**: dòng cha so với TỔNG KỲ, dòng con so trong nội bộ cha (tổng con = 100%).
- **Id không resolve được tên** (phòng ban / nhân viên / tỉnh / phường đã xoá) bị **null hoá id** rồi gộp vào nhóm "Chưa xác định" — giữ id mà mất tên sẽ tạo 2 dòng trùng nhãn nằm cạnh nhau.
- **Không so tổng tuyệt đối trong e2e**: DB test có nhiều fixture cùng rơi vào kỳ. Spec kiểm bằng ánh xạ id → nhóm chỉ tiêu + các đẳng thức.
- Ảnh màn hình: `.plans/bao-cao-cskh-tiem-nang/screenshots/` (`bao-cao-cskh-v2.png` màn chính · `popup-v3.png` popup · `mockup-goc.png` + `mockup-popup.png` bản đối chiếu)

### Style — PORT TỪ MOCKUP, KHÔNG TỰ CHẾ (user trả lại 2 lần, 2026-08-25)

Lần đầu tôi tự đặt palette/markup nên lệch hẳn mockup. Cách làm đúng: **trích thẳng CSS trong
`<style>` của file mockup** rồi giữ nguyên tên class + giá trị.

| Thành phần | Class port từ mockup |
|---|---|
| Dải tổng hợp | `.type-summary-bar` · `.rsum-goal` · `.rsum-toggle` · `.rsum-blk*` |
| 3 hộp KPI | `.rsum-kpi*` (+ biến thể `.drill-kpibox` thu nhỏ dùng trong popup) |
| Bảng theo dõi | `.rsum-tb*` · `.rsum-caret` · `.rsum-drill` · `.rsum-sbar` |
| Popup | `.minutes-modal__header` (gradient navy→teal) · `.drill-filters` · `.drill-sum*` · `.drill-table*` |

Quy ước đã chốt khi port:
- **Dòng tiêu đề phần MANG số tổng**, không có dòng TỔNG CỘNG riêng; 3 tông màu field xanh lá ·
  market tím · dept cam.
- Tiền trong bảng theo dõi rút gọn `billion()` → `2065,3 tỷ`; trong popup để **số đầy đủ**;
  cột Thời gian triển khai chỉ `MM/YYYY`. Helper gom ở `pages/.../potential-customer-care/format.js`.
- Popup: **thứ tự cột bám đúng thứ tự hàng trong khối phân bổ**, cột cơ cấu đứng ngay sau STT và
  TRƯỚC cột Khách hàng; ô lọc của cơ cấu đang xem bị ẩn và **không lọc ngầm**; nhóm "không tiếp tục"
  bỏ hẳn khối KPI.
- **Ngoại lệ duy nhất không theo mockup**: icon ⓘ. Mockup tự vẽ `.rsum-info` + tooltip CSS
  `data-tip`; skill `.claude/skills/info-icon-tooltip` cấm đúng kiểu đó → dùng `ri-information-line`
  14px `#94a3b8` + `b-popover custom-class="info-popover"` `placement="bottom"`. **Bắt buộc khai
  `font-weight: normal`** trên span bọc, nếu không icon ăn theo `font-weight: 800` của nhãn xung
  quanh và nét dày hơn hẳn các màn khác.
- **Bộ lọc**: cascade cha ▸ con ở CẢ màn báo cáo lẫn popup, lọc theo `parent_id` mà `filter-options`
  đã trả sẵn — KHÔNG gọi thêm API; đổi ô cha thì xoá giá trị ô con. Bỏ ô **Bộ phận**
  (`disable_part`) vì mockup PIVOT v10 đã bỏ và BE không lọc theo `part_id`.
- **Khối phân bổ trong popup**: **1 container cuộn ngang chung** cho cả 3 cơ cấu (`.drill-sum`
  `flex-direction: column`) — làm mỗi cơ cấu 1 container riêng sẽ ra 3 thanh cuộn và các hàng
  không thẳng cột. Nhãn cơ cấu 96px, `position: sticky; left: 0`.
- **Tiêu đề popup**: câu dẫn để mờ, **tên đối tượng đang xem** trắng đậm cho nổi.
- Bộ lọc màn chính giữ `V2BaseFilterPanel` (user chốt): đồng bộ 10 màn báo cáo khác, không theo
  toolbar 1 hàng của mockup.

⚠️ Bug bắt được khi verify: các `th` sticky cùng `z-index` → ô sau trong DOM vẽ đè ô trước, che mất
nút "Hiện chi tiết" nằm sát mép phải ô tiêu đề (Playwright báo "th intercepts pointer events").
Phải nâng riêng `z-index` cho ô đó.

⚠️ `V2BaseIconButton` nhận icon qua **slot**, không có prop `icon` — truyền `icon="..."` ra nút rỗng.

⚠️ Nội dung `b-popover` được render ra `<body>` nên **scoped style không ăn** — style trong tooltip
phải viết inline.

## Quyết định đã chốt — Phase 7 (nghiệm thu UI, 2026-08-28)

| Điểm | Chốt |
| --- | --- |
| Kiểu tooltip ⓘ | Giữ chuẩn `.claude/skills/info-icon-tooltip` (`ri-information-line` + `b-popover.info-popover`), **không** port vòng tròn chữ `i` + tooltip nền `#0f2537` của mockup. Lấy của mockup phần **nội dung + bố cục bên trong** (tiêu đề IN HOA đậm + gạch đầu dòng). |
| 2 chỗ mockup mô tả SAI luật đã code | Viết theo luật thật: "hết hạn theo dõi" = quá `expected_start_date` (mockup ghi "+ số tháng cấu hình"); bỏ dòng 'gắn nhãn "Kỳ trước"' trong tooltip vì bảng theo dõi không có nhãn đó (nhãn nằm ở popup). |
| Bảng tràn ngang | Không xuống dòng (`nowrap`) toàn bộ ô + tên cột, cho cuộn; thanh cuộn ngang ở **cả trên lẫn dưới**, thanh trên tự ẩn khi bảng vừa khung. |
| Chip "Phân bổ" trong popup | Là **lối tắt của ô lọc**, ghi thẳng vào `filters` — không giữ state riêng. |
| Header popup | `N / M nhu cầu`: M là tổng **trước** bộ lọc riêng của popup; số tiền vẫn của phần đang xem. |
| Lọc sâu bằng hộp KPI | Bỏ hẳn khối KPI (nó nói về tập cha) + hiện dải "← Quay lại". |
| Panel chi tiết meeting | Dùng lại `MeetingDetailDrawer` của màn Lịch (user chốt sửa component dùng chung), thêm 2 prop `extraBlocks`/`extraActions`; footer = mockup **+ giữ nút "Xem biên bản"**. |
| Vào màn tạo dự án từ link | Tự chọn KH + nhu cầu rồi **khoá cả 2 ô** — đổi KH ở đó là nhu cầu đang gắn thành của khách khác. |
| Quyền tạo dự án TKT | Phân hệ **không có** quyền "tạo" riêng; gate bằng OR của 4 quyền `Xem danh sách dự án tiền khả thi theo …` (quyền `Quản lý dự án tiền khả thi` KHÔNG tồn tại). |
| Thứ tự danh sách | Mới nhất lên trước theo **ngày họp**, rồi id nhu cầu. |

## Ngoài scope

Xuất Excel, bản In, SRS/testcase (làm khi được yêu cầu).

*(Nút phóng to popup ban đầu để ngoài scope, user yêu cầu bổ sung 2026-08-25 — đã làm.)*

## Quyết định đã chốt — Phase 14 (tiêu chí "Khách hàng", 2026-09-06)

Spec đầy đủ: `docs/superpowers/specs/2026-09-06-cskh-tieu-chi-khach-hang-design.md`

1. **Phần IV "Theo khách hàng"** hiện ở CẢ `criteria = all` lẫn `criteria = customer` — "Tất cả" nay có 4 phần.
2. **Phòng ban / Bộ phận của phần IV lấy theo hồ sơ NGƯỜI CHỦ TRÌ** (`employee_infos` của `meetings.host_employee_id`).
   Lý do: `meetings.department_id` / `meetings.part_id` được gán lúc tạo meeting = cấp tổ chức của **người TẠO**
   (`MeetingController.php:239-241`), và `meetings.part_id` gần như luôn rỗng (2/44 meeting ở DB local).
   Câu hỏi nghiệp vụ của phần IV là "KH này ai đang chăm" → phải là người chủ trì.
3. **KHÔNG đổi phần III** sang nguồn mới, dù phần III đang trộn nguồn (cha = phòng ban người tạo, con = người chủ trì)
   — đổi là làm lệch số của báo cáo đang chạy thật. Chấp nhận phần III và IV cho ra số phòng ban khác nhau,
   ghi rõ trong tooltip ⓘ của phần IV.
4. **Cấp Bộ phận "nếu có"**: phòng ban mà KHÔNG nhân viên nào có bộ phận → bỏ hẳn cấp đó (nhánh 3 cấp).
   Phòng ban có ít nhất 1 bộ phận → giữ đủ 4 cấp, người không có bộ phận gom vào "Chưa xác định bộ phận".
   (75% nhân viên có `employee_infos.part_id` rỗng — 274/1102.)
5. **Ô lọc Khách hàng chỉ hiện khi `criteria = customer`**, chọn 1 KH bằng `V2BaseSelectRemote`
   (endpoint có sẵn `assign/prospective-projects/search-customers`). Giữ đúng luật "mỗi tiêu chí một khối lọc".
6. **Popup**: thêm cột Bộ phận + bộ ô lọc riêng cho phần IV. Khối "Phân bổ theo cơ cấu" **giữ 3 chiều cũ**
   (thêm chiều Khách hàng sẽ đẻ ra hàng trăm chip); drill theo `hdept`/`hpart` thì ẩn chiều "Phòng ban" vì khác nguồn.
7. **Nới bảng 2 → 4 cấp bằng đệ quy hoá khung dùng chung**, không viết bản riêng cho phần IV.
   Kéo theo: `drill_key` thành **tổ hợp** `customer:12+hdept:5+hpart:9+emp:88` (lọc AND; key 1 phần tử tương thích ngược),
   BE trả thêm `sections[].key`, FE tách `CareTrackingRow.vue` tự gọi chính nó.

⚠️ Rủi ro chính: đệ quy hoá `buildSection()` đụng vào 3 phần đang chạy thật → bắt buộc có ca e2e hồi quy
khẳng định `criteria=all` giữ nguyên số **và `drill_key`** của I/II/III.
⚠️ Fixture `e2e_care_report_seed.php` hiện KHÔNG cover được cây 4 cấp — phải bổ sung trước khi viết test.

## Phase 14 — 4 yêu cầu bổ sung sau nghiệm thu (2026-09-06 → 07)

1. **Sửa 2 ca e2e đỏ có sẵn** (không do Phase 14): `meeting-host.api` đỏ vì meeting fixture
   `customer_id = NULL` mà báo cáo thị trường có `whereNotNull('customer_id')` → ca tự gán KH rồi
   trả lại; `customer-demand-link` ca 1 đỏ vì KH của dự án fixture là **cá nhân** nên khối "Người
   liên hệ" bị ẩn → ca đối chiếu theo đúng loại KH.
2. **Khối tổng hợp mặc định THU GỌN** ở cả màn báo cáo và popup chi tiết.
3. **Cột ngày meeting sắp xếp được ở mọi popup**: popup chi tiết sắp client-side theo `meeting_start_date`
   (helper đổi `dd/MM/yyyy HH:mm` thành mốc số — KHÔNG so chuỗi); popup lịch sử sắp **ở BE** qua
   `sort_dir` vì phân trang server-side.
4. **Nén dải tổng hợp + tiêu đề cột hoa chữ đầu**: 296px (34% màn) → **186px (21%)**, bảng lên
   `top 343px`; bỏ dòng tiêu đề "Kết quả KPI", 2 ô chỉ tiêu con dồn 1 dòng; `th` của cả 2 bảng
   `text-transform: none` + `nowrap`; dòng tiêu đề phần cũng bỏ viết hoa toàn bộ.

Trạng thái cuối: 20/20 task, **84/84 e2e xanh**, **đã commit 2026-09-07** — `hrm-api` `7bddb9fb1`,
`hrm-client` `f29eaaf35` trên nhánh `tpe-cskh-tieu-chi-khach-hang`; chưa push và chưa merge về `tpe`.
