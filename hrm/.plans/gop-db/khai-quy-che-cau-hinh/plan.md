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
