<?php
/**
 * Tạo DATA TEST cho cột "Công tính lương (13)" — Redmine #11457
 *
 * Chạy:
 *   cd hrm-api
 *   php artisan tinker --execute="\$MA_NV='10610024'; \$THANG='2026-08'; require '/Users/manhcuong/Desktop/dns/HRM/.plans/cong-tinh-luong-khong-vdm/seed-test-data.php';"
 *
 * Script CHỈ đụng vào 1 nhân viên + 1 tháng bạn chỉ định (xoá sạch rồi tạo lại),
 * không ảnh hưởng nhân viên khác hay tháng khác.
 */

use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Entities\TimesheetSummary;
use Modules\Timesheet\Entities\OvertimeDetail;
use Carbon\Carbon;

$code  = $MA_NV  ?? '10610024';
$month = $THANG  ?? '2026-08';

$emp = EmployeeInfo::where('code', $code)->first();
if (!$emp) { echo "KHÔNG tìm thấy nhân viên mã $code\n"; return; }

$start = Carbon::parse($month . '-01')->startOfMonth();
$end   = (clone $start)->endOfMonth();

// 1. Xoá sạch dữ liệu cũ của ĐÚNG nhân viên này trong ĐÚNG tháng này
$oldIds = TimesheetSummary::where('employee_info_id', $emp->id)
    ->whereBetween('day', [$start->toDateString(), $end->toDateString()])->pluck('id');
OvertimeDetail::whereIn('timesheet_summary_id', $oldIds)->delete();
TimesheetSummary::whereIn('id', $oldIds)->delete();

// ⚠️ 'type_day' và 'ca_dem' KHÔNG nằm trong $fillable của model TimesheetSummary
//    -> create() bỏ qua im lặng, phải ghi thẳng bằng query builder sau khi tạo.
$mk = function ($date, $attrs = []) use ($emp) {
    $attrs = array_merge(['type_day' => 1], $attrs);   // 1 = ngày thường, 2 = cuối tuần, 3 = ngày lễ
    $ngoaiFillable = array_intersect_key($attrs, array_flip(['type_day', 'ca_dem']));
    $attrs = array_diff_key($attrs, $ngoaiFillable);
    $ts = TimesheetSummary::create(array_merge([
        'employee_info_id' => $emp->id,
        'day'              => $date,
        'labour_day'       => 1,
        'labour_hour'      => 8,
        'overtime_hour'    => 0,
        'minutes_late'     => 0,
        'minutes_early'    => 0,
        'punishment_rule'  => 0,
        'work_day_phep'    => 0,
        'work_day_che_do'  => 0,
        'data_attendance'  => 1,
    ], $attrs));
    if ($ngoaiFillable) {
        TimesheetSummary::where('id', $ts->id)->update($ngoaiFillable);
        $ts->refresh();
    }
    return $ts;
};

$ngayThuong = [];
$d = clone $start;
while ($d <= $end) {                       // bỏ T7/CN cho giống thực tế
    if (!in_array($d->dayOfWeek, [0, 6])) $ngayThuong[] = $d->toDateString();
    $d->addDay();
}

$i = 0;
$log = [];

// --- CA 1: các ngày công hành chính bình thường (chừa lại 8 ngày cho 5 ca dưới)
$soNgayHC = count($ngayThuong) - 8;
if ($soNgayHC < 1) { echo "Tháng $month quá ít ngày thường để tạo đủ ca test\n"; return; }
for (; $i < $soNgayHC; $i++) { $mk($ngayThuong[$i]); }
$log[] = "$soNgayHC ngày công hành chính (labour_day = 1)";

// --- CA 2: 2 ngày NGHỈ PHÉP  -> vào cột (5) Phép, KHÔNG vào công hành chính (1)
for ($n = 0; $n < 2; $n++, $i++) { $mk($ngayThuong[$i], ['work_day_phep' => 1]); }
$log[] = "2 ngày nghỉ phép  -> cột (5)";

// --- CA 3: 1 ngày LỄ hưởng lương -> cột (6)
$mk($ngayThuong[$i++], ['type_day' => 3]);
$log[] = "1 ngày lễ hưởng lương -> cột (6)";

// --- CA 4: 1 ngày NGHỈ CHẾ ĐỘ hưởng nguyên lương -> cột (7)
$mk($ngayThuong[$i++], ['work_day_che_do' => 1]);
$log[] = "1 ngày nghỉ chế độ -> cột (7)";

// --- CA 5: 1 ngày ĐI MUỘN 30 phút + 1 ngày VỀ SỚM 24 phút -> cột (9)(10)(11)
// LƯU Ý: bảng CHI TIẾT tính cột (11) từ SỐ PHÚT / (60*8);
//        bảng TỔNG HỢP tính cột (11) từ cột punishment_rule.
//        Phải set cả hai cho khớp nhau, nếu không 2 màn ra số lệch.
$mk($ngayThuong[$i++], ['minutes_late'  => 30, 'punishment_rule' => round(30 / 480, 2)]);
$mk($ngayThuong[$i++], ['minutes_early' => 24, 'punishment_rule' => round(24 / 480, 2)]);
$log[] = "1 ngày đi muộn 30' + 1 ngày về sớm 24' -> cột (9)(10)(11)";

// --- CA 6: 2 ngày CÓ LÀM THÊM (vượt định mức) -> cột VĐM + (3), KHÔNG được vào cột (13)
foreach ([['1.50', 4], ['2.00', 3]] as [$ratio, $gio]) {
    $ts = $mk($ngayThuong[$i++], ['overtime_hour' => $gio]);
    OvertimeDetail::create([
        'timesheet_summary_id'  => $ts->id,
        'ratio'                 => $ratio,
        'hour'                  => $gio,
        'hour_after_converting' => $gio * floatval($ratio),
        'start_at'              => $ts->day . ' 18:00:00',
        'end_at'                => $ts->day . ' 22:00:00',
    ]);
}
$log[] = "2 ngày làm thêm (x1.5 = 4h, x2 = 3h) -> VĐM, KHÔNG vào cột (13)";

// ================= Tính tay giá trị kỳ vọng =================
$rows      = TimesheetSummary::where('employee_info_id', $emp->id)
    ->whereBetween('day', [$start->toDateString(), $end->toDateString()])->get();
$tongLabour = $rows->sum('labour_day');
$phep       = $rows->sum('work_day_phep');
$cheDo      = $rows->sum('work_day_che_do');
$le         = $rows->filter(fn($r) => (int) $r->type_day === 3)->sum('labour_day');
$hanhChinh  = $tongLabour - $phep - $cheDo - $le;          // cột (1)
$nhl        = $phep + $le + $cheDo;                        // cột (8)
$phut       = $rows->sum('minutes_late') + $rows->sum('minutes_early');
$giamTru    = round($phut / 480, 2);                       // cột (11) ở màn CHI TIẾT
$vdm        = round(OvertimeDetail::whereIn('timesheet_summary_id', $rows->pluck('id'))
                    ->sum('hour_after_converting') / 8, 2); // cột (3)

echo "\n=== ĐÃ TẠO DATA TEST ===\n";
echo "Nhân viên : {$emp->fullname} ({$emp->code}) — employee_info_id = {$emp->id}\n";
echo "Kỳ        : {$start->format('d/m/Y')} - {$end->format('d/m/Y')}\n";
foreach ($log as $l) echo "  - $l\n";
echo "\n=== GIÁ TRỊ KỲ VỌNG TRÊN MÀN HÌNH ===\n";
printf("  (1)  Công hành chính        = %s\n", $hanhChinh);
printf("  (3)  Tổng VĐM quy đổi       = %s\n", $vdm);
printf("  (8)  Cộng NHL               = %s  (phép %s + lễ %s + chế độ %s)\n", $nhl, $phep, $le, $cheDo);
printf("  (11) Công cộng giảm trừ     = %s  (%s phút / 480)\n", $giamTru, $phut);
printf("  (13) CÔNG TÍNH LƯƠNG        = %s  <-- (1)+(8)-(11)\n", round($hanhChinh + $nhl - $giamTru, 2));
printf("  (14) Tổng công tính lương   = %s  <-- (13) + VĐM %s\n", round($hanhChinh + $nhl - $giamTru + $vdm, 2), $vdm);
echo "\nMở: http://127.0.0.1:3000/timesheet/timesheet_details  (chọn tháng {$start->format('m/Y')}, tìm '{$emp->code}')\n";
