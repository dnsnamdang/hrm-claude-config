# Config System Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the system config page from a single form into 7 independent tabs with per-tab save, change history tracking, and a new "hidden product types per ticket type" feature.

**Architecture:** Refactor the existing `edit.blade.php` into a Bootstrap 4 tabbed layout with 7 partial views. Add `updateTab($tab)` and `histories($tab)` methods to `ConfigsController`. Create two new DB tables (`config_hidden_product_types`, `config_histories`) and corresponding Eloquent models. Remove unused fields from UI only (keep DB columns).

**Tech Stack:** PHP 7.4, Laravel 8, AngularJS 1.3.9, jQuery, Bootstrap 4, Select2, Yajra DataTables

---

## File Structure

### New files
| File | Responsibility |
|---|---|
| `database/migrations/2026_06_03_000001_create_config_hidden_product_types_table.php` | Migration for hidden product type mapping |
| `database/migrations/2026_06_03_000002_create_config_histories_table.php` | Migration for config change history |
| `app/Model/Common/ConfigHiddenProductType.php` | Eloquent model for hidden product types |
| `app/Model/Common/ConfigHistory.php` | Eloquent model for config history |
| `resources/views/common/configs/tabs/general.blade.php` | Tab 1: Logo, Title, Description |
| `resources/views/common/configs/tabs/category.blade.php` | Tab 2: Product natures + hidden product types table |
| `resources/views/common/configs/tabs/business.blade.php` | Tab 3: 13 business fields |
| `resources/views/common/configs/tabs/warehouse.blade.php` | Tab 4: Transport tax |
| `resources/views/common/configs/tabs/xnk.blade.php` | Tab 5: Environment tax |
| `resources/views/common/configs/tabs/accounting.blade.php` | Tab 6: E-commerce coefficient + debt date |
| `resources/views/common/configs/tabs/cskh.blade.php` | Tab 7: Serial product types + piece-rate table |
| `resources/views/common/configs/partials/tab_buttons.blade.php` | Shared Save + History + Cancel buttons |
| `resources/views/common/configs/partials/history_modal.blade.php` | Shared history modal |

### Modified files
| File | Changes |
|---|---|
| `app/Model/Common/Config.php` | Add `hiddenProductTypes()` and `histories()` relations |
| `app/Http/Controllers/Common/ConfigsController.php` | Add constants, refactor `edit()`, add `updateTab()` and `histories()` methods |
| `resources/views/common/configs/edit.blade.php` | Complete rewrite: Bootstrap tabs layout + new Angular controller |
| `routes/web.php:5558-5561` | Add 2 new routes in configs group |

---

### Task 1: Create database migrations

**Files:**
- Create: `database/migrations/2026_06_03_000001_create_config_hidden_product_types_table.php`
- Create: `database/migrations/2026_06_03_000002_create_config_histories_table.php`

- [ ] **Step 1: Create config_hidden_product_types migration**

Create file `TanPhatDev/database/migrations/2026_06_03_000001_create_config_hidden_product_types_table.php`:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateConfigHiddenProductTypesTable extends Migration
{
    public function up()
    {
        Schema::create('config_hidden_product_types', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('config_id');
            $table->text('product_types');
            $table->text('ticket_types');
            $table->timestamps();

            $table->foreign('config_id')->references('id')->on('configs')->onDelete('cascade');
        });
    }

    public function down()
    {
        Schema::dropIfExists('config_hidden_product_types');
    }
}
```

- [ ] **Step 2: Create config_histories migration**

Create file `TanPhatDev/database/migrations/2026_06_03_000002_create_config_histories_table.php`:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateConfigHistoriesTable extends Migration
{
    public function up()
    {
        Schema::create('config_histories', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('config_id');
            $table->string('tab', 50);
            $table->string('field_name', 255);
            $table->text('old_value')->nullable();
            $table->text('new_value')->nullable();
            $table->unsignedBigInteger('updated_by');
            $table->timestamps();

            $table->foreign('config_id')->references('id')->on('configs')->onDelete('cascade');
            $table->foreign('updated_by')->references('id')->on('users')->onDelete('cascade');
            $table->index('tab');
        });
    }

    public function down()
    {
        Schema::dropIfExists('config_histories');
    }
}
```

- [ ] **Step 3: Run migrations**

Run: `cd TanPhatDev && php artisan migrate`

Expected: Both tables created successfully.

- [ ] **Step 4: Commit**

```bash
git add database/migrations/2026_06_03_000001_create_config_hidden_product_types_table.php database/migrations/2026_06_03_000002_create_config_histories_table.php
git commit -m "feat: add migrations for config_hidden_product_types and config_histories tables"
```

---

### Task 2: Create new Eloquent models

**Files:**
- Create: `app/Model/Common/ConfigHiddenProductType.php`
- Create: `app/Model/Common/ConfigHistory.php`
- Modify: `app/Model/Common/Config.php`

- [ ] **Step 1: Create ConfigHiddenProductType model**

Create file `TanPhatDev/app/Model/Common/ConfigHiddenProductType.php`:

```php
<?php

namespace App\Model\Common;

use Illuminate\Database\Eloquent\Model;

class ConfigHiddenProductType extends Model
{
    protected $table = 'config_hidden_product_types';

    protected $fillable = ['config_id', 'product_types', 'ticket_types'];

    protected $casts = [
        'product_types' => 'array',
        'ticket_types' => 'array',
    ];

    public function config()
    {
        return $this->belongsTo(Config::class);
    }
}
```

- [ ] **Step 2: Create ConfigHistory model**

Create file `TanPhatDev/app/Model/Common/ConfigHistory.php`:

```php
<?php

namespace App\Model\Common;

use App\User;
use Illuminate\Database\Eloquent\Model;

class ConfigHistory extends Model
{
    protected $table = 'config_histories';

    protected $fillable = ['config_id', 'tab', 'field_name', 'old_value', 'new_value', 'updated_by'];

    public function updater()
    {
        return $this->belongsTo(User::class, 'updated_by');
    }

    public function config()
    {
        return $this->belongsTo(Config::class);
    }
}
```

- [ ] **Step 3: Add relations to Config model**

Modify `TanPhatDev/app/Model/Common/Config.php`. Add these two methods after the existing `contractRows()` method:

```php
public function hiddenProductTypes()
{
    return $this->hasMany(ConfigHiddenProductType::class);
}

public function histories()
{
    return $this->hasMany(ConfigHistory::class);
}
```

The full file should now be:

```php
<?php

namespace App\Model\Common;

use App\Models\ContractRow;
use Illuminate\Database\Eloquent\Model;

class Config extends Model
{
    public static function getConfig($column = null)
    {
        if ($column) {
            return self::query()->value($column);
        }

        return self::first();
    }

    public function contractRows()
    {
        return $this->hasMany(ContractRow::class);
    }

    public function hiddenProductTypes()
    {
        return $this->hasMany(ConfigHiddenProductType::class);
    }

    public function histories()
    {
        return $this->hasMany(ConfigHistory::class);
    }
}
```

- [ ] **Step 4: Commit**

```bash
git add app/Model/Common/ConfigHiddenProductType.php app/Model/Common/ConfigHistory.php app/Model/Common/Config.php
git commit -m "feat: add ConfigHiddenProductType, ConfigHistory models and Config relations"
```

---

### Task 3: Add routes and controller constants + updateTab method

**Files:**
- Modify: `routes/web.php:5558-5561`
- Modify: `app/Http/Controllers/Common/ConfigsController.php`

- [ ] **Step 1: Add new routes**

In `TanPhatDev/routes/web.php`, find lines 5558-5561 (the configs route group) and add 2 new routes. The group should become:

```php
Route::group(['prefix' => 'configs', 'middleware' => 'checkPermission:Cấu hình hệ thống'], function () {
    Route::get('/edit', 'Common\ConfigsController@edit')->name('configs.edit');
    Route::post('/', 'Common\ConfigsController@update')->name('configs.update');
    Route::post('/update/{tab}', 'Common\ConfigsController@updateTab')->name('configs.updateTab');
    Route::get('/histories/{tab}', 'Common\ConfigsController@histories')->name('configs.histories');
});
```

- [ ] **Step 2: Add use statements and constants to ConfigsController**

Add at top of `TanPhatDev/app/Http/Controllers/Common/ConfigsController.php`, after the existing use statements:

```php
use App\Model\Common\ConfigHiddenProductType;
use App\Model\Common\ConfigHistory;
use App\Model\Product\Category;
use App\Model\Sale\CustomerGroup;
use App\Model\Common\Department;
use App\Model\Product\Group;
use App\Http\Traits\ResponseTrait;
```

Add the `use ResponseTrait;` line and constants inside the class, before the `edit()` method:

```php
class ConfigsController extends Controller
{
    use ResponseTrait;

    const VALID_TABS = ['general', 'category', 'business', 'warehouse', 'xnk', 'accounting', 'cskh'];

    const TAB_FIELDS = [
        'general'    => ['logo', 'title', 'description'],
        'category'   => ['product_types'],
        'business'   => [
            'max_borrow_date', 'max_prepick_date', 'consignment_holding_time',
            'max_prepick_date_project_contract', 'warning_day',
            'customer_is_following', 'customer_taken_care',
            'quotation_valid_days', 'project_quotation_valid_days',
            'customer_register_expiry', 'customer_groups', 'department_groups',
            'is_equipment', 'is_repair', 'is_project', 'is_principle', 'is_dental_principle',
        ],
        'warehouse'  => ['vat_delivery_trip_percent'],
        'xnk'       => ['environment_tax'],
        'accounting' => ['coefficient_ecommerce_price', 'debt_calculation_date'],
        'cskh'      => ['serial_product_types'],
    ];

    const TICKET_TYPES = [
        'yeu_cau_hoi_gia'        => 'Phiếu Yêu cầu hỏi giá',
        'yeu_cau_dat_hang_ngoai' => 'Phiếu Yêu cầu đặt hàng mua ngoài',
        'yeu_cau_dat_hang'       => 'Phiếu Yêu cầu đặt hàng',
        'bao_gia_vt_hh_tb'      => 'Báo giá vật tư- hàng hóa - thiết bị',
        'bao_gia_dv_sc_bd_bt'   => 'Báo giá dịch vụ sửa chữa - bảo dưỡng - bảo trì',
        'bao_gia_hd_nguyen_tac' => 'Báo giá hợp đồng nguyên tắc',
        'bao_gia_du_an'         => 'Báo giá dự án',
        'yeu_cau_sc_bd'         => 'Phiếu yêu cầu sửa chữa - bảo dưỡng',
    ];

    const FIELD_LABELS = [
        'logo' => 'Logo',
        'title' => 'Tiêu đề',
        'description' => 'Mô tả',
        'product_types' => 'Tính chất hàng hóa',
        'max_borrow_date' => 'Số ngày mượn tối đa',
        'max_prepick_date' => 'Số ngày giữ tối đa',
        'consignment_holding_time' => 'Số ngày giữ tối đa của hàng gửi',
        'max_prepick_date_project_contract' => 'Số ngày giữ tối đa - HĐDA',
        'warning_day' => 'Số ngày cảnh báo (mượn/giữ hàng)',
        'customer_is_following' => 'Khách hàng đang theo dõi',
        'customer_taken_care' => 'Khách hàng được chăm sóc',
        'quotation_valid_days' => 'Số ngày hiệu lực báo giá',
        'project_quotation_valid_days' => 'Số ngày hiệu lực báo giá dự án',
        'customer_register_expiry' => 'Thời gian đăng ký khách hàng',
        'customer_groups' => 'Nhóm khách hàng không ràng buộc HĐ thị trường',
        'department_groups' => 'Phòng ban không ràng buộc thị trường',
        'is_equipment' => 'Ràng buộc HĐ bán hàng',
        'is_repair' => 'Ràng buộc HĐ dịch vụ',
        'is_project' => 'Ràng buộc HĐ dự án',
        'is_principle' => 'Ràng buộc HĐ nguyên tắc',
        'is_dental_principle' => 'Ràng buộc HĐ nguyên tắc nha khoa',
        'vat_delivery_trip_percent' => 'Thuế vận tải',
        'environment_tax' => 'Hệ số thuế bảo vệ môi trường',
        'coefficient_ecommerce_price' => 'Hệ số giá thương mại điện tử',
        'debt_calculation_date' => 'Ngày khai báo công nợ đầu kỳ',
        'serial_product_types' => 'Hàng không bắt buộc Serial',
    ];
```

- [ ] **Step 3: Add validation rules per tab**

Add this private method to the controller, after the constants:

```php
private function getValidationRules(string $tab)
{
    $rules = [];
    $messages = [];

    switch ($tab) {
        case 'general':
            $rules = [
                'logo' => 'required',
                'title' => 'required|max:255',
                'description' => 'required',
            ];
            $messages = [
                'logo.required' => 'Bắt buộc chọn',
                'title.required' => 'Bắt buộc nhập',
                'title.max' => 'Nhập tối đa 255 ký tự',
                'description.required' => 'Bắt buộc nhập',
            ];
            break;

        case 'category':
            $rules = [
                'product_types' => 'required|array|min:1',
                'hidden_product_types' => 'nullable|array',
                'hidden_product_types.*.product_types' => 'required|array|min:1',
                'hidden_product_types.*.ticket_types' => 'required|array|min:1',
            ];
            $messages = [
                'product_types.required' => 'Bắt buộc phải chọn',
                'product_types.min' => 'Bắt buộc phải chọn',
                'hidden_product_types.*.product_types.required' => 'Bắt buộc chọn loại hàng hóa',
                'hidden_product_types.*.product_types.min' => 'Bắt buộc chọn loại hàng hóa',
                'hidden_product_types.*.ticket_types.required' => 'Bắt buộc chọn loại phiếu',
                'hidden_product_types.*.ticket_types.min' => 'Bắt buộc chọn loại phiếu',
            ];
            break;

        case 'business':
            $rules = [
                'max_borrow_date' => 'required|numeric|min:1|max:999',
                'max_prepick_date' => 'required|numeric|min:1|max:999',
                'consignment_holding_time' => 'required|integer|min:1|max:999',
                'max_prepick_date_project_contract' => 'required|numeric|min:1|max:999',
                'warning_day' => 'required|numeric|min:0|max:100',
                'customer_is_following' => 'required|numeric|min:0|max:100',
                'customer_taken_care' => 'required|numeric|min:0|max:100',
                'quotation_valid_days' => 'required|numeric|min:1|max:999999',
                'project_quotation_valid_days' => 'required|numeric|min:1|max:999999',
                'customer_register_expiry' => 'required|numeric|min:1',
                'customer_groups' => 'nullable|array',
                'department_groups' => 'nullable|array',
            ];
            $messages = [
                'max_borrow_date.required' => 'Bắt buộc nhập',
                'max_borrow_date.numeric' => 'Không hợp lệ',
                'max_borrow_date.min' => 'Bắt buộc nhập',
                'max_prepick_date.required' => 'Bắt buộc nhập',
                'max_prepick_date.numeric' => 'Không hợp lệ',
                'max_prepick_date.min' => 'Bắt buộc nhập',
                'consignment_holding_time.required' => 'Bắt buộc nhập',
                'consignment_holding_time.integer' => 'Không hợp lệ',
                'max_prepick_date_project_contract.required' => 'Bắt buộc nhập',
                'max_prepick_date_project_contract.numeric' => 'Không hợp lệ',
                'max_prepick_date_project_contract.min' => 'Bắt buộc nhập',
                'warning_day.required' => 'Bắt buộc nhập',
                'warning_day.numeric' => 'Không hợp lệ',
                'customer_is_following.required' => 'Bắt buộc nhập',
                'customer_taken_care.required' => 'Bắt buộc nhập',
                'quotation_valid_days.required' => 'Bắt buộc nhập',
                'project_quotation_valid_days.required' => 'Bắt buộc nhập',
                'customer_register_expiry.required' => 'Bắt buộc nhập',
                'customer_register_expiry.numeric' => 'Không hợp lệ',
                'customer_register_expiry.min' => 'Không hợp lệ',
            ];
            break;

        case 'warehouse':
            $rules = [
                'vat_delivery_trip_percent' => 'required|numeric|min:0|max:100',
            ];
            $messages = [
                'vat_delivery_trip_percent.required' => 'Bắt buộc nhập',
                'vat_delivery_trip_percent.numeric' => 'Không hợp lệ',
            ];
            break;

        case 'xnk':
            $rules = [
                'environment_tax' => 'required|numeric|min:0|max:999999999',
            ];
            $messages = [
                'environment_tax.required' => 'Bắt buộc nhập',
                'environment_tax.numeric' => 'Không hợp lệ',
            ];
            break;

        case 'accounting':
            $rules = [
                'coefficient_ecommerce_price' => 'required|numeric',
                'debt_calculation_date' => 'required|date',
            ];
            $messages = [
                'coefficient_ecommerce_price.required' => 'Bắt buộc nhập',
                'coefficient_ecommerce_price.numeric' => 'Không hợp lệ',
                'debt_calculation_date.required' => 'Bắt buộc nhập',
                'debt_calculation_date.date' => 'Không hợp lệ',
            ];
            break;

        case 'cskh':
            $rules = [
                'serial_product_types' => 'nullable|array',
                'contract_rows' => [
                    'nullable',
                    'array',
                    function ($attribute, $value, $fail) {
                        if (empty($value)) return;
                        $hasAnyProductGroup = false;
                        $hasAnyProductNature = false;
                        foreach ($value as $row) {
                            $hasProductGroup = !empty(array_filter($row['product_group'] ?? [null], function($v) { return $v !== null; }));
                            $hasProductNature = !empty(array_filter($row['product_nature'] ?? [null], function($v) { return $v !== null; }));
                            if ($hasProductGroup) $hasAnyProductGroup = true;
                            if ($hasProductNature) $hasAnyProductNature = true;
                        }
                        if ($hasAnyProductGroup && $hasAnyProductNature) {
                            $fail("Không được sử dụng cả Nhóm hàng hóa và Tính chất hàng hóa trong các dòng khác nhau");
                        }
                    }
                ],
                'contract_rows.*.quantity' => 'required|integer|min:1',
            ];
            $messages = [
                'contract_rows.*.quantity.required' => 'Bắt buộc nhập',
                'contract_rows.*.quantity.integer' => 'Không hợp lệ',
                'contract_rows.*.quantity.min' => 'Phải lớn hơn 0',
            ];
            break;
    }

    return [$rules, $messages];
}
```

- [ ] **Step 4: Add updateTab method**

Add this method to the controller:

```php
public function updateTab(Request $request, string $tab)
{
    if (!in_array($tab, self::VALID_TABS)) {
        return $this->responseErrors('Tab không hợp lệ');
    }

    list($rules, $messages) = $this->getValidationRules($tab);
    $validate = Validator::make($request->all(), $rules, $messages);

    if ($validate->fails()) {
        $json = new stdClass();
        $json->success = false;
        $json->errors = $validate->errors();
        $json->message = "Sửa cấu hình thất bại!";
        return Response::json($json);
    }

    $config = Config::getConfig();
    $fields = self::TAB_FIELDS[$tab] ?? [];

    // Track changes for history
    foreach ($fields as $field) {
        $oldValue = $config->{$field};
        $newValue = $request->{$field};

        // Normalize comma-separated fields
        if (in_array($field, ['product_types', 'customer_groups', 'department_groups', 'serial_product_types'])) {
            $newValue = is_array($newValue) ? join(',', $newValue) : $newValue;
        }

        // Normalize boolean fields
        if (in_array($field, ['is_equipment', 'is_repair', 'is_project', 'is_principle', 'is_dental_principle'])) {
            $oldValue = $oldValue ? '1' : '0';
            $newValue = $newValue ? '1' : '0';
        }

        if ((string)$oldValue !== (string)$newValue) {
            ConfigHistory::create([
                'config_id' => $config->id,
                'tab' => $tab,
                'field_name' => self::FIELD_LABELS[$field] ?? $field,
                'old_value' => (string)$oldValue,
                'new_value' => (string)$newValue,
                'updated_by' => auth()->user()->id,
            ]);
        }
    }

    // Save config fields for this tab
    foreach ($fields as $field) {
        if (in_array($field, ['product_types', 'customer_groups', 'department_groups', 'serial_product_types'])) {
            $config->{$field} = $request->{$field} ? join(',', $request->{$field}) : null;
        } elseif (in_array($field, ['is_equipment', 'is_repair', 'is_project', 'is_principle', 'is_dental_principle'])) {
            $config->{$field} = $request->{$field} ? 1 : 0;
        } else {
            $config->{$field} = $request->{$field};
        }
    }
    $config->save();

    // Tab category: handle hidden product types
    if ($tab === 'category') {
        $oldHidden = $config->hiddenProductTypes()->get()->toArray();
        ConfigHiddenProductType::where('config_id', $config->id)->delete();
        if ($request->hidden_product_types) {
            foreach ($request->hidden_product_types as $row) {
                ConfigHiddenProductType::create([
                    'config_id' => $config->id,
                    'product_types' => json_encode($row['product_types'] ?? []),
                    'ticket_types' => json_encode($row['ticket_types'] ?? []),
                ]);
            }
        }
        $newHidden = $config->hiddenProductTypes()->get()->toArray();
        if (json_encode($oldHidden) !== json_encode($newHidden)) {
            ConfigHistory::create([
                'config_id' => $config->id,
                'tab' => $tab,
                'field_name' => 'Loại hàng hóa không hiển thị trên các phiếu',
                'old_value' => json_encode($oldHidden),
                'new_value' => json_encode($newHidden),
                'updated_by' => auth()->user()->id,
            ]);
        }
    }

    // Tab cskh: handle contract rows
    if ($tab === 'cskh') {
        $oldRows = $config->contractRows()->get()->toArray();
        ContractRow::where('config_id', $config->id)->delete();
        if ($request->contract_rows) {
            foreach ($request->contract_rows as $row) {
                ContractRow::create([
                    'config_id' => $config->id,
                    'product_groups' => json_encode($row['product_group'] ?? []),
                    'product_natures' => json_encode($row['product_nature'] ?? []),
                    'quantity' => $row['quantity'],
                ]);
            }
        }
        $newRows = $config->contractRows()->get()->toArray();
        if (json_encode($oldRows) !== json_encode($newRows)) {
            ConfigHistory::create([
                'config_id' => $config->id,
                'tab' => $tab,
                'field_name' => 'Bảng tính công khoán',
                'old_value' => json_encode($oldRows),
                'new_value' => json_encode($newRows),
                'updated_by' => auth()->user()->id,
            ]);
        }
    }

    $json = new stdClass();
    $json->success = true;
    $json->message = "Sửa cấu hình thành công!";
    return Response::json($json);
}
```

- [ ] **Step 5: Add histories method**

Add this method to the controller:

```php
public function histories(string $tab)
{
    if (!in_array($tab, self::VALID_TABS)) {
        return $this->responseErrors('Tab không hợp lệ');
    }

    $config = Config::getConfig();
    $histories = ConfigHistory::where('config_id', $config->id)
        ->where('tab', $tab)
        ->with('updater.info')
        ->orderBy('created_at', 'desc')
        ->get()
        ->map(function ($h) {
            $updaterName = '';
            if ($h->updater && $h->updater->info) {
                $updaterName = $h->updater->info->code . '_' . $h->updater->fullname;
            }
            return [
                'updater' => $updaterName,
                'field_name' => $h->field_name,
                'old_value' => $h->old_value,
                'new_value' => $h->new_value,
                'created_at' => $h->created_at->format('d/m/Y H:i'),
            ];
        });

    return $this->responseSuccess($histories->toArray());
}
```

- [ ] **Step 6: Refactor edit method**

Replace the existing `edit()` method with:

```php
public function edit()
{
    $config = Config::getConfig();

    $config->contract_rows = $config->contractRows()->get()->map(function ($row) {
        return [
            'product_group' => json_decode($row->product_groups),
            'product_nature' => json_decode($row->product_natures),
            'quantity' => $row->quantity,
        ];
    });

    $hiddenProductTypes = $config->hiddenProductTypes()->get()->map(function ($row) {
        return [
            'product_types' => $row->product_types,
            'ticket_types' => $row->ticket_types,
        ];
    });

    $ticketTypes = self::TICKET_TYPES;
    $productCategories = Category::where('status', 1)->get(['id', 'name']);
    $customerGroups = CustomerGroup::getForSelect();
    $departmentGroups = Department::getForSelect();
    $groups = Group::getForSelect();

    return view('common.configs.edit', compact([
        'config',
        'hiddenProductTypes',
        'ticketTypes',
        'productCategories',
        'customerGroups',
        'departmentGroups',
        'groups',
    ]));
}
```

- [ ] **Step 7: Commit**

```bash
git add routes/web.php app/Http/Controllers/Common/ConfigsController.php
git commit -m "feat: add updateTab, histories methods and per-tab validation to ConfigsController"
```

---

### Task 4: Create shared partials (tab buttons + history modal)

**Files:**
- Create: `resources/views/common/configs/partials/tab_buttons.blade.php`
- Create: `resources/views/common/configs/partials/history_modal.blade.php`

- [ ] **Step 1: Create tab_buttons partial**

Create directories and file `TanPhatDev/resources/views/common/configs/partials/tab_buttons.blade.php`:

```bash
mkdir -p TanPhatDev/resources/views/common/configs/partials
mkdir -p TanPhatDev/resources/views/common/configs/tabs
```

```php
<div class="text-right mt-3">
    <button type="button" class="btn btn-success btn-cons" ng-click="submitTab('{{ $tab }}')" ng-disabled="loading.{{ $tab }}">
        <i ng-if="!loading.{{ $tab }}" class="fa fa-save"></i>
        <i ng-if="loading.{{ $tab }}" class="fa fa-spin fa-spinner"></i>
        Lưu
    </button>
    <button type="button" class="btn btn-info btn-cons" ng-click="showHistory('{{ $tab }}')">
        <i class="fa fa-history"></i> Lịch sử chỉnh sửa
    </button>
    <a href="/" class="btn btn-danger btn-cons">
        <i class="fa fa-remove"></i> Hủy
    </a>
</div>
```

- [ ] **Step 2: Create history_modal partial**

Create file `TanPhatDev/resources/views/common/configs/partials/history_modal.blade.php`:

```php
<div class="modal fade" id="historyModal" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Lịch sử chỉnh sửa</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <div ng-if="historyLoading" class="text-center p-3">
                    <i class="fa fa-spin fa-spinner"></i> Đang tải...
                </div>
                <div ng-if="!historyLoading && histories.length === 0" class="text-center p-3 text-muted">
                    Chưa có lịch sử chỉnh sửa
                </div>
                <table class="table table-bordered table-hover" ng-if="!historyLoading && histories.length > 0">
                    <thead>
                        <tr>
                            <th>Người cập nhật</th>
                            <th>Tên trường sửa</th>
                            <th>Nội dung cũ</th>
                            <th>Nội dung mới</th>
                            <th>Ngày cập nhật</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr ng-repeat="h in histories track by $index">
                            <td><% h.updater %></td>
                            <td><% h.field_name %></td>
                            <td><% h.old_value %></td>
                            <td><% h.new_value %></td>
                            <td><% h.created_at %></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Đóng</button>
            </div>
        </div>
    </div>
</div>
```

- [ ] **Step 3: Commit**

```bash
git add resources/views/common/configs/partials/
git commit -m "feat: add shared tab_buttons and history_modal partials"
```

---

### Task 5: Create tab partial views (Tab 1-4)

**Files:**
- Create: `resources/views/common/configs/tabs/general.blade.php`
- Create: `resources/views/common/configs/tabs/category.blade.php`
- Create: `resources/views/common/configs/tabs/business.blade.php`
- Create: `resources/views/common/configs/tabs/warehouse.blade.php`

- [ ] **Step 1: Create Tab 1 — general.blade.php**

Create file `TanPhatDev/resources/views/common/configs/tabs/general.blade.php`:

```php
<div class="card-body">
    <div class="form-group row">
        <label class="col-md-3 col-form-label text-md-right">Logo <span class="text-danger">(*)</span></label>
        <div class="col-md-9">
            <label for="upload-logo" title="Click để chọn ảnh" class="employee-image profile-avatar cursor-pointer">
                <img ng-src="<% config.logo %>" class="w-100">
            </label>
            <input class="form-control d-none" type="file" id="upload-logo" accept="image/*">
            <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.logo">
                <strong><% errors.logo[0] %></strong>
            </span>
        </div>
    </div>

    <div class="form-group row">
        <label class="col-md-3 col-form-label text-md-right">Tiêu đề <span class="text-danger">(*)</span></label>
        <div class="col-md-9">
            <input type="text" class="form-control"
                ng-class="{'is-invalid': errors && errors.title}" ng-model="config.title">
            <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.title">
                <strong><% errors.title[0] %></strong>
            </span>
        </div>
    </div>

    <div class="form-group row">
        <label class="col-md-3 col-form-label text-md-right">Mô tả <span class="text-danger">(*)</span></label>
        <div class="col-md-9">
            <textarea rows="3" class="form-control"
                ng-class="{'is-invalid': errors && errors.description}" ng-model="config.description"></textarea>
            <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.description">
                <strong><% errors.description[0] %></strong>
            </span>
        </div>
    </div>

    @include('common.configs.partials.tab_buttons', ['tab' => 'general'])
</div>
```

- [ ] **Step 2: Create Tab 2 — category.blade.php**

Create file `TanPhatDev/resources/views/common/configs/tabs/category.blade.php`:

```php
<div class="card-body">
    <h5>1. Tính chất hàng hóa <span class="text-danger">(*)</span></h5>
    <div class="form-group row">
        <div class="col-md-6">
            <select class="select2 form-control" name="product_types[]"
                ng-class="{'is-invalid': errors && errors.product_types}"
                ng-model="config.product_types" multiple>
                <option ng-repeat="type in product_types" ng-value="type.value"
                    ng-selected="config.config_product_types.includes(type.value)"><% type.name %></option>
            </select>
            <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.product_types">
                <strong><% errors.product_types[0] %></strong>
            </span>
        </div>
    </div>

    <hr>

    <h5>2. Loại hàng hóa không hiển thị trên các phiếu</h5>
    <div style="max-height: 500px; overflow-y: auto; width: 100%; overflow-x: auto;">
        <table class="table table-bordered table-hover" style="min-width: 600px;">
            <thead>
                <tr>
                    <th style="width: 40%">Loại hàng hóa <span class="text-danger">(*)</span></th>
                    <th style="width: 50%">Loại phiếu <span class="text-danger">(*)</span></th>
                    <th style="width: 10%; min-width: 60px">
                        <a class="btn btn-link text-success p-0" href="javascript:void(0)" ng-click="addHiddenRow()">
                            <i class="fa fa-plus"></i>
                        </a>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr ng-repeat="row in hiddenProductTypes track by $index">
                    <td>
                        <select class="select2 form-control hidden-product-type-select"
                            ng-model="row.product_types" multiple
                            ng-class="{'is-invalid': errors && errors['hidden_product_types.' + $index + '.product_types']}">
                            <option ng-repeat="cat in productCategories" ng-value="cat.id"
                                ng-selected="arrayInclude(row.product_types, cat.id)"><% cat.name %></option>
                        </select>
                        <span class="invalid-feedback d-block" role="alert"
                            ng-if="errors && errors['hidden_product_types.' + $index + '.product_types']">
                            <strong><% errors['hidden_product_types.' + $index + '.product_types'][0] %></strong>
                        </span>
                    </td>
                    <td>
                        <select class="select2 form-control hidden-ticket-type-select"
                            ng-model="row.ticket_types" multiple
                            ng-class="{'is-invalid': errors && errors['hidden_product_types.' + $index + '.ticket_types']}">
                            <option ng-repeat="(key, label) in ticketTypes" ng-value="key"
                                ng-selected="arrayInclude(row.ticket_types, key)"><% label %></option>
                        </select>
                        <span class="invalid-feedback d-block" role="alert"
                            ng-if="errors && errors['hidden_product_types.' + $index + '.ticket_types']">
                            <strong><% errors['hidden_product_types.' + $index + '.ticket_types'][0] %></strong>
                        </span>
                    </td>
                    <td class="text-center">
                        <button class="btn btn-link text-danger p-0" type="button" ng-click="removeHiddenRow($index)">
                            <i class="fa fa-minus"></i>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    @include('common.configs.partials.tab_buttons', ['tab' => 'category'])
</div>
```

- [ ] **Step 3: Create Tab 3 — business.blade.php**

Create file `TanPhatDev/resources/views/common/configs/tabs/business.blade.php`:

```php
<div class="card-body">
    <div class="row">
        <div class="col-md-6">
            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Số ngày mượn tối đa <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="number" class="form-control text-right" step="1"
                        ng-class="{'is-invalid': errors && errors.max_borrow_date}" ng-model="config.max_borrow_date">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.max_borrow_date">
                        <strong><% errors.max_borrow_date[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Số ngày giữ tối đa <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="number" class="form-control text-right" step="1"
                        ng-class="{'is-invalid': errors && errors.max_prepick_date}" ng-model="config.max_prepick_date">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.max_prepick_date">
                        <strong><% errors.max_prepick_date[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Số ngày giữ tối đa của hàng gửi <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="number" class="form-control text-right" min="1" step="1"
                        ng-class="{'is-invalid': errors && errors.consignment_holding_time}" ng-model="config.consignment_holding_time">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.consignment_holding_time">
                        <strong><% errors.consignment_holding_time[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Số ngày giữ tối đa - HĐDA <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="number" class="form-control text-right" step="1"
                        ng-class="{'is-invalid': errors && errors.max_prepick_date_project_contract}" ng-model="config.max_prepick_date_project_contract">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.max_prepick_date_project_contract">
                        <strong><% errors.max_prepick_date_project_contract[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Số ngày cảnh báo (mượn/giữ hàng) <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="number" class="form-control text-right" step="1"
                        ng-class="{'is-invalid': errors && errors.warning_day}" ng-model="config.warning_day">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.warning_day">
                        <strong><% errors.warning_day[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Khách hàng đang theo dõi <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="text" class="form-control text-right" step="1" placeholder="Nhập số tháng"
                        ng-class="{'is-invalid': errors && errors.customer_is_following}" ng-model="config.customer_is_following">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.customer_is_following">
                        <strong><% errors.customer_is_following[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Khách hàng được chăm sóc <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="text" class="form-control text-right" step="1" placeholder="Nhập số tháng"
                        ng-class="{'is-invalid': errors && errors.customer_taken_care}" ng-model="config.customer_taken_care">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.customer_taken_care">
                        <strong><% errors.customer_taken_care[0] %></strong>
                    </span>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Số ngày hiệu lực báo giá <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="number" class="form-control text-right" step="1"
                        ng-class="{'is-invalid': errors && errors.quotation_valid_days}" ng-model="config.quotation_valid_days">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.quotation_valid_days">
                        <strong><% errors.quotation_valid_days[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Số ngày hiệu lực báo giá dự án <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="number" class="form-control text-right" step="1"
                        ng-class="{'is-invalid': errors && errors.project_quotation_valid_days}" ng-model="config.project_quotation_valid_days">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.project_quotation_valid_days">
                        <strong><% errors.project_quotation_valid_days[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Thời gian đăng ký khách hàng <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="number" class="form-control" min="0" step="1"
                        ng-class="{'is-invalid': errors && errors.customer_register_expiry}" ng-model="config.customer_register_expiry">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.customer_register_expiry">
                        <strong><% errors.customer_register_expiry[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <div class="col-md-12">
                    <label class="col-form-label text-md-right">Nhóm khách hàng không ràng buộc HĐ thị trường</label>
                    <div class="input-group mb-0">
                        <select class="select2 form-control" name="customer_groups[]"
                            ng-model="config.customer_groups" multiple>
                            <option ng-repeat="c in customer_groups" ng-value="c.id"
                                ng-selected="arrayInclude(config.config_customer_groups, c.id)"><% c.name %></option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="form-group row">
                <div class="col-md-12">
                    <label class="col-form-label text-md-right">Phòng ban không ràng buộc thị trường</label>
                    <div class="input-group mb-0">
                        <select class="select2 form-control" name="department_groups[]"
                            ng-model="config.department_groups" multiple>
                            <option ng-repeat="d in department_groups" ng-value="d.id"
                                ng-selected="arrayInclude(config.config_department_groups, d.id)"><% d.name %></option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-3 col-form-label text-md-right">Ràng buộc lập HĐ theo thị trường</label>
                <div class="col-md-9">
                    <div class="border-checkbox-section mb-2">
                        <div class="border-checkbox-group border-checkbox-group-primary">
                            <input class="border-checkbox" type="checkbox" id="is_equipment" ng-model="config.is_equipment" ng-checked="config.is_equipment == 1">
                            <label class="border-checkbox-label m-0" for="is_equipment">HĐ bán hàng</label>
                        </div>
                    </div>
                    <div class="border-checkbox-section mb-2">
                        <div class="border-checkbox-group border-checkbox-group-primary">
                            <input class="border-checkbox" type="checkbox" id="is_repair" ng-model="config.is_repair" ng-checked="config.is_repair == 1">
                            <label class="border-checkbox-label m-0" for="is_repair">HĐ dịch vụ</label>
                        </div>
                    </div>
                    <div class="border-checkbox-section mb-2">
                        <div class="border-checkbox-group border-checkbox-group-primary">
                            <input class="border-checkbox" type="checkbox" id="is_project" ng-model="config.is_project" ng-checked="config.is_project == 1">
                            <label class="border-checkbox-label m-0" for="is_project">HĐ dự án</label>
                        </div>
                    </div>
                    <div class="border-checkbox-section mb-2">
                        <div class="border-checkbox-group border-checkbox-group-primary">
                            <input class="border-checkbox" type="checkbox" id="is_principle" ng-model="config.is_principle" ng-checked="config.is_principle == 1">
                            <label class="border-checkbox-label m-0" for="is_principle">HĐ nguyên tắc</label>
                        </div>
                    </div>
                    <div class="border-checkbox-section mb-2">
                        <div class="border-checkbox-group border-checkbox-group-primary">
                            <input class="border-checkbox" type="checkbox" id="is_dental_principle" ng-model="config.is_dental_principle" ng-checked="config.is_dental_principle == 1">
                            <label class="border-checkbox-label m-0" for="is_dental_principle">HĐ nguyên tắc nha khoa</label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    @include('common.configs.partials.tab_buttons', ['tab' => 'business'])
</div>
```

- [ ] **Step 4: Create Tab 4 — warehouse.blade.php**

Create file `TanPhatDev/resources/views/common/configs/tabs/warehouse.blade.php`:

```php
<div class="card-body">
    <div class="row">
        <div class="col-md-6">
            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Thuế vận tải</label>
                <div class="col-md-6">
                    <div class="input-group mb-0">
                        <input type="number" class="form-control text-right" step="1"
                            ng-class="{'is-invalid': errors && errors.vat_delivery_trip_percent}"
                            ng-model="config.vat_delivery_trip_percent">
                        <span class="input-group-addon">%</span>
                    </div>
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.vat_delivery_trip_percent">
                        <strong><% errors.vat_delivery_trip_percent[0] %></strong>
                    </span>
                </div>
            </div>
        </div>
    </div>

    @include('common.configs.partials.tab_buttons', ['tab' => 'warehouse'])
</div>
```

- [ ] **Step 5: Commit**

```bash
git add resources/views/common/configs/tabs/general.blade.php resources/views/common/configs/tabs/category.blade.php resources/views/common/configs/tabs/business.blade.php resources/views/common/configs/tabs/warehouse.blade.php
git commit -m "feat: add tab partial views for General, Category, Business, Warehouse"
```

---

### Task 6: Create tab partial views (Tab 5-7)

**Files:**
- Create: `resources/views/common/configs/tabs/xnk.blade.php`
- Create: `resources/views/common/configs/tabs/accounting.blade.php`
- Create: `resources/views/common/configs/tabs/cskh.blade.php`

- [ ] **Step 1: Create Tab 5 — xnk.blade.php**

Create file `TanPhatDev/resources/views/common/configs/tabs/xnk.blade.php`:

```php
<div class="card-body">
    <div class="row">
        <div class="col-md-6">
            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Hệ số thuế bảo vệ môi trường <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="text" class="form-control text-right"
                        ng-class="{'is-invalid': errors && errors.environment_tax}" ng-model="config.environment_tax">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.environment_tax">
                        <strong><% errors.environment_tax[0] %></strong>
                    </span>
                </div>
            </div>
        </div>
    </div>

    @include('common.configs.partials.tab_buttons', ['tab' => 'xnk'])
</div>
```

- [ ] **Step 2: Create Tab 6 — accounting.blade.php**

Create file `TanPhatDev/resources/views/common/configs/tabs/accounting.blade.php`:

```php
<div class="card-body">
    <div class="row">
        <div class="col-md-6">
            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Hệ số giá thương mại điện tử <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="text" class="form-control text-right"
                        ng-class="{'is-invalid': errors && errors.coefficient_ecommerce_price}" ng-model="config.coefficient_ecommerce_price">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.coefficient_ecommerce_price">
                        <strong><% errors.coefficient_ecommerce_price[0] %></strong>
                    </span>
                </div>
            </div>

            <div class="form-group row">
                <label class="col-md-6 col-form-label text-md-right">Ngày khai báo công nợ đầu kỳ <span class="text-danger">(*)</span></label>
                <div class="col-md-6">
                    <input type="text" class="form-control text-right" date-form
                        ng-class="{'is-invalid': errors && errors.debt_calculation_date}" ng-model="config.debt_calculation_date">
                    <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.debt_calculation_date">
                        <strong><% errors.debt_calculation_date[0] %></strong>
                    </span>
                </div>
            </div>
        </div>
    </div>

    @include('common.configs.partials.tab_buttons', ['tab' => 'accounting'])
</div>
```

- [ ] **Step 3: Create Tab 7 — cskh.blade.php**

Create file `TanPhatDev/resources/views/common/configs/tabs/cskh.blade.php`:

```php
<div class="card-body">
    <div class="form-group row">
        <div class="col-md-6">
            <label class="col-form-label text-md-right">Hàng không bắt buộc Serial</label>
            <div class="input-group mb-0">
                <select class="select2 form-control" name="serial_product_types[]"
                    ng-class="{'is-invalid': errors && errors.serial_product_types}"
                    ng-model="config.serial_product_types" multiple>
                    <option ng-repeat="type in product_types" ng-value="type.value"
                        ng-selected="config.config_serial_product_types.includes(type.value)"><% type.name %></option>
                </select>
            </div>
            <span class="invalid-feedback d-block" role="alert" ng-if="errors && errors.serial_product_types">
                <strong><% errors.serial_product_types[0] %></strong>
            </span>
        </div>
    </div>

    <hr>

    <div class="form-group row">
        <div class="col-md-12">
            <label class="col-form-label text-md-right">Bảng tính công khoán</label>
            <div style="max-height: 500px; overflow-y: auto; width: 100%; overflow-x: auto;">
                <table class="table table-hover table-condensed table-bordered table-head-border" style="min-width: 800px;">
                    <thead>
                        <tr>
                            <th style="width: 30%">Nhóm hàng hóa</th>
                            <th style="width: 30%">Tính chất hàng hóa</th>
                            <th style="width: 20%">SL hàng tính công khoán</th>
                            <th style="width: 10%; min-width: 80px">
                                <a class="btn btn-link text-success p-0" type="button" ng-click="addNewRow()">
                                    <i class="fa fa-plus"></i>
                                </a>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr ng-repeat="row in config.contract_rows track by $index">
                            <td class="text-center">
                                <select class="select2 form-control" name="product_groups[]"
                                    ng-class="{'is-invalid': errors && errors['contract_rows.' + $index + '.product_group'][0]}"
                                    ng-model="row.product_group" multiple>
                                    <option ng-repeat="group in groups" ng-value="group.id"
                                        ng-selected="arrayInclude(row.product_group, group.id)"><% group.name %></option>
                                </select>
                                <span class="invalid-feedback d-block" role="alert">
                                    <strong><% errors['contract_rows.' + $index + '.product_group'][0] %></strong>
                                </span>
                            </td>
                            <td class="text-center">
                                <select class="select2 form-control" name="product_types[]"
                                    ng-class="{'is-invalid': errors && errors['contract_rows.' + $index + '.product_nature'][0]}"
                                    ng-model="row.product_nature" multiple>
                                    <option ng-repeat="type in product_types" ng-value="type.value"
                                        ng-selected="row.product_nature.includes(type.value)"><% type.name %></option>
                                </select>
                                <span class="invalid-feedback d-block" role="alert">
                                    <strong><% errors['contract_rows.' + $index + '.product_nature'][0] %></strong>
                                </span>
                            </td>
                            <td class="text-center">
                                <input type="number" class="form-control text-right"
                                    min="0" step="1" style="min-width: 120px;"
                                    ng-class="{'is-invalid': errors && errors['contract_rows.' + $index + '.quantity'][0]}"
                                    ng-model="row.quantity"
                                    ng-change="validateQuantity(row)">
                                <span class="invalid-feedback d-block" role="alert">
                                    <strong><% errors['contract_rows.' + $index + '.quantity'][0] %></strong>
                                </span>
                            </td>
                            <td class="text-center">
                                <button class="btn btn-link text-danger p-0" type="button" ng-click="removeRow($index)">
                                    <i class="fa fa-minus"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <span class="invalid-feedback d-block" role="alert">
                    <strong><% errors['contract_rows'][0] %></strong>
                </span>
            </div>
        </div>
    </div>

    @include('common.configs.partials.tab_buttons', ['tab' => 'cskh'])
</div>
```

- [ ] **Step 4: Commit**

```bash
git add resources/views/common/configs/tabs/xnk.blade.php resources/views/common/configs/tabs/accounting.blade.php resources/views/common/configs/tabs/cskh.blade.php
git commit -m "feat: add tab partial views for XNK, Accounting, CSKH"
```

---

### Task 7: Rewrite edit.blade.php (main layout + Angular controller)

**Files:**
- Modify: `resources/views/common/configs/edit.blade.php` (complete rewrite)

- [ ] **Step 1: Rewrite edit.blade.php**

Replace the entire contents of `TanPhatDev/resources/views/common/configs/edit.blade.php` with:

```php
@extends('layouts.app')
@section('title')
    Cấu hình hệ thống
@endsection
@section('content')
<div ng-controller="ConfigController">
    <div class="row justify-content-center">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">Cài đặt cấu hình</div>
                <div class="card-body p-0">
                    <ul class="nav nav-tabs px-3 pt-3" id="configTabs" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" id="tab-general-link" data-toggle="tab" href="#tab-general" role="tab">Thông tin chung</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="tab-category-link" data-toggle="tab" href="#tab-category" role="tab">Danh mục</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="tab-business-link" data-toggle="tab" href="#tab-business" role="tab">Kinh doanh</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="tab-warehouse-link" data-toggle="tab" href="#tab-warehouse" role="tab">Kho</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="tab-xnk-link" data-toggle="tab" href="#tab-xnk" role="tab">XNK</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="tab-accounting-link" data-toggle="tab" href="#tab-accounting" role="tab">Kế toán</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="tab-cskh-link" data-toggle="tab" href="#tab-cskh" role="tab">CSKH</a>
                        </li>
                    </ul>
                    <div class="tab-content p-3" id="configTabContent">
                        <div class="tab-pane fade show active" id="tab-general" role="tabpanel">
                            @include('common.configs.tabs.general')
                        </div>
                        <div class="tab-pane fade" id="tab-category" role="tabpanel">
                            @include('common.configs.tabs.category')
                        </div>
                        <div class="tab-pane fade" id="tab-business" role="tabpanel">
                            @include('common.configs.tabs.business')
                        </div>
                        <div class="tab-pane fade" id="tab-warehouse" role="tabpanel">
                            @include('common.configs.tabs.warehouse')
                        </div>
                        <div class="tab-pane fade" id="tab-xnk" role="tabpanel">
                            @include('common.configs.tabs.xnk')
                        </div>
                        <div class="tab-pane fade" id="tab-accounting" role="tabpanel">
                            @include('common.configs.tabs.accounting')
                        </div>
                        <div class="tab-pane fade" id="tab-cskh" role="tabpanel">
                            @include('common.configs.tabs.cskh')
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    @include('common.configs.partials.history_modal')
</div>
@endsection
@section('script')
<script src="{{ asset('pages/ckeditor/ckeditor.js') }}"></script>
<script>
    class Config {
        constructor(object) {
            this.no_set = [];
            if (object) {
                for (let key in object) {
                    if (!this.no_set.includes(key)) this[key] = object[key];
                }
            }
        }

        get max_prepick_date() { return this._max_prepick_date; }
        set max_prepick_date(value) { this._max_prepick_date = Number(value); }

        get consignment_holding_time() { return this._consignment_holding_time; }
        set consignment_holding_time(value) { this._consignment_holding_time = Number(value); }

        get max_prepick_date_project_contract() { return this._max_prepick_date_project_contract; }
        set max_prepick_date_project_contract(value) { this._max_prepick_date_project_contract = Number(value); }

        get max_borrow_date() { return this._max_borrow_date; }
        set max_borrow_date(value) { this._max_borrow_date = Number(value); }

        get vat_delivery_trip_percent() { return this._vat_delivery_trip_percent; }
        set vat_delivery_trip_percent(value) { this._vat_delivery_trip_percent = Number(value); }

        get quotation_valid_days() { return this._quotation_valid_days; }
        set quotation_valid_days(value) { this._quotation_valid_days = Number(value); }

        get environment_tax() { return this._environment_tax ? this._environment_tax.toLocaleString('en') : 0; }
        set environment_tax(value) { this._environment_tax = parseNumberString(value); }

        get customer_taken_care() { return this._customer_taken_care; }
        set customer_taken_care(value) { this._customer_taken_care = Number(value); }

        get customer_is_following() { return this._customer_is_following; }
        set customer_is_following(value) { this._customer_is_following = Number(value); }

        get is_equipment() { return this._is_equipment; }
        set is_equipment(value) { this._is_equipment = !!value; }

        get is_repair() { return this._is_repair; }
        set is_repair(value) { this._is_repair = !!value; }

        get is_project() { return this._is_project; }
        set is_project(value) { this._is_project = !!value; }

        get is_principle() { return this._is_principle; }
        set is_principle(value) { this._is_principle = !!value; }

        get is_dental_principle() { return this._is_dental_principle; }
        set is_dental_principle(value) { this._is_dental_principle = !!value; }

        get config_product_types() {
            return this.product_types && !Array.isArray(this.product_types) ? this.product_types.split(',') : this.product_types || [];
        }

        get config_serial_product_types() {
            return this.serial_product_types && !Array.isArray(this.serial_product_types) ? this.serial_product_types.split(',') : this.serial_product_types || [];
        }

        get config_customer_groups() {
            return this.customer_groups && !Array.isArray(this.customer_groups) ? this.customer_groups.split(',') : this.customer_groups || [];
        }

        get config_department_groups() {
            return this.department_groups && !Array.isArray(this.department_groups) ? this.department_groups.split(',') : this.department_groups || [];
        }
    }
</script>
<script>
    app.controller('ConfigController', function ($scope) {
        $scope.config = new Config(@json($config));
        $scope.product_types = PRODUCT_TYPES;
        $scope.customer_groups = @json($customerGroups);
        $scope.department_groups = @json($departmentGroups);
        $scope.groups = @json($groups);
        $scope.hiddenProductTypes = @json($hiddenProductTypes);
        $scope.ticketTypes = @json($ticketTypes);
        $scope.productCategories = @json($productCategories);
        $scope.loading = {};
        $scope.errors = {};
        $scope.histories = [];
        $scope.historyLoading = false;

        if (!$scope.config.contract_rows) {
            $scope.config.contract_rows = [];
        }

        setTimeout(function() { $('.select2').select2(); }, 100);

        // --- Tab-specific data builders ---
        $scope.getTabData = function(tab) {
            let c = $scope.config;
            switch (tab) {
                case 'general':
                    return { logo: c.logo, title: c.title, description: c.description };
                case 'category':
                    return {
                        product_types: c.config_product_types,
                        hidden_product_types: $scope.hiddenProductTypes
                    };
                case 'business':
                    return {
                        max_borrow_date: c.max_borrow_date,
                        max_prepick_date: c.max_prepick_date,
                        consignment_holding_time: c.consignment_holding_time,
                        max_prepick_date_project_contract: c.max_prepick_date_project_contract,
                        warning_day: c.warning_day,
                        customer_is_following: c.customer_is_following,
                        customer_taken_care: c.customer_taken_care,
                        quotation_valid_days: c.quotation_valid_days,
                        project_quotation_valid_days: c.project_quotation_valid_days,
                        customer_register_expiry: c.customer_register_expiry,
                        customer_groups: c.config_customer_groups,
                        department_groups: c.config_department_groups,
                        is_equipment: c.is_equipment ? 1 : 0,
                        is_repair: c.is_repair ? 1 : 0,
                        is_project: c.is_project ? 1 : 0,
                        is_principle: c.is_principle ? 1 : 0,
                        is_dental_principle: c.is_dental_principle ? 1 : 0,
                    };
                case 'warehouse':
                    return { vat_delivery_trip_percent: c.vat_delivery_trip_percent };
                case 'xnk':
                    return { environment_tax: c._environment_tax || 0 };
                case 'accounting':
                    return {
                        coefficient_ecommerce_price: c.coefficient_ecommerce_price,
                        debt_calculation_date: c.debt_calculation_date,
                    };
                case 'cskh':
                    return {
                        serial_product_types: c.config_serial_product_types,
                        contract_rows: c.contract_rows || [],
                    };
            }
        };

        // --- Submit per tab ---
        $scope.submitTab = function(tab) {
            $scope.loading[tab] = true;
            $scope.errors = {};
            let data = $scope.getTabData(tab);
            $.ajax({
                type: 'POST',
                url: "{{ url('admin/configs/update') }}/" + tab,
                headers: { 'X-CSRF-TOKEN': CSRF_TOKEN },
                data: data,
                success: function(response) {
                    if (response.success) {
                        toastr.success(response.message);
                    } else {
                        $scope.errors = response.errors;
                        toastr.warning(response.message);
                    }
                },
                error: function() { toastr.error('Đã có lỗi xảy ra'); },
                complete: function() {
                    $scope.loading[tab] = false;
                    $scope.$applyAsync();
                }
            });
        };

        // --- History modal ---
        $scope.showHistory = function(tab) {
            $scope.historyLoading = true;
            $scope.histories = [];
            $('#historyModal').modal('show');
            $scope.$applyAsync();
            $.get("{{ url('admin/configs/histories') }}/" + tab, function(response) {
                $scope.histories = response.data;
                $scope.historyLoading = false;
                $scope.$applyAsync();
            });
        };

        // --- Tab 2: Hidden product types ---
        $scope.addHiddenRow = function() {
            $scope.hiddenProductTypes.push({ product_types: [], ticket_types: [] });
            setTimeout(function() { $('.select2').select2(); }, 100);
        };
        $scope.removeHiddenRow = function(index) {
            $scope.hiddenProductTypes.splice(index, 1);
        };

        // --- Tab 7: Contract rows ---
        $scope.addNewRow = function() {
            $scope.config.contract_rows.push({ product_group: [''], product_nature: [''], quantity: 0 });
            setTimeout(function() { $('.select2').select2(); }, 100);
        };
        $scope.removeRow = function(index) {
            $scope.config.contract_rows.splice(index, 1);
        };
        $scope.validateQuantity = function(row) {
            row.quantity = Math.floor(row.quantity);
        };

        // --- Logo upload ---
        $(document).on('change', "#upload-logo", function() {
            if (this.files && this.files[0]) {
                var data = new FormData();
                data.append('_token', CSRF_TOKEN);
                data.append('file[]', this.files[0]);
                $.ajax({
                    url: "{{ route('uploadImg') }}",
                    dataType: 'text',
                    cache: false,
                    contentType: false,
                    processData: false,
                    data: data,
                    type: 'post',
                    success: function (res) {
                        res = JSON.parse(res);
                        if (res.success) $scope.config.logo = res.data.pop();
                    },
                    error: function () { toastr.error('Đã có lỗi xảy ra'); },
                    complete: function() { $scope.$applyAsync(); }
                });
            }
        });

        // --- Re-init select2 on tab change ---
        $('a[data-toggle="tab"]').on('shown.bs.tab', function () {
            setTimeout(function() { $('.select2').select2(); }, 100);
        });
    });
</script>
@endsection
```

- [ ] **Step 2: Verify the page loads**

Run: Navigate to `admin/configs/edit` in browser.

Expected: 7 tabs displayed. Tab 1 (Thông tin chung) active by default with Logo, Title, Description fields. All existing data populated correctly.

- [ ] **Step 3: Test each tab**

Click through all 7 tabs. Verify:
- Tab 1: Logo, Title, Description display correctly
- Tab 2: Product natures select populated + empty hidden product types table with (+) button
- Tab 3: All 13 business fields display correctly with current values
- Tab 4: Transport tax field with % suffix
- Tab 5: Environment tax field
- Tab 6: E-commerce coefficient + Debt date picker
- Tab 7: Serial product types select + Contract rows table
- Each tab has Save, History, Cancel buttons

- [ ] **Step 4: Test Save per tab**

On Tab 4 (Kho), change "Thuế vận tải" to a different value, click Save.

Expected: toastr success message. Reload page — value persists. Other tab values unchanged.

- [ ] **Step 5: Test History**

On Tab 4, click "Lịch sử chỉnh sửa".

Expected: Modal opens showing the change just made — updater name, "Thuế vận tải", old value, new value, timestamp.

- [ ] **Step 6: Test Tab 2 hidden product types**

On Tab 2, click (+) to add a row. Select "Ngừng kinh doanh" as loại HH, select "Phiếu Yêu cầu hỏi giá" as loại phiếu. Click Save.

Expected: toastr success. Reload — row persists with correct selections.

- [ ] **Step 7: Commit**

```bash
git add resources/views/common/configs/edit.blade.php
git commit -m "feat: rewrite config edit page with 7-tab layout, per-tab save, and change history"
```

---

### Task 8: Final cleanup and integration test

**Files:**
- No new files

- [ ] **Step 1: Test all tabs save independently**

1. Go to Tab 3 (Kinh doanh), change "Số ngày mượn tối đa" to 99
2. Click Save — verify success
3. Go to Tab 4 (Kho), verify "Thuế vận tải" is unchanged
4. Go back to Tab 3, verify "Số ngày mượn tối đa" is 99
5. Check database: `SELECT max_borrow_date, vat_delivery_trip_percent FROM configs LIMIT 1`

- [ ] **Step 2: Test validation per tab**

1. Tab 1: Clear "Tiêu đề", click Save — expect validation error "Bắt buộc nhập"
2. Tab 3: Set "Số ngày mượn tối đa" to 0, click Save — expect validation error
3. Tab 2: Add hidden row, select loại HH but leave loại phiếu empty, click Save — expect "Bắt buộc chọn loại phiếu"

- [ ] **Step 3: Test history across multiple tabs**

1. Make changes to Tab 3, Tab 5, Tab 6 sequentially
2. Click History on Tab 3 — should only show Tab 3 changes
3. Click History on Tab 5 — should only show Tab 5 changes
4. Click History on Tab 6 — should only show Tab 6 changes

- [ ] **Step 4: Test that old update route still works (backward compatibility)**

Verify the old `POST /admin/configs` route still exists (it was kept in routes). This ensures no other part of the system that might call it directly breaks. It can be removed in a future cleanup task.

- [ ] **Step 5: Final commit if any fixes needed**

```bash
git add -A
git commit -m "fix: address issues found during integration testing"
```
