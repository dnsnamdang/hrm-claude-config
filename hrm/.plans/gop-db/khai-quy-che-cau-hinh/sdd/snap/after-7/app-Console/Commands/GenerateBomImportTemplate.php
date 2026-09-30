<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;
use PhpOffice\PhpSpreadsheet\Style\Alignment;
use PhpOffice\PhpSpreadsheet\Style\Border;
use PhpOffice\PhpSpreadsheet\Style\Fill;

class GenerateBomImportTemplate extends Command
{
    protected $signature = 'bom:generate-import-template';
    protected $description = 'Tạo file mẫu import BOM List';

    public function handle()
    {
        $spreadsheet = new Spreadsheet();
        $sheet = $spreadsheet->getActiveSheet();
        $sheet->setTitle('Data');

        $headers = [
            'STT', 'Tên hàng hoá', 'Mã hàng hoá', 'Model', 'Thương hiệu',
            'Xuất xứ', 'Đơn vị tính', 'Số lượng', 'Đặc điểm',
            'Đơn giá dự toán', 'Đơn giá báo giá',
        ];

        foreach ($headers as $i => $h) {
            $col = chr(65 + $i);
            $sheet->setCellValue($col . '1', $h);
            $sheet->getColumnDimension($col)->setAutoSize(true);
        }

        $sheet->getStyle('A1:K1')->applyFromArray([
            'font' => ['name' => 'Times New Roman', 'bold' => true, 'size' => 11],
            'fill' => ['fillType' => Fill::FILL_SOLID, 'startColor' => ['rgb' => 'D9E1F2']],
            'borders' => ['allBorders' => ['borderStyle' => Border::BORDER_THIN]],
            'alignment' => ['horizontal' => Alignment::HORIZONTAL_CENTER, 'vertical' => Alignment::VERTICAL_CENTER],
        ]);
        $sheet->getRowDimension(1)->setRowHeight(25);

        $sample = ['1', 'PLC Siemens S7-1500', 'HH-00001', '1800QLK', 'KOISU', 'Germany', 'Bộ', 2, 'CPU 1515-2 PN, 750KB work memory', 45000000, 48000000];
        foreach ($sample as $i => $v) {
            $col = chr(65 + $i);
            $sheet->setCellValue($col . '2', $v);
        }
        $sheet->getStyle('A2:K2')->getFont()->setName('Times New Roman')->setSize(11);
        $sheet->getStyle('A2:K2')->getBorders()->getAllBorders()->setBorderStyle(Border::BORDER_THIN);

        $path = public_path('Mau_import_bomlist.xlsx');
        $writer = new Xlsx($spreadsheet);
        $writer->save($path);

        $this->info('Template created: ' . $path);
    }
}
