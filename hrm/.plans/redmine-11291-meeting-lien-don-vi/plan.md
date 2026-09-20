# Plan — Redmine #11291: Meeting liên đơn vị

@khoipv · Nhánh `fix-bug-11092026` (hrm-api) · Tạo 2026-09-11

Phạm vi đã chốt với user: **chỉ bổ sung thông báo chuông cho người MỚI được giao nhiệm vụ**.
3 yêu cầu còn lại của issue đã có sẵn trong code (xem `design.md` mục Hiện trạng) → không đụng.
Không gửi Email / chat. Không thêm cột Công ty/Đơn vị (issue không yêu cầu).

## Phase 1 — BE: thông báo giao nhiệm vụ

- [x] T1. `MeetingService::reportExecutorEmployeeIds(Meeting $meeting): array`
      Gom `executor_id` các dòng `meeting_report_executors` có `executor_type = 1` (nội bộ),
      lọc null + trùng. Người thực hiện phía khách hàng (type = 2) bỏ qua.
- [x] T2. `MeetingService::notifyReportExecutors(Meeting $meeting, array $oldExecutorIds)`
      Diff mới − cũ → chỉ báo người vừa được thêm. Gộp 1 thông báo / 1 người dù nhiều nhiệm vụ.
      Bỏ qua khi meeting ở trạng thái Đang tạo (nháp) hoặc Hủy.
- [x] T3. Thêm tham số TÙY CHỌN `$prefix` cho `buildMeetingNotificationContent()`
      và `$url` cho `notifyMeetingEmployees()` (mặc định giữ nguyên `[MET]` + `/show`)
      → 5 chỗ gọi cũ không đổi hành vi.
- [x] T4. `MeetingController@store`: tập executor cũ = rỗng, gọi `notifyReportExecutors()` sau commit.
- [x] T5. `MeetingController@update`: chụp `$oldExecutorIds` TRƯỚC mọi `sync*()`
      (vì `syncReports()` xoá sạch rồi ghi lại), gọi `notifyReportExecutors()` sau `DB::commit()`,
      ĐẶT NGOÀI khối `if/elseif` theo status nhưng TRONG `if ($shouldNotify)`.
- [x] T6. Kiểm chứng: `php -l` 2 file + chạy thử service qua tinker trên meeting thật.

## Ghi chú kỹ thuật

- Nội dung: `[BBH] Tạo mới: <b>{tên cuộc họp ≤50}</b>. Bạn được giao N nhiệm vụ.`
  (nhóm hành động `Tạo mới` thuộc 14 giá trị của `.claude/skills/notification-convention`).
- Deep-link: `/assign/meeting/{id}/show?active_tab=reports` — `MeetingForm.vue:1206` đọc `?active_tab`.
- Không lọc bỏ chính người thao tác (đồng nhất với `notifyMeetingChanges()` hiện tại).
- `send_notification = 0` vẫn phải chặn được thông báo này.

### Checkpoint — 2026-09-11
Vừa hoàn thành: T1–T6. BE xong toàn bộ phạm vi đã chốt, `php -l` sạch 2 file,
chạy 6 ca kiểm thử qua tinker với `Notification::fake()` + `Queue::fake()` — đúng hết.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm chứng luồng thật (gán người thực hiện ở tab Biên bản
→ Lưu → xem chuông của người được gán). Chưa commit.
Blocked:

## Phase 2 — Kiểm thử trình duyệt (Playwright, 2026-09-11)

- [x] T7. Dựng cuộc họp thật `#29 [TPE.MET.NB.26.0027]` qua UI (Họp nội bộ, Lên lịch),
      người chủ trì + thành phần = DNS Admin (employee 13 / employee_info 6).
- [x] T8. Tạo meeting chưa có biên bản → chỉ 1 thông báo `[Meeting]` cũ, **không** có `[BBH]`. ĐÚNG.
- [x] T9. Tab Biên bản → Thêm dòng → Người thực hiện = DNS Admin → Lưu
      → sinh đúng `[BBH] Tạo mới: <b>…</b>. Bạn được giao 1 nhiệm vụ.` ĐÚNG.
- [x] T10. Lưu lại lần 2 không đổi gì → tổng thông báo vẫn = 2, **không spam**. ĐÚNG.
- [x] T11. Chuông FE hiển thị đúng, tên cuộc họp **in đậm** (dropdown dùng v-html, không lòi thẻ `<b>`).
- [x] T12. Bấm vào thông báo → nhảy `/assign/meeting/29/show?active_tab=reports`,
      tab **Biên bản** active sẵn. Deep-link ĐÚNG.
- [x] T13. Popup "Chọn người thực hiện": 552 nhân sự, dropdown Công ty đủ **5 pháp nhân**
      (Tân Phát, CN Hải Phòng, CN Vinh, Tân Phát Sài Gòn, **Tập đoàn ETEK**)
      → xác nhận yêu cầu 1 & 2 của issue đã đạt sẵn, bằng UI thật.

### Việc phát sinh ngoài phạm vi (đã xử lý)
- DB local thiếu bảng `meeting_history` → mọi thao tác lưu meeting trả **500**.
  Đã chạy đúng 1 migration `2026_08_17_000001_create_meeting_history_table` (`--path`), KHÔNG chạy cả
  loạt pending. Không liên quan code #11291.

### Rác kiểm thử còn lại
- Meeting **#29** `[TEST 11291] Họp kiểm thử thông báo giao nhiệm vụ` + 2 thông báo của info 6.
  Chỉ nằm trên DB local `hrm_production_18072026`. Xoá khi nào thấy cần.

### Checkpoint — 2026-09-11 (sau kiểm thử)
Vừa hoàn thành: T1–T13. Đã kiểm thử end-to-end qua trình duyệt, 6/6 ca đúng.
Đang làm dở: không có.
Bước tiếp theo: chờ lệnh commit + cập nhật Redmine #11291.
Blocked:
