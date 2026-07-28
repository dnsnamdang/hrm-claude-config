# Plan — Human customer scope: single → multi-select (như Assign) bằng CascadePairSelect

Người phụ trách: @manhcuong

Đổi form Khách hàng HRM Human (/human/customers) chọn 2 trường "Loại hình hoạt động khách hàng" + "Lĩnh vực kinh doanh khách hàng" từ single-select sang multi-select cascade GIỐNG Assign, dùng component `CascadePairSelect`. Model đổi scalar → mảng (customer_scope_group_ids + customer_business_fields cặp).

## Phase 1 — Component dùng chung (additive) ✅
- [x] CascadePairSelect.vue: thêm prop `parents` (Array) + watch sync `explicitParents` (guard chống loop) để prefill Loại hình chọn riêng. Giữ emit `parents-change`. Không ảnh hưởng popup/filter (default []).

## Phase 2 — FE Human (CustomerForm.vue) ✅
- [x] Bỏ import/register/usage `CustomerScopeSelect`; thêm `CascadePairSelect`
- [x] data.form: bỏ scalar → thêm `customer_scope_group_ids: []` + `customer_business_fields: []`
- [x] data `listScopeGroups`/`listScopes`; methods `loadScopeGroups`/`loadScopes` (assign/customer-scope-groups|scopes/getAll, map parent_ids từ customer_scope_group_ids/groups)
- [x] computed `scopeParentOptions`/`scopeChildOptions`/`scopePairsModel` (get/set map business_fields ↔ {parent_id,child_id})
- [x] mounted: load 2 catalog; edit `normalizeScopeFields()`
- [x] template: CascadePairSelect (labels đúng, :parents + @parents-change, v-model scopePairsModel, :readonly isShow)
- [x] BONUS (user): đưa trường "Mã" ngang hàng với Khách hàng + Loại hình tổ chức (3 col-xl-4 cùng 1 row, scope full-width dưới)

## Phase 3 — BE Human ✅
- [x] SaveCustomerRequest + UpdateCustomerRequest: rule scalar → mảng (customer_scope_group_ids array + customer_business_fields.* cặp + closure belongs, nullable); đổi messages
- [x] Service `syncCustomerScopes`: nhận mảng, ghi N activity_types + N business_fields (dedup, delete+insert); GỌI thêm trong updateCustomer
- [x] `show()`: trả thêm customer_scope_group_ids (=activityTypeIds()) + customer_business_fields (=businessFieldPairs())

## Phase 4 — Verify ✅
- [x] php -l sạch 3 BE; FE compile OK
- [x] Playwright form add: CascadePairSelect render (nhãn đúng), options load từ API, cascade tick "Điện-điện tử"→Lĩnh vực thu hẹp→tick "Khác"→chip cha + "Cha : Con"; Mã cùng hàng Khách hàng+Loại hình tổ chức (top=182)
- [x] Tinker Human SaveCustomerRequest: cặp hợp lệ PASS, để trống PASS
- [ ] User E2E: tạo KH chọn nhiều Loại hình+Lĩnh vực → lưu → mở sửa prefill đúng (gồm Loại hình chọn riêng)

### Checkpoint — 2026-07-14
Vừa hoàn thành: Human customer scope single→multi (CascadePairSelect như Assign) + prop `parents` prefill + BE arrays + layout Mã. Verify Playwright + tinker.
Bước tiếp: User E2E tạo/sửa thực tế.
