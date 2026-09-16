<?php

namespace App\Console\Commands;
use App\Models\TpHamlet;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;

class SeedHamletData extends Command
{
    protected $signature = 'seed:hamlet-data';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
    public function handle()
    {
        DB::table('hamlets')->truncate();
        $tpHamlets = TpHamlet::query()->select(['id', 'name', 'ward_id', 'status', 'created_at', 'updated_at'])->get()->toArray();
        DB::table('hamlets')->insert($tpHamlets);
    }
}
