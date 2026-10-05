# Spec — Khách "không bắt buộc VAT" ⇒ VAT 0% trên Báo giá / Hợp đồng hãng (ERP, đợt 1)

**Người phụ trách:** @junfoke — 2026-09-24
**Repo:** `TanPhatDev` (clone `hrm/TanPhatDev`), làm thẳng trên `master` (bản sửa gấp cho prod; user tự commit như các fix trước).

## 1. Bối cảnh

- Nhóm khách hàng có cờ `customer_groups.no_require_vat` ("Khách không bắt buộc VAT", màn
  `admin/customer_groups`). Hiện cờ chỉ **miễn chặn** lỗi "Hàng hóa thuộc hãng X cần VAT khi bán"
  khi người dùng tự nhập VAT = 0; không đưa VAT về 0.
- Ca thật 24/09/2026: khách **CÔNG TY TNHH KIM MAY ORGAN (VIỆT NAM)** (nhóm "Bán lẻ" + "Khu chế xuất",
  "Khu chế xuất" có cờ). KD lập báo giá hãng trên ERP vẫn bị tính VAT.
- Yêu cầu nghiệp vụ: khách thuộc nhóm có cờ ⇒ trên **mọi** BG/HĐ, VAT của hàng hoá / dịch vụ /
  chi phí / vận chuyển đều **0%**, xuất hàng cũng 0%. Áp cho cả báo giá dự án TKT bên HRM.

## 2. Phạm vi

**Đợt 1 (spec này):** ERP — Báo giá hãng (`firm_quotations`) + Hợp đồng hãng (`firm_contracts`).
Đây là luồng ERP đang dùng thật (2026: ~27,9k BG, ~12,9k HĐ; các loại BG khác gần như không dùng).

**Ngoài phạm vi (đợt sau):**
- Đợt 2: báo giá dự án TKT bên HRM (module Assign, `QuotationService::enforceErpProductVat` đang ép VAT
  theo sản phẩm) **cùng** đường đồng bộ HRM→ERP `FirmQuotationService::saveDataApi` /
  `HrmQuotationContractController` — sửa 2 phía một lúc để không lệch hiển thị.
- Phụ lục HĐ hãng, quyết toán, đơn nguyên tắc, các loại BG/HĐ ERP khác.

## 3. Quyết định đã chốt với user

| # | Quyết định |
|---|---|
| Q1 | Khách có cờ ⇒ **ép 0% và KHOÁ** mọi ô VAT (không cho sửa), BE cũng ép khi lưu |
| Q2 | Chứng từ cũ: **không** chạy script hàng loạt; mở sửa và lưu lại thì về 0%. Đã duyệt/đã xuất giữ nguyên |
| Q3 | Phương án A: helper dùng chung + chặn BE + FE khoá ô. Phạm vi BG + HĐ hãng |
| Q4 | `saveDataApi` (đường HRM) để sang đợt 2 |
| Q5 | Khách thuộc nhiều nhóm: chỉ cần 1 nhóm có cờ là áp dụng (theo accessor sẵn có) |

## 4. Thiết kế

### 4.1 Nhận biết khách miễn VAT
- `App\Model\Sale\Customer::isNoRequireVat($customerId): bool` — static, `find` + accessor
  `no_require_vat` (duyệt `customer_has_groups`). `null`/không tìm thấy ⇒ `false`.
- Route `GET admin/sale/firm_quotations/customerVatInfo?customer_id=` →
  `{success:true, data:{no_require_vat: bool}}`. KHÔNG sửa `Common\SearchController@searchCustomer`
  (dùng chung nhiều màn).

### 4.2 BE ép 0% khi lưu — `App\Services\Sale\Firm\FirmVatExemption`
- `zeroQuotationData(array $data): array` — gán 0 cho: `delivery_vat_percent`; `tabs[*].vat_percent`,
  `tabs[*].products[*].vat_percent`, `tabs[*].cost_after_vat` = tiền trước VAT của tab;
  `groups[*].vat_percent`, `groups[*].products[*].vat_percent`; `costs[*].vat_percent`,
  `revenue_costs[*].vat_percent`. Các khoản tiền VAT còn lại BE tự tính lại từ `vat_percent`
  (`syncGroups`, `syncCosts`, `delivery_vat`).
- `zeroContractData(array $data): array` — tương tự cho payload hợp đồng.
- Điểm gọi (chỉ khi `Customer::isNoRequireVat(customer_id)`):
  - Báo giá: `FirmQuotationController::store/update` (controller WEB) — ép payload `$data` trước khi
    gọi service. KHÔNG đặt trong `FirmQuotationService::update` vì `apiUpdate` (đường HRM) cũng gọi hàm
    này (giữ Q4).
  - Hợp đồng: cờ `$noRequireVat` trong `FirmContractService::saveFirmContractData` (tính 1 lần, bỏ qua
    nguồn `hrm_quotation_id`) → `delivery_vat_percent` (~466), `vat_extra_cost(_percent)`,
    `syncTabsFromQuotation` (VAT dòng hàng + `vat_cost`/`total_after_vat` tab), `syncGroupsFromQuotation`,
    `syncCostsFromQuotation` đều dùng 0. Tổng HĐ BE tự cộng từ các `vat_cost` ⇒ tự về 0.
- Luôn **thêm** bước, không đổi hành vi khách thường.

### 4.3 Không nhảy lại VAT theo danh mục sản phẩm
Dữ liệu trả cho FE khi mở sửa / lập HĐ đi qua `FirmVatExemption::zeroLoadedData()` (mọi % VAT = 0 +
`no_require_vat = true`) nếu khách có cờ:
- `FirmQuotationService::getDataForEdit` (cả chứng từ cũ có VAT mở ra là về 0)
- `FirmQuotationService::getDataForContract` (~747 đang gán lại VAT theo danh mục)
- `FirmContractService::getDataForEdit` (~1347 đang gán lại VAT theo danh mục)

(`FirmContractService::getDataForPrincipleOrder` ~148 cũng gán lại VAT nhưng thuộc đơn nguyên tắc — ngoài phạm vi.)

### 4.4 FE — `sale/firm/quotations` + `sale/firm/contracts`

Trên cả 2 form, ô VAT đều **chỉ hiển thị** (VAT hàng theo danh mục SP, chi phí theo danh mục chi phí,
vận chuyển cố định 8% trong `FirmQuotation.after()`); HĐ lấy nguyên số từ BE. Nên FE chỉ cần:
- `form.no_require_vat` lấy từ `customerVatInfo` khi `setCustomer` và khi load màn sửa/lập HĐ.
- Có cờ: mọi `vat_percent` (dòng hàng, tab, nhóm, vận chuyển, chi phí doanh thu, chi phí khác) = 0;
  dòng hàng thêm mới sau đó cũng 0 (hook ở `addProduct` của tab); ô VAT `ng-disabled` + icon ⓘ
  tooltip "Khách thuộc nhóm không bắt buộc VAT"; bỏ qua cảnh báo "cần VAT khi bán".
- Đổi sang khách không cờ: trả VAT dòng hàng về VAT danh mục sản phẩm, vận chuyển về 8%.

### 4.5 Xuất hàng
Không sửa — `FirmContractProductExportService` đọc `firm_contract_tab_products.vat_percent`.

## 5. Kiểm thử
- `php -l` các file PHP sửa.
- Local `php artisan serve :8001` (DB `erp_dev_30_01_26`), Playwright:
  1. Khách gán nhóm có cờ: tạo BG hãng → mọi ô VAT 0 & khoá, tổng = trước VAT; lưu; mở sửa vẫn 0.
  2. Lập HĐ từ BG đó → VAT 0; mở sửa HĐ vẫn 0; kiểm DB `firm_contract_tab_products.vat_percent = 0`.
  3. Khách thường: VAT theo sản phẩm, vận chuyển 8% — không đổi so với trước.
  4. Đổi khách có cờ ↔ không cờ trên cùng form → VAT chuyển đúng.
  5. Gửi payload giả VAT 10% cho khách có cờ → BE vẫn lưu 0.

## 6. Rủi ro
- `FirmQuotationService`/`FirmContractService` là service lõi luồng bán hàng — chỉ thêm nhánh có điều
  kiện, review kỹ diff.
- Tổng tiền tab do FE gửi (`cost_after_vat`) — BE phải tự gán lại, nếu sót sẽ lệch tổng khi FE cũ cache.
- Đợt 1 chưa phủ HRM: BG TKT đồng bộ sang vẫn theo VAT HRM cho tới đợt 2.
