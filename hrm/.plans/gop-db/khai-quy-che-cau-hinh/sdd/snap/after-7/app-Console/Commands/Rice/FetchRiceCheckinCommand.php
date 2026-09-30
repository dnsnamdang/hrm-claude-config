<?php

namespace App\Console\Commands\Rice;

use App\Models\EmployeeInfo;
use Illuminate\Console\Command;
use GuzzleHttp\Client;
use Carbon\Carbon;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Modules\Rice\Entities\Category\RiceConnInfo;
use Modules\Rice\Entities\RiceEmployeeInfo;
use Modules\Rice\Entities\RiceRegistration;
use Modules\Timesheet\Entities\ConnInfo;
use Modules\Timesheet\Entities\Timesheet;

class FetchRiceCheckinCommand extends Command
{
    // Tên của lệnh (command) khi gọi qua terminal
    // php artisan attendance:fetch "10/08/2024 10:10" "10/08/2024 10:15"

    protected $signature = 'rice:fetch-checkin {startTime?} {endTime?}';

    // Số lượng kết quả tối đa trên mỗi trang
    protected $maxResultsPerPage = 30;
    /**
     * Thực thi lệnh.
     */
    public function handle()
    {
        try {
            // Lấy thời gian bắt đầu và kết thúc từ tham số truyền vào
            $startTime = $this->argument('startTime');
            $endTime = $this->argument('endTime');

            // Nếu không có, mặc định lấy khoảng thời gian trong 2 phút gần nhất
            [$startTime, $endTime] = $this->getTimeRange($startTime, $endTime);
            // Gọi API để lấy tất cả bản ghi chấm công
            $allRecords = $this->fetchAllRiceCheckinData($startTime, $endTime);
            // Lưu các bản ghi vào cơ sở dữ liệu
            $this->saveRiceCheckinRecords($allRecords);
        } catch (\Exception $e) {
            Log::error('Error fetching attendance data: ' . $e->getMessage());
        }
    }

    /**
     * Lấy khoảng thời gian bắt đầu và kết thúc.
     */
    private function getTimeRange($startTime, $endTime)
    {
        if (!$startTime || !$endTime) {
            // Lấy thời gian hiện tại và 2 phút trước với múi giờ +07:00
            $now = Carbon::now('Asia/Ho_Chi_Minh');
            $tenMinutesAgo = $now->copy()->subMinutes(10);

            $startTime = $tenMinutesAgo->format('Y-m-d\TH:i:sP');
            $endTime = $now->format('Y-m-d\TH:i:sP');
        } else {
            // Chuyển đổi thời gian từ định dạng d/m/Y H:i sang Y-m-d\TH:i:sP với múi giờ +07:00
            $startTime = Carbon::createFromFormat('d/m/Y H:i', $startTime, 'Asia/Ho_Chi_Minh')
                ->format('Y-m-d\TH:i:sP');
            $endTime = Carbon::createFromFormat('d/m/Y H:i', $endTime, 'Asia/Ho_Chi_Minh')
                ->format('Y-m-d\TH:i:sP');
        }

        Log::info('Start time: ' . $startTime);
        Log::info('End time: ' . $endTime);

        return [$startTime, $endTime];
    }

    /**
     * Gọi API để lấy tất cả các trang dữ liệu chấm công.
     */
    private function fetchAllRiceCheckinData($startTime, $endTime)
    {
        $client = new Client();
        $allRecords = [];
        $connInfos = RiceConnInfo::where('status', 1)->get();
        foreach ($connInfos as $connInfo) {
            $records = $this->fetchRiceCheckinFromMachine($client, $connInfo, $startTime, $endTime);
            $allRecords = array_merge($allRecords, $records);
        }

        Log::info('Total records: ' . count($allRecords));

        return $allRecords;
    }

    /**
     * Gọi API từ máy chấm công cụ thể và phân trang.
     */
    private function fetchRiceCheckinFromMachine($client, $connInfo, $startTime, $endTime)
    {
        $allRecords = [];
        $hasMorePages = true;
        $searchResultPosition = 0;
        while ($hasMorePages) {

            $data = $this->prepareRequestData($startTime, $endTime, $searchResultPosition);
            try {
                $client = new Client([
                    'base_uri' => "{$connInfo->ip}:{$connInfo->port}",
                    'timeout'  => 30,  // Thời gian chờ cho mỗi request
                    'headers'  => [
                        'Connection' => 'keep-alive',  // Bật Keep-Alive
                    ],
                ]);
                $response = $client->post(
                    "/ISAPI/AccessControl/AcsEvent?format=json",
                    [
                        'json' => $data,
                        'auth' => [$connInfo->user_name, $connInfo->password, 'digest'],
                        'headers' => ['Content-Type' => 'application/json'],
                    ]
                );
                $contentResponse = $response->getBody()->getContents();

                $records = $this->processResponse($contentResponse, $connInfo);
                $allRecords = array_merge($allRecords, $records);
                if (!$this->hasMorePages($contentResponse)) {
                    $hasMorePages = false;
                } else {
                    $searchResultPosition += $this->maxResultsPerPage;
                }
            } catch (\Exception $e) {
                Log::error("Error fetching attendance data from {$connInfo->ip}: ", ['error' => $e->getMessage()]);
                $hasMorePages = false;
            }
        }
        return $allRecords;
    }

    /**
     * Chuẩn bị dữ liệu request cho API.
     */
    private function prepareRequestData($startTime, $endTime, $searchResultPosition)
    {
        return [
            'AcsEventCond' => [
                'searchID' => '1',
                'searchResultPosition' => $searchResultPosition,
                'maxResults' => $this->maxResultsPerPage,
                'major' => 0,
                'minor' => 0,
                'startTime' => $startTime,
                'endTime' => $endTime,
                'timeReverseOrder' => true,
                'isAbnomalTemperature' => true,
                'temperatureSearchCond' => 'all',
                'isAttendanceInfo' => true,
                'hasRecordInfo' => true,
            ],
        ];
    }

    /**
     * Xử lý dữ liệu trả về từ API.
     */
    private function processResponse($responseContent, $connInfo)
    {
        $responseData = json_decode($responseContent, true);
        $records = $responseData['AcsEvent']['InfoList'] ?? [];

        $validRecords = array_filter($records, function ($record) {
            return isset($record['employeeNoString'], $record['time']) && is_numeric($record['employeeNoString']);
        });

        $uniqueRecords = [];
        foreach ($validRecords as $record) {
            $key = $record['employeeNoString'] . '-' . $record['time'];
            if (!isset($uniqueRecords[$key])) {
                $uniqueRecords[$key] = [
                    'employeeNoString' => $record['employeeNoString'],
                    'time' => $record['time'],
                    'conn_info_id' => $connInfo->id,
                    'currentVerifyMode' => $record['currentVerifyMode'],
                ];
            }
        }

        return array_values($uniqueRecords);
    }

    /**
     * Kiểm tra xem còn trang dữ liệu nào nữa không.
     */
    private function hasMorePages($responseContent)
    {
        $responseData = json_decode($responseContent, true);
        return $responseData['AcsEvent']['responseStatusStrg'] == 'MORE';
    }

    /**
     * Lưu các bản ghi chấm công vào cơ sở dữ liệu.
     */
    private function saveRiceCheckinRecords($records)
    {
        foreach ($records as $record) {
            $date = Carbon::parse($record['time'])->format('Y-m-d');
            $riceEmployeeInfo = RiceEmployeeInfo::where('rice_ssn', (int)$record['employeeNoString'])->first();
            $riceRegistration = RiceRegistration::where('rice_employee_info_id', $riceEmployeeInfo->id)
                ->where('status_regular', 4)->where('date', $date)->first();

            if (!$riceRegistration) {
                continue;
            } else {
                $riceRegistration->update([
                    'status_regular' => 3,
                ]);
            }
        }
    }
}
