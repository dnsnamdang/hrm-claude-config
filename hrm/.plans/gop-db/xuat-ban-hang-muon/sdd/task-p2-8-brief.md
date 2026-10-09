# Task P2-8 Brief — StoreBorrowSellRequest FormRequest (validate payload lập phiếu xuất bán hàng mượn)

> **ĐỌC FILE NÀY TRƯỚC — requirements đầy đủ, dùng giá trị exact verbatim.**
> Feature `xuat-ban-hang-muon` Phase 2 (HRM, Laravel 8/PHP 7.4, nhánh `gop_db`). Giao tiếp tiếng Việt.
> Thư mục code: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api`

## Bối cảnh 1 dòng

FormRequest validate payload cho endpoint `POST /borrow-sells` (lập phiếu xuất bán thực tế). Payload này được `BorrowSellService::store()` (đã tồn tại, task T7) tiêu thụ. FormRequest phải validate ĐÚNG shape mà T7 đọc.

## File

- **Create:** `Modules/Finance/Http/Requests/BorrowSell/StoreBorrowSellRequest.php`
- **Create test:** `Modules/Finance/Tests/Unit/StoreBorrowSellRequestTest.php`

## Pattern để MIRROR (đọc trước khi viết)

`Modules/Finance/Http/Requests/BorrowSellRequest/StoreBorrowSellRequestRequest.php` (Phase 1) — copy cấu trúc class (namespace, extends FormRequest, authorize/rules/messages, cách viết messages tiếng Việt). **Lưu ý:** namespace file MỚI là `Modules\Finance\Http\Requests\BorrowSell` (thư mục `BorrowSell`, KHÁC thư mục Phase 1 `BorrowSellRequest`).

## Payload shape BẮT BUỘC (Ruling T8-payload — khớp T7 đang tiêu thụ)

T7 `store()` đọc payload theo shape sau (KHÔNG phải `borrow_sell_request_product_id` — plan cũ ghi sai, đã có ruling chốt trong ledger):

```json
{
  "borrow_sell_request_id": 123,
  "products": [
    {
      "objectable_id": 456,
      "objectable_type": "App\\Model\\Sale\\Firm\\Contract\\FirmContractTabProduct",
      "details": [
        { "product_export_request_detail_id": 789, "qty": 5 }
      ]
    }
  ]
}
```

## rules() BẮT BUỘC (exact)

```php
public function rules(): array
{
    return [
        'borrow_sell_request_id' => 'required|integer|exists:borrow_sell_requests,id',
        'products' => 'required|array|min:1',
        'products.*.objectable_id' => 'required|integer',
        'products.*.objectable_type' => 'required|string',
        'products.*.details' => 'required|array|min:1',
        'products.*.details.*.product_export_request_detail_id' => 'required|integer',
        'products.*.details.*.qty' => 'required|numeric|min:0',
    ];
}
```

## authorize()

```php
public function authorize(): bool
{
    return true; // quyền gate ở middleware checkPermission:Kế toán kho (route) + $parent->canApprove() trong service
}
```

## messages()

Tiếng Việt, tối thiểu các key sau (mirror phong cách Phase 1):
```php
public function messages(): array
{
    return [
        'borrow_sell_request_id.required' => 'Thiếu yêu cầu xuất bán hàng mượn.',
        'borrow_sell_request_id.exists' => 'Yêu cầu xuất bán hàng mượn không tồn tại.',
        'products.required' => 'Phải có ít nhất một sản phẩm để xuất bán.',
        'products.min' => 'Phải có ít nhất một sản phẩm để xuất bán.',
        'products.*.objectable_id.required' => 'Thiếu thông tin dòng hợp đồng của sản phẩm.',
        'products.*.objectable_type.required' => 'Thiếu loại dòng hợp đồng của sản phẩm.',
        'products.*.details.required' => 'Mỗi sản phẩm phải có ít nhất một dòng chi tiết xuất.',
        'products.*.details.*.product_export_request_detail_id.required' => 'Thiếu tham chiếu phiếu xuất kho của dòng chi tiết.',
        'products.*.details.*.qty.required' => 'Thiếu số lượng xuất bán.',
        'products.*.details.*.qty.numeric' => 'Số lượng xuất bán phải là số.',
    ];
}
```

## Ràng buộc
- Rethrow `ValidationException` (FormRequest chuẩn Laravel tự làm — KHÔNG override `failedValidation` để catch chung; giữ mặc định).
- KHÔNG dùng DB_CONNECTION_SECOND/mysql2. KHÔNG đọc vendor/. KHÔNG spawn subagent.

## Test — `Modules/Finance/Tests/Unit/StoreBorrowSellRequestTest.php`

Chạy: `cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api && php vendor/bin/phpunit --filter=StoreBorrowSellRequestTest Modules/Finance/Tests/Unit/StoreBorrowSellRequestTest.php` (KHÔNG `php artisan test`).

Dùng `Illuminate\Support\Facades\Validator` + `(new StoreBorrowSellRequest)->rules()`. KHÔNG cần DB (dùng rule không đụng `exists` hoặc bỏ rule exists khi test unit — nếu test đụng `exists:borrow_sell_requests` mà cần DB thì tách: test phần structure rules bằng cách bỏ borrow_sell_request_id hoặc dùng `use DatabaseTransactions` + seed 1 row). Đơn giản nhất: test các rule mảng (products/details/qty) — KHÔNG cần DB:

Tối thiểu 3 test:
1. **Thiếu `products`** → validator fails, có lỗi key `products`.
2. **Thiếu `products.0.details`** → fails.
3. **Payload đủ + hợp lệ** (bỏ qua `borrow_sell_request_id` exists bằng cách chỉ validate subset rules mảng, HOẶC seed 1 borrow_sell_requests row nếu dùng DatabaseTransactions) → passes.

Nếu muốn tránh DB hoàn toàn: trong test, lấy `$rules = (new StoreBorrowSellRequest)->rules();` rồi `unset($rules['borrow_sell_request_id']);` trước khi `Validator::make($data, $rules)` cho case "payload đủ hợp lệ" (case 3) — để không phụ thuộc bảng. Case 1/2 vẫn dùng full rules (chúng fail trước khi tới rule exists). Ghi rõ trong test comment lý do unset.

## Report contract
1. Test xanh → `git add Modules/Finance/Http/Requests/BorrowSell Modules/Finance/Tests/Unit/StoreBorrowSellRequestTest.php` + `git commit` message tiếng Việt.
2. Ghi report vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-8-report.md`.
3. Trả về ngắn: status, commit hash, 1 dòng test summary, concerns nếu có.
