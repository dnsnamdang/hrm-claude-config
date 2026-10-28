# SDD ledger — plan: HRM/.plans/gop-db/quan-ly-hang-hoa/popup-tim-kiem-hang-hoa/plan.md
Spec: HRM/docs/superpowers/specs/gop-db/2026-10-13-popup-chon-hang-hoa-dung-chung-design.md
BASE: hrm-api bbc4cf8b2, hrm-client baad69b58 (nhánh feat/cdhh-p4-popup-chon-hang từ feat/chuyen-doi-hang-hoa)
Ruling: ledger để cạnh plan (.plans ngoài git) thay vì workspace sdd — plan không nằm trong repo nào, script sdd cần repo — cost if wrong: không có.
Ruling: tạo nhánh ở 2 repo hrm-api + hrm-client (plan ghi checkout ở thư mục worktree, nhưng đó không phải repo) — cost if wrong: không có.
Pre-flight: T3→T4 subquery(int) khớp · T1→T4 cột is_service_product/is_service_quotation khớp · T4→T5 query() trả Query\Builder chưa select khớp rows(Builder) · T5→T6 rows() chữ ký khớp · T4/T5→T8 items dùng query()+rows() khớp · OPTIONAL_COLUMNS (T5) dùng trong Request (T6) — T6 phải sau T5 ✓.
Task 1: complete (hrm-api bbc4cf8..e1b0c9eaf, tests: phpunit ProductNatureServiceFlagsTest → OK 3/3; ProductNatureAutoPartsTest → OK 2/2; migration 2026_10_13_000001 đã chạy vào hrm_erp_giacty)
Task 2: Ruling: nới 2 cột danh sách 130/140 → 160/180px — Playwright đo chữ tiêu đề tràn (116>113, 135>123) — cost if wrong: bảng rộng thêm 70px.
Task 2: Ruling: không đăng nhập tài khoản thiếu quyền riêng — gate chỉ đọc là code cũ (isShow) không đổi; đã đo 3 ô disabled ở chế độ xem — cost if wrong: thấp.
Task 2: complete (hrm-client baad69b..ee5236b5b, Playwright MCP: th 1 dòng 33px không tràn; 2 checkbox cùng top 249, ô phải thẳng cột Phụ tùng ô tô left 749; Lưu → danh sách "Có/Có"; mở xem: checked+disabled; bản ghi TCHH.P4SV đã xoá khỏi DB dev)
Task 3: Ruling: test tắt FOREIGN_KEY_CHECKS trong phiên (bật lại tearDown) + điền cột NOT NULL đo bằng SHOW COLUMNS — bảng kho có FK tới employees/kho/lô; test kiểm công thức — cost if wrong: test không bắt lỗi FK (không thuộc phạm vi reader chỉ đọc).
Task 3: Ruling: thêm ca phiếu status 3 (không trừ) + ca mảng id rỗng — phủ đủ nhánh công thức — cost: không.
Task 3: complete (hrm-api e1b0c9e..336c4195b, tests: phpunit SellableStockReaderTest → OK 2 tests 3 assertions)
Task 4: Ruling: fixture products điền brand/manufacture/origin/created_by (NOT NULL, đo SHOW COLUMNS) + tắt FK trong phiên test; hàng "khớp" dùng thương hiệu KHÁC mặc định (plan để cả 2 hàng chung thương hiệu ⇒ ca brand_ids sai) — cost: không.
Task 4: Ruling: $paths rút gọn thành hằng CLASSIFICATION_PATHS (plan đã ghi phải rút gọn) — cost: không.
Task 4: Ruling: thêm ca business_scope_id + ca từ khoá < 2 ký tự bị bỏ qua — cost: không.
Task 4: complete (hrm-api 336c419..4e0aaf70c, tests: phpunit ProductPickerSearchTest → OK 7 tests 21 assertions; productables đã xác nhận product_id = phụ tùng, productable_id = máy)
Task 5: Ruling: "Định mức đàm phán giá" không có cột trên products (plan đoán products.sale_max_percent) ⇒ đọc product_unit_prices.sale_max_percent của ĐVT cơ bản theo bảng giá qua ProductPriceReader::pricesByUnit (null khi không truyền bảng giá) — giữ whitelist G3 xanh — cost if wrong: cột hiện định mức của ĐVT cơ bản thay vì ĐVT khác.
Task 5: Ruling: cột tuỳ chọn trả theo thứ tự cố định OPTIONAL_COLUMNS (test sửa kỳ vọng) — FE tự sắp theo cấu hình cột — cost: không.
Task 5: complete (hrm-api 4e0aaf7..2348b901b, tests: ProductPickerSearchTest → OK 8 tests 28 assertions; PriceReaderWhitelistTest → OK 2 tests)
Task 6: Ruling: test dùng helper actor() (luôn kèm quyền "Xem dữ liệu hàng hoá công ty" để actAs tạo role, rồi insert company_roles kèm timestamps) thay allowCompanies/auth()->id() của plan — actAs trả employeeId, auth()->id() trong test không đáng tin — cost: không.
Task 6: Ruling: thêm priceTypeId() vào Request + failedAuthorization() thông báo tiếng Việt; thêm ca columns[]=bogus ⇒ 422 — cost: không.
Task 6: complete (hrm-api 2348b90..79b1e6432, tests: ProductPickerApiTest → OK 4 tests 18 assertions)
Task 7: Ruling: từ khoá test gắn token uniqid (plan dùng "P4T Bơm" cố định — dễ dính hàng thật/ca khác) + ca 403 đặt luôn trong file test này — cost: không.
Task 7: complete (hrm-api 79b1e64..071c06c2a, tests: ProductPickerTreeCountsTest → OK 2 tests 7 assertions)
Task 8: Ruling: ĐVT trả {unit_id, unit_name, is_base(bool), unit_coefficient, price} (+cost_price khi có quyền) thay {product_unit_id,…} của A3 — unitOptions không có product_unit_id; unit_id duy nhất trong 1 hàng — cost if wrong: FE 4.3 tra ĐVT theo unit_id.
Task 8: Ruling: items bỏ cost_price khỏi ĐVT khi không quyền (unitOptions luôn kèm giá vốn) — chặn lộ giá vốn — cost: không.
Task 8: Ruling: đo thấy machine_id + include_service_shared > 60s (server dev 8031 chết, đã khởi động lại PID mới) — nguyên nhân EXISTS tương quan trên productables không index trong nhánh OR ⇒ đổi sang IN subquery không phụ thuộc (cả whereProductable), test EXPLAIN chặn hồi quy; KHÔNG thêm migration index (mọi ca < 1s) ⇒ không cần hỏi user chạy migration — cost if wrong: dữ liệu productables tăng mạnh thì cần index sau.
Task 8: đối chiếu tồn HRM↔ERP 15.345 dòng lệch 0; đo 9 ca 0,32–0,68s (doi-chieu-ton.md).
Task 8: complete (hrm-api 071c06c..0b068b8f5, tests: ProductPickerSearchTest OK 9/31 · ProductPickerTreeCountsTest OK 2/7 · ProductPickerApiTest OK 4/18 · ProductPickerItemsTest OK 3/19 · SellableStockReaderTest OK 2/3 · ProductNatureServiceFlagsTest OK 3/11 · ProductNatureAutoPartsTest OK 2/7 · PriceReaderWhitelistTest OK 2/45)
Final review: reviewer mới (opus) — 0 Critical, 3 Important, 6 Minor.
Final: fixed I-1 quyền giá vốn xét công ty đang làm thay vì công ty chứng từ (lộ giá vốn cty khác) — quyen_gia_von_xet_theo_cong_ty_chung_tu RED (195989760 thay vì null) → GREEN; canSeeCost(companyId) đọc role_has_permissions.company_id = công ty chứng từ.
Final: fixed I-3 test công ty chứng từ quá yếu — thay bằng cong_ty_chung_tu_khac_cong_ty_dang_lam_doc_ton_cua_cong_ty_chung_tu (tồn giả chỉ ở cty 6: 7 vs 0).
Final: fixed I-2 tree-counts cộng dồn đếm trùng cấp trên — cap_tren_dem_phan_biet_khop_so_dong_khi_bam_nhanh RED (Undefined index groups) → GREEN; BE trả clusters/groups/chapters/scopes đếm phân biệt (gộp luôn M-4: join đủ cây, bỏ dòng mồ côi). Suite MasterData 495/495.
Final: minor (deferred): M-1 SellableStockReader bỏ kho KM ở WHERE — hàng chỉ có tồn ở kho KM + có giữ hàng: ERP ra âm, HRM ra 0 (đối chiếu thật lệch 0).
Final: minor (deferred): M-2 company_id=abc ra 403 thay vì 422 (authorize chạy trước rules).
Final: minor (deferred): M-3 ngưỡng 2 ký tự đo sau escape — gõ 1 ký tự % hoặc _ vẫn tìm.
Final: minor (deferred): M-5 page vượt last_page trả data rỗng — FE 4.3 tự kẹp trang.
Final: minor (deferred): M-6 promo_warehouse_ids rỗng "" thêm 0 vào NOT IN — vô hại.
Final: note — tree-counts in_stock + include_uncataloged đo 0,9s (sát mục tiêu 1s).
Final: fixed M-1 (user cho làm 13/10) — chi_co_ton_kho_khuyen_mai_va_dang_giu_hang_ra_so_am_nhu_erp RED (0) → GREEN (−3); bỏ kho KM trong SUM(CASE) như ERP; đối chiếu lại 15.345 dòng lệch 0; commit 152c70ad1, merge 7e5c63b1a (chưa push).

## Bước 4.3 (Phần C) — BASE hrm-api 7e5c63b1a, hrm-client aa13b7038, nhánh feat/cdhh-p4-3-popup-fe (user 'Làm' 13/10)
T9: complete (hrm-api 7e5c63b..ba8d65c16, tests: ProductPickerItemsTest OK 4/22 · ProductPickerApiTest OK 5/27 · PriceReaderWhitelistTest OK)
T12: Ruling+fix BE: 403 với chính công ty đang làm việc khi company_roles trống (role gắn công ty qua employee_has_roles.company_id) — allowedCompanyIds() = công ty đang làm ∪ employee_has_roles.company_id ∪ company_roles; test cong_ty_dang_lam_viec_luon_duoc_phep_khi_company_roles_trong RED(403)→GREEN; commit 10dad8aad
T9b: items thêm standard_accessories (hover tên hàng) — test RED→GREEN, hrm-api 9c2bb471c.
T10: complete (hrm-client 453f6ed04) — Ruling: gộp levelCounts+selectAnyLevel thành 1 prop `picker` (+levelCounts, selectedKey, extraRows, popoverContainer) — picker cần thêm dòng gốc + toggle 1 nút, tách prop lẻ dễ lệch — cost: không. Playwright: popup Xây dựng catalog giữ 2 nút mở/thu, ghi chú, số chỉ ở nút đóng >0.
T11: complete (hrm-client 2f7448a11) — Playwright: trang Dữ liệu hàng hoá công ty mở đúng 1 modal id cũ; picker mở product-picker-columns-N.
T12: complete (hrm-client 0b393fe94) — Ruling: tooltip đặc điểm (Phần 2 đã duyệt) đọc qua items khi hover, đệm theo id — search không có thông số. Ruling: cột Tên co giãn (min 200) để bộ cột mặc định vừa 1440 không cuộn ngang (đo 1041=1041). Ruling: nâng z-index lớp bọc modal cột (5060) + tooltip (5040) + popover gắn vào khung popup — overlay báo giá z 5000 che mất (đo, ảnh p43-colcfg.png). Ruling: ô Tên flex để "Đã có" không bị "…" che (đo badge nằm trong ô).
T13: complete (hrm-client 4816cdb3c) — Playwright báo giá 279: tick 2 hàng giữ qua trang 2, Thêm 2 ⇒ 2 dòng vào lưới (xuất xứ, đặc điểm, SL 1, giá dự kiến, giá niêm yết = giá popup), tick tự xoá; bấm tên ⇒ thêm ngay, popup không đóng; hàng đã có ⇒ hộp cộng dồn; "Đã có" đúng 2 hàng. Không quyền giá vốn (báo giá 280, E2E No Cost): không có cột Giá vốn trong cấu hình, items không có cost_price ở hàng + ĐVT, lưới "—". BOM 25: popup chạy (khối "Hàng đã có trong BOM" không có dữ liệu thật để đo — BOM sửa được đều 0 hàng). Phiếu điều chuyển (block): lần 2 không thêm + toast "đã có trong phiếu", ẩn "Thêm hàng tạm". Cấu hình cột lưu + tải lại còn; đã xoá bản ghi test user_column_settings id 61.
T14: complete (hrm-client b96d8944b) — git grep 0 chỗ gọi trước khi commit (lần grep đầu hỏng vì glob zsh, đã kiểm lại đúng).
T15: complete — e2e/tests/assign/product-picker-ui.spec.ts (ngoài git; 4 ca: số đếm + khuôn, tick/Thêm/bấm tên/Đã có, modal cột nổi trên overlay, không quyền giá vốn). tsc không lỗi; CHƯA chạy (chỉ chạy khi user yêu cầu).
Final review 4.3: reviewer mới (opus) — 0 Critical, 1 Important, 10 Minor.
Final: fixed I-1 chọn >200 hàng ⇒ items 422, không thêm gì — Playwright tái hiện (300 tick ⇒ 1 request ⇒ toast "The given data was invalid.") → fetchItems chia lô 200 ⇒ 2 request (200+100), báo giá 55 → 355 dòng. Commit 860587e96.
Final: fixed M-3 (nâng Important: bấm đúp ⇒ thêm trùng dòng vào chứng từ) — cờ applying + nút không bấm được khi đang tải; đo bấm đúp chỉ 1 cặp request.
Final: e2e spec bổ sung (theo review): kiểm nội dung lưới báo giá (mã + giá niêm yết = cột Giá bán), chỉ chọn hàng chưa "Đã có", ca >200 hàng + bấm đúp.
Final: minor (deferred): M-1 selectAllFiltered không chặn race/không try-catch/bấm đúp chạy song song.
Final: minor (deferred): M-2 panel thiếu beforeDestroy xoá timer từ khoá (đóng popup trong 400ms vẫn gọi API).
Final: minor (deferred): M-4 hàng bị BE loại (khoá/ra khỏi phạm vi giữa lúc tick và Thêm) mất im lặng, không báo.
Final: minor (deferred): M-5 không xác định được công ty đang làm việc ⇒ tab Hàng hoá trống không báo.
Final: minor (deferred): M-6 import V2BasePagination + CSS .row.paging thừa trong QuotationProductSearchModal.
Final: minor (deferred): M-7 priceTypeId chuỗi từ màn ⇒ cảnh báo kiểu prop Vue.
Final: minor (deferred): M-8 id ⓘ dòng gốc cây không kèm uid (2 picker cùng lúc trùng id).
Final: minor (deferred): M-9 rê nhanh qua tên gọi items mỗi dòng (có đệm).
Final: minor (deferred): M-10 (có từ trước) thêm nhanh trúng hàng trùng ⇒ chọn cộng dồn/tạo dòng mới xoá luôn các tick khác.
E2E 14/10: product-picker-ui 5/5 (sửa spec: selector hasText vì glyph icon V2BaseButton, setTimeout 180s, đo không cuộn ngang ở 1440 + 1280 bảng tự cuộn, ca phân trang bật gồm hàng chưa xếp catalog thay skip); products-catalog-popup-ui 7/7; price-asking-temp-product + quotation-unit-select 14/15 — N92 spec nocost gõ cứng giá cũ (có sẵn, không do 4.3).

## Bước 4.4 (Phần D) — BASE hrm-api 41a64bed6 (nhánh feat/cdhh-p4-4-erp-popup), ERP 3aaae676fe (nhánh feat/cdhh-p4-4-popup) — user "Làm" 14/10
Brief/report: sdd-44/. Spec: §5.3 + khao-sat-4.4.md §6 (Q1–Q5) là căn cứ.
Pre-flight:
| Cặp | Bên làm ⇒ bên dùng | Kết quả |
|---|---|---|
| D-T1 ⇒ D-T3 | tham số `scope`, `only_ids[]`, `service_quotation_only`, POST search/tree-counts ⇒ proxy gọi POST | khớp |
| D-T2 ⇒ D-T3 | `LegacyPickerScope::resolve(array $legacy, int $companyId, int $employeeId): ?array{ids, stock_label, stock_map}` ⇒ proxy | khớp (chốt chữ ký ở đây) |
| D-T3 ⇒ D-T4 | route `/admin/hrm/product-picker/*` + whitelist options + column-customizations ⇒ popup JS | khớp |
| D-T4 ⇒ D-T5/D-T6 | popup mới API JS `$scope.openProductPicker(config)` ⇒ 2 adapter | khớp (chốt ở D-T4) |
| D-T5 ↔ D-T6 | cùng include `productPicker` — trang có cả 2 partial / partial include 2 lần (project_quotations) | Ruling: partial mới tự chống include trùng (cờ PHP), 2 adapter dùng chung 1 modal id — cost: thấp |
| D-T1 tự thân | `scope=all` "toàn bộ hàng" vẫn loại hàng tạm (pcc 6/7/8) + hàng làm dịch vụ | Ruling: hàng tạm = có dòng pcc status 6/7/8 ở BẤT KỲ công ty — cost: hàng tạm đã duyệt thành hàng thật mà còn dòng 7 cũ sẽ bị ẩn ở báo cáo |
| D-T2 tự thân | test ERP chạy sqlite :memory: (phpunit.xml) — so tập id với endpoint cũ trên giacty không chạy được trong phpunit | Ruling: unit test trên sqlite dựng fixture; đối chiếu với endpoint cũ trên giacty làm bằng script đọc (tinker --execute) ghi kết quả vào report — cost: không |
| D-T6 tự thân | `is_service_quotation:false` (merchandise) không tác dụng server | giữ chặn `product_type=='product'` phía client như cũ |
Ruling: D-T2 (ERP) chạy song song D-T1 (hrm-api) — 2 repo khác nhau, không chung file — cost: không.
Ruling: `has_stock` KHÔNG kèm `is_self_inventory` (kiểm kê ×2, kiểm kê KT ×2, YC giữ hàng) ⇒ map sang công tắc "Còn tồn" khoá bật (tồn bán được công ty — đúng hành vi server hôm nay: `warehouses`/`warehouse_id` bị bỏ qua ở nhánh này, SellableStockReader đã đối chiếu lệch 0), KHÔNG dùng only_ids — cost: nếu user muốn kiểm kê theo tồn kho thật thì phải đổi sau (hôm nay cũng không có).
D-T1: implementer xong (hrm-api 41a64bed6..0700701fe; Search 13 · TreeCounts 4 · Api 7 · Items 4 · SSR 3 · Whitelist 2) — đang review.
D-T2: implementer xong (ERP 3aaae676fe..c3884e6484; LegacyPickerScopeTest 11/11, ERP 119/119; đối chiếu giacty lệch 0 — service_contract 0=0 do bảng rỗng) — đang review. Nhiều tuỳ chọn ⇒ giao tập (khớp AND cũ).
Ruling: modal popup mới đổi id thành `searchProduct` khi thay ruột (D-T5) — 47 file ERP gọi `$('#searchProduct').modal('hide')` trong callback; giữ id để khỏi sửa 47 file — cost: D-T4 dùng id tạm `productPickerModal`, D-T5 phải đổi + kiểm CSS scoped theo id.
Ruling: chọn nhiều chỉ khi màn bật `has_checkbox_all` (popup `searchProduct`) — các màn khác giữ hành vi cũ "bấm tên = thêm 1, popup không đóng" — tránh báo cáo/màn gán `form.product` bị ghi đè bởi nhiều hàng — cost: màn kho muốn thêm nhiều phải bấm từng tên như hôm nay.
Ruling: popup KM `searchProductPromotion` (markup ở `searchProductPromotions.blade.php` — partial phụ của 4.5) KHÔNG đổi ở 4.4; PL HĐ mua TN v2 tab KM dùng popup cũ tới 4.5 — cost: 1 màn dùng 2 popup khác kiểu tạm thời.
Ruling: HRM Row thêm `brand_id` (D-T5, hrm-api) — 4 màn BH hãng từ chối hàng khác thương hiệu bằng `row.brand_id` — cost: không.
Ruling: bỏ cột "tồn lắp ráp" + nút mở popup tồn lắp ráp trong popup báo giá (N+1 mỗi dòng, không có trong mockup đã duyệt); ghi N95 để user quyết — cost: người lập báo giá mất lối xem nhanh tồn lắp ráp ngay trong popup.
D-T1: ⚠️ hiệu năng scope=all — controller tự đo trên giacty: không lọc 45.890 hàng search 0,17s / tree 0,07s; từ khoá "bơm" 0,18/0,21s; còn tồn 0,34/0,44s (giacty có 0 hàng tạm, 17.512 hàng status 0 ⇒ total 45.890 đúng).
D-T1: minor (deferred): only_ids_set chuỗi "false" vẫn truthy.
D-T1: minor (deferred): validate only_ids.* 20.000 phần tử có thể chậm.
D-T1: minor (deferred): thiếu test POST scope=all.
D-T1: complete (hrm-api 41a64bed6..0700701fe, review clean)
D-T2: minor (deferred): is_self_inventory + has_prepick cùng lúc ⇒ nhãn/map giữ hàng đè nhãn tồn kho (tập id giao đúng).
D-T2: minor (deferred): thiếu test kết hợp nhiều tuỳ chọn / tập rỗng.
D-T2: minor (deferred): đối chiếu giacty bằng SQL thô, service_contract không có dữ liệu thật.
D-T2: complete (ERP 3aaae676fe..c3884e6484, review clean)
D-T3: implementer xong (ERP c3884e6484..b66291792e; proxy 17 ca, ERP 136/136; gọi thật 8031 đạt; .env worktree + HRM_API_BASE_URL=8031) — đang review.
D-T3: review — Spec ❌ 1 Important: client gửi only_ids không kèm legacy ⇒ HRM bỏ lọc Đang KD (nới phạm vi). 6 minor.
D-T3: minor (deferred): scope=all do client chọn (giá bán không bảo mật — memory hang-hoa-khong-bao-mat; chỉ ảnh hưởng hàng ngừng KD).
D-T3: minor (deferred): giao tập rỗng trả 0 dòng không thông báo.
D-T3: minor (deferred): chuyển tiếp giá trị null.
D-T3: minor (deferred): thiếu test đường cookie token.
D-T3: fix round 1/5 dispatched (only_ids chỉ từ LegacyPickerScope; + token() exception ⇒ 401, cookie rỗng lùi session) — FIX_BASE b66291792e.
D-T3: fix round 1/5 (3 addressed, 0 open; commits b66291792e..516afa6b14; proxy 21 ca, ERP 140/140)
D-T3: complete (ERP c3884e6484..516afa6b14, review clean sau fix 1)
D-T4: implementer xong (ERP 516afa6b14..6ef28ce03a; Playwright đo đủ; xoá user_column_settings 62/63) — đang review. Controller ⚠️: thiếu tooltip hover tên (spec §3), 'Dùng cho máy' thiếu proxy item-search, guard 1 lần/trang.
D-T4: review — Spec ❌ 1 Important (thiếu hover Đặc điểm/PK tiêu chuẩn spec §3); rủi ro include 1 lần: không trang nào dính; Angular 1.3 OK; XSS OK. 8 minor (file review).
D-T4: fix round 1/5 dispatched (hover tooltip; item-search vào whitelist proxy + popup; guard theo lần render thay define(); escape toast) — FIX_BASE 6ef28ce03a.
D-T4: fix round 1/5 (4 addressed, 0 open; commits 6ef28ce03a..11fd52d2cf; proxy 22 ca, ERP 141/141)
D-T4: minor (deferred): hide.bs.modal gắn lúc script chạy — JS in trước markup thì hook rỗng.
D-T4: minor (deferred): 8 minor ở task-4-review.md (đọc khi final review).
D-T4: complete (ERP 516afa6b14..11fd52d2cf, review clean sau fix 1)
D-T5: BASE ERP 11fd52d2cf, hrm-api 0700701fe — dispatch.
D-T5: implementer xong (ERP 11fd52d2cf..3eaed211dc; hrm-api 0700701fe..d345fc125 brand_id; ERP 141, picker 28; Playwright 10 màn; role tạm 119930 + prepick 62066/62067 đã xoá) — đang review.
Ruling: chấp nhận thêm khoá `group_id` vào `Product::dataFor` (getData dùng chung) để `sale/services` lưu đúng nhóm — chỉ thêm khoá, không đổi khoá cũ — cost: nơi nào serialize getData nguyên khối có thêm 1 trường.
D-T5: ⚠️ beginning_stocks — controller kiểm: không is_self_inventory ⇒ resolve() null, proxy không chuyển warehouse_id ⇒ danh sách Đang KD như popup cũ (cũ cũng bỏ qua warehouse_id ở nhánh này). Đạt.
D-T5: ⚠️ accounting_prepick_cancel (2 modal #searchProduct) — chưa mở trình duyệt; đưa vào danh sách kiểm Playwright cuối (final).
D-T5: minor (deferred): pickAllRowsPromotion/removeAllRowsPromotion dùng biến đã xoá (code chết, hỏng sẵn).
D-T5: minor (deferred): sale/services getData lỗi thoát im lặng.
D-T5: minor (deferred): group_id mới trong dataFor không có test.
D-T5: minor (deferred): CSS select2 multiple cũ cho modal #searchProduct khác đã bỏ (không thấy ảnh hưởng).
D-T5: minor (deferred): không test tự động ánh xạ options ⇒ config.
D-T5: complete (ERP 11fd52d2cf..3eaed211dc, hrm-api 0700701fe..d345fc125, review clean)
D-T6: implementer xong (ERP 3eaed211dc..15918bedd2; ERP 141; Playwright đủ nhóm; role tạm 119931 đã xoá) — đang review.
Ruling: giữ @json danh mục cũ + $scope.search/resetSearchProduct/availableGroup trong partial báo giá (brief bảo bỏ) — 2 popup cũ khác trên báo giá DV CSKH (searchProductEquivalent, searchServiceProduct) + form barcode/model đọc chúng, bỏ ⇒ 68 lỗi — cost: còn truy vấn @json thừa ở 27 view tới 4.5.
D-T6: ⚠️ báo giá thường (quotations) không mở được ở local (tạo bị khoá, sửa chỉ phiếu status 3 tự tạo) — phủ bằng báo giá thanh lý cùng luồng.
D-T6: ⚠️ service_quotation_only ra 0 dòng trên dev (cờ Tính chất chưa có dữ liệu — thuộc việc quy đổi phân loại chặn go-live); Trang thiết bị / extend_product kiểm bằng stub.
D-T6: ⚠️ "trang có cả 2 partial": controller grep ở D-T4 review — không trang nào; chấp nhận.
D-T6: minor ⇒ chuyển vào D-T7: monkey-patch pp.quickPick ⇒ picker truyền {via:'name'|'add'} cho onPick; CSS chết #search-product-table ở 3 trang.
D-T6: minor (deferred): @json danh mục cũ vẫn chạy ở 18 báo cáo (4.5 gỡ cùng N94).
D-T6: minor (deferred): bấm mở popup máy 2 lần nhanh ⇒ getData 2 lần.
D-T6: minor (deferred): sqExistingIds nhận báo giá DV bán qua tên biến trang.
D-T6: minor (deferred): wr_product không truyền existingIds (vẫn có cảnh báo trùng cũ).
D-T6: complete (ERP 3eaed211dc..15918bedd2, review clean)
D-T7: implementer xong (ERP 15918bedd2..3914bef232; onPick {via}; xoá CSS chết 3 form báo giá; accounting_prepick_cancel đạt; role 119932 đã xoá) — đang review.
D-T7: minor (deferred): 2 minor ở task-7-review.md
D-T7: complete (ERP 15918bedd2..3914bef232, review clean)
Final review: dispatch (ERP 3aaae676fe..3914bef232, hrm-api 41a64bed6..d345fc125).
Final review: With fixes — 0 Critical, 1 Important (4 báo cáo gọi searchProduct() không tuỳ chọn ⇒ vẫn chỉ hàng Đang KD, trái Q2 — lỗ plan D1), 7 minor mới.
Ruling: sửa trong 1 lượt final: (I-1) 4 view báo cáo ⇒ scope all; (D-T4 #2) không làm mất mục cost_price trong cấu hình cột dùng chung HRM; banner HĐ ghi số HĐ (Q3); LegacyPickerScope chạy 1 lần/search; only_ids > 20.000 ⇒ thông báo rõ; test đường cookie token — cost: không.
Ruling: báo giá thường loại 2 nay lưu rate_liquidation = null (bỏ chế độ thanh lý) ⇒ ghi vào N93, không sửa (thanh lý sẽ ngừng) — cost: nếu N93 chậm, báo giá loại 2 tạo trong thời gian chờ thiếu % giảm thanh lý.
Final: fix wave (ERP 3914bef232..2f4fbf9e82): 4 báo cáo scope all · giữ cost_price/khoá HRM trong cấu hình cột · banner ghi số HĐ (meta.locked_label) · danh sách khoá cache theo lần mở popup (khoá NV+công ty+sha1(pick_session|legacy), TTL 600s) · >20.000 id ⇒ 422 tiếng Việt · test cookie token. Re-review: 6/6 addressed, 0 breakage. ERP 149/149.
Final: minor (deferred): danh sách khoá không làm mới trong 1 lần mở popup (tối đa 10 phút).
Final: minor (deferred): user_column_settings id 64 (user 13, product_picker) có sẵn — không phải dữ liệu test của 4.4.
Merge LOCAL: hrm-api feat/chuyen-doi-hang-hoa db6f95787 · ERP feat/2d1-erp-khong-loi 4a0b8a60e3 — CHƯA push. Sau merge: ERP 149/149, picker HRM 33/33.
Deploy: ERP prod cần HRM_API_BASE_URL + config:cache; giữ IS_USE_SSO=true; kiểm 1 lần trên staging có SSO (đường cookie jwt_token).
Ruling (đính chính 14/10): ruling "báo giá thường loại 2 lưu rate_liquidation null" SAI — màn /admin/quotations đã hỏng sẵn trên DB gộp (bảng quotations là của HRM); user chốt bỏ màn này ⇒ N96.
Push 14/10: hrm-api feat/chuyen-doi-hang-hoa db6f95787 · ERP feat/2d1-erp-khong-loi 4a0b8a60e3 (user chạy bằng !).

## Bước 4.5 (Phần E) — BASE hrm-api db6f95787 (nhánh feat/cdhh-p4-5-out-of-stock), ERP 4a0b8a60e3 (nhánh feat/cdhh-p4-5-popup-con-lai) — user "làm" 14/10
Brief/report: sdd-45/. Căn cứ: khao-sat-4.5.md §4–§5 + spec §5.3.
Pre-flight:
| Cặp | Bên làm ⇒ bên dùng | Kết quả |
|---|---|---|
| E-T1 ⇒ E-T2/E-T3 | `out_of_stock=1` ⇒ proxy whitelist + popup lọc 3 trạng thái | khớp |
| E-T2 ⇒ E-T3 | `stock_view{warehouse_id|warehouse_group_id}` + options kho/nhóm kho + `supplier` legacy ⇒ popup | khớp (chốt tên khoá ở E-T2) |
| E-T3 ⇒ E-T4/5/6 | config `stockView`, `stockFilter`, `showSupplierFilter` ⇒ adapter màn | khớp |
| E-T4/5/6 ⇒ E-T7 | gỡ file cũ chỉ sau khi hết chỗ dùng | Ruling: E-T7 chạy cuối, git grep 0 trước mỗi xoá — cost: không |
| E-T5 tự thân | 5 màn đặt hàng có modal `#searchProduct` tự viết trùng id popup mới | bỏ modal tự viết trước khi include partial mới |
Ruling: E-T1 (hrm-api) chạy song song E-T2 (ERP) — khác repo — cost: không.
E-T1: implementer xong (hrm-api db6f95787..dc5e579d5; Search 14 · Tree 4 · Api 8 · Items 4 · SSR 3 · WL 2) — đang review.
E-T1: review — Spec ✅ (⚠️ đo < 1s), 1 Important (lặp khối subquery in_stock/out_of_stock ⇒ tách helper), 4 minor.
E-T1: minor (deferred): thiếu test HTTP dòng trả về, ca out_of_stock=0, POST 422, giả định thứ tự kết quả.
E-T1: fix round 1/5 dispatched (helper chung + đo giacty) — FIX_BASE dc5e579d5.
E-T1: fix round 1/5 (1 addressed, 0 open; dc5e579d5..92ea83c5d; giacty out_of_stock search 0,32s / tree 0,48s, total 22.577)
E-T1: complete (hrm-api db6f95787..92ea83c5d, review clean)
E-T2: implementer xong (ERP 4a0b8a60e3..573667071a; ERP 167/167) — đang review.
Ruling: danh sách khoá thắng stock_view CHỈ khi nó có cột tồn riêng (tự kiểm kê / hàng đang giữ); khoá HĐ / NCC vẫn hiện "Tồn tại kho" theo kho chọn — nếu không, chọn NCC ở YC đặt hàng TN sẽ tắt Xem tồn — cost: không.
Ruling: công thức Tồn tại kho = floor(SUM(stocks.total_qty) / hệ số ĐVT cơ bản) như cột tồn popup cũ searchProduct2; nhóm kho thắng kho khi gửi cả 2; hàng không tồn hiện 0 thay "-" — cost: thấp.
E-T2: review — Spec ✅ · Approved; 0 Critical/Important; 5 minor. (d) danh sách kho cũ = Warehouse::getByAllCompany() (kho MỌI công ty, mặc định nhóm kho mặc định công ty user).
Ruling: ô Xem tồn giữ phạm vi cũ — kho mọi công ty + nhóm kho công ty user + mặc định nhóm kho mặc định; kho công ty khác được xem tồn (màn cũ đã cho) — cost: người đặt hàng thấy tồn kho công ty khác (như hôm nay).
Ruling: lọc Còn tồn/Hết tồn theo tồn bán được HRM, cột Tồn tại kho chỉ để xem (đã tự chốt khao-sat-4.5 §5) — cost: "Còn tồn" có thể hiện dòng Tồn tại kho = 0.
E-T2: minor (deferred): ksort vô dụng; thiếu test stock_view chỉ khoá lạ.
E-T2: fix round 1/5 dispatched (phạm vi kho như cũ + mặc định; supplier mảng 500; lỗi tra tồn 500) — FIX_BASE 573667071a.
E-T2: fix round 1/5 (3 addressed, 0 open; 573667071a..d55db03e3f; ERP 171/171)
E-T2: minor (deferred): default nhóm kho chỉ trả khi nhóm có ≥ 1 kho (cũ trả cả nhóm rỗng) ⇒ null = không xem tồn.
E-T2: complete (ERP 4a0b8a60e3..d55db03e3f, review clean)
E-T3: BASE d55db03e3f — dispatch.
E-T3: implementer xong (ERP d9819f8e58 — chỉ productPicker + productPickerJs; hàng lọc 1 dòng 1440/1280; tồn kho khớp SQL; Hết tồn 33/33; NCC 162 khớp) — đang review.
Ruling: "Làm mới" không đặt lại ô Xem tồn (là cài đặt xem, không phải bộ lọc) — cost: 1 dòng nếu user muốn đặt lại.
E-T3: ⚠️ controller kiểm: out_of_stock trong whitelist chung (proxy l.35, dùng cho search + tree-counts); khoá cache gồm sha1(pick_session|legacy đã sắp) ⇒ có supplier. Đạt.
E-T3: minor (deferred): ô từ khoá 120px ở 1280 khi bật Xem tồn; CSS order đổi chỗ lưới nâng cao khi bật NCC; chưa có test tự động hành vi mới.
E-T3: complete (ERP d55db03e3f..d9819f8e58, review clean)
E-T4: implementer xong (ERP 53b0de68c0, 8 file; ERP 171/171; Playwright 5 màn; 2 màn sửa kiểm bằng render view tại chỗ — không có bản ghi e2e_assign sửa được; role tạm 119990 đã xoá) — đang review.
E-T4: ⚠️ 2 màn SỬA (Báo giá DV CSKH, PL HĐ mua TN v2) kiểm bằng render view tại chỗ, không qua route thật (không có bản ghi e2e_assign sửa được) — đưa vào danh sách kiểm Playwright cuối nếu tìm được bản ghi.
E-T4: minor ⇒ chuyển E-T7: hide '#searchServiceProduct' no-op ở create/edit; include chết warranty_repair_requests/form:727.
E-T4: minor (deferred): sspCompatRow lặp searchProductCompatRow; chưa có e2e.
E-T4: complete (ERP 53b0de68c0, review clean)
E-T5: implementer xong (ERP 36b7cd283f, 10 file; Playwright 5 màn; TN mới không mở được (controller thiếu create/edit — 500 sẵn) ⇒ render view tại chỗ) — đang review. ⚠️ thêm hàng NK 2 / TN mới lỗi `unit_coefficient` chỉ có getter — đang truy có phải hồi quy nhánh mình.
E-T6: implementer xong (ERP 8b5bdeedeb; dùng chung sale/device_errors/chooseProductJs; sửa lớp z-index #createDeviceError 9998; Playwright tạo/sửa + Báo giá DV CSKH 3 modal lồng; role tạm 119991 đã xoá) — đang review.
Ruling: popup ở 5 màn đặt hàng + lỗi thiết bị giữ phạm vi mặc định spec §4.2 (chỉ hàng đã xếp catalog, công tắc mở rộng) — đúng thiết kế đã duyệt; dev ít catalog là việc quy đổi chặn go-live — cost: trước go-live, người dùng phải bật công tắc mới thấy hàng chưa xếp.
E-T6: ⚠️ Xử lý YC bảo hành (404 local) — reviewer đọc code: popup + JS của trang render trước modal, guard đúng ⇒ cùng cơ chế trang CSKH đã kiểm. Chấp nhận.
E-T6: minor ⇒ chuyển final fix: toast "Thêm thành công" trước khi getData xong + lỗi getData nuốt im lặng; bấm tên nhanh ⇒ trùng dòng.
E-T6: minor ⇒ E-T7: khối code cũ bị comment ở sale/device_errors/edit.blade.php:122-224.
E-T6: complete (ERP 8b5bdeedeb, review clean)
E-T5: minor ⇒ E-T7: CSS chết #search-product-table ở create/edit/copy 5 màn; markPickerExisting + wrapper onPick chép 5 lần ⇒ đưa thành helper public trong productPickerJs (vd pp.markExisting) và thay 5 chỗ.
E-T5: minor (deferred): root 2 lần bấm rất nhanh hàng khác hãng lọt kiểm (popup cũ cũng vậy); nhóm kho không có trong danh sách ⇒ tiêu đề trống; chưa có spec hồi quy.
E-T5: complete (ERP 36b7cd283f, review clean)
Ruling: lỗi unit_coefficient NK 2 / TN mới có sẵn trên gop_db từ 01/2024 (không phải hồi quy) ⇒ ghi N97, không vá trong 4.5 (quy tắc ngoài luồng) — cost: 2 màn vẫn không thêm hàng tay được tới khi N97 xử lý (như hôm nay).
E-T7: implementer xong (ERP 55412db134, 62 file +118/−2991; php -l 4.128 view; Playwright 18 màn 0 pageerror; báo cáo 6,06 MB → 3,89 MB; role tạm 119992 đã xoá) — đang review.
E-T7: ghi lại (không làm): catalog @json trong searchProductJs còn ~70 trang đọc ⇒ việc riêng; customermanager/show.blade.php vẫn được route customer-care/customer-managers phục vụ (khảo sát ghi nhầm "không render"); createPIBarcode 0 include; sync_products gọi availableGroup không tồn tại (lỗi sẵn).
E-T7: minor (deferred): customermanager/show.blade.php:1409 hide '#searchProductEquivalent' no-op; pp.eachPicked dừng khi 1 dòng ném lỗi (như wrapper cũ); createPIBarcode chết chưa xoá.
E-T7: complete (ERP 55412db134, review clean)
Final review: dispatch (ERP 4a0b8a60e3..55412db134, hrm-api db6f95787..92ea83c5d).
Final review: CHƯA merge — 1 Critical (NCC đi only_ids ⇒ HRM bỏ lọc Đang KD/status ⇒ lộ hàng ngừng KD/đã xoá: THAI SENG 162 vs 21), 1 Important (2 màn SỬA chưa kiểm route thật), 2 minor mới. Minor hoãn: không cái nào bắt buộc; E-T6 minor đã sửa trong E-T7.
Ruling: tách đường NCC — hrm-api thêm `filter_ids[]` (+`filter_ids_set`) CHỈ THU HẸP, giữ scope/catalog/status; LegacyPickerScope trả supplier ở khoá riêng (vd `filter_ids`), proxy gửi filter_ids thay only_ids; only_ids giữ cho danh sách khoá HĐ/kho/giữ hàng — cost: thêm 1 tham số API.
Ruling: kiểm route thật 2 màn sửa bằng bản ghi THỬ tạo qua UI (role tạm), xoá khi xong — cost: không.
Final: fix wave dispatched.
Final: fix wave (hrm-api 92ea83c5d..3c6664ee6 filter_ids; ERP 55412db134..a53c1ad006): NCC chỉ thu hẹp (THAI SENG 162 ⇒ 0 mặc định / 93 khi bật chưa xếp catalog — khớp SQL), 2 màn SỬA kiểm route thật (bản ghi thử 12227 + annex2 3 đã xoá; role tạm 120010 đã xoá), 2 minor. Re-review: 3/3 addressed, 0 breakage.
Final: minor (deferred): NCC + khoá HĐ ⇒ giao tập dưới phạm vi only_ids (hàng ngừng KD trong HĐ của NCC vẫn hiện).
Merge LOCAL: hrm-api feat/chuyen-doi-hang-hoa f5bf2e01c · ERP feat/2d1-erp-khong-loi 370fdd64de — CHƯA push. Sau merge: ERP 176/176, picker HRM 37/37.
Push 14/10: hrm-api f5bf2e01c · ERP 370fdd64de (user chạy bằng !).

## Bước 4.3b (Phần F) — BASE hrm-api f5bf2e01c, hrm-client 094412b40 (nhánh feat/cdhh-p4-3b-cskh ở cả 2) — user "làm" 14/10
Brief/report: sdd-43b/. Căn cứ: khao-sat-4.3b.md §4–§5 + spec §3–§4.
Pre-flight:
| Cặp | Bên làm ⇒ bên dùng | Kết quả |
|---|---|---|
| F-T1 ⇒ F-T2..F-T5 | `V2ProductPickerModal` (props/emit) + prop panel `serviceQuotationOnly`/`scope` ⇒ 8 chỗ gọi | khớp (chốt API ở F-T1, các task sau đọc file) |
| F-T2..F-T5 ⇒ F-T6 | gỡ ProductSearchModal/GroupSearchModal + route BE chỉ sau khi hết chỗ dùng | Ruling: F-T6 chạy cuối, git grep 0 — cost: không |
| F-T2 ↔ F-T3..F-T5 | chung 1 Nuxt dev 3031 + Playwright MCP 1 trình duyệt | Ruling: chạy TUẦN TỰ F-T2…F-T5 (memory e2e-phai-chay-workers-1; MCP dùng chung) — cost: chậm hơn |
F-T1: implementer xong (client 28c06ae81: Panel + V2ProductPickerModal; Playwright đo đủ) — đang review.
Ruling: nút Đóng = tertiary theo button-convention (brief ghi secondary là nhầm) — cost: 1 chữ.
Ruling: `items` bỏ qua `scope` (chỉ hàng Đang KD) — 4.3b không chỗ nào dùng V2ProductPickerModal với scope=all (Tra cứu tồn dùng ô tìm, không popup) ⇒ ghi lại, không sửa — cost: nếu sau này có màn modal scope=all thì cần sửa BE.
F-T1: minor ⇒ F-T6: footer V2ProductPickerModal dùng gap:12px thay `mr-2 mb-2` (quy tắc CLAUDE.md); multiple=false không có item ⇒ im lặng (báo toast); prop scope thiếu validator.
F-T1: minor (deferred): màu cứng trong style scoped; prop title/icon thừa cạnh slot #header; catch nuốt lỗi (toast do interceptor).
F-T1: complete (client 094412b40..28c06ae81, review clean)
F-T2: implementer xong (client cd6730112; A qua luồng thật, B gọi method form; role tạm 120026 đã xoá) — đang review.
F-T2: ⚠️ BE xử lý machine_id / include_service_shared / service_quotation_only — đã có PHPUnit từ 4.2/4.4 (ProductPickerSearchTest) + request đo được trong Playwright. Đạt.
F-T2: minor (deferred): 4 minor ở task-2-review.md.
F-T2: complete (client 28c06ae81..cd6730112, review clean)
F-T3: implementer xong (client c42361c6d; tạo + sửa 2924 + xử lý YC BH; role 120027 + YC BH 6478/9249 thử đã xoá) — đang review.
Ruling: Vật tư thay thế cần popup không cột giá — V2ProductPickerModal ép null ⇒ 1; sửa ở F-T6 (modal/panel nhận priceTypeId null) + truyền null ở màn lỗi thiết bị — cost: tới F-T6 cột giá vẫn hiện.
Ruling: cột "Nhóm" ở bảng thiết bị lỗi giữ group_name cũ (dev 0 hàng có Loại SP) — đổi sang Loại SP gắn với việc quy đổi phân loại — cost: còn hiển thị phân loại cũ.
Ruling: phạm vi Đang KD (không scope=all) cho "Áp dụng cho thiết bị" / "Hàng tương đương" — khớp ERP E-T4/E-T6 — HỎI LẠI user ở báo cáo cuối (máy KH cũ có thể không còn KD) — cost: không chọn được máy đã ngừng KD.
F-T3: ⚠️ controller: Item = Row + units… (A3) có name/code/model_name; "Đã có" chỉ là nhãn, vẫn chọn được (spec §3) ⇒ đạt.
F-T3: minor (deferred): fallback item||row khi items rỗng; gọi items 2 lần khi bấm tên (tooltip + chọn); chưa có e2e; +2 ở task-3-review.md.
F-T3: complete (client cd6730112..c42361c6d, review clean)
F-T4: implementer xong (api 82e21f4f4 + client c0040bf14; PHPUnit 2/18; Playwright gói 1 + dữ liệu giả; bản ghi thử 228 + lịch sử 7860 + role 120028 đã xoá) — đang review.
Ruling: chấp nhận BE tự điền pivot group_id (NOT NULL) từ products.group_id khi hàng mới chọn qua popup không có nhóm — thiếu là 422 — cost: pivot vẫn ghi nhóm cũ.
F-T4: ⚠️ DB import ở ServiceRequest — PHPUnit test 2 qua ⇒ có. Đạt.
F-T4: minor ⇒ F-T6: hàng không có group_id cũ ⇒ 422 im lặng ở form gói bảo dưỡng ⇒ hiện lỗi rõ (dev hiện 0/45.890 hàng thiếu nhóm).
F-T4: minor (deferred): thiếu test hàng không nhóm; bỏ rồi thêm lại lấy nhóm từ products; test phụ thuộc dữ liệu dev; lịch sử gói vẫn gom theo nhóm cũ.
F-T4: complete (api f5bf2e01c..82e21f4f4, client c42361c6d..c0040bf14, review clean)
User Q4 (14/10): chỗ chọn MÁY/THIẾT BỊ ⇒ toàn bộ hàng; vật tư/hàng bán giữ Đang KD; sửa ERP đồng bộ (option user chọn ghi rõ phạm vi ERP).
Ruling: thêm F-T7 (hrm-api `items` nhận scope=all + client truyền scope='all' ở C-thiết bị, D, E) — chạy TRƯỚC F-T5; F-T5 truyền scope='all'; F-T8 (ERP đồng bộ, nhánh con mới từ feat/2d1-erp-khong-loi) chạy sau F-T6 — cost: thêm 2 task.
F-T7: implementer xong (api 71becd413, client b3bc604b9; picker 33/164; Playwright gói 1 / lỗi thiết bị / xử lý YC BH; role 120055 + YC 6479/9250 đã xoá) — đang review.
F-T7: minor (deferred): thiếu dòng trống giữa test; test dựa dữ liệu dev (có transaction); thiếu test scope=all + quyền giá vốn; thiếu test 422 scope sai.
F-T7: complete (api 82e21f4f4..71becd413, client c0040bf14..b3bc604b9, review clean)
F-T8: implementer xong (ERP nhánh feat/cdhh-p4-3b-erp-dong-bo f10d1c1c6b từ 370fdd64de; ERP 177/177; Playwright 16/16 ca 6 màn; role 120056 đã xoá) — đang review. Bảo hành hãng (firm_warranty_*) không đổi — hỏi user ở báo cáo cuối.
F-T8: ⚠️ JS/adapter không có test tự động (ERP không có e2e) — Playwright 16/16 ca đã đo; chấp nhận.
F-T8: minor (deferred): 5 minor ở task-8-review.md.
F-T8: complete (ERP 370fdd64de..f10d1c1c6b, review clean)
F-T5: implementer xong (client cd6c05f18; 3 chỗ, scope=all, chọn 1; POST chặn không ghi; role ERP 120057 đã xoá) — đang review. MCP Playwright treo (tab cũ beforeunload) ⇒ dùng headless riêng.
F-T5: ⚠️ z-index + hàng ngừng KD chỉ có số đo Playwright của implementer (đã ghi số: 1035/1040/1041, sp 21666/15192) — chấp nhận.
F-T5: minor (deferred): JSDoc lệch chỗ ở AddExternalEquipmentModal ~l.222; chưa có e2e. (aria-hidden + gỡ ProductSearchModal ⇒ F-T6.)
F-T5: complete (client b3bc604b9..cd6c05f18, review clean)
F-T6: implementer xong (client 9e47fb88b + 469bc53d0, api 646436d34; gỡ 2 modal + 4 endpoint (giữ product-catalogs — 2 màn còn gọi); 1 search khi mở; items đệm theo id; priceTypeId null; câu trống theo chế độ; mr-2 mb-2; blur trước đóng) — đang review.
Ruling: ô tìm Tra cứu tồn công ty ⇒ scope=all (toàn bộ hàng) — màn tra cứu, theo nguyên tắc user chốt Q2 bước 4.4 (báo cáo chọn toàn bộ hàng) — cost: danh sách tìm dài hơn.
F-T6: review — Spec ❌ mục 6 một phần: emptyText khi đã lọc rơi vào câu "chưa xếp catalog" (Important). ⚠️ aria-hidden chỉ đo DOM. 4 minor.
F-T6: fix round 1/5 dispatched (emptyText + Tra cứu tồn scope=all + thử headed aria) — FIX_BASE 469bc53d0.
F-T6: fix round 1 xong (client c15027c0d) — re-review + final review song song.
F-T6: fix round 1/5 (2 addressed, 0 open; client 469bc53d0..c15027c0d). ⚠️ aria-hidden: trình duyệt headed cũng không in cảnh báo — chỉ chứng minh qua DOM (focus ra ngoài modal) — cần kiểm tay Chrome DevTools.
F-T6: minor (deferred): 4 minor ở task-6-review.md; câu trống chế độ dịch vụ hiện chậm vài giây (chờ tree-counts).
F-T6: complete (client cd6c05f18..c15027c0d, api 71becd413..646436d34, review clean sau fix 1)
Final review: With fixes — 0 Critical, 2 Important: (1) scope=all trả cả hàng status 0 (ERP coi status 0 = đã xoá; deleted_at bị ERP bỏ qua — 175 hàng đang bán có deleted_at) ở chỗ chọn máy + Tra cứu tồn + ERP F-T8; (2) gói bảo dưỡng không lưu được máy tạo ở HRM (service_has_products.group_id NOT NULL, hàng HRM không có nhóm cũ ⇒ 422).
Ruling: (1) thêm scope `all_active` = toàn bộ hàng trừ products.status=0 (như popup cũ status≠0; KHÔNG lọc deleted_at theo quy ước ERP) cho chỗ chọn máy HRM + ERP + Tra cứu tồn; báo cáo 4.4 giữ `all` (include_deleted cũ) — cost: thêm 1 giá trị scope.
User chốt (2) 14/10: thay group_id trong bảng nối gói bảo dưỡng bằng id Loại sản phẩm; user sẽ gửi dữ liệu mapping nhóm cũ → loại SP ⇒ TÁCH VIỆC RIÊNG (migration + chuyển dữ liệu + ERP đọc) — khảo sát + xin "làm" sau khi có mapping; chặn go-live. Ghi N100.
Final: fix wave dispatched (all_active + JSDoc AddExternalEquipmentModal).
Final: fix wave (api 483e0d2f0, client 3eb27434a, ERP 254137fb4f — scope all_active cho chỗ chọn máy + Tra cứu tồn; báo cáo 4.4 giữ all). Re-review: tất cả addressed, 0 breakage. Minor: comment đầu searchServiceProductJs còn ghi 'all'.
Merge LOCAL: hrm-api feat/chuyen-doi-hang-hoa 3b7dd0f1a · hrm-client e3377eb7e · ERP feat/2d1-erp-khong-loi d7f15cfcca — CHƯA push. Sau merge: ERP 178/178, picker HRM 41 + ServiceAppliedProductType 2/2.
Treo: N100 (gói bảo dưỡng group_id → Loại SP, chờ mapping user — chặn go-live); câu hỏi Bảo hành hãng (firm_warranty_*) có cần chọn toàn bộ hàng; kiểm tay aria-hidden; N99.
14/10 sau merge 4.3b: user báo "chọn Thiết bị cần bảo dưỡng báo không có quyền" ⇒ route assign/customers/{id}/equipment gác erpPermission "Xem khách hàng" (có sẵn, không do 4.3b); e2e_assign (1180) 0 vai trò. Theo yêu cầu user: tạo role tạm 120113 `UAT_43B_ARIA_TMP` (guard web, quyền 100057 Xem khách hàng, công ty 1) gán 1180 — GIỮ để user kiểm aria-hidden; gỡ khi user báo xong. Gọi thử endpoint ⇒ 200.
N101 (Bảo hành hãng) ghi ngoài luồng; N100 mapping = task riêng sau (user 14/10).
User 14/10: màn YC thông tin BH-SC bên HRM đang dev — user tự xử lý sau; ERP chạy được là đạt. Role tạm 120113 ĐÃ GỠ (0/0/0). Kiểm tay aria-hidden HRM: để user làm khi màn HRM xong.
Push 14/10: hrm-api 3b7dd0f1a · hrm-client e3377eb7e · ERP d7f15cfcca (user chạy bằng !).
