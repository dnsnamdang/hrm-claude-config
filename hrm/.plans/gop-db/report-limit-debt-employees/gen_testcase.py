# -*- coding: utf-8 -*-
"""Testcase màn "Báo cáo hạn mức công nợ nhân viên" (phân hệ Tài chính) — skill testcase-documenter (tc_engine).

Chạy: python gen_testcase.py -> testcase.xlsx
03/11/2026: bản đầu theo checklist "Mẫu tài liệu.xlsx" (../phieu-theo-form-quoc-gia/checklist_mau_tai_lieu.json): section
  xếp theo thứ tự nhóm của checklist, BỎ nhóm màn không có (Thêm mới, Chỉnh sửa, Xóa, Khóa/Mở khóa, Lịch sử thay đổi,
  Import Excel, Duyệt, Không duyệt), đánh số liền. Một nhóm Phân quyền duy nhất (role_tcs=[]); case Cài đặt bộ lọc nằm
  trong nhóm Tìm kiếm và lọc. Đối chiếu ở gen_checklist.py. Khuôn: màn chị em ../report-limit-debts/gen_testcase.py.
Nguồn hành vi (đọc 03/11/2026, nhánh develop cả 2 repo): pages/finance/report-limit-debt-employees/{index.vue,
  components/DebtByCustomerModal.vue}, V2BaseSmartFilterPanel, V2BaseCompanyDepartmentFilter, V2BaseDataTable, export-fields-modal,
  column-customization-modal, filterStateMixin, utils/export/listExportFile.js (allowEmpty); BE ReportLimitDebtEmployeeService,
  ReportLimitDebtEmployeeController; form Tài khoản nhân viên (EmployeeForm.vue, Create/UpdateEmployeeRequest).
  Số liệu dev-hrm 03/11/2026 (DNS Admin): 2 nhân viên có hạn mức (DNS01 200, 10410006 6,770,777), công nợ đều 0, cửa sổ chi
  tiết rỗng → các case cần công nợ dùng bộ dữ liệu tester tự khai hạn mức (PRE) + số ERP của #11727/#11730.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_engine import build  # noqa: E402
from tc_phieu_bosung import check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Tài chính > menu "Kế toán công nợ" > nhóm "Nhân viên" > bấm "Báo cáo hạn mức công nợ nhân viên".'
ADV = 'Bấm Tìm kiếm nâng cao.'
EMPTY = '"Không có dữ liệu phù hợp."'
POPT = '"Thông tin chi tiết hạn mức dư nợ nhân viên 11410102 - Chu Khương Duy theo khách hàng"'
ACCF = ('Vào phân hệ Quản trị hệ thống > "Người dùng & phân quyền" > "Tài khoản nhân viên", mở form Sửa tài khoản của nhân viên.')

PRE = ('Tài khoản DNS Admin. Bộ dữ liệu: ở form Tài khoản nhân viên đã khai "Hạn mức công nợ xuất hàng" cho 6 nhân viên, khai sau '
       'cùng trước: 11410102 Chu Khương Duy 47; 41410780 Bùi Thị Thịnh 1,000,000; 19910001 Nguyễn Trung Phong 2,000,000; '
       '10510016 Cao Xuân Khang 50,000,000; DNS01 DNS Admin 200; 10410006 Bùi Thị Phương 6,770,777. Các nhân viên khác chưa khai.')
DUY = ('Nhân viên 11410102 Chu Khương Duy (PHÒNG THIẾT BỊ Ô TÔ 1): ERP báo Tổng công nợ -20,000,000; có hợp đồng đầu kỳ với khách '
       '24TLAPYE-50 (Nợ − Có của riêng khách = -20,000,000) và 19TPHPVI-87 (khách có bút toán ghi sổ sau cùng).')
THINH = ('Nhân viên 41410780 Bùi Thị Thịnh (Kế toán_Hành chính CN Vinh, công ty Chi nhánh Vinh): công nợ hợp đồng đầu kỳ lớn hơn '
         'hạn mức 1,000,000 (ERP khoảng 1,16 tỷ).')
ZERO = 'Nhân viên DNS01 và 10410006 chưa có bút toán công nợ (Tổng công nợ 0).'
ACC_A = 'Tài khoản A: kế toán không được gán quyền nào ở phân hệ Tài chính, thuộc công ty khác công ty của các nhân viên trong bộ dữ liệu.'
P5 = 'Đổi Số dòng/trang = 5.'


SYM = [('ⓘ', '(i)'), ('🔒', 'ổ khóa'), ('⇅', 'hai mũi tên'), ('≤', '<='), ('≥', '>='), ('−', '-'), ('→', 'đến')]


def clean(x):
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    for k, v in SYM:
        x = x.replace(k, v)
    return x


def T(no, func, prio, pre, steps, td, exp):
    func, pre, steps, td, exp = clean(func), clean(pre), clean(steps), clean(td), clean(exp)
    if isinstance(pre, (list, tuple)):
        pre = '\n'.join(pre)
    if isinstance(td, (list, tuple)):
        td = '\n'.join(td)
    st = '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(steps))
    ex = '\n'.join(x if x.startswith('- ') else '- ' + x for x in exp)
    return ('%03d' % no, func, prio, pre, st, td, ex)


def renum(cases):
    return [('%03d' % (i + 1),) + tuple(c[1:]) for i, c in enumerate(cases)]


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Báo cáo liệt kê các nhân viên đã được khai "Hạn mức công nợ xuất hàng" (form Tài khoản nhân viên), kèm bộ phận, phòng ban, '
     'hạn mức và Tổng công nợ khách hàng hiện tại của nhân viên (tính y ERP). Bấm Mã nhân viên mở cửa sổ công nợ theo khách hàng. '
     'Màn chỉ đọc; có Xuất Excel chọn trường, Tùy chỉnh cột, Cài đặt bộ lọc, icon ⓘ giải thích.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Tài khoản nhân viên có hạn mức > 0, mọi công ty, mọi trạng thái.\n'
     '- Công nợ: bút toán tài khoản con của 131, gắn hợp đồng đầu kỳ / thanh lý / dịch vụ / dự án / loại cũ do nhân viên tạo.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Tài khoản chưa khai hạn mức hoặc hạn mức 0.\n'
     '- Bút toán hợp đồng bán hàng, hợp đồng dịch vụ bảo hành (giữ y ERP, #11727).\n'
     '- Màn KHÔNG có Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel, In, Lịch sử thay đổi.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Chỉ "Đến ngày" có tác dụng: công nợ tính tới Đến ngày (bảng, cửa sổ chi tiết, file Excel). "Từ ngày" không đổi số liệu.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Công ty > Phòng ban > Bộ phận > Nhân viên (hạn mức) > công nợ theo khách hàng.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tổng công nợ = Σ Nợ − Σ Có; Trong hạn mức: công nợ < hạn mức; Vượt hạn mức: công nợ > hạn mức; bằng nhau: không thuộc.\n'
     '- Cửa sổ theo khách hàng CỘNG DỒN y ERP (#11729): số của khách là số lũy kế, cộng các dòng không ra tổng; không có dòng tổng.'),
    ('7. Phân quyền cấp',
     '- Màn không gắn quyền, không bó công ty: ai vào được phân hệ Tài chính đều xem được mọi nhân viên có hạn mức.'),
    ('8. Cách tính các ô thống kê',
     'Dòng "Hiển thị a–b / N": N là số nhân viên khớp bộ lọc. Không có ô tổng hợp; cửa sổ chi tiết không có dòng tổng.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: DNS Admin, A (không quyền, công ty khác).\n'
     '- Bộ dữ liệu 6 nhân viên ở tiền điều kiện do tester tự khai ở form Tài khoản nhân viên (dev ngày 03/11 mới có 2 nhân viên).\n'
     '- Lưu ý: bộ lọc giữ khi tải lại trang (10 phút), mất khi rời sang màn khác; số tiền phân cách hàng nghìn bằng dấu phẩy.\n'
     '- Các case "dùng công cụ kiểm thử API" dành cho tester kỹ thuật.'),
]

ORDER6 = '11410102, 41410780, 19910001, 10510016, DNS01, 10410006'

# ============================================================== I. HIỂN THỊ DANH SÁCH VÀ TRUY CẬP
S1 = [
    T(1, 'Mở màn từ menu', 'P0', PRE, ['Đăng nhập.', MENU], '—',
      ['Mở màn "Báo cáo hạn mức công nợ nhân viên".', 'Bảng hiện 6 dòng; dưới bảng "Hiển thị 1–6 / 6".']),
    T(2, 'Tiêu đề màn hình', 'P0', PRE, [MENU, 'Quan sát thanh trên cùng, tab trình duyệt và tiêu đề bảng.', 'Rê chuột vào icon ⓘ cạnh tiêu đề trang.'], '—',
      ['Thanh trên cùng và tab trình duyệt: "Báo cáo hạn mức công nợ nhân viên"; tiêu đề bảng trùng chữ.',
       'Bước 3: hiện khung "Theo dõi công nợ khách hàng hiện tại của từng nhân viên so với hạn mức công nợ xuất hàng được giao, '
       'để phát hiện nhân viên đang vượt hạn mức. …".']),
    T(3, 'Các nút chức năng được hiển thị', 'P0', PRE, [MENU, 'Quan sát khối bộ lọc và thanh công cụ của bảng.'], '—',
      ['Khối bộ lọc: ô "Tìm theo mã hoặc tên nhân viên", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
       'Thanh công cụ: Xuất Excel, nút biểu tượng cột (Cấu hình cột hiển thị).',
       'KHÔNG có nút Thêm mới, Import Excel, Sửa, Xóa, In, Lịch sử.']),
    T(4, 'Các cột mặc định hiển thị', 'P0', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột từ trái sang phải.'], '—',
      ['Đúng 7 cột: STT, Mã nhân viên, Tên nhân viên, Bộ phận, Phòng ban, Hạn mức công nợ xuất hàng, Tổng công nợ khách hàng hiện tại.',
       'STT và Mã nhân viên ghim bên trái khi cuộn ngang; 2 cột tiền có icon ⓘ ở đầu cột.']),
    T(5, 'Không có cột mặc định ẩn', 'P2', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
      ['Cửa sổ "Tuỳ chỉnh cột" tích đủ 7/7 cột, không cột nào ẩn sẵn.']),
    T(6, 'Dữ liệu dòng khớp form Tài khoản nhân viên', 'P0', [PRE, ZERO],
      [MENU, 'Đối chiếu dòng 10410006 với hồ sơ và form Tài khoản nhân viên của Bùi Thị Phương.'], '—',
      ['Mã "10410006" (chữ xanh gạch chân), Tên "Bùi Thị Phương".', 'Bộ phận trống (hồ sơ chưa gắn bộ phận); Phòng ban "BAN ĐIỀU HÀNH".',
       'Hạn mức công nợ xuất hàng "6,770,777" căn phải; Tổng công nợ khách hàng hiện tại "0".']),
    T(7, 'Tổng công nợ âm và dòng không có trạng thái', 'P0', [PRE, DUY], [MENU, 'Quan sát dòng 11410102.'], '—',
      ['Tổng công nợ khách hàng hiện tại hiện "-20,000,000" (có dấu trừ, khớp ERP).',
       'Dòng báo cáo không có cột / nhãn trạng thái (không Khóa / Hoạt động).']),
    T(8, 'Tổng công nợ tính y ERP', 'P0', [PRE, DUY, THINH],
      [MENU, 'So cột Tổng công nợ của 11410102 và 41410780 với màn Báo cáo hạn mức công nợ nhân viên bên ERP (cùng ngày).'], '—',
      ['Hai số trùng ERP từng đồng.', 'Lưu ý: chỉ tính bút toán hợp đồng đầu kỳ / thanh lý / dịch vụ / dự án do nhân viên tạo, không '
       'tính hợp đồng bán hàng — giữ y ERP theo #11727, không phải lỗi.']),
    T(9, 'Danh sách chưa có dữ liệu', 'P1', 'Không tài khoản nhân viên nào có hạn mức > 0 (môi trường mới).', [MENU], '—',
      ['Bảng hiện ' + EMPTY, 'Dưới bảng không có dòng "Hiển thị…" và không có câu "Không có nhân viên nào." (#11928).', 'Không báo lỗi.']),
    T(10, 'Không có dữ liệu phù hợp bộ lọc', 'P1', PRE, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
      ['Bảng hiện ' + EMPTY, 'Dưới bảng để trống.']),
    T(11, 'Số dòng mặc định / trang', 'P1', PRE, [MENU, 'Quan sát ô Số dòng/trang.'], '—', ['Mặc định 10; ô có 5, 10, 20, 50, 100.']),
    T(12, 'Thay đổi số dòng / trang', 'P0', PRE, [MENU, P5], 'Số dòng/trang: 5',
      ['Bảng hiện 5 dòng (11410102 … DNS01).', 'Tự quay về trang 1, "Hiển thị 1–5 / 6"; có 2 trang.']),
    T(13, 'Trang trước / trang tiếp theo', 'P0', PRE, [MENU, P5, 'Bấm nút ›.', 'Bấm nút ‹.'], '—',
      ['Bước 3: trang 2 có 1 dòng 10410006; "Hiển thị 6–6 / 6".', 'Bước 4: về trang 1, "Hiển thị 1–5 / 6".']),
    T(14, 'Trang đầu / trang cuối', 'P1', PRE, [MENU, P5, 'Bấm nút ».', 'Bấm nút «.'], '—',
      ['Bước 3: trang 2 (trang cuối), 1 dòng.', 'Bước 4: về trang 1.']),
    T(15, 'Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE, [MENU, P5, 'Ở trang 1 quan sát « và ‹.', 'Về trang cuối, quan sát › và ».'], '—',
      ['Trang 1: « và ‹ mờ, bấm không tác dụng.', 'Trang cuối: › và » mờ, bấm không tác dụng.']),
    T(16, 'STT liên tục giữa các trang', 'P0', PRE, [MENU, P5, 'Sang trang 2.'], '—', ['Trang 2: STT 6.']),
    T(17, 'Tổng số bản ghi', 'P0', [PRE, THINH], [MENU, 'Đọc dòng dưới bảng.', ADV, 'Chọn Chỉ tiêu vượt hạn mức = Vượt hạn mức.'], '—',
      ['Bước 2: "Hiển thị 1–6 / 6".', 'Bước 4: còn các nhân viên có công nợ > hạn mức, trong đó có 41410780; dòng tổng đếm đúng số dòng còn lại.']),
    T(18, 'Về trang 1 khi thay đổi bộ lọc', 'P0', PRE, [MENU, P5, 'Sang trang 2.', ADV, 'Chọn Chỉ tiêu = Trong hạn mức.'], '—',
      ['Danh sách tự nạp lại ở trang 1, dòng tổng "Hiển thị 1–…" bắt đầu từ 1.']),
    T(19, 'Về trang 1 khi thay đổi số dòng', 'P1', PRE, [MENU, P5, 'Sang trang 2.', 'Đổi Số dòng/trang = 10.'], '—',
      ['Quay về trang 1, "Hiển thị 1–6 / 6".']),
    T(20, 'Sắp xếp mặc định', 'P1', PRE, [MENU, 'Quan sát thứ tự dòng, chưa bấm tiêu đề cột nào.'], '—',
      ['Tài khoản cập nhật gần nhất ở trên: ' + ORDER6 + '.', 'Không cột nào có mũi tên sắp xếp đang bật (biểu tượng ⇅).']),
    T(21, 'Sắp xếp tăng dần theo Hạn mức', 'P0', PRE, [MENU, 'Bấm tiêu đề cột Hạn mức công nợ xuất hàng.'], '—',
      ['Mũi tên lên; thứ tự 11410102 (47), DNS01 (200), 41410780 (1,000,000), 19910001 (2,000,000), 10410006 (6,770,777), 10510016 (50,000,000).']),
    T(22, 'Sắp xếp giảm dần', 'P0', PRE, [MENU, 'Bấm tiêu đề Hạn mức công nợ xuất hàng 2 lần.', 'Bấm tiêu đề Tên nhân viên 2 lần.'], '—',
      ['Bước 2: dòng đầu 10510016 (50,000,000), dòng cuối 11410102 (47).',
       'Bước 3: tên giảm dần theo chữ cái, dòng đầu Nguyễn Trung Phong, dòng cuối Bùi Thị Phương / Bùi Thị Thịnh nhóm cuối.']),
    T(23, 'Sắp xếp theo Mã nhân viên và Tổng công nợ', 'P1', [PRE, DUY, THINH],
      [MENU, 'Bấm tiêu đề Mã nhân viên.', 'Bấm tiêu đề Tổng công nợ khách hàng hiện tại.'], '—',
      ['Bước 2: tăng dần theo mã, so tự nhiên (10410006, 10510016, 11410102, 19910001, 41410780, DNS01).',
       'Bước 3: tăng dần theo công nợ, dòng đầu 11410102 (-20,000,000), dòng cuối 41410780.', 'Màn không có cột Ngày tạo / Ngày cập nhật.']),
    T(24, 'Cột không hỗ trợ sắp xếp', 'P2', PRE, [MENU, 'Bấm tiêu đề STT, Bộ phận, Phòng ban.', 'Bấm icon ⓘ ở đầu cột Hạn mức.'], '—',
      ['Các tiêu đề STT, Bộ phận, Phòng ban không có biểu tượng sắp xếp; bấm không đổi thứ tự.',
       'Bấm icon ⓘ chỉ hiện khung giải thích, không sắp xếp.']),
    T(25, 'Giữ sắp xếp khi chuyển trang', 'P1', PRE, [MENU, P5, 'Bấm tiêu đề Mã nhân viên (tăng dần).', 'Sang trang 2.'], '—',
      ['Trang 2: DNS01 (tiếp thứ tự tăng dần).', 'Mũi tên sắp xếp vẫn ở cột Mã nhân viên.']),
    T(26, 'Về trang 1 khi đổi sắp xếp', 'P1', PRE, [MENU, P5, 'Sang trang 2.', 'Bấm tiêu đề Tên nhân viên.'], '—',
      ['Danh sách quay về trang 1, sắp theo Tên nhân viên tăng dần.']),
    T(27, 'Không có nhân viên chưa khai hạn mức', 'P0', [PRE, 'Nhân viên 10510016 trước khi khai hạn mức có hạn mức trống.'],
      [MENU, 'Tìm "11410101" (nhân viên chưa khai hạn mức).'], '—',
      [EMPTY, 'Chỉ nhân viên có hạn mức > 0 mới lên báo cáo.']),
    T(28, 'Giải thích cột bằng icon ⓘ', 'P1', PRE, [MENU, 'Rê chuột vào icon ⓘ ở đầu cột Hạn mức công nợ xuất hàng.',
                                                   'Rê chuột vào icon ⓘ ở đầu cột Tổng công nợ khách hàng hiện tại.'], '—',
      ['Bước 2: "HẠN MỨC CÔNG NỢ XUẤT HÀNG" + "Mức công nợ khách hàng tối đa nhân viên được phép để tồn khi xuất hàng" + nơi khai.',
       'Bước 3: "TỔNG CÔNG NỢ KHÁCH HÀNG HIỆN TẠI" + công thức Tổng phát sinh Nợ − Tổng phát sinh Có trên các tài khoản con của TK 131 + '
       'điều kiện Trong / Vượt hạn mức.', 'Các cột khác không có icon ⓘ.']),
    T(29, 'Phiên đăng nhập hết hạn khi đang ở báo cáo', 'P2', [PRE, 'Phiên đăng nhập đã hết hạn (đăng xuất ở tab khác).'],
      [MENU, P5, 'Bấm sang trang 2.'], '—', ['Báo "Phiên đăng nhập đã hết hạn".', 'Tự chuyển về màn đăng nhập, không hiện dữ liệu.']),
]

# ============================================================== II. TÌM KIẾM VÀ LỌC
S2 = [
    T(1, 'Tìm theo mã nhân viên chính xác', 'P0', PRE, [MENU, 'Nhập "10410006", bấm Tìm kiếm.'], 'Ô tìm nhanh: 10410006',
      ['Chỉ còn 1 dòng 10410006: "Hiển thị 1–1 / 1".']),
    T(2, 'Tìm theo một phần mã / tên', 'P0', PRE, [MENU, 'Nhập "104100", bấm Tìm kiếm.', 'Đổi thành "Bùi Thị", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: 104100', 'Ô tìm nhanh: Bùi Thị'],
      ['Bước 2: 1 dòng 10410006.', 'Bước 3: 2 dòng 41410780 Bùi Thị Thịnh, 10410006 Bùi Thị Phương.']),
    T(3, 'Không phân biệt hoa / thường', 'P0', PRE, [MENU, 'Nhập "dns01", bấm Tìm kiếm.', 'Nhập "PHƯƠNG", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: dns01', 'Ô tìm nhanh: PHƯƠNG'], ['Bước 2: ra DNS01.', 'Bước 3: ra 10410006 Bùi Thị Phương.']),
    T(4, 'Có dấu / không dấu', 'P1', PRE, [MENU, 'Nhập "Phương", bấm Tìm kiếm.', 'Nhập "phuong", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: Phương', 'Ô tìm nhanh: phuong'], ['Cả 2 lần ra cùng dòng 10410006 Bùi Thị Phương.']),
    T(5, 'Từ khóa không tồn tại', 'P1', PRE, [MENU, 'Nhập "ZZZ999", bấm Tìm kiếm.', 'Nhập "BAN ĐIỀU HÀNH", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: ZZZ999', 'Ô tìm nhanh: BAN ĐIỀU HÀNH'],
      ['Cả 2 lần bảng ' + EMPTY + ' (ô tìm nhanh chỉ theo mã, tên nhân viên, không theo phòng ban).']),
    T(6, 'Ký tự đặc biệt trong ô tìm nhanh', 'P2', PRE, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", rồi "_", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: @#$<>', 'Ô tìm nhanh: %', 'Ô tìm nhanh: _'],
      ['Không lỗi, không treo; cả 3 lần ' + EMPTY, 'Ký tự % và _ được hiểu là ký tự thường (không ra toàn bộ dòng).']),
    T(7, 'Khoảng trắng đầu / cuối từ khóa', 'P1', PRE, [MENU, 'Nhập "  DNS01  ", bấm Tìm kiếm.'], 'Ô tìm nhanh: "  DNS01  "',
      ['Hệ thống bỏ khoảng trắng đầu / cuối, ra 1 dòng DNS01.']),
    T(8, 'Độ dài ô tìm nhanh', 'P2', PRE, [MENU, 'Dán chuỗi 300 ký tự vào ô tìm nhanh, bấm Tìm kiếm.'], 'Chuỗi 300 ký tự chữ và số',
      ['Ô nhận hết chuỗi, không lỗi, không treo.', 'Bảng ' + EMPTY, 'Lưu ý: ô chưa giới hạn số ký tự.']),
    T(9, 'Xóa từ khóa', 'P1', 'Đang tìm "dns01", bảng còn 1 dòng.', ['Bấm nút × trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
      ['Sau bước 1 bảng chưa đổi (ô tìm nhanh chỉ áp khi bấm Tìm kiếm).', 'Sau bước 2 hiện lại đủ 6 dòng.']),
    T(10, 'Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P0', PRE, [MENU, 'Nhập "Bùi Thị", nhấn Enter.', 'Làm mới, nhập lại "Bùi Thị", bấm Tìm kiếm.'],
      'Ô tìm nhanh: Bùi Thị', ['Cả 2 cách đều ra 2 dòng, về trang 1.']),
    T(11, 'Giá trị mặc định của bộ lọc', 'P1', PRE, [MENU, ADV], '—',
      ['Ô tìm nhanh trống; Thời gian, Công ty, Phòng ban, Bộ phận, Nhân viên, Chỉ tiêu vượt hạn mức đều trống.', 'Báo cáo đủ 6 dòng.']),
    T(12, 'Lọc Chỉ tiêu "Trong hạn mức"', 'P0', [PRE, DUY, ZERO], [MENU, ADV, 'Mở ô Chỉ tiêu vượt hạn mức.', 'Chọn "Trong hạn mức".'], '—',
      ['Ô có 2 lựa chọn: Trong hạn mức, Vượt hạn mức.',
       'Còn các nhân viên có Tổng công nợ < Hạn mức, gồm 11410102 (-20,000,000 < 47), DNS01 và 10410006 (0 < hạn mức).']),
    T(13, 'Lọc Chỉ tiêu "Vượt hạn mức"', 'P0', [PRE, THINH, DUY], [MENU, ADV, 'Chọn Chỉ tiêu = "Vượt hạn mức".'], '—',
      ['Có 41410780 (công nợ > 1,000,000).', 'Không có 11410102, DNS01, 10410006.']),
    T(14, 'Công nợ bằng hạn mức không thuộc chỉ tiêu nào', 'P2',
      [PRE, 'Nhân viên DNS01 được sửa hạn mức về đúng bằng Tổng công nợ hiện tại (0 không cho lưu → dùng nhân viên có công nợ dương X, '
            'khai hạn mức = X).'],
      [MENU, ADV, 'Chọn Chỉ tiêu = Trong hạn mức.', 'Chọn Chỉ tiêu = Vượt hạn mức.', 'Bỏ chọn chỉ tiêu.'], '—',
      ['Bước 3 và 4: nhân viên đó không có trong kết quả.', 'Bước 5: nhân viên đó hiện lại.']),
    T(15, 'Lọc Công ty', 'P0', [PRE, THINH], [MENU, ADV, 'Mở ô Công ty.', 'Chọn "CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT- CHI NHÁNH VINH".'], '—',
      ['Bước 3: ô liệt kê mọi công ty (không bó theo công ty người đăng nhập).',
       'Bước 4: chỉ còn nhân viên có hồ sơ thuộc công ty đó, có 41410780; không có DNS01.']),
    T(16, 'Lọc Phòng ban, Bộ phận theo cấp', 'P1', PRE,
      [MENU, ADV, 'Chọn Công ty "CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT".', 'Mở ô Phòng ban, chọn "BAN ĐIỀU HÀNH".', 'Mở ô Bộ phận.',
       'Đổi Công ty sang công ty khác.'], '—',
      ['Bước 4: ô Phòng ban chỉ có phòng ban của công ty đã chọn; chọn xong còn 1 dòng 10410006.',
       'Bước 5: ô Bộ phận chỉ có bộ phận của BAN ĐIỀU HÀNH.', 'Bước 6: Phòng ban, Bộ phận, Nhân viên tự xóa.']),
    T(17, 'Lọc Nhân viên', 'P0', PRE, [MENU, ADV, 'Gõ "Bùi Thị Phương" vào ô Nhân viên.', 'Chọn "Bùi Thị Phương - BDH - 10410006".',
                                       'Chọn nhân viên chưa khai hạn mức.'], '—',
      ['Bước 3: lựa chọn dạng "Tên - Mã phòng - Mã nhân viên".', 'Bước 4: lọc ngay, còn 1 dòng 10410006.', 'Bước 5: ' + EMPTY]),
    T(18, 'Hiện cả đơn vị / nhân viên đã khóa', 'P2', PRE, [MENU, ADV, 'Bấm biểu tượng ổ khóa cạnh nhãn Nhân viên.', 'Mở ô Nhân viên.', 'Bấm lại biểu tượng ổ khóa.'], '—',
      ['Bước 3: danh sách có thêm nhân viên đã nghỉ (có biểu tượng 🔒); di chuột lên biểu tượng hiện "Đang hiện cả nhân viên đã nghỉ đã khoá — bấm để ẩn đi".',
       'Bước 4: nhân viên đã nghỉ ẩn khỏi danh sách.']),
    T(19, 'Lọc Thời gian: chỉ Đến ngày làm mốc', 'P0', [PRE, DUY],
      [MENU, ADV, 'Chọn Thời gian Từ ngày 01/01/2020.', 'Chọn Đến ngày 31/12/2020.', 'Đổi Từ ngày thành 01/06/2020 (giữ Đến ngày).'],
      'Thời gian: 01/01/2020 – 31/12/2020',
      ['Bước 3: chưa nạp lại (mới chọn 1 đầu).', 'Bước 4: nạp lại; Tổng công nợ của 11410102 chỉ tính bút toán tới 31/12/2020.',
       'Bước 5: số liệu không đổi (Từ ngày không ảnh hưởng).', 'Lịch Đến ngày không cho chọn trước Từ ngày.']),
    T(20, 'Kết hợp từ khóa với 1 ô lọc', 'P0', [PRE, THINH], [MENU, 'Nhập "Bùi Thị", bấm Tìm kiếm.', ADV, 'Chọn Chỉ tiêu = Vượt hạn mức.'],
      ['Từ khóa: Bùi Thị', 'Chỉ tiêu: Vượt hạn mức'], ['Còn 1 dòng 41410780.']),
    T(21, 'Kết hợp nhiều ô lọc', 'P0', PRE, [MENU, ADV, 'Chọn Công ty "CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT".', 'Chọn Chỉ tiêu = Trong hạn mức.'],
      ['Công ty: Tân Phát', 'Chỉ tiêu: Trong hạn mức'],
      ['Chỉ còn dòng thỏa CẢ HAI điều kiện: công ty Tân Phát và công nợ < hạn mức (có DNS01, 10410006; không có 41410780).']),
    T(22, 'Kết hợp tìm kiếm không có kết quả', 'P1', PRE, [MENU, 'Nhập "DNS01", bấm Tìm kiếm.', ADV, 'Chọn Chỉ tiêu = Vượt hạn mức.'], '—',
      ['Bảng ' + EMPTY]),
    T(23, 'Tổng số và phân trang sau lọc', 'P0', PRE, [MENU, P5, ADV, 'Chọn Chỉ tiêu = Trong hạn mức.', 'Bấm trang cuối nếu có.'], '—',
      ['Dòng tổng "Hiển thị 1–… / N" với N = số nhân viên Trong hạn mức; số trang = N chia 5 làm tròn lên.']),
    T(24, 'Sắp xếp sau lọc', 'P1', 'Đang lọc Chỉ tiêu = Trong hạn mức.', ['Bấm tiêu đề Hạn mức công nợ xuất hàng 2 lần.'], '—',
      ['Chỉ các dòng Trong hạn mức được sắp giảm dần theo hạn mức; bộ lọc giữ nguyên.']),
    T(25, 'Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "Bùi Thị", lọc Công ty, Chỉ tiêu, Thời gian, sắp theo Tên.',
      ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống; bỏ sắp xếp.', 'Nạp lại từ trang 1, đủ 6 dòng theo thứ tự mặc định.']),
    T(26, 'Chuyển màn rồi quay lại', 'P1', 'Đang lọc Chỉ tiêu = Vượt hạn mức.',
      ['Vào màn Báo cáo hạn mức công nợ khách hàng bằng menu.', 'Quay lại màn báo cáo nhân viên bằng menu.'], '—',
      ['Bộ lọc về trống, hiện đủ 6 dòng.', 'Lưu ý: màn không giữ bộ lọc khi rời sang màn khác — ghi nhận nếu nghiệp vụ yêu cầu giữ.']),
    T(27, 'Tải lại trang (F5) khi đang lọc', 'P1', 'Đang lọc Chỉ tiêu = Vượt hạn mức, khối Tìm kiếm nâng cao đang mở.',
      ['Nhấn F5 trong vòng 10 phút.', 'Đợi quá 10 phút không thao tác, nhấn F5.'], '—',
      ['Bước 1: màn mở lại vẫn giữ Chỉ tiêu = Vượt hạn mức, khối nâng cao vẫn mở.', 'Bước 2: bộ lọc về trống, 6 dòng.']),
    T(28, 'Mở màn trong tab trình duyệt mới', 'P2', 'Đang lọc Chỉ tiêu = Vượt hạn mức ở tab 1 (vừa lọc dưới 10 phút).',
      ['Mở màn Báo cáo hạn mức công nợ nhân viên ở tab mới.'], '—',
      ['Tab mới khôi phục bộ lọc ghi tạm của trình duyệt (Chỉ tiêu = Vượt hạn mức).', 'Lưu ý: bộ lọc ghi tạm dùng chung giữa các tab cùng trình duyệt.']),
    T(29, 'Đổi tài khoản trên cùng trình duyệt', 'P1', 'Tài khoản DNS Admin đang lọc Chỉ tiêu = Vượt hạn mức.',
      ['Đăng xuất.', 'Đăng nhập tài khoản A trên cùng trình duyệt.', MENU], '—',
      ['Rời màn để đăng xuất làm xóa bộ lọc: A thấy bộ lọc trống, đủ 6 dòng.']),
    T(30, 'Khoảng ngày sai khi gọi thẳng', 'P2', PRE,
      ['Dùng công cụ kiểm thử API gọi chức năng lấy báo cáo với Từ ngày 10/10/2026, Đến ngày 01/10/2026.'], '—',
      ['Bị từ chối với thông báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.".', 'Trên giao diện lịch đã chặn chọn ngày sai.']),
    T(31, 'Cài đặt bộ lọc: danh sách tiêu chí', 'P2', PRE, [MENU, 'Bấm Cài đặt bộ lọc.'], '—',
      ['Cửa sổ "Cài đặt bộ lọc" có 3 mục: Thời gian; Công ty – Phòng ban – Bộ phận – Nhân viên; Chỉ tiêu vượt hạn mức.',
       'Có nút Lưu, Khôi phục mặc định, Đóng, (x).']),
    T(32, 'Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Thời gian, bấm Lưu.', ADV], '—',
      ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Thời gian; vẫn còn 4 ô tổ chức và Chỉ tiêu.']),
    T(33, 'Cài đặt bộ lọc: ẩn mục tổ chức thì bày 1 hàng', 'P2', PRE,
      [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích "Công ty – Phòng ban – Bộ phận – Nhân viên" và Thời gian, bấm Lưu.'], '—',
      ['Ô tìm nhanh + Chỉ tiêu bày thẳng trên 1 hàng, không còn nút Tìm kiếm nâng cao.', 'Nút Cài đặt bộ lọc vẫn hiện để bật lại.']),
    T(34, 'Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn Thời gian và mục tổ chức ở case trên.',
      ['Bấm Cài đặt bộ lọc, bấm Khôi phục mặc định, bấm Đóng.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
      ['Bước 1: đóng không lưu, 2 mục vẫn ẩn.', 'Bước 2: tích lại đủ 3 mục, các ô hiện lại.']),
    T(35, 'Cài đặt bộ lọc: kéo đổi thứ tự tiêu chí', 'P2', PRE, [MENU, 'Bấm Cài đặt bộ lọc, kéo Chỉ tiêu vượt hạn mức lên đầu, bấm Lưu.', ADV], '—',
      ['Ô Chỉ tiêu vượt hạn mức đứng đầu khối Tìm kiếm nâng cao.']),
    T(36, 'Cài đặt bộ lọc: ẩn tiêu chí đang có giá trị', 'P2', 'Đang lọc Nhân viên = 10410006 (1 dòng).',
      ['Bấm Cài đặt bộ lọc, bỏ tích "Công ty – Phòng ban – Bộ phận – Nhân viên", bấm Lưu.'], '—',
      ['4 ô tổ chức biến mất, giá trị Nhân viên bị bỏ, báo cáo về 6 dòng.']),
]

# ============================================================== III. XEM CHI TIẾT (CỬA SỔ THEO KHÁCH HÀNG)
OPEN = [MENU, 'Bấm mã "11410102".']
S3 = [
    T(1, 'Mở cửa sổ chi tiết theo khách hàng', 'P0', [PRE, DUY], OPEN, '—',
      ['Mở cửa sổ ' + POPT + ' ngay trên báo cáo (cửa sổ nổi).', 'Bộ lọc trống; bảng chưa sắp (cột Công nợ hiện ⇅).']),
    T(2, 'Tiêu đề cửa sổ', 'P1', [PRE, ZERO], [MENU, 'Bấm mã "DNS01".'], '—',
      ['Tiêu đề "Thông tin chi tiết hạn mức dư nợ nhân viên DNS01 - DNS Admin theo khách hàng".', 'Góc phải tiêu đề có nút (x).']),
    T(3, 'Đầy đủ trường', 'P0', [PRE, DUY], OPEN, '—',
      ['Khối "Bộ lọc công nợ theo khách hàng": ô "Tìm theo mã, tên khách hàng", ô Khách hàng, ô Số tiền (Từ → Đến), nút Tìm kiếm, Làm mới.',
       'Bảng cột STT, Mã khách hàng, Tên khách hàng, Công nợ; không phân trang; không có dòng tổng.', 'Nút Đóng ở chân cửa sổ.']),
    T(4, 'Khớp dữ liệu công nợ với ERP', 'P0', [PRE, DUY], OPEN + ['Mở popup cùng nhân viên ở màn ERP, so từng dòng.'], '—',
      ['Cùng danh sách khách hàng, cùng thứ tự, cùng số Công nợ từng dòng như ERP.',
       'Lưu ý: số mỗi dòng là số cộng dồn qua các khách (giữ y ERP, #11729), không phải nợ riêng của khách.']),
    T(5, 'Khớp với dòng trên báo cáo', 'P0', [PRE, DUY], OPEN, '—',
      ['Tiêu đề đúng mã, tên của dòng đã bấm.',
       'Dòng của khách 19TPHPVI-87 (bút toán ghi sổ sau cùng) có Công nợ -20,000,000 = cột Tổng công nợ của 11410102.',
       'Cộng các dòng KHÔNG ra -20,000,000 (do cộng dồn) — đúng thiết kế.']),
    T(6, 'Trường chỉ đọc', 'P1', [PRE, DUY], OPEN + ['Thử bấm / gõ vào các ô của bảng.'], '—',
      ['Không ô nào của bảng sửa được; chỉ ô lọc và tiêu đề Công nợ thao tác được.']),
    T(7, 'Không có nút Lưu', 'P1', [PRE, DUY], OPEN + ['Quan sát chân cửa sổ.'], '—',
      ['Chỉ có nút Đóng; không có Lưu, Sửa, Xuất Excel, In.']),
    T(8, 'Lọc theo Khách hàng', 'P0', [PRE, DUY], OPEN + ['Mở ô Khách hàng.', 'Chọn "24TLAPYE-50 - …".', 'Bấm × bỏ chọn.'], '—',
      ['Bước 3: lựa chọn dạng "Mã - Tên", đủ mọi khách của nhân viên.',
       'Bước 4: lọc ngay, còn 1 dòng 24TLAPYE-50 với Công nợ -20,000,000 (Nợ − Có của riêng khách).',
       'Bước 5: hiện lại đủ danh sách như lúc mở.']),
    T(9, 'Tìm nhanh trong cửa sổ', 'P0', [PRE, DUY],
      OPEN + ['Nhập "19tphpvi", nhấn Enter.', 'Nhập "ô tô", bấm Tìm kiếm.', 'Nhập "o to", bấm Tìm kiếm.', 'Bấm × trong ô tìm nhanh.'], '—',
      ['Bước 3: còn dòng 19TPHPVI-87, Công nợ giữ nguyên -20,000,000 (lọc sau khi cộng dồn).',
       'Bước 4: các khách có tên chứa "Ô TÔ" (không phân biệt hoa / thường).',
       'Bước 5: ' + EMPTY + ' — ô tìm nhanh của cửa sổ CÓ phân biệt dấu (khác ô tìm nhanh báo cáo).',
       'Bước 6: nạp lại ngay, đủ danh sách.']),
    T(10, 'Lọc Số tiền từ → đến', 'P0', [PRE, DUY], OPEN + ['Nhập Số tiền Từ 0, nhấn Enter.', 'Nhập thêm Đến 1,000,000,000, bấm Tìm kiếm.',
                                                             'Bấm Làm mới.'], 'Số tiền: 0 → 1,000,000,000',
      ['Bước 3: chỉ còn dòng có Công nợ ≥ 0.', 'Bước 4: chỉ còn dòng có 0 ≤ Công nợ ≤ 1,000,000,000 (tính cả 2 đầu).',
       'Bước 5: 3 ô lọc về trống, đủ danh sách.']),
    T(11, 'Sắp xếp cột Công nợ', 'P1', [PRE, DUY], OPEN + ['Bấm tiêu đề Công nợ.', 'Bấm lại.'], '—',
      ['Bước 3: tăng dần, số âm nhỏ nhất lên đầu.', 'Bước 4: giảm dần.', 'Các cột khác không sắp xếp được.']),
    T(12, 'Mốc Đến ngày áp vào cửa sổ', 'P0', [PRE, DUY],
      [MENU, ADV, 'Chọn Thời gian 01/01/2020 – 31/12/2020.', 'Bấm "11410102".'], 'Thời gian: 01/01/2020 – 31/12/2020',
      ['Cửa sổ chỉ tính bút toán có ngày hạch toán tới 31/12/2020.',
       'Khách có bút toán sau cùng (tới 31/12/2020) mang số bằng cột Tổng công nợ của 11410102 cùng mốc.', 'Công nợ có thể âm.']),
    T(13, 'Nhân viên chưa có công nợ', 'P1', [PRE, ZERO], [MENU, 'Bấm "DNS01".'], '—',
      ['Bảng ' + EMPTY, 'Ô Khách hàng không có lựa chọn.']),
    T(14, 'Đóng cửa sổ', 'P0', [PRE, DUY], ['Mở cửa sổ 11410102, chọn Khách hàng 24TLAPYE-50, bấm tiêu đề Công nợ.', 'Bấm Đóng.',
                                            'Mở lại, bấm (x).', 'Mở lại, click ra ngoài cửa sổ.'], '—',
      ['Mỗi lần cửa sổ đóng ngay, không hỏi xác nhận.', 'Lần mở sau bộ lọc trống, bảng chưa sắp.']),
    T(15, 'Giữ trang và bộ lọc khi đóng cửa sổ', 'P1', 'Đang ở trang 2 (5 dòng/trang), sắp theo Mã nhân viên.',
      ['Bấm "DNS01" ở trang 2.', 'Bấm Đóng.'], '—', ['Báo cáo vẫn ở trang 2, giữ sắp xếp và bộ lọc.']),
]

# ============================================================== IV. TÙY CHỈNH CỘT
COL = [MENU, 'Bấm nút biểu tượng cột (Cấu hình cột hiển thị).']
COL_PRE = [PRE, 'Tài khoản chưa từng lưu cấu hình cột.']
S4 = [
    T(1, 'Mở cửa sổ tùy chỉnh cột', 'P1', COL_PRE, COL, '—', ['Mở cửa sổ "Tuỳ chỉnh cột" có nút (x), dòng hướng dẫn.']),
    T(2, 'Danh sách cột', 'P1', COL_PRE, COL, '—',
      ['Đủ 7 cột: STT, Mã nhân viên, Tên nhân viên, Bộ phận, Phòng ban, Hạn mức công nợ xuất hàng, Tổng công nợ khách hàng hiện tại.']),
    T(3, 'Cột được chọn mặc định', 'P1', COL_PRE, COL, '—', ['Cả 7 cột tích; dòng đếm "Đang chọn 7/7 cột".']),
    T(4, 'Hiện cột đang ẩn', 'P0', [PRE, 'Đã ẩn cột Bộ phận.'], COL + ['Tích Bộ phận, bấm Lưu.'], '—',
      ['Báo "Cập nhật thành công".', 'Bảng có lại cột Bộ phận.']),
    T(5, 'Ẩn cột', 'P0', COL_PRE, COL + ['Bỏ tích Bộ phận, bấm Lưu.'], '—', ['Báo "Cập nhật thành công".', 'Bảng không còn cột Bộ phận.']),
    T(6, 'Cột bắt buộc không ẩn được', 'P0', COL_PRE, COL + ['Thử bỏ tích STT, Mã nhân viên; di chuột lên biểu tượng cuối dòng.'], '—',
      ['STT, Mã nhân viên: ô tích xám, biểu tượng ổ khóa, gợi ý "Cột bắt buộc — không thể ẩn hoặc đổi vị trí".']),
    T(7, 'Kéo thả đổi thứ tự cột', 'P1', COL_PRE, COL + ['Kéo Tổng công nợ khách hàng hiện tại lên ngay sau Tên nhân viên, bấm Lưu.'], '—',
      ['Cột Tổng công nợ khách hàng hiện tại (kèm icon ⓘ) đứng ngay sau Tên nhân viên trên bảng.']),
    T(8, 'Cột cố định', 'P2', COL_PRE, COL + ['Thử kéo STT, Mã nhân viên.', 'Đóng cửa sổ, thu hẹp cửa sổ trình duyệt, cuộn bảng sang phải.'], '—',
      ['STT, Mã nhân viên không kéo được.', 'STT, Mã nhân viên ghim trái khi cuộn ngang.']),
    T(9, 'Lưu cấu hình với Chọn tất cả / Bỏ chọn hết', 'P1', COL_PRE, COL + ['Bấm Bỏ chọn hết, bấm Lưu.', 'Mở lại, bấm Chọn tất cả, bấm Lưu.'], '—',
      ['Bước 3: bảng chỉ còn STT, Mã nhân viên.', 'Bước 4: bảng đủ 7 cột.']),
    T(10, 'Đóng không lưu', 'P1', COL_PRE, COL + ['Bỏ tích Phòng ban.', 'Bấm Đóng (hoặc (x) / click ra ngoài).', 'Mở lại cửa sổ.'], '—',
      ['Bảng vẫn có cột Phòng ban.', 'Mở lại thấy Phòng ban vẫn tích.']),
    T(11, 'Ghi nhớ sau khi tải lại', 'P0', 'Đã lưu cấu hình ẩn Bộ phận ở TC_04.005.', ['Nhấn F5.'], '—', ['Bảng vẫn không có cột Bộ phận.']),
    T(12, 'Cấu hình theo tài khoản', 'P1', 'DNS Admin đã ẩn cột Bộ phận.', ['Đăng nhập A trên cùng trình duyệt, mở màn.',
                                                                        'Đăng nhập DNS Admin ở trình duyệt khác, mở màn.'], '—',
      ['A vẫn thấy cột Bộ phận.', 'DNS Admin ở trình duyệt khác vẫn không có cột Bộ phận (lưu theo tài khoản).']),
    T(13, 'Không ảnh hưởng dữ liệu', 'P1', COL_PRE, COL + ['Ẩn 3 cột, bấm Lưu.'], '—', ['Dòng tổng vẫn "Hiển thị 1–6 / 6".']),
    T(14, 'Không ảnh hưởng lọc', 'P1', [PRE, 'Đang lọc Chỉ tiêu = Vượt hạn mức.'], COL + ['Ẩn cột Phòng ban, bấm Lưu.'], '—',
      ['Bộ lọc giữ nguyên, kết quả không đổi.']),
]

# ============================================================== V. XUẤT EXCEL
EXP = [MENU, 'Bấm Xuất Excel trên thanh công cụ.']
FILE = '"bao-cao-han-muc-cong-no-nhan-vien.xlsx"'
S5 = [
    T(1, 'Mở cửa sổ chọn trường', 'P1', PRE, EXP, '—', ['Mở cửa sổ "Chọn trường xuất file", chưa tải file ngay.']),
    T(2, 'Danh sách trường', 'P0', PRE, EXP, '—',
      ['6 trường: Mã nhân viên, Tên nhân viên, Bộ phận, Phòng ban, Hạn mức công nợ xuất hàng, Tổng công nợ khách hàng hiện tại.',
       'STT không nằm trong danh sách (luôn có trong file).']),
    T(3, 'Trường chọn mặc định theo cột đang hiện', 'P1', [PRE, 'Đã ẩn cột Bộ phận bằng Tùy chỉnh cột.'], EXP, '—',
      ['5 trường tích sẵn theo thứ tự cột trên bảng, Bộ phận xếp cuối và không tích; "Đang chọn 5/6 trường".']),
    T(4, 'Xuất với trường mặc định', 'P0', PRE, EXP + ['Bấm Xuất file.'], '—',
      ['Cửa sổ đóng, cạnh nút Xuất Excel hiện tiến độ, tải file ' + FILE + ', báo "Xuất Excel thành công.".',
       'File có STT + 6 cột, 6 dòng dữ liệu.']),
    T(5, 'Xuất tất cả trường', 'P1', [PRE, 'Đã ẩn cột Bộ phận.'], EXP + ['Bấm Chọn tất cả.', 'Bấm Xuất file.'], '—',
      ['"Đang chọn 6/6 trường".', 'File có STT + 6 cột (gồm Bộ phận).']),
    T(6, 'Xuất một số trường', 'P0', PRE, EXP + ['Bấm Bỏ chọn hết, tích Mã nhân viên, Tổng công nợ khách hàng hiện tại.', 'Bấm Xuất file.'], '—',
      ['File đúng STT + 2 cột Mã nhân viên, Tổng công nợ khách hàng hiện tại.']),
    T(7, 'Không chọn trường nào', 'P1', PRE, EXP + ['Bấm Bỏ chọn hết.'], '—', ['"Đang chọn 0/6 trường"; nút Xuất file bị khóa.']),
    T(8, 'Xuất theo từ khóa tìm kiếm', 'P1', PRE, [MENU, 'Tìm "Bùi Thị".', 'Bấm Xuất Excel, Xuất file.'], '—',
      ['File chỉ gồm 2 dòng 41410780, 10410006.']),
    T(9, 'Xuất theo bộ lọc', 'P0', [PRE, THINH], [MENU, ADV, 'Chọn Chỉ tiêu = Vượt hạn mức.', 'Xuất Excel, Xuất file.'], '—',
      ['File đúng các dòng đang hiện (có 41410780).', 'File không có dòng ghi điều kiện lọc / khoảng ngày.']),
    T(10, 'Xuất nhiều trang', 'P0', PRE, [MENU, P5, 'Đang ở trang 1.', 'Xuất Excel, Xuất file.'], '—',
      ['File có đủ 6 dòng (không chỉ 5 dòng trang đang xem).']),
    T(11, 'Xuất danh sách rỗng', 'P0', PRE, [MENU, 'Tìm "ZZZ999".', 'Xuất Excel, Xuất file.'], '—',
      ['VẪN tải file ' + FILE + ', báo "Xuất Excel thành công.".',
       'File có letterhead, tiêu đề, hàng tên cột, khối ký; không có dòng dữ liệu (#11725).']),
    T(12, 'Tên file', 'P2', PRE, EXP + ['Bấm Xuất file.'], '—', ['Tên file ' + FILE + '.']),
    T(13, 'Định dạng và bố cục file', 'P1', PRE, EXP + ['Xuất file, mở bằng Excel.'], '—',
      ['Mở được, đuôi .xlsx, sheet "Han muc cong no NV".',
       'Dòng 1 letterhead công ty người đăng nhập rộng bằng bảng; dòng 2 tiêu đề "BÁO CÁO HẠN MỨC CÔNG NỢ NHÂN VIÊN"; dòng 3 hàng tên cột in đậm có nút lọc.',
       'Bảng có viền; cuối file khối "Ngày ..., tháng ..., năm ...", "Người lập", "(Ký, họ tên)".']),
    T(14, 'Tiêu đề cột trong file', 'P1', PRE, EXP + ['Xuất file.'], '—',
      ['Hàng tên cột: STT, Mã nhân viên, Tên nhân viên, Bộ phận, Phòng ban, Hạn mức công nợ xuất hàng, Tổng công nợ khách hàng hiện tại.']),
    T(15, 'Thứ tự cột theo kéo thả', 'P1', PRE, EXP + ['Bỏ chọn hết; tích Mã nhân viên, Tên nhân viên, Hạn mức công nợ xuất hàng; kéo Hạn mức lên đầu.', 'Xuất file.'], '—',
      ['File: STT, Hạn mức công nợ xuất hàng, Mã nhân viên, Tên nhân viên (đúng thứ tự kéo).']),
    T(16, 'Số lượng bản ghi', 'P0', PRE, [MENU, ADV, 'Chọn Chỉ tiêu = Trong hạn mức.', 'Xuất file.'], '—',
      ['Số dòng dữ liệu trong file = N của dòng "Hiển thị 1–… / N" trên màn, STT từ 1.']),
    T(17, 'Dữ liệu khớp danh sách', 'P0', [PRE, ZERO], [MENU, 'Tìm "10410006".', 'Xuất file.'], '—',
      ['Dòng 1: 1, 10410006, Bùi Thị Phương, (trống), BAN ĐIỀU HÀNH, 6,770,777, 0.', 'Giá trị từng ô trùng dòng trên bảng.']),
    T(18, 'Định dạng ngày / số / chữ', 'P1', [PRE, DUY], EXP + ['Xuất file, mở Excel, chọn các ô Hạn mức rồi xem thanh trạng thái.'], '—',
      ['Hạn mức, Tổng công nợ là ô SỐ định dạng #,##0, Excel cộng SUM được.', 'Số âm giữ dấu (-20,000,000); mã nhân viên số giữ dạng chữ; file không có cột ngày.']),
    T(19, 'Tiếng Việt và ký tự đặc biệt', 'P2', PRE, EXP + ['Xuất file.'], '—',
      ['Tên "Bùi Thị Phương", "HỘI ĐỒNG QUẢN TRỊ", "Kế toán_Hành chính CN Vinh" đúng dấu, giữ ký tự "_".']),
    T(20, 'Mốc Đến ngày áp vào file', 'P1', [PRE, DUY], [MENU, ADV, 'Chọn Thời gian 01/01/2020 – 31/12/2020.', 'Xuất file.'], '—',
      ['Cột Tổng công nợ trong file bằng số trên màn ở cùng mốc Đến ngày 31/12/2020.']),
    T(21, 'Đóng cửa sổ không xuất', 'P2', PRE, EXP + ['Bấm Đóng (hoặc (x) / click ra ngoài).'], '—', ['Cửa sổ đóng, không tải file.']),
]

# ============================================================== VI. ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU
S6 = [
    T(1, 'Khai hạn mức mới xuất hiện trên báo cáo', 'P0',
      [PRE, 'Tài khoản E có quyền Quản lý tài khoản nhân viên; nhân viên Y chưa có hạn mức.'],
      ['Đăng nhập E.', ACCF + ' (nhân viên Y)', 'Nhập Hạn mức công nợ xuất hàng 10,000,000, bấm Lưu.', MENU],
      'Hạn mức công nợ xuất hàng: 10,000,000',
      ['Báo cáo có dòng nhân viên Y ở ĐẦU bảng (vừa cập nhật): Hạn mức 10,000,000.', 'Tổng số dòng tăng 1 (7).']),
    T(2, 'Sửa hạn mức cập nhật trên báo cáo', 'P0', [PRE, 'Tài khoản E như trên.'],
      [ACCF + ' (DNS01)', 'Đổi Hạn mức công nợ xuất hàng thành 300, bấm Lưu.', MENU], 'Hạn mức: 300',
      ['Dòng DNS01 lên đầu, Hạn mức hiện 300; các cột khác giữ nguyên.', 'Lịch sử tài khoản DNS01 ghi Hạn mức 200 → 300.']),
    T(3, 'Đặt hạn mức về 0 thì dòng rời báo cáo', 'P0', [PRE, 'Tài khoản E như trên; nhân viên Y ở case 1.'],
      [ACCF + ' (nhân viên Y)', 'Xóa trắng ô Hạn mức công nợ xuất hàng (hoặc nhập 0), bấm Lưu.', MENU, 'Tìm theo mã nhân viên Y.'], '—',
      [EMPTY + '; tổng số dòng về 6.']),
    T(4, 'Form Tài khoản nhân viên chặn hạn mức âm', 'P1', [PRE, 'Tài khoản E như trên.'],
      [ACCF + ' (DNS01)', 'Nhập Hạn mức -5, bấm Lưu.'], 'Hạn mức: -5',
      ['Báo "Hạn mức công nợ xuất hàng không được âm" dưới ô; không lưu.', 'Báo cáo vẫn hiện Hạn mức cũ của DNS01.']),
    T(5, 'Công nợ cập nhật theo bút toán', 'P0', [PRE, DUY, 'Kế toán vừa ghi thêm bút toán Nợ 5,000,000 vào hợp đồng đầu kỳ do 11410102 tạo (tài khoản 1311).'],
      [MENU, 'Quan sát dòng 11410102.', 'Bấm "11410102".'], '—',
      ['Tổng công nợ tăng 5,000,000 (-15,000,000).', 'Cửa sổ: khách của bút toán mới mang số lũy kế mới = -15,000,000.']),
    T(6, 'Bút toán hợp đồng bán hàng không làm đổi công nợ', 'P0', [PRE, DUY, 'Kế toán vừa duyệt phiếu xuất hàng thuộc hợp đồng bán do 11410102 tạo.'],
      [MENU, 'Quan sát dòng 11410102.'], '—',
      ['Tổng công nợ KHÔNG đổi (-20,000,000).', 'Lưu ý: giữ y ERP, hợp đồng bán không tính (#11727).']),
    T(7, 'Bộ lọc chỉ tiêu cập nhật khi đổi hạn mức', 'P1', [PRE, THINH, 'Tài khoản E như trên.'],
      [ACCF + ' (41410780)', 'Đổi Hạn mức thành 5,000,000,000, bấm Lưu.', MENU, ADV, 'Chọn Chỉ tiêu = Vượt hạn mức.', 'Chọn Chỉ tiêu = Trong hạn mức.'], '—',
      ['Bước 5: 41410780 không còn trong Vượt hạn mức.', 'Bước 6: 41410780 có trong Trong hạn mức.']),
    T(8, 'Không xóa được dữ liệu từ báo cáo', 'P1', PRE, [MENU, 'Quan sát từng dòng và thanh công cụ.'], '—',
      ['Không có nút Xóa / Sửa; hạn mức chỉ đổi ở form Tài khoản nhân viên.']),
    T(9, 'Cấp con đúng cấp cha', 'P1', [PRE, DUY], [MENU, 'Bấm "11410102".'], '—',
      ['Cửa sổ chỉ có khách hàng của hợp đồng do 11410102 tạo; không có khách của nhân viên khác.']),
    T(10, 'Tham chiếu không mất khi đổi trạng thái', 'P1', [PRE, 'Tài khoản nhân viên 19910001 vừa bị khóa (nhân viên nghỉ việc).'],
      [MENU, 'Tìm "19910001".'], '—', ['Dòng vẫn hiện đủ Mã, Tên, Phòng ban, Hạn mức (báo cáo không lọc theo trạng thái tài khoản).']),
    T(11, 'Đổi tên / phòng ban đồng bộ', 'P2', [PRE, 'Hồ sơ nhân viên 10410006 vừa được đổi phòng ban.'], [MENU, 'Tìm "10410006".'], '—',
      ['Cột Phòng ban hiện phòng ban mới; hạn mức giữ nguyên.']),
    T(12, 'Không có bản ghi mồ côi', 'P2', [PRE, 'Nhân viên Y đã bị đặt hạn mức về 0 ở case 3.'],
      [MENU, 'Dùng công cụ kiểm thử API gọi chức năng mở cửa sổ theo khách hàng của nhân viên Y.'], '—',
      ['Trả "Không tìm thấy dữ liệu" (trên giao diện hiện "Lỗi khi tải dữ liệu").']),
    T(13, 'Không có dữ liệu trùng', 'P2', PRE, [MENU, P5, 'So 2 trang khi sắp theo Mã nhân viên.'], '—',
      ['Không dòng nào lặp lại giữa 2 trang; mỗi tài khoản nhân viên chỉ 1 dòng.']),
]

# ============================================================== VII. PHÂN QUYỀN
S7 = renum([
    T(1, 'Xem báo cáo không cần quyền riêng', 'P0', [ACC_A, PRE], ['Đăng nhập A.', MENU], '—',
      ['A mở được màn, thấy đủ 6 dòng như DNS Admin (không bó theo công ty của A).']),
    T(2, 'Phạm vi dữ liệu mọi công ty', 'P0', [ACC_A, PRE, THINH], ['Đăng nhập A.', MENU, ADV, 'Mở ô Công ty.'], '—',
      ['Ô Công ty liệt kê mọi công ty; A thấy cả 41410780 (Chi nhánh Vinh) và DNS01 (Tân Phát).']),
    T(3, 'Xem chi tiết theo khách hàng không cần quyền', 'P0', [ACC_A, DUY], ['Đăng nhập A.', MENU, 'Bấm "11410102".'], '—',
      ['A mở được cửa sổ, số liệu như DNS Admin.']),
    T(4, 'Không có chức năng Thêm mới / Sửa / Xóa / Khóa / Import / Lịch sử', 'P1', 'Tài khoản DNS Admin (quyền cao nhất).',
      [MENU, 'Quan sát thanh công cụ và từng dòng.'], '—',
      ['Không có nút Thêm mới, Sửa, Xóa, Khóa / Mở khóa, Import Excel, In, Lịch sử ở màn.']),
    T(5, 'Xuất Excel không cần quyền', 'P1', [ACC_A, PRE], ['Đăng nhập A.', MENU, 'Xuất Excel, Xuất file.'], '—',
      ['A tải được file 6 dòng; letterhead là công ty của A.']),
    T(6, 'Nút luôn hiện, không phụ thuộc quyền', 'P0', ACC_A, ['Đăng nhập A.', MENU], '—',
      ['Nút Xuất Excel, Cấu hình cột hiển thị, Cài đặt bộ lọc, liên kết Mã nhân viên, icon ⓘ đều hiện và dùng được.']),
    T(7, 'Mở thẳng đường dẫn màn', 'P1', ACC_A, ['Đăng nhập A.', 'Dán đường dẫn màn báo cáo vào thanh địa chỉ.'], '—',
      ['Mở được màn bình thường (màn không gắn quyền).']),
    T(8, 'Gọi thẳng chức năng bỏ qua giao diện', 'P0', [ACC_A, PRE],
      ['Dùng công cụ kiểm thử API, đăng nhập A, gọi chức năng lấy báo cáo không kèm bộ lọc.',
       'Gọi chức năng mở cửa sổ theo khách hàng của nhân viên chưa có hạn mức.'], '—',
      ['Bước 1: trả đủ 6 dòng (đúng thiết kế không phân quyền).', 'Bước 2: "Không tìm thấy dữ liệu".']),
    T(9, 'Quyền sửa hạn mức nằm ở màn Tài khoản nhân viên', 'P1', ACC_A,
      ['Đăng nhập A.', 'Vào phân hệ Quản trị hệ thống > "Người dùng & phân quyền".'], '—',
      ['A không thấy / không mở được mục Tài khoản nhân viên (không có quyền) — không sửa được hạn mức.',
       'A vẫn xem được báo cáo.']),
    T(10, 'Đổi quyền giữa lúc thao tác', 'P2', 'Tài khoản A đang mở màn; quản trị gỡ hết quyền của A ở phân hệ Tài chính.',
      ['A bấm sang trang khác hoặc tải lại trang.'], '—', ['A vẫn xem được báo cáo (màn không gắn quyền).']),
    T(11, 'Mục menu bị tắt', 'P2', 'Mục "Báo cáo hạn mức công nợ nhân viên" của phân hệ Tài chính bị tắt ở màn Cài đặt phân hệ.',
      ['Đăng nhập tài khoản thường.', 'Mở phân hệ Tài chính > Kế toán công nợ > Nhân viên.'], '—',
      ['Không thấy mục menu Báo cáo hạn mức công nợ nhân viên.']),
])

SECTIONS = [
    ('I', 'HIỂN THỊ DANH SÁCH VÀ TRUY CẬP', S1),
    ('II', 'TÌM KIẾM VÀ LỌC', S2),
    ('III', 'XEM CHI TIẾT', S3),
    ('IV', 'TÙY CHỈNH CỘT', S4),
    ('V', 'XUẤT EXCEL', S5),
    ('VI', 'ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU', S6),
    ('VII', 'PHÂN QUYỀN', S7),
]
DESCRIPTION_BLOCK = [(h, clean(t)) for h, t in DESCRIPTION_BLOCK]
check_no_dash_pre(SECTIONS, [])

if __name__ == '__main__':
    n = sum(len(s[2]) for s in SECTIONS)
    p0 = sum(1 for s in SECTIONS for c in s[2] if c[2] == 'P0')
    print('TC', n, 'P0', p0, '%.0f%%' % (100.0 * p0 / n))
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name='Báo cáo hạn mức công nợ nhân viên - Cập nhật ngày 03/11/2026',
          module_name='Báo cáo hạn mức công nợ nhân viên', description_block=DESCRIPTION_BLOCK, role_tcs=[], sections=SECTIONS)
