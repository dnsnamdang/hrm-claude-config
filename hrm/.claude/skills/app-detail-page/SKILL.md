---
name: app-detail-page
description: Quy chuẩn màn CHI TIẾT / HUB của TPE_APP — đầu màn (chip loại · mã, badge trạng thái, tên, dòng meta có icon), dòng nhãn – giá trị, khuôn Hub nhiều khối (Meeting), danh sách con tick tại chỗ, dải thông báo, hành động: nút đáy theo trạng thái + menu ⋮ cho hành động phụ / nguy hiểm, khớp hành động với màn danh sách, tải lại sau khi màn con lưu. Dùng khi làm / sửa màn chi tiết, màn xem phiếu / việc, màn hub nhiều khối, khi chi tiết và danh sách lệch nút.
---

# Màn chi tiết / Hub — TPE_APP

Ví dụ tham khảo (không phải chuẩn — chuẩn là quy tắc dưới): **Chi tiết nhắc việc cá nhân** (`ui/my_todo/personal_todo_detail_page.dart` — chi tiết đơn giản),
**Hub Meeting** (`ui/meeting/meeting_hub/meeting_hub_page.dart` — nhiều khối, nút theo trạng thái). Thiết kế
mẫu cho phiếu / nhiệm vụ / vấn đề: `mytodo.pen` C1–C6.

## 1. Đầu màn (khối trắng trên cùng)

```
[chip loại · mã]                      [badge trạng thái]   ← chip màu loại; badge chữ + màu BE trả
Tên bản ghi (17 đậm, tối đa 2–3 dòng)
📅 12/09 → 18/09/2026                                        ← dòng meta: icon 14 xám + chữ 13
👤 Trưởng nhóm: …  ·  ⚠ Trễ 2 ngày (đỏ, chỉ khi quá hạn)
```

- Tiêu đề header (`PrimaryAppBar`) = "Chi tiết <đối tượng>" (Chi tiết nhiệm vụ, Chi tiết phiếu giao công tác);
  mã nằm ở chip đầu màn, không nhét vào tiêu đề header.
- Thời gian nhiều ngày: `bắt đầu → hạn`; đang diễn ra ghi "Đang diễn ra, còn n ngày".

## 2. Thân màn

- Chia khối trắng cách nhau 8–10px nền `pageBg`; mỗi khối có tiêu đề nhỏ CHỮ HOA xám (THÔNG TIN, MÔ TẢ,
  NHÂN SỰ THAM GIA, BƯỚC CON · 2/4, TỆP ĐÍNH KÈM · 2).
- Dòng nhãn – giá trị: `MeetingViewRow`, 2 cột khi giá trị ngắn (Khách hàng | Thời gian), 1 cột khi dài.
  Trường trống: ẩn dòng (chi tiết) — không in "—" hàng loạt.
- Người: `MeetingPersonRow` (danh sách) hoặc chip tên (nhân sự tham gia); tệp: dòng tên · dung lượng ·
  `MeetingFileActions` (xem · tải · chia sẻ).
- Danh sách con thao tác tại chỗ (bước, checklist): tick ngay trên dòng; tick xong việc cha → hỏi xác nhận
  (nêu "n bước chưa xong cũng sẽ được tick"); dòng cuối "+ Thêm …" mở bottom sheet nhập (`app-form` mục 2).
- **Hub nhiều khối** (Meeting): mỗi khối 1 `MeetingHubRow` (icon · tên · gợi ý · giá trị Đủ / Trống / số · ›),
  bấm mở màn con; có thanh "Mức độ hoàn thiện"; khối lỗi khi lưu tô đỏ (`error: true`). Dùng khi bản ghi có
  ≥ 5 nhóm dữ liệu sửa riêng; còn lại dùng chi tiết thường.
- Thông báo trạng thái bản ghi (đã hủy, chỉ xem, quá hạn biên bản): `MeetingBanner` dưới header. KHÔNG hiện dải
  "Chế độ chỉ xem" khi chỉ thiếu quyền (ẩn nút là đủ).

## 3. Hành động

- **Nút đáy (`BottomActionBar`) theo trạng thái**, ví dụ Meeting: Nháp `[Lưu nháp][Lên lịch][Chốt lịch]` · Lên
  lịch `[Lưu][Chốt lịch]` · Chốt lịch `[Lưu][Hoàn thành]` · đã đóng `[Quay lại]`. Chi tiết đơn giản:
  `[Đánh dấu hoàn thành]` + `[Sửa][Xóa]`.
- Hành động phụ / nguy hiểm (Sửa, Hủy, Xóa, In, Lịch sử) → nút ⋮ (`AppBarGlassButton`) trên header → bottom
  sheet "Hành động", mục nguy hiểm chữ + icon đỏ.
- **Khớp màn danh sách** (CLAUDE.md HRM): cùng bản ghi thì danh sách hành động + điều kiện hiện/ẩn ở danh sách
  và chi tiết phải như nhau, đọc cùng cờ BE (`can_edit`, `can_delete`, `can_import_result`, `can_approve`…).
- Không dùng được thì ẨN (không disable); chưa đủ điều kiện mà BE có lý do → `BottomActionBar(note: lý do)`.
- Thao tác ghi khó hoàn tác (Xóa, Hủy, Hoàn thành, Lên lịch / Chốt lịch, Duyệt / Từ chối) → `showAppConfirm` nêu
  mã + tên + hệ quả, `acceptText` = chữ nút (`app-ui-convention` mục 2).

## 4. Dữ liệu

- Mở từ danh sách: nhận object để hiện ngay + tải lại chi tiết đầy đủ (không màn trắng chờ API).
- Màn con lưu xong → chi tiết tải lại (`push(...).then(_reload)`) + báo danh sách (`ValueNotifier` chung).
- Bản ghi không còn / không có quyền → `MeetingLoadError` / `AppEmptyWidget(title:)` + nút Quay lại.
- Loại chưa có màn chi tiết trên app → snackbar "…chưa có trên app, vui lòng xem trên web", không mở màn trống.

## Checklist

- [ ] Đầu màn đủ: chip loại · mã, badge BE, tên, meta có icon
- [ ] Nút đáy đúng theo trạng thái; hành động phụ ở ⋮; số nút khớp màn danh sách
- [ ] Thao tác ghi có hỏi xác nhận; lưu ở màn con → chi tiết + danh sách cập nhật
