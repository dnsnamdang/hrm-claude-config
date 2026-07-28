# Plan: Đồng bộ popup "Thêm hàng hoá" báo giá theo popup ERP

> Spec: `docs/superpowers/specs/2026-07-03-quotation-product-popup-erp-design.md`
> Phụ trách: @manhcuong · Design đã duyệt 2026-07-03

## Phase 1 — ERP API nội bộ (repo TanPhatDev)

**BE**
- [x] Tạo `app/Http/Controllers/Api/HrmProductSearchController.php` — action `search`: validate `company_id` + `employee_id` bắt buộc, tái dùng logic `SearchController::searchProductStockBuyerApi`, trả JSON phẳng `{total, products[]}` (đủ field spec 4.1, `avatar_url` tuyệt đối theo APP_URL)
- [x] Action `catalogs`: trả product_types (qua `Product::getProductTypes()`), product_cates, brands, manufactures, origins, groups (kèm mapping classify), scopes, chapters (kèm scope_id), job_groups (kèm chapter_id), job_clusters (kèm job_group_id), vehicle_manufacts/brands/models (kèm liên kết)/lifes — bọc `Cache::remember` 10 phút
- [x] Đăng ký 2 route nội bộ không api-key trong `routes/api.php` (cạnh nhóm `v1/tmp-product-requests`): `GET /api/v1/hrm/products/search` + `GET /api/v1/hrm/products/catalogs`
- [x] Test curl trực tiếp: search theo name / brand_ids[] / product_types[] / check_in_stock / phân trang start-length; catalogs trả đủ key; thiếu company_id → lỗi 422

### Checkpoint — 2026-07-03 (tạm dừng theo yêu cầu user)
Vừa hoàn thành: Phase 1 code xong (implementer Opus, status DONE_WITH_CONCERNS), curl test pass. Code nằm ở WORKING TREE TanPhatDev branch master, CHƯA commit (quy tắc dự án).
Đang làm dở: đã tạo gói diff `scratchpad/task-phase1-diff.txt` (348 dòng), CHƯA dispatch reviewer Phase 1.
Bước tiếp theo: dispatch task reviewer Phase 1 (diff + brief scratchpad/task-phase1-brief.md + report scratchpad/task-phase1-report.md) → fix nếu có finding → Phase 2 (HRM BE).
Blocked: 3 concern của implementer cần user biết: (1) `in_stock_assembly` (SL có thể lắp ráp) bản API ERP không tính, tạm trả rỗng — cần user quyết bổ sung hay hiển thị "—"; (2) `product_attributes` giữ raw HTML, FE phải render an toàn; (3) `price`/`sale_max_percent` chỉ trả khi gửi `price_type`.
Lưu ý mới: CLAUDE.md vừa bổ sung — select trong modal PHẢI dùng `V2BaseSelectInModal` (áp dụng cho Phase 3).

## Phase 2 — HRM BE (hrm-api, Modules/Assign)

**BE**
- [x] Tạo `Modules/Assign/Services/ErpProductSearchService.php` — `search($filters, $employee)`: gọi `ErpApiService->get('/api/v1/hrm/products/search', ...)` kèm company_id/employee_id/price_type bán lẻ; enrich `cost_price` từ `TpProductUnitPrice::getCostPrices()` gate quyền `Xem giá vốn hàng hoá`; map về format FE (erp_product_id, product_type:1, list_price=price, source:'ERP', stripLeadingQuote, + field hiển thị mới spec 4.2)
- [x] `catalogs()`: proxy `/api/v1/hrm/products/catalogs`, cache Redis 10 phút
- [x] Thêm action `erpProductSearch` + `erpProductCatalogs` vào `QuotationController`, ERP lỗi → message "Không thể kết nối đến ERP..."
- [x] Đăng ký `GET /erp-product-search` + `GET /erp-product-catalogs` vào nhóm `assign/quotations` trong `Modules/Assign/Routes/api.php` — **đặt TRƯỚC route `/{id}`** (dòng ~452), không gắn checkPermission
- [x] Test tinker: đủ filter, phân trang, user không quyền giá vốn không thấy cost_price, ERP offline → message tiếng Việt (review Approved; đã fix 2 Minor: list_price ?? 0, stripLeadingQuote product_cate_name)

## Phase 3 — HRM FE modal mới (hrm-client)

**FE**
- [x] Đọc skill `modal-popup` + `button-convention` trước khi code
- [x] Tạo `pages/assign/quotations/components/QuotationProductSearchModal.vue` — props/emits y hệt `BomBuilderAddProductModal` (`apply(items, parentRowId, groupId)` / `close`), giữ select Nhóm hàng HRM đầu modal
- [x] Khối filter 19 control theo layout 4 hàng (spec 4.3): multi-select Tính chất/Loại HH/Thương hiệu/Hãng SX (dùng `:extraSettings="{ multiple: true }"` sau review); cascade Lĩnh vực→Chương→Nhóm CV→Cụm CV client-side; remote Dùng cho máy + Model; select tĩnh Tồn kho; load catalogs 1 lần khi mở — mọi select tĩnh dùng V2BaseSelectInModal
- [x] Auto-search deep watcher + debounce 300ms theo pattern TasksTab.vue (ignoredFields + oldFilters); nút "Làm mới" reset filter; multi-select rỗng không gửi param
- [x] Bảng kết quả 16 cột đúng thứ tự, scroll ngang, sticky header, click ô Mã/Tên toggle chọn, KHÔNG cột ĐVT/Số lượng, in_stock pre-line, in_stock_assembly "—", selection giữ qua trang
- [x] Phân trang server-side 20 dòng/trang (V2BasePagination, start/length)
- [x] Copy overlay "Thêm hàng tạm" + quick-add từ `BomBuilderAddProductModal` (KHÔNG sửa file gốc), source NEW
- [x] Nút "Thêm N hàng hoá": apply `qty = 1`, payload giữ format cũ → `onAddProductApply` chạy nguyên
- [x] `_id/edit.vue`: swap sang `QuotationProductSearchModal` (BOM giữ modal cũ), flow `erp-recipe-children` không đổi (review Approved; đã fix multiple→extraSettings, revert file ngoài phạm vi CreateTaskModal.vue)

## Phase 4 — Kiểm thử

- [x] Verify Playwright trên /assign/quotations/create: 12/12 PASS — 19 filter/16 cột, multi-select tag + network brand_ids[], auto-search, cascade reset, tồn kho theo công ty, phân trang giữ tick qua trang, chọn 2 hàng vào form SL=1 VAT khớp (report: scratchpad/task-phase4-report.md + 13 ảnh phase4_shots/)
- [x] "Thêm hàng tạm" tạo hàng NEW về form đúng như trước (không quick-add, không ghi DB)
- [x] ERP offline: test ở tầng service Phase 2 (URL chết → rethrow message tiếng Việt, controller trả 500 không nuốt lỗi); không tắt ERP thật vì server dùng chung — chưa test toast UI
- [x] Regression: popup BOM (BomBuilderAddProductModal) vẫn mở + search bình thường, console 0 error
- [x] Final review toàn 3 repo (Opus): READY, không Critical — contract 3 lớp khớp, HRM route có JWT (auth:api), BOM nguyên vẹn

## Việc còn lại (sau bàn giao — chờ user quyết)

- [x] (Important) FE race guard: `doSearch()` thêm `_reqSeq` latest-request-wins (init ở `created()`, guard cả catch/finally) — làm 2026-07-04, dev server build sạch, page 200
- [x] (Important) Bảo mật route ERP nội bộ — làm 2026-07-04 (user đồng ý "tiếp tục"): shared-secret env-gated. ERP `HrmProductSearchController::checkInternalKey()` check header `X-Internal-Key` bằng `hash_equals`, CHỈ enforce khi env `HRM_INTERNAL_API_KEY` set; HRM `ErpApiService::defaultHeaders()` gửi header khi env set (áp cho cả get/post — backward-compatible, route khác bỏ qua header). Env đã ghi vào `hrm-api/.env.example` (ERP không có .env.example). **DEPLOY PRODUCTION: set `HRM_INTERNAL_API_KEY` cùng giá trị ở .env của CẢ 2 repo** (LOCAL đã set sẵn 2026-07-04 — key random 64 hex trong .env cả 2 repo, KHÔNG commit .env). Verified enforce thật: không header → 401, sai key → 401, đúng key → 200; e2e HRM→ERP với key: catalogs 15 key + search total=6269
- [x] (Minor) `V2BaseSelectInModal.vue:49` — làm 2026-07-04: thêm guard `$el.data('select2') &&` cùng pattern dòng 169 (file dùng chung, user đồng ý), FE build sạch page 200
- [ ] (Minor) Giá null ERP hiển thị "0" thay "—"; xác nhận `unit_id` có trong payload apply hàng ERP; catalog filter trễ 10' sau quick-add; `in_stock_assembly` muốn số thật phải sửa hàm dùng chung ERP `searchProductStockBuyerApi`

## Phase 5 — Popup mới cho toàn phân hệ dự án (user yêu cầu 2026-07-04, spec mục 6c)

**FE**
- [x] `QuotationProductSearchModal.vue`: nhánh `bomListId` — gọi song song `bom-products?keyword=` (race guard _reqSeq bao cả 2), hàng BOM prepend trang 1, cột thiếu "—", badge theo source, hint tổng riêng (total pagination = ERP)
- [x] Đổi key selection `erp_product_id` → `_uid` (`erp_<id>`/`bom_<id>`) mọi chỗ, payload apply không chứa _uid
- [x] Swap `BomBuilderEditor.vue` sang popup mới (3 màn bom-list add/edit/detail); KHÔNG xoá popup cũ (dead code, xoá sau merge)
- [x] Test Playwright: bom-list/add popup 19 filter + apply ERP qty=1; BOM edit thấy hàng BOM (seed tạm, đã xoá sạch); regression quotations OK — review Approved (2 Minor chấp nhận: Promise.all fail-fast bằng hành vi cũ, total không cộng hàng BOM)

## Phase 6 — UX popup: nút Tìm kiếm + ẩn/hiện bộ lọc + sticky cột (user yêu cầu 2026-07-04)

- [x] Refactor khối filter dùng `V2BaseFilterPanel` (pattern /assign/application): quick search = "Tên hoặc mã", 18 filter trong slot advanced (mặc định THU GỌN khi mở popup), nút "Tìm kiếm" (search ngay, huỷ debounce), toggle ẩn/hiện không mất giá trị, reset của panel thay nút "Làm mới" cũ; "Thêm hàng tạm" chuyển lên trên bảng
- [x] Sticky 4 cột đầu (checkbox 40px / Ảnh 56 / Loại HH 130 / **Tên hàng hoá** 220 — left cộng dồn 0/40/96/226, pattern BomBuilderTableCard), header sticky cả top+left z-index 3, background đục mọi state
- [x] Test Playwright 8 bước pass (thu gọn/xổ/giữ giá trị, auto-search + nút Tìm kiếm áp filter ẩn, reset, sticky khi scroll ngang, apply qty=1) — review Approved, chỉ 2 minor cosmetic (subtitle chết do panel comment, hover cột sticky mất màu xanh nhạt)

## Phase 6b — Nén không gian popup (user yêu cầu 2026-07-04)

- [x] Nén toàn popup (CSS-only, 1 file): modal head/body/footer 14-20px → 8-16px, tab content 16→6px, filter panel ::v-deep p-3→8/10px bỏ shadow, filter-row mb 8→4px, cell bảng 4-6px font 12px, thumbnail 40→32px, vùng bảng max-height 420px → calc(100vh-340px) min 260px. Số dòng bảng thấy được: 4 → 8 (thu gọn), ~1 → ~4 (xổ filter). Sticky offsets giữ nguyên khớp (verify scrollLeft=400), console sạch. Ảnh before/after: scratchpad/phase6b_shots/

## Phase 6c — Loading table + Enter mới search + no-data xám (user yêu cầu 2026-07-04)

- [x] Loading row chuẩn V2BaseDataTable (spinner + "Đang tải dữ liệu...") khi lọc/chuyển trang, ẩn rows + pagination lúc loading
- [x] Empty state "Không có dữ liệu phù hợp bộ lọc." xám nghiêng #9ca3af (chuẩn V2BaseDataTable)
- [x] Ô "Tên hoặc mã": gõ KHÔNG search — chỉ Enter / nút Tìm kiếm / X clear; dropdown filter giữ auto-search (verify network: gõ 15 ký tự 0 request)
- [x] Text đỏ no-data: quét computed style toàn DOM popup KHÔNG tìm thấy chỗ nào đỏ (select2 no-results màu đen xám) — cần user chỉ chỗ thấy đỏ nếu vẫn còn

## Phase 6d — Nút X đóng popup (user yêu cầu 2026-07-04)

- [x] Thêm `button.close` (&times;) vào modal-head theo skill modal-popup (thay comment nút Đóng cũ), header sẵn flex space-between → X góc phải; verify Playwright trên bom-list/add: X hiện đúng vị trí, click đóng popup, backdrop click vẫn đóng như cũ

## Phase 6e — Popup 95% + top scrollbar + nén cột số + fix select2 multiple (user yêu cầu 2026-07-04)

- [x] Popup 95vw × 95vh, body flex — bảng flex-grow lấp hết chỗ (bỏ max-height calc cứng)
- [x] Thanh scroll ngang PHÍA TRÊN bảng sync 2 chiều (port pattern table-top-scroll của V2BaseDataTable), tự ẩn khi không cần scroll
- [x] Nén cột số (Định mức ĐP giá/SL tồn/SL KM/SL LR/VAT/Bảo hành ~70-90px, header wrap 2 dòng font 11px) → @1440 đủ 16/16 cột KHÔNG cần scroll ngang; @1200 scroll trên+dưới hoạt động
- [x] Fix select2 multiple không hiện caret/placeholder: nguyên nhân init lúc panel v-show ẩn → search field width ~0; fix CSS ::v-deep ép width 100% min 120px (không sửa component chung) — placeholder "Tất cả" + caret hiện ngay khi click
- [x] Sticky offsets cập nhật theo width mới, verify Playwright @1440/@1200, console 0 error (ảnh .playwright-mcp/phase6e_shots/)

## Phase 6f — Không đóng popup khi click ngoài / khi Thêm hàng (user yêu cầu 2026-07-04)

- [x] Bỏ `@click.self` đóng popup trên backdrop (chỉ đóng bằng X / nút Đóng — user yêu cầu, override khuyến nghị backdrop-close của skill modal-popup)
- [x] "Thêm N hàng hoá" KHÔNG đóng popup: bỏ emit close trong applySelection, reset tick + toast success "Đã thêm N hàng hoá vào phiếu." để user chọn tiếp
- [x] Verify browser thật (bom-list/add): backdrop click giữ popup, apply giữ popup + toast + counter về 0 + dòng vào bảng BOM, X vẫn đóng được. Lưu ý dev: HMR từng serve bundle stale do ENOENT lúc ghi file — touch file + hard reload là sạch
- [x] Overlay "Thêm hàng tạm" + overlay Quick Add (model/brand/origin): click ra ngoài cũng KHÔNG đóng (đồng bộ), chỉ đóng bằng X/Huỷ — verify browser: backdrop giữ overlay, X đóng được, popup chính không ảnh hưởng
- [x] Nút X overlay Thêm hàng tạm + Quick Add đổi sang UI giống popup chính (`button.close` &times; chuẩn Bootstrap, thay bom-close-btn icon vuông; xoá CSS chết) — verify computed style trùng popup chính, X đóng OK

## Phase 7 — Confirm cộng dồn / tạo dòng mới khi thêm hàng trùng (user yêu cầu 2026-07-04)

- [x] Modal: prop `existingProducts` (computed reactive từ 2 parent), detect trùng theo key (erp_product_id / code) + scope (nhóm đích, cha-con), overlay confirm 3 lựa chọn: Cộng dồn số lượng / Tạo dòng mới / Huỷ (bỏ qua hàng trùng, giữ tick nếu toàn trùng)
- [x] edit.vue: nhánh `_merge_qty` → tìm dòng cùng key+nhóm+cha, `qty_needed += 1`, KHÔNG push, KHÔNG re-fetch hàng con công thức; BomBuilderEditor: tương tự với `qty` (con chỉ so parentRowId — vá open-pick 2 biến thể)
- [x] Test Playwright 5 case pass (lần 1 không confirm; cộng dồn 1→2; tạo dòng mới; huỷ nguyên trạng; mix trùng+mới) — review Approved, 4 Minor ghi nhận: hàng tạm emit thẳng không qua confirm (code auto-sinh, khó trùng), `return` pre-existing nhánh service edit.vue nên đổi `continue`, Huỷ mix xoá tick cả hàng trùng, toast đếm cả item cộng dồn

## Phase 8 — Thông số kỹ thuật đúng format gốc như ERP (user yêu cầu 2026-07-04)

- [x] Helper mới dùng chung `utils/specHtml.js` (`renderSpecHtml`): có thẻ HTML → sanitize nhẹ (bỏ script/style/iframe/on*/javascript:, GIỮ b/strong/i/em/u/p/br/ul/ol/li/span/div + style) render nguyên định dạng; text thuần → escape + `\n`→`<br>`. Mixin global `$specHtml` đăng ký trong plugins/global-mixins.js (theo pattern CheckPermission sẵn có)
- [x] Áp cho MỌI chỗ hiển thị: edit.vue (2), quotations/_id/index.vue (2), product-project/index.vue (1), BomBuilderTableCard (4), QuotationPrintPreview (3 — file feature song song, sửa tối thiểu để bản in giữ đậm/nghiêng). Chỗ nhập liệu (editor) giữ nguyên; BomExportModal (Excel) không đụng
- [x] Đối chiếu ERP thật: 23.706 sản phẩm đều lưu HTML (0 dòng \n thuần — dạng \n chỉ phát sinh từ import Excel/nhập tay HRM, helper vẫn xử lý); E2E: thêm TEWI-865011 qua popup → bảng BOM giữ nguyên `<em><strong>` + entity như ERP; inject `<script>`/onclick bị lọc; console sạch. Lưu ý: cột Thông số kỹ thuật ở bảng BOM ẩn/hiện theo cấu hình cột (visibleColumns)
- [x] Fix bổ sung (user báo "vẫn không được" ở mẫu in): thủ phạm là CSS `td.cell-spec { white-space: pre-line }` (tàn dư bản fix strip-text) — nội dung giờ là HTML nên newline TRONG SOURCE giữa các thẻ tạo dòng trống thừa, nhìn xấu hơn khối thông tin khách hàng. Đổi về `normal` + margin gọn cho p/div ở CẢ preview lẫn CSS cửa sổ in. Verify trên báo giá thật id=3: đậm/nghiêng render (21 ô), whiteSpace=normal, từng gạch đầu dòng xuống dòng đúng (ảnh scratchpad/phase8b_spec_print.png)
- [x] Fix bổ sung 2 (user: "bấm In thấy được, xem trước chưa được" — case Ghi chú Quan Trọng BG-2026-00160): theme app có rule GLOBAL `b, strong { font-weight: 500 }` đè chữ đậm thành 500 ở modal XEM TRƯỚC (cửa sổ in là document riêng nên không dính → In đẹp). Ép `font-weight: 700` cho strong/b trong vùng spec ở 5 chỗ: QuotationPrintPreview (.cell-spec), edit.vue + _id/index.vue (.q-spec-preview ::v-deep), BomBuilderTableCard + product-project (.spec-preview ::v-deep). Verify: computed strong = 700, em = italic trong preview local

## Phase 9 — Popover hover "Đặc điểm" trên tên hàng hoá giống ERP (user yêu cầu 2026-07-08)

- [x] ERP `HrmProductSearchController`: thêm `standard_accessories` vào response; decode `htmlspecialchars_decode` vì Yajra escape mọi cột ngoài rawColumns (product_attributes thoát nhờ có trong whitelist) — KHÔNG sửa rawColumns của hàm dùng chung
- [x] hrm-api `ErpProductSearchService`: passthrough `standard_accessories`
- [x] FE `QuotationProductSearchModal`: hover tên hàng → popover fixed (z-index 5030, max 320px, pointer-events none) hiện "Đặc điểm" (u+b, fallback "Chưa có đặc điểm") + "Phụ kiện tiêu chuẩn" (chỉ khi có), nội dung qua `$specHtml`, ép strong/b=700 (né theme global 500), tự né mép màn hình (đo sau render, lật sang trái/kéo lên), ẩn khi mouseleave + khi doSearch reload
- [x] Verify Playwright local (bom-list/add): popover hiện đúng cạnh phải cell, đủ 2 mục, không còn literal `&lt;div&gt;`, label weight 700, mouseleave ẩn, case rỗng hiện "Chưa có đặc điểm" (ảnh scratchpad/spec-popover.png)
- [x] Tên hàng hoá đổi sang dạng link như ERP (`a.product-name-link` xanh #007bff, hover underline) để user biết hover được — click vẫn tick chọn dòng (bubble lên td); verify Playwright: màu link đúng, hover hiện popover, click toggle checkbox OK (ảnh scratchpad/name-link.png)

### Checkpoint — 2026-07-03 (wrap up, feature CODE DONE)
Vừa hoàn thành: cả 4 phase code + review từng phase + test UI Playwright 12/12 + final review READY.
Đang làm dở: không.
Bước tiếp theo: user review code working tree 3 repo (CHƯA commit theo quy tắc) → quyết 2 việc Important ở mục "Việc còn lại" → user tự commit. LƯU Ý khi commit: working tree còn file của feature KHÁC làm song song cùng ngày (`task-assignee-all-company`: hrm-api `SolutionVersionsReportService.php` + hrm-client `CreateTaskModal.vue`) → tách commit theo feature. File của feature NÀY: TanPhatDev (`app/Http/Controllers/Api/HrmProductSearchController.php` + `routes/api.php`), hrm-api (`ErpProductSearchService.php` + `QuotationController.php` + `Routes/api.php`), hrm-client (`QuotationProductSearchModal.vue` + `_id/edit.vue`).
Blocked: không.

## Bugfix — 2026-07-24: Ô "Tên hoặc mã hàng hoá" tìm thêm theo Model (parity với Báo giá ERP)

Popup Thêm hàng hoá (BOM Giải pháp + Báo giá) ô "Tên hoặc mã" chỉ khớp products.name/code, không khớp Model → mở rộng khớp cả pm.name (tên model), giống hàm `searchProductStockBuyer` của Báo giá ERP.

### BE (ERP TanPhatDev)
- [x] `SearchController::searchProductStockBuyerApi()` (~dòng 1369) — thêm `->orWhere('pm.name','like','%name%')` vào nhánh lọc `$request->name`, mirror bản `searchProductStockBuyer` (dòng 953-957). Join `product_models as pm` đã có sẵn. Ảnh hưởng 2 consumer: HRM popup (HrmProductSearchController) + endpoint modal-data searchProductStockBuyer — đều là search "Tên hoặc mã", broadening nhất quán.

### Checkpoint — 2026-07-24 (đã test)
Vừa hoàn thành: thêm khớp Model (pm.name) vào ô "Tên hoặc mã" của searchProductStockBuyerApi (ERP).
Kết quả test:
- DB (ERP tinker) so OLD vs NEW: kw 'XR.294096' 0→1, 'GLM 50C' 0→1, 'MN-E-GEQ-DNDAU140' 1→1 (không phá match cũ).
- E2E qua HRM API erp-product-search (đúng API popup gọi): name='XR.294096' (chỉ khớp model) trả đúng id 10123. Trước fix trả 0.
- Ghi chú: 'GLM 50C' trả 0 qua API do product id 23641 bị ERP loại theo filter nghiệp vụ (tìm bằng chính code 'CH-GLM50C' cũng 0) — không liên quan model-search.
Đang làm dở: không
Bước tiếp theo: (tuỳ chọn) test UI popup thực tế; commit khi user yêu cầu (repo TanPhatDev).
Blocked: không

### FE — placeholder ô tìm kiếm
- [x] `QuotationProductSearchModal.vue` — đổi `quickSearchPlaceholder` "Nhập tên hoặc mã hàng hoá..." → "Nhập tên, mã hoặc model hàng hoá..." (phản ánh việc search đã hỗ trợ Model). Popup dùng chung BOM + Báo giá.
