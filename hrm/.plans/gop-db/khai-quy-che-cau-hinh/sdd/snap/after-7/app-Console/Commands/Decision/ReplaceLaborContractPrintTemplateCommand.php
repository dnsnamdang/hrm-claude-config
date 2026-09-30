<?php

namespace App\Console\Commands\Decision;

use Exception;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Modules\Human\Entities\PrintTemplate;

class ReplaceLaborContractPrintTemplateCommand extends Command
{
    protected $signature = 'decision:replace-labor-print-template
        {target : Bảng đích: labor-contract hoặc appendix-labor-contract}
        {print_template_id : ID mẫu in trong bảng print_templates}
        {--from-date= : (Tùy chọn) Chỉ cập nhật bản ghi tạo từ ngày này đến hiện tại (định dạng Y-m-d). Bỏ trống = cập nhật tất cả}
        {--force : Không hỏi xác nhận trước khi cập nhật}';

    protected $description = 'Thay thế mẫu in cho toàn bộ Quyết định HĐLĐ (decision_labor_contracts) hoặc Phụ lục HĐLĐ (appendix_labor_contracts) (ghi đè print_template, print_template_id, print_template_type_id)';

    /**
     * Map target slug -> cấu hình bảng đích.
     */
    const TARGETS = [
        'labor-contract' => [
            'table' => 'decision_labor_contracts',
            'label' => 'Quyết định hợp đồng lao động',
            'soft_delete' => true,
        ],
        'appendix-labor-contract' => [
            'table' => 'appendix_labor_contracts',
            'label' => 'Phụ lục hợp đồng lao động',
            'soft_delete' => false,
        ],
    ];

    public function handle()
    {
        try {
            $target = $this->argument('target');
            $printTemplateId = $this->argument('print_template_id');

            if (!array_key_exists($target, self::TARGETS)) {
                $this->error("Target '{$target}' không hợp lệ. Các giá trị hợp lệ:");
                foreach (array_keys(self::TARGETS) as $key) {
                    $this->line("  {$key}");
                }
                return 1;
            }
            $config = self::TARGETS[$target];

            $printTemplate = PrintTemplate::find($printTemplateId);
            if (!$printTemplate) {
                $this->error("Không tìm thấy mẫu in có ID = {$printTemplateId}.");
                return 1;
            }

            $fromDate = $this->option('from-date');
            if ($fromDate !== null && $fromDate !== '') {
                $parsedDate = \DateTime::createFromFormat('Y-m-d', $fromDate);
                if (!$parsedDate || $parsedDate->format('Y-m-d') !== $fromDate) {
                    $this->error("Ngày '{$fromDate}' không hợp lệ. Định dạng đúng: Y-m-d (ví dụ: 2026-07-01).");
                    return 1;
                }
            } else {
                $fromDate = null;
            }

            $query = DB::table($config['table']);
            if ($config['soft_delete']) {
                $query->whereNull('deleted_at');
            }
            if ($fromDate !== null) {
                $query->where('created_at', '>=', $fromDate . ' 00:00:00');
            }

            $total = (clone $query)->count();
            if ($total === 0) {
                $rangeText = $fromDate !== null ? " (tạo từ {$fromDate} đến hiện tại)" : '';
                $this->info("Không có bản ghi nào trong '{$config['label']}'$rangeText.");
                return 0;
            }

            $this->info("Mẫu in: [{$printTemplate->id}] {$printTemplate->name}");
            $this->info("Đối tượng: {$target} — {$config['label']} (bảng {$config['table']})");
            if ($fromDate !== null) {
                $this->info("Phạm vi: bản ghi tạo từ {$fromDate} đến hiện tại");
            } else {
                $this->info('Phạm vi: tất cả bản ghi (không lọc theo ngày)');
            }
            $this->info("Số bản ghi sẽ bị ghi đè mẫu in: {$total}");

            if (!$this->option('force') && !$this->confirm('Xác nhận thay thế mẫu in cho toàn bộ các bản ghi trên?')) {
                $this->info('Đã hủy, không có dữ liệu nào bị thay đổi.');
                return 0;
            }

            $updated = $query->update([
                'print_template' => $printTemplate->template,
                'print_template_id' => $printTemplate->id,
                'print_template_type_id' => $printTemplate->type,
            ]);

            $this->info("Đã thay thế mẫu in cho {$updated}/{$total} bản ghi trong '{$config['label']}'.");
            return 0;
        } catch (Exception $e) {
            Log::error($e);
            $this->error('Đã xảy ra lỗi khi thay thế mẫu in: ' . $e->getMessage());
            return 1;
        }
    }
}
