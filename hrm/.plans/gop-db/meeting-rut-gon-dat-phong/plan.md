# Plan — Rút gọn đường đặt phòng khi tạo meeting

User cho "làm" 01/11/2026 — phạm vi: TPE_APP develop + hrm-client gop_db, không BE, không DB, không commit.

## App (TPE_APP develop)
- [x] C: ô Phòng họp ở form tạo — đếm phòng trống theo giờ + chọn phòng dự kiến (`_PlannedRoomPanel` trong meeting_room_box.dart)
- [x] Giữ phòng dự kiến trong lượt tạo (`plannedRoomOf` Expando → `meetingPlannedRooms[id]`)
- [x] A: Hub — Lên lịch xong hỏi "Đặt phòng cho cuộc họp này?" [Đặt phòng][Để sau] → form đặt phòng (chọn sẵn phòng dự kiến)
- [x] B: Hub — dòng "Phòng họp · Chưa đăng ký · Đăng ký" (ẩn khi đã giữ phòng vì đầu Hub đã có dải phòng)
- [x] (user bổ sung giữa chừng) Gợi ý phòng như popup web: `RoomFreeSuggestions` (room_picker_sheet.dart) — "Phòng còn trống (N)" tối đa 5, hết phòng → khe trống gần nhất (+ "Đổi giờ" ở hướng Nhu cầu khác); gắn vào form Đăng ký phòng + khối phòng dự kiến
- [x] analyze (0 lỗi) + bấm thử simulator tpeDev: đếm 2/2, chọn dự kiến VIP1, Lên lịch → hộp hỏi, Để sau → dòng Hub → form chọn sẵn VIP1, bấm gợi ý đổi sang tầng 3 → gửi → Đã duyệt + push; nhánh Đặt phòng không dự kiến. Đã huỷ 2264/2265 trên dev

## Web (hrm-client gop_db)
- [x] BookingFormModal: prop tuỳ chọn `presetRoomId`
- [x] GeneralInfo: C (đếm phòng trống + gợi ý + chọn dự kiến) ở form tạo/nháp; B nút ở màn Xem; `offerRoomBooking()`
- [x] create/edit: A sau "Lưu và Lên lịch" (web dùng nút "Đóng" theo button-convention, không có "Để sau")
- [x] Playwright (client local trỏ API dev — API local gop_db lỗi 500 thiếu bảng `permission_aliases` của rbac, chưa migrate): C đếm "Còn 2/2", gợi ý 2 phòng, chọn VIP1 dự kiến; A hỏi sau Lưu và Lên lịch (có / không phòng dự kiến) → popup chọn sẵn VIP1 (presetRoomId=1, data.meeting_room_id=1); Đóng → về danh sách; B nút ở màn Xem → đặt tầng 3 → khối phòng cập nhật, nút ẩn. Console: không lỗi mới (chỉ cảnh báo hasCustomer có sẵn). Đã huỷ 2318/2319 trên dev
- [x] e2e `tests/meeting/meeting-room-sync.spec.ts`: sửa P4UI-1 (nháp hiện khối phòng dự kiến thay câu cũ), thêm P4UI-5 (A+C) và P4UI-6 (B); tsc sạch, CHƯA chạy (chờ user yêu cầu + DB local cần migrate rbac)

### Checkpoint — 01/11/2026 23:00
Vừa hoàn thành: A/B/C app + web + gợi ý phòng như popup web trên app; kiểm simulator + Playwright
Đang làm dở: —
Bước tiếp theo: user xem; khi muốn chạy e2e thì DB local cần bảng permission_aliases (migration rbac) — hỏi trước
Blocked: —

## Fix 10/11/2026 — đặt phòng trên form meeting (user cho "làm": hrm-client gop_db, chỉ GeneralInfo.vue + spec e2e, không BE)
- [x] Đổi giờ → phòng dự kiến (nháp/tạo) hiện tình trạng theo giờ mới (trống / chờ duyệt / bận / ngoài giờ)
- [x] Đổi giờ ở cuộc họp đang giữ phòng (Lên lịch) → gọi availability (exclude_booking_id) báo phòng đang giữ còn trống / bận / phải duyệt lại theo giờ mới
- [x] Giờ quá khứ báo đỏ ngay dưới ô Bắt đầu / Kết thúc — khớp luật BE (tạo + Lên lịch so hiện tại; nháp so created_at; không đổi giờ thì không báo)
- [x] Kiểm Playwright (phòng tạm trên db_gop_6_11, xoá sau) + cập nhật spec meeting-room-sync.spec.ts (thêm P4UI-7, P4UI-8; tsc sạch, CHƯA chạy)

### Checkpoint — 10/11/2026
Vừa hoàn thành: GeneralInfo.vue — `heldRecheck` (đổi giờ khi đang giữ phòng → availability + exclude_booking_id: bận/ngoài giờ = V2BaseError, chờ duyệt = cảnh báo vàng, trống = xanh, phòng cần duyệt báo "lưu xong về Chờ duyệt"); `plannedRoomWarning` (phòng dự kiến bận/chờ duyệt/ngoài giờ/bị bỏ theo giờ mới); `startDateError`/`endDateError` khớp luật BE + `nowTick` 30s; giờ quá khứ thì khối phòng không gợi ý. Kiểm Playwright MCP trên db_gop_6_11 (2 phòng + 2 cuộc họp tạm, đã xoá): đo text + màu DOM cả 4 ca màn Sửa, gõ thật datepicker ở màn Tạo.
Đang làm dở: —
Bước tiếp theo: user kiểm tay → bảo commit; (tuỳ chọn) chạy e2e meeting-room-sync khi user yêu cầu. Chưa chặn bấm Lưu phía FE khi còn lỗi giờ quá khứ (validate() ở MeetingForm.vue đang tắt) — BE vẫn trả 422 đúng ô.
Blocked:

## Fix 10/11/2026 (2) — chặn Lưu phía FE khi còn lỗi giờ/phòng (user cho "làm": hrm-client gop_db, MeetingForm.vue + GeneralInfo.vue + assert e2e P4UI-8)
- [x] GeneralInfo: tách lỗi FE (`clientScheduleErrors()`) khỏi lỗi BE
- [x] MeetingForm.save(): còn lỗi FE → không gọi API, đổ formError + toast chung + nhảy tới ô lỗi (khuôn handleComplete)
- [x] Kiểm Playwright: bấm Lưu nháp với giờ quá khứ → 0 request POST/PUT, lỗi tại ô; spec P4UI-8 thêm assert

### Checkpoint — 10/11/2026 (2)
Vừa hoàn thành: MeetingForm.save() → blockOnClientScheduleErrors(): còn lỗi giờ quá khứ / phòng đang giữ bị trùng-ngoài giờ thì không gọi API, lỗi giờ vào formError (tự gỡ khi sửa), lỗi phòng chỉ hiện ở khối kiểm lại, toast chung, kéo về tab Thông tin + cuộn tới lỗi. Kiểm Playwright MCP: màn Tạo (Lưu nháp + Lưu và Lên lịch → 0 request ghi, sửa giờ → formError rỗng, cờ tab tắt); màn Sửa ca phòng bận bằng giả lập phản hồi API trên cuộc họp 3061 (chặn PUT/POST ở trình duyệt, DB không đổi). Spec P4UI-8 thêm assert "không gửi request"; tsc sạch, CHƯA chạy.
Đang làm dở: —
Bước tiếp theo: ĐÃ COMMIT + PUSH 10/11 hrm-client gop_db `830631cb6` (không BE, không migration). Còn: deploy client; chạy e2e meeting-room-sync khi user yêu cầu.
Blocked:

## Fix 12/11/2026 — LỖI PROD: tạo meeting không hiện đủ danh sách phòng để chọn (user cho "làm": hrm-client, nhánh `gop_db-fix-meeting-ds-phong` tách từ origin/gop_db, worktree `websites/wt-fix-meeting-ds-phong/hrm-client`)
Gốc lỗi: `GeneralInfo.vue` `roomPlanSuggestions` cắt `.slice(0, 5)` — khối "Phòng còn trống" là chỗ DUY NHẤT chọn phòng dự kiến ở form Tạo/nháp ⇒ phòng thứ 6+ không chọn được (BE `availabilityForSlot` trả đủ). Tiêu đề "(5)" lệch dòng "Còn N/M".
User chốt: hiển thị đủ phòng, dạng BẢNG CHỌN, cảnh báo phòng có phiếu chờ duyệt trùng giờ.
- [x] Bảng chọn (style MISA `_misa-grid.scss`, bám `.ppp-table`): cột chọn · Phòng · Sức chứa · Duyệt phòng · Tình trạng; cuộn trong khối max 296px, header sticky
- [x] Thứ tự Trống → Chờ duyệt → Ngoài giờ → Đã có lịch; chọn được Trống + Chờ duyệt (cảnh báo vàng + tên cuộc họp/người đặt); Bận/Ngoài giờ ẩn ô chọn, bận kèm "Trống gần nhất"
- [x] Bỏ `roomPlanSuggestions` / `roomPlanAltSlots` + CSS `.free-room-*` / `.alt-slot-item` (khe trống gần nhất nay nằm trên dòng phòng bận)
- [x] Playwright: chặn availability 12 phòng — đủ 12 dòng, chọn phòng thứ 8 được, phòng chờ duyệt cảnh báo, bận/ngoài giờ không chọn được, icon #1abc9c, 0 lỗi console
- [x] e2e `meeting-room-sync.spec.ts`: P4UI-5/P4UI-8 đổi selector sang bảng, thêm P4UI-9 (12 phòng chặn API); P4UI-8 bước "giờ quá khứ" đổi hôm qua → 00:00 hôm nay (picker khoá ngày trước hôm nay — ca chưa từng chạy). Chạy toàn spec: 10/10 passed

### Checkpoint — 2026-11-12
Vừa hoàn thành: fix + kiểm Playwright + e2e 10/10 trên worktree (Nuxt cổng 57665, API :8000)
Đang làm dở: —
Đã commit `f424d46b1` + push fast-forward lên origin/gop_db (12/11/2026, user yêu cầu). 12/11/2026 09:31 đã build prod TPE bằng `~/build_tpe.sh` (api 5d13365e3, client f424d46b1; không migration, catalog 0 thay đổi; bản build có `meeting-room-plan-table`). Bước tiếp theo: user kiểm form Tạo meeting trên prod
Blocked:

## Fix 12/11/2026 (2) — LỖI PROD: Hoàn thành meeting có phòng báo "Không thể đặt phòng cho thời điểm đã qua" (user cho "làm": hrm-api, nhánh `gop_db-fix-meeting-hoan-thanh-phong`, worktree `websites/wt-fix-meeting-hoan-thanh-phong/hrm-api`)
Gốc: `MeetingRoomBookingSyncService::ROOM_FIELDS` chứa `status` ⇒ Hoàn thành / Chốt lịch (chỉ đổi status) chạy lại `validateBookingRules()` ⇒ luật quá khứ chặn (sau giờ bắt đầu).
- [x] Bỏ `status` khỏi ROOM_FIELDS (Hủy vẫn qua `meetingHoldsRoom()`, phiếu chưa có/đã chết vẫn kiểm nhờ `$aboutToHoldRoom`)
- [x] PHPUnit `tests/Feature/MeetingCompleteKeepsRoomTest.php` (3 ca, transaction rollBack): đỏ 2/3 trên code cũ (tái hiện đúng lỗi), xanh 3/3 sau sửa; Unit `MeetingRoomBookingSyncRuleTest` 8/8 (sửa thêm ca Online lỗi thời từ Task 75)
- [x] e2e `meeting-room-sync` (client :3062 + API :8062): P4UI-1 đỏ 3 lần do popup nhận 0 phòng (nghi phiên khác chạy e2e cùng tài khoản đổi công ty — CHƯA chứng minh), lần chạy có probe bookable trả 5 phòng thì xanh với bản sửa; user dừng e2e, cho push
- [x] Commit `e674367d1`, push fast-forward origin/gop_db
- Tồn: kéo dài giờ Kết thúc cuộc họp đang diễn ra vẫn bị luật "thời điểm đã qua" chặn (start đã qua) — chờ user quyết
- Tồn: `tests/Feature/MeetingRoomBookingRaceTest.php` hỏng sẵn (insert cột `code` đã bỏ ở Task 44)

### Checkpoint — 12/11/2026 (wrap up)
Vừa hoàn thành: Fix (2) commit `e674367d1` + push fast-forward origin/gop_db (hrm-api); PHPUnit Feature 3/3 + Unit 8/8. e2e dừng giữa chừng theo yêu cầu user
Đang làm dở: — (prod CHƯA có e674367d1; client f424d46b1 đã lên prod 09:31)
Bước tiếp theo: hỏi user build prod TPE bằng `~/build_tpe.sh` (chỉ 1 commit api, không migration); dọn API :8062 + Nuxt :3062 (worktree wt-fix-meeting-ds-phong, `.env` đang trỏ BASE_API_URL :8062) + xoá 2 worktree `wt-fix-meeting-ds-phong`, `wt-fix-meeting-hoan-thanh-phong`
Blocked: kéo dài giờ Kết thúc cuộc họp đang diễn ra — chờ user quyết có sửa không
