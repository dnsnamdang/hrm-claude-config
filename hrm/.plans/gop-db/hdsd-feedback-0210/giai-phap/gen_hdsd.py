# -*- coding: utf-8 -*-
"""Cập nhật HDSD_GiaiPhap.docx theo feedback tester 02/10/2026.

GIỮ nguyên nội dung file gốc (bản tải từ Drive), chỉ:
  - sửa tại chỗ các đoạn lệch code hiện tại (đường bấm menu, ô tìm nhanh, URL, nhãn nhiệm vụ);
  - chèn các PHẦN còn thiếu theo đúng thứ tự feedback, trình bày bằng chính style của file
    (nhân bản XML Heading 1 / Heading 2 / bước / ảnh / chú thích có sẵn);
  - chuyển khối "F. Giao việc (task)" vào PHẦN Nhiệm vụ; đánh số lại Hình liên tục.
Chạy: /opt/homebrew/bin/python3 gen_hdsd.py
"""
import copy, os, re
from PIL import Image
from docx import Document
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

R = os.path.dirname(os.path.abspath(__file__)) + '/'
SRC = R + '../drive_orig/HDSD_GiaiPhap.docx'
OUT = R + 'HDSD_GiaiPhap.docx'
SH, IC = R + 'shots/', R + 'icons/'

doc = Document(SRC)
body = doc.element.body
B = list(body)


def text_of(el):
    return ''.join(t.text or '' for t in el.iter(qn('w:t')))


def find(prefix):
    for el in body:
        if text_of(el).strip().startswith(prefix):
            return el
    raise KeyError(prefix)


# ---- nguyên mẫu (đã dò chỉ số trong file gốc) ----
P_H1 = B[48]        # PHẦN 2 …
P_H2 = B[50]        # A. Tạo mới giải pháp
P_STEP = B[51]      # Bước A1 (bullet ●, "Bước" in đậm)
P_IMG = B[52]
P_CAP = B[53]
P_TXT = B[49]       # đoạn văn thường
RPR_B = copy.deepcopy(P_STEP.findall(qn('w:r'))[0].find(qn('w:rPr')))   # đậm
RPR_N = copy.deepcopy(P_STEP.findall(qn('w:r'))[2].find(qn('w:rPr')))   # thường
RPR_H1 = copy.deepcopy(P_H1.findall(qn('w:r'))[0].find(qn('w:rPr')))
RPR_H2 = copy.deepcopy(P_H2.findall(qn('w:r'))[0].find(qn('w:rPr')))
RPR_CAP = copy.deepcopy(P_CAP.findall(qn('w:r'))[0].find(qn('w:rPr')))


def _clone(proto):
    p = copy.deepcopy(proto)
    for ch in list(p):
        if ch.tag != qn('w:pPr'):
            p.remove(ch)
    return p


def _run(rpr, text=None, inline=None):
    r = OxmlElement('w:r')
    r.append(copy.deepcopy(rpr))
    if inline is not None:
        d = OxmlElement('w:drawing'); d.append(inline); r.append(d)
    else:
        t = OxmlElement('w:t'); t.set(qn('xml:space'), 'preserve'); t.text = text; r.append(t)
    return r


def _inline(path, h=0.22, w=None):
    if w:
        return doc.part.new_pic_inline(path, Inches(w), None)
    return doc.part.new_pic_inline(path, None, Inches(h))


def fill(p, segs, bold_first=False):
    """segs: chuỗi | ('b', chữ đậm) | ('img', tên icon)."""
    for s in segs:
        if isinstance(s, tuple) and s[0] == 'img':
            path = s[1] if s[1].startswith('/') else IC + s[1] + '.png'
            p.append(_run(RPR_N, inline=_inline(path)))
        elif isinstance(s, tuple) and s[0] == 'b':
            p.append(_run(RPR_B, s[1]))
        else:
            p.append(_run(RPR_N, s))
    return p


NEW = []   # các phần tử chèn mới, theo thứ tự


def h1(text):
    p = _clone(P_H1)
    ppr = p.find(qn('w:pPr'))
    pb = OxmlElement('w:pageBreakBefore'); ppr.insert(1, pb)   # sang trang bằng chính tiêu đề
    p.append(_run(RPR_H1, text)); NEW.append(p)


def _bold_heading(p):
    # tiêu đề lấy rPr của chính heading mẫu (font TNR, đen) để giống heading cũ
    pass


def h2(text):
    p = _clone(P_H2); p.append(_run(RPR_H2, text)); NEW.append(p)


def step(n, segs):
    p = _clone(P_STEP); p.append(_run(RPR_B, 'Bước %s:' % n)); p.append(_run(RPR_N, ' '))
    fill(p, segs); NEW.append(p)


def sub(segs):
    p = _clone(P_STEP)
    ppr = p.find(qn('w:pPr'))
    num = ppr.find(qn('w:numPr'))
    if num is not None:
        ppr.remove(num)
    ind = ppr.find(qn('w:ind'))
    ind.set(qn('w:left'), '720'); ind.set(qn('w:hanging'), '0')
    fill(p, segs); NEW.append(p)


def txt(segs):
    p = _clone(P_TXT); fill(p, segs); NEW.append(p)


def image(path, caption):
    im = Image.open(path); w, h = im.size
    width = 6.0
    if h / w * width > 4.3:
        width = 4.3 * w / h
    p = _clone(P_IMG)
    ppr = p.find(qn('w:pPr'))
    kn = OxmlElement('w:keepNext'); ppr.insert(0, kn)          # ảnh dính chú thích
    p.append(_run(OxmlElement('w:rPr'), inline=_inline(path, w=width)))
    NEW.append(p)
    c = _clone(P_CAP); c.append(_run(RPR_CAP, 'Hình 0: ' + caption)); NEW.append(c)


def set_text(p, segs_or_text):
    """Thay nội dung 1 đoạn cũ, giữ pPr + rPr của run đầu (cho đoạn thường) / Bước đậm."""
    for ch in list(p):
        if ch.tag != qn('w:pPr'):
            p.remove(ch)
    if isinstance(segs_or_text, str):
        segs_or_text = [segs_or_text]
    fill(p, segs_or_text)


def set_step(p, label, segs):
    for ch in list(p):
        if ch.tag != qn('w:pPr'):
            p.remove(ch)
    p.append(_run(RPR_B, label)); p.append(_run(RPR_N, ' '))
    fill(p, segs)


MENU = ['Từ phân hệ ', ('img', 'menu_cong_viec'), ', tại menu ', ('img', 'menu_lam_giai_phap'),
        ', chọn ', ('img', 'menu_quan_ly_giai_phap'), '.']
def open_mgr(cond='cần thao tác'):
    return ['Tại dòng giải pháp ' + cond + ', bấm ', ('img', 'btn_quan_ly_row'),
            ' (Quản lý giải pháp) ở cột Hành động. Hệ thống mở màn hình Quản lý giải pháp.']


OPEN_MGR = open_mgr()

# =====================================================================
# 1) SỬA TẠI CHỖ phần cũ cho khớp code hiện tại
# =====================================================================
set_text(find('Trên menu trái, vào nhóm'), 'Từ phân hệ “Công việc”, tại menu “Làm giải pháp” chọn:')
p = find('“Dự án tiền khả thi” (đường dẫn')
set_text(p, '“Quản lý giải pháp” — màn hình quản lý toàn bộ giải pháp: tạo mới, phê duyệt tiếp nhận, '
            'phân công PM/Leader/nhân sự, nhiệm vụ, vấn đề, hồ sơ trình duyệt, version và tiến độ.')
set_step(find('Bước 2: Menu bên trái'), 'Bước 2:', MENU)
set_step(find('Bước 1: Nhập từ khoá vào ô tìm nhanh'), 'Bước 1:',
         ['Nhập từ khoá vào ô tìm nhanh (tìm theo mã giải pháp, tên giải pháp, mã khách hàng, tên khách hàng).'])
h1_old2 = find('PHẦN 2: THIẾT KẾ GIẢI PHÁP')
for r in h1_old2.findall(qn('w:r')):
    for t in r.iter(qn('w:t')):
        t.text = 'PHẦN 2: TẠO MỚI GIẢI PHÁP, HẠNG MỤC VÀ PHÂN CÔNG LEADER'
set_text(find('Đây là hướng dẫn thao tác chi tiết cho Bước'),
         'Đây là hướng dẫn thao tác chi tiết cho bước “Thiết kế giải pháp”: tạo giải pháp, khai báo hạng mục, '
         'phân công Leader và nhân sự cho hạng mục. Mỗi bước đều có ảnh minh hoạ.')
set_step(find('Bước A1:'), 'Bước A1:',
         ['Vào phân hệ ', ('img', 'menu_cong_viec'), ' → menu ', ('img', 'menu_lam_giai_phap'), ' → ',
          ('img', 'menu_quan_ly_giai_phap'), ', bấm nút ', ('img', 'btn_tao_moi'),
          '. Màn “Tạo giải pháp” mở ra gồm 3 tab: Thông tin · Quản lý hạng mục · Sơ đồ nhân sự.'])

# câu tham chiếu cuối phần hạng mục/Leader (feedback: chi tiết sang HDSD hạng mục)
cap15 = find('Hình 15:')
ref = _clone(P_TXT)
fill(ref, ['Chi tiết các thao tác với hạng mục (sửa, Leader duyệt hạng mục, hồ sơ trình duyệt hạng mục) xem ',
           ('b', 'HDSD Hạng mục giải pháp'), '.'])
cap15.addnext(ref)

# Khối F (giao việc task) — tách ra, sửa nhãn, chèn lại vào PHẦN Nhiệm vụ
f_head = find('F. Giao việc (task)')
F = []
el = f_head
while el is not None and el.tag != qn('w:sectPr'):
    nxt = el.getnext(); F.append(el); body.remove(el); el = nxt
for t in f_head.iter(qn('w:t')):
    t.text = ''
f_head.findall(qn('w:r'))[0].find(qn('w:t')).text = 'Giao việc (nhiệm vụ) từ menu Nhiệm vụ'


def fx(prefix, label, segs):
    for e in F:
        if text_of(e).strip().startswith(prefix):
            set_step(e, label, segs); return
    raise KeyError(prefix)


fx('Bước F1:', 'Bước F1:', ['Vào phân hệ ', ('img', 'menu_cong_viec'), ' → menu “Nhiệm vụ” → “Nhiệm vụ”, bấm ',
                            ('img', 'btn_tao_moi'), '. Cửa sổ “Thêm mới nhiệm vụ” mở ra.'])
fx('Bước F2:', 'Bước F2:', ['Chọn “Loại nhiệm vụ” và nhập “Tên công việc” (đều bắt buộc).'])
fx('Bước F7:', 'Bước F7:', ['(tuỳ chọn) Bấm “Chế độ nâng cao” để khai báo thêm: Người duyệt kết quả, Người theo dõi, '
                            'Thẻ, Checklist, Nhiệm vụ con, Lặp lại, Yêu cầu báo cáo tiến độ.'])
fx('Bước F8:', 'Bước F8:', ['Bấm “Lưu” (hoặc “Lưu & Tiếp tục” để tạo nhiệm vụ tiếp theo). Tuỳ cấu hình, nhiệm vụ sẽ ở '
                            'trạng thái “Chờ phê duyệt triển khai” hoặc “Chờ bắt đầu”. Chi tiết luồng thực hiện/duyệt '
                            'nhiệm vụ xem ', ('b', 'HDSD Nhiệm vụ'), '.'])

# nhãn "task" cũ -> "nhiệm vụ" (menu/cửa sổ đã đổi tên)
for e in F:
    for t in e.iter(qn('w:t')):
        if t.text:
            t.text = re.sub(r'\btask\b', 'nhiệm vụ', re.sub(r'\bTask\b', 'nhiệm vụ', t.text))

# =====================================================================
# 2) CÁC PHẦN CHÈN MỚI (thứ tự theo feedback)
# =====================================================================
h1('PHẦN 3: THÊM NHÂN SỰ GIẢI PHÁP')
step(1, MENU)
step(2, OPEN_MGR)
step(3, ['Chọn thẻ ', ('img', 'tab_nhan_su'), '.'])
step(4, ['Bấm ', ('img', 'btn_them_nhan_su'), ', hệ thống mở cửa sổ “Thêm nhân sự vào hạng mục”.'])
image(SH + '03_them_nhan_su.png', 'Cửa sổ Thêm nhân sự vào hạng mục')
step(5, ['Chọn đầy đủ thông tin bắt buộc: Hạng mục, Thành viên, Vai trò dự án, Ngày bắt đầu; nhập Mô tả công việc nếu cần.'])
sub(['Giải pháp không có hạng mục: cửa sổ là “Thêm nhân sự vào dự án”, không có ô Hạng mục.'])
step(6, ['Bấm ', ('img', 'btn_them_nhan_su_modal'), ' để lưu.'])
sub(['Hoặc bấm ', ('img', 'btn_huy_modal'), ' để không lưu.'])

h1('PHẦN 4: ĐỔI PM')
step(1, MENU)
step(2, OPEN_MGR)
step(3, ['Chọn thẻ ', ('img', 'tab_nhan_su'), '.'])
step(4, ['Bấm ', ('img', 'btn_phan_cong'), ', hệ thống mở cửa sổ “Phân công quản lý”.'])
image(SH + '04_doi_pm.png', 'Cửa sổ Phân công quản lý — Phân công PM')
step(5, ['Tại Loại phân công, chọn “Phân công PM”.'])
step(6, ['Chọn Vai trò mới trong giải pháp/hạng mục cho PM cũ và Hạng mục cho PM cũ.'])
sub(['Hoặc để trống Vai trò mới nếu PM cũ rời giải pháp.'])
step(7, ['Chọn PM mới, nhập Ghi chú (tối thiểu 50 ký tự).'])
step(8, ['Bấm ', ('img', 'btn_xac_nhan_phan_cong'), ' để đổi PM.'])
sub(['Hoặc bấm ', ('img', 'btn_dong_pc'), ' để không lưu.'])
step(9, ['Bấm ', ('img', 'btn_ls_phan_cong'), ' để xem lại các lần phân công.'])

h1('PHẦN 5: PM PHÊ DUYỆT TIẾP NHẬN GIẢI PHÁP')
step(1, MENU)
step(2, ['Tại dòng giải pháp ở trạng thái “Chờ PM duyệt”, bấm ', ('img', 'btn_giao_leader_row'),
         ' (Giao cho Leader) ở cột Hành động. Hệ thống mở màn hình “Duyệt giải pháp”.'])
step(3, ['Kiểm tra thông tin ở thẻ Thông tin và thẻ ', ('img', 'tab_quan_ly_hang_muc'),
         '; bổ sung hạng mục, Leader hạng mục nếu cần.'])
image(SH + '05_pm_duyet.png', 'Màn hình Duyệt giải pháp')
step(4, ['Bấm ', ('img', 'btn_giao_leader'), ' để đồng ý tiếp nhận và giao hạng mục cho Leader.'])
sub(['Giải pháp không có hạng mục: nút là “Lưu và duyệt”, giải pháp chuyển thẳng sang “Đang triển khai”.'])
sub(['Hoặc bấm ', ('img', 'btn_quay_lai'), ' để không duyệt.'])
step(5, ['Leader từng hạng mục bấm ', ('img', 'btn_luu_duyet_row'), ' (Lưu và duyệt) ở cột Hành động rồi bấm ',
         ('img', 'btn_luu_duyet'), '. Khi các hạng mục đã duyệt, giải pháp chuyển sang “Đang triển khai” '
         '(chi tiết xem ', ('b', 'HDSD Hạng mục giải pháp'), ').'])

h1('PHẦN 6: PM TẠO / CẬP NHẬT / XÓA NHIỆM VỤ')
step(1, MENU)
step(2, OPEN_MGR)
step(3, ['Chọn thẻ ', ('img', 'tab_nhiem_vu'), '.'])
image(SH + '06_nhiem_vu.png', 'Thẻ Nhiệm vụ của giải pháp')
step(4, ['Bấm ', ('img', 'btn_tao_moi'), ' để tạo nhiệm vụ.'])
sub(['Hoặc bấm ', ('img', 'btn_sua_task'), ' (Sửa) dưới tên nhiệm vụ để cập nhật.'])
sub(['Hoặc bấm ', ('img', 'btn_xoa_task'), ' (Xoá) dưới tên nhiệm vụ để xóa (chỉ nhiệm vụ Nháp do mình tạo).'])
txt(['Chi tiết các trường nhập và luồng thực hiện nhiệm vụ xem ', ('b', 'HDSD Nhiệm vụ'), '.'])
NEW.extend(F)

h1('PHẦN 7: PM THÊM / SỬA / XÓA / BÁO CÁO KẾT QUẢ VẤN ĐỀ (ISSUE)')
step(1, MENU)
step(2, OPEN_MGR)
step(3, ['Chọn thẻ ', ('img', 'tab_van_de'), '.'])
image(SH + '07_van_de.png', 'Thẻ Vấn đề giải pháp')
step(4, ['Bấm ', ('img', 'btn_tao_moi'), ' để thêm vấn đề.'])
sub(['Hoặc bấm ', ('img', 'btn_sua_issue'), ' (Sửa) dưới tên vấn đề để sửa.'])
sub(['Hoặc bấm ', ('img', 'btn_xoa_issue'), ' (Xoá) dưới tên vấn đề để xóa.'])
sub(['Hoặc người xử lý bấm ', ('img', 'btn_xu_ly_issue'), ' (Xử lý) để báo cáo kết quả xử lý.'])
txt(['Chi tiết các trường nhập và luồng xử lý vấn đề xem ', ('b', 'HDSD Vấn đề'), '.'])

h1('PHẦN 8: PM TRÌNH DUYỆT HỒ SƠ GIẢI PHÁP')
step(1, MENU)
step(2, open_mgr('ở trạng thái “Đang triển khai”'))
step(3, ['Bấm ', ('img', 'btn_tao_ho_so'), ', hệ thống mở cửa sổ “Tạo hồ sơ trình duyệt”.'])
image(SH + '08_tao_ho_so.png', 'Cửa sổ Tạo hồ sơ trình duyệt')
step(4, ['Nhập đầy đủ thông tin bắt buộc: Tên hồ sơ, Nội dung trình duyệt, Hạn duyệt; thêm file ở Danh sách các file nếu cần.'])
step(5, ['Bấm ', ('img', 'btn_luu_trinh_duyet'), ' để gửi Trưởng phòng giải pháp duyệt.'])
sub(['Hoặc bấm ', ('img', 'btn_luu'), ' để lưu nháp hồ sơ.'])
sub(['Hoặc bấm ', ('img', 'btn_dong'), ' để không lưu.'])

h1('PHẦN 9: TRƯỞNG PHÒNG GIẢI PHÁP PHÊ DUYỆT HỒ SƠ GIẢI PHÁP')
step(1, MENU)
step(2, OPEN_MGR)
step(3, ['Chọn thẻ ', ('img', 'tab_ho_so'), ', tại hồ sơ “Chờ duyệt” bấm ', ('img', 'btn_duyet_row'),
         ' (Duyệt). Hệ thống mở cửa sổ “Duyệt hồ sơ trình duyệt”.'])
image(SH + '09_tp_duyet.png', 'Cửa sổ Duyệt hồ sơ trình duyệt')
step(4, ['Bấm ', ('img', 'btn_duyet'), ' để duyệt hồ sơ.'])
sub(['Hoặc bấm ', ('img', 'btn_tu_choi'), ', nhập Lý do từ chối rồi bấm ', ('img', 'btn_dong_y'),
     ' (bấm ', ('img', 'btn_khong'), ' để quay lại).'])
sub(['Hoặc bấm ', ('img', 'btn_dong'), ' để đóng cửa sổ.'])

h1('PHẦN 10: TẠO VERSION MỚI')
step(1, MENU)
step(2, open_mgr('ở trạng thái “Đã duyệt giải pháp”, “Đã duyệt giá” hoặc “Chờ làm giá”'))
step(3, ['Bấm ', ('img', 'btn_tao_version'), ', hệ thống mở cửa sổ “Tạo phiên bản mới”.'])
image(SH + '10_tao_version.png', 'Cửa sổ Tạo phiên bản mới')
step(4, ['Nhập Mô tả, chọn Ngày kết thúc.'])
step(5, ['Bấm ', ('img', 'btn_tao_moi_version'), ' để tạo version.'])
sub(['Hoặc bấm ', ('img', 'btn_dong_version'), ' để không lưu.'])

h1('PHẦN 11: THIẾT LẬP % HẠNG MỤC')
step(1, MENU)
step(2, OPEN_MGR)
step(3, ['Chọn thẻ ', ('img', 'tab_tien_do'), '.'])
image(SH + '11_tien_do.png', 'Thẻ Tiến độ — Phân bổ tiến độ theo hạng mục')
step(4, ['Nhập tỷ lệ ở cột Phân bổ (%) cho từng hạng mục sao cho tổng bằng 100%. Hệ thống tự lưu.'])

sect = body.find(qn('w:sectPr'))
for e in NEW:
    sect.addprevious(e)

# =====================================================================
# 3) ĐÁNH SỐ LẠI HÌNH liên tục
# =====================================================================
n = 0
for p in body.iter(qn('w:p')):
    s = text_of(p)
    m = re.match(r'\s*Hình\s+\d+\s*:(.*)', s, re.S)
    if not m:
        continue
    n += 1
    runs = [r for r in p.findall(qn('w:r')) if r.find(qn('w:t')) is not None]
    runs[0].find(qn('w:t')).text = 'Hình %d:%s' % (n, m.group(1))
    for r in runs[1:]:
        r.find(qn('w:t')).text = ''
print('Số hình:', n)

doc.save(OUT)
print('Đã lưu', OUT)
