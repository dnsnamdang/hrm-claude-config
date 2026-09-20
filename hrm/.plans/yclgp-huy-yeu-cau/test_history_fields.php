<?php
/**
 * Test lịch sử Yêu cầu làm giải pháp — MỖI CA ĐỔI ĐÚNG MỘT TRƯỜNG (skill entity-history §7a).
 * Mỗi ca bọc transaction rồi rollback nên KHÔNG để lại rác trong dữ liệu thật.
 */
$base = '/Users/manhcuong/Desktop/dns/HRM/worktrees/tpe-api';
require $base.'/vendor/autoload.php';
$app = require_once $base.'/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\RequestSolution;
use Modules\Assign\Entities\RequestSolutionHistory;
use Modules\Assign\Services\RequestSolutionHistoryService;
use Modules\Assign\Services\SystemLogService;

Illuminate\Support\Facades\Auth::setUser(\App\Models\TpEmployee::find(13));

$svc  = app(RequestSolutionHistoryService::class);
$logs = app(SystemLogService::class);
$rsId = (int) (getenv('RS_ID') ?: 24);

$ok = 0; $fail = 0;

function ca(string $ten, callable $doi, callable $kiemTra) {
    global $svc, $rsId, $ok, $fail;
    DB::beginTransaction();
    try {
        $rs = RequestSolution::find($rsId);
        $before = $svc->snapshot($rs);
        $doi($rs);
        $rs->save();
        $rs->refresh();
        $svc->log($rs, $before, $svc->snapshot($rs));
        $rows = RequestSolutionHistory::where('request_solution_id', $rsId)->orderByDesc('id')->get();
        $moTa = [];
        foreach ($rows as $r) {
            $new = json_decode($r->new_value, true) ?: [];
            $old = json_decode($r->old_value, true) ?: [];
            foreach ($new as $k => $v) {
                $cu = isset($old[$k]) ? $old[$k] : null;
                $moTa[] = $k.': '.(is_array($cu) ? json_encode($cu, JSON_UNESCAPED_UNICODE) : ($cu === null ? '(trống)' : $cu))
                    .' -> '.(is_array($v) ? json_encode($v, JSON_UNESCAPED_UNICODE) : ($v === null ? '(trống)' : $v));
            }
        }
        $ketQua = $kiemTra(count($rows), $moTa);
        printf("%-52s | %d dòng | %s | %s\n", $ten, count($rows), $ketQua ? 'ĐẠT ' : 'HỎNG', implode(' ~ ', $moTa) ?: '(không có thay đổi)');
        $ketQua ? $ok++ : $fail++;
    } finally {
        DB::rollBack();
    }
}

/** Ca đổi 1 trường: phải ra đúng 1 dòng log, và dòng đó nhắc đúng tên trường */
function caTruong(string $nhan, string $cot, $giaTri) {
    ca("Đổi $nhan", function ($rs) use ($cot, $giaTri) { $rs->$cot = $giaTri; },
        function ($soDong, $moTa) use ($nhan) {
            return $soDong === 1 && count($moTa) === 1 && strpos($moTa[0], $nhan) === 0;
        });
}

echo "=== A. TỪNG TRƯỜNG MỘT (mỗi ca đổi đúng 1 ô) ===\n";
caTruong('Tiêu đề', 'title', 'Tiêu đề thử nghiệm lịch sử');
caTruong('Giai đoạn dự án', 'project_phase_id', 6);
caTruong('Phòng tiếp nhận', 'receive_dept', 44);
caTruong('Nhóm ngành', 'scope_id', 10);
caTruong('Nhóm giải pháp', 'industry_id', 2);
caTruong('Ngày khách hàng cần giải pháp', 'customer_need_gp_date', '2026-12-01');
caTruong('Ngày khách hàng cần báo giá', 'customer_need_quote_date', '2026-12-05');
caTruong('Ngày nội bộ cần giải pháp', 'internal_need_gp_date', '2026-11-20');
caTruong('Ngày chốt giải pháp', 'close_solution_date', '2026-12-20');
caTruong('Ghi chú', 'note', 'Ghi chú thử nghiệm');
caTruong('Người phụ trách (PM)', 'pm_id', 13);
caTruong('Số điện thoại PM', 'pm_phone', '0900000001');
caTruong('Ghi chú PM', 'pm_note', 'PM ghi chú thử');
caTruong('Người tiếp nhận', 'receive_id', 13);
caTruong('Ngày gửi tiếp nhận', 'sent_date', '2026-09-10 08:00:00');
caTruong('Hạn tiếp nhận', 'need_receive_date', '2026-09-12 17:00:00');
caTruong('Dự án tiền khả thi', 'project_key', 274);

echo "\n=== B. CÁC CA ĐẶC BIỆT ===\n";
ca('Không sửa gì -> KHÔNG được ghi log', function ($rs) {}, function ($soDong) { return $soDong === 0; });
ca('Lưu lại y nguyên giá trị cũ -> KHÔNG ghi log', function ($rs) { $rs->title = $rs->title; $rs->note = $rs->note; }, function ($soDong) { return $soDong === 0; });
ca('Số dạng "5.00" vs 5 -> KHÔNG ghi log rác', function ($rs) { $rs->scope_id = (string) $rs->scope_id; }, function ($soDong) { return $soDong === 0; });
ca('Chuỗi rỗng vs null -> KHÔNG ghi log rác', function ($rs) { if ($rs->note === null) { $rs->note = ''; } }, function ($soDong) { return $soDong === 0; });
ca('Đổi 3 trường cùng lúc -> 1 dòng, 3 khoá', function ($rs) {
    $rs->title = 'Ba trường'; $rs->note = 'Ghi chú ba'; $rs->pm_phone = '0900000009';
}, function ($soDong, $moTa) { return $soDong === 1 && count($moTa) === 3; });
// Ca xoá trắng: phải CÓ giá trị trước khi chụp snapshot "trước", nếu không before/after đều null
DB::beginTransaction();
try {
    $rs = RequestSolution::find($rsId);
    $rs->note = 'Có giá trị để xoá'; $rs->save(); $rs->refresh();
    $before = $svc->snapshot($rs);
    $rs->note = null; $rs->save(); $rs->refresh();
    $svc->log($rs, $before, $svc->snapshot($rs));
    $row = RequestSolutionHistory::where('request_solution_id', $rsId)->orderByDesc('id')->first();
    $new = $row ? json_decode($row->new_value, true) : [];
    $old = $row ? json_decode($row->old_value, true) : [];
    $dat = $row && array_key_exists('Ghi chú', $new) && $new['Ghi chú'] === null && $old['Ghi chú'] === 'Có giá trị để xoá';
    printf("%-52s | %s | Ghi chú: %s -> %s\n", 'Xoá trắng 1 trường -> log "giá trị -> (trống)"', $dat ? 'ĐẠT ' : 'HỎNG',
        $old['Ghi chú'] ?? '(trống)', $new['Ghi chú'] === null ? '(trống)' : $new['Ghi chú']);
    $dat ? $ok++ : $fail++;
} finally { DB::rollBack(); }

echo "\n=== B2. TỆP ĐÍNH KÈM (bảng con dạng danh sách) ===\n";
DB::beginTransaction();
try {
    $rs = RequestSolution::find($rsId);
    $before = $svc->snapshot($rs);
    \App\Models\File::create(['table' => 'request_solutions', 'table_id' => $rsId, 'name' => 'Bao gia thu.pdf', 'file_name' => 'Bao gia thu.pdf', 'file_path' => '/uploads/bao-gia-thu.pdf', 'created_by' => 13]);
    $rs->refresh();
    $svc->log($rs, $before, $svc->snapshot($rs));
    $row = RequestSolutionHistory::where('request_solution_id', $rsId)->orderByDesc('id')->first();
    $chg = $row ? \Modules\Assign\Services\MeetingHistoryService::changesFrom(json_decode($row->old_value, true), json_decode($row->new_value, true)) : [];
    $dat = count($chg) === 1 && $chg[0]['field'] === 'Tệp đính kèm' && count($chg[0]['added']) === 1 && count($chg[0]['removed']) === 0;
    printf("%-52s | %s | thêm: %s\n", 'Thêm 1 tệp -> 1 dòng "đã thêm"', $dat ? 'ĐẠT ' : 'HỎNG', json_encode($chg[0]['added'] ?? [], JSON_UNESCAPED_UNICODE));
    $dat ? $ok++ : $fail++;
} finally { DB::rollBack(); }

DB::beginTransaction();
try {
    $f = \App\Models\File::create(['table' => 'request_solutions', 'table_id' => $rsId, 'name' => 'Tep se xoa.pdf', 'file_name' => 'Tep se xoa.pdf', 'file_path' => '/uploads/tep-se-xoa.pdf', 'created_by' => 13]);
    $rs = RequestSolution::find($rsId); $rs->refresh();
    $before = $svc->snapshot($rs);
    $f->delete();
    $rs->refresh();
    $svc->log($rs, $before, $svc->snapshot($rs));
    $row = RequestSolutionHistory::where('request_solution_id', $rsId)->orderByDesc('id')->first();
    $chg = $row ? \Modules\Assign\Services\MeetingHistoryService::changesFrom(json_decode($row->old_value, true), json_decode($row->new_value, true)) : [];
    $dat = count($chg) === 1 && $chg[0]['field'] === 'Tệp đính kèm' && count($chg[0]['removed']) === 1 && count($chg[0]['added']) === 0;
    printf("%-52s | %s | xoá: %s\n", 'Xoá 1 tệp -> 1 dòng "đã xoá"', $dat ? 'ĐẠT ' : 'HỎNG', json_encode($chg[0]['removed'] ?? [], JSON_UNESCAPED_UNICODE));
    $dat ? $ok++ : $fail++;
} finally { DB::rollBack(); }

echo "\n=== C. ĐỔI TRẠNG THÁI + LÝ DO (dòng RIÊNG theo skill §3a/§4.1) ===\n";
DB::beginTransaction();
try {
    $rs = RequestSolution::find($rsId);
    $st = (int) $rs->status;
    $rs->status = RequestSolution::STATUS_DA_HUY; $rs->save();
    $svc->logStatus($rs, $st, 'Khách hàng dừng dự án');
    $row = RequestSolutionHistory::where('request_solution_id', $rsId)->orderByDesc('id')->first();
    $new = json_decode($row->new_value, true); $old = json_decode($row->old_value, true);
    $dat = $row->action === 'change_status' && $row->note === 'Khách hàng dừng dự án' && isset($new['Trạng thái']);
    printf("%-52s | %s | %s -> %s | ghi chú: %s\n", 'Hủy: dòng change_status + lý do', $dat ? 'ĐẠT ' : 'HỎNG',
        $old['Trạng thái'], $new['Trạng thái'], $row->note);
    $dat ? $ok++ : $fail++;

    $rows = $logs->getLogs('request-solution', $rsId);
    $dat2 = count($rows) && $rows[0]['action_label'] === 'Đổi trạng thái' && $rows[0]['note'] === 'Khách hàng dừng dự án'
        && ($rows[0]['action_group'] ?? '') === 'status';
    printf("%-52s | %s | nhãn: %s | nhóm lọc: %s\n", 'Đọc qua API lịch sử (getLogs)', $dat2 ? 'ĐẠT ' : 'HỎNG',
        $rows[0]['action_label'], $rows[0]['action_group'] ?? '-');
    $dat2 ? $ok++ : $fail++;
} finally { DB::rollBack(); }

DB::beginTransaction();
try {
    $rs = RequestSolution::find($rsId);
    $st = (int) $rs->status;
    $svc->logStatus($rs, $st, null);
    $n = RequestSolutionHistory::where('request_solution_id', $rsId)->count();
    printf("%-52s | %s | số dòng: %d\n", 'Trạng thái KHÔNG đổi, không lý do -> không ghi', $n === 0 ? 'ĐẠT ' : 'HỎNG', $n);
    $n === 0 ? $ok++ : $fail++;
} finally { DB::rollBack(); }

echo "\n=== D. THỨ TỰ + DỮ LIỆU CŨ ===\n";
DB::beginTransaction();
try {
    $rs = RequestSolution::find($rsId);
    $b = $svc->snapshot($rs); $rs->title = 'Sửa lần 1'; $rs->save(); $svc->log($rs, $b, $svc->snapshot($rs->fresh()));
    $b = $svc->snapshot($rs->fresh()); $rs->refresh(); $rs->note = 'Sửa lần 2'; $rs->save(); $svc->log($rs, $b, $svc->snapshot($rs->fresh()));
    $rows = $logs->getLogs('request-solution', $rsId);
    $dat = count($rows) === 2 && $rows[0]['changes'][0]['field'] === 'Ghi chú';
    printf("%-52s | %s | thứ tự: %s\n", 'Sắp xếp MỚI -> CŨ', $dat ? 'ĐẠT ' : 'HỎNG',
        implode(' , ', array_map(function ($r) { return $r['changes'][0]['field']; }, $rows)));
    $dat ? $ok++ : $fail++;
} finally { DB::rollBack(); }

$rowsCu = $logs->getLogs('request-solution', $rsId);
$datCu = count($rowsCu) > 0;
printf("%-52s | %s | %d dòng (%s)\n", 'Phiếu CŨ chưa có log -> vẫn dựng từ cột audit', $datCu ? 'ĐẠT ' : 'HỎNG',
    count($rowsCu), implode(', ', array_map(function ($r) { return $r['action_label']; }, $rowsCu)));
$datCu ? $ok++ : $fail++;

printf("\n==== TỔNG: %d ĐẠT / %d HỎNG ====\n", $ok, $fail);
printf("Số dòng log còn sót lại sau test (phải = 0): %d\n", RequestSolutionHistory::count());
