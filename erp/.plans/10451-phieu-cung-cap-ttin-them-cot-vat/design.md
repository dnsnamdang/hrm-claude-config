# #10451 — Phiếu cung cấp thông tin: thêm cột VAT / Tiền VAT / Thành tiền sau VAT

> Placeholder — sẽ fill sau brainstorming.

## Nguồn
- Redmine #10451 [CSKH] (TPE GỬI), tác giả Trịnh Lợi, status Mới.
- Link lỗi: `/admin/customer-care/warranty_repair_information_requests/8162/show`
- Ảnh: scratchpad `rm10451/att-13845.png` — ô đỏ đánh dấu 3 cột cần chèn giữa "Thành tiền sau chiết khấu" và "Thời gian có vật tư (ngày)", mục B/I (Công 1.1, Danh sách dịch vụ 1.2, Danh sách vật tư 1.3).

## Yêu cầu (thô)
Thêm 3 trường **VAT (%) · Tiền VAT · Thành tiền sau VAT** vào màn *Phiếu cung cấp thông tin* (warranty_repair_information_requests) ở mục công / dịch vụ / vật tư, **tương tự màn báo giá dịch vụ** (service_quotations).

## Hiện trạng (đã truy gốc qua Explore)
- 2 màn *Phiếu cung cấp thông tin* (warranty_repair_information_requests) và *Báo giá dịch vụ* (service_quotations) **dùng chung** model `WrServiceQuotation` + cùng bảng con `wr_service_quotation_*` + cùng `syncProduct()` (controller đích `store()` tạo `new WrServiceQuotation()`).
- Mục B/I = bảng `product_repairs`, render ở `warranty_repair_information_requests/form.blade.php:363-569`. Header `:366-379`: ...Chiết khấu(373) · Thành tiền sau CK(374) · Loại công việc(375) · Thời gian có vật tư(376)... — **chưa có cột VAT** (grep "VAT" rỗng).
- 3 nhóm dòng: Công (`:413-441`, ô TT sau CK `:430`) · Danh sách dịch vụ (`ng-repeat choose_services :461-504`, `:488`) · Danh sách vật tư (`ng-repeat choose_product_items :525-566`, `:550`).
- Cột `vat_percent` (float 8,2 default 0) **ĐÃ CÓ** trên cả 3 bảng con (migration 2025_07_25); fillable sẵn → `syncProduct()` **đã lưu tự động**. BE `create()` khởi tạo `vat_percent` mặc định từ master.
- **JS getter đã có sẵn ở màn đích**: `vat_cost` + `total_cost_after_vat` trong ProductInformation.blade.php (Công :186-191), ProductInformationService.blade.php (DV :141-146), ProductInformationProduct.blade.php (Vật tư :133-138). `toSave` đã gửi `vat_percent`.
  - Công thức: `Tiền VAT = total_cost_after_discount * vat_percent/100`; `Thành tiền sau VAT = total_cost_after_discount + Tiền VAT`.
- Màn tham chiếu `service_quotations/form.blade.php`: 3 cột VAT đặt sau "Loại công việc" (`:437-439`), VAT% **chỉ đọc** (auto từ master, không input), Tiền VAT/TT sau VAT tính runtime không lưu.

## Quyết định (short design — chờ duyệt)
- **Approach chốt:** CHỈ sửa FE `warranty_repair_information_requests/form.blade.php` — thêm 3 `<th>` (sau "Loại công việc" :375) + 3 `<td>` cho mỗi nhóm (sau ô "Thành tiền sau chiết khấu"), bind getter sẵn có `vat_percent` / `vat_cost | number` / `total_cost_after_vat | number`. Chèn ô trống tương ứng ở dòng header-nhóm + dòng thiết bị cha để không lệch cột. **KHÔNG migration, KHÔNG sửa BE** (đã sẵn).
- **Alternatives loại bỏ:** (a) thêm migration + lưu BE — thừa, đã có; (b) VAT% nhập tay per-dòng — màn tham chiếu để chỉ đọc auto từ master, làm khác sẽ lệch nghiệp vụ.
- **Phạm vi user chốt:** Form + Xem + Bản in.

## Recon show + print (bổ sung sau khi chốt phạm vi)
- **show.blade.php (76 dòng):** chỉ `@extends layouts.app` + `ng-controller="WarrantyRepairRequest"` → **`@include('...form')`** (dòng 17) ở chế độ readonly. ⇒ Sửa `form.blade.php` là **tự động áp cho màn Xem**, không cần đụng show.
- **Bản in:** controller `print($id)` (`WarrantyRepairInformationRequestsController.php:629`) dùng `App\Services\PrintTemplate\WarrantyRepairServiceQuotationPrint` — **DÙNG CHUNG** với màn báo giá DV (`WarrantyRepairServiceQuotationsController` cũng gọi service này). Bảng `product_repairs_table` trong `getTable()` **ĐÃ CÓ sẵn 3 cột VAT per-dòng**: header `:1226-1228` (colspan 11); data-row phát đủ 3 `<td>` cho Công (`:932/937/938`), Dịch vụ (service), Vật tư (product_item). ⇒ **Bản in đã khớp sẵn, KHÔNG cần sửa.**

## KẾT LUẬN PHẠM VI THẬT
Chỉ sửa **1 file FE**: `resources/views/customercare/warranty_repair_information_requests/form.blade.php`. Show tự khớp; print đã xong. Không migration, không BE.
