---
name: app-form
description: Quy chuẩn màn FORM tạo / sửa của TPE_APP (bám skill web form-validate + unsaved-changes) — bố cục nhãn + ô, ô gõ / ô chọn / nút gạt / ngày giờ, danh sách bước gõ nhanh, chọn nhân sự / khách hàng toàn trang, bàn phím (chạm ra ngoài đóng, Enter, ô nhiều dòng), chỉ kiểm định dạng – lỗi bắt buộc / nghiệp vụ do BE trả và tô đỏ đúng ô, cảnh báo thoát khi chưa lưu, nút Hủy / Lưu, lưu xong quay về. Dùng khi làm / sửa form, popup nhập liệu, bottom sheet có ô nhập, khi bàn phím che nút, khi lỗi không hiện đúng ô.
---

# Màn form — TPE_APP

Ví dụ tham khảo (không phải chuẩn — chuẩn là quy tắc dưới): **Tạo / Sửa nhắc việc cá nhân** (`ui/my_todo/personal_todo_form_page.dart`),
**Thông tin chung Meeting** (`ui/meeting/meeting_general/` — form dài, khối ①②③). Widget: `app-components` mục 4.

## 1. Bố cục

```
PrimaryAppBar ("Tạo …" / "Sửa …")
ListView  (padding 16, keyboardDismissBehavior: onDrag, nền trắng)
  Nhãn *  ─ ô                     ← nhãn 12 đậm vừa ở TRÊN ô, * đỏ khi bắt buộc
  Nhãn    ─ ô nhiều dòng (minLines 3)
  Nhãn    ─ khối danh sách bước (gõ nhanh, Enter / + để thêm)
  Nhãn *  ─ ô chọn ▾               ← bấm mở bottom sheet (ít mục) / trang chọn (nhiều mục)
  Ngày ─ Giờ  (2 cột)
BottomActionBar [ Hủy ][ Lưu ]     ← nút trắng trái, nút chính phải; icon tự có
```

- Ô: `MeetingTextField` / `MeetingSelectRow` (cao 44, bo 8, viền `AppPalette.border`, **nền trắng**). Khối tự dựng
  (danh sách bước…) cũng nền trắng, cao dòng 48, chữ căn giữa dọc (từng lệch vì đệm trên 2 – dưới 12).
- Nút gạt 2–3 lựa chọn: `MeetingSegmented`. Ngày / giờ: ô chỉ đọc mở date/time picker, hiện `dd/mm/yyyy`, `hh:mm`.
- Form dài (> 8 trường): chia khối `MeetingSection` ①②③ như Meeting, khối có lỗi tự mở.

## 2. Bàn phím (user báo 29/10/2026: "nhập xong không tắt được bàn phím để bấm Lưu")

- **Chạm ra ngoài ô nhập là đóng bàn phím — đã có SẴN toàn app** (`ui/app/my_app.dart` bọc `GestureDetector`
  ngoài Navigator; ô bị khoá `CommonTextField` cũng đóng). KHÔNG dựng lại ở từng màn, KHÔNG gỡ.
- Thêm ở form: `ListView(keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag)` (vuốt là đóng) và
  ô 1 dòng `textInputAction: TextInputAction.next` để Enter sang ô sau. `TextField` tự dựng thêm
  `onTapOutside: (_) => FocusManager.instance.primaryFocus?.unfocus()` như form Meeting.
- Ô nhiều dòng: Enter = xuống dòng (đúng) → bắt buộc phải có lối đóng ở trên.
- Danh sách gõ nhanh: Enter **và** nút ➕ đều thêm; thêm xong giữ focus (`FocusNode.requestFocus()`) để gõ tiếp.
- Bottom sheet có ô nhập: sheet nằm trên bàn phím (`viewInsets`), nút Lưu của sheet bấm được khi bàn phím mở.
- **Test với bàn phím ảo** (simulator ngắt bàn phím Mac ⇧⌘K) — xem `app-simulator-test`.

## 3. Validate + lỗi

- **App chỉ kiểm ĐỊNH DẠNG** (email, số, độ dài). Bắt buộc / nghiệp vụ để BE trả 422 theo trường — không chặn
  trước khi gọi API (memory "App chỉ hiện validate BE").
- Bắt lỗi: `catch (e) { final err = MeetingSaveError.from(e); setState(() => _errors = err.fields); }` →
  ô có lỗi viền đỏ + câu lỗi đỏ dưới ô **nguyên văn BE** ("Bắt buộc phải nhập"); lỗi chung (không gắn trường) →
  `err.summary` lên snackbar. Lỗi mảng (`sub_items.0.title`) → hiện dưới khối tương ứng.
- Sửa ô nào thì xoá lỗi ô đó ngay (`_edited('title')` trong `onChanged`), không chờ bấm Lưu lại.
- KHÔNG tự sửa giá trị user nhập (cắt, làm tròn, kéo về min/max, tự xoá dòng trống).
- Chữ đỏ CHỈ cho lỗi + dấu `*` + mục nguy hiểm; ghi chú / mô tả xám (`AppPalette.textMuted`).

## 4. Chọn dữ liệu

| Số mục | Cách chọn |
|---|---|
| ≤ ~15, cố định (danh sách cá nhân, loại nghỉ) | `showModalBottomSheet` (`useRootNavigator: true`), mục đang chọn có ✓, bấm là chọn + đóng |
| Nhiều / tìm máy chủ (nhân sự, khách hàng, dự án) | trang chọn toàn màn: `pickEmployee()`, `CustomerPickerPage`, `MeetingEmployeePickerPage` |

- KHÔNG hộp thoại nhỏ có ô tìm + danh sách nhãn xếp dọc (kiểu `ChonNvPage` cũ — đã thay 29/10/2026).
- Giá trị đang chọn mà danh mục đã khoá vẫn hiện đúng tên (thêm vào danh sách chọn nếu thiếu), không đổi ngầm.
- Danh mục cache (loại meeting…) tải lại khi mở form để thấy loại mới thêm trên web.

## 5. Chưa lưu + lưu

- Bọc màn: `UnsavedChangesGuard(isDirty: _dirty, screenName: 'Nhắc việc cá nhân', onSave: _save, child: …)` —
  thoát / vuốt lùi khi đã sửa → hỏi 3 lựa chọn (Lưu và quay lại · Quay lại, không lưu · Ở lại màn này).
  `_dirty` chỉ bật khi user thật sự sửa (`_markDirty()` trong onChanged / sau khi chọn), không bật lúc nạp dữ liệu.
- Nút đáy: tạo mới / sửa = `[Hủy][Lưu]`; phiếu có luồng = `[Lưu nháp][Lưu và gửi duyệt]`. `onPressed` trả Future
  → nút tự quay + chặn bấm lặp, KHÔNG đổi chữ thành "Đang lưu…".
- Lưu xong: `navigator.pop(result: true)` về màn trước + báo màn danh sách tải lại (`myTodoChanged.value++` /
  `then(reload)`) + toast `Thêm mới thành công` / `Cập nhật thành công` (`app-ui-convention` 6a). KHÔNG ở lại form.
- Form sửa nhận dữ liệu điền sẵn (`item`), tạo mới nhận giá trị mặc định (vd `initialDate` khi mở từ lịch).

## Checklist (bấm thử trên simulator, bàn phím ảo)

- [ ] Gõ ô nhiều dòng → chạm ra ngoài → bàn phím đóng, bấm được Lưu; vuốt form cũng đóng
- [ ] Enter ô 1 dòng sang ô sau; danh sách bước: Enter và ➕ đều thêm, bàn phím giữ
- [ ] Để trống ô bắt buộc → Lưu → BE trả lỗi đỏ đúng ô; sửa ô → lỗi mất
- [ ] Sửa rồi bấm ‹ → hỏi chưa lưu; không sửa → thoát thẳng
- [ ] Lưu xong về màn trước, danh sách cập nhật; dữ liệu đúng trong DB
