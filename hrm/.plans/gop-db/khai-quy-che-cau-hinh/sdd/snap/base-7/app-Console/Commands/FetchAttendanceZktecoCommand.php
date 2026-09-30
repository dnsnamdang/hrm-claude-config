<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Fsuuaas\Zkteco\Lib\ZKTeco;
use Carbon\Carbon;
use Illuminate\Support\Facades\Log;
use Modules\Human\Entities\EmployeeInfo;
use Modules\Timesheet\Entities\ConnInfo;
use Modules\Timesheet\Entities\Timesheet;

class FetchAttendanceZktecoCommand extends Command
{
    protected $signature = 'attendance:fetch-zkteco
                            {--from= : Thời gian bắt đầu (VD: "2025-05-29 08:00")}
                            {--to= : Thời gian kết thúc (VD: "2025-05-29 08:05")}';

    protected $description = 'Lấy dữ liệu từ máy chấm công ZKTeco theo khoảng thời gian';

    public function handle()
    {
        $devices = $this->getConnInfo();

        // Lấy thời gian từ tham số hoặc mặc định 5 phút gần nhất
        $from = $this->option('from')
            ? Carbon::parse($this->option('from'))
            : now()->startOfDay();

        $to = $this->option('to')
            ? Carbon::parse($this->option('to'))
            : now()->endOfDay();

        if ($from->greaterThan($to)) {
            $this->error("Thời gian bắt đầu phải nhỏ hơn hoặc bằng thời gian kết thúc.");
            return;
        }

        $this->info("Đang lấy log từ {$from->toDateTimeString()} đến {$to->toDateTimeString()}");
        Log::info("Đang lấy log từ {$from->toDateTimeString()} đến {$to->toDateTimeString()}");

        foreach ($devices as $device) {
            try {
                $zk = new ZKTeco($device['ip'], $device['port']);

                if ($zk->connect()) {
                    $this->info("Đã kết nối tới thiết bị: {$device['ip']}:{$device['port']}");
                    Log::info("Đã kết nối tới thiết bị: {$device['ip']}:{$device['port']}");
                    $allLogs = $zk->getAttendance(49); // Lấy toàn bộ log
                    $zk->disconnect();

                    $logs = collect($allLogs)->filter(function ($log) use ($from, $to) {
                        $timestamp = Carbon::parse($log['timestamp']);
                        return $timestamp->between($from, $to);
                    });

                    if ($logs->isEmpty()) {
                        $this->warn(" Không có log nào trong khoảng thời gian đã chọn.");
                        Log::info(" Không có log nào trong khoảng thời gian đã chọn.");
                    } else {
                        $this->info(" Số log tìm được: " . $logs->count());
                        Log::info(" Số log tìm được: " . $logs->count());
                        foreach ($logs as $log) {
                            $log['conn_info_id'] = $device['id'];
                            $this->storeTimeSheet($log);
                        }
                    }

                    $this->info("Đã ngắt kết nối với thiết bị.");
                } else {
                    $this->error(" Không thể kết nối tới thiết bị: {$device['ip']}:{$device['port']}");
                }
            } catch (\Throwable $e) {
                $this->error("Lỗi: " . $e->getMessage());
                Log::error("Lỗi: " . $e->getMessage());
            }
        }
    }

    public function getConnInfo()
    {
        $connInfos = ConnInfo::select('id', 'ip', 'port')->where('machine_type_id', Timesheet::MACHINE_TYPES['zkteco'])->get();

        return $connInfos;
    }

    public function storeTimeSheet($data)
    {
        $employeeInfo = EmployeeInfo::where('ssn', (int)$data['id'])->first();
        if (!$employeeInfo) {
            return;
        }

        Timesheet::firstOrCreate([
            'employee_info_id' => (int)$data['id'],
            'verify_date' => $data['timestamp'],
            'machine_type_id' => Timesheet::MACHINE_TYPES['zkteco'],
            'conn_info_id' => $data['conn_info_id'],
            'company_id' => $employeeInfo->company_id,
        ]);
    }
}
