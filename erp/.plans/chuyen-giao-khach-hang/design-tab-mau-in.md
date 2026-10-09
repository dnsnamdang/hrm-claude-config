# Design — Tab "Mẫu in" (phiếu YC chuyển giao khách hàng)

## Mục tiêu
Cho phép sửa **mẫu in của hợp đồng** ngay trong tab "Mẫu in" của phiếu YC chuyển giao KH.
Nội dung sửa được **lưu nháp trên phiếu**; **khi phiếu Đã duyệt** thì ghi mẫu in đã sửa vào HĐ →
màn view + in HĐ hiển thị mẫu mới. (Lý do: mẫu in là HTML nhúng sẵn thông tin KH cũ, sau chuyển
giao KH thì phải cập nhật.)

## Quyết định đã chốt (brainstorming)
- **Sửa tay** bằng CKEditor (không auto tìm–thay).
- **Lưu nháp trên phiếu**, chỉ **áp vào HĐ khi DUYỆT** (trước đó HĐ giữ nguyên).
- Áp cho **cả 2 loại HĐ**: HĐ Hãng (FirmContract → `template_print_product`), HĐ Dịch vụ (WrServiceContract → `template`).
- **Chỉ HĐ chính** (không đụng phụ lục).
- Prefill editor = mẫu in **hiện tại** của HĐ.
- Không lưu bản cũ (không audit before/after) — YAGNI.

## Data model
Migration: thêm cột vào `customer_handover_requests`:
- `new_template_print` — `LONGTEXT` nullable — mẫu in nháp đã sửa (HTML).

Model `CustomerHandoverRequest`: thêm `new_template_print` vào `$fillable`.

## Hiện trạng liên quan (đã khảo sát)
- Tab "Mẫu in" (`form.blade.php`, `id="tab-contract"`) hiện là **placeholder** ("triển khai Phase sau").
- Mẫu in HĐ: FirmContract `template_print_product`; WrServiceContract `template` (+ `template_id`). In bằng `fillReport(template, data)`.
- Editor các form HĐ: **CKEditor** (`asset('pages/ckeditor/ckeditor.js')`) + directive `ck-editor-print` trên `<textarea>`.
- Duyệt phiếu: `CustomerHandoverRequestController@approve` → `CustomerHandoverService::applyToContract($handover)` (đã áp `new_customer_data` lên HĐ chính + phụ lục) → set `status = DA_DUYET`.
- `applyToContract` phân biệt loại HĐ bằng `instanceof FirmContract` / `instanceof WrServiceContract`.

## Thiết kế chi tiết

### FE — Tab "Mẫu in" (`resources/views/sale/customer_handover_requests/form.blade.php`)
- Thay khối placeholder trong `#tab-contract` (nhánh `@if($contractable)`):
  - Giữ bảng info HĐ (số HĐ / loại / KH).
  - Thêm **CKEditor**: `<textarea ng-model="form.new_template_print" ck-editor-print rows="20"></textarea>`.
- `create.blade.php` / `edit.blade.php`: include `<script src="{{ asset('pages/ckeditor/ckeditor.js') }}"></script>` (nếu chưa có).
- Prefill (`formJs.blade.php` hoặc controller → view):
  - **Create**: `$scope.form.new_template_print = <mẫu in hiện tại của HĐ>` (truyền từ controller qua biến, vd `$currentTemplate`).
  - **Edit**: `= new_template_print` đã lưu; nếu rỗng → dùng mẫu in hiện tại của HĐ.
- Nếu không có HĐ (`$contractable` null): giữ cảnh báo "chọn HĐ trước".

### BE — Controller
- `create()` / `edit()`: tính `$currentTemplate` từ contractable
  (`FirmContract` → `template_print_product`; `WrServiceContract` → `template`) và truyền xuống view.
  Nên đặt helper trên service: `CustomerHandoverService::getContractTemplate($contractable): ?string`.
- `store()` / `update()`: lưu `new_template_print` từ request vào phiếu (giữ guard hiện có: chỉ sửa khi `DANG_TAO` & đúng người tạo).

### BE — Áp khi duyệt (`CustomerHandoverService::applyToContract`)
Sau khi `mapCustomerDataToContract($c, $data)` (HĐ chính), thêm:
```php
$tpl = $handover->new_template_print;
if ($tpl !== null && $tpl !== '') {
    if ($c instanceof FirmContract) {
        $c->template_print_product = $tpl;
    } elseif ($c instanceof WrServiceContract) {
        $c->template = $tpl;
    }
    $c->save();
}
```
- **Chỉ HĐ chính** (không lặp phụ lục cho mẫu in).

### Màn Show phiếu (`show.blade.php`)
- Tab "Mẫu in": hiển thị `new_template_print` read-only (preview HTML, vd `ng-bind-html` / `{!! !!}` đã sanitize hoặc iframe/preview như chỗ khác trong dự án).

## Quy tắc / Edge cases
- Chỉ sửa mẫu in khi phiếu **Đang tạo** (theo guard sẵn có của store/update).
- `new_template_print` rỗng → **không ghi đè** mẫu in HĐ khi duyệt (an toàn).
- Prefill = mẫu hiện tại → user không sửa thì duyệt ghi lại y nguyên (no-op vô hại).
- Loại HĐ khác Firm/Wr: bỏ qua (không có field mẫu in tương ứng).

## Không làm (ngoài phạm vi)
- Không auto tìm–thay KH cũ→mới trong mẫu in.
- Không sửa mẫu in của phụ lục.
- Không lưu bản mẫu in cũ để audit.

## File ảnh hưởng
- `database/migrations/xxxx_add_new_template_print_to_customer_handover_requests.php` (mới)
- `app/Model/Sale/CustomerHandoverRequest.php` (thêm `new_template_print` vào `$fillable`; LONGTEXT thường, KHÔNG cast)
- `app/Services/Sale/CustomerHandoverService.php` (getContractTemplate + applyToContract)
- `app/Http/Controllers/Sale/CustomerHandoverRequestController.php` (create/edit/store/update)
- `resources/views/sale/customer_handover_requests/form.blade.php` (tab)
- `resources/views/sale/customer_handover_requests/create.blade.php` + `edit.blade.php` (include ckeditor)
- `resources/views/sale/customer_handover_requests/formJs.blade.php` (prefill)
- `resources/views/sale/customer_handover_requests/show.blade.php` (preview)
