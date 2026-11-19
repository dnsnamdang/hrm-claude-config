# -*- coding: utf-8 -*-
"""Case DÙNG CHUNG cho testcase các danh mục kho theo KHUÔN CHUẨN tab "13. DM quốc gia" (user chốt 03/11/2026).

Dùng bởi gen_testcase.py của warehouses / accounting-warehouses / houses. Mỗi màn khai 1 dict cấu hình C, gọi
`gen(C)` lấy các case chung theo khoá (vd 'h_stt', 't_f5'…), tự xếp thứ tự trong từng nhóm cùng case nghiệp vụ riêng
của màn rồi gọi `build(...)` -> `_tc_chuan.build_chuan(loai='danh_muc')`.

Case = (chức năng, P0-2, tiền điều kiện, bước, test data, expected). Bước / expected / data / tiền điều kiện được
phép là list: bước tự đánh số "1. …", expected tự thêm "-  " đầu mỗi ý (giống tab Quốc gia).
"""
import os
import re
import sys

XTL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
                                   'xuat-tai-lieu-chuyen-doi'))
sys.path.insert(0, XTL)

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]


# ------------------------------------------------------------------ định dạng
def _steps(x):
    if isinstance(x, str):
        return x
    out = []
    for i, s in enumerate(x, 1):
        s = s.strip()
        out.append(s if re.match(r'^\d+\.\s', s) else '%d. %s' % (i, s))
    return '\n'.join(out)


def _exp(x):
    items = x.split('\n') if isinstance(x, str) else list(x)
    out = []
    for s in items:
        s = s.strip()
        if not s:
            continue
        s = re.sub(r'^-\s*', '', s)
        out.append('-  ' + s)
    return '\n'.join(out)


def _txt(x):
    if x is None:
        return ''
    if isinstance(x, str):
        return '' if x.strip() == '-' else x
    return '\n'.join(s for s in x if s and s.strip() != '-')


def K(func, prio, pre, steps, data, exp):
    """Một case (chưa đánh số)."""
    assert prio in ('P0', 'P1', 'P2'), prio
    # mũi tên bị tính là icon (cấm trong ô) -> viết "->"
    return tuple(s.replace('→', '->').replace('☰', 'biểu tượng ba gạch') for s in (func, prio, _txt(pre), _steps(steps), _txt(data), _exp(exp)))


_REF = re.compile(r'\s*\((?:theo |xem )?TC[_-][\w.]+(?:\s*,\s*TC[_-][\w.]+)*\)|\s*(?:theo|như|ở) TC[_-][\w.]+')


def _bo_ma(s):
    """Bỏ các tham chiếu mã case kiểu cũ ("(TC_04.002)", "như TC_08.002") — mã đã đổi theo khuôn mới."""
    # mã dữ liệu mẫu cũ kiểu "KHO-E2E-01" -> "KHO-VD-01" (chữ E2E bị cấm trong khuôn mới)
    if not isinstance(s, str):
        return s
    s = re.sub(r'file TC_[\d.]+', 'file ở case "Kiểm tra dữ liệu - báo lỗi từng dòng"', s)
    s = re.sub(r'Đã làm TC_[\d.]+(?:(?:,| và) TC_[\d.]+)* trên', 'Đã sửa thông tin (case Sửa nhiều trường) trên', s)
    s = re.sub(r'Đã làm TC_[\d.]+(?:(?:,| và) TC_[\d.]+)*',
               'Đã thực hiện các case Sửa, Khóa, Mở khóa ở các nhóm trước', s)
    return _REF.sub('', s).replace('-E2E-', '-VD-')


def load_v1(path):
    """Nạp gen_testcase_v1.py (bản 02/11) để lấy nguyên văn case cũ: trả {('S4','007'): case, ('ROLE','01'): …}."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('tc_v1_' + str(abs(hash(path))), path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    cases = {}
    for name in dir(m):
        if re.match(r'^S\d+$', name) or name == 'ROLE_TCS':
            key = 'ROLE' if name == 'ROLE_TCS' else name
            for tc in getattr(m, name):
                cases[(key, tc[0])] = tc
    return m, cases


def O(cases, sec, num, **ov):
    """Case cũ giữ nội dung, bỏ tham chiếu mã case; ov ghi đè func/prio/pre/steps/data/exp."""
    _, func, prio, pre, steps, data, exp = cases[(sec, num)]
    v = dict(func=func, prio=prio, pre=pre, steps=steps, data=data, exp=exp)
    v.update(ov)
    return K(v['func'], v['prio'], _bo_ma(v['pre']), _bo_ma(v['steps']), _bo_ma(v['data']), _bo_ma(v['exp']))


def build(C, groups, description_block, sheet_name='Trang tính1'):
    """groups = [(TIÊU ĐỀ NHÓM, [case…]), …] theo đúng thứ tự khuôn danh_muc."""
    from _tc_chuan import build_chuan
    sections = []
    for i, (title, cases) in enumerate(groups):
        tcs = [('%03d' % (j + 1),) + tuple(cs) for j, cs in enumerate(cases)]
        sections.append((ROMAN[i], title, tcs))
    return build_chuan(C['out'], sheet_name, C['ten'] + ' - Cập nhật ngày ' + C['ngay'], C['ten'],
                       description_block, sections, loai='danh_muc')


# ------------------------------------------------------------------ case chung
def gen(C):
    """Trả dict khoá -> case chung đã điền theo màn."""
    obj, lb, ma, tn = C['obj'], C['label'], C['ma'], C['tenf']
    A, B = C['A'], C['B']                      # (mã, tên) bản ghi mẫu Hoạt động
    MENU = C['menu']
    TT = C['title']
    srt = C['sort_cols']
    nos = C['nosort_cols']
    lock = C['locked_cols']
    T = {}

    # ===================== I. HIỂN THỊ TRANG & TRUY CẬP
    T['h_trangthai'] = K('Cột Trạng thái phân biệt Hoạt động và Khóa', 'P0',
                         'Trong phạm vi xem có ít nhất 1 %s Hoạt động và 1 %s đang Khóa.' % (obj, obj),
                         ['Mở màn hình', 'Đọc cột Trạng thái của 2 bản ghi'], '',
                         ['Bản ghi bình thường hiện nhãn "Hoạt động" màu xanh',
                          'Bản ghi đã khóa hiện nhãn "Khóa" màu đỏ, phân biệt rõ ràng'])
    T['h_rong_dm'] = K('Danh sách khi chưa có bản ghi nào', 'P2',
                       'Đăng nhập tài khoản thuộc một công ty chưa khai báo %s nào (hoặc môi trường kiểm thử trống).' % obj,
                       ['Vào menu ' + MENU, 'Quan sát bảng và dòng tổng'], '',
                       ['Bảng hiện dòng "Không có dữ liệu phù hợp."',
                        'Dòng tổng dưới bảng hiện "Không có %s nào."' % obj,
                        'Màn hình không báo lỗi, các nút Tạo mới, Import Excel, Xuất Excel vẫn dùng được'])
    T['h_khong_khop'] = K('Hiển thị khi không có dữ liệu khớp', 'P1', 'Danh mục có dữ liệu bình thường.',
                          ['Gõ vào ô tìm kiếm một chuỗi chắc chắn không tồn tại', 'Nhấn Tìm kiếm hoặc Enter'],
                          'Từ khóa: zzzkhongtontai999',
                          ['Bảng hiện "Không có dữ liệu phù hợp."',
                           'Dòng tổng dưới bảng hiện "Không có %s nào."' % obj, 'Không báo lỗi'])
    T['h_so_dong_md'] = K('Số bản ghi mặc định mỗi trang', 'P0',
                          'Phạm vi xem có nhiều hơn 10 %s. Chưa đổi số dòng / trang.' % obj,
                          ['Vào menu ' + MENU, 'Đếm số dòng trên bảng', 'Mở ô "Số dòng/trang" ở góc dưới bên phải bảng'],
                          '',
                          ['Bảng hiện đúng 10 dòng',
                           'Ô Số dòng/trang cho chọn 5 / 10 / 20 / 50 / 100, đang chọn 10',
                           'Dòng tổng hiện "Hiển thị 1–10 / N" (N là tổng số %s khớp bộ lọc)' % obj])
    T['h_doi_so_dong'] = K('Đổi số dòng mỗi trang thì quay về trang 1', 'P1',
                           'Phạm vi xem có nhiều hơn 20 %s. Đang đứng ở trang 2.' % obj,
                           ['Đổi ô Số dòng/trang sang 20', 'Đếm số dòng, đọc thanh phân trang và dòng tổng'],
                           'Số dòng/trang: 20',
                           ['Bảng hiện đúng 20 dòng', 'Bảng quay về trang 1, dòng tổng hiện "Hiển thị 1–20 / N"',
                            'Số thứ tự bắt đầu lại từ 1'])
    T['h_truoc_sau'] = K('Nút sang trang kế tiếp và lùi về trang trước', 'P0',
                         'Phạm vi xem có ít nhất 3 trang dữ liệu. Đang ở trang 1.',
                         ['Bấm nút › (trang kế tiếp)', 'Đọc thanh phân trang và dòng tổng', 'Bấm nút ‹ (trang trước)',
                          'Đọc lại'], '',
                         ['Bước 1: chuyển sang trang 2, số trang 2 được tô đậm, dòng tổng hiện "Hiển thị 11–20 / N"',
                          'Bước 3: quay lại trang 1, dòng tổng hiện "Hiển thị 1–10 / N"',
                          'Dữ liệu từng trang không lặp, không thiếu dòng'])
    T['h_dau_cuoi'] = K('Nút về trang cuối và về trang đầu', 'P0',
                        'Phạm vi xem có N %s, nhiều hơn 3 trang. Đang ở trang 1.' % obj,
                        ['Bấm nút » (về trang cuối)', 'Đọc thanh phân trang, dòng tổng và số thứ tự dòng cuối',
                         'Bấm nút « (về trang đầu)', 'Đọc lại'], 'N = tổng số %s' % obj,
                        ['Bước 1: nhảy tới trang cuối cùng, dòng tổng hiện "Hiển thị …–N / N", số thứ tự dòng cuối bằng N',
                         'Bước 3: quay về trang 1, dòng tổng hiện "Hiển thị 1–10 / N"'])
    T['h_nut_mo'] = K('Nút phân trang ở trang đầu và trang cuối', 'P1', 'Phạm vi xem có nhiều hơn 1 trang.',
                      ['Đứng ở trang 1, quan sát hai nút « và ‹', 'Bấm » để về trang cuối, quan sát hai nút › và »'], '',
                      ['Ở trang 1: nút « và ‹ bị mờ, bấm không có tác dụng',
                       'Ở trang cuối: nút › và » bị mờ, bấm không có tác dụng'])
    T['h_stt'] = K('Số thứ tự liên tục qua các trang', 'P0', 'Phạm vi xem có nhiều hơn một trang dữ liệu.',
                   ['Ghi lại số thứ tự dòng cuối trang 1', 'Sang trang 2, đọc số thứ tự dòng đầu'], '',
                   ['Số thứ tự nối tiếp liền mạch (trang 2 bắt đầu từ 11), không quay về 1'])
    T['h_tong'] = K('Tổng số bản ghi khi mở danh sách', 'P0',
                    'Phạm vi xem có N %s (gồm cả Hoạt động và Khóa). Chưa lọc gì.' % obj,
                    ['Vào menu ' + MENU, 'Đọc dòng tổng ở góc dưới bên trái bảng'], 'N = tổng số %s đã đếm trước' % obj,
                    ['Dòng tổng hiện "Hiển thị 1–10 / N"',
                     'N bằng đúng tổng số %s trong phạm vi xem, tính cả bản ghi đã Khóa' % obj])
    T['h_loc_ve_1'] = K('Đổi bộ lọc khi đang ở trang giữa thì quay về trang 1', 'P0',
                        'Phạm vi xem có hơn 3 trang. Đang đứng ở trang 3.',
                        ['Bấm Tìm kiếm nâng cao, ô Trạng thái chọn "Hoạt động"', 'Quan sát bảng và thanh phân trang'],
                        'Trạng thái: Hoạt động',
                        ['Bảng quay về trang 1 của kết quả lọc, số thứ tự bắt đầu từ 1',
                         'Không rơi vào trang trống'])
    T['h_sx_md'] = K('Thứ tự mặc định khi mở màn', 'P0',
                     'Vừa tạo mới %s "%s". Chưa bấm sắp xếp cột nào.' % (obj, C['new'][0]),
                     ['Vào menu ' + MENU, 'Đọc các dòng đầu tiên của bảng'], '%s: %s' % (ma, C['new'][0]),
                     ['%s vừa tạo nằm ở dòng đầu tiên, STT = 1' % C['new'][0],
                      'Các dòng xếp theo Ngày tạo giảm dần (tạo mới nhất ở trên)'])
    T['h_sx_ma'] = K('Sắp xếp theo cột %s' % ma, 'P1', 'Phạm vi xem có ít nhất 5 %s có mã khác nhau.' % obj,
                     ['Bấm tiêu đề cột ' + ma, 'Đọc 5 dòng đầu', 'Bấm tiêu đề cột %s lần thứ hai' % ma,
                      'Đọc lại 5 dòng đầu'], '',
                     ['Lần 1: các dòng xếp tăng dần theo mã (A → Z), tiêu đề cột có mũi tên lên',
                      'Lần 2: thứ tự đảo ngược (Z → A), mũi tên xuống'])
    T['h_sx_ten'] = K('Sắp xếp theo cột %s' % tn, 'P1', 'Phạm vi xem có ít nhất 5 %s.' % obj,
                      ['Bấm tiêu đề cột ' + tn, 'Đọc 5 dòng đầu', 'Bấm lần thứ hai'], '',
                      ['Lần 1: xếp tăng dần đúng thứ tự chữ cái tiếng Việt có dấu',
                       'Lần 2: thứ tự đảo ngược hoàn toàn'])
    T['h_sx_ngay'] = K('Sắp xếp theo Ngày tạo và Ngày cập nhật', 'P1',
                       'Có %s tạo ở nhiều thời điểm khác nhau; %s tạo trước nhưng vừa được sửa sau cùng.' % (obj, A[0]),
                       ['Bấm tiêu đề cột Ngày cập nhật đến khi giảm dần', 'Đọc 5 dòng đầu',
                        'Bấm tiêu đề cột Ngày tạo đến khi giảm dần', 'Đọc 5 dòng đầu'], '',
                       ['Bước 2: %s đứng đầu, cột Ngày cập nhật giảm dần' % A[0],
                        'Bước 4: bản ghi tạo gần đây nhất đứng đầu, cột Ngày tạo giảm dần'])
    T['h_khong_sx'] = K('Các cột không cho sắp xếp', 'P2', 'Đang ở màn %s.' % TT,
                        ['Di chuột và bấm vào tiêu đề các cột ' + ', '.join(nos), 'Quan sát bảng'], '',
                        ['Các cột này KHÔNG có biểu tượng mũi tên sắp xếp',
                         'Bấm vào tiêu đề không làm thay đổi thứ tự dòng',
                         'Chỉ các cột %s là sắp xếp được' % ', '.join(srt)])
    T['h_sx_giu'] = K('Sắp xếp giữ nguyên khi chuyển trang', 'P1',
                      'Đang sắp xếp giảm dần theo cột %s, có nhiều hơn 1 trang.' % tn,
                      ['Bấm sang trang 2', 'So dòng đầu trang 2 với dòng cuối trang 1'], '',
                      ['Mũi tên sắp xếp vẫn ở cột ' + tn, 'Thứ tự nối tiếp liền mạch, không đảo lộn hay lặp bản ghi'])
    T['h_sx_ve_1'] = K('Bấm sắp xếp khi đang ở trang giữa thì quay về trang 1', 'P1',
                       'Phạm vi xem có nhiều hơn 3 trang. Đang đứng ở trang 3.',
                       ['Bấm tiêu đề cột ' + ma, 'Quan sát thanh phân trang và dòng tổng'], '',
                       ['Bảng quay về trang 1, hiển thị các bản ghi đầu tiên theo mã tăng dần',
                        'Dòng tổng hiện "Hiển thị 1–10 / N", tổng N không đổi'])

    # ===================== II. TÌM KIẾM & LỌC DANH SÁCH
    T['t_chinh_xac'] = K('Tìm theo đúng mã đầy đủ', 'P0', 'Có %s mã "%s".' % (obj, A[0]),
                         ['Gõ đúng mã vào ô tìm kiếm', 'Nhấn Enter'], 'Từ khóa: ' + A[0],
                         ['Có %s trong kết quả' % A[0],
                          'Chỉ còn các bản ghi có mã hoặc tên chứa đúng chuỗi này; dòng tổng đổi theo kết quả'])
    T['t_mot_phan'] = K('Tìm theo một phần tên', 'P0', 'Có %s tên "%s".' % (obj, B[1]),
                        ['Gõ một phần tên vào ô tìm kiếm', 'Bấm nút Tìm kiếm'], 'Từ khóa: ' + C['mot_phan'],
                        ['Chỉ còn các bản ghi có mã hoặc tên chứa "%s", có %s' % (C['mot_phan'], B[0]),
                         'Dòng tổng đổi theo kết quả'])
    T['t_hoa_thuong'] = K('Tìm không phân biệt chữ hoa chữ thường', 'P1', 'Có %s mã "%s".' % (obj, A[0]),
                          ['Gõ từ khóa toàn chữ thường, nhấn Enter, ghi nhận kết quả',
                           'Xóa, gõ lại toàn chữ hoa, nhấn Enter', 'So sánh'],
                          ['Lần 1: ' + A[0].lower(), 'Lần 2: ' + A[0].upper()],
                          ['Hai lần tìm cho ra CÙNG một tập kết quả, đều có ' + A[0]])
    T['t_dau'] = K('Tìm không dấu vẫn ra tên có dấu', 'P1', 'Có %s tên "%s".' % (obj, C['ten_dau'][0]),
                   ['Gõ tên không dấu vào ô tìm kiếm, nhấn Enter', 'Gõ lại đúng tên có dấu, nhấn Enter', 'So sánh'],
                   ['Lần 1: ' + C['ten_dau'][1], 'Lần 2: ' + C['ten_dau'][0]],
                   ['Cả hai lần đều ra "%s"' % C['ten_dau'][0], 'Hai lần cho cùng một tập kết quả'])
    T['t_khoang_trang'] = K('Từ khóa có khoảng trắng đầu / cuối hoặc chỉ toàn khoảng trắng', 'P1',
                            'Có %s mã "%s". Phạm vi xem có N %s.' % (obj, A[0], obj),
                            ['Gõ từ khóa có 2 khoảng trắng ở đầu và cuối, nhấn Enter',
                             'Xóa, gõ 3 khoảng trắng, nhấn Enter'],
                            ['Lần 1: "  %s  "' % A[0], 'Lần 2: "   "'],
                            ['Lần 1: kết quả giống hệt khi gõ "%s" không có khoảng trắng' % A[0],
                             'Lần 2: coi như không lọc, dòng tổng về "Hiển thị 1–10 / N"', 'Không báo lỗi'])
    T['t_gioi_han'] = K('Giới hạn độ dài ô tìm kiếm', 'P2', 'Đang ở màn danh sách.',
                        ['Dán chuỗi Test data vào ô tìm kiếm', 'Kiểm tra chuỗi trong ô có bị cắt bớt không',
                         'Bấm Tìm kiếm', 'Bấm Làm mới'],
                        'Chuỗi 500 ký tự (vd chữ "abcde" lặp lại 100 lần)',
                        ['Bước 2: ô tìm kiếm nhận đủ 500 ký tự, không bị cắt, không có thông báo lỗi',
                         'Bước 3: bảng hiện "Không có dữ liệu phù hợp.", dòng dưới bảng hiện "Không có %s nào."; màn '
                         'hình không treo, không báo lỗi hệ thống' % obj,
                         'Bước 4: ô tìm kiếm trống, bảng về toàn bộ danh sách'])
    T['t_xoa'] = K('Xóa từ khóa thì danh sách quay về đầy đủ', 'P0',
                   'Đang tìm với từ khóa cho ra ít kết quả. Phạm vi xem có N %s.' % obj,
                   ['Xóa hết nội dung ô tìm kiếm', 'Nhấn Enter'], '',
                   ['Dòng tổng quay lại "Hiển thị 1–10 / N" như ban đầu', 'Bảng về trang 1'])
    T['t_md'] = K('Mặc định khi vào màn không lọc gì', 'P0',
                  'Phạm vi xem có ít nhất 1 %s đang Khóa. Vào màn lần đầu trong phiên.' % obj,
                  ['Vào menu ' + MENU + ', không đụng vào bộ lọc', 'Bấm Tìm kiếm nâng cao, đọc các ô lọc',
                   'Tìm bản ghi đang Khóa trên bảng'], '',
                  ['Ô tìm kiếm và mọi ô lọc (kể cả Trạng thái, Ngày tạo) đều trống',
                   'Bản ghi đang Khóa VẪN hiện trong danh sách cùng bản ghi Hoạt động'])
    T['t_tong_loc'] = K('Tổng số bản ghi sau khi tìm theo từ khóa và lọc trạng thái', 'P0',
                        'Phạm vi xem có M %s chứa chuỗi "%s" ở mã hoặc tên, trong đó K bản ghi đang Khóa.'
                        % (obj, C['tu_khoa_chung']),
                        ['Gõ "%s" vào ô tìm kiếm, nhấn Enter' % C['tu_khoa_chung'], 'Đọc dòng tổng',
                         'Chọn thêm Trạng thái = Khóa', 'Đọc lại dòng tổng'],
                        ['Từ khóa: ' + C['tu_khoa_chung'], 'Trạng thái: Khóa'],
                        ['Bước 2: dòng tổng hiện "Hiển thị 1–… / M"',
                         'Bước 4: dòng tổng hiện "… / K", đúng bằng số bản ghi vừa chứa từ khóa vừa đang Khóa',
                         'Số dòng trên bảng khớp với con số này'])
    T['t_trang_loc'] = K('Phân trang theo kết quả lọc', 'P1',
                         'Lọc Trạng thái = Hoạt động cho ra M bản ghi, M lớn hơn 10.',
                         ['Chọn Trạng thái = Hoạt động', 'Đọc dòng tổng', 'Sang trang 2, đọc lại ô Trạng thái và dòng tổng'],
                         'Trạng thái: Hoạt động',
                         ['Bước 2: "Hiển thị 1–10 / M"',
                          'Bước 3: "Hiển thị 11–… / M", ô Trạng thái vẫn là Hoạt động, mọi dòng đều có nhãn Hoạt động'])
    T['t_sx_loc'] = K('Sắp xếp trên kết quả đã lọc', 'P1', 'Đang lọc Trạng thái = Hoạt động, có M bản ghi.',
                      ['Bấm tiêu đề cột %s để xếp tăng dần' % tn, 'Đọc ô lọc, dòng tổng và các dòng'], '',
                      ['Chỉ các bản ghi Hoạt động được xếp lại theo tên tăng dần',
                       'Ô Trạng thái vẫn giữ Hoạt động, dòng tổng vẫn "/ M"'])
    T['t_lam_moi_tong'] = K('Tổng số bản ghi quay về ban đầu sau khi bấm Làm mới', 'P1',
                            'Phạm vi xem có N %s. Đang lọc Trạng thái = Khóa và có từ khóa tìm kiếm, đang ở trang 2 '
                            '(nếu có).' % obj,
                            ['Bấm nút Làm mới', 'Đọc ô tìm kiếm, các ô lọc và dòng tổng'], '',
                            ['Ô tìm kiếm và mọi ô lọc trở về trống, bảng tải lại ngay',
                             'Bảng về trang 1, dòng tổng hiện lại "Hiển thị 1–10 / N"'])
    data_luu = ['Từ khóa: "%s"' % C['tu_khoa_chung'], 'Trạng thái: Hoạt động']
    T['t_chuyen_man'] = K('Rời sang màn khác rồi quay lại (trước và sau 10 phút) thì bộ lọc trở về mặc định', 'P1',
                          'Đang ở màn %s.' % TT,
                          ['Gõ từ khóa vào ô tìm kiếm, nhấn Enter, chọn Trạng thái theo Test data',
                           'Ghi nhận dòng tổng',
                           'Vào màn khác trên menu (vd Phân hệ Kho => Danh mục => %s)' % C['man_khac'],
                           'Khoảng 1 phút sau, quay lại bằng menu ' + MENU, 'Quan sát khối tìm kiếm và bảng',
                           'Lọc lại như bước 1, rời sang màn khác, chờ hơn 10 phút rồi quay lại'],
                          data_luu,
                          ['Bước 5 và bước 6 cho cùng kết quả: ô tìm kiếm trống, các ô lọc trở về rỗng',
                           'Bảng hiện toàn bộ danh sách ở trang 1, dòng tổng bằng tổng số bản ghi như lúc mới mở màn',
                           'Màn này không giữ bộ lọc khi rời sang màn khác, dù quay lại trước hay sau 10 phút'])
    T['t_f5'] = K('Tải lại trang (F5) khi đang lọc', 'P2', 'Đang ở màn %s.' % TT,
                  ['Gõ từ khóa vào ô tìm kiếm, nhấn Enter, chọn Trạng thái theo Test data', 'Nhấn F5 tải lại trang',
                   'Quan sát khối tìm kiếm và bảng'], data_luu,
                  ['Ô tìm kiếm và các ô lọc trở về rỗng',
                   'Bảng hiện toàn bộ danh sách ở trang 1 với số dòng mặc định 10'])
    T['t_tab'] = K('Mở màn hình ở tab trình duyệt mới khi tab cũ đang lọc', 'P2', 'Tab 1 đang mở màn %s.' % TT,
                   ['Ở tab 1: gõ từ khóa, nhấn Enter, chọn Trạng thái theo Test data',
                    'Mở tab trình duyệt mới (đã đăng nhập sẵn), vào màn bằng menu ' + MENU, 'Quan sát tab 2',
                    'Quay lại tab 1, quan sát'], data_luu,
                   ['Tab 2: ô tìm kiếm và các ô lọc rỗng, bảng hiện toàn bộ danh sách ở trang 1',
                    'Tab 1: vẫn giữ nguyên từ khóa, giá trị lọc và kết quả đang xem'])
    T['t_tk_khac'] = K('Đăng xuất, đăng nhập tài khoản khác trên cùng trình duyệt', 'P1',
                       'Có 2 tài khoản TK-A và TK-H cùng công ty, đều có quyền "Quản lý kho". Dùng chung một trình duyệt.',
                       ['Đăng nhập TK-A, vào menu ' + MENU, 'Gõ từ khóa, nhấn Enter, chọn Trạng thái theo Test data',
                        'Đăng xuất', 'Đăng nhập TK-H, vào lại màn', 'Quan sát khối tìm kiếm và bảng'], data_luu,
                       ['TK-H thấy ô tìm kiếm và các ô lọc rỗng, bảng hiện toàn bộ danh sách ở trang 1',
                        'Từ khóa và giá trị lọc của TK-A KHÔNG hiện sang TK-H'])

    # ===================== III. THÊM MỚI
    T['a_chi_bat_buoc'] = K('Thêm mới chỉ nhập các ô bắt buộc', 'P0',
                            'Đang ở màn %s, chưa có %s mã "%s".' % (TT, obj, C['new2'][0]),
                            ['Bấm Tạo mới', 'Chỉ nhập các ô bắt buộc theo Test data; để trống Trạng thái và Mô tả',
                             'Bấm Lưu', 'Bật cột Mô tả ở Cấu hình cột, đọc dòng vừa tạo'],
                            C['form_min'],
                            ['Hiện "Thêm mới thành công.", cửa sổ đóng, bản ghi mới đứng đầu danh sách',
                             'Trạng thái mặc định là "Hoạt động"',
                             'Ô Mô tả để trống, không in dấu gạch'])
    T['a_lich_su'] = K('Ghi nhận lịch sử Tạo mới sau khi thêm thành công', 'P1',
                       'Vừa tạo %s "%s" thành công, chưa sửa lần nào.' % (obj, C['new2'][0]),
                       ['Tìm bản ghi vừa tạo', 'Mở nút ba chấm "Hành động khác" (hoặc cột Hành động), bấm Lịch sử'],
                       '%s: %s' % (ma, C['new2'][0]),
                       ['Cửa sổ "Lịch sử thay đổi: <tên bản ghi>" có đúng 1 mốc "Tạo mới"',
                        'Mốc ghi "Người thực hiện: <họ tên> — <phòng ban>" của tài khoản vừa tạo và thời điểm tới phút'])
    T['a_ma_khoang_trang'] = K('Khoảng trắng đầu / cuối: Tên được cắt bỏ, Mã bị báo lỗi', 'P1',
                               'Đang ở cửa sổ Tạo mới, các ô khác đã nhập hợp lệ.',
                               ['Gõ %s có khoảng trắng đầu / cuối như Test data' % ma,
                                'Sửa %s về đúng "%s" (không khoảng trắng); gõ %s có khoảng trắng đầu / cuối'
                                % (ma, C['new3'][0], tn), 'Bấm Lưu', 'Đọc dòng vừa tạo'],
                               ['%s: "  %s  "' % (ma, C['new3'][0]), '%s: "  %s  "' % (tn, C['new3'][1])],
                               ['Bước 1: báo đỏ ngay dưới ô %s: "Chỉ gồm chữ không dấu, số, dấu - và _" (khoảng '
                                'trắng không được phép trong mã)' % ma,
                                'Bước 3: lưu thành công',
                                'Bước 4: tên hiện "%s", không còn khoảng trắng thừa ở đầu / cuối' % C['new3'][1]])
    T['a_chi_khoang_trang'] = K('Mã / Tên chỉ toàn khoảng trắng', 'P1', 'Đang ở cửa sổ Tạo mới.',
                                ['Gõ 3 khoảng trắng vào ô %s' % ma,
                                 'Gõ 3 khoảng trắng vào ô %s, nhập đủ các ô bắt buộc khác' % tn, 'Bấm Lưu'],
                                ['%s: "   "' % ma, '%s: "   "' % tn],
                                ['Ô %s báo đỏ ngay khi gõ: "Chỉ gồm chữ không dấu, số, dấu - và _"' % ma,
                                 'Sửa %s về hợp lệ rồi bấm Lưu: ô %s báo đỏ "Bắt buộc phải nhập", không tạo bản ghi'
                                 % (ma, tn)])
    T['a_loi_mat'] = K('Thông báo lỗi định dạng %s mất ngay khi nhập lại đúng' % ma, 'P0',
                       'Đang ở cửa sổ Tạo mới.',
                       ['Nhập %s sai định dạng' % ma, 'Nhập lại %s đúng định dạng' % ma],
                       ['%s lần 1: %s' % (ma, C['ma_sai']), '%s lần 2: %s' % (ma, C['new3'][0])],
                       ['Lần 1: báo đỏ "Chỉ gồm chữ không dấu, số, dấu - và _"',
                        'Lần 2: thông báo lỗi mất ngay, không cần bấm Lưu'])
    T['a_dung_max'] = K('Nhập %s đúng 50 ký tự và %s đúng 255 ký tự thì lưu được' % (ma, tn), 'P1',
                        'Đang ở cửa sổ Tạo mới, các ô bắt buộc khác đã nhập hợp lệ.',
                        ['Nhập %s dài đúng 50 ký tự (chỉ chữ không dấu, số)' % ma,
                         'Nhập %s dài đúng 255 ký tự (chưa tồn tại)' % tn, 'Bấm Lưu', 'Mở cửa sổ Xem bản ghi vừa tạo'],
                        ['%s: chuỗi 50 ký tự' % ma, '%s: chuỗi 255 ký tự' % tn],
                        ['Không báo lỗi dưới 2 ô', 'Lưu thành công',
                         'Cửa sổ Xem hiện đủ 50 ký tự của mã và 255 ký tự của tên, không bị cắt'])
    T['a_ltt_thieu'] = K('Lưu & Tiếp tục khi bỏ trống trường bắt buộc', 'P0', 'Đang mở cửa sổ ' + C['title_tao'] + '.',
                         ['Để trống toàn bộ, bấm "Lưu & Tiếp tục"',
                          'Nhập %s, để trống %s, bấm "Lưu & Tiếp tục"' % (ma, tn)], '',
                         ['Bước 1: hiện "Bạn chưa nhập đầy đủ thông tin.", báo "Bắt buộc phải nhập" dưới mọi ô bắt buộc',
                          'Bước 2: báo "Bắt buộc phải nhập" dưới ô ' + tn,
                          'Cửa sổ vẫn mở, giá trị đã nhập giữ nguyên, không bị xóa trắng',
                          'Không hiện "Thêm mới thành công.", danh sách phía sau không có bản ghi mới'])
    T['a_ltt_sai'] = K('Lưu & Tiếp tục khi nhập sai định dạng', 'P1', 'Đang mở cửa sổ ' + C['title_tao'] + '.',
                       ['Nhập đủ các ô bắt buộc, %s theo Test data' % ma, 'Bấm "Lưu & Tiếp tục"',
                        'Sửa %s về đúng định dạng, bấm "Lưu & Tiếp tục"' % ma],
                       '%s: %s' % (ma, C['ma_sai']),
                       ['Bước 2: dưới ô %s báo "Chỉ gồm chữ không dấu, số, dấu - và _"; không lưu, cửa sổ vẫn mở, '
                        'mọi giá trị đã nhập (kể cả giá trị sai) giữ nguyên' % ma,
                        'Bước 3: lưu thành công, cửa sổ xóa trắng để nhập tiếp'])
    T['a_ltt_trung'] = K('Lưu & Tiếp tục khi trùng mã', 'P0',
                         'Đã có %s mã "%s". Đang mở cửa sổ %s.' % (obj, A[0], C['title_tao']),
                         ['Nhập %s = %s, các ô khác hợp lệ (%s)' % (ma, A[0], C['trung_ghi_chu']),
                          'Bấm "Lưu & Tiếp tục"', 'Sửa mã thành mã chưa có, bấm lại "Lưu & Tiếp tục"'],
                         '%s: %s' % (ma, A[0]),
                         ['Bước 2: báo "%s" dưới ô %s; không lưu, cửa sổ vẫn mở, các ô giữ nguyên' % (C['dup'], ma),
                          'Bước 3: lưu thành công, cửa sổ xóa trắng để nhập tiếp'])
    T['a_ltt_dong'] = K('Bấm Lưu & Tiếp tục rồi bấm Đóng ngay thì không hỏi', 'P1',
                        'Đang ở cửa sổ %s, đã nhập đủ trường bắt buộc hợp lệ.' % C['title_tao'],
                        ['Bấm "Lưu & Tiếp tục"', 'Không nhập gì thêm vào cửa sổ trống', 'Bấm Đóng'], '',
                        ['Bản ghi vừa lưu có trong danh sách',
                         'Bấm Đóng thì cửa sổ đóng ngay, KHÔNG hiện hộp "Thông tin chưa lưu"'])
    T['a_x'] = K('Đã nhập thông tin rồi bấm nút X góc trên cửa sổ', 'P1',
                 'Đang ở cửa sổ %s, đã nhập %s.' % (C['title_tao'], tn),
                 ['Bấm nút X ở góc trên bên phải cửa sổ', 'Bấm "Ở lại"', 'Bấm nút X lần nữa, bấm "Thoát"'],
                 '%s: Thử nghiệm' % tn,
                 ['Bước 1: hiện hộp "Thông tin chưa lưu" với câu "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" '
                  'và 2 nút Thoát, Ở lại',
                  'Bước 2: quay về cửa sổ Tạo mới, dữ liệu đã nhập vẫn còn',
                  'Bước 3: cửa sổ đóng, không tạo bản ghi'])
    T['a_dong'] = K('Bấm Đóng khi đã nhập thông tin vào cửa sổ Tạo mới', 'P1',
                    'Đang ở cửa sổ %s, đã nhập %s.' % (C['title_tao'], ma),
                    ['Bấm Đóng', 'Bấm "Ở lại"', 'Bấm Đóng lần nữa, bấm "Thoát"', 'Bấm Tạo mới lần nữa'],
                    '%s: %s' % (ma, C['new4'][0]),
                    ['Bước 1: hiện hộp "Thông tin chưa lưu" với câu "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" '
                     'và 2 nút Thoát, Ở lại',
                     'Bước 2: hộp đóng, quay lại cửa sổ Tạo mới, dữ liệu đã nhập vẫn còn',
                     'Bước 3: cửa sổ đóng, quay về danh sách, KHÔNG có bản ghi mới',
                     'Bước 4: các ô trống, không còn dữ liệu cũ'])
    T['a_xoa_het'] = K('Nhập rồi xóa hết về như ban đầu, bấm Đóng thì không hỏi', 'P2',
                       'Đang ở cửa sổ %s, các ô đang trống.' % C['title_tao'],
                       ['Gõ vài ký tự vào ô ' + tn, 'Xóa hết các ký tự vừa gõ để ô trống trở lại', 'Bấm Đóng'], '',
                       ['Cửa sổ đóng ngay, KHÔNG hiện hộp "Thông tin chưa lưu"', 'Không có bản ghi mới nào được tạo'])
    T['a_de_lau'] = K('Đã nhập đủ dữ liệu nhưng không bấm Lưu, để nguyên cửa sổ thì không ghi gì', 'P2',
                      'Đang ở cửa sổ %s, đã nhập đủ trường bắt buộc hợp lệ.' % C['title_tao'],
                      ['Không bấm nút nào, để nguyên cửa sổ khoảng 15 phút', 'Mở tab khác xem danh sách'], '',
                      ['Cửa sổ Tạo mới giữ nguyên dữ liệu đã nhập', 'KHÔNG có bản ghi mới nào được tạo'])
    T['a_hai_tab'] = K('Hai tab cùng tạo một mã', 'P1',
                       'Mở màn %s ở 2 tab (hoặc 2 tài khoản cùng công ty). Chưa có mã "%s".' % (TT, C['new4'][0]),
                       ['Ở cả 2 tab bấm Tạo mới, nhập cùng dữ liệu theo Test data',
                        'Tab 1 bấm Lưu', 'Tab 2 bấm Lưu', 'Tải lại danh sách, tìm "%s"' % C['new4'][0]],
                       C['form_hai_tab'],
                       ['Tab 1: "Thêm mới thành công."',
                        'Tab 2: báo "%s" dưới ô %s, cửa sổ không đóng' % (C['dup'], ma),
                        'Danh sách chỉ có ĐÚNG MỘT bản ghi "%s"' % C['new4'][0]])

    # ===================== IV. CHỈNH SỬA
    T['e_mot_truong'] = K('Sửa một trường và lưu thành công', 'P0', '%s đang Hoạt động, Mô tả đang trống.' % B[0],
                          ['Mở cửa sổ Sửa ' + B[0], 'Chỉ nhập Mô tả', 'Bấm Lưu', 'Bật cột Mô tả, đọc dòng ' + B[0]],
                          'Mô tả: Sửa một trường',
                          ['Hiện "Cập nhật thành công.", cửa sổ đóng',
                           'Cột Mô tả hiện "Sửa một trường"; các cột khác giữ nguyên',
                           'Người cập nhật = tài khoản vừa sửa, Ngày cập nhật = thời điểm vừa lưu'])
    T['e_trong'] = K('Để trống %s khi sửa' % tn, 'P0', 'Đang mở cửa sổ Sửa một %s Hoạt động.' % obj,
                     ['Xóa trắng ô ' + tn, 'Bấm Lưu'], '%s: (để trống)' % tn,
                     ['Hiện "Bạn chưa nhập đầy đủ thông tin."',
                      'Báo đỏ "Bắt buộc phải nhập" dưới ô %s, cửa sổ không đóng, bản ghi không bị thay đổi' % tn])
    T['e_sai'] = K('Nhập %s sai định dạng khi sửa' % ma, 'P0', 'Đang mở cửa sổ Sửa một %s Hoạt động.' % obj,
                   ['Đổi %s thành giá trị Test data' % ma, 'Bấm Lưu'], '%s: %s' % (ma, C['ma_sai']),
                   ['Báo đỏ ngay dưới ô %s: "Chỉ gồm chữ không dấu, số, dấu - và _"' % ma,
                    'Bấm Lưu không lưu, cửa sổ không đóng'])
    T['e_vuot'] = K('Nhập %s vượt 50 ký tự khi sửa' % ma, 'P1', 'Đang mở cửa sổ Sửa một %s Hoạt động.' % obj,
                    ['Thay %s bằng chuỗi 51 ký tự (chỉ chữ không dấu, số)' % ma, 'Bấm Lưu'], '%s: chuỗi 51 ký tự' % ma,
                    ['Báo đỏ dưới ô %s: "Vui lòng nhập tối đa 50 ký tự.", ô KHÔNG tự cắt bớt' % ma,
                     'Không lưu, mã trên bảng giữ nguyên giá trị cũ'])
    T['e_trung'] = K('Sửa trùng mã với %s khác' % obj, 'P0', '%s và %s cùng %s.' % (A[0], B[0], C['trung_pham_vi']),
                     ['Mở cửa sổ Sửa ' + B[0], 'Đổi %s thành "%s"' % (ma, A[0]), 'Bấm Lưu'], '%s: %s' % (ma, A[0]),
                     ['Báo đỏ dưới ô %s: "%s"' % (ma, C['dup']), 'Cửa sổ không đóng, %s giữ mã cũ' % B[0]])
    T['e_loi_mat'] = K('Lỗi biến mất khi sửa lại hợp lệ', 'P1', 'Đang mở cửa sổ Sửa một %s Hoạt động.' % obj,
                       ['Xóa trắng ô %s, bấm Lưu' % tn, 'Gõ lại %s hợp lệ' % tn, 'Bấm Lưu'], '',
                       ['Bước 1: báo "Bắt buộc phải nhập" dưới ô ' + tn,
                        'Bước 2: dòng báo đỏ dưới ô %s mất' % tn, 'Bước 3: "Cập nhật thành công."'])
    T['e_khong_doi'] = K('Mở Sửa, không thay đổi gì rồi bấm Đóng', 'P1', '%s đang Hoạt động.' % B[0],
                         ['Bấm Sửa ở dòng ' + B[0], 'Không thay đổi ô nào', 'Bấm Đóng'], '',
                         ['Cửa sổ đóng ngay, KHÔNG hiện hộp "Thông tin chưa lưu"', 'Dữ liệu trên bảng không đổi'])
    T['e_tra_lai'] = K('Sửa rồi trả lại đúng giá trị cũ, bấm Đóng thì không hỏi', 'P2', '%s tên "%s".' % (B[0], B[1]),
                       ['Mở cửa sổ Sửa ' + B[0], 'Đổi %s thành "%s 1"' % (tn, B[1]), 'Sửa lại đúng "%s"' % B[1],
                        'Bấm Đóng'], '%s: %s → %s 1 → %s' % (tn, B[1], B[1], B[1]),
                       ['Cửa sổ đóng ngay, KHÔNG hiện hộp "Thông tin chưa lưu" vì dữ liệu không khác ban đầu'])
    T['e_khong_ls'] = K('Bấm Lưu nhưng không thay đổi gì thì không ghi lịch sử', 'P1',
                        '%s đã có N mốc lịch sử.' % B[0],
                        ['Mở cửa sổ Sửa ' + B[0], 'Không thay đổi gì', 'Bấm Lưu', 'Mở Lịch sử của ' + B[0]], '',
                        ['Lưu không báo lỗi', 'Lịch sử vẫn đúng N mốc, KHÔNG có mốc "Thay đổi thông tin" mới'])
    T['e_ls'] = K('Sửa xong ghi vào lịch sử', 'P0', 'Vừa đổi %s của %s từ "%s" thành "%s sửa".' % (tn, B[0], B[1], B[1]),
                  ['Mở Lịch sử của ' + B[0], 'Đọc mốc trên cùng'], '',
                  ['Có mốc "Thay đổi thông tin" nêu giá trị cũ "%s" → giá trị mới "%s sửa"' % (B[1], B[1]),
                   'Kèm người thực hiện và thời điểm'])
    T['e_dong_thoi'] = K('Hai người cùng sửa một bản ghi', 'P1',
                         'TK-A và TK-H cùng mở cửa sổ Sửa %s.' % B[0],
                         ['TK-A đổi Mô tả thành "Sửa của A", bấm Lưu', 'TK-H (cửa sổ mở từ trước) đổi Mô tả thành '
                          '"Sửa của H", bấm Lưu', 'Tải lại danh sách, mở Lịch sử của ' + B[0]], '',
                         ['Cả 2 lần đều "Cập nhật thành công."',
                          'Bản ghi giữ giá trị của người lưu SAU: Mô tả "Sửa của H", Người cập nhật là TK-H',
                          'Lịch sử có 2 mốc "Thay đổi thông tin" lần lượt của TK-A và TK-H'])

    # ===================== VI. KHÓA / MỞ KHÓA
    Kc, Kn = C['K']
    T['k_huy_mo'] = K('Bấm Hủy ở hộp xác nhận mở khóa', 'P2', '%s đang Khóa.' % Kc,
                      ['Bấm Mở khóa ở dòng ' + Kc, 'Bấm Hủy'], '',
                      ['Hộp đóng, %s vẫn Khóa, không có thông báo thành công' % Kc, 'Lịch sử không thêm mốc mới'])
    T['k_mo_dong_thoi'] = K('Mở khóa bản ghi đã bị người khác mở khóa', 'P1',
                            '%s đang Khóa. TK-A và TK-H cùng mở màn danh sách.' % Kc,
                            ['TK-H bấm Mở khóa %s và xác nhận' % Kc,
                             'TK-A (chưa tải lại trang) bấm Mở khóa %s và xác nhận' % Kc], '',
                            ['TK-H: "Mở khóa thành công.", ghi nhận lịch sử',
                             'TK-A: hiện thông báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang"',
                             'Lịch sử chỉ có 1 mốc Mở khóa (của TK-H)'])
    T['k_bi_xoa'] = K('Mở khóa bản ghi đã bị người khác xóa', 'P2',
                      '%s đang Khóa, %s. TK-A và TK-H cùng mở màn danh sách.' % (C['K_xoa'], C['K_xoa_dk']),
                      ['TK-H mở khóa %s, rồi bấm Xóa và xác nhận' % C['K_xoa'],
                       'TK-A (chưa tải lại trang, dòng vẫn hiện Khóa) bấm Mở khóa %s và xác nhận' % C['K_xoa'],
                       'TK-A tải lại trang'], '',
                      ['Bước 1: TK-H xóa thành công',
                       'Bước 2: TK-A nhận thông báo lỗi, hộp xác nhận đóng; không có bản ghi nào được mở khóa hay tạo lại',
                       'Bước 3: %s không còn trong danh sách của TK-A' % C['K_xoa']])

    # ===================== VII. LỊCH SỬ THAY ĐỔI
    T['l_mo'] = K('Mở cửa sổ Lịch sử', 'P0', '%s đã được sửa ít nhất 1 lần.' % B[0],
                  ['Ở dòng %s bấm Lịch sử (trong nút ba chấm "Hành động khác" nếu dòng có nút Xóa)' % B[0],
                   'Quan sát cửa sổ'], '',
                  ['Cửa sổ tiêu đề "Lịch sử thay đổi: <tên %s>"' % obj,
                   'Có nút Bộ lọc, các mốc xếp theo thời gian, nút Đóng ở cuối'])
    T['l_bo_loc'] = K('Mở ô bộ lọc của Lịch sử', 'P0', 'Đang mở cửa sổ Lịch sử của %s.' % B[0],
                      ['Bấm nút Bộ lọc'], '',
                      ['Hiện các ô lọc: Loại hành động, Người thực hiện, Từ ngày, Đến ngày, kèm nút Làm mới'])
    T['l_loai'] = K('Lọc theo Loại hành động', 'P0', '%s có mốc Tạo mới, Thay đổi thông tin, Khóa, Mở khóa.' % B[0],
                    ['Mở Lịch sử của %s, bấm Bộ lọc' % B[0], 'Mở ô Loại hành động',
                     'Chọn "Thay đổi trạng thái"'], 'Loại hành động: Thay đổi trạng thái',
                    ['Ô Loại hành động có đủ 3 giá trị: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái',
                     'Chọn xong chỉ còn các mốc Khóa / Mở khóa'])
    T['l_nguoi'] = K('Lọc theo Người thực hiện', 'P0', '%s được TK-A tạo và TK-H sửa.' % B[0],
                     ['Mở Lịch sử của %s, bấm Bộ lọc' % B[0], 'Mở ô Người thực hiện, chọn TK-H'], 'Người thực hiện: TK-H',
                     ['Ô Người thực hiện liệt kê nhân viên dạng "Tên - Mã phòng - Mã NV"',
                      'Chọn TK-H thì chỉ còn các mốc do TK-H thực hiện'])
    T['l_tg'] = K('Lọc theo khoảng thời gian', 'P0', '%s có mốc ở nhiều ngày khác nhau.' % B[0],
                  ['Mở Lịch sử, bấm Bộ lọc', 'Bấm ô Từ ngày, Đến ngày', 'Chọn khoảng chỉ chứa ngày tạo bản ghi'],
                  'Từ ngày = Đến ngày = ngày tạo bản ghi',
                  ['Ô Từ ngày, Đến ngày mở hộp lịch để chọn', 'Chỉ còn các mốc nằm trong khoảng đã chọn'])
    T['l_ket_hop'] = K('Kết hợp nhiều tiêu chí lọc lịch sử', 'P1', '%s có mốc Khóa do TK-A thực hiện.' % B[0],
                       ['Mở Lịch sử, bấm Bộ lọc', 'Chọn Loại hành động, Người thực hiện, Từ ngày, Đến ngày theo Test data'],
                       ['Loại hành động: Thay đổi trạng thái', 'Người thực hiện: TK-A', 'Từ ngày / Đến ngày: hôm nay'],
                       ['Chỉ trả về mốc Khóa / Mở khóa do TK-A thực hiện trong ngày'])
    T['l_khong_kq'] = K('Lọc lịch sử không có kết quả', 'P1', 'Đang mở Lịch sử của %s.' % B[0],
                        ['Bấm Bộ lọc', 'Chọn khoảng ngày trước ngày tạo bản ghi'], 'Từ ngày / Đến ngày: 01/01/2020',
                        ['Hiện "Không có lịch sử phù hợp bộ lọc."'])
    T['l_lam_moi'] = K('Nút Làm mới trong bộ lọc lịch sử', 'P1', 'Đang lọc lịch sử theo Loại hành động và Người thực hiện.',
                       ['Bấm Làm mới trong khối bộ lọc'], '',
                       ['Các ô lọc xóa hết giá trị', 'Danh sách trả về toàn bộ mốc lịch sử'])
    T['l_dong_loc'] = K('Đóng ô bộ lọc lịch sử', 'P2', 'Đang mở bộ lọc, đã chọn Loại hành động.',
                        ['Bấm nút Bộ lọc lần nữa'], '',
                        ['Khối bộ lọc thu lại, danh sách giữ nguyên theo tiêu chí đã lọc'])
    T['l_thu_tu'] = K('Thứ tự mới nhất ở trên cùng', 'P0', '%s đã được sửa 3 lần vào 3 thời điểm khác nhau.' % B[0],
                      ['Mở Lịch sử của ' + B[0], 'Đọc thời điểm các mốc từ trên xuống'], '',
                      ['Mốc trên cùng là lần thao tác MỚI NHẤT, càng xuống càng cũ'])
    T['l_mot_truong'] = K('Mỗi mốc nêu đủ thông tin khi sửa một trường', 'P0',
                          'Vừa đổi Mô tả của %s từ trống thành "Sửa một trường".' % B[0],
                          ['Mở Lịch sử của ' + B[0], 'Đọc mốc trên cùng'], '',
                          ['Mốc nhóm "Thay đổi thông tin" nêu rõ trường Mô tả: (trống) → "Sửa một trường"',
                           'Kèm "Người thực hiện: <họ tên> — <phòng ban>" và thời điểm tới phút',
                           'Các trường không đổi KHÔNG xuất hiện'])
    T['l_khoa'] = K('Lịch sử sau khi Khóa và Mở khóa', 'P0', '%s đang Hoạt động, đã có lịch sử tạo mới.' % C['K_lich_su'],
                    ['Khóa %s và xác nhận' % C['K_lich_su'], 'Mở khóa lại và xác nhận', 'Mở Lịch sử của ' + C['K_lich_su']],
                    '', ['Có mốc "Khóa" với Trạng thái: "Hoạt động" → "Khóa"',
                         'Có mốc "Mở khóa" với Trạng thái: "Khóa" → "Hoạt động"',
                         'Mốc khóa trước đó KHÔNG bị mất hay ghi đè; mỗi mốc ghi người thực hiện và thời điểm'])
    T['l_import'] = K('Lịch sử của bản ghi tạo bằng Import Excel', 'P1',
                      'Vừa import thành công %s "%s" từ file Excel.' % (obj, C['imp'][0]),
                      ['Tìm "%s" trên danh sách' % C['imp'][0], 'Mở Lịch sử'], '',
                      ['Có mốc "Tạo mới" ghi nhận việc thêm bản ghi',
                       'Người thực hiện là tài khoản vừa chạy import'])
    T['l_trang_thai_va_ten'] = K('Đổi tên và đổi Trạng thái cùng lúc trong cửa sổ Sửa', 'P1',
                                 '%s tên "%s", đang Hoạt động, %s.' % (C['K_lich_su'], C['K_lich_su_ten'], C['dk_khoa']),
                                 ['Mở cửa sổ Sửa ' + C['K_lich_su'],
                                  'Đổi %s thành "%s mới" và đổi Trạng thái sang "Khóa"' % (tn, C['K_lich_su_ten']),
                                  'Bấm Lưu', 'Mở Lịch sử'],
                                 ['%s: %s → %s mới' % (tn, C['K_lich_su_ten'], C['K_lich_su_ten']),
                                  'Trạng thái: Hoạt động → Khóa'],
                                 ['Sinh 2 mốc riêng: 1 mốc "Khóa" (Hoạt động → Khóa) và 1 mốc "Thay đổi thông tin" (%s)' % tn,
                                  'Trạng thái không bị lặp lại trong mốc "Thay đổi thông tin"'])
    T['l_dong'] = K('Đóng cửa sổ Lịch sử giữ nguyên danh sách', 'P2',
                    'Đang mở cửa sổ Lịch sử; danh sách phía sau đang lọc Trạng thái = Hoạt động và đứng ở trang 2.',
                    ['Bấm Đóng (hoặc nút X)'], '',
                    ['Cửa sổ đóng, danh sách giữ nguyên bộ lọc và trang 2'])

    # ===================== VIII. XEM CHI TIẾT
    T['v_khop'] = K('Dữ liệu trong cửa sổ Xem khớp với dòng trên bảng và dữ liệu đã tạo', 'P0',
                    '%s đã nhập đủ mọi ô.' % A[0],
                    ['Bật mọi cột ẩn ở Cấu hình cột hiển thị', 'Đọc giá trị trên dòng ' + A[0],
                     'Bấm mã %s mở cửa sổ Xem, đối chiếu' % A[0]], '',
                    ['Mọi ô trong cửa sổ trùng với giá trị trên bảng và với dữ liệu đã nhập khi tạo'])
    T['v_chi_doc'] = K('Các ô trong cửa sổ Xem không sửa được và không có nút Lưu', 'P0',
                       'Đang mở cửa sổ %s của %s.' % (C['title_xem'], A[0]),
                       ['Bấm vào từng ô và thử gõ', 'Quan sát vùng nút cuối cửa sổ'], '',
                       ['Mọi ô đều ở trạng thái khóa, không gõ được ký tự nào, nhãn không có dấu (*)',
                        'Chỉ có nút Đóng; KHÔNG có nút Lưu và Lưu & Tiếp tục'])
    T['v_khoa'] = K('Xem chi tiết bản ghi đã khóa', 'P1', '%s đang Khóa.' % C['K'][0],
                    ['Bấm vào mã %s' % C['K'][0]], '',
                    ['Mở cửa sổ "%s"' % C['title_xem'], 'Trạng thái hiện "Khóa", các ô khác hiện đúng dữ liệu'])
    T['v_dong'] = K('Đóng cửa sổ Xem giữ nguyên bộ lọc và trang', 'P1',
                    'Đang lọc Trạng thái = Hoạt động và đứng ở trang 2.',
                    ['Bấm mã một bản ghi để mở cửa sổ Xem', 'Bấm Đóng (hoặc nút X)'], '',
                    ['Quay lại danh sách vẫn ở trang 2 và vẫn giữ bộ lọc Hoạt động',
                     'Không hiện hộp "Thông tin chưa lưu"'])

    # ===================== IX. TÙY CHỈNH CỘT
    an = C['cols_an']
    T['c_mo'] = K('Mở cửa sổ Tùy chỉnh cột', 'P0', 'Chưa từng chỉnh cấu hình cột ở màn này.',
                  ['Bấm nút biểu tượng cột trên hàng nút (gợi ý "Cấu hình cột hiển thị")'], '',
                  ['Mở cửa sổ "Tuỳ chỉnh cột" liệt kê toàn bộ %d cột của bảng' % C['n_cols'],
                   'Các cột đang hiển thị được tích sẵn, dòng "Đang chọn %d/%d cột"' % (C['n_cols'] - len(an), C['n_cols']),
                   'Cột %s chưa tích' % ', '.join(an), 'Có nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng'])
    T['c_hien'] = K('Bật cột đang ẩn mặc định', 'P0', 'Mặc định bảng không hiện ' + ', '.join(an) + '.',
                    ['Mở Tùy chỉnh cột', 'Tích ' + ', '.join(an), 'Bấm Lưu'], 'Cột bật thêm: ' + ', '.join(an),
                    ['Hiện "Cập nhật thành công"', 'Bảng hiện thêm đúng %d cột vừa bật, có dữ liệu' % len(an),
                     'Thứ tự các cột còn lại không bị xáo trộn'])
    T['c_an'] = K('Tắt một cột tùy chọn', 'P1', 'Bảng đang hiện cột %s.' % C['cot_tat'],
                  ['Mở Tùy chỉnh cột', 'Bỏ tích cột ' + C['cot_tat'], 'Bấm Lưu'], 'Cột tắt: ' + C['cot_tat'],
                  ['Cột %s biến mất khỏi bảng' % C['cot_tat'], 'Dữ liệu các dòng không thay đổi, chỉ ẩn cột'])
    T['c_bat_buoc'] = K('Cột bắt buộc không tắt được', 'P0', 'Đang mở cửa sổ Tùy chỉnh cột.',
                        ['Thử bỏ tích các cột ' + ', '.join(lock)], '',
                        ['%d cột này có biểu tượng ổ khóa, hiển thị mờ, không bỏ tích được' % len(lock)])
    T['c_keo'] = K('Kéo thả đổi thứ tự cột', 'P1', 'Đang mở cửa sổ Tùy chỉnh cột.',
                   ['Kéo dòng Ngày tạo lên trên dòng ' + tn, 'Bấm Lưu', 'Quan sát bảng'], '',
                   ['Hiện "Cập nhật thành công"', 'Trên bảng, cột Ngày tạo đứng trước cột ' + tn,
                    'Dữ liệu từng cột vẫn đúng'])
    T['c_co_dinh'] = K('Cột bắt buộc không kéo đổi vị trí được và đứng yên khi cuộn ngang', 'P2',
                       'Đã bật mọi cột; thu cửa sổ trình duyệt còn khoảng 1000 điểm ảnh.',
                       ['Mở Tùy chỉnh cột, thử kéo dòng ' + ', '.join(lock) + ' sang vị trí khác', 'Đóng cửa sổ',
                        'Cuộn bảng sang phải'], '',
                       ['Các dòng cột bắt buộc không kéo đi được, thứ tự không đổi',
                        'Khi cuộn ngang, STT và %s luôn nằm bên trái, không bị cuộn mất' % ma])
    T['c_dong'] = K('Đóng cửa sổ mà không lưu thì không áp dụng thay đổi', 'P1', 'Bảng đang hiện cột %s.' % C['cot_tat'],
                    ['Mở Tùy chỉnh cột', 'Bỏ tích %s và kéo đổi thứ tự một cột' % C['cot_tat'], 'Bấm Đóng (hoặc nút X)',
                     'Quan sát bảng, rồi mở lại Tùy chỉnh cột'], '',
                    ['Bảng giữ nguyên cột %s và thứ tự cột cũ' % C['cot_tat'],
                     'Mở lại cửa sổ: %s vẫn được tích, thứ tự như trước khi chỉnh' % C['cot_tat']])
    T['c_nho'] = K('Cấu hình cột được ghi nhớ sau F5 và khi quay lại màn', 'P0',
                   'Vừa bật thêm cột %s và lưu cấu hình.' % an[0],
                   ['Chuyển sang màn khác rồi quay lại màn %s' % TT, 'Tải lại trang bằng F5'], '',
                   ['Cột %s vẫn hiển thị sau khi quay lại và sau khi tải lại trang' % an[0],
                    'Không phải cấu hình lại từ đầu'])
    T['c_tk'] = K('Cấu hình cột lưu riêng theo từng tài khoản', 'P2',
                  'TK-A đã bật cột %s và lưu. TK-H chưa chỉnh cột.' % an[0],
                  ['Đăng nhập TK-H, vào màn ' + TT, 'Quan sát các cột', 'Đăng nhập lại TK-A trên trình duyệt khác, vào màn'],
                  'Tài khoản: TK-A, TK-H',
                  ['TK-H thấy bộ cột mặc định, KHÔNG có cột ' + an[0],
                   'TK-A vẫn thấy cột %s dù đăng nhập ở trình duyệt khác' % an[0]])
    T['c_du_lieu'] = K('Cấu hình cột không ảnh hưởng dữ liệu và bộ lọc', 'P1',
                       'Đang lọc Trạng thái = Khóa, danh sách còn K dòng.',
                       ['Mở Tùy chỉnh cột, bật thêm 2 cột rồi Lưu', 'Quan sát danh sách'], '',
                       ['Vẫn đúng K dòng, ô lọc Trạng thái vẫn là Khóa', 'Dòng tổng không đổi'])

    # ===================== X. XUẤT DANH SÁCH EXCEL
    ef = C['export_fields']
    T['x_md'] = K('Xuất file với các trường mặc định', 'P0', 'Phạm vi xem có N %s, không lọc gì, cấu hình cột mặc định.' % obj,
                  ['Bấm Xuất Excel', 'Giữ nguyên các trường tích sẵn, bấm Xuất file', 'Mở file'], '',
                  ['Hiện "Xuất Excel thành công", tải về file %s' % C['export_file'],
                   'File mở được bằng Excel (định dạng .xlsx), dòng tiêu đề "%s"' % TT,
                   'Có đủ N dòng dữ liệu; cột theo đúng các trường đang tích, đúng thứ tự trong cửa sổ'])
    T['x_mot_so'] = K('Bỏ tích một trường thì file không có cột đó', 'P0', 'Đang mở cửa sổ Chọn trường xuất file.',
                      ['Bỏ tích trường ' + C['cot_tat'], 'Bấm Xuất file, mở file'], 'Trường bỏ tích: ' + C['cot_tat'],
                      ['File không có cột ' + C['cot_tat'], 'Các cột còn lại vẫn đủ và đúng thứ tự'])
    T['x_tim'] = K('Xuất theo từ khóa tìm nhanh', 'P1', 'Gõ "%s" ở ô tìm kiếm, nhấn Enter, danh sách còn M dòng.'
                   % C['tu_khoa_chung'],
                   ['Bấm Xuất Excel, bấm Xuất file', 'Mở file'], 'Từ khóa: ' + C['tu_khoa_chung'],
                   ['File chỉ chứa đúng M dòng khớp từ khóa'])
    T['x_rong'] = K('Xuất khi danh sách không có dòng nào', 'P2',
                    'Gõ từ khóa không khớp bản ghi nào, bảng hiện "Không có dữ liệu phù hợp."',
                    ['Bấm Xuất Excel, bấm Xuất file', 'Mở file'], 'Từ khóa: zzzz',
                    ['Không báo lỗi', 'File chỉ có dòng tiêu đề và dòng tên cột, không có dòng dữ liệu'])
    T['x_ten_cot'] = K('Tiêu đề cột, thứ tự cột và số lượng dòng trong file', 'P1',
                       'Phạm vi xem có N %s.' % obj,
                       ['Bấm Xuất Excel, bấm Chọn tất cả', 'Kéo trường %s lên đầu danh sách' % tn, 'Bấm Xuất file, mở file'],
                       '',
                       ['Tên cột trong file đúng nguyên văn: ' + ', '.join(ef) + ' (cột %s đứng đầu)' % tn,
                        'Số dòng dữ liệu đúng bằng N'])
    T['x_dinh_dang'] = K('Định dạng ngày, chữ tiếng Việt và ký tự đặc biệt trong file', 'P1',
                         'Có %s tên "%s" (chữ có dấu, dấu phẩy, dấu hai chấm).' % (obj, C['ten_dac_biet']),
                         ['Tìm "%s"' % C['ten_dac_biet'].split(',')[0], 'Xuất Excel đủ mọi trường, mở file'], '',
                         ['Tên hiện đúng "%s", không lỗi font, không mất dấu' % C['ten_dac_biet'],
                          'Ngày tạo / Ngày cập nhật dạng ngày/tháng/năm giờ:phút giống bảng',
                          'Mã giữ nguyên dạng chữ (không bị đổi thành số, không mất số 0 ở đầu)',
                          'Trạng thái ghi chữ "Hoạt động" / "Khóa"; ô không có dữ liệu để TRỐNG'])

    # ===================== XI. IMPORT TỪ FILE EXCEL
    T['i_sai_dinh_dang'] = K('Chọn file không phải Excel', 'P1', 'Đang mở cửa sổ ' + C['import_title'] + '.',
                             ['Bấm Chọn file Excel, chọn file PDF'], 'File: danh_sach.pdf',
                             ['Báo "Vui lòng chọn file .xlsx hoặc .xls"', 'Không có dòng nào lên bảng xem trước'])
    T['i_thieu_cot'] = K('Import thiếu cột trong file', 'P1', 'File Excel bị xóa cột "%s".' % C['import_cot_xoa'],
                         ['Chọn file', 'Bấm Load lên bảng'], 'File thiếu cột ' + C['import_cot_xoa'],
                         ['Báo "%s"' % C['import_header_err'], 'Không có dòng nào lên bảng, cửa sổ Import vẫn mở'])
    T['i_sai_ten_cot'] = K('Sai tên cột hoặc đổi thứ tự cột', 'P2', 'Có 2 file chuẩn bị từ file mẫu.',
                           ['File 1: đổi tên cột "%s" thành "%s cũ", chọn file, bấm Load lên bảng' % (tn, tn),
                            'File 2: giữ tên cột nhưng đổi chỗ 2 cột %s và %s, chọn file, bấm Load lên bảng' % (ma, tn)],
                           '',
                           ['File 1: báo "%s"' % C['import_header_err'],
                            'File 2: đọc đúng dữ liệu theo tên cột, bảng xem trước hiện mã và tên đúng ô'])
    T['i_rong'] = K('Import file Excel không có dữ liệu', 'P2', 'File mẫu chỉ có dòng tên cột, không có dòng nào khác.',
                    ['Chọn file', 'Bấm Load lên bảng'], '',
                    ['Báo "Sheet dữ liệu trống hoặc thiếu dòng."', 'Vẫn giữ nguyên cửa sổ Import'])
    T['i_dong_trong'] = K('File có dòng trống xen giữa', 'P2',
                          'File có 3 dòng hợp lệ, giữa dòng 1 và dòng 2 có 2 dòng để trống hoàn toàn.',
                          ['Chọn file', 'Bấm Load lên bảng'], '',
                          ['Dòng trống bị bỏ qua, bảng xem trước có đúng 3 dòng, "Tổng: 3"',
                           'File chỉ toàn dòng trống (dưới dòng tên cột): báo "Không có dòng dữ liệu hợp lệ (toàn dòng trống)."'])
    T['i_vuot_do_dai'] = K('Kiểm tra dữ liệu - %s vượt 50 ký tự' % ma, 'P1', 'File có 1 dòng %s dài 51 ký tự.' % ma,
                           ['Load lên bảng', 'Bấm Validate'], '%s: chuỗi 51 ký tự' % ma,
                           ['Dòng báo lỗi "%s: Nhập tối đa 50 ký tự"' % ma, 'Dòng này không được import'])
    T['i_khoang_trang_hoa'] = K('Kiểm tra dữ liệu - khoảng trắng và chữ hoa / thường', 'P2',
                                'Đã có %s mã "%s". File có 2 dòng theo Test data.' % (obj, A[0]),
                                ['Load lên bảng', 'Bấm Validate'],
                                ['Dòng 1: %s "%s" (chữ thường)' % (ma, A[0].lower()),
                                 'Dòng 2: %s "   %s   " (khoảng trắng 2 đầu), mã mới hợp lệ' % (tn, C['imp'][1])],
                                ['Dòng 1 báo trùng "%s: %s" (so trùng không phân biệt hoa thường)' % (ma, C['dup']),
                                 'Dòng 2 hợp lệ; khoảng trắng 2 đầu tự được bỏ khi đọc file'])
    T['i_tat_ca_hop_le'] = K('Import khi tất cả dòng hợp lệ', 'P0',
                             'File có 3 dòng hợp lệ, chưa tồn tại. Phạm vi xem đang có N %s.' % obj,
                             ['Chọn file, Load lên bảng', 'Bấm Validate', 'Bấm Import'], 'File: 3 dòng hợp lệ',
                             ['Bước 2: trong cửa sổ hiện "Tất cả 3 dòng đã hợp lệ. Có thể import ngay.", nút Import bấm được',
                              'Bước 3: hiện "%s", cửa sổ đóng' % C['import_ok'].format(n=3),
                              'Danh sách tự tải lại, dòng tổng = N + 3, 3 bản ghi mới ở trạng thái theo cột Trạng thái '
                              '(để trống = Hoạt động)'])
    T['i_khong_hop_le'] = K('Không có dòng nào hợp lệ', 'P1', 'File có 2 dòng, cả 2 đều thiếu %s.' % tn,
                            ['Load lên bảng, bấm Validate', 'Thử bấm Import'], 'File: 0 dòng hợp lệ',
                            ['Trong cửa sổ báo "Không có dòng nào hợp lệ để import. Hãy sửa các dòng lỗi và validate lại."',
                             'Nút Import mờ, không bấm được',
                             'Không có bản ghi mới nào được thêm'])
    T['i_tron'] = K('Còn dòng lỗi thì không Import được', 'P0', 'File có 2 dòng hợp lệ và 1 dòng lỗi, đã Validate.',
                    ['Thử bấm Import', 'Quan sát danh sách phía sau'], 'File: 2 hợp lệ, 1 lỗi',
                    ['Nút Import mờ, không bấm được khi còn dòng lỗi', 'Không có bản ghi mới nào được thêm',
                     'Phải sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi'])
    T['i_lai_file'] = K('Import lại đúng file vừa import', 'P1', 'Vừa import thành công file 3 dòng.',
                        ['Mở lại cửa sổ Import, chọn đúng file đó', 'Load lên bảng, bấm Validate'], '',
                        ['Cả 3 dòng báo lỗi trùng "%s: %s"' % (ma, C['dup']), 'Nút Import mờ, không tạo thêm bản ghi trùng'])
    T['i_dong_thoi'] = K('Hai người cùng import một file', 'P2',
                         'TK-A và TK-H cùng chọn một file 2 dòng hợp lệ, cùng đã Validate xong.',
                         ['TK-A bấm Import', 'TK-H bấm Import ngay sau'], '',
                         ['TK-A: "%s"' % C['import_ok'].format(n=2),
                          'TK-H: bảng kết quả "Import xong: 0 dòng thành công, 2 dòng lỗi bị bỏ qua", lý do trùng',
                          'Danh sách chỉ có đúng 1 bản ghi cho mỗi mã, không sinh bản ghi trùng'])
    T['i_man_khac'] = K('Dữ liệu import dùng được ngay ở màn liên quan', 'P1',
                        'Vừa import thành công %s "%s" (Hoạt động).' % (obj, C['imp'][0]),
                        ['Mở ' + C['man_dung'][0], 'Bấm Tạo mới, mở ô ' + C['man_dung'][1]], '',
                        ['Ô %s có ngay "%s"' % (C['man_dung'][1], C['imp'][0]), 'Không cần tải lại trang mới thấy'])

    # ===================== XIII. PHÂN QUYỀN
    T['q_mot_quyen'] = K('Một quyền "Quản lý kho" dùng cho mọi thao tác của màn', 'P0',
                         'TK-A có quyền "Quản lý kho" (gán qua vai trò), không có quyền nào khác của nhóm Danh mục kho.',
                         ['Đăng nhập TK-A, vào menu ' + MENU, 'Bấm mã một bản ghi (Xem chi tiết)',
                          'Bấm Lịch sử ở một dòng', 'Bấm Xuất Excel > Xuất file', 'Bấm Import Excel > Tải file mẫu'], '',
                         ['Mọi thao tác đều thực hiện được: xem danh sách, xem chi tiết, lịch sử, xuất, tải file mẫu import',
                          'Không có quyền "chỉ xem" riêng; Lịch sử không cần quyền riêng'])
    T['q_doi_quyen'] = K('Bị gỡ quyền khi đang mở màn', 'P1',
                         'TK-A đang mở cửa sổ Sửa %s. Quản trị gỡ quyền "Quản lý kho" khỏi vai trò của TK-A.' % B[0],
                         ['TK-A đổi Mô tả, bấm Lưu', 'TK-A tải lại trang', 'TK-A đăng xuất, đăng nhập lại'], '',
                         ['Bước 1: bị từ chối, hiện thông báo không có quyền thực hiện; Mô tả không đổi',
                          'Bước 2: màn bị chặn, bảng không có dữ liệu', 'Bước 3: mục "%s" không còn trên menu' % C['menu_item'],
                          'Gán lại quyền sau khi test'])
    return T
