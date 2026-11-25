# Ledger — plan: HRM/.plans/khoa-hang-chan-tien-trinh/plan.md

Executor: inline (Native). Repo hrm-api branch `develop` @ 5c2db2e96 (clean). KHÔNG worktree (user làm thẳng develop), KHÔNG auto-commit (rule HRM).

Pre-flight: Task 2–5 đều consume `ProductInProgressService` do Task 1 tạo; Task 5 consume cả 4 method `existsXxxInProgress`. Chữ ký khai 1 chỗ ở Task 1, dùng lại nhất quán — không xung đột interface.
Ruling chung: dùng probe tinker READ-ONLY thay phpunit (phpunit HRM chia sẻ DB thật, không transaction-isolated) — đã ghi trong plan Global Constraints. Cost nếu sai: verify yếu hơn test ghi, bù bằng Playwright ở Task 5.

## Tiến độ

Task 1 Step 1 (kiểm dữ liệu/const, 2026-11-25):
- Const model ERP (CHUẨN, khác map blade đã trace): Inland `{DA_HUY=0, DA_DUYET=1, CHO_DUYET=2, DANG_TAO=3, DANG_LAP_HOP_DONG=4, DA_LAP_HOP_DONG=5, CHO_TP_DUYET=6}` → chặn {1,2,3,4,6}, terminal {0,5}. Root `{DANG_TAO=1, CHO_TP_DUYET=2, CHO_DUYET=3, DA_DUYET=4, DA_HUY=5}` → chặn {1,2,3}, terminal {4,5}.
- Ruling: BỎ `order_request2` khỏi guard — 3366 dòng nhưng 100% terminal (status 0:1, 1:3365; không có {2,3,5,6}) ⇒ chặn 0 phiếu; in-progress sau duyệt mua nằm ở luồng nhập (Task 2). Cost nếu sai: nếu tồn tại dòng order_request2 ở trạng thái 2/3/5/6 trong tương lai sẽ không chặn ở buy-flow — nhưng luồng nhập vẫn bắt. Khớp ruling #5 design §5.
- Index: `root_order_request_products.product_id` KHÔNG có index (full-scan nhẹ khi EXISTS) — không tự thêm migration vào bảng ERP; nêu ở báo cáo. inland + order_request_product2 có index.

Task 2 Step 1 (xác minh const/nhãn trạng thái phiếu nhập, 2026-11-25) — KIỂM TỚI GỐC (const model + nhãn blade + phân bố DB thật):
- YCNH `product_import_requests` (const `ProductImportRequest`): terminal {5 DA_HACH_TOAN, 6 DA_HUY_PHIEU, 8 DA_NHAP_KHO} → chặn {1,2,3,4,7,9,10,11,12}. ✓ khớp design.
- ĐNNK `warehouse_import_requests` (nhãn blade index): 1 Đang nhập kho, 2 Chờ duyệt, 3 Đang tạo, 4 Đã hạch toán, 5 Đã hủy, 6 Đã nhập kho, 7 Đang hạch toán → terminal {4,5,6}, chặn {1,2,3,7}. ✓ khớp design.
- PNK `warehouse_imports` (nhãn blade index): 1 Đã hạch toán, 2 Chờ duyệt, 3 Đang tạo, 4 Không duyệt, 5 Đã xuất lại, 6 Đã nhập lại, 7 Đang hạch toán, +8 Hủy(DB) → terminal {1,4,8}, chặn {2,3,5,6,7}. ✓ khớp design (5/6 coi là in-progress: chu kỳ xuất lại/nhập lại chưa về hạch toán).
- Phiếu nhập hàng `product_imports` (nhãn blade): 1 Đã hoàn thành, 3 Đang tạo → terminal {1}, chặn {3}. ✓.
- Nhập ĐC kiểm kê `inventory_discrepancy_handling_imports` (const): DANG_TAO=1, DA_GUI_NCC=2, KHONG_DUYET=3, CHO_DUYET=4, DA_DUYET=5 → terminal {3,5}, chặn {1,2,4}. ✓.
- Ruling: BỎ `order_import_requests` khỏi guard nhập. Lý do: bảng KHÔNG có `company_id`; `warehouse_id` NULL 193/634 (và 2/3 dòng in-progress status=3 cũng NULL warehouse) ⇒ scope theo kho bỏ sót, scope theo `created_by` thì gán theo cty gốc người lập (trái CurrentCompany, chặn chéo cty). Nhãn status {1 Đã duyệt, 2 Chờ duyệt, 3 Đang tạo}: 1 (634 dòng) = đã duyệt→chuyển tiếp sang phiếu nhập downstream đã nằm trong guard (ruling #5 → terminal); chỉ còn {2,3}=3 dòng in-progress toàn hệ thống, bản chất là đặt-hàng-nhập (giao thoa luồng mua). Cost nếu sai: 1 phiếu đặt hàng nhập nháp (status 3) không chặn khóa — hiếm & thường product đó còn nằm phiếu mua/nhập khác. → guard nhập = 5 phiếu.

Task 2 complete (2026-11-25): viết `existsImportInProgress()` — 5 khối whereExists (YCNH {1,2,3,4,7,9,10,11,12}, ĐNNK {1,2,3,7}, PNK lot d.company_id {2,3,5,6,7}, Phiếu nhập hàng {3}, Nhập ĐC kiểm kê {1,2,4}; order_import_requests bỏ). Probe READ-ONLY: YCNH st4→true, ĐNNK st1→true, PNK st6(lot)→true (st3 không có lô), Nhập hàng st3→true, Nhập ĐCKK st2→true, NEG (chỉ product_imports st1, không phiếu khác)→false. Khớp Expected. Chưa commit.

Task 3 Step 1 (xác minh const/nhãn phiếu xuất, 2026-11-25) — KIỂM TỚI GỐC (const + STATUSES model + nhãn blade + phân bố DB):
- YCXH `product_export_requests` (const `ProductExportRequest` 1-19): terminal {5 đã hạch toán,6 đã hủy,8 đã xuất kho,13 đã quyết toán} → `whereNotIn([5,6,8,13])`. Dữ liệu: {1:117,2:26,3:333,4:54,5:33868,6:993,7:35,8:112,9:3,10:1,11:2}.
- Ruling YCXH 8/12: dùng quy ước terminal THỐNG NHẤT của design (8 "đã xuất kho"=xuất hoàn tất→terminal, nhất quán luồng nhập YCNH 8; 12 "đang quyết toán"→chặn). KHÔNG dùng `ProductExportRequest::STATUS_PROCESING` (ERP phân loại ngược: 8 chặn/12 terminal) vì hằng số đó KHÔNG được tham chiếu ở đâu trong `app/` ERP (grep 1 hit = chính định nghĩa). Cost nếu sai: khác biệt chỉ ở status 8 & 12; DB hiện KHÔNG có dòng status 12/14-19, status 8=112 dòng coi là terminal (hàng đã rời kho, khóa hàng chỉ chặn chứng từ MỚI nên an toàn).
- ĐNXK `warehouse_export_requests` (nhãn blade): 1 Đang xuất kho,2 Chờ duyệt,3 Đang tạo,4 Đã hạch toán,5 Đã hủy,6 Đã xuất kho,7 Đang hạch toán + cột `is_complete` → chặn {1,2,3,7} AND is_complete<>1; terminal {4,5,6}/is_complete=1. is_complete {1:30627,0:330}.
- PXK `warehouse_exports` (nhãn blade): 1 Đã hạch toán,2 Chờ duyệt,3 Đang tạo,4 Không duyệt,5 Đã nhập lại,6 Đã xuất lại,7 Đang hạch toán,+8 Hủy(DB) → terminal {1,4,8}, chặn {2,3,5,6,7} (nhất quán PNK luồng nhập). Scope qua lot d.company_id.
- YC chuyển hàng `product_transfer_requests` (STATUSES const): 1 Đã tiếp nhận,2 Chờ duyệt,3 Đang tạo,4 Đang đề nghị,14 Đã đề nghị,5 Đang xuất kho,6 Đã xuất kho,7 Đang vận chuyển,8/9 Đang nhập kho,10 Đã nhập kho,11 Đã nhập hàng,12 Đã phân bổ,13 Đã hủy → terminal {10,11,12,13}, chặn {1,2,3,4,5,6,7,8,9,14}. company_id đơn (cty lập). DB: {1:76,2:24,3:159,4:56,5:20,7:8,8:3,9:11,11:1159,12:1610}.
- Xuất ĐC kiểm kê `inventory_exports`: DANG_TAO=3, DA_HOAN_THANH=1 → terminal {1}, chặn {3}. Scope chi tiết d.company_id. DB chỉ {1:1} (không dòng st3).
- PXH `product_exports` KHÔNG tính (ruling design §PXH).

Task 3 complete (2026-11-25): viết `existsExportInProgress()` — 5 khối whereExists (YCXH whereNotIn[5,6,8,13] h.company_id; ĐNXK {1,2,3,7}+is_complete<>1 h.company_id; PXK lot d.company_id {2,3,5,6,7}; Transfer {1-9,14} h.company_id; InvExport d.company_id st=3). Probe READ-ONLY: YCXH pid31919/cty1→true, ĐNXK pid33846/cty4→true, PXK pid4825/cty4→true, Transfer pid31874/cty2→true, InvExport không mẫu st3 (wiring kiểm bằng st1 test→true), NEG product chỉ ở YCXH terminal→false, NEG product ảo→false. Khớp Expected. Chưa commit.

Task 4 Step 1 (scope công ty HĐ + cột số lượng, 2026-11-25) — KIỂM TỚI GỐC:
- `contracts` & `service_contracts` KHÔNG có cột `company_id` (chỉ `company_account_*` = TK ngân hàng, + `created_by`/`department_id`). `project_contracts` CÓ `company_id`.
- Cơ chế gốc ERP: `App\Services\Product\DocumentCompany::of()` khai `NO_COMPANY_TABLES=['contracts','project_quotations','order_requests','combo_campaigns','tmp_products']` → suy công ty từ NGƯỜI LẬP `created_by` → `Employee::companyIdOf()` = `employees.employee_info_id` → `employee_infos.company_id`. App\Contract.php dòng 713-714 dùng chính cơ chế này cho đọc giá. → Ruling: scope `contracts`/`service_contracts` qua join `employees`+`employee_infos` theo `created_by`; `project_contracts` lọc `company_id` thẳng. Join path xác minh DB gộp: employees.employee_info_id OK, employee_infos.company_id OK.
- Cột số lượng detail: `contract_products.quantity` (+exported_qty); `service_contract_item_products.qty` (+exported_qty); `project_contract_tab_products.qty` (+exported_qty). "Chưa xuất hết" = (SL - exported_qty) > 0.
- Bảng theo dõi xuất của HĐ vật tư = `contract_products` (KHÔNG phải root_contract_products): relation `Contract::final_products`→`ContractProduct`(table contract_products); `getDataForAnnex` dòng 854 tính còn lại = `(quantity - exported_qty)`; `exported_qty` dùng thật (Contract.php 739/854/3995). root_contract_products = dòng gốc (combo/kit), DB dev rỗng. → Plan chọn contract_products là đúng.
- Ruling công thức "chưa xuất hết": dùng `(quantity - exported_qty) > 0` theo design đã duyệt + khớp `final_products` dòng 854. ERP có 1 chỗ khác (`canHandoverAcceptanceRecord` dòng 3995: `quantity > exported_qty + returned_qty`) nhưng đó là điều kiện NGHIỆM THU, không phải "chưa xuất hết"; bỏ `returned_qty`. Cost nếu sai: product có exported=returned (xuất rồi trả hết phần đã xuất) vẫn bị chặn khóa nếu còn SL chưa xuất — đúng ý "chưa xuất hết".

Task 4 complete (2026-11-25): viết `existsContractInProgress()` — 3 khối: (1) contracts qua contract_products, join employees+employee_infos theo created_by lọc ei.company_id, điều kiện (type1 status∈{6,8}) OR (type3 status=1) OR (type6 status=6), (quantity-exported_qty)>0; (2) service_contracts qua service_contract_item_products, scope qua người lập, status=6, (qty-exported_qty)>0; (3) project_contracts qua project_contract_tab_products, lọc h.company_id, status=6, (qty-exported_qty)>0. Probe READ-ONLY: DB dev chỉ có 1 HĐ type3 status2 (chờ duyệt) → existsContractInProgress=false (đúng: type3 chỉ chặn status=1); wiring block1 (nới status=2, qty>ex, join+scope) → true; NEG product ảo → false; firstBlockingFlow(ảo) → NULL. Khớp Expected. Chưa commit.

Task 1 complete (2026-11-25): tạo `ProductInProgressService` (`Modules/MasterData/Services/Product/`) — scaffold `firstBlockingFlow()` + 4 const FLOW_* + `existsBuyInProgress()` (YCHG qua `PriceAskingProductReader::hasOpenRequest`, inland whereIn{1,2,3,4,6}, root whereIn{1,2,3}; order_request2 bỏ). 3 method còn lại stub `return false`. Probe READ-ONLY: inland p=40238/cty1/st1 → true, root p=18308/cty1/st1 → true, NEG p=999999999 → false, inland st=5(terminal) p=39747 → false. Khớp Expected. Chưa commit (rule HRM).

Task 5 complete (2026-11-25): viết orchestrator + chèn guard vào `lock()`.
- `ProductInProgressService::firstBlockingFlow()` đã có (scaffold Task 1), khớp plan: xét mua→nhập→xuất→HĐ, trả luồng đầu tiên, null nếu sạch.
- `ProductLifecycleService`: thêm 4 const MESSAGE_IN_PROGRESS_{BUY,IMPORT,EXPORT,CONTRACT} + map const `IN_PROGRESS_MESSAGES` (FLOW_* → câu); inject `ProductInProgressService` qua constructor (thêm tham số thứ 4, container tự resolve); chèn guard sau check STATUS_TRADING, trước setStatus: `$flow = firstBlockingFlow(id, companyId()); if($flow) fail(IN_PROGRESS_MESSAGES[$flow]);`.
- Lint sạch 2 file. php artisan test ProductImportPriceTest = 26/26 PASS (regression: constructor 4 tham số không vỡ — test dùng app() + Mockery partial).
- KIỂM TỚI GỐC — auth guard: `TpEmployee::getCurrentCompanyRoleAttribute` đọc `auth()->user()` = guard MẶC ĐỊNH (api), KHÔNG phải `web`. (Các probe trước set nhầm `Auth::guard("web")` → ccr/quyền rỗng là ARTIFACT, không phải RBAC chưa convert.) Set đúng `auth()->setUser(TpEmployee::find(13))` → ccr=1, có quyền `master_data.thong_tin_hang_hoa.manage`.
- END-TO-END lock() THẬT (emp13/cty1, qua assertCanWrite + lockAndAssertUsing + guard + fail/setStatus):
  · CASE blocked: product 3907 (export in-progress) → lock() ném HttpResponseException 422, message="Hàng đang trong tiến trình xuất.", status GIỮ 3 (guard chặn trước setStatus). ✓
  · CASE clean: product 3897 (trading, sạch) trong `DB::beginTransaction` → status 3→4, trả payload; `rollBack` → về 3 (KHÔNG mutation tồn dư). ✓
- Map 4 câu verify đủ (reflection IN_PROGRESS_MESSAGES). cty1 chỉ có mẫu trading bị chặn bởi 'export'; buy/import/contract đã verify `exists*`=true ở Task 1/2/4 tại cty khác; guard tra map đồng nhất nên 3 câu còn lại bảo đảm cùng đường.
- Ruling (Playwright thay bằng tinker end-to-end): token e2e sub=1 không tồn tại trong DB local (min employee id=13), nên không đăng nhập UI thật được; thay bằng gọi lock() THẬT qua container đúng auth guard — đi trọn đường HTTP-tương-đương gồm cả assertCanWrite. Cost nếu sai: chưa thấy toast render trên trình duyệt; nhưng message + mã 422 + giữ/đổi status đều đã chứng thực ở tầng service thật. QA xác nhận toast trên môi trường đã convert RBAC.

=== FINAL REVIEW (2026-11-25, reviewer Opus fresh-context, whole branch) ===
Reviewer xác nhận: guard placement/wiring, thứ tự short-circuit, 422, company-scoping, điều kiện HĐ "(quantity-exported_qty)>0", và PHẦN LỚN tập status đều đúng, trace tới gốc. 1 Important + 4 minor/by-design.

Final: fixed [YCXH export status set] — tiến trình xuất YCXH loại nhầm status 8 "Đã xuất kho" vào terminal.
- Re-grade theo hiệu lực: Important (sản phẩm có YCXH đang ở 8 = hàng đã ra kho nhưng HẠCH TOÁN còn treo (8→9 Đang hạch toán→5 Đã hạch toán) vẫn khoá được — lệch nguồn chuẩn ERP; 112 dòng thật).
- KIỂM TỚI GỐC trước khi vá: reviewer đề xuất mirror `ProductExportRequest::STATUS_PROCESING` (loại {5,6,12,13}). grep app/+resources/ ERP: STATUS_PROCESING DORMANT, KHÔNG nơi nào dùng → không đủ tư cách làm chuẩn. Trace vòng đời + usage: status 8 phải CHẶN (giữa luồng); status 12 "Đang quyết toán" cũng phải CHẶN (SettlementContract.php:669 set YCXH=12 khi đang quyết toán = chưa xong) — mirror STATUS_PROCESING sẽ làm HẾT chặn 12 = bug mới. => terminal đúng = CHỈ {5 Đã hạch toán, 6 Đã hủy, 13 Đã quyết toán}.
- Fix: `existsExportInProgress` YCXH `whereNotIn [5,6,8,13]` → `whereNotIn [5,6,13]` + viết lại docblock.
- RED→GREEN (tinker probe thay phpunit theo Global Constraint): product 18943/cty1 (YCXH dist {5:23,6:2,8:1}) — OLD set không chặn (BUG) → NEW set chặn. existsExportInProgress=true, firstBlockingFlow='export'. Virtual pid 999999999 vẫn NULL. Suite ProductImportPriceTest 26/26 PASS.

Final: minor (deferred): tập status ĐNNK/PNK/ĐNXK/PXK/Phiếu nhập hàng suy từ nhãn blade + phân phối DB (các model này không có const status để đối chiếu tuyệt đối). Đã khớp blade+DB; không mâu thuẫn code.
Final: minor (deferred): `root_order_request_products.product_id` không index — chỉ perf, không sửa được (bảng ERP, rule cấm).
Final: Ruling: Transfer/inventory scope theo header company_id (công ty nguồn) — reviewer nêu hàng chuyển SANG công ty hiện tại không bắt ở scope công ty đích — ĐÚNG Ý ĐỒ (công ty nguồn vẫn chặn, khớp mô hình công ty vận hành). Cost nếu sai: công ty đích có thể khoá hàng đang trên đường về; nhưng công ty nguồn còn phiếu mở nên vẫn chặn ở đầu nguồn.
Final: Ruling: company-scope HĐ/HĐ DV theo created_by→employee_infos.company_id (không theo current_company_role người xem) — bám đúng ERP DocumentCompany::of()/Employee::companyIdOf(), là tín hiệu công ty DUY NHẤT các bảng này có (không có cột company_id). Cost nếu sai: HĐ của người tạo khác công ty hiện tại vẫn tính vào — nhưng đó chính là định nghĩa công ty của HĐ bên ERP.

Final review: DONE. Fix committed? CHƯA (rule HRM: không tự commit). Branch develop, 2 file thay đổi (chưa commit).

Commit+push (2026-11-25): commit 5621f7503 "fix(#11924)..." đã rebase lên origin/develop (remote +103 file người khác, KHÔNG đụng 2 file fix) và push. Suite 26/26 + sanity firstBlockingFlow lại xanh trên base mới trước khi push. CHƯA gop_db.
