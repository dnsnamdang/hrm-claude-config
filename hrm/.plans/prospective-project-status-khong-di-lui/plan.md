# Fix: bấm Lưu ở màn Sửa dự án kéo trạng thái dự án đi lùi

Triệu chứng: đã gửi/tiếp nhận yêu cầu làm giải pháp mà dự án vẫn ở "Thu thập thông tin dự án".
Nguyên nhân: FE gửi cứng `status = 2` mỗi lần Lưu, BE `fill($request->all())` nuốt luôn (`status` nằm trong `$fillable`), không có guard chặn đi lùi.

## Phase 1

### BE
- [x] `ProspectiveProjectService::update()`: sau `fill()`, giữ nguyên `$originalStatus` khi dự án đã qua bước "Đang tạo"; còn "Đang tạo" thì chỉ nhận status 1 hoặc 2 (chặn payload rác `status='save'` → 0)
- [x] Sinh mã dự án soi `$prospectiveProject->status` (đã qua guard) thay vì `$request->status` thô

### FE
- [x] `pages/assign/prospective-projects/_id/edit.vue`: thêm `statusToSubmit()` — dự án đã qua "Đang tạo" thì gửi lại đúng trạng thái hiện tại (`status` vẫn `required` ở FormRequest nên bắt buộc gửi); `@submitAndDraft="submitForm(1)"`; `@submit.prevent` không còn gửi `'save'`
- [x] `pages/assign/prospective-projects/_id/index.vue`: submit form gửi `formSubmit.status` thay vì `'save'`

### Dữ liệu
- [x] Backup `prospective_projects` (10 bản ghi liên quan) → scratchpad `pp_backup_before_status_backfill.sql`
- [x] Backfill: 22, 68, 69, 110 → 4 (Đang làm giải pháp, solution đang triển khai); 55 → 3 (Chờ tiếp nhận làm giải pháp)
- [x] 6, 23, 109 giữ nguyên — solution còn nháp nên "Thu thập thông tin dự án" là đúng
- [ ] 37 (YC đã tiếp nhận, chưa có giải pháp): **user chốt để nguyên** — `syncStatusBySolution` chưa map trạng thái YC "Đã tiếp nhận"/"Đang thực hiện"
- [ ] 111 (solution "Chờ làm giá"): chưa map — thuộc phase báo giá, chưa làm

### Kiểm
- [x] Test thật qua UI: mở `/assign/prospective-projects/55/edit`, bấm Lưu → `updated_at` đổi, `status` vẫn = 3 (không tụt về 2)
- [x] Test guard ở tầng service (tinker, bọc `DB::transaction` + rollback) — 5/5 đúng: nháp+Lưu nháp giữ 1 · nháp+Lưu tiến sang 2 · nháp+payload `'save'` giữ 1 · dự án status 3 gửi 2 giữ 3 · dự án status 7 gửi 2 giữ 7
- [x] Luồng MEETING (không đi qua `ProspectiveProjectService::update`, phải test riêng): `MeetingService::syncProjects` nhánh cập nhật dự án đã gắn — dự án 175 giữ nguyên status 7 kể cả khi payload gửi kèm `status = 2` (map chỉ set `status` khi `$isNew`)
- [x] Luồng meeting nhánh TẠO NHANH dự án: dự án mới ra status 2 (Thu thập thông tin dự án) — hành vi sẵn có, điều kiện `$hasAnswers` đã bị comment nên luôn nâng 1 → 2; bản vá không đổi hành vi này
- [ ] CHƯA test qua UI: màn Thêm mới dự án, màn Sửa meeting thật (mới test ở tầng service)

### Checkpoint — 2026-08-20
Vừa hoàn thành: vá BE + FE, backfill 5 dự án, test thật trên trình duyệt.
Đang làm dở: không.
Bước tiếp theo: user review + push. Còn 2 khoảng trống nghiệp vụ chưa map (dự án 37, 111).
Blocked: không.
