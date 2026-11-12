# Làm lại màn Bảng định biên theo quy mô — chặn xóa dòng do Quyết định + giao diện V2 (chưa có số Redmine) — @cuong61n

Nguồn: khách phản ánh màn `/human/department-manpower` đang dùng Quyết định mà vẫn có nút Xóa (khách muốn không xóa được).
Thiết kế: Pen `~/Downloads/meeting-mobile_v2.pen` — frame "HRM · Bảng định biên theo quy mô — Danh sách (menu ngang)" + component `C/Topbar menu ngang`.
Nhánh: `develop` (có gốc `gop_db`) cả hrm-api và hrm-client.

## Quyết định đã chốt (2026-11-12)
- Điều kiện xóa = phương án A: bật `use_decision` → ẩn Xóa với mọi dòng; tắt (nhập tay) → xóa được. BE chặn 423, FE ẩn hẳn nút (không disable).
- Nút Lịch sử ở cột Hành động: để lần sau (bảng chưa có audit log, cần migration + log BE).
- Bộ lọc: bỏ ô Công ty (BE đã tự lọc theo công ty đang chọn); thay bằng Nhóm chức vụ + Chức vụ. Giữ Phòng ban, Loại phòng ban.
- Header menu ngang giữ nguyên, chỉ thêm mã công ty dưới tên người dùng (cần BE trả `code` trong danh sách công ty của user).

## Phase 1 — BE (hrm-api)
- [x] (12/11/2026) Entity DepartmentManpower: `isUsingDecision()` (đọc master_settings use_decision, nhớ trong request) + `isCanDelete()`
- [x] (12/11/2026) Service index: thêm lọc `keyword` (tên phòng ban / nhóm chức vụ / chức vụ), `working_position_group_id`, `working_position_id`; trả `is_can_delete` cho từng nhóm
- [x] (12/11/2026) Service/Controller delete: không tìm thấy → 404 (trước đây 500), không cho xóa → 423 kèm message rõ

## Phase 2 — FE (hrm-client) `pages/human/department-manpower/index.vue`
- [x] (12/11/2026, chờ test trình duyệt) Dựng lại theo khuôn V2 trong layout menu ngang: PageHeader + V2BaseSmartFilterPanel (floating, ô tìm nhanh) + V2BaseDataTable (cellSpan gộp Phòng ban / Nhóm chức vụ / Hành động)
- [x] (12/11/2026, chờ test trình duyệt) Cột Hành động dùng V2BaseRowActions: Xóa ẩn theo `is_can_delete`; bỏ nút Xem (tên nhóm chức vụ là link mở popup Xem/Sửa)
- [x] (12/11/2026) Popup Thêm/Sửa/Xem dựng lại trên V2BaseModal + V2BaseLabel/V2BaseSelectInModal/V2BaseInput/V2BaseCurrencyInput/V2BaseError + V2BaseTableScroll, cảnh báo thoát chưa lưu (unsavedModalMixin), kiểm FE bấm Lưu báo đỏ mọi ô bắt buộc cùng lúc; giữ nguyên API + quy tắc nghiệp vụ

## Chưa làm (ghi để lần sau)
- Nút Xuất Excel, Tuỳ chỉnh cột hiển thị (skill list-page bắt buộc), nút Lịch sử
- Mã quyền riêng cho thêm/xóa định biên (Catalog chỉ có `human.dinh_bien_theo_quy_mo.view`; route DELETE chưa gắn checkPermission)
- BE trả `code` công ty trong `company_roles` + FE hiện mã công ty ở Topbar

## Kiểm đã làm (12/11/2026)
- BE (script PHP ngoài, DB local): index trả `is_can_delete=false` khi dùng Quyết định; lọc keyword/nhóm chức vụ/chức vụ đúng, SQL OR của ô tìm nhanh nằm trong 1 cặp ngoặc (không phá phạm vi quyền); DELETE khi dùng Quyết định → 423, id không tồn tại → 404 (trước đây 500), số dòng không đổi.
- E2E Playwright thật trên http://127.0.0.1:3000 (tài khoản test namdangit), 2 chế độ:
  - Dùng Quyết định (use_decision=1): ẩn Tạo mới + cột Hành động; popup "Xem định biên" chỉ có Huỷ, ô khóa; gọi thẳng API xóa → 423, còn nguyên 62 nhóm.
  - Nhập tay (tạm đặt use_decision=0, đã TRẢ LẠI nguyên giá trị gốc kể cả updated_at): có Tạo mới + Sửa + Xóa; Sửa nạp đúng dữ liệu; Tạo mới mở trắng; Xóa → popup xác nhận → "Xóa thành công." → dòng biến mất, DB không còn dòng/vị trí.
  - Danh sách: 10 phòng ban/trang × 3 trang, đổi cỡ trang, 47/47 dòng khớp API (0 sai lệch), gộp ô Phòng ban/Nhóm/Nhiệm vụ theo phòng/Hành động đúng; tìm nhanh (Enter), 4 ô lọc (kể cả Loại phòng ban = 0), kết hợp lọc, trạng thái rỗng, Làm mới; nút Xem nhiệm vụ / Xem đầy đủ / Thu gọn độc lập từng hàng.
- Lỗi tìm ra khi test và đã sửa: (1) dòng đếm "1–22/22" sai khi mỗi phòng ban gồm nhiều dòng → điền from/to; (2) tên phòng ban/cấp bậc dài bị cắt "…" → cho xuống dòng; (3) ô rỗng hiện chữ "[]" (slot rỗng làm V2BaseDataTable in mảng rỗng) → bọc slot trong thẻ; (4) thiếu cột Nhiệm vụ theo phòng, Doanh số/Đơn hàng tiêu chuẩn so với màn cũ → khôi phục đủ; (5) cột Nhiệm vụ bị cắt, không xem được đầy đủ → thêm nút Xem đầy đủ/Thu gọn.
- Chưa test được: tài khoản phạm vi Phòng ban/Công ty (2 tài khoản kd1 không có quyền Xem màn này).
- Lưu ý: cột Doanh số/Đơn hàng tiêu chuẩn luôn trống như màn cũ — DB `department_manpower_positions` không có cột lưu (popup có ô nhập nhưng không lưu đi đâu). Cần user quyết định giữ hay bỏ.
- Lệch thiết kế Pen: tên phòng ban là cột "Phòng ban" gộp dọc (V2BaseDataTable không có dòng trải hết cột); phân trang theo phòng ban ở FE vì BE trả cả danh sách; không dùng filterStateMixin vì màn không có trang chi tiết.

## Bổ sung 12/11/2026 (sau góp ý)
- Sửa dùng chung `V2BaseDataTable`: dòng "Đang tải"/"Không có dữ liệu" luôn nằm giữa vùng nhìn thấy kể cả bảng cuộn ngang (trước lệch ~570px) — đã kiểm màn định biên + màn Quốc gia.
- Popup làm lại theo V2, test e2e thật (use_decision tạm =0, đã trả lại gốc): bấm Lưu trống → 4 lỗi đỏ cùng lúc; nhập đủ → Lưu thành công (DB: 1 dòng định biên + 1 vị trí + 1 cấp bậc + 1 P2-P3 + 2 nhiệm vụ nhóm, created_by tự gán); Sửa nạp đủ dữ liệu, đổi giá trị → Lưu → danh sách cập nhật; trần < sàn báo "Không hợp lệ" và không gọi API; trùng phòng ban + nhóm → BE trả error_messages; cảnh báo "Thông tin chưa lưu" khi Đóng/Esc lúc đã sửa; Xóa bản ghi thử qua giao diện. Dữ liệu thử đã xóa, cài đặt đã trả.
- Pen: frame popup đã vẽ lại theo V2.
- Lưu ý: BE vẫn trả lỗi validate kiểu cũ (HTTP 200 + `error_messages`), FE xử lý theo hợp đồng này; đổi sang 422 chuẩn là việc riêng.

- Sửa hover bảng (user báo xấu): trước chỉ tô ô của `<tr>` đang trỏ nên ô gộp dọc xanh cả khối còn dòng dưới trắng, và ô đầu dòng nối tiếp có viền trái đặc đậm hơn viền chấm. Nay hover tô cả NHÓM chức vụ (rowClass `dm-g-<id>` + `dm-row-hover`), STT/Phòng ban giữ nền, dòng nối tiếp bỏ viền trái đặc. Làm ở trang định biên, KHÔNG đụng V2BaseDataTable. Đã kiểm bằng rê chuột thật + đo màu nền các ô.

- Sửa hover lần 2 (user: trỏ 1 dòng con mà tô cả cụm là sai): chỉ tô các ô RIÊNG của dòng đang trỏ, ô gộp (STT, Phòng ban, Nhóm chức vụ, Nhiệm vụ theo phòng, Hành động — class `dm-span-cell`) luôn giữ nền, trỏ vào ô gộp thì không tô dòng nào. Đã đo màu nền ô bằng rê chuột thật.
- Lỗi popup Sửa trống Chức vụ/Cấp bậc (user báo, tắt Quyết định mới lộ): ô chỉ liệt kê chức vụ cùng nhóm và cấp bậc thuộc chức vụ, nhưng dữ liệu cũ lệch (DB: 102/219 vị trí có chức vụ ngoài nhóm của dòng, 103/221 cấp bậc ngoài danh sách của chức vụ; 56/140 dòng định biên bị ảnh hưởng) → giá trị đã lưu không nằm trong option nên ô trống. Sửa: `withSelected()` luôn gộp thêm giá trị đang chọn vào option của Chức vụ, Cấp bậc, Chức danh, Nhiệm vụ nhóm, Nhiệm vụ vị trí (quy tắc "giá trị đang dùng luôn phải hiện"). Kiểm: quét 62 nhóm bằng popup Sửa thật (tắt Quyết định tạm, đã trả lại) → 0 nhóm trống; tắt tạm hàm gộp thì 10/10 nhóm thử bị trống Chức vụ + Cấp bậc (tái hiện đúng lỗi).
- Chưa làm: dữ liệu lệch nhóm/cấp bậc vẫn nằm trong DB — popup nay hiển thị đúng nhưng nếu muốn dọn dữ liệu cho khớp danh mục là việc riêng (cần hỏi nghiệp vụ).

- Header: thêm mã công ty đang làm việc dưới tên người dùng (`components/BasicSubsystem.vue`, dùng cho cả header menu ngang lẫn sidebar; menu ngang màu xanh #1F5FAE, sidebar kế thừa màu chữ; tooltip = tên đầy đủ). BE: `AuthNewController` trả `code` trong `company_roles` (trước chỉ id + name). Chưa có `code` (BE chưa deploy) thì dòng mã tự ẩn. Đổi công ty = API + `$router.go(0)` nên mã tự cập nhật. Đã kiểm: TPE hiển thị, cao thanh header vẫn 60px.
- Nhiệm vụ đánh số đầu dòng (`1.`, `2.`…, canh thẳng khi xuống hàng) ở cột "Nhiệm vụ theo phòng" (mở ra) và cột "Nhiệm vụ" (cả thu gọn lẫn mở rộng).

- Header (user góp ý "chưa cân đối"): làm lại khu vực tài khoản trong `BasicSubsystem.vue` — [ảnh] [tên / chip mã công ty] [mũi tên] canh giữa theo chiều dọc, tên + chip cùng căn trái (trước bị căn giữa lệch nhau do text-align của nút), mã công ty thành chip nền xanh nhạt (#E8F0FC, chữ #1F5FAE; sidebar nền navy: chip trắng mờ). Đã đo: avatar, mũi tên, các icon cùng trục y=31 trong thanh cao 60px. Lỗi tự gây ra khi làm: lỡ xóa 2 rule `.noti-icon`/`.noti-title`, đã khôi phục nguyên văn (git diff chỉ còn phần sửa chủ ý). Pen đã đồng bộ.

- Header sidebar (nền navy) bị xấu: chip mã công ty đặc sáng như menu ngang, icon không thấy. Thêm prop `onDark` cho `BasicSubsystem` (`SidebarMenu.vue` truyền `on-dark`): nền tối dùng chip trắng mờ + viền nhẹ, chữ/icon trắng; menu ngang giữ chip xanh nhạt. Đã chụp + đo cả 2 layout (sidebar: /human/nations; menu ngang: /human/department-manpower).

## Trạng thái
Code xong BE + FE, đã test e2e (xem trên), chưa push, chưa deploy.

## Phần 2 — Làm lại màn Phân công nhiệm vụ `/human/assignment_missions` (@cuong61n) — 2026-11-12
- Yêu cầu: khách (ảnh chụp, khung đỏ cột "Nhiệm vụ được giao") nhờ sửa giao diện; user: "design lại và sửa luôn".
- Nguyên nhân lỗi thấy trong ảnh: `shouldRenderWorkingPosition` bỏ ô Chức vụ nếu CHỨC VỤ ĐÃ XUẤT HIỆN Ở BẤT KỲ DÒNG TRƯỚC, nhưng `getRowspan` chỉ đếm dòng LIỀN NHAU → nhân viên cùng chức vụ nhưng không liền nhau bị mất 1 ô, cả hàng lệch trái 1 cột (Cấp bậc nằm dưới "Chức vụ", Nhiệm vụ trống chỉ còn nút).
- Hướng làm (FE thuần, không đổi API): V2 list (PageHeader + V2BaseSmartFilterPanel + V2BaseDataTable), phẳng hoá Phòng ban → Nhóm → Nhân sự, sắp theo chức vụ để gộp ô liền nhau (`cellSpan`); cột Nhiệm vụ được giao = 1 select nhiều (chip) thay cho nhiều select rời; Lưu chỉ hiện khi dòng có thay đổi; popup Xem nhiệm vụ / Nhiệm vụ chưa giao dựng lại trên V2BaseModal.
- [x] Code xong 2026-11-12: pages/human/assignment_missions/index.vue viết lại + components/MissionListModal.vue (thay ListMissions + MissionNotAssigns, đã xoá 2 file cũ)
- [x] Test Playwright 2026-11-12 (namdangit): dòng thẳng cột, gộp ô Chức vụ đúng; chọn nhiệm vụ → viền cam + hiện Lưu; Lưu thật OK (toast cảnh báo còn nhiệm vụ chưa giao); popup Xem / Chưa giao OK; đã trả dữ liệu test về cũ.
- Test lần 2 (2026-11-12): tìm kiếm / trống / phân trang / đổi cỡ trang / lọc Phòng ban, Loại phòng ban, Công ty / Làm mới OK, 0 lỗi console. Sửa 3 lỗi tìm ra: (1) bấm "Ở lại" ở hộp chưa lưu thì bảng nhảy sang trang mới còn dữ liệu cũ → hoàn lại trang/bộ lọc; (2) watcher bộ lọc gọi API cả khi không đổi gì → hộp hỏi lặp; (3) 2 lần tìm liên tiếp sau "Tiếp tục" hỏi lại → cờ `discarding`.
- Test phân quyền (2026-11-12, tài khoản cannt.kd1 + 3 vai trò tạm ZZTEST_PCNV_* chỉ có `human.phan_cong_nhiem_vu.view` ở phạm vi Bộ phận/Phòng ban/Công ty; đã XOÁ vai trò + dòng quản lý phòng ban tạm, đếm lại = 0):
  - Phòng ban (quản lý phòng 50): UI chỉ 1 phòng CSKH, 28 nhân sự; lọc phòng 51 / công ty 4 → 0 dòng.
  - Công ty: 19 phòng / 318 nhân sự, không có ô lọc Công ty; company_id=2|4 → 0 dòng (không lọt chéo công ty).
  - Bộ phận (API): 29 nhân sự của bộ phận 11 (2 phòng). KHÔNG vào được từ UI: `menu.js` mục 17 chỉ khai `isShow` tên cũ Tổng công ty/Công ty/Phòng ban → user chỉ có quyền Bộ phận bị chuyển 404 (lỗi có từ trước, chưa sửa vì menu.js dùng chung — chờ user chốt).
  - Không có vai trò: API vẫn trả 200 nhưng chỉ 1 dòng (chính họ); FE ẩn menu.
  - Lưu nhiệm vụ: trong phạm vi → 201 như thường; ngoài phạm vi (phòng 51) → HTTP 500 (`EmployeeSalaryHistoryService::saveMission` find() null) — không ghi gì, nhưng nên trả 403/404.
- Sửa thêm: ô gộp dọc (STT, Phòng ban, Nhóm, Chức vụ) canh TRÊN — phòng nhiều nhân sự thì chữ canh giữa nằm ngoài màn hình. Chưa commit.

### Sửa 3 vấn đề phân quyền (2026-11-12, @cuong61n) — đã code + test, chưa commit
- [x] 1. `hrm-client/components/menu.js` mục 17: thêm `isShow` 'Xem phân công nhiệm vụ theo bộ phận' (alias có sẵn trong permission_aliases, min_scope 1) → user chỉ có quyền Bộ phận vào được màn. Test UI: vào được, thấy 29 nhân sự của bộ phận, Lưu thật OK.
- [x] 2. Điều tra lỗi 500: KHÔNG phải ngoài-phạm-vi như ghi nhầm trước đó mà là id đã xoá mềm (find() null). Nhưng test lại phát hiện LỖ HỔNG THẬT: `POST payroll/employee-salary-histories/store_mission` không kiểm phạm vi → user quyền Phòng ban 50 ghi đè được nhiệm vụ của nhân sự phòng 51 (đã khôi phục dữ liệu ngay). Sửa: `EmployeeSalaryHistoryController::store_mission` kiểm trước — id không có/đã xoá → 404, ngoài phạm vi → 403; `DepartmentManpowerService` tách `assignmentScopeQuery()` (dùng chung danh sách + chốt chặn) và `canAssignMissionTo()`. Test: ngoài phạm vi 403 (DB không đổi), xoá mềm 404, thiếu id 404, trong phạm vi 201.
- [x] 3. Ô lọc Phòng ban theo phạm vi: API assignment_missions trả thêm `scopeDepartmentIds` (null khi phạm vi Công ty trở lên); FE chỉ liệt kê các phòng đó. Test: quyền Phòng ban → chỉ 1 phòng.
- Đã dọn vai trò/quản lý phòng ban test tạm (đếm = 0). Trong lúc test tôi lỡ bỏ chọn 1 nhiệm vụ của Phạm Ngọc Quý rồi lưu — đã gán lại đúng (mission 150), khớp bản ghi trước.
