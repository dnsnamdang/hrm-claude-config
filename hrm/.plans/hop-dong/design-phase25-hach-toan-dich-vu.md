# Phase 25 — Hạch toán dịch vụ / chi phí / vận chuyển cho Hợp đồng bán HRM

> Ngày: 05/11/2026 · Nhánh: `gop_db-hop-dong-ban` (worktree `wt-hop-dong-ban`, cả hrm-api + hrm-client) · Người phụ trách: @dnsnamdang
> Trạng thái: thiết kế — CHƯA code. Code / migration cần user cho phép riêng ("làm" + phạm vi).

## 1. Mục đích và lý do

Hợp đồng bán HRM (`Modules\Assign\Entities\Contract\Contract`, bảng `hrm_contracts`) sẽ **thay thế Hợp đồng hãng**
(`FirmContract`, bảng `firm_contracts`). Hiện HĐ HRM đã có xuất hàng (YCXH → PXK → ghi sổ) và thu tiền, nhưng **chưa có
đường hạch toán phần dịch vụ / chi phí / vận chuyển** — doanh thu 5113, giá vốn 632, thưởng / hoa hồng / quỹ rủi ro của
phần này chưa ghi sổ được.

Trên `gop_db`, nguyentrancu97 đã port xong (30/10–04/11) 2 màn cho HĐ hãng:
- **Yêu cầu hạch toán dịch vụ – HĐBH** (`service_accounting_requests`, mã `.YCHTDV.`): người lập HĐ tạo, kế toán duyệt / không duyệt.
- **Phiếu hạch toán dịch vụ – HĐBH** (`service_accounting`, mã `.HTDV.`): kế toán lập từ yêu cầu, "Lưu và duyệt" thì ghi `account_details`.

**Quyết định (user 05/11):** HĐ HRM dùng **chung đúng 2 màn này**, không dựng màn mới — mở rộng để nhận thêm HĐ HRM.
Làm thẳng trên nhánh HĐ bán (đã merge `gop_db` mới nhất vào nhánh, 05/11).

## 2. Mục tiêu / Không làm / Thất bại nếu

**Mục tiêu**
- Người lập HĐ HRM tạo được yêu cầu hạch toán **Dịch vụ** (type 1) / **Chi phí** (type 2) / **Vận chuyển** (type 3) cho HĐ của mình.
- Kế toán duyệt / không duyệt yêu cầu, lập Phiếu hạch toán, ghi sổ đúng bộ bút toán như HĐ hãng (5113 / 33311 / 5213 / 632 / 1541 + 4 cụm nặng cho type 1).
- Mỗi dòng dịch vụ / chi phí (và phần vận chuyển) của HĐ chỉ hạch toán **một lần**.
- Phiếu hạch toán đã ghi sổ làm HĐ chuyển sang "Đang thực hiện" (như thu tiền / mượn bán).

**Không làm**
- Không hạch toán từng phần một dòng (ERP cũng không — 1 dòng = 1 lần).
- Không đụng luồng "Yêu cầu làm dịch vụ" (`service_export_requests`) — HĐ hãng ERP cũng không dùng.
- Không bỏ hỗ trợ HĐ hãng ở 2 màn (chạy song song tới khi chuyển hết sang HĐ HRM).
- Không làm phụ lục bổ sung (HĐ HRM chưa có PLBS).

**Thất bại nếu (dù chạy được)**
- Một dòng bị hạch toán 2 lần (cờ lệch phiếu), hoặc bị khoá vĩnh viễn sau khi kế toán không duyệt.
- Phiếu của HĐ hãng đang chạy bị ảnh hưởng (số liệu / quyền / màn hình).
- Số thưởng / hoa hồng lệch cách ERP tính vì HTHT gộp chi phí vào dịch vụ (xem 4.4).

## 3. Quyết định đã chốt (05/11/2026)

| # | Câu hỏi | Chốt | Hệ quả |
|---|---|---|---|
| D1 | Dùng chung 2 màn HĐBH hay màn riêng | **Dùng chung**, HĐ HRM thay FirmContract | Mở rộng code nguyentrancu97, giữ nhánh HĐ hãng |
| D2 | Làm ở đâu | **Thẳng trên nhánh HĐ bán** | Không tách nhánh / không chờ người khác |
| D3 | Đánh dấu "đã yêu cầu hạch toán" | **Thêm cột như ERP**: `hrm_contract_service_items.exported`, `hrm_contracts.shipping_exported` | 1 migration; logic cờ y hệt HĐ hãng |
| D4 | HTHT gộp DV + CP vào `repair` | **Tách theo ERP**: `revenue_calculation = 0` → nhóm `other_cost` | Bút toán PXK HĐ HRM MỚI đổi tỷ lệ (phiếu đã ghi sổ giữ nguyên) |
| D5 | HĐ trạng thái nào được tạo yêu cầu | **Có hiệu lực (6) + Đang thực hiện (19)** — như YCXH | Hết hiệu lực (20) không tạo được, đợi Gia hạn |
| D6 | ERP còn dùng 2 màn HTDV-HĐBH không | **Còn dùng** ⇒ ERP **không xử lý HĐ HRM** ở 2 màn này | Thêm việc ở repo ERP (mục 4.8) |
| D7 | Giá vốn 632 của dòng DV/CP HĐ HRM | **Theo giá vốn chốt trên HĐ**: `estimated_price × qty` từng dòng | Sửa nhánh HRM của engine giá vốn (mục 4.5) |

**Quyết định của Claude (05/11, sau builder check — user kiểm khi đọc):**
- C1 Không tính lại HTHT cho HĐ cũ: dump prod 21/10 chỉ 1 HĐ HRM, 0 HTHT ⇒ không cần script.
- C2 Cost có `revenue_calculation` NULL (hoặc dòng không `cost_id`) = **Dịch vụ** — khớp màn HĐ / bản in / `isCostItem`. `QuotationExcelExport.php:1206-1210` đang coi NULL là "Không tính doanh thu" — lệch, ghi vào danh sách sửa sau (không sửa trong phase này). Dump prod: 0 dòng thiếu `cost_id`.
- C3 Vận chuyển 1 cột, nghĩa "đã yêu cầu hạch toán": đặt tên `hrm_contracts.shipping_exported` (thay `shipping_exported`). Gửi duyệt bật, Không duyệt gỡ — như dòng DV. Nút "Yêu cầu hạch toán vận chuyển" ẩn từ lúc gửi duyệt; "đang chờ / đã hạch toán" xem ở phiếu yêu cầu.
- C4 Diễn giải D6: ERP **lọc bỏ** phiếu yêu cầu / phiếu hạch toán có `contractable_type` = HĐ HRM ở 2 màn HTDV-HĐBH (danh sách, xem, sửa, lập phiếu, export) — KHÔNG gỡ morphMap toàn cục `Modules\Assign\Entities\Contract\Contract => HrmContract` trong `AppServiceProvider` vì ánh xạ này đang dùng cho `delivery_requests` và chỗ khác.

## 4. Thiết kế

### 4.1 Dữ liệu (1 migration — hrm-api)

`database/migrations/2026_11_xx_xxxxxx_add_service_accounting_flags_to_hrm_contracts.php`
- `hrm_contract_service_items.exported` boolean default false (sau `note`).
- `hrm_contracts.shipping_exported` boolean default false (C3 — nghĩa "đã yêu cầu hạch toán vận chuyển").
- Không backfill (chưa HĐ HRM nào hạch toán DV/CP).

### 4.2 Nguồn dòng của yêu cầu (`ServiceAccountingRequestService::buildCostsFromContract`)

Mở rộng nhận `FirmContract | Contract` (HĐ HRM). Nhánh HĐ HRM:
- **Type 1 Dịch vụ:** `serviceItems` có `costs.revenue_calculation` = 1 hoặc NULL (cùng luật `isCostItem` FE / `ContractPrintService`).
- **Type 2 Chi phí:** `serviceItems` có `costs.revenue_calculation = 0`.
- **Type 3 Vận chuyển:** một dòng ảo dựng từ `shipping_cost` / `shipping_discount` / `shipping_vat_percent` của HĐ (HĐ HRM không có `delivery_extra`).
  - KHÔNG chèn dòng "Chi phí vận chuyển" vào `hrm_contract_service_items` như ERP upsert `FirmContractCost` — bảng này cộng vào tổng HĐ (`recomputeTotals`) ⇒ nhân đôi.
  - Nguồn morph của dòng vận chuyển = chính HĐ (`contract_costable_type` = class HĐ HRM, `contract_costable_id` = id HĐ); cờ = `shipping_exported`.
  - Điều kiện: chưa `shipping_exported` và có `shipping_cost` hoặc `shipping_discount` (tương đương `canRequestAccountingDelivery`).
- Dòng chuẩn hoá giữ đúng khoá FE đang dùng (`contract_costable_id`, `name`, `price`, `value_discount`, `value_extra` = 0, `total_price`, `cost_id`, `vat_percent`, `exported`, `need_export`), thêm `contract_costable_type` để FE gửi lại.
  - Giá trị: `price` = `quoted_price × qty` (trước giảm), `value_discount` = phần giảm giá dòng (`discount_amount` + `allocated_discount_amount`), `total_price` = thành tiền trước VAT sau giảm — **builder đối chiếu với cách `ContractService::recomputeTotals` / `ContractPrintService` đang tính, dùng đúng 1 nguồn, không tự chế công thức mới**.
  - `coefficient_cost_price`: lấy hệ số giá vốn của cost tương ứng (như FirmContractCost) — builder kiểm `costs` có cột này; không có thì 0 và ghi chú.

**Cổng (gate) cho HĐ HRM:**
- Có HTHT (`support_accounting`) — thiếu ⇒ "Hợp đồng không có hỗ trợ hạch toán".
- Trạng thái ∈ {6, 19} (D5) và người lập HĐ = người đăng nhập — dùng chung tinh thần `Contract::EXPORTABLE_STATUSES` + `assertContractCreatedByMe` của YCXH.
- Màn Sửa (`$forEdit`) bỏ gate chọn HĐ như nhánh HĐ hãng.

### 4.3 Lưu / không duyệt / xoá yêu cầu

- `syncCosts`: tra nguồn theo **cặp (`contract_costable_type`, `contract_costable_id`)** thay vì `FirmContractCost::find(id)` — id 2 bảng có thể trùng. Nguồn `exported` (hoặc HĐ `shipping_exported`) ⇒ chặn cả phiếu như hiện tại. Gửi duyệt (status Chờ duyệt) ⇒ bật cờ.
- `rollbackAccounting` (Không duyệt): gỡ cờ cả 3 loại nguồn (FirmContractCost.exported · ContractServiceItem.exported · Contract.shipping_exported).
- `store`: nhận `contract_type` (`firm` | `hrm`) + `contract_id` (giữ tương thích `firm_contract_id` cũ) ⇒ ghi `contractable_type` / `contractable_id` tương ứng (HĐ HRM lưu nguyên tên class, đúng quy ước `AccountDetail::CONTRACTABLE_HRM_CONTRACT`, không map sang chuỗi ERP).
- `findForShow` / `detailData` / danh sách / export: `morphWith` thêm HĐ HRM (customer, người lập) và các khoá hiển thị (mã HĐ, KH, NVKD) lấy đúng cột của HĐ HRM.
- Thông báo, lịch sử, quyền: giữ nguyên (quyền theo mã đã có: xem yêu cầu `customer_care.yeu_cau_hach_toan_lam_dich_vu.view`, hạch toán `accounting.hach_toan_yeu_cau_lam_dich_vu.create`, xem phiếu `customer_care.hach_toan_dich_vu.view`).

### 4.4 HTHT tách chi phí (D4) — `Modules/Assign/Services/ContractSupportAccountingService.php`

- `getAccountingInfo` (dòng ~58-69): dòng `revenue_calculation = 0` vào nhóm `other` (→ `*_other_cost`), còn lại vào `repair` (→ `*_repair_service`). Vận chuyển giữ nhóm `delivery`.
- Ảnh hưởng: tỷ lệ phân bổ (`pct_wo_delivery`, `pct_wo_cost`) của bút toán PXK HĐ HRM (`ProductExportPostingService::prepareData`) và phiếu hạch toán dịch vụ. Chỉ áp cho lần tính HTHT sau khi sửa; `account_details` đã ghi không đổi.
- Builder kiểm lại nơi khác đọc `before_vat_repair_service` / `*_other_cost` của HĐ HRM (màn HTHT, in, thưởng) để không lệch.

### 4.5 Phiếu hạch toán + ghi sổ (`ServiceAccountingService`, `FirmContractServiceAccountingPostingService`)

- Engine dùng được cho HĐ HRM, chỉ đổi:
  - `prepareData`: % VAT type 1/2 lấy từ dòng nguồn đầu tiên của HĐ HRM (`serviceItems` lọc theo loại) — tương đương `revenue_costs[0]` / `costs[0]`; type 3 lấy `shipping_vat_percent`.
  - `loadRichSupportAccounting`: `contractable_type` theo đúng HĐ của phiếu (HĐ HRM ⇒ class HĐ HRM).
  - Đổi tên class thành tên trung tính (vd `ContractServiceAccountingPostingService`) hoặc giữ tên + docblock ghi rõ nhận cả 2 — builder chọn, ưu tiên ít đụng.
- `ServiceAccountingService` ghi sổ: nhánh `contractable_type` = HĐ HRM ⇒ meta `contractable_type = AccountDetail::CONTRACTABLE_HRM_CONTRACT`, mã HĐ HRM; bỏ nhánh PLBS. Tổ chức (company / department / part) theo HĐ HRM (HĐ HRM CÓ cột tổ chức — dùng của HĐ, khác HĐ hãng phải lấy theo người lập).
- Vận chuyển: cờ `shipping_exported` đã bật từ lúc gửi duyệt yêu cầu (C3) — phiếu hạch toán không bật thêm cờ nào.
- **Giá vốn (D7):** nhánh HĐ HRM của `costAccountingSa` lấy giá vốn = `estimated_price × qty` của dòng `hrm_contract_service_items` nguồn (chụp vào `service_accounting_request_costs` / `service_accounting_costs` lúc tạo để phiếu không đổi khi HĐ sửa — builder chọn cột chụp: dùng lại `coefficient_cost_price` quy đổi hoặc cột giá vốn sẵn có `service_accounting_costs.cost_price`). Vận chuyển (type 3) không có giá vốn như ERP.
- `invoiceable_type` giữ `ServiceAccounting::INVOICEABLE_TYPE` (`App\Model\Sale\ServiceAccounting`) ⇒ công nợ 131 tự cộng (`CustomerDebtAggregator`).

### 4.6 HĐ chuyển "Đang thực hiện"

- Thêm `ServiceAccounting::INVOICEABLE_TYPE => 'hạch toán dịch vụ'` vào `ContractService::IN_PROGRESS_LEDGER_TYPES`.
- Theo DTH-Q3 đã chốt (05/11): chỉ quét bù trong lệnh 00:20 `assign:activate-signed-contracts`, không móc vào service Finance. Mốc: ghi sổ SAU lúc HĐ có hiệu lực (logic `firstLedgerSinceEffective` sẵn có).

### 4.8 ERP (repo `ERP/TanPhatDev`, nhánh `gop_db`) — D6 / C4

- `app/Model/Sale/ServiceAccountingRequest::searchByFilter` và `app/Model/Sale/ServiceAccounting` (danh sách + đếm dashboard `HomeController` + export): loại `contractable_type = 'Modules\Assign\Entities\Contract\Contract'` (và alias nếu có).
- `show` / `edit` / `update` / `reject` / tạo Phiếu hạch toán từ yêu cầu của HĐ HRM: chặn (404 / thông báo "Phiếu của hợp đồng HRM — xử lý trên HRM").
- Không đổi morphMap toàn cục.
- Builder kiểm thêm báo cáo ERP đọc `service_accounting` (`MonitorContractImplementService`, quyết toán HĐ hãng) — chỉ join theo HĐ hãng thì không phải sửa.

### 4.7 FE (hrm-client)

- **Màn chi tiết HĐ HRM** (`pages/assign/contracts/_id/index.vue`): 3 nút "Yêu cầu hạch toán dịch vụ" / "… chi phí" / "… vận chuyển" (ẩn khi không đủ điều kiện — cờ BE `is_can_request_service_accounting` / `…_cost` / `…_shipping` trong `DetailContractResource`), mở `/finance/service-accounting-requests/create?hrm_contract_id=…&type=…`. Khuôn: nút YCXH hiện có (`goToCreateExportRequest`). Nút theo `button-convention`.
- **Form yêu cầu** (`ServiceAccountingRequestForm.vue` + `FirmContractPickerModal.vue`): ô chọn HĐ liệt kê **cả 2 loại** (HĐ hãng + HĐ HRM đủ điều kiện) — BE thêm endpoint/nhánh danh sách HĐ HRM (hoặc gộp vào `/firm-contracts` kèm `contract_type`); prefill từ query `hrm_contract_id`. Hiển thị loại HĐ để phân biệt.
- **Chi tiết yêu cầu / phiếu hạch toán:** link mã HĐ trỏ đúng màn (HĐ HRM ⇒ `/assign/contracts/{id}`).
- **HTHT** màn HĐ: chi phí hiện ở dòng "Chi phí khác".
- Mọi thay đổi FE kiểm bằng Playwright (đo DOM) + bổ sung e2e.

## 5. Ràng buộc

- Nhánh mang rbac — không push khi chưa có lệnh; hook chặn push.
- Phạm vi repo: hrm-api + hrm-client (worktree) **+ ERP `TanPhatDev`** (D6) — hỏi phép riêng khi code từng repo.
- Không đổi hành vi HĐ hãng: mọi nhánh mới rẽ theo `contractable_type`.
- Theo quy ước gop_db: không dùng connection `mysql2`; HĐ HRM lưu morph bằng tên class HRM.
- Quyền: dùng mã đã có trong Catalog (không thêm quyền mới). `permission:catalog-sync` thật vào DB là việc riêng (chưa chạy).

## 6. Kiểm thử

- BE: tinker/feature trên rehearsal — tạo yêu cầu 3 loại cho HĐ HRM; gửi duyệt bật cờ; không duyệt gỡ cờ; dòng đã cờ bị chặn; phiếu "Lưu và duyệt" ghi đủ bút toán (so tổng Nợ = tổng Có từng nhóm, TK đúng như bảng ERP) với `contractable_type` HĐ HRM; vận chuyển bật `shipping_exported`; HĐ hãng chạy lại test có sẵn (`Modules/Finance/Tests/Feature/ServiceAccounting*`, `FirmContractServiceAccountingPostingTest`) vẫn xanh.
- HTHT: so before/after tách chi phí trên 1 HĐ có CP; bút toán PXK mới dùng tỷ lệ mới.
- Lệnh 00:20: HĐ có phiếu HTDV ghi sổ sau hiệu lực ⇒ 19.
- FE: Playwright 3 nút ở chi tiết HĐ (đủ / thiếu điều kiện), picker 2 loại HĐ, tạo yêu cầu từ HĐ HRM, chi tiết yêu cầu / phiếu hiện đúng HĐ; e2e mới cho luồng.

## 7. Để builder quyết

- Tên class engine (giữ / đổi trung tính).
- Gộp hay tách endpoint danh sách HĐ cho picker.
- Chi tiết công thức `price` / `value_discount` / `total_price` của dòng service item — miễn đúng nguồn với tổng HĐ.
