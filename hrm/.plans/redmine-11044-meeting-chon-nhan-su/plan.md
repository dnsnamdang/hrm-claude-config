# Redmine #11044 — Tối ưu UI/UX chọn nhân sự (Người đề xuất / Người thực hiện)

Màn: Meetings → Lịch meeting → Chi tiết → Tab Biên bản cuộc họp (`pages/assign/meeting/components/MeetingReport.vue`)
Nhánh: `tpe-develop-assign_fix` (cả API và Client)

## Phase 1 — Người thực hiện chọn nhiều

### BE
- [x] Migration tạo bảng `meeting_report_executors` (meeting_report_id, executor_id, executor_name, executor_type, created_by, updated_by)
- [x] Entity `MeetingReportExecutor` + quan hệ `executors()` trên `MeetingReport` (`$with`)
- [x] `MeetingService::syncReports()` ghi danh sách người thực hiện; vẫn ghi `executor_name` (chuỗi gộp) để in/xuất Excel/báo cáo cũ không vỡ
- [x] `getListEmployee`: thêm filter `working_position_id` (Chức vụ), `employee_role_id` (Chức danh), tham số `only_ids=1` trả toàn bộ id theo bộ lọc (phục vụ Chọn tất cả nhiều trang)

### FE
- [x] Component dùng chung `components/V2BasePickerField.vue` — ô click cả khối mở popup, hiển thị text (đơn) hoặc tag có nút x (nhiều)
- [x] `PopupStaff.vue`: chế độ đơn click dòng là chọn + tự đóng; thêm filter Chức vụ / Chức danh; checkbox "Chọn tất cả" theo toàn bộ bộ lọc (mọi trang); nút "Thêm thành viên"; nhận `initialSelected` để tick sẵn người đã chọn
- [x] `MeetingReport.vue`: ô Người đề xuất dùng picker đơn, Người thực hiện dùng picker nhiều (`r.executors`), đồng bộ `executor_name`

### Checkpoint — 2026-08-26
Vừa hoàn thành: toàn bộ Phase 1 (BE + FE), đã test BE bằng tinker (sync/filter/get_all trả đúng)
Đang làm dở: chưa test UI thật trên trình duyệt
Bước tiếp theo: chạy thử màn Biên bản cuộc họp trên :3000 theo 4 AC của task
Blocked:

## Kiểm thử (2026-08-26)

- [x] BE 33 case (tinker): bộ lọc Chức vụ/Chức danh + kết hợp + giá trị không tồn tại · `get_all` khớp tổng phân trang và chứa hết id mọi trang · lưu nhiều/0/tên rỗng người thực hiện · lưu lại lần 2 không nhân đôi · nhân sự khách hàng type=2 · tương thích ngược `executor_name` · xoá meeting không để mồ côi
- [x] UI vòng 1 — 32 case (Playwright): AC1 chọn đơn tự đóng · AC2 tag + nút x · AC3 bộ lọc Chức vụ/Chức danh/Phòng ban · AC4 Chọn tất cả mọi trang · click lại bỏ tick · bỏ tick tất cả · đóng popup không mất tag · không lỗi JS
- [x] UI vòng 2 — 18 case: lưu → tải lại còn đủ tag, đúng thứ tự · bỏ hết người thực hiện bị BE chặn (400, lỗi đúng `reports.0.executor_name`) · màn Xem khoá ô + không mở popup · tài khoản ngoài cuộc họp bị 403 và bị đá khỏi màn Sửa · chưa đăng nhập thì `get_all` bị chặn
- [x] UI vòng 3 — 4 case: màn In hiện đủ 3 người thực hiện; `executor_name` (báo cáo cũ) đủ 3 tên
- [x] Dọn dữ liệu thử: xoá dòng biên bản thử + meeting thử, trả lại ngày meeting 26, trả lại mật khẩu tài khoản test

**Lỗi phát hiện khi test và đã sửa:** `MeetingController::destroy()` xoá meeting nhưng không dọn `meeting_report_executors` → dữ liệu mồ côi.

**Ngoài phạm vi task:** DB `hrm_prod_local` thiếu 12 migration nhánh meeting (mọi API chi tiết meeting trả 500) — đã chạy `php artisan migrate` theo xác nhận của user.

### Checkpoint — 2026-08-26
Vừa hoàn thành: code + test đầy đủ (87 case, 0 FAIL), Redmine #11044 chuyển "Đang tiến hành"
Đang làm dở:
Bước tiếp theo: chờ review / chuyển "Code xong chờ test" khi bàn giao
Blocked:

## Bổ sung — Bộ lọc dạng "Tìm kiếm nâng cao" (yêu cầu user 2026-08-26)

- [x] `PopupStaff.vue` bỏ khối `.pick-filter` tự dựng, chuyển sang `components/V2BaseFilterPanel.vue` — copy pattern từ `pages/assign/quotations/components/QuotationProductSearchModal.vue:34` (popup "Thêm hàng hoá")
  - Ô tìm nhanh "Tìm theo tên, mã nhân viên" + nút Tìm kiếm / Làm mới luôn hiện cùng hàng (`inlineSearchButtons`)
  - Công ty · Phòng ban · Bộ phận · Chức vụ · Chức danh nằm trong panel ẩn/hiện, **mặc định thu gọn** để dồn chỗ cho bảng nhân sự
  - Gõ chữ chỉ cập nhật keyword (Enter/nút mới tìm), bấm X xoá trắng thì tìm lại ngay — đúng khuôn `onQuickSearchChange` của popup Báo giá
- [x] Chạy lại bộ UI test: 35/35 PASS (thêm 3 case: mặc định thu gọn · ô tìm nhanh luôn hiện · bấm "Tìm kiếm nâng cao" mở panel)
- [x] Sửa lệch lề bộ lọc: 3 ô Công ty/Phòng ban/Bộ phận do `V2BaseCompanyDepartmentFilter` render (component con, bọc `.d-contents`) nên rule padding scoped không chạm tới → dòng 1 lệch 8px so với dòng 2 và ô tìm nhanh. Đổi sang `.pick-filter-row ::v-deep [class*='col-']`. Đo lại bằng Playwright: mọi hàng đều `left=271`, ô lọc `x=275` = mép ô tìm nhanh. Thêm 2 case chống tái phát (37/37 PASS)

## Bổ sung 2026-09-11 — thêm cột trong popup chọn nhân sự
- [x] BE `getListEmployee`: join `parts` + `titles`, trả `part_name`, `title_name`
- [x] FE `PopupStaff.vue`: thêm cột Bộ phận / Chức vụ / Chức danh vào bảng nhân sự công ty (bỏ dòng phụ chức vụ dưới tên)
- [x] Popup rộng hơn (`dialog-class="pick-staff-dialog"`, max-width 1500px/96vw) + min-width cho cột Bộ phận/Chức vụ/Chức danh
- [x] Giảm padding popup: `body-class="p-0"` + `.pick-body` 0.5rem, tab bar margin 8px

## Bổ sung 2026-09-14 — popup chọn nhân viên phía công ty mặc định lọc theo công ty đăng nhập (@khoipv)

Yêu cầu user: màn Tạo meeting → khối "Thành phần — Phía Công ty" → mở popup chọn nhân viên thì
ô **Công ty** phải điền sẵn công ty đang đăng nhập (hiện đang để trống = xem toàn bộ công ty).

Quyết định đã chốt với user:
- Chỉ áp dụng cho popup "Chọn nhân viên phía công ty" (`GeneralInfo.vue`, `modalId=pickModalCompanyMember`).
  Popup "Chọn người đề xuất / Người thực hiện" ở tab Biên bản (`MeetingReport.vue`) GIỮ NGUYÊN → gate bằng prop.
- Nút "Xoá lọc/Làm mới" vẫn xoá trắng cả ô Công ty (không kéo về mặc định).
- Đóng popup rồi mở lại thì về mặc định (điền lại công ty đăng nhập).
- Popup ở màn Sửa meeting cũng có mặc định này (dùng chung `MeetingForm`) — user chấp nhận.

### FE
- [x] `PopupStaff.vue`: thêm prop `defaultCurrentCompany` + computed `defaultCompanyId` (`$store.state.current_company`)
- [x] `PopupStaff.vue`: `mounted()` gán company_id trước lần `getDataStaff()` đầu → không gọi API thừa
- [x] `PopupStaff.vue`: `onModalShow()` đặt lại TOÀN BỘ bộ lọc về mặc định rồi nạp lại danh sách
      (đặt lại cả phòng ban/bộ phận, nếu chỉ kéo ô Công ty mà giữ phòng ban của công ty cũ sẽ ra danh sách rỗng khó hiểu)
- [x] Tách `clearFilterValues(companyId)` dùng chung cho `resetFilter()` và `applyDefaultFilter()` — khỏi lặp danh sách trường
- [x] `GeneralInfo.vue`: truyền `:defaultCurrentCompany="true"` cho `PopupStaff` của thành phần công ty
- [x] Kiểm chứng: compile FE (vue-template-compiler + babel) OK cả 2 file; truy nguồn `current_company`

### Ghi chú kỹ thuật
- `$store.state.current_company` nạp trong `store/actions.js` `nuxtClientInit()` (API `users/auth/user-profile`),
  BE trả `auth()->user()->current_company_role` — là **id công ty**, không phải object. Có ở mọi trang nên popup luôn lấy được.
- `buildQuery()` (`utils/url-action.js`) bỏ qua `null`/`undefined`/`''` → công ty rỗng vẫn gọi API như cũ, không sinh `company_id=`.
- `V2BaseCompanyDepartmentFilter` v-model THẲNG vào `form.company_id` nên chỉ cần gán giá trị là ô select hiển thị đúng;
  watcher của nó tự xoá department/part/employee khi company đổi.

### Checkpoint — 2026-09-14
Vừa hoàn thành: FE 2 file (`PopupStaff.vue`, `GeneralInfo.vue`), compile sạch
Đang làm dở:
Bước tiếp theo: user mở `/assign/meeting/create` → khối Thành phần Phía Công ty → bấm chọn nhân viên, xác nhận ô Công ty điền sẵn công ty đăng nhập và danh sách lọc đúng
Blocked:

BE: KHÔNG đổi. Migration: KHÔNG. Quyền: KHÔNG.

## Bổ sung 2026-09-14 (2) — popup bị KHOÁ CUỘN sau khi bấm × xoá bộ lọc (@khoipv)

User báo: trong popup chọn nhân sự, tìm kiếm xong bấm × thì không cuộn được nữa.

### Nguyên nhân gốc (đã đo, không phải suy đoán)
`select2 4.0.13` — `dropdown/attachBody`:
- `_attachPositioningHandler` (:4433-4457): mở dropdown là ghi lại vị trí cuộn của MỌI cha đang có
  thanh cuộn rồi gắn `scroll.select2.<id>` KÉO `scrollTop` về chỗ cũ mỗi lần cuộn. Cha đó ở popup này
  là `div.modal` (đo: `scrollHeight 848 / clientHeight 738`).
- `_detachPositioningHandler` (:4460-4470): lúc đóng lại LỌC cha bằng `Utils.hasScroll` (:711-733) —
  tính theo nội dung TẠI THỜI ĐIỂM ĐÓ. Bộ lọc làm danh sách ngắn lại (3-6 dòng → `scrollHeight 738
  = clientHeight 738`, popup hết cuộn) ⇒ select2 KHÔNG thấy `.modal` nên KHÔNG gỡ ⇒ handler mồ côi.
- Danh sách dài lại (10 dòng) ⇒ handler cũ ghim `scrollTop` ⇒ không cuộn được, F5 mới hết.

Kích hoạt bởi **nút × (clear) của select2**, KHÔNG phải nút X của ô tìm nhanh (ô tìm nhanh đo ra bình thường).
Lỗi CÓ SẴN TỪ TRƯỚC (× ở ô Chức vụ cũng dính); thay đổi mặc định công ty hôm nay chỉ làm ô Công ty
có thêm nút × nên gặp dễ hơn.

### Cách vá
- [x] Lấy NGUYÊN file `components/V2BaseSelectInModal.vue` từ nhánh `gop_db` (commit `f85cefb8c`, hàm
      `releaseScrollLock` — chính bản vá lỗi này, đã chạy trên `gop_db` từ 07/09):
      `git checkout gop_db -- components/V2BaseSelectInModal.vue`
      Chọn lấy nguyên file thay vì gõ tay 44 dòng để **sau này merge `gop_db` không conflict ở file này**
      (đã xác nhận `git diff gop_db -- <file>` = 0 dòng). File chỉ hơn bản cũ 49 dòng thêm, 0 dòng xoá;
      5 dòng thừa là prop `keepLockedOptions` (mặc định false, nhánh này không màn nào truyền → vô hại).
- [x] Compile check 3 file: OK

### Kiểm chứng (Playwright, localhost:3000 — đo `scrollTop` đặt 120 rồi đọc lại sau 600ms)
| Ca | Trước vá | Sau vá |
| --- | --- | --- |
| Mở popup, chưa đụng gì | 110 tự do | 110 tự do |
| Tìm nhanh → bấm X ô tìm nhanh | 110 tự do | 110 tự do |
| Bấm × ở ô **Công ty** | **0 — ghim** | **110 — tự do** ✅ |
| Chọn Chức vụ → bấm × ở ô **Chức vụ** | **0 — ghim** | **110 — tự do** ✅ |
| Hồi quy: dropdown ĐANG MỞ thì vẫn phải ghim (để dropdown không trôi) | ghim | **vẫn ghim** ✅ |
| Hồi quy: đóng dropdown xong cuộn tự do | — | **tự do** ✅ |
| Hồi quy: đóng popup mở lại → ô Công ty vẫn điền sẵn, 10 dòng, cuộn tự do | — | ✅ |

### Checkpoint — 2026-09-14 (2)
Vừa hoàn thành: vá khoá cuộn bằng cách port `V2BaseSelectInModal.vue` từ `gop_db`, đo lại 7 ca đều đạt
Đang làm dở:
Bước tiếp theo: user bấm tay lại trên trình duyệt cho chắc; nhánh này chưa commit
Blocked:

## Bổ sung 2026-09-14 (3) — bộ lọc popup tự tìm khi chọn, khỏi bấm nút Tìm kiếm (@khoipv)

Yêu cầu user: chọn giá trị ở bộ lọc trong popup chọn nhân sự là tìm luôn.
Hiện trạng: Chức vụ/Chức danh đã tự tìm (`@input="searchStaff"`), riêng Công ty/Phòng ban/Bộ phận thì không —
`V2BaseCompanyDepartmentFilter` KHÔNG `$emit` gì cả (ghi thẳng vào prop `form`) nên `@filter-change`
ở dòng 70 là listener chết, `handleFilterChange()` cũng rỗng.

### FE (chỉ `PopupStaff.vue`, không đụng component dùng chung)
- [x] Thêm watcher cho 5 khoá lọc (company_id, department_id, part_id, working_position_id, employee_role_id) → `autoSearch()`
- [x] `autoSearch()` gộp nhiều thay đổi cùng nhịp thành 1 request (`$nextTick` + cờ `pendingAutoSearch`):
      chọn 1 công ty làm component con xoá luôn department_id + part_id → 3 watcher nổ cùng lúc
- [x] Cờ `suppressAutoSearch` bật trong `clearFilterValues()` — "Làm mới" và bộ lọc mặc định lúc mở popup
      đổi 6 trường một lúc mà đã tự gọi `getDataStaff()` rồi
- [x] Bỏ `@input="searchStaff"` ở Chức vụ/Chức danh (watcher đã lo, để lại là gọi API 2 lần)
- [x] Xoá `@filter-change` + `handleFilterChange()` rỗng
- [x] Giữ nguyên: ô tìm nhanh vẫn Enter/nút Tìm kiếm; nút Tìm kiếm vẫn còn
- [x] Kiểm chứng: đếm request `getListEmployee` — mỗi thao tác đúng 1 request

⚠️ **Bẫy đã trả giá — thứ tự hàng đợi `$nextTick` của Vue.** Bản đầu đặt `$nextTick(nhả cờ)` ngay đầu
`clearFilterValues()` (trước khi gán giá trị) ⇒ "Làm mới" bắn **2 request giống hệt nhau**. Lý do:
hàng đợi watcher (`flushSchedulerQueue`) chỉ được đăng ký ở LẦN GÁN ĐẦU TIÊN, nên callback nhả cờ
đăng ký trước đó nằm TRƯỚC nó ⇒ cờ nhả xong watcher mới chạy ⇒ hết bị chặn. Sửa: đăng ký nhả cờ ở
CUỐI hàm, sau khi đã gán hết 6 trường. Đo lại còn đúng 1 request.

### Kiểm chứng (Playwright — đếm request `assign/meeting/getListEmployee`)
| Thao tác | Số request | Query gửi lên |
| --- | --- | --- |
| Mở popup | 1 | `page=1&per_page=10&company_id=1` |
| Chọn Phòng ban | 1 | `…&company_id=1&department_id=5` |
| Đổi Công ty (kéo theo xoá phòng ban + bộ phận) | **1** | `…&company_id=4` (không còn department_id) |
| Chọn Chức vụ | 1 | `…&working_position_id=18` |
| Bấm × xoá Chức vụ | 1 | `page=1&per_page=10` — cuộn vẫn tự do (110) ✅ |
| Bấm "Làm mới" | 1 | `page=1&per_page=10`, ô Công ty về trống |
| Gõ 6 ký tự ở ô tìm nhanh | **0** | (đúng thiết kế — chưa Enter) |
| Enter ở ô tìm nhanh | 1 | `…&keyword=nguyen` |
| Đóng rồi mở lại popup | 1 | `…&company_id=1`, keyword đã xoá, ô Công ty điền sẵn |

### Checkpoint — 2026-09-14 (3)
Vừa hoàn thành: bộ lọc popup tự tìm khi chọn, đo 9 ca đều đúng 1 (hoặc 0) request
Đang làm dở:
Bước tiếp theo: user bấm tay xác nhận; cả 3 việc hôm nay (mặc định công ty · vá khoá cuộn · tự tìm) đều CHƯA COMMIT
Blocked:

## Bổ sung 2026-09-14 (4) — đổi tiền tố thông báo [Meeting] → [MET] (@khoipv)

Theo `.claude/skills/notification-convention` mục 3, prefix chuẩn của Meeting là `[MET]`.
Rà cả 2 repo: FE không có chỗ nào, BE còn **đúng 2 chỗ** trong `sendMeetingNotification()` —
code cũ không đi qua helper `notifyMeetingEmployees()` (helper này vốn đã mặc định `[MET]`).

### BE
- [x] `Modules/Assign/Services/MeetingService.php:1597` (trạng thái Lên lịch) — `[Meeting]:` → `[MET]:`
- [x] `Modules/Assign/Services/MeetingService.php:1615` (trạng thái Chốt lịch) — `[Meeting]:` → `[MET]:`
- [x] Rà lại: `grep -rn "\[Meeting\]"` ở cả `hrm-api` (Modules/, app/, resources/) lẫn `hrm-client` — 0 kết quả
- [x] `php -l` sạch

### Còn lệch chuẩn (CHƯA sửa — ngoài phạm vi user yêu cầu, chờ chốt)
2 thông báo này vẫn là `[MET]: <b>Tên</b>. …`, THIẾU **Nhóm hành động** theo mục 1 của skill
(`[PREFIX] {Nhóm hành động}: {Tên}. {Ghi chú}`) và không cắt 50/120 ký tự. Muốn chuẩn hoá thì
chuyển sang `buildMeetingNotificationContent()` như các chỗ khác, nhưng phải chốt nhóm hành động:
- Lên lịch → `Tạo mới`?
- Chốt lịch → `Cập nhật` hay `Thay đổi lịch`? ("Chốt lịch" KHÔNG nằm trong 14 giá trị cho phép)
Lưu ý khi làm: `sendMeetingNotification()` có `array_merge(..., attendanceConfirmNotificationData())`
(cụm nút Có mặt/Vắng — Redmine #11369), helper `notifyMeetingEmployees()` không kèm dữ liệu này
→ không được thay thẳng bằng helper, chỉ thay phần dựng chuỗi.

### Dữ liệu cũ
`notifications` trên DB local còn **4 dòng** mang tiền tố `[Meeting]` (mới nhất 2026-09-12).
CHƯA đụng vào — chờ user quyết có cập nhật dữ liệu cũ hay để tự trôi.

## Bổ sung 2026-09-14 (5) — thông báo giao nhiệm vụ chỉ gửi khi meeting HOÀN THÀNH (@khoipv)

Yêu cầu user: hiện bấm "Lưu và Lên lịch" / "Lưu và Chốt lịch" là thông báo giao nhiệm vụ bắn ngay.
Đổi thành **sau khi Hoàn thành meeting mới gửi**, gửi cho **Người thực hiện VÀ Người đề xuất**.
Nội dung thông báo GIỮ NGUYÊN (user chốt: "chỉ thay đổi lúc gửi thông báo thôi").

Hiện trạng: `MeetingService::notifyReportExecutors()` (Redmine #11291) chỉ chặn khi Nháp/Huỷ →
Lên lịch/Chốt lịch là gửi. Và nó CHỈ gửi cho người thực hiện; `meeting_reports.proposer_id`
chưa từng được dùng để gửi thông báo.

### BE (`Modules/Assign/Services/MeetingService.php` + `MeetingController.php`)
- [x] `notifyReportExecutors()`: chỉ chạy khi `status == Meeting::HOAN_THANH`
- [x] BỎ so sánh chênh lệch (`added = mới − cũ`) — bẫy: người thực hiện đã được gán từ lúc Chốt lịch
      nên đến lúc Hoàn thành tập chênh RỖNG → không ai nhận. Khi hoàn thành gửi cho TOÀN BỘ.
      Không sợ spam: `update()` khoá meeting đã Hoàn thành (423, controller dòng 478) nên chỉ gửi 1 lần.
- [x] Thêm `reportProposerEmployeeIds()` — `meeting_reports.proposer_id` với `proposer_type = CONG_TY`
      (đề xuất phía KH trỏ sang `meeting_employees`, không có tài khoản → loại, giống người thực hiện)
- [x] Gộp trùng: ai vừa đề xuất vừa thực hiện chỉ nhận 1 thông báo
- [x] Đổi `countReportTasksByExecutor()` thành `countReportRowsByEmployee()` — đếm số DÒNG biên bản
      người đó liên quan với vai thực hiện HOẶC đề xuất (kiêm 2 vai cùng 1 dòng vẫn tính 1)
- [x] Bỏ tham số `$oldExecutorIds` + snapshot ở controller (hết chỗ dùng, không để lại code chết)
- [x] Giữ nguyên: chuỗi thông báo, prefix `[MET]`, nhóm hành động `Tạo mới`, deep-link `?active_tab=reports`
- [x] `php -l` sạch cả 2 file

### Kiểm chứng (tinker — `Queue::fake()` chặn job FCM + bọc transaction rồi rollback, KHÔNG để lại dữ liệu)
| Trạng thái meeting | Số thông báo tạo ra |
| --- | --- |
| Lên lịch (#30, status=1) | **0** ✅ |
| Chốt lịch (#16, status=2) | **0** ✅ |
| Hoàn thành (#19, status=3) | **6** = 2 người thực hiện + 5 người đề xuất, gộp trùng emp 84 |
| Hoàn thành (#4, status=3) | **4** = 3 thực hiện + 2 đề xuất, gộp trùng emp 138 |

Tổng bảng `notifications` trước/sau test đều = 11 → rollback sạch.
Nội dung sinh ra giữ nguyên format cũ:
`[MET] Tạo mới: <b>Đào tạo sử dụng dự án tiền khả thi -phòng kd2</b>. Bạn được giao 6 nhiệm vụ.`
`url=/assign/meeting/19/show?active_tab=reports · type=meeting`

⚠️ Chưa đụng: `changeStatus()` (docblock ghi "chỉ dùng cho action Huỷ") — nếu sau này có luồng
hoàn thành meeting qua endpoint đó thì phải gọi thêm `notifyReportExecutors()` ở đấy.

### Checkpoint — 2026-09-14 (4)
Vừa hoàn thành: 5 việc trong ngày (mặc định công ty · vá khoá cuộn · bộ lọc tự tìm · [Meeting]→[MET] · dời thời điểm gửi thông báo giao nhiệm vụ)
Đang làm dở:
Bước tiếp theo: user nghiệm thu trên trình duyệt; TẤT CẢ đều CHƯA COMMIT (hrm-api + hrm-client)
Blocked:

### Kiểm chứng vòng 2 — chạy THẬT qua API (user yêu cầu test lại, 2026-09-14)
Script: `scratchpad/test_noti_flow.php` + `test_noti_flow2.php` — gọi endpoint `POST /api/v1/assign/meeting/{id}`
qua HTTP kernel bằng JWT thật (auth model `TpEmployee`), `Queue::fake()` chặn job đẩy FCM ra thiết bị thật
(`QUEUE_CONNECTION=sync` nên không chặn là bắn push thật), toàn bộ bọc transaction rồi rollback.

| Ca | Kết quả |
| --- | --- |
| Meeting #17 (Chốt lịch) — bấm Lưu, giữ nguyên trạng thái | HTTP 200 · **0** thông báo giao nhiệm vụ ✅ |
| Meeting #17 — chuyển **Hoàn thành** | HTTP 200 · **2** thông báo = người thực hiện 1370 + người đề xuất 1141 ✅ |
| Meeting #30 — **Lên lịch → Chốt lịch** (hồi quy) | HTTP 200 · **0** giao nhiệm vụ, **+3** thông báo mời họp cho 3 thành viên ✅ |
| Sau rollback | `notifications` = 11 như trước, status meeting trả về nguyên trạng ✅ |

Nội dung sinh ra: `[MET] Tạo mới: <b>Đào tạo hướng dẫn sử dung phần mềm Dự án tiền k...</b>. Bạn được giao 1 nhiệm vụ.`
(tên cắt 50 ký tự đúng chuẩn notification-convention).

2 guard KHÔNG liên quan nhưng chặn test, phải dời giờ họp trong transaction mới đi tiếp được:
`isReportOverdue()` (quá hạn nhập biên bản = end_date + 1 ngày) và `completeBlockedReason()` (chưa tới giờ bắt đầu).

⚠️ Ghi chú tồn đọng: docblock `notifyMeetingEmployees()` (dòng ~1868) và `buildMeetingNotificationContent()`
(dòng ~1916) vẫn ghi "nhiệm vụ giao từ biên bản dùng [BBH]", trong khi commit `ac48f36f2` (12/09) đã đổi
lời gọi sang `[MET]`. Comment lạc hậu, chưa sửa vì ngoài phạm vi yêu cầu.

### Kiểm chứng vòng 3 — Playwright, bấm tay trên giao diện thật (2026-09-14)
Phạm vi an toàn user chốt: meeting test có **duy nhất tài khoản đang đăng nhập** (DNS Admin, employee 13,
employee_info 6) vừa là thành phần, vừa là người đề xuất, vừa là người thực hiện → không đồng nghiệp nào
bị bắn push. Xong thì xoá sạch.

Luồng: `/assign/meeting/create` → điền form (Họp nội bộ · Meeting nội bộ · Trực tiếp · bắt đầu +2 phút) →
tab Biên bản thêm 1 dòng (đề xuất = thực hiện = DNS Admin, hạn 17/09) → **Lưu và Chốt lịch** → đợi qua giờ
bắt đầu → mở `/52/edit` → Điểm danh nhanh: Tất cả có mặt → **Hoàn thành**.

| Mốc | Thông báo mời họp | Thông báo giao nhiệm vụ |
| --- | --- | --- |
| Trước khi tạo | — | 2 (dữ liệu cũ) |
| Sau **Lưu và Chốt lịch** | **+1** `[MET]: <b>[TEST 14/09]…</b>. Thời gian (…) Địa điểm: …` | **+0** ✅ |
| Sau **Hoàn thành** | +0 | **+1** `[MET] Tạo mới: <b>[TEST 14/09]…</b>. Bạn được giao 1 nhiệm vụ.` ✅ |

Chỉ **1** thông báo dù kiêm cả 2 vai (đề xuất + thực hiện) → gộp trùng chạy đúng.
Ảnh màn Thông báo: `.plans/redmine-11044-meeting-chon-nhan-su/screenshots/2026-09-14-thong-bao-sau-hoan-thanh.png`
— trong ảnh thấy rõ 2 dòng mới dùng `[MET]`, còn các dòng cũ ngày 12/09 vẫn là `[BBH]` và `[Meeting]`
(bằng chứng cho cả 2 lần đổi tiền tố).

**Dọn dẹp đã làm:** xoá meeting #52 + 1 thành viên + 1 dòng biên bản + 1 người thực hiện + 2 dòng
`meeting_history` + 2 thông báo. Đối chiếu lại: `notifications` toàn hệ thống 11 dòng đúng như trước test,
không còn bản ghi nào chứa `[TEST 14/09]`.
