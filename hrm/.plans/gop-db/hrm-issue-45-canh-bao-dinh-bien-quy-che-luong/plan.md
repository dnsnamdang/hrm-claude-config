# Cảnh báo lệch định biên ở quy chế lương + chưa phân nhiệm vụ ở QĐ định biên (HRM issue ISS-202611-0045) — @cuong61n

Nguồn: https://hrm.eteksofts.com/assign/issues?open_issue=45 (tester huyenntt tạo 21/11/2026, hạn 25/11). Nhánh `gop_db` (worktree `worktrees/gop_db-api` + `gop_db-client`).

## Quyết định đã chốt (27/11/2026, user)
- Điểm 1 — popup "Thêm/Sửa quy chế lương và hỗ trợ" theo ngạch lương (`AddRegulationSalary.vue`): so chức vụ ĐÃ LƯU trong quy chế (từng cấp bậc) với Bảng định biên hiện hành (`department_manpowers` cùng ngạch, gộp mọi phòng ban công ty đang chọn). **Chỉ cảnh báo chiều (a)**: chức vụ có trong quy chế nhưng định biên không còn ở cấp bậc đó (bị bỏ hoặc đã chuyển cấp bậc). Không báo chức vụ định biên mới thêm. Chỉ cảnh báo, không tự sửa, không chặn lưu.
- Điểm 2 — màn Tạo/Sửa QĐ ban hành/thay đổi định biên: **cảnh báo ngay khi vào màn** (chưa cần bấm Lưu) ngạch lương / chức vụ nào chưa phân nhiệm vụ; **Lưu thì chặn** (BE 422, FE hiện rõ tên ngạch/chức vụ, chuyển tới tab lỗi).
- Ví dụ thật prod: quy chế ngạch TPSG_CHUYÊN VIÊN (id 17) lưu 4 chức vụ bậc 1 (560, 563, 566, 521); định biên hiện hành chỉ còn 566, 610, 521 → cảnh báo 560 Trưởng BP Lắp Đặt SG, 563 Trưởng BP Công Nghệ SG.

## Phase 1 — Điểm 1: cảnh báo lệch định biên ở popup quy chế lương
### BE (hrm-api)
- [x] 27/11 `RegulationSalaryService::manpowerMismatches()`: với 1 quy chế (rank_group_id) → đọc `department_manpowers` công ty hiện tại (`CurrentCompany::id()`) cùng `working_position_group_id`, gom tập (rank_id, working_position_id) đang có; so với `regulation_salary_rank_group_working_positions` → trả `[{rank_id, rank_name, working_position_id, working_position_name, reason: removed|moved, moved_to_rank_name}]`.
- [x] 27/11 Trả `manpower_mismatches` trong `RegulationSalaryResource` (API detail popup Sửa). Màn Tạo mới không có gì để so → mảng rỗng.
### FE (hrm-client)
- [x] 27/11 `AddRegulationSalary.vue`: hộp cảnh báo vàng đầu popup (copy pattern `pages/assign/contracts/components/ContractTransferBgdModal.vue:14`) liệt kê từng dòng "Cấp bậc X — Chức vụ Y: không còn trong định biên / đã chuyển sang cấp bậc Z".

## Phase 2 — Điểm 2: chưa phân nhiệm vụ ở QĐ định biên
### BE (hrm-api)
- [x] 27/11 `ManpowerPlanningRequest`: thêm rule `list_rank_groups.*.mission_ids` required|array|min:1 + `.*.id` required (ngạch lương; chức vụ đã có).
- [x] 27/11 `withValidator`: lỗi nhiệm vụ gắn message nghiệp vụ có tên: "Ngạch lương X chưa phân nhiệm vụ" / "Chức vụ Y chưa phân nhiệm vụ" (key field để FE map tới tab).
### FE (hrm-client)
- [x] 27/11 `FormTableComponent.vue`: icon phân nhiệm vụ của ngạch/chức vụ chưa có nhiệm vụ → màu cảnh báo `#F59E0B` + popover "Chưa phân nhiệm vụ".
- [x] 27/11 `FormComponent.vue`: hộp cảnh báo vàng trên tab, tính realtime từ dữ liệu (hiện ngay khi vào màn Sửa / sau khi chọn phòng ban), liệt kê "Phòng ban – Ngạch – Chức vụ"; bấm Lưu còn thiếu → chặn ở FE, chuyển tới tab đầu tiên có thiếu; 422 từ BE hiện cùng chỗ.

- [x] 27/11 Tách component dùng chung `components/V2BaseWarningList.vue` (hộp vàng + danh sách lý do; từ `.tbgd-reasons` của ContractTransferBgdModal) — dùng ở cả 2 nơi trên.

## Kiểm
- [x] 27/11 BE script PHP in-process trên DB local (`local_hrm_erp`, user công ty 4): quy chế 15 (TPSG_NHÂN VIÊN) → báo đúng 1 chức vụ 326 "TPSG_Nhân viên Công nghệ" ở cấp bậc TPSG_NHÂN VIÊN 2 không còn trong định biên (đối chiếu tay SQL khớp); quy chế 14 → 1; ngạch công ty không có định biên → []. Validate: đủ nhiệm vụ → qua; placeholder `{id:null}` ở ngạch + chức vụ → 422 với "Ngạch lương TPSG_NHÂN VIÊN chưa phân nhiệm vụ" / "Chức vụ TPSG_Nhân viên Kinh doanh chưa phân nhiệm vụ"; thiếu hẳn key → 422. Tên tra bằng `withoutGlobalScopes()` để không ra "#id".
- [x] 27/11 FE Playwright local (3002 → 8003, TK namdangit, phải cài `livekit-client` vào worktree + chạy lại nuxt vì commit chat gọi điện mới kéo về):
  - Popup Sửa quy chế "NHÂN VIÊN 1" (id 7): hộp vàng đầu popup liệt kê đúng 4 chức vụ "không còn trong định biên hiện hành" (Nhân viên Bếp, tạp vụ, Chăm sóc cây, Thực tập sinh) khớp BE.
  - QĐ định biên 5 (nháp, 3 phòng): đủ nhiệm vụ → không cảnh báo, 7 icon xanh. Bỏ nhiệm vụ của ngạch + chức vụ (HN_KD2) → hộp vàng hiện ngay 2 dòng có tên phòng/ngạch/cấp bậc/chức vụ, 2 icon đổi `mdi-clipboard-alert-outline` màu #F59E0B; bấm Lưu → KHÔNG gọi PUT, tab HN_KD2 đỏ. Bỏ nhiệm vụ ở tab chưa mở (HN_QTTT) → validate chuyển sang đúng tab 1, tab đỏ. Gọi PUT thẳng (bỏ qua FE) → 422 "Ngạch lương QUẢN LÝ chưa phân nhiệm vụ" / "Chức vụ Trưởng phòng Kinh doanh chưa phân nhiệm vụ"; câu BE không hiện trùng với câu FE (sửa 1 lần: FE có dòng thì không nối thêm câu BE). Bấm icon vàng → popup phân công → chọn nhiệm vụ → Đóng → icon về xanh, dòng cảnh báo hết. Lưu lại đủ dữ liệu → PUT 200, về danh sách.
  - Console không lỗi (chỉ log 422 của axios khi cố ý test), log Nuxt/Laravel sạch.
- [x] 27/11 Commit + push `gop_db`: hrm-api `f93623bde`, hrm-client `e6bb8afe6` (rebase lên origin trước khi push). Deploy PROD tpe bằng `~/build_tpe.sh` trên hrm-prod (user bảo "đẩy lên prod") — **đã deploy PROD tpe 27/11/2026** (BE fast-forward → f93623bde, migrate/route:cache/catalog-sync OK; FE build 4m30 → e6bb8afe6, bundle prod có chuỗi cảnh báo; site 200; warning favicon.ico trong log build là có sẵn từ trước). Còn: bình luận/đóng issue 45 cho tester.
