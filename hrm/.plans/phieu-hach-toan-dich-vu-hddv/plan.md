# Plan — Port Phiếu hạch toán dịch vụ HDDV

Xem `design.md` cho scope + quyết định. Bám khuôn màn anh em `wr-accounting-service-requests`.

## Phase 1 — BE nền (Entity + List + Show + Export), CHƯA ghi sổ ✅ XONG + verify data thật (2026-10-30)

> Verify tinker trên erp_hrm_check: 2420 phiếu; detailData đủ khối; total_payment=2,392,092 (TPE.HTDV.2026002425);
> services 2 / other_costs 4 / delivery 1; journal 22 dòng resolve đúng account+Nợ/Có+đối tượng; requester+phòng ban OK.
> QUYẾT ĐỊNH (lệch plan T1.4/T1.5): dời builder nguồn `contractData/requestData` sang Phase 2 (co-located với store);
> Phase 1 chỉ giao list+show+export. Controller/route Phase 1 KHÔNG có contract-data.

- [x] T1.1 Entity `Modules/Finance/Entities/WrAccountingService/WrAccountingService.php`
  - `extends Model` (bảng ERP `wr_accounting_services`, `$casts` total_service/total_cost => array)
  - STATUS `DA_HACH_TOAN=1`; STATUSES xanh `#16A34A`; const COST_ID_DELIVERY=5; const INVOICEABLE_TYPE
  - const PERMISSION_VIEW_* (3 cấp) + PERMISSION_ACCOUNTING; `use ChecksEmployeePermission`
  - quan hệ: services, costs, wrServiceContract, wrAccountingServiceRequest, customer, company, department, employee_create, accounting
  - `generateCode()`, `statusMeta()`, `contractCode()`, `totalPayment()`
  - `searchByFilter($request)` scope 3 cấp (port ERP, OR created_by) + `canView()` mirror
- [x] T1.2 Entity `WrAccountingServiceItem` (dịch vụ) + `WrAccountingServiceCost` (chi phí/vận chuyển)
- [x] T1.3 ListResource `WrAccountingServiceListResource` (cột §4; Người tạo/Ngày tạo; số format qt)
- [x] T1.4 Service `WrAccountingServiceService`: searchByFilter+paginate, meta (is_all_company…),
      exportRows, findForShow, detailData (thông tin chung + 3 bảng + tổng + journal resolve Customer/Employee/Work),
      formatDateTime. (contractData/requestData DỜI sang Phase 2)
- [x] T1.5 Controller `V1/WrAccountingServiceController`: index, show (canView 403), export. (store+nguồn ở Phase 2)
- [x] T1.6 Permissions: +3 quyền XEM "Phiếu hạch toán dịch vụ HDDV" type 23 (ghi sổ dùng lại 'Hạch toán dịch vụ HDDV'
      đã có); `permission:sync --dry-run` xác nhận Thêm 3.
- [x] T1.7 Routes `wr-accounting-services` (index/show/export); ExportColumnRegistry `wr_accounting_services` đã register
- [x] T1.8 Đăng ký bảng `wr_accounting_services` vào `CatalogHistoryService::TABLES`

## Phase 2 — Ghi sổ (posting) + store + lật nguồn

- [x] T2.0 Thêm hằng `INVOICEABLE_WR_ACCOUNTING_SERVICE` + `CONTRACTABLE_WR_SERVICE_CONTRACT`
      vào `AccountDetail` (chuỗi FQN ERP). Verify `accounting_works` id (DTHH/CKHH/GGHH/TTHHD/TNST/TNSQ/RRP)
      + `accounts.identify_number` (1311,5113,5111,33311,5211,5213,632,1541,35241,3335,6411) qua tinker.
- [x] T2.1 `WrAccountingServicePostingService` — port `getDataCreateDept` (BAO_HANH + HOP_DONG B1–B5). ✅ 2026-10-30
      B1–B4 port trực tiếp (doanh thu 5113, giá vốn 1541 theo service_name); B5 DÙNG LẠI `SupportAccountingTrait`
      (giống `BorrowSellPostingService::wrServiceBranch`, percent = (amount_after_extra − discount_price −
      rebate_price)/before_without_delivery, gọi null company). Fail-closed B5 (RuntimeException khi HTHT null);
      rollback khi saveAccountDetail fail (DB::transaction + try/catch); KHÔNG dd(); GIỮ bug rebate BAO_HANH.
      ⚠️ `resolveSupportAccounting` bỏ type-hint (quan hệ trả CustomerCare\WrServiceContract, cùng bảng).
      VERIFY tinker erp_hrm_check: HOP_DONG #2425 + BAO_HANH #808 → journal KHỚP 100% account_details ERP
      đã ghi theo (số TK, Nợ/Có); balance Nợ=Có từng group OK.
- [x] T2.2 `WrAccountingServiceService::store()` — ĐƯỜNG CHI PHÍ (YCHTDV) ✅ 2026-10-30.
      DB::transaction: lockForUpdate YCHTDV → `isWaitingAccounting()` sai ⇒ return null (409) →
      tạo phiếu (code='', status DA_HACH_TOAN, total_service = khuôn JSON rỗng ERP JS, total_cost từ YCHTDV,
      company/department/created_by theo người đăng nhập) → generateCode → copyCostsFromRequest →
      postAccounting (fail ⇒ throw ⇒ rollback) → lật YCHTDV (DA_DUYET + approver_id/approved_at) →
      markContractCostsCompleted (HOP_DONG→is_repair_completed, BAO_HANH→is_warranty_completed; PL_BO_SUNG không cờ).
      ĐƯỜNG DỊCH VỤ (WrAssignTask / wr_approve_result_id + updateHandoverDate) **HOÃN** — HRM chưa có module Giao việc;
      chặn sớm bằng RuntimeException. **KHÔNG notification** (ERP store không emit; bám ERP).
      postAccounting thêm nhánh PL_BO_SUNG: contractable_id/code/created_by/customer_id lấy từ HĐ CHA (parent_id) — khớp ERP store.
      ⚠️ KHÁC ERP (cải thiện): `!$status` ERP `return responseSuccess` để treo transaction; HRM throw ⇒ rollback sạch.
      VERIFY tinker erp_hrm_check (868 phiếu đường chi phí): getDataAccounting KHỚP 40/40 (bỏ 2 phiếu rác) về
      account+Nợ/Có+group+giá trị; meta HĐ (contractable_id/code/created_by/customer_id) KHỚP 30/30 kể cả type-3→parent.
      📌 2 phiếu rác id=3 (type3) + id=4 (type1): journal KHÔNG có vế VAT dù cost rows vat_percent=8 — **data artifact prod**
      (post lúc input khác, sau backfill vat_percent=8), KHÔNG phải lỗi port. ERP else-branch tính VAT theo vat_percent TỪNG DÒNG
      (không theo contract->vat_percent) — xác nhận bằng ERP `WrAccountingService::getDataCreateDept` dòng 267-282.
- [x] T2.3 Route `POST /wr-accounting-services` + `checkPermission:Hạch toán dịch vụ HDDV` ✅ 2026-10-30.
      FormRequest `WrAccountingServiceStoreRequest` (rules only: `wr_accounting_service_request_id`
      required|integer|exists) — chỉ nhận id YCHTDV, phiếu dựng server-side. Controller `store()`:
      findOrFail YCHTDV → `canAccounting()` sai ⇒ 403 → service->store → RuntimeException ⇒ 400 →
      null ⇒ 409 "Trạng thái đã bị thay đổi. Vui lòng load lại trang" → 200 + detailData.
      Verify router: POST đăng ký đúng, mw = api,auth:api,checkPermission:Hạch toán dịch vụ HDDV. php -l sạch.
- [x] T2.4 Feature test đối chiếu số với ERP ✅ 2026-10-30 — `WrAccountingServicePostingTest` (3 pass, 2.95s).
      Dùng phiếu THẬT trên erp_hrm_check + bút toán ERP đã ghi (`account_details.money_value`) làm kỳ vọng;
      thiếu data ⇒ markTestSkipped. 3 phiếu neo: id=1 HỢP ĐỒNG (đủ cụm B5 2 phòng, không VAT) — đối chiếu
      gộp theo (số TK, Nợ/Có) KHỚP + cân Nợ=Có; id=292 BẢO HÀNH — khớp journal + GIỮ bug rebate (5213=doanh thu);
      id=9 PHỤ LỤC — ghi dưới invoiceable_id sentinel (DatabaseTransactions rollback) rồi assert meta quy về HĐ CHA
      (contractable_id=21/code/created_by=28/customer_id=1048). ✅ Phase 2 (BE ghi sổ) HOÀN TẤT.

## Phase 3 — FE

- [x] T3.1 `pages/finance/wr-accounting-services/index.vue` (list xem+export, 4 mixin). ✅ 2026-10-30
      ⚠️ LỆCH note cũ "không cột Hành động": GIỮ cột **Hành động = CHỈ Lịch sử** (bỏ reject/edit/delete/accounting).
      Lý do: ERP index comment cột action, nhưng HRM bắt buộc Lịch sử tới được ở CẢ list + chi tiết, và
      mọi màn anh em đều có cột Hành động → bám ngang (SKILL THẮNG SPEC). Cột: STT · Ngày tạo · Số phiếu(nuxt-link
      `/finance/wr-accounting-services/{id}`) · Số hợp đồng(chữ, link trống) · Khách hàng · Tổng thanh toán(format qt) ·
      Người yêu cầu · Người tạo · Trạng thái(DA_HACH_TOAN xanh #16A34A) · Hành động(Lịch sử). Lọc: org · customer_id ·
      requester_id(Người yêu cầu) · creator_id(Người tạo) · status · code · contract_code · date_range.
      localStorageKey=`finance_wr_accounting_services`, columnScreenKey=`wr_accounting_services`, API_PREFIX=`finance/wr-accounting-services`.
      KHÔNG "Tạo mới" ở danh sách (phiếu sinh từ YCHTDV/nghiệm thu).
- [x] T3.2 `_id/index.vue` (chi tiết) ✅ 2026-10-30 — Form DÙNG CHUNG `WrAccountingServiceForm.vue` (Thông tin
      chung: Số hợp đồng/Khách hàng/Người yêu cầu/Phòng ban disabled + CreatorInfoLine) + `ServiceTable.vue` (17 cột,
      v-if hasServices) + `ServiceCostTable.vue` ×2 (import lại từ YCHTDV, chi phí khác/vận chuyển) + `JournalTable.vue`
      (8 cột bút toán, v-if hasJournal) + SystemInfoSection + V2Footer chỉ "Quay lại".
- [x] T3.3 `create.vue` + `components/WrAccountingServiceForm.vue` ✅ 2026-10-30 — Form nhận `requestId` → preview
      YCHTDV; footer `#custom-actions` "Hạch toán" POST `{wr_accounting_service_request_id}`. **LỆCH vs note:** sau
      hạch toán thành công `$router.replace` sang CHI TIẾT PHIẾU MỚI (để xem bút toán), không về list — vì màn tạo
      không có "danh sách của chính nó" để quay về, và kết quả cần xem ngay là sổ. `backUrl`="Quay lại" trỏ về chi tiết
      YCHTDV nguồn. Đường service `?wr_approve_result_id=` — BE sẵn, FE nối sau khi màn nghiệm thu có nút.
- [x] T3.4 Menu finance.js + sale-hub.js ✅ 2026-10-30 — **LỆCH vs note "isShow theo quyền view":** KHÔNG khai
      `isShow`, bám ngang sibling YCHTDV (dòng finance.js 308 cũng không có) → phạm vi do BE canView gate. finance.js
      dòng 309 placeholder → `link`; sale-hub.js thêm `{ n, link }` ngay sau YCHTDV.
- [x] T3.5 **Nối link trống** ✅ 2026-10-30 — `wr-accounting-service-requests/_id/index.vue` `goToAccounting()` +
      `index.vue` handleRowAction case 'accounting' đều push `/finance/wr-accounting-services/create?wr_accounting_service_request_id=<id>`.
- [x] T3.6a ExportColumnRegistry ✅ 2026-10-30 — FE `exportFields` (9 cột) KHỚP 1:1 BE
      `ExportColumnRegistry::COLUMNS['wr_accounting_services']` (id + nhãn); grep V2Base raw-HTML RỖNG.
- [x] T3.6b verify Playwright ✅ 2026-10-30 (API :8000 + client :3000, token từ e2e/.auth/user.json):
      - **Danh sách** `/finance/wr-accounting-services?type=all`: 10 cột đúng, 2420 bản ghi, số chuẩn quốc tế,
        ngày dd/mm/yyyy HH:mm, badge "Đã hạch toán", hành động chỉ Lịch sử, phân trang 5/10/20/50/100, toolbar
        Xuất Excel + Cấu hình cột, tab title "Phiếu hạch toán dịch vụ HDDV". ✓
      - **Chi tiết** `/finance/wr-accounting-services/2425`: Thông tin chung đủ 4 ô (HĐ/KH/Người yêu cầu/Phòng ban),
        creator line kế toán tạo phiếu, bảng Dịch vụ 17 cột + 5 footer, bảng Hạch toán 8 cột đầy đủ bút toán hỗ trợ,
        footer Lịch sử + Quay lại. ✓
      - **Hạch toán (preview)** `/finance/wr-accounting-services/create?wr_accounting_service_request_id=882`:
        **FIX** `WrAccountingServiceForm.loadRequestPreview()` — YCHTDV shape khác phiếu: map `creator_name`→`requester_name`,
        `department_name`→`requester_department_name`, bỏ trống creator_name/created_at để CreatorInfoLine (is-create) lấy
        current user + giờ hiện tại. Verify lại: Số HĐ + Khách hàng + Người yêu cầu (Trịnh Thùy Linh) + Phòng ban (PHÒNG
        THIẾT BỊ Ô TÔ 2) đều hiện; creator line = "DNS Admin - 30/10/2026 15:28". Bảng Chi phí khác 4 dòng + Tổng cộng. ✓
        (KHÔNG bấm POST "Hạch toán" — tránh ghi phiếu + bút toán thật lên DB gộp.)
      - **Đối chiếu ngang**: bám sibling YCHTDV — ServiceCostTable dùng lại nguyên, CreatorInfoLine, V2BaseFormSection,
        V2Footer, badge V2BaseBadge theo status_color BE; grep V2Base raw-HTML RỖNG. ✓

## Checkpoint
- [x] Đối chiếu ngược ERP (cột/lọc/hành động/điều kiện) + ngang màn HRM đã QA — xong ở T3.6b.
- [x] Checklist erp-to-hrm-screen; grep V2Base RỖNG; số format quốc tế — xong ở T3.6b.
- [x] **COMMIT + PUSH develop (2026-10-31)** theo yêu cầu user: hrm-api `06b01e074`
      "feat(finance): port màn Phiếu hạch toán dịch vụ HDDV (phía bán) từ ERP";
      hrm-client `51f44677b` "feat(finance): màn Phiếu hạch toán dịch vụ HDDV (phía bán)".
      Stage có chọn lọc (chỉ file feature) — KHÔNG đụng thay đổi lạc (bonus-component docs đã xóa,
      SupplierReturnSearchModal.vue) trong working tree hrm-client. Cả 2 push fast-forward, không rebase.
      ✅ TOÀN BỘ feature HOÀN TẤT + BÀN GIAO.
