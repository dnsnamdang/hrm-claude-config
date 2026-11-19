# -*- coding: utf-8 -*-
"""Bộ case DÙNG CHUNG cho màn PHIẾU (danh sách V2) theo khuôn tab "13. DM quốc gia" + checklist "Mẫu tài liệu.xlsx".

Sinh các case lặp lại giữa các màn phiếu (hiển thị, phân trang, sắp xếp, tìm kiếm, lưu trạng thái lọc, tùy chỉnh cột,
xuất Excel, lịch sử, đóng form chưa lưu…) từ 1 cấu hình K; case nghiệp vụ riêng viết ở gen_testcase.py của từng màn.
Bản sao giống hệt nằm ở docs/ của: phieu-nhap-kho, finance-product-transfer, buy-service-request (sửa thì sửa cả 3).

Case = (Chức năng, Priority, Tiền điều kiện, Bước, Test data, Expected) — số TC đánh tự động theo thứ tự trong nhóm.
"""

THAY = [('→', '>'), ('−', '-'), ('⋮', 'ba chấm'), ('☰', 'biểu tượng kéo thả'), ('≤', 'không quá'), ('≥', 'từ')]


def _sach(s):
    for a, b in THAY:
        s = s.replace(a, b)
    return s


def _j(x):
    return _sach(x if isinstance(x, str) else '\n'.join(x))


def _exp(x):
    lines = [x] if isinstance(x, str) else list(x)
    out = []
    for ln in lines:
        ln = ln.strip()
        if ln.startswith('- '):
            ln = ln[2:].strip()
        elif ln.startswith('-'):
            ln = ln[1:].strip()
        out.append('-  ' + ln)
    return _sach('\n'.join(out))


def C(func, prio, pre, steps, data, exp):
    assert prio in ('P0', 'P1', 'P2'), func
    return (_sach(func), prio, _j(pre), _j(steps), _j(data or ''), _exp(exp))


def danh_so(cases):
    return [('%03d' % i,) + c for i, c in enumerate(cases, 1)]


def q(s):
    return '"%s"' % s


# ============================================================ I. HIỂN THỊ TRANG & TRUY CẬP
def hien_thi(K):
    menu = K['menu']
    out = [
        C('Mở màn hình từ menu', 'P0', K.get('pre_mo', 'Tài khoản đã đăng nhập, có phiếu trong phạm vi xem.'),
          ['1. Đăng nhập', '2. Vào menu ' + menu] + K.get('buoc_mo_them', []), '',
          ['Tiêu đề trang hiện ' + q(K['tieu_de']),
           'Bảng tự tải dữ liệu, không cần bấm Tìm kiếm',
           'Mặc định hiển thị 10 dòng/trang; ô số dòng/trang ở góc dưới bên phải bảng cho chọn 5 / 10 / 20 / 50 / 100',
           'Chưa bấm sắp xếp cột nào: phiếu tạo MỚI NHẤT nằm trên cùng',
           'Góc dưới bên trái bảng hiện dòng tổng dạng "Hiển thị 1–10 / N", N là tổng số phiếu trong phạm vi xem']
          + K.get('exp_mo_them', [])),
        C('Các nút chức năng trên thanh công cụ', 'P0', K.get('pre_nut', 'Tài khoản đã đăng nhập.'),
          ['1. Mở màn hình', '2. Quan sát thanh công cụ phía trên bảng và khối tìm kiếm'], '',
          K['exp_nut']),
        C('Kiểm tra đủ các cột mặc định của bảng', 'P0', 'Tài khoản chưa từng tùy chỉnh cột của màn này.',
          ['1. Mở màn hình', '2. Đọc tên từng tiêu đề cột từ trái sang phải'], '',
          ['Có đủ các cột theo đúng thứ tự: ' + ', '.join(K['cot'])]
          + (['Các cột ' + ', '.join(K['cot_an']) + ' KHÔNG xuất hiện (mặc định ẩn)'] if K.get('cot_an') else
             ['Không có cột nào bị ẩn mặc định'])
          + K.get('exp_cot_them', [])),
    ]
    if K.get('cot_an'):
        out.append(C('Các cột mặc định ẩn bật lên được', 'P1', 'Tài khoản chưa từng tùy chỉnh cột.',
                     ['1. Bấm nút Cấu hình cột hiển thị', '2. Quan sát các cột chưa tích'], '',
                     ['Các cột ' + ', '.join(K['cot_an']) + ' có trong danh sách nhưng chưa được tích',
                      'Tích các cột này rồi bấm Lưu thì bảng hiện thêm đúng các cột đó']))
    out += [
        C('Dữ liệu trên bảng khớp với phiếu đã lập', 'P0', K['pre_du_lieu'],
          ['1. Mở màn hình, tìm phiếu vừa lập', '2. So từng cột với dữ liệu đã nhập lúc lập phiếu và trang Chi tiết'], '',
          K['exp_du_lieu'] + ['Ngày giờ hiện dạng dd/mm/yyyy hh:mm', 'Ô không có dữ liệu để TRỐNG, không in dấu "-"']),
        C('Nhãn trạng thái phân biệt theo màu', 'P0', 'Có phiếu ở mỗi trạng thái.',
          ['1. Lọc lần lượt từng trạng thái ở ô Trạng thái', '2. Quan sát cột Trạng thái'], '',
          ['Nhãn hiện đúng chữ và màu: ' + '; '.join('%s (%s)' % (a, b) for a, b in K['trang_thai'])]
          + K.get('exp_trang_thai_them', [])),
        C('Danh sách khi chưa có phiếu nào trong phạm vi xem', 'P2', K.get('pre_rong', 'Tài khoản chưa lập phiếu nào và không có quyền xem phiếu của người khác.'),
          ['1. Đăng nhập tài khoản ở tiền điều kiện', '2. Vào menu ' + menu], '',
          ['Bảng hiện dòng ' + q(K['rong_bang']),
           (('Dòng tổng dưới bảng hiện ' + q(K['rong_chan'])) if K.get('rong_chan') else 'Không hiện dòng tổng "Hiển thị …" dưới bảng'),
           'Màn hình không báo lỗi; các nút trên thanh công cụ vẫn dùng được']),
        C('Hiển thị khi không có dữ liệu khớp tìm kiếm', 'P1', 'Danh sách có dữ liệu.',
          ['1. Gõ vào ô tìm kiếm một chuỗi chắc chắn không tồn tại', '2. Nhấn Enter hoặc bấm Tìm kiếm'], 'Từ khóa: zzzkhongtontai999',
          ['Bảng hiện ' + q(K['rong_bang'])]
          + (['Dòng tổng hiện ' + q(K['rong_chan'])] if K.get('rong_chan') else [])),
        C('Số thứ tự liên tục qua các trang', 'P0', 'Có nhiều hơn 1 trang dữ liệu.',
          ['1. Ghi lại STT dòng cuối trang 1', '2. Sang trang 2, đọc STT dòng đầu'], '',
          ['STT trang 2 bắt đầu từ 11 (nối tiếp trang 1), không quay về 1']),
        C('Đổi số dòng mỗi trang', 'P1', 'Đang ở trang 2, số dòng mặc định 10.',
          ['1. Đổi ô số dòng/trang sang 20', '2. Đếm số dòng trên bảng, đọc dòng tổng'], '',
          ['Bảng hiện đúng 20 dòng (hoặc ít hơn nếu không đủ dữ liệu)', 'Bảng quay về trang 1, dòng tổng "Hiển thị 1–20 / N"',
           'Bộ lọc và thứ tự sắp xếp đang áp dụng được giữ nguyên']),
        C('Nút sang trang kế tiếp và lùi về trang trước', 'P0', 'Có ít nhất 3 trang dữ liệu. Đang ở trang 1.',
          ['1. Bấm nút › (trang kế tiếp)', '2. Đọc thanh phân trang và dòng tổng', '3. Bấm nút ‹ (trang trước)', '4. Đọc lại'], '',
          ['Bước 1: chuyển sang trang 2, số trang 2 được tô đậm, dòng tổng "Hiển thị 11–20 / N"',
           'Bước 3: quay lại trang 1, dòng tổng "Hiển thị 1–10 / N"', 'Dữ liệu từng trang không lặp, không thiếu dòng']),
        C('Nút về trang cuối và về trang đầu', 'P0', 'Có N phiếu, nhiều hơn 3 trang. Đang ở trang 1.',
          ['1. Bấm nút » (về trang cuối)', '2. Đọc dòng tổng và STT dòng cuối', '3. Bấm nút « (về trang đầu)'], '',
          ['Bước 1: nhảy tới trang cuối, dòng tổng "Hiển thị …–N / N", STT dòng cuối bằng N',
           'Bước 3: quay về trang 1, dòng tổng "Hiển thị 1–10 / N"']),
        C('Nút phân trang ở trang đầu và trang cuối', 'P1', 'Có nhiều hơn 1 trang.',
          ['1. Đứng ở trang 1, quan sát nút « và ‹', '2. Về trang cuối, quan sát nút › và »'], '',
          ['Ở trang 1: nút « và ‹ bị mờ, bấm không có tác dụng', 'Ở trang cuối: nút › và » bị mờ, bấm không có tác dụng']),
        C('Tổng số bản ghi khi mở danh sách', 'P0', 'Có N phiếu trong phạm vi xem (mọi trạng thái). Chưa lọc gì.',
          ['1. Vào menu ' + menu, '2. Đọc dòng tổng ở góc dưới bên trái bảng'], 'N = tổng số phiếu trong phạm vi xem',
          ['Dòng tổng hiện "Hiển thị 1–10 / N"', 'N bằng đúng tổng số phiếu tài khoản được xem, ghi liền không có dấu phân cách hàng nghìn']
          + K.get('exp_tong_them', [])),
        C('Thứ tự mặc định khi mở màn', 'P1', 'Vừa lập phiếu X. Chưa bấm sắp xếp cột nào.',
          ['1. Vào menu ' + menu, '2. Đọc dòng đầu tiên của bảng'], 'Phiếu X',
          ['Phiếu X vừa lập nằm ở dòng đầu, STT = 1', 'Các dòng xếp theo thời điểm tạo, mới nhất ở trên']),
    ]
    for col in K['sap_xep']:
        out.append(C('Sắp xếp theo cột ' + col, 'P1', 'Có ít nhất 5 phiếu có giá trị cột %s khác nhau.' % col,
                     ['1. Bấm tiêu đề cột ' + col, '2. Đọc 5 dòng đầu', '3. Bấm tiêu đề cột lần thứ hai', '4. Đọc lại 5 dòng đầu'], '',
                     ['Lần 1: xếp TĂNG dần theo ' + col + ', tiêu đề cột hiện mũi tên lên',
                      'Lần 2: thứ tự đảo ngược (GIẢM dần), mũi tên xuống',
                      'Ô trống (nếu có) không làm lẫn thứ tự các dòng có dữ liệu']))
    out += [
        C('Các cột không cho sắp xếp', 'P2', 'Đang ở màn danh sách.',
          ['1. Bấm vào tiêu đề các cột ' + ', '.join(K['khong_sap_xep']), '2. Quan sát bảng'], '',
          ['Các cột này KHÔNG có biểu tượng mũi tên sắp xếp', 'Bấm vào tiêu đề không làm đổi thứ tự dòng',
           'Chỉ các cột ' + ', '.join(K['sap_xep']) + ' sắp xếp được']),
        C('Sắp xếp giữ nguyên khi chuyển trang', 'P1', 'Đang sắp xếp giảm dần theo cột %s, có nhiều trang.' % K['sap_xep'][0],
          ['1. Bấm sang trang 2', '2. So dòng đầu trang 2 với dòng cuối trang 1'], '',
          ['Mũi tên sắp xếp vẫn giữ ở cột ' + K['sap_xep'][0], 'Thứ tự nối tiếp liền mạch, không lặp hay mất phiếu']),
        C('Bấm sắp xếp khi đang ở trang giữa thì quay về trang 1', 'P1', 'Có nhiều hơn 3 trang. Đang ở trang 3.',
          ['1. Bấm tiêu đề cột ' + K['sap_xep'][0], '2. Quan sát thanh phân trang và dòng tổng'], '',
          ['Bảng quay về trang 1 theo thứ tự mới', 'Dòng tổng "Hiển thị 1–10 / N", N không đổi']),
        C('Thời gian tải danh sách', 'P2', 'Môi trường có nhiều phiếu (từ 1,000 phiếu trở lên).',
          ['1. Mở màn hình', '2. Chuyển trang, đổi 100 dòng/trang', '3. Bấm sắp xếp một cột'], '',
          ['Trong lúc chờ bảng có biểu tượng đang tải, không hiện dữ liệu cũ lẫn mới',
           'Mỗi thao tác tải xong, màn hình không treo, không báo lỗi']),
    ]
    return out + K.get('hien_thi_rieng', [])


# ============================================================ II. TÌM KIẾM & LỌC DANH SÁCH
def tim_kiem(K):
    ma, ex, part = K['ma'], K['vd_ma'], K['vd_mot_phan']
    menu = K['menu']
    tl, tl_dau, tl_khong_dau = K['loc_text']
    out = [
        C('Tìm nhanh theo %s đầy đủ' % ma, 'P0', 'Biết %s của 1 phiếu trong phạm vi xem.' % ma,
          ['1. Gõ %s vào ô tìm kiếm (%s)' % (ma, q(K['placeholder'])), '2. Nhấn Enter'], 'Từ khóa: ' + ex,
          ['Bảng chỉ còn phiếu có %s = %s' % (ma, ex), 'Dòng tổng "Hiển thị 1–1 / 1"']),
        C('Tìm nhanh theo một phần %s' % ma, 'P0', 'Có nhiều phiếu có %s chứa chuỗi cần tìm.' % ma,
          ['1. Gõ một phần %s vào ô tìm kiếm' % ma, '2. Bấm Tìm kiếm'], 'Từ khóa: ' + part,
          ['Chỉ còn các phiếu có %s chứa %s' % (ma, q(part)), 'Dòng tổng đổi theo số kết quả, bảng về trang 1']),
        C('Tìm kiếm không phân biệt chữ hoa chữ thường', 'P1', 'Có phiếu có %s chứa chữ cái.' % ma,
          ['1. Gõ từ khóa toàn chữ thường, nhấn Enter, ghi nhận kết quả', '2. Xóa, gõ lại toàn chữ hoa, nhấn Enter', '3. So sánh'],
          'Từ khóa: %s / %s' % (part.lower(), part.upper()),
          ['Hai lần tìm cho ra CÙNG một tập kết quả']),
        C('Tìm có dấu và không dấu ở ô ' + tl, 'P2', 'Có phiếu có %s chứa %s.' % (tl.lower(), q(tl_dau)),
          ['1. Mở Tìm kiếm nâng cao', '2. Gõ %s vào ô %s, nhấn Enter, ghi nhận kết quả' % (q(tl_dau), tl),
           '3. Xóa, gõ %s (không dấu), nhấn Enter' % q(tl_khong_dau)], 'Từ khóa: %s / %s' % (tl_dau, tl_khong_dau),
          ['Bước 2: ra các phiếu có %s chứa %s' % (tl.lower(), q(tl_dau)),
           'Bước 3: ra cùng tập kết quả với bước 2 (tìm không phân biệt dấu)', 'Không báo lỗi']),
        C('Tìm từ khóa không tồn tại', 'P1', 'Danh sách có dữ liệu.',
          ['1. Gõ từ khóa không tồn tại vào ô tìm kiếm', '2. Nhấn Enter'], 'Từ khóa: zzzkhongtontai999',
          ['Bảng hiện ' + q(K['rong_bang'])] + (['Dòng tổng hiện ' + q(K['rong_chan'])] if K.get('rong_chan') else [])),
        C('Tìm với ký tự đặc biệt', 'P2', 'Danh sách có dữ liệu.',
          ['1. Lần lượt gõ từng chuỗi ở Test data vào ô tìm kiếm', '2. Nhấn Enter sau mỗi lần'], "Chuỗi: %  /  _  /  '  /  <script>",
          ['Màn hình không báo lỗi hệ thống, không treo',
           'Bảng chỉ hiện phiếu có %s chứa đúng chuỗi đã gõ; không có thì hiện %s' % (ma, q(K['rong_bang'])),
           'Chuỗi <script> hiện nguyên văn trong ô, không chạy']),
        C('Từ khóa có khoảng trắng đầu và cuối', 'P2', 'Biết %s của 1 phiếu.' % ma,
          ['1. Gõ 2 dấu cách + %s + 2 dấu cách vào ô tìm kiếm' % ma, '2. Nhấn Enter'], 'Từ khóa: "  %s  "' % ex,
          ['Hệ thống bỏ khoảng trắng đầu và cuối, kết quả giống khi gõ ' + q(ex)]),
        C('Ô tìm kiếm chỉ có khoảng trắng', 'P2', 'Danh sách có N phiếu.',
          ['1. Gõ toàn dấu cách vào ô tìm kiếm', '2. Nhấn Enter'], 'Từ khóa: "     "',
          ['Coi như không có từ khóa: bảng hiện đủ N phiếu', 'Không báo lỗi']),
        C('Giới hạn độ dài ô tìm kiếm', 'P2', 'Đang ở màn danh sách.',
          ['1. Dán chuỗi Test data vào ô tìm kiếm', '2. Kiểm tra chuỗi trong ô có bị cắt không', '3. Nhấn Enter', '4. Bấm Làm mới'],
          'Chuỗi 500 ký tự (chữ "abcde" lặp 100 lần)',
          ['Bước 2: ô nhận đủ chuỗi, không có thông báo lỗi',
           'Bước 3: bảng hiện %s; màn hình không treo, không báo lỗi hệ thống' % q(K['rong_bang']),
           'Bước 4: ô tìm kiếm trống, bảng về toàn bộ danh sách']),
        C('Xóa từ khóa thì danh sách quay về đầy đủ', 'P0', 'Đang tìm với từ khóa ra ít kết quả.',
          ['1. Xóa hết nội dung ô tìm kiếm', '2. Nhấn Enter'], '',
          ['Dòng tổng quay lại như ban đầu', 'Bảng về trang 1']),
        C('Chỉ lọc khi nhấn Enter hoặc bấm Tìm kiếm', 'P0', 'Đang ở màn danh sách.',
          ['1. Gõ từ khóa vào ô tìm kiếm, chưa nhấn gì', '2. Quan sát bảng', '3. Nhấn Enter', '4. Gõ từ khóa khác, bấm nút Tìm kiếm'],
          'Từ khóa: ' + part,
          ['Bước 2: bảng CHƯA đổi', 'Bước 3: bảng lọc theo từ khóa', 'Bước 4: bảng lọc theo từ khóa mới']),
        C('Mở và đóng khu vực Tìm kiếm nâng cao', 'P1', 'Khu vực ô lọc đang thu gọn.',
          ['1. Bấm "Tìm kiếm nâng cao"', '2. Bấm lại nút'], '',
          ['Bước 1: hiện các ô lọc: ' + ', '.join(K['loc_list']) + '; nút đổi chữ thành "Ẩn tìm kiếm nâng cao"',
           'Bước 2: khu vực ô lọc thu gọn, giá trị đang lọc vẫn giữ']),
        C('Giá trị mặc định của bộ lọc', 'P1', 'Vào màn lần đầu trong ngày (chưa có bộ lọc ghi nhớ).',
          ['1. Vào menu ' + menu, '2. Mở Tìm kiếm nâng cao, đọc từng ô lọc'], '',
          ['Ô tìm kiếm và mọi ô lọc để trống', 'Danh sách hiện mọi trạng thái trong phạm vi xem'] + K.get('exp_mac_dinh_them', [])),
    ]
    out += K['loc_rieng']
    c1, v1 = K['loc_chon']
    out += [
        C('Lọc kết hợp nhiều tiêu chí', 'P0', 'Có phiếu thỏa đồng thời các điều kiện.',
          ['1. Mở Tìm kiếm nâng cao', '2. Chọn ' + K['loc_ket_hop']], '',
          ['Mỗi lần chọn ở ô chọn bảng lọc lại ngay', 'Kết quả thỏa ĐỒNG THỜI mọi điều kiện đã chọn']),
        C('Kết hợp từ khóa tìm nhanh với ô lọc', 'P1', 'Có phiếu khớp từ khóa ở nhiều trạng thái.',
          ['1. Gõ từ khóa vào ô tìm kiếm, nhấn Enter', '2. Chọn %s = %s' % (c1, v1)], 'Từ khóa: %s; %s: %s' % (part, c1, v1),
          ['Bước 2: chỉ còn phiếu vừa chứa từ khóa vừa có %s = %s' % (c1, v1), 'Từ khóa ở ô tìm kiếm vẫn giữ']),
        C('Lọc ra kết quả rỗng', 'P1', 'Chọn tổ hợp điều kiện chắc chắn không có phiếu nào thỏa.',
          ['1. Chọn tổ hợp đó', '2. Quan sát bảng'], K.get('td_rong', ''),
          ['Bảng hiện ' + q(K['rong_bang'])] + (['Dòng tổng hiện ' + q(K['rong_chan'])] if K.get('rong_chan') else [])),
        C('Tổng số bản ghi sau khi lọc', 'P0', 'Biết trước có M phiếu %s = %s trong phạm vi xem.' % (c1, v1),
          ['1. Chọn %s = %s' % (c1, v1), '2. Đọc dòng tổng', '3. Đếm tổng số dòng qua các trang'], '%s: %s' % (c1, v1),
          ['Dòng tổng hiện "Hiển thị 1–… / M"', 'Tổng số dòng đếm được qua các trang đúng bằng M']),
        C('Áp dụng bộ lọc khi đang ở trang giữa', 'P0', 'Đang ở trang 3 của danh sách đầy đủ.',
          ['1. Chọn %s = %s' % (c1, v1), '2. Quan sát thanh phân trang'], '',
          ['Bảng quay về trang 1 của kết quả lọc']),
        C('Phân trang trên kết quả lọc', 'P1', 'Kết quả lọc có hơn 10 phiếu.',
          ['1. Chọn %s = %s' % (c1, v1), '2. Sang trang 2', '3. Kiểm tra cột %s các dòng' % c1], '',
          ['Trang 2 vẫn chỉ gồm phiếu thỏa điều kiện lọc, STT nối tiếp 11, 12…', 'Dòng tổng giữ đúng tổng số kết quả lọc']),
        C('Sắp xếp trên kết quả lọc', 'P1', 'Đang lọc %s = %s, kết quả nhiều trang.' % (c1, v1),
          ['1. Bấm tiêu đề cột ' + K['sap_xep'][0], '2. Kiểm tra các dòng'], '',
          ['Bảng sắp xếp lại nhưng vẫn chỉ gồm phiếu thỏa điều kiện lọc', 'Dòng tổng không đổi']),
        C('Nút Làm mới xóa hết tiêu chí và tải lại', 'P0', 'Đang có từ khóa tìm nhanh và nhiều ô lọc.',
          ['1. Bấm nút Làm mới', '2. Quan sát các ô lọc và bảng'], '',
          ['Ô tìm kiếm và mọi ô lọc trở về rỗng', 'Bảng tải lại ngay danh sách đầy đủ, về trang 1',
           'Dòng tổng quay về tổng số ban đầu']),
        C('Cài đặt bộ lọc: ẩn ô lọc và đổi thứ tự', 'P2', 'Đang ở màn danh sách.',
          ['1. Bấm "Cài đặt bộ lọc"', '2. Bỏ tích 1 ô lọc, kéo ô %s lên đầu' % c1, '3. Bấm Lưu', '4. Tải lại trang (F5)'], '',
          ['Cửa sổ liệt kê đủ %d ô lọc: %s' % (len(K['loc_list']), ', '.join(K['loc_list'])),
           'Sau Lưu: khu vực lọc bỏ ô đã bỏ tích, ô %s đứng đầu' % c1, 'Sau F5 cấu hình vẫn giữ (lưu theo tài khoản)']),
        C('Cài đặt bộ lọc: Khôi phục mặc định và Đóng không lưu', 'P2', 'Đã đổi cấu hình bộ lọc ở case trước.',
          ['1. Bấm "Cài đặt bộ lọc", đổi tiếp vài ô, bấm Đóng', '2. Mở lại, bấm "Khôi phục mặc định", Lưu'], '',
          ['Bước 1: khu vực lọc không đổi (Đóng không lưu)', 'Bước 2: khu vực lọc trở về đủ ô, đúng thứ tự mặc định']),
        C('Mở chi tiết phiếu rồi quay lại trong 10 phút thì giữ bộ lọc', 'P1', 'Đang ở màn danh sách.',
          ['1. Gõ từ khóa, chọn %s = %s' % (c1, v1), '2. Bấm %s 1 phiếu để mở trang Chi tiết' % ma,
           '3. Bấm Quay lại (trong vòng 10 phút)'], 'Từ khóa: %s; %s: %s' % (part, c1, v1),
          ['Từ khóa và giá trị lọc vẫn giữ nguyên', 'Bảng hiện đúng kết quả lọc như trước khi mở chi tiết']),
        C('Quay lại sau hơn 10 phút thì bộ lọc về mặc định', 'P2', 'Đang lọc như case trước.',
          ['1. Mở trang Chi tiết 1 phiếu', '2. Chờ hơn 10 phút', '3. Quay lại danh sách'], '',
          ['Ô tìm kiếm và ô lọc trở về rỗng, bảng hiện danh sách đầy đủ ở trang 1']),
        C('Rời sang màn khác qua menu rồi quay lại thì bộ lọc về mặc định', 'P1', 'Đang lọc %s = %s.' % (c1, v1),
          ['1. Vào một màn khác trên menu', '2. Quay lại bằng menu ' + menu], '',
          ['Ô tìm kiếm và các ô lọc trở về rỗng', 'Bảng hiện toàn bộ danh sách ở trang 1']),
        C('Tải lại trang (F5) khi đang lọc', 'P2', 'Đang lọc %s = %s, chưa mở trang chi tiết nào.' % (c1, v1),
          ['1. Nhấn F5', '2. Quan sát khối tìm kiếm và bảng'], '',
          ['Ô tìm kiếm và các ô lọc trở về rỗng', 'Bảng hiện toàn bộ danh sách ở trang 1, 10 dòng/trang']),
        C('Mở màn ở tab trình duyệt mới khi tab cũ đang lọc', 'P2', 'Tab 1 đang lọc %s = %s.' % (c1, v1),
          ['1. Mở tab mới, vào menu ' + menu, '2. Quan sát tab 2', '3. Quay lại tab 1'], '',
          ['Tab 2: ô lọc rỗng, bảng hiện toàn bộ danh sách', 'Tab 1: vẫn giữ nguyên giá trị lọc và kết quả đang xem']),
        C('Đăng xuất, đăng nhập tài khoản khác trên cùng trình duyệt', 'P1', 'Có 2 tài khoản A và B, dùng chung trình duyệt.',
          ['1. Tài khoản A vào màn, lọc %s = %s' % (c1, v1), '2. Đăng xuất', '3. Tài khoản B đăng nhập, vào màn'], '',
          ['Tài khoản B thấy ô lọc rỗng, bảng hiện danh sách theo phạm vi xem của B',
           'Giá trị lọc của A KHÔNG hiện sang B']),
    ]
    return out


# ============================================================ THÊM MỚI — đóng form, bấm lặp, đồng thời
def them_moi_dong_form(K):
    f, nut = K['form_tao'], K['nut_quay_lai']
    return [
        C('Bấm %s khi chưa nhập thông tin nào' % nut, 'P0', 'Đang ở trang %s, chưa nhập gì.' % q(f),
          ['1. Bấm ' + nut], '', ['Về màn danh sách ngay, không hỏi', 'Không có phiếu mới nào được tạo']),
        C('Bấm %s khi đã nhập thông tin' % nut, 'P0', 'Đang ở trang %s.' % q(f),
          ['1. Nhập ' + K['truong_nhap_thu'], '2. Bấm ' + nut], K.get('td_nhap_thu', ''),
          ['Hiện hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với 2 nút Thoát, Ở lại']),
        C('Bấm Thoát ở hộp "Thông tin chưa lưu"', 'P1', 'Đang hiện hộp "Thông tin chưa lưu" ở trang tạo.',
          ['1. Bấm Thoát'], '', ['Về màn danh sách', 'Không có phiếu mới nào được tạo']),
        C('Bấm Ở lại ở hộp "Thông tin chưa lưu"', 'P1', 'Đang hiện hộp "Thông tin chưa lưu" ở trang tạo.',
          ['1. Bấm Ở lại'], '', ['Hộp đóng, vẫn ở trang tạo', 'Dữ liệu đã nhập còn nguyên']),
        C('Nhập rồi xóa hết về như ban đầu, bấm %s thì không hỏi' % nut, 'P2', 'Đang ở trang tạo, chưa nhập gì.',
          ['1. Nhập ' + K['truong_nhap_thu'], '2. Xóa hết về trống như lúc mở', '3. Bấm ' + nut], '',
          ['Về màn danh sách ngay, KHÔNG hiện hộp "Thông tin chưa lưu"']),
        C('Rời trang bằng menu hoặc nút quay lại của trình duyệt khi đã nhập', 'P1', 'Đang ở trang tạo, đã nhập dữ liệu.',
          ['1. Bấm một mục menu khác (hoặc nút Back của trình duyệt)'], '',
          ['Hiện hộp "Thông tin chưa lưu"', 'Ở lại: giữ nguyên form; Thoát: rời trang, không lưu']),
        C('Để nguyên form đã nhập đủ mà không bấm lưu thì không ghi gì', 'P1', 'Đang ở trang tạo, đã nhập đủ dữ liệu hợp lệ.',
          ['1. Không bấm nút lưu nào, để nguyên màn hình khoảng 15 phút', '2. Mở tab khác xem danh sách'], '',
          ['Danh sách KHÔNG có phiếu mới', 'Quay lại tab cũ dữ liệu trên form vẫn còn, bấm lưu thì lưu bình thường (nếu phiên đăng nhập còn hiệu lực)']),
        C('Bấm nút lưu hai lần liên tục', 'P0', 'Đang ở trang tạo, đã nhập đủ dữ liệu hợp lệ.',
          ['1. Bấm %s 2 lần thật nhanh' % K['nut_luu_chinh']], '',
          ['Nút bị khóa ngay sau lần bấm đầu cho tới khi có kết quả', 'Chỉ tạo ĐÚNG 1 phiếu, không sinh phiếu trùng']),
        C('Hai người cùng lưu phiếu mới gần như đồng thời', 'P1', 'Tài khoản A và B cùng mở trang tạo ở 2 trình duyệt.',
          ['1. A và B nhập dữ liệu hợp lệ', '2. Cùng bấm %s gần như đồng thời' % K['nut_luu_chinh']], '',
          ['Cả 2 lưu thành công, 2 phiếu có %s KHÁC nhau, không báo lỗi' % K['ma']] + K.get('exp_dong_thoi_them', [])),
    ]


# ============================================================ LỊCH SỬ THAY ĐỔI
def lich_su(K):
    t = K['lich_su_title']
    nut = K['nut_lich_su']
    return [
        C('Mở cửa sổ Lịch sử từ danh sách', 'P0', 'Có phiếu đã qua vài thao tác.',
          ['1. Ở dòng phiếu, bấm %s (nút ba chấm "Hành động khác" nếu không hiện ngoài)' % nut], '',
          ['Mở cửa sổ ' + q(t), 'Có nút Bộ lọc và danh sách các mốc lịch sử', 'Danh sách phía sau không đổi']),
        C('Mở ô bộ lọc lịch sử', 'P0', 'Đang mở cửa sổ Lịch sử.',
          ['1. Bấm nút Bộ lọc'], '',
          ['Hiện 4 ô: Loại hành động, Người thực hiện, Từ ngày, Đến ngày và nút Làm mới', 'Không có nút Tìm kiếm: chọn giá trị là lọc luôn']),
        C('Lọc lịch sử theo Loại hành động', 'P0', 'Phiếu có cả mốc Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.',
          ['1. Mở Bộ lọc', '2. Chọn Loại hành động = Thay đổi trạng thái'], '',
          ['Chỉ còn các mốc Thay đổi trạng thái']),
        C('Lọc lịch sử theo Người thực hiện', 'P0', 'Phiếu có mốc do ít nhất 2 người thực hiện.',
          ['1. Mở Bộ lọc', '2. Chọn 1 người ở ô Người thực hiện'], '',
          ['Chỉ còn các mốc do người đó thực hiện']),
        C('Lọc lịch sử theo khoảng thời gian', 'P0', 'Phiếu có mốc ở nhiều ngày khác nhau.',
          ['1. Mở Bộ lọc', '2. Chọn Từ ngày, Đến ngày bao 1 ngày có mốc'], '',
          ['Chỉ còn các mốc trong khoảng ngày đã chọn, tính cả 2 ngày đầu mút']),
        C('Lọc lịch sử kết hợp và không có kết quả', 'P1', 'Đang mở Bộ lọc.',
          ['1. Chọn Loại hành động và Người thực hiện không khớp mốc nào'], '',
          ['Hiện "Không có lịch sử phù hợp bộ lọc."']),
        C('Nút Làm mới bộ lọc lịch sử', 'P1', 'Đang lọc lịch sử theo vài điều kiện.',
          ['1. Bấm Làm mới trong khu bộ lọc'], '', ['Các ô lọc về trống, hiện lại đủ các mốc']),
        C('Đóng ô bộ lọc lịch sử', 'P2', 'Đang mở Bộ lọc.',
          ['1. Bấm lại nút Bộ lọc'], '', ['Khu bộ lọc thu gọn']),
        C('Thứ tự mốc mới nhất ở trên cùng', 'P0', 'Phiếu có từ 3 mốc trở lên.',
          ['1. Mở cửa sổ Lịch sử', '2. Đọc thời điểm các mốc từ trên xuống'], '',
          ['Mốc mới nhất nằm trên cùng, thời điểm giảm dần xuống dưới', 'Mốc Tạo mới nằm dưới cùng']),
        C('Mỗi mốc nêu đủ thông tin', 'P0', 'Phiếu đã được sửa ít nhất 1 lần.',
          ['1. Mở cửa sổ Lịch sử', '2. Đọc 1 mốc Thay đổi thông tin'], '',
          ['Có thời điểm dd/mm/yyyy hh:mm, tên hành động', 'Có dòng "Người thực hiện: <họ tên> — <phòng ban>"',
           'Mỗi trường đổi ghi giá trị cũ (đỏ) > giá trị mới (xanh)']),
        C('Đóng cửa sổ Lịch sử', 'P2', 'Đang mở cửa sổ Lịch sử, danh sách đang lọc và ở trang 2.',
          ['1. Bấm Đóng (hoặc dấu x)'], '', ['Cửa sổ đóng', 'Danh sách giữ nguyên bộ lọc, trang đang xem']),
        C('Khối Lịch sử ở trang Chi tiết giống cửa sổ ở danh sách', 'P1', 'Phiếu có vài mốc lịch sử.',
          ['1. Mở trang Chi tiết phiếu', '2. Mở khối Lịch sử cuối trang', '3. So với cửa sổ Lịch sử mở từ danh sách'], '',
          ['Cùng các mốc, cùng thứ tự, cùng nội dung và bộ lọc']),
    ] + K['lich_su_rieng']


# ============================================================ TÙY CHỈNH CỘT
def tuy_chinh_cot(K):
    n = K['tong_cot']
    khoa = ', '.join(K['cot_khoa'])
    so_hien = len(K['cot'])
    them = K['cot_an'][0] if K.get('cot_an') else None
    bo = K['cot_bo_thu']
    return [
        C('Mở cửa sổ Tùy chỉnh cột', 'P0', 'Đang ở màn danh sách, chưa từng tùy chỉnh cột.',
          ['1. Bấm biểu tượng Cấu hình cột hiển thị trên thanh công cụ'], '',
          ['Mở cửa sổ tùy chỉnh cột liệt kê đủ %d cột' % n, 'Dòng đếm "Đang chọn %d/%d cột"' % (so_hien, n),
           'Có nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng']),
        C('Cột đang hiện được tích sẵn', 'P1', 'Đang mở cửa sổ Tùy chỉnh cột.',
          ['1. Đối chiếu danh sách cột đã tích với bảng'], '',
          ['Các cột đang hiện trên bảng được tích sẵn' + ((', các cột ' + ', '.join(K['cot_an']) + ' chưa tích') if K.get('cot_an') else '')]),
    ] + ([C('Bật cột đang ẩn', 'P0', 'Đang mở cửa sổ Tùy chỉnh cột.',
            ['1. Tích cột ' + them, '2. Bấm Lưu'], '',
            ['Bảng hiện thêm cột ' + them + ' với dữ liệu đúng từng phiếu', 'Dòng đếm tăng 1'])] if them else []) + [
        C('Tắt một cột tùy chọn', 'P1', 'Đang mở cửa sổ Tùy chỉnh cột.',
          ['1. Bỏ tích cột ' + bo, '2. Bấm Lưu'], '', ['Bảng không còn cột ' + bo, 'Các cột khác giữ nguyên dữ liệu']),
        C('Cột bắt buộc không tắt được', 'P0', 'Đang mở cửa sổ Tùy chỉnh cột.',
          ['1. Bấm vào ô tích của các cột ' + khoa, '2. Bấm Bỏ chọn hết'], '',
          ['Các cột %s có biểu tượng khóa, luôn được tích, không bỏ được' % khoa,
           'Bỏ chọn hết chỉ bỏ các cột không khóa']),
        C('Kéo thả đổi thứ tự cột', 'P1', 'Đang mở cửa sổ Tùy chỉnh cột.',
          ['1. Kéo cột Trạng thái lên ngay sau cột ' + K['cot'][1], '2. Bấm Lưu'], '',
          ['Bảng hiện cột Trạng thái ngay sau cột ' + K['cot'][1], 'Dữ liệu từng cột vẫn đúng']),
        C('Cột bắt buộc không kéo đổi vị trí được', 'P2', 'Đang mở cửa sổ Tùy chỉnh cột.',
          ['1. Thử kéo cột STT (hoặc Hành động) sang vị trí khác'], '',
          ['Cột khóa đứng yên, không đổi vị trí']),
        C('Đóng cửa sổ mà không lưu thì không áp dụng thay đổi', 'P1', 'Đang mở cửa sổ Tùy chỉnh cột.',
          ['1. Bỏ tích vài cột, đổi thứ tự', '2. Bấm Đóng (hoặc dấu x)'], '',
          ['Bảng giữ nguyên bộ cột và thứ tự như trước khi mở cửa sổ']),
        C('Cấu hình cột được ghi nhớ sau khi tải lại trang', 'P0', 'Đã tắt cột %s và lưu.' % bo,
          ['1. Nhấn F5', '2. Đăng xuất rồi đăng nhập lại, vào màn'], '',
          ['Cả 2 lần: bảng vẫn không có cột ' + bo]),
        C('Cấu hình cột lưu riêng theo từng tài khoản', 'P2', 'Tài khoản A đã tắt cột %s.' % bo,
          ['1. Đăng nhập tài khoản B (chưa tùy chỉnh), vào màn'], '',
          ['Tài khoản B vẫn thấy đủ bộ cột mặc định']),
        C('Tùy chỉnh cột không ảnh hưởng dữ liệu và bộ lọc', 'P1', 'Đang lọc %s = %s, đang ở trang 2.' % K['loc_chon'],
          ['1. Mở Tùy chỉnh cột, tắt 1 cột, Lưu', '2. Quan sát bảng'], '',
          ['Bộ lọc giữ nguyên, số dòng tổng không đổi', 'Chỉ đổi cột hiển thị, dữ liệu các cột còn lại không đổi']),
    ]


# ============================================================ XUẤT DANH SÁCH EXCEL
def xuat_excel(K):
    E = K['excel']
    n = E['so_truong']
    c1, v1 = K['loc_chon']
    return [
        C('Mở cửa sổ chọn trường xuất file', 'P0', 'Đang ở màn danh sách, chưa tùy chỉnh cột.',
          ['1. Bấm Xuất Excel'], '',
          ['Mở cửa sổ ' + q(E['title']), 'Liệt kê %d trường: %s' % (n, ', '.join(E['truong'])),
           E['mac_dinh'], 'Có nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng']),
        C('Xuất file với các trường mặc định', 'P0', 'Danh sách có dữ liệu.',
          ['1. Bấm Xuất Excel', '2. Giữ nguyên lựa chọn, bấm Xuất file', '3. Mở file tải về'], '',
          ['Báo "Xuất Excel thành công"', 'Tên file ' + E['file'] + ', định dạng .xlsx mở được bằng Excel',
           'Dòng tiêu đề ' + q(E['tieu_de']) + '; tiêu đề cột đúng tên và thứ tự các trường đã chọn'] + E.get('exp_them', [])),
        C('Chọn tất cả trường', 'P1', 'Đang mở cửa sổ chọn trường.',
          ['1. Bấm Chọn tất cả', '2. Bấm Xuất file'], '',
          ['Dòng đếm "Đang chọn %d/%d trường"' % (n, n), 'File có đủ %d cột' % n]),
        C('Bỏ tích một trường thì file không có cột đó', 'P0', 'Đang mở cửa sổ chọn trường.',
          ['1. Bỏ tích trường ' + E['bo_thu'], '2. Bấm Xuất file'], '',
          ['File không có cột ' + E['bo_thu'], 'Các cột còn lại đúng thứ tự']),
        C('Kéo thả đổi thứ tự cột trong file', 'P1', 'Đang mở cửa sổ chọn trường.',
          ['1. Kéo trường Trạng thái lên đầu danh sách', '2. Bấm Xuất file'], '',
          ['Cột Trạng thái là cột đầu tiên (sau STT nếu có) trong file']),
        C('Không chọn trường nào', 'P1', 'Đang mở cửa sổ chọn trường.',
          ['1. Bấm Bỏ chọn hết', '2. Bấm Xuất file'], '',
          ['Dòng đếm "Đang chọn 0/%d trường"' % n, 'Nút Xuất file mờ, bấm không có tác dụng, không tải file']),
        C('Xuất theo đúng bộ lọc đang áp dụng', 'P0', 'Đang lọc %s = %s, kết quả M phiếu.' % (c1, v1),
          ['1. Bấm Xuất Excel, Xuất file', '2. Đếm số dòng dữ liệu trong file'], '',
          ['File có đúng M dòng, mọi dòng có %s = %s' % (c1, v1)]),
        C('Xuất theo từ khóa tìm nhanh', 'P1', 'Đang tìm nhanh theo một phần %s.' % K['ma'],
          ['1. Bấm Xuất Excel, Xuất file'], 'Từ khóa: ' + K['vd_mot_phan'],
          ['File chỉ gồm các phiếu có %s chứa từ khóa' % K['ma']]),
        C('Xuất lấy tất cả các trang', 'P0', 'Kết quả lọc có 25 phiếu (3 trang 10 dòng). Đang ở trang 1.',
          ['1. Bấm Xuất Excel, Xuất file'], '',
          ['File có đủ 25 dòng, không chỉ 10 dòng của trang đang xem']),
        C('Xuất khi danh sách không có dòng nào', 'P2', 'Bộ lọc cho kết quả rỗng.',
          ['1. Bấm Xuất Excel, Xuất file'], '', E['rong']),
        C('Dữ liệu trong file khớp với trên màn hình', 'P0', 'Danh sách có phiếu ở nhiều trạng thái.',
          ['1. Xuất file với đủ trường', '2. So 5 dòng bất kỳ trong file với bảng trên màn'], '',
          ['Mỗi ô khớp với dữ liệu trên màn', 'Ngày giờ dạng dd/mm/yyyy hh:mm, ô rỗng để trống',
           'Tiếng Việt có dấu, ký tự đặc biệt hiện đúng, không lỗi phông']),
        C('Xuất Excel theo phạm vi xem của tài khoản', 'P1', 'Tài khoản chỉ được xem phiếu do mình lập.',
          ['1. Đăng nhập tài khoản đó', '2. Xuất Excel không lọc gì'], '',
          ['File chỉ gồm các phiếu tài khoản được xem trên danh sách']),
    ]


# ============================================================ PHÂN QUYỀN — case chung
def phan_quyen_chung(K):
    menu = K['menu']
    return [
        C('Nút thao tác bị ẨN khi không đủ quyền hoặc sai trạng thái', 'P0', K['pre_an_nut'],
          ['1. Mở danh sách và trang Chi tiết các phiếu ở tiền điều kiện', '2. Quan sát cột Hành động và chân trang'], '',
          ['Nút không dùng được thì ẨN hẳn, không có nút mờ bấm không được'] + K['exp_an_nut']),
        C('Mở đường dẫn trực tiếp phiếu ngoài phạm vi xem', 'P0', K['pre_url'],
          ['1. Dán đường dẫn trang Chi tiết của phiếu đó vào trình duyệt'], '',
          K['exp_url']),
        C('Bị đổi quyền trong lúc đang thao tác', 'P1', K['pre_doi_quyen'],
          ['1. Tài khoản A mở sẵn ' + K['man_doi_quyen'], '2. Quản trị bỏ quyền của A ở màn Phân quyền', '3. A bấm ' + K['nut_doi_quyen']],
          '', K['exp_doi_quyen']),
        C('Phạm vi áp như nhau cho danh sách, chi tiết, in, xuất Excel, lịch sử', 'P1', 'Tài khoản chỉ có phạm vi hẹp (vd chỉ phiếu mình lập).',
          ['1. Vào menu ' + menu, '2. Xuất Excel, In danh sách (nếu có), mở Lịch sử, In phiếu từng phiếu'], '',
          ['Mọi nơi chỉ gồm phiếu trong phạm vi xem, không lộ phiếu ngoài phạm vi']),
    ]
