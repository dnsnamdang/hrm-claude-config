# Tab "Lịch meeting" trong màn Todo — Implementation Plan

> **Cho agentic worker:** thực thi theo từng Phase → Task. Đánh `[x]` khi xong mỗi task. KHÔNG commit/push git khi chưa được yêu cầu (theo CLAUDE.md HRM).

**Goal:** Thêm tab "📅 Lịch meeting" vào màn Todo cá nhân (`pages/assign/my-todo/index.vue`), chia màn thành 2 tab, giữ nguyên tab "✅ Công việc của tôi".

**Architecture:** BE thêm 1 endpoint đọc gọn `GET assign/meeting/calendar` (không phân trang, tái dùng scoping `MeetingCriteria`, lọc overlap khoảng ngày). FE bọc nội dung my-todo trong tab switcher (`v-show`) + thêm cây component `components/calendar/` render lịch Tháng/Tuần, bám mockup.

**Tech Stack:** Laravel 8 (Modules/Assign) · Nuxt 2 / Vue 2 · Bootstrap-Vue · dayjs · Remix Icon · V2Base components.

Người phụ trách: @dnsnamdang · Branch: `meeting-schedule` (api + client)
Spec: `docs/superpowers/specs/2026-08-14-lich-meeting-tab-design.md` · Design: `design.md`
Mockup: `.plans/gop-db/ke-hoach-phat-trien-thi-truong/ke-hoach-phat-trien-thi-truong-mockup-meeting.html`

## Phase 9 — Fix lỗi feature (2026-08-15)

- [x] **9.1 Điều tra anomaly click tab đầu → /meeting/35/show**: KẾT LUẬN = test artifact (accessibility ref stale khi click qua Playwright, trúng nhầm nút "Xem biên bản" lúc drawer mở). Code an toàn: drawer chỉ `emit('view-report')`/`emit('edit')` từ `@click` nút footer (MeetingDetailDrawer.vue:197,207), KHÔNG có auto-emit/watcher/mounted. Không sửa code.
- [x] **9.2 Minor: nhãn hình thức drawer** → đổi "Trực tuyến" (mode_id 2) sang "Online" cho khớp `pages/assign/meeting/index.vue` (mode_id 2 = 'Online'). File: `MeetingDetailDrawer.vue` modeText (dòng ~302-303).
- [x] **9.3 Minor: popover reposition** → `DayMeetingsPopover.vue` thêm listener `scroll`(capture,passive)+`resize` khi show, gọi updatePosition throttle rAF; gỡ khi ẩn/destroy.
- [x] **9.4 Nút "Xem biên bản" mở POPUP biên bản** (không điều hướng /show): tái dùng đúng popup màn meeting — b-modal `calendar-meeting-print-preview-modal` + `openPrintPreview(id)` fetch `assign/meeting/{id}/print` → `printTemplate` (v-html) + nút "In biên bản". `onViewReport`→`openPrintPreview`. Thêm gate `hasMinutes` (chỉ hiện nút khi `detail.reports.length>0`, giống màn meeting list). File: `MeetingCalendarTab.vue` + `MeetingDetailDrawer.vue`.
- [x] **9.5 Verify Playwright**: PASS — click "Xem biên bản" → popup mở (title "Xem biên bản cuộc họp" + spinner), URL KHÔNG đổi (không navigate), gate hasMinutes đúng (chỉ meeting có biên bản mới hiện nút).

- [x] **9.6 Fix "báo lỗi" khi click Xem biên bản** — ROOT CAUSE = DB local `hrm_erp` THIẾU row `print_templates` code `BIEN_BAN_CUOC_HOP` (mẫu in HỆ THỐNG / PROTECTED_CODE, production có) → `MeetingController::print()` `PrintTemplate::where('code',...)->first()` = null → 400 "Trying to get property 'template' of non-object" cho MỌI meeting (ảnh hưởng cả màn meeting list). KHÔNG phải bug code. **Đã seed row này vào DB local qua tinker** (`PrintTemplate::firstOrCreate(code=BIEN_BAN_CUOC_HOP, template wrap {{Ma_Bien_Ban}}/{{Ngay_Lap_Bien_Ban}}/{{NOI_DUNG_CUOC_HOP}})`, id=241). fillReport thay `{{key}}`; NOI_DUNG_CUOC_HOP do BE renderTemplate() sinh nội dung biên bản đầy đủ.
- [x] **9.7 Verify Playwright popup biên bản**: PASS — click "Xem biên bản" → popup mở, `/print` 200, render biên bản THẬT (7926 ký tự: tiêu đề + mã + địa điểm + bảng thành phần tham dự + kết luận), nút "In biên bản", URL không đổi, không toast lỗi. Screenshot `.playwright-mcp/bien-ban-popup.png`.

> Ghi chú: template đã seed là mẫu TỐI THIỂU (wrap nội dung BE render) cho DB LOCAL — production dùng mẫu chính thức. Nếu muốn khớp format production → import mẫu thật từ prod/staging thay row local này.

## Global Constraints

- **KHÔNG** sửa nội dung/logic/method/data của tab "Công việc của tôi" hiện có (chỉ bọc lớp tab).
- Data = scoping `MeetingCriteria` hiện tại (không thêm business rule / permission mới).
- Cờ quyền FE fail-closed (mặc định `false`) — feature này không có cờ quyền mới, nhưng nếu drawer ẩn/hiện nút theo quyền thì tuân thủ.
- Select ngoài modal dùng `V2BaseSelect`; icon dùng SVG/Remix theo convention (lưu ý xung đột codepoint remixicon — ưu tiên SVG tô màu nếu glyph sai).
- Interpolation Vue bình thường (`{{ }}`) — đây là hrm-client (Nuxt), KHÔNG phải AngularJS ERP.
- Không phân trang endpoint calendar; payload chỉ các field trong spec §3.2.

---

## Phase 1 — BE: endpoint calendar

> ✅ TẤT CẢ PHASE ĐÃ HOÀN THÀNH + Playwright verify PASS (xem mục "Trạng thái thực thi" + Checkpoint 2026-08-15 ở cuối file). Các checkbox bước nhỏ bên dưới đánh `[x]` đồng loạt để phản ánh đã xong; nguồn trạng thái chính xác là phần Checkpoint.

> ✅ Phase 1 DONE (2026-08-14) — endpoint + route + MeetingCalendarRangeCriteria. Review clean (fix double-apply criteria).

### Task 1.1: Thêm method `calendar()` vào MeetingController

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingController.php` (thêm method mới, cạnh `index`)
- Modify: `hrm-api/Modules/Assign/Repositories/Criteria/MeetingCriteria.php` (chỉ nếu cần tách nhánh range — xem bước dưới)

**Việc làm:**
- [x] Thêm method:
```php
/**
 * Danh sách meeting cho lịch (không phân trang) — lọc overlap khoảng ngày.
 * Tái dùng scoping quyền của MeetingCriteria (bỏ from_date/to_date của criteria
 * vì đó là lọc "nằm trọn"; lịch cần overlap để lấy meeting nhiều ngày vắt biên kỳ).
 */
public function calendar(Request $request)
{
    $from = $request->input('from_date');
    $to   = $request->input('to_date');

    // Clone request bỏ from_date/to_date để MeetingCriteria không áp lọc "contained"
    $criteriaRequest = clone $request;
    $criteriaRequest->offsetUnset('from_date');
    $criteriaRequest->offsetUnset('to_date');

    $query = $this->repository->with(['meeting_type'])
        ->pushCriteria(new MeetingCriteria($criteriaRequest));

    $models = $query->getQuery(); // lấy Eloquent builder để thêm điều kiện overlap
    // Overlap: start_date <= to AND COALESCE(end_date, start_date) >= from
    if ($from) {
        $models->whereRaw('COALESCE(meetings.end_date, meetings.start_date) >= ?', [$from]);
    }
    if ($to) {
        $models->where('meetings.start_date', '<=', $to);
    }
    $list = $models->orderBy('meetings.start_date', 'asc')->get();

    $data = $list->map(function ($m) {
        $statusName = collect(Meeting::STATUS)->firstWhere('id', $m->status)['name'] ?? '';
        return [
            'id'                => $m->id,
            'name'              => $m->name,
            'code'              => $m->code,
            'meeting_type_id'   => $m->meeting_type_id,
            'meeting_type_name' => $m->meeting_type->name ?? null,
            'status'            => (int) $m->status,
            'status_name'       => $statusName,
            'start_date'        => $m->start_date,
            'end_date'          => $m->end_date,
            'mode_id'           => $m->mode_id,
            'location'          => $m->location,
            'online_link'       => $m->online_link,
            'customer_name'     => $m->customer_name,
        ];
    })->values();

    return $this->responseSuccess($data);
}
```
- [x] Kiểm tra API repository có expose builder đúng cách (`$this->repository->...->getQuery()` hoặc cách tương đương trong prettus repository). Nếu pattern repo khác, thay bằng: build criteria xong gọi `->all()` rồi lọc overlap ở PHP — nhưng ưu tiên lọc ở query. Đọc `MeetingRepository` + cách `index` gọi `apiPaginate` để dùng đúng builder.
- [x] Đảm bảo `use` đủ: `Meeting`, `MeetingCriteria`, `Request`.

**Verify:**
- [x] Chạy artisan route:list lọc meeting sau khi thêm route (Task 1.2) để chắc method resolve.

### Task 1.2: Đăng ký route GET calendar

**Files:**
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (nhóm route `assign/meeting`)

**Việc làm:**
- [x] Tìm nhóm route trỏ tới `MeetingController` (route `assign/meeting` index/show). Thêm **trước** route wildcard `{identifier}` để không bị nuốt:
```php
Route::get('assign/meeting/calendar', [MeetingController::class, 'calendar']);
```
- [x] Đối chiếu route `index` (`GET assign/meeting`): nếu index KHÔNG gắn `checkPermission` thì calendar cũng không gắn (route xem, cùng scoping criteria).

**Verify:**
- [x] `php artisan route:list --path=assign/meeting | grep calendar` → thấy route.
- [x] Gọi thử (Postman/tinker/HTTP) `GET /api/v1/assign/meeting/calendar?from_date=2026-08-01&to_date=2026-08-31` với token user → trả mảng meeting đúng field, đúng phạm vi "của tôi", gồm cả meeting nhiều ngày vắt biên (m09 workshop 27–28/08 phải xuất hiện khi query cả tháng, và khi query tuần chứa 1 trong 2 ngày).

---

## Phase 2 — FE: tab switcher (không đổi tab todo)

### Task 2.1: Bọc nội dung my-todo trong tab switcher

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/index.vue`

**Việc làm:**
- [x] Trong `<template>`: thêm dải nút tab ngay dưới đầu card, TRƯỚC khối stats-row hiện tại. Mẫu markup theo mockup `.view-tabs`:
```html
<div class="mt-view-tabs">
  <button type="button" class="mt-view-tabs__btn" :class="{ active: activeTab === 'mytodo' }" @click="activeTab = 'mytodo'">✅ Công việc của tôi</button>
  <button type="button" class="mt-view-tabs__btn" :class="{ active: activeTab === 'calendar' }" @click="activeTab = 'calendar'">📅 Lịch meeting</button>
</div>
```
- [x] Bọc TOÀN BỘ nội dung todo hiện tại (từ stats-row tới hết các modal của todo) trong `<div v-show="activeTab === 'mytodo'"> ... </div>`. Dùng `v-show` (KHÔNG `v-if`) để giữ nguyên state list/filter/detail khi chuyển tab. KHÔNG sửa gì bên trong.
- [x] Thêm tab calendar sau khối todo:
```html
<div v-if="activeTab === 'calendar'" class="mt-tab-calendar">
  <meeting-calendar-tab />
</div>
```
- [x] Trong `<script>`: thêm `activeTab: 'mytodo'` vào `data()`. Đăng ký component `MeetingCalendarTab: () => import('./components/calendar/MeetingCalendarTab.vue')` (lazy). KHÔNG đụng data/method khác.
- [x] Thêm CSS `.mt-view-tabs` / `.mt-view-tabs__btn` (port từ mockup `.view-tabs` §550–600): dải nút bo tròn, nút active nền teal/đậm.

**Verify:**
- [x] Build/chạy client (node 12 + heap 8192 theo memory), mở màn `/assign/my-todo`: thấy 2 tab; tab "Công việc của tôi" active mặc định, hoạt động y như trước; bấm "Lịch meeting" chuyển sang placeholder calendar; bấm lại "Công việc của tôi" thấy state list/filter được giữ nguyên.

---

## Phase 3 — FE: container calendar + fetch data

### Task 3.1: Store action gọi endpoint calendar

**Files:**
- Modify: `hrm-client/store/actions.js` (hoặc dùng thẳng `apiGetMethod` như meeting index)

**Việc làm:**
- [x] Theo pattern hiện có (`pages/assign/meeting/index.vue` dùng `this.$store.dispatch('apiGetMethod', 'assign/meeting...')`), KHÔNG cần action riêng — gọi `apiGetMethod` với url `assign/meeting/calendar${buildQueryString(params)}`. Ghi chú lại quyết định trong component.

### Task 3.2: `MeetingCalendarTab.vue` — state + fetch + layout khung

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/MeetingCalendarTab.vue`

**Việc làm:**
- [x] `data()`: `view: 'month'`, `cursorDate: dayjs()`, `filters: { meeting_type_id: null, status: null }`, `meetings: []`, `loading: false`, `meetingTypes: []`, drawer/popover state.
- [x] `computed periodRange`: tính `[from, to]` theo view:
  - month: đầu tuần của ngày 1 → cuối tuần của ngày cuối tháng (trọn lưới 6 hàng). Tuần bắt đầu Thứ 2 (đối chiếu mockup — xác định `getWeekStart` mockup dùng CN hay T2, làm theo mockup).
  - week: đầu tuần → cuối tuần của `cursorDate`.
  Format `YYYY-MM-DD HH:mm:ss` (from = 00:00:00, to = 23:59:59) khớp kiểu datetime `start_date`/`end_date`.
- [x] `methods.fetchMeetings()`: set loading, gọi `apiGetMethod` url calendar với `from_date,to_date,meeting_type_id,status` (bỏ field null qua `buildQueryString`), gán `meetings`, tắt loading.
- [x] `methods.loadMeetingTypes()`: gọi `assign/meeting_types/getAll` → `meetingTypes`.
- [x] `mounted()`: `loadMeetingTypes()` + `fetchMeetings()`.
- [x] `watch`: `view`, `cursorDate`, `filters` (deep) → `fetchMeetings()`.
- [x] Template khung: `<calendar-header>`, `<calendar-filter-toolbar>`, `<calendar-summary-bar>`, rồi `<month-grid v-if="view==='month'">` / `<week-grid v-else>`, `<meeting-detail-drawer>`, `<day-meetings-popover>`. Tạm để placeholder cho các component chưa làm (Phase sau).
- [x] Đăng ký lazy import các component con.

**Verify:**
- [x] Mở tab Lịch meeting → Network thấy request calendar đúng khoảng ngày; đổi tháng → gọi lại; `meetings` có data (dùng Vue devtools).

---

## Phase 4 — FE: view Tháng + thẻ + multi-day

### Task 4.1: Helper lanes multi-day (JS thuần, tách file)

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/calendar-lanes.js`

**Việc làm:**
- [x] Port từ mockup: `isMultiDayTicket`, `getEffectiveEndDate`, `assignMultiDayLanes`, `computeWeekSegments`, `mapLanesToDisplayRows` (§4820–4960). Chuẩn hoá input là meeting `{id, start_date, end_date}` (so sánh theo phần date dayjs). Export các hàm cần dùng.
- [x] Viết cho meeting: multi-day khi `dayjs(end_date).format('YYYY-MM-DD') > start_date` (end_date null → 1 ngày).

**Verify:**
- [x] Test tay trong console/Vue devtools: truyền mảng meeting mẫu (gồm m09 27–28/08) → hàm trả lane/segment đúng cột & bo góc.

### Task 4.2: `MeetingCard.vue`

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/MeetingCard.vue`

**Việc làm:**
- [x] Props `meeting`. Render theo mockup `buildTicketCardHtml`: icon loại (SVG) + tiêu đề (`name`) + dòng khách hàng (nếu `customer_name`) + dòng giờ `HH:mm–HH:mm` (dayjs) + badge trạng thái (`status_name` + chấm màu).
- [x] Màu theo status: map `statusColorKey(status)` (dùng int 0–4 theo spec §3.3) → biến `--card-color/--card-bg/--card-border`. Huỷ (4) → class muted (mờ + gạch tiêu đề).
- [x] Emit `click` (payload meeting.id) khi bấm.
- [x] CSS port từ mockup `.ticket-card*` (chỉ phần meeting).

**Verify:** Render 1 thẻ mỗi trạng thái → màu/giờ/badge đúng; Huỷ bị muted.

### Task 4.3: `MeetingMultiDayBar.vue` + `MonthGrid.vue`

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/MeetingMultiDayBar.vue`
- Create: `hrm-client/pages/assign/my-todo/components/calendar/MonthGrid.vue`

**Việc làm:**
- [x] `MeetingMultiDayBar`: props `segment` (colStart, colSpan, variant, meeting) → thanh span cột, màu theo status, click emit `click`.
- [x] `MonthGrid`: props `cursorDate`, `meetings`. Dựng lưới 6×7 (port `renderMonth` §5144): tiêu đề thứ, mỗi ô: số ngày (ngoài tháng mờ, cuối tuần tint, hôm nay nổi bật), hàng lane multi-day (dùng helper 4.1 + `MeetingMultiDayBar`), rồi tối đa 3 `MeetingCard` 1-ngày (ngân sách 3 đã trừ lane), dư → nút "+N khác".
- [x] Emit `click-meeting` (id) và `click-more` (date, anchorEl).
- [x] Sắp thẻ trong ô theo giờ bắt đầu.

**Verify:** View Tháng 08/2026 hiển thị đúng meeting mẫu; ô >3 meeting hiện "+N khác"; workshop 27–28 là thanh multi-day span 2 cột.

---

## Phase 5 — FE: view Tuần

### Task 5.1: `WeekGrid.vue`

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/WeekGrid.vue`

**Việc làm:**
- [x] Port `renderWeek` (§5222): 7 cột ngày, hàng lane multi-day trên đầu (helper 4.1), dưới mỗi cột list `MeetingCard` theo ngày (không giới hạn 3 hoặc cuộn — theo mockup). Cột hôm nay/cuối tuần style riêng.
- [x] Emit `click-meeting`.

**Verify:** Toggle sang Tuần → tuần chứa ngày đang xem hiển thị đúng; chuyển tuần ‹ › chạy.

---

## Phase 6 — FE: header, filter, summary

### Task 6.1: `CalendarHeader.vue`

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/CalendarHeader.vue`

**Việc làm:**
- [x] Props `view`, `periodLabel`. Toggle Tháng/Tuần (§3623 `.view-toggle`), nút ‹ ›, nút "Hôm nay", nhãn kỳ, chú thích màu trạng thái (5 màu).
- [x] Emit `change-view(view)`, `prev`, `next`, `today`.
- [x] Container tính `periodLabel`: month `"Tháng M/YYYY"`, week `"Tuần DD/MM – DD/MM/YYYY"`; `prev/next` dịch `cursorDate` theo view; `today` set về hôm nay.

**Verify:** Đổi view/kỳ cập nhật nhãn + reload data.

### Task 6.2: `CalendarFilterToolbar.vue`

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/CalendarFilterToolbar.vue`

**Việc làm:**
- [x] Props `filters`, `meetingTypes`. 2 select (`V2BaseSelect`): Loại meeting (từ meetingTypes) + Trạng thái (5 mục theo spec §3.3). Nút "Xóa lọc".
- [x] Emit `change(filters)` / `clear`. (Không có lọc nhân viên/thị trường.)

**Verify:** Chọn loại/trạng thái → lịch lọc đúng; Xóa lọc reset.

### Task 6.3: `CalendarSummaryBar.vue`

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/CalendarSummaryBar.vue`

**Việc làm:**
- [x] Props `meetings`, `periodLabel`. Port `buildSummaryBarInnerHtml` (§4039, chỉ phần meeting, bỏ chip thị trường/extraStats): hero "Số meeting + khoảng ngày" + pill đếm theo 5 trạng thái. Đếm trên `meetings` (đã lọc theo kỳ+filter). Mục count 0 → mờ.

**Verify:** Số tổng + đếm trạng thái khớp số thẻ đang hiển thị; đổi filter/kỳ cập nhật.

---

## Phase 7 — FE: drawer chi tiết + popover ngày

### Task 7.1: `MeetingDetailDrawer.vue`

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/MeetingDetailDrawer.vue`

**Việc làm:**
- [x] Props `meetingId`, `show`. Khi mở: gọi chi tiết qua endpoint `show` sẵn có (`assign/meeting/{id}` — đối chiếu url thật ở `pages/assign/meeting/index.vue`).
- [x] UI port từ mockup `.ticket-drawer`/`openTicketDrawer` (§1552+, builders §4334–4562): header màu theo status + code + thời gian; body các khối: Mục tiêu/Nội dung (`content`), Loại meeting, Hình thức (`mode_id`) + địa điểm/`online_link`, Khách hàng + người liên hệ (`customer_contact_*`), Thành phần công ty/khách, Kết luận (`conclusion`), Người tạo. Null-check mọi field.
- [x] Footer: nút "Xem biên bản" + "Sửa" → emit `view-report(id)` / `edit(id)`. Backdrop + nút close → emit `close`.

**Verify:** Click thẻ → drawer mở đúng meeting, đủ thông tin, màu header theo status.

### Task 7.2: `DayMeetingsPopover.vue`

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/DayMeetingsPopover.vue`

**Việc làm:**
- [x] Props `date`, `meetings` (đủ meeting ngày đó), `anchor`. Port `openDayTicketsPopover`/`positionPopoverAt` (§5401–5438): định vị cạnh ô, liệt kê đủ `MeetingCard`. Click 1 thẻ → emit `click-meeting`; click ngoài → `close`.

**Verify:** Ô "+N khác" → popover liệt kê đủ; click thẻ trong popover mở drawer.

### Task 7.3: Nối "Sửa" + "Xem biên bản" vào flow meeting sẵn có

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/MeetingCalendarTab.vue`
- (tham chiếu) `hrm-client/pages/assign/meeting/index.vue` + các modal của nó

**Việc làm:**
- [x] Đọc `pages/assign/meeting/index.vue` xác định cách nó SỬA meeting (modal `CreateMeetingModal`/route) và XEM BIÊN BẢN (modal "Xem biên bản cuộc họp", §331 index meeting).
- [x] Ưu tiên **tái dùng**: import chính modal đó vào `MeetingCalendarTab` và mở với `meetingId`. Nếu modal phụ thuộc nặng context trang meeting → fallback: điều hướng `this.$router.push('/assign/meeting?...')` mở đúng meeting. Chốt cách ít rủi ro nhất, KHÔNG viết lại modal.
- [x] Sau khi sửa xong (event saved) → `fetchMeetings()` refresh lịch.

**Verify:** Từ drawer bấm "Sửa" → mở form sửa meeting hoạt động; lưu xong lịch cập nhật. "Xem biên bản" → mở biên bản đúng meeting.

---

## Phase 8 — Style bám mockup + verify tổng thể

### Task 8.1: Đồng bộ style theo mockup

**Files:**
- Modify: các component calendar (scoped style) + biến màu chung.

**Việc làm:**
- [x] Rà từng component so mockup: token màu trạng thái (`--status-*`), khung `.calendar-panel`, lưới ngày/đường kẻ, hôm nay/cuối tuần tint, thẻ, thanh multi-day, drawer, popover, summary. Đảm bảo khớp thị giác.
- [x] Kiểm tra icon (remixicon codepoint conflict — dùng SVG nếu glyph sai, theo memory).

**Verify:** So sánh trực quan tab Lịch meeting với mockup (mở mockup qua HTTP local, không file://) — bố cục/màu/tương tác khớp.

### Task 8.2: Regression tab "Công việc của tôi"

**Việc làm:**
- [x] Kiểm lại toàn bộ chức năng tab todo (list, filter, calendar sidebar, các modal, detail) hoạt động y như trước khi thêm tab — vì chỉ bọc `v-show`, không được ảnh hưởng.

**Verify:** Tất cả thao tác todo cũ chạy bình thường; chuyển tab qua lại giữ nguyên state.

---

## Trạng thái thực thi (Subagent-Driven, 2026-08-14)

Thực thi qua SDD (mỗi task 1 implementer + review + fix loop). Chi tiết per-task: `sdd-ledger.md`. KHÔNG commit git.

- [x] **Phase 1 — BE endpoint calendar**: `MeetingController::calendar()` + route `GET assign/meeting/calendar` + `MeetingCalendarRangeCriteria` (overlap). Fix: tránh double-apply criteria. Review clean.
- [x] **Phase 2 — FE tab switcher**: bọc todo trong `v-show` + tab "Lịch meeting" + placeholder. Không đổi logic todo. CSS xác nhận an toàn. Review clean.
- [x] **Phase 3+4 — FE-core (Tháng)**: container fetch + MonthGrid + MeetingCard + MeetingMultiDayBar + calendar-lanes.js + calendar-status.js. Fix: fetchRange khớp lưới 6 hàng cố định + dedupe helper. Review clean.
- [x] **Phase 5 — FE-week (Tuần)**: WeekGrid time-grid (giờ 07–17 clamp, dải Cả ngày, lanes) + calendar-week-helpers.js. Không phá Tháng. Review clean.
- [x] **Phase 6 — FE-chrome**: CalendarHeader + CalendarFilterToolbar + CalendarSummaryBar; bỏ filter Thị trường + nút Thêm meeting (ngoài scope); status 5 giá trị BE. Fix: status id STRING (né bug V2BaseSelect id=0 falsy). Review clean.
- [x] **Phase 7 — FE-detail**: MeetingDetailDrawer (fetch show, gate canEdit fail-closed) + DayMeetingsPopover + nối Sửa/Xem biên bản (router.push, tái dùng). Fix: vá XSS `online_link` (chỉ http/https) + reset detail. Review clean.
- [x] **Final whole-branch review**: clean. Fix cuối: summary đếm OVERLAP (khớp lưới) + nhãn 'Hủy' khớp BE.
- [x] **Phase 8.1 — Visual pass (Playwright, 2026-08-14)**: PASS trên app thật (data thật, user DNS Admin). Tháng/Tuần render đúng mockup, thẻ màu theo status, "+N khác", summary đếm đúng theo kỳ (nhãn "Hủy" khớp BE), filter đổ options thật, nav OK, drawer fetch chi tiết + fail-closed (nút "Sửa" ẩn khi canEdit=false). Screenshots: `.playwright-mcp/cal-month.png` · `cal-week.png`. (Phải restart Nuxt dev do manifest .nuxt stale sau đổi branch.)
- [x] **Phase 8.2 — Regression tab todo**: an toàn (chỉ v-show wrapper, không đổi logic; verified ở review Phase 2).

Deferred minors (polish sau, không block): label mode "Trực tuyến" vs "Online"; popover không reposition khi resize.

## Checkpoint — 2026-08-14
Vừa hoàn thành: Toàn bộ implementation BE + FE (7 phase code) qua SDD, final review clean, tất cả fix ADDRESSED. Không commit git.
Đang làm dở: — (code xong).
Bước tiếp theo: USER build client (node12 + heap8192) + api (php7.4 artisan serve), mở /assign/my-todo → tab "Lịch meeting", duyệt visual Tháng/Tuần/drawer/popover/filter + test data thật + phân quyền (canEdit). Báo lại issue nếu có để polish (gồm 2 deferred minor).
Blocked:

## Checkpoint — 2026-08-15 (wrap up)
Vừa hoàn thành: **Playwright verify PASS** trên app thật (user DNS Admin, data thật). Tháng/Tuần render đúng mockup, thẻ màu theo status, "+N khác", summary đếm đúng theo kỳ (nhãn "Hủy" khớp BE), filter đổ options thật, nav OK, drawer fetch chi tiết + FAIL-CLOSED đúng (nút "Sửa" ẩn khi canEdit=false, chỉ hiện "Xem biên bản"). So mockup cạnh nhau: khác biệt đều là quyết định scope đã chốt (bỏ tab thị trường, bỏ filter/summary thị trường, bỏ nút Thêm meeting, dùng 5 status thật BE + thêm nút Hôm nay). Screenshots: `.playwright-mcp/cal-month.png`·`cal-week.png`·`mockup-calendar.png`.
Phát sinh (ngoài scope, đã báo user → user chọn KHÔNG tự sửa): bug CÓ SẴN `ProspectiveProjectResource.php:22-23` thiếu null-check `Employee::find()` → 500 "Trying to get property 'employee_info_id' of non-object" khi drawer bấm Sửa/Xem biên bản điều hướng sang trang meeting show/edit (trang này load dự án tiền khả thi). Thuộc feature `du-an-cha-con`, đã bàn giao report cho người phụ trách. Endpoint calendar KHÔNG liên quan.
Đang làm dở: — .
Bước tiếp theo: (1) user quyết fix 2 deferred minor (label "Trực tuyến"/"Online"; popover reposition khi resize) hay để sau; (2) khi cần merge → yêu cầu commit (hiện chưa commit git); (3) bug ProspectiveProjectResource để owner du-an-cha-con xử lý.
Blocked:

Môi trường đang chạy (dọn khi cần): Nuxt dev `:3000` (đã restart bản mới), API `:8000`, HTTP server mockup `:8899` (python http.server — kill khi so xong).
