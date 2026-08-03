# Plan — Dự án cha / dự án con (#10882)

## Phase 1 — Dự án cha - con

### BE

- [x] Migration `add_parent_project_fields_to_prospective_projects_table`: thêm `is_parent_project`, `discount_method`, `price_type_id` + index (không bọc transaction) — đã chạy
- [x] Kiểm tra dữ liệu `parent_id` rác từ mock cũ — DB sạch, 0 bản ghi, không cần xử lý
- [x] `ProspectiveProject`: thêm hằng số + mảng `PARENT_STATUS`, `getStatusListByType()`, `resolveStatusName()`
- [x] `ProspectiveProject`: thêm `generateParentProjectCode()` (`{phòng}.{năm}.DAC{seq}`)
- [x] `ProspectiveProject`: relation `parent()`/`children()`, accessor `project_type`/`allocated_budget`/`status_name`, `isParentSelectable()`, `canChangeProjectType()`
- [x] `ProspectiveProjectService`: nhánh sinh mã theo `is_parent_project` ở store + update
- [x] `ProspectiveProjectService::applyParentInheritance()` — ghi đè trường kế thừa từ cha xuống con
- [x] `ProspectiveProjectService::promoteParentToInProgress()` — cha `Đang tạo → Đang thực hiện` khi lưu con
- [x] Tách `doCloseProjectCascade()` khỏi `closeProject()` (bỏ check quyền ở phần cascade)
- [x] `ProspectiveProjectService::closeParentProject()` — đóng cha + cascade từng con
- [x] `ProspectiveProjectRequest`: rule riêng cho dự án cha (bỏ rule trường ẩn; lưu nháp chỉ cần `name`)
- [x] Khóa `is_parent_project`/`parent_id` khi status != 1 hoặc đã có con; khóa `customer_id` khi cha đã có con
- [x] Validate dự án con: cha hợp lệ & chưa đóng, timeline trong khung cha, ngân sách không vượt cha (lỗi inline từng field)
- [x] API `GET /prospective-projects/parent-options`
- [x] API `GET /prospective-projects/{id}/children`
- [x] API `POST /prospective-projects/{id}/close-parent`
- [x] Sửa `index`: filter `project_type`, chế độ tree chỉ trả dòng cấp 1 + `children_count`
- [x] Sửa `show`: trả `parent`, `allocated_budget`, `children_count`, `can_change_project_type`
- [x] `ProspectiveProjectResource` + `DetailProspectiveProjectResource`: thêm `is_parent_project`, `project_type`, `parent`, `allocated_budget`, `children_count`, `status_name` phân nhánh, `discount_method`, `price_type_id`
- [x] Rà chỗ BE render tên trạng thái: `MeetingByProjectsService` dùng `resolveStatusName()`; `ProspectiveProjectsReportService` loại dự án cha khỏi báo cáo (PO chốt)
- [x] Smoke test tinker 23 case: sinh mã, kế thừa, roll-up ngân sách, 4 case validate, đóng cascade — PASS hết

### FE

- [x] `RelatedSection.vue`: checkbox "Là dự án cha" + select "Dự án cha" nối API thật, 2 control loại trừ lẫn nhau
- [x] `add.vue` + `_id/index.vue`: xóa sạch mảng mock `parentProjects` và `loadMockData()`
- [x] Box preview dự án cha: mã, tên, trạng thái, KH, Sale chính, khung thời gian, tổng ngân sách, đã phân bổ, còn lại
- [x] Ẩn trường không thuộc URD khi là dự án cha (Ứng dụng, Phân loại đầu tư, Cách triển khai, Địa điểm, Giai đoạn, Mức ưu tiên, ngày GP, Nguồn vốn, kỳ vọng tài chính, `SolutionSection`)
- [x] `FinanceSection`: select Giảm giá (3 giá trị) + select Bảng giá (`price_type_id`) + ô Ngân sách đã phân bổ read-only
- [x] Read-only các trường kế thừa khi là dự án con, tự fill từ cha khi chọn cha
- [x] Khóa checkbox + select khi `can_change_project_type = false`, kèm dòng giải thích lý do
- [x] `_id/manager.vue`: nhánh `tabs()` cho dự án cha (3 tab: Thông tin chung / Dự án con / Meetings)
- [x] `TktTab.vue`: truyền cờ `isParentProject` xuống các section để tab Thông tin chung hiển thị đúng
- [x] Component mới `ProspectiveProjectChildrenTab.vue`: tóm tắt ngân sách + data grid dự án con + nút [+ Thêm dự án con]
- [x] `add.vue`: đọc query `parent_id`, chọn sẵn cha và khóa control chọn loại dự án
- [x] `CloseProjectModal.vue`: cảnh báo số dự án con bị đóng theo, gọi `close-parent` khi là dự án cha
- [x] `index.vue`: tree view — expand/collapse, lazy load + cache con, thụt lề, badge Cha/Con, reset cây khi đổi filter/trang
- [x] `index.vue`: filter "Loại dự án" (thêm vào `initialStateForm` → deep watcher tự search)
- [x] `index.vue`: cột Trạng thái ưu tiên `status_name` từ BE, bỏ map cứng enum FE
- [x] Compile check 12 file .vue (template + script) bằng vue-template-compiler trên Node 14.21.3 — sạch
- [x] Verify UI thực tế bằng Playwright (login namdangit, FE :3000 / BE :8000 từ thư mục HRM): form cha thu gọn đúng, tree view expand/collapse, filter Loại dự án, màn chi tiết cha 3 tab + tab Dự án con, form con kế thừa + khoá ô KH

### Rà soát lần 2 theo URD — bổ sung nốt (28/07)

- [x] `DetailProspectiveProjectResource`: trả `status_steps` (danh sách bước theo đúng enum của loại dự án) + metadata `created_at`/`updated_at`/`created_by_name`/`updated_by_name`
- [x] Component mới `ProspectiveProjectStatusBar.vue` — Thanh Tiến trình URD yêu cầu: 8 bước của dự án cha, bước đã qua tick xanh, bước hiện tại highlight xanh dương + phân vùng metadata
- [x] Nối status bar vào tab "Thông tin chung" của màn chi tiết dự án cha
- [x] **Sửa lỗi nhãn trạng thái sai**: `manager.vue` có bảng tên trạng thái hardcode → dự án cha status 7 hiện "Thương thảo giá" thay vì "Trình duyệt hợp đồng". Nay ưu tiên `status_name` từ BE
- [x] **Sửa format ngày**: 3 component mới dùng `this.$dayjs` (không tồn tại trong project) → ngày hiện dạng ISO thô. Đổi sang `import dayjs` đúng convention
- [x] Verify lại trên trình duyệt: 8 bước đúng tên, highlight đúng bước "Đang thực hiện", metadata hiện `28/07/2026 10:21`

### Bug phát hiện khi test (đã sửa)

- [x] **Dự án con không lưu được (422)** — BE đòi `customer_contact_name`/`customer_contact_phone` trong khi 2 trường này kế thừa từ cha và bị `applyParentInheritance()` ghi đè. Sửa: bỏ điều kiện required khi có `parent_id`. Smoke test tinker KHÔNG bắt được vì gọi thẳng Service, bỏ qua FormRequest.
- [x] **FE quên khoá ô chọn Khách hàng ở dự án con** — user đổi được KH rồi BE ghi đè khi lưu → mất dữ liệu thầm lặng. Sửa: dùng `lock-picker` sẵn có của `CustomerBlock` + thêm prop `lock-picker-placeholder`, nối vào add/edit/TktTab.
- [x] Bổ sung trường người liên hệ vào `parent-options` + `RelatedSection` để FE hiển thị đúng thông tin KH kế thừa.
- [x] Xác nhận `Loại hình/Lĩnh vực KH` dự án con vẫn tự chọn (form cha ẩn 2 trường này nên không có gì kế thừa).

### Checkpoint

### Checkpoint — 27/07/2026
Vừa hoàn thành: Đọc task #10882 + URD, chốt 21 điểm quyết định với PO, viết xong design.md + plan.md + spec chi tiết
Đang làm dở: chưa bắt đầu code
Bước tiếp theo: chờ duyệt tài liệu, sau đó chạy migration đầu tiên (BE task 1)
Blocked:

### Checkpoint — 28/07/2026
Vừa hoàn thành: Code + TEST xong toàn bộ Phase 1 BE + FE.
- Migration đã chạy trên DB local.
- E2E API qua HTTP thật: 34/34 PASS.
- Verify UI bằng Playwright: form cha thu gọn, tree view, filter, màn chi tiết 3 tab, form con kế thừa + khoá ô KH.
- Compile check 16 file .vue sạch (Node 14.21.3).
- 2 bug thật phát hiện trong lúc test đã sửa (xem mục "Bug phát hiện khi test").
- Dữ liệu test đã dọn sạch, DB về nguyên trạng (0 dự án cha, 0 dự án con).
Đang làm dở: không
Bước tiếp theo: user review code + merge. Khi deploy phải chạy `php artisan migrate`.
Blocked: không. (PO đã chốt loại dự án cha khỏi báo cáo dự án tiền khả thi — câu hỏi phát sinh lúc code.)

### Ghi nhận (không sửa ở phase này)
- Màn danh sách dự án: `filters` khởi tạo bằng `JSON.parse(JSON.stringify(initialStateForm))` → mọi khoá có giá trị `undefined` bị xoá, Vue 2 không theo dõi được nên deep watcher không tự chạy khi đổi các filter đó; phải bấm nút "Tìm kiếm". Lỗi SẴN CÓ, ảnh hưởng cả các filter cũ (đã kiểm chứng bằng `project_phase_id`), không phải regression của feature này.

---

## Phase 2 — Báo giá tổng

Spec chi tiết: `docs/superpowers/specs/2026-07-28-bao-gia-tong-design.md`

### BE

- [x] Migration 1: thêm `is_summary`, `name`, `parent_project_id` vào `quotations` + index
- [x] Migration 2: tạo bảng `quotation_total_sources` (unique summary+source)
- [x] Entity `QuotationTotalSource` + relation `sources()` / `summaryUsages()` trên `Quotation`
- [x] `Quotation`: hằng số + `getSummaryStatusList()` + `resolveStatusName()` phân nhánh theo `is_summary`
- [x] `Quotation::generateSummaryCode()` — `BGT-YYYY-XXXXX`
- [x] Service mới `SummaryQuotationService::create()` — validate quyền, hết hiệu lực bản cũ, tạo Section, copy dòng hàng
- [x] Quy tắc copy đơn giá bán cuối cùng theo 3 trường hợp giảm giá của nguồn; xoá sạch thông tin GG trên bản tổng
- [x] Copy cây nhóm hàng nhiều cấp + cộng dồn `shipping_cost` từ các nguồn
- [x] `syncFromSources()` (Làm mới dữ liệu) + `updateSources()` (tick thêm/bớt nguồn)
- [x] `submit()` / `approve()` / `reject()` — luồng 1 cấp, KHÔNG cascade dự án, KHÔNG đồng bộ ERP
- [x] `markWon()` / `cancel()` / `duplicate()` / `destroy()`
- [x] `SummaryQuotationRequest` — 8 rule validate chọn nguồn (cùng KH/MST/tiền tệ, đã duyệt, đúng dự án cha, tối thiểu 1, không trùng, mỗi dự án con tối đa 1 báo giá, **cùng loại GG**, **GG tổng phải trùng khớp bộ dòng giảm giá**)
- [x] Helper so khớp bộ dòng `quotation_discounts` giữa các nguồn (số dòng, discount_type_id, input_mode, giá trị) + trả về báo giá nào lệch
- [x] 16 API route + gắn `checkPermission` cho route duyệt/từ chối
- [x] Resource cho báo giá tổng + `usage_status` tính live cho báo giá con
- [x] **Rà loại `is_summary` khỏi luồng cũ**: hàng đợi duyệt giá, tab báo giá dự án con, `/assign/product-project`, report, đồng bộ ERP
- [x] Màn Quản lý báo giá: NGƯỢC LẠI — cho hiện báo giá tổng + filter "Loại báo giá" + badge; rà cột null (mã GP, phiên bản GP, mã YCBG) và nút thao tác từng dòng trỏ đúng luồng
- [x] Cascade đóng dự án cha → báo giá tổng chuyển Hết hiệu lực

### FE — luồng cốt lõi (đợt 2026-07-30)

- [x] Bật lại tab "Báo giá" cho dự án cha trong `manager.vue` (truyền thêm `:project` để biết KD phụ trách chính)
- [x] Component `ProspectiveProjectParentQuotationsTab.vue` — Khu vực 1 (báo giá từ dự án con + cột Trạng thái sử dụng)
- [x] Khu vực 2 — danh sách báo giá tổng (Tên/Mã, chip báo giá nguồn, tổng tiền, người tạo & ngày, trạng thái, thao tác Xem/Sửa/Xoá) + nút [Tạo báo giá tổng] chỉ hiện với KD phụ trách chính
- [x] `SummaryQuotationSourceModal.vue` — popup nhập tên + chọn nguồn NHÓM THEO DỰ ÁN CON dùng radio (mỗi dự án con 1 báo giá + lựa chọn "không đưa vào"), hiện mã BG/giá trị/ngày duyệt/người duyệt; dùng lại cho cả chế độ "chọn lại nguồn" ở màn sửa
- [x] Popup: sau khi tick báo giá đầu tiên → làm mờ + khoá các báo giá không tương thích (khác KH/MST/tiền tệ/loại GG/chữ ký chính sách GG) kèm lý do ngay tại dòng
- [x] Màn xem `summary-quotations/_id/index.vue` + sửa `edit.vue`
- [x] Phân vùng Thông tin chung (read-only vs sửa được theo URD) + phân vùng Điều khoản (chọn mẫu báo giá từ ERP) & Ghi chú nội bộ
- [x] Bảng chi tiết nhóm theo Section + nút "Xem nguồn"; duyệt cây nhóm hàng NHIỀU CẤP (Section → nhóm → nhóm con) vì dòng hàng nằm ở nhóm lá
- [x] Cột "Tỷ suất lợi nhuận" theo URD (ẩn cùng cột giá vốn khi user không có quyền "Xem giá vốn hàng hoá")
- [x] Bảng Tổng hợp giá trị theo nhóm chi phí (dùng `summary_breakdown` sẵn có của BE)
- [x] Bộ nút theo trạng thái + quyền (Sửa, Làm mới dữ liệu, Trình duyệt, Duyệt, Từ chối kèm modal lý do, Trúng thầu, Sao chép, Huỷ, Quay lại)
- [x] Banner cảnh báo khi có báo giá nguồn không còn hiệu lực
- [x] BE bổ sung: `ChildQuotationResource` trả "Đã gộp BG Tổng" (trước đây là TODO chờ Khu vực 2), controller nạp sẵn danh sách nguồn để tránh N+1

- [x] Bộ nút chuyển sang `V2Footer` như các màn khác (Sửa / In / Xoá / Huỷ / Lịch sử + slot custom-actions cho Trình duyệt, Trúng thầu, Làm mới dữ liệu, Sao chép, Xuất Excel); màn sửa dùng `V2Footer` menu `submit_form`
- [x] In: dùng lại `QuotationPrintConfigModal` + `QuotationPrintPreview`. Bản in dùng chung chỉ dựng được cây 2 cấp trong khi báo giá tổng sâu 3 cấp (Section → nhóm → nhóm con) → **làm phẳng dữ liệu truyền vào** (ghép tên theo đường dẫn "Hệ thống điện › Cụm Tủ Điện"), KHÔNG sửa component dùng chung
- [x] Xuất Excel: dùng lại endpoint `assign/quotations/{id}/export-quotation-data` (chung bảng quotations) — đã test trả file .xlsx 200
- [x] Lịch sử: dùng lại `QuotationHistoryModal` (`assign/quotations/{id}/histories`)

### FE — bổ sung cho ĐỦ theo URD (đợt 2026-07-30, sau rà soát lại tài liệu)

- [x] Cột **"Loại"** (Hàng hoá / Dịch vụ / Chi phí khác) ở bảng chi tiết — URD "Phân vùng Chi tiết báo giá" mục 2
- [x] **Thu gọn / mở rộng** từng Section (Action trên bảng chi tiết)
- [x] **Kéo-thả đổi thứ tự Section** ở màn sửa (Rule 3 + 4: chỉ kéo theo Section, không kéo dòng ra khỏi nhóm), lưu `sort_order` qua `PUT /sections`
- [x] **Rule 7** — khối "Giảm giá tổng đơn hàng": BE `SummaryQuotationController@show` trả `discount_summary` gộp GROUP BY loại GG của các nguồn (SUM thành tiền, bỏ cột %); FE hiện bảng read-only kèm ghi chú "đơn giá bán đã là giá sau giảm"
- [x] Cột **TSLN trước GG / sau GG** ở bảng Tổng hợp theo nhóm chi phí (ẩn cùng cột giá vốn theo quyền)
- [x] Popup cảnh báo **hàng hoá tạm trùng tên** khi Lưu nháp và Trình duyệt (liệt kê tên + số dòng, cho chọn "Vẫn lưu" / "Để tôi rà soát lại")

### FE — còn lại

- [ ] Màn Quản lý báo giá: thêm filter "Loại báo giá" + badge phân biệt báo giá tổng
- [ ] Khoá Giảm giá / Tiền tệ / Bảng giá ở màn báo giá của dự án con (kế thừa từ cha)
- [ ] **Tạo hợp đồng tổng + trạng thái "Đã tạo hợp đồng"** (URD mục "TẠO HỢP ĐỒNG") — CHẶN: HRM hiện không tự tạo HĐ ERP, chỉ deep-link sang ERP (`buildContractSummary`); cần API ERP tạo hợp đồng → Phase 3

### Verify

- [x] E2E API qua HTTP thật — **31/31 PASS** (tạo BGT, Section, snapshot dòng hàng, 3 rule validate, luồng duyệt 1 cấp, hết hiệu lực, khu vực 1, cách ly luồng cũ, đóng cha cascade)
- [x] Kiểm tra báo giá tổng KHÔNG lọt vào: tab báo giá dự án con, hàng hoá dự án; và CÓ hiện ở Quản lý báo giá theo filter
- [ ] Verify UI Playwright (sau khi làm xong FE)

### Bug phát hiện khi test BE (đã sửa)

- [x] `discount_percent` / `unit_price_after_discount` là NOT NULL default 0, truyền `null` gây SQL 1048 → đổi thành 0
- [x] Dùng sai API phân quyền: `$user->can()` không phải cơ chế của project → đổi sang `PermissionService::isCurrentEmployeeHasPermission()` như `QuotationService` đang dùng

### Đổi hàm dùng chung (PO đã duyệt)

- [x] `QuotationService::recomputeTotals()` và `calculateValidityDate()`: `private` → `public` để `SummaryQuotationService` dùng chung công thức. Chỉ đổi khoá truy cập, không đổi tham số/logic.

## Phase 3 — Hợp đồng tổng (chưa bắt đầu, phụ thuộc API ERP)

## Sửa lẻ

- [x] Bỏ ghi chú "Kế thừa từ dự án cha, không sửa được" + box preview thông tin dự án cha dưới ô "Chọn dự án cha"; thay bằng lấy đủ giá trị kế thừa qua form (BE `parentOptions` trả thêm SĐT/Email/Địa chỉ KH + toàn bộ khối KH thụ hưởng cuối, có che SĐT theo quyền; FE `RelatedSection` ghi theo danh sách `INHERITED_FIELDS` khớp `applyParentInheritance`)
- [x] Chọn dự án cha → fill luôn Sale chính / Phòng KD / Bộ phận của cha xuống form con
- [x] Vào `/add?parent_id={id}` cũng kế thừa (tách `applyParentInheritance()` + prop `auto-apply-parent-inheritance`)
- [x] Ẩn trường "Giảm giá" ở form dự án con (chỉ cha chọn; con vẫn kế thừa giá trị ngầm)
- [x] Bỏ các ghi chú hướng dẫn trong form cha-con (khoá đổi loại dự án, "Để trống nếu là dự án độc lập", "Tự động cộng dồn ngân sách..."); giữ cảnh báo cascade ở modal Đóng dự án
- [x] Màn chi tiết dự án cha (`/{id}/manager`): bỏ thanh bước trạng thái ở `ProspectiveProjectStatusBar`, giữ khối metadata
- [x] Gỡ hẳn `ProspectiveProjectStatusBar` (cả metadata) khỏi `manager.vue` + xoá file; bỏ `status_steps` khỏi `DetailProspectiveProjectResource`
- [x] Màn danh sách: tách badge Cha/Con/Độc lập + nút mở rộng cây ra cột riêng "Loại DA", không viết vào cột "Mã - Tên dự án TKT"; sửa merge `defaultTableColumns` để cột mới chèn đúng vị trí thay vì rơi xuống cuối
- [x] Làm lại UI phân cấp màn danh sách theo mẫu bảng báo cáo hiệu suất NV: thêm prop `rowClass` cho `V2BaseDataTable` (đã hỏi & được duyệt), tô nền dòng cha/con + viền trái, nút mở rộng tròn chuyển sang cột STT, badge dùng `V2BaseBadge`; sửa STT tính theo dòng gốc để mở dự án con không làm nhảy số
- [x] Chặn dự án cha làm giải pháp kỹ thuật theo URD: lọc `is_parent_project` khỏi dropdown `forRequestSolution` (`ProspectiveProjectService`), validate chặn ở `RequestSolutionRequest` (`project_key`) và `SolutionRequest` (`prospective_project_id`)
- [x] UX màn `/{id}/manager`: hết nháy tab (isParentProject/hasSolution/isSelfImplementation đọc từ `project` của asyncData thay vì `tktForm`), thêm skeleton + thanh loading Nuxt trong lúc `initializeData()`, watcher đưa về tab đầu khi tab đang mở không còn trong danh sách
- [x] Đồng bộ loading cho màn tạo/sửa dự án: tách component dùng chung `components/FormSkeleton.vue`; `edit.vue` skeleton + thanh loading Nuxt + try/catch/finally cho `getData()` (trước đây không bắt lỗi); `add.vue` chỉ chờ khi vào bằng `?parent_id=` (RelatedSection emit `parent-inheritance-done`); manager.vue dùng lại FormSkeleton
- [x] Làm đẹp tab "Danh sách dự án con": cột mã-tên dùng V2BaseTitleSubInfo, trạng thái dùng V2BaseBadge (bảng màu khớp cột Tiến trình màn danh sách), cột Thời gian 2 dòng, nút Thao tác theo kiểu icon-button 32x32 của màn /assign/project_phase

## Phase 2 — Tab Báo giá dự án cha (Khu vực 1: báo giá từ dự án con)

### BE
- [x] Route `GET /assign/prospective-projects/{projectId}/children-quotations`
- [x] `QuotationController@childrenQuotations`: gom báo giá của toàn bộ dự án con (is_summary=false), phân trang
- [x] `ChildQuotationResource`: bổ sung Dự án con, Người phụ trách (sale dự án con), Trạng thái sử dụng, Mã HĐ ERP

### FE
- [x] Thêm tab "Báo giá" vào danh sách tab của dự án cha (`manager.vue`)
- [x] Component `ProspectiveProjectParentQuotationsTab.vue` — bảng Khu vực 1 theo URD

### Checkpoint — 2026-07-29
Vừa hoàn thành: Khu vực 1 tab Báo giá dự án cha (BE + FE)
Đang làm dở: chưa có
Bước tiếp theo: Khu vực 2 — Báo giá tổng (cần bảng nguồn quotation_summary_sources, nút [Tạo báo giá tổng], Rule 9-14)
Blocked: cột `erp_firm_contract_code` chưa migrate ở DB local → cần chạy `php artisan migrate`
- [x] Thay checkbox "Là dự án cha" bằng select "Loại dự án" 3 lựa chọn theo URD (mặc định Dự án độc lập); ô chọn dự án cha chỉ hiện khi chọn "Dự án con"; gửi thêm `project_type` để BE validate `parent_id` required_if

## Sửa lẻ — đợt 2026-07-30 (màn tạo mới / cập nhật dự án TKT)

- [x] Fix select "Loại dự án": chọn Dự án cha → đổi sang Dự án con bị nhảy về Dự án độc lập (watcher `derivedProjectType` đè lựa chọn user khi `parent_id` còn rỗng)
- [x] Cảnh báo "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" khi rời màn tạo mới / cập nhật lúc form đã đổi (mixin dùng chung `utils/mixins/unsavedChangesMixin.js`, chặn cả điều hướng nội bộ lẫn đóng tab/F5). Chỉ tính là user sửa khi thay đổi xảy ra trong 500ms sau thao tác chuột/phím; thay đổi đến muộn hơn = auto-fill (currency_id, options Loại hình/Lĩnh vực...) thì dời mốc so sánh. 2 cách trước (chốt mốc bằng setTimeout, đóng băng mốc ở lần chạm đầu tiên) đều bị false positive → vào màn sửa rồi thoát luôn vẫn hiện popup
- [x] Ẩn dòng "Liên hệ" trong khối tóm tắt KH khi khách hàng là cá nhân (phần chọn Người liên hệ vốn đã ẩn)
- [x] Ẩn "Loại hình hoạt động KH" + "Lĩnh vực kinh doanh KH" ở form dự án cha (cả KH trực tiếp và KH thụ hưởng cuối) — BE vốn đã không validate 2 trường này khi `is_parent_project`
- [x] Cột "Tổng giá trị" tab Báo giá dự án cha: làm tròn về số nguyên (bỏ phần thập phân)
- [x] Chuyển "Loại dự án" + "Chọn dự án cha" từ phân vùng 6 lên ngay dưới "Tên dự án TKT" (phân vùng 2), 2 cột cạnh nhau; tách component `ProjectTypeBlock.vue`, `RelatedSection` chỉ còn phần meeting
- [x] Gộp Loại dự án / Ứng dụng / Quy mô / Phân loại đầu tư vào MỘT lưới `.row` (ProjectTypeBlock dùng `display:contents`) → dự án cha (ẩn Ứng dụng + Phân loại) tự kéo "Quy mô dự án" lên ngang hàng "Loại dự án"; dự án độc lập/con giữ nguyên bố cục cũ

### Checkpoint — 2026-07-30
Vừa hoàn thành: 6 fix màn tạo/sửa dự án TKT, đã verify bằng Playwright trên dev :3000
Đang làm dở: chưa có
Bước tiếp theo: chờ user review; cột "Tổng giá trị" mới verify được bằng gọi trực tiếp formatMoney (DB local chưa có báo giá dự án con nào)
Blocked:

### Checkpoint — 2026-07-30 (FE báo giá tổng, luồng cốt lõi)
Vừa hoàn thành: FE luồng cốt lõi báo giá tổng — Khu vực 2 ở tab Báo giá dự án cha, popup gộp nguồn, màn xem/sửa BGT, bộ nút trạng thái. Verify Playwright end-to-end trên dev :3000: tạo BGT-2026-00001 từ 2 báo giá con → sửa (đổi tên Section, giao hàng) → Trình duyệt → Duyệt; cột "Trạng thái sử dụng" của báo giá con chuyển "Đã gộp BG Tổng".
Đang làm dở: chưa có
Bước tiếp theo: phần FE còn lại (kéo-thả Section, In/Excel, filter màn Quản lý báo giá, khoá 3 trường ở báo giá dự án con)
Blocked:
Dữ liệu test đã tạo trên DB local: dự án cha #82 (SUMTEST.2026.DAC900), dự án con #83/#84, báo giá BG-TEST-901/902 (#198/#199), báo giá tổng #200 — xoá được nếu không cần.

### Checkpoint — 2026-07-30 (bổ sung cho đủ URD)
Vừa hoàn thành: 6 mục còn thiếu so với tài liệu (cột Loại, thu gọn/mở rộng Section, kéo-thả Section, Rule 7 bảng GG gộp, TSLN trước/sau GG, cảnh báo hàng tạm trùng tên). Verify Playwright: thu gọn Section (6→3 dòng), đổi thứ tự Section rồi Lưu → màn xem đổi đúng thứ tự, popup hàng tạm trùng tên liệt kê đúng tên gốc, bảng GG gộp 1tr + 2tr = 3tr theo loại.
Đang làm dở: chưa có
Bước tiếp theo: filter "Loại báo giá" ở màn Quản lý báo giá + khoá GG/tiền tệ/bảng giá ở báo giá dự án con. Mục "Tạo hợp đồng tổng" chờ API ERP.
Blocked: API ERP tạo hợp đồng (cho mục Tạo hợp đồng tổng)
Dữ liệu test bổ sung: đã thêm dòng giảm giá cho BG-TEST-901 (1tr) và BG-TEST-902 (2tr) để kiểm chứng Rule 7.

## Refactor UI 3 màn báo giá tổng (2026-07-30)

- [x] Tách **MỘT component UI dùng chung** `pages/assign/summary-quotations/components/SummaryQuotationForm.vue` cho cả 3 màn (tạo / sửa / xem) — khác nhau duy nhất ở prop `mode`: `view` render text, `edit`/`create` đổi ô sửa được thành input + bật khối kéo-thả Section
- [x] Màn **TẠO MỚI** riêng `pages/assign/summary-quotations/add.vue`: nút [Tạo báo giá tổng] ở tab dự án cha điều hướng sang màn này (KHÔNG lưu thẳng từ popup như trước); popup chỉ trả lựa chọn (`mode="select"`), user chỉnh tên/liên hệ/giao hàng/bảo hành/điều khoản/tên Section/thứ tự rồi mới bấm Lưu
- [x] BE `POST /assign/summary-quotations/preview` — dựng bản xem trước (Section + dòng hàng + đơn giá cuối cùng + GG gộp) bằng ĐÚNG công thức lúc lưu, không ghi DB; ẩn giá vốn theo quyền "Xem giá vốn hàng hoá"
- [x] BE `create()` nhận thêm header (người liên hệ, SĐT, email, địa chỉ, giao hàng, bảo hành, điều khoản, ghi chú) + `section_names` → lưu 1 lần, không phải gọi PUT bổ sung
- [x] Tách hằng số trạng thái báo giá tổng ra `pages/assign/summary-quotations/constants.js` (3 màn dùng chung, hết lặp)
- [x] Verify Playwright: tạo BGT-2026-00003 qua màn create (chọn nguồn → xem trước 478tr → sửa tên + tên Section → Lưu) → màn xem hiện đúng tên Section "Gói A - Khoa Cơ khí", bảng GG gộp, đủ 10 nút ở V2Footer

### Checkpoint — 2026-07-30 (refactor UI dùng chung)
Vừa hoàn thành: gom UI 3 màn báo giá tổng về 1 component, thêm màn tạo mới đúng luồng "chọn nguồn → xem trước → chỉnh → lưu".
Đang làm dở: chưa có
Bước tiếp theo: filter "Loại báo giá" ở màn Quản lý báo giá; khoá GG/tiền tệ/bảng giá ở báo giá dự án con; Tạo hợp đồng tổng (chờ API ERP)
Blocked: API ERP tạo hợp đồng

## Rà soát lại URD lần 2 (2026-07-30) — bổ sung 3 điểm lệch

- [x] **Rule 2** (URD "Rule tổng hợp"): "chỉ chọn báo giá đã duyệt **CHƯA tạo hợp đồng/phụ lục**" — trước đây mới check trạng thái. Bổ sung: `selectableQuotations` lọc `whereNull('erp_firm_contract_id')`, `loadAndValidateSources` chặn kèm thông báo "Báo giá X đã lập hợp đồng nên không tổng hợp được"
- [x] **Khu vực 1** (URD: "có các icon xem/sửa/xóa/tải excel, in báo giá/copy theo phân quyền"): bổ sung icon **Sửa** (chỉ báo giá Đang tạo của chính người tạo), **Tải Excel**, **Xoá**. In/Copy vẫn mở từ màn chi tiết báo giá con vì cần popup cấu hình in / preview copy
- [x] **Khu vực 2** (URD: Action gồm View / **Download** / Sửa / Xoá): bổ sung icon **Tải Excel**

### Điểm còn lệch tài liệu — cần PO chốt

- **Hiệu lực báo giá**: Rule 3 ("Đồng nhất dữ liệu Header") nói user được điều chỉnh; nhưng bảng "Thông tin chung" lại nói hệ thống tự tính `MIN(hạn ERP, ngày điều chỉnh giá)` và tính lại mỗi lần Lưu/Gửi/Duyệt. Hiện đang để **tự tính, read-only** theo bảng Thông tin chung.
- **Cột "Nhóm hàng cha / Nhóm hàng con"** (bảng Chi tiết mục 3, 4): đang render dạng **dòng tiêu đề nhóm** trong bảng (giống màn báo giá thường + ảnh mô phỏng của URD) thay vì 2 cột riêng.
- **Tạo hợp đồng tổng / trạng thái "Đã tạo hợp đồng"**: chờ API ERP (HRM hiện chỉ deep-link sang ERP, không tự tạo HĐ).

## Fix: chia Block A / Block B trong từng Section (2026-07-31)

Phát hiện khi user hỏi "sao không chia 2 group A — Hàng hoá / B — Dịch vụ như báo giá độc lập".
URD Rule 17 mục 3 yêu cầu: dòng dịch vụ phải nằm ở **Block B của đúng Section** sinh ra nó
("DV-THICONG 50tr ở Block B của Section A1, DV-THICONG 10tr ở Block B của Section A2"),
trong khi code đang gộp toàn bộ dịch vụ vào một khối chung cuối bảng.

- [x] Migration `2026_07_31_000001_add_quotation_group_id_to_quotation_service_items` — bảng `quotation_service_items` trước đây KHÔNG có cột nhóm nên không biết dòng dịch vụ thuộc nguồn nào (báo giá thường để NULL, không ảnh hưởng dữ liệu cũ)
- [x] `copyServiceItems()` nhận `sectionId` → gán `quotation_group_id`; `preview()` cũng gắn section cho dòng dịch vụ
- [x] `DetailQuotationResource::resolveServiceItems()` trả thêm `quotation_group_id`
- [x] FE component dùng chung: mỗi Section render **A — Hàng hoá** + **B — Dịch vụ & Chi phí khác** của chính Section đó; tổng Section = A + B; dịch vụ chưa gắn Section (dữ liệu cũ) vẫn hiện ở khối chung cuối bảng để không mất dòng
- [x] Verify: BG-TEST-901 có DV-THICONG 50tr, BG-TEST-902 có DV-THICONG 10tr → sau "Làm mới dữ liệu", Section Khoa Cơ khí tổng 260tr (210 hàng hoá + 50 dịch vụ), Section Khoa Điện tử 220tr (210 + 10) — đúng Rule 17 (miễn đối soát giá dịch vụ giữa các nguồn)

### Chốt với user (2026-07-31)
- Hiệu lực báo giá: giữ **tự tính, read-only**
- Nhóm hàng cha/con: giữ dạng **dòng tiêu đề nhóm**, không tách 2 cột
- Tạo hợp đồng tổng: chờ API ERP — OK
- In / Copy ở Khu vực 1: **chưa làm** (2/6 icon còn thiếu), chờ user quyết

## Fix UI popup chọn báo giá nguồn (2026-07-31)

User báo: chọn 1 báo giá → các báo giá không tương thích hiện lý do làm vỡ layout.
Nguyên nhân: dùng `b-form-radio` với nội dung nhiều dòng — `.custom-control` có min-height cố định nên
dòng lý do bị **đè lên** dòng thông tin; mã BG / giá trị / ngày duyệt cũng không thẳng cột.

- [x] Bỏ `b-form-radio`, dựng mỗi dòng bằng CSS grid `22px | 150px | 130px | 1fr | auto`: radio · mã BG · giá trị (căn phải, `tabular-nums`) · ngày duyệt + người duyệt · lý do
- [x] Lý do không gộp được đổi thành **chip cam sát phải cùng dòng** (kèm `title` để xem đủ khi bị cắt), không xuống dòng nữa
- [x] Dòng bị khoá: chữ xám + `cursor: not-allowed`, nền nhạt; dòng chọn được có hover; chiều cao dòng đều 36px
- [x] Verify: chọn BG-2026-00204 → 3 dòng còn lại mờ đúng, chip "Khác loại giảm giá" / "Chính sách giảm giá tổng không khớp" hiển thị gọn một dòng

- [x] Fix (2026-07-31): Báo giá tổng hiển thị sai định dạng số — `SummaryQuotationForm.formatMoney` dùng `Math.round + vi-VN` (mất số thập phân, khác dấu phân cách) → đổi sang cùng công thức báo giá con: tối đa 2 số lẻ, `Intl.NumberFormat en-US`. Áp cho cả 3 màn add/xem/sửa (dùng chung component).
- [x] Fix (2026-07-31b): Header bảng "Chi tiết báo giá" của báo giá tổng bám đúng báo giá con — "Giá nhập ({CUR})", "Giá bán ({CUR})" (thay "Đơn giá bán"), VAT(%) width 100px.

## Bổ sung Rule 6 URD — đồng nhất thuộc tính hàng hoá (2026-07-31)

User phát hiện BGT-205 (gộp BG-2026-00203 + BG-2026-00204) có mã `CH-MN-HB-XD0106:04`
giá bán cuối lệch nhau (52.13 vs 78.19) mà hệ thống vẫn cho gộp → đúng là Rule 6 chưa implement.

- [x] `SummaryQuotationService::assertConsistentProducts()` — gom dòng hàng của mọi nguồn theo `[Mã hàng + ĐVT]`,
      chỉ đối chiếu nhóm xuất hiện ở ≥2 báo giá; so 4 trường: **cấu trúc cha/con · giá bán niêm yết · VAT · giá bán cuối cùng**
- [x] Lỗi báo đích danh theo mẫu URD, có nêu rõ lệch trường nào và giữa 2 báo giá nào
- [x] Dịch vụ & chi phí khác nằm ở bảng `quotation_service_items` nên tự động được miễn (đúng Rule 17)
- [x] Verify: preview [203, 204] → 422 "Mã hàng CH-MN-HB-XD0106:04 … sai lệch về Giá bán cuối cùng giữa báo giá BG-2026-00203 và BG-2026-00204"; preview [203] → OK. Trên UI bấm "Xác nhận chọn" hiện đúng toast lỗi, không cho sang bước tiếp

Lưu ý: rule chỉ chặn khi TẠO / CHỌN LẠI NGUỒN. Các báo giá tổng đã tạo trước đó (vd BGT-205) vẫn giữ dữ liệu cũ.

## Lỗi validate hiện tại dòng thay vì toast (2026-07-31)

- [x] BE `fail()` nhận thêm `conflict_quotation_codes` → `ValidationException` trả kèm mã báo giá liên quan; gắn cho tất cả rule (không thuộc dự án cha, chưa duyệt, đã lập hợp đồng, khác KH/MST/tiền tệ, khác loại GG, khác chính sách GG tổng, Rule 6 lệch hàng hoá)
- [x] Popup chọn nguồn: thêm `serverErrors` + `setServerErrors()`; lỗi hiện **ngay dưới đúng dòng báo giá** (chữ đỏ, xuống dòng tự nhiên nhờ `grid-column: 2 / -1`); lỗi không khớp báo giá nào → banner đỏ cuối danh sách; đổi lựa chọn thì xoá lỗi cũ
- [x] Chế độ `select` (màn tạo): popup KHÔNG tự đóng khi bấm "Xác nhận chọn" — trang gọi preview, thành công mới đóng, lỗi thì giữ popup để user thấy lỗi tại dòng và sửa lựa chọn ngay
- [x] Chế độ `update` (màn sửa): lỗi cũng hiện tại dòng thay vì toast
- [x] Verify: chọn BG-2026-00203 + BG-2026-00204 → popup vẫn mở, lỗi Rule 6 hiện dưới CẢ HAI dòng, không còn toast

## Rà tài liệu lần 3 (2026-07-31) — 2 fix + tồn đọng

- [x] **Dự án con: hiện trường "Giảm giá"** (URD bảng dự án con mục 7 — "Kế thừa từ cha, không sửa").
      Trước đây đợt "sửa lẻ" đã ẩn hẳn trường này ở dự án con → SAI tài liệu. Nay hiện lại, disabled khi là dự án con
      (cùng cách với Loại tiền tệ / Bảng giá). Verify: màn sửa dự án con #83 hiện đủ Loại tiền tệ · **Giảm giá** · Bảng giá, tất cả disabled
- [x] **Khoá cứng Khách hàng khi dự án cha ĐÃ CÓ dự án con** (URD "Cập nhật Dự án Cha") — trước chưa làm.
      `edit.vue` khoá picker KH (cả KH trực tiếp lẫn KH thụ hưởng cuối) khi `is_parent_project && children_count > 0`,
      kèm câu giải thích trong ô. Verify: màn sửa dự án cha #82 hiện "Dự án cha đã có dự án con — không đổi được khách hàng"

### Tồn đọng so với tài liệu (chưa làm)

1. **Khoá Giảm giá / Tiền tệ / Bảng giá ở màn BÁO GIÁ của dự án con** (Rule 1.1, 1.2 nhóm "Ràng buộc kế thừa từ dự án cha")
2. **Toàn bộ cơ chế "Báo giá Mỏ neo"** — mục "UI/UX: LUỒNG TẠO BÁO GIÁ CON TRONG DỰ ÁN CHA" + "BỘ QUY TẮC: QUẢN LÝ TÍNH ĐỒNG NHẤT BÁO GIÁ CON":
   - Truy vấn báo giá "Đã duyệt" đầu tiên của dự án cha làm Mỏ neo
   - Điểm chạm 1: tạo báo giá con mới → tự sinh các dòng Giảm giá tổng giống Mỏ neo + banner thông báo
   - Điểm chạm 2: khi Lưu → cảnh báo mềm (toast cam + tô nền dòng lệch)
   - Điểm chạm 3: khi Trình duyệt → popup lỗi liệt kê từng dòng sai lệch, chặn gửi
   - Điểm chạm 4: khi Duyệt → badge xanh xác nhận đã đồng bộ 100% với Mỏ neo
3. **Khoá cứng Tổng ngân sách dự kiến từ bước "7 - Trình duyệt hợp đồng"** — phụ thuộc trạng thái sinh từ API ERP (Phase 3)
4. **In / Copy ở Khu vực 1** (2/6 icon)
5. **Tạo hợp đồng tổng** — chờ API ERP
6. Màn Quản lý báo giá: filter "Loại báo giá" + badge

## Khoá Giảm giá / Tiền tệ / Bảng giá ở màn BÁO GIÁ của dự án con (2026-07-31)

URD "BỘ QUY TẮC: QUẢN LÝ TÍNH ĐỒNG NHẤT BÁO GIÁ CON" — Rule 1.1 (khoá Tiền tệ) + Rule 1.2 (khoá Phương thức giảm giá);
bảng dự án con mục 7 bổ sung Bảng giá. Trước đó: màn báo giá vẫn cho chọn tự do, BE lấy thẳng giá trị client gửi.

- [x] BE `QuotationService::store()` — báo giá thuộc dự án con (project.parent_id ≠ null) thì `currency_id`, `price_type_id`,
      `discount_method` **ép theo dự án** (dự án con đã kế thừa từ cha), bỏ qua giá trị client gửi lên
- [x] BE `QuotationService::update()` — chặn đổi `discount_method` với báo giá của dự án con (giữ theo dự án)
- [x] BE `DetailQuotationResource` — trả `project.parent_id` + cờ `inherits_from_parent_project` cho FE
- [x] FE màn báo giá: khoá select Giảm giá (kèm icon ổ khoá + tooltip), Loại tiền tệ, Bảng giá; hiện dòng "Kế thừa từ dự án cha, không sửa được"
- [x] Verify API: báo giá 198 (dự án con 83) → `inherits_from_parent_project = true`, `project.parent_id = 82`; báo giá 143 (dự án độc lập) → false

### BOM list của dự án con — chưa xử lý (ngoài phạm vi tài liệu)

- `bom_lists` chỉ có `currency_id` (KHÔNG có `discount_method` / `price_type_id`) → BOM không dính giảm giá & bảng giá
- Màn BOM vẫn cho đổi tiền tệ tự do kể cả khi BOM gắn dự án con → BOM có thể lệch tiền tệ so với dự án cha
- Báo giá tạo từ BOM đó KHÔNG bị ảnh hưởng (đã ép currency theo dự án), nhưng BOM và báo giá lệch tiền tệ dễ gây nhầm khi đối chiếu giá vốn
- URD không đề cập BOM → đề xuất khoá `currency_id` của BOM theo dự án cha khi BOM gắn dự án con; **chờ PO/user chốt**

### Bổ sung: báo giá dự án con LẤY giá trị theo dự án, không dùng giá trị cũ trên báo giá

Verify UI phát hiện: ô Giảm giá đã disabled nhưng vẫn hiển thị giá trị cũ lưu trên báo giá
(báo giá `discount_method = null` trong khi dự án con = 2 "GG tổng").

- [x] `DetailQuotationResource` trả thêm `project.discount_method / currency_id / price_type_id`
- [x] FE dùng computed `inheritedDiscountMethod / inheritedCurrencyId / inheritedPriceTypeId`:
      dự án con → lấy theo DỰ ÁN; dự án độc lập → giữ giá trị đã lưu trên báo giá (luồng cũ không đổi)
- [x] Verify UI báo giá 206 (dự án con 83, dự án đặt GG tổng): ô Giảm giá hiển thị **"GG tổng"**, disabled, có icon khoá;
      bảng chi tiết hiện đúng cột phân bổ GG của phương thức "theo tổng"

### Màn TẠO báo giá (/assign/quotations/create) — chọn dự án con thì ép + khoá ngay

Màn create dùng chung `_id/edit.vue` (extends) nên lúc tạo chưa có `item` từ BE → cờ `inherits_from_parent_project`
chưa tồn tại, 3 trường vẫn cho chọn tự do. Đã sửa ở `selectProject()`:

- [x] Khi chọn dự án: lưu `project.parent_id / discount_method / currency_id / price_type_id` vào `item`
      và bật cờ `inherits_from_parent_project` ngay tại FE
- [x] Dự án con → set luôn Giảm giá / Tiền tệ / Bảng giá theo dự án rồi khoá 3 ô
- [x] Verify UI trên `/assign/quotations/create`: chọn "SUMTEST.2026.DA901 — [TEST BGT] Khoa Cơ khí" (dự án con, dự án đặt GG tổng)
      → ô Giảm giá tự nhảy sang **"GG tổng"**, disabled, có icon khoá, 2 dòng "Kế thừa từ dự án cha, không sửa được" (Tiền tệ + Bảng giá)

### Phân vùng "Thanh toán & Ghi chú nội bộ" của báo giá tổng — dùng chung UI với báo giá thường (2026-07-31)

- [x] Thay `V2BaseTextarea` bằng **`CompactReviewEditor`** (rich text như màn báo giá thường) cho cả
      "Điều khoản báo giá" (height 180) và "Ghi chú nội bộ (chỉ nội bộ)" (height 140); dropdown mẫu điều khoản
      đặt phía trên editor, cùng bố cục màn báo giá
- [x] Đổi cột ghi chú nội bộ từ `sales_note` → **`note`** cho khớp báo giá thường
      (`sales_note` ở báo giá thường là "ghi chú của sale" sửa ở màn xem qua endpoint riêng, không phải ô này)
- [x] Màn xem: điều khoản + ghi chú render `v-html` (nội dung rich text)
- [x] Bỏ 2 dòng chú thích "Kế thừa từ dự án cha, không sửa được" ở màn báo giá theo yêu cầu user (giữ icon khoá + tooltip)
- [x] Verify UI trên BGT-2026-00004 (Đang tạo): 2 trình soạn thảo + 2 thanh công cụ hiển thị đúng

- [x] Thông tin chung báo giá tổng: tách **Loại tiền tệ** và **Bảng giá** thành 2 hàng riêng (trước đây Bảng giá nằm chung ô với Tiền tệ),
      bố cục khớp màn báo giá thường; "Người phê duyệt" chuyển xuống hàng riêng colspan

## Phase 3 — Hợp đồng tổng: LÀM ĐƯỢC theo kiến trúc sẵn có (2026-07-31, phương án A user chốt)

**Phát hiện khi đọc source ERP (`HRM/TanPhatDev`):** luồng hợp đồng NGƯỢC với mô tả URD.
URD viết "HRM gửi API sang ERP tạo hợp đồng", nhưng thực tế người dùng lập HĐ **bên ERP**
(`HrmQuotationContractController` + `HrmApiService`), ERP gọi ngược 3 endpoint của HRM:
`GET erp-contract/eligible`, `GET erp-contract/{id}`, `POST erp-contract/{id}/mark`.
→ Không cần sửa repo ERP, chỉ cần cho báo giá tổng đi vào đúng cơ chế đó.

- [x] `Quotation`: thêm `SUMMARY_STATUS_DA_TAO_HOP_DONG = 9` ("Đã tạo hợp đồng", URD trạng thái mục 5) + đưa vào `SUMMARY_ACTIVE_STATUSES`
- [x] `erpEligibleQuery()`: báo giá tổng được phép lập HĐ dù có dòng cha-con (ngoại lệ có chú thích) — trước đây bị loại thẳng
- [x] `erpContractData()`: báo giá tổng chỉ đẩy **dòng cấp 1** sang ERP (dòng con là chi tiết cấu thành, thành tiền = 0)
- [x] `erpMarkContract()`: khi là báo giá tổng → ghi mã HĐ, chuyển trạng thái **Đã tạo hợp đồng**,
      **khoá toàn bộ báo giá con nguồn** (Action 3 của URD — không lập HĐ nhánh nữa),
      đẩy dự án cha sang **"Trình duyệt hợp đồng"** (PARENT_STATUS 7); tất cả trong 1 transaction
- [x] `SummaryQuotationController@show` trả `erp_firm_contract_id/code`; FE hiện dòng "Hợp đồng ERP" trong Thông tin chung
- [x] FE: đã lập HĐ thì không Sao chép/Huỷ/Sửa được nữa, chỉ còn In / Lịch sử / Xuất Excel / Quay lại
- [x] Chạy migration còn tồn `2026_07_23_000001_add_erp_firm_contract_code_to_quotations_table` (blocked từ đợt trước)

### Verify end-to-end (API thật + UI)
1. `GET erp-contract/eligible` → có **BGT-2026-00004** trong danh sách ERP lập HĐ
2. `GET erp-contract/205` → trả 2 nhóm, 4 dòng, **không có dòng con nào lọt sang**
3. `POST erp-contract/205/mark` → `{"success":true}`; HRM: BGT sang **Đã tạo hợp đồng**, mã HĐ `HD-TEST-001`;
   2 báo giá nguồn BG-2026-00203/00204 **bị khoá** (gắn cùng mã HĐ); dự án cha #82 sang **status 7**
4. Gọi lại `eligible` → BGT không còn trong danh sách (chống lập trùng)
5. UI màn BGT: badge **Đã tạo hợp đồng**, dòng "Hợp đồng ERP: HD-TEST-001", footer chỉ còn In/Lịch sử/Xuất Excel/Quay lại

### 3 điểm hành vi lệch URD đã sửa
- [x] Lưu nháp dự án: ở lại form (chuyển sang màn sửa bản vừa tạo, tránh tạo trùng), toast "Đã lưu nháp thành công"
- [x] Lưu chính thức: chuyển sang **màn chi tiết dự án** vừa tạo (trước đây về danh sách)
- [x] Nút [Đóng dự án] của dự án cha: chỉ hiện khi trạng thái **"Đang thực hiện"**

Dữ liệu test: BGT-2026-00004 (id 205) đã bị gán HĐ giả `HD-TEST-001` + currency tạm đổi sang VND để chạy thử —
cần xoá/khôi phục khi không dùng nữa.

## Khu vực 1: bổ sung nốt icon In + Sao chép (2026-07-31)

URD Khu vực 1 yêu cầu 6 icon "xem/sửa/xóa/tải excel, in báo giá/copy". Trước đó mới có 4.

- [x] **In báo giá**: nạp chi tiết báo giá con rồi mở đúng `QuotationPrintConfigModal` + `QuotationPrintPreview` của màn báo giá
- [x] **Sao chép**: dùng lại `QuotationCopyMixin` (mixin dùng chung với màn Quản lý báo giá + tab báo giá dự án con),
      tự đăng ký `QuotationCopyPreviewModal`, gate hiển thị theo `canCopyQuotation()` của mixin
- [x] Verify: dòng BG-TEST-901 hiện đủ icon; bấm In → popup "Cấu hình in báo giá" → Xem trước ra đúng mã BG-TEST-901 + dòng hàng thật

→ Khu vực 1 giờ đủ 6 icon theo URD (xem / sửa / tải Excel / in / sao chép / xoá — hiện theo phân quyền từng dòng).

## Cơ chế BÁO GIÁ MỎ NEO — 4 điểm chạm (2026-07-31)

URD "LUỒNG TẠO BÁO GIÁ CON TRONG DỰ ÁN CHA" + "BỘ QUY TẮC: QUẢN LÝ TÍNH ĐỒNG NHẤT BÁO GIÁ CON" (Nhóm 2, 3, 4).

### BE
- [x] Service mới `QuotationAnchorService`:
      - `findAnchor()` — báo giá con ĐẦU TIÊN của dự án cha đã duyệt (sort theo `COALESCE(approved_at, created_at)`)
      - `check()` — đối chiếu **cấu trúc dòng Giảm giá tổng** (Rule 2.2: thiếu/thừa loại GG) và **hàng hoá cùng [Mã + ĐVT]**
        (Rule 3.2: cấu trúc cha/con · giá niêm yết · VAT · giá bán cuối)
      - `seedDiscountLinesFromAnchor()` — Điểm chạm 1: báo giá con mới tạo tự sinh đúng bộ Loại giảm giá của Mỏ neo
        (chỉ copy CẤU TRÚC, giá trị để 0 cho Sale tự nhập theo quy mô báo giá của mình)
- [x] API `GET /assign/quotations/{id}/anchor-check`
- [x] `QuotationService::submit()` gọi `assertMatchesAnchorQuotation()` — chặn Trình duyệt kèm danh sách lỗi (Rule 4.1)
- [x] `store()` gọi seed dòng giảm giá theo Mỏ neo

### FE
- [x] **Điểm chạm 1** — banner ghim ở màn báo giá: xanh khi đã đồng bộ, cam + link "Xem chi tiết" khi lệch
- [x] **Điểm chạm 2** — Lưu nháp: vẫn lưu, hiện toast cảnh báo mềm + **tô nền cam các dòng hàng lệch** (kèm tooltip lý do)
- [x] **Điểm chạm 3** — Gửi duyệt: chặn, mở popup "Không thể trình duyệt — vi phạm quy tắc đồng bộ" liệt kê từng lỗi
- [x] **Điểm chạm 4** — màn xem báo giá: badge xanh "đã đồng bộ 100% với Báo giá Mỏ neo … Đủ tiêu chuẩn gộp Báo giá tổng",
      hoặc badge cam liệt kê điểm lệch để người duyệt biết

### Verify (báo giá 206 thuộc dự án con 83, Mỏ neo = BG-TEST-901)
- `anchor-check` → `has_anchor: true`, `is_synced: false`, 3 product_issues
- Màn sửa: banner cam "lệch 3 điểm so với Báo giá Mỏ neo BG-TEST-901", **3 dòng hàng bị tô nền**
- Bấm "Xem chi tiết" → popup liệt kê đúng 3 lỗi theo mẫu thông báo của URD
- Gọi thẳng API `POST /submit` → **422** kèm message "KHÔNG THỂ TRÌNH DUYỆT — … Mỏ neo BG-TEST-901" + 3 dòng lỗi
- Màn xem: badge cam liệt kê 3 điểm lệch

→ Toàn bộ URD đã hiện thực hoá, trừ: filter "Loại báo giá" ở màn Quản lý báo giá (thuộc spec nội bộ, không có trong URD)
  và các trạng thái dự án cha 8→10 (phụ thuộc trigger từ ERP).

## Rà tài liệu lần cuối (2026-07-31) — mục cuối cùng làm được

- [x] **Khoá cứng Tổng ngân sách dự kiến từ bước "7 - Trình duyệt hợp đồng"** (URD "Cập nhật Dự án Cha").
      Trước đây không làm được vì chưa có cách đạt trạng thái 7; nay luồng hợp đồng đã đẩy dự án cha sang 7 nên làm được.
      FE khoá ô + ghi chú; BE `ProspectiveProjectService::update()` chặn nếu giá trị đổi (không lách được qua API).
      Verify: dự án cha #82 (đang ở bước 7 sau khi lập HĐ) → ô Tổng ngân sách disabled + hiện ghi chú.

### Còn lại so với tài liệu — đều phụ thuộc bên ngoài

1. **Trạng thái dự án cha 8, 9, 10** (Thương thảo DA/HĐ · HĐ đủ điều kiện thực hiện · Nghiệm thu & Thanh lý):
   URD ghi rõ trigger là "API check với ERP" theo trạng thái hợp đồng / ủy nhiệm chi / quyết toán.
   HRM hiện KHÔNG có kênh nhận tín hiệu này — ERP mới chỉ gọi sang HRM lúc lập hợp đồng (`erp-contract/*`).
   Cần ERP bổ sung webhook/endpoint báo đổi trạng thái hợp đồng thì HRM mới cập nhật được.
2. **"Xuất PDF" riêng** cho báo giá tổng: hiện dùng nút In → trình duyệt "Lưu thành PDF" (quyết định #14 của spec,
   hệ thống chưa có xuất PDF kể cả ở báo giá thường).
3. (Ngoài URD — spec nội bộ) Filter "Loại báo giá" + badge ở màn Quản lý báo giá.

## Màn Quản lý báo giá: filter "Loại báo giá" + badge + FIX LINK (2026-07-31)

- [x] **FIX lỗi user báo**: dòng báo giá tổng ở màn Quản lý báo giá đang trỏ link của báo giá thường
      (`/assign/quotations/{id}`) → sửa `quotationDetailLink()` / `quotationEditLink()`: `is_summary`
      thì sang `/assign/summary-quotations/{id}` và `/edit` tương ứng
- [x] Cột "Loại" hiện badge xanh **"Báo giá tổng"** để phân biệt (dùng chung bảng quotations)
- [x] Thêm ô lọc **"Loại báo giá"** (Tất cả / Báo giá thường / Báo giá tổng) — BE đã có sẵn filter `quotation_type`
- [x] Verify: link dòng BGT-2026-00004 → `/assign/summary-quotations/205`; chọn lọc "Báo giá tổng" → còn đúng 4 dòng BGT

### Trả lời câu hỏi của user về trạng thái hợp đồng ở DỰ ÁN ĐỘC LẬP
Kiểm tra code: dự án thường chỉ tự lên **8 - Thương thảo DA/Hợp đồng** khi bấm **Chốt giải pháp**
(`ProspectiveProjectService::finalizeSolution()`). Hai trạng thái **9 - Thực hiện hợp đồng** và
**10 - Nghiệm thu & Thanh lý** KHÔNG có bất kỳ chỗ nào set — chỉ dùng để hiển thị/lọc/report.
→ Việc dự án CHA chưa có 8/9/10 là **đồng nhất với hiện trạng dự án thường**, không phải thiếu sót riêng của feature này.

### Chốt với user
- Xuất PDF riêng: **bỏ** (dùng In → lưu PDF của trình duyệt)

## Kiểm thử toàn diện lần cuối (2026-07-31)

Bộ dữ liệu test sạch: dự án cha #88 (RT.2026.DACX) + 3 con #89/#90/#91, báo giá RT-BG-001→005 (#207-#211).

### Backend — bộ quy tắc tổng hợp
- [x] Chặn khi không chọn nguồn nào
- [x] Rule 5 — khác phương thức giảm giá → chặn, nêu đúng mã báo giá lệch
- [x] Rule 6 — cùng [Mã hàng + ĐVT] lệch giá bán cuối → chặn, nêu đúng cặp báo giá xung đột
- [x] Rule 8 — mỗi dự án con chỉ một báo giá → chặn
- [x] Rule 2 — nguồn đã lập hợp đồng → chặn không cho tổng hợp lại
- [x] Tổ hợp hợp lệ → preview + tạo thành công

### Backend — nội dung & vòng đời báo giá tổng
- [x] Section = tên do người dùng đặt, đúng thứ tự, truy vết đúng báo giá nguồn
- [x] Gộp đủ dòng hàng của mọi nguồn; giá trị khớp tay (420tr hàng + 42tr VAT + 16tr vận chuyển = 478tr)
- [x] Vận chuyển cộng dồn từ các nguồn; bảng giảm giá tổng gộp đúng (1tr + 1tr = 2tr)
- [x] Gửi duyệt → Phê duyệt → Trúng thầu → khoá sửa
- [x] Đồng bộ lại khi nguồn đổi giá: chặn nếu nguồn lệch nhau, cập nhật đúng khi hợp lệ (478tr → 588tr)

### Backend — hợp đồng tổng (ERP)
- [x] `eligible` liệt kê đúng báo giá tổng trúng thầu
- [x] `erp-contract/{id}` chỉ trả dòng cấp 1 kèm cây Section
- [x] `mark` → báo giá tổng sang "Đã tạo hợp đồng", ghi mã HĐ xuống cả báo giá nguồn, dự án cha lên bước 7
- [x] Sau khi lập HĐ: biến mất khỏi `eligible`, nguồn bị chặn tổng hợp lại

### Backend — báo giá con & Mỏ neo
- [x] Tạo báo giá cho dự án con: BE ép loại giảm giá / tiền tệ / bảng giá theo dự án dù FE gửi giá trị khác
- [x] Tự sinh cấu trúc dòng giảm giá từ Báo giá Mỏ neo (giá trị 0 để Sale nhập)
- [x] `anchor-check` phát hiện đúng dòng lệch; Gửi duyệt bị chặn kèm danh sách sai lệch

### Frontend
- [x] Màn xem: đủ nút trong V2Footer (Sửa/In/Xóa/Hủy/Lịch sử/Trình duyệt/Làm mới/Sao chép/Excel/Quay lại)
- [x] Bảng chi tiết đủ cột theo tài liệu (Loại, Loại giảm giá, Thành tiền giảm...)
- [x] Màn sửa: CKEditor cho Điều khoản + Ghi chú nội bộ, đổi tên Section, kéo-thả Section
- [x] Màn tạo: popup chọn nguồn tự vô hiệu hoá lựa chọn xung đột kèm chip lý do
- [x] Lỗi từ BE hiện dưới đúng từng dòng báo giá + toast chung "Có lỗi xảy ra, vui lòng kiểm tra lại"
- [x] Tab báo giá ở dự án cha: Khu vực 1 (icon theo trạng thái) + Khu vực 2 (danh sách bản báo giá tổng)
- [x] Xuất Excel (file .xlsx hợp lệ), Lịch sử, bản in hiện đủ các Section

### 2 lỗi phát hiện và đã sửa trong đợt kiểm này
1. **Báo giá tổng đã lập hợp đồng bị đánh "Hết hiệu lực"** khi tạo bản mới cho cùng dự án cha
   → `SummaryQuotationService::expireActiveSummaries()` loại trừ trạng thái "Đã tạo hợp đồng"
   (hợp đồng đã phát sinh bên ERP, huỷ hiệu lực báo giá gốc làm hồ sơ mất căn cứ).
2. **Icon Sửa / Xoá ở Khu vực 1 không bao giờ hiện** — API `child-quotations` không trả `creator_id`
   nên điều kiện "đúng người tạo" luôn sai → bổ sung `creator_id` vào `ChildQuotationResource`.
   Sau khi sửa: báo giá "Đang tạo" đủ 6 icon, báo giá đã duyệt chỉ còn xem/tải/in/sao chép.

## Rà lại theo tài liệu URD — vòng 2 (2026-07-31)

### Luồng tạo báo giá con khi đã có Báo giá Mỏ neo — 4 điểm chạm
- [x] **Điểm chạm 1 (Tạo mới)** — TRƯỚC ĐÂY THIẾU, đã bổ sung:
      thêm API `GET /assign/quotations/anchor-info/project/{projectId}` + `QuotationAnchorService::anchorInfoForProject()`
      (tra Mỏ neo theo dự án khi báo giá chưa có id); màn tạo báo giá nay hiện banner
      "Báo giá [Mã A1] … là Báo giá Mỏ neo … đã tự động đồng bộ cấu trúc giảm giá tổng"
      và dựng sẵn đúng bộ dòng "Loại giảm giá" của Mỏ neo ngay trên lưới
- [x] **Điểm chạm 2 (Lưu)** — lưu vẫn thành công + toast cam nêu đích danh:
      "Mã hàng HHBG002310 - ĐVT Bộ … sai lệch về Thuế VAT so với Báo giá Mỏ neo…"; dòng lệch bôi nền (`anchor-mismatch-row`)
- [x] **Điểm chạm 3 (Trình duyệt)** — popup "Không thể trình duyệt — vi phạm quy tắc đồng bộ"
      liệt kê đủ 2 loại lỗi (thiếu loại giảm giá + lệch VAT), chỉ có nút Đóng
- [x] **Điểm chạm 4 (Phê duyệt)** — badge xanh "Hệ thống xác nhận: … đã đồng bộ 100% với Báo giá Mỏ neo RT-BG-001"
- [x] Rule 1.1/1.2 — chọn dự án con ở màn tạo: tiền tệ/giảm giá/bảng giá lấy theo dự án và khoá; BE ép lại khi lưu

### Các luồng khác đã kiểm trong vòng này
- [x] Rule 17 — dịch vụ cùng mã khác giá (DV-THICONG 50tr vs 10tr) vẫn gộp được, mỗi dòng nằm đúng Section của nguồn
- [x] Cảnh báo hàng tạm trùng tên khi Lưu báo giá tổng (popup tổng kết + "Vẫn lưu"/"Để tôi rà soát lại")
- [x] Đổi tên + đổi thứ tự Section; kéo-thả; "Xem nguồn" trỏ đúng báo giá gốc
- [x] Từ chối duyệt kèm lý do → về "Đang tạo"; Sao chép; Huỷ → "Hết hiệu lực"
- [x] Hợp đồng Luồng 2 — báo giá con đã lập HĐ nhánh bị loại khỏi danh sách gộp và chặn khi cố gộp
- [x] Dự án cha: roll-up "Ngân sách đã phân bổ" = tổng ngân sách con (3 tỷ); khoá Tổng ngân sách từ bước 7;
      khoá Khách hàng khi đã có dự án con (kèm dòng giải thích); ẩn Loại hình/Lĩnh vực
- [x] Đang tạo → Đang thực hiện khi lưu dự án con; Đóng dự án cha → cascade đóng toàn bộ dự án con
- [x] Đủ 4 tab ở dự án cha (Thông tin chung / Dự án con / Báo giá / Meetings) + nút Thêm dự án con, Tạo báo giá tổng

### Lỗi phát hiện và đã sửa ở vòng 2
3. **Điểm chạm 1 chưa được làm ở màn tạo báo giá** (chỉ có ở màn sửa) → bổ sung API + banner + tự dựng dòng giảm giá.
4. **Dòng giảm giá do hệ thống tự dựng (giá trị 0) chặn cả nút Lưu nháp** ("Giá trị phải > 0") — hệ thống tự thêm
   dòng rồi bắt người dùng nhập mới cho lưu, trái tinh thần "Lưu = cảnh báo mềm" của tài liệu.
   → `validateQuotationDiscounts(strict)` bỏ qua dòng kế thừa chưa nhập khi Lưu nháp; Trình duyệt vẫn kiểm chặt.
   Đánh dấu lại cờ khi tải báo giá để lần sửa sau vẫn lưu nháp được.

- [x] **Sửa vị trí banner Mỏ neo** (user phản hồi): tài liệu ghi "banner ghim trên cùng" nhưng đang đặt ở cuối form
      (sát khối Thanh toán & Ghi chú) → chuyển lên **ngay dưới bảng "Thông tin chung"**, trước thanh công cụ
      VAT/Giảm giá, cho cả màn tạo và màn sửa. Banner nằm ngoài vùng thu gọn nên vẫn hiện khi user gập Thông tin chung.

## Rà tài liệu lần 3 — quét từng mục (2026-07-31)

Đối chiếu lại toàn bộ tài liệu URD, gồm cả những mục chưa đụng ở 2 vòng trước:

- [x] Rule 1 — khác Khách hàng / MST / Loại tiền tệ đều bị chặn, nêu đúng mã báo giá lệch
- [x] Rule 2 — chỉ lấy báo giá Đã duyệt/Trúng thầu, loại báo giá Đóng/Dừng và báo giá đã lập hợp đồng
- [x] Rule 3 — sửa header báo giá tổng (người liên hệ, địa chỉ, giao hàng, bảo hành) KHÔNG đụng báo giá nguồn
- [x] Rule 7 (phần UI) — bảng giảm giá tổng gộp read-only, không có cột %, kèm ghi chú "chỉ để tham chiếu"
- [x] Hiệu lực báo giá tổng tính lại theo MIN(mốc hệ thống, mốc hàng sắp đổi giá) ở mọi thao tác lưu/duyệt
- [x] Dropdown "Chọn mẫu báo giá" (lấy từ ERP) có ở phân vùng Thanh toán của báo giá tổng
- [x] Khu vực 2 đủ 4 action theo tài liệu (Xem / Tải / Sửa / Xoá); bản đã lập hợp đồng chỉ còn Xem + Tải
- [x] Timeline dự án con bị ràng buộc phải nằm trong khung thời gian dự án cha (FormRequest)
- [x] Đóng dự án cha: modal cảnh báo rõ "N dự án con trực thuộc sẽ bị đóng theo", bắt buộc chọn nguyên nhân
- [x] Tab Meetings ở dự án cha

### Bổ sung ở vòng này
5. **Chưa có dấu hiệu "báo giá nguồn đã đổi sau khi tổng hợp"** — tài liệu (Rule kế thừa) nói báo giá tổng
   không tự cập nhật khi nguồn thay đổi, nhưng hệ thống không hề báo cho người dùng biết là nó đã cũ.
   → Thêm cờ `source_is_outdated` (so `updated_at` của nguồn với thời điểm gộp) + cảnh báo trên màn báo giá tổng:
   "Báo giá nguồn X đã được sửa sau khi tổng hợp… bấm Làm mới dữ liệu để đồng bộ lại, hoặc tạo bản mới".
   Kiểm chứng: mới tạo → không cảnh báo; sửa nguồn → cảnh báo đúng mã; bấm Làm mới dữ liệu → cảnh báo tắt.

### Điểm KHÁC tài liệu (đã thống nhất trước đó, ghi lại để khỏi quên)
- Tài liệu mô tả nút **[Tạo Hợp Đồng Tổng] đặt tại màn Chi tiết Dự án Cha** (HRM chủ động gọi ERP tạo hợp đồng).
  Thực tế đang chạy theo **phương án A**: ERP chủ động gọi sang HRM (`erp-contract/eligible|{id}|{id}/mark`),
  người dùng lập hợp đồng bên ERP. Hệ quả nghiệp vụ giống hệt (khoá báo giá nguồn, báo giá tổng sang
  "Đã tạo hợp đồng", dự án cha lên bước 7) nhưng KHÔNG có nút bấm bên HRM.
- Bỏ mục xuất PDF riêng (dùng In → lưu PDF của trình duyệt).

## Dọn note thừa + gọn nút theo phản hồi (2026-07-31)

- [x] **Bỏ hết note/cảnh báo tài liệu không yêu cầu**: cảnh báo "nguồn đã sửa sau khi tổng hợp" (gỡ luôn cờ
      `source_is_outdated` ở BE), cảnh báo "báo giá nguồn không còn hiệu lực", ghi chú "(gộp từ báo giá nguồn —
      chỉ để tham chiếu…)" ở bảng giảm giá, 2 dòng hướng dẫn + cảnh báo "bản cũ sẽ hết hiệu lực" trong popup
      chọn nguồn, note "Dự án đã sang bước hợp đồng — không đổi được tổng ngân sách", note "Dự án cha đã có
      dự án con — không đổi được khách hàng". Các trường vẫn khoá như cũ, chỉ bỏ chữ giải thích.
      GIỮ những gì tài liệu yêu cầu: banner Mỏ neo, toast/popup 4 điểm chạm, popup hàng tạm trùng tên,
      popup "thông tin chưa lưu", cảnh báo đóng dự án cha kéo theo dự án con.
- [x] **Nút ở màn báo giá tổng bày theo trạng thái** (trước đây hiện hết 10 nút ở mọi trạng thái).
      Theo bảng "Trạng thái báo giá tổng" của tài liệu: In / Xuất Excel / Sao chép chỉ mở từ "Đã duyệt" trở đi;
      Huỷ bỏ khỏi trạng thái "Đang tạo" (đã có Xoá). Kết quả:
      - Đang tạo: Sửa, Xóa, Lịch sử, Trình duyệt, Làm mới dữ liệu, Quay lại (6 nút)
      - Đã duyệt: In, Hủy, Lịch sử, Trúng thầu, Sao chép, Xuất Excel, Quay lại
      - Hết hiệu lực: Lịch sử, Quay lại (đúng "chỉ xem")
- [x] Banner đỏ "Đã bị từ chối: [lý do]" trên màn báo giá tổng: GIỮ (người duyệt trả về thì Sale phải thấy
      ngay lý do để sửa).

## Fix: không chọn được "Không giảm giá" ở dự án cha (2026-08-01)

- [x] **Lỗi**: màn tạo/sửa dự án cha, dropdown Giảm giá không chọn được lựa chọn "Không giảm giá".
      Nguyên nhân: option để `id: null`, mà `V2BaseSelect` quy id về `opt.id || opt.value || opt.code`
      nên null (và cả 0) đều rơi về `undefined` → select2 không nhận được lựa chọn.
      → Đặt id nội bộ `'none'` cho lựa chọn này + computed `discountMethodValue` quy đổi 'none' ↔ null
      trước khi ghi vào form. KHÔNG sửa `V2BaseSelect` (component dùng chung).
- [x] Kiểm chứng: chuyển qua lại 3 lựa chọn đều đúng (2→2, 1→1, none→null); mở lại dự án cha đã lưu
      "Không giảm giá" thì dropdown hiển thị đúng "Không giảm giá", giá trị trong form vẫn là null.

### Rà toàn luồng sau khi sửa "Không giảm giá" (dữ liệu test: cha #99 + con #100/#101, báo giá #224/#225)

- [x] Màn tạo/sửa dự án cha: chọn qua lại cả 3 lựa chọn đều ăn, lưu xuống form đúng (2→2, 1→1, Không GG→null)
- [x] Màn xem dự án (chế độ chỉ đọc): hiển thị "Không giảm giá" thay vì để trống
- [x] Tạo dự án con, chọn cha "Không giảm giá": kế thừa đúng null + khoá trường (kèm tiền tệ, bảng giá)
- [x] Tạo báo giá cho dự án con: BE ép về "không giảm giá" dù FE gửi giá trị khác; màn báo giá hiển thị
      "Không GG" và khoá dropdown
- [x] Mỏ neo trên nhánh không giảm giá: anchor-check chạy bình thường (không sinh lỗi giả), anchor-info
      trả 0 dòng giảm giá dựng sẵn (đúng — chỉ dựng khi Mỏ neo dùng GG theo tổng)
- [x] Báo giá tổng từ 2 nguồn "không giảm giá": tạo được, bảng "Giảm giá tổng đơn hàng" KHÔNG hiện, tổng đúng
- [x] Rule 5 vẫn chặn khi trộn nguồn "không GG" với nguồn "GG tổng"
- [x] Kế thừa đơn giá đúng tài liệu: nguồn không giảm giá → báo giá tổng lấy **Đơn giá bán**
      (thử bẫy: để `unit_price_after_discount` = 1đ, báo giá tổng vẫn lấy đúng 100.000.000)
- [x] Nhánh "có giảm giá" cũ không bị ảnh hưởng: BGT-2026-00010 vẫn hiện bảng giảm giá gộp 2.000.000

## Fix: tick "Quản lý tất cả phòng ban" vẫn không duyệt được báo giá (2026-08-01)

- [x] **Lỗi**: ô tick "Quản lý tất cả phòng ban" (`company_employees.all_department`) chỉ set cờ, KHÔNG sinh
      bản ghi nào trong `employee_manage_departments`. Hai hàm gác quyền duyệt lại chỉ đọc bảng đó
      → người quản lý tất cả phòng ban hoá ra không quản lý phòng nào, luôn bị chặn với thông báo
      "Bạn không quản lý phòng ban của báo giá này". Ảnh hưởng CẢ báo giá thường lẫn báo giá tổng.
- [x] **Sửa theo pattern sẵn có của hệ thống** (`AssignJobService::listManageDepartmentIds`):
      thêm `QuotationService::managedDepartmentIdsOf()` — `all_department = 1` thì trả về toàn bộ phòng ban
      của công ty, ngược lại đọc `employee_manage_departments` như cũ.
      `SummaryQuotationService::ensureCanApprove()` gọi chung hàm này thay vì tự query.
- [x] Kiểm chứng: NV #36 (tick tất cả phòng ban, 0 bản ghi phòng) trước đây quản lý 0 phòng → nay 36 phòng.
      Xoá tạm 21 bản ghi phòng của tài khoản đang dùng, chỉ để lại cờ: duyệt được báo giá tổng
      (BGT-2026-00012 → Đã duyệt) và báo giá thường (NOGG-BG-002 → Đã duyệt). Đã khôi phục lại dữ liệu.
      Người không tick và không quản lý phòng nào (NV #25) vẫn bị chặn đúng.

## Redmine #10921 — 13 điểm feedback tester (2026-08-03)

- [x] 1. Meeting tạo từ dự án (tab Meetings → Tạo mới) rồi chọn loại "Meeting nội bộ" → mất sạch thông tin KH.
      Nguyên nhân: watcher `form.meeting_type_id` (GeneralInfo.vue) xoá toàn bộ trường KH khi loại meeting có
      `has_customer = 0`, nhưng khối "Khách hàng & Người liên hệ" vẫn hiện + vẫn bắt buộc vì meeting gắn dự án
      (KH kế thừa từ dự án) → màn trống trơn, không lưu được.
      → Thêm cờ `keepCustomerFromProject` (has_prospective_project / isFromProject / đã chọn dự án): meeting gắn
      dự án thì KHÔNG xoá KH khi đổi loại meeting. Verify A/B trên dev: code gốc customer_id → null; sau fix giữ
      nguyên KH 43244 + người liên hệ.
- [x] 2. Bảng "Dự án con" bám theo màn danh sách dự án TKT: thêm 4 cột Tiến trình dự án (pill cùng bảng màu
      .pj-status-*), Giải pháp, Version giải pháp, Khách hàng; cột Mã - Tên bổ sung Bộ phận / Ngày tạo / Ngày
      cập nhật. API `children` đã dùng chung ProspectiveProjectResource nên không phải sửa BE.
- [x] 3. Bỏ hẳn cột "Loại" khỏi bảng chi tiết báo giá tổng (user chốt 03/08): báo giá con không có cột này,
      phân biệt đã nằm ở dòng nhóm A/B. baseColspan 7 → 6, gỡ hàm rowKind. Verify: 15 cột khi bật "Hiện cột
      chi tiết", tổng colspan mọi dòng khớp 15/15.
- [x] 4. Block A/B đổi sang bộ màu của báo giá con: nền #e2f5ee, chữ #0f8a63, viền dưới 2px #9bdcc6.
      Dòng Section (tên dự án con) giữ màu tím nhạt riêng để còn phân biệt cấp.
- [x] 5. Khối cuối đổi thành "Thanh toán & Ghi chú nội bộ" y như báo giá con: thêm nút thu gọn
      (bottomCollapsed), label "Điều khoản báo giá" gắn required, dropdown mẫu điều khoản full width.
- [x] 6. Thêm dòng "TSLN trước GG / TSLN sau GG" ngay dưới bảng Tổng hợp giá trị (chỉ hiện khi xem được
      giá vốn), dựng như báo giá dự án con — công thức (doanh thu − giá vốn)/giá vốn, khác công thức /doanh thu
      của cột TSLN trong bảng (giữ nguyên đúng như báo giá con). Verify: BGT-2026-00013 hiện 46.17%.
- [x] 7. Phí vận chuyển: trước chỉ cộng `shipping_cost` nên dòng "Chi phí vận chuyển" ở bảng Tổng hợp có
      Thành tiền nhập = 0 và Thuế VAT = 0. Nay cộng dồn thêm `shipping_import_price` và quy %VAT về mức bình
      quân theo giá trị (helper `SummaryQuotationService::weightedVatPercent`) ở CẢ `buildSectionsFromSources`
      (lưu/sync) lẫn `preview`; FE `localBreakdown` truyền giá nhập + tiền VAT vào dòng vận chuyển.
      Verify: nguồn 3tr/VAT10% + 1tr/VAT5% → tổng 4tr, nhập 2,5tr, %VAT 8.75, tiền VAT 350.000 (đúng 300k+50k).
      Đã trả dữ liệu test về 0.
- [x] 8. Thêm thanh cuộn ngang phụ phía TRÊN bảng chi tiết, đồng bộ 2 chiều với thanh cuộn của bảng
      (copy pattern .products-scroll-top + ResizeObserver của báo giá con). Verify: spacer width = table
      scrollWidth (1120px), kéo thanh trên → bảng cuộn theo.
- [x] 9. Màn XEM báo giá tổng render thẳng `payment_terms` nên lộ nguyên `{{VAT_NOTE}}`,
      `{{VAN_CHUYEN_NOTE}}`. Nay dùng chung helper `substituteQuotationTermPlaceholders`
      (utils/assign/quotation-term.js) như báo giá con — số liệu lấy từ breakdown (gồm VAT vận chuyển).
      Bản in đã dùng helper từ trước nên không phải sửa. Bản LƯU vẫn giữ placeholder (mẫu còn động).
      Verify: {{VAT_NOTE}} → "Giá trên đã bao gồm thuế VAT", {{THANH_TIEN}} → 665.000.000.
- [x] 10. Vùng "Báo giá tổng" dựng lại theo đúng vùng "Báo giá từ dự án con": gom toàn bộ icon vào cột
      "Tên - Mã báo giá tổng" (dưới mã, cùng loại icon + cỡ 17px + class tp-icon-btn), BỎ cột "Thao tác"
      riêng đang trùng icon Xem. Bổ sung nút In và Sao chép cho đủ bộ; In/Excel/Sao chép chỉ hiện từ
      "Đã duyệt" trở đi (canExportOrPrintSummary) đúng như màn xem, Sao chép gọi endpoint
      `summary-quotations/{id}/duplicate` (KHÔNG dùng QuotationCopyMixin của báo giá thường).
- [x] 11. `ProspectiveProject::PARENT_STATUS` id 11 đổi nhãn "Đóng / Hủy dự án" → "Đóng/Không thực hiện
      dự án" (trùng nhãn của dự án con). FE đọc `status_name` từ BE nên không phải sửa. Verify: màn
      RT2.2026.CHA hiện đúng nhãn mới.
- [x] 12. Cột "Trạng thái sử dụng" tính theo `SUMMARY_ACTIVE_STATUSES`, mà đóng dự án lại đẩy báo giá tổng
      ra khỏi nhóm này → báo giá con tụt về "Chưa dùng". Nay `QuotationController::childrenQuotations` tính
      thêm báo giá tổng ở trạng thái ĐÓNG. Phân biệt rõ: đóng theo dự án thì GIỮ "Đã gộp BG Tổng", còn hết
      hiệu lực do có bản tổng mới thì vẫn về "Chưa dùng" (verify cả 2 chiều bằng API).
      Đổi tên cột "Trạng thái duyệt" → "Trạng thái".
- [x] 13. Thêm `Quotation::SUMMARY_STATUS_DONG = 5` (trùng id với STATUS_DONG của báo giá thường) + nhãn
      "Đóng" trong `getSummaryStatusList`. Tách hàm `SummaryQuotationService::closeByParentProject()` cho
      luồng đóng dự án (giữ nguyên `expireByParentProject`/`expireActiveSummaries` cho luồng "có bản mới
      thay thế"); `ProspectiveProjectService::closeParentProject` gọi hàm mới. Bản ĐÃ TẠO HỢP ĐỒNG vẫn
      được giữ nguyên trạng thái. Verify: đóng dự án cha #99 → BGT-2026-00012/13 chuyển "Đóng"; đã khôi
      phục dữ liệu test.

### Verify bổ sung #10921 (2026-08-03, sau khi user hỏi "test kỹ chưa")

Bốn chỗ trước đó mới verify gián tiếp, nay đã chạy thật:

- [x] Nút **Sao chép báo giá tổng** (mục 10 — code mới, trước đó chưa chạy lần nào vì đang đăng nhập tài khoản
      không phải sale chính nên nút bị ẩn): bấm thật trên BGT-2026-00011 → popup xác nhận → tạo BGT-2026-00014
      (id 228) + điều hướng sang bản mới, bản cũ chuyển Hết hiệu lực. `apiPostMethod` key `payload` đúng.
- [x] Nút **In báo giá tổng** (mục 10) + **biến điều khoản trên BẢN IN** (mục 9): modal cấu hình in mở đúng,
      bản xem trước ra "Giá trên đã bao gồm thuế VAT, đã bao gồm chi phí vận chuyển. Tổng: 666.280.000",
      không còn `{{`.
- [x] **Mục 6 + 7 ở màn TẠO** (nhánh `localBreakdown` tính client-side, khác nhánh breakdown từ BE đã test
      trước): 2 nguồn 8tr/nhập 5tr/VAT 8% → dòng Chi phí vận chuyển hiện nhập 10.000.000, VAT 1.280.000;
      dòng TSLN tổng hiện 122.79% (khớp (606tr−272tr)/272tr).
- [x] **Mục 13 qua đúng `ProspectiveProjectService::closeParentProject`** (trước đó mới gọi thẳng
      `closeByParentProject`): chạy trong `DB::beginTransaction()` → dự án cha #99 sang "Đóng/Không thực hiện
      dự án", 2 dự án con đóng theo, BGT-2026-00012/13 sang "Đóng" → `DB::rollBack()`, dữ liệu nguyên trạng.

Dọn sau test: xoá BGT-2026-00014 (0 group / 0 source còn lại), trả BGT-2026-00011 về "Đang tạo",
gỡ role "Xem giá vốn ERP" cấp tạm cho NV#13, xoá payment_terms test.

CHƯA test: build production FE (chỉ chạy dev server), bảng "Dự án con" khi dự án cha chưa có con nào.

### Bổ sung mục 2 (2026-08-03 — user phản hồi "vẫn không đủ trường")

- [x] Bảng "Dự án con" **bê nguyên bộ cột của màn danh sách dự án TKT** thay vì chỉ thêm 4 cột như lần đầu:
      đủ 20 cột theo đúng thứ tự `allColumns` của `index.vue` (STT, Mã - Tên dự án TKT, Loại DA, Tiến trình
      dự án, Giải pháp, Version giải pháp, Khách hàng, Khách hàng cuối, Giai đoạn dự án, Quy mô dự án,
      Phân loại đầu tư, Nguồn vốn, Tổng số ngày hoàn thành, Phòng làm GP, PM giải pháp, Ngày KH cần GP,
      Ngày dự kiến chốt GP, Ứng dụng, Lĩnh vực KD KH, Loại hình hoạt động KH) + copy nguyên cell template
      và các hàm đổi id → tên (getStatusLabel/getNameScale/getNameInvestmentType/getNameFundingSource),
      cộng 2 cột đặc thù cha - con ở cuối (Ngân sách dự kiến, Thời gian). Nút Xem/Sửa chuyển vào cột
      Mã - Tên như màn danh sách, bỏ cột "Thao tác" riêng.
      API `children` đã dùng chung `ProspectiveProjectResource` nên trả sẵn đủ trường → không sửa BE.
      Verify: 22 cột render đúng, badge "Dự án con", pill tiến trình đúng màu, 0 lỗi console của component
      (8 warning còn lại là của TktTab/ChooseErpCustomerModal/SolutionApprovalModal, có sẵn từ trước).
      CHƯA bê: bộ lọc nâng cao và nút "Cấu hình cột hiển thị" của màn danh sách (nút này lưu cấu hình theo
      key `prospective_projects` dùng chung — bật ở tab sẽ ảnh hưởng luôn màn danh sách).

### Bổ sung mục 10 (2026-08-03 — user: "icon nhỏ thôi, như ở tab Dự án con")

- [x] Bỏ `tp-icon-btn` (ô vuông 32×32) + `style="font-size: 17px"` khỏi **cả hai** vùng của tab Báo giá
      (Báo giá từ dự án con + Báo giá tổng), dùng đúng kiểu nút của bảng tab "Dự án con":
      `class="btn btn-light border btn-sm mr-1"`, icon để cỡ mặc định. Sửa cả 2 vùng vì yêu cầu gốc #10921
      là 2 vùng phải thống nhất — chỉ thu nhỏ vùng tổng sẽ lại lệch nhau. Class `.tp-icon-btn` trong file
      đã hết chỗ dùng nên xoá luôn.
      Verify: icon 13px và nút 29×28 ở cả 2 vùng, khớp tab "Dự án con" (13px).

### Bổ sung mục 5 (2026-08-03 — user: "ở màn show tôi đang thấy khác nhau")

- [x] Lần đầu mới làm khớp CHẾ ĐỘ SỬA (section-header + thu gọn + editor như quotations/_id/edit.vue),
      còn chế độ XEM vẫn là hộp `terms-box` bo góc — khác màn xem báo giá con. Nay phân nhánh theo chế độ:
      * Tạo/Sửa: giữ section "Thanh toán & Ghi chú nội bộ" + nút thu gọn (như edit.vue báo giá con)
      * Xem: bảng 2 cột y hệt quotations/_id/index.vue — hàng "Điều khoản báo giá" (đã thay biến) +
        hàng "Ghi chú nội bộ" chỉ hiện khi có; không tiêu đề, không hộp riêng.
      Style copy đúng thông số màn xem báo giá con nhưng đặt trong class riêng `.terms-table`, KHÔNG sửa
      `.info-table` chung (đang dùng cho khối Thông tin chung của chính màn này). Gỡ `.terms-box` hết dùng.
      Verify bằng getComputedStyle 2 màn: padding 6px 10px · font-size 12.5px · color rgb(55,65,81) ·
      nền rgb(249,250,251) · width 160px · vertical-align top — khớp 100%.
      KHÁC BIỆT CÒN LẠI (chưa làm, cần chốt): màn xem báo giá con có thêm hàng "Ghi chú Kinh doanh"
      (ô nhập + nút Lưu ghi chú) khi báo giá Đã duyệt — báo giá tổng có sẵn cột `sales_note` nhưng chưa
      có UI này, thêm vào là thêm hành vi nghiệp vụ mới nên đang để nguyên.

### Bổ sung mục 5 — hàng "Ghi chú Kinh doanh" (2026-08-03, user: "làm giống hệt báo giá con")

- [x] BE: `SummaryQuotationService::updateSalesNote()` — bản sao của `QuotationService::updateSalesNote`
      cho báo giá tổng: chỉ sửa khi Đã duyệt (status 4) + chỉ NV KD phụ trách chính của DỰ ÁN CHA,
      ghi lịch sử `update_sales_note` (from = to = 4, meta old/new). KHÔNG tái dùng `updateHeader`
      vì hàm đó `ensureEditable` chặn ở mọi trạng thái khác "Đang tạo".
      Thêm `SummaryQuotationController::updateSalesNote` + route `PUT assign/summary-quotations/{id}/sales-note`
      (đối xứng route của báo giá thường).
- [x] FE: hàng "Ghi chú Kinh doanh" ở cuối bảng điều khoản màn xem, hiện khi status = 4 —
      KD phụ trách thấy ô nhập + nút "Lưu ghi chú", người khác chỉ đọc (giống hệt quotations/_id/index.vue).
      `form.sales_note` bổ sung ở `_id/index.vue`, lưu xong emit `sales-note-saved` → page `loadData()`.
- [x] Verify: API chặn đúng 3 case (người không phụ trách → 422 "Chỉ NV Kinh doanh phụ trách dự án...",
      bản Đang tạo → 422 "Chỉ có thể sửa ghi chú khi báo giá tổng đã duyệt", sale chính → 200);
      UI nhập + bấm Lưu thật → DB lưu đúng + sinh 1 dòng lịch sử `update_sales_note`; đăng nhập NV khác
      thì hàng chỉ hiển thị text, không có ô nhập/nút lưu. Đã xoá sales_note + 2 dòng history test.
