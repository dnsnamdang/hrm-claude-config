# Biên bản meeting — "Ghi nhận nội dung meeting" + ô tick "Giao người xử lý" (web + app) — @namdangit

Yêu cầu 08/11/2026:
- Đổi tên mục "Các nội dung khác" → **"Ghi nhận nội dung meeting"**.
- Dòng mặc định chỉ bắt buộc Nội dung. Thêm ô tick **"Giao người xử lý"** — tick mới hiện
  Người đề xuất (không bắt buộc) · Người thực hiện (bắt buộc) · Hạn dự kiến (bắt buộc).

## Quyết định đã chốt (08/11)
- Q1 (user): dòng không tick vẫn có nút "Giao" ở màn Chi tiết web (#11456); popup tạo nhiệm vụ điền sẵn tên, người + hạn để trống.
- Claude tự chọn (đã báo user):
  - KHÔNG thêm cột: trạng thái tick suy từ "có người thực hiện" ⇒ biên bản cũ hiện đã tick.
  - Payload gửi `reports[i].has_assignee`; thiếu cờ (app bản cũ) ⇒ coi như tick (giữ luật cũ).
  - Bỏ tick ⇒ BE gỡ người đề xuất / người thực hiện / hạn trước validate + khi lưu.
  - Bản in / Excel giữ đủ cột, dòng không giao để trống. Vẫn bắt buộc ≥ 1 dòng khi Hoàn thành.
  - Phương án xử lý luôn hiện, không bắt buộc.
- Không migration, không quyền mới.

## Task
### BE (hrm-api gop_db)
- [x] Trait `NormalizesMeetingReportRows` + gắn vào Create/Update request; rule `required_if:reports.*.has_assignee,1`
- [x] `MeetingService::syncReports` bỏ dữ liệu giao người khi `has_assignee = 0`
- [x] `meeting_record.blade.php` đổi tên mục
- [x] Test PHPUnit: dòng không tick lưu được; tick mà thiếu người/hạn ⇒ lỗi validate (meeting trả HTTP 400); thiếu cờ ⇒ luật cũ

### Web (hrm-client gop_db)
- [x] `MeetingReport.vue`: đổi tên mục, ô tick, ẩn/hiện 3 cột, nút Giao ở mọi dòng đã lưu
- [x] `MeetingForm.vue`: kiểm thiếu trường theo tick + câu báo lỗi
- [x] `MeetingPrintPreview.vue`: đổi tên mục
- [x] Kiểm Playwright MCP (đo DOM)

### App (TPE_APP develop)
- [x] `meeting_report_item_page.dart`: ô tick + ẩn/hiện 3 ô
- [x] `meeting_minutes_page.dart`: đổi tên mục, thẻ dòng không giao người
- [x] Kiểm máy ảo tpeLocal

### E2E
- [x] Spec mới `e2e/tests/assign/meeting-report-assignee.api.spec.ts` (CHƯA chạy — chờ user)

### Checkpoint — 08/11/2026 11:15
Vừa hoàn thành: code 3 repo + kiểm. BE: `MeetingReportAssigneeRulesTest` 5/5. Web (Playwright MCP, meeting thử 3040 trên db_gop_6_11): ô tick bật/tắt 3 cột, lưới đủ 12 cột, Lưu thiếu người ở dòng tick → lỗi đúng dòng; dòng không tick lưu được (`has_assignee=false`, người/hạn null); dòng có người mở lại tự tick; màn Chi tiết nút Giao ở cả 2 dòng, popup điền sẵn tên; Hoàn thành chặn FE đúng dòng. App (máy ảo tpeLocal): nhãn GHI NHẬN NỘI DUNG MEETING, thẻ không giao ẩn dòng người/hạn, thêm dòng không tick lưu được, tick thiếu người → BE báo đỏ đúng thẻ. Đã xoá meeting thử 3040 + dữ liệu kèm.
Đang làm dở: —
Bước tiếp theo: user xem diff → commit/push (hrm-api + hrm-client gop_db, TPE_APP develop); chạy spec e2e mới khi user bảo. Không migration.
Blocked:

## Mockup app vẽ lại (08/11 11:20) — chờ user duyệt
`meeting-mobile.pen`, khung top-level "BIÊN BẢN — vẽ lại 08/11" (x 2900, y 12620), 3 màn: 09' danh sách · 10a' chỉ ghi nhận · 10b' tick Giao người xử lý.
- 09': các dòng gom 1 thẻ; mỗi dòng = số tròn + nội dung + phương án (↳, nếu có) + hàng "Người đề xuất → Người thực hiện" + chip hạn (chỉ dòng có giao người). Nhãn "GHI NHẬN NỘI DUNG MEETING *" + đếm dòng.
- 10': ô tick dạng thẻ có mô tả; Người đề xuất + Người thực hiện * chung 1 hàng; Hạn dự kiến * hàng riêng; Nội dung 3 dòng, Phương án 2 dòng.
- Footer theo quy ước 29/10: nút chính trái, Huỷ / Quay lại phải (code app hiện đang ngược — sửa khi code mockup này).
- [ ] User duyệt mockup → hỏi phạm vi → code lại 2 màn app
- [x] User duyệt mockup (08/11) → user "làm" (kèm bổ sung hỏi Hoàn thành sau Lưu biên bản, web + app)

## Đợt 2 (08/11) — code mockup 09'/10' + hỏi "Hoàn thành luôn?" sau Lưu biên bản
- [x] App `meeting_report_item_page.dart`: ô tick dạng thẻ, Người đề xuất + Người thực hiện 1 hàng (maxLines 1, nhiều người "Tên +N"), Hạn hàng riêng, Nội dung 3 / Phương án 2 dòng, footer Lưu nội dung trái · Hủy phải
- [x] App `meeting_widgets.dart`: `MeetingSelectRow.maxLines` (mặc định 2, không đổi chỗ cũ)
- [x] App `meeting_minutes_page.dart`: danh sách gom 1 thẻ (số tròn · nội dung · ↳ phương án · "đề xuất → thực hiện" + chip hạn), nhãn có số dòng, footer Lưu biên bản trái · Quay lại phải; lưu xong hỏi Hoàn thành khi Chốt lịch + can_complete + ≥1 nội dung + có kết luận
- [x] App `meeting_hub_page.dart`: `_complete({confirm})` — từ màn biên bản không hỏi lần 2; xong pop về màn đã mở Hub
- [x] Web `MeetingForm.vue` `canOfferCompleteAfterSave()` (tab Biên bản · status 2 · nút Hoàn thành có · can_complete · ≥1 nội dung + kết luận) + `backUrl` nhận from=my-todo
- [x] Web `_id/edit.vue`: lưu xong hỏi `$confirm` → Hoàn thành chạy `handleComplete()`; from=my-todo quay về /assign/my-todo
- [x] Web `my-todo/index.vue`: nút Sửa meeting ở drawer gửi `from=my-todo` (ngoài phạm vi đã báo, cần cho yêu cầu "về Việc của tôi")
- [x] Kiểm: app máy ảo (từ Danh sách + từ Việc của tôi; Để sau; thiếu kết luận không hỏi; lỗi chặn ở lại Hub) · web Playwright 4 ca (my-todo Để sau / my-todo Hoàn thành / danh sách Hoàn thành / tab Thông tin không hỏi). Meeting thử 3041 đã xoá.
- [x] E2E: `e2e/tests/assign/meeting-complete-after-minutes.spec.ts` (6 ca, 6/6 xanh) + `meeting-report-assignee.api.spec.ts` chuyển sang fixture tự dựng (4/4 xanh); fixture dùng chung `e2e/utils/e2eMeetingFixture.ts` (chép meeting Chốt lịch loại 14, chủ trì = tài khoản gọi, dọn sạch ở afterAll)
- Chạy kèm 08/11: meeting-room-sync 7/7, meeting-target 3/4, meeting-participants 0/4 (đỏ ở beforeAll: DB db_gop_6_11 không có meeting Lên lịch của tài khoản test → dữ liệu, không do thay đổi này). meeting-investment-survey + meeting-form-sections KHÔNG chạy: fixture E2E_* trong e2e/.env (6353, 6356…) không còn trong DB, cần chạy seed (chưa được phép).

## Đợt 3 (08/11) — chạy lại spec meeting cũ (user "làm 1 + 2")
- [x] (1) Chạy seed `e2e_meeting_survey_seed.php` + `e2e_customer_demand_seed.php` vào db_gop_6_11; `e2e/.env` cập nhật E2E_SYSTEM 3053 · INTERNAL 3054 · LOCKED_SCOPE_MEETING 3055 · LOCKED_SCOPE_ID 69 · SCOPE_ROW 44 · EDITABLE 3058 (bản cũ lưu scratchpad e2e.env.bak)
- [x] (2) `meeting-participants` + `meeting-target` ca 4 tự dựng meeting Lên lịch loại 13 qua `createE2eMeeting(..., {status:1, meetingTypeId:13, upcoming:true})` → 4/4 + 4/4 xanh
- [x] Lệch người tạo fixture (seed ghi cứng e2e_assign, e2e/.env TEST_EMAIL = namdangit): user "làm cả 3" →
  (2) SQL đổi created_by/host/thành viên 6 meeting E2E-SURVEY-*/E2E-DEMAND-* sang namdangit (13);
  (1) sửa hrm-api `database/e2e_meeting_survey_seed.php` + `e2e_customer_demand_seed.php` đọc chủ fixture từ env E2E_OWNER_EMAIL → TEST_EMAIL trong e2e/.env → e2e_assign, chạy lại (creator 13);
  sửa `e2e_meeting_survey_fixture.php` cho DB có rbac (roles.company_id bắt buộc, role_has_permissions không có company_id — chỉ ghi khi có cột), chạy với E2E_SYSTEM_MEETING_ID=3053 → user 1344/1345, meeting 3061, E2E_MEETING_ONLY_MEETING_ID=3061, cache:clear;
  (3) chạy bằng e2e_assign: KHÔNG làm — ngược với (1)(2), ghi đè phiên namdangit.
- Kết quả: meeting-investment-survey 19/19 · meeting-form-sections 3/6 — 3 ca đỏ đo khuôn (padding card 6px≠4px, vòng số ① không đặc, header /customer-care/warranty-repair-requests cao 50≠36): diff đợt này không đụng class/CSS → không do đợt này, CHƯA lần nguyên nhân gốc.
- Lưu ý: `meeting-host.api` dùng token e2e_assign trên E2E-SURVEY-SYSTEM (nay thuộc namdangit) → có thể 403, chưa chạy.

## Lần nguyên nhân 3 ca đỏ meeting-form-sections (08/11, Playwright MCP đo DOM) — KHÔNG do đợt này, KHÔNG phải hồi quy
- Ca 1 "card chính p-1 = 4px": `.p-1` ra 6px vì theme Minton `assets/scss/config/{default,corporate}/_variables.scss` đặt `$spacer: 1.5rem` (từ 2021) → app.scss sinh `.p-1 {0.375rem !important}` nạp SAU bootstrap dist (0.25rem). Không file nào đổi từ 19/10. Spec giả định sai. Phần header của ca này đo lại: 6 header đều 36px, lệch tâm 0, không gạch dưới.
- Ca 2 "vòng số đặc khi đủ": `.mf-num` có `transition: background-color .2s`; spec đo ngay khi `is-done` vừa bật → ra màu đang chuyển (tái hiện: 0ms rgb(86,77,230), 300ms rgb(79,70,229) đúng). Lỗi thời điểm đo.
- Ca 3 "header màn bảo hành 36px": `WarrantyRepairRequestForm.vue` có `@media (max-width:1400px)` cho tiêu đề chiếm 1 hàng + cụm nút xuống dưới (Redmine #11170, bfea31a42 24/08, CỐ Ý). Project chromium chạy viewport 1280 (preset Desktop Chrome đè 1440 của config) → 50/62px; ở 1440 đều 36px.
- [x] Sửa spec (user "Làm" 08/11): ca 1 kiểm class p-1 + so padding với `.p-1` thật của trang; ca 2 `expect.poll` chờ vòng ① tô đặc rồi mới đo; ca 3 đặt viewport 1440×900. → meeting-form-sections 6/6 xanh. Bản cũ lưu scratchpad meeting-form-sections.spec.ts.bak.

## meeting-host.api + seed nhu cầu (08/11, user "1")
- [x] `meeting-host.api`: tự dựng meeting `E2E-CHU-TRI` (người tạo = token API e2e_assign) thay E2E-SURVEY-SYSTEM dùng chung; payload gửi lại `has_assignee` từ detail (thiếu cờ ⇒ BE coi app cũ, bắt người thực hiện + hạn). → 4 xanh + 1 skip (DB không có NV nghỉ việc — điều kiện skip sẵn của spec).
- [x] Phát hiện: sửa seed (đọc TEST_EMAIL) làm `customer-demand-link.api` thấy 0 nhu cầu — API chỉ trả nhu cầu có chủ trì = người gọi (`listSelectableCustomerDemands`: COALESCE(owner_employee_id, host_employee_id) = auth()->id()). Gỡ: spec chạy seed với `E2E_OWNER_EMAIL` = email token API; `meeting-form-sections` thôi dùng E2E-DEMAND-EDITABLE, tự dựng `E2E-KHUON-FORM` (6/6 xanh). `customer-demand-link.api` cũng gửi `has_assignee`.
- [x] `customer-demand-link.api` ca 3 403: `ProspectiveProject::canEdit()` chỉ cho NGƯỜI TẠO sửa (6fdec08de 10/09), e2e_provision.php tạo E2E-ASSIGN-PRJ (588) với created_by = 1. Spec tạm đặt created_by = employee của token API ở beforeAll, trả lại ở afterAll (đã kiểm: về 1). → 11/11 xanh.
- E2E_EDITABLE_MEETING_ID trong e2e/.env nay không spec nào dùng.

### Checkpoint — 08/11/2026 (wrap up)
Vừa hoàn thành: biên bản "Ghi nhận nội dung meeting" + ô tick "Giao người xử lý" (BE + web + app), vẽ lại + code 2 màn mobile theo mockup 09'/10', hỏi "Hoàn thành luôn?" sau Lưu biên bản (web + app, về đúng màn nguồn); e2e meeting xanh hết (complete-after-minutes 6/6 mới · report-assignee.api 4/4 · participants 4/4 · target 4/4 · room-sync 7/7 · investment-survey 19/19 · form-sections 6/6 · host.api 4+1 skip · customer-demand-link.api 11/11); seed lại fixture e2e trên db_gop_6_11. Kiểm: PHPUnit 5/5, Playwright MCP, máy ảo tpeLocal.
Đang làm dở: — (CHƯA commit: hrm-api 10 file · hrm-client 5 · TPE_APP 4; e2e ngoài git)
Bước tiếp theo: user xem diff → commit/push (hrm-api + hrm-client gop_db, TPE_APP develop); tuỳ chọn chạy `customer-demand-link.spec.ts` (UI, dùng chung seed nhu cầu, chưa chạy); deploy: không migration, build app mới.
Blocked:

- 08/11: ĐÃ COMMIT + PUSH — hrm-api gop_db `87b8bc65d` + `643e0849f` · hrm-client gop_db `dda38e17a` · TPE_APP develop `59641ca` (origin khớp local, lệch 0/0).
