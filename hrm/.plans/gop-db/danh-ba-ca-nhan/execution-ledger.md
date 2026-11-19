# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-claude-config/hrm/.plans/gop-db/danh-ba-ca-nhan/plan.md

Spec: design.md cùng thư mục. Repo: hrm-api (gop_db), hrm-client (gop_db), TPE_APP (develop). KHÔNG commit (user). Review package = diff giữa 2 snapshot tree (snap.sh / pkg.sh trong workspace này), không dùng commit range.
Baseline trees 07/11 19:36: hrm-api 13687054 · hrm-client 165c7b0c · TPE_APP 1f04812d

## Pre-flight scan
| Cặp / task | Produces → consumes | Kết quả |
|---|---|---|
| T1 → T2/T3/T4 | PersonalContact, PhoneNormalizer::normalize, PersonalTodo::contact(), cột contact_id | khớp |
| T2 ↔ T3 | cùng PersonalContactService/Controller + route; T3 route `company-lookup` phải TRƯỚC `/{id}` | khớp (T3 ghi rõ) |
| T2 → T4 | resolveOrCreate(int,array), touch(int) | khớp |
| T2/T4 → T5/T6 | API `/assign/my-todo/contacts…`, payload `contact_id`/`contact`, item `contact` | khớp |
| T5 ↔ T6 | ContactFormFields, avatarColor, TodoFormModal prop `presetContact` | HỞ: T6 dùng `presetContact` nhưng không task nào thêm prop, T6 không liệt kê TodoFormModal → Ruling R1 |
| T2/T4 → T7 | `GET /contacts` {data, recent, total} → ContactPage{items, recent, total}; show {data+todos{upcoming,done}} → ContactDetail | khớp (map tên) |
| T7 → T8 → T9 | ContactApiService, PersonalContact, ContactDraft, ContactAvatar; form param `presetContact` | HỞ: T9 dùng `presetContact` của form app, không task nào thêm → Ruling R2 |
| T1 tự thân | test schema ↔ migration | khớp |
| T2 tự thân | test `test_trung_so_dang_84_dung_lai` ↔ POST trả 200 + meta.existed | khớp |
| T3 tự thân | phạm vi KH "như ChooseErpCustomerModal phone_exact_bypass" nhưng popup đó chỉ khớp customers.mobile, không có customer_contacts | ghi chú: điều kiện phạm vi KH lấy từ CustomerService::index, phần customer_contacts tự join thêm — đúng spec §5.3 |
| T4 tự thân | test leader schedule ↔ không sửa LeaderSchedule code | khớp (chỉ cần không thêm) |
| T5/T6 | yêu cầu Playwright MCP + spec e2e không chạy | khớp Global Constraints |
| T8/T9 | "máy ảo" verify | Ruling R4 |
| Mọi task | bước "Commit" | Ruling R3 |

## Rulings
- Ruling R1: T5 (đang sửa TodoFormModal) thêm luôn prop `presetContact` (Object|null, đổ sẵn liên hệ khi mở form Tạo) — T6 chỉ dùng — chi phí nếu sai: T6 phải sửa thêm TodoFormModal, nhỏ.
- Ruling R2: T8 (đang sửa personal_todo_form_page.dart) thêm tham số `presetContact` (PersonalContact?) cho form — T9 chỉ dùng — chi phí nếu sai: T9 sửa thêm 1 file.
- Ruling R3: bỏ mọi bước Commit; task xong để nguyên working tree; review dùng diff snapshot tree — user dặn "không commit, user tự báo" — chi phí nếu sai: không có, user commit sau.
- Ruling R4: T8/T9 kiểm máy ảo qua Mobile MCP nếu máy ảo + build sẵn sàng; nếu không, implementer ghi rõ "chưa kiểm máy ảo" thành concern, KHÔNG coi là xong phần kiểm trực quan — controller báo user — chi phí nếu sai: lỗi giao diện app lọt tới lúc user kiểm.
- Ruling R5: TPE_APP đang có 29 file STAGED của Lịch lãnh đạo — implementer KHÔNG `git add`/unstage/stash/checkout; chỉ sửa file — user chọn "làm chồng lên" — chi phí nếu sai: thay đổi trộn vào index của việc khác (đã tránh bằng cách không chạm index).

## Progress
Task 1: dispatched implementer (sonnet) agent=afd858f802fe73175 base tree hrm-api 13687054
Task 1: implementer DONE, head tree 3a61ceaac707b1395ba611fa23e7a57c108dffd1; migrations verified in db_gop_6_11 batch 468/469
Task 1: review → spec ❌ 1 Important (+840… → 00… double zero). ⚠️ migrations-run resolved by controller (verified db_gop_6_11 batch 468/469). ⚠️ BaseModel boot hooks → carried to Task 2 dispatch.
Task 1: minor (deferred): phone_normalized string(30) vs phone string(50), normalizer không chặn độ dài >15 số → insert lỗi; validate độ dài ở Request Task 2.
Task 1: minor (deferred): test thiếu biên 84+10 số / 13 số / chuỗi rất dài.
Task 1: fix round 1 implementer done (tree 0fb0f4d4).
NOTE: 1 phiên Claude khác đang sửa RBAC song song trong hrm-api (app/Http/Controllers/Api/V1/Admin/RoleController.php, app/Services/Admin/RoleManagementService.php, routes/api.php, tests/Feature/Rbac/*) — KHÔNG phải của plan này; mọi review package lọc pathspec Modules/Assign; implementer không được đụng các file đó.
Task 1: fix round 1/5 (1 addressed, 0 open — +840 double zero; trees 3a61ceaa..0fb0f4d4)
Task 1: minor (deferred): 84 + 0 ở 11 số (84012345678) ra 9 số — input dị dạng.
Task 1: complete (trees 13687054..0fb0f4d4, review clean)
Ruling R6: Task 2 Request chặn SĐT có phone_normalized null hoặc > 15 chữ số → 422 `phone` (gom minor Task 1 về độ dài vào chỗ validate tự nhiên) — chi phí nếu sai: số nước ngoài dài hơn 15 bị từ chối (E.164 tối đa 15, gần như không xảy ra).
Task 2: dispatched implementer (sonnet), base tree hrm-api 0fb0f4d4
Task 2: implementer DONE, head tree c5054fd6f14f6f07ff5e3d61a85c3467b9a6c3e6. Concern: LeaderSchedule suite 12 fail (permission-gate). Controller check: LeaderScheduleOrderApiTest alone 5/6 fail — expected leaders [25,24], got +8 real holders (825,13,1084,…) from db_gop_6_11 data / parallel RBAC work; Task 2 diff adds only new files + 5 routes, không đụng PermissionLookup. Ruling R7: coi là lỗi môi trường có sẵn, không chặn Task 2 — CHƯA kiểm trên cây sạch (không stash được) — chi phí nếu sai: một lỗi hồi quy quyền lịch lãnh đạo lọt; final review sẽ kiểm lại.
Task 2: review ✅ Approved. ⚠️ resolved by controller (normalizer digits-only verified T1; PersonalTodo casts due_date date / completed_at datetime verified; auth()->id() same as MyTodoController).
Task 2: minor (deferred): store() existed=false khi thua race; Update request kế thừa rule source vô dụng; update() ghi null address/note khi thiếu khoá; test next_due có $c2 thừa.
Task 2: complete (trees 0fb0f4d4..head, review clean)
Ruling R8: phạm vi tra KH công ty = điều kiện LUÔN áp của CustomerService::index (vd is_customer, chưa xoá) + status=1 (Hoạt động, như popup ChooseErpCustomerModal) + khớp đúng toàn bộ số ⇒ bỏ qua lớp quyền xem (như phone_exact_bypass); áp cho cả KH cá nhân lẫn tổ chức — chi phí nếu sai: KH bị khoá không tra được / lệch nhẹ với popup.
Task 3: dispatched implementer (sonnet), base tree hrm-api c5054fd6f14f6f07ff5e3d61a85c3467b9a6c3e6
Ruling R9: tra KH công ty khớp cả 3 dạng lưu của cùng số (0xxx / 84xxx / +84xxx) — DB có ~143 dòng lưu dạng 84/+84 — chi phí nếu sai: query thêm 2 nhánh OR LIKE, chậm nhẹ.
Task 3: implementer DONE + addendum R9, head tree 6a01d85fc41938d8356b4a31a7b1d9d6976c4ca0.
Task 3: minor (deferred): số lưu có dấu chấm/gạch (customers 79, contacts 32 dòng) chưa khớp — có thể thêm REPLACE '.', '-' trong SQL.
Task 3: review ✅ Approved. ⚠️ resolved: tests reported 10/10 + 9/9; stored formats counted in DB; status=1 = popup.
Task 3: minor (deferred): KH + người liên hệ cùng số ra 2 dòng (FE nên chịu được cặp cùng customer_id); >5 KH thì không thấy dòng liên hệ; thiếu test biên dạng 84 lưu.
Task 3: complete (trees c5054fd6..6a01d85fc41938d8356b4a31a7b1d9d6976c4ca0, review clean)
Task 4: dispatched implementer (sonnet), base tree hrm-api 6a01d85fc41938d8356b4a31a7b1d9d6976c4ca0
Task 4: implementer DONE, head tree 5d6e62a73a243b036fc12b6f8d8cb3264f346925; LeaderSchedule 12 fail before/after (counts only)
Task 4: review ✅ Approved. ⚠️ resolved: route `/todos/{id}` → param `id` đúng; LeaderSchedule 12 fail trước/sau (R7).
Task 4: minor (deferred): race trùng SĐT trong transaction REPEATABLE READ → 400 thay vì dùng lại (hiếm); contact: [] tính là có liên hệ; thêm 1 query/update; touch mỗi lần update.
Task 4: complete (review clean)
Task 5: dispatched implementer (sonnet), base tree hrm-client 37d745b9ab83e710f8b9e36c9159e07c9d85623b (servers: nuxt :3000 + php -S :8000 from main checkouts)
NOTE: hrm-client có thay đổi của phiên khác (pages/admin/roles/_id/permissions.vue, utils/import-helper.js) — review package web lọc pathspec pages/assign/my-todo + components liên quan.
Task 5: implementer DONE, head tree 5de4d8c22ce786b4e6e28a203c6fce1e199418d2. Playwright verified (form-group 6→6, link 10px dưới Tiêu đề, popup trong 1280, lookup 0 req @7 số / 1 @10 số, tạo mới + đóng form = 0 POST /contacts).
Task 5: test data local: contact 164, todo 465 (DB dev local, được phép).
Task 5: review ❌ Changes required: I1 gate 9 số chưa chuẩn hoá +84 ở FE; I2 e2e đếm request trước debounce (flaky); I3 e2e thiếu payload/Escape/cleanup.
Task 5: Ruling R10: bỏ yêu cầu ca e2e "không quyền xem KH → ẩn tra cứu" trong I3 — spec §8 chốt tra KH theo đúng SĐT KHÔNG xét quyền (tiền lệ phone_exact_bypass) — chi phí nếu sai: thiếu 1 ca test quyền nếu user đổi chủ trương.
Task 5: ⚠️ resolved: Escape chỉ đóng picker + shape API đã đo Playwright trong report.
Task 5: minor (deferred): lỗi API hiện như "trống"; q='' khi mở lại gọi loadContacts 2 lần; lỗi 422 contact.* không xoá khi chọn người khác; ContactCard role=button lồng nút; ô tìm thiếu aria-label; spec đếm .form-group=6 dễ gãy; mở lại picker làm mất liên hệ mới chưa lưu.
Task 5: fix round 1 dispatched, FIX_BASE tree 5de4d8c22ce786b4e6e28a203c6fce1e199418d2
Ruling R11: chấp nhận '+84 9123456' (=849123456, 9 số) vẫn gọi lookup — FE bám đúng PhoneNormalizer BE; kỳ vọng 0 request trong lời nhắn sửa là sai của controller — chi phí nếu sai: 1 request thừa, BE trả rỗng nếu không khớp.
Task 5: fix round 1/5 (3 addressed, 0 open — gate chuẩn hoá, e2e chờ request, e2e payload/Escape/cleanup)
Task 5: minor (deferred): donDep e2e xoá mọi liên hệ có SDT_KH (có thể xoá liên hệ thật cùng số).
Task 5: complete (review clean after 1 fix round), head tree 8c12d560ffd7568584967703371ac856723603ed
Task 6: dispatched implementer (sonnet), base tree hrm-client 8c12d560ffd7568584967703371ac856723603ed
Task 6: implementer DONE, head tree 7ebb1ee0201d6d177cd1d0c1d8e24ab913fcc94a. Menu key mới: assign::Danh bạ cá nhân (phải ẩn ở Cài đặt phân hệ prod). Playwright: không tràn 1366/1440, list cuộn riêng, confirm nguyên văn, xoá liên hệ giữ nhắc việc.
Task 6: concern: lỗi console chưa soi từng dòng → final review kiểm.
Task 6: review ✅ Approved. ⚠️ key menu: utils/menuVisibility.js ghép <phân hệ>::<nhãn> ⇒ 'assign::Danh bạ cá nhân' khớp (chưa mở màn Cài đặt phân hệ để nhìn) — ghi chú deploy.
Task 6: minor (deferred): lỗi tải chi tiết làm pane "Đang tải..." mãi; refresh chi tiết nháy + mất cuộn; doDelete không tăng detailSeq; .dbca-sub uppercase → "SẮP TỚI/ĐÃ XONG" lệch copy chốt (nên bỏ uppercase — user thích chữ thường); saveForm gọi loadList 2 lần; e2e donDep sót todo đã xong; e2e overdue chỉ check class; comment afterAll sai.
Task 6: complete (review clean)
Task 7: dispatched implementer (sonnet), base tree TPE_APP 1f04812dd45258648457c0060fde0064c88b9ad3 (29 staged LCT files untouched: 29)
Task 7: implementer DONE, head tree 9adb2dbded30d5d067b8e7373b9bd0638cb5c76c. DI di.config.dart sửa tay (alias _i9001) vì agent nền không được chạy make gen.
Ruling R12 (thay R4): TPE_APP/CLAUDE.md cấm agent nền chạy make gen / build / simulator, và "báo xong = đã bấm thử simulator" ⇒ subagent chỉ code + widget test; SAU Task 9 controller (phiên chính) chạy make gen (chuẩn hoá DI/route) + bấm thử simulator tpeLocal theo DB-01…09 — chi phí nếu sai: gen ghi đè thêm file sinh của việc Lịch lãnh đạo (đã staged) — chỉ là file sinh, không mất logic.
Task 7: review ✅ Approved. ⚠️ company_name: resource trả từ cột personal_contacts.company_name (T1) — ok; 422 errors → chuyển Task 8/9.
Task 7: minor (deferred): _timeOrNull/_strOrNull trùng; storeWithMeta thêm ngoài interface.
Task 7: complete (review clean)
Task 8: dispatched implementer (sonnet), base tree TPE_APP 9adb2dbded30d5d067b8e7373b9bd0638cb5c76c
Task 8: implementer DONE_WITH_CONCERNS, head tree 95645c30eb481dd27d53deb4736e0e91913c7bf1. Package flutter_native_contact_picker ^0.0.12; cần make gen (route args presetContact) + pod install. Test bỏ qua RenderFlex overflow (Ahem) — để reviewer xét. Không RED thật.
Task 8: review ❌ Changes required: I1 nút gọi chết (canLaunchUrl tel: không khai queries/LSApplicationQueriesSchemes); I2 filter test nuốt mọi overflow + rail chữ cái/ dải Gần đây có thể tràn thật; I3 test thiếu source 3, 422 contact.*, teardown sai.
Ruling R13: I1 sửa bằng gọi launchUrl trực tiếp cho tel:/sms:, KHÔNG sửa AndroidManifest/Info.plist (cần user duyệt) — chi phí nếu sai: nếu máy không có app gọi, launchUrl ném lỗi → bắt và báo toast.
Ruling R14: nút "Thử lại" thiếu icon vi phạm quy tắc cứng TPE_APP/CLAUDE.md → gộp vào fix round 1 (không coi là minor) — chi phí: không.
Task 8: minor (deferred): comment "lọc tại chỗ" sai (không có local filter); SĐT "abc" báo "Bắt buộc phải nhập" thay vì "không hợp lệ"; package yêu cầu Dart ≥3.11/Flutter ≥3.41 — khớp fvm 3.41.7, kiểm CI.
Task 8: fix round 1 dispatched, FIX_BASE tree 95645c30eb481dd27d53deb4736e0e91913c7bf1
Ruling R15: chấp nhận ẩn nút Đóng của sheet chọn liên hệ khi bàn phím mở (lệch DB-03) — tránh tràn 17px ở máy thấp; đóng vẫn bằng vuốt/chạm nền, nút hiện lại khi tắt bàn phím — chi phí nếu sai: user muốn nút luôn hiện → thu nhỏ khoảng đệm.
Task 8: fix round 1/5 (4 addressed: I1, I2, R14, I3b; 2 open: I3a company payload source 3 không được test, I3c teardown tự gán — controller grep xác nhận)
Task 8: fix round 2 dispatched, FIX_BASE tree 6fdac3d80dc68739437b22fdd0eca74bb978deda
Task 8: fix round 2/5 (2 addressed, 0 open — test source 3 payload, teardown original)
Task 8: complete (review clean after 2 fix rounds), head tree 3c4bb78e7e79afb0264432725b85cb2b3cb31fb0
Task 9: dispatched implementer (sonnet), base tree TPE_APP 3c4bb78e7e79afb0264432725b85cb2b3cb31fb0
Task 9: implementer DONE_WITH_CONCERNS, head tree 84659aa37fb41911d7d6b4f4140aa761c61011bf. Package flutter_contacts ^2.1.0 (showCreator). 5 analyze errors = route chưa gen. Không BottomNav/rail (màn push từ drawer).
Task 9: review ✅ Approved. flutter_contacts: manifest plugin rỗng (không merge READ/WRITE_CONTACTS), iOS showCreator không xin quyền.
Task 9: minor (deferred): màu quá hạn ở chi tiết tính theo ngày ≠ danh sách tính theo giờ; lỗi chung hiện 2 lần khi sửa; menu ⋮ vẫn bấm được khi đang xoá; Android không có app danh bạ → plugin crash native; "0 người" khi đang tải.
Task 9: complete (review clean)
Controller: running make gen (R12)
Controller: make gen OK (76s, 1134 outputs, index vẫn 29). Sau gen: compile error app_router.gr.dart 'PersonalContact' not found (part file cần import ở app_router.dart) → my_todo tests 16 pass / 5 fail (compile). analyze 175 issues.
Task 9: post-gen fix dispatched (import PersonalContact in app_router.dart), FIX_BASE tree 304da8e2953d93be6986303914089a46488c7e37
Controller simulator check (iPhone 18 Pro, tpeLocal, namdangit/DNS Admin) — PASS: menu trái có "Danh bạ cá nhân"; DB-06 list + empty state; DB-07 chi tiết; "Tạo nhắc việc" mở form gắn sẵn → Lưu → hiện "Sắp tới 1"; DB-01 dòng "Gắn liên hệ"; DB-02 sheet; DB-03 gõ 0912345678 → 3 dòng KH công ty; chọn KH công ty → thẻ có huy hiệu + công ty; Hủy form → danh bạ vẫn 1 (không sinh rác); DB-08 menu ⋮; DB-09 câu xác nhận "1 nhắc việc…" → xoá → todo 470 còn, contact_id null (tinker); bộ chọn danh bạ iOS mở với banner "chỉ truy cập liên hệ bạn chọn" (không xin full quyền).
App finding A1 (Minor/UI): dải "Gần đây" nền xanh chỉ ôm nội dung, không trải hết bề ngang như DB-02 (hệ quả fix I2 Task 8).
App finding A2 (Important/copy): sheet "Liên hệ mới" mở từ DB-06 (thêm tay) vẫn ghi nút "Gắn liên hệ" + dòng "Lưu nhắc việc xong, liên hệ tự vào danh bạ của bạn" — sai ngữ cảnh; phải là "Lưu" và không có dòng ghi chú đó.
App unverified U1: chọn 1 người trong bộ chọn iOS rồi tự điền Tên/SĐT — Mobile MCP không chạm được view tiến trình riêng của CNContactPicker; cần user bấm thử tay. "Lưu vào danh bạ điện thoại", Gọi/Nhắn tin cũng chưa kiểm (simulator không gọi được).
Test data còn: todo 470 "SIM test goi lai Lan" (user 13, không liên hệ).
Final review packages: api 5d6e62a73a243b036fc12b6f8d8cb3264f346925 web 7ebb1ee0201d6d177cd1d0c1d8e24ab913fcc94a app 7243b1f68446ba96264122827403b7d5c542b26f
Final review: Ready after fixes. Important: A2 (app manual-add copy + 422 mất dữ liệu); tên KH >100 ký tự → 422 (28 KH local); spec gap §5.2 thẻ/chi tiết nhắc việc chưa hiện liên hệ; Info.plist thiếu NSContactsUsageDescription (ITMS-90683 khi upload). Minor: uppercase web; company_name lệch web/app; web nuốt lỗi contact.*; web DB-07 dòng không bấm; tên đầy đủ vs tên ngắn ở DB-09.
Ruling R16: fix wave gồm A2, tên KH cắt 100 ký tự ở lookup, bỏ uppercase web (.cp-title, .dbca-sub), company_name thống nhất (kind=customer → null; kind=contact → customer_name), web hiện mọi lỗi contact.*, app 'abc' → "Số điện thoại không hợp lệ", web pane chi tiết lỗi → báo + Thử lại — chi phí nếu sai: nhỏ, chỉ đổi hiển thị/validate.
Ruling R17: spec gap §5.2 (liên hệ trên thẻ/chi tiết nhắc việc) KHÔNG làm trong fix wave — thêm màn mới ngoài plan, đưa user quyết — chi phí nếu sai: tính năng thiếu 1 điểm spec tới khi user chốt.
Ruling R18: Info.plist NSContactsUsageDescription KHÔNG tự sửa (cần user duyệt, như R13) — báo user trước lần upload iOS đầu — chi phí: upload TestFlight bị Apple cảnh báo/từ chối nếu quên.
Final fix wave dispatched.
HRM/hrm-api 5d6e62a73a243b036fc12b6f8d8cb3264f346925
HRM/hrm-client 7ebb1ee0201d6d177cd1d0c1d8e24ab913fcc94a
TPE_APP 7243b1f68446ba96264122827403b7d5c542b26f
Final fix wave: implementer DONE F1–F7 (api 11/9/12 pass; flutter my_todo 72 pass, analyze 173 info 0 err; Playwright verified F3/F5/F7).
Ruling R19: nhãn nhóm trong sheet app vẫn VIẾT HOA (khớp mockup DB-03 app) — để nguyên, web đã chữ thường — chi phí: lệch nhẹ web/app, user có thể muốn đồng bộ.
Final fix wave: re-review all addressed (F1–F7). Controller simulator recheck F1: sheet thêm tay hiện nút "Lưu", không còn dòng ghi chú.
Ruling R20: giữ workspace + chép ledger sang .plans vì KHÔNG có commit (user tự commit) — git chưa phải nơi lưu lịch sử — chi phí: vài file nháp trong .superpowers (đã gitignore).
ALL TASKS COMPLETE 07/11/2026.

## Bổ sung §5.2 (user: "Có làm" + cho phép code: hrm-client gop_db TodoItem.vue + contacts/index.vue + e2e; TPE_APP develop work_item_card + personal_todo_detail_page + test; không hrm-api/migration/commit)
Task 10: dispatched implementer (sonnet), base tree hrm-client 3b81a783212951eda5794c0a8c5c95ea501bfa22
Task 10: implementer DONE, head tree 932134466d63586eab50974360cf86ab26d13d3c (Playwright: line chỉ khi có liên hệ, không tràn 848=848, tên → ?id=243 chọn đúng, 0 modal)
Task 10: review ❌ 1 Important (copy lỗi im lặng). Ruling R21: gộp kiểm kết quả execCommand + SĐT thành link tel: (design §8 "link tel: vẫn để") vào fix round 1 — chi phí: không.
Task 10: minor (deferred): setTimeout không clear; ?id ngoài danh sách đang lọc bị bỏ qua; e2e không kiểm nội dung clipboard.
Task 10: fix round 1 dispatched, FIX_BASE tree 932134466d63586eab50974360cf86ab26d13d3c
Task 10: fix round 1/5 (3 addressed, 0 open — toast lỗi copy, execCommand false, tel: link)
Task 10: minor (deferred): textarea dự phòng sót lại nếu execCommand ném lỗi.
Task 10: complete (review clean after 1 fix round)
Task 11: dispatched implementer (sonnet), base tree TPE_APP d22abbf71b837193e7125940736301a53b972d16
Task 11: implementer DONE, head tree 046b08aaf784440e7c78fc659cc70c385e9ee86c; ran dart format on work_item_card.dart (vi phạm luật, xem số dòng)
Task 11: review ✅ Approved. Ruling R22: giữ nhãn khối "LIÊN HỆ" viết hoa cho đồng bộ "MÔ TẢ"/"BƯỚC CON" trên cùng màn — chi phí: lệch nhẹ copy "Liên hệ".
Task 11: minor (deferred): khối Liên hệ ở chi tiết chưa có widget test; vùng chạm tên ~15px; 3 dòng format lẻ.
Task 11: complete (review clean)
Controller simulator check Task 11 — PASS: thẻ "SIM the lien he" hiện dòng "Nguyễn Văn A · 0912345678" + nút gọi tròn; chi tiết nhắc việc có khối LIÊN HỆ (avatar huy hiệu KH, tên, SĐT, công ty, nút Gọi); chạm khối → chi tiết liên hệ, "Sắp tới 1" đúng. Dọn data thử: todos 465/470/500, contact 0912345678 (user 13).
Ruling R23: không chạy thêm 1 lượt final review toàn nhánh cho phần bổ sung (2 task nhỏ, mỗi task đã soát + Playwright/simulator) — chi phí nếu sai: lỗi chéo web↔app của phần bổ sung lọt (thấp: BE không đổi, payload `contact` đã soát ở final review trước).
ADDENDUM §5.2 COMPLETE 07/11/2026.
- 07/11 (user cho phép): thêm NSContactsUsageDescription vào app/ios/Runner/Info.plist — plutil OK, build simulator OK, khoá có trong Runner.app.
- 07/11 bug user báo "màn sau khi click chọn liên hệ lỗi UI" (user cho phép sửa): tái hiện trên simulator — sheet "Gắn liên hệ" khi danh bạ TRỐNG co vào giữa, thanh chữ cái trôi giữa màn. Nguyên nhân: cột gốc sheet căn giữa mặc định + `Expanded(child: _body())` chỉ cho chiều rộng lỏng → thân co theo nội dung; có danh bạ thì Row+Expanded của dòng ép giãn nên che lỗi; cột trong `crossAxisAlignment.start` làm hộp "Gần đây" không giãn (= A1). Sửa contact_picker_sheet.dart: SizedBox(width: infinity) quanh _body, cột trong stretch, ẩn thanh chữ cái khi 0 người (+ key). Test RED (left 131.6 / width 144) → GREEN; my_todo 81/81; analyze 173. Simulator: trống + có danh bạ + form sau chọn đều đúng. A1 đã hết.
- 07/11 bug user báo "chưa chọn được 1 liên hệ từ danh bạ điện thoại" (user xác nhận: chạm tên → mở thẻ chi tiết; user cho phép sửa). Nguyên nhân (đọc mã plugin flutter_native_contact_picker 0.0.12 iOS): selectPhoneNumber() chỉ xử lý didSelect contactProperty → phải chạm thêm 1 SĐT trong thẻ chi tiết mới trả kết quả; app còn nuốt lỗi im lặng. Sửa new_contact_sheet.dart: dùng selectContact() (chạm tên là xong), hàm thuần phonePickFromContact (ưu tiên số được chọn, không có số → phone rỗng + báo "Liên hệ này chưa có số điện thoại"), lỗi bộ chọn → "Không mở được danh bạ điện thoại". Test RED (hàm chưa có) → GREEN 4+2 ca; my_todo 87/87; analyze 173. Chưa kiểm tay được: Mobile MCP không chạm được bộ chọn iOS → user bấm thử.
- 08/11 (user "làm 1"): e2e my-todo-contact "Escape trong picker" đỏ — GỐC: bấm "Gắn liên hệ" rồi Esc trong ~200–300ms (trước khi BV chuyển focus vào picker) thì Esc rơi vào form ⇒ đóng cả form + mất dữ liệu đang nhập (đo: Esc ngay 2/2 đóng form, chờ 300ms thì đúng). Sửa `TodoFormModal.vue` `@hide="onModalHide"`: trigger esc + showPicker ⇒ preventDefault, chỉ đóng picker. Playwright 6 tình huống đúng (Esc sớm/muộn, Esc lần 2, Esc không picker, nút Đóng). Spec sửa thêm 3 lỗi của chính spec (lộ ra vì trước đây dừng ở ca Escape): chờ form đóng 15s (artisan serve tuần tự, POST xếp hàng 2,5s); ca thẻ nhắc việc phải mở nhóm "Không hạn" (thu gọn) trước khi bấm; `new URL` bị hằng `URL` của spec đè ⇒ `globalThis.URL`. Cả 12 ca xanh (vài ca cần --timeout=90000 khi máy chậm).
- 08/11 test máy thật (user): Gọi OK. Góp ý: chọn từ danh bạ máy phải qua "Tạo mới" ⇒ [x] thêm ô "Danh bạ máy" ở dải Gần đây + dòng "Chọn từ danh bạ điện thoại" ở kết quả tìm của sheet ĐẦU (`contact_picker_sheet._pickFromPhone`): có số → gắn thẳng vào form (source 2, vào danh bạ khi lưu nhắc việc); không số → mở Liên hệ mới điền sẵn tên; bộ chọn lỗi → dòng đỏ ngay trên sheet. Ô rộng 86 + cách 6 (64 cắt "Danh bạ..."). Test +3 ca, app 137/137, analyze 173. CHƯA COMMIT.
- 08/11: góp ý máy thật ĐÃ PUSH — TPE_APP develop `1ae3033`.
