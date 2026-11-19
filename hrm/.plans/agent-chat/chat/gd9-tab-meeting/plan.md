# GĐ9 — Tab Meeting trong nhóm · PLAN

Design: `design.md` · Mockup: `mockup.html` · User cho phép code 14/11 ("làm") — phạm vi: hrm-api + hrm-client nhánh
`gop_db-chat-tab-meeting` (tách từ `gop_db-chat-giao-dien`, mang theo GĐ8 chưa commit), 1 migration
`2026_11_18_000001_add_workspace_id_to_meetings_table` chạy vào `db_gop_6_11` bằng `--path`, PHPUnit + e2e mới.

## BE (hrm-api)
- [x] B1 Migration `meetings.workspace_id` nullable + index (`workspace_id`, `start_date`); Meeting fillable/cast.
- [x] B2 Tạo meeting có `workspace_id`: request nhận `nullable|integer`; controller kiểm nhóm tồn tại, là Nhóm trao đổi,
      đang mở, bật tab Meeting, người tạo là Quản lý/Thành viên (không phải Xem) ⇒ sai 422 `workspace_id`. Update KHÔNG đổi nhóm.
- [x] B3 `Meeting::canView()` thêm nhánh thành viên nhóm (không áp cho Đang tạo).
- [x] B4 `GET workspaces/{id}/meetings` (`CheckWorkspaceAccess:member`): `bucket` upcoming|done|cancelled|all, `q`, `page`,
      `per_page` ≤ 50 ⇒ items + counts từng nhóm + meta. Nháp chỉ người tạo/chủ trì.
- [x] B5 Chi tiết nhóm trả `upcoming_meeting_count` (số trên tab).
- [x] B6 Tin hệ thống qua `WorkspaceActivity` (listener SyncWorkspaceChat): meeting_scheduled / meeting_confirmed /
      meeting_rescheduled / meeting_cancelled, meta `meeting_id`; bật/tắt tab Meeting cũng ghi tin.
- [x] B7 PHPUnit `WorkspaceMeetingTest`: tạo có/không quyền (ngoài nhóm, Xem, nhóm tắt tab, nhóm đóng) · danh sách 3 nhóm
      + nháp người khác ẩn · người ngoài nhóm 403 · canView thành viên · tin hệ thống 4 loại · update không đổi nhóm.

## FE (hrm-client)
- [x] F1 `WorkspaceMeetingList.vue` (components/chat/workspace) theo mockup ①.
- [x] F2 Trang nhóm: panel `meetings`, tab Meeting (#7C3AED, số = upcoming_meeting_count), fallback chat khi tắt.
- [x] F3 SettingsPanel: công tắc Meeting (hỏi xác nhận khi tắt mà còn cuộc sắp họp).
- [x] F4 Form meeting: `?workspace_id=&from=workspace` ⇒ chip nhóm khoá + nút "Mời tất cả thành viên nhóm (N)";
      lưu xong / Quay lại ⇒ về tab Meeting; màn chi tiết `from=workspace` Quay lại về tab.
- [x] F5 Tin hệ thống có `meta.meeting_id` bấm được ⇒ mở chi tiết meeting.
- [x] F6 Playwright đo DOM + e2e `workspace-meetings.spec.ts` (gồm ca không quyền) + chạy lại bộ chat/workspace liên quan.

## Kết quả 14/11
- Migration `2026_11_18_000001_add_workspace_id_to_meetings_table` ĐÃ chạy vào `db_gop_6_11` (`--path`, đúng 1 bản).
- PHPUnit `WorkspaceMeetingTest` 8/8 (58 assertions). Thư mục Workspace 147: còn đúng 2 ca fail CÓ SẴN trên gop_db
  (`WorkspaceTaskTest::test_workspace_and_solution_are_exclusive`, `test_patch_field_enforces_workspace_rules`).
  Bộ meeting cũ (`tests/Feature/MeetingTarget`, `ReportMeetingView`, `Rbac/MeetingCodesTest`, `ServiceDemand/MeetingViewPermissionTest`)
  lỗi ở fixture (khoá ngoại `roles.company_id`, trùng `permission_aliases`, thiếu cột) — không dính GĐ9; `MeetingHookTest` đạt.
- Playwright MCP 1440px: bật tab ở Cấu hình ⇒ tab "Meeting 0"; tạo thật từ nhóm (dải nhóm, Mời tất cả 1 ⇒ Nhân sự 1→2, payload có
  workspace_id) ⇒ popup đặt phòng (luồng cũ) ⇒ về `?panel=meetings`, tab "Meeting 1"; dòng không tràn (body scrollWidth = clientWidth);
  tin "DNS Admin đã lên lịch họp: … — 09:00 17/11" nền #f5f3ff bấm ⇒ `/assign/meeting/{id}/show?from=workspace&workspace_id=` ⇒ Quay lại về tab.
  Console chỉ có cảnh báo `hasCustomer` CÓ SẴN của form meeting.
- E2E mới `e2e/tests/assign/workspace-meetings.spec.ts` 5/5 (M4 = ca không quyền).

## Rulings (Claude tự quyết khi code — user xem lại)
- Danh sách hiện 1 nhóm theo chip đang chọn (mặc định Sắp họp) thay vì 3 khối cùng lúc như mockup ① — 1 request/lần, số từng
  nhóm vẫn hiện trên chip. Sai thì: thêm chế độ "Tất cả" chia 3 khối (3 request).
- Dải "Nhóm: …" + nút "Mời tất cả thành viên nhóm (N)" đặt NGAY TRÊN dải tab của form (thấy ở mọi tab) thay vì trong khối Thành
  phần (tab Nhân sự tham gia). Sai thì: chuyển nút vào MeetingParticipants.
- Tin báo trong chat là nhật ký nhóm ⇒ KHÔNG theo cờ `send_notification` (lưu im lặng vẫn ghi tin). Nhóm đã đóng ⇒ không ghi tin.
- Vai trò Xem của nhóm cũng mở được chi tiết meeting của nhóm (Q2 "mọi thành viên"), chỉ không có nút Tạo + BE 422 khi gắn nhóm.
- Màn Sửa meeting không hiện dải nhóm, lưu xong về danh sách meeting như cũ; màn Chi tiết đi từ nhóm thì Quay lại về tab.
- Ngoài luồng (note, chưa sửa): cảnh báo Vue `hasCustomer` (prop trùng computed / Number thay Boolean) ở GeneralInfo, MeetingParticipants,
  MeetingReport, PopupStaff — có từ trước.

## Chỉnh theo góp ý 14/11
- [x] 3 chip trạng thái có màu (9 mã chuẩn): Sắp họp #2563EB · Đã họp #16A34A · Đã huỷ #DC2626 (đỏ, đồng bộ nút Huỷ — user 14/11) — chưa chọn: icon + số nhuộm màu;
      chọn: nền đặc màu, chữ trắng. "Tất cả" giữ navy. Đo Playwright: màu đúng cả 2 trạng thái, thanh công cụ không tràn. Chưa chạy e2e (task nhỏ).
