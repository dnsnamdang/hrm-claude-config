---
name: notification-convention
description: Use when tạo/sửa bất kỳ thông báo nghiệp vụ nào (notification bắn cho user qua chuông/push/socket) ở BE hoặc FE — chuẩn nội dung, prefix, độ dài, in đậm, deep-link theo tài liệu QLDA
---

# Skill: Notification Convention (Thông báo nghiệp vụ)

Áp dụng cho **mọi màn**, mọi module: khi nghiệp vụ có bắn thông báo cho người dùng
(tạo mới, duyệt, từ chối, nhắc hạn, comment…) thì nội dung + hành vi click phải theo chuẩn dưới đây.

> Chỉ nói về **Thông báo nghiệp vụ**. Lỗi validate / toast kết quả thao tác
> ("Bạn chưa nhập đầy đủ thông tin", "Cập nhật thành công"…) xem mục 6.

---

## 1. Cấu trúc nội dung bắt buộc (Template Standard)

```
[{PREFIX}] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú bổ sung}
```

| Thành phần | Quy tắc |
|---|---|
| `[PREFIX]` | Mã đối tượng trong ngoặc vuông, viết hoa |
| `{Nhóm hành động}` | Lấy đúng 1 giá trị trong bảng mục 2, kết thúc bằng dấu `:` |
| `{Tên đối tượng}` | Tiêu đề Task/Meeting/Giải pháp… **tối đa 50 ký tự**, dài hơn thì cắt và thêm `...` |
| `{Ghi chú bổ sung}` | Ngắn gọn: deadline, thời gian họp, lý do từ chối. Không bắt buộc |

Ví dụ:
- `[MET] Tạo mới: Họp chốt phương án TKT. Thời gian: 14:00 12/08. Hình thức: Online.`
- `[TASK] Từ chối: Khảo sát hiện trạng kho A. Lý do: thiếu ảnh hiện trường.`

---

## 2. Nhóm hành động (chỉ dùng 16 giá trị này)

`Tạo mới` · `Cập nhật` · `Chờ duyệt` · `Đã duyệt` · `Từ chối` · `Yêu cầu làm lại` ·
`Góp ý` · `Sắp đến hạn` · `Quá hạn` · `Hủy` · `Tạm dừng` · `Tiếp tục` ·
`Thay đổi lịch` · `Nhắc báo cáo` · `Không duyệt` · `Chờ tính giá`

> Bổ sung 17/10/2026 (luồng tính giá): `Không duyệt` dùng khi chứng từ có trạng thái tên đúng "Không duyệt" (vd `[YCTG] Không duyệt: …`) — đồng bộ nút / trạng thái / lịch sử; `Chờ tính giá` dùng khi gửi YC tính giá (trạng thái "Chờ tính giá", vd `[YCTG] Chờ tính giá: …`). Màn khác vẫn dùng `Từ chối` / `Chờ duyệt` như cũ.

Không tự chế nhóm hành động mới. Không viết câu tự do kiểu
"Nguyễn A đã trả lời bình luận của bạn trong task X" — phải quy về `[TASK] Góp ý: {Tên task}. …`.

## 3. Prefix (tiền tố)

Prefix là **mã viết tắt của loại đối tượng**, đặt trong ngoặc vuông, viết hoa —
ưu tiên trùng với mã đối tượng đã dùng trong hệ thống (mã code/số phiếu của chính đối tượng đó).

Vài prefix đang dùng để tham khảo (**chỉ là ví dụ, không phải danh sách đóng**):
`[TASK]` Task · `[GP]` Giải pháp · `[MET]` Meeting · `[HMGP]` Hạng mục giải pháp ·
`[BBH]` Biên bản họp · `[YCG]` Yêu cầu làm giải pháp · `[ISSUE]` Vấn đề ·
`[BGCV]` Phiếu bàn giao công việc · `[PTT]` Phiếu thu thập thông tin.

Đối tượng khác → lấy prefix theo mã đối tượng tương ứng; nếu không có sẵn thì đề xuất
prefix ngắn (3–5 ký tự) và **hỏi user xác nhận** — điều bắt buộc vẫn là đúng cấu trúc ở mục 1.

### 3a. ⚠️ Prefix MỚI → BẮT BUỘC khai nhãn ở `NotificationMeta::OBJECT_LABELS`

Tiêu đề push trên màn khoá điện thoại là CÂU tự nhiên ghép từ Loại đối tượng + Nhóm hành động (vd "Đơn xin nghỉ bị từ chối", câu khai ở `NotificationMeta::PUSH_TITLE_PHRASES`, chốt 30/10/2026 — kiểu cũ `Nhóm hành động · Loại` đọc máy móc), trong đó "Loại đối tượng" tra từ
prefix trong `hrm-api/app/Support/NotificationMeta.php` → `OBJECT_LABELS`. Prefix CHƯA khai thì:
- phiếu thuộc 5 phân hệ app (Chấm công, Công việc, Meeting, Đào tạo, Cơm) → tiêu đề ghép tên phân hệ;
- phiếu nhóm Khác (Kho, Vận chuyển, Tài chính, CSKH…) → tiêu đề CHỈ còn `Từ chối` / `Chờ duyệt`, người nhận
  không biết là phiếu gì.

Đã dính thật 30/10/2026: 6 màn port ERP (HĐ vận chuyển, Tổng hợp giá VC, Chuyến xe khác, Báo thừa thiếu nhập
kho, Xuất/Nhập điều chỉnh kiểm kê) dùng prefix mới mà không khai → push ra `Từ chối · Thông báo`.

Vì vậy, mỗi khi màn mới / màn port có bắn thông báo với prefix chưa từng dùng:
1. Thêm 1 dòng `'PREFIX' => 'Tên loại đối tượng'` vào `OBJECT_LABELS` đúng nhóm (khoá viết HOA, không ngoặc
   vuông; nhãn ngắn ≤ 25 ký tự vì tiêu đề iOS chỉ 1 dòng). File dùng chung nhưng thêm dòng nhãn KHÔNG cần hỏi.
2. Loại có dữ liệu nhạy cảm (lương, tiền, sức khoẻ, hồ sơ cá nhân) → thêm prefix vào `SENSITIVE_PREFIXES`.
3. Tự kiểm — lệnh phải in RỖNG:
   `python3 .claude/skills/notification-convention/scripts/check_prefix_labels.py` (chạy từ `HRM/`)

---

## 4. Quy chuẩn hiển thị (UI/UX)

- **Tổng nội dung ≤ 180 ký tự** (nới từ 120 ngày 22/10/2026 — khách cần đủ ai · khi nào · lý do; màn khoá iOS hiện ~4 dòng). Cắt phần `{Ghi chú}` trước, rồi mới cắt `{Tên đối tượng}` về 50 ký tự. Ghi chú bị cắt thì bản đầy đủ lưu `data.note_full`, app / web bấm **Xem thêm** hiện đủ → chữ tự do người dùng nhập (lý do, nội dung) luôn đặt **CUỐI** ghi chú.
- **Ghi chú phải đủ thông tin cơ bản** để đọc là nắm được việc: ai (khi người nhận không phải chính họ) · thời gian / khoảng ngày / số tiền · người xử lý · lý do. Vd `[DXN] Chờ duyệt: Nguyễn Văn An - Phép năm. 23/10 – 24/10/2026 (2 ngày). Lý do: Về quê có việc gia đình`.
- **Tên đối tượng là TÊN RIÊNG, không lặp loại** (loại đã ở `[PREFIX]`, chốt 22/10/2026): có mã → mã (`PNK-2026-00012`); có tiêu đề → tiêu đề; đơn không mã gửi người duyệt → `Người - Loại`, gửi chính chủ → `Loại + thời gian`. Cấm `Đơn xin nghỉ - …`, `Phiếu nhập kho PNK-…`. Bảng hướng dẫn theo loại: `docs/superpowers/specs/2026-10-22-notification-content-design.md`.
- **Push ra màn hình chờ KHÔNG lộ thông tin nhạy cảm** (chốt 22/10/2026, theo Workday / app ngân hàng): tiêu đề push = câu tự nhiên "Loại đối tượng + hành động" (`OBJECT_LABELS` + `PUSH_TITLE_PHRASES`; thêm nhóm hành động mới thì khai luôn câu tương ứng, chưa khai thì tiêu đề rơi về kiểu cũ `Nhóm hành động · Loại`; thông báo cần trình bày riêng truyền `push_title` / `push_body`); loại nhạy cảm (`NotificationMeta::SENSITIVE_PREFIXES`: đơn nghỉ, đi muộn về sớm, lương, bảo hiểm, HĐLĐ, quyết định, hồ sơ tự khai, thu chi / công nợ) thì thân push chỉ còn người hoặc mã + `Mở ứng dụng để xem chi tiết` — lý do, loại nghỉ, số tiền chỉ hiện trong app sau khi mở khoá. Thêm loại nhạy cảm mới → khai prefix vào `SENSITIVE_PREFIXES`; thêm prefix mới → khai nhãn vào `OBJECT_LABELS`. Prefix chưa khai nhãn thì tiêu đề lấy tên phân hệ; phiếu nhóm Khác (ngoài 5 phân hệ app) KHÔNG có nhãn dự phòng → tiêu đề chỉ còn `Nhóm hành động` (vd `Từ chối`), không ghép chữ "Thông báo" (chốt 30/10/2026).
- **Tên đối tượng in đậm** trên Web và App → BE bọc `<b>…</b>` quanh tên đối tượng, FE render bằng `v-html` (đã sanitize).
- **Deep-link bắt buộc**: mỗi thông báo phải có `url` dẫn thẳng màn xử lý và **luôn kèm ID đối tượng** (`/assign/tasks?open_task=123`). Không bắn thông báo trỏ về màn danh sách trống.
- Thông báo là **kết quả của event**, gửi ngay khi event xảy ra; loại nhắc hạn gửi theo cấu hình thời điểm.

---

## 5. Cách implement trong project này

**BE** — helper dùng chung, KHÔNG tự viết cơ chế mới:

```php
// Modules/Timesheet/Services/EmployeeInfoService.php:466
EmployeeInfoService::sendNotification($employeeInfoId, [
    'url'   => '/assign/tasks?open_task=' . $task->id,   // deep-link + ID
    'title' => $content,                                  // chuỗi theo mục 1
    'type'  => 'task_approve',
    'id'    => $task->id,
]);
// nhiều người nhận: EmployeeInfoService::sendToAllNotification($ids, $data)
```

Nên ghép chuỗi qua 1 chỗ duy nhất (helper `buildNotificationContent(prefix, action, name, note)`)
để tự cắt 50/120 ký tự, thay vì nối chuỗi rải rác trong service.

**FE** — danh sách chuông: `pages/timesheet/notifications/index.vue`,
dropdown `components/assign-components/AssignMenu.vue`, `components/BasicSubsystem.vue`.
Click → `markAsRead` rồi `$router.push(data.url)`.

⚠️ Hiện trạng cần chú ý khi đụng vào phần thông báo:
- FE đang render title bằng interpolation `{{ }}` → thẻ `<b>` BE gửi bị hiện thành text thô. Muốn in đậm phải đổi sang `v-html`.
- Dropdown `AssignMenu.vue` / `BasicSubsystem.vue` bind `@click="markAsRead(noti)"` nhưng chưa định nghĩa method → click không mark-read, không deep-link.
- Notification cũ trong module Assign (task comment, issue, solution) đang viết câu tự do, chưa có prefix → khi sửa vùng nào thì chuẩn hoá vùng đó, không sửa đại trà nếu chưa được yêu cầu.

---

## 6. Không nhầm với thông báo kiểm tra dữ liệu (Validation)

| Tình huống | Cách hiển thị |
|---|---|
| Trống dữ liệu / sai định dạng / vượt độ dài / trùng dữ liệu | Lỗi **inline dưới trường** (không popup, không dùng mã QLDA) |
| Ràng buộc nhiều trường | Toast/alert chung + inline nếu xác định được trường |
| Không đủ quyền | `QLDA_012` — "Bạn không có quyền thực hiện chức năng này." |
| Không thể xóa do đang được sử dụng | `QLDA_015` — "Không thể xóa do dữ liệu đang được sử dụng." |
| Lỗi hệ thống | `QLDA_010` — "Đã xảy ra lỗi hệ thống. Vui lòng thử lại." |

Câu hỏi phân loại duy nhất: **lỗi này có chỉ đích danh 1 trường không?**
Có → inline tại trường. Không → thông báo chung theo mã QLDA.
Còn lại: tuyệt đối không dùng popup để báo lỗi validate; scroll + focus trường lỗi đầu tiên;
lỗi tự ẩn khi sửa hợp lệ; còn lỗi thì không gọi API lưu.

---

## Checklist trước khi kết thúc task có thông báo

- [ ] Đúng cấu trúc mục 1: `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}`
- [ ] Prefix là mã viết tắt của loại đối tượng, viết hoa trong ngoặc vuông
- [ ] Prefix mới đã khai nhãn ở `NotificationMeta::OBJECT_LABELS` (mục 3a) — `check_prefix_labels.py` in rỗng
- [ ] Nhóm hành động nằm trong 16 giá trị mục 2
- [ ] Tên đối tượng cắt ≤ 50 ký tự, tổng ≤ 180 ký tự (dựng bằng `NotificationMeta::build()`, tự sinh `note_full`)
- [ ] Ghi chú đủ ai · khi nào · lý do; chữ tự do để cuối
- [ ] Tên đối tượng in đậm (`<b>`)
- [ ] `url` deep-link có kèm ID đối tượng, bấm vào mở đúng màn xử lý
- [ ] Gửi đúng người nhận, đúng thời điểm event
