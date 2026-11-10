# -*- coding: utf-8 -*-
"""Testcase màn "Theo dõi theo kho" (phân hệ Kho, mục cấp 1, 2 trang) — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026
(tc_chuan.build_chuan, loai='bao_cao').

Chạy: python gen_testcase.py -> testcase.xlsx (sau đó chạy check_tc ... bao_cao, phải 0 lỗi).
LOẠI 'bao_cao' (đọc code 10/11/2026): màn THEO DÕI chỉ đọc — 4 lời gọi GET (danh sách kho, nguồn ô lọc, dữ liệu xuất Excel, hoạt động
1 kho), không Thêm / Sửa / Xóa / Khóa / Duyệt / Import / Lịch sử; trang 2 có khối tổng hợp đếm phiếu + trạng thái / Tổng thời gian xử lý
suy ra từ mốc thời gian, trang 1 có tổng số kho phải khớp danh mục Kho vật lý → cần nhóm SỐ LIỆU BÁO CÁO để đối soát (loại 'danh_muc' không
có nhóm đó). Tô màu dòng theo thời gian chờ ĐÃ BỎ 29/10/2026 (#11901) → không có case màu.
Nhóm có mặt: I Hiển thị · II Tìm kiếm & lọc · III Số liệu báo cáo · IV Xem chi tiết (trang hoạt động của kho + mở phiếu đề nghị) ·
V Tùy chỉnh cột · VI Xuất danh sách Excel · VII Ràng buộc · VIII Phân quyền. Không có In thì bỏ nhóm.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../hoat-dong-kho/gen_testcase.py (10/11, check_tc 0 lỗi).
Số liệu mẫu dev-hrm 10/11/2026 (_capture/probe.js + capture.js, chỉ đọc): 22 kho mọi công ty (21 Hoạt động + 1 Khóa), công ty Tân Phát 8
kho, Nhóm Kho Hà Nội 4 kho; kho PTT 55 phiếu = 40 đề nghị xuất + 15 đề nghị nhập (34 Đã nhận đề nghị, 12 Đang lấy hàng, 9 Đang xếp
hàng, 0 Đã hoàn thành); MT 5 = 1 + 4; KTCN 2 = 2 + 0.
"""
import os
import sys
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
from tc_chuan import build_chuan  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Kho > bấm mục "Theo dõi theo kho" (mục cấp 1, không có nhóm con).'
EMPTY = 'Không có dữ liệu phù hợp'
LOADERR = 'Lỗi khi tải dữ liệu'
NOPERM = 'Bạn không có quyền thực hiện chức năng này'
P404 = 'trang "KHÔNG TÌM THẤY TRANG YÊU CẦU" ("Không tìm thấy hoặc không được cấp quyền truy cập trang")'
FILE1 = 'theo_doi_theo_kho.xlsx'
FILE2 = 'hoat_dong_kho_PTT.xlsx'
DNXK = 'Phiếu đề nghị xuất kho'
DNNK = 'Phiếu đề nghị nhập kho'
T2 = 'Hoạt động nhập/xuất kho PTT - Phan Trọng Tuệ'
ACC_A = ('Tài khoản A: DNS Admin (Super Admin) — có quyền "Quản lý kho" và "Xem danh mục kho của tất cả công ty".\n'
         'Dev 10/11/2026: 22 kho (21 Hoạt động + 1 Khóa MT-KNXT) của 6 công ty.')
ACC_C = ('Tài khoản C: có quyền "Quản lý kho", KHÔNG có quyền xem mọi công ty; công ty đang làm: CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN '
         'PHÁT (8 kho: DATD, N10, N9, KTCN, SL, CSKH, LN, PTT).')
ACC_N = 'Tài khoản N: KHÔNG có quyền "Quản lý kho".'
OPEN = [MENU]
OPEN2 = OPEN + ['Tìm "PTT", bấm mã PTT (trang hoạt động mở ở tab mới).']
VIEW_DNXK = 'Vào phân hệ Kho > menu "Xuất kho" > "Phiếu đề nghị xuất kho".'
VIEW_DNNK = 'Vào phân hệ Kho > menu "Nhập kho" > "Phiếu đề nghị nhập kho".'
VIEW_KVL = 'Vào phân hệ Kho > menu "Danh mục" > "Kho vật lý".'
TIP_KHOI = ('HOẠT ĐỘNG NHẬP/XUẤT KHO PTT - PHAN TRỌNG TUỆ • Phiếu đề nghị xuất kho và đề nghị nhập kho của kho này • Gồm phiếu đang xử lý '
            'và phiếu nhận trong hôm nay (kể cả đã hoàn thành) • Danh sách tự tải lại mỗi 60 giây')
COLS2 = ('STT, Phiếu đề nghị, Loại, Người yêu cầu, Hình thức vận chuyển, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn '
         'thành, Trạng thái, Tổng thời gian xử lý')
FIELDS2 = ('Phiếu đề nghị, Loại, Người yêu cầu, Hình thức vận chuyển, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn '
           'thành, Trạng thái, Tổng thời gian xử lý')
TEST_ENV = 'Môi trường kiểm thử (không làm trên dữ liệu thật).'

CK = defaultdict(list)


def T(no, func, prio, pre, steps, td, exp):
    if isinstance(pre, (list, tuple)):
        pre = '\n'.join(pre)
    if isinstance(td, (list, tuple)):
        td = '\n'.join(td)
    st = '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(steps))
    ex = '\n'.join(x if x.startswith('- ') else '- ' + x for x in exp)
    return ('%03d' % no, func, prio, pre, st, td, ex)


class Sec(list):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    def add(self, func, prio, pre, steps, td, exp, ck=()):
        self.append(T(len(self) + 1, func, prio, pre, steps, td, exp))
        tid = 'TC_%02d.%s' % (self.idx, self[-1][0])
        for s in (ck if isinstance(ck, (list, tuple)) else [ck]):
            CK[s].append(tid)


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn theo dõi 2 trang: trang 1 liệt kê kho vật lý trong phạm vi (Mã, Tên, Nhóm, Công ty, phân trang); bấm Mã / Tên mở trang 2 '
     '(tab mới) là bảng %s và %s của RIÊNG kho đó — phiếu đang xử lý và phiếu nhận trong hôm nay — kèm 3 ô tổng hợp (Tổng số phiếu '
     'nhận, Tổng hoàn thành, Tổng chưa xử lý), tự tải lại mỗi 60 giây. Chỉ đọc: tìm / lọc, sắp xếp, mở phiếu, Tùy chỉnh cột, Xuất Excel '
     'ở cả 2 trang.' % (DNXK, DNNK)),
    ('2. Đối tượng được tính / hiển thị',
     '- Trang 1: kho vật lý chưa xóa (cả kho Hoạt động và kho Khóa) trong phạm vi công ty.\n'
     '- Trang 2: phiếu đề nghị xuất / nhập của kho, trạng thái Chờ duyệt hoặc Đang xuất kho / Đang nhập kho (bất kể ngày); hoặc nhận từ '
     '00:00 hôm nay mà không phải Đang tạo / Đã hủy.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Trang 1: kho đã xóa; kho của công ty khác (người không được xem mọi công ty).\n'
     '- Trang 2: phiếu Đang tạo, Đã hủy; phiếu đã xong mà nhận trước hôm nay; phiếu của kho khác.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Không có ô lọc thời gian. Mốc "hôm nay" ở trang 2 tính theo Thời gian nhận từ 00:00 ngày hiện tại.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Trang 1: bảng phẳng 5 cột, 10 dòng/trang, mặc định kho tạo mới nhất trước.\n'
     '- Trang 2: bảng phẳng 11 cột, không phân trang, phiếu chưa hoàn thành trước, trong nhóm Thời gian nhận mới nhất trước.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Mỗi kho 1 dòng; mỗi phiếu 1 dòng (đề nghị xuất và đề nghị nhập trùng số thứ tự vẫn là 2 dòng).\n'
     '- Trạng thái: có Thời gian hoàn thành thì Đã hoàn thành; có Thời gian lấy/xếp hàng thì Đang lấy hàng (đề nghị xuất) / Đang xếp hàng '
     '(đề nghị nhập); còn lại Đã nhận đề nghị.'),
    ('7. Phân quyền cấp',
     '- Cần quyền "Quản lý kho" cho cả 2 trang; không có thì không thấy menu, mở thẳng ra trang không tìm thấy.\n'
     '- Không có quyền "Xem danh mục kho của tất cả công ty": chỉ kho công ty đang làm, không có ô lọc Công ty.\n'
     '- Có quyền đó (Super Admin có sẵn): mọi công ty + ô lọc Công ty.'),
    ('8. Cách tính các ô thống kê',
     '- Trang 1: "Hiển thị a–b / N", N = số kho theo bộ lọc.\n'
     '- Trang 2: Tổng số phiếu nhận = số dòng (sau tìm); Tổng hoàn thành = số dòng "Đã hoàn thành"; Tổng chưa xử lý = hiệu 2 số.\n'
     '- Tổng thời gian xử lý = Thời gian hoàn thành - Thời gian nhận, "x ngày y giờ z phút", dưới 1 phút "Vài giây".'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản: A (Super Admin, mọi công ty), C (Quản lý kho, công ty Tân Phát), N (không có Quản lý kho).\n'
     '- Lưu ý: số phiếu trang 2 đổi theo thời gian thực (tự tải lại 60 giây) — ghi lại số trước khi đối soát; dev 10/11/2026 sáng PTT 54, '
     'trưa 55 (thêm PDNXK-39058).\n'
     '- Lưu ý: trang 2 không phân trang; nhóm Phân trang của checklist kiểm ở trang 1.\n'
     '- Lưu ý: không còn tô màu dòng theo thời gian chờ (bỏ theo yêu cầu 29/10/2026).'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', ACC_A, OPEN, '—',
       ['Mở trang "Theo dõi theo kho", không báo lỗi.', 'Khối "Bộ lọc danh sách" và bảng danh sách kho, "Hiển thị 1–10 / 22".'], [1, 6])
S1.add('Tiêu đề màn hình', 'P1', ACC_A, OPEN + ['Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi là "Theo dõi theo kho".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', ACC_A, OPEN + ['Quan sát các khối.'], '—',
       ['Khối lọc: ô "Tìm theo mã, tên kho", ô Nhóm, ô Công ty, nút Tìm kiếm, Làm mới (một hàng).',
        'Đầu bảng: Xuất Excel, biểu tượng Cấu hình cột hiển thị.',
        'KHÔNG có Tạo mới, Sửa, Xóa, Import, In, cột Hành động, Tìm kiếm nâng cao, Cài đặt bộ lọc.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', ACC_A, OPEN + ['Đọc tiêu đề cột.'], '—',
       ['Đủ 5 cột: STT, Mã, Tên, Nhóm, Công ty.', 'Biểu tượng sắp xếp ở cột Mã, Tên.'], 4)
S1.add('Không có cột ẩn mặc định', 'P2', ACC_A, OPEN + ['Bấm Cấu hình cột hiển thị.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" tích đủ 5 cột, "Đang chọn 5/5 cột".'], 5)
S1.add('Dữ liệu dòng đúng với danh mục kho', 'P0', ACC_A, OPEN + ['Tìm "PTT".', VIEW_KVL + ' Tìm kho PTT để so.'], 'Tìm: PTT',
       ['Dòng PTT: Tên "Phan Trọng Tuệ", Nhóm "Kho Hà Nội", Công ty "CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT" — khớp danh mục Kho vật lý.',
        'Kho chưa gắn nhóm (vd EG_LN) để trống cột Nhóm.'], 6)
S1.add('Kho đang Khóa vẫn hiện', 'P1', [ACC_A, 'Kho MT-KNXT đang ở trạng thái Khóa ở danh mục Kho vật lý.'], OPEN + ['Tìm "MT-KNXT".'],
       'Tìm: MT-KNXT', ['Kho MT-KNXT vẫn có trong danh sách (bảng không có cột trạng thái); bấm vào vẫn xem được hoạt động.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', ['Tài khoản có quyền "Quản lý kho" nhưng chưa được gắn công ty nào.'], OPEN, '—',
       ['Bảng "%s", dòng dưới bảng "Không có kho nào."; không báo lỗi, không hiện kho không thuộc công ty nào.' % EMPTY], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', ACC_A, OPEN + ['Nhập "ZZZ999", nhấn Enter.'], 'Tìm: ZZZ999',
       ['Bảng "%s"; dưới bảng "Không có kho nào."' % EMPTY], [9, 30, 40])
S1.add('Số dòng mặc định mỗi trang', 'P0', ACC_A, OPEN, '—',
       ['Ô Số dòng/trang = 10; trang 1 có 10 dòng; "Hiển thị 1–10 / 22"; thanh trang 1, 2, 3.'], 10)
S1.add('Đổi số dòng mỗi trang', 'P1', ACC_A, OPEN + ['Bấm trang 2.', 'Chọn Số dòng/trang = 50.'], '—',
       ['Về trang 1, đủ 22 dòng, "Hiển thị 1–22 / 22"; lựa chọn có 5, 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / tiếp theo', 'P1', ACC_A, OPEN + ['Bấm ›.', 'Bấm ‹.'], '—',
       ['Bấm ›: trang 2, "Hiển thị 11–20 / 22", dòng 11 là MT-KNXT.', 'Bấm ‹: về trang 1.'], 12)
S1.add('Trang đầu / cuối', 'P1', ACC_A, OPEN + ['Bấm ».', 'Bấm «.'], '—',
       ['Bấm »: trang 3, "Hiển thị 21–22 / 22".', 'Bấm «: trang 1.'], 13)
S1.add('Trạng thái nút ở trang đầu / cuối', 'P2', ACC_A, OPEN + ['Quan sát thanh trang ở trang 1, rồi ở trang 3.'], '—',
       ['Trang 1: « và ‹ mờ, không bấm được.', 'Trang 3: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P1', ACC_A, OPEN + ['Bấm trang 2.'], '—', ['STT bắt đầu 11 tới 20 (không quay về 1).'], 15)
S1.add('Tổng số bản ghi', 'P0', ACC_A, OPEN, '—', ['Dòng "Hiển thị 1–10 / 22": 22 = tổng số kho trong phạm vi.'], 16)
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', ACC_A, OPEN + ['Bấm trang 2.', 'Chọn Nhóm = Kho Hà Nội.'], '—',
       ['Về trang 1, "Hiển thị 1–4 / 4".'], 17)
S1.add('Thứ tự mặc định', 'P0', ACC_A, OPEN, '—',
       ['Kho tạo mới nhất ở trên: 1 EG_LN, 2 DATD, 3 SGSX, 4 ETG, 5 EG2-LN…'], 19)
S1.add('Sắp xếp tăng dần theo Mã', 'P0', ACC_A, OPEN + ['Bấm tiêu đề "Mã".'], '—',
       ['Mũi tên lên; mã xếp A đến Z: CB, CSKH, DATD…'], 20)
S1.add('Sắp xếp giảm dần theo Mã', 'P0', ACC_A, OPEN + ['Bấm "Mã" 2 lần.'], '—', ['Mũi tên xuống; đầu bảng SL, SGSX, SG-KHOAO.'], 21)
S1.add('Sắp xếp theo Tên', 'P1', ACC_A, OPEN + ['Bấm tiêu đề "Tên".'], '—', ['Tên xếp A đến Z: Cát Bà, Chăm sóc khách hàng, ETEK GROUP…'],
       [20, 22])
S1.add('Cột không hỗ trợ sắp xếp', 'P2', ACC_A, OPEN + ['Bấm tiêu đề Nhóm, Công ty, STT.'], '—',
       ['Không có biểu tượng sắp xếp, thứ tự không đổi.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', ACC_A, OPEN + ['Bấm "Mã" (tăng).', 'Bấm trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự Mã tăng dần (dòng 11 tiếp sau dòng 10 theo chữ cái).'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', ACC_A, OPEN + ['Bấm trang 3.', 'Bấm "Tên".'], '—', ['Về trang 1, theo Tên tăng dần.'], 25)
S1.add('Bấm Mã kho mở tab mới', 'P0', ACC_A, OPEN + ['Bấm mã "PTT".'], '—',
       ['Mở TAB MỚI trang "%s"; tab danh sách giữ nguyên trang, bộ lọc.' % T2], [1, 186])
S1.add('Phiên đăng nhập hết hạn', 'P2', [ACC_A, 'Phiên đăng nhập đã hết hạn.'], OPEN + ['Bấm Tìm kiếm.'], '—',
       ['Chuyển về màn đăng nhập, không hiện dữ liệu.'], 39)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm đúng mã đầy đủ', 'P0', ACC_A, OPEN + ['Nhập "KTCN", bấm Tìm kiếm.'], 'Tìm: KTCN', ['Còn 1 dòng KTCN - Kỹ thuật công nghệ.'], 26)
S2.add('Tìm một phần mã hoặc tên', 'P0', ACC_A, OPEN + ['Nhập "phan", nhấn Enter.'], 'Tìm: phan',
       ['Còn 2 dòng: EG1 - PTT (tên "Kho etek group 1 - Phan Trọng Tuệ") và PTT (tên "Phan Trọng Tuệ"); "Hiển thị 1–2 / 2".'], [27, 41])
S2.add('Không phân biệt hoa thường', 'P0', ACC_A, OPEN + ['Nhập "PHAN", nhấn Enter.'], 'Tìm: PHAN', ['Kết quả 2 dòng như khi nhập "phan".'], 28)
S2.add('Có dấu / không dấu', 'P2', ACC_A, OPEN + ['Nhập "Trọng Tuệ", nhấn Enter.', 'Nhập "Trong Tue", nhấn Enter.'], 'Tìm: Trọng Tuệ ; Trong Tue',
       ['"Trọng Tuệ" ra 2 kho có tên chứa chuỗi.', '"Trong Tue": kết quả theo cách so chữ của hệ thống — chỉ cần không lỗi, không treo.'], 29)
S2.add('Ký tự đặc biệt', 'P1', ACC_A, OPEN + ['Lần lượt nhập "%", "_", "\'", nhấn Enter.'], 'Tìm: % ; _ ; \'',
       ['"%" và "_" được tìm đúng nghĩa đen; "_" ra kho EG_LN, "%" ra "' + EMPTY + '".', 'Không báo lỗi hệ thống.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', ACC_A, OPEN + ['Nhập "  KTCN  ", nhấn Enter.'], 'Tìm: "  KTCN  "', ['Bỏ khoảng trắng 2 đầu, ra 1 dòng KTCN.'], 32)
S2.add('Chuỗi dài', 'P2', ACC_A, OPEN + ['Dán chuỗi 300 ký tự, nhấn Enter.'], 'Chuỗi 300 ký tự',
       ['Ô nhận đủ; bảng "%s"; không lỗi.' % EMPTY], 33)
S2.add('Xóa từ khóa bằng dấu ×', 'P1', ACC_A, OPEN + ['Tìm "phan".', 'Bấm × trong ô tìm.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bấm ×: ô trống, bảng chưa đổi (vẫn 2 dòng).', 'Sau Tìm kiếm: lại 22 kho.'], 34)
S2.add('Gõ chưa bấm Tìm kiếm thì chưa lọc', 'P1', ACC_A, OPEN + ['Nhập "phan", không bấm gì.', 'Nhấn Enter.'], 'Tìm: phan',
       ['Trước Enter: vẫn "Hiển thị 1–10 / 22".', 'Sau Enter (hoặc bấm Tìm kiếm): 2 dòng.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', ACC_A, ['Rời sang màn khác.'] + OPEN, '—',
       ['Ô tìm trống, ô Nhóm "Nhóm", ô Công ty "Công ty" (chưa chọn), chưa sắp xếp, 22 kho.'], 36)
S2.add('Lọc theo Nhóm', 'P0', ACC_A, OPEN + ['Chọn Nhóm = Kho Hà Nội.'], 'Nhóm: Kho Hà Nội',
       ['Danh sách nạp lại ngay (không cần bấm Tìm kiếm): 4 kho SL, CSKH, LN, PTT; "Hiển thị 1–4 / 4".'], [37, 41])
S2.add('Lọc theo Công ty', 'P0', ACC_A, OPEN + ['Mở ô Công ty, chọn "CÔNG TY TNHH THIẾT BỊ TÂN PHÁT SÀI GÒN".'], 'Công ty: Tân Phát Sài Gòn',
       ['Ô liệt kê 9 công ty.', 'Còn 4 kho SGSX, SG-KHOAO, SG-CSKH, SG.'], [37, 299])
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', ACC_A, OPEN + ['Chọn Công ty = Tân Phát Sài Gòn.', 'Chọn Nhóm = Kho Sài Gòn.', 'Tìm "CSKH".'],
       'Công ty: Tân Phát Sài Gòn; Nhóm: Kho Sài Gòn; Tìm: CSKH', ['Còn 1 kho SG-CSKH (thỏa đồng thời 3 điều kiện).'], [38, 39])
S2.add('Lọc không có kết quả', 'P1', ACC_A, OPEN + ['Chọn Nhóm = Kho Sài Gòn.', 'Chọn Công ty = CN HẢI PHÒNG.'], '—',
       ['Bảng "%s", "Không có kho nào."' % EMPTY], 40)
S2.add('Phân trang sau lọc', 'P1', ACC_A, OPEN + ['Chọn Số dòng/trang = 5.', 'Chọn Công ty = CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT.'], '—',
       ['8 kho chia 2 trang (5 + 3), "Hiển thị 1–5 / 8".'], 42)
S2.add('Sắp xếp sau lọc', 'P2', ACC_A, OPEN + ['Chọn Nhóm = Kho Hà Nội.', 'Bấm "Mã".'], '—', ['4 kho theo Mã tăng: CSKH, LN, PTT, SL.'], 43)
S2.add('Làm mới', 'P0', ACC_A, OPEN + ['Tìm "phan", chọn Nhóm = Kho Hà Nội, bấm "Mã".', 'Bấm Làm mới.'], '—',
       ['Ô tìm trống, ô Nhóm / Công ty bỏ chọn, bỏ sắp xếp, trang 1, "Hiển thị 1–10 / 22".'], 44)
S2.add('Chuyển màn rồi quay lại', 'P0', ACC_A, OPEN + ['Tìm "phan".', 'Vào màn khác từ menu.', 'Quay lại Theo dõi theo kho từ menu.'], '—',
       ['Ô tìm trống, 22 kho (bộ lọc bị xóa khi rời màn).'], 45)
S2.add('Tải lại trang giữ bộ lọc', 'P1', ACC_A, OPEN + ['Tìm "phan", chọn Nhóm = Kho Hà Nội.', 'Nhấn F5 (trong 10 phút).'], '—',
       ['Ô tìm vẫn "phan", ô Nhóm vẫn Kho Hà Nội, 1 kho PTT; sắp xếp và trang về mặc định.'], 46)
S2.add('Mở ở tab mới', 'P2', ACC_A, OPEN + ['Tìm "phan".', 'Mở Theo dõi theo kho ở tab mới trong 10 phút.'], '—',
       ['Tab mới hiện sẵn "phan" (ghi tạm trên trình duyệt, chung các tab), 2 dòng.'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', [ACC_A, ACC_C], OPEN + ['A tìm "phan", đăng xuất.', 'C đăng nhập, mở màn trong 10 phút.'], '—',
       ['C thấy ô tìm "phan" (ghi tạm theo trình duyệt); dữ liệu vẫn theo phạm vi của C: chỉ 1 kho PTT (EG1 - PTT thuộc công ty khác).'], 48)
S2.add('Máy chủ lỗi khi tìm', 'P2', [ACC_A, 'Máy chủ tạm lỗi.'], OPEN + ['Bấm Tìm kiếm.'], '—', ['Thông báo "%s".' % LOADERR], 40)

# ============================================================== III. SỐ LIỆU BÁO CÁO
S3 = Sec(3)
S3.add('Tổng số kho khớp danh mục Kho vật lý', 'P0', ACC_A, OPEN + [VIEW_KVL + ' Chọn trạng thái Hoạt động, rồi Khóa, đếm tổng.'], '—',
       ['Theo dõi theo kho 22 kho = Kho vật lý 21 Hoạt động + 1 Khóa, trùng đúng từng mã.'], [6, 16, 274])
S3.add('Số kho theo công ty khớp danh mục', 'P0', ACC_C, ['Đăng nhập C.'] + OPEN + [VIEW_KVL], '—',
       ['C thấy 8 kho ở cả 2 màn (DATD, N10, N9, KTCN, SL, CSKH, LN, PTT).'], [16, 274, 299])
S3.add('Ô tổng hợp bằng số dòng bảng', 'P0', ACC_A, OPEN2 + ['Đếm dòng theo cột Trạng thái.'], '—',
       ['Tổng số phiếu nhận 55 = số dòng.', 'Tổng hoàn thành 0 = số dòng "Đã hoàn thành".',
        'Tổng chưa xử lý 55 = 55 - 0 = 34 Đã nhận đề nghị + 12 Đang lấy hàng + 9 Đang xếp hàng.'], [16, 37])
S3.add('Đối soát dòng đề nghị xuất với màn Phiếu đề nghị xuất kho', 'P0', ACC_A,
       OPEN2 + ['Tìm "PDNXK" ở trang hoạt động, ghi danh sách mã.', VIEW_DNXK, 'Lọc Kho = PTT, Trạng thái = Chờ duyệt; rồi Đang xuất kho.'],
       '—', ['Trang hoạt động 40 dòng = tổng 2 lần lọc ở màn Phiếu đề nghị xuất kho, khớp ĐÚNG từng mã.'], [6, 274])
S3.add('Đối soát dòng đề nghị nhập với màn Phiếu đề nghị nhập kho', 'P0', ACC_A,
       OPEN2 + ['Tìm "PDNNK", ghi danh sách mã.', VIEW_DNNK, 'Lọc Kho = PTT, Trạng thái = Chờ duyệt; rồi Đang nhập kho.'], '—',
       ['15 dòng = tổng 2 lần lọc, khớp đúng từng mã.'], [6, 274])
S3.add('Đối soát kho khác', 'P1', ACC_A, OPEN + ['Mở trang hoạt động của kho MT, rồi KTCN.'], '—',
       ['MT: 5 phiếu = 1 đề nghị xuất + 4 đề nghị nhập (1 Đã nhận đề nghị, 4 Đang xếp hàng).',
        'KTCN: 2 phiếu = 2 đề nghị xuất + 0 đề nghị nhập.'], [6, 274])
S3.add('Đối soát với màn Hoạt động kho', 'P1', [ACC_A, 'Tài khoản K là thủ kho DUY NHẤT của kho PTT.'],
       OPEN2 + ['K mở phân hệ Kho > "Hoạt động kho".'], '—',
       ['Hai bảng trùng từng dòng, cùng thứ tự, cùng 3 ô (55 / 0 / 55).'], [6, 274])
S3.add('Phiếu Đang tạo / Đã hủy không hiện', 'P0', [ACC_A, 'Kho PTT có 1 phiếu đề nghị xuất Đang tạo và 1 phiếu Đã hủy hôm nay.'],
       OPEN2 + ['Tìm mã 2 phiếu đó.'], '—', ['Cả 2 không có trên bảng; không tính vào ô tổng hợp.'], [6, 281])
S3.add('Trạng thái Đã nhận đề nghị', 'P0', [ACC_A, TEST_ENV], ['Gửi thủ kho 1 %s của kho PTT.' % DNXK] + OPEN2, '—',
       ['Dòng mới: Thời gian nhận = lúc gửi, Thời gian lấy/xếp hàng trống, nhãn cam "Đã nhận đề nghị".'], [7, 281])
S3.add('Chuyển sang Đang lấy hàng khi lập phiếu xuất kho', 'P0', [ACC_A, TEST_ENV, 'Phiếu đề nghị xuất X của kho PTT đang "Đã nhận đề nghị".'],
       ['Lập Phiếu xuất kho cho X (Tài chính > Xuất hàng > Phiếu xuất kho).'] + OPEN2, '—',
       ['Dòng X: Thời gian lấy/xếp hàng = lúc lập, nhãn xanh dương "Đang lấy hàng"; Tổng chưa xử lý không đổi.'], [7, 281])
S3.add('Đề nghị nhập kho hiện "Đang xếp hàng"', 'P1', [ACC_A, TEST_ENV, 'Phiếu đề nghị nhập Y của kho PTT đang "Đã nhận đề nghị".'],
       ['Lập Phiếu nhập kho cho Y.'] + OPEN2, '—', ['Dòng Y nhãn "Đang xếp hàng", Hình thức vận chuyển trống.'], [7, 281])
S3.add('Hoàn thành trong ngày', 'P0', [ACC_A, TEST_ENV, 'Phiếu đề nghị xuất X nhận hôm nay 08:00, đang lấy hàng.'],
       ['Gửi Phiếu xuất kho của X lúc 10:15.'] + OPEN2, '—',
       ['Dòng X: Thời gian hoàn thành 10:15, nhãn xanh lá "Đã hoàn thành", Tổng thời gian xử lý "2 giờ 15 phút", xuống CUỐI bảng.',
        'Tổng hoàn thành tăng 1, Tổng chưa xử lý giảm 1, Tổng số phiếu nhận không đổi.'], [7, 281])
S3.add('Phiếu hoàn thành rời bảng sang ngày hôm sau', 'P1', [ACC_A, TEST_ENV, 'Kho PTT có dòng "Đã hoàn thành" nhận hôm nay.'],
       OPEN2 + ['Để trang mở qua 00:00, chờ lượt tự tải lại.'], '—',
       ['Dòng đã hoàn thành của hôm trước biến mất; phiếu chưa hoàn thành nhận hôm trước vẫn còn.'], 281)
S3.add('Tổng thời gian xử lý dưới 1 phút', 'P2', [ACC_A, TEST_ENV, 'Phiếu kho PTT nhận 09:00:10, hoàn thành 09:00:40 hôm nay.'], OPEN2, '—',
       ['Cột Tổng thời gian xử lý ghi "Vài giây".'], 7)
S3.add('Tổng thời gian xử lý trên 1 ngày', 'P2', [ACC_A, TEST_ENV, 'Phiếu kho PTT nhận hôm nay 00:05, hoàn thành 26 giờ 3 phút sau.'],
       OPEN2, '—', ['Ghi "1 ngày 2 giờ 3 phút" (bỏ phần bằng 0).'], 7)
S3.add('Người yêu cầu và Hình thức vận chuyển', 'P1', ACC_A, OPEN2 + ['Mở Yêu cầu xuất hàng gốc của PDNXK-39034.'], '—',
       ['Người yêu cầu "Tạ Xuân Quyết" = người lập Yêu cầu xuất hàng; Hình thức vận chuyển "Khách hàng vận chuyển".',
        'Dòng đề nghị nhập kho luôn trống Hình thức vận chuyển.'], 6)
S3.add('Ô tổng hợp theo kết quả tìm', 'P0', ACC_A, OPEN2 + ['Tìm "PDNNK".'], 'Tìm: PDNNK',
       ['Bảng 15 dòng; 3 ô 15 / 0 / 15.'], [41, 39])
S3.add('Chữ i khối và từng ô tổng hợp', 'P2', ACC_A, OPEN2 + ['Rê chuột vào chữ i cạnh "PHIẾU NHẬN" và 3 ô.'], '—',
       ['Khối: "%s".' % TIP_KHOI,
        'Tổng số phiếu nhận: "Số phiếu đề nghị xuất kho + đề nghị nhập kho đang hiện ở danh sách bên dưới".',
        'Tổng hoàn thành: "Số phiếu đã hoàn thành (đã có Thời gian hoàn thành)".',
        'Tổng chưa xử lý: "Tổng số phiếu nhận trừ Tổng hoàn thành" và "Gồm phiếu "Đã nhận đề nghị" và phiếu đang lấy hàng / xếp hàng".'], 3)
S3.add('Kho không có phiếu', 'P1', ACC_A, OPEN + ['Bấm mã kho EG_LN.'], '—',
       ['Trang "Hoạt động nhập/xuất kho EG_LN - Kho ETEK GREEN Liên Ninh": bảng "%s", 3 ô 0 / 0 / 0.' % EMPTY], 8)

# ============================================================== IV. XEM CHI TIẾT
S4 = Sec(4)
S4.add('Mở trang hoạt động của kho', 'P0', ACC_A, OPEN + ['Bấm tên kho "Phan Trọng Tuệ".'], '—',
       ['Tab mới: tiêu đề "%s" ở thanh tiêu đề, tiêu đề bảng, tab trình duyệt.' % T2,
        'Khối lọc chỉ có ô "Tìm theo mã phiếu đề nghị", Tìm kiếm, Làm mới; khối PHIẾU NHẬN 55 / 0 / 55; nút Xuất Excel, Cấu hình cột; '
        'chân trang nút Quay lại.'], [186, 187, 188])
S4.add('Các cột của bảng hoạt động', 'P0', ACC_A, OPEN2, '—',
       ['Đủ 11 cột: %s.' % COLS2, 'Sắp xếp được 5 cột: Phiếu đề nghị, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành.',
        'Không phân trang: 55 dòng trên 1 trang, không có ô Số dòng/trang.'], [188, 190])
S4.add('Dòng khớp phiếu gốc', 'P0', ACC_A, OPEN2 + ['Đọc dòng PDNXK-39053, mở phiếu để so.'], '—',
       ['Dòng: Xuất mượn, DNS Admin, Công ty vận chuyển, PTT - Phan Trọng Tuệ, 29/10/2026 15:53, 29/10/2026 15:56, trống, Đang lấy hàng.',
        'Kho, mã, các mốc thời gian khớp phiếu gốc.'], [189, 190])
S4.add('Trang hoạt động chỉ đọc', 'P1', ACC_A, OPEN2, '—',
       ['Không có ô nhập, nút Lưu, Sửa, Xóa; số ở 3 ô không bấm được.'], [191, 192])
S4.add('Thứ tự mặc định trang hoạt động', 'P0', ACC_A, OPEN2, '—',
       ['Phiếu chưa hoàn thành trên, Thời gian nhận mới nhất trước: PDNXK-39058 (10/11 11:12), PDNXK-39053 (29/10 15:53), PDNXK-39035…'], 19)
S4.add('Sắp xếp trang hoạt động', 'P1', ACC_A, OPEN2 + ['Bấm "Phiếu đề nghị".'], '—',
       ['Mã A đến Z: PDNNK-07592, PDNNK-09815, PDNNK-10376…'], [20, 43])
S4.add('Tìm mã phiếu', 'P0', ACC_A, OPEN2 + ['Nhập "39053", bấm Tìm kiếm.'], 'Tìm: 39053',
       ['Còn 1 dòng PDNXK-39053; khối PHIẾU NHẬN 1 / 0 / 1.'], [26, 27])
S4.add('Tìm mã phiếu không có', 'P1', ACC_A, OPEN2 + ['Nhập "ZZZ999", nhấn Enter.'], 'Tìm: ZZZ999', ['Bảng "%s"; 3 ô 0 / 0 / 0.' % EMPTY], 30)
S4.add('Từ khóa trang hoạt động không ghi nhớ', 'P1', ACC_A, OPEN2 + ['Tìm "PDNNK".', 'Nhấn F5.'], '—',
       ['Sau F5 ô tìm trống, bảng đủ 55 dòng (không lọc ngầm khi sang kho khác).'], 46)
S4.add('Thu gọn / mở rộng khối tổng hợp', 'P2', ACC_A, OPEN2 + ['Bấm Thu gọn.', 'Bấm Mở rộng.'], '—',
       ['Thu gọn: ẩn 3 ô, nút đổi "Mở rộng".', 'Mở rộng: hiện lại, số không đổi.'], 3)
S4.add('Tự tải lại sau 60 giây', 'P0', [ACC_A, TEST_ENV], OPEN2 + ['Ở tab khác gửi thủ kho 1 phiếu đề nghị xuất mới của kho PTT.',
                                                                  'Quay lại, chờ tối đa 60 giây.'], '—',
       ['Phiếu mới tự xuất hiện đầu bảng, Tổng số phiếu nhận tăng 1; không vòng tải, không báo lỗi.'], [40, 281])
S4.add('Quay lại giữ bộ lọc danh sách', 'P0', ACC_A, OPEN + ['Tìm "phan".', 'Bấm mã PTT, ở tab mới bấm Quay lại.'], '—',
       ['Tab đó về trang danh sách kho, ô tìm vẫn "phan", 2 kho.'], [196, 197])
S4.add('Mở phiếu đề nghị xuất kho từ mã', 'P0', ACC_A, OPEN2 + ['Bấm mã PDNXK-39058.'], '—',
       ['Mở TAB MỚI màn chi tiết Phiếu đề nghị xuất kho PDNXK-39058; trang hoạt động giữ nguyên.'], [186, 187])
S4.add('Mở phiếu đề nghị nhập kho từ mã', 'P0', ACC_A, OPEN2 + ['Bấm mã PDNNK-11037.'], '—',
       ['Tab mới "Chi tiết đề nghị nhập kho: PDNNK-11037".'], [186, 187])
S4.add('Nút trên màn phiếu theo quyền của màn phiếu', 'P1', ACC_A, OPEN2 + ['Bấm 1 mã phiếu, quan sát màn chi tiết.'], '—',
       ['Nút thao tác (Sửa, Duyệt, Lập phiếu…) hiện theo quyền và trạng thái của màn phiếu; Theo dõi theo kho không thêm nút nào.'], 193)
S4.add('Xử lý phiếu rồi quay lại', 'P1', [ACC_A, TEST_ENV], OPEN2 + ['Bấm mã 1 phiếu "Đã nhận đề nghị", lập Phiếu xuất kho ở tab mới.',
                                                                    'Quay lại tab hoạt động, chờ tối đa 60 giây.'], '—',
       ['Dòng đó đổi sang "Đang lấy hàng" ở lượt tự tải lại.'], [196, 281])
S4.add('Mở kho không tồn tại', 'P1', ACC_A, ['Dán địa chỉ trang hoạt động với mã kho 999999.'], '—',
       ['Chuyển sang %s; không hiện thông báo lỗi.' % P404], 296)

# ============================================================== V. TÙY CHỈNH CỘT
S5 = Sec(5)
S5.add('Mở cửa sổ Tuỳ chỉnh cột', 'P0', ACC_A, OPEN + ['Bấm biểu tượng Cấu hình cột hiển thị.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột", hướng dẫn "Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.", 5 cột, "Đang chọn 5/5 cột", '
        'nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng.'], [198, 199, 200])
S5.add('Ẩn cột', 'P0', ACC_A, OPEN + ['Mở Tuỳ chỉnh cột, bỏ tích Nhóm.', 'Bấm Lưu.'], '—', ['Báo "Cập nhật thành công"; bảng còn 4 cột.'], [202, 206])
S5.add('Hiện lại cột đã ẩn', 'P1', [ACC_A, 'Đã ẩn cột Nhóm.'], OPEN + ['Mở Tuỳ chỉnh cột, tích Nhóm, Lưu.'], '—', ['Cột Nhóm hiện lại.'], 201)
S5.add('Cột khóa không ẩn được', 'P0', ACC_A, OPEN + ['Mở Tuỳ chỉnh cột.', 'Bấm Bỏ chọn hết.'], '—',
       ['STT, Mã có ổ khóa, luôn tích, không kéo được; "Đang chọn 2/5 cột".'], [203, 205])
S5.add('Kéo thả thứ tự cột', 'P1', ACC_A, OPEN + ['Kéo Công ty lên ngay sau Mã.', 'Lưu.'], '—', ['Bảng hiện Công ty là cột thứ 3.'], 204)
S5.add('Đóng không lưu', 'P1', ACC_A, OPEN + ['Bỏ tích Tên.', 'Bấm Đóng (hoặc ×, hoặc bấm ra ngoài).'], '—',
       ['Cửa sổ đóng không hỏi; cột Tên vẫn hiện.'], 207)
S5.add('Ghi nhớ sau F5 và đăng nhập lại', 'P1', [ACC_A, 'Đã ẩn cột Nhóm.'], OPEN + ['Nhấn F5.', 'Đăng xuất, đăng nhập lại.'], '—',
       ['Cột Nhóm vẫn ẩn ở cả 2 lần.'], 208)
S5.add('Cấu hình theo từng tài khoản', 'P1', [ACC_A, ACC_C, 'A đã ẩn cột Nhóm.'], ['C đăng nhập.'] + OPEN, '—', ['C vẫn thấy đủ 5 cột.'], 209)
S5.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', ACC_A, OPEN + ['Tìm "phan".', 'Ẩn cột Công ty, Lưu.'], '—',
       ['Vẫn 2 kho, từ khóa giữ, trang và sắp xếp giữ.'], [210, 211])
S5.add('Tuỳ chỉnh cột trang hoạt động', 'P0', ACC_A, OPEN2 + ['Bấm Cấu hình cột hiển thị.'], '—',
       ['Cửa sổ liệt kê 11 cột, "Đang chọn 11/11 cột"; STT, Phiếu đề nghị có ổ khóa.'], [198, 199, 203])
S5.add('Cấu hình trang hoạt động dùng chung mọi kho', 'P1', ACC_A, OPEN2 + ['Ẩn cột Loại, Lưu.', 'Mở trang hoạt động của kho MT.'], '—',
       ['Kho MT cũng ẩn cột Loại; trang danh sách kho và màn Hoạt động kho không bị ảnh hưởng.'], [206, 209])

# ============================================================== VI. XUẤT DANH SÁCH EXCEL
S6 = Sec(6)
S6.add('Mở cửa sổ chọn trường', 'P0', ACC_A, OPEN + ['Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất Excel", hướng dẫn "Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.", 4 trường Mã, Tên, '
        'Nhóm, Công ty; "Đang chọn 4/4 trường"; nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng.'], [212, 213])
S6.add('Trường tích sẵn theo cột đang hiện', 'P1', [ACC_A, 'Đã ẩn cột Nhóm ở Tuỳ chỉnh cột.'], OPEN + ['Bấm Xuất Excel.'], '—',
       ['Tích sẵn 3 trường Mã, Tên, Công ty; Nhóm không tích ("Đang chọn 3/4 trường").'], 214)
S6.add('Xuất với trường mặc định', 'P0', ACC_A, OPEN + ['Bấm Xuất Excel > Xuất file.'], '—',
       ['Tải file "%s", báo "Xuất Excel thành công.", cửa sổ đóng.' % FILE1,
        'File trang "Theo dõi theo kho": ảnh letterhead công ty người xuất, tiêu đề "DANH SÁCH THEO DÕI THEO KHO", 5 cột (STT, Mã, Tên, '
        'Nhóm, Công ty) có nút lọc, 22 dòng (đủ mọi trang), khối ký "Người lập".'], [215, 221, 223, 224, 227])
S6.add('Chọn tất cả / Bỏ chọn hết', 'P1', ACC_A, OPEN + ['Bấm Xuất Excel.', 'Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
       ['Bỏ chọn hết: "Đang chọn 0/4 trường", nút Xuất file mờ.', 'Chọn tất cả: 4/4.'], [216, 218])
S6.add('Xuất một số trường và đổi thứ tự', 'P0', ACC_A, OPEN + ['Bấm Xuất Excel, chỉ tích Mã, Công ty.', 'Kéo Công ty lên đầu.', 'Xuất file.'], '—',
       ['File có 3 cột theo đúng thứ tự: STT, Công ty, Mã.'], [217, 225, 226])
S6.add('Xuất theo tìm kiếm', 'P0', ACC_A, OPEN + ['Tìm "phan".', 'Xuất file.'], 'Tìm: phan', ['File đúng 2 dòng EG1 - PTT, PTT.'], 219)
S6.add('Xuất theo bộ lọc và sắp xếp', 'P1', ACC_A, OPEN + ['Chọn Nhóm = Kho Hà Nội, bấm "Mã".', 'Xuất file.'], '—',
       ['File 4 dòng theo thứ tự CSKH, LN, PTT, SL như bảng.'], [220, 228])
S6.add('Xuất khi danh sách rỗng', 'P1', ACC_A, OPEN + ['Tìm "ZZZ999".', 'Bấm Xuất Excel > Xuất file.'], 'Tìm: ZZZ999',
       ['KHÔNG tải file; báo "Không có dữ liệu để xuất".'], 222)
S6.add('Định dạng dữ liệu trong file', 'P1', ACC_A, OPEN + ['Xuất file, mở bằng Excel.'], '—',
       ['Tên kho, tên công ty tiếng Việt đúng dấu, ký tự "Đ" trong mã KĐN-ALM đúng; ô trống để trống.'], [229, 230])
S6.add('Đóng cửa sổ không xuất', 'P2', ACC_A, OPEN + ['Bấm Xuất Excel > Đóng (hoặc ×).'], '—', ['Cửa sổ đóng, không tải file.'], 128)
S6.add('Xuất Excel trang hoạt động', 'P0', ACC_A, OPEN2 + ['Bấm Xuất Excel.', 'Xuất file.'], '—',
       ['Cửa sổ 10 trường %s, tích sẵn cả 10.' % FIELDS2,
        'Tải "%s", báo "Xuất Excel thành công."; file trang "Hoạt động kho", tiêu đề "HOẠT ĐỘNG NHẬP/XUẤT KHO PTT - PHAN TRỌNG TUỆ", '
        '11 cột, 55 dòng, khối ký "Người lập".' % FILE2], [212, 213, 215, 223, 227])
S6.add('Xuất trang hoạt động theo từ khóa', 'P1', ACC_A, OPEN2 + ['Tìm "PDNNK".', 'Xuất file.'], 'Tìm: PDNNK',
       ['File 15 dòng đề nghị nhập kho, cùng thứ tự bảng.'], [219, 228])
S6.add('Trang hoạt động rỗng vẫn tạo file', 'P1', ACC_A, OPEN2 + ['Tìm "ZZZ999".', 'Xuất file.'], 'Tìm: ZZZ999',
       ['Vẫn tải file có tiêu đề, hàng tên cột, khối ký, không có dòng dữ liệu; báo "Xuất Excel thành công.".'], 222)
S6.add('Trường trang hoạt động không theo cột ẩn', 'P2', [ACC_A, 'Đã ẩn cột Loại ở trang hoạt động.'], OPEN2 + ['Bấm Xuất Excel.'], '—',
       ['Vẫn tích đủ 10 trường, kể cả Loại.'], 214)
S6.add('Định dạng file trang hoạt động', 'P2', ACC_A, OPEN2 + ['Xuất file, mở bằng Excel.'], '—',
       ['Ngày giờ dd/mm/yyyy hh:mm; Trạng thái ghi chữ; ô dài tự xuống dòng, không bị cắt chữ.'], 229)

# ============================================================== VII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S7 = Sec(7)
S7.add('Kho mới tạo xuất hiện', 'P0', [ACC_A, TEST_ENV], ['Thêm kho "TEST01" ở danh mục Kho vật lý.'] + OPEN, '—',
       ['TEST01 ở đầu danh sách (tạo mới nhất), tổng 23.'], [274, 282])
S7.add('Đổi tên kho đồng bộ', 'P1', [ACC_A, TEST_ENV], ['Sửa tên kho TEST01 thành "Kho thử 2" ở Kho vật lý.'] + OPEN, '—',
       ['Cột Tên hiện "Kho thử 2"; trang hoạt động của kho đổi tiêu đề theo tên mới.'], [272, 278, 279])
S7.add('Khóa kho vẫn hiện', 'P1', [ACC_A, TEST_ENV], ['Khóa kho TEST01 ở Kho vật lý.'] + OPEN, '—',
       ['TEST01 vẫn trong danh sách, mở trang hoạt động được.'], [273, 284])
S7.add('Xóa kho thì rời danh sách', 'P0', [ACC_A, TEST_ENV], ['Xóa kho TEST01 ở Kho vật lý.'] + OPEN + ['Dán địa chỉ trang hoạt động cũ của TEST01.'],
       '—', ['TEST01 không còn trong danh sách; trang hoạt động cũ chuyển sang trang không tìm thấy.'], [280, 285])
S7.add('Đổi nhóm / công ty của kho', 'P1', [ACC_A, TEST_ENV], ['Đổi Nhóm của kho SL từ Kho Hà Nội sang trống ở Kho vật lý.'] + OPEN +
       ['Chọn Nhóm = Kho Hà Nội.'], '—', ['Còn 3 kho; ô Nhóm của SL trống.'], [278, 282])
S7.add('Hủy phiếu thì rời bảng hoạt động', 'P0', [ACC_A, TEST_ENV, 'Phiếu đề nghị xuất X của kho PTT đang "Đã nhận đề nghị".'],
       ['Hủy X ở màn Phiếu đề nghị xuất kho.'] + OPEN2, '—', ['X không còn trên bảng; Tổng số phiếu nhận giảm 1.'], [280, 281])
S7.add('Đổi kho của phiếu', 'P1', [ACC_A, TEST_ENV, 'Phiếu nháp kho MT được sửa sang kho PTT rồi gửi thủ kho.'], OPEN + ['Mở trang hoạt động của PTT, rồi MT.'],
       '—', ['Phiếu có ở trang hoạt động PTT, không còn ở MT.'], [278, 282])
S7.add('Không có dòng trùng / mồ côi', 'P1', ACC_A, OPEN2, '—',
       ['55 dòng, không mã nào lặp; mọi dòng cột Kho = PTT - Phan Trọng Tuệ.'], [283, 285, 286])

# ============================================================== VIII. PHÂN QUYỀN
S8 = Sec(8)
S8.add('Có Quản lý kho xem được danh sách', 'P0', ACC_C, ['Đăng nhập C.'] + OPEN, '—',
       ['Thấy mục "Theo dõi theo kho" ở menu; trang mở, 8 kho của công ty Tân Phát.'], [287, 299])
S8.add('Không thấy ô Công ty khi không xem mọi công ty', 'P0', ACC_C, ['Đăng nhập C.'] + OPEN, '—',
       ['Khối lọc chỉ có ô tìm nhanh, ô Nhóm; không có ô Công ty.'], [295, 299])
S8.add('Xem mọi công ty', 'P0', ACC_A, ['Đăng nhập A.'] + OPEN, '—', ['22 kho của 6 công ty; có ô Công ty (9 công ty).'], 299)
S8.add('Không có Quản lý kho: ẩn menu', 'P0', ACC_N, ['Đăng nhập N.', 'Mở phân hệ Kho.'], '—',
       ['Không có mục "Theo dõi theo kho" trong menu.'], [287, 295])
S8.add('Không có quyền mở thẳng địa chỉ trang danh sách', 'P0', ACC_N, ['Đăng nhập N.', 'Dán địa chỉ màn Theo dõi theo kho.'], '—',
       ['Chuyển sang %s; không lộ danh sách kho.' % P404], 296)
S8.add('Không có quyền mở thẳng trang hoạt động', 'P0', ACC_N, ['Đăng nhập N.', 'Dán địa chỉ trang hoạt động của kho PTT.'], '—',
       ['Chuyển sang %s; không lộ phiếu của kho.' % P404], [288, 296])
S8.add('Mở trang hoạt động kho công ty khác', 'P0', ACC_C, ['Đăng nhập C.', 'Dán địa chỉ trang hoạt động của kho SG (công ty Tân Phát Sài Gòn).'],
       '—', ['Chuyển sang %s.' % P404], [288, 296, 299])
S8.add('Xuất Excel theo phạm vi', 'P0', ACC_C, ['Đăng nhập C.'] + OPEN + ['Xuất file.'], '—',
       ['File 8 dòng, chỉ kho công ty Tân Phát.'], [293, 299])
S8.add('Mở phiếu khi thiếu quyền xem phiếu', 'P1', [ACC_C, 'C không có quyền xem ở màn Phiếu đề nghị xuất kho.'], OPEN2 + ['Bấm mã PDNXK-39053.'],
       '—', ['Tab mới xử lý theo quyền của màn Phiếu đề nghị xuất kho; trang hoạt động vẫn hiện dòng.'], 288)
S8.add('Không có nút ghi dữ liệu để ẩn', 'P2', ACC_C, ['Đăng nhập C.'] + OPEN, '—',
       ['Chỉ có Tìm kiếm, Làm mới, Xuất Excel, Cấu hình cột (và Quay lại ở trang hoạt động); không có Thêm / Sửa / Xóa / Khóa / Import.'],
       [289, 290, 291, 292, 294])
S8.add('Gỡ quyền giữa thao tác', 'P0', [ACC_C, TEST_ENV], OPEN + ['Ở tab khác gỡ quyền "Quản lý kho" của C.', 'Bấm Tìm kiếm.'], '—',
       ['Thông báo "%s"; không nạp dữ liệu mới.' % NOPERM, 'Trang hoạt động đang mở chuyển sang trang không tìm thấy ở lượt tải kế tiếp.'], 298)
S8.add('Người có quyền nhưng chưa gắn công ty', 'P1', ['Tài khoản có "Quản lý kho", không có quyền xem mọi công ty, chưa gắn công ty.'],
       OPEN, '—', ['Danh sách rỗng, không hiện kho chưa gắn công ty.'], 299)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'SỐ LIỆU BÁO CÁO', S3),
    ('IV', 'XEM CHI TIẾT HOẠT ĐỘNG KHO VÀ PHIẾU ĐỀ NGHỊ', S4),
    ('V', 'TÙY CHỈNH CỘT', S5),
    ('VI', 'XUẤT DANH SÁCH EXCEL', S6),
    ('VII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S7),
    ('VIII', 'PHÂN QUYỀN', S8),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Theo dõi theo kho - Cập nhật ngày 10/11/2026',
                module_name='Theo dõi theo kho', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='bao_cao')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))
