<?php

namespace App\Console\Commands\Decision;

use Exception;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Modules\Decision\Entities\Decision;
use Modules\Human\Entities\PrintTemplate;

class ReplacePrintTemplateCommand extends Command
{
    protected $signature = 'decision:replace-print-template
        {print_template_id : ID mẫu in trong bảng print_templates}
        {type : Loại quyết định (cột type trong decisions), ví dụ: accept_personnels}
        {--from-date= : (Tùy chọn) Chỉ cập nhật quyết định tạo từ ngày này đến hiện tại (định dạng Y-m-d). Bỏ trống = cập nhật tất cả}
        {--company-id= : (Tùy chọn) Chỉ cập nhật mẫu in cho công ty này. Bỏ trống = cập nhật tất cả công ty}
        {--force : Không hỏi xác nhận trước khi cập nhật}';

    protected $description = 'Thay thế mẫu in cho tất cả quyết định theo loại (ghi đè print_template, print_template_id, print_template_type_id)';

    public function handle()
    {
        try {
            $printTemplateId = $this->argument('print_template_id');
            $type = $this->argument('type');

            $printTemplate = PrintTemplate::find($printTemplateId);
            if (!$printTemplate) {
                $this->error("Không tìm thấy mẫu in có ID = {$printTemplateId}.");
                return 1;
            }

            if (!array_key_exists($type, Decision::TYPE)) {
                $this->error("Loại quyết định '{$type}' không hợp lệ. Các loại hợp lệ:");
                foreach (Decision::TYPE as $key => $name) {
                    $this->line("  {$key} — {$name}");
                }
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

            $companyId = $this->option('company-id');
            if ($companyId !== null && $companyId !== '') {
                if (!ctype_digit((string) $companyId)) {
                    $this->error("ID công ty '{$companyId}' không hợp lệ. Phải là số nguyên dương.");
                    return 1;
                }
                $companyId = (int) $companyId;
            } else {
                $companyId = null;
            }

            $query = DB::table('decisions')
                ->where('type', $type)
                ->whereNull('deleted_at');

            if ($fromDate !== null) {
                $query->where('created_at', '>=', $fromDate . ' 00:00:00');
            }

            if ($companyId !== null) {
                $query->where('company_id', $companyId);
            }

            $total = (clone $query)->count();
            if ($total === 0) {
                $rangeText = $fromDate !== null ? " (tạo từ {$fromDate} đến hiện tại)" : '';
                $this->info("Không có quyết định nào thuộc loại '{$type}' (" . Decision::TYPE[$type] . ")$rangeText.");
                return 0;
            }

            $this->info("Mẫu in: [{$printTemplate->id}] {$printTemplate->name}");
            $this->info("Loại quyết định: {$type} — " . Decision::TYPE[$type]);
            if ($fromDate !== null) {
                $this->info("Phạm vi: quyết định tạo từ {$fromDate} đến hiện tại");
            } else {
                $this->info('Phạm vi: tất cả quyết định (không lọc theo ngày)');
            }
            if ($companyId !== null) {
                $this->info("Công ty: chỉ cập nhật cho công ty ID = {$companyId}");
            } else {
                $this->info('Công ty: tất cả công ty');
            }
            $this->info("Số quyết định sẽ bị ghi đè mẫu in: {$total}");

            if (!$this->option('force') && !$this->confirm('Xác nhận thay thế mẫu in cho toàn bộ các quyết định trên?')) {
                $this->info('Đã hủy, không có dữ liệu nào bị thay đổi.');
                return 0;
            }

            $updated = $query->update([
                'print_template' => $printTemplate->template,
                'print_template_id' => $printTemplate->id,
                'print_template_type_id' => $printTemplate->type,
            ]);

            $this->info("Đã thay thế mẫu in cho {$updated}/{$total} quyết định loại '{$type}'.");
            return 0;
        } catch (Exception $e) {
            Log::error($e);
            $this->error('Đã xảy ra lỗi khi thay thế mẫu in: ' . $e->getMessage());
            return 1;
        }
    }
}
