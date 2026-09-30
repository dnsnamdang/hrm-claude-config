<?php

namespace App\Console\Commands;
use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Human\Entities\TpEmployee;
use Modules\Human\Entities\Employee;

class UpdatePass extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'update:pass';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
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
        $employees = Employee::all();
        foreach($employees as $employee) {
          $tpEmployee = TpEmployee::find($employee->id);
          $employee->password = $tpEmployee->password;
          $employee->save();
        }
    }
}
