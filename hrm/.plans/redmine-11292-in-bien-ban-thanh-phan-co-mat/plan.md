# Plan — Redmine #11292: In biên bản meeting, cấu hình chỉ hiện người CÓ MẶT

Nguồn: http://quanly.dnsmedia.vn/issues/11292 — nhánh `fix-bug-11092026` (hrm-api + hrm-client). @khoipv

## FE — Popup cấu hình in (bước 1)
- [x] `components/assign/meeting/MeetingPartsConfigModal.vue`: thêm prop `showOnlyPresentOption` (mặc định `false`) + data `onlyPresent` (mặc định `false`, reset mỗi lần mở)
- [x] Checkbox "Thành phần tham dự có mặt" — CHỈ hiện khi `showOnlyPresentOption` && danh sách `parts` có phần `attendees`
- [x] `handleConfirm` emit thêm tham số 2: `{ onlyPresent }` (giữ nguyên tham số 1 là mảng parts → usage Xuất Excel không vỡ)

## FE — Bản xem trước / bản in (bước 2)
- [x] `components/assign/meeting/MeetingPrintPreview.vue`: thêm prop `onlyPresent`
- [x] `companyMembers` / `customerMembers` lọc `attendance_status === 1` khi `onlyPresent = true`
- [x] `onlyPresent = false`: thêm cột **"Trạng thái tham dự (Attendance)"** vào cả 2 bảng (phía công ty / phía khách hàng), lý do để trong ngoặc — `Vắng có lý do (Đi công tác)`
- [x] `onlyPresent = true`: ẩn cột trạng thái, bảng về đúng 4 cột như cũ
- [x] `hasSectionIII` + `hasCustomerMembers` tính trên danh sách ĐÃ LỌC (lọc xong rỗng thì không in mục III)

## FE — 2 màn gọi luồng in
- [x] `pages/assign/meeting/components/MeetingReport.vue` (tab Biên bản): truyền `showOnlyPresentOption`, hứng `onlyPresent`, truyền xuống preview
- [x] `pages/assign/meeting/index.vue` (nút In biên bản ở danh sách): như trên
- [x] Popup cấu hình **Xuất Excel** giữ nguyên (issue chỉ nói bản in)

## BE — nguồn in thứ 2 (giữ 2 nguồn không lệch)
- [x] `hrm-api/resources/views/exports/meeting_record.blade.php`: thêm cột Trạng thái tham dự + lọc theo `$onlyPresent`
- [x] `MeetingController@print`: nhận query `only_present`, truyền vào view (mặc định `false`)

## Kiểm thử
- [ ] Mặc định (không tick): in đủ mọi thành viên, có cột trạng thái, dòng vắng có ghi chú hiện lý do trong ngoặc
- [ ] Tick: chỉ còn người "Có mặt", không có cột trạng thái
- [ ] Meeting nội bộ (không có khách hàng) — chỉ có mục "1/ Phía công ty"
- [ ] Tick mà không ai "Có mặt" → mục III không in ra
- [ ] Bỏ tích phần "Thành phần tham dự" → checkbox ẩn, đánh số mục I-V vẫn đúng
- [ ] Xuất Excel không đổi

### Checkpoint — 2026-09-11
Vừa hoàn thành: toàn bộ code FE (4 file) + BE (blade + controller) của #11292.
Đã kiểm chứng:
- BE — render thật `exports.meeting_record` với meeting id 11 (dữ liệu thật + 2 trạng thái giả lập trong bộ nhớ, KHÔNG ghi DB):
  tắt cờ ra đủ 3 dòng kèm cột trạng thái (`Vắng có lý do (Đi công tác Đà Nẵng)`), bật cờ còn 1 dòng "Có mặt" và mất cột trạng thái.
- FE — render SSR component `MeetingPrintPreview.vue` 4 kịch bản: mặc định (4 dòng + cột trạng thái, ghi chú của người "Có mặt" KHÔNG bị ghép),
  bật cờ (còn người có mặt, mất cột), bật cờ mà không ai có mặt (không in mục III), bật cờ mà khách vắng hết (mất mục "2/ Phía khách hàng").
- `php -l` controller + biên dịch blade OK; 4 file .vue qua vue-template-compiler + babel parse OK.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm thử thật (chưa chạy Playwright theo quy ước) — chạy đủ 6 test case ở mục Kiểm thử, đặc biệt regression Xuất Excel.
Blocked:

## FE — Chỉnh vị trí checkbox (user yêu cầu 2026-09-11)
- [x] Đưa checkbox "Thành phần tham dự có mặt" vào **trong** khối "Chọn phần cần xuất"
      (`.part-list`), nằm ngay dưới dòng "Thành phần tham dự" như tuỳ chọn con thụt 1 cấp
      — bỏ hộp viền riêng `.only-present-box` ở dưới
- [x] Vòng lặp `v-for` đổi sang `<template>` để chèn tuỳ chọn con đúng sau phần `attendees`
      (mỗi nhánh tự giữ `:key` riêng)
- [x] Bỏ computed `hasAttendeesPart` — render trong vòng lặp nên `attendees` không có trong `parts`
      thì tuỳ chọn con tự không render
- [x] Checkbox con `:disabled` khi dòng "Thành phần tham dự" chưa được tích (tuỳ chọn vô nghĩa khi không in phần đó)
- [x] Biên dịch lại `MeetingPartsConfigModal.vue` — vue-template-compiler + babel parse OK

### Checkpoint — 2026-09-11 (lần 2)
Vừa hoàn thành: chuyển checkbox "Thành phần tham dự có mặt" vào chung khối "Chọn phần cần xuất".
Đang làm dở: không có.
Bước tiếp theo: user Ctrl+Shift+R rồi mở popup **In biên bản** (không phải Xuất Excel) để xem vị trí mới,
sau đó chạy tiếp 6 test case ở mục Kiểm thử.
Blocked:
