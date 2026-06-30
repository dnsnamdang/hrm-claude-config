# Phase 3 Report — BE lưu cha-con BG + carryover sang HĐ

## Tổng quan

Phase 3 implement logic BE cho quan hệ cha-con sản phẩm trong báo giá và carryover sang hợp đồng.
Tất cả thay đổi backward-compatible: dòng không có `child_parent_id` (null) chạy như cũ.

---

## TASK 3.1 — syncProducts lưu cha-con khi store/update báo giá

**File:** `app/Services/Sale/Firm/Quotation/FirmQuotationService.php` (dòng 345–401)

**Thay đổi:** Thêm `$tmpToReal = []` map ngoài vòng lặp. Trong vòng lặp:
- Tách `tmp_row_id`, `child_parent_tmp_id` ra khỏi `$pro` trước `fill()` và `unset($pro['child_parent_id'])` để tránh fill nhầm id tạm vào cột DB.
- Sau `$p->save()`: set `$tmpToReal[$tmp_row_id] = $p->id` để các dòng con phía sau resolve được.
- Resolve `child_parent_id` từ map: nếu `child_parent_tmp_id` có trong `$tmpToReal` → set `$p->child_parent_id = $tmpToReal[...]`, ngược lại set `null`.
- Set `child_ratio = (int)$pro['child_ratio']` nếu có, ngược lại `null`.

**Tab vs Group:** `syncProducts()` là method dùng chung cho cả tab (`FirmQuotationTabProduct`) và group (`FirmQuotationGroupProduct`) thông qua tham số `$model_class`. Thay đổi áp dụng cho cả hai — không cần xử lý riêng.

**FE contract:** FE đảm bảo dòng CHA đứng trước CON trong mảng `products` khi gửi lên. Map `tmp→real` chỉ cần duyệt 1 lượt (O(n)).

---

## TASK 3.2 — Validate cha-con khi store/update báo giá

**File:** `app/Http/Requests/Sale/Firm/Quotation/CreateFirmQuotationRequest.php` (toàn bộ)
**File:** `app/Http/Requests/Sale/Firm/Quotation/UpdateFirmQuotationRequest.php` (toàn bộ)

**Thay đổi:**

1. **Import thêm** `use Illuminate\Validation\ValidationException;` (dự phòng tương lai nếu cần throw trực tiếp).

2. **Rule mới** trong `rules()`:
   - `'tabs.*.products.*.child_ratio' => 'nullable|integer|min:1'`
   - `'groups.*.products.*.child_ratio' => 'nullable|integer|min:1'`

3. **Method `withValidator($validator)`** — chạy sau validate cơ bản pass, dùng `$validator->after(...)`:
   - Duyệt products của từng tab và group.
   - Gọi `checkParentChildProducts(array $products)` — helper protected.

4. **Method `checkParentChildProducts(array $products)`:**
   - **Rule 1:** Dòng có `child_parent_tmp_id` không rỗng → bắt buộc `child_ratio >= 1`. Trả lỗi nếu vi phạm.
   - **Rule 2:** Cấm cấp 3 — build set `$parentTmpIds` (các tmp_row_id được dùng làm CHA), sau đó nếu 1 dòng vừa là CHA vừa có `child_parent_tmp_id` → trả lỗi "cấm cấp 3".

**Lý do dùng `withValidator` thay vì throw trong controller:** FormRequest của Laravel expose hook này đúng chỗ, không break flow validation chuẩn, và lỗi tự động convert sang `ValidationException` với format đồng nhất với các lỗi khác (FE nhận `errors.products[0]`).

---

## TASK 3.3 — Carryover cha-con BG → HĐ (remap id)

**File:** `app/Services/Sale/Firm/Contract/FirmContractService.php`, method `syncTabsFromQuotation` (dòng 605–760+)

**Thay đổi:**

1. **Khai báo 2 map** trước vòng lặp tab:
   - `$quotationToContract = []` — quotation_product_id → contract_product_id
   - `$contractByQuotationId = []` — quotation_product_id → FirmContractTabProduct instance

2. **Trước `$firm_contract_product->fill($p_attributes)`:** `unset($p_attributes['child_parent_id'], $p_attributes['child_ratio'])` — đảm bảo không mang nhầm id BG vào HĐ.

3. **Sau `$firm_contract_product->save()`:** Ghi vào 2 map dùng `$firm_quotation_product->id` làm key.

4. **Lượt 2** sau khi kết thúc toàn bộ vòng lặp tab — remap quan hệ cha-con:
   ```php
   foreach ($contractByQuotationId as $qId => $contractProduct) {
       $qProduct = FirmQuotationTabProduct::query()->find($qId);
       if ($qProduct && $qProduct->child_parent_id
           && isset($quotationToContract[$qProduct->child_parent_id])) {
           $contractProduct->child_parent_id = $quotationToContract[$qProduct->child_parent_id];
           $contractProduct->child_ratio = $qProduct->child_ratio;
           $contractProduct->save();
       }
   }
   ```
   `FirmQuotationTabProduct` đã được import sẵn trong file (dùng ở dòng 613 vòng lặp tab).

**Lưu ý cấu trúc thực tế:** `syncTabsFromQuotation` và `syncGroupsFromQuotation` là 2 method riêng biệt. Task 3.3 chỉ yêu cầu sửa tab. Group dùng `FirmContractGroupProduct` — sẽ xử lý ở phase sau nếu cần.

---

## TASK 3.4 — HĐ khoá cấu trúc cha-con

**File:** `app/Http/Controllers/Sale/Firm/FirmContractController.php`

**Thay đổi:** Thêm comment docblock trước `$storeValues = $request->only([...])` ở cả `store()` và `update()`:

> "THIẾT KẾ: quan hệ cha-con sản phẩm HĐ (child_parent_id / child_ratio) được thiết lập DUY NHẤT qua carryover từ BG trong FirmContractService::syncTabsFromQuotation(). Không nhận 2 trường này từ request HĐ để tránh inconsistency với cấu trúc BG gốc."

**Lý do chỉ comment, không thêm logic:** Kiểm tra code thực tế: `$request->only([...])` trong `store()` và `update()` không include `child_parent_id` hay `child_ratio`. Hai cột này không có trong danh sách `only()`, không có trong `FirmContractStoreRequest::rules()` hay `FirmContractUpdateRequest::rules()`. Không có đường nào set 2 cột này từ request HĐ → chỉ cần comment ghi rõ thiết kế là đủ.

---

## php -l Results

```
No syntax errors detected in FirmQuotationService.php
No syntax errors detected in CreateFirmQuotationRequest.php
No syntax errors detected in UpdateFirmQuotationRequest.php
No syntax errors detected in FirmContractService.php
No syntax errors detected in FirmContractController.php
```

5/5 file sạch.

---

## Concerns & Ghi chú

1. **syncGroupsFromQuotation:** Tương tự `syncTabsFromQuotation`, method xử lý group (`syncGroupsFromQuotation` dòng 709+) cũng copy `FirmContractGroupProduct` từ BG. Phase 3 không yêu cầu sửa group-side của HĐ. Nếu sau này cần carryover cha-con cho group HĐ, áp dụng pattern tương tự.

2. **`withValidator` không phải `passedValidation`:** Dùng `withValidator` vì nó chạy SAU validate rules nhưng VẪN trong pipeline FormRequest, lỗi được merge vào `$validator->errors()` và tự động raise `ValidationException` đúng format. Không dùng `passedValidation` (chạy sau khi tất cả pass, không thể add error).

3. **Import `ValidationException`** trong Request files: được thêm vào nhưng không dùng trực tiếp trong implementation hiện tại (dùng `$validator->errors()->add()` thay). Giữ lại để sẵn sàng nếu cần throw thủ công sau.
