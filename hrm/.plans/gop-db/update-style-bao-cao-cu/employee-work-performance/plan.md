# Báo cáo kế hoạch & kết quả làm việc theo nhân viên — chuyển style chung (report-styles)

Màn: `/assign/report/employee-work-performance`. Nhánh `gop_db-update-style-ewp` (hrm-api + hrm-client), worktree
`websites/wt-update-style-ewp` (cổng 8023/3023). User cho phép code 05/10/2026. Chưa merge gop_db.

## Quyết định đã chốt (user 05/10/2026)
- Phân trang bảng chính ở **BE**, theo nhóm Phòng ban (cấp 0), 20/trang, chọn 10/20/50/100; khối tổng hợp + dòng TỔNG
  tính trên toàn bộ; trang vượt quá -> về trang cuối.
- Làm luôn 3 điểm logic: chống response cũ đè mới (reportSeq / reportParams), Excel popup tải từ server
  (`drill/export`, thay blob `.xls`), ô Công ty theo `filter-options` + `can_change_company` (luôn false — báo cáo
  không có cấp tổng công ty, BE chỉ nhận đúng công ty đang làm việc).

## Điểm UI tự chốt theo khuôn
- ⓘ MỤC ĐÍCH BÁO CÁO lên `#title-suffix`; nút "In báo cáo" -> "In danh sách"; PrintOptionsModal: In trước, Hủy cuối.
- Kỳ đứng đầu bộ lọc; ô Tuỳ chọn chưa đủ 2 ngày thì chưa gọi API; 2 công tắc gộp 1 ô (8 ô = 2 hàng × 4).
- Khối tổng hợp: CSS khuôn, ẩn nhóm trạng thái = 0, số đếm đầu việc bấm được (popup key ALL); bỏ tô màu 5 loại.
  ⓘ từng ô gộp vào ⓘ của khối.
- Bảng: `.ptr-table` + `V2BaseTableScroll` (tiêu đề dính, 2 thanh cuộn ngang), ô chọn cấp trong tiêu đề cột (mặc định
  "Đến Bộ phận"), STT I / 1 / 1.1, dòng TỔNG cam, bỏ tô màu cột loại + dòng ghi chú dưới bảng (chuyển vào ⓘ dòng TỔNG).
- Popup: bỏ `mr-2/ml-0` footer, đếm dòng định dạng `4,049`; In/Excel danh sách mang `q` + cột đang sắp (BE lọc/sắp
  cùng tập trường với popup).

## Tasks
- [x] BE: `getPage()` (groups + meta + generated_at), `filterOptions()`, `getDrillRows` nhận `q` + `sort/dir`,
      `drill/export` (EmployeeWorkDrillExport + blade), routes
- [x] BE test `tests/Feature/EmployeeWorkPerformance/ReportApiTest.php` (6 ca, RED -> GREEN); 5 bộ Unit cũ xanh
- [x] FE: index, WorkSummary, WorkTable, DrillNum (thay DrillCell), InfoTip, PrintOptionsModal, WorkDrillModal, api.js, format.js
- [x] E2E `e2e/tests/assign/employee-work-performance.spec.ts` (6 ca) xanh trên 3023
- [x] Vòng góp ý 06/10: Loại công việc xuống cuối + `CheckboxMultiSelect`; ô chọn cấp bỏ `height="18px"` (bị bóp/lệch)
- [x] Vòng góp ý 06/10 (2): bỏ "Chỉ tính việc chủ trì" (BE bỏ qua host_only) — chỉ meeting có chủ trì, ai trong danh
      sách thực hiện đều tính; bỏ cột Vai trò (popup / bản in / Excel) + KPI tỷ lệ việc chủ trì (user chọn bỏ hẳn);
      "Chỉ hiện nhân viên có việc" dời lên dòng tiêu đề khối tổng hợp cạnh nút Thu gọn
- [x] 06/10 (3): ô Loại công việc `col: 6` + chip bỏ đệm dọc (1 dòng, khung 32px)
- [x] 06/10 (4): bỏ vạch `::before` đầu tiêu đề bộ lọc / tiêu đề card trong `assets/scss/sale-theme.scss` — áp TOÀN BỘ
      theme Sale (user chốt), commit riêng de8779fb9 trên nhánh này -> merge gop_db là mọi màn theme Sale đổi theo
- [x] 06/10 (5): Phiếu công tác / Phiếu giao việc — ẩn cột Tên công việc khi popup chỉ 2 loại này (lẫn loại: "—"),
      cả bản in / Excel; Mã phiếu bấm mở panel; panel khối "Thông tin phiếu" tải qua `GET …/item` (user chọn đầy đủ)
- [x] 06/10: SRS `SRS - Báo cáo kế hoạch & kết quả làm việc theo nhân viên.docx` (skill srs-documenter, form 2026-09-24 +
      màn báo cáo: 2.1.6 / 2.1.7 / popup 2.5–2.6). 06/10 đã CHUYỂN về folder feat gốc `.plans/gop-db/bao-cao-ke-hoach-lam-viec-nhan-vien/` (ghi đè bản 03/10 giao diện cũ);
      sinh lại: `python3 .plans/gop-db/bao-cao-ke-hoach-lam-viec-nhan-vien/gen_srs.py` (ảnh ở `ewp_shots/`, không commit)
- [x] 06/10 (6): Meeting trong popup mở panel chi tiết meeting DÙNG CHUNG `ReportMeetingDetailDrawer` (thay panel tự dựng,
      có nút "Xem biên bản" → xem trước bản in biên bản khi meeting đã có biên bản). Làm thẳng trên gop_db (user chốt), chưa
      commit. BE: `Meeting::canViewByEmployeeWorkPerformanceReport()` + `EmployeeWorkPerformanceService::applyEmployeeScope()`
      (nguồn duy nhất phạm vi NV 1612–1614, allowedEmployeeIds() dùng lại); test `tests/Feature/EmployeeWorkPerformance/
      MeetingCanViewTest.php` 3 ca (RED → GREEN), hồi quy EWP 13 + Unit 39 + ReportMeetingView 6 + MBE canView 3 xanh.
      FE: WorkDrillModal emit `open-meeting`, index dựng drawer (above-modal) + openMeetingReport; bỏ nhánh Meeting chết
      trong `.wd-drawer`. E2E: thêm ca 8 (chưa chạy — user tự kiểm trên app)
- [x] 06/10 (7): "Chỉ lấy NV đang làm việc" cho nhóm Báo cáo thị trường — user chốt: người ĐÃ NGHỈ giữ nếu có số liệu
      trong kỳ, không có thì bỏ; ô chọn NV giữ nguyên (mặc định đang làm, 🔒 hiện cả người đã nghỉ). Rà 7 báo cáo: chỉ báo cáo
      này dựng dòng từ danh mục NV (6 báo cáo kia NV đi theo chứng từ → không đổi). Sửa getData(): bỏ NV hồ sơ status ≠ 1 không
      có đầu việc trong kỳ (xét trước ô Loại / Trạng thái), "/ N nhân viên" đếm theo tập đó. Test `WorkingEmployeeTest` 3 ca
      (đỏ trước sửa: 795 ≠ 402), EWP Feature 16 + Unit 39 xanh. Chưa commit
- [x] 06/10 (8): Nhóm "Không thuộc bộ phận" cho 4 báo cáo Giao việc phân cấp Phòng ban › Bộ phận (user chốt: phòng CÓ chia
      bộ phận → NV chưa gán vào nhóm ngang cấp bộ phận, đứng CUỐI; phòng KHÔNG chia → bỏ cấp, NV thẳng dưới phòng; quyền
      theo phòng). (1) EWP: TreeBuilder dựng node `part:__no_part__` + filterByNodeKey quy part rỗng về sentinel; FE WorkTable
      `childLevel` cho NV thẳng dưới phòng hiện ở "Đến Bộ phận". (2) Phát triển thị trường – KH: đổi tên, đứng cuối,
      `filterRowsByKey` sửa popup nhóm trống. (3) Kết quả dự án TKT: nhóm `part:0` thay vì NV lẫn sau bộ phận. (4) Kết quả CSKH
      tiềm năng: đổi tên "Chưa xác định bộ phận", `emptyLast`. Test: EmployeeWorkTreeTest (sửa), NoPartGroupTest, 3 Unit
      *NoPartTest — đỏ trước sửa, xanh sau; hồi quy EWP + PotentialCustomerTracking 21 + ReportMeetingView 6 xanh. Báo cáo
      đánh giá năng lực (Đào tạo) để sau. Chưa kiểm FE bằng trình duyệt, chưa commit
- [x] 06/10 (9): Đổi chữ hiển thị Task → Nhiệm vụ, Issue → Vấn đề (báo cáo + my-todo). EWP FE: index, WorkSummary, WorkTable
      (ⓘ "SỐ NHIỆM VỤ" / "SỐ VẤN ĐỀ"), WorkDrillModal; BE: PrintService TYPE_LABEL + Export cột Excel. my-todo: Task đã là
      "Nhiệm vụ", chỉ đổi Issue ở work-item-types.js + TodoFilterBar. Mã loại task/issue giữ nguyên. E2E: employee-work-perf
      (nhãn ô Loại) + work-calendar-popup (tiêu đề popup thật là "Chi tiết nhiệm vụ"/"Chi tiết Vấn đề" — spec đang kiểm chữ cũ).
      BE EWP 17 + 8 xanh. Chưa commit
- [x] 06/10 (10): Popup Meeting — user chốt: (a) popup CHỈ toàn Meeting (metric meeting / lọc Loại = Meeting) thì cột +
      ô lọc Trạng thái + In/Excel dùng 5 trạng thái GỐC (Đang tạo · Lên lịch · Chốt lịch · Hoàn thành · Hủy), màu BE trả;
      KPI vẫn theo 4 nhóm; popup lẫn loại giữ 4 nhóm. (b) Panel meeting DÙNG CHUNG (mọi báo cáo): thêm Người chủ trì + File
      đính kèm (tài liệu chuẩn bị + kèm biên bản, V2BaseFileList) + nút "Xem chi tiết" mở /assign/meeting/{id}/show tab mới
      (chỉ panel báo cáo, my-todo không). (c) Excel đã đủ cột như popup → bỏ qua.
      Làm: BE collector `status_color` (meeting) · Service `isMeetingOnly()` + lọc `status` + sắp theo status · PrintService
      cột Trạng thái/dòng mô tả lọc ra trạng thái gốc. FE WorkDrillModal `listTypes`/`meetingOnly` (đổi qua lại thì xoá giá trị
      lọc cũ); MeetingDrawerBody (Người chủ trì trong "Thành phần tham dự", khối "File đính kèm"); WorkItemDetailDrawer prop
      `meeting-detail-link` + truyền `above-modal` xuống thân; ReportMeetingDetailDrawer bật nút; V2BaseFileList thêm prop
      `previewZIndex` (user cho phép) để popup Xem trước nổi trên panel 1060. Kiểm MCP: 816 meeting = 3+85+139+492+97, Excel
      lọc Đang tạo ra 3 dòng, xem trước nằm trên panel, Xem chi tiết mở tab mới tải được meeting. Unit EWP 56 xanh. E2E thêm
      ca 9 (chưa chạy). Chưa commit
- [x] 06/10 (11): Bỏ panel xem nhanh tự dựng (`.wd-drawer`) trong popup — user chốt: Nhiệm vụ / Vấn đề bấm Mã/Tên mở popup
      chi tiết CÓ SẴN (`CreateTaskModal.view` / `CreateIssueModal.open`, chỉ xem + `hideActions`, khuôn FilesTab.vue:401-403,
      tải async khi bấm lần đầu); Phiếu công tác / Phiếu giao việc mở MÀN chi tiết tab mới (`/assign/assign_business/{id}/show`,
      `/assign/assign_jobs/{id}/show`). Chỉ sửa WorkDrillModal.vue (gỡ ~400 dòng drawer + CSS). Kiểm MCP: task 1 mở popup
      "Chi tiết nhiệm vụ" đè popup báo cáo, chỉ nút Đóng (khung bình luận của popup gốc giữ nguyên), đóng thì popup báo cáo
      còn; PCT-07986 / PGV-00315 mở đúng màn tab mới. Vấn đề: DB local rỗng → chỉ kiểm đường gọi (popup "Chi tiết Vấn đề" +
      GET assign/issues/{id}). E2E: sửa ca 7, thêm ca 10 (chưa chạy). Chưa commit
- [x] 06/10 (12): Bản in danh sách (popup + màn chính) — user chốt: (a) thể hiện ĐÚNG đối tượng + phạm vi đang in, (b) không
      in ô lọc "Tất cả"; chỉ báo cáo này, áp cả bản in màn chính. PrintService: `detailTitle()` theo chỉ tiêu ("DANH SÁCH
      MEETING", "DANH SÁCH ĐẦU VIỆC QUÁ HẠN"…; total giữ "DANH SÁCH CHI TIẾT ĐẦU VIỆC"), `describeNode()` từ `key` (gồm 2
      sentinel "Chưa phân phòng ban" / "Không thuộc bộ phận"), `describeFilters()` chỉ ghi điều kiện đang lọc + ô lọc riêng
      popup + từ khoá, bỏ chiều đã nằm ở tiêu đề / dòng đối tượng. Blade detail: tiêu đề động + dòng đối tượng (đậm). Trước
      sửa: popup Meeting NV Dương Đức Thế in "Phòng ban: Tất cả · Nhân viên: Tất cả · Loại công việc: Tất cả". Unit
      EmployeeWorkPrintHeaderTest 5 ca, cả bộ EWP 61 xanh; kiểm MCP 9 tổ hợp + xem trước thật. Chưa commit
- [x] 07/10 (13): Ô lọc đơn vị. Màn chính: `V2BaseCompanyDepartmentFilter` đã tự lọc Phòng theo Công ty, Bộ phận theo
      Phòng (đo lại đúng); lỗi thật là công tắc 🔒 cạnh nhãn — bật lên thì ô lấy cả đơn vị đã khoá (đo được 9 phòng khoá,
      đang chọn sẵn "Phòng ban test 2"). User chốt ẩn công tắc cả 4 ô (`:show-locked-toggle="false"`, chỉ sửa index.vue).
      Popup: `optionsOf` thêm ràng buộc cha → con (Bộ phận theo Phòng, Nhân viên theo Phòng/Bộ phận), `onFilterChange`
      đổi cha xoá con trước khi gọi API (1 lượt). Kiểm MCP: phòng 51 → Bộ phận 10→2, Nhân viên 250→72 trên DOM; đổi phòng
      xoá bộ phận + NV. E2E thêm ca 11 (chưa chạy). Chưa commit
- [x] 07/10: Chạy e2e employee-work-performance.spec.ts (`--no-deps --workers=1`): 11/11 xanh, không retry. 2 lỗi ở CA TEST đã
      sửa (không phải lỗi màn): ca 9 đếm ô Trạng thái khi bảng còn "Đang tải…"; ca 9 đo "xem trước nằm trên panel" ở điểm
      ngoài khung popup (popup 800px ở màn 1366) — trace xác nhận popup xem trước z 1070 > panel 1060. Ca 10 phần Vấn đề tự bỏ
      qua vì DB local không có issue.
- [ ] User check trên app · merge gop_db (chờ user)

## Ngoài phạm vi (ghi lại)
- BE `GET assign/report/employee-work-performance/item` (+ `getItemDetail`) KHÔNG còn FE nào gọi sau 06/10 (11) — chờ user
  chốt có gỡ không (đụng BE).
- Drawer chi tiết đầu việc trong popup vẫn là drawer tự dựng (`.wd-drawer`) — 5 loại phiếu, `WorkItemDetailDrawer`
  chưa hỗ trợ đủ; header đã đúng gradient khuôn.
- Endpoint popup giữ tên `/drill` (khuôn gọi `/item-list`), popup tự tải 1 lượt — đổi hợp đồng là việc riêng.
- Người không quyền bị router app chặn (trang 404 "không được cấp quyền") trước khi vào màn.
- ⚠️ Lỗi ô chọn cấp bị bóp/lệch có ở CHÍNH khuôn `report-styles` (template TrackingTable ép `height="18px"` cho cỡ
  `xs` 26px) -> mọi báo cáo đã chuyển style đều dính (đo potential-customer-tracking: 18px, chữ line-height 24px). Chưa
  sửa skill / các báo cáo khác — chờ user quyết.

### Checkpoint — 2026-10-06 (wrap up)
Vừa hoàn thành: báo cáo 3 employee-work-performance chuyển style chung + phân trang BE + 5 vòng góp ý 06/10 (Loại công
việc cuối + CheckboxMultiSelect; ô chọn cấp bỏ height 18px; bỏ "Chỉ tính việc chủ trì" + cột Vai trò; "Chỉ hiện nhân viên
có việc" lên dòng tiêu đề khối tổng hợp; P. công tác / P. giao việc bỏ cột Tên công việc + panel "Thông tin phiếu"; bỏ
vạch ::before tiêu đề theme Sale) + SRS. Nhánh `gop_db-update-style-ewp` (worktree `websites/wt-update-style-ewp`,
api 8023 · client 3023): api 214bcfd1b..c3add6709 (4 commit), client 855d49b86..6f4912ae7 (7 commit, gồm de8779fb9 sửa
theme Sale toàn cục). PHPUnit Feature 10/10 + Unit cũ 39/39; e2e `e2e/tests/assign/employee-work-performance.spec.ts` 7/7.
Đang làm dở: không.
Bước tiếp theo: user check app 3023 → lệnh merge gop_db (2 repo). Chưa push.
Còn treo (hỏi user): sửa lỗi khuôn report-styles (ô chọn cấp height 18px) cho skill + báo cáo khác; số "3174" không dấu phẩy
ở phân trang V2BaseReportModal (component dùng chung); cột Trạng thái bản in danh sách chi tiết hẹp (có từ trước).
Môi trường: `.env` worktree api có thêm ERP_URL=https://erp.eteksofts.com (cho letterhead bản in local) — không phải source.
Blocked:
- [x] 06/10: ĐÃ MERGE + PUSH gop_db (api 45b8a2b2f, client 88c9f3f01)

### Checkpoint — 2026-10-06 (wrap up, chiều)
Vừa hoàn thành (làm thẳng trên gop_db, user chốt): (6) Meeting trong popup mở panel meeting dùng chung + Xem biên bản —
ĐÃ PUSH (api 7fe53a02d, client 94c8a39c3); (7) chỉ NV đang làm việc + (8) nhóm "Không thuộc bộ phận" cho 4 báo cáo Giao việc —
ĐÃ PUSH (api 0abaa3194, client c8c06e90a); (9) đổi chữ Task → Nhiệm vụ, Issue → Vấn đề (báo cáo + my-todo) — CHƯA COMMIT
(api: PrintService, Export; client: 4 file báo cáo + TodoFilterBar + work-item-types.js; e2e 2 spec, e2e không nằm trong git).
SRS báo cáo đã chuyển về folder feat gốc `.plans/gop-db/bao-cao-ke-hoach-lam-viec-nhan-vien/`.
Đang làm dở: không.
Bước tiếp theo: user kiểm (9) trên app → commit + push gop_db. Chưa kiểm FE bằng trình duyệt cho (6), (8), (9) — Playwright MCP
chưa có phiên đăng nhập (127.0.0.1:3000 về /login); ca e2e 8 (panel meeting) + spec đổi chữ chưa chạy.
Còn treo: lỗi phiếu công tác ở 4 bước thanh toán (8–11) bị tính "Đang thực hiện"/"Quá hạn" thay vì "Đã hoàn thành" (lệch ⓘ,
~29% phiếu) — chưa sửa, chờ user; Báo cáo đánh giá năng lực (Đào tạo) chưa có nhóm "Không thuộc bộ phận" (trùng STT, nhóm
không tên khi part_id = 0); khuôn report-styles ô chọn cấp height 18px.
Blocked:

### Checkpoint — 2026-10-07 (wrap up)
Vừa hoàn thành: 06/10 (10)→(13) + e2e 11/11 xanh; ĐÃ COMMIT + PUSH gop_db (api e20e02e04, client c62d1a79b)
Đang làm dở: —
Bước tiếp theo: user kiểm trên app; (tuỳ) gỡ endpoint BE `employee-work-performance/item` không còn FE gọi — chờ user chốt
Blocked: —
