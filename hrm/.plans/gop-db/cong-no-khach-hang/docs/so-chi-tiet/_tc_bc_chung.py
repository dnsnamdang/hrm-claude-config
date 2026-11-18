# -*- coding: utf-8 -*-
"""Phần DÙNG CHUNG cho testcase 3 màn báo cáo công nợ KH (compare / by-employee / details) theo khuôn chuẩn
tab "13. DM quốc gia" (xem xuat-tai-lieu-chuyen-doi/TC_CHUAN.md, loại bao_cao).

- C(...)        : 1 case (chức năng, priority, tiền điều kiện, bước, test data, expected) — bước / expected nhận list.
- sections(...) : [(TIÊU ĐỀ NHÓM, [case…]), …] -> SECTIONS cho build_chuan (đánh La Mã liên tục + số case 001…).
- Các hàm pt_*, tk_*, luu_*, xl_*, pq_* sinh các case CHUNG theo checklist "Mẫu tài liệu.xlsx" (phân trang, tìm kiếm,
  lưu trạng thái bộ lọc, xuất Excel, phân quyền), tham số hoá theo từng màn qua dict `m`.
Hành vi bám code hrm-client (V2BaseSmartFilterPanel, filterStateMixin + isPageReload, b-pagination) đọc ngày 03/11/2026.
"""

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
        elif s.startswith('-') and not s[1:2].isdigit():   # giữ dấu âm của số (vd -2,251,800)
            s = s[1:].strip()
        out.append('-  ' + s)
    return '\n'.join(out)


def C(func, prio, pre, steps, data, exp):
    assert prio in ('P0', 'P1', 'P2'), func
    return (func, prio, '\n'.join(_lines(pre)), '\n'.join(_lines(steps)), '\n'.join(_lines(data)), _exp(exp))


def sections(groups):
    out = []
    for i, (title, cases) in enumerate(groups):
        out.append((ROMAN[i], title, [('%03d' % (k + 1),) + c for k, c in enumerate(cases)]))
    return out


def dem(groups):
    return ' · '.join('%s %d' % (t, len(c)) for t, c in groups) + ' · tổng %d' % sum(len(c) for _, c in groups)


# ---------------------------------------------------------------- PHÂN TRANG (checklist 10–18) + cột không sắp xếp (23)
def pt_chung(m):
    dv, loc, nhieu = m['dv'], m['loc'], m['nhieu_trang']
    return [
        C('Số dòng mặc định mỗi trang và đổi số dòng', 'P0', nhieu,
          ['1. ' + loc, '2. Đọc ô "Số dòng/trang" và đếm số ' + dv + ' trên trang 1', '3. Sang trang 2',
           '4. Đổi ô "Số dòng/trang" sang 20'], '',
          ['Bước 2: ô "Số dòng/trang" mặc định 10, có các lựa chọn 10 / 20 / 50 / 100; trang 1 có đúng 10 ' + dv,
           'Bước 4: bảng quay về trang 1, hiện 20 ' + dv + ', chân bảng "Hiển thị 1–20 / N ' + dv + '"',
           'Tổng N không đổi khi đổi số dòng']),
        C('Nút sang trang kế tiếp và lùi về trang trước', 'P0', nhieu,
          ['1. ' + loc, '2. Bấm nút › (trang kế tiếp)', '3. Đọc thanh phân trang và chân bảng', '4. Bấm nút ‹ (trang trước)'], '',
          ['Bước 2: sang trang 2, số trang 2 được tô đậm, chân bảng "Hiển thị 11–20 / N ' + dv + '"',
           'Bước 4: quay lại trang 1, chân bảng "Hiển thị 1–10 / N ' + dv + '"',
           'Dữ liệu từng trang không lặp, không thiếu ' + dv]),
        C('Nút về trang cuối và về trang đầu', 'P1', nhieu,
          ['1. ' + loc, '2. Bấm nút » (về trang cuối)', '3. Đọc chân bảng', '4. Bấm nút « (về trang đầu)'], '',
          ['Bước 2: nhảy tới trang cuối cùng, chân bảng "Hiển thị …–N / N ' + dv + '"',
           'Bước 4: quay về trang 1, chân bảng "Hiển thị 1–10 / N ' + dv + '"']),
        C('Nút phân trang ở trang đầu và trang cuối', 'P1', nhieu,
          ['1. ' + loc + ', đứng ở trang 1, quan sát hai nút « và ‹', '2. Bấm » để về trang cuối, quan sát hai nút › và »'], '',
          ['Ở trang 1: nút « và ‹ bị mờ, bấm không có tác dụng',
           'Ở trang cuối: nút › và » bị mờ, bấm không có tác dụng']),
        C('Tổng số ' + dv + ' ở chân bảng', 'P0', m.get('pre_tong', nhieu),
          ['1. ' + loc, '2. Đọc chân bảng ở góc dưới bên trái', '3. Bấm » về trang cuối, đếm số ' + dv + ' trang cuối'], '',
          ['Chân bảng theo đúng khuôn "Hiển thị 1–10 / N ' + dv + '"; N từ 1,000 trở lên có dấu phẩy ngăn hàng nghìn (vd "/ 25,309")',
           'N chỉ đếm ' + dv + m.get('tong_ghi_chu', '') + '; N = 10 × (số trang - 1) + số ' + dv + ' ở trang cuối',
           'Bảng không có dữ liệu thì KHÔNG hiện chân bảng và thanh phân trang']),
        C('Đổi bộ lọc khi đang ở trang giữa thì quay về trang 1', 'P0', nhieu,
          ['1. ' + loc + ', bấm sang trang 3', '2. ' + m['doi_loc']], '',
          ['Bảng quay về trang 1 theo kết quả lọc mới', 'Chân bảng tính lại "Hiển thị 1–… / N ' + dv + '" theo bộ lọc mới']),
        C('Các cột không cho sắp xếp', 'P2', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. ' + loc, '2. Bấm lần lượt vào tiêu đề từng cột', '3. Quan sát bảng'], '',
          ['Tiêu đề cột KHÔNG có biểu tượng mũi tên sắp xếp',
           'Bấm vào tiêu đề không làm thay đổi thứ tự dòng (báo cáo luôn xếp theo thứ tự cố định)']),
    ]


# ---------------------------------------------------------------- TÌM NHANH (checklist 28, 30–35)
def tk_chung(m):
    loc, kw = m['loc'], m['tu_khoa']
    out = [
        C('Tìm nhanh không phân biệt chữ hoa chữ thường', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. ' + loc, '2. Gõ từ khóa toàn chữ thường vào ô tìm nhanh, nhấn Enter, ghi nhận kết quả',
           '3. Xóa, gõ lại cùng từ khóa toàn chữ hoa, nhấn Enter', '4. So sánh'], 'Từ khóa: ' + kw + ' (chữ thường / CHỮ HOA)',
          ['Hai lần tìm cho ra CÙNG một tập kết quả, cùng chân bảng']),
        C('Tìm nhanh từ khóa không tồn tại', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. ' + loc, '2. Gõ chuỗi chắc chắn không tồn tại vào ô tìm nhanh', '3. Nhấn Enter'], 'Từ khóa: zzzkhongtontai999',
          ['Bảng hiện "Không có dữ liệu phù hợp bộ lọc."', 'Không hiện dòng Tổng cộng, không có chân bảng và thanh phân trang']),
        C('Tìm nhanh với ký tự đặc biệt', 'P2', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. ' + loc, '2. Gõ lần lượt từng chuỗi ở Test data vào ô tìm nhanh, nhấn Enter'], ['%', '_', "' OR 1=1 --", '<b>abc</b>'],
          ['Ký tự % và _ được hiểu đúng là ký tự thường (không khớp tất cả): bảng hiện "Không có dữ liệu phù hợp bộ lọc." nếu không có số hiệu chứa đúng ký tự đó',
           'Không báo lỗi hệ thống, màn không treo, không hiện chữ in đậm từ chuỗi đã gõ']),
        C('Tìm nhanh có khoảng trắng đầu và cuối', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. ' + loc, '2. Gõ từ khóa có 2 dấu cách ở đầu và cuối, nhấn Enter', '3. Gõ lại từ khóa không có dấu cách, nhấn Enter', '4. So sánh'],
          'Từ khóa: "  ' + kw + '  "',
          ['Hai lần tìm cho ra cùng một kết quả (khoảng trắng đầu / cuối được bỏ qua)']),
        C('Giới hạn độ dài ô tìm nhanh', 'P2', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. ' + loc, '2. Dán chuỗi Test data vào ô tìm nhanh, kiểm tra chuỗi có bị cắt bớt không', '3. Nhấn Enter', '4. Bấm Làm mới'],
          'Chuỗi 500 ký tự (vd chữ "abcde" lặp lại 100 lần)',
          ['Bước 2: ô tìm nhanh nhận đủ 500 ký tự, không có thông báo lỗi',
           'Bước 3: bảng hiện "Không có dữ liệu phù hợp bộ lọc."; màn không treo, không báo lỗi hệ thống',
           'Bước 4: mọi ô lọc về trống, bảng về lời nhắc "' + m['loi_nhac'] + '"']),
        C('Gõ từ khóa chưa nhấn Enter thì bảng chưa lọc', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. ' + loc, '2. Gõ từ khóa vào ô tìm nhanh, KHÔNG nhấn Enter, không bấm Tìm kiếm', '3. Nhấn Enter', '4. Gõ từ khóa khác, bấm nút Tìm kiếm'],
          'Từ khóa: ' + kw,
          ['Bước 2: bảng chưa đổi', 'Bước 3: bảng lọc theo từ khóa, về trang 1', 'Bước 4: bấm nút Tìm kiếm cho kết quả giống nhấn Enter']),
        C('Xóa từ khóa thì danh sách quay về đầy đủ', 'P0', 'Đang tìm nhanh với từ khóa cho ra ít kết quả.',
          ['1. Bấm nút x trong ô tìm nhanh (hoặc xóa hết nội dung ô)', '2. Nhấn Enter hoặc bấm Tìm kiếm'], '',
          ['Bước 1: ô tìm nhanh trống, bảng chưa đổi', 'Bước 2: chân bảng quay lại tổng ban đầu (như khi chưa tìm), bảng về trang 1']),
    ]
    if m.get('co_dau'):
        out.insert(1, C('Tìm nhanh tên khách hàng có dấu và không dấu', 'P2', 'Có khách hàng tên tiếng Việt có dấu, có phát sinh trong kỳ.',
                        ['1. ' + m['loc_khong_kh'], '2. Gõ một phần tên khách có dấu vào ô tìm nhanh, nhấn Enter, ghi nhận kết quả',
                         '3. Gõ lại đúng phần tên đó nhưng không dấu, nhấn Enter'], m['co_dau'],
                        ['Bước 2: còn các hợp đồng của khách có tên chứa từ khóa',
                         'Bước 3: ra cùng tập kết quả như bước 2 (tìm không phân biệt dấu)']))
    return out


# ---------------------------------------------------------------- LƯU TRẠNG THÁI BỘ LỌC (checklist 45–48)
def luu_chung(m):
    loc, ln = m['loc'], m['loi_nhac']
    return [
        C('Rời sang màn khác rồi quay lại thì bộ lọc trở về mặc định', 'P1', 'Đang xem báo cáo đã lọc có số liệu.',
          ['1. ' + loc + ', gõ thêm từ khóa ở ô tìm nhanh, nhấn Enter', '2. Vào màn khác trên menu (vd ' + m['man_khac'] + ')',
           '3. Quay lại màn báo cáo bằng menu', '4. Quan sát khu vực lọc và bảng'], '',
          ['Ô Thời gian, các ô lọc và ô tìm nhanh trở về trống', 'Bảng hiện lời nhắc "' + ln + '"']),
        C('Tải lại trang (F5) khi đang lọc', 'P1', 'Đang xem báo cáo đã lọc có số liệu.',
          ['1. ' + loc, '2. Nhấn F5 tải lại trang', '3. Quan sát khu vực lọc và bảng'], '',
          ['Mọi ô lọc (kể cả Thời gian) và ô tìm nhanh trở về trống, giống như bấm Làm mới',
           'Bảng hiện lời nhắc "' + ln + '", không tự tải số liệu']),
        C('Đăng xuất, đăng nhập tài khoản khác trên cùng trình duyệt', 'P1', 'Có 2 tài khoản A và B, dùng chung một trình duyệt.',
          ['1. Đăng nhập tài khoản A, mở màn báo cáo, ' + loc[0].lower() + loc[1:], '2. Đăng xuất',
           '3. Đăng nhập tài khoản B, mở màn báo cáo', '4. Quan sát khu vực lọc và bảng'], '',
          ['Tài khoản B thấy mọi ô lọc trống, bảng hiện lời nhắc "' + ln + '"',
           'Bộ lọc và số liệu của tài khoản A KHÔNG hiện sang tài khoản B']),
        C('Mở màn ở tab trình duyệt mới khi tab cũ đang lọc', 'P2', 'Tab 1 đang mở màn báo cáo.',
          ['1. Ở tab 1: ' + loc[0].lower() + loc[1:], '2. Trong vòng 10 phút, mở tab trình duyệt mới, vào màn báo cáo bằng menu',
           '3. Quan sát tab 2', '4. Quay lại tab 1, quan sát'], '',
          ['Tab 2: mở ra với đúng bộ lọc tab 1 đang dùng và tự tải số liệu (bộ lọc được nhớ 10 phút trên cùng trình duyệt)',
           'Tab 1: vẫn giữ nguyên bộ lọc, trang và kết quả đang xem',
           'Quá 10 phút không thao tác rồi mới mở tab mới: tab mới có bộ lọc trống']),
    ]


# ---------------------------------------------------------------- XUẤT EXCEL CHUNG (checklist 216, 218, 219, 221–230)
def xl_chung(m):
    loc, nhieu, f = m['loc'], m['nhieu_trang'], m['excel_file']
    return [
        C('Không chọn trường nào', 'P1', 'Đang mở cửa sổ "Chọn trường xuất Excel".',
          ['1. Bấm "Bỏ chọn hết"', '2. Thử bấm "Xuất file"', '3. Bấm "Chọn tất cả"'], '',
          ['Bước 1: dòng đếm hiện "Đang chọn 0/' + m['so_truong'] + ' trường"',
           'Bước 2: nút "Xuất file" mờ, không bấm được, không tải file',
           'Bước 3: dòng đếm về "Đang chọn ' + m['so_truong'] + '/' + m['so_truong'] + ' trường"']),
        C('Đóng cửa sổ chọn trường thì không xuất', 'P2', 'Đang mở cửa sổ "Chọn trường xuất Excel".',
          ['1. Bỏ tích vài trường', '2. Bấm "Đóng"'], '',
          ['Cửa sổ đóng, không tải file, không có thông báo', 'Bảng báo cáo giữ nguyên bộ lọc và trang đang xem']),
        C('Xuất lấy tất cả các trang, không chỉ trang đang xem', 'P0', nhieu,
          ['1. ' + loc + ', để 10 dòng mỗi trang, đứng ở trang 1', '2. Bấm Xuất Excel > "Xuất file"', '3. Đếm số ' + m['dv'] + ' trong file'], '',
          ['File có đủ N ' + m['dv'] + ' (bằng N ở chân bảng), không phải 10 ' + m['dv'] + ' của trang đang xem']),
        C('Xuất theo từ khóa tìm nhanh', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. ' + loc, '2. Gõ từ khóa ở ô tìm nhanh, nhấn Enter, ghi nhận số dòng trên màn', '3. Bấm Xuất Excel > "Xuất file", mở file'],
          'Từ khóa: ' + m['tu_khoa'],
          ['File chỉ chứa đúng các ' + m['dv'] + ' khớp từ khóa như trên màn', 'Dòng Tổng cộng trong file bằng dòng Tổng cộng trên màn']),
        C('Xuất khi danh sách không có dòng nào', 'P2', 'Đã chọn bộ lọc, ô tìm nhanh gõ chuỗi không tồn tại, bảng hiện "Không có dữ liệu phù hợp bộ lọc."',
          ['1. Bấm Xuất Excel > "Xuất file"', '2. Mở file'], 'Từ khóa: zzzz',
          ['Không báo lỗi, vẫn tải file', 'File có tiêu đề báo cáo, dòng thời gian, hàng tên cột; không có dòng dữ liệu nào ngoài dòng Tổng cộng (nếu có)']),
        C('Tên file và định dạng file', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. Bấm Xuất Excel > "Xuất file"', '2. Xem tên file tải về', '3. Mở file bằng Excel'], '',
          ['Thông báo "Xuất Excel thành công"', 'Tên file "' + f + '"',
           'File mở được bình thường bằng Excel, không báo file hỏng / sai định dạng']),
        C('Tiêu đề cột và thứ tự cột trong file', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.',
          ['1. Xuất file với đủ trường mặc định', '2. So hàng tiêu đề trong file với tiêu đề bảng trên màn'], '',
          ['Cột STT đứng đầu, các cột tiếp theo đúng thứ tự trường trong cửa sổ chọn trường',
           'Tên cột viết đúng như trên màn, tiêu đề 2 tầng giữ đúng nhóm như trên màn']),
        C('Định dạng số và tiếng Việt trong file', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu có số âm và tên khách hàng tiếng Việt có dấu.',
          ['1. Xuất file', '2. Bấm vào 1 ô số tiền, xem thanh công thức', '3. Chọn cả cột số tiền, xem tổng ở thanh trạng thái Excel', '4. Đọc cột tên khách hàng / diễn giải'], '',
          ['Ô số tiền là kiểu SỐ (Excel cộng được, không có cảnh báo "số lưu dạng chữ"), hiển thị 1,234,567, không phần lẻ, số âm có dấu "-"',
           m.get('xl_ngay', 'Ngày hiển thị dạng dd/mm/yyyy'),
           'Tiếng Việt có dấu và ký tự đặc biệt (&, /, -, ngoặc) hiển thị đúng, không lỗi phông']),
    ]


# ---------------------------------------------------------------- PHÂN QUYỀN CHUNG (checklist 296, 298, 299)
def pq_chung(m):
    return [
        C('Không có quyền thì ẩn các ô lọc tổ chức', 'P0', 'Tài khoản không có quyền nào trong nhóm "' + m['nhom_quyen'] + '".',
          ['1. Đăng nhập tài khoản đó', '2. ' + m['menu'], '3. Quan sát khu vực lọc và các nút'], '',
          ['Màn vẫn mở được, không báo thiếu quyền',
           'KHÔNG có ô Công ty, Phòng ban, Bộ phận, Nhân viên',
           'Các nút ' + m['nut'] + ' vẫn hiện và dùng được (màn không có nút nào cần quyền riêng)']),
        C('Mở màn bằng đường dẫn trực tiếp khi không có quyền', 'P1', 'Tài khoản không có quyền nào trong nhóm "' + m['nhom_quyen'] + '"; biết đường dẫn của màn.',
          ['1. Đăng nhập tài khoản đó', '2. Dán đường dẫn màn vào thanh địa chỉ, nhấn Enter', '3. ' + m['loc']], 'Đường dẫn: ' + m['url'],
          ['Màn mở bình thường như khi vào từ menu, không bị chặn',
           'Chỉ thấy các hợp đồng do chính tài khoản đó tạo; không có ô lọc tổ chức']),
        C('Đổi quyền trong lúc đang xem báo cáo', 'P1', 'Tài khoản X có quyền "' + m['quyen_rong'] + '", đang mở màn và đã lọc có số liệu.',
          ['1. Ghi lại dòng Tổng cộng', '2. Người quản trị gỡ quyền đó của X', '3. Ở màn đang mở, bấm Tìm kiếm', '4. Nhấn F5, chọn lại bộ lọc như cũ'], '',
          ['Bước 3: số liệu thu hẹp ngay về phạm vi mới (chỉ hợp đồng X tạo), dòng Tổng cộng giảm theo',
           'Bước 4: các ô lọc tổ chức biến mất; số liệu như bước 3',
           'Không lúc nào hiện số liệu ngoài phạm vi quyền mới']),
    ]
