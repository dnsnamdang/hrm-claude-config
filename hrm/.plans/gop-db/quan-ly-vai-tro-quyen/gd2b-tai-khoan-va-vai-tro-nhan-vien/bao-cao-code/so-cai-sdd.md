# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-claude-config/hrm/.plans/gop-db/quan-ly-vai-tro-quyen/gd2b-tai-khoan-va-vai-tro-nhan-vien/plan.md
Spec: design.md + mockup.html cùng folder.
User 27/10: "làm" — 3 repo wt-rbac nhánh rbac, KHÔNG commit; chạy migration 2026_11_02_000001 vào hrm_erp_rbac_test; kiểm UI rehearsal dữ liệu Zz.
Cơ chế diff thay commit: snap.sh TAG (tree id qua index tạm) + pkg.sh FROM TO. Snapshot base0 = trước Task 1.

## Pre-flight scan
| Cặp/Task | Chia sẻ | Kết quả |
|---|---|---|
| T1↔T2/T3 | employee_permission_history.company_id | T1 tạo cột + adapter đọc; T2/T3 ghi company_id=C. Khớp |
| T2↔T3 | EmployeeRoleController/Service, routes | T3 mở rộng T2. Khớp |
| T2↔T4 | routes/api.php, ExportColumnRegistry | thêm khác key. Khớp |
| T3↔T8 | BulkPermissionService / route timesheet/bulk-permissions | T8 chỉ gỡ route, giữ service. Khớp |
| T6↔T8 | BulkPermission*.vue | T6 chuyển file; trang cũ còn import tới T8 → xem Ruling 2 |
| T5↔T6 | admin.js | sửa 2 mục khác nhau. Khớp |
| T4↔T5 | API admin/accounts | Khớp |
| T7↔GĐ2 | RolePermissionsViewModal không sửa | Khớp |
| T1 | test 403 C3 theo ruling I2 GĐ2 | tự khớp |
| T8 | catalog đánh dấu deprecated admin.tai_khoan.manage vs design Q1 "không sửa catalog chuyển đổi" | Q1 cũng nói đánh dấu deprecated → chỉ đánh dấu, không đổi luật chuyển đổi |
| T9 | e2e HRM/e2e nằm ngoài git, có bản lệch worktree | xử lý khi tới T9 |

Ruling 1: design có 2 bản mục 4.4/4.4b; bản "2 panel col-lg-8/col-lg-4" (user chốt 27/10, khớp plan Global Constraints) thắng bản banner cũ dòng 197-217 — sai thì phải làm lại bố cục T7.
Ruling 2: T6 chuyển BulkPermission*.vue sang pages/admin/employee-roles/components/ và sửa import ở trang cũ còn dùng cho tới T8 (tránh Nuxt vỡ build giữa chừng) — sai thì chỉ thừa 1 sửa import tạm.
Ruling 3: không commit ⇒ thay review-package bằng snapshot tree; reviewer nhận diff giữa 2 snapshot — sai thì chỉ là cách đóng gói diff.

## Tasks
Task 1: complete (snap base0..t1, review clean)
Task 1: minor (deferred): test gửi GET 2 lần (EmployeeRoleHistoryTest:214); thiếu ca NV không có employee_infos.company_id; performerCompanyId vẫn trả công ty chính dù authorize theo C
Task 1→2 note: writer duy nhất Modules/Timesheet/Services/EmployeeService.php:264 EmployeePermissionHistory::create; Entity $fillable cần thêm company_id
Task 2: implementer DONE_WITH_CONCERNS (6 concerns trong report)
Ruling: companies[].role_names trả tên vai trò ở công ty khác chỉ khi C là công ty chính — design 4.1 bắt buộc liệt kê vai trò sẽ mất khi gỡ công ty; chỉ tên, không quyền — sai thì quản trị công ty chính thấy tên vai trò công ty khác
Ruling: cột Người cập nhật bỏ dòng company_id NULL — đúng Q3 design — sai thì dòng cũ không hiện ở danh sách
Task 2 review: Needs fixes — I1 save() không tự mở transaction
Ruling: nhãn lịch sử vai trò "Quyền" → "Vai trò" sửa luôn ở T2 — Global Constraints quy định nhãn "Vai trò" — sai thì đổi lại 1 chuỗi
Ruling: gỡ công ty X ghi thêm 1 dòng lịch sử company_id = X (snapshot vai trò/phân công ở X trước/sau) — review focus #2 "lịch sử ghi đủ", không thì admin X không thấy vai trò bị gỡ — sai thì thừa 1 dòng lịch sử
Task 2: minor (deferred): findWorking chạy ~3 lần/PUT; NULL-flag row ở công ty chính bị xoá khi lưu (ghi deploy note); không lockForUpdate; thiếu test filter kind=main/department/part + 422 part khác phòng
Task 2: fix round 1/5 (5 addressed, 0 open; snap t2..t2f1)
Task 2: complete (snap t1..t2f1, review clean)
Task 2→7 note: PUT gửi key company_ids (kể cả null) cho NV kiêm nhiệm ⇒ 403 — FE phải bỏ hẳn key. Detail trả roles[].permission_ids + permission_meta {id:{kind,subsystem}} để FE tính tổng hợp.
Task 3: implementer DONE_WITH_CONCERNS
Ruling: (thay Ruling 2) BulkPermission*.vue đã bị GĐ2 commit 25824b310 gỡ ở wt-rbac/hrm-client ⇒ Task 6 khôi phục từ 25824b310^ (git show, không checkout) vào pages/admin/employee-roles/components/, không còn importer cũ — sai thì popup lệch bản gop_db hiện hành
Task 3: complete (snap t2f1..t3, review clean)
Task 3: minor (deferred): test 422 khối/chức vụ/chức danh bỏ qua im lặng khi thiếu data C2; test lịch sử chỉ 1 NV đổi; `granted` có thể đếm dư; bulk snapshot ~10 query/NV (hoist companies.name); query NV bị resolve 2 lần + Rule::exists từng id
Task 3→8 note: route cũ timesheet/bulk-permissions/* vẫn còn (BulkPermissionController truyền claim) — gỡ ở T8
User 27/10 (hỏi lại): cho chạy migration 2026_11_02_000001 vào hrm_erp_rbac_rehearsal — đã chạy
Task 4: implementer DONE_WITH_CONCERNS
Ruling: route lịch sử là /admin/accounts/histories/{id} (khuôn URL SystemInfoSection dựng, như products) thay vì /{id}/histories trong plan — skill entity-history thắng plan về hình thức — sai thì đổi 1 route
Task 4: complete (snap t3..t4, review clean)
Ruling: tạo tài khoản không kiểm hồ sơ thuộc phạm vi xem của người tạo — giữ hành vi cũ (design 3.2 "giữ nguyên, không mở rộng"); chặn có thể làm người chỉ có quyền quản lý không tạo được — sai thì người có quyền quản lý tạo được tài khoản cho hồ sơ công ty khác
Ruling: Khoá/Mở khoá vẫn đồng bộ employee_infos.status như màn cũ; đổi Trạng thái qua form Sửa thì không — giữ nguyên hành vi cũ, báo user — sai thì 2 đường cho 2 tác dụng phụ khác nhau
Task 4: minor (deferred): export is_all chưa assert số dòng; findInScope chạy 2 lần/PUT; "Khóa"/"Khoá" 2 cách viết trên timeline; keyword LIKE không escape %/_; rice_setting_location_id thiếu exists
Task 4→5 note: is_all còn dùng ở components/modals/AddEmployeeSingleModal.vue (training TeacherForm/ExamierForm) — giữ API cũ
Task 5: implementer DONE_WITH_CONCERNS; controller khởi động lại 8011 kèm DB_*_TPE (scratchpad/start-8011.sh)
Task 5 review: Approved; Important duy nhất (nút máy ảnh) — user chốt 27/10 ảnh chỉ đọc ⇒ đóng. User chốt giữ sửa V2BaseSmartFilterPanel. Ghi design §9.
Task 5: complete (snap t4..t5, review clean sau quyết định user)
Task 5: minor (deferred): form lấy canManage từ store còn list lấy BE can_manage; sửa tài khoản gửi rice_ssn gợi ý ⇒ tự cấp mã check-in cơm (như form cũ — báo user); "⋮ Lịch sử" hiện inline vì V2BaseRowActions maxInline=3; redirect bỏ query string; cần đo lại danh sách trên 8011 ở T9
Task 6: implementer DONE_WITH_CONCERNS
Task 6 review: Needs fixes — I1 nhãn "Tất cả bộ phận" sai với phạm vi theo bộ phận
Ruling: dòng phân công không có bộ phận hiện "Chưa chọn bộ phận" (xám), có part_ids nhưng không còn tồn tại hiện "Bộ phận đã xoá"; BE effective-permissions trả thêm part_ids — mockup chỉ quyết hình thức, nhãn không được khẳng định quyền nhân viên không có — sai thì đổi lại 1 chuỗi
Task 6: minor (deferred): Lịch sử không vào ⋮ (V2BaseRowActions maxInline=3, như Màn 1); "Loại" chữ thường vì BE chưa trả kind_color; export bulk dùng blob+<a download> (lỗi Safari đã biết)
Task 6: fix round 1/5 (4 addressed, 0 open; snap t6..t6f1)
Task 6: complete (snap t5..t6f1, review clean)
Task 6: minor (deferred): đường Áp dụng bulk + lịch sử có dòng thật chưa kiểm UI (T9); companyEmployees phụ thuộc lần tải đầu của Filter
Task 7: implementer DONE_WITH_CONCERNS (concern 1: lưu với 'tất cả phòng ban' xoá dòng phân công từng phòng ở C — NV 13 có 22 dòng)
Task 7 review: Needs fixes — I1 lưu khi bật "tất cả phòng ban" xoá dòng phân công ở C; ≥6 module (Finance prepick/due-config, Assign customer…) đọc thẳng bảng ⇒ mất quyền âm thầm
Ruling: all_department=true ⇒ KHÔNG đụng dòng department_id NOT NULL, chỉ ghi cờ (công ty chính: company_employees; kiêm nhiệm: dòng NULL); all=false ⇒ xoá cả 2 nguồn cờ rồi ghi lại dòng theo payload; allDepartmentAt đọc đúng 2 nguồn như PermissionHelper::employeeManagesAllDepartmentsIn; FE khoá bảng khi bật cờ + ghi chú "các dòng phân công cũ vẫn được giữ" — design 4.4 "giữ nguyên, đang có hiệu lực" — sai thì còn dòng cũ khi bật cờ (vô hại với PermissionHelper)
Ruling: badge Công ty chính/Kiêm nhiệm dùng variant có sẵn (brand / status-ok) — skill cho phép variant với nhãn cố định — sai thì đổi 1 prop
Task 7: minor (deferred): tổng hợp đếm cả vai trò khoá (khớp BE summary; xem lại ở final review); rp-summary CSS chép từ permissions.vue; confirm gỡ công ty chưa liệt kê tên phòng ban; tải lỗi khác 403/404 để trang trắng
Task 7: fix round 1/5 (2 addressed, 0 open; snap t7..t7f1)
Task 7: complete (snap t6f1..t7f1, review clean)
Task 7: minor (deferred): khi bật cờ "tất cả" payload vẫn gửi dòng cũ ⇒ dòng trỏ phòng ban đã khoá có thể 422 trên dòng chỉ đọc
Task 8: implementer DONE_WITH_CONCERNS
Ruling: admin.tai_khoan.manage chỉ đánh dấu ngừng dùng bằng comment trong catalog, không đặt deprecated_at — quyền vẫn gác ERP employee.searchData (popup chọn NV phiếu thu/chi), deprecated thật làm 403 popup; Q1 cấm đổi luật chuyển đổi — sai thì quyền còn hiện ở màn phân quyền tới khi dọn popup ERP
Ruling: báo cáo "có quyền ERP mà thiếu Quản lý tài khoản nhân viên" làm bằng SQL chỉ đọc (rehearsal: 1 người — NV 258 TPE) thay vì sửa rbac:convert — Q1 cấm đổi chuyển đổi GĐ1 — sai thì admin phải chạy SQL tay lúc go-live
Task 8 review: Needs fixes — I1/I2 (catalog deprecated, báo cáo chuyển đổi) đã có Ruling ở trên ⇒ đưa user quyết cuối phiên, không vào vòng sửa; I3 khối gate menu ERP lặp 3 layout
Task 8: minor (deferred): widget trang chủ ERP gate can('Phân quyền') nhưng link sang màn gate 5 quyền khác + mất ?status=2; mục "Vai trò nhân viên" ở ERP không gate (như mục "Vai trò" GĐ2); dead code EmployeeInfosController@basic, nhánh $byWorkingCompany=false, RoleService::list; tên test BulkRoleGrantTest lệch
Task 8: fix round 1/5 (2 addressed, 0 open; snap t8..t8f1)
Task 8: complete (snap t7f1..t8f1, 2 parked — catalog deprecated + báo cáo chuyển đổi: xem Ruling, chờ user)
Task 9: spec e2e viết xong (HRM/e2e/tests/admin/admin-accounts.spec.ts 9 ca, admin-employee-roles.spec.ts 12 ca, gd2b-fixture.ts), --list 25 OK, chưa chạy (chỉ chạy khi user yêu cầu)
Ruling: review spec e2e gộp vào final review (file ngoài git, không vào snapshot) — sai thì spec có selector sai, lộ ra ở lần chạy đầu
Task 9: complete (spec chưa chạy)
Final review: With fixes — I1 route ghi cũ human/employee còn companies()->sync (bỏ qua mọi luật Màn 2; rehearsal có 12 dòng employee_has_roles mồ côi); I2 company_ids.* exists status=1 làm 422 NV còn làm ở công ty ngưng; I3 e2e header 'Tên'; I4 e2e click label 0×0
Ruling: gỡ hẳn 4 route ghi human/employee (POST/PUT/updateStatus/DELETE) + store action chết — design 3.5 "gỡ hẳn sau khi rà hết nơi gọi", rà đã sạch — sai thì client ngoài (app mobile) gọi route cũ nhận 404
Ruling: minor phải sửa trước prod gộp vào đợt sửa cuối: rice_setting_location_id exists; tổng hợp quyền hiệu lực bỏ vai trò khoá (FE+BE, theo đúng PermissionChecker); xoá writer lịch sử chết Timesheet EmployeeService; kiểm UI bulk Áp dụng + đo lại danh sách Màn 1 trên 8011
Final fix wave: complete (snap final0..final2, re-review: 7/7 addressed, 0 new)
