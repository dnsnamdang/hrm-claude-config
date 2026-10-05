# Redmine #10455 — Lịch sử thiết lập/phân ca/cấu hình HCNS/cấu hình giao việc (@manhcuong)

Code gốc: nhánh feature-10455 (@khoipv), đã merge gop_db (API PR #634, Client PR #630).

- [x] Rà 11 hạng mục trên gop_db: đủ code; PROD hrm_erp_gop đủ 18 bảng lịch sử + 18 migration (2026-09-26)
- [x] Mở lại menu "Lịch sử phân ca" (components/menu.js — bị comment từ commit 10e0f70b9), chưa commit
- [x] Test Playwright từng trường 11 hạng mục trên gop_db local (2026-09-26): lịch sử đủ trường; 4 lỗi nghiêm trọng (bảo mật màn Người dùng/API, mất quyền khi lưu, mất ETEK GREEN, route Cài đặt không auth), 6 cao, 7 TB — báo cáo https://claude.ai/artifact/6o3CrMvH1BGdPWQqjJRnKn; chưa sửa lỗi nào

## Phase 2 — Sửa lỗi sau test (2026-09-26) — sửa thẳng worktree gop_db, chưa commit
User chốt: quyền dùng 'Quản lý phân quyền' + quyền màn cấu hình tương ứng; bool popup thống nhất Có/Không; HM9 thêm lối vào lịch sử phân ca theo NV.
### Nhóm A — Lịch sử phân ca
- [x] C1 thêm cột Mô tả sự kiện · C2 dời ngày BĐ muộn hơn xoá phân ca cũ + log · L3 chặn gán ô đã có ca · UI chuẩn (V2BaseBadge, nút V2Base, khuôn tên NV, dropdown trống, icon đè nhãn, Excel mã dạng text) · nút Xoá bảng phân ca chi tiết · HM9 lối vào theo NV
### Nhóm B — Thiết lập chấm công
- [x] N3 mất ETEK GREEN · N4 route master-settings bắt đăng nhập+quyền · C3 khung giờ chồng chéo chính nó · T6 500 khi trống · C4 ca làm việc tự tính lại Giờ công · T7 miễn CC lọc công ty · số en-US · Bật/Tắt→Có/Không · placeholder · mũi tên đỏ · (trống) vs 0
### Nhóm C — Phân quyền / HCNS / Giao việc
- [x] N1 gắn quyền màn+API · N2 mất quyền model_type App\Employee · C5 500 QL tất cả PB · C6 mức ưu tiên theo công ty · T1 popup HCNS theo màn · T2 % thâm niên · T3 BHXH log rỗng · T4 tên phân hệ · T5 nút Lịch sử màn Sửa chức vụ · nhẹ (Vị trí, company_roles mồ côi, popup Đóng dự án, ô tiền trống→0)
- [x] Bổ sung: gate quyền mọi route ghi + histories nhóm chấm công (Thiết lập thông số), gate theo trường POST general-regulations (5 màn dùng chung), BHXH/menu 3 màn HCNS, EmployeeRoleStoreRequest, decimal working_hour_deducted, lọc công ty miễn chấm công, cascade xoá nghỉ cắt phép/ca
- N2 KHÔNG chuẩn hoá model_type App\Employee (vai trò ERP, ErpPermissionHelper đọc riêng) — sửa code: storeRole chỉ ghi quyền HRM, hiện vai trò ERP chỉ xem

### Checkpoint — 2026-09-26
Vừa hoàn thành: sửa toàn bộ lỗi test (3 nhóm), đã verify Playwright/API từng lỗi, php -l sạch, chưa commit
Đang làm dở: (không)
Bước tiếp theo: user review → commit gop_db (LOẠI file của phiên khác: District*, ServiceService, ServiceExport, ExportColumnRegistry, pages/human/districts/*) → deploy PROD: migrate 3 file 2026_09_26_* + route:cache; SQL dọn mồ côi chờ duyệt
Blocked:
- [x] UI màn Lịch sử phân ca: thêm PageHeader cho layout menu ngang (bộ lọc không dính sát menu), không sửa base; ghi nguyên tắc list-page SKILL mục 2b
- [x] Commit nhánh task_10455 (tách từ gop_db local HEAD api 14f10900e / client 58f23512f): api 8d2419668, client b3161ac59 — worktree riêng worktrees/task_10455-api + task_10455-client; đã gỡ thay đổi #10455 khỏi worktree gop_db chung (backup patch ở scratchpad). Chưa push.
- [x] Đối chiếu spec Excel: HM9 đổi sang POPUP 'Lịch sử chỉnh sửa - Tên NV' trên Bảng phân ca tổng hợp (components/timesheet/shift-history/EmployeeShiftHistoryModal.vue, 9 bộ lọc, 9 cột); cột Người thực hiện thêm mã phòng; tên 4 cột theo spec; filter-options thêm changed_bys; utils/shiftHistoryFormat.js dùng chung. Chưa commit, chưa Playwright. Chờ chốt: sự kiện NV nghỉ việc, khuôn tên NV trong ô
- [x] Skill modal-popup thêm mục 4c 'Popup có BỘ LỌC' (V2BaseSmartFilterPanel in-modal, khuôn popup Thêm hàng hoá Báo giá) + checklist; EmployeeShiftHistoryModal chuyển sang khuôn đó
- [x] Popup lịch sử theo NV làm lại đúng skill: ô tìm nhanh (BE thêm keyword), nâng cao thu gọn, bảng gọn + V2BasePagination khung 98vh, nút Đóng mặc định V2BaseModal; skill modal-popup 4c cập nhật theo. Playwright :3005 đạt (keyword LINH=3, lọc Xóa=1 khớp DB, 0 lỗi console/4xx). Chưa commit
- [x] Testcase 10 file (.plans/gop-db/lich-su-thiet-lap-10455/testcase - *.xlsx, gen_testcase.py): 683 TC, kiểm thuật ngữ OK

## Phase 3 — Sửa lỗi phát hiện khi soạn testcase (2026-09-28, nhánh task_10455, chưa commit)
- [x] Nhóm X (chấm công): cờ Sử dụng quyết định bị reset · CTV miễn chấm công mất NV sau lọc công ty · chặn xoá ca đã phân ở máy chủ · thông báo sai chữ/màu (khung giờ, nghỉ lễ, lỗi lưu)
- [x] Nhóm Y (quyền/HCNS/giao việc): tên mức ưu tiên trùng theo công ty · lương cơ bản trống→0, đơn giá công khoán bắt buộc lệch, BH thất nghiệp NSDLĐ số âm · nhãn popup khác form, placeholder "Tất cả", trùng tiêu đề popup
### Checkpoint — 2026-09-29
Vừa hoàn thành: Phase 3 cả 2 nhóm, verify Playwright :3005/:8005, testcase cập nhật (chấm công 310 TC, quyền/HCNS/giao việc 260 TC). Chưa commit.
Bước tiếp theo: user duyệt → commit task_10455; deploy chạy 2 migration 2026_09_28_000001 (Assign priority unique theo công ty, Timesheet backfill company_id miễn chấm công).
Blocked: chờ chốt — dọn dữ liệu miễn chấm công trùng; lối đổi use_decision; câu lang min.numeric; tiêu đề popup chức vụ ID-Tên; màn /human/settings cũ; TC khoá ô ca đã phân (can_delete luôn true).
- [x] Chốt 29/09: lang min.numeric → 'Không được nhỏ hơn :min.' (BE validation.php + bảng trong CLAUDE.md); tiêu đề popup chức vụ chỉ tên; TC ca đã phân không khoá ô; không dọn trùng miễn CC, không làm lối đổi use_decision, không sửa màn /human/settings cũ; duyệt prop AddEmployee.vue. Testcase tổng 696 TC
- [x] Commit + push nhánh task_10455: API c216d955c, Client 243b3b857 (29/09/2026)
- [x] Đối chiếu testcase Lịch sử phân ca với giao diện :3005 (29/09): 129 TC; sửa popup NV nút Làm mới sau tìm nhanh không tải lại (EmployeeShiftHistoryModal.vue), Excel DS nhân viên thêm bề rộng cột (ShiftAssignmentHistoryEmployeesExport.php). Chưa commit
- [x] Đối chiếu testcase Thiết lập chấm công (5 file) với giao diện :3005 (29/09): 314 TC; sửa race form Sửa khung giờ làm thêm + nghỉ lễ (khoá Lưu khi đang tải), nhãn lựa chọn popup lịch sử Quy định nghỉ theo đúng chữ trên màn, tên chức vụ ngoài phạm vi trong lịch sử làm thêm (bỏ "#id"), bỏ messages() tự khai 3 request Loại nghỉ/Nghỉ lễ/Nghỉ cắt phép, tiêu đề màn Sửa ca. Chưa commit
- [x] Đối chiếu testcase Phân quyền/Người dùng/Cấu hình HCNS/Cấu hình giao việc với giao diện :3005 (29/09): 261 TC; sửa popup Thêm khung giờ (tự đóng sau OK, giờ đủ 2 chữ số — add-time-slot-modal.vue), bấm chữ 'Thêm mới' mở được popup (assign/settings/index.vue). Chưa commit. Chờ chốt: Phân hệ chấm công trống trên màn Sửa chức vụ (78 quyền type NULL)
- [x] Đối chiếu testcase với màn thật (704 TC) + 10 lỗi code; push task_10455: API cbff99313, Client eb74ed1fd (29/09/2026)
- [x] Merge task_10455 vào develop (local, chưa push): API edaaf4703, Client f9b81c6ae — 2 conflict giữ bản develop (MenuSettingService use_decision theo chốt 28/09; tiêu đề popup chức vụ)
- [x] Push develop: API 7b4cba665..edaaf4703, Client 45fa304a2..f9b81c6ae (29/09/2026)
- [x] Gộp testcase 1 file 'testcase - Lịch sử thiết lập (#10455).xlsx' (10 sheet, 704 TC) — gen_testcase_1file.py
- [x] Xoá 10 file testcase lẻ, chỉ giữ file gộp; gen_testcase.py gọi gen_testcase_1file.py

## Phase 4 — Chuẩn hoá 17 popup lịch sử theo skill entity-history (2026-09-30, làm thẳng trên develop, user chốt)
- [x] Khung BE: SettingHistoryService + interface/base adapter + SettingHistoryController, route `setting-histories/{type}/{id}` (+ filter-options), quyền + chặn công ty theo adapter (30/09)
- [x] Khung FE: `components/modal/SettingHistoryModal.vue` (V2BaseModal + SystemInfoSection, endpoint-base setting-histories)
- [x] 2 mẫu: `general_regulation` (tab Chung) + `leave_type` (Loại nghỉ) — thay popup, xoá GeneralHistoryModal/LeaveTypeHistoryModal, route cũ giữ + ghi chú đã thay thế; verify API + Playwright 22/23 (1 fail = warn Vue có sẵn của trang), đã dọn log test (leave_type_history 39-43, general_regulation_history 46-47, leave_types 69 đã xoá)
- [x] Hướng dẫn nhóm sau: `SETTING_HISTORY_ADAPTER.md`
- [ ] BE+FE: chuyển 15 popup còn lại theo SETTING_HISTORY_ADAPTER.md (3 nhóm song song)
  - [x] Nhóm C (5 popup HCNS/giao việc, 30/09): adapter human_setting(+_salary/_manpower/_insurance), assign_config(+_places), priority_level, deadline_config, project_close_config; thay FE 5 màn, xoá 5 popup cũ, route cũ ghi chú ĐÃ THAY THẾ; verify API (DTO/403/400/khớp route cũ) + Playwright 0 fail; đã dọn log test + trả dữ liệu. Chưa commit
  - [x] Nhóm B phần phân quyền + ca (30/09): adapter role_permission, employee_permission, working_shift; thay FE 3 màn danh sách, xoá 3 popup cũ, route cũ ghi chú ĐÃ THAY THẾ; verify API (DTO/403 quyền/403 công ty khác/400) + Playwright 48/49 (1 = warn Vue có sẵn màn Chức vụ); đã dọn log test + trả dữ liệu NV 448. Chưa commit
- [x] 3 màn Sửa (chức vụ, người dùng, ca): Lịch sử thành khối SystemInfoSection trong thân trang, bỏ nút Lịch sử ở footer/cạnh nút Lưu (30/09, nhóm B)
- [ ] Verify Playwright + cập nhật testcase gộp; sửa dòng mẫu cũ trong skill entity-history
- [x] Phase 4 xong: 17 popup → SettingHistory (22 adapter), 3 màn Sửa có khối Lịch sử; testcase gộp cập nhật (chấm công 350, quyền/HCNS/giao việc 278, phân ca 129 = 757 TC). Sửa thêm: performers Cài đặt toàn hệ thống, actor fallback email, nhãn 2 danh sách chức vụ giao việc. Chưa commit
- [x] Chốt 30/09: SystemInfoSection mũi tên xám (.si-arrow) + placeholder 'Chọn…' (+ ui-base.md); migration 2026_09_30_000001 role_permission_history MEDIUMTEXT (đã chạy local) + log cũ bị cắt hiện ghi chú; bỏ ngoại lệ 'Bảng chấm công chi tiết' ở lịch sử người dùng; giữ ô màu chỉ chữ + tên phân hệ 2 nơi. Testcase 759 TC. Chưa commit
- [x] Push develop 30/09: API bfacae831..965c5c7df, Client ..add1ed5f3 (fd57a7f2c + merge origin/develop). Không commit 2 file Tỉnh/Thành của phiên khác
- [x] 30/09: nhãn dòng lịch sử màn thiết lập theo bộ chuẩn (SettingHistoryService::standardLabel/standardColor) — bỏ nhãn riêng 'Cập nhật quy định chung'…; mức ưu tiên + danh sách chức vụ đưa định danh vào nội dung; skill entity-history §0a cập nhật. Chưa commit
- [x] 30/09: nhãn nhóm 2 danh sách chức vụ Quy định làm thêm tách tên danh sách; testcase cập nhật nhãn chuẩn (759 TC, OK 10 sheet). Chưa commit

## Fix 01/10/2026 — Dời ngày BĐ bảng phân ca xoá mất ca ngày đã qua (PROD)
- [x] Dữ liệu PROD: khôi phục 5.906 dòng shift_detail_employee_dates bị gỡ sáng 01/10 (08:49–09:54, 15 bảng phân ca) từ binlog, giữ nguyên id; file ở `~/khoiphuc_phanca_20261001/` trên server PROD; tính lại công 09/2026 cho 270 NV đang làm (recalc.sh, chạy nền)
- [x] BE: `WorkShiftDetailService` — dời BĐ muộn hơn chỉ gỡ từ max(BĐ cũ, hôm nay), cửa sổ log khớp theo (`shiftStartRemoveFrom`). Chưa commit, chưa test end-to-end
