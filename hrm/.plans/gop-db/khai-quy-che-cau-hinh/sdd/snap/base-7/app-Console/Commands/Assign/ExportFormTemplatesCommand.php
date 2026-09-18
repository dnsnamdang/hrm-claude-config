<?php

namespace App\Console\Commands\Assign;

use Illuminate\Console\Command;
use Modules\Assign\Entities\FormTemplate;
use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;
use PhpOffice\PhpSpreadsheet\Style\Alignment;
use PhpOffice\PhpSpreadsheet\Style\Border;
use PhpOffice\PhpSpreadsheet\Style\Fill;

class ExportFormTemplatesCommand extends Command
{
    protected $signature = 'assign:export-form-templates
        {--path= : Đường dẫn file xuất ra (mặc định storage/app/exports/phieu-thu-thap-thong-tin.xlsx)}';

    protected $description = 'Export toàn bộ phiếu thu thập thông tin (kèm tất cả câu hỏi) ra file Excel';

    /** Nhãn trạng thái phiếu */
    private const STATUS_LABELS = [
        FormTemplate::STATUS_DRAFT => 'Nháp',
        FormTemplate::STATUS_PUBLISHED => 'Đã xuất bản',
        FormTemplate::STATUS_LOCKED => 'Đã khóa',
    ];

    /** Nhãn loại câu hỏi */
    private const TYPE_LABELS = [
        'text' => 'Văn bản ngắn',
        'textarea' => 'Văn bản dài',
        'select' => 'Danh sách chọn',
        'radio' => 'Một lựa chọn',
        'checkbox' => 'Nhiều lựa chọn',
        'date' => 'Ngày',
        'file' => 'Tệp đính kèm',
        'parent' => 'Câu hỏi cha',
        'number' => 'Số',
        'boolean' => 'Có/Không',
    ];

    /** Đếm số câu hỏi gom được khi xuất */
    private int $questionCount = 0;

    public function handle()
    {
        $templates = FormTemplate::with([
            'application',
            'sections' => function ($q) {
                $q->orderBy('position');
            },
            'sections.questions' => function ($q) {
                $q->orderBy('position');
            },
            'sections.questions.options' => function ($q) {
                $q->orderBy('position');
            },
            'sections.groups' => function ($q) {
                $q->orderBy('position');
            },
            'sections.groups.questions' => function ($q) {
                $q->orderBy('position');
            },
            'sections.groups.questions.options' => function ($q) {
                $q->orderBy('position');
            },
        ])->orderBy('id')->get();

        if ($templates->isEmpty()) {
            $this->warn('Không có phiếu thu thập thông tin nào trong cơ sở dữ liệu.');
            return 0;
        }

        $spreadsheet = new Spreadsheet();
        $this->buildTemplatesSheet($spreadsheet, $templates);
        $this->buildQuestionsSheet($spreadsheet, $templates);
        $spreadsheet->setActiveSheetIndex(0);

        $path = $this->resolvePath();
        $writer = new Xlsx($spreadsheet);
        $writer->save($path);

        $this->info('Đã xuất ' . $templates->count() . ' phiếu, ' . $this->questionCount . ' câu hỏi.');
        $this->info('File: ' . $path);

        return 0;
    }

    /** Sheet 1: tổng quan từng phiếu */
    private function buildTemplatesSheet(Spreadsheet $spreadsheet, $templates): void
    {
        $sheet = $spreadsheet->getActiveSheet();
        $sheet->setTitle('Danh sách phiếu');

        $headers = ['STT', 'ID phiếu', 'Tên phiếu', 'Ứng dụng', 'Trạng thái', 'Số phần', 'Số câu hỏi', 'Ngày tạo'];
        $this->writeHeaderRow($sheet, $headers);

        $row = 2;
        foreach ($templates as $i => $template) {
            $sheet->setCellValue('A' . $row, $i + 1);
            $sheet->setCellValue('B' . $row, $template->id);
            $sheet->setCellValue('C' . $row, (string) $template->name);
            $sheet->setCellValue('D' . $row, $template->application->name ?? '');
            $sheet->setCellValue('E' . $row, self::STATUS_LABELS[$template->status] ?? (string) $template->status);
            $sheet->setCellValue('F' . $row, $template->sections->count());
            $sheet->setCellValue('G' . $row, $this->countQuestions($template));
            $sheet->setCellValue('H' . $row, optional($template->created_at)->format('d/m/Y H:i'));
            $row++;
        }

        $this->styleBody($sheet, 'A2:H' . ($row - 1));
        foreach (range('A', 'H') as $col) {
            $sheet->getColumnDimension($col)->setAutoSize(true);
        }
    }

    /** Sheet 2: flat toàn bộ câu hỏi của tất cả phiếu */
    private function buildQuestionsSheet(Spreadsheet $spreadsheet, $templates): void
    {
        $sheet = $spreadsheet->createSheet();
        $sheet->setTitle('Chi tiết câu hỏi');

        $headers = [
            'STT', 'ID phiếu', 'Tên phiếu', 'Phần (Section)', 'Nhóm (Group)',
            'Loại câu hỏi', 'Nội dung câu hỏi',
            'Mã (code)', 'Key', 'Bắt buộc', 'Mô tả', 'Gợi ý (placeholder)',
            'Điều kiện hiển thị', 'Đáp án',
        ];
        $this->writeHeaderRow($sheet, $headers);

        // Thu thập toàn bộ dòng trước để biết phạm vi gộp ô
        $records = [];
        $stt = 0;
        foreach ($templates as $template) {
            foreach ($template->sections as $section) {
                $sectionLabel = $this->positionTitle($section->position, $section->title);

                // Câu hỏi trực tiếp dưới section (không thuộc group)
                foreach ($this->topLevel($section->questions) as $question) {
                    $this->collectQuestionRows($records, $stt, $template, $sectionLabel, '', $question, 0);
                }

                // Câu hỏi trong các group
                foreach ($section->groups as $group) {
                    $groupLabel = $this->positionTitle($group->position, $group->title);
                    foreach ($this->topLevel($group->questions) as $question) {
                        $this->collectQuestionRows($records, $stt, $template, $sectionLabel, $groupLabel, $question, 0);
                    }
                }
            }
        }

        // Ghi từng dòng ra sheet (cột chứa text dài cần ép kiểu chuỗi)
        $textCols = ['G', 'H', 'I', 'N'];
        $row = 2;
        foreach ($records as $rec) {
            foreach (range('A', 'N') as $idx => $col) {
                $value = $rec[$idx];
                if (in_array($col, $textCols, true)) {
                    $sheet->setCellValueExplicit($col . $row, (string) $value, \PhpOffice\PhpSpreadsheet\Cell\DataType::TYPE_STRING);
                } else {
                    $sheet->setCellValue($col . $row, $value);
                }
            }
            $row++;
        }

        $lastRow = max(2, $row - 1);
        $this->styleBody($sheet, 'A2:N' . $lastRow);
        foreach (range('A', 'N') as $col) {
            $sheet->getColumnDimension($col)->setAutoSize(true);
        }
        $sheet->getStyle('G2:N' . $lastRow)->getAlignment()->setWrapText(true)->setVertical(Alignment::VERTICAL_TOP);

        // Gộp ô cho dữ liệu trùng: ID + Tên phiếu (theo phiếu), Section/Group (trong cùng phiếu)
        $this->mergeColumn($sheet, $records, 'B', fn($r) => $r[1]);                          // ID phiếu
        $this->mergeColumn($sheet, $records, 'C', fn($r) => $r[1]);                          // Tên phiếu
        $this->mergeColumn($sheet, $records, 'D', fn($r) => $r[1] . '|' . $r[3]);            // Section trong phiếu
        $this->mergeColumn($sheet, $records, 'E', fn($r) => $r[1] . '|' . $r[3] . '|' . $r[4]); // Group trong section

        $this->questionCount = $stt;
    }

    /** Gom 1 câu hỏi + đệ quy câu hỏi con vào mảng $records (mỗi phần tử là 1 dòng A..P) */
    private function collectQuestionRows(array &$records, int &$stt, $template, string $sectionLabel, string $groupLabel, $question, int $level): void
    {
        $stt++;
        $indent = str_repeat('    ', $level);

        $records[] = [
            $stt,                                                       // A STT
            $template->id,                                             // B ID phiếu
            (string) $template->name,                                 // C Tên phiếu
            $sectionLabel,                                            // D Section
            $groupLabel,                                              // E Group
            self::TYPE_LABELS[$question->type] ?? (string) $question->type, // F Loại
            $indent . (string) $question->label,                     // G Nội dung
            (string) $question->code,                                 // H Mã
            (string) $question->key,                                  // I Key
            $question->required ? 'Có' : 'Không',                     // J Bắt buộc
            (string) $question->description,                          // K Mô tả
            (string) $question->placeholder,                         // L Placeholder
            $this->formatVisibility($question->visibility),          // M Điều kiện hiển thị
            $this->formatOptions($question),                         // N Đáp án
        ];

        // Đệ quy câu hỏi con
        $children = $question->relationLoaded('children')
            ? $question->children
            : $question->children()->orderBy('position')->with('options')->get();

        foreach ($children->sortBy('position') as $child) {
            $this->collectQuestionRows($records, $stt, $template, $sectionLabel, $groupLabel, $child, $level + 1);
        }
    }

    /** Gộp các ô liên tiếp cùng giá trị (theo key) trong 1 cột */
    private function mergeColumn($sheet, array $records, string $col, callable $keyFn): void
    {
        $total = count($records);
        $start = 0;
        while ($start < $total) {
            $key = $keyFn($records[$start]);
            $end = $start;
            while ($end + 1 < $total && $keyFn($records[$end + 1]) === $key) {
                $end++;
            }
            if ($end > $start) {
                // +2 vì dữ liệu bắt đầu ở dòng 2
                $sheet->mergeCells($col . ($start + 2) . ':' . $col . ($end + 2));
                $sheet->getStyle($col . ($start + 2))->getAlignment()->setVertical(Alignment::VERTICAL_CENTER);
            }
            $start = $end + 1;
        }
    }

    /** Lọc câu hỏi cấp cao nhất (không phải câu hỏi con) */
    private function topLevel($questions)
    {
        return $questions->whereNull('parent_question_id')->sortBy('position')->values();
    }

    /** Đếm tổng câu hỏi (kể cả câu hỏi con) của 1 phiếu */
    private function countQuestions(FormTemplate $template): int
    {
        return $template->questions()->count();
    }

    /** "1. Tiêu đề" — ghép position + title */
    private function positionTitle($position, $title): string
    {
        $title = (string) $title;
        if ($position === null || $position === '') {
            return $title;
        }
        return trim($position . '. ' . $title);
    }

    /** Định dạng điều kiện hiển thị thành chuỗi đọc được */
    private function formatVisibility($visibility): string
    {
        if (empty($visibility)) {
            return '';
        }
        if (is_array($visibility)) {
            $code = (string) ($visibility['ifQuestionCode'] ?? ($visibility['question'] ?? ''));
            // Không có câu hỏi tham chiếu -> coi như không có điều kiện
            if ($code === '') {
                return '';
            }
            $op = (string) ($visibility['operator'] ?? '');
            $val = $visibility['value'] ?? '';
            $valStr = is_array($val) ? implode(', ', $val) : (string) $val;
            return trim("Nếu [{$code}] {$op} {$valStr}");
        }
        return (string) $visibility;
    }

    /** Gom đáp án thành nhiều dòng "code — label (value)" */
    private function formatOptions($question): string
    {
        $options = $question->relationLoaded('options')
            ? $question->options
            : $question->options()->orderBy('position')->get();

        if ($options->isEmpty()) {
            return '';
        }

        return $options->sortBy('position')->map(function ($opt) {
            $label = (string) $opt->label;
            $parts = [];
            // Chỉ kèm code khi khác label (tránh "Ghi xích — Ghi xích")
            if (!empty($opt->code) && (string) $opt->code !== $label) {
                $parts[] = $opt->code . ' —';
            }
            $parts[] = $label;
            // Chỉ kèm value khi khác cả label và code
            if ($opt->value !== null && $opt->value !== '' && (string) $opt->value !== $label && (string) $opt->value !== (string) $opt->code) {
                $parts[] = '(' . $opt->value . ')';
            }
            return trim(implode(' ', $parts));
        })->implode("\n");
    }

    /** Style hàng tiêu đề */
    private function writeHeaderRow($sheet, array $headers): void
    {
        foreach ($headers as $i => $header) {
            $col = $this->colLetter($i);
            $sheet->setCellValue($col . '1', $header);
        }
        $lastCol = $this->colLetter(count($headers) - 1);
        $sheet->getStyle('A1:' . $lastCol . '1')->applyFromArray([
            'font' => ['name' => 'Times New Roman', 'bold' => true, 'size' => 11],
            'fill' => ['fillType' => Fill::FILL_SOLID, 'startColor' => ['rgb' => 'D9E1F2']],
            'borders' => ['allBorders' => ['borderStyle' => Border::BORDER_THIN]],
            'alignment' => ['horizontal' => Alignment::HORIZONTAL_CENTER, 'vertical' => Alignment::VERTICAL_CENTER, 'wrapText' => true],
        ]);
        $sheet->getRowDimension(1)->setRowHeight(28);
        $sheet->freezePane('A2');
    }

    /** Style vùng dữ liệu */
    private function styleBody($sheet, string $range): void
    {
        $sheet->getStyle($range)->applyFromArray([
            'font' => ['name' => 'Times New Roman', 'size' => 11],
            'borders' => ['allBorders' => ['borderStyle' => Border::BORDER_THIN]],
            'alignment' => ['vertical' => Alignment::VERTICAL_TOP],
        ]);
    }

    /** Chỉ số cột (0-based) -> chữ cái cột Excel */
    private function colLetter(int $index): string
    {
        return \PhpOffice\PhpSpreadsheet\Cell\Coordinate::stringFromColumnIndex($index + 1);
    }

    /** Xác định đường dẫn lưu file, tạo thư mục nếu chưa có */
    private function resolvePath(): string
    {
        $path = $this->option('path');
        if (!$path) {
            $dir = storage_path('app/exports');
            if (!is_dir($dir)) {
                mkdir($dir, 0755, true);
            }
            $path = $dir . '/phieu-thu-thap-thong-tin.xlsx';
        }
        return $path;
    }
}
