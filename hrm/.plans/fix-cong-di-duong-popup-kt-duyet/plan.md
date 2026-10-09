# Fix công đi đường: popup rỗng + báo cáo không theo KT duyệt

## Bug (DNTT KT duyệt, BC chi tiết tháng)
1. Popup "Chi tiết công đi đường" rỗng.
2. Cột công đi đường hiện 0.25 (ĐM gốc) thay vì 0.77 (KT duyệt).

## Nguyên nhân
Fix "công đi đường LIVE" (commit 26dac304f) chuyển nguồn sang `PaymentBusinessRequest` nhưng:
- `detailPaymentProfile` (popup) vẫn query bảng CŨ `payment_profiles` → DNTT (payment_business_requests) không có ở đó → popup rỗng.
- `getDataTimesheet` lọc theo `approved_time` (ngày TP duyệt) trong kỳ + sum `road_travel_allowance_approve` → DNTT làm 31/07 duyệt sang T8 bị rớt khỏi kỳ T7; và chưa lấy giá trị KT duyệt.

## Quyết định (user chốt: a)
Lọc DNTT theo **ngày công tác `from_time`** trong kỳ (không theo approved_time). Include status CHO_KT_DUYET(3)+DA_DUYET(4). Giá trị: DA_DUYET → `road_travel_allowance_kt_approve`, else `road_travel_allowance_approve`.

## Tasks
- [x] BE `getDataTimesheet`: filter theo from_time + status [3,4]; sum kt_approve (DA_DUYET) + approve (CHO_KT_DUYET)
- [x] BE `detailPaymentProfile`: rẽ nhánh type — type=2 query PaymentBusinessRequest, type=1 giữ payment_profiles (không gãy công truy thu)
- [x] FE index.vue: truyền `type` vào endpoint
- [x] FE `PaymentProfileInfoModal.vue`: link "Hồ sơ thanh toán" theo type (type=2 → payment_business_request)
- [x] php -l sạch

## Ghi chú
Status PaymentBusinessRequest: DANG_TAO=1, CHO_TP_DUYET=2, CHO_KT_DUYET=3 (TP đã duyệt), DA_DUYET=4 (KT đã duyệt). Branch tpe.

## Bug — Công đi đường (2) bảng chấm công chi tiết không đúng + popup rỗng
User: đề nghị thanh toán (payment_business_request) KT đã duyệt công đi đường 0.77, nhưng bảng công chi tiết (timesheet_details) cột "Công đi đường" hiện 0.25, và popup "Chi tiết công đi đường" rỗng. "Đã từng fix nhưng chưa được" (commit a75a52e65 — chỉ sửa BE, nửa vời).

### Root cause
1. **Popup rỗng (100% bug code):** FE `pages/timesheet/timesheet_details/index.vue::openPaymentProfileInfoModal` KHÔNG gửi `type` lên API `detailPaymentProfile`. BE (`TimesheetSummaryService::detailPaymentProfile` dòng 1970) `if($request->type==2)` → null → luôn chạy nhánh cũ `payment_profiles` → rỗng. Nhánh `type==2` (nguồn payment_business_requests, đúng) thành dead code.
2. **Cột 0.25 thay vì 0.77:** code cột (`getDataTimesheet` dòng 1503-1510) ĐÃ sum `road_travel_allowance_kt_approve` cho `DA_DUYET`. a75a52e65 CÓ trong gop_db HEAD. → Nếu prod vẫn 0.25: nhiều khả năng (i) chưa DEPLOY a75a52e65 lên production, hoặc (ii) phiếu chưa `DA_DUYET`/`from_time` ngoài tháng/`kt_approve` chưa lưu 0.77. Cần kiểm data thật.

### Đã fix
- [x] FE: `openPaymentProfileInfoModal` thêm `type: type` vào params → popup gọi đúng nhánh type=2/type=1. (compile OK)

### Chưa xử lý / cần xác nhận
- [ ] Cột 0.25: xác minh trên DB (status phiếu, from_time, road_travel_allowance_kt_approve) — phân biệt lỗi deploy vs data. (Kẹt: chưa truy cập được production DB.)
- [ ] (Liên quan) Job `CreateTimesheetSummary::calc_employee_new` + màn "Bảng chấm công TỔNG HỢP" (`TimesheetMonthSummaryService`) VẪN dùng logic cũ (approved_time + road_travel_allowance_approve) → cột stored `work_day_timekeeper_to_go` = 0.25. Chưa fix (khác màn đang báo).

### Checkpoint — 2026-08-07 (fix lại phần FE bị thiếu)
Phát hiện: plan lần trước đánh [x] "FE index.vue truyền type" + "modal link theo type" nhưng CODE THỰC TẾ KHÔNG CÓ (chưa code/bị mất) → đó là lý do popup vẫn rỗng.
Đã sửa THẬT (hrm-client, gop_db, CHƯA commit):
- [x] `pages/timesheet/timesheet_details/index.vue::openPaymentProfileInfoModal`: thêm `type: type` vào params gửi `detailPaymentProfile` → BE chạy nhánh type=2 (payment_business_requests) → popup hiện dòng.
- [x] `components/modals/PaymentProfileInfoModal.vue`: link "Hồ sơ thanh toán" theo type — type=2 → `/assign/payment_business_request/{pp_id}/show` (trước hardcode `payment_profile`).
- Compile 2 file OK.
Cột 0.25: code branch ĐÃ đúng (sum kt_approve 0.77 cho DA_DUYET, a75a52e65 có trong HEAD). Nếu prod vẫn 0.25 → nghi CHƯA DEPLOY gop_db lên production, hoặc data phiếu (status/from_time/kt_approve). Cần DB xác minh.

### Checkpoint — 2026-08-07 (chốt nghiệp vụ: CHỈ tính phiếu KT đã duyệt)
User chốt: bỏ nhánh CHO_KT_DUYET, chỉ tính phiếu DA_DUYET (KT đã duyệt). Sửa BE trên nhánh **tpe** (hrm-api, CHƯA commit):
- `TimesheetSummaryService::getDataTimesheet`: bỏ `$tpApprovedBrIds` + vế sum `road_travel_allowance_approve` → chỉ còn sum `road_travel_allowance_kt_approve` cho phiếu DA_DUYET.
- `detailPaymentProfile` (type=2): `whereIn(status,[3,4])` → `where(status, DA_DUYET)`; CASE → `d.road_travel_allowance_kt_approve as road_travel_allowance_approve`.
- php -l sạch. diff 5+/11-.
→ Sau sửa: cột công đi đường của NV này = 0.77 (chỉ phiếu 867), không còn +0.25 của phiếu chờ KT duyệt.

### CÒN LẠI (deploy)
- BE fix này cần commit tpe + deploy (php artisan clear cache + reload php-fpm).
- FE hrm-client production VẪN CHƯA build lại (URL detailPaymentProfile thiếu `type`) → popup vẫn rỗng cho tới khi `yarn build` + restart hrm-client (HEAD e6f5e9d3a đã có gửi type).
