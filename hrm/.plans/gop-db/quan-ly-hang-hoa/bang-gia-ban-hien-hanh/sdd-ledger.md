# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/bang-gia-ban-hien-hanh/plan.md
Spec: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/docs/superpowers/specs/gop-db/2026-10-28-bang-gia-ban-hien-hanh-design.md
Repos: hrm-api + hrm-client @ gop_db (HEAD api bf24b5f5b, client 4eb26ea7d lúc bắt đầu, cả 2 sạch)
User cho phép 28/10: code trên gop_db ("làm luôn gop_db"); chèn quyền vào DB local.

## Pre-flight scan
| Cặp / task | Produces → Consumes | Kết quả |
|---|---|---|
| T1 ↔ T2 (service, controller, routes, test file chung) | T1: resolveCompanyId, canViewCost, query, units → T2 dùng | khớp |
| T3 ↔ T5 (export-fields-modal) | T3: props submitText/submitIcon/headerIcon + slot #options → T5 dùng | khớp |
| T4 ↔ T5 (page index.vue) | T4: filters/sort/tableColumns/companyMeta/canViewCost/canExport → T5; khoá cột = id exportFields = khoá sort/fields BE (code,name,manufacture,brand,model,unit,cost,price_1..6) | khớp |
| T1 ↔ T4 (API contract) | data[]{id,code,name,manufacture_name,brand_name,model_name,units[]}, meta{company,can_view_cost} | khớp |
| T1 tự thân | Step1 "không chạy seeder vào DB khi chưa hỏi" ↔ user đã cho chèn quyền | xem Ruling 1 |
| T2 tự thân | headings 1 tầng ↔ spec 2 tầng | xem Ruling 2 |
| T3 tự thân | đo /assign/customers trước/sau | khớp |
| T4 tự thân | khớp | khớp |
| T5 tự thân | khớp | khớp |
| T6 tự thân | Step2 chạy e2e chỉ khi user yêu cầu | xem Ruling 3 |
| Toàn plan | skill SDD yêu cầu commit/task ↔ CLAUDE.md + memory: không commit | xem Ruling 4 |

Ruling 1: chèn tay đúng 2 dòng permissions (guard api, group 'Hàng hoá', type 8) vào DB local + cấp tạm cho tài khoản test khi kiểm UI; KHÔNG chạy cả PermissionsTableSeeder — DB local lệch, sync kéo quyền người khác (memory hrm-them-permission-moi) — sai thì thiếu/sai quyền ở local, sửa tay được.
Ruling 2: Excel tiêu đề 1 tầng ghép "<Loại> - Hiện tại/Sắp áp dụng/Từ ngày" — listExportFile chỉ 1 hàng tiêu đề, không sửa util dùng chung — sai thì user muốn 2 tầng ⇒ sửa listExportFile sau (đã báo user khi giao plan).
Ruling 3: Task 6 chỉ VIẾT spec e2e, KHÔNG chạy — memory khong-tu-chay-e2e-moi-task; kiểm thật bằng Playwright MCP ở T3–T5 — sai thì user yêu cầu chạy là chạy.
Ruling 4: KHÔNG commit. Mốc task = `git add -A` (staging) ở cả 2 repo sau khi review sạch; diff task sau = worktree vs index (+ `git add -N` file mới) — sai thì user muốn commit từng task, gom lại commit được từ staging.

## Tiến độ
Task 1: dispatched (sonnet) — BASE api bf24b5f5b / client 4eb26ea7d (worktree sạch, chưa staging)
DB test: hrm_erp_bang_gia_test (bản sao hrm_erp_21_10_prod, user chọn 28/10) — đang sao
DB test: hrm_erp_bang_gia_test sẵn sàng 16:32 (1912 bảng, product_unit_prices 1,032,019 = nguồn)
Task 1: implementer DONE_WITH_CONCERNS — 12 test/64 assert xanh + ProductPriceScreenApiTest 32 xanh (DB bản sao); perf cty 2 (30,275 hàng): list 0.33s, sort giá ~1s, only_next 0.11s. Concerns: không RED đúng nghĩa (code trước test vì chờ DB); cost null chỉ khi ≤0; sort giả định 1 is_base/hàng; only_next xét mọi ĐVT; catalog form-options chỉ nhánh có hàng. Review dispatched (sonnet), diff review-task1.diff.
Task 1: review Approved (0 Critical/Important). ⚠️ tự kiểm: hàng ≥2 ĐVT is_base=1 trên hrm_erp_21_10_prod = 0 ⇒ rủi ro nhân dòng khi sort không xảy ra với dữ liệu hiện tại.
Task 1: minor (deferred): sort giá join is_base có thể nhân dòng nếu dữ liệu bẩn (hiện 0 hàng)
Task 1: minor (deferred): thiếu test sort name/manufacture/brand/model, trần per_page, company_id không tồn tại (404), price_9 ngoài whitelist, only_next lọt qua ĐVT phụ
Task 1: minor (deferred): companyBrief truy vấn companies lặp
Ruling 5: catalog form-options = chỉ nhánh có hàng xếp ở công ty xem (khác ProductListPage nạp cả cây, có is_locked) — giữ, vì spec "catalog theo công ty đang xem" và màn lọc không cần nhánh rỗng — sai thì user muốn cả cây ⇒ đổi sang ProductOptionService::catalogOptions + lọc theo công ty.
Ruling 6: giá vốn ≤ 0 ⇒ null (ô trống) — quy ước "chưa có giá vốn", spec chỉ nói giá bán ≤1 — sai thì cột giá vốn hiện 0 thay vì trống, sửa 2 dòng.
Ruling 7: ô giá chính null nhưng có next_price ⇒ FE vẫn hiện dòng phụ (giá hiện tại chưa có, sắp có giá) — đúng nghĩa nghiệp vụ.
Task 1: complete (staged, review clean, 3 minor deferred)
Task 2: dispatched (sonnet) — BASE = index sau Task 1 (staged)
Task 2: implementer DONE_WITH_CONCERNS — RED 9/9 404 ⇒ GREEN cả file 21 test/109 assert; perf cty 2: export p1 1.14s, p2 0.61s, all 0.51s, sort price 1.51s, print only_next 0.09s. Concerns: payload in thêm truncated; trần in đếm theo HÀNG (all ĐVT có thể >2000 dòng); config price_board_print_max_rows chưa khai (fallback 2000); total ở all = số dòng ĐVT. Review dispatched.
Task 2: review Needs fixes — Important: blade number_format kiểu VN (2.000.000) + test khoá sai. ⚠️ perf export: implementer báo p1 1.14s / p2 0.61s (đã đọc report) ⇒ resolved.
Task 2: minor (deferred): controller rỗng template khi vượt trần trùng với trait
Task 2: minor (deferred): placeholder hàng không ĐVT làm rows lệch total ở unit_mode=all (FE có thể dừng sớm) — hiếm, hàng nào cũng có ĐVT gốc
Task 2: minor (deferred): docblock EXPORT_INFO sai mô tả
Task 2: minor (deferred): thiếu test in unit_mode=all + test in không lộ cột Giá vốn khi không quyền
Task 2: minor (deferred): trần in đếm theo hàng (all ĐVT có thể >2000 dòng)
Task 2: fix round 1/5 dispatched (resume implementer) — finding: định dạng số bản in
Task 2: fix round 1/5 (1 addressed, 0 open — định dạng số bản in)
Task 2: complete (staged, review clean sau 1 vòng sửa, 5 minor deferred)
DB app hrm_erp_21_10_prod: chèn 2 quyền mới (user cho phép) — xem id ở trên
Task 3: dispatched (sonnet) — BASE client = 4eb26ea7d (worktree sạch)
Task 3: implementer DONE — đo /assign/customers trước/sau khớp (tiêu đề, icon, nút, 720x620, 20 dòng, không options); 192 file dùng; 4 lỗi console có sẵn trước/sau. Review dispatched.
Task 3: review Approved. minor (deferred): v-if $slots.options bỏ sót slot có scope (#options="x") — nên thêm $scopedSlots.options
Task 3: complete (staged client, review clean)
DB app: role tạm 108490 TMP-BANG-GIA-28-10 → NV 13 cty 1, quyền 101269/101270/1092 @cty1 — XOÁ khi xong (roles, employee_has_roles, role_has_permissions)
Task 4: dispatched (sonnet) — BASE client = index sau Task 3. API thật: cty1 30,272 hàng can_view_cost=true; cty4 can_view_cost=false (đúng quyền theo công ty xem)
Task 4: implementer DONE_WITH_CONCERNS — DOM: th 14/13, next-price rgb(37,99,235), đổi ĐVT 0 request, sort 1 request price_1, gap 18px, 0 tiêu đề nhóm, nút 12px, đổi cty reset catalog, 0 lỗi console. Chưa kiểm ca không quyền view-all/export + menu DOM. Review dispatched.
Task 4: review Approved. ⚠️ V2BaseSelect size xs: có (validator xs/sm/md/lg) ⇒ ok. ⚠️ DOM Step 5: tin report implementer; ca không quyền view-all/export controller tự kiểm ở bước cuối.
Task 4: minor (deferred): cờ _restoringFilters một lần có thể nuốt lần đổi lọc kế tiếp (xác suất thấp)
Task 4: minor (deferred): item.units.length thiếu guard || []
Task 4: minor (deferred): sort_by=cost còn giữ khi đổi sang công ty không quyền giá vốn (BE bỏ qua ⇒ về code)
Task 4: minor (deferred): :key thừa trong slot; handleSearch bắn lại request khi bấm Tìm
Task 4: complete (staged client, review clean)
Task 5: dispatched (sonnet) — BASE client = index sau Task 4. Ruling 8: letterhead Excel lấy theo công ty xem bằng gọi trực tiếp letterhead?company_id= ở page, KHÔNG đổi chữ ký fetchCompanyLetterhead dùng chung — sai thì trùng logic nhỏ ở 1 page.
Task 5: implementer DONE_WITH_CONCERNS — popup 13 trường tick đúng cột, ẩn Model ⇒ 12; xlsx 18 dòng 26 cột, ô số numFmt #,##0, letterhead cty xem; in: khổ ngang 1124px, dòng phụ xanh; cty2 không Giá vốn. Concern: lỗi console chưa truy; ca không quyền export chưa đo. Review dispatched.
Controller kiểm ca KHÔNG quyền (gỡ tạm 101269/101270 khỏi role 108490 rồi trả lại): 0 nút Xuất/In, không ô Công ty, API công ty 4 ⇒ 403, export-rows ⇒ 403, cột Giá vốn vẫn có (quyền 1092 cty1). ⇒ ⚠️ Task 4/5 về ca không quyền: resolved.
Task 5: review Approved-có-điều-kiện. Important (reviewer): letterhead fallback khi filters.company_id rỗng (!canViewAll) ⇒ rơi về info->company_id có thể ≠ công ty đang làm. Controller tìm thêm (Playwright): Vue warn "exportFieldsModalId is not defined" ×5 mỗi lần tải trang — confirmed gap.
Task 5: minor (deferred): exportOptions không reset khi mở lại popup; nút In thiếu :interactable=!exporting; tên trường popup theo tiêu đề cột ("Hãng sản xuất")
Task 5: fix round 1/5 dispatched (resume implementer) — exportFieldsModalId + letterhead fallback companyMeta.id
Task 5: fix round 1/5 (2 addressed, 0 open — exportFieldsModalId; letterhead fallback companyMeta.id). minor (deferred): cả filters.company_id lẫn companyMeta rỗng (form-options lỗi) thì letterhead vẫn thiếu company_id
Task 5: complete (staged client, review clean sau 1 vòng)
Task 6: dispatched (sonnet) — chỉ viết spec, chạy --list
Task 6: implementer DONE_WITH_CONCERNS — 13 ca (U1–U9 admin, P1–P4 có/không quyền), --list OK (16 gồm setup). Tài khoản hạn chế e2e_assign_nocost (id 4589, ghim company_role=1, trả lại afterAll); helper role tạm viết trong spec; đọc Excel bằng unzip; dữ liệu thật cty 1/2. Chưa chạy (Ruling 3). Review dispatched.
Task 6: review Needs fixes — Important: P1–P4/U2/U3/U8 skip im lặng; U2 đỏ giả (next ở ĐVT không hiển thị); công ty admin không ghim; assert #,##0 yếu (numFmtId 3). Gap: chưa có ca export/print không lộ giá vốn.
Task 6: minor (deferred): serial ⇒ đọc dòng tổng kết; P3 phụ thuộc cty 2 có hàng; company_role ghép SQL không nháy; selector chưa kiểm (title nút cấu hình cột, .board-filter-only-next, select2)
Task 6: fix round 1/5 dispatched (resume implementer)
Task 6: fix round 1/5 (5 addressed, 2 open — restore company_role không nằm trong finally riêng; chọn công ty select2 substring). minor (deferred): waitForTimeout 1500 ở U3 (chờ "không request" — chấp nhận); U2 chưa đối chiếu ĐVT đang hiện = units[0]
Task 6: fix round 2/5 dispatched
Task 6: fix round 2/5 (2 addressed, 0 open). minor (deferred): restore khi old='' ⇒ ghi 0; unwrap giả định response bọc data; nhãn option công ty phải đúng "CODE - NAME"
Task 6: complete (spec ngoài git, review clean sau 2 vòng, CHƯA chạy — Ruling 3)
Final review: dispatched (opus) — package review-final.diff
Final review: SẴN SÀNG (opus) — 0 Critical/Important, PHPUnit 21/21; minor triage: tất cả để sau; Ruling 1–8 đồng ý (R2 cần ghi design)
