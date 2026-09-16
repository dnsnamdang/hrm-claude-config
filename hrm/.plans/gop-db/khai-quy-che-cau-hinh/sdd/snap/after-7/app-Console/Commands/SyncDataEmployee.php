<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Human\Entities\EmployeeInfo;
use Modules\Human\Entities\TpEmployeeInfo;
use Modules\Timesheet\Services\EmployeeInfoService;
use Modules\Human\Entities\TpEmployee;
use Modules\Human\Entities\Employee;

class SyncDataEmployee extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'sync:data_employee';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';
    private $employeeInfoService;
    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct(EmployeeInfoService $employeeInfoService)
    {
        $this->employeeInfoService = $employeeInfoService;
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $fillable = [
            'code',
            'fullname',
            'image',
            'telephone',
            'department_id',
            'part_id',
            'team_id',
            'company_id',
            'ssn',
            'position',
            'account_number',
            'bank_name',
            'status',
            'gender',
            'birthday',
            'national',
            'termination_date',
            'receive_date',
            'hire_date',
            'working_type',
            'job_position_id',
            'enter_date',
            'vacation_start_date',
            'vacation_start_date_type',
            'email',
            'leave_date',
            'seniority_start_date_type',
            'seniority_start_date',
            'first_name',
            'last_name',
            'place_of_birth',
            'home_town',
            'permanent_residence',
            'address',
            'marital_status',
            'religion',
            'tax_code',
            'social_insurance_code',
            'personal_email',
            'personal_telephone',
            'participate_communist_party_day',
            'participate_communist_party_place',
            'health_status',
            'health_certification_file',
            'emergency_contact_number',
            'emergency_contact_name',
            'id_card',
            'grant_date',
            'id_expire_date',
            'grant_location',
            'id_images',
            'passport_number',
            'passport_grant_date',
            'passport_expire_date',
            'passport_grant_place',
            'passport_images',
            'bank_id',
            'bank_branch_id',
            'academic_level',
            'academic_experience',
            'academic_skill',
            'time_attendance_code',
            'return_date',
            'employee_role_id',
            'employee_work_position_id',
            'employee_concurrently_position_id',
            'salary_p1',
            'salary_p2',
            'salary_p3',
            'gasonline_car_support_money',
            'phone_support_money',
            'different_support_money',

            'province_id_residence',
            'district_id_residence',
            'ward_id_residence',
            'hamlet_residence',
            'province_id_address',
            'district_id_address',
            'ward_id_address',
            'hamlet_address',

            'created_by',
            'updated_by'
        ];
        $tpEmployeeInfos = TpEmployeeInfo::all();
        foreach ($tpEmployeeInfos as $tpEmployeeInfo) {
            $employeeInfo = EmployeeInfo::find($tpEmployeeInfo->id);
            if (!$employeeInfo) {
                $this->info('Khong ton tai id = ' . $tpEmployeeInfo->id);
                $newEmp = new EmployeeInfo();
                $newEmp->id = $tpEmployeeInfo->id;
                foreach ($fillable as $column) {
                    if (isset($tpEmployeeInfo->$column)) {
                        $newEmp->$column = $tpEmployeeInfo->$column;
                    }
                }
                $newEmp->save();
            } else {
                if ($employeeInfo->email != $tpEmployeeInfo->email) {
                    $this->info('Email khac nhau id = ' . $tpEmployeeInfo->id);
                }
                foreach ($fillable as $column) {
                    if (isset($tpEmployeeInfo->$column)) {

                        if ($tpEmployeeInfo->$column != $employeeInfo->$column) {
                            $employeeInfo->$column = $tpEmployeeInfo->$column;
                        }
                    }
                }
                $employeeInfo->save();
            }
        }


        // Tai khoan
        $tpEmployees = TpEmployee::all();
        foreach ($tpEmployees as $tpEmployee) {
            $employee = Employee::find($tpEmployee->id);
            if (!$employee) {
                $this->info('Khong ton tai id = ' . $tpEmployee->id);
            } else {
                if ($employee->email != $tpEmployee->email) {
                    $this->info('Email khac nhau id = ' . $tpEmployee->id);
                }

                if ($employee->employee_info_id != $tpEmployee->employee_info_id) {
                    $this->info('employee_info_id khac nhau id = ' . $tpEmployee->id);
                }
            }
        }
    }
}
