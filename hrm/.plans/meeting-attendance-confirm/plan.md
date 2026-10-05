# Plan — Xác nhận tham dự trước cuộc họp (Redmine #11369)

Nhánh: `task_11369` (tách từ `tpe`) ở cả `hrm-api` và `hrm-client`.

## Phase 1 — Backend

- [x] `Meeting::canConfirmAttendance()` + `attendanceConfirmMember()` — điều kiện trạng thái + thời gian + là khách mời nội bộ
- [x] `MeetingService::confirmAttendance()` — validate + ghi `attendance_status` / `attendance_note` + ghi lịch sử
- [x] `MeetingController::confirmAttendance()` + route `POST v1/assign/meeting/{id}/attendance-confirm`
- [x] `MeetingTransformer` trả khối `attendance_confirm` (can_confirm / my_status / my_note / locked_reason)
- [x] `MeetingService::sendMeetingNotification()` gắn thêm `attendance_confirm`, `meeting_id`, `start_date` vào payload thông báo Lên lịch / Chốt lịch

## Phase 2 — Frontend màn chi tiết

- [x] Component dùng chung `components/assign/MeetingAttendanceConfirm.vue` (2 nút + badge + popup lý do)
- [x] Thêm 2 prop tùy chọn `required-input` / `input-required-message` cho `components/modal/base-confirm-modal.vue`
- [x] Nhúng vào `MeetingForm.vue` ngay dưới thanh trạng thái, chỉ hiện ở chế độ xem chi tiết
- [x] Cập nhật lại dòng của chính mình trong tab Điểm danh sau khi xác nhận (không phải F5)

## Phase 3 — Frontend thông báo chuông

- [x] `BasicSubsystem.vue`: render `MeetingAttendanceConfirm` (chế độ gọn) cho thông báo `type = meeting` có cờ `attendance_confirm`
- [x] Bấm nút không được kích hoạt `markAsRead` → điều hướng (chặn nổi bọt sự kiện)

## Phase 4 — Verify

- [x] AC1-AC5 trên môi trường local (FE :3005 → API :8002 → DB `hrm_prod_30_3_26`)

## Checkpoint — 2026-09-11

Vừa hoàn thành: BE + FE đủ 3 phase. Đã verify BE end-to-end trên DB `hrm_prod_30_3_26` (API :8002):
- AC1 người ngoài danh sách → 403 kèm message
- AC3 meeting đã qua giờ bắt đầu → chặn, báo quyền chốt điểm danh thuộc người chủ trì
- AC4 meeting Hoàn thành → chặn
- Lý do vắng để trống → 400 "Vui lòng nhập lý do vắng mặt"; chọn `attendance_status = 3` → 400
- Báo vắng rồi đổi ý sang Có mặt → lý do cũ bị xoá sạch
- `MeetingTransformer` trả đúng khối `attendance_confirm`

Đang làm dở: verify UI bằng Playwright trên FE :3005.
Bước tiếp theo: chạy AC2 + AC5 trên giao diện, sau đó commit.
Blocked: 
## Checkpoint — 2026-09-11 (2)

Vừa hoàn thành: **XONG toàn bộ, đã verify AC1-AC5 trên giao diện thật.**
- AC2: popup lý do để trống → viền đỏ + "Vui lòng nhập lý do vắng mặt", popup KHÔNG đóng; nhập lý do → lưu, badge đổi ngay
- AC5: tab Điểm danh nhận đúng trạng thái + lý do mà không phải tải lại trang
- Chuông: 2 nút hiện trên dòng thông báo meeting, bấm không điều hướng, toast "Xác nhận tham dự thành công"
- Bấm ở chuông thì badge + tab Điểm danh ở màn chi tiết đổi theo (đồng bộ qua `$root` event)

Phát sinh ngoài plan: `Modules/Timesheet/Services/EmployeeInfoService::sendNotification()` **lọc trắng
danh sách khoá** của payload thông báo nên dữ liệu kèm bị rụng im lặng. Đã thêm 1 nhánh additive
(chỉ chạy khi có cờ `attendance_confirm`) — đây là hàm dùng chung của MỌI phân hệ, nhưng không
sửa thì không cách nào đưa được dữ liệu ra chuông.

Dữ liệu test đã trả về nguyên trạng: meeting 54 về giờ cũ, điểm danh về 0, xoá 5 thông báo test.

Bước tiếp theo: commit 2 repo, cập nhật Redmine #11369.
Blocked: 

## Phase 4 — QA vòng 1 (Redmine #11369, 2026-09-12)

- [x] Lỗi 1 + 3b — "xác nhận rồi vẫn hiện 2 nút": **KHÔNG sửa**. Spec ghi *"Cho phép user thay đổi
      lại lựa chọn trước thời hạn khóa"* → 2 nút phải ở lại sau khi chọn (user chốt lại 2026-09-12).
- [x] Lỗi 2 — bấm [Có mặt] thì panel thông báo ở chuông vẫn mở, bấm [Vắng có lý do] lại đóng.
      Nguyên nhân: popup lý do được `b-modal` đưa ra ngoài DOM của panel → `b-nav-item-dropdown`
      tưởng user click ra ngoài rồi tự đóng.
      Sửa: `MeetingAttendanceConfirm` bắn `@modal-toggle` (nghe `bv::modal::shown|hidden` đúng
      `modalId` của mình); `BasicSubsystem` giữ cờ `keepNotiDropdownOpen` và `preventDefault()`
      sự kiện `@hide` của dropdown, nhả cờ sau 300ms để nuốt luôn cú click đóng popup.
- [x] Lỗi 3a — thanh "Xác nhận tham dự" ở màn chi tiết quá cao (gần bằng thanh trạng thái).
      Nút `V2BaseButton` đổi `size="sm"` (32px) → `xs` (24px), icon 15px → 13px, badge `sm` → `xs`,
      padding thanh `0.5rem 0.75rem` → `0.25rem 0.5rem`, margin-bottom `0.75rem` → `0.5rem`.
- Làm trên git worktree riêng `../wt-11369-client` (nhánh `task_11369`) vì checkout chính đang
  dở task_11145. FE dev của worktree chạy port 3006 để không đụng :3005 đang chạy.

### Checkpoint — 2026-09-12

Vừa hoàn thành: **XONG** — sửa lỗi 2 + 3a, verify trên giao diện thật, commit `d003f860e`
(hrm-client, nhánh `task_11369`). Lỗi 1/3b kết luận không sửa (đúng spec).
Kết quả verify (FE :3006 → API :8003, đều là worktree riêng, không đụng :3005/:8002 đang chạy):
- Chuông, nút [Vắng có lý do]: panel mở suốt lúc popup hiện; bấm Hủy panel vẫn mở; bấm Xác nhận
  → badge "Đã báo: Vắng có lý do - …", thanh ở màn chi tiết đổi theo, panel vẫn mở.
- Chuông, nút [Có mặt]: panel vẫn mở, badge "Đã xác nhận: Có mặt", không điều hướng.
- Thanh màn chi tiết: cao **35px** (trước ~58px), nút 24px — thấp hơn hẳn thanh trạng thái (~60px).

⚠️ Dữ liệu test còn sót: meeting 54 (`TPE.MET.KH.26.0050`) có `attendance_status = 1` (Có mặt)
của employee 13 — giao diện KHÔNG có đường đưa về "Chưa điểm danh" (chip không bỏ chọn được),
chưa đụng DB vì chưa được phép. Muốn sạch thì chạy:
`UPDATE meeting_employees SET attendance_status = 0, attendance_note = NULL WHERE meeting_id = 54 AND employee_id = 13;`
Thời gian họp đã trả đúng về 11/09/2026 15:25–16:25.

Ghi nhận ngoài phạm vi: thông báo **"[MET] Thay đổi lịch"** (`notifyMeetingChanges`) KHÔNG kèm cờ
`attendance_confirm` nên không có cụm nút — chỉ thông báo Lên lịch / Chốt lịch mới có. Nếu nghiệp vụ
muốn đổi lịch cũng phải xác nhận lại thì phải bổ sung, chưa làm vì ngoài 3 lỗi QA báo.

Bước tiếp theo: merge `task_11369` về `tpe-develop-assign` (cả 2 repo) khi QA duyệt.
Blocked: 

## Phase 5 — QA vòng 2: cỡ chữ + canh dọc thanh xác nhận (2026-09-12)

- [x] Chữ trong cụm mỗi chỗ một cỡ (nhãn `0.8rem` = 12.8px, nút xs 12px, badge xs 11px) và các
      thành phần không nằm trên cùng một đường.
      Sửa: cả cụm về **12px**; nhãn / badge / nút ép cùng `height: 24px` + `line-height: 1`, bọc
      trong flex `align-items: center` thay vì để baseline tự quyết. Badge xs ép `padding: 0 10px`
      (mặc định `4px 8px` làm chiều cao lệch). Icon trong nhãn và 2 nút 13px → 12px.
      Đo thật: nhãn/badge/2 nút đều `height 24px`, `top 161.1px`, tâm `173.1px` — trùng khít.
      Thanh cao **33px**. Commit `141586a95`.

### Checkpoint — 2026-09-12 (2)

Vừa hoàn thành: QA vòng 2 — cỡ chữ đồng đều + canh giữa theo chiều dọc, đã đo trên giao diện thật.
Đang làm dở: không.
Bước tiếp theo: chờ QA duyệt rồi merge `task_11369` về `tpe-develop-assign` (cả 2 repo).
Blocked: 

## Phase 6 — Ẩn nút của lựa chọn đang áp dụng (2026-09-12)

- [x] QA: bấm [Có mặt] rồi mà nút [Có mặt] vẫn bấm được → spam vào thứ không đổi gì.
      Sửa: ẩn nút của lựa chọn ĐANG áp dụng, giữ nút còn lại (spec cho đổi lại trước hạn khoá).
      `status = 1` → chỉ còn [Vắng có lý do]; `status = 2` → chỉ còn [Có mặt];
      chưa phản hồi hoặc bị chủ trì đánh Vắng không lý do (3) → hiện cả 2.
      **Ẩn chứ không disable** — user chọn phương án này 12/09/2026 sau khi cân với quy ước
      "nút không dùng được thì ẩn hẳn"; nút xám đọc thành "không có quyền", trong khi đây là
      lựa chọn hiện tại của chính user và badge đã nói rõ trạng thái.
      ⚠️ Đánh đổi đã chốt: đang ở trạng thái Vắng thì **không sửa được riêng lý do** — phải chọn
      [Có mặt] rồi báo vắng lại. Nếu sau này QA thấy vướng thì cân nhắc cho bấm vào badge để sửa.
      Verify 3 trạng thái trên giao diện thật, DB ghi đúng. Commit `18e07ff95`.

### Checkpoint — 2026-09-12 (3)

Vừa hoàn thành: ẩn nút của lựa chọn đang áp dụng; verify đủ 2 chiều Có mặt ⇄ Vắng có lý do.
Đang làm dở: không.
Bước tiếp theo: chờ QA duyệt rồi merge `task_11369` về `tpe-develop-assign` (cả 2 repo).
Blocked: 

## Phase 7 — Icon bút sửa riêng lý do vắng (2026-09-12)

- [x] Bỏ đánh đổi của Phase 6: khi `attendance_status = 2`, cạnh badge có nút vuông 24×24
      `ri-edit-line` (`V2BaseButton tertiary status=warning size=xs square`) — bấm mở lại popup
      "Báo vắng mặt cuộc họp" đã điền sẵn lý do cũ. Chỉ hiện ở trạng thái Vắng.
      Vì sao icon bút mà không phải bấm cả badge: badge không có dấu hiệu bấm được, user không
      đoán ra. Vì sao `ri-edit-line`: icon Sửa đang dùng 68 chỗ trong project (so với 7 chỗ
      `ri-pencil-line`) — theo quy ước rà project trước khi tự nghĩ kiểu mới.
      Verify: trạng thái Có mặt không có icon; báo vắng → icon hiện, cùng `top` với nút kia, thanh
      vẫn 33px; bấm icon → popup fill sẵn lý do cũ, sửa xong DB ghi đúng `attendance_note`,
      `attendance_status` giữ = 2. Commit `8aadab021`.
- Ở chuông (chế độ `compact`) mọi thay đổi Phase 6 + 7 dùng CHUNG component nên tự có, nhưng chỉ
  hiện **sau khi user bấm ngay trên dòng thông báo đó** — thông báo không mang theo trạng thái
  phản hồi hiện tại (`showBadge = !compact || touched`), nên lúc mới mở chuông vẫn là 2 nút,
  chưa có badge và icon bút. Muốn chuông biết trạng thái ngay từ đầu thì phải cho BE trả kèm,
  nhưng thông báo lưu lúc gửi → dữ liệu sẽ cũ; chưa làm.

### Checkpoint — 2026-09-12 (4)

Vừa hoàn thành: icon bút sửa lý do vắng, đã verify trên giao diện thật.
Đang làm dở: không.
Bước tiếp theo: chờ QA duyệt rồi merge `task_11369` về `tpe-develop-assign` (cả 2 repo).
Blocked: 

## Phase 8 — Chuông biết trạng thái ngay từ lúc mở (2026-09-12)

- [x] **BE** `GET assign/meeting/attendance-confirm-states?meeting_ids=1,2,3` — trạng thái xác nhận
      của CHÍNH user cho nhiều meeting, trần 50 id, đặt TRƯỚC route wildcard `{id}`.
      `Meeting::attendanceConfirmState()` chuyển từ helper private của `MeetingTransformer` lên
      Entity để màn chi tiết + chuông dùng chung (output không đổi);
      `Meeting::preloadMyCompanyMember()` nạp dòng điểm danh bằng 1 query, tránh N+1.
      Commit `ae1136682`.
- [x] **FE** panel chuông gọi endpoint trên **1 lần lúc `@shown`** (lazy, không gọi ở `mounted`,
      không gọi theo từng dòng); prop mới `status-known` để compact chỉ hiện badge khi đã tra được.
      Request lỗi → im lặng, quay về hành vi cũ (hiện 2 nút). Commit `17e9f6883`.
- [x] Badge trong chuông lệch dọc + chữ 13px: theme `assets/scss/custom/structure/_topbar.scss` có
      `.notification-list .notify-item .notify-details span { display: block; font-size: 13px }`,
      badge là `<span>` nên bị ép `display:block`, mất `align-items:center` → chữ dính mép trên.
      **Không sửa theme** (file dùng chung), ghi đè tại component bằng `.v2-badge.ac-badge`
      (2 class mới thắng được selector 3 class của theme). Lý do dài thì cắt "…" + `title`.

### Checkpoint — 2026-09-12 (5)

Vừa hoàn thành: chuông biết trạng thái ngay khi mở (BE + FE), sửa badge lệch trong chuông.
Verify: mở chuông chưa bấm gì đã hiện đúng badge + ẩn đúng nút; đúng 1 request cho mọi dòng;
badge và nút cùng height 24 / top 162.7 / font 12px.
Đang làm dở: không.
Bước tiếp theo: chờ QA duyệt rồi merge `task_11369` về `tpe-develop-assign` (cả 2 repo).
Blocked: 

## Phase 9 — Test case cho QA (2026-09-14)

- [x] 9.1 `gen_testcase.py` + `testcase.xlsx` — 67 TC / 9 section La Mã + 6 TC phân quyền & truy cập
      (gồm 3 ca gọi thẳng chức năng bỏ qua giao diện), P0 58%. Bộ kiểm tra thuật ngữ in "OK - sach".
- [x] 9.2 Phủ đủ các điểm QA từng bắt lỗi: bảng thông báo không được đóng khi bấm nút, ẩn nút của
      lựa chọn đang áp dụng, icon bút sửa riêng lý do, chuông biết trạng thái ngay khi mở, canh dọc
      + cỡ chữ của thanh xác nhận.
- [x] 9.3 Ghi nhận là hành vi ĐÚNG (không phải lỗi): thông báo "Thay đổi lịch" không kèm cụm nút.
