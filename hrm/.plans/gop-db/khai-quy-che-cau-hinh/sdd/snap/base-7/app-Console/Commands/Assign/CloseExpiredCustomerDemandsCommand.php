<?php

namespace App\Console\Commands\Assign;

use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Modules\Assign\Entities\Meeting\MeetingInvestmentDemand;

/**
 * Dong cac NHU CAU khach hang khong chuyen doi duoc thanh du an TKT
 * (feature bao-cao-cskh-tiem-nang).
 *
 * Luat da chot voi user: toi ngay du kien trien khai (`expected_start_date`) ma nhu cau van
 * chua gan du an nao -> chuyen "Khong tiep tuc". Day KHONG phai thao tac tay, hoan toan do cron.
 *
 * 2 diem de sai neu viet lai:
 *  - `closed_at` = CHINH `expected_start_date`, KHONG phai ngay chay cron. Cron chay tre / chay bu
 *    thi nhu cau van roi dung vao ky ma no het han, bao cao khong bi lech.
 *  - `expected_start_date` rong -> KHONG BAO GIO tu dong (khong co moc de tinh), de nguyen
 *    "Dang theo doi" cho toi khi co du an hoac user sua lai bien ban.
 *
 * Idempotent: chi dung toi `status = DANG_THEO_DOI` nen chay lai bao nhieu lan cung ra 1 ket qua.
 */
class CloseExpiredCustomerDemandsCommand extends Command
{
    protected $signature = 'assign:close-expired-customer-demands {--dry-run : Chỉ liệt kê, không ghi DB}';

    protected $description = 'Đóng nhu cầu khách hàng quá ngày dự kiến triển khai mà chưa lập được dự án TKT';

    public function handle()
    {
        $today = Carbon::today();
        $dryRun = (bool) $this->option('dry-run');

        $demands = MeetingInvestmentDemand::query()
            ->where('status', MeetingInvestmentDemand::DANG_THEO_DOI)
            ->whereNotNull('expected_start_date')
            ->whereDate('expected_start_date', '<', $today)
            ->get();

        if ($demands->isEmpty()) {
            $this->info('Không có nhu cầu nào quá hạn theo dõi.');
            return 0;
        }

        foreach ($demands as $demand) {
            $closedAt = $demand->expected_start_date->format('Y-m-d');

            $this->line(sprintf(
                '#%d %s (meeting %d) — đóng với ngày %s',
                $demand->id,
                $demand->scope_name,
                $demand->meeting_id,
                $closedAt
            ));

            if ($dryRun) {
                continue;
            }

            // forceFill: 3 cột vòng đời do hệ thống quản lý, không đi qua payload của form nào
            $demand->forceFill([
                'status' => MeetingInvestmentDemand::KHONG_TIEP_TUC,
                'closed_at' => $closedAt,
            ])->save();
        }

        $message = sprintf(
            '%s %d nhu cầu quá hạn theo dõi.',
            $dryRun ? '[dry-run] Sẽ đóng' : 'Đã đóng',
            $demands->count()
        );

        $this->info($message);
        if (!$dryRun) {
            Log::info('[assign:close-expired-customer-demands] ' . $message);
        }

        return 0;
    }
}
