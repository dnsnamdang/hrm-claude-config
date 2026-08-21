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

## ✅ 3. `customer-care/costs` — Dịch vụ sửa chữa & chi phí khác

Bảng `costs` đã có đủ cột audit + cờ `is_can_edit/delete/lock/unlock` → không cần migration.

### 🔑 Middleware DÙNG CHUNG cho quy tắc "bản ghi khoá không cho sửa"

Trước đó mỗi màn một file (`CheckCustomerNotLocked`, `CheckServiceNotLocked`). Còn 18 màn nữa →
viết **`App\Http\Middleware\CheckRecordNotLocked`** (alias `recordNotLocked:<tên route param>`):

- Model đã được `SubstituteBindings` resolve sẵn → middleware KHÔNG cần biết class, chỉ cần entity
  có `isLocked()`; entity khai thêm hằng `LOCKED_MESSAGE` nếu muốn thông điệp riêng.
- Vẫn phải là middleware (không phải `if` đầu controller) vì controller nhận `FormRequest` →
  validate chạy trước thân hàm, payload thiếu trường sẽ trả 422 và guard không tới lượt.
- 2 middleware cũ giữ nguyên, không sửa (đang chạy ở màn Khách hàng / Gói bảo dưỡng).

| Hạng mục | Trước | Sau |
| --- | --- | --- |
| BE khoá | `update()` chặn nhưng trả **400** và nằm SAU validate của `CostRequest` | `Cost::isLocked()` + `LOCKED_MESSAGE`, route `update`/`delete` gắn `recordNotLocked:cost` → **423** |
| BE tên NV | `employeeDisplayName()` trả `"MÃ - Họ tên"` | chỉ TÊN (list-page mục 6) |
| BE ngày | `created_at` `d/m/Y` | `d/m/Y H:i` |
| U1 | `V2BaseFilterPanel` + 3 ô hard-code trong slot | `V2BaseSmartFilterPanel` + `filterFields` (Phân loại · Trạng thái · Người cập nhật) → 4 ô > 3 nên vẫn có nút "Tìm kiếm nâng cao" |
| U2 | 3 nút tự dựng + nút Khóa nằm TRONG ô Trạng thái | `V2BaseRowActions`: Sửa · Xóa · Khóa/Mở khóa |
| U3 | Tên là text đậm | `<button class="v2-cell-link">` mở modal Xem, bỏ nút Xem |
| U4 | Cột "Cập nhật" gộp `ngày + bởi ai` trong `V2BaseTitleSubInfo` | Tách 4 cột: Người tạo · Ngày tạo (hiện) · Người sửa · Ngày sửa (ẩn) |
| U5 | Hiện đủ 9 cột | 6 cột mặc định, cột nghiệp vụ để user tự bật |
| U6 | STT `left`, Trạng thái `left` | `center` |
| U7 | — | Cột đổi key `status` → `costStatus` (dời vị trí) nên `handleSort` map ngược về `status` |
| U11/U15 | Xuất Excel `secondary` info | `secondary status="success"` |
| U13 | Sửa / Xóa / Khóa hiện **xám + tooltip** khi không đủ điều kiện | **ẨN hẳn** theo cờ `is_can_*` |
| Badge | `renderStatus()` tự dựng `span.status-pill` | `V2BaseBadge` |
| Rác | CSS `.action-icon-btn`, import `V2BaseLabel`/`V2BaseSelect`/`V2BaseTitleSubInfo` | đã xoá |

**Test**: cột STT · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động ✓ · `Đào Thị Thúy` /
`27/07/2026 09:43` ✓ · dòng Hoạt động: Sửa · Xóa · Khóa ✓ · lọc Trạng thái = Khóa → dòng khoá chỉ
còn **Mở khóa** ✓ · panel nâng cao hiện đúng 3 ô ✓ · **API**: PUT/DELETE lên cost đang khoá → **423**
đúng thông điệp; PUT lên cost hoạt động qua được middleware (422 do payload test thiếu trường);
`unlock` không bị chặn (đã trả cost 44 về trạng thái khoá như cũ) ✓ · 0 lỗi console.

## ✅ 4. `customer-care/service-price-config` — Cập nhật nhanh giá dịch vụ

**KHÔNG phải màn danh sách** (form cấu hình 2 trường) → chỉ áp quy tắc form/nút.

| Hạng mục | Trước | Sau |
| --- | --- | --- |
| U12 V2Footer | Nút Lưu tự dựng trong `.card-footer text-right` | `V2Footer` + `footerMenu = { submit_form: canUpdate }`; "Quay lại" do footer tự render |
| U13 | Nút Lưu `:disabled="saving"` + đổi chữ "Đang lưu..." | Không quyền → không đưa vào menu (ẩn hẳn); chống bấm 2 lần đã chặn ở đầu `submit()` |
| U10 | Nút modal xác nhận ghi "Đồng ý" | **"Xác nhận"** (bảng chuẩn button-convention 4.2) |

Sẵn có đúng: `unsavedChangesMixin`, `formValidateMixin` (vee-validate realtime), `BaseConfirmModal`.

**Test**: footer có Lưu + Quay lại ✓ · gõ `a` vào ô hệ số → lỗi inline **"Phải là số"** + viền đỏ,
KHÔNG popup ✓ · bấm Lưu khi đang lỗi → **không mở** popup xác nhận ✓ · sửa hợp lệ → popup "Xác nhận
cập nhật giá dịch vụ" nêu đúng 207 gói bị ảnh hưởng, nút **Xác nhận / Hủy** ✓ · sửa rồi bấm Quay lại
→ popup "Thông tin chưa lưu", Ở lại giữ nguyên ✓ · 0 lỗi console.

## ✅ 5. `customer-care/serials` — Serial thiết bị làm dịch vụ

Màn **CHỈ ĐỌC** (thêm/sửa/xoá serial nằm ở màn Khách hàng) → không có cột Hành động, không có modal
xem. Cột định danh `serial` để **text thường**: màn không có route chi tiết lẫn modal nên không bịa
link (list-page mục 3a chỉ áp khi có modal Xem).

| Hạng mục | Trước | Sau |
| --- | --- | --- |
| BE | Query không select `created_at`, Resource không trả; `updated_at` `d/m/Y` | Thêm `serials.created_at` vào select + `SORT_FIELDS`, Resource trả `created_at`/`updated_at` `d/m/Y H:i` |
| U1 | `V2BaseFilterPanel` + 4 ô hard-code | `V2BaseSmartFilterPanel` + `filterFields`; Khách hàng là select tìm-từ-server nên giữ ở slot `#field-customer_id` |
| U4 | Có Người tạo nhưng **thiếu Ngày tạo** | Thêm Ngày tạo, đứng cạnh Người tạo ngay trước Trạng thái |
| U5 | Hiện đủ 8 cột | Mặc định 7 cột; Người sửa / Ngày cập nhật để user tự bật |
| U6 | STT `left`, Trạng thái `left` | `center` |
| U7 | Cột Trạng thái sortable | Bỏ (badge không thuộc nhóm được sort); đổi key `status` → `serialStatus` vì cột dời vị trí |
| U11/U15 | Xuất Excel `secondary` info + `:disabled` | `secondary status="success"` + `:interactable` |
| Badge | `span.status-pill` tự dựng | `V2BaseBadge`, text từ `status_text` |
| Export | Cột Excel lọc theo key cột màn | Đổi `status` → `serialStatus` cho khớp (nếu quên thì file mất cột Trạng thái) + thêm cột Ngày tạo |

**Test**: cột STT · Serial · Tên hàng · Khách hàng · Người tạo · Ngày tạo · Trạng thái ✓ ·
`Nguyễn Thị Thu Hiền` / `28/07/2026 08:58` ✓ · badge chuẩn, không còn `.status-pill` ✓ · panel nâng
cao đủ 4 ô (Khách hàng · Trạng thái · Người tạo · Người cập nhật) ✓ · lọc Trạng thái = Ngưng sử dụng
→ ra đúng dòng "Ngưng sử dụng" ✓ · 0 lỗi console.

## 🔧 Quy tắc BỔ SUNG giữa chừng (user chốt 2026-08-15)

**Chữ trong ô bảng để THƯỜNG, không in đậm — kể cả cột Mã.** Gốc của việc cả bảng bị đậm là class
dùng chung `.field-line` khai `font-weight: 600` trong `assets/scss/v2-styles.scss` → đổi về `400`,
và `.v2-cell-link` (cột định danh) cũng từ 600 → 400. Ngoài ra bỏ `font-weight-bold` trong ô của
8 file: costs · serials · currencies · banks · account-banks · accounts · product-transfer-requests ·
type-accounts. Đã ghi vào skill `list-page` mục 3.

Badge trạng thái (`V2BaseBadge`) vẫn giữ 600 — đó là chip có nền riêng, không phải chữ trong ô.

**Verify**: `/assign/customers`, `/customer-care/device-errors`, `/customer-care/services` — mọi ô
đều `font-weight: 400`, riêng badge 600; cột Mã vẫn nhận ra nhờ màu navy + gạch chân đứt.

## ✅ 6. `human/nations` — Danh mục quốc gia

| Hạng mục | Trước | Sau |
| --- | --- | --- |
| DB | 5/33 dòng thiếu `created_by` | Migration `2026_08_15_000002_backfill_created_by_on_nations_table` (bảng đã có sẵn cột, chỉ bù dữ liệu) |
| BE | Resource không trả người tạo, ngày `d/m/Y` | `Nation::creator()` + eager load, trả `created_by_name`, ngày `d/m/Y H:i` |
| U1 | `V2BaseFilterPanel` + 1 ô lọc trong slot | `V2BaseSmartFilterPanel`; 1 ô lọc + tìm nhanh = 2 ô → **chế độ gọn**, không nút nâng cao/cài đặt |
| U2 | 4 nút tự dựng, Sửa/Xóa **xám + tooltip** | `V2BaseRowActions`: Sửa · Xóa · Khóa/Mở khóa, ẩn hẳn khi không dùng được |
| U3 | Mã là text thường, không bấm được | `<button class="v2-cell-link">` mở **modal Xem** (modal trước đây KHÔNG có chế độ xem — đã thêm) |
| U4 | Không có Người tạo/Ngày tạo | Đã thêm |
| U5 | Hiện đủ 6 cột, thứ tự Tên trước Mã | Mặc định: STT · Mã · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động; Mã bưu chính ẩn |
| U6 | STT/Trạng thái `left` | `center` |
| U10 | Nút "Thêm quốc gia"; modal "Lưu và làm tiếp" | **"Tạo mới"**; **"Lưu và tiếp tục"** |
| Cấu hình cột | Không có | `columnCustomizationMixin` + modal + nút |
| Modal | Không có `unsavedModalMixin`, nút dùng `:disabled` | Thêm mixin (3 sự kiện shown/hide/hidden), đổi sang `:interactable`, footer Lưu · Lưu và tiếp tục · Đóng |

⚠️ **2 phát hiện phải nhớ cho các màn sau:**

1. **Nhóm danh mục địa lý CHƯA CÓ permission nào** trong `PermissionsTableSeeder`, route BE cũng
   không gắn `checkPermission`. Tôi đã thử gate bằng tên quyền tự đặt → nút biến mất hết. Đã bỏ, giữ
   đúng hiện trạng "không gate quyền", và **KHÔNG tạo cờ giả `canManage = true`** (CLAUDE.md cấm).
   → **Cần user quyết**: có bổ sung quyền cho nhóm danh mục địa lý vào seeder không?
2. **`unsavedModalMixin` mặc định tìm `ref="my-modal"`.** Modal nhóm địa lý đặt `ref="modal"` →
   popup "chưa lưu" hiện bình thường nhưng **bấm Thoát modal đứng im**. Phải override
   `unsavedModalRef() { return 'modal' }`. Đã ghi vào skill `unsaved-changes`.

**Test**: cột đúng thứ tự ✓ · `DNS Admin` / `03/08/2026 15:20` ✓ · bấm mã → modal "Xem quốc gia",
3 ô disabled, chỉ nút Đóng ✓ · dòng Hoạt động: Sửa · Xóa · Khóa ✓ · Khóa "Poland" → confirm đúng
tên → trạng thái đổi, nút còn **Mở khóa** ✓ → đã mở khóa trả lại trạng thái cũ ✓ · Tạo mới, gõ dở
rồi bấm ×/Esc → popup "Thông tin chưa lưu", chọn Thoát → modal đóng thật ✓ · 0 lỗi console.

## 🔧 Quy tắc BỔ SUNG lần 2 (user chốt 2026-08-15)

**Placeholder ô lọc phải nói đúng trường đó lọc gì**: ô chọn `Chọn <tên trường>`, ô gõ tay
`Nhập <tên trường>`, ô tìm nhanh `Tìm theo <các trường BE thực sự lọc>`. CẤM `Tất cả`, `Chọn...`,
để trống. Lý do: bộ lọc ≤ 3 ô chạy **chế độ gọn** không render nhãn → placeholder là thứ DUY NHẤT
cho user biết ô đó là gì, `Tất cả` lúc đó vô nghĩa. Đã sửa 10 chỗ ở serials · nations · areas ·
provinces · districts (+ wards/hamlets viết mới đã đúng), ghi vào `list-page` và `CLAUDE.md`.

## ✅ 7–11. Nhóm danh mục ĐỊA LÝ: `areas` · `provinces` · `districts` · `wards` · `hamlets`

5 màn cùng khuôn với `nations` nên áp cùng một bộ sửa (BE + FE + modal).

### BE (chung)

| Việc | Chi tiết |
| --- | --- |
| Cột bắt buộc | 5 Resource trả thêm `created_by_name` (chỉ `fullname`) + `created_at`; `updated_at` đổi `d/m/Y - H:i` → `d/m/Y H:i` |
| Tránh N+1 | `AreaService`/`ProvinceService`/`WardService` eager load `employee_create.info`; District/Hamlet vốn đã join sẵn `employee_infos` |
| KHÔNG đụng hàm dùng chung | `BaseModel::employee_create_name` ghép `"MÃ - Tên"` — sửa nó là ảnh hưởng cả hệ thống, nên Resource tự đọc `optional(...)->fullname` |

### FE (chung, mỗi màn)

Bộ lọc mới (2 ô lọc + tìm nhanh = 3 ô → **chế độ gọn**, không nút nâng cao/cài đặt) · `V2BaseRowActions`
thay 3-4 nút tự dựng · cột định danh thành `<button class="v2-cell-link">` mở **modal Xem** · thêm
Người tạo/Ngày tạo · bộ cột mặc định gọn + popup Cấu hình cột · STT/Trạng thái căn giữa · nút
"Thêm X" → **"Tạo mới"** · ẩn hẳn nút không dùng được.

**Modal (5 file)**: thêm chế độ `isView` (mọi ô `:disabled`, footer chỉ còn Đóng) · `unsavedModalMixin`
+ override `unsavedModalRef() = 'modal'` · `markFormSaved()` trước khi đóng · text nút
"Lưu và làm tiếp" → **"Lưu và tiếp tục"** · `:disabled` → `:interactable`.

### 🐛 Lỗi phát hiện khi test (áp cho CẢ nations đã làm trước)

**Lưu xong modal không đóng.** `submit()` gọi `$refs.modal.hide()` nhưng KHÔNG gọi `markFormSaved()`
→ guard "chưa lưu" thấy form còn bẩn nên chặn luôn cú `hide()` của chính mình; user thấy bấm Lưu mà
modal đứng im, dữ liệu thì đã lưu rồi. Đã bổ sung `markFormSaved()` cho cả 6 modal.

### Khác biệt từng màn

| Màn | Riêng |
| --- | --- |
| `areas` | Bảng đang RỖNG (0 dòng) — test bằng cách tạo bản ghi rồi xoá. Cột định danh = Tên (không có mã) |
| `provinces` | Có cột Mã → Mã là cột định danh, đứng ngay sau STT |
| `districts` | KHÔNG có cột Trạng thái (service chỉ lấy bản ghi hoạt động) → không có Khóa/Mở khóa |
| `wards` | Giữ nguyên điều kiện nghiệp vụ: Xóa/Khóa chỉ hiện khi `can_delete` |
| `hamlets` | Cột Quận/Huyện mặc định ẩn (VN đã bỏ cấp huyện, BE trả rỗng) |

### Test (Playwright :3002)

| Màn | Kết quả |
| --- | --- |
| `areas` | Tạo "TEST KHU VUC QT" → dòng hiện `DNS Admin` / `15/08/2026 15:01` ✓; bấm tên → modal "Xem khu vực" (ô + select disabled, chỉ nút Đóng) ✓; Sửa → đổi tên OK, **modal đóng được sau khi lưu** ✓; Khóa → nút còn "Mở khóa" ✓; nút Xóa ẩn đúng vì đã có 4 tỉnh trỏ tới ✓; đã xoá dữ liệu test |
| `provinces` | Cột STT · Mã · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động ✓; `Trịnh Thị Lợi` / `08/11/2025 08:37` ✓; modal "Xem Tỉnh/TP" khoá 3 input + 2 select ✓; lọc Trạng thái = Khóa → 0 dòng (DB không có tỉnh khoá) ✓ |
| `districts` | 6 cột (không có Trạng thái) ✓; `Trần Hạnh Minh` / `19/06/2026 15:36` ✓; nút Sửa · Xóa ✓; modal "Xem quận/huyện" ✓ |
| `wards` | 7 cột ✓; `Trịnh Thị Lợi` / `26/08/2025 09:50` ✓; nút Sửa · Xóa · Khóa ✓; modal "Xem phường/xã" ✓ |
| `hamlets` | 7 cột (Quận/Huyện ẩn) ✓; `Nguyễn Hồng Hiệp` / `28/07/2026 08:49` ✓; nút Sửa · Xóa ✓; modal "Xem đường/phố" ✓ |

Tất cả: hàng lọc 5 phần tử (tìm nhanh + 2 ô lọc + Tìm kiếm + Làm mới), không nút "Tìm kiếm nâng
cao", 0 lỗi console.

## 🔧 Quy tắc BỔ SUNG lần 3 (user chốt 2026-08-15)

**Chọn cột định danh**: mặc định là **Mã**, đứng ngay sau STT (TRƯỚC Tên), sticky + locked + là link.
Chỉ đổi sang **Tên** khi (a) bảng không có cột mã, hoặc (b) bảng có mã nhưng CÒN bản ghi bỏ trống mã
— link ở ô `—` thì bấm cũng vô nghĩa. Phải kiểm bằng dữ liệu thật:
`SELECT COUNT(*), SUM(code IS NULL OR code='') FROM <bang>`.

Áp lại: `nations` (5/33 trống) và `provinces` (11/45 trống) → link ở **Tên**, Mã lùi xuống sau Tên.
`services` · `accounts` · `customers` (mã đủ 100%) → giữ link ở **Mã**. Ghi vào `list-page` mục 3a.

## ✅ 12. `finance/accounts` — Danh mục tài khoản

| Hạng mục | Trước | Sau |
| --- | --- | --- |
| DB | 307/309 dòng thiếu `created_by` | Migration `2026_08_15_000003_backfill_created_by_on_finance_catalogs` — bù cho 5 bảng danh mục Tài chính cùng lúc (accounts · type_accounts · works · cost_debts · source_capitals) |
| BE tên NV | `Account::employeeDisplayName()` trả `"MÃ - Tên"` | chỉ TÊN |
| BE ngày | `created_at`/`updated_at` `d/m/Y` | `d/m/Y H:i` |
| BE khoá | `update()`/`delete()` KHÔNG chặn tài khoản đã khoá | `Account::isLocked()` + `LOCKED_MESSAGE`, route gắn `recordNotLocked:account` → **423** |
| U1 | `V2BaseFilterPanel` + 6 ô hard-code trong slot | `V2BaseSmartFilterPanel` + `filterFields` (6 field, > 3 nên vẫn có nút "Tìm kiếm nâng cao"); placeholder "Tất cả" → "Chọn theo dõi công nợ" |
| U2 | 3 nút tự dựng + nút Khóa nằm TRONG ô Trạng thái | `V2BaseRowActions`: Sửa · Xóa · ⋮ (Khóa/Mở khóa, Lịch sử) |
| U3 | Số tài khoản (cột Cấp 1/2/3) là text thường | Ô có giá trị thành `nuxt-link` vào màn chi tiết (giữ khuôn cây 3 cột của ERP) |
| U4 | Cột "Ngày tạo"/"Cập nhật" gộp `ngày + bởi ai` | Tách 4 cột: Người tạo · Ngày tạo (hiện) · Người sửa · Ngày cập nhật (ẩn) |
| U5 | Hiện đủ 10 cột | 9 cột mặc định (giữ 3 cột Cấp vì là số tài khoản); Loại TK / Theo dõi công nợ ẩn |
| U9/U14 | **KHÔNG có màn chi tiết** | Thêm `_id/index.vue` (form mode `show`) + tiêu đề `Chi tiết tài khoản: <số TK>` |
| U11/U15 | "In danh sách" `primary`, Xuất Excel `secondary` info | In `secondary`, Xuất Excel `secondary status="success"` |
| U12 | Nút Lưu/Lưu&Thêm tiếp/Quay lại nằm ở **HEADER** của form | Chuyển hết vào `V2Footer` (+ slot cho "Lưu và tiếp tục") |
| U13 | Sửa/Xóa/Khóa hiện xám + tooltip | ẨN hẳn theo cờ BE |
| R3 parity | — | Footer chi tiết = Sửa · Lịch sử · Quay lại, khớp cột Hành động ngoài danh sách |
| Badge | `renderStatus()` tự dựng `span.status-pill` | `V2BaseBadge` |
| Rác | `V2BaseLabel`, `V2BaseSelect`, `renderStatus`, `lockButtonTitle`, `deleteButtonTitle` | đã xoá |

**Test**: cột STT · Cấp 1/2/3 · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động ✓ ·
`DNS Admin` / `06/09/2023 14:29` ✓ · bấm số TK → `/finance/accounts/1`, tiêu đề tab
**"Chi tiết tài khoản: 111"**, mọi ô + 4 select disabled ✓ · footer chi tiết Sửa · Lịch sử · Quay lại,
bấm Lịch sử mở đúng modal ✓ · màn Sửa: footer Lưu · Quay lại ✓ · **khoá account 308 rồi vào thẳng
`/308/edit` → tự chuyển về màn chi tiết**, footer chỉ còn Lịch sử · Quay lại ✓ · **API**: PUT lên
account khoá → **423**; account hoạt động qua middleware (422 do payload test) ✓ · đã trả account 308
về trạng thái Hoạt động · 0 lỗi console (đã sửa 1 lỗi thiếu prop `modalId` của modal lịch sử).

⚠️ Ghi nhận: `Account::isCanUnlock()` chỉ cho **chính người tạo** mở khoá (`created_by == employeeId`)
— dữ liệu ERP cũ có `created_by` là người khác nên admin không mở khoá được. Giữ nguyên hành vi ERP,
KHÔNG tự sửa; nêu ra để user quyết.

## ✅ 13. `finance/type-accounts` — Danh mục loại tài khoản

| Hạng mục | Trước | Sau |
| --- | --- | --- |
| DB | thiếu `created_by` | Đã bù ở migration chung `2026_08_15_000003` |
| BE | `employeeDisplayName()` trả `"MÃ - Tên"`; ngày `d/m/Y`; không chặn bản ghi khoá | chỉ TÊN; `d/m/Y H:i`; `TypeAccount::isLocked()` + `recordNotLocked:typeAccount` → **423** |
| U1 | `V2BaseFilterPanel` + 5 ô hard-code | `V2BaseSmartFilterPanel` + `filterFields` (Trạng thái · Người tạo · Người cập nhật · Cập nhật từ/đến) |
| U2 | 4 nút tự dựng + Khóa nằm trong ô Trạng thái | `V2BaseRowActions`: Sửa · Xóa · ⋮ (Khóa/Mở khóa, Lịch sử) |
| U3 | Mã là text thường; Tên nhồi "Người tạo - Ngày lập" vào sub | Mã là `<button class="v2-cell-link">` mở modal Xem; Tên để trần |
| U4 | Người tạo/Ngày lập nằm trong ô Tên; "Cập nhật" gộp ngày + người | Tách 4 cột riêng |
| U5/U6 | 6 cột hiện hết, STT `left` | 7 cột mặc định gọn (Ghi chú, Người sửa, Ngày cập nhật ẩn), STT/Trạng thái `center` |
| Badge | `renderStatus()` tự dựng | `V2BaseBadge` |

**Test**: cột STT · Mã · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động ✓ · `DNS Admin` /
`04/08/2026 10:18` ✓ · dòng: Sửa · Xóa · ⋮ ✓ · bấm mã → modal "Xem loại tài khoản" (3 ô disabled,
chỉ nút Đóng) ✓ · panel nâng cao đủ 5 ô kể cả 2 ô ngày ✓ · **API PUT lên bản ghi khoá → 423** ✓ ·
0 lỗi console.

## ✅ 14. `finance/currencies` — Danh mục tiền tệ

| Hạng mục | Trước | Sau |
| --- | --- | --- |
| DB | Bảng **KHÔNG có** `created_by`/`updated_by` | Migration `2026_08_15_000004_add_audit_columns_to_currencies_table` + backfill 11 dòng |
| BE | Không ghi audit; Resource không trả người tạo; ngày `d/m/Y` | `Currency::creator()` + `isLocked()` + `LOCKED_MESSAGE`; service ghi `created_by`/`updated_by`; Resource trả `created_by_name`, ngày `d/m/Y H:i`; route gắn `recordNotLocked:currency` |
| U1 | `V2BaseFilterPanel` + 1 ô lọc trong slot | `V2BaseSmartFilterPanel`; 1 ô lọc + tìm nhanh = 2 ô → **chế độ gọn** |
| U2 | 3 nút tự dựng + Khóa trong ô Trạng thái | `V2BaseRowActions`: Sửa · Xóa · Khóa/Mở khóa |
| U3 | Mã là text; Tên gọi khác nhồi vào ô Tên | Mã là link mở modal Xem; Tên gọi khác thành cột riêng (mặc định ẩn) |
| U4 | Không có Người tạo/Ngày tạo | Đã thêm |
| Badge | `renderStatus()` | `V2BaseBadge` |

**Test**: cột STT · Mã · Tên · Tỷ giá · Người tạo · Ngày tạo · Trạng thái · Hành động ✓ ·
`DNS Admin` / `02/12/2021 09:11` ✓ · hàng lọc 4 phần tử, không nút nâng cao ✓ · bấm mã → modal
"Xem tiền tệ" (4 ô disabled) ✓ · **Tạo mới "TQT" → DB ghi `created_by = updated_by = 13`** ✓ ·
khoá bản ghi rồi PUT → **423** ✓ · đã xoá dữ liệu test · 0 lỗi console.

## ✅ 15–20. Nhóm còn lại: `banks` · `account-banks` · `works` · `cost-debts` · `source-capitals` · `product-transfer-requests`

### DB (migration)

| Bảng | Việc |
| --- | --- |
| `banks` | Thiếu hẳn `created_by` → migration `2026_08_15_000005` thêm cột (kiểu `int` cho khớp `updated_by` sẵn có) + backfill |
| `company_accounts` | Thiếu `created_by`/`updated_by` → migration `2026_08_15_000006` + backfill |
| works · cost_debts · … | `created_by = 0` (kiểu "trống" thứ 2 của ERP, migration trước chỉ bù `NULL`) → migration `2026_08_15_000007` bù thêm 18 dòng |

### BE

- 5 Resource trả `created_by_name` (chỉ `fullname`) + `created_at`; mọi mốc thời gian đổi sang `d/m/Y H:i`
- `CompanyAccount`/`Currency` ghi `created_by`/`updated_by` khi tạo/sửa (trước đó không ghi gì)
- `isLocked()` + `LOCKED_MESSAGE` cho `CompanyAccount`, route `account-banks` gắn `recordNotLocked` → **423**

**Mở rộng middleware dùng chung**: route `account-banks` nhận `{id}` thô (không bind model) nên
`CheckRecordNotLocked` được bổ sung tham số thứ 2 là CLASS entity:
`recordNotLocked:id,Modules\Finance\Entities\CompanyAccount\CompanyAccount` → middleware tự `find()`.

### FE (cả 6 màn)

Bộ lọc mới · `V2BaseRowActions` thay các nút tự dựng · cột định danh thành link/button mở modal Xem ·
tách nút thao tác ra khỏi ô Mã và ô Trạng thái · `V2BaseBadge` · thêm Người tạo/Ngày tạo · bộ cột
mặc định gọn · thêm chế độ **Xem** cho modal của works/cost-debts/source-capitals.

### 🐛 3 lỗi phát hiện khi test

1. **Text nút sai chuẩn ở 4 màn** (user chỉ ra ở `account-banks`): "Thêm tài khoản" / "Thêm mã phí" /
   "Thêm nguồn vốn" / "Thêm mới" → **"Tạo mới"**. Rà tiếp toàn bộ 20 màn còn phát hiện:
   "Lưu & Tiếp tục" → **"Lưu và tiếp tục"** (6 modal), tiêu đề modal "Thêm X" → "Tạo X" (7 modal),
   "Xem chi tiết X" → "Xem X" (2 modal).
2. **`rows="3"` truyền CHUỖI cho prop Number** của `V2BaseTextarea` → mỗi lần mở modal đẻ 3 dòng
   `[Vue warn] Invalid prop: type check failed`. Lỗi có sẵn từ trước, sửa `:rows="3"` cho **55 file**
   (bỏ qua 1 file `.html` mockup — file đó là HTML thuần, thêm `:` sẽ hỏng).
3. Modal Xem của works/cost-debts còn 1 ô textarea chưa `:disabled` — đã bổ sung.

### Test

| Màn | Kết quả |
| --- | --- |
| `banks` | STT · Mã · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động ✓; `DNS Admin` / `20/04/2026 09:35` ✓; nút Sửa · Xóa · ⋮ (Khóa, Chi nhánh) ✓; bấm mã → modal "Xem ngân hàng" (4 ô disabled, chỉ nút Đóng) ✓ |
| `account-banks` | 8 cột chuẩn ✓; dòng Hoạt động: Sửa · Khóa — dòng Khóa chỉ còn **Mở khóa** ✓; API PUT lên bản ghi khoá → **423** ✓ |
| `works` | `DNS Admin` / `15/08/2026 15:28` ✓; modal "Xem vụ việc" khoá đủ 3 ô ✓ |
| `cost-debts` | 7 cột chuẩn ✓; modal "Xem mã phí" khoá đủ 3 ô ✓; 0 lỗi console sau khi sửa `rows` |
| `source-capitals` | STT · Tên · Người tạo · Ngày tạo · Hành động ✓; hàng lọc 3 phần tử (chế độ gọn) ✓; modal "Xem nguồn vốn" chỉ còn nút Đóng ✓ |
| `product-transfer-requests` | 8 cột ✓; bỏ hàng nút nhét dưới mã, chuyển sang cột Hành động ✓; badge chuẩn thay `status-pill` ✓; panel nâng cao đủ 6 ô ✓; bấm mã → `/7359`, tiêu đề "Chi tiết phiếu yêu cầu chuyển hàng PYCCH-07359" ✓ |

**→ HOÀN THÀNH 20/20 màn user giao.**


---

## Đợt kiểm thử cuối — rà lại 20/20 màn theo tất cả skill (2026-08-15)

Chạy lại từng màn trên trình duyệt (tải lại trang đầy đủ, chờ bảng render xong), kiểm: tên cột ·
dữ liệu dòng 1 · nút hành động theo trạng thái · cột định danh là link · không nút disabled trong
bảng · không còn `status-pill` · chữ trong ô không in đậm · số ô trên hàng lọc · text + **màu** nút ·
modal Xem · lỗi console.

### Lỗi phát hiện thêm và đã sửa

- [x] **Màu nút sai `button-convention` mục 2b** (user chỉ ra ở màn chi tiết tài khoản):
  - `accounts` chi tiết: nút Khóa để `secondary` (trắng) → `primary :status="isLocked ? 'success' : 'warning'"` (Khóa cam · Mở khóa xanh lá)
  - `accounts` + `type-accounts`: Import Excel thiếu `status="warning"` + icon `ri-file-upload-line` → `ri-upload-line`
  - `type-accounts` · `currencies` · `product-transfer-requests`: Xuất Excel thiếu `status="success"`
  - `product-transfer-requests`: Xuất Excel đứng sau Cấu hình cột → đưa lên trước
  - `AccountBankModal`: nút Lưu thiếu `size`, nút Đóng dùng `light` trong modal footer → `tertiary size="sm"`
  - `BankModel`: icon nút "Xóa ảnh" là `ri-close-circle-line` (icon Từ chối) → `ri-delete-bin-line`
  - `BankBranchesModel`: "Thêm chi nhánh" → "Tạo mới"
  - `ServiceFormComponent`: 2 nút chọn hàng hoá để `primary` + icon `ri-search-line`, text thiếu động từ → `secondary`, icon `ri-checkbox-circle-line`, "Chọn hàng hóa" / "Chọn nhóm hàng"
- [x] **Màn chi tiết `accounts` thiếu hành động so với danh sách** (list-page 7.2): danh sách có Sửa · Khóa · Lịch sử, footer chỉ có Sửa · Lịch sử → thêm nút Khóa/Mở khóa (`$confirm` chung) + nút Xóa gate bằng `is_can_delete`; điều kiện hiện đọc từ cùng cờ BE như dòng danh sách
- [x] **Thiếu `head()`** (tab trình duyệt hiện tên mặc định của app): `account-banks`, `works`, `cost-debts`, `source-capitals`
- [x] **`product-transfer-requests` — Ngày tạo thiếu giờ phút**: Resource để `d/m/Y` → `d/m/Y H:i` (cả `created_at` lẫn `approved_time`, cả List lẫn Detail Resource)
- [x] `costs`: cột Phân loại còn `status-pill` → chữ thường, xoá `renderStatus` chết
- [x] `source-capitals` + `product-transfer-requests`: thiếu `columnCustomizationMixin` → thêm mixin + `columnScreenKey` + nút Cấu hình cột + `ColumnCustomizationModal`

### Giữ nguyên có chủ ý

- Popup chọn hàng hoá/nhóm hàng của `services` giữ text "Thêm {n} hàng hoá" + icon `ri-add-line`
  vì bám đúng popup dùng chung `QuotationProductSearchModal` của Báo giá — sửa 1 màn sẽ lệch màn kia.
- `source-capitals` không có cột Mã (bảng `source_capitals` không có cột `code`) → link đặt ở Tên;
  không có cột Trạng thái vì `status` dùng làm xoá mềm, danh sách chỉ hiện bản ghi còn hoạt động.
- `works` / `cost-debts` không có nút Khóa/Mở khóa vì BE không có endpoint lock (trạng thái sửa trong form).

### Kết quả

20/20 màn đạt, 0 lỗi console ứng dụng (chỉ còn cảnh báo HMR của dev server khi vừa sửa file).
Thao tác đã test thật: Khóa → Mở khóa ở chi tiết tài khoản (dữ liệu trả nguyên trạng), vào thẳng
`/accounts/1/edit` khi bản ghi đang khoá → tự chuyển về màn Chi tiết, modal Xem của 9 màn danh mục.

---

## Lượt duyệt lại toàn bộ skill + 20 màn (2026-08-15, sau phản hồi của user)

Đọc lại 6 skill (`list-page` đủ 615 dòng, `button-convention`, `modal-popup`, `unsaved-changes`,
`form-validate`, `select-and-input-state`) rồi rà lại từng màn bằng 3 lớp: grep tĩnh · đo layout
bằng Playwright · thao tác thật.

### Lỗi mới phát hiện và đã sửa

- [x] **`/human/banks` — nút "Tạo mới" lệch và dính nút bên cạnh** (user chỉ ra): nút thừa class `mb-2`
      (đẩy lên 6px) và màn dùng slot `#actions` trong khi 19 màn kia dùng `#actions-bottom` —
      slot `actions` KHÔNG có `gap` nên 2 nút dính sát nhau. Đã đưa về `#actions-bottom` + `btn-compact`
      → cùng `top`, khoảng cách 10px như mọi màn.
- [x] **Ô lọc select cao 32px trong khi ô tìm nhanh 30px** → hàng lọc gọn lệch 1px ở mọi màn có ô chọn.
      Sửa ở `V2BaseSmartFilterPanel` (ép `select2`/`mx-datepicker` trong `.inline-field` về 30px).
- [x] **Căn lề (list-page mục 15)**: cột STT ở `accounts` và `currencies` để `align: 'left'` → `center`.
- [x] **Sortable (list-page "Cột nào được sort")** — chỉ cột định danh, Tên, tiền, ngày:
  - Bỏ sort sai nhóm: `accounts` (Bậc), `costs` (ĐM giảm giá, % Tính giá vốn, % VAT),
    `serials` (Tên hàng, Khách hàng, Người sửa, Người tạo), `note-maintenances` (Ký hiệu).
  - **11 màn không có cơ chế sort nào** (thiếu cả `@sort`/`handleSort`/`sort_by`): works, cost-debts,
    source-capitals, account-banks, product-transfer-requests, nations, areas, provinces, districts,
    wards, hamlets → thêm `:sortBy`/`:sortDirection`/`@sort` + `handleSort` + truyền `sort_by`/`sort_desc`.
  - **BE thiếu whitelist sắp xếp** → thêm cho: `WorkService`, `CostDebtService`, `SourceCapitalService`,
    `CompanyAccountService`, `BankService`, `NationService`, `AreaService`, `ProvinceService`,
    `WardService`, `DistrictService`, `HamletService`, `ProductTransferRequest::searchByFilter`.
    4 service địa lý trước đó đọc `sortBy` (tên FE không hề gửi) và **ghép thẳng vào `orderBy`** —
    vừa không ăn vừa hở SQL; nay đọc đúng `sort_by` qua whitelist.
  - `AccountService` / `TypeAccountService`: FE khai key cột dạng camel (`createdAt`) → thêm alias
    trong whitelist, nếu không bấm sort cột ngày sẽ im lặng không đổi.
  - `CurrencyService`: bổ sung `created_at` vào whitelist.
- [x] `/human/banks` còn 3 điểm lệch skill: cột "Chi nhánh" dùng `<a href="javascript:void(0)">` → `<button>`;
      badge tự map `1 → 'Hoạt động'` ở FE → dùng `status_text` BE trả về (bổ sung vào `BankListResource`);
      thiếu `filterStateMixin` (19 màn kia đều có); text "Khoá/Mở khoá" → "Khóa/Mở khóa".

### Đã rà và KHÔNG có vi phạm

`status-pill` · `font-weight-bold` trong ô · nút xám `disabledTitle` · `msgBoxConfirm` ·
`no-close-on-backdrop` · cờ quyền hard-code `true` · `rows="3"` chuỗi · "Lưu & Tiếp tục" ·
`v-b-tooltip`/`fa-info-circle` · `V2BaseSelect` trong modal · modal thiếu `hide-footer` ·
modal thiếu `unsavedModalMixin`/`markFormSaved` · thiếu deep watcher filter · thiếu `columnCustomizationMixin`
· thiếu import `v2-styles.scss` · `javascript:void(0)`.

### Ghi chú (không phải lỗi)

- `districts` / `hamlets` / `source-capitals` không có cột Trạng thái vì BE chỉ trả bản ghi đang hoạt động
  ("Xóa" = khóa mềm) — mọi dòng cùng trạng thái.
- Bảng `areas` hiện **0 dòng dữ liệu** trên DB gộp nên màn hiện "Không có dữ liệu" — không phải lỗi màn.
- `service-price-config` là màn form cấu hình, không phải màn danh sách → không áp bộ quy tắc bảng.

### Test đã chạy

Sort thật (2 chiều) trên works · nations · wards · banks · account-banks · cost-debts ·
product-transfer-requests; sort cột ngày của accounts và sort tên của type-accounts kiểm qua API.
Đo layout (top/height/gap của nút toolbar + ô lọc, tràn ngang) trên 20/20 màn. 0 lỗi console ứng dụng.

---

## Đợt bổ sung LỊCH SỬ THAY ĐỔI cho 18 màn danh mục (2026-08-15)

User chốt: mọi màn danh sách phải có nút **Lịch sử**; màn chi tiết / popup Xem phải có **khối**
Lịch sử trong thân trang (KHÔNG để nút ở footer, khuôn `/assign/customers/{id}`); padding nội dung
khối Lịch sử = **5px** đồng bộ mọi màn.

### BE — nền dùng chung

- [x] Bảng chung `catalog_histories` (`table_name` + `table_id`, subset-diff JSON, `note`, `changed_by`,
      `changed_at`) — khuôn bảng `files` dùng chung, thay vì 18 bảng `<entity>_history` cho 18 danh mục.
      Entity lớn (khách hàng, báo giá, phiếu) GIỮ NGUYÊN bảng riêng + `SystemLogService`.
- [x] `App\Services\CatalogHistoryService` — ghi (`log`/`logUpdate`/`logStatus`) + đọc (`getLogs`)
      trả **đúng hợp đồng DTO của `SystemLogService::finalize()`** để FE dùng lại `SystemInfoSection`.
      Whitelist 20 bảng + nhãn cột tiếng Việt khai tập trung ở `TABLES`.
- [x] `App\Services\Concerns\LogsCatalogHistory` — trait cho service danh mục (snapshot trước khi
      sửa → diff → chỉ ghi khi thực sự đổi).
- [x] Endpoint chung `GET /api/v1/catalog-histories/{table}/{id}` + `/filter-options`, whitelist bảng.
- [x] Gắn ghi log vào **17 service**: services · levels · note-maintenances · costs · currencies ·
      company_accounts · works · cost_debts · source_capitals · banks · nations · areas · provinces ·
      districts · wards · hamlets · product_transfer_requests.
      (serials là màn CHỈ ĐỌC — sửa serial nằm ở màn Quản lý khách hàng — nên chưa có chỗ ghi.)
- [x] Adapter đọc **log cũ kiểu version** (`account_versions`/`type_account_versions`) rồi trộn vào
      kết quả → accounts + type-accounts chuyển sang UI chung mà KHÔNG mất lịch sử đã có.
- [x] `ServiceService::unlock()` — chuyển thao tác Mở khóa từ controller vào service để có ghi log.

### FE

- [x] `SystemInfoSection` thêm 3 prop: `endpointBase` (dùng cho `catalog-histories`), `defaultOpened`,
      `hideHeader`; padding `.si-body` → **5px**.
- [x] **Bộ lọc trong khối Lịch sử GHIM cố định** (`.si-filter-sticky`) — cuộn danh sách log không mất
      nút Bộ lọc và các ô lọc (user phản hồi 2026-08-15).
- [x] `components/modal/CatalogHistoryModal.vue` — popup Lịch sử dùng chung, ruột là chính
      `SystemInfoSection` nên popup ở danh sách và khối ở chi tiết hiện GIỐNG HỆT nhau.
- [x] Thêm hành động **Lịch sử** vào menu ⋮ của **20/20 màn** danh sách (serials phải thêm hẳn cột
      Hành động vì màn chỉ đọc trước đó không có).
- [x] Nhúng khối Lịch sử vào **cuối popup Xem** của 15 modal danh mục (chỉ hiện ở chế độ Xem).
- [x] Màn chi tiết `accounts`: **bỏ nút Lịch sử khỏi `V2Footer`**, thay bằng khối `SystemInfoSection`
      trong thân trang; accounts + type-accounts bỏ `FinanceHistoryModal` → dùng popup chung.

### Skill đã cập nhật

- `list-page` mục 1: **mọi màn danh sách BẮT BUỘC có hành động "Lịch sử"**, không gate quyền.
- `entity-history` §5.1: thêm dòng "Popup XEM của màn danh mục" vào bảng 2 nơi hiển thị; ghi rõ
  Lịch sử ở màn chi tiết là **khối trong thân trang, không phải nút footer**; padding nội dung 5px;
  BỎ quy ước cũ "chi tiết mở dạng modal thì ẩn khối Lịch sử".

### Test đã chạy

Tinker: đổi 1 trường → 1 log 1 key; lưu không đổi gì → KHÔNG ghi log; khóa/mở khóa → 2 dòng nhóm
"Thay đổi trạng thái"; thứ tự mới → cũ. UI: popup Lịch sử ở works/nations/banks/currencies, khối
Lịch sử trong popup Xem (works, banks, nations, currencies), khối Lịch sử ở màn chi tiết accounts
(đọc được 8 dòng log cũ), bộ lọc ghim khi cuộn (đo `top` không đổi), padding 5px. 0 lỗi console.

### Chuẩn hoá POPUP dùng chung (2026-08-15, theo phản hồi của user)

- [x] **`components/modal/V2BaseModal.vue`** — khuôn popup dùng chung, chốt sẵn 3 thứ trước đây mỗi
      màn làm một kiểu: body cuộn riêng **padding `0.5rem`** (khuôn popup "Chọn trường xuất CSV"),
      **footer ghim đáy** (`sticky`, nằm ngoài vùng cuộn) và header (icon tròn + tiêu đề + dòng mô tả).
- [x] `CatalogHistoryModal` dựng lại trên `V2BaseModal`; dòng mô tả đổi thành
      `Vụ việc: RRP - Rủi ro theo phòng` — chữ xám `#6b7280` / giá trị `#374151`, **KHÔNG in đậm,
      KHÔNG màu đỏ**; truyền `record-prefix` đúng đối tượng cho 20 màn.
- [x] `CustomerHistoryModal` (màn khách hàng): bỏ in đậm tên bản ghi + ghim footer + tách vùng cuộn.
- [x] `V2BaseImportModal`: body `1rem` → `0.5rem`, footer `static` → `sticky` (popup Import trước đây
      thừa khoảng trắng và mất nút khi bảng preview dài).
- [x] Skill `modal-popup`: thêm **mục 0 — KHUÔN DÙNG CHUNG `V2BaseModal`** (kèm ví dụ + bảng chuẩn
      body/footer/header) và bổ sung checklist; mục 1 ghi rõ footer BẮT BUỘC ghim đáy.
- [x] `CLAUDE.md`: **chữ màu đỏ CHỈ dùng cho lỗi validate** (mô tả/phụ đề/ghi chú dùng chữ xám,
      không in đậm) + popup mới bắt buộc dựng trên `V2BaseModal`.

Đo lại sau khi sửa: popup Lịch sử — mô tả `rgb(107,114,128)`, giá trị `rgb(55,65,81)`, `font-weight 400`,
body padding `8px`, footer `sticky` và vẫn trong tầm nhìn sau khi cuộn hết. Popup Import — body `8px`,
footer `sticky`.

### Sửa tiếp sau phản hồi (2026-08-15)

- [x] **Popup Lịch sử danh mục bị "khung trong khung"**: `SystemInfoSection` luôn vẽ viền
      `1px #e5e7eb` + đường kẻ trên vùng nội dung; nằm trong popup (đã có khung riêng) thì thành 2
      lớp viền. Thêm class `si-borderless` — tự bật khi `hideHeader` (tức đang dùng trong popup).
- [x] **Popup Lịch sử khách hàng chưa ghim nút Bộ lọc**: bọc cụm lọc vào `.ch-filter-sticky`
      (`position: sticky; top: 0`), bỏ `pt-2` của vùng cuộn để không còn khe hở cho nội dung lọt lên
      trên nút. Đo lại: `sticky_top == body_top` (khe hở = 0) sau khi cuộn hết.
- [x] Popup Import: nội dung cách header 32px vì khối đầu body có `mt-3`. Triệt tận gốc trong
      `V2BaseModal` (`.v2-modal-body > :first-child { margin-top: 0 }`) + áp cùng luật cho
      `V2BaseImportModal`. Đo lại: khoảng cách header → nội dung còn **8px** (đúng bằng padding).

---

## Xuất file — popup "Chọn trường xuất file" cho mọi màn (2026-08-15, user chỉ ra thiếu)

Trước đợt này chỉ màn Khách hàng có popup chọn cột; các màn khác bấm Xuất là tải thẳng cả bảng.
**Skill cũng CHƯA có quy tắc** → đã bổ sung `list-page` **mục 14b** (kèm bảng lớp dùng chung + ví dụ).

### Hạ tầng dùng chung (mới)

- [x] BE `App\ExcelExport\ExportColumnRegistry` — khai `[key => nhãn]` cột xuất của từng màn, là
      nguồn DUY NHẤT cho cả popup FE lẫn header file; `resolve()` lọc `fields` qua whitelist
      (bỏ key lạ) và giữ ĐÚNG thứ tự user tick.
- [x] BE `App\ExcelExport\DynamicExport` + view chung `resources/views/exports/dynamic.blade.php` —
      cột động, tự chặn Excel hiểu nhầm công thức (`=`, `+`, `-`, `@` ở đầu chuỗi).
- [x] FE `utils/mixins/exportFieldsMixin.js` — mở popup, nhớ loại file, nhận cột user tick rồi gọi
      `runExport(type, fields)` của màn. Popup dùng lại `components/modal/export-fields-modal.vue`.

### Đã áp cho 10 màn có nút Xuất

`levels` · `note-maintenances` · `costs` · `services` · `serials` · `accounts` · `type-accounts` ·
`currencies` · `product-transfer-requests` · **`device-errors`** (màn user chỉ ra).

- 3 màn có Export class riêng vì định dạng đặc thù (`services` vá XML, `device-errors` có block
  tiêu đề + định dạng cột, `serials` dựng file ở FE bằng ExcelJS vì >20k dòng) → GIỮ class riêng,
  chỉ đổi nguồn cột sang `fields` của popup (`fields` ưu tiên, fallback tham số `columns` cũ).
- 7 màn còn lại chuyển sang `DynamicExport` + registry, bỏ Export class + blade cứng cột.

### Test

Popup mở đúng ở levels / device-errors / serials (số option khớp registry). 8/8 endpoint export trả
file 200. Đọc lại file thật của `levels` với `fields=created_at,name`: header ra **STT | Ngày tạo |
Tên cấp** — đúng thứ tự user tick, dữ liệu khớp. Registry test: key lạ bị loại, không truyền `fields`
thì xuất đủ cột (giữ hành vi cũ).

### Bộ lọc "Người thực hiện" trong lịch sử (2026-08-15, user chỉ ra)

- [x] `CatalogHistoryService::getFilterOptions()` trước đây trả `performers: []` (để FE tự suy từ
      log) → dropdown chỉ hiện 1-2 người. Nay trả **đủ nhân sự cùng công ty với người tạo bản ghi**,
      khuôn `SystemLogService::performerOptions()`; không suy được công ty thì trả tất cả.
      Endpoint `filter-options` truyền thêm `{table}` + `{id}`.
- [x] Skill `entity-history`: thay ghi chú cũ ("performers chỉ trả cho customer") bằng mục
      **Ô "Người thực hiện" — phải liệt kê ĐỦ nhân sự, KHÔNG suy từ log**, kèm cách kiểm nhanh.

Đo lại: works / nations / accounts đều trả **783** người — bằng đúng màn Khách hàng. Trên UI, ô
"Người thực hiện" của popup Lịch sử màn Vụ việc có 783 option (trước đó 1).
- [x] **Gộp logic "Người thực hiện" về 1 chỗ**: `App\Services\HistoryPerformerOptions`
      (`forCompany()` + `companyOfCreator()`). `SystemLogService` và `CatalogHistoryService` đều gọi
      helper này thay vì mỗi nơi một bản copy → sau này đổi quy tắc chỉ sửa 1 file.
      Đồng thời bỏ cổng chặn cũ ở `SystemLogService` (chỉ `customer` mới trả danh sách) → mọi loại
      đối tượng đều có danh mục người thực hiện.
      Đo lại: works 783 · khách hàng 783 (công ty của người tạo) · task/issue 1.063 (chưa suy được
      công ty → trả tất cả, đúng fallback).

---

## Phản hồi Redmine #11073 (ghi chú #12–#27, xử lý 2026-08-17)

Bỏ qua #13 (DM tài khoản mất data — user tự sửa).

### BE

- [x] `device_errors` vào `CatalogHistoryService::TABLES` + `DeviceErrorService` dùng
      `LogsCatalogHistory` (create/update/delete/lock/unlock) — ghi chú #17.
- [x] `areas`: bản đồ nhãn thiếu `nation_name` (service log theo cột này) → lịch sử hiện thô
      `nation_name`; thêm nhãn "Quốc gia", giữ `nation_id` cho log cũ — #16.
- [x] **#16 vẫn lỗi sau lần sửa đầu** (user báo lại 2026-08-17): `logUpdate()` đổi tên cột sang nhãn
      NGAY LÚC GHI rồi lưu thẳng nhãn làm khoá của `old_value`/`new_value` → mọi dòng log ghi TRƯỚC
      khi bản đồ nhãn có cột đó bị **đóng băng tên cột thô**, sửa TABLES không cứu được log cũ.
      Bổ sung map nhãn lần nữa khi ĐỌC (`changesOf()` nhận thêm `$table`) → log cũ của mọi bảng đều
      hiện đúng nhãn, không cần script sửa dữ liệu. Đã test: dòng `nation_name` cũ đọc ra "Quốc gia".
- [x] Thêm Người cập nhật cho danh mục địa lý: join `updated_by` ở `DistrictService`/`HamletService`,
      quan hệ `Nation::updater()` + eager load; resource trả `updated_by_name`
      (districts/hamlets/nations, alias thêm cho areas/wards/provinces) — #21, #22, #23.
- [x] `CustomerService`: whitelist sort thêm `updatedAt` → cột Ngày cập nhật sắp xếp được — #24.

### FE

- [x] Device errors: "Khôi phục" → **"Mở khóa"** ở cả danh sách lẫn chi tiết — #12.
- [x] `HamletModel`: khối Lịch sử bị lồng trong ô Tỉnh/TP → đưa xuống CUỐI form — #14.
- [x] Popup Xem của 11 danh mục còn để `md` → `:size="isView ? 'lg' : 'md'"` cho khối Lịch sử đủ
      chỗ (bảng lọc không bị bó) — #15.
- [x] Device errors: thêm hành động **Lịch sử** ở menu ⋮ (CatalogHistoryModal) + khối
      `SystemInfoSection` trong thân màn chi tiết — #17.
- [x] **Mất data ở 2 màn** (`finance/type-accounts`, `finance/product-transfer-requests`): dòng
      `params.fields = fields.join(',')` bị dán nhầm vào `loadData()` — `fields` không tồn tại nên
      ném ReferenceError, bảng luôn rỗng. Gỡ bỏ (bản đúng nằm trong `runExport`) — #18, #27.
- [x] Chuẩn hoá nhãn toàn bộ màn danh mục: "Người sửa"/"Người sửa (gần nhất)" → **Người cập nhật**,
      "Ngày sửa" → **Ngày cập nhật**, "Người lập" → **Người tạo** (works, cost-debts, accounts,
      type-accounts, banks, costs, services, serials, device-errors, customers) — #19, #20, #24.
- [x] Danh mục địa lý: thêm cột **Người cập nhật** (nations, areas, provinces, districts, wards,
      hamlets) — #21, #22, #23.
- [x] **Chốt lại 2026-08-17 (user quyết)**: cột Người cập nhật / Ngày cập nhật **ẩn mặc định ở TẤT
      CẢ màn danh mục**, kể cả màn địa lý và màn Khách hàng — giữ đúng `list-page` mục 6 (bảng mặc
      định gọn, user tự bật ở "Cấu hình cột hiển thị"). KHÔNG chia màn này hiện / màn kia ẩn.
- [x] Khách hàng: thêm cột **Ngày cập nhật** (`updatedAt`) + đổi tiêu đề màn/tab thành
      **"Danh mục khách hàng"** — #24, #25.
- [x] Dịch vụ sửa chữa & chi phí khác: bỏ ô lọc "Người cập nhật" → còn 2 ô + tìm nhanh nên
      `V2BaseSmartFilterPanel` tự chuyển sang **bộ lọc gọn 1 hàng** — #26.

### Checkpoint — 2026-08-17
Vừa hoàn thành: 15/16 ghi chú phản hồi của #11073 (BE + FE).
Đang làm dở: chưa chạy kiểm thử UI trên cổng 3002/8003.
Bước tiếp theo: user xác nhận có cần verify bằng Playwright không, sau đó phản hồi lại Redmine.
Blocked:

### Footer che nội dung cuối trang (2026-08-17, user báo ở màn chi tiết device-errors)

- [x] `components/V2Footer.vue`: thanh nút là `position: fixed` nên không chiếm chỗ trong luồng →
      nội dung cuối trang bị đè. Bọc thêm khối TĨNH `.v2-footer-spacer` cao **66px** (50px thanh nút
      + 16px khoảng thở) ngay trong component → **mọi màn dùng V2Footer tự có chỗ trống ở đáy**,
      không phải tự thêm `margin-bottom`/`padding-bottom` ở từng trang.
- [x] Gỡ 7 miếng vá thủ công ở các màn đã dùng V2Footer (nếu giữ sẽ chừa chỗ 2 lần):
      `summary-quotations` (add/edit/index), `BillPaymentRequestForm`, `BillIncomeRequestForm`,
      `CustomerForm`, `meeting/_id/show`. Các màn KHÔNG dùng V2Footer (bom-list, quotations,
      contracts, EquipmentTab…) giữ nguyên vá cũ vì chúng chừa chỗ cho footer khác.

### Bổ sung cột Người/Ngày cập nhật cho 5 màn còn thiếu (2026-08-17, user chỉ ra)

Cột **ẩn mặc định** đúng chuẩn đã chốt — user bật ở "Cấu hình cột hiển thị".

- [x] **BE — quan hệ `updater()`/`employee_update()` + eager load + trả `updated_by_name`**:
      `Level`, `NoteMaintenance`, `Currency`, `CompanyAccount`, `ProductTransferRequest`.
      3 Resource dùng helper `creatorName()` được bổ sung `updaterName()` cùng khuôn (chỉ đọc khi
      quan hệ đã eager load → không sinh N+1).
- [x] **BE — `ExportColumnRegistry`**: thêm `updated_by_name`/`updated_at` cho `note_maintenances`
      và `currencies` (2 màn export dùng chính Resource nên dữ liệu có sẵn). `product_transfer_requests`
      KHÔNG thêm vì màn đó dùng Export class riêng.
- [x] **FE — thêm cột**: `levels`, `note-maintenances` (thiếu Người cập nhật) · `currencies`,
      `account-banks`, `product-transfer-requests` (thiếu cả Người + Ngày cập nhật).
      Popup "Chọn trường xuất file" của note-maintenances / currencies đồng bộ theo registry.

Đo lại bằng tinker: levels · note_maintenances · currencies · company_accounts ·
product_transfer_requests đều trả `updated_by_name` + `updated_at`
(vd PYCCH-07359 → "Võ Thị Hà" / 27/07/2026 16:47).

### Luồng GHI Người cập nhật của Khu vực / Quốc gia (2026-08-17, user báo "chưa thấy được")

Thêm cột ở FE là chưa đủ — cột trống vì **BE không ghi `updated_by` đúng**. 2 nguyên nhân khác nhau:

- [x] **Quốc gia**: `Nation` kế thừa `Model` THUẦN (không phải `BaseModel`) nên KHÔNG có hook audit
      -> `nations.updated_by` luôn `NULL` (kiểm DB: 100% bản ghi null, kể cả bản vừa sửa hôm 15/08).
      `NationService`: set tay `updated_by` (và `created_by` lúc tạo) ở create/update/lock/unlock.
- [x] **Khu vực**: `Area::boot()` còn 2 hook đồng bộ ERP thời chưa gộp DB. Sau gộp, `TpArea` trỏ về
      **CHÍNH bảng `areas`** -> hook `updated` ghi đè lên bản ghi vừa lưu và đóng dấu
      `updated_by = auth()->user()->info->id` (**id bảng `employee_infos`**) trong khi cột lưu
      `employees.id`. Kết quả: `areas.updated_by = 6` — id không tồn tại trong `employees` -> join
      ra rỗng -> cột trống. **Gỡ hẳn 2 hook**; service tầng trên đã bỏ đồng bộ từ trước (có comment).
- [x] **Lỗi y hệt ở `Province` và `Ward`** (TpProvince → `provinces`, TpWard → `wards`): gỡ luôn,
      nếu không Tỉnh/TP và Phường/xã sẽ trống cột Người cập nhật đúng theo cách này.
- [x] Bỏ `use MasterSetting` / `use Log` đã chết ở 3 entity.

Đo lại (tinker, user id 13): areas sửa → 13 · areas khóa/mở khóa → 13 · nations sửa → 13;
đọc qua Resource danh sách: AREA `updated_by_name = "DNS Admin"`, NATION `updated_by_name = "DNS Admin"`.
