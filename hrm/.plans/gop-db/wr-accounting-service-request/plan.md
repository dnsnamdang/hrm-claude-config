# Yêu cầu hạch toán dịch vụ HDDV — Implementation Plan

> @dangquang · nhánh `develop` (con `gop_db`, KHÔNG tạo nhánh mới, KHÔNG commit — user tự commit)
> Spec: `docs/superpowers/specs/gop-db/2026-10-30-wr-accounting-service-request-design.md` (đọc trước mọi task).
> Khuôn: `buy-service-accounting-request` (BE `Modules/Finance`, FE `pages/finance/buy-service-accounting-requests`).

**Goal:** Port màn ERP "Yêu cầu hạch toán dịch vụ - HDDV" (phía BÁN) sang HRM
`/finance/wr-accounting-service-requests`, bám ERP 1:1, UI chuẩn HRM, link màn chưa-port để trống.

**Tech:** PHP 7.4 / Laravel 8 / nwidart modules · Nuxt 2.14 / Vue 2 / Bootstrap-Vue · MySQL `gop_db`.

## Global Constraints
- Không migration (bảng ERP). Không `mysql2`. Không commit/push.
- Quyền mới guard `api`, `type 23`, group `Yêu cầu hạch toán dịch vụ HDDV` — chỉ sửa `PermissionsTableSeeder`.
- BE tự tính total_cost/cost rows từ HĐ, không tin payload client (chỉ nhận status + comment).
- Nhãn "Người tạo / Ngày tạo". Ngày BE `d/m/Y H:i`. Số `1,234,567.89`. Ô rỗng để trống. "Đang tạo" xám.
- Toast QLDA chuẩn (dấu chấm cuối). 409 "Trạng thái đã bị thay đổi. Vui lòng load lại trang".
- Link màn chưa-port (Số hợp đồng, Hạch toán chi phí) = placeholder vô hiệu.
- Skill đọc khi tới phần: `erp-to-hrm-screen`, `list-page`, `button-convention`, `modal-popup`,
  `form-validate`, `unsaved-changes`, `entity-history`, `export-excel`, `notification-convention`.
- Verify BE bằng HTTP kernel trong tinker; FE bằng compile. User tự bấm trình duyệt.

## Review Focus
1. Người không phải người tạo gọi PUT/DELETE trực tiếp → 403; phiếu đã sang Chờ duyệt → 409.
2. Kế toán khác công ty → không thấy phiếu công ty khác, không có nút Hạch toán/Không duyệt.
3. BE tính lại chi phí từ HĐ: client gửi total_cost sai → BE bỏ qua, ghi theo HĐ.
4. `company_id = null` không kéo phiếu rác; super admin không bị bó công ty.
5. Trừ phụ lục PL_GIAM đúng khi lấy chi phí từ HĐ.

## Phase 0 — Khảo sát + design (DONE 30/10)
- [x] Khảo sát ERP (controller/model/view/JS/export/WrServiceContract) + HRM state (Explore) + DB gộp.
- [x] Chốt điểm mở (call của tôi, user "làm đi"): 1 loại, 3 cấp quyền + Hạch toán, Bán hàng chính,
      link chưa-port để trống, tạo từ HĐ qua URL, không migration.
- [x] Fill spec + design.md + plan.md + STATUS.

## Phase 1 — BE nền: quyền + Entity ✅ DONE 30/10
### Task 1: Quyền + 2 Entity ✅
- [x] Thêm 4 dòng `$this->perm([...])` (type 23, group 'Yêu cầu hạch toán dịch vụ HDDV') sau cụm
      'Hạch toán mua dịch vụ' trong `PermissionsTableSeeder.php` (dry-run thấy 4 Thêm); insert tinker
      firstOrCreate guard api → id 101422-101425.
- [x] `Modules/Finance/Entities/WrAccountingServiceRequest/WrAccountingServiceRequest.php`:
      $table, $guarded=['id'], $casts total_service/total_cost=>array; consts DA_DUYET=1/CHO_DUYET=2/
      DANG_TAO=3 + COST_ID_DELIVERY=5, STATUSES (Đang tạo=draft #64748B), SORTABLE_COLUMNS, PERMISSION_*;
      quan hệ costs/customer/approver/employee_create/wrServiceContract(CustomerCare rich)/company/department;
      generateCode('.YCHTDV.'), canView/canEdit/canDelete/canAccounting, isBigBoss/isBoss/isManager/
      hasAccountingPermission, searchByFilter (preset all + mặc định), applyFilters/applySort.
- [x] `.../WrAccountingServiceRequestCost.php` ($table, $fillable khớp cột thật `discount_value`, quan hệ request/cost).
- [x] **Verify** tinker (auth setUser TpEmployee SA id13): searchByFilter all = **873** = raw 877 − 4 draft
      người khác (đúng); first()->canView() true; casts total_cost=array; costs=5; contractCode ra mã HĐ;
      **negative** emp24 canView(draft người khác) = false. `customer_name` lưu sẵn trên phiếu (dùng cột này
      hiển thị — quan hệ `customer`.name NULL, bẫy bảng customers ERP).

## Phase 2 — BE nghiệp vụ
### Task 2: Service đọc + nguồn tạo + Resource ✅ DONE 30/10
- [x] `Modules/Finance/Services/WrAccountingServiceRequestService.php` (read-only, CHƯA trait/constructor
      — write ở Task 3): `searchByFilter(Request)`, `meta()`, `exportRows`, `findForShow`,
      `detailData(model)` (cột spec §7 + cờ is_can_edit/delete/accounting + placeholder HĐ + costs tách
      other/delivery + total_cost), `contractData(int)` → `buildCostsFromContract(int)` **hàm duy nhất**
      dựng chi phí: load HĐ+costs, trừ PL_GIAM (type 4, query thẳng parent_id), map cost_name cứng
      COST_NAMES (cost_id KHÔNG join costs — ids 1..5 là phí logistics), VAT 8%, tách delivery(5)/other,
      total_cost (key `discount`). Helper `sumGroup/splitCostRows/costRow/normalizeTotalCost/customerLabel`.
- [x] `Transformers/WrAccountingServiceRequestResource/WrAccountingServiceRequestListResource.php`
      (STT FE · Ngày tạo · Số phiếu · Số hợp đồng · Khách hàng mã-tên · Người tạo · Người duyệt ·
      Ngày duyệt · Trạng thái + cờ is_can_*).
- [x] **Verify** tinker (SA id13): `contractData(19)` KHỚP tính tay — cost1 2,250,000→vat 180,000→
      2,430,000; cost5 15,000,000+4,802,400=19,802,400→vat 1,584,192→21,386,592; total 2 nhóm đúng;
      `detailData(882)` costs 4/1, cờ fail-closed false; list total **873** = Phase 1; exportRows 873.
- [x] **Fix bug Phase 1**: gỡ eager-load chết `wrServiceContract.employee_create.info` trong
      `searchByFilter()` (HĐ CustomerCare có `creator()` chứ không `employee_create`) → RelationNotFound.

### Task 3: Service ghi + Notify + lịch sử ✅ DONE 30/10
- [x] store(array): DB::transaction — đọc HĐ, **tính lại** chi phí/total_cost (không tin client),
      assertContractAccountable (port canAccountingCost), lưu phiếu (status client in WRITABLE=[2];
      company/dept từ info), syncCosts (xoá+insert), generateCode sau insert, log 'create',
      afterSentForApproval (notify quyền 'Hạch toán dịch vụ HDDV' cùng công ty) nếu status=2.
- [x] update(model, array): lockForUpdate, snapshot before, rebuild từ HĐ (bỏ qua total_cost client),
      syncCosts, logUpdateWithRows + logStatusChange. (409/403 gate ở controller.)
- [x] reject(model, comment): lockForUpdate + recheck isWaitingAccounting (else null→409), status→3
      (DANG_TAO) + approver_id + approved_at + comment, logStatusChange, afterCommit onRejected notify.
- [x] destroy(model): log 'delete' trong transaction → xoá costs + phiếu.
- [x] `WrAccountingServiceRequestNotifyService.php` (khuôn BuyServiceAccountingRequestNotifyService):
      PREFIX='YCHTDV', onSentToAccountant/onRejected, try/catch không rollback.
- [x] `app/Services/CatalogHistoryService.php`: TABLES['wr_accounting_service_requests'] — dùng
      endpoint CHUNG `catalog-histories/{table}/{id}` (bảng trong TABLES, không gate canView), giống
      màn anh em `buy_service_accounting_requests`. **Lệch plan gốc** (dự định route riêng `/histories/{id}`)
      — chọn theo sibling cho nhất quán + ít code. Cột bảng là `table_name` (KHÔNG phải `table`).
- [x] **Verify** tinker (SA id13, HĐ 47): STORE code `TPE.YCHTDV.2026000883` status 2, 5 costs,
      other_cost price_after_vat=270000, 1 history 'create' → UPDATE (client total_cost rác bị bỏ, BE
      ghi 270000, +1 history) → REJECT (status→3, approver=13, approved_at, +1 'change_status') →
      DESTROY (phiếu+costs sạch) → dọn history. Phiếu 883 sạch.

### Task 4: FormRequest + Controller + Route + Export ✅ DONE 30/10
- [x] `Http/Requests/WrAccountingServiceRequest/WrAccountingServiceRequestStoreRequest.php`
      (`wr_service_contract_id` required khi tạo / nullable khi sửa (khoá HĐ), `status required|integer|Rule::in(WRITABLE_STATUSES)`,
      `comment nullable|string|max:1000`); chỉ `rules()`+`attributes()`, KHÔNG `messages()`.
- [x] `.../WrAccountingServiceRequestRejectRequest.php` (`comment required|string|max:1000`).
- [x] `Http/Controllers/V1/WrAccountingServiceRequestController.php` (khuôn Buy...; 409 trước 403;
      reject: isWaitingAccounting else 409, canAccounting else 403, service->reject null→409).
      KHÔNG có method histories (dùng endpoint chung). Service thêm public `findOrFail(int)` cho update/destroy/reject.
- [x] `Modules/Finance/Routes/api.php`: group `/wr-accounting-service-requests` (8 route tĩnh trước `/{id}`;
      reject `->middleware('checkPermission:Hạch toán dịch vụ HDDV')`). Sau khối buy-service-accountings.
- [x] `app/ExcelExport/ExportColumnRegistry.php`: key `wr_accounting_service_requests` (Số phiếu,
      Số hợp đồng, Khách hàng, Ngày tạo, Người tạo, Ngày duyệt, Người duyệt, Công ty, Trạng thái).
- [x] **Verify**: `php -l` sạch 3 file mới; 8 route confirmed qua `app('router')->getRoutes()`
      (route tĩnh trước `/{id}`, reject có middleware). `route:list` crash sẵn do route Rice hỏng, không liên quan.

### Task 5: Smoke test BE (tinker HTTP kernel) ✅ DONE 30/10
- [x] INDEX `?type=all` SA id13 → total=873, is_all_company=true, 3 statuses.
- [x] CONTRACT-DATA HĐ 47 → code/customer/total khớp (other_after_vat=270000).
- [x] STORE qua FormRequest → 200 id=884, status Chờ duyệt. (đường tính lại/bỏ total_cost client đã verify ở Task 3.)
- [x] SHOW phiếu 884 → status "Chờ duyệt", is_can_edit=false, is_can_accounting=false (fail-closed đúng).
- [x] REJECT SA id13 → 403 (SA KHÔNG có shortcut; canAccounting cần quyền 'Hạch toán dịch vụ HDDV' —
      khớp sibling Buy + middleware CheckPermission cũng không bypass SA → nhất quán, KHÔNG bug).
- [x] DESTROY phiếu 884 (Chờ duyệt) → 409 (không phải nháp — đúng).
- [x] Dọn phiếu test 883/884 + catalog_histories qua Service::destroy() trực tiếp; đếm lại = sạch.

## Phase 3 — FE
Đọc skill `erp-to-hrm-screen` (A–H), `list-page`, `button-convention`, `modal-popup`, `form-validate`,
`unsaved-changes`, `entity-history` trước khi code.
### Task 6: Danh sách
- [ ] `pages/finance/wr-accounting-service-requests/index.vue` (khuôn buy-service-accounting-requests):
      4 mixin, columnScreenKey `wr_accounting_service_requests`, cột/lọc/hành động spec §7.1,
      Số hợp đồng = placeholder vô hiệu, Hạch toán chi phí = placeholder. Xuất Excel + Cấu hình cột + Lịch sử.
### Task 7: Form + bảng chi phí
- [ ] `components/WrAccountingServiceRequestForm.vue` + `components/ServiceCostTable.vue` (2 card chi phí
      other/delivery, chỉ-đọc, ẩn khi tổng ≤ 0). CreatorInfoLine, Ghi chú duyệt, footer nút spec §7.2.
### Task 8: Tạo / Sửa / Chi tiết + menu
- [ ] `create.vue` (đọc `$route.query.wr_service_contract_id` → GET contract-data; không có id → thông
      báo "Phiếu tạo từ hợp đồng dịch vụ" + nút Quay lại), `_id/edit.vue`, `_id/index.vue` (footer theo cờ BE;
      404 → /pages/extras/404).
- [ ] `hrm-client/components/subsystem-menu/finance.js:308` → `link: '/finance/wr-accounting-service-requests?type=all'`.
- [ ] `hrm-client/components/subsystem-menu/sale-hub.js` (~190): gán link cho 'YC hạch toán dịch vụ - HDDV'.
### Task 9: Verify FE
- [ ] Compile các .vue mới (vue-template-compiler + babel) — 0 lỗi.
- [ ] Grep checklist cuối skill `erp-to-hrm-screen` trên thư mục feature — sạch.
- [ ] Báo user các bước bấm thử trình duyệt.

## Phase 4 — Wrap up
- [ ] Cập nhật plan checkpoint + STATUS gop-db.
