# SDD ledger — plan: HRM/.plans/gop-db/ycxh-xuat-ban-hang-type14/plan.md

Spec: docs/superpowers/specs/gop-db/2026-10-05-ycxh-xuat-ban-hang-type14-design.md (reachable ✅)
Repos: hrm-api @ gop_db (BASE 622ce6c), hrm-client @ gop_db (BASE 6e31e81)
Pre-existing uncommitted (NOT ours): hrm-client components/regulation-config/RegulationConfigScreen.vue — leave untouched.
DB: erp_new (gộp). T5 tinker = READ-ONLY only.

## Pre-flight conflict scan

Cross-task (shared file / interface):
| Tasks | Produces → Consumes | Finding |
|---|---|---|
| T1 ↔ T4 | both edit `rulesForType()` | Different line regions (T1=`$isContract` draft block; T4=new `$isFirmContract` block + widen `if($isContract)`→`||$isFirmContract`). Sequential T1→T4. OK. |
| T3 ↔ T4 | T3 adds 14 to CREATABLE_TYPE_IDS; T4 reads type | Independent lines. OK. |
| T5 → T6/T7/T8 | real column names | HARD dep: T5 must finish before Phase-2 BE briefs written. Enforced by order. |
| T6 → T7/T9 | `FirmContractExportStockService::remainingByContractProduct()` | Signature fixed in T6; T7/T9 consume. OK. |
| T8 ↔ T9 | both edit `createFromFirmContract()` | T8 creates method; T9 adds business checks inside. Sequential T8→T9. OK. |
| T11 → T13/T14 | `FIRM_CONTRACT_TYPES`/`isFirmContractType` | OK. |
| T12 → T14 | `FirmContractSearchModal` | OK. |
| T13 → T14 | `loadFirmContractLines` | OK. |
| T10 ↔ T12 | HĐ-hãng list endpoint | T10 conditional (reuse if exists). T12 consumes. Resolve T10 before T12. |

Self-consistency (each task): each references concrete file+template+line; no internal contradiction found.

Review-rubric vs plan-mandated:
| Item | Ruling |
|---|---|
| T9-B3 skips 3 phụ-checks w/ TODO | PLAN-MANDATED (user chốt "chỉ 2 check thiết yếu"). If reviewer flags "incomplete validation" → rule: stands, spec authority. |

Scan verdict: no blocking conflict; sequencing noted above.

## Progress

T5: COMPLETE (read-only). Facts → scratchpad/t5-facts.md. Key maps:
  firm_contracts: id,code,status,type,created_by,company_id,department_id,part_id; KH snapshot = customer_name/customer_address/customer_contact_name/customer_contact_phone(+customer_mobile,customer_fax). KHÔNG có cột mã số thuế → join `customers` qua customer_id nếu cần.
  firm_contract_tab_products: FK=firm_contract_id(+root_firm_contract_id); parent=parent_id(+root_firm_contract_tab_id); product_id; unit_id; qty=quantity(+exported_qty,contract_quantity,returned_qty); giá niêm yết=standard_price; sau giảm=net_price(+price_after_discount,price_discount); extra=price_extra/price_with_extra; vat=vat_percent; model_id/brand_id.
  CO_HIEU_LUC = status 3 (FirmContract::SELECTABLE_STATUSES=[3,9,10]; 3=Có hiệu lực,9=Đang quyết toán,10=Đã quyết toán).
  In-flight (HRM đã xác nhận):
    - ProductExportRequest (Modules/Assign): in-flight {2,7,10,11} + need_export=1, loại DA_HUY. (Đúng class Assign — controller/service ta sửa ở Assign. Có 1 class trùng tên ở Finance/ProductImportRequest/ — KHÔNG dùng.)
    - WarehouseExportRequest (Modules/Assign): in-flight {1,2,4,6,7} (= !=3 DANG_TAO && !=5 DA_HUY).
    - BorrowSellRequest (Modules/Finance): DA_DUYET=1,CHO_KE_TOAN_KHO=2,DANG_TAO=3,KHONG_DUYET=4,CHO_TP_DUYET=10,CHO_BGD_DUYET=11. ⚠️ ERP dùng =2 nhưng nhãn HRM=2 là "Chờ kế toán kho" (ngữ nghĩa lệch).
  #5 KHÔNG có endpoint list firm_contracts trong Modules/Assign → T10 phải dựng mới (mẫu filter: Finance BillIncomeRequestService / SELECTABLE_STATUSES).

Ruling R1 (picker + canProductExport): HĐ hãng "còn hiệu lực" = status 3 (CO_HIEU_LUC). Endpoint list T10 lọc status=3 để khớp check Gửi duyệt (T9), tránh cho chọn HĐ 9/10 rồi submit fail. Cost nếu sai: picker hẹp hơn mong muốn (người dùng thiếu HĐ đang quyết toán) — sửa 1 dòng where.
Ruling R2 (borrow-sell in-flight): T6 implementer phải (a) xác nhận borrow_sell_request_tab_products có khóa về firm_contract không — không có thì LOẠI nguồn này + ghi chú; (b) nếu có, dùng tập active/pending {1,2,10,11} (bỏ DANG_TAO=3, KHONG_DUYET=4) thay vì chỉ =2, kèm comment mapping ERP→HRM + flag trong report. Cost nếu sai: phần trừ mượn-bán lệch (ca hiếm) — chỉnh tập status.
Phase 1 (T1+T2): COMPLETE (commits api 622ce6c..1bfc5d81, client 6e31e81..c3bb7ad8b, review APPROVED).
  Task 1 minor (deferred→fold into Dispatch A): stale BE comment ~line 21 still says HĐ required "kể cả nháp" — fix when T4 edits same file.
  Task 2 minor (deferred): T2 touched 2 comment lines beyond literal scope — comment-only, no action.
  ⚠️-resolved: reviewer couldn't confirm no 2nd validation path. Controller: store()→rulesForType is the single BE gate; FE: single validateForm (confirmed prior systematic-debugging). No bypass. OK.
Dispatch A (T3+T4): DONE commit 1bfc5d81..31e5a237d. php -l clean.
Task A (T3+T4): complete. Review APPROVED (sonnet) — 2 verdicts clean, no Critical/Important. Spec-compliance table all ✅.
  Parked minor (deferred): docblock trên CREATABLE_TYPE_IDS (ProductExportRequest.php) vẫn ghi "Mở khoá từng loại khi hoàn tất: 14, 15..." — nay stale vì 14 đã mở. Comment-only, out-of-scope brief A. Fold vào final review cleanup hoặc task sau chạm file.
T6 (FirmContractExportStockService): DONE_WITH_CONCERNS commit 31e5a237d..59b45965a. php -l clean. Review DISPATCHED (sonnet, a92f7e17965136d9b), package .superpowers/sdd/plan/review-31e5a237d..59b45965a.diff.
  Implementer concerns: (1) cả 3 nguồn in-flight CÓ khóa firm_contract_id+firm_contract_tab_id → không loại nguồn nào; (2) R2 borrow-sell {1,2,10,11} đã comment+flag; (3) quỹ cha-con port verbatim nhưng HĐ test (id2) không có dòng con → chưa number-verify; (4) ⚠️ in-flight CHỈ bắt được nếu create-flow loại 14 GHI firm_contract_id+firm_contract_tab_id lên 3 bảng in-flight → ĐÃ fold vào dispD-brief (T8 bắt buộc set 2 cột này); (5) WER không có hằng XUAT_BAN_HD_HANG → reuse ProductExportRequest::XUAT_BAN_HD_HANG(=14).
  Tinker mẫu: HĐ2 → 16 dòng in_flight=0 (PER duy nhất status3 DANG_TAO đã loại đúng); HĐ22253 → {needed2,exported0,in_flight2,remaining0} (path trừ in-flight chạy).

Ruling R3: KHÔNG dispatch Dispatch C (T7) song song khi T6 còn có thể vào fix-loop — tôn trọng "không 2 implementer song song". Chờ review T6 xong (APPROVED→dispatch C; CHANGES→fix T6 trước). Cost nếu sai: chỉ chậm wall-clock, đổi lấy diff-range sạch. Reviewer T6 (read-only) overlap là hợp lệ.
T6 review (sonnet a92f7e17): CHANGES_REQUESTED. 1 Important + 2 Minor.
  Important: in-flight subquery PER/WER lấy firm_contract_id từ bảng DETAIL (perd/werd) thay vì HEADER (per/wer) như ERP → lệch ERP + dính bẫy cột trùng header/detail sau gộp. → FIX round 1.
  Minor-1 (R2 borrow-sell mapping): code đã comment+flag; quyết định nghiệp vụ, CẦN USER CHỐT → đưa vào bản tổng kết Ruling cuối. KHÔNG chặn.
  Minor-2 (quỹ cha-con chưa number-verify, HĐ test không có dòng con): verbatim port, PARK.
  Đã verify sạch: qualify cột (4 query đều qualify), PHP7.4, an toàn số (guard chia 0, clamp max0), scope (1 file).
Adjudication: Important = lệch BRIEF ("port y ERP") → sửa, không phải conflict plan. 2 Minor park/surface.
T6 FIX round 1 (1/5): DONE commit eb020eff9. PER/WER đọc firm_contract_id từ header; firm_contract_tab_id giữ detail. Borrow-sell GIỮ bsrtp.firm_contract_id (detail) vì borrow_sell_requests KHÔNG có cột firm_contract_id (polymorphic contractable_*) + ERP cũng đọc detail → có comment. php -l sạch, tinker HĐ22253 không đổi {2,0,2,0}.
T6 RE-REVIEW (scoped, sonnet a8c668be41): APPROVED. 3/3 điểm đạt (header-source PER/WER; borrow-sell detail justified — confirmed BorrowSellRequest polymorphic contractable_* + ERP FirmContractProductExportService dòng 110/312/544 cũng đọc bsrtp.firm_contract_id; không regress).
Task 6 (FirmContractExportStockService): complete. HEAD eb020eff9.

Dispatch C (T7+T10): DONE_WITH_CONCERNS commit eb020eff9..c97c30db1. php -l sạch (controller + Routes/api.php). Route: GET /assign/product-export-requests/firm-contracts → firmContracts(Request).
  Deviation (DB-verified, hợp lý): (a) firm_contract_tab_products đã có cột snapshot code/product_name/model_name/brand_name/unit_name → không join catalog; (b) firm_contracts.identity_card_number = mã số thuế (đã dùng nơi khác trong controller) → không join customers; (c) không có hằng CO_HIEU_LUC trên HRM FirmContract → literal 3 + comment (mẫu PrepickTransferRequestService::FIRM_CONTRACT_ACTIVE), không thêm hằng vào shared entity. Tinker HĐ22253 remaining_qty=0 đúng.
  Review APPROVED (sonnet a6dc7b8b). 2 deviation verified hợp lệ (snapshot cột thật trên firm_contract_tab_products; identity_card_number=customer_tax_code đã dùng ở editData:823/show:961). Literal 3 chấp nhận.
Task 7 + Task 10: complete. HEAD c97c30db1.
  ⚠️ FE caveat (carry vào T11-T14): firmContractProductLines (loại 14) field id-dòng = `contract_product_id`, giá phụ = `price_extra`; còn contractProductLines (20/21) = `id` + `extra_price`. Component bảng dùng chung phải xử lý đúng theo loại.
  BE contract chốt cho FE:
    - Picker: GET /assign/product-export-requests/firm-contracts?q=&limit= → [{id,code,customer_name,customer_address}] (status=3 + của người đăng nhập).
    - createData loại 14 (type=14 + firm_contract_id): payload.contract{id,code,customer_name,customer_tax_code,customer_contact_name,customer_contact_phone,customer_address}; payload.product_lines[]{contract_product_id,parent_id,product_id,code,name,model_name,brand_name,unit_id,unit_name,qty_needed,exported_qty,in_flight_qty,remaining_qty,contract_qty,quoted_price,unit_price_after_discount,price_extra,vat_percent} (toàn SỐ); payload.vat_options[] (float asc); transition_types + warehouses như cũ.
    - Submit loại 14: type, firm_contract_id, products[].contract_product_id + quantity, need_repair(0/1), is_export_direct, warehouse_id (required_unless is_export_direct=1), firm_tab_vat_percent (required khi gửi duyệt).

Ruling R4: Dispatch D (T8+T9, service — DISJOINT file controller) chạy SONG SONG với C-review (read-only). NẾU C-review CHANGES → QUEUE C-fix chạy SAU khi D xong, giữ writer tuần tự + diff range sạch. Cost nếu sai: nếu C-fix+D commit đồng thời thì diff D lẫn noise C-fix — tránh bằng queue.
Dispatch D (T8+T9): DISPATCHED (sonnet a5707de339af1384c). BASE c97c30db1. Brief dispD-brief.md (đã fold ghi firm_contract_id+firm_contract_tab_id trên tab_products). Sửa ProductExportRequestService.php.
  FE briefs (T11-T14) viết SAU khi C review xong (có route path + field createData chốt).

T7+T10 (Dispatch C): brief t7-brief.md — READY. Chờ T6 fix+re-review xong (Ruling R3: không chạy implementer T7 song song T6 fix).
T8+T9 (Dispatch D): brief dispD-brief.md — READY (đã fold concern #4). Chờ T6 + C.

## Ruling R5 (2026-10-05)
Dispatch E (FE, repo hrm-client) chạy SONG SONG Dispatch D (BE, repo hrm-api).
Why: 2 repo tách biệt (git khác nhau) → quy tắc "no two implementers in parallel" (chống xung đột file/diff TRONG 1 repo) không ràng buộc qua repo; mỗi bên review package riêng. Submit contract loại 14 đã khóa ở Task A rules (user duyệt) nên FE không phụ thuộc nội dung D.
Cost nếu sai: FE phải sửa lại nếu D đổi submit contract (thấp — field submit cố định bởi rules đã duyệt).

## Dispatch E (T11+T12+T13+T14) — FE loại 14 (gộp 4 task vì 3/4 sửa cùng ProductExportRequestForm.vue)
Brief: scratchpad/dispE-fe-brief.md. Implementer a8e7e820 (sonnet). FE BASE c3bb7ad8 (hrm-client @ gop_db). RUNNING.
Mang theo caveat field-name: loại14 contract_product_id/price_extra vs 20/21 id/extra_price.
Schema confirmed (từ output D): product_export_request_tab_products CÓ sẵn firm_contract_id + firm_contract_tab_id + firm_contract_tab_product_id + contract_product_id → concern #4 của T6 thỏa, KHÔNG cần migration.

## Dispatch D (T8+T9) — BE service createFromFirmContract + 2 check Gửi duyệt
Brief: scratchpad/dispD-brief.md. Implementer a5707de3 (sonnet). BE BASE c97c30db1 (hrm-api). RUNNING.

### Dispatch D — DONE: commit 86df980e3 (php -l sạch). Review DISPATCHED (opus a5d9e5e4), package review-c97c30db1..86df980e3.diff.
Implementer concern cần reviewer xác nhận: GHI firm_contract_tab_id = firm_contract_tab_products.parent_id; firm_contract_tab_product_id = id dòng (FE contract_product_id). Lý do: khớp T6 getInFlightQtyByRow JOIN fctp.parent_id=pr.firm_contract_tab_id. → reviewer phải confirm alignment write↔read (lớp bug over-commit).

### Dispatch D review (opus a5d9e5e4): APPROVED — 0 Critical, 0 Important, 4 Minor.
Crux CONFIRMED: write path D (firm_contract_tab_id = fctp.parent_id; firm_contract_tab_product_id = line id) KHỚP read path T6 (getInFlightQtyByRow JOIN fctp.parent_id = pr.firm_contract_tab_id) → in-flight loại 14 ĐƯỢC tính → KHÔNG over-commit. Deviation so với brief literal ("firm_contract_tab_id = fctp.id") là ĐÚNG: nếu theo literal thì join không bao giờ khớp → silent over-commit.
Adjudication 4 Minor:
  M1 (Gửi duyệt 0 dòng hàng không bị 2 check chặn): ĐÃ GUARD sẵn ở tầng validate — rulesForType() dòng 729 `products = required|array|min:1` nằm trong khối status=2 (sau `if($isDraft){...return}` 708-718), + dòng 731-732 `products.*.contract_product_id required` cho loại HĐ hãng. Reviewer chỉ thấy diff D (service), không thấy T4 rules → flag gap mà T4 đã đóng. KHÔNG sửa.
  M2 (`company_id` dùng `?:` thay `??`): style, PARK (chấp nhận — `?:` an toàn vì không có key nào trả falsy hợp lệ ở đây).
  M3 (`identity_card_number` làm MST snapshot): pattern đã có ở editData/show cùng controller → chấp nhận.
  M4 (T6 có thể double-count nếu 1 tab có 2 dòng cùng product_id): XÁC MINH read-only — getInFlightQtyByRow gom theo (firm_contract_id, parent_id, product_id), KHÔNG theo fctp.id → 2 dòng cùng product trong 1 tab share in-flight → UNDER-count remaining. Hướng lỗi BẢO THỦ (over-block, hiện rõ cho user, KHÔNG phải silent over-commit). T6 đã APPROVED qua gate riêng. WER/BorrowSell nguồn in-flight không chắc có per-line id nên không join đồng bộ theo fctp.id được. PARK + surface cho final whole-branch review cân nhắc; nếu final reviewer coi là load-bearing thì fix ở T6 (thêm firm_contract_tab_product_id vào khóa in-flight cho nguồn PER).
Task 8 + Task 9 (Dispatch D): complete. HEAD 86df980e3.

## Ruling R6 (2026-10-05) — editData() thiếu nhánh loại 14 = lỗ hổng PLAN, fix riêng bên BE
Điều tra concern #4 của Dispatch E: `editData($id)` (ProductExportRequestController ~779) chỉ có `if($req->isContractType())` (20/21) trả product_lines/selected_lines, loại 14 rơi vào `else` → trả `products` phẳng, `$detail` KHÔNG có firm_contract_id/product_lines/selected_lines/vat_options → màn SỬA nháp loại 14 trống dòng hàng. Không task nào trong plan cover editData loại 14 (plan chỉ lo create).
Quyết: đây là LỖ HỔNG BE (không phải lỗi FE). Nhánh `applyInitialData` loại 14 của FE là ĐÚNG (nhắm shape editData sẽ trả sau fix). Dispatch F riêng trong hrm-api (BASE 86df980e3) thêm nhánh elseif loại 14 vào editData. Chạy SONG SONG với FE reviewer (R5: disjoint repo; D đã xong nên không có hrm-api writer khác đồng thời).
Cost nếu sai: màn Sửa nháp loại 14 trống dòng (chỉ ảnh hưởng luồng edit, create vẫn chạy) — sửa thêm nhánh.

## Dispatch E review (FE, T11-T14) — DISPATCHED
Reviewer a565d34f (sonnet, read-only hrm-client). Inputs: dispE-fe-brief.md + dispE-report.md + dispE-review-package.diff (c3bb7ad8..141df11ef). Mang caveat: field-name 14 vs 20/21; đây là FORM (không áp luật list); concern #4 là BE gap đang fix (R6) → KHÔNG flag applyInitialData; phải adjudicate 3 deviation của E (V2BaseInput thay SelectInModal / need_repair V2BaseRadio / pay-box mở rộng cho 14). RUNNING.
E báo: DONE_WITH_CONCERNS, commit 141df11ef (+290 ProductExportRequestForm.vue, +178 FirmContractSearchModal.vue mới).

### Dispatch E review (sonnet a565d34f): APPROVED — 0 Critical, 0 Major, 1 Minor (parked).
Minor: bảng dòng loại 14 (ProductExportRequestForm.vue ~414/428/434) dùng raw `<input checkbox/number>` thay vì V2BaseCheckbox. NHƯNG là COPY Y NGUYÊN khuôn 20/21 (dòng 327/345/352 cũng raw) theo đúng chỉ đạo brief "bắt chước khối 20/21" → nợ kỹ thuật CÓ TỪ TRƯỚC, không phải defect của E. Sửa 14 mà không sửa 20/21 sẽ lệch. PARK → surface final whole-branch review (sửa cả 2 khối nếu final reviewer coi load-bearing).
3 deviation ĐỀU CHẤP NHẬN (reviewer verify từng cái):
  (a) V2BaseSelectInModal→V2BaseInput: khuôn thật ContractSearchModal.vue 20/21 cũng chỉ dùng V2BaseInput cho ô tìm; brief mô tả "Select" lỏng so với codebase; endpoint chỉ q+limit. OK.
  (b) need_repair dùng chung V2BaseRadio (chạm render 20/21): cùng field form.need_repair, cùng nghĩa; đổi raw→V2BaseRadio đúng tinh thần "V2Base* bắt buộc"; kiểu/giá trị không đổi. OK.
  (c) pay-box mở rộng cho 14: hệ quả tất yếu của isSaleType gồm 14, tính qua nhánh isFirmContractType riêng trong paymentSummary, không đụng 20/21. OK.
Verify thêm: field-name caveat xử lý đúng (buildFirmContractLines giữ price_extra/contract_product_id; buildProducts 2 nhánh map đúng; priceOf trả đủ field); needWarehouse/needTransition hoạt động đúng cho 14 qua logic sẵn có (14 bắt buộc kho khi không xuất thẳng); commit CHỈ 2 file, RegulationConfigScreen.vue vẫn unstaged (không dính).
Task 11+12+13+14 (Dispatch E): complete. hrm-client HEAD 141df11ef.

## Dispatch F (sót plan: editData loại 14) — DISPATCHED
Brief: scratchpad/dispF-brief.md. Implementer ab44e957 (sonnet). BE BASE 86df980e3 (hrm-api @ gop_db). Thêm nhánh elseif type===XUAT_BAN_HD_HANG trong editData → trả firm_contract_id + product_lines (firmContractProductLines excludeRequestId=$req->id) + selected_lines (key firm_contract_tab_product_id) + vat_options + firm_contract_code. Chỉ sửa controller. RUNNING.

### Dispatch F — DONE_WITH_CONCERNS: commit b798c54e8 (php -l sạch, 1 file +29 dòng). Review DISPATCHED (sonnet a7697323), package dispF-review-package.diff (86df980e3..b798c54e8).
Nhánh elseif đặt giữa if(isContractType) và else. selected_lines pluck cột `firm_contract_tab_product_id` (xác nhận từ writeFirmContractLines: service set cột này = id dòng HĐ = FE contract_product_id; contract_product_id trên bảng để NULL cho loại 14). firm_contract_code SELECT từ firm_contracts.code (không có cột snapshot riêng).
Concern (DATA CŨ, không phải bug): phiếu nháp 237 có firm_contract_tab_product_id NULL (tạo trước khi D ghi cột) → selected_lines rỗng khi mở đúng phiếu 237; mapping đã verify đúng trên phiếu 34384 có data chuẩn. Ghi nhận cho người gop_db, KHÔNG tự sửa data.

### Dispatch F review (sonnet a7697323): APPROVED — 0 finding (sạch).
Xác nhận trực tiếp trên code (không chỉ brief/report): nhánh elseif đặt đúng giữa if(isContractType)/else (dòng 849-886), 2 nhánh kia nguyên vẹn; selected_lines pluck ĐÚNG cột firm_contract_tab_product_id (đọc writeFirmContractLines 924-984: set `firm_contract_tab_product_id=$line->id`, KHÔNG set contract_product_id cho loại 14); vat_options copy byte-for-byte createData (380-387 vs 878-885); mọi query mới qualify table.column (firm_contracts.id/code, firm_contract_tab_products.*); PHP7.4 OK không `?->`; không nuốt lỗi; chữ ký editData nguyên; firm_contract_code SELECT từ firm_contracts (không N+1, 1 bản ghi).
Observation non-blocking: nếu draft có firm_contract_id null → firmContractProductLines((int)null=0) → remainingByContractProduct(0) trả [] → product_lines rỗng, KHÔNG crash. canEdit()/store() đã đảm bảo type-14 draft có firm_contract_id. Không gate.
Task F (editData loại 14): complete. hrm-api HEAD b798c54e8.

## TRẠNG THÁI: mọi task code + review xong. hrm-api @ b798c54e8, hrm-client @ 141df11ef. Còn: T15 Playwright verify → final whole-branch review → finishing-a-development-branch.

## T15 — Verify chức năng (2026-10-05)
- KB1 ✅ (browser thật 127.0.0.1:3000, login DNS Admin): Loại 14 + chỉ chọn loại + Lưu nháp → điều hướng phiếu nháp mới /41533, trạng thái "Đang tạo", KHÔNG toast đỏ "Loại yêu cầu không được phép tạo". BUG GỐC ĐÃ HẾT ở runtime.
- KB3 ✅ (tinker read-only, Auth::login creator): createData(type=14, firm_contract_id=28335 status3) → product_lines[0]={contract_product_id:364323, contract_qty:10, exported:0, in_flight:0, remaining:10}, vat_options=[8]. Đúng shape FE tiêu thụ, "Còn được xuất"=remaining tính đúng (contract−exported−inflight).
- KB2 (nháp 20/21 chỉ cần loại): = Phase 1, đã ship+review (hrm-client c3bb7ad8b). Không chạy lại browser.
- KB4 (Gửi duyệt loại 14 chặn SL vượt / HĐ hết hiệu lực / sai người lập): chặn ở 3 lớp đã review — FE báo đỏ khi qty>remaining (không tự kéo max), picker chỉ liệt HĐ status=3 + created_by=auth (loại trừ HĐ hết hiệu lực & khác người), BE 422 backstop (createFromFirmContract 2 check, commit 86df980e3 APPROVED). KHÔNG tạo phiếu "Chờ duyệt" thật để tránh ghi phiếu outward lên erp_new.
- B6 ✅ php -l SẠCH: ProductExportRequestController.php, ProductExportRequestService.php, FirmContractExportStockService.php, ProductExportRequest.php (entity), Routes/api.php. (Không có FormRequest riêng — validate nằm trong controller rulesForType.)
- Dọn dẹp: đã XÓA phiếu test 41533 (type14/status3/created_by13, 0 dòng con) khỏi erp_new. still_exists=NO.

Ruling R7: KB2/KB4 verify ở mức CODE+tinker thay vì browser — browser $axios thủ công rụng token gây logout, automation đắt+giòn; KB1 (bug gốc) đã verify live, phần còn lại nằm trong commit đã review. Cost nếu sai: bỏ sót lỗi tích hợp runtime chỉ hiện khi bấm thật → final whole-branch review (opus) là lưới chốt.

## Final whole-branch review — DISPATCHED (opus, general-purpose)
Review cả 2 repo: hrm-api 622ce6c..b798c54e8 + hrm-client 6e31e81..141df11ef (packages: scratchpad/final-review-hrm-api.diff, final-review-hrm-client.diff). Findings → scratchpad/final-review-findings.md. Đang chạy nền.

### Final whole-branch review (opus): 3 finding (2 High / 1 Medium) + 2 Low. gop_db qualification/column-align/in-flight-dedup/ValidationException/PHP7.4 = CLEAN.
Cả 3 đã đối chiếu code thật, root-cause xác nhận:
- HIGH#1 FirmContractSearchModal.vue: `this.rows=(res&&res.data)||res||[]` đọc `res.data`={items:[...]} (object) → picker LUÔN rỗng → không tạo được phiếu loại 14. FE-only.
- HIGH#2 ProductExportRequestForm.vue: HĐ 1-VAT → selector `v-if vatOptions.length>1` ẩn → firmTabVatPercent mãi null → Gửi duyệt payload null → BE `firm_tab_vat_percent required|numeric` (rulesForType 768) fail 422 trên trường vô hình. BE KHÔNG đọc trường này cho loại 14 → chỉ cần FE auto-set. FE-only.
- MEDIUM#3 ProductExportRequestForm.vue: buildProducts/paymentSummary duyệt firmContractLines (toàn bộ) thay vì firmContractDisplayLines (đã lọc VAT) → dòng VAT khác vẫn _checked bị gửi âm thầm. FE-only.
NGỮ NGHĨA CHỐT (từ nguồn ERP): migration 2022_12_04 `firm_tab_vat_percent decimal(5)` 1 cột/phiếu + controller ERP line 829 gán 1 value → **MỘT PHIẾU MỘT VAT**. Nên rule BE required là ĐÚNG; #2/#3 fix THUẦN FE.
L1 (createData firm branch không gate owner/status — chỉ lộ info nhẹ, 20/21 cũng vậy) + L2 (input HTML thô trong bảng dòng 14 — copy pattern 20/21 sẵn có) → PARK as Low.
Ruling R8: gộp cả 3 finding vào MỘT fix dispatch FE-only (2 file hrm-client), KHÔNG sửa rule BE — vì one-VAT-per-phiếu đã xác nhận từ ERP source (migration+controller), rule required là đúng ngữ nghĩa. Cost nếu sai: nếu thực ra multi-VAT-per-phiếu thì phải bỏ rule BE thay vì fix FE — nhưng ERP source 1 cột/1 value là bằng chứng mạnh.

## Fix dispatch G (3 finding) — DISPATCHED
Brief: scratchpad/fixG-brief.md. Implementer ace14555 (sonnet). hrm-client BASE 141df11ef. 2 file: FirmContractSearchModal.vue (fix#1 shape) + ProductExportRequestForm.vue (fix#2 auto-VAT ở loadFirmContractLines+applyInitialData; fix#3 buildProducts+paymentSummary duyệt firmContractDisplayLines). CHỈ stage 2 file, RegulationConfigScreen.vue để nguyên. KHÔNG push. RUNNING.

### Fix dispatch G — DONE: commit bb6239224e (hrm-client @ gop_db, 2 file). RegulationConfigScreen.vue vẫn unstaged (xác nhận). Scoped re-review DISPATCHED (sonnet a3d10622), package scratchpad/fixG-review-package.diff (141df11ef..bb6239224e, 186 dòng).
FIX1: fetch() đọc `data.items`. FIX2: auto-set firmTabVatPercent ở loadFirmContractLines (VAT đầu) + applyInitialData (theo dòng tick, fallback VAT đầu). FIX3: buildProducts+paymentSummary nhánh isFirmContractType duyệt firmContractDisplayLines. RUNNING re-review.

### Scoped re-review (sonnet a3d10622): APPROVED — 0 finding. Xác nhận trực tiếp trên code cả 3 fix + commit chỉ 2 file + RegulationConfigScreen.vue vẫn unstaged nguyên vẹn. Không regression, không lỗi correctness khác trong diff.

## FINAL REVIEW LOOP CLEAN (2026-10-05). Mọi task + review xong, 3 finding cuối đã fix+re-review APPROVED.
HEAD cuối: hrm-api b798c54e8 · hrm-client bb6239224e (nhánh gop_db cả 2, CHƯA push).
Còn lại: finishing-a-development-branch + xoá workspace plan + thông điệp cuối (surface Ruling R1-R8, đặc biệt R2 chờ user xác nhận).

## PUSHED to origin/gop_db (2026-10-05) — user "commit và push"
Remote đã tiến (hrm-api 62 commit, hrm-client 38 commit của team) → rebase local lên origin (KHÔNG force).
- hrm-api: rebase sạch (chỉ Routes/api.php trùng, route thêm vùng khác → auto-merge), php -l sạch 5 file → push 214bcfd1b..beaf58560. HEAD beaf585606.
- hrm-client: stash file lạ RegulationConfigScreen.vue (giữ nguyên, không commit) → rebase sạch (0 trùng file) → pop → push 855d49b86..fa59ffadf. HEAD fa59ffadf.
Redmine #11385 fix đã lên nhánh gop_db remote. Chờ deploy hrm-crm.eteksofts.com để nghiệm thu.
