# -*- coding: utf-8 -*-
"""Testcase Redmine #11949 — YC hỏi giá: popup Chọn hàng hoá + tab Chọn từ kho hàng tạm (tìm theo Model, bộ lọc nâng cao,
cột Ảnh / Trạng thái / Giá nhập / Giá bán, Phóng to). Khuôn chuẩn 03/11/2026 (tc_chuan.build_chuan, loai='phieu').
Nguồn hành vi (đọc 18/11/2026, develop): FE pages/assign/quotations/components/QuotationProductSearchModal.vue,
components/product/picker/ProductPickerPanel.vue + ProductPickerAdvancedFilters.vue; BE Assign ProductProjectController (scope ychg).
Chạy: python gen_testcase.py -> testcase.xlsx rồi python check_tc.py testcase.xlsx phieu.
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
from tc_chuan import build_chuan  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Bán hàng > nhóm "Yêu cầu" > "Hàng hóa" > bấm "YC hỏi giá" > bấm "Tạo mới".'
OPEN_PICK = 'Bấm nút "Chọn hàng hóa" ở bảng hàng hóa của phiếu.'
OPEN_TMP = 'Bấm nút "Thêm hàng tạm".'
TAB_TMP = 'Bấm thẻ "Chọn từ kho hàng tạm (Tái sử dụng)".'
EMPTY = '"Không có hàng tạm phù hợp."'
COST = '"Xem giá vốn hàng hoá"'

ACC_A = ('Tài khoản A: nhân viên kinh doanh, CÓ quyền %s, xem được dự án DA-01 và DA-02.' % COST)
ACC_B = ('Tài khoản B: nhân viên kinh doanh, KHÔNG có quyền %s, xem được dự án DA-01.' % COST)
DATA = ('Kho hàng tạm có:\n'
        '- HT-001 "Máy nén khí 5HP", Model MNK-5, thương hiệu PUMA, nguồn Báo giá BG-01 (Trúng thầu, do A lập, VNĐ, '
        'Giá nhập 20,000,000, Giá bán 25,000,000), dự án DA-01, hàng độc lập.\n'
        '- HT-002 "Bộ nâng cầu 2 trụ" (hàng cha có 2 hàng con), nguồn BOM BOM-01, dự án DA-01, Giá nhập 30,000,000, Giá bán 38,000,000.\n'
        '- HT-003 "Máy rửa xe", Model RX-200, nguồn Báo giá BG-02 (Đang báo giá, do A lập, USD), dự án DA-02.\n'
        '- HT-004 "Bơm mỡ", nguồn Báo giá BG-03 (Trúng thầu, do C lập), dự án DA-01.')


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

    def add(self, func, prio, pre, steps, td, exp):
        self.append(T(len(self) + 1, func, prio, pre, steps, td, exp))


TMP_STEPS = [MENU, OPEN_TMP, TAB_TMP]
PICK_STEPS = [MENU, OPEN_PICK]

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Ở màn tạo Yêu cầu hỏi giá (Bán hàng > Yêu cầu > Hàng hóa > YC hỏi giá), nâng cấp 2 popup chọn hàng:\n'
     '- Popup "Chọn hàng hóa": làm giống popup chọn hàng ở màn Báo giá hãng (cây catalog, Tìm kiếm nâng cao, cấu hình cột), thêm 2 cột '
     '"Trạng thái HH công ty quản lý", "Trạng thái" (trong bảng, bộ lọc, cấu hình cột) và cột "Giá nhập" cho người có quyền xem giá vốn.\n'
     '- Thẻ "Chọn từ kho hàng tạm (Tái sử dụng)" trong popup "Thêm hàng tạm": tìm nhanh thêm theo Model, 7 ô lọc nâng cao, cột STT, '
     'Hình ảnh (bấm phóng to), Trạng thái, Giá nhập (Mã tiền tệ), Giá bán (Mã tiền tệ), nút Phóng to toàn màn hình.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Thẻ kho hàng tạm: chỉ dòng hàng tạm CHA của BOM giải pháp hoặc Báo giá, CHƯA thành hàng hoá chính thức, thuộc các dự án tài '
     'khoản được xem.\n'
     '- Hàng tạm vừa thêm ngay trong phiếu đang lập (chưa lưu) hiện ở đầu bảng với nhãn Nguồn "Trong phiếu".\n'
     '- Popup Chọn hàng hóa: hàng hoá đang ở trạng thái Đang nhập thông tin, Đang kinh doanh, Hàng tạm, Hàng tạm không duyệt.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Hàng tạm đã được tạo mã hàng hoá chính thức.\n'
     '- Dòng hàng con (chỉ chọn qua dòng cha; chọn cha thì mang theo con).\n'
     '- Hàng tạm thuộc dự án tài khoản không được xem.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Không áp dụng — 2 popup không có ô lọc thời gian.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Dự án > BOM giải pháp / Báo giá > dòng hàng tạm cha > hàng con ghép bộ.\n'
     '- Popup Chọn hàng hóa: cây catalog kinh doanh của công ty ở cột trái.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Một hàng tạm vừa nằm trong phiếu vừa có trong kho chỉ hiện 1 dòng (dòng "Trong phiếu").\n'
     '- Trạng thái cấu trúc: "Hàng độc lập" = dòng không có hàng con; "Hàng cha – ghép bộ" = dòng có ít nhất 1 hàng con.'),
    ('7. Phân quyền cấp',
     '- Xem giá vốn hàng hoá: hiện cột "Giá nhập" ở popup Chọn hàng hóa; là 1 trong các điều kiện để thấy số ở cột "Giá nhập (Mã tiền '
     'tệ)" của thẻ kho hàng tạm.\n'
     '- Không cần quyền riêng để mở 2 popup (đi theo quyền tạo Yêu cầu hỏi giá).'),
    ('8. Cách tính các ô thống kê',
     '- Cột STT = nối tiếp qua các trang: trang 2, 10 dòng/trang thì bắt đầu từ 11.\n'
     '- Giá nhập (Mã tiền tệ): chỉ hiện số khi CẢ 3 điều kiện đúng: có quyền xem giá vốn; dòng sinh từ Báo giá trạng thái Trúng thầu; '
     'Báo giá đó do chính tài khoản đang đăng nhập lập. Còn lại hiện "—".\n'
     '- Giá bán (Mã tiền tệ): ai cũng xem được. Dòng từ Báo giá có mã tiền tệ (vd "25,000,000 VNĐ"); dòng từ BOM không có mã tiền tệ.\n'
     '- Popup Chọn hàng hóa: dòng "N hàng hoá thoả bộ lọc" = tổng số hàng khớp bộ lọc.'),
    ('9. Ghi chú đọc bảng',
     '- Số định dạng quốc tế: dấu phẩy ngăn nghìn, dấu chấm thập phân (25,000,000).\n'
     '- Thẻ kho hàng tạm chọn 1 dòng (nút tròn); nút "Dùng hàng này" chỉ bấm được khi dòng đang chọn còn hiện trong bảng. Bấm thì điền '
     'sẵn Tên, ĐVT, Thương hiệu, Xuất xứ, Model, Thông số kỹ thuật, % VAT, ảnh rồi chuyển sang thẻ nhập.\n'
     '- Số dòng/trang của popup: 10 / 20 / 50 / 100, mặc định 10.\n'
     '- Lưu ý: QA từng ghi "Bỏ giúp chị yêu cầu này" cho cột Giá nhập ở popup Chọn hàng hóa; bản hiện tại VẪN có cột này cho người có '
     'quyền xem giá vốn (các case TC_03.003, TC_05.001, TC_05.002). Nếu đã chốt bỏ thì đánh các case đó là không áp dụng.'),
]

# ---------------- I. HIỂN THỊ ----------------
S1 = Sec(1)
S1.add('Mở popup Chọn hàng hóa từ màn tạo YC hỏi giá', 'P0', ACC_A, PICK_STEPS, '—',
       ['Mở popup tiêu đề "Chọn hàng hoá".',
        'Cột trái là cây catalog; cột phải có ô tìm "Tìm theo mã, tên hàng hoá, model, barcode, mã đặt hàng", công tắc "Còn tồn", '
        '"Gồm hàng ngoài catalog", nút "Tìm kiếm nâng cao", "Làm mới", nút cấu hình cột.',
        'Bố cục giống popup chọn hàng ở màn Báo giá hãng.'])
S1.add('Popup Chọn hàng hóa hiện 2 cột trạng thái', 'P0', ACC_A + '\nHàng hoá X: Trạng thái HH công ty quản lý "Đang kinh doanh", '
       'Trạng thái tại công ty "Đang nhập thông tin".', PICK_STEPS + ['Tìm hàng X.'], 'Từ khoá: mã hàng X',
       ['Có 2 cột "Trạng thái HH công ty quản lý" và "Trạng thái" đứng ngay sau cột "Tồn bán được".',
        'Dòng X: cột 1 hiện nhãn "Đang kinh doanh", cột 2 hiện "Đang nhập thông tin", mỗi nhãn có màu riêng.',
        'Chữ và màu khớp màn Kho dữ liệu hàng hóa với cùng hàng X.'])
S1.add('Mở thẻ Chọn từ kho hàng tạm', 'P0', [ACC_A, DATA], TMP_STEPS, '—',
       ['Có ô tìm "Tìm theo mã / tên / model hàng tạm".',
        'Có 7 ô lọc theo thứ tự: Dự án, Báo giá nguồn, BOM nguồn, Nguồn, Trạng thái cấu trúc, Thương hiệu, Model.',
        'Bảng có cột theo thứ tự: chọn | STT | Mã hàng | Hình ảnh | Tên hàng | Model | Thương hiệu | Xuất xứ | ĐVT | Nguồn | Dự án | '
        'Trạng thái | Giá nhập (Mã tiền tệ) | Giá bán (Mã tiền tệ).',
        'Chân popup có nút "Dùng hàng này" (chưa bấm được) và "Đóng".'])
S1.add('Phóng to / thu nhỏ toàn màn hình', 'P1', ACC_A, TMP_STEPS + ['Bấm nút "Phóng to toàn màn hình" góc trên popup.',
       'Bấm lại nút (lúc này tên là "Thu nhỏ").'], '—',
       ['Bước 4: popup phủ kín màn hình, bảng rộng ra, không mất ô lọc / dòng đang chọn.',
        'Bước 5: popup về kích thước cũ.',
        'Đóng popup rồi mở lại: popup mở ở kích thước thường.'])
S1.add('Cột STT nối tiếp qua các trang', 'P1', [ACC_A, 'Kho hàng tạm có 25 dòng tài khoản A xem được.'],
       TMP_STEPS + ['Bấm sang trang 2.'], 'Số dòng/trang: 10',
       ['Trang 1 STT 1–10; trang 2 STT bắt đầu từ 11 đến 20.'])
S1.add('Cột Hình ảnh — bấm phóng to', 'P0', [ACC_A, 'HT-001 có 3 ảnh; HT-003 không có ảnh.'],
       TMP_STEPS + ['Bấm ảnh nhỏ ở dòng HT-001.', 'Xem ô Hình ảnh của HT-003.'], '—',
       ['Cột Hình ảnh đứng ngay sau cột Mã hàng.',
        'Bước 4: mở ảnh phóng to, xem được cả 3 ảnh; bấm ảnh KHÔNG làm đổi dòng đang chọn.',
        'Bước 5: hiện "—".'])
S1.add('Cột Nguồn hiện đúng nhãn', 'P1', [ACC_A, DATA, 'Trong phiếu đang lập đã thêm hàng tạm mới HT-NEW (chưa lưu phiếu).'],
       [MENU, 'Thêm hàng tạm HT-NEW bằng thẻ Thêm mới.', OPEN_TMP, TAB_TMP], '—',
       ['HT-NEW nằm đầu bảng, Nguồn "Trong phiếu" (xanh lá).',
        'HT-001 Nguồn "Báo giá"; HT-002 Nguồn "BOM".'])
S1.add('Cột Trạng thái hiện trạng thái đồng bộ', 'P1', [ACC_A, 'HT-001 chưa gửi tạo mã; HT-003 đã gửi tạo mã, đang chờ.'],
       TMP_STEPS, '—',
       ['HT-001 hiện nhãn "Chưa đồng bộ" (xám).', 'HT-003 hiện nhãn "Đang đồng bộ" (xanh dương).'])
S1.add('Phân trang thẻ kho hàng tạm', 'P1', [ACC_A, 'Kho có 25 dòng.'],
       TMP_STEPS + ['Đổi số dòng/trang sang 20.', 'Bấm trang sau, trang trước.'], 'Số dòng/trang: 10 > 20',
       ['Lựa chọn số dòng/trang: 10, 20, 50, 100; mặc định 10.',
        'Đổi sang 20: về trang 1, hiện 20 dòng.',
        'Tổng ghi đúng 25 hàng tạm.'])
S1.add('Không có dữ liệu phù hợp', 'P1', ACC_A, TMP_STEPS + ['Gõ từ khoá không tồn tại.'], 'Từ khoá: zzzxxx',
       ['Bảng hiện %s' % EMPTY, 'Nút "Dùng hàng này" không bấm được.'])
S1.add('Bấm Đóng', 'P2', ACC_A, TMP_STEPS + ['Bấm "Đóng".'], '—',
       ['Popup đóng, quay về màn tạo YC hỏi giá, phiếu không thêm dòng nào.'])

# ---------------- II. TÌM KIẾM & LỌC ----------------
S2 = Sec(2)
S2.add('Tìm nhanh theo Model', 'P0', [ACC_A, DATA], TMP_STEPS + ['Gõ "MNK-5" vào ô tìm.'], 'Từ khoá: MNK-5',
       ['Bảng chỉ còn HT-001 (Model MNK-5).', 'Bảng tự lọc sau khi ngừng gõ, không cần bấm Enter; về trang 1.'])
S2.add('Tìm nhanh theo Mã và theo Tên', 'P0', [ACC_A, DATA], TMP_STEPS + ['Gõ "HT-002".', 'Xoá, gõ "máy nén".'],
       ['Từ khoá 1: HT-002', 'Từ khoá 2: máy nén'],
       ['Bước 4: chỉ còn HT-002.', 'Bước 5: còn HT-001 (khớp một phần, không phân biệt hoa thường).'])
S2.add('Tìm một phần Model', 'P1', [ACC_A, DATA], TMP_STEPS + ['Gõ "RX".'], 'Từ khoá: RX',
       ['Hiện HT-003 (Model RX-200).'])
S2.add('Xoá từ khoá', 'P1', [ACC_A, DATA], TMP_STEPS + ['Gõ "MNK-5".', 'Xoá trắng ô tìm.'], '—',
       ['Bảng hiện lại toàn bộ hàng tạm như lúc mở.'])
S2.add('Lọc theo Dự án', 'P0', [ACC_A, DATA], TMP_STEPS + ['Chọn Dự án = DA-02.'], 'Dự án: DA-02',
       ['Chỉ còn HT-003.', 'Ô Dự án gõ tìm được theo tên hoặc mã dự án.', 'Danh sách dự án chỉ gồm dự án A được xem.'])
S2.add('Lọc theo Báo giá nguồn', 'P0', [ACC_A, DATA], TMP_STEPS + ['Chọn Báo giá nguồn = BG-01.'], 'Báo giá nguồn: BG-01',
       ['Chỉ còn HT-001.', 'Danh sách Báo giá nguồn chỉ gồm báo giá còn hàng tạm chưa thành hàng hoá.'])
S2.add('Lọc theo BOM nguồn', 'P0', [ACC_A, DATA], TMP_STEPS + ['Chọn BOM nguồn = BOM-01.'], 'BOM nguồn: BOM-01',
       ['Chỉ còn HT-002.'])
S2.add('Lọc theo Nguồn', 'P0', [ACC_A, DATA], TMP_STEPS + ['Chọn Nguồn = "Từ BOM Giải pháp".', 'Đổi sang "Từ Báo giá".',
       'Đổi về "Tất cả".'], 'Nguồn: Từ BOM Giải pháp > Từ Báo giá > Tất cả',
       ['Lựa chọn gồm: Tất cả, Từ BOM Giải pháp, Từ Báo giá.',
        'Từ BOM Giải pháp: chỉ dòng Nguồn "BOM" (HT-002).',
        'Từ Báo giá: chỉ dòng Nguồn "Báo giá" (HT-001, HT-003, HT-004).',
        'Tất cả: hiện lại đủ.'])
S2.add('Lọc theo Trạng thái cấu trúc', 'P0', [ACC_A, DATA], TMP_STEPS + ['Chọn "Hàng độc lập".', 'Đổi sang "Hàng cha – ghép bộ".'],
       'Trạng thái cấu trúc: Hàng độc lập > Hàng cha – ghép bộ',
       ['Lựa chọn gồm: Tất cả, Hàng độc lập, Hàng cha – ghép bộ.',
        'Hàng độc lập: KHÔNG có HT-002.',
        'Hàng cha – ghép bộ: chỉ còn HT-002.'])
S2.add('Lọc theo Thương hiệu', 'P1', [ACC_A, DATA], TMP_STEPS + ['Gõ "PUMA" vào ô Thương hiệu, chọn.'], 'Thương hiệu: PUMA',
       ['Chỉ còn hàng tạm thương hiệu PUMA (HT-001).'])
S2.add('Lọc theo Model', 'P1', [ACC_A, DATA], TMP_STEPS + ['Gõ "RX-200" vào ô Model, chọn.'], 'Model: RX-200',
       ['Chỉ còn HT-003.'])
S2.add('Kết hợp nhiều ô lọc với từ khoá', 'P0', [ACC_A, DATA],
       TMP_STEPS + ['Chọn Dự án DA-01.', 'Chọn Nguồn "Từ Báo giá".', 'Gõ "bơm".'],
       ['Dự án: DA-01', 'Nguồn: Từ Báo giá', 'Từ khoá: bơm'],
       ['Chỉ còn HT-004 (thoả cả 3 điều kiện).', 'Tổng số và phân trang tính lại theo kết quả lọc, về trang 1.'])
S2.add('Lọc làm dòng đang chọn biến mất', 'P1', [ACC_A, DATA],
       TMP_STEPS + ['Chọn dòng HT-001.', 'Chọn Nguồn "Từ BOM Giải pháp".'], '—',
       ['HT-001 không còn trong bảng; nút "Dùng hàng này" không bấm được.'])
S2.add('Popup Chọn hàng hóa lọc theo 2 trạng thái', 'P0', [ACC_A, 'Có hàng ở trạng thái Đang kinh doanh và Đang nhập thông tin.'],
       PICK_STEPS + ['Bấm "Tìm kiếm nâng cao".', 'Chọn "Trạng thái HH công ty quản lý" = Đang kinh doanh.',
                     'Chọn "Trạng thái" = Đang nhập thông tin.'],
       ['Trạng thái HH công ty quản lý: Đang kinh doanh', 'Trạng thái: Đang nhập thông tin'],
       ['Khu Tìm kiếm nâng cao có 2 ô "Trạng thái HH công ty quản lý" và "Trạng thái".',
        'Ô "Trạng thái" chỉ có: Đang nhập thông tin, Đang kinh doanh, Hàng tạm, Hàng tạm không duyệt.',
        'Bảng chỉ còn hàng thoả cả 2 trạng thái; dòng "N hàng hoá thoả bộ lọc" đổi theo.'])
S2.add('Popup Chọn hàng hóa bấm Làm mới', 'P1', ACC_A,
       PICK_STEPS + ['Đặt 2 ô trạng thái như case trên, gõ từ khoá.', 'Bấm "Làm mới".'], '—',
       ['Xoá hết từ khoá và các ô lọc, bảng về danh sách mặc định.'])
S2.add('Popup Chọn hàng hóa tìm theo Model', 'P1', ACC_A, PICK_STEPS + ['Gõ model của hàng Y vào ô tìm.'], 'Từ khoá: model hàng Y',
       ['Hiện hàng Y.'])

# ---------------- III. TÙY CHỈNH CỘT ----------------
S3 = Sec(3)
S3.add('Ẩn / hiện 2 cột trạng thái ở popup Chọn hàng hóa', 'P1', ACC_A,
       PICK_STEPS + ['Bấm nút "Cấu hình cột hiển thị".', 'Bỏ tích "Trạng thái HH công ty quản lý", lưu.', 'Tích lại, lưu.'], '—',
       ['Danh sách cột có "Trạng thái HH công ty quản lý" và "Trạng thái".',
        'Bỏ tích: cột biến mất khỏi bảng; tích lại: cột hiện lại đúng vị trí.'])
S3.add('Cấu hình cột được ghi nhớ', 'P1', ACC_A,
       PICK_STEPS + ['Ẩn cột "Trạng thái", lưu.', 'Đóng popup, tải lại trang, mở lại popup.'], '—',
       ['Cột "Trạng thái" vẫn ẩn.',
        'Cấu hình này riêng cho YC hỏi giá: mở popup chọn hàng ở màn khác không bị ảnh hưởng.'])
S3.add('Ẩn / hiện cột Giá nhập ở popup Chọn hàng hóa', 'P1', ACC_A,
       PICK_STEPS + ['Bấm "Cấu hình cột hiển thị".', 'Bỏ tích "Giá nhập", lưu.', 'Tích lại, lưu.'], '—',
       ['Mặc định cột "Giá nhập" hiện ngay sau cột "Giá bán".',
        'Bỏ tích: cột ẩn; tích lại: cột hiện lại.'])

# ---------------- IV. RÀNG BUỘC ----------------
S4 = Sec(4)
S4.add('Giá nhập hiện với hàng từ Báo giá trúng thầu do chính mình lập', 'P0', [ACC_A, DATA], TMP_STEPS, '—',
       ['Dòng HT-001: Giá nhập (Mã tiền tệ) = "20,000,000 VNĐ"; Giá bán (Mã tiền tệ) = "25,000,000 VNĐ".'])
S4.add('Giá nhập ẩn với Báo giá chưa trúng thầu', 'P0', [ACC_A, DATA], TMP_STEPS, '—',
       ['Dòng HT-003 (BG-02 Đang báo giá): cột Giá nhập hiện "—".',
        'Cột Giá bán vẫn hiện số kèm "USD" nếu báo giá có giá bán.'])
S4.add('Giá nhập ẩn với Báo giá trúng thầu do người khác lập', 'P0', [ACC_A, DATA], TMP_STEPS, '—',
       ['Dòng HT-004 (BG-03 do C lập): cột Giá nhập hiện "—"; cột Giá bán vẫn hiện số.'])
S4.add('Dòng từ BOM không hiện Giá nhập', 'P0', [ACC_A, DATA], TMP_STEPS, '—',
       ['Dòng HT-002: Giá nhập hiện "—".',
        'Giá bán hiện "38,000,000", KHÔNG kèm mã tiền tệ (BOM không có tiền tệ).'])
S4.add('Bấm Dùng hàng này điền sẵn thông tin', 'P0', [ACC_A, DATA, 'HT-001 có ĐVT Cái, xuất xứ Đài Loan, % VAT 10, 3 ảnh.'],
       TMP_STEPS + ['Chọn nút tròn dòng HT-001.', 'Bấm "Dùng hàng này".'], '—',
       ['Chuyển sang thẻ nhập hàng tạm.',
        'Điền sẵn: Tên "Máy nén khí 5HP", ĐVT Cái, Thương hiệu PUMA, Xuất xứ Đài Loan, Model MNK-5, Thông số kỹ thuật, % VAT 10%, 3 ảnh.'])
S4.add('Chọn hàng cha mang theo hàng con', 'P0', [ACC_A, DATA], TMP_STEPS + ['Chọn HT-002.', 'Bấm "Dùng hàng này", lưu hàng tạm.'], '—',
       ['Phiếu có dòng "Bộ nâng cầu 2 trụ" kèm đủ 2 hàng con.'])
S4.add('Chỉ chọn được 1 dòng', 'P1', [ACC_A, DATA], TMP_STEPS + ['Chọn HT-001.', 'Chọn HT-003.'], '—',
       ['Chỉ HT-003 được chọn (nút tròn), HT-001 bỏ chọn.'])
S4.add('Hàng tạm đã thành hàng hoá không còn trong kho', 'P0',
       [ACC_A, 'HT-001 vừa được duyệt tạo mã hàng hoá chính thức.'], TMP_STEPS + ['Tìm "HT-001".'], 'Từ khoá: HT-001',
       ['Bảng hiện %s' % EMPTY])
S4.add('Định dạng số giá', 'P1', [ACC_A, DATA], TMP_STEPS, '—',
       ['Giá dùng dấu phẩy ngăn nghìn: "20,000,000", không dùng dấu chấm ngăn nghìn.'])

# ---------------- V. PHÂN QUYỀN ----------------
S5 = Sec(5)
S5.add('Có quyền Xem giá vốn hàng hoá — popup Chọn hàng hóa', 'P0', ACC_A, PICK_STEPS, '—',
       ['Có cột "Giá nhập" sau cột "Giá bán", hiện số giá vốn từng hàng.',
        'Trong cấu hình cột có mục "Giá nhập".'])
S5.add('Không có quyền Xem giá vốn hàng hoá — popup Chọn hàng hóa', 'P0', ACC_B, PICK_STEPS + ['Bấm "Cấu hình cột hiển thị".'], '—',
       ['KHÔNG có cột "Giá nhập" trong bảng.', 'KHÔNG có mục "Giá nhập" trong cấu hình cột.'])
S5.add('Không có quyền Xem giá vốn hàng hoá — kho hàng tạm', 'P0',
       [ACC_B, 'Báo giá BG-05 (Trúng thầu, do B lập) có hàng tạm HT-005, Giá nhập 10,000,000, Giá bán 12,000,000 VNĐ.'],
       TMP_STEPS, '—',
       ['Dòng HT-005: Giá nhập hiện "—" (dù là báo giá trúng thầu của chính B).',
        'Giá bán vẫn hiện "12,000,000 VNĐ".'])
S5.add('Được cấp quyền thì thấy Giá nhập', 'P1', ACC_B + '\nQuản trị cấp thêm quyền %s cho B.' % COST,
       ['Đăng nhập lại bằng B.', MENU, OPEN_TMP, TAB_TMP], '—',
       ['Dòng HT-005: Giá nhập hiện "10,000,000 VNĐ".'])
S5.add('Chỉ thấy hàng tạm thuộc dự án được xem', 'P0', [ACC_B, DATA], TMP_STEPS + ['Mở ô lọc Dự án.'], '—',
       ['Không có HT-003 (dự án DA-02) trong bảng.', 'Ô Dự án không có DA-02.'])

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'TÙY CHỈNH CỘT', S3),
    ('IV', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S4),
    ('V', 'PHÂN QUYỀN', S5),
]

if __name__ == '__main__':
    total = sum(len(s) for _, _, s in SECTIONS)
    p0 = sum(1 for _, _, s in SECTIONS for tc in s if tc[2] == 'P0')
    print('Tong %d TC, P0 %d (%.0f%%)' % (total, p0, 100.0 * p0 / total))
    BANNED = [r"`[a-z_]{3,}`", r"\bBE\b", r"\bFE\b", r"\bHTTP\b", r"\b(400|403|404|422)\b", r"/api/v1", r"localStorage",
              r"\bERP\b", r"\bAPI\b", r"E2E", r"Postman", r"gọi thẳng", r"TC-ROLE", r"https?://"]
    text = '\n'.join(v for _, v in DESCRIPTION_BLOCK) + '\n' + '\n'.join('\n'.join(tc) for _, _, s in SECTIONS for tc in s)
    found = {p: len(re.findall(p, text)) for p in BANNED if re.findall(p, text)}
    print('!!! CON THUAT NGU KY THUAT:', found) if found else print('OK - sach')
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='YCHG chọn hàng & kho hàng tạm (#11949) - Cập nhật ngày 18/11/2026',
                module_name='YC hỏi giá - Chọn hàng', description_block=DESCRIPTION_BLOCK,
                sections=[(r, t, list(s)) for r, t, s in SECTIONS], loai='phieu')
