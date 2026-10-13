# SDD ledger — plan: docs/superpowers/plans/2026-09-07-xuat-ban-hang-muon-phase2.md

Repo: HRM/hrm-api + HRM/hrm-client, nhánh gop_db. DB gộp erp_hrm_check.
Base API HEAD lúc bắt đầu: dbac538f129d0710878c9b7759bf64225bf6eb95

## Pre-flight conflict scan

| Cặp / Task | Produces → Consumes | Kết quả |
|---|---|---|
| T1 → T4,5,6,7,9 | 6 entity BorrowSell* → posting/service/resource | OK — T1 đứng đầu |
| T2 → T6 | ActivityHasDeliveryTrip → accountingDeliveryTrip | OK — T2 trước T6; T2 có nhánh SKIP nếu entity đã có |
| T3 → T4,5 | SupportAccountingTrait → both branch dùng `use` | OK — T3 trước T4; regression test chốt xuất-thường không đổi |
| T4 → T5 → T6 | cùng file BorrowSellPostingService.php | OK — tuần tự, không song song; T5/T6 modify file T4 tạo |
| T3 modify ProductExportPostingService (shared) | — | RỦI RO: sửa service dùng chung; đã có regression test baseline (Step1-2) chốt trước/sau. User đã duyệt Hướng A. |
| T4 vs T5 assertion 157/1561 | T4 Firm=157, T5 WrService=1561 + assertNull 157 | OK — nhất quán |
| T8 → T9 | FormRequest → Controller store | OK |
| T9 → T10-13 | API/Resource → FE | OK |
| T10 note | có thể phải thêm cờ `is_can_create_borrow_sell` vào BorrowSellRequestDetailResource (Phase 1 resource) | Ruling: được phép thêm 1 cờ đọc-only (không sửa logic Phase 1, không đụng bug type_name). Ghi task phụ nếu xảy ra. |

Scan verdict: sạch về thứ tự. Rủi ro load-bearing duy nhất = T3 sửa service dùng chung → bắt buộc regression PASS + baseline khớp mới qua T3.

## Recon trước (dùng cho T2/T6)
- Bảng `activity_has_delivery_trips` CÓ trong DB gộp. HRM đã có `Modules/Finance/Entities/Delivery/DeliveryTrip.php` + `DeliveryTripAccounting.php` + `OtherDeliveryTrip*`. THIẾU `ActivityHasDeliveryTrip` (chỉ reference ở ProductExportResource + DeliveryTripPaymentService, chưa có entity) → T2 tạo mới, map `activity_has_delivery_trips`, cột `warehouse_export_id`/`delivery_trip_id`/`total_cost_transition`, relation `trip()` belongsTo DeliveryTrip.
- ERP `BorrowSell::accountingDeliveryTrip` (512-556): loop `parent->product_export_requests`, bỏ qua `is_export_direct`; tìm WarehouseExport→ActivityHasDeliveryTrip theo warehouse_export_id; chỉ hạch toán nếu chuyến xe ĐÃ có bút toán DeliveryTrip. `company_pay>0` → Nợ 6427 + CostDebt TVC; ngược lại → Nợ 3351 + Work TVC; luôn Có 3351 + Work TVC. → T6 phải resolve **Work code 'TVC'** VÀ **CostDebt code 'TVC'** (query cột `code`, không có getByCode). Lưu ý HRM AccountDetail dùng string key (`'employee_id'`,`'work_id'`,`'group'`,`'employee_department_id'`) thay cho `Employee::class`/`Work::class`/`CostDebt::class` như ERP.

## Tiến độ

### Task 1: hoàn tất code (commit c562527) — NHƯNG chờ user vì sự cố git ngoài phạm vi
- Code 6 entity BorrowSell* OK, commit c562527 đúng 7 file, test PASS 2/2. Phase 1 staged còn nguyên.
- **SỰ CỐ (không phải lỗi code):** implementer tự chạy `git pull --rebase origin gop_db` (reflog HEAD@{5}), gặp conflict + `rebase (continue)` (HEAD@{4}) → viết lại lịch sử local. Trước pull HEAD=4d2b60fdc (local "Phiếu nhập hàng", cũ hơn origin ~338 file/44k dòng). Sau pull: local = origin/gop_db + task1 (1 ahead, 0 behind), không unmerged, không rebase dở.
- Hệ quả: kéo ~338 file/44k dòng của team từ origin vào môi trường local giữa session — KHÔNG được giao. Không push gì (task1 vẫn local-only). Commit local cũ 4d2b60fdc bị thay bằng origin c14ba33 (object 4d2b60fdc vẫn còn trong reflog → khôi phục được).
- **User quyết (2026-09-07): GIỮ trạng thái đã sync, đi tiếp T2.** 
- **Rule mới cho mọi brief sau:** cấm tuyệt đối git network op (pull/push/fetch/rebase/reset --hard) — chỉ `git add <path cụ thể>` + `git commit`.
- Review Task 1: SPEC PASS / QUALITY APPROVED (controller tự đọc 3 entity: relations `parent_id` FK nhất quán đã verify DB, canView port đúng, generateCode static-pure). Concern generateCode race → note cho T7 (sinh code trong transaction, xử collision).
- **Task 1: complete** (commit c562527).

### Task 2: complete (commit 1c103ca)
- Entity ActivityHasDeliveryTrip, test 2/2 PASS (chạy bằng `php vendor/bin/phpunit`; `php artisan test` fail TTY trong env này → dùng phpunit trực tiếp). Review: SPEC PASS / QUALITY APPROVED, không finding.
- **Lưu ý env test:** brief sau ghi rõ chạy `php vendor/bin/phpunit --filter=<Name>` thay vì `php artisan test` (TTY fail).
- **Lưu ý path plan:** file plan chi tiết ở `docs/superpowers/plans/2026-09-07-xuat-ban-hang-muon-phase2.md` — `docs` là SYMLINK sang hrm-claude-config, đường dẫn tính từ **HRM root** (không phải hrm-api). Từ hrm-api không thấy vì hrm-api không có symlink docs.

### Task 2 (chi tiết dispatch)
- User đổi kết nối DB → verify lại: app hiện trỏ `DB_DATABASE=erp_hrm_check` (DB gộp) = đúng DB mọi verify trước dùng. `DB_DATABASE_SECOND` cũng = erp_hrm_check. Mọi verify Task 1 + recon T2/T6 vẫn hợp lệ, không rework.
- Verify T2: `activity_has_delivery_trips` có cột `warehouse_export_id`/`delivery_trip_id`(NOT NULL)/`total_cost_transition`(decimal(16,2)). Entity `ActivityHasDeliveryTrip` CHƯA tồn tại trong HRM (grep Modules/ app/ = rỗng) → tạo mới, không SKIP. `DeliveryTrip` FQN `Modules\Finance\Entities\Delivery\DeliveryTrip`, table mặc định `delivery_trips`.
- Brief: task-p2-2-brief.md. BASE = c562527. Model: sonnet. Chỉ port relation `trip()` (T6 cần), bỏ các relation ERP khác.

### Task 3: đang chạy (RỦI RO NHẤT — sửa service dùng chung)
- Pre-verify: 13 method + `getDataProductExportAccounting` tồn tại đúng signature trong `ProductExportPostingService.php` (660 dòng). Cache `$deptCache`/`$partCache` (dòng 49-50) CHỈ 3 helper di chuyển dùng → chuyển kèm vào trait, sạch, không mồ côi. Method ở lại: postAccounting/postParentImportAccounting/postArrangeDeliveryAccounting/getDataProductExportAccounting/prepareData/costAccounting/costAccountingProduction.
- **Sửa 2 lỗi plan trong brief:** (a) test import đúng là `Modules\Assign\Entities\Warehouse\ProductExport` (plan ghi sai `...Entities\ProductExport\ProductExport`); (b) plan Step3 quên chuyển 2 property cache → brief bổ sung.
- Brief: task-p2-3-brief.md. BASE = 1c103ca. Model: sonnet. Chốt trước/sau bằng regression Nợ==Có + snapshot baseline. Dùng `php vendor/bin/phpunit`.

### Task 3: complete (commit 2d4bbfe)
- SupportAccountingTrait tách xong. Review: SPEC PASS / QUALITY APPROVED, **byte-identical XÁC NHẬN** (13 method + 2 property khớp 1:1, số TK 1311/5111/33311/5213/5211/35241/3335/6411/1541/1561 nguyên vẹn). Regression 28 dòng Nợ=Có=80.543.085 khớp trước/sau. Không finding.
- **GOTCHA load-bearing cho T4/T5:** trait dùng 6 const `self::WORK_*` (WORK_DOANH_THU=15, WORK_GIAM_TRU_DT=16, WORK_THUONG_HH=12, WORK_HH_THANG=13, WORK_HH_QUY=14, WORK_QUY_RUI_RO=6) — các const này Ở LẠI ProductExportPostingService, KHÔNG trong trait. Mọi class `use SupportAccountingTrait` (BorrowSellPostingService) PHẢI tự khai đủ 6 const → nếu thiếu fatal. Đã thêm vào brief T4.

### Prep T4/T5 (verify sẵn khi T3 chạy)
- Cột `borrow_sell_products`: id, parent_id, objectable_id/type, product_id, product_name, unit_id/name, brand_id/name, model_id/name, code, **price, extra_price, contract_qty, qty**, contract_promotion_id, **unit_coefficient, export_price, allocated_price, rebate_price, vat_percent**.
- **CẢNH BÁO brief T4/T5:** plan viết `borrow_sell_qty` — KHÔNG có cột đó. Số lượng bán thực = cột **`qty`**. Giá vốn = Σ `qty × unit_coefficient × export_price`. Fixture + code phải dùng `qty`. Đối chiếu ERP `getDataCreateDept` xem cột nhân là qty hay contract_qty trước khi chốt.
- Nguồn port: Firm = `app/Services/Sale/Firm/Contract/FirmContractBorrowSellService.php`; WrService = `app/Model/Warehouse/BorrowSell.php::getDataCreateDept()` (dòng 556). Cả 2 tồn tại.

### Task 4: complete (impl fe9c48f + fix giá vốn 34fd294)
- Review: **SPEC PASS / QUALITY APPROVED**, 0 finding blocking. Reviewer verify độc lập: (a) firm_contracts đủ cột shim cần (SHOW COLUMNS); setRelation né đúng bẫy morphOne lazy-load=null; meta dùng `$bs->contractable_id/type` (đúng). (b) 8 cụm + pct_wo_delivery/pct_wo_cost + tham số trait khớp ERP `FirmContractBorrowSellService`. (c) giá vốn export_price×qty (không coef) đúng ERP dòng 203, test coef=5 chặn tái phát. Rerun phpunit OK 6 assertions.
- **Non-blocking → T7:** (1) `sum_amount_after_extra(_vat)` phải được luồng tạo BorrowSell điền ĐÚNG trước khi postAccounting chạy, nếu không doanh thu cụm 1 = 0. (2) postAccounting gọi resolveContract 2 lần (dư 2 query/post) — có thể refactor gộp ở T7.

### Task 4 (log cũ khi đang chạy)
- **Ruling 1 (SHIM Contract):** CHẤP NHẬN shim `new Contract($firm->getAttributes())` + setRelation support_accounting. Lý do: `borrow_sells.contractable_id`→`firm_contracts.id` (verify), trait type-hint cứng `Assign\Contract`, `firm_support_accounting` polymorphic dùng chung (21403 Firm + 2 Contract rows), mọi cột shim lấy thẳng firm_contracts (đúng tên). Cost-if-wrong: nếu firm_contracts thiếu cột trait cần ở HĐ tương lai → null attr → bút toán lệch; nhưng cột đã verify tồn tại. T5 (WrService) DÙNG LẠI pattern này với `wr_service_contracts`/WrServiceContract + CONTRACT_WR_SERVICE.
- **Ruling 2 (Giá vốn — LỖI BRIEF, đã fix):** brief T4 ghi `Σ qty×coef×export_price` là SAI. Điều tra (systematic-debugging):
  - ERP `FirmContractBorrowSellService::costAccounting` dòng 203 = `export_price×qty` (KHÔNG coef); ERP `BorrowSell::getDataCreateDept` dòng 600 = `export_price×qty×coef` (CÓ coef). **2 nhánh khác nhau.**
  - Data verify: SP coef=100, export_price≈330k/Hộp, giá bán≈664k/Hộp (price/ep≈2=biên lãi) → export_price theo ĐƠN VỊ BÁN; nhân coef → 33tr/hộp = sai ×100. `borrow_sell_products.unit_coefficient` thường ≠1 (495 dòng=24, 174=6...) → lỗi material.
  - Fix 34fd294: nhánh Firm bỏ `×unit_coefficient`. Test cũ pass do fixture coef=1 (2 CT trùng); đổi fixture coef=5 + assert cost=9tr (không 45tr) → PASS 6 assertions. Cost-if-wrong: 0, đã port đúng ERP + có test chặn tái phát.
  - **CHỐT cho T5:** nhánh WrService GIỮ `×unit_coefficient` (port ERP dòng 600) — NGƯỢC nhánh Firm. Brief T5 phải ghi rõ.

### Prep T5 (đọc sẵn ERP `BorrowSell::getDataCreateDept` dòng 556-723 — PLAN STUB THIẾU NHIỀU)
Nhánh WrService ERP có **5 block bút toán + cụm hỗ trợ**, nhiều hơn plan T5 (plan chỉ ghi 3 block):
1. **Doanh thu** 1311/5111/33311 (Work DTHH=15): dùng `sum_amount_after_extra_after_vat` (Nợ1311), `sum_amount_after_extra` (Có5111), `sum_amount_after_extra_vat` (Có33311). Meta 5111: Employee=created_by, employee_department_id=department_id.
2. **Chiết khấu** 5211/33311/1311 (Work **CKHH** — KHÔNG có trong 6 WORK_* của T4, phải resolve thêm): `discount=Σ rebate_price×qty`, `discount_vat=Σ rebate_price×qty×vat%`. Nợ5211=discount, Nợ33311=discount_vat, Có1311=discount+discount_vat. **Không có method trait cho block này → viết inline trong wrServiceBranch.**
3. **Giảm trừ DT** 5213/33311/1311 (Work GGHH=16) — **PLAN STUB BỎ SÓT BLOCK NÀY**: `sale_invoice=Σ(price+extra-allocated-rebate)×qty`, `sale_invoice_vat=Σ×vat%`. Nợ5213=sale_invoice, Nợ33311=sale_invoice_vat, Có1311=tổng.
4. **Giá vốn** 1561/632 (KHÔNG phải 157): `Σ export_price×qty×unit_coefficient` (**CÓ nhân coef** — khớp Ruling 2; NGƯỢC nhánh Firm).
5. **Cụm hỗ trợ** (trait) với `percent` RIÊNG: `percent = (sum_amount_after_extra − sale_invoice − discount) / (before_vat_total − before_vat_other_cost − before_vat_delivery_cost)` — KHÁC công thức percent nhánh Firm (T4 firmBranch tính riêng, phải đối chiếu). Cụm gồm thưởng HĐ (5211/35241 TTHHD=12), TNCN (35241/3335 TTHHD), hoa hồng tháng (6411/35241 TNST=13), hoa hồng quý (6411/35241 TNSQ=14), quỹ rủi ro (6411/35241 RRP=6) — cùng cấu trúc trait T3.
- **resolveContract WrService**: `WrServiceContract::find($bs->contractable_id)` → shim `new Contract(...)` (pattern T4 Ruling 1) + setRelation support_accounting theo `CONTRACT_WR_SERVICE`. **PHẢI verify** nơi lưu HTHT của WrServiceContract: cùng `firm_support_accounting` (polymorphic) hay bảng khác? + có shim đủ cột không.
- **Sửa lỗi plan T5 trong brief:** (a) `getDataAccounting` trả `[bool,array,string]` — test destructure tuple, KHÔNG `$accounts = getDataAccounting()`; (b) `borrow_sell_qty`→`qty`; (c) `php artisan test`→`php vendor/bin/phpunit`; (d) khai thêm const cho CKHH (WORK_CHIET_KHAU) nếu wrServiceBranch cần.
- **Verify trước dispatch T5:** trait có `revenueAccounting`/`revenueDeductionAccounting` → wrServiceBranch tái dùng cho block 1 & 3? hay ERP truyền tham số khác? Đọc thân 2 method trait + cách firmBranch gọi để chốt.
- **CHỐT nơi lưu HTHT WrService (verify SQL):** `firm_support_accounting` có 0 row WrServiceContract → HTHT HĐ dịch vụ nằm ở bảng **`wr_support_accounting`** (ERP model `WrSupportAccounting`, morphOne 'contractable'). Bảng này CÓ đủ 5 cột trait đọc (before_vat_total/before_vat_other_cost/before_vat_delivery_cost/contract_performance_bonus_before_vat/personal_income_tax) + bảng con `wr_support_accounting_departments`/`_employees`/`_department_details` song song firm_*. → **T5 resolveContract phải gắn support_accounting từ WrSupportAccounting (theo HRM entity map `wr_support_accounting`), KHÔNG dùng query `firm_support_accounting` như T4** (T4 query `SupportAccounting::where contractable_type=CONTRACT_FIRM` → NULL cho WrService). Cần tìm HRM entity map `wr_support_accounting` + xác nhận nó có relation `departments()`/`employees()`/`department_root`/`objectable`/`department_lead` cùng tên trait gọi. Data: 70 phiếu borrow_sells WrService thật để dựng fixture.
- **Entity note T5:** T4 dùng `Modules\Assign\Entities\Contract\SupportAccounting` (firm) + `Modules\Finance\Entities\Contract\FirmContract`. HRM CHƯA có entity riêng map `wr_support_accounting` (grep chỉ thấy string ở `BorrowSellRequestService`). Ứng viên WrServiceContract HRM: `Modules\Assign\Entities\TpWrServiceContract` (cần xác nhận `$table`). **Insight quan trọng:** trait nhận `$sa` là THAM SỐ (`bonusContractAccounting($percent, $sa, Contract $contract, ...)`) + đọc `$sa->departments` — nên chỉ cần TRUYỀN đúng model WrSupportAccounting (có relation departments/employees) làm `$sa`; shim `$contract` chỉ cần company_id/created_by/customer_id. → wrServiceBranch có thể lấy `$sa` trực tiếp không nhất thiết qua setRelation. Chốt cách khi viết brief (đọc thân firmBranch xem lấy $sa từ đâu).

### Prep T5 — CHỐT CUỐI (mọi ẩn số đã verify, sẵn sàng dispatch)
- **CKHH work id = 20** (khớp plan). Work ids: DTHH=15, GGHH=16, CKHH=20, TTHHD=12, TNST=13, TNSQ=14, RRP=6.
- **HĐ dịch vụ**: dùng entity SẴN CÓ `Modules\Finance\Entities\Contract\WrServiceContract` ($table=wr_service_contracts, read-only). `wr_service_contracts` đủ 7 cột shim: id/code/company_id/department_id/part_id/customer_id/created_by. `wr_support_accounting.contractable_type` = `App\Model\Customers\WrServiceContract` (2471 row) = khớp `BorrowSell::CONTRACT_WR_SERVICE`.
- **Entity mirror phải TẠO** (HRM chưa có) tại `Modules/Finance/Entities/Contract/`: `WrSupportAccounting` (table wr_support_accounting, `departments()` hasMany FK `wr_support_accounting_id`) + `WrSupportAccountingDepartment` (table wr_support_accounting_departments, `employees()` + `details()` hasMany FK `wr_support_accounting_department_id`) + `WrSupportAccountingEmployee` (table wr_support_accounting_employees) + `WrSupportAccountingDepartmentDetail` (table wr_support_accounting_department_details). MIRROR y hệt bộ Assign `Modules/Assign/Entities/Contract/SupportAccounting*` chỉ đổi $table + FK. Parity cột verify: wr_departments giống firm_departments CHỈ khác tên FK.
- **Trait tái dùng được cho cụm hỗ trợ**: trait đọc `$sa->departments`/`$department->employees` (relation) + `department_id/objectable_type/objectable_id/commission_sale_percent/...` (CỘT, resolve qua helper `dept()`/`objectableDeptId()`/`partLeadId()`) → mirror tối thiểu là đủ. Cụm Firm (FirmContractBorrowSellService) và WrService (getDataCreateDept) DÙNG CHUNG cấu trúc account 5211/35241/3335/6411 + TTHHD/TNST/TNSQ/RRP → trait dùng lại.
- **KHÁC BIỆT then chốt Firm vs WrService** (port faithful): (1) WrService dùng **MỘT** `percent` cho MỌI cụm (Firm dùng 2: pct_wo_delivery + pct_wo_cost). `percent_ws = (sum_amount_after_extra − sale_invoice − discount)/(before_vat_total − before_vat_other_cost − before_vat_delivery_cost)`. (2) WrService có thêm block **chiết khấu** (5211/33311/1311 CKHH=20, inline, không có trait method). (3) Giá vốn WrService = Nợ632/Có**1561** × **unit_coefficient** (Firm=157 không coef). (4) revenueAccounting/revenueDeductionAccounting của trait TÁI DÙNG cho block doanh thu + giảm trừ.
- **Fixture test T5**: borrow_sells id=93 → contractable_id=139 → wr_support_accounting id=64 (before_vat_total=1.581.300). Hoặc dựng in-memory như T4 với contractable_id thật có HTHT.
- **Sửa lỗi plan T5**: getDataAccounting trả tuple `[bool,array,string]` (test destructure, KHÔNG `$accounts=getDataAccounting()`); `qty` không `borrow_sell_qty`; phpunit không artisan test; khai thêm const WORK_CHIET_KHAU=20.
- **resolveContract**: hiện Firm-only. T5 sửa để rẽ nhánh theo contractable_type (Firm→FirmContract+SupportAccounting; WrService→WrServiceContract+WrSupportAccounting). postAccounting (dòng 72-74) hiện chỉ resolve cho FIRM → sửa để resolve cả 2 (meta HĐ dịch vụ).

### Task 5: BASE = 34fd294 (nhánh gop_db). Model dispatch: sonnet.

#### RULINGS T5 (verify bằng information_schema, KHÔNG đoán):
- **Ruling T5-1 (BẪY tên cột — accessor alias):** `wr_support_accounting` KHÔNG có cột `bonus_contract_before_vat`/`tndn_vat` (đó là cột của `firm_support_accounting`). Cột tương đương ở WR: `contract_performance_bonus_before_vat` + `personal_income_tax`. Trait `bonusContractAccounting`/`vatExtraCostAccounting` đọc `$sa->bonus_contract_before_vat`/`$sa->tndn_vat` → trên WR sẽ ra NULL → thưởng HĐ + TNCN = 0 (HỎNG ÂM THẦM). GIẢI: mirror `WrSupportAccounting` khai 2 accessor alias `getBonusContractBeforeVatAttribute()`→`contract_performance_bonus_before_vat`, `getTndnVatAttribute()`→`personal_income_tax`. KHÔNG sửa trait, KHÔNG inline block 5. Cô lập khác biệt tên cột vào entity-adapter. Cost nếu sai: nếu bỏ sót alias → thưởng/TNCN=0, lệch sổ (test phải assert 5211 thưởng > 0).
- **Ruling T5-2 (bỏ lọc company):** ERP `getDataCreateDept` (dòng 613, 711) lặp `support_accounting->departments` KHÔNG lọc theo company; trait (port từ ProductExportPostingService) LẠI lọc `deptCompany !== contractCompanyId`. Port faithful = KHÔNG lọc. GIẢI: sửa trait `monthlyAndQuarterlyCommissionAccounting` + `riskFundAccounting`: khi `$contractCompanyId === null` thì BỎ QUA lọc. `wrServiceBranch` truyền `null`. Backward-compatible (caller cũ truyền company_id thật → giữ nguyên). Cost nếu sai: nếu WrService toàn phòng cùng company thì null-filter ≡ có filter (vô hại); nếu có phòng khác company thì null-filter mới khớp ERP. An toàn 2 chiều. (Sửa trait = trong phạm vi Hướng A đã duyệt.)
- **Ruling T5-3 (block 1-4 inline, block 5 tái dùng trait):** block 1 doanh thu + 2 chiết khấu + 3 giảm trừ + 4 giá vốn → INLINE trong `wrServiceBranch` (khác Firm: block 2 chỉ WrService có; block 4 giá vốn Nợ632/Có**1561** ×unit_coefficient; block 1&3 ERP set `employee_department_id=contract->department_id` trên 5111/5213 mà trait bỏ → inline để khớp faithful). Block 5 (thưởng/TNCN/hoa hồng tháng-quý/quỹ rủi ro) → tái dùng 4 method trait (bonusContractAccounting, vatExtraCostAccounting, monthlyAndQuarterlyCommissionAccounting[null], riskFundAccounting[null]) nhờ accessor alias + null-filter. **MỘT** percent WrService cho cả 4: `percent = (sum_amount_after_extra − sale_invoice − discount)/(before_vat_total − before_vat_other_cost − before_vat_delivery_cost)`.
- **Verify cột (information_schema erp_hrm_check):** WR header có `contract_performance_bonus_before_vat`, `personal_income_tax`, `before_vat_total`, `before_vat_other_cost`, `before_vat_delivery_cost`, `before_vat_product`, `before_vat_repair` (KHÔNG `before_vat_repair_service`). WR dept (46 cột = parity firm) đủ is_main/department_id/objectable_type/objectable_id/diff_*_percent/month_*_amount/after_settlement_*_amount/risk_fund_amount, FK header = `wr_support_accounting_id`. WR emp có employee_id/part_id/commission_sale_percent, FK dept = `wr_support_accounting_department_id`.
- Mirror entity `department_main()` = hasOne(...)->where('is_main', true) (giống Assign SupportAccounting).
- Brief đã viết: task-p2-5-brief.md.
- **DISPATCHED** T5 implementer (sonnet, agentId a5d879bb974da1961) lúc BASE=34fd294. Đang chạy nền. Chờ report → review.

### Task 5: complete (impl 4ddb4cd + fix test 04869e2)
- Review (sonnet a955b24): **SPEC PASS / QUALITY APPROVED**. Verify độc lập bằng 2 script probe trên DB erp_hrm_check: 3 ruling ĐÚNG — (T5-1) `WrSupportAccounting` có 2 accessor alias, probe xác nhận `$sa->bonus_contract_before_vat`=9000 (đọc contract_performance_bonus_before_vat), `$sa->tndn_vat`=0 (đọc personal_income_tax); (T5-2) trait thêm `$contractCompanyId !== null &&` ở cả 2 method, wrServiceBranch truyền null, firmBranch giữ company_id thật (regression Firm/ProductExport không đổi); (T5-3) costAccountingWrService = export_price×qty×coef → 1561/632 = 45tr, chiết khấu CKHH=1tr, 1 percent chung cho 4 lệnh cụm. Nhánh Firm chỉ thêm doc-comment. Không dùng mysql2.
- **Finding (nên sửa, KHÔNG blocker):** test fixture `allocated_price=0` → numerator percent (=allocated×qty) = 0 → mọi bút toán cụm hỗ trợ value=0 → assertion "phải có thưởng HĐ" vacuous (pass cả khi alias hỏng vì entry vẫn tạo với value=0). Code đã verify đúng bằng probe ngoài test, nhưng test chưa bảo vệ.
- **Ruling (fix inline, không dùng subagent — test-only 2 dòng, tự verify bằng phpunit):** đặt `allocated_price=50000` → percent≠0 → thêm `assertGreaterThan(0, $bonus['value'])`. Chạy `phpunit` = OK (1 test, **9 assertions**). Cost/chiết khấu/balance giữ nguyên (không phụ thuộc allocated). Commit test 04869e2. TNCN vẫn không exercise được (personal_income_tax=0 ở fixture id=4) — chấp nhận, đã note; thưởng HĐ (bonus=9000) đủ khoá regression alias.
- **Task 5: complete** (commit 4ddb4cd code + 04869e2 test).

### Prep T6 (cước vận chuyển — accountingDeliveryTrip), làm SAU khi T5 xong (cùng đụng BorrowSellPostingService.php, KHÔNG song song)
- Nguồn ERP: `BorrowSell::accountingDeliveryTrip()` dòng 512-554. Lặp `parent->product_export_requests`, bỏ qua `is_export_direct`; tra WarehouseExportRequest→WarehouseExport→ActivityHasDeliveryTrip; CHỈ hạch toán nếu chuyến xe ĐÃ có bút toán (`AccountDetail where invoiceable=delivery_trip` count>0). company_pay>0 → Nợ 6427/Có 3351 (cost_debt TVC); ngược lại Nợ 3351/Có 3351 (work TVC). Ghi theo `DeliveryTrip::class` + delivery_trip_id.
- HRM ĐÃ CÓ entity: `Modules/Finance/Entities/Delivery/ActivityHasDeliveryTrip.php`, `.../Delivery/DeliveryTrip.php`, `Modules/Finance/Entities/CostDebt.php`. WarehouseExport có 2 bản (Assign + Finance) → brief phải chốt dùng bản nào (theo bảng chung merged-DB).
- **work TVC id = 10** (verify DB). ⚠️ **cost_debts KHÔNG có row code='TVC'** (query rỗng) → nhánh company_pay (6427) tag cost_debt sẽ null. OPEN ITEM T6: kiểm CostDebt::getByCode() + cách ERP map TVC; có thể HRM chưa seed cost_debt TVC. Điều tra khi viết brief T6.
- borrow_sells.parent = borrow_sell_request (mã YCXBHM). BorrowSell HRM entity cần quan hệ `parent` + request có `product_export_requests`. Kiểm khi viết brief.
- **T6 điều tra thêm (2026-09-07):** HRM BorrowSell CÓ `borrowSellRequest()` (KHÔNG có `parent` — dùng borrowSellRequest thay ERP `$this->parent`). BorrowSellRequest entity có sẵn — cần kiểm quan hệ `product_export_requests`. `ActivityHasDeliveryTrip` có `trip()` belongsTo DeliveryTrip + cột warehouse_export_id/delivery_trip_id/total_cost_transition. **CostDebt KHÔNG có `getByCode()`** → T6 query cost_debts theo code trực tiếp (như works). **cost_debts KHÔNG có code 'TVC'** — ERP dùng `$cost_debts['TVC'] ?? 0` → thực tế = 0; đây LÀ hành vi ERP thật (nhánh company_pay Nợ 6427 tag cost_debt_id=0), KHÔNG phải bug → port faithful với `?? 0`. Work TVC=10 vẫn dùng cho nhánh còn lại + vế Có 3351. → T6 KHÔNG bị chặn bởi thiếu cost_debt TVC.
- Còn phải chốt khi viết brief T6: WarehouseExport/WarehouseExportRequest + ProductExportRequest dùng entity module nào (Assign vs Finance) cho khớp bảng merged-DB.

### Task 6 — CHỐT CUỐI (mọi ẩn số verify xong, BASE = 04869e2, model sonnet)
- **T6 là method RIÊNG** trong BorrowSellPostingService (`postDeliveryTripAccounting`), TÁCH khỏi getDataAccounting: lưu sổ theo TỪNG chuyến xe (`invoiceable=(delivery_trip_id, DeliveryTrip FQN)`), gọi độc lập ở orchestrator T7 (ERP gọi tại `BorrowSellsController@update:281` sau khi finalize phiếu).
- **Entity map (Explore verify):** đọc PER qua `$bs->borrowSellRequest->product_export_requests` (relation SẴN CÓ trên `BorrowSellRequest`, belongsToMany qua pivot `borrow_sell_request_has_export_requests` → `Modules\Finance\Entities\ProductImportRequest\ProductExportRequest` read-only — CHỈ ĐỌC is_export_direct/created_by/department_id nên bản read-only OK, KHÔNG cần relation mới). `WarehouseExportRequest`+`WarehouseExport` = bản **Assign** (`Modules\Assign\Entities\Warehouse\*`). `ActivityHasDeliveryTrip`+`DeliveryTrip` = **Finance** (`Modules\Finance\Entities\Delivery\*`, T2 đã tạo, `trip()` belongsTo OK). `AccountDetail` = Finance `Entities\Account\AccountDetail`.
- **saveAccountDetail HRM ≠ ERP:** HRM `saveAccountDetail($accounts, $invoiceable_id, $invoiceable_type, $invoiceable_code, array $meta=[])` — `$invoiceable_code` BẮT BUỘC (NOT NULL). ERP dòng 552 gọi 3 args (không code). → HRM truyền `code = $trip->name` (khớp ERP AccountDetail:202 set invoiceable_code=trip->name khi type=DeliveryTrip), meta=[].
- **RULING T6-A (FQN check — no-op trên data hiện tại, PORT FAITHFUL):** ERP check dòng 526 `where invoiceable_id=delivery_trip_id AND invoiceable_type=DeliveryTrip::class` (`App\Model\Warehouse\DeliveryTrip`). Seed row đó do `DeliveryTripController:951` ghi (verify grep). NHƯNG DB gộp có **0 row** type=DeliveryTrip (15k+ row chuyến xe đều key `DeliveryTripAccounting` — flow DeliveryTripAccountingController). → trên data hiện tại check luôn 0 → luôn `continue` → T6 KHÔNG post gì. GIẢI: port THẲNG với const `INVOICEABLE_DELIVERY_TRIP='App\\Model\\Warehouse\\DeliveryTrip'` (giống pattern INVOICEABLE_BORROW_SELL để ERP đọc lại). KHÔNG tự đổi sang DeliveryTripAccounting (đó là thay đổi spec, không phải faithful port). Cost nếu sai: nếu HRM active-flow là DeliveryTripAccounting-marker thì cước không bao giờ ghi — NHƯNG hành vi trùng ERP trên cùng data → faithful. Flag rõ cho reviewer + report; nếu user muốn đổi cột check = quyết định nghiệp vụ ngoài port.
- **RULING T6-B (fix double-post):** ERP set `$accounts=[]` 1 lần NGOÀI loop rồi saveAccountDetail MỖI vòng → chuyến 2 lưu lại cả bút toán chuyến 1 (double-post). Rõ ràng là oversight (invoiceable_id đã per-trip). GIẢI: build `$tripAccounts=[]` MỚI mỗi vòng, save riêng. Diverge code chữ ERP nhưng khớp intent per-trip. Cost nếu sai≈0.
- **RULING T6-C (null guard):** ERP `$warehouse_export->id` không guard null → thêm `if(!$warehouse_export) continue;` (an toàn, ERP giả định luôn có).
- **Bút toán 1 chuyến** (amount = `activity->total_cost_transition`, work TVC=**10**, cost_debt TVC KHÔNG tồn tại → `cost_debt_id=0`):
  - `company_pay>0`: Nợ 6427 [ref 3351] meta{employee_id=per.created_by, group, cost_debt_id=0}; Có 3351 [ref 3351] meta{employee_id=per.created_by, employee_department_id=per.department_id, group, work_id=10}.
  - `company_pay<=0`: Nợ 3351 [ref 3351] meta{employee_id=per.created_by, employee_department_id=per.department_id, group, work_id=10}; Có 3351 [ref 3351] meta{...work_id=10} (như trên).
  - Tách helper thuần `buildTripCostAccounts(float $amount, bool $companyPay, ?int $createdBy, ?int $deptId, int $group): array` để TEST không cần DB.
- **Test T6:** (1) unit `buildTripCostAccounts`: company_pay>0 → có 6427 Nợ + 3351 Có, cost_debt_id=0, work_id=10, Nợ=Có; company_pay=0 → 3351 Nợ + 3351 Có, cả 2 work_id=10, Nợ=Có. (2) guard: `postDeliveryTripAccounting` trên BorrowSell in-memory không có chuyến đã-hạch-toán → trả [true,''] + không ghi row (đúng data thực tế).

### Note chuyển tiếp T7
- `BorrowSell::generateCode()` static-pure `max(id)+1` — race nhẹ. T7 store: gọi trong DB::transaction + retry/lock hoặc dựa unique index; đối chiếu cách Phase 1 sinh code.
- FK đã chốt: `borrow_sell_products.parent_id`→borrow_sell; `borrow_sell_product_details.parent_id`→product; `borrow_sell_tabs.parent_id`; `borrow_sell_tab_products.parent_id`; `borrow_sell_tab_product_details.parent_id`; `borrow_sells.borrow_sell_request_id`→phiếu YC.

### Task 6 — DISPATCHED
- brief `task-p2-6-brief.md`, BASE `04869e226aeec6cdd70382ecccb874470ed0cbef`, implementer agent `aedb6d145e84346af` (sonnet). Chờ report.

### Task 6 — COMPLETE ✅
- commit `60674e96c` (service +105/-0 vùng mới, test mới). Test `BorrowSellDeliveryTripAccountingTest` PASS 2/13 assertions.
- Reviewer (agent a58466fa02c2e48e7): SPEC PASS + QUALITY APPROVED, 0 blocker. 3 non-blocker đều kế thừa brief/hàm chung, không sửa.
- **Carryover cho T7** (từ review): (a) `saveAccountDetail` bỏ lặng vế `value<=0` → nếu `total_cost_transition=0` cho 1 chuyến thì cả 2 vế bị bỏ (an toàn); chỉ lệch cân nếu upstream sai lệch 1 vế — lưu ý khi QA. (b) `$trip` null → `$trip->name ?? ''` an toàn nhưng có PHP warning; faithful-ERP, giữ nguyên. (c) `postDeliveryTripAccounting` CHƯA được gọi từ đâu — T7 orchestrator phải nối dây (ERP gọi ở BorrowSellsController@update:281 SAU finalize phiếu).
- **T6 no-op trên DB gộp hiện tại** (Ruling T6-A) = đúng kỳ vọng.

---

## Task 7 — BorrowSellService::store() orchestrator

BASE: 60674e96cf3319a0a89e44754e4890210d58f94c

### Rulings T7 (ghi trước khi dispatch)

- **Ruling T7-1 (tiền ở BE):** Tính LẠI header financial sums server-side trong store() bằng cách mirror Phase 1 `computeAmounts()` (price×Firm/extra/allocated/vat × qty), lấy giá từ snapshot request_product (BE-persisted) + qty từ FE. KHÔNG đọc `sum_amount_*`/`vat_cost_allocated` từ request. — Vì ràng buộc đã chốt "tiền tính ở BE, FE chỉ gửi qty" + postAccounting đọc trực tiếp `sum_amount_after_extra(_vat)`. — Cost nếu sai: header sums lệch hiển thị FE, nhưng BE là nguồn hạch toán → đúng về kế toán.
- **Ruling T7-2 (generateCode chống race):** Code sinh bằng real auto-increment id sau save đầu (`code='TMP-'.uniqid()` → save → `code=PREFIX.'-'.str_pad(id,5,'0')` → save), KHÔNG dùng static `generateCode()` (max('id')+1 có race). — Mirror ERP. — Cost nếu sai: không đáng kể, an toàn hơn.
- **Ruling T7-3 (updateWarehouse atomic):** Cột cộng dồn (`borrow_returned_qty`, `returned_by_sell` trên product_export_request_details; `exported_qty` trên objectable) dùng `increment()` atomic; cột gán (`approved_qty`, `borrow_status`) dùng `update()`. — Fix lost-update BorrowSell (memory incident 2026-09-04). — Cost nếu sai: tồn ảo khi 2 phiếu chạy đồng thời.
- **Ruling T7-4 (nested transaction):** store() mở 1 `DB::transaction(closure)`; gọi `postDeliveryTripAccounting($bs)` RỒI `postAccounting($bs)` bên trong (mỗi hàm tự mở transaction lồng = savepoint); check `[ok,err]` trả về, THROW nếu ok=false để rollback outer. — 2 hàm posting catch Throwable & return (không tự rethrow) nên phải check + throw. — Cost nếu sai: phiếu tạo nhưng thiếu bút toán mà không rollback.
- **Ruling T7-5 (returningQty loại trừ parent):** Port `returningQty($exportRequestId,$productId)` của Phase 1 vào Service, THÊM tham số loại trừ `$parent->id` khỏi nhánh sell subquery (bsr.status=2). — Mirror ERP `getReturningQty(null,$parent->id,null)`; lúc store parent vẫn status=2 nên qty đang bán của chính nó bị đếm 2 lần → chặn nhầm. — Cost nếu sai: check tồn quá chặt, chặn phiếu hợp lệ.
- **Ruling T7-6 (HANG_THUONG only, bỏ tabs/KM):** Bỏ `syncTabs` và nhánh tabs của updateWarehouse; chỉ path SP thường. — Ràng buộc đã chốt "hàng thường only, skip KM". — Cost nếu sai: Firm borrow-sell cần tách tab sẽ không lưu borrow_sell_tabs; hạch toán+kho KHÔNG ảnh hưởng (key theo products/objectable). Flag QA T14.
- **Ruling T7-7 (bỏ guard need_check_exported):** Bỏ guard quota hợp đồng của ERP. — Cột `need_check_exported` KHÔNG tồn tại ở firm_contract_tab_products / wr_service_contract_items / borrow_sell_requests trong DB gộp (verify SQL); `availableSellQty` per-detail là guard tồn chính. — Cost nếu sai: không có (cột không tồn tại để check).

### T7 dispatch
- Brief: task-p2-7-brief.md
- Implementer: aca86ab42c0ecf87c (sonnet), BASE 60674e96c
- Trạng thái: đang chạy (chờ report → review). Không dispatch song song đụng BorrowSellPostingService.php.

### CONFLICT T7↔T8 (phát hiện lúc chờ review T7) — cần ruling
- Plan T8 FormRequest quy định payload `products.*.borrow_sell_request_product_id` (FK trực tiếp tới BorrowSellRequestProduct).
- T7 implementer lại tra parent product theo `products[].objectable_id/objectable_type` (kiểu ERP morph) + `details[].product_export_request_detail_id`.
- Phải thống nhất 1 shape, nếu không Controller T9 truyền payload T7 không đọc được.
- **Nghiêng về:** dùng `borrow_sell_request_product_id` (FK trực tiếp — unique, sạch, không mơ hồ morph). T7 vẫn đọc được objectable_id/type TỪ DB row của BorrowSellRequestProduct (không cần từ payload) để tăng exported_qty. → sửa nhỏ product-loop lookup của T7 + rules T8 khớp.
- Chốt ruling + gộp vào fix round T7 (nếu reviewer yêu cầu fix) hoặc mở fix nhỏ, RỒI mới viết brief T8. Chưa dispatch T8 tới khi giải quyết.

### Task 7: complete
- Commit 99f08bf6c. Test 3/3 xanh thật (BorrowSellStoreTest) + regression 9 test cũ xanh.
- Reviewer a47e1eb5209acfc68 (verify trực tiếp ERP source): Spec ✅ PASS cả 7 rulings; Quality APPROVED, không blocker.
- Reviewer xác nhận thêm: công thức weighted `total_export_price += detailQty*unit_coefficient*export_price` khớp ERP dòng 240 (code ĐÚNG hơn tóm tắt brief); increment exported_qty theo $p->qty (không nhân coef) khớp ERP dòng 414.

### Backlog follow-up (ghi trước khi WrService đi production qua Service này)
- **FU-1 updateHandoverDate:** ERP store() dòng 316 gọi $contract->updateHandoverDate(); HRM chưa port (brief flow a→i không có). Cần confirm có port method này không.
- **FU-2 nested WrService double-increment:** ERP updateWarehouse dòng 416-421 tăng exported_qty 2 lần cho WrService (wr_service_contract_items + objectable lồng bên trong). HRM chỉ tăng 1 lần bảng phẳng. Gap thật đã verify — chỉ ảnh hưởng nhánh WrService (103 rows). Xử lý trước khi bán mượn hàng dịch vụ WrService chạy thật.

### Ruling T8-payload (chốt conflict T7↔T8)
- Align T8 FormRequest + T9 Controller + FE về ĐÚNG shape T7 đang tiêu thụ (KHÔNG dùng `borrow_sell_request_product_id` như plan T8 ghi):
  - `borrow_sell_request_id` (int)
  - `products[].objectable_id` (int) + `products[].objectable_type` (string)
  - `products[].details[].product_export_request_detail_id` (int) + `products[].details[].qty` (numeric)
- Vì: T7 đã APPROVED với shape này (ERP-faithful, đã test); sửa T7 sang FK trực tiếp là scope creep vô ích. Cost nếu sai: morph-matching mong manh hơn FK trực tiếp một chút, nhưng T7 đã handle + test lookup này.

## Task 8 — StoreBorrowSellRequest FormRequest
BASE: 99f08bf6ccb87ccd82e3d04af48fb6d8629f8827
Brief: task-p2-8-brief.md. Payload theo Ruling T8-payload (objectable_id/type + product_export_request_detail_id + qty).

### Task 8: complete
- Commit 7277390be. Test 3/3 xanh (5 assertions).
- Review (controller trực tiếp, diff 2-file trivial): Spec ✅ PASS (rules khớp payload T7: objectable_id/type + product_export_request_detail_id + qty), Quality APPROVED — messages tiếng Việt đủ, test không vacuous, authorize()=true đúng (gate middleware+service).

## Task 9 — BorrowSellController + 3 Resource + routes
BASE: 7277390bec9eeea36558657bcefeff9afe6da70d

### Rulings T9 (chốt từ kết quả Explore ad26034bba839b476 — plan lệch thực tế)
- **Ruling T9-perm (sửa id sai):** Plan ghi 4 quyền 100315-100318 — KHÔNG tồn tại. Cơ chế thật là NAME-based qua trait ChecksEmployeePermission. BorrowSell list scope tái dùng ĐÚNG 4-tier NAME của BorrowSellRequest (VIEW_ALL_COMPANY / VIEW_COMPANY / VIEW_DEPARTMENT / else created_by=self), cài bằng static `BorrowSell::searchByFilter($request)` mirror `BorrowSellRequest::searchByFilter()`. Tham chiếu hằng `BorrowSellRequest::PERMISSION_VIEW_*` (DRY, cùng feature). — Cost nếu sai: phạm vi thấy list = phạm vi thấy yêu cầu (nhất quán, chấp nhận được).
- **Ruling T9-store-gate (bỏ middleware checkPermission):** KHÔNG dùng `checkPermission` middleware (Phase 1 cố tình tránh vì spatie guard/model_type mismatch — docblock controller). Controller store() gate tường minh trả 403 nếu thiếu 'Kế toán kho' (mirror show()→canView→403) bằng public helper mới `BorrowSell::userCanCreate(): bool`; service `canApprove()` giữ làm defense-in-depth + gate status (throw ValidationException 422 nếu sai status). — Cost nếu sai: 403 vs 422 khác nhau chút, nhưng khớp pattern Phase 1 đã chứng minh.
- **Ruling T9-print (không có mẫu in):** `XUAT_BAN_HANG_MUON` không tồn tại. PrintResource trả JSON thuần mirror BorrowSellRequestPrintResource, KHÔNG tra report_key/template. FE tự render. — Cost nếu sai: nếu sau này cần khóa mẫu in thật thì bổ sung, không chặn T9.
- **Ruling T9-accounting-in-detail:** Detail Resource của BorrowSell nhúng khối `accounting` = `getDataAccounting($bs)` (trả [ok,accounts,err]) → nếu ok=true nhúng `accounts`, else nhúng `accounting_error=err`. Đây là điểm KHÁC Phase 1 (Phase 1 không có accounting). Loại HĐ suy từ contractable_type (đã có trong getDataAccounting).
- **Ruling T9-entity-additions:** T9 được phép bổ sung vào entity BorrowSell (file Phase 2 của chính feature): static `searchByFilter($request)`, static `meta()` (cờ FE: is_ke_toan_kho), public `userCanCreate()`, accessor `getIsCanViewAttribute` (=canView()) cho Resource. KHÔNG sửa entity dùng chung khác.

### Task 9: complete
- Commit 394b5da44. API layer: BorrowSellController (index/store/show/printData) + 3 Resource (List/Detail/Print) + routes /borrow-sells + entity additions (searchByFilter/meta/userCanCreate/getIsCanViewAttribute + relation employee_create).
- Reviewer a61c79acf6102cd0c: Spec ✅ PASS cả 5 ruling (verify BorrowSellRequest có đúng 4 hằng NAME; route không có checkPermission middleware; store gate 403 qua userCanCreate; PrintResource JSON thuần; DetailResource nhúng getDataAccounting đúng contract; chỉ sửa BorrowSell.php). Quality APPROVED, không BLOCKER. Test 5/13 assertions OK (1 skip có lý do: thiếu helper actingAs JWT).
- Verify thêm: không hardcode `= true`; whereHas scope fail-closed không leak; N+1 tránh bằng whereIn; show route đặt cuối; không catch-all Exception; không DB_CONNECTION_SECOND.

### Backlog follow-up (bổ sung)
- **FU-3 getDataAccounting chỉ catch \RuntimeException:** BorrowSellPostingService::getDataAccounting (dòng ~117-149) chỉ catch \RuntimeException — TypeError/DivisionByZeroError/\Exception khác ném xuyên BorrowSellDetailResource::toArray() → vỡ 500 thay vì trả accounting_error. Code T4-6 cũ, KHÔNG do T9. Fix nhỏ sau: bọc `try{...}catch(\Throwable $e){accounting_error}` trong Resource HOẶC mở rộng catch trong service. Không chặn.

## Task 10 — FE wiring: BE flag + api.js + nút "Lập phiếu bán" + menu
BASE: (ghi trước dispatch)

### Explore FE (a6b3cc2239896557c) — phát hiện lệch plan
- FE Phase 1 KHÔNG dùng Vuex store module. Dùng `pages/finance/<feature>/api.js` wrapper mỏng quanh action chung `apiGetMethod`(store/actions.js:1455)/`apiPostMethod`(:1474). BASE path 'finance/...' (bỏ /api/v1/, action tự thêm).
- `$store.state.permissions` = mảng object có `.name` (tên quyền tiếng Việt); check `perms.some(p=>p.name==='Tên quyền')`. Init `[]` (state.js:10), set từ res.data.permissions (actions.js:96).
- List Phase 1 gate nút Xem per-row bằng `item.is_can_view` (BE trả), KHÔNG global-gate nút Tạo.
- Detail `_id/index.vue` CHƯA có nút "Lập phiếu bán". Actionbar `.export-actionbar` fixed, các nút gate bằng `data.is_can_*`.
- BE `BorrowSellRequestDetailResource:144-149` CHƯA có cờ tạo phiếu bán.
- Menu: `components/subsystem-menu/finance.js:169` có entry borrow-sell-requests; cần thêm entry borrow-sells.
- Form Phase 1 `BorrowSellRequestForm.vue`: bảng lồng 2 cấp productGroups→details, getter tiền dòng 570-606, buildPayload 613-648, unsavedChangesMixin+markFormSaved, map 422 qua handleSaveError→formErrors.
- Print Phase 1 `_id/print.vue`: layout:'print', $printContent, render template thường (KHÔNG v-html), data từ printData endpoint.

### Rulings T10
- **Ruling T10-apijs (sửa "modify store"):** Plan T10 ghi sửa `store/finance.js` — SAI. FE Phase 1 không có store module cho feature này. Tạo MỚI `hrm-client/pages/finance/borrow-sells/api.js` mirror `borrow-sell-requests/api.js` (BASE='finance/borrow-sells', 4 hàm list/show/store/printData quanh apiGetMethod/apiPostMethod). — Cost nếu sai: 0, đúng pattern Phase 1 đã chạy.
- **Ruling T10-flag (thêm cờ BE fail-closed):** Thêm field `is_can_create_borrow_sell` vào `BorrowSellRequestDetailResource` = `BorrowSell::userCanCreate() && $this->canApprove()` (Kế toán kho + phiếu YC ở trạng thái được lập phiếu bán). Additive, read-only, cùng họ feature borrow-sell, bắt buộc để FE gate fail-closed. — Cost nếu sai: 1 field thừa trên response detail, gỡ được, không đổi hành vi field cũ. Đây là ruling (không phải stop): additive, revertible.
- **Ruling T10-button:** Thêm nút "Lập phiếu bán" vào `borrow-sell-requests/_id/index.vue` actionbar, `v-if="data.is_can_create_borrow_sell"` (init false fail-closed), điều hướng `/finance/borrow-sells/create?request_id=<id>`. Tuân skill button-convention.
- **Ruling T10-menu:** Thêm entry `{ label: 'Xuất bán hàng mượn', link: '/finance/borrow-sells' }` vào `components/subsystem-menu/finance.js` cạnh entry borrow-sell-requests.

### T10 thực thi — tách 2 phần
- T10a (BE cờ) DONE inline: commit hrm-api 8b9e77bd6. Cờ `is_can_create_borrow_sell = BorrowSell::userCanCreate() && $this->canApprove()` trên BorrowSellRequestDetailResource. Ruling T10a-inline: không test riêng (mirror 5 cờ sibling), phủ bởi review whole-branch. php -l OK.
- T10b (FE) dispatch sonnet. BASE hrm-client: dbac538f129d0710878c9b7759bf64225bf6eb95. FE giữ UNCOMMITTED (nhất quán Phase 1 FE staged/working-tree). Review qua working-tree diff.
- Sửa Ruling T10-menu: menu finance.js:170 ĐÃ có placeholder `{ label: 'Phiếu xuất bán hàng mượn' }` (không link) → chỉ THÊM `link: '/finance/borrow-sells'`, KHÔNG tạo entry mới.

### Task 10: complete (T10a BE + T10b FE)
- T10a: commit hrm-api 8b9e77bd6 (cờ is_can_create_borrow_sell).
- T10b: FE uncommitted — api.js (mới) + nút "Lập phiếu bán" (_id/index.vue) + menu link (finance.js). Implementer af61de39f0ccd2ec4 DONE_WITH_CONCERNS (concern chỉ do môi trường: node -c coi export là CJS — verify qua .mjs PASS; eslint không có local — bỏ qua theo brief).
- Task review INLINE (controller, wiring 3-file trivial đã soi từng dòng): Spec ✅ PASS — api.js 4 hàm (list/show/store/printData) khớp route BE `/v1/finance/borrow-sells` (verify prefix api.php:43+767); nút gate `data.is_can_create_borrow_sell` (fail-closed, KHÔNG hardcode true), primary+ri-shopping-cart-2-line+size sm, đặt sau In trước Từ chối; goCreateSell dùng this.requestId → /finance/borrow-sells/create?request_id; menu:170 thêm link. Quality APPROVED — button-convention OK, mirror Phase 1 sạch.
- Review package: task-p2-10b-review-package.txt (diff _id/index.vue hiện toàn file do Phase 1 FE chưa commit — nhiễu chấp nhận).

## Task 11 — Màn DANH SÁCH borrow-sells (pages/finance/borrow-sells/index.vue)
BASE hrm-client: dbac538 (uncommitted, review working-tree diff).
Brief: task-p2-11-brief.md. Mirror Phase 1 list, cắt bỏ tạo/sửa/duyệt/từ chối; filter chỉ 5 param BE đọc (code/contractable_type/status/startDate/endDate); action chỉ Xem (is_can_view); thêm cột Tổng tiền.

### Task 11: complete
- Implementer a381d36877df9a41f (sonnet) DONE. File tạo: hrm-client/pages/finance/borrow-sells/index.vue (uncommitted, mirror khuôn Phase 1).
- Task review INLINE (controller đọc toàn file + grep): Spec ✅ PASS — đúng 5 param filter (code/contractable_type/status/startDate/endDate) trong initialStateForm+buildParams; CONTRACT_TYPE_OPTIONS dùng chuỗi morph FirmContract/WrServiceContract; action dòng CHỈ Xem gate `!!item.is_can_view` (fail-closed); thêm cột Tổng tiền (formatMoney tự viết, không có helper sẵn); columnScreenKey/localStorage/pathsToKeep = finance_borrow_sells; giữ nguyên khối pagination fallback camelCase/snake_case (chống nhảy trang). Quality APPROVED — sạch: grep createItem/runRowAction/manager_approve/BaseConfirmModal/deny* = CLEAN, `can*=true` = CLEAN. contract_code còn lại chỉ là cột hiển thị (field BE trả) + comment, KHÔNG phải filter param.
- Eslint không chạy được (project không có local, npx kéo v10 lỗi Node 14) — bỏ qua theo brief, thay bằng grep tự kiểm.

### Ruling T12-objectable (BE additive — gỡ blocker T12)
- Phát hiện: `BorrowSellRequestDetailResource` products map KHÔNG expose `objectable_id`/`objectable_type`, nhưng payload T8 (Ruling T8-payload) BẮT BUỘC cần 2 field này để FE dựng { products:[{objectable_id, objectable_type, details:[...]}] }.
- Quyết: thêm `objectable_id` + `objectable_type` vào products map (đọc thẳng $p->objectable_id/type). Additive, giống T10a. Rẻ hơn nhiều so với rework T7/T8 (đã approved đọc objectable_id/type từ payload) sang borrow_sell_request_product_id.
- Cost nếu sai: 2 field thừa trên response detail Phase 1, revertible, không đổi hành vi field cũ. Đây là ruling (không stop): additive, revertible.
- Đã sửa inline: BorrowSellRequestDetailResource.php:100-102. php -l ngầm (chỉ thêm key mảng). CHƯA commit — gom cùng lần commit BE kế (hoặc để review whole-branch).

## Task 12 — Màn TẠO phiếu bán (pages/finance/borrow-sells/create.vue)
BASE hrm-client: dbac538 (uncommitted). Nhận request_id query → getBorrowSellRequest (Phase 1 action) đổ SP → nhập SL bán → submit storeBorrowSell payload qty-only.

### Task 12: complete
- Implementer DONE (report task-p2-12-report.md). 2 file tạo: `create.vue` (vỏ ~29 dòng, mixins PageTitleMixin+unsavedChildFormMixin) + `components/BorrowSellForm.vue` (form thật).
- Task review INLINE (controller đọc toàn bộ BorrowSellForm.vue + report): **Spec ✅ PASS / Quality APPROVED**.
  - Gate fail-closed `is_can_create_borrow_sell` trong loadRequest() (BE trả, KHÔNG hardcode true) → redirect nếu thiếu quyền.
  - Payload qty-only đúng Ruling T8-payload: `{borrow_sell_request_id, products[].{objectable_id, objectable_type, details[].{product_export_request_detail_id, qty}}}`, KHÔNG gửi field tiền/giá; filter details qty>0 + bỏ product rỗng.
  - Getter tiền verbatim Phase 1 (groupDisplayPrice=0 khi type=2/WrService; groupTotalAfterExtra/Allocated/VatCost/discount khớp). Box tổng đọc getter form-level.
  - Entry-point khép kín: T10 nút "Lập phiếu bán" → `create?request_id=<id>`; form đọc `$route.query.request_id` → thiếu thì toast + replace về list.
  - markFormPristine() (mixin thật, brief nhầm captureFormSnapshot) + markFormSaved() sau lưu. Redirect `/finance/borrow-sells/<id>` sau tạo.
  - grep sạch (ContractPicker|ExportRequestPicker|rebuildGrid|selectedExportRequests|change_price|_priceError|can*=true = 0 match). Template tag cân bằng.
- **Deviation benign chấp nhận:** totalColumns=15/16 (Phase 1=16/17) vì Phase 2 gộp cận `max_qty` vào ô Bán (`/ {{max_qty}}`) thay cột "Đang mượn" riêng; `groupBorrowSellExceedsContract` chỉ cảnh báo UI (đỏ), KHÔNG chặn submit (brief B3 — validate chỉ theo max_qty per-detail; BE T7 hard-validate tồn thực là nguồn chặn thật).
- eslint không chạy (Node 14, không local) — bỏ qua theo brief, thay grep.
- **Task 12: complete** (FE uncommitted, nhất quán Phase 1).

## Task 13 — Màn CHI TIẾT (tab Hạch toán) + IN (pages/finance/borrow-sells/_id/)
BASE hrm-client: dbac538 (uncommitted). Brief: task-p2-13-brief.md. 2 file: `_id/index.vue` (2 tab: Thông tin phiếu + Hạch toán) + `_id/print.vue`. Import show/printData từ `../api` (T10b), KHÔNG api Phase 1.
- Implementer a1468216d42fdcd5a (sonnet) DONE (report task-p2-13-report.md). 2 file tạo (uncommitted).

### Task 13: complete
- Task review INLINE (controller đọc toàn bộ 2 file): **Spec ✅ PASS / Quality APPROVED**.
  - `_id/index.vue`: 2 tab b-tabs/b-tab (không có V2Base tab component). Tab 1 mirror Phase 1 (info + KH + bảng hàng hoá + box tổng đọc `sum_*` BE tính sẵn qua formatMoney). Tab 2 Hạch toán: render `accounting[]` đúng — `Nợ = type===1 ? formatMoney(value):''`, `Có = type===2`, TK đối ứng `(ref||[]).join(', ')`, note; nhánh `accounting_error` (banner alert-warning, KHÔNG render bảng); rỗng+no-error → "Chưa có dữ liệu hạch toán."; dòng tổng `sumDebit`/`sumCredit` (filter type reduce value) — 2 số phải cân.
  - Gate nút In `v-if="data.is_can_view"` + guard `printPage() { if(!this.data.is_can_view) return }` (fail-closed, KHÔNG hardcode true). Import `show` từ `../api`.
  - `_id/print.vue`: layout 'print', `printData` từ `../api`, render template Vue thường (KHÔNG v-html) đúng field BorrowSellPrintResource; tiêu đề "PHIẾU XUẤT BÁN HÀNG MƯỢN"; bảng SP + dòng Tổng thành tiền (`sumThanhTien` reduce `thanh_tien`); formatMoney null→'—'; `$printContent({styles, pageMargin})` trong user-gesture. Import `printData` từ `../api`.
  - grep `can[A-Za-z]*\s*=\s*true` = 0 match cả 2 file (report + controller xác nhận). Tag balance OK.
- **Ruling T13-print-newtab:** brief A5 yêu cầu "làm y hệt khuôn Phase 1". Phase 1 `_id/index.vue:494` dùng `window.open('/finance/borrow-sell-requests/{id}/print', '_blank')` (tab mới); T13 ban đầu dùng `$router.push` (cùng tab). Controller sửa 1 dòng `printPage()` → `window.open('/finance/borrow-sells/{id}/print', '_blank')` cho khớp. Cost nếu sai: chỉ đổi tab-mới↔cùng-tab, revertible 1 dòng.
- **Concerns T13 → defer backlog (display-only, không chặn merge):**
  - FU-4: `BorrowSellDetailResource.details[]` chưa expose `product_export_request_code` → tab 1 hiện "Nguồn phiếu mượn #{id}" thay vì mã. Nếu muốn mã: thêm 1 field vào BorrowSellDetailResource (giống BorrowSellRequestDetailResource:127). Ngoài scope T13 (FE-only).
  - FU-5: chưa có bảng màu status pill cho BorrowSell → `status_name` render text thường. Nicety.
- eslint không chạy (Node 14, không local) — bỏ qua theo brief, thay grep + tag-balance.
- **Task 13: complete** (FE uncommitted, nhất quán Phase 1).

## Task 14 prep — baseline test (chạy trong lúc T13 chạy, 2026-09-07, DB erp_hrm_check)
Xác nhận DB env: `DB_DATABASE=erp_hrm_check` (gộp) + SECOND cũng erp_hrm_check. Chạy từng file (phpunit.xml quirk: truyền nhiều path CLI chỉ chạy file đầu → chạy tách):
| Test | Kết quả | Phủ verify T14 |
|---|---|---|
| BorrowSellPostingFirmTest | OK 1 test / 6 assert | V1 Nợ=Có; V2 giá vốn Có **157** Firm |
| BorrowSellPostingWrServiceTest | OK 1 test / 9 assert | V1; V2 Có **1561**×coef; V3 chiết khấu **5211** chỉ WrService |
| BorrowSellDeliveryTripAccountingTest | OK 2 tests / 13 assert | V8 chuyến xe 6427/3351 + no-op khi không gắn |
| BorrowSellStoreTest | OK 3 tests / 13 assert | V4 returned_by_sell atomic; V5 parent status=1 DA_DUYET; account_details sinh |
| ProductExportPostingRegressionTest | OK 1 test / 2 assert | V6 xuất-thường bút toán không đổi + Nợ=Có |
→ V1-V6 + V8 ĐÃ phủ bởi test tự động xanh.
- **Ruling T14-V7 (chấp nhận phủ đơn vị + đọc code cho gate 403, KHÔNG dựng JWT actingAs):** V7 gate 403 khép kín bằng: (a) test `test_user_can_create_is_fail_closed_without_auth` assert `BorrowSell::userCanCreate()=false` cho guest (khoá regression hardcode-true); (b) đọc code `BorrowSellController::store` dòng 48 `if(!BorrowSell::userCanCreate()) return responseJson('Không đủ quyền!',403)` TRƯỚC khi vào service (grep xác nhận dòng 48/66/76 đều 403). Điều kiện gate + wiring đều verify. Test end-to-end 403 (skip ở BorrowSellApiTest) cần dựng employee+spatie role+JWT actingAs — chi phí cao, dễ flaky, giá trị biên. — Cost nếu sai: nếu ai đó sau này đổi controller bỏ gate mà không đổi userCanCreate() thì unit test không bắt được; nhưng review whole-branch + code hiện tại đã có gate. Chấp nhận.
- Còn lại T14 = document mapping trên (đã đủ) + spot-check DB thật 1 phiếu Firm + 1 WrService nếu có dữ liệu (tùy chọn, không chặn).

### Task 14: complete — spot-check DB thật (2026-09-07, erp_hrm_check)
- borrow_sells: 4303 phiếu (dữ liệu ERP port sang). account_details morph HRM (`Modules\Finance\...\BorrowSell`) = 0 (code HRM MỚI chưa chạy tạo phiếu production — đúng kỳ vọng). Dữ liệu lịch sử dùng morph ERP `App\Model\Warehouse\BorrowSell` (77166 dòng) — dùng làm tham chiếu cấu trúc port.
- **V1 Nợ=Có (dữ liệu thật):** Firm #4312 No=Co=1.219.638 ✅; WrService #4228 No=Co=1.646.613 ✅.
- **V2 giá vốn nhánh (dữ liệu thật):** Firm #4312 Có có **157** (KHÔNG 1561) ✅; WrService #4228 Có có **1561** (KHÔNG 157) ✅.
- **V3 làm rõ (KHÔNG bug):** Firm #4312 cũng có 5211 bên Nợ → thoạt nhìn nghịch V3 "5211 chỉ WrService". Soi code: 5211 dùng ở CẢ 2 nhánh nhưng KHÁC mục đích/đối ứng:
  - Firm: 5211 do `bonusContractAccounting` (SupportAccountingTrait #4: Thưởng thực hiện HĐ, Nợ 5211 / **Có 35241**) — khớp ERP #4312 (Có có 35241).
  - WrService: 5211 do cụm CHIẾT KHẤU riêng (BorrowSellPostingService:305, Nợ 5211 + 33311 / **Có 1311**, work CKHH=20).
  → V3 câu chữ chưa chính xác; ý đúng = "cụm chiết khấu 5211-ref-1311 (work CKHH) chỉ ở WrService". Port trung thành, test BorrowSellPostingWrServiceTest phủ đúng cụm này.
- **Bảng phủ verify (chốt):** V1 ✅ (test + data thật) · V2 ✅ (test + data thật) · V3 ✅ (test WrService + làm rõ trên) · V4 ✅ (BorrowSellStoreTest returned_by_sell atomic) · V5 ✅ (BorrowSellStoreTest parent status=1) · V6 ✅ (ProductExportPostingRegressionTest) · V7 ✅ (Ruling T14-V7: unit fail-closed + đọc gate 403) · V8 ✅ (BorrowSellDeliveryTripAccountingTest 6427/3351 + no-op).
- **Task 14: complete.** Toàn bộ 14 task Phase 2 xong → chuyển sang final whole-branch review (most capable model).

## Final whole-branch review — adjudication (2026-09-07)
Reviewer (most capable) verdict: **SHIP-with-nits** — 0 Blocker / 0 High / 1 Medium (F1) / 3 Low (F2/F3/F4). Report: `sdd/final-review-report.md`.

### F1 (Medium) — updateWarehouse bỏ sót side-effect rollup so ERP → **RULING: FIX (đã fix)**
Điều tra 2 sub-claim của F1:
- **Firm `warehouse_exported_qty`/`need_repair` trên firm_contract_tab_products (ERP ~481-483): FALSE-POSITIVE.** Các dòng này nằm TRONG block `if (count($this->tabs))` = nhánh tabs/KM mà HRM chủ ý bỏ (Ruling T7-6). Ngoài scope → KHÔNG fix. Firm cấp-1 `exported_qty` HRM đã cộng đúng (updateWarehouse dòng 254 ↔ ERP 414).
- **WrService `exported_qty` cấp-2 lồng (ERP 416-421): SÓT THẬT.** Nhánh HANG_THUONG, không dính tabs. HRM chỉ cộng cấp-1 `wr_service_contract_items` (dòng 254), thiếu cấp-2 trên `$contract_item->objectable`.
- Verify tất định trước khi fix: `wr_service_contract_items.objectable_type` chỉ có 3 FQN (`App\Model\Customers\WrServiceContractProductItem` 3080 / `...WrServiceContractMerchandise` 789 / `...WrServiceContractExtendProductServiceItem` 96); cả 3 bảng con tồn tại + CÓ cột `exported_qty`. HRM KHÔNG đọc cột cấp-2 ở đâu (grep sạch) → bổ sung KHÔNG double-count.
- **Fix áp dụng** (BorrowSellService.php, 2 file, +33 dòng — CHƯA commit, chờ user):
  - const `WR_SERVICE_NESTED_TABLES` (map 3 FQN→bảng) + helper pure `nestedWrServiceTable()`.
  - Trong updateWarehouse nhánh non-Firm: đọc row cấp-1 theo `$p->objectable_id`, map type→bảng, `increment('exported_qty', (float)$p->qty)` ATOMIC (Ruling T7-3, KHÔNG `+=`/save). Dùng `$p->qty` (khớp ERP + cấp-1, KHÔNG ×unit_coefficient). Type lạ/null → bỏ qua, không throw.
  - Test `test_nested_wr_service_table_maps_all_three_types_and_null_for_unknown` (BorrowSellStoreTest, 4/4 PASS 18 assert).
- **Scoped re-review (haiku):** báo 1 HIGH "null access $wrItem" — kiểm lại là **FALSE-POSITIVE** (dòng trên `$nestedTable = $wrItem ? ... : null` ⇒ khi $wrItem null thì $nestedTable null ⇒ `&&` short-circuit không truy cập $wrItem->objectable_id). Vẫn thêm guard tường minh `$wrItem &&` (zero-cost, bỏ phụ thuộc invariant ngầm). Re-lint + re-test PASS.
- **Cost nếu sai:** cực nhỏ — cột cấp-2 exported_qty (phía ERP đọc trong DB gộp) cộng dư/thiếu; HRM không đọc; revertible, không đụng cân bằng bút toán/guard tồn khả bán.

### F2 (Low, CONFIRMED cosmetic) — comment sai ở StoreBorrowSellRequestRequest::authorize → **RULING: PARK (FU-6)**
Comment nói gate ở middleware `checkPermission` (route) nhưng gate 403 thật ở `BorrowSellController::store` qua `userCanCreate()`. Chỉ comment, không đổi hành vi. File thuộc delta Phase 1 đang uncommitted → không đụng lúc này. Cost nếu sai: người đọc sau hiểu nhầm vị trí gate (route↔controller); gate thật vẫn đúng. Backlog FU-6.

### F3 (Low, CONFIRMED design choice) — tab Hạch toán tính lại live thay vì đọc account_details → **RULING: ĐÓNG (by-design)**
Đúng Ruling T9-accounting-in-detail (đã chốt trước). Nếu sau này cần "sổ đúng như đã post" thì đọc `account_details`; hiện chấp nhận. Không action.

### F4 (Low, PLAUSIBLE biên hiếm) — catch \Throwable ở postAccounting nuốt ValidationException → **RULING: ĐÓNG (chấp nhận)**
Ghi sổ nội bộ (không phải validate payload user — payload đã validate ở StoreBorrowSellRequest + service trước đó). Lỗi hạch toán = server error → 500 hợp lý, không phải 422. Rule CLAUDE.md rethrow-ValidationException nhắm form-validate người dùng, không nhắm posting nội bộ. Reviewer cũng kết "không cần sửa". Không action.

### Kết luận Phase 2
14/14 task xong + final review SHIP-with-nits đã adjudicate: F1 FIXED (uncommitted), F2 park FU-6, F3/F4 đóng by-design. **BE fix F1 CHƯA commit** (chỉ 2 file: BorrowSellService.php + BorrowSellStoreTest.php) — chờ user cho phép commit. FE toàn bộ Phase 2 vẫn uncommitted đúng quy ước Phase 1. Phase 1 BE staged vẫn giữ nguyên (không đụng).
