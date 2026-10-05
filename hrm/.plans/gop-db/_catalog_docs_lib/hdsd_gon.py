# -*- coding: utf-8 -*-
"""Dựng HDSD bản GỌN cho màn DANH MỤC (skill hdsd-documenter, khuôn HDSD_MAU_GON.docx — 29/09/2026).

Mỗi màn chỉ khai một dict G (mẫu: catalog-docs-v2/provinces/gen_hdsd_gon.py):
  dir, ten, dt (tên đối tượng viết thường), dt_hoa (dạng trong tiêu đề cửa sổ),
  menu [(chữ, icon)x3], thuat_ngu, phien_ban, quyen (list câu, hoặc list [Quyền, Chức năng]),
  bat_buoc, loc: {'o_nhanh', 'bo_loc': [(nhãn, icon)], 'nang_cao': bool, 'khac': 'câu Hoặc…'},
  mo_chi_tiet: 'tên' | 'mã', khoa_icon_thang: bool, xoa_cua_so / khoa_cua_so / mokhoa_cua_so.
Tuỳ biến:
  bo        = {'xoa', 'import', ...}         bỏ phần màn không có
  thay      = {'them': fn(ctx), ...}          viết thay phần chuẩn (màn khác kiểu: form trang riêng…)
  them_phan = [('sua', fn(ctx)), ...]         chèn phần riêng của màn NGAY SAU phần đó
  Khoá phần: truycap, them, sua, xoa, khoa, mokhoa, lichsu, chitiet, xuat, import, cot.
  ctx = dict(w, ic, img, step, sub, sub2, phan, vao, G) — dùng như trong các hàm dưới.
Ảnh trong <dir>/shots, icon ở <dir>/icons rồi tới catalog-docs-v2/icons (dùng chung).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from qg_writer import QgWriter  # noqa: E402
from catalog_v2 import finalize  # noqa: E402

ROOT = os.path.join(HERE, '..', '..', '..')
TPL = os.path.join(ROOT, '.claude', 'skills', 'hdsd-documenter', 'assets', 'HDSD_MAU_GON.docx')
ROLES = {'pagebreak': 33, 'h1': 34, 'h2': 21, 'p': 28, 'step': 43, 'sub': 49, 'sub2': 126,
         'img': 45, 'cap': 46, 'blank': 23, 'tbl2': 22, 'tbl4': 25}
SHARED_ICONS = os.path.join(HERE, '..', 'catalog-docs-v2', 'icons')
ORDER = ['truycap', 'them', 'sua', 'xoa', 'khoa', 'mokhoa', 'lichsu', 'chitiet', 'xuat', 'import', 'cot']


def h1_trang_moi(w, text):
    """Heading 1 sang trang mới bằng thuộc tính 'ngắt trang trước' gắn vào chính tiêu đề.

    KHÔNG dùng đoạn ngắt trang riêng (QgWriter.page_break): khi trang trước vừa kín (ảnh Sơ đồ dài),
    đoạn ngắt bị đẩy sang đầu trang sau rồi mới ngắt → dư 1 TRANG TRẮNG (gặp 29/09/2026).
    """
    from docx.oxml.ns import qn
    w.h1(text, new_page=False)
    el = w.sectPr.getprevious()
    ppr = el.find(qn('w:pPr'))
    if ppr is None:
        ppr = el.makeelement(qn('w:pPr'), {})
        el.insert(0, ppr)
    if ppr.find(qn('w:pageBreakBefore')) is None:
        pb = ppr.makeelement(qn('w:pageBreakBefore'), {})
        ps = ppr.find(qn('w:pStyle'))
        (ps.addnext(pb) if ps is not None else ppr.insert(0, pb))


def anh_lien_chu_thich(w):
    """Gắn 'giữ với đoạn sau' cho đoạn ảnh vừa chèn → chú thích 'Hình N' không bị tách sang trang sau."""
    from docx.oxml.ns import qn
    cap = w.sectPr.getprevious()
    el = cap.getprevious()
    if el is None or not el.findall('.//' + qn('w:drawing')):
        return
    ppr = el.find(qn('w:pPr'))
    if ppr is None:
        ppr = el.makeelement(qn('w:pPr'), {})
        el.insert(0, ppr)
    if ppr.find(qn('w:keepNext')) is None:
        kn = ppr.makeelement(qn('w:keepNext'), {})
        ps = ppr.find(qn('w:pStyle'))
        (ps.addnext(kn) if ps is not None else ppr.insert(0, kn))


def build(G, out):
    D = G['dir']

    def ic(name):
        for d in (os.path.join(D, 'icons'), SHARED_ICONS):
            p = os.path.join(d, name + '.png')
            if os.path.exists(p):
                return ('img', p)
        raise AssertionError('Thiếu icon ' + name)

    w = QgWriter(TPL, ROLES, body_from=19, cover_replace={'Danh mục khu vực': G['ten']})
    step = w.step

    def sub(segs):
        w.raw('sub', segs)

    def sub2(segs):
        w.raw('sub2', segs)

    def img(name, cap):
        w.image(os.path.join(D, 'shots', name + '.png'), caption=cap)
        anh_lien_chu_thich(w)

    dt, DT, TEN = G.get('dt', ''), G.get('dt_hoa', ''), G['ten']
    vao = 'Bước 1: Truy cập vào màn hình %s.' % TEN
    n = [0]

    def phan(title):
        n[0] += 1
        h1_trang_moi(w, 'PHẦN %d: %s' % (n[0], title))

    ctx = dict(w=w, ic=ic, img=img, step=step, sub=sub, sub2=sub2, phan=phan, vao=vao, G=G)

    # ---------------------------------------------------------------- TỔNG QUAN
    h1_trang_moi(w, 'TỔNG QUAN')
    w.h2('1. Thuật ngữ sử dụng trong tài liệu')
    w.table([['Thuật ngữ', 'Giải thích']] + G['thuat_ngu'], widths=[2.0, 4.5])
    w.h2('2. Cập nhật tài liệu')
    w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung']] + G['phien_ban'], widths=[0.9, 1.1, 1.5, 3.0])
    w.h2('3. Quyền sử dụng')
    if G['quyen'] and isinstance(G['quyen'][0], list):
        w.table([['Quyền', 'Chức năng được dùng']] + G['quyen'], widths=[2.3, 4.2])
    else:
        for s in G['quyen']:
            w.p(s)
    w.h2('4. Sơ đồ chức năng tổng quan')
    w.image(os.path.join(D, 'uml', 'overview.png'), caption='Sơ đồ chức năng tổng quan màn ' + TEN)
    anh_lien_chu_thich(w)

    # ---------------------------------------------------------------- các phần chuẩn
    def truycap():
        (m1, i1), (m2, i2), (m3, i3) = G['menu']
        L = G['loc']
        phan('TRUY CẬP VÀ TÌM KIẾM')
        step(['Bước 1: Từ phân hệ %s ' % m1, ic(i1), ', tại menu %s ' % m2, ic(i2), ', chọn %s ' % m3, ic(i3)])
        img('01_list', 'Màn hình ' + TEN)
        step(['Bước 2: Nhập %s vào ô tìm kiếm nhanh ' % L['o_nhanh'], ic('o_timnhanh')])
        step(['Bước 3: Nhấn ', ic('btn_timkiem')])
        k = 4
        bl = L.get('bo_loc', [])
        if bl:
            head = ['Bước %d: ' % k]
            head += (['Bấm ', ic('btn_timkiemnangcao'), ', chọn giá trị trong '] if L.get('nang_cao')
                     else ['Chọn giá trị trong '])
            step(head + [ic(bl[0][1]), ' để lọc theo %s' % bl[0][0]])
            for lb, icon in bl[1:]:
                sub(['Hoặc chọn giá trị ', ic(icon), ' để lọc theo %s' % lb])
            if L.get('khac'):
                sub([L['khac']])
            k += 1
        step(['Bước %d: Chọn ' % k, ic('btn_lammoi'), ' để xóa giá trị đã lọc'])

    def them():
        phan('THÊM MỚI ' + dt.upper())
        step(vao)
        step(['Bước 2: Bấm ', ic('btn_taomoi')])
        img('10_create', 'Cửa sổ Tạo ' + DT)
        step('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: %s.' % ', '.join(G['bat_buoc']))
        step(['Bước 4: Bấm ', ic('btn_luu'), ' để lưu và đóng cửa sổ,'])
        if not G.get('khong_luu_tiep_tuc'):
            sub(['Hoặc ', ic('btn_luutieptuc'), ' để lưu rồi nhập tiếp %s khác.' % dt])
        sub(['Hoặc ', ic('btn_dong'), ' để không lưu thông tin.'])

    def sua():
        phan('CHỈNH SỬA')
        step(vao)
        step(['Bước 2: Bấm nút ', ic('btn_sua'), ' ở cột Hành động.'])
        step('Bước 3: Hệ thống hiển thị cửa sổ “Sửa %s”.' % DT)
        img('12_edit', 'Cửa sổ Sửa ' + DT)
        step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới).')
        step(['Bước 5: Bấm ', ic('btn_luu'), ' để xác nhận thay đổi'])
        sub(['Hoặc ', ic('btn_dong'), ' nếu muốn hủy.'])

    def xoa():
        phan('XÓA')
        step(['Bước 1: Bấm ', ic('btn_xoa'), ' ở cột Hành động'])
        step('Bước 2: Hệ thống hiện hộp xác nhận “%s”' % G['xoa_cua_so'])
        img('13_delete', 'Hộp xác nhận xóa ' + dt)
        step(['Bước 3: Bấm ', ic('btn_confirm_xoa'), ' để xác nhận xóa'])
        sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])

    def khoa():
        phan('KHÓA')
        if G.get('khoa_icon_thang'):
            # tester bỏ mũi tên "→" giữa ba chấm và mục Khóa (sửa tay trên Drive 29/09/2026)
            step(['Bước 1: Chọn Khóa ', ic('btn_khoa_row'), ' hoặc ', ic('btn_bacham_row'), ' ', ic('item_khoa'),
                  ' ở cột Hành động.'])
        else:
            step(['Bước 1: Bấm ', ic('btn_bacham_row'), ' ở cột Hành động, chọn ', ic('item_khoa')])
        step('Bước 2: Hệ thống hiện hộp xác nhận “%s”' % G['khoa_cua_so'])
        img('14_lock', 'Hộp xác nhận khóa ' + dt)
        step(['Bước 3: Bấm ', ic('btn_confirm_khoa'), ' để xác nhận'])
        sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])

    def mokhoa():
        phan('MỞ KHÓA')
        step(['Bước 1: Bấm ', ic('btn_mokhoa_row'), ' ở cột Hành động của %s đang Khóa.' % dt])
        step('Bước 2: Hệ thống hiện hộp xác nhận “%s”' % G['mokhoa_cua_so'])
        img('15_unlock', 'Hộp xác nhận mở khóa ' + dt)
        step(['Bước 3: Bấm ', ic('btn_confirm_mokhoa'), ' để xác nhận'])
        sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])

    def lichsu():
        phan('XEM LỊCH SỬ THAY ĐỔI')
        w.p('Cách 1: Xem từ màn danh sách:')
        if G.get('lichsu_chi_bacham'):
            step(['Ở cột Hành động, bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_lichsu')])
        else:
            step(['Ở cột Hành động, bấm ', ic('btn_lichsu_row')])
            sub(['Hoặc bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_lichsu')])
        w.p('Cách 2: Xem từ màn chi tiết:')
        step('Bước 1: Bấm vào %s %s để mở cửa sổ xem chi tiết' % (G['mo_chi_tiet'], dt))
        step(['Bước 2: Chọn nút ', ic('btn_xemlichsu')])
        img('16_history', 'Cửa sổ Lịch sử thay đổi')

    def chitiet():
        phan('XEM CHI TIẾT ' + dt.upper())
        step(vao)
        step('Bước 2: Bấm vào %s %s. Hệ thống mở cửa sổ “Xem %s”.' % (G['mo_chi_tiet'], dt, DT))
        img('17_detail', 'Xem chi tiết %s ở chế độ chỉ đọc' % dt)

    def xuat():
        phan('XUẤT DANH SÁCH RA EXCEL')
        step('Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
        step(['Bước 2: Bấm nút ', ic('btn_xuatexcel'), '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
        img('20_export', 'Cửa sổ Chọn trường xuất file')
        step('Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.')
        step(['Bước 4: Bấm ', ic('btn_xuatfile')])
        step('Bước 5: Mở file Excel đã xuất.')

    def import_():
        phan('IMPORT %s TỪ FILE EXCEL' % dt.upper())
        step(['Bước 1: Tại màn hình danh sách, bấm ', ic('btn_import'), '. Hệ thống mở cửa sổ “Import %s”.' % dt])
        img('21_import_open', 'Cửa sổ Import %s khi vừa mở' % dt)
        step(['Bước 2: Bấm ', ic('btn_taifilemau'), ' để lấy file mẫu'])
        step('Bước 3: Điền dữ liệu vào file mẫu.')
        step(['Bước 4: Bấm ', ic('btn_chonfile'), ', chọn file vừa điền'])
        step(['Bước 5: Bấm ', ic('btn_load')])
        img('22_import_loaded', 'Dữ liệu đã được load lên bảng xem trước')
        step(['Bước 6: Bấm ', ic('btn_validate'), ' để hệ thống kiểm tra từng dòng.'])
        img('23_import_validated', 'Kết quả kiểm tra — mỗi dòng lỗi nêu rõ lý do')
        step('Bước 7:')
        sub2('Sửa trực tiếp các dòng lỗi trên bảng rồi bấm Validate lại.')
        sub2(['Nếu không muốn nhập các dòng lỗi thì bấm ', ic('btn_bodongloi')])
        sub2(['Muốn sửa lại những dòng đã khoá, bấm ', ic('btn_xoavalidate')])
        step(['Bước 8: Bấm ', ic('btn_import_modal')])

    def cot():
        phan('TÙY CHỈNH CỘT HIỂN THỊ')
        step(['Bước 1: Ở màn danh sách, bấm biểu tượng ', ic('btn_cauhinhcot')])
        img('25_colcfg', 'Cửa sổ Tùy chỉnh cột')
        step('Bước 2: Tích để hiện cột, bỏ tích để ẩn cột.')
        step('Bước 3: Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.')
        step(['Bước 4: Bấm ', ic('btn_luu'), ' để áp dụng'])
        sub(['Hoặc bấm ', ic('btn_dong'), ' nếu muốn bỏ thay đổi.'])

    STD = dict(truycap=truycap, them=them, sua=sua, xoa=xoa, khoa=khoa, mokhoa=mokhoa, lichsu=lichsu,
               chitiet=chitiet, xuat=xuat, import_=import_, cot=cot)
    SKIP = set(G.get('bo', ()))
    CUSTOM = G.get('thay', {})
    EXTRA = G.get('them_phan', [])
    for key in G.get('thu_tu', ORDER):
        if key in CUSTOM:
            CUSTOM[key](ctx)
        elif key not in SKIP and key in ORDER:
            STD['import_' if key == 'import' else key]()
        for after, f in EXTRA:
            if after == key:
                f(ctx)

    w.rebuild_toc(levels=(1, 2))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    w.save(out)
    finalize(out)
    return out
