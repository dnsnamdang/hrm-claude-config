# Design — Chương trình khuyến mại: Phạm vi áp dụng (Chọn khách hàng + Bảng giá)

## Mục tiêu
Sửa tab **"Phạm vi áp dụng"** của Chương trình khuyến mại (`new_combo_categories`, model `ComboCategory`, bảng `combo_categories`) trên cả 4 chế độ dùng chung form (Thêm/Sửa/Duyệt/Xem):
- Khối **Khách hàng**: đổi "Nhóm khách hàng" → **"Chọn khách hàng"** (chọn từng KH cụ thể, multi-select ajax).
- Thêm khối **Bảng giá**: ○ Toàn bộ bảng giá / ○ Chọn bảng giá → multi-select `price_types`.
- 2 khối độc lập (có thể kết hợp). Giữ nguyên 2 khối **Công ty** và **Nhân viên**.

## Quyết định đã chốt (brainstorming)
- Khối Khách hàng và Bảng giá là **2 cụm radio riêng** (B) — có thể vừa giới hạn KH vừa giới hạn bảng giá.
- "Chọn khách hàng" = KH cụ thể, nguồn `Customer`, search ajax (`customers.searchCustomerByKeywords`).
- "Bảng giá" = `price_types` (biến global `price_types`, model `PriceType`).
- **Enforce ngay (1B)**: sửa `checkActive` để áp KM thực tế theo KH cụ thể + bảng giá.
- **KM cũ (2iii)**: KHÔNG migrate. Pivot KH rỗng (KM cũ) ⇒ coi như không giới hạn KH (legacy-safe), tránh làm KM cũ chết.
- Cột/pivot "nhóm khách hàng" cũ KHÔNG drop, chỉ ngừng dùng ở form mới.

## Hiện trạng (đã khảo sát)
- Form chung: `resources/views/sale/new_combo_categories/form.blade.php`, tab `#pham_vi` (dòng ~126-216). Khối KH dòng ~158-184 (radio `form.customers` 1/2 + multi-select `form.customer_groups`, `ng-disabled="form.customers != 2"`).
- Class AngularJS: `resources/views/partials/classes/sale/ComboCategory.blade.php` (`all_customer_groups` = `CustomerGroup::getForSelect()`).
- Model `ComboCategory` (`app/Model/Sale/ComboCategory.php`): cờ int `customers` (1=toàn bộ, 2=một phần — hằng `MOT_PHAN`); quan hệ `customer_groups()` (belongsToMany pivot `combo_category_has_customer_groups`).
- Controller `app/Http/Controllers/Sale/NewComboCategoryController.php`: validate + sync ở `store()` (~232-477) và `update()` (~479-772). Trường hiện tại: `customers`, `customer_groups[]`.
- Enforce: `ComboCategory::checkActive($id,$customer_id,$employee_id)` (preview, dòng 168-194) và `ComboCampaign::checkActive($id,$customer_id,$employee_id)` (áp KM thật, dòng 354-381) — nhánh `customers==MOT_PHAN` lọc theo nhóm KH của khách (`CustomerHasGroup` → `ComboCategoryHasCustomerGroup`).
- Call site áp KM thật (đều có sẵn `price_type` trên chứng từ): `Contract.php:2474`, `Model/Sale/Firm/Quotation/FirmQuotation.php:551`, `Quotation.php:270`, `Model/Warehouse/ProductExportRequest.php:2013`, `Model/Sale/ContractAdditionAnnex.php:125`; preview: `NewComboCategoryController:169,191`.
- `PromoCampaign` là feature khác (tab riêng) → NGOÀI phạm vi.

## DB (migration mới)
1. Thêm cột: `combo_categories.price_lists` `unsignedTinyInteger` default 1 (1=toàn bộ bảng giá, 2=chọn).
2. Pivot `combo_category_has_customers`: `id`, `combo_category_id`, `customer_id`, timestamps. (KH cụ thể)
3. Pivot `combo_category_has_price_types`: `id`, `combo_category_id`, `price_type_id`, timestamps. (Bảng giá)
- Giữ nguyên `customers` (cờ 1/2), `customer_group_id`, pivot `combo_category_has_customer_groups` (legacy, không dùng ở form mới).

## Model `ComboCategory`
- Thêm quan hệ:
  - `applied_customers()` → belongsToMany `Customer` qua `combo_category_has_customers` (KHÔNG đặt tên `customers()` vì trùng cột cờ int).
  - `price_types()` → belongsToMany `PriceType` qua `combo_category_has_price_types`.
- Eager-load thêm 2 quan hệ này ở các hàm trả data cho edit/show (chỗ đang load `customer_groups`).
- Hằng cờ tái dùng `MOT_PHAN`/`TOAN_BO` cho cả `customers` và `price_lists`.

## BE — store() & update()
- Validate (thay block nhóm KH):
  - `customers` => `required|in:1,2`
  - `customer_ids` => `required_if:customers,2|nullable|array|min:1`
  - `customer_ids.*` => `exists:customers,id`
  - `price_lists` => `required|in:1,2`
  - `price_list_ids` => `required_if:price_lists,2|nullable|array|min:1`
  - `price_list_ids.*` => `exists:price_types,id`
  - Message lỗi "Bắt buộc phải chọn" như cũ; rethrow `ValidationException` (không catch chung).
- Gán: `$object->customers = $request->customers; $object->price_lists = $request->price_lists;`
- Sync:
  - `customers==2` → `$object->applied_customers()->sync($request->customer_ids)`; else `->sync([])`.
  - `price_lists==2` → `$object->price_types()->sync($request->price_list_ids)`; else `->sync([])`.
- Bỏ sync `customer_groups` ở luồng mới (giữ code cũ không gọi, hoặc xoá nhánh nhóm KH).

## FE — form.blade.php (#pham_vi) + class ComboCategory
- Khối Khách hàng:
  - Radio `form.customers` 1/2; label option 2 đổi "Nhóm khách hàng" → **"Chọn khách hàng"**.
  - Đổi multi-select: từ `form.customer_groups`/`all_customer_groups` → **`form.customer_ids`** dùng **select2 ajax** (search KH, route `customers.searchCustomerByKeywords`), `ng-disabled="form.customers != 2"`, lỗi inline `required` khi `customers==2`.
- Khối Bảng giá (mới, đặt cạnh/ dưới khối KH bên phải):
  - Radio `form.price_lists` 1/2 (Toàn bộ bảng giá / Chọn bảng giá).
  - Multi-select `form.price_list_ids` từ `price_types` (global), `ng-disabled="form.price_lists != 2"`, lỗi inline `required` khi `price_lists==2`.
- Class `ComboCategory.blade.php`:
  - Khởi tạo `price_lists` mặc định 1; map `customer_ids`, `price_list_ids` (id) từ data khi edit/show; preload nhãn KH đã chọn cho select2 ajax (dữ liệu KH kèm tên trong @json data edit).
  - Bỏ `all_customer_groups` ở luồng mới (giữ nếu còn dùng nơi khác — kiểm tra trước khi xoá).
- 4 chế độ dùng chung form → show/duyệt readonly tự áp dụng (giữ pattern disabled hiện có).

## Enforce (downstream) — 1B
Sửa **cả** `ComboCategory::checkActive` (preview) và `ComboCampaign::checkActive` (áp KM thật), thêm tham số `$price_type` (nullable):
- Nhánh khách hàng (`customers == MOT_PHAN`):
  - Lấy `$ids = combo_category_has_customers.pluck(customer_id)`.
  - **Legacy-safe**: nếu `$ids` rỗng → bỏ qua (không chặn) — đúng quyết định 2iii cho KM cũ.
  - Nếu có → `if (!in_array($customer_id,$ids)) return false`.
- Nhánh bảng giá (`price_lists == MOT_PHAN`):
  - Lấy `$pt = combo_category_has_price_types.pluck(price_type_id)`.
  - Nếu rỗng → bỏ qua; nếu có → `if (empty($price_type) || !in_array($price_type,$pt)) return false`.
- Giữ nguyên 2 nhánh `scope` (công ty) và `sellers` (phòng ban).
- Bỏ phụ thuộc nhóm KH ở nhánh khách hàng (legacy pivot không còn được đọc).
- Truyền `price_type` tại call site (đều có sẵn): `Contract` (`$this->price_type`), `FirmQuotation`, `Quotation`, `ProductExportRequest`, `ContractAdditionAnnex`, 2 controller preview (lấy từ request/chứng từ). Tham số mặc định null để call site chưa truyền vẫn chạy (chỉ không enforce bảng giá).

## Edge cases / rủi ro
- Trùng tên `customers` (cờ int) vs quan hệ → dùng tên quan hệ khác (`applied_customers`).
- KH rất nhiều → bắt buộc select2 ajax (không nhồi toàn bộ KH vào @json).
- KM cũ: `price_lists` mặc định 1 (không giới hạn) ⇒ không ảnh hưởng; `customers=2` cũ pivot KH rỗng ⇒ legacy-safe bỏ qua.
- `ComboCampaign::checkActive` đọc category cha → đảm bảo load đúng cờ + pivot mới.
- Đảm bảo show/duyệt readonly hiển thị đúng KH đã chọn (preload nhãn) + bảng giá đã chọn.

## Phân quyền
- Không thêm quyền mới (theo quyền hiện có của new_combo_categories). Route store/update giữ middleware hiện tại.

## Phân phase (đề xuất)
- **Phase 1 — Form + lưu**: migration (cột + 2 pivot), model quan hệ, FE 2 khối, BE store/update + validate. Verify nhập/sửa/duyệt/xem + lưu đúng.
- **Phase 2 — Enforce**: sửa `checkActive` (2 model) + truyền `price_type` tại các call site. Verify áp KM thực tế theo KH cụ thể & bảng giá; KM cũ không vỡ.

## Out of scope
- `PromoCampaign`, `ComboCampaign` form (chỉ sửa `ComboCampaign::checkActive` cho enforce).
- Bản in, báo cáo, Excel — không đụng.
- Không migrate dữ liệu KM cũ.
