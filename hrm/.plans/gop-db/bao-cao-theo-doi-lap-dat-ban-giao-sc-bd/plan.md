# Plan — Báo cáo theo dõi lắp đặt - bàn giao - SC - BD (@khoipv)

## Phase 1 — Port màn

### Khảo sát
- [x] T1. Đọc ERP controller / service / blade / class JS; ghi bảng nghiệp vụ vào spec
- [x] T2. Đo dữ liệu thật (3 nhánh, 1 GV ↔ 1 PCT/NKQ/DKQ, người tạo PCT + nhân sự lưu `employee_infos.id`)
- [x] T3. Hỏi user: quyền / ô lọc chết / In-Excel / giao diện → chốt (spec mục 1)

### BE (hrm-api `Modules/CustomerCare`)
- [x] T4. `InstallDeliveryRepairReportService`: query dòng (3 nhánh), lọc nhóm + dòng, gom nhóm, summary, phân trang, item-list, filter-options
- [x] T5. Controller + route `/v1/customer-care/report/install-delivery-repair*`
- [x] T6. PrintService + blade in (summary / detail, chọn cột)
- [x] T7. Export Excel báo cáo + danh sách popup (letterhead, khuôn export-excel)
- [x] T8. Smoke test HTTP kernel: index / filter-options / item-list / print / export

### FE (hrm-client)
- [x] T9. `pages/customer-care/report/install-delivery-repair/index.vue` + api/format + DrillNum/InfoTip (copy template)
- [x] T10. `ReportSummary.vue` (2 khối) + `ReportTable.vue` (cây 2 cấp) + `ItemListModal.vue`
- [x] T11. Link menu CSKH › Báo cáo
- [x] T12. Verify compile (vue-template-compiler + babel parse) 8/8 file sạch; HTTP thật 401/200; trang Nuxt 200
- [x] T12b. Viết e2e `e2e/tests/customer-care/install-delivery-repair-report.spec.ts` (16 test, chỉ đọc). Lượt 1: test 01 fail do kỳ vọng sai (dòng TỔNG viết HOA bằng CSS) -> đã sửa test; lượt 2: test 06 bắt nhầm response trễ của ô "Từ" -> sửa chờ đúng response có to_date. Lượt 3 (14/11): 15/16 ĐẠT; test 16 phần Xóa lọc đạt, chỉ vướng lỗi console HMR Nuxt dev (`hot-update.json timed out`, không phải lỗi màn) -> đã lọc trong test, CHƯA chạy lại sau khi lọc. Không phát hiện lỗi code màn.
- [x] T12c. (16/11) User yêu cầu BỎ cột "Phiếu duyệt KQ" (HRM đã gộp duyệt KQ vào phiếu nhập kết quả, không còn màn PDKQ riêng) — chỉ giữ cột Phiếu NKQ: bảng cây, popup, chọn cột In, bản in, Excel. Khối tổng hợp "Đã / Chưa duyệt kết quả" giữ nguyên. Đã sửa ReportTable/ItemListModal/index.vue/format.js + PrintService + Export (11 cột, LAST_COL K) + blade summary + e2e spec; kiểm: compile 4 file sạch, php -l, Excel tháng 7 ra 11 cột, bản in tổng hợp + danh sách kết thúc ở Phiếu NKQ. E2E CHƯA chạy lại. CHƯA commit.
- [x] T12d. (16/11) Phân trang theo màn `sale/sale-by-product-report`: chép `SaleByProductPagination.vue` -> `components/ReportPagination.vue` (không sửa file màn Bán hàng). Bảng chính + popup: "Hiển thị a–b / tổng", select Số dòng/trang + b-pagination; mặc định 10, chọn 5/10/20/50/100 (FE perPage 10, BE PER_PAGE 10, popup đè pageSize 10 của mixin qua slot `#pagination`). E2E test 04 sửa XXI -> XI + selector select. Kiểm: compile 4 file, API mặc định per_page=10, Nuxt 200. CHƯA mở trình duyệt, E2E chưa chạy lại. CHƯA commit.
- [x] T12e. Push develop 16/11 (user yêu cầu) T12c + T12d: hrm-api `912a60356`, hrm-client `13ef5636a`. Không kèm `install-delivery-repair-detail/index.vue` (thay đổi của phiên khác, để nguyên). Sau đó user yêu cầu đẩy nốt: hrm-client `ea5ad5b50` (màn chi tiết gom thay đổi lọc thành 1 lần tải, cờ reloadQueued).
- [ ] T13. User tự bấm trình duyệt (chưa kiểm chứng bằng mắt: bố cục bảng cây, popup drill, in, Excel tải về)

### Checkpoint — 2026-11-14
Vừa hoàn thành: BE (service + print + export + route) + FE (index, ReportSummary, ReportTable, ItemListModal, DocCell, format/api) + menu.
Đo: index ~2s (6.432 chứng từ / 6.942 phiếu), filter-options ~1,4s, item-list ~1,7s; Excel 1 tháng 4s, toàn bộ 14s; in vượt trần 2.000 dòng -> chặn.
Gotcha đã gặp: `employee_assign_task_progress` không có index (whereExists 16s -> whereIn subquery); Excel blade FromView 235s -> PhpSpreadsheet trực tiếp 14s;
Carbon::parse 28k lần 3,7s -> tách chuỗi.
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt `/customer-care/report/install-delivery-repair` kiểm bố cục / popup / in / Excel. Code CHƯA commit.
Blocked:

## Phase 2 — Màn CHI TIẾT (port ERP `customerCareReport.reportInstallDeliveryRepairDetail`) — 2026-11-14

User chốt 14/11: không phân quyền · tab SC-BD / Bảo hành vẫn bắt buộc 1 HĐ nhưng CHỌN từ ô tìm HĐ DV · có In + Xuất Excel ·
lỗi số liệu ERP GIỮ Y ERP (ô "SL đã duyệt KQ" tab Lắp đặt + SC không bấm được; popup duyệt KQ tab Bảo hành liệt kê phiếu NKQ;
vật tư bảo dưỡng = 0, SL PCT bảo dưỡng cộng đôi).
Route FE `/customer-care/report/install-delivery-repair-detail` · BE `/v1/customer-care/report/install-delivery-repair-detail*`.

### BE (hrm-api `Modules/CustomerCare`)
- [x] P2-T1. `InstallDeliveryRepairDetailReportService`: tab install (HĐ bán, phân trang 20 HĐ) · tab repair / warranty (1 HĐ DV,
      cây Sửa chữa / Bảo dưỡng / Bảo hành) · drill 8 loại popup · tìm HĐ DV · filter-options
- [x] P2-T2. Controller + route
- [x] P2-T3. In (print-list-data: bảng tab đang xem chọn cột / danh sách popup) + Excel (bảng tab / danh sách popup)
- [x] P2-T4. Smoke test HTTP kernel + đối chiếu số với hàm ERP trên vài HĐ

### FE (hrm-client)
- [x] P2-T5. `pages/customer-care/report/install-delivery-repair-detail/index.vue` (3 tab, SmartFilterPanel / tab, chọn HĐ, chọn hàng)
- [x] P2-T6. `DetailTreeTable.vue` (cây rsum-tb chung 3 tab) + `DetailDrillModal.vue` (popup theo loại)
- [x] P2-T7. Link menu CSKH › Báo cáo
- [x] P2-T8. Verify compile + HTTP thật
- [ ] P2-T9. User tự bấm trình duyệt 3 tab (chưa kiểm chứng bằng mắt: bố cục cây 5 cấp, ô chọn HĐ, popup, In, Excel)

### Checkpoint — 2026-11-14 (Phase 2)
Vừa hoàn thành: BE service/print/export/controller/route + FE index/DetailTreeTable/DetailDrillModal + menu.
Kiểm: số liệu khớp ERP 100% (851 dòng lắp đặt, 54 HĐ SC-BD/BH — gọi thẳng controller ERP cùng DB); smoke HTTP mọi endpoint 200,
Excel toàn bộ 14s; compile vue-template-compiler + babel 6/6 file sạch; Nuxt trả 200.
Đang làm dở: không.
Bước tiếp theo: user mở `/customer-care/report/install-delivery-repair-detail` bấm thử. Code CHƯA commit.
Blocked:
- [x] P2-T10. E2E Playwright `e2e/tests/customer-care/install-delivery-repair-detail-report.spec.ts` (17 test, chỉ đọc): 17/17 qua (6 phút). 2 lần đỏ đầu do test (đo tiêu đề tính cả chữ ô chọn cấp; đọc ô HĐ lúc "Đang tìm..."), không sửa code màn. Test 15 lấy HĐ bảo hành có SL duyệt KQ từ DB để bắt buộc bấm popup duyệt KQ.
- [x] P2-T11. Push develop 14/11 (user yêu cầu): hrm-api `6fa8d92b9` + hrm-client `44518bef6` (Phase 1 + 2). Kèm commit riêng của màn Bán hàng theo mặt hàng (api `68ff7041e`, client `ccf56257e`, gồm slot `pagination` của V2BaseReportModal).

### 2026-11-16 — Test kỹ (user yêu cầu "test playwright thật kỹ")
- [x] P2-T12. E2E chuyên sâu `e2e/tests/customer-care/install-delivery-repair-detail-deep.spec.ts` (20 test): phân trang + đếm request, race, rỗng, ô Hàng hóa (popup chọn hàng), Công ty → Phòng ban, tiêu đề dính, 1366px, popup > 20 dòng (phân trang / sắp / tìm), link tab mới không 404, In vượt trần, Excel toàn bộ, SC-BD 5 cấp + mũi tên + ô HĐ theo Công ty / Hàng hóa + bỏ HĐ, Bảo hành đủ 4 popup + In/Excel, user 0 quyền / không token. 20/20 qua.
- [x] P2-T13. FIX (bắt từ e2e D05): đổi Công ty khi đang lọc Phòng ban gửi 2 request, request đầu mang department_id cũ -> `index.vue` gom thay đổi cùng nhịp bằng `$nextTick` (`reloadQueued`). Bộ chính 17/17 chạy lại vẫn qua. CHƯA commit.
- [ ] P2-T14. Đối chiếu TOÀN BỘ số liệu HRM ↔ ERP: phía HRM dump xong (8.451 dòng hàng, 1.643 HĐ SC-BD, 3.018 HĐ BH, 3.479 popup); phía ERP bị hệ thống dừng vì máy thiếu RAM (16/11) — chưa so. Script: scratchpad `full_hrm.php` / `full_erp.php`. Đã so ở 14/11: 851 dòng + 54 HĐ khớp 100%.
- [x] P2-T15. Phân trang kiểu màn danh sách (user yêu cầu 16/11): component chung MỚI `components/report/ReportListPagination.vue` (khuôn SaleByProductPagination — "Hiển thị a–b / tổng", 10 dòng, chọn 5/10/20/50/100) cho bảng tab Lắp đặt (`DetailTreeTable`) + popup (`DetailDrillModal` qua slot `#pagination`, pageSize 10); `index.vue` perPage 10; BE PER_PAGE mặc định 10. Màn Bán hàng theo mặt hàng KHÔNG đổi (vẫn dùng bản riêng). E2E: bộ chính 17/17 + bộ chuyên sâu 20/20 qua. CHƯA commit (gồm cả fix P2-T13).

### Checkpoint — 2026-11-16
Vừa hoàn thành: phân trang kiểu màn danh sách + fix 2 request khi đổi Công ty; 37/37 e2e qua.
Đang làm dở: không.
Bước tiếp theo: chờ user bảo commit + push (hrm-client index.vue, DetailTreeTable, DetailDrillModal, ReportListPagination mới; hrm-api PER_PAGE). Đối chiếu toàn bộ ERP (P2-T14) chờ máy đủ RAM.
Blocked: API local chậm ~3s/request (máy thiếu RAM) — test chạy lâu, không ảnh hưởng kết quả.
- [x] P2-T16. Check (16/11, user hỏi "2 tab SC-BD / Bảo hành không có phân trang à?"): ĐÚNG là không có — y ERP (blade chỉ có `uib-pagination` ở tab Lắp đặt; 2 tab kia mỗi lần xem 1 HĐ bắt buộc). Dữ liệu local: 1 HĐ tối đa 27 thiết bị sửa chữa / 12 bảo hành / 20 thiết bị bảo dưỡng (TB 1–2). Chưa sửa gì — chờ user chọn có thêm phân trang theo thiết bị không.
- [x] P2-T17. Phân trang THEO THIẾT BỊ tab SC-BD / Bảo hành (user chọn 16/11): BE `service()` cắt trang thiết bị (STT gốc, 1 thiết bị đi trọn), In/Excel `$all`; FE gửi page/per_page cả 3 tab. FIX bắt từ e2e D16: HĐ không khớp lọc -> BE trả per_page = 1 -> FE kẹt 1 dòng/trang; sửa BE giữ per_page + FE chỉ nhận cỡ trang 5/10/20/50/100. Test mới D18b.
- [x] P2-T18. Push develop 16/11 (user yêu cầu): hrm-api `ce7fb5ce1`, hrm-client `9ef6d6e3f` (gồm P2-T13/T15/T17). Rebase qua 35 / 24 commit mới của remote, không đụng file.
- [ ] P2-T19. Chạy lại bộ e2e chuyên sâu sau fix per_page: chưa được — Nuxt dev (:3000) không trả lời từ sau khi pull 24 commit mới về hrm-client (16/11), API vẫn sống. Chờ user khởi động lại Nuxt rồi chạy `npx playwright test tests/customer-care/install-delivery-repair-detail-deep.spec.ts`.

### 2026-11-17 — #12186 QA (Huyền Trang) màn `/customer-care/report/install-delivery-repair`
- [x] P3-T1. Khối tổng hợp: 2 khối Chứng từ nguồn / Tiến độ xử lý chia đều 50/50 (bỏ khối nguồn rộng theo nội dung)
- [x] P3-T2. Ô chọn cấp ở tiêu đề cột "Chứng từ nguồn / Phiếu yêu cầu": chữ 12px (khuôn #11929 transport), đủ rộng đọc hết "Đến phiếu giao việc" — nới cột 320 → 370px
- [x] P3-T3. Ô "Số dòng/trang" (bảng chính + popup): chữ 12px khớp nhãn (đang 10.24px của form-control-sm), mặc định vẫn 10. Áp cả `components/report/ReportListPagination.vue` (chỉ màn chi tiết cùng báo cáo dùng)
- Kiểm: compile template + babel 4 file OK; chưa mở trình duyệt. CHƯA commit.

### 2026-11-17 — #12187 QA (Huyền Trang) popup bấm số
- [x] P3-T4. Bỏ chữ "Bạn đang xem:" ở tiêu đề popup (bỏ prop `lead`) — `ItemListModal.vue` + áp luôn `install-delivery-repair-detail/components/DetailDrillModal.vue`
- [x] P3-T5. Ô tìm của popup thêm nút × xoá nhanh (khuôn PlanPickerModal: button tuyệt đối + `ri-close-line`, xoá xong về trang 1) — 2 popup trên
- Kiểm: compile template + babel 2 file OK; chưa mở trình duyệt. CHƯA commit.

### 2026-11-17 — #12190 QA (Huyền Trang) đối chiếu ERP
- [x] Ý 2 (lọc Thời gian công tác — QA kết luận ERP sai): ĐÚNG. ERP gửi `to_date=YYYY-MM-DD`, `ReportInstallDeliveryRepairService::filter()` so `assign_business_work_end_time <= '2026-11-07'` = 07/11 00:00 → loại mọi CT kết thúc trong ngày cuối. Sửa ERP (repo `D:\laragon\www\erp`, nhánh gop_db): ghép ` 23:59:59`. HRM đã đúng (`<= $to 23:59:59`), không sửa
- [x] Ý 1 (thiếu ô Hợp đồng + Trạng thái), ý 3 (thiếu cột Số phiếu yêu cầu), ý 4 (thiếu cột Phiếu duyệt KQ): NGƯỢC quyết định đã chốt → user chốt 17/11 GIỮ NGUYÊN cả 4, không sửa code, trả lời QA (ô tìm nhanh = ô Hợp đồng; phiếu YC ở dòng con cột cây; bỏ Trạng thái 14/11; bỏ Phiếu duyệt KQ 16/11)
- Kiểm: `php -l` file ERP OK; chưa chạy thử màn ERP. CHƯA commit (cả repo erp).
- [x] Đã đăng ghi chú trả lời QA lên Redmine #12190 (journal change-44022, 17/11); không đổi trạng thái (đang "Đang tiến hành")

### 2026-11-17 — #12194 QA (Huyền Trang) màn CHI TIẾT `/customer-care/report/install-delivery-repair-detail`
- [x] P3-T6. Ô chọn cấp ở tiêu đề cột: thêm × xoá nhanh (bấm × = về "Chỉ hợp đồng"/"Chỉ chứng từ nguồn", cấp 1) + chữ 12px — `DetailTreeTable.vue`; áp luôn `install-delivery-repair/components/ReportTable.vue` cho đồng bộ
- [x] P3-T7. Ô "Số dòng/trang" to lên — đã xong ở #12186 (`components/report/ReportListPagination.vue` 12px / cao 30px)
- [x] P3-T8. ⓘ tooltip cạnh tiêu đề trang trên topbar (`pageTitleInfo`, khuôn transport #11877) — 2 màn index
- Kiểm: compile template + babel 4 file OK; chưa mở trình duyệt. CHƯA commit.

### 2026-11-17 — #12196 QA (Huyền Trang) màn CHI TIẾT
- [x] Ý 1: ô Hàng hóa đổi chip `V2BasePickerField` → `V2BasePickerInput` (kính lúp + × cuối ô, skill select-and-input-state 2d) — `install-delivery-repair-detail/index.vue`. Ô tìm popup đã có × từ #12187
- [x] Ý 2 (ô Số dòng/trang) + ý 3 (bỏ "Bạn đang xem") — đã xong ở #12186 / #12187 (dùng chung ReportListPagination / DetailDrillModal)
- [x] Ý 4: Chi tiết đề nghị xuất kho (`finance/warehouse-export-requests/_id/index.vue`) — khoảng trắng dưới "Tổng thành tiền" do `.table-responsive { min-height: 50vh }` global → huỷ trong `.wer-tabs` (khuôn borrow-export-requests)
- [x] Ý 5: thu cột `DetailTreeTable` 1.784 → 1.484px (cột cây 380, SL theo HĐ 135, 6 cột SL 95, hoàn thành 105, chưa HT 110, còn tạo GV 120), tiêu đề cột số xuống dòng
- [x] Ý 6: số 0 → để trống y ERP `numberOrHyphen` (mọi cột số), riêng "SL còn được tạo giao việc" giữ 0 (ERP `my_number`). Chỉ màn, In/Excel chưa đổi
- Kiểm: compile template + babel 3 file OK; chưa mở trình duyệt. CHƯA commit.

### 2026-11-17 — #12197 QA (Huyền Trang) màn CHI TIẾT
- [x] Bug 1 + 2: tab SC-BD / Bảo hành bật ô TÌM NHANH (bỏ `:show-quick-search="isInstall"`) → bộ lọc cùng bố cục tab Lắp đặt (hàng tìm nhanh + nút Tìm kiếm / Xóa lọc ở trên, ô lọc ở dưới). Tìm theo THIẾT BỊ trong HĐ: tên / model / mã hàng / seri — BE `InstallDeliveryRepairDetailReportService::filterDevices()` lọc trước khi phân trang (nhóm rỗng giữ nhãn); FE gửi `keyword` cả 3 tab; dòng điều kiện bản in ghi "Thiết bị: "…"" (PrintService)
- [x] Bug 3: 2 toast "Bạn không được làm việc tại công ty này" = popup chọn hàng nhận `company-id` = Công ty đang LỌC → `ProductPickerRequest` 403 ở cả search + tree-counts (interceptor toast mỗi cái 1 lần). Bỏ truyền `company-id` (hàng hóa dùng chung, popup tự dùng công ty đang làm việc). Chưa đụng interceptor chung `plugins/axios.js` (gộp toast trùng = hàm chung, cần hỏi)
- [x] Bug 4: × xoá nhanh — đã làm ở #12194 (ô chọn cấp) + #12196 (ô Hàng hóa `V2BasePickerInput`); Công ty / Phòng ban / Hợp đồng / ô tìm nhanh vốn có ×. Ảnh QA chụp trên dev chưa có bản này
- Kiểm: `php -l` 2 file; tinker gọi `service()` 2 tab với keyword (tên đầy đủ / chữ hoa / không khớp → 0) OK; compile template + babel index.vue OK; chưa mở trình duyệt. CHƯA commit.

### 2026-11-17 — #12199 QA (Huyền Trang) màn CHI TIẾT — STT + số 0
- [x] Ý 1 "1.2 đâu": ERP đánh cứng "x.1 Công tháo lắp / x.2 Danh sách dịch vụ / x.3 Danh sách vật tư", nhóm dịch vụ ẩn khi thiết bị không có dịch vụ → nhảy 1.1 → 1.3 (ERP cũng vậy). Sửa BE `deviceNodes()`: STT vật tư liền sau nhóm trước (không có dịch vụ → x.2, con x.2.n). In / Excel dùng chung `no` từ BE. Tab Bảo dưỡng (`extendNodes`) vốn đánh liên tục, không đổi
- [x] Ý 2 "-" → trống, 0 giữ 0: đã làm ở #12196 (đối chiếu lại ERP `detail.blade.php`: mọi cột `numberOrHyphen`, riêng "còn được tạo giao việc" `my_number`). Ảnh QA chụp trên dev chưa có bản đó. Bổ sung: số 0 cột "còn được tạo giao việc" bỏ màu mờ `rsum-tb__zero` (#c2cbd6 gần như không thấy) → màu chữ thường — `DetailTreeTable.vue`
- Kiểm: `php -l`; tinker HĐ bảo hành local → 1 / 1.1 / 1.2 Danh sách vật tư, can_request = 0; compile template + babel DetailTreeTable OK; chưa mở trình duyệt. CHƯA commit.

### 2026-11-17 — #12200 Đổi nút "Xóa lọc" → "Làm mới" (2 màn BC theo dõi LĐ-BG-SC-BD + chi tiết)
- [x] Bỏ `reset-button-text="Xóa lọc"` ở `install-delivery-repair/index.vue` + `install-delivery-repair-detail/index.vue` → dùng mặc định `V2BaseSmartFilterPanel` ("Tìm kiếm" / "Làm mới"), hành vi giữ nguyên. Làm cùng màn BC bán hàng theo mặt hàng
- Kiểm: compile template OK; chưa mở trình duyệt. CHƯA commit.

### 2026-11-18 — Check: lọc 01/11–17/11/2026 ERP 10 bản ghi, HRM 11 (chỉ điều tra, không sửa code)
- [x] So API dev 2 bên cùng kỳ: 10 nhóm trùng khớp; HRM thừa **firm:19648 `HĐ_TPE_HN_KD2_26_0653_MINHKHUE`** (hiện 1 dòng: YC `TPE.YCLDBG.2026001191` · GV `TPE.PGV.2026011933` · `PCT-14690` 12/11/2026 10:00–17:00, chưa NKQ/duyệt KQ)
- Nguyên nhân = lệch ERP CÓ CHỦ Ý đã ghi ở design.md: ERP `getData()` `groupBy(contract_id)` rồi mới `filter()` ngày → so ngày trên 1 dòng ĐẠI DIỆN tuỳ ý của HĐ (ở đây dòng tiến độ 15572 `PCT-12502` 27/05–06/06/2026) → HĐ rơi khỏi kỳ tháng 11 dù có phiếu công tác 12/11. HRM lọc từng dòng con → HĐ hiện với đúng dòng PCT-14690
- Hệ quả bên ERP: HĐ đã có công tác cũ thì công tác mới phát sinh không bao giờ lên báo cáo theo kỳ → HRM đúng hơn. Đề xuất giữ; nếu user muốn khớp số với ERP thì phải bắt chước lỗi (không khuyến nghị)

### 2026-11-18 — Sửa ERP: lọc ngày công tác theo từng dòng (khớp HRM)
- [x] ERP `ReportInstallDeliveryRepairService::getData()`: nhóm (HĐ / YC giao việc khác) hiện khi có ≥ 1 dòng Đã duyệt VÀ ≥ 1 dòng tiến độ có công tác trong kỳ (whereExists từng dòng) — bỏ lọc ngày trên dòng đại diện ở `filter()`
- [x] ERP `assignProcess()` / `assignProcessOtherRequest()`: dòng con chỉ lấy dòng có công tác trong kỳ (y HRM)
- [x] Kiểm: `php -l` OK; tinker local (ERP + HRM cùng `gop_db`) 3 kỳ 01–28/07, 01–30/06, 15/05–10/06/2026: ERP mới = HRM đúng từng khoá nhóm + số dòng con (542/560, 594/611, 534/559); ERP cũ 527/545, 580/605, 525/564. Helper mới `filterWorkDate()` + `whereHasWorkInRange()`, `filter()` bỏ phần ngày. Chưa mở trình duyệt, CHƯA commit, chưa deploy dev

### 2026-11-18 — #12186 phản hồi lần 2 (Huyền Trang): phân trang POPUP về kiểu V2BasePagination
- [x] P3-T9. Popup bấm số của 3 màn (`install-delivery-repair` ItemListModal, `install-delivery-repair-detail` DetailDrillModal, `sale/sale-by-product-report` SaleByProductDetailModal + SaleByProductAllItemsModal): bỏ slot `#pagination` (ReportPagination / ReportListPagination / SaleByProductPagination) → vỏ `V2BaseReportModal` tự dùng `V2BasePagination` mặc định (thanh xám `.paging`, nút tròn nhỏ) — y popup báo cáo chuyến xe (ảnh mẫu QA)
- Kiểm: compile template + babel 4 file OK; chưa mở trình duyệt. Bảng CHÍNH của 3 màn vẫn dùng phân trang cũ (QA chỉ nêu popup) — chờ user chốt có đổi luôn không. Đã commit + push develop `27d24e8b1`.
- [x] 19/11 check lại phản hồi #12186 (journal #3, 18/11 10:04): đúng nội dung P3-T9, code đã có trên origin/develop; Redmine chưa có ghi chú trả lời, trạng thái vẫn "Phản hồi" — không sửa thêm code
