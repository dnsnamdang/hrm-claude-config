<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Artisan;

class InitiateProject extends Command
{

    //B1: export structure database TPE
    //B2: import structure database TPE vào 1 database mới
    //B3: chạy command: php artisan initiate:project
    //B4: export data table migration migrations của TPE
    //B5: import data table migration migrations của TPE vào database mới
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'initiate:project {--email=namdangit@gmail.com} {--password=12345678}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Khởi tạo dự án...';

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $email = $this->option('email');
        $password = $this->option('password');

        $seeders = [
            'TruncateAllTableSeeder',
            'Modules\Timesheet\Database\Seeders\PermissionsTableSeeder',
            'Database\Seeders\DefaultAdminSeeder',
            'Database\Seeders\CreateDefaultDataToRewardModeTableSeeder',
        ];

        foreach ($seeders as $seeder) {
            $this->info("Seeding: $seeder");
            if ($seeder === 'Database\Seeders\DefaultAdminSeeder') {
                $this->callSeederWithArgs($seeder, $email, $password);
            } else {
                Artisan::call('db:seed', [
                    '--class' => $seeder,
                ]);
            }
            $this->info("Seeded: $seeder");
        }

        // // Chạy command vietnamzone:import sau khi các seeder đã hoàn thành
        // $this->info('Running vietnamzone:import...');
        // Artisan::call('vietnamzone:import');
        // $this->info('Completed vietnamzone:import.');
    }

    protected function callSeederWithArgs($seeder, $email, $password)
    {
        $seederInstance = new $seeder;
        $seederInstance->runWithArgs($email, $password);
    }
}
