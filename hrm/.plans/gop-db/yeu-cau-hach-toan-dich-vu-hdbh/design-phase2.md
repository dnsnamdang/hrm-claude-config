# Design — Port "Yêu cầu hạch toán dịch vụ HĐBH" ERP → HRM — **PHASE 2 (write-side)**

> Tiếp nối Phase 1 (chỉ-đọc, đã DONE + push — xem `design.md` + `plan.md`).
> Nguồn nghiệp vụ ERP: `App\Model\Sale\ServiceAccountingRequest`,
> `app/Http/Controllers/Sale/ServiceAccountingRequestController.php`,
> `app/Services/Sale/Firm/Contract/FirmContractCostService.php::getDataForServiceExport`,
> view `resources/views/sale/service_accounting_requests/`.
> **Khuôn HRM 1:1**: màn song sinh HDDV write-side ĐÃ CÓ ĐỦ —
> `wr-accounting-service-requests` (Controller/Service/FormRequest/NotifyService/catalog-history).
> Bám khuôn này; chỉ khác ở bộ nạp chi phí (FirmContract) + 5 trạng thái / 3 loại / 4 cấp quyền + đính kèm.

## 1. Ý định & vì sao

Phase 1 mới port phần đọc. Phase 2 mở **vòng đời phiếu YÊU CẦU**: Tạo → (Lưu nháp / Gửi duyệt) →
Sửa/Xóa (khi nháp/bị từ chối) → Không duyệt. Để lập được phiếu, HRM phải nạp **chi phí sống từ Hợp
đồng hãng (FirmContract)** — hạ tầng này HRM CHƯA có (read-model FirmContract hiện mỏng, không có quan
hệ costs, không có entity FirmContractCost). Đây là phần dựng-mới lớn nhất của Phase 2.

Mục tiêu: người lập HĐ hãng tạo được phiếu yêu cầu kế toán hạch toán phần dịch vụ/chi phí/vận chuyển
của HĐ, gửi duyệt; kế toán (có quyền) Không duyệt kèm lý do. Hành vi port **trung thành ERP**.

## 2. Scope đã chốt với user (2026-11-02, hỏi dạng chọn đáp án)

| # | Quyết định | Chốt |
|---|---|---|
| A | Vòng đời | **Tạo/Sửa/Xóa + Gửi duyệt + Không duyệt**. KHÔNG có Duyệt/Hạch toán (màn #2 `serviceAccounting`) — để phase sau. Phiếu "Chờ duyệt" trong HRM chỉ có thể bị Không duyệt. |
| B | Cờ `exported` trên dòng chi phí HĐ hãng | **Port y hệt (faithful)**: khi Gửi duyệt ghi `exported=true` lên `firm_contract_costs`; khi Không duyệt `rollbackAccounting` gỡ về `false`. Chấp nhận HRM ghi vào bảng HĐ (DB chung `erp_hrm_check`). |
| C | Quyền Không duyệt | **Seed ngay** quyền `Hạch toán yêu cầu làm dịch vụ` (guard `api`). |
| D | Đính kèm file | **Port đầy đủ** (ERP có `syncAttachments`). Dùng convention `files` + `V2BaseFile.vue` của HRM (khuôn HDDV HRM KHÔNG có — phải thêm mới). |
| E | Loại phiếu | **Cả 3 loại**: 1 Dịch vụ (`revenue_costs`), 2 Chi phí (`costs`), 3 Vận chuyển (tạo/tìm dòng "Chi phí vận chuyển" từ `delivery_*`, GHI vào `firm_contract_costs`). |
| F | Màn Tạo | **Standalone create + popup chọn HĐ hãng** (HRM chưa port màn HĐ hãng). Bám `FirmContractSearchModal.vue` (có sẵn ở product-export-requests). |
| G | Validate Lưu nháp | **Theo convention HRM**: Lưu nháp (status 1) cho lưu **rỗng** (không cần dòng chi phí); chỉ Gửi duyệt (status 2) mới bắt `costs` required ≥1 dòng. **LỆCH ERP có chủ đích** (ERP bắt cả 2). |

## 3. Nghiệp vụ ERP phải port (đã đọc source, bám 1:1)

### 3.1 Tạo phiếu (store) — `ServiceAccountingRequestController::store` + `syncCosts`
1. User mở màn Tạo → chọn **1 FirmContract** qua popup → chọn **type** (1/2/3) → hệ nạp dòng chi phí
   → **tick chọn dòng nào xuất** (`need_export`) + nhập Ghi chú + Đính kèm → Lưu nháp **hoặc** Lưu & gửi duyệt.
2. BE: validate (loại 2/3 cần `contractable_id/type`, `status∈{1,2}`; **`costs` chỉ required khi
   `status==2` (Gửi duyệt) — Lưu nháp (status 1) cho phép rỗng, theo convention HRM, LỆCH ERP có chủ đích,
   user chốt 2026-11-02**), check
   **`$contract->support_accounting`** tồn tại (morphOne `FirmSupportAccounting`) → nếu không: báo
   "Hợp đồng không có hỗ trợ hạch toán". `generateCode()` = `"{company_code}.YCHTDV."` + autoGenerate(5).
   `fill(status,note,type,payed_cost,contractable_type,contractable_id)`, save.
3. `syncCosts($costs)`: **xoá sạch** `service_accounting_request_costs` của phiếu rồi ghi lại từ
   payload. **Mỗi dòng payload chỉ gửi `contract_costable_id`** (= id `FirmContractCost`); BE **đọc lại
   giá trị thật từ `FirmContractCost::find(id)`** (name/price/value_discount/value_extra/total_price=
   value_before_vat/sale_max_percent/coefficient_cost_price/cost_id), KHÔNG tin FE. Set
   `contract_costable_type = FirmContractCost::class`.
   - **Chống trùng**: nếu dòng `FirmContractCost` đã `exported==true` → `syncCosts` trả false →
     rollback transaction, báo "...đã hoàn thành".
   - **Khi `status==CHO_DUYET(2)`**: set `FirmContractCost.exported=true` (khóa dòng). Lưu nháp (1) KHÔNG khóa.
4. `syncAttachments(attachments, delete_attachments)`.
5. Nếu `status==CHO_DUYET`: notify người giữ quyền `Hạch toán yêu cầu làm dịch vụ` (cùng công ty).

### 3.2 Nạp chi phí từ HĐ hãng — `FirmContractCostService::getDataForServiceExport($contract,$delivery_cost)`
Đây là **hàm dựng-mới trọng tâm** (bám `buildCostsFromContract()` của HDDV). Dùng CHUNG cho đọc (contract-data) và ghi (store/update — đọc lại giá trị):
- **type 1 / 2 (`$delivery_cost=false`)**: nạp quan hệ `costs` + `revenue_costs` của FirmContract,
  `->where('is_decrease', false)`, `select('*','value_before_vat as total_price')`, kèm `cost`.
  - `costs()` = `firm_contract_costs` `revenue_calculation=false` & `name<>'Chi phí vận chuyển'`.
  - `revenue_costs()` = `revenue_calculation=true`.
  - `vat_percent` = `type==2 ? costs[0].vat_percent : revenue_costs[0].vat_percent`.
  - **KHÔNG trừ phần đã hạch toán** (chỉ loại `is_decrease`); dòng đã `exported` vẫn hiện (FE tô invalid).
- **type 3 (`$delivery_cost=true`)**: tìm/tạo `Cost(name='Chi phí vận chuyển')`, rồi tìm/tạo 1
  `FirmContractCost(firm_contract_id, cost_id)`; tính `price/value_extra/value_discount/value_before_vat`
  từ `delivery_*` của HĐ (trừ các phụ lục giảm nếu `delivery_decrease_annex`), `vat_percent=
  delivery_vat_percent`, `vat_cost=round(before_vat*vat/100)`, `value_after_vat`, **`$item->save()`**
  (GHI dòng mới vào `firm_contract_costs`), trả về 1 dòng `need_export=true`, `total_price=value_before_vat`.
- Gate chọn HĐ: `canProductExport()` = HĐ `status==CO_HIEU_LUC` **&&** `created_by==mình`; type 3 thêm
  `canRequestAccountingDelivery()`.

### 3.3 Sửa (update) — `canEdit()` = `created_by==mình && status∈{DANG_TAO(1), TU_CHOI(3)}`
`only(status,note,payed_cost)` (KHÔNG đổi type/contractable), save, `syncItems`(rỗng với FirmContract),
`syncCosts`, `syncAttachments`, notify nếu CHO_DUYET. Thứ tự gác (bám HDDV): **trạng thái trước (409),
quyền sau (403)**.

### 3.4 Xóa (destroy) — `canDelete()` = giống `canEdit`
**Xóa cứng** (`$object->delete()`, bảng không softDeletes), **không hỏi lý do**. Trong transaction,
log catalog 'delete' trước, xoá costs, xoá phiếu.

### 3.5 Không duyệt (reject) — quyền `Hạch toán yêu cầu làm dịch vụ`, chỉ khi `status==CHO_DUYET`
**Bắt buộc nhập lý do** (`comment` required) → set `status=TU_CHOI(3)`, `approver_id=Auth::id()`,
`approved_at=now()`, `save`, **`rollbackAccounting()`** (gỡ `exported=false` trên các `FirmContractCost`
đã khóa; nhánh `service_export_request` null với FirmContract nên bỏ qua), notify người tạo.
**Call của tôi (lệch ERP có chủ đích, theo convention HRM):** ERP `reject()` KHÔNG chặn trạng thái ở BE
(chỉ gác bằng nút FE + middleware quyền). HRM **thêm guard BE**: nếu `status != CHO_DUYET` → **409/423**
(bám cách HDDV gác trạng thái trước, quyền sau). Lý do: BE phải fail-closed, không tin FE.

### 3.6 payed_cost
FE tính và gửi lên: `payed_cost = Σ(total_price dòng chọn) × (1 + vat_percent/100)`. BE lưu qua `fill`.
(Nhất quán công thức VAT Phase 1.)

## 4. Dữ liệu (DB gộp local `erp_hrm_check`)
- `firm_contracts` 23.277 dòng; `firm_contract_costs` **1.752 dòng** — có đủ cột cần: `exported`,
  `is_decrease`, `revenue_calculation`, `value_before_vat`, `vat_percent`, `company_discount_percent`
  (→ accessor `sale_max_percent`), `cost_id`, `coefficient_cost_price`, `delivery_*` nằm ở `firm_contracts`.
- `service_accounting_requests` / `service_accounting_request_costs`: schema đã mô tả ở Phase 1
  (`design.md §4`). Cột NOT NULL khi ghi: request → `code,status,type,created_by,updated_by,contractable_id`;
  cost → `service_accounting_request_id,cost_id,name`.
- Gate `support_accounting`: bảng tên **`firm_support_accounting`** (số ít), morphOne. **ĐÃ VERIFY DB gộp
  (2026-11-02)**: 21.403 dòng gắn FirmContract (> 9.466 HĐ Có hiệu lực) — `contractable_type` lưu **chuỗi
  FQN ERP** `App\Model\Sale\Firm\Contract\FirmContract`; **cả 1303 phiếu hiện có đều có dòng support**.
  Gate thỏa dư → luồng Tạo chạy + test được. Chỉ cần read-model mỏng `FirmSupportAccounting` (morphOne +
  đọc chuỗi FQN ERP như Phase 1 đã làm cho `contractable` của phiếu).

## 5. Việc phải DỰNG MỚI (HRM chưa có)

### BE (hrm-api, module Finance)
1. **Entity `FirmContractCost`** (`Modules/Finance/Entities/Contract/FirmContractCost.php`): map
   `firm_contract_costs`, `$fillable` gồm `exported` + các cột tính type-3; accessor `sale_max_percent =
   company_discount_percent`; quan hệ `cost()`. **Cho phép ghi** `exported` (và tạo dòng type-3) — khác
   FirmContract read-model (`$guarded=['*']`).
2. **Quan hệ trên read-model FirmContract**: `costs()` / `revenue_costs()` (lọc như §3.2),
   `support_accounting()` morphOne (→ read-model mỏng `FirmSupportAccounting`), các accessor `delivery_*`
   nếu thiếu. ADDITIVE, giữ model chỉ-đọc ở các cột khác.
   - **Call của tôi — morphMap cho `contract_costable` (điểm builder-check #3, bắt buộc để rollback đúng):**
     (a) đăng ký trong `FinanceServiceProvider::registerMorphMap` chuỗi ERP
     `App\Model\Sale\Firm\Contract\FirmContractCost` → HRM `FirmContractCost` (như Phase 1 đã map
     `...\FirmContract`); (b) thêm quan hệ `contract_costable()` morphTo vào entity
     `ServiceAccountingRequestCost` (Phase 1 chưa có — chỉ đọc cột); (c) khi `syncCosts` ghi dòng mới,
     **`contract_costable_type` ghi CHUỖI FQN ERP** (dùng `getMorphClass()` sau khi đăng ký morphMap, ra
     đúng chuỗi ERP) để **cả ERP lẫn HRM resolve được** — tránh anti-goal "kẹt khóa `exported`" khi phiếu
     Chờ-duyệt (có thể gửi từ ERP) lại bị Không duyệt ở HRM. Verify: dữ liệu hiện lưu `contractable_type`
     dạng FQN ERP (đã xác nhận ở §4).
3. **Loader `buildCostsFromContract()`** cho HDBH (port `getDataForServiceExport`, cả nhánh delivery
   type-3 có GHI dòng) — đặt trong `ServiceAccountingRequestService`, dùng chung cho `contractData()`
   (đọc) và `store/update` (đọc lại giá trị).
4. **Write-side controller + service**: `store/update/destroy/reject` + `contractData` + endpoint
   **list FirmContract chọn được** cho popup. Bám `WrAccountingServiceRequestController/Service` 1:1,
   chỉnh 5 trạng thái / 3 loại.
5. **2 FormRequest**: Store (dùng chung update, `contractable_id` required khi tạo) + Reject
   (`comment` required). Chỉ `rules()`+`attributes()`.
6. **Routes** (module Finance `api.php`): route tĩnh (`contract-data`, firm-contract list, `export`)
   khai TRƯỚC `/{id}`; `reject` gắn `checkPermission:Hạch toán yêu cầu làm dịch vụ`; store/update/destroy
   KHÔNG middleware (gác theo bản ghi trong Entity).
7. **Entity ServiceAccountingRequest** (đã có từ Phase 1): bổ sung cờ `canEdit/canDelete/canAccounting`
   + `WRITABLE_STATUSES` + `generateCode()` + đính kèm (`files()` relation).
8. **Catalog history**: gọi TAY `log('create'/'delete')`, `logUpdate()`, `logCatalogStatus()` (bám HDDV);
   bảng `service_accounting_requests` đã nằm trong `CatalogHistoryService::TABLES` (verify).
9. **NotifyService** cho HDBH (bám `WrAccountingServiceRequestNotifyService`): `onSentForApproval` +
   `onRejected`, bọc try/catch, gọi trong `DB::afterCommit`.
10. **Seed quyền** `Hạch toán yêu cầu làm dịch vụ` (guard api) ở `PermissionsTableSeeder` + gán role phù hợp.
11. **Đính kèm**: quan hệ `files()` + sync (convention `files` chung).

### FE (hrm-client)
12. `pages/finance/service-accounting-requests/create.vue` + `_id/edit.vue` + form dùng chung
    (`components/ServiceAccountingRequestForm.vue`) — bám form HDDV; thêm **popup chọn HĐ hãng** (bám
    `FirmContractSearchModal.vue`, row-click chọn 1 HĐ) + select **type** + bảng chi phí read-only
    **có checkbox tick dòng** (chưa có khuôn — dựng mới, tham khảo checkbox ở `SourceProductPickerModal.vue`)
    + **upload đính kèm** (`V2BaseFile.vue`).
13. Màn chi tiết `_id/index.vue` (Phase 1): **bật lại** nút Sửa/Xóa (theo `canEdit/canDelete`) + nút
    **Không duyệt** (modal nhập lý do, theo `canAccounting`). Danh sách: cột Hành động thêm Sửa/Xóa.
14. Menu: giữ mục Phase 1.

## 6. Verify (khi tới bước làm)
- Playwright: tạo nháp → sửa → gửi duyệt (kiểm `exported=true` trên `firm_contract_costs`) → Không duyệt
  (kiểm `exported` về false) → xóa. Cả 3 loại (đặc biệt type-3 tạo dòng vận chuyển). Test âm quyền
  (reject bằng tài khoản không có quyền hạch toán → 403; sửa/xóa phiếu người khác → 403; sửa phiếu đã
  CHO_DUYET → 409).
- Đối chiếu số `payed_cost`/VAT với công thức.

## 7. Non-goals / Anti-goals
- **Non-goal**: màn #2 `serviceAccounting` (ghi sổ) + nút Duyệt/Hạch toán + nút "Hạch toán dịch vụ" ở chi tiết.
- **Non-goal**: 3 loại HĐ còn lại (ServiceContract/Contract/ProjectContract) — chỉ FirmContract.
- **Non-goal**: port màn HĐ hãng (chỉ cần popup chọn + read-model đủ nạp chi phí).
- **Anti-goal**: tin giá trị chi phí từ payload FE (phải đọc lại từ `FirmContractCost`).
- **Anti-goal**: làm lệch hành vi `exported`/`rollbackAccounting` so ERP (DB chung — lệch gây xuất trùng/kẹt khóa).

## 8. Ràng buộc
- Mọi thao tác trong `HRM/` (CLAUDE.md root). Faithful port. Dùng khuôn HDDV, không tự sáng tạo kiến trúc.
- Port tiếp theo: sau khi design DUYỆT → `superpowers:writing-plans` + skill `erp-to-hrm-screen`.

## 9. Để builder tự quyết (ghi rõ là call của tôi, không phải user)
- Tên chính xác route list FirmContract cho popup + tham số lọc (bám `FirmContractSearchModal` hiện có).
- Có tái dùng được endpoint firm-contract list ở `assign/product-export-requests/firm-contracts` không,
  hay khai route Finance riêng (ưu tiên khai riêng trong Finance để gate `support_accounting`+`canProductExport`).
- Chi tiết UI checkbox "chọn tất cả / từng dòng" + cách disable dòng đã `exported`.

## 10. Call đã chốt sau builder-check (2026-11-02) — không phải điểm user quyết
- **Đính kèm KHÔNG lệch 2 cổng**: ERP sau gộp DB cũng dùng chung bảng `files` (`table`=tên bảng,
  `table_id`) y hệt HRM → HRM ghi `files` với `table='service_accounting_requests'` là ERP đọc được. Port theo §D.
- **Tên quyền Không duyệt**: ERP `update()` notify nhầm chuỗi `'Duyệt yêu cầu làm dịch vụ'` ≠ gate
  `canAccounting` dùng `'Hạch toán yêu cầu làm dịch vụ'` (typo phía ERP). HRM **chuẩn hóa cả 2 đường về
  `'Hạch toán yêu cầu làm dịch vụ'`**.
- **mimes/size lệch create vs update ERP** (create: +zip, max 30MB; update: bỏ zip, max 10MB, min:1):
  HRM **chuẩn hóa 1 bộ rule** (mimes pdf/jpg/jpeg/png/zip/doc/docx, max 30MB, min theo quyết định §1),
  dùng chung store+update.
- **Guard trạng thái BE cho reject** → 409/423 (xem §3.5).
- Các điểm trên là mechanics port trung thành / fail-closed, builder áp theo convention HDDV.
