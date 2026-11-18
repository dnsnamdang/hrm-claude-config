# -*- coding: utf-8 -*-
"""Phần DÙNG CHUNG cho testcase 2 báo cáo vận chuyển cùng khung (hiệu quả gộp xe vận tải, chi tiết chuyến xe) — khuôn chuẩn
skill testcase-documenter (tc_chuan.build_chuan, loai='bao_cao'). Khung C()/sections() chép từ mẫu đã duyệt
sale-customer-debt-reports/docs/compare/_tc_bc_chung.py; các hàm sinh case chung viết lại theo khung TransportReportPage
(Kỳ mặc định Tháng này, không ghi nhớ bộ lọc, phân trang theo nhóm cấp 1, popup danh sách lọc tại chỗ, In / Excel chọn bản + cột).
Tham số hoá theo màn qua dict m.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
sys.path.insert(0, SKILL)
from tc_chuan import build_chuan  # noqa: E402,F401

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


def _lines(x):
    if x is None:
        return []
    return [x] if isinstance(x, str) else list(x)


def _exp(x):
    out = []
    for s in _lines(x):
        s = s.strip()
        if s.startswith('- '):
            s = s[2:].strip()
        elif s.startswith('-') and not s[1:2].isdigit():
            s = s[1:].strip()
        out.append('-  ' + s)
    return '\n'.join(out)


def _sach(t):
    """Bỏ ký hiệu bị bộ kiểm emoji của skill chặn (mũi tên, dấu trừ toán học, biểu tượng kéo, nút phân trang)."""
    return (t.replace(' − ', ' trừ ').replace('−', '-').replace(' → ', ' -> ').replace('→', '->')
            .replace('☰', 'biểu tượng ba gạch').replace('✓', 'dấu tích').replace('›', '>').replace('«', '<<').replace('»', '>>').replace('‹', '<'))


def C(func, prio, pre, steps, data, exp):
    assert prio in ('P0', 'P1', 'P2'), func
    return tuple(_sach(x) for x in (func, prio, '\n'.join(_lines(pre)), '\n'.join(_lines(steps)), '\n'.join(_lines(data)), _exp(exp)))


def sections(groups):
    out = []
    for i, (title, cases) in enumerate(groups):
        out.append((ROMAN[i], title, [('%03d' % (k + 1),) + c for k, c in enumerate(cases)]))
    return out


def dem(groups):
    total = sum(len(c) for _, c in groups)
    p0 = sum(1 for _, cs in groups for c in cs if c[1] == 'P0')
    return ' · '.join('%s %d' % (t, len(c)) for t, c in groups) + ' · tổng %d (P0 %d = %.0f%%)' % (total, p0, 100.0 * p0 / total)


# ---------------------------------------------------------------- PHÂN TRANG theo nhóm cấp 1 (checklist 10–18, 23)
def pt_chung(m):
    dv, loc, nhieu = m['dv'], m['loc_nhieu'], m['nhieu_trang']
    return [
        C('Số dòng mặc định mỗi trang và đổi số dòng', 'P0', nhieu,
          ['1. ' + loc, '2. Đọc ô "Số dòng/trang" và đếm số dòng ' + dv + ' trên trang 1', '3. Sang trang 2', '4. Đổi ô "Số dòng/trang" sang 20'], '',
          ['Bước 2: ô "Số dòng/trang" mặc định 10, có các lựa chọn 10 / 20 / 50 / 100; trang 1 có đúng 10 dòng ' + dv,
           'Bước 4: bảng quay về trang 1, hiện 20 dòng ' + dv + ', chân bảng "Hiển thị 1–20 / N ' + dv + '"',
           'Tổng N, dòng TỔNG và khối tổng hợp không đổi khi đổi số dòng']),
        C('Nút sang trang kế tiếp và lùi về trang trước', 'P0', nhieu,
          ['1. ' + loc, '2. Bấm nút › (trang kế tiếp)', '3. Đọc thanh phân trang và chân bảng', '4. Bấm nút ‹ (trang trước)'], '',
          ['Bước 2: sang trang 2, số trang 2 được tô đậm, chân bảng "Hiển thị 11–20 / N ' + dv + '"',
           'Bước 4: quay lại trang 1, chân bảng "Hiển thị 1–10 / N ' + dv + '"',
           'Dữ liệu từng trang không lặp, không thiếu; các dòng con luôn nằm cùng trang với dòng ' + dv + ' của nó']),
        C('Nút về trang cuối và về trang đầu', 'P1', nhieu,
          ['1. ' + loc, '2. Bấm nút » (về trang cuối)', '3. Bấm nút « (về trang đầu)'], '',
          ['Bước 2: nhảy tới trang cuối, chân bảng "Hiển thị …–N / N ' + dv + '"', 'Bước 3: quay về trang 1']),
        C('Nút phân trang ở trang đầu và trang cuối', 'P2', nhieu,
          ['1. ' + loc + ', đứng ở trang 1, quan sát nút « và ‹', '2. Bấm » về trang cuối, quan sát nút › và »'], '',
          ['Ở trang 1: nút « và ‹ bị mờ, bấm không có tác dụng', 'Ở trang cuối: nút › và » bị mờ, bấm không có tác dụng']),
        C('STT dòng ' + dv + ' liên tục giữa các trang', 'P1', nhieu,
          ['1. ' + loc, '2. Ghi STT dòng ' + dv + ' cuối trang 1', '3. Sang trang 2, đọc STT dòng ' + dv + ' đầu tiên'], '',
          ['Trang 1 kết thúc ở X (số La Mã), trang 2 bắt đầu ở XI', 'STT dòng con đánh lại từ 1 trong từng nhóm']),
        C('Tổng số ' + dv + ' ở chân bảng', 'P0', nhieu,
          ['1. ' + loc, '2. Đọc chân bảng góc dưới trái', '3. Về trang cuối, đếm số dòng ' + dv], '',
          ['Chân bảng dạng "Hiển thị 1–10 / N ' + dv + '"', 'N = 10 × (số trang − 1) + số dòng ' + dv + ' ở trang cuối',
           m.get('tong_ghi_chu', 'N bằng số nhóm có dữ liệu theo bộ lọc')]),
        C('Đổi bộ lọc khi đang ở trang giữa thì quay về trang 1', 'P0', nhieu,
          ['1. ' + loc + ', bấm sang trang 3', '2. ' + m['doi_loc']], '',
          ['Bảng quay về trang 1 theo kết quả lọc mới', 'Chân bảng, dòng TỔNG, khối tổng hợp tính lại theo bộ lọc mới']),
        C('Bảng không cho sắp xếp theo cột', 'P2', 'Báo cáo có dữ liệu.',
          ['1. ' + m['loc'], '2. Bấm lần lượt vào tiêu đề từng cột của bảng chính'], '',
          ['Tiêu đề cột KHÔNG có mũi tên sắp xếp', 'Bấm tiêu đề không làm đổi thứ tự dòng; thứ tự luôn theo quy tắc cố định: ' + m['thu_tu']]),
    ]


# ---------------------------------------------------------------- KỲ + LƯU TRẠNG THÁI (checklist 36, 44–48)
def ky_chung(m):
    loc = m['loc']
    return [
        C('Giá trị mặc định của ô Kỳ', 'P0', 'Tài khoản bất kỳ.',
          ['1. ' + m['menu'], '2. Đọc ô Kỳ, dòng kỳ ở khối tổng hợp'], '',
          ['Ô Kỳ mặc định "Tháng này", không có nút xoá', 'Dòng kỳ ghi "Kỳ tháng <tháng hiện tại>/<năm> (' + m['theo'] + ')"',
           'Báo cáo tự tải ngay, không cần bấm Tìm kiếm']),
        C('Các lựa chọn của ô Kỳ', 'P1', 'Đang mở màn.',
          ['1. Bấm ô Kỳ', '2. Lần lượt chọn Tuần này, Tháng trước, Năm nay'], '',
          ['Danh sách: Tuần này, Tháng này, Tháng trước, Năm nay, Tuỳ chọn',
           'Mỗi lần chọn báo cáo tự tải lại; dòng kỳ ghi đúng "Kỳ tuần này" / "Kỳ tháng mm/yyyy" của tháng trước / "Kỳ năm yyyy"',
           'Tuần này tính từ thứ Hai đến Chủ nhật của tuần hiện tại']),
        C('Kỳ Tuỳ chọn hiện thêm ô Thời gian', 'P0', 'Đang mở màn.',
          ['1. Chọn Kỳ = Tuỳ chọn', '2. Quan sát khu vực lọc', '3. Chọn Từ ngày, chưa chọn Đến ngày', '4. Chọn Đến ngày'], 'Từ ngày 01/10/2026, Đến ngày 31/10/2026',
          ['Bước 2: xuất hiện ô "Thời gian" (Từ ngày → Đến ngày) ngay sau ô Kỳ; báo cáo chưa tải lại',
           'Bước 3: báo cáo chưa tải lại', 'Bước 4: báo cáo tự tải, dòng kỳ "Kỳ từ 01/10/2026 đến 31/10/2026 (' + m['theo'] + ')"',
           'Số liệu bằng đúng kỳ Tháng trước khi tháng trước là tháng 10/2026']),
        C('Kỳ Tuỳ chọn thiếu ngày mà bấm Tìm kiếm thì bị chặn', 'P0', 'Đã chọn Kỳ = Tuỳ chọn, ô Thời gian trống.',
          ['1. Bấm Tìm kiếm', '2. Chỉ chọn Từ ngày rồi bấm Tìm kiếm'], '',
          ['Cả 2 lần đều báo đỏ "Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn."', 'Báo cáo không tải lại, số liệu đang hiện giữ nguyên']),
        C('Kỳ Tuỳ chọn tính cả 2 ngày đầu mút', 'P1', m['bien_ngay'],
          ['1. Chọn Kỳ = Tuỳ chọn, Từ ngày = Đến ngày = ngày của chuyến mẫu', '2. Đọc số liệu'], '',
          ['Chuyến có ' + m['ngay_loc'] + ' đúng ngày đã chọn được tính (kể cả phát sinh cuối ngày)', 'Chuyến của ngày hôm sau không được tính']),
        C('Không chọn được Đến ngày nhỏ hơn Từ ngày', 'P1', 'Đã chọn Kỳ = Tuỳ chọn.',
          ['1. Chọn Từ ngày 20/10/2026', '2. Mở lịch Đến ngày, thử chọn 10/10/2026'], '',
          ['Lịch không cho chọn ngày trước Từ ngày (hoặc hệ thống báo "Ngày kết thúc phải sau hoặc bằng ngày bắt đầu")', 'Báo cáo không tải với khoảng ngày ngược']),
        C('Đổi Kỳ khỏi Tuỳ chọn thì ô Thời gian biến mất', 'P2', 'Đang chọn Kỳ Tuỳ chọn 01/10/2026 - 31/10/2026.',
          ['1. Đổi Kỳ sang Năm nay', '2. Đổi Kỳ lại Tuỳ chọn'], '',
          ['Bước 1: ô Thời gian biến mất, báo cáo tải theo năm nay', 'Bước 2: ô Thời gian hiện lại TRỐNG (khoảng ngày cũ đã bị xoá)']),
        C('Xóa lọc đưa mọi ô về mặc định', 'P0', 'Đang lọc ' + m['loc_nhieu_o'] + '.',
          ['1. Bấm Xóa lọc'], '',
          ['Kỳ về "Tháng này", các ô lọc khác về trống' + m.get('xoaloc_them', ''), 'Ô chọn cấp bung về mặc định', 'Báo cáo tự tải lại, về trang 1']),
        C('Rời sang màn khác rồi quay lại thì bộ lọc về mặc định', 'P1', 'Đang xem báo cáo đã lọc.',
          ['1. ' + loc + ', đổi thêm 1 ô lọc', '2. Vào màn khác trên menu (vd ' + m['man_khac'] + ')', '3. Quay lại màn báo cáo bằng menu'], '',
          ['Kỳ về "Tháng này", các ô lọc khác trống (màn không ghi nhớ bộ lọc)', 'Báo cáo tự tải theo kỳ mặc định']),
        C('Tải lại trang (F5) khi đang lọc', 'P1', 'Đang xem báo cáo đã lọc.',
          ['1. ' + loc, '2. Nhấn F5'], '', ['Bộ lọc về mặc định như mở màn lần đầu', 'Báo cáo tự tải theo Kỳ "Tháng này"']),
        C('Mở màn ở tab trình duyệt mới khi tab cũ đang lọc', 'P2', 'Tab 1 đang lọc báo cáo.',
          ['1. Mở tab mới, vào màn báo cáo bằng menu', '2. Quay lại tab 1'], '',
          ['Tab 2 mở với bộ lọc mặc định (Kỳ "Tháng này")', 'Tab 1 giữ nguyên bộ lọc và kết quả']),
        C('Đăng xuất, đăng nhập tài khoản khác trên cùng trình duyệt', 'P1', 'Có 2 tài khoản A (quyền mức Tổng công ty) và B (không quyền).',
          ['1. Tài khoản A mở báo cáo, chọn Kỳ Năm nay', '2. Đăng xuất, đăng nhập B, mở báo cáo'], '',
          ['B thấy bộ lọc mặc định, chỉ số liệu trong phạm vi của B', 'Không còn bộ lọc / số liệu của A']),
        C('Đổi bộ lọc liên tục chỉ giữ kết quả lần cuối', 'P2', 'Đang mở màn.',
          ['1. Đổi Kỳ thật nhanh: Năm nay → Tháng trước → Tuần này'], '',
          ['Bảng mờ đi trong lúc tải, không nháy trắng', 'Kết quả cuối cùng đúng kỳ "Tuần này", không bị kết quả của lần chọn trước đè lên']),
    ]


# ---------------------------------------------------------------- POPUP DANH SÁCH (checklist 186–197 + tìm kiếm 26–35 trong popup)
def popup_chung(m):
    o, dv = m['popup_mo'], m['popup_dv']
    return [
        C('Ô số bằng 0 không bấm được', 'P1', m['pre_0'],
          ['1. ' + m['loc'], '2. Rê chuột / bấm vào ô số bằng 0'], '', ['Số 0 hiện chữ thường, không gạch chân', 'Bấm không mở popup']),
        C('Popup tải đủ mọi dòng của ô số', 'P0', m['pre_popup'],
          ['1. ' + o, '2. Đọc bộ đếm "n / N ' + dv + '", chuyển hết các trang của popup'], '',
          ['N = đúng con số đã bấm', 'Popup lấy đủ mọi dòng (kể cả khi trên 500 dòng), không dừng ở trang đầu']),
        C('Tìm trong popup theo một phần, không phân biệt hoa thường và dấu', 'P1', m['pre_popup'],
          ['1. ' + o, '2. Gõ "' + m['popup_kw'] + '" vào ô tìm', '3. Xoá, gõ lại bằng chữ hoa / không dấu'], '',
          ['Lọc ngay khi gõ (không cần Enter); bộ đếm "n / N ' + dv + '" giảm theo', 'Kết quả bước 2 và 3 giống nhau', 'Ô tìm chỉ tìm theo: ' + m['popup_fields']]),
        C('Tìm trong popup từ khoá không tồn tại / ký tự đặc biệt', 'P2', m['pre_popup'],
          ['1. ' + o, '2. Gõ lần lượt từng chuỗi ở Test data'], ['zzzkhongtontai', '%', "' OR 1=1 --", '<b>x</b>'],
          ['Bảng popup hiện "' + m['popup_empty'] + '", bộ đếm "0 / N ' + dv + '"', 'Không lỗi, không treo, ký tự hiện đúng như gõ']),
        C('Khoảng trắng đầu cuối và nút x trong ô tìm', 'P2', m['pre_popup'],
          ['1. ' + o, '2. Gõ "  ' + m['popup_kw'] + '  "', '3. Bấm nút x trong ô tìm'], '',
          ['Bước 2: kết quả như khi không có khoảng trắng', 'Bước 3: ô tìm trống, popup hiện lại đủ N ' + dv]),
        C('Ô lọc trong popup và nút Xoá lọc', 'P1', m['pre_popup'],
          ['1. ' + o, '2. Chọn 1 giá trị ở ô ' + m['popup_filter'], '3. Gõ thêm từ khoá', '4. Bấm biểu tượng Xoá lọc'], '',
          ['Bước 2-3: chỉ còn dòng thoả cả 2 điều kiện', 'Biểu tượng Xoá lọc chỉ hiện khi có ô lọc đang chọn', 'Bước 4: bỏ lọc, hiện lại đủ N ' + dv]),
        C('Sắp xếp theo cột trong popup', 'P1', m['pre_popup'],
          ['1. ' + o, '2. Bấm tiêu đề cột ' + m['popup_sort'] + ' 1 lần, rồi lần nữa', '3. Sang trang 2'], '',
          ['Lần 1 tăng dần, lần 2 giảm dần (số so theo số, ngày so theo ngày)', 'Ô trống luôn xuống cuối', 'Sang trang vẫn giữ thứ tự đã sắp']),
        C('Phân trang trong popup', 'P1', m['pre_popup'],
          ['1. ' + o, '2. Đọc số dòng/trang, đổi sang 20'], '',
          ['Mặc định 10 dòng/trang, lựa chọn 10/20/50/100', 'Chân popup "Hiển thị a–b / n ' + dv + '"', 'Đổi số dòng về trang 1']),
        C('Số 0 trong popup để trống', 'P2', m['pre_popup'], ['1. ' + o, '2. Tìm dòng có cột số bằng 0'], '', ['Ô số bằng 0 để trống (không in "0")']),
        C('Đóng popup giữ nguyên báo cáo, mở lại thì sạch lọc', 'P1', m['pre_popup'],
          ['1. ' + o + ', gõ từ khoá, sắp xếp 1 cột, sang trang 2', '2. Bấm Đóng (hoặc ×)', '3. Mở lại đúng ô số đó'], '',
          ['Bước 2: báo cáo giữ nguyên bộ lọc, trang, cấp bung', 'Bước 3: popup mở ở trang 1, ô tìm trống, không còn sắp xếp / ô lọc cũ']),
        C('Bản in danh sách từ popup', 'P1', m['pre_popup'],
          ['1. ' + o + ', gõ từ khoá còn ít dòng', '2. Bấm In danh sách', '3. Bỏ tích vài cột, bấm In'], '',
          ['Bước 2: cửa sổ "In danh sách" liệt kê đúng các cột đang hiện trên popup, đã tích sẵn',
           'Bước 3: xem trước bản in "' + m['list_title'] + '", chỉ gồm các dòng khớp ô số + từ khoá, đúng các cột đã chọn, có dòng phạm vi (tiêu đề popup)',
           'Bỏ hết cột rồi bấm In: "Vui lòng chọn ít nhất 1 cột để in"']),
        C('Xuất Excel danh sách từ popup', 'P1', m['pre_popup'],
          ['1. ' + o, '2. Bấm Xuất Excel danh sách' + m.get('popup_xl_buoc', ''), '3. Mở file'], '',
          ['Tải file "' + m['list_file'] + '"', m['popup_xl_noi_dung'], 'Ô số là kiểu số, định dạng 1,234,567']),
    ]


# ---------------------------------------------------------------- TÙY CHỈNH CỘT (checklist 198–211)
def cot_chung(m):
    return [
        C('Mở cửa sổ Tuỳ chỉnh cột', 'P1', 'Đang mở màn' + m.get('cot_pre', '') + '.',
          ['1. Bấm nút Cấu hình cột hiển thị (biểu tượng cột, đầu cụm nút trên khu vực lọc)'], '',
          ['Mở cửa sổ "Tuỳ chỉnh cột", dòng hướng dẫn "Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."',
           'Danh sách: ' + m['cot_ds'], 'Mặc định tích tất cả, dòng đếm "Đang chọn ' + m['cot_n'] + '/' + m['cot_n'] + ' cột"']),
        C('Cột khoá không ẩn được', 'P0', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
          ['1. Thử bỏ tích cột STT và cột ' + m['cot_khoa'], '2. Bấm Bỏ chọn hết'], '',
          ['STT và ' + m['cot_khoa'] + ' có biểu tượng khoá, không bỏ tích được', 'Bỏ chọn hết vẫn giữ 2 cột khoá']),
        C('Ẩn cột và lưu', 'P0', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
          ['1. Bỏ tích cột ' + m['cot_an'], '2. Bấm Lưu'], '',
          ['Thông báo "Cập nhật thành công"', 'Bảng không còn cột ' + m['cot_an'] + '; dòng TỔNG / dòng nhóm vẫn khớp các cột còn lại']),
        C('Hiện lại cột đã ẩn', 'P1', 'Cột ' + m['cot_an'] + ' đang bị ẩn.',
          ['1. Mở Tuỳ chỉnh cột', '2. Bấm Chọn tất cả, Lưu'], '', ['Bảng hiện lại đủ cột, đúng vị trí']),
        C('Kéo thả đổi thứ tự cột', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
          ['1. Kéo ☰ của cột ' + m['cot_keo'] + ' lên ngay sau cột khoá', '2. Bấm Lưu'], '',
          ['Bảng hiện cột ' + m['cot_keo'] + ' ngay sau cột ' + m['cot_khoa'] + ', tiêu đề và số liệu đi cùng nhau']),
        C('Đóng không lưu', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
          ['1. Bỏ tích vài cột', '2. Bấm Đóng (hoặc ×)'], '', ['Cửa sổ đóng, bảng giữ nguyên cột như trước']),
        C('Cấu hình cột được ghi nhớ sau F5 và theo tài khoản', 'P1', 'Tài khoản A đã ẩn cột ' + m['cot_an'] + '; tài khoản B chưa cấu hình.',
          ['1. Tài khoản A nhấn F5, đăng xuất rồi đăng nhập lại', '2. Tài khoản B mở báo cáo trên cùng trình duyệt'], '',
          ['A: vẫn ẩn cột ' + m['cot_an'], 'B: thấy đủ cột (cấu hình theo từng người dùng)']),
        C('Tuỳ chỉnh cột không làm đổi số liệu, bộ lọc, In / Excel', 'P1', 'Đang lọc ' + m['loc_nhieu_o'] + ', đã ẩn cột ' + m['cot_an'] + '.',
          ['1. So dòng TỔNG trước / sau khi ẩn cột', '2. Bấm In báo cáo, xem danh sách cột in', '3. Xuất Excel bảng tổng hợp'], '',
          ['Bộ lọc, trang, số liệu các cột còn lại không đổi', 'Cửa sổ In / Xuất Excel vẫn liệt kê đủ cột (kể cả cột ' + m['cot_an'] + ')',
           'Cấu hình cột chỉ áp cho bảng trên màn']),
    ]


# ---------------------------------------------------------------- PHÂN QUYỀN CHUNG (checklist 287, 293, 295–299)
def pq_chung(m):
    return [
        C('Không có quyền vẫn mở được màn và đủ nút', 'P0', 'Tài khoản không có ' + m['quyen_ten'] + ' ở công ty đang làm việc.',
          ['1. Đăng nhập tài khoản đó', '2. ' + m['menu'], '3. Quan sát các nút'], '',
          ['Menu vẫn hiện mục "' + m['ten'] + '", màn mở bình thường, không báo thiếu quyền',
           'Đủ nút Cấu hình cột hiển thị, In báo cáo, Xuất Excel; bấm số vẫn mở popup',
           'Ô Công ty bị khoá ở công ty của tài khoản']),
        C('Mở màn bằng đường dẫn trực tiếp khi không có quyền', 'P1', 'Tài khoản không có ' + m['quyen_ten'] + '; biết đường dẫn của màn.',
          ['1. Đăng nhập tài khoản đó', '2. Dán đường dẫn màn vào thanh địa chỉ, nhấn Enter'], 'Đường dẫn: <địa chỉ hệ thống>' + m['url'],
          ['Màn mở như khi vào từ menu', 'Chỉ thấy số liệu trong phạm vi "của mình" (BR phạm vi)']),
        C('Sửa tay tham số Công ty trên thanh địa chỉ khi không có quyền tổng công ty', 'P1', m['pre_url_cty'],
          ['1. Đăng nhập tài khoản mức Công ty / không quyền', '2. Mở đường dẫn màn kèm tham số công ty của công ty khác'], 'Đường dẫn: <địa chỉ hệ thống>' + m['url'] + '?company_id=<id công ty khác>',
          ['Ô Công ty vẫn khoá ở công ty của tài khoản', 'KHÔNG hiện số liệu của công ty khác, không báo lỗi']),
        C('Đổi quyền trong lúc đang xem báo cáo', 'P1', 'Tài khoản X đang có ' + m['quyen_cao'] + ', đang mở màn, Kỳ Năm nay.',
          ['1. Ghi lại dòng TỔNG', '2. Người quản trị gỡ quyền của X', '3. Ở màn đang mở, bấm Tìm kiếm', '4. Nhấn F5'], '',
          ['Bước 3: số liệu thu hẹp ngay về phạm vi mới, dòng TỔNG giảm', 'Bước 4: ô Công ty bị khoá ở công ty của X', 'Không lúc nào hiện số liệu ngoài phạm vi mới']),
        C('Đổi công ty đang làm việc thì phạm vi tính lại', 'P1', 'Tài khoản Y có ' + m['quyen_cao'] + ' ở công ty A, không có quyền ở công ty B.',
          ['1. Đang làm việc ở công ty A, mở báo cáo', '2. Đổi công ty đang làm việc sang B, mở lại báo cáo'], '',
          ['Bước 1: phạm vi theo quyền ở công ty A', 'Bước 2: quyền tính lại theo công ty B (không quyền → chỉ số liệu của mình)', 'Không thấy số liệu ngoài phạm vi ở công ty B']),
        C('Phạm vi áp cho mọi con số, popup, In, Excel', 'P0', 'Tài khoản không quyền NV-A.',
          ['1. Mở báo cáo Kỳ Năm nay', '2. Bấm số ở dòng TỔNG', '3. In bảng tổng hợp, Xuất Excel'], '',
          ['Popup, bản in, file Excel chỉ chứa số liệu trong phạm vi của NV-A, khớp dòng TỔNG trên màn']),
    ]
