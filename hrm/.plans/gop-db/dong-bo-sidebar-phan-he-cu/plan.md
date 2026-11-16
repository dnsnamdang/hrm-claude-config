# Plan — Đồng bộ sidebar 4 phân hệ cũ về chuẩn hub — @khoipv

## Phase 1 — FE (hrm-client, nhánh develop ← gop_db)
- [x] T1. `hub.js`: thêm `human`, `timesheet`, `rice`, `payroll` vào `HUB_SUBSYSTEMS`
- [x] T2. `components/menu.js` + `default-menu/rice.js`: thêm `icon` (Remix, đã kiểm có trong `_remixicon.scss`) cho mục cấp 1
- [x] T3. `layouts/subsystem.vue`: bổ sung thu gọn / rê chuột bung / ghim ☰ (localStorage `hub-sidebar-pinned`) — bản sao logic `default-sidebar.vue`; tên sidebar ưu tiên `shortLabel`
- [x] T4. Khai `layout: 'subsystem'` cho 208 page của `pages/{human,timesheet,payroll,rice}` chưa khai layout
      + 4 file chỉ nhắc "layout" trong comment/code khác (`human/company-struct`, `timesheet/setting/subsystems`,
      `payroll/manpower-allocations`, `payroll/salary/manpower_report`). Bỏ 2 file rỗng
      (`human/department/_id/regulations.vue`, `payroll/salary/report/manpower_report.vue`) + file trong `components/`.
- [x] T5. `timesheet/setting/subsystems`: thực ra không khai layout (chỉ comment) → gộp vào T4, sửa comment
- [x] T6. Verify: parse 213 file (vue-template-compiler + babel, mỗi page đúng 1 `layout: 'subsystem'`);
      chạy registry thật (jiti): số màn hub = số mục con menu gốc (22 / 39 / 11 / 18), link lẻ cấp 1 hiện ở rail
      (Cơm 3, Lương 1), mọi nhóm có icon, `resolveSubsystem` đúng 4 phân hệ

- [x] T7. Check (user hỏi "không thấy menu Cấu hình › Quy định chung…"): KHÔNG phải lỗi chuyển hub.
      Gate quyền của hub (`isScreenVisible`) giống hệt topbar cũ (`Topbar.vue::showMenuChild`): cần mã
      `timesheet.thong_so.configure` (permissions id 6192) VÀ tên cũ "Thiết lập thông số". DB local: mã 6192
      chưa gán vai trò nào; Super admin (NV 13, cty 1) chỉ có 7 mã, NV 34 có 0 mã → DB local chưa chuyển đổi RBAC
      đủ. Trước đây vẫn vào được nhờ sidebar con `SettingSlidebar` (KHÔNG kiểm quyền) ở /timesheet/setting/*, nay
      layout hub không còn sidebar con đó. `menu_settings` không tắt mục nào của timesheet. Chờ user chọn hướng.

- [x] T8. Check (user hỏi "title chưa được sửa à", ảnh màn YC kiểm tra SC-BH): đúng, CHƯA làm. Tên màn trên topbar
      cạnh ☰ (`SidebarMenu.vue` đọc `$store.state.pageTitle`) do TỪNG page tự đặt qua `PageTitleMixin` + `pageTitle`
      (690 page mới có). 212 page cũ: chỉ 9 page có (8 danh mục địa lý của human + shift-history). (Đính chính: `Page-header.vue`
      VẪN render tiêu đề + breadcrumb — chỉ 1 khối cũ bị comment; user bắt bỏ cụm này ở T10.) Chờ user chọn hướng (fallback chung / từng page).

## Phase 2 — Tên màn trên topbar + bỏ cụm tiêu đề/breadcrumb trong màn (user chốt 16/11: hướng 2 — từng page)
Chia lô: `title-batches/{human,timesheet-a,timesheet-b,payroll-rice}.tsv` (213 page, cột: file · route · · nhãn menu
khớp đúng · screenTitleOf · heading trong màn). Subagent Opus 5.5 (user chọn).
- [x] T9. Mỗi page: `PageTitleMixin` + computed `pageTitle` (danh sách = nhãn menu; Thêm = "Thêm/Tạo …"; Sửa/Chi tiết/Duyệt
      = "Sửa/Chi tiết/Duyệt …" + `: <mã>` khi bản ghi có mã)
- [x] T10. Bỏ cụm tiêu đề + breadcrumb trong màn (`<PageHeader>` / `page-title-box` tự viết) — KHÔNG sửa `components/Page-header.vue`
      (dùng chung ~300 page phân hệ khác)
- [x] T11. Verify parse toàn bộ + rà kết quả 4 lô — 201 page sửa (`title-batches/*-done.txt`), parse ok 201/bad 0,
      không page nào còn `<PageHeader`. Bỏ qua 12: 9 page chỉ redirect (human/employee*, human/roles*, timesheet/setting/
      employees*, roles*), 3 vỏ bọc `request-update-working/form.vue` (form tự đặt tên theo mode).
- [x] T12. Rà: 10 màn chi tiết Tính lương mất tên bản ghi (heading cũ chỉ hiện tên bảng, bảng không có mã) → nối
      `: <tên>` (payment, salary, salary-summary, other-*, p3 + p3 approve, salary-advance, timesheet_summaries + kỳ)

- [x] T13. Fix bug có sẵn (user yêu cầu 16/11): `pages/rice/report/general/index.vue` + `report-detail/index.vue` khai
      `mixins:` 2 lần trong cùng object → khai sau (`[FormatDate, PageTitleMixin]`) đè khai trước (`[CheckPermission]`).
      Template gọi `permissionScope('rice.bao_cao_com_{tong_hop,chi_tiet}.view')` cho phạm vi bộ lọc công ty/phòng ban →
      hàm không tồn tại, lỗi render. Sửa: gộp 1 khai báo `[CheckPermission, FormatDate, PageTitleMixin]`.
      Verify: parse 2 file ok; quét toàn `pages/ components/ layouts/` không còn file .vue nào khai `mixins:` 2 lần.
      Chưa mở trình duyệt.

- [x] T14. Commit + push (user yêu cầu 16/11): hrm-client `e876d0237` lên `develop` (218 file: 214 page + hub.js, menu.js,
      rice.js, layouts/subsystem.vue). Chỉ stage file của feature này — WIP feature khác (customer-care, warehouse, sale-hub.js,
      menu-sidebar.js, notificationIcon.js) để nguyên. Pull --rebase --autostash trước khi push, không conflict. hrm-api không đổi.

### Checkpoint — 2026-11-16 (wrap up)
Vừa hoàn thành: T1–T14 — code xong + ĐÃ PUSH develop hrm-client `e876d0237`
Đang làm dở: (không)
Bước tiếp theo: (1) user test trình duyệt sau build: bố cục màn rộng cố định (rail 58px), 5 màn Cấu hình chấm công,
  Sơ đồ cơ cấu tổ chức, form Chấm công còn mỗi nút quay lại, 2 báo cáo Cơm (bộ lọc theo quyền);
  (2) user chốt: đuôi "… chờ duyệt" ở màn duyệt danh sách; 9 màn human chép từ màn Công ty (sửa nội dung hay để nguyên);
  (3) nhóm "Cấu hình" Chấm công ẩn với mọi tài khoản local vì mã `timesheet.thong_so.configure` chưa gán vai trò
  (T7) — gán quyền hoặc chạy chuyển đổi RBAC trên DB.
Blocked: (không)

### Checkpoint — 2026-11-16 (Phase 2)
Vừa hoàn thành: T9–T12 (chưa commit)
Đang làm dở: (không)
Bước tiếp theo: user mở trình duyệt; chốt 3 điểm: (1) màn duyệt danh sách đặt "… chờ duyệt" (nhãn menu Phê duyệt trùng
  màn gốc); (2) 9 màn human chép nguyên từ màn Công ty (department/part/major/team add/_id, major/team index) — tên đặt theo
  route nhưng nội dung là công ty (lỗi có sẵn); (3) nút quay lại ở 7+ form Chấm công nay đứng một mình
Blocked:
Lỗi `mixins:` khai 2 lần ở 2 báo cáo Cơm: đã sửa ở T13.

### Checkpoint — 2026-11-16 (Phase 1)
Vừa hoàn thành: T1–T6 (code xong, chưa commit)
Đang làm dở: (không)
Bước tiếp theo: user mở trình duyệt kiểm — chú ý màn có chiều rộng cố định (trước full-width, nay trừ rail 58px),
  4 màn Cấu hình chấm công (mất sidebar con SettingSlidebar), Sơ đồ cơ cấu tổ chức (GoJS)
Blocked:
