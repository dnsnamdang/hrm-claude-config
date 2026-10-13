# Task 7 — FormRequest (Store + Deny)

**Repo:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api` (nhánh gop_db, Laravel 8, PHP 7.4). KHÔNG commit/push, KHÔNG dispatch subagent, KHÔNG đọc vendor/, KHÔNG dùng mysql2/DB_CONNECTION_SECOND.

Task NHỎ, thuần transcription: tạo 2 FormRequest cho luồng "yêu cầu xuất bán hàng mượn". Code đầy đủ dưới đây, copy verbatim (đã port ERP validate rules controller:181-213). Entity `Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest` (Task 3) đã có constants CONTRACT_FIRM/CONTRACT_WR_SERVICE.

## File tạo
- `Modules/Finance/Http/Requests/BorrowSellRequest/StoreBorrowSellRequestRequest.php`
- `Modules/Finance/Http/Requests/BorrowSellRequest/DenyBorrowSellRequestRequest.php`

## RULING (đã chốt, đừng flag):
- `authorize(): bool { return true; }` là ĐÚNG ở đây — KHÔNG vi phạm "fail-closed" của CLAUDE.md. `authorize()` là cơ chế request-authorization của Laravel, KHÔNG phải cờ phân quyền dữ liệu. Gate quyền thực tế nằm ở `canX()` trong Controller (Task 8) — theo tiền lệ Product Import Request đã duyệt. Cờ fail-closed áp cho `can_view_*`/giá vốn/lương, không phải authorize().
- FE gửi `products`/`tabs`/`product_export_request_ids` có thể là JSON string (multipart) → `prepareForValidation()` decode. Giữ nguyên.

## StoreBorrowSellRequestRequest.php (copy verbatim)
```php
<?php
namespace Modules\Finance\Http\Requests\BorrowSellRequest;

use Illuminate\Foundation\Http\FormRequest;
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;

class StoreBorrowSellRequestRequest extends FormRequest
{
    public function authorize(): bool { return true; }

    protected function prepareForValidation(): void
    {
        foreach (['products', 'tabs', 'product_export_request_ids'] as $key) {
            $v = $this->input($key);
            if (is_string($v)) {
                $this->merge([$key => json_decode($v, true) ?: []]);
            }
        }
    }

    public function rules(): array
    {
        return [
            'type' => 'required|in:1,2',
            'products' => 'required|array|min:1',
            'products.*.details.*.qty' => 'required|numeric|min:0|max:999999',
            'note' => 'nullable|max:255',
            'contractable_id' => 'required',
            'contractable_type' => 'required|in:' . BorrowSellRequest::CONTRACT_FIRM . ',' . BorrowSellRequest::CONTRACT_WR_SERVICE,
            'product_export_request_ids' => 'required|array|min:1',
            'product_export_request_ids.*' => 'required|exists:product_export_requests,id',
            'tabs' => 'nullable|array|min:1',
            'tabs.*.firm_contract_tab_id' => 'required|exists:firm_contract_tabs,id',
            'tabs.*.products' => 'required|array|min:1',
            'tabs.*.products.*.details.*.qty' => 'required|numeric|min:0|max:999999',
        ];
    }

    public function messages(): array
    {
        return [
            'type.required' => 'Bắt buộc phải chọn',
            'product_export_request_ids.required' => 'Bắt buộc phải chọn',
            'contractable_id.required' => 'Bắt buộc phải chọn',
            'products.required' => 'Bắt buộc phải chọn',
            'products.*.details.*.qty.numeric' => 'Không hợp lệ',
            'products.*.details.*.qty.min' => 'Phải lớn hơn 0',
            'products.*.details.*.qty.max' => 'Không được vượt quá 6 chữ số',
            'products.*.details.*.qty.required' => 'Bắt buộc nhập',
            'note.max' => 'Không được vượt quá 255 ký tự',
        ];
    }
}
```

## DenyBorrowSellRequestRequest.php (copy verbatim)
```php
<?php
namespace Modules\Finance\Http\Requests\BorrowSellRequest;

use Illuminate\Foundation\Http\FormRequest;

class DenyBorrowSellRequestRequest extends FormRequest
{
    public function authorize(): bool { return true; }
    public function rules(): array { return ['comment' => 'required|max:255']; }
    public function messages(): array
    {
        return ['comment.required' => 'Bắt buộc phải nhập', 'comment.max' => 'Không được vượt quá 255 ký tự'];
    }
}
```

## Verify (chạy, DÁN output report)
- `php -l` cả 2 file.
- `composer dump-autoload -o` rồi tinker: `class_exists('\Modules\Finance\Http\Requests\BorrowSellRequest\StoreBorrowSellRequestRequest')` + Deny → cả 2 in `true`.

## Report
Ghi `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-7-report.md` (2 file, output php -l + class_exists). TRẢ VỀ ngắn: STATUS, 1 dòng verify.
