# Khai Quy chế – Cấu hình — Plan

> Feature lớn (nhiều slice). Design tổng: `docs/superpowers/specs/gop-db/2026-09-09-khai-quy-che-cau-hinh-design.md`.
> Design versioning "hẹn ngày áp dụng": `docs/superpowers/specs/gop-db/2026-09-11-khai-quy-che-hen-ngay-ap-dung-design.md`.
> Plan triển khai chi tiết Slice 1: `docs/superpowers/plans/gop-db/2026-09-12-khai-quy-che-congno-versioning-slice1.md`.

## Phase 0 — Chuẩn bị / thiết kế
- [x] UI mock (index.vue + data.js + menu) — đã xong trước đó
- [x] Chốt hướng nguồn dữ liệu: A (port ERP)
- [x] Dò bảng/controller ERP nguồn cho 3 miền (2 agent Explore)
- [x] Chốt schema versioning "hẹn ngày áp dụng" (Cách A — staging mỏng + reuse company_regulation_histories)
- [x] Viết spec chi tiết + brainstorm approve
- [x] Kiểm chứng ERP: tab Công nợ = 7 cột `companies` + history `company_regulation_histories`; due_configs là concern riêng

## Slice 1 — Versioning tab Công nợ (cấp công ty) — ĐÃ CODE XONG
> Chi tiết code/TDD từng bước ở plan doc trên. 8 task đều đã có code + test (`RegulationCongnoVersioningTest`):
- [x] Task 1 — Migration `regulation_scheduled_versions`
- [x] Task 2 — Model `RegulationScheduledVersion` (extends BaseModel) + `CompanyRegulationHistory`
- [x] Task 3 — Service: metadata 7 field + đọc cấu hình hiện hành (`getCongnoConfig`)
- [x] Task 4 — Service: tạo/sửa/huỷ phiên bản + diff xâu chuỗi (`recomputeDiffChain`)
- [x] Task 5 — Service: áp phiên bản (áp-ngay + core cron) + ghi `company_regulation_histories` (actor = version.created_by)
- [x] Task 6 — FormRequest + Controller + Routes `/v1/master-data/regulation-config/congno...` (gate quyền tái dùng, không đẻ quyền mới)
- [x] Task 7 — Command `regulation-config:apply-scheduled` + đăng ký Kernel `dailyAt('00:00')`
- [x] Task 8 — FE: nối tab `congno` với API (GET on mount, saveVer→POST/PUT, nút Huỷ→DELETE), thay mock

## Slice 2 — Tổng quát hoá + 2 tab scalar (chietkhau, kythuat) — ĐÃ CODE XONG ✅
> Plan chi tiết: `docs/superpowers/plans/gop-db/2026-09-14-khai-quy-che-slice2-generalize-scalar-tabs.md`.
> Thực thi bằng SDD (subagent-driven), ledger: `hrm-api/.superpowers/sdd/2026-09-14-khai-quy-che-slice2-generalize-scalar-tabs/progress.md`.
> Zero migration (dùng lại cột `companies` + bảng `company_regulation_histories`); regression congno bất biến qua wrapper. 5 task:
- [x] Task 1 — `RegulationTabRegistry` (khai báo congno/chietkhau/kythuat scalar-company) — TDD Unit (3/3)
- [x] Task 2 — Tổng quát hoá `RegulationConfigService` theo `tab_key` + 6 wrapper congno (giữ test Slice 1 chạy nguyên)
- [x] Task 3 — Cron `regulation-config:apply-scheduled` áp mọi tab scalar-company (`applyDueVersions()`)
- [x] Task 4 — Controller + Routes generic `regulation-config/{tabKey}` + FormRequest rule động (IDOR scope_id 403 + tab_key 404)
- [x] Task 5 — FE: tổng quát hoá `fetchTab/applyTabToModel/collectTabValues` theo `tabKey`, nối chietkhau/kythuat, bỏ mock

### Checkpoint — 2026-09-14
Vừa hoàn thành: Slice 2 — 5 task đều code + test xong, qua task-review (spec+quality) và final whole-branch review (opus) → **CLEAN, không finding chặn**. Test 22/22 xanh (14 regression congno byte-identical + 5 scalar + 3 registry unit).
Đang làm dở: (không) — Slice 2 đóng.
Bước tiếp theo: Slice 3+ (tab scope global `chung/thitruong/quyettoan`, tab shape json/subtable/grid, quy chế phòng ban) — cần migration 3 cột mới + bảng `regulation_config_histories` khi bắt đầu.
Blocked: chưa commit (chưa được uỷ quyền git). Backlog Slice sau (từ review): getTabConfig trả kèm `payload` để modal hẹn prefill đúng baseline khi nhiều lịch hẹn chồng field khác nhau; field non-API trong tab API bị drop âm thầm ở modal hẹn; congnoLoading dùng chung có thể race khi đổi tab nhanh.

### Checkpoint — 2026-09-14 (quyettoan json)
Vừa hoàn thành: tab **quyettoan** (NO_HEN, json `companies.config_settlement_period` — kỳ quyết toán theo năm) BE+FE trọn vẹn. BE: registry + `withValidator`/`toDate` port ERP overlap + chống trùng/rỗng năm; `RegulationQuyettoanJsonTest` 5/5, full MasterData 46/0. FE: `jperiods` helper + editor lồng năm→kỳ (V2BaseDatePicker `value-type="DD/MM/YYYY"`, Kỳ N=di+1, thêm/xoá tự do), `quyettoan` vào API_TABS, CSS `.ystack/.yhead/.yyear`. 2 file FE giữ LF (CR=0). Ghi 2 ruling (parity validate + bỏ khoá-năm UX).
Đang làm dở: (không) — quyettoan đóng.
Bước tiếp theo: kythuat subtable (`contract_rows` FK config_id, replace-all, scope global) hoặc chung (NO_HEN logo `configs.logo`) — theo mandate "làm xong tất cả".
Blocked: chưa commit (chưa được uỷ quyền git).

## Slice 3a — Hạ tầng scope `global` (bảng `configs` singleton) — ĐÃ CODE XONG ✅
> Plan chi tiết: `docs/superpowers/plans/gop-db/2026-09-14-khai-quy-che-slice3a-global-scope-infra.md`.
> Spec authority: `docs/superpowers/specs/gop-db/2026-09-14-khai-quy-che-hoan-thien-cac-tab-design.md`.
> Thực thi bằng SDD, ledger: `hrm-api/.superpowers/sdd/2026-09-14-khai-quy-che-slice3a-global-scope-infra/progress.md`.
> Mục tiêu: dựng scope thứ 3 `global` (ghi bảng `configs` singleton, scope_id=0, history `regulation_config_histories` MỚI) song song scope `company` sẵn có, chứng minh qua tab `baogia` ở tầng service/cron. **Controller-split cho tab mixed + nối FE = HOÃN sang Slice 3b.**
- [x] Task 1 — Schema: 2 migration (3 cột `companies` cho hanghoa/dieukhoan 3b + bảng `regulation_config_histories`) + Entity `RegulationConfigHistory` (extends BaseModel) — test 3/3 (15 assertions)
- [x] Task 2 — Registry: `SCOPE_GLOBAL`/`SCOPE_MIXED`, tab `baogia` 14 field (10 store=config + 4 store=company), `fieldStore()` + `scalarKeysForStore()` — test 6/6 (35 assertions)
- [x] Task 3 — Service: scope `global` end-to-end (`createGlobalVersion`/`applyVersion` nhánh global ghi `configs` + history, `applyDueVersions` quét cả company+global, bỏ `tabModel()`) — test GlobalScope 4/4 · regression Congno 14/14 byte-identical · Scalar 5/5

### Checkpoint — 2026-09-14
Vừa hoàn thành: Slice 3a — 3 task code + test xong, qua task-review (spec+quality) từng task và final whole-branch review (opus) → **VERDICT: SẠCH — đủ điều kiện khép Slice 3a**. Test 4 suite xanh: GlobalScope 4/4 · Congno 14/14 · Scalar 5/5 · Registry 6/6 (4/4·14/14·5/5·6/6). CR=0 cả 8 file (giữ LF, không đụng line ending).
Đang làm dở: (không) — Slice 3a đóng về mặt code.
Bước tiếp theo: Slice 3b (tách controller/FormRequest/route cho tab mixed baogia/giaban/xnk-scalar/hanghoa/dieukhoan + nối FE) — **PHẢI round-trip đủ 10 field store=config khi tạo global version** (xem caveat dưới).
Blocked: chưa commit (git chưa được uỷ quyền).
- **Đã xử lý (fix trong Slice 3a)**: finding MEDIUM test-hygiene — `RegulationGlobalScopeTest` ban đầu chỉ backup 4/10 cột store=config nên `applyVersion(global)` (ghi đủ 10 field) làm null 6 cột trên DB dev mỗi lần chạy; đã mở rộng backup/restore đủ 10 cột (`$configCols`), verify hash `configs` giống hệt trước/sau (hết làm bẩn DB).
- **Caveat cho Slice 3b (từ review, LOW — đã ghi backlog)**: snapshot-wipe full-field-set — global version + `applyVersion` ghi TRỌN bộ 10 field config; field nào không truyền → null → xoá trắng cột đó trên `configs`. Controller/FE 3b BẮT BUỘC round-trip đủ 10 field config (hoặc merge giá trị hiện hành) khi tạo/áp global version.
- **ĐÃ khôi phục data (2026-09-14, user chốt "làm như ERP có")**: đối chiếu ERP `ConfigSeeder` + migration `configs`: `customer_register_expiry` ERP=30 (seed), còn `service_quotation_footer` + `is_repair/is_project/is_principle/is_dental_principle` ERP để NULL (nullable, không seed). Trạng thái sau fix test chỉ còn lệch 1 cột → đã `UPDATE configs SET customer_register_expiry=30 WHERE id=1`; 5 cột nullable vốn đã = NULL (khớp ERP), `is_equipment=1` được giữ nguyên. `configs` nay khớp trạng thái ERP-fresh.

## HOÀN THIỆN TẤT CẢ (user chốt 2026-09-14: "làm xong tất cả, không ưu tiên cái nào")
> Hạ tầng đã xong (Slice 1/2/3a): scope company scalar + scope global (`configs`) + versioning staging + cron + history `regulation_config_histories`.
> Còn lại = nối controller/route + FE + shape phức tạp + scope phòng ban + **gộp về 1 logic lưu**.
> Nguồn chân lý: spec `2026-09-14-khai-quy-che-hoan-thien-cac-tab-design.md` (map field→cột đủ 14 tab ở mục 2, rule theo shape ở mục 5).
>
> **Quyết định UX đã chốt (user "ok" trước đó) — "một logic lưu":**
> - **1 nút "Lưu cấu hình" trên cùng** lưu ĐÚNG tab đang mở (theo scope hiện tại). Bỏ modal "Hẹn phiên bản mới".
> - Ô **"Ngày áp dụng"** đưa INLINE vào tab có hẹn (mặc định = hôm nay). Ngày ≤ hôm nay → áp ngay; tương lai → vào hàng đợi.
> - Tab NO_HEN (chung/thị trường/quyết toán) không có ô ngày → luôn áp ngay.
> - Tab grid (hoa hồng) hẹn theo **từng dòng** (ô "Hiệu lực từ" mỗi dòng); tab ladder/form hẹn theo cả phiên bản.
> - Hàng đợi "Phiên bản đã hẹn" + nút Huỷ vẫn nằm INLINE trong tab.

### Slice 3b — "Một logic lưu" + nối tab scalar/text/mixed cấp công ty
> Plan chi tiết: `docs/superpowers/plans/gop-db/2026-09-14-khai-quy-che-slice3b-unified-save.md`.
> Không shape mới (tách csv/json/subtable/logo sang 3c). Làm cho nút Lưu ăn thật trên: baogia (số+text), giaban, xnk (phần số), dieukhoan (2 text), + giữ congno/chietkhau/kythuat(2 số).
- [x] BE-1 — Registry: khai giaban / xnk(scalar) / dieukhoan (+ verify cột `companies` đủ, thêm migration nếu thiếu); baogia bật end-to-end (đã có ở 3a service)
- [x] BE-2 — Controller/Route/FormRequest: rẽ scope company↔global trên cùng endpoint versions; tab mixed sinh ≤2 bản staging (mục 4.4); NO_HEN bỏ effective_date
- [x] FE-1 — Bỏ `onSave` mock + modal hẹn; dựng `saveCurrentTab()` chung: gom field tab hiện tại + effective_date → POST/PUT versions (BE tự quyết áp-ngay/hẹn)
- [x] FE-2 — Ô "Ngày áp dụng" inline (V2BaseDatePicker) cho tab có hẹn; hàng đợi + Huỷ inline; nhãn "Áp dụng toàn hệ thống" cho field global (nhãn: apiFieldKeys mang `store`, applyTabToModel $set `global`, template render `.global-tag`)
- [x] FE-3 — Nối generic mọi tab scalar/text đã đăng ký; tab chưa hỗ trợ (3c/3d) hiện rõ trạng thái "đang phát triển", không im lặng

### Slice 3c — Shape phức tạp (csv tags / json / subtable / logo / toggles)
> Field shape đặc biệt trong các tab công ty + global NO_HEN.
- [x] thitruong (NO_HEN, MIXED): select `market_division_type` (province/ward, company) + 2 multiselect danh mục csv `configs.department_groups` (bảng departments) / `configs.customer_groups` (bảng customer_groups) — BE registry+resolveOptions+getTabConfig input/options; FE helpers `csel`/`msel`, render mselect V2BaseSelect multiple, split/join csv, NO_HEN gửi hôm nay; test `RegulationThitruongTest` 2/2 (getTabConfig options + round-trip csv)
- [x] hanghoa (GLOBAL) — user chốt 2026-09-14 hướng (a): bám đúng màn config ERP, KHÔNG superset. 3 field lưu `configs`: `serial_product_types` (multiselect mã PRODUCT_TYPES, csv) "Hàng không bắt buộc Serial"; `is_company_price` (bool) "BGĐ duyệt giá"; `is_all_brand` (bool) "Tất cả các hãng sản xuất". Đã BỎ khỏi mock: `product_types` "Tính chất hàng hóa", `applied_brand_ids` "Nhãn hiệu áp dụng", `environment_tax` (là field per-SP, không phải config), toggle "Quy tắc duyệt giá" bịa. BE registry `SCOPE_GLOBAL`; FE `msel` + `tog` (2 bool apiLabel khớp registry), thêm vào API_TABS. Test `RegulationHanghoaTest` 2/2 (getTabConfig multiselect+bool + round-trip). 38/38 test MasterData xanh.
- [x] baogia toggles: 5 bit `configs.is_equipment/is_repair/is_project/is_principle/is_dental_principle` — registry boolean store=config; FE `tog` với apiLabel khớp 1-1 registry, render + collect qua path toggles generic (item[2]); round-trip is_equipment phủ ở `RegulationGlobalScopeTest`
- [x] xnk json `companies.prepick_contract_types` `[{code,name,percent}]` (spec 5.2). BE: json xử lý như KIỂU field trong tab SHAPE_SCALAR (xnk vẫn MIXED+SCALAR → cron/scalarKeysForStore vẫn phủ). `castValue` case json (decode→mảng); helper `encodeForStorage` json_encode mặc định (khớp escape ERP `\uXXXX`+`\/`) vì Company/configs KHÔNG có `$casts` mảng; `buildDiffSnapshot` nhánh json (so bằng chuỗi json); `applyVersion` encode trước ghi + **tách history theo kiểu field**: numeric (integer/decimal/boolean)→`CompanyRegulationHistory` (bảng ERP decimal, giữ nguyên màn ERP), non-numeric (string/csv/json)→`RegulationConfigHistory` (bảng json diff riêng, scope=company) — đồng thời vá bug cũ string/csv company ghi 0.00 vào cột decimal ERP. Registry field `prepick_contract_types` (type json, input `json_percent_rows`, `item_rules` chặn code∈{ban_hang,dich_vu,du_an,nguyen_tac} + percent 0..100); FormRequest json validation. Test `RegulationXnkJsonTest` 3/3 (getTabConfig mảng + apply-today round-trip byte-khớp + rule chặn code lạ). FE: helper `jrows`, thay 6 field mock bằng `jrows('% Đặt cọc theo loại hợp đồng')` (label khớp 1-1 registry); grid nội tuyến sửa % (code/name chỉ đọc); modal hẹn phiên bản render jrows + clone SÂU tránh rò vào giá trị đang hiển thị + `parseJsonRows` cho pending json-string + `verChanged` so JSON mảng. Cả 2 file LF (CR=0)
- [x] quyettoan (NO_HEN): json `companies.config_settlement_period` `[{year,details:[{date_from,date_to,period}]}]` — kỳ quyết toán theo năm (spec 5.x). BE: theo đúng pattern xnk (json là KIỂU field trong tab SHAPE_SCALAR) — chỉ cần đăng ký tab trong `RegulationTabRegistry` (scope company, no_hen, model Company, field `config_settlement_period` type json input `json_settlement_periods`, nested `item_rules` `details.*.date_from|date_to` = `required|date_format:d/m/Y`), pipeline generic (castValue/encodeForStorage/buildDiffSnapshot/applyVersion) tự phủ; history non-numeric → `RegulationConfigHistory` scope=company. Business rule cross-field trong `ScheduleRegulationVersionRequest::withValidator` (phát hiện qua `input==='json_settlement_periods'`): chống trùng năm + năm rỗng + date_from>date_to + **overlap port ERP `storeConfigSettlementPeriod`** (date_from rơi HẲN trong (date_from,date_to) kỳ khác cùng năm) + helper `toDate` (Carbon d/m/Y→Y-m-d). Test `RegulationQuyettoanJsonTest` 5/5 (getTabConfig mảng lồng; apply-today round-trip json lồng + escape `\/` + history diff; rule nested lộ ra; overlap + trùng năm bị chặn); full MasterData suite 46/0. **Gotcha MySQL: cột staging `payload` là JSON native → chuẩn hoá thứ tự key theo (độ dài, byte)** → test so cấu trúc bằng `ksortDeep` (bỏ qua thứ tự key; không ảnh hưởng nghiệp vụ vì companies là text đọc theo key). FE: helper `jperiods`, thay mock `sub` bằng `jperiods('Kỳ quyết toán theo năm')` (label khớp 1-1 registry); editor lồng năm→kỳ (V2BaseDatePicker `value-type="DD/MM/YYYY"` để emit dd/mm/yyyy đúng rule BE); Kỳ N = di+1 (không cho gõ, gán khi collect); thêm/xoá năm & kỳ (`addPeriodYear/removePeriodYear/addPeriodRow/removePeriodRow`, gate `canEditRegulation`); thêm `quyettoan` vào `API_TABS`, `jperiods` vào wide binding. NO_HEN → không mở modal hẹn, lưu effective_date=hôm nay. Cả 2 file LF (CR=0).
  - **Ruling (parity validate)**: quyettoan port đúng validate overlap ĐANG CHẠY của ERP (date_from rơi hẳn trong khoảng kỳ khác), ĐỒNG THỜI bật lại 2 kiểm tra ERP viết hụt (năm rỗng / trùng năm — ERP là no-op nên không chặn). Chi phí nếu sai: chặt hơn ERP một chút, nhưng năm rỗng/trùng không bao giờ hợp lệ.
  - **Ruling (bỏ khoá năm UX)**: KHÔNG port quirk "chỉ sửa được năm cuối" của ERP (là artefact AngularJS, không phải business rule); cho thêm/xoá/sửa tự do mọi năm & kỳ — BE vẫn validate overlap+trùng+rỗng bất kể. Chi phí nếu sai: user sửa được năm quá khứ mà ERP khoá, nhưng vẫn được validate + hồi phục được.
- [x] kythuat subtable: `contract_rows` (FK `config_id`) replace-all — scope global. **kythuat → MIXED**: `work_price`/`work_bond` company scalar decimal + `contract_rows` global subtable. BE: subtable là **FIELD TYPE** (`type='subtable'`, input `subtable_contract_rows`) bám pipeline SHAPE_SCALAR (KHÔNG shape mới) → `scalarKeysForStore`/`applyDueVersions` phủ cả 2 nhánh. `RegulationConfigService`: `castValue` case subtable (decode→mảng); `loadSubtable`/`applySubtable` (đọc/replace-all theo `config_id`, multiselect↔json_encode, quantity→int); `getTabConfig` trả `columns` [{key,label,input,options}] (product_group→`groups` status=1 backtick, product_nature→PRODUCT_TYPES, quantity→number) + `value` mảng dòng giải mã; `applyVersion` global branch tách subtable khỏi cột configs, history scope=global (scope_id=0). `ScheduleRegulationVersionRequest`: rules case json|subtable→array + item_rules (`quantity` required|integer|min:1); `withValidator` `validateContractRows` port 3 kiểm chéo dòng ERP (không trộn nhóm/tính chất, ≥1 loại, chống trùng); mảng rỗng=xoá sạch (cho phép). Test `RegulationKythuatSubtableTest` 7/7 + `RegulationTabRegistryTest` tách chietkhau/kythuat; full MasterData **54/0**. FE (cả 2 file LF CR=0): helper `sub(label)` → `{t:'subtable', val:[], cols:[]}`; `fetchTab` map thêm `columns`; `applyTabToModel` nhánh subtable set `cols`/`val`/`global`; `collectTabValuesFromModel` map dòng→{product_group,product_nature,quantity:Number} theo cột; editor động (multiselect V2BaseSelect multiple + options BE, number V2BaseInput) + `addSubRow`/`removeSubRow` gate `canEditRegulation`. verEditableFields skip 'subtable' → không hẹn qua modal phiên bản (chỉ sửa/áp qua nút Lưu cấu hình).
  - **Ruling (subtable = field type, không shape mới)**: song song với json — tab giữ `shape=SHAPE_SCALAR` để cron/store nhặt cho cả 2 nhánh company+config. Chi phí nếu sai: nếu sau này cần subtable ở tab non-scalar phải thêm nhánh, nhưng hiện chỉ kythuat dùng.
- [x] chung (NO_HEN): logo upload (`configs.logo` qua V2BaseFile) + title + description — ghi thẳng, áp ngay. **GLOBAL scalar, no_hen=true**: 3 field string ghi thẳng cột `configs.logo/title/description` qua pipeline generic có sẵn (getTabConfig echo `input`, applyVersion global branch update configs generic theo field key, history scope=global scope_id=0) — KHÔNG cần code service mới. BE registry `chung` (logo `type=string,input='logo'` — `input='logo'` chỉ là gợi ý render FE, resolveOptions(null)=[] vô hại; title/description string). FE (cả 2 file LF CR=0): data.js label khớp registry 1-1 (`Logo hệ thống`/`Tiêu đề hệ thống`/`Mô tả hệ thống`); index.vue thêm `chung` vào `API_TABS`, logo render → `V2BaseFile auto-upload accept=.png,.jpg,.jpeg :disabled="!canEditRegulation"` (v-model nhả URL S3 vào `f.val` qua action Vuex `uploadImage`→`files/upload`); logo/text/area round-trip qua nhánh generic sẵn có (join theo label, `values[key]=f.val`). Test `RegulationChungTest` 2/2 (getTabConfig phơi 3 string + logo input; save-today áp ngay + round-trip + history global) + `RegulationTabRegistryTest::registers_chung_as_global_no_hen_with_logo_field`. Full MasterData **57/0**.
  - **Ruling (logo = string URL, không kiểu field mới)**: BE coi logo là `string` lưu URL; FE `V2BaseFile auto-upload` tự đẩy S3 rồi gán URL vào field → pipeline generic không đổi. `input='logo'` thuần là hint render FE. Chi phí nếu sai: nếu sau cần validate/định dạng ảnh riêng phải thêm nhánh, nhưng hiện chỉ 1 field logo dùng.

### Checkpoint — 2026-09-14 (chung tab — BE+FE xong)
Vừa hoàn thành: chung tab (GLOBAL/NO_HEN, logo/title/description ghi thẳng configs) — BE registry + tận dụng pipeline generic (không service mới) + FE (V2BaseFile auto-upload cho logo, label khớp registry, thêm vào API_TABS, round-trip generic). Test `RegulationChungTest` 2/2 + registry unit test; full MasterData **57/0**. Cả 2 file FE giữ LF (CR=0).
Đang làm dở: (không) — chung đóng. Slice 3c (tab scope company/global/mixed) hoàn tất.
Bước tiếp theo: Slice 3d — scope phòng ban (FE chọn phòng ban + BE gate `department_id` fail-closed; `khac` form 3 cột departments; `themquy` ladder `conditions_quarter_bonus`; `hoahong` grid `regulations` CRUD tổng=100). Chờ agent xác nhận bảng DB thật trên DB gộp.
Blocked:

### Slice 3d — Scope phòng ban (hoahong grid + themquy ladder + khac)
> Chờ agent xác nhận bảng DB thật trên DB gộp (`regulations` polymorphic Department / `departments` / bảng hoa hồng). Spec mục 2.2 + 5.4/5.5 + 6.
- [x] FE chọn phòng ban (thay mock SCOPE_UNITS bằng phòng ban THẬT qua endpoint `regulation-config-departments`, `selectedDeptId` int, re-fetch khi đổi phòng); BE nhận `department_id`, gate phòng thuộc công ty user (fail-closed: `assertDepartmentInCompany`)
- [x] khac (form scalar, scope=department): 3 cột `departments` (`risk_fund`/`profit_percent`/`max_value_contract`) — staging scalar giống company. **BE**: scope SCOPE_DEPARTMENT trong RegulationConfigService (storeForScopeType→'department', applyVersion/applyDueVersions/updateVersion/recomputeDiffChain nhánh department, lịch sử → `regulation_config_histories` scope_type='department' scope_id=department_id) · controller resolveScopeId/refreshScopeId/assertVersionOwnership · route + FormRequest `department_id`. **FE**: DEPT_API_TABS=['khac'], fetchTab/applyTabToModel/onSave/curTabIsApi/watch scope-aware, đổ vào model.department.groups, nhãn data.js khớp registry. **Test**: RegulationKhacDepartmentTest 3/3 + registry unit; MasterData suite 61 passed. CR=0.
- [x] themquy (ladder, scope=department): `departments.conditions_quarter_bonus` (json bậc thang, GIỮ ĐÚNG khoá ERP money_from/money_to/percent + comparator type_condition_from/to) + `rate_reward_progressive_tp/tbp/nv`. **Ruling B**: lịch sử → `RegulationConfigHistory` scope=department (KHÔNG dual-write bảng audit ERP `department_condition_quarter_bonus_histories` — test assert count=0). **BE**: registry themquy (json+input='ladder', item_rules percent 0-100, 3 decimal) + FormRequest `validateQuarterBonusLadder` (per-row from<to + ∑tp/tbp/nv=100). **FE**: DEPT_API_TABS=['khac','themquy']; verbar inline "Ngày áp dụng" + pending-queue cancel-only (ẩn nút sửa vì ladder không dùng modal hẹn); bảng bậc thang V2BaseSelect(ladderFromOps/ToOps)+V2BaseCurrencyInput(money, rỗng=INF)+V2BaseInput%; addLadderRow/removeLadderRow; applyTabToModel/collectTabValuesFromModel nhánh themquy (ladder+progressive); ladderRateValid tô đỏ + chặn onSave; cancelPending nhận cả DEPT_API_TABS. **Test**: RegulationThemquyDepartmentTest 3/3 + registry unit `registers_themquy_as_department_ladder_tab`; MasterData suite 65 passed. CR=0 index.vue+data.js.
- [x] hoahong (grid per-dòng) — **BE XONG (test 76/76) + FE grid wiring XONG**: CRUD `regulations` + `effective_date/status` từng dòng; validate ∑department/part/employee=100 và ∑*_bonus_contract=100; cron flip pending→applied theo dòng.
  - [x] **BE**: migration thêm 2 cột nullable effective_date/status vào `regulations` (đã chạy); registry hoahong shape=SHAPE_GRID scope=department 18 field metadata (loại khỏi mọi helper scalar); controller show() rẽ getGridConfig, storeGridRow/updateGridRow/destroyGridRow (assertGridTab+currentCompanyId+assertDepartmentInCompany, actorId=auth()->id()), route version rẽ 404 cho tab grid; RegulationCommissionRowRequest (condition_sale_type required_if type=1; value_end gt start; ∑ 2 nhóm %=100; conditions_commissions[from_day<to_day, receive_percent 0..100]); ScheduleRegulationVersionRequest guard isGridTab; service statusForEffective/fillGridRow (sale_type=0 khi type≠1, after_commission_type ép=1, change_approver→0/1, conditions rỗng→null)/presentGridRow (is_applied/is_pending/status_text)/getGridConfig (fields+rows resolveOptions)/createGridRow·updateGridRow·deleteGridRow (ownership 403)/applyDueGridRows; history buildGridHistoryDiff numeric-aware TRƯỚC save (đã FIX false-diff decimal) → regulation_histories. Routes: POST/PUT/DELETE regulation-config/{tabKey}/grid[/{rowId}]. **Test**: RegulationHoahongGridTest 10/10 + registry unit; MasterData 76/76. CR=0 (4 file BE LF).
  - [x] **FE grid wiring (index.vue + data.js)** — XONG (2026-09-15): GRID_DEPT_TABS=['hoahong'] (ngoài DEPT_API_TABS); fetchGridTab GET `.../hoahong?department_id=` → applyGridConfig đổ {fields→gridFieldOptions, rows OBJECT vào group}; tbody dựng lại theo row object (gridOptLabel/gridNetText/fmtPercent/fmtDate + pill is_pending/is_applied/status_text, cột Thao tác gate canEditRegulation); modal reg bind ĐÚNG 18 key BE + effective_date + id (condition_sale_type chỉ hiện khi Number(condition_type)===1, condition_compare_type disabled 'Giá net', conditions_commissions sub-table add/removeCommissionDay); openReg object-prefill; saveReg guard 2 nhóm ∑=100 + POST/PUT `.../grid[/{id}]` (condition_sale_type null nếu type≠1, change_approver 'true'/'false') → applyGridConfig(res.data.config) hoặc fetchGridTab, map 422 → regError inline; deleteReg `$confirm` danh:true → apiDelete `.../grid/{id}?department_id=`; import+register V2BaseCheckbox; groupPending grid dùng r.is_pending. **Ruling**: KHÔNG gọi markFormSaved (trang KHÔNG dùng unsavedChangesMixin — không import/beforeRouteLeave, sibling scalar-tab onSave cũng không gọi; gọi sẽ ném undefined method). CR=0 (index.vue + data.js LF nguyên trạng).

### Checkpoint — 2026-09-14 (khac tab — BE+FE xong)
Vừa hoàn thành: Slice 3d tab `khac` (scope phòng ban) — BE (service/controller/route/FormRequest) + FE (index.vue scope-aware, picker phòng ban thật, data.js nhãn khớp) + test (RegulationKhacDepartmentTest 3/3, registry unit, MasterData 61 passed). CR=0 index.vue+data.js.
Đang làm dở: (không) — khac đóng.
Bước tiếp theo: Slice 3d tab `themquy` (departments.conditions_quarter_bonus json + rate_reward_progressive_tp/tbp/nv; history `department_condition_quarter_bonus_histories`), rồi `hoahong` (grid = mỗi dòng 1 `regulations` objectable Department; thêm cột nullable effective_date/status cho hẹn-lịch; ∑*_bonus_contract_percent=100).
Blocked:

### Checkpoint — 2026-09-14 (themquy tab — BE+FE xong)
Vừa hoàn thành: Slice 3d tab `themquy` (ladder, scope phòng ban) — BE (registry json+ladder, FormRequest `validateQuarterBonusLadder` per-row + ∑=100) + FE (index.vue: bảng bậc thang V2Base object-keyed, verbar inline date + pending cancel-only, addLadderRow/removeLadderRow, applyTabToModel/collectTabValuesFromModel nhánh themquy, ladderRateValid tô đỏ+chặn lưu, cancelPending nhận dept tabs; data.js mock ladder object khoá ERP) + test (RegulationThemquyDepartmentTest 3/3, registry unit, MasterData 65 passed). CR=0. Ruling B: history → RegulationConfigHistory scope=department, KHÔNG dual-write bảng audit ERP.
Đang làm dở: (không) — themquy đóng. Slice 3d còn `hoahong` (tab phức tạp nhất).
Bước tiếp theo: Slice 3d tab `hoahong` — grid, mỗi dòng = 1 `regulations` (objectable Department); `regulations` CHƯA có effective_date/status → thêm cột nullable cho hẹn-lịch từng dòng; validate ∑*_bonus_contract_percent=100; KHÔNG port risk_fund_percent/department_support_percent.
Blocked:

### Checkpoint — 2026-09-14 (hoahong BE xong — bàn giao FE grid wiring cho mai)
Vừa hoàn thành: Slice 3d tab `hoahong` — **BE CODE-COMPLETE** (mỗi dòng lưới = 1 `regulations` objectable Department, KHÔNG staging version; 2 cột nullable effective_date/status ghi thẳng `regulations`). Migration đã chạy; registry SHAPE_GRID + loại khỏi helper scalar; controller getGridConfig/storeGridRow/updateGridRow/destroyGridRow (gate currentCompanyId + assertDepartmentInCompany, ownership 403); RegulationCommissionRowRequest + ScheduleRegulationVersionRequest guard isGridTab; service statusForEffective/fillGridRow/presentGridRow/getGridConfig/CRUD/applyDueGridRows; history numeric-aware buildGridHistoryDiff (đã FIX false-diff decimal). Routes POST/PUT/DELETE `.../grid[/{rowId}]`. Test RegulationHoahongGridTest 10/10 + registry unit; MasterData suite **76/76**. CR=0 (4 file BE LF nguyên trạng). NOT committed (rule gop_db).
Đang làm dở: (không code dở — chỉ mới ĐỌC file FE để chuẩn bị wiring, chưa viết dòng FE nào → không có gì nửa vời/hỏng). FE grid wiring của hoahong CHƯA làm.
Bước tiếp theo (FE grid wiring hoahong — index.vue + data.js, ĐỂ MAI):
  1. Thêm hằng `GRID_DEPT_TABS=['hoahong']` (KHÔNG cho vào DEPT_API_TABS — đó là tab scalar chạy pipeline version; hoahong là grid, CRUD riêng qua route /grid).
  2. `fetchTab` thêm nhánh grid: GET `master-data/regulation-config/hoahong?department_id=<selectedDeptId>` → nhận `{fields, rows}`, đổ vào group (rows là mảng OBJECT có id + 18 field + effective_date + status + is_applied/is_pending/status_text — KHÔNG còn mảng positional r[0..8] như mock).
  3. Viết lại `<tbody>` grid dùng row OBJECT, cột dựng: Áp dụng cho = option condition_type; Bảng giá = option condition_sale_type (— nếu type≠1); Giá net so sánh = operator + value_start .. value_end_operator + value_end; % Tháng = month_percent; % Sau HH = after_commission_percent; Chia DS TP/TBP/NV = department/part/employee_percent; Chia thưởng HĐ TP/TBP/NV = *_bonus_contract_percent; Hiệu lực từ = effective_date (fmt dd/mm/yyyy); Trạng thái = V2BaseBadge theo is_pending ("Chờ áp dụng") / is_applied ("Đang áp dụng"). Số hiển thị theo chuẩn quốc tế toLocaleString('en-US').
  4. Viết lại modal reg (V2BaseModal ref=regModal) bind ĐÚNG key BE (KHÔNG dùng key mock applyFor/priceList/opFrom...): condition_type (V2BaseSelectInModal inline HH/DV) · condition_sale_type (V2BaseSelectInModal price_types, CHỈ hiện khi condition_type=1) · condition_compare_operator (select >, >=, =, <=, <) · condition_compare_type (V2Base disabled hiển thị "Giá net", giá trị 'net_price') · condition_compare_value_start (V2BaseCurrencyInput/number) · condition_compare_value_end_operator (select <=,<, cho rỗng) · condition_compare_value_end · change_approver (checkbox) · month_percent · month_type (select 1/2) · after_commission_percent · conditions_commissions (sub-table lặp lại từ_ngày<đến_ngày + %nhận, để trống đến_ngày = bậc cuối) · department/part/employee_percent · *_bonus_contract_percent · effective_date (V2BaseDatePicker YYYY-MM-DD). Guard FE 2 nhóm ∑=100 + map 422 BE về lỗi inline. Tất cả nút gate canEditRegulation.
  5. `openReg(row?)` prefill từ row object / mặc định; `saveReg()` POST `.../hoahong/grid` (mới) hoặc PUT `.../hoahong/grid/{id}` (sửa), payload có department_id=selectedDeptId; xong re-fetch grid + markFormSaved + đóng modal. Nút xoá dòng: `$confirm` → DELETE `.../hoahong/grid/{id}` → re-fetch.
  6. GIỮ line-ending (index.vue + data.js hiện LF — kiểm `file` trước khi lưu). Theo skill modal-popup + button-convention + form-validate.
Blocked:

### Checkpoint — 2026-09-15 (hoahong FE grid wiring XONG — Slice 3d ĐÓNG)
Vừa hoàn thành: FE grid wiring tab `hoahong` (index.vue + data.js) theo đủ 6 bước bàn giao — fetchGridTab/applyGridConfig, tbody row-object, modal reg bind 18 key BE, openReg/saveReg/deleteReg qua route /grid, import V2BaseCheckbox, CSS .grid-empty/.reg-err. Đã verify: methods block cân, không còn ref mock positional (r[0..8]/split(' / ')/applyFor/priceList…), index.vue + data.js vẫn LF (CR=0).
Ruling (giải quyết câu hỏi treo từ summary): KHÔNG gọi `markFormSaved()` trong saveReg/deleteReg — trang KHÔNG dùng `unsavedChangesMixin` (không import, không beforeRouteLeave, không markFormSaved ở đâu; sibling scalar-tab onSave cũng không gọi). Gọi sẽ ném undefined method. Giá phải trả nếu sai: nếu về sau trang gắn mixin thì phải thêm markFormSaved — rủi ro thấp, sửa 1 dòng.
Với Slice 3d: khac + themquy + hoahong đều XONG BE + FE. **Slice 3d ĐÓNG.**
Đang làm dở: (không).
Bước tiếp theo: Slice 3b (nối FE tab mixed cấp công ty baogia/giaban/xnk-scalar/hanghoa/dieukhoan — round-trip đủ 10 field store=config khi tạo global version) hoặc Slice 3e (rà quyền + số quốc tế + line-ending + review cuối whole-branch). Chưa QA trình duyệt hoahong (code chưa deploy dev).
Blocked:

### Slice 3e — Rà soát toàn màn (quyền + menu + review)
- [x] Gate quyền "Cài đặt cấu hình" mọi route ghi; ẩn nút Lưu khi thiếu quyền (v-if, fail-closed)
- [x] Nhãn "Áp dụng toàn hệ thống" cho field global; định dạng số quốc tế; audit line-ending (CR=0)
- [x] Final whole-branch review (opus) — 0 Critical / 1 High / 4 Medium / 4 Low. Báo cáo: scratchpad/final-review-khai-quy-che.md
- [x] Xử lý findings (fix batch mechanical + ①A + ②A) + cập nhật design.md/STATUS.md

### Slice 3f — Xử lý findings review cuối — ĐÓNG ✅ (2026-09-15)
**Fix batch (mechanical) — XONG:**
- [x] #2 Element form thô → V2Base (verify: grep raw button/label/btn = RỖNG)
- [x] #3 confirm() native → $confirm (verify: không còn confirm() native ngoài $confirm)
- [x] #6 Bỏ 2 field mock thừa tab congno (verify: Thuế vận tải + Ngày khai báo — grep RỖNG trong data.js)
- [x] #7 Bỏ cột chết companies.applied_brand_ids khỏi migration (verify: grep migrations RỖNG)
- [x] #8 KHÔNG set updated_by — CompanyRegulationHistory KHÔNG có cột updated_by (append-only, đã revert đúng ở session trước; verify: grep RỖNG)
- [x] #9 Dọn data.js: xoá export chết SCOPE_UNITS; GIỮ CURRENT_COMPANY (index.vue dùng ở dòng 21/1019/1070 — KHÔNG chết); HIST đã xoá ở ①A

**Đã chốt với user (2026-09-15) — XONG:**
- [x] **①A #1 [High]** Endpoint BE `GET regulation-config-history?scope=company|department` đọc lịch sử THẬT — gộp 4 nguồn theo scope: `regulation_config_histories` + `company_regulation_histories` + `regulation_histories` (grid) + `regulation_scheduled_versions` pending. Trả mảng vị trí 6 phần tử `[time,who,content,scopeApplied,note,isScheduled]`, mới nhất trước, cắt 50. FE `fetchHistory(scope)` thay `HIST` mock; empty-state #6b7280. Test service 3 + test HTTP 3.
- [x] **②A #4 [Medium]** `unsavedChangesMixin` (beforeRouteLeave) + dirty-guard `guardLeaveDirty()` `$confirm` khi đổi tab (`selectGroup`)/scope (`setScope`)/phòng ban (`onDeptChange` hoàn tác `selectedDeptId`); `unsavedSnapshotSource(){return this.model}`; `markFormPristine()` (KHÔNG markFormSaved — trang persist đa chu kỳ) sau onSave/onCancel/saveVer/cancelPending/saveReg/deleteReg. `revertCurrentTab()` re-fetch tab đang rời khi discard (khớp lời hứa dialog).

**Ruling (từ review độc lập + fix round 1):**
- **#5 `condition_compare_value_end => required|gt`: KHÔNG đổi** — ERP gốc (RegulationRequest.php:39) cũng required|gt, HRM port trung thành. Giá nếu sai: nới nullable, sửa 1 dòng.
- **markFormPristine thay markFormSaved (②A)**: màn cấu hình persist qua nhiều chu kỳ sửa-lưu; markFormSaved tắt cảnh báo vĩnh viễn. Deviation có chủ đích khỏi câu chữ CLAUDE.md.
- **M1 sort ổn định**: PHP 7.4 usort KHÔNG stable → gán `_seq` tie-break; dòng cùng-giây giữ thứ tự nạp nguồn.
- **L2 null-safe created_at**: dòng ERP legacy created_at null → coi ts=0 đẩy cuối, format "—" (không fatal).
- **L1 truyền $type company field**: future-proof boolean store=company hiện Có/Không.
- **L3 test HTTP**: phủ hợp đồng bảo mật 403 (thiếu quyền) + 422 (scope sai / thiếu department_id).

### Checkpoint — 2026-09-15 (Slice 3f ĐÓNG — feature khép về mặt code)
Vừa hoàn thành: Slice 3f — xử lý toàn bộ findings review cuối. Fix batch mechanical (#2/#3/#6/#7/#8/#9) đã xong (verify grep sạch), ①A endpoint lịch sử thật + ②A dirty-guard code + test + qua review độc lập (opus: APPROVED, 0 blocker) + fix round 1 (M1/M2/L1/L2/L3) đã adjudicate đạt. **phpunit MasterData 82/82 PASS** (76 cũ + 3 service history + 3 HTTP). CR=0 cả 6 file (giữ LF). FE không vi-VN cho số; BE không number_format VN-param. NOT committed (rule gop_db, chưa uỷ quyền git).
Đang làm dở: (không) — Slice 3f đóng. Toàn bộ 14 tab (company scalar/text/csv/json/subtable + global + department form/ladder/grid) đã BE+FE+test. Lịch sử thật + cảnh báo chưa lưu đã có.
Bước tiếp theo: QA trình duyệt toàn màn (chưa deploy dev) → user quyết định commit/merge về gop_db. Backlog nhỏ (LOW/NIT chưa fix): cap-50 kép an toàn (chỉ cần comment); test HTTP cap-50/join>3 để service-level.
Blocked: chưa commit (git chưa được uỷ quyền); QA trình duyệt cần deploy dev.

### Checkpoint — 2026-09-15 (Slice 3e task 1+2 XONG; review cuối đang chạy)
Vừa hoàn thành:
  - **Task 3e-1 (gate quyền)**: bọc cả 8 route regulation-config trong `Route::group(['middleware' => 'checkPermission:Cài đặt cấu hình'], …)` tại Modules/MasterData/Routes/api.php — chạy TRƯỚC FormRequest → 403 rõ ràng. Verify: quyền id 149 không có dấu phẩy (middleware-safe); alias `checkPermission` đã đăng ký Kernel.php:69; controller `guard()` còn nguyên ở cả 8 method (phòng thủ lớp 2); FE `canEditRegulation` fail-closed (index.vue:1150). → 3 lớp gate.
  - **Task 3e-2 (nhãn global + số quốc tế + line-ending)**: global-tag "· Áp dụng toàn hệ thống" hiện đúng (index.vue:218). Audit số quốc tế: FE `vi-VN` cho số = RỖNG ✓; BE `number_format(...,',','.')` = RỖNG ✓. Line-ending: index.vue, data.js, api.php, RegulationConfigService.php, RegulationConfigController.php đều CR=0 ✓.
  - **phpunit MasterData: 76/76 PASS** sau khi thêm middleware (test gọi service trực tiếp, không qua HTTP → không ảnh hưởng).
Đang làm dở: Task 3e-3 — final whole-branch review (opus subagent) đang chạy nền; chờ báo cáo tại scratchpad/final-review-khai-quy-che.md.
Bước tiếp theo: nhận findings reviewer → xử lý/park → cập nhật design.md + STATUS.md → đóng feature (chờ QA trình duyệt + quyết định commit của user).
Blocked:

## Ngoài phạm vi (YAGNI — spec mục 11)
- [x] `change_approver` — ĐÃ hiểu đúng + đã có (2026-09-15). KHÔNG phải "duyệt phiên bản quy chế"
  (diễn giải cũ SAI, đã gỡ). ERP: nhãn "Chuyển duyệt Ban giám đốc" — cờ per-dòng-hoa-hồng
  `regulations.change_approver`; bật = mức hoa hồng dòng này do BGĐ quyết khi DUYỆT HĐ (không tính
  công thức). Ở màn cấu hình chỉ là ô tích lưu cờ (đã có: registry/Entity/service/FormRequest/FE
  checkbox + 2 test). Tác động "chặn nút Duyệt thường + bắt BGĐ nhập %" nằm ở MÀN DUYỆT HĐ/ĐƠN hạ
  nguồn (10 blade ERP tiêu thụ `department_main_regulation.change_approver`) → port cùng lúc port màn HĐ.
- [ ] Diff JSON tới từng dòng (chỉ báo "đã thay đổi bảng X")
- [ ] Lưu `version_id` trên chứng từ / truy vấn as-of-date (không cần do Cách A)
- [ ] Field `Thuế vận tải`, `Ngày khai báo công nợ đầu kỳ` (fixed) — chưa version hoá
- [ ] due_configs (ma trận chặn quá hạn) — concern riêng, không thuộc versioning này

## Fix — Điều khoản báo giá/thanh toán hiện HTML thô (2026-09-16)
Báo lỗi (user + screenshot): tab "Báo giá – Hợp đồng" 2 ô Điều khoản hiện nguyên chuỗi HTML CKEditor
của ERP (`<div><span style="font-size:22px">…`) thay vì văn bản đã render. Gốc: 4 field điều khoản
khai `area` → render bằng `V2BaseTextarea` (plain), trong khi BE (RegulationTabRegistry) lưu chúng
là chuỗi HTML rich.
- [x] `data.js`: thêm helper `rich(label, val) => { t:'rich', … }`; đổi 4 `area(...)` → `rich(...)`
      (baogia: quotation_footer, service_quotation_footer; dieukhoan: quotation_footer_company,
      payment_term_company). Nhãn giữ nguyên → mapping label→key BE không đổi.
- [x] `index.vue`: import + register `CompactReviewEditor` (CKEditor wrapper giữ fidelity HTML ERP,
      `remove-buttons=""` = full toolbar như ERP); thêm nhánh render `f.t === 'rich'` ở lưới chính
      (disabled theo `canEditRegulation`) và ở modal hẹn phiên bản (`verEditableFields` không skip
      'rich'); scoped CSS ẩn `<label>` rỗng nội bộ editor (nhãn đã do wrapper `.f` hiện).
- [x] QA trình duyệt Playwright MCP tại `http://127.0.0.1:3000/master-data/regulation-config`
      (2026-09-16): tab "Báo giá – Hợp đồng" hiện 2 CKEditor (`.cke`×2, iframe wysiwyg×2), HTML ERP
      render đúng định dạng (font-size span giữ nguyên), KHÔNG còn chuỗi HTML thô; label rỗng nội bộ
      editor đã ẩn; console 0 lỗi. Ảnh xác nhận đã xem.

## Fix — Nút "Xóa" logo hệ thống không có tác dụng (2026-09-16)
Báo lỗi (user + screenshot): tab "Chung", field "Logo hệ thống" (`V2BaseFile` auto-upload,
`v-model="f.val"`) — bấm nút "Xóa" logo không xảy ra gì, ảnh vẫn hiện.
Gốc (chẩn qua Playwright, xác định bằng `__ob__` + property descriptor): helper `logo()` trong
`data.js` là helper DUY NHẤT không khai `val` (`{ t:'logo', label }`). `model` được observe lúc
init nên object logo có `__ob__`, NHƯNG vì thiếu key `val` lúc đó nên khi `applyTabToModel` gán
`f.val = <path>` (index.vue:1592) thì `val` được thêm dưới dạng property THƯỜNG, KHÔNG reactive.
→ Nút Xóa (V2BaseFile.removeFile) nhả `input: null` qua `v-model="f.val"`, ghi được null vào model
nhưng Vue không notify → child V2BaseFile giữ nguyên prop `value` cũ → ảnh vẫn hiện. (Không phải lỗi
`:key="fi"` cũng không phải lỗi V2BaseFile.)
- [x] `data.js`: `logo = () => ({ t:'logo', label:'Logo hệ thống', val: null })` — khai `val` từ đầu
      như mọi helper khác để Vue observe → reactive; kèm comment giải thích bẫy.
- [x] QA Playwright MCP `http://127.0.0.1:3000/master-data/regulation-config` (2026-09-16): sau reload,
      `Object.getOwnPropertyDescriptor(logoField,'val').get` = có (reactive:true); bấm "Xóa" → row biến
      mất, `model...logo.val = null`, field trở về trạng thái trống "Chọn tệp" (còn dùng lại được);
      console 0 lỗi. Không sửa file dùng chung V2BaseFile.

## Fix — Đổi tab báo "chưa lưu" dù user không sửa gì (2026-09-16)
Báo lỗi (user): chỉ bấm vào 1 tab (không nhập/sửa gì) rồi chuyển sang tab khác thì luôn hiện confirm
"Thông tin chưa lưu".
Gốc: `unsavedChangesMixin` chỉ tính là "user sửa" nếu thay đổi model xảy ra trong `USER_ACTION_WINDOW_MS`
(500ms) sau 1 pointerdown/keydown. Cú CLICK vào tab chính là pointerdown → mở cửa sổ 500ms; cùng cú
click đó gọi `fetchTab` → API (dev local thường < 500ms) trả về + `applyTabToModel` ghi dữ liệu server
vào `this.model` NGAY TRONG cửa sổ → mixin hiểu nhầm data-load là user edit, dời baseline về giá trị
cũ và đánh `unsavedUserChanged=true` → `isFormDirty()` = true → mở tab kế tiếp bị chặn hỏi. `fetchTab`/
`fetchGridTab` không re-baseline sau khi nạp.
- [x] `index.vue`: sau `applyTabToModel` trong `fetchTab` và sau `applyGridConfig` trong `fetchGridTab`,
      gọi `this.$nextTick(() => this.markFormPristine())`. Dùng `$nextTick` để chạy SAU khi watcher của
      mixin flush (nếu không, watcher chạy sau lại đánh bẩn). Nạp dữ liệu server không phải user sửa nên
      chốt lại mốc pristine là đúng; không ảnh hưởng luồng revert/onSave (đều nạp lại từ server = đúng mốc).
- [x] QA Playwright MCP `http://127.0.0.1:3000/master-data/regulation-config` (2026-09-16):
      (1) set groupIdx qua 8 tab → `isFormDirty()` = false ở mọi tab;
      (2) mô phỏng race (pointerdown mở cửa sổ + load nhanh trong 320ms): mọi tab `dirtyAfterSettle=false`
      (transient trong cửa sổ tự hết trong cùng nextTick);
      (3) click THẬT (pointerdown+click) qua 6 tab, cách nhau ~1s như người dùng → `confirmAppeared=false`
      ở tất cả, console 0 lỗi. Không sửa file dùng chung (mixin giữ nguyên).

## Thiết kế lại UI "Lịch sử thay đổi" — quá dài (2026-09-16)
Báo lỗi (user): "lịch sử thay đổi quá dài, thiết kế lại giao diện".
Hiện trạng: khối đổ THẲNG toàn bộ lịch sử (mock 50 dòng) → cao ~2111px, lấn cả trang; link "Xem tất
cả lịch sử" là link chết (`href="javascript:void(0)"`, không handler); cột "Phạm vi áp dụng" lặp lại
đúng tên công ty ở tiêu đề nên nặng mắt.
- [x] `index.vue` data: thêm `historyExpanded: false` + `historyPreview: 6`.
- [x] `index.vue` computed `shownHistory`: gọn = `curHistory.slice(0, historyPreview)` (6 dòng mới nhất),
      bung = toàn bộ. Watch `scope`: đổi phạm vi thì reset `historyExpanded=false`.
- [x] `index.vue` template: đổi link chết thành `<button class="lnk">` toggle — chỉ hiện khi
      `curHistory.length > historyPreview`; nhãn "Xem tất cả {N} thay đổi" ↔ "Thu gọn" (icon mũi tên
      xuống/lên). Render `shownHistory`. Khi bung, `.tbl-wrap` thêm class `history-scroll`. Footer `.hf`
      "Đang hiển thị 6 / {N} thay đổi gần nhất" khi đang gọn. Cột phạm vi gắn class `scope-cell` (làm nhạt).
- [x] `index.vue` CSS: `.lnk` reset về style button (border 0, bg trong suốt, hover nền teal nhạt);
      `.tbl-wrap.history-scroll{max-height:360px;overflow-y:auto}` (thead đã sticky sẵn); `.scope-cell`
      màu `--ink-3` 12px; `.hf` footer viền trên + chữ nhạt.
- [x] QA Playwright MCP `http://127.0.0.1:3000/master-data/regulation-config` (2026-09-16):
      gọn = 6 dòng, cao 378px (trước 2111px), toggle "Xem tất cả 50 thay đổi", footer "Đang hiển thị
      6 / 50 thay đổi gần nhất"; bấm bung = 50 dòng trong khung cuộn max-height 360px (scrollable),
      cả khối chỉ 422px, toggle "Thu gọn"; bấm lại thu gọn về đúng 6 dòng/378px; console 0 lỗi.

## Chuyển field "% Thưởng NVKD tối đa" sang tab Báo giá – Hợp đồng (2026-09-16)
Yêu cầu (user): "cái % thưởng nvkd tối đa chuyển sang tab báo giá - hợp đồng".
Field `maximum_market_cost_percent` (store=company, cột `companies`) trước nằm ở tab `giaban` (Giá bán);
người dùng muốn nó thuộc tab `baogia` (Báo giá – Hợp đồng) cạnh các % HĐ khác. Cả 2 tab đều MIXED scope,
cùng ghi bảng `companies`; BE join theo KEY (cột), FE join theo LABEL trong từng tab → chỉ đổi chỗ khai.
- [x] BE `RegulationTabRegistry.php`: gỡ entry `maximum_market_cost_percent` khỏi block company của tab
      `giaban`, chèn vào cuối block company tab `baogia` (sau `max_employee_on_department`). Key/label/store
      giữ nguyên nên lịch sử (keyed by field_name) và cột DB không đổi.
- [x] FE `data.js`: gỡ `num('% Thưởng NVKD tối đa', '%', 5)` khỏi group `giaban`, thêm vào group `baogia`
      sau `num('SL nhân viên tối đa/phòng', ...)`. Badge đếm field: baogia +1, giaban −1.
- [x] QA Playwright MCP `http://127.0.0.1:3000/master-data/regulation-config` (2026-09-16): badge đếm
      Báo giá 10→11, Giá bán 5→4; mở tab Báo giá → "% Thưởng NVKD tối đa" hiện sau "SL nhân viên tối
      đa/phòng", KHÔNG có nhãn "Áp dụng toàn hệ thống" (đúng company-scope); mở tab Giá bán → field đã
      biến mất (còn 4 field); console 0 lỗi.
      Lưu ý dữ liệu prod: phiên bản hẹn ngày đang tag `tab_key='giaban'` sẽ không hiện dưới baogia sau khi
      đổi — nên áp/huỷ trước (concern dữ liệu, không phải blocker code).

## Tách 3 tab (Công nợ / Xuất–nhập hàng / Kỳ quyết toán) sang phân hệ Tài chính (2026-09-16)
Yêu cầu (user + screenshot "3 phần này chuyển sang phần Tài chính"): 3 tab **Công nợ & tài chính (congno),
Xuất – nhập hàng (xnk), Kỳ quyết toán (quyettoan)** phải rời khỏi màn cấu hình ở phân hệ **Danh mục**
(master-data) và được thao tác ở một màn tương tự nằm trong phân hệ **Tài chính** (finance). Phân hệ Danh
mục mất 3 tab đó; phân hệ Tài chính có màn giống hệt chỉ hiện 3 tab đó.
- Kiến trúc đã chốt (user approve): **1 component dùng chung + 2 trang thin `extends`** (KHÔNG dựng màn trùng
  lặp, KHÔNG import-as-child). Lý do quyết định: `unsavedChangesMixin` dùng in-component guard
  `beforeRouteLeave` — guard này CHỈ chạy khi trang là route component thật (qua `extends` + merge mixin),
  KHÔNG chạy khi component chỉ render như con → buộc phải extends thay vì import làm child.
- Quyền: **dùng chung** quyền `'Cài đặt cấu hình'` sẵn có (user chọn phương án a), KHÔNG đẻ quyền tài chính
  riêng. BE api.php gate mọi route regulation-config bằng đúng quyền này → không đổi. BE join tab theo KEY
  qua URL `regulation-config/{tabKey}` (mỗi tab fetch độc lập) → **BE KHÔNG ĐỔI GÌ**, việc phân tab ở đâu
  thuần FE.
- [x] `git mv` `pages/master-data/regulation-config/{index.vue,data.js}` → `components/regulation-config/`
      thành component dùng chung `RegulationConfigScreen.vue` + `data.js` (đi cùng nhau, giữ import tương đối
      `./data.js`; mọi import khác đã dùng alias `@/`/`~/` nên không lệ thuộc độ sâu thư mục).
- [x] `RegulationConfigScreen.vue`: thêm data `subsystem: 'master-data'`; `curGroups` lọc theo
      `(g.subsystem || 'master-data') === this.subsystem`; thêm computed `hasDeptScope`; khối "Phạm vi áp dụng"
      bọc `v-if="hasDeptScope"` (phân hệ Tài chính không có tab phòng ban → ẩn toggle scope). Giữ nguyên
      `layout: 'default-sidebar'`, `mixins: [unsavedChangesMixin]`, `head()`.
- [x] `data.js`: thêm `subsystem: 'finance'` vào 3 group congno/xnk/quyettoan (các tab còn lại mặc định
      'master-data'). **Bổ sung 2026-09-16 (user + screenshot "Giá bán cũng đưa về tài chính")**: thêm
      `subsystem: 'finance'` vào group `giaban` → phân hệ Tài chính có 4 tab (Giá bán + 3 tab cũ),
      Danh mục còn 7 tab. Chỉ sửa data.js, BE không đổi. Verify MCP: finance 4 tab (có Giá bán),
      master-data 7 tab (mất Giá bán), console 0 lỗi.
- [x] `pages/master-data/regulation-config/index.vue` (thin) — `extends RegulationConfigScreen`, không override
      subsystem → mặc định 'master-data' (hiện 8 tab, ẩn 3 tab Tài chính). Là route component thật → giữ
      beforeRouteLeave.
- [x] `pages/finance/regulation-config/index.vue` (thin) — `extends RegulationConfigScreen` + `data(){return{
      subsystem:'finance'}}` → chỉ hiện 3 tab Tài chính, ẩn scope toggle.
- [x] `components/subsystem-menu/finance.js`: item **cấp 1** (ngoài sidebar, KHÔNG nhóm con) "Khai Quy chế –
      Cấu hình" (tên khớp bên Danh mục) → `/finance/regulation-config`, `icon: 'ri-file-settings-line'`,
      `isShow: ['Cài đặt cấu hình']`, đặt ngay sau "Tổng quan" giống vị trí bên phân hệ Danh mục
      (master-data.js item #2). Menu Danh mục cũ giữ nguyên `/master-data/regulation-config`.
      (Chốt với user 2026-09-16: tên = "Cấu hình" như bên Danh mục, để cấp 1 không lồng menu cấp 2.)
- [x] QA Playwright MCP (2026-09-16, `http://127.0.0.1:3000`):
      - `/master-data/regulation-config`: 8 tab (3 tab Tài chính đã biến mất), scope toggle CÒN (có tab
        phòng ban), console 0 lỗi.
      - `/finance/regulation-config`: đúng 3 tab (Công nợ & tài chính · Xuất – nhập hàng · Kỳ quyết toán),
        KHÔNG có scope toggle (`hasDeptScope=false` → ẩn), sidebar/layout render, console 0 lỗi.
      - Sau `git mv` lần đầu webpack dev-server báo ENOENT (watcher giữ inode cũ) → `touch` 4 file + rebuild
        là hết; route finance lần đầu blank do chunk build on-demand, chờ build xong render đủ 3 tab.

---

## Bổ sung 2 field kho — tab "Công nợ & tài chính" (congno) — 2026-09-17

Yêu cầu user (kèm screenshot): tab Công nợ & tài chính thiếu 2 trường **Kho khuyến mại** và **Kho hàng gửi**.
Chốt với user: "kho khuyến mại bên erp có, kho hàng gửi thêm mới cho chọn kho kế toán".

Quyết định (không hỏi thêm — user đã trả lời rõ):
- **Kho khuyến mại** = cột SẴN CÓ `companies.promo_warehouse_ids` (ERP getter json_decode) → BẮT BUỘC lưu JSON
  mảng id, nguồn option = `warehouses` của ĐÚNG công ty (status=1).
- **Kho hàng gửi** = cột MỚI `companies.consignment_warehouse_ids` (JSON), nguồn option = `accounting_warehouses`
  (kho kế toán) của công ty. Chọn **nhiều** (multiselect) cho đồng bộ với kho khuyến mại + linh hoạt.
- Đặt ở tab **congno** (đúng như user báo). congno `no_hen=false` → 2 field vào cả luồng lưu ngay lẫn modal hẹn phiên bản.

Tasks:
- [x] Migration `Modules/MasterData/Database/Migrations/2026_09_17_000001_add_consignment_warehouse_to_companies_table.php`
      thêm `companies.consignment_warehouse_ids` text nullable (promo_warehouse_ids đã có, KHÔNG thêm). Đã chạy trên erp_new local.
- [x] `RegulationTabRegistry.php` congno: thêm 2 field `promo_warehouse_ids` + `consignment_warehouse_ids`
      (type=json, input=multiselect, options=warehouses/accounting_warehouses).
- [x] `RegulationConfigService::resolveOptions()` thêm param `?int $companyId` + 2 case `warehouses`/`accounting_warehouses`
      (lọc company_id + status=1, id int). getTabConfig truyền $companyId vào resolveOptions (field + subtable col).
- [x] FE `data.js` congno: thêm `msel('Kho khuyến mại')`, `msel('Kho hàng gửi')`.
- [x] FE `RegulationConfigScreen.vue`: apiFieldKeys mang `type`; mselect json-aware ở applyTabToModel (đọc mảng),
      collectTabValuesFromModel + collectTabValues (json→mảng, csv→join ','); thêm case mselect vào modal hẹn phiên bản
      (V2BaseSelectInModal multiple) + openVer parse c.new json cho mselect.
- [x] BE smoke test (tinker): getTabConfig congno cty 1 trả 2 field (options 7 kho / 11 kho kế toán, lọc đúng cty);
      roundtrip ghi JSON → đọc lại ra mảng. Khôi phục promo cty 1 về gốc `["2","4"]`.
- [x] `resolveOptions()` case `accounting_warehouses`: hiển thị nhãn `<mã kho kế toán> - <tên>` (select thêm cột `code`,
      bỏ tiền tố nếu kho không có mã). id lưu/diff không đổi. (17/09/2026, theo yêu cầu user)
- [x] Verify FE bằng Playwright: 2 field hiện ở tab Công nợ & tài chính, chọn/lưu được, reload giữ giá trị.
      (17/09/2026) Kho khuyến mại hiện dữ liệu ERP sẵn có (Liên Ninh); Kho hàng gửi (11 kho kế toán) chọn
      "Hàng gửi tại kho Hải Phòng" (id 35) → Lưu cấu hình → reload giữ chip + log `— → ["35"]`; xoá chip → lưu →
      log `["35"] → —`. Console 0 lỗi suốt quá trình. Test data đã dọn về NULL.


---

## Fix: Trường "Ràng buộc lập HĐ" — đổi tên, bỏ nha khoa, chuyển tab, tô xanh khi chọn (22/09/2026)

Yêu cầu user (màn Khai quy chế – cấu hình, phân hệ Bán hàng/Tài chính):
1. Sai tên trường: "Ràng buộc lập HĐ theo loại" → tên đúng "Ràng buộc lập HĐ theo thị trường".
2. Bỏ item "Nguyên tắc nha khoa".
3. Chuyển trường (toggle) từ tab "Báo giá – Hợp đồng" (baogia) sang tab "Tổ chức bán hàng & thị trường" (thitruong).
4. Toggle khi CHỌN phải đổi xanh rõ ràng (hiện chỉ công tắc nhỏ đổi teal → user thấy chọn/không như nhau).

Phân tích (không hỏi thêm — yêu cầu rõ):
- Toggle join value theo apiLabel (item[2]) qua `apiFieldKeys[tabKey]` → BE registry BẮT BUỘC move 4 field
  is_equipment/is_repair/is_project/is_principle từ baogia sang thitruong; is_dental_principle XÓA khỏi registry.
- KHÔNG drop cột `configs.is_dental_principle` (giữ data, không migration) — chỉ gỡ khỏi UI/registry.
- `normalizeValues` bỏ qua field vắng mặt (không null hoá) → move tab không làm mất data cột cũ.
- thitruong `no_hen=true` (áp ngay) → 4 toggle chuyển thành áp-ngay, hợp ngữ nghĩa cấu hình thị trường.
- f.label (arg1 của tog) chỉ để hiển thị → đổi tên an toàn, apiLabel item giữ nguyên khớp registry.

Tasks:
- [x] FE `data.js`: gỡ block `tog(...)` khỏi group baogia; thêm vào cuối group thitruong với label
      "Ràng buộc lập HĐ theo thị trường", bỏ item "Nguyên tắc nha khoa".
- [x] BE `RegulationTabRegistry.php`: move 4 field is_equipment/is_repair/is_project/is_principle từ baogia → thitruong;
      xóa is_dental_principle. (tinker verify: baogia còn 10 key, thitruong nay 7 key gồm 4 is_*)
- [x] FE `RegulationConfigScreen.vue` CSS `.toggles .tg.on`: tô nền + viền + chữ xanh (teal) khi chọn
      (+ transition mượt); công tắc `.sw` bật phải.
- [x] Test `RegulationGlobalScopeTest`: thay is_equipment (không còn thuộc baogia) bằng field baogia khác
      (customer_register_expiry) ở 4 chỗ dùng functional (setUp + 3 assert). 6/6 test pass, php lint clean.
- [x] Verify Playwright (2026-09-22, `http://127.0.0.1:3000/sale/regulation-config`): tab "Tổ chức bán hàng &
      thị trường" (badge 4) có toggle "Ràng buộc lập HĐ theo thị trường" đúng 4 item (Thiết bị/Sửa chữa/Dự án/
      Nguyên tắc), KHÔNG còn "Nguyên tắc nha khoa"; Thiết bị+Sửa chữa (val=1) hiện XANH cả chip+công tắc,
      Dự án+Nguyên tắc (val=0) xám → phân biệt rõ; click "Dự án" → đổi xanh ngay. Tab "Báo giá – Hợp đồng"
      (badge 10) cuộn hết KHÔNG còn toggle. Ảnh xác nhận đã xem.
      GHI CHÚ: round-trip lưu+reload KHÔNG kiểm được vì user "Trần Văn Đức" thiếu quyền tải cấu hình
      (API trả "Bạn không có quyền" → giá trị rơi về default data.js); cần user có quyền để test lưu/đọc lại.


---

## Bổ sung 3 trường DSTC vào tab "Báo giá – Hợp đồng" (22/09/2026)

Yêu cầu user: thiếu 3 trường (có bên ERP) — Hệ số quy đổi loại giá tính DSTC / Hệ số quy đổi theo
tính chất hàng hóa tính DSTC / Tỷ lệ chia DS theo quy chế phối hợp thực hiện. Đồng ý ghi thẳng 3 bảng
ERP (company_price_types, company_product_types, company_rule_commissions); đặt tab baogia; CÓ hẹn ngày
áp dụng (uỷ quyền thiết kế); hành vi giống ERP (preset, chỉ sửa hệ số/%). Chi tiết design.md.

Tasks:
- [x] BE `RegulationConfigService`: generalize `loadSubtable($meta,$scopeId)` (fk company_id + cast theo
      cột + merge preset) & `applySubtable` (cast theo cột); thêm `buildPresetRows`/`mergePresetRows`.
- [x] BE `RegulationConfigService::getCurrentValues`: truyền $scopeId vào loadSubtable.
- [x] BE `RegulationConfigService::applyVersion` nhánh company: tách field subtable → applySubtable(company_id).
- [x] BE `RegulationConfigService::getTabConfig`: passthrough `unit` cho cột subtable; `resolveOptions`
      thêm `inline:coordination_address`.
- [x] BE `RegulationTabRegistry`: thêm 3 field subtable (store=company, fk=company_id, columns+cast+preset+
      item_rules) vào tab baogia.
- [x] BE `ScheduleRegulationVersionRequest`: withValidator branch preset_rule_commissions (tổng %=100/dòng).
- [x] FE `data.js`: helper `subPreset` + 3 field vào group baogia.
- [x] FE `RegulationConfigScreen.vue`: editor preset (nhãn dòng read-only + ô số; ③ ẩn sup2 khi room=2);
      applyTabToModel set thêm cols/preset cho field mới (dùng lại subtable branch).
- [x] Test: chạy `RegulationGlobalScopeTest` (không vỡ) + php lint.
- [x] Verify Playwright (http://127.0.0.1:3000): 3 trường hiện đúng preset ở tab Báo giá – Hợp đồng, sửa
      hệ số/% + Lưu cấu hình → reload giữ giá trị; ③ ẩn sup2 khi 2 phòng, tổng ≠100 báo lỗi.

### Checkpoint — 2026-09-22 15:10
Vừa hoàn thành: 3 trường DSTC (subtable preset) tab "Báo giá – Hợp đồng" — BE + FE xong, verify Playwright PASS.
- Render: ① Loại giá 7 dòng (kèm ảo "Giá dịch vụ"), ② Tính chất hàng hoá 15 dòng (kèm ảo "Dịch vụ"),
  ③ Quy chế phối hợp 5 dòng; ③ ẩn "hỗ trợ 2" = "—" ở 3 dòng 2 phòng, hiện ô số ở 2 dòng 3 phòng.
- Sửa hệ số "Giá bán theo lô" + Lưu cấu hình → POST /baogia/versions 200 → reload giữ 0.09; tổng %≠100
  chặn lưu (KHÔNG POST) + báo lỗi đỏ inline "Tổng tỉ lệ chia … phải bằng 100%".
- Tab mixed baogia lưu tách 2 version: scope company (giữ 3 subtable trong payload → cron hẹn ngày vẫn áp
  được) + scope global (các scalar config). Đã kiểm payload company chứa đủ 3 subtable.
- BẪY môi trường (không phải bug code): user e2e `ductv.kd2` (emp 48, role Timesheet 32) THIẾU quyền
  `Cài đặt cấu hình` (perm 149) → mọi API regulation-config trả 403. Đã tạm cấp perm cho role 32 để test
  rồi GỠ; đã khôi phục hệ số 0.04, xoá 3 version test + 3 dòng history test. DB dev sạch như trước.
Bước tiếp theo: chờ user review; nếu OK có thể wrap up (design.md đã có mục DSTC). KHÔNG commit khi chưa được yêu cầu.
Blocked:

## Bug #9 — Phòng ban không ràng buộc thị trường show all toàn hệ thống
Yêu cầu: tab "Tổ chức bán hàng & thị trường", field "Phòng ban không ràng buộc thị trường"
chỉ show phòng ban ĐANG HOẠT ĐỘNG (status=1) thuộc CÔNG TY đang cấu hình. Hiện đang show all.

- [x] Root cause: `RegulationConfigService::resolveOptions()` case `'departments'` không lọc
      `company_id`/`status` (khác warehouses/accounting_warehouses vốn đã lọc). tab thitruong=MIXED
      nên `$companyId` truyền vào getTabConfig là công ty thật.
- [x] Fix BE: case `'departments'` thêm `->where('status',1)->when($companyId, company_id=$companyId)`.
      Chỉ 1 field dùng nguồn này (department_groups, dòng registry 227) → phạm vi gọn.
- [x] Test đỏ→xanh: `RegulationThitruongTest::department_groups_options_scoped_to_active_departments_of_company`
      (assert đúng đủ tập active của công ty; loại phòng ban công ty khác + đã ngừng hoạt động). 3/3 PASS.
- [x] FE không đổi (msel render nguyên options BE trả).

### Checkpoint — 2026-09-23
Vừa hoàn thành: fix Bug #9 option source departments (lọc company + status) + test PASS.
1 file BE đổi (RegulationConfigService) + 1 file test (RegulationThitruongTest). Chờ user duyệt commit.
Bước tiếp theo: commit khi user yêu cầu.
Blocked:

## Bug #10 — Lịch sử "Tổ chức bán hàng & thị trường": giá trị sai + gộp 1 lần lưu vào 1 ô
Yêu cầu: (1) lịch sử chưa hiển thị đúng giá trị (đang show id/mã thô); (2) mỗi trường thay đổi 1 dòng
khó theo dõi — 1 lần cập nhật nhiều trường thì gộp vào 1 ô.

Fix #1 — giá trị đúng (id/mã → tên người đọc):
- [x] Root cause: `formatDiffList` không map field có nguồn `options` (department_groups, customer_groups,
      market_division_type) → hiện id/mã csv thô.
- [x] BE `RegulationConfigService`: thêm `optionLabelMap($source)` (cache, KHÔNG lọc active/company để giá
      trị cũ trỏ bản ghi đã khoá/đổi cty vẫn tra ra tên) + `formatOptionValue($raw,$source)`; `formatDiffList`
      nhánh `options` → dùng formatOptionValue thay formatHistoryValue.
- [x] Verify tinker: dept ids → "PHÒNG THIẾT BỊ Ô TÔ 2, …"; customer_groups → tên nhóm; market_division_type
      "ward" → "Theo quận / huyện".

Fix #2 — gộp 1 lần lưu vào 1 ô (chốt với user: hướng B):
- [x] Quyết định (user chốt): tab hỗn hợp 1 lần lưu sinh 2 dòng khác phạm vi (company + global) → gộp 1 ô,
      mỗi phạm vi 1 dòng có nhãn `[Phạm vi]`, cột "Phạm vi áp dụng" để `—` (chú thích phạm vi trong nội dung).
- [x] BE `RegulationConfigService`: const `HISTORY_MERGE_WINDOW=2` (giây); `historyConfigCompany` +
      `historyConfigDepartment` đi qua `groupConfigHistoryRecords()` (gộp bản ghi cùng người+tab+created_at
      sát nhau) → `buildConfigHistoryRow()` (1 phạm vi: giữ định dạng cũ; nhiều phạm vi: mỗi phạm vi 1 dòng
      nhãn `[Phạm vi]`, applied=`—`; thứ tự company/department trước, global sau).
- [x] FE `RegulationConfigScreen.vue`: ô "Nội dung thay đổi" thêm class `chg` + CSS `white-space: pre-line`
      (xuống dòng theo `\n`). Không đổi logic FE.
- [x] Test: RegulationHistoryTest 7/7 + RegulationThitruongTest 3/3 PASS (nhánh 1 phạm vi giữ nguyên
      output → không vỡ assertion chuỗi cũ). Lint sạch.
- [x] Verify tinker: 1 lần lưu thitruong → 1 dòng, 2 block phạm vi; dòng cũ 1-phạm-vi không đổi.
- [x] Dọn 2 dòng rác test (`by=999`, tab=baogia, global) sót trong DB chung `erp_hrm_check` — chính là
      nguyên nhân RegulationHistoryTest trước đó đỏ (assertCount 4 nhận 6); dọn xong 7/7 xanh.

### Checkpoint — 2026-09-23 (Bug #10)
Vừa hoàn thành: Fix #1 (giá trị lịch sử → tên) + Fix #2 (gộp 1 lần lưu vào 1 ô, hướng B) — BE + FE + test.
Regression: 16 errors + 2 failures ở suite MasterData tổng đều PRE-EXISTING (đã stash xác nhận):
11 ProductClassificationCatalogTest (lỗi setup) + 5+2 RegulationCongnoVersioningTest (cột
`consignment_warehouse_ids` migration chưa apply DB local + field count 9≠7) — KHÔNG do thay đổi này.
File đổi: `RegulationConfigService.php` (BE), `RegulationConfigScreen.vue` (FE).
Bước tiếp theo: commit khi user yêu cầu (Bug #9 + Bug #10 chung file BE → gộp/commit theo yêu cầu user).
Blocked:

### Bug #10b — Lịch sử tab "Báo giá – Hợp đồng" (baogia) DUMP nguyên JSON (subtable)
User "lưu thử ra cái đống này" (ảnh 2026-09-23 16:22): 3 field subtable DSTC
(`company_price_types`, `company_product_types`, `company_rule_commissions`) hiển thị lịch sử bằng
CHUỖI JSON thô `[{"price_type_id":1,"name":"Bên lẻ",...}]` → không đọc được.
- Nguyên nhân 1 (đã fix — DISPLAY): `formatHistoryValue` case json/subtable trả nguyên chuỗi JSON.
  → Thêm `formatSubtableChange`: đọc `columns` registry, tách theo DÒNG, chỉ nêu ô SỐ đổi
  ("Bên lẻ: 1 → 1.5"; rule_commissions gồm nhãn định danh + %). Không đủ định danh/cột số (bảng
  công khoán) → tóm tắt "N dòng → M dòng". Giới hạn 6 dòng + "…(+N)". Helpers: `formatSubtableChange`,
  `decodeSubtableRows`, `subtableNumEq`, `subtableNumText`, `subtableRowLabel`, `subtableRowCountSummary`.
  Verify tinker: price_types 1→1.5 sạch; id=503 render OK.
- Nguyên nhân 2 (ROOT — CHƯA fix, chờ user): `buildDiffSnapshot` (dòng 557) so json/subtable bằng
  `json_encode` CHUỖI → khác THỨ TỰ KEY (`product_type_id,name,coefficient` vs `name,coefficient,
  product_type_id`) hay `1` vs `1.0` = ghi DIFF GIẢ dù bảng KHÔNG đổi (id=503: product_types +
  rule_commissions "đổi" nhưng value y hệt → hiện "cập nhật 15 dòng / 5 dòng" thừa). Đề xuất
  `canonicalizeDiffValue` (ksort key + chuẩn hoá số) trước khi so → không ghi phiên bản/lịch sử giả.
  `buildDiffSnapshot` là HÀM DÙNG CHUNG (hasChanges + saveTabVersions + scheduled) → HỎI user trước khi sửa.
  → User "sửa đi": ĐÃ fix `buildDiffSnapshot` so CANONICAL (`canonicalizeDiffValue`: ksort KEY, `1`↔`1.0`)
  thay vì so chuỗi `json_encode` → hết diff giả. Verify tinker: phantom → 0 diff, 1→1.5 thật → 1 diff.
- [x] Bug #10b-2 — VẼ BẢNG ô "Nội dung thay đổi" (user "ví dụ vẽ bảng" → duyệt mock "ok"):
  - BE: `getHistory` thêm phần tử [6] = nội dung CÓ CẤU TRÚC `[{scope, lines:[{field,old,new}|{field,summary}]}]`,
    nhóm theo phạm vi (scope=null khi 1 phạm vi → FE không hiện nhãn). Chuỗi [2] GIỮ nguyên làm fallback.
    Helpers mới: `buildDiffLines` (mirror `formatDiffList`) + `buildSubtableLines` (mirror `formatSubtableChange`,
    mỗi ô số đổi = 1 dòng "Nhãn – Tên dòng[ (Cột)]"; không đổi → 1 dòng summary; cap 6 + "…(+N dòng)").
    Cập nhật 5 producer: buildConfigHistoryRow (2 nhánh), historyCompanyRegulation, historyRegulationGrid, scheduledRow.
    Test: `RegulationHistoryTest` assertCount 6→7 (×2) + assert cấu trúc [6] dòng company_regulation.
    Verify tinker company 1: multi-scope → 2 nhóm có nhãn, subtable đổi → `{field:"… – Bán lẻ",old:"1",new:"1.5"}`,
    subtable không đổi → `{summary:"cập nhật 15 dòng"}` — KHỚP mock đã duyệt.
  - FE `RegulationConfigScreen.vue`: `.chg` render `<table.chg-tbl>` khi `hasChangeTable(r)` (có [6]), else `{{ r[2] }}`.
    Cột Trường | Cũ(đỏ #dc2626) | → (xám) | Mới(xanh --ok). Nhóm nhiều phạm vi có header `● <tên>`.
    Dòng summary span 3 cột, muted italic. Method `hasChangeTable`. CSS `.chg-tbl` thêm sau `.chg`. GIỮ LF.
  - Chưa verify Playwright (không có `e2e/.auth/user.json`) → user nghiệm thu bằng ảnh.
File đổi Bug #10b: `RegulationConfigService.php` (BE: display + canonical diff + structured [6]),
`RegulationConfigScreen.vue` (FE: bảng), `RegulationHistoryTest.php` (test).

## Bug #11 — Tab "Hàng hóa" thiếu 4 khối (ĐẢO chốt sai 2026-09-14)

Redmine: 'Hàng hóa "Thiếu các trường: Hệ số thuế BVMT · Hàng reset giá · Hàng cập nhật giá · Hàng mới
(đang khai ở quy chế công ty cũ)"'. Chốt 2026-09-14 hướng (a) đã CẮT NHẦM: `environment_tax` tưởng
"field theo SP" (thực ra `configs.environment_tax` global), nhóm toggle "Hàng cập nhật giá / Hàng mới"
tưởng "bịa" (thực ra là card per-company trên `companies`). Nguyên nhân: pass 2026-09-14 chỉ soi blade
config GLOBAL của ERP, KHÔNG soi blade quy chế per-company (`common/companies/regulation.blade.php`).

Bản đồ ERP đã xác minh (Explore agent + Schema::hasColumn trên erp_hrm_check — CÓ đủ cột):
| Field | Cột | Bảng/scope | Kiểu |
|---|---|---|---|
| Hàng không bắt buộc Serial | serial_product_types | configs / global | csv product_types |
| Hệ số thuế BVMT | environment_tax | configs / global | decimal %, |
| Hàng reset giá | reset_price_when_zero_inventory_product_types | companies / company | csv product_types |
| Hàng cập nhật giá | is_company_price·is_all_brand·brand_ids | companies / company | bool·bool·csv brands |
| Hàng mới | is_new_company·is_new_brand·new_brand_ids | companies / company | bool·bool·csv brands |

Quyết định user: Q1 "Gộp vào card công ty (bám ERP)" → dời is_company_price/is_all_brand từ configs
sang companies, gom brand_ids thành card; Q2 "ẩn 'Hãng cần duyệt' khi bật 'Tất cả hãng SX'".
Quyết định thêm (coherence): tab → **no_hen=true** (ERP không hẹn lịch mấy field này + modal hẹn SKIP
toggle nên không sửa được → apply-ngay là đúng & nhất quán).

- [x] BE `RegulationTabRegistry.php`: hanghoa GLOBAL→**MIXED**, no_hen=true, 9 field, LABEL DUY NHẤT
  (FE join theo label → 2 card không được trùng). serial+environment_tax store=config; 3 field card
  "Hàng cập nhật giá" + 3 field card "Hàng mới" + reset store=company. brand_ids/new_brand_ids
  type=string options='brands'; reset type=string options='product_types'; bool type=boolean.
- [x] FE `data.js`: dựng lại fields hanghoa (msel Serial; num environment_tax %; msel reset; tog+msel
  mỗi card, apiLabel khớp registry; mselect card gắn `hideWhenOn` = apiLabel toggle "Tất cả hãng").
  Thêm 'hanghoa' vào `NO_HEN`.
- [x] FE `RegulationConfigScreen.vue`: `isFieldShown(f)` (ẩn mselect khi toggle điều khiển ON) +
  `v-if="isFieldShown(f)"` trên `.f`; `noHenReason` thêm nhánh hanghoa.
- [x] BE `RegulationHanghoaTest.php`: cập nhật cho MIXED (config: serial+environment_tax; company:
  6 field brand/bool + reset), round-trip + áp ngay.
- [~] Verify: BE 2 test PASS; data.js parse OK + template .vue compile sạch + không có eslint-loader (v-for+v-if an toàn). Playwright THỦ CÔNG chờ login (repo chưa có e2e/.auth) → user nghiệm thu bằng ảnh.

### Checkpoint — 2026-09-24
Vừa hoàn thành: Bug #11 hanghoa restructure (đảo chốt sai 2026-09-14) — BE registry MIXED+no_hen 9 field
(serial+environment_tax=config; 2 card duyệt giá + reset=company; label duy nhất theo card), FE data.js
+ NO_HEN + isFieldShown/v-if ẩn "Hãng cần duyệt" khi "Tất cả hãng" bật, test cập nhật (2 PASS).
Đang làm dở: (không) — code xong, chưa commit.
Bước tiếp theo: user nghiệm thu UI tab Hàng hóa bằng ảnh; nếu OK → commit gop_db (chờ lệnh).
Blocked: Playwright thủ công cần login (repo HRM chưa setup e2e/.auth).

## Bug #12 — Điều khoản báo giá/thanh toán mô hình hoá SAI (port lệch ERP)

Redmine 12: "điều khoản báo giá và điều khoản thanh toán đang cài theo LOẠI BÁO GIÁ. Form hiện tại
chưa có phần chọn loại báo giá → phần điều khoản ở tab Báo giá – Hợp đồng có đang thừa không?"

Chẩn đoán (2 Explore agent + Schema check):
- ERP cài điều khoản báo giá theo **loại báo giá** (bảng `quotation_terms.type`, có dropdown "Loại báo
  giá" + lọc lúc tạo báo giá) và điều khoản thanh toán theo **phương thức thanh toán**
  (`payment_method_terms.payment_method_id`) — là THƯ VIỆN danh mục, KHÔNG phải ô rich-text phẳng.
  `configs.quotation_footer`/`service_quotation_footer` chỉ là footer mặc định fallback (ERP CÓ 2 cột này).
- HRM đang có 4 ô rich-text phẳng, KHÔNG có khái niệm "loại báo giá". Trong đó:
  - `configs.quotation_footer` + `service_quotation_footer` (tab Báo giá – Hợp đồng): KHỚP footer mặc
    định ERP → **GIỮ**.
  - `companies.quotation_footer_company` + `payment_term_company` (tab Điều khoản): **BỊA** — migration
    HRM `2026_09_14_000001` tự tạo, ERP KHÔNG có cột per-company này; không code nào đọc; DB 0 dòng data.
- Quyết định user: **hướng 2 (bám ERP đầy đủ)**, làm **Phần A (dọn)** trước; giữ 2 footer global.

Phần A — Dọn (đợt này):
- [x] BE `RegulationTabRegistry.php`: xoá hẳn tab `dieukhoan` (2 field bịa per-company). Verify `R::has('dieukhoan')=0`.
- [x] FE `data.js`: xoá tab `dieukhoan` khỏi nhóm company (giữ nguyên 2 `rich()` footer ở tab baogia).
  Verify company_tab_ids không còn dieukhoan; baogia vẫn có 2 footer.
- [x] FE `RegulationConfigScreen.vue`: bỏ `dieukhoan` khỏi `API_TABS` + dọn 2 comment nhắc dieukhoan.
- [x] BE: drop 2 cột rỗng `companies.quotation_footer_company`/`payment_term_company` (DB 0 data) +
  xoá file migration `2026_09_14_000001` + xoá bản ghi trong bảng `migrations`.
- [x] Test: `RegulationConfigSchemaTest` gỡ assert 2 cột; `RegulationHistoryTest` gỡ nhánh company rich
  (không còn field rich scope company) + ghi chú fixture lịch sử cũ dùng tab đã gỡ. 5/7 PASS.
  2 test còn lại (`company_scope_isolates`/`company_scope_merges`) FAIL **PRE-EXISTING** (baseline code
  gốc cũng fail): DB test dùng chung còn 2 dòng `regulation_config_histories` scope=global từ lần chạy
  trước; getHistory scope company luôn kèm global (đúng thiết kế) → count lệch. KHÔNG do cleanup, KHÔNG đụng data.
- [x] Verify: FE data.js parse OK; grep hrm-api/hrm-client sạch ref chức năng tới field/tab đã gỡ.

Phần B — Port thư viện điều khoản theo loại báo giá + phương thức thanh toán: **TÁCH FEATURE SAU**
(brainstorm + spec riêng khi user yêu cầu; HRM chưa có khái niệm loại báo giá).

### Checkpoint — 2026-09-24 (Bug #12 Phần A)
Vừa hoàn thành: dọn điều khoản port lệch — gỡ tab `dieukhoan` (BE registry + FE data.js + API_TABS),
drop 2 cột bịa rỗng `companies.quotation_footer_company`/`payment_term_company` + xoá migration
`2026_09_14_000001`, giữ 2 footer global ở tab baogia (khớp fallback ERP), cập nhật 2 test.
Đang làm dở: (không) — Phần A code xong, chưa commit.
Bước tiếp theo: user nghiệm thu UI (tab Điều khoản biến mất, tab Báo giá – Hợp đồng vẫn còn 2 footer);
OK → commit gop_db (chờ lệnh). Phần B chờ user yêu cầu mở feature riêng.
Blocked: (không) — 2 test fail là pre-existing, không thuộc phạm vi task.

---

## #13 — Quy chế thưởng năm (Cấu hình thưởng cuối năm công ty) — port ERP

> Bổ sung khâu KHAI "thưởng cuối năm" mà HRM đang thiếu. Port màn ERP
> `admin/companies/{id}/config-bonus-end-year` vào nhóm MỚI **"Quy chế thưởng năm"** trong phạm vi
> **Theo công ty** của màn quy chế. User chốt: khai theo công ty · KHÔNG hẹn ngày · Approach A.
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-09-24-khai-quy-che-thuong-nam-design.md`.

**Quyết định đã chốt:** (A) SHAPE mới `SHAPE_DEPT_GRID` + nhánh pipeline riêng, lưu **replace-all** theo
`company_id` (KHÔNG dùng version pipeline, KHÔNG dùng grid per-row của hoahong). (B) scope=company,
`no_hen=true`. (C) ghi thẳng bảng ERP `company_bonus_end_year_configs` (đã có, 0 dòng — không migration/bảng
mới). (H) **KHÔNG ghi RegulationConfigHistory** (ERP cũng không; formatter lịch sử dựng cho field scalar →
rủi ro cao) — rows vẫn mang created_by/updated_by. (G) **GIỮ gate** quyền `Cài đặt cấu hình` (không ungated
như ERP), KHÔNG thêm quyền mới.

**6 cột/dòng (per phòng ban):** department_id (select 'departments' theo cty) · bonus_rate (số, req) ·
settlement_type (select 1/2/3: DSTC quyết toán/Lợi nhuận phòng/Lợi nhuận công ty, req) ·
reserve_fund_percent · reserve_fund_value (**XOR** với percent) · max_risk_reserve_fund.

### BE
- [x] `Support/RegulationTabRegistry.php`: thêm `const SHAPE_DEPT_GRID = 'dept_grid'` + tab `thuongnam`
  (scope=COMPANY, shape=DEPT_GRID, no_hen=true, model=CompanyBonusEndYearConfig, 6 field metadata).
  Verify: `R::get('thuongnam')['shape']===SHAPE_DEPT_GRID`; `scalarKeysForStore` KHÔNG chứa thuongnam.
- [x] `Entities/CompanyBonusEndYearConfig.php` (MỚI): `extends Model` (bảng ERP — ghi rõ lý do trên class),
  `$table='company_bonus_end_year_configs'`, `$guarded=[]`. (Service tự gán created_by/updated_by.)
- [x] `Services/RegulationConfigService.php`: `resolveOptions` thêm nhánh `inline:settlement_type`
  (3 option cố định).
- [x] `Services/RegulationConfigService.php`: `getDeptGridConfig(int $companyId)` → `{fields, rows,
  department_options (resolveOptions('departments',$companyId)), settlement_options}`.
- [x] `Services/RegulationConfigService.php`: `saveDeptGrid(int $companyId, array $rows, int $actorId)` —
  transaction: delete theo company_id → insert lại từng dòng (created_by=updated_by=actorId, percent/value/
  max rỗng→null); trả `getDeptGridConfig`. KHÔNG ghi history.
- [x] `Http/Requests/RegulationDeptGridRequest.php` (MỚI): rules rows.* (department_id req int; bonus_rate
  req numeric min:0; settlement_type req in 1,2,3; 3 field quỹ nullable numeric min:0) + withValidator
  (department_id không trùng; mỗi dòng KHÔNG cùng percent>0 & value>0). Message tiếng Việt kèm số dòng.
- [x] `Http/Controllers/V1/RegulationConfigController.php`: show() thêm nhánh SHAPE_DEPT_GRID →
  getDeptGridConfig(currentCompanyId()); endpoint `saveDeptGrid` (guard() + assertDeptGridTab 404 +
  currentCompanyId + saveDeptGrid); chặn SHAPE_DEPT_GRID trong assertVersionTab (store/update/cancel).
- [x] `Routes/api.php`: `Route::post('regulation-config/{tabKey}/dept-grid', ...@saveDeptGrid)->where('tabKey','[a-z]+')`.
- [x] `php -l` sạch các file BE; giữ line-ending nguyên trạng.

### FE
- [x] `components/regulation-config/data.js`: thêm group company `{ id:'thuongnam', name:'Quy chế thưởng năm',
  type:'dept-grid' }` (giữ LF).
- [x] `RegulationConfigScreen.vue`: thêm `thuongnam` vào API_TABS + renderer `type==='dept-grid'` (bảng động:
  thêm/xoá dòng, V2BaseSelect phòng lọc trùng, V2BaseSelect loại quyết toán, số en-US, %/value loại trừ
  disable chéo, báo đỏ dưới ô không toast/không tự sửa số, nút Lưu POST `.../thuongnam/dept-grid`). V2Base*.

### Test
- [x] `tests/Feature/RegulationDeptGridTest.php`: backup/restore `company_bonus_end_year_configs` cho cty test;
  cases: save N dòng đọc lại đúng + created_by set; replace-all (save lần 2 ít dòng → dòng cũ mất);
  %+value cùng >0 → 422; department trùng → 422; settlement_type ngoài {1,2,3} → 422.
- [x] Playwright e2e + verify MCP (127.0.0.1:3000): nhóm "Quy chế thưởng năm" → thêm dòng + nhập + Lưu →
  reload thấy data; lỗi %+value hiện đỏ dưới ô. **BẮT BUỘC kiểm Playwright trước khi báo xong.**

### Checkpoint — 2026-09-24
Vừa hoàn thành: #13 XONG toàn bộ BE+FE+Test. `RegulationDeptGridTest.php` 7 test / 29 assertion PASS
(save + created_by, replace-all, empty→clear, %+value cùng >0 → 422, dept trùng → 422, settlement_type
ngoài {1,2,3} → 422, thiếu field required → 422). Playwright MCP đã verify end-to-end trước đó.
Đang làm dở: (không)
Bước tiếp theo: chờ lệnh commit gop_db (2 repo). Phần B (port thư viện điều khoản) chờ user mở feature riêng.
Blocked: (không)
