# -*- coding: utf-8 -*-
"""Testcase màn "Hệ số công nghệ theo nhóm hàng hóa" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan,
loai='danh_muc').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'danh_muc' — lý do từ code: màn danh sách + popup Thêm / Sửa / Xem (BenefitRateModal), không có số chứng từ, không có vòng đời
trạng thái / duyệt; bản ghi là cấu hình dùng chung (hệ số theo nhóm hàng hóa) đọc ngược ở Duyệt kết quả lắp đặt.
Nhóm theo đúng tên + thứ tự chuẩn loại 'danh_muc' (check_tc.THU_TU), bỏ nhóm màn không có (kiểm code 06/11/2026: không có route / nút
Khóa - Mở khóa, Import):
I Hiển thị · II Tìm kiếm & lọc (gồm "Cài đặt bộ lọc:") · III Thêm mới · IV Chỉnh sửa · V Xóa · VI Lịch sử · VII Xem chi tiết ·
VIII Tùy chỉnh cột · IX Xuất danh sách Excel · X Ràng buộc · XI Phân quyền (màn KHÔNG gắn quyền — viết theo thực tế: ai đăng nhập cũng
dùng được, phạm vi theo công ty).
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../bien-ban-xu-ly-thua-thieu-kiem-ke/gen_testcase.py (06/11, qua check_tc 0 lỗi).
Nguồn hành vi (đọc 06/11/2026, nhánh develop): FE pages/admin/benefit-rates/**; BE Modules/CustomerCare BenefitRate*
(Entity / Service / Request / Resource / Controller), WrApproveResultSourceService::productCoefficient.
Số liệu mẫu: bộ 12 hệ số của công ty Tân Phát dùng khi chụp ảnh (giả trên trình duyệt — dev chưa có dữ liệu), QA dựng lại trên môi
trường test trước khi chạy.
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
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_chuan import build_chuan  # noqa: E402
from tc_phieu_bosung import check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Bán hàng > nhóm "Quy chế - Thiết lập" > "Thiết lập" > bấm "Hệ số công nghệ theo nhóm hàng hóa".'
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'
MISS = '"Bạn chưa nhập đầy đủ thông tin."'
REQ = '"Bắt buộc phải nhập"'
DUP = '"Loại tỷ lệ hưởng đã tồn tại."'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'
EMPTY = '"Không có dữ liệu phù hợp."'
UNSAVED = '"Thông tin chưa lưu" – "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"'

ACC_A = 'Tài khoản A: nhân viên công ty Tân Phát (Hà Nội).'
ACC_B = 'Tài khoản B: nhân viên khác cùng công ty Tân Phát (Bùi Duy Trước).'
ACC_C = 'Tài khoản C: nhân viên công ty Tân Phát Sài Gòn; công ty này có 2 hệ số: "Lắp đặt cầu nâng" (1.80) và "Máy hàn" (1.00).'
ACC_D = 'Tài khoản D: tài khoản chưa gắn công ty.'
DATA = ('Công ty Tân Phát có 12 hệ số (mới nhất trước): Lắp đặt cầu nâng 1.50 (Cầu nâng 1 trụ, Cầu nâng 2 trụ thủy lực có cổng, Cầu '
        'nâng 4 trụ), Lắp đặt phòng sơn 2.00, Máy ra vào lốp 1.20, Máy cân bằng lốp 1.20, Máy nén khí 1.00, Thiết bị hút khí thải '
        '1.30, Thiết bị kiểm tra góc đặt bánh xe 2.50, Máy rửa áp lực 0.80, Máy hàn 1.00, Máy chẩn đoán 0.50, Kích nâng 0.75, Thiết '
        'bị kiểm tra đèn pha 1.10.')
PRE_LIST = ACC_A + '\n' + DATA
H12 = ('Hệ số "Lắp đặt cầu nâng": A tạo 05/11/2026 09:15 với Hệ số 1.20, 2 nhóm; B sửa 06/11/2026 08:40 thành 1.50 và thêm nhóm '
       '"Cầu nâng 4 trụ".')
PHONGSON = ('Hệ số "Lắp đặt phòng sơn" 2.00 gắn 3 nhóm, trong đó nhóm "Phòng sơn sấy xe bus" đã bị khóa ở danh mục nhóm hàng hóa.')
FULL = ['Loại tỷ lệ hưởng: Lắp đặt máy nâng hạ', 'Hệ số: 1.75', 'Nhóm hàng hóa áp dụng: Cầu nâng cắt kéo di động']
FILL = TAO + ['Nhập Loại tỷ lệ hưởng "Lắp đặt máy nâng hạ", Hệ số "1.75", chọn nhóm "Cầu nâng cắt kéo di động".']
EDIT = [MENU, 'Ở dòng "Máy nén khí" bấm Sửa (bút chì).']

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
     'Danh mục khai báo hệ số công nghệ (trên popup gọi là "tỷ lệ hưởng công khoán") theo nhóm hàng hóa: mỗi loại hệ số có tên, '
     'hệ số (tối đa 2 số lẻ) và các nhóm hàng hóa áp dụng. Khi duyệt kết quả lắp đặt ở Phiếu nhập kết quả, dòng hàng chưa có hệ số '
     'lấy hệ số theo nhóm hàng hóa của hàng (không có thì 1); kết quả công khoán = công khoán duyệt x hệ số.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: mọi hệ số thuộc công ty của người đăng nhập.\n- Màn KHÔNG có trạng thái (không có Hoạt động / Khóa).\n'
     '- Ô Nhóm hàng hóa áp dụng: nhóm hàng hóa đang hoạt động; khi sửa / xem thì thêm các nhóm đang gắn dù đã bị khóa (có biểu '
     'tượng ổ khóa).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Hệ số của công ty khác (kể cả với Super admin).\n- Tài khoản chưa gắn công ty: không thấy hệ số nào.\n'
     '- Nhóm hàng hóa đã khóa: không chọn mới được.\n- Hệ số đã xóa: mất hẳn, không xem lại được.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Không áp dụng: màn không có ô lọc ngày (chỉ có ô lọc ngày trong cửa sổ Lịch sử thay đổi, lọc '
                                         'theo thời điểm thao tác).'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Hệ số > các nhóm hàng hóa áp dụng (một - nhiều).\n- Mỗi nhóm hàng hóa thuộc tối đa MỘT hệ số trên toàn hệ thống (mọi công ty).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Loại tỷ lệ hưởng không trùng trong cùng công ty (không phân biệt hoa / thường, dấu).\n'
     '- Một nhóm hàng hóa không được gắn cho 2 hệ số.\n- Chọn trùng nhóm trong cùng popup được gộp còn 1.'),
    ('7. Phân quyền cấp',
     '- Màn KHÔNG gắn quyền riêng (giữ như hệ thống cũ): mọi người dùng đăng nhập đều thấy menu và dùng được mọi nút.\n'
     '- Phạm vi dữ liệu theo CÔNG TY của người đăng nhập.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là thứ tự dòng đầu – cuối của trang, N là tổng hệ số khớp bộ lọc của công ty mình.\n'
     '- Cột Hệ số luôn 2 số lẻ, dấu phẩy ngăn nghìn, dấu chấm thập phân (1,234.50).'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A, B (công ty Tân Phát), C (Tân Phát Sài Gòn), D (chưa gắn công ty).\n'
     '- Cùng một trường: danh sách gọi "Loại hệ số", popup gọi "Loại tỷ lệ hưởng".\n'
     '- Lưu ý: kiểm trùng NHÓM HÀNG HÓA trên toàn hệ thống — nhóm đã gắn ở công ty khác cũng bị chặn.\n'
     '- Lưu ý: bộ lọc KHÔNG được ghi nhớ khi rời màn / tải lại trang.\n'
     '- Lưu ý: Xóa là xóa hẳn, không có điều kiện chặn.\n'
     '- Thêm / Sửa / Xem là cửa sổ nổi trên màn danh sách.'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', PRE_LIST, [MENU], '—',
       ['Mở màn "Hệ số công nghệ theo nhóm hàng hóa", không báo lỗi.', 'Bảng hiện 10 dòng đầu, "Hiển thị 1–10 / 12".',
        'Mặc định 10 dòng/trang; phân trang có 2 trang.'], [1, 10, 16])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng và tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Hệ số công nghệ theo nhóm hàng hóa".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc, thanh công cụ và cột Hành động.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo loại tỷ lệ hưởng"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, nút biểu tượng cột.', 'Mỗi dòng có 3 nút: Sửa, Xóa, Lịch sử (không có nút ba chấm).'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 9 cột theo thứ tự: STT, Loại hệ số, Hệ số, Nhóm hàng hóa, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 9/9 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp hệ số đã tạo', 'P0', [PRE_LIST, H12], [MENU, 'Đối chiếu dòng "Lắp đặt cầu nâng".'], '—',
       ['Hệ số "1.50" căn phải.', 'Nhóm hàng hóa 3 dòng: Cầu nâng 1 trụ / Cầu nâng 2 trụ thủy lực có cổng / Cầu nâng 4 trụ.',
        'Người tạo "<tên A> - <mã phòng A>", Ngày tạo "05/11/2026 09:15".',
        'Người cập nhật "Bùi Duy Trước - <mã phòng>", Ngày cập nhật "06/11/2026 08:40".'], [6, 58])
S1.add('Định dạng cột Hệ số', 'P1', [PRE_LIST, 'Có thêm hệ số "Hệ số thử" = 1234.5.'], [MENU, 'Quan sát cột Hệ số.'], '—',
       ['"Hệ số thử" hiện "1,234.50"; "Kích nâng" hiện "0.75"; "Máy nén khí" hiện "1.00" (luôn 2 số lẻ).'], 6)
S1.add('Màn không có trạng thái bản ghi', 'P2', PRE_LIST, [MENU, 'Quan sát các cột và khối lọc.'], '—',
       ['Không có cột / ô lọc Trạng thái; mọi hệ số đang tồn tại đều có hiệu lực.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', [ACC_D], ['Đăng nhập D.', MENU], '—',
       ['Bảng hiện ' + EMPTY + '; không báo lỗi.', 'Nút Tạo mới vẫn hiện.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện ' + EMPTY + '.'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện cả 12 hệ số, tự về trang 1, "Hiển thị 1–12 / 12".', 'Ô có các lựa chọn 5, 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–12 / 12" (Kích nâng, Thiết bị kiểm tra đèn pha).', 'Bước 3: "Hiển thị 1–10 / 12".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—', ['Bước 2: trang 2.', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 2 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ, không bấm được.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.'], '—', ['Trang 2 đánh số 11–12.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', ADV, 'Chọn Người tạo = Bùi Duy Trước.'],
       'Người tạo: Bùi Duy Trước', ['Tự nạp lại ở trang 1; chỉ còn Máy cân bằng lốp, Máy nén khí; "Hiển thị 1–2 / 2".'], 17)
S1.add('Thứ tự mặc định', 'P0', PRE_LIST, [MENU, 'Quan sát thứ tự khi mới vào.'], '—',
       ['Hệ số tạo gần nhất ở trên ("Lắp đặt cầu nâng" dòng 1, "Thiết bị kiểm tra đèn pha" cuối trang 2).',
        'Không cột nào có mũi tên sắp xếp.'], 19)
S1.add('Sắp xếp tăng dần theo Loại hệ số', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Loại hệ số.'], '—',
       ['Xếp theo tên A sang Z ("Kích nâng" trên cùng), mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Hệ số', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Hệ số 2 lần.'], '—',
       ['Xếp giảm theo giá trị số: 2.50 (Thiết bị kiểm tra góc đặt bánh xe), 2.00, 1.50 …; mũi tên xuống.',
        'Cùng giá trị (1.20 / 1.00) thì hệ số mới hơn ở trên.'], 21)
S1.add('Sắp xếp theo Ngày tạo / Ngày cập nhật', 'P1', [PRE_LIST, H12], [MENU, 'Bấm tiêu đề Ngày tạo.', 'Bấm tiêu đề Ngày cập nhật 2 lần.'],
       '—', ['Ngày tạo tăng: "Thiết bị kiểm tra đèn pha" (25/10/2026) trên cùng.',
             'Ngày cập nhật giảm: "Lắp đặt cầu nâng" (06/11/2026 08:40) trên cùng.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST, [MENU, 'Bấm tiêu đề Nhóm hàng hóa, Người tạo, Người cập nhật, Hành động.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Loại hệ số (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự A sang Z của trang 1.', 'Cột không nhảy bề rộng khi sắp xếp.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 2.', 'Bấm tiêu đề Ngày tạo.'], '—', ['Về trang 1.'], 25)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo loại hệ số chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "Máy nén khí", bấm Tìm kiếm.'], 'Ô tìm nhanh: Máy nén khí',
       ['Chỉ còn 1 dòng "Máy nén khí", "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần tên', 'P0', PRE_LIST, [MENU, 'Nhập "lốp", bấm Tìm kiếm.'], 'Ô tìm nhanh: lốp',
       ['Ra 2 dòng: Máy ra vào lốp, Máy cân bằng lốp.'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "MÁY HÀN", bấm Tìm kiếm.'], '—', ['Ra "Máy hàn".'], 28)
S2.add('Có dấu / không dấu', 'P1', PRE_LIST, [MENU, 'Nhập "may han", bấm Tìm kiếm.'], 'Ô tìm nhanh: may han',
       ['Ra "Máy hàn" (tìm không phân biệt dấu).'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "Thang máy", bấm Tìm kiếm.'], '—', [EMPTY + '.'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, ' + EMPTY + '.', 'Bước 3: không lỗi; % được tìm đúng ký tự nên ' + EMPTY + '.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "   Máy hàn   ", bấm Tìm kiếm.'], '—',
       ['Ra "Máy hàn" (bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Từ khóa rất dài', 'P2', PRE_LIST, [MENU, 'Dán chuỗi 300 ký tự vào ô tìm nhanh, bấm Tìm kiếm.'], 'Chuỗi 300 ký tự "a"',
       ['Ô nhận đủ (không giới hạn số ký tự), không lỗi, ' + EMPTY + '.'], 33)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "Máy hàn", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 1 danh sách chưa đổi; sau bước 2 hiện lại đủ 12 hệ số.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST, [MENU, 'Nhập "khí", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'],
       '—', ['Cả 2 cách đều ra Máy nén khí, Thiết bị hút khí thải; về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', PRE_LIST, [MENU, ADV], '—',
       ['3 ô Công ty, Người tạo, Người cập nhật đều trống.', 'Đủ 12 hệ số.'], 36)
S2.add('Lọc Công ty là công ty mình', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Công ty = Công ty cổ phần công nghệ thiết bị Tân Phát.'], '—',
       ['Vẫn đủ 12 hệ số.', 'Ô Công ty liệt kê mọi công ty trong hệ thống.'], 37)
S2.add('Lọc Công ty là công ty khác', 'P1', PRE_LIST, [MENU, ADV, 'Chọn Công ty = Công ty TNHH thiết bị Tân Phát Sài Gòn.'], '—',
       [EMPTY + ' (ô Công ty chỉ lọc thêm trong phạm vi công ty mình — giữ như hệ thống cũ).'], [37, 40])
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Mở ô Người tạo.', 'Chọn Người tạo = Bùi Duy Trước.'], '—',
       ['Ô chỉ có người đã tạo hệ số của công ty mình (A, Bùi Duy Trước), dạng "Họ tên - Mã phòng ban".',
        'Còn Máy cân bằng lốp, Máy nén khí.'], 37)
S2.add('Lọc Người cập nhật', 'P0', [PRE_LIST, H12], [MENU, ADV, 'Chọn Người cập nhật = Bùi Duy Trước.'], '—',
       ['Còn Lắp đặt cầu nâng, Máy cân bằng lốp, Máy nén khí.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', [PRE_LIST, H12], [MENU, ADV, 'Chọn Người tạo = A.', 'Chọn Người cập nhật = Bùi Duy Trước.'],
       '—', ['Chỉ còn "Lắp đặt cầu nâng".'], 38)
S2.add('Kết hợp tìm kiếm với bộ lọc', 'P0', PRE_LIST, [MENU, 'Nhập "lốp", bấm Tìm kiếm.', ADV, 'Chọn Người tạo = A.'], '—',
       ['Chỉ còn "Máy ra vào lốp" (Máy cân bằng lốp do Bùi Duy Trước tạo).'], 39)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "phòng sơn", bấm Tìm kiếm.', ADV, 'Chọn Người tạo = Bùi Duy Trước.'],
       '—', [EMPTY + '.'], 40)
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = A.', 'Đổi Số dòng/trang = 5, bấm trang 2.'],
       '—', ['"Hiển thị 1–5 / 10" rồi "Hiển thị 6–10 / 10"; STT 6–10.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Người tạo = A (10 hệ số).', ['Bấm tiêu đề Hệ số.'], '—',
       ['Chỉ 10 hệ số đang lọc được sắp tăng theo hệ số; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "Máy", lọc Người tạo = A, sắp theo Hệ số, ở trang 2.', ['Bấm Làm mới.'], '—',
       ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 12 hệ số.'], 44)
S2.add('Chuyển màn rồi quay lại', 'P1', 'Đang lọc Người tạo = Bùi Duy Trước, tìm "lốp".',
       ['Vào màn khác trong menu Bán hàng.', 'Quay lại màn Hệ số công nghệ theo nhóm hàng hóa.'], '—',
       ['Bộ lọc, ô tìm nhanh về trống, đủ 12 hệ số (màn không ghi nhớ bộ lọc).'], 45)
S2.add('Tải lại trang (F5)', 'P1', 'Đang lọc Người tạo = Bùi Duy Trước.', ['Nhấn F5.'], '—', ['Bộ lọc về trống, đủ 12 hệ số.'], 46)
S2.add('Mở màn ở tab mới', 'P2', 'Đang lọc Người tạo = Bùi Duy Trước ở tab 1.', ['Mở màn ở tab trình duyệt mới.'], '—',
       ['Tab mới bộ lọc trống, đủ 12 hệ số; tab 1 giữ nguyên.'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', [ACC_A, ACC_C], ['A lọc Người tạo = Bùi Duy Trước, đăng xuất.', 'Đăng nhập C, vào màn.'],
       '—', ['C thấy bộ lọc trống và chỉ 2 hệ số của công ty Tân Phát Sài Gòn.'], 48)
S2.add('Cài đặt bộ lọc: mở cửa sổ', 'P1', PRE_LIST, [MENU, 'Bấm "Cài đặt bộ lọc".'], '—',
       ['Mở cửa sổ "Cài đặt bộ lọc" có 3 mục tích sẵn: Công ty, Người tạo, Người cập nhật.',
        'Có nút Lưu, Khôi phục mặc định, Đóng.'], 36)
S2.add('Cài đặt bộ lọc: ẩn một ô lọc', 'P1', PRE_LIST, ['Mở Cài đặt bộ lọc.', 'Bỏ tích Công ty, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công", ô Công ty biến mất.',
        'Còn 3 ô (tìm nhanh + 2 ô lọc) nên 2 ô lọc bày thẳng cạnh ô tìm nhanh, nút Tìm kiếm nâng cao ẩn; nút Cài đặt bộ lọc vẫn còn.'], 36)
S2.add('Cài đặt bộ lọc: đổi thứ tự và khôi phục', 'P2', 'Đã ẩn ô Công ty.',
       ['Mở Cài đặt bộ lọc, kéo Người cập nhật lên đầu, bấm Lưu.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: ô Người cập nhật đứng trước Người tạo.', 'Bước 2: đủ 3 ô theo thứ tự Công ty, Người tạo, Người cập nhật.'], 36)
S2.add('Cài đặt bộ lọc: Đóng không lưu', 'P2', PRE_LIST, ['Mở Cài đặt bộ lọc, bỏ tích Người tạo.', 'Bấm Đóng.'], '—',
       ['Không hỏi xác nhận; khối lọc giữ nguyên 3 ô.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Mở popup Thêm mới', 'P0', ACC_A, TAO, '—',
       ['Mở popup trên màn danh sách, không chuyển trang.', 'Danh sách nhóm hàng hóa nạp xong thì ô Nhóm hết khóa.'], 49)
S3.add('Tiêu đề popup', 'P1', ACC_A, TAO, '—', ['Tiêu đề "Thêm mới tỷ lệ hưởng công khoán".'], 50)
S3.add('Các trường và nút', 'P0', ACC_A, TAO, '—',
       ['3 ô: Loại tỷ lệ hưởng (gợi ý "Nhập loại tỷ lệ hưởng"), Hệ số (gợi ý "Nhập hệ số", căn phải), Nhóm hàng hóa áp dụng (gợi ý '
        '"Chọn nhóm hàng hóa", chọn nhiều).', 'Nút Lưu, Lưu và tiếp tục, Đóng và (x) góc phải.'], [51, 54])
S3.add('Đánh dấu trường bắt buộc', 'P0', ACC_A, TAO, '—', ['Cả 3 nhãn đều có dấu * đỏ.'], 52)
S3.add('Giá trị mặc định', 'P1', ACC_A, TAO, '—', ['Cả 3 ô trống, không có giá trị điền sẵn.'], 53)
S3.add('Danh sách nhóm hàng hóa', 'P1', [ACC_A, 'Nhóm "Phòng sơn sấy xe bus" đã bị khóa ở danh mục nhóm hàng hóa.'],
       TAO + ['Mở ô Nhóm hàng hóa áp dụng, gõ "Phòng sơn".'], '—',
       ['Chỉ liệt kê nhóm đang hoạt động, xếp theo tên; KHÔNG có "Phòng sơn sấy xe bus".'], [51, 276])
S3.add('Lưu thành công đủ thông tin', 'P0', ACC_A, FILL + ['Bấm Lưu.'], FULL,
       ['Báo "Thêm mới thành công.", popup đóng.', 'Dòng "Lắp đặt máy nâng hạ" ở đầu trang 1, Hệ số "1.75", nhóm "Cầu nâng cắt kéo di '
        'động", Người tạo = Người cập nhật = A, Ngày tạo = Ngày cập nhật = lúc lưu.', 'Tổng tăng thành 13.'], [55, 58, 268, 269])
S3.add('Lưu chỉ với trường bắt buộc', 'P0', ACC_A, TAO + ['Nhập Loại "Máy bơm", Hệ số "1", chọn nhóm "Bơm thủy lực", bấm Lưu.'],
       ['Loại tỷ lệ hưởng: Máy bơm', 'Hệ số: 1', 'Nhóm: Bơm thủy lực'],
       ['Lưu thành công; Hệ số hiện "1.00".', 'Màn không có trường không bắt buộc nên không có trường nào để trống.'], [56, 57])
S3.add('Nhiều nhóm hàng hóa', 'P1', ACC_A, TAO + ['Nhập Loại "Máy rửa xe", Hệ số "0.9", chọn 2 nhóm "Máy rửa hơi nước nóng", '
                                                   '"Máy rửa áp lực cao treo tường", bấm Lưu.'], '—',
       ['Cột Nhóm hàng hóa hiện 2 dòng, xếp theo tên.'], [55, 283])
S3.add('Màn không có trạng thái mặc định', 'P2', ACC_A, FILL + ['Bấm Lưu.'], FULL,
       ['Hệ số lưu xong có hiệu lực ngay, không có cột / nhãn trạng thái.'], 59)
S3.add('Ghi lịch sử Tạo mới', 'P0', 'A vừa tạo "Lắp đặt máy nâng hạ".', ['Bấm Lịch sử ở dòng đó.'], '—',
       ['Có 1 mốc "Tạo mới" màu xanh lá, Người thực hiện A, thời điểm lúc lưu.'], [60, 176])
S3.add('Bỏ trống tất cả trường bắt buộc', 'P0', ACC_A, TAO + ['Bấm Lưu.'], '—',
       ['Viền đỏ + chữ đỏ dưới 3 ô: Loại ' + REQ + ', Hệ số "Bắt buộc phải nhập.", Nhóm ' + REQ + '.',
        'Thông báo ' + MISS + ', popup không đóng, không lưu.'], [61, 70])
S3.add('Bỏ trống từng trường', 'P0', ACC_A, TAO + ['Nhập đủ trừ ô Nhóm hàng hóa, bấm Lưu.'], '—',
       ['Chỉ ô Nhóm báo ' + REQ + '; 2 ô đã nhập không báo lỗi; dữ liệu đã nhập còn nguyên.'], 61)
S3.add('Ô Hệ số chặn ký tự sai định dạng', 'P0', ACC_A, TAO + ['Gõ "1a-2.555" vào ô Hệ số.'], 'Hệ số: 1a-2.555',
       ['Ô chỉ còn "12.55": chữ, dấu âm bị bỏ, số lẻ thứ 3 bị bỏ ngay khi gõ.'], [62, 63])
S3.add('Hệ số vượt trần', 'P1', ACC_A, TAO + ['Nhập Hệ số "1000000".'], 'Hệ số: 1000000',
       ['Chữ đỏ dưới ô "Hệ số – Không được lớn hơn 999,999.99"; bấm Lưu không gửi.'], [62, 66])
S3.add('Hệ số bằng 0 và trần 999999.99', 'P2', ACC_A, TAO + ['Nhập đủ, Hệ số "0", Lưu.', 'Tạo tiếp hệ số khác với Hệ số "999999.99".'],
       '—', ['Cả 2 lưu được; danh sách hiện "0.00" và "999,999.99".'], [64, 65])
S3.add('Ký tự đặc biệt trong Loại tỷ lệ hưởng', 'P2', ACC_A, TAO + ['Nhập Loại "Lắp đặt (A&B) - 50%", đủ ô khác, Lưu.'], '—',
       ['Lưu được, tên hiện đúng nguyên văn (ô nhận mọi ký tự).'], [63, 230])
S3.add('Loại tỷ lệ hưởng đúng 255 ký tự', 'P1', ACC_A, TAO + ['Nhập Loại đúng 255 ký tự, đủ ô khác, Lưu.'], 'Loại: 255 ký tự',
       ['Lưu thành công.'], 65)
S3.add('Loại tỷ lệ hưởng 256 ký tự', 'P1', ACC_A, TAO + ['Nhập Loại 256 ký tự.'], 'Loại: 256 ký tự',
       ['Chữ đỏ dưới ô "Vui lòng nhập tối đa 255 ký tự."; bấm Lưu báo ' + MISS + ', không lưu.'], 66)
S3.add('Trùng Loại tỷ lệ hưởng trong công ty', 'P0', PRE_LIST, TAO + ['Nhập Loại "máy hàn", Hệ số 1, nhóm "Máy hàn bấm", Lưu.'], '—',
       ['Chữ đỏ dưới ô Loại ' + DUP + ', thông báo cùng câu; popup giữ dữ liệu, không lưu.',
        'Trùng không phân biệt hoa / thường.'], [67, 70])
S3.add('Trùng tên khác dấu', 'P2', PRE_LIST, TAO + ['Nhập Loại "May han", đủ ô khác, Lưu.'], '—',
       ['Báo ' + DUP + ' (so sánh tên không phân biệt dấu).'], 67)
S3.add('Trùng tên với hệ số của công ty khác', 'P1', [PRE_LIST, ACC_C], ['Đăng nhập C.', 'Bấm Tạo mới, nhập Loại "Kích nâng", Hệ số 1, '
                                                                          'nhóm "Kích phụ", Lưu.'], '—',
       ['Lưu thành công (chỉ chặn trùng trong cùng công ty).'], 67)
S3.add('Nhóm hàng hóa đã thuộc loại hệ số khác', 'P0', PRE_LIST, TAO + ['Nhập Loại "Cầu nâng mới", Hệ số 1, chọn nhóm "Cầu nâng 4 trụ", Lưu.'],
       '—', ['Chữ đỏ dưới ô Nhóm "Cầu nâng 4 trụ đã thuộc loại hệ số khác.", thông báo cùng câu, không lưu.'], [67, 70, 286])
S3.add('Nhóm đã gắn ở công ty khác cũng bị chặn', 'P0', [PRE_LIST, ACC_C, 'Nhóm "Cầu nâng cắt kéo di động" đang gắn hệ số của công ty '
                                                                        'Tân Phát Sài Gòn.'],
       ['Đăng nhập A.', 'Tạo hệ số mới, chọn nhóm "Cầu nâng cắt kéo di động", Lưu.'], '—',
       ['Báo "Cầu nâng cắt kéo di động đã thuộc loại hệ số khác." (kiểm trên toàn hệ thống).'], [67, 286])
S3.add('Khoảng trắng đầu / cuối được bỏ', 'P1', ACC_A, TAO + ['Nhập Loại "   Máy khoan   ", đủ ô khác, Lưu.'], '—',
       ['Lưu với tên "Máy khoan" (không còn khoảng trắng đầu / cuối).'], 68)
S3.add('Chỉ nhập khoảng trắng', 'P1', ACC_A, TAO + ['Nhập Loại "     ", đủ ô khác, Lưu.'], '—',
       ['Ô Loại báo ' + REQ + ', không lưu.'], 69)
S3.add('Lỗi biến mất sau khi sửa', 'P1', 'Popup đang báo lỗi đỏ ở 3 ô.', ['Nhập Loại, Hệ số, chọn 1 nhóm.'], '—',
       ['Lỗi dưới từng ô mất ngay khi ô đó hợp lệ.'], 71)
S3.add('Lưu và tiếp tục dữ liệu hợp lệ', 'P0', ACC_A, FILL + ['Bấm Lưu và tiếp tục.'], FULL,
       ['Báo "Thêm mới thành công.".', 'Popup VẪN MỞ, 3 ô trở về trống, không còn lỗi.', 'Danh sách phía sau đã có dòng mới.'],
       [72, 76, 77])
S3.add('Lưu và tiếp tục thiếu bắt buộc', 'P1', ACC_A, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       ['Báo lỗi 3 ô + ' + MISS + ', không lưu.'], 73)
S3.add('Lưu và tiếp tục sai định dạng', 'P2', ACC_A, TAO + ['Nhập Hệ số "1000000", bấm Lưu và tiếp tục.'], '—',
       ['Báo "Hệ số – Không được lớn hơn 999,999.99", không lưu.'], 74)
S3.add('Lưu và tiếp tục trùng dữ liệu', 'P1', PRE_LIST, TAO + ['Nhập Loại "Máy hàn", Hệ số 1, nhóm "Máy hàn bấm", bấm Lưu và tiếp tục.'],
       '—', ['Báo ' + DUP + ', popup giữ dữ liệu, không làm trắng form.'], 75)
S3.add('Đóng sau Lưu và tiếp tục', 'P1', 'Vừa Lưu và tiếp tục xong, form đang trống.', ['Bấm Đóng.'], '—',
       ['Popup đóng ngay, không hỏi; danh sách có hệ số vừa lưu.'], 78)
S3.add('Đóng khi chưa nhập', 'P1', ACC_A, TAO + ['Bấm Đóng.'], '—', ['Popup đóng ngay, không hỏi.'], 93)
S3.add('Đóng khi đã nhập', 'P0', ACC_A, TAO + ['Nhập Loại "Thử".', 'Bấm Đóng.'], '—', ['Hiện hộp ' + UNSAVED + ', nút Thoát và Ở lại.'], 94)
S3.add('Đóng bằng X hoặc click ra ngoài', 'P1', ACC_A, TAO + ['Nhập Hệ số "2".', 'Bấm (x).', 'Chọn Ở lại, click ra ngoài popup.'], '—',
       ['Cả 2 lần đều hiện hộp "Thông tin chưa lưu".'], 95)
S3.add('Chọn Thoát', 'P0', 'Đang ở hộp "Thông tin chưa lưu".', ['Bấm Thoát.'], '—',
       ['Popup đóng, không lưu; mở lại Tạo mới thì form trống.'], 96)
S3.add('Chọn Ở lại', 'P1', 'Đang ở hộp "Thông tin chưa lưu", đã nhập Loại "Thử".', ['Bấm Ở lại.'], '—',
       ['Quay lại popup, ô Loại vẫn "Thử".'], 97)
S3.add('Nhập rồi xóa hết', 'P2', ACC_A, TAO + ['Nhập Loại "Thử" rồi xóa hết.', 'Bấm Đóng.'], '—', ['Đóng ngay, không hỏi.'], 98)
S3.add('Đổi rồi khôi phục ban đầu', 'P2', ACC_A, TAO + ['Chọn 1 nhóm rồi bấm × bỏ nhóm đó.', 'Bấm Đóng.'], '—', ['Đóng ngay, không hỏi.'], 99)
S3.add('Không thao tác lâu', 'P2', ACC_A, TAO + ['Nhập đủ, để yên 30 phút (phiên còn hạn).', 'Bấm Lưu.'], '—',
       ['Lưu bình thường; dữ liệu đã nhập không mất.'], 100)
S3.add('Bấm Lưu liên tục', 'P0', ACC_A, FILL + ['Bấm Lưu 3 lần thật nhanh.'], '—',
       ['Nút khóa trong lúc lưu; chỉ tạo 1 hệ số "Lắp đặt máy nâng hạ".'], 101)
S3.add('Tạo trùng đồng thời 2 tab', 'P2', ACC_A, ['Mở 2 tab, cùng mở Tạo mới, nhập Loại "Máy tiện", Hệ số 1, nhóm khác nhau.',
                                                   'Lưu tab 1.', 'Lưu tab 2.'], '—',
       ['Tab 1 lưu được; tab 2 báo ' + DUP + '.'], 102)

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
S4.add('Mở popup Sửa', 'P0', PRE_LIST, EDIT, '—',
       ['Mở popup "Chỉnh sửa tỷ lệ hưởng công khoán" trên màn danh sách.'], 103)
S4.add('Dữ liệu điền đúng', 'P0', PRE_LIST, EDIT, '—',
       ['Loại "Máy nén khí", Hệ số "1", Nhóm 2 thẻ "Máy nén khí piston", "Máy nén khí trục vít".'], [104, 64])
S4.add('Trường được sửa', 'P1', PRE_LIST, EDIT, '—', ['Cả 3 ô đều sửa được; không có trường chỉ đọc.'], 105)
S4.add('Các nút trên popup Sửa', 'P1', PRE_LIST, EDIT, '—', ['Chỉ có Lưu, Đóng và (x); KHÔNG có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_LIST, EDIT + ['Đổi Hệ số thành "1.1", bấm Lưu.'], 'Hệ số: 1.1',
       ['Báo "Cập nhật thành công.", popup đóng.', 'Dòng hiện Hệ số "1.10"; danh sách giữ trang đang xem.'], [107, 110])
S4.add('Sửa nhiều trường', 'P0', PRE_LIST, EDIT + ['Đổi Loại "Máy nén khí công nghiệp", Hệ số "1.4", thêm nhóm "Máy nén khí piston không '
                                                     'dầu", Lưu.'], '—',
       ['Lưu thành công, cả 3 thay đổi hiện trên dòng.'], 108)
S4.add('Giữ nguyên tên của chính mình', 'P0', PRE_LIST, EDIT + ['Không đổi Loại, chỉ đổi Hệ số "1.05", Lưu.'], '—',
       ['Lưu được, KHÔNG báo trùng với chính bản ghi.', 'Giữ nguyên 2 nhóm của chính bản ghi cũng không báo "đã thuộc loại hệ số khác".'],
       [109, 68])
S4.add('Ngày / người cập nhật', 'P0', [PRE_LIST, ACC_B], ['Đăng nhập B.', 'Sửa "Máy nén khí" đổi Hệ số "1.2", Lưu.'], '—',
       ['Người cập nhật = B, Ngày cập nhật = lúc lưu; Người tạo, Ngày tạo giữ nguyên.'], 111)
S4.add('Chỉ đổi nhóm cũng cập nhật ngày', 'P1', PRE_LIST, EDIT + ['Chỉ thêm nhóm "Máy nén khí trục vít không dầu", Lưu.'], '—',
       ['Ngày cập nhật đổi thành lúc lưu, Người cập nhật = người sửa.'], 111)
S4.add('Ghi lịch sử sửa', 'P0', 'Vừa đổi Hệ số "Máy nén khí" từ 1.00 thành 1.10.', ['Bấm Lịch sử ở dòng.'], '—',
       ['Mốc mới nhất "Thay đổi thông tin", "Hệ số: 1.00 sang 1.10", người sửa, thời điểm.'], [112, 177])
S4.add('Bỏ trống trường bắt buộc khi sửa', 'P0', PRE_LIST, EDIT + ['Xóa hết Loại, bỏ hết nhóm, bấm Lưu.'], '—',
       ['Ô Loại và ô Nhóm báo ' + REQ + ', thông báo ' + MISS + ', không lưu.'], [113, 117])
S4.add('Sai định dạng khi sửa', 'P1', PRE_LIST, EDIT + ['Xóa hết ô Hệ số rồi gõ "abc".'], '—', ['Ô bỏ chữ, còn trống, báo "Bắt buộc phải nhập.".'], 114)
S4.add('Vượt giới hạn khi sửa', 'P1', PRE_LIST, EDIT + ['Nhập Loại 256 ký tự, Hệ số "1000000".'], '—',
       ['"Vui lòng nhập tối đa 255 ký tự." và "Hệ số – Không được lớn hơn 999,999.99".'], 115)
S4.add('Trùng tên hệ số khác', 'P0', PRE_LIST, EDIT + ['Đổi Loại thành "Máy hàn", Lưu.'], '—', ['Báo ' + DUP + ', không lưu.'], [116, 117])
S4.add('Trùng nhóm của hệ số khác', 'P0', PRE_LIST, EDIT + ['Thêm nhóm "Máy hàn TIG", Lưu.'], '—',
       ['Báo "Máy hàn TIG đã thuộc loại hệ số khác.", không lưu.'], [116, 286])
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Popup Sửa đang báo trùng tên.', ['Đổi Loại thành "Máy nén khí 2".'], '—',
       ['Lỗi dưới ô Loại mất ngay.'], 118)
S4.add('Mở không thay đổi rồi đóng', 'P1', PRE_LIST, EDIT + ['Bấm Đóng.'], '—', ['Đóng ngay, không hỏi.'], 119)
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_LIST, EDIT + ['Đổi Hệ số "2" rồi gõ lại "1".', 'Bấm Đóng.'], '—', ['Đóng ngay, không hỏi.'], 120)
S4.add('Đóng khi đã đổi', 'P0', PRE_LIST, EDIT + ['Đổi Hệ số "2".', 'Bấm Đóng.'], '—', ['Hiện hộp ' + UNSAVED + '.'], 121)
S4.add('Xác nhận Thoát', 'P1', 'Hộp "Thông tin chưa lưu" đang mở sau khi đổi Hệ số "Máy nén khí" thành 2.', ['Bấm Thoát.'], '—',
       ['Popup đóng; dòng vẫn Hệ số "1.00".'], [122, 124])
S4.add('Xác nhận Ở lại', 'P1', 'Hộp "Thông tin chưa lưu" đang mở.', ['Bấm Ở lại.'], '—', ['Quay lại popup, Hệ số vẫn "2".'], 123)
S4.add('Không ghi lịch sử khi không thay đổi', 'P0', PRE_LIST, EDIT + ['Không đổi gì, bấm Lưu.', 'Mở Lịch sử của dòng.'], '—',
       ['Báo "Cập nhật thành công.".', 'Không có mốc "Thay đổi thông tin" mới.'], [125, 182])
S4.add('Nhóm đã khóa vẫn giữ khi sửa', 'P1', [PRE_LIST, PHONGSON], [MENU, 'Bấm Sửa ở dòng "Lắp đặt phòng sơn".', 'Đổi Hệ số "2.1", Lưu.'],
       '—', ['Thẻ "Phòng sơn sấy xe bus" có biểu tượng ổ khóa trước tên.', 'Lưu được, nhóm khóa vẫn được giữ.'], [284, 105])
S4.add('Bản ghi bị người khác xóa', 'P0', [PRE_LIST, 'B vừa xóa "Máy nén khí" sau khi A đã mở danh sách.'],
       ['A bấm Sửa ở dòng "Máy nén khí".'], '—', ['Thông báo ' + CONFLICT + ', popup tự đóng, danh sách nạp lại không còn dòng đó.'], 127)
S4.add('Bản ghi bị xóa khi đang mở popup Sửa', 'P1', 'A đang mở popup Sửa "Máy nén khí"; B xóa hệ số này.', ['A bấm Lưu.'], '—',
       ['Thông báo ' + CONFLICT + '; không tạo lại bản ghi.'], 127)
S4.add('Hai người sửa đồng thời', 'P1', [ACC_A, ACC_B], ['A và B cùng mở Sửa "Máy nén khí".', 'A đổi Hệ số 1.1, Lưu.',
                                                         'B đổi Hệ số 1.3, Lưu.'], '—',
       ['Cả 2 lần đều lưu được; kết quả cuối 1.30 (lần sau ghi đè).', 'Lịch sử có 2 mốc: 1.00 sang 1.10 và 1.10 sang 1.30.'], 128)
S4.add('Hệ số đang được dùng ở phiếu', 'P1', ['Phiếu duyệt kết quả X đã lưu dòng lắp đặt hàng nhóm "Máy nén khí trục vít" với hệ số 1.00.'],
       EDIT + ['Đổi Hệ số "1.5", Lưu.', 'Mở lại phiếu X.'], '—',
       ['Sửa được (không chặn).', 'Phiếu X vẫn giữ hệ số 1.00 đã lưu; chỉ lần duyệt mới mới lấy 1.50.'], [129, 272])

# ============================================================== V. XÓA
S5 = Sec(5)
S5.add('Nút Xóa trên dòng', 'P0', PRE_LIST, [MENU, 'Quan sát cột Hành động.'], '—',
       ['Mọi dòng có nút thùng rác đỏ, rê chuột hiện "Xóa".'], 130)
S5.add('Hộp xác nhận xóa', 'P0', PRE_LIST, [MENU, 'Bấm Xóa ở dòng "Máy hàn".'], '—',
       ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?", nút Xóa (đỏ), Hủy.',
        'Hộp không nêu tên bản ghi.'], [131, 132])
S5.add('Xóa thành công', 'P0', PRE_LIST, [MENU, 'Bấm Xóa ở dòng "Máy hàn".', 'Bấm Xóa.'], '—',
       ['Báo "Xóa thành công.", hộp đóng.', 'Dòng "Máy hàn" biến mất; "Hiển thị 1–10 / 11".'], [133, 139, 140])
S5.add('Hủy xóa', 'P0', PRE_LIST, [MENU, 'Bấm Xóa ở dòng "Máy hàn".', 'Bấm Hủy (lần 2: bấm (x), lần 3: click ra ngoài).'], '—',
       ['Hộp đóng, dòng vẫn còn, tổng vẫn 12.'], 134)
S5.add('Xóa hệ số đang được dùng ở phiếu', 'P1', ['Phiếu duyệt kết quả X đã lưu dòng lắp đặt hàng nhóm "Máy hàn TIG" với hệ số 1.00.'],
       [MENU, 'Xóa "Máy hàn".', 'Mở lại phiếu X.'], '—',
       ['Xóa được, không bị chặn (phiếu chỉ chép số hệ số).', 'Phiếu X vẫn giữ hệ số 1.00.'], [135, 141, 270])
S5.add('Xóa kéo theo các nhóm áp dụng', 'P0', PRE_LIST, ['Xóa "Máy hàn".', 'Tạo hệ số mới "Máy hàn 2" chọn nhóm "Máy hàn TIG", Lưu.'], '—',
       ['Bước 2 lưu được: nhóm của hệ số đã xóa được giải phóng, không còn liên kết thừa.'], [136, 285])
S5.add('Xóa bản ghi đã bị người khác xóa', 'P0', 'A đang xem danh sách; B vừa xóa "Máy hàn".', ['A bấm Xóa ở dòng "Máy hàn", bấm Xóa.'],
       '—', ['Thông báo ' + CONFLICT + '; danh sách nạp lại không còn dòng đó.'], 138)
S5.add('Ghi lịch sử xóa', 'P2', 'A vừa xóa "Máy hàn".', ['Kiểm tra danh sách và tìm "Máy hàn".'], '—',
       ['Không tìm thấy; lịch sử "Xóa" được hệ thống ghi nhưng không mở xem được trên màn vì bản ghi đã mất.'], 141)

# ============================================================== VI. LỊCH SỬ THAY ĐỔI
S6 = Sec(6)
S6.add('Mở cửa sổ Lịch sử', 'P0', [PRE_LIST, H12], [MENU, 'Bấm Lịch sử (đồng hồ) ở dòng "Lắp đặt cầu nâng".'], '—',
       ['Cửa sổ "Lịch sử thay đổi: Lắp đặt cầu nâng".'], 162)
S6.add('Nội dung mỗi mốc', 'P0', [PRE_LIST, H12], [MENU, 'Mở Lịch sử "Lắp đặt cầu nâng".'], '—',
       ['Mỗi mốc có thời điểm, hành động, "Người thực hiện: <tên> — <phòng ban>".',
        'Mốc "Thay đổi thông tin" có "Hệ số: 1.20 sang 1.50" và "Nhóm hàng hóa áp dụng" dạng khối Trước / Sau, mỗi nhóm một dòng.'],
       [163, 165, 166, 167, 168])
S6.add('Mới nhất trước', 'P0', [PRE_LIST, H12], [MENU, 'Mở Lịch sử "Lắp đặt cầu nâng".'], '—',
       ['Mốc 06/11/2026 08:40 "Thay đổi thông tin" ở trên, mốc 05/11/2026 09:15 "Tạo mới" ở dưới.'], 164)
S6.add('Lọc theo Loại hành động', 'P1', [PRE_LIST, H12], ['Mở Lịch sử "Lắp đặt cầu nâng", bấm Bộ lọc.', 'Chọn Loại hành động = Tạo mới.'],
       '—', ['Ô có 3 lựa chọn: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.', 'Chỉ còn mốc "Tạo mới".'], [169, 175])
S6.add('Lọc theo Người thực hiện', 'P1', [PRE_LIST, H12], ['Mở Lịch sử, bấm Bộ lọc.', 'Chọn Người thực hiện = Bùi Duy Trước.'], '—',
       ['Chỉ còn mốc "Thay đổi thông tin".', 'Ô liệt kê nhân viên cùng công ty, dạng "Tên - Mã phòng - Mã NV".'], 170)
S6.add('Lọc theo thời gian', 'P1', [PRE_LIST, H12], ['Mở Lịch sử, bấm Bộ lọc.', 'Chọn Từ ngày 06/11/2026.'], '—',
       ['Chỉ còn mốc 06/11/2026.'], 171)
S6.add('Kết hợp lọc và không có kết quả', 'P2', [PRE_LIST, H12], ['Bộ lọc: Loại = Tạo mới, Người thực hiện = Bùi Duy Trước.'], '—',
       ['"Không có lịch sử phù hợp bộ lọc."'], [172, 173])
S6.add('Làm mới bộ lọc lịch sử', 'P2', 'Đang lọc Loại = Tạo mới.', ['Bấm Làm mới trong cửa sổ.'], '—', ['Hiện lại đủ 2 mốc.'], 174)
S6.add('Sửa nhiều trường một lần', 'P1', PRE_LIST, ['Sửa "Máy nén khí": đổi Loại, Hệ số và thêm 1 nhóm, Lưu.', 'Mở Lịch sử.'], '—',
       ['MỘT mốc "Thay đổi thông tin" liệt kê cả 3 trường cũ sang mới.'], [178, 183])
S6.add('Hệ số chưa có lịch sử', 'P2', 'Hệ số "Hệ số 1" tạo trước khi màn ghi lịch sử, chưa sửa lần nào.', ['Mở Lịch sử.'], '—',
       ['"Chưa có lịch sử thao tác nào."'], 167)
S6.add('Đóng cửa sổ', 'P1', 'Đang ở trang 2, lọc Người tạo = A, mở Lịch sử 1 dòng.', ['Bấm Đóng (lần 2: (x)).'], '—',
       ['Cửa sổ đóng; danh sách giữ trang 2 và bộ lọc.'], [184, 185])

# ============================================================== VII. XEM CHI TIẾT
S7 = Sec(7)
S7.add('Mở popup Xem', 'P0', PRE_LIST, [MENU, 'Bấm vào chữ "Lắp đặt cầu nâng" ở cột Loại hệ số.'], '—',
       ['Mở popup "Xem tỷ lệ hưởng công khoán" trên màn danh sách.'], [186, 187])
S7.add('Đầy đủ trường và khớp dữ liệu', 'P0', [PRE_LIST, H12], [MENU, 'Mở Xem "Lắp đặt cầu nâng".'], '—',
       ['Loại "Lắp đặt cầu nâng", Hệ số "1.5", 3 thẻ nhóm khớp cột Nhóm hàng hóa trên danh sách.',
        'Lưu ý: ô Hệ số hiện số đã lưu "1.5" (danh sách hiện "1.50").'], [188, 189, 190])
S7.add('Trường chỉ đọc, không có nút Lưu', 'P0', PRE_LIST, [MENU, 'Mở Xem "Máy hàn".', 'Thử gõ vào các ô.'], '—',
       ['Các ô nền xám, không sửa được; thẻ nhóm không có nút ×.', 'Chân popup chỉ có Đóng.'], [191, 192, 193])
S7.add('Nhóm đã khóa trong popup Xem', 'P2', [PRE_LIST, PHONGSON], [MENU, 'Mở Xem "Lắp đặt phòng sơn".'], '—',
       ['Thẻ "Phòng sơn sấy xe bus" có biểu tượng ổ khóa.'], 284)
S7.add('Khu vực lịch sử', 'P1', [PRE_LIST, H12], ['Mở Xem "Lắp đặt cầu nâng".', 'Bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử ban đầu thu gọn, có số mốc.', 'Bấm sang mở 2 mốc như cửa sổ Lịch sử; có Làm mới, Thu gọn, Bộ lọc.'], 195)
S7.add('Đóng popup giữ trang và bộ lọc', 'P1', 'Đang ở trang 2, sắp theo Hệ số.', ['Mở Xem 1 dòng.', 'Bấm Đóng (hoặc (x), click ra ngoài).'],
       '—', ['Đóng không hỏi; danh sách giữ trang 2 và thứ tự sắp xếp.'], [196, 197])
S7.add('Xem hệ số đã bị xóa', 'P1', 'B vừa xóa "Máy hàn" khi A đang ở danh sách.', ['A bấm "Máy hàn".'], '—',
       ['Thông báo ' + CONFLICT + ', popup tự đóng, danh sách nạp lại.'], 186)

# ============================================================== VIII. TÙY CHỈNH CỘT
S8 = Sec(8)
S8.add('Mở cửa sổ Tuỳ chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" liệt kê 9 cột theo thứ tự bảng, "Đang chọn 9/9 cột".'], [198, 199, 200])
S8.add('Ẩn cột', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột, bỏ tích Người cập nhật, Ngày cập nhật, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; bảng còn 7 cột.'], 202)
S8.add('Hiện lại cột đã ẩn', 'P1', 'Đã ẩn Người cập nhật, Ngày cập nhật.', ['Mở Tuỳ chỉnh cột, bấm Chọn tất cả, Lưu.'], '—',
       ['Bảng hiện lại đủ 9 cột.'], 201)
S8.add('Cột bắt buộc không ẩn được', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột.', 'Bấm Bỏ chọn hết.'], '—',
       ['STT, Loại hệ số, Hành động có ổ khóa, ô tích mờ, vẫn tích sau Bỏ chọn hết; "Đang chọn 3/9 cột".'], [203, 205])
S8.add('Kéo thả đổi thứ tự', 'P1', PRE_LIST, ['Mở Tuỳ chỉnh cột, kéo Nhóm hàng hóa lên trước Hệ số, Lưu.'], '—',
       ['Bảng hiện Nhóm hàng hóa trước Hệ số; cột khóa không kéo được.'], [204, 205])
S8.add('Đóng không lưu', 'P1', PRE_LIST, ['Mở Tuỳ chỉnh cột, bỏ tích Hệ số.', 'Bấm Đóng.'], '—', ['Không hỏi; bảng giữ nguyên cột Hệ số.'], 207)
S8.add('Ghi nhớ sau tải lại và đăng nhập lại', 'P0', 'A đã ẩn cột Ngày tạo.', ['Nhấn F5.', 'Đăng xuất, đăng nhập lại A ở trình duyệt khác.'],
       '—', ['Cả 2 lần cột Ngày tạo vẫn ẩn.'], [206, 208])
S8.add('Cấu hình theo tài khoản', 'P1', 'A đã ẩn cột Ngày tạo.', ['Đăng nhập B, vào màn.'], '—', ['B vẫn thấy đủ 9 cột.'], 209)
S8.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P1', 'Đang lọc Người tạo = A, ở trang 2.', ['Ẩn cột Hệ số, Lưu.'], '—',
       ['Tổng "/ 10" và bộ lọc giữ nguyên; dữ liệu không đổi.'], [210, 211])

# ============================================================== IX. XUẤT DANH SÁCH EXCEL
S9 = Sec(9)
S9.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất file" có 7 trường: Loại hệ số, Hệ số, Nhóm hàng hóa, Người tạo, Ngày tạo, Người cập nhật, Ngày '
        'cập nhật.', 'Có Chọn tất cả, Bỏ chọn hết, "Đang chọn 7/7 trường", Xuất file, Đóng.'], [212, 213])
S9.add('Trường chọn mặc định theo cột đang hiện', 'P1', 'A đã ẩn cột Người cập nhật, Ngày cập nhật.', ['Bấm Xuất Excel.'], '—',
       ['Tích sẵn 5 trường đang hiện; 2 trường đã ẩn không tích ("Đang chọn 5/7 trường").'], 214)
S9.add('Xuất với trường mặc định', 'P0', PRE_LIST, ['Bấm Xuất Excel.', 'Bấm Xuất file.'], '—',
       ['Tải file he-so-cong-nghe-theo-nhom-hang-hoa.xlsx, báo "Xuất Excel thành công.".',
        'File có STT + 7 cột, 12 dòng (cả 2 trang, không chỉ trang đang xem).'], [215, 221, 223, 227])
S9.add('Xuất tất cả / một số trường', 'P1', PRE_LIST, ['Bấm Xuất Excel, Bỏ chọn hết, tích Loại hệ số và Hệ số, Xuất file.'], '—',
       ['File chỉ có STT, Loại hệ số, Hệ số.'], [216, 217])
S9.add('Không chọn trường nào', 'P1', PRE_LIST, ['Bấm Xuất Excel, Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S9.add('Xuất theo tìm kiếm và bộ lọc', 'P0', PRE_LIST, ['Tìm "lốp".', 'Xuất Excel đủ trường.', 'Làm mới, lọc Người tạo = Bùi Duy Trước, Xuất.'],
       '—', ['Lần 1: 2 dòng Máy ra vào lốp, Máy cân bằng lốp.', 'Lần 2: 2 dòng Máy cân bằng lốp, Máy nén khí.'], [219, 220])
S9.add('Danh sách rỗng', 'P1', PRE_LIST, ['Tìm "ZZZ", bấm Xuất Excel, Xuất file.'], '—',
       ['Thông báo "Không có dữ liệu để xuất", KHÔNG tải file.'], 222)
S9.add('Định dạng và nội dung file', 'P0', [PRE_LIST, H12], ['Xuất đủ trường, mở file.'], '—',
       ['Letterhead công ty Tân Phát trên cùng, tiêu đề "HỆ SỐ CÔNG NGHỆ THEO NHÓM HÀNG HÓA", khối ký "Người lập".',
        'Hàng tiêu đề cột không có nút lọc.', 'Tên cột đúng như cửa sổ chọn trường.'], [224, 225])
S9.add('Thứ tự cột theo kéo thả', 'P1', PRE_LIST, ['Bấm Xuất Excel, kéo Hệ số lên đầu, Xuất file.'], '—',
       ['File: STT, Hệ số, Loại hệ số, …'], 226)
S9.add('Dữ liệu khớp màn hình', 'P0', [PRE_LIST, H12], ['Xuất đủ trường, đối chiếu dòng "Lắp đặt cầu nâng".'], '—',
       ['Hệ số là ô SỐ 1.50; Nhóm hàng hóa 3 dòng trong 1 ô; ngày dạng dd/mm/yyyy hh:mm; người tạo / cập nhật đúng.'], [228, 229])
S9.add('Tiếng Việt và ký tự đặc biệt', 'P2', 'Có hệ số "Lắp đặt (A&B) - 50%".', ['Xuất Excel, mở file.'], '—',
       ['Tiếng Việt có dấu và ký tự đặc biệt hiện đúng.'], 230)

# ============================================================== X. RÀNG BUỘC
S10 = Sec(10)
RD = ('Phiếu nhập kết quả Y (CSKH sau bán) ở trạng thái Chờ duyệt kết quả, có dòng lắp đặt hàng thuộc nhóm "Cầu nâng 4 trụ", công khoán '
      'đề xuất 2, dòng chưa ghi hệ số.')
DUYET = ['Vào phân hệ CSKH sau bán > nhóm "Giao việc" > "Phiếu nhập kết quả".', 'Mở phiếu Y, bấm Duyệt kết quả.']
S10.add('Duyệt kết quả lấy hệ số theo nhóm', 'P0', [PRE_LIST, RD], DUYET, '—',
       ['Dòng lắp đặt hiện Hệ số 1.5 (của "Lắp đặt cầu nâng").', 'Kết quả công khoán = công khoán duyệt x 1.5.'], [274, 283])
S10.add('Nhóm chưa có hệ số lấy 1', 'P0', ['Phiếu nhập kết quả Y2 có dòng lắp đặt hàng thuộc nhóm "Máy khoan cần" chưa gắn hệ số nào.'],
        ['Vào Phiếu nhập kết quả, mở Y2, bấm Duyệt kết quả.'], '—', ['Dòng lắp đặt hiện Hệ số 1.'], 268)
S10.add('Hệ số mới tạo dùng ngay', 'P1', ['A vừa tạo hệ số "Máy khoan" 1.3 gắn nhóm "Máy khoan cần".', 'Phiếu Y2 như trên, chưa duyệt.'],
        ['Mở Duyệt kết quả phiếu Y2.'], '—', ['Dòng lắp đặt hiện Hệ số 1.3.'], [274, 282])
S10.add('Sửa hệ số không đổi phiếu đã lưu', 'P0', [RD, 'Phiếu Y đã lưu Duyệt kết quả với Hệ số 1.5.'],
        ['Sửa "Lắp đặt cầu nâng" thành 2.0.', 'Mở lại phiếu Y.'], '—', ['Phiếu Y vẫn hiện Hệ số 1.5 đã lưu.'], [272, 129])
S10.add('Xóa hệ số thì lần duyệt sau lấy 1', 'P1', RD, ['Xóa "Lắp đặt cầu nâng".', 'Mở Duyệt kết quả phiếu Y (chưa lưu lần nào).'], '—',
        ['Dòng lắp đặt hiện Hệ số 1.'], 280)
S10.add('Đổi tên nhóm hàng hóa đồng bộ', 'P2', 'Nhóm "Cầu nâng 4 trụ" được đổi tên thành "Cầu nâng 4 trụ thủy lực" ở danh mục nhóm hàng hóa.',
        [MENU, 'Quan sát dòng "Lắp đặt cầu nâng".'], '—', ['Cột Nhóm hàng hóa hiện tên mới; liên kết không mất.'], 278)
S10.add('Nhóm bị khóa không chọn mới nhưng giữ liên kết', 'P1', PHONGSON,
        ['Tạo hệ số mới, tìm "Phòng sơn sấy xe bus".', 'Mở Sửa "Lắp đặt phòng sơn".'], '—',
        ['Bước 1: không có nhóm đó để chọn.', 'Bước 2: nhóm vẫn hiện kèm ổ khóa, không mất liên kết.'], [276, 284])
S10.add('Mỗi nhóm thuộc một hệ số', 'P0', PRE_LIST, ['Thử gắn "Cầu nâng 1 trụ" cho "Máy nén khí" (Sửa) và cho hệ số mới (Tạo).'], '—',
        ['Cả 2 lần báo "Cầu nâng 1 trụ đã thuộc loại hệ số khác."; không có nhóm nào thuộc 2 hệ số.'], [286, 283])
S10.add('Ô Người tạo cập nhật sau khi thêm', 'P2', [PRE_LIST, 'Tài khoản E cùng công ty Tân Phát, chưa tạo hệ số nào.'],
        ['Tài khoản E (cùng công ty, chưa tạo hệ số) tạo 1 hệ số.', 'Mở ô Người tạo.'], '—', ['Ô có thêm E ngay sau khi lưu.'], 282)

# ============================================================== XI. PHÂN QUYỀN
S11 = Sec(11)
S11.add('Màn không gắn quyền: ai cũng vào được', 'P0', [ACC_B, 'B không được gán vai trò hay quyền nào liên quan.'], ['Đăng nhập B.', MENU],
        '—', ['Menu hiện, vào màn được, thấy 12 hệ số của công ty Tân Phát.'], [287, 295])
S11.add('Xem chi tiết không cần quyền', 'P0', ACC_B, ['Đăng nhập B.', MENU, 'Bấm "Máy hàn".'], '—', ['Mở popup Xem bình thường.'], 288)
S11.add('Thêm mới không cần quyền', 'P0', ACC_B, ['Đăng nhập B.', MENU, 'Bấm Tạo mới, nhập đủ, Lưu.'], '—',
        ['Có nút Tạo mới, lưu thành công; hệ số ghi công ty Tân Phát.'], 289)
S11.add('Sửa, Xóa hệ số người khác tạo', 'P0', ACC_B, ['Đăng nhập B.', 'Sửa "Máy hàn" (do A tạo), Lưu.', 'Xóa "Kích nâng" (do A tạo).'],
        '—', ['Cả 2 thao tác đều được — không giới hạn theo người tạo.'], [290, 291])
S11.add('Xuất Excel và Lịch sử không cần quyền', 'P1', ACC_B, ['Đăng nhập B.', 'Xuất Excel.', 'Mở Lịch sử 1 dòng.'], '—',
        ['Đều dùng được.'], [293, 294])
S11.add('Phạm vi dữ liệu theo công ty', 'P0', [PRE_LIST, ACC_C], ['Đăng nhập C.', MENU], '—',
        ['C chỉ thấy 2 hệ số của Tân Phát Sài Gòn; không thấy 12 hệ số của Tân Phát.'], 299)
S11.add('Super admin cũng bó theo công ty', 'P1', 'Tài khoản Super admin thuộc công ty Tân Phát.', [MENU], '—',
        ['Chỉ thấy 12 hệ số của Tân Phát, không thấy hệ số công ty khác.'], 299)
S11.add('Tài khoản chưa gắn công ty', 'P1', ACC_D, ['Đăng nhập D.', MENU], '—', [EMPTY + '; ô Người tạo / Người cập nhật trống.'], 299)
S11.add('Mở hệ số công ty khác qua đường link cũ', 'P1', [ACC_C, 'C có đường link màn danh sách do A gửi.'],
        ['Đăng nhập C, mở link.'], '—', ['Chỉ thấy hệ số công ty mình; không xem / sửa / xóa được hệ số của Tân Phát.'], [296, 297])
S11.add('Đổi công ty giữa thao tác', 'P1', [ACC_B, 'Quản trị chuyển B sang công ty Tân Phát Sài Gòn khi B đang mở popup Sửa "Máy hàn".'],
        ['B bấm Lưu.'], '—', ['Thông báo ' + CONFLICT + ', không lưu (hệ số không còn thuộc công ty của B).'], 298)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'XÓA', S5),
    ('VI', 'LỊCH SỬ THAY ĐỔI', S6),
    ('VII', 'XEM CHI TIẾT HỆ SỐ CÔNG NGHỆ', S7),
    ('VIII', 'TÙY CHỈNH CỘT', S8),
    ('IX', 'XUẤT DANH SÁCH EXCEL', S9),
    ('X', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S10),
    ('XI', 'PHÂN QUYỀN', S11),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Hệ số công nghệ theo nhóm hàng hóa - Cập nhật ngày 06/11/2026',
                module_name='Hệ số công nghệ theo nhóm hàng hóa', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='danh_muc')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))
