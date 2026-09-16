<?php

namespace App\Console\Commands\MasterData;

use Illuminate\Console\Command;
use Modules\MasterData\Services\RegulationConfigService;

class ApplyScheduledRegulationsCommand extends Command
{
    protected $signature = 'regulation-config:apply-scheduled';
    protected $description = 'Áp dụng các phiên bản quy chế/cấu hình đã hẹn tới hạn (effective_date <= hôm nay)';

    public function handle(RegulationConfigService $service): int
    {
        $applied = $service->applyDueCongnoVersions();
        $this->info("Đã áp dụng {$applied} phiên bản Công nợ tới hạn.");
        return 0;
    }
}
