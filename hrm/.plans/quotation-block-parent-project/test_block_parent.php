<?php
/**
 * Chặn lập BÁO GIÁ THƯỜNG trên dự án CHA.
 *
 * Dự án cha không tự lập báo giá (URD du-an-cha-con): báo giá của nó là BÁO GIÁ TỔNG
 * (is_summary = 1) gộp từ báo giá đã duyệt của dự án con, qua luồng assign/summary-quotations.
 * Trước khi sửa: dropdown màn /assign/quotations/create liệt kê cả dự án cha và BE tạo được thật.
 *
 * Bộ test phủ 2 chiều: chặn đúng chỗ cần chặn, và KHÔNG phá các luồng còn lại.
 */
$root = '/Users/manhcuong/Desktop/dns/HRM/worktrees/tpe-api';
require $root . '/vendor/autoload.php';
$app = require $root . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Http\Kernel::class);
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

$pass = 0; $fail = 0; $msgs = [];
function ok($cond, $name, $extra = '') {
    global $pass, $fail, $msgs;
    if ($cond) { $pass++; echo "  ✓ $name\n"; }
    else { $fail++; $msgs[] = $name . ($extra ? " | $extra" : ''); echo "  ✗ $name" . ($extra ? " | $extra" : '') . "\n"; }
}
function api($m, $uri, $payload, $e) {
    global $kernel, $app;
    $u = \App\Models\TpEmployee::find($e);
    $t = \Tymon\JWTAuth\Facades\JWTAuth::fromUser($u);
    \Illuminate\Support\Facades\Auth::forgetGuards();
    $r = Request::create($uri, $m, [], [], [], [
        'CONTENT_TYPE' => 'application/json', 'HTTP_ACCEPT' => 'application/json',
        'HTTP_AUTHORIZATION' => 'Bearer ' . $t,
    ], json_encode($payload));
    $app->instance('request', $r);
    \Tymon\JWTAuth\Facades\JWTAuth::setRequest($r);
    \Tymon\JWTAuth\Facades\JWTAuth::unsetToken();
    \Illuminate\Support\Facades\Auth::guard('api')->setUser($u);
    $res = $kernel->handle($r);
    \Illuminate\Support\Facades\Auth::forgetGuards();
    return [$res->getStatusCode(), json_decode($res->getContent(), true)];
}
$created = [];
function dropQuotation($id) {
    if (!$id) return;
    DB::table('quotation_product_prices')->where('quotation_id', $id)->delete();
    DB::table('quotation_service_items')->where('quotation_id', $id)->delete();
    DB::table('quotations')->where('id', $id)->delete();
}

$SALE = 13;                       // NV KD phụ trách dự án 356 / 357
$OTHER = 34;                      // tài khoản khác quyền
$PARENT = 356;                    // [TEST] Dự án CHA
$CHILD = 357;                     // [TEST] Dự án CON
// Dự án ĐỘC LẬP của cùng NV KD (để chắc luồng cũ không bị chặn oan)
$INDEP = DB::table('prospective_projects')
    ->where('main_sale_employee_id', $SALE)
    ->where(function ($q) { $q->where('is_parent_project', 0)->orWhereNull('is_parent_project'); })
    ->whereNull('parent_id')->where('status', '!=', 1)
    ->orderByDesc('id')->value('id');
echo "Dự án: cha=$PARENT | con=$CHILD | độc lập=$INDEP\n";

// ===== TC1: dropdown màn báo giá KHÔNG còn dự án cha =====
echo "\nTC1 — Dropdown Dự án ở màn lập báo giá (for_quotation=1)\n";
list($c, $b) = api('GET', '/api/v1/assign/prospective-projects/getAll?per_page=50&main_sale_mine=1&for_quotation=1', [], $SALE);
$rows = $b['data'] ?? [];
$parents = array_filter($rows, fn ($r) => !empty($r['is_parent_project']));
ok($c === 200, 'API trả 200', "code=$c");
ok(count($rows) > 0, 'Vẫn trả về dự án (không lọc sạch)', 'số dòng=' . count($rows));
ok(count($parents) === 0, 'KHÔNG còn dự án CHA trong dropdown', 'còn ' . count($parents));
ok(in_array($CHILD, array_column($rows, 'id')), 'Dự án CON vẫn chọn được');

// ===== TC2: không gửi cờ -> giữ nguyên hành vi cũ (không phá màn khác) =====
echo "\nTC2 — Các màn khác dùng chung getAll KHÔNG bị ảnh hưởng\n";
list($c2, $b2) = api('GET', '/api/v1/assign/prospective-projects/getAll?per_page=50&main_sale_mine=1', [], $SALE);
$parents2 = array_filter($b2['data'] ?? [], fn ($r) => !empty($r['is_parent_project']));
ok(count($parents2) > 0, 'Không gửi for_quotation thì dự án cha vẫn trả về như cũ', 'số cha=' . count($parents2));

// ===== TC3: TẠO báo giá trên dự án CHA -> bị chặn =====
echo "\nTC3 — POST /assign/quotations trên dự án CHA\n";
list($c3, $b3) = api('POST', '/api/v1/assign/quotations', ['project_id' => $PARENT, 'type' => 1, 'price_type_id' => 6], $SALE);
$err3 = $b3['errors']['project_id'] ?? ($b3['message'] ?? '');
$err3 = is_array($err3) ? implode(' ', $err3) : $err3;
ok($c3 === 422, 'Bị chặn với HTTP 422', "code=$c3");
ok(strpos($err3, 'Dự án cha không lập báo giá riêng') !== false, 'Thông báo nói rõ lý do + lối đi đúng', $err3);
ok(DB::table('quotations')->where('project_id', $PARENT)->where('is_summary', 0)->count() === 0, 'Không có bản ghi nào lọt xuống DB');
if (!empty($b3['data']['id'])) { $created[] = $b3['data']['id']; }

// ===== TC4: tài khoản KHÁC cũng bị chặn (không phải lỗ hổng theo quyền) =====
echo "\nTC4 — Tài khoản khác (id $OTHER) gọi thẳng API\n";
list($c4, $b4) = api('POST', '/api/v1/assign/quotations', ['project_id' => $PARENT, 'type' => 1, 'price_type_id' => 6], $OTHER);
ok($c4 === 422, 'Cũng bị chặn 422', "code=$c4");

// ===== TC5: dự án CON vẫn tạo báo giá bình thường =====
echo "\nTC5 — Dự án CON vẫn lập được báo giá (luồng đúng)\n";
list($c5, $b5) = api('POST', '/api/v1/assign/quotations', ['project_id' => $CHILD, 'type' => 1, 'price_type_id' => 6], $SALE);
$qChild = $b5['data']['id'] ?? null;
if ($qChild) $created[] = $qChild;
ok($c5 === 200 && $qChild, 'Tạo được báo giá cho dự án con', "code=$c5 | " . json_encode($b5['message'] ?? $b5['errors'] ?? '', JSON_UNESCAPED_UNICODE));
ok((int) DB::table('quotations')->where('id', $qChild)->value('price_type_id') === 6, 'Bảng giá kế thừa = 6 (TMĐT online)');

// ===== TC6: dự án ĐỘC LẬP vẫn tạo báo giá bình thường =====
echo "\nTC6 — Dự án độc lập vẫn lập được báo giá\n";
list($c6, $b6) = api('POST', '/api/v1/assign/quotations', ['project_id' => $INDEP, 'type' => 1, 'price_type_id' => 1], $SALE);
$qIndep = $b6['data']['id'] ?? null;
if ($qIndep) $created[] = $qIndep;
ok($c6 === 200 && $qIndep, 'Tạo được báo giá cho dự án độc lập', "code=$c6 | " . json_encode($b6['message'] ?? $b6['errors'] ?? '', JSON_UNESCAPED_UNICODE));

// ===== TC7: ĐỔI dự án của báo giá đã có sang dự án CHA -> bị chặn =====
echo "\nTC7 — PUT đổi Dự án của báo giá sang dự án CHA (luồng báo giá sao chép)\n";
list($c7, $b7) = api('PUT', "/api/v1/assign/quotations/$qIndep", ['project_id' => $PARENT], $SALE);
$err7 = $b7['errors']['project_id'] ?? ($b7['message'] ?? '');
$err7 = is_array($err7) ? implode(' ', $err7) : $err7;
ok($c7 === 422, 'Bị chặn 422', "code=$c7");
ok(strpos($err7, 'Dự án cha không lập báo giá riêng') !== false, 'Cùng một thông báo với lúc tạo', $err7);
ok((int) DB::table('quotations')->where('id', $qIndep)->value('project_id') === (int) $INDEP, 'Dự án của báo giá giữ nguyên, không bị đổi');

// ===== TC8: PUT bình thường (không đụng project_id) vẫn chạy =====
echo "\nTC8 — PUT sửa báo giá không đổi dự án\n";
list($c8, $b8) = api('PUT', "/api/v1/assign/quotations/$qIndep", ['note' => 'ghi chu test chan du an cha'], $SALE);
ok($c8 === 200, 'Sửa bình thường vẫn 200', "code=$c8 | " . json_encode($b8['errors'] ?? '', JSON_UNESCAPED_UNICODE));
ok(DB::table('quotations')->where('id', $qIndep)->value('note') === 'ghi chu test chan du an cha', 'Ghi chú đã lưu');

// ===== TC9: đổi dự án sang dự án CON -> vẫn cho =====
echo "\nTC9 — PUT đổi Dự án sang dự án CON\n";
list($c9, $b9) = api('PUT', "/api/v1/assign/quotations/$qIndep", ['project_id' => $CHILD], $SALE);
ok($c9 === 200, 'Cho đổi sang dự án con', "code=$c9 | " . json_encode($b9['errors'] ?? '', JSON_UNESCAPED_UNICODE));

// ===== TC10: BÁO GIÁ TỔNG của dự án cha KHÔNG bị vạ lây =====
echo "\nTC10 — Luồng Báo giá tổng của dự án cha không bị chặn nhầm\n";
list($c10, $b10) = api('GET', "/api/v1/assign/prospective-projects/$PARENT/summary-quotations", [], $SALE);
ok($c10 === 200, 'Vẫn vào được tab Báo giá tổng của dự án cha', "code=$c10");
list($c11, $b11) = api('GET', "/api/v1/assign/prospective-projects/$PARENT/selectable-quotations", [], $SALE);
ok($c11 === 200, 'Vẫn lấy được danh sách báo giá nguồn để gộp', "code=$c11");

// ===== TC11: luồng Yêu cầu làm giải pháp giữ nguyên bộ lọc cũ =====
echo "\nTC11 — Dropdown Yêu cầu làm giải pháp giữ nguyên (không bị sửa lây)\n";
list($c12, $b12) = api('GET', '/api/v1/assign/prospective-projects/getAll?per_page=50&forRequestSolution=1', [], $SALE);
$p12 = array_filter($b12['data'] ?? [], fn ($r) => !empty($r['is_parent_project']));
ok($c12 === 200 && count($p12) === 0, 'Vẫn không có dự án cha', "code=$c12 | cha=" . count($p12));

echo "\n==============================\nPASS: $pass | FAIL: $fail\n";
foreach ($msgs as $m) echo " - $m\n";
foreach ($created as $id) dropQuotation($id);
$left = DB::table('quotations')->whereIn('id', $created)->count();
echo "Đã dọn " . count($created) . " báo giá thử nghiệm, còn sót: $left\n";
exit($fail > 0 ? 1 : 0);
