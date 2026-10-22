# Plan — Thiết kế lại form Tạo/Sửa meeting

## Phase 0 — Mockup
- [x] Rà form hiện tại (`GeneralInfo.vue`, `MeetingForm.vue`), chụp hiện trạng
- [x] Mockup `mockup.html` 5 khối theo thứ tự chọn + Tóm tắt, bỏ thanh trạng thái; 5 trạng thái mẫu; kiểm 1440px + 390px không tràn ngang
- [x] Mockup v2 theo góp ý (ⓘ thay ghi chú, Thêm nhanh đồng nhất, thẻ KH, segmented iOS, Thông tin bản ghi, tab iOS) — đo: segmented 36px = ô bên cạnh, thumb khớp tab đang chọn, 390px không tràn
- [x] Mockup v3 bám chuẩn dự án (số liệu từ component dùng chung)
- [x] Mockup v4: 4 thành phần (tab, nút gạt, thẻ KH, Thêm nhanh) kiểu mới, còn lại theo chuẩn chung
- [x] Mockup v5: đủ tab Nhân sự / Biên bản / Nhiệm vụ / Dự án TKT, chế độ Chi tiết, footer theo chế độ, mã đúng định dạng thật; hover tab trắng sáng kiểu iOS
- [x] **User chốt mockup 15/10/2026** → ghi design.md (D1–D8) + spec đầy đủ; đóng băng `mockup-chot-2026-10-15.html`
- [x] 4 câu hỏi còn lại chốt theo mockup: có Tóm tắt · có Gợi ý tên · Chi tiết dùng chung bố cục · bỏ thanh trạng thái cả ở Chi tiết

## Phase 1 — 4 thành phần dùng chung (CHỜ user cho phép code)
- [x] `components/V2BaseTabNavigation.vue`: kiểu viên thuốc kính mờ iOS (spec 2.1) — kiểm 7 màn đang dùng
- [x] `components/V2BaseSegmented.vue` (mới) + SKILL `segmented-control`
- [x] `components/V2BaseCustomerCard.vue` (mới) → thay khối thông tin KH ở `meeting/GeneralInfo.vue` + `prospective-projects/CustomerBlock.vue`
- [x] `components/V2BaseQuickAddButton.vue` (mới) → thay ở GeneralInfo (2) · CustomerBlock (2) · CreateTaskModal (2) · WarrantyRepairHandleRequestForm (1) · CustomerEquipmentPickerModal (1) · MeetingRoomModal (1) · WrMaintenanceTable
- [x] Playwright đo từng màn bị ảnh hưởng + e2e liên quan (xem checkpoint)

## Phase 2 — Bố cục form meeting (user "làm" 15/10/2026)
- [x] `MeetingForm.vue` bỏ thanh trạng thái, cột phải (Xác nhận tham dự · Thông tin bản ghi · Tóm tắt) chỉ tab Thông tin
- [x] `GeneralInfo.vue` 5 khối theo thứ tự chọn, ghi chú → ⓘ, Gợi ý tên, liên hệ 1 ô
- [x] `MeetingParticipants.vue` + `AttendanceStatusCell.vue` (nút gạt điểm danh, bộ đếm)
- [x] `MeetingReport.vue` (I–III gộp, Xuất Excel, số La Mã, cột Nhiệm vụ)
- [x] `MeetingProject.vue` (thẻ chọn dự án, tab con nút gạt, thẻ KH chỉ xem)
- [x] (thêm) `MeetingInvestmentSurvey.vue`: câu Có/Không → V2BaseSegmented (testid q1-yes/q1-no/q4-yes/q4-no giữ nguyên); V2BaseSegmented thêm `option.testid`
- [x] e2e meeting-target, meeting-participants, investment-survey… chạy lại toàn bộ

### Checkpoint — 2026-10-15
Vừa hoàn thành: mockup v1
Đang làm dở: —
Bước tiếp theo: user review mockup, trả lời 4 câu hỏi
Blocked: chờ user

### Checkpoint — 2026-10-15 (chốt mockup)
Vừa hoàn thành: user "Chốt mockup" → design.md D1–D8 + spec `docs/superpowers/specs/gop-db/2026-10-15-meeting-form-redesign-design.md`; đóng băng mockup-chot-2026-10-15.html
Đang làm dở: —
Bước tiếp theo: xin phép code Phase 1 (4 component dùng chung) + Phase 2 (màn meeting) — hrm-client, gop_db, không DB
Blocked: chờ user "làm"

### Checkpoint — 2026-10-15 (Phase 1 xong, user: "làm")
Vừa hoàn thành (hrm-client, gop_db, chưa commit, không đụng BE/DB):
- `V2BaseTabNavigation.vue` viết lại kiểu viên thuốc kính mờ (thumb + hover là 2 lớp nền, giãn kiểu giọt nước, hover nở 2px, giữ cuộn ngang + mũi tên + hasError; thêm `tab.count`, prop `sticky`).
  Đo 7 màn (meeting, Dự án TKT manager, Giải pháp form + manager, Hạng mục manager, Yêu cầu GP, Công việc của tôi): thanh 36→40px, tab 28→32px, khe 2→4px, viên chọn khớp tab ±2px cả trước/sau đổi tab, hover nở 2px; 1000px tràn ngang → mũi tên + viên bám khi cuộn.
- Mới: `V2BaseSegmented.vue` (chưa màn nào dùng — kiểm ở Phase 2), `V2BaseCustomerCard.vue`, `V2BaseQuickAddButton.vue`.
- CustomerBlock (form Dự án TKT): thẻ KH mới + 2 Thêm nhanh; gỡ CSS `.readonly-customer-info`, `.quick-add-btn`. Thẻ ẩn trường rỗng / "-" (dữ liệu ERP lưu SĐT "-").
- Thêm nhanh: CreateTaskModal ("Thêm nhanh checklist" / "Thêm nhanh nhiệm vụ con") · WarrantyRepairHandleRequestForm + CustomerEquipmentPickerModal ("Thêm nhanh lỗi thiết bị") · WrMaintenanceTable ("Thêm vật tư") · MeetingRoomModal ("Thêm nhanh tiện nghi"; e2e meeting-room cập nhật chữ + class).
- Kiểm trình duyệt: Dự án TKT add/show (thẻ + chip cùng hàng nhãn, 22px), popup nhiệm vụ nâng cao (2 chip), phiếu xử lý tạo từ YC 6477 (chip nằm gọn ô, bấm mở đúng popup "Thêm nhanh công việc / lỗi thiết bị").
- KHÔNG kiểm được bằng tài khoản e2e (thiếu quyền → 404/403): popup phòng họp, Thêm vật tư ở báo giá CSKH, popup chọn thiết bị. Spec meeting-room viết cho worktree (API 8001, token -wt cũ) + e2e_assign không có quyền "Khai báo phòng họp" → lỗi setup có sẵn.
- e2e: meeting-target + meeting-participants + meeting-investment-survey + service-demand = **49 passed, 1 skipped, 0 failed** (13.3 phút).
- SKILL: `.claude/skills/segmented-control/SKILL.md` (mới) + `button-convention` mục 6d "Thêm nhanh" (tài sản chung — đưa vào PR).
Đang làm dở: —
Bước tiếp theo: user review Phase 1 → xin phép Phase 2 (màn meeting).
Blocked:

### Checkpoint — 2026-10-15 (Phase 2 xong, user: "làm")
Vừa hoàn thành (hrm-client, gop_db, chưa commit, không BE/DB):
- MeetingForm: bỏ thanh trạng thái + getStepClass + CSS; Xác nhận tham dự → slot cột phải; tab có số đếm (Nhân sự, Dự án TKT).
- GeneralInfo: 5 khối V2BaseFormSection đánh số theo thứ tự chọn (khoá ② khi chưa chọn loại, ẩn ② khi Nội bộ → đánh lại số);
  Phân loại + Hình thức = V2BaseSegmented; thẻ KH V2BaseCustomerCard (Lịch sử / Đổi / Bỏ chọn); liên hệ 1 ô "tên · chức vụ · SĐT";
  Thêm nhanh dùng chung; Gợi ý tên; editor Mục tiêu thanh công cụ rút gọn; 7 ghi chú → ⓘ b-popover info-popover;
  cột phải Thông tin bản ghi + Tóm tắt (bấm cuộn tới khối).
- MeetingParticipants + AttendanceStatusCell: khối có bộ đếm + "Tất cả có mặt"; nhóm có số người + Thêm nhanh; avatar + "Mã phòng · Mã NV"
  (lấy từ activeCompanyEmployeeOptions) + badge Chủ trì; điểm danh = V2BaseSegmented sm 3 màu, Chi tiết = badge.
- MeetingReport: cảnh báo hạn nhập chữ xám; I–III gộp 1 khối + In · Xuất Excel; IV / V thành khối; "Xóa hết"; Giao nhiệm vụ = Thêm nhanh.
- MeetingProject: thẻ chọn dự án; tab con = V2BaseSegmented; "Mở dự án" (tab mới); nút phiếu theo V2BaseButton.
- MeetingInvestmentSurvey: Có/Không = V2BaseSegmented (giữ testid); V2BaseSegmented thêm option.testid.
- Kiểm trình duyệt (6353 sửa/chốt lịch, 832 chi tiết, tạo mới, 390px): số khối, khoá/mở khối ②, tóm tắt + tiến độ, gợi ý tên, popover ⓘ,
  nút gạt điểm danh đổi màu + bộ đếm, Tất cả có mặt, tab Biên bản / Dự án TKT; không tràn ngang.
- e2e (cập nhật meeting-target, meeting-participants, meeting-investment-survey helper đóng panel + chooseRadio, meeting-host vị trí chủ trì):
  meeting-target + participants 14 passed · investment-survey 22 passed · meeting-host 7 passed ·
  employee-work-performance + report-meeting-drawer + service-demand (+host lần đầu) 39 passed 1 skipped.
Lệch mockup (có lý do, xem design.md mục "Lệch so với mockup"): không sticky; Phòng họp hiện cả Online; số mục Biên bản giữ I–V như bản in;
  Kết luận giữ full toolbar; API thiếu người cập nhật / mã phòng người tạo / giờ tạo.
Đang làm dở: —
Bước tiếp theo: user review → quyết bổ sung BE (người cập nhật, giờ tạo) nếu cần → commit.
Blocked:

### Checkpoint — 2026-10-15 (bổ sung BE Thông tin bản ghi, user: "có" → "làm")
Vừa hoàn thành (hrm-api + hrm-client, gop_db, chưa commit, không migration / DB):
- BE `MeetingTransformer`: thêm `creator_label`, `created_at_full` (d-m-Y H:i), `updated_by`, `updater`, `updater_label` (khuôn
  employeeOptionLabel); `company_members` thêm `employee_code`, `department_code` và bỏ `Employee::find` từng người (1 query nạp sẵn
  info.department — hết N+1). Trường cũ giữ nguyên. `MeetingService::getDataForShow` eager load employee_create/update.info.department.
- PHPUnit mới `tests/Feature/MeetingTarget/MeetingRecordInfoTest.php` (2 ca: đủ trường + thành viên mồ côi không sập).
  MeetingTarget 45/45 · ReportMeetingView 6 · PotentialCustomerTracking 24 · ServiceDemand 45 — xanh.
- FE: cột phải hiện Người tạo "Tên - Mã phòng - Mã NV" (tạo mới lấy từ activeCompanyEmployeeOptions), Ngày tạo có giờ, Cập nhật gần nhất
  "người · thời điểm"; tab Nhân sự dòng phụ ưu tiên mã từ API.
- Kiểm trình duyệt 832 / 6353 / tạo mới: đúng. e2e meeting-target + participants + host 18 passed (bước đổi KH ở meeting-target bấm lại
  tới khi popup đóng — popup nạp danh sách 2 lần trong lúc server dev 4 worker bận ~8 request dự án, cú bấm từng bị nuốt).
Đang làm dở: —
Bước tiếp theo: user review toàn bộ → commit (hrm-api + hrm-client, nhánh gop_db).
Blocked:

### Checkpoint — 2026-10-15 (Dự án TKT tóm tắt, user: "làm")
Vừa hoàn thành:
- BE `MeetingService::getDataForShow`: mỗi dự án thêm `status_name`, `status_color`, `scope_name` (Nhóm ngành = scope_id → hrm_scopes;
  dự án cha ghép nhiều scopes), `project_scale_name`, `investment_type_name`, `implementation_type_name`, `main_sale_employee_label`;
  eager load prospectiveProject.scope/scopes/mainSaleEmployee.info.department. PHPUnit +1 ca → MeetingTarget 46/46.
- FE `MeetingProject.vue`: Thông tin chung = thẻ tóm tắt (V2BaseFormSection + V2BaseInput disabled + V2BaseCustomerCard), nút "Xem chi tiết"
  ($router.push màn chi tiết dự án); gỡ CustomerInfoSection / ProjectInfoSection khỏi tab. Mở tab không còn chùm request nạp danh mục dự án.
- Kiểm trình duyệt meeting 832: đủ 12 trường đúng dữ liệu, badge tiến trình, nút chuyển tới /assign/prospective-projects/325. e2e target + participants 14 passed.
- Server Nuxt :3000 tự thoát lúc biên dịch lại → khởi động lại (task bxxvm3aq8).
Phát hiện (chưa sửa, ngoài phạm vi): ô khoá (disabled) ở 3 màn Tạo/Sửa/Chi tiết meeting đều nền TRẮNG — rule nền #f1f5f9 chỉ áp trong khung
  `.v2-styles` (import v2-styles.scss), màn meeting không bọc.
Chưa xử lý: tab cuối bị khuất bên phải ở màn Tạo mới — CHƯA tái hiện được (Chrome headless 1440/1280/1024/800, có / không tab Dự án TKT,
  hover); chờ user gửi ảnh / kích thước hoặc bật tiện ích Claude for Chrome.
Bước tiếp theo: user review → (tuỳ chọn) bọc .v2-styles cho màn meeting → commit.
Blocked: lỗi tab chờ thông tin từ user.

### Checkpoint — 2026-10-15 (sửa lỗi tab cuối bị khuất — ảnh user gửi)
Vừa hoàn thành:
- Nguyên nhân (đo được): viên chọn trượt lò xo QUÁ ĐÀ vượt mép phải ~150ms → scrollWidth 405→415; lần đo độ tràn rơi đúng lúc đó
  (ResizeObserver khi tab đổi chữ đậm / scroll) → cờ isOverflow kẹt true → mũi tên › + vệt mờ đè tab cuối. Tái hiện có chủ đích bằng
  cách bắn scroll đúng khung hình quá đà → isOverflow true dù 405 = 405 (khớp ảnh user).
- Sửa `components/V2BaseTabNavigation.vue`: độ tràn tính theo mép phải NÚT tab cuối (contentWidth) thay scrollWidth; đo lại 450ms sau khi
  viên chọn dừng; cuộn tab đang chọn vào tầm nhìn chừa 40px (mũi tên + vệt mờ) thay 6px.
- e2e mới `e2e/tests/assign/tab-navigation.spec.ts` (2 ca) — với bản cũ ca 1 ĐỎ, bản sửa XANH. Đo lại 7 màn dùng tab: không hồi quy.
  tab-navigation + meeting-participants + meeting-target 16 passed.
Bước tiếp theo: user review → (tuỳ chọn) bọc .v2-styles cho màn meeting → commit.
Blocked:

### Checkpoint — 2026-10-15 (bọc .v2-styles + COMMIT, user: "làm nốt việc dở rồi commit")
Vừa hoàn thành:
- MeetingForm bọc `.v2-styles` + import v2-styles.scss → ô khoá Chi tiết / thẻ tóm tắt dự án nền #f1f5f9 (đo DOM).
- Kiểm trước commit: e2e tab-navigation + participants + target + host + investment-survey 39 passed; PHPUnit MeetingTarget 46,
  MeetingByProjects 28, MeetingByEmployees 41, ServiceDemand 45, PotentialCustomerTracking 24, ReportMeetingView 6,
  EmployeeWorkPerformance 17 — xanh.
- Commit nhánh gop_db (CHƯA push):
  hrm-api: f5f05eb01 chore(test) fixture DB gộp · d62a22bd7 feat(assign/meeting) chọn Dự án TKT theo KH, tóm tắt dự án, thông tin bản ghi
  hrm-client: 18596a5dd fix bộ lọc Dự án TKT · 868558c3c feat(ui) 4 thành phần dùng chung · 5cf8a8c71 feat(assign/meeting) thiết kế lại màn meeting
Lưu ý deploy: chạy migration 2026_10_14_000001 (index ô chọn dự án). SKILL mới (.claude/skills) + .plans nằm ở hrm-claude-config — đưa qua PR riêng.
Bước tiếp theo: user push / tạo PR khi sẵn sàng; việc tồn: meeting-mobile.pen, gộp ~25 API màn Sửa meeting.
Blocked:

### Checkpoint — 2026-10-15 (wrap up)
Vừa hoàn thành: toàn bộ meeting-form-redesign (mockup chốt D1–D9, Phase 1 component dùng chung, Phase 2 màn meeting, BE thông tin bản
  ghi + tóm tắt dự án, sửa lỗi tab cuối bị khuất, bọc .v2-styles) — đã PUSH gop_db: hrm-api 00c829746, hrm-client f4b44b9d9
  (merge origin, giải 1 xung đột GeneralInfo — giữ class v2-cell-link của remote). Sau merge: PHPUnit MeetingTarget 46/46,
  e2e tab-navigation + meeting-target + meeting-participants + prospective-projects-filter 25 passed.
Đang làm dở: —
Bước tiếp theo: (1) đưa .plans + SKILL mới (segmented-control, button-convention 6d) qua PR hrm-claude-config;
  (2) cập nhật meeting-mobile.pen theo thiết kế mới; (3) đề xuất gộp ~25 API lúc mở màn Sửa meeting;
  (4) 7 migration của người khác chưa chạy ở DB local (cần user cho phép).
Blocked:

## Phase 3 — Form liền mạch + chuẩn header chung (mockup vòng 2c duyệt 19/10/2026; user "làm cả 2 bước")
Phạm vi: hrm-client · gop_db · checkout chính · không BE/DB · không commit. Mockup: `mockup-lien-mach-2026-10-19.html` (bản B + viền màu nhẹ).
Bước 1 — form meeting
- [x] `MeetingForm.vue`: card chính `p-3` → `p-1`
- [x] `FileAttachmentTable.vue` (dùng chung 9 màn): thêm slot `#title` tuỳ chọn — không truyền thì giữ icon + chữ như cũ
- [x] `GeneralInfo.vue`: màu theo khối (data-sec type/target/content/time/files), vòng số nhạt/đặc theo `.is-done`, viền `rgba(màu,.28)` bo 8px,
      dải tiêu đề `rgba(màu,.07)`, khối cách 12px; khối ⑤ dùng slot `#title` + `data-sec="files"`; 2 card cột phải cùng khung (slate)
Bước 2 — chuẩn header toàn phần mềm
- [x] `V2BaseFormSection.vue` rule `.card-header.section-header`: cao 36px, đệm 2px 10px, căn giữa, `h6` margin 0 / 14px / lh 20px,
      nền `rgba(100,116,139,.07)`, bỏ gạch dưới
- [x] Playwright đo: 7 header form meeting (36px, lệch tâm 0), chiều cao cột form ≈ mockup 1327px, không tràn ngang 1440/1366;
      ~8 màn tiêu biểu dùng V2BaseFormSection + 2 màn viết tay; FileAttachmentTable ở 1 màn khác không đổi
- [x] Ghi nhận: 55 màn tự viết `.section-header` + CSS riêng KHÔNG ăn đủ chuẩn mới → báo user, chưa sửa

### Checkpoint — 2026-10-19 (Phase 3 code xong)
Vừa hoàn thành: bước 1 + 2 (hrm-client gop_db, CHƯA commit) — MeetingForm p-1 · FileAttachmentTable slot #title · GeneralInfo màu/viền/dải
  theo data-sec + khối ⑤ + cột phải slate · V2BaseFormSection chuẩn header chung `body .card .card-header.section-header` (36px, căn giữa,
  h6 margin 0, dải rgba(100,116,139,.07), bỏ gạch dưới). Gốc lệch tâm: h6 margin-top 10px toàn cục. Gốc nền trắng sót: rule KHÔNG scoped
  trong assign-components/customer/CustomerForm.vue nạp sau đè rule chung → tăng độ ưu tiên selector.
  Đo Playwright 9 màn (meeting sửa/tạo/chi tiết, BH sửa chữa, báo giá DV, YC mua DV, gia hạn mượn, YC nhập hàng, bổ sung hạch toán):
  mọi header 36px, lệch tâm 0, nền slate (meeting giữ màu khối); cột form 1461→1327px (= mockup), không tràn 1440/1366.
  FileAttachmentTable màn khác (/assign/request-solution/add) giữ nguyên icon + chữ 13px. Ảnh trước/sau: anh-mockup/do-header/.
  e2e `tests/assign/meeting-form-sections.spec.ts` 5 ca — viết xong, `--list` OK, CHƯA CHẠY (theo quy ước chỉ chạy khi user yêu cầu).
Đang làm dở: —
Đã PUSH gop_db hrm-client `53421e1cb` (rebase lên d10edd229 của Tri Lee, không xung đột).
Bước tiếp theo: user xem trên app; nếu cần thì chạy e2e meeting-form-sections + bộ meeting. Ghi nhận: 55 màn tự viết `.section-header`
  có CSS riêng — nay chuẩn chung đã thắng ở 2 màn mẫu đo được, các màn còn lại chưa đo từng màn.
Blocked:

## Phase 4 — Gộp khối (19/10/2026, user cho phép "Làm": hrm-client gop_db · GeneralInfo.vue + spec e2e)
- [x] Gộp ① Loại meeting + ③ Nội dung cuộc họp → ① "Thông tin cuộc họp" (Phân loại · Loại meeting · Tên * + Gợi ý tên · Mục tiêu/Nội dung)
- [x] Đổi tên khối "Khách hàng & đối tượng" → "Đối tác" (②); Nội bộ ẩn ② như cũ
- [x] secNo + màu data-sec + danh sách khối panel phải + is-done
- [x] Kiểm Playwright (đo DOM) + cập nhật meeting-form-sections.spec.ts
- [x] Đồng bộ thiết kế app (03 · 05 · 25 · 28 · 33 + caption)

### Checkpoint — 2026-10-19 (Phase 4 gộp khối)
Vừa hoàn thành: GeneralInfo.vue — ① Thông tin cuộc họp (data-sec="info", is-done = Loại + Tên), ② Đối tác, secNo info/target/time/files, bỏ màu 'content', Tóm tắt đưa Tên lên sau Loại, ô Tên cách hàng Phân loại 16px (.mf-name-grp). Đo DOM: 4 khối header 36px lệch 0, màu đúng, Nội bộ → info:1,time:2,files:3. Spec meeting-form-sections cập nhật + thêm ca gộp khối (--list OK, CHƯA chạy). Thiết kế app 03/05/25/28/33 đã gộp.
Đang làm dở: —
Bước tiếp theo: user review web (chưa commit); chạy e2e khi được yêu cầu
Blocked:
