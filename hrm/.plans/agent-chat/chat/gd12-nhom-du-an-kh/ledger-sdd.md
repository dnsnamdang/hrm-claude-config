# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/agent-chat/chat/gd12-nhom-du-an-kh/plan.md

Spec: design.md cùng thư mục. Worktree `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-nhom-trao-doi`, nhánh `gop_db-chat-nhom-du-an-kh` (api từ 86fcb16ba, client từ 814664a79). User cho phép "làm" 14/11 (phạm vi ở chat). DB local `db_gop_6_11`.
Workspace SDD (scratch): /private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/322109df-2fb2-436b-b5ec-1e4a38259b74/scratchpad/sdd12 (snap.sh, pkg.sh, briefs, reports)
Base trees: api 55c23d9095a8 · client 664438c2cc78

## Rulings tiền kiểm
- Ruling: KHÔNG commit — implementer không commit; review bằng tree snapshot (snap.sh) — sai thì chỉ mất tiện truy vết.
- Ruling: migration `2026_11_20_000001` — implementer chạy `--pretend` rồi `--path` đúng file đó (user đã cho phép) — sai thì rollback 1 index.
- Ruling: Task 2 gọi `KhProjectMemberSource::seed` (Task 3 định nghĩa) ⇒ T2 KHÔNG gọi seed; T3 thêm lời gọi vào `WorkspaceService::create` — sai thì T2 test thiếu thành viên (không cần ở T2).
- Ruling: e2e (HRM/e2e) không thuộc git — review T10 đọc file trực tiếp.

## Bảng tiền kiểm
| Cặp/Task | Chung | Kết quả |
|---|---|---|
| T1→T7 | `preview` nhận `company_id`; resource `company_name` | khớp |
| T2→T3 | `create` ↔ `seed` | lệch thứ tự ⇒ Ruling trên |
| T2→T4/T5/T6 | `Workspace::isKhProject`, `SOURCE_*`, `KhProjectSourceService::isClosed` | khớp |
| T2→T8 | `GET kh-sources` {id,code,name}; request `kh_source_type`/`kh_source_id` | khớp |
| T2→T10 | `GET kh-group` {workspace_id,is_member,can_create} | khớp |
| T3→T9 | `manager_role_label` | khớp |
| T4→T9 | TaskPanel gửi `workspace_id`, BE tự điền dự án/GP | khớp |
| T1 | test ↔ eligibleIds chữ ký mới | ok |
| T2 | test ↔ 5 câu 422 | ok |
| T3 | test ↔ seed / label | ok |
| T4 | test lệch nguồn 422 | ok |
| T5 | test dòng prospective_project_meetings | ok |
| T6 | test tin 1 lần | ok |
| T7–T10 | FE kiểm bằng Playwright, không unit test | ok (ghi nhận) |

## Tiến độ
- Task 1: dispatched (sonnet), base tree api 55c23d9095a8
- Task 1: implementer DONE_WITH_CONCERNS — tree api a0253917bc4fe689952c5e2f01667f2737cac915. 2 test WorkspaceTaskTest (exclusive) fail SẴN trước patch (controller chạy lại: 422 không có key workspace_id) ⇒ giao Task 4 (đụng đúng luật đó).
- Ruling: preview nhận company_id tuỳ ý không kiểm quyền thấy công ty — chấp nhận: Q14 cho chọn NV mọi công ty, preview chỉ trả tên NV — sai thì lộ danh sách NV công ty khác (đã chủ ý mở).
- Task 1: review ✅ spec + quality Approved (3 minor: company_id preview không exists — chấp nhận theo Ruling; test phụ thuộc dữ liệu local — như các test cũ). FE T7 phải tự so company với nhóm (resource đã có company_name).
- Task 1: complete (trees api 55c23d9..a025391)
- Task 2: dispatched (sonnet), base tree api a0253917bc4f
- Task 2: implementer DONE_WITH_CONCERNS — tree api c27b6225c1143a834e3280727aebf911a47bc10f. Migration 2026_11_20_000001 đã chạy --path --force (APP_ENV=production ở .env local, DB 127.0.0.1). Không có RED (viết code trước). 422 chỉ câu đầu/khoá — đúng format BaseRequest hiện có (chấp nhận).
- Task 2: review ✅ spec, quality Approved + 1 Important (N+1 sourceInfo ở WorkspaceResource) + minor 23000 bắt rộng ⇒ fix round 1 (resume implementer). Minor migration trùng dữ liệu: chấp nhận — prod 0 dòng source (cột mới dùng lần đầu).
- Task 2: fix round 1 DONE — controller tự soát diff fix (attachSourceInfo batch whereIn; catch 23000 chỉ theo tên index): đạt. tree api f2498bfe68c5
- Task 2: complete (trees api a025391..f2498bf)
- Task 3: dispatched (sonnet), base tree api f2498bfe68c5
- Task 3: implementer DONE — tree api 4c1739d94e0ec9ceb0e3f271389f2e432d214135 (report ghi hộ từ tin trả về)
- Task 3: controller tự review (diff ~120 dòng): spec ✅; Important: seed chạy TRƯỚC manager_ids ⇒ người nguồn được chọn làm Quản lý bị thành Thành viên; Minor: nhãn hạng mục rỗng chức vụ ⇒ fix round 1 (resume implementer)
- Task 3: fix round 1 DONE — controller kiểm thứ tự seed sau manager/member/department: đạt. tree api 384fb1afd3bf2bca338d402dc42a6d19c052e2a2
- Task 3: complete (trees api f2498bf..384fb1a)
- Task 4: dispatched (opus — tích hợp TaskService/TaskAccess + 2 test exclusive fail sẵn), base tree api 384fb1afd3bf
- Task 4: implementer DONE — tree api 2fd48347dd6e0947b381be05bf010a78ca5e8306. 2 test exclusive cũ: lệch fixture (GP id 1 thuộc dự án đã đóng, closedLinkErrors từ 5207f2a45) ⇒ sửa fixture. Thêm 1 dòng MessageService::resolveTaskCard. Tab TKT dùng prospective_project_id.
- Ngoài luồng (note, không sửa): tasks.solution_id không có index; ProspectiveProjectVisibleIdsTest lỗi FK roles có sẵn.
- Task 4: review ✅ spec, quality Approved; Minor 1 (PATCH assignee truyền project/solution cho nhóm thường ⇒ đổi hành vi dữ liệu cũ) ⇒ fix round 1. Minor 2,3: chấp nhận (query nhẹ ngoài vòng lặp; nguồn đóng đã chặn bằng MSG_SOURCE_CLOSED).
- Task 4: fix round 1 DONE (RED→GREEN ca nhóm thường dữ liệu cũ). complete (trees api 384fb1a..9fc0a05)
- Task 5: dispatched (sonnet), base tree api 9fc0a0580c27
- Task 5: implementer DONE — tree api 7596f40288ea6dda281f932841d086d70a0f9578. Meeting::canView thêm canViewByKhWorkspace. MeetingController store/update gọi ensureWorkspaceProjectLink.
- Ruling: nhóm GP lọc meeting theo DỰ ÁN của GP (giống tab Meeting manager GP getMeetingListForSolution), lệch chữ plan "solution_id" — 1 dự án = 1 GP nên tương đương; sai thì thấy dư meeting cấp dự án.
- Task 5: controller tự review (≈90 dòng prod): spec ✅ (trừ Ruling lọc theo dự án), canViewByKhWorkspace 1 EXISTS chạy sau nhánh rẻ, ensureWorkspaceProjectLink sau syncProjects — đạt.
- Task 5: complete (trees api 9fc0a05..7596f40)
- Task 6: dispatched (sonnet), base tree api 7596f40288ea
- Task 6: implementer DONE. Ruling: cascade đóng GP bằng mass update (ProspectiveProjectService:2053) bỏ qua observer ⇒ KHÔNG sửa service dùng chung; tin đóng/mở TKT gửi cả nhóm TKT lẫn nhóm GP của dự án — sai thì nhóm GP thấy tin TKT thay vì tin GP (vẫn đủ ý). fix round 1.
- Task 6: fix round 1 (tin TKT gửi cả nhóm GP) + round 2 (bỏ dedupe 10s) DONE; controller đọc observer: đạt. Cả folder Workspace 219/219 xanh (controller chạy). complete (trees api 7596f40..e259622)
- DỮ LIỆU TEST TẠM (phải TRẢ LẠI khi xong): prospective_projects#273 main_sale_employee_id 40→13; solutions#37 pm_id 40→13 (DB db_gop_6_11).
- Ruling: gộp Task 7+8+9 (FE chat, cùng CreateWorkspaceModal/MembersPanel) 1 dispatch + 1 review. Task 10 riêng. base tree client 664438c2cc78
- Task 7-9: implementer DONE_WITH_CONCERNS — tree client 6178f702ee50e6175072f342764a8cd60e550f5a. Playwright đo đạt; dữ liệu test đã dọn (2 nhóm, task 25680…). Push FCM cho NV 348 thử gửi nhưng local thiếu service account ⇒ không đi (đã kiểm log theo lời implementer).
- Task 7-9: review ✅ spec, quality Approved (3 Low). Controller thêm comment lý do V2BaseSelectRemote. Low 2 (công ty ngừng HĐ không hậu tố) + Low 3 (so theo tên công ty — cả 2 phía cùng từ companies.name) chấp nhận.
- Task 7-9: complete (trees client 664438c..6178f70 + 1 comment)
- Task 10: dispatched (sonnet), base tree client b6450fbeea34f8fc95976437e6b8c8f1acf1ba43
- Task 10: implementer DONE_WITH_CONCERNS — tree client 1e359e68c2de1f9d7002b7847a885d4179fb2d5e. e2e: workspace-kh-project 7/7, workspace-tasks 12/12, workspace-meetings 5/5, chat-core 8/8, bug-report 8/8 (cấp lại role tạm TMP_GD11_BaoLoi rồi gỡ). Sửa file dùng chung BasicSubsystem.vue (+watch drawerState.open ⇒ drawerMounted) — controller đọc: thêm 6 dòng, chỉ dựng ngăn khi mở; chấp nhận, báo user. Manager GP layout:false ⇒ mở nhóm ở tab mới /assign/workspaces/{id}.
- Task 10: complete. Final review: dispatched (opus) api 55c23d9..e259622, client 664438c..1e359e6
- Final review: Needs fixes. I1 (đóng / tự lưu trữ nhóm KH huỷ việc của dự án + 423 trên màn manager).
- Ruling I1: chọn phương án 1 — nhóm KH đóng/tự lưu trữ KHÔNG huỷ việc; assertWritable không chặn 423 cho việc của nhóm KH — theo anti-goal §2 "nhóm không đổi dữ liệu dự án"; sai thì user muốn huỷ theo nhóm ⇒ bật lại 1 nhánh.
- Ruling: sửa luôn M1 (đếm theo scopeTasks), M2, M3, M4, M6, M7; M5 (link dự án có thể 403 với người ngoài dự án) chấp nhận, báo user.
- Final fix: dispatched (opus)
- Final fix DONE: 7 mục + nới thêm DetailTaskResource/WorkspaceTaskController/xoá lô TaskController (cùng luật nhóm KH đóng không khoá việc) + eager load thêm source_*. PHPUnit Workspace 226 OK, Task 31 OK; e2e workspace-kh-project 7/7, workspace-tasks 12/12. Controller đọc diff + grep eager load thiếu source_*: đạt.
- Dữ liệu test ĐÃ TRẢ: #273 main_sale 13→40, GP#37 pm 13→40.
