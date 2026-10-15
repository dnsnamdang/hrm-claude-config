# Task 2 — 5 child entity cho BorrowSellRequest

**Repo:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api` (nhánh gop_db). Laravel 8, PHP 7.4.

Tạo 5 file Eloquent model trong namespace `Modules\Finance\Entities\BorrowSellRequest`. Extends `Illuminate\Database\Eloquent\Model` trần, KHÔNG set `$connection` (dùng default = DB gộp). `protected $guarded = ['id'];`.

## Cột thực tế các bảng (đã xác nhận qua Schema — dùng để chắc chắn field gán tồn tại, KHÔNG bịa cột)
- `borrow_sell_request_products`: id,parent_id,objectable_id,objectable_type,product_id,product_name,unit_id,unit_name,brand_id,brand_name,model_id,model_name,code,price,extra_price,contract_qty,qty,contract_promotion_id,unit_coefficient,approved_qty,returned_qty,allocated_price,export_price,net_price,rebate_price,usage_status,vat_percent,created_at,updated_at
- `borrow_sell_request_product_details`: id,parent_id,request_id,product_export_request_id,product_export_request_detail_id,product_id,unit_id,qty,approved_qty,created_at,updated_at
- `borrow_sell_request_tabs`: id,parent_id,firm_contract_id,firm_contract_tab_id,name,created_at,updated_at
- `borrow_sell_request_tab_products`: id,parent_id,borrow_sell_request_id,firm_contract_id,firm_contract_tab_id,product_id,unit_id,contract_qty,qty,approved_qty,exported_qty,returned_qty,vat_percent,created_at,updated_at
- `borrow_sell_request_tab_product_details`: id,parent_id,borrow_sell_request_id,firm_contract_tab_id,product_export_request_id,product_export_request_detail_id,product_id,unit_id,qty,approved_qty,created_at,updated_at

## File 1: `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequestProductDetail.php`
```php
<?php
namespace Modules\Finance\Entities\BorrowSellRequest;

use Illuminate\Database\Eloquent\Model;

class BorrowSellRequestProductDetail extends Model
{
    protected $table = 'borrow_sell_request_product_details';
    public $timestamps = true;
    protected $guarded = ['id'];
}
```

## File 2: `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequestProduct.php`
```php
<?php
namespace Modules\Finance\Entities\BorrowSellRequest;

use Illuminate\Database\Eloquent\Model;

class BorrowSellRequestProduct extends Model
{
    protected $table = 'borrow_sell_request_products';
    public $timestamps = true;
    protected $guarded = ['id'];

    public function details()
    {
        return $this->hasMany(BorrowSellRequestProductDetail::class, 'parent_id', 'id');
    }
}
```

## File 3: `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequestTabProductDetail.php`
```php
<?php
namespace Modules\Finance\Entities\BorrowSellRequest;

use Illuminate\Database\Eloquent\Model;

class BorrowSellRequestTabProductDetail extends Model
{
    protected $table = 'borrow_sell_request_tab_product_details';
    public $timestamps = true;
    protected $guarded = ['id'];
}
```

## File 4: `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequestTabProduct.php`
```php
<?php
namespace Modules\Finance\Entities\BorrowSellRequest;

use Illuminate\Database\Eloquent\Model;

class BorrowSellRequestTabProduct extends Model
{
    protected $table = 'borrow_sell_request_tab_products';
    public $timestamps = true;
    protected $guarded = ['id'];

    public function details()
    {
        return $this->hasMany(BorrowSellRequestTabProductDetail::class, 'parent_id', 'id');
    }

    // Tạo các dòng chi tiết của 1 sản phẩm trong tab
    public function syncTabProductDetails($tab, array $details)
    {
        foreach ($details as $detail) {
            $d = new BorrowSellRequestTabProductDetail();
            $d->parent_id = $this->id;
            $d->borrow_sell_request_id = $tab->parent_id;
            $d->firm_contract_tab_id = $tab->firm_contract_tab_id;
            $d->product_export_request_id = $detail['product_export_request_id'] ?? null;
            $d->product_export_request_detail_id = $detail['product_export_request_detail_id'] ?? null;
            $d->product_id = $detail['product_id'] ?? null;
            $d->unit_id = $detail['unit_id'] ?? null;
            $d->qty = $detail['qty'] ?? 0;
            $d->save();
        }
    }
}
```

## File 5: `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequestTab.php`
```php
<?php
namespace Modules\Finance\Entities\BorrowSellRequest;

use Illuminate\Database\Eloquent\Model;

class BorrowSellRequestTab extends Model
{
    protected $table = 'borrow_sell_request_tabs';
    public $timestamps = true;
    protected $guarded = ['id'];

    public function products()
    {
        return $this->hasMany(BorrowSellRequestTabProduct::class, 'parent_id');
    }

    // Tạo các sản phẩm của tab + chi tiết từng sản phẩm
    public function syncTabProducts($products)
    {
        foreach ($products as $pro) {
            if (!isset($pro['details'])) {
                continue;
            }
            $p = new BorrowSellRequestTabProduct();
            $p->parent_id = $this->id;
            $p->borrow_sell_request_id = $this->parent_id;
            $p->firm_contract_id = $this->firm_contract_id;
            $p->firm_contract_tab_id = $this->firm_contract_tab_id;
            $p->product_id = $pro['product_id'];
            $p->unit_id = $pro['unit_id'];
            $p->exported_qty = $pro['exported_qty'] ?? 0;
            $p->qty = $pro['qty'] ?? 0;
            $p->contract_qty = $pro['contract_qty'] ?? 0;
            $p->vat_percent = $pro['vat_percent'] ?? 0;
            $p->save();
            $p->syncTabProductDetails($this, $pro['details']);
        }
    }
}
```

## Verify (bắt buộc chạy, dán output vào report)
```
php artisan tinker --execute="
echo Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequestProduct::query()->count().PHP_EOL;
echo Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequestProductDetail::query()->count().PHP_EOL;
echo Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequestTab::query()->count().PHP_EOL;
echo Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequestTabProduct::query()->count().PHP_EOL;
echo Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequestTabProductDetail::query()->count().PHP_EOL;
"
```
Kỳ vọng: in ra 5 con số (0 hoặc >0), KHÔNG lỗi "table/class not found".

## KHÔNG làm
- KHÔNG tạo entity cha `BorrowSellRequest.php` (Task 3 làm).
- KHÔNG commit. KHÔNG dispatch subagent. KHÔNG sửa file khác.

## Report
Ghi vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-2-report.md`: 5 đường dẫn file tạo, output lệnh verify. Trả về: STATUS, 1 dòng tóm tắt verify, concerns.
