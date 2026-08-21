# SDD ledger — plan: .plans/lich-meeting-tab/plan.md

Branch: meeting-schedule (api + client). KHÔNG commit git (theo CLAUDE.md) → review qua working-tree diff.
BASE api=78bc26ccf · client=b1cd90762 (giữ nguyên, không commit).

## Tiến độ
- Task P1 (BE endpoint calendar): fix round 1/5 (1 Important + 2 Minor addressed, 0 open). complete — review clean.
  Files (uncommitted): MeetingController.php (calendar()), Routes/Meeting/api.php (route), MeetingCalendarRangeCriteria.php (mới).
  Ghi chú: route:list không chạy được do bug có sẵn Modules/Decision (ngoài phạm vi); chưa test HTTP thật (không có DB/auth env).
- Task P2 (FE tab switcher): complete — review clean (SPEC ✅, 1 Minor cosmetic indent). CSS xác nhận an toàn khi lồng thêm cấp v-show.
  Files (uncommitted, client): pages/assign/my-todo/index.vue (tab bar + v-show wrapper + activeTab + lazy component + CSS); components/calendar/MeetingCalendarTab.vue (placeholder).

## Right-sizing FE còn lại (gộp Phase 3-7 plan → 5 đơn vị coherent)
- FE-core: container MeetingCalendarTab (fetch) + calendar-lanes.js + MonthGrid + MeetingCard + MeetingMultiDayBar (lịch Tháng chạy data thật). [tương ứng plan Task 3.1,3.2,4.1,4.2,4.3]
- FE-week: WeekGrid. [Task 5.1]
- FE-chrome: CalendarHeader + CalendarFilterToolbar + CalendarSummaryBar + nối vào container. [Task 6.1-6.3]
- FE-detail: MeetingDetailDrawer + DayMeetingsPopover + nối Sửa/Xem biên bản. [Task 7.1-7.3]
- FE-polish: style bám mockup + regression todo. [Task 8.1-8.2]
Interface chốt: tuần bắt đầu THỨ 2; period label Tháng "Tháng M/YYYY", Tuần "DD–DD/MM/YYYY"; fetch range Tháng = trọn lưới 6 tuần (Mon tuần chứa ngày 1 .. Sun tuần chứa ngày cuối); summary đếm chỉ meeting trong [ngày1..ngày cuối tháng].

- Task FE-core (container + MonthGrid + card + lanes + status): complete — fix round 1 (1 Important fetchRange lệch lưới 6 hàng + 2 Minor dedupe helper/dùng cardStatusStyle → ADDRESSED, re-review clean).
  Files (uncommitted, client, components/calendar/): calendar-status.js, calendar-lanes.js (export mondayOf/monthGridStart), MeetingCard.vue, MeetingMultiDayBar.vue, MonthGrid.vue, MeetingCalendarTab.vue (thay ruột).
  CHỐT interface: fetchRange month = monthGridStart(cursor) .. +41 ngày (khớp MonthGrid 6 hàng cố định). container: view/cursorDate/filters/meetings/loading/meetingTypes/selectedMeetingId/showDrawer/popover; methods fetchMeetings/loadMeetingTypes/setView/goPrev/goNext/goToday/onClickMeeting(meeting,evt)/onClickMore(date,evt,dayMeetings). MonthGrid emit click-meeting(meeting,$event)/click-more(dateStr,$event,dayMeetings). Ghi chú: `?.` optional chaining lỗi trên node --check Node12 nhưng Nuxt/babel OK (pattern có ở pages/assign/meeting/index.vue).
  Mockup week = TIME-GRID (giờ 07–18, clamp), không phải list — FE-week port renderWeek đầy đủ.
- Task FE-week (WeekGrid time-grid): complete — review clean (SPEC ✅, Approved). 2 Minor deferred: (1) all-day detect dựa start_date==00:00:00 (meeting nửa đêm thật bị xếp nhầm dải "Cả ngày" — hiếm, không có flag BE); (2) toggle tạm dùng lại class --today (sẽ thay ở FE-chrome).
  Files (uncommitted): WeekGrid.vue (mới), calendar-week-helpers.js (mới), MeetingMultiDayBar.vue (thêm prop colOffset default0 + variant default month, KHÔNG phá month), MeetingCalendarTab.vue (cắm week + toggle tạm).
- Task FE-chrome (CalendarHeader + CalendarFilterToolbar + CalendarSummaryBar + wiring): complete — fix round 1 (1 Critical: status id:0 number bị V2BaseSelect `opt.id||...` nuốt → dùng STRING id '0'..'4' trong MEETING_STATUS_OPTIONS (calendar-status.js) + 1 Minor dedupe → ADDRESSED, re-review clean).
  Files (uncommitted): CalendarHeader.vue, CalendarFilterToolbar.vue, CalendarSummaryBar.vue (mới), calendar-status.js (+MEETING_STATUS_OPTIONS string id), MeetingCalendarTab.vue (xóa nav tạm, bố cục summary→header+filter→grid, computed summaryPeriod/summaryPeriodMeetings/summaryRangeText, onFilterChange/onFilterClear).
  Bỏ filter Thị trường + nút Thêm meeting (ngoài scope). filters.status giờ là string '0'..'4' (BE coerce OK). V2BaseSelect option shape = {id, name}; id status PHẢI string (0 falsy bug).
- FE-detail sắp làm: drawer fetch GET assign/meeting/{id} (MeetingTransformer: content/company_members/customer_members/conclusion/creator/canEdit/cancel_reason...); nút "Sửa" gate canEdit (fail-closed); "Sửa"→router.push /assign/meeting/{id}/edit, "Xem biên bản"→push /assign/meeting/{id}/show (tái dùng, không viết modal). Popover dùng anchor từ $event của click-more.
- Task FE-detail (drawer + popover + wiring edit/report): review clean SPEC ✅ + fail-closed đúng (canEdit=!!(detail&&canEdit===true)); đang fix round 1 (Important XSS online_link javascript: → vá scheme http/https + rel=noopener; Minor reset detail khi đóng).
  Files (uncommitted): MeetingDetailDrawer.vue, DayMeetingsPopover.vue (mới), MeetingCalendarTab.vue (nối drawer/popover + edit/report/close). Endpoint show KHÔNG trả status_name → derive từ MEETING_STATUS_OPTIONS (Number cast). onClickMore param2 = native evt → anchor evt.currentTarget (nút "+N khác" bind trực tiếp).
  Deferred minors (đưa final review triage): (1) label mode "Trực tuyến"(drawer) vs "Online"(meeting/index.vue) cho mode_id=2 — copy lệch; (2) DayMeetingsPopover không reposition khi resize/scroll window.
  Task FE-detail: complete — fix round 1 (Important XSS online_link + Minor reset detail) ADDRESSED, re-review clean. safeOnlineLink chỉ cho http/https/`//`; detail null-hoá tường minh; canEdit fail-closed nguyên vẹn.

## TẤT CẢ TASK IMPLEMENTATION XONG (2026-08-14)
BE: endpoint calendar. FE: tab switcher + MonthGrid + WeekGrid + header/filter/summary + drawer/popover.

## FINAL WHOLE-BRANCH REVIEW — clean (2026-08-14)
Không Critical/merge-blocking. Fix wave cuối (1 Important + 1 Minor) ADDRESSED, re-review clean:
- Fix Important: summaryPeriodMeetings đổi sang OVERLAP (khớp lưới; meeting multi-day carry-in nay được đếm). SummaryBar.safeMeetings chỉ lọc null (không lọc lại kỳ) → fix hiệu lực.
- Fix Minor: MEETING_STATUS_OPTIONS[4] 'Huỷ'→'Hủy' khớp BE + card status_name.
Deferred (KHÔNG block, để polish sau): (1) label mode "Trực tuyến"(drawer) vs "Online"(meeting/index.vue); (2) DayMeetingsPopover không reposition khi resize window.
Contract BE↔FE khớp; fail-closed (canEdit) + XSS online_link đã vá; regression tab todo an toàn (chỉ v-show wrapper); grep `can*=true` = 0 hit.

## PLAYWRIGHT VERIFY — PASS (2026-08-14, data thật, user DNS Admin)
Phải RESTART Nuxt dev server trước: manifest .nuxt/components stale sau khi checkout gop_db→meeting-schedule (liệt kê subsystems.js/finance/sale-hub không tồn tại → cả app không compile). Kill node cũ + `rm -rf .nuxt/components` + start lại node12 heap8192 → clean.
Kết quả verify:
- Tab switcher OK (2 tab, todo tab nguyên vẹn). BE endpoint calendar 200, 12–28 meeting đúng payload.
- View Tháng: lưới 6 hàng, thẻ màu theo status (Hoàn thành xanh lá/Chốt lịch xanh dương/Lên lịch xám), spillover mờ, CN đỏ, "+N khác" OK.
- View Tuần: time-grid giờ 07–17, thẻ đúng, toggle OK.
- Summary đếm theo kỳ đúng (Th8=0 vì data toàn Th7; Th7=28: LL7/CL13/HT7/Hủy1). Nhãn "Hủy" khớp BE.
- Drawer: fetch show OK, header+body đầy đủ (loại/hình thức/địa điểm/thành phần), FAIL-CLOSED đúng (meeting Hoàn thành → nút "Sửa" ẩn, chỉ hiện "Xem biên bản").
- Filter Loại meeting + Trạng thái đổ options thật. Nav prev/next/today OK.
Anomaly nhỏ: lần click tab ĐẦU TIÊN có nhảy /meeting/35/show (không tái hiện lần sau) — theo dõi thêm, chưa xác định nguyên nhân, không phải lỗi hệ thống.
Screenshots: ERP-HRM/.playwright-mcp/cal-month.png · cal-week.png

## CÒN LẠI (không code được headless)
- Visual pass + test data thật: user build client (node12 + heap8192) + api (php7.4 artisan serve) → mở /assign/my-todo tab "Lịch meeting" duyệt mắt Tháng/Tuần/drawer/popover/filter + test quyền (có/không canEdit).
- KHÔNG commit git (chờ user yêu cầu).
