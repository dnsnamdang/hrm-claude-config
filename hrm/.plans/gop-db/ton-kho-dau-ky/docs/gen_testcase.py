# -*- coding: utf-8 -*-
"""Testcase màn "Khai báo tồn kho đầu kỳ" — KHUÔN CHUẨN tab "13. DM quốc gia" (user chốt 03/11/2026, loại 'phieu').

Làm lại từ bản 02/11 (gen_testcase_v1.py — giữ để tra): lấy NGUYÊN VĂN mọi case của bản cũ qua hàm cu(<nhóm cũ>, <số cũ>),
xếp lại vào đúng nhóm chuẩn; bỏ nhóm/mã kiểu cũ (TC-ROLE, DANH SÁCH SẮP XẾP, TÁC ĐỘNG SỐ LIỆU, LUỒNG ĐẦU CUỐI…); viết thêm
case cho các dòng checklist "Mẫu tài liệu.xlsx" áp dụng được mà bản cũ thiếu. Màn không có Chi tiết, Lịch sử, In, Duyệt.
Cuối file kiểm: mọi case cũ đều đã dùng đúng 1 lần.
Chạy: python gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import gen_testcase_v1 as V1  # noqa: E402  (bản 02/11 — nguồn nguyên văn các case cũ)
from _tc_chuan import build_chuan  # noqa: E402

TEN = V1.TEN
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SHEET = 'Trang tính1'
MODULE = V1.MODULE
NGAY = '03/11/2026'
MENU = V1.MENU
BC = V1.BC
TK = V1.TK
GD = V1.GD
CHUA_LUU = '"Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"'
DOI = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'


def _gach(text):
    """Giọng tab Quốc gia: mỗi ý Expected bắt đầu "-  "; bỏ dấu trừ toán học (U+2212)."""
    out = []
    for line in str(text).replace('−', '-').replace(' → ', ' > ').split('\n'):
        if line.startswith('- ') and not line.startswith('-  '):
            line = '-  ' + line[2:]
        out.append(line)
    return '\n'.join(out)


# ------------------------------------------------------------------ case cũ (nguyên văn)
OLD = {('ROLE', c[0]): c for c in V1.ROLE_TCS}
for _k, _t, _cs in V1.SECTIONS:
    for _c in _cs:
        OLD[(_k, _c[0])] = _c
SO_CU = len(OLD)
DA_DUNG = set()


def cu(nhom, so, func=None, pre=None, steps=None, data=None, exp=None, prio=None, them_exp=None):
    """Lấy nguyên văn case cũ; tham số khác None = sửa câu chữ ô đó; them_exp = thêm ý vào cuối Expected."""
    key = (nhom, so)
    assert key not in DA_DUNG, 'Case cũ dùng 2 lần: %s' % (key,)
    DA_DUNG.add(key)
    _, f, p, pr, st, td, ex = OLD[key]
    td = '' if td == '—' else td
    pr = '' if pr == '—' else pr
    ex = exp or ex
    if them_exp:
        ex = ex + '\n' + '\n'.join('- ' + e for e in them_exp)
    return (func or f, prio or p, pre or pr, steps or st, td if data is None else data, _gach(ex))


def moi(func, prio, pre, steps, data, exp):
    """Case mới: steps / exp truyền list, tự đánh số bước và gạch đầu dòng."""
    if not isinstance(steps, str):
        steps = '\n'.join('%d. %s' % (i, s) for i, s in enumerate(steps, 1))
    if not isinstance(exp, str):
        exp = '\n'.join('-  ' + e for e in exp)
    return (func, prio, pre, steps, data, exp)


def nhom(cases):
    return [('%03d' % i,) + c for i, c in enumerate(cases, 1)]


# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
G1 = [
    cu('I', '001', func='Mở màn hình từ menu'),
    moi('Các nút chức năng trên màn danh sách', 'P0', 'TK-A có quyền "Khai báo tồn kho đầu kỳ".',
        ['Vào ' + MENU, 'Quan sát thanh công cụ của bảng và khu vực tìm kiếm'], '',
        ['Thanh công cụ của bảng có lần lượt: Tạo mới, Import Excel, Xuất Excel, nút biểu tượng cột (gợi ý "Cấu hình cột hiển thị")',
         'Khu vực tìm kiếm có ô tìm nhanh (gợi ý "Tìm theo mã / tên hàng"), nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
         'KHÔNG có nút In']),
    cu('I', '002', func='Các cột mặc định hiển thị và mặc định ẩn',
       them_exp=['TK-A: cột Công ty ẩn, bật được ở Cấu hình cột hiển thị']),
    cu('I', '003', func='Định dạng số, người, ngày và ô trống'),
    cu('I', '004', func='Tên hàng, Kho, Vị trí dài'),
    cu('III', '004', func='Nút Sửa, Xóa theo trạng thái giao dịch của nhóm'),
    moi('Dữ liệu trên bảng khớp với khai báo vừa lưu', 'P0',
        'TK-A vừa khai H-1 tại kho PTT, công ty TPE: vị trí A 4, vị trí B 6 (ĐVT Bộ).',
        ['Vào màn danh sách', 'Tìm nhanh "H-1", nhấn Enter', 'Đọc 2 dòng kết quả'], 'Ô tìm nhanh: H-1',
        ['Có đúng 2 dòng của H-1: một dòng vị trí A số lượng 4, một dòng vị trí B số lượng 6',
         'Tên hàng, Mã hàng, Kho "Phan Trọng Tuệ", Mã vị trí, Vị trí, ĐVT "Bộ" đúng với dữ liệu đã nhập',
         'Người tạo = "<họ tên TK-A> - <mã phòng ban>", Ngày tạo đúng thời điểm lưu; Người cập nhật, Ngày cập nhật để trống']),
    moi('Danh sách khi chưa có khai báo nào', 'P2', 'Môi trường kiểm thử: công ty của TK-A chưa có khai báo tồn kho đầu kỳ nào.',
        ['Vào ' + MENU, 'Quan sát bảng'], '',
        ['Bảng hiện dòng "Không có dữ liệu phù hợp."',
         'Màn hình không báo lỗi; các nút Tạo mới, Import Excel, Xuất Excel vẫn dùng được']),
    moi('Không có dữ liệu phù hợp bộ lọc', 'P1', 'Không có hàng nào có mã hoặc tên chứa "zzzkhongtontai999".',
        ['Gõ "zzzkhongtontai999" vào ô tìm nhanh', 'Nhấn Enter'], 'Ô tìm nhanh: zzzkhongtontai999',
        ['Bảng hiện dòng "Không có dữ liệu phù hợp."',
         'Không hiện dòng "Hiển thị a–b / N", không có thông báo lỗi']),
    # --- phân trang
    moi('Số dòng mặc định và các lựa chọn số dòng/trang', 'P1', 'Danh sách có hơn 50 dòng.',
        ['Mở màn danh sách', 'Mở ô "Số dòng/trang" ở góc dưới bên phải bảng'], '',
        ['Mặc định hiển thị 10 dòng/trang, dòng tổng "Hiển thị 1–10 / N"',
         'Ô "Số dòng/trang" cho chọn 5 / 10 / 20 / 50 / 100']),
    cu('III', '002', func='Đổi số dòng mỗi trang và số thứ tự liên tục'),
    moi('Nút sang trang kế tiếp và lùi về trang trước', 'P0', 'Danh sách có N dòng, nhiều hơn 3 trang. Đang ở trang 1.',
        ['Bấm nút › (trang kế tiếp)', 'Đọc thanh phân trang và dòng tổng', 'Bấm nút ‹ (trang trước)', 'Đọc lại'], '',
        ['Bước 2: sang trang 2, số trang 2 được tô đậm, dòng tổng hiện "Hiển thị 11–20 / N"',
         'Bước 4: về trang 1, dòng tổng hiện "Hiển thị 1–10 / N"',
         'Dữ liệu hai trang không lặp, không thiếu dòng']),
    moi('Nút về trang cuối và về trang đầu', 'P0', 'Danh sách có N dòng, nhiều hơn 3 trang. Đang ở trang 1.',
        ['Bấm nút » (về trang cuối)', 'Đọc dòng tổng và STT dòng cuối', 'Bấm nút « (về trang đầu)'], 'N = tổng số dòng',
        ['Bước 2: nhảy tới trang cuối, dòng tổng hiện "Hiển thị …–N / N", STT dòng cuối bằng N',
         'Bước 3: về trang 1, dòng tổng hiện "Hiển thị 1–10 / N"']),
    moi('Nút phân trang ở trang đầu và trang cuối', 'P1', 'Danh sách có nhiều hơn 1 trang.',
        ['Đứng ở trang 1, quan sát hai nút « và ‹', 'Bấm » về trang cuối, quan sát hai nút › và »'], '',
        ['Ở trang 1: nút « và ‹ bị mờ, bấm không có tác dụng',
         'Ở trang cuối: nút › và » bị mờ, bấm không có tác dụng']),
    moi('Áp dụng bộ lọc khi đang ở trang giữa thì về trang 1', 'P1', 'Đang đứng ở trang 3. Kho PTT có ít dòng hơn 1 trang.',
        ['Mở Tìm kiếm nâng cao', 'Chọn Kho = PTT', 'Quan sát thanh phân trang và dòng tổng'], 'Kho: PTT',
        ['Bảng quay về trang 1, dòng tổng hiện "Hiển thị 1–… / <số dòng của kho PTT>"']),
    # --- sắp xếp
    moi('Thứ tự mặc định khi mở màn', 'P1', 'Vừa lưu khai báo mới cho hàng H-1. Chưa bấm sắp xếp cột nào.',
        ['Vào ' + MENU, 'Đọc các dòng đầu'], '',
        ['Các dòng của H-1 vừa lưu nằm trên cùng',
         'Các dòng xếp theo khai báo mới nhất ở trên, càng xuống càng cũ']),
    cu('III', '001', func='Sắp xếp tăng dần, giảm dần và các cột không sắp xếp'),
    moi('Sắp xếp giữ nguyên khi chuyển trang', 'P1', 'Đang sắp xếp Số lượng giảm dần, 10 dòng/trang.',
        ['Ghi lại Số lượng dòng cuối trang 1', 'Bấm sang trang 2', 'So Số lượng dòng đầu trang 2'], '',
        ['Trang 2 vẫn sắp xếp Số lượng giảm dần, mũi tên ở tiêu đề cột không đổi',
         'Số lượng dòng đầu trang 2 nhỏ hơn hoặc bằng dòng cuối trang 1, không lặp dòng']),
]

# ================================================================== II. TÌM KIẾM & LỌC DANH SÁCH
G2 = [
    moi('Tìm nhanh đúng nguyên mã hàng', 'P0', 'Có nhóm N-TU-DO (BLNS-IR-EVOPYRO, 2 vị trí).',
        ['Gõ "BLNS-IR-EVOPYRO" vào ô tìm nhanh', 'Nhấn Enter'], 'Ô tìm nhanh: BLNS-IR-EVOPYRO',
        ['Ra đúng 2 dòng (2 vị trí) của BLNS-IR-EVOPYRO',
         'Dòng tổng hiện "Hiển thị 1–2 / 2"']),
    cu('II', '001', func='Tìm nhanh theo một phần mã hoặc tên hàng'),
    moi('Tìm nhanh không phân biệt chữ hoa chữ thường', 'P1', 'Có nhóm N-TU-DO.',
        ['Gõ "evopyro", nhấn Enter, ghi nhận kết quả', 'Xoá, gõ "EVOPYRO", nhấn Enter', 'So sánh'], 'Ô tìm nhanh: evopyro / EVOPYRO',
        ['Hai lần tìm cho ra CÙNG kết quả']),
    moi('Tìm nhanh với ký tự đặc biệt', 'P2', 'Không có hàng nào có mã hoặc tên chứa "@#$%".',
        ['Gõ "@#$%" vào ô tìm nhanh', 'Bấm Tìm kiếm'], 'Ô tìm nhanh: @#$%',
        ['Bảng hiện "Không có dữ liệu phù hợp."',
         'Màn hình không treo, không báo lỗi hệ thống']),
    moi('Tìm nhanh có khoảng trắng đầu và cuối', 'P2', 'Có nhóm N-TU-DO.',
        ['Gõ "   EVOPYRO   " (có khoảng trắng hai đầu) vào ô tìm nhanh', 'Bấm Tìm kiếm'], 'Ô tìm nhanh: "   EVOPYRO   "',
        ['Ra cùng kết quả như khi gõ "EVOPYRO" không có khoảng trắng']),
    moi('Giới hạn độ dài ô tìm nhanh', 'P2', 'Đang ở màn danh sách.',
        ['Dán chuỗi 300 ký tự vào ô tìm nhanh', 'Bấm Tìm kiếm', 'Bấm Làm mới'], 'Chuỗi 300 ký tự (vd "abcde" lặp 60 lần)',
        ['Bước 2: bảng hiện "Không có dữ liệu phù hợp."; màn hình không treo, không báo lỗi hệ thống',
         'Bước 3: ô tìm nhanh trống, bảng về toàn bộ danh sách']),
    moi('Xóa từ khóa thì danh sách quay về đầy đủ', 'P0', 'Danh sách có N dòng. Đang tìm "EVOPYRO", còn 2 dòng.',
        ['Xóa hết nội dung ô tìm nhanh', 'Nhấn Enter'], '',
        ['Dòng tổng quay lại "Hiển thị 1–10 / N"', 'Bảng về trang 1']),
    moi('Các ô lọc ở Tìm kiếm nâng cao và giá trị mặc định', 'P1', 'TK-A (không phải quản trị cao nhất).',
        ['Bấm Tìm kiếm nâng cao', 'Đọc nhãn và giá trị các ô lọc'], '',
        ['Có 4 ô: Mã hàng (gợi ý "Mã hàng"), Kho, Vị trí (gợi ý "Mã / tên vị trí"), Người tạo',
         'Mọi ô mặc định để TRỐNG (không lọc), danh sách hiện mọi dòng trong phạm vi',
         'KHÔNG có ô Công ty, KHÔNG có ô lọc theo ngày']),
    cu('II', '002'),
    cu('II', '003'),
    cu('II', '004', func='Lọc theo Vị trí (mã hoặc tên vị trí)'),
    cu('II', '005'),
    moi('Lọc kết hợp nhiều tiêu chí', 'P1', 'Kho PTT có nhóm N-TU-DO do TK-A tạo.',
        ['Chọn Kho = PTT', 'Chọn Người tạo = TK-A', 'Gõ "EVOPYRO" vào ô tìm nhanh, nhấn Enter'],
        'Kho: PTT\nNgười tạo: TK-A\nÔ tìm nhanh: EVOPYRO',
        ['Chỉ còn các dòng thoả CẢ BA điều kiện: kho Phan Trọng Tuệ, người tạo TK-A, mã hoặc tên chứa "EVOPYRO"',
         'Dòng tổng đổi theo đúng số dòng còn lại']),
    cu('II', '006', func='Lọc kết hợp ra kết quả rỗng'),
    moi('Tổng số và phân trang sau khi lọc', 'P0', 'Kho PTT có 25 dòng khai báo. Danh sách 10 dòng/trang.',
        ['Chọn Kho = PTT', 'Đọc dòng tổng và thanh phân trang', 'Bấm sang trang 3'], 'Kho: PTT',
        ['Bước 2: dòng tổng hiện "Hiển thị 1–10 / 25", thanh phân trang có 3 trang',
         'Bước 3: dòng tổng hiện "Hiển thị 21–25 / 25", STT từ 21 đến 25']),
    moi('Sắp xếp trên kết quả đã lọc', 'P2', 'Đang lọc Kho = PTT.',
        ['Bấm tiêu đề cột Mã hàng', 'Đọc cột Kho và cột Mã hàng'], '',
        ['Vẫn chỉ có dòng của kho Phan Trọng Tuệ, tổng không đổi, ô lọc Kho vẫn là PTT',
         'Mã hàng xếp tăng dần, bảng về trang 1']),
    cu('II', '007', func='Nút Làm mới xóa hết điều kiện lọc'),
    cu('II', '008', func='Mở trang Sửa rồi Quay lại thì giữ bộ lọc'),
    moi('Rời sang màn khác rồi quay lại thì bộ lọc về mặc định', 'P1', 'Đang lọc Kho = PTT, ô tìm nhanh "EVOPYRO".',
        ['Vào menu khác của phân hệ Kho (vd ' + BC + ')', 'Quay lại màn Khai báo tồn kho đầu kỳ bằng menu',
         'Quan sát khu vực tìm kiếm và bảng'], 'Kho: PTT\nÔ tìm nhanh: EVOPYRO',
        ['Ô tìm nhanh và các ô lọc trở về trống',
         'Bảng hiện toàn bộ danh sách ở trang 1']),
    moi('Tải lại trang (F5) khi đang lọc', 'P2', 'Vừa vào màn từ menu, chưa mở trang Sửa nào. Đang lọc Kho = PTT.',
        ['Nhấn F5 tải lại trang', 'Quan sát khu vực tìm kiếm và bảng'], 'Kho: PTT',
        ['Các ô lọc trở về trống', 'Bảng hiện toàn bộ danh sách ở trang 1 với 10 dòng/trang']),
    moi('Mở màn ở tab trình duyệt mới khi tab cũ đang lọc', 'P2', 'Tab 1 đang mở màn danh sách, chưa mở trang Sửa nào.',
        ['Ở tab 1: chọn Kho = PTT', 'Mở tab mới, vào màn bằng menu', 'Quan sát tab 2', 'Quay lại tab 1'], 'Kho: PTT',
        ['Tab 2: các ô lọc trống, bảng hiện toàn bộ danh sách ở trang 1',
         'Tab 1: vẫn giữ Kho = PTT và kết quả đang xem']),
    moi('Đăng xuất, đăng nhập tài khoản khác trên cùng trình duyệt', 'P1',
        'TK-A và một tài khoản khác cùng công ty, cùng quyền. Dùng chung một trình duyệt.',
        ['Đăng nhập TK-A, vào màn, chọn Kho = PTT, ô tìm nhanh "EVOPYRO"', 'Đăng xuất', 'Đăng nhập tài khoản còn lại, vào màn'],
        'Kho: PTT\nÔ tìm nhanh: EVOPYRO',
        ['Tài khoản sau thấy ô tìm nhanh và các ô lọc trống, bảng hiện toàn bộ danh sách ở trang 1',
         'Điều kiện lọc của TK-A KHÔNG hiện sang tài khoản sau']),
    cu('II', '009', func='Cài đặt bộ lọc: ẩn, đổi thứ tự, khôi phục mặc định'),
]

# ================================================================== III. THÊM MỚI
G3 = [
    cu('IV', '001', func='Mở trang Thêm'),
    cu('IV', '002', func='Ô Kho và Công ty độc lập với nhau'),
    cu('IV', '003', func='Chọn hàng hóa hợp lệ'),
    cu('IV', '004', func='Hàng đã khai tồn đầu tại kho thì bị chặn'),
    cu('IV', '005', func='Hàng chưa khai tồn kế toán tại kho thì bị chặn'),
    cu('IV', '006'),
    cu('IV', '007', func='Cửa sổ chọn vị trí'),
    cu('IV', '008', func='Thêm vị trí tự điền phần số lượng còn thiếu'),
    cu('IV', '018', func='Bỏ hàng hoặc xóa dòng vị trí'),
    moi('Thêm mới chỉ một vị trí bằng đúng SL tồn kế toán', 'P0', 'H-1 chưa khai, SL tồn kế toán 10 Bộ tại PTT / TPE.',
        ['Chọn Kho = PTT, Công ty = TPE', 'Chọn hàng hóa H-1', 'Chọn 1 vị trí, giữ Số lượng = 10', 'Bấm Lưu'], 'H-1: 1 vị trí, 10',
        ['Báo "Thêm mới thành công", quay về danh sách',
         'Danh sách có 1 dòng mới của H-1 với Số lượng 10, có nút Sửa, Xóa']),
    cu('IV', '013', func='Thêm mới nhiều vị trí thành công'),
    # --- validate
    cu('IV', '011', func='Bỏ trống trường bắt buộc thì bị chặn'),
    cu('IV', '012', func='Ô Số lượng chỉ nhận số'),
    cu('IV', '009', func='Chọn trùng vị trí trong một hàng thì bị chặn'),
    cu('IV', '010', func='Tổng số lượng khác SL tồn kế toán thì bị chặn'),
    moi('Thông báo lỗi tổng số lượng mất ngay khi sửa đúng', 'P1',
        'H-1 hai vị trí 4 + 5 đang báo đỏ "Tổng số lượng phải bằng SL tồn kế toán (10)".',
        ['Sửa vị trí 2 thành 6', 'Quan sát các ô Số lượng và dòng Tổng số lượng'], 'Vị trí 2: 6',
        ['Viền đỏ và câu lỗi dưới ô biến mất ngay, Tổng số lượng 10 không còn chữ đỏ',
         'Bấm Lưu thì lưu thành công']),
    cu('IV', '016', func='Kho không thuộc công ty đã chọn'),
    # --- lưu và tiếp tục
    cu('IV', '014', func='Lưu và tiếp tục giữ trang Thêm để nhập tiếp'),
    moi('Lưu và tiếp tục khi bỏ trống trường bắt buộc', 'P1', 'Đã chọn Kho, Công ty, thêm H-1, bỏ trống Vị trí.',
        ['Bấm "Lưu và tiếp tục"'], '',
        ['Dưới ô Vị trí "Bắt buộc phải chọn"; thông báo "Bạn chưa nhập đầy đủ thông tin."',
         'Vẫn ở trang Thêm, Kho, Công ty, hàng đã chọn giữ nguyên, không bị xoá trắng',
         'Không có dòng khai báo mới ở danh sách']),
    moi('Lưu và tiếp tục khi tổng số lượng lệch', 'P1', 'H-1 (kế toán 10) hai vị trí 4 + 5.',
        ['Bấm "Lưu và tiếp tục"', 'Sửa vị trí 2 thành 6, bấm lại "Lưu và tiếp tục"'], '',
        ['Bước 1: báo "Tổng số lượng phải bằng SL tồn kế toán (10)" và thông báo "' + V1.LECH + '"; không lưu, giữ nguyên dữ liệu',
         'Bước 2: báo "Thêm mới thành công", trang Thêm mở lại trống (Kho, Công ty, bảng trống)']),
    moi('Bấm Lưu và tiếp tục rồi bấm Quay lại ngay thì không hỏi', 'P2', 'Form hợp lệ trên trang Thêm.',
        ['Bấm "Lưu và tiếp tục"', 'Không nhập gì thêm vào trang Thêm trống', 'Bấm Quay lại'], '',
        ['Khai báo vừa lưu có trong danh sách',
         'Bấm Quay lại về thẳng danh sách, KHÔNG hiện hộp "Thông tin chưa lưu"']),
    # --- đổi kho / đóng khi chưa lưu
    cu('IV', '015', func='Đổi Kho hoặc Công ty khi đã có hàng'),
    moi('Bấm Quay lại khi chưa nhập gì', 'P1', 'Trang Thêm vừa mở, chưa chọn gì.',
        ['Bấm Quay lại'], '',
        ['Về thẳng danh sách, KHÔNG hiện hộp "Thông tin chưa lưu"']),
    cu('IV', '017', func='Bấm Quay lại khi đã nhập thông tin'),
    moi('Rời trang Thêm bằng menu khi đã nhập', 'P2', 'Đã chọn Kho, Công ty và thêm H-1, chưa Lưu.',
        ['Bấm một mục menu khác', 'Bấm Ở lại', 'Bấm lại mục menu đó, chọn Thoát'], '',
        ['Hiện hộp "Thông tin chưa lưu": ' + CHUA_LUU + ' với 2 nút Thoát, Ở lại',
         'Ở lại: vẫn ở trang Thêm, dữ liệu còn nguyên',
         'Thoát: sang màn đã chọn, không có khai báo mới']),
    # --- đặc biệt
    moi('Bấm Lưu liên tục chỉ ghi một lần', 'P0', 'Form hợp lệ: H-1 hai vị trí 4 + 6.',
        ['Bấm Lưu', 'Bấm Lưu lần hai thật nhanh', 'Xem danh sách và ' + BC], '',
        ['Chỉ có đúng 2 dòng của H-1 (không bị ghi đôi thành 4 dòng)',
         'Báo cáo tồn của H-1 tại PTT tăng đúng 10, không phải 20']),
    cu('IX', '003', func='Hai người cùng khai báo một hàng cùng lúc'),
]

# ================================================================== IV. CHỈNH SỬA
G4 = [
    cu('V', '001', func='Mở trang Sửa theo nhóm'),
    cu('V', '003', func='Sửa chia lại số lượng các vị trí thành công'),
    moi('Sửa xong ghi nhận người và ngày cập nhật', 'P1', 'Vừa sửa nhóm N-TU-DO ở case trên.',
        ['Tìm các dòng của BLNS-IR-EVOPYRO trên danh sách', 'Đọc cột Người cập nhật, Ngày cập nhật'], '',
        ['Hai dòng có số lượng thay đổi ghi Người cập nhật = người vừa sửa, Ngày cập nhật = thời điểm lưu',
         'Người tạo, Ngày tạo giữ nguyên như lúc khai']),
    moi('Lưu khi không thay đổi gì thì không ghi cập nhật', 'P1', 'Nhóm N-TU-DO chưa ai sửa (Người cập nhật trống).',
        ['Mở trang Sửa N-TU-DO', 'Không đổi số lượng nào, bấm Lưu', 'Xem các dòng trên danh sách'], '',
        ['Lưu không báo lỗi, quay về danh sách',
         'Người cập nhật, Ngày cập nhật của các dòng vẫn để trống; số lượng không đổi']),
    cu('V', '002', func='Sửa lệch SL tồn kế toán thì bị chặn'),
    cu('V', '004', func='Bỏ trống hoặc nhập 0 ở Số lượng khi sửa'),
    moi('Thông báo lỗi mất ngay khi sửa về số hợp lệ', 'P1', 'Trang Sửa N-TU-DO đang báo đỏ do tổng 9 khác 10.',
        ['Sửa lại số lượng để tổng bằng 10'], '',
        ['Viền đỏ và câu "Tổng số lượng phải bằng SL tồn kế toán (10)" biến mất ngay',
         'Bấm Lưu thì báo "Cập nhật thành công"']),
    cu('V', '006', func='Bấm Quay lại khi đã sửa'),
    moi('Sửa rồi trả lại đúng số cũ, bấm Quay lại thì không hỏi', 'P2', 'Trang Sửa N-TU-DO, vị trí 1 đang 4.',
        ['Sửa vị trí 1 thành 5', 'Sửa lại đúng 4', 'Bấm Quay lại'], 'Vị trí 1: 4 -> 5 -> 4',
        ['Về thẳng danh sách, KHÔNG hiện hộp "Thông tin chưa lưu" vì dữ liệu không khác ban đầu']),
    moi('Bấm Thoát hoặc Ở lại ở hộp Thông tin chưa lưu khi sửa', 'P1', 'Trang Sửa N-TU-DO, đã đổi vị trí 1 từ 4 thành 3.',
        ['Bấm Quay lại, chọn Ở lại', 'Bấm Quay lại, chọn Thoát', 'Mở lại trang Sửa N-TU-DO'], '',
        ['Ở lại: vẫn ở trang Sửa, vị trí 1 vẫn là 3',
         'Thoát: về danh sách; mở lại trang Sửa vị trí 1 vẫn là 4 (không lưu)']),
    cu('V', '005', func='Mở thẳng trang Sửa của nhóm đã có giao dịch'),
    cu('IX', '004', func='Nhóm vừa phát sinh giao dịch khi đang sửa'),
    moi('Sửa nhóm đã bị người khác xóa', 'P1', 'A đang mở trang Sửa N-TU-DO; B xóa nhóm N-TU-DO.',
        ['A sửa số lượng (tổng vẫn khớp), bấm Lưu'], '',
        ['A nhận thông báo ' + DOI,
         'Không tạo lại dòng nào; danh sách không còn nhóm N-TU-DO']),
]

# ================================================================== V. XÓA
G5 = [
    cu('VI', '001', func='Hộp xác nhận xóa và bấm Hủy'),
    cu('VI', '002', func='Xóa cả nhóm thành công', pre='Nhóm H-1 vừa lập ở TC_03.011 (2 vị trí 4 + 6), chưa có giao dịch.',
       them_exp=['Dòng tổng dưới bảng giảm đúng 2']),
    cu('VI', '003', func='Khai lại sau khi xóa'),
    moi('Nhóm đã có giao dịch không có nút Xóa', 'P0', 'Nhóm N-GD đã có giao dịch kho.',
        ['Tìm các dòng của N-GD', 'Quan sát cột Hành động'], '',
        ['Cột Hành động của mọi dòng N-GD KHÔNG có nút Xóa (ẩn hẳn, không hiện xám)']),
    moi('Xóa nhóm vừa phát sinh giao dịch khi đang mở danh sách', 'P1',
        'A đang mở danh sách, dòng N-TU-DO còn nút Xóa. B vừa lập phiếu chuyển vị trí (nháp) lấy từ lô tồn đầu của N-TU-DO.',
        ['A bấm Xóa ở dòng N-TU-DO, bấm Xóa ở hộp xác nhận'], '',
        ['A nhận thông báo "' + GD + '"',
         'Không dòng nào bị xóa, tồn kho không đổi']),
    moi('Xóa nhóm đã bị người khác xóa', 'P1', 'A và B cùng mở danh sách có nhóm N-TU-DO.',
        ['B xóa nhóm N-TU-DO', 'A (chưa tải lại trang) bấm Xóa ở dòng N-TU-DO, bấm Xóa'], '',
        ['Bước 1: B xóa thành công',
         'Bước 2: A nhận thông báo ' + DOI + '; tồn kho không bị trừ lần hai']),
]

# ================================================================== VI. TÙY CHỈNH CỘT
G6 = [
    moi('Mở cửa sổ Tuỳ chỉnh cột', 'P0', 'TK-A chưa từng tuỳ chỉnh cột ở màn này.',
        ['Bấm nút biểu tượng cột trên thanh công cụ (gợi ý "Cấu hình cột hiển thị")'], '',
        ['Mở cửa sổ "Tuỳ chỉnh cột" liệt kê các cột của bảng',
         'Các cột đang hiện trên bảng được tích sẵn',
         'STT, Tên hàng, Hành động bị khoá']),
    moi('Tắt một cột tuỳ chọn', 'P1', 'Bảng đang hiện cột Người cập nhật.',
        ['Mở Tuỳ chỉnh cột', 'Bỏ tích Người cập nhật', 'Bấm Lưu'], 'Cột tắt: Người cập nhật',
        ['Cột Người cập nhật biến mất khỏi bảng', 'Thứ tự và dữ liệu các cột còn lại không đổi']),
    cu('III', '003', func='Ẩn cột, kéo đổi thứ tự và ghi nhớ sau F5'),
    moi('Cột bắt buộc không tắt, không kéo đi được', 'P2', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
        ['Thử bỏ tích STT, Tên hàng, Hành động', 'Thử kéo ba dòng này sang vị trí khác'], '',
        ['Ba cột này không bỏ tích được, luôn hiện', 'Không kéo đổi vị trí được']),
    moi('Đóng cửa sổ mà không lưu thì không áp dụng thay đổi', 'P1', 'Bảng đang hiện cột Mã vị trí.',
        ['Mở Tuỳ chỉnh cột', 'Bỏ tích Mã vị trí và kéo đổi thứ tự một cột', 'Bấm Đóng (hoặc nút X)', 'Mở lại cửa sổ'], '',
        ['Bảng giữ nguyên cột Mã vị trí và thứ tự cột cũ',
         'Mở lại cửa sổ: Mã vị trí vẫn được tích, thứ tự như trước khi chỉnh']),
    moi('Cấu hình cột lưu riêng theo từng tài khoản', 'P2', 'TK-A đã tắt cột Người cập nhật và lưu. Tài khoản khác chưa chỉnh cột.',
        ['Đăng nhập tài khoản khác, vào màn', 'Đăng nhập lại TK-A ở trình duyệt khác, vào màn'], '',
        ['Tài khoản khác thấy bộ cột mặc định, có cột Người cập nhật',
         'TK-A vẫn không thấy cột Người cập nhật dù ở trình duyệt khác']),
    moi('Tuỳ chỉnh cột không ảnh hưởng dữ liệu và bộ lọc', 'P1', 'Đang lọc Kho = PTT, đứng ở trang 2.',
        ['Mở Tuỳ chỉnh cột, tắt cột Ngày cập nhật, bấm Lưu', 'Quan sát danh sách'], '',
        ['Vẫn lọc Kho = PTT, tổng số dòng không đổi',
         'Dữ liệu các dòng không đổi, chỉ ẩn cột Ngày cập nhật']),
]

# ================================================================== VII. XUẤT DANH SÁCH EXCEL
G7 = [
    cu('VIII', '001', func='Xuất Excel theo bộ lọc với trường đã chọn'),
    moi('Xuất file với tất cả trường', 'P1', 'Đang mở cửa sổ "Chọn trường xuất Excel".',
        ['Bấm Chọn tất cả', 'Bấm Xuất file, mở file tải về'], '',
        ['File có cột STT rồi đủ các cột: Tên hàng, Mã hàng, Kho, Mã vị trí, Vị trí, Công ty, ĐVT, Số lượng, Người nhập, '
         'Ngày nhập, Người cập nhật, Ngày cập nhật']),
    moi('Không chọn trường nào thì không xuất', 'P2', 'Đang mở cửa sổ "Chọn trường xuất Excel".',
        ['Bấm Bỏ chọn hết', 'Bấm Xuất file'], '',
        ['Chân cửa sổ ghi "Đang chọn 0/12 trường"',
         'Bấm Xuất file không có tác dụng, không tải file nào']),
    moi('Xuất theo từ khoá tìm nhanh', 'P1', 'Có nhóm N-TU-DO (2 dòng).',
        ['Gõ "EVOPYRO" vào ô tìm nhanh, nhấn Enter', 'Bấm Xuất Excel, Xuất file, mở file'], 'Ô tìm nhanh: EVOPYRO',
        ['File có đúng 2 dòng dữ liệu của BLNS-IR-EVOPYRO']),
    moi('Xuất lấy tất cả các trang, không chỉ trang đang xem', 'P0', 'Đang lọc Kho = PTT (25 dòng), 10 dòng/trang, ở trang 1.',
        ['Bấm Xuất Excel, Xuất file', 'Đếm dòng dữ liệu trong file'], '',
        ['File có đủ 25 dòng, không chỉ 10 dòng của trang đang xem']),
    cu('VIII', '002', func='Xuất khi không có dữ liệu'),
    moi('Tên file, tiêu đề và định dạng trong file', 'P1', 'Vừa xuất file với các trường mặc định.',
        ['Mở file tải về', 'Đọc dòng tiêu đề, tên cột, cột Ngày nhập và Số lượng'], '',
        ['Tên file Khai_bao_ton_dau_vat_ly.xlsx, dòng đầu "DANH SÁCH KHAI BÁO TỒN KHO ĐẦU KỲ"',
         'Tên cột Người tạo / Ngày tạo trên màn ra file là "Người nhập" / "Ngày nhập"',
         'Ngày dạng dd/mm/yyyy hh:mm; Số lượng là ô số, có phần lẻ thì giữ đúng (vd 406.81)',
         'Ô không có dữ liệu để TRỐNG']),
    moi('Dữ liệu trong file khớp với danh sách', 'P0', 'Đang lọc Kho = PTT; có hàng tên tiếng Việt có dấu.',
        ['Xuất file với các trường mặc định', 'Đối chiếu từng dòng trong file với bảng trên màn'], '',
        ['Số dòng trong file bằng N ở dòng tổng dưới bảng',
         'Tên hàng, Mã hàng, Kho, vị trí, Số lượng từng dòng trùng khớp bảng',
         'Chữ tiếng Việt có dấu hiển thị đúng, không lỗi phông']),
    cu('VIII', '003', func='Phạm vi công ty áp cho file xuất'),
]

# ================================================================== VIII. IMPORT TỪ FILE EXCEL
G8 = [
    cu('VII', '001', func='Mở cửa sổ Import và tải file mẫu'),
    moi('Các nút trong cửa sổ Import', 'P1', 'Đang mở cửa sổ "Import khai báo tồn kho đầu kỳ".',
        ['Quan sát các nút khi chưa chọn file', 'Bấm "Chọn file Excel", chọn file đúng mẫu', 'Bấm "Load lên bảng"',
         'Bấm Validate'], '',
        ['Nhóm File có "Chọn file Excel", "Tải file mẫu"; nhóm Hành động có "Load lên bảng", Validate, Import',
         'Chưa chọn file: "Load lên bảng", Validate, Import đều mờ',
         'Sau bước 3: bảng xem trước hiện đủ các dòng trong file; Validate bấm được, Import vẫn mờ',
         'Sau bước 4: Import chỉ bấm được khi mọi dòng hợp lệ']),
    moi('Tải lên file sai định dạng', 'P1', 'Có file .pdf và file .csv.',
        ['Bấm "Chọn file Excel", chọn file .pdf', 'Chọn file .csv'], '',
        ['Báo "Vui lòng chọn file .xlsx hoặc .xls", không nhận file, "Load lên bảng" vẫn mờ']),
    moi('Import file Excel không có dữ liệu', 'P2', 'File đúng mẫu nhưng chỉ có dòng tiêu đề và dòng hướng dẫn.',
        ['Chọn file, bấm "Load lên bảng"'], '',
        ['Báo "Không có dòng dữ liệu hợp lệ.", bảng xem trước trống',
         'Validate và Import vẫn mờ']),
    moi('Import file thiếu cột bắt buộc', 'P2', 'File mẫu đã xoá cột "Mã vị trí *", có 2 dòng dữ liệu.',
        ['Chọn file, Load lên bảng', 'Bấm Validate'], '',
        ['Cột Mã vị trí trên bảng xem trước để trống ở mọi dòng',
         'Validate: mọi dòng báo "Thiếu Mã vị trí", không dòng nào hợp lệ']),
    cu('VII', '002', func='Validate bắt lỗi từng cột'),
    cu('VII', '005', func='Cùng nhóm dùng 2 ĐVT hoặc trùng vị trí trong file'),
    moi('Mã có khoảng trắng đầu cuối trong file', 'P2', 'File H-1 hợp lệ nhưng ô Mã kho ghi " PTT " và Mã vị trí có khoảng trắng hai đầu.',
        ['Load, Validate'], 'Mã kho: " PTT "',
        ['Khoảng trắng hai đầu được bỏ qua, dòng hợp lệ như khi ghi "PTT"']),
    cu('VII', '003', func='Nhóm nhiều dòng phải khớp tồn kế toán, sửa dòng lỗi rồi Validate lại'),
    cu('VII', '004'),
    cu('VII', '006', func='Bỏ dòng lỗi rồi Import'),
    moi('Không có dòng hợp lệ thì không Import được', 'P1', 'File 2 dòng đều lỗi (mã hàng không tồn tại).',
        ['Load, Validate', 'Quan sát nút Import', 'Bấm "Bỏ dòng lỗi"'], '',
        ['Validate báo "Validate xong: 0 hợp lệ, 2 không hợp lệ"; mỗi dòng nêu lý do lỗi',
         'Nút Import mờ, không bấm được',
         'Bỏ dòng lỗi xong bảng không còn dòng nào, Import vẫn mờ; không ghi dữ liệu']),
    cu('VII', '007', func='File vượt quá 200 dòng'),
    cu('VII', '008', func='Nhóm bị người khác khai trước khi Import'),
    moi('Import lại cùng một file đã import thành công', 'P1', 'Vừa import thành công file H-1 (10) tại PTT / TPE.',
        ['Mở lại Import, chọn đúng file đó', 'Load, Validate'], '',
        ['Các dòng của H-1 báo "Hàng hóa H-1 đã được khai báo tồn đầu kỳ tại kho PTT, không thể nhập tiếp!"',
         'Không có dòng hợp lệ, không ghi trùng']),
    moi('Dữ liệu import dùng được ngay ở các màn liên quan', 'P1', 'Vừa import thành công H-1 = 10 tại vị trí A, kho PTT.',
        ['Đóng cửa sổ Import, xem danh sách', 'Mở ' + BC + ' lọc H-1'], '',
        ['Danh sách tự tải lại, có dòng H-1 với nút Sửa, Xóa',
         'Báo cáo có H-1 = 10 tại vị trí A, công ty TPE']),
]

# ================================================================== IX. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
G9 = [
    cu('IX', '001', func='Lưu cộng tồn kho đúng kho, vị trí, công ty'),
    cu('IX', '002', func='Phát sinh giao dịch thì khóa Sửa, Xóa', pre='H-1 đã khai ở TC_09.001.'),
    moi('Xóa khai báo thì thẻ kho bỏ dòng tồn đầu', 'P1', 'H-1 đã khai 10 tại PTT, chưa có giao dịch.',
        ['Xóa nhóm H-1 tại PTT', 'Mở ' + TK + ' của H-1 tại PTT'], '',
        ['Thẻ kho không còn dòng tồn đầu kỳ của H-1', 'Tồn H-1 tại PTT về như trước khi khai']),
    moi('Vị trí bị khóa không chọn được khi khai báo', 'P1', 'Kho PTT có vị trí V-KHOA đang bị khóa ở Danh mục vị trí.',
        ['Tạo mới, chọn Kho = PTT, Công ty = TPE, thêm H-1', 'Bấm ô Vị trí, tìm "V-KHOA"'], '',
        ['Cửa sổ "Chọn vị trí kho" không có V-KHOA',
         'Mở khóa V-KHOA ở danh mục rồi mở lại cửa sổ thì V-KHOA xuất hiện']),
    cu('IX', '005', func='Không xóa được kho, vị trí, hàng đã có khai báo'),
    cu('X', '001', func='Luồng nghiệp vụ: khai, sửa, xóa, khai lại'),
    cu('X', '002', func='Luồng nghiệp vụ: import rồi phát sinh giao dịch'),
]

# ================================================================== X. PHÂN QUYỀN
G10 = [
    cu('ROLE', '00'),
    cu('ROLE', '01', func='Có quyền thì dùng được đủ chức năng'),
    moi('Không có quyền nhưng mở thẳng đường dẫn trang Thêm', 'P1', 'TK-Z không có quyền "Khai báo tồn kho đầu kỳ".',
        ['Đăng nhập TK-Z', 'Dán đường dẫn trang Thêm khai báo tồn kho đầu kỳ lên thanh địa chỉ'], '',
        ['Báo "Bạn không có quyền thực hiện chức năng này"',
         'Không lưu được khai báo nào']),
    moi('Bị gỡ quyền khi đang khai báo', 'P1', 'TK-A đang ở trang Thêm, form hợp lệ. Quản trị vừa gỡ quyền "Khai báo tồn kho đầu kỳ" của TK-A.',
        ['TK-A bấm Lưu', 'TK-A tải lại màn danh sách'], '',
        ['Bước 1: bị từ chối, báo không có quyền; không có dòng khai báo mới, tồn kho không đổi',
         'Bước 2: menu không còn mục "Khai báo tồn kho đầu kỳ", bảng không có dữ liệu']),
    cu('ROLE', '02'),
    cu('ROLE', '03'),
    cu('ROLE', '04'),
]

SECTIONS = [(r, t, nhom(cs)) for r, t, cs in [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', G2),
    ('III', 'THÊM MỚI', G3),
    ('IV', 'CHỈNH SỬA', G4),
    ('V', 'XÓA', G5),
    ('VI', 'TÙY CHỈNH CỘT', G6),
    ('VII', 'XUẤT DANH SÁCH EXCEL', G7),
    ('VIII', 'IMPORT TỪ FILE EXCEL', G8),
    ('IX', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G9),
    ('X', 'PHÂN QUYỀN', G10),
]]

DESCRIPTION_BLOCK = [(t, _gach(b)) for t, b in V1.DESCRIPTION_BLOCK]

if __name__ == '__main__':
    con = sorted(set(OLD) - DA_DUNG)
    assert not con, 'Còn case cũ chưa đưa vào: %s' % con
    total = build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='phieu')
    print('Case cũ (bản 02/11): %d -> mới: %d (thêm %d)' % (SO_CU, total, total - SO_CU))
