# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu báo hàng thừa, thiếu nhập kho" (STT 289) — KHUÔN CHUẨN tab "13. DM quốc gia" (03/11/2026), loại 'phieu'.

Sinh bằng testcase-documenter/assets/tc_chuan.build_chuan (tự chạy check_tc — phải 0 lỗi). Case chung (hiển thị, phân trang,
tìm kiếm, lưu bộ lọc, tùy chỉnh cột, xuất Excel, lịch sử, đóng form) từ ../_tc_phieu_chung.py; case nghiệp vụ viết ở đây.
Không có TC cũ. Nhóm không áp dụng: Khóa / Mở khóa, Hủy phiếu, In phiếu, Import.
Chạy: python gen_testcase.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets')))
from tc_chuan import build_chuan  # noqa: E402
from _tc_phieu_chung import C, danh_so, hien_thi, tim_kiem, them_moi_dong_form, lich_su, tuy_chinh_cot, \
    xuat_excel, phan_quyen_chung  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Phiếu báo hàng thừa, thiếu nhập kho'
MODULE = 'Phiếu báo hàng thừa, thiếu NK'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SHEET = 'Trang tính1'
NGAY = '18/11/2026'


def L_(*lines):
    return '\n'.join(lines)


MENU = 'Kho > Nhập kho > Phiếu báo hàng thừa, thiếu nhập kho'
MENU_CHO = 'Kho > Nhập kho > Phiếu nhập kho chờ báo thừa, thiếu'
Q_XEM = 'Xem xử lý thừa thiếu nhập kho'
Q_TAO = 'Tạo phiếu báo hàng thừa, thiếu nhập kho'
Q_DUYET = 'Duyệt phiếu báo hàng thừa, thiếu nhập kho'
CHUA_DU = 'Bạn chưa nhập đầy đủ thông tin.'
E_PNK = 'Phiếu nhập kho – Vui lòng chọn phiếu nhập kho.'
E_DG = 'Diễn giải – Vui lòng nhập diễn giải.'
E_FILE = 'File đính kèm – Vui lòng đính kèm ít nhất 1 file.'
E_TAKEN = 'Phiếu nhập kho không còn chờ báo thừa, thiếu (đã có phiếu báo hoặc không đủ điều kiện).'
E_DOI_TT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'
E_LD = 'Vui lòng nhập lý do không duyệt'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '-  TK-A: nhân viên kho công ty TPE, có quyền "' + Q_TAO + '", không có quyền xem / duyệt.',
    '-  TK-D: có "' + Q_DUYET + '", cùng công ty TPE, được giao quản lý phòng ban của TK-A. TK-D2: có quyền Duyệt nhưng KHÔNG quản lý phòng của TK-A.',
    '-  TK-CTY: "' + Q_XEM + '" mức Công ty (TPE). TK-ALL: mức Tổng công ty. TK-Z: không có quyền nào.',
    '-  PNK-1: phiếu nhập kho Đã hạch toán, loại Nhập hàng mua trong nước (TỰ DO + HÃNG), do TK-A lập, có 1 dòng hàng SL đề nghị 20, SL thực nhập 0 (dev: PNK-02741).',
    '-  PNK-2: như PNK-1 nhưng có nhà cung cấp (dev: PNK-02667 - CÔNG TY CỔ PHẦN VIỆT ĐỨC).',
    '-  Phiếu báo mẫu trên dev: TPE_BHNK-00020 (Đang tạo, có 2 mốc lịch sử), TPE_BHNK-00021 (Chờ xử lý), TPE_BHNK-00019 (Đã xử lý).',
    '-  File mẫu: bien-ban.pdf (200KB); file.exe; file-lon.pdf (16MB).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Phiếu báo hàng thừa, thiếu nhập kho" dùng để báo các dòng hàng của 1 phiếu nhập kho đã hạch toán có số lượng thực nhập '
        'khác số lượng đề nghị nhập, để người duyệt xử lý (lập phiếu xử lý hàng thiếu) hoặc trả lại.',
        'Luồng: chọn phiếu nhập kho chờ báo (hệ thống tự điền dòng hàng lệch) > nhập Diễn giải + file > Lưu (Đang tạo) hoặc Lưu và gửi '
        '(Chờ xử lý) > người duyệt Không duyệt (trả về, người tạo sửa gửi lại) hoặc Xử lý (lập phiếu xử lý ở hệ thống quản lý kho cũ, phiếu báo thành Đã xử lý).',
        'Đường vào: menu ' + MENU + '; hoặc nút "Báo hàng thừa thiếu" ở menu ' + MENU_CHO + '.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới, Sửa, Xóa, Xem chi tiết, Không duyệt, Xử lý, '
        'Lịch sử, Xuất Excel.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi danh sách (xét lần lượt):',
        '-  "' + Q_XEM + '" mức Tổng công ty: mọi phiếu mọi công ty; có ô lọc Công ty.',
        '-  Mức Công ty: phiếu thuộc công ty đang làm việc + phiếu mình tạo.',
        '-  "' + Q_DUYET + '": thêm phiếu Chờ xử lý của công ty mình.',
        '-  Không có quyền nào: chỉ phiếu mình tạo.',
        'Phiếu nhập kho chọn được khi lập phiếu báo: Đã hạch toán, thuộc 6 loại nhập hàng mua, có dòng lệch SL, chưa có phiếu báo, trong phạm vi.',
        'Trạng thái phiếu báo: Đang tạo (xám), Chờ xử lý (vàng), Đã xử lý (xanh lá), Không duyệt (đỏ).',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Phiếu ngoài phạm vi: không hiện; mở đường dẫn trực tiếp sang trang "Không tìm thấy".',
        '-  Phiếu nhập kho đã có phiếu báo (mọi trạng thái) không còn trong cửa sổ "Chọn phiếu nhập kho".',
        '-  Bảng Chi tiết chỉ có dòng hàng LỆCH (so phần nguyên); dòng khớp số lượng không hiện.',
        '-  Nút Sửa / Xóa ẨN với phiếu Chờ xử lý, Đã xử lý và với người không phải người tạo; Xử lý / Không duyệt ẨN nếu không phải phiếu Chờ xử lý hoặc không có quyền Duyệt.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" (Từ – Đến) lọc theo ngày tạo phiếu báo, tính cả 2 đầu mút. Bộ lọc được ghi nhớ 10 phút khi sang trang '
        'Chi tiết / Sửa rồi quay lại.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Phiếu báo = 1 phiếu nhập kho + Diễn giải + file đính kèm + các dòng hàng lệch (Tên hàng hóa, Model, Mã hàng hóa, ĐVT, '
        'SL đề nghị nhập, SL thực nhập, SL thiếu, SL thừa).',
        'Số phiếu dạng <mã công ty người lập>_BHNK-<5 chữ số>. Yêu cầu nhập, Số hợp đồng, Nhà cung cấp lấy theo phiếu nhập kho.',
        'SL thiếu = SL đề nghị trừ SL thực nhập (khi dương); SL thừa = SL thực nhập trừ SL đề nghị (khi dương).',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  1 phiếu nhập kho chỉ có 1 phiếu báo; 2 người lưu cùng lúc thì người sau bị từ chối.',
        '-  Xóa phiếu báo thì phiếu nhập kho quay lại hàng chờ.',
        '-  Phiếu báo KHÔNG ghi tồn kho, không sinh bút toán.',
    )),
    ('7. Phân quyền cấp', L_(
        '-  "' + Q_XEM + '" — mức: Công ty / Tổng công ty (dùng chung với màn Phiếu nhập kho chờ báo thừa, thiếu).',
        '-  "' + Q_TAO + '": nút Tạo mới, lập phiếu báo.',
        '-  "' + Q_DUYET + '": Không duyệt, Xử lý phiếu Chờ xử lý; nhận thông báo Chờ duyệt.',
        '-  Người tạo phiếu (không cần quyền): Sửa, Xóa khi Đang tạo / Không duyệt. Menu không ẩn theo quyền. Super Admin có mọi quyền.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N": N = tổng phiếu báo khớp bộ lọc và phạm vi xem.',
        'Bảng Chi tiết: SL thiếu chữ đỏ, SL thừa chữ xanh; ô không có giá trị để trống.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        'Các bẫy dễ sai nhất của màn này, QA đọc trước khi test:',
        '-  Chọn file là tải lên NGAY; ở trang Sửa, xóa file đã lưu là gỡ NGAY (không chờ bấm Lưu).',
        '-  "Lưu" ở phiếu Không duyệt đưa phiếu về Đang tạo; "Lưu và gửi" đưa về Chờ xử lý.',
        '-  Thông báo Chờ duyệt chỉ tới người có quyền Duyệt CÙNG công ty VÀ đang quản lý phòng ban của người lập.',
        '-  Nút Xử lý mở màn của hệ thống quản lý kho cũ ở tab mới; trạng thái Đã xử lý do màn đó cập nhật.',
        '-  Số theo chuẩn quốc tế 1,234.5. Cột KQ thực tế, DNS check để trống cho tester điền.',
    )),
]

K = dict(
    menu=MENU,
    tieu_de='Danh sách phiếu báo hàng thừa, thiếu nhập kho',
    exp_mo_them=['Tiêu đề trang (thanh trên cùng) "Phiếu báo hàng thừa, thiếu nhập kho"'],
    exp_nut=['Thanh công cụ có: Tạo mới (chỉ khi có quyền Tạo), Xuất Excel, Cấu hình cột hiển thị',
             'Khối tìm kiếm có ô "Tìm theo số phiếu", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
             'Không có nút Import, In danh sách'],
    cot=['STT', 'Số phiếu', 'Ngày tạo', 'Phiếu nhập kho', 'Yêu cầu nhập', 'Nhà cung cấp', 'Số hợp đồng', 'Người tạo', 'Trạng thái', 'Hành động'],
    cot_an=[],
    tong_cot=10,
    cot_khoa=['STT', 'Số phiếu', 'Hành động'],
    cot_bo_thu='Nhà cung cấp',
    pre_du_lieu='TK-A vừa lập phiếu báo từ PNK-2, bấm Lưu và gửi.',
    exp_du_lieu=['Số phiếu dạng TPE_BHNK-<5 chữ số>, là liên kết; Phiếu nhập kho = PNK-2; Yêu cầu nhập, Số hợp đồng đúng theo PNK-2',
                 'Nhà cung cấp "CÔNG TY CỔ PHẦN VIỆT ĐỨC"; Người tạo dạng "Mã phòng ban - Họ tên" của TK-A',
                 'Trạng thái "Chờ xử lý" nền vàng'],
    trang_thai=[('Đang tạo', 'xám'), ('Chờ xử lý', 'vàng'), ('Đã xử lý', 'xanh lá'), ('Không duyệt', 'đỏ')],
    pre_rong='TK-Z chưa tạo phiếu báo nào, không có quyền nào.',
    rong_bang='Không có dữ liệu phù hợp.',
    rong_chan=None,
    sap_xep=['Số phiếu', 'Ngày tạo'],
    khong_sap_xep=['STT', 'Phiếu nhập kho', 'Yêu cầu nhập', 'Nhà cung cấp', 'Số hợp đồng', 'Người tạo', 'Trạng thái', 'Hành động'],
    ma='Số phiếu', vd_ma='TPE_BHNK-00021', vd_mot_phan='BHNK-0002', placeholder='Tìm theo số phiếu',
    loc_text=('Hàng hóa', 'Thấu kính', 'thau kinh'),
    loc_list=['Phiếu nhập kho', 'Yêu cầu nhập', 'Hợp đồng', 'Hàng hóa', 'Nhà cung cấp', 'Trạng thái', 'Người tạo', 'Ngày tạo', 'Công ty'],
    exp_mac_dinh_them=['Ô Công ty chỉ hiện với tài khoản xem mức Tổng công ty'],
    loc_chon=('Trạng thái', 'Chờ xử lý'),
    loc_ket_hop='Trạng thái = Chờ xử lý, Người tạo = TK-A, Ngày tạo = tháng hiện tại',
    td_rong='Trạng thái: Đã xử lý; Ngày tạo: hôm nay (chưa có phiếu nào xử lý hôm nay)',
    form_tao='Tạo phiếu báo hàng thừa, thiếu nhập kho', nut_quay_lai='Quay lại', truong_nhap_thu='Diễn giải',
    td_nhap_thu='Diễn giải: "Hàng về thiếu"', nut_luu_chinh='Lưu và gửi',
    exp_dong_thoi_them=['(Mỗi người chọn 1 phiếu nhập kho khác nhau: PNK-1 và PNK-2)'],
    lich_su_title='Lịch sử thay đổi: <số phiếu>', nut_lich_su='Lịch sử',
    excel=dict(title='Chọn trường xuất Excel', so_truong=8,
               truong=['Số phiếu', 'Ngày tạo', 'Phiếu nhập kho', 'Yêu cầu nhập', 'Nhà cung cấp', 'Số hợp đồng', 'Người tạo', 'Trạng thái'],
               mac_dinh='Mặc định tích sẵn cả 8 trường, dòng đếm "Đang chọn 8/8 trường"',
               file='danh_sach_phieu_bao_hang_thua_thieu_nhap_kho.xlsx', tieu_de='DANH SÁCH PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO',
               bo_thu='Số hợp đồng', exp_them=['Cột STT đứng đầu file; Trạng thái ghi bằng chữ (Đang tạo / Chờ xử lý…)'],
               rong=['Báo "Không có dữ liệu để xuất"', 'KHÔNG tải file nào']),
    pre_an_nut='Có phiếu báo ở cả 4 trạng thái; TK-A là người tạo phiếu Đang tạo; TK-D có quyền Duyệt.',
    exp_an_nut=['TK-A: phiếu Đang tạo / Không duyệt của mình có Sửa, Xóa; phiếu Chờ xử lý / Đã xử lý chỉ có Lịch sử',
                'TK-D: phiếu Chờ xử lý có Xử lý, Lịch sử (chân trang Chi tiết: Xử lý, Không duyệt); phiếu Đang tạo của TK-A không có Sửa / Xóa'],
    pre_url='TK-Z (không quyền) biết đường dẫn trang Chi tiết của phiếu do TK-A tạo.',
    exp_url=['Chuyển sang trang "Không tìm thấy", không lộ dữ liệu phiếu'],
    pre_doi_quyen='TK-D có quyền Duyệt; phiếu Chờ xử lý đang mở trang Chi tiết.', man_doi_quyen='cửa sổ Không duyệt của phiếu',
    nut_doi_quyen='Không duyệt (đã nhập lý do)',
    exp_doi_quyen=['Hệ thống từ chối (phiếu không còn trong phạm vi / không có quyền), phiếu vẫn Chờ xử lý', 'Không gửi thông báo'],
    cot_keo='Trạng thái',
)

K['hien_thi_rieng'] = [
    C('Liên kết ở cột Phiếu nhập kho, Yêu cầu nhập, Số hợp đồng', 'P1', 'Có phiếu TPE_BHNK-00021.',
      ['1. Bấm mã ở cột Phiếu nhập kho', '2. Bấm mã ở cột Yêu cầu nhập', '3. Bấm số ở cột Số hợp đồng'], '',
      ['Mỗi lần mở 1 tab mới: chi tiết phiếu nhập kho PNK-00339 / chi tiết yêu cầu nhập PYCNH-00416 / hợp đồng DEMARK 0825 HN (màn của hệ thống quản lý kho cũ)',
       'Danh sách ở tab cũ giữ nguyên']),
    C('Bấm Số phiếu mở trang Chi tiết', 'P0', 'Có phiếu TPE_BHNK-00021.', ['1. Bấm số phiếu TPE_BHNK-00021'], '',
      ['Mở trang "Chi tiết phiếu báo hàng thừa, thiếu: TPE_BHNK-00021" ở cùng tab']),
    C('Ô trống để trống', 'P2', 'Có phiếu mà phiếu nhập kho không có nhà cung cấp (vd TPE_BHNK-00020).', ['1. Xem cột Nhà cung cấp'], '',
      ['Ô để TRỐNG, không in dấu "-" hay "null"']),
]

K['loc_rieng'] = [
    C('Lọc theo Phiếu nhập kho', 'P0', 'Có phiếu báo của PNK-00339.', ['1. Mở Tìm kiếm nâng cao', '2. Nhập "00339" ở ô Phiếu nhập kho', '3. Nhấn Enter'],
      'Phiếu nhập kho: 00339', ['Chỉ còn phiếu báo có Phiếu nhập kho chứa "00339"', 'Gõ chưa Enter thì chưa lọc']),
    C('Lọc theo Yêu cầu nhập', 'P1', 'Có phiếu báo của PYCNH-00416.', ['1. Nhập "PYCNH-00416" ở ô Yêu cầu nhập, Enter'], '',
      ['Chỉ còn phiếu có Yêu cầu nhập khớp']),
    C('Lọc theo Hợp đồng', 'P1', 'Có phiếu số hợp đồng "DEMARK 0825 HN".', ['1. Nhập "DEMARK" ở ô Hợp đồng, Enter'], '',
      ['Chỉ còn phiếu có Số hợp đồng chứa "DEMARK"']),
    C('Lọc theo Hàng hóa', 'P0', 'Phiếu TPE_BHNK-00021 có hàng mã DMK-TRUMPFD96X3.', ['1. Nhập "TRUMPFD96X3" ở ô Hàng hóa, Enter'], '',
      ['Ra các phiếu có ít nhất 1 dòng hàng có mã hoặc tên chứa từ khóa, gồm TPE_BHNK-00021']),
    C('Lọc theo Nhà cung cấp', 'P1', 'Có phiếu của RENQIU FIRLEND WELDING EQUIPMENT CO.,LTD.', ['1. Chọn Nhà cung cấp = RENQIU FIRLEND…'], '',
      ['Danh sách chọn chỉ gồm nhà cung cấp có trên phiếu trong phạm vi; nhà cung cấp đã khóa có biểu tượng ổ khóa',
       'Bảng lọc ngay, chỉ còn phiếu của nhà cung cấp đó']),
    C('Lọc theo Trạng thái', 'P0', 'Có phiếu ở nhiều trạng thái.', ['1. Chọn lần lượt từng giá trị ở ô Trạng thái'], '',
      ['Danh sách chọn có đúng 4 giá trị: Đang tạo, Chờ xử lý, Đã xử lý, Không duyệt', 'Mỗi lần chỉ còn phiếu đúng trạng thái']),
    C('Lọc theo Người tạo', 'P1', 'Có phiếu do 2 người tạo.', ['1. Chọn 1 người ở ô Người tạo'], '',
      ['Danh sách chọn dạng "Mã phòng ban - Họ tên", chỉ gồm người đã lập phiếu trong phạm vi', 'Chỉ còn phiếu do người đó tạo']),
    C('Lọc theo khoảng Ngày tạo', 'P0', 'Có phiếu tạo ngày 23/10/2026 và 24/10/2026.', ['1. Chọn Ngày tạo từ 23/10/2026 đến 23/10/2026'], '',
      ['Chỉ còn phiếu tạo trong ngày 23/10/2026 (tính cả 2 đầu mút)']),
    C('Lọc theo Công ty', 'P1', 'TK-ALL; có phiếu của 2 công ty.', ['1. Đăng nhập TK-ALL', '2. Chọn Công ty = TPE'], '',
      ['Ô Công ty hiện dạng "Mã - Tên công ty"', 'Chỉ còn phiếu thuộc công ty TPE']),
]

# ------------------------------------------------------------------ III. THÊM MỚI
S_THEM = [
    C('Mở trang Tạo phiếu báo', 'P0', 'TK-A có quyền Tạo.', ['1. Vào menu ' + MENU, '2. Bấm Tạo mới'], '',
      ['Mở trang "Tạo phiếu báo hàng thừa, thiếu nhập kho"', 'Góc phải khối Thông tin chung: "<tên TK-A> - <ngày giờ hiện tại>"',
       'Có các khối Thông tin chung, File đính kèm, Chi tiết; bảng Chi tiết ghi "Chọn phiếu nhập kho để nạp hàng hóa lệch số lượng"',
       'Chân trang: Lưu, Lưu và gửi, Lưu và tiếp tục, Quay lại']),
    C('Mở cửa sổ Chọn phiếu nhập kho', 'P0', 'Đang ở trang Tạo; phạm vi TK-A có PNK-1, PNK-2 chờ báo.', ['1. Bấm vào ô Phiếu nhập kho'], '',
      ['Mở cửa sổ "Chọn phiếu nhập kho", dòng phụ "Phiếu nhập kho đã hạch toán có hàng thừa / thiếu, chưa có phiếu báo"',
       'Cột: STT, Mã phiếu, Loại, Nhà cung cấp, Phiếu ĐNNK, Ngày tạo; mặc định 10 dòng/trang, mới nhất trên cùng',
       'Danh sách trùng khớp với màn ' + MENU_CHO + ' của cùng tài khoản']),
    C('Tìm phiếu nhập kho trong cửa sổ chọn', 'P1', 'Đang mở cửa sổ chọn.', ['1. Gõ "02741" ở ô Mã phiếu', '2. Nhấn Enter', '3. Bấm Làm mới'], '',
      ['Bước 2: chỉ còn PNK-02741', 'Bước 3: ô tìm trống, hiện lại đủ danh sách']),
    C('Sắp xếp trong cửa sổ chọn', 'P2', 'Đang mở cửa sổ chọn, có từ 3 phiếu.', ['1. Bấm tiêu đề Mã phiếu', '2. Bấm tiêu đề Ngày tạo'], '',
      ['Danh sách đổi thứ tự theo cột đã bấm; các cột khác không sắp xếp được']),
    C('Bấm vào chữ Mã phiếu trong cửa sổ chọn', 'P2', 'Đang mở cửa sổ chọn.', ['1. Bấm vào chữ PNK-02741 ở cột Mã phiếu'], '',
      ['Mở chi tiết phiếu nhập kho PNK-02741 ở tab mới', 'Cửa sổ chọn vẫn mở, CHƯA chọn phiếu']),
    C('Chọn phiếu nhập kho thì tự điền dữ liệu', 'P0', 'Đang mở cửa sổ chọn.', ['1. Bấm vào ô Loại của dòng PNK-02741'], 'PNK-1 (PNK-02741)',
      ['Cửa sổ đóng; ô Phiếu nhập kho = PNK-02741', 'Yêu cầu nhập = PYCNH-04259, Số hợp đồng = DHNT-000522 (đều là liên kết); Nhà cung cấp trống',
       'Bảng Chi tiết có dòng "Bia Heineken (250ml/lon)", SL đề nghị nhập 20, SL thực nhập 0, SL thiếu 20 (chữ đỏ), SL thừa trống']),
    C('Bảng Chi tiết chỉ gồm dòng lệch, có cả thiếu và thừa', 'P0', 'PNK-3 có 3 dòng: 20/10 (thiếu), 10/20 (thừa), 5/5 (khớp).',
      ['1. Chọn PNK-3', '2. Đọc bảng Chi tiết'], '',
      ['Chỉ 2 dòng: dòng 1 SL thiếu 10 (đỏ), SL thừa trống; dòng 2 SL thừa 10 (xanh), SL thiếu trống', 'Dòng khớp 5/5 KHÔNG hiện']),
    C('Lệch phần thập phân không tính là lệch', 'P2', 'PNK-4 có 1 dòng SL đề nghị 2.5, thực nhập 2 (phần nguyên bằng nhau) và 1 dòng 135/0.',
      ['1. Mở cửa sổ chọn phiếu nhập kho', '2. Tìm PNK-4, chọn'], '',
      ['PNK-4 có trong danh sách nhờ dòng 135/0', 'Lưu ý: dòng 2.5/2 so phần nguyên coi là khớp — ghi nhận đúng như quy tắc hệ thống']),
    C('Bỏ chọn phiếu nhập kho bằng nút ×', 'P1', 'Đã chọn PNK-1, đã nhập Diễn giải.', ['1. Bấm × trong ô Phiếu nhập kho'], '',
      ['Ô Phiếu nhập kho trống; Yêu cầu nhập, Số hợp đồng, Nhà cung cấp, bảng Chi tiết bị xóa', 'Diễn giải và file đã chọn GIỮ NGUYÊN']),
    C('Đổi sang phiếu nhập kho khác', 'P1', 'Đã chọn PNK-1.', ['1. Bấm lại ô Phiếu nhập kho', '2. Chọn PNK-2'], '',
      ['Dữ liệu và bảng Chi tiết thay bằng của PNK-2', 'Nhà cung cấp = CÔNG TY CỔ PHẦN VIỆT ĐỨC']),
    C('Bấm Lưu khi chưa nhập gì', 'P0', 'Trang Tạo trống.', ['1. Bấm Lưu'], '',
      ['Toast "' + CHUA_DU + '"', 'Dưới ô Phiếu nhập kho: "' + E_PNK + '"', 'Dưới ô Diễn giải: "' + E_DG + '"',
       'Dưới khối File đính kèm: "' + E_FILE + '", khối viền đỏ', 'Không lưu; màn cuộn tới ô lỗi đầu tiên']),
    C('Thiếu Phiếu nhập kho thì bị chặn', 'P0', 'Đã nhập Diễn giải, đã đính kèm file.', ['1. Bấm Lưu và gửi'], '',
      ['Chỉ báo lỗi dưới ô Phiếu nhập kho: "' + E_PNK + '"', 'Không lưu']),
    C('Thiếu Diễn giải thì bị chặn', 'P0', 'Đã chọn PNK-1, đã đính kèm file.', ['1. Để trống Diễn giải', '2. Bấm Lưu'], '',
      ['Dưới ô Diễn giải: "' + E_DG + '"', 'Không lưu']),
    C('Diễn giải chỉ có khoảng trắng', 'P1', 'Đã chọn PNK-1, có file.', ['1. Gõ 5 dấu cách vào Diễn giải', '2. Bấm Lưu'], 'Diễn giải: "     "',
      ['Báo "' + E_DG + '"', 'Không lưu']),
    C('Diễn giải đúng 255 ký tự và quá 255 ký tự', 'P1', 'Đã chọn PNK-1, có file.',
      ['1. Dán chuỗi 255 ký tự vào Diễn giải', '2. Dán thêm 1 ký tự', '3. Bấm Lưu'], 'Chuỗi 255 ký tự có dấu tiếng Việt',
      ['Bước 2: ô không nhận thêm ký tự thứ 256', 'Bước 3: lưu thành công, mở lại thấy đủ 255 ký tự']),
    C('Diễn giải có ký tự đặc biệt và nhiều dòng', 'P2', 'Đã chọn PNK-1, có file.', ['1. Nhập Diễn giải ở Test data', '2. Lưu, mở Chi tiết'],
      'Diễn giải: "Thiếu 20 thùng <b>bia</b> & 1/2 \'lô\'"\n(xuống dòng ở giữa)', ['Lưu thành công', 'Chi tiết hiện nguyên văn, thẻ <b> không bị chạy']),
    C('Lỗi biến mất khi nhập lại đúng', 'P1', 'Đang có lỗi đỏ ở Diễn giải và Phiếu nhập kho.', ['1. Gõ Diễn giải', '2. Chọn phiếu nhập kho'], '',
      ['Lỗi dưới từng ô mất ngay khi nhập / chọn, không cần bấm Lưu lại']),
    C('Thiếu file đính kèm thì bị chặn', 'P0', 'Đã chọn PNK-1, có Diễn giải, chưa có file.', ['1. Bấm Lưu'], '',
      ['Dưới khối File đính kèm: "' + E_FILE + '"', 'Không lưu']),
    C('Thêm file hợp lệ', 'P0', 'Đang ở trang Tạo.', ['1. Bấm "Thêm tài liệu"', '2. Bấm "Chọn tệp", chọn bien-ban.pdf'], 'bien-ban.pdf (200KB)',
      ['Dòng đang tải "Đang tải lên bien-ban.pdf..." rồi hiện tên file, dung lượng "200 KB"', 'Có nút Xem trước, Tải xuống, Thay đổi, Xóa trên dòng file']),
    C('Rê chuột vào nút chọn file thấy định dạng cho phép', 'P2', 'Đang ở trang Tạo.', ['1. Rê chuột vào "Thêm tài liệu" / "Chọn tệp"'], '',
      ['Hiện gợi ý "Chấp nhận ppt, pptx, doc, docx, pdf, xls, xlsx, jpg, jpeg, png, zip — tối đa 15MB/file"']),
    C('File sai định dạng bị từ chối', 'P0', 'Đang ở trang Tạo.', ['1. Chọn tệp file.exe'], 'file.exe',
      ['Báo đỏ ở khối file: "File "file.exe" không thuộc định dạng cho phép"', 'File không được thêm']),
    C('File quá 15MB bị từ chối', 'P1', 'Đang ở trang Tạo.', ['1. Chọn tệp file-lon.pdf'], 'file-lon.pdf (16MB)',
      ['Báo "File "file-lon.pdf" vượt quá 15MB"', 'File không được thêm']),
    C('Thêm nhiều file, đổi và bỏ file chưa lưu', 'P1', 'Đã thêm 2 file.', ['1. Bấm Thay đổi ở file 1, chọn file khác', '2. Bấm Xóa ở file 2'], '',
      ['File 1 được thay tại chỗ, không nhảy xuống cuối', 'File 2 bị bỏ khỏi danh sách, không hỏi xác nhận']),
    C('Lưu ở trạng thái Đang tạo', 'P0', 'Đã chọn PNK-1, nhập Diễn giải, có 1 file.', ['1. Bấm Lưu'], 'Diễn giải: "Hàng về thiếu 20 thùng"',
      ['Toast "Lưu thành công."; về danh sách', 'Phiếu mới đứng đầu, số phiếu TPE_BHNK-<5 chữ số>, trạng thái Đang tạo',
       'Không gửi thông báo cho người duyệt', 'Lịch sử có mốc Tạo mới']),
    C('Lưu và gửi thì phiếu sang Chờ xử lý', 'P0', 'Đã chọn PNK-2, nhập đủ, có file.', ['1. Bấm Lưu và gửi'], '',
      ['Toast "Lưu và gửi thành công."; về danh sách', 'Phiếu mới trạng thái Chờ xử lý (nền vàng)', 'Không có nút Sửa / Xóa trên dòng phiếu này']),
    C('Lưu và tiếp tục', 'P1', 'Đã chọn PNK-1, nhập đủ, có file.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Toast "Lưu thành công."; vẫn ở trang Tạo, form trống hoàn toàn (kể cả file)', 'Phiếu vừa lưu ở trạng thái Đang tạo']),
    C('Vào trang Tạo từ màn hàng chờ', 'P0', 'TK-A; PNK-2 đang ở màn ' + MENU_CHO + '.',
      ['1. Vào menu ' + MENU_CHO, '2. Bấm nút Báo hàng thừa thiếu ở dòng PNK-02667'], '',
      ['Mở trang Tạo với ô Phiếu nhập kho = PNK-02667, Nhà cung cấp, bảng Chi tiết điền sẵn', 'Diễn giải trống, chưa có file']),
    C('Lưu và tiếp tục khi vào từ hàng chờ', 'P2', 'Đang ở trang Tạo mở từ hàng chờ, nhập đủ.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Lưu thành công; trang Tạo mở lại TRỐNG, không còn chọn sẵn PNK-02667']),
    C('Phiếu nhập kho vừa được người khác báo', 'P0', 'TK-A và TK-A2 (cùng quyền) cùng mở trang Tạo, cùng chọn PNK-1.',
      ['1. TK-A2 bấm Lưu trước', '2. TK-A bấm Lưu'], '',
      ['TK-A bị từ chối, dưới ô Phiếu nhập kho: "' + E_TAKEN + '"', 'Chỉ có 1 phiếu báo cho PNK-1']),
    C('Mở trang Tạo từ hàng chờ khi phiếu nhập kho đã có phiếu báo', 'P1', 'Tab 1 mở màn hàng chờ cũ có PNK-1; tab 2 đã lập phiếu báo cho PNK-1.',
      ['1. Ở tab 1 bấm Báo hàng thừa thiếu của PNK-1'], '',
      ['Toast "Phiếu nhập kho không còn chờ báo thừa, thiếu hoặc bạn không có quyền."', 'Ô Phiếu nhập kho trống']),
    C('Không ghi tồn kho, không sinh bút toán khi lưu', 'P0', 'Ghi lại tồn kho của hàng trong PNK-1 ở báo cáo tồn kho.',
      ['1. Lập phiếu báo PNK-1, Lưu và gửi', '2. Xem lại tồn kho của hàng đó'], '', ['Tồn kho KHÔNG đổi']),
    C('Thông báo Chờ duyệt gửi đúng người', 'P0', 'TK-D, TK-D2 có quyền Duyệt cùng công ty; chỉ TK-D quản lý phòng của TK-A.',
      ['1. TK-A lập phiếu, bấm Lưu và gửi', '2. Kiểm chuông thông báo của TK-D, TK-D2'], '',
      ['TK-D nhận "[BHNK] Chờ duyệt: <số phiếu>. Người gửi: <tên TK-A>. Phiếu nhập kho: PNK-…"', 'TK-D2 KHÔNG nhận',
       'Bấm thông báo mở trang Chi tiết phiếu']),
] + them_moi_dong_form(K)

# ------------------------------------------------------------------ IV. CHỈNH SỬA
S_SUA = [
    C('Mở trang Sửa phiếu Đang tạo', 'P0', 'TK-A có phiếu Đang tạo TPE_BHNK-00020.', ['1. Bấm Sửa ở dòng phiếu'], '',
      ['Mở trang "Sửa phiếu báo hàng thừa, thiếu: TPE_BHNK-00020"', 'Phiếu nhập kho, Yêu cầu nhập, Số hợp đồng, Nhà cung cấp, bảng Chi tiết hiện đúng, KHÔNG sửa được',
       'Ô Phiếu nhập kho có biểu tượng chữ i "Phiếu nhập kho không đổi được sau khi tạo phiếu báo."',
       'Diễn giải điền sẵn; file đã lưu hiện kèm Xem trước, Tải xuống, Xóa', 'Chân trang: Lưu, Lưu và gửi, Quay lại (không có Lưu và tiếp tục)']),
    C('Sửa Diễn giải rồi Lưu', 'P0', 'Đang ở trang Sửa phiếu Đang tạo.', ['1. Đổi Diễn giải', '2. Bấm Lưu'], 'Diễn giải mới: "Thiếu 10 cái"',
      ['Toast "Lưu thành công."; về danh sách', 'Phiếu vẫn Đang tạo', 'Lịch sử thêm mốc Thay đổi thông tin: Diễn giải cũ > mới']),
    C('Sửa rồi Lưu và gửi', 'P0', 'Đang ở trang Sửa phiếu Đang tạo.', ['1. Bấm Lưu và gửi'], '',
      ['Toast "Lưu và gửi thành công."', 'Phiếu sang Chờ xử lý; lịch sử có mốc Thay đổi trạng thái Đang tạo > Chờ xử lý', 'Người duyệt nhận thông báo Chờ duyệt']),
    C('Không đổi gì mà bấm Lưu', 'P2', 'Đang ở trang Sửa, chưa đổi.', ['1. Bấm Lưu'], '',
      ['Lưu thành công', 'Lịch sử KHÔNG thêm mốc Thay đổi thông tin']),
    C('Xóa Diễn giải khi sửa thì bị chặn', 'P1', 'Đang ở trang Sửa.', ['1. Xóa hết Diễn giải', '2. Bấm Lưu'], '',
      ['Báo "' + E_DG + '"; toast "' + CHUA_DU + '"', 'Không lưu']),
    C('Thêm file khi sửa', 'P1', 'Đang ở trang Sửa phiếu có 1 file.', ['1. Thêm tài liệu, chọn bien-ban.pdf', '2. Bấm Lưu'], '',
      ['Phiếu có 2 file', 'Lịch sử ghi "File đính kèm thêm mới: bien-ban.pdf"']),
    C('Xóa file đã lưu khi sửa', 'P0', 'Phiếu Đang tạo có 2 file.', ['1. Bấm Xóa ở dòng file đã lưu', '2. Đọc hộp xác nhận', '3. Bấm xác nhận', '4. Bấm Quay lại, chọn Thoát'], '',
      ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa file đính kèm này?"', 'Bước 3: toast "Xóa file thành công", file mất khỏi danh sách',
       'Lưu ý: file bị gỡ NGAY, dù bước 4 thoát không lưu thì mở lại phiếu vẫn mất file đó; lịch sử ghi file bị xóa']),
    C('Sửa phiếu không bắt buộc thêm file mới', 'P2', 'Phiếu Đang tạo có 1 file đã lưu.', ['1. Đổi Diễn giải, bấm Lưu'], '',
      ['Lưu thành công, không báo thiếu file']),
    C('Sửa phiếu Không duyệt thấy lý do', 'P0', 'Phiếu của TK-A bị Không duyệt lý do "Thiếu biên bản kiểm đếm".', ['1. Bấm Sửa'], '',
      ['Có ô "Lý do không duyệt" (chỉ đọc): "Thiếu biên bản kiểm đếm (<tên người duyệt> – <dd/mm/yyyy hh:mm>)"']),
    C('Lưu phiếu Không duyệt thì về Đang tạo', 'P1', 'Phiếu Không duyệt của TK-A.', ['1. Sửa Diễn giải', '2. Bấm Lưu'], '',
      ['Phiếu chuyển Đang tạo; lịch sử có Thay đổi trạng thái Không duyệt > Đang tạo']),
    C('Lưu và gửi phiếu Không duyệt thì về Chờ xử lý', 'P0', 'Phiếu Không duyệt của TK-A.', ['1. Bổ sung file', '2. Bấm Lưu và gửi'], '',
      ['Phiếu chuyển Chờ xử lý', 'Người duyệt nhận lại thông báo Chờ duyệt']),
    C('Người khác không sửa được phiếu', 'P0', 'TK-CTY xem được phiếu Đang tạo của TK-A.', ['1. Đăng nhập TK-CTY, xem dòng phiếu', '2. Dán đường dẫn trang Sửa của phiếu'], '',
      ['Không có nút Sửa / Xóa', 'Bước 2: tự chuyển sang trang Chi tiết, không sửa được']),
    C('Mở trang Sửa của phiếu Chờ xử lý', 'P1', 'TK-A có phiếu Chờ xử lý.', ['1. Dán đường dẫn trang Sửa của phiếu'], '',
      ['Tự chuyển sang trang Chi tiết, không có nút Sửa']),
    C('Phiếu vừa được gửi ở tab khác', 'P1', 'TK-A mở trang Sửa phiếu Đang tạo ở 2 tab.', ['1. Tab 1 bấm Lưu và gửi', '2. Tab 2 sửa Diễn giải, bấm Lưu'], '',
      ['Tab 2 báo "' + E_DOI_TT + '"', 'Không lưu thay đổi của tab 2']),
    C('Quay lại khi đã sửa', 'P1', 'Đang ở trang Sửa, đã đổi Diễn giải.', ['1. Bấm Quay lại', '2. Bấm Ở lại', '3. Bấm Quay lại, bấm Thoát'], '',
      ['Bước 1: hộp "Thông tin chưa lưu"', 'Bước 2: ở lại, dữ liệu còn', 'Bước 3: về danh sách, phiếu không đổi']),
]

# ------------------------------------------------------------------ V. XÓA
S_XOA = [
    C('Mở hộp xác nhận xóa', 'P0', 'TK-A có phiếu Đang tạo.', ['1. Bấm Xóa ở dòng phiếu'], '',
      ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?" với nút Xóa, Hủy']),
    C('Bấm Hủy thì không xóa', 'P1', 'Đang mở hộp xác nhận.', ['1. Bấm Hủy'], '', ['Hộp đóng, phiếu còn nguyên']),
    C('Xóa phiếu Đang tạo', 'P0', 'TK-A có phiếu Đang tạo của PNK-1.', ['1. Bấm Xóa, bấm Xóa ở hộp'], '',
      ['Toast "Xóa thành công."; danh sách tải lại, không còn phiếu', 'PNK-1 xuất hiện lại ở màn ' + MENU_CHO]),
    C('Xóa phiếu Không duyệt từ trang Chi tiết', 'P1', 'TK-A có phiếu Không duyệt.', ['1. Mở Chi tiết, bấm Xóa', '2. Xác nhận'], '',
      ['Xóa thành công, về danh sách']),
    C('Phiếu Chờ xử lý / Đã xử lý không có nút Xóa', 'P0', 'TK-A có phiếu Chờ xử lý và Đã xử lý.', ['1. Xem cột Hành động và trang Chi tiết'], '',
      ['Không có nút Xóa (ẩn hẳn)']),
    C('Phiếu vừa được gửi ở tab khác thì không xóa được', 'P1', 'Phiếu Đang tạo mở ở 2 tab.', ['1. Tab 1 Sửa > Lưu và gửi', '2. Tab 2 bấm Xóa, xác nhận'], '',
      ['Báo "' + E_DOI_TT + '"', 'Phiếu không bị xóa']),
    C('Xóa ghi lịch sử', 'P2', 'Vừa xóa phiếu X.', ['1. Quản trị kiểm nhật ký lịch sử của phiếu X'], '', ['Có mốc Xóa do TK-A thực hiện']),
]

# ------------------------------------------------------------------ VI. GỬI DUYỆT
S_GUI = [
    C('Gửi ngay khi lập phiếu', 'P0', 'Trang Tạo đã nhập đủ.', ['1. Bấm Lưu và gửi'], '',
      ['Phiếu vào thẳng Chờ xử lý (không qua Đang tạo)', 'Lịch sử chỉ có mốc Tạo mới']),
    C('Gửi phiếu Đang tạo', 'P0', 'Phiếu Đang tạo của TK-A.', ['1. Mở Sửa', '2. Bấm Lưu và gửi'], '',
      ['Phiếu sang Chờ xử lý', 'Lịch sử thêm Thay đổi trạng thái Đang tạo > Chờ xử lý']),
    C('Người duyệt thấy phiếu vừa gửi', 'P0', 'TK-D có quyền Duyệt (không có quyền Xem); TK-A vừa gửi phiếu.', ['1. TK-D vào menu ' + MENU], '',
      ['Danh sách của TK-D có phiếu Chờ xử lý của TK-A với nút Xử lý, Lịch sử', 'TK-D không thấy phiếu Đang tạo của TK-A']),
    C('Thông báo khi người lập không thuộc phòng nào người duyệt quản lý', 'P2', 'Chỉ TK-D2 có quyền Duyệt và không quản lý phòng của TK-A.',
      ['1. TK-A gửi phiếu', '2. Kiểm chuông TK-D2'], '', ['TK-D2 không nhận thông báo nhưng vẫn thấy phiếu trong danh sách (Chờ xử lý cùng công ty)']),
    C('Gửi lại phiếu Không duyệt', 'P0', 'Phiếu Không duyệt của TK-A.', ['1. Sửa, bấm Lưu và gửi'], '',
      ['Phiếu sang Chờ xử lý; người duyệt nhận thông báo lần nữa']),
]

# ------------------------------------------------------------------ VII. DUYỆT PHIẾU (Xử lý)
S_DUYET = [
    C('Nút Xử lý chỉ với phiếu Chờ xử lý và người có quyền Duyệt', 'P0', 'TK-D có quyền Duyệt; có phiếu ở 4 trạng thái.', ['1. TK-D xem cột Hành động', '2. Mở Chi tiết phiếu Chờ xử lý'], '',
      ['Chỉ phiếu Chờ xử lý có nút Xử lý (biểu tượng dụng cụ)', 'Chân trang Chi tiết: Xử lý, Không duyệt, Quay lại']),
    C('Bấm Xử lý mở màn lập phiếu xử lý', 'P0', 'TK-D; phiếu TPE_BHNK-00021 Chờ xử lý.', ['1. Bấm Xử lý ở dòng phiếu'], '',
      ['Mở tab mới tới màn Lập phiếu xử lý hàng thiếu nhập kho (hệ thống quản lý kho cũ), đã gắn sẵn phiếu báo', 'Danh sách tab cũ giữ nguyên']),
    C('Lập phiếu xử lý thì phiếu báo sang Đã xử lý', 'P0', 'TK-D đã lập phiếu xử lý từ phiếu báo ở màn hệ thống cũ.', ['1. Quay lại danh sách, bấm Tìm kiếm'], '',
      ['Phiếu báo trạng thái Đã xử lý (xanh lá), chỉ còn nút Lịch sử']),
    C('Người tạo không có quyền Duyệt không thấy Xử lý', 'P1', 'TK-A (không quyền Duyệt) có phiếu Chờ xử lý.', ['1. Xem dòng và trang Chi tiết'], '',
      ['Không có Xử lý, Không duyệt']),
]

# ------------------------------------------------------------------ VIII. KHÔNG DUYỆT
S_KD = [
    C('Mở cửa sổ Không duyệt', 'P0', 'TK-D mở Chi tiết phiếu Chờ xử lý.', ['1. Bấm Không duyệt'], '',
      ['Mở cửa sổ "Không duyệt phiếu báo hàng thừa, thiếu" với ô "Lý do không duyệt *" (placeholder "Nhập lý do không duyệt"), con trỏ đặt sẵn trong ô',
       'Nút Không duyệt (đỏ), Hủy']),
    C('Không nhập lý do thì bị chặn', 'P0', 'Đang mở cửa sổ Không duyệt.', ['1. Bấm Không duyệt'], '',
      ['Dưới ô báo đỏ "' + E_LD + '"', 'Cửa sổ không đóng, phiếu vẫn Chờ xử lý']),
    C('Lý do chỉ có khoảng trắng', 'P1', 'Đang mở cửa sổ.', ['1. Gõ 3 dấu cách', '2. Bấm Không duyệt'], '', ['Báo "' + E_LD + '"']),
    C('Lý do tối đa 255 ký tự', 'P2', 'Đang mở cửa sổ.', ['1. Dán chuỗi 300 ký tự'], '', ['Ô chỉ nhận 255 ký tự']),
    C('Không duyệt thành công', 'P0', 'Đang mở cửa sổ.', ['1. Nhập lý do', '2. Bấm Không duyệt'], 'Lý do: "Thiếu biên bản kiểm đếm"',
      ['Toast "Không duyệt thành công."; về danh sách', 'Phiếu sang Không duyệt (đỏ)', 'Chi tiết hiện "Lý do không duyệt: Thiếu biên bản kiểm đếm (<tên TK-D> - <thời điểm>)"',
       'Lịch sử có mốc Không duyệt: Chờ xử lý > Không duyệt kèm lý do']),
    C('Người tạo nhận thông báo Không duyệt', 'P0', 'TK-D vừa không duyệt phiếu của TK-A.', ['1. TK-A xem chuông thông báo', '2. Bấm thông báo'], '',
      ['Có "[BHNK] Không duyệt: <số phiếu>. Người duyệt: <tên TK-D>. Lý do: Thiếu biên bản kiểm đếm"', 'Bấm mở trang Chi tiết phiếu']),
    C('Bấm Hủy thì không đổi', 'P1', 'Đang mở cửa sổ, đã nhập lý do.', ['1. Bấm Hủy'], '', ['Cửa sổ đóng, phiếu vẫn Chờ xử lý']),
    C('Phiếu vừa được xử lý ở nơi khác', 'P1', 'TK-D mở cửa sổ Không duyệt; người khác vừa lập phiếu xử lý (phiếu Đã xử lý).', ['1. Nhập lý do, bấm Không duyệt'], '',
      ['Báo "' + E_DOI_TT + '"', 'Phiếu giữ Đã xử lý']),
    C('Bấm Không duyệt 2 lần liên tục', 'P2', 'Đang mở cửa sổ, đã nhập lý do.', ['1. Bấm Không duyệt 2 lần thật nhanh'], '',
      ['Chỉ 1 mốc Không duyệt trong lịch sử, chỉ 1 thông báo']),
]

K['lich_su_rieng'] = [
    C('Phiếu chưa có mốc Tạo mới được ghi vẫn hiện Tạo mới', 'P2', 'Phiếu TPE_BHNK-00001 lập trước khi có ghi lịch sử.', ['1. Mở Lịch sử phiếu'], '',
      ['Có mốc Tạo mới với người tạo và ngày tạo của phiếu; danh sách không trống']),
    C('Lịch sử file đính kèm', 'P1', 'Phiếu TPE_BHNK-00020 đã thêm 1 file sau khi tạo.', ['1. Mở Lịch sử phiếu'], '',
      ['Mốc Thay đổi thông tin ghi "File đính kèm thêm mới: <tên file>", tên file là liên kết mở file']),
    C('Tiêu đề cửa sổ Lịch sử', 'P2', 'Có phiếu TPE_BHNK-00020.', ['1. Bấm Lịch sử ở dòng phiếu'], '', ['Tiêu đề "Lịch sử thay đổi: TPE_BHNK-00020"']),
]

# ------------------------------------------------------------------ XII. XEM CHI TIẾT
S_XEM = [
    C('Xem chi tiết phiếu Chờ xử lý', 'P0', 'TK-D; phiếu TPE_BHNK-00021.', ['1. Bấm số phiếu'], '',
      ['Tiêu đề "Chi tiết phiếu báo hàng thừa, thiếu: TPE_BHNK-00021"', 'Góc phải: "DNS Admin - 26/10/2026 13:48" (người tạo - ngày tạo)',
       'Mọi ô chỉ đọc; Phiếu nhập kho PNK-00339, Yêu cầu nhập PYCNH-00416, Số hợp đồng DEMARK 0825 HN là liên kết',
       'Bảng Chi tiết: dòng 1 SL thiếu 10 (đỏ), dòng 2 SL thừa 10 (xanh)', 'Khối File đính kèm chỉ có Xem trước, Tải xuống; khối Lịch sử thu gọn']),
    C('Xem chi tiết phiếu Đã xử lý', 'P1', 'Phiếu TPE_BHNK-00019.', ['1. Bấm số phiếu'], '', ['Chân trang chỉ có Quay lại']),
    C('Xem trước và tải file đính kèm', 'P1', 'Phiếu có file pdf.', ['1. Bấm Xem trước', '2. Bấm Tải xuống'], '',
      ['Bước 1: cửa sổ xem trước nội dung pdf', 'Bước 2: tải đúng file']),
    C('Mở khối Lịch sử', 'P1', 'Đang ở Chi tiết.', ['1. Bấm "Xem lịch sử"', '2. Bấm "Thu gọn"'], '', ['Khối mở ra danh sách mốc; bấm lại thì thu gọn']),
    C('Phiếu không tồn tại', 'P1', '—', ['1. Dán đường dẫn trang Chi tiết với số không tồn tại'], '', ['Chuyển sang trang "Không tìm thấy"']),
    C('Quay lại giữ bộ lọc', 'P2', 'Danh sách đang lọc Trạng thái = Chờ xử lý.', ['1. Mở Chi tiết 1 phiếu', '2. Bấm Quay lại'], '', ['Về danh sách, bộ lọc giữ nguyên']),
]

# ------------------------------------------------------------------ RÀNG BUỘC
S_RB = [
    C('Lập phiếu báo thì phiếu nhập kho rời hàng chờ', 'P0', 'PNK-1 đang ở màn ' + MENU_CHO + '.', ['1. Lập phiếu báo cho PNK-1, bấm Lưu', '2. Mở lại màn hàng chờ'], '',
      ['PNK-1 KHÔNG còn ở hàng chờ (dù phiếu báo mới Đang tạo)', 'PNK-1 không còn trong cửa sổ Chọn phiếu nhập kho']),
    C('Xóa phiếu báo thì phiếu nhập kho quay lại hàng chờ', 'P0', 'Phiếu báo Đang tạo của PNK-1.', ['1. Xóa phiếu báo', '2. Mở màn hàng chờ'], '', ['PNK-1 xuất hiện lại']),
    C('Không duyệt KHÔNG trả phiếu nhập kho về hàng chờ', 'P1', 'Phiếu báo của PNK-2 bị Không duyệt.', ['1. Mở màn hàng chờ'], '', ['PNK-2 không có ở hàng chờ']),
    C('Phiếu nhập kho chưa hạch toán không báo được', 'P1', 'PNK-5 Chờ duyệt (chưa hạch toán) có dòng lệch.', ['1. Mở cửa sổ Chọn phiếu nhập kho, tìm PNK-5'], '',
      ['Không có PNK-5; sau khi PNK-5 được hạch toán thì mới xuất hiện']),
    C('Phiếu nhập kho loại khác nhập mua không vào danh sách', 'P2', 'PNK-6 loại Nhập điều chuyển kho chi nhánh, Đã hạch toán, có dòng lệch.', ['1. Tìm PNK-6 trong cửa sổ chọn'], '', ['Không có PNK-6']),
    C('Liên kết sang phiếu nhập kho và yêu cầu nhập', 'P2', 'Phiếu báo của PNK-00339.', ['1. Ở Chi tiết bấm PNK-00339', '2. Bấm PYCNH-00416'], '',
      ['Mở đúng chi tiết Phiếu nhập kho / Yêu cầu nhập hàng ở tab mới']),
]

# ------------------------------------------------------------------ PHÂN QUYỀN
S_QUYEN = [
    C('Không có quyền nào: chỉ thấy phiếu mình tạo', 'P0', 'TK-Z không có quyền, đã tạo 0 phiếu.', ['1. Đăng nhập TK-Z', '2. Vào menu ' + MENU], '',
      ['Mục menu vẫn hiện, mở được màn', 'Danh sách "Không có dữ liệu phù hợp."', 'Không có nút Tạo mới; không có ô Công ty']),
    C('Quyền "' + Q_XEM + '" mức Tổng công ty', 'P0', 'TK-ALL; có phiếu của 2 công ty.', ['1. Đăng nhập TK-ALL, vào màn', '2. Mở Tìm kiếm nâng cao'], '',
      ['Thấy phiếu mọi công ty, mọi trạng thái', 'Có ô Công ty']),
    C('Quyền "' + Q_XEM + '" mức Công ty', 'P0', 'TK-CTY thuộc TPE; có phiếu TPE và công ty khác.', ['1. Đăng nhập TK-CTY, vào màn'], '',
      ['Chỉ phiếu của TPE và phiếu mình tạo', 'Không có ô Công ty', 'Không có Sửa / Xóa trên phiếu của người khác']),
    C('Quyền "' + Q_TAO + '"', 'P0', 'TK-A có quyền Tạo.', ['1. Đăng nhập TK-A, vào màn'], '', ['Có nút Tạo mới; mở trang Tạo, lưu được phiếu']),
    C('Không có quyền Tạo thì không tạo được', 'P0', 'TK-Z.', ['1. Dán đường dẫn trang Tạo', '2. Chọn phiếu nhập kho, nhập đủ, bấm Lưu'], '',
      ['Cửa sổ chọn không có phiếu nào / báo không có quyền', 'Hệ thống từ chối: "Bạn không có quyền tạo phiếu báo hàng thừa, thiếu nhập kho."']),
    C('Quyền "' + Q_DUYET + '"', 'P0', 'TK-D thuộc TPE, không có quyền Xem; TPE có phiếu Chờ xử lý, Đang tạo của người khác.', ['1. Đăng nhập TK-D, vào màn'], '',
      ['Thấy thêm phiếu Chờ xử lý của TPE (có Xử lý); không thấy phiếu Đang tạo / Đã xử lý của người khác']),
    C('Người có 2 quyền Xem mức khác nhau', 'P1', 'TK-X có mức Công ty ở 1 vai trò và Tổng công ty ở vai trò khác.', ['1. Đăng nhập TK-X, vào màn'], '',
      ['Áp mức lớn hơn: thấy phiếu mọi công ty, có ô Công ty']),
    C('Đổi công ty đang làm việc', 'P1', 'TK-CTY làm việc ở 2 công ty.', ['1. Đổi công ty đang làm việc sang công ty B', '2. Vào màn'], '',
      ['Danh sách tính lại theo công ty B, không thấy phiếu của công ty cũ (trừ phiếu mình tạo)']),
    C('Super Admin', 'P2', 'Tài khoản Super Admin.', ['1. Vào màn'], '', ['Thấy mọi phiếu; có Tạo mới, Xử lý, Không duyệt với phiếu Chờ xử lý']),
] + phan_quyen_chung(K)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', danh_so(hien_thi(K))),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', danh_so(tim_kiem(K))),
    ('III', 'THÊM MỚI', danh_so(S_THEM)),
    ('IV', 'CHỈNH SỬA', danh_so(S_SUA)),
    ('V', 'XÓA', danh_so(S_XOA)),
    ('VI', 'GỬI DUYỆT', danh_so(S_GUI)),
    ('VII', 'DUYỆT PHIẾU (XỬ LÝ)', danh_so(S_DUYET)),
    ('VIII', 'KHÔNG DUYỆT PHIẾU', danh_so(S_KD)),
    ('IX', 'LỊCH SỬ THAY ĐỔI', danh_so(lich_su(K))),
    ('X', 'XEM CHI TIẾT PHIẾU BÁO', danh_so(S_XEM)),
    ('XI', 'TÙY CHỈNH CỘT', danh_so(tuy_chinh_cot(K))),
    ('XII', 'XUẤT DANH SÁCH EXCEL', danh_so(xuat_excel(K))),
    ('XIII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', danh_so(S_RB)),
    ('XIV', 'PHÂN QUYỀN', danh_so(S_QUYEN)),
]

if __name__ == '__main__':
    build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='phieu')
