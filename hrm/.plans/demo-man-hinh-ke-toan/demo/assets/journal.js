/* ============================================================
   Demo Kế toán HRM — Sổ nhật ký chung (S03a-DN TT99/2025 + mở rộng ERP)
   Nguồn cấu trúc: file Mau_So_Nhat_Ky_Chung_TT99_2025.xlsx (user cung cấp)
   - Bảng 21 cột: 9 cột chuẩn TT99 + 4 cột tổ chức (Công ty→Phòng ban→Bộ phận→Nhân viên)
     + 8 chiều phân tích (Khoản mục, Đối tượng, Dự án, Hợp đồng, Hàng hóa, Loại tiền, Tỷ giá, GD nội bộ)
   - Bộ lọc phân cấp cascade + Cộng phát sinh theo bộ lọc + kiểm tra CÂN ĐỐI
   - In sổ theo đúng mẫu chuẩn S03a-DN
   ============================================================ */

/* ---------- Cây tổ chức (cascade Công ty → Phòng ban → Bộ phận → Nhân viên) ----------
   Danh sách công ty lấy từ bảng `companies` của hrm-api (DB hrm_tpe, status=1, bỏ bản ghi test) */
var ORG = {
    'TPE': {
        name: 'CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT',
        depts: {
            'PB-MUA': { name: 'Phòng Mua hàng', parts: { 'BP-MUA01': ['NV-001'] } },
            'PB-KD': { name: 'Phòng Kinh doanh', parts: { 'BP-KD01': ['NV-005'], 'BP-KD02': ['NV-006'] } },
            'PB-HCNS': { name: 'Phòng HCNS', parts: { 'BP-HCNS01': ['NV-010'] } },
            'PB-KT': { name: 'Phòng Kế toán', parts: { 'BP-KT01': ['NV-015'], 'BP-KT02': ['NV-020'] } },
        },
    },
    'TPHP': {
        name: 'CN HẢI PHÒNG - CÔNG TY CP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT',
        depts: {
            'PB-KD': { name: 'Phòng Kinh doanh', parts: { 'BP-KD01': ['NV-201'] } },
            'PB-KT': { name: 'Phòng Kế toán', parts: { 'BP-KT01': ['NV-210'] } },
        },
    },
    'TPV': { name: 'CÔNG TY CP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT- CHI NHÁNH VINH', depts: {} },
    'TPSG': {
        name: 'CÔNG TY TNHH THIẾT BỊ TÂN PHÁT SÀI GÒN',
        depts: {
            'PB-MUA': { name: 'Phòng Mua hàng', parts: { 'BP-MUA01': ['NV-101'] } },
            'PB-KD': { name: 'Phòng Kinh doanh', parts: { 'BP-KD01': ['NV-105'] } },
            'PB-HCNS': { name: 'Phòng HCNS', parts: { 'BP-HCNS01': ['NV-110'] } },
        },
    },
    'ETEK GREEN': { name: 'CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN', depts: {} },
};
var EMP_NAMES = {
    'NV-001': 'Trần Văn Bình', 'NV-005': 'Lê Thị Hoa', 'NV-006': 'Phạm Đức Anh',
    'NV-010': 'Ngô Thu Trang', 'NV-015': 'Vũ Minh Tâm', 'NV-020': 'Đỗ Quang Huy',
    'NV-101': 'Bùi Văn Sơn', 'NV-105': 'Hoàng Lan Chi', 'NV-110': 'Nguyễn Hải Yến',
    'NV-201': 'Phan Văn Đức', 'NV-210': 'Lê Thị Thu',
};

/* ---------- Dữ liệu bút toán mẫu ----------
   17 dòng đầu lấy nguyên từ sheet "Ví dụ có dữ liệu mẫu" (cân đối 785tr);
   bổ sung 8 dòng TPSG (mua nội bộ đối ứng HĐ-IC01, bán hàng, lương) → tổng 1.138tr cân đối.
   [date, docNo, docDate, desc, line, account, debit, credit, company, dept, part, emp,
    item, object, project, contract, goods, currency, rate, internal] */
var JOURNAL_ROWS = [
    ['2026-01-06', 'PN-001', '2026-01-06', 'Mua nguyên vật liệu nhập kho NCC X', 1, '152', 50000000, 0, 'TPE', 'PB-MUA', 'BP-MUA01', 'NV-001', 'KM-NVL', 'NCC-X', '', 'HĐ-M001', 'NVL-001', 'VND', 1, 'N'],
    ['2026-01-06', 'PN-001', '2026-01-06', 'Thuế GTGT đầu vào được khấu trừ', 2, '1331', 5000000, 0, 'TPE', 'PB-MUA', 'BP-MUA01', 'NV-001', 'KM-THUE', 'NCC-X', '', 'HĐ-M001', '', 'VND', 1, 'N'],
    ['2026-01-06', 'PN-001', '2026-01-06', 'Phải trả NCC X', 3, '331', 0, 55000000, 'TPE', 'PB-MUA', 'BP-MUA01', 'NV-001', '', 'NCC-X', '', 'HĐ-M001', '', 'VND', 1, 'N'],
    ['2026-01-10', 'HD-101', '2026-01-10', 'Bán thành phẩm cho KH Y', 4, '131', 110000000, 0, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', '', 'KH-Y', 'VV-001', 'HĐ-B101', 'TP-001', 'VND', 1, 'N'],
    ['2026-01-10', 'HD-101', '2026-01-10', 'Doanh thu bán hàng', 5, '511', 0, 100000000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'KM-DT', 'KH-Y', 'VV-001', 'HĐ-B101', 'TP-001', 'VND', 1, 'N'],
    ['2026-01-10', 'HD-101', '2026-01-10', 'Thuế GTGT đầu ra phải nộp', 6, '3331', 0, 10000000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'KM-THUE', 'KH-Y', '', 'HĐ-B101', '', 'VND', 1, 'N'],
    ['2026-01-15', 'HD-201', '2026-01-15', 'Bán hàng cho TPSG (nội bộ tập đoàn)', 7, '1368', 220000000, 0, 'TPE', 'PB-KD', 'BP-KD02', 'NV-006', '', 'TPSG', '', 'HĐ-IC01', 'TP-002', 'VND', 1, 'Y'],
    ['2026-01-15', 'HD-201', '2026-01-15', 'Doanh thu bán hàng nội bộ', 8, '5111', 0, 200000000, 'TPE', 'PB-KD', 'BP-KD02', 'NV-006', 'KM-DT-NB', 'TPSG', '', 'HĐ-IC01', 'TP-002', 'VND', 1, 'Y'],
    ['2026-01-15', 'HD-201', '2026-01-15', 'Thuế GTGT đầu ra', 9, '3331', 0, 20000000, 'TPE', 'PB-KD', 'BP-KD02', 'NV-006', 'KM-THUE', 'TPSG', '', 'HĐ-IC01', '', 'VND', 1, 'Y'],
    ['2026-01-25', 'BL-01', '2026-01-25', 'Tính lương phải trả CBCNV tháng 01', 10, '6421', 80000000, 0, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-01-25', 'BL-01', '2026-01-25', 'Phải trả người lao động', 11, '334', 0, 80000000, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-01-31', 'PB-01', '2026-01-31', 'Trích khấu hao TSCĐ tháng 01', 12, '6424', 15000000, 0, 'TPE', 'PB-KT', 'BP-KT01', 'NV-015', 'KM-KH', '', 'VV-001', '', '', 'VND', 1, 'N'],
    ['2026-01-31', 'PB-01', '2026-01-31', 'Hao mòn TSCĐ hữu hình', 13, '2141', 0, 15000000, 'TPE', 'PB-KT', 'BP-KT01', 'NV-015', 'KM-KH', '', 'VV-001', '', '', 'VND', 1, 'N'],
    ['2026-01-31', 'UNC-15', '2026-01-31', 'Chuyển khoản thanh toán NCC X', 14, '331', 55000000, 0, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'NCC-X', '', 'HĐ-M001', '', 'VND', 1, 'N'],
    ['2026-01-31', 'UNC-15', '2026-01-31', 'Tiền gửi ngân hàng VCB', 15, '1121', 0, 55000000, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'NH-VCB', '', '', '', 'VND', 1, 'N'],
    ['2026-01-20', 'PN-005', '2026-01-20', 'Nhập khẩu hàng hóa từ NCC nước ngoài', 16, '156', 250000000, 0, 'TPSG', 'PB-MUA', 'BP-MUA01', 'NV-101', 'KM-HH', 'NCC-Z', '', 'HĐ-IM01', 'HH-005', 'USD', 25000, 'N'],
    ['2026-01-20', 'PN-005', '2026-01-20', 'Phải trả NCC nước ngoài', 17, '331', 0, 250000000, 'TPSG', 'PB-MUA', 'BP-MUA01', 'NV-101', '', 'NCC-Z', '', 'HĐ-IM01', '', 'USD', 25000, 'N'],
    /* --- bổ sung minh hoạ thêm cho TPSG --- */
    ['2026-01-15', 'PN-B01', '2026-01-15', 'Mua hàng nội bộ từ TPE (nhập kho)', 18, '156', 200000000, 0, 'TPSG', 'PB-MUA', 'BP-MUA01', 'NV-101', 'KM-HH', 'TPE', '', 'HĐ-IC01', 'TP-002', 'VND', 1, 'Y'],
    ['2026-01-15', 'PN-B01', '2026-01-15', 'Thuế GTGT đầu vào được khấu trừ', 19, '1331', 20000000, 0, 'TPSG', 'PB-MUA', 'BP-MUA01', 'NV-101', 'KM-THUE', 'TPE', '', 'HĐ-IC01', '', 'VND', 1, 'Y'],
    ['2026-01-15', 'PN-B01', '2026-01-15', 'Phải trả nội bộ TPE', 20, '3368', 0, 220000000, 'TPSG', 'PB-MUA', 'BP-MUA01', 'NV-101', '', 'TPE', '', 'HĐ-IC01', '', 'VND', 1, 'Y'],
    ['2026-01-22', 'HD-B55', '2026-01-22', 'Bán hàng hóa cho KH W', 21, '131', 88000000, 0, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', '', 'KH-W', 'VV-B01', 'HĐ-B055', 'HH-005', 'VND', 1, 'N'],
    ['2026-01-22', 'HD-B55', '2026-01-22', 'Doanh thu bán hàng', 22, '511', 0, 80000000, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', 'KM-DT', 'KH-W', 'VV-B01', 'HĐ-B055', 'HH-005', 'VND', 1, 'N'],
    ['2026-01-22', 'HD-B55', '2026-01-22', 'Thuế GTGT đầu ra phải nộp', 23, '3331', 0, 8000000, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', 'KM-THUE', 'KH-W', '', 'HĐ-B055', '', 'VND', 1, 'N'],
    ['2026-01-28', 'BL-B01', '2026-01-28', 'Tính lương phải trả CBCNV tháng 01', 24, '6421', 45000000, 0, 'TPSG', 'PB-HCNS', 'BP-HCNS01', 'NV-110', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-01-28', 'BL-B01', '2026-01-28', 'Phải trả người lao động', 25, '334', 0, 45000000, 'TPSG', 'PB-HCNS', 'BP-HCNS01', 'NV-110', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    /* --- bổ sung TPE: thu tiền KH + bán hàng đợt 2 (làm giàu Sổ Cái TK 131) --- */
    ['2026-01-15', 'UNC-05', '2026-01-15', 'Thu tiền khách hàng Y qua NH Techcombank', 26, '1121', 50000000, 0, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'KH-Y', '', 'HĐ-B101', '', 'VND', 1, 'N'],
    ['2026-01-15', 'UNC-05', '2026-01-15', 'Giảm phải thu khách hàng Y', 27, '131', 0, 50000000, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'KH-Y', '', 'HĐ-B101', '', 'VND', 1, 'N'],
    ['2026-01-20', 'HD-115', '2026-01-20', 'Bán hàng cho KH X (đợt 2)', 28, '131', 132000000, 0, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', '', 'KH-X', 'VV-001', 'HĐ-B115', 'TP-001', 'VND', 1, 'N'],
    ['2026-01-20', 'HD-115', '2026-01-20', 'Doanh thu bán hàng', 29, '511', 0, 120000000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'KM-DT', 'KH-X', 'VV-001', 'HĐ-B115', 'TP-001', 'VND', 1, 'N'],
    ['2026-01-20', 'HD-115', '2026-01-20', 'Thuế GTGT đầu ra phải nộp', 30, '3331', 0, 12000000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'KM-THUE', 'KH-X', '', 'HĐ-B115', '', 'VND', 1, 'N'],
    /* --- bổ sung tháng 2/2026 (làm giàu Sổ Cái nhiều kỳ) --- */
    ['2026-02-05', 'HD-130', '2026-02-05', 'Bán thành phẩm cho KH Y (đơn tháng 2)', 31, '131', 165000000, 0, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', '', 'KH-Y', 'VV-001', 'HĐ-B130', 'TP-001', 'VND', 1, 'N'],
    ['2026-02-05', 'HD-130', '2026-02-05', 'Doanh thu bán hàng', 32, '511', 0, 150000000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'KM-DT', 'KH-Y', 'VV-001', 'HĐ-B130', 'TP-001', 'VND', 1, 'N'],
    ['2026-02-05', 'HD-130', '2026-02-05', 'Thuế GTGT đầu ra phải nộp', 33, '3331', 0, 15000000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'KM-THUE', 'KH-Y', '', 'HĐ-B130', '', 'VND', 1, 'N'],
    ['2026-02-12', 'UNC-22', '2026-02-12', 'Thu tiền khách hàng X qua NH Techcombank', 34, '1121', 132000000, 0, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'KH-X', '', 'HĐ-B115', '', 'VND', 1, 'N'],
    ['2026-02-12', 'UNC-22', '2026-02-12', 'Giảm phải thu khách hàng X', 35, '131', 0, 132000000, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'KH-X', '', 'HĐ-B115', '', 'VND', 1, 'N'],
    ['2026-02-18', 'PN-010', '2026-02-18', 'Mua nguyên vật liệu nhập kho NCC X (đợt 2)', 36, '152', 40000000, 0, 'TPE', 'PB-MUA', 'BP-MUA01', 'NV-001', 'KM-NVL', 'NCC-X', '', 'HĐ-M001', 'NVL-001', 'VND', 1, 'N'],
    ['2026-02-18', 'PN-010', '2026-02-18', 'Thuế GTGT đầu vào được khấu trừ', 37, '1331', 4000000, 0, 'TPE', 'PB-MUA', 'BP-MUA01', 'NV-001', 'KM-THUE', 'NCC-X', '', 'HĐ-M001', '', 'VND', 1, 'N'],
    ['2026-02-18', 'PN-010', '2026-02-18', 'Phải trả NCC X', 38, '331', 0, 44000000, 'TPE', 'PB-MUA', 'BP-MUA01', 'NV-001', '', 'NCC-X', '', 'HĐ-M001', '', 'VND', 1, 'N'],
    ['2026-02-25', 'BL-02', '2026-02-25', 'Tính lương phải trả CBCNV tháng 02', 39, '6421', 82000000, 0, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-25', 'BL-02', '2026-02-25', 'Phải trả người lao động', 40, '334', 0, 82000000, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-28', 'PB-02', '2026-02-28', 'Trích khấu hao TSCĐ tháng 02', 41, '6424', 15000000, 0, 'TPE', 'PB-KT', 'BP-KT01', 'NV-015', 'KM-KH', '', 'VV-001', '', '', 'VND', 1, 'N'],
    ['2026-02-28', 'PB-02', '2026-02-28', 'Hao mòn TSCĐ hữu hình', 42, '2141', 0, 15000000, 'TPE', 'PB-KT', 'BP-KT01', 'NV-015', 'KM-KH', '', 'VV-001', '', '', 'VND', 1, 'N'],
    ['2026-02-28', 'UNC-30', '2026-02-28', 'Chuyển khoản thanh toán NCC X (PN-010)', 43, '331', 44000000, 0, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'NCC-X', '', 'HĐ-M001', '', 'VND', 1, 'N'],
    ['2026-02-28', 'UNC-30', '2026-02-28', 'Tiền gửi ngân hàng VCB', 44, '1121', 0, 44000000, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'NH-VCB', '', '', '', 'VND', 1, 'N'],
    ['2026-02-08', 'HD-B60', '2026-02-08', 'Bán hàng hóa cho KH W (đơn tháng 2)', 45, '131', 110000000, 0, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', '', 'KH-W', 'VV-B01', 'HĐ-B060', 'HH-005', 'VND', 1, 'N'],
    ['2026-02-08', 'HD-B60', '2026-02-08', 'Doanh thu bán hàng', 46, '511', 0, 100000000, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', 'KM-DT', 'KH-W', 'VV-B01', 'HĐ-B060', 'HH-005', 'VND', 1, 'N'],
    ['2026-02-08', 'HD-B60', '2026-02-08', 'Thuế GTGT đầu ra phải nộp', 47, '3331', 0, 10000000, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', 'KM-THUE', 'KH-W', '', 'HĐ-B060', '', 'VND', 1, 'N'],
    ['2026-02-20', 'UNC-B05', '2026-02-20', 'Chuyển khoản thanh toán NCC Z', 48, '331', 100000000, 0, 'TPSG', 'PB-KT', 'BP-KT01', 'NV-110', '', 'NCC-Z', '', 'HĐ-IM01', '', 'VND', 1, 'N'],
    ['2026-02-20', 'UNC-B05', '2026-02-20', 'Tiền gửi ngân hàng', 49, '1121', 0, 100000000, 'TPSG', 'PB-KT', 'BP-KT01', 'NV-110', '', 'NH-VCB', '', '', '', 'VND', 1, 'N'],
    ['2026-02-25', 'BL-B02', '2026-02-25', 'Tính lương phải trả CBCNV tháng 02', 50, '6421', 46000000, 0, 'TPSG', 'PB-HCNS', 'BP-HCNS01', 'NV-110', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-25', 'BL-B02', '2026-02-25', 'Phải trả người lao động', 51, '334', 0, 46000000, 'TPSG', 'PB-HCNS', 'BP-HCNS01', 'NV-110', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-12', 'HD-H01', '2026-02-12', 'Doanh thu dịch vụ lắp đặt KH H', 52, '131', 55000000, 0, 'TPHP', 'PB-KD', 'BP-KD01', 'NV-201', '', 'KH-H', '', 'HĐ-B201', '', 'VND', 1, 'N'],
    ['2026-02-12', 'HD-H01', '2026-02-12', 'Doanh thu bán hàng và cung cấp DV', 53, '511', 0, 50000000, 'TPHP', 'PB-KD', 'BP-KD01', 'NV-201', 'KM-DT', 'KH-H', '', 'HĐ-B201', '', 'VND', 1, 'N'],
    ['2026-02-12', 'HD-H01', '2026-02-12', 'Thuế GTGT đầu ra phải nộp', 54, '3331', 0, 5000000, 'TPHP', 'PB-KD', 'BP-KD01', 'NV-201', 'KM-THUE', 'KH-H', '', 'HĐ-B201', '', 'VND', 1, 'N'],
    ['2026-02-25', 'BL-H01', '2026-02-25', 'Tính lương phải trả CBCNV tháng 02', 55, '6421', 30000000, 0, 'TPHP', 'PB-KT', 'BP-KT01', 'NV-210', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-25', 'BL-H01', '2026-02-25', 'Phải trả người lao động', 56, '334', 0, 30000000, 'TPHP', 'PB-KT', 'BP-KT01', 'NV-210', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    /* --- bổ sung tháng 3/2026 --- */
    ['2026-03-10', 'HD-150', '2026-03-10', 'Bán thành phẩm cho KH Y (đơn tháng 3)', 57, '131', 220000000, 0, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', '', 'KH-Y', 'VV-001', 'HĐ-B150', 'TP-002', 'VND', 1, 'N'],
    ['2026-03-10', 'HD-150', '2026-03-10', 'Doanh thu bán hàng', 58, '511', 0, 200000000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'KM-DT', 'KH-Y', 'VV-001', 'HĐ-B150', 'TP-002', 'VND', 1, 'N'],
    ['2026-03-10', 'HD-150', '2026-03-10', 'Thuế GTGT đầu ra phải nộp', 59, '3331', 0, 20000000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'KM-THUE', 'KH-Y', '', 'HĐ-B150', '', 'VND', 1, 'N'],
    ['2026-03-20', 'UNC-35', '2026-03-20', 'Thu tiền khách hàng Y qua NH Techcombank', 60, '1121', 165000000, 0, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'KH-Y', '', 'HĐ-B130', '', 'VND', 1, 'N'],
    ['2026-03-20', 'UNC-35', '2026-03-20', 'Giảm phải thu khách hàng Y', 61, '131', 0, 165000000, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'KH-Y', '', 'HĐ-B130', '', 'VND', 1, 'N'],
    ['2026-03-25', 'BL-03', '2026-03-25', 'Tính lương phải trả CBCNV tháng 03', 62, '6421', 82000000, 0, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-03-25', 'BL-03', '2026-03-25', 'Phải trả người lao động', 63, '334', 0, 82000000, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'KM-LN', '', '', '', '', 'VND', 1, 'N'],
    /* --- bổ sung chứng từ CHI PHÍ gắn Mã phí (phục vụ Bảng kê chứng từ theo mã phí) ---
       Mỗi phiếu 2 vế cân đối, gắn mã phí cả 2 vế để bảng kê hiện đủ Nợ/Có. */
    ['2026-01-26', 'PC-101', '2026-01-26', 'Công tác phí đi lắp đặt xưởng Garage Thành Công (11-12/01)', 64, '6418', 400000, 0, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'CTP-KTCN', '', 'VV-001', '', '', 'VND', 1, 'N'],
    ['2026-01-26', 'PC-101', '2026-01-26', 'Công tác phí đi lắp đặt xưởng Garage Thành Công (11-12/01)', 65, '1111', 0, 400000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'CTP-KTCN', '', 'VV-001', '', '', 'VND', 1, 'N'],
    ['2026-01-28', 'PC-102', '2026-01-28', 'Vé xe HN - Hải Phòng đi giao hàng bảo hành', 66, '6417', 140000, 0, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'VC-BH', '', '', '', '', 'VND', 1, 'N'],
    ['2026-01-28', 'PC-102', '2026-01-28', 'Vé xe HN - Hải Phòng đi giao hàng bảo hành', 67, '1111', 0, 140000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'VC-BH', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-10', 'PC-110', '2026-02-10', 'Công tác phí đi sửa chữa bảo hành (14/02)', 68, '6418', 800000, 0, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'CTP-KTCN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-10', 'PC-110', '2026-02-10', 'Công tác phí đi sửa chữa bảo hành (14/02)', 69, '1111', 0, 800000, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'CTP-KTCN', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-14', 'PC-115', '2026-02-14', 'Thanh toán tiền điện, nước, viễn thông văn phòng tháng 01', 70, '6427', 3500000, 0, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'DVMN-QL', 'NCC-VNPT', '', '', '', 'VND', 1, 'N'],
    ['2026-02-14', 'PC-115', '2026-02-14', 'Thanh toán tiền điện, nước, viễn thông văn phòng tháng 01', 71, '1111', 0, 3500000, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'DVMN-QL', 'NCC-VNPT', '', '', '', 'VND', 1, 'N'],
    ['2026-02-28', 'PKT-120', '2026-02-28', 'Phân bổ chi phí công cụ dụng cụ văn phòng tháng 02', 72, '6423', 3000000, 0, 'TPE', 'PB-KT', 'BP-KT01', 'NV-015', 'CCDC-QL', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-28', 'PKT-120', '2026-02-28', 'Phân bổ chi phí công cụ dụng cụ văn phòng tháng 02', 73, '242', 0, 3000000, 'TPE', 'PB-KT', 'BP-KT01', 'NV-015', 'CCDC-QL', '', '', '', '', 'VND', 1, 'N'],
    ['2026-03-12', 'PC-130', '2026-03-12', 'Mua văn phòng phẩm, vật tư phục vụ bán hàng', 74, '6417', 1200000, 0, 'TPE', 'PB-KD', 'BP-KD02', 'NV-006', 'VPP-BH', 'NCC-W', '', '', '', 'VND', 1, 'N'],
    ['2026-03-12', 'PC-130', '2026-03-12', 'Mua văn phòng phẩm, vật tư phục vụ bán hàng', 75, '1111', 0, 1200000, 'TPE', 'PB-KD', 'BP-KD02', 'NV-006', 'VPP-BH', 'NCC-W', '', '', '', 'VND', 1, 'N'],
    ['2026-02-20', 'PC-B10', '2026-02-20', 'Công tác phí đi giao hàng khách hàng W', 76, '6418', 600000, 0, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', 'CTP-BH', 'KH-W', '', '', '', 'VND', 1, 'N'],
    ['2026-02-20', 'PC-B10', '2026-02-20', 'Công tác phí đi giao hàng khách hàng W', 77, '1111', 0, 600000, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', 'CTP-BH', 'KH-W', '', '', '', 'VND', 1, 'N'],
    ['2026-03-05', 'PC-B12', '2026-03-05', 'Chi phí vận chuyển hàng hóa nội thành', 78, '6417', 350000, 0, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', 'VC-BH', '', '', '', '', 'VND', 1, 'N'],
    ['2026-03-05', 'PC-B12', '2026-03-05', 'Chi phí vận chuyển hàng hóa nội thành', 79, '1111', 0, 350000, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', 'VC-BH', '', '', '', '', 'VND', 1, 'N'],
    ['2026-02-18', 'PC-H05', '2026-02-18', 'Công tác phí đi lắp đặt thiết bị khách hàng H', 80, '6418', 234000, 0, 'TPHP', 'PB-KD', 'BP-KD01', 'NV-201', 'CTP-KTCN', 'KH-H', '', '', '', 'VND', 1, 'N'],
    ['2026-02-18', 'PC-H05', '2026-02-18', 'Công tác phí đi lắp đặt thiết bị khách hàng H', 81, '1111', 0, 234000, 'TPHP', 'PB-KD', 'BP-KD01', 'NV-201', 'CTP-KTCN', 'KH-H', '', '', '', 'VND', 1, 'N'],
];

/* ---------- Danh mục tên tài khoản + số dư đầu năm (phục vụ Sổ Cái) ---------- */
var ACC_NAMES = {
    '1111': 'Tiền mặt (VNĐ)',
    '1121': 'Tiền gửi ngân hàng — VNĐ',
    '131': 'Phải thu của khách hàng',
    '1331': 'Thuế GTGT được khấu trừ của hàng hóa, dịch vụ',
    '1368': 'Phải thu nội bộ khác',
    '152': 'Nguyên liệu, vật liệu',
    '156': 'Hàng hóa',
    '2141': 'Hao mòn TSCĐ hữu hình',
    '242': 'Chi phí trả trước',
    '331': 'Phải trả cho người bán',
    '3331': 'Thuế GTGT phải nộp',
    '334': 'Phải trả người lao động',
    '3368': 'Phải trả nội bộ khác',
    '511': 'Doanh thu bán hàng và cung cấp dịch vụ',
    '5111': 'Doanh thu bán hàng hóa',
    '6417': 'Chi phí dịch vụ mua ngoài (bán hàng)',
    '6418': 'Chi phí bằng tiền khác (bán hàng)',
    '6421': 'Chi phí nhân viên quản lý',
    '6423': 'Chi phí đồ dùng văn phòng (quản lý)',
    '6424': 'Chi phí khấu hao TSCĐ',
    '6427': 'Chi phí dịch vụ mua ngoài (quản lý)',
};
/* Tính chất TK: dư Nợ (đầu 1,2,6,8) / dư Có (đầu 3,4,5,7) */
function isDebitNature(acc) { return /^[1268]/.test(acc); }
/* Số dư đầu năm 2026 theo Công ty × TK (demo) */
var OPENING = {
    'TPE': { '131': 500000000, '1121': 800000000, '152': 120000000, '331': 150000000, '334': 0 },
    'TPSG': { '131': 200000000, '1121': 400000000, '156': 90000000, '331': 60000000 },
    'TPHP': { '131': 80000000, '1121': 150000000, '331': 30000000 },
};
function openingOf(company, acc) { return (OPENING[company] && OPENING[company][acc]) || 0; }
var JR = { date: 0, docNo: 1, docDate: 2, desc: 3, line: 4, account: 5, debit: 6, credit: 7, company: 8, dept: 9, part: 10, emp: 11, item: 12, object: 13, job: 14, contract: 15, goods: 16, currency: 17, rate: 18, internal: 19 };

/* ---------- Sắp xếp chuẩn kế toán (Luật KT 2015 + hình thức Nhật ký chung) ----------
   Ngày ghi sổ → Ngày chứng từ → Số chứng từ → thứ tự dòng trong chứng từ (Nợ trước, Có sau).
   Đánh lại STT dòng liên tục theo thứ tự mới — Sổ Cái (STT/Trang NKC, link ?line=) dẫn xuất
   từ cùng JOURNAL_ROWS nên tự khớp. */
JOURNAL_ROWS.sort(function (a, b) {
    if (a[JR.date] !== b[JR.date]) return a[JR.date] < b[JR.date] ? -1 : 1;
    if (a[JR.docDate] !== b[JR.docDate]) return a[JR.docDate] < b[JR.docDate] ? -1 : 1;
    if (a[JR.docNo] !== b[JR.docNo]) return a[JR.docNo] < b[JR.docNo] ? -1 : 1;
    return a[JR.line] - b[JR.line];
});
JOURNAL_ROWS.forEach(function (r, i) { r[JR.line] = i + 1; });

/* Vụ việc: Mã — Tên (cột 14, thay cột Dự án cũ) */
var JOB_NAMES = {
    'VV-001': 'Lắp đặt xưởng dịch vụ Garage Thành Công',
    'VV-B01': 'Cung cấp thiết bị cân chỉnh cho KH W',
};
function jobLabel(code) { return code ? code + ' — ' + (JOB_NAMES[code] || '') : ''; }

/* Danh mục đối tượng: Mã — Tên (dùng chung NKC / Sổ Cái / NK thu-chi).
   Mã nội bộ (TPE/TPSG/...) lấy tên từ ORG; mã nhân viên (NV-*) lấy từ EMP_NAMES. */
var OBJECT_NAMES = {
    'KH-A': 'Công ty TNHH An Bình',
    'KH-B': 'Công ty CP Bảo Minh',
    'KH-C': 'Công ty TNHH Cường Thịnh',
    'KH-D': 'Công ty CP Đại Dương',
    'KH-H': 'Công ty TNHH Hải Đăng',
    'KH-W': 'Công ty TNHH Wintech Việt Nam',
    'KH-X': 'Công ty CP Xuân Phát',
    'KH-Y': 'Công ty TNHH Yên Bình',
    'NCC-X': 'Công ty CP Thiết bị Xuân Hòa',
    'NCC-Y': 'Công ty TNHH Vật tư Yến Vy',
    'NCC-Z': 'Zenith Equipment Co., Ltd (nước ngoài)',
    'NCC-W': 'Công ty TNHH Thương mại Vạn Lợi',
    'NCC-CCDC': 'Công ty TNHH CCDC Hòa Phát',
    'NCC-VNPT': 'VNPT Hà Nội (dịch vụ viễn thông)',
    'NH-VCB': 'NH TMCP Ngoại thương VN (Vietcombank)',
    'NH-TCB': 'NH TMCP Kỹ thương VN (Techcombank)',
    'CĐ-01': 'Cổ đông Nguyễn Văn Anh',
};
function objName(code) {
    if (!code) return '';
    if (typeof ORG !== 'undefined' && ORG[code]) return ORG[code].name;
    if (typeof EMP_NAMES !== 'undefined' && EMP_NAMES[code]) return EMP_NAMES[code];
    return OBJECT_NAMES[code] || '';
}
/* Nhãn option cho select lọc Đối tượng / Khách hàng: "Mã — Tên" */
function objOptLabel(code) {
    var n = objName(code);
    return n ? code + ' — ' + n : code;
}

/* ---------- Danh mục MÃ PHÍ (khoản mục chi phí) — phục vụ Bảng kê chứng từ theo mã phí ----------
   Mỗi mã phí có tên + 3 chiều nhóm phí (theo dialog lọc Fast rpt_gldtbkb):
   [tên, Nhóm phí 1 (641/642), Nhóm phí 2 (bản chất), Nhóm phí 3 (bộ phận)] */
var COST_GROUP1 = { 'CPBH': 'Chi phí bán hàng (641)', 'CPQL': 'Chi phí quản lý DN (642)' };
var COST_GROUP2 = { 'CTP': 'Công tác phí', 'DVMN': 'Chi phí dịch vụ mua ngoài', 'VLDC': 'Vật liệu, đồ dùng', 'NC': 'Chi phí nhân công', 'KH': 'Khấu hao TSCĐ', 'CCDC': 'Phân bổ công cụ dụng cụ' };
var COST_GROUP3 = { 'KD': 'Khối kinh doanh', 'KTCN': 'Kỹ thuật công nghệ', 'HCNS': 'Hành chính nhân sự', 'KT': 'Kế toán' };
var COST_CODES = {
    'CTP-KTCN': { name: 'Công tác phí kỹ thuật (bảo hành, lắp đặt)', g1: 'CPBH', g2: 'CTP', g3: 'KTCN' },
    'CTP-BH':   { name: 'Công tác phí bán hàng', g1: 'CPBH', g2: 'CTP', g3: 'KD' },
    'VC-BH':    { name: 'Vận chuyển, vé xe bán hàng', g1: 'CPBH', g2: 'DVMN', g3: 'KD' },
    'VPP-BH':   { name: 'Văn phòng phẩm, vật tư bán hàng', g1: 'CPBH', g2: 'VLDC', g3: 'KD' },
    'DVMN-QL':  { name: 'Dịch vụ mua ngoài (điện, nước, viễn thông)', g1: 'CPQL', g2: 'DVMN', g3: 'HCNS' },
    'CCDC-QL':  { name: 'Phân bổ công cụ dụng cụ văn phòng', g1: 'CPQL', g2: 'CCDC', g3: 'KT' },
    'KM-LN':    { name: 'Chi phí lương nhân viên quản lý', g1: 'CPQL', g2: 'NC', g3: 'HCNS' },
    'KM-KH':    { name: 'Chi phí khấu hao TSCĐ', g1: 'CPQL', g2: 'KH', g3: 'KT' },
};
function isCostCode(code) { return !!(code && COST_CODES[code]); }
function costCodeName(code) { return COST_CODES[code] ? COST_CODES[code].name : ''; }
function costCodeLabel(code) { return code ? code + ' — ' + costCodeName(code) : ''; }

/* Chứng từ CHƯA ghi Sổ Cái (demo cột E + bộ lọc "Đã ghi Sổ Cái") */
var UNPOSTED_DOCS = ['BL-B01'];
function isPosted(r) { return UNPOSTED_DOCS.indexOf(r[JR.docNo]) === -1; }

/* Kỳ báo cáo → khoảng ngày (năm dữ liệu demo: 2026) */
var PERIODS = { 'y': ['2026-01-01', '2026-12-31'] };
['I', 'II', 'III', 'IV'].forEach(function (q, i) {
    var m1 = i * 3 + 1, m3 = i * 3 + 3;
    PERIODS['q' + (i + 1)] = ['2026-' + String(m1).padStart(2, '0') + '-01', '2026-' + String(m3).padStart(2, '0') + '-' + new Date(2026, m3, 0).getDate()];
});
for (var _m = 1; _m <= 12; _m++) {
    PERIODS['m' + _m] = ['2026-' + String(_m).padStart(2, '0') + '-01', '2026-' + String(_m).padStart(2, '0') + '-' + new Date(2026, _m, 0).getDate()];
}

/* ---------- Màn Sổ nhật ký chung ---------- */
function renderJournalPage() {
    function uniq(vals) { return [...new Set(vals.filter(Boolean))].sort(); }
    function selOptions(list, labelFn) {
        return '<option value="">— Tất cả —</option>' + list.map(function (v) {
            return '<option value="' + v + '">' + (labelFn ? labelFn(v) : v) + '</option>';
        }).join('');
    }

    renderShell('journal',
        /* ----- FILTER PANEL ----- */
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Sổ nhật ký chung</p>' +
        '    </div>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="ff-gear" title="Cài đặt trường lọc mặc định / mở rộng">' +
        '        <i class="ri-settings-3-line"></i> Cài đặt bộ lọc</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-toggle">' +
        '        <i class="ri-equalizer-line"></i> Tìm kiếm nâng cao</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-hide" title="Ẩn / hiện toàn bộ khu vực bộ lọc">' +
        '        <i class="ri-eye-off-line"></i> Ẩn bộ lọc</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="filter-body">' +
        '  <div class="quick-search-row">' +
        '    <div class="quick-search">' +
        '      <i class="ri-search-line"></i>' +
        '      <input class="form-control form-control-sm" id="f-search" placeholder="Tìm theo Số CT, Diễn giải, Số hiệu TK">' +
        '      <button type="button" class="btn-clear-quick-search" id="f-search-clear"><i class="ri-close-line"></i></button>' +
        '    </div>' +
        '    <button type="button" class="v2-btn v2-btn--primary btn-compact" id="f-go"><i class="ri-search-line"></i> Tìm kiếm</button>' +
        '    <button type="button" class="v2-btn v2-btn--tertiary btn-compact" id="f-clear"><i class="ri-refresh-line"></i> Nhập lại</button>' +
        '  </div>' +
        /* Trường MẶC ĐỊNH (setupFilterSettings kéo trường được cấu hình vào đây) */
        '  <div class="form-row filter-grid" id="ff-default"></div>' +
        /* Trường MỞ RỘNG tùy chọn — toàn bộ trường render tại đây trước */
        '  <div class="advanced-filters collapsed" id="adv-filters">' +
        '    <div class="form-row filter-grid" id="ff-adv">' +
        '      <div class="col-md-3" data-ff="f-period"><label class="tp-label">Kỳ báo cáo</label>' +
        '        <select class="form-control form-control-sm" id="f-period">' +
        '          <option value="y">Cả năm 2026</option>' +
        '          <optgroup label="Theo quý"><option value="q1">Quý I/2026</option><option value="q2">Quý II/2026</option><option value="q3">Quý III/2026</option><option value="q4">Quý IV/2026</option></optgroup>' +
        '          <optgroup label="Theo tháng">' + Array.from({ length: 12 }, function (_, i) { return '<option value="m' + (i + 1) + '">Tháng ' + (i + 1) + '/2026</option>'; }).join('') + '</optgroup>' +
        '          <option value="custom">Tùy chọn...</option>' +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-from"><label class="tp-label">Từ ngày</label><input type="date" class="form-control form-control-sm" id="f-from" value="2026-01-01"></div>' +
        '      <div class="col-md-3" data-ff="f-to"><label class="tp-label">Đến ngày</label><input type="date" class="form-control form-control-sm" id="f-to" value="2026-12-31"></div>' +
        '      <div class="col-md-3" data-ff="f-account"><label class="tp-label">Tài khoản</label>' +
        '        <select class="form-control form-control-sm" id="f-account"><option value="">— Tất cả —</option>' +
                uniq(JOURNAL_ROWS.map(function (r) { return r[JR.account]; })).map(function (a) { return '<option value="' + a + '">' + a + '</option>'; }).join('') +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-company"><label class="tp-label">Công ty</label>' +
        '        <select class="form-control form-control-sm" id="f-company">' + selOptions(Object.keys(ORG), function (c) { return c + ' — ' + ORG[c].name; }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-dept"><label class="tp-label">Phòng ban</label>' +
        '        <select class="form-control form-control-sm" id="f-dept" disabled><option value="">— Tất cả —</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-part"><label class="tp-label">Bộ phận</label>' +
        '        <select class="form-control form-control-sm" id="f-part" disabled><option value="">— Tất cả —</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-emp"><label class="tp-label">Nhân viên</label>' +
        '        <select class="form-control form-control-sm" id="f-emp" disabled><option value="">— Tất cả —</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-customer"><label class="tp-label">Khách hàng</label><select class="form-control form-control-sm f-adv" id="f-customer">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.object]; })).filter(function (o) { return o.indexOf('KH-') === 0; }), objOptLabel) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-item"><label class="tp-label">Mã phí</label><select class="form-control form-control-sm f-adv" id="f-item">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.item]; }))) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-job"><label class="tp-label">Vụ việc</label><select class="form-control form-control-sm f-adv" id="f-job">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.job]; })), jobLabel) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-object"><label class="tp-label">Đối tượng</label><select class="form-control form-control-sm f-adv" id="f-object">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.object]; })), objOptLabel) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-contract"><label class="tp-label">Hợp đồng</label><select class="form-control form-control-sm f-adv" id="f-contract">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.contract]; }))) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-goods"><label class="tp-label">Hàng hóa</label><select class="form-control form-control-sm f-adv" id="f-goods">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.goods]; }))) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-currency"><label class="tp-label">Loại tiền tệ</label><select class="form-control form-control-sm f-adv" id="f-currency">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.currency]; }))) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-internal"><label class="tp-label">GD nội bộ</label><select class="form-control form-control-sm f-adv" id="f-internal"><option value="">— Tất cả —</option><option value="Y">Y — Nội bộ tập đoàn</option><option value="N">N — Bên ngoài</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-posted"><label class="tp-label">Đã ghi Sổ Cái</label><select class="form-control form-control-sm f-adv" id="f-posted"><option value="">— Tất cả —</option><option value="Y">Đã ghi</option><option value="N">Chưa ghi</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-amt-min"><label class="tp-label">Số tiền từ</label><input class="form-control form-control-sm text-right" id="f-amt-min" placeholder="0"></div>' +
        '      <div class="col-md-3" data-ff="f-amt-max"><label class="tp-label">Số tiền đến</label><input class="form-control form-control-sm text-right" id="f-amt-max" placeholder="Không giới hạn"></div>' +
        '      <div class="col-md-3" data-ff="f-carry" style="display:flex;align-items:flex-end;padding-bottom:6px">' +
        '        <label style="display:inline-flex;align-items:center;gap:6px;font-weight:400;font-size:12.5px;color:#4b5563;margin:0;cursor:pointer">' +
        '        <input type="checkbox" id="f-carry" class="f-adv" style="accent-color:#16a34a"> Hiển thị số lũy kế kỳ trước chuyển sang</label></div>' +
        '    </div>' +
        '  </div>' +
        '  </div>' +
        '</section>' +

        /* ----- DATA TABLE ----- */
        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-book-2-line"></i></div>' +
        '      <div><h5>Sổ nhật ký chung</h5>' +
        '      <p class="tp-section-subtitle">Đơn vị tính: VNĐ</p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In sổ (mẫu S03a-DN)</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-cols" title="Chọn cột hiển thị trên bảng"><i class="ri-layout-column-line"></i> Cấu hình cột</button>' +
        '    </div>' +
        '  </div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="jtbl">' +
        '    <thead><tr id="jtbl-head"></tr></thead>' +
        '    <tbody></tbody>' +
        '    <tfoot></tfoot>' +
        '  </table></div>' +
        '  <div class="table-pager" id="jtbl-pager"></div>' +
        '  <div class="d-flex align-center gap-2 mt-2" id="jtbl-summary"></div>' +
        '</section>' +

        /* ----- Modal In sổ ----- */
        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:1000px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span>In Sổ nhật ký chung — Mẫu số S03a-DN (TT 99/2025/TT-BTC)</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div>' +
        '<div id="print-area"></div>');

    /* ----- Cascade Công ty → Phòng ban → Bộ phận → Nhân viên ----- */
    var fCompany = document.getElementById('f-company');
    var fDept = document.getElementById('f-dept');
    var fPart = document.getElementById('f-part');
    var fEmp = document.getElementById('f-emp');

    function fillSelect(sel, list, labelFn) {
        sel.innerHTML = '<option value="">— Tất cả —</option>' + list.map(function (v) {
            return '<option value="' + v + '">' + (labelFn ? labelFn(v) : v) + '</option>';
        }).join('');
        sel.disabled = !list.length;
    }
    function cascade(level) {
        if (level <= 0) { // đổi công ty → reset 3 cấp dưới
            var c = fCompany.value;
            fillSelect(fDept, c ? Object.keys(ORG[c].depts).map(function (d) { return d; }) : [], function (d) { return d + ' — ' + ORG[c].depts[d].name; });
            if (!c) { fDept.disabled = true; }
        }
        if (level <= 1) {
            var c1 = fCompany.value, d1 = fDept.value;
            fillSelect(fPart, (c1 && d1) ? Object.keys(ORG[c1].depts[d1].parts) : []);
            if (!(c1 && d1)) fPart.disabled = true;
        }
        if (level <= 2) {
            var c2 = fCompany.value, d2 = fDept.value, p2 = fPart.value;
            fillSelect(fEmp, (c2 && d2 && p2) ? ORG[c2].depts[d2].parts[p2] : [], function (e) { return e + ' — ' + (EMP_NAMES[e] || ''); });
            if (!(c2 && d2 && p2)) fEmp.disabled = true;
        }
    }
    fCompany.addEventListener('change', function () { cascade(0); draw(); });
    fDept.addEventListener('change', function () { cascade(1); draw(); });
    fPart.addEventListener('change', function () { cascade(2); draw(); });
    fEmp.addEventListener('change', draw);

    /* toggle tìm kiếm nâng cao */
    var collapsed = true;
    document.getElementById('f-toggle').addEventListener('click', function () {
        collapsed = !collapsed;
        document.getElementById('adv-filters').classList.toggle('collapsed', collapsed);
        updateAdvBadge();
    });

    /* ẩn / hiện toàn bộ khu vực bộ lọc (helper chung, lưu trạng thái theo màn) */
    setupFilterHide({ storageKey: 'demo-filter-journal-hidden', btnId: 'f-hide', bodyId: 'filter-body' });

    /* Kỳ báo cáo → tự set Từ/Đến ngày; sửa ngày tay → chuyển "Tùy chọn" */
    document.getElementById('f-period').addEventListener('change', function () {
        var range = PERIODS[this.value];
        if (range) {
            document.getElementById('f-from').value = range[0];
            document.getElementById('f-to').value = range[1];
        }
        draw();
    });
    ['f-from', 'f-to'].forEach(function (id) {
        document.getElementById(id).addEventListener('change', function () {
            document.getElementById('f-period').value = 'custom';
            draw();
        });
    });
    document.getElementById('f-account').addEventListener('change', draw);

    /* Số tiền từ/đến: format nghìn + lọc ngay khi nhập */
    ['f-amt-min', 'f-amt-max'].forEach(function (id) {
        var inp = document.getElementById(id);
        bindMoneyInput(inp);
        inp.addEventListener('input', draw);
    });

    /* ----- Lọc dữ liệu ----- */
    function val(id) { return document.getElementById(id).value; }
    function matchRow(r, skipDate) {
        var kw = val('f-search').toLowerCase().trim();
        var amtMin = parseMoney(val('f-amt-min'));
        var amtMax = parseMoney(val('f-amt-max'));
        if (val('f-company') && r[JR.company] !== val('f-company')) return false;
        if (val('f-dept') && r[JR.dept] !== val('f-dept')) return false;
        if (val('f-part') && r[JR.part] !== val('f-part')) return false;
        if (val('f-emp') && r[JR.emp] !== val('f-emp')) return false;
        if (!skipDate && val('f-from') && r[JR.date] < val('f-from')) return false;
        if (!skipDate && val('f-to') && r[JR.date] > val('f-to')) return false;
        // TK tổng hợp: chọn 331 lấy cả 3311, 3312... (match theo prefix)
        if (val('f-account') && r[JR.account].indexOf(val('f-account')) !== 0) return false;
        if (val('f-item') && r[JR.item] !== val('f-item')) return false;
        if (val('f-object') && r[JR.object] !== val('f-object')) return false;
        if (val('f-customer') && r[JR.object] !== val('f-customer')) return false;
        if (val('f-job') && r[JR.job] !== val('f-job')) return false;
        if (val('f-contract') && r[JR.contract] !== val('f-contract')) return false;
        if (val('f-goods') && r[JR.goods] !== val('f-goods')) return false;
        if (val('f-currency') && r[JR.currency] !== val('f-currency')) return false;
        if (val('f-internal') && r[JR.internal] !== val('f-internal')) return false;
        if (val('f-posted') && (isPosted(r) ? 'Y' : 'N') !== val('f-posted')) return false;
        var amount = r[JR.debit] || r[JR.credit];
        if (amtMin > 0 && amount < amtMin) return false;
        if (amtMax > 0 && amount > amtMax) return false;
        if (kw && (r[JR.docNo] + ' ' + r[JR.desc] + ' ' + r[JR.account]).toLowerCase().indexOf(kw) === -1) return false;
        return true;
    }
    function applyFilter() {
        return JOURNAL_ROWS.filter(function (r) { return matchRow(r, false); });
    }
    /* Sort theo cột (click header). Không sort → thứ tự chuẩn kế toán (theo STT dòng).
       Bản in mẫu S03a-DN LUÔN theo thứ tự chuẩn, không theo sort cột. */
    var sortState = null;
    var SORT_NUMERIC = { line: 1, debit: 1, credit: 1, rate: 1 };
    function applySort(list) {
        if (!sortState) return list;
        var ji = JR[sortState.key], asc = sortState.dir === 'asc' ? 1 : -1;
        /* cột dẫn xuất không có trong JR (Tên đối tượng) → lấy giá trị qua danh mục */
        function sv(r) { return sortState.key === 'objectName' ? objName(r[JR.object]) : r[ji]; }
        return list.slice().sort(function (a, b) {
            var x = sv(a), y = sv(b);
            if (SORT_NUMERIC[sortState.key]) return (x - y) * asc || a[JR.line] - b[JR.line];
            if (x === y) return a[JR.line] - b[JR.line];
            return (x < y ? -1 : 1) * asc;
        });
    }

    /* ----- Cột hiển thị (header 1 hàng, render động + cấu hình ẩn/hiện) -----
       Các cột chuẩn mẫu S03a-DN + Mã/Tên đối tượng (đặt trước Diễn giải theo yêu cầu)
       là cột cố định đầu bảng → bắt buộc, không cho ẩn. */
    var COLUMNS = [
        { key: 'line', label: 'STT<br>dòng', cls: 'text-center', always: true },
        { key: 'date', label: 'Ngày ghi sổ', always: true },
        { key: 'docNo', label: 'Số CT', always: true },
        { key: 'docDate', label: 'Ngày CT', always: true },
        { key: 'object', label: 'Mã đối tượng', cls: 'text-center', always: true },
        { key: 'objectName', label: 'Tên đối tượng', style: 'min-width:180px', always: true },
        { key: 'desc', label: 'Diễn giải', style: 'min-width:230px', always: true },
        { key: 'account', label: 'Số hiệu<br>TK', cls: 'text-center', always: true },
        { key: 'debit', label: 'Phát sinh Nợ', cls: 'text-right', always: true },
        { key: 'credit', label: 'Phát sinh Có', cls: 'text-right', always: true },
        { key: 'item', label: 'Mã phí' },
        { key: 'job', label: 'Vụ việc', style: 'min-width:200px' },
        { key: 'contract', label: 'Hợp đồng' },
        { key: 'goods', label: 'Hàng hóa' },
        { key: 'currency', label: 'Loại tiền', cls: 'text-center' },
        { key: 'rate', label: 'Tỷ giá', cls: 'text-right' },
        { key: 'internal', label: 'GD nội bộ', cls: 'text-center' },
        { key: 'company', label: 'Công ty' },
        { key: 'dept', label: 'Phòng ban' },
        { key: 'part', label: 'Bộ phận' },
        { key: 'emp', label: 'Nhân viên' },
    ];
    /* Cấu hình cột (helper chung): 8 cột chuẩn khóa đầu bảng, cột mở rộng tick + kéo thả */
    var colCfg = setupColumnConfig({
        storageKey: 'demo-journal-columns',
        btnId: 'btn-cols',
        columns: COLUMNS,
        fixedNote: 'Các cột chuẩn mẫu S03a-DN cùng <b>Mã / Tên đối tượng</b> (đặt trước Diễn giải) là <b>cố định</b> ở đầu bảng.',
        onChange: function () { renderHeader(); draw(); },
    });
    function renderHeader() {
        var visCols = colCfg.visible();
        document.getElementById('jtbl-head').innerHTML = visCols.map(function (c) {
            return '<th' + (c.cls ? ' class="' + c.cls + '"' : '') + (c.style ? ' style="' + c.style + '"' : '') + '>' + c.label + '</th>';
        }).join('');
        if (sortState && !visCols.some(function (c) { return c.key === sortState.key; })) sortState = null;
        setupColumnSort({
            tableSel: '#jtbl',
            headRow: 1,
            cols: visCols.map(function (c) { return { key: c.key }; }),
            onChange: function (s) { sortState = s; draw(); },
        });
    }
    function cellHTML(r, c) {
        switch (c.key) {
            case 'line': return '<td class="text-center">' + r[JR.line] + '</td>';
            case 'date': return '<td class="num">' + fmtDate(r[JR.date]) + '</td>';
            case 'docNo': return '<td><span class="cell-title" style="font-size:12px">' + r[JR.docNo] + '</span>' + (isPosted(r) ? '' : ' <i class="ri-time-line" style="color:#d97706;font-size:13px" title="Chưa ghi Sổ Cái"></i>') + '</td>';
            case 'docDate': return '<td class="num">' + fmtDate(r[JR.docDate]) + '</td>';
            case 'desc': return '<td style="white-space:normal">' + r[JR.desc] + '</td>';
            case 'account': return '<td class="text-center"><b>' + r[JR.account] + '</b></td>';
            case 'debit': return '<td class="text-right num">' + (r[JR.debit] ? fmtMoney(r[JR.debit]) : '') + '</td>';
            case 'credit': return '<td class="text-right num">' + (r[JR.credit] ? fmtMoney(r[JR.credit]) : '') + '</td>';
            case 'objectName': return '<td style="white-space:normal">' + objName(r[JR.object]) + '</td>';
            case 'job': return '<td>' + jobLabel(r[JR.job]) + '</td>';
            case 'currency': return '<td class="text-center">' + r[JR.currency] + '</td>';
            case 'rate': return '<td class="text-right num">' + fmtMoney(r[JR.rate]) + '</td>';
            case 'internal': return '<td class="text-center">' + (r[JR.internal] === 'Y' ? '<span class="status-pill st-paused">Y</span>' : '<span class="status-pill st-none">N</span>') + '</td>';
            case 'emp': return '<td>' + (r[JR.emp] ? '<span title="' + (EMP_NAMES[r[JR.emp]] || '') + '">' + r[JR.emp] + '</span>' : '') + '</td>';
            default: return '<td>' + r[JR[c.key]] + '</td>'; // item, object, contract, goods, company, dept, part
        }
    }
    /* Số lũy kế kỳ trước chuyển sang = tổng các dòng TRƯỚC "Từ ngày" (thoả các điều kiện khác) */
    function carryForward() {
        var from = val('f-from');
        if (!from) return null;
        var d = 0, c = 0, n = 0;
        JOURNAL_ROWS.forEach(function (r) {
            if (r[JR.date] < from && matchRow(r, true)) { d += r[JR.debit]; c += r[JR.credit]; n++; }
        });
        return { debit: d, credit: c, count: n };
    }

    /* Đếm số điều kiện nâng cao đang áp dụng → badge trên nút toggle */
    function updateAdvBadge() {
        var n = ['f-customer', 'f-item', 'f-job', 'f-object', 'f-contract', 'f-goods', 'f-currency', 'f-internal', 'f-posted', 'f-amt-min', 'f-amt-max']
            .filter(function (id) { return String(val(id)).trim() !== ''; }).length;
        if (document.getElementById('f-carry').checked) n++;
        var btn = document.getElementById('f-toggle');
        var label = collapsed ? 'Tìm kiếm nâng cao' : 'Ẩn tìm kiếm nâng cao';
        var icon = collapsed ? 'ri-equalizer-line' : 'ri-arrow-up-s-line';
        btn.innerHTML = '<i class="' + icon + '"></i> ' + label + (n ? ' <span class="adv-count">' + n + '</span>' : '');
    }

    /* ----- Phân trang (helper chung) — mặc định 25 dòng/trang, khớp quy ước "Trang NKC" ----- */
    var pager = createPager({ storageKey: 'demo-journal-pagesize', containerSel: '#jtbl-pager', onChange: function () { draw(); } });
    /* Đổi bộ lọc / sort → tự về trang 1; chuyển trang giữ nguyên bộ lọc */
    function filterSignature() {
        return ['f-search', 'f-company', 'f-dept', 'f-part', 'f-emp', 'f-from', 'f-to', 'f-account',
            'f-customer', 'f-item', 'f-job', 'f-object', 'f-contract', 'f-goods', 'f-currency',
            'f-internal', 'f-posted', 'f-amt-min', 'f-amt-max']
            .map(val).join('|') + '|' + document.getElementById('f-carry').checked + '|' + JSON.stringify(sortState);
    }

    function draw() {
        var list = applyFilter();
        var tbody = document.querySelector('#jtbl tbody');
        var tfoot = document.querySelector('#jtbl tfoot');
        document.getElementById('f-search-clear').style.display = val('f-search') ? 'inline-flex' : 'none';
        var sig = filterSignature();
        var visCols = colCfg.visible();
        if (!list.length) {
            tbody.innerHTML = '<tr><td colspan="' + visCols.length + '"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-2-line"></i></div>Không có bút toán phù hợp bộ lọc.</div></td></tr>';
            tfoot.innerHTML = '';
            document.getElementById('jtbl-summary').innerHTML = '';
            pager.paginate([], sig);
            pager.render();
            return;
        }
        /* Dòng tổng: nhãn span các cột TRƯỚC "Phát sinh Nợ"; Nợ/Có cố định; phần sau "Có" span nốt.
           Tính động theo cấu hình cột (đã đưa Mã/Tên đối tượng vào cột cố định trước Diễn giải). */
        var jkeys = visCols.map(function (c) { return c.key; });
        var lead = jkeys.indexOf('debit');
        var trail = visCols.length - jkeys.indexOf('credit') - 1;
        var trailTd = trail > 0 ? '<td colspan="' + trail + '"></td>' : '';
        var totD = 0, totC = 0;
        list.forEach(function (r) { totD += r[JR.debit]; totC += r[JR.credit]; });
        var totalRow = '<tr class="row-total"><td colspan="' + lead + '">Cộng phát sinh (theo bộ lọc) — ' + list.length + ' dòng</td>' +
            '<td class="text-right num">' + fmtMoney(totD) + '</td>' +
            '<td class="text-right num">' + fmtMoney(totC) + '</td>' +
            trailTd + '</tr>';
        /* Số lũy kế kỳ trước chuyển sang (theo MISA) */
        var carryRow = '', grandRow = '';
        if (document.getElementById('f-carry').checked) {
            var cf = carryForward();
            if (cf) {
                carryRow = '<tr class="row-carry"><td colspan="' + lead + '"><i>Số lũy kế kỳ trước chuyển sang' + (cf.count ? ' (' + cf.count + ' dòng trước ' + fmtDate(val('f-from')) + ')' : '') + '</i></td>' +
                    '<td class="text-right num"><i>' + fmtMoney(cf.debit) + '</i></td>' +
                    '<td class="text-right num"><i>' + fmtMoney(cf.credit) + '</i></td>' +
                    trailTd + '</tr>';
                grandRow = '<tr><td colspan="' + lead + '">Cộng lũy kế từ đầu năm (kỳ trước + kỳ này)</td>' +
                    '<td class="text-right num">' + fmtMoney(cf.debit + totD) + '</td>' +
                    '<td class="text-right num">' + fmtMoney(cf.credit + totC) + '</td>' +
                    trailTd + '</tr>';
            }
        }
        var sorted = applySort(list);
        var pageRows = pager.paginate(sorted, sig);
        tbody.innerHTML = totalRow + carryRow + pageRows.map(function (r) {
            return '<tr data-line="' + r[JR.line] + '">' +
                visCols.map(function (c) { return cellHTML(r, c); }).join('') +
                '</tr>';
        }).join('');
        tfoot.innerHTML = totalRow + grandRow;
        var balanced = totD === totC;
        document.getElementById('jtbl-summary').innerHTML =
            '<span class="tp-small-text">Kiểm tra cân đối Nợ = Có (theo bộ lọc):</span> ' +
            (balanced
                ? '<span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>CÂN ĐỐI</span>'
                : '<span class="status-pill st-cancel"><i class="ri-error-warning-line"></i>LỆCH ' + fmtMoney(Math.abs(totD - totC)) + '</span>') +
            '<span class="tp-small-text" style="margin-left:14px">💡 GD nội bộ = Y: giao dịch giữa các pháp nhân trong tập đoàn, dùng để loại trừ khi hợp nhất báo cáo</span>';
        updateAdvBadge();
        applyStickyTotals('#jtbl');
        pager.render();
    }

    /* filter auto-search: select/date đổi → lọc ngay; keyword cần Enter/nút */
    document.querySelectorAll('.f-adv').forEach(function (el) { el.addEventListener('change', draw); });
    document.getElementById('f-search').addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    document.getElementById('f-search').addEventListener('input', function () {
        document.getElementById('f-search-clear').style.display = this.value ? 'inline-flex' : 'none';
    });
    document.getElementById('f-search-clear').addEventListener('click', function () {
        document.getElementById('f-search').value = ''; draw();
    });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        ['f-search', 'f-company', 'f-account', 'f-customer', 'f-item', 'f-job', 'f-object', 'f-contract', 'f-goods', 'f-currency', 'f-internal', 'f-posted', 'f-amt-min', 'f-amt-max'].forEach(function (id) { document.getElementById(id).value = ''; });
        document.getElementById('f-carry').checked = false;
        document.getElementById('f-period').value = 'y';
        document.getElementById('f-from').value = PERIODS.y[0];
        document.getElementById('f-to').value = PERIODS.y[1];
        cascade(0);
        draw();
    });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });

    /* ----- In sổ theo mẫu chuẩn S03a-DN ----- */
    function printSheetHTML() {
        var list = applyFilter();
        var totD = 0, totC = 0;
        var body = list.map(function (r) {
            totD += r[JR.debit]; totC += r[JR.credit];
            return '<tr>' +
                '<td class="pc">' + fmtDate(r[JR.date]) + '</td>' +
                '<td class="pc">' + r[JR.docNo] + '</td>' +
                '<td class="pc">' + fmtDate(r[JR.docDate]) + '</td>' +
                '<td>' + r[JR.desc] + '</td>' +
                '<td class="pc">✓</td>' +
                '<td class="pc">' + r[JR.line] + '</td>' +
                '<td class="pc">' + r[JR.account] + '</td>' +
                '<td class="pr">' + (r[JR.debit] ? fmtMoney(r[JR.debit]) : '') + '</td>' +
                '<td class="pr">' + (r[JR.credit] ? fmtMoney(r[JR.credit]) : '') + '</td>' +
                '</tr>';
        }).join('');
        var company = val('f-company');
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr>' +
            '<td style="width:55%"><b>Đơn vị:</b> ' + (company ? ORG[company].name : ORG['TPE'].name) + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:center"><b>Mẫu số S03a - DN</b><br><i style="font-size:10.5px">(Ban hành theo Thông tư số 99/2025/TT-BTC<br>ngày 17/10/2025 của Bộ Tài chính)</i></td>' +
            '</tr></table>' +
            '<div class="p-title">SỔ NHẬT KÝ CHUNG</div>' +
            '<div class="p-sub">Năm: 2026' + (val('f-from') || val('f-to') ? ' (Từ ' + fmtDate(val('f-from')) + ' đến ' + fmtDate(val('f-to')) + ')' : '') + '</div>' +
            '<div class="p-unit">Đơn vị tính: VNĐ</div>' +
            '<table class="p-grid">' +
            '<thead>' +
            '<tr><th rowspan="2">Ngày, tháng<br>ghi sổ</th><th colspan="2">Chứng từ</th><th rowspan="2" style="width:26%">Diễn giải</th>' +
            '<th rowspan="2">Đã ghi<br>Sổ Cái</th><th rowspan="2">STT<br>dòng</th><th rowspan="2">Số hiệu<br>TK đối ứng</th><th colspan="2">Số phát sinh</th></tr>' +
            '<tr><th>Số hiệu</th><th>Ngày, tháng</th><th>Nợ</th><th>Có</th></tr>' +
            '<tr class="p-abc"><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>G</th><th>H</th><th>1</th><th>2</th></tr>' +
            '</thead><tbody>' + body +
            '<tr class="p-total"><td colspan="7" style="text-align:left"><b>Cộng phát sinh</b></td>' +
            '<td class="pr"><b>' + fmtMoney(totD) + '</b></td><td class="pr"><b>' + fmtMoney(totC) + '</b></td></tr>' +
            '</tbody></table>' +
            '<div class="p-note">- Sổ này có …. trang, đánh số từ trang số 01 đến trang ….<br>- Ngày mở sổ: ……………</div>' +
            '<table class="p-sign"><tr>' +
            '<td><b>Người ghi sổ</b><br><i>(Ký, họ tên)</i></td>' +
            '<td><b>Kế toán trưởng</b><br><i>(Ký, họ tên)</i></td>' +
            '<td><i>Ngày ... tháng ... năm ...</i><br><b>Người đại diện theo pháp luật</b><br><i>(Ký, họ tên, đóng dấu)</i></td>' +
            '</tr></table>' +
            '</div>';
    }
    document.getElementById('btn-print').addEventListener('click', function () {
        document.getElementById('print-preview').innerHTML = printSheetHTML();
        openModal('print-modal');
    });
    document.getElementById('btn-do-print').addEventListener('click', function () {
        document.getElementById('print-area').innerHTML = printSheetHTML();
        window.print();
    });

    /* Cài đặt bộ lọc: trường mặc định vs mở rộng (lưu localStorage theo màn) */
    setupFilterSettings({
        storageKey: 'demo-filter-journal',
        gearBtnId: 'ff-gear',
        defaultWrap: 'ff-default',
        advWrap: 'ff-adv',
        fields: [
            { id: 'f-period', label: 'Kỳ báo cáo', locked: true },
            { id: 'f-from', label: 'Từ ngày', locked: true },
            { id: 'f-to', label: 'Đến ngày', locked: true },
            { id: 'f-account', label: 'Tài khoản' },
            { id: 'grp-org', label: 'Công ty – Phòng ban – Bộ phận', ids: ['f-company', 'f-dept', 'f-part'] },
            { id: 'f-emp', label: 'Nhân viên' },
            { id: 'f-customer', label: 'Khách hàng' },
            { id: 'f-item', label: 'Mã phí' },
            { id: 'f-job', label: 'Vụ việc' },
            { id: 'f-object', label: 'Đối tượng' },
            { id: 'f-contract', label: 'Hợp đồng' },
            { id: 'f-goods', label: 'Hàng hóa' },
            { id: 'f-currency', label: 'Loại tiền tệ' },
            { id: 'f-internal', label: 'GD nội bộ' },
            { id: 'f-posted', label: 'Đã ghi Sổ Cái' },
            { id: 'f-amt-min', label: 'Số tiền từ' },
            { id: 'f-amt-max', label: 'Số tiền đến' },
            { id: 'f-carry', label: 'Lũy kế kỳ trước chuyển sang' },
        ],
    });

    renderHeader();
    cascade(0);
    draw();

    /* Tham chiếu ngược từ Sổ Cái: ?line=N → nhảy đúng trang chứa dòng, scroll + highlight */
    var lineParam = qs('line');
    if (lineParam) {
        var allSorted = applySort(applyFilter());
        var lineIdx = allSorted.findIndex(function (r) { return String(r[JR.line]) === String(lineParam); });
        if (lineIdx !== -1) {
            pager.goToIndex(lineIdx);
            draw();
        }
        var target = document.querySelector('#jtbl tbody tr[data-line="' + lineParam + '"]');
        if (target) {
            target.classList.add('row-flash');
            target.scrollIntoView({ block: 'center' });
            toast('Tham chiếu từ Sổ Cái — dòng bút toán STT ' + lineParam + ' trên Sổ NKC', 'info');
        }
    }
}
