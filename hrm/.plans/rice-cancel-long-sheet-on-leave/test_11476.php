<?php
/**
 * Test luồng "huỷ cơm khi có đơn xin nghỉ" — Redmine #11476
 * Chạy: php test_11476.php   (từ thư mục worktree tpe-api)
 */
$root = '/Users/manhcuong/Desktop/dns/HRM/worktrees/tpe-api';
require $root . '/vendor/autoload.php';
$app = require $root . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Http\Kernel::class);
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

use Illuminate\Support\Facades\DB;
use Illuminate\Http\Request;

// ---------- cấu hình fixture ----------
const A_EMP = 25,  A_INFO = 13, A_RICE = 2;   // Nguyễn Thị Cần  — người ĐĂNG NHẬP (trưởng phòng)
const B_EMP = 27,  B_INFO = 15, B_RICE = 3;   // Chu Khương Duy  — nhân viên TRÊN ĐƠN
const TAG = 'TST11476';

$pass = 0; $fail = 0; $failMsgs = [];
function ok($cond, $name, $extra = '') {
    global $pass, $fail, $failMsgs;
    if ($cond) { $pass++; echo "  ✓ $name\n"; }
    else { $fail++; $failMsgs[] = $name . ($extra ? " | $extra" : ''); echo "  ✗ $name" . ($extra ? " | $extra" : '') . "\n"; }
}

function token($employeeId) {
    $user = \App\Models\TpEmployee::find($employeeId);
    return \Tymon\JWTAuth\Facades\JWTAuth::fromUser($user);
}

function call($method, $uri, $payload, $employeeId) {
    global $kernel, $app;
    $tok = token($employeeId);
    \Illuminate\Support\Facades\Auth::forgetGuards();
    $req = Request::create($uri, $method, [], [], [], [
        'CONTENT_TYPE' => 'application/json',
        'HTTP_ACCEPT' => 'application/json',
        'HTTP_AUTHORIZATION' => 'Bearer ' . $tok,
    ], json_encode($payload));
    $app->instance('request', $req);
    $res = $kernel->handle($req);
    return [$res->getStatusCode(), json_decode($res->getContent(), true)];
}

function regStatus($riceInfoId, $from, $to) {
    return DB::table('rice_registrations')
        ->where('rice_employee_info_id', $riceInfoId)
        ->whereBetween('date', [$from, $to])
        ->pluck('status_regular', 'date')->toArray();
}
function sheetStatus($id) {
    return DB::table('rice_sheet_registrations')->where('id', $id)->first();
}
function allAre($map, $value) {
    foreach ($map as $v) { if ((int)$v !== $value) return false; }
    return count($map) > 0;
}

// ---------- dọn fixture cũ ----------
function cleanup() {
    $ids = DB::table('rice_sheet_registrations')->where('code', 'like', TAG . '%')->pluck('id')->toArray();
    if ($ids) {
        DB::table('rice_registrations')->whereIn('sheet_id', $ids)->delete();
        DB::table('rice_sheet_registrations')->whereIn('id', $ids)->delete();
    }
    DB::table('rice_registrations')->whereBetween('date', ['2030-01-01', '2030-12-31'])->delete();
    DB::table('rice_menu_days')->whereBetween('date', ['2030-01-01', '2030-12-31'])->delete();
    DB::table('attendances')->where('attendance_reason', 'like', TAG . '%')->delete();
}
cleanup();

// ---------- tạo fixture ----------
$now = date('Y-m-d H:i:s');

// menu ngày (cần để hàm check nhìn thấy "có cơm")
$menuDays = [];
foreach (['2030-03-01', '2030-03-05', '2030-06-30', '2030-07-01', '2030-10-01', '2030-10-02'] as $d) {
    $menuDays[] = ['date' => $d, 'menu_regular_id' => 1, 'created_by' => A_EMP, 'updated_by' => A_EMP,
        'company_id' => 1, 'department_id' => 1, 'created_at' => $now, 'updated_at' => $now];
}
DB::table('rice_menu_days')->insert($menuDays);

function mkSheet($code, $riceBy, $type, $status, $start = null, $end = null, $guestTime = null) {
    $now = date('Y-m-d H:i:s');
    return DB::table('rice_sheet_registrations')->insertGetId([
        'code' => $code, 'register_rice_type' => $type, 'status' => $status,
        'register_rice_date_start' => $start, 'register_rice_date_end' => $end,
        'guest_register_rice_time' => $guestTime, 'guest_register_rice_guest_number' => $guestTime ? 2 : null,
        'rice_created_by' => $riceBy, 'rice_company_id' => 1, 'rice_department_id' => 1,
        'created_by' => 1, 'company_id' => 1, 'department_id' => 1,
        'created_at' => $now, 'updated_at' => $now,
    ]);
}

$S1 = mkSheet(TAG . '-S1-B-long', B_RICE, 1, 1, '2030-01-01', '2030-12-31');  // B: phiếu dài, bao trùm
$S2 = mkSheet(TAG . '-S2-A-long', A_RICE, 1, 1, '2030-01-01', '2030-12-31');  // A: phiếu riêng, không được đụng
$S3 = mkSheet(TAG . '-S3-B-short', B_RICE, 1, 1, '2030-03-01', '2030-03-10'); // B: phiếu nằm trọn trong đơn nghỉ
$S4 = mkSheet(TAG . '-S4-B-guest', B_RICE, 2, 1, null, null, '2030-03-05 10:00:00'); // phiếu khách
$S5 = mkSheet(TAG . '-S5-B-cancelled', B_RICE, 1, 2, '2030-05-01', '2030-05-10'); // đã huỷ sẵn

function mkRegs($riceInfoId, $sheetId, $from, $to) {
    $now = date('Y-m-d H:i:s');
    $rows = [];
    for ($d = strtotime($from); $d <= strtotime($to); $d = strtotime('+1 day', $d)) {
        $rows[] = ['rice_company_id' => 1, 'rice_department_id' => 1, 'rice_employee_info_id' => $riceInfoId,
            'type_sheet' => 1, 'sheet_id' => $sheetId, 'date' => date('Y-m-d', $d), 'status_regular' => 1,
            'rice_created_by' => $riceInfoId, 'created_at' => $now, 'updated_at' => $now];
    }
    DB::table('rice_registrations')->insert($rows);
}
mkRegs(B_RICE, $S1, '2030-06-25', '2030-07-05');
mkRegs(A_RICE, $S2, '2030-06-25', '2030-07-05');
mkRegs(B_RICE, $S3, '2030-03-01', '2030-03-10');

echo "Fixture: S1=$S1 S2=$S2 S3=$S3 S4=$S4 S5=$S5\n\n";

// ============ TC1: huỷ cho NGƯỜI KHÁC, đơn nghỉ NGẮN hơn phiếu dài ngày ============
echo "TC1 — A đăng nhập, huỷ cơm cho B (30/06–02/07/2030), phiếu B dài cả năm\n";
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-06-30', 'end_time' => '2030-07-02',
    'employees' => [['employee_info_id' => B_INFO]],
], A_EMP);
ok($code === 200, 'API trả 200', "code=$code " . json_encode($body));
ok(allAre(regStatus(B_RICE, '2030-06-30', '2030-07-02'), 2), 'B: 3 ngày trong đơn nghỉ -> Đã huỷ');
ok(allAre(regStatus(B_RICE, '2030-07-03', '2030-07-05'), 1), 'B: ngày ngoài đơn nghỉ giữ Đã đăng ký');
ok(allAre(regStatus(B_RICE, '2030-06-25', '2030-06-29'), 1), 'B: ngày trước đơn nghỉ giữ Đã đăng ký');
ok(allAre(regStatus(A_RICE, '2030-06-25', '2030-07-05'), 1), 'A (người đăng nhập) KHÔNG bị huỷ nhầm');
ok((int)sheetStatus($S1)->status === 1, 'Phiếu dài ngày của B vẫn "Đã đăng ký" (đơn nghỉ ngắn hơn)');
$his = DB::table('rice_registration_histories')->join('rice_registrations', 'rice_registrations.id', '=', 'rice_registration_histories.rice_registration_id')
    ->where('rice_registrations.rice_employee_info_id', B_RICE)
    ->whereBetween('rice_registrations.date', ['2030-06-30', '2030-07-02'])
    ->where('rice_registration_histories.status', 2)->count();
ok($his === 3, 'Ghi đủ 3 dòng lịch sử huỷ', "đếm được $his");

// ============ TC2: đơn nghỉ TRÙM TRỌN phiếu dài ngày ============
echo "\nTC2 — A huỷ cơm cho B khoảng 01/03–10/03/2030 (trùm trọn phiếu S3)\n";
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-03-01', 'end_time' => '2030-03-10',
    'employees' => [['employee_info_id' => B_INFO]],
], A_EMP);
ok($code === 200, 'API trả 200', "code=$code");
$s3 = sheetStatus($S3);
ok((int)$s3->status === 2, 'Phiếu S3 (nằm trọn trong đơn nghỉ) -> Đã huỷ', 'status=' . $s3->status);
ok(!empty($s3->cancel_reason), 'Có ghi lý do huỷ', (string)$s3->cancel_reason);
ok(allAre(regStatus(B_RICE, '2030-03-01', '2030-03-10'), 2), 'Toàn bộ 10 ngày cơm -> Đã huỷ');
ok((int)sheetStatus($S1)->status === 1, 'Phiếu S1 (dài hơn đơn nghỉ) vẫn giữ Đã đăng ký');
ok((int)sheetStatus($S2)->status === 1, 'Phiếu của A không bị đụng');
ok((int)sheetStatus($S4)->status === 1, 'Phiếu suất ăn KHÁCH không bị đụng');
ok((int)sheetStatus($S5)->status === 2, 'Phiếu đã huỷ sẵn giữ nguyên');

// ============ TC3: không truyền employees -> huỷ cho chính người đăng nhập ============
echo "\nTC3 — A huỷ cơm không truyền employees (luồng cũ: phiếu công tác/giao việc)\n";
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-06-25', 'end_time' => '2030-06-26',
], A_EMP);
ok($code === 200, 'API trả 200', "code=$code");
ok(allAre(regStatus(A_RICE, '2030-06-25', '2030-06-26'), 2), 'A tự huỷ cơm của mình');
ok(allAre(regStatus(A_RICE, '2030-06-27', '2030-07-05'), 1), 'Ngày ngoài khoảng của A giữ nguyên');
ok(allAre(regStatus(B_RICE, '2030-06-25', '2030-06-29'), 1), 'B không bị đụng');

// ============ TC4: employee_info_id không tồn tại ============
echo "\nTC4 — Truyền employee_info_id rác (99999999)\n";
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-07-03', 'end_time' => '2030-07-04',
    'employees' => [['employee_info_id' => 99999999]],
], A_EMP);
ok($code === 200, 'Không nổ 500', "code=$code " . json_encode($body));
ok(allAre(regStatus(B_RICE, '2030-07-03', '2030-07-05'), 1), 'Không huỷ nhầm của B');
ok(allAre(regStatus(A_RICE, '2030-07-03', '2030-07-05'), 1), 'Không huỷ nhầm của A (fallback người đăng nhập)');

// ============ TC5: nhân viên CHƯA có hồ sơ cơm ============
$noRice = DB::table('employee_infos')
    ->whereNotIn('id', function ($q) { $q->select('employee_info_id')->from('rice_employee_infos'); })
    ->value('id');
echo "\nTC5 — Truyền employee_info_id chưa có hồ sơ cơm (id=$noRice)\n";
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-07-03', 'end_time' => '2030-07-04',
    'employees' => [['employee_info_id' => $noRice]],
], A_EMP);
ok($code === 200, 'Không nổ 500 (bản cũ ->first()->id sẽ chết)', "code=$code " . json_encode($body));
ok(allAre(regStatus(A_RICE, '2030-07-03', '2030-07-05'), 1), 'Không rơi về huỷ cơm của người đăng nhập');

// ============ TC6: cảnh báo trùng lịch cơm khi lưu đơn nghỉ — đúng người ============
echo "\nTC6 — Cảnh báo \"đã đăng ký cơm\" khi gửi duyệt đơn nghỉ của B (A thao tác)\n";
$svc = $app->make(\Modules\Rice\Services\SheetRegistration\SheetRegistrationService::class);
\Illuminate\Support\Facades\Auth::setUser(\App\Models\TpEmployee::find(A_EMP));
// vùng dữ liệu sạch: CHỈ B có đăng ký cơm 01–02/10/2030, A không có
mkRegs(B_RICE, $S1, '2030-10-01', '2030-10-02');
$checkB = $svc->checkDuplicateTimeWithRiceRegistrationAttendance('2030-10-01', '2030-10-02', B_INFO);
$checkA = $svc->checkDuplicateTimeWithRiceRegistrationAttendance('2030-06-25', '2030-06-26', A_INFO);
$checkNull = $svc->checkDuplicateTimeWithRiceRegistrationAttendance('2030-10-01', '2030-10-02', null);
ok(!empty($checkB), 'Phát hiện B còn đăng ký cơm 01-02/10 (trước fix: soi nhầm người đăng nhập)');
ok(empty($checkA), 'A đã huỷ 25-26/06 nên không cảnh báo');
ok(empty($checkNull), 'Không truyền employee -> soi người đăng nhập (A, không có cơm 01-02/10) -> không cảnh báo');

// ============ TC7: AttendanceController lấy đúng nhân viên của đơn ============
echo "\nTC7 — AttendanceController@store: đơn đã có id thì soi cơm theo nhân viên trên đơn\n";
$attId = DB::table('attendances')->insertGetId([
    'attendance_reason' => TAG . ' nghỉ thử', 'application_date' => '2030-06-20 08:00:00',
    'attendance_start_at' => '2030-10-01 08:00:00', 'attendance_end_at' => '2030-10-02 17:30:00',
    'total_days' => 2, 'attendance_status' => 0, 'leave_type_id' => DB::table('leave_types')->value('id'),
    'employee_id' => B_INFO, 'company_id' => 1, 'department_id' => 1,
    'created_by' => B_EMP, 'updated_by' => B_EMP, 'created_at' => $now, 'updated_at' => $now,
]);
$attSvc = $app->make(\Modules\Timesheet\Services\AttendanceService::class);
$resolved = optional($attSvc->show($attId))->employee_id;
ok((int)$resolved === B_INFO, 'Đơn có id -> lấy employee_id của đơn (B)', "resolved=$resolved");
$checkFromController = $svc->checkDuplicateTimeWithRiceRegistrationAttendance('2030-10-01 08:00:00', '2030-10-02 17:30:00', $resolved);
$checkAsLoginUser = $svc->checkDuplicateTimeWithRiceRegistrationAttendance('2030-10-01 08:00:00', '2030-10-02 17:30:00', A_INFO);
ok(!empty($checkFromController), 'Với dữ liệu đó -> cảnh báo B đang đăng ký cơm (423)');
ok(empty($checkAsLoginUser), 'Bản CŨ (soi người đăng nhập A) sẽ không cảnh báo -> đúng là lỗi đã fix');

// ============ TC8: không huỷ ngược lại các ngày đã ăn / bếp huỷ ============
echo "\nTC8 — Không đụng vào ngày trạng thái khác (Đã ăn / Bếp huỷ)\n";
DB::table('rice_registrations')->where('rice_employee_info_id', B_RICE)->where('date', '2030-07-04')->update(['status_regular' => 3]);
DB::table('rice_registrations')->where('rice_employee_info_id', B_RICE)->where('date', '2030-07-05')->update(['status_regular' => 5]);
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-07-03', 'end_time' => '2030-07-05',
    'employees' => [['employee_info_id' => B_INFO]],
], A_EMP);
$map = regStatus(B_RICE, '2030-07-03', '2030-07-05');
ok($code === 200, 'API trả 200', "code=$code");
ok((int)$map['2030-07-03'] === 2, 'Ngày Đã đăng ký -> Đã huỷ');
ok((int)$map['2030-07-04'] === 3, 'Ngày "Đã ăn" giữ nguyên');
ok((int)$map['2030-07-05'] === 5, 'Ngày "Bếp huỷ" giữ nguyên');

// ============ TC9: huỷ nhiều nhân viên một lượt ============
echo "\nTC9 — Huỷ cho nhiều nhân viên cùng lúc (A + B), khoảng 08/07–09/07/2030\n";
mkRegs(B_RICE, $S1, '2030-07-08', '2030-07-09');
mkRegs(A_RICE, $S2, '2030-07-08', '2030-07-09');
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-07-08', 'end_time' => '2030-07-09',
    'employees' => [['employee_info_id' => A_INFO], ['employee_info_id' => B_INFO]],
], A_EMP);
ok($code === 200, 'API trả 200', "code=$code");
ok(allAre(regStatus(A_RICE, '2030-07-08', '2030-07-09'), 2), 'A được huỷ');
ok(allAre(regStatus(B_RICE, '2030-07-08', '2030-07-09'), 2), 'B được huỷ');
ok((int)sheetStatus($S1)->status === 1 && (int)sheetStatus($S2)->status === 1, 'Phiếu dài ngày 2 người vẫn hiệu lực');

// ============ TC10: khoảng huỷ trùm phiếu nhưng của NGƯỜI KHÁC -> không đụng ============
echo "\nTC10 — Khoảng huỷ trùm phiếu S3 nhưng chỉ huỷ cho A\n";
$S6 = mkSheet(TAG . '-S6-B-short2', B_RICE, 1, 1, '2030-09-01', '2030-09-05');
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-09-01', 'end_time' => '2030-09-05',
    'employees' => [['employee_info_id' => A_INFO]],
], A_EMP);
ok($code === 200, 'API trả 200', "code=$code");
ok((int)sheetStatus($S6)->status === 1, 'Phiếu của B không bị huỷ theo đơn nghỉ của A');

// ============ TC11: khoảng nghỉ CHƯA CÓ THỰC ĐƠN vẫn phải cảnh báo ============
echo "\nTC11 — Có đăng ký cơm nhưng nhà bếp chưa lập thực đơn (ca chị Huyền báo)\n";
// 20-21/12/2030: KHÔNG tạo rice_menu_days, chỉ có đăng ký cơm của B
mkRegs(B_RICE, $S1, '2030-12-20', '2030-12-21');
$menuCount = DB::table('rice_menu_days')->whereBetween('date', ['2030-12-20', '2030-12-21'])->whereNotNull('menu_regular_id')->count();
ok($menuCount === 0, 'Xác nhận khoảng này không có thực đơn nào', "menu=$menuCount");
$checkNoMenu = $svc->checkDuplicateTimeWithRiceRegistrationAttendance('2030-12-20', '2030-12-21', B_INFO);
ok(!empty($checkNoMenu), 'VẪN cảnh báo "đã đăng ký cơm" (trước fix: im lặng vì chưa có thực đơn)');
// và huỷ được bình thường
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-12-20', 'end_time' => '2030-12-21',
    'employees' => [['employee_info_id' => B_INFO]],
], A_EMP);
ok($code === 200 && allAre(regStatus(B_RICE, '2030-12-20', '2030-12-21'), 2), 'Huỷ cơm khoảng không có thực đơn vẫn chạy');

// ============ TC12: hàm cảnh báo dùng chung (giao việc / công tác / đề xuất) ============
echo "\nTC12 — checkDuplicateTimeWithRiceRegistration (phiếu giao việc/công tác)\n";
mkRegs(B_RICE, $S1, '2030-12-24', '2030-12-26');
mkRegs(A_RICE, $S2, '2030-12-24', '2030-12-26');
$menu = DB::table('rice_menu_days')->whereBetween('date', ['2030-12-24', '2030-12-26'])->whereNotNull('menu_regular_id')->count();
ok($menu === 0, 'Khoảng 24-26/12/2030 không có thực đơn', "menu=$menu");
$names = $svc->checkDuplicateTimeWithRiceRegistration('2030-12-24', '2030-12-26', [B_INFO]);
ok($names->count() === 1 && $names->first() === 'Chu Khương Duy', 'Chưa có thực đơn vẫn cảnh báo, trả đúng tên NV', $names->toJson());
$names2 = $svc->checkDuplicateTimeWithRiceRegistration('2030-12-24', '2030-12-26', [A_INFO, B_INFO]);
ok($names2->count() === 2, 'Nhiều nhân viên -> trả đủ tên, không trùng lặp', $names2->toJson());
$names3 = $svc->checkDuplicateTimeWithRiceRegistration('2030-12-24', '2030-12-26', [99999999]);
ok($names3->isEmpty(), 'employee rác -> rỗng, không nổ 500');
$names4 = $svc->checkDuplicateTimeWithRiceRegistration('2030-12-24', '2030-12-26', [$noRice]);
ok($names4->isEmpty(), 'NV chưa có hồ sơ cơm -> rỗng, không nổ 500');
$names5 = $svc->checkDuplicateTimeWithRiceRegistration('2030-12-24', '2030-12-26', []);
ok($names5->count() === 1 && $names5->first() === 'Nguyễn Thị Cần', 'Không truyền employees -> soi người đăng nhập (A)', $names5->toJson());

// ============ TC13: CHỐNG TÁI DIỄN — cảnh báo và huỷ phải nhìn CÙNG một tập ngày ============
echo "\nTC13 — Cảnh báo và huỷ luôn khớp nhau (mọi khoảng, có/không có thực đơn)\n";
$ranges = [
    ['2030-12-24', '2030-12-26', 'khoảng không có thực đơn'],
    ['2030-06-25', '2030-07-10', 'khoảng có thực đơn'],
    ['2030-12-24', '2030-12-24', 'đúng 1 ngày'],
    ['2031-05-01', '2031-05-10', 'khoảng không có đăng ký nào'],
];
foreach ($ranges as list($from, $to, $label)) {
    $riceIds = $svc->resolveRiceEmployeeInfoIds([B_INFO]);
    $seCanhBao = $svc->riceRegistrationsRegisteredInRange($riceIds, $from, $to)->count();
    $coCanhBao = !empty($svc->checkDuplicateTimeWithRiceRegistrationAttendance($from, $to, B_INFO));
    $coCanhBao2 = $svc->checkDuplicateTimeWithRiceRegistration($from, $to, [B_INFO])->isNotEmpty();
    $svc->rejectDuplicateTimeWithRiceRegistration($from, $to, [B_INFO]);
    $daHuy = DB::table('rice_registrations')->whereIn('rice_employee_info_id', $riceIds)
        ->whereBetween('date', [$from, $to])->where('status_regular', 2)->count();
    ok($coCanhBao === ($seCanhBao > 0) && $coCanhBao2 === ($seCanhBao > 0) && $daHuy >= $seCanhBao,
        "$label: cảnh báo ($seCanhBao ngày) khớp với số ngày huỷ được",
        "canhbao_don=" . var_export($coCanhBao, true) . " canhbao_giaoviec=" . var_export($coCanhBao2, true) . " dahuy=$daHuy");
}

// ============ TC14: nghỉ bắt đầu GIỮA phiếu, kết thúc SAU ngày đăng ký cơm cuối cùng ============
// Luật chốt 17/09/2026 (ca chị Trịnh Thị Lợi #11476): chỉ cần ngày kết thúc nghỉ >= ngày cuối phiếu
// thì phiếu phải về "Đã huỷ" — sau ngày bắt đầu nghỉ không còn ngày ăn nào nữa.
echo "\nTC14 — Nghỉ 15/08–30/09/2030, phiếu S6 của B là 01/08–31/08/2030\n";
$S6 = mkSheet(TAG . '-S6-B-giua', B_RICE, 1, 1, '2030-08-01', '2030-08-31');
$S7 = mkSheet(TAG . '-S7-B-sau', B_RICE, 1, 1, '2030-08-01', '2030-10-31'); // kết thúc SAU đơn nghỉ -> phải giữ
mkRegs(B_RICE, $S6, '2030-08-01', '2030-08-31');
list($code, $body) = call('POST', '/api/v1/rice/sheet-registration/reject-duplicate-time', [
    'start_time' => '2030-08-15', 'end_time' => '2030-09-30',
    'employees' => [['employee_info_id' => B_INFO]],
], A_EMP);
ok($code === 200, 'API trả 200', "code=$code " . json_encode($body));
$s6 = sheetStatus($S6);
ok((int)$s6->status === 2, 'Phiếu S6 -> Đã huỷ dù đơn nghỉ bắt đầu GIỮA phiếu', 'status=' . $s6->status);
ok(!empty($s6->cancel_reason), 'S6 có ghi lý do huỷ', (string)$s6->cancel_reason);
ok(allAre(regStatus(B_RICE, '2030-08-15', '2030-08-31'), 2), 'Ngày trong đơn nghỉ -> Đã huỷ');
ok(allAre(regStatus(B_RICE, '2030-08-01', '2030-08-14'), 1), 'Ngày TRƯỚC đơn nghỉ giữ nguyên, không bị đụng');
ok((int)sheetStatus($S7)->status === 1, 'Phiếu S7 (kết thúc sau đơn nghỉ) vẫn giữ Đã đăng ký');
ok((int)sheetStatus($S2)->status === 1, 'Phiếu của A vẫn không bị đụng');

// ---------- tổng kết ----------
echo "\n==============================\n";
echo "PASS: $pass | FAIL: $fail\n";
foreach ($failMsgs as $m) echo " - $m\n";

// ---------- dọn dẹp ----------
DB::table('rice_sheet_registrations')->where('code', 'like', TAG . '%')->delete();
cleanup();
$left = DB::table('rice_registrations')->whereBetween('date', ['2030-01-01', '2030-12-31'])->count()
    + DB::table('rice_sheet_registrations')->where('code', 'like', TAG . '%')->count()
    + DB::table('attendances')->where('attendance_reason', 'like', TAG . '%')->count();
echo "Đã dọn fixture, còn sót: $left\n";
exit($fail > 0 ? 1 : 0);
