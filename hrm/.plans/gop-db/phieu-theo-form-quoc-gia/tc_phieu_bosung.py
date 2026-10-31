# -*- coding: utf-8 -*-
"""Bổ sung testcase màn PHIẾU theo chuẩn mẫu Danh mục quốc gia + 8 ý góp ý tester 07/10/2026.

Dùng trong gen_testcase.py của từng màn (sau khi khai S1, S2…, trước build()):

    from tc_phieu_bosung import ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases, \
        weird_param_case, add_advanced_step, fill_pre, check_no_dash_pre

Các ý tester (srs-tc-feedback-0710/tc/BRIEF_TC.md):
  1 Lưu và tiếp tục khi có dữ liệu lỗi            → viết riêng từng màn (hành vi nháp mỗi màn khác nhau)
  2 Ô chọn cha–con (Công ty → Phòng ban → Bộ phận) → org_cases()
  3 Expected case mở màn: số dòng/trang, lựa chọn, thứ tự, khuôn dòng tổng → open_menu_case()
  4 Case lọc ô nằm trong "Tìm kiếm nâng cao" phải có bước bấm nút đó     → add_advanced_step()
  5 Nhớ bộ lọc: trước/sau 10 phút, sang màn khác, đổi tài khoản, tab mới  → filter_memory_cases()
  6 Kết hợp tiêu chí + độ dài ô tìm nhanh          → combo_cases()
Hành vi lấy từ code chung (đọc 30/10/2026):
  - V2BaseDataTable: mặc định 10 dòng/trang, lựa chọn 5/10/20/50/100, dòng tổng "Hiển thị a–b / N" (N không có dấu phẩy
    ngăn hàng nghìn — tester đã ghi nhận là lỗi chung).
  - filterStateMixin: chỉ lưu bộ lọc khi rời sang trang con (chi tiết / sửa) của chính màn, hết hạn 10 phút; rời sang màn
    khác thì xoá; lưu theo trình duyệt (không theo tài khoản), dùng chung giữa các tab.
  - V2BaseCompanyDepartmentFilter: chưa chọn Công ty → Phòng ban liệt kê mọi phòng ban trong phạm vi quyền; chọn Công ty →
    chỉ phòng ban của công ty đó; đổi Công ty → xoá Phòng ban, Bộ phận; chọn Phòng ban trước KHÔNG tự điền Công ty.
  - Ô tìm nhanh không giới hạn số ký tự.
"""
import re


class ListScreen(object):
    """Thông tin màn danh sách để dựng case chuẩn."""

    def __init__(self, menu, title, total, quick_label, quick_sample, quick_hit, filters, unit='phiếu',
                 child='màn chi tiết', org_levels=('Công ty', 'Phòng ban')):
        self.menu = menu                  # câu đường bấm menu (đã có dấu chấm cuối)
        self.title = title                # tiêu đề bảng
        self.total = total                # tổng số bản ghi ví dụ
        self.quick_label = quick_label    # ô tìm nhanh tìm theo gì
        self.quick_sample = quick_sample  # từ khóa mẫu
        self.quick_hit = quick_hit        # bản ghi khớp từ khóa mẫu
        self.filters = filters            # [(nhãn ô lọc, giá trị mẫu)] — ít nhất 2
        self.unit = unit
        self.child = child
        self.org_levels = org_levels


def open_menu_case(s, no='001', pre=None, extra=()):
    """Ý 3 — Expected mở màn ghi đủ: số dòng/trang, lựa chọn, thứ tự, khuôn dòng tổng."""
    exp = [
        '- Tiêu đề bảng "%s".' % s.title,
        '- Mặc định hiện 10 %s / trang; ô Số dòng/trang có các lựa chọn 5, 10, 20, 50, 100.' % s.unit,
        '- Sắp xếp %s tạo mới nhất ở trên, cũ nhất ở dưới.' % s.unit,
        '- Dưới bảng ghi đúng khuôn "Hiển thị 1–10 / %d".' % s.total,
    ] + list(extra)
    return (no, 'Mở màn từ menu', 'P0',
            pre or 'Tài khoản DNS Admin; trong phạm vi xem có %d %s.' % (s.total, s.unit),
            '1. Đăng nhập.\n2. ' + s.menu, '—', '\n'.join(exp))


def filter_memory_cases(s, start):
    """Ý 5 — nhớ bộ lọc 10 phút (5 case)."""
    f1, v1 = s.filters[0]
    n = start
    out = []

    def nid():
        nonlocal n
        n += 1
        return '%03d' % (n - 1)

    pre = 'Đang ở màn danh sách, đã chọn %s = %s.' % (f1, v1)
    out.append((nid(), 'Giữ bộ lọc khi mở %s rồi quay lại trước 10 phút' % s.child, 'P0', pre,
                '1. Bấm mã một %s để mở %s.\n2. Trong vòng 10 phút bấm Quay lại.' % (s.unit, s.child), '—',
                '- Quay về danh sách vẫn giữ %s = %s.\n- Danh sách đúng theo bộ lọc đó.' % (f1, v1)))
    out.append((nid(), 'Bộ lọc hết hiệu lực sau 10 phút', 'P2', pre,
                '1. Mở %s.\n2. Chờ quá 10 phút rồi quay lại danh sách.' % s.child, '—',
                '- Bộ lọc trở về trống, danh sách hiện đầy đủ như lúc mới vào màn.'))
    out.append((nid(), 'Sang màn khác rồi quay lại', 'P2', pre,
                '1. Vào một màn khác bằng menu.\n2. Quay lại màn này bằng menu (trong 10 phút).', '—',
                '- Bộ lọc trở về trống (chỉ giữ khi đi vào %s của chính màn này).' % s.child))
    out.append((nid(), 'Đổi tài khoản trên cùng trình duyệt', 'P1',
                'Tài khoản A đang lọc %s = %s và vừa mở %s.' % (f1, v1, s.child),
                '1. Đăng xuất A.\n2. Đăng nhập tài khoản B trên cùng trình duyệt trong vòng 10 phút.\n3. Mở màn danh sách.', '—',
                '- B thấy bộ lọc trống, KHÔNG thấy bộ lọc của A.\n- Lưu ý: hiện bộ lọc lưu theo trình duyệt, nếu B còn thấy bộ '
                'lọc của A thì ghi nhận lỗi.'))
    out.append((nid(), 'Mở màn trong tab trình duyệt mới', 'P2', pre,
                '1. Mở %s (bộ lọc được lưu).\n2. Trong 10 phút mở màn danh sách ở một tab mới.' % s.child, '—',
                '- Tab mới mở danh sách với bộ lọc %s = %s (bộ lọc dùng chung trên trình duyệt).' % (f1, v1)))
    return out


def combo_cases(s, start):
    """Ý 6 — kết hợp tiêu chí + độ dài ô tìm nhanh (4 case)."""
    (f1, v1), (f2, v2) = s.filters[0], s.filters[1]
    ids = ['%03d' % (start + i) for i in range(4)]
    pre = ('Trong phạm vi xem có %d %s; %s khớp từ khóa "%s"; có %s vừa khớp %s = %s vừa khớp %s = %s.'
           % (s.total, s.unit, s.quick_hit, s.quick_sample, s.unit, f1, v1, f2, v2))
    return [
        (ids[0], 'Kết hợp từ khóa tìm nhanh với 1 ô lọc', 'P0', pre,
         '1. ' + s.menu + '\n2. Nhập "%s" vào ô tìm nhanh, bấm Tìm kiếm.\n3. Bấm Tìm kiếm nâng cao.\n4. Chọn %s = %s.'
         % (s.quick_sample, f1, v1), 'Từ khóa: %s\n%s: %s' % (s.quick_sample, f1, v1),
         '- Chỉ còn %s vừa khớp từ khóa vừa có %s = %s.\n- Tổng số ở dòng "Hiển thị" giảm tương ứng.' % (s.unit, f1, v1)),
        (ids[1], 'Kết hợp 2 ô lọc với nhau', 'P0', pre,
         '1. ' + s.menu + '\n2. Bấm Tìm kiếm nâng cao.\n3. Chọn %s = %s.\n4. Chọn %s = %s.' % (f1, v1, f2, v2),
         '%s: %s\n%s: %s' % (f1, v1, f2, v2),
         '- Chỉ còn %s thỏa CẢ HAI điều kiện.\n- Bỏ một ô lọc thì danh sách nới ra tương ứng.' % s.unit),
        (ids[2], 'Kết hợp cả 3 tiêu chí', 'P1', pre,
         '1. ' + s.menu + '\n2. Nhập "%s" vào ô tìm nhanh, bấm Tìm kiếm.\n3. Bấm Tìm kiếm nâng cao.\n4. Chọn %s = %s.\n'
         '5. Chọn %s = %s.' % (s.quick_sample, f1, v1, f2, v2),
         'Từ khóa: %s\n%s: %s\n%s: %s' % (s.quick_sample, f1, v1, f2, v2),
         '- Chỉ còn %s thỏa cả 3 tiêu chí; không có thì bảng báo "Không có dữ liệu phù hợp.".\n'
         '- Bấm Làm mới xóa cả 3 tiêu chí.' % s.unit),
        (ids[3], 'Độ dài ô tìm nhanh', 'P2', 'Đang ở màn danh sách.',
         '1. Dán một chuỗi 300 ký tự vào ô tìm nhanh.\n2. Bấm Tìm kiếm.', 'Chuỗi 300 ký tự chữ và số',
         '- Ô nhận hết chuỗi, không báo lỗi, màn không treo.\n- Bảng báo "Không có dữ liệu phù hợp.".\n'
         '- Lưu ý: ô chưa giới hạn số ký tự (tìm theo %s).' % s.quick_label),
    ]


def org_cases(s, start, total_all=None):
    """Ý 2 — ô chọn cha–con Công ty → Phòng ban (→ Bộ phận) (3 case)."""
    child = s.org_levels[1]
    rest = ', '.join(s.org_levels[1:])
    ids = ['%03d' % (start + i) for i in range(3)]
    pre = ('Tài khoản có quyền xem của tổng công ty; Công ty 1 có 5 phòng ban, Công ty 2 có 4 phòng ban.')
    return [
        (ids[0], 'Chưa chọn Công ty thì ô %s' % child, 'P1', pre,
         '1. ' + s.menu + '\n2. Bấm Tìm kiếm nâng cao.\n3. Mở ô %s khi ô Công ty còn trống.' % child, '—',
         '- Ô %s liệt kê phòng ban của mọi công ty trong phạm vi quyền (9 phòng ban).\n- Chọn được ngay, danh sách lọc theo '
         'phòng ban đã chọn.' % child),
        (ids[1], 'Chọn Công ty thì ô %s chỉ còn con của công ty đó' % child, 'P0', pre,
         '1. Bấm Tìm kiếm nâng cao.\n2. Chọn Công ty = Công ty 1.\n3. Mở ô %s.' % child, 'Công ty: Công ty 1',
         '- Ô %s chỉ còn 5 phòng ban của Công ty 1.' % child),
        (ids[2], 'Chọn %s trước rồi đổi Công ty' % child, 'P1', pre,
         '1. Bấm Tìm kiếm nâng cao.\n2. Chọn %s = một phòng ban của Công ty 1 (Công ty còn trống).\n3. Chọn Công ty = Công ty 2.'
         % child, '—',
         '- Bước 2: ô Công ty KHÔNG tự điền.\n- Bước 3: các ô %s bị xóa, danh sách lọc lại theo Công ty 2.' % rest),
    ]


def weird_param_case(no, s, param_note):
    """Lối vào: sửa tay tham số trên thanh địa chỉ thành giá trị lạ."""
    return (no, 'Sửa tay tham số chế độ trên thanh địa chỉ thành giá trị lạ', 'P1',
            'Tài khoản không có quyền xem theo cấp; tự lập 3 %s.' % s.unit,
            '1. ' + s.menu + '\n2. Sửa phần tham số chế độ trên thanh địa chỉ thành "abc", nhấn Enter.', '—',
            '- Hệ thống bỏ qua giá trị lạ, mở chế độ danh sách chung (%s).\n- Vẫn chỉ thấy 3 %s của mình, không lộ thêm dữ liệu, '
            'không báo lỗi.' % (param_note, s.unit))


def add_advanced_step(cases, ids, menu):
    """Ý 4 — chèn bước "Bấm Tìm kiếm nâng cao." vào đầu các case lọc ô nâng cao, đánh số lại."""
    out = []
    for c in cases:
        if c[0] in ids and 'nâng cao' not in c[4]:
            lines = [re.sub(r'^\d+\.\s*', '', x) for x in c[4].split('\n') if x.strip()]
            if lines and lines[0].startswith('Vào phân hệ'):
                lines = lines[1:]
            steps = [menu, 'Bấm Tìm kiếm nâng cao.'] + lines
            c = (c[0], c[1], c[2], c[3], '\n'.join('%d. %s' % (i + 1, x) for i, x in enumerate(steps)), c[5], c[6])
        out.append(c)
    return out


def fill_pre(cases, mapping, default=None):
    """Thay tiền điều kiện '—' bằng câu có số liệu: mapping {id: câu}, còn lại dùng default."""
    out = []
    for c in cases:
        if str(c[3]).strip() in ('—', '-', ''):
            pre = mapping.get(c[0], default)
            assert pre, 'Case %s còn tiền điều kiện trống — khai mapping' % c[0]
            c = (c[0], c[1], c[2], pre) + tuple(c[4:])
        out.append(c)
    return out


def check_no_dash_pre(sections, role_tcs):
    bad = [tc[0] for _, _, tcs in sections for tc in tcs if str(tc[3]).strip() in ('—', '-', '')]
    bad += [tc[0] for tc in role_tcs if str(tc[3]).strip() in ('—', '-', '')]
    assert not bad, 'Còn tiền điều kiện trống: %s' % bad
