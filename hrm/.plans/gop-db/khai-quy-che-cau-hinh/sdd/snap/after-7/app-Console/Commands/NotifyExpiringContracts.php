<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;

class NotifyExpiringContracts extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'contracts:notify-expiring';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Thông báo HĐLĐ sắp hết hạn (3 lần: còn 15, 10, 5 ngày)';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        app()->call('Modules\Decision\Services\DecisionLaborContract\DecisionLaborContractService@notifyExpiringContracts');
        $this->info('Thông báo hợp đồng sắp hết hạn đã được gửi.');
    }
}
