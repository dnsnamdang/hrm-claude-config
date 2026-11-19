# -*- coding: utf-8 -*-
"""Testcase màn "Danh sách loại phiếu hạch toán" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan,
loai='danh_muc').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'danh_muc' — lý do từ code: màn danh sách danh mục cấu hình (105 loại phiếu cố định), không có số chứng từ, không có vòng đời.
Nhóm theo đúng tên + thứ tự chuẩn loại 'danh_muc' (check_tc.THU_TU), BỎ nhóm màn không có (kiểm code 06/11/2026: FE chỉ có 1 file
pages/admin/list-bill-accountings/index.vue, BE chỉ có 3 đường GET — danh sách / phân loại / dữ liệu xuất; không có Thêm mới, Chỉnh
sửa, Xóa, Khóa - Mở khóa, Lịch sử, Xem chi tiết, Import):
I Hiển thị · II Tìm kiếm & lọc (bộ lọc gọn 2 ô — không có Cài đặt bộ lọc) · III Tùy chỉnh cột · IV Xuất danh sách Excel ·
V Ràng buộc · VI Phân quyền (màn KHÔNG gắn quyền — viết theo thực tế: ai đăng nhập cũng dùng được, không giới hạn phạm vi).
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../benefit-rates/gen_testcase.py (06/11, qua check_tc 0 lỗi).
Nguồn hành vi (đọc 06/11/2026, nhánh develop): FE pages/admin/list-bill-accountings/index.vue, V2BaseSmartFilterPanel, V2BaseDataTable,
listExportFile; BE Modules/Finance ListBillAccounting* (Entity / Service / Resource / Controller).
Số liệu mẫu: dữ liệu THẬT 105 loại phiếu (giống nhau trên dev và máy phát triển, đếm 06/11/2026).
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
MENU = 'Vào phân hệ Bán hàng > nhóm "Quy chế - Thiết lập" > "Thiết lập" > bấm "Danh sách loại phiếu hạch toán".'
EMPTY = '"Không có dữ liệu phù hợp bộ lọc."'
TYPES = 'Đề nghị xuất, Đề nghị nhập, Xuất hàng, Nhập hàng, Thu, Chi, Phiếu kế toán, Dịch vụ, Khác'

ACC_A = 'Tài khoản A: kế toán công ty Tân Phát (Hà Nội).'
ACC_B = 'Tài khoản B: nhân viên kinh doanh công ty Tân Phát Sài Gòn, không được gán vai trò hay quyền nào.'
DATA = ('Danh mục có 105 loại phiếu cấu hình sẵn: Đề nghị xuất 20, Đề nghị nhập 23, Xuất hàng 21, Nhập hàng 24, Thu 5, Chi 8, Phiếu kế '
        'toán 1, Dịch vụ 2, Khác 1; 94 loại Hạch toán riêng, 11 loại không.')
PRE = ACC_A + '\n' + DATA
THU = 'Phân loại Thu có 5 loại: Phiếu thu, PT - Thu bán hàng, PT - Thu nhà cung cấp, PT - Thu khác, Phiếu báo có.'

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
     'Màn tra cứu danh mục loại phiếu hạch toán của hệ thống (chuyển từ Quản trị hệ thống › Cấu hình ERP của hệ thống cũ): tên loại '
     'phiếu, Phân loại và loại nào được hạch toán riêng. Màn CHỈ XEM — không thêm, sửa, xóa; có tìm kiếm, lọc theo Phân loại, sắp xếp, '
     'Tùy chỉnh cột, Xuất Excel.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Toàn bộ 105 loại phiếu cấu hình sẵn, không phân biệt công ty của người xem.\n'
     '- Phân loại gồm 9 giá trị: ' + TYPES + '.\n'
     '- Hạch toán riêng: Có (dấu tích) hoặc Không (ô trống).\n- Màn KHÔNG có trạng thái (không có Hoạt động / Khóa).'),
    ('3. Đối tượng bị ẩn / không tính', 'Không áp dụng: màn không ẩn loại phiếu nào — mọi người dùng thấy cùng 105 dòng; chỉ thu hẹp '
                                        'khi người dùng tự tìm kiếm / lọc.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Không áp dụng: màn không có ô lọc ngày (danh mục không có ngày tạo / ngày cập nhật).'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phân loại > Loại phiếu (một - nhiều).\n- Thứ tự mặc định giữ đúng thứ tự cấu hình của hệ thống cũ: dòng tổng (vd "Phiếu nhập '
     'hàng") đứng trước các dòng con cùng nhóm ("PNH - ...").'),
    ('6. Quy tắc cộng dồn / deduplicate', '- Không áp dụng cộng dồn.\n- Tên loại phiếu không trùng nhau trong danh mục.'),
    ('7. Phân quyền cấp',
     '- Màn KHÔNG gắn quyền riêng (giữ như hệ thống cũ): mọi người dùng đăng nhập đều thấy menu và dùng được mọi nút.\n'
     '- Không giới hạn phạm vi dữ liệu theo công ty / phòng ban.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là thứ tự dòng đầu – cuối của trang, N là tổng loại phiếu khớp bộ lọc (không lọc: 105).'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (công ty Tân Phát), B (công ty Tân Phát Sài Gòn, không có vai trò nào).\n'
     '- Lưu ý: sắp xếp cột Phân loại theo THỨ TỰ 9 phân loại (Đề nghị xuất trước, Khác sau), KHÔNG theo chữ cái.\n'
     '- Lưu ý: tìm kiếm không phân biệt dấu ("xuat thang" ra giống "xuất thẳng").\n'
     '- Lưu ý: chọn Phân loại là lọc ngay; ô tìm nhanh chỉ áp khi bấm Tìm kiếm / Enter.\n'
     '- Lưu ý: bộ lọc KHÔNG được ghi nhớ khi rời màn / tải lại trang.\n'
     '- Màn không có cột Hành động, không có nút Tạo mới, không mở được chi tiết từng dòng.'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', PRE, [MENU], '—',
       ['Mở màn "Danh sách loại phiếu hạch toán", không báo lỗi.', 'Bảng hiện 10 dòng đầu, "Hiển thị 1–10 / 105".',
        'Mặc định 10 dòng/trang.'], [1, 10, 16])
S1.add('Tiêu đề màn hình', 'P1', PRE, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng và tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Danh sách loại phiếu hạch toán".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE, [MENU, 'Quan sát khối bộ lọc và thanh công cụ của bảng.'], '—',
       ['Khối "Bộ lọc danh sách" một hàng: ô tìm nhanh (gợi ý "Tìm theo loại phiếu..."), ô Phân loại, Tìm kiếm, Làm mới.',
        'KHÔNG có nút Tìm kiếm nâng cao, Cài đặt bộ lọc.', 'Thanh công cụ: Xuất Excel, nút biểu tượng cột.',
        'KHÔNG có nút Tạo mới, Import, KHÔNG có cột Hành động.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 4 cột theo thứ tự: STT, Loại phiếu, Phân loại, Hạch toán riêng.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 4/4 cột".'], 5)
S1.add('Dữ liệu trên dòng đúng danh mục', 'P0', PRE, [MENU, 'Đối chiếu 3 dòng đầu.'], '—',
       ['Dòng 1 "Đề nghị xuất kho": Phân loại Đề nghị xuất, có dấu tích.', 'Dòng 2 "Đề nghị - Xuất bán hàng": Phân loại Đề nghị xuất, có dấu tích.',
        'Dòng 3 "Đề nghị - Xuất bán hàng - Xuất thẳng": Phân loại Đề nghị xuất, có dấu tích.'], 6)
S1.add('Hạch toán riêng = Không để trống', 'P0', PRE, [MENU, 'Đổi Số dòng/trang = 50, quan sát dòng "Đề nghị nhập kho" (STT 21) và '
                                                       '"Phiếu xuất hàng" (STT 44).'], '—',
       ['Cột Hạch toán riêng của 2 dòng này để TRỐNG (không hiện số 0).', 'Các dòng còn lại trong trang có dấu tích màu xanh, rê chuột '
        'hiện "Có".'], 6)
S1.add('Màn không có trạng thái bản ghi', 'P2', PRE, [MENU, 'Quan sát các cột và khối lọc.'], '—',
       ['Không có cột / ô lọc Trạng thái; mọi loại phiếu đều hiện.'], 7)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện ' + EMPTY + '; không báo lỗi.'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 100.'], 'Số dòng/trang: 100',
       ['Tự về trang 1, "Hiển thị 1–100 / 105"; còn 2 trang.', 'Ô có các lựa chọn 5, 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 105", dòng 11 "Đề nghị - Xuất điều chuyển kho chi nhánh - Xuất thẳng".', 'Bước 3: "Hiển thị 1–10 / 105".'],
       12)
S1.add('Trang đầu / trang cuối', 'P1', PRE, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 11, "Hiển thị 101–105 / 105": Phiếu báo nợ, Phiếu kế toán, Bán dịch vụ, Mua dịch vụ, Khác thu, chi, nhập, xuất.',
        'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 11 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ, không bấm được.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE, [MENU, 'Sang trang 2.', 'Sang trang 11.'], '—',
       ['Trang 2 đánh số 11–20; trang 11 đánh số 101–105.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE, [MENU, 'Sang trang 3.', 'Chọn Phân loại = Chi.'], 'Phân loại: Chi',
       ['Tự nạp lại ở trang 1; "Hiển thị 1–8 / 8" (Phiếu chi, 6 dòng "PC - ...", Phiếu báo nợ).'], 17)
S1.add('Thứ tự mặc định', 'P0', PRE, [MENU, 'Quan sát thứ tự khi mới vào.'], '—',
       ['Giữ thứ tự cấu hình: "Đề nghị xuất kho" dòng 1, "Khác thu, chi, nhập, xuất" dòng cuối trang 11.',
        'Không cột nào có mũi tên sắp xếp đang bật.'], 19)
S1.add('Sắp xếp tăng dần theo Loại phiếu', 'P0', PRE, [MENU, 'Bấm tiêu đề cột Loại phiếu.'], '—',
       ['Xếp theo chữ cái, không phân biệt hoa / thường: "Bán dịch vụ" trên cùng, kế đến các dòng "Đề nghị - Nhập ...".',
        'Mũi tên lên; về trang 1.'], 20)
S1.add('Sắp xếp giảm dần theo Loại phiếu', 'P0', PRE, [MENU, 'Bấm tiêu đề cột Loại phiếu 2 lần.'], '—',
       ['Dòng 1 "PXH- Xuất điều chuyển kho nội bộ - Xuất thẳng"; mũi tên xuống.'], 21)
S1.add('Sắp xếp Phân loại theo thứ tự phân loại', 'P0', PRE, [MENU, 'Bấm tiêu đề cột Phân loại.', 'Bấm lần nữa.'], '—',
       ['Lần 1 (tăng): 20 dòng Đề nghị xuất trước, đúng thứ tự cấu hình.',
        'Lần 2 (giảm): "Khác thu, chi, nhập, xuất" (Khác), "Bán dịch vụ", "Mua dịch vụ" (Dịch vụ), "Phiếu kế toán", rồi các dòng Chi.',
        'Lưu ý: KHÔNG xếp theo chữ cái của tên phân loại.'], [21, 22])
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE, [MENU, 'Bấm tiêu đề STT và Hạch toán riêng.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE, [MENU, 'Bấm Loại phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự chữ cái của trang 1; mũi tên vẫn bật.', 'Cột không nhảy bề rộng khi sắp xếp.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE, [MENU, 'Sang trang 5.', 'Bấm tiêu đề Phân loại.'], '—', ['Về trang 1.'], 25)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo tên chính xác', 'P0', PRE, [MENU, 'Nhập "Phiếu kế toán", bấm Tìm kiếm.'], 'Ô tìm nhanh: Phiếu kế toán',
       ['Chỉ còn 1 dòng "Phiếu kế toán" (Phân loại Phiếu kế toán), "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần tên', 'P0', PRE, [MENU, 'Nhập "kiểm kê", bấm Tìm kiếm.'], 'Ô tìm nhanh: kiểm kê',
       ['Ra 2 dòng: PXH - Xuất điều chỉnh kiểm kê, PNH - Nhập điều chỉnh kiểm kê.'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE, [MENU, 'Nhập "PHIẾU THU", bấm Tìm kiếm.'], 'Ô tìm nhanh: PHIẾU THU',
       ['Ra 1 dòng "Phiếu thu".'], 28)
S2.add('Có dấu / không dấu', 'P1', PRE, [MENU, 'Nhập "xuat thang", bấm Tìm kiếm.', 'Nhập "xuất thẳng", bấm Tìm kiếm.'], '—',
       ['Cả 2 lần đều ra 16 dòng (tìm không phân biệt dấu), gồm cả dòng "Đề nghị - Xuất khác - Xuât thẳng".'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE, [MENU, 'Nhập "Hóa đơn đỏ", bấm Tìm kiếm.'], '—', [EMPTY], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.', 'Nhập "_", bấm Tìm kiếm.'], '—',
       ['Không lỗi; cả 3 lần đều ' + EMPTY + ' (% và _ được tìm đúng ký tự, không hiểu là "mọi ký tự").'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE, [MENU, 'Nhập "   kiểm kê   ", bấm Tìm kiếm.'], '—',
       ['Ra 2 dòng như tìm "kiểm kê" (bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Từ khóa rất dài', 'P2', PRE, [MENU, 'Dán chuỗi 300 ký tự vào ô tìm nhanh, bấm Tìm kiếm.'], 'Chuỗi 300 ký tự "a"',
       ['Ô nhận đủ (không giới hạn số ký tự), không lỗi, ' + EMPTY + '.'], 33)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "kiểm kê", bảng còn 2 dòng.', ['Bấm × trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 1 ô trống nhưng danh sách CHƯA đổi; sau bước 2 hiện lại đủ 105 loại phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE, [MENU, 'Nhập "mượn", nhấn Enter.', 'Làm mới, nhập lại "mượn", bấm Tìm kiếm.'],
       '—', ['Cả 2 cách đều ra 10 dòng có chữ "mượn"; về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', PRE, [MENU, 'Quan sát ô tìm nhanh và ô Phân loại.'], '—',
       ['Ô tìm nhanh trống; ô Phân loại trống (chữ gợi ý "Phân loại").', 'Đủ 105 loại phiếu.'], 36)
S2.add('Lựa chọn của ô Phân loại', 'P1', PRE, [MENU, 'Mở ô Phân loại.'], '—', ['Có đúng 9 lựa chọn theo thứ tự: ' + TYPES + '.'], 37)
S2.add('Lọc theo Phân loại', 'P0', [PRE, THU], [MENU, 'Chọn Phân loại = Thu.'], 'Phân loại: Thu',
       ['Lọc ngay, không cần bấm Tìm kiếm; "Hiển thị 1–5 / 5".', 'Đúng 5 dòng: Phiếu thu, PT - Thu bán hàng, PT - Thu nhà cung cấp, PT - '
        'Thu khác, Phiếu báo có.'], 37)
S2.add('Lọc từng Phân loại ra đúng số lượng', 'P1', PRE, [MENU, 'Lần lượt chọn từng giá trị ô Phân loại.'], '—',
       ['Đề nghị xuất 20, Đề nghị nhập 23, Xuất hàng 21, Nhập hàng 24, Thu 5, Chi 8, Phiếu kế toán 1, Dịch vụ 2, Khác 1 (cộng 105).'], 37)
S2.add('Bỏ chọn Phân loại bằng ×', 'P1', 'Đang lọc Phân loại = Thu.', ['Bấm × trong ô Phân loại.'], '—',
       ['Bỏ lọc và nạp lại ngay, hiện đủ 105 loại phiếu.'], [37, 44])
S2.add('Kết hợp tìm kiếm với Phân loại', 'P0', [PRE, THU], [MENU, 'Chọn Phân loại = Thu.', 'Nhập "PT", bấm Tìm kiếm.'], '—',
       ['Còn 3 dòng: PT - Thu bán hàng, PT - Thu nhà cung cấp, PT - Thu khác.'], [38, 39])
S2.add('Kết hợp ra nhiều dòng', 'P1', PRE, [MENU, 'Nhập "nhập thẳng", bấm Tìm kiếm.', 'Chọn Phân loại = Nhập hàng.'], '—',
       ['Bước 1: 20 dòng (cả Đề nghị nhập lẫn Nhập hàng).', 'Bước 2: còn 10 dòng "PNH - ... - Nhập thẳng".'], [38, 39])
S2.add('Không có kết quả khi kết hợp', 'P1', PRE, [MENU, 'Chọn Phân loại = Chi.', 'Nhập "kiểm kê", bấm Tìm kiếm.'], '—', [EMPTY], 40)
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE, [MENU, 'Chọn Phân loại = Nhập hàng.', 'Bấm trang 3.'], '—',
       ['Bước 1: "Hiển thị 1–10 / 24", 3 trang.', 'Bước 2: "Hiển thị 21–24 / 24", STT 21–24.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', [PRE, THU, 'Đang lọc Phân loại = Thu.'], ['Bấm tiêu đề Loại phiếu.'], '—',
       ['Chỉ 5 dòng đang lọc được sắp: Phiếu báo có, Phiếu thu, PT - Thu bán hàng, PT - Thu khác, PT - Thu nhà cung cấp.',
        'Bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "PT", lọc Phân loại = Thu, sắp theo Loại phiếu, ở trang 1.', ['Bấm Làm mới.'],
       '—', ['Ô tìm nhanh và ô Phân loại về trống, bỏ sắp xếp, nạp lại trang 1, "Hiển thị 1–10 / 105".'], 44)
S2.add('Chữ đang gõ được áp khi đổi Phân loại', 'P2', PRE, [MENU, 'Gõ "PT" (không bấm Tìm kiếm).', 'Chọn Phân loại = Thu.'], '—',
       ['Kết quả 3 dòng "PT - ..." — chữ đang gõ cũng được áp cùng Phân loại.'], 39)
S2.add('Chuyển màn rồi quay lại', 'P1', 'Đang lọc Phân loại = Chi, tìm "PC".',
       ['Vào màn khác trong menu Bán hàng.', 'Quay lại màn Danh sách loại phiếu hạch toán.'], '—',
       ['Ô tìm nhanh, ô Phân loại về trống, đủ 105 loại phiếu (màn không ghi nhớ bộ lọc).'], 45)
S2.add('Tải lại trang (F5)', 'P1', 'Đang lọc Phân loại = Chi.', ['Nhấn F5.'], '—', ['Bộ lọc về trống, đủ 105 loại phiếu.'], 46)
S2.add('Mở màn ở tab mới', 'P2', 'Đang lọc Phân loại = Chi ở tab 1.', ['Mở màn ở tab trình duyệt mới.'], '—',
       ['Tab mới bộ lọc trống, đủ 105 loại phiếu; tab 1 giữ nguyên.'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', [ACC_A, ACC_B], ['A lọc Phân loại = Chi, đăng xuất.', 'Đăng nhập B, vào màn.'],
       '—', ['B thấy bộ lọc trống và đủ 105 loại phiếu.'], 48)

# ============================================================== III. TÙY CHỈNH CỘT
S3 = Sec(3)
S3.add('Mở cửa sổ Tuỳ chỉnh cột', 'P0', PRE, [MENU, 'Bấm nút biểu tượng cột cạnh Xuất Excel.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" liệt kê 4 cột theo thứ tự bảng: STT, Loại phiếu, Phân loại, Hạch toán riêng; "Đang chọn 4/4 cột".',
        'Có nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng.'], [198, 199, 200])
S3.add('Ẩn cột', 'P0', PRE, ['Mở Tuỳ chỉnh cột, bỏ tích Hạch toán riêng, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; bảng còn 3 cột STT, Loại phiếu, Phân loại.'], 202)
S3.add('Hiện lại cột đã ẩn', 'P1', 'Đã ẩn Hạch toán riêng.', ['Mở Tuỳ chỉnh cột, bấm Chọn tất cả, Lưu.'], '—',
       ['Bảng hiện lại đủ 4 cột.'], 201)
S3.add('Cột bắt buộc không ẩn được', 'P0', PRE, ['Mở Tuỳ chỉnh cột.', 'Bấm Bỏ chọn hết.'], '—',
       ['STT, Loại phiếu có biểu tượng ổ khóa, ô tích mờ, vẫn tích sau Bỏ chọn hết; "Đang chọn 2/4 cột".'], [203, 205])
S3.add('Kéo thả đổi thứ tự', 'P1', PRE, ['Mở Tuỳ chỉnh cột, kéo Hạch toán riêng lên trước Phân loại, Lưu.'], '—',
       ['Bảng hiện Hạch toán riêng trước Phân loại; STT, Loại phiếu không kéo được.'], [204, 205])
S3.add('Lưu cấu hình', 'P0', PRE, ['Mở Tuỳ chỉnh cột, bỏ tích Phân loại, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công", cửa sổ đóng, bảng vẽ lại ngay không cần tải lại trang.'], 206)
S3.add('Đóng không lưu', 'P1', PRE, ['Mở Tuỳ chỉnh cột, bỏ tích Phân loại.', 'Bấm Đóng (lần 2: (x)).'], '—',
       ['Không hỏi; bảng giữ nguyên cột Phân loại.'], 207)
S3.add('Ghi nhớ sau tải lại và đăng nhập lại', 'P0', 'A đã ẩn cột Hạch toán riêng.', ['Nhấn F5.', 'Đăng xuất, đăng nhập lại A ở trình duyệt '
                                                                                    'khác.'],
       '—', ['Cả 2 lần cột Hạch toán riêng vẫn ẩn.'], 208)
S3.add('Cấu hình theo tài khoản', 'P1', 'A đã ẩn cột Hạch toán riêng.', ['Đăng nhập B, vào màn.'], '—', ['B vẫn thấy đủ 4 cột.'], 209)
S3.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P1', 'Đang lọc Phân loại = Nhập hàng, ở trang 2.', ['Ẩn cột Phân loại, Lưu.'], '—',
       ['Tổng "/ 24" và bộ lọc giữ nguyên; dữ liệu không đổi.'], [210, 211])

# ============================================================== IV. XUẤT DANH SÁCH EXCEL
S4 = Sec(4)
S4.add('Mở cửa sổ chọn trường', 'P0', PRE, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất file" có 3 trường: Loại phiếu, Phân loại, Hạch toán riêng.',
        'Có Chọn tất cả, Bỏ chọn hết, "Đang chọn 3/3 trường", Xuất file, Đóng.'], [212, 213])
S4.add('Trường chọn mặc định theo cột đang hiện', 'P1', 'A đã ẩn cột Hạch toán riêng.', ['Bấm Xuất Excel.'], '—',
       ['Tích sẵn Loại phiếu, Phân loại; Hạch toán riêng không tích ("Đang chọn 2/3 trường").'], 214)
S4.add('Xuất với trường mặc định', 'P0', PRE, ['Bấm Xuất Excel.', 'Bấm Xuất file.'], '—',
       ['Tải file danh_sach_loai_phieu_hach_toan.xlsx, báo "Xuất Excel thành công.".',
        'File có STT + 3 cột, đủ 105 dòng (cả 11 trang, không chỉ trang đang xem).'], [215, 221, 223, 227])
S4.add('Xuất tất cả / một số trường', 'P1', PRE, ['Bấm Xuất Excel, Bỏ chọn hết, tích Loại phiếu, Xuất file.',
                                                    'Lần 2: bấm Chọn tất cả, Xuất file.'], '—',
       ['Lần 1: file chỉ có STT, Loại phiếu.', 'Lần 2: file có STT và đủ 3 cột.'], [216, 217])
S4.add('Không chọn trường nào', 'P1', PRE, ['Bấm Xuất Excel, Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S4.add('Xuất theo tìm kiếm', 'P0', PRE, ['Tìm "kiểm kê".', 'Xuất Excel đủ trường.'], '—',
       ['File có 2 dòng: PXH - Xuất điều chỉnh kiểm kê, PNH - Nhập điều chỉnh kiểm kê.'], 219)
S4.add('Xuất theo bộ lọc', 'P0', [PRE, THU], ['Chọn Phân loại = Thu.', 'Xuất Excel đủ trường.'], '—',
       ['File có 5 dòng: Phiếu thu, PT - Thu bán hàng, PT - Thu nhà cung cấp, PT - Thu khác, Phiếu báo có.'], 220)
S4.add('Xuất theo thứ tự sắp xếp', 'P1', 'Đang sắp giảm dần theo Phân loại.', ['Xuất Excel đủ trường.'], '—',
       ['Dòng 1 của file "Khác thu, chi, nhập, xuất" — đúng thứ tự đang xem trên bảng.'], 221)
S4.add('Danh sách rỗng', 'P1', PRE, ['Tìm "ZZZ", bấm Xuất Excel, Xuất file.'], '—',
       ['Thông báo "Không có dữ liệu để xuất", KHÔNG tải file.'], 222)
S4.add('Định dạng và nội dung file', 'P0', PRE, ['Xuất đủ trường, mở file.'], '—',
       ['Letterhead công ty của người xuất trên cùng, tiêu đề "DANH SÁCH LOẠI PHIẾU HẠCH TOÁN", trang tính "Loai phieu hach toan".',
        'Khối ký "Ngày ..., tháng ..., năm ..." và "Người lập" cuối bảng.', 'Hàng tiêu đề cột KHÔNG có nút lọc.',
        'Tên cột STT, Loại phiếu, Phân loại, Hạch toán riêng.'], [224, 225])
S4.add('Thứ tự cột theo kéo thả', 'P1', PRE, ['Bấm Xuất Excel, kéo Phân loại lên đầu, Xuất file.'], '—',
       ['File: STT, Phân loại, Loại phiếu, Hạch toán riêng.'], 226)
S4.add('Dữ liệu khớp màn hình', 'P0', PRE, ['Xuất đủ trường, đối chiếu dòng "Phiếu thu" và "PT - Thu bán hàng".'], '—',
       ['"Phiếu thu": Phân loại Thu, cột Hạch toán riêng TRỐNG.', '"PT - Thu bán hàng": Phân loại Thu, Hạch toán riêng ghi chữ "Có".'], [228, 229])
S4.add('Tiếng Việt và ký tự đặc biệt', 'P2', PRE, ['Xuất Excel, mở file.'], '—',
       ['Tên "Khác thu, chi, nhập, xuất", "Đề nghị - Xuất điều chuyển kho chi nhánh - Xuất thẳng" hiện đúng dấu, dấu phẩy, gạch nối.'],
       230)
S4.add('Bấm Xuất file liên tục', 'P2', PRE, ['Bấm Xuất Excel, bấm Xuất file 2 lần thật nhanh.'], '—',
       ['Nút khóa trong lúc xuất; chỉ tải 1 file.'], 215)

# ============================================================== V. RÀNG BUỘC
S5 = Sec(5)
S5.add('Mỗi loại phiếu đúng một Phân loại', 'P0', PRE, [MENU, 'Đổi Số dòng/trang = 100, đối chiếu cột Phân loại các dòng "PXH - ...", '
                                                       '"PNH - ...", "PT - ...", "PC - ...".'], '—',
       ['"PXH - ..." đều là Xuất hàng; "PNH - ..." đều là Nhập hàng; "PT - ..." là Thu; "PC - ..." là Chi.'], 283)
S5.add('Không có loại phiếu thiếu Phân loại', 'P1', PRE, [MENU, 'Lần lượt lọc 9 Phân loại, cộng số dòng.'], '—',
       ['Tổng 9 lần lọc = 105 = tổng không lọc: không dòng nào thiếu hoặc sai Phân loại.'], 285)
S5.add('Không có loại phiếu trùng tên', 'P1', PRE, [MENU, 'Sắp xếp theo Loại phiếu, Số dòng/trang = 100, dò các dòng liền nhau.'], '—',
       ['Không có 2 dòng trùng tên.'], 286)
S5.add('Khớp danh mục của hệ thống cũ', 'P2', [PRE, 'Có tài khoản trên hệ thống cũ.'],
       ['Mở màn Danh sách loại phiếu hạch toán ở hệ thống cũ (Quản trị hệ thống › Cấu hình).', 'So với màn ở phần mềm mới.'], '—',
       ['Cùng 105 dòng, cùng thứ tự mặc định, cùng Phân loại và dấu Hạch toán riêng.'], 283)

# ============================================================== VI. PHÂN QUYỀN
S6 = Sec(6)
S6.add('Màn không gắn quyền: ai cũng vào được', 'P0', ACC_B, ['Đăng nhập B.', MENU], '—',
       ['Menu hiện, vào màn được, thấy đủ 105 loại phiếu.'], [287, 295])
S6.add('Không có nút nào bị ẩn theo quyền', 'P1', ACC_B, ['Đăng nhập B.', MENU], '—',
       ['B thấy đủ ô tìm nhanh, ô Phân loại, Tìm kiếm, Làm mới, Xuất Excel, nút biểu tượng cột như A.'], 295)
S6.add('Xuất Excel không cần quyền', 'P0', ACC_B, ['Đăng nhập B.', 'Bấm Xuất Excel, Xuất file.'], '—',
       ['Tải file thành công với đủ 105 dòng; letterhead là công ty Tân Phát Sài Gòn của B.'], 293)
S6.add('Phạm vi dữ liệu không theo công ty', 'P0', [ACC_A, ACC_B], ['Đăng nhập A, ghi tổng số.', 'Đăng nhập B, ghi tổng số.'], '—',
       ['Cả 2 đều "Hiển thị 1–10 / 105" với cùng dữ liệu (danh mục dùng chung toàn hệ thống).'], 299)
S6.add('Mở màn qua đường link được gửi', 'P1', [ACC_B, 'B nhận đường link màn từ A.'], ['Đăng nhập B, mở đường link.'], '—',
       ['Mở được màn, thấy đủ 105 loại phiếu (không có quyền nào để thiếu).'], [296, 297])
S6.add('Đổi công ty giữa thao tác', 'P2', [ACC_B, 'Quản trị chuyển B sang công ty Tân Phát trong lúc B đang ở trang 3.'],
       ['B bấm sang trang 4.'], '—', ['Vẫn xem bình thường, dữ liệu không đổi (màn không phụ thuộc công ty).'], 298)
S6.add('Super admin thấy như mọi người', 'P2', 'Tài khoản Super admin.', [MENU], '—',
       ['Thấy đúng 105 loại phiếu như A, B; không có thêm nút Tạo mới / Sửa / Xóa.'], 299)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'TÙY CHỈNH CỘT', S3),
    ('IV', 'XUẤT DANH SÁCH EXCEL', S4),
    ('V', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S5),
    ('VI', 'PHÂN QUYỀN', S6),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Danh sách loại phiếu hạch toán - Cập nhật ngày 06/11/2026',
                module_name='Danh sách loại phiếu hạch toán', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='danh_muc')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))
