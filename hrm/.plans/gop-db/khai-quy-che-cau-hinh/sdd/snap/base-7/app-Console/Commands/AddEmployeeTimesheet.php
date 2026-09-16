<?php

namespace App\Console\Commands;

use Carbon\Carbon;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Entities\ShiftDetailEmployeeDate;
use Modules\Timesheet\Entities\Timesheet;
use Modules\Timesheet\Entities\WorkShift;
use Modules\Timesheet\Services\WorkShiftDetailService;
use Modules\Timesheet\Services\TimesheetSummaryService;

class AddEmployeeTimesheet extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'add:employee_timesheet {employee_info_id} {working_shift_id} {date=-1} {shift_detail_id=null} {--to-date= : Ngày kết thúc (Y-m-d) — có truyền thì phân ca cho cả khoảng date -> to-date}'
        . ' {--with-attendance : Sinh luôn dữ liệu chấm công (bảng timesheets) để nhân viên có công thực tế}'
        . ' {--checkin= : Giờ vào (H:i hoặc H:i:s), mặc định lấy giờ bắt đầu ca}'
        . ' {--checkout= : Giờ ra (H:i hoặc H:i:s), mặc định lấy giờ kết thúc ca}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Thêm ca cho 1 nhân viên theo ngày hoặc khoảng ngày (--to-date): ghi shift_detail_employee_dates, tạo timesheet detail, sinh chấm công (--with-attendance) rồi tính công';
    private $workShiftDetailService;
    private $timesheetSummaryService;

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct(
        WorkShiftDetailService $workShiftDetailService,
        TimesheetSummaryService $timesheetSummaryService
    ) {
        $this->workShiftDetailService = $workShiftDetailService;
        $this->timesheetSummaryService = $timesheetSummaryService;
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $employeeInfoId = $this->argument('employee_info_id');
        $workingShiftId = $this->argument('working_shift_id');
        $date = $this->argument('date');
        $shiftDetailId = $this->argument('shift_detail_id');
        $toDate = $this->option('to-date');
        if ($date == -1) {
            $date = Carbon::now()->format('Y-m-d');
        }
        if ($shiftDetailId === 'null') {
            $shiftDetailId = null;
        }

        // Không truyền --to-date => giữ nguyên hành vi cũ: chỉ phân ca đúng 1 ngày
        if (empty($toDate)) {
            $toDate = $date;
        }

        try {
            $fromDay = Carbon::createFromFormat('Y-m-d', $date)->startOfDay();
            $toDay = Carbon::createFromFormat('Y-m-d', $toDate)->startOfDay();
        } catch (\Exception $e) {
            $this->error('Ngày không hợp lệ, định dạng đúng là Y-m-d (VD: 2026-08-01)');
            return;
        }

        if ($toDay->lt($fromDay)) {
            $this->error("Ngày kết thúc {$toDate} nhỏ hơn ngày bắt đầu {$date}");
            return;
        }

        // Kiểm tra nhân viên tồn tại
        $employeeInfo = EmployeeInfo::where('id', '=', $employeeInfoId)->first();
        if (!$employeeInfo) {
            $this->error("Không tìm thấy nhân viên #{$employeeInfoId}");
            return;
        }

        // Chuẩn bị dữ liệu cho bước sinh chấm công (nếu có --with-attendance)
        $withAttendance = $this->option('with-attendance');
        $workShift = null;
        if ($withAttendance) {
            $workShift = WorkShift::find($workingShiftId);
            if (!$workShift) {
                $this->error("Không tìm thấy ca làm việc #{$workingShiftId}, không sinh được chấm công");
                return;
            }
            if (empty($employeeInfo->ssn)) {
                $this->error("Nhân viên #{$employeeInfoId} chưa có mã chấm công (ssn) — bảng timesheets khớp theo ssn nên không sinh được chấm công");
                return;
            }
        }

        $totalDays = $fromDay->diffInDays($toDay) + 1;
        if ($totalDays > 1) {
            $this->info("Phân ca #{$workingShiftId} cho nhân viên #{$employeeInfoId} từ {$date} đến {$toDate} ({$totalDays} ngày)");
        }

        for ($day = $fromDay->copy(); $day->lte($toDay); $day->addDay()) {
            $currentDate = $day->format('Y-m-d');

            // Bước 1: ghi ca vào shift_detail_employee_dates (1 bản ghi/nhân viên/ngày)
            ShiftDetailEmployeeDate::updateOrCreate(
                [
                    'employee_info_id' => $employeeInfoId,
                    'date' => $currentDate,
                ],
                [
                    'working_shift_id' => $workingShiftId,
                    'shift_detail_id' => $shiftDetailId,
                ]
            );
            $this->info("Đã ghi ca #{$workingShiftId} cho nhân viên #{$employeeInfoId} ngày {$currentDate}");

            // Bước 2: sinh timesheet detail từ ca vừa ghi
            $this->workShiftDetailService->createTimesheetDetail($currentDate, $employeeInfoId);
            $this->info("Đã tạo timesheet detail cho nhân viên #{$employeeInfoId} ngày {$currentDate}");

            // Bước 3 (tuỳ chọn): sinh dữ liệu chấm công thực tế để nhân viên có công
            if ($withAttendance) {
                [$checkin, $checkout] = $this->makeAttendance($employeeInfo, $workShift, $currentDate);
                $this->info("Đã sinh chấm công ngày {$currentDate}: vào {$checkin} — ra {$checkout}");
            }

            // Bước 4: tính công cho nhân viên ngày đó
            $this->timesheetSummaryService->calcTimesheetEmployee($employeeInfo, $currentDate);
            $this->info("Đã tính công cho nhân viên #{$employeeInfoId} ngày {$currentDate}");
        }

        $this->info('Hoàn tất');
    }

    /**
     * Sinh 2 bản ghi chấm công (vào/ra) trong bảng timesheets cho 1 ngày.
     *
     * Lưu ý: cột timesheets.employee_info_id thực chất lưu ssn (mã chấm công)
     * của nhân viên — xem TimesheetSummaryService::calcTimesheetEmployee.
     *
     * @return array [checkin, checkout] dạng Y-m-d H:i:s
     */
    private function makeAttendance($employeeInfo, $workShift, $date)
    {
        $startAt = $this->option('checkin') ?: $workShift->start_at;
        $endAt = $this->option('checkout') ?: $workShift->end_at;

        $checkin = Carbon::parse("$date " . $this->normalizeTime($startAt));
        $checkout = Carbon::parse("$date " . $this->normalizeTime($endAt));

        // Ca đêm: giờ ra <= giờ vào => checkout rơi sang ngày hôm sau
        if ($checkout->lte($checkin)) {
            $checkout->addDay();
        }

        foreach ([$checkin, $checkout] as $verifyDate) {
            Timesheet::updateOrCreate(
                [
                    'employee_info_id' => $employeeInfo->ssn,
                    'verify_date' => $verifyDate->format('Y-m-d H:i:s'),
                ],
                [
                    'accept' => true,
                    'type' => 0, // máy chấm công
                    'company_id' => $employeeInfo->company_id ?: 1,
                ]
            );
        }

        return [$checkin->format('Y-m-d H:i:s'), $checkout->format('Y-m-d H:i:s')];
    }

    /**
     * Chuẩn hoá giờ về H:i:s (chấp nhận đầu vào H:i hoặc H:i:s).
     */
    private function normalizeTime($time)
    {
        $time = trim((string) $time);

        return substr_count($time, ':') === 1 ? $time . ':00' : $time;
    }
}
