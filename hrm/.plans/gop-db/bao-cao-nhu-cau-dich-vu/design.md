# Báo cáo tổng hợp nhu cầu làm dịch vụ

> Trạng thái: **ĐÃ CODE + MERGE gop_db (04/10/2026)** — xem bổ sung mục 3b.
> Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`) → checkout nhánh con khi bắt đầu code.
> Mockup: `mockup.html` (cùng thư mục, mở bằng file://) — 4 màn: Báo cáo · Lập báo giá DV · Cấu hình hạn · Vòng đời.
> Token giao diện + mọi quyết định UI nằm trong comment đầu file mockup.

## 1. Mục tiêu

Theo dõi **trạng thái hiện tại** của nhu cầu sửa chữa – bảo dưỡng mà NVKD thu thập được qua meeting
"Họp tìm hiểu & giới thiệu sản phẩm", và nối nhu cầu đó sang **Báo giá dịch vụ SC-BD** → **Hợp đồng dịch vụ**.

Ba phần việc:
1. Thực thể mới **nhu cầu làm dịch vụ** + vòng đời trạng thái tự động.
2. Màn **Lập báo giá DV**: thêm ô chọn nhu cầu.
3. **Báo cáo** mới ở phân hệ CSKH trước bán + 1 cấu hình hạn + 1 thông báo sắp hết hạn.

## 2. Hiện trạng (khảo sát 03–04/10/2026)

| Chỗ | Thực tế | File |
|---|---|---|
| Câu Q4 biên bản | Chỉ là cờ `meetings.has_maintenance_demand` (0/1), bắt buộc khi Hoàn thành — **không có bảng chi tiết** | `MeetingInvestmentSurvey.vue:207`, `MeetingUpdateApiRequest.php:164-168` |
| Meeting Hoàn thành | Đường duy nhất ghi đồng thời status=3 + Q4 là `MeetingController::update` (L524-761). `completed_at` set 1 lần trong `Meeting::boot()` (L164-173) | |
| Sau Hoàn thành | Meeting **khoá**: update trả 423, không xoá được (chỉ xoá khi Đang tạo) → Q4 không đổi được nữa | `MeetingController.php:560-562, 770` |
| Lỗ hổng `changeStatus` | API cho đổi status tuỳ ý (chỉ chặn 3→4); FE chỉ gửi 4 | `MeetingController.php:344-435` |
| Báo giá DV | `wr_service_quotations` type=1 · trạng thái 1 Đang tạo · 2 Duyệt · 3 Đã tạo HĐ · 4 Hết hiệu lực. "Lưu và duyệt" = lưu thẳng status 2. Sửa/xoá chỉ khi status 1 + người tạo | `WrServiceQuotation.php:82-91, 326-343` |
| Hợp đồng DV | 1 cấp duyệt: Đang tạo → Chờ duyệt → **Duyệt** (Có hiệu lực) · Không duyệt · Huỷ duyệt (3→11) · Đóng (10). Mỗi báo giá chỉ lập được 1 HĐ | `WrServiceContractService.php:1411-1460` |
| Nhu cầu đầu tư (làm mẫu) | `meeting_investment_demands` + cron `assign:close-expired-customer-demands` + cảnh báo `general_regulations.demand_warning_days` | `CloseExpiredCustomerDemandsCommand.php` |

## 3. Quyết định đã chốt

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Một nhu cầu là gì | **1 meeting** "Họp tìm hiểu & giới thiệu SP" **Hoàn thành** có **Q4 = Có** → **1 nhu cầu**. Không thêm câu hỏi chi tiết vào biên bản. Không theo dõi giá trị |
| 2 | Khách có nhiều meeting cùng xác nhận | **Vẫn sinh đủ** — mỗi meeting 1 nhu cầu, báo cáo gộp ô khách hàng |
| 3 | Hạn theo dõi | Cấu hình **"Thời gian theo dõi nhu cầu dịch vụ (ngày)"** ở Cấu hình phân hệ giao việc › Quản lý dự án › Cấu hình hạn, **theo công ty**. Chụp N lúc sinh nhu cầu. N = 0 → không hết hạn |
| 4 | Hết hạn | Cron đóng nhu cầu **Đang theo dõi** quá hạn → **Đóng** (lý do "Hết hạn theo dõi"). Chỉ áp cho Đang theo dõi |
| 5 | Chọn nhu cầu ở báo giá | Ô **"Nhu cầu dịch vụ"** (không bắt buộc). Chỉ nhu cầu **Đang theo dõi** của **khách đang chọn**, chưa gắn báo giá khác. **Ai cũng chọn được**. **1 nhu cầu ↔ 1 báo giá** |
| 6 | Khi nào "Đã lập báo giá" | Chỉ khi báo giá **được Duyệt** (status 2). Lưu nháp: nhu cầu vẫn Đang theo dõi nhưng **đã bị khoá chọn** |
| 7 | Người xử lý | = **người tạo báo giá**, ghi lúc báo giá được duyệt |
| 8 | Xoá báo giá / bỏ chọn nhu cầu | Gỡ liên kết, nhu cầu **giữ nguyên trạng thái hiện có** (thực tế chỉ xảy ra khi báo giá còn nháp → nhu cầu đang là Đang theo dõi hoặc Đóng-do-hết-hạn). Hạn theo dõi không gia hạn |
| 9 | Báo giá nháp được duyệt sau khi nhu cầu đã Đóng do hết hạn | **Vẫn cho duyệt** → nhu cầu chuyển Đã lập báo giá (chứng từ sau được duyệt luôn ghi đè) |
| 10 | Báo giá Hết hiệu lực | **Giữ "Đã lập báo giá"** |
| 11 | HĐ lập từ báo giá được **Duyệt** | → **Đã lập hợp đồng** (kể cả nhu cầu đang Đóng vì HĐ từng Không duyệt rồi trình lại) |
| 12 | HĐ **Không duyệt / Huỷ duyệt / Đóng** | → **Đóng** (lý do tương ứng), **giữ liên kết báo giá + HĐ** |
| 13 | Dữ liệu cũ | **Sinh bù** cho meeting đã Hoàn thành + Q4 = Có; hạn tính từ **ngày deploy + N** (ngày hoàn thành meeting giữ nguyên để báo cáo lọc theo kỳ) |
| 14 | Quyền xem báo cáo | **2 quyền mới**: "Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo tổng công ty" / "… theo công ty". Không có quyền nào → nhu cầu từ meeting mình **chủ trì hoặc tham dự** + nhu cầu mình là **người xử lý** |
| 15 | Cảnh báo sắp hết hạn | **Có gửi thông báo**, 1 lần, trước M ngày (M = "Cảnh báo trước khi đóng nhu cầu" — dùng chung). Người nhận: **người chủ trì + người tạo meeting** |
| 16 | Vị trí báo cáo | Phân hệ **CSKH trước bán** › Báo cáo (nhóm "Báo cáo thị trường", cạnh báo cáo CSKH tiềm năng) |
| 17 | Cấu trúc báo cáo | 2 cấp **Tỉnh/TP ▸ Khách hàng**, mỗi dòng lá = 1 nhu cầu. Cột: STT · Thị trường / Khách hàng · Người liên hệ (họ tên + sđt có icon) · Meeting xác định nhu cầu · Ngày hoàn thành meeting · Người chủ trì meeting · Trạng thái · Báo giá · Hợp đồng |
| 18 | Kỳ | Lọc theo **ngày hoàn thành meeting**. Tuần này / Tháng này / **Năm nay (mặc định)** / Năm trước / Tuỳ chọn |
| 19 | Lọc Công ty / Phòng ban | Theo **người chủ trì meeting** (icon ⓘ giải thích). Thêm lọc **Người xử lý nhu cầu** |
| 20 | Khuôn UI | Bám **`/sale/prepick-tracking`** (SmartFilterPanel · `.rsum` 2 khối · bảng cây `rsum-tb`). Dòng TỔNG có; dòng TỔNG + tỉnh hiện số đếm ở cột Meeting/Báo giá/Hợp đồng; **mọi số bấm được** → `V2BaseReportModal`. Tiêu đề cột cho xuống tối đa 2 dòng |
| 21 | Bấm mã meeting | Mở **`WorkItemDetailDrawer`** (import tên `MeetingDetailDrawer`), header gradient của popup báo cáo `linear-gradient(135deg,#0a1c3d,#06b6d4)`, thêm `extraBlocks` "Nhu cầu làm dịch vụ"; trong popup thì `above-modal` |

## 3b. Quyết định bổ sung sau khi code (04/10/2026)

| # | Vấn đề | Chốt |
|---|---|---|
| 22 | Prefix thông báo | **`NCDV`** — user duyệt |
| 23 | Cột / số "Hợp đồng" | Chỉ đếm nhu cầu **Đã lập hợp đồng** (HĐ đang có hiệu lực). Nhu cầu Đóng vì HĐ không duyệt / huỷ duyệt / đóng vẫn hiện mã HĐ trên dòng nhưng **không** tính vào số và lọc `has_contract` |
| 24 | Xem chi tiết meeting từ báo cáo | Nới `Meeting::canView()`: quyền 1660 → xem mọi meeting **có nhu cầu dịch vụ**; quyền 1661 → khi nhu cầu thuộc công ty đang làm việc. Người xử lý không có quyền báo cáo, meeting không có nhu cầu → giữ luật cũ |
| 25 | Quyền "theo công ty" của báo cáo | = công ty hiện tại ∪ (chủ trì / dự họp / người xử lý) — không bao giờ thấy ít hơn người không có quyền |
| 26 | API bổ sung | `demand-list` nhận `id` (link thông báo, bỏ qua kỳ, vẫn theo quyền), `pv=0` (Chưa xác định thị trường), `q` (tìm trong popup, áp cả in/Excel) |
| 27 | Tiêu đề bảng | Dính trong vùng cuộn riêng của bảng (layout dùng chung có `overflow:hidden`) |

## 4. Vòng đời trạng thái

| Mã | Trạng thái | Màu (bảng 9 màu chuẩn) |
|---|---|---|
| 1 | Đang theo dõi | `#0EA5E9` |
| 2 | Đã lập báo giá | `#2563EB` |
| 3 | Đã lập hợp đồng | `#16A34A` |
| 4 | Đóng | `#6B7280` |

Lý do đóng (`close_reason`): 1 Hết hạn theo dõi · 2 HĐ không duyệt · 3 Huỷ duyệt HĐ · 4 Đóng HĐ.

| Sự kiện | Điều kiện | Kết quả |
|---|---|---|
| Meeting chuyển Hoàn thành | loại PRODUCT_INTRO, Q4 = 1, chưa có nhu cầu của meeting này | Tạo nhu cầu, status 1, `tracking_start_date = completed_at`, `due_days_snapshot = N`, `due_date = start + N` (N=0 → null) |
| Lưu báo giá (nháp) có chọn nhu cầu | nhu cầu status 1, đúng khách, chưa gắn báo giá khác | `wr_service_quotation_id = báo giá` — status giữ 1 |
| Báo giá được Duyệt (lưu status 2) | báo giá đang gắn nhu cầu | status 2, `handler_employee_id = báo giá.created_by`, `quoted_at = now`, xoá `close_reason/closed_at` |
| Sửa báo giá nháp đổi/bỏ nhu cầu · xoá báo giá nháp | | Nhu cầu cũ: `wr_service_quotation_id = null`, status giữ nguyên |
| Báo giá Hết hiệu lực (2→4) | | Không đổi |
| HĐ lập từ báo giá được Duyệt (→ 3) | | status 3, `wr_service_contract_id`, `contracted_at = now`, xoá `close_reason/closed_at` |
| HĐ Không duyệt (→11) / Huỷ duyệt (3→11) / Đóng (→10) | | status 4, `close_reason` 2/3/4, `closed_at = now`, giữ liên kết |
| Cron hằng ngày | status 1, `due_date <= hôm nay` | status 4, `close_reason = 1`, `closed_at = due_date` |
| Cron cảnh báo | status 1, N > M > 0, hôm nay ≥ due − M, chưa cảnh báo | Gửi thông báo, set `expiry_warned_at` |

Bất biến: "chứng từ phía sau được duyệt luôn ghi đè trạng thái" (#9, #11). Mọi chuyển trạng thái gọi
qua **1 service duy nhất** (`ServiceDemandStatusService`), không rải `forceFill` ở các service báo giá/HĐ.

## 5. Dữ liệu

### 5.1 Bảng mới `meeting_service_demands`

| Cột | Kiểu | Ghi chú |
|---|---|---|
| id | bigint | |
| meeting_id | bigint, **unique** | 1 meeting ↔ 1 nhu cầu |
| company_id | int | công ty của NGƯỜI CHỦ TRÌ lúc tạo (employee_infos), fallback `meetings.company_id` — design #19 |
| customer_id | int | chụp từ meeting |
| status | tinyint | 1–4 |
| close_reason | tinyint null | 1–4 |
| tracking_start_date | date | = ngày hoàn thành meeting; dữ liệu sinh bù = ngày deploy |
| due_days_snapshot | smallint | N lúc tạo |
| due_date | date null | null khi N = 0 |
| wr_service_quotation_id | bigint null, **unique** | báo giá đang gắn (kể cả nháp) |
| handler_employee_id | int null | người xử lý = người tạo báo giá, ghi lúc duyệt |
| quoted_at | datetime null | |
| wr_service_contract_id | bigint null | |
| contracted_at | datetime null | |
| closed_at | datetime null | |
| expiry_warned_at | datetime null | |
| created_at / updated_at | | |

Index: `(status, due_date)` cho cron · `(company_id)` · `(customer_id, status)` cho ô chọn ở báo giá.
Dùng kết nối mặc định (DB gộp) — **không dùng `mysql2`**.

Không thêm cột vào `wr_service_quotations`: liên kết nằm trên nhu cầu (giống `prospective_project_id`
của nhu cầu đầu tư). Request báo giá nhận thêm `service_demand_id`.

### 5.2 Cấu hình

`general_regulations.service_demand_due_days` — `unsignedSmallInteger`, default **30**, theo công ty.
Copy khuôn migration `2026_09_14_000002_add_demand_expiry_columns.php` (guard `hasColumn`), thêm vào
`$fillable` của `GeneralRegulation`, `MyJobService::getDeadlineConfig/saveDeadlineConfig` (trả field mới),
`DEADLINE_TRACKED_FIELDS` + nhãn trong `DeadlineConfigAdapter` (lịch sử thay đổi).

## 6. Backend (`hrm-api`)

### 6.1 Sinh nhu cầu
- `ServiceDemandSyncService::syncFromMeeting(Meeting $m)`: idempotent (`firstOrCreate` theo `meeting_id`),
  chỉ khi PRODUCT_INTRO + status 3 + `has_maintenance_demand = 1`.
- Gọi trong transaction của `MeetingController::update` (cạnh `syncInvestmentDemands`, L700) **và**
  `changeStatus` khi status mới = 3 (vá lỗ hổng mục 2).
- Lệnh `assign:backfill-service-demands {--dry-run}`: sinh bù theo #13, in số lượng; chạy tay 1 lần sau deploy.

### 6.2 Báo giá (`Modules/CustomerCare`)
- `GET wr-quotations/service-demands?customer_id=&include_id=` → danh sách chọn (status 1, chưa gắn,
  hoặc đúng `include_id` khi sửa). Trả: mã meeting, ngày họp, người chủ trì + phòng, hạn, số ngày còn lại.
- `WrQuotationRequest`: `service_demand_id` nullable|exists; validate cùng khách + được phép gắn
  (status 1 & chưa gắn báo giá khác, hoặc là nhu cầu báo giá này đang gắn).
- `WrQuotationService::store/update` (sau `syncChildren`, trong transaction): gắn/gỡ liên kết; nếu status
  cuối = 2 → `ServiceDemandStatusService::onQuotationApproved`.
- `delete`: gỡ liên kết.
- `prefillFromQuotation` (copy báo giá): **không** mang `service_demand_id` sang.
- `WrQuotationResource` (chi tiết): trả khối `service_demand` (mã meeting, trạng thái, hạn) để form/màn
  xem hiển thị.

### 6.3 Hợp đồng
- `WrServiceContractService::approve` → callback sau lưu gọi `onContractApproved`.
- `reject` / `unApprove` / `close` → `onContractClosed(reason)`.
- Tìm nhu cầu qua `wr_service_quotation_id = contract.wr_service_quotation_id`.

### 6.4 Cron
- Command **riêng** `assign:close-expired-service-demands {--dry-run}`, lịch hằng ngày 01:25 Asia/Ho_Chi_Minh,
  `withoutOverlapping` — không đụng `CloseExpiredCustomerDemandsCommand` của nhu cầu đầu tư đang chạy.
- Cảnh báo: dùng chung `demand_warning_days`, quy tắc N > M > 0 như nhu cầu đầu tư. Thông báo theo skill
  `notification-convention` (prefix mới cho nhu cầu dịch vụ), deep-link
  `/assign/report/service-demand?demand_id=`.

### 6.5 API báo cáo (`Modules/Assign`, prefix `report/service-demand`)
| Route | Việc |
|---|---|
| `GET /` | cây Tỉnh ▸ Khách hàng ▸ nhu cầu + khối tổng hợp, phân trang theo nhóm tỉnh |
| `GET /filter-options` | công ty (theo quyền), phòng ban, người chủ trì, tỉnh, người xử lý |
| `GET /demand-list` | danh sách phẳng cho popup drill (lọc thêm `pv`, `status`, `has_quotation`, `has_contract`) |
| `GET /export`, `/demand-list/export`, `/print-list-data` | Excel / in theo skill `export-excel`, `print-page` |

- Kỳ: `meetings.completed_at` trong khoảng. Tỉnh/khách hàng lấy như báo cáo CSKH tiềm năng
  (`attachCustomerMarket`) nhưng **không qua `mysql2`** — join thẳng bảng khách hàng của DB gộp.
- Người liên hệ: liên hệ khách hàng ghi trên meeting (họ tên + sđt).
- Báo giá nháp đang gắn: trả kèm cờ `is_draft` → FE hiện "(nháp)" dưới mã báo giá.
- Quyền (`applyPermissionFilter`): tổng công ty → không giới hạn · theo công ty → `company_id` = công ty
  đang làm việc OR chủ trì là mình · không quyền → chủ trì / tham dự (`meeting_employees`) / người xử lý là mình.
  **Không bypass super admin**. Ô Công ty: chỉ quyền tổng công ty mới đổi được, còn lại khoá.
- 2 quyền seed mới, nhóm "Báo cáo tổng hợp nhu cầu làm dịch vụ", type 4, guard `api`. **Kiểm id thật
  trong DB + `uniq -d` seeder trước khi chọn id** (dải 1177-1180 đang bị trùng giữa 2 seeder). Không gán sẵn role.

## 7. Frontend (`hrm-client`)

| Màn | Việc | Khuôn |
|---|---|---|
| `pages/assign/report/service-demand/index.vue` + `components/` | Báo cáo đúng mockup | copy `pages/sale/prepick-tracking/` |
| Popup drill | `V2BaseReportModal` + `reportDrillListMixin` | `.plans/gop-db/base-popup-bao-cao/design.md` |
| Panel meeting | `WorkItemDetailDrawer` + `extraBlocks` + `above-modal` | `pages/assign/report/potential-customer-care/index.vue:153-163, 607-633` |
| Người liên hệ | tên + `ri-phone-line` + sđt chữ nhỏ | `pages/assign/request-solution/index.vue:191-196` |
| Menu | `components/subsystem-menu/presale.js` nhóm "Báo cáo thị trường" — không `isShow` (BE lọc theo quyền), giống mục CSKH tiềm năng | |
| `WrQuotationForm.vue` | Ô "Nhu cầu dịch vụ" hàng 2 (Địa chỉ sửa chữa thu về col-3 → hàng đủ 4 ô); khoá khi chưa chọn khách; đổi khách thì xoá lựa chọn; dưới ô hiện badge + chủ trì + hạn | mockup màn 2 |
| Màn xem báo giá | Hiện nhu cầu đang gắn (link mở panel meeting) | |
| `pages/assign/settings/index.vue` | Dòng "Thời gian theo dõi nhu cầu dịch vụ" sau "Cảnh báo trước khi đóng nhu cầu", `required|non_negative_integer|max_value:3650` | |

Badge trạng thái: `V2BaseBadge :color="status_color"` — chữ + màu do BE trả.

## 8. Kiểm thử

- **BE feature test** cho từng dòng bảng mục 4 (tạo, gắn nháp, duyệt, gỡ, xoá, HĐ duyệt/không duyệt/
  huỷ duyệt/đóng, cron hết hạn + cảnh báo, backfill idempotent, ghi đè sau khi Đóng). Test riêng đường
  **tạo mới** và **sửa** báo giá.
- **Phân quyền**: tổng công ty · theo công ty · không quyền (chỉ thấy của mình + người xử lý) — cả có
  quyền lẫn không quyền.
- **E2E (Playwright)**: báo cáo (lọc kỳ, cây, drill, panel meeting, in/excel), ô chọn nhu cầu ở báo giá,
  cấu hình hạn. Đo DOM theo khuôn (footer, sticky header, số khối cuộn, định dạng) và so với mockup.
  Chỉ chạy bộ e2e khi user yêu cầu; vẫn kiểm bằng Playwright MCP trước khi báo xong.

## 9. Ngoài phạm vi

- Màn quản lý / bàn giao / đóng tay nhu cầu dịch vụ (chỉ có báo cáo).
- Lịch sử thay đổi nhu cầu (trạng thái có mốc thời gian + lý do đóng là đủ).
- Theo dõi giá trị báo giá/HĐ trên báo cáo.
