# -*- coding: utf-8 -*-
"""Bộ sinh HDSD + SRS DÙNG CHUNG cho các màn danh mục, dựng trên KHUÔN tài liệu Danh mục quốc gia
(bản TPE duyệt 23/09/2026). Tổng quát hoá từ bộ Gói bảo dưỡng (docs_v2) đã được user duyệt 25/09/2026.

Mỗi màn chỉ cần 1 file cấu hình `configs/<slug>.py` khai biến `CFG` (xem SCHEMA ở cuối file).
Quy tắc cứng (user chốt): KHÔNG ghi URL / đường dẫn; chỉ đường bấm menu + nút (icon cắt từ UI);
chữ trên UI, message lỗi, toast ghi NGUYÊN VĂN theo code.

Chạy:  python3 catalog_v2.py <slug> [hdsd|srs|all]
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
from qg_writer import QgWriter, strip_embedded_fonts  # noqa: E402

ROOT = os.path.join(HERE, '..', 'catalog-docs-v2')
TPL = os.path.join(ROOT, 'templates')
ICONS = os.path.join(ROOT, 'icons')          # icon nút dùng chung (Tạo mới, Xuất Excel, Sửa…)
HDSD_TPL = os.path.join(TPL, 'HDSD_Danh mục quốc gia.docx')
SRS_TPL = os.path.join(TPL, 'SRS - Danh mục quốc gia.docx')

HDSD_ROLES = {'pagebreak': 39, 'h1': 40, 'h2': 41, 'p': 31, 'bullet': 48, 'step': 42,
              'img': 44, 'cap': 45, 'blank': 26, 'tbl2': 25, 'tbl4': 28, 'tbl5': 90}
SRS_ROLES = {'pagebreak': 11, 'h1': 12, 'h2': 13, 'h3': 35, 'p': 14, 'bullet': 15, 'sub': 36,
             'qtc': 37, 'menu_b': 42, 'menu': 43, 'img': 44, 'cap': 45, 'blank': 19,
             'tbl2': 18, 'tbl4': 50, 'tbl5': 47, 'tbl6': 64, 'tbl7': 87, 'tbl8': 108}
QTC_LINK = 'SRS_Các quy tắc chung_VN_1.0'


def load_cfg(slug):
    path = os.path.join(ROOT, 'configs', slug + '.py')
    spec = importlib.util.spec_from_file_location('cfg_' + slug, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CFG


class Ctx(object):
    def __init__(self, cfg):
        self.c = cfg
        self.dir = os.path.join(ROOT, cfg['slug'])
        self.shots = os.path.join(self.dir, 'shots')
        self.icons_local = os.path.join(self.dir, 'icons')

    def shot(self, key):
        """key trong cfg['shots'] -> đường dẫn ảnh; None nếu không khai / không có file."""
        name = self.c.get('shots', {}).get(key)
        if not name:
            return None
        for d in (self.shots, self.dir):
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
        print('  [thiếu ảnh] %s -> %s' % (key, name))
        return None

    def ic(self, name, h=0.22):
        for d in (self.icons_local, ICONS):
            p = os.path.join(d, name + '.png')
            if os.path.exists(p):
                return ('img', p, h)
        return name  # thiếu icon thì để chữ

    def segs(self, value):
        """Chuỗi có {icon:ten} -> list segment chữ + icon."""
        if not isinstance(value, str) or '{icon:' not in value:
            return value
        out = []
        rest = value
        while '{icon:' in rest:
            a, b = rest.split('{icon:', 1)
            name, rest = b.split('}', 1)
            if a:
                out.append(a)
            out.append(self.ic(name))
        if rest:
            out.append(rest)
        return out

    def menu_segs(self, prefix=''):
        """"Từ phân hệ X [icon], tại menu Y [icon], chọn Z [icon]" (2 cấp: "Từ phân hệ X, chọn Z")."""
        items = self.c['menu']
        segs = [prefix] if prefix else []
        for i, (text, icon) in enumerate(items):
            if i == 0:
                lead = 'Từ phân hệ '
            elif i == len(items) - 1:
                lead = ', chọn '
            else:
                lead = ', tại menu '
            segs.append(lead + text + ' ')
            if icon:
                segs.append(self.ic(icon))
        return segs


# ====================================================================== HDSD
def build_hdsd(slug, out=None):
    c = load_cfg(slug)
    x = Ctx(c)
    w = QgWriter(HDSD_TPL, HDSD_ROLES, body_from=21,
                 cover_replace={'Danh mục quốc gia': c['ten']})
    dt = c['doi_tuong']

    def img(key, cap, width=6.0):
        p = x.shot(key)
        if p:
            w.image(p, width=width, caption=cap)

    def block(items):
        """items: list các ('p'|'b'|'s'|'img'|'tbl'|'h2', data)."""
        for kind, data in items:
            if kind == 'p':
                w.p(x.segs(data))
            elif kind == 'b':
                w.bullet(x.segs(data))
            elif kind == 's':
                w.step(x.segs(data))
            elif kind == 'img':
                img(data[0], data[1])
            elif kind == 'tbl':
                w.table(data[0], widths=data[1] if len(data) > 1 else None)
            elif kind == 'h2':
                w.h2(data)

    # ---------------------------------------------------------------- TỔNG QUAN
    w.h1('TỔNG QUAN')
    w.h2('1. Thuật ngữ sử dụng trong tài liệu')
    w.table([['Thuật ngữ', 'Giải thích']] + c['thuat_ngu'], widths=[1, 2.6])
    w.h2('2. Cập nhật tài liệu')
    w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung']] + c['phien_ban'],
            widths=[0.8, 1, 1.4, 3.4])
    w.h2('3. Mục đích')
    for p in c['muc_dich']:
        w.p(p)
    w.h2('4. Quyền sử dụng')
    q = c['quyen']
    for p in q.get('truoc', []):
        w.p(p)
    if q.get('rows'):
        w.table([['Tên quyền', 'Được phép']] + q['rows'], widths=[1.4, 2.6])
    for p in q.get('sau', []):
        w.p(p)
    w.h2('5. Sơ đồ chức năng tổng quan')
    uml = os.path.join(x.dir, 'uml', 'overview.png')
    if os.path.exists(uml):
        w.image(uml, width=5.8, caption='Sơ đồ chức năng tổng quan màn %s' % c['ten'])

    part = [0]

    def P(title):
        part[0] += 1
        w.h1('PHẦN %d: %s' % (part[0], title))

    # ---------------------------------------------------------------- PHẦN truy cập
    P('TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')
    w.h2('1. Truy cập màn hình')
    w.step(x.menu_segs())
    w.p(c['danh_sach'].get('mo_ta_vao', 'Hệ thống hiển thị danh sách %s hiện có.' % dt))
    img('list', 'Màn hình %s khi mới truy cập' % c['ten'])
    w.h2('2. Bố cục màn hình')
    w.p('Màn hình chia làm ba khu vực từ trên xuống:')
    for b in c['danh_sach']['bo_cuc']:
        w.bullet(x.segs(b))
    w.h2('3. Các cột của bảng danh sách')
    w.table([['Cột', 'Nội dung']] + c['danh_sach']['cot'], widths=[1.3, 3])
    hd = c['danh_sach'].get('hanh_dong')
    if hd:
        w.h2('4. Cột Hành động')
        if hd.get('intro'):
            w.p(hd['intro'])
        if hd.get('rows'):
            w.table([['Nút', 'Khi nào hiện', 'Tác dụng']] + hd['rows'], widths=[0.9, 2, 2])
        for b in hd.get('bullets', []):
            w.bullet(x.segs(b))
        img('rowmenu', hd.get('anh', 'Các nút ở cột Hành động'))
        for p in hd.get('luu_y', []):
            w.p(x.segs(p))
    w.h2('%d. Phân trang và sắp xếp' % (5 if hd else 4))
    for p in c['danh_sach']['phan_trang']:
        w.p(p)
    block(c['danh_sach'].get('them', []))

    # ---------------------------------------------------------------- PHẦN tìm kiếm
    loc = c['loc']
    P('TÌM KIẾM VÀ LỌC DANH SÁCH')
    w.h2('1. Các ô tìm kiếm và lọc')
    w.p('Các bước tìm kiếm, lọc thông tin:')
    w.step(x.menu_segs('Bước 1: '))
    w.step(x.segs(loc.get('buoc2', 'Bước 2: Nhập chữ vào ô tìm kiếm nhanh hoặc chọn giá trị ở các ô lọc.')))
    img('filter', 'Khu vực tìm kiếm và lọc')
    w.table([['Ô', 'Cách dùng']] + loc['rows'], widths=[1.2, 3])
    w.h2('2. Cách áp dụng')
    for p in loc['ap_dung']:
        w.p(x.segs(p))
    img('filter_result', loc.get('anh_ket_qua', 'Kết quả sau khi lọc'))

    # ---------------------------------------------------------------- PHẦN thêm mới
    f = c['form']
    if f.get('co_tao', True):
        P('THÊM MỚI %s' % dt.upper())
        w.h2('1. Các bước Thêm mới %s' % dt)
        for s in f['buoc_tao']:
            w.step(x.segs(s))
        img('create', f.get('anh_tao', 'Cửa sổ Tạo %s' % dt))
        w.h2('2. Các trường cần nhập')
        w.table([['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị ban đầu', 'Ghi chú']] + f['truong'],
                widths=[1.3, 0.9, 0.7, 1.1, 2.6])
        for p in f.get('sau_truong', []):
            w.p(x.segs(p))
        block(f.get('them', []))
        n = 3 + sum(1 for k, _ in f.get('them', []) if k == 'h2')
        w.h2('%d. Tác dụng các nút' % n)
        w.table([['Nút', 'Tác dụng']] + f['nut'], widths=[1.2, 4])
        w.h2('%d. Các lỗi thường gặp' % (n + 1))
        w.p(f.get('loi_mo_dau', 'Nếu còn thiếu sót, hệ thống báo lỗi đỏ ngay dưới ô tương ứng. %s KHÔNG đóng và dữ liệu đã nhập vẫn còn nguyên — Người dùng chỉ cần sửa chỗ báo đỏ rồi bấm Lưu lại.' % ('Cửa sổ' if f.get('kieu', 'popup') == 'popup' else 'Trang')))
        img('create_error', 'Hệ thống báo lỗi đỏ ngay dưới ô còn thiếu / sai')
        img('code_error', 'Lỗi định dạng mã hiện ngay khi gõ')
        w.table([['Thông báo', 'Nguyên nhân và cách xử lý']] + f['loi'], widths=[1.8, 3])

    # ---------------------------------------------------------------- PHẦN sửa & xoá
    s = c.get('sua')
    xo = c.get('xoa')
    if s or xo:
        P('CHỈNH SỬA VÀ XÓA' if (s and xo) else ('CHỈNH SỬA' if s else 'XÓA'))
        k = 0
        if s:
            k += 1
            w.h2('%d. Chỉnh sửa' % k)
            for st in s['buoc']:
                w.step(x.segs(st))
            img('edit', s.get('anh', 'Cửa sổ Sửa %s' % dt))
            for b in s.get('ghi_chu', []):
                w.bullet(x.segs(b))
        if xo:
            k += 1
            w.h2('%d. Xóa' % k)
            for st in xo['buoc']:
                w.step(x.segs(st))
            img('delete', xo.get('anh', 'Hộp xác nhận xóa %s' % dt))
            for p in xo.get('ghi_chu', []):
                w.p(x.segs(p))

    # ---------------------------------------------------------------- PHẦN khoá
    kh = c.get('khoa')
    if kh:
        P('KHÓA VÀ MỞ KHÓA')
        w.h2('1. Ý nghĩa')
        for b in kh['y_nghia']:
            w.bullet(x.segs(b))
        w.h2('2. Các bước khóa')
        for st in kh['buoc_khoa']:
            w.step(x.segs(st))
        img('lock', kh.get('anh_khoa', 'Hộp xác nhận khóa %s' % dt))
        w.h2('3. Mở khóa')
        for st in kh['buoc_mo']:
            w.step(x.segs(st))
        img('unlock', kh.get('anh_mo', 'Hộp xác nhận mở khóa %s' % dt))
        for p in kh.get('ghi_chu', []):
            w.p(x.segs(p))

    # ---------------------------------------------------------------- PHẦN lịch sử
    ls = c.get('lich_su')
    if ls:
        P('XEM LỊCH SỬ THAY ĐỔI')
        for st in ls['buoc']:
            w.step(x.segs(st))
        img('history', 'Cửa sổ Lịch sử thay đổi của %s' % dt)
        w.p('Cửa sổ liệt kê mọi lần thay đổi của bản ghi, mới nhất trên cùng. Mỗi mốc cho biết:')
        for b in ['Thời điểm thay đổi, dạng dd/mm/yyyy hh:mm.',
                  'Loại thay đổi — Tạo mới, Thay đổi thông tin' + (', Khóa, Mở khóa.' if kh else '.'),
                  'Người thực hiện kèm phòng ban.',
                  'Trường nào đã đổi, giá trị cũ → giá trị mới.']:
            w.bullet(b)
        for p in ls.get('ghi_chu', []):
            w.p(x.segs(p))

    # ---------------------------------------------------------------- PHẦN xem chi tiết
    ct = c.get('chi_tiet')
    if ct:
        P('XEM CHI TIẾT %s' % dt.upper())
        for st in ct['buoc']:
            w.step(x.segs(st))
        img('detail', ct.get('anh', 'Xem chi tiết %s ở chế độ chỉ đọc' % dt))
        for p in ct.get('ghi_chu', []):
            w.p(x.segs(p))

    # ---------------------------------------------------------------- phần riêng (trước xuất)
    for sec in c.get('phan_rieng', []):
        P(sec['tieu_de'])
        block(sec['noi_dung'])

    # ---------------------------------------------------------------- PHẦN xuất excel
    xe = c.get('xuat')
    if xe:
        P('XUẤT DANH SÁCH RA EXCEL')
        w.h2('1. Các bước xuất file')
        for st in xe['buoc']:
            w.step(x.segs(st))
        img('export', xe.get('anh', 'Cửa sổ Chọn trường xuất file'))
        if xe.get('bang_thanh_phan', True):
            w.h2('2. Tác dụng các thành phần trên cửa sổ')
            w.table([['Thành phần', 'Tác dụng'],
                     ['Danh sách trường', xe['truong']],
                     ['Chọn tất cả', 'Tích hết các trường.'],
                     ['Bỏ chọn hết', 'Bỏ tích toàn bộ. Khi không còn trường nào được chọn, nút Xuất file không bấm được.'],
                     ['Xuất file', 'Sinh file Excel và tải về máy.'],
                     ['Đóng', 'Đóng cửa sổ, không xuất gì.']], widths=[1.3, 3.5])
        for p in xe.get('ghi_chu', []):
            w.p(x.segs(p))

    # ---------------------------------------------------------------- PHẦN import
    im = c.get('import')
    if im:
        P('IMPORT %s TỪ FILE EXCEL' % dt.upper())
        w.h2('1. Các bước nhập dữ liệu')
        w.step(x.segs('Bước 1: Tại màn hình danh sách, bấm {icon:btn_import}. Hệ thống mở cửa sổ “%s”.' % im['tieu_de']))
        img('import_open', 'Cửa sổ %s khi vừa mở' % im['tieu_de'])
        w.step(x.segs('Bước 2: Bấm {icon:btn_taifilemau} để lấy file %s, gồm các cột: %s. Điền dữ liệu vào file này.' % (im['file'], im['cot_text'])))
        w.step(x.segs('Bước 3: Bấm {icon:btn_chonfile}, chọn file vừa điền, rồi bấm {icon:btn_load}. Dữ liệu hiện lên bảng xem trước và ô Tổng cho biết đọc được bao nhiêu dòng.'))
        img('import_loaded', 'Dữ liệu đã được load lên bảng xem trước')
        w.step(x.segs('Bước 4: Bấm {icon:btn_validate} để hệ thống kiểm tra từng dòng. Bước này CHƯA ghi dữ liệu vào hệ thống.'))
        img('import_validated', 'Kết quả kiểm tra — mỗi dòng lỗi nêu rõ lý do')
        w.p('Sau khi kiểm tra, hệ thống hiển thị ba con số: Tổng, Hợp lệ, Lỗi. Dòng lỗi được tô nền đỏ kèm lý do ngay dưới ô; dòng hợp lệ bị khoá lại, không sửa được nữa.')
        w.step(x.segs('Bước 5: Sửa trực tiếp các dòng lỗi trên bảng rồi bấm Validate lại. Nếu không muốn nhập các dòng lỗi thì bấm {icon:btn_bodongloi} để loại chúng khỏi bảng. Muốn sửa lại cả những dòng đã khoá thì bấm {icon:btn_xoavalidate}.'))
        w.step(x.segs('Bước 6: Bấm {icon:btn_import_modal}. Nút này chỉ bấm được khi đã Validate và không còn dòng lỗi. Hệ thống báo “%s”, đóng cửa sổ và nạp lại danh sách.' % im['toast']))
        w.h2('2. Các lỗi thường gặp khi kiểm tra dữ liệu')
        w.table([['Thông báo', 'Nguyên nhân']] + im['loi'], widths=[2.6, 2.4])
        for p in im.get('ghi_chu', []):
            w.p(x.segs(p))

    # ---------------------------------------------------------------- PHẦN tuỳ chỉnh cột
    tc = c.get('tuy_chinh_cot')
    if tc:
        P('TÙY CHỈNH CỘT HIỂN THỊ')
        w.step(x.segs('Bước 1: Ở thanh công cụ của bảng, bấm biểu tượng {icon:btn_cauhinhcot}. Hệ thống mở cửa sổ “Tuỳ chỉnh cột”.'))
        img('colcfg', 'Cửa sổ Tuỳ chỉnh cột')
        w.step('Bước 2: Tích để hiện cột, bỏ tích để ẩn cột. Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.')
        w.step(x.segs('Bước 3: Bấm {icon:btn_luu} để áp dụng; bấm Đóng nếu muốn bỏ các thay đổi vừa chỉnh.'))
        w.p('%s bị khoá: không bỏ tích và không kéo đổi vị trí được.' % tc['cot_khoa'])
        w.p('Cấu hình cột được ghi nhớ riêng cho từng người dùng, lần sau vào màn hình vẫn giữ nguyên.')

    w.rebuild_toc()
    out = out or os.path.join(x.dir, 'out', c['file_hdsd'])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    return w.save(out)


# ====================================================================== SRS

def apply_tester_edits(c):
    """Giữ các chỗ tester đã sửa tay trên Drive (CFG['srs_tester']): bỏ ý trong bảng Giới thiệu,
    thay nội dung quy tắc Phần 4. Chạy trước khi dựng SRS để lần đẩy sau không ghi đè mất."""
    te = c.get('srs_tester')
    if not te:
        return c
    import re as _re
    norm = lambda s: _re.sub(r'\s+', ' ', s).strip(' •–-')
    dels = {norm(x) for x in te.get('del', [])}
    for fr in c['srs']['fr']:
        for row in fr.get('gioi_thieu', []):
            if not isinstance(row[1], str):
                continue
            lines = [l for l in row[1].split('\n') if not (norm(l) and norm(l) in dels)]
            if row[0] == 'Dòng sự kiện chính' and len(lines) != len(row[1].split('\n')):
                k = 0
                for i, l in enumerate(lines):
                    m = _re.match(r'^\d+\.\s*(.*)', l)
                    if m:
                        k += 1
                        lines[i] = '%d. %s' % (k, m.group(1))
            row[1] = '\n'.join(lines).strip('\n')
    br = te.get('br', {})
    c['srs']['quy_tac'] = [tuple(br[q[0]]) if q[0] in br else q for q in c['srs']['quy_tac']]
    return c

def build_srs(slug, out=None):
    c = apply_tester_edits(load_cfg(slug))
    x = Ctx(c)
    w = QgWriter(SRS_TPL, SRS_ROLES, body_from=10,
                 cover_replace={'Danh mục quốc gia': c['ten']})
    sr = c['srs']
    menu = []
    for i, (text, icon) in enumerate(c['menu']):
        menu.append(('Phân hệ ' if i == 0 else ' => ') + text + ' ')
        if icon:
            menu.append(x.ic(icon, 0.24))

    w.h1('Phần 1. Giới thiệu')
    w.h2('1 Mục đích')
    w.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % c['ten'])
    for b in sr['muc_dich']:
        w.bullet(b)
    w.h2('2 Thuật ngữ và viết tắt')
    w.table([['Thuật ngữ', 'Mô tả']] + c['thuat_ngu'], widths=[1.3, 3])

    w.h1('Phần 2. Phân quyền')
    w.h2('1 Danh sách quyền')
    for p in sr['quyen_truoc']:
        w.p(p)
    w.table([['Tên quyền', 'Tác dụng trên màn hình']] + sr['quyen_rows'], widths=[1.5, 3])
    w.h2('2 Ma trận phân quyền')
    w.table(sr['ma_tran'], widths=sr.get('ma_tran_widths'))
    for p in sr.get('quyen_sau', []):
        w.p(p)

    w.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
    w.h2('1 Sơ đồ UML tổng quan')
    uml_dir = os.path.join(x.dir, 'uml')
    if os.path.exists(os.path.join(uml_dir, 'overview.png')):
        w.image(os.path.join(uml_dir, 'overview.png'), width=5.6,
                caption='Sơ đồ Use Case tổng quan màn %s' % c['ten'])
    w.h2('2 Đặc tả chi tiết từng chức năng')

    for i, fr in enumerate(sr['fr']):
        # Skill srs-documenter (28/09/2026): MỌI chức năng phải có bảng giao diện + bảng event
        if not fr.get('ui') or not fr.get('events'):
            raise ValueError('SRS %s: FR "%s" thiếu ui/events — bắt buộc ở mọi chức năng' % (slug, fr['ten']))
        n = '2.%d' % (i + 1)
        w.h3('%s %s' % (n, fr['ten']))
        k = 0
        uc = fr.get('uc') and os.path.join(uml_dir, fr['uc'] + '.png')
        if uc and os.path.exists(uc):
            k += 1
            w.raw('sub', '%s.%d Biểu đồ Usecase' % (n, k))
            w.image(uc, width=5.2, caption='Biểu đồ Use Case — %s' % fr['ten'])
        k += 1
        w.raw('sub', '%s.%d Giới thiệu' % (n, k))
        if fr.get('qtc'):
            w.clone_texts('qtc', ['Quy tắc chung: ', 'Áp dụng SRS Các quy tắc chung ', QTC_LINK, ' - ' + fr['qtc']])
        w.table([['Mục', 'Nội dung']] + fr['gioi_thieu'], widths=[1, 3.2])
        k += 1
        w.raw('sub', '%s.%d Layout màn hình' % (n, k))
        w.p('Đường dẫn màn hình:')
        w.raw('menu_b', 'Menu: ')
        extra = x.segs(fr.get('menu_them', ''))
        if isinstance(extra, str):
            extra = [extra] if extra else []
        w.raw('menu', menu + extra)
        if fr.get('ghi_chu_layout'):
            w.p(fr['ghi_chu_layout'])
        for key, cap in fr.get('anh', []):
            p = x.shot(key)
            if p:
                w.image(p, caption=cap)
        if fr.get('ui'):
            k += 1
            w.raw('sub', '%s.%d Mô tả chi tiết giao diện' % (n, k))
            w.table(fr['ui'], widths=fr.get('ui_widths'))
        if fr.get('events'):
            k += 1
            w.raw('sub', '%s.%d Danh sách event và xử lý event' % (n, k))
            w.table([['STT', 'Event', 'Loại event', 'Xử lý event']] +
                    [[str(j + 1)] + e for j, e in enumerate(fr['events'])], widths=[0.6, 1.4, 0.8, 3.4])
        for extra_title, extra_rows, extra_w in fr.get('bang_them', []):
            k += 1
            w.raw('sub', '%s.%d %s' % (n, k, extra_title))
            w.table(extra_rows, widths=extra_w)

    w.h1('Phần 4. Quy tắc nghiệp vụ')
    w.p('**Quy tắc áp dụng:** Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung SRS_Các quy tắc chung_VN_1.0. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có trong SRS quy tắc chung.' % c['ten'])
    # Khuôn SRS Quốc gia / skill srs-documenter: bảng 5 cột STT | Mã quy tắc | Tên quy tắc | Mô tả | Phạm vi áp dụng.
    # Mỗi quy tắc: (mã, tên, mô tả, phạm vi) — mô tả / phạm vi là chuỗi hoặc list (mỗi phần tử 1 dòng).
    j = lambda v: '\n'.join(v) if isinstance(v, (list, tuple)) else v
    rows = [['STT', 'Mã quy tắc', 'Tên quy tắc', 'Mô tả', 'Phạm vi áp dụng']]
    for i, q in enumerate(sr['quy_tac'], 1):
        assert len(q) == 4, 'quy_tac phải là (mã, tên, mô tả, phạm vi): %r' % (q,)
        rows.append([str(i), q[0], q[1], j(q[2]), j(q[3])])
    w.table(rows, widths=[0.6, 0.85, 1.3, 2.65, 1.2])

    w.rebuild_toc(levels=(1, 2, 3))
    out = out or os.path.join(x.dir, 'out', c['file_srs'])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    return w.save(out)


def finalize(path):
    """Cho Word cập nhật mục lục (macOS) rồi gỡ font nhúng."""
    from _mac_docx import update_fields_by_word_mac
    update_fields_by_word_mac(os.path.realpath(path))
    return strip_embedded_fonts(path)


def build_uml(slug):
    """Sơ đồ Use Case theo cfg['uml'] = {'mains': [(mã, tên, nhóm)], 'subs': [(mã, tên, nhóm)]}.
    Quy ước bộ Quốc gia: tổng quan chỉ vẽ «extend» cho chức năng phụ gắn vào FR xem danh sách;
    sơ đồ riêng từng chức năng chỉ actor + 1 use case."""
    c = load_cfg(slug)
    sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'srs-documenter', 'assets'))
    import srs_uml_render as uml
    from _mac_docx import MAC_FONTS
    for k, v in MAC_FONTS.items():
        if os.path.exists(v):
            setattr(uml, k, v)
    out = os.path.join(ROOT, slug, 'uml')
    os.makedirs(out, exist_ok=True)
    u = c['uml']
    actor = u.get('actor', 'Người dùng đã đăng nhập')
    mains = u['mains']
    subs = [(a, b, g, 'extend', [0], None) for a, b, g in u.get('subs', [])]
    uml.draw_overview2(os.path.join(out, 'overview.png'), [(actor, list(range(len(mains))))], mains, subs)
    for code, name, group in mains[1:] + u.get('rieng', []):
        uml.draw_usecase(os.path.join(out, 'uc_' + code.lower().replace('-', '') + '.png'),
                         actor, code, name, group, relations=())
    return sorted(os.listdir(out))


if __name__ == '__main__':
    slug = sys.argv[1]
    what = sys.argv[2] if len(sys.argv) > 2 else 'all'
    outs = []
    if what in ('uml', 'all'):
        print(build_uml(slug))
    if what in ('hdsd', 'all'):
        outs.append(build_hdsd(slug))
    if what in ('srs', 'all'):
        outs.append(build_srs(slug))
    for o in outs:
        print(o, finalize(o))


SCHEMA = """
CFG = {
  'slug': 'areas',                       # tên thư mục catalog-docs-v2/<slug>/
  'ten': 'Danh mục khu vực',             # tên màn (bìa, tiêu đề)
  'doi_tuong': 'khu vực',                # danh từ chung, chữ thường
  'file_hdsd': 'HDSD_Danh mục khu vực.docx',   # ĐÚNG tên file đang có trên Drive
  'file_srs': 'SRS - Danh mục khu vực.docx',
  'menu': [('Danh mục', 'menu_phanhe'), ('Địa lý', 'menu_nhom'), ('Khu vực', 'menu_muc')],  # (chữ, icon)
  'thuat_ngu': [[thuật ngữ, giải thích], ...],
  'phien_ban': [['1.0','17/08/2026','Đội phát triển phần mềm','...'], ['1.1','25/09/2026','Đội phát triển phần mềm','...']],
  'muc_dich': [đoạn, ...],
  'quyen': {'truoc': [đoạn], 'rows': [[tên quyền, được phép]] hoặc [], 'sau': [đoạn]},
  'danh_sach': {'bo_cuc': [3 gạch đầu dòng], 'cot': [[cột, nội dung]], 'hanh_dong': {'intro','rows'?,'bullets','anh','luu_y'} | None,
                'phan_trang': [đoạn], 'them': [('h2'|'p'|'b'|'s'|'img'|'tbl', data)]},
  'loc': {'buoc2': chuỗi, 'rows': [[ô, cách dùng]], 'ap_dung': [đoạn], 'anh_ket_qua': chuỗi},
  'form': {'co_tao': True, 'kieu': 'popup'|'trang', 'buoc_tao': [bước], 'anh_tao', 'truong': [[Trường,Kiểu,Bắt buộc,Mặc định,Ghi chú]],
           'sau_truong': [đoạn], 'them': [...], 'nut': [[nút, tác dụng]], 'loi': [[thông báo, nguyên nhân]]},
  'sua': {'buoc': [...], 'anh', 'ghi_chu': [...]} | None,
  'xoa': {'buoc': [...], 'anh', 'ghi_chu': [...]} | None,
  'khoa': {'y_nghia': [...], 'buoc_khoa': [...], 'buoc_mo': [...], 'ghi_chu': [...]} | None,
  'lich_su': {'buoc': [...], 'ghi_chu': [...]} | None,
  'chi_tiet': {'buoc': [...], 'ghi_chu': [...]} | None,
  'phan_rieng': [{'tieu_de': 'CHI NHÁNH NGÂN HÀNG', 'noi_dung': [...]}],
  'xuat': {'buoc': [...], 'truong': chuỗi, 'ghi_chu': [...]} | None,
  'import': {'tieu_de','file','cot_text','toast','loi': [[thông báo, nguyên nhân]],'ghi_chu': [...]} | None,
  'tuy_chinh_cot': {'cot_khoa': 'Ba cột STT, Tên khu vực và Hành động'} | None,
  'shots': {'list': '01_list.png', 'rowmenu', 'filter', 'filter_result', 'create', 'create_error', 'code_error', 'edit',
            'delete', 'lock', 'unlock', 'history', 'detail', 'export', 'import_open', 'import_loaded', 'import_validated', 'colcfg'},
  'srs': {'muc_dich': [...], 'quyen_truoc': [...], 'quyen_rows': [[..]], 'ma_tran': [[header...],[...]], 'quyen_sau': [...],
          'fr': [{'ten','uc','qtc','gioi_thieu':[[Mục,Nội dung]],'menu_them': ' => Tạo mới {icon:btn_taomoi}','ghi_chu_layout',
                  'anh': [(shot key, chú thích)], 'ui': [[header...],[...]], 'ui_widths', 'events': [[event, loại, xử lý]]}],
          'quy_tac': [('BR-01', 'Tên quy tắc', ['dòng mô tả', ...], ['Tạo mới', 'Chỉnh sửa'])]},
}
Chuỗi có thể chèn icon bằng {icon:ten_icon} (btn_taomoi, btn_xuatexcel, btn_import, btn_cauhinhcot, btn_sua, btn_xoa,
btn_bacham, btn_mokhoa, btn_luu, btn_luutieptuc, btn_dong, btn_huy, btn_confirm_xoa, btn_timkiem, btn_lammoi, btn_xuatfile ...).
"""
