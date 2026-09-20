<?php
/**
 * Redmine #10804 — Bảng giá ERP trên báo giá.
 * Phản hồi QA: "Có dự án cha A và dự án con B. Tạo nháp báo giá A với bảng giá = Giá bán thương mại
 * điện tử (online). Tạo mới báo giá B → B không kế thừa được bảng giá từ A".
 *
 * Luật sau khi sửa: báo giá dự án CON lấy Bảng giá theo thứ tự
 *   1) prospective_projects.price_type_id của chính dự án con (kế thừa lúc tạo dự án)
 *   2) Bảng giá của BÁO GIÁ MỚI NHẤT thuộc dự án cha
 *   3) mặc định 1 (Bán lẻ)
 * Dự án độc lập (không có cha) vẫn lấy đúng bảng giá người dùng chọn.
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

const TAG = 'TST10804';

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
    DB::table('quotations')->where('project_id', function ($q) {
        $q->select('id')->from('prospective_projects')->where('name', 'like', TAG . '%')->limit(1);
    })->delete();
    DB::table('prospective_projects')->where('name', 'like', TAG . '%')->delete();
}
cleanup();

$emp = 34;
DB::table('employees')->where('id', $emp)->update(['password' => Hash::make('Test@12345'), 'password_changed_at' => now()->subDay(), 'token_version' => 1]);

// Bảng giá dùng để test (khác 1 = Bán lẻ)
// Bảng giá ERP nằm ở DB ERP (không có bảng cục bộ) -> dùng id khác 1 để phân biệt với "Bán lẻ".
$bangGiaTmdt = 3;
echo "Bảng giá test (khác Bán lẻ): $bangGiaTmdt\n";

$khachHang = DB::table('prospective_projects')->whereNotNull('customer_id')->value('customer_id');
echo "Khách hàng dùng cho fixture: $khachHang\n";

$now = now();
$duAnCha = DB::table('prospective_projects')->insertGetId([
    'name' => TAG . ' - Du an CHA', 'code' => TAG . '-CHA', 'company_id' => 1, 'main_sale_employee_id' => $emp, 'customer_id' => $khachHang,
    'is_parent_project' => 1, 'created_by' => $emp, 'updated_by' => $emp,
    'created_at' => $now, 'updated_at' => $now,
]);
$duAnCon = DB::table('prospective_projects')->insertGetId([
    'name' => TAG . ' - Du an CON', 'code' => TAG . '-CON', 'company_id' => 1,
    'parent_id' => $duAnCha, 'price_type_id' => null, 'main_sale_employee_id' => $emp, 'customer_id' => $khachHang, 'created_by' => $emp, 'updated_by' => $emp,
    'created_at' => $now, 'updated_at' => $now,
]);
echo "Dự án cha=$duAnCha | dự án con=$duAnCon (price_type_id = null)\n";

function taoBaoGia($projectId, $payloadThem, $emp) {
    return api('POST', '/api/v1/assign/quotations', array_merge([
        'project_id' => $projectId,
        'type' => Quotation::TYPE_SELF_BUILT,
    ], $payloadThem), $emp);
}

// ============ TC1: báo giá dự án CHA chọn bảng giá TMĐT ============
echo "\nTC1 — Tạo báo giá nháp cho dự án CHA với bảng giá khác Bán lẻ\n";
list($code, $body) = taoBaoGia($duAnCha, ['price_type_id' => $bangGiaTmdt], $emp);
$qCha = $body['data']['id'] ?? null;
if ($qCha) DB::table('quotations')->where('id', $qCha)->update(['code' => TAG . '-CHA-Q']);
$ptCha = DB::table('quotations')->where('id', $qCha)->value('price_type_id');
ok($code === 200 && $qCha, 'Tạo được báo giá dự án cha', "code=$code");
ok((int) $ptCha === (int) $bangGiaTmdt, 'Báo giá cha lưu đúng bảng giá người dùng chọn', "chọn=$bangGiaTmdt | lưu=$ptCha");

// ============ TC2: báo giá dự án CON kế thừa bảng giá của báo giá cha (ca QA) ============
echo "\nTC2 — Tạo báo giá cho dự án CON (dự án con chưa khai bảng giá)\n";
list($code2, $body2) = taoBaoGia($duAnCon, ['price_type_id' => 1], $emp);   // FE gửi gì cũng bị ghi đè
$qCon = $body2['data']['id'] ?? null;
if ($qCon) DB::table('quotations')->where('id', $qCon)->update(['code' => TAG . '-CON-Q']);
$ptCon = DB::table('quotations')->where('id', $qCon)->value('price_type_id');
ok($code2 === 200 && $qCon, 'Tạo được báo giá dự án con', "code=$code2");
ok((int) $ptCon === (int) $bangGiaTmdt, 'KẾ THỪA bảng giá từ báo giá của dự án cha', "cha=$bangGiaTmdt | con=$ptCon");

// ============ TC3: dự án con ĐÃ khai bảng giá riêng -> ưu tiên của dự án ============
echo "\nTC3 — Dự án con đã có price_type_id riêng thì ưu tiên giá trị đó\n";
DB::table('prospective_projects')->where('id', $duAnCon)->update(['price_type_id' => 1]);
list($code3, $body3) = taoBaoGia($duAnCon, ['price_type_id' => $bangGiaTmdt], $emp);
$qCon3 = $body3['data']['id'] ?? null;
if ($qCon3) DB::table('quotations')->where('id', $qCon3)->update(['code' => TAG . '-CON-Q3']);
$ptCon3 = DB::table('quotations')->where('id', $qCon3)->value('price_type_id');
ok((int) $ptCon3 === 1, 'Lấy theo prospective_projects.price_type_id của dự án con', "kỳ vọng=1 | thực tế=$ptCon3");
DB::table('prospective_projects')->where('id', $duAnCon)->update(['price_type_id' => null]);

// ============ TC4: dự án cha CHƯA có báo giá nào -> về mặc định Bán lẻ ============
echo "\nTC4 — Dự án cha chưa có báo giá nào -> báo giá con về mặc định Bán lẻ (1)\n";
$chaTrong = DB::table('prospective_projects')->insertGetId([
    'name' => TAG . ' - Cha rong', 'code' => TAG . '-CHA2', 'company_id' => 1, 'is_parent_project' => 1, 'main_sale_employee_id' => $emp,
    'created_by' => $emp, 'updated_by' => $emp, 'created_at' => $now, 'updated_at' => $now,
]);
$conTrong = DB::table('prospective_projects')->insertGetId([
    'name' => TAG . ' - Con rong', 'code' => TAG . '-CON2', 'company_id' => 1, 'parent_id' => $chaTrong, 'main_sale_employee_id' => $emp, 'customer_id' => $khachHang,
    'created_by' => $emp, 'updated_by' => $emp, 'created_at' => $now, 'updated_at' => $now,
]);
list($code4, $body4) = taoBaoGia($conTrong, ['price_type_id' => $bangGiaTmdt], $emp);
$qCon4 = $body4['data']['id'] ?? null;
if ($qCon4) DB::table('quotations')->where('id', $qCon4)->update(['code' => TAG . '-CON-Q4']);
$ptCon4 = DB::table('quotations')->where('id', $qCon4)->value('price_type_id');
ok((int) $ptCon4 === 1, 'Không có gì để kế thừa -> Bán lẻ (1)', "thực tế=$ptCon4");

// ============ TC5: dự án ĐỘC LẬP vẫn lấy đúng bảng giá người dùng chọn ============
echo "\nTC5 — Dự án độc lập (không có cha) chọn bảng giá bất kỳ\n";
$doclap = DB::table('prospective_projects')->insertGetId([
    'name' => TAG . ' - Doc lap', 'code' => TAG . '-DL', 'company_id' => 1, 'main_sale_employee_id' => $emp, 'customer_id' => $khachHang,
    'created_by' => $emp, 'updated_by' => $emp, 'created_at' => $now, 'updated_at' => $now,
]);
list($code5, $body5) = taoBaoGia($doclap, ['price_type_id' => $bangGiaTmdt], $emp);
$qDl = $body5['data']['id'] ?? null;
if ($qDl) DB::table('quotations')->where('id', $qDl)->update(['code' => TAG . '-DL-Q']);
$ptDl = DB::table('quotations')->where('id', $qDl)->value('price_type_id');
ok((int) $ptDl === (int) $bangGiaTmdt, 'Giữ nguyên lựa chọn của người dùng', "chọn=$bangGiaTmdt | lưu=$ptDl");

// ============ TC6: báo giá cha MỚI NHẤT quyết định (đổi bảng giá ở báo giá cha thứ 2) ============
echo "\nTC6 — Dự án cha có 2 báo giá, báo giá MỚI NHẤT quyết định bảng giá kế thừa\n";
list($c6, $b6) = taoBaoGia($duAnCha, ['price_type_id' => 1], $emp);
$qCha2 = $b6['data']['id'] ?? null;
if ($qCha2) DB::table('quotations')->where('id', $qCha2)->update(['code' => TAG . '-CHA-Q2']);
list($c7, $b7) = taoBaoGia($duAnCon, ['price_type_id' => $bangGiaTmdt], $emp);
$qCon6 = $b7['data']['id'] ?? null;
if ($qCon6) DB::table('quotations')->where('id', $qCon6)->update(['code' => TAG . '-CON-Q6']);
$ptCon6 = DB::table('quotations')->where('id', $qCon6)->value('price_type_id');
ok((int) $ptCon6 === 1, 'Lấy theo báo giá cha mới nhất (bảng giá 1)', "thực tế=$ptCon6");

echo "\n==============================\nPASS: $pass | FAIL: $fail\n";
foreach ($msgs as $m) echo " - $m\n";
cleanup();
$left = DB::table('quotations')->where('code', 'like', TAG . '%')->count()
    + DB::table('prospective_projects')->where('name', 'like', TAG . '%')->count();
echo "Đã dọn fixture, còn sót: $left\n";
exit($fail > 0 ? 1 : 0);
