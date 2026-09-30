<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;
use PhpOffice\PhpSpreadsheet\Style\Alignment;
use PhpOffice\PhpSpreadsheet\Style\Border;
use PhpOffice\PhpSpreadsheet\Style\Fill;

class GenerateBomListTestcase extends Command
{
    protected $signature = 'bom:generate-testcase';
    protected $description = 'Tạo file test case BOM List theo template';

    public function handle()
    {
        $spreadsheet = new Spreadsheet();
        $sheet = $spreadsheet->getActiveSheet();
        $sheet->setTitle('BOM List');

        // Row 1: Title + Summary
        $sheet->setCellValue('A1', 'Testcase _ BOM List');
        $sheet->mergeCells('A1:E1');
        $sheet->setCellValue('F1', 'TEST SUMMARY');
        $sheet->mergeCells('F1:I1');
        $sheet->setCellValue('J1', 'Số trường hợp kiểm thử đạt (P):');
        $sheet->setCellValue('K1', '=COUNTIF(L8:L500,"Passed")');
        $sheet->setCellValue('J2', 'Số trường hợp kiểm thử không đạt (F):');
        $sheet->setCellValue('K2', '=COUNTIF(L8:L500,"Failed")');
        $sheet->setCellValue('J3', 'Số trường hợp kiểm thử đang xem xét (PE):');
        $sheet->setCellValue('K3', '=COUNTIF(L8:L500,"Pending")');
        $sheet->setCellValue('J4', 'Số trường hợp kiểm thử chưa thực hiện:');
        $sheet->setCellValue('K4', '=COUNTIF(L8:L500,"Not Executed")');
        $sheet->setCellValue('J5', 'Tổng số trường hợp kiểm thử:');
        $sheet->setCellValue('K5', '=COUNTA(L8:L500)');

        // Row 6: Headers
        $headers = ['Module', 'Nhóm chức năng', 'TC ID', 'Chức năng', 'Priority', 'Tiền điều kiện', 'Bước thực hiện', 'Test Data', 'Test Data', 'Expected Result (chi tiết)', 'KQ thực tế', 'Status', 'Ghi chú'];
        foreach ($headers as $i => $h) {
            $col = chr(65 + $i);
            $sheet->setCellValue($col . '6', $h);
        }

        $headerStyle = [
            'font' => ['name' => 'Times New Roman', 'bold' => true, 'size' => 11],
            'fill' => ['fillType' => Fill::FILL_SOLID, 'startColor' => ['rgb' => '4472C4']],
            'font' => ['name' => 'Times New Roman', 'bold' => true, 'size' => 11, 'color' => ['rgb' => 'FFFFFF']],
            'borders' => ['allBorders' => ['borderStyle' => Border::BORDER_THIN]],
            'alignment' => ['horizontal' => Alignment::HORIZONTAL_CENTER, 'vertical' => Alignment::VERTICAL_CENTER, 'wrapText' => true],
        ];
        $sheet->getStyle('A6:M6')->applyFromArray($headerStyle);
        $sheet->getRowDimension(6)->setRowHeight(30);

        // Title style
        $sheet->getStyle('A1')->applyFromArray([
            'font' => ['name' => 'Times New Roman', 'bold' => true, 'size' => 14, 'color' => ['rgb' => '1F4E79']],
        ]);

        $module = 'BOM List';
        $group = 'BOM List';
        $tcPrefix = 'BOM';
        $row = 7;

        // Section headers + test cases
        $sections = [
            [
                'title' => 'I. TRANG DANH SÁCH BOM LIST (/assign/bom-list)',
                'cases' => [
                    ['001.001', 'Hiển thị trang danh sách đúng', 'P0', 'User đã đăng nhập, có quyền xem BOM', "1. Truy cập /assign/bom-list\n2. Quan sát layout trang", '', "Hiển thị tiêu đề 'Danh sách BOM List'\nCó bảng dữ liệu với các cột: STT, Mã/Tên BOM, Dự án, Giải pháp, Hạng mục, KH, Loại, Trạng thái, Người tạo, Ngày tạo, Cập nhật"],
                    ['001.002', 'Tìm kiếm nhanh theo mã/tên BOM', 'P0', 'Có nhiều BOM trong hệ thống', "1. Nhập 'PLC' vào ô tìm kiếm nhanh\n2. Bấm Enter hoặc chờ auto search", 'Keyword: PLC', "Chỉ hiển thị BOM có mã/tên chứa 'PLC'"],
                    ['001.003', 'Filter cascading: Dự án → Giải pháp → Hạng mục', 'P0', '', "1. Mở bộ lọc nâng cao\n2. Chọn 1 Dự án TKT\n3. Quan sát Giải pháp\n4. Chọn Hạng mục", '', "Giải pháp tự fill (readonly) theo dự án\nHạng mục enable, hiện DS theo giải pháp\nBỏ chọn dự án → Giải pháp + HM disable"],
                    ['001.004', 'Lọc theo Trạng thái', 'P0', '', "1. Chọn Trạng thái = 'Hoàn thành'\n2. Bấm Tìm kiếm", '', "Chỉ hiển thị BOM status = Hoàn thành"],
                    ['001.005', 'Lọc theo Loại BOM', 'P1', '', "1. Chọn Loại BOM = 'Thành phần'\n2. Bấm Tìm kiếm", '', "Chỉ hiển thị BOM loại Thành phần"],
                    ['001.006', 'Lọc theo Công ty / Phòng ban / Bộ phận', 'P1', '', "1. Chọn Công ty\n2. Chọn Phòng ban\n3. Bấm Tìm kiếm", '', "Chỉ hiển thị BOM thuộc phòng ban đã chọn"],
                    ['001.007', 'Lọc theo khoảng ngày tạo', 'P1', '', "1. Chọn Ngày tạo từ = 01/03/2026\n2. Chọn Đến = 31/03/2026\n3. Bấm Tìm kiếm", 'Từ: 01/03/2026\nĐến: 31/03/2026', "Chỉ hiển thị BOM tạo trong khoảng đã chọn"],
                    ['001.008', 'Reset bộ lọc', 'P1', 'Đã đặt nhiều filter', "1. Bấm nút 'Làm mới'", '', "Tất cả filter về mặc định. Danh sách reload đầy đủ"],
                    ['001.009', 'BOM Đang tạo chỉ hiện cho người tạo', 'P0', 'Có BOM status=1 do user A tạo', "1. Login user B\n2. Truy cập /assign/bom-list", '', "User B không thấy BOM Đang tạo của user A\nUser A thấy BOM Đang tạo của mình"],
                    ['001.010', 'Phân trang + Sort', 'P1', 'Có > 10 BOM', "1. Chuyển trang\n2. Click header 'Ngày tạo' để sort", '', "Phân trang đúng. Sort tăng/giảm hoạt động"],
                    ['001.011', 'Tuỳ chỉnh cột hiển thị', 'P2', '', "1. Click icon tuỳ chỉnh cột\n2. Ẩn 1 cột\n3. Save", '', "Cột đã ẩn biến mất. Reload vẫn giữ cấu hình"],
                    ['001.012', 'Row actions hiện theo điều kiện', 'P0', '', "1. BOM Hoàn thành → có Xem, Sửa, Xuất Excel\n2. BOM Đang tạo (mình tạo) → có Xoá\n3. BOM của người khác → không có Xoá", '', "Actions hiện đúng theo status + quyền"],
                ],
            ],
            [
                'title' => 'II. TẠO BOM LIST (/assign/bom-list/add)',
                'cases' => [
                    ['002.001', 'Chọn Dự án → tự fill Giải pháp + KH', 'P0', '', "1. Chọn 1 Dự án TKT", '', "Giải pháp tự fill (readonly)\nKhách hàng tự fill (disabled)\nHạng mục enable"],
                    ['002.002', 'Tạo BOM Thành phần — Lưu nháp', 'P0', '', "1. Chọn Dự án, nhập Tên BOM\n2. Loại: Thành phần\n3. Thêm nhanh 1 SP cha\n4. Click 'Lưu nháp'", '', "Toast thành công. Redirect danh sách\nDB: status=1\nproduct_projects KHÔNG có record mới"],
                    ['002.003', 'Tạo BOM Thành phần — Lưu', 'P0', '', "1. Tương tự 002.002\n2. Click 'Lưu BOM'", '', "Toast thành công. DB: status=2"],
                    ['002.004', 'Thêm nhanh hàng cha x2 không trùng', 'P0', '', "1. Click 'Thêm nhanh hàng hoá'\n2. Nhập tên, model, brand, origin, ĐVT, SL\n3. Lưu\n4. Lặp lại", '', "Lần 1 OK. Lần 2 code tự tăng, không lỗi trùng"],
                    ['002.005', 'Thêm nhanh hàng con cho cha local', 'P0', '', "1. Thêm nhanh 1 cha (chưa save BOM)\n2. Click 'Thêm nhanh con' trên cha\n3. Nhập thông tin con\n4. Lưu", '', "Con thêm thành công dưới cha. Không lỗi 'cha chưa có trong danh mục'"],
                    ['002.006', 'Chọn hàng hoá từ danh mục', 'P0', '', "1. Click 'Chọn hàng hoá'\n2. Tick SP cha + con\n3. Click 'Áp dụng'\n4. Lưu BOM", '', "SP thêm vào bảng đầy đủ thông tin\nDB: bom_list_products có name, code, product_project_id"],
                    ['002.007', 'Sửa SP trong BOM không ảnh hưởng danh mục', 'P0', '', "1. Click 'Sửa' trên 1 SP\n2. Đổi tên/giá\n3. Lưu BOM\n4. Check product_projects", '', "SP trong BOM đổi. product_projects KHÔNG thay đổi"],
                    ['002.008', 'Xoá SP cha/con', 'P1', '', "1. Xoá 1 SP cha\n2. Xoá 1 SP con", '', "Xoá cha → con cũng mất\nXoá con → cha vẫn còn"],
                    ['002.009', 'Kéo thả đổi thứ tự', 'P2', '', "1. Kéo icon đổi thứ tự cha\n2. Kéo icon đổi thứ tự con", '', "Thứ tự thay đổi, STT cập nhật"],
                    ['002.010', 'company/department/part tự fill', 'P1', '', "1. Tạo BOM + save\n2. Check DB bom_lists", '', "company_id, department_id, part_id từ user đang login"],
                ],
            ],
            [
                'title' => 'III. SỬA BOM LIST (/assign/bom-list/{id}/edit)',
                'cases' => [
                    ['003.001', 'BOM Đang tạo: hiện Lưu nháp + Lưu', 'P0', 'BOM status=1', "1. Mở edit BOM Đang tạo\n2. Quan sát footer", '', "Có cả 2 button: 'Lưu nháp' + 'Lưu BOM'"],
                    ['003.002', 'BOM Hoàn thành: ẩn Lưu nháp', 'P0', 'BOM status=2', "1. Mở edit BOM Hoàn thành\n2. Quan sát footer", '', "Chỉ có 'Lưu BOM'. Không có 'Lưu nháp'"],
                    ['003.003', 'BOM Chờ duyệt/Đã duyệt: form disabled', 'P0', 'BOM status=3 hoặc 4', "1. Mở edit BOM\n2. Quan sát form", '', "Tất cả input disabled. Không có footer bar"],
                    ['003.004', 'Sửa SP → save → reload đúng', 'P0', '', "1. Đổi qty/price SP\n2. Lưu BOM\n3. Mở lại edit", '', "Data hiển thị đúng sau reload"],
                    ['003.005', 'name/code lưu đúng trong DB', 'P0', '', "1. Lưu BOM\n2. Check bom_list_products", '', "Có name, code trong DB (không null)"],
                ],
            ],
            [
                'title' => 'IV. XOÁ BOM LIST',
                'cases' => [
                    ['004.001', 'Xoá BOM Đang tạo + chủ sở hữu', 'P0', 'BOM status=1, created_by = user', "1. Click icon Xoá\n2. Confirm", '', "Toast thành công. BOM biến mất khỏi danh sách"],
                    ['004.002', 'Không xoá BOM Hoàn thành', 'P0', 'BOM status=2', "1. Quan sát row actions", '', "Không hiện icon Xoá"],
                    ['004.003', 'Không xoá BOM của người khác', 'P0', 'BOM do user khác tạo', "1. Quan sát row actions", '', "Không hiện icon Xoá"],
                    ['004.004', 'Confirm modal đúng thông tin', 'P1', '', "1. Click Xoá\n2. Quan sát modal", '', "Hiện mã + tên BOM trong message"],
                ],
            ],
            [
                'title' => 'V. XUẤT EXCEL',
                'cases' => [
                    ['005.001', 'Popup chọn cột xuất', 'P0', '', "1. Click icon Excel trên 1 BOM\n2. Quan sát popup", '', "Popup hiện: checkbox cấp con + danh sách cột\nMặc định chọn tất cả"],
                    ['005.002', 'Select all / Deselect all', 'P1', '', "1. Bỏ tick 'Chọn tất cả'\n2. Tick lại", '', "Bỏ: tất cả cột bỏ chọn\nTick: tất cả cột chọn lại"],
                    ['005.003', 'Xuất có cấp con', 'P0', '', "1. Bật checkbox cấp con\n2. Xuất Excel\n3. Mở file", '', "File có hàng cha + hàng con (STT 1, 1.1, 1.2...)"],
                    ['005.004', 'Xuất không cấp con', 'P0', '', "1. Tắt checkbox cấp con\n2. Xuất Excel\n3. Mở file", '', "File chỉ có hàng cha"],
                    ['005.005', 'Header thông tin BOM đúng', 'P0', '', "1. Xuất Excel\n2. Mở file, xem header", '', "Có: Tên BOM, Mã BOM, Dự án TKT, Giải pháp, Hạng mục, Khách hàng"],
                    ['005.006', 'Format Excel đúng', 'P1', '', "1. Mở file Excel\n2. Kiểm tra format", '', "Font Times New Roman\nAuto-fit column\nSố tiền format #,##0 (dùng được SUM)"],
                    ['005.007', 'Hàng cha/con style đúng', 'P1', '', "1. Mở file Excel\n2. Quan sát style", '', "Cha: bold, nền xanh nhạt\nCon: indent, nền trắng\nDòng cuối: TỔNG CỘNG đúng"],
                    ['005.008', 'Xuất từ trang chi tiết', 'P0', '', "1. Mở /assign/bom-list/{id}\n2. Click 'Xuất Excel' ở footer bar", '', "Popup hiện, xuất thành công"],
                ],
            ],
            [
                'title' => 'VI. IMPORT EXCEL',
                'cases' => [
                    ['006.001', 'Download template mẫu', 'P0', '', "1. Mở edit BOM\n2. Click 'Import Excel'\n3. Click 'Download template'", '', "File .xlsx mở được. Có header + dòng mẫu cha (STT 1) + con (STT 1.1)"],
                    ['006.002', 'Import preview đúng', 'P0', '', "1. Điền data vào template\n2. Upload file\n3. Quan sát preview", '', "Bảng preview hiện đúng số dòng + cột"],
                    ['006.003', 'Validate: thiếu trường bắt buộc', 'P0', '', "1. Bỏ trống tên SP\n2. Click Validate", '', "Lỗi: 'Tên hàng hoá là bắt buộc'\nTương tự cho: Model, Thương hiệu, Xuất xứ, ĐVT, SL"],
                    ['006.004', 'Validate: lookup không tồn tại', 'P0', '', "1. Nhập Model = 'ABCXYZ' (không có trong danh mục)\n2. Validate", '', "Lỗi: 'Model \"ABCXYZ\" không tồn tại trong danh mục'"],
                    ['006.005', 'Validate: thành tiền cha ≠ tổng con', 'P1', '', "1. Cha: giá 100, SL 1 (thành tiền 100)\n2. Con: giá 200, SL 1 (thành tiền 200)\n3. Validate", '', "Cảnh báo: thành tiền cha không bằng tổng con"],
                    ['006.006', 'Import thành công', 'P0', '', "1. Upload file hợp lệ\n2. Validate → all valid\n3. Click Import", '', "Toast thành công. SP thêm vào BOM. Reload đúng"],
                    ['006.007', 'Mã hàng tự sinh', 'P1', '', "1. Bỏ trống cột Mã hàng hoá\n2. Import", '', "Mã tự sinh: HH-XXXXX"],
                    ['006.008', 'Cha/con mapping đúng qua STT', 'P0', '', "1. STT 1 = cha, 1.1 = con\n2. Import\n3. Check DB", '', "bom_list_products: con có parent_id = id của cha"],
                    ['006.009', 'Button Import chỉ hiện BOM Thành phần', 'P1', '', "1. Mở edit BOM Tổng hợp\n2. Quan sát toolbar", '', "Không có nút 'Import Excel'"],
                ],
            ],
            [
                'title' => 'VII. TRANG CHI TIẾT (/assign/bom-list/{id})',
                'cases' => [
                    ['007.001', 'Hiện readonly — không có input', 'P0', '', "1. Truy cập /assign/bom-list/{id}\n2. Quan sát form + bảng", '', "Tất cả field hiện text thuần (không input/textarea)\nSố tiền hiện format"],
                    ['007.002', 'Ẩn tất cả action buttons', 'P0', '', "1. Quan sát toolbar + bảng", '', "Không có: Chọn HH, Import, Thêm nhanh, Sửa, Xoá, kéo thả\nKhông có cột Thao tác"],
                    ['007.003', 'Layout không lệch', 'P0', '', "1. Quan sát bảng chi tiết", '', "Không có cột trống thừa\nCột Model hiện đầy đủ (không bị che)"],
                    ['007.004', 'STT cấp con indent', 'P1', '', "1. Quan sát cột STT", '', "STT con (1.1, 1.2) lùi đầu dòng, font normal\nSTT cha (1, 2) bold"],
                    ['007.005', 'Header card: người tạo + thời gian', 'P1', '', "1. Quan sát góc phải header card", '', "Hiện: [Tên người tạo] — [dd/mm/yyyy HH:mm:ss]"],
                    ['007.006', 'Footer bar: Sửa → edit', 'P0', '', "1. Click 'Sửa' ở footer bar", '', "Navigate sang /assign/bom-list/{id}/edit"],
                    ['007.007', 'Footer bar: Xuất Excel', 'P0', '', "1. Click 'Xuất Excel' ở footer bar", '', "Popup chọn cột hiện, xuất thành công"],
                    ['007.008', 'Form header disabled', 'P1', '', "1. Quan sát form header (tên, dự án, GP...)", '', "Tất cả input/select disabled"],
                ],
            ],
            [
                'title' => 'VIII. BOM TỔNG HỢP (Aggregate)',
                'cases' => [
                    ['008.001', 'Tạo BOM Tổng hợp', 'P0', '', "1. Chọn loại 'Tổng hợp'", '', "'Chọn hàng hoá' disabled\n'Chọn BL con' enable"],
                    ['008.002', 'Chọn BL con', 'P0', 'Có BOM Thành phần', "1. Click 'Chọn BL con'\n2. Chọn BOM\n3. OK", '', "Chip hiện mã + tên BOM con dưới button"],
                    ['008.003', 'Save BOM Tổng hợp', 'P0', '', "1. Chọn BL con\n2. Lưu BOM\n3. Check DB", '', "bom_list_type=2\nbom_list_relations có record child_bom_list_id"],
                    ['008.004', 'Ẩn Import Excel ở BOM Tổng hợp', 'P1', '', "1. Quan sát toolbar", '', "Không có nút 'Import Excel'"],
                    ['008.005', 'Chuyển Thành phần → Tổng hợp', 'P1', '', "1. Đổi loại BOM", '', "Hàng hoá bị clear. BL con enable"],
                    ['008.006', 'Chuyển Tổng hợp → Thành phần', 'P1', '', "1. Đổi loại BOM", '', "BL con bị clear. Hàng hoá enable"],
                    ['008.007', 'Edit BOM Tổng hợp', 'P0', '', "1. Mở edit\n2. BL con hiện đúng\n3. Thêm/bỏ BL con\n4. Save", '', "BL con cập nhật đúng"],
                    ['008.008', 'Detail BOM Tổng hợp', 'P1', '', "1. Mở chi tiết", '', "BL con hiện readonly. Không có 'Chọn BL con'"],
                ],
            ],
        ];

        foreach ($sections as $section) {
            // Section header
            $sheet->setCellValue('C' . $row, $section['title']);
            $sheet->mergeCells('C' . $row . ':M' . $row);
            $sheet->getStyle('A' . $row . ':M' . $row)->applyFromArray([
                'font' => ['name' => 'Times New Roman', 'bold' => true, 'size' => 11, 'color' => ['rgb' => '1F4E79']],
                'fill' => ['fillType' => Fill::FILL_SOLID, 'startColor' => ['rgb' => 'D6E4F0']],
                'borders' => ['allBorders' => ['borderStyle' => Border::BORDER_THIN]],
            ]);
            $row++;

            foreach ($section['cases'] as $tc) {
                $sheet->setCellValue('A' . $row, $module);
                $sheet->setCellValue('B' . $row, $group);
                $sheet->setCellValue('C' . $row, $tcPrefix . '_' . $tc[0]);
                $sheet->setCellValue('D' . $row, $tc[1]);
                $sheet->setCellValue('E' . $row, $tc[2]);
                $sheet->setCellValue('F' . $row, $tc[3]);
                $sheet->setCellValue('G' . $row, $tc[4]);
                $sheet->setCellValue('H' . $row, $tc[5]);
                // I = Test Data 2 (empty)
                $sheet->setCellValue('J' . $row, $tc[6]);
                $sheet->setCellValue('L' . $row, 'Not Executed');

                $sheet->getStyle('A' . $row . ':M' . $row)->applyFromArray([
                    'font' => ['name' => 'Times New Roman', 'size' => 11],
                    'borders' => ['allBorders' => ['borderStyle' => Border::BORDER_THIN]],
                    'alignment' => ['vertical' => Alignment::VERTICAL_TOP, 'wrapText' => true],
                ]);
                $row++;
            }
        }

        // Column widths
        $widths = ['A' => 14, 'B' => 18, 'C' => 16, 'D' => 35, 'E' => 10, 'F' => 30, 'G' => 45, 'H' => 20, 'I' => 12, 'J' => 50, 'K' => 15, 'L' => 14, 'M' => 15];
        foreach ($widths as $col => $w) {
            $sheet->getColumnDimension($col)->setWidth($w);
        }

        // Status dropdown validation
        $validation = $sheet->getCell('L8')->getDataValidation();
        $validation->setType(\PhpOffice\PhpSpreadsheet\Cell\DataValidation::TYPE_LIST);
        $validation->setFormula1('"Passed,Failed,Pending,Not Executed"');
        $validation->setShowDropDown(true);
        for ($r = 8; $r < $row; $r++) {
            $sheet->getCell('L' . $r)->setDataValidation(clone $validation);
        }

        $path = base_path('../docs/test-cases/Testcase_BOM_List.xlsx');
        $writer = new Xlsx($spreadsheet);
        $writer->save($path);

        $this->info('Testcase file created: ' . $path);
        $this->info('Total test cases: ' . ($row - 8 - count($sections)));
    }
}
