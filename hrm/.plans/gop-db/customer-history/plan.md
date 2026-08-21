# Plan — Lịch sử thay đổi Khách hàng (`customer-history`) — @khoipv

Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`).

## Phase 1 — Backend

- [x] BE1. Migration `create_customer_history_table` — bảng `customer_history`
      (`customer_id`, `action`, `old_value`, `new_value`, `changed_by`, `changed_at`, `timestamps`)
- [x] BE2. Entity `Modules/Assign/Entities/CustomerHistory.php`
- [x] BE3. `Modules/Assign/Services/CustomerHistoryService.php`
      (snapshot 40 khoá → giá trị hiển thị · diff subset · ghi log, lỗi log không chặn nghiệp vụ)
- [x] BE4. Hook ghi log trong `CustomerService`:
      `save()` (create/update, gồm cả import Excel) · `setStatus()` (lock/unlock) ·
      `updateMedia()` + `deleteAttachmentFile()` (update_media)
- [x] BE5. `SystemLogService`: `TYPE_CUSTOMER` + adapter `customerLogs()` + `CUSTOMER_FIELD_LABELS`
      + `customerChanges()` (danh sách con dạng bỏ → thêm) + fallback cột audit cho KH cũ
- [x] BE6. Chạy migrate + `php -l` sạch

## Phase 2 — Frontend

- [x] FE1. `components/assign/customer/CustomerHistoryModal.vue` (theo skill modal-popup, cũ ĐỎ → mới XANH)
- [x] FE2. `pages/assign/customers/index.vue` — action `history` (icon `ri-history-line`) + modal
- [x] FE3. Màn chi tiết — dùng base `components/assign/SystemInfoSection.vue`
      (`entity-type="customer"`) đặt **dưới cùng** form, đúng như màn chi tiết Task;
      chỉ render khi `readonly && !modalMode`; `V2Footer` giữ nguyên Sửa · Quay lại

## Phase 3 — Verify

- [x] V1. Tinker: tạo → 1 log create; sửa 3 trường → 1 dòng 3 khoá; lưu y nguyên → không log;
      `''` vs null → không log rác; khóa/mở khóa đúng action, gọi lại không nhân đôi
- [x] V2. `GET assign/system-logs/customer/{id}` đúng DTO, mới → cũ, có `actor_name` + phòng ban
- [x] V3. Playwright: nút lịch sử ở 10/10 hàng danh sách → modal đúng KH; màn chi tiết có phân vùng
      "Lịch sử" ở dưới cùng, bấm "Xem lịch sử" → tải log + badge số dòng + nút Làm mới/Thu gọn
- [x] V4. Dọn sạch dữ liệu test (KH test + log test đã xóa, `customer_history` về 0 dòng)

## Phase 4 — Chỉnh sau khi user test

- [x] F1. Bỏ track 4 trường màn KH không có ô nhập nhưng BE vẫn ghi đè: `district` (form gửi
      `district_id: null` cố định — đã bỏ cấp huyện), 2 hạn mức công nợ, `type_calculate_interest`.
      Bỏ luôn Quận/Huyện khỏi chuỗi "Địa điểm giao hàng".
- [x] F2. `SystemLogService::CUSTOMER_HIDDEN_FIELDS` — ẩn 4 khoá đó cả ở log ĐÃ sinh trước đó
      (verify: log KH 232397 giờ chỉ còn dòng "Số điện thoại 0901234567 → 0901234591").

### Checkpoint — 2026-08-11
Vừa hoàn thành: toàn bộ Phase 1–3 (BE + FE + verify).
Đang làm dở: không.
Bước tiếp theo: user test trên trình duyệt bằng tài khoản thật (sửa 1 KH → mở modal Lịch sử ở cả
màn danh sách và màn chi tiết).
Blocked:

---

## Phase — Fix: modal lịch sử ở màn DANH SÁCH hiện thừa "(trống)" khi chỉ thêm (không bỏ)

- [x] FE `components/assign/customer/CustomerHistoryModal.vue` — ẩn vế `old` + mũi tên khi `c.old` rỗng, khớp với màn xem chi tiết (`components/assign/SystemInfoSection.vue`)
- [x] Verify: parse SFC + đối chiếu markup 2 component + chạy thử 3 case (chỉ thêm / chỉ bỏ / vừa thêm vừa bỏ)

### Checkpoint — 2026-08-11
Vừa hoàn thành: bỏ "(trống)" thừa ở modal lịch sử của màn DANH SÁCH khách hàng.

Gốc rễ: với khoá dạng danh sách (`SystemLogService::DIFF_LIST_FIELDS` — hãng xe, nhóm KH, người
liên hệ...), BE KHÔNG trả giá trị trước/sau mà trả:
```php
'old' => count($removed) ? implode(', ', $removed) : '',      // phần BỊ BỎ
'new' => count($added)   ? implode(', ', $added)   : '(đã bỏ)' // phần ĐƯỢC THÊM
```
Nên `old` rỗng = "không bỏ hãng xe nào", KHÔNG phải "trước đó đang trống". Modal màn danh sách in
`c.old || '(trống)'` nên ra `Hãng xe: (trống) → Omoda` → người dùng hiểu ngược. Màn xem chi tiết
(`SystemInfoSection.vue`) đã ẩn vế cũ khi rỗng từ trước — chỉ cần đồng bộ modal theo nó, không đụng BE.

Verify (render THẬT cả 2 component qua vue-server-renderer rồi so chuỗi, không đọc mắt):

| Case | Danh sách (đã sửa) | Chi tiết | |
| --- | --- | --- | --- |
| Thêm Omoda, không bỏ gì | `Hãng xe: Omoda` | `Hãng xe: Omoda` | ✓ |
| Bỏ BMW, không thêm gì | `Hãng xe: BMW → (đã bỏ)` | như trái | ✓ |
| Bỏ BMW + thêm Omoda | `Hãng xe: BMW → Omoda` | như trái | ✓ |
| Trường thường: trống → ABC | `Tên viết tắt: ABC` | như trái | ✓ |
| Trường thường: ABC → trống | `Tên viết tắt: ABC → (trống)` | như trái | ✓ |

Đang làm dở: không có.
Bước tiếp theo: user build lại hrm-client → mở `/assign/customers`, menu ⋮ của 1 KH → Lịch sử.
Blocked: không có.

- [x] BE `SystemLogService::customerChanges()` — trả thêm `removed[]` / `added[]` cho khoá dạng danh sách (giữ nguyên `old`/`new` để không phá màn khác)
- [x] FE `CustomerHistoryModal.vue` — render mỗi phần tử 1 dòng, `-` cho phần bỏ, `+` cho phần thêm
- [x] FE `SystemInfoSection.vue` — cùng cách render, bọc `v-if` theo `removed/added` để 10 màn dùng chung khác giữ nguyên (user đã duyệt sửa component chung 2026-08-11)
- [x] Verify: render thật 2 component + đối chiếu output BE bằng tinker trên log KH thật

### Checkpoint — 2026-08-11 (hiển thị -/+ cho khoá dạng danh sách)
Vừa hoàn thành: khoá dạng danh sách trên lịch sử KH tách mỗi phần tử một dòng, `-` = bỏ, `+` = thêm.
Áp cho CẢ 2 màn (user duyệt sửa component chung `SystemInfoSection.vue`).

BE — `SystemLogService::customerChanges()` trả thêm `removed[]` / `added[]`; GIỮ NGUYÊN `old`/`new`
để chỗ nào đang đọc 2 khoá cũ không phải sửa theo. Chỉ nhánh khách hàng có 2 khoá này; task/issue
(`diffSnapshot`) không có → 10 màn dùng chung `SystemInfoSection` render y như trước.

FE — cả 2 component thêm nhánh `v-if="(removed && removed.length) || (added && added.length)"`,
CSS `flex: 0 0 100%` + `padding-left: 12px` để danh sách xuống dòng dưới nhãn trường và thụt vào.

Verify BE (gọi thẳng method qua Reflection, không ghi DB):
```
Thêm Omoda, không bỏ gì  → {"old":"","new":"Omoda","removed":[],"added":["Omoda"]}
Bỏ BMW, không thêm gì    → {"old":"BMW","new":"(đã bỏ)","removed":["BMW"],"added":[]}
Bỏ BMW + thêm Omoda      → {"old":"BMW","new":"Omoda","removed":["BMW"],"added":["Omoda"]}
Trường thường            → {"old":"CÔNG TY A","new":"CÔNG TY B"}   (không có removed/added)
Log THẬT id=11 (KH 232396) → {"field":"Hãng xe","removed":[],"added":["Omoda"]}  ← đúng case user báo
```
Verify FE (render thật 2 component qua vue-server-renderer, so chuỗi): 7/7 case hai màn giống hệt —
gồm cả case "loại đối tượng khác" (không có removed/added) vẫn ra `cũ → mới` như trước.

Đang làm dở: không có.
Bước tiếp theo: user build lại hrm-client → so 2 màn (danh sách: menu ⋮ → Lịch sử; chi tiết: mục Lịch sử cuối trang).
Blocked: không có.

## Phase — Thống nhất vị trí thời gian giữa 2 màn (2026-08-12)

- [x] FE `CustomerHistoryModal.vue` — chuyển `.log-time` từ CUỐI mục lên ĐẦU mục (giống `SystemInfoSection.vue` màn chi tiết), đổi `margin-top: 4px` → `margin-bottom: 2px`
- [x] Verify: `vue-template-compiler` compile template không lỗi + kiểm tra thứ tự block ra `log-time -> log-header -> log-detail -> log-changes -> log-note`

### Checkpoint — 2026-08-12
Vừa hoàn thành: popup "Lịch sử khách hàng" ngoài màn danh sách hiển thị thời gian ở đầu mỗi mục,
thống nhất với mục "Lịch sử" trong màn chi tiết KH.
Lưu ý: thứ tự bản ghi mới → cũ vốn đã đúng ở cả 2 màn (BE `SystemLogService::customerLogs()`
orderByDesc `changed_at`/`id` + `finalize()` usort giảm dần) — không cần sửa.
Đang làm dở: không có.
Bước tiếp theo: user build lại hrm-client → mở `/assign/customers`, menu ⋮ của 1 KH → Lịch sử, so với mục Lịch sử màn chi tiết.
Blocked: không có.

## Phase — Ghi đủ thông tin TK ngân hàng + người liên hệ (2026-08-12)

- [x] BE `CustomerHistoryService::bankAccountLines()` — thêm Tỉnh/TP (`bank_province_id` → tên tỉnh) + ghi KÈM NHÃN: `Số TK / Chủ TK / Ngân hàng / Chi nhánh / Tỉnh/TP`
- [x] BE `CustomerHistoryService::contactLines()` — ghi đủ `Họ tên / Chức vụ / Ngày sinh / SĐT / Email / CCCD/CMND` (trước chỉ có 4 trường, không nhãn)
- [x] BE `CustomerHistoryService::contactAccountLines()` (mới) — gắn TK cá nhân của từng người liên hệ (`customer_contact_has_bank_accounts`), đủ 5 trường, nhiều TK ghép bằng `;`
- [x] BE helper mới `labeledParts()` + `bankAccountFields()` + `provinceNames()` (1 query cho cả danh sách, tránh N+1)
- [x] BE `SystemLogService::CUSTOMER_FIELD_LABELS` — đổi nhãn `bank_accounts`: "Tài khoản ngân hàng" → "Tài khoản công ty" (khớp tiêu đề form)
- [x] Verify: `php -l` 2 file + snapshot thật KH 232396 / 1774 + chạy diff qua Reflection ra đúng dòng `-` / `+`

### Checkpoint — 2026-08-12
Vừa hoàn thành: lịch sử KH ghi đầy đủ thông tin TK ngân hàng công ty và người liên hệ (kèm TK cá nhân).

Định dạng mới:
```
Tài khoản công ty: Số TK: ... — Chủ TK: ... — Ngân hàng: ... — Chi nhánh: ... — Tỉnh/TP: ...
Người liên hệ: Họ tên: ... — Chức vụ: ... — Ngày sinh: ... — SĐT: ... — Email: ... — CCCD/CMND: ...
               — TK cá nhân: (Số TK: ..., Chủ TK: ..., Ngân hàng: ..., Chi nhánh: ..., Tỉnh/TP: ...)
```

LƯU Ý: định dạng dòng đổi so với log cũ → lần SỬA ĐẦU TIÊN sau khi deploy, các log cũ chưa có
nhãn sẽ hiện thành 1 cặp `-` (dòng cũ) / `+` (dòng mới) cho mỗi TK & người liên hệ dù nội dung
không đổi. Từ lần thứ 2 trở đi diff sạch.

Đang làm dở: không có.
Bước tiếp theo: user thử sửa 1 KH có TK ngân hàng + người liên hệ → mở Lịch sử đối chiếu.
Blocked: không có.

## Phase — Chỉ liệt kê phần thực sự thay đổi (2026-08-12, bản sửa theo phản hồi user)

Vấn đề: gộp cả người liên hệ + TK cá nhân vào 1 chuỗi → thêm 1 TK là in lại nguyên dòng dài ở cả
`-` và `+`, không nhìn ra đổi cái gì.

- [x] BE `CustomerHistoryService` — 3 khoá dạng BẢNG (`contacts`, `bank_accounts`, `contact_bank_accounts` MỚI) lưu **bản ghi `[nhãn => giá trị]` + `__key`** thay vì chuỗi ghép (`contactRecords/bankAccountRecords/contactBankAccountRecords/record()`)
- [x] BE — tách TK cá nhân của người liên hệ ra khoá riêng `contact_bank_accounts` (kèm tên chủ sở hữu) → thêm/sửa 1 TK không kéo theo dòng người liên hệ
- [x] BE `CustomerHistoryService::diff()` — nhánh `RECORD_LIST_FIELDS` so mảng bản ghi (không `strval`)
- [x] BE `SystemLogService::customerChanges()` — nhận diện danh sách bản ghi (`isRecordList`), ghép cặp theo `__key` (`indexRecords`) → trả thêm `changed[]` (chỉ trường đã đổi: `Tên: cũ → mới`), giữ `removed[]`/`added[]` cho bản ghi xóa/thêm
- [x] BE — thêm nhãn `contact_bank_accounts` = "TK cá nhân người liên hệ"
- [x] FE `CustomerHistoryModal.vue` + `SystemInfoSection.vue` — thêm dòng `~` (màu hổ phách `#b45309`) cho `changed`, gom điều kiện vào method `hasListChange()`
- [x] Verify BE: 5 kịch bản qua Reflection (thêm TK cá nhân / sửa SĐT liên hệ / sửa TK công ty / xóa+thêm liên hệ / **log CŨ dạng chuỗi vẫn đọc được**)
- [x] Verify FE: render thật 2 component bằng vue-server-renderer → output giống hệt nhau, trường thường vẫn ra "cũ → mới"

### Checkpoint — 2026-08-12
Vừa hoàn thành: log KH chỉ liệt kê phần thay đổi.

```
Người liên hệ:
   ~ Trần Thị B: SĐT: 0912345678 → 0999888777
TK cá nhân người liên hệ:
   + Người liên hệ: jjjj — Số TK: 1900 — Chủ TK: 777 — Ngân hàng: 790 — ...
Tài khoản công ty:
   ~ ffff: Chi nhánh: (trống) → CN Cầu Giấy; Ngân hàng: (trống) → Techcombank
```

Khoá ghép cặp: người liên hệ = id contact (luồng lưu upsert theo id); TK công ty = số TK;
TK cá nhân = id contact + số TK (2 bảng TK bị xóa/tạo lại mỗi lần lưu nên KHÔNG dùng id TK).

Log cũ (phần tử là chuỗi) vẫn đọc bình thường — `isRecordList()` trả false → đi nhánh cũ.
Lần sửa ĐẦU TIÊN sau deploy vẫn nhiễu 1 lần do đổi định dạng snapshot.

Đang làm dở: không có.
Bước tiếp theo: user build lại hrm-client → sửa thử 1 KH (đổi SĐT liên hệ, thêm 1 TK cá nhân) rồi mở Lịch sử.
Blocked: không có.

## Phase — Popup lịch sử KH theo base popup "Lịch sử thay đổi quy định nghỉ" (2026-08-12)

Yêu cầu user: sửa popup Lịch sử khách hàng cho GIỐNG popup lịch sử ở màn Quy định nghỉ
(`components/setting/holiday/AttendanceWatchHistoryModal.vue` — base đang dùng cho 4 popup ở màn đó).

- [x] FE `CustomerHistoryModal.vue` — dựng lại theo base: `scrollable` + `body-class="p-0"`, sub-title "Khách hàng: ..." ở header, nút **Bộ lọc** + `b-collapse` thanh lọc (Thao tác / Người thực hiện / Từ ngày / Đến ngày + Tìm kiếm / Làm mới)
- [x] FE — timeline chấm tròn nối dọc (`ho-timeline`) thay icon tròn; mỗi mục: thời gian (monospace) → thao tác (đậm, màu `action_color`) → "Người thực hiện: mã - tên — phòng ban" → khối thay đổi nền `#f8fafc`
- [x] FE — màu chấm lấy từ `action_color` BE trả (`dotStyle()`), không hardcode class như bản holiday
- [x] FE — giữ nguyên cách render `-` / `+` / `~` cho khoá dạng danh sách và "cũ → mới" cho trường thường
- [x] FE — 3 trạng thái rỗng theo base: đang tải / chưa có lịch sử / không khớp bộ lọc (+ giữ nhánh lỗi tải có nút Thử lại)
- [x] Lọc: `actionOptions` + `performerOptions` dựng từ chính log đang có (DTO không trả id NV → gom theo `actor_code`), ngày so bằng `created_at_raw`
- [x] Verify: compile template + parse script; render SSR ra đủ 2 mục log; test 3 bộ lọc (thao tác / từ ngày / người thực hiện) trả đúng

### Checkpoint — 2026-08-12
Vừa hoàn thành: popup Lịch sử khách hàng đã đồng bộ layout với popup lịch sử màn Quy định nghỉ.
KHÔNG đụng `SystemInfoSection.vue` (mục Lịch sử trong màn chi tiết KH) — component dùng chung 10 màn,
user chỉ yêu cầu popup.
Đang làm dở: không có.
Bước tiếp theo: user build lại hrm-client → `/assign/customers` → menu ⋮ → Lịch sử để đối chiếu.
Blocked: không có.

## Phase — Tô màu riêng giá trị cũ/mới trong dòng "đã sửa" (2026-08-12)

Phản hồi user: dòng `~ ffff: Chủ TK: gggg → Nguyễn Văn C` để CÙNG MỘT MÀU nên không phân biệt
được cái nào cũ, cái nào mới.

- [x] BE `SystemLogService::recordFieldChanges()` — trả DỮ LIỆU thay vì chuỗi ghép:
      `['name' => 'ffff', 'fields' => [['field' => 'Chủ TK', 'old' => '...', 'new' => '...']]]`
- [x] BE `recordChangeText()` (mới) — vẫn dựng chuỗi gộp 1 dòng cho khoá `new` (nơi hiển thị gộp)
- [x] FE `CustomerHistoryModal.vue` + `SystemInfoSection.vue` — render `changed` theo cấu trúc mới:
      tên bản ghi màu trung tính `#475569`, giá trị cũ dùng class `change-old` (ĐỎ),
      mũi tên `ri-arrow-right-line`, giá trị mới dùng `change-new` (XANH); nhiều trường ngăn bằng `;`
- [x] Verify BE: đổi Chủ TK 1 TK công ty + đổi SĐT/Email 1 người liên hệ → payload tách đúng old/new
- [x] Verify FE: dump HTML thật 2 component → `<span class="change-old">cũ</span> → <span class="change-new">mới</span>`

### Checkpoint — 2026-08-12
Vừa hoàn thành: dòng "đã sửa" giờ tô cũ ĐỎ / mới XANH giống dòng thay đổi của trường thường.
`changed[]` đổi từ string[] sang object[] — tính TẠI LÚC ĐỌC log nên không cần migrate dữ liệu cũ.
Đang làm dở: không có.
Bước tiếp theo: user build lại hrm-client → sửa 1 KH rồi mở Lịch sử kiểm tra màu.
Blocked: không có.

## Phase — Mục "Lịch sử" màn chi tiết đồng bộ với popup (2026-08-12)

- [x] FE `SystemInfoSection.vue` — thêm nút **Bộ lọc** + thanh lọc (Thao tác / Người thực hiện / Từ ngày / Đến ngày + Tìm kiếm / Làm mới) giống popup; state `showFilter/filters/appliedFilters`, computed `actionOptions/performerOptions/filteredItems`
- [x] FE — dòng người thực hiện đổi về đúng dạng popup: `Người thực hiện: <mã - tên> — <phòng ban>` (bỏ icon user/building, bỏ fallback "—" của phòng ban), `actorText()` fallback "Hệ thống" thay vì "—"
- [x] FE — thêm trạng thái rỗng "Không có lịch sử phù hợp bộ lọc."; reset lọc khi đổi `entityId` hoặc bấm Làm mới (tải lại)
- [x] FE — bỏ CSS `.si-dept` không còn dùng, thêm `.si-filter-bar`
- [x] Verify: compile template + parse script; render SSR 3 log (có/không phòng ban, không có người thực hiện) + test 3 bộ lọc trả đúng

### Checkpoint — 2026-08-12
Vừa hoàn thành: mục "Lịch sử" trong màn chi tiết KH giờ có bộ lọc và hiển thị người thực hiện
giống hệt popup ngoài màn danh sách.

ẢNH HƯỞNG: `SystemInfoSection.vue` dùng chung 10 màn (bom-list, handover ×2, issues modal, meeting,
project item modal, prospective project, request solution, task modal, customer form) → các màn này
cũng có thêm bộ lọc + đổi cách hiển thị người thực hiện. Bộ lọc chỉ đọc DTO chuẩn của
`SystemLogService::finalize()` (action / actor_code / created_at_raw) nên loại đối tượng nào cũng chạy.

Đang làm dở: không có.
Bước tiếp theo: user build lại hrm-client → mở chi tiết KH, thử lọc; ngó qua 1 màn khác (VD chi tiết báo giá/BOM) xem bộ lọc mới có ổn không.
Blocked: không có.

## Phase — Viết skill entity-history theo base màn KH (2026-08-12)

- [x] Cập nhật `.claude/skills/entity-history/SKILL.md` — thêm YAML frontmatter (name/description "Use when..."), đổi mẫu chuẩn sang bộ file màn Khách hàng, mô tả khoá dạng BẢNG + `__key`, hợp đồng DTO `changes[]` (removed/added/changed), sửa quy ước sắp xếp thành MỚI → CŨ (bỏ quy ước ASC cũ)
- [x] Tạo `.claude/skills/entity-history/ui-base.md` — spec UI đầy đủ copy-paste: vỏ popup, bộ lọc 4 ô + logic filters/appliedFilters, 4 trạng thái rỗng/lỗi, timeline 1 mục log, khối thay đổi `~ / - / +`, bảng màu + kích thước, bảng text chuẩn, bảng sai lầm hay gặp
- [x] `CLAUDE.md` — thêm dòng vào bảng "Skill bắt buộc đọc theo ngữ cảnh": làm lịch sử thay đổi/audit log → đọc `entity-history`
- [x] Verify: 7 file mẫu được trích dẫn đều tồn tại; các hàm BE nhắc trong skill (`getLogs/finalize/customerChanges/recordListChange/isRecordList/recordFieldChanges`, `RECORD_LIST_FIELDS`, `__key`) đều có thật; màu + text trong skill khớp 100% code đang chạy

### Checkpoint — 2026-08-12
Vừa hoàn thành: skill `entity-history` đã chuẩn hoá theo base màn Khách hàng (hiển thị, text, màu, bộ lọc).
Không tạo skill mới trùng chủ đề — cập nhật skill sẵn có để tránh 2 nguồn convention mâu thuẫn.
Đang làm dở: không có.
Bước tiếp theo: lần tới làm màn lịch sử nào → đọc `entity-history/SKILL.md` + `ui-base.md` trước khi code.
Blocked: không có.

- [x] Bổ sung skill `entity-history`: quy tắc PHẠM VI — lịch sử thay đổi phải làm ĐỦ 2 nơi (popup màn danh sách + khối "Lịch sử" màn chi tiết) như màn KH; thêm §5.1 (bảng 2 nơi + cách vào + component mẫu + ngoại lệ) và 1 dòng checklist; `ui-base.md` nhấn "phải làm CẢ HAI"
- [x] Bổ sung skill `entity-history` §4.1: thao tác có lý do/ghi chú (từ chối, hủy, đóng, duyệt kèm ghi chú...) BẮT BUỘC hiện đủ trên lịch sử — ghi vào `note`/`meta['reason']`, không được để lý do chỉ nằm ở bảng chính; kèm 1 dòng checklist + nhắc ở câu hỏi chốt §0

### Checkpoint — 2026-08-12 (HOÀN THÀNH)
Vừa hoàn thành: user đã test trình duyệt xong → feature chuyển sang mục **Hoàn thành** trong
`.plans/gop-db/STATUS.md`.
Đang làm dở: không.
Bước tiếp theo: không còn việc trong phạm vi feature này.
Blocked: không.
