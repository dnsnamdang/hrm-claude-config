# Hợp đồng (Sale Contract) — Implementation Plan

> **For agentic workers:** thực thi task-by-task (subagent-driven). Steps dùng checkbox `- [ ]`.

**Goal:** Hợp đồng lập từ báo giá đã duyệt (Modules/Sale), workflow giống báo giá, snapshot Bên A/B đầy đủ, mẫu in tuỳ chỉnh (tái dùng print_templates của Quyết định).

**Spec:** `docs/superpowers/specs/2026-06-27-contract-design.md` · **Design:** `.plans/contract/design.md`

## Global Constraints
- Trạng thái dùng lại bộ SaleQuotation (1 Nháp/2 Chờ duyệt/3 Đã duyệt/4 Từ chối); BE trả `status_name`+`status_color`, FE render `V2BaseBadge`.
- Validate: Request extend `BaseRequest`; FE lỗi inline (`is-invalid`/`invalid-feedback`/`touched`).
- Route thao tác gắn `checkPermission` nhóm "Hợp đồng"; route xem gắn quyền xem.
- Snapshot Bên A/B lưu trên hợp đồng (sửa được). Items + totals **khoá** (copy từ báo giá).
- 1 báo giá → tối đa 1 HĐ (`unique(quotation_id)` + check service). Chỉ created_by báo giá tạo được HĐ.
- Datetime list `d/m/Y H:i:s`, ngày `d/m/Y`. Cột bảng FE dùng `title:` (không `label:`).
- KHÔNG commit git. KHÔNG đọc vendor/, node_modules/. Verify `php artisan migrate`/`php -l`/tinker.

**Template để copy (đọc khi implement):**
- BE: `Modules/Sale/{Entities/SaleQuotation.php, Entities/SaleQuotationItem.php, Services/SaleQuotationService.php, Http/Requests/SaleQuotationRequest.php, Http/Controllers/Api/V1/QuotationController.php, Transformers/SaleQuotationResource/*, Routes/api.php}`; `app/Helper/FormatHelper.php` (`fillReport`/`clearNull`); `Modules/Human/Entities/PrintTemplateVariable.php`; `Modules/Decision/Services/Decision/DecisionService.php::setValuePrintDecision`.
- FE: `pages/sale/quotation/{index.vue,_id/index.vue,create.vue,_id/edit.vue}`, `components/sale/quotation/QuotationForm.vue`, `pages/decision/components/FormPrintTemplateComponent.vue`, `pages/decision/department-change/_id/print.vue`, `components/default-menu/sale.js`.

---

## Phase 1 — DB + Entities

### Task 1: Migrations
- [x] Tạo `Modules/Sale/Database/Migrations/2026_06_27_100001_create_sale_contracts_table.php` — đủ cột theo design (code/quotation_id unique/customer_id/contract_date/status/approved_at/by/snapshot a_*+b_*/discount+totals/print_template_id+type_id+print_template/terms/warranty_time/company_id/department_id/part_id/created_by/updated_by/timestamps).
- [x] Tạo `...100002_create_sale_contract_items_table.php` (contract_id FK cascade, product_id, unit_id, quantity, unit_price, vat_rate, line_amount, sort_order).
- [x] Tạo `...100003_add_bank_account_to_category_customers.php` (`bank_account` string nullable).
- [x] Tạo `...100004_add_bank_account_representative_to_companies.php` (`bank_account` + `representative` string nullable).
- [x] `php artisan migrate` → 4 Migrated; tinker kiểm 2 bảng + 3 cột tồn tại.

### Task 2: Entities
- [x] `Modules/Sale/Entities/SaleContract.php`: copy SaleQuotation (HasStatusBadge + const STATUSES/STATUS_*, getNextCode `HD-YYYY-NNNNN`, isCanEdit/Delete/Submit/Approve, accessor employee_create_name/employee_approve_name + relations items/quotation/customer/contact/createdByEmployee/approvedByEmployee). Fillable đủ field gồm snapshot + print_*.
- [x] `Modules/Sale/Entities/SaleContractItem.php`: copy SaleQuotationItem (table sale_contract_items, belongsTo contract/product/unit).
- [x] `php -l` OK.

## Phase 2 — BE CRUD + workflow + permission

### Task 3: Service `SaleContractService`
- [x] Copy `SaleQuotationService`. `getListForUser`: đổi permission sang nhóm "Hợp đồng" (Xem tất cả/công ty/phòng ban/bộ phận), eager-load customer/createdByEmployee.info/approvedByEmployee.info, trả query builder.
- [x] `createFromQuotation($quotationId)`: validate quote APPROVED + `created_by==auth()->id()` + chưa có contract (`SaleContract::where('quotation_id',$id)->exists()` false). Snapshot A từ `quotation->customer` (a_name=customer->name, a_tax_code, a_address, a_phone, a_email, a_bank_account=customer->bank_account, a_representative=optional(contact)->fullname). Snapshot B từ `Company::find(quotation->company_id)` (b_name/b_tax_code/b_address/b_phone/b_email/b_bank_account/b_representative). Copy items khoá + totals + discount + warranty + terms + price_tier_id + customer_id/contact_id. code=getNextCode, status=DRAFT, created_by/company_id/department_id/part_id từ auth. Trả contract.
- [x] `updateOrCreate($request)`: chỉ sửa contract_date, snapshot A/B, terms, print_template_id/type_id/print_template. KHÔNG đụng items/totals. Sửa → reset DRAFT.
- [x] `submit/approve/reject/destroy`: copy SaleQuotationService (approve set approved_at/by).
- [x] `php -l` OK.

### Task 4: Request + Resources
- [x] `SaleContractRequest` (extend BaseRequest): `contract_date` required|date, `a_name` required, `b_name` required, party fields nullable string, `print_template_id` nullable. messages tiếng Việt.
- [x] `Transformers/SaleContractResource/SaleContractResource.php` (list): id, code, customer_name, contract_date (d/m/Y), total_amount, status+status_name+status_color, employee_create_name, employee_approve_name, created_at/approved_at (d/m/Y H:i:s), is_can_*.
- [x] `DetailSaleContractResource.php`: thêm snapshot A/B đầy đủ, items (read-only), discount/totals, terms, warranty_time, print_template_id/type_id/print_template, rejected_reason, customer_name, approver name. `php -l` OK.

### Task 5: Controller + Routes + Permission
- [x] `SaleContractController`: index/show/createFromQuotation/updateOrCreate/update/submit/approve/reject/delete/print (copy QuotationController; `index` dùng `apiGetList(SaleContractResource::apiPaginate(...))`; `delete`/`approve` KHÔNG nuốt ValidationException; `print` trả `{template}` từ buildPrintData — phần print hoàn thiện ở Phase 3, tạm trả print_template thô).
- [x] Routes `/v1/sale/contracts/*` (giống quotations) + `POST /contracts/from-quotation/{quotationId}` + `GET /contracts/{id}/print`. checkPermission nhóm Hợp đồng (xem/quản lý/duyệt).
- [x] Permission seeder: thêm id 1115-1122 nhóm "Hợp đồng" type 4 (Xem tất cả/công ty/phòng ban/bộ phận, Thêm, Sửa, Xóa, Duyệt).
- [x] `php -l` OK (4/4 file). Route verify bằng grep: 10 route `/contracts` đúng vị trí. Seeder: 8 dòng id 1115-1122 đã thêm.

### Task 6: Móc tạo HĐ từ báo giá
- [x] `DetailSaleQuotationResource`: thêm `has_contract` (SaleContract tồn tại theo quotation_id) + `is_can_create_contract` (status==APPROVED && created_by==auth && !has_contract).

### Checkpoint — 2026-06-27
Vừa hoàn thành: Task 5 (SaleContractController + Routes + Permission seeder 1115-1122) + Task 6 (DetailSaleQuotationResource has_contract/is_can_create_contract)
Đang làm dở: không có
Bước tiếp theo: Task 7 — Phase 3 Mẫu in (PrintTemplateVariable type Hợp đồng + biến)
Blocked: không có

### Checkpoint — 2026-06-27 (Task 7+8)
Vừa hoàn thành: Task 7 (PrintTemplateVariable::HOP_DONG_KINH_TE=7 + GROUP_BEN_A/B + 20 biến) + Task 8 (SaleContractService::buildPrintData + SaleContractController::print dùng service)
Đang làm dở: không có
Bước tiếp theo: Task 9 — Phase 4 Frontend (Menu + List page hợp đồng)
Blocked: không có

## Phase 3 — Mẫu in

### Task 7: Type + biến Hợp đồng
- [x] `PrintTemplateVariable`: thêm const type Hợp đồng (id trống kế tiếp) + entries `PRINT_TEMPLATE_VARIABLES` (nhóm Thông tin chung [SO_HOP_DONG, NGAY_HOP_DONG], Bên A [TEN_BEN_A/MST_BEN_A/DIA_CHI_BEN_A/STK_BEN_A/DAI_DIEN_BEN_A/EMAIL_BEN_A/SDT_BEN_A], Bên B [*_BEN_B], Thanh toán [BANG_HANG_HOA, TONG_TIEN, TONG_TIEN_CHU, BAO_HANH]). Verify `get-types`/`get-variables` trả type mới.

### Task 8: buildPrintData + /print
- [x] `SaleContractService::buildPrintData(SaleContract $c)`: map scalar (SO_HOP_DONG=code, NGAY_HOP_DONG=contract_date format VI, TEN_BEN_A..a_*, TEN_BEN_B..b_*, TONG_TIEN, TONG_TIEN_CHU [đọc số thành chữ — dùng helper sẵn có nếu có, else format tiền], BAO_HANH) + sinh HTML bảng hàng hoá `BANG_HANG_HOA` (STT/tên SP/ĐVT/SL/đơn giá/thành tiền + dòng tổng). Render `fillReport($c->print_template, $data)`.
- [x] Controller `print($id)`: `return responseJson('success', 200, ['template' => $service->buildPrintData($contract)])`. `php -l` + tinker render mẫu test.

## Phase 4 — Frontend

### Task 9: Menu + List
- [x] `components/default-menu/sale.js`: thêm item "Hợp đồng" (icon, isShow:true, link `/sale/contract`).
- [x] `pages/sale/contract/index.vue` (copy quotation list): cột Mã HĐ/Khách hàng/Ngày HĐ/Tổng tiền/Trạng thái/Ngày tạo/Người tạo/Ngày duyệt/Người duyệt/Thao tác (dùng `title:`), filter keyword+status, layout default-sidebar, store calls `sale/contracts`.
- [x] `store/sale-contract.js`: namespace `sale-contract`, actions list/detail/update/submit/approve/reject/createFromQuotation.

### Checkpoint — 2026-06-27 (Task 9)
Vừa hoàn thành: Task 9 (Menu sale.js + store/sale-contract.js + pages/sale/contract/index.vue)
Đang làm dở: không có
Bước tiếp theo: Task 10 — Detail page + ContractForm + edit/print pages
Blocked: không có

### Task 10: Detail + Form + Print
- [x] `pages/sale/contract/_id/index.vue` (detail): khối Bên A/Bên B đầy đủ, bảng hàng hoá read-only, totals, footer V2Footer (Sửa/Gửi duyệt/Duyệt/Từ chối/In/Quay lại theo is_can_* + quyền Duyệt hợp đồng).
- [x] `components/sale/contract/ContractForm.vue` (sửa): contract_date, khối Bên A + Bên B (input đầy đủ, pre-fill snapshot), terms editor, **nhúng FormPrintTemplateComponent** (type Hợp đồng), bảng hàng hoá read-only. Footer Lưu / Lưu & Gửi duyệt. Validate inline.
- [x] `pages/sale/contract/_id/edit.vue` (wrap ContractForm) + (KHÔNG có create.vue — HĐ tạo từ báo giá rồi điều hướng sang edit).
- [x] `pages/sale/contract/_id/print.vue` (copy decision print): gọi `GET sale/contracts/{id}/print` → v-html.
- [x] FormPrintTemplateComponent: import trực tiếp từ `@/pages/decision/components/FormPrintTemplateComponent.vue`.
- [x] Modal SubmitModal + RejectModal riêng cho contract (`components/sale/contract/SubmitModal.vue`, `RejectModal.vue`).

### Checkpoint — 2026-06-27 (Task 10)
Vừa hoàn thành: Task 10 — Detail page + ContractForm + edit/print + SubmitModal + RejectModal
Đang làm dở: không có
Bước tiếp theo: Task 11 — Nút "Tạo hợp đồng" trên màn detail báo giá
Blocked: không có

### Checkpoint — 2026-06-27 (Task 11)
Vừa hoàn thành: Task 11 — Nút "Tạo hợp đồng" trong footer trang detail báo giá
Đang làm dở: không có
Bước tiếp theo: Task 12 — Số TK khách hàng (Phase 5)
Blocked: không có

### Task 11: Nút "Tạo hợp đồng" trên báo giá
- [x] `pages/sale/quotation/_id/index.vue`: nút "Tạo hợp đồng" (hiện khi `item.is_can_create_contract`) → `POST sale/contracts/from-quotation/{id}` → điều hướng `/sale/contract/{newId}/edit`.

## Phase 5 — Danh mục mở rộng

### Task 12: Số TK khách hàng
- [x] Form danh mục KH (AddCustomerModal) + CustomerCategory fillable + resource: thêm `bank_account` (input + trả về).

### Task 13: Số TK + người đại diện công ty
- [x] Tìm form/Service/Resource danh mục Công ty (Modules/Human settings). Thêm `bank_account` + `representative` (input + fillable + resource).

---

## Self-Review (sau khi xong)
- [ ] Migrate OK, php -l sạch.
- [ ] createFromQuotation: snapshot A/B đúng nguồn, items/totals copy, 1-1 enforce.
- [ ] Workflow submit/approve/reject + isCan* đúng.
- [ ] Mẫu in render `{{BANG_HANG_HOA}}` + biến đúng.
- [ ] Permission 1115-1122 seed + gán Admin company 1.
- [ ] FE: badge status, validate inline, cột dùng title, format ngày.

---

## Checkpoint — 2026-06-28 (tinh chỉnh HĐ/báo giá + màn chờ duyệt)

Vừa hoàn thành (BE+FE, chưa commit) — sau khi core hợp đồng đã xong:
- **ContractForm 2 tab** (Thông tin HĐ / Mẫu in), bỏ tiêu đề thừa.
- **Số HĐ**: input bắt buộc + unique (BE `code` rule `required|unique` ignore-self; FE cùng hàng Ngày HĐ).
- **Bên A đại diện = select** từ `customer_representatives` (mặc định đầu) + hiện chức vụ. **Bên B đại diện + chức vụ = read-only**, lấy từ **Người điều hành** công ty (`owner_id` → fullname + workPosition.name); cột mới `a_representative_role`/`b_representative_role`; **drop** `companies.representative/representative_role`. Bên B STK từ công ty.
- **Mẫu in**: đổi tên type → **"Hợp đồng bán hàng"**; `FormPrintTemplateComponent` thêm prop `lockedTypeId` (ẩn select loại, chỉ lấy mẫu loại này); ép **Times New Roman** trong `buildPrintData` (style `.tnr-print *`); biến `{{CHUC_VU_BEN_A/B}}`. Tạo 3 mẫu demo (HDBH-FULL/SHORT/BANG).
- **Preview mẫu in vào popup**: `ContractPrintPreview` modal (báo giá đã sẵn popup).
- **Lưu/Lưu&Gửi duyệt → redirect danh sách** (cả HĐ + báo giá).
- **Danh mục KH**: Người đại diện + Ngân hàng = section bảng động (bảng `customer_representatives`, `customer_bank_accounts`); ghi chú = input.
- **Menu "Mẫu in"** chuyển Quyết định → **HCNS** (cả trang `/human/category/print_templates` + route).
- **2 màn chờ duyệt**: `/sale/quotation-approval` + `/sale/contract-approval` — khoá status=Chờ duyệt, Duyệt/Từ chối inline, menu gated quyền "Duyệt báo giá bán"/"Duyệt hợp đồng".

Bug fix:
- Sửa HĐ không lưu/redirect được: `DetailSaleContractResource.contract_date` trả `d/m/Y` → BE rule `date` từ chối → đổi `Y-m-d` (form) + format FE màn xem.
- Lỗi validate báo **inline tại field** (bỏ toast) + nhảy về tab chứa lỗi.
- Nút thêm người đại diện/ngân hàng không phản hồi = HMR nạp thiếu script (restart dev server); fix luôn bug `close()` undefined ở AddCustomerModal.

Bước tiếp: user restart dev server + test trình duyệt toàn bộ; commit 2 repo.
Blocked: (không)

### Checkpoint — 2026-06-28 (UI danh sách)
Vừa hoàn thành: màn danh sách hợp đồng — **mã HĐ là link** (nuxt-link → `/sale/contract/:id`, hover underline) + **thêm nút In** cột thao tác (đặt trước Xóa). Tái dùng `ContractPrintPreview` (props :show + :contract-id, load qua API `sale/contracts/{id}/print` khi @shown) + handler `handlePrint` set printContractId + showPrintPreview. Đúng pattern màn chi tiết.
Bước tiếp: user reload test click mã + In trên danh sách.

### Checkpoint — 2026-06-28 (chi tiết HĐ: 2 tab + xuất hàng)
Vừa hoàn thành: màn chi tiết HĐ `pages/sale/contract/_id/index.vue` chia **2 tab** (`b-tabs` chuẩn dự án):
- Tab 1 "Thông tin hợp đồng": toàn bộ nội dung cũ (info + Bên A/B + chi tiết hàng hoá có giá + tổng tiền + điều khoản). Alert từ chối nằm ngoài tab (luôn hiện).
- Tab 2 "Thông tin xuất hàng": bảng hàng hoá **bỏ cột Đơn giá/VAT/Thành tiền**, cột **Số lượng** + thêm **Số lượng đã xuất** (cạnh nhau). Logic: `exportedQty` đọc `it.exported_quantity` (CHƯA có do chưa làm luồng xuất bán → hiển thị "-"); `isFullyExported` = đã xuất != null && == số lượng → tô **xanh `.qty-full`** cả 2 cột.
Khi làm luồng xuất bán: BE chỉ cần trả `exported_quantity` cho mỗi item → cột tự hiện số + xanh khi đủ. Footer/modals/script khác giữ nguyên. Thêm data `activeTab`.

### Checkpoint — 2026-06-28 (Xuất Excel + tinh chỉnh tab)
- **Xuất Excel** màn danh sách HĐ: nút #actions (V2BaseButton secondary + ri-download-line). BE `Modules/Sale/Exports/SaleContractExport.php` + `SaleContractController::export()` (getListForUser($filters)->get() → SaleContractResource resolve → Excel::download 'hop_dong.xlsx'), route `GET /contracts/export` trước `/{id}` + checkPermission giống index. FE exportExcel() token+arraybuffer+blob (revoke URL). Review opus: Spec ✅ + Quality Approved (fix 3 minor float/revoke/MIME).
- **Chi tiết HĐ**: bỏ tiêu đề trùng trong tab content + thêm icon lên tên tab (Tab1 ri-file-paper-2-line, Tab2 ri-truck-line).
Bước tiếp: user test xuất Excel theo filter + xem 2 tab.
