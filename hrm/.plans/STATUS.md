# STATUS.md

## Đang làm

- erp-to-hrm-migration → @dnsnamdang → .plans/erp-to-hrm-migration/plan.md
  Trạng thái: **SIZING DONE — chờ DB production để đối chiếu bất đồng bộ T3 (2026-07-27)**. Umbrella hợp nhất ERP⊕HRM + chuyển 4 mảng (Báo giá · HĐ bán/firm · HĐ dịch vụ · Kế toán). **Mục tiêu lớn nhất = gộp chung 1 database** (không phải chỉ viết lại UI). ĐÃ CHỐT: chỉ gộp 1 pháp nhân `hrm_tpe`⊕`erp2326` (bỏ connection etek/tpe); đích = **1 schema HRM duy nhất** (HRM canonical); ERP repoint sang DB HRM + retire dần (Strangler); prefix legacy `tp_` phía ERP; KHÔNG ETL — colocate + dedupe dần theo domain. Phân tích: ERP 1.225 bảng / HRM 635 / **trùng tên 50** → phân tầng T0 auth(không merge)·T1 giả(rename, gồm `quotations`)·T2 danh mục·T3 lõi tổ chức(rủi ro CAO NHẤT)·T4 nghiệp vụ KH/HĐ. ~165 bảng 4 mảng phần lớn KHÔNG trùng → bê nguyên tên. T3 đã sync sẵn HRM→ERP (id lệch, map qua natural key: companies=tax_code, departments/employee_infos=code, employees=email, parts=name) → gộp 1 DB thì gỡ luôn sync. Lộ trình 2 phase: P1 hợp nhất hạ tầng (đạt "1 DB chung", data nguyên vẹn) → P2 viết lại UI + dedupe theo domain (T2→master/KH→báo giá→HĐ→kế toán).
  Blocker phụ: `Modules/Accounting/{Routes/api.php, module.json}` merge conflict → tinker không boot (dùng mysql CLI thay thế).
  Spec: docs/superpowers/specs/2026-07-27-erp-to-hrm-migration-design.md · phase2-risk-map.md · collisions-50-tables.txt
  Bước tiếp: user kéo DB production về local → verify cơ chế sync trong code (chốt đúng field mapping) → chạy lại harness đối chiếu → xuất danh sách bản ghi bất đồng bộ (id 2 bên) làm đầu vào bảng ánh xạ id merge T3.

- du-an-cha-con → @dnsnamdang → .plans/du-an-cha-con/plan.md
  Trạng thái: **DESIGN DONE — chờ user review spec (2026-07-20)**. Bổ sung quản lý dự án TKT (`prospective_projects`) theo cấp Dự án cha → Dự án con (Modules/Assign), từ bước dự án tới phê duyệt báo giá. Phát hiện: `parent_id` + picker "Dự án cha" (`RelatedSection.vue`) + `canDelete()` chặn cha có con ĐÃ CÓ sẵn → phương án A hoàn thiện trên nền này. Chốt 5 QĐ: con tự chủ hoàn toàn (BOM/báo giá/duyệt riêng) · 2 tầng · tạo con 2 đường (nút chi tiết cha prefill KH khóa + picker) cùng khách hàng · cấp duyệt báo giá GIỮ NGUYÊN theo từng báo giá · chặn đóng cha khi con chưa Đóng(11)/Kết thúc(12) · DS phẳng + cột/filter "Dự án cha" + tab "Dự án con" roll-up giá bán đã duyệt (không lộ giá vốn). Việc phải làm: migration index + validation parent_id (6 rule) + chặn close() + API `{id}/children` + `getAll?parent_candidates=1` + resource/filter + FE (RelatedSection dọn, tab con, nút tạo con prefill, cột/filter cha). Không permission mới, không sửa QuotationService.
  Spec: docs/superpowers/specs/2026-07-20-du-an-cha-con-design.md
  Bước tiếp: user review spec → writing-plans lên plan chi tiết hoặc code Phase 1 BE. Xác nhận branch (dự kiến tpe-develop-assign) trước khi code.

- demo-man-hinh-ke-toan → @dnsnamdang → .plans/demo-man-hinh-ke-toan/plan.md
  Trạng thái: **DEMO DONE Phase 1–24 (2026-07-26), chờ user review + gửi khách/deploy VPS**. Bộ demo HTML tĩnh phân hệ Kế toán tại `.plans/demo-man-hinh-ke-toan/demo/` (mở index.html, offline, style V2 hrm-client) — 14 nhóm màn: Khế ước đi vay/cho vay (6 màn) · Sổ NKC S03a (81 dòng bút toán T1–T3/2026, 3 pháp nhân, sắp xếp chuẩn kế toán; tổng PS 2.620.224.000 sau khi thêm chứng từ chi phí gắn mã phí) · NK thu/chi S03a1-a2 (2 cột Mã/Tên đối tượng trước Diễn giải) · Sổ quỹ tiền mặt S04a/S04b (tồn realtime, đối chiếu 3 số dư, cảnh báo chi TM ≥5tr NĐ 181/2025) · Sổ Cái S03b (dẫn xuất NKC, link chéo ?line=) · Bảng CĐKT B01-DN (màn hình về ĐÚNG mẫu chuẩn TT99 5 cột; số hợp nhất đã loại trừ GD nội bộ ngầm, select Phạm vi xem từng pháp nhân) · BC số dư tiền (TK kế toán bỏ mã NH) · **Bảng kê hóa đơn bán hàng, dịch vụ** (bang-ke-hoa-don-ban-hang.html — theo mẫu Fast rpt_sobk1t đã khảo sát Playwright: nguồn Phiếu xuất hàng + Phiếu hạch toán dịch vụ ERP, 9 cột chuẩn Tiền/Thuế/CK/Phải thu, link Số CT NKC ?line= động, ảnh tham-khao/fast-bang-ke-hdbh-*.png) · **Bảng kê chứng từ theo mã phí** (bang-ke-chung-tu-ma-phi.html — theo mẫu Fast rpt_gldtbkb: nhóm theo mã phí, mỗi nghiệp vụ 2 vế cân đối, tổng 405.224.000; danh mục COST_CODES + 9 chứng từ chi phí bổ sung vào JOURNAL_ROWS, note-box hướng dẫn dev; ảnh tham-khao/fast-bkct-maphi-*.png) · **Sổ tổng hợp chữ T của một tài khoản** (so-tong-hop-chu-t.html — theo mẫu Excel Fast: chọn 1 TK → SDĐK + bảng theo TK đối ứng PS Nợ/Có + Tổng phát sinh + SDCK, tái dùng công thức số dư Sổ Cái, khớp số 131 toàn tập đoàn 780→1.313tr) · **Cấu hình hạch toán** (posting-rule-engine-v3.html — Vue 3 vendor offline: nhóm bút toán theo loại phiếu, công thức ƒx + điều kiện, kéo thả dòng, lưu cấu hình theo phiên bản + modal lịch sử chỉnh sửa, select TK có search). Chuẩn UI thống nhất mọi màn sổ/báo cáo (helper chung app.js — createPager/setupColumnConfig/setupColumnSort/setupFilterHide): bộ lọc mặc định = trường bắt buộc + khối Công ty–PB–BP + nút Ẩn bộ lọc + hàng tìm nhanh kèm nút Tìm kiếm/Nhập lại · cấu hình cột ẩn/hiện + kéo thả (cột chuẩn mẫu sổ khóa) · icon sort mọi cột (lũy kế/tồn quỹ giữ giá trị theo trình tự thời gian) · phân trang 10/25/50/100/Tất cả · header 1 hàng (bỏ group) · bỏ thẻ stat-row (thông tin đưa vào bảng) · tách cột Mã/Tên đối tượng (danh mục OBJECT_NAMES) · bản in mẫu chuẩn TT99 giữ nguyên · cài đặt lưu localStorage theo màn · tất cả verify Playwright với bộ số liệu bất biến.
  Spec: docs/superpowers/specs/2026-07-14-demo-man-hinh-ke-toan-design.md
  ### Checkpoint — 2026-07-26 (đợt nâng cấp): + màn **Chọn phân hệ** (chon-phan-he.html — splash lõi 3 múi hover + 4 nhóm nghiệp vụ drill-down 2 cấp + popup phân hệ mặc định ⭐ + auto-fit 1 màn) · **sidebar 2 cấp** (rail icon nhóm cha + flyout submenu, hết tràn) · **sticky cột đầu** khi cuộn ngang cho 9 báo cáo (helper app.js: đo width động + MutationObserver + resize) · Sổ Cái bỏ 2 cột Trang/STT NKC + bỏ 3 dòng tổng cuối bảng · Sổ NKC đưa Mã/Tên đối tượng thành cột cố định TRƯỚC Diễn giải (dòng tổng colspan động) · Sổ quỹ VNĐ gộp Số phiếu thu/chi → **Số chứng từ** + thêm Loại phiếu/Người yêu cầu/lập/nhận-nộp · **2 báo cáo mới**: Bảng cân đối phát sinh công nợ trên nhiều tài khoản (debtbalance.js — 131/1368/331/3368/334 × đối tượng, thu gọn/mở) + Bảng cân đối phát sinh trên nhiều tài khoản / trial balance (trialbalance.js — tự thêm 411 cân SDĐK → tổng cân Nợ=Có cả 3 cặp, lọc bằng select TK, in S06-DN) · **topbar thêm tiêu đề màn hình** (breadcrumb nhóm + tên trang từ `<title>`) trong renderShell. Preview ảnh trong folder feature.
  Bước tiếp: user hard-refresh review tổng thể → zip demo/ gửi khách hoặc deploy VPS dev. Tuỳ chọn còn treo: tab Sổ quỹ USD (S04b) chưa gộp Số PT/PC · bản in các sổ chưa thêm cột mới · 334 công nợ chưa lấy đối tượng theo emp · đổi tên posting-rule-engine-v3.html → cau-hinh-hach-toan.html.

- prospective-projects → @dnsnamdang → .plans/prospective-projects/plan.md
  Trạng thái: **CODE DONE (2026-07-13, FE-only)**. Chờ user build FE + test. Branch `tpe-develop-assign`.
  Scope: màn `/assign/prospective-projects`. (1) Đổi label filter "Nhân viên kinh doanh"→"Nhân viên KD phụ trách". (2) Gộp 2 select nhân viên → chỉ còn 1 "Nhân viên KD phụ trách": ẩn select thừa của `V2BaseCompanyDepartmentFilter` (`:disable_employee`), select KD phụ trách lọc cascade Công ty→Phòng ban→Bộ phận (`mainSaleEmployeeOptions`), disable đến khi chọn Phòng ban, reset khi đổi cấp tổ chức. BE `main_sale_employee_id` filter đã đúng — không sửa. File: `hrm-client/pages/assign/prospective-projects/index.vue`.

- fix-ten-thong-bao-quan-ly-du-an → @dnsnamdang → .plans/fix-ten-thong-bao-quan-ly-du-an/plan.md
  Trạng thái: **CODE DONE (2026-07-13, BE)**. Chờ user build + restart queue worker + test. Branch `tpe-develop-assign`.
  Scope: fix thứ tự Họ Tên trong thông báo Modules/Assign (đang "Tên trước Họ" → "Họ Tên"). Root cause: `first_name`=Họ và đệm, `last_name`=Tên; 3 chỗ ghép ngược `last_name.' '.first_name` → sửa thành `first_name.' '.last_name`. Files: `QuotationService.php:2518`, `ProspectiveProjectService.php:1547`, `BomPriceApprovalConfigController.php:53` (log). Audit toàn module: 16 chỗ notification còn lại đều đúng (dùng `fullname`). KHÔNG đụng field `fullname` global.

- quotation-print-config → @dnsnamdang → .plans/quotation-print-config/plan.md
  Trạng thái: **CODE DONE (2026-07-13, FE-only)**. Chờ user build FE + test. Branch `tpe-develop-assign`.
  Scope: popup "Cấu hình in báo giá" → chọn cột hiển thị: bỏ tích mặc định cột "Mã hàng hoá" (`code`). Thêm `defaultUncheckedColumns:['code']` + method `selectDefault()`; mặc định (mounted/mở modal/đổi discountMethod) dùng selectDefault, nút "Chọn tất cả" giữ selectAll. File: `hrm-client/components/assign/quotation/QuotationPrintConfigModal.vue`.

- quotation-unit-select → @dnsnamdang → .plans/quotation-unit-select/plan.md
  Trạng thái: **CODE DONE + E2E 5/5 PASS + USER TEST OK (2026-07-12)**. Chưa commit git. Branch `tpe-develop-assign`.
  Gồm: feature ĐVT (Task 1-5) + fix chiết khấu khi đổi ĐVT + testcase 30 TC + UI popup "Thêm hàng hoá" (bỏ tab title 1-tab, header nowrap scroll ngang, input+nút inline 100% qua prop opt-in inlineSearchButtons ở V2BaseFilterPanel). Harness HRM/e2e/ (đồng nhất nhatlinh + e2e_provision.php seed 2 user permission). Đã revert 1 fix robustness sai (gây 404 màn tạo) về gốc.
  Bước tiếp: commit git khi user yêu cầu (không cần migration/permission). Chi tiết files + checkpoint xem plan.md.
  Scope: chọn ĐVT dòng hàng ERP ở màn Tạo/Sửa báo giá (CHỈ type=2, hàng ERP đơn, loại combo); đổi ĐVT → lấy lại giá bán+vốn theo đơn vị. BE nguồn chân lý (saveDirectProduct re-derive theo unit_id, create+update). Endpoint erp-product-units gate giá vốn tại API + helper getUnitOptions/getUnitPrice. FE isUnitSelectable/loadUnitOptions/onChangeUnit + cột ĐVT select. Detail giữ text. Không migration/permission.
  Files: hrm-api (TpProductUnitPrice, QuotationController, Routes/api, QuotationService) + hrm-client (quotations/_id/edit.vue). Spec: docs/superpowers/specs/2026-07-12-quotation-unit-select-design.md.
  Bước tiếp: user build FE + E2E (mục "Verify tổng thể" plan.md); commit khi yêu cầu.

- Bomlist-Quotation → @dnsnamdang → .plans/Bomlist-Quotation/plan.md
  Trạng thái: **Phase 32 CODE DONE (2026-07-14)** + 2 việc 2026-07-12 CODE DONE — tất cả chờ user build FE + E2E, chưa commit. Branch `tpe-develop-assign`.
  **Phase 32 — Chọn/đổi ĐVT màn Tạo/Sửa BOM** (spec: docs/superpowers/specs/2026-07-14-bom-unit-select-design.md): dòng cha ERP đơn chọn ĐVT (BOM không quản lý giá → chỉ đổi unit_id+nhãn); detail BOM nhúng unit_options (không giá); BE syncErpFields giữ unit hợp lệ (validate, rác→base); create()/createFromBom() lấy giá theo ĐVT của BOM (pickUnitPrices); báo giá type=1 khoá ĐVT + fix I-1 upsertBomProducts giữ ĐVT snapshot cho dòng ERP đã tồn tại (BOM đổi ĐVT không kéo báo giá cũ); M-1 option fallback khi unit bị xoá bên ERP; M-2 nạp options sau xoá hết con recipe. Subagent-driven 5 task + final review, tất cả Approved. php -l sạch. Không migration/permission.
  Files P32: hrm-api DetailBomListResource + BomListService (syncErpFields) + QuotationService (pickUnitPrices/create/createFromBom/upsertBomProducts); hrm-client BomBuilderEditor.vue + BomBuilderTableCard.vue.
  E2E P32 (Task 32.6 plan.md): select đúng phạm vi (ERP đơn; tạm/con/combo/view-only = text), lưu giữ unit không bị ép base, tạo báo giá giá theo unit + regression base unit, báo giá cũ giữ snapshot khi BOM đổi ĐVT, combo recipe con giữ unit hợp lệ.
  Việc 2026-07-12 (chờ test): (1) màn `/assign/product-project` hiện cả hàng ERP + hàng tạm (chỉ hàng cha; cột "Mã đồng bộ ERP"; trạng thái Đã/Đang/Chưa); (2) bugfix FK created_by popup "Thêm nhanh Model/Thương hiệu/Xuất xứ/ĐVT" (map ERP employee id).
  Điều tra tồn: mã sync ERP dài do model.name là chuỗi số quá dài (data) — chờ user chọn hướng (A validate tên Model [khuyến nghị]/B dọn data/C sửa generateCode). Audit quyền giá vốn màn duyệt tạm gác (BE gate ổn). Chi tiết + checkpoint xem plan.md.

- accounting-posting-config → @dnsnamdang → .plans/accounting-posting-config/plan.md
  Trạng thái: **UI CODE DONE (6/6 task, FE mock data)** trên nhánh `tpe-develop-accounting` (hrm-client). 8 commit `4f63af86..cd7fb13a`, CHƯA push. Qua subagent-driven (impl+review mỗi task) + final review opus (0 Critical, 2 Important đã fix).
  Scope: UI/UX màn "Cấu hình hạch toán cho các phiếu". Master-detail: danh sách loại phiếu (ERP/HRM) + bảng bút toán (Diễn giải/TK Nợ/TK Có/Nguồn/Điều kiện/Hệ số) + kéo-thả + validation inline + Lưu/Huỷ + cảnh báo chưa lưu + modal "Xem thử bút toán". Toàn bộ mock data.
  Spec: docs/superpowers/specs/2026-07-07-accounting-posting-config-design.md · Plan: docs/superpowers/plans/2026-07-07-accounting-posting-config-ui.md
  Bước tiếp theo: user `npm run dev` test trực quan `/accounting/posting-config` → quyết định push/merge. Ngoài scope (spec sau): DB/API/đồng bộ TK+loại phiếu từ ERP/engine sinh bút toán thật.
  ⏸️ 2026-07-08: TẠM DỪNG theo yêu cầu user để check ý tưởng (code local chưa push, không tiến trình nền).

- quotation-currency-editable → @dnsnamdang → .plans/quotation-currency-editable/plan.md
  Trạng thái: CODE DONE (2026-07-02, FE-only). Chờ user build FE + E2E. Branch `tpe-develop-assign`.
  Scope: Màn tạo/sửa báo giá. Field "Loại tiền tệ" tự kế thừa dự án TKT (đã có qua selectProject) + cho chọn lại — CHỈ khi lập MỚI (`:disabled="!isCreateMode"`), form Sửa khoá (theo note user). Wire `@change="handleChangeCurrency"` (đã có confirm giá không đổi) + sync làm tròn theo tiền tệ mới (VNĐ→Số nguyên). Lưu: `currency_id` trong `form`→payload (BE store/update đã lưu). FE `quotations/_id/edit.vue`. Không BE/migration.

- quotation-currency-format → @dnsnamdang → .plans/quotation-currency-format/plan.md
  Trạng thái: CODE DONE (2026-07-02). Chờ user build FE + E2E. Branch `tpe-develop-assign`.
  Scope: Chuẩn hoá định dạng số tiền luồng báo giá/BOM/dự án (Assign, KHÔNG gồm báo cáo): hàng nghìn=",", thập phân="." (vi-VN→en-US). Hiển thị: 9 file đổi `NumberFormat/toLocaleString('vi-VN')`→`'en-US'` (giữ `toLocaleDateString`). Ô nhập: `V2BaseCurrencyInput` (Assign-only) format thousands `,`/decimal `.` + parse. BE: `QuotationService::fmtNum` (log đổi giá) `.`→`,`. product-project (raw) + Excel blade (summary đã `,` nghìn) không đổi. Giữ nguyên công thức. Không migration/permission.

- quotation-rounding-vnd → @dnsnamdang → .plans/quotation-rounding-vnd/plan.md
  Trạng thái: CODE DONE (2026-07-03, FE-only, Phase 1–4). Chờ user build FE + E2E. Branch `tpe-develop-assign`.
  P4 (tinh chỉnh non-VNĐ): (1) đổi giữa 2 ngoại tệ CÓ phần lẻ (USD↔EUR) giữ nguyên lựa chọn làm tròn; (2) tiền KHÔNG phần lẻ (JPY/KRW — `zeroDecimalCurrencyCodes`) mặc định "Số nguyên (0)" nhưng vẫn cho đổi (chỉ VNĐ khoá). Thêm computed `isZeroDecimalCurrency` + `currencyDefaultRounding`; sửa init/reset/handleChangeCurrency.
  P3 (BUGFIX nhận diện VNĐ): mã VNĐ trong ERP `currencies` là **'VNĐ'** (ký tự đ), rate=1 — KHÔNG phải 'VND'. Detection `currencyCode === 'VND'` luôn false → chọn VNĐ nhưng select làm tròn không ép "Số nguyên (0)". Fix: `isVndCurrency` chuẩn hoá `toUpperCase().replace(/Đ/g,'D')` (edit.vue + index.vue view) + watcher/tỷ giá dùng isVndCurrency. Print đã tự xử lý 'VNĐ'.
  Scope P1: Màn tạo/sửa báo giá (độc lập type=2 + từ BOM type=1). Trường "Làm tròn" tự động theo tiền tệ: VNĐ → ép "Số nguyên (0)" + disable + tooltip; khác VNĐ → "tối đa 2 số lẻ" (null), chọn tự do. Tái dùng `roundingPrecision` cho thành tiền/thuế/tổng (formatMoney). FE `quotations/_id/edit.vue`: `isVndCurrency`, watcher `currencyCode`, init roundingMode (loadDetail+selectProject+initCreateMode), disable+tooltip.
  Scope P2 (fix ô nhập chưa làm tròn): thêm prop `precision` cho `V2BaseCurrencyInput` (Assign-only) — làm tròn theo precision, precision=0 chặn nhập thập phân + reformat khi đổi tiền tệ. Wire `:precision="roundingPrecision"` vào 16 ô TIỀN (₫: giá nhập/bán parent/child/svc, CK₫, CK phân bổ, CPVC, VAT₫); KHÔNG áp ô % (VAT%/CK%). VNĐ→ô tiền chỉ nhập số nguyên; USD→2 số lẻ.
  Không migration/BE/permission (BE đã lưu rounding_mode, 0 hợp lệ).

- rename-loai-chiet-khau-giam-gia → @dnsnamdang → .plans/rename-loai-chiet-khau-giam-gia/plan.md
  Trạng thái: CODE DONE (2026-07-01, Phase 1 + 2 + 3). Chờ user build FE + **reseed permission** + E2E. Branch `tpe-develop-assign`.
  Scope: Đổi "Chiết khấu/CK" → "Giảm giá/GG" toàn hệ thống. P1: danh mục "Loại giảm giá" (menu/tiêu đề/nhãn/toast) + tiền tố mã `CK-`→`GG-`. P2: đổi tên QUYỀN `...loại chiết khấu` → `...loại giảm giá` (seeder id=1090 giữ nguyên → phân quyền cũ không mất) + 7 middleware + menu isShow. P3: đổi nhãn Chiết khấu→Giảm giá trên toàn màn Báo giá (edit/view/print/submit/history + Excel blade + BE controller/service/history) — CHỈ text hiển thị, giữ biến/khóa/công thức/alias import cũ. GIỮ nguyên: route `/assign/discount-types`, bảng `discount_types`, API, mã bản ghi cũ.
  File: BE `DiscountType`, `PermissionsTableSeeder`(id1090), `Assign/Routes/api.php`, `QuotationController`, `QuotationService`, `QuotationHistory`, `DiscountTypeRequest/Controller`, `exports/bom_list.blade.php`; FE `menu-sidebar.js`, `discount-types/index.vue`, `discount-type-modal.vue`, `quotations/_id/edit.vue`+`index.vue`, `QuotationPrintPreview/PrintConfigModal/SubmitModal/HistoryModal.vue`. Không migration.
  ⚠️ DEPLOY: phải reseed PermissionsTableSeeder cùng lúc deploy code (middleware check tên MỚI; DB chưa reseed → 403). Import Excel báo giá cũ (header "CK(%)") vẫn chạy nhờ alias.

- playwright-e2e → @dnsnamdang → .plans/playwright-e2e/plan.md
  Trạng thái: CHUẨN TEAM DONE + PILOT nhatlinh CHẠY ĐƯỢC (2026-07-01). HRM/e2e/ chưa dựng (pivot sang chuẩn team + nhatlinh).
  Spec: docs/superpowers/specs/2026-06-26-playwright-e2e-design.md | Plan: docs/superpowers/plans/2026-06-26-playwright-e2e.md | Tóm tắt: .plans/playwright-e2e/design.md
  Scope gốc: Playwright E2E cho hrm-client. Đã mở rộng thành CHUẨN TEAM: e2e/ riêng Node 20 local + @playwright/test + storageState + POM (KHÔNG webServer auto).
  Đã làm: skill `playwright-setup` đặt ở hrm/nhatlinh/erp/thanh_an trong hrm-claude-config (user tự commit/push) + guide websites/playwright-e2e-setup-guide.md. Pilot nhatlinh/e2e migrate script cũ → @playwright/test+POM; chạy thật 6 pass/5 fail (5 fail do data tồn kho E2E_PROD=0 + selector kho — KHÔNG do setup, WIP user).
  Bước tiếp: (khi cần) scaffold HRM/e2e/ bằng skill playwright-setup, pilot module Human. Git skill: user tự đẩy.

- quotation-shipping-cost → @dnsnamdang → .plans/quotation-shipping-cost/plan.md
  Trạng thái: CODE DONE Phase 1–17 (BE + FE edit/view/print + Excel + product-project). php -l sạch. Chờ user migrate + E2E. Branch `tpe-develop-assign`.
  Spec: docs/superpowers/specs/2026-06-06-quotation-shipping-cost-design.md
  Scope: Redesign "Tổng hợp giá trị báo giá" (bảng nhóm chi phí 6/7 cột động) + Chi phí vận chuyển cấp phiếu (5 cột DB: shipping_cost/vat_percent/discount/allocated_discount/import_price). Mô hình cuối: VC tính vào TSLN + dòng Tổng bảng Tổng hợp + Footer, KHÔNG vào bảng HH/DV phía trên. Kèm nhiều fix phụ (popup gửi duyệt, currency tab Hồ sơ, toolbar gọn, middleware duyệt, product-project gộp báo giá tự lập, validate CK ≤ đơn giá bán...).
  Checkpoint: 2026-06-08 — Phase 8–17 done (xem plan.md). Migration mới: `2026_06_07_000001_add_shipping_import_price_to_quotations_table` (backfill = sau CK cũ). Bước tiếp: ⏳ user `php artisan migrate` + hard-refresh + E2E toàn bộ (các mục Verify `[ ]`).

- erp-cost-catalog → @dnsnamdang → .plans/erp-cost-catalog/plan.md
  Trạng thái: CODE DONE (BE B1-B5 + FE F1-F11 + P3 tách bảng service riêng cho BOM). Chờ E2E browser test.
  Scope: Dòng dịch vụ/chi phí trong BOM + Quotation chọn từ danh mục `costs` ERP (mysql2; chỉ status=1 & kind_of=2, phân loại bằng revenue_calculation 1=Dịch vụ có tính DT / 0=Chi phí khác, type=null) + tạo nhanh ghi thẳng `costs`. Popup hợp nhất "Thêm mới" 2 tab (Hàng hoá ERP / Dịch vụ & Chi phí — CostCatalogPanel). Quick-create overlay z-index 5300. P3: BOM tách "Dịch vụ & Chi phí khác" thành bảng riêng `bom_list_service_items` (đồng nhất quotation_service_items), copy sang báo giá khi tạo. Ghi mysql2 trực tiếp (created_by qua TpEmployee). Branch `tpe-develop-assign`.
  Checkpoint: 2026-06-05 — Phase P12→P19 DONE (sau P11): P12 createFromRequest copy service items BOM→báo giá; P13-P14 chốt tỷ lệ giá vốn (tự lập khoá giá vốn tính từ rate ERP; từ BOM nhập cả giá vốn+giá bán, PM tính tỷ lệ + ghi rate_value_capital về ERP khi lưu — syncServiceCostRatesToErp); P15 hiển thị tỷ giá + ngày tạo (edit toolbar + view); P16 fix validate giá dịch vụ false-positive (bỏ check unit_id + giá vốn>0, giữ giá bán>0); P17-P18 validate con không trùng mã CHA trực tiếp (so theo erp_product_id, không chặn hàng tạm theo code) + dedupe mã hàng tạm khi gộp BOM; P19 khoá sửa mã hàng tạm màn edit. Compile sạch + php -l OK. Bước tiếp: user E2E test P12→P19 + (tồn) chốt BOM aggregate có cho thêm dịch vụ thủ công không.
- elearning-exam-mode → @junfoke → .plans/elearning-exam-mode/plan.md
  Trạng thái: CODE DONE toàn bộ (BE+FE, additive — không đụng luồng course cũ). Chờ user chạy 2 migration + build elearning + verify browser. Chi tiết phase + checkpoint xem plan.md. Spec: docs/superpowers/specs/2026-06-15-elearning-exam-mode-design.md.
  Kiến trúc: engine thi NHẬN BIẾT SUBJECT (tách khỏi course), deep-link theo subject_id (route /training/subjects/{id}/exams/{examId}/todo, tái dùng ExamToDoForm). Chỉ employee thi.
  Tổng kết phase: P1 chặn auto-done exam-mode • P2 migration exam_test_results.subject_id + subject_enrollments.exam_score/exam_result (CHƯA chạy) + getForSubjectTodo + canReplyDoExamSubject • P3 syncSubjectExamCompletion (chấm theo exam_score_rule → set done + chứng chỉ) • P4 endpoint exam-status • P5 FE (màn làm bài hrm-client + DetailEnrollCard khối exam-mode) • P7 chấm tự luận subject (ExaminerService UNION subject_exams/graders) • P8 notify elearning khi chấm xong (type ExamGraded → màn khóa học xem điểm).
  LƯU Ý: không tự chạy migration. DEFER: widget dashboard chờ chấm.
  Tóm tắt: .plans/elearning-exam-mode/design.md
  Scope: Xử lý khóa `evaluation_mode='exam'` ở elearning — học viên vẫn học bài, nhưng làm bài thi đi theo luồng đào tạo cũ (HRM, deep-link); điểm quyết định hoàn thành + chứng chỉ. Nút "Làm đề thi" thay "Tiếp tục học", gate theo `exam_participation_required` (=1 cần đạt `exam_min_required_percent` mới được thi; =0 thi ngay). Phát hiện: Training đã có luồng thi cho employee (exam_test_results/ExamTestResult) nhưng CHƯA có logic set enrollment done theo điểm; elearning chưa có route exam; `recalculateCourseProgress` đang tự done theo % bài (sai cho exam-mode). Quyết định mở: deep-link HRM, mối nối subject↔ExamTestResult.course_id, ai set done theo điểm, employee vs external learner.

- elearning-notification-center → @junfoke → .plans/elearning-notification-center/plan.md
  Trạng thái: CODE DONE + VERIFIED (2026-06-15). User xác nhận chuông hiện thông báo onboarding thật, click điều hướng góc học tập. Chờ merge. Tiếp nối onboarding-auto-enroll.
  Điều chỉnh sau verify: chuông hiện cho mọi user đã đăng nhập (learner rỗng); trigger auto-enroll chuyển sang NotificationController::index (noti hiện ngay sau đăng nhập ở mọi trang); ghi DB notification đồng bộ (không cần queue worker) gom trong OnboardingAutoEnrollService::runAndNotify().
  Spec: docs/superpowers/specs/2026-06-15-elearning-notification-center-design.md | Plan: docs/superpowers/plans/2026-06-15-elearning-notification-center.md
  Scope: Trung tâm thông báo THẬT + realtime trên header elearning (thay chuông mock). BE: NotificationController trong Modules/Elearning (index/markAsRead/markAllAsRead, lọc data.type ∈ whitelist ['OnboardingAutoEnroll'], chỉ employee, learner rỗng) + 3 route /api/v1/elearning/notifications. FE: socket.io-client@^2.3.0 connect socket server có sẵn (8891) bằng JWT employee nghe event 'notification' → fetch lại list (payload realtime thiếu UUID); store notification.js + composable useNotificationSocket.js + dropdown thật trong AppHeader.vue (badge unread + mark-read + click router.push nội bộ). KHÔNG sửa backend socket.

- onboarding-auto-enroll → @junfoke → .plans/onboarding-auto-enroll/plan.md
  Trạng thái: CODE DONE + VERIFIED (2026-06-15, subagent-driven). User xác nhận: auto-enroll chạy khi vào app, thông báo hiện, hạn "Còn 10 ngày" + độ khó đúng. Chờ merge.
  Spec: docs/superpowers/specs/2026-06-15-onboarding-auto-enroll-design.md | Plan: docs/superpowers/plans/2026-06-15-onboarding-auto-enroll.md | Tóm tắt: .plans/onboarding-auto-enroll/design.md
  Fix sau verify: trigger chuyển sang app-load (NotificationController) + bỏ guard enter_date cho days=0 + wire due_date vào hiển thị hạn (DeadlineHelper::resolve ở MyLearningService/SubjectDetailController) + fix độ khó StudyCard (level_name + icon ri-bar-chart-box-line + ẩn khi rỗng).
  Scope: Bổ sung phần THỰC THI cho Onboarding (UI cấu hình đã có ở TabLearners). Lazy auto-enroll khi NV vào "Không gian học tập" (GET elearning/my/learning-space). Chỉ user_type=employee, dùng enter_date. Gán mọi khóa onboarding_enabled=1 + status=HOAT_DONG (publish) cho NV mới (days=0 → gán cả NV cũ). Thêm cột due_date vào subject_enrollments. 1 noti gộp qua SendNotificationToEmployee khi có khóa mới.
  Checkpoint: 2026-06-15 — BE 3 file mới (migration due_date + OnboardingAutoEnrollService + Unit test) + 1 file sửa (MyLearningController hook autoEnrollOnboarding, chỉ employee, try/catch nuốt lỗi). Logic: isNewEmployee (days=0/null luôn mới, <=ngưỡng, guard '0000-00-00'/date rác) + computeDueDate. Hướng B (tự tạo enrollment, không đụng SubjectEnrollmentService). Review spec+chất lượng pass; xác nhận TpEmployee->info tồn tại nên noti an toàn. Bước tiếp: user `php artisan migrate` + verify 6 kịch bản. FE không đổi.

- course-level → @junfoke → .plans/course-level/plan.md
  Trạng thái: DESIGN DONE (2026-06-09). Đang lên plan.
  Spec: docs/superpowers/specs/2026-06-09-course-level-design.md | Tóm tắt: .plans/course-level/design.md
  Scope: Thêm trường "Độ khó" (level) cho Khóa học (Subject) — 3 mức cố định (Cơ bản/Trung cấp/Nâng cao), cột DB nullable, bắt buộc ở form. BE: migration + hằng Subject::LEVELS + validate store/update + SubjectDetailResource/SubjectBrowseResource + PublicBrowseController (filterOptions levels + filter level). FE admin (hrm-client): TabInfo dropdown + SubjectBuilderForm payload. FE elearning: filterOptions store + sidebar filter "Độ khó" + card badge + subjectDetail dùng level thật. Lộ trình ngoài scope.

- external-user-report → @junfoke → .plans/external-user-report/plan.md
  Trạng thái: CODE DONE (2026-06-06). Nối API thật. Chờ user verify browser.
  Spec: .plans/external-user-report/design.md
  Scope: Màn báo cáo học tập học viên ngoài công ty (Đào tạo → Danh mục, tạm thời). BE 2 endpoint mới trong ExternalUserController: `report` (gộp subject+learning_path qua learner_id, filter/sort/KPI, không phân trang) + `{id}/enrollments` (drill-down). FE 1 trang `pages/training/external-user-report/index.vue`: danh sách dùng V2BaseFilterPanel + V2BaseDataTable (rowClickable mở popup), popup chi tiết dùng table CUSTOM (không bắt buộc V2Base — theo yêu cầu). Sửa component chung V2BaseDataTable: thêm prop opt-in `rowClickable` (mặc định false → an toàn màn khác) + emit row-click. Thêm mục menu vào training-sidebar.vue.
  Checkpoint: 2026-06-06 — Tiến độ/trạng thái lộ trình tính theo logic chuẩn MyLearningService: % = TB progress các khoá trong lộ trình; hoàn thành khi status=DONE hoặc progress>=100 (status DB của LP không đáng tin). Fix bug LP 94% hiện 50% + LP 100% kẹt "Đã đăng ký" — sửa cả report() lẫn enrollments(). Bước tiếp: user verify browser. Defer: cột "Đạt"=hoàn thành (DB chưa có is_passed), Xuất Excel báo cáo còn demo, chưa phân trang, menu chưa gắn permission.

- goc-hoc-tap-ca-nhan → @junfoke → .plans/goc-hoc-tap-ca-nhan/plan.md
  Trạng thái: CODE DONE Phase 1-5 (2026-06-06). Chờ user verify browser (Docker 3001) + nhập cấu hình deadline ở form admin.
  Spec: docs/superpowers/specs/2026-06-05-goc-hoc-tap-ca-nhan-design.md | Plan: .plans/goc-hoc-tap-ca-nhan/plan.md (chi tiết từng phase + checkpoint ở đây)
  Scope: FE elearning. Trang /goc-hoc-tap 4 tab (Tổng quan/Tôi cần học/Tôi đang học/Chứng chỉ) + tìm kiếm global kiểu f8. API thật qua MyLearningController/Service (GET my/learning-space). Deadline = enrolled_at + complete_within_days (đã migrate). Auto-complete lộ trình khi đủ khóa con (LearningSessionService.syncLearningPathCompletion, backfill đã chạy). Tiến độ path = TB % khóa con + nhãn "Khoá x/y"; đếm theo đơn vị gốc (ẩn khóa con khỏi khóa lẻ). Verify php -l + lint + build PASS.

- elearning-home-need-to-learn → @khoipv (P1-4) / @junfoke (P5) → .plans/elearning-home-need-to-learn/plan.md
  Trạng thái: CODE DONE (Phase 5 — 2026-06-08). Lint BE PASS. Chờ user verify browser.
  Spec: .plans/elearning-home-need-to-learn/design.md
  Scope: Trang chủ elearning (3001) lấy data thật cho 4 section qua 1 endpoint `public/home-content`. P1-2: "Bạn cần học". P5: thêm 3 section "Khuyến nghị cho bạn" / "Nội dung nhiều người học" / "Nội dung mới". Khách=public, nhân viên HRM=đang dùng. Tái dùng SubjectBrowseResource + LearningPathBrowseResource.
  Checkpoint: 2026-06-08 (P9) — Trang chủ data thật 4 section + màn "Xem tất cả". P5: response `{need_to_learn, recommend, popular, newest}`. P6: "Bạn cần học"=nội dung bắt buộc khớp profile (user ngoài/guest ẩn). P7: card hiển thị trạng thái học (Học tiếp/Xem lại + badge); BE dựng progress map subject+path. P8: Khuyến nghị loại item đã hoàn thành + sửa text subtitle. P9: endpoint phân trang `home-section` (trộn khóa+lộ trình theo mode) + màn `HomeSectionView` (/noi-dung/:type) + wire 4 nút "Xem tất cả". BE refactor helper dùng chung (sectionBaseQueries/applySectionConstraints/transformSectionItems/recommendExcludeIds). Lint BE PASS. Bước tiếp: user verify browser toàn bộ.

- skills-v2-redesign → @khoipv → .plans/skills-v2-redesign/plan.md
  Trạng thái: CODE DONE (2026-06-03, 2 file FE). Chờ user verify browser (Task 3).
  Spec: docs/superpowers/specs/2026-06-03-skills-v2-redesign-design.md | Plan: docs/superpowers/plans/2026-06-03-skills-v2-redesign.md
  Scope: CHỈ FE hrm-client. Đổi giao diện màn training/skills cho giống learning-path (V2BaseFilterPanel + V2BaseDataTable + BaseConfirmModal), gộp cột, toggle khóa inline. Giữ modal thêm/sửa (restyle V2 + validate inline), giữ Excel/In/Lịch sử/Khóa. Không đổi BE/API/permission. Giữ tham số & shape response API cũ.
  Checkpoint: 2026-06-03 — Rewrite index.vue + add_skill_modal.vue xong, review prop/slot V2 đạt (không lỗi runtime). Bước tiếp: user chạy npm run dev + duyệt browser theo Task 3.
- elearning-completion-criteria → @junfoke → .plans/elearning-completion-criteria/plan.md
  Trạng thái: CODE DONE Hướng A + SCORM viewed (+min giây mở) + Hướng B (2026-06-04). Chờ user rebuild + verify browser. KHÔNG migration.
  Spec: docs/superpowers/specs/2026-06-04-elearning-completion-criteria-enforcement-design.md
  Scope: Khớp form cấu hình tiêu chí hoàn thành với enforcement thật. (A) Form tạo bài text/file thêm "Min thời gian đọc (giây)" (trường BE thực dùng), gắn nhãn "(chưa áp dụng)" cho field % + các tiêu chí scroll/dwell/seek/active-tab/allow-download chưa enforce (giữ, vẫn nhập được). (B) SCORM thêm option viewed (mở là xong, cho gói content single-page; đã bỏ browsed sau test vì browse-mode gần như không xảy ra) + sửa completionHint màn học cho viewed. 6 file, KHÔNG migration. Hướng B (implement scroll/dwell/seek-block...) để sau. Tiếp nối elearning-tracking-fix + scorm-lms-runtime.

- elearning-sequential-lock → @junfoke → .plans/elearning-sequential-lock/plan.md
  Trạng thái: CODE DONE (2026-06-03). Chờ verify browser trong Docker (Node ≥18).
  Scope: Fix khoá bài học khi vào học. (1) Khoá "Học tuần tự" (subjects.linear_required) không enforce → tạo LessonLockResolver (nguồn chân lý chung BE), transformer + service dùng chung. (2) Prerequisite ALL/ANY trên từng bài (đã có sẵn, dọn về resolver). (3) Defense-in-depth: chặn heartbeat/scorm-commit bài đang khoá (423). (4) FE: disable click bài khoá + disable nút Trước/Sau (hasPrev/hasNext) + sửa badge tiền ĐK. (5) Fix bài kế không mở khi hoàn thành (phải F5) → recomputeLocks() client mirror resolver, gọi trong handleHeartbeatResponse. Tiếp nối learning-session-api + elearning-tracking-fix.

- elearning-learning-path-seamless → @junfoke → .plans/elearning-learning-path-seamless/plan.md
  Trạng thái: CODE DONE (2026-06-03, 13/13 task / 6 phase, subagent-driven). BE 5 file + FE 8 file. Không migration. Chờ user verify browser (Docker Node ≥18) 8 kịch bản.
  Spec: docs/superpowers/specs/2026-06-03-elearning-learning-path-seamless-design.md
  Plan: docs/superpowers/plans/2026-06-03-elearning-learning-path-seamless.md
  Scope: Học liền mạch lộ trình — context ?lp trong màn học, Quay lại về lộ trình, resume xuyên khoá, lock cấp khoá (linear_required), modal 3 biến thể (khoá tiếp theo / hoàn thành lộ trình / khoá lẻ), chứng chỉ lộ trình (mirror cert khoá, không migration). Tiếp nối elearning-learning-path-detail (đã fix Phase 10: trạng thái bài + % trung bình khoá + nút Vào học/Tiếp tục học).

- elearning-course-completion → @junfoke → .plans/elearning-course-completion/plan.md
  Trạng thái: CODE DONE (13/13 task, 4 phase — 2026-06-03). Chờ verify browser trong Docker (Node ≥18).
  Spec: docs/superpowers/specs/2026-06-03-elearning-course-completion-design.md
  Plan: docs/superpowers/plans/2026-06-03-elearning-course-completion.md
  Checkpoint: 2026-06-03 — Implement xong qua subagent-driven. BE 4 file (CertificateService + CertificateController + route /subjects/{slug}/certificate + certificate_enabled vào LearningSessionResource). FE 9 file: store certificate.js, CertificateView+CertificateCanvas+route /certificate/:slug+print CSS, courseCompletionSignal trong learningSession, CourseCompleteModal tích hợp SubjectLearnView, map certificateEnabled (subjectDetail), DetailEnrollCard đổi "Chứng nhận"→"Chứng chỉ"+nút "Xem lại nội dung", ContentDetailView nối router, nút "Chứng chỉ" sidebar màn học. Phương án A (endpoint riêng), chứng chỉ render web in qua window.print. Bước tiếp: user chạy dev server Docker → verify 4 kịch bản (100%→modal; có cert→in được; không cert→khám phá/xem lại; vào thẳng /certificate chưa xong→403). Defer: nút cert ở My Learning, PDF/email BE, QR, cert cho LearningPath.
- hrm-quotation-to-erp-contract → @dnsnamdang → .plans/hrm-quotation-to-erp-contract/plan.md
  Cross-system (ERP-primary). **CODE DONE cả 3 phase (không commit), chờ test E2E.** Lập HĐ ERP thẳng từ báo giá Assign HRM (status=7 + tmp synced + VND), bỏ firm-quotation. Phần HRM (done): migration `quotations.erp_firm_contract_id` (đã chạy) + `buildContractSummary` trong `QuotationController::byProject` + banner/nút "Lập hợp đồng ERP" deep-link trong `ProspectiveProjectQuotationsTab.vue`. Spec authoritative: `ERP/.plans/hrm-quotation-to-erp-contract/design.md`.

- timesheet-detail-note → @dnsnamdang → .plans/timesheet-detail-note/plan.md
  Thêm cột "Ghi chú" vào modal Chi tiết chấm công (tab Dữ liệu chấm công), lấy từ `timesheets.note` (app mobile đã lưu, web chưa show). Chỉ modal `TimeSheetDetailModal.vue` + field `note` trong `TimekeeperListResource`. Không migration.
  Spec: docs/superpowers/specs/2026-06-15-timesheet-detail-note-design.md
  Checkpoint: 2026-06-15 — Brainstorm + spec DONE. Chờ user review spec → writing-plans.

- chan-tp-duyet-qua-han → .plans/chan-tp-duyet-qua-han/plan.md
  Testcase luồng chặn TP duyệt khi NV có hàng quá hạn (HRM gọi API ERP). testcase.xlsx 29 TC (use_erp, mapping NV, fail-open, 20 phiếu Timesheet+Assign, modal). Cặp ERP ở `ERP/.plans/chan-tp-duyet-qua-han/`. Checkpoint 2026-06-11: đã sinh xong, chờ user review.

- sync-hang-tam → @dnsnamdang → .plans/sync-hang-tam/plan.md
  Trạng thái: ĐÃ COMMIT (branch sync_quotation, 3 repo — CHƯA push/merge). ERP 04efffe32d · hrm-api b3f8ee7e4 · hrm-client b119b1d0. Đã test E2E bug duyệt hàng tạm OK trên dev_erp_2.
  Spec: docs/superpowers/specs/2026-06-06-sync-hang-tam-design.md | Plan: docs/superpowers/plans/2026-06-06-sync-hang-tam.md
  Checkpoint: 2026-06-06 — Đã thực thi toàn bộ plan 12 task/4 phase qua subagent-driven (branch sync_quotation cả 3 repo, KHÔNG commit).
    Phase 1 (ERP): migration 4 cột hrm_* trên tmp_product_requests + FormRequest + TmpProductRequestSyncService + TmpProductRequestSyncController + route v1/tmp-product-requests (sync-from-hrm, approved-status). Migration đã chạy thật. Approved.
    Phase 2 (HRM api): migration erp_tmp_product_id + tmp_sync_status/tmp_synced_at + TmpProductSyncService(push/pull) + QuotationController(sendTmpApproval/pullTmpApproval) + byProject/QuotationResource(3 field) + 2 route. Migration đã chạy thật. Approved.
    Phase 3 (HRM client): ProspectiveProjectQuotationsTab.vue — nút Gửi duyệt hàng tạm + badge trạng thái + nút Cập nhật kết quả duyệt + autoPullSyncing. Approved (bác bỏ 1 false-positive về response path: apiPostMethod trả body nên res.data.counts ĐÚNG).
    Phase 4: retrySync early-return "tạm tắt" (giữ code cũ trong comment) + ẩn nút FE retry-sync (v-if=false). QuotationErpSyncService + route giữ nguyên.
    Data contract 2 chiều HRM↔ERP đã verify khớp trên code.
  Checkpoint: 2026-06-06 (b) — DEBUG + MỞ RỘNG (đã test ERP thật trên dev_erp_2): 
    Bugfix: (1) ERP tmp_products NOT NULL brand/manufacture/origin → migration nullable + product_cate='[]'; (2) approved-status chỉ trả product_id khi status=1; (3) sendApproval guard map rỗng → gửi lỗi không kẹt syncing. Reset BG-2026-00044 đang kẹt.
    Mở rộng: 2 nút header (gửi/cập nhật cấp dự án, endpoint sendTmpApprovalForProject/pullTmpApprovalForProject + cờ tmp_can_send/tmp_can_pull) + cột "Trạng thái đồng bộ" + giữ nút per-row.
    Quyết định: 1 dự án = 1 báo giá trúng thầu (giữ rule finalize). Bước tiếp: user test E2E từ UI rồi commit (3 repo branch sync_quotation, chưa commit).
  Checkpoint: 2026-06-06 (c) — Bugfix ERP `TmpProductsController::approve`: duyệt hàng tạm khi sửa trường (hãng SX/nhóm hàng hoá/avatar/units...) trước chỉ lưu sang Product, KHÔNG lưu về tmp_products. Fix: cập nhật đầy đủ field vô hướng + re-sync quan hệ (suppliers/barcodes/videos sync; attributes/galleries/units+prices xoá→insert) mirror store(), cùng transaction. Cô lập luồng sync (tmp_products không có cột sync; approved-status chỉ đọc status+product_id; HRM map theo tmp_products.id không đổi). ĐÃ TEST E2E OK trên dev_erp_2. Bước tiếp: user commit.
  Checkpoint: 2026-06-08 — MỞ RỘNG: hàng tạm "Đang tạo" trước khi gửi duyệt. Spec docs/superpowers/specs/2026-06-08-tmp-product-draft-status-design.md · Plan docs/superpowers/plans/2026-06-08-tmp-product-draft-status.md. Chỉ đụng ERP, không migration. Đang triển khai inline 8 task. Bước tiếp: code Task 1→8 rồi user test E2E trên dev_erp_2.

- project-implementation-types → @dnsnamdang → .plans/project-implementation-types/plan.md
  Trạng thái: Phase A+B done. Phase C đã pivot sang quotation-redesign. Branch `tpe-develop-assign`.
  Checkpoint: 2026-05-27 — Phase C scope mở rộng → tách thành feature riêng quotation-redesign.

- quotation-redesign → @dnsnamdang → .plans/quotation-redesign/plan.md
  Trạng thái: Code DONE (Task 1-13) + bugfix Phase 6/7. Branch `tpe-develop-assign`.
  Spec: docs/superpowers/specs/2026-05-27-quotation-redesign-design.md
  Checkpoint: 2026-06-02 — Phase 7 (Task 15): fix flash "Không tìm thấy báo giá" khi vào màn tạo báo giá (bật loading=true bao quanh mounted edit.vue). Test PASS. Bước tiếp: nhận yêu cầu mới hoặc test các flow còn lại.

- solution-manager-assignment → @dnsnamdang → .plans/solution-manager-assignment/plan.md
  Trạng thái: Code DONE. Phân công PM/Leader + lịch sử + notification + confirm. SRS + Testcase đã tạo.
  Checkpoint: 2026-05-17 — Phase 1+2 done. BE 7 file, FE 3 file. 28 test cases. Bước tiếp: deploy.
- elearning-tracking-fix → @junfoke → .plans/elearning-tracking-fix/plan.md
  Trạng thái: CODE DONE (2026-06-02, ~12 file: 1 BE + FE). Chờ verify browser trong Docker (Node ≥18). Scope: (1) hiển thị thời gian 3:12, (2) completionHint theo config, (3) video tracking thật IFrame Player API (free), (4) tối ưu heartbeat (keepalive + dừng khi done), (5) fix status chậm (optimistic learning) + toast bắn nhầm khi quay lại bài đã xong (dùng just_completed), (6) toàn vẹn tracking: chống tua video (SEEK_THRESHOLD, cho 2x) + rời tab khi đọc tài liệu (useReadingTracker + ReadingGateOverlay "Tiếp tục học"). Tiếp nối learning-session-api + elearning-lesson-viewer. Defer: idle-trong-tab, enforce scroll/dwell, Redis/queue (chỉ khi scale nghìn).

- scorm-preview-runtime → @junfoke → .plans/scorm-preview-runtime/plan.md
  Trạng thái: CODE DONE (2026-06-01). Chờ user restart dev server + verify trên browser (upload gói SCORM → preview hết lỗi objective).
  Spec: docs/superpowers/specs/2026-06-01-scorm-preview-runtime-design.md
  Scope: CHỈ FE hrm-client. Port runtime SCORM (scorm-again + proxy same-origin) sang panel preview màn quản lý bài học (LessonForm.vue type=4) để hết lỗi "could not find objective". Rút gọn: KHÔNG tracking/resume/commit BE. Proxy bằng Nuxt serverMiddleware. Tiếp nối scorm-lms-runtime (elearning) + scorm-upload.

- scorm-lms-runtime → @junfoke → .plans/scorm-lms-runtime/plan.md
  Trạng thái: DONE — chạy đúng end-to-end trên browser (completion + resume + popup). Chờ note OPS cấu hình nginx prod + merge.
  Spec: docs/superpowers/specs/2026-05-30-scorm-lms-runtime-design.md (mục 11 = các fix khi debug) | Plan: docs/superpowers/plans/2026-05-30-scorm-lms-runtime.md
  Scope: Học bài SCORM (type=4) trên elearning. Reverse-proxy S3 same-origin (window.parent.API) + scorm-again v3 (1.2+2004) + ScormPlayer.vue + endpoint scorm-commit + 9 cột scorm_* (resume + completion theo cấu hình bài). Tiếp nối scorm-upload.
  Checkpoint: 2026-05-30 — Verify PASS với gói Run-Time SCORM 2004 (scorm.com): "Đã xong" + resume. Fix phát sinh: host tanphat.s3, :key chống kẹt bài, proxy inject window.confirm=()=>true + no-store chặn 2 native confirm, popup resume riêng. OPS: nginx /scorm-proxy + sub_filter inject + no-store (spec mục 2&11). elearning cần Node ≥18; scorm-again cài trong container.

- learning-session-api → @junfoke → .plans/learning-session-api/plan.md
  Trạng thái: Code DONE (13/13 task). Chờ chạy migration + test API thật trên browser.
  Spec: docs/superpowers/specs/2026-05-28-learning-session-api-design.md
  Scope: BE (migration enrollment_lesson_progress + entity + service + controller + routes) + FE (sửa store + viewers + bỏ nút Hoàn thành). Heartbeat 30s + auto-mark done + comment bài học.

- elearning-lesson-viewer → @junfoke → .plans/elearning-lesson-viewer/plan.md
  Trạng thái: Code DONE (14/14 task). Browser test passed. Chờ kết nối API thật (→ learning-session-api).
  Fix 2026-06-16: đổi bài học hết nháy spinner toàn màn (App.vue routeKey cố định cho route subject-learn). Chờ verify.
  Spec: docs/superpowers/specs/2026-05-28-elearning-lesson-viewer-design.md
  Scope: FE elearning — màn học đầy đủ (viewer YouTube+PDF+HTML, sidebar outline, tracking giả lập, prerequisite, focus mode, tabs, mock data). SCORM mở rộng sau.

- external-user-list → @junfoke → .plans/external-user-list/plan.md
  Trạng thái: Brainstorming DONE, spec viết xong. Chờ user review spec → lên plan → implement.
  Spec: docs/superpowers/specs/2026-05-25-external-user-list-design.md
  Scope: Migration (4 field mới elearning_learners) + BE Training (controller + route + export) + FE hrm-client (index.vue list page)

- subject-enrollment → @junfoke → .plans/subject-enrollment/plan.md
  Trạng thái: Spec done, chờ duyệt → lên plan → implement.
  Spec: docs/superpowers/specs/2026-05-21-subject-enrollment-design.md
  Scope: BE (migration + model + service + controller + route) + FE (store + composable + placeholder page + button update)

- elearning-learning-path-detail → @junfoke → .plans/elearning-learning-path-detail/plan.md
  Trạng thái: Code DONE (70 task, 11 phases). Đã migrate. Chờ verify browser (Docker, Node ≥18).
  Spec: docs/superpowers/specs/2026-05-19-elearning-learning-path-detail-design.md
  Checkpoint: 2026-06-03 (6) — Phase 11: hiển thị cấp Chương (learner PathOutline + builder TabInfo, BE trả chapters[]/loose_lessons + chapter_id), quy đổi giờ-phút toàn bộ (helper formatMinutes), badge tổng "X khoá/chương • Y bài • giờ-phút" + gộp nút "Mở tất cả", fix trạng thái bài/chương màn chi tiết môn (BE đính learn_status từ EnrollmentLessonProgress + FE deriveChapterStatus), placeholder overview "Chưa có thông tin". Bước tiếp: verify browser 4 điểm (chương→bài+thời lượng, builder hiện chương, bài xong hiện "Đã xong"/chương "Đạt", overview rỗng placeholder). Defer: status chương exam chưa tính kết quả thi.

- Bomlist-Quotation → @dnsnamdang → .plans/Bomlist-Quotation/plan.md
  Trạng thái: Phase 31 CODE DONE + SRS/TESTCASE (2026-07-03) + **4 fix bug/UI (2026-07-07) CODE DONE, chưa commit**. Branch `tpe-develop-assign`.
  ### Checkpoint — 2026-07-07 (fix bản in + tổng giá trị + UI người lập)
  Vừa hoàn thành: (1) Bản in báo giá độc lập nhân đôi hàng thành dòng con — `QuotationPrintPreview.getChildren` hardcode `bom_list_product_id` (null→0 khớp mọi cha); fix bằng `isDirectQuotation`/`productIdKey`; (2) In báo giá có group mất chi tiết — `groupedData` mirror `index.vue groupedRows` (orphan/empty-group/roman); (3) Tab dự án TKT phiếu nháp không hiện Tổng giá trị — tận gốc `createFromBom` thiếu `recomputeTotals` (đã thêm) + backfill seeder (sửa BG-27,BG-30: 0→72.6M) + FE fallback `total_after_vat||total_sale` + BE byProject eager-load qty; (4) UI Người lập·Ngày tạo trên title bar "Thông tin chung" màn xem chi tiết.
  Đang làm dở: (không)
  Bước tiếp theo: user build FE + E2E 4 mục; deploy production chạy `db:seed RecomputeQuotationTotalsSeeder --force` sau deploy code; commit git khi user yêu cầu.
  Blocked: (không)
  ### Checkpoint — 2026-07-03
  Vừa hoàn thành: Rà soát toàn bộ feature (Phase 7→31 + 7 folder quotation-* điều chỉnh) qua 7 agent song song (data model, entity/enum, API+validation, business rules BR-01→70, design phases, quotation-* adjustments, FE+testcase cũ) → viết tài liệu chuẩn dự án:
    • `srs.html` (SRS đầy đủ + sơ đồ SVG use-case + swimlane tạo/duyệt/chốt báo giá) + `srs.docx` (pandoc, 27 bảng).
    • `testcase.xlsx` (135 TC, P0 40%, section Phân quyền + 14 section La Mã: BOM CRUD/cha-con/import-export + Báo giá tạo/làm giá/VAT/CK/VC/làm tròn/cha-con P31/duyệt/chốt/in-xuất/ERP + edge/bảo mật/E2E).
  Đang làm dở: (không)
  Bước tiếp theo: user review SRS + testcase; (feature code) user migrate + build + test E2E theo test-summary-phase31.md.
  Blocked:
  ### Checkpoint — 2026-07-03 (bug fix rò rỉ giá vốn)
  Vừa hoàn thành: Fix bug NV không quyền "Xem giá vốn hàng hoá" (1092) vẫn thấy giá vốn ở cột Giá nhập form tạo báo giá độc lập. 3 layer:
    • BE `BomListController::searchErpProducts` + `getErpProductPrices` — gate `cost_price` theo quyền (trả null nếu thiếu), mirror `getErpRecipeChildren`. Rà soát toàn bộ: show báo giá độc lập (703→734) đã gate sẵn.
    • FE `quotations/_id/edit.vue::initCreateMode` — bỏ hard-code `canViewCostPrice=true`/`can_view_import_price:true`, lấy quyền thật `this.canPickErpChild`.
    • Root cause: leftover hard-code `= true` từ commit ec93512f (28/05), bị `hasUserCreatedProducts` (06/06) thay thế nhưng không xoá. Thêm quy ước fail-closed vào HRM/CLAUDE.md.
  Đang làm dở: (không). `php -l` sạch. **User đã test OK (2026-07-03).** Chưa commit git.
  Bước tiếp theo: commit git (khi user yêu cầu); đưa thay đổi CLAUDE.md qua PR hrm-claude-config.
  Blocked:
  ### Checkpoint — 2026-07-04/05 (ẩn giá vốn toàn bộ form báo giá)
  Vừa hoàn thành: Mở rộng ẩn giá vốn ERP + tổng thành tiền nhập/TSLN theo quyền 1092 ở TẤT CẢ form báo giá.
    • BE: `DetailQuotationResource` (can_view_cost_price → strict; null `summary_breakdown.nhap`); `exportExcel` strict.
    • FE: `edit.vue` (bỏ bypass hasUserCreatedProducts); `_id/index.vue` (ẩn cột breakdown "Thành tiền nhập" theo quyền); `QuotationPrintPreview` (**bản in gửi khách LUÔN ẩn** — showImportCol=false cứng).
    • Quy tắc: hàng tự tạo (non-ERP) creator luôn xem/nhập; hàng ERP + mọi tổng nhập/TSLN cần quyền 1092. Bản in HTML luôn ẩn; Excel theo quyền (nội bộ).
  Đang làm dở: (không). `php -l` sạch. Chưa commit git.
  Bước tiếp theo: user build FE + test; xác nhận Excel export là bản nội bộ hay gửi khách (quyết định có ẩn cứng như bản in không).
  Blocked:
  ---
  Spec Phase 31: .plans/Bomlist-Quotation/design-phase31.md
  Phase 31 (2026-06-08): Logic hàng hoá cha-con. Cha ERP → con auto từ recipe_products (snapshot, khoá) + toggle show_children/dòng; ERP không recipe → hàng lẻ. Cha tự tạo → chọn con ERP (cần quyền "Xem giá vốn hàng hoá")/tự tạo, giá nhập auto roll-up, giá bán nhập tay + validate cha ≥ Σ con (thành tiền, chỉ Báo giá). Con cha tạm hiện giá bán; con cha ERP giữ ẩn. Migration: thêm show_children vào bom_list_products + quotation_product_prices.
  Phase 30 (2026-05-28): BOM ẩn giá ERP, báo giá load giá ERP + quy đổi tỷ giá, validity_date, tab báo giá dự án TKT, icon cảnh báo thay đổi giá, toolbar CK+TSLN màn xem.
  Spec test: .plans/Bomlist-Quotation/test-summary-phase31.md
  Checkpoint: 2026-06-10 — Phase 31 CODE DONE + fixes test vòng 2: giữ nguyên giá ERP (revert roll-up) + validate giá vốn cha<Σcon chặn gửi duyệt; tổng "Thành tiền nhập"=Σ dòng cha (Cách A) đồng bộ mọi nơi; CK hiển thị số dương; validate bắt buộc "Điều khoản thanh toán" khi gửi duyệt; sync auto-allocation+layout edit↔view. CHƯA migrate, CHƯA test browser. Bước tiếp: user migrate + build + test.
  (2026-06-09) Phase 31 CODE DONE toàn bộ (Task 1-20 + nhiều fix sau review). BE+FE đồng bộ BOM + Báo giá. Logic cha-con: cha ERP có recipe → con auto snapshot KHOÁ hoàn toàn (không thêm/xoá/sửa, SL nhân theo SL cha) + toggle show_children; cha tạm → chọn con ERP (cần quyền "Xem giá vốn hàng hoá")/tự tạo, hiện giá bán con, validate cha≥Σcon (gửi duyệt). Validate báo giá: VAT/CK 0-100% (cả nháp+gửi), thành tiền>0/giá nhập tự nhập/dịch vụ (gửi duyệt), hàng ERP giá nhập=0 hợp lệ. Khác: bỏ spinner SL, confirm xoá (cascade con), text "Bảng giá bán lẻ" sau tỷ giá, sync auto-allocation+layout+dòng tổng CK edit↔view. Chọn Cách A (BE tin payload FE). CHƯA migrate, CHƯA test browser. Bước tiếp: user `php artisan migrate` + build FE + test theo test-summary-phase31.md.

## Tạm dừng

- training-elearning → @dnsnamdang → .plans/training-elearning/plan.md
  Trạng thái: Phase 0 done (3/3 task khảo sát BE + FE + deep dive). docs/training.md ~580 dòng / 13 sections. design.md đã enhance với gap analysis P1/P2/P3 + convention bắt buộc + risk note.
  Checkpoint: 2026-04-18 — Wrap up Phase 0. Chờ user gửi spec chung + spec từng màn + file demo HTML/Vue → tạo .plans/training-elearning-<feature>/ riêng cho mỗi màn → brainstorm + lên task BE+FE → code.

- notify-task-report → @dnsnamdang → .plans/notify-task-report/plan.md
  Trạng thái: 37/37 task done. Phase 12 + 13 vừa hoàn thành (bỏ cấu hình giờ + giảm spam + an toàn cron).
  Checkpoint: 2026-04-17 — Phase 13 done. 4 mốc gửi cố định 08:30/11:30/14:30/17:30, withoutOverlapping, fix N+1, deploy code trước rồi migrate sau. Chờ user deploy + test.

## Hoàn thành

- employee-info-concurrent-allowance → @khoipv → .plans/employee-info-concurrent-allowance/design.md
  Hoàn thành: 2026-06-15. Verify browser PASS (Task 6 + Task 7 3 kịch bản nhập PC_KN). Tab "Thông tin thu nhập" màn hồ sơ NS — khi NV có ≥1 dòng phòng ban kiêm nhiệm thì popup hiện ô nhập Phụ cấp kiêm nhiệm (PC_KN, nhập tay), lưu thật vào employee_salary_history_allowances, cột PC_KN hiện trên bảng. BE 3 file (Request validate mảng + Service syncAllowances forceDelete resolve theo allowance_id/allowance_code + Controller store trong transaction) + FE 2 file (add-salary-history-modal prop concurrentPositions + computed hasConcurrent/nonConcurrentAllowances/pcknEntry + prepareConcurrentAllowance + dòng PC_KN editable; EmployeeInfoForm truyền prop + prepare 2 nhánh openSalaryHistory). Task 7 (BUG báo cáo lương): SalaryService::report() chuyển PC_KN từ dòng phòng chính → dòng phòng kiêm nhiệm (cd.id=MIN), bỏ pckn khỏi mainQuery. KHÔNG migration. Spec: .plans/employee-info-concurrent-allowance/design.md

- appoint-concurrent-sync-employee → @khoipv → .plans/appoint-concurrent-sync-employee/design.md
  Hoàn thành: 2026-06-15. Verify browser PASS (3 kịch bản: kiêm nhiệm thêm dòng & giữ vị trí chính / chống trùng / regression bổ nhiệm thường). Khi duyệt QĐ bổ nhiệm có tick Kiêm nhiệm (is_concurrently=1) → THÊM 1 dòng vào "Phòng ban/Chức vụ kiêm nhiệm" của hồ sơ NS (employee_concurrently_department_has_positions), GIỮ NGUYÊN vị trí chính. Phương án A: thêm cột is_concurrently vào appendix_labor_contracts (đã migrate DB dev); copy từ DecisionAppointPersonnel. Sửa AppendixLaborContractService::autogenousAppendixLaborContract (copy cờ) + updateEmployeeInfo (rẽ nhánh) + addConcurrentlyDepartmentPosition (chống trùng theo employee_info_id+department_id+working_position_id + null-guard). BE-only, không FE/permission. Spec: .plans/appoint-concurrent-sync-employee/design.md

- employee-relationship-export-columns → @khoipv → .plans/employee-relationship-export-columns/plan.md
  Hoàn thành: 2026-06-10. Verify browser PASS. FE-only. Thêm modal chọn cột khi xuất Excel màn human/employee-relationships (pattern employee_info), decouple cột export khỏi cột bảng. BE đã sẵn (visible_fields[]). 1 file mới ExportRelationshipModal.vue + sửa index.vue (nút mở modal, đăng ký, exportEx nhận selectedKeys). Cột cố định luôn xuất; không chọn cột vẫn xuất 6 cột. Spec: docs/superpowers/specs/2026-06-09-employee-relationship-export-columns-design.md | Design: .plans/employee-relationship-export-columns/design.md

- prospective-project-autofill-single-option → @manhcuong → .plans/prospective-project-autofill-single-option/plan.md
  Hoàn thành: 2026-06-04. Màn /assign/prospective-projects/add: auto-fill các dropdown phân loại kỹ thuật CHỈ khi còn đúng 1 option (thay vì luôn lấy [0]), lan truyền đến ổn định, không ghi đè lựa chọn tay. FE-only 1 file ProjectInfoSection.vue (autoFillSingleOptions + 5 watcher field + xóa autoFillFromApplication). Pass review spec + review chất lượng. Spec: docs/superpowers/specs/2026-06-04-prospective-project-autofill-single-option-design.md

- fix-employee-avatar-missing → @khoipv → .plans/fix-employee-avatar-missing/plan.md
  Hoàn thành: 2026-06-06. Bước 1 (chặn bug) + Bước 2/3 (khôi phục) XONG. Root cause: sync mặt (`ConnInfoService`/`RiceConnInfoService::deleteS3ByUrl`) xóa nhầm file avatar vì `face_image_url` = URL avatar khi tạo nhân sự có face_recognition (`EmployeeInfoService:779`). Fix: thêm guard không xóa nếu URL đang là `employee_infos.image` (2 file BE, lint PASS). Khôi phục: set image=face_image_url cho 56 nhân sự (query builder, bỏ qua sync ERP), verify 56/56 OK. CÒN LẠI: nhóm cũ path-style mất ~77% không có face_image_url → cần upload tay/ERP. LƯU Ý: fix BE mới ở local, cần deploy production.

- accept-personnel-seniority-manual → @khoipv → .plans/accept-personnel-seniority-manual/plan.md
  Hoàn thành: 2026-06-06. Verify browser PASS. CHỈ FE hrm-client. Cho nhập tay Số tháng + Số tiền lương thâm niên khi human/settings = "Không dùng định biên" (using_manpower=false) ở 3 màn quyết định. Phase 1 accept-personnel (FormComponent.vue + add.vue): số tiền text tĩnh, nhập độc lập. Phase 2 salary-change (CurrentIncomeComponent.vue khối "new" + add.vue): dùng định biên giữ auto-tính số tiền (newSeniorityPay = p1×tang_tham_nien×floor(tháng/12)), không định biên nhập tay độc lập. Phase 3 transfer-personnel (CurrentIncomeComponent.vue khối "new" + add.vue): giống accept-personnel (số tiền text tĩnh). Mirror pattern P1/P2/P3 (v-if isUsingManpower text / v-else input + required + helper-error). BE không đổi cả 3 màn (lưu thẳng, không recompute). Show/approve readonly (addDisabledToElement). T1-T15. Spec: .plans/accept-personnel-seniority-manual/design.md

- form-templates-print → @khoipv → .plans/form-templates-print/plan.md
  Hoàn thành: 2026-06-06. Verify browser PASS. CHỈ FE hrm-client. In mẫu phiếu bản TRỐNG từ màn assign/form-templates (nút ở list cạnh "Sửa" mọi trạng thái + màn chi tiết), modal preview + window.print. Component RIÊNG components/FormTemplatePrintSheet.vue (copy layout SurveyPrintSheet, KHÔNG sửa file dùng chung). Header: bỏ Giai đoạn dự án/Ứng dụng/Địa chỉ, thêm "Ngày khảo sát" trước "Người khảo sát"; Nhóm ngành+Nhóm giải pháp điền từ template, còn lại (Tên KH/Tên DA/Mã DA/Phân loại) để trống. Bảng đổi cột "Thông tin thu thập"→"Đáp án/giá trị thu thập cho tôi", cột đáp án để trống hoàn toàn. KHÔNG BE/permission/migration. File: components/FormTemplatePrintSheet.vue (mới), pages/assign/form-templates/_id/index.vue + index.vue (sửa). Quy ước: ref=printSheet, method=handlePrint. Spec: .plans/form-templates-print/design.md

- meeting-list-permission → @khoipv → .plans/meeting-list-permission/plan.md
  Hoàn thành: 2026-06-05. Verify browser PASS. Phân quyền xem danh sách màn assign/meeting theo 4 cấp (tổng cty/cty/phòng/bộ phận) như màn giải pháp — dùng checkPermissionList + OR own/participant (company_members type=1). Thêm 4 permission (id 1095-1098, group 'Quản lý meeting'). Gán company_id/department_id/part_id khi store (KHÔNG backfill, KHÔNG đụng update). FE filter động theo hasAPermission. BE 4 file + FE 1 file, không migration. T1-T5. Spec: .plans/meeting-list-permission/design.md

- meeting-bien-ban-phuong-an-xu-ly → @khoipv → .plans/meeting-bien-ban-phuong-an-xu-ly/plan.md
  Hoàn thành: 2026-06-05. Verify browser PASS. Thêm cột text "Phương án xử lý" (solution, nullable) vào biên bản cuộc họp màn assign/meeting create/edit, sau cột Nội dung. Đồng bộ 3 nơi: màn nhập (grid Nội dung 3/Phương án 2), Excel export (5→6 cột A:F), màn in (blade meeting_record fill td solution). BE: migration cột solution + fillable MeetingReport (syncReports/Resource không sửa) + rule nullable 2 request. Không bắt buộc nhập. 6 task / 6 file. Spec: .plans/meeting-bien-ban-phuong-an-xu-ly/design.md

- copy-form-template → @khoipv → .plans/copy-form-template/plan.md
  Hoàn thành: 2026-06-05. Verify browser PASS. Nút "Sao chép" ở list assign/form-templates → vào form Tạo mới đã prefill từ mẫu gốc (Hướng A). Tên + Nhóm ngành (scope_id) giữ nguyên; Nhóm giải pháp (industry_id) để trống (chọn lại); status=Nháp; Section sao chép 100% giữ position. Câu hỏi application_scope=1 (Tất cả)→CLONE, =2 (Theo nhóm giải pháp)→BỎ QUA (tra qua survey_question_id→SurveyQuestion). BE 3 file: +1 route copy-data + controller method + service prepareCopyData + CopyFormTemplatesResource. FE 2 file: +action copy (index.vue) + nhánh prefill ?copyFrom (add.vue). Dùng chung quyền "Quản lý danh mục mẫu phiếu thu thập thông tin", KHÔNG migration, KHÔNG sửa transformer dùng chung. Spec: docs/superpowers/specs/2026-06-05-copy-form-template-design.md | Design: .plans/copy-form-template/design.md

- quotation-finalize → @khoipv → .plans/quotation-finalize/plan.md
  Hoàn thành: 2026-06-04. 8 task (6 BE + 2 FE), verify browser PASS. Tab "Báo giá" màn assign/prospective-projects/{id}/manager: nút Chốt báo giá (Đã duyệt 4 → Trúng thầu 7) + Hủy chốt (7 → 4, bắt buộc lý do). Mỗi dự án 1 báo giá trúng thầu (BE chặn + báo lỗi nếu đã có). Nút chỉ hiện khi đúng trạng thái + isSaleOfProject. BE: +status 7, +2 history action, +finalize/unfinalize service, +2 route (không middleware/permission/migration — chỉ ghi history): Quotation.php, QuotationHistory.php, QuotationUnfinalizeRequest.php (mới), QuotationService.php, QuotationController.php, Routes/api.php. FE: ProspectiveProjectQuotationsTab.vue (2 icon-button + modal lý do hủy chốt validate inline). Spec: .plans/quotation-finalize/design.md
- xuat-ghep-tu-hang-giu → @nguyentrancu97 → .plans/xuat-ghep-tu-hang-giu/plan.md
  Hoàn thành: 2026-06-16. Xuất ghép từ hàng giữ (TanPhatDev). User xác nhận đã làm xong toàn bộ. (Brainstorm 2026-04-28 chốt 7 quyết định: hiển thị tồn/giữ qua API stockOfProducts, validate `qty ≤ in_stock + prepick_qty`, cascade nhập ghép giữ toàn bộ thành phẩm, customer per-parent, hạn giữ = today + Config.max_prepick_date, xuất thẳng tái dùng pattern export_prepick_qty/hold_qty/total_qty + FIFO consume.)

- termination-filter-include-resigned → @khoipv → .plans/termination-filter-include-resigned/plan.md
  Hoàn thành: 2026-06-02. Dropdown "Nhân viên" màn decision/termination-labor-contract/index hiển thị cả người đã nghỉ việc (Hướng A: endpoint riêng `GET decision/termination-labor-contract/employee-options` trả toàn bộ employee_infos bất kể status; FE bind vào data local `employeeFilterOptions` thay vì state global). BE 2 file (controller method + route) + FE 1 file (index.vue). Không đụng state global lẫn hàm dùng chung. Spec: .plans/termination-filter-include-resigned/design.md

- print-template-delete → @khoipv → .plans/print-template-delete/plan.md
  Hoàn thành: 2026-06-02. Xóa mềm mẫu in màn decision/category/print_templates (cột status, xóa = set status 0, list lọc status=1). Nút Xóa chỉ hiện khi can_delete=true; chặn xóa nếu mẫu đang dùng ở 9 bảng FK (decisions, department_establishments, department_dissolutions, trouble_shooting_reports, decision_labor_contracts, appendix_labor_contracts, training_contracts, self_notifications, suspend_labor_contracts.print_template_agreement_id) HOẶC code ∈ PrintTemplate::PROTECTED_CODES (BIEN_BAN_CUOC_HOP, HOP_DONG_DAO_TAO, PHU_LUC_HOP_DONG_LAO_DONG, QUYET_DINH_DIEU_CHINH_LUONG, HOP_DONG_LAO_DONG_CHINH_THUC_KHONG_THOI_HAN — mẫu hệ thống bị code hardcode tra cứu theo code). BE: migration cột status + entity PROTECTED_CODES + service getUsedTemplateIds/isPrintTemplateInUse/deletePrintTemplate (can_delete precompute theo lô tránh N+1) + controller delete($id) 4 nhánh (not_found/protected/in_use/ok) + Resource trả status+can_delete. FE: index.vue nút Xóa v-if="item.can_delete" + đọc message lỗi BE + dọn code chết, popup xác nhận tái dùng confirm-delete-selected. Branch `tpe` (đã migrate DB dev). Spec: docs/superpowers/specs/2026-06-02-print-template-delete-design.md

- employee-account-change-history → @khoipv → .plans/employee-account-change-history/plan.md
  Hoàn thành: 2026-06-02. Lịch sử thay đổi cho màn human/employee (quản lý tài khoản đăng nhập NV), mirror pattern task_history của module Assign. BE: migration bảng employee_history (employee_id, action create/update/change_status, old_value/new_value JSON, changed_by, changed_at) + entity EmployeeHistory + quan hệ Employee::history() + EmployeeService logHistory()/buildHistorySnapshot() ghi snapshot khi create/update (theo dõi email, status, rice_setting_location_id, company_ids, cờ password_changed — KHÔNG lưu giá trị mật khẩu) + endpoint GET /human/employee/{id}/histories + resource formatHistory (resolve ID→tên, enum→nhãn, format ngày). FE: nút "Lịch sử" mỗi dòng pages/human/employee/index.vue + modal timeline diff old/new. Spec: docs/superpowers/specs/2026-06-01-employee-account-change-history-design.md

- forgot-password → @manhcuong → .plans/forgot-password/plan.md
  Hoàn thành: 2026-06-01. Quên mật khẩu từ màn login. Link "Quên mật khẩu?" → màn forgot_password (email + captcha ảnh BE mews/captcha) → BE check tài khoản (TH1 tồn tại+status=1 gửi mail link reset token 30p, TH2 không/khóa báo "Không tìm thấy tài khoản") → màn reset_password (rule 7-20+4 yếu tố) → verify token (≤30p, dùng 1 lần, bảng password_resets) → đổi mật khẩu + set password_changed_at. BE: mews/captcha ^3.4, ForgotPasswordRequest/ResetPasswordRequest, AuthNewController captcha/forgotPassword/resetPassword, ResetPasswordMail + blade, 3 route public. FE: 3 store action, link login, 2 màn forgot/reset_password, whitelist authenticated.js. LƯU Ý deploy: composer install trên PHP 7.4. Spec: docs/superpowers/specs/2026-06-01-forgot-password-design.md

- force-change-password → @manhcuong → .plans/force-change-password/plan.md
  Hoàn thành: 2026-06-01. Bắt buộc đổi mật khẩu từ lần login thứ 2 nếu chưa từng đổi (chỉ tài khoản mới tạo). Chặn FE (route guard) + BE (middleware MustChangePassword). Tái dùng màn /change_password (chế độ bắt buộc + banner + nút Đóng=logout). DB: thêm login_count + password_changed_at vào employees (backfill now() cho tài khoản cũ). Rule mật khẩu mới: 7-20 ký tự, đủ 4 yếu tố, khác 123456@. Refactor updatePass sang UpdatePasswordRequest/ValidationException. Spec: docs/superpowers/specs/2026-06-01-force-change-password-design.md

- customer-scope-group → @manhcuong → .plans/customer-scope-group/plan.md
  Hoàn thành: 2026-06-01. Nhóm lĩnh vực khách hàng là CHA của Lĩnh vực (1-n), Lĩnh vực bắt buộc chọn Nhóm cha; Ứng dụng↔Lĩnh vực giữ n-n. Màn Nhóm full CRUD + import/export + 2 permission (id 1093/1094). Migration 2026_05_29_000001 (thêm customer_scopes.customer_scope_group_id, khôi phục application_customer_scopes, drop 2 pivot n-n). Downstream MeetingProject resolve qua nhóm. Spec: docs/superpowers/specs/2026-05-28-customer-scope-group-design.md

- bulk-permission → @manhcuong → .plans/bulk-permission/plan.md
  Hoàn thành: 2026-06-01. Popup "Phân quyền hàng loạt" trên /timesheet/setting/roles — cấp/thu hồi permission hàng loạt cho NV theo Khối/PB/BP/CV/CD, scope current_company, dùng V2Base. KHÔNG đụng Role. Defer lịch sử (#10455). Spec: docs/superpowers/specs/2026-05-27-bulk-permission-design.md

- request-solution-adjustment → @manhcuong → .plans/request-solution-adjustment/plan.md
  Hoàn thành: 2026-06-01. BE 8 files + FE 3 files. Fix: BaseConfirmModal @event, cột Hành động luôn hiện, cột Version, popup chi tiết dạng bảng, notification URL /manager, FileAttachmentTable readonly (disabled prop), sort id desc. Phase 8: review logic cascade khi Tiếp nhận YCĐC — gửi YCĐC không đổi trạng thái dự án TKT, tiếp nhận cascade dừng YCXD giá + Báo giá chưa duyệt. Spec: docs/superpowers/specs/2026-05-06-request-solution-adjustment-design.md | SRS: docs/srs/solution-adjustment-request-SRS.html | Testcases: docs/srs/solution-adjustment-request-testcases.xlsx

- my-todo → @dnsnamdang → .plans/my-todo/plan.md
  Hoàn thành: 2026-05-16. Phase 1-5 + 7-9 done. Nhắc việc cá nhân + lịch làm việc (cascade toggle, sub-items, confirm modal).
- fix-handover → @dnsnamdang → .plans/fix-handover/plan.md
  Hoàn thành: 2026-05-16. V6 done. Bàn giao công việc — tiếp nhận tất cả + filter cascade + submitted_at.
- close-prospective-projects → @dnsnamdang → .plans/close-prospective-projects/plan.md
  Hoàn thành: 2026-05-16. Phase 17C done. Chốt dự án tiềm năng — hồ sơ trình duyệt + đổi trạng thái YC làm GP.

- google-login → @junfoke → .plans/google-login/plan.md
  Hoàn thành: 2026-05-26. Đăng nhập Google bằng GIS (Google Identity Services). Migration (password nullable + google_id + avatar_url) + BE endpoint auth/google (verify token, tìm/tạo learner, auth_source='google') + FE composable useGoogleAuth + nút Google trên LoginView + RegisterView + avatar fallback. Spec: docs/superpowers/specs/2026-05-26-google-login-design.md

- project-implementation-types → @manhcuong → .plans/project-implementation-types/plan.md
  Hoàn thành: 2026-05-24. Bổ sung 3 phương án triển khai dự án TKT (1=Tự triển khai, 2=Theo phòng, 3=Liên phòng ban). Type=1: KD tự làm GP không qua YC, Solution skip duyệt PM/Leader, Hồ sơ TĐ auto-approve. Type=2: lock receive_dept = phòng KD phụ trách. Type=3 giữ nguyên (backward-compat). 2 migration + ~15 file BE/FE. Spec: docs/superpowers/specs/2026-05-23-project-implementation-types-design.md

- solution-module-show-closed → @manhcuong → .plans/solution-module-show-closed/plan.md
  Trạng thái: Brainstorming DONE (2026-05-22). Design + plan + spec đã viết. Đang implement BE.
  Spec: docs/superpowers/specs/2026-05-22-solution-module-show-closed-design.md
  Checkpoint: 2026-05-22 — Sửa SolutionModuleService::index() để hạng mục thuộc Solution status=Đóng vẫn hiện ra. Bước tiếp: edit dòng 121-123, user test.

- add-member-no-modules → @manhcuong → .plans/add-member-no-modules/plan.md
  Trạng thái: Code DONE (2026-05-22). Phase 1 BE + Phase 2 FE xong, đã spec-review PASS. Chờ user test 9 case.
  Spec: docs/superpowers/specs/2026-05-22-add-member-no-modules-design.md
  Checkpoint: 2026-05-22 — BE: AddMemberRequest (nullable), SolutionService::addMember (DB::transaction + rẽ nhánh has_modules, insert solution_module_members hoặc solution_members, check trùng, throw ValidationException), SolutionController::addMember (catch ValidationException → responseUnprocessableEntity). FE: HumanResourceTab.vue title động, v-if has_modules cho field Hạng mục, availableMembersOptions 2 nhánh, openAddMemberModal/submitAddMember conditional. Bước tiếp: user test 9 case ở spec section 6.

- improve-testcase-baocao → @manhcuong → .plans/improve-testcase-baocao/plan.md
  Trạng thái: Phase 1-3 DONE (2026-05-22). File Testcase_baocao.xlsx đã sửa. Backup giữ .bak. Chờ user review file.
  Checkpoint: 2026-05-22 — 10 sheet báo cáo đều có khối "MÔ TẢ BÁO CÁO" 9 dòng đầu + cột mới "Giải thích nghiệp vụ" + cột "KQ thực tế" đã dịch jargon. Script ở `tools/improve_testcase_baocao.py`. Bước tiếp: user xem file rồi quyết định cleanup (.bak + sheet-data.md).

- personnel-report-contract-status → @manhcuong → .plans/personnel-report-contract-status/plan.md
  Trạng thái: Brainstorming DONE (2026-05-21). Design + plan đã viết. Chờ code.
  Checkpoint: 2026-05-21 — Bổ sung logic trạng thái HĐLĐ theo ngày còn lại (effective/expiring_soon/expired/none) + cập nhật FE text/badge + cột HĐLĐ trong Excel export. Bước tiếp: code BE accessor.

- solution-employee-cross-department → @manhcuong → .plans/solution-employee-cross-department/plan.md
  Trạng thái: Brainstorming DONE (2026-05-20). Spec + design + plan đã viết. Chờ verify payload BE rồi bắt đầu code.
  Spec: docs/superpowers/specs/2026-05-20-solution-employee-cross-department-design.md
  Checkpoint: 2026-05-20 — Mở rộng PM/Leader/Member dropdown ra toàn công ty (cùng `current_company`, `status=1`), đồng bộ cho cả modal "Tiếp nhận yêu cầu giải pháp". BE mở rộng `checkPermissionList` để leader/member phòng khác xem được Solution.

- elearning-auth → @manhcuong → .plans/elearning-auth/plan.md
  Trạng thái: Code DONE v2 (2026-05-20). Phase 0→7 hoàn thành. Chờ: chạy migration + test thủ công 15 TC.
  Spec: docs/superpowers/specs/2026-05-20-elearning-auth-design.md
  Spec cũ (deprecated): docs/superpowers/specs/2026-05-12-elearning-auth-design.md
  Checkpoint: 2026-05-20 — BE 18 files (2 migration, 2 entity, 1 middleware, 6 request, 1 service, 1 controller, 2 resource, 1 mail, 1 blade, module scaffold, config auth, Kernel, modules_statuses) + FE elearning 8 files (api util, store, router, 5 view) + FE hrm-client 1 file (pages/sso/elearning.vue) + env. Bước tiếp: chạy `php artisan migrate` + test 15 TC.

- course-rebuild-subject → @manhcuong/@junfoke → .plans/course-rebuild-subject/plan.md
  Trạng thái: Code DONE P1-P9 (2026-04-22). Phase 13+14 bug fix 2026-04-28.
  Checkpoint: 2026-04-28 — P14 (đang tiếp): fix mã auto-gen BE, override_completion reset, modal info bài học + trạng thái ghi đè, format tiêu chí hoàn thành (giây+%), labels tiếng Việt mapping/prerequisite, DRAFT canDelete, assignee pill auto-open, confirm lock modal. Phase 10 manual test còn 10 test case.

- my-job-assign-business-tab → @manhcuong → .plans/my-job-assign-business-tab/plan.md
  Spec: docs/superpowers/specs/2026-04-20-my-job-assign-business-tab-design.md
  Hoàn thành: 2026-04-21. Phase 1–2 (BE) + Phase 4–8 (FE). BE: routes + service + Resource + Export + Helper. FE: index.vue wiring + AssignBusinessTab.vue đầy đủ (filter 8 ô, bảng 8 cột, 13 row actions dropdown, column customization, ExportModal, ConfirmDelete, ConfirmCancelApprove). Test OK.

- customer-development-report → @manhcuong → .plans/customer-development-report/plan.md
  Hoàn thành: 2026-05-19. Testcases báo cáo QLDA_BC_10 đã bổ sung trong Testcase \_baocao.xlsx. Spec: docs/superpowers/specs/2026-05-18-customer-development-report-design.md
- optimize-getall-manager-context → @manhcuong → .plans/optimize-getall-manager-context/plan.md
  Hoàn thành: 2026-05-11. Tối ưu API getAll khi tạo Task/Issue từ màn Manager: BE thêm filter id vào 2 service, FE truyền id param + lock select. 6 file (2 BE + 4 FE). Spec: docs/superpowers/specs/2026-05-11-optimize-getall-manager-context-design.md
- task-status-notification → @khoipv → .plans/task-status-notification/plan.md
  Hoàn thành: 2026-05-07. 8 case thông báo push (Redis+FCM) khi task đổi trạng thái. Code đã có sẵn trong TaskService::handleStatusNotification(). Spec: docs/superpowers/specs/2026-05-07-task-status-notification-design.md
- learning-path → @khoipv → .plans/learning-path/plan.md
  Hoàn thành: 2026-05-04. Phase 1-7 (24 task). CRUD lộ trình học (3 bảng DB, 4 tab FE: thông tin+builder khoá học, kết quả, người học, chứng chỉ). Danh sách V2Base với lock/unlock, bộ lọc nâng cao 7 ô, popup bài thi + điều kiện học. Spec: docs/superpowers/specs/2026-04-29-learning-path-design.md
- progress-percent-auto-from-log → @manhcuong → .plans/progress-percent-auto-from-log/plan.md
  Hoàn thành: 2026-05-05. Mode B ImportResultModal: Tiến độ hoàn thành tự động từ log gần nhất có giá trị (computed latestLogProgressPct). BE validate tiến độ tăng dần + bắt buộc 100% khi chuyển sang REVIEW/DONE. Spec: docs/superpowers/specs/2026-05-04-progress-percent-auto-from-log-design.md

- issue-completion-flow → @khoipv → .plans/issue-completion-flow/plan.md
  Hoàn thành: 2026-04-28. 22/22 task. Thêm 2 trạng thái completed/rejected vào flow Issue + branching logic approver (duyệt/từ chối) + notification cho approver khi resolved và assignee khi rejected. BE: 1 migration + entity + service + resource + controller. FE: index + modal. Spec: docs/superpowers/specs/2026-04-28-issue-completion-flow-design.md
- add-description-column-list → @khoipv → .plans/add-description-column-list/plan.md
  Hoàn thành: 2026-04-28. 8/8 task. Thêm cột "Mô tả" vào 7 màn danh sách module Giao việc (industry-groups, customer-scopes, solution-groups, application, project_items, project_role, meeting_type). Chỉ FE, không sửa BE/API.
- progress-version-snapshot → @manhcuong → .plans/progress-version-snapshot/plan.md
  Hoàn thành: 2026-04-29. BE snapshot progress version + filter module theo version hiện tại + FE hiển thị version hiện tại và tiến độ trên danh sách giải pháp.
  Checkpoint: 2026-04-29 — user test OK.

- subjects-list-ui → @junfoke → .plans/subjects-list-ui/plan.md
  Hoàn thành: 2026-04-25. Fix 3 bug logic (`exportExcel` formFilter→filters, `lockItem`/`unlockItem` getData→loadData, `getTrainingTypes` method xung đột computed) + 1 bug CSS (`::v-deep` row-actions hover) + thêm nút lock/unlock toggle trong cột Trạng thái + status pill dùng global `tpl-status-*` class từ `v2-styles.scss`. Xóa dead code `onEditClick`/`eventHandler`. Chỉ 1 file: `hrm-client/pages/training/subjects/index.vue`.
- merge-module-review-profiles → @manhcuong → .plans/merge-module-review-profiles/plan.md
  Hoàn thành: 2026-04-25. 7/7 task. Gộp hồ sơ trình duyệt hạng mục vào tab Hồ sơ giải pháp. BE: mở rộng `getSolutionReviewProfiles()` merge 2 query (solution + module) + manual paginate + transform + auto-force type theo filter. FE: 3 filter mới (Loại/Hạng mục/Version HM) + 2 cột mới + deep watcher auto-search + row actions phân loại + tích hợp `ModuleApprovalModal` để PM duyệt hồ sơ hạng mục. Lọc bỏ draft. Spec: docs/superpowers/specs/2026-04-25-merge-module-review-profiles-design.md
- scorm-upload → @khoipv → .plans/scorm-upload/plan.md
  Hoàn thành: 2026-04-22. 14/14 task. Spec: docs/superpowers/specs/2026-04-22-scorm-upload-design.md. BE: `CmcS3Helper::putLocalFile` + `UploadScormRequest` + `LessonService::handleScormUpload` (ZipArchive extract → parseScormManifest → upload S3 recursive với MIME chuẩn → cleanup tmp) + Controller `uploadScorm` + route `POST /training/lessons/upload-scorm`. FE: `LessonForm.vue` block SCORM thêm `V2BaseFile(.zip)` + spinner + info card + `onUploadScormZip` / `clearScormPackage`; submit type=4 gửi thêm `package_path / package_title / file_size / file_name`. Giới hạn 1GB, 2000 files. Known issue pending: cross-origin SCORM API (S3 ≠ LMS domain) — để lại cho feature sau `scorm-lms-runtime`.
  Phase 4 fix (2026-06-02, @junfoke): (4.1-4.3) parser manifest robust — dò identifierref đệ quy qua item lồng nhau + xml:base + fallback quét đệ quy → hết 422 với gói SCORM.com "Randomized Testing"; (4.4) launch URL đổi path-style → virtual-hosted (tanphat.s3.cloud.cmctelecom.vn/<key>) → hết 403 AccessDenied khi preview qua /scorm-proxy; (4.5) bỏ default scorm_min_score=60 → null (gói nội dung không chấm điểm vẫn hoàn thành) + hint UI; (4.6) prune tracking_completion khi submit chỉ giữ key đúng loại bài. Lesson tạo trước fix cần gỡ gói + tải lại rồi lưu lại.
- ke-toan-module-scaffold → @manhcuong → .plans/ke-toan-module-scaffold/plan.md
  Hoàn thành: 2026-04-22. Scaffold phân hệ Kế toán (module mới). BE `Modules/Accounting/` đầy đủ structure + `module.json` + `composer.json` + `AccountingServiceProvider` + `RouteServiceProvider` + `Routes/api.php` (`GET /dashboard`) + `DashboardController` + đăng ký `modules_statuses.json`. FE: layout riêng `layouts/accounting.vue` + sidebar `accounting-components/accounting-slidebar.vue` + topbar `AccountingMenu.vue` (dùng `<BasicSubsystem />`) + `custom-accounting.scss` + `icon_ke_toan.svg` placeholder + Vuex flag `is_use_accounting` (master-setting `use_accounting`) + checkbox "Sử dụng kế toán" tại `/timesheet/setting/setting-master` + tile `BasicSubsystem.vue`/`pages/index.vue` + `pages/accounting/index.vue`+`dashboard.vue`. Tài liệu tổng quan: `docs/accounting.md`. Spec: `docs/superpowers/specs/2026-04-21-ke-toan-module-scaffold-design.md`.
- overdue-task-unified-predicate → @manhcuong → .plans/overdue-task-unified-predicate/plan.md
  Hoàn thành: 2026-04-21. Thêm `Task::scopeOverdue` + áp ở `TaskController::index` + `SolutionService::getCategoriesWithLateTasks`/`getPeopleWithLateTasks` + `SolutionModuleService::getPeopleWithLateTasks`. Đồng bộ `late_tasks_count` + card Overview với logic `overdue_total` tab Task (status NOT IN [1,8,9], CONCAT due_date+due_time). Review pass 0 Critical/Important. Test OK.
- solution-save-and-approve → @manhcuong → .plans/solution-save-and-approve/plan.md
  Hoàn thành: 2026-04-07. 2/2 task. Button "Lưu và duyệt" khi has_modules=false
- solution-version-report → @manhcuong → .plans/solution-version-report/plan.md
  Hoàn thành: 2026-04-07. 15/15 task + 53 test cases. Báo cáo QLDA_BC_10 theo version
- question-form-industry-level → @manhcuong → .plans/question-form-industry-level/plan.md
  Hoàn thành: 2026-04-18. 8/8 Phase. Đổi cấp gán Câu hỏi & Mẫu phiếu thu thập từ Ứng dụng → Nhóm giải pháp, ràng buộc 1 nhóm giải pháp - 1 phiếu Published. 2 migration chạy sạch, BE 12 file + FE 16 file, 14 service test pass
- application-export-split-columns → @manhcuong → .plans/application-export-split-columns/plan.md
  Hoàn thành: 2026-04-17. Tách Excel xuất Ứng dụng từ 7 cột (gộp) → 12 cột riêng biệt. Chỉ sửa 1 file blade
- daily-report-testcase → @manhcuong → .plans/daily-report-testcase/plan.md
  Hoàn thành: 2026-04-15. 40 test case UI theo góc nhìn người dùng cho màn Nhập kết quả báo cáo tiến độ hàng ngày
- assignee-reject-start → @manhcuong → .plans/assignee-reject-start/plan.md
  Hoàn thành: 2026-04-10. 9/9 task + 13 manual test case. Assignee từ chối triển khai khi task chưa có kết quả (BE only, FE không đổi)
- category-multi-select → @manhcuong → .plans/category-multi-select/plan.md
  Hoàn thành: 2026-04-10. 56/56 task. Đổi 4 FK đơn trong Nhóm giải pháp & Ứng dụng sang multi-select qua 4 pivot. Bao gồm Phase 10 hot-fix downstream (7 file: Scope/CustomerScope relations, ProspectiveProject auto-fill, SurveyQuestions Resource, SolutionsWorkSummary report, optionsSelect store, FormMeta cascade)
- report-testcases → @manhcuong → .plans/report-testcases/plan.md
  Hoàn thành: 2026-04-09. 149 test cases cho 8 báo cáo module Assign
- solution-module-version-tracking → @manhcuong → .plans/solution-module-version-tracking/plan.md
  Hoàn thành: 2026-04-08. 6/6 task. Theo dõi chỉ số hoàn thành giải pháp theo version
- task-manager-by-employees → @junfoke → .plans/task-manager-by-employees/plan.md
  Hoàn thành: 2026-04-08. 9/9 task. Báo cáo phân bổ nguồn lực dạng Gantt theo NV (QLDA_BC_V2_11)
- solution-add-module-deploying → @manhcuong → .plans/solution-add-module-deploying/plan.md
  Hoàn thành: 2026-04-07. 3/3 task. PM thêm hạng mục khi đang triển khai + auto-approve
- pi-approved-price → @nguyentrancu97 → .plans/pi-approved-price/plan.md
  Hoàn thành: 2026-04-13. Cột giá đề xuất + đơn giá duyệt + chênh lệch + notification cho PI nhập khẩu / trong nước (TanPhatDev, 11 files + 1 migration)
- price-request-filter-columns → @nguyentrancu97 → .plans/price-request-filter-columns/plan.md
  Hoàn thành: 2026-04-13. 11/11 task. Thêm filter + cột thương hiệu, hãng SX vào 3 danh sách YCHG/YCTG/Phiếu TG (TanPhatDev, 9 files)
- bill-settlement-remove-checkbox → @nguyentrancu97 → .plans/bill-settlement-remove-checkbox/plan.md
  Hoàn thành: 2026-04-13. 4/4 task. Xoá UI checkbox chọn nhân viên form Quyết toán thưởng NS quý (TanPhatDev)
- bill-income-report-fix-accounting → @nguyentrancu97 → .plans/bill-income-report-fix-accounting/plan.md
  Hoàn thành: 2026-04-29. 4/4 task. Lọc + chạy lại hạch toán phiếu báo có sai. 3 method thêm vào `database/seeds/UpdateDB.php`: `findInvalidBillIncomeReports()`, `fixCustomerSupplierSwap()`, `rerunBillIncomeReportAccounting($ids)`. User chạy 4 step tinker + verify giảm error (TanPhatDev)
- bill-income-supplier-export → @nguyentrancu97 → .plans/bill-income-supplier-export/plan.md
  Hoàn thành: 2026-04-29. 13/13 task. Phiếu báo có loại NCC: thay search HĐ mua trực tiếp bằng search phiếu xuất hàng (3 type 1/2/15) → auto-fill HĐ mua. 8 BE + 1 migration + 3 FE. Test 7 case pass (TanPhatDev)
- pi-inland-supplement-annex → @nguyentrancu97 → .plans/pi-inland-supplement-annex/plan.md
  Hoàn thành: 2026-04-29. 12/12 task. Lập phụ lục bổ sung cho PI trong nước (firm type=4 + free type=5, KHÔNG migration). 2 BE + 5 FE. Test 6 case pass (TanPhatDev)
- delivery-trip-accounting-cost-validate → @nguyentrancu97 → .plans/delivery-trip-accounting-cost-validate/plan.md
  Hoàn thành: 2026-06-16 (vòng 2 — đã làm xong). Áp dụng logic validate cước cho phiếu hạch toán + enable edit header + tick is_company_sp. (Vòng 1: 2026-04-29, 10/10 task, 1 migration + controller + JS class + 3 view, test 5 case pass) (TanPhatDev)
- delivery-trip-actual-cost-validate → @nguyentrancu97 → .plans/delivery-trip-actual-cost-validate/plan.md
  Hoàn thành: 2026-06-16 (vòng 2 — đã làm xong). Validate `total_cost_transition` theo CP xăng + cầu đường + công tác phí + CP khác. (Vòng 1: 2026-04-29, 10/10 task, JS class + 2 view, test 6 case pass) (TanPhatDev)
- firm-order-contact-select → @nguyentrancu97 → .plans/firm-order-contact-select/plan.md
  Hoàn thành: 2026-06-16 (vòng 2 — đã làm xong). Select người liên hệ cho đơn hàng nguyên tắc thay vì copy từ HĐNT. (Vòng 1: 2026-04-29) (TanPhatDev)
