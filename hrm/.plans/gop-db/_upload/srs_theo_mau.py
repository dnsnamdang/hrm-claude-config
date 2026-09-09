# -*- coding: utf-8 -*-
"""Chuyen 2 generator SRS sang dung khuon BAN MAU CUA SKILL.

Ban mau chuan (chot 03/09/2026 sau khi tester phan hoi 2 lan):
    .claude/skills/srs-documenter/assets/SRS_MAU.docx = "SRS - Phieu de nghi thu tien"
Day la chung tu cung dang voi 2 man cua minh (co trang thai, lap phieu, gui duyet), khac han
"SRS - Danh muc quoc gia" tren Drive — file do la DANH MUC, va la ban chua co phan quyen nen bo
cot Ky hieu + rut cot bang giao dien. BAM THEO SRS_MAU, KHONG bam theo Danh muc quoc gia.

Ban mau giu nguyen (generator goc da dung, khong dong toi):
  - Phan 2: 2 bang co cot "Ky hieu" (Q1.., V1..) + ma tran phan quyen dung Q/V lam tieu de cot
  - Bang "Mo ta chi tiet giao dien": 7 cot cho chuc nang chi doc, 8 cot cho chuc nang co nhap lieu
  - Muc dich viet dang gach dau dong (List Bullet)

Chi bo sung 3 diem con thieu:
  1. Moi muc "2.x.y Gioi thieu" mo dau bang dong "Quy tac chung: Ap dung SRS Cac quy tac chung
     SRS_Cac quy tac chung_VN_1.0 - <nhom quy tac>. Chi bo sung <phan rieng> tai phan mo ta chi tiet."
  2. Muc Layout: "Duong dan man hinh:" + "Menu: <phan he => nhom => man>" (MOT dong), bo han URL
  3. Phan 4 mo dau bang dong "Quy tac ap dung: ..."

Chay 1 lan tren ban generator GOC:  python3 srs_theo_mau.py
"""
import ast
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.dirname(HERE)

HELPERS = '''

# ------------------------------------------------- khuon cua ban mau SRS_MAU.docx
# Ban mau: .claude/skills/srs-documenter/assets/SRS_MAU.docx ("SRS - Phieu de nghi thu tien").
# Bang giao dien + bang phan quyen giu nguyen theo lib; chi bo sung dong "Quy tac chung" o moi
# muc Gioi thieu va doi muc Layout sang ghi duong bam menu.
QUY_TAC_CHUNG = 'SRS_Các quy tắc chung_VN_1.0'


def rule(nhom, rieng):
    """Dong "Quy tac chung" dau moi muc Gioi thieu — bam nguyen van ban mau."""
    d.p('Quy tắc chung: Áp dụng SRS Các quy tắc chung %s - %s. Chỉ bổ sung %s tại phần mô tả '
        'chi tiết.' % (QUY_TAC_CHUNG, nhom, rieng))


def layout(menu, shot=None, shot_caption=None, modal=None):
    """Muc Layout — ghi duong bam menu, KHONG ghi URL (dung nhu ban mau)."""
    d.p('Đường dẫn màn hình:')
    for m in (menu if isinstance(menu, (list, tuple)) else [menu]):
        d.p('Menu: %s' % m)
    if modal:
        d.p('Modal %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.' % modal)
    if shot:
        d.figure(shot, shot_caption or 'Màn hình thực tế', width_in=6.2)
'''


def transform(path, rules, menus, extra):
    src = io.open(path, encoding='utf-8').read()

    anchor = "img_prefix='%s')" % extra['img_prefix']
    assert anchor in src, path
    src = src.replace(anchor, anchor + HELPERS, 1)

    tree = ast.parse(src)
    edits = []
    layout_i = 0
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr != 'layout':
            continue
        kw = {k.arg: k.value for k in node.keywords}
        parts = ["menu=%r" % (menus[layout_i],)]
        layout_i += 1
        for k in ('modal', 'shot', 'shot_caption'):
            if k in kw:
                parts.append('%s=%s' % (k, ast.get_source_segment(src, kw[k])))
        edits.append((node, 'layout(%s)' % ', '.join(parts)))

    # ⚠️ col_offset cua ast tinh bang BYTE UTF-8 — tai lieu tieng Viet day dau nen phai cat
    # chuoi o muc byte, cat theo ky tu se an nham mat mot doan nguon.
    data = src.encode('utf-8')
    offs = [0]
    for ln in data.splitlines(keepends=True):
        offs.append(offs[-1] + len(ln))
    for node, new_txt in sorted(edits, key=lambda e: -offs[e[0].lineno - 1]):
        start = offs[node.lineno - 1] + node.col_offset
        end = offs[node.end_lineno - 1] + node.end_col_offset
        data = data[:start] + new_txt.encode('utf-8') + data[end:]
    src = data.decode('utf-8')

    def add_rule(m):
        r = rules.get(m.group(1))
        return m.group(0) + ("\n" + r if r else "")
    src = re.sub(r"d\.p\('(\d+\.\d+\.\d+) Giới thiệu'\)", add_rule, src)

    for old, new in extra['replace']:
        assert old in src, 'khong tim thay doan can sua: %s' % old[:60]
        src = src.replace(old, new, 1)

    io.open(path, 'w', encoding='utf-8').write(src)
    print('%s: %d muc Layout, %d dong Quy tac chung' % (os.path.basename(path), layout_i,
                                                        len(rules)))


# ============================================================= MAN 1
M1 = 'Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành'
M1_SALE = ('Phân hệ Bán hàng => Bán dịch vụ => Báo giá dịch vụ SC-BD-BT '
           '=> Yêu cầu sửa chữa - bảo hành')

transform(
    os.path.join(GOPDB, 'warranty-repair-request', 'gen_srs.py'),
    rules={
        '2.1.1': "rule('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột',\n"
                 "     'các quy tắc riêng của màn Yêu cầu kiểm tra sửa chữa – bảo hành')",
        '2.2.1': "rule('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang',\n"
                 "     'các tiêu chí tìm kiếm và lọc riêng của màn hình')",
        '2.3.1': "rule('Cấu hình bộ lọc và Tùy chỉnh cột',\n"
                 "     'danh sách cột và ô lọc riêng của màn hình')",
        '2.4.2': "rule('Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX',\n"
                 "     'các trường riêng của phiếu và quy tắc bắt buộc nhập theo từng nút bấm')",
        '2.5.2': "rule('Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử',\n"
                 "     'điều kiện được phép sửa của màn hình')",
        '2.6.1': "rule('Màn Xem chi tiết và Phân quyền',\n"
                 "     'bố cục các khối và điều kiện hiện / ẩn từng nút của màn hình')",
        '2.7.2': "rule('Quy tắc thao tác trạng thái, Thông báo và Quy tắc ghi lịch sử',\n"
                 "     'điều kiện chuyển phòng tiếp nhận của màn hình')",
        '2.8.2': "rule('Quy tắc thao tác trạng thái, Thông báo và Quy tắc ghi lịch sử',\n"
                 "     'điều kiện từ chối và tác động lên trạng thái phiếu')",
        '2.9.2': "rule('Quy tắc điều hướng sang chứng từ tiếp theo và Phân quyền',\n"
                 "     'điều kiện lập phiếu xử lý của màn hình')",
        '2.10.2': "rule('Quy tắc Xóa, Thông báo và Quy định xác nhận',\n"
                  "     'điều kiện được phép xóa của màn hình')",
        '2.11.2': "rule('Quy tắc In và Mẫu in chứng từ',\n"
                  "     'nội dung bản in và giới hạn in danh sách của màn hình')",
        '2.12.2': "rule('Quy tắc Excel và Cấu hình cột',\n"
                  "     'danh sách trường được phép xuất riêng của màn hình')",
        '2.13.1': "rule('Quy tắc ghi lịch sử và hiển thị lịch sử',\n"
                  "     'danh sách trường được theo dõi riêng của màn hình')",
    },
    menus=[[M1, M1_SALE],                                # 2.2 tim kiem
           [M1 + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột'],  # 2.3
           [M1 + ' => Tạo mới'],                         # 2.4
           [M1 + ' => Chỉnh sửa'],                       # 2.5
           [M1 + ' => Xem chi tiết'],                    # 2.6
           [M1 + ' => Chuyển phòng tiếp nhận'],          # 2.7
           [M1 + ' => Từ chối'],                         # 2.8
           [M1 + ' => Tạo phiếu xử lý yêu cầu'],         # 2.9
           [M1 + ' => Xóa'],                             # 2.10
           [M1 + ' => In'],                              # 2.11
           [M1 + ' => Xuất excel'],                      # 2.12
           [M1 + ' => Lịch sử']],                        # 2.13
    extra={
        'img_prefix': 'wrr_',
        'replace': [
            # muc Layout dau tien cua 2.1 viet tay bang bullets -> doi sang khuon menu
            ("""d.p('Đường dẫn màn hình:')
d.bullets([
    'URL đầy đủ: %s (CSKH → Kiểm tra bảo hành sửa chữa → “Yêu cầu kiểm tra sửa chữa - bảo hành”). '
    'Hiển thị: toàn bộ phiếu trong phạm vi quyền của người đăng nhập.' % URL_CSKH,
    'URL đầy đủ: %s (Bán hàng → Bán dịch vụ → Báo giá dịch vụ SC-BD-BT → “Yêu cầu sửa chữa - bảo '
    'hành”). Hiển thị: CHỈ phiếu do chính người đăng nhập lập — đây là phạm vi mặc định.' % URL_BH,
])
d.p('Cùng một màn hình nhưng hai lối vào cho hai danh sách khác nhau. Danh sách ít hơn mong đợi '
    'thường là do vào từ lối vào thứ hai, không phải hệ thống thiếu dữ liệu.')
d.figure(shot('01-danh-sach.png'),
         'Màn Yêu cầu kiểm tra sửa chữa – bảo hành lúc mới truy cập', width_in=6.2)""",
             """layout(menu=[MENU_CSKH + '   (hiển thị: toàn bộ phiếu trong phạm vi quyền của người '
                          'đăng nhập)',
             MENU_SALE + '   (hiển thị: chỉ phiếu do chính người đăng nhập lập — phạm vi mặc định)'],
       shot=shot('01-danh-sach.png'),
       shot_caption='Màn Yêu cầu kiểm tra sửa chữa – bảo hành lúc mới truy cập')"""),
            ("""URL_CSKH = 'https://<host-hrm>/customer-care/warranty-repair-requests?type=all'
URL_BH = 'https://<host-hrm>/customer-care/warranty-repair-requests'""",
             """MENU_CSKH = ('Phân hệ CSKH => Kiểm tra bảo hành sửa chữa '
             '=> Yêu cầu kiểm tra sửa chữa - bảo hành')
MENU_SALE = ('Phân hệ Bán hàng => Bán dịch vụ => Báo giá dịch vụ SC-BD-BT '
             '=> Yêu cầu sửa chữa - bảo hành')"""),
            ("    full_url=URL_CSKH,",
             "    full_url='/customer-care/warranty-repair-requests',   # lib giu de tham chieu"),
            ("""d.h1('Phần 4. Quy tắc nghiệp vụ')

d.p('BR-01""",
             """d.h1('Phần 4. Quy tắc nghiệp vụ')

d.p('Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung '
    '%s. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu kiểm tra sửa chữa – bảo hành; không '
    'lặp lại các quy tắc đã có trong SRS quy tắc chung.' % QUY_TAC_CHUNG)

d.p('BR-01"""),
        ],
    })

# ============================================================= MAN 2
M2 = 'Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu'

transform(
    os.path.join(GOPDB, 'warranty-repair-handle-request', 'gen_srs.py'),
    rules={
        '2.1.1': "rule('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột',\n"
                 "     'các quy tắc riêng của màn Phiếu xử lý yêu cầu')",
        '2.2.1': "rule('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang',\n"
                 "     'các tiêu chí tìm kiếm và lọc riêng của màn hình')",
        '2.3.1': "rule('Cấu hình bộ lọc và Tùy chỉnh cột',\n"
                 "     'danh sách cột và ô lọc riêng của màn hình')",
        '2.4.2': "rule('Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX',\n"
                 "     'các trường riêng của phiếu và quy tắc bắt buộc nhập theo từng nút bấm')",
        '2.5.2': "rule('Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử',\n"
                 "     'điều kiện được phép sửa của màn hình')",
        '2.6.1': "rule('Màn Xem chi tiết và Phân quyền',\n"
                 "     'bố cục các khối và điều kiện hiện / ẩn từng nút của màn hình')",
        '2.7.2': "rule('Màn Thêm mới danh mục, Validate dữ liệu và Thông báo',\n"
                 "     'các trường của cửa sổ thêm nhanh nguyên nhân')",
        '2.8.2': "rule('Quy tắc điều hướng sang chứng từ tiếp theo và Phân quyền',\n"
                 "     'điều kiện lập phiếu cung cấp thông tin của màn hình')",
        '2.9.2': "rule('Quy tắc thao tác trạng thái, Thông báo và Quy tắc ghi lịch sử',\n"
                 "     'điều kiện không duyệt và tác động lên trạng thái phiếu')",
        '2.10.2': "rule('Quy tắc Xóa, Thông báo và Quy định xác nhận',\n"
                  "     'điều kiện được phép xóa và tác động lên phiếu yêu cầu gốc')",
        '2.11.2': "rule('Quy tắc In và Mẫu in chứng từ',\n"
                  "     'nội dung bản in và giới hạn in danh sách của màn hình')",
        '2.12.2': "rule('Quy tắc Excel và Cấu hình cột',\n"
                  "     'danh sách trường được phép xuất riêng của màn hình')",
        '2.13.1': "rule('Quy tắc ghi lịch sử và hiển thị lịch sử',\n"
                  "     'danh sách trường được theo dõi riêng của màn hình')",
    },
    menus=[[M2],                                            # 2.2
           [M2 + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột'],     # 2.3
           ['Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành '
            '=> Tạo phiếu xử lý yêu cầu'],                  # 2.4
           [M2 + ' => Chỉnh sửa'],                          # 2.5
           [M2 + ' => Xem chi tiết'],                       # 2.6
           [M2 + ' => Tạo mới / Chỉnh sửa => Thêm nhanh'],  # 2.7
           [M2 + ' => Tạo phiếu cung cấp thông tin'],       # 2.8
           [M2 + ' => Không duyệt'],                        # 2.9
           [M2 + ' => Xóa'],                                # 2.10
           [M2 + ' => In'],                                 # 2.11
           [M2 + ' => Xuất excel'],                         # 2.12
           [M2 + ' => Lịch sử']],                           # 2.13
    extra={
        'img_prefix': 'wrhr_',
        'replace': [
            ("""d.p('Đường dẫn màn hình:')
d.bullets([
    'URL đầy đủ: %s (CSKH → Kiểm tra bảo hành sửa chữa → “Phiếu xử lý yêu cầu”). Hiển thị: toàn bộ '
    'phiếu trong phạm vi quyền của người đăng nhập.' % URL_ALL,
    'URL đầy đủ: %s (đường dẫn trần, không có mục menu). Hiển thị: CHỈ phiếu do chính người đăng '
    'nhập lập — đây là phạm vi mặc định.' % URL_MINE,
    'URL đầy đủ: %s (đường dẫn trần, không có mục menu). Hiển thị: phiếu đang ở trạng thái Chờ '
    'CCTT, dành cho người có quyền Tạo phiếu cung cấp thông tin.' % URL_WAIT,
])
d.p('Cùng một màn hình nhưng các lối vào cho ra phạm vi dữ liệu khác nhau. Danh sách ít hơn mong '
    'đợi thường là do vào bằng đường dẫn trần, không phải hệ thống thiếu dữ liệu.')
d.figure(shot('01-danh-sach.png'), 'Màn Phiếu xử lý yêu cầu lúc mới truy cập', width_in=6.2)""",
             """layout(menu=[MENU_CSKH + '   (hiển thị: toàn bộ phiếu trong phạm vi quyền của người '
                          'đăng nhập)',
             MENU_CSKH + ' — mở bằng đường dẫn trần, không qua menu   (hiển thị: chỉ phiếu do '
                         'chính người đăng nhập lập — phạm vi mặc định)',
             MENU_CSKH + ' — lối vào danh sách chờ cung cấp thông tin   (hiển thị: phiếu đang ở '
                         'trạng thái Chờ CCTT)'],
       shot=shot('01-danh-sach.png'),
       shot_caption='Màn Phiếu xử lý yêu cầu lúc mới truy cập')"""),
            ("""URL_ALL = 'https://<host-hrm>/customer-care/warranty-repair-handle-requests?type=all'
URL_MINE = 'https://<host-hrm>/customer-care/warranty-repair-handle-requests'
URL_WAIT = ('https://<host-hrm>/customer-care/warranty-repair-handle-requests'
            '?type=waiting_information')""",
             """MENU_CSKH = 'Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu'"""),
            ("    full_url=URL_ALL,",
             "    full_url='/customer-care/warranty-repair-handle-requests',   # lib giu de tham chieu"),
            ("""d.h1('Phần 4. Quy tắc nghiệp vụ')

d.p('BR-01""",
             """d.h1('Phần 4. Quy tắc nghiệp vụ')

d.p('Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung '
    '%s. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu xử lý yêu cầu; không lặp lại các quy '
    'tắc đã có trong SRS quy tắc chung.' % QUY_TAC_CHUNG)

d.p('BR-01"""),
        ],
    })

print('Xong. Chay lai 2 generator de sinh file .docx moi.')
