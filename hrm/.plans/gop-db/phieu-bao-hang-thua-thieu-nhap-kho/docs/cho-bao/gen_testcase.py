# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu nhập kho chờ báo thừa, thiếu" (STT 288) — KHUÔN CHUẨN tab "13. DM quốc gia" (03/11/2026), loại 'phieu'.

Màn là hàng chờ (danh sách việc cần làm): không Sửa / Xóa / Duyệt riêng. Thao tác "Báo hàng thừa thiếu" mở trang Tạo phiếu báo
(màn 289) ⇒ đặt ở nhóm THÊM MỚI; validate chi tiết của form nằm ở testcase màn 289.
Sinh bằng testcase-documenter/assets/tc_chuan.build_chuan (tự chạy check_tc — phải 0 lỗi); case chung từ ../_tc_phieu_chung.py.
Không có TC cũ. Chạy: python gen_testcase.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets')))
from tc_chuan import build_chuan  # noqa: E402
from _tc_phieu_chung import C, danh_so, hien_thi, tim_kiem, tuy_chinh_cot, xuat_excel  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Phiếu nhập kho chờ báo thừa, thiếu'
MODULE = 'PNK chờ báo thừa, thiếu'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SHEET = 'Trang tính1'
NGAY = '18/11/2026'


def L_(*lines):
    return '\n'.join(lines)


MENU = 'Kho > Nhập kho > Phiếu nhập kho chờ báo thừa, thiếu'
MENU_PB = 'Kho > Nhập kho > Phiếu báo hàng thừa, thiếu nhập kho'
MENU_PNK = 'Kho > Nhập kho > Phiếu nhập kho'
Q_XEM = 'Xem xử lý thừa thiếu nhập kho'
Q_TAO = 'Tạo phiếu báo hàng thừa, thiếu nhập kho'
Q_DUYET = 'Duyệt phiếu báo hàng thừa, thiếu nhập kho'
RONG = 'Không có phiếu nhập kho nào chờ báo thừa, thiếu.'
LOAI6 = ('Nhập hàng mua trong nước; Nhập hàng mua trong nước (HĐNT); Nhập hàng mua trong nước (TỰ DO + HÃNG); '
         'Nhập hàng mua nước ngoài; Nhập hàng mua nước ngoài (mới); Nhập hàng mua ngoài')

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '-  TK-A: thủ kho công ty TPE, có quyền "' + Q_TAO + '", không có quyền xem; đã lập PNK-1, PNK-2.',
    '-  TK-CTY: "' + Q_XEM + '" mức Công ty (TPE). TK-ALL: mức Tổng công ty. TK-Z: không có quyền nào. TK-D: chỉ có "' + Q_DUYET + '".',
    '-  PNK-1 (dev PNK-02741): Đã hạch toán, Nhập hàng mua trong nước (TỰ DO + HÃNG), 1 dòng SL đề nghị 20, thực nhập 0, không có nhà cung cấp.',
    '-  PNK-2 (dev PNK-02667): như PNK-1, nhà cung cấp CÔNG TY CỔ PHẦN VIỆT ĐỨC, Phiếu ĐNNK PDNNK-02573.',
    '-  Dev 18/11/2026 có 7 phiếu trong hàng chờ (tài khoản xem mức Tổng công ty).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Phiếu nhập kho chờ báo thừa, thiếu" là HÀNG CHỜ: liệt kê các phiếu nhập kho đã hạch toán có hàng thực nhập khác số lượng '
        'đề nghị nhập mà chưa được lập phiếu báo hàng thừa, thiếu. Từ mỗi dòng, người có quyền bấm "Báo hàng thừa thiếu" để mở trang '
        'Tạo phiếu báo (màn ' + MENU_PB + ') với phiếu nhập kho chọn sẵn.',
        'Đường vào: menu ' + MENU + '.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Báo hàng thừa thiếu, Xuất Excel.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phiếu nhập kho hiện trên màn khi ĐỦ cả 4 điều kiện:',
        '-  Trạng thái Đã hạch toán.',
        '-  Loại thuộc 6 loại: ' + LOAI6 + '.',
        '-  Có ít nhất 1 dòng hàng SL thực nhập khác SL đề nghị nhập (so phần nguyên).',
        '-  Chưa có phiếu báo hàng thừa, thiếu nào (mọi trạng thái).',
        'Phạm vi: mức Tổng công ty: mọi công ty; mức Công ty: phiếu nhập kho của công ty đang làm việc; không có quyền xem: phiếu nhập kho do mình lập.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Phiếu nhập kho chưa hạch toán (Đang tạo, Chờ duyệt, Đang hạch toán, Không duyệt…) hoặc loại nhập khác (điều chuyển, nhập lại…).',
        '-  Phiếu nhập kho mà mọi dòng khớp số lượng, hoặc chỉ lệch phần thập phân.',
        '-  Phiếu nhập kho đã có phiếu báo (kể cả phiếu báo Đang tạo / Không duyệt).',
        '-  Nút "Báo hàng thừa thiếu" ẨN khi tài khoản không có quyền "' + Q_TAO + '".',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô "Ngày tạo" (Từ – Đến) lọc theo ngày tạo PHIẾU NHẬP KHO, tính cả 2 đầu mút. Bộ lọc ghi nhớ 10 phút.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Mỗi dòng = 1 phiếu nhập kho: Mã phiếu, Loại, Nhà cung cấp, Ngày tạo, Phiếu ĐNNK, Người đề nghị (người lập đề nghị nhập kho), '
        'Người yêu cầu (người lập yêu cầu nhập hàng), Người tạo (người lập phiếu nhập kho).',
        'Phiếu nhập lại có dòng phụ "Nhập lại cho phiếu <mã phiếu gốc>".',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  1 phiếu nhập kho chỉ được báo 1 lần: lưu phiếu báo thì phiếu nhập kho rời hàng chờ; xóa phiếu báo thì quay lại.',
        '-  Màn không ghi tồn kho, không sửa phiếu nhập kho.',
    )),
    ('7. Phân quyền cấp', L_(
        '-  "' + Q_XEM + '" — mức: Công ty / Tổng công ty (dùng chung với màn Phiếu báo hàng thừa, thiếu nhập kho).',
        '-  "' + Q_TAO + '": nút Báo hàng thừa thiếu.',
        '-  Menu không ẩn theo quyền. Quyền "' + Q_DUYET + '" không mở rộng phạm vi màn này. Super Admin có mọi quyền.',
    )),
    ('8. Cách tính các ô thống kê', 'Chân bảng "Hiển thị a–b / N": N = tổng phiếu nhập kho khớp điều kiện hàng chờ, bộ lọc và phạm vi.'),
    ('9. Ghi chú đọc bảng', L_(
        'Các bẫy dễ sai nhất của màn này, QA đọc trước khi test:',
        '-  Lưu phiếu báo ở trạng thái Đang tạo cũng làm phiếu nhập kho rời hàng chờ.',
        '-  Lệch chỉ ở phần thập phân (2.5 so với 2) KHÔNG đưa phiếu vào hàng chờ.',
        '-  Bấm Quay lại ở trang Tạo phiếu báo về danh sách Phiếu báo, KHÔNG về hàng chờ.',
        '-  Ô trống để trống. Cột KQ thực tế, DNS check để trống cho tester điền.',
    )),
]

K = dict(
    menu=MENU,
    tieu_de='Danh sách phiếu nhập kho chờ báo thừa, thiếu',
    exp_mo_them=['Tiêu đề trang (thanh trên cùng) "Phiếu nhập kho chờ báo thừa, thiếu"'],
    exp_nut=['Thanh công cụ có: Xuất Excel, Cấu hình cột hiển thị; KHÔNG có Tạo mới, Import, In danh sách',
             'Khối tìm kiếm có ô "Tìm theo mã phiếu nhập kho", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc'],
    cot=['STT', 'Mã phiếu', 'Loại', 'Nhà cung cấp', 'Ngày tạo', 'Phiếu ĐNNK', 'Người đề nghị', 'Người yêu cầu', 'Người tạo', 'Hành động'],
    cot_an=[],
    tong_cot=10,
    cot_khoa=['STT', 'Mã phiếu', 'Hành động'],
    cot_bo_thu='Người yêu cầu',
    cot_keo='Ngày tạo',
    pre_du_lieu='PNK-2 vừa được hạch toán, có dòng lệch, chưa có phiếu báo.',
    exp_du_lieu=['Mã phiếu PNK-02667 là liên kết; Loại "Nhập hàng mua trong nước (TỰ DO + HÃNG)"; Nhà cung cấp "CÔNG TY CỔ PHẦN VIỆT ĐỨC"',
                 'Phiếu ĐNNK PDNNK-02573 là liên kết; Người đề nghị, Người yêu cầu, Người tạo dạng "Họ tên - Mã phòng ban"'],
    trang_thai=None,
    pre_rong='TK-Z không có quyền xem, chưa lập phiếu nhập kho nào.',
    rong_bang=RONG,
    rong_chan=None,
    sap_xep=['Mã phiếu', 'Ngày tạo'],
    khong_sap_xep=['STT', 'Loại', 'Nhà cung cấp', 'Phiếu ĐNNK', 'Người đề nghị', 'Người yêu cầu', 'Người tạo', 'Hành động'],
    ma='Mã phiếu', vd_ma='PNK-02667', vd_mot_phan='PNK-02', placeholder='Tìm theo mã phiếu nhập kho',
    loc_text=('Hàng hóa', 'Nước làm mát', 'nuoc lam mat'),
    loc_list=['Hàng hóa', 'Kho hàng', 'Phiếu ĐNNK', 'Loại', 'Nhà cung cấp', 'Người đề nghị', 'Ngày tạo', 'Công ty'],
    exp_mac_dinh_them=['Ô Công ty chỉ hiện với tài khoản xem mức Tổng công ty'],
    mac_dinh_ds='Danh sách hiện mọi phiếu nhập kho chờ báo trong phạm vi xem',
    loc_chon=('Nhà cung cấp', 'CÔNG TY CỔ PHẦN VIỆT ĐỨC'),
    loc_ket_hop='Loại = Nhập hàng mua trong nước (TỰ DO + HÃNG), Nhà cung cấp = CÔNG TY CỔ PHẦN VIỆT ĐỨC, Ngày tạo = tháng 11/2025',
    td_rong='Loại: Nhập hàng mua ngoài; Ngày tạo: hôm nay',
    excel=dict(title='Chọn trường xuất Excel', so_truong=8,
               truong=['Mã phiếu', 'Loại', 'Nhà cung cấp', 'Ngày tạo', 'Phiếu ĐNNK', 'Người đề nghị', 'Người yêu cầu', 'Người tạo'],
               mac_dinh='Mặc định tích sẵn các trường ứng với cột đang hiện trên bảng (chưa tùy chỉnh cột: cả 8, "Đang chọn 8/8 trường")',
               file='danh_sach_phieu_nhap_kho_cho_bao_thua_thieu.xlsx', tieu_de='DANH SÁCH PHIẾU NHẬP KHO CHỜ BÁO THỪA, THIẾU',
               bo_thu='Người yêu cầu', exp_them=['Cột STT đứng đầu file'],
               rong=['Báo "Không có dữ liệu để xuất"', 'KHÔNG tải file nào']),
)

K['hien_thi_rieng'] = [
    C('Liên kết cột Mã phiếu và Phiếu ĐNNK', 'P1', 'Có PNK-2.', ['1. Bấm PNK-02667', '2. Bấm PDNNK-02573'], '',
      ['Mỗi lần mở 1 tab mới: chi tiết Phiếu nhập kho / chi tiết Phiếu đề nghị nhập kho', 'Danh sách ở tab cũ giữ nguyên']),
    C('Phiếu nhập lại ghi phiếu gốc', 'P2', 'Có phiếu nhập lại (nhập lại cho phiếu PNK-G) thỏa điều kiện hàng chờ.', ['1. Xem ô Mã phiếu của dòng đó'], '',
      ['Dưới mã có dòng nghiêng "Nhập lại cho phiếu PNK-G", PNK-G là liên kết mở tab mới']),
    C('Nút Báo hàng thừa thiếu trên từng dòng', 'P0', 'TK-A có quyền Tạo.', ['1. Xem cột Hành động'], '',
      ['Mỗi dòng có 1 nút biểu tượng chấm than, rê chuột hiện "Báo hàng thừa thiếu"']),
    C('Ô trống để trống', 'P2', 'PNK-1 không có nhà cung cấp.', ['1. Xem cột Nhà cung cấp dòng PNK-1'], '', ['Ô để TRỐNG, không in "-"']),
]

K['loc_rieng'] = [
    C('Lọc theo Hàng hóa', 'P0', 'PNK-2 có hàng VDUC-E504LXANH.', ['1. Mở Tìm kiếm nâng cao', '2. Nhập "E504LXANH" ở ô Hàng hóa', '3. Nhấn Enter'],
      'Hàng hóa: E504LXANH', ['Chỉ còn phiếu có dòng hàng mã / tên chứa từ khóa, gồm PNK-02667', 'Gõ chưa Enter thì chưa lọc']),
    C('Lọc theo Kho hàng', 'P0', 'Có phiếu của 2 kho.', ['1. Chọn 1 kho ở ô Kho hàng'], '',
      ['Danh sách chọn dạng "Mã - Tên kho", chỉ gồm kho có trên phiếu trong phạm vi; kho đã khóa có biểu tượng ổ khóa', 'Chỉ còn phiếu của kho đó']),
    C('Lọc theo Phiếu ĐNNK', 'P1', 'PNK-2 lập từ PDNNK-02573.', ['1. Nhập "02573" ở ô Phiếu ĐNNK, Enter'], '', ['Chỉ còn PNK-02667']),
    C('Lọc theo Loại', 'P0', 'Có phiếu nhiều loại.', ['1. Mở ô Loại', '2. Chọn Nhập hàng mua trong nước (TỰ DO + HÃNG)'], '',
      ['Danh sách chọn đúng 6 loại: ' + LOAI6, 'Chỉ còn phiếu đúng loại']),
    C('Lọc theo Nhà cung cấp', 'P1', 'PNK-2 có nhà cung cấp.', ['1. Chọn Nhà cung cấp = CÔNG TY CỔ PHẦN VIỆT ĐỨC'], '',
      ['Danh sách chọn chỉ gồm nhà cung cấp có trên phiếu trong hàng chờ; nhà cung cấp khóa có ổ khóa', 'Chỉ còn PNK-02667']),
    C('Lọc theo Người đề nghị', 'P1', 'Có phiếu do 2 người đề nghị.', ['1. Chọn Người đề nghị = Bùi Khánh Hòa'], '',
      ['Danh sách chọn dạng "Mã phòng ban - Họ tên"', 'Chỉ còn phiếu có cột Người đề nghị là người đã chọn']),
    C('Lọc theo khoảng Ngày tạo', 'P0', 'Có phiếu tạo 27/11/2025 và 28/11/2025.', ['1. Chọn Ngày tạo từ 27/11/2025 đến 27/11/2025'], '',
      ['Chỉ còn phiếu nhập kho tạo ngày 27/11/2025 (tính cả 2 đầu mút)']),
    C('Lọc theo Công ty', 'P1', 'TK-ALL; có phiếu của 2 công ty.', ['1. Đăng nhập TK-ALL', '2. Chọn Công ty = TPE'], '',
      ['Ô Công ty dạng "Mã - Tên"', 'Chỉ còn phiếu của TPE']),
]

S_BAO = [
    C('Báo hàng thừa thiếu mở trang Tạo phiếu báo', 'P0', 'TK-A có quyền Tạo; PNK-2 trong hàng chờ.', ['1. Vào menu ' + MENU, '2. Bấm Báo hàng thừa thiếu ở dòng PNK-02667'], '',
      ['Mở trang "Tạo phiếu báo hàng thừa, thiếu nhập kho"', 'Ô Phiếu nhập kho = PNK-02667; Yêu cầu nhập PYCNH-04125; Số hợp đồng DHNT-000499; Nhà cung cấp CÔNG TY CỔ PHẦN VIỆT ĐỨC',
       'Bảng Chi tiết: "Nước làm mát động cơ Gly Coolant E50 xanh/Thùng 4x4L", SL đề nghị 7, thực nhập 0, SL thiếu 7', 'Diễn giải trống, chưa có file']),
    C('Bảng Chi tiết chỉ có dòng lệch', 'P0', 'PNK-3 có 3 dòng: 20/10, 10/20, 5/5.', ['1. Bấm Báo hàng thừa thiếu ở PNK-3'], '',
      ['Bảng Chi tiết có 2 dòng: SL thiếu 10 và SL thừa 10; dòng 5/5 không hiện']),
    C('Lưu phiếu báo thì phiếu nhập kho rời hàng chờ', 'P0', 'Đang ở trang Tạo mở từ PNK-2.', ['1. Nhập Diễn giải, đính kèm 1 file pdf', '2. Bấm Lưu', '3. Vào lại menu ' + MENU], '',
      ['Bước 2: toast "Lưu thành công.", về danh sách Phiếu báo hàng thừa, thiếu nhập kho, có phiếu mới Đang tạo của PNK-02667',
       'Bước 3: PNK-02667 KHÔNG còn ở hàng chờ; tổng N giảm 1']),
    C('Lưu và gửi từ hàng chờ', 'P0', 'Trang Tạo mở từ PNK-1, nhập đủ.', ['1. Bấm Lưu và gửi'], '',
      ['Phiếu báo Chờ xử lý; PNK-1 rời hàng chờ; người duyệt nhận thông báo Chờ duyệt']),
    C('Bấm Quay lại không nhập gì', 'P0', 'Trang Tạo mở từ PNK-2, chưa nhập Diễn giải / file.', ['1. Bấm Quay lại'], '',
      ['Về danh sách Phiếu báo hàng thừa, thiếu nhập kho (không phải hàng chờ), không tạo phiếu', 'PNK-2 vẫn ở hàng chờ']),
    C('Bấm Quay lại khi đã nhập', 'P1', 'Trang Tạo mở từ PNK-2, đã nhập Diễn giải.', ['1. Bấm Quay lại', '2. Bấm Thoát'], '',
      ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"', 'Thoát: không tạo phiếu, PNK-2 vẫn ở hàng chờ']),
    C('Thiếu Diễn giải / file thì bị chặn', 'P0', 'Trang Tạo mở từ PNK-2.', ['1. Bấm Lưu ngay'], '',
      ['Toast "Bạn chưa nhập đầy đủ thông tin."', 'Báo "Diễn giải – Vui lòng nhập diễn giải." và "File đính kèm – Vui lòng đính kèm ít nhất 1 file."',
       'Ô Phiếu nhập kho không báo lỗi (đã chọn sẵn)']),
    C('Phiếu nhập kho vừa được người khác báo', 'P0', 'TK-A và TK-A2 cùng mở hàng chờ có PNK-1.', ['1. TK-A2 bấm Báo hàng thừa thiếu PNK-1, nhập đủ, Lưu', '2. TK-A (chưa tải lại) bấm Báo hàng thừa thiếu PNK-1'], '',
      ['TK-A: toast "Phiếu nhập kho không còn chờ báo thừa, thiếu hoặc bạn không có quyền.", ô Phiếu nhập kho trống', 'Chỉ có 1 phiếu báo cho PNK-1']),
    C('Hai người cùng lưu cho một phiếu nhập kho', 'P1', 'TK-A và TK-A2 cùng ở trang Tạo của PNK-1, đã nhập đủ.', ['1. Cả 2 bấm Lưu gần như đồng thời'], '',
      ['1 người lưu được; người còn lại bị báo "Phiếu nhập kho không còn chờ báo thừa, thiếu (đã có phiếu báo hoặc không đủ điều kiện)."']),
    C('Lưu và tiếp tục khi vào từ hàng chờ', 'P2', 'Trang Tạo mở từ PNK-1, nhập đủ.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Lưu thành công; trang Tạo mở lại trống, không còn chọn sẵn phiếu nhập kho']),
    C('Bấm nút 2 lần liên tục', 'P2', 'Hàng chờ có PNK-2.', ['1. Bấm Báo hàng thừa thiếu 2 lần thật nhanh'], '',
      ['Chỉ mở 1 trang Tạo, không lỗi']),
]

S_RB = [
    C('Xóa phiếu báo thì phiếu nhập kho quay lại hàng chờ', 'P0', 'PNK-2 đã có phiếu báo Đang tạo của TK-A.', ['1. Vào ' + MENU_PB + ', xóa phiếu báo của PNK-2', '2. Mở lại hàng chờ'], '',
      ['PNK-02667 xuất hiện lại trong hàng chờ']),
    C('Phiếu báo bị Không duyệt không trả phiếu nhập kho về hàng chờ', 'P1', 'Phiếu báo của PNK-1 bị Không duyệt.', ['1. Mở hàng chờ'], '', ['PNK-1 không có trong hàng chờ']),
    C('Phiếu nhập kho mới hạch toán có hàng lệch thì vào hàng chờ', 'P0', 'PNK-7 (loại nhập mua, có dòng lệch) đang Đang hạch toán.',
      ['1. Mở hàng chờ, tìm PNK-7', '2. Kế toán hoàn tất hạch toán PNK-7', '3. Tìm lại'], '', ['Bước 1: không có', 'Bước 3: PNK-7 có trong hàng chờ']),
    C('Phiếu nhập kho không lệch không vào hàng chờ', 'P0', 'PNK-8 Đã hạch toán, mọi dòng khớp số lượng.', ['1. Tìm PNK-8'], '', ['Không có PNK-8']),
    C('Lệch phần thập phân không vào hàng chờ', 'P2', 'PNK-9 Đã hạch toán, chỉ 1 dòng SL đề nghị 2.5, thực nhập 2.', ['1. Tìm PNK-9'], '',
      ['Không có PNK-9 (so phần nguyên coi là khớp)']),
    C('Loại nhập khác không vào hàng chờ', 'P0', 'PNK-10 loại Nhập điều chuyển kho chi nhánh, Đã hạch toán, có dòng lệch.', ['1. Tìm PNK-10'], '', ['Không có PNK-10']),
    C('Danh sách khớp cửa sổ Chọn phiếu nhập kho', 'P0', 'TK-A.', ['1. Ghi lại danh sách hàng chờ', '2. Vào ' + MENU_PB + ' > Tạo mới > bấm ô Phiếu nhập kho'], '',
      ['Cửa sổ chọn có đúng các phiếu như hàng chờ của cùng tài khoản']),
    C('Màn không đổi tồn kho và phiếu nhập kho', 'P2', 'Ghi lại tồn kho hàng trong PNK-2.', ['1. Mở hàng chờ, xuất Excel, mở trang Tạo rồi thoát'], '',
      ['Tồn kho và phiếu nhập kho PNK-2 không đổi']),
]

S_QUYEN = [
    C('Không có quyền nào: chỉ thấy phiếu nhập kho mình lập', 'P0', 'TK-Z chưa lập phiếu nhập kho nào.', ['1. Đăng nhập TK-Z', '2. Vào menu ' + MENU], '',
      ['Mục menu vẫn hiện, mở được màn', 'Bảng "' + RONG + '"', 'Không có ô Công ty']),
    C('Không quyền xem nhưng là người lập phiếu nhập kho', 'P0', 'TK-A lập PNK-1, PNK-2 (trong hàng chờ); không có quyền xem.', ['1. Đăng nhập TK-A, vào màn'], '',
      ['Chỉ thấy PNK-1, PNK-2 (phiếu do mình lập), không thấy phiếu người khác']),
    C('Quyền "' + Q_XEM + '" mức Tổng công ty', 'P0', 'TK-ALL; hàng chờ có phiếu của 2 công ty.', ['1. Đăng nhập TK-ALL, vào màn', '2. Mở Tìm kiếm nâng cao'], '',
      ['Thấy phiếu mọi công ty (dev: 7 phiếu)', 'Có ô Công ty']),
    C('Quyền "' + Q_XEM + '" mức Công ty', 'P0', 'TK-CTY thuộc TPE.', ['1. Đăng nhập TK-CTY, vào màn'], '',
      ['Chỉ phiếu nhập kho của TPE', 'Không có ô Công ty']),
    C('Quyền "' + Q_TAO + '"', 'P0', 'TK-A có quyền Tạo; TK-CTY không có.', ['1. Lần lượt đăng nhập TK-A, TK-CTY, xem cột Hành động'], '',
      ['TK-A: có nút Báo hàng thừa thiếu trên mọi dòng', 'TK-CTY: cột Hành động trống (nút ẨN, không hiện mờ)']),
    C('Quyền Duyệt không mở rộng phạm vi', 'P1', 'TK-D chỉ có "' + Q_DUYET + '", chưa lập phiếu nhập kho.', ['1. Đăng nhập TK-D, vào màn'], '',
      ['Danh sách trống như người không có quyền']),
    C('Không có quyền Tạo mà mở thẳng trang Tạo từ hàng chờ', 'P1', 'TK-CTY biết đường dẫn trang Tạo kèm PNK-2.', ['1. Dán đường dẫn vào trình duyệt'], '',
      ['Toast "Phiếu nhập kho không còn chờ báo thừa, thiếu hoặc bạn không có quyền."; không nạp dữ liệu', 'Bấm Lưu bị từ chối "Bạn không có quyền tạo phiếu báo hàng thừa, thiếu nhập kho."']),
    C('Người có 2 mức xem khác nhau', 'P1', 'TK-X có mức Công ty và mức Tổng công ty ở 2 vai trò.', ['1. Đăng nhập TK-X, vào màn'], '', ['Áp mức lớn hơn: thấy mọi công ty, có ô Công ty']),
    C('Đổi công ty đang làm việc', 'P0', 'TK-CTY làm việc ở 2 công ty.', ['1. Đổi sang công ty B', '2. Vào màn'], '',
      ['Danh sách tính lại theo công ty B, không thấy phiếu nhập kho công ty cũ']),
    C('Bị bỏ quyền Tạo khi đang ở màn', 'P0', 'TK-A đang mở hàng chờ.', ['1. Quản trị bỏ quyền Tạo của TK-A', '2. TK-A bấm Báo hàng thừa thiếu, nhập đủ, bấm Lưu'], '',
      ['Hệ thống từ chối, không tạo phiếu báo; tải lại màn thì nút Báo hàng thừa thiếu biến mất']),
    C('Phạm vi áp như nhau cho danh sách và xuất Excel', 'P1', 'TK-CTY.', ['1. Xuất Excel không lọc'], '', ['File chỉ gồm phiếu nhập kho của TPE, khớp số dòng trên màn']),
    C('Super Admin', 'P2', 'Tài khoản Super Admin.', ['1. Vào màn'], '', ['Thấy mọi phiếu, có ô Công ty và nút Báo hàng thừa thiếu']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', danh_so(hien_thi(K))),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', danh_so(tim_kiem(K))),
    ('III', 'THÊM MỚI (BÁO HÀNG THỪA THIẾU)', danh_so(S_BAO)),
    ('IV', 'TÙY CHỈNH CỘT', danh_so(tuy_chinh_cot(K))),
    ('V', 'XUẤT DANH SÁCH EXCEL', danh_so(xuat_excel(K))),
    ('VI', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', danh_so(S_RB)),
    ('VII', 'PHÂN QUYỀN', danh_so(S_QUYEN)),
]

if __name__ == '__main__':
    build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='phieu')
