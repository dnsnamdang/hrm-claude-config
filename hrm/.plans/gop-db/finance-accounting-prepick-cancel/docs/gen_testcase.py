# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu huỷ hàng giữ kế toán" — KHUÔN CHUẨN tab "13. DM quốc gia" (user chốt 03/11/2026, loại 'phieu').

Làm lại từ bản 02/11 (gen_testcase_v1.py — giữ để tra): lấy NGUYÊN VĂN mọi case nghiệp vụ của bản cũ (đã rà theo code
develop 02/11) qua hàm cu(<nhóm cũ>, <số cũ>), xếp lại vào đúng nhóm chuẩn; bỏ nhóm/mã kiểu cũ (TC-ROLE, LẬP PHIẾU, RÀNG
BUỘC NHẬP LIỆU, LUỒNG ĐẦU CUỐI…); viết thêm case cho các dòng checklist "Mẫu tài liệu.xlsx" áp dụng được mà bản cũ thiếu.
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

TEN = 'Phiếu huỷ hàng giữ kế toán'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SHEET = 'Trang tính1'
MODULE = V1.MODULE
NGAY = '03/11/2026'
MENU = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Giữ hàng > Phiếu huỷ hàng giữ kế toán'
CHUA_LUU = '"Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"'


def _gach(text):
    """Giọng tab Quốc gia: mỗi ý Expected bắt đầu "-  "."""
    out = []
    for line in str(text).split('\n'):
        if line.startswith('- ') and not line.startswith('-  '):
            line = '-  ' + line[2:]
        out.append(line)
    return '\n'.join(out)


# ------------------------------------------------------------------ case cũ (nguyên văn, đã rà ở v1)
OLD = {('ROLE', c[0]): c for c in V1.ROLE_NEW}
for _k, _t, _cs in V1.SECTIONS_NEW:
    for _c in _cs:
        OLD[(_k, _c[0])] = _c
SO_CU = len(OLD)
DA_DUNG = set()


def cu(nhom, so, func=None, pre=None, steps=None, data=None, exp=None, prio=None):
    """Lấy nguyên văn case cũ; tham số khác None = sửa câu chữ ô đó."""
    key = (nhom, so)
    assert key not in DA_DUNG, 'Case cũ dùng 2 lần: %s' % (key,)
    DA_DUNG.add(key)
    _, f, p, pr, st, td, ex = OLD[key]
    td = '' if td == '—' else td
    return (func or f, prio or p, pre or pr, steps or st, td if data is None else data, _gach(exp or ex))


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
    cu('I', '001', func='Mở màn hình từ menu',
       steps='1. Đăng nhập bằng B.\n2. Vào menu ' + MENU + '.'),
    cu('I', '002'),
    moi('Các nút chức năng trên màn danh sách', 'P0', 'Tài khoản B có quyền "Quản lý giữ hàng".',
        ['Mở màn danh sách', 'Quan sát thanh công cụ của bảng và khu vực tìm kiếm'], '',
        ['Thanh công cụ của bảng có lần lượt: Tạo mới, In, Xuất Excel, nút biểu tượng cột (gợi ý "Cấu hình cột hiển thị")',
         'Khu vực tìm kiếm có ô tìm nhanh (gợi ý "Tìm theo mã phiếu..."), nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
         'KHÔNG có nút Import Excel']),
    cu('I', '003', func='Các cột mặc định hiển thị và mặc định ẩn'),
    cu('I', '004'),
    cu('I', '006'),
    moi('Dữ liệu trên bảng khớp với phiếu vừa lập', 'P0',
        'Kế toán B vừa lập phiếu huỷ hàng giữ của nhân viên N, ghi chú "huỷ test 01".',
        ['Mở màn danh sách, đọc dòng đầu tiên', 'Bật cột Ghi chú ở Cấu hình cột hiển thị, đọc lại dòng đó'], 'Ghi chú: huỷ test 01',
        ['Mã phiếu dạng KTPHHG-xxxxx (5 chữ số), là phiếu vừa lập',
         'Hủy của nhân viên = N; Người tạo = "<họ tên B> - <mã phòng ban của B>"; Ngày tạo đúng thời điểm lập, dạng dd/mm/yyyy hh:mm',
         'Người cập nhật, Ngày cập nhật trùng Người tạo, Ngày tạo (phiếu không sửa được)',
         'Cột Ghi chú hiện "huỷ test 01"']),
    cu('III', '008', func='Ô không có dữ liệu để trống'),
    moi('Danh sách khi chưa có phiếu nào', 'P2',
        'Môi trường kiểm thử: công ty của tài khoản B chưa có phiếu huỷ hàng giữ kế toán nào.',
        ['Vào menu ' + MENU, 'Quan sát bảng và dòng dưới bảng'], '',
        ['Bảng hiện dòng "Không có dữ liệu phù hợp."',
         'Dòng dưới bảng hiện "Không có phiếu nào."',
         'Màn hình không báo lỗi; các nút Tạo mới, In, Xuất Excel vẫn dùng được']),
    cu('I', '007', func='Không có dữ liệu phù hợp bộ lọc',
       exp='- Bảng hiện dòng "Không có dữ liệu phù hợp.".\n- Dòng dưới bảng hiện "Không có phiếu nào.", không có thông báo lỗi.'),
    # --- phân trang
    moi('Số dòng mặc định và các lựa chọn số dòng/trang', 'P1', 'Danh sách có 580 phiếu.',
        ['Mở màn danh sách', 'Mở ô "Số dòng/trang" ở góc dưới bên phải bảng'], '',
        ['Mặc định hiển thị 10 dòng/trang',
         'Ô "Số dòng/trang" cho chọn 5 / 10 / 20 / 50 / 100']),
    cu('III', '004', func='Đổi số dòng mỗi trang thì về trang 1',
       pre='Danh sách có 580 phiếu, đang 10 dòng/trang và đứng ở trang 3.'),
    moi('Nút sang trang kế tiếp và lùi về trang trước', 'P0', 'Danh sách có 580 phiếu, đang ở trang 1, 10 dòng/trang.',
        ['Bấm nút › (trang kế tiếp)', 'Đọc thanh phân trang và dòng tổng', 'Bấm nút ‹ (trang trước)', 'Đọc lại'], '',
        ['Bước 2: sang trang 2, số trang 2 được tô đậm, dòng tổng hiện "Hiển thị 11–20 / 580"',
         'Bước 4: về trang 1, dòng tổng hiện "Hiển thị 1–10 / 580"',
         'Dữ liệu hai trang không lặp, không thiếu phiếu']),
    moi('Nút về trang cuối và về trang đầu', 'P0', 'Danh sách có 580 phiếu, đang ở trang 1, 10 dòng/trang.',
        ['Bấm nút » (về trang cuối)', 'Đọc dòng tổng và STT dòng cuối', 'Bấm nút « (về trang đầu)'], '',
        ['Bước 2: đứng ở trang 58, dòng tổng hiện "Hiển thị 571–580 / 580", STT dòng cuối = 580',
         'Bước 3: về trang 1, dòng tổng hiện "Hiển thị 1–10 / 580"']),
    moi('Nút phân trang ở trang đầu và trang cuối', 'P1', 'Danh sách có nhiều hơn 1 trang.',
        ['Đứng ở trang 1, quan sát hai nút « và ‹', 'Bấm » về trang cuối, quan sát hai nút › và »'], '',
        ['Ở trang 1: nút « và ‹ bị mờ, bấm không có tác dụng',
         'Ở trang cuối: nút › và » bị mờ, bấm không có tác dụng']),
    cu('III', '005', func='Số thứ tự liên tục qua các trang, giữ nguyên bộ lọc'),
    moi('Áp dụng bộ lọc khi đang ở trang giữa thì về trang 1', 'P1',
        'Danh sách có 580 phiếu, đang đứng ở trang 5. Kế toán B đã lập 12 phiếu.',
        ['Mở Tìm kiếm nâng cao', 'Chọn Người tạo = B', 'Quan sát thanh phân trang và dòng tổng'], 'Người tạo: B',
        ['Bảng quay về trang 1, dòng tổng hiện "Hiển thị 1–10 / 12"',
         'Không còn đứng ở trang 5 (trang không tồn tại với kết quả mới)']),
    # --- sắp xếp
    moi('Thứ tự mặc định khi mở màn', 'P1', 'Vừa lập phiếu mới. Chưa bấm sắp xếp cột nào.',
        ['Vào menu ' + MENU, 'Đọc 5 dòng đầu'], '',
        ['Phiếu vừa lập nằm ở dòng đầu tiên, STT = 1',
         'Các dòng xếp theo Ngày tạo mới nhất ở trên, càng xuống càng cũ',
         'Không cột nào hiện mũi tên đang sắp xếp']),
    cu('III', '001', func='Sắp xếp theo cột Mã phiếu'),
    cu('III', '002', func='Sắp xếp theo Ngày tạo và Ngày cập nhật'),
    cu('III', '003', func='Các cột không cho sắp xếp'),
    moi('Sắp xếp giữ nguyên khi chuyển trang', 'P1', 'Đang sắp xếp Mã phiếu giảm dần, 10 dòng/trang.',
        ['Ghi lại mã phiếu dòng cuối trang 1', 'Bấm sang trang 2', 'So mã phiếu dòng đầu trang 2'], '',
        ['Trang 2 vẫn sắp xếp Mã phiếu giảm dần, mũi tên ở tiêu đề cột không đổi',
         'Mã dòng đầu trang 2 nhỏ hơn liền kề mã dòng cuối trang 1, không lặp hay sót phiếu']),
]

# ================================================================== II. TÌM KIẾM & LỌC DANH SÁCH
G2 = [
    moi('Tìm nhanh đúng nguyên mã phiếu', 'P0', 'Tồn tại phiếu KTPHHG-00604.',
        ['Gõ "KTPHHG-00604" vào ô tìm nhanh', 'Nhấn Enter'], 'Ô tìm nhanh: KTPHHG-00604',
        ['Danh sách còn đúng 1 phiếu KTPHHG-00604',
         'Dòng tổng hiện "Hiển thị 1–1 / 1"']),
    cu('II', '001', func='Tìm nhanh theo một phần mã phiếu'),
    moi('Tìm nhanh không phân biệt chữ hoa chữ thường', 'P1', 'Tồn tại phiếu KTPHHG-00604.',
        ['Gõ "ktphhg-00604", bấm Tìm kiếm, ghi nhận kết quả', 'Xoá, gõ "KTPHHG-00604", bấm Tìm kiếm', 'So sánh'],
        'Ô tìm nhanh: ktphhg-00604 / KTPHHG-00604',
        ['Hai lần tìm cho ra CÙNG kết quả: phiếu KTPHHG-00604']),
    cu('II', '002'),
    cu('II', '003', func='Ô tìm nhanh chỉ lọc khi bấm Tìm kiếm hoặc Enter'),
    moi('Tìm nhanh với ký tự đặc biệt', 'P2', 'Không có mã phiếu nào chứa chuỗi "@#$%".',
        ['Gõ "@#$%" vào ô tìm nhanh', 'Bấm Tìm kiếm'], 'Ô tìm nhanh: @#$%',
        ['Bảng hiện "Không có dữ liệu phù hợp.", dòng dưới bảng hiện "Không có phiếu nào."',
         'Màn hình không treo, không báo lỗi hệ thống']),
    moi('Tìm nhanh có khoảng trắng đầu và cuối', 'P2', 'Tồn tại phiếu KTPHHG-00604.',
        ['Gõ "   00604   " (có khoảng trắng hai đầu) vào ô tìm nhanh', 'Bấm Tìm kiếm'], 'Ô tìm nhanh: "   00604   "',
        ['Ra đúng phiếu KTPHHG-00604, giống khi gõ "00604" không có khoảng trắng']),
    moi('Giới hạn độ dài ô tìm nhanh', 'P2', 'Đang ở màn danh sách.',
        ['Dán chuỗi 300 ký tự vào ô tìm nhanh', 'Bấm Tìm kiếm', 'Bấm Làm mới'], 'Chuỗi 300 ký tự (vd "abcde" lặp 60 lần)',
        ['Bước 2: bảng hiện "Không có dữ liệu phù hợp."; màn hình không treo, không báo lỗi hệ thống',
         'Bước 3: ô tìm nhanh trống, bảng về toàn bộ danh sách']),
    moi('Xóa từ khóa thì danh sách quay về đầy đủ', 'P0', 'Danh sách có 580 phiếu. Đang tìm "00604", còn 1 phiếu.',
        ['Xóa hết nội dung ô tìm nhanh', 'Nhấn Enter'], '',
        ['Dòng tổng quay lại "Hiển thị 1–10 / 580"',
         'Bảng về trang 1']),
    cu('II', '004', func='Các ô lọc ở Tìm kiếm nâng cao và giá trị mặc định',
       exp='- Có 4 ô: Hủy của nhân viên, Người tạo, Tên/mã hàng hóa (gợi ý "Nhập tên hoặc mã hàng hóa"), Ngày tạo.\n'
           '- Mọi ô mặc định để TRỐNG (không lọc), danh sách hiện mọi phiếu trong phạm vi.\n'
           '- KHÔNG có ô Trạng thái và ô Công ty.'),
    cu('II', '005', func='Lọc theo Hủy của nhân viên'),
    cu('II', '006'),
    cu('II', '007'),
    cu('II', '008'),
    cu('II', '009', func='Lọc khoảng Ngày tạo lấy trọn hai đầu mút'),
    cu('II', '011'),
    cu('II', '010', func='Lọc kết hợp nhiều tiêu chí'),
    moi('Kết hợp ô tìm nhanh với ô lọc', 'P1', 'Kế toán B lập 12 phiếu, trong đó 2 phiếu có mã chứa "006".',
        ['Mở Tìm kiếm nâng cao, chọn Người tạo = B', 'Gõ "006" vào ô tìm nhanh, bấm Tìm kiếm'], 'Người tạo: B\nÔ tìm nhanh: 006',
        ['Còn đúng 2 phiếu: mã chứa "006" VÀ Người tạo là B',
         'Dòng tổng hiện "Hiển thị 1–2 / 2"']),
    moi('Lọc ra kết quả rỗng', 'P1', 'Nhân viên M đang làm việc nhưng chưa bị huỷ hàng ở phiếu nào.',
        ['Mở Tìm kiếm nâng cao', 'Chọn Hủy của nhân viên = M'], 'Hủy của nhân viên: M',
        ['Bảng hiện "Không có dữ liệu phù hợp."',
         'Dòng dưới bảng hiện "Không có phiếu nào."']),
    moi('Tổng số và phân trang sau khi lọc', 'P0', 'Kế toán B đã lập 25 phiếu. Danh sách 10 dòng/trang.',
        ['Chọn Người tạo = B', 'Đọc dòng tổng và thanh phân trang', 'Bấm sang trang 3'], 'Người tạo: B',
        ['Bước 2: dòng tổng hiện "Hiển thị 1–10 / 25", thanh phân trang có 3 trang',
         'Bước 3: dòng tổng hiện "Hiển thị 21–25 / 25", trang 3 có 5 dòng, STT từ 21 đến 25']),
    moi('Sắp xếp trên kết quả đã lọc', 'P2', 'Đang lọc Người tạo = B (25 phiếu).',
        ['Bấm tiêu đề cột Mã phiếu', 'Đọc cột Người tạo và cột Mã phiếu'], '',
        ['Vẫn chỉ có phiếu do B lập, tổng vẫn 25, ô lọc Người tạo vẫn là B',
         'Mã phiếu xếp tăng dần, bảng về trang 1']),
    cu('II', '012', func='Nút Làm mới xóa hết điều kiện lọc và sắp xếp'),
    cu('II', '013', func='Mở chi tiết phiếu rồi Quay lại thì giữ bộ lọc'),
    moi('Rời sang màn khác rồi quay lại thì bộ lọc về mặc định', 'P1', 'Đang lọc Người tạo = B, ô tìm nhanh "006".',
        ['Vào menu Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Giữ hàng > Danh sách hàng giữ',
         'Quay lại màn Phiếu huỷ hàng giữ kế toán bằng menu', 'Quan sát khu vực tìm kiếm và bảng'], 'Người tạo: B\nÔ tìm nhanh: 006',
        ['Ô tìm nhanh và các ô lọc trở về trống',
         'Bảng hiện toàn bộ danh sách ở trang 1, dòng tổng bằng tổng số phiếu như lúc mới mở màn']),
    moi('Tải lại trang (F5) khi đang lọc', 'P2', 'Vừa vào màn từ menu, chưa mở chi tiết phiếu nào. Đang lọc Người tạo = B.',
        ['Nhấn F5 tải lại trang', 'Quan sát khu vực tìm kiếm và bảng'], 'Người tạo: B',
        ['Các ô lọc trở về trống',
         'Bảng hiện toàn bộ danh sách ở trang 1 với 10 dòng/trang']),
    moi('Mở màn ở tab trình duyệt mới khi tab cũ đang lọc', 'P2', 'Tab 1 đang mở màn danh sách, chưa mở chi tiết phiếu nào.',
        ['Ở tab 1: chọn Người tạo = B', 'Mở tab mới, vào màn danh sách bằng menu', 'Quan sát tab 2', 'Quay lại tab 1'],
        'Người tạo: B',
        ['Tab 2: các ô lọc trống, bảng hiện toàn bộ danh sách ở trang 1',
         'Tab 1: vẫn giữ Người tạo = B và kết quả đang xem']),
    moi('Đăng xuất, đăng nhập tài khoản khác trên cùng trình duyệt', 'P1',
        'Hai tài khoản B và D cùng công ty, đều có quyền "Quản lý giữ hàng". Dùng chung một trình duyệt.',
        ['Đăng nhập B, vào màn danh sách, chọn Người tạo = B, ô tìm nhanh "006"', 'Đăng xuất',
         'Đăng nhập D, vào màn danh sách'], 'Người tạo: B\nÔ tìm nhanh: 006',
        ['D thấy ô tìm nhanh và các ô lọc trống, bảng hiện toàn bộ danh sách ở trang 1',
         'Điều kiện lọc của B KHÔNG hiện sang tài khoản D']),
    cu('II', '014', func='Cài đặt bộ lọc: tắt bớt ô lọc'),
]

# ================================================================== III. THÊM MỚI
G3 = [
    cu('IV', '001', func='Mở trang Thêm phiếu'),
    cu('IV', '002'),
    cu('IV', '003'),
    cu('IV', '004', func='Nội dung cửa sổ Hàng đang giữ của nhân viên'),
    cu('IV', '005'),
    cu('IV', '006'),
    cu('IV', '007'),
    cu('IV', '008'),
    cu('IV', '009'),
    cu('IV', '010'),
    cu('IV', '011'),
    cu('IV', '012'),
    cu('IV', '013'),
    cu('IV', '014'),
    cu('V', '001'),
    cu('V', '002'),
    cu('V', '003'),
    cu('V', '004'),
    cu('V', '005'),
    cu('V', '006'),
    cu('V', '009'),
    moi('Ô Khách hàng luôn có giá trị', 'P1', 'Đã thêm hàng H, dòng khách đầu tiên đang chọn K1.',
        ['Quan sát ô Khách hàng của dòng K1', 'Thử xoá trống ô Khách hàng'], '',
        ['Ô Khách hàng có dấu bắt buộc, KHÔNG có nút x xoá giá trị',
         'Chỉ đổi được sang khách khác, không để trống được']),
    cu('VI', '001'),
    cu('VI', '002'),
    cu('VI', '003'),
    cu('VI', '004'),
    cu('VI', '005'),
    cu('VI', '006'),
    cu('VI', '007'),
    # --- validate
    cu('VIII', '001', func='Bỏ trống Duyệt hủy thì bị chặn'),
    cu('VIII', '002'),
    cu('VIII', '003', func='Nhập Duyệt hủy bằng 0 thì báo lỗi'),
    cu('VIII', '004', func='Nhập vượt Có thể hủy thì báo lỗi, giữ nguyên số đã nhập'),
    cu('VIII', '005', func='Thông báo lỗi mất ngay khi sửa về số hợp lệ'),
    cu('VIII', '006'),
    cu('VIII', '007'),
    cu('VIII', '008'),
    cu('VIII', '009'),
    moi('Nhập Ghi chú đúng 255 ký tự thì lưu được', 'P1', 'Phiếu hợp lệ, đã có hàng hoá và số lượng.',
        ['Nhập Ghi chú dài đúng 255 ký tự', 'Bấm Duyệt, xác nhận', 'Mở chi tiết phiếu vừa lập'], 'Ghi chú: chuỗi 255 ký tự',
        ['Không báo lỗi ô Ghi chú, lập phiếu thành công',
         'Ô Ghi chú ở chi tiết hiện đủ 255 ký tự, không bị cắt']),
    cu('VIII', '010', func='Nhập Ghi chú vượt 255 ký tự'),
    cu('VIII', '011'),
    moi('Ghi chú có khoảng trắng đầu cuối hoặc chỉ toàn khoảng trắng', 'P2', 'Phiếu hợp lệ, đã có hàng hoá và số lượng.',
        ['Nhập Ghi chú "   huỷ test   " (khoảng trắng hai đầu), Duyệt, xác nhận, mở chi tiết',
         'Lập phiếu khác, Ghi chú chỉ gõ vài dấu cách, Duyệt, xác nhận, mở chi tiết'],
        'Ghi chú: "   huỷ test   " / "     "',
        ['Bước 1: Ghi chú lưu là "huỷ test", không còn khoảng trắng hai đầu',
         'Bước 2: lập thành công, ô Ghi chú ở chi tiết để TRỐNG']),
    cu('VIII', '012'),
    # --- Lưu và tiếp tục
    cu('IV', '016'),
    moi('Lưu và tiếp tục khi chưa nhập số lượng', 'P1', 'Đã chọn nhân viên N, thêm hàng H, dòng K1 chưa nhập Duyệt hủy.',
        ['Bấm "Lưu và tiếp tục"'], 'Duyệt hủy: (để trống)',
        ['Dưới ô hiện chữ đỏ "Chưa nhập số lượng"; thông báo "Bạn chưa nhập đầy đủ thông tin."',
         'KHÔNG hiện hộp xác nhận, vẫn ở trang Thêm, nhân viên và hàng hoá đã chọn còn nguyên',
         'Không có phiếu mới ở danh sách']),
    moi('Lưu và tiếp tục khi nhập vượt Có thể hủy', 'P1', 'Dòng K1 hàng H, ĐVT Cái, Có thể hủy = 5.',
        ['Gõ 7 vào Duyệt hủy', 'Bấm "Lưu và tiếp tục"'], 'Duyệt hủy: 7',
        ['Báo đỏ dưới ô "Vượt quá số có thể hủy (tối đa 5)", ô giữ nguyên số 7',
         'Thông báo lỗi kèm tên hàng H, không hiện hộp xác nhận, không lưu',
         'Sửa thành 5 rồi bấm lại "Lưu và tiếp tục" thì lập thành công, trang Thêm trống để lập tiếp']),
    moi('Bấm Lưu và tiếp tục rồi bấm Quay lại ngay thì không hỏi', 'P2', 'Phiếu hợp lệ trên trang Thêm.',
        ['Bấm "Lưu và tiếp tục", xác nhận Duyệt', 'Không nhập gì thêm vào trang Thêm trống', 'Bấm Quay lại'], '',
        ['Phiếu vừa lập có trong danh sách',
         'Bấm Quay lại về thẳng danh sách, KHÔNG hiện hộp "Thông tin chưa lưu"']),
    # --- đóng khi chưa lưu
    cu('IV', '015', func='Bấm Quay lại khi đã nhập thông tin'),
    moi('Nhập Ghi chú rồi xoá hết, bấm Quay lại thì không hỏi', 'P2', 'Trang Thêm vừa mở, chưa chọn nhân viên.',
        ['Gõ vài ký tự vào ô Ghi chú', 'Xoá hết để ô trống trở lại', 'Bấm Quay lại'], '',
        ['Về thẳng danh sách, KHÔNG hiện hộp "Thông tin chưa lưu"',
         'Không có phiếu mới']),
    moi('Rời trang Thêm bằng menu khi đã nhập', 'P2', 'Đã chọn nhân viên N và thêm 1 hàng hoá, chưa Duyệt.',
        ['Bấm một mục menu khác (vd Danh sách hàng giữ)', 'Bấm Ở lại', 'Bấm lại mục menu đó, chọn Thoát'], '',
        ['Hiện hộp "Thông tin chưa lưu": ' + CHUA_LUU + ' với 2 nút Thoát, Ở lại',
         'Ở lại: vẫn ở trang Thêm, dữ liệu còn nguyên',
         'Thoát: sang màn đã chọn, không có phiếu mới, hàng giữ không đổi']),
    cu('IV', '017'),
]

# ================================================================== IV. DUYỆT PHIẾU
G4 = [
    moi('Điều kiện hiển thị nút Duyệt', 'P0', 'Nhân viên N đang giữ hàng H.',
        ['Mở trang Thêm, quan sát chân trang', 'Chọn N ở ô "Hủy của nhân viên"', 'Thêm hàng H',
         'Bấm thùng rác xoá hàng H khỏi phiếu'], '',
        ['Bước 1 và 2: nút "Duyệt", "Lưu và tiếp tục" ẨN (không phải hiện mờ)',
         'Bước 3: hai nút hiện ra',
         'Bước 4: bảng không còn hàng hoá, hai nút ẩn lại']),
    cu('VII', '001', func='Hộp xác nhận trước khi duyệt'),
    cu('VII', '002', func='Bấm Hủy ở hộp xác nhận thì không lập phiếu'),
    cu('VII', '003', func='Duyệt phiếu thành công quay về danh sách'),
    cu('VII', '004', func='Hàng giữ bị trừ đúng số sau khi duyệt'),
    cu('VII', '005'),
    cu('VII', '006'),
    cu('VII', '007'),
    cu('V', '007'),
    cu('VII', '010'),
    cu('VII', '011'),
    cu('VII', '012'),
    cu('VII', '008', func='Phiếu đã duyệt không duyệt lại, không sửa, không xoá được'),
    cu('VII', '009', func='Bấm Duyệt liên tục chỉ tạo một phiếu'),
    cu('XIV', '001', func='Hai kế toán cùng duyệt huỷ một hàng giữ'),
    cu('XIV', '002'),
    cu('XIV', '003'),
    cu('XI', '001', func='Nhân viên bị huỷ hàng nhận thông báo sau khi duyệt'),
    cu('XI', '002', func='Bấm thông báo mở đúng chi tiết phiếu'),
    cu('XI', '003'),
    cu('XI', '004'),
]

# ================================================================== V. LỊCH SỬ THAY ĐỔI
G5 = [
    cu('X', '003', func='Mở cửa sổ Lịch sử từ cột Hành động'),
    cu('X', '001', func='Lịch sử ngay sau khi lập phiếu'),
    cu('X', '002', func='Mở, làm mới, thu gọn khối lịch sử ở chi tiết'),
    cu('X', '004'),
    moi('Mở bộ lọc trong cửa sổ Lịch sử', 'P1', 'Phiếu KTPHHG-00605 có lịch sử.',
        ['Mở Lịch sử của KTPHHG-00605', 'Bấm nút Bộ lọc', 'Bấm Bộ lọc lần nữa'], '',
        ['Bước 2: hiện 4 ô Loại hành động (gợi ý "Tất cả loại hành động"), Người thực hiện (gợi ý "Tất cả người thực hiện"), '
         'Từ ngày, Đến ngày và 2 nút Tìm kiếm, Làm mới',
         'Bước 3: khu vực bộ lọc thu gọn lại']),
    moi('Lọc lịch sử theo Loại hành động và Người thực hiện', 'P1',
        'Phiếu KTPHHG-00605 do Trần Thị Bình lập, có mốc Tạo mới.',
        ['Mở Lịch sử, bấm Bộ lọc', 'Chọn Loại hành động = Tạo mới, Người thực hiện = Trần Thị Bình', 'Bấm Tìm kiếm'],
        'Loại hành động: Tạo mới\nNgười thực hiện: Trần Thị Bình',
        ['Mốc Tạo mới của Trần Thị Bình vẫn hiện đủ thời điểm, người thực hiện, ghi chú số lô đã trừ']),
    moi('Lọc lịch sử theo thời gian không có kết quả rồi Làm mới', 'P1', 'Phiếu KTPHHG-00605 lập ngày 29/09/2026.',
        ['Mở Lịch sử, bấm Bộ lọc', 'Chọn Từ ngày 01/09/2026, Đến ngày 10/09/2026, bấm Tìm kiếm', 'Bấm Làm mới'],
        'Từ ngày: 01/09/2026\nĐến ngày: 10/09/2026',
        ['Bước 2: hiện câu "Không có lịch sử phù hợp bộ lọc."',
         'Bước 3: các ô lọc về trống, mốc Tạo mới hiện lại']),
    moi('Đóng cửa sổ Lịch sử', 'P2', 'Danh sách đang lọc Người tạo = B và đứng ở trang 2.',
        ['Bấm nút Lịch sử ở một dòng', 'Bấm Đóng (hoặc nút X)'], '',
        ['Cửa sổ đóng, danh sách vẫn ở trang 2 và giữ bộ lọc Người tạo = B',
         'Dữ liệu trên bảng không thay đổi']),
]

# ================================================================== VI. XEM CHI TIẾT PHIẾU
G6 = [
    cu('I', '005', func='Mở chi tiết bằng cách bấm Mã phiếu'),
    cu('IX', '001', func='Nội dung khối Thông tin chung ở chi tiết'),
    cu('IX', '002', func='Bảng hàng hoá ở chi tiết'),
    moi('Dữ liệu chi tiết khớp dòng trên danh sách và dữ liệu đã lập', 'P0',
        'Vừa lập phiếu huỷ hàng của N: H1 cho K1 = 2, K2 = 1 Hộp; ghi chú "huỷ test 02".',
        ['Đọc dòng của phiếu trên danh sách', 'Bấm Mã phiếu mở chi tiết, đối chiếu'], '',
        ['Mã phiếu, Hủy của nhân viên, Người tạo, ngày giờ tạo ở chi tiết trùng với dòng trên danh sách',
         'Bảng chi tiết có H1 gộp 2 dòng: K1 Duyệt hủy 2 (ĐVT cơ bản), K2 Duyệt hủy 1, ĐVT Hộp — đúng số đã nhập lúc lập',
         'Ghi chú "huỷ test 02"']),
    cu('IX', '003'),
    cu('IX', '008'),
    cu('IX', '004', func='Các nút ở cuối màn chi tiết'),
    cu('IX', '005', func='Quay lại danh sách giữ bộ lọc'),
    cu('IX', '006'),
    cu('IX', '007'),
]

# ================================================================== VII. IN PHIẾU
G7 = [
    cu('XII', '001'),
    cu('XII', '002'),
    cu('XII', '003'),
    cu('XII', '004'),
    cu('XII', '005'),
    cu('XII', '006'),
    moi('In danh sách khi không có phiếu nào khớp', 'P2', 'Đang lọc Hủy của nhân viên = M, không có phiếu nào.',
        ['Bấm In trên thanh công cụ danh sách'], 'Hủy của nhân viên: M',
        ['Cửa sổ xem trước vẫn mở, bảng in ghi "Không có dữ liệu"',
         'Dòng "Tổng số phiếu: 0"; không báo lỗi']),
    cu('XII', '007'),
]

# ================================================================== VIII. TÙY CHỈNH CỘT
G8 = [
    moi('Mở cửa sổ Tuỳ chỉnh cột', 'P0', 'Tài khoản chưa từng tuỳ chỉnh cột ở màn này.',
        ['Bấm nút biểu tượng cột trên thanh công cụ (gợi ý "Cấu hình cột hiển thị")'], '',
        ['Mở cửa sổ "Tuỳ chỉnh cột" liệt kê đủ 9 cột: STT, Mã phiếu, Hủy của nhân viên, Ngày tạo, Người tạo, Người cập nhật, '
         'Ngày cập nhật, Ghi chú, Hành động',
         'Tích sẵn 8 cột đang hiện; Ghi chú chưa tích',
         'Có nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng']),
    cu('III', '006', func='Bật cột đang ẩn mặc định'),
    moi('Tắt một cột tuỳ chọn', 'P1', 'Bảng đang hiện cột Người cập nhật.',
        ['Mở Tuỳ chỉnh cột', 'Bỏ tích Người cập nhật', 'Bấm Lưu'], 'Cột tắt: Người cập nhật',
        ['Cột Người cập nhật biến mất khỏi bảng',
         'Thứ tự và dữ liệu các cột còn lại không đổi']),
    cu('III', '007', func='Cột bắt buộc không tắt được'),
    moi('Kéo thả đổi thứ tự cột', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
        ['Kéo biểu tượng ba gạch của Ngày tạo lên trên Hủy của nhân viên', 'Bấm Lưu', 'Quan sát bảng'], '',
        ['Trên bảng, cột Ngày tạo đứng trước cột Hủy của nhân viên',
         'Dữ liệu từng cột vẫn đúng']),
    moi('Đóng cửa sổ mà không lưu thì không áp dụng thay đổi', 'P1', 'Bảng đang hiện cột Người tạo.',
        ['Mở Tuỳ chỉnh cột', 'Bỏ tích Người tạo và kéo đổi thứ tự một cột', 'Bấm Đóng (hoặc nút X)', 'Mở lại cửa sổ'], '',
        ['Bảng giữ nguyên cột Người tạo và thứ tự cột cũ',
         'Mở lại cửa sổ: Người tạo vẫn được tích, thứ tự như trước khi chỉnh']),
    moi('Cấu hình cột được ghi nhớ sau khi tải lại trang', 'P0', 'Vừa bật cột Ghi chú và tắt cột Người cập nhật, đã Lưu.',
        ['Nhấn F5', 'Chuyển sang màn khác rồi quay lại màn danh sách'], '',
        ['Cả hai lần: cột Ghi chú vẫn hiện, cột Người cập nhật vẫn ẩn',
         'Không phải cấu hình lại']),
    moi('Cấu hình cột lưu riêng theo từng tài khoản', 'P2',
        'Tài khoản B đã bật cột Ghi chú và lưu. Tài khoản D cùng quyền chưa chỉnh cột.',
        ['Đăng nhập D, vào màn danh sách', 'Đăng nhập lại B ở trình duyệt khác, vào màn danh sách'], '',
        ['D thấy bộ cột mặc định, KHÔNG có cột Ghi chú',
         'B vẫn thấy cột Ghi chú dù đăng nhập ở trình duyệt khác']),
    moi('Tuỳ chỉnh cột không ảnh hưởng dữ liệu và bộ lọc', 'P1', 'Đang lọc Người tạo = B (12 phiếu), đứng ở trang 2.',
        ['Mở Tuỳ chỉnh cột, bật Ghi chú, bấm Lưu', 'Quan sát danh sách'], '',
        ['Vẫn lọc Người tạo = B, tổng vẫn 12',
         'Dữ liệu các dòng không đổi, chỉ thêm cột Ghi chú']),
]

# ================================================================== IX. XUẤT DANH SÁCH EXCEL
G9 = [
    cu('XIII', '001', func='Mở cửa sổ chọn trường xuất file'),
    cu('XIII', '002', func='Xuất file theo bộ lọc với các trường mặc định'),
    moi('Xuất file với tất cả trường', 'P1', 'Đang mở cửa sổ "Chọn trường xuất Excel".',
        ['Bấm Chọn tất cả', 'Bấm Xuất file, mở file tải về'], '',
        ['Chân cửa sổ ghi "Đang chọn 7/7 trường"',
         'File có cột STT rồi đủ 7 cột: Mã phiếu, Hủy của nhân viên, Ngày tạo, Người tạo, Người cập nhật, Ngày cập nhật, Ghi chú']),
    cu('XIII', '003', func='Xuất một số trường theo thứ tự đã kéo'),
    cu('XIII', '006', func='Không chọn trường nào thì không xuất'),
    moi('Xuất theo từ khoá tìm nhanh', 'P1', 'Có 11 phiếu có mã chứa "0060".',
        ['Gõ "0060" vào ô tìm nhanh, bấm Tìm kiếm', 'Bấm Xuất Excel, Xuất file, mở file'], 'Ô tìm nhanh: 0060',
        ['File có đúng 11 dòng dữ liệu, mọi mã phiếu đều chứa "0060"']),
    moi('Xuất lấy tất cả các trang, không chỉ trang đang xem', 'P0',
        'Đang lọc Người tạo = B (25 phiếu), 10 dòng/trang, đang ở trang 1.',
        ['Bấm Xuất Excel, Xuất file', 'Đếm dòng dữ liệu trong file'], '',
        ['File có đủ 25 dòng, không chỉ 10 dòng của trang đang xem',
         'Thứ tự dòng giống thứ tự trên bảng']),
    moi('Xuất khi danh sách không có dòng nào', 'P2', 'Đang lọc Hủy của nhân viên = M, không có phiếu nào.',
        ['Bấm Xuất Excel, Xuất file', 'Mở file tải về'], '',
        ['Vẫn tải được file, có dòng tiêu đề "DANH SÁCH PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN" và dòng tên cột',
         'Không có dòng dữ liệu nào; không báo lỗi']),
    cu('XIII', '004'),
    cu('XIII', '005', func='Định dạng ngày, số, chữ trong file'),
    moi('Dữ liệu trong file khớp với danh sách', 'P0',
        'Đang lọc Người tạo = B (12 phiếu); có phiếu huỷ hàng của nhân viên tên có dấu "Nguyễn Văn Ấn".',
        ['Xuất file với các trường mặc định', 'Đối chiếu từng dòng trong file với bảng trên màn'], '',
        ['Tên cột trong file trùng tên cột trên bảng',
         'Mã phiếu, Hủy của nhân viên, Người tạo, ngày giờ từng dòng trùng khớp bảng',
         'Tên tiếng Việt có dấu hiển thị đúng, không lỗi phông']),
    cu('XIII', '007', func='Phạm vi công ty áp cho file xuất'),
]

# ================================================================== X. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
G10 = [
    cu('X', '005', func='Lịch sử giữ hàng ghi nhận phiếu huỷ kế toán'),
    moi('Số có thể huỷ ở phiếu Yêu cầu hủy hàng giữ giảm theo', 'P1',
        'Nhân viên N giữ 10 cái hàng H cho K1. Kế toán vừa lập phiếu huỷ hàng giữ kế toán 4 cái H-K1 của N.',
        ['Đăng nhập N, vào Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Giữ hàng > Yêu cầu hủy hàng giữ, bấm Tạo mới',
         'Chọn hàng H, khách K1, đọc số có thể huỷ'], '',
        ['Số có thể huỷ của H-K1 là 6, không còn là 10']),
    moi('Màn Hàng sắp hết hạn giữ cập nhật sau khi huỷ', 'P1',
        'Lô hàng H của N cho K1 hạn 15/10/2026 còn 3, đang hiện ở màn Hàng sắp hết hạn giữ.',
        ['Lập phiếu huỷ hàng giữ kế toán 3 cái H-K1 của N', 'Mở màn Hàng sắp hết hạn giữ, tìm lô đó'], '',
        ['Số đang giữ của lô về 0 / lô không còn trong danh sách sắp hết hạn',
         'Các lô khác của N không bị ảnh hưởng']),
    moi('Đổi tên hàng hoá sau khi lập phiếu thì chi tiết giữ tên lúc lập', 'P2',
        'Phiếu KTPHHG-00605 có hàng H tên "Dầu A". Sau đó danh mục hàng hoá đổi tên H thành "Dầu A mới".',
        ['Mở chi tiết KTPHHG-00605', 'Mở bản in phiếu'], '',
        ['Chi tiết và bản in vẫn ghi "Dầu A" (thông tin hàng chụp lại lúc lập phiếu)',
         'Phiếu không bị lỗi, không mất dòng hàng']),
    moi('Hàng hoá đã có trên phiếu không xoá được ở danh mục', 'P2', 'Hàng H có trên phiếu KTPHHG-00605.',
        ['Vào Danh mục > Hàng hoá, thử xoá hàng H', 'Mở lại chi tiết KTPHHG-00605'], '',
        ['Hệ thống không cho xoá hàng H vì đang được sử dụng',
         'Chi tiết phiếu vẫn hiện đủ thông tin hàng H']),
    cu('XV', '001', func='Luồng nghiệp vụ: huỷ hàng giữ một khách một hàng'),
    cu('XV', '002', func='Luồng nghiệp vụ: nhiều hàng, nhiều khách, nhiều đơn vị tính'),
    cu('XV', '003', func='Luồng nghiệp vụ: huỷ hết hàng giữ rồi mở lại trang Thêm'),
    cu('XV', '004', func='Phiếu hủy hàng giữ thường vẫn chạy đúng song song với phiếu kế toán'),
]

# ================================================================== XI. PHÂN QUYỀN
G11 = [
    cu('ROLE', '00', func='Không có quyền "Quản lý giữ hàng" thì không xem được màn'),
    cu('ROLE', '01'),
    cu('ROLE', '02'),
    cu('ROLE', '03'),
    cu('ROLE', '04', func='Không có quyền nhưng mở thẳng đường dẫn trang Thêm'),
    moi('Không có quyền nhưng mở thẳng đường dẫn chi tiết phiếu', 'P1',
        'Tài khoản A không có quyền "Quản lý giữ hàng". Phiếu KTPHHG-00604 thuộc công ty của A.',
        ['Đăng nhập bằng A', 'Dán đường dẫn trang chi tiết KTPHHG-00604 lên thanh địa chỉ'], '',
        ['Báo "Bạn không có quyền xem phiếu này.", tự quay về màn danh sách',
         'Không hiện dữ liệu phiếu, không mở được bản in hay lịch sử']),
    moi('Bị gỡ quyền khi đang lập phiếu', 'P1',
        'Kế toán B đang ở trang Thêm, đã nhập đủ phiếu hợp lệ. Quản trị vừa gỡ quyền "Quản lý giữ hàng" của B.',
        ['B bấm Duyệt, xác nhận', 'B tải lại màn danh sách'], '',
        ['Bước 1: báo "Bạn chưa có quyền Quản lý giữ hàng.", không tạo phiếu, hàng giữ không đổi',
         'Bước 2: màn danh sách hiện câu chưa có quyền thay cho bảng']),
    cu('XIV', '006', func='Phạm vi dữ liệu: cô lập danh sách giữa hai công ty'),
]

SECTIONS = [(r, t, nhom(cs)) for r, t, cs in [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', G2),
    ('III', 'THÊM MỚI', G3),
    ('IV', 'DUYỆT PHIẾU', G4),
    ('V', 'LỊCH SỬ THAY ĐỔI', G5),
    ('VI', 'XEM CHI TIẾT PHIẾU HỦY HÀNG GIỮ KẾ TOÁN', G6),
    ('VII', 'IN PHIẾU', G7),
    ('VIII', 'TÙY CHỈNH CỘT', G8),
    ('IX', 'XUẤT DANH SÁCH EXCEL', G9),
    ('X', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G10),
    ('XI', 'PHÂN QUYỀN', G11),
]]

DESCRIPTION_BLOCK = [(t, _gach(b)) for t, b in V1.DESCRIPTION_BLOCK]

if __name__ == '__main__':
    con = sorted(set(OLD) - DA_DUNG)
    assert not con, 'Còn case cũ chưa đưa vào: %s' % con
    total = build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='phieu')
    print('Case cũ (bản 02/11): %d -> mới: %d (thêm %d)' % (SO_CU, total, total - SO_CU))
