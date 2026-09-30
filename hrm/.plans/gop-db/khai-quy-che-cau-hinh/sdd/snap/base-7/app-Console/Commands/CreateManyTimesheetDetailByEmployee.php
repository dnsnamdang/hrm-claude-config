<?php

namespace App\Console\Commands;

use App\Models\EmployeeInfo;
use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Services\WorkShiftDetailService;

class CreateManyTimesheetDetailByEmployee extends Command
{
    /**
     * The name and signature of the console command.
     *
     * employee_info_id: 1 hoặc nhiều id ngăn cách bởi dấu phẩy (vd: 123 hoặc 123,124,125)
     *                   Có thể bỏ trống nếu dùng --company_id
     * --company_id    : tạo cho TẤT CẢ nhân sự đang hoạt động (employee_infos.status = 1)
     *                   thuộc công ty đó. Nhiều công ty ngăn cách bởi dấu phẩy.
     *
     * VD: php artisan create:many_timesheet_detail_by_employee --company_id=1 2025-08-01 2025-08-31
     *
     * @var string
     */
    protected $signature = 'create:many_timesheet_detail_by_employee
        {employee_info_id? : 1 hoặc nhiều employee_info_id ngăn cách bởi dấu phẩy}
        {from_date=-1}
        {to_date=-1}
        {--company_id= : Tạo cho tất cả nhân sự đang hoạt động của công ty (nhiều công ty ngăn cách bởi dấu phẩy)}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Tạo bảng chấm công chi tiết theo khoảng ngày cho 1/nhiều nhân viên (employee_info_id) hoặc toàn bộ nhân sự đang hoạt động của công ty (--company_id)';
    private $workShiftDetailService;

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct(WorkShiftDetailService $workShiftDetailService)
    {
        $this->workShiftDetailService = $workShiftDetailService;
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $employeeInfoIdArg = $this->argument('employee_info_id');
        $companyIdOption = $this->option('company_id');
        $from_date = $this->argument('from_date');
        $to_date = $this->argument('to_date');

        $employeeInfoIds = $this->parseIds($employeeInfoIdArg);
        $companyIds = $this->parseIds($companyIdOption);

        if ($companyIds->isNotEmpty()) {
            $idsByCompany = EmployeeInfo::query()
                ->whereIn('company_id', $companyIds->all())
                ->where('status', EmployeeInfo::STATUSES['active'])
                ->orderBy('id')
                ->pluck('id');

            if ($idsByCompany->isEmpty()) {
                $this->error('Không tìm thấy nhân sự đang hoạt động nào thuộc company_id = ' . $companyIds->implode(', '));
                return;
            }

            $this->info("Tìm thấy {$idsByCompany->count()} nhân sự đang hoạt động thuộc company_id = " . $companyIds->implode(', '));
            $employeeInfoIds = $employeeInfoIds->merge($idsByCompany)->unique()->values();
        }

        if ($employeeInfoIds->isEmpty()) {
            $this->error('Thiếu employee_info_id hoặc --company_id.');
            return;
        }

        $diff = Carbon::parse($to_date)->diff($from_date);
        $diffDay = $diff->days;

        $total = $employeeInfoIds->count();
        $index = 0;

        foreach ($employeeInfoIds as $employeeInfoId) {
            $index++;
            $start = Carbon::parse($from_date);
            for ($i = 0; $i <= $diffDay; $i++) {
                $date = $start->format('Y-m-d');
                $this->workShiftDetailService->createTimesheetDetail($date, $employeeInfoId);
                $start->addDays();
            }
            $this->info("[{$index}/{$total}] Đã tạo chấm công cho employee_info_id = {$employeeInfoId}");
        }

        $this->info('Cập nhật thành công');
    }

    /**
     * Tách chuỗi id ngăn cách bởi dấu phẩy thành collection id hợp lệ.
     *
     * @param  string|null $value
     * @return \Illuminate\Support\Collection
     */
    private function parseIds($value)
    {
        if ($value === null || $value === '') {
            return collect();
        }

        return collect(explode(',', $value))
            ->map(function ($id) {
                return trim($id);
            })
            ->filter(function ($id) {
                return $id !== '' && is_numeric($id);
            })
            ->map(function ($id) {
                return (int) $id;
            })
            ->unique()
            ->values();
    }
}
