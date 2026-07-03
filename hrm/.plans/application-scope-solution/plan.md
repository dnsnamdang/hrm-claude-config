# Plan — application-scope-solution

> Thực thi subagent-driven (Opus). Spec: `docs/superpowers/specs/2026-06-25-application-scope-solution-design.md`
> Phụ trách: @manhcuong. HRM-only (Assign), KHÔNG ERP. Verify browser cuối mỗi phase. KHÔNG commit/git. Branch hrm-api/hrm-client = tpe-develop-assign.

**Ràng buộc chung:** Thuật ngữ: scopes=Nhóm ngành(cha), industries=Nhóm giải pháp(con) qua `industry_scopes`; customer_scope_groups=Loại hình(cha), customer_scopes=Lĩnh vực(con) qua `customer_scope_group_members`. Lưu theo CẶP. Payload: `industry_pairs` [{scope_id, industry_id}] + `customer_scope_pairs` [{customer_scope_group_id, customer_scope_id}]. Lĩnh vực bắt buộc trên FORM, KHÔNG bắt buộc khi IMPORT. Validate cha-con tồn tại trong catalog; rethrow ValidationException; FE lỗi inline is-invalid/invalid-feedback/touched. Format hiển thị "Cha : Con", nhiều cặp cách `,`. Mã tra theo code (không hard-code prefix). KHÔNG sửa CustomerForm.vue.

---

## Phase 1 — DB (hrm-api Modules/Assign/Database/Migrations)

- [x] BE: Migration thêm `scope_id` (nullable) vào `application_industries` + drop unique cũ app_industries_unique + unique mới app_ind_scope_unique — 2026_06_26_000001
- [x] BE: Migration backfill scope_id = cha đầu qua industry_scopes (idempotent, industry không cha→null) — 2026_06_26_000002
- [x] BE: Migration thêm `customer_scope_group_id` (nullable) vào `application_customer_scopes` + unique app_cs_group_unique — 2026_06_26_000003
- [ ] Verify (USER): migrate, đối soát application_industries có scope_id; pivot customer rỗng

## Phase 2 — BE core (hrm-api Modules/Assign)

- [x] BE: `Applications.php` industryPairs()/customerScopePairs()/customerScopes()
- [x] BE: `ApplicationsRequest` rule industry_pairs + customer_scope_pairs (closure cha-con), message VN
- [x] BE: `ApplicationService.updateOrCreate` sync 3 pivot theo cặp (controller bọc DB::transaction); bỏ auto-derive
- [x] BE: `ApplicationService.index` filter customer_scope_group_id + customer_scope_id (whereExists)
- [x] BE: `ApplicationsResource` emit industry_pairs/_label, customer_scope_pairs/_label, customer_scope_group_names; giữ scope_names
- [x] BE: `DetailApplicationsResource` industry_pairs+customer_scope_pairs; getAll eager customerScopes
- [ ] Verify (USER): tạo-sửa Ứng dụng với cặp → 3 pivot đúng; validate chặn cặp sai; filter Loại hình/Lĩnh vực. (Minor: list N+1 pairs — màn catalog, chấp nhận)

## Phase 3 — BE import/export (hrm-api Modules/Assign)

- [x] BE: Import parse cặp (catCode=scopeCode:industryCode + customerScopeCode=groupCode:scopeCode optional) → tra code→id + validate cha-con, lưu qua syncApplicationPairs (transaction); controller thêm rule customerScopeCode
- [x] BE: Export blade 17 cột (header VN khớp mẫu, distinct cha + map cặp Mã/Tên) từ industry_pairs/customer_scope_pairs
- [ ] Verify (USER): export 17 cột + format cặp; import file mẫu cặp → DB đúng. (Lưu ý: validate chỉ chấp catalog ACTIVE)

## Phase 4 — FE component dùng chung (hrm-client)

- [x] FE: Tạo `components/assign-components/CascadeTreeSelect.vue` (port .csp-→.cts- từ CustomerForm B): props value(cặp parent_id/child_id)/parentOptions/childOptions(parent_ids)/label/tooltip/placeholder/readonly/required/error; emit input; chip Cha:Con, tree, search, chọn/xóa tất cả, click-outside. compile+babel OK
- [x] Verify: compile sạch (verify UI ở Phase 5)

## Phase 5 — FE form (hrm-client)

- [x] FE: `application-modal.vue` "Nhóm giải pháp" → CascadeTreeSelect (data.industry_tree)
- [x] FE: thêm "Lĩnh vực kinh doanh khách hàng" → CascadeTreeSelect (data.customer_scope_tree), bắt buộc inline
- [x] FE: buildPayload map tree→industry_pairs/customer_scope_pairs; loadDetail map pairs→tree; ensureOptionsLoaded fetch đủ 4 (getter trả `text`→map name)
- [ ] Verify browser (USER): tạo/sửa/xem Ứng dụng — 2 tree chọn cặp, chip Cha:Con, lưu+load đúng. (compile OK)

## Phase 6 — FE list/filter/import (hrm-client)

- [x] FE: `index.vue` cột Nhóm giải pháp→industry_pair_label + thêm cột Loại hình (customer_scope_group_names) + Lĩnh vực (customer_scope_pair_label)
- [x] FE: 2 filter Loại hình + Lĩnh vực (V2BaseSelect, cascade, auto-search deep watcher, export truyền param)
- [x] FE: import config (catCode=cặp + customerScopeCode optional) + template Mau_Import_UngDung_FN.xlsx regenerate (openpyxl)
- [ ] Verify browser (USER): list 3 cột cặp/distinct; 2 filter; import/export end-to-end (compile OK)

## Phase 7 — Verify end-to-end

- [ ] Verify (USER + Playwright nếu được): tạo Ứng dụng có nhiều cặp 2 quan hệ → list/detail/export khớp; import file mẫu → DB đúng; filter chính xác; AC đầy đủ

---

### Bổ sung — 2 trường cha (Nhóm ngành / Loại hình) trên form + CSS center/height — 2026-06-25
- User yêu cầu thêm trường CHA riêng cho mỗi quan hệ trên popup Ứng dụng, map cặp cha-con giống /assign/customers/add. Chốt: cha = UI filter/hiển thị, SUY TỪ con (KHÔNG lưu độc lập, KHÔNG đổi BE/DB). Tách component dùng chung `components/assign-components/CascadePairSelect.vue` (field cha multi-select + field con tree, cross-map port từ CustomerForm: explicitParents lọc con, tick con fill cha không lock, tick cha trực tiếp=explicit+cascade bỏ pairs khi bỏ cha). v-model = mảng cặp {parent_id, child_id}; payload/loadDetail/buildPayload + BE GIỮ NGUYÊN. Thay 2 CascadeTreeSelect trong application-modal bằng 2 CascadePairSelect (Nhóm ngành+Nhóm giải pháp; Loại hình+Lĩnh vực). Compile PASS. FE-only.
- Fix CSS placeholder/height: CascadeTreeSelect `.cts-*` + ERP scopeFieldA/B `.escp-*` + CascadePairSelect `.cps-*`: align-items center (placeholder căn giữa), HRM min-height 34 (=V2BaseInput md), ERP giữ 38 (=Bootstrap form-control), box-sizing border-box, placeholder 13px/line-height 1.4, caret align-self center. (Playwright verify bị chặn do dev server :3000 load SPA chậm/timeout headless lần này — xác minh qua source; chờ user hard-refresh confirm.)

### Layout + height fix (verified Playwright) — 2026-06-25
- CascadePairSelect: `.cps-wrap` flex row → field cha + con CÙNG 1 HÀNG (col 50/50). application-modal reorder: Mã|Tên → Trạng thái (dưới Tên) → (Nhóm ngành|Nhóm giải pháp) → (Loại hình|Lĩnh vực) → Mô tả.
- Height: cps/cts min-height 34→32 = V2BaseInput trong modal (đo Playwright: cps=32=v2input=32, align center, placeholder 13px). ERP escp giữ 38 (Bootstrap form-control).
- VERIFIED Playwright (login namdangit, /assign/application modal): layout đúng + height khớp + placeholder căn giữa. Migration đã chạy (list 4 cột hiển thị).

### Checkpoint — 2026-06-25
Vừa hoàn thành: CODE DONE Phase 1-6 (subagent-driven Opus, final whole-branch review PASS READY không Critical/Important). BE: 3 migration (scope_id→application_industries + backfill, customer_scope_group_id→application_customer_scopes) + entity pairs + request validate cặp + service sync 3 pivot/filter + resources (industry_pairs/_label, customer_scope_pairs/_label, customer_scope_group_names) + import parse cặp + export 17 cột. FE: CascadeTreeSelect.vue (component mới) + application-modal (2 tree chọn cặp) + index.vue (3 cột + 2 filter + import config) + template xlsx. Compile/lint sạch.
Bước tiếp theo (USER): (1) chạy 3 migration `Modules/Assign/Database/Migrations/2026_06_26_000001/2/3`; (2) verify browser /assign/application. LƯU Ý: list/export gọi industryPairs() join scope_id → PHẢI chạy migration trước.
Blocked: chờ user chạy migration + verify.
Minor (final review): N+1 list/export; show() eager thiếu customerScopes (không bug). KHÔNG commit/git.
