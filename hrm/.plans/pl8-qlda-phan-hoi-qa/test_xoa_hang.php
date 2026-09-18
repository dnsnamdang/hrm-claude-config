<?php
/**
 * Bug: "xoá hàng hoá bấm Lưu nhưng không nhận" (báo giá BG-2026-00419).
 *
 * Nguyên nhân: QuotationService::update dùng `!empty($data['products'])` -> xoá HẾT hàng thì FE gửi
 * `products: []`, điều kiện false ⇒ bỏ qua luôn bước đồng bộ dòng hàng, dòng cũ nằm nguyên trong DB.
 * Sửa thành `isset(...)`. Bộ test này phủ cả 2 chiều để chắc không phá luồng khác.
 */
$root = '/Users/manhcuong/Desktop/dns/HRM/worktrees/tpe-api';
require $root . '/vendor/autoload.php';
$app = require $root . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Http\Kernel::class);
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Http\Request;
use Modules\Assign\Entities\Quotation;

const TAG = 'TSTXOA';

$pass = 0; $fail = 0; $msgs = [];
function ok($cond, $name, $extra = '') {
    global $pass, $fail, $msgs;
    if ($cond) { $pass++; echo "  ✓ $name\n"; }
    else { $fail++; $msgs[] = $name . ($extra ? " | $extra" : ''); echo "  ✗ $name" . ($extra ? " | $extra" : '') . "\n"; }
}

function api($method, $uri, $payload, $employeeId) {
    global $kernel, $app;
    $tok = \Tymon\JWTAuth\Facades\JWTAuth::fromUser(\App\Models\TpEmployee::find($employeeId));
    \Illuminate\Support\Facades\Auth::forgetGuards();
    $req = Request::create($uri, $method, [], [], [], [
        'CONTENT_TYPE' => 'application/json',
        'HTTP_ACCEPT' => 'application/json',
        'HTTP_AUTHORIZATION' => 'Bearer ' . $tok,
    ], json_encode($payload));
    $app->instance('request', $req);
    \Tymon\JWTAuth\Facades\JWTAuth::setRequest($req);
    \Tymon\JWTAuth\Facades\JWTAuth::unsetToken();
    \Illuminate\Support\Facades\Auth::guard('api')->setUser(\App\Models\TpEmployee::find($employeeId));
    $res = $kernel->handle($req);
    \Illuminate\Support\Facades\Auth::forgetGuards();
    return [$res->getStatusCode(), json_decode($res->getContent(), true)];
}

function cleanup() {
    $qIds = DB::table('quotations')->where('code', 'like', TAG . '%')->pluck('id');
    if ($qIds->count()) {
        DB::table('quotation_product_prices')->whereIn('quotation_id', $qIds)->delete();
        DB::table('quotation_service_items')->whereIn('quotation_id', $qIds)->delete();
        DB::table('quotations')->whereIn('id', $qIds)->delete();
    }
    DB::table('prospective_projects')->where('name', 'like', TAG . '%')->delete();
}
cleanup();

$emp = 34;
DB::table('employees')->where('id', $emp)->update(['password' => Hash::make('Test@12345'), 'password_changed_at' => now()->subDay(), 'token_version' => 1]);
$khachHang = DB::table('prospective_projects')->whereNotNull('customer_id')->value('customer_id');
$now = now();

$duAn = DB::table('prospective_projects')->insertGetId([
    'name' => TAG . ' - Du an', 'code' => TAG . '-DA', 'company_id' => 1, 'customer_id' => $khachHang,
    'main_sale_employee_id' => $emp, 'created_by' => $emp, 'updated_by' => $emp,
    'created_at' => $now, 'updated_at' => $now,
]);

function mkQuotation($code, $projectId, $emp, $bomListId = null) {
    $now = now();
    return DB::table('quotations')->insertGetId([
        'code' => $code, 'project_id' => $projectId, 'type' => Quotation::TYPE_SELF_BUILT,
        'bom_list_id' => $bomListId, 'is_summary' => 0, 'status' => Quotation::STATUS_DANG_TAO,
        'company_id' => 1, 'customer_id' => DB::table('prospective_projects')->where('id', $projectId)->value('customer_id'),
        'price_type_id' => 1, 'exchange_rate' => 1,
        'created_by' => $emp, 'updated_by' => $emp, 'created_at' => $now, 'updated_at' => $now,
    ]);
}
function mkRow($qId, $name, $erpId = null) {
    $now = now();
    return DB::table('quotation_product_prices')->insertGetId([
        'quotation_id' => $qId, 'code' => $erpId ? 'ERP-' . $erpId : null, 'name' => $name,
        'erp_product_id' => $erpId, 'qty_needed' => 1, 'estimated_price' => 100, 'quoted_price' => 200,
        'created_at' => $now, 'updated_at' => $now,
    ]);
}
function soDong($qId) {
    return DB::table('quotation_product_prices')->where('quotation_id', $qId)->count();
}
function tenDong($qId) {
    return DB::table('quotation_product_prices')->where('quotation_id', $qId)->pluck('name')->sort()->values()->toJson();
}

// ============ TC1: xoá HẾT hàng hoá (ca người dùng báo) ============
echo "\nTC1 — Báo giá tự lập, xoá HẾT hàng rồi Lưu (products: [])\n";
$q1 = mkQuotation(TAG . '-Q1', $duAn, $emp);
mkRow($q1, TAG . ' hang 1');
ok(soDong($q1) === 1, 'Chuẩn bị: có 1 dòng hàng');
list($c1) = api('PUT', "/api/v1/assign/quotations/$q1", ['products' => []], $emp);
ok($c1 === 200, 'API trả 200', "code=$c1");
ok(soDong($q1) === 0, 'Dòng hàng ĐÃ bị xoá khỏi DB (trước fix: vẫn còn)', 'còn ' . soDong($q1) . ' dòng');

// ============ TC2: xoá 1 trong nhiều dòng — dòng còn lại phải giữ ============
echo "\nTC2 — Xoá 1 dòng, giữ các dòng còn lại\n";
$q2 = mkQuotation(TAG . '-Q2', $duAn, $emp);
$r1 = mkRow($q2, TAG . ' giu lai');
$r2 = mkRow($q2, TAG . ' se xoa');
list($c2) = api('PUT', "/api/v1/assign/quotations/$q2", ['products' => [[
    'price_id' => $r1, 'code' => null, 'name' => TAG . ' giu lai', 'erp_product_id' => null,
    'qty_needed' => 1, 'estimated_price' => 100, 'quoted_price' => 200,
]]], $emp);
ok($c2 === 200, 'API trả 200', "code=$c2");
ok(soDong($q2) === 1, 'Còn đúng 1 dòng', 'còn ' . soDong($q2));
ok(strpos(tenDong($q2), 'giu lai') !== false, 'Dòng giữ lại đúng là dòng không bị xoá', tenDong($q2));

// ============ TC3: KHÔNG gửi key products -> không đụng dòng hàng ============
echo "\nTC3 — Lưu mà payload KHÔNG có key products (chỉ sửa thông tin chung)\n";
$q3 = mkQuotation(TAG . '-Q3', $duAn, $emp);
mkRow($q3, TAG . ' khong duoc mat');
list($c3) = api('PUT', "/api/v1/assign/quotations/$q3", ['note' => 'chi sua ghi chu'], $emp);
ok($c3 === 200, 'API trả 200', "code=$c3");
ok(soDong($q3) === 1, 'Dòng hàng GIỮ NGUYÊN (không bị xoá oan)', 'còn ' . soDong($q3));

// ============ TC4: báo giá TỪ BOM, gửi products rỗng -> không mất dòng ============
echo "\nTC4 — Báo giá lập từ BOM, gửi products rỗng\n";
$bom = DB::table('bom_lists')->insertGetId([
    'code' => TAG . '-BOM', 'bom_list_type' => 1, 'status' => 1, 'prospective_project_id' => $duAn,
    'company_id' => 1, 'created_by' => $emp, 'updated_by' => $emp, 'created_at' => $now, 'updated_at' => $now,
]);
$q4 = mkQuotation(TAG . '-Q4', $duAn, $emp, $bom);
mkRow($q4, TAG . ' hang tu BOM');
list($c4) = api('PUT', "/api/v1/assign/quotations/$q4", ['products' => []], $emp);
ok(soDong($q4) === 1, 'Báo giá từ BOM KHÔNG bị xoá dòng khi products rỗng', 'còn ' . soDong($q4) . ' dòng, code=' . $c4);

echo "\n==============================\nPASS: $pass | FAIL: $fail\n";
foreach ($msgs as $m) echo " - $m\n";
DB::table('bom_lists')->where('code', 'like', TAG . '%')->delete();
cleanup();
$left = DB::table('quotations')->where('code', 'like', TAG . '%')->count()
    + DB::table('prospective_projects')->where('name', 'like', TAG . '%')->count();
echo "Đã dọn fixture, còn sót: $left\n";
exit($fail > 0 ? 1 : 0);
