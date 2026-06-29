# STATUS.md

## Đang làm

- warehouse-management (Quản lý kho) → @manhcuong → .plans/warehouse-management/plan.md
  Spec: docs/superpowers/specs/2026-06-28-warehouse-management-design.md · Plan P1: docs/superpowers/plans/2026-06-28-warehouse-management-phase1.md
  Phân hệ Quản lý kho mới (greenfield, module `Modules/Warehouse` + `pages/warehouse`). Engine hướng A: sổ cái `stock_movements` + cache `inventories`; chỉ số lượng; workflow Nháp→Chờ duyệt→Đã duyệt (tồn đổi khi DUYỆT); ĐVT quy đổi về cơ bản; chặn cứng tồn âm; không scope cấp; permission từ 1124 (type=10). 5 phase: P1 Engine+Nhập, P2 Xuất(+HĐ), P3 Chuyển, P4 Kiểm kê, P5 Báo cáo.
  Checkpoint 2026-06-29: **CODE HOÀN THÀNH Phase 1 (Engine+Nhập) + Phase 2 (Xuất kho) BE+FE + FINAL REVIEW PASS cả 2** (subagent-driven 10+8 task, chưa commit). Final review opus: SẴN SÀNG BÀN GIAO, 0 Critical. Chi tiết .plans/warehouse-management/plan.md.
  - P1: module Warehouse; engine stock_movements+inventories+StockService; Nhập kho (WhReceipt*, permission 1124-1126). + popup phân hệ topbar (icon_kho.svg) + accordion phân quyền type=10 (Permission.vue).
  - P2: Xuất kho (wh_issues/items, WhIssueService approve=assertEnough+assertContractRemaining+postMovement âm trong transaction+lockForUpdate; gắn HĐ ĐVT khoá / tự do; permission 1127-1129) + Sale accessor `quantity_issued` (tab "Thông tin xuất hàng" ra số thật). FE store/form(HĐ-tự do)/list/detail/menu "Xuất kho". Smoke test PASS (tồn giảm, chặn vượt tồn+vượt HĐ).
  - Permission DB dev: ĐÃ seed (612 quyền) + gán role 1 đủ 1124-1129 + cache clear.
  - Important TRACK (chưa fix, chờ user OK vì đụng hàm dùng chung): TOCTOU race StockService::assertEnough/assertContractRemaining (đọc tồn không lockForUpdate).
  - CÒN (user dev server, FE Node v12 chưa build): restart+re-login test menu/guard/E2E nhập+xuất→tồn; commit 2 repo. Kế tiếp: Phase 3 Chuyển kho.

- sale-dashboard (Dashboard Kinh doanh) → @manhcuong → .plans/sale-dashboard/plan.md
  Spec: docs/superpowers/specs/2026-06-28-sale-dashboard-design.md
  Trang tổng quan phân hệ Kinh doanh (Modules/Sale + pages/sale/dashboard), dữ liệu co giãn theo cấp quyền. 4 khối: KPI chờ duyệt (BG/HĐ) + Doanh số theo thời gian (bar 2 series) + Tỉ lệ chuyển đổi BG→HĐ + Top 10 KH. 1 endpoint GET /v1/sale/dashboard (aggregate SQL). Quyết định: A=permission MỚI 1123, B=scope theo cấp viết RIÊNG (không sửa getListForUser).
  Checkpoint 2026-06-28: **CODE HOÀN THÀNH BE+FE + REVIEW PASS** (subagent-driven 2 phase, chưa commit). Final review opus: SẴN SÀNG BÀN GIAO, 0 Critical/Important.
  - BE (nhatlinh-api): permission 1123 "Xem dashboard kinh doanh" (group Báo giá bán, type 4); SaleDashboardService (applyScope RIÊNG nhân bản getListForUser + applyExtraFilter giao-không-nới; getData: KPI chờ duyệt status=2 không lọc ngày, revenue_by_month status=3 theo approved_at fill đủ tháng, conversion tử số whereIn quotationIds đã scope, top_customers whereIn 2-query tránh ambiguous); DashboardRequest; DashboardController@index; route /v1/sale/dashboard gắn checkPermission. Entity KH thật = CustomerCategory. php -l sạch; E2E HTTP có auth CHƯA chạy (DB dev thiếu users).
  - FE (nhatlinh-client): store/sale-dashboard.js; pages/sale/dashboard/index.vue (thanh lọc Công ty/Phòng + 2 datepicker mặc định đầu năm→nay, 4 KPI card link sang 2 màn approval, 3 chart ApexCharts: doanh số theo tháng bar 2 series + chuyển đổi bar ngang + top 10 KH bar ngang, empty-state, shortMoney/formatNumber); menu "Tổng quan" sale.js isShow=['Xem dashboard kinh doanh']. FE KHÔNG build được (node cũ) → user test trình duyệt.
  - **Fix màn Role (Phase 3)**: nhóm Báo giá bán/Hợp đồng/Dashboard không hiện ở /timesheet/setting/roles/add vì bị gán chung type=4 (phân hệ Giao việc đang ẩn). → Tách **type=9 "Phân hệ kinh doanh"**: seeder đổi type 4→9 cho group Báo giá bán+Hợp đồng (1105-1123); UPDATE DB dev; thêm accordion filterPermission(9) trong components/setting/Permission.vue. Đã verify không chỗ nào lọc Sale theo type=4 (PermissionService chỉ ->get()). php -l sạch.
  - CÒN: user (1) reload màn role → thấy accordion "Phân hệ kinh doanh" (2 nhóm) → gán quyền + lưu; (2) seed/gán quyền 1123 + test menu dashboard hiện/ẩn + 403; (3) test render 4 KPI + 3 chart với data thật; (4) test scope theo cấp; (5) commit 2 repo. Lưu ý deploy: seeder Sale nay type=9; nếu DB cũ đã seed type=4 phải UPDATE lại type=9; KHÔNG sửa getListForUser.

- contract (Hợp đồng) → @manhcuong → .plans/contract/plan.md
  Spec: docs/superpowers/specs/2026-06-27-contract-design.md
  Hợp đồng lập từ báo giá ĐÃ DUYỆT (Modules/Sale + pages/sale/contract), workflow giống báo giá. Snapshot Bên A (KH)/Bên B (Công ty) đầy đủ (MST/Số TK/người đại diện/email/SĐT). 1 báo giá → 1 HĐ; chỉ created_by báo giá tạo được; dòng hàng khoá (copy). Mẫu in tuỳ chỉnh tái dùng print_templates Quyết định (thêm type "Hợp đồng kinh tế" + {{BANG_HANG_HOA}}). Permission 1115-1122. Danh mục: +Số TK (KH) +Số TK/người đại diện (Công ty).
  Checkpoint 2026-06-27: **CODE HOÀN THÀNH 5 PHASE/13 TASK + FINAL REVIEW** (BE+FE, subagent-driven, chưa commit).
  - P1 DB+Entities: sale_contracts (+snapshot a_*/b_*, print_template*), sale_contract_items, +bank_account (KH), +bank_account/representative (Công ty). Entity SaleContract (HD-YYYY-NNNNN) + Item.
  - P2 BE: SaleContractService (createFromQuotation snapshot A/B + copy items khoá + 1-1 check + chỉ created_by; updateOrCreate chỉ header; submit/approve/reject), Request, 2 Resource, Controller, Routes /v1/sale/contracts, permission 1115-1122 (đã tạo+gán Admin company 1). Móc is_can_create_contract/has_contract ở báo giá.
  - P3 Mẫu in: type "Hợp đồng kinh tế" (7) + biến trong PrintTemplateVariable; buildPrintData + {{BANG_HANG_HOA}} tự sinh bảng + TONG_TIEN_CHU (convertNumberToWords); endpoint /print.
  - P4 FE: menu sidebar + list + detail (Bên A/B + items read-only + footer workflow) + ContractForm (snapshot sửa được + FormPrintTemplateComponent + Lưu/Lưu&Gửi duyệt) + print page + nút "Tạo hợp đồng" trên báo giá. store sale-contract (update=PUT).
  - P5 Danh mục: Số TK (KH) + Số TK/người đại diện (Công ty) vào form+resource.
  - Verify: php -l sạch; E2E tinker (tạo HĐ→mẫu in render bảng→submit→approve) PASS; 1-1 chặn OK. Final review opus: 0 lỗi luồng chính; fix 2 (Critical: Company fillable thiếu bank_account/representative→mất data; Important: filter dept/part). Minor còn (keyword chỉ code) không chặn.
  - CÒN: user reload FE test (Node v12 chưa build); commit 2 repo. Lưu ý team: seed permission 1115-1122 + gán role khi deploy.
  Checkpoint 2026-06-28: **TINH CHỈNH HĐ/BÁO GIÁ + 2 MÀN CHỜ DUYỆT** (BE+FE, chưa commit) — chi tiết .plans/contract/plan.md.
  - HĐ: ContractForm chia **2 tab** (Thông tin HĐ / Mẫu in), bỏ tiêu đề thừa; **Số HĐ** input bắt buộc (unique) cùng hàng Ngày HĐ; Bên A người đại diện = **select** từ DS KH (mặc định đầu) + chức vụ; Bên B người đại diện + chức vụ = **read-only lấy từ Người điều hành (owner_id) công ty** (a_/b_representative_role mới); Bên B STK từ công ty. Mẫu in: đổi tên type → **"Hợp đồng bán hàng"**, form HĐ khoá chỉ lấy mẫu loại này (prop lockedTypeId); ép font **Times New Roman** trong buildPrintData; **preview mẫu in vào popup** (ContractPrintPreview, báo giá đã sẵn popup). Lưu/Lưu&Gửi duyệt → **redirect danh sách** (logic chung). Bỏ thông tin KH trùng ở khối trên màn xem.
  - Danh mục KH: Người đại diện + Ngân hàng thành **section bảng động** (như Người liên hệ): bảng customer_representatives + customer_bank_accounts; ghi chú dạng input. Danh mục Công ty: thêm "Người điều hành/chức vụ" dùng owner; **drop** cột representative/representative_role không dùng.
  - **Bug fix**: sửa HĐ không lưu/redirect được do DetailSaleContractResource trả contract_date d/m/Y (rule date từ chối) → đổi Y-m-d + format FE; validate báo lỗi inline tại field (bỏ toast) + nhảy về tab lỗi; menu "Mẫu in" chuyển từ Quyết định → **HCNS** (cả trang + route).
  - **2 màn chờ duyệt** (`/sale/quotation-approval`, `/sale/contract-approval`): khoá status=Chờ duyệt, Duyệt/Từ chối inline, gated quyền "Duyệt báo giá bán"/"Duyệt hợp đồng"; tạo 3 mẫu in "Hợp đồng bán hàng" demo.
  - CÒN: user reload (restart dev server) test toàn bộ; commit 2 repo. Lưu ý deploy: migrate các bảng/cột mới (customer_representatives, customer_bank_accounts, sale_contracts.a_/b_representative_role, companies.representative_role đã drop).
  Checkpoint 2026-06-28: **UI danh sách + chi tiết 2 tab + Xuất Excel** (chưa commit). DS: mã HĐ link → chi tiết, nút In (ContractPrintPreview), nút **Xuất Excel** (BE SaleContractExport + SaleContractController::export, route /contracts/export trước /{id}); chi tiết HĐ chia **2 tab** (Thông tin HĐ / Thông tin xuất hàng — bảng bỏ cột giá, thêm "Số lượng đã xuất" cạnh "Số lượng", xanh khi đủ, hiện "-" vì chưa có luồng xuất); Bên A/B + Tên in hoa+đậm. Review opus Spec ✅/Quality Approved.

- price-tier-management → @manhcuong → .plans/price-tier-management/plan.md
  Spec: docs/superpowers/specs/2026-06-26-price-tier-management-design.md
  Quản lý giá hàng hoá động: bỏ cột cứng `price_p3/p5/p7/p10`, thêm danh mục **Bảng giá** (price_tiers: name+percent+status, mã BG.XXXX, dùng chung) + lịch sử sửa đổi. Hàng hoá chỉ nhập P0 (NET), BE tự tính & lưu snapshot `product_unit_prices` (= P0×(1+%/100)). Nút "Tính lại" hàng loạt trên danh mục. Permission 1113-1114. 3 phase: (1) danh mục Bảng giá + lịch sử, (2) đổi cấu trúc giá product + FE form cột động + seeder, (3) nút tính lại.
  Checkpoint 2026-06-26: **CODE HOÀN THÀNH TOÀN BỘ 3 PHASE + FINAL REVIEW PASS** (subagent-driven, 13 task, chạy branch hiện tại chưa commit).
  - Phase 1 (BE Task 1-7 + FE Task 8): danh mục Bảng giá — migration price_tiers + price_tier_histories, Entity PriceTier (getNextCode BG.XXXX, isCanDelete chặn xoá khi đã áp hàng hoá) + PriceTierHistory, Request extend BaseRequest, Service (CRUD + ghi history create/update/delete), 3 Resource (ApiResource), Controller (delete để ValidationException bubble → 422), routes + permission 1113-1114 (group "Danh mục chung"). FE: menu + list page (badge V2BaseBadge) + modal thêm/sửa (validate inline touched) + modal lịch sử, global store actions.
  - Phase 2 (Task 9-11): đổi cấu trúc giá — migration tạo product_unit_prices (snapshot) + DROP price_p3/p5/p7/p10 khỏi product_units (giữ price_p0). ProductService.syncUnitPrices tính snapshot = round(p0×(1+%/100),2) theo tier ACTIVE; DetailProductResource trả tier_prices; sửa kèm ProductRequest + ProductController eager-load. FE ProductForm: cột giá render động theo getAll tier, P0 editable, cấp giá read-only preview. Đã dọn sạch mọi ref price_p3.. (trừ migration).
  - Phase 3 (Task 12-13): PriceTierService.recalcAllProducts (chunkById, dọn snapshot tier non-active, áp % mới hàng loạt) + endpoint POST price-tiers/recalc-products + nút FE "Tính lại giá hàng hoá" (confirm → toast count).
  - Verify: php -l + migrate + smoke-test tinker (công thức 1000→1050/1100, đổi 8%→1080, recalc 51 unit) PASS. Final review opus: 0 Critical, fix 1 Important (modal map lỗi 422 beErrors.name[0]→bỏ [0]).
  - Đã tối ưu N+1: index() dùng withCount('productUnitPrices'), isCanDelete() đọc count.
  - Setup dev DONE: tạo permission 1113/1114 + gán role 18 Super admin (insert pivot trực tiếp + reset cache; KHÔNG chạy seeder vì seeder TRUNCATE bảng permissions → sẽ phá phân quyền). Khi deploy: 2 dòng Permission đã có sẵn trong PermissionsTableSeeder.
  - **3 lỗi user test đã fix**: (1) menu không hiện = phiên login cũ chưa có quyền → re-login; (2) Vue warn "errors already defined" = vee-validate inject computed errors → đổi errors→formErrors trong AddPriceTierModal; (3) load trang 500 = index() paginate 2 lần (service + apiPaginate) → sửa index() trả query builder.
  - **Phase 4 (Task 14-15) — auto-fill giá vào Báo giá** (theo yêu cầu mới): thêm cột `sale_quotations.price_tier_id` (nullable, null=P0) + fillable/service/request/DetailResource; `category/products/getAll` load thêm `productUnits.prices` (snapshot giá cấp). FE QuotationForm: dropdown "Cấp giá" đầu phiếu (sentinel 0=Giá gốc P0 + các cấp ACTIVE), chọn cấp → đơn giá MỌI dòng tự điền theo cấp+ĐVT, **đơn giá khoá read-only**; nguồn giá ưu tiên snapshot, thiếu thì P0×(1+%/100); lưu price_tier_id vào phiếu, sửa phiếu khôi phục selector + giữ giá đã lưu. php -l + migrate OK.
  - CÒN LẠI: user re-login + test UI đầy đủ (FE chưa build do node v12); test auto-fill giá báo giá (chọn cấp → giá điền/khoá); xác nhận Báo giá không vỡ; commit 2 repo. Lưu ý team: route:list toàn cục fail do lỗi CÓ SẴN ở DecisionController (không liên quan feature).

- quotation → @manhcuong → .plans/quotation/plan.md
  Spec: docs/superpowers/specs/2026-06-25-quotation-design.md
  Báo giá BÁN độc lập trong phân hệ Kinh doanh (Modules/Sale + pages/sale/quotation) — KHÁC bản Báo giá pipeline đã có ở Modules/Assign (giữ nguyên). Master-detail (sale_quotations + sale_quotation_items), workflow Nháp→Chờ duyệt→Đã duyệt/Từ chối, CK tổng phiếu, dompdf, phân quyền theo cấp.
  Checkpoint 2026-06-25: **CODE HOÀN THÀNH + UX revamp + 8 bổ sung + E2E PASS** (BE+FE, branch `quotation` chưa commit).
  - Core: 6 phase subagent-driven, review opus SẴN SÀNG; BE migrate OK, dompdf 1.0.2, 8 permission id 1105-1112.
  - UX/UI revamp theo style Assign (info-table/sticky table/totals-card), bỏ pipeline fields.
  - 8 bổ sung: địa chỉ/email KH, SĐT liên hệ, Bảo hành (cột `warranty_time`), editor Điều khoản (`terms`), kéo-thả dòng, validate trùng mã (distinct), Đơn giá currency-format, chiết khấu %⇄tiền.
  - E2E Playwright (e2e/) 6/6 PASS; BE verify tổng tiền đúng. Setup dev (user duyệt): cấp quyền role 3/18/21 company 1 + seed *.E2E.
  Checkpoint 2026-06-26: thêm **modal chọn hàng hoá** (lọc keyword/nhóm/hãng SX/nước SX/phân loại + chọn hàng loạt + báo "đã thêm"), **cột Thông số KT + ẩn/hiện cột**, **tổng hợp chi phí 5 dòng**, tinh chỉnh UI, **tính năng In** (print preview thay Xuất PDF), fix **toast 403 loadContacts** (endpoint Sale customer-contacts), fix **FE route guard** (checkPermission đăng ký menu category+sale + isShow → chặn truy cập khi thiếu quyền), **seeder 50 hàng hoá TBTH**. E2E 6/6 PASS; route-guard kiểm 2 chiều.
  - Setup dev (user duyệt): sync+gán 18 quyền "Danh mục chung" cho role 3/18/21 company 1 (DB dev chưa seed MODULE-1 dù seeder đã có).
  Checkpoint 2026-06-27: **BỔ SUNG BÁO GIÁ + SETUP DB CHUẨN** (BE+FE, chưa commit) — chi tiết trong .plans/quotation/plan.md.
  - Auto-fill cấp giá (đơn giá khoá), **banner công ty bản In** (tham khảo Assign), **footer người duyệt** (Tổng Net/Bán/CK/sau CK + cảnh báo bán dưới giá Net + confirm khi duyệt), nút **Lưu & Gửi duyệt**, **menu Kinh doanh xuống sidebar** (luôn hiện).
  - Danh sách: fix tiêu đề cột (label→title); thêm 4 cột Ngày tạo/Người tạo/**Ngày duyệt**/**Người duyệt** (cột mới `approved_at`/`approved_by`); datetime `d/m/Y H:i:s`, ngày `d/m/Y`. Validate hiệu lực phải SAU ngày báo giá.
  - SaleDemoSeeder (KH + cấp giá + recalc + 3 phiếu demo). DB chuẩn `nhatlinh`: migrate + 597 quyền gán role Admin(1) + 50 hàng hoá.
  - Bug fix khi test: company_id quyền (0→1) gây ẩn menu; list 500 (paginate 2 lần); errors→formErrors (vee-validate); phiếu seed ẩn (created_by null).
  - Còn: user reload test UI đầy đủ + commit 2 repo. Lưu ý team: seed quyền MODULE-1 + Báo giá bán + Bảng giá (1113/1114) khi deploy; chạy SaleDemoSeeder nếu cần data mẫu.
  Checkpoint 2026-06-28: **UI danh sách + Xuất Excel** (chưa commit). Mã BG là link → chi tiết; nút **Xuất Excel** (#actions) — BE SaleQuotationExport + QuotationController::export (getListForUser scope + Resource resolve, route /quotations/export trước /{id} + checkPermission như index), FE tải arraybuffer theo filter. Review opus Spec ✅/Quality Approved (fix 3 minor). Permission Sale đã tách **type=9 "Phân hệ kinh doanh"** (hiện trên màn role qua accordion mới).

- product-bom-inline → @manhcuong → .plans/product-bom-inline/plan.md
  Spec: docs/superpowers/specs/2026-06-06-product-bom-inline-design.md
  Đổi BOM thành inline trong tab hàng hoá (lưu nested), bỏ hẳn danh mục BOM riêng + permission BOM. Mỗi SP ≤1 BOM = bảng NVL; bỏ Mã/Tên BOM; status theo hàng hoá.
  Checkpoint 2026-06-06: **CODE HOÀN THÀNH** (BE+FE, subagent-driven, chạy main chưa commit). BE smoke-test 5 kịch bản PASS; FE compile sạch; đã xoá trang/menu/route/permission BOM. Còn: user test trình duyệt.

- MODULE 1 — Danh mục & Cấu hình: **CODE HOÀN THÀNH TOÀN BỘ** (2026-06-05, chạy main chưa commit).
  Tất cả BE smoke-test pass + FE reviewed. Còn lại: user test UI trên app + tạo file mẫu import .xlsx + commit.
  - DM-03 product-type-hierarchy (nhóm hàng cha-con, list đã đổi về phẳng theo yêu cầu)
  - DM-04 supplier-category (NCC + nhóm NCC + liên hệ)
  - DM-05 customer-category (KH mới `category_customers` + loại trường + liên hệ)
  - DM-06 warehouse-category (Kho + loại kho + thủ kho)
  - DM-02 product-bom (BOM nhiều/sp + default + dòng NVL + lịch sử)
  - DM-08+DM-01 product-catalog-extend (quy đổi ĐVT + phân loại mua sẵn/SX + NCC/BOM mặc định)
  Permission đã thêm: NCC 1097-98, nhóm NCC 1099-1100, KH 1101-02, Kho 1103-04, BOM 1105-06 (gán Super admin).

- supplier-category → @manhcuong → .plans/supplier-category/plan.md
  DM-04 — Nhà cung cấp + Nhóm NCC (2 entity + supplier_contacts).
  Checkpoint 2026-06-05: CODE HOÀN THÀNH (BE+FE, chạy main chưa commit). BE smoke-test pass. Còn: user test UI + tạo file mẫu import. Tiếp theo: #3 unit-conversion (DM-08) hoặc #4 customer-category (DM-05).

- product-type-hierarchy → @manhcuong → .plans/product-type-hierarchy/plan.md
  Spec: docs/superpowers/specs/2026-06-04-product-type-hierarchy-design.md
  DM-03 — đổi tên "Loại hàng hoá" → "Nhóm hàng hoá" + phân cấp cha-con (tree-table).
  Checkpoint 2026-06-04: CODE HOÀN THÀNH (BE+FE, chạy trên main chưa commit). BE đã smoke-test pass (tinker). Còn lại: user test UI trên app + tạo file mẫu import .xlsx. Tiếp theo: feature #2 supplier-category (DM-04).

- product-catalog → @manhcuong → .plans/product-catalog/plan.md
  Spec: docs/superpowers/specs/2026-06-03-product-catalog-design.md

## MODULE 1 — Danh mục & Cấu hình (overview)

- Bản đồ phân rã 7 feature: docs/superpowers/specs/2026-06-04-module-1-danh-muc-overview.md
- Thứ tự: (1) product-type-hierarchy DM-03 ← đang làm, (2) supplier-category DM-04, (3) unit-conversion DM-08, (4) customer-category DM-05 (entity KH MỚI trong Category, KH chính thức ERP), (5) warehouse-category DM-06, (6) product-bom DM-02, (7) product-catalog mở rộng DM-01.

## Chờ

- claude-config-repo → @manhcuong → .plans/claude-config-repo/plan.md
  Spec: docs/superpowers/specs/2026-05-16-claude-config-repo-design.md

## Đã làm

- manufacturer-category → @manhcuong → .plans/manufacturer-category/plan.md
  Hoàn thành: 2026-06-01 — CRUD + Import/Export + Lock/Unlock, code HSX.XXXX

- country-of-origin-category → @manhcuong → .plans/country-of-origin-category/plan.md
  Hoàn thành: 2026-06-01 — CRUD + Import/Export + Lock/Unlock, code NSX.XXXX

- product-type-category → @manhcuong → .plans/product-type-category/plan.md
  Hoàn thành: 2026-06-01 — CRUD + Import/Export + Lock/Unlock, code LHH.XXXX

- unit-category → @manhcuong → .plans/unit-category/plan.md
  Hoàn thành: 2026-06-01 — CRUD + Import/Export + Lock/Unlock, code DVT.XXXX

- ke-toan-module-scaffold → @manhcuong → .plans/ke-toan-module-scaffold/plan.md
  Hoàn thành: 2026-04-21 — Giữ làm mẫu chuẩn cho task scaffold module mới.
