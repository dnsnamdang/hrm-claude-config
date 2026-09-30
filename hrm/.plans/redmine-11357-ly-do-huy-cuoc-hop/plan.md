# Plan — Redmine #11357: Danh mục Lý do hủy cuộc họp + ràng buộc thời gian Hoàn thành/Hủy

- **Người phụ trách**: @khoipv — **Nhánh**: `fix-bug-11092026`
- **Design**: `.plans/redmine-11357-ly-do-huy-cuoc-hop/design.md`
- **Spec**: `docs/superpowers/specs/2026-09-12-redmine-11357-ly-do-huy-cuoc-hop-design.md`

> **Hồ sơ MÀN DANH MỤC đã tách sang `.plans/danh-muc-ly-do-huy-cuoc-hop/`** (1 danh mục = 1 thư mục):
> plan + design của màn, việc siết quyền (14/09), sửa file mẫu import (15/09) và **tài liệu testcase**
> (`testcase - Danh mục lý do hủy cuộc họp.xlsx` + `gen_testcase.py`).
> Thư mục này giữ **lịch sử thi công #11357** (Phase 1–8 bên dưới, có cả phần danh mục) và là nơi
> theo dõi tiếp phần **ràng buộc Hoàn thành/Hủy theo giờ + popup hủy** ở màn Cuộc họp.

---

## Phase 1 — Database (hrm-api)

- [x] 1.1 Migration `2026_09_12_000001_create_meeting_cancel_reasons_table.php` (kèm PHPDoc trên `up()`/`down()`)
- [x] 1.2 Seed 3 bản ghi idempotent ngay trong migration 1.1 (người tạo = tài khoản quản trị, có vá ngược cho bản ghi cũ)
- [x] 1.3 Migration `2026_09_12_000002_add_cancel_reason_columns_to_meetings_table.php` — `cancel_reason_id` (FK restrict), `cancelled_at`, `cancelled_by`
- [x] 1.4 Chạy `php artisan migrate` trên DB local, xác nhận 2 bảng/3 cột đã có

## Phase 2 — Backend danh mục (hrm-api)

- [x] 2.1 Entity `MeetingCancelReason` (+ `isCanEdit` / `isCanLockUpdate` / `isCanDelete`)
- [x] 2.2 Service `MeetingCancelReasonService` (index / getAll / updateOrCreate / destroy / validateImportData / importReasons)
- [x] 2.3 FormRequest `MeetingCancelReasonRequest` (rethrow `ValidationException`)
- [x] 2.4 Resource list + detail
- [x] 2.5 Controller `MeetingCancelReasonController` (10 action) — `destroy()` chặn khi đã có meeting dùng
- [x] 2.6 Export class `MeetingCancelReasonExport` + blade `exports/meeting_cancel_reason.blade.php`
- [x] 2.7 Routes trong `Modules/Assign/Routes/api.php` + `checkPermission` (`/getAll` đặt trước `/{id}`)
- [x] 2.8 Permission 1182 / 1183 vào `PermissionsTableSeeder.php`

## Phase 3 — Backend ràng buộc thời gian (hrm-api)

- [x] 3.1 `Meeting.php`: relation `cancel_reason_ref()`, thêm 3 cột vào `$fillable`
- [x] 3.2 `Meeting.php`: `completeBlockedReason()` / `cancelBlockedReason()` / `canComplete()` / `canCancel()` / `cancelReasonText()`
- [x] 3.3 `MeetingController::update()` — guard Hoàn thành trong khối `status === HOAN_THANH`
- [x] 3.4 `MeetingController::changeStatus()` — guard Hủy + validate `cancel_reason_id` + ghi `cancelled_at` / `cancelled_by`
- [x] 3.5 `MeetingResource` + `MeetingTransformer` — trả 8 field mới (cờ mặc định `false`)
- [x] 3.6 `MeetingHistoryService::snapshot()` — `'Lý do hủy'` dùng `cancelReasonText()`
- [x] 3.7 `sendMeetingNotification()` — dòng "Lý do:" dùng `cancelReasonText()`

## Phase 4 — Frontend danh mục (hrm-client)

- [x] 4.1 `pages/assign/meeting_cancel_reason/index.vue` (copy khuôn `reason_project_failure`)
- [x] 4.2 `components/modal/meeting-cancel-reason-modal.vue`
- [x] 4.3 `store/actions.js` — `addMeetingCancelReason`
- [x] 4.4 `components/menu-sidebar.js` — mục "Lý do hủy cuộc họp" (đặt CUỐI nhóm Danh mục)
- [x] 4.5 Nút Xóa mờ khi `is_can_delete === false` + tooltip

## Phase 5 — Frontend ràng buộc + popup (hrm-client)

- [x] 5.1 `components/V2Footer.vue` — prop optional `complete_disabled` / `complete_tooltip` / `cancel_disabled` / `cancel_tooltip`
- [x] 5.2 `pages/assign/meeting/components/CancelMeetingModal.vue` — dropdown bắt buộc + textarea ghi chú + validate inline
- [x] 5.3 `MeetingForm.vue` — thay `BaseConfirmModal` bằng `CancelMeetingModal`, gửi `cancel_reason_id`
- [x] 5.4 `MeetingForm.vue` — `footerMenu` thêm 4 khóa disabled/tooltip
- [x] 5.5 Hiển thị lý do hủy dùng `cancel_reason_text` ở `MeetingForm.vue` + `MeetingDetailDrawer.vue`

## Phase 8 — Chuẩn hoá component chung + kiểm thử logic Khóa/Xóa danh mục

- [x] 8.1 `CancelMeetingModal.vue`: bỏ CSS tự chế, dùng `V2BaseLabel required`, `:invalid` của
      `V2BaseSelectInModal`, `V2BaseError`, class Bootstrap `alert alert-danger` (khuôn `CloseProjectModal`)
- [x] 8.2 `meeting-cancel-reason-modal.vue`: dựng lại trên **`V2BaseModal`** (trước đó tự khai `b-modal`
      vì bê từ modal danh mục đời cũ); `<textarea>` thô → `V2BaseTextarea`; bỏ khối `<style>` chép thừa
- [x] 8.3 2 popup confirm (Xóa · Khóa/Mở khóa): thêm `danger` + `accept-icon` theo skill button-convention
      — Khóa đỏ, **Mở khóa KHÔNG đỏ** (là thao tác khôi phục)
- [x] 8.4 Chuẩn hoá chữ dấu kiểu mới toàn màn: Xóa / Hủy / Khóa (bỏ Xoá / Huỷ / Khoá)
- [x] 8.5 Kiểm thử Playwright logic **Xóa**: nút mờ + tooltip khi lý do đang dùng; API chặn 400;
      xóa lý do chưa dùng thành công
- [x] 8.6 Kiểm thử Playwright logic **Khóa/Mở khóa**: đổi trạng thái, nút Sửa mờ khi khóa,
      dropdown popup hủy loại lý do đã khóa, meeting cũ vẫn hiện tên lý do đã khóa

**Bài học**: modal danh mục đời cũ (`reason-project-failure-modal.vue`) KHÔNG phải khuôn để copy —
nó tự khai `b-modal` + `<textarea>` thô. Popup mới phải dựng trên `V2BaseModal`, ô nhập dùng `V2Base*`.

## Phase 7 — Rà downstream `cancel_reason` (phát sinh sau khi user hỏi "test xong hết chưa")

- [x] 7.1 `grep -rn "cancel_reason"` toàn bộ hrm-api + hrm-client, loại trừ entity khác (RequestSolution, Rice)
- [x] 7.2 `MeetingByMarketService` — cột "Biên bản / Lý do huỷ" của báo cáo theo thị trường (**lỗi thật: rỗng khi không nhập ghi chú**)
- [x] 7.3 `MeetingByMarketService` — eager load `cancel_reason_ref` chống N+1
- [x] 7.4 `MeetingController::customerMeetingHistory()` — leftJoin danh mục + helper `joinCancelReason()`
- [x] 7.5 `MeetingController::update()` — note lịch sử khi đổi trạng thái sang Hủy
- [x] 7.6 `SystemLogService::meetingLogs()` — nhánh log meeting cũ
- [x] 7.7 Xác nhận bản in KHÔNG in lý do hủy → không phải sửa
- [x] 7.8 Test 4 chỗ trên với 3 loại dữ liệu: có ghi chú / không ghi chú / dữ liệu cũ (chỉ text)
- [x] 7.9 Chạy lại bộ 8 ca gốc — vẫn xanh
- [x] 7.10 Kiểm vị trí mục menu trên trình duyệt — nằm cuối nhóm Danh mục

## Phase 6 — Kiểm thử

- [x] 6.1 BE: 8 ca trong spec mục 10 (tinker / HTTP kernel)
- [x] 6.2 FE: compile sạch (`vue-template-compiler` + babel parse) mọi file đã sửa
- [x] 6.3 Báo user phần chưa kiểm chứng trên trình duyệt

---

## Checkpoint

### Checkpoint — 2026-09-12 (khởi tạo)

Vừa hoàn thành: brainstorming, chốt 9 quyết định với user, viết xong design.md + spec đầy đủ + plan.
Đang làm dở: chưa code.
Bước tiếp theo: Phase 1.1 — migration tạo bảng `meeting_cancel_reasons`.
Blocked:

### Checkpoint — 2026-09-12 (code xong Phase 1-6)

Vừa hoàn thành: TOÀN BỘ 6 phase. Chưa commit.

**hrm-api** (nhánh `fix-bug-11092026`)
- 2 migration đã chạy trên DB local: `meeting_cancel_reasons` (+ seed 3 bản ghi) và 3 cột mới trên
  `meetings` (`cancel_reason_id` FK restrict / `cancelled_at` / `cancelled_by`)
- Danh mục đầy đủ: Entity · Service · FormRequest · 2 Resource · Controller (10 action) ·
  Export + blade · 10 route có `checkPermission` · permission 1182/1183 trong seeder
- `Meeting.php`: relation `cancel_reason_ref()`, `cancelReasonText()`,
  `completeBlockedReason()` / `cancelBlockedReason()` / `canComplete()` / `canCancel()`
- Guard: `update()` (Hoàn thành) + `changeStatus()` (Hủy, bắt buộc `cancel_reason_id`)
- `MeetingResource` + `MeetingTransformer` trả 8 field mới (cờ mặc định `false`)
- `MeetingHistoryService::snapshot()` + `sendMeetingNotification()` dùng `cancelReasonText()`
- `index()` eager load `cancel_reason_ref` chống N+1

**hrm-client** (nhánh `fix-bug-11092026`)
- Màn danh mục `pages/assign/meeting_cancel_reason/index.vue` + `components/modal/meeting-cancel-reason-modal.vue`
- `store/actions.js` thêm `addMeetingCancelReason`; `menu-sidebar.js` thêm mục "Lý do hủy cuộc họp"
- File mẫu import `static/Mau_import_LyDoHuyCuocHop.xlsx`
- `components/V2Footer.vue` (**file dùng chung, user đã duyệt**): thêm 4 khóa optional
  `complete_disabled` / `complete_tooltip` / `cancel_disabled` / `cancel_tooltip`, mặc định tắt
- `CancelMeetingModal.vue` mới (dựng trên `V2BaseModal`) — dropdown bắt buộc + ghi chú + validate inline
- `MeetingForm.vue` nối popup mới, gửi `cancel_reason_id`, footer đọc cờ BE
- `MeetingDetailDrawer.vue` hiển thị `cancel_reason_text`

**Kiểm thử đã chạy**
- BE 8/8 ca của spec mục 10 qua HTTP kernel + tinker, mọi ghi đều rollback (DB sạch)
- Export Excel: dựng file thật rồi đọc lại — bề rộng cột đúng (A=6 B=36 C=14 D=45…),
  STT là ô kiểu số, mô tả nhiều dòng giữ được ngắt dòng
- FE: compile sạch 9 file (`vue-template-compiler` + babel parse)

**CHƯA kiểm chứng** (cần user mở trình duyệt)
- Giao diện màn danh mục + menu sidebar
- Popup hủy: dropdown select2 trong modal, viền đỏ khi chưa chọn
- Tooltip trên nút Hoàn thành/Hủy khi bị làm mờ

Bước tiếp theo: user mở trình duyệt kiểm thử; nếu đạt thì commit 2 repo.
Blocked:

### Checkpoint — 2026-09-12 (demo lại + sửa ô Ghi chú)

User xem trực tiếp thao tác trên trình duyệt, phát hiện **ô "Ghi chú" trong popup hủy dùng
`<textarea class="form-control">` thô** thay vì component base.

Nguyên nhân: bê khuôn từ `components/modal/reason-project-failure-modal.vue` (modal danh mục cũ
vẫn dùng textarea thô), trong khi hệ thống ĐÃ CÓ `components/V2BaseTextarea.vue` và popup cùng kiểu
`components/assign/prospective-project/CloseProjectModal.vue` (chọn lý do + ghi chú) đang dùng nó.

**Đã sửa** `CancelMeetingModal.vue` → `<V2BaseTextarea v-model="cancelNote" :rows="3" maxlength="1000" />`.
Kiểm chứng trên trình duyệt: class ra `form-control v2-textarea v2-textarea--sm`, `maxlength=1000`,
`rows=3`; viền / bo góc / cỡ chữ đồng bộ với ô chọn lý do phía trên.

Bài học: **khuôn mẫu để copy phải là màn CÙNG KIỂU NGHIỆP VỤ (popup nhập lý do), không phải
modal danh mục** — modal danh mục là code cũ chưa chuyển sang V2Base.

Demo lại 6 phần đều ĐẠT, dữ liệu demo `[DEMO 11357-A/B]` đã xóa sạch.
Ảnh: `demo11357-01..09-*.png`.

### Checkpoint — 2026-09-12 (KIỂM THỬ PLAYWRIGHT ĐẠT)

Đã test end-to-end trên trình duyệt thật (`localhost:3000` + API `localhost:8000`), tài khoản
DNS Admin (employee 13). Dữ liệu test: 4 meeting tự tạo `[T11357-A..D]` phủ 2 chiều thời gian
× 2 trạng thái — **đã xóa sạch sau khi test**, meeting thật #29/#30 và danh mục 3 lý do nguyên vẹn.

**14/14 ca ĐẠT:**

| # | Ca | Kết quả |
| --- | --- | --- |
| 1 | Meeting CHƯA tới giờ (status 1) — màn xem | Nút Hủy BẬT, không tooltip |
| 2 | Meeting ĐÃ qua giờ (status 1) — màn xem | Nút Hủy MỜ; Playwright **không click được** (disabled thật) |
| 3 | Tooltip nút Hủy bị mờ | Hiện "Cuộc họp đã đến giờ bắt đầu, không hủy được nữa" — khuôn `<span v-b-tooltip>` chạy đúng |
| 4 | Meeting CHƯA tới giờ (status 2) — màn sửa | Hoàn thành MỜ + tooltip "Chỉ được xác nhận hoàn thành khi cuộc họp đã bắt đầu", Hủy BẬT |
| 5 | Meeting ĐÃ qua giờ (status 2) — màn sửa | Đảo ngược: Hoàn thành BẬT, Hủy MỜ |
| 6 | Bấm Hoàn thành khi đã qua giờ | Qua được cổng thời gian, rơi vào validate cũ "Vui lòng thêm biên bản…" (không hồi quy) |
| 7 | Mở popup hủy | Đủ tiêu đề / cảnh báo / dropdown 3 lý do / ghi chú / 2 nút; dropdown select2 nằm trong modal, không bị cắt |
| 8 | Bấm Xác nhận hủy khi CHƯA chọn lý do | Popup giữ nguyên, viền select đỏ `rgb(220,53,69)`, chữ lỗi "Vui lòng chọn lý do hủy cuộc họp", **không gọi API** |
| 9 | Chọn lý do | Lỗi + viền đỏ tự tắt |
| 10 | Hủy hợp lệ (lý do + ghi chú) | 200, quay về danh sách; DB: status=4, cancel_reason_id=1, ghi chú, cancelled_at, cancelled_by=13 |
| 11 | Màn chi tiết sau hủy | "Lý do hủy: Hủy do khách dời lịch — Khách báo dời sang thứ 5 tuần sau" + "Hủy lúc 12/09/2026 11:12 bởi DNS Admin" |
| 12 | Popup Lịch sử | Chốt lịch → Hủy, "Lý do hủy: …" đúng chuỗi ghép |
| 13 | Thông báo chuông | "[T11357-A]… đã bị DNS Admin huỷ. Lý do: Hủy do khách dời lịch — Khách báo dời…" |
| 14 | Drawer Lịch meeting (`/assign/my-todo`) | "Lý do hủy: Hủy do khách dời lịch — Khách báo dời sang thứ 5 tuần sau" |

**Ca phụ đạt thêm:** khóa 1 lý do → dropdown popup chỉ còn 2 (lọc Active đúng);
đóng popup rồi mở lại → lý do/ghi chú/lỗi reset sạch, icon 2 nút footer vẫn còn
(không dính bẫy `$slots.prefix` mất icon từ lần mở thứ 2).

**Guard BE qua HTTP thật (JWT của phiên trình duyệt) — 6/6:**
Hủy quá giờ → 400 · Hủy thiếu lý do → 400 · Lý do không tồn tại/khóa → 400 ·
Hủy meeting đã hủy → 400 · Hoàn thành chưa tới giờ (status 2, payload hợp lệ) → 400 đúng message ·
Hoàn thành đã qua giờ → **200**.

Console: chỉ còn lỗi CÓ SẴN (`hasCustomer` sai kiểu prop, `computed "errors"/"fields" already
defined in data` của vee-validate) — **không lỗi nào từ file mới**.

Ảnh chụp: `t11357-01..09-*.png` ở thư mục gốc `HRM/`.

⚠️ **Ghi nhận (KHÔNG phải lỗi mới)**: popup Lịch sử in lý do hủy **2 lần** — 1 lần ở dòng diff
`Lý do hủy: null → …`, 1 lần ở dòng `note`. Cấu trúc này có từ trước (`snapshot['Lý do hủy']`
và tham số `$note` vốn cùng đọc `cancel_reason`), thay đổi lần này chỉ làm chuỗi đầy đủ hơn.

### Checkpoint — 2026-09-12 (bổ sung: người tạo dữ liệu seed)

Vừa hoàn thành: migration `2026_09_12_000001` gán `created_by`/`updated_by` cho 3 lý do khởi tạo
bằng tài khoản quản trị (`adminEmployeeId()`: email `namdangit@gmail.com` → Super admin id nhỏ nhất
→ null). Vòng lặp seed vá ngược cột này cho bản ghi đã tạo ở lần chạy trước.
DB local đã chạy lại `up()` (idempotent) — 3 bản ghi hiện `Người tạo: DNS01 - DNS Admin`.
Bước tiếp theo: vẫn chờ user kiểm thử trình duyệt.
Blocked:

---

## Phase bổ sung — đã chuyển sang hồ sơ màn danh mục

Hai đợt việc dưới đây thuộc **màn danh mục**, nay theo dõi ở `.plans/danh-muc-ly-do-huy-cuoc-hop/plan.md`:

- **Sửa file mẫu import (15/09/2026)** — đổi tên sheet `Mau_import_LyDoHuyCuocHop.xlsx` từ
  `DM_NNthatbai` thành `DM_lydohuycuochop` → Giai đoạn C của plan mới.
- **Tài liệu testcase màn danh mục (18/09/2026)** — `gen_testcase.py` + file Excel 159 TC
  → Giai đoạn D của plan mới. Hai file đã chuyển sang thư mục đó.

Cần testcase cho popup "Hủy cuộc họp" ở màn Cuộc họp (phần còn lại của issue này) thì tạo file
riêng trong thư mục này.
