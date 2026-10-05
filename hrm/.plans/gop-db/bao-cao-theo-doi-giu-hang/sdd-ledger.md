# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/bao-cao-theo-doi-giu-hang/plan.md

Spec: HRM/docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md + bảng chốt 02/10 cuối design.md (đè spec ở URL/menu, màn cũ song song, root lưu cột).
Workspace: hrm-api/.superpowers/sdd/bao-cao-theo-doi-giu-hang (đặt tên riêng — script mặc định ra ".../plan" trùng mọi plan.md).
Worktree: /Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-giu-hang/{hrm-api,hrm-client,erp}

## Pre-flight scan

| Cặp / Task | Sản xuất ↔ Tiêu thụ | Kết quả |
|---|---|---|
| T2 → T3 | `PrepickDetail::rootPair()`, fillable 2 cột | khớp |
| T2 → T4 | cột trên DB ERP local `erp2326` (T4 Step 1 chạy lại migration với DB_DATABASE override) | khớp, phụ thuộc config:clear (T1 Step 3) |
| T2 → T8 | `PrepickRootResolver::EXTEND_TYPE`, `MAX_DEPTH` dùng trong `PrepickExtendChain` | khớp |
| T5 → T8 | `PrepickTrackingScope::companyIdFor/ownCompanyId/canViewAllCompanies` | khớp |
| T6 → T8 | `PrepickDocumentResolver::resolve()/label()` | khớp |
| T7 → T8/T9 | hình dạng row; `Tree::DIMS/build/find/paginate`; `Drill::filter/sort` (đọc `root_code`) | khớp — `root_code` chỉ có sau `attachDocuments` (T8 xử) |
| T8 ↔ T9 | Controller T8 type-hint `PrepickTrackingPrintService` (tạo ở T9) | PHP không autoload type-hint lúc khai báo → route T8 nạp được; test T8 không gọi print. OK |
| T7 test ↔ test | `PrepickTrackingMetricsTest::row()` gọi từ test class khác | cần namespace `Modules\Finance\Tests\Unit` autoload được — implementer kiểm |
| T10 ↔ T15 | `stock?prepick_detail_id` → `focus`; `/lot` | khớp |
| T8 → T11-14 | 8 endpoint `finance/prepick-tracking` | khớp |
| T1 | tự nhất quán | OK |
| T2 | test 5 ca ↔ code resolver | khớp (đã dò tay) |
| T3 | test dùng `addLot` 8 tham số ↔ chữ ký thật | khớp; ca transfer có ghi chú kiểm hạn đích |
| T4 | không test tự động (ERP không có suite) | chấp nhận — kiểm `php -l` + grep đếm |
| T5 | test dùng `\App\Models\Employee` + bảng `employee_has_permissions` | có ghi chú kiểm provider/cột |
| T7 | 3 test ↔ code — đã dò tay từng assert | khớp |
| T9 | test flatten ↔ code | khớp |

Ruling: Super admin (role 18) coi như có quyền "theo tổng công ty" — spec nói "đúng 1 quyền" nhưng toàn bộ nhóm giữ hàng HRM bỏ qua quyền cho super admin; nếu sai: super admin thấy "Tất cả công ty" mà không được gán quyền (họ vốn xem được mọi thứ).
Ruling: Sắp xếp tên dùng strcmp sau mb_strtolower (chữ có dấu xếp sau) trừ khi máy có ext intl — nếu sai: thứ tự A→Z lệch ở tên có dấu, chỉnh 1 hàm.
Ruling: Task 1 (worktree) controller tự làm — là bước Setup môi trường, không có code để review.

## Tiến độ
Task 1: complete (worktree 3 repo; base hrm-api 0bfd98d31 · hrm-client 976e1eb32 · erp 3a87a07d4f; autoload trỏ đúng worktree; config:clear)
Note: ERP origin/gop_db đã tiến từ 1fd600e7fe lên 3a87a07d4f sau khảo sát — số dòng trong T4 có thể lệch, tìm theo tên hàm.
Ruling: Commit từng task trên nhánh feature trong worktree (không push) — CLAUDE.md cấm commit khi chưa có yêu cầu, nhưng user đã duyệt plan có bước commit + chọn subagent-driven; nếu sai: gộp/huỷ commit trên nhánh riêng, không ảnh hưởng gop_db.
Task 2: dispatched (base 0bfd98d31, implementer sonnet)
Task 2: implementer DONE_WITH_CONCERNS (commit 0c3808af5). Số đo local: trước backfill EXT 34.034/61.771; ghi 48.080 (WPR 31.095 · ProductImportDetailCustomer 8.969 · PrepickTransfer2 8.016); sau backfill dòng còn tồn chưa root = 304 (41 objectable NULL + 263 dòng gia hạn có gốc NULL); số yêu cầu giữ = 2.146.
Ruling: 263 dòng gia hạn có gốc là dòng objectable NULL để root NULL → báo cáo COALESCE về objectable (hiện mã phiếu gia hạn, loại "Gia hạn giữ hàng") — đúng resolver, chỉ ~1/2.400 dòng còn tồn; nếu sai: cần resolver gán root = dòng gốc NULL thành "không xác định" thay vì phiếu gia hạn.
Task 2: review dispatched (sonnet)
Task 2: minor (deferred): backfill UPDATE từng dòng trong lô 500 (không CASE WHEN) — chạy 1 lần, chấp nhận.
Task 2: complete (commits 0bfd98d31..0c3808af5, review clean)
Task 3: dispatched (base 0c3808af5, sonnet)
Task 3: implementer DONE (534566cfb); review dispatched
Task 3: minor (deferred): chưa có test ca "dòng đã có → cộng dồn, root giữ nguyên" (cấu trúc diff đã bảo đảm).
Task 3: complete (commits 0c3808af5..534566cfb, review clean)
Task 4: dispatched (base erp 3a87a07d4f, sonnet)
Task 4: implementer DONE (erp 856dc00e4f; migration chạy được trên erp2326)
Task 4: review dispatched
Task 4: complete (erp commits 3a87a07d4f..856dc00e4f, review clean)
Task 5: dispatched (base 534566cfb, sonnet)
Task 5: implementer DONE (8085ba5); auth model = TpEmployee (ghi vào implementer-common)
Task 5: review dispatched
Task 5: minor (deferred): test chưa phủ nhánh super admin; plainEmployee() không orderBy; companyIdFor ép (int) chuỗi không phải số thành 0 (rỗng) thay vì báo lỗi.
Task 5: complete (commits 534566cfb..8085ba518, review clean)
Task 6: dispatched (base 8085ba518, sonnet)
Task 6: implementer DONE (8e2c4693c); logsOfLot trước/sau giống hệt trên 3 lô
Task 6: review dispatched
Task 6: minor (deferred): label() chưa có test.
Task 6: complete (commits 8085ba518..8e2c4693c, review clean)
Task 7: dispatched (base 8e2c4693c, sonnet)
Task 7: implementer DONE (f87936f, cea621e, 31994f6); intl có trên máy local
Task 7: review dispatched (opus — logic lõi)
Task 7: review Needs fixes — Important: sắp tên bằng strcmp (chữ có dấu xếp sau Z).
Ruling: Đổi sang Collator('vi_VN') khi class_exists('Collator'), fallback strcmp(mb_strtolower) — đè lên chỉ dẫn "đừng đổi" của controller (chính controller sai so với plan); nếu sai: production không có intl thì vẫn chạy fallback.
Ruling: Khoá yêu cầu giữ dùng đúng 1 dạng "root_type#root_id|product_id|employee_id" (khớp plan T8 + test helper) — global constraint ghi "|" là mô tả lỏng; nếu sai: chỉ đổi 1 chỗ dựng key trong RowLoader.
Ruling: gộp vào fix round 1 thêm 2 minor rẻ: tiebreak cuối bằng id (usort PHP 7.4 không ổn định → node nhảy trang) + sort cột ngày dùng cmpDate (null xuống cuối).
Task 7: fix round 1 implemented (218ba41d8); re-review dispatched
Task 7: fix round 1/5 (3 addressed, 0 open — collation vi, tiebreak id, null date cuối; commits 31994f663..218ba41d8)
Task 7: minor (deferred): nhãn sort nhân viên chỉ tên (mockup "tên - phòng"); find() bỏ qua $criteria; comment `sub` sai; thiếu test dept null / find tiêu chí product / metric ok,soon; tiebreak id ở nhánh desc cũng đảo chiều.
Task 7: complete (commits 8e2c4693c..218ba41d8, review clean sau fix)
Task 8: dispatched (base 218ba41d8, opus) — mang theo: allow-list `metric`, dùng PrepickTrackingText::compare cho sort tên trong service, TpEmployee
Task 8: implementer DONE_WITH_CONCERNS (2ee52a606). Hiệu năng 60–210ms/endpoint (service, company all). Lệch brief: employees không có cột code → ei.code; đơn vị cơ bản qua baseUnits(); alias SUM; test dùng JWT thật (withToken); parts.status=1 mới tính.
Ruling: "Tổng thanh toán" giữ nguồn spec (bill_income_details + bill_incomes.status=3) dù local ra 0 cho cả 72 HĐ đang có hàng giữ (bảng có 7.543 dòng FirmContract nhưng không trùng HĐ nào) — spec là căn cứ; nghi DB local thiếu phiếu thu gần đây. Phải báo user khi kết thúc: có nên đổi sang firm_contracts.payed_cost / account_details. Nếu sai: cột Tổng thanh toán = 0 trên production → đổi 1 hàm paidOf()+payments().
Task 8: review dispatched (opus)
Task 8: minor (deferred): CONTRACT_CLASSES trùng map tableOf() của PrepickLotContractService; tham số dạng mảng (?metric[]=) ra 500; LIKE không escape % _; test payments chỉ so 0=0.
Task 8: complete (commits 218ba41d8..2ee52a606, review clean)
Task 9: dispatched (base 2ee52a606, sonnet)
Task 9: implementer DONE (083c25f2c); lo ngại letterhead không ghép ERP_URL
Task 9: review dispatched
Task 9: review Needs fixes — (1) letterhead không theo headerUrl() (ghép ERP_URL khi path tương đối); (2) colspan bảng cây lệch 1 cột ở blade Excel + in.
Ruling: theo quy tắc CLAUDE.md (print-page 4b) cho letterhead — CLAUDE.md đè brief "copy prepick-stock-list"; nếu sai: chỉ là đường dẫn ảnh đầu trang.
Task 9: fix round 1 implemented (d3c11f6ff); re-review dispatched
Task 9: fix round 1/5 (2 addressed, 0 open — letterhead headerUrl, colspan; commits 083c25f2c..d3c11f6ff)
Task 9: complete (commits 2ee52a606..d3c11f6ff, review clean sau fix)
Task 10: dispatched (base d3c11f6ff, sonnet)
Task 10: implementer DONE (bf69c26c3). Ghi chú: lô quá hạn luôn nằm trong danh sách (hạn ≤ hôm nay+W) nên nhánh 'còn N ngày' không bao giờ ra N âm.
Task 10: minor (deferred): lot() trả thêm prepick_detail_id, customer_code; comment "5 route TINH" cũ; chưa test nhánh focus "không thuộc về bạn".
Task 10: complete (commits d3c11f6ff..bf69c26c3, review clean)
Task 11: dispatched (base hrm-client 976e1eb32, opus — FE từ prose + mockup)
Task 11: implementer DONE_WITH_CONCERNS (client 25bc005e7). Chưa test được tài khoản không quyền thật (2 tài khoản e2e không quyền login 422) — giả lập qua window.$nuxt.
Ruling: canViewAll lấy theo field BE `can_view_all_companies` (khởi tạo false, chỉ bật khi BE trả true) — CLAUDE.md cho phép "set từ field BE trả về"; super admin không có quyền trong store nhưng BE coi là có; nếu sai: super admin mất ô Công ty.
Task 11: review dispatched (opus)
Task 11: minor (deferred): /meta đầu tiên có thể gửi company_id=công ty mình khi cache quyền FE cũ; employeeOptionText .trim() nếu code là số; title dài trên nút.
Ruling: minor "warn_day lỗi đỏ mà đổi ô khác vẫn gọi API" vi phạm quy tắc CLAUDE.md → gửi kèm Task 12 (cùng file index.vue) thay vì mở fix round riêng.
Task 11: complete (client commits 976e1eb32..25bc005e7, review clean)
Task 12: dispatched (base 25bc005e7, opus)
Task 12: implementer DONE_WITH_CONCERNS (abef5ae3b); TỔNG 676 Mã khớp dải tổng hợp; lo ngại: nhãn floating đè radio 'Theo nhân viên' (từ T11), /children lỗi im lặng
Task 12: review dispatched (opus)
Task 12: review Needs fixes — (1) /children dùng bộ lọc đang gõ chưa áp; (2) chữ đậm trong ô (.prd-code 700, ...) trái quy tắc; (3) /children lỗi nuốt im lặng, dòng mở rỗng.
Ruling: gộp vào fix round 1 lỗi nhãn floating đè radio "Theo nhân viên" (code Task 11, implementer T12 tự báo) — lỗi giao diện nhìn thấy được trên màn, cùng file; nếu sai: chỉ thêm 1 chỉnh CSS.
Task 12: fix round 1 implemented (b93d08ed3)
Task 12: fix round 1/5 (4 addressed, 1 new open — X-Silent-Errors bỏ qua xử lý 401 hết phiên; commits abef5ae3b..b93d08ed3)
Task 12: fix round 2 implemented (91b9e4cc0) — bỏ X-Silent-Errors; re-review dispatched
Task 12: fix round 2/5 (1 addressed, 0 open; commits b93d08ed3..91b9e4cc0)
Task 12: minor (deferred): INTERCEPTOR_TOAST_CODES thiếu 428; level select hiện nhãn tiêu chí cũ thoáng qua khi đổi tiêu chí; loadReport lỗi → bảng biến mất không có trạng thái rỗng; thụt lề COLS lệch (chưa chạy prettier); 403/500/504 chỉ có thông báo chung không kèm tên dòng.
Task 12: complete (client commits 25bc005e7..91b9e4cc0, review clean sau 2 vòng)
Task 13: dispatched (base 91b9e4cc0, opus)
Task 13: implementer DONE_WITH_CONCERNS (8c2182764). Chế độ 'của tôi' phải giả lập (user e2e không có hàng giữ); popup phiếu thu chỉ kiểm khung (paid local = 0).
Task 13: review dispatched (opus)
Task 13: minor (deferred): popup lỗi hiện như rỗng; badge trạng thái tự dựng (không V2BaseBadge, FE map chữ/màu); mã HĐ/phiếu thu trông như link mà không phải link; "Đã gia hạn 0 lần" lúc đang tải; chế độ "của tôi" + phiếu thu chưa kiểm dữ liệu thật.
Ruling: minor "mine đọc trực tiếp không snapshot cùng reportParams" gửi kèm Task 14 (cùng index.vue) — rẻ, chặn nút hiện trên hàng người khác trong lúc đang tải lại.
Task 13: complete (client commits 91b9e4cc0..8c2182764, review clean)
Task 14: dispatched (base 8c2182764, sonnet)
Task 14: implementer DONE (93d9626fa); Excel dùng secondary status=success (#15803d) thay #16a34a của brief
Task 14: review dispatched
Task 14: minor (deferred): PrintOptionsModal footer Hủy→In (port nguyên TKT, lệch button-convention §5); nhánh cắt 2.000 dòng chỉ kiểm bằng curl.
Task 14: complete (client commits 8c2182764..93d9626fa, review clean)
Task 15: dispatched (base 93d9626fa, sonnet)
Task 15: implementer DONE (b9f933218); 404 interceptor KHÔNG toast → tự thêm 1 toast; dữ liệu test 61824/61825 đã xoá
Task 15: review dispatched
Task 15: minor (deferred): cancel pre-fill tìm hàng không ra → im lặng chỉ điền khách; applyFocusFromQuery dựa ngầm vào BE luôn có message khi in_list=false.
Task 15: complete (client commits 93d9626fa..b9f933218, review clean)
Ruling: e2e/ không nằm trong git → spec Task 16 ghi thẳng vào HRM/e2e, không commit; không chạy cả bộ (memory "không tự chạy e2e") — chỉ `playwright test --list` + tsc để chắc biên dịch; nếu sai: spec có thể đỏ khi user chạy lần đầu.
Task 16: dispatched (opus)
Task 16: implementer DONE_WITH_CONCERNS — API spec 11/11, UI 13/13 (run 3; run 1 FK cleanup, run 2 timeout 30s→120s). Đối chiếu mockup ghi vào design.md: lệch đáng kể = dòng hàng hoá xuống dòng nhiều (880/1.162 dòng >40px), nút "Hàng giữ của tôi" xám thay vì viền teal, chữ ô popup đen thay vì #1f2937.
Ruling: chạy spec 3 lần thay vì 1 — chấp nhận (2 lần đầu đỏ vì lỗi fixture/timeout của chính spec, không phải app).
Task 16: review dispatched (sonnet, đọc file trực tiếp — e2e không có git)
Task 16: review Needs fixes — cleanup khi seed hỏng giữa chừng để sót dòng ok/soon/exp/contract (fx undefined → không chạy heuristic theo employee_id).
Task 16: fix round 1 implemented (seed transaction + cleanup độc lập fx + state file trước insert); re-review dispatched
Task 16: fix round 1/5 (1 addressed, 0 open)
Task 16: complete (e2e files không git; review clean sau fix)
Final review: dispatched (opus, 3 repo)
Final review: needs fixes — I1 thứ tự deploy sai (code trước migrate → mọi đường tạo hàng giữ lỗi Unknown column); I2 backfill lần 2 phải --all; I3 Huỷ giữ có thể điền sai hàng (|| items[0]); I4 footer In/Hủy sai thứ tự; I5 badge tự dựng trái quy tắc V2BaseBadge; I6 gop_db upstream đã tiến 74 commit (hrm-api) chồng file; I7 Tổng thanh toán =0 (đã ghi); M1 lộ tên KH/NV công ty khác ở dòng tóm tắt bộ lọc bản in; M2 metric[] → 500.
Ruling: I5 theo CLAUDE.md (V2BaseBadge + BE trả status_text/status_color, màu chuẩn #16A34A/#F59E0B/#DC2626) — quy tắc dự án đè mockup; nếu sai: badge lệch màu mockup chút, đổi lại 1 map ở BE.
Ruling: gộp M1 + M2 vào đợt sửa final (rẻ, M1 là rò tên ngoài phạm vi).
Ruling: I1/I2 sửa trong checklist deploy (Task 17, controller ghi tài liệu) — không phải code.
Ruling: I6 (merge gop_db vào nhánh feature) để bước finishing do user quyết — merge là thao tác user phải đồng ý.
Final fix wave: dispatched (opus) — I3, I4, I5, M1, M2
Final fix wave: DONE (api 361007723, client 389c3497e); scoped re-review dispatched
Final fix wave: re-review clean (5/5 addressed)
