# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/danh-muc-hang-tam/p6-plan.md
Workspace: /private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/7f13b514-f0f1-4314-bf17-0ea4d7f3ff97/scratchpad/p6-sdd (plan .plans/ không nằm trong git)
Nhánh: hrm-api + hrm-client feat/p6-hang-tam từ feat/chuyen-doi-hang-hoa (api 1e194fe5c, client 58965aa63); ERP feat/p6-chan-hang-tam tạo ở Task 8.

## Pre-flight scan
| Cặp / Task | Sản xuất ↔ tiêu thụ | Kết quả |
|---|---|---|
| T1 ↔ T2/T3/T4/T6/T7 | T1 sinh ProductCompany::STATUS_TEMP* / TEMP_STATUSES / isTemp | khớp |
| T2 ↔ T3 | T2 đổi ProductWriteService::store(data, status); T3 đổi writeAdmin(..., ?companyId) — cùng file, tuần tự | khớp |
| T2 ↔ T6 | POST/PUT master-data/temp-products ⇒ popup | khớp |
| T3 ↔ T7 | approve/reject + GET temp-products/{product} ⇒ form duyệt; lineRow cờ ⇒ YCHG form | khớp |
| T4 ↔ T1 | SCREEN_TEMP dùng TEMP_STATUSES | khớp |
| T5 ↔ T2 | log temp_created (C5) được ghi ở T3, đọc ở T5 filterOutNativeErp | khớp (T3 trước T5) |
| T1 tự thân | Step 1 có ca "ProductListResource màn Hàng tạm trả status_text" nhưng màn Hàng tạm làm ở T4 | **xung đột** |
| T3 tự thân | ca "sale thêm hàng tạm vào phiếu Chờ PTKD bị chặn" giả định phiếu status 2 khoá sửa — chưa xác minh | **mơ hồ** |
| T6/T7 | "viết e2e" vs quy tắc chỉ chạy e2e khi user bảo | **lưu ý** |
| T2..T9 khác | file tạo/sửa trong task khớp nhau | khớp |

Ruling: T1 bỏ ca status_text màn Hàng tạm, chuyển sang T4 — màn chưa tồn tại ở T1 — nếu sai chỉ thiếu 1 ca test ở T1.
Ruling: T3 ca "thêm hàng tạm vào phiếu Chờ PTKD" khẳng định theo luật khoá sửa HIỆN CÓ của writer; nếu phiếu 2 vẫn sửa được thì ca phải chứng minh ptkdApprove kiểm lại còn hàng 6 trong transaction — Review Focus 3 vẫn được phủ — nếu sai: thêm ca ở review.
Ruling: e2e chỉ VIẾT spec, KHÔNG chạy tới khi user bảo (memory khong-tu-chay-e2e) — chi phí: e2e chưa xác minh tới lúc chạy.

## Tasks
Task 1: dispatched (BASE api 1e194fe5c, client 58965aa63; model sonnet)
Task 1: implementer DONE_WITH_CONCERNS — api a19f6012f, client 621ae0e34; MasterData 404/404 xanh; implementer agent ac414e37276c0b26f; reviewer dispatched (sonnet)
Ruling: trailer commit T1 ghi "Claude Sonnet 5.5" (model thật của implementer) thay vì "Opus 5.5" — giữ, không amend; các task sau ghi đúng 2 dòng trong context-chung — nếu sai: amend trailer 2 commit local trước merge.
Task 1: ⚠️ resolved — badge ProductListPage đọc status_text/color từ BE ⇒ kiểm DOM ở Task 4; catalog tab Thêm ẩn qua SCREEN_COMPANY có test `catalog_tab_them...` ⇒ đủ.
Task 1: minor (deferred): FQCN inline thay `use` ở ServiceService.php:61, DeviceErrorController.php:34
Task 1: minor (deferred): excludeTempOnly ghép tên cột — ghi chú "chỉ truyền cột cố định"
Task 1: minor (deferred): 2 endpoint CustomerCare chưa test gọi thật
Task 1: minor (deferred): EXISTS/NOT EXISTS pcc trên picker — EXPLAIN kiểm index product_id
Task 1: complete (api 1e194fe5c..a19f6012f, client 58965aa63..621ae0e34, review clean)
Task 2: dispatched (BASE api a19f6012f; model sonnet)
Task 2: implementer DONE — api 7def38679; TempProductApiTest 8/8, MasterData 412/412; agent a647945517db32ac6
Ruling: product_characteristics = 0 dòng (giacty + hrm_erp) nhưng user chốt Đặc tính bắt buộc (A12) — giữ bắt buộc, ghi điều kiện go-live B5 viec-con-lai — nếu sai: không ai tạo được hàng tạm tới khi nhập danh mục.
Task 2: review Needs fixes — Important: thiếu test checkTypeTree; thiếu test nhánh lỗi/rollback linkSourceLines. Fix round 1 dispatched (resume implementer), FIX_BASE 7def38679
Task 2: minor (deferred): linked_lines gắn thuộc tính động lên model; mã HHB cùng code có thể gắn lan dự án khác (ruling 5 cho phép)
Task 2: fix round 1/5 (2 addressed, 0 open; commits 7def38679..99201d3d9)
Task 2: minor (deferred): SET FOREIGN_KEY_CHECKS trong TempProductApiTest không bọc try/finally
Task 2: complete (api a19f6012f..99201d3d9, review clean)
Task 3: dispatched (BASE api 99201d3d9; model opus)
Ruling: T3 thêm `PUT price-asking-requests/{id}/temp-products/{product}` (gate 1662 công ty phiếu) cho nút "Lưu" của PTKD — route sửa hàng tạm sẵn có gate người tạo/1652 nên PTKD không dùng được; lưu khi hàng đang 7 ⇒ về 6 (A5) — nếu sai: PTKD lưu không mất trạng thái đồng ý.
Ruling: T3 log temp_created ghi khi phiếu lưu có hàng 6 gắn lần đầu (1 log/phiếu×hàng) — nếu sai: Task 5 không nhận diện được dòng BOM/báo giá đã gắn mã.
Task 3: implementer DONE_WITH_CONCERNS — api bb7dd513e; PriceAskingTempProductTest 9/9, MasterData 423/423; agent a5bf4acd9ae512f14
Ruling: T3 concern 1 — log temp_reject group_id NULL (FK nhóm chặn rebuild) — chấp nhận; lý do tra theo tiền tố mã trong note — nếu sai: lý do mất khi đổi mã hàng.
Ruling: T3 concern 2 — PTKD phải đổi được quyết định khi phiếu còn 2: approve từ 6/7/8 ⇒ 7, reject từ 6/7/8 ⇒ 8 (mockup: hàng đã xử lý có nút "Sửa") — đưa vào fix round — nếu sai: PTKD không sửa được lựa chọn nhầm.
Ruling: T3 concern 3 — sale sửa hàng tạm (TempProductService::update) KHÔNG được xoá dữ liệu Quản trị PTKD đã nhập — lỗi mất dữ liệu, đưa vào fix round.
Ruling: T3 concern 5 — chặn duyệt phiếu khi hàng tạm bị xoá: Task 4 chặn xoá hàng đang trong YCHG Nháp/Chờ PTKD ⇒ không cần chặn ở ptkdApprove — nếu sai: phiếu duyệt với hàng đã xoá mềm.
Ruling: T3 concern 6 — Task 7 dùng `PUT price-asking-requests/{id}/temp-products/{product}` cho Lưu của PTKD (thay `PUT temp-products/{id}` trong brief T7).
Task 3: review Approved (0 Critical/Important); ⚠️ 2 mục ⇒ controller xác nhận là gap thật ⇒ fix round
Ruling: ⚠️1 hàng 8 trong phiếu 10 có nhóm chưa đóng KHÔNG tính "đang mở" (A9 hàng 8 không đi tiếp, A10 lập YCHG khác) — nếu sai: hàng 8 nằm 2 phiếu cùng lúc.
Ruling: ⚠️2 PTKD KHÔNG đổi brand_id/manufacture_id trong tempSave/tempApprove (422 "Đổi Thương hiệu/Hãng sản xuất: để người lập sửa và đưa vào YCHG khác") — nhóm theo thương hiệu×hãng đã cố định — nếu sai: PTKD phải trả về sale để đổi hãng.
Task 3: fix round 1 dispatched — gồm ⚠️1, ⚠️2, concern 2 (đổi quyết định 6/7/8), concern 3 (giữ admin khi sale sửa), Minor 1 (thứ tự khoá products→pcc), Minor 4 (test phiếu toàn hàng 8). FIX_BASE bb7dd513e
Task 3: minor (deferred): tempRejectReasons tra lý do theo tiền tố mã trong note
Task 3: fix round 1 implemented — 42373c0fd (6 điểm); MasterData 428/428; chưa re-review (gộp với round 2)
Ruling: hàng 8 đưa vào YCHG mới ⇒ GỠ dòng của nó khỏi YCHG cũ (log temp_reject giữ); nhóm cũ rỗng ⇒ đóng Huỷ duyệt — tránh dòng cũ sống lại trong YCTG/closeGroup kéo 2⇒1 — nếu sai: phiếu cũ mất dòng hiển thị hàng đã bị không duyệt (chỉ còn log).
Task 3: fix round 2 dispatched (resume implementer)
Task 3: fix round 2 implemented — b7b36a128; MasterData 430/430
Task 3: fix round 1+2 re-review: 7/7 addressed, 0 open (commits bb7dd513e..b7b36a128)
Task 3: minor (deferred): deadlock tiềm ẩn detachFromOldRequests (phiếu→nhóm) vs PriceCalculateFinalizer (nhóm→phiếu); lockForXnk vs Finalizer ngược nhau từ trước
Task 3: minor (deferred): race hẹp — danh sách phiếu cũ đọc trước khi khoá
Task 3: minor (deferred): gỡ dòng cả ở phiếu đã kết thúc (đúng ruling); lưu nháp gỡ dòng ngay — xoá nháp thì hàng 6 không thuộc phiếu nào (vẫn ở màn Hàng tạm)
Task 3: complete (api 99201d3d9..b7b36a128, review clean)
Task 4: dispatched (BASE api b7b36a128, client 621ae0e34; model sonnet)
Ruling: T4 KHÔNG hiện nút Sửa ở màn Hàng tạm (route sửa hàng hoá gate 1652; popup sửa hàng tạm làm ở T6) — T6 phải bổ sung nút Sửa màn Hàng tạm mở popup — nếu sai: màn Hàng tạm thiếu Sửa tới T6.
Ruling: T4 xoá cứng/mềm đều đặt erp_product_id của dòng BOM/báo giá về NULL — tránh dòng nháp treo tham chiếu — nếu sai: dòng nháp mất liên kết tới hàng đã xoá mềm.
Task 4: implementer DONE — api 62a70da52, client 0297e89e5; TempProductScreenTest 10/10, MasterData 440/440; agent a1e894124d731a85e
Task 4: review Needs fixes — Important: hàng xoá mềm lọt picker YCHG; thiếu tick + Lập YCHG hàng loạt + lọc "Yêu cầu hỏi giá" (mockup M3)
Ruling: mockup M3 đã duyệt là yêu cầu ⇒ làm bulk-ask + lọc YCHG trong T4 (brief thiếu) — nếu sai: thêm việc không cần, dễ gỡ.
Task 4: fix round 1 dispatched (resume implementer) — kèm Minor cột Ngày tạo + thứ tự cột theo mockup. FIX_BASE api 62a70da52 / client 0297e89e5
Task 4: minor (deferred): openRequests() parse 3 lần/dòng; group_concat 1024 byte cần comment; actingAsSameUser dễ vỡ; chưa spec e2e màn temp
Task 4: fix round 1 implemented — api 0889f5828, client 1a6c3436f; controller kiểm reader sau sự cố ghi đè: diff từ b7b36a128 chỉ phần thêm T4, PriceAskingTempProductTest 16/16
Task 4: fix round 1/5 (3 addressed, 0 open; api 62a70da52..0889f5828, client 0297e89e5..1a6c3436f)
Task 4: complete (api b7b36a128..0889f5828, client 621ae0e34..1a6c3436f, review clean)
Task 5: dispatched (BASE api 0889f5828, client 1a6c3436f; model sonnet)
Task 5: implementer DONE — api a0a02154c, client 1d3e8e64b; Assign 7 test (0 fail, 1 skip cũ); agent a08109afd3fa389e6
Task 5: review Needs fixes — Important: mysql2 trong filterOutNativeErp; company_id rỗng lệch giữa pendingCount và erpEligibleQuery
Task 5: ⚠️ resolved — products.tmp_product_id có trong DB gộp (8.931 khác 0); quotations company_id NULL 2/206, trúng thầu 0
Ruling: báo giá company_id NULL ⇒ chưa đạt ở mọi đường (bỏ fallback công ty người đăng nhập) — nhất quán HRM↔ERP — nếu sai: 2 báo giá cũ không lập được HĐ tới khi gán công ty.
Task 5: fix round 1 dispatched (kèm Minor 1 payload rớt dòng im lặng, Minor 4 test 7/8 + bỏ skip). FIX_BASE api a0a02154c
Task 5: minor (deferred): dấu } lệch thụt lề ProspectiveProjectQuotationsTab watch projectId; nhánh/comment erp_tmp_product_id & TmpProductSyncService cũ (ProductProjectController :233-238, :691; QuotationService :2308, :2548)
Task 5: fix round 1 implemented — api 099594b5a; Assign 9 (0 fail, 1 skip cũ), MasterData 442
Task 5: fix round 1/5 (4 addressed, 0 open; api a0a02154c..099594b5a)
Task 5: minor (deferred): priceCompanyOf/pricingCompanyId fallback công ty người đăng nhập (QuotationService :5161, :5204) khác khái niệm "công ty báo giá" của cổng — rà ở review cuối
Task 5: minor (deferred): test payload chưa phủ đường BOM-có-mã & ca ném lỗi
Task 5: complete (api 0889f5828..099594b5a, client 1a6c3436f..1d3e8e64b, review clean)
Task 6: dispatched (BASE api 099594b5a, client 1d3e8e64b; model opus)
USER 12/10: 'xong các task thì chạy e2e luôn' ⇒ T9 được CHẠY e2e (--no-deps --workers=1, 3031/8031). User đi nghỉ — chạy liên tục tới hết.
Task 6: implementer DONE_WITH_CONCERNS — api f2767ec18, client 151abc4a6; TempProductApiTest 13/13, ProductProjectReuseYchgTest 3/3, MasterData 445, Assign 12; spec e2e viết (6 ca, chưa chạy); agent ab778b0e094c16882
Ruling: cây phân loại rỗng trên cả 2 DB (Loại SP/Đặc tính 0) — có sẵn, không do P6; ghi B6 viec-con-lai (chặn go-live); e2e phải tự dựng cây thử + dọn — nếu sai: e2e đỏ vì thiếu fixture.
Ruling: T6 concern 4 — sửa hàng tạm khoá ĐVT (BE cấm đổi ĐVT đã lưu) khác mockup — chấp nhận, đúng luật BE 2-C1 — nếu sai: user muốn đổi ĐVT phải tạo hàng tạm mới.
Task 6: review Needs fixes — Important: luật xem dự án TKT chép ở visibleIdsQuery()
Ruling: không sửa ProspectiveProjectService::index (quy tắc không sửa hàm dùng chung khi chưa hỏi user — user đang vắng) ⇒ giữ bản chép + test đối chiếu ≥5 loại người dùng — nếu sai: còn 2 bản luật nhưng lệch sẽ bị test bắt.
Task 6: ⚠️ resolved — tạo hàng tạm từ phiếu khác công ty: PriceAskingAccess::isVisible 404 phiếu ngoài công ty đang làm việc ⇒ không xảy ra.
Task 6: fix round 1 dispatched (kèm Minor 1,3,4,6). FIX_BASE api f2767ec18 / client 151abc4a6
Task 6: minor (deferred): Tái sử dụng tải per_page=1000 lọc client (>1000 dòng thiếu im lặng); route assign/product-projects không gate (có sẵn)
Task 6: fix round 1 implemented — api b67a2a37f, client bbf221083; test đối chiếu bắt lệch thật (dự án nháp người khác) đã sửa; MasterData 445, Assign 13
Task 6: fix round 1/5 (5 addressed, 0 open; api f2767ec18..b67a2a37f, client 151abc4a6..bbf221083)
Task 6: minor (deferred): useReuseRow để trống ĐVT nếu ychgOptions.units chưa tải; fixture ProspectiveProjectVisibleIdsTest created_by = employees đầu tiên
Task 6: complete (api 099594b5a..b67a2a37f, client 1d3e8e64b..bbf221083, review clean)
Task 7: dispatched (BASE api b67a2a37f, client bbf221083; model opus)
Task 7: implementer DONE_WITH_CONCERNS — client bba8eab26; e2e Y10–Y15 viết (chưa chạy); agent abcc9258fd2e9bf19
Ruling: T7 concern 1 — form duyệt báo 10 lỗi (mockup 11) vì Hãng SX khoá + ĐVT đã lưu chỉ đọc — chấp nhận.
Ruling: T7 concern 2 — theo mockup: ẩn "Đồng ý" khi hàng 7, ẩn "Không duyệt" khi hàng 8 — đưa vào fix round sau review.
Ruling: T7 concern 3 — dòng 8 mờ + lý do cho mọi người xem — đúng A8.
Task 7: review Needs fixes — Important: footer chưa ẩn Đồng ý (7) / Không duyệt (8) theo mockup M4
Task 7: fix round 1 dispatched (kèm Minor: cảnh báo mất thay đổi khi Không duyệt; bỏ GET thừa nếu BE có sẵn). FIX_BASE client bba8eab26
Task 7: minor (deferred): khối toast lặp; hàng thiếu Thương hiệu/Hãng không sửa được ở form duyệt (hiếm)
Task 7: fix round 1 implemented — client 6f1d8aab4
Task 7: fix round 1/5 (3 addressed, 0 open; client bba8eab26..6f1d8aab4)
Task 7: complete (client bbf221083..6f1d8aab4, review clean)
Task 8: ERP nhánh feat/p6-chan-hang-tam tạo từ feat/2d1-erp-khong-loi @ 443c812553; dispatched (model sonnet)
Task 8: implementer DONE_WITH_CONCERNS — ERP f117bf3ce4; ERP PHPUnit 74 (ExampleTest đỏ sẵn); route chặn 106→115; agent af1082a8808bc9303
Ruling: T8 concern 1 — nút "Hàng tạm" báo giá ERP không đo DOM được (màn tạo báo giá ERP đã ngừng, sửa chỉ status 3 của mình, DB không có) — chấp nhận kiểm bằng test chuỗi + Blade compile.
Task 8: review Approved (0 Critical/Important)
Task 8: minor (deferred): 2 link menu "Duyệt hàng tạm (HRM)" / "Hàng tạm chờ duyệt (HRM)" cùng URL; ô ghi chú màn xem phiếu YC hàng tạm vẫn POST updateNote ⇒ toast lỗi chung; import thừa HomeController
Task 8: complete (ERP 443c812553..f117bf3ce4, review clean)
Final review: dispatched (api 1e194fe5c..b67a2a37f, client 58965aa63..6f1d8aab4, ERP 443c812553..f117bf3ce4; model opus)
Final review: With fixes — 4 Important (đổi hãng qua đường sale khi phiếu Chờ PTKD; đường sửa 1652 chưa biết hàng tạm; picker BOM lọt hàng tạm; itemSearch chỉ loại công ty đang xem) + minors triage: sửa trước merge = spec e2e màn Hàng tạm, test payload; còn lại để sau. Danh sách: /private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/7f13b514-f0f1-4314-bf17-0ea4d7f3ff97/scratchpad/p6-sdd/final-findings.md
Final fix wave: dispatched (BASE api b67a2a37f, client 6f1d8aab4, ERP f117bf3ce4; model opus)
Final fix wave: DONE — api 499cc2c25, client 8edf78631, ERP 089a50c66d; MasterData 447, Assign 18 (1 skip cũ), ERP 75 (ExampleTest đỏ sẵn); spec e2e products-temp-ui (7 ca) viết, chưa chạy
Ruling: câu banner C3 đổi thành "Còn N hàng hoá chưa sẵn sàng kinh doanh (hàng tạm chưa tính giá xong / chưa lấy về)" — vì cổng C3 đếm mọi dòng chưa ở 3, không chỉ hàng tạm; lệch chữ spec C3 — cần user duyệt câu — nếu sai: đổi 1 hằng chuỗi.
Task 9: e2e lượt 1 price-asking-temp-product: 1 passed, 1 failed (Y2–Y4 radio tab Tái sử dụng 0 vs 1 tr), 10 did not run ⇒ agent debug e2e dispatched (sửa spec nếu lỗi spec; lỗi app thì báo)
Final re-review: 10/10 addressed, 0 Critical/Important mới
Final: minor (deferred): editableAt xét pcc công ty đang xem vs assertNotTemp xét pcc công ty chủ (lệch nguồn, khó xảy ra); câu MSG_GROUP_KEY viết cho PTKD nay hiện cho người lập; comment cũ QuotationService.php:2557
Task 9: e2e price-asking-temp-product 12/12 passed (sửa 4 lỗi spec, app không lỗi); chạy tiếp temp-ui, md-ui, md-api, Phase 7 (nền)
