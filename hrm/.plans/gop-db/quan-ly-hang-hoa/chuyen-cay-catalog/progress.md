# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/chuyen-cay-catalog/plan.md

Ruling: ledger đặt ở .plans (không trong git) thay vì <repo>/.superpowers — plan nằm ngoài 2 repo, script sdd-workspace không dùng được — cost if wrong: không có
Ruling: bỏ bước xoá role_has_permissions 1616-1619 — user chốt 04/10 "Admin có thêm quyền không sao" — cost: Super admin local có thêm 4 quyền công nợ
Pre-flight: T1→T2 (entity names/relations businessScope, jobGroup, chapter) khớp; T2→T5/T6 (field resource *_name/*_locked, getAll keys) khớp; T2 routes slug chapters/job-groups/job-clusters ↔ T5 TREE_SOURCES khớp
Task 0: complete (api commit e3f90f7d4, migrate hrm_erp OK: scope_id NULL-able, internal_business_scope_id+FK, chapters=65)
Ruling: Request chỉ giữ message nghiệp vụ (name.unique theo cha), bỏ name.max/required tự viết — HRM/CLAUDE.md cấm khai lại message rule phổ biến (lang file) dù khuôn Xe có khai — cost: câu lỗi max ra 'Vui lòng nhập tối đa 64 ký tự.' thay vì 'Nhập tối đa 64 ký tự'
Ruling: điều kiện xoá/khoá (D6) theo nền BaseCatalogModel, không hỏi riêng — user đã duyệt phạm vi kèm design.md D6 — cost: nếu user muốn khác thì sửa childrenCount/activeChildrenCount
Task 1: complete (api commit d4bea2cae, tests: phpunit BusinessCatalogTreeTest → OK 3/3, 13 assertions; RED trước đó: Class not found)
Task 2: Ruling: quyền 1657-1662 → 1670-1675 — DB local + nhánh gop_db-bao-cao-nhu-cau-dich-vu đã dùng 1660/1661 (seed vào DB dùng chung, git không báo xung đột) — cost: nếu nhánh khác cũng nhảy tới 167x thì trùng lại; kiểm uniq -d + DB trước khi seed
Task 2: Ruling: KHÔNG chạy cả PermissionsTableSeeder — seeder xoá mọi quyền api rồi tạo lại theo file nhánh này ⇒ sẽ xoá 1660/1661 của nhánh báo cáo dịch vụ khỏi DB dùng chung; thay bằng INSERT đúng 6 dòng + gán role 18 company 1 + cache:clear — cost: DB local lệch seeder ở chỗ khác (không đổi gì ngoài 6 dòng)
Task 2: Ruling: route:list hỏng sẵn (RequestUpdateTimeSheetController constructor gọi isCurrentEmployeeHasPermission khi chưa đăng nhập) — kiểm route bằng router trong tinker: 27 route, gate đúng — cost: không
Task 2: complete (api commit fcd25bf1a, tests: phpunit BusinessCatalogTreeTest → OK 9/9 24 assertions; ProductClassificationCatalogTest → OK 11/11; RED trước: 6 Error class not found)
Task 3: complete (không commit code — chỉ kiểm; 15/15 ca đúng mong đợi, 2 ca 'SAI' ban đầu là do thứ tự dọn của script, đã điều tra)
Final: minor (deferred): nền BaseCatalogController — sửa bản ghi khoá trả 400 thay vì 423; mở khoá bản ghi đang hoạt động báo nhầm 'cha đang bị khoá' (dùng chung 17+ màn)
Task 4: complete (api commit 6c993582e, tests: phpunit BusinessCatalogTreeTest → OK 10/10 29 assertions; RED trước: undefined method isUsed(); smoke API danh sách lĩnh vực 200, is_can_delete=false do Nhóm ngành có sẵn)
Task 5: Ruling: icon menu ri-book-2-line thay ri-node-tree — 2 bản remixicon lệch codepoint (memory), icon đã dùng ở menu khác chắc chắn hiện — cost: chỉ là icon
Task 5: complete (client commit 341c2b20b; không có test riêng — kiểm DOM menu ở Task 7)
Task 6: Ruling: thêm internal_business_scope_locked (Mục, Tiểu mục) + chapter_locked (Tiểu mục) vào Resource — soát popup thấy Xem bản ghi có tổ tiên khoá sẽ trống ô; plan chưa có — cost: 3 field thừa nếu không dùng
Task 6: complete (client d632db255, api 4d8b9b68e; sinh 3 màn từ khuôn vehicle-brands có assert số lần thay; grep HTML thô: chỉ còn <button class=v2-cell-link> có sẵn trong khuôn)
Task 7: complete (Playwright MCP, số đo ghi ở plan.md "Nhật ký kiểm")
Task 8: complete (spec e2e business-catalog-tree.api.spec.ts 6 ca, --list OK 7 tests in 2 files; KHÔNG chạy theo quy tắc user)
Task 9: complete (SO-CHOT 2d → code xong; design §35h H2 trỏ thư mục; gop-db/STATUS.md thêm mục Đang làm)
Final: fixed N+1 is_can_lock (Chương/Mục list + export) — test_danh_sach_chuong_khong_n_cong_1_khi_tinh_is_can_lock RED(6 query)→GREEN(0), suite BusinessCatalogTree 11/11 + ProductClassification 11/11 (2cf1f4a0e); lộ thêm: index() class đè index() trait SelectsChildrenFlag → dùng bí danh
Final: fixed m5 unique Chương khi thiếu Lĩnh vực so với chương cũ (re-graded: lộ data ẩn, trái D3) — test_chuong_thieu_linh_vuc_khong_so_trung_voi_chuong_cu RED→GREEN, suite 12/12 (f0779d86e)
Final: fixed m1 ô Trạng thái popup Sửa Chương/Mục không khoá khi is_can_lock=false (re-graded: user điền xong mới bị 400; màn cây khác đều khoá) — Playwright RED statusSelectDisabled=false → GREEN true; chiều ngược (chương không con) vẫn mở (b603ed039)
Final: fixed m3 ô Lĩnh vực/Chương có * mà không báo lỗi (re-graded: trái yêu cầu user "báo lỗi mọi ô cùng lúc") — Playwright RED Mục: Lĩnh vực ''; Tiểu mục: Lĩnh vực+Chương '' → GREEN cả 4/5 ô 'Bắt buộc phải nhập'; lưu hợp lệ vẫn 200, 0 lỗi (b603ed039)
Final: minor (deferred): m2 option cha đã khoá chèn cho 1 bản ghi còn dính ở lần Tạo mới sau (khuôn Xe cũng vậy) — chọn nó BE trả 422 rõ ràng
Final: minor (deferred): m4 nền BaseCatalogController PUT thiếu status bị hiểu là khoá ((int)null===0) — lớp dùng chung, FE luôn gửi status
Final: minor (deferred): m6 comment 'Loại xe' trong ExportColumnRegistry nằm lệch lên trên khối chapters
Final: minor (deferred): m7 ô lọc Chương/Mục chưa chọn cha có thể hiện 2 tên trùng (tên chỉ unique theo cha)
Final: minor (deferred): m8 e2e chưa chốt job-groups/getAll loại mục của chương cũ + đường PUT lĩnh vực status=2 khi còn chương
Final: minor (deferred): m9 danh sách Lĩnh vực thêm tối đa 4 query/dòng (8 dòng, không đáng kể)
Final: review subagent opus — 0 Critical, 1 Important + 9 Minor; sửa 4 (I1 + m1/m3/m5 re-graded), 6 minor deferred. Ledger GIỮ lại ở .plans (không phải workspace git-ignored).
E2E: business-catalog-tree.api.spec.ts 6/6 passed (04/10, user yêu cầu chạy); dữ liệu E2ECAT + lĩnh vực tạm dọn sạch
