<?php
/**
 * Test: công ty đã khoá (companies.status = 0) không được hiện ở ô chọn công ty (header).
 * Endpoint: GET /api/v1/users/auth/user-profile  -> data.company_roles
 */
$root = '/Users/manhcuong/Desktop/dns/HRM/worktrees/tpe-api';
require $root . '/vendor/autoload.php';
$app = require $root . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Http\Kernel::class);
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

use Illuminate\Support\Facades\DB;
use Illuminate\Http\Request;

$pass = 0; $fail = 0; $msgs = [];
function ok($cond, $name, $extra = '') {
    global $pass, $fail, $msgs;
    if ($cond) { $pass++; echo "  ✓ $name\n"; }
    else { $fail++; $msgs[] = $name . ($extra ? " | $extra" : ''); echo "  ✗ $name" . ($extra ? " | $extra" : '') . "\n"; }
}

function profile($employeeId) {
    global $kernel, $app;
    $tok = \Tymon\JWTAuth\Facades\JWTAuth::fromUser(\App\Models\TpEmployee::find($employeeId));
    \Illuminate\Support\Facades\Auth::forgetGuards();
    $req = Request::create('/api/v1/users/auth/user-profile', 'GET', [], [], [], [
        'HTTP_ACCEPT' => 'application/json',
        'HTTP_AUTHORIZATION' => 'Bearer ' . $tok,
    ]);
    $app->instance('request', $req);
    $res = $kernel->handle($req);
    $body = json_decode($res->getContent(), true);
    return [$res->getStatusCode(), $body['data']['company_roles'] ?? $body['company_roles'] ?? null];
}

// ---- tìm 1 nhân viên có role trải trên >= 2 công ty ----
$row = DB::table('company_roles')
    ->select('role_id', DB::raw('count(distinct company_id) c'))
    ->groupBy('role_id')->having('c', '>=', 2)->orderByDesc('c')->first();
$emp = DB::table('employee_has_roles')->where('role_id', $row->role_id)->value('employee_id');
$companyIds = DB::table('company_roles')->where('role_id', $row->role_id)->pluck('company_id')->unique()->values()->all();
echo "Nhân viên test: employees.id=$emp | role $row->role_id gắn " . count($companyIds) . " công ty: " . implode(',', $companyIds) . "\n";

$goc = DB::table('companies')->whereIn('id', $companyIds)->pluck('status', 'id')->toArray();
$khoa = $companyIds[0];                       // công ty sẽ bị khoá để test
$conLai = array_slice($companyIds, 1);

// ================= TC1: khoá 1 công ty -> biến mất khỏi danh sách =================
echo "\nTC1 — Khoá công ty id=$khoa\n";
DB::table('companies')->whereIn('id', $companyIds)->update(['status' => 1]);
list($code, $before) = profile($emp);
ok($code === 200, 'API user-profile trả 200', "code=$code");
$idsBefore = collect($before)->pluck('id')->map('intval')->all();
ok(in_array($khoa, $idsBefore), 'Khi chưa khoá: công ty có trong danh sách');

DB::table('companies')->where('id', $khoa)->update(['status' => 0]);
list($code, $after) = profile($emp);
$idsAfter = collect($after)->pluck('id')->map('intval')->all();
ok(!in_array($khoa, $idsAfter), 'Sau khi khoá: KHÔNG còn trong ô chọn công ty', json_encode($idsAfter));
ok(count($idsAfter) === count($idsBefore) - 1, 'Các công ty còn hoạt động vẫn nguyên', count($idsBefore) . ' -> ' . count($idsAfter));
foreach ($conLai as $c) {
    ok(in_array((int)$c, $idsAfter), "Công ty đang hoạt động id=$c vẫn hiện");
}

// ================= TC2: mở khoá lại -> hiện lại =================
echo "\nTC2 — Mở khoá lại công ty id=$khoa\n";
DB::table('companies')->where('id', $khoa)->update(['status' => 1]);
list($code, $back) = profile($emp);
ok(in_array($khoa, collect($back)->pluck('id')->map('intval')->all()), 'Mở khoá thì hiện lại ngay');

// ================= TC3: công ty ĐANG LÀM VIỆC bị khoá -> vẫn đăng nhập/xem được =================
echo "\nTC3 — Công ty user đang làm việc bị khoá (chốt: ẩn hẳn, không ngoại lệ)\n";
$current = optional(\App\Models\TpEmployee::find($emp))->current_company_role;
echo "  current_company_role = $current\n";
if (in_array((int)$current, array_map('intval', $companyIds))) {
    DB::table('companies')->where('id', $current)->update(['status' => 0]);
    list($code, $list) = profile($emp);
    $ids = collect($list)->pluck('id')->map('intval')->all();
    ok($code === 200, 'Vẫn vào được hệ thống, API không lỗi', "code=$code");
    ok(!in_array((int)$current, $ids), 'Công ty đang làm việc bị khoá cũng bị ẩn khỏi ô chọn', json_encode($ids));
    DB::table('companies')->where('id', $current)->update(['status' => 1]);
} else {
    echo "  (bỏ qua: công ty hiện tại không nằm trong nhóm test)\n";
}

// ================= TC4: toàn bộ công ty bị khoá -> danh sách rỗng, không lỗi =================
echo "\nTC4 — Khoá hết công ty của user\n";
DB::table('companies')->whereIn('id', $companyIds)->update(['status' => 0]);
list($code, $empty) = profile($emp);
ok($code === 200, 'Không nổ lỗi khi không còn công ty nào', "code=$code");
ok(count(collect($empty)->all()) === 0, 'Danh sách rỗng', json_encode($empty));

// ---- trả lại trạng thái gốc ----
foreach ($goc as $id => $st) {
    DB::table('companies')->where('id', $id)->update(['status' => $st]);
}
$restored = DB::table('companies')->whereIn('id', $companyIds)->pluck('status', 'id')->toArray();
ok($restored == $goc, 'Đã trả lại trạng thái công ty như ban đầu', json_encode($restored));

echo "\n==============================\nPASS: $pass | FAIL: $fail\n";
foreach ($msgs as $m) echo " - $m\n";
exit($fail > 0 ? 1 : 0);
