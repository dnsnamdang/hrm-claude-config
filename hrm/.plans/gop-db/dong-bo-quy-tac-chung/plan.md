# Plan — Đồng bộ bộ quy tắc chung (đã chốt ở màn Khách hàng) sang các màn khác

Nhánh: `gop_db` · @dnsnamdang · Bắt đầu 2026-08-15

## Bộ quy tắc cần áp cho mỗi màn

**Nghiệp vụ / dữ liệu**

| # | Quy tắc | Nguồn |
| --- | --- | --- |
| R1 | Bộ lọc "Loại hoạt động" của Lịch sử = **3 nhóm cố định** (Tạo mới / Thay đổi thông tin / Thay đổi trạng thái) | `entity-history` §0a |
| R2 | **Bản ghi đã khoá thì KHÔNG cho sửa/xoá** — chặn ở BE (**423**), FE ẩn nút + chặn vào thẳng URL `/edit` | `CLAUDE.md` |

**UI màn danh sách + chi tiết** (`.claude/skills/list-page/SKILL.md`)

| # | Quy tắc | Mục |
| --- | --- | --- |
| U1 | Dùng **bộ lọc mới** `V2BaseSmartFilterPanel` + `filterFields` (có popup "Cài đặt bộ lọc"), bỏ prop `title`/`subtitle` | đầu skill |
| U2 | Cột Hành động ở CUỐI, **tối đa 3 nút** = 2 chính + `⋮`, dùng `V2BaseRowActions`; bỏ hành động "Xem" | 1–2 |
| U3 | Cột định danh (Mã, hoặc Tên nếu bảng không có mã) là **link `nuxt-link` + `.v2-cell-link`**; cấm `href="javascript:void(0)"` | 3 |
| U4 | Cột **Người tạo + Ngày tạo bắt buộc**; Người tạo **chỉ TÊN**, không kèm mã NV; ngày = `d/m/Y H:i` (không giây) | 6 |
| U5 | Bộ cột mặc định gọn, cột nghiệp vụ khác `isVisible: false` | 6 |
| U6 | Căn lề: STT/Trạng thái/Hành động `center`, số & tiền `right`, chữ & ngày `left` | 15 |
| U7 | Cột `sortable` phải có trong whitelist `SORTABLE_COLUMNS` của BE (lệch tên → khai `sortKeyMap`) | "Cột nào được sort" |
| U8 | Dòng đếm chỉ có số, không kèm tên đối tượng | 14 |
| U9 | Màn chi tiết: tiêu đề `Chi tiết <đối tượng>: <mã/tên>` | 7.1 |
| R3 | **Hành động màn chi tiết khớp màn danh sách** — giống cả điều kiện hiện/ẩn | 7.2 |
| R4 | Icon Info + tooltip: `ri-information-line` + `b-popover.info-popover` | `info-icon-tooltip` |
| U10 | **Text nút theo bảng chuẩn** — cùng 1 hành động thì mọi màn dùng cùng 1 chữ (`Tạo mới`, không phải `Thêm <đối tượng>`) | `button-convention` §4.2 |
| U11 | Toolbar danh sách chỉ **1 nút primary** (Tạo mới); In / Xuất / Cấu hình cột là `secondary` | `button-convention` §5 |
| U12 | Màn chi tiết/form: nút **bắt buộc đặt trong `V2Footer`**, không tự dựng khối nút | `list-page` §7.2 |
| U13 | **Nút không dùng được → ẨN HẲN**, không hiện rồi disable — áp cho MỌI lý do (không quyền, chưa đủ điều kiện nghiệp vụ) | `CLAUDE.md` · `list-page` §7.2 |
| U14 | Tiêu đề chi tiết **chỉ ghép `: <mã>` khi có mã**; không có mã → để trần, KHÔNG lấy tên thay | `list-page` §7.1 |
| U15 | **Màu nút theo bảng chuẩn**: Xóa/Từ chối `primary status="danger"` · Khóa `primary status="warning"` · Mở khóa/Khôi phục `primary status="success"` · Xuất file `secondary status="success"` · In/Cấu hình cột `secondary` info | `button-convention` §2b |

---

## ✅ Màn Khách hàng (`/assign/customers`) — làm trước, đã xong

Xem `.plans/gop-db/history-action-groups/plan.md`.

## ✅ Danh mục công việc / lỗi thiết bị (`/customer-care/device-errors`)

Khảo sát trước khi sửa — phần lớn đã đúng sẵn, chỉ hở đúng 1 chỗ ở BE:

| Quy tắc | Hiện trạng khi khảo sát | Việc đã làm |
| --- | --- | --- |
| R1 Lịch sử | **Màn này KHÔNG có tính năng Lịch sử** (không dùng `SystemInfoSection`, `SystemLogService` cũng chưa khai `TYPE_DEVICE_ERROR`) | Không áp dụng. Thêm Lịch sử là **feature mới**, không nằm trong phạm vi "đồng bộ quy tắc" — chờ user quyết |
| R2 BE | `delete()` + `lock()` **đã chặn** sẵn ở service; **`update()` KHÔNG chặn** → sửa được bản ghi đã khoá | ✅ Đã bịt |
| R2 FE (ẩn nút) | **Đã đúng sẵn**: danh sách `status === 1` mới hiện Sửa/Xóa/Khóa, ngược lại chỉ In/Khôi phục | Không phải sửa |
| R2 FE (URL `/edit`) | **Chưa có** chốt chặn | ✅ Đã thêm |
| R3 | **Đã đúng sẵn**: footer chi tiết mirror y hệt cột Hành động (`isActiveRecord` → Sửa/In/Xóa/Khóa; else In/Khôi phục), cùng gate `canManage` + `recordCanDelete` | Không phải sửa |
| R4 | Màn không có icon Info dạng tooltip mô tả | Không áp dụng |

### Đã sửa
- **BE** `DeviceError` entity: thêm `isLocked()` / `isCanEdit()` — nguồn chân lý duy nhất cho điều kiện khoá
- **BE** `DeviceErrorController::update()`: guard ngay đầu hàm → **423** "Bản ghi đang bị khoá, vui lòng khôi phục trước khi cập nhật."
- **FE** `DeviceErrorFormComponent.loadDetail()`: chế độ `edit` + bản ghi khoá → toast + `$router.replace` về màn chi tiết

Không dùng middleware như màn KH vì màn này chỉ có 2 endpoint ghi trên 1 bản ghi (`update`, `delete`)
và `delete` đã chặn sẵn — guard tại controller là đủ, vẫn giữ điều kiện trong entity theo đúng CLAUDE.md.

### Test
| Ca | Kết quả |
| --- | --- |
| `update()` bản ghi đang khoá (id 2244, status=2) | **423** + message đúng |
| `update()` bản ghi đang hoạt động (id 1) | Qua được guard, chạy tiếp luồng bình thường |
| `delete()` bản ghi đang khoá | Đã chặn sẵn từ trước ("Không được xóa!") |
| `isLocked()` / `isCanEdit()` | status=2 → true/false; status=1 → false/true |

Kiểm chứng lỗ hổng trước khi sửa: gọi `DeviceErrorService::update()` trên bản ghi khoá → **đổi được tên**
(bọc `DB::transaction` + `rollBack()` nên dữ liệu không đổi).

### Đợt 2 — đồng bộ bộ quy tắc UI (U1–U9)

Khảo sát cho thấy màn này còn dùng khuôn cũ ở phần lớn quy tắc UI:

| Quy tắc | Trước | Sau |
| --- | --- | --- |
| U1 bộ lọc | `V2BaseFilterPanel` cũ + title/subtitle tự đặt, 9 ô hard-code trong template | `V2BaseSmartFilterPanel` + `filterFields` (9 field), có popup "Cài đặt bộ lọc"; 3 ô tiền/định mức giữ `V2BaseCurrencyInput` qua slot `#field-*` |
| U2 hành động | **4 nút icon tự dựng** trên 1 dòng (Sửa/In/Xóa/Khóa) | `V2BaseRowActions`: 2 nút chính + `⋮` |
| U3 link | `<a href="javascript:void(0)" @click>` — chuột phải KHÔNG mở tab mới | `nuxt-link` + `.v2-cell-link` |
| U4 cột bắt buộc | **Không có Người tạo / Ngày tạo**; Người sửa hiện `"MÃ - Tên"`; ngày `d/m/Y` (thiếu giờ) | Thêm 2 cột; bỏ mã NV (đồng bộ với bản in vốn chỉ lấy `fullname`); ngày `d/m/Y H:i` |
| U5 cột mặc định | Hiện hết 11 cột | 6 cột: STT · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động (bảng không có cột Mã) |
| U6 căn lề | STT `left`, Định mức công `left`, Trạng thái `left` | STT/Trạng thái `center`, Định mức công `right`; width Trạng thái 130px, Hành động 140px |
| U7 sort | — | `sortKeyMap` map `createdAt → created_at`, `price_display → price` (BE whitelist không có `createdAt`, thiếu map là bấm sort không đổi mà không báo lỗi) |
| U9 tiêu đề chi tiết | `Chi tiết công việc / lỗi thiết bị` | `Chi tiết công việc / lỗi thiết bị: <tên>` (form `$emit('loaded')`) |
| U10 text nút | `Thêm công việc/lỗi thiết bị` (vừa sai động từ, vừa lặp tên đối tượng) | **`Tạo mới`** |
| U11 màu nút | `In danh sách` để `primary` → 2 nút primary cạnh nhau | `secondary` |
| U12 V2Footer | Footer **tự dựng** `<div class="d-flex justify-content-end">` + 7 `V2BaseButton` | `V2Footer` + slot `#custom-actions` (Xóa/Khóa/Khôi phục) |
| U13 ẩn nút | Nút Xóa hiện **xám + tooltip** khi bản ghi đã phát sinh chứng từ (cả danh sách lẫn chi tiết) | **ẨN hẳn** — đưa `is_can_delete` vào `visible`/`v-if`; xoá luôn `deleteButtonTitle()` ở 2 file |
| U14 tiêu đề | Tôi từng thêm nhầm tên vào tiêu đề | Trả về **tiêu đề trần** vì bảng không có cột mã |
| U15 màu nút | Xóa `secondary danger` · Khóa `secondary` info · Khôi phục `primary` info · Xuất Excel `secondary` info · In `primary` (do `menu.print` của V2Footer hard-code) · icon Xóa `ri-delete-bin-6-line` | Xóa **`primary danger`** · Khóa **`primary warning`** (cam) · Khôi phục **`primary success`** (xanh lá) · Xuất Excel **`secondary success`** · In **`secondary`** (bỏ `menu.print`, tự render ở slot) · icon **`ri-delete-bin-line`** |

⚠️ `V2Footer` hard-code `menu.print` là `primary`, trái bảng màu (In thuộc nhóm phụ). Không sửa
component dùng chung (ảnh hưởng nhiều màn) → render nút In ở slot `custom-actions` với `secondary`.

Đã rà **toàn bộ** text nút của cả 3 màn (danh sách / form / modal xác nhận): ngoài 1 nút trên,
các nút còn lại đã đúng bảng chuẩn sẵn — `In danh sách`, `Xuất Excel`, `Cấu hình cột hiển thị`,
`Lưu`, `Sửa`, `In`, `Xóa`, `Khóa`, `Khôi phục`, `Quay lại`, `Hủy`, `Chọn`.

Bảng `device_errors` **không có cột mã** → cột **Tên** đóng vai trò cột định danh của quy tắc U3
(sticky + locked + là link).

**Verify trình duyệt (0 lỗi console):**

| Ca | Kết quả |
| --- | --- |
| Cột mặc định | STT · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động |
| Dòng Hoạt động | Sửa (thẻ `<a href>` → mở tab mới được) · Xóa (disabled + giải thích lý do) · `⋮` (Khóa, In) |
| Dòng **Khóa** | Khôi phục · In — **khớp footer chi tiết** (In · Khôi phục · Quay lại) |
| Dữ liệu | Người tạo `Lê Thị Thanh Vy` (không mã), Ngày tạo `27/07/2026 16:01` |
| Bộ lọc mới | 9 field + popup "Cài đặt bộ lọc"; đổi filter → tự search (13 dòng khi lọc Khóa) |
| Dòng đếm | `Hiển thị 1–20 / 2768` (không kèm tên đối tượng) |
| Tiêu đề chi tiết | `Chi tiết công việc / lỗi thiết bị: Kiểm tra tình trạng hoạt động Thiết bị kiểm tra đèn pha 120K` |

### Verify trên trình duyệt — ĐÃ XONG (sau khi gỡ vướng quyền)

| Ca | Kết quả |
| --- | --- |
| Vào `/customer-care/device-errors` | 20 dòng, 0 lỗi console |
| Dòng **Hoạt động** ở danh sách | Sửa · In · Xóa · Khóa |
| Màn **chi tiết** bản ghi khoá (2244) | In · Khôi phục · Quay lại (không Sửa/Xóa/Khóa) — khớp danh sách |
| Vào thẳng `/2244/edit` | Đá về `/customer-care/device-errors/2244` + toast "Bản ghi đang bị khoá, vui lòng khôi phục trước khi chỉnh sửa." |

### Đợt 3 — rà soát ĐỐI CHIẾU với màn Khách hàng + toàn bộ skill (2026-08-15)

Quét marker giữa 2 màn + đọc lại 7 skill. Kết quả: **đã khớp**, còn 2 chỗ lệch → đã sửa,
2 chỗ khác biệt có lý do → giữ nguyên, 2 việc cần user quyết.

**Đã khớp sẵn** (không phải sửa):

| Hạng mục | Ghi chú |
| --- | --- |
| `V2BaseSmartFilterPanel` + `filterFields` · `V2BaseRowActions` · `V2BaseBadge` · `v2-cell-link` | Cả 2 màn như nhau |
| `filterStateMixin` (`localStorageKey` / `pathsToKeep` / `expirationTime`) | Có đủ |
| `columnCustomizationMixin` + `locked` + sticky | Có đủ |
| Filter auto-search (`ignoredFields` / `oldFilters` / deep watcher) | Có đủ |
| `loading: true` ngay từ `data()`; danh sách bắn API không chờ request khác | Đúng mục 8 |
| `import '@/assets/scss/v2-styles.scss'` · `PageTitleMixin` · `CheckPermission` | Có đủ |
| **modal-popup**: xác nhận Xóa/Khóa/Khôi phục dùng `BaseConfirmModal` chung, không `msgBoxConfirm` | ✓ |
| **unsaved-changes**: `create.vue` + `_id/edit.vue` dùng `unsavedChildFormMixin` (đúng loại — form nằm trong component con) | ✓ |
| **button-convention**: text + màu + icon + thứ tự | Đã sửa ở đợt 2 |
| `pageSizeOptions` | Cả 2 màn đều không truyền prop → dùng mặc định 5/10/20/50/100 ✓ |

**Lệch — đã sửa ở đợt này:**

| # | Vấn đề | Sửa |
| --- | --- | --- |
| 1 | **Thiếu `loadSeq`** — 2 lượt `loadData()` chạy song song lúc vào màn, lượt cũ về sau sẽ **ghi đè dữ liệu mới** (list-page mục 8) | Thêm `loadSeq`, bỏ qua response cũ, và chỉ tắt spinner ở lượt mới nhất |
| 2 | **Options bộ lọc nâng cao nạp ngay lúc vào màn** dù panel mặc định thu gọn → 2 request tranh chỗ với API danh sách trên server dev 1 worker | Hoãn tới khi mở panel + cờ `filterOptionsLoaded` chỉ nạp 1 lần |

Verify: vào màn `filterOptionsLoaded = false`, `typeOptions = 0` (chưa tốn request);
mở panel → 6 loại + 884 nhóm hàng hoá; mở/đóng lại **không gọi lại**. 20 dòng, 0 lỗi console.

**Khác biệt CÓ LÝ DO — giữ nguyên:**

- **Không có cột Mã**: bảng `device_errors` không có cột mã → cột **Tên** đóng vai trò cột định danh
  (sticky + locked + link). Tiêu đề màn chi tiết để trần.
- **Không có mục Lịch sử**: entity chưa khai trong `SystemLogService` → R1 không áp dụng.
- **Validate form**: cả 2 màn đều dùng lỗi inline (`showError`/`fieldError` vs `formErrors`),
  không màn nào dùng `vee-validate` — đúng nhóm "màn cũ" của CLAUDE.md, không lệch nhau.

**Đợt 3b — A + B (user duyệt làm):**

**A. Ô tìm nhanh tìm thêm NGƯỜI TẠO** (`DeviceErrorService::filteredQuery`)
Bảng không có cột mã → ô tìm nhanh = Tên + Người tạo. Dùng `orWhereExists` chứ **không join**
(join làm phình câu COUNT của phân trang). Placeholder đổi thành
`"Tìm theo tên công việc/lỗi thiết bị, người tạo..."` cho khớp thứ thực sự tìm được.

**B. Sắp xếp theo ĐỘ KHỚP** — `DeviceErrorService::applyRelevanceOrder()`, khuôn
`CustomerService::applyRelevanceOrder()`.
Bảng chỉ có **1 trường chữ** để chấm điểm (`name`) — không mã, không SĐT/MST — nên công thức rút gọn
còn 1 chiều: trùng khít `0` · bắt đầu bằng `10` · khớp đầu từ `20` · chỉ chứa `30`.
Cũng vì vậy **KHÔNG có** nhánh "từ khoá toàn số ≥6 chữ số thì đảo ưu tiên" (mục 3b) — không có
trường số nào để đảo.
Tie-break giữ đủ 4 bậc: (a) khớp đúng dấu `COLLATE utf8mb4_0900_as_ci` → (b) `IF(LOCATE(..)=0, 9999, LOCATE(..))`
→ (c) `CHAR_LENGTH(name)` → (d) `id DESC`.

**Test:**

| Ca | Kết quả |
| --- | --- |
| Tìm `Kiểm tra tình trạng cầu` (trùng khít) | Bản ghi trùng khít đứng **#1** |
| Tìm `đèn pha` | Xếp theo vị trí khớp tăng dần (9 → 10 → 13…) |
| Tìm `kiem tra` (gõ thiếu dấu) | 5 dòng đầu đều là bản ghi **đúng dấu** |
| Chốt 1 — user bấm sort cột `name` | Bỏ qua relevance, sắp theo tên A→Z |
| Chốt 2 — từ khoá 1 ký tự | Không sinh `CASE WHEN`; ≥2 ký tự thì có |
| Chốt 3 — `id DESC` cuối cùng | Có |
| A — tìm `Cao Đình Hòe` | **1186** bản ghi (do người này tạo); tìm theo tên công việc vẫn chạy (41 cho `đèn pha`) |
| Hiệu năng COUNT phân trang | 647 dòng / **0,014s** (có EXISTS) · 2768 dòng / 0,005s (không lọc) |

📌 Ghi nhận: `device_errors.name` và `customers.fullname` đều `utf8mb4_unicode_ci` — collation này
**bỏ dấu thanh** (`kiem tra` khớp `kiểm tra`) nhưng coi **`đ` khác `d`** (`den pha` KHÔNG khớp
`đèn pha`). Đây là đặc tính MySQL, giống nhau ở cả 2 màn, không phải lệch chuẩn.

### Đợt 3c — user soi lại, phát hiện thêm (2026-08-15)

**1. Cột Trạng thái vẫn sort được** — quy tắc `list-page` "Cột nào được sort": chỉ **Mã/Tên · tiền ·
ngày**. Rà lại thì có **2 cột sai**, không chỉ 1:

| Cột | Trước | Sau | Vì sao |
| --- | --- | --- | --- |
| Trạng thái | `sortable: true` | bỏ | Badge trạng thái không thuộc 3 nhóm được sort |
| Định mức công | `sortable: true` | bỏ | Là **số định mức**, không phải cột tiền |

Còn sortable: Tên (định danh) · Đơn giá bán (tiền) · Ngày sửa · Ngày tạo — khớp màn Khách hàng
(chỉ Mã KH · Tên KH · Ngày tạo).

**2. Modal "chưa lưu" không đúng chuẩn** — đã dựng lại đúng ca test và xác định chính xác:

| Hạng mục | Kết quả |
| --- | --- |
| Chuỗi mixin | `_id/edit.vue` + `create.vue` dùng `unsavedChildFormMixin`, component con dùng `unsavedChangesMixin` + `unsavedSnapshotSource()` + `markFormPristine()` + `markFormSaved()` — **đúng đủ** |
| Phát hiện bẩn | Gõ phím thật → `isFormDirty() = true` ✓ |
| Chặn điều hướng | Bấm Quay lại → **chặn**, không rời màn ✓ |
| `beforeunload` (F5/đóng tab) | Có hộp thoại trình duyệt ✓ |
| **Giao diện popup** | ❌ Là modal mặc định bootstrap-vue (`__BVID__91`, nút `btn-secondary`/`btn-danger`), **KHÔNG phải** `base-confirm-modal` |

⚠️ Nguyên nhân nằm ở **hàm dùng chung**: cả 3 mixin (`unsavedChangesMixin`, `unsavedModalMixin`,
`unsavedChildFormMixin`) đều gọi `$bvModal.msgBoxConfirm()` — trái CLAUDE.md
("Mọi popup XÁC NHẬN dùng đúng 1 component `base-confirm-modal`… TUYỆT ĐỐI không dùng
`$bvModal.msgBoxConfirm()`"). Project đã có sẵn `plugins/confirm-dialog.js` (`this.$confirm`) là
cách đúng.

**CHƯA SỬA** — sửa mixin là sửa hàm dùng chung, đang có **33 màn** phụ thuộc → CLAUDE.md yêu cầu
hỏi trước. Đây KHÔNG phải lỗi riêng màn device-errors mà là lỗi chung của cả 33 màn.

**Còn lại — chưa làm, chờ user:**

| # | Vấn đề | Vì sao |
| --- | --- | --- |
| C | Icon `(i)` ở cột Tên (mở popup "Hàng hoá áp dụng") dùng `title` thuần | Là **nút mở popup**, không phải icon mô tả hover → skill `info-icon-tooltip` không áp. Đổi hay không tuỳ bạn |

### 🔑 Vướng quyền — nguyên nhân gốc (đáng lưu ý cho cả nhánh gop_db)
Ban đầu tài khoản `namdangit@gmail.com` (employee 13) **không vào được màn** (API 403, FE đá về 404):
thiếu quyền `Quản lý danh mục công việc - lỗi thiết bị` (permission id **1131**), và menu FE cũng gate
bằng chính quyền này (`components/subsystem-menu/customer-care.js:31`) nên mục menu không hiện.

Nguyên nhân sâu hơn: bảng `employee_has_roles` của employee 13 có 4 dòng role nhưng **chỉ 1 dòng có
tác dụng**, vì quan hệ `roles()` lọc `model_type = 'Modules\Timesheet\Entities\Employee'`:

| role_id | Tên | model_type | Hiệu lực |
| --- | --- | --- | --- |
| 100002 | Super Admin (company 1 & 4) | `App\Employee` | ❌ |
| 100010 | Giám đốc | `App\Employee` | ❌ |
| 18 | Super admin | `Modules\Timesheet\Entities\Employee` | ✅ |

→ 3 role port từ ERP (`model_type = App\Employee`) bị bỏ qua hoàn toàn. **Nhiều khả năng là vấn đề dữ
liệu chung của nhánh gop_db, không riêng 1 tài khoản** — nên rà xem còn bao nhiêu tài khoản dính.

Đã xử lý (user chọn): gán role **100123 "Quyền giám đốc kinh doanh"** (chứa quyền 1131) cho employee 13
với `model_type = 'Modules\Timesheet\Entities\Employee'`, `company_id = 1` → quyền hiệu lực **575 → 734 (+159)**.

⚠️ Spatie cache quyền **24 giờ** (`config/permission.php`). `php artisan permission:cache-reset` trên máy này
báo *"Unable to flush cache"* → dùng `php artisan cache:clear` hoặc
`app(\Spatie\Permission\PermissionRegistrar::class)->forgetCachedPermissions()`.

---

## Dữ liệu local đã đụng khi test (đã khôi phục)

- `customers.id = 43712`: bị sửa khi chứng minh lỗ hổng + khi test luồng khoá/mở khoá.
  Đã khôi phục 48 cột + 2 quan hệ từ snapshot `customer_versions.id = 59083` và **khoá lại `status = 0`**
  (trạng thái gốc). Riêng `updated_at` / `updated_by` phải lấy theo snapshot (`2026-07-28 09:39:59` / `1085`)
  vì giá trị gốc sau lần khoá không có nguồn nào lưu lại.
- `device_errors.id = 2244`: chỉ đụng trong `DB::transaction` + `rollBack()` → không đổi.
- `role_has_permissions`: có cấp TẠM 1 quyền để thử đi hết luồng HTTP, **đã xoá** (còn 0 dòng).
- `employee_has_roles`: **CÒN GIỮ** 1 dòng mới `(employee_id=13, role_id=100123, model_type='Modules\Timesheet\Entities\Employee', company_id=1)`
  — đây là thay đổi user yêu cầu để mở quyền vào module, KHÔNG phải dữ liệu test. Muốn gỡ:
  `DELETE FROM employee_has_roles WHERE employee_id=13 AND role_id=100123 AND model_type='Modules\\Timesheet\\Entities\\Employee';` + xoá cache quyền.

## Chưa làm — các màn còn lại
Chờ user chỉ định thứ tự. Ứng viên: các màn danh mục Customer Care khác (services, costs, serial…),
danh mục Finance, và các màn có chức năng Khoá/Mở khoá nói chung.

**ĐÃ SỬA (user duyệt: "đồng ý")** — sửa **2 mixin** (`unsavedChildFormMixin`, `unsavedModalMixin`).
`unsavedChangesMixin` rà lại thì **đã dùng `$confirm` sẵn** — `grep msgBoxConfirm` trả 1 dòng nhưng đó là
chữ trong comment, không phải lời gọi. Đổi sang:

```js
ok = await this.$confirm({
    title: 'Thông tin chưa lưu',
    message: CONFIRM_MESSAGE,
    textAccept: 'Thoát',
    textClose: 'Ở lại',
    acceptIcon: 'ri-logout-box-r-line',
    danger: true,
})
```

Giữ nguyên toàn bộ logic guard (cửa sổ 500ms, `beforeunload`, `preventDefault`) — chỉ đổi cách render popup.

**Verify trên trình duyệt (:3002) — 3 màn đại diện, đủ 3 mixin:**

| Màn / mixin | Ca test | Kết quả |
| --- | --- | --- |
| `device-errors/2779/edit` (childForm) | Sửa 1 trường → Quay lại | Popup `app-confirm-…`, nút `v2-btn--primary-danger` + icon `ri-logout-box-r-line` / `v2-btn--tertiary-info` ✓ |
| ″ | Ở lại | Ở nguyên màn, dữ liệu đang nhập còn nguyên ✓ |
| ″ | Thoát | Về danh sách ✓ |
| ″ | Không sửa gì → Quay lại | Thoát thẳng, KHÔNG hỏi ✓ |
| `finance/accounts/add` (childForm) | Sửa 1 trường → Quay lại | Popup chuẩn ✓ |
| ″ | Đổi URL khi đang bẩn | Hộp thoại `beforeunload` của trình duyệt ✓ |
| `finance/works` → modal Thêm vụ việc (`unsavedModalMixin`) | Gõ rồi **Esc** | Popup chuẩn, modal form vẫn mở ✓ |
| ″ | Ở lại | Modal form giữ nguyên, dữ liệu `A` còn ✓ |
| ″ | Bấm **×** | Hỏi lại ✓ → Thoát → modal đóng ✓ |

Đồng thời 33 màn đang dùng 3 mixin này được chuẩn hoá UI theo — không cần sửa từng màn.

---

## ✅ Danh mục gói bảo dưỡng (`/customer-care/services`)

Khảo sát rồi áp cả R1–R4 + U1–U15 như màn Khách hàng / Lỗi thiết bị.

### Nghiệp vụ (R)

| Quy tắc | Hiện trạng | Việc đã làm |
| --- | --- | --- |
| R1 Lịch sử | Màn này KHÔNG có tính năng Lịch sử (`SystemLogService` chưa khai type cho `services`) | Không áp dụng — thêm Lịch sử là feature mới, chờ user quyết |
| R2 BE | `update()`/`delete()` KHÔNG chặn gói đã Khóa | ✅ Đã bịt bằng **middleware** (xem ghi chú dưới) |
| R2 lối thoát | Màn **CHƯA CÓ** thao tác Mở khóa (chỉ `delete()` tự chuyển sang Khóa) → chặn update xong là gói kẹt vĩnh viễn | ✅ Thêm endpoint `PUT /services/{id}/unlock` + nút Mở khóa (danh sách + chi tiết) |
| R2 FE | — | ✅ Ẩn Sửa/Xóa khi gói Khóa; vào thẳng URL `/edit` → chuyển về màn Chi tiết |
| R3 | Màn này **CHƯA CÓ màn chi tiết** | ✅ Thêm `_id/index.vue` (form mode `show`), footer mirror đúng cột Hành động |
| R4 | Giá theo cấp gắn `v-b-tooltip` lên chính tên gói (tooltip đen) | ✅ Đổi sang icon `ri-information-line` + `b-popover.info-popover` |

⚠️ **Guard phải nằm ở MIDDLEWARE, không phải đầu controller.** `ServiceController::update()` nhận
`ServiceRequest` (FormRequest) → Laravel validate lúc resolve tham số, tức TRƯỚC thân hàm: payload
thiếu trường trả **422** và guard trong hàm không bao giờ chạy (đã đo: lần đầu test ra 422 chứ không
phải 423). Thêm `App\Http\Middleware\CheckServiceNotLocked` (alias `serviceNotLocked`) gắn vào
route `update` + `delete`, KHÔNG gắn vào `unlock`. Guard trong controller giữ lại làm lớp thứ 2.

### UI (U)

| Quy tắc | Trước | Sau |
| --- | --- | --- |
| U1 bộ lọc | `V2BaseFilterPanel` cũ + title/subtitle tự đặt | `V2BaseSmartFilterPanel` + `filterFields` (Trạng thái · Người tạo), có popup "Cài đặt bộ lọc" |
| U2 hành động | 4 nút icon nhét trong ô **Tên** (Sao chép/Sửa/In/Xóa) | Cột **Hành động** ở cuối + `V2BaseRowActions` |
| U3 link | Cột Mã là text thường, không vào được chi tiết | Mã = `nuxt-link` + `.v2-cell-link`, sticky + locked |
| U4 cột bắt buộc | Người tạo/sửa hiện `"MÃ - Tên"`; ngày `d/m/Y` (thiếu giờ) | Bỏ mã NV; ngày `d/m/Y H:i` |
| U5 cột mặc định | Hiện hết 9 cột | 7 cột: STT · Mã · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động |
| U6 căn lề | STT/Trạng thái `left` | STT/Trạng thái/Hành động `center` |
| U7 sort | Cột **Trạng thái** đang sortable | Bỏ (chỉ Mã/Tên · tiền · ngày); `serviceCode`/`serviceStatus` map ngược về `code`/`status` khi gửi BE |
| U9/U14 tiêu đề | Không có màn chi tiết | `Chi tiết gói bảo dưỡng: <mã>` (bảng CÓ cột mã) |
| U10 text nút | `Thêm mới`, `Xuất excel`, `Sao chép` | **`Tạo mới`**, **`Xuất Excel`**, **`Nhân bản`** (button-convention 4.2 cấm dùng "Sao chép") |
| U11/U15 màu | Xuất excel `secondary` info | **`secondary success`**; Xóa `primary danger`; Mở khóa `primary success`; In/Nhân bản `secondary` |
| U12 V2Footer | Form đã dùng sẵn | Giữ, bổ sung slot `#custom-actions` cho In/Nhân bản/Xóa/Mở khóa |
| U13 ẩn nút | Nút Xóa hiện **xám + tooltip** khi gói đã dùng | **ẨN hẳn** (`is_can_delete` nằm trong `visible`); bỏ `deleteButtonTitle()` |
| 3b độ khớp | Không có | `ServiceService::applyRelevanceOrder()` chấm điểm 2 trường Mã (0) → Tên (1), `LEAST()`, 3 tie-break + `id DESC` |

**Đổi key cột** `code → serviceCode`, `status → serviceStatus` (list-page mục 4 — cột dời vị trí phải
đổi key, nếu không cấu hình đã lưu của user ghim cột ở chỗ cũ). `ServiceExport::columnDefinitions()`
phải đổi key theo, nếu không `ExportColumns::filter()` loại cột và file Excel thiếu cột mà không báo
gì. Nhân tiện bổ sung 4 cột Người tạo/Ngày tạo/Người sửa/Ngày sửa vào export cho khớp bảng.

### Test

| Ca | Kết quả |
| --- | --- |
| `POST /services/171` (gói **Khóa**) | **423** "Gói bảo dưỡng đang bị khoá, vui lòng mở khoá trước khi cập nhật." |
| `DELETE /services/171` | **423** — trước đây xóa/khóa được |
| `POST /services/138` (gói Hoạt động) | Qua middleware, vào validate bình thường (422 do payload test thiếu trường) |
| `PUT /services/171/unlock` | 200, `status` 0 → 1; gọi lại khi đang Hoạt động → 400 "không cần mở khóa" (đã trả 171 về Khóa sau test) |
| Vào thẳng `/services/171/edit` | Tự chuyển về `/services/171`, không hỏi "chưa lưu" |
| Danh sách — dòng Hoạt động (138) | Sửa · Xóa · ⋮ (Nhân bản, In) |
| Chi tiết 138 | Sửa · In · Nhân bản · Xóa · Quay lại — **khớp** dòng danh sách |
| Danh sách — dòng Khóa (171) | Mở khóa · Nhân bản · In |
| Chi tiết 171 | In · Nhân bản · Mở khóa · Quay lại — **khớp** |
| Chi tiết: ô nhập | Toàn bộ input/select2 `disabled`; ẩn nút Thêm dòng, Hàng hóa, Xóa dòng, Xóa file, Thêm file |
| Cột mặc định | STT · Mã · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động |
| Dữ liệu | Người tạo `Cao Xuân Khang` (không mã), Ngày tạo `15/07/2026 14:22` |
| Sắp xếp cột Mã | FE gửi `sort_by=code`, danh sách đổi đúng thứ tự |
| Icon Info | Hover ra `.popover.b-popover.bs-popover-bottom.info-popover`, nội dung "Cấp 1 (12T): 2,800,000" |
| Lọc Trạng thái = Khóa | Ra đúng 10 dòng Khóa |
| Xuất Excel | HTTP 200, header: STT · Mã · Tên · Giá · **Người tạo · Ngày tạo** · Trạng thái |
| Màn Sửa (138) | Ô nhập bình thường; sửa 1 ký tự rồi Quay lại → popup `app-confirm-…` chuẩn |
| Console | 0 lỗi ở cả danh sách, chi tiết, sửa |

**Quyền**: tài khoản test (`namdangit@gmail.com`, employee 13) thiếu 3 quyền của màn → đã gán
permission 1126/1127/1128 cho role 100123 trong DB local (không sửa seeder — quyền đã có sẵn).

---

## Quy tắc mới: bộ lọc ≤ 3 ô thì bày ngang, bỏ nút "Tìm kiếm nâng cao"

User chốt 2026-08-15. Làm ở **component dùng chung** `V2BaseSmartFilterPanel` để mọi màn hưởng
luôn, page không phải khai gì.

- Computed `isInlineMode` = `visibleFields.length + (showQuickSearch ? 1 : 0) <= 3`
- Inline: ô lọc render ngay trong `.quick-search-row`, `flex: 1` + `min-width: 0` (thiếu `min-width`
  thì select2 tự đo theo option dài nhất và bóp ô tìm nhanh); ép `select2-container`/`mx-datepicker`
  `width: 100%` cho 3 ô đều nhau. Không có nhãn — dùng `placeholder` để thẳng trục với ô tìm nhanh
- Nút "Tìm kiếm nâng cao" và khối `.smart-advanced-filters` cùng ẩn khi inline
- Nút **"Cài đặt bộ lọc"** cũng ẩn khi inline (`showConfigButton`) — **trừ khi còn trường đang bị
  user tắt**: lúc đó panel gọn là do user, ẩn nút = khoá luôn lối duy nhất để bật lại trường
- Ngưỡng đếm **động** theo `visibleFields` → user ẩn/hiện trường ở popup "Cài đặt bộ lọc" thì panel
  tự đổi chế độ
- Tách `components/V2BaseFilterFieldControl.vue` (ô nhập của 1 trường lọc) vì panel giờ render
  trường lọc ở 2 chỗ — nhân đôi markup chắc chắn sẽ lệch khi thêm `type` mới

### 🐛 Lỗi phát hiện khi test (có sẵn từ trước, không phải do đợt này)

`V2BaseSmartFilterPanel` báo giá trị ô lọc về page qua sự kiện `filter-change`, nhưng **`device-errors`
và `services` đều KHÔNG lắng nghe** → mọi ô select/date/text do panel tự render chọn xong **không lọc
gì cả**, cũng không có lỗi console. Chỉ ô do page tự render qua slot `#field-*` (v-model thẳng vào
`filters`) là chạy — nên trước đó không lộ. Đã thêm `@filter-change="handleFilterChange"` + handler
cho cả 2 màn (khuôn `assign/customers/index.vue:1686`).

Trước đây tôi ghi "đổi filter → tự search" ở phần device-errors là **kết luận sai**: lúc đó tôi set
`filters` bằng code chứ không bấm trên UI.

### Test

| Ca | Kết quả |
| --- | --- |
| `/customer-care/services` (1 ô nhanh + 2 ô lọc = 3) | 3 ô cùng 1 hàng, **rộng bằng nhau (317px × 3)**, không có nút "Tìm kiếm nâng cao", khối nâng cao không render |
| Chọn Trạng thái = Khóa ở ô ngang | `filters.status = '0'`, bảng ra dòng Khóa, nút dòng đổi thành Mở khóa · Nhân bản · In |
| `/customer-care/device-errors` (9 trường) | Vẫn có nút "Tìm kiếm nâng cao", 9 ô trong khối nâng cao — không bị ảnh hưởng |
| Chọn Trạng thái = Khóa trong khối nâng cao | `filters.status = '2'`, bảng ra dòng Khóa (trước khi sửa: không lọc được) |
| `/services` — nút "Cài đặt bộ lọc" | Đã ẩn (3 ô, không trường nào bị tắt) |
| device-errors, giả lập user tắt còn 2 trường | Panel chuyển inline, **vẫn giữ** nút "Cài đặt bộ lọc" để bật lại |
| Console | 0 lỗi ở cả 2 màn |

---

# Đợt 4 — 20 màn danh mục (user giao 2026-08-15)

## Quyết định chung (user chốt trước khi làm)

1. **18/20 màn là danh mục dùng MODAL** (không có route chi tiết) → cột định danh là
   `<button class="v2-cell-link">` bấm ra **modal Xem**, BỎ nút "Xem" ở cột Hành động.
   Đã thêm `button.v2-cell-link` vào `assets/scss/v2-styles.scss` + mục **3a** trong skill `list-page`.
2. **Người tạo / Ngày tạo là bắt buộc**; bảng thiếu cột thì **thêm migration**, backfill
   `created_by` = nhân viên của `namdangit@gmail.com` (tra theo EMAIL, không hard-code id),
   `created_at` = thời điểm chạy migration.
3. Quyền test: gán thêm 21 permission danh mục cho role 100123 trên DB local.

## ✅ 1. `customer-care/levels` — Cấp dịch vụ bảo dưỡng

| Hạng mục | Trước | Sau |
| --- | --- | --- |
| DB | `levels` không có `created_by`/`updated_by` | Migration `2026_08_15_000001_add_audit_columns_to_levels_table` + backfill 29 dòng (`created_by` = 13) |
| BE | Entity không ghi audit; Resource trả `created_at` `d/m/Y` | `Level::creator()`, service ghi `created_by`/`updated_by` khi tạo/sửa, Resource trả `created_by_name` (chỉ tên) + ngày `d/m/Y H:i` |
| U1 bộ lọc | `V2BaseFilterPanel` cũ + title/subtitle riêng | `V2BaseSmartFilterPanel` — 1 ô tìm nhanh → **tự chạy chế độ gọn**, không có nút "Tìm kiếm nâng cao" lẫn "Cài đặt bộ lọc" |
| U2 hành động | 3 nút tự dựng (Xem/Sửa/Xóa) | `V2BaseRowActions`: Sửa + Xóa |
| U3 định danh | Tên là text đậm | `<button class="v2-cell-link">` → mở modal Xem; bỏ nút Xem |
| U4 cột bắt buộc | Không có Người tạo/Ngày tạo | Đã thêm cả 2 |
| U5 cấu hình cột | Không có | `columnCustomizationMixin` + nút "Cấu hình cột hiển thị"; Ngày cập nhật mặc định ẩn |
| U6 căn lề | STT `left` | STT `center` |
| U11/U15 màu | Xuất Excel `secondary` info | `secondary status="success"` |
| U13 ẩn nút | Nút Xóa hiện **xám + tooltip** khi cấp đang được dùng | **ẨN hẳn** (`can_delete !== false` nằm trong `visible`) |
| U10 text nút | Modal: "Lưu & Tiếp tục" | "Lưu và tiếp tục" |

**Test (Playwright :3002)** — cột: STT · Tên cấp · Người tạo · Ngày tạo · Hành động ✓ · dữ liệu
`DNS Admin` / `13/10/2021 14:58` ✓ · bấm tên → modal "Xem cấp dịch vụ", ô nhập disabled, chỉ có nút
Đóng ✓ · dòng đang dùng chỉ có Sửa, dòng xoá được có Sửa + Xóa ✓ · Tạo mới → DB ghi
`created_by = updated_by = 13` ✓ · gõ dở rồi Esc → popup "Thông tin chưa lưu" chuẩn, Ở lại giữ
nguyên dữ liệu ✓ · Xóa → confirm đúng tên, xoá xong DB còn 0 dòng test ✓ · 0 lỗi console.

## ✅ 2. `customer-care/note-maintenances` — Ghi chú kiểm tra bảo dưỡng

Bảng `note_maintenances` ĐÃ CÓ sẵn `created_by`/`created_at` (16/16 dòng có dữ liệu) → **không cần
migration**, chỉ thiếu phần BE trả tên người tạo.

| Hạng mục | Trước | Sau |
| --- | --- | --- |
| BE | Resource không trả người tạo, ngày `d/m/Y` | `NoteMaintenance::creator()` + eager load `creator.info`, trả `created_by_name` (chỉ tên), ngày `d/m/Y H:i` |
| U1 | `V2BaseFilterPanel` cũ + title/subtitle | `V2BaseSmartFilterPanel`, 1 ô tìm nhanh → chế độ gọn (không nút nâng cao/cài đặt) |
| U2 | 3 nút tự dựng (Xem/Sửa/Xóa) | `V2BaseRowActions`: Sửa + Xóa |
| U3 | Hạng mục là text đậm | `<button class="v2-cell-link">` mở modal Xem, bỏ nút Xem |
| U4 | Không có Người tạo/Ngày tạo | Đã thêm |
| U5 | Hiện đủ 5 cột | Mặc định 5 cột chuẩn; Ký hiệu / Mô tả / Ngày cập nhật để user tự bật |
| U6 | STT `left` | `center` |
| U13 | Nút Xóa xám + tooltip khi đang dùng | ẨN hẳn |
| Badge sai chỗ | Ký hiệu bọc `span.status-pill.tpl-status-active` (dùng badge trạng thái cho dữ liệu thường) | text thường |
| Rác | CSS `.action-icon-btn` không còn dùng | đã xoá |

**Test**: cột STT · Hạng mục · Người tạo · Ngày tạo · Hành động ✓ · `Đào Thị Thúy` /
`13/10/2021 14:59` ✓ · bấm tên → modal "Xem ghi chú kiểm tra", 3 ô disabled, chỉ có nút Đóng ✓ ·
dòng đang dùng chỉ có Sửa ✓ · Tạo mới: bỏ trống → **3 lỗi inline "Bắt buộc phải nhập"** (không
popup) ✓, nhập đủ → lưu, DB ghi `created_by = 13` ✓ · dòng mới có Sửa + Xóa ✓ · Xóa → confirm đúng
tên → DB còn 0 ✓.

