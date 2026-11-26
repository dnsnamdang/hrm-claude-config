# #10631 — Hợp đồng bán: thêm cột Model (ERP)

> Redmine #10631 [Kinh doanh_task 9663]. ERP (erp.eteksofts.com, repo `TanPhatDev`), branch `develop_02`.
> Thêm cột **Model** (model của hàng hóa, bind `model_name`) vào các bảng hàng hóa còn thiếu.

## Ý đồ / vì sao
Một số màn trong cụm Hợp đồng bán chưa hiển thị cột **Model** của hàng hóa (model = `products.model_id` → `product_models.name`, snapshot vào `firm_contract_tab_products.model_name`). Cần bổ sung để KD xem được model ngay trên bảng, đồng bộ với các màn đã có.

## Phạm vi thật (đã điều tra tới gốc)
Ticket liệt kê 4 mục, nhưng recon cho thấy phần lớn **đã có sẵn**:

| # | Ticket | Màn thật | Hiện trạng | Việc |
|---|---|---|---|---|
| 1 | HĐ bán tạo/xem/sửa/DS | `sale/firm/contracts/*` + index DataTable | ✅ đã có cột Model | — |
| 2 | PL giảm HĐ VT-HH-TB (tạo+xem) | `sale/firm/annexes/form` + `show` | tạo: có `<th>` nhưng **trống data**; xem: **thiếu cột** | BE + FE |
| 3 | ĐHNT tab hàng hóa | `sale/firm/orders/form` (tab Hàng hóa) | **thiếu cột** (payload đã có `model_name`) | FE |
| 4 | PL giảm HĐ dự án | = `annexes/form`+`show` với `contract_type=6` | **trùng #2** | gộp #2 |

**Chốt nghi vấn màn #4:** menu `topmenubar.blade.php` — mục "Hợp đồng dự án" → "Phụ lục giảm" trỏ `firmContractAnnexes.index?contract_type=6` (dòng 590), nhãn "Phụ lục giảm hợp đồng dự án" (dòng 2129). ⇒ dùng **chung** controller `FirmContractAnnexesController` / service `FirmContractAnnexService` / view `sale/firm/annexes/` với PL giảm HĐ bán, chỉ khác `contract_type`. Màn `contract_annexes`/`App\Contract` là hệ cũ khác — KHÔNG thuộc ticket.

## Gốc rễ "màn tạo PL giảm trống Model"
`FirmContractAnnexService::getDataForAnnex()` (dòng 94-97) có SELECT **tường minh** không kèm `fctp.model_name`/`model_id`. View `annexes/form.blade.php` đã có `<th>Model` (:166) + row `product.model_name || ''` (:206) nhưng data không về ⇒ cột trống. Cột `firm_contract_tab_products.model_name`/`model_id` tồn tại thật (model fillable :35-36). Sửa SELECT là mấu chốt, cấp data cho cả màn tạo (th sẵn) lẫn màn xem (sau khi thêm th).

## Mục tiêu / không mục tiêu
- **Mục tiêu:** hiện cột Model (read-only) ở 3 màn còn thiếu, đúng vị trí **Tên hàng → Model → Mã hàng**, bind `<% product.model_name %>`, đồng bộ các màn đã có.
- **Không mục tiêu:** đụng logic tính toán/lưu; sửa màn HĐ bán (đã có); hệ `contract_annexes` cũ; màn ĐHNT nha khoa `zt.*`.
- **Anti-goal:** thêm join runtime hay bảng mới — model_name đã snapshot sẵn, chỉ SELECT thêm.

## Phương án (1 cách duy nhất)
Bám pattern `model_name` sẵn có (các màn HĐ bán đã làm y hệt). Không có phương án thay thế đáng cân nhắc — chỉ là thêm cột hiển thị.

### Chạm file
- **BE:** `app/Services/Sale/Firm/Contract/FirmContractAnnexService.php:94-97` — thêm `'fctp.model_name'`, `'fctp.model_id'` vào SELECT `getDataForAnnex()`. Phủ PL giảm HĐ bán + HĐ dự án (ct=6) + ĐHNT phụ lục giảm (ct=10) vì chung service.
- **FE1:** `resources/views/sale/firm/annexes/show.blade.php` — `<th rowspan="2">Model</th>` giữa :169/:170; `<td><% product.model_name || '' %></td>` giữa :193/:194.
- **FE2:** `resources/views/sale/firm/orders/form.blade.php` (tab Hàng hóa) — `<th rowspan="2">Model</th>` sau "Tên hàng" (:299); `<td><% product.model_name %></td>` sau ô product_name (:319).

### Kiểm thử
Playwright trên form ERP thật: (a) màn tạo + xem PL giảm → Model có giá trị sau sửa BE; (b) tab Hàng hóa ĐHNT → cột Model hiện đúng.

## Ràng buộc
- ERP = Laravel 6, Blade + AngularJS 1.3.9, interpolation `<% %>`.
- Không commit/push/gop_db khi chưa có yêu cầu rõ.
