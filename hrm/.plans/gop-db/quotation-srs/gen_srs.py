# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo giá.docx" theo FORM CHUẨN (srs-documenter, form 2026-09-24 + 7 quy tắc 05/10/2026).

Nguồn: code nhánh gop_db (worktree gop_db-client / gop_db-api), đọc 13/10/2026.
Tóm tắt code đã rà: ./_brief/brief_A..D.md (truy vết file:dòng).
Ảnh chụp thật (Playwright, 1440x900, cổng 3002): ./quotation_shots/ — KHÔNG commit.

Yêu cầu riêng của user (13/10/2026), ưu tiên hơn khung 4 chương của skill:
  - Thêm BẢNG ĐÍNH KÈM thể hiện công thức / logic tính báo giá  -> chương "Phụ lục" cuối tài liệu
  - Có phần Xóa báo giá
  - "Điều kiện ban đầu" ghi rõ: quyền gì, trạng thái báo giá nào, yêu cầu đặc biệt
  - Thứ tự: Tạo mới (thông tin chung, bảng chi tiết, tổng hợp, VAT & GG, điều khoản, lưu/gửi duyệt)
            -> Chỉnh sửa (+ Import) -> Sao chép -> Duyệt/Từ chối -> Xem chi tiết -> In -> Xuất Excel -> Lịch sử
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '..', '.claude', 'skills',
                                                 'srs-documenter', 'assets')))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.environ.get('SRS_SHOTS') or os.path.join(HERE, 'quotation_shots')
OUT = os.path.join(HERE, 'SRS - Báo giá.docx')


def shot(name):
    return os.path.join(SHOTS, name)


ACT_KD = 'Nhân viên kinh doanh'
ACT_TP = 'Trưởng phòng'
ACT_BGD = 'Ban giám đốc'

MENU = 'Phân hệ CSKH trước bán => Báo giá'
MENU_DUYET = 'Phân hệ Bán hàng => Phê Duyệt => Dự án TKT => Báo giá chờ duyệt'
MENU_TAO = MENU + ' => Tạo báo giá'
MENU_SUA = MENU + ' => Sửa / Làm giá'

d = SrsDoc(out=OUT, menu=MENU, route='/assign/quotations', full_url='', img_prefix='bg_')
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ CSKH trước bán': 'phanhe',
    'Phân hệ Bán hàng': 'phanhe_banhang',
    'Báo giá': 'baogia',
    'Tạo báo giá': 'taomoi',
    'Tìm kiếm nâng cao': 'timkiem',
    'Sửa': 'sua',
    'Thêm nhóm': 'themnhom',
    'Thêm hàng tạm': 'hangtam',
    'Lưu nháp': 'luunhap',
    'Gửi duyệt': 'guiduyet',
    'Import Excel': 'import',
    'Xuất Excel': 'xuatexcel',
    'Sao chép báo giá': 'saochep',
    'Xóa': 'xoa',
    'Duyệt': 'duyet',
    'Từ chối': 'tuchoi',
    'In báo giá': 'in',
    'In': 'in_ct',
    'Lịch sử': 'lichsu',
}.items()})


def dk(quyen, trang_thai, khac):
    """Điều kiện ban đầu — 3 ý user yêu cầu: quyền, trạng thái báo giá, yêu cầu đặc biệt."""
    return ('• Quyền: %s\n• Trạng thái báo giá: %s\n• Yêu cầu khác: %s'
            % (quyen, trang_thai, khac))


def L(*items):
    return list(items)


# =================================================================== TRANG ĐẦU
d.title_block('Báo giá')
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1. GIỚI THIỆU
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Báo giá (Danh sách báo giá, Tạo báo giá, '
    'Làm giá, Xem chi tiết, Báo giá chờ duyệt), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của luồng báo giá: lập – gửi duyệt – duyệt/từ chối.',
    'Làm rõ cách tính thành tiền, giảm giá, VAT, tỷ suất lợi nhuận dòng và tỷ suất lợi nhuận tổng '
    '(chi tiết ở Phụ lục – Bảng đính kèm công thức).',
    'Làm rõ cách hệ thống xử lý khi giá bán / giá vốn hàng hoá trên ERP thay đổi trong lúc tạo mới, '
    'chỉnh sửa, sao chép và import báo giá.',
    'Làm rõ cách xác định cấp duyệt (Tự duyệt / Trưởng phòng / Trưởng phòng & Ban giám đốc).',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Báo giá tự nhập', 'Báo giá do người dùng tự xây dựng bảng hàng hoá (không kế thừa BOM). '
                        'Được thêm / sửa / xoá nhóm, hàng hoá, dịch vụ.'),
    ('Báo giá từ BOM', 'Báo giá kế thừa cấu trúc hàng hoá của BOM tổng hợp đã duyệt của dự án. '
                       'Cấu trúc khoá, chỉ được sửa giá.'),
    ('Hàng ERP', 'Hàng hoá có trong danh mục hàng hoá ERP. Giá nhập, giá bán, VAT lấy từ ERP, '
                 'người dùng không sửa được.'),
    ('Hàng tạm', 'Hàng hoá chưa có trong danh mục ERP, người dùng tự khai báo. Giá nhập, giá bán, VAT '
                 'nhập tay. Mã hàng tạm dạng HHBG + 6 số, hệ thống sinh khi Lưu.'),
    ('Hàng cha / hàng con', 'Hàng cha là cụm thiết bị; hàng con là thiết bị thành phần của cụm. '
                            'Hàng con không tính tiền riêng, giá trị nằm trong hàng cha.'),
    ('Giá nhập (giá vốn)', 'Đơn giá vốn của hàng hoá / dịch vụ.'),
    ('Giá bán', 'Đơn giá bán chào khách, trước giảm giá, trước VAT.'),
    ('GG', 'Giảm giá. Có 3 phương thức: Không GG / GG mặt hàng (giảm trên từng dòng) / GG tổng '
           '(giảm trên tổng đơn hàng rồi phân bổ xuống từng dòng).'),
    ('TSLN', 'Tỷ suất lợi nhuận, tính TRÊN GIÁ VỐN: (Thành tiền bán sau GG − Thành tiền nhập) / '
             'Thành tiền nhập × 100%.'),
    ('Bảng giá', 'Bảng giá bán của ERP: Bán lẻ, Giá bán theo lô, Đại lý cấp 1/2/3, Giá bán thương mại '
                 'điện tử. Quyết định giá bán của hàng ERP.'),
    ('Cấp duyệt', 'Cấp 1 – Tự duyệt (người lập tự duyệt); Cấp 2 – Trưởng phòng duyệt; Cấp 3 – Trưởng '
                  'phòng duyệt rồi chuyển Ban giám đốc duyệt.'),
    ('YCBG', 'Yêu cầu xây dựng giá (Yêu cầu tính giá bán) — nguồn lập báo giá từ BOM.'),
    ('Sale phụ trách dự án', 'Nhân viên kinh doanh phụ trách Dự án TKT mà báo giá gắn vào.'),
    ('Người lập', 'Người tạo báo giá (người bấm Lưu lần đầu).'),
    ('TP / BGĐ', 'Trưởng phòng / Ban giám đốc.'),
], widths=[1.6, 4.4])

# ========================================================= PHẦN 2. PHÂN QUYỀN
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác (nhóm quyền "Báo giá"):')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Xây dựng giá bán theo công ty',
     'Lập báo giá và sao chép báo giá lập từ Yêu cầu xây dựng giá của dự án triển khai liên phòng.'),
    ('Q2', 'Xây dựng giá bán theo phòng',
     'Như Q1 nhưng cho dự án triển khai theo phòng; Yêu cầu xây dựng giá phải cùng phòng ban với '
     'người thao tác.'),
    ('Q3', 'Trưởng phòng duyệt giá Bom giải pháp',
     'Vào màn Báo giá chờ duyệt; Duyệt / Duyệt & chuyển BGĐ / Từ chối báo giá đang "Chờ TP duyệt" '
     'thuộc phòng ban mình quản lý; nhận thông báo gửi duyệt.'),
    ('Q4', 'Ban giám đốc duyệt giá Bom giải pháp',
     'Vào màn Báo giá chờ duyệt; BGĐ duyệt / Từ chối báo giá đang "Chờ BGĐ duyệt" thuộc công ty của '
     'mình; nhận thông báo TP đã duyệt & chuyển BGĐ.'),
    ('Q5', 'Xem giá vốn hàng hoá',
     'Thấy Giá nhập, Thành tiền nhập, Tỷ suất LN, Cấp duyệt dự kiến; thấy giá vốn trong popup Gửi '
     'duyệt, popup Sao chép, file xuất Excel và lịch sử. Thiếu quyền → các ô này hiện "—".'),
    ('Q6', 'Cho phép thêm giảm giá trong báo giá',
     'Chọn phương thức GG, nhập GG mặt hàng, khai báo giảm giá tổng, phân bổ, xoá giảm giá. '
     'Thiếu quyền → ô GG khoá; giữ nguyên giảm giá cũ vẫn lưu được.'),
], widths=[0.7, 2.0, 3.3])
d.p('Không có quyền riêng cho Tạo / Sửa / Xoá / Gửi duyệt / Sao chép / In / Xuất Excel / Import. '
    'Các thao tác này được quyết định theo VAI TRÒ trên báo giá:')
d.table(['Vai trò', 'Được làm'], [
    ('Người lập', 'Sửa, Xoá, Gửi duyệt, Tự duyệt (cấp 1), Import — chỉ khi báo giá đang "Đang tạo". '
                  'Sao chép báo giá không gắn dự án do mình lập.'),
    ('Sale phụ trách dự án', 'Tạo báo giá tự nhập gắn dự án; sao chép báo giá tự nhập của dự án; sửa Ghi '
                             'chú kinh doanh khi báo giá Đã duyệt.'),
    ('Mọi người dùng vào được màn', 'Tạo báo giá không gắn dự án; xem, in, xuất Excel, xem lịch sử báo '
                                    'giá trong phạm vi dữ liệu của mình.'),
], widths=[1.8, 4.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước '
    'thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách Báo giá theo tổng công ty', 'Toàn bộ báo giá của hệ thống.'),
    ('V2', 'Xem danh sách Báo giá theo công ty',
     'Báo giá thuộc công ty đang chọn của người đăng nhập, cộng báo giá do mình lập.'),
    ('V3', 'Xem danh sách Báo giá theo phòng ban',
     'Báo giá thuộc phòng ban / bộ phận mình quản lý, cộng báo giá do mình lập.'),
    ('V4', 'Xem danh sách Báo giá theo bộ phận',
     'Báo giá thuộc bộ phận mình quản lý, cộng báo giá do mình lập.'),
    ('—', '(không có cấp nào)', 'Chỉ báo giá do chính mình lập.'),
], widths=[0.7, 2.3, 3.0])
d.p('Ghi chú: công ty / phòng ban / bộ phận của báo giá lấy theo hồ sơ của người lập tại thời điểm '
    'tạo. Người duyệt (Q3/Q4) xem được chi tiết báo giá đang chờ chính mình duyệt dù nằm ngoài phạm vi '
    'V1–V4.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1/Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách báo giá', '✅', '✅', '✅', '✅', '✅', '✅ (theo V1–V4)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 → FR-13 Tạo mới, bảng chi tiết, Lưu nháp, Gửi duyệt', '✅ (từ YCBG)', '❌', '❌', '✅ (thấy giá vốn)',
     '✅ (giảm giá)', '✅ (không gắn dự án, hoặc là Sale phụ trách)'),
    ('FR-14 Chỉnh sửa báo giá', '❌', '❌', '❌', '✅ (thấy giá vốn)', '✅ (giảm giá)', '✅ (người lập, Đang tạo)'),
    ('FR-15 Import báo giá từ Excel', '❌', '❌', '❌', '✅ (thấy giá vốn)', '❌', '✅ (người lập, Đang tạo)'),
    ('FR-16 Sao chép báo giá', '✅ (BG từ YCBG)', '❌', '❌', '✅ (thấy giá vốn)', '❌',
     '✅ (Sale phụ trách / người lập)'),
    ('FR-17 Xóa báo giá', '❌', '❌', '❌', '❌', '❌', '✅ (người lập, Đang tạo)'),
    ('FR-18 Duyệt báo giá', '❌', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '❌', '❌', '❌'),
    ('FR-19 Từ chối báo giá', '❌', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '❌', '❌', '❌'),
    ('FR-20 Xem chi tiết', '✅', '✅', '✅', '✅', '✅', '✅ (trong phạm vi)'),
    ('FR-21 In báo giá', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-22 Xuất Excel danh sách', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-23 Xuất Excel chi tiết', '✅', '✅', '✅', '✅ (có cột giá vốn)', '✅', '✅'),
    ('FR-24 Xem lịch sử', '✅', '✅', '✅', '✅ (thấy giá nhập)', '✅', '✅'),
], widths=[1.9, 0.75, 0.65, 0.65, 0.7, 0.6, 0.95])

# ============================================= PHẦN 3. ĐẶC TẢ CHI TIẾT
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
MAINS = [
    ('FR-01', 'Xem danh sách báo giá', 'view'),      # 0
    ('FR-03', 'Tạo mới báo giá', 'crud'),            # 1
    ('FR-13', 'Lưu nháp / Gửi duyệt', 'action'),     # 2
    ('FR-14', 'Chỉnh sửa báo giá', 'crud'),          # 3
    ('FR-15', 'Import báo giá từ Excel', 'io'),      # 4
    ('FR-16', 'Sao chép báo giá', 'crud'),           # 5
    ('FR-17', 'Xóa báo giá', 'action'),              # 6
    ('FR-18', 'Duyệt báo giá', 'action'),            # 7
    ('FR-19', 'Từ chối báo giá', 'action'),          # 8
    ('FR-21', 'In báo giá', 'io'),                   # 9
    ('FR-22/23', 'Xuất Excel', 'io'),                # 10
]
d.overview_figure2(
    [(ACT_KD, [0, 1, 2, 3, 4, 5, 6, 9, 10]),
     (ACT_TP, [0, 7, 8]),
     (ACT_BGD, [0, 7, 8])],
    MAINS,
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-20', 'Xem chi tiết báo giá', 'view', 'extend', [0], None),
     ('FR-24', 'Xem lịch sử', 'view', 'extend', [0], None),
     ('FR-05', 'Thêm hàng hoá có sẵn', 'sub', 'extend', [1], None),
     ('FR-06', 'Thêm hàng tạm', 'sub', 'extend', [1], None),
     ('FR-07', 'Thêm dịch vụ / chi phí', 'sub', 'extend', [1], None),
     ('FR-11', 'Áp dụng VAT và giảm giá', 'sub', 'extend', [1], None)],
    'Sơ đồ Use Case tổng quan màn Báo giá')

d.h2('2 Đặc tả chi tiết từng chức năng')


def fn(num, title, code, group, actor, intro, rule, menu, shots, ui, ui_mode, events,
       uc=True, extra=None):
    """Dựng 1 chức năng 2.x theo đúng thứ tự mục con của form chuẩn."""
    d.h3('%s %s' % (num, title))
    k = 0

    def sub(name):
        nonlocal k
        k += 1
        d.p('%s.%d %s' % (num, k, name))

    if uc:
        sub('Biểu đồ Usecase')
        d.uc_figure(code, title, group, actor=actor,
                    caption='Biểu đồ Use Case — %s %s' % (code, title))
    sub('Giới thiệu')
    d.rule_ref(rule[0], anchor=rule[1])
    d.intro_table(**intro)
    sub('Layout màn hình')
    first = shots[0]
    d.layout(menu=menu, shot=shot(first[0]), shot_caption=first[1])
    for f, c in shots[1:]:
        d.figure(shot(f), c, width_in=6.2)
    sub('Mô tả chi tiết giao diện')
    if ui_mode == 'full':
        d.ui_table(ui)
    elif ui_mode == 'ro':
        d.ui_table(ui, required=False)
    else:
        d.ui_table(ui, required=False, scope=False)
    sub('Danh sách event và xử lý event')
    d.event_table(events)
    if extra:
        extra()


NO_PERM = ('– Nếu không đủ điều kiện → không hiển thị nút; gọi thẳng chức năng thì hệ thống từ '
           'chối với thông báo tương ứng và dừng xử lý.')

# ------------------------------------------------------------- 2.1 Xem danh sách
fn('2.1', 'Xem danh sách báo giá', 'FR-01', 'view', ACT_KD,
   dict(ten='Truy cập và xem danh sách báo giá',
        mota='Hiển thị bảng báo giá nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân trang, '
             'cấu hình cột và các thao tác trên từng dòng.',
        tacnhan='Nhân viên kinh doanh, Trưởng phòng, Ban giám đốc; Người dùng đã đăng nhập',
        dieukien=dk('không cần quyền riêng; phạm vi dữ liệu theo V1–V4 (không có → chỉ báo giá do mình lập).',
                    'mọi trạng thái.', 'đã đăng nhập; có quyền vào phân hệ CSKH trước bán hoặc Bán hàng.'),
        chinh='1. Người dùng vào menu Phân hệ CSKH trước bán → Báo giá (hoặc Phân hệ Bán hàng → Bán hàng → '
              'Báo giá → Danh sách báo giá).\n'
              '2. Hệ thống xác định phạm vi dữ liệu theo quyền V1 → V4.\n'
              '3. Hệ thống hiển thị trang 1, 20 dòng/trang, sắp xếp Ngày tạo mới nhất trước.\n'
              '4. Mỗi dòng hiện các nút thao tác theo trạng thái báo giá và vai trò của người xem.',
        phu='• Không có báo giá phù hợp → bảng hiện "Không có dữ liệu phù hợp bộ lọc."\n'
            '• Lỗi tải → thông báo "Lỗi tải dữ liệu".\n'
            '• Bộ lọc đang dùng được giữ lại 10 phút khi người dùng đi sang màn chi tiết / sửa rồi quay lại.',
        dacbiet=None),
   ('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc '
    'riêng của màn Báo giá tại phần mô tả chi tiết.', 'list'),
   MENU,
   [('01-danh-sach.png', 'Màn Danh sách báo giá lúc mới truy cập'),
    ('01c-hanh-dong-khac.png', 'Cột Hành động và menu "Hành động khác" của một báo giá Đang tạo')],
   [
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Danh sách báo giá', '- Tiêu đề cố định trên header.'),
       ('Nút Tạo báo giá', 'Button', 'Enable', '–', 'Hiển thị',
        L('- Luôn hiện (không gắn quyền).', '- Bấm → mở màn Tạo báo giá (mục 2.3).')),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
        '- Bấm → mở popup Chọn trường xuất file (mục 2.22).'),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        L('- Ẩn / hiện / kéo đổi thứ tự cột.', '- Cột khoá, không bỏ tích được: STT, Mã báo giá, Hành động.')),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự', '- Ghim bên trái, đánh liên tục qua các trang.'),
       ('Cột Mã báo giá', 'Table/Grid', 'Read-only', 'BG-YYYY-NNNNN', 'Theo dữ liệu',
        L('- Ghim bên trái, sắp xếp được.', '- Bấm mã → mở màn Xem chi tiết báo giá (mục 2.20).',
          '- Báo giá tổng (mã BGT-…) → mở màn Báo giá tổng.')),
       ('Cột Loại báo giá', 'Badge', 'Read-only', '3 giá trị', 'Theo dữ liệu',
        L('- "Từ BOM": báo giá kế thừa BOM tổng hợp.', '- "Tự nhập": báo giá tự xây dựng.',
          '- "Báo giá tổng": báo giá gộp của dự án cha.')),
       ('Cột BOM list', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- "Mã BOM - Tên BOM"; trống với báo giá tự nhập.'),
       ('Cột Mã yêu cầu xây dựng giá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        '- Mã YCBG nguồn; trống với báo giá tự nhập.'),
       ('Cột Dự án TKT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- "Mã - Tên dự án"; trống nếu báo giá không gắn dự án.'),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Tên khách hàng.'),
       ('Cột Giai đoạn dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Giai đoạn dự án ghi trên báo giá.'),
       ('Cột Tiền tệ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Loại tiền của báo giá (VNĐ, USD…).'),
       ('Cột Tổng giá trị sau VAT', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
        L('- Căn phải, định dạng 1,234,567, làm tròn số nguyên.', '- Sắp xếp được.',
          '- = dòng V "Tổng giá trị báo giá", cột Thành tiền sau VAT (Phụ lục, bảng PL-3).')),
       ('Cột Cấp duyệt', 'Badge', 'Read-only', '3 giá trị', 'Theo dữ liệu',
        L('- "Tự duyệt" (cấp 1), "TP" (cấp 2), "TP & BGĐ" (cấp 3).', '- Trống khi chưa gửi duyệt.')),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Người duyệt cuối cùng.'),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy HH:mm', 'Theo dữ liệu', '- Sắp xếp được.'),
       ('Cột Đồng bộ ERP', 'Badge', 'Read-only', '2 giá trị', 'Theo dữ liệu',
        L('- "Đã đồng bộ" (xanh): báo giá đã duyệt đã đẩy sang ERP.',
          '- "Thất bại" (đỏ): rê chuột xem lý do lỗi.', '- Trống khi chưa duyệt.')),
       ('Cột Người tạo / Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        '- "Tên nhân viên - Mã phòng".'),
       ('Cột Ngày tạo / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy HH:mm', 'Theo dữ liệu',
        L('- Sắp xếp được.', '- Mặc định sắp Ngày tạo giảm dần.')),
       ('Cột Trạng thái', 'Badge', 'Read-only', '7 giá trị', 'Theo dữ liệu',
        L('- Đang tạo (xám)', '- Chờ TP duyệt (cam)', '- Chờ BGĐ duyệt (cam)', '- Đã duyệt (xanh lá)',
          '- Đóng (xám)', '- Dừng (đỏ)', '- Trúng thầu (tím)')),
       ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo trạng thái',
        L('- Tối đa 3 nút hiện thẳng; nhiều hơn → 2 nút đầu + nút "⋮ Hành động khác".',
          '- Sửa / Làm giá: Đang tạo + là người lập → mục 2.14.',
          '- Xóa (đỏ): Đang tạo + là người lập → mục 2.17.',
          '- Sao chép báo giá: đủ điều kiện sao chép, mọi trạng thái → mục 2.16.',
          '- Chốt báo giá (Trúng thầu) / Hủy chốt: báo giá không gắn dự án, là người lập.',
          '- Lập hợp đồng: Trúng thầu, chưa có hợp đồng, là người lập. Xem hợp đồng: đã có hợp đồng.',
          '- In báo giá: luôn hiện → mục 2.21.', '- Lịch sử: luôn hiện → mục 2.24.',
          '- Nút không đủ điều kiện → ẨN (không hiện xám).')),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1, 20 dòng',
        '- Nút đầu / lùi / số trang / tiến / cuối + ô số dòng mỗi trang.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '- "Không có dữ liệu phù hợp bộ lọc."'),
   ], 'ro',
   [
       ('Mở màn hình', 'System',
        'Before:\n– Xác định phạm vi dữ liệu theo quyền V1 → V4.\n'
        'After:\n– Trả về trang 1 và tổng số bản ghi; hiển thị bảng và nút thao tác theo từng dòng.'),
       ('Bấm Mã báo giá', 'Click', 'After:\n– Mở màn Xem chi tiết báo giá (mục 2.20).'),
       ('Bấm tiêu đề cột sắp xếp được', 'Click',
        'After:\n– Đổi chiều sắp xếp tăng / giảm, nạp lại trang 1.'),
       ('Bấm số trang / đổi số dòng mỗi trang', 'Click / Change',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp lại dữ liệu trang mới.'),
       ('Bấm nút trong cột Hành động', 'Click',
        'After:\n– Chuyển sang chức năng tương ứng (mục 2.14, 2.16, 2.17, 2.21, 2.24).'),
   ], uc=False)

# ------------------------------------------------------------- 2.2 Tìm kiếm
fn('2.2', 'Tìm kiếm và lọc báo giá', 'FR-02', 'view', ACT_KD,
   dict(ten='Tìm kiếm và lọc danh sách báo giá',
        mota='Thu hẹp danh sách báo giá theo ô tìm nhanh và khối Tìm kiếm nâng cao.',
        tacnhan='Nhân viên kinh doanh, Trưởng phòng, Ban giám đốc; Người dùng đã đăng nhập',
        dieukien=dk('không cần quyền riêng; lựa chọn Công ty / Phòng ban / Bộ phận bị giới hạn theo V1–V4.',
                    'mọi trạng thái.', 'đang ở màn Danh sách báo giá.'),
        chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi bấm Tìm kiếm hoặc Enter.\n'
              '2. Hoặc bấm Tìm kiếm nâng cao → chọn giá trị ở các ô lọc.\n'
              '3. Chọn xong 1 ô lọc → hệ thống lọc ngay, không cần bấm Tìm kiếm.\n'
              '4. Bảng hiển thị kết quả từ trang 1.',
        phu='• Bấm Làm mới → xoá hết điều kiện lọc và nạp lại danh sách.\n'
            '• Đổi Dự án TKT → xoá giá trị Giải pháp và Version giải pháp đã chọn.',
        dacbiet=None),
   ('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Báo giá.', 'search'),
   MENU + ' => Tìm kiếm nâng cao',
   [('02-tim-kiem.png', 'Khối Tìm kiếm nâng cao đang mở')],
   [
       ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Trống',
        L('- Placeholder: "Tìm theo mã báo giá, tên khách hàng".', '- Tìm gần đúng theo Mã báo giá HOẶC tên khách hàng.',
          '- Chỉ tìm khi bấm Tìm kiếm / Enter.')),
       ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', 'Hiển thị',
        L('- Tìm kiếm: áp ô tìm nhanh.', '- Làm mới: xoá mọi điều kiện lọc.')),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Bật / tắt và sắp xếp các ô lọc.'),
       ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn',
        '- Mở / đóng khối lọc nâng cao.'),
       ('Ô Công ty, Phòng ban, Bộ phận', 'Dropdown', 'Enable', 'Danh sách', 'Trống',
        L('- Lọc theo đơn vị của báo giá (theo người lập).', '- Chỉ liệt kê đơn vị trong phạm vi quyền V1–V4.')),
       ('Ô Nhân viên', 'Dropdown', 'Enable', 'Danh sách', 'Trống', '- Lọc theo người lập. Hiển thị "Tên - Mã phòng - Mã NV".'),
       ('Ô Dự án TKT', 'Dropdown', 'Enable', 'Gõ tìm, 20 kết quả', 'Trống', '- Đổi giá trị → xoá Giải pháp, Version giải pháp.'),
       ('Ô Giải pháp', 'Dropdown', 'Disable / Enable', 'Danh sách', 'Trống', '- Khoá khi chưa chọn Dự án TKT.'),
       ('Ô Version giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Trống', '- Chỉ có lựa chọn khi đã chọn Giải pháp.'),
       ('Ô Khách hàng', 'Dropdown', 'Enable', 'Gõ tìm', 'Trống', '- Lọc theo khách hàng.'),
       ('Ô Trạng thái', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Trống',
        L('- Mặc định: trống (tất cả).', '- Lựa chọn: Đang tạo · Chờ TP duyệt · Chờ BGĐ duyệt · Đã duyệt · Đóng · Dừng · Trúng thầu.')),
       ('Ô Loại báo giá', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Trống',
        L('- Mặc định: trống.', '- Lựa chọn: Báo giá thường · Báo giá tổng.')),
       ('Ô Cấp duyệt', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Trống',
        L('- Mặc định: trống.', '- Lựa chọn: Cấp 1 — Tự duyệt · Cấp 2 — TP duyệt · Cấp 3 — BGĐ duyệt.')),
       ('Ô Người duyệt', 'Dropdown', 'Enable', 'Danh sách', 'Trống', '- Lọc theo người duyệt cuối.'),
       ('Ô Giai đoạn dự án', 'Dropdown', 'Enable', 'Danh sách', 'Trống',
        L('- Mỗi giai đoạn kèm icon ⓘ: “<mô tả của giai đoạn trong danh mục>”.',
          '- Giai đoạn đã khoá vẫn hiện khi đang được dùng để lọc.')),
       ('Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Trống', '- Khoảng ngày tạo báo giá (tính theo ngày).'),
   ], 'full',
   [
       ('Bấm Tìm kiếm / Enter ở ô tìm nhanh', 'Click / Keypress',
        'During:\n– Lọc theo mã báo giá hoặc tên khách hàng chứa từ khoá.\nAfter:\n– Nạp lại trang 1.'),
       ('Chọn giá trị ở 1 ô lọc nâng cao', 'Change',
        'During:\n– Kết hợp với các điều kiện lọc đang có (AND).\nAfter:\n– Nạp lại trang 1 ngay.'),
       ('Đổi Dự án TKT', 'Change', 'After:\n– Xoá Giải pháp và Version giải pháp; nạp lại danh sách.'),
       ('Bấm Làm mới', 'Click', 'After:\n– Xoá hết điều kiện lọc, nạp lại trang 1.'),
   ], uc=False)

# ------------------------------------------------------------- 2.3 Tạo mới - thông tin chung
TAO_DK = dk('không cần quyền riêng. Báo giá gắn dự án: phải là Sale phụ trách dự án. Lập từ Yêu cầu '
            'xây dựng giá: cần Q1 (dự án liên phòng) hoặc Q2 (dự án theo phòng, YCBG cùng phòng).',
            'báo giá chưa tồn tại (sẽ ở trạng thái Đang tạo sau khi Lưu).',
            'dự án được chọn phải là dự án con hoặc dự án độc lập — dự án cha không lập báo giá riêng.')

fn('2.3', 'Tạo mới báo giá — Thông tin chung', 'FR-03', 'crud', ACT_KD,
   dict(ten='Tạo mới báo giá — nhập khối Thông tin chung',
        mota='Mở màn Tạo báo giá, chọn dự án (hoặc khách hàng) và khai báo thông tin chung: tiền tệ, '
             'bảng giá, giao hàng, bảo hành, giai đoạn dự án. Báo giá chỉ được tạo khi bấm Lưu nháp / '
             'Gửi duyệt (mục 2.13).',
        tacnhan='Nhân viên kinh doanh (Sale phụ trách dự án / người lập)',
        dieukien=TAO_DK,
        chinh='1. Người dùng bấm Tạo báo giá ở màn danh sách.\n'
              '2. Hệ thống mở màn "Tạo báo giá": Mã báo giá "(Chưa tạo)", Loại tiền tệ VNĐ, Bảng giá Bán lẻ, '
              'phương thức GG "Không GG".\n'
              '3. Người dùng chọn Dự án (chỉ liệt kê dự án mình là Sale phụ trách) — hệ thống điền khách '
              'hàng, MST, địa chỉ, email, người liên hệ, SĐT, tiền tệ, giai đoạn theo dự án.\n'
              '4. Nếu dự án có BOM tổng hợp đã duyệt: chọn BOM → hệ thống nạp nhóm, hàng hoá, dịch vụ của BOM.\n'
              '5. Không chọn dự án → bấm Chọn khách hàng để chọn khách hàng trực tiếp.\n'
              '6. Người dùng nhập Giao hàng (ngày), Bảo hành (tháng), Email, chọn Bảng giá, Giai đoạn dự án.\n'
              '7. Tiếp tục khai báo bảng chi tiết (mục 2.4 – 2.12) và Lưu (mục 2.13).',
        phu='• Đổi / bỏ chọn Dự án khi đã có hàng hoá → hỏi "Xác nhận thay đổi Dự án": “Việc chọn lại Dự án sẽ '
            'xóa toàn bộ thông tin hàng hoá/dịch vụ trên báo giá!”. Đồng ý → xoá sạch bảng chi tiết.\n'
            '• Chọn BOM khi chưa có tiền tệ → thông báo "Vui lòng chọn loại tiền tệ trước để tính tỷ giá quy '
            'đổi khi tải sản phẩm từ BOM."\n'
            '• Đổi Bảng giá khi có hàng ERP → hỏi "Xác nhận đổi bảng giá"; đồng ý → cập nhật lại Giá bán + VAT '
            'các hàng ERP theo bảng giá mới (giá vốn, hàng tạm, chiết khấu giữ nguyên).\n'
            '• Đổi Loại tiền tệ khi đã có giá → hỏi "Xác nhận đổi loại tiền tệ"; số đã nhập KHÔNG quy đổi.\n'
            '• Dự án con: Loại tiền tệ, Bảng giá, phương thức GG kế thừa dự án cha và bị khoá.\n'
            '• Chọn dự án cha → báo "Dự án cha không lập báo giá riêng. Vui lòng tạo báo giá trên dự án con, '
            'hoặc dùng Báo giá tổng ở màn dự án cha."',
        dacbiet='Hiệu lực báo giá do hệ thống tự tính, không nhập tay (xem Phụ lục, bảng PL-7). '
                'Tiền tệ và Bảng giá chỉ đổi được ở màn Tạo mới.'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn '
    'Báo giá tại phần mô tả chi tiết.', 'create'),
   MENU_TAO,
   [('03-tao-moi.png', 'Màn Tạo báo giá — khối Thông tin chung khi chưa chọn dự án')],
   [
       ('Mã báo giá', 'Text', 'Read-only', 'BG-YYYY-NNNNN', '–', '(Chưa tạo)', '- Hệ thống sinh khi Lưu.'),
       ('Dự án', 'Dropdown', 'Enable', 'Gõ tìm, tối đa 50', 'Không', 'Trống',
        L('- Hiển thị "Mã — Tên dự án".', '- Chỉ liệt kê dự án mình là Sale phụ trách.',
          '- Có nút × để bỏ chọn.')),
       ('BOM tổng hợp', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Không', 'Trống',
        L('- Chỉ BOM tổng hợp cấp giải pháp đã duyệt của dự án.', '- Chưa chọn dự án: "Chọn dự án trước".',
          '- Dự án không có BOM: "Không có BOM tổng hợp đã duyệt".', '- Dự án có đúng 1 BOM → tự chọn.')),
       ('Khách hàng', 'Button / Text', 'Enable / Read-only', 'Danh sách', 'Có khi không chọn dự án', 'Trống',
        L('- Có dự án: chữ chỉ đọc lấy theo dự án.', '- Không dự án: nút "Chọn khách hàng" / "Đổi khách hàng".',
          '- Gợi ý xám: “Không chọn dự án = báo giá không gắn Dự án TKT, khách hàng chọn trực tiếp.”',
          '- Thiếu: "Bắt buộc phải nhập".')),
       ('MST, Địa chỉ, SĐT liên hệ, Người liên hệ', 'Text', 'Read-only', '–', '–', '—', '- Lấy theo dự án / khách hàng.'),
       ('Email khách hàng', 'Textbox', 'Enable', '0–255 ký tự, email', 'Không', 'Theo dự án',
        '- Sai định dạng: "Định dạng email không hợp lệ".'),
       ('Giao hàng (ngày)', 'Number', 'Enable', '> 0', 'Có khi Gửi duyệt', 'Trống',
        '- Thiếu khi Gửi duyệt: "Vui lòng nhập thời gian giao hàng".'),
       ('Hiệu lực báo giá', 'Text', 'Read-only', 'dd/mm/yyyy', '–', 'Tự tính',
        L('- = MIN(hôm nay + số ngày hiệu lực cấu hình ERP (mặc định 30), ngày đổi giá ERP sắp tới gần nhất).',
          '- Màn Sửa: khác ngày đã lưu thì kèm "(đã lưu: dd/mm/yyyy)".')),
       ('Loại tiền tệ', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Có khi Gửi duyệt', 'VNĐ',
        L('- Có dự án: mặc định tiền tệ của dự án.', '- Khoá ở màn Sửa và khi kế thừa dự án cha.',
          '- Thiếu: "Vui lòng chọn loại tiền tệ".')),
       ('Bảo hành (tháng)', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', '–'),
       ('Bảng giá', 'Dropdown', 'Enable / Disable', 'Danh sách 6 giá trị', 'Có', 'Bán lẻ',
        L('- Mặc định: Bán lẻ.', '- Lựa chọn: Bán lẻ · Giá bán theo lô · Đại lý cấp 1 · Đại lý cấp 2 · Đại lý cấp 3 · '
          'Giá bán thương mại điện tử (online).', '- Thiếu: "Vui lòng chọn bảng giá".')),
       ('Giai đoạn dự án', 'Dropdown', 'Enable', 'Danh sách', 'Có khi Gửi duyệt', 'Giai đoạn hiện tại của dự án',
        L('- Chỉ hiện khi có dự án.', '- Mỗi giai đoạn có icon ⓘ: “<mô tả giai đoạn trong danh mục>”.',
          '- Thiếu: "Vui lòng chọn giai đoạn dự án".')),
       ('Tỷ giá', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        '- Chỉ hiện với ngoại tệ: "Tỷ giá: 1 <mã tiền> = <tỷ giá> VND (<ngày tạo>) - Bảng giá bán lẻ".'),
   ], 'full',
   [
       ('Bấm Tạo báo giá', 'Click',
        'After:\n– Mở màn Tạo báo giá với giá trị mặc định: VNĐ, Bán lẻ, Không GG, VAT vận chuyển 8%.'),
       ('Chọn Dự án', 'Change',
        'Before:\n– Đã có hàng hoá/dịch vụ → hỏi "Xác nhận thay đổi Dự án". Huỷ → giữ dự án cũ.\n'
        'During:\n– Dự án cha → báo "Dự án cha không lập báo giá riêng…" và dừng.\n'
        'After:\n– Xoá bảng chi tiết cũ; điền thông tin khách hàng, tiền tệ, giai đoạn; dò BOM tổng hợp đã duyệt.\n'
        '– Dự án con: khoá tiền tệ, bảng giá, phương thức GG theo dự án cha.'),
       ('Chọn BOM tổng hợp', 'Change',
        'Before:\n– Chưa có tiền tệ → thông báo chọn tiền tệ trước và dừng.\n'
        '– Đã có dữ liệu → hỏi "Xác nhận thay đổi BOM": “Việc chọn lại BOM sẽ xóa toàn bộ thông tin hàng hoá/dịch vụ trên báo giá!”\n'
        'After:\n– Nạp nhóm, hàng hoá, dịch vụ của BOM. Hàng ERP lấy giá vốn, giá bán ERP (quy đổi tỷ giá); '
        'hàng tạm: giá bán ban đầu = giá vốn BOM; dịch vụ giá = 0.'),
       ('Đổi Bảng giá', 'Change',
        'Before:\n– Có hàng ERP → hỏi "Xác nhận đổi bảng giá": “Đổi bảng giá sẽ cập nhật lại đơn giá bán của các '
        'hàng hoá ERP theo bảng giá mới. Chiết khấu và hàng tạm giữ nguyên. Bạn có chắc muốn đổi?”\n'
        'After:\n– Cập nhật Giá bán + VAT của hàng ERP; hàng ERP không có giá ở bảng mới giữ giá cũ; GG tổng đã '
        'phân bổ → yêu cầu phân bổ lại.'),
       ('Đổi Loại tiền tệ', 'Change',
        'Before:\n– Có giá > 0 → hỏi "Xác nhận đổi loại tiền tệ": “Các giá trị tiền tệ đã nhập sẽ không thay đổi '
        'khi bạn đổi loại tiền tệ ! Bạn có chắc chắc muốn đổi?”\n'
        'After:\n– Không quy đổi số trên màn. VNĐ → khoá làm tròn "Số nguyên (0)".'),
   ])

# ------------------------------------------------------------- 2.4 Thêm nhóm
CHI_TIET_DK = dk('như Tạo mới (mục 2.3) hoặc Chỉnh sửa (mục 2.14).',
                 'Đang tạo (tạo mới hoặc đang sửa bởi người lập).',
                 'chỉ áp cho báo giá tự nhập; báo giá từ BOM không thêm / xoá / sắp xếp hàng hoá được.')

fn('2.4', 'Thêm nhóm hàng hoá', 'FR-04', 'crud', ACT_KD,
   dict(ten='Thêm / sửa / xoá nhóm hàng hoá trong bảng chi tiết',
        mota='Tổ chức hàng hoá phần "A — Hàng hoá" theo nhóm 2 cấp: nhóm cấp 1 (I, II…) và nhóm con cấp 2 (I.1, I.2…).',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=CHI_TIET_DK,
        chinh='1. Người dùng bấm Thêm nhóm (trên thanh tiêu đề bảng hoặc dòng "A — Hàng hoá").\n'
              '2. Hệ thống mở popup "Thêm nhóm sản phẩm".\n'
              '3. Người dùng nhập Tên nhóm và bấm Thêm (hoặc Enter).\n'
              '4. Nhóm mới hiện cuối phần A, đánh số La Mã.\n'
              '5. Thêm nhóm con: bấm Thêm nhóm con trên dòng nhóm cấp 1.',
        phu='• Tạo nhóm đầu tiên → mọi hàng chưa có nhóm tự vào nhóm vừa tạo.\n'
            '• Còn hàng chưa thuộc nhóm → hiện nhóm "Không nhóm" ở đầu; khi Lưu, hàng lẻ tự gán vào nhóm đầu tiên.\n'
            '• Bấm ✏ trên dòng nhóm → popup "Sửa nhóm sản phẩm" đổi tên.\n'
            '• Bấm 🗑 "Xóa nhóm" → xoá ngay, KHÔNG hỏi xác nhận; nhóm cấp 1 xoá kèm nhóm con; hàng hoá của nhóm '
            'chuyển sang nhóm đầu tiên còn lại (hàng hoá không bị xoá).',
        dacbiet='Tối đa 2 cấp nhóm. Không có dòng tổng tiền theo nhóm — tiêu đề nhóm chỉ đếm số hàng.'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   MENU_TAO + ' => Thêm nhóm',
   [('03a-them-nhom.png', 'Popup Thêm nhóm sản phẩm')],
   [
       ('Nút Thêm nhóm', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Ẩn với báo giá từ BOM hoặc khi không sửa được.'),
       ('Popup Thêm nhóm sản phẩm / Sửa nhóm sản phẩm', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', '- Tiêu đề theo thao tác thêm / sửa.'),
       ('Tên nhóm', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
        L('- Placeholder: "Nhập tên nhóm".', '- Enter = Thêm / Lưu.')),
       ('Nút Thêm / Lưu', 'Button', 'Enable / Disable', '–', '–', 'Disable', '- Chỉ bấm được khi Tên nhóm có chữ.'),
       ('Nút Huỷ', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup, không thay đổi.'),
       ('Dòng nhóm', 'Table/Grid', 'Hiển thị', '–', '–', 'Mở rộng',
        L('- "I. <Tên nhóm> (N hàng)" + mũi tên đóng / mở.', '- Nút Thêm mới (mục 2.5), Thêm nhóm con (chỉ nhóm cấp 1), ✏ Đổi tên, 🗑 Xóa nhóm.')),
       ('Nút Thu gọn tất cả / Mở rộng tất cả', 'Button', 'Enable', '–', '–', 'Thu gọn tất cả', '- Đóng / mở mọi nhóm và nhóm con.'),
   ], 'full',
   [
       ('Bấm Thêm nhóm / Thêm nhóm con', 'Click', 'After:\n– Mở popup Thêm nhóm sản phẩm.'),
       ('Bấm Thêm', 'Click',
        'During:\n– Tên nhóm trống → nút bị khoá, không thêm.\n'
        'After:\n– Thêm nhóm trên màn (ghi vào hệ thống khi Lưu báo giá).'),
       ('Bấm 🗑 Xóa nhóm', 'Click',
        'After:\n– Xoá nhóm (và nhóm con); chuyển hàng hoá sang nhóm đầu tiên còn lại.'),
       ('Kéo thả tiêu đề nhóm', 'Drag',
        'During:\n– Chỉ đổi thứ tự giữa các nhóm cùng cấp, cùng nhóm cha; kéo sang cấp khác → con trỏ cấm.'),
   ])

# ------------------------------------------------------------- 2.5 Thêm hàng hoá có sẵn
fn('2.5', 'Thêm hàng hoá có sẵn', 'FR-05', 'crud', ACT_KD,
   dict(ten='Thêm hàng hoá có sẵn trong danh mục ERP vào báo giá',
        mota='Tìm và chọn hàng hoá ERP; hệ thống tự lấy giá bán theo Bảng giá của báo giá, giá vốn, VAT, ĐVT.',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('như Tạo mới / Chỉnh sửa. Giá vốn chỉ trả về khi có Q5; không có Q5 thì không được chọn '
                    'hàng ERP làm hàng con.',
                    'Đang tạo.', 'đã chọn Loại tiền tệ; báo giá tự nhập.'),
        chinh='1. Người dùng bấm Thêm mới ở dòng "A — Hàng hoá", trên dòng nhóm, hoặc thanh thêm nhanh cuối nhóm.\n'
              '2. Hệ thống mở popup "Thêm hàng hoá", Nhóm hàng mặc định = nhóm vừa bấm.\n'
              '3. Người dùng tìm theo tên / mã / model hoặc mở Tìm kiếm nâng cao.\n'
              '4. Bấm vào 1 dòng để thêm ngay, hoặc tích nhiều dòng rồi bấm "Thêm N hàng hoá".\n'
              '5. Hệ thống thêm vào nhóm đã chọn, Số lượng = 1, báo "Đã thêm N hàng hoá vào phiếu."; popup KHÔNG tự đóng.',
        phu='• Chưa chọn tiền tệ → "Vui lòng chọn loại tiền tệ trước khi thêm."\n'
            '• Hàng đã có trong cùng nhóm → hỏi "Hàng hoá đã tồn tại": Cộng dồn số lượng / Tạo dòng mới / Huỷ.\n'
            '• Hàng ERP là combo → tự thêm các hàng con theo công thức ghép bộ; SL con = SL công thức × SL cha, khoá.\n'
            '• Thêm con (nút Thêm con trên hàng tạm cha): hàng con trùng mã cha → "Hàng con không được trùng mã với '
            'hàng cha (<cha>): <danh sách>".\n'
            '• Không có Q5 mà chọn hàng ERP làm con → "Bạn không có quyền xem giá vốn nên không thể thêm hàng ERP làm hàng con."',
        dacbiet='Giá bán và VAT của hàng ERP bị khoá trên bảng. Khi Lưu, hệ thống luôn lấy lại giá ERP hiện hành '
                '(Phụ lục, bảng PL-7).'),
   ('- Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', 'search'),
   MENU_TAO + ' => Thêm mới',
   [('03e-popup-hang-hoa.png', 'Popup Thêm hàng hoá — đã tích chọn 2 hàng')],
   [
       ('Nhóm hàng', 'Dropdown', 'Enable', 'Danh sách nhóm', 'Có (khi báo giá có nhóm)', 'Nhóm vừa bấm',
        '- Gợi ý: “Hàng hoá sẽ được thêm vào nhóm này”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
        L('- Placeholder: "Tìm theo tên, mã, model hàng hoá".', '- Tìm khi Enter / bấm Tìm kiếm.')),
       ('Tìm kiếm nâng cao', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
        L('- 19 ô: Tính chất hàng hóa, Loại hàng hóa, Công ty, Thương hiệu, Hãng sản xuất, Xuất xứ, Lĩnh vực, Chương, '
          'Nhóm công việc, Cụm công việc, Nhóm hàng hóa, Dùng cho nhóm máy, Dùng cho máy, Hãng xe, Loại xe, '
          'Model xe, Đời xe, Model, Tồn kho.', '- Ô Công ty chỉ thu hẹp danh sách, không đổi giá.')),
       ('Nút Thêm hàng tạm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Mở popup Thêm hàng tạm (mục 2.6).'),
       ('Bảng kết quả', 'Table/Grid', 'Read-only', '–', '–', 'Trang 1, 10 dòng',
        L('- Cột: ☐ · Ảnh · Loại hàng hóa · Tên hàng hoá · Lĩnh vực · Chương · Model · Mã hàng · Nguồn hàng · '
          'Giá niêm yết · Bảo hành · VAT(%) · Định mức đàm phán giá (%) · SL tồn có thể bán · SL KM có thể xuất · '
          'SL có thể LR · Ghi chú · Tính chất hàng hóa · Nguồn.',
          '- Giá niêm yết = "<giá theo Bảng giá của báo giá> / <ĐVT>".',
          '- Rê chuột Tên hàng hoá → hiện Đặc điểm, Phụ kiện tiêu chuẩn.', '- Bấm Ảnh → xem ảnh lớn.',
          '- Bấm vào dòng → thêm ngay 1 hàng.')),
       ('Checkbox chọn', 'Checkbox', 'Enable', '–', 'Không', 'Bỏ tích', '- Chọn nhiều, giữ lựa chọn khi chuyển trang.'),
       ('Nút Thêm N hàng hoá', 'Button', 'Enable / Disable', '–', '–', 'Thêm 0 hàng hoá', '- N = số dòng đang tích; N = 0 → khoá.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup. Bấm ra ngoài popup KHÔNG đóng.'),
   ], 'full',
   [
       ('Bấm Thêm mới', 'Click',
        'Before:\n– Chưa có Loại tiền tệ → "Vui lòng chọn loại tiền tệ trước khi thêm." và dừng.\n'
        'After:\n– Mở popup Thêm hàng hoá, nạp danh sách hàng hoá ERP.'),
       ('Bấm dòng / Thêm N hàng hoá', 'Click',
        'During:\n– Trùng hàng → hỏi Cộng dồn số lượng / Tạo dòng mới / Huỷ.\n'
        '– Thêm con trùng mã cha → báo lỗi, bỏ dòng trùng.\n'
        'After:\n– Thêm dòng: Giá bán = giá ERP theo Bảng giá; Giá nhập = giá vốn ERP (có Q5); VAT = VAT ERP; '
        'SL = 1; ngoại tệ: giá ÷ tỷ giá, làm tròn 2 số lẻ.\n'
        '– Hàng combo → nạp hàng con.\n– Dò lịch đổi giá ERP sắp tới → icon ⚠ cạnh Mã + rút ngắn Hiệu lực báo giá.\n'
        '– Thông báo "Đã thêm N hàng hoá vào phiếu."'),
   ])

# ------------------------------------------------------------- 2.6 Thêm hàng tạm
fn('2.6', 'Thêm hàng tạm', 'FR-06', 'crud', ACT_KD,
   dict(ten='Thêm hàng tạm (hàng chưa có trong danh mục ERP)',
        mota='Tái sử dụng hàng tạm đã có của dự án / phiếu, hoặc khai báo mới thủ công. Giá nhập, giá bán, VAT '
             'nhập trực tiếp trên bảng chi tiết.',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('như Tạo mới / Chỉnh sửa.', 'Đang tạo.', 'đang mở popup Thêm hàng hoá; báo giá tự nhập.'),
        chinh='1. Trong popup Thêm hàng hoá, bấm Thêm hàng tạm.\n'
              '2. Chọn Nhóm hàng.\n'
              '3a. Tab "Chọn từ kho hàng tạm (Tái sử dụng)": tích hàng tạm rồi bấm "Thêm N hàng hóa".\n'
              '3b. Tab "Thêm mới thủ công": nhập Tên hàng hoá, Đơn vị tính, Thương hiệu, Xuất xứ (+ Model, Số lượng, '
              'Ghi chú, Đặc điểm) rồi bấm Lưu hoặc Lưu và tiếp tục.\n'
              '4. Hàng tạm vào bảng với Giá nhập = 0, Giá bán = 0, VAT = 0 → người dùng nhập giá trên bảng.',
        phu='• Thiếu trường bắt buộc → báo đỏ dưới ô: "Tên là bắt buộc", "Đơn vị tính là bắt buộc", '
            '"Thương hiệu là bắt buộc", "Xuất xứ là bắt buộc".\n'
            '• Bấm ⊕ cạnh Model / Thương hiệu / Xuất xứ → thêm nhanh danh mục; thành công "Đã thêm nhanh thành công."\n'
            '• Tab tái sử dụng: chọn hàng cha có con → thêm cả cha và con; giá vốn, giá bán, VAT, mã lấy theo dòng nguồn.\n'
            '• Không có hàng tạm phù hợp → "Không có hàng tạm phù hợp."',
        dacbiet='Mã hàng tạm để trống tới khi Lưu báo giá, hệ thống sinh mã HHBG + 6 số. Giữ mã cũ khi trùng hàng '
                'tạm của cùng dự án đã có trên màn Hàng hoá dự án, khi nhân bản dòng, và khi sao chép báo giá.'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   MENU_TAO + ' => Thêm mới => Thêm hàng tạm',
   [('03f-hang-tam.png', 'Tab Chọn từ kho hàng tạm (Tái sử dụng)'),
    ('03g-hang-tam-thu-cong.png', 'Tab Thêm mới thủ công')],
   [
       ('Nhóm hàng', 'Dropdown', 'Enable', 'Danh sách nhóm', 'Có', 'Nhóm đang chọn', '- Thiếu: "Vui lòng chọn nhóm hàng".'),
       ('Tab Chọn từ kho hàng tạm (Tái sử dụng)', 'Table/Grid', 'Enable', '–', '–', 'Hiển thị',
        L('- Ô "Tìm nhanh theo mã / tên hàng tạm...".', '- Cột: ☐ · Mã hàng · Tên hàng · Model · Thương hiệu · Xuất xứ · ĐVT · Nguồn.',
          '- Nguồn "Dự án": hàng tạm đã lên màn Hàng hoá dự án của cùng dự án.', '- Nguồn "Trong phiếu": hàng tạm đang có trên bảng.')),
       ('Tên hàng hoá', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', '- Placeholder "Nhập tên hàng hoá".'),
       ('Đơn vị tính', 'Dropdown', 'Enable', 'Danh mục ĐVT', 'Có', 'Trống', '- Placeholder "Chọn ĐVT".'),
       ('Model', 'Dropdown', 'Enable', 'Gõ tìm', 'Không', 'Trống', '- Nút ⊕ thêm nhanh Model.'),
       ('Thương hiệu', 'Dropdown', 'Enable', 'Gõ tìm', 'Có', 'Trống', '- Nút ⊕ thêm nhanh (Tên + Mã thương hiệu).'),
       ('Xuất xứ', 'Dropdown', 'Enable', 'Gõ tìm', 'Có', 'Trống', '- Nút ⊕ thêm nhanh.'),
       ('Số lượng cần dùng', 'Number', 'Enable', '> 0', 'Không', '1', '- Để trống → 1.'),
       ('Ghi chú', 'Textbox', 'Enable', '–', 'Không', 'Trống', '–'),
       ('Đặc điểm / Thông số kỹ thuật', 'Textarea', 'Enable', '–', 'Không', 'Trống', '- Trình soạn thảo có định dạng.'),
       ('Nút Lưu / Lưu và tiếp tục / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị',
        L('- Lưu: thêm vào bảng và đóng.', '- Lưu và tiếp tục: thêm vào bảng, xoá trắng form để nhập tiếp.', '- Đóng: huỷ.')),
   ], 'full',
   [
       ('Bấm Thêm hàng tạm', 'Click', 'After:\n– Mở popup Thêm hàng tạm, mặc định tab tái sử dụng.'),
       ('Bấm Lưu / Lưu và tiếp tục (tab thủ công)', 'Click',
        'During:\n– Thiếu Tên / ĐVT / Thương hiệu / Xuất xứ → báo đỏ dưới ô, không thêm.\n'
        'After:\n– Thêm dòng hàng tạm: mã trống, Giá nhập 0, Giá bán 0, VAT 0, SL theo ô Số lượng.'),
       ('Bấm Thêm N hàng hóa (tab tái sử dụng)', 'Click',
        'After:\n– Thêm các hàng đã chọn (kèm hàng con), giữ mã, giá, VAT của nguồn. Thông báo "Đã thêm N hàng hóa".'),
   ])

# ------------------------------------------------------------- 2.7 Thêm dịch vụ
fn('2.7', 'Thêm dịch vụ / chi phí', 'FR-07', 'crud', ACT_KD,
   dict(ten='Thêm dịch vụ / chi phí khác vào phần B',
        mota='Chọn dịch vụ / chi phí từ danh mục Dịch vụ & Chi phí của ERP vào phần "B — Dịch vụ & Chi phí khác".',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('như Tạo mới / Chỉnh sửa.', 'Đang tạo.', 'áp cho cả báo giá tự nhập và báo giá từ BOM.'),
        chinh='1. Bấm Thêm mới ở dòng "B — Dịch vụ & Chi phí khác".\n'
              '2. Hệ thống mở popup "Thêm dịch vụ / chi phí".\n'
              '3. Người dùng gõ tìm hoặc lọc theo Tất cả / Dịch vụ có tính DT / Chi phí khác.\n'
              '4. Bấm vào 1 mục → thêm 1 dòng: SL = 1, VAT theo danh mục, Giá nhập = 0, Giá bán = 0.\n'
              '5. Người dùng nhập Giá bán (và Giá nhập nếu danh mục chưa có tỷ lệ giá vốn) trên bảng.',
        phu='• Không tìm thấy → "Không tìm thấy mục nào. Bấm "Thêm mới" để tạo nhanh." → mục 2.8.\n'
            '• Danh mục đã có tỷ lệ giá vốn R% > 0 → Giá nhập khoá, tự tính = Giá bán × R%.\n'
            '• Bấm ✏ "Chọn lại dịch vụ / chi phí" → đổi sang mục khác của danh mục.\n'
            '• Bấm 🗑 "Xoá dịch vụ": dòng đã lưu → hỏi "Bạn có chắc muốn xóa dịch vụ này?" và XOÁ NGAY vào hệ thống '
            '("Đã xoá dịch vụ"); dòng chưa lưu → xoá ngay không hỏi.',
        dacbiet='Loại "Chi phí khác" vào dòng III Chi phí; còn lại vào dòng II Dịch vụ của bảng Tổng hợp (mục 2.10).'),
   ('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   MENU_TAO + ' => Thêm mới (B — Dịch vụ & Chi phí khác)',
   [('03h-dich-vu-popup.png', 'Popup Thêm dịch vụ / chi phí'),
    ('03c-dich-vu.png', 'Phần B — Dịch vụ & Chi phí khác trên bảng chi tiết')],
   [
       ('Ô tìm kiếm', 'Textbox', 'Enable', '–', 'Không', 'Trống',
        L('- Placeholder: "Tìm theo tên dịch vụ / chi phí...".', '- Tự tìm sau 0,3 giây ngừng gõ.')),
       ('Bộ lọc nút', 'Button', 'Enable', '3 giá trị', 'Không', 'Tất cả',
        L('- Mặc định: Tất cả.', '- Lựa chọn: Tất cả · Dịch vụ có tính DT · Chi phí khác.')),
       ('Danh sách mục', 'Table/Grid', 'Read-only', '–', '–', 'Toàn bộ danh mục',
        L('- Mỗi mục: tên + badge loại ("Dịch vụ có tính doanh thu" / "Chi phí khác") + "VAT x%".', '- Bấm mục → thêm 1 dòng, báo "Đã thêm: <tên>".')),
       ('Nút Thêm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Mở popup Tạo nhanh dịch vụ / chi phí (mục 2.8).'),
       ('Dòng dịch vụ trên bảng', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu',
        L('- Icon 💲 "Chi phí khác" hoặc icon "Dịch vụ"; badge "Tỷ lệ giá vốn: X%".',
          '- Icon ⓘ: “Giá vốn = Giá bán × tỷ lệ này” (rê chuột vào badge tỷ lệ giá vốn).', '- SL = 1, chỉ đọc.',
          '- Giá bán, VAT, GG nhập được; Giá nhập khoá khi có tỷ lệ > 0.')),
   ], 'full',
   [
       ('Bấm mục trong danh sách', 'Click',
        'After:\n– Thêm dòng dịch vụ (SL 1, giá 0, VAT danh mục); thông báo "Đã thêm: <tên>".'),
       ('Nhập Giá bán dịch vụ có tỷ lệ giá vốn', 'Change / Blur',
        'After:\n– Giá nhập = Giá bán × tỷ lệ / 100 (làm tròn 2 số lẻ); tính lại thành tiền, TSLN.'),
       ('Bấm 🗑 Xoá dịch vụ (dòng đã lưu)', 'Click',
        'Before:\n– Hỏi "Xác nhận xóa": “Bạn có chắc muốn xóa dịch vụ này?”\n'
        'After:\n– Xoá ngay vào hệ thống, thông báo "Đã xoá dịch vụ"; lỗi: "Lỗi xoá dịch vụ".'),
   ])

# ------------------------------------------------------------- 2.8 Tạo nhanh dịch vụ
fn('2.8', 'Tạo nhanh dịch vụ / chi phí', 'FR-08', 'crud', ACT_KD,
   dict(ten='Thêm mới nhanh dịch vụ / chi phí vào danh mục ERP',
        mota='Tạo mục mới trong danh mục Dịch vụ & Chi phí của ERP ngay trong lúc làm báo giá; dòng dịch vụ tự '
             'được thêm vào báo giá với đúng giá vừa nhập.',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('như Tạo mới / Chỉnh sửa.', 'Đang tạo.', 'đang mở popup Thêm dịch vụ / chi phí.'),
        chinh='1. Bấm Thêm mới trong popup Thêm dịch vụ / chi phí.\n'
              '2. Hệ thống mở popup "Tạo nhanh dịch vụ / chi phí"; ô Tên điền sẵn từ khoá đang gõ.\n'
              '3. Người dùng chọn Loại, nhập Tên, Giá vốn, Giá bán, % VAT.\n'
              '4. Bấm Lưu → hệ thống lưu vào danh mục ERP kèm tỷ lệ giá vốn, báo "Đã tạo mục danh mục" và '
              'thêm dòng vào phần B.',
        phu='• Thiếu / sai → báo: "Bắt buộc phải chọn loại", "Bắt buộc phải nhập tên", "Bắt buộc nhập giá vốn", '
            '"Giá bán phải lớn hơn 0", "Bắt buộc phải nhập % VAT".',
        dacbiet='Mục vừa tạo dùng được ngay cho các báo giá khác (lưu thật vào danh mục, kể cả khi không lưu báo giá).'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   MENU_TAO + ' => Thêm mới (B — Dịch vụ & Chi phí khác) => Thêm mới',
   [('03i-them-nhanh-dich-vu.png', 'Popup Tạo nhanh dịch vụ / chi phí')],
   [
       ('Loại', 'Dropdown', 'Enable', '2 giá trị', 'Có', '-- Chọn loại --',
        L('- Mặc định: trống.', '- Lựa chọn: Dịch vụ có tính doanh thu · Chi phí khác.')),
       ('Tên', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Từ khoá đang tìm', '- Placeholder "Nhập tên dịch vụ / chi phí".'),
       ('Giá vốn (<mã tiền>)', 'Number', 'Enable', '≥ 0', 'Có', '0', '–'),
       ('Giá bán (<mã tiền>)', 'Number', 'Enable', '> 0', 'Có', '0', '- Phải > 0: "Giá bán phải lớn hơn 0".'),
       ('% VAT', 'Number', 'Enable', '0 – 100', 'Có', '8', '–'),
       ('Dòng tỷ lệ giá vốn', 'Label', 'Hiển thị', '–', '–', '0%',
        L('- "Tỷ lệ giá vốn lưu vào danh mục: X%".', '- X = Giá vốn / Giá bán × 100 (2 số lẻ).')),
       ('Nút Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ], 'full',
   [
       ('Bấm Lưu', 'Click',
        'During:\n– Kiểm 5 trường bắt buộc; lỗi → báo đỏ dưới ô, không lưu.\n'
        'After:\n– Lưu mục mới vào danh mục Dịch vụ & Chi phí ERP (kèm VAT, tỷ lệ giá vốn).\n'
        '– Thêm dòng dịch vụ vào phần B với giá vốn / giá bán vừa nhập; thông báo "Đã tạo mục danh mục".'),
   ])

# ------------------------------------------------------------- 2.9 Bảng chi tiết: tính toán, sắp xếp, xoá
fn('2.9', 'Bảng chi tiết sản phẩm — tính toán, sắp xếp, xoá dòng', 'FR-09', 'crud', ACT_KD,
   dict(ten='Nhập giá, tính toán tự động, sắp xếp và xoá hàng hoá trên bảng chi tiết',
        mota='Người dùng nhập Số lượng, Giá nhập (hàng tạm), Giá bán, VAT; hệ thống tự tính thành tiền, tiền VAT, '
             'tỷ suất lợi nhuận dòng và dòng TỔNG. Cho phép kéo thả sắp xếp và xoá dòng.',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('như Tạo mới / Chỉnh sửa. Cột Giá nhập, Thành tiền nhập, TSLN của hàng ERP chỉ hiện số khi có Q5.',
                    'Đang tạo.', 'kéo thả và xoá chỉ áp cho báo giá tự nhập.'),
        chinh='1. Người dùng nhập SL, Giá nhập (hàng tạm), Giá bán (hàng tạm, dịch vụ), VAT (hàng tạm, dịch vụ).\n'
              '2. Hệ thống tính ngay: Thành tiền nhập, Thành tiền bán, Tỷ suất LN, Tiền VAT, Thành tiền sau VAT của '
              'dòng, tổng phần A, phần B và dòng TỔNG (công thức: Phụ lục, bảng PL-2, PL-3).\n'
              '3. Hàng tạm cha có con: Giá nhập cha tự tính = Σ(Giá nhập con × SL con) / SL cha; Giá bán cha người dùng '
              'nhập, phải ≥ tổng giá bán con.\n'
              '4. Kéo tay nắm ⋮⋮ để đổi thứ tự dòng / nhóm.\n'
              '5. Bấm 🗑 để xoá dòng.',
        phu='• Xoá dòng có con → hỏi “Xoá "<tên>" sẽ xoá cả <N> hàng con kèm theo. Bạn có chắc?”; không có con → '
            '“Bạn có chắc muốn xoá "<tên>" khỏi báo giá?”. Xoá trên màn, ghi vào hệ thống khi Lưu.\n'
            '• Hàng con của combo ERP: không xoá riêng, không sửa SL (tooltip “SL theo công thức ghép bộ, tự nhân theo SL cha”).\n'
            '• Nút Nhân bản (hàng tạm không có con) → chèn dòng sao ngay dưới, dùng chung mã: "Đã nhân bản hàng tạm '
            '(dùng chung mã). Chỉnh số lượng nếu cần rồi Lưu."\n'
            '• Nút Ẩn con / Hiện con (hàng ERP có con) → ẩn / hiện hàng con khi in / xuất, vẫn tính tổng.\n'
            '• Nút Sửa (hàng tạm) → popup Sửa hàng hoá (tên, ĐVT, model, thương hiệu, xuất xứ, thông số, ghi chú; không sửa giá).\n'
            '• Đổi ĐVT của hàng ERP → giá bán, giá vốn (có Q5) lấy theo ĐVT mới.\n'
            '• GIÁ BÁN THAY ĐỔI TRONG LÚC TẠO MỚI: hàng ERP có lịch đổi giá trong tương lai → icon ⚠ cạnh Mã '
            '("Giá bán thay đổi ngày dd/mm/yyyy") và Hiệu lực báo giá rút về ngày đổi giá; giá ERP đổi giữa lúc thêm '
            'hàng và lúc Lưu → màn không cảnh báo, khi Lưu hệ thống tự lấy giá ERP hiện hành (Phụ lục, bảng PL-7).\n'
            '• Sửa giá bán khi GG tổng đã phân bổ → "Giá bán đã thay đổi, vui lòng phân bổ lại giảm giá".\n'
            '• Lần đầu đổi VAT 1 dòng từ 0 sang > 0 mà còn dòng 0% → popup "Áp dụng VAT đồng loạt?" (mục 2.11).',
        dacbiet='Dòng con không tính thành tiền riêng (hiện "—"). Kéo thả chỉ đổi thứ tự, không đổi nhóm của hàng. '
                'Bảng cao tối đa 500px, có thanh cuộn ngang trên và dưới, tiêu đề cột ghim.'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   MENU_TAO,
   [('03b-chi-tiet-san-pham.png', 'Bảng Chi tiết sản phẩm — phần cột thông tin hàng hoá'),
    ('03d-cot-gia.png', 'Bảng Chi tiết sản phẩm — phần cột giá, tỷ suất LN, VAT và dòng TỔNG')],
   [
       ('Cột Thao tác', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
        L('- Tay nắm ⋮⋮ kéo thả + nút 🗑 xoá.', '- Ẩn với báo giá từ BOM hoặc khi không sửa được.')),
       ('Cột STT', 'Text', 'Read-only', '–', '–', 'Tự đánh', '- Cha: 1, 2, 3 (đánh lại trong từng nhóm). Con: 1.1, 1.2.'),
       ('Cột Mã', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
        L('- Hàng tạm chưa lưu: trống.', '- Hàng ERP có lịch đổi giá: icon ⚠ vàng, tooltip “Giá bán thay đổi ngày dd/mm/yyyy”.')),
       ('Cột Tên hàng', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
        L('- Dịch vụ có badge "DV".', '- Dưới tên: Ghi chú nội bộ của hàng ERP (chỉ đọc) và nút Sửa / Nhân bản / Thêm con / Ẩn con.')),
       ('Cột Model, Thương hiệu, Xuất xứ, Thông số kỹ thuật', 'Text', 'Read-only', '–', '–', 'Hiển thị',
        '- Ẩn / hiện bằng nút "Ẩn cột chi tiết" / "Hiện cột chi tiết".'),
       ('Cột Ghi chú', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- Placeholder "Ghi chú"; ẩn cùng nhóm cột chi tiết.'),
       ('Cột SL', 'Number', 'Enable / Read-only', '≥ 0, bước 0.01', 'Không', '1',
        L('- Nhập được ở báo giá tự nhập.', '- Báo giá từ BOM và hàng con combo ERP: chỉ đọc.')),
       ('Cột ĐVT', 'Dropdown / Text', 'Enable / Read-only', 'ĐVT của hàng', 'Không', 'ĐVT cơ bản',
        '- Chọn được chỉ với hàng ERP không có con, báo giá tự nhập.'),
       ('Cột Giá nhập (<mã tiền>)', 'Number', 'Enable / Read-only', '≥ 0', 'Có (hàng tạm, khi Gửi duyệt)', '0',
        L('- Hàng tạm không có con: nhập được, Gửi duyệt phải > 0 ("Giá nhập phải > 0").',
          '- Hàng ERP: khoá; không có Q5 → "—".', '- Hàng tạm cha có con: khoá, tooltip “Tự động tính từ SP con”.',
          '- Dịch vụ có tỷ lệ giá vốn: khoá, tooltip “Tự tính từ giá bán × tỷ lệ giá vốn”.')),
       ('Cột Thành tiền nhập', 'Text', 'Read-only', '≥ 0', '–', '0', '- = SL × Giá nhập. Hàng ERP không có Q5 → "—".'),
       ('Cột Giá bán (<mã tiền>)', 'Number', 'Enable / Read-only', '≥ 0', 'Có khi Gửi duyệt', '0',
        L('- Nhập được với hàng tạm, dịch vụ; hàng ERP khoá.', '- Con của cha ERP: "—".',
          '- Gửi duyệt: thành tiền sau GG phải > 0 ("Giá / thành tiền bán phải > 0").',
          '- Cha tạm có con: Giá bán × SL ≥ Σ(Giá bán con × SL con) ("Giá bán hàng cha phải ≥ tổng giá bán hàng con").')),
       ('Cột Thành tiền bán', 'Text', 'Read-only', '≥ 0', '–', '0', '- = thành tiền SAU giảm giá, TRƯỚC VAT (bảng PL-2).'),
       ('Cột Tỷ suất LN', 'Text', 'Read-only', '%', '–', '—',
        L('- = (Thành tiền bán − Thành tiền nhập) / Thành tiền nhập × 100, 2 số lẻ.',
          '- Đỏ khi < "Tỷ suất lợi nhuận mức sàn" (Cấu hình duyệt giá); xanh khi ≥.',
          '- Thành tiền nhập = 0 hoặc hàng ERP không có Q5 → "—".')),
       ('Cột VAT(%)', 'Number', 'Enable / Read-only', '0 – 100', 'Không', 'Theo danh mục / 0',
        L('- Icon ⓘ: “VAT chỉ áp dụng trên dòng CHA hoặc SP độc lập. SP con được cộng gộp vào CHA.” (ở tiêu đề cột)',
          '- Hàng ERP khoá, tooltip “VAT lấy từ danh mục hàng hoá ERP”.', '- Ngoài 0–100: "VAT phải trong 0–100%".')),
       ('Cột Tiền VAT, Thành tiền sau VAT', 'Text', 'Read-only', '≥ 0', '–', '0',
        L('- Tiền VAT = Thành tiền bán × VAT%.', '- Thành tiền sau VAT = Thành tiền bán + Tiền VAT.')),
       ('Dòng "A — Hàng hoá" / "B — Dịch vụ & Chi phí khác"', 'Text', 'Read-only', '–', '–', 'Hiển thị',
        '- Tổng của phần: Thành tiền nhập, Thành tiền bán, Tiền VAT, Thành tiền sau VAT.'),
       ('Dòng TỔNG', 'Text', 'Read-only', '–', '–', '0',
        L('- Tổng phần A + B; KHÔNG gồm chi phí vận chuyển.', '- TSLN dòng TỔNG = TSLN của hàng hoá + dịch vụ (không gồm vận chuyển).')),
       ('Popup xác nhận xoá dòng', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', '- Tiêu đề "Xác nhận xóa", nút Xóa (đỏ) / Huỷ.'),
   ], 'full',
   [
       ('Nhập SL / Giá nhập / Giá bán / VAT', 'Change / Blur',
        'During:\n– Kiểm VAT 0–100 ngay; các kiểm tra giá kiểm khi Gửi duyệt (mục 2.13).\n'
        'After:\n– Tính lại dòng, tổng phần, dòng TỔNG, bảng Tổng hợp, chân trang (Nhập · Bán · LN · Cấp duyệt).\n'
        '– Cha tạm có con: tính lại Giá nhập cha. GG tổng đã phân bổ: yêu cầu phân bổ lại.'),
       ('Kéo thả dòng / nhóm', 'Drag',
        'During:\n– Dòng cha: kéo cả cụm cha + con. Dòng con: chỉ trong phạm vi cha. Nhóm: chỉ cùng cấp, cùng nhóm cha.\n'
        'After:\n– Đổi thứ tự trên màn, ghi khi Lưu.'),
       ('Bấm 🗑 Xoá dòng', 'Click',
        'Before:\n– Hỏi xác nhận (kèm số hàng con nếu có).\nAfter:\n– Xoá dòng (và hàng con) trên màn; ghi khi Lưu.'),
       ('Đổi ĐVT hàng ERP', 'Change',
        'After:\n– Giá bán, giá vốn lấy theo ĐVT mới (quy đổi tỷ giá); GG nhập theo % tự tính lại tiền GG.'),
       ('Thêm hàng ERP / mở báo giá', 'System',
        'After:\n– Dò lịch đổi giá ERP sắp tới: gắn icon ⚠, rút ngắn Hiệu lực báo giá.'),
   ])

# ------------------------------------------------------------- 2.10 Tổng hợp giá trị
fn('2.10', 'Tổng hợp giá trị báo giá', 'FR-10', 'view', ACT_KD,
   dict(ten='Tổng hợp giá trị báo giá theo nhóm chi phí và chi phí vận chuyển',
        mota='Bảng tổng hợp giá trị báo giá theo 4 nhóm chi phí (Hàng hoá, Dịch vụ, Chi phí, Chi phí vận chuyển) '
             'và dòng Tổng; người dùng nhập chi phí vận chuyển ngay trong bảng.',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('như Tạo mới / Chỉnh sửa. Cột Thành tiền nhập, TSLN trước / sau GG chỉ hiện số khi có Q5 '
                    '(trừ ô nhập giá nhập vận chuyển).', 'Đang tạo (nhập được); trạng thái khác chỉ xem.',
                    'Chi phí vận chuyển chỉ được tính khi > 0.'),
        chinh='1. Hệ thống tự cộng bảng chi tiết vào các dòng I Hàng hoá, II Dịch vụ, III Chi phí.\n'
              '2. Người dùng nhập dòng IV Chi phí vận chuyển: Giá nhập vận chuyển, Chi phí vận chuyển (giá bán), GG '
              'vận chuyển (nếu có phương thức GG).\n'
              '3. Hệ thống tính VAT vận chuyển cố định 8% và dòng V Tổng giá trị báo giá.\n'
              '4. Dưới bảng hiện TSLN trước GG và TSLN sau GG (có Q5).',
        phu='• Giá nhập VC < 0 → "Giá nhập không hợp lệ"; Chi phí VC < 0 → "Chi phí vận chuyển không hợp lệ" (khi Gửi duyệt).\n'
            '• GG vận chuyển < 0 hoặc > chi phí → "GG vận chuyển không được lớn hơn chi phí".\n'
            '• Thay đổi bất kỳ giá / SL / VAT / GG ở bảng chi tiết → bảng Tổng hợp tính lại ngay.',
        dacbiet='Công thức từng ô: Phụ lục, bảng PL-3. Chân trang ghim cuối màn hiển thị Nhập · Bán · GG · Sau GG · '
                '~VND (ngoại tệ) · LN · Cấp duyệt dự kiến.'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   MENU_TAO,
   [('05-tong-hop.png', 'Bảng Tổng hợp giá trị báo giá')],
   [
       ('Cột STT / Nhóm chi phí', 'Text', 'Read-only', '–', '–', 'I – V',
        L('- I Hàng hoá: chỉ cộng dòng cha / hàng độc lập.', '- II Dịch vụ: dịch vụ có tính doanh thu.',
          '- III Chi phí: mục "Chi phí khác".', '- IV Chi phí vận chuyển: nhập tay.', '- V Tổng giá trị báo giá = I + II + III + IV.')),
       ('Cột Thành tiền nhập', 'Text', 'Read-only', '≥ 0', '–', '0', '- Không có Q5 → "—".'),
       ('Cột Thành tiền trước VAT', 'Text', 'Read-only', '≥ 0', '–', '0', '- = Σ SL × Giá bán (trước GG).'),
       ('Cột Giảm giá, Thành tiền sau GG (trước VAT)', 'Text', 'Read-only', '≥ 0', '–', 'Ẩn',
        L('- Chỉ hiện khi phương thức GG khác "Không GG".', '- Tổng Giảm giá dòng V in chữ đỏ.')),
       ('Cột Thuế VAT, Thành tiền sau VAT', 'Text', 'Read-only', '≥ 0', '–', '0',
        '- Dòng V Thành tiền sau VAT in đậm xanh kèm mã tiền (vd "154,418,400 VNĐ").'),
       ('Ô Giá nhập vận chuyển', 'Number', 'Enable', '≥ 0', 'Không', '0', '- Người lập nhập được kể cả khi không có Q5.'),
       ('Ô Chi phí vận chuyển', 'Number', 'Enable', '≥ 0', 'Không', '0', '- Là giá bán vận chuyển (trước VAT).'),
       ('Ô GG vận chuyển', 'Number', 'Enable / Ẩn', '0 – Chi phí VC', 'Không', '0',
        L('- GG mặt hàng: cặp ô % ↔ ₫ liên động.', '- GG tổng: 1 ô Phân bổ GG vận chuyển (khoá khi Tổng GG = 0).')),
       ('Ô VAT vận chuyển', 'Number', 'Disable', '8%', '–', '8', '- Cố định 8%, không sửa được.'),
       ('Dòng TSLN trước GG / TSLN sau GG', 'Label', 'Hiển thị / Ẩn', '%', '–', '0%',
        L('- Chỉ hiện khi có Q5.', '- Xanh khi ≥ 0, đỏ khi < 0.', '- Gồm cả vận chuyển (bảng PL-3).')),
       ('Chân trang ghim', 'Label', 'Hiển thị', '–', '–', '0',
        L('- Nhập (— nếu không có Q5) · Bán · GG · Sau GG · ~VND (chỉ ngoại tệ) · LN (có Q5).',
          '- Cấp duyệt dự kiến (có Q5): "C1 — Tự duyệt" / "C2 — TP" / "C3 — TP & BGĐ" — chỉ để tham khảo, '
          'cấp chính thức hiện ở popup Gửi duyệt (mục 2.13).')),
   ], 'full',
   [
       ('Nhập chi phí / giá nhập / GG vận chuyển', 'Change / Blur',
        'After:\n– Tính VAT VC = (Chi phí − GG VC) × 8%; Thành tiền sau VAT VC; dòng V; TSLN; cấp duyệt dự kiến.'),
       ('Thay đổi bảng chi tiết', 'System', 'After:\n– Cộng lại các dòng I, II, III và dòng V ngay.'),
   ])

# ------------------------------------------------------------- 2.11 VAT và giảm giá
fn('2.11', 'Áp dụng VAT và giảm giá', 'FR-11', 'crud', ACT_KD,
   dict(ten='Áp VAT đồng loạt, chọn phương thức giảm giá, khai báo và phân bổ giảm giá, làm tròn giá',
        mota='Thanh công cụ trên bảng chi tiết: VAT đồng loạt cho hàng tạm; chọn Không GG / GG mặt hàng / GG tổng; '
             'khai báo giảm giá tổng và phân bổ xuống dòng; làm tròn giá nhập, giá bán.',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('như Tạo mới / Chỉnh sửa; giảm giá cần Q6 "Cho phép thêm giảm giá trong báo giá".',
                    'Đang tạo.', 'dự án con: phương thức GG kế thừa dự án cha, bị khoá.'),
        chinh='1. VAT: nhập % vào ô VAT rồi bấm "Tất cả" (mọi hàng tạm cha / độc lập) hoặc "VAT=0" (chỉ dòng đang 0%) → '
              'thông báo "Đã áp X% cho N dòng".\n'
              '2. GG: chọn phương thức ở ô "GG:".\n'
              '3a. GG mặt hàng: nhập GG(%) hoặc GG(₫) trên từng dòng → hệ thống tính ô còn lại và Đơn giá sau GG.\n'
              '3b. GG tổng: ở khối "Giảm giá tổng đơn hàng" bấm Thêm khoản GG, chọn Loại GG, Kiểu (% / ₫), Giá trị → '
              'bấm Phân bổ tự động để chia Tổng GG xuống cột "Phân bổ GG" theo tỷ lệ giá trị.\n'
              '4. Làm tròn: chọn mức ở ô "Làm tròn" rồi bấm Áp dụng → xác nhận → "Đã làm tròn đơn giá".\n'
              '5. Mọi số tính lại ngay (bảng PL-2, PL-4); chỉ ghi vào hệ thống khi Lưu.',
        phu='• Đổi phương thức GG khi đã có dữ liệu GG → hỏi "Xác nhận đổi phương thức giảm giá": “Thay đổi phương thức '
            'sẽ xóa dữ liệu giảm giá hiện tại. Tiếp tục?”. Đồng ý → xoá mọi GG dòng, vận chuyển, khoản GG tổng.\n'
            '• Nút "Xóa giảm giá" (GG mặt hàng) → hỏi “Bạn có chắc chắn muốn xóa toàn bộ dữ liệu giảm giá?” → '
            '"Đã xóa toàn bộ dữ liệu giảm giá".\n'
            '• Nút "Xóa phân bổ" (GG tổng) → hỏi “Bạn có chắc chắn muốn xóa toàn bộ giá trị phân bổ giảm giá? Tất cả '
            'giá trị tại cột Phân bổ GG sẽ được đặt về 0” → "Đã xóa toàn bộ phân bổ giảm giá" (giữ khoản GG tổng).\n'
            '• Đã phân bổ mà lệch tổng / giá bán vừa đổi → hiện nút "Phân bổ lại".\n'
            '• Lỗi: "GG (%) phải trong 0–100%", "GG không được lớn hơn đơn giá bán", "Vui lòng chọn loại GG", '
            '"Giá trị phải > 0", "Giá trị tối đa 100%".\n'
            '• Không có Q6 mà cố thay đổi giảm giá → "Bạn không có quyền áp dụng giảm giá trong báo giá".',
        dacbiet='VAT áp theo DÒNG, không có VAT chung cho cả báo giá. VAT tính SAU giảm giá. VAT hàng ERP và dịch vụ '
                'lấy theo danh mục, không áp đồng loạt. Giảm giá thực tế của GG tổng = tổng cột Phân bổ GG; hệ thống '
                'không chặn lưu khi chưa phân bổ hết (chỉ cảnh báo màu đỏ "Chênh lệch").'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   MENU_TAO,
   [('04-vat-gg.png', 'Thanh công cụ VAT, GG, Làm tròn trên bảng chi tiết')],
   [
       ('Ô VAT (%)', 'Number', 'Enable / Disable', '0 – 100, bước 0.01', 'Không', 'Trống',
        L('- Placeholder "%".', '- Nút Tất cả / VAT=0 chỉ bấm được khi ô hợp lệ.', '- Tự xoá trắng sau khi áp.')),
       ('Nút Tất cả', 'Button', 'Enable / Disable', '–', '–', 'Disable', '- Áp VAT cho mọi hàng tạm cha / độc lập (bỏ qua hàng ERP, dịch vụ, vận chuyển).'),
       ('Nút VAT=0', 'Button', 'Enable / Disable', '–', '–', 'Disable', '- Chỉ áp cho hàng tạm cha / độc lập đang VAT 0%.'),
       ('Popup Áp dụng VAT đồng loạt?', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
        L('- Hiện 1 lần / phiên khi lần đầu đổi VAT 1 dòng từ 0 sang > 0 mà còn dòng 0%.',
          '- Nội dung: “Áp dụng X% VAT cho N sản phẩm còn đang để 0%?”',
          '- Nút "Chỉ dòng này" / "Áp dụng tất cả dòng còn 0%".')),
       ('Ô GG', 'Dropdown', 'Enable / Disable', '3 giá trị', 'Không', 'Không GG',
        L('- Mặc định: Không GG.', '- Lựa chọn: Không GG · GG mặt hàng · GG tổng.',
          '- Khoá + 🔒 khi dự án con (tooltip “Kế thừa từ dự án cha, không sửa được”) hoặc không có Q6 '
          '(tooltip “Bạn không có quyền áp dụng giảm giá trong báo giá”).')),
       ('Cột GG(%), GG(₫), Đơn giá sau GG', 'Number', 'Enable / Read-only', '0 – 100 / 0 – Giá bán', 'Không', '0',
        L('- Chỉ hiện khi GG mặt hàng.', '- Nhập % → GG(₫) = Giá bán × % (2 số lẻ); nhập ₫ → % = GG(₫) / Giá bán × 100.',
          '- Áp cho dòng cha và dịch vụ; dòng con "—".')),
       ('Cột GG phân bổ tự động', 'Text', 'Read-only', '≥ 0', '–', '0',
        L('- Chỉ hiện khi GG tổng.', '- Icon ⓘ: “Tham khảo — tự tính theo tỷ lệ giá trị”.')),
       ('Cột Phân bổ GG', 'Number', 'Enable / Disable', '≥ 0', 'Không', '0',
        L('- Chỉ hiện khi GG tổng; khoá khi Tổng GG ≤ 0.', '- Tiêu đề kèm "Còn: <Tổng GG − Đã phân bổ>" (xanh khi khớp, đỏ khi lệch).')),
       ('Khối Giảm giá tổng đơn hàng', 'Table/Grid', 'Enable', '–', '–', 'Ẩn',
        L('- Chỉ hiện khi GG tổng.', '- Cột: # · Loại GG · Kiểu (% / ₫) · Giá trị · Thành tiền GG · 🗑; dòng "Tổng GG".',
          '- Mỗi Loại GG chỉ chọn 1 lần.', '- Kiểu %: Thành tiền GG = (hàng hoá + dịch vụ + chi phí + vận chuyển, trước GG) × %.',
          '- Dòng trạng thái: "Đã phân bổ: X / Y ✓" hoặc "— Chênh lệch: Z".')),
       ('Nút Thêm khoản GG / Phân bổ tự động / Phân bổ lại', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
        L('- Ẩn khi không có Q6.', '- Phân bổ tự động: hiện khi Tổng GG > 0 và chưa phân bổ.',
          '- Phân bổ lại: hiện khi đã phân bổ mà lệch hoặc giá bán vừa đổi.',
          '- Xác nhận: “Thao tác này sẽ ghi đè toàn bộ giá trị cột "Phân bổ GG" bằng giá trị phân bổ tự động (theo tỷ lệ giá trị). Bạn có chắc chắn?”')),
       ('Nút Xóa giảm giá / Xóa phân bổ', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Hiện khi có Q6 và đã chọn phương thức GG; bấm được khi có dữ liệu để xoá.'),
       ('Ô Làm tròn', 'Dropdown', 'Enable / Disable', '7 giá trị', 'Không', 'Mặc định (tối đa 2 số lẻ)',
        L('- Icon ⓘ: “Khi bấm Áp dụng, hệ thống tự động tính toán giá trị làm tròn dựa trên cấu hình, giá trị làm tròn áp dụng với các cột GIÁ NHẬP, GIÁ BÁN”',
          '- Lựa chọn: Mặc định (tối đa 2 số lẻ) · Hàng nghìn (-3) · Hàng trăm (-2) · Hàng chục (-1) · Số nguyên (0) · 1 số lẻ (1) · 2 số lẻ (2).',
          '- VNĐ: khoá ở "Số nguyên (0)", tooltip “Đồng VNĐ mặc định làm tròn đến số nguyên”.')),
       ('Nút Áp dụng (làm tròn)', 'Button', 'Enable', '–', '–', 'Hiển thị',
        '- Xác nhận: “Bạn có chắc muốn làm tròn đến <mức> cho toàn bộ đơn giá? Thao tác này không thể hoàn tác.”'),
   ], 'full',
   [
       ('Bấm Tất cả / VAT=0', 'Click',
        'Before:\n– Ô VAT phải trong 0–100.\nAfter:\n– Ghi VAT cho các hàng tạm thuộc phạm vi; "Đã áp X% cho N dòng".'),
       ('Đổi phương thức GG', 'Change',
        'Before:\n– Kiểm Q6; không có → ô bị khoá.\n– Có dữ liệu GG → hỏi xác nhận; Huỷ → giữ phương thức cũ.\n'
        'After:\n– Xoá dữ liệu GG cũ, hiện cột / khối theo phương thức mới.'),
       ('Bấm Phân bổ tự động / Phân bổ lại', 'Click',
        'Before:\n– Hỏi xác nhận ghi đè cột Phân bổ GG.\n'
        'During:\n– Chia Tổng GG theo tỷ lệ Thành tiền trước GG của từng dòng (gồm vận chuyển), làm tròn 0,01, '
        'phần dư chia cho dòng có phần lẻ lớn nhất để tổng khớp tuyệt đối (bảng PL-4).\n'
        'After:\n– Ghi cột Phân bổ GG; "Đã cập nhật cột Phân bổ GG theo phân bổ tự động".'),
       ('Bấm Áp dụng làm tròn', 'Click',
        'Before:\n– Hỏi xác nhận.\nAfter:\n– Làm tròn Giá nhập (dòng không có con), Giá bán (dòng cha / độc lập), giá dịch vụ; '
        '"Đã làm tròn đơn giá". Không làm tròn thành tiền, VAT, GG.'),
       ('Lưu khi không có Q6 nhưng giảm giá bị thay đổi', 'System',
        'During:\n– Hệ thống chặn: "Bạn không có quyền áp dụng giảm giá trong báo giá".'),
   ])

# ------------------------------------------------------------- 2.12 Điều khoản
fn('2.12', 'Điều khoản báo giá và ghi chú nội bộ', 'FR-12', 'crud', ACT_KD,
   dict(ten='Nhập Điều khoản báo giá và Ghi chú nội bộ',
        mota='Khối "Thanh toán & Ghi chú nội bộ": chọn mẫu điều khoản để điền nhanh, chỉnh sửa nội dung điều khoản '
             '(in ra bản báo giá gửi khách) và ghi chú nội bộ (không in ra).',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('như Tạo mới / Chỉnh sửa.', 'Đang tạo.', 'Điều khoản bắt buộc khi Gửi duyệt, Lưu nháp được để trống.'),
        chinh='1. Người dùng chọn "Mẫu điều khoản báo giá" → nội dung mẫu điền vào ô Điều khoản.\n'
              '2. Người dùng chỉnh sửa nội dung trong trình soạn thảo.\n'
              '3. Người dùng nhập Ghi chú nội bộ (tuỳ chọn).',
        phu='• Ô Điều khoản đã có nội dung mà chọn mẫu khác → hỏi "Xác nhận thay đổi mẫu điều khoản": “Nếu bạn thay đổi '
            'mẫu điều khoản, thông tin điều khoản báo giá sẽ bị thay đổi! Bạn có chắc chắn muốn thực hiện?”. Huỷ → giữ nội dung.\n'
            '• Gửi duyệt khi Điều khoản trống → "Vui lòng nhập điều khoản thanh toán".',
        dacbiet='Nội dung điều khoản giữ nguyên các biến {{...}} khi lưu; chỉ thay giá trị khi xem / in: {{VAT_NOTE}} → '
                '"Giá trên đã / chưa bao gồm thuế VAT", {{VAN_CHUYEN_NOTE}} → "đã / chưa bao gồm chi phí vận chuyển", '
                '{{SO_BAO_GIA}}, {{NGAY_BAO_GIA}}, {{HIEU_LUC_BAO_GIA}}, {{TEN_KHACH_HANG}}…; biến lạ để trống. '
                'Hệ thống chỉ lưu nội dung, không lưu mẫu đã chọn.'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   MENU_TAO,
   [('06-dieu-khoan.png', 'Khối Thanh toán & Ghi chú nội bộ')],
   [
       ('Mẫu điều khoản báo giá', 'Dropdown', 'Enable / Ẩn', 'Danh mục ERP', 'Không', 'Trống',
        L('- Danh mục "Mẫu điều khoản báo giá" loại Báo giá dự án, sắp theo tiêu đề.', '- Ẩn khi không sửa được.')),
       ('Điều khoản báo giá', 'Textarea', 'Enable / Disable', '–', 'Có khi Gửi duyệt', 'Trống',
        L('- Trình soạn thảo có định dạng.', '- In ra bản báo giá (mục "Điều khoản báo giá:").',
          '- Thiếu khi Gửi duyệt: "Vui lòng nhập điều khoản thanh toán".')),
       ('Ghi chú nội bộ (chỉ nội bộ)', 'Textarea', 'Enable / Disable', '–', 'Không', 'Trống',
        L('- Không in ra bản báo giá gửi khách.', '- Hiện ở màn Xem chi tiết cho mọi người xem được báo giá.',
          '- Được sao chép sang báo giá mới.')),
   ], 'full',
   [
       ('Chọn Mẫu điều khoản', 'Change',
        'Before:\n– Ô Điều khoản có chữ → hỏi xác nhận; Huỷ → trả mẫu cũ, giữ nội dung.\n'
        'After:\n– Ghi đè nội dung ô Điều khoản bằng nội dung mẫu.'),
   ])

# ------------------------------------------------------------- 2.13 Lưu nháp / Gửi duyệt
fn('2.13', 'Lưu nháp và Gửi duyệt báo giá', 'FR-13', 'action', ACT_KD,
   dict(ten='Lưu nháp và Gửi duyệt báo giá',
        mota='Lưu nháp: ghi báo giá ở trạng thái Đang tạo. Gửi duyệt: kiểm tra đầy đủ, tính cấp duyệt rồi chuyển '
             'báo giá sang Chờ TP duyệt (cấp 2, 3) hoặc tự duyệt (cấp 1).',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('như Tạo mới (mục 2.3); màn Sửa: phải là người lập.',
                    'chưa tạo hoặc Đang tạo.',
                    'Gửi duyệt cần đủ: Giao hàng, Loại tiền tệ, Bảng giá, Điều khoản, Giai đoạn dự án (khi có dự án) '
                    'và giá hợp lệ (bảng dưới).'),
        chinh='Lưu nháp:\n'
              '1. Bấm Lưu nháp → hệ thống kiểm VAT, GG(%), khoản GG tổng, khách hàng (báo giá không dự án).\n'
              '2. Hệ thống tạo / cập nhật báo giá ở trạng thái Đang tạo, sinh Mã BG-YYYY-NNNNN (lần đầu) và mã hàng tạm.\n'
              '3. Thông báo "Đã tạo báo giá" / "Đã lưu báo giá" và quay về Danh sách báo giá.\n'
              'Gửi duyệt:\n'
              '1. Bấm Gửi duyệt → hệ thống kiểm đầy đủ (bảng giao diện dưới).\n'
              '2. Có dòng đơn giá bán ≤ 1.000 → tô cam + popup cảnh báo; người dùng chọn Tiếp tục gửi duyệt / Quay lại.\n'
              '3. Hệ thống tính cấp duyệt và mở popup "Gửi duyệt báo giá" (tổng nhập, tổng bán, tổng GG, TSLN, cấp dự kiến).\n'
              '4. Bấm Xác nhận gửi (cấp 2, 3) → trạng thái Chờ TP duyệt, gửi thông báo cho Trưởng phòng; hoặc Xác nhận '
              'duyệt (cấp 1) → trạng thái Đã duyệt, đồng bộ ERP.\n'
              '5. Thông báo "Đã gửi duyệt báo giá" / "Đã tự duyệt báo giá" và quay về Danh sách báo giá.',
        phu='• Màn Tạo mới: bấm Gửi duyệt chưa tạo báo giá; chỉ khi bấm Xác nhận mới tạo + gửi duyệt trong 1 lượt. '
            'Bị chặn → popup "Không thể gửi duyệt báo giá" kèm lý do.\n'
            '• Màn Sửa: bấm Gửi duyệt là dữ liệu đã được LƯU trước khi popup hiện; Huỷ ở popup không hoàn tác phần đã lưu.\n'
            '• Báo giá dự án con lệch Báo giá Mỏ neo của dự án cha → popup "Không thể trình duyệt — vi phạm quy tắc đồng bộ"; '
            'Lưu nháp vẫn được, kèm cảnh báo.\n'
            '• Cấp duyệt thực tế đổi thành cấp 1 lúc xác nhận → "Cấp duyệt của báo giá vừa thay đổi thành cấp 1 (tự duyệt). '
            'Vui lòng bấm Gửi duyệt lại để xác nhận."\n'
            '• Không tính được cấp → "Không tính được cấp duyệt. Vui lòng kiểm tra giá sản phẩm."',
        dacbiet='Cấp duyệt = MAX(cấp theo giá trị đơn hàng sau GG quy VND, cấp theo TSLN tổng sau GG, cấp theo TSLN thấp '
                'nhất của các dòng hàng tạm), tra theo Cấu hình duyệt giá; báo giá chỉ gồm hàng / dịch vụ ERP, đơn giá bán '
                '> 1.000, không giảm giá → tự động duyệt (Phụ lục, bảng PL-5). Hệ thống KHÔNG chặn báo giá không có hàng '
                'hoá và KHÔNG chặn giá bán thấp hơn giá vốn (chỉ đẩy cấp duyệt lên cao). Cảnh báo thoát khi chưa lưu chỉ áp '
                'cho báo giá sao chép chưa lưu.'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc '
    'chung - Quy tắc ghi lịch sử.', 'create'),
   MENU_TAO + ' => Gửi duyệt',
   [('07b-canh-bao-gia-thap.png', 'Popup cảnh báo mặt hàng có đơn giá ≤ 1.000'),
    ('07-gui-duyet.png', 'Popup Gửi duyệt báo giá — cấp duyệt dự kiến')],
   [
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về Danh sách báo giá.'),
       ('Nút Lưu nháp', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Hiện khi đang sửa được; bị khoá trong lúc xử lý.'),
       ('Nút Gửi duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Hiện khi đang sửa được.'),
       ('Kiểm tra khi Lưu nháp', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        L('- Lỗi đỏ dưới ô, tự cuộn tới ô lỗi đầu tiên:', '- "VAT phải trong 0–100%"', '- "GG (%) phải trong 0–100%" / "Giá trị tối đa 100%"',
          '- "Vui lòng chọn loại GG" / "Giá trị phải > 0" (khoản GG tổng)',
          '- Không dự án mà chưa chọn khách hàng: "Bắt buộc phải nhập" + "Vui lòng chọn dự án hoặc khách hàng trước khi tạo báo giá".')),
       ('Kiểm tra thêm khi Gửi duyệt', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        L('- "Vui lòng nhập thời gian giao hàng"', '- "Vui lòng chọn loại tiền tệ"', '- "Vui lòng chọn bảng giá"',
          '- "Vui lòng nhập điều khoản thanh toán"', '- "Vui lòng chọn giai đoạn dự án"',
          '- "Giá / thành tiền bán phải > 0"', '- "Giá nhập phải > 0" (hàng tạm)',
          '- "Giá bán hàng cha phải ≥ tổng giá bán hàng con"', '- "Giá vốn cha phải ≥ tổng giá vốn con" (có Q5)',
          '- "GG không được lớn hơn đơn giá bán"', '- "GG vận chuyển không được lớn hơn chi phí"',
          '- "Chi phí vận chuyển không hợp lệ" / "Giá nhập không hợp lệ"')),
       ('Popup Cảnh báo: Tồn tại mặt hàng có đơn giá <= 1.000 vnđ', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
        L('- “Hệ thống phát hiện báo giá đang chứa N mặt hàng chưa được cập nhật giá bán hoặc là hàng khuyến mãi/giảm giá.”',
          '- Bảng: STT · Mã hàng hóa · Tên hàng hóa · Đơn giá bán.', '- Nút "Tiếp tục gửi duyệt" / "Quay lại". Không chặn.')),
       ('Popup Gửi duyệt báo giá', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
        L('- Ô: Tổng giá nhập (có Q5) · Tổng giá bán · Tổng giảm giá + Tổng bán sau GG (khi có GG) · Tỷ suất LN (có Q5) · Cấp duyệt dự kiến.',
          '- Tỷ suất LN: xanh ≥ 20%, cam ≥ 10%, đỏ < 10%.',
          '- Cấp 1: “Theo quy chế, bạn có thể tự duyệt báo giá này.”',
          '- Cấp 2: “Theo quy chế, báo giá cần gửi tới Trưởng phòng duyệt.”',
          '- Cấp 3: “Theo quy chế, báo giá cần gửi qua 2 cấp duyệt:” + ① Trưởng phòng duyệt & chuyển BGĐ → ② Ban giám đốc duyệt.',
          '- Tự động duyệt: “Báo giá chỉ gồm hàng hoá/dịch vụ đã khai báo trên ERP, đơn giá bán > 1.000 đ và không có giảm giá — hệ thống tự động duyệt.”',
          '- Nút "Xác nhận duyệt" (cấp 1) / "Xác nhận gửi" (cấp 2, 3) · "Huỷ".')),
   ], 'full',
   [
       ('Bấm Lưu nháp', 'Click',
        'Before:\n– Kiểm người lập + trạng thái Đang tạo (màn Sửa); quyền tạo theo dự án / YCBG (màn Tạo mới).\n'
        '– Không đủ: "Bạn không phải Sale phụ trách dự án này" / "Chỉ người tạo báo giá mới có thể sửa." / '
        '"Báo giá không ở trạng thái Đang tạo, không thể sửa."\n'
        'During:\n– Kiểm tra mục "Kiểm tra khi Lưu nháp"; có lỗi → không thực hiện After.\n'
        'After:\n– Lưu báo giá Đang tạo; giá hàng ERP lấy theo ERP hiện hành; tính lại Hiệu lực báo giá.\n'
        '– Dự án đang ở bước thấp hơn "Dự toán" → chuyển dự án sang "Dự toán".\n'
        '– Ghi lịch sử "Tạo mới" / "Thay đổi thông tin" (chỉ các trường đã đổi).\n'
        '– Thông báo "Đã tạo báo giá" / "Đã lưu báo giá", quay về danh sách.'),
       ('Bấm Gửi duyệt', 'Click',
        'Before:\n– Như Lưu nháp.\n'
        'During:\n– Kiểm tra đầy đủ (Lưu nháp + Gửi duyệt); hệ thống kiểm thêm: điều khoản, giai đoạn dự án, '
        '"Có N sản phẩm/dịch vụ chưa hợp lệ (giá bán > 0, số lượng > 0, giảm giá ≤ đơn giá bán).", giá cha ≥ tổng con, '
        'đồng bộ Báo giá Mỏ neo.\n– Có lỗi → không thực hiện After.\n'
        '– Có đơn giá bán ≤ 1.000 → popup cảnh báo.\n'
        'After:\n– Tính cấp duyệt, mở popup Gửi duyệt báo giá.'),
       ('Bấm Xác nhận gửi / Xác nhận duyệt', 'Click',
        'After:\n– Đồng bộ Giai đoạn dự án về Dự án TKT; tính lại tổng và Hiệu lực báo giá.\n'
        '– Cấp 2, 3: trạng thái "Chờ TP duyệt", ghi ngày gửi, xoá lý do từ chối cũ; lịch sử "Gửi duyệt"; thông báo '
        '“<Tên người gửi> gửi duyệt báo giá (cấp TP | cấp TP + BGĐ) <Mã>” tới người có Q3 quản lý phòng ban của báo giá.\n'
        '– Cấp 1: trạng thái "Đã duyệt"; lịch sử "Tự duyệt"; YCBG → "Đã có báo giá"; dự án → tiến trình "Thương thảo giá"; '
        'đồng bộ sang ERP; thông báo "đã duyệt".\n'
        '– Thông báo "Đã gửi duyệt báo giá" / "Đã tự duyệt báo giá", quay về danh sách.'),
   ])

# ------------------------------------------------------------- 2.14 Chỉnh sửa
fn('2.14', 'Chỉnh sửa báo giá', 'FR-14', 'crud', ACT_KD,
   dict(ten='Chỉnh sửa (Làm giá) báo giá',
        mota='Sửa báo giá đang ở trạng thái Đang tạo: thông tin chung (trừ tiền tệ, bảng giá), bảng chi tiết, tổng hợp, '
             'VAT, giảm giá, điều khoản; Import Excel; Xuất Excel. Khi mở, hệ thống đối chiếu giá ERP hiện hành.',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('không cần quyền riêng; phải là NGƯỜI LẬP báo giá. Q5 để thấy giá vốn, Q6 để sửa giảm giá.',
                    'Đang tạo (kể cả báo giá bị Từ chối — đã quay về Đang tạo).',
                    'báo giá đã gửi duyệt / đã duyệt không sửa được, muốn thay đổi thì Sao chép (mục 2.16).'),
        chinh='1. Bấm Sửa / Làm giá ở danh sách hoặc màn chi tiết.\n'
              '2. Hệ thống mở màn "Làm giá: <Mã> (Đang tạo)".\n'
              '3. Hệ thống lấy giá bán ERP hiện hành của mọi hàng ERP; lệch so với giá đã lưu → popup "Đơn giá hàng hoá đã '
              'thay đổi" liệt kê tối đa 10 hàng "Tên: giá cũ → giá mới".\n'
              '4. Người dùng chọn Đồng ý (lấy giá mới) hoặc Từ chối (giữ giá cũ).\n'
              '5. Người dùng sửa dữ liệu như mục 2.3 – 2.12 rồi Lưu nháp / Gửi duyệt (mục 2.13).',
        phu='• Không đủ điều kiện mà mở bằng đường dẫn trực tiếp → băng vàng “Báo giá ở trạng thái (<trạng thái>) — không cho '
            'phép sửa.”, mọi ô khoá, ẩn Lưu nháp / Gửi duyệt.\n'
            '• Đồng ý: cập nhật Giá bán + VAT hàng ERP trên màn; khi Lưu hệ thống ghi CẢ giá vốn lẫn giá bán ERP hiện hành '
            '(theo tỷ giá đã chốt của báo giá); GG tổng đã phân bổ → phải phân bổ lại.\n'
            '• Từ chối: giữ giá cũ; khi Lưu hệ thống khôi phục đúng giá vốn + giá bán đã lưu của các hàng ERP cũ; hàng ERP mới '
            'thêm trong lần sửa này vẫn lấy giá hiện hành; VAT ERP luôn cập nhật theo danh mục.\n'
            '• Chỉ giá vốn ERP thay đổi (giá bán không đổi) → không hiện popup, nhưng khi Lưu hệ thống tự cập nhật giá vốn '
            'mới → Tỷ suất LN thay đổi sau khi lưu.\n'
            '• Hàng tạm, dịch vụ không bị ảnh hưởng (dịch vụ có tỷ lệ giá vốn vẫn tính lại Giá nhập theo tỷ lệ hiện hành).',
        dacbiet='Loại tiền tệ và Bảng giá khoá ở màn Sửa. Màn Sửa có thêm nút Xuất Excel (mục 2.23) và Import Excel (mục 2.15) '
                'trên thanh tiêu đề bảng chi tiết.'),
   ('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc '
    'chung - Quy tắc ghi lịch sử.', 'create'),
   MENU_SUA,
   [('08-chinh-sua.png', 'Màn Làm giá báo giá Đang tạo')],
   [
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Làm giá: <Mã> (<Trạng thái>)', '–'),
       ('Băng cảnh báo không sửa được', 'Label', 'Hiển thị / Ẩn', '–', '–', 'Ẩn',
        '- “Báo giá ở trạng thái (<trạng thái>) — không cho phép sửa.” khi không phải người lập hoặc không Đang tạo.'),
       ('Dự án', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
        L('- Link tên dự án, mở tab mới.', '- Báo giá sao chép: vẫn đổi được dự án (mục 2.16).')),
       ('Loại tiền tệ, Bảng giá', 'Dropdown', 'Disable', '–', '–', 'Theo dữ liệu', '- Khoá ở màn Sửa.'),
       ('Các trường còn lại', 'Theo mục 2.3 – 2.12', 'Enable', '–', 'Theo mục 2.3', 'Theo dữ liệu', '- Như màn Tạo mới.'),
       ('Popup Đơn giá hàng hoá đã thay đổi', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
        L('- “Có sự thay đổi về đơn giá của một số hàng hóa. Bạn có muốn cập nhật đơn giá theo thời giá hiện tại không?”',
          '- Danh sách tối đa 10 dòng "<Tên hàng>: <giá cũ> → <giá mới> VNĐ" (+ "… và N hàng hoá khác").',
          '- Nút "Đồng ý" / "Từ chối".', '- Chỉ so GIÁ BÁN, chênh > 0,005 mới hiện.')),
       ('Nút Import Excel / Xuất Excel', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
        L('- Import Excel: hiện khi sửa được → mục 2.15.', '- Xuất Excel → mục 2.23.')),
   ], 'full',
   [
       ('Bấm Sửa / Làm giá', 'Click',
        'Before:\n– Kiểm Đang tạo + là người lập.\n' + NO_PERM + '\n'
        'After:\n– Mở màn Làm giá với dữ liệu đã lưu.'),
       ('Mở màn Làm giá', 'System',
        'During:\n– Lấy giá bán ERP hiện hành theo Bảng giá + tiền tệ của báo giá; so với giá đã lưu.\n'
        'After:\n– Có chênh lệch → popup Đơn giá hàng hoá đã thay đổi.'),
       ('Bấm Đồng ý / Từ chối', 'Click',
        'After:\n– Đồng ý: cập nhật giá bán + VAT hàng ERP trên màn.\n– Từ chối: giữ nguyên, đánh dấu "giữ giá đã lưu" cho lần Lưu.'),
       ('Bấm Lưu nháp / Gửi duyệt', 'Click', 'Xử lý như mục 2.13; kết thúc quay về Danh sách báo giá.'),
   ])

# ------------------------------------------------------------- 2.15 Import
fn('2.15', 'Import báo giá từ Excel', 'FR-15', 'io', ACT_KD,
   dict(ten='Import hàng hoá, dịch vụ, giảm giá và chi phí vận chuyển vào báo giá từ file Excel',
        mota='Đọc file Excel theo mẫu, kiểm tra dữ liệu ở máy chủ, rồi đổ vào bảng chi tiết của màn Làm giá theo phương '
             'thức Từng phần hoặc Thay thế. Phải bấm Lưu báo giá mới ghi.',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('không cần quyền riêng; phải là người lập; Q5 để thấy giá vốn hàng ERP trong kết quả.',
                    'Đang tạo.', 'báo giá đã được lưu ít nhất 1 lần (màn Tạo mới không có nút Import).'),
        chinh='1. Ở màn Làm giá bấm Import Excel → popup "Import báo giá từ Excel".\n'
              '2. Bấm Tải file mẫu (file theo phương thức GG của báo giá) và điền dữ liệu.\n'
              '3. Bấm Chọn file Excel (.xlsx, .xls) → Load lên bảng → dữ liệu hiện ở trạng thái "Chưa validate".\n'
              '4. Bấm Validate → máy chủ kiểm tra; hợp lệ → "Dữ liệu hợp lệ. Bấm "Import" để ghi đè báo giá."\n'
              '5. Bấm Import → chọn "Import từng phần" hoặc "Thay thế hoàn toàn" → Import.\n'
              '6. Dữ liệu đổ vào bảng: "Đã nạp dữ liệu từ file Excel. Kiểm tra lại rồi bấm "Lưu báo giá" để chốt."\n'
              '7. Người dùng bấm Lưu nháp / Gửi duyệt (mục 2.13).',
        phu='• Sai định dạng file → "Định dạng file không hỗ trợ. Vui lòng chọn file Excel (.xlsx, .xls)."\n'
            '• File sai mẫu → "File không đúng mẫu: không tìm thấy khu vực "Khai báo hàng hoá - dịch vụ"."; file rỗng → '
            '"File không có dòng dữ liệu nào để import."; file có mật khẩu / đang mở / hỏng → thông báo tương ứng.\n'
            '• Có lỗi → dòng tô đỏ, liệt kê "[Tên cột] lỗi", popup "Import thất bại: Phát hiện N lỗi dữ liệu" (Sao chép lỗi, '
            'Tải File lỗi CSV); nút Import khoá cho tới khi Validate lại không còn lỗi.\n'
            '• Model / Thương hiệu / Xuất xứ / Dịch vụ chưa có danh mục → cảnh báo vàng "… chưa có trong danh mục — sẽ tự '
            'tạo mới khi import.", không chặn.\n'
            '• File xuất từ báo giá khác → tiêu đề "Phát hiện dữ liệu thuộc báo giá khác", nút đổi thành "Sao chép".\n'
            '• Sửa ô trực tiếp trên bảng xem trước → dòng về "Chưa validate", phải Validate lại.',
        dacbiet='Import theo kiểu tất cả hoặc không — không có "Bỏ dòng lỗi". Hàng ERP: tên, model, thương hiệu, xuất xứ, '
                'thông số, VAT, GIÁ NHẬP và GIÁ BÁN lấy theo ERP hiện hành, bỏ qua giá trong file. Hàng tạm: ô Đơn giá nhập '
                'trống = giữ giá nhập cũ. Danh mục mới (Model, Thương hiệu, Xuất xứ, Dịch vụ) được tạo thật ngay ở bước Import '
                'kể cả khi không bấm Lưu báo giá. Không giới hạn dung lượng / số dòng.'),
   ('- Quy tắc Excel và Cấu hình cột, Validate dữ liệu, Thông báo.', 'excel'),
   MENU_SUA + ' => Import Excel',
   [('11-import.png', 'Popup Import báo giá từ Excel sau khi Validate'),
    ('11b-import-phuong-thuc.png', 'Popup Chọn phương thức import')],
   [
       ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx, .xls', 'Có', 'Hiển thị', '- Chọn file khác → xoá kết quả cũ.'),
       ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị',
        L('- Không GG → import_baogia_khong_gg.xlsx (23 cột).', '- GG mặt hàng → import_baogia_gg_mat_hang.xlsx (thêm GG(%), GG(đ), Đơn giá sau GG).',
          '- GG tổng → import_baogia_gg_tong.xlsx (thêm khối "KHU VỰC CẤU HÌNH GIẢM GIÁ TỔNG").')),
       ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Disable', '- Bấm được khi đã chọn file.'),
       ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Disable', '- Bấm được khi bảng đã có dòng.'),
       ('Nút Chỉ dòng lỗi / Hiện tất cả', 'Button', 'Enable', '–', '–', 'Chỉ dòng lỗi', '- Lọc bảng xem trước.'),
       ('Dải thống kê', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        L('- "Tổng: N · Hợp lệ: N · Lỗi: N".', '- Link "Xem chi tiết N lỗi" → popup lỗi.', '- "Tạo mới danh mục: N" khi có danh mục sẽ tự tạo.')),
       ('Bảng xem trước', 'Table/Grid', 'Enable / Read-only', '–', '–', 'Trống',
        L('- Cột: # · Trạng thái · Loại * · Có tính doanh thu · Nhóm hàng cha (Cấp 1) · Nhóm hàng con (Cấp 2) · STT * · Mã hàng cha · '
          'Mã hàng * · Tên hàng * · Model · Thương hiệu * · Xuất xứ * · Thông số kỹ thuật · Ghi chú · ĐVT * · Số lượng * · Đơn Giá nhập · '
          'Thành tiền nhập · Đơn giá bán · Thành tiền bán · Tỷ suất lợi nhuận (%) · Thuế VAT (%) · Giá trị VAT · Thành tiền sau VAT.',
          '- Trạng thái dòng: Chưa validate (xám) · Hợp lệ (xanh) · Hợp lệ (tạo mới) (vàng) · Lỗi (đỏ).',
          '- Trống: “Chưa có dữ liệu. Chọn file Excel rồi bấm "Load lên bảng".”')),
       ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Disable',
        L('- Bấm được khi đã Validate, không còn lỗi.', '- Tooltip khi khoá: “Còn dòng lỗi — sửa file rồi Validate lại.” hoặc '
          '“Bấm Validate để kiểm tra dữ liệu trước khi Import.”')),
       ('Popup Chọn phương thức import', 'Modal', 'Hiển thị', '2 giá trị', 'Có', 'Import từng phần',
        L('- Import từng phần: “Giữ nguyên dòng đang có không xuất hiện trong file, cập nhật dòng khớp, thêm dòng mới.”',
          '- Thay thế hoàn toàn (chỉ báo giá tự nhập): “Xoá toàn bộ dòng đang có rồi đổ lại từ đầu theo file. Thao tác không thể hoàn tác.”',
          '- Báo giá từ BOM: chỉ có Từng phần.')),
       ('Nút Làm mới / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Làm mới: xoá sạch trạng thái popup.'),
   ], 'full',
   [
       ('Bấm Load lên bảng', 'Click',
        'During:\n– Đọc sheet đầu tiên, tìm dòng tiêu đề có "Tên hàng" và "Mã hàng"; bỏ 2 dòng hướng dẫn và dòng trống.\n'
        'After:\n– Hiện dữ liệu "Chưa validate".'),
       ('Bấm Validate', 'Click',
        'Before:\n– Báo giá phải Đang tạo: "Chỉ được import khi báo giá ở trạng thái Đang tạo."\n'
        'During:\n– Kiểm từng cột (Phần 4, BR-15), ví dụ: "STT tại dòng N không được để trống.", "STT x bị trùng lặp.", '
        '"Loại hạng mục tại dòng N không tồn tại trong hệ thống.", "Tên hàng tại dòng N không được để trống.", '
        '"Thương hiệu tại dòng N là bắt buộc với hàng tạm.", "ĐVT \'x\' tại dòng N không khớp với Master Data.", '
        '"Đơn giá bán tại dòng N không được để trống.", "GG(đ) tại dòng N không được lớn hơn đơn giá bán.", '
        '"Đơn giá bán của Cụm thiết bị tại dòng N không được nhỏ hơn tổng giá bán của các thiết bị thành phần.", '
        '"Chỉ được khai báo tối đa 1 dòng Chi phí vận chuyển."\n'
        '– Có lỗi → không thực hiện After; hiện "Phát hiện N lỗi dữ liệu. Sửa các dòng bôi đỏ trong file Excel rồi bấm Validate lại."\n'
        'After:\n– Chuẩn hoá dữ liệu (hàng ERP lấy theo danh mục), tính lại cột công thức; "Dữ liệu hợp lệ…".'),
       ('Bấm Import → chọn phương thức → Import', 'Click',
        'During:\n– Kiểm tra lại lần nữa; còn lỗi → dừng, KHÔNG tạo danh mục.\n'
        'After:\n– Tự tạo Model / Thương hiệu / Xuất xứ / Dịch vụ chưa có.\n'
        '– Đổ dữ liệu vào bảng chi tiết (Thay thế: dựng lại toàn bộ; Từng phần: khớp theo mã định danh ẩn, cập nhật / thêm mới; '
        'báo giá từ BOM: chỉ ghi đè giá nhập, giá bán, VAT, ghi chú, GG hàng tạm).\n'
        '– Chi phí vận chuyển và khoản GG tổng lấy theo file; GG tổng → yêu cầu phân bổ lại.\n'
        '– Đóng popup, thông báo đã nạp dữ liệu; chưa ghi báo giá cho tới khi Lưu.'),
   ])

# ------------------------------------------------------------- 2.16 Sao chép
fn('2.16', 'Sao chép báo giá', 'FR-16', 'crud', ACT_KD,
   dict(ten='Sao chép báo giá thành báo giá mới',
        mota='Tạo báo giá mới (Đang tạo) từ báo giá có sẵn ở mọi trạng thái; giá hàng ERP cập nhật theo giá hiện hành. '
             'Báo giá mới chỉ được tạo khi bấm Lưu nháp / Gửi duyệt.',
        tacnhan='Nhân viên kinh doanh (Sale phụ trách dự án / người lập)',
        dieukien=dk('Báo giá nguồn lập từ YCBG: cần Q1 hoặc Q2 (YCBG cùng phòng). Báo giá tự nhập có dự án: phải là Sale phụ '
                    'trách dự án. Báo giá không gắn dự án: phải là người lập. Q5 để thấy thay đổi giá vốn.',
                    'mọi trạng thái của báo giá nguồn.', 'báo giá nguồn nằm trong phạm vi dữ liệu V1–V4 của người dùng.'),
        chinh='1. Bấm Sao chép báo giá (danh sách) hoặc Sao chép (màn chi tiết).\n'
              '2. Hệ thống so dữ liệu báo giá nguồn với ERP hiện hành.\n'
              '3a. Không có thay đổi → mở thẳng màn Tạo báo giá đã điền sẵn.\n'
              '3b. Có thay đổi → popup "Phát hiện thay đổi dữ liệu từ ERP" → bấm "Xác nhận Sao chép báo giá".\n'
              '4. Màn Tạo báo giá hiện Mã "(Chưa tạo)" và dòng "Sao chép từ: <mã nguồn> — báo giá mới chỉ được tạo sau khi bấm Lưu".\n'
              '5. Người dùng chỉnh sửa như Tạo mới rồi Lưu nháp / Gửi duyệt (mục 2.13).',
        phu='• Không đủ điều kiện → "Chỉ người lập báo giá mới được sao chép." / "Bạn không phải Sale phụ trách dự án này" / '
            '"Không tìm thấy báo giá."\n'
            '• Lỗi kiểm tra → "Không kiểm tra được thay đổi từ ERP"; lỗi tải → "Không tải được dữ liệu sao chép" và quay về danh sách.\n'
            '• Rời màn khi chưa lưu → hệ thống hỏi xác nhận rời trang.\n'
            '• Đổi Dự án trên bản sao → hỏi "Xác nhận đổi Dự án"; GIỮ hàng hoá, dịch vụ, giảm giá; lấy lại khách hàng, tiền tệ, '
            'bảng giá theo dự án mới. Chỉ liệt kê dự án chưa có BOM tổng hợp đã duyệt.',
        dacbiet='KHI GIÁ THAY ĐỔI: hàng ERP luôn lấy giá vốn + giá bán ERP hiện hành (theo Bảng giá, ĐVT của dòng, tỷ giá hiện '
                'hành) và VAT ERP hiện hành — người dùng KHÔNG chọn giữ giá cũ được; hàng tạm giữ nguyên giá, VAT, mã; dịch vụ giữ '
                'giá bán, giá vốn tính lại theo tỷ lệ danh mục; GG mặt hàng giữ vế đã nhập (% hoặc ₫); GG tổng tự phân bổ lại. '
                'Khi Lưu, hệ thống lấy lại giá ERP hiện hành một lần nữa. Bản sao luôn là báo giá tự nhập, không kế thừa YCBG, '
                'Ghi chú kinh doanh, thông tin duyệt, lịch sử.'),
   ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   MENU + ' => Sao chép báo giá',
   [('10-sao-chep.png', 'Màn Tạo báo giá điền sẵn từ báo giá BG-2026-00098')],
   [
       ('Nút Sao chép báo giá / Sao chép', 'Icon Button / Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
        L('- Danh sách: icon trong cột Hành động.', '- Màn chi tiết: nút ở chân trang, đang xử lý "Đang sao chép...".')),
       ('Popup Phát hiện thay đổi dữ liệu từ ERP', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
        L('- Dòng phụ: “Báo giá này kế thừa cấu trúc từ <mã nguồn>. Hệ thống đã tự động cập nhật giá mới nhất và phát hiện các thay đổi sau”.',
          '- Cột: Loại thay đổi · Mã / Tên vật tư · Thông tin cũ (V1) · Thông tin mới (Cập nhật) · Hành động hệ thống.',
          '- Loại "Thay đổi giá": 2 dòng "<tên> (Giá vốn)" (chỉ người có Q5 thấy) và "<tên> (Giá bán)" → "Đã cập nhật giá mới".',
          '- Loại "Thay đổi VAT" → "Đã cập nhật VAT mới".',
          '- Loại "Thay đổi cấu trúc" (combo ERP đổi vật tư con) → "(Bỏ qua) — Giữ nguyên cấu trúc V1".',
          '- Nút "Xác nhận Sao chép báo giá" / "Hủy bỏ".')),
       ('Dòng Sao chép từ', 'Text', 'Read-only', '–', '–', '<mã nguồn>', '- Chỉ có ở bản sao.'),
       ('Dự án (bản sao)', 'Dropdown', 'Enable', 'Dự án chưa có BOM tổng hợp đã duyệt', 'Không', 'Dự án nguồn',
        '- Gợi ý: “Báo giá sao chép — đổi Dự án giữ nguyên hàng hoá, dịch vụ và giảm giá đã sao chép, chỉ lấy lại khách hàng, tiền tệ và bảng giá theo dự án mới…”'),
       ('Các trường còn lại', 'Theo mục 2.3 – 2.12', 'Enable', '–', 'Theo mục 2.3', 'Theo báo giá nguồn', '- Như màn Tạo mới.'),
   ], 'full',
   [
       ('Bấm Sao chép báo giá', 'Click',
        'Before:\n– Kiểm phạm vi dữ liệu và điều kiện sao chép.\n' + NO_PERM + '\n'
        'During:\n– So giá vốn, giá bán, VAT, cấu trúc combo của báo giá nguồn với ERP hiện hành.\n'
        'After:\n– Không có thay đổi → mở màn Tạo báo giá điền sẵn; có thay đổi → popup.'),
       ('Bấm Xác nhận Sao chép báo giá', 'Click',
        'After:\n– Mở màn Tạo báo giá điền sẵn (chưa ghi vào hệ thống).'),
       ('Bấm Lưu nháp / Gửi duyệt trên bản sao', 'Click',
        'After:\n– Tạo báo giá mới Đang tạo, ghi vết nguồn sao chép trong lịch sử "Tạo mới"; xử lý tiếp như mục 2.13.'),
   ])

# ------------------------------------------------------------- 2.17 Xóa
fn('2.17', 'Xóa báo giá', 'FR-17', 'action', ACT_KD,
   dict(ten='Xóa báo giá',
        mota='Xoá hẳn báo giá đang ở trạng thái Đang tạo do chính mình lập.',
        tacnhan='Nhân viên kinh doanh (người lập)',
        dieukien=dk('không cần quyền riêng; phải là NGƯỜI LẬP báo giá.', 'Đang tạo.',
                    'báo giá đã gửi duyệt / đã duyệt / đóng / dừng / trúng thầu không xoá được (nút bị ẩn).'),
        chinh='1. Bấm Xóa (cột Hành động) hoặc Xoá (chân trang màn chi tiết).\n'
              '2. Hệ thống hỏi "Xác nhận xoá": “Bạn có chắc muốn xoá báo giá \'<Mã>\'?”.\n'
              '3. Bấm Xoá → hệ thống xoá báo giá, thông báo "Đã xoá báo giá".\n'
              '4. Ở danh sách: tải lại danh sách; ở màn chi tiết: quay về danh sách.',
        phu='• Bấm Huỷ → đóng hộp thoại, không xoá.\n'
            '• Báo giá đã đổi trạng thái / không phải người lập → "Báo giá không ở trạng thái Đang tạo, không thể sửa." / '
            '"Chỉ người tạo báo giá mới có thể sửa."; lỗi khác → "Xoá thất bại".',
        dacbiet='Xoá cứng, không khôi phục được; xoá kèm toàn bộ dòng hàng hoá và lịch sử của báo giá. Báo giá lập từ YCBG mà YCBG '
                'không còn báo giá nào khác → YCBG quay về trạng thái "Chờ XD giá".'),
   ('- Thông báo / Quy tắc Xóa.', 'delete'),
   MENU + ' => Xóa',
   [('09-xoa.png', 'Hộp thoại Xác nhận xoá báo giá')],
   [
       ('Nút Xóa (danh sách) / Xoá (chi tiết)', 'Icon Button / Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện',
        L('- Màu đỏ.', '- Chỉ hiện khi Đang tạo và là người lập; cùng điều kiện ở 2 nơi.')),
       ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xoá', '–'),
       ('Nội dung', 'Label', 'Hiển thị', 'Bạn có chắc muốn xoá báo giá \'<Mã>\'?', '- Mã báo giá trong dấu nháy đơn.'),
       ('Nút Xoá', 'Button', 'Enable', 'Hiển thị', '- Màu đỏ; bấm → thực hiện xoá.'),
       ('Nút Huỷ', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp thoại.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn', L('- Thành công: "Đã xoá báo giá".', '- Lỗi: thông báo của hệ thống hoặc "Xoá thất bại".')),
   ], 'confirm',
   [
       ('Bấm Xóa', 'Click', 'After:\n– Mở hộp thoại Xác nhận xoá.'),
       ('Bấm Xoá trong hộp thoại', 'Click',
        'Before:\n– Kiểm trạng thái Đang tạo và người lập.\n– Không đủ → hiện thông báo tương ứng và dừng xử lý.\n'
        'After:\n– Xoá dòng hàng hoá, lịch sử và báo giá; trả YCBG về "Chờ XD giá" nếu không còn báo giá nào.\n'
        '– Thông báo "Đã xoá báo giá"; tải lại danh sách / quay về danh sách.'),
   ])

# ------------------------------------------------------------- 2.18 Duyệt
fn('2.18', 'Duyệt báo giá', 'FR-18', 'action', ACT_TP,
   dict(ten='Duyệt báo giá (Trưởng phòng / Ban giám đốc)',
        mota='Trưởng phòng duyệt báo giá cấp 2 (→ Đã duyệt) hoặc duyệt & chuyển BGĐ báo giá cấp 3; Ban giám đốc duyệt báo giá '
             'đang Chờ BGĐ duyệt. Màn "Báo giá chờ duyệt" liệt kê báo giá đang chờ chính người dùng duyệt.',
        tacnhan='Trưởng phòng; Ban giám đốc',
        dieukien=dk('Q3 "Trưởng phòng duyệt giá Bom giải pháp" (báo giá thuộc phòng ban mình quản lý) hoặc Q4 "Ban giám đốc '
                    'duyệt giá Bom giải pháp" (báo giá thuộc công ty mình).',
                    'Chờ TP duyệt (Q3) / Chờ BGĐ duyệt (Q4).', 'không áp cho báo giá tổng (có luồng duyệt riêng).'),
        chinh='1. Người duyệt mở thông báo hoặc vào menu Phân hệ Bán hàng → Phê Duyệt → Dự án TKT → Báo giá chờ duyệt.\n'
              '2. Bấm Duyệt trên dòng (hoặc Mã báo giá) → mở màn Xem chi tiết.\n'
              '3. Bấm Duyệt / Duyệt & chuyển BGĐ / BGĐ duyệt ở chân trang.\n'
              '4. Hệ thống hỏi "Xác nhận duyệt" → bấm Duyệt.\n'
              '5. Cấp 2 (TP) hoặc BGĐ duyệt → trạng thái Đã duyệt; cấp 3 (TP) → Chờ BGĐ duyệt.\n'
              '6. Thông báo kết quả, quay về màn Báo giá chờ duyệt.',
        phu='• Trưởng phòng khác phòng / BGĐ khác công ty vẫn thấy nút nhưng bấm sẽ báo "Bạn không quản lý phòng ban của báo giá '
            'này." / "Bạn không thuộc công ty của báo giá này."\n'
            '• Báo giá đã được người khác xử lý → "Báo giá không ở trạng thái Chờ TP duyệt." / "… Chờ BGĐ duyệt."\n'
            '• Không có quyền mà vào màn Báo giá chờ duyệt → hệ thống từ chối truy cập.\n'
            '• Đồng bộ ERP thất bại không chặn việc duyệt; cột Đồng bộ ERP hiện "Thất bại".',
        dacbiet='Sau khi Đã duyệt: YCBG (nếu có) → "Đã có báo giá"; Dự án TKT → tiến trình "Thương thảo giá"; giải pháp → "Đã duyệt '
                'giá"; báo giá được đồng bộ sang ERP thành báo giá chính thức. Báo giá Đã duyệt không sửa được.'),
   ('- Màn Xem chi tiết và Phân quyền, Thông báo. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
    'detail'),
   MENU_DUYET,
   [('12c-cho-duyet.png', 'Màn Báo giá chờ duyệt'),
    ('12-duyet.png', 'Hộp thoại Xác nhận duyệt ở màn Xem chi tiết')],
   [
       ('Ô tìm nhanh (màn chờ duyệt)', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- "Tìm theo mã báo giá, tên khách hàng".'),
       ('Bộ lọc (màn chờ duyệt)', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
        L('- Công ty / Phòng ban / Bộ phận / Người lập · Dự án TKT · Giai đoạn dự án · Ngày tạo.',
          '- Cấp duyệt: Cấp 2 — TP duyệt · Cấp 3 — TP & BGĐ duyệt.', '- Không có ô Trạng thái.')),
       ('Bảng Báo giá chờ duyệt', 'Table/Grid', 'Read-only', '–', '–', 'Sắp Ngày gửi duyệt mới nhất',
        L('- Nhãn "Tổng: N".', '- Cột: STT · Mã báo giá · Loại báo giá · Mã - Tên BOM list · Dự án TKT · Khách hàng · Giai đoạn dự án · '
          'Tiền tệ · Tổng giá trị sau VAT · Cấp duyệt · Người gửi duyệt · Ngày gửi duyệt · Ngày tạo · Người cập nhật · Ngày cập nhật · '
          'Trạng thái · Hành động.', '- Rỗng: "Không có báo giá nào chờ duyệt."')),
       ('Nút Duyệt (dòng)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Mở màn Xem chi tiết để duyệt (không duyệt ngay tại dòng).'),
       ('Nút Duyệt / Duyệt & chuyển BGĐ (chi tiết)', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
        L('- Hiện khi có Q3 và Chờ TP duyệt.', '- Cấp 3: chữ "Duyệt & chuyển BGĐ"; cấp 2: "Duyệt".')),
       ('Nút BGĐ duyệt (chi tiết)', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Hiện khi có Q4 và Chờ BGĐ duyệt.'),
       ('Hộp thoại Xác nhận duyệt', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
        L('- Nội dung: "Duyệt báo giá?" (cấp 2) · "Duyệt & chuyển BGĐ?" (cấp 3) · "BGĐ duyệt báo giá?".', '- Nút Duyệt / Huỷ.')),
   ], 'full',
   [
       ('Bấm Duyệt (TP)', 'Click',
        'Before:\n– Kiểm Q3, phòng ban báo giá thuộc phòng mình quản lý, trạng thái Chờ TP duyệt.\n'
        '– Không đủ → thông báo tương ứng và dừng xử lý.\n'
        'After:\n– Cấp 3: "Chờ BGĐ duyệt", lưu người / ngày TP duyệt; lịch sử "TP duyệt & chuyển BGĐ"; thông báo '
        '“<Tên TP> TP đã duyệt & chuyển BGĐ <Mã>” tới người có Q4 của công ty báo giá.\n'
        '– Cấp 2: "Đã duyệt"; lịch sử "TP duyệt"; cập nhật YCBG, dự án, giải pháp; đồng bộ ERP; thông báo '
        '“<Tên> đã duyệt báo giá <Mã>” tới người lập, Sale phụ trách dự án, Trưởng phòng duyệt giá của phòng.\n'
        '– Thông báo "Đã duyệt báo giá"; lỗi "Lỗi duyệt".'),
       ('Bấm BGĐ duyệt', 'Click',
        'Before:\n– Kiểm Q4, công ty báo giá = công ty mình, trạng thái Chờ BGĐ duyệt.\n'
        'After:\n– "Đã duyệt"; lịch sử "BGĐ duyệt"; tác động như duyệt cấp 2; thông báo "BGĐ đã duyệt báo giá".'),
   ])

# ------------------------------------------------------------- 2.19 Từ chối
fn('2.19', 'Từ chối báo giá', 'FR-19', 'action', ACT_TP,
   dict(ten='Từ chối báo giá',
        mota='Trưởng phòng / Ban giám đốc từ chối báo giá đang chờ mình duyệt; báo giá quay về Đang tạo để người lập sửa và gửi lại.',
        tacnhan='Trưởng phòng; Ban giám đốc',
        dieukien=dk('Q3 (báo giá Chờ TP duyệt, thuộc phòng mình quản lý) hoặc Q4 (báo giá Chờ BGĐ duyệt, thuộc công ty mình).',
                    'Chờ TP duyệt / Chờ BGĐ duyệt.', 'bắt buộc nhập lý do từ chối.'),
        chinh='1. Ở màn Xem chi tiết bấm Từ chối.\n'
              '2. Hệ thống mở popup "Từ chối báo giá".\n'
              '3. Người duyệt nhập Lý do từ chối và bấm Xác nhận từ chối.\n'
              '4. Báo giá về "Đang tạo", xoá cấp duyệt và thông tin duyệt; thông báo "Đã từ chối báo giá"; quay về màn trước.',
        phu='• Lý do trống / chỉ có khoảng trắng → "Vui lòng nhập lý do từ chối".\n'
            '• Lý do > 1.000 ký tự → hệ thống báo lỗi độ dài.\n'
            '• Lỗi khác → "Không thể từ chối".',
        dacbiet='Không có trạng thái "Từ chối" riêng. Người lập mở lại báo giá thấy dải đỏ “Đã bị từ chối: <lý do>”; lý do bị xoá khi '
                'gửi duyệt lại. Cấp duyệt được tính lại từ đầu ở lần gửi sau.'),
   ('- Màn Xem chi tiết và Phân quyền, Thông báo. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
    'detail'),
   MENU_DUYET + ' => Từ chối',
   [('12b-tu-choi.png', 'Popup Từ chối báo giá')],
   [
       ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Hiện khi (Q3 và Chờ TP duyệt) hoặc (Q4 và Chờ BGĐ duyệt).'),
       ('Lý do từ chối', 'Textarea', 'Enable', '1–1.000 ký tự', 'Có', 'Trống',
        L('- Placeholder "Nhập lý do từ chối...".', '- Thiếu: "Vui lòng nhập lý do từ chối".')),
       ('Nút Xác nhận từ chối', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Màu đỏ; đang gửi: "Đang gửi...".'),
       ('Nút Huỷ', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup.'),
   ], 'full',
   [
       ('Bấm Xác nhận từ chối', 'Click',
        'Before:\n– Kiểm quyền + phòng ban / công ty + trạng thái chờ duyệt: "Báo giá không ở trạng thái chờ duyệt."\n'
        'During:\n– Lý do trống → "Vui lòng nhập lý do từ chối"; có lỗi → không thực hiện After.\n'
        'After:\n– Trạng thái "Đang tạo"; lưu lý do; xoá ngày gửi duyệt, người / ngày duyệt, cấp duyệt.\n'
        '– Lịch sử "Từ chối" kèm lý do.\n'
        '– Thông báo “<Tên> từ chối báo giá <Mã>. Lý do: <lý do>” tới người lập (từ chối ở bước BGĐ: thêm TP đã duyệt trước đó).\n'
        '– Thông báo "Đã từ chối báo giá", quay về màn trước.'),
   ])

# ------------------------------------------------------------- 2.20 Xem chi tiết
fn('2.20', 'Xem chi tiết báo giá', 'FR-20', 'view', ACT_KD,
   dict(ten='Xem chi tiết báo giá',
        mota='Hiển thị toàn bộ báo giá ở chế độ chỉ đọc và các thao tác theo trạng thái ở chân trang.',
        tacnhan='Nhân viên kinh doanh, Trưởng phòng, Ban giám đốc; Người dùng đã đăng nhập',
        dieukien=dk('không cần quyền riêng; báo giá trong phạm vi V1–V4 hoặc đang chờ chính mình duyệt. Q5 để thấy giá vốn.',
                    'mọi trạng thái.', 'không.'),
        chinh='1. Bấm Mã báo giá ở danh sách / màn chờ duyệt / tab Báo giá của Dự án TKT.\n'
              '2. Hệ thống hiển thị: Thông tin chung → Chi tiết báo giá (A Hàng hoá, B Dịch vụ & Chi phí khác, TỔNG) → '
              'Giảm giá tổng đơn hàng → Tổng hợp giá trị báo giá → Điều khoản / Ghi chú → Lịch sử.\n'
              '3. Chân trang hiện các nút theo trạng thái và vai trò.',
        phu='• Ngoài phạm vi → "Không tìm thấy báo giá."; lỗi tải → "Không tải được báo giá".\n'
            '• Báo giá bị từ chối → dải đỏ “Đã bị từ chối: <lý do>”.\n'
            '• Báo giá Đã duyệt: Sale phụ trách dự án sửa được Ghi chú Kinh doanh (nút "Lưu ghi chú" → "Đã lưu ghi chú").',
        dacbiet=None),
   ('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Báo giá.', 'detail'),
   MENU + ' => Mã báo giá',
   [('13-chi-tiet.png', 'Màn Chi tiết báo giá đang Chờ TP duyệt')],
   [
       ('Tiêu đề', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
        L('- "Chi tiết báo giá: <Mã> (<Trạng thái>) <Cấp duyệt>".', '- Cấp duyệt: "Cấp 1 — Tự duyệt" / "Cấp 2 — TP duyệt" / "Cấp 3 — TP & BGĐ duyệt".')),
       ('Khối Thông tin chung', 'Text', 'Read-only', '–', 'Mở rộng',
        L('- Đầu khối: "Người lập: … · Ngày tạo: …".', '- Mã báo giá · YCBG · BOM list · Dự án · Giải pháp · Hạng mục (ẩn với báo giá tự nhập).',
          '- Khách hàng · MST · Người liên hệ · SĐT · Địa chỉ · Email · Hiệu lực báo giá · Giao hàng (ngày) · Bảo hành (tháng).',
          '- Loại tiền tệ (ngoại tệ kèm tỷ giá) + chip "Bảng giá: …" · Giai đoạn dự án (icon ⓘ: “<mô tả giai đoạn>”) · Ngày lập · Người lập · Ghi chú yêu cầu.')),
       ('Khối Chi tiết báo giá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        L('- Cột như bảng chi tiết (mục 2.9), thêm cột GG theo phương thức.', '- Badge Giảm giá: "GG theo mặt hàng" / "GG theo tổng" / "Không áp dụng".',
          '- Giá nhập, Thành tiền nhập, Tỷ suất LN hiện "—" khi không có Q5.', '- Nút Thu gọn tất cả, Ẩn cột chi tiết.')),
       ('Khối Giảm giá tổng đơn hàng', 'Table/Grid', 'Read-only', '–', 'Ẩn', '- Chỉ khi GG tổng: Loại GG · Giá trị · Tổng GG.'),
       ('Khối Tổng hợp giá trị báo giá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Như mục 2.10; TSLN trước / sau GG khi có Q5.'),
       ('Khối Điều khoản / Ghi chú nội bộ / Ghi chú Kinh doanh', 'Text / Textarea', 'Read-only / Enable', '–', 'Theo dữ liệu',
        L('- Điều khoản đã thay biến {{...}}.', '- Ghi chú nội bộ: chỉ hiện khi có nội dung.',
          '- Ghi chú Kinh doanh: chỉ khi Đã duyệt; Sale phụ trách dự án sửa được.')),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút "Xem lịch sử" → mục 2.24.'),
       ('Chân trang', 'Button', 'Enable / Ẩn', '–', 'Theo trạng thái',
        L('- Quay lại · Xuất Excel (mục 2.23) · In (mục 2.21): luôn hiện.', '- Sao chép: đủ điều kiện sao chép (mục 2.16).',
          '- Sửa / Làm giá, Xoá: Đang tạo + người lập.', '- Duyệt / Duyệt & chuyển BGĐ / BGĐ duyệt / Từ chối: mục 2.18, 2.19.',
          '- Chốt báo giá (Trúng thầu) / Hủy chốt / Lập hợp đồng / Xem hợp đồng: như cột Hành động màn danh sách.')),
   ], 'ro',
   [
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm báo giá trong phạm vi xem hoặc đang chờ mình duyệt; không → "Không tìm thấy báo giá."\n'
        'After:\n– Hiển thị dữ liệu, ẩn giá vốn nếu không có Q5; hiện nút chân trang theo điều kiện.'),
       ('Bấm nút chân trang', 'Click', 'After:\n– Chuyển sang chức năng tương ứng (mục 2.14 – 2.24).'),
       ('Bấm Quay lại', 'Click', 'After:\n– Về trang trước; mở thẳng thì về Danh sách báo giá.'),
   ], uc=False)

# ------------------------------------------------------------- 2.21 In
fn('2.21', 'In báo giá', 'FR-21', 'io', ACT_KD,
   dict(ten='In báo giá gửi khách hàng',
        mota='Chọn cột hiển thị, xem trước và in báo giá khổ A4 ngang (không có giá vốn).',
        tacnhan='Nhân viên kinh doanh; Người dùng đã đăng nhập',
        dieukien=dk('không cần quyền riêng.', 'mọi trạng thái.', 'báo giá nằm trong phạm vi xem.'),
        chinh='1. Bấm In báo giá (cột Hành động) hoặc In (chân trang màn chi tiết).\n'
              '2. Hệ thống mở popup "Cấu hình in báo giá".\n'
              '3. Người dùng tích / bỏ "Hiện hàng hoá cấp con", chọn cột hiển thị, bấm Xem trước.\n'
              '4. Hệ thống mở popup "Xem trước báo giá"; bấm In → mở cửa sổ in, tự bật hộp thoại in.',
        phu='• Không chọn cột nào → "Vui lòng chọn ít nhất 1 cột để in".\n'
            '• Lỗi tải dữ liệu từ danh sách → "Không tải được chi tiết báo giá".',
        dacbiet='Bản in luôn ẩn giá vốn (Giá nhập, Thành tiền nhập, TSLN). Letterhead hiện lấy theo công ty của người đang đăng nhập. '
                'Điều khoản in đã thay biến {{...}}; mục "Ghi chú:" in Ghi chú Kinh doanh; Ghi chú nội bộ KHÔNG in.'),
   ('- Thông báo và UI/UX.', 'notice'),
   MENU + ' => In báo giá',
   [('15-cau-hinh-in.png', 'Popup Cấu hình in báo giá'),
    ('15b-xem-truoc-in.png', 'Popup Xem trước báo giá')],
   [
       ('Hiện hàng hoá cấp con', 'Checkbox', 'Enable', '–', 'Không', 'Tích', '- Bỏ tích → không in dòng hàng con.'),
       ('Chọn cột hiển thị', 'Checkbox', 'Enable', 'Danh sách cột', 'Có (≥ 1 cột)', 'Tích tất cả trừ Mã hàng hoá',
        L('- Cột: STT · Tên hàng hoá · Mã hàng hoá · Model · Thương hiệu · Xuất xứ · Đơn vị tính · Thông số kỹ thuật · Ghi chú · Số lượng · '
          'Đơn giá bán · Thành tiền bán · [GG (%) · GG (₫) · Đơn giá sau GG | GG phân bổ] · VAT (%) · Tiền VAT · Thành tiền sau VAT · Hình ảnh · '
          'Thời gian bảo hành.', '- Ô "Chọn tất cả".')),
       ('Nút Huỷ / Xem trước', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Bản xem trước', 'Modal', 'Read-only', 'A4 ngang', '–', 'Ẩn',
        L('- Letterhead công ty; tiêu đề "BÁO GIÁ HÀNG HÓA".',
          '- Trái: Kính gửi (ông/bà) · Tên đơn vị · Địa chỉ · Điện thoại/ Email · Hiệu lực báo giá "Đến ngày …" · Bảo hành.',
          '- Phải: Báo giá số · Dự án · Ngày · Đại diện kinh doanh/ Email · Giao hàng (ngày) · Loại tiền tệ.',
          '- Bảng hàng hoá theo nhóm, khối "Dịch vụ & Chi phí khác", dòng "TỔNG CỘNG".',
          '- Bảng tổng hợp giá trị (không có Thành tiền nhập); "Điều khoản báo giá:"; "Ghi chú:"; chữ ký "ĐẠI DIỆN KINH DOANH".')),
       ('Nút In', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Mở cửa sổ in, chờ ảnh tải (tối đa 3 giây) rồi bật hộp thoại in.'),
   ], 'full',
   [
       ('Bấm In báo giá / In', 'Click', 'After:\n– Mở popup Cấu hình in báo giá.'),
       ('Bấm Xem trước', 'Click',
        'During:\n– Không chọn cột → "Vui lòng chọn ít nhất 1 cột để in" và dừng.\nAfter:\n– Mở bản xem trước.'),
       ('Bấm In', 'Click', 'After:\n– Mở cửa sổ in tiêu đề "Báo giá <Mã>", tự bật hộp thoại in của trình duyệt.'),
   ])

# ------------------------------------------------------------- 2.22 Xuất Excel danh sách
fn('2.22', 'Xuất Excel danh sách báo giá', 'FR-22', 'io', ACT_KD,
   dict(ten='Xuất danh sách báo giá ra file Excel',
        mota='Xuất toàn bộ báo giá khớp bộ lọc hiện tại (trong phạm vi quyền) với các trường người dùng chọn.',
        tacnhan='Nhân viên kinh doanh, Trưởng phòng, Ban giám đốc; Người dùng đã đăng nhập',
        dieukien=dk('không cần quyền riêng; phạm vi theo V1–V4.', 'mọi trạng thái.', 'không.'),
        chinh='1. Ở màn danh sách bấm Xuất Excel.\n'
              '2. Hệ thống mở popup "Chọn trường xuất file" (tích sẵn các cột đang hiện).\n'
              '3. Người dùng tích / bỏ trường, kéo đổi thứ tự rồi bấm Xuất file.\n'
              '4. Hệ thống tải file danh_sach_bao_gia.xlsx, thông báo "Xuất Excel thành công".',
        phu='• Lỗi → "Lỗi khi xuất Excel".\n• Không chọn trường nào → xuất đủ mọi cột.\n'
            '• Màn Báo giá chờ duyệt có nút Xuất Excel riêng → file danh_sach_bao_gia_cho_duyet.xlsx.',
        dacbiet='Xuất mọi dòng khớp bộ lọc, không phân trang. Ô số là số thật, định dạng 1,234,567.'),
   ('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   MENU + ' => Xuất Excel',
   [('16-xuat-excel-ds.png', 'Popup Chọn trường xuất file')],
   [
       ('Popup Chọn trường xuất file', 'Modal', 'Hiển thị', '20 trường', '–', 'Ẩn',
        L('- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”',
          '- Trường: Mã báo giá · Loại báo giá · Mã BOM · Mã YCBG · Dự án TKT · Khách hàng · Giai đoạn dự án · Tiền tệ · Tổng giá trị sau VAT · '
          'Cấp duyệt · Người duyệt · Ngày duyệt · Trạng thái đồng bộ ERP · Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật · Trạng thái · '
          'Tên báo giá · Version giải pháp.', '- Dòng đếm "Đang chọn X/20 trường".')),
       ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Checkbox trường', 'Checkbox', 'Enable', '–', 'Không', 'Các cột đang hiện', '- Kéo thả đổi thứ tự.'),
       ('Nút Xuất file / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ], 'full',
   [
       ('Bấm Xuất file', 'Click',
        'Before:\n– Áp bộ lọc hiện tại + phạm vi V1–V4.\nAfter:\n– Tải file danh_sach_bao_gia.xlsx (sheet "Danh sách báo giá"); '
        'thông báo "Xuất Excel thành công".'),
   ])

# ------------------------------------------------------------- 2.23 Xuất Excel chi tiết
fn('2.23', 'Xuất Excel chi tiết báo giá', 'FR-23', 'io', ACT_KD,
   dict(ten='Xuất 1 báo giá ra file Excel theo khuôn file mẫu Import',
        mota='Xuất toàn bộ hàng hoá, dịch vụ, vận chuyển, giảm giá tổng của 1 báo giá theo đúng khuôn file mẫu Import để có thể '
             'sửa rồi import lại.',
        tacnhan='Nhân viên kinh doanh; Người dùng đã đăng nhập',
        dieukien=dk('không cần quyền riêng; Q5 để file có giá vốn (người lập không có Q5 chỉ thấy giá vốn hàng tạm / dịch vụ / '
                    'vận chuyển).', 'mọi trạng thái.', 'báo giá trong phạm vi xem; màn Tạo mới không có nút.'),
        chinh='1. Bấm Xuất Excel ở chân trang màn Xem chi tiết hoặc thanh tiêu đề bảng ở màn Làm giá.\n'
              '2. Hệ thống tải file "<Mã báo giá>_DD-MM-YYYY.xlsx".',
        phu='• Lỗi → "Không xuất được file Excel. Vui lòng thử lại."\n• Đang xuất: nút đổi "Đang xuất..." và khoá.',
        dacbiet='File không có logo / thông tin khách hàng / chữ ký — chỉ bảng dữ liệu. Có 2 cột Hình ảnh (ảnh nhúng) và Thời gian bảo '
                'hành; 3 cột ẩn định danh dùng cho Import từng phần. Cột Thành tiền, Tỷ suất, VAT là công thức Excel thật.'),
   ('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   MENU + ' => Mã báo giá => Xuất Excel',
   [('13-chi-tiet.png', 'Nút Xuất Excel ở chân trang màn Chi tiết báo giá')],
   [
       ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Luôn hiện ở màn chi tiết; màn Làm giá: hiện khi không phải Tạo mới.'),
       ('Khối Giảm giá tổng (file)', 'Table/Grid', 'Read-only', '–', '–', 'Chỉ GG tổng',
        '- "KHU VỰC CẤU HÌNH GIẢM GIÁ TỔNG": STT · Loại GG · Kiểu · Giá trị · Thành tiền GG.'),
       ('Khối hàng hoá – dịch vụ (file)', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        L('- Cột như file mẫu Import (mục 2.15) + Hình ảnh + Thời gian bảo hành.',
          '- Thứ tự: nhóm cha → nhóm con → hàng cha → hàng con; tiếp theo dịch vụ, rồi Chi phí vận chuyển (nếu > 0).',
          '- Không có Q5: Đơn Giá nhập, Thành tiền nhập, Tỷ suất để trống (trừ dòng người lập tự nhập).')),
   ], 'full',
   [
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Kiểm báo giá trong phạm vi xem; không → "Không tìm thấy báo giá."\n'
        'After:\n– Dựng file theo phương thức GG của báo giá, ẩn giá vốn theo quyền, tải file.'),
   ])

# ------------------------------------------------------------- 2.24 Lịch sử
fn('2.24', 'Xem lịch sử báo giá', 'FR-24', 'view', ACT_KD,
   dict(ten='Xem lịch sử thao tác của báo giá',
        mota='Dòng thời gian các lần tạo, thay đổi thông tin, chuyển trạng thái của báo giá, kèm giá trị cũ → mới.',
        tacnhan='Nhân viên kinh doanh, Trưởng phòng, Ban giám đốc; Người dùng đã đăng nhập',
        dieukien=dk('không cần quyền riêng; Q5 để thấy thay đổi Giá nhập.', 'mọi trạng thái.', 'báo giá trong phạm vi xem.'),
        chinh='1. Bấm Lịch sử ở cột Hành động (popup "Lịch sử báo giá: <Mã>") hoặc "Xem lịch sử" ở khối Lịch sử màn chi tiết.\n'
              '2. Hệ thống hiển thị dòng thời gian, mới nhất trên cùng.\n'
              '3. Người dùng lọc theo Loại hành động, Người thực hiện, Từ ngày / Đến ngày.',
        phu='• Chưa có lịch sử → "Chưa có lịch sử thao tác nào."; lọc không khớp → "Không có lịch sử phù hợp bộ lọc."\n'
            '• Lỗi tải → "Không tải được lịch sử." + nút Thử lại.',
        dacbiet=None),
   ('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Báo giá.', 'history'),
   MENU + ' => Lịch sử',
   [('14-lich-su.png', 'Popup Lịch sử báo giá')],
   [
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Lịch sử báo giá: <Mã>', '–'),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Thu gọn', '- Bung / thu vùng lọc; chọn là lọc ngay.'),
       ('Ô Loại hành động', 'Dropdown', 'Enable', '3 giá trị', 'Trống', L('- Lựa chọn: Tạo mới · Thay đổi thông tin · Thay đổi trạng thái.')),
       ('Ô Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Trống', '- "Tên - Mã phòng - Mã NV".'),
       ('Ô Từ ngày / Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '–'),
       ('Mục lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        L('- Thời gian dd/mm/yyyy HH:mm · nhãn hành động (tô màu) · "Người thực hiện: <tên> — <phòng ban>".',
          '- Nhãn: Tạo mới · Thay đổi thông tin · Gửi duyệt · Tự duyệt · TP duyệt · TP duyệt & chuyển BGĐ · BGĐ duyệt · Từ chối · Chốt · '
          'Hủy chốt · Cập nhật ghi chú KD · Đóng theo dự án.',
          '- Trường đơn: "<Trường>: <cũ (đỏ)> → <mới (xanh)>".',
          '- Bảng con: "<Bảng> thêm mới:", "<Bảng> đã xóa:", "<Bảng> sửa thông tin:" (Nhóm hàng hoá, Hàng hoá, Dịch vụ & Chi phí khác, Giảm giá tổng đơn hàng).',
          '- Ghi chú / lý do (từ chối, hủy chốt) kèm icon bình luận.')),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–'),
   ], 'ro',
   [
       ('Bấm Lịch sử / Xem lịch sử', 'Click',
        'After:\n– Tải và hiển thị lịch sử; bỏ Giá nhập, Giá nhập vận chuyển nếu người xem không có Q5.'),
       ('Chọn ô lọc', 'Change', 'After:\n– Lọc ngay danh sách lịch sử.'),
   ], uc=False)

# ==================================================== PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Báo giá; công thức chi tiết ở Phụ lục – Bảng đính kèm.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Chỉ người lập sửa / xoá / gửi duyệt', [
        '– Sửa, Xoá, Gửi duyệt, Tự duyệt, Import chỉ khi báo giá "Đang tạo" và người thao tác là người lập.',
        '– Báo giá đã gửi duyệt / đã duyệt không sửa được; muốn thay đổi thì Sao chép.',
        '– Bị Từ chối → quay về "Đang tạo", người lập sửa và gửi lại.'],
     ['Chỉnh sửa', 'Xóa', 'Gửi duyệt', 'Import']),
    ('BR-02', 'Ai được lập báo giá', [
        '– Gắn dự án: chỉ Sale phụ trách dự án; dự án cha không lập báo giá riêng.',
        '– Từ YCBG: dự án theo phòng cần Q2 + YCBG cùng phòng; dự án liên phòng cần Q1.',
        '– Không gắn dự án: mọi người vào được màn, bắt buộc chọn khách hàng.'], ['Tạo mới', 'Sao chép']),
    ('BR-03', 'Phạm vi dữ liệu', [
        '– Xét V1 → V4, có quyền nào dừng ở đó; luôn cộng báo giá do mình lập.',
        '– Không có quyền nào → chỉ báo giá do mình lập.',
        '– Người duyệt xem được báo giá đang chờ mình duyệt.'], ['Xem danh sách', 'Xem chi tiết', 'Xuất Excel']),
    ('BR-04', 'Trạng thái và luồng chuyển', [
        '– Đang tạo → Gửi duyệt → Cấp 1: Đã duyệt (tự duyệt); Cấp 2: Chờ TP duyệt → Đã duyệt; Cấp 3: Chờ TP duyệt → Chờ BGĐ duyệt → Đã duyệt.',
        '– Chờ TP / Chờ BGĐ duyệt → Từ chối → Đang tạo.',
        '– Đã duyệt → Chốt (Trúng thầu) → Trúng thầu; Hủy chốt → Đã duyệt.',
        '– Dự án TKT đóng → mọi báo giá của dự án chuyển "Đóng".',
        '– Yêu cầu điều chỉnh giải pháp dừng YCBG → báo giá Đang tạo / chờ duyệt chuyển "Dừng".'], 'Toàn màn hình'),
    ('BR-05', 'Cấp duyệt', [
        '– Cấp = MAX(cấp theo giá trị đơn hàng sau GG quy VND, cấp theo TSLN tổng sau GG, cấp theo TSLN thấp nhất của dòng hàng tạm).',
        '– Ngưỡng theo Cấu hình duyệt giá; không khớp khoảng nào → cấp 3 (bảng PL-5).',
        '– Tự động duyệt khi chỉ có hàng / dịch vụ ERP, đơn giá bán > 1.000, không giảm giá, báo giá không rỗng.'], 'Gửi duyệt'),
    ('BR-06', 'Tỷ suất lợi nhuận', [
        '– TSLN = (Thành tiền bán sau GG − Thành tiền nhập) / Thành tiền nhập × 100, làm tròn 2 số lẻ.',
        '– Tính trên giá vốn, trước VAT; VAT không ảnh hưởng TSLN và cấp duyệt.',
        '– Thành tiền nhập = 0: TSLN dòng hiện "—", TSLN tổng = 0%; dòng hàng tạm giá nhập 0 tính là 0% khi xét cấp duyệt.'],
     ['Bảng chi tiết', 'Tổng hợp', 'Gửi duyệt']),
    ('BR-07', 'Hàng ERP lấy giá theo ERP', [
        '– Giá nhập, giá bán (theo Bảng giá, ĐVT, tỷ giá), VAT của hàng ERP lấy từ ERP, không sửa tay.',
        '– Mỗi lần Lưu / Gửi duyệt, hệ thống lấy lại giá ERP hiện hành (trừ khi người dùng chọn Từ chối ở popup đổi đơn giá màn Sửa).',
        '– Ngoại tệ: giá VND ÷ tỷ giá, làm tròn 2 số lẻ; tỷ giá chốt lúc tạo báo giá.'],
     ['Tạo mới', 'Chỉnh sửa', 'Sao chép', 'Import']),
    ('BR-08', 'Hàng cha – hàng con', [
        '– Hàng con không tính tiền riêng; chỉ dòng cha / độc lập cộng vào tổng.',
        '– Cha hàng tạm: Giá nhập = Σ(Giá nhập con × SL con) / SL cha; Giá bán cha × SL ≥ Σ(Giá bán con × SL con).',
        '– Cha hàng ERP (combo) được miễn 2 kiểm tra trên; SL con = SL công thức × SL cha.'], ['Bảng chi tiết', 'Gửi duyệt', 'Import']),
    ('BR-09', 'VAT theo dòng', [
        '– VAT áp trên dòng cha / độc lập và dịch vụ; tính SAU giảm giá.',
        '– VAT đồng loạt chỉ áp cho hàng tạm; hàng ERP và dịch vụ theo danh mục.',
        '– VAT vận chuyển cố định 8%.'], ['Bảng chi tiết', 'Tổng hợp']),
    ('BR-10', 'Giảm giá', [
        '– Cần Q6; không có Q6 thì không được thay đổi bất kỳ số giảm giá nào.',
        '– GG mặt hàng: GG(₫) ≤ đơn giá bán, GG(%) trong 0–100.',
        '– GG tổng: giảm giá thực tế = tổng cột Phân bổ GG; không chặn lưu khi chưa phân bổ hết.',
        '– Đổi phương thức GG xoá dữ liệu GG cũ. Dự án con kế thừa phương thức GG của dự án cha.'], ['Áp dụng VAT và giảm giá']),
    ('BR-11', 'Hiệu lực báo giá', [
        '– Hiệu lực = MIN(hôm nay + số ngày hiệu lực cấu hình ERP (mặc định 30), ngày đổi giá ERP sắp tới gần nhất của hàng ERP cấp cha).',
        '– Tính lại mỗi lần Lưu / Gửi duyệt; không nhập tay.'], ['Tạo mới', 'Chỉnh sửa', 'Gửi duyệt']),
    ('BR-12', 'Xử lý khi giá ERP thay đổi', [
        '– Tạo mới: chỉ cảnh báo icon ⚠ + rút hiệu lực; khi Lưu lấy giá hiện hành.',
        '– Chỉnh sửa: popup Đồng ý / Từ chối (chỉ so giá bán); giá vốn đổi âm thầm khi Lưu nếu Đồng ý hoặc không có popup.',
        '– Sao chép: luôn lấy giá mới, không chọn giữ giá cũ.', '– Chi tiết: Phụ lục, bảng PL-7.'],
     ['Tạo mới', 'Chỉnh sửa', 'Sao chép']),
    ('BR-13', 'Xoá báo giá', [
        '– Xoá cứng kèm dòng hàng hoá và lịch sử; không khôi phục.',
        '– YCBG nguồn không còn báo giá nào → về "Chờ XD giá".'], 'Xóa'),
    ('BR-14', 'Sao chép', [
        '– Sao chép được ở mọi trạng thái; bản sao luôn là báo giá tự nhập, trạng thái Đang tạo.',
        '– Không kế thừa YCBG, Ghi chú kinh doanh, thông tin duyệt, lịch sử; giữ mã hàng tạm.',
        '– Báo giá mới chỉ tạo khi bấm Lưu.'], 'Sao chép'),
    ('BR-15', 'Import Excel', [
        '– Tất cả hoặc không; còn lỗi thì không Import được.',
        '– STT bắt buộc, duy nhất, tối đa 2 cấp; quan hệ cha – con theo cột Mã hàng cha (dòng cha phía trên, cùng nhóm).',
        '– Hàng tạm: Tên, Thương hiệu, Xuất xứ, VAT, Đơn giá bán bắt buộc; ô Đơn giá nhập trống = giữ giá cũ.',
        '– ĐVT không có trong danh mục → lỗi; Model / Thương hiệu / Xuất xứ / Dịch vụ chưa có → tự tạo.',
        '– Tối đa 1 dòng Chi phí vận chuyển; báo giá từ BOM không thêm hàng, không đổi SL / tên / model / ĐVT.',
        '– Sau Import phải bấm Lưu báo giá.'], 'Import'),
    ('BR-16', 'Duyệt đúng phạm vi', [
        '– TP chỉ duyệt / từ chối báo giá thuộc phòng ban mình quản lý; BGĐ chỉ báo giá thuộc công ty mình.',
        '– Từ chối bắt buộc lý do ≤ 1.000 ký tự.',
        '– Đã duyệt → đồng bộ ERP; đồng bộ lỗi không chặn duyệt.'], ['Duyệt', 'Từ chối']),
    ('BR-17', 'Bảo vệ giá vốn', [
        '– Không có Q5: ẩn Giá nhập, Thành tiền nhập, TSLN, cấp duyệt dự kiến trên màn, popup, file Excel, lịch sử.',
        '– Bản in luôn ẩn giá vốn.'], 'Toàn màn hình'),
])

# ==================================================== PHỤ LỤC — BẢNG ĐÍNH KÈM CÔNG THỨC
d.h1('Phụ lục. Bảng đính kèm — Công thức và logic tính báo giá')
d.p('Các bảng dưới đây là nguồn duy nhất cho cách tính số liệu trên màn Báo giá. Số tiền hiển thị theo chuẩn quốc tế '
    '(1,234,567.89), số chữ số lẻ theo ô "Làm tròn" của báo giá (VNĐ: số nguyên).')

d.p('Bảng PL-1. Ký hiệu')
d.table(['Ký hiệu', 'Ý nghĩa'], [
    ('SL', 'Số lượng của dòng'),
    ('GN', 'Giá nhập (đơn giá vốn)'),
    ('GB', 'Giá bán (đơn giá, trước giảm giá, trước VAT)'),
    ('GG%, GG₫', 'Giảm giá mặt hàng theo % / theo tiền, tính trên 1 đơn vị'),
    ('PB', 'Số tiền Phân bổ GG của cả dòng (phương thức GG tổng)'),
    ('VAT%', 'Thuế suất VAT của dòng'),
    ('CPVC, GNVC, GGVC', 'Chi phí vận chuyển (giá bán), Giá nhập vận chuyển, Giảm giá vận chuyển'),
], widths=[1.4, 4.6])

d.p('Bảng PL-2. Công thức theo từng dòng hàng hoá / dịch vụ')
d.table(['STT', 'Đại lượng', 'Công thức', 'Ghi chú'], [
    (1, 'Thành tiền nhập', 'SL × GN', 'Dòng con không cộng vào tổng'),
    (2, 'Thành tiền trước GG', 'SL × GB', 'Dùng cho cột "Thành tiền trước VAT" bảng Tổng hợp'),
    (3, 'GG₫ khi nhập %', 'round(GB × GG% / 100, 2)', 'GG mặt hàng'),
    (4, 'GG% khi nhập ₫', 'round(GG₫ / GB × 100, 4); GB = 0 → 0', 'GG mặt hàng'),
    (5, 'Đơn giá sau GG', 'GB − GG₫', 'GG mặt hàng'),
    (6, 'Giảm giá của dòng', 'Không GG: 0\nGG mặt hàng: GG₫ × SL\nGG tổng: PB', '–'),
    (7, 'Thành tiền bán (sau GG, trước VAT)', 'SL × GB − Giảm giá của dòng', 'Cột "Thành tiền bán" trên bảng'),
    (8, 'Tiền VAT', 'Thành tiền bán × VAT% / 100', 'VAT tính SAU giảm giá'),
    (9, 'Thành tiền sau VAT', 'Thành tiền bán + Tiền VAT', '–'),
    (10, 'Tỷ suất LN dòng', 'round((Thành tiền bán − Thành tiền nhập) / Thành tiền nhập × 100, 2) %',
     'Trên giá vốn; Thành tiền nhập ≤ 0 → "—"; đỏ khi < Tỷ suất lợi nhuận mức sàn'),
    (11, 'GN cha hàng tạm có con', 'round(Σ(GN con × SL con) / SL cha) theo mức làm tròn', 'Khoá ô; SL cha = 0 → 0'),
    (12, 'Ràng buộc giá bán cha hàng tạm', 'GB cha × SL cha ≥ Σ(GB con × SL con)', 'Cha ERP được miễn'),
    (13, 'SL hàng con combo ERP', 'SL công thức × SL cha, làm tròn 2 số lẻ', 'Khoá'),
    (14, 'GN dịch vụ có tỷ lệ giá vốn R%', 'round(GB × R / 100, 2)', 'Khoá; chưa có R → nhập tay, khi Lưu ghi R = GN / GB × 100 vào danh mục'),
    (15, 'Giá hàng ERP theo ngoại tệ', 'round(Giá VND / Tỷ giá, 2)', 'Tỷ giá chốt lúc tạo báo giá'),
], widths=[0.4, 1.5, 2.3, 1.8])

d.p('Bảng PL-3. Tổng hợp giá trị và tỷ suất lợi nhuận tổng')
d.table(['STT', 'Đại lượng', 'Công thức', 'Hiển thị ở'], [
    (1, 'Nhóm I Hàng hoá / II Dịch vụ / III Chi phí', 'Cộng các cột của dòng thuộc nhóm (I: chỉ dòng cha / độc lập; II: dịch vụ có tính doanh thu; '
     'III: "Chi phí khác")', 'Bảng Tổng hợp'),
    (2, 'Giảm giá vận chuyển GGVC', 'GG mặt hàng: ô GG VC (% ↔ ₫, 2 số lẻ)\nGG tổng: ô Phân bổ VC\nKhông GG: 0', 'Dòng IV'),
    (3, 'VAT vận chuyển', '(CPVC − GGVC) × 8%', 'Dòng IV; chỉ tính khi CPVC > 0'),
    (4, 'Thành tiền sau VAT vận chuyển', 'CPVC − GGVC + VAT vận chuyển', 'Dòng IV'),
    (5, 'Dòng V — Tổng giá trị báo giá', 'Cộng dòng I + II + III + IV theo từng cột', 'Bảng Tổng hợp, cột Tổng giá trị sau VAT ở danh sách'),
    (6, 'Thành tiền sau GG (trước VAT)', 'Thành tiền trước VAT − Giảm giá', 'Bảng Tổng hợp (khi có GG)'),
    (7, 'TSLN trước GG', 'round((Tổng trước VAT − Tổng nhập) / Tổng nhập × 100, 2)', 'Dưới bảng Tổng hợp (có Q5)'),
    (8, 'TSLN sau GG', 'round((Tổng sau GG − Tổng nhập) / Tổng nhập × 100, 2) — GỒM vận chuyển', 'Dưới bảng Tổng hợp, chân trang "LN", tính cấp duyệt'),
    (9, 'TSLN dòng TỔNG của bảng chi tiết', 'Như dòng 8 nhưng KHÔNG gồm vận chuyển', 'Dòng TỔNG bảng chi tiết'),
    (10, 'Tổng nhập = 0', 'TSLN tổng hiển thị 0%', '–'),
    (11, '~VND', 'Tổng sau GG × Tỷ giá', 'Chân trang, chỉ ngoại tệ'),
], widths=[0.4, 1.7, 2.6, 1.3])

d.p('Bảng PL-4. Giảm giá tổng và phân bổ')
d.table(['STT', 'Đại lượng', 'Công thức / Logic'], [
    (1, 'Cơ sở tính khoản GG kiểu %', 'Σ(SL × GB dòng cha hàng hoá) + Σ(SL × GB dịch vụ, chi phí) + CPVC — trước GG, trước VAT'),
    (2, 'Thành tiền GG của khoản', 'Kiểu %: round(Cơ sở × % / 100, 2)\nKiểu ₫: số tiền nhập'),
    (3, 'Tổng GG', 'Σ Thành tiền GG các khoản'),
    (4, 'Phân bổ tự động', 'Mỗi dòng (cha hàng hoá, dịch vụ, vận chuyển nếu > 0) nhận Tổng GG × (SL × GB của dòng / Tổng SL × GB các dòng). '
     'Làm tròn 0,01 theo phương pháp phần dư lớn nhất: lấy phần nguyên trước, phần còn thiếu chia lần lượt 0,01 cho dòng có phần lẻ '
     'lớn nhất → tổng phân bổ khớp tuyệt đối Tổng GG'),
    (5, 'Khớp phân bổ', '|Đã phân bổ − Tổng GG| < 1 → "✓"; ngược lại "Chênh lệch: Z" (đỏ)'),
    (6, 'Giảm giá thực tế trên báo giá', 'Tổng cột Phân bổ GG (không phải Tổng GG khai báo)'),
    (7, 'Ví dụ', 'Tổng GG 1,000,000; dòng X bán 6,000,000, dòng Y 3,000,000, vận chuyển 1,000,000 → X 600,000; Y 300,000; VC 100,000'),
], widths=[0.4, 1.6, 4.0])

d.p('Bảng PL-5. Cấp duyệt (theo Cấu hình duyệt giá — Phân hệ Bán hàng => Cấu hình duyệt giá)')
d.table(['Tiêu chí', 'Cấp 1 — Tự duyệt', 'Cấp 2 — Trưởng phòng', 'Cấp 3 — Ban giám đốc'], [
    ('Giá trị đơn hàng V = Tổng sau GG × Tỷ giá (VND)', '0 ≤ V < 1 tỷ', '1 tỷ ≤ V < 20 tỷ', 'V ≥ 20 tỷ'),
    ('TSLN tổng sau GG M', 'M ≥ 35%', '20% ≤ M < 35%', '0 ≤ M < 20%'),
    ('TSLN thấp nhất của dòng hàng tạm T', 'T ≥ 35%', '20% ≤ T < 35%', 'T < 20%'),
], widths=[2.1, 1.3, 1.3, 1.3])
d.bullets([
    'Cấp duyệt = MAX(cấp theo V, cấp theo M, cấp theo T). Không có hàng tạm → bỏ tiêu chí T. Giá trị không rơi vào khoảng nào '
    '(vd M âm) → cấp 3. Khoảng tính theo min ≤ x < max.',
    'Ngưỡng trên là giá trị cấu hình hiện hành tại thời điểm viết tài liệu; người quản trị đổi được ở màn Cấu hình duyệt giá.',
    'Tự động duyệt (ép cấp 1): không chọn phương thức GG và không có giảm giá; mọi hàng hoá là hàng ERP, mọi dịch vụ từ danh mục; mọi '
    'đơn giá bán > 1.000; báo giá có ít nhất 1 dòng.',
    'Chân trang màn Tạo / Sửa chỉ xét V và M nên chỉ là cấp DỰ KIẾN; cấp chính thức là cấp hiển thị ở popup Gửi duyệt.',
])

d.p('Bảng PL-6. Ví dụ tính toán (VNĐ)')
d.table(['Trường hợp', 'Dữ liệu', 'Kết quả'], [
    ('(a) Không GG',
     'Hàng A: SL 2, GN 1,000,000, GB 1,300,000, VAT 10%\nHàng B: SL 1, GN 500,000, GB 600,000, VAT 8%\n'
     'Dịch vụ: SL 1, GN 200,000, GB 400,000, VAT 8%\nVận chuyển: GNVC 100,000, CPVC 150,000',
     'I Hàng hoá: nhập 2,500,000 · trước VAT 3,200,000 · VAT 308,000 · sau VAT 3,508,000\n'
     'II Dịch vụ: 200,000 · 400,000 · 32,000 · 432,000\nIV Vận chuyển: 100,000 · 150,000 · 12,000 · 162,000\n'
     'V Tổng: 2,800,000 · 3,750,000 · 352,000 · 4,102,000\nTSLN = (3,750,000 − 2,800,000) / 2,800,000 = 33.93%'),
    ('(b) GG tổng 10%', 'Như (a), 1 khoản GG kiểu 10%',
     'Thành tiền GG = 3,750,000 × 10% = 375,000\nPhân bổ: A 260,000 · B 60,000 · DV 40,000 · VC 15,000\n'
     'Sau GG 3,375,000; VAT 316,800; Tổng sau VAT 3,691,800\nTSLN trước GG 33.93% · TSLN sau GG 20.54%\n'
     'TSLN dòng A = (2,340,000 − 2,000,000) / 2,000,000 = 17%'),
    ('(c) GG mặt hàng 10% cho A', 'Như (a)',
     'GG₫ = 130,000/đơn vị; Đơn giá sau GG 1,170,000; Giảm giá dòng 260,000\nThành tiền bán A 2,340,000; VAT A 234,000'),
    ('(d) Cha hàng tạm có con', 'Cha SL 2; con 1: SL 4 × GN 300,000, GB 400,000; con 2: SL 2 × GN 150,000, GB 200,000',
     'GN cha = (1,200,000 + 300,000) / 2 = 750,000\nGB cha phải ≥ (1,600,000 + 400,000) / 2 = 1,000,000'),
], widths=[1.2, 2.2, 2.6])

d.p('Bảng PL-7. Xử lý khi giá bán / giá vốn ERP thay đổi')
d.table(['Thời điểm', 'Hệ thống phát hiện', 'Người dùng thấy', 'Giá được ghi khi Lưu'], [
    ('Đang Tạo mới — giá đã lên lịch đổi trong tương lai', 'Lịch đổi giá của hàng ERP cấp cha',
     'Icon ⚠ cạnh Mã: “Giá bán thay đổi ngày dd/mm/yyyy”; Hiệu lực báo giá rút về ngày đổi giá', 'Giá ERP hiện hành'),
    ('Đang Tạo mới — giá ERP đổi giữa lúc thêm hàng và lúc Lưu', 'Không so sánh', 'Không có cảnh báo',
     'Giá vốn + giá bán ERP hiện hành (số trên màn có thể khác số sau khi lưu)'),
    ('Mở Chỉnh sửa — giá bán ERP khác giá đã lưu', 'So giá bán từng hàng ERP (cha, combo, con)',
     'Popup "Đơn giá hàng hoá đã thay đổi" (tối đa 10 dòng) — Đồng ý / Từ chối',
     'Đồng ý: giá vốn + giá bán + VAT ERP hiện hành\nTừ chối: giữ giá vốn + giá bán đã lưu; VAT ERP vẫn cập nhật; hàng ERP mới thêm lấy giá hiện hành'),
    ('Mở Chỉnh sửa — chỉ giá vốn ERP đổi', 'Không so giá vốn', 'Không có popup',
     'Giá vốn ERP mới → TSLN và cấp duyệt thay đổi sau khi lưu'),
    ('Sao chép', 'So giá vốn (có Q5), giá bán, VAT, cấu trúc combo với báo giá nguồn',
     'Popup "Phát hiện thay đổi dữ liệu từ ERP" — chỉ Xác nhận / Hủy bỏ',
     'Hàng ERP: giá + VAT ERP hiện hành (tỷ giá hiện hành); hàng tạm giữ nguyên; cấu trúc combo giữ theo bản gốc'),
    ('Import Excel', 'Mã hàng tra được trong ERP', 'Ô dữ liệu chuẩn ERP khoá trên bảng xem trước',
     'Giá nhập, giá bán, VAT ERP hiện hành; giá trong file bị bỏ qua'),
    ('Đổi Bảng giá (Tạo mới)', 'Giá bán hàng ERP theo bảng giá mới', 'Hộp xác nhận đổi bảng giá',
     'Giá bán + VAT theo bảng giá mới; giá vốn không đổi'),
], widths=[1.4, 1.4, 1.6, 1.6])

d.save()
