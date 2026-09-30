<?php

namespace App\Console\Commands\Timesheet;

use Illuminate\Console\Command;
use Modules\Timesheet\Entities\ConnInfo;
use Modules\Timesheet\Services\HikvisionSyncService;

class SyncHikvisionEmployees extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'timesheet:sync-hikvision-employees
                            {source_id : ID của máy chấm công nguồn}
                            {target_id : ID của máy chấm công đích}
                            {employee_nos : Danh sách mã nhân viên (ngăn cách bởi dấu phẩy)}
                            {--no-face : Không đồng bộ khuôn mặt, chỉ đồng bộ thông tin user}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Đồng bộ thủ công một hoặc nhiều nhân sự từ máy chấm công Hikvision này sang máy khác';

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $sourceId = (int) $this->argument('source_id');
        $targetId = (int) $this->argument('target_id');
        $employeeNosStr = $this->argument('employee_nos');
        $includeFaces = !$this->option('no-face');

        // Parse danh sách employeeNo
        $employeeNos = array_map('trim', explode(',', $employeeNosStr));
        $employeeNos = array_filter($employeeNos); // Loại bỏ empty values

        if (empty($employeeNos)) {
            $this->error('Không có mã nhân viên nào để đồng bộ!');
            return 1;
        }

        $this->info("=== ĐỒNG BỘ NHÂN SỰ HIKVISION ===");
        $this->info("Máy nguồn: {$sourceId}");
        $this->info("Máy đích: {$targetId}");
        $this->info("Số lượng nhân sự: " . count($employeeNos));
        $this->info("Đồng bộ khuôn mặt: " . ($includeFaces ? 'CÓ' : 'KHÔNG'));
        $this->info("");

        // Kiểm tra conn_info
        try {
            $source = ConnInfo::findOrFail($sourceId);
            $target = ConnInfo::findOrFail($targetId);
        } catch (\Exception $e) {
            $this->error("Lỗi: Không tìm thấy máy chấm công! " . $e->getMessage());
            return 1;
        }

        $this->info("Máy nguồn: {$source->name} ({$source->ip}:{$source->port})");
        $this->info("Máy đích: {$target->name} ({$target->ip}:{$target->port})");
        $this->info("");

        if (!$this->confirm('Bạn có chắc muốn tiếp tục?')) {
            $this->info('Đã hủy!');
            return 0;
        }

        $hikvision = new HikvisionSyncService($source, $target);

        $successCount = 0;
        $failCount = 0;
        $progress = $this->output->createProgressBar(count($employeeNos));
        $progress->start();

        foreach ($employeeNos as $employeeNo) {
            try {
                // Lấy thông tin user từ máy nguồn
                $userInfo = $this->getUserFromSource($hikvision, $employeeNo);

                if (!$userInfo) {
                    $this->newLine();
                    $this->warn("⚠️  Không tìm thấy nhân sự {$employeeNo} trên máy nguồn");
                    $failCount++;
                    $progress->advance();
                    continue;
                }

                $name = $userInfo['name'] ?? $employeeNo;

                // Tạo user trên máy đích
                try {
                    $this->createUserOnTarget($hikvision, $employeeNo, $name);
                } catch (\Exception $e) {
                    // Bỏ qua nếu user đã tồn tại
                    if (strpos($e->getMessage(), 'employeeNoAlreadyExist') === false) {
                        throw $e;
                    }
                }

                // Đồng bộ khuôn mặt nếu cần
                if ($includeFaces) {
                    $face = $this->callProtectedMethod($hikvision, 'getFaceImageFromSource', [$employeeNo]);

                    if ($face) {
                        $uploaded = $this->callProtectedMethod($hikvision, 'uploadFaceToTarget', [$employeeNo, $face]);

                        if (!$uploaded) {
                            $this->newLine();
                            $this->warn("⚠️  Upload khuôn mặt thất bại: {$employeeNo} - {$name}");
                            $failCount++;
                            $progress->advance();
                            continue;
                        }
                    } else {
                        $this->newLine();
                        $this->warn("⚠️  Không tìm thấy khuôn mặt: {$employeeNo} - {$name}");
                        $failCount++;
                        $progress->advance();
                        continue;
                    }
                }

                $successCount++;
            } catch (\Exception $e) {
                $this->newLine();
                $this->error("❌ Lỗi khi đồng bộ {$employeeNo}: " . $e->getMessage());
                $failCount++;
            }

            $progress->advance();
        }

        $progress->finish();
        $this->newLine(2);

        $this->info("=== KẾT QUẢ ===");
        $this->info("✅ Thành công: {$successCount}");
        $this->info("❌ Thất bại: {$failCount}");
        $this->info("📊 Tổng cộng: " . count($employeeNos));

        return 0;
    }

    /**
     * Lấy thông tin user từ máy nguồn
     */
    protected function getUserFromSource($hikvision, $employeeNo)
    {
        $users = $this->callProtectedMethod($hikvision, 'getUsersFromSource', []);

        foreach ($users as $user) {
            if ($user['employeeNo'] === $employeeNo) {
                return $user;
            }
        }

        return null;
    }

    /**
     * Tạo user trên máy đích
     */
    protected function createUserOnTarget($hikvision, $employeeNo, $name)
    {
        return $this->callProtectedMethod($hikvision, 'createUserOnTarget', [$employeeNo, $name]);
    }

    /**
     * Call protected method using reflection
     */
    protected function callProtectedMethod($object, $method, array $args = [])
    {
        $reflection = new \ReflectionClass(get_class($object));
        $method = $reflection->getMethod($method);
        $method->setAccessible(true);
        return $method->invokeArgs($object, $args);
    }
}
