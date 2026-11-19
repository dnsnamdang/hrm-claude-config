---
name: app-ui-convention
description: CỬA VÀO bộ quy chuẩn TPE_APP (app Flutter gắn với HRM) — đọc ĐẦU TIÊN khi làm / sửa bất kỳ màn nào của app. Gồm mục lục các skill app-*, quy tắc nền (bám skill web, phạm vi, dùng component chung), nút bấm (widget, chữ, thứ tự, icon tự động), hộp thoại xác nhận, định dạng số / nhân viên / danh mục khoá, thông báo. Dùng khi user nói "làm cho giống web", "đồng bộ các màn", "mỗi màn 1 kiểu", "nút này sai màu / sai chữ / thiếu icon".
---

# Quy chuẩn TPE_APP — cửa vào chung

App `TPE_APP` (Flutter, thư mục `HRM/TPE_APP`, repo riêng) là **mặt di động của HRM**: dữ liệu + nghiệp vụ ở
`hrm-api`, chuẩn giao diện bám skill web `hrm-client`. Vì skill chỉ được nạp khi mở Claude ở `HRM/` (đã thử
29/10/2026: skill thư mục con `skills/app/...` không được nạp, mở Claude trong `TPE_APP` không thấy skill của
`HRM/`) → **luôn mở Claude ở `HRM/`**, mọi skill app nằm chung `HRM/.claude/skills/` với tiền tố `app-`.

## Mục lục skill app — đọc đúng skill theo việc

| Việc | Skill |
|---|---|
| Bất kỳ màn nào (đọc trước) | `app-ui-convention` (file này) |
| Tra component có sẵn trước khi dựng UI — "cái này dùng widget nào" | `app-components` |
| Khung phân hệ: màu, header, vân nền, tab, nút giữa "Tạo mới", menu trái | `app-module-shell` |
| Màn danh sách: tìm + lọc, nhóm, thẻ, rỗng, kéo tải lại | `app-list-page` |
| Màn tạo / sửa (form): ô nhập, bàn phím, chọn nhân sự / khách hàng, lỗi BE, chưa lưu | `app-form` |
| Màn chi tiết / Hub: đầu thẻ, dòng xem, hành động, menu ⋮ | `app-detail-page` |
| Gọi API hrm-api, model, lỗi 422, khi nào phải sửa BE | `app-hrm-api` |
| Thông báo: loại → màn mở, push, nhắc hạn | `app-notification` |
| Test E2E trên simulator từng bước (`step.sh` mỗi thao tác, ma trận trạng thái — bắt buộc trước khi báo xong) | `app-simulator-test` |
| Scaffold màn mới (cấu trúc thư mục, route, DI) | `app-new-screen` |
| Model freezed / json | `app-new-model` |
| Review code / trước khi commit | `app-review` |
| Build TestFlight / CH Play | `app-build-release` |

**Chuẩn là bộ QUY TẮC CHUNG trong các skill `app-*`, KHÔNG phải một màn cụ thể** (user chốt 29/10/2026). Meeting
(`ui/meeting/`) và Việc của tôi (`ui/my_todo/`) chỉ là nguồn đã dùng để rút ra quy tắc + ví dụ tham khảo cách code;
chính 2 màn này chỗ nào lệch quy tắc chung thì cũng phải sửa theo quy tắc. Không chép nguyên 1 màn làm khuôn.

## Quy tắc nền

**Bám web (user chốt 23/10/2026):** app dùng CHUNG bộ quy tắc với web. Skill web quyết định **nghiệp vụ + chữ +
nhóm màu**. Các skill `app-*` chỉ ghi phần **chuyển sang Flutter** và chỗ app **khác web có lý do** (màn hẹp,
thao tác 1 tay). Gặp quy tắc web chưa có → đọc skill web gốc ở `HRM/.claude/skills/<tên>/SKILL.md`, áp tương
tự, rồi bổ sung vào skill app tương ứng.

**Phạm vi (user chốt 23/10/2026):** Meeting + MỌI màn mới / màn đang sửa. Màn cũ chưa đụng tới để nguyên,
KHÔNG sửa đại trà — sửa màn nào chuẩn hoá màn đó. Ngoại lệ: thay đổi nằm trong widget dùng chung (vd icon nút,
đóng bàn phím) thì tự áp mọi màn — đó là cách đồng bộ rẻ nhất.

**Component chung trước, màn sau:** tra `app-components` trước khi dựng. Thiếu → tạo trong `lib/custom_view/`
(export ở `custom_view.dart`) + ghi vào `app-components`, KHÔNG dựng riêng trong màn. Sửa widget chung đang
có (đổi hành vi màn cũ) → hỏi user trước, trừ khi user đã yêu cầu áp toàn app.

**Thứ tự ưu tiên (user chốt 29/10/2026): QUY TẮC CHUNG + COMPONENT CHUNG của app > file thiết kế.**
Thiết kế `.pen` (meeting-mobile_v2.pen, mytodo.pen — Pencil chỉ đọc được file đang mở) vẽ từng màn, có thể chưa
đồng nhất với component / quy tắc chung đang dùng (vd thiết kế ghi nút cao 48, chung là 44; thiết kế còn nút
"Giao việc", chung đã đổi tên). Nên:
- Mặc định làm theo quy tắc chung + component chung; lấy thiết kế cho **bố cục, nội dung, thứ tự thông tin** của màn.
- Muốn **làm khác quy tắc chung** (theo thiết kế hay theo ý mình) → **HỎI user trước**, nêu: quy tắc chung nói gì ·
  thiết kế / đề xuất nói gì · đề nghị chọn bên nào. KHÔNG tự chọn im lặng.
- Chốt xong → ghi "Quyết định đã chốt" của skill liên quan (nếu đổi quy tắc chung thì sửa luôn quy tắc + component).
- Đổi BE / dữ liệu hiển thị (thêm-bớt trường, API) cũng phải báo user duyệt.

**Đồng bộ web ↔ app:** sửa nghiệp vụ một bên thì kiểm bên kia (tên loại, nhãn, luồng trạng thái, menu Tạo
mới…). Tên gọi trên app = tên trên web (vd "Phiếu giao việc (chấm công)").

---

## 1. Nút bấm (web: `button-convention`)

### 1a. Widget ↔ variant web

| Web | App (`custom_view/primary_button.dart`) | Dùng cho |
|---|---|---|
| `primary` | `PrimaryButton` (gradient màu phân hệ) | Hành động chính: Lưu · Tạo mới · Xác nhận · Duyệt · Gửi duyệt · Lên lịch · Chốt lịch · Hoàn thành |
| `secondary` / `tertiary` | `SecondaryButton` (trắng, viền xám) | **Lưu nháp** · Hủy · Đóng · Quay lại · Làm mới · hành động phụ |
| `primary status="danger"` | `DangerButton` (nền đỏ nhạt, chữ đỏ) | CHỈ Xóa · Từ chối · Hủy phiếu (không hoàn tác) |
| `primary status="warning/success"` | *(chưa có)* | Khóa (cam) / Mở khóa (xanh lá). Khi cần → thêm tham số màu vào `PrimaryButton`, hỏi trước |

- **Lưu nháp LUÔN là `SecondaryButton`**, mọi bước làm luồng tiến lên (Lên lịch, Chốt lịch, Gửi duyệt,
  Hoàn thành) dùng `PrimaryButton` **cùng màu chính, không tô màu riêng từng bước** (user chốt
  23/10/2026 theo bảng skill, dù footer web meeting đang tô Chốt lịch cam / Hoàn thành xanh lá).
- **Lưu** (lưu thường, không đổi trạng thái) = `PrimaryButton`.
- Không dùng `ElevatedButton` / `TextButton` / `OutlinedButton` / `CommonButton` tự tô màu cho nút hành động.
- Nút đang gọi API: `onPressed: _busy ? null : …` + `GlobalLoading.show()` ngay trước lệnh gọi,
  `hide()` khi xong (cả nhánh lỗi) — tương đương `$safeLoadingStart/Finish` + `interactable` của web.
  Không đổi chữ nút thành "Đang lưu…" ở màn mới (đã có lớp tải).

### 1b. Chữ trên nút — dùng ĐÚNG bảng text chuẩn mục 4.2 của `button-convention` web

Hay sai nhất trên app:

| Chuẩn | KHÔNG dùng |
|---|---|
| **Hủy** · **Xóa** · **Khóa** · **Mở khóa** (dấu kiểu mới) | Huỷ · Xoá · Khoá · Mở khoá |
| **Hủy** (nút thoát trong hộp thoại) | Không · Huỷ bỏ · Thoát |
| **Xác nhận** | Đồng ý · OK · Xong |
| **Sửa** | Chỉnh sửa · Sửa thông tin · Cập nhật |
| **Lưu** | Cập nhật · Lưu lại · Thêm (ở popup sửa / thêm 1 dòng) |
| **Duyệt** / **Từ chối** | Phê duyệt / Không duyệt |
| **Lưu và …** | Lưu & … (không dùng ký hiệu `&`) |

- Tối đa 3 từ; nêu rõ đối tượng khi chữ trần dễ nhầm ("Hủy meeting" trong menu ⋮, vì "Hủy" trần
  giống nút đóng menu). Đã rõ ngữ cảnh thì không thêm đối tượng ("Xóa", không "Xóa meeting nháp").
- 2 màn làm cùng 1 việc phải cùng chữ (vd màn con soạn nội dung rồi trả về màn cha: đều là "Xác nhận").
- Chữ trạng thái / danh mục do BE trả (status_name…) KHÔNG phải chữ nút — hiển thị nguyên văn BE.

### 1c. Thứ tự + vị trí — KHÁC web có chủ đích

Thanh nút đáy (`BottomActionBar`), trái → phải: **nút trắng (Lưu nháp / Hủy / Quay lại) trước, nút
chính ngoài cùng bên PHẢI** (gần ngón cái; web đặt Đóng cuối cùng bên phải vì chuột). Nhiều nút
chính thì nút làm luồng tiến xa nhất đứng cuối: `Lưu nháp · Lên lịch · Chốt lịch`.
**Bottom sheet có hàng nút ở đáy** (đổi trạng thái, bảng lọc, nhập nhanh…) theo ĐÚNG thứ tự thanh nút đáy: `[Hủy | nút chính]`
— sheet nằm ở mép dưới, nhìn và cầm như thanh nút đáy (user báo 30/10/2026: sheet để Hủy phải đặt cạnh form để Hủy trái
là "thứ tự button không đồng nhất").
Hộp thoại NỔI GIỮA MÀN (`showAppConfirm`, `AppDialog`): **giống web** — nút hành động trước (trái), `Hủy` / `Đóng` LUÔN
cuối cùng (phải) (user chốt 28/10/2026: "phải đồng bộ web, app"). Cảnh báo chưa lưu (3 nút) xếp dọc, nút chính trên cùng.

- Icon trên nút: **MỌI nút đều có icon** (user chốt 29/10/2026 "đồng bộ có icon hết", thay quy ước cũ
  "không bắt buộc"). KHÔNG phải tự khai: `PrimaryButton` / `SecondaryButton` / `DangerButton` tự lấy icon theo
  chữ qua `appButtonIcon()` (custom_view/primary_button.dart) — bảng bám icon web (Lưu `save_outlined`, Gửi
  `send_rounded`, Duyệt/Xác nhận `check_rounded`, Từ chối `highlight_off_rounded`, Hủy/Đóng `close_rounded`, Xóa
  `delete_outline_rounded`, Sửa `edit_outlined`, Thêm/Tạo `add_rounded`, Lên lịch `event_rounded`…). Chỉ truyền
  `icon:` khi cần icon khác bảng; chữ mới chưa có trong bảng thì THÊM vào `appButtonIcon()`, đừng để nút trơn.
  Thanh 3 nút (Lưu nháp · Lên lịch · Chốt lịch) có icon vẫn vừa màn 393pt (đã xem simulator).
- Hành động thứ yếu / nguy hiểm (Sửa, Hủy meeting, Xóa, In) gom vào menu ⋮ ở header → bottom sheet
  "Hành động"; mục nguy hiểm chữ + icon đỏ.

### 1c-2. Mỗi hành động chỉ 1 lối vào trên 1 màn (user hỏi 23/10/2026)

KHÔNG đặt cùng 1 hành động ở 2 chỗ (vd icon ➕ trên header VÀ nút "Thêm" ngay nhóm) — người dùng
tưởng là 2 việc khác nhau. Chọn 1:
- Màn có NHIỀU nhóm (Phía Công ty / Phía Khách hàng…) → nút có chữ đặt **tại tiêu đề từng nhóm**
  (`MeetingGroupHeader.actionLabel`), header KHÔNG có ➕ (icon trên header không nói thêm vào nhóm nào).
- Màn 1 danh sách đang sửa → nút / dòng có chữ ở cuối danh sách ("Thêm nội dung trao đổi"), không ➕ header.
- Màn chọn (picker) → ➕ header là lối thường trực; nút to ở trạng thái rỗng là ngoại lệ được phép
  (gợi ý khi tìm không ra), cùng điều kiện quyền.
- Chữ: **"Thêm"** = chọn / nhập 1 dòng vào danh sách; **"Thêm nhanh <đối tượng>"** CHỈ khi tạo mới bản
  ghi danh mục ngay tại chỗ (Thêm nhanh khách hàng / người liên hệ).

### 1d. Nút không dùng được thì ẨN, không disable (CLAUDE.md HRM)

Áp mọi lý do (không quyền, sai trạng thái, đã khóa). Điều kiện đọc từ cờ BE (`can_edit`,
`can_manage`, `is_can_delete`…) giống web, danh sách và chi tiết cùng 1 điều kiện. Ẩn nút vì KHÔNG CÓ QUYỀN
thì im lặng — không hiện dải / thẻ "Chế độ chỉ xem" giải thích (user bỏ 23/10/2026); dải trạng thái chỉ
dùng cho trạng thái của bản ghi (đã hủy, đã hoàn thành, quá hạn). Ẩn vì CHƯA ĐỦ ĐIỀU KIỆN mà BE có trả lý do
(vd `complete_blocked_reason`) → `BottomActionBar(note: lý do)` — dòng xám trên hàng nút (web làm mờ nút + tooltip). Cờ quyền khởi tạo
`false` (fail-closed) — vd `_canCreate = false` rồi mới bật theo `my-permissions`.

---

## 2. Hộp thoại (web: `modal-popup` mục 3a + `button-convention` 6c)

Widget chung `lib/custom_view/app_dialog.dart` (user chốt 23/10/2026 — khuôn meeting, tương đương
`base-confirm-modal` web): icon tròn + tiêu đề + câu mô tả + hàng nút.

| Việc | Dùng |
|---|---|
| Hỏi Có / Không trước thao tác ghi | `await showAppConfirm(context, title:, message:, acceptText:, danger:)` → `bool` |
| Thoát màn form khi chưa lưu | `await showUnsavedChangesDialog(context, screenName:)` → `UnsavedChoice` |
| Hộp thoại có nội dung riêng (chọn lý do, so giờ cũ / mới…) | `AppDialog(content: …, actions: [...])` |
| Nhập lý do (Từ chối, Không duyệt…) | `ReasonInputDialog` (có sẵn) — truyền rõ `confirmLabel` / `cancelLabel` chuẩn |

- **Bắt buộc hỏi** trước: Xóa · Hủy · Từ chối · Hoàn thành · Chốt · Gửi duyệt / Lên lịch (gửi đi cho
  người khác) · Khóa. KHÔNG hỏi cho Lưu nháp / Lưu / mở màn / lệnh đọc.
- `message` nêu **mã + tên bản ghi + hệ quả** ("TPE.MET… - Họp giao ban sẽ bị xóa hẳn, không khôi
  phục được."), không hỏi trống "Bạn có chắc không?".
- `acceptText` = đúng chữ trên nút vừa bấm (Xóa / Lên lịch / Hoàn thành), không để "Xác nhận" chung.
- `danger: true` CHỈ cho Xóa / Từ chối / Hủy phiếu; nhóm duyệt / gửi / chốt là bước tiến → nút màu chính.
- Hỏi TRƯỚC khi `GlobalLoading.show()`.
- Màn mới KHÔNG tự dựng `AlertDialog` / `CupertinoAlertDialog` / `showDialog` + `Column` nút riêng.
  (Hiện còn ~40 file màn cũ tự dựng — để nguyên, sửa khi đụng tới màn đó.)
- Chọn 1 trong danh sách → bottom sheet (`showModalBottomSheet`), không dùng hộp thoại.

---

## 3. Form → xem `app-form` · 4. Danh sách → xem `app-list-page`

(Đã tách thành skill riêng 29/10/2026 — giống web tách `form-validate` / `list-page`.)

## 5. Chọn / hiển thị dữ liệu (web: `select-and-input-state`, CLAUDE.md HRM)

- Nhân viên hiển thị `Tên - Mã phòng - Mã NV`.
- Danh mục đã khóa mà bản ghi đang dùng vẫn phải hiện đúng tên (thêm vào danh sách chọn nếu thiếu).
- Danh mục cache trong app: tải lại khi mở form (loại mới thêm trên web phải thấy ngay) — vd
  `MeetingTypeCache.load(refresh: true)`.
- **Số theo chuẩn quốc tế** `1,234,567.89`: `NumberFormat('#,##0', 'en_US')`. KHÔNG dùng locale `vi`
  cho SỐ (ngày giờ vẫn `dd/MM/yyyy`). (Còn 2 chỗ cũ dùng `LocaleConstants.vi` — sửa khi đụng tới.)

## 6. Thông báo (web: `notification-convention`)

Nội dung do BE dựng (`[PREFIX] Nhóm hành động: Tên. Ghi chú`, ≤ 180 ký tự, `note_full` cho "Xem
thêm"). App chỉ hiển thị + deep-link theo `type` / `id`; không tự ghép câu thông báo ở app.

### 6a. Báo kết quả thao tác (web: toast `plugins/toast.js`) — user chốt 29/10/2026

User: "lưu xong chưa hiện thông báo thành công như web — đồng bộ kiểu thành công / thất bại cho app".

- **MỌI thao tác ghi thành công phải báo** (Lưu, Lưu nháp, Lên lịch, Duyệt, Hủy, Xóa, Xác nhận…), kể cả khi
  sau đó `pop()` về danh sách — toast nằm ở tầng gốc nên không mất khi chuyển màn.
- Gọi `navigator.showSuccessSnackBar(...)` / `showErrorSnackBar(...)` (đã đổi sang `AppToast`: đầu màn dưới tai
  thỏ, nền xanh lá `#16A34A` + ✓ / đỏ `#DC2626` + ✕, thành công 2,5s · lỗi 4s, chạm / vuốt lên để ẩn).
  KHÔNG tự dựng `SnackBar` / `Fluttertoast` / dải màu riêng.
- **Câu thành công theo web**: tạo → `Thêm mới thành công` · sửa / lưu / đổi trạng thái / hủy → `Cập nhật thành công`
  · xóa → `Xóa thành công`. Thao tác đặc thù đã có câu riêng ở web thì dùng đúng câu đó (`Duyệt thành công`,
  `Gửi duyệt thành công`, `Đăng ký phòng thành công`…). Không tự chế câu kiểu "Đã lưu nhắc việc".
- **Lỗi**: lỗi gắn được ô → đỏ dưới ô (`app-form` mục 3) + 1 toast lỗi `Vui lòng kiểm tra dữ liệu nhập`;
  lỗi chung → toast lỗi nguyên văn BE. Tick checkbox / đổi chip lọc không cần toast thành công.
- **Hình thức** (user duyệt 29/10/2026): viên gọn nền tối `#1F2937`, chỉ icon mang màu, rộng theo chữ, căn giữa.
- **Câu lỗi chuẩn** (`AppMessages` trong `custom_view/app_toast.dart`): câu đầy đủ, viết hoa đầu câu, không
  "nhé", không tiếng Anh / mã lỗi kỹ thuật.

  | Tình huống | Câu | Nút |
  |---|---|---|
  | Mất mạng / không tới được máy chủ / quá giờ chờ | Mất kết nối mạng. Vui lòng thử lại. | Thử lại |
  | Máy chủ lỗi (≥ 500) | Đã xảy ra lỗi hệ thống. Vui lòng thử lại. (QLDA_010) | Thử lại |
  | Không có quyền (403, câu BE tiếng Anh) | Bạn không có quyền thực hiện chức năng này. (QLDA_012) | — |
  | Lỗi 1 trường không có ô trên màn đang mở | `<Tên trường>: <câu BE>` — vd `Nhân sự tham gia (phía Công ty): Bắt buộc phải nhập` | — |
  | Lỗi app không đọc được | Không lưu được, vui lòng thử lại | — |

  `navigator.showErrorSnackBar` tự đổi câu kỹ thuật (chuỗi exception, SQL / PHP, "Server Error") qua
  `AppMessages.friendly`. Lỗi lưu dùng `MeetingSaveError.from(e)` → `.summary`, `.retryable` (chỉ lỗi mạng /
  hệ thống mới có nút: `showErrorSnackBar(err.summary, onRetry: err.retryable ? _save : null)`), tên trường ở
  `MeetingSaveError.fieldLabels` / `describe()`.

---

## Checklist trước khi báo xong 1 màn

- [ ] Nút đúng widget theo 1a; Lưu nháp trắng; Xóa / Từ chối mới đỏ
- [ ] Chữ nút đúng bảng 1b (Hủy / Xóa / Khóa / Xác nhận / Sửa, không `&`)
- [ ] Thứ tự 1c: nút trắng trái, nút chính phải
- [ ] Nút không dùng được đã ẩn (không disable), điều kiện theo cờ BE
- [ ] Thao tác ghi khó hoàn tác có `showAppConfirm` nêu mã + tên + hệ quả, `acceptText` đúng chữ nút
- [ ] Không còn `AlertDialog` / `CupertinoAlertDialog` tự dựng trong màn
- [ ] Form: chỉ kiểm định dạng, lỗi BE tô đỏ đúng ô; có cảnh báo chưa lưu
- [ ] Số `en_US`; badge chữ + màu từ BE
- [ ] `fvm dart analyze` không thêm lỗi (mức chuẩn 173 info); đã test theo `app-simulator-test` (mọi bước `step.sh` sạch lỗi + đủ mục 4)

## Quyết định đã chốt

- 23/10/2026 — Màu nút đổi trạng thái theo bảng skill (Lưu nháp trắng, các bước tiến cùng màu chính),
  không theo footer web meeting (Chốt lịch cam / Hoàn thành xanh lá).
- 23/10/2026 — Khuôn hộp thoại chung = khuôn meeting (`AppDialog` / `showAppConfirm`).
- 23/10/2026 — Phạm vi chuẩn hoá: Meeting + màn mới / màn đang sửa; màn cũ để nguyên tới khi đụng.
- 23/10/2026 — Lên lịch / Chốt lịch hỏi xác nhận (skill 6c) dù web meeting hiện chưa hỏi.
- 28/10/2026 — Hộp thoại: nút hành động trước, Hủy/Đóng cuối (giống web).
- 29/10/2026 — Bỏ hàng chip lọc nhanh (`quickChips`) ở mọi màn danh sách; không đặt nút ↻ / pill lọc riêng (Việc của tôi dùng ListFilterBar như các màn khác).
- 29/10/2026 — Màn rỗng danh sách dùng 1 khuôn: "Không có dữ liệu." / "Không có dữ liệu phù hợp.".
- 29/10/2026 — Mọi nút có icon, tự lấy theo chữ (`appButtonIcon`), thay quy ước cũ "icon không bắt buộc".
- 29/10/2026 — Chạm ra ngoài ô nhập là đóng bàn phím ở MỌI màn (gắn ở `my_app.dart`), ô bị khoá chạm vào cũng đóng.
- 29/10/2026 — Chọn nhân sự toàn trang (`pickEmployee`) thay hộp thoại `ChonNvPage`; tab con / nút gạt chuyển bằng con trượt.
- 29/10/2026 — Skill app chuyển về `HRM/.claude/skills/app-*` (1 chỗ với skill web); mở Claude ở `HRM/`.
- 29/10/2026 — Quy tắc chung + component chung của app ưu tiên hơn file thiết kế; làm khác quy tắc chung phải hỏi user.
- 29/10/2026 (ĐỀ XUẤT, chờ user duyệt) — Màn mới chỉ 2 kiểu: BLoC (màn nhiều trạng thái, như Hub Meeting) hoặc
  StatefulWidget + ApiService (như Việc của tôi); không Riverpod mới. Kích thước: dùng kích thước của component chung
  (nút 44…); phần riêng của màn lấy theo số đo thiết kế (pt); không bắt buộc `Dimen` / `CommonText` ở màn mới.
