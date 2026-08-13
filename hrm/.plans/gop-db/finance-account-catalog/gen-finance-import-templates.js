/**
 * Sinh 2 file mẫu import Excel cho phân hệ Tài chính:
 *   - hrm-client/static/Mau_import_tai_khoan.xlsx        (Danh mục tài khoản)
 *   - hrm-client/static/Mau_import_loai_tai_khoan.xlsx   (Danh mục loại tài khoản)
 *
 * Header PHẢI khớp `importColumns` của 2 màn (utils/import-helper.js so khớp theo
 * label đã bỏ thẻ HTML, hoặc theo aliases) — header row là dòng 1, dữ liệu từ dòng 2
 * (2 màn này không set `skip-rows`).
 *
 * Chạy: node scripts/gen-finance-import-templates.js
 */
const path = require('path')
const ExcelJS = require(path.join(__dirname, '..', 'node_modules', 'exceljs'))

const OUT_DIR = path.join(__dirname, '..', 'static')

const HEADER_FILL = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD9E1F2' } }
const BORDER = {
    top: { style: 'thin', color: { argb: 'FFB0B0B0' } },
    left: { style: 'thin', color: { argb: 'FFB0B0B0' } },
    bottom: { style: 'thin', color: { argb: 'FFB0B0B0' } },
    right: { style: 'thin', color: { argb: 'FFB0B0B0' } },
}

async function build({ fileName, sheetName, columns, rows }) {
    const wb = new ExcelJS.Workbook()
    wb.creator = 'HRM'
    const ws = wb.addWorksheet(sheetName)

    ws.columns = columns.map((c) => ({ header: c.header, key: c.header, width: c.width }))

    const headerRow = ws.getRow(1)
    headerRow.height = 30
    headerRow.eachCell((cell, colIdx) => {
        cell.font = { bold: true, size: 11 }
        cell.fill = HEADER_FILL
        cell.alignment = { vertical: 'middle', horizontal: 'center', wrapText: true }
        cell.border = BORDER
        const note = columns[colIdx - 1].note
        if (note) cell.note = note
    })

    rows.forEach((values) => {
        const row = ws.addRow(values)
        row.eachCell((cell) => {
            cell.border = BORDER
            cell.alignment = { vertical: 'middle', wrapText: true }
            // Giữ số tài khoản / mã ở dạng chuỗi để không mất số 0 đầu.
            if (typeof cell.value === 'string') cell.numFmt = '@'
        })
    })

    ws.views = [{ state: 'frozen', ySplit: 1 }]

    const out = path.join(OUT_DIR, fileName)
    await wb.xlsx.writeFile(out)
    console.log('Đã tạo:', out)
}

async function main() {
    // --- Danh mục tài khoản -------------------------------------------------
    await build({
        fileName: 'Mau_import_tai_khoan.xlsx',
        sheetName: 'DM_taikhoan',
        columns: [
            { header: 'Số tài khoản *', width: 18, note: 'Bắt buộc. Chỉ nhận ký tự số, không được trùng.' },
            { header: 'Tên tài khoản *', width: 40, note: 'Bắt buộc. Tối đa 255 ký tự.' },
            { header: 'Bậc *', width: 10, note: 'Bắt buộc. Chỉ nhận 1, 2 hoặc 3.' },
            {
                header: 'Tài khoản mẹ',
                width: 18,
                note: 'Bắt buộc với tài khoản bậc 2 và 3. Có thể là tài khoản đã có trên hệ thống hoặc tài khoản khai ở dòng khác trong chính file này.',
            },
            {
                header: 'Loại tài khoản *',
                width: 34,
                note: 'Bắt buộc. Nhập MÃ hoặc TÊN loại tài khoản đã có trong danh mục loại tài khoản (vd: TKTS hoặc Tài khoản tài sản).',
            },
            { header: 'Theo dõi công nợ', width: 18, note: 'Để trống hoặc nhập "Có".' },
        ],
        rows: [
            ['8888', 'Tài khoản ví dụ bậc 1', '1', '', 'TKTS', ''],
            ['88881', 'Tài khoản ví dụ bậc 2', '2', '8888', 'TKTS', 'Có'],
            ['888811', 'Tài khoản ví dụ bậc 3', '3', '88881', 'Tài khoản tài sản', ''],
        ],
    })

    // --- Danh mục loại tài khoản -------------------------------------------
    await build({
        fileName: 'Mau_import_loai_tai_khoan.xlsx',
        sheetName: 'DM_loaitaikhoan',
        columns: [
            { header: 'Mã loại tài khoản *', width: 24, note: 'Bắt buộc, không được trùng. Tối đa 255 ký tự.' },
            { header: 'Tên loại tài khoản *', width: 40, note: 'Bắt buộc. Tối đa 255 ký tự.' },
            { header: 'Ghi chú', width: 34, note: 'Không bắt buộc. Tối đa 255 ký tự.' },
            { header: 'Trạng thái', width: 16, note: 'Để trống (mặc định Hoạt động) hoặc nhập "Hoạt động" / "Khóa".' },
        ],
        rows: [
            ['LTK001', 'Loại tài khoản ví dụ 1', 'Ghi chú ví dụ', 'Hoạt động'],
            ['LTK002', 'Loại tài khoản ví dụ 2', '', 'Khóa'],
        ],
    })
}

main().catch((e) => {
    console.error(e)
    process.exit(1)
})
