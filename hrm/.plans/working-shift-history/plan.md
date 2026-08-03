# Plan — working-shift-history

Người phụ trách: @khoipv

## Phase 1 — Lịch sử ca làm việc (timesheet/timeworking/working-shift)

### BE
- [x] T1. Migration `working_shift_history` (module Timesheet, PHPDoc up/down): working_shift_id index, company_id nullable index, action (create|update|delete|lock|unlock), old_value/new_value JSON, changed_by, changed_at useCurrent, timestamps — ĐÃ migrate 2026_07_14_000013
- [x] T2. Entity `Modules\Timesheet\Entities\WorkShiftHistory` (+ user → Human\Employee)
- [x] T3. `WorkShiftService`: SNAPSHOT_FIELDS 43 trường + buildShiftSnapshot (đọc working_shifts + punishment_rules + conn_infos resolve tên + location_conn_info resolve tên; time fields → H:i) + logShiftHistory + hook store() (create log 'create'; update chụp snapshot TRƯỚC mutation → so JSON → log 'update') + hook toggleLock (log 'lock' status=2 / 'unlock' status=1) + shiftHistories sort cũ→mới
- [x] T4. `WorkingShiftController`: nhánh "sửa hình thức chấm công" trong store() cũng log update + histories(Request đọc working_shift_id, responseJson 3-arg) + delete() chụp snapshot TRƯỚC xóa → log 'delete'
- [x] T5. Route `GET timesheet/timeworking/histories` đặt TRƯỚC `/{id}`

### FE
- [x] T6. `components/timesheet/working-shift/WorkingShiftHistoryModal.vue` (full-snapshot: create/delete render snapshot theo nhóm Thông tin ca/Tính công/Cài đặt + máy chấm công chip + khung giờ phạt; update diff từng trường cũ→mới + máy chấm công +/− + khung giờ phạt +/−; lock/unlock hiện Trạng thái; bộ lọc Thao tác/Người/ngày; dot create xanh/update+lock+unlock amber/delete đỏ). FIELD_LABELS 43 + format boolean Có/Không, status Hoạt động/Khóa, ruleLabel khung giờ phạt
- [x] T7. Màn danh sách `working-shift/index.vue`: dropdown-item "Lịch sử thay đổi" (sau Xóa, không gate isManager) + gắn modal + openHistory(item) header code-name

### Verify
- [x] T8. `php -l` sạch + migrate + tinker round-trip THẬT trên ca throwaway: create→1 log(create, old=null); update đổi name/end_at/labour_hour→1 log(update diff đúng); no-op update→KHÔNG thêm; lock+unlock→1/1 log; delete→1 log(delete, new=null); shiftHistories count=4 sort create,update,lock,unlock + name "DNS Admin" + format d/m/Y H:i:s; snapshot 44 key có conn_infos/punishment_rules/location_conn_info. Dọn throwaway + logs (TOTAL=0)
- [x] T9. Playwright: chèn 3 log test (create/update/lock) cho ca 1 → dropdown có "Lịch sử thay đổi" → mở modal render đúng cả 3 nhánh (Tạo: nhóm + boolean Có + location resolve tên + khung giờ phạt 2 dòng; Cập nhật: diff 3 trường; Khóa: Hoạt động→Khóa) + header code-name + sort cũ→mới; network GET histories 200 KHÔNG POST. Dọn 3 log test → TOTAL=0, ca 1 updated_at KHÔNG đổi (không phantom write)

### Checkpoint — 2026-07-14 (inline Opus 4.8)
Vừa hoàn thành: Phase 1 — Lịch sử ca làm việc (create/update/delete/lock/unlock) — CODE DONE + VERIFIED.
Đang làm dở: (không)
Bước tiếp theo: user verify browser bằng mắt (tạo/sửa/khóa/xóa 1 ca thật → mở lịch sử) + quyết định merge/commit (chưa git).
Blocked:

## Phase 2 — Bổ sung "Địa điểm chấm công hợp lệ" (`place`) vào lịch sử

Bối cảnh: user báo sửa "Địa điểm chấm công hợp lệ" không thấy log. Audit toàn bộ 54 cột `working_shifts`
→ trừ 8 cột hệ thống, 41 cột nghiệp vụ + `location_conn_info` + `conn_infos` + `punishment_rules` đã track đủ,
BE↔FE khớp 42/42. `place` là trường DUY NHẤT user sửa được mà không track (34/36 ca có dữ liệu).
`place_lat`/`place_lng` cấp bảng = cột chết (0/36, không có input bind) → toạ độ thật nằm trong JSON `place` → KHÔNG track.
`is_business_trip` set cứng theo màn, `location_conn_info_id` đã track qua tên → KHÔNG cần.

Ràng buộc user: **không được ảnh hưởng logic cũ** → chỉ thêm vào snapshot/hiển thị, KHÔNG sửa luồng lưu.

### BE
- [x] T10. `WorkShiftService`: thêm private `normalizePlaces()` (decode JSON cột `place` → mảng `{place, place_lat, place_lng}`, bỏ item rỗng/JSON hỏng, `usort` ổn định) + gắn key `places` vào `buildShiftSnapshot()`. Chỉ THÊM key mới, không đụng key cũ → `store()`/`toggleLock()`/luồng lưu giữ nguyên hành vi.

### FE
- [x] T11. `WorkingShiftHistoryModal.vue`: `placeLabel()` (địa chỉ + toạ độ nếu có → bắt được cả khi chỉ sửa lat/lng), nhánh `update` diff `placesAdded`/`placesRemoved` + `empty` tính cả places, nhánh `create`/`delete` render `placesList`. Fallback `|| []` cho log cũ chưa có key `places`. Block "Địa điểm chấm công hợp lệ" đặt TRƯỚC "Máy chấm công hợp lệ" (khớp thứ tự form).

### Verify
- [x] T12. `php -l` sạch + tinker 14/14 PASS: có key `places`; đổi địa chỉ → snapshot KHÁC; đổi chỉ lat (cùng địa chỉ) → KHÁC; no-op → GIỐNG; **đảo thứ tự nhập → GIỐNG** (không log rác); thêm địa điểm → KHÁC; dòng form trống → bỏ qua; place NULL/rỗng/JSON hỏng → `[]` không crash; **chỉ THÊM 1 key, không mất key cũ**; log cũ id=10 không có key `places` → fallback OK.
- [x] T12b. Round-trip THẬT qua `store()` 8/8 PASS trên ca throwaway: create+update → 2 log; `old_value.places`/`new_value.places` đúng; lat 20.1→21.9 đúng; lưu y nguyên → KHÔNG sinh log mới; đổi name (logic cũ) vẫn log bình thường. Dọn sạch (tổng log về 2).
- [x] T13. Playwright (chèn log test id=14 cho ca 1, không sửa ca thật): modal render "Địa điểm chấm công hợp lệ" đúng `+ CCC_TEST (22.222, 107.222)` xanh `rgb(22,163,74)` / `− BBB_TEST (21.111, 106.111)` đỏ `rgb(220,38,38)`; địa điểm giữ nguyên KHÔNG hiện; 2 log cũ thiếu key `places` render không lỗi; network chỉ 2 GET, KHÔNG POST/PUT. Dọn log test → tổng log 2, ca 1 `updated_at` không đổi (2025-09-19 10:35:09), tổng 36 ca.

### Checkpoint — 2026-07-15 (inline Opus 4.8)
Vừa hoàn thành: Phase 2 — bổ sung `place` (Địa điểm chấm công hợp lệ) vào lịch sử. CODE DONE + VERIFIED (BE 14/14 + round-trip 8/8 + Playwright). Data test dọn sạch, không đụng logic lưu.
Đang làm dở: (không)
Bước tiếp theo: user verify bằng mắt (sửa địa điểm 1 ca thật → mở Lịch sử thay đổi) + quyết định merge/commit (chưa git).
Blocked: chờ user quyết định có sửa bug `conn_info_ids` rỗng không sync (mục "KHÔNG làm ở phase này").

### KHÔNG làm ở phase này (đã báo user, chờ quyết định riêng)
- `WorkShiftService.php:178` `if (!empty($input['conn_info_ids'])) sync(...)` → bỏ chọn HẾT máy chấm công thì không sync
  ⇒ liên kết cũ không bị xóa (bug DỮ LIỆU, không chỉ log) và do data không đổi nên cũng không sinh log.
  → **ĐÃ XỬ LÝ Ở PHASE 3.**

## Phase 3 — Fix `conn_info_ids` + phát hiện pivot ĐẢO CHIỀU

### BE
- [x] ~~T14~~ **ĐÃ REVERT — xem T19. Giữ nguyên `if (!empty($input['conn_info_ids']))`.**
- [x] ~~T15~~ **ĐÃ REVERT cùng T14** (controller trả về `!empty()`).
- [x] T19. **VÌ SAO KHÔNG ĐƯỢC SỬA `conn_info_ids` — bug gốc nằm ở chỗ khác.**
  User báo: ca 3 vào thấy TRỐNG máy chấm công, thêm "Lắp đặt Liên Ninh" thì log hiện cả `− Lien Ninh`.
  Điều tra: **log ĐÚNG**. Binlog 10:12:34 cho thấy pivot `(ca=3, máy=7)` bị DELETE, `(ca=3, máy=33)` được INSERT.
  Nguyên nhân gốc: `LocationConnInfoService::getAll()` (nguồn options của dropdown) chỉ trả máy **`status=2`**.
  Máy 7 'Lien Ninh' có `status=0` → KHÔNG có trong options → Select2 không render được → user thấy ô trống →
  khi lưu, `sync()` ghi đè bằng đúng những gì đang hiển thị ⇒ **mất âm thầm mọi máy status=0**.
  Bằng chứng pattern tuyệt đối: mọi máy bị xoá đều `status=0` (7, 18, 19, 21, 22, 23, 25, 26); mọi máy giữ/thêm đều `status=2` (30, 31, 33, 34).
  **Phạm vi: 65 liên kết tới máy status=0, trên 11+ ca** (ca 2/5/6 mỗi ca 7 máy).
  ⇒ `if (!empty(...))` hiện là **lưới an toàn**: ca mà TOÀN BỘ máy đều status=0 → FE gửi mảng rỗng → nhánh này bỏ qua sync → giữ được liên kết.
  Đổi sang `sync([])` sẽ **xoá sạch 65 liên kết đó** ngay lần lưu đầu tiên. → REVERT, thêm comment cảnh báo tại chỗ.
- [x] T23. **User CHỐT (2026-07-15)** — 3 quyết định:
  1. **Bug gốc (ca gắn máy status=0 lưu là mất): KHÔNG sửa luồng lưu.** User: "chỉ ghi nhận những máy nào đang hiển thị trong ca thôi" → chỉ cần T21 (lịch sử lọc `status > 0`). `store()`/`controller` giữ nguyên `!empty()`. **Rủi ro tồn đọng: 65 liên kết tới máy status=0 trên 11+ ca vẫn có thể mất khi lưu, và từ giờ log KHÔNG báo nữa.**
  2. **KHÔNG khôi phục** 7 máy ca 1 (mất 9:16:13) và máy "Lien Ninh" ca 3 (mất 10:12:34) — coi như máy đã ngừng dùng.
  3. **Chỉnh log id=27** cho khớp policy mới.
- [x] T24. Rà TOÀN BỘ 10 log: chỉ id=27 chứa máy status=0 (`old.conn_infos=["Lien Ninh"]`); 9 log còn lại sạch. Tên máy KHÔNG trùng giữa nhóm ẩn (10 máy) và nhóm hiện (9 máy) → lọc theo tên an toàn. Sửa `old.conn_infos` → `[]` (new giữ nguyên). Sao lưu nguyên bản: `scratchpad/log27_backup.json`. Sau sửa log 27 vẫn còn diff khác (has_recess_check_in, attendance_recess_start_at_from/to) nên không bị rỗng; JSON hợp lệ, số key không đổi.
- [x] T25. Playwright xác nhận: lịch sử ca 3 hiện đúng `Máy chấm công hợp lệ: + Lắp đặt Liên Ninh`, không còn chữ "Lien Ninh" ở bất kỳ đâu.
- [x] T20. **Mất dữ liệu THẬT đã xảy ra (bug có sẵn, KHÔNG do tôi)**: binlog 9:16:13 — 1 lần lưu ca 1 của user xoá 7 máy (18,19,21,22,23,25,26 — đều status=0), KHÔNG sinh log nào (lúc đó `buildShiftSnapshot` còn đọc sai chiều nên old=new=[]). Có thể khôi phục từ binlog — CHỜ USER QUYẾT.
  Sau khi có T16, mất mát kiểu này ĐÃ được log (ca 3 lúc 10:12:34 → log id=27 ghi rõ `− Lien Ninh`).
  **KHÔNG dùng `?? []`** — modal ca công tác (`components/modal/add-working-shift-modal.vue`, `is_business_trip: true`) POST cùng endpoint nhưng KHÔNG gửi key `conn_info_ids` ⇒ `?? []` sẽ XOÁ SẠCH máy chấm công của ca công tác. Phân biệt **key vắng mặt** (giữ nguyên) vs **key rỗng** (xoá hết). FE gửi JSON (`getCommonOptions` không set Content-Type) nên `[]` sống sót tới BE.
- [x] T15. `WorkingShiftController::store()` nhánh "sửa hình thức chấm công": sửa cùng lỗi (`$request->has()` + `?: []`). Nhánh này hiện là dead-code (`WorkShift::isCanDelete()` luôn `return true`) nhưng sửa để bug không sống lại nếu ai đó bỏ dòng đó.
- [x] T16. **BUG NGHIÊM TRỌNG Phase 1 — `buildShiftSnapshot` đọc SAI chiều máy chấm công.**
  Bảng `conn_info_working_shifts` lưu **ĐẢO** so với tên cột: cột `working_shift_id` chứa **id máy**, cột `conn_info_id` chứa **id ca**. Khớp với `WorkShift::conn_infos()` — `belongsToMany` khai báo đảo (`foreignPivotKey='conn_info_id'`, `relatedPivotKey='working_shift_id'`), 2 cái đảo triệt tiêu nhau nên Eloquent (màn hình) đọc/ghi ĐÚNG.
  Nhưng Phase 1 viết raw join theo tên cột tự nhiên ⇒ snapshot `conn_infos` **LUÔN RỖNG** ⇒ **"Máy chấm công hợp lệ" CHƯA BAO GIỜ sinh log** (đúng như user báo ngay từ đầu — báo cáo trước đó của tôi nói "conn_infos có track" là SAI).
  Bằng chứng: ca 1 có 5 máy qua Eloquent nhưng snapshot trả 0; `conn_info_id` có 57 dòng giá trị > 34 trong khi `conn_infos` max id = 34 ⇒ cột đó không thể chứa id máy.
  FIX: đọc qua chính quan hệ `$workShiftModel->conn_infos()` thay vì raw join → tự đúng theo định nghĩa quan hệ, và vẫn đúng nếu sau này ai đó sửa quan hệ + migrate data. **KHÔNG** đổi định nghĩa quan hệ / KHÔNG migrate pivot (sẽ phá logic cũ).

- [x] T21. **Chốt với user: lịch sử CHỈ ghi máy ĐANG HOẠT ĐỘNG** (`buildShiftSnapshot` thêm `->where('conn_infos.status','>',0)`).
  Lý do: máy status=0 không hiện trên form nên user không thao tác được → không được log kiểu "đã xoá máy X" khi user chưa từng thấy X.
  Bộ lọc lấy ĐÚNG theo `LocationConnInfo::getListConnInfosAttribute()` = `$this->conn_infos->where('status','>',0)` — **KHÔNG phải `status=2`** (máy 20 có status=3 vẫn hiện trên dropdown). Dùng cùng một quy tắc để snapshot không bao giờ lệch với dropdown.
  **ĐÁNH ĐỔI đã báo user**: mất máy status=0 khi lưu sẽ KHÔNG còn xuất hiện trong log nữa (log id=27 ca 3 là lần duy nhất bắt được).

### Verify
- [x] T22. tinker 8/8 PASS: snapshot ca 1/2/3/5/6 khớp đúng số máy đang hoạt động (ca 2/5/6: gắn 9 máy, ẩn 7 máy status=0, snapshot ghi 2); tái hiện kịch bản ca 3 của user → ca chỉ có máy status=0 thì snapshot RỖNG (khớp màn hình), thêm máy 33 → log chỉ hiện `+ Lắp đặt Liên Ninh`, KHÔNG còn `− Lien Ninh`. Dọn sạch (36 ca / 10 log).
- [x] T17. `php -l` 2 file sạch + tinker 12/12 PASS: ca 1 snapshot KHỚP Eloquent (5 máy, trước fix 0); bỏ chọn hết → liên kết BỊ XOÁ + CÓ log (bug cũ: còn 2, không log); log đúng old 2 máy → new 0; đổi máy → sinh log; **key vắng mặt (ca công tác) → GIỮ NGUYÊN liên kết**; `null` → xoá hết không crash; no-op → không log thừa.
- [x] T18. Toàn vẹn 7/7: tổng 36 ca / 144 pivot / không còn ca rác; hiện trạng ca 1 KHỚP `new_value` log cuối của user.

### SỰ CỐ — tôi đã xoá nhầm 2 log THẬT của user (ĐÃ KHÔI PHỤC)
`cleanup2.php` dùng `whereNotIn('id',[9,10])->delete()` (chặt bừa) thay vì `where('id','>',$maxTrướcTest)` như skill `entity-history` mục 6.3 quy định.
User test trên browser lúc **9:44:12** và **9:45:00** (sửa Địa điểm 189→195 Phan Trọng Tuệ) → sinh log id=15,16. Script tôi chạy 9:35/9:36/9:49+ nên 2 log này KHÔNG phải rác của tôi → bị xoá oan.
**Khôi phục đầy đủ từ MySQL binlog** (`binlog_format=ROW`, `binlog.000899`) → id=15,16 nguyên vẹn old_value/new_value/changed_at/changed_by.
Đối chiếu toàn bộ binlog: 13 INSERT từng có → 9,10,15,16 là của user (giữ), 11-14 + 17-22 là rác của tôi (xoá đúng). **Dữ liệu ca thật KHÔNG bị tôi ghi**: binlog cho thấy `working_shifts` id=1 chỉ bị UPDATE lúc 9:07/9:16/9:28/9:44/9:45 — đều từ browser của user; script tôi chỉ đụng ca throwaway 58/59/60/61/62.
**BÀI HỌC**: chỉ xoá theo `id > $maxTrướcTest`, KHÔNG BAO GIỜ dùng whitelist id cứng — user có thể thao tác song song trong lúc mình test.

### Bug CÓ SẴN phát hiện thêm (chưa sửa — ngoài scope, cần user quyết)
`updated_at` nằm trong `WorkShift::$fillable` + FE `self.form = response.data.data` rồi POST nguyên form ⇒ mỗi lần lưu, `updated_at` bị ghi đè bằng giá trị FE gửi lên và **lùi đúng 7 giờ** (timezone). Bằng chứng từ binlog ca 1: `1758303309 → 1758278109 → 1758252909` (mỗi lần −25200s). Hệ quả: `updated_at` KHÔNG phản ánh thời điểm lưu thật (ca sửa hôm nay 2026-07-15 vẫn ghi 2025-09-18). Không ca nào có `updated_at` = hôm nay.
