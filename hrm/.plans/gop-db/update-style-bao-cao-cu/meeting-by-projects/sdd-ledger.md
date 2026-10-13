# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/update-style-bao-cao-cu/meeting-by-projects/plan.md

Spec: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/docs/superpowers/specs/gop-db/2026-10-04-update-style-bao-cao-meeting-theo-du-an-design.md
Worktrees: wt-update-style-mbp/{hrm-api,hrm-client} · branch gop_db-update-style-meeting-by-projects · base api 85a1c59d7 / client a6ad678d0
Servers: api 8018 (php@7.4 artisan serve) · client 3018 (nuxt, node 12)

## Pre-flight scan
| Pair / Task | Produces → Consumes | Finding |
|---|---|---|
| T2 ↔ T3 | MeetingParticipantCounter (min) → T3 hoàn thiện key() + listFor() | khớp |
| T2 ↔ T4 | route filter-options tối thiểu (can_change_company) → T4 thay bản đủ | khớp, T4 phải xoá bản tối thiểu |
| T2/T3 ↔ T5 | index($r,true), meetingRows(), participantRows() → export/print | khớp |
| T2 ↔ T6 | PERM_ALL/PERM_COMPANY const → canView | khớp |
| T2–T5 ↔ T7/T8 | route -v2 + shape summary/groups/meta, item-list, participant-list → FE | khớp (FE dùng khoá by_status '2','3', by_mode '1','2') |
| T7 ↔ T8 | emit drill / drill-people / open-meeting / open-minutes → index handlers | khớp |
| T2–T8 ↔ T9 | -v2 → đổi route chính, tests URL, api.js | khớp |
| T1 | worktree | self-consistent |
| T2 | tests dùng /filter-options (route tối thiểu ở chính task) | self-consistent |
| T3 | test dùng pq? — test không gửi pq; ok | self-consistent |
| T4 | test project_creator_id skip | self-consistent |
| T5 | test .xlsx; tên file .xlsx | self-consistent |
| T6 | mốc assertFalse có thể sai actor → note đổi actor | self-consistent |
| T7/T8 | không có test tự động (Playwright MCP đo DOM theo CLAUDE.md) | chấp nhận theo quy tắc dự án |
| T10 | e2e chỉ viết, không chạy | khớp memory khong-tu-chay-e2e |

Ruling: Plan tạo class mới MeetingByProjectsReportService và xoá MeetingByProjectsService ở T9, thay vì "viết lại" file cũ như spec §4 — giữ màn cũ chạy được tới khi FE chuyển xong — nếu sai: chỉ là tên file, đổi tên rẻ.
Ruling: Tìm người trong participant-list dùng tham số `pq` (spec §4 ghi `q`) vì `q` đã lọc meeting trong meetingQuery — nếu sai: FE gửi sai khoá → ô tìm người không lọc; e2e/Playwright bắt được.
Ruling: Task 1 (worktree) controller tự làm, không dispatch subagent — chỉ là dựng môi trường, không code — nếu sai: không ảnh hưởng code.

Task 1: complete (worktree + vendor/node_modules copy, autoload trỏ worktree, .env client 3018/8018)
Task 2: dispatched (BASE 85a1c59d7, implementer sonnet)
Ruling: Interface `meetingRows(Request $r, array $extra = [])` trong brief T2 không khớp code của chính brief (không có $extra) — chốt KHÔNG có $extra, không task nào sau dùng — nếu sai: task sau thêm tham số, rẻ.
Task 2: ⚠️ resolved — meetings không có deleted_at (hard delete, không rác); quyền tra theo tên chạy (test xanh).
Task 2: minor (deferred): comment "print-list-data contract" bị tách khỏi route potential-customer-tracking do chèn route mới (api.php ~92-96)
Task 2: minor (deferred): join ppm có thể nhân dòng nếu 1 meeting gắn 2 dự án/trùng cặp (local 0 dòng trùng) — duration/by_status sẽ lệch
Task 2: minor (deferred): q không escape %/_ 
Task 2: minor (deferred): orderBy thiếu tiebreak p.id → phân trang có thể nhảy khi created_at trùng
Task 2: minor (deferred): thiếu test status 1 bị loại, các period week/month/last_year, nhánh 1061 OR created_by
Task 2: complete (commits 85a1c59d7..c22fc965c, review clean)
Task 3: dispatched (BASE c22fc965c, sonnet)
Task 3: minor (deferred): người KH gộp qua nhiều dự án lấy unit của meeting đầu tiên (thứ tự không chắc)
Task 3: minor (deferred): usort so tên byte-wise, tiếng Việt sắp lệch → dùng collator
Task 3: minor (deferred): dòng KH có SĐT không tên / dòng trống hiện tên rỗng trong popup — FE phải xử lý
Task 3: minor (deferred): thiếu test pq, meeting_count phía công ty, phân trang item-list
Task 3: complete (commits c22fc965c..15ea5d03b, review clean)
Ruling: Ô Giai đoạn dự án ở FE vẫn dùng store optionsSelect/fetchProjectPhases (giữ giai đoạn đã khoá đang được lọc); filter-options vẫn trả phases status=1 theo plan — nếu sai: 2 nguồn danh mục, FE chọn 1, không sai số liệu.
Task 4: dispatched (BASE 15ea5d03b, sonnet)
Task 4: minor (deferred): test filter-options chưa kiểm nhãn creators, danh sách companies 1 công ty khi không quyền (can_change_company=false đã có ở test T2)
Task 4: complete (commits 15ea5d03b..5cb157f0f, review clean)
Task 5: dispatched (BASE 5cb157f0f, sonnet)
Task 5: review — Important: SĐT export bị DefaultValueBinder ép số; ExportPrintTest mỏng (thiếu lọc loại trừ, vượt trần, đọc nội dung xlsx). Logo 0 drawing = do môi trường (cùng đường nhúng với template).
Task 5: fix round 1/5 dispatched (resume implementer, FIX_BASE 2161e798a)
Task 5: fix round 1/5 (3 addressed, 0 open; commits 2161e798a..a2af7e8a5)
Task 5: minor (deferred): logo theo URL công ty thật chưa kiểm (môi trường test không tải được) — kiểm tay khi chạy FE
Task 5: minor (deferred): FE phải gửi scope_label cho tiêu đề phụ Excel/in popup
Task 5: complete (commits 5cb157f0f..a2af7e8a5, review clean)
Task 6: dispatched (BASE a2af7e8a5, sonnet)
Ruling: canView nới theo đúng chữ quyết định #10 (mọi meeting gắn dự án TKT / dự án thuộc công ty hiện tại), KHÔNG lọc trạng thái dự án/meeting như báo cáo — user duyệt đúng câu chữ đó; chỉ là quyền XEM — nếu sai: người có 1060/1061 xem được meeting nháp/hủy gắn dự án; thêm 2 điều kiện where là xong.
Task 6: minor (deferred): thiếu test meeting KHÔNG gắn dự án vẫn bị ẩn với 1060/1061
Task 6: complete (commits a2af7e8a5..63d13fc31, review clean)
Note: FE briefs/reports nằm ở workspace hrm-client/.superpowers/sdd/plan/ (script chọn theo repo); ledger vẫn ở đây.
Task 7: dispatched (client BASE a6ad678d0, opus) — login E2E Assign (1060), dữ liệu 57 meeting 2026
Task 7: implementer DONE dabc141a2 — đo DOM đạt; note: tài khoản E2E_NO_PERM trong e2e/.env không có trong hrm_erp (dùng e2e_cmd_noperm@test.local, 0 dự án); level select 22px thay 18px (khớp mockup)
Task 7: review dispatched (opus)
Task 7: minor (deferred): .rsum-tb__cnt tabular-nums bị bỏ ở ô CountList
Task 7: minor (deferred): handleReset không gọi lại loadProjectPhases; khối trạng thái rỗng khi mọi số = 0 vẫn vẽ header
Task 7: complete (client commits a6ad678d0..dabc141a2, review clean)
Ruling: Popup theo loại: FE gửi meeting_type_id (không phải type_id); BE coi meeting_type_id=0 / mode_id=0 là NULL (whereNull) — để "Chưa phân loại"/"Chưa xác định" drill khớp số — làm trong Task 8 (sửa BE nhỏ + test) — nếu sai: popup lệch số ô bấm, e2e bắt được.
Ruling: Thêm nhóm hình thức "Chưa xác định" (mode_id NULL): by_mode có khoá '0'; ô Hình thức dòng dự án/TỔNG và khối Trạng thái & hình thức hiện "n Chưa xác định" khi > 0 — giữ bất biến Trực tiếp + Online + Chưa xác định = Số meeting (local 10/57 meeting thiếu hình thức) — điểm UI tự chốt theo khuôn (skill §3 unknown→0) — nếu sai: bỏ 1 ô, rẻ; cần báo user ở tổng kết.
Task 8: dispatched (client BASE dabc141a2, api BASE 63d13fc31, opus) — kèm 2 ruling Chưa xác định/0=NULL
Task 8: implementer DONE — api fd95b1494, client c2f722523
Ruling: Cột Hình thức nới 180→270px (bảng 2504→2594px) để ô "n Trực tiếp · n Online · n Chưa xác định" không bị cắt/bấm không được — lệch mockup, do thêm nhóm Chưa xác định — nếu sai: chỉnh độ rộng.
Ruling: Ô Loại meeting dòng dự án/TỔNG giữ cắt "…" + tooltip đủ (mockup mục c); số bị cắt vẫn xem được qua popup "Số meeting" có ô lọc Loại — nếu sai: user muốn xuống dòng, đổi 1 rule CSS.
Ruling: BE coi 0 là NULL OR = 0 (khớp cả giá trị lưu 0) — dữ liệu 0 không hợp lệ cũng là "chưa xác định" — nếu sai: không ảnh hưởng (không id 0 hợp lệ).
Task 8: review dispatched
Task 8: minor (deferred): Excel link với mode_id=0/meeting_type_id=0 chưa đo (code giữ 0) — đưa vào e2e
Task 8: minor (deferred): cột Hình thức trong popup 100px có thể chật với "Chưa xác định"
Task 8: minor (deferred): q chứa %/_ — FE lọc literal, BE LIKE wildcard
Task 8: complete (api 63d13fc31..fd95b1494, client dabc141a2..c2f722523, review clean)
Task 9: dispatched (api BASE fd95b1494, client BASE c2f722523, sonnet)
Task 9: implementer DONE_WITH_CONCERNS api 73cb25e6c client 7e02f5b74; route:list crash có sẵn trên gop_db (đã kiểm worktree cskh) — 8 route mới đếm trong api.php
Task 9: minor (deferred): import ChartDataResource / MeetingProject trong ReportController có thể đã thừa
Task 9: NGOÀI LUỒNG (có sẵn): meeting-by-employees/components/MeetingsByStatusModal.vue:140 gọi route meeting-by-employees/meetings-by-status không tồn tại — note cho user, không vá
Task 9: complete (api fd95b1494..73cb25e6c, client c2f722523..7e02f5b74, review clean)
Task 10: dispatched Step 1-2 (viết spec e2e, không chạy; e2e không thuộc git) — Step 3-5 controller
Task 10: review — Important: ca side filter rỗng (fixture không seed meeting_employees); cổng mặc định 8017/3017 sai nhánh. Minor 3-8 gửi kèm.
Task 10: fix round 1/5 dispatched (resume implementer)
Task 10: fix round 1/5 (8 addressed, 0 open)
Task 10: minor (deferred): fixture dự án chép các cột customer_* phụ (tax/phone/contact) từ dự án thật — không ảnh hưởng số
Task 10: complete (Step 1-2; e2e không thuộc git; CHƯA chạy theo quy tắc)
Final review: With fixes — I1 meeting gắn ≥2 dự án làm lệch tổng hợp/item-list; I2 thứ tự thiếu p.id; I3 canView không khớp phạm vi báo cáo (created_by/NVKD) → CẦN USER QUYẾT (quyền), không tự sửa.
Ruling: Meeting gắn nhiều dự án — cây hiện meeting dưới MỖI dự án (totals từng dự án tính nó), nhưng tổng hợp/TỔNG và popup không scope dự án đếm 1 lần (dedupe theo id, kèm project_count) — giữ "4 nơi 1 số" ở cấp báo cáo — nếu sai: Σ dòng dự án có thể > TỔNG khi có meeting gắn nhiều dự án (ghi chú cho user).
Ruling: mode_id ngoài {1,2} xếp vào nhóm 0 "Chưa xác định" cả ở totals lẫn bộ lọc — giữ bất biến tổng hình thức = số meeting — nếu sai: không ảnh hưởng dữ liệu hiện có.
Final fix wave: dispatched (BE, FIX_BASE api 73cb25e6c)
Final fix: re-review all addressed (api 73cb25e6c..e5a334044, 23 + 68 tests green)
