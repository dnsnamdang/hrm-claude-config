<?php
// Đối chiếu cong_viec_theo_nhan_vien (WorkByEmployee::rows) với báo cáo "Kế hoạch & kết quả làm việc theo nhân viên" cùng kỳ.
// Chạy trong wt-tpe-agent/hrm-api: php -d memory_limit=1G <đường dẫn>/work_parity.php [NV=13] [tu=2026-10-01] [den=2026-10-31]
require 'vendor/autoload.php'; $app = require 'bootstrap/app.php'; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
use Illuminate\Http\Request;
use Modules\Agent\Support\WorkByEmployee;
use Modules\Agent\Support\WorkByEmployeeScope;

$emp = (int) ($argv[1] ?? 13); $tu = $argv[2] ?? '2026-10-01'; $den = $argv[3] ?? '2026-10-31';
auth()->onceUsingId($emp); App\Support\RequestCache::flush(); App\Support\Permissions\PermissionChecker::flush();
$co = (int) auth()->user()->current_company_role;

$rep = new Modules\Assign\Services\Report\EmployeeWorkPerformanceService();
$data = $rep->getData(new Request(['company_id' => $co, 'period' => 'custom', 'start_date' => $tu, 'end_date' => $den, 'busy_only' => 0,
    // Agent tạm loại phiếu công tác (19/11) ⇒ so với báo cáo bỏ loại trip
    'types' => implode(',', array_values(WorkByEmployeeScope::LOAI))]));
$report = [];
$walk = function ($nodes) use (&$walk, &$report) {
    foreach ($nodes as $n) {
        if ($n['dim'] === 'emp') {
            $m = $n['metrics'];
            $report[(int) $n['id']] = [$m['total'], $m['done'], $m['doing'], $m['late'], $m['cancel']];
        }
        $walk($n['children'] ?? []);
    }
};
$walk($data['tree']);

$in = ['tu_ngay' => $tu, 'den_ngay' => $den];
$ids = WorkByEmployeeScope::employeeIds($in)['ids'];
$rows = WorkByEmployee::rows($ids, WorkByEmployeeScope::period($in), []);
$mine = [];
foreach ($rows as $r) {
    $mine[$r['nhan_vien_id']] = [$r['tong'], $r['hoan_thanh'], $r['dang_lam'], $r['qua_han'], $r['dung_huy']];
}

$diff = 0;
foreach (array_unique(array_merge(array_keys($report), array_keys($mine))) as $id) {
    $a = $report[$id] ?? null; $b = $mine[$id] ?? null;
    if ($a !== $b) {
        $diff++;
        echo "LỆCH NV $id: báo cáo ", json_encode($a), " · agent ", json_encode($b), "\n";
    }
}
echo "Kỳ $tu..$den · NV báo cáo ", count($report), " · NV agent ", count($mine), " · lệch $diff\n";
echo "[tong, hoan_thanh, dang_lam, qua_han, dung_huy]\n";
