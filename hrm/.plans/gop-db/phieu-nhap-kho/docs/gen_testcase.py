# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu nhập kho" (STT 178) — KHUÔN CHUẨN tab "13. DM quốc gia" (user chốt 03/11/2026), loại 'phieu'.

Bản cũ (khuôn tc_engine + nhóm TC-ROLE, sinh 02/11) giữ ở gen_testcase_v1.py để tra. Bản này:
  - giữ mọi case nghiệp vụ của bản cũ, đưa vào đúng nhóm chuẩn, sửa câu chữ theo giọng tab Quốc gia;
  - bổ sung case theo checklist "Mẫu tài liệu.xlsx" (case chung sinh từ _tc_phieu_chung.py).
Chạy: python gen_testcase.py  (tự gọi check_tc → phải 0 lỗi)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHUAN = os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi'))
sys.path.insert(0, HERE)
sys.path.insert(0, CHUAN)
from _tc_chuan import build_chuan  # noqa: E402
from _tc_phieu_chung import C, danh_so, hien_thi, tim_kiem, them_moi_dong_form, lich_su, tuy_chinh_cot, \
    xuat_excel, phan_quyen_chung  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Phiếu nhập kho'
MODULE = 'Phiếu nhập kho'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SHEET = 'Trang tính1'
NGAY = '03/11/2026'


def L_(*lines):
    return '\n'.join(lines)


MENU = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > Phiếu nhập kho'
MENU2 = 'Kho > Nhập kho > Phiếu nhập kho'
TON = 'Kho > Báo cáo kho > Báo cáo tồn kho chi tiết theo mặt hàng'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '-  TK-TK: thủ kho của kho K1 (Kho Sài Gòn), không có quyền xem phiếu nhập kho nào. TK-TK2: thủ kho khác của kho K1.',
    '-  TK-KT: có quyền "Kế toán kho", cùng công ty với K1. TK-KT2: "Kế toán kho" công ty khác.',
    '-  TK-CTY: có "Xem phiếu nhập kho theo công ty". TK-ALL: có "Xem phiếu nhập kho theo tổng công ty". '
    'TK-PB: có "Xem phiếu nhập kho theo phòng ban". TK-Z: không quyền, không phải thủ kho.',
    '-  ĐN-1: đề nghị nhập kho Chờ duyệt của kho K1, loại Nhập hàng mua trong nước (TỰ DO + HÃNG), 1 hàng H1 SL đề nghị 2 Cái.',
    '-  ĐN-2: đề nghị Chờ duyệt khác của kho K1. ĐN-7: đề nghị Chờ duyệt loại Nhập điều chuyển kho chi nhánh của kho K1.',
    '-  Vị trí V1, V2 thuộc kho K1 (không kiểm kê); V3 thuộc kho K1 đang trong đợt kiểm kê.',
    '-  File đính kèm mẫu: 1 file pdf dưới 20MB; 1 file .exe; 1 file pdf trên 20MB.',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Phiếu nhập kho" là chứng từ thủ kho nhập hàng VẬT LÝ vào vị trí kho, lập từ 1 đề nghị nhập kho Chờ duyệt. '
        'Luồng: Tạo phiếu (vị trí dự kiến) > Phiếu xếp hàng (chia nhóm, người đi xếp) > Nhập kho (SL, vị trí thực, file) > '
        '"Lưu và nhập" (cộng tồn kho, Chờ duyệt) > kế toán kho lập Phiếu nhập hàng (Đang hạch toán > Đã hạch toán) hoặc '
        'Không duyệt > Xuất lại (trừ tồn) > Nhập lại (phiếu mới). Hủy khi còn Đang tạo.',
        'Đường vào: menu ' + MENU + '; lối thứ 2: menu ' + MENU2 + ' (cùng 1 màn).',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới, Phiếu xếp hàng, Nhập kho / Sửa phiếu, '
        'Lưu và nhập, Xem chi tiết, Hủy, Không duyệt, Tạo phiếu nhập hàng, Tạo phiếu xuất lại, Tạo phiếu nhập lại, In phiếu, '
        'In barcode, Xuất Excel, Lịch sử. Không có Xóa, Khóa, Import.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi xem (cộng dồn):',
        '-  "Xem phiếu nhập kho theo tổng công ty" (hoặc Super admin): mọi công ty; "… theo công ty": công ty đang làm việc; '
        '"… theo phòng ban": phòng ban được giao quản lý.',
        '-  Thủ kho có quyền "Xem tất cả phiếu xuất nhập kho": phiếu của kho mình là thủ kho.',
        '-  "Kế toán kho": phiếu đã gửi (khác Đang tạo) của công ty mình.',
        '-  Luôn thấy phiếu do mình tạo.',
        'Cửa sổ chọn đề nghị: chỉ đề nghị Chờ duyệt của kho người dùng là thủ kho.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Phiếu Đang tạo của người khác không hiện ở danh sách (phiếu đang đi xếp hàng vẫn mở được qua liên kết).',
        '-  Vị trí đang kiểm kê: mờ, ghi "Đang kiểm kho", không chọn được.',
        '-  Nút trên dòng ẨN khi không đúng trạng thái / vai trò (không làm mờ).',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" (Từ – Đến) lọc theo ngày tạo phiếu, tính cả 2 đầu mút.',
        'Ngày nhận = lúc "Lưu và nhập"; Ngày duyệt = lúc lập phiếu nhập hàng (không phải ô lọc).',
        'Bộ lọc được giữ khi mở trang chi tiết / sửa rồi quay lại trong 10 phút; vào màn khác qua menu thì về mặc định.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Phiếu > dòng hàng (theo đề nghị) > nhiều dòng vị trí (vị trí + SL nhập). Bước xếp hàng: mỗi dòng vị trí thuộc 1 phiếu '
        'xếp hàng có 1 người đi xếp.',
        'Trạng thái: Đang tạo (tiến trình Đang đi xếp hàng / Đang nhập kho), Chờ duyệt, Đang hạch toán, Đã hạch toán, '
        'Không duyệt, Đã xuất lại, Đã nhập lại, Đã hủy.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  Tổng SL các vị trí của 1 dòng không vượt SL đề nghị (điều chuyển kho chi nhánh: phải bằng); cả phiếu phải có ít nhất '
        '1 hàng SL > 0; SL tối đa 999,999.',
        '-  1 dòng hàng không chọn trùng vị trí. Chỉ "Lưu và nhập" mới cộng tồn; Xuất lại trừ toàn bộ; Không duyệt không hoàn tồn.',
    )),
    ('7. Phân quyền cấp', L_(
        '-  Màn không có quyền vào riêng. 3 quyền xem nằm ở nhóm "Phiếu nhập kho" màn Phân quyền; "Kế toán kho" là quyền dùng chung kho.',
        '-  Thủ kho khai ở danh mục kho (danh sách thủ kho của kho). Thao tác do vai trò (thủ kho / người tạo / kế toán kho) '
        'và trạng thái phiếu quyết định.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N": N = tổng phiếu khớp bộ lọc và phạm vi xem. Trang chi tiết có dòng Tổng cộng SL đề nghị, '
        'SL thực nhập, SL nhập.',
        'Tab Bốc xếp: Số tiền = Đơn giá × Khối lượng (hoặc Số giờ); Số tiền sau VAT = Số tiền × (1 + VAT%).',
    )),
    ('9. Ghi chú đọc bảng', L_(
        'Các bẫy dễ sai nhất của màn này, QA đọc trước khi test:',
        '-  Tạo phiếu CHƯA cộng tồn; chỉ "Lưu và nhập" mới cộng tồn. "Lưu" ở bước Nhập kho vẫn là Đang tạo.',
        '-  Kế toán kho "duyệt" bằng cách lập Phiếu nhập hàng (màn khác), không có nút Duyệt trên màn này.',
        '-  Không duyệt KHÔNG hoàn tồn; phải Tạo phiếu xuất lại mới trừ tồn.',
        '-  Kiểm tồn: sau "Lưu và nhập" / "Xuất lại" mở menu ' + TON + ' hoặc cột Tồn ở cửa sổ chọn vị trí.',
        '-  Số theo chuẩn quốc tế 1,234,567.89. Cột KQ thực tế, DNS check để trống cho tester điền.',
    )),
]

# ------------------------------------------------------------------ cấu hình case chung
K = dict(
    menu=MENU,
    tieu_de='Danh sách phiếu nhập kho',
    buoc_mo_them=['3. Vào thêm menu ' + MENU2],
    exp_mo_them=['Cả 2 đường menu mở CÙNG một màn "Danh sách phiếu nhập kho"'],
    exp_nut=['Thanh công cụ có: Tạo mới, Xuất Excel, Cấu hình cột hiển thị',
             'Khối tìm kiếm có ô "Tìm theo Mã phiếu", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
             'Không có nút Import, In danh sách'],
    cot=['STT', 'Mã phiếu', 'Loại', 'Nhà cung cấp', 'Kho nhập', 'Ngày tạo', 'Phiếu ĐNNK', 'Người đề nghị', 'Người yêu cầu',
         'Người tạo', 'Trạng thái', 'Tiến trình', 'Người duyệt', 'Ngày nhận', 'Ngày duyệt', 'Hành động'],
    cot_an=[],
    exp_cot_them=['Cột Mã phiếu dính bên trái khi cuộn ngang'],
    tong_cot=16,
    cot_khoa=['STT', 'Hành động'],
    cot_bo_thu='Người yêu cầu',
    pre_du_lieu='TK-TK vừa tạo phiếu từ ĐN-1, đã Lưu và nhập.',
    exp_du_lieu=['Mã phiếu dạng PNK-<5 chữ số>, là liên kết; Loại, Kho nhập, Nhà cung cấp, Phiếu ĐNNK, Người đề nghị đúng theo ĐN-1',
                 'Người tạo dạng "Họ tên - Mã phòng ban" của TK-TK',
                 'Trạng thái Chờ duyệt, Tiến trình Hoàn thành nhập kho, Ngày nhận = lúc bấm Lưu và nhập',
                 'Người duyệt, Ngày duyệt để TRỐNG (chưa lập phiếu nhập hàng)'],
    trang_thai=[('Đang tạo', 'xám'), ('Chờ duyệt', 'cam'), ('Không duyệt', 'đỏ')],
    exp_trang_thai_them=['Các trạng thái Đang hạch toán, Đã hạch toán, Đã xuất lại, Đã nhập lại, Đã hủy hiện đúng chữ, màu phân biệt được',
                         'Cột Tiến trình hiện Đang đi xếp hàng / Đang nhập kho / Hoàn thành nhập kho đúng bước của phiếu'],
    pre_rong='TK-Z chưa tạo phiếu nào, không có quyền xem, không phải thủ kho / kế toán kho.',
    rong_bang='Không có dữ liệu phù hợp.',
    rong_chan=None,
    sap_xep=['Mã phiếu', 'Loại', 'Nhà cung cấp', 'Kho nhập', 'Ngày tạo', 'Ngày nhận', 'Ngày duyệt'],
    khong_sap_xep=['STT', 'Phiếu ĐNNK', 'Người đề nghị', 'Người yêu cầu', 'Người tạo', 'Trạng thái', 'Tiến trình', 'Người duyệt', 'Hành động'],
    ma='Mã phiếu', vd_ma='PNK-01159', vd_mot_phan='PNK-011', placeholder='Tìm theo Mã phiếu',
    loc_text=('Hàng hoá', 'Dầu nhớt', 'dau nhot'),
    loc_list=['Công ty – Phòng ban', 'Kho nhập', 'Hàng hoá', 'Mã phiếu', 'Loại', 'Nhà cung cấp', 'Phiếu ĐNNK', 'Người đề nghị',
              'Người yêu cầu', 'Người tạo', 'Trạng thái', 'Người duyệt', 'Ngày tạo'],
    exp_mac_dinh_them=['Ô Công ty – Phòng ban chỉ hiện với tài khoản có quyền xem theo tổng công ty / công ty'],
    loc_chon=('Trạng thái', 'Chờ duyệt'),
    loc_ket_hop='Kho nhập = K1, Loại = Nhập hàng mua trong nước (TỰ DO + HÃNG), Trạng thái = Chờ duyệt',
    td_rong='Kho nhập: K1; Trạng thái: Đã hủy; Ngày tạo: hôm nay (chưa hủy phiếu nào hôm nay)',
    form_tao='Dự kiến vị trí', nut_quay_lai='Quay lại', truong_nhap_thu='Người giao hàng',
    td_nhap_thu='Người giao hàng: "Nguyễn Văn A"', nut_luu_chinh='Lưu',
    exp_dong_thoi_them=['(Mỗi người chọn 1 đề nghị khác nhau: ĐN-1 và ĐN-2)'],
    lich_su_title='Lịch sử thay đổi: <mã phiếu>', nut_lich_su='Xem lịch sử',
    excel=dict(title='Chọn trường xuất Excel', so_truong=14,
               truong=['Mã phiếu', 'Loại', 'Nhà cung cấp', 'Kho nhập', 'Ngày tạo', 'Phiếu ĐNNK', 'Người đề nghị', 'Người yêu cầu',
                       'Người tạo', 'Trạng thái', 'Tiến trình', 'Người duyệt', 'Ngày nhận', 'Ngày duyệt'],
               mac_dinh='Mặc định tích sẵn cả 14 trường, dòng đếm "Đang chọn 14/14 trường"',
               file='danh_sach_phieu_nhap_kho.xlsx', tieu_de='DANH SÁCH PHIẾU NHẬP KHO', bo_thu='Người duyệt',
               exp_them=['Có dòng khoảng ngày lọc dưới tiêu đề và khối ký "Người lập" cuối file'],
               rong=['Báo "Xuất Excel thành công"', 'File chỉ có tiêu đề và dòng tên cột, không có dòng dữ liệu']),
)

# ------------------------------------------------------------------ I. HIỂN THỊ (phần riêng)
K['hien_thi_rieng'] = [
    C('Phiếu nhập lại hiển thị phiếu gốc', 'P2', 'Có phiếu nhập lại.',
      ['1. Xem ô Mã phiếu của phiếu nhập lại', '2. Bấm mã phiếu gốc'], '',
      ['Dưới mã có dòng nghiêng "Nhập lại cho phiếu <mã gốc>"', 'Bấm mở trang Chi tiết phiếu gốc']),
    C('Liên kết ở cột Phiếu ĐNNK', 'P2', 'Có phiếu lập từ ĐN-1.', ['1. Bấm mã ở cột Phiếu ĐNNK'], '',
      ['Mở màn chi tiết Đề nghị nhập kho đúng mã ĐN-1']),
    C('Nút trên dòng theo trạng thái với thủ kho tạo phiếu', 'P0',
      'TK-TK có phiếu Đang đi xếp hàng, Đang nhập kho, Không duyệt, Đã xuất lại.',
      ['1. Đăng nhập TK-TK', '2. Xem cột Hành động từng phiếu'], '',
      ['Đang đi xếp hàng: Nhập kho, Hủy hiện ngoài; nút ba chấm "Hành động khác" có Phiếu xếp hàng, In phiếu, Xem lịch sử',
       'Đang nhập kho: nút đổi nhãn "Sửa phiếu", có thêm In barcode',
       'Không duyệt: có Tạo phiếu xuất lại; Đã xuất lại: có Tạo phiếu nhập lại',
       'Phiếu có hơn 3 nút: 2 nút đầu hiện ngoài, còn lại trong "Hành động khác"']),
    C('Nút trên dòng với kế toán kho', 'P0', 'TK-KT; có phiếu Chờ duyệt của kho K1.',
      ['1. Đăng nhập TK-KT', '2. Lọc Trạng thái = Chờ duyệt', '3. Xem cột Hành động'], '',
      ['Có Tạo phiếu nhập hàng, Không duyệt; In phiếu, In barcode, Xem lịch sử', 'Không có Nhập kho, Sửa phiếu, Hủy']),
]

# ------------------------------------------------------------------ II. LỌC (phần riêng)
K['loc_rieng'] = [
    C('Lọc theo Kho nhập', 'P0', 'Có phiếu của kho K1 và kho khác.', ['1. Mở Tìm kiếm nâng cao', '2. Chọn Kho nhập = K1'], 'Kho nhập: K1',
      ['Bảng lọc ngay, mọi dòng có Kho nhập = K1']),
    C('Lọc theo Loại', 'P1', 'Có phiếu nhiều loại.', ['1. Chọn Loại = Nhập điều chuyển kho chi nhánh'], '',
      ['Danh sách chọn có 17 loại nhập', 'Chỉ còn phiếu đúng loại đã chọn']),
    C('Lọc theo Trạng thái', 'P0', 'Có phiếu ở nhiều trạng thái.', ['1. Chọn Trạng thái = Chờ duyệt'], '',
      ['Danh sách chọn có 8 trạng thái: Đang tạo, Chờ duyệt, Đang hạch toán, Đã hạch toán, Không duyệt, Đã xuất lại, Đã nhập lại, Đã hủy',
       'Chỉ còn phiếu Chờ duyệt (kế toán kho dùng để xem phiếu cần xử lý)']),
    C('Lọc theo Hàng hoá', 'P1', 'H1 có trong ĐN-1.', ['1. Nhập mã H1 ở ô Hàng hoá', '2. Nhấn Enter'], 'Hàng hoá: mã H1',
      ['Ra phiếu có H1 ở đề nghị nguồn hoặc lô thực nhập', 'Gõ chưa Enter thì chưa lọc']),
    C('Lọc theo Phiếu ĐNNK và Mã phiếu', 'P1', 'Có phiếu lập từ ĐN-1.',
      ['1. Nhập 1 phần mã ĐN-1 ở ô Phiếu ĐNNK, Enter', '2. Làm mới, nhập 1 phần mã phiếu ở ô Mã phiếu, Enter'], '',
      ['Mỗi ô tìm gần đúng đúng cột tương ứng']),
    C('Lọc theo Người đề nghị, Người yêu cầu, Người tạo, Người duyệt, Nhà cung cấp', 'P1', 'Có dữ liệu ở các cột này.',
      ['1. Mở lần lượt từng ô chọn, chọn 1 giá trị'], '',
      ['Danh sách chọn chỉ gồm người / nhà cung cấp có trong phiếu thuộc phạm vi xem', 'Kết quả khớp cột cùng tên trên bảng',
       'Nhà cung cấp hiện dạng "Mã - Tên"']),
    C('Lọc theo Ngày tạo tính cả 2 đầu mút', 'P1', 'Có phiếu tạo ngày 28/10/2026 lúc 17:30.',
      ['1. Chọn Ngày tạo từ 28/10/2026 đến 28/10/2026'], 'Ngày tạo: 28/10/2026 – 28/10/2026',
      ['Ra các phiếu tạo trong ngày 28/10/2026, gồm cả phiếu tạo lúc 17:30']),
    C('Lọc theo Công ty – Phòng ban', 'P2', 'TK-ALL.', ['1. Chọn Công ty', '2. Chọn Phòng ban'], '',
      ['Ô Phòng ban chỉ mở sau khi chọn Công ty', 'Lọc theo tổ chức của phiếu (chép từ đề nghị nhập kho)',
       'TK-Z không có quyền xem thì không thấy ô Công ty – Phòng ban']),
]

# ------------------------------------------------------------------ III. THÊM MỚI
S_THEM = [
    C('Mở trang tạo phiếu', 'P0', 'TK-TK là thủ kho kho K1.', ['1. Bấm Tạo mới', '2. Quan sát trang'], '',
      ['Mở trang "Dự kiến vị trí"; góc phải tiêu đề khối hiện "<tên TK-TK> - <ngày giờ hiện tại>"',
       'Bảng hàng hoá hiện "Chưa chọn phiếu đề nghị nhập kho"', 'Chân trang có Lưu và tiếp tục, Lưu, Quay lại']),
    C('Trường bắt buộc và giá trị mặc định', 'P1', 'Đang ở trang Dự kiến vị trí.', ['1. Quan sát nhãn và giá trị các ô'], '',
      ['Phiếu đề nghị nhập kho, Người giao hàng có dấu * bắt buộc; Ghi chú không bắt buộc',
       'Kho nhập, Người đề nghị chỉ đọc, có biểu tượng chữ i giải thích nguồn dữ liệu',
       'Tab Vận chuyển mặc định "Nhân viên vận chuyển"; tab Bốc xếp mặc định Tính theo khối lượng, các số = 0']),
    C('Cửa sổ chọn đề nghị chỉ có đề nghị Chờ duyệt kho mình', 'P0', 'TK-TK; có đề nghị Chờ duyệt của kho khác.',
      ['1. Bấm ô Phiếu đề nghị nhập kho'], '',
      ['Cửa sổ "Chọn phiếu đề nghị nhập kho", dòng phụ "Chỉ hiện đề nghị Chờ duyệt của kho bạn là thủ kho"',
       'Chỉ có đề nghị Chờ duyệt kho K1; cột STT, Mã phiếu, Loại, Kho, Người tạo, Ngày tạo; 10 dòng/trang',
       'Ô Mã phiếu tìm gần đúng; bấm vào dòng là chọn và đóng cửa sổ']),
    C('Không có đề nghị để chọn', 'P2', 'TK-Z không phải thủ kho kho nào.', ['1. Bấm Tạo mới', '2. Bấm ô Phiếu đề nghị nhập kho'], '',
      ['Cửa sổ hiện "Không có đề nghị nhập kho chờ duyệt ở kho bạn phụ trách."']),
    C('Chọn đề nghị thì điền form', 'P0', 'ĐN-1.', ['1. Bấm dòng ĐN-1 trong cửa sổ chọn'], 'ĐN-1',
      ['Tiêu đề khối = loại đề nghị; Kho nhập, Người đề nghị, Ghi chú lấy theo đề nghị',
       'Bảng hàng có H1, SL đề nghị 2, SL nhập mặc định 2', 'Loại có vận chuyển thì có tab Vận chuyển']),
    C('Bỏ chọn đề nghị bằng nút x', 'P2', 'Đã chọn ĐN-1.', ['1. Bấm nút x ở ô Phiếu đề nghị nhập kho'], '',
      ['Ô đề nghị về trống, bảng hàng hoá xóa trắng']),
    C('Lưu thành công khi nhập đủ dữ liệu', 'P0', 'ĐN-1; ghi tồn H1 tại V1 trước khi làm.',
      ['1. Chọn ĐN-1', '2. Nhập Người giao hàng, chọn vị trí V1, SL 2', '3. Bấm Lưu'], 'Người giao hàng: "Nguyễn Văn A"',
      ['Báo "Phiếu đã được lưu. Hãy tạo phiếu đi xếp hàng", về danh sách',
       'Phiếu PNK-xxxxx đứng đầu, Trạng thái Đang tạo, Tiến trình Đang đi xếp hàng, Người tạo = TK-TK',
       'ĐN-1 chuyển Đang nhập kho; yêu cầu nhập hàng nguồn Đang nhập kho; người lập nhận thông báo',
       'Tồn kho H1 tại V1 CHƯA thay đổi']),
    C('Lưu khi chỉ nhập trường bắt buộc', 'P1', 'ĐN-2.', ['1. Chọn ĐN-2, nhập Người giao hàng, chọn vị trí cho mọi dòng', '2. Để trống Ghi chú, không khai vận chuyển, bốc xếp', '3. Bấm Lưu'], '',
      ['Lưu thành công', 'Ghi chú của phiếu lấy theo ghi chú đề nghị; tab Bốc xếp ở chi tiết hiện "Không có thông tin bốc xếp"']),
    C('Ghi nhận lịch sử Tạo mới sau khi lưu', 'P1', 'Vừa lưu phiếu ở case trước.', ['1. Bấm Xem lịch sử ở dòng phiếu'], '',
      ['Có mốc Tạo mới với người tạo TK-TK và thời điểm lưu']),
    C('Lưu khi chưa chọn đề nghị', 'P1', 'Form trống.', ['1. Bấm Lưu'], '',
      ['Báo "Phiếu phải có ít nhất 1 hàng hoá có số lượng thực nhập lớn hơn 0", không lưu']),
    C('Bỏ trống Người giao hàng', 'P0', 'Đã chọn ĐN-1, vị trí V1.', ['1. Để trống Người giao hàng', '2. Bấm Lưu'], '',
      ['Dưới ô báo đỏ "Bắt buộc phải nhập"; tab Thông tin chung tô đỏ', 'Cuộn tới ô lỗi đầu tiên, không lưu']),
    C('Người giao hàng chỉ nhập khoảng trắng', 'P2', 'Đã chọn ĐN-1, vị trí V1.', ['1. Nhập toàn dấu cách vào Người giao hàng', '2. Bấm Lưu'], 'Người giao hàng: "     "',
      ['Báo "Bắt buộc phải nhập" như khi để trống, không lưu']),
    C('Người giao hàng có khoảng trắng đầu và cuối', 'P2', 'Đã chọn ĐN-1, vị trí V1.', ['1. Nhập Người giao hàng có dấu cách 2 đầu', '2. Bấm Lưu', '3. Mở chi tiết'], 'Người giao hàng: "  Nguyễn Văn A  "',
      ['Lưu được; chi tiết hiện "Nguyễn Văn A" đã bỏ khoảng trắng 2 đầu']),
    C('Người giao hàng đúng 255 ký tự thì lưu được', 'P1', 'Đã chọn ĐN-1, vị trí V1.', ['1. Nhập Người giao hàng 255 ký tự', '2. Bấm Lưu'], 'Chuỗi 255 ký tự',
      ['Lưu thành công, chi tiết hiện đủ 255 ký tự']),
    C('Người giao hàng hoặc Ghi chú vượt 255 ký tự', 'P2', 'Đã chọn ĐN-1, vị trí V1.', ['1. Nhập Người giao hàng 256 ký tự, bấm Lưu', '2. Sửa lại, nhập Ghi chú 256 ký tự, bấm Lưu'], 'Chuỗi 256 ký tự',
      ['Mỗi lần báo "Không được vượt quá 255 ký tự" dưới đúng ô, không lưu']),
    C('Thông báo lỗi mất ngay khi nhập lại hợp lệ', 'P1', 'Ô Người giao hàng đang báo "Bắt buộc phải nhập".', ['1. Gõ "Nguyễn Văn A" vào ô'], '',
      ['Chữ báo đỏ dưới ô biến mất ngay, không cần bấm Lưu lại']),
    C('Bỏ trống vị trí', 'P0', 'Đã chọn ĐN-1.', ['1. Không chọn vị trí, nhập Người giao hàng', '2. Bấm Lưu'], '',
      ['Dưới ô vị trí: "Bắt buộc phải chọn vị trí"', 'Toast "Số lượng nhập không hợp lệ — xem ô báo đỏ ở bảng hàng hoá"', 'Không lưu']),
    C('Cửa sổ chọn vị trí kho', 'P1', 'Đã chọn ĐN-1.', ['1. Bấm ô vị trí của dòng H1'], '',
      ['Cửa sổ "Chọn vị trí kho": STT, Vị trí, Nhà, Dãy, Khoang, Tồn (của H1 tại vị trí); 10 dòng/trang',
       'Chỉ có vị trí đang hoạt động của kho K1; bấm vào dòng là chọn và đóng cửa sổ']),
    C('Vị trí đang kiểm kho không chọn được', 'P1', 'V3 đang kiểm kê.', ['1. Mở cửa sổ Chọn vị trí kho', '2. Bấm dòng V3'], '',
      ['Dòng V3 mờ, ghi "Đang kiểm kho", bấm không chọn được']),
    C('Chọn trùng vị trí cho 1 dòng hàng', 'P1', 'Dòng H1 đã chọn V1.', ['1. Bấm Thêm vị trí', '2. Chọn lại V1 cho dòng vị trí thứ 2'], '',
      ['Báo "Vị trí đã được chọn cho hàng này"']),
    C('Chia 1 dòng hàng ra 2 vị trí', 'P1', 'Đã chọn ĐN-1.', ['1. Bấm Thêm vị trí', '2. V1 SL 1, V2 SL 1', '3. Bấm Lưu'], '',
      ['SL thực nhập = 2', 'Lưu được, chi tiết có 2 dòng vị trí']),
    C('Tổng SL vượt SL đề nghị', 'P0', 'SL đề nghị 2.', ['1. Nhập SL 3', '2. Bấm Lưu'], 'SL: 3',
      ['Ô SL đỏ "Vượt SL đề nghị (2)"', 'Số 3 GIỮ NGUYÊN, không tự sửa về 2', 'Không lưu']),
    C('SL để trống hoặc vượt 999,999', 'P1', 'Đã chọn vị trí.', ['1. Xóa SL, bấm Lưu', '2. Nhập 1000000, bấm Lưu'], 'SL: trống / 1000000',
      ['Bước 1: "Bắt buộc phải nhập"', 'Bước 2: "Không được lớn hơn 999,999"', 'Không lưu']),
    C('SL nhập ký tự không phải số', 'P2', 'Đã chọn vị trí.', ['1. Gõ chữ "abc" và dấu "-" vào ô SL'], 'SL: abc / -5',
      ['Ô không nhận chữ và số âm']),
    C('Điều chuyển kho chi nhánh phải nhập đủ SL', 'P1', 'ĐN-7, SL đề nghị 5.', ['1. Chọn ĐN-7, nhập SL 4', '2. Bấm Lưu'], 'SL: 4',
      ['Báo "SL thực nhập phải bằng SL đề nghị", không lưu']),
    C('Áp dụng tất cả vị trí', 'P2', 'Đề nghị nhiều dòng hàng.', ['1. Chọn V1 cho dòng 1', '2. Tích "Áp dụng tất cả"'], '',
      ['Mọi dòng hàng nhận vị trí V1']),
    C('Vận chuyển bằng Công ty vận chuyển bắt buộc chuyến xe', 'P1', 'Loại có vận chuyển.',
      ['1. Tab Vận chuyển chọn "Công ty vận chuyển"', '2. Không chọn chuyến, bấm Lưu', '3. Thêm chuyến, chọn 2 lần cùng 1 chuyến'], '',
      ['Bước 2: "Bắt buộc phải chọn chuyến xe"', 'Bước 3: "Không được chọn trùng"']),
    C('Tạo nhanh chuyến xe từ tab Vận chuyển', 'P2', 'Tab Vận chuyển = Công ty vận chuyển.', ['1. Bấm "Tạo chuyến xe"', '2. Nhập đủ, lưu'], '',
      ['Mở popup tạo nhanh chuyến xe chở hàng', 'Lưu xong chuyến được chọn sẵn vào phiếu']),
    C('Bốc xếp thuê ngoài thiếu thông tin', 'P1', 'Tab Bốc xếp.',
      ['1. Chọn Loại hình thuê = Thuê ngoài', '2. Để trống Nhà cung cấp, Loại bốc xếp, Khối lượng, bấm Lưu', '3. Nhập Khối lượng 0, bấm Lưu'], '',
      ['Bước 2: 3 ô báo "Bắt buộc phải chọn" / "Bắt buộc phải nhập"', 'Bước 3: Khối lượng báo "Phải lớn hơn 0"']),
    C('Bốc xếp công ty: chia tiền người nhận việc', 'P1', 'Loại hình thuê = Công ty, Số tiền 200,000.',
      ['1. Thêm 2 nhân sự 100,000 và 50,000, bấm Lưu', '2. Sửa thành 100,000 + 100,000, bấm Lưu'], '',
      ['Bước 1: "Tổng số tiền chia cho các nhân viên phải bằng tổng số tiền bốc xếp"', 'Bước 2: lưu được',
       'Đơn giá, Số tiền tự tính; Số tiền sau VAT = Số tiền × (1 + VAT%)']),
    C('Hàng đang kiểm kho', 'P2', 'H1 thuộc đợt kiểm kê đang chạy ở K1.', ['1. Lập phiếu có H1, bấm Lưu'], '',
      ['Báo "Hàng <tên H1> đang kiểm kho!", không lưu']),
    C('Lưu và tiếp tục với dữ liệu hợp lệ', 'P1', 'ĐN-1 đủ dữ liệu.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Báo "Phiếu đã được lưu. Hãy tạo phiếu đi xếp hàng"', 'Ở lại trang Dự kiến vị trí, form trống hoàn toàn để tạo tiếp',
       'Danh sách có phiếu vừa lưu']),
    C('Lưu và tiếp tục khi thiếu trường bắt buộc', 'P1', 'Đã chọn ĐN-1, để trống Người giao hàng.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Báo "Bắt buộc phải nhập" dưới Người giao hàng, không lưu, dữ liệu đã nhập còn nguyên']),
    C('Lưu và tiếp tục khi dữ liệu sai', 'P1', 'Đã chọn ĐN-1, SL 1000000.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Báo "Không được lớn hơn 999,999", không lưu']),
    C('Lưu và tiếp tục khi chọn trùng vị trí', 'P2', 'Dòng H1 có 2 dòng vị trí cùng V1.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Báo "Vị trí đã được chọn cho hàng này", không lưu']),
    C('Bấm Quay lại ngay sau Lưu và tiếp tục thì không hỏi', 'P1', 'Vừa Lưu và tiếp tục, form đang trống.', ['1. Bấm Quay lại'], '',
      ['Về danh sách ngay, không hiện hộp "Thông tin chưa lưu"']),
    C('Tạo phiếu từ màn Đề nghị nhập kho', 'P1', 'ĐN-1 Chờ duyệt.', ['1. Ở màn Đề nghị nhập kho, bấm "Tạo phiếu nhập kho" của ĐN-1'], '',
      ['Mở trang Dự kiến vị trí đã chọn sẵn ĐN-1']),
] + them_moi_dong_form(K) + [
    C('Hai thủ kho cùng tạo phiếu từ 1 đề nghị', 'P1', 'TK-TK và TK-TK2 cùng mở trang tạo, cùng chọn ĐN-1.',
      ['1. TK-TK bấm Lưu', '2. TK-TK2 bấm Lưu'], '',
      ['TK-TK lưu thành công', 'TK-TK2 bị chặn: "Chỉ thủ kho của kho nhập mới tạo được phiếu nhập kho từ đề nghị đang chờ duyệt." (đề nghị đã hết Chờ duyệt)',
       'Chỉ có 1 phiếu nhập kho cho ĐN-1']),
]

# ------------------------------------------------------------------ IV. CHỈNH SỬA (phiếu xếp hàng, nhập kho, sửa phiếu)
S_SUA = [
    C('Mở trang Phiếu đi xếp hàng', 'P0', 'Phiếu vừa tạo (Đang đi xếp hàng) của TK-TK.', ['1. Ở dòng phiếu bấm ba chấm > Phiếu xếp hàng'], '',
      ['Trang "Phiếu đi xếp hàng: <mã>"; khối thông tin chung chỉ đọc', '"Phiếu 1" chứa mọi dòng vị trí của phiếu']),
    C('Chia nhóm xếp hàng và chọn người đi xếp', 'P0', 'Phiếu có 2 dòng vị trí.',
      ['1. Bấm Thêm phiếu xếp hàng', '2. Kéo 1 dòng sang Phiếu 2', '3. Chọn người đi xếp cho 2 phiếu', '4. Bấm Lưu phiếu xếp hàng'], '',
      ['Báo "Đã lưu phiếu xếp hàng"; mở lại trang vẫn giữ nhóm và người đi xếp',
       'Danh sách người đi xếp chỉ gồm thủ kho của kho nhập, dạng "Họ tên - Mã phòng ban - Mã nhân viên"']),
    C('Thiếu người đi xếp', 'P0', 'Phiếu 2 có dòng nhưng chưa chọn người.', ['1. Bấm Lưu phiếu xếp hàng'], '',
      ['Báo "Bắt buộc phải chọn người đi xếp", không lưu']),
    C('Bấm Nhập kho khi chưa xếp xong', 'P1', 'Còn phiếu xếp hàng chưa có người đi xếp.', ['1. Bấm Nhập kho ở trang xếp hàng'], '',
      ['Báo "Còn dòng hàng chưa có người đi xếp — chọn người đi xếp cho mọi phiếu.", ở lại trang']),
    C('Bỏ phiếu xếp hàng trống', 'P2', 'Có 2 phiếu, Phiếu 2 không còn dòng.', ['1. Bấm biểu tượng thùng rác ở Phiếu 2'], '',
      ['Phiếu 2 bị bỏ', 'Nút chỉ hiện ở phiếu không còn dòng']),
    C('Mở trang Nhập kho', 'P0', 'Đã xếp xong.', ['1. Bấm Nhập kho ở dòng phiếu'], '',
      ['Trang "Phiếu nhập kho: <mã>" nạp đúng dữ liệu đã lưu (người giao hàng, ghi chú, vị trí, SL, vận chuyển, bốc xếp)',
       'Có khối File đính kèm (*); nút In dự kiến, Lưu, Lưu và nhập, Quay lại', 'Không có "Áp dụng tất cả"']),
    C('Trường không sửa được ở trang Nhập kho', 'P1', 'Đang ở trang Nhập kho.', ['1. Thử sửa Phiếu đề nghị nhập kho, Kho nhập, Người đề nghị'], '',
      ['Phiếu đề nghị nhập kho là liên kết, không đổi được', 'Kho nhập, Người đề nghị chỉ đọc']),
    C('Lưu thiếu file đính kèm', 'P0', 'Phiếu chưa có file.', ['1. Bấm Lưu'], '', ['Báo "Bắt buộc phải chọn file đính kèm", không lưu']),
    C('File sai định dạng hoặc quá 20MB', 'P1', 'Đang ở trang Nhập kho.', ['1. Thêm tài liệu: file .exe', '2. Thêm file pdf trên 20MB'], '',
      ['"Chỉ nhận file pdf, jpeg, jpg, png, doc, csv, xlsx, xls, docx"', '"Dung lượng tối đa 20MB"', 'File không được thêm vào phiếu']),
    C('Vị trí chỉ bắt buộc ở dòng SL lớn hơn 0', 'P1', 'Đang ở trang Nhập kho.', ['1. Thêm vị trí, để SL 0 không chọn vị trí', '2. Bấm Lưu'], '',
      ['Lưu được', 'Dòng SL > 0 mà không có vị trí thì báo "Bắt buộc phải chọn vị trí"']),
    C('Vận chuyển công ty ở bước nhập kho', 'P1', 'Công ty vận chuyển, km dự kiến 50.',
      ['1. Để trống Tuyến đường, Số km chốt, bấm Lưu', '2. Nhập km chốt 60, không ghi chú, bấm Lưu', '3. Nhập km chốt 1000000'], '',
      ['Bước 1: "Bắt buộc phải chọn" / "Bắt buộc phải nhập"', 'Bước 2: "Số km chốt khác số km dự kiến — bắt buộc nhập ghi chú vận chuyển"',
       'Bước 3: "Không được lớn hơn 999,999"']),
    C('Lưu ở bước nhập kho (chưa ghi tồn)', 'P0', 'Đủ dữ liệu; ghi tồn H1 tại V1.', ['1. Bấm Lưu'], '',
      ['Báo "Phiếu đã được lưu. Bạn cần gửi để phiếu được xử lý"; phiếu Đang tạo, tiến trình Đang nhập kho',
       'Nút trên dòng đổi thành "Sửa phiếu"; tồn H1 tại V1 KHÔNG đổi']),
    C('Sửa một trường rồi lưu', 'P0', 'Phiếu Đang nhập kho.', ['1. Bấm Sửa phiếu', '2. Đổi Ghi chú', '3. Bấm Lưu', '4. Xem lịch sử'], 'Ghi chú: "Giao bổ sung"',
      ['Lưu thành công, chi tiết hiện Ghi chú mới', 'Lịch sử có mốc Thay đổi thông tin: Ghi chú cũ > mới']),
    C('Sửa nhiều trường cùng lúc', 'P1', 'Phiếu Đang nhập kho.', ['1. Đổi Người giao hàng, SL, vị trí', '2. Bấm Lưu', '3. Xem lịch sử'], '',
      ['Lưu thành công', '1 mốc Thay đổi thông tin liệt kê đủ các trường đổi (gồm bảng hàng × vị trí)']),
    C('Gỡ file đã lưu', 'P2', 'Phiếu Đang nhập kho có 2 file.', ['1. Ở trang Sửa phiếu gỡ 1 file', '2. Bấm Lưu'], '',
      ['File bị gỡ khỏi phiếu, lịch sử ghi File đính kèm cũ > mới']),
    C('Chuyến xe đã duyệt không gỡ được', 'P2', 'Phiếu có chuyến đã duyệt.', ['1. Mở Sửa phiếu, tab Vận chuyển'], '',
      ['Ô chuyến đã duyệt bị khóa, không có nút xóa']),
    C('Mở sửa không thay đổi gì rồi bấm Quay lại', 'P1', 'Phiếu Đang nhập kho.', ['1. Bấm Sửa phiếu', '2. Bấm Quay lại ngay'], '',
      ['Về danh sách, không hỏi "Thông tin chưa lưu"']),
    C('Sửa rồi trả lại đúng giá trị cũ, bấm Quay lại thì không hỏi', 'P2', 'Phiếu Đang nhập kho.',
      ['1. Đổi Ghi chú', '2. Sửa về đúng như cũ', '3. Bấm Quay lại'], '', ['Về danh sách, không hỏi']),
    C('Đã đổi dữ liệu rồi bấm Quay lại', 'P0', 'Đang ở trang Sửa phiếu.', ['1. Đổi Người giao hàng', '2. Bấm Quay lại', '3. Bấm Ở lại', '4. Bấm Quay lại, bấm Thoát'], '',
      ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"', 'Ở lại: giữ form và dữ liệu đang sửa',
       'Thoát: về danh sách, dữ liệu phiếu KHÔNG đổi, không ghi lịch sử']),
    C('Bấm Lưu mà không đổi gì thì không ghi lịch sử', 'P1', 'Phiếu Đang nhập kho.', ['1. Mở Sửa phiếu, bấm Lưu ngay', '2. Xem lịch sử'], '',
      ['Không sinh mốc Thay đổi thông tin mới']),
    C('Phiếu đã gửi không sửa được', 'P0', 'Phiếu Chờ duyệt của TK-TK.', ['1. Xem cột Hành động', '2. Dán đường dẫn trang Nhập kho của phiếu'], '',
      ['Không có nút Nhập kho / Sửa phiếu', 'Báo "Phiếu không sửa được hoặc bạn không có quyền." và về danh sách']),
    C('Người khác không nhập kho được', 'P1', 'TK-TK2 mở đường dẫn trang Nhập kho phiếu của TK-TK.', ['1. Mở đường dẫn'], '',
      ['Báo "Phiếu không sửa được hoặc bạn không có quyền.", về danh sách']),
    C('Hai tab cùng sửa 1 phiếu', 'P2', 'TK-TK mở trang Sửa phiếu ở 2 tab.', ['1. Tab 1 bấm Lưu và nhập', '2. Tab 2 đổi Ghi chú, bấm Lưu'], '',
      ['Tab 2 bị chặn, báo phiếu không còn sửa được, dữ liệu phiếu không đổi']),
]

# ------------------------------------------------------------------ VI. GỬI DUYỆT (Lưu và nhập)
S_GUI = [
    C('Nút Lưu và nhập chỉ có ở trang Nhập kho của người tạo', 'P1', 'TK-TK; phiếu Đang nhập kho.', ['1. Mở trang Sửa phiếu', '2. Đăng nhập TK-TK2 mở chi tiết phiếu'], '',
      ['TK-TK thấy nút Lưu và nhập', 'TK-TK2 không có nút Nhập kho / Sửa phiếu nên không gửi được']),
    C('Lưu và nhập: cộng tồn, chuyển Chờ duyệt', 'P0', 'Ghi tồn H1 tại V1 trước khi làm.', ['1. Bấm Lưu và nhập', '2. Xem tồn H1 tại V1'], '',
      ['Báo "Phiếu đã được gửi", về danh sách; phiếu Chờ duyệt, Tiến trình Hoàn thành nhập kho, có Ngày nhận',
       'Tồn H1 tại V1 tăng đúng SL nhập (quy đổi ĐVT về đơn vị cơ bản)',
       'ĐN-1 Đã nhập kho; yêu cầu nhập hàng Đã nhập kho']),
    C('Kiểm tra dữ liệu bắt buộc trước khi gửi', 'P0', 'Phiếu chưa có file.', ['1. Bấm Lưu và nhập'], '',
      ['Báo "Bắt buộc phải chọn file đính kèm"; phiếu vẫn Đang tạo, tồn không đổi']),
    C('Gửi khi chưa xếp hàng xong', 'P1', 'Phiếu Đang đi xếp hàng còn dòng chưa có người đi xếp (mở trang Nhập kho bằng đường dẫn).', ['1. Bấm Lưu và nhập'], '',
      ['Báo "Chưa xếp hàng xong — hãy lưu phiếu xếp hàng (chọn người đi xếp cho mọi dòng) trước khi nhập kho."']),
    C('Lưu và nhập khi chuyến xe chưa duyệt', 'P1', 'Công ty vận chuyển, chuyến chưa duyệt.', ['1. Bấm Lưu và nhập'], '',
      ['Báo "Chuyến xe chưa được duyệt — duyệt chuyến xe trước khi gửi."; tồn không đổi, phiếu vẫn Đang tạo']),
    C('Thông báo tới kế toán kho sau khi gửi', 'P1', 'TK-KT là kế toán kho của kho K1.', ['1. TK-TK Lưu và nhập', '2. TK-KT mở chuông thông báo, bấm thông báo'], '',
      ['TK-KT nhận thông báo phiếu nhập kho chờ xử lý, ghi đúng mã phiếu', 'Bấm mở đúng trang Chi tiết phiếu']),
    C('Loại mua ngoài: cập nhật đơn đặt hàng và hàng đang về', 'P1', 'Đề nghị loại Nhập hàng mua nước ngoài có đơn đặt hàng gốc.', ['1. Lưu và nhập', '2. Xem đơn đặt hàng gốc và báo cáo hàng đang về'], '',
      ['Dòng đơn đặt hàng gốc "Đã nhập kho"', 'Số hàng đang về giảm đúng SL đã nhập']),
    C('Lịch sử ghi Thay đổi trạng thái khi gửi', 'P1', 'Vừa Lưu và nhập.', ['1. Xem lịch sử phiếu'], '',
      ['Có mốc Thay đổi trạng thái Đang tạo > Chờ duyệt, người thực hiện TK-TK']),
    C('Phiếu đã gửi không gửi lại được', 'P1', 'Phiếu Chờ duyệt.', ['1. Xem nút ở dòng và trang chi tiết'], '',
      ['Không còn Sửa phiếu / Lưu và nhập', 'Tồn chỉ cộng 1 lần']),
]

# ------------------------------------------------------------------ VII. DUYỆT PHIẾU (Tạo phiếu nhập hàng)
S_DUYET = [
    C('Điều kiện hiện nút Tạo phiếu nhập hàng', 'P0', 'TK-KT; có phiếu Chờ duyệt, Đang tạo, Đang hạch toán của kho K1.', ['1. Xem cột Hành động các phiếu'], '',
      ['Chỉ phiếu Chờ duyệt có Tạo phiếu nhập hàng', 'Phiếu loại "Nhập điều chuyển cùng thủ kho" không có nút này']),
    C('Mở form Thêm phiếu nhập hàng', 'P0', 'TK-KT, phiếu Chờ duyệt.', ['1. Bấm Tạo phiếu nhập hàng'], '',
      ['Mở trang Thêm phiếu nhập hàng, ô "Chọn phiếu nhập kho" đã điền sẵn mã phiếu', 'Phiếu nhập kho chưa đổi trạng thái']),
    C('Quay lại từ form phiếu nhập hàng không lưu', 'P1', 'Đang ở form Thêm phiếu nhập hàng mở từ phiếu Chờ duyệt.', ['1. Bấm Quay lại, không lưu'], '',
      ['Phiếu nhập kho vẫn Chờ duyệt, chưa có Người duyệt, Ngày duyệt']),
    C('Lưu phiếu nhập hàng: phiếu nhập kho Đang hạch toán', 'P0', 'Tiếp case trên.', ['1. Lập và lưu phiếu nhập hàng', '2. Xem phiếu nhập kho'], '',
      ['Phiếu nhập kho Đang hạch toán; có Người duyệt = TK-KT, Ngày duyệt = lúc lưu phiếu nhập hàng',
       'Không còn nút Không duyệt, Tạo phiếu nhập hàng']),
    C('Phiếu nhập hàng hoàn thành: phiếu nhập kho Đã hạch toán', 'P1', 'Phiếu nhập kho Đang hạch toán.', ['1. Hoàn thành phiếu nhập hàng', '2. Xem phiếu nhập kho'], '',
      ['Phiếu nhập kho Đã hạch toán', 'Tồn kho không đổi thêm (đã cộng ở bước Lưu và nhập)']),
    C('Kế toán kho công ty khác không duyệt được', 'P1', 'TK-KT2; phiếu Chờ duyệt công ty của TK-KT.', ['1. Đăng nhập TK-KT2, mở phiếu (nếu xem được)'], '',
      ['Không có nút Tạo phiếu nhập hàng / Không duyệt']),
    C('Không duyệt lại phiếu đã xử lý', 'P1', 'Phiếu Đang hạch toán / Đã hạch toán.', ['1. Mở chi tiết phiếu bằng TK-KT'], '',
      ['Không có nút Tạo phiếu nhập hàng, Không duyệt']),
]

# ------------------------------------------------------------------ VIII. KHÔNG DUYỆT PHIẾU (+ xuất lại, nhập lại)
S_KD = [
    C('Điều kiện hiện nút Không duyệt', 'P0', 'TK-KT; phiếu Chờ duyệt loại thường và loại nhập ghép.', ['1. Xem nút ở 2 phiếu'], '',
      ['Phiếu loại thường có Không duyệt', 'Loại điều chuyển cùng thủ kho, điều chuyển kho nội bộ, nhập ghép, nhập tách KHÔNG có Không duyệt']),
    C('Giao diện hộp Không duyệt', 'P1', 'TK-KT, phiếu Chờ duyệt.', ['1. Bấm Không duyệt'], '',
      ['Hộp "Không duyệt phiếu nhập kho": "Phiếu <mã> sẽ bị không duyệt."', 'Ô Lý do không duyệt (*) placeholder "Nhập lý do không duyệt..."',
       'Nút Không duyệt, Đóng']),
    C('Bỏ trống lý do không duyệt', 'P0', 'Đang mở hộp Không duyệt.', ['1. Để trống lý do', '2. Bấm Không duyệt'], '',
      ['Báo "Vui lòng nhập lý do không duyệt."; hộp vẫn mở, phiếu không đổi']),
    C('Lý do chỉ có khoảng trắng', 'P2', 'Đang mở hộp Không duyệt.', ['1. Nhập toàn dấu cách', '2. Bấm Không duyệt'], 'Lý do: "    "',
      ['Bị chặn như khi để trống']),
    C('Lý do vượt 255 ký tự', 'P2', 'Đang mở hộp Không duyệt.', ['1. Nhập lý do 256 ký tự', '2. Bấm Không duyệt'], 'Chuỗi 256 ký tự',
      ['Báo "Không được vượt quá 255 ký tự", không lưu']),
    C('Không duyệt thành công', 'P0', 'TK-KT; ghi tồn H1 trước.', ['1. Nhập lý do "sai số lượng", bấm Không duyệt', '2. Kiểm tồn H1', '3. Mở chi tiết phiếu'], 'Lý do: "sai số lượng"',
      ['Báo "Đã không duyệt phiếu nhập kho"; phiếu Không duyệt', 'Chi tiết có "Lý do không duyệt: sai số lượng"',
       'Tồn H1 KHÔNG giảm (không hoàn tồn)']),
    C('Thông báo tới người tạo khi không duyệt', 'P1', 'Vừa không duyệt phiếu của TK-TK.', ['1. TK-TK mở chuông thông báo'], '',
      ['Có thông báo phiếu bị không duyệt kèm lý do, bấm mở đúng phiếu']),
    C('Bấm Đóng ở hộp Không duyệt', 'P2', 'Đang mở hộp, đã nhập lý do.', ['1. Bấm Đóng'], '', ['Hộp đóng, phiếu vẫn Chờ duyệt']),
    C('Không duyệt lại phiếu đã Không duyệt', 'P1', 'Phiếu Không duyệt.', ['1. Mở chi tiết bằng TK-KT'], '', ['Không còn nút Không duyệt']),
    C('Lịch sử ghi người không duyệt và lý do', 'P1', 'Vừa không duyệt.', ['1. Xem lịch sử'], '',
      ['Mốc Thay đổi trạng thái Chờ duyệt > Không duyệt, người thực hiện TK-KT, kèm lý do, thời điểm']),
    C('Tạo phiếu xuất lại', 'P0', 'Phiếu Không duyệt của TK-TK; ghi tồn trước.',
      ['1. Bấm Tạo phiếu xuất lại', '2. Nhập ghi chú, bấm Xuất lại', '3. Bấm Xuất lại trong hộp xác nhận'], '',
      ['Trang "Tạo phiếu xuất lại" hiện Lý do không duyệt và toàn bộ hàng (không chọn từng dòng)',
       'Hộp "Xác nhận xuất lại": "Toàn bộ hàng của phiếu <mã> sẽ bị trừ khỏi tồn kho. Thao tác không hoàn tác được."',
       'Báo "Hàng đã được xuất lại"; phiếu Đã xuất lại; tồn trở về như trước khi nhập']),
    C('Xuất lại khi không đủ tồn', 'P1', 'Hàng của phiếu đã bị xuất bớt khỏi V1.', ['1. Bấm Xuất lại, xác nhận'], '',
      ['Báo "Hàng <tên> không đủ tồn tại vị trí <mã>. Cần x, còn y"', 'Không trừ lô nào, phiếu vẫn Không duyệt']),
    C('Tạo phiếu nhập lại', 'P0', 'Phiếu Đã xuất lại.', ['1. Bấm Tạo phiếu nhập lại', '2. Chọn file, vị trí, bấm Lưu và nhập'], '',
      ['Trang "Tạo phiếu nhập lại": Người giao hàng khóa, File đính kèm trống (bắt buộc chọn mới)',
       'Sinh phiếu mới "Nhập lại cho phiếu <mã gốc>" Chờ duyệt, tồn cộng lại',
       'Phiếu gốc Đã nhập lại; lịch sử phiếu gốc "Tạo phiếu nhập lại <mã mới>"']),
    C('Người khác không xuất lại, nhập lại được', 'P2', 'TK-TK2 với phiếu của TK-TK.', ['1. Xem nút ở dòng phiếu Không duyệt, Đã xuất lại'], '',
      ['Không có nút Tạo phiếu xuất lại / Tạo phiếu nhập lại']),
]

# ------------------------------------------------------------------ IX. HỦY PHIẾU
S_HUY = [
    C('Điều kiện hiện nút Hủy', 'P0', 'TK-TK có phiếu Đang tạo, Chờ duyệt; phiếu Đang tạo loại Nhập điều chuyển kho chi nhánh.', ['1. Xem nút các phiếu'], '',
      ['Chỉ phiếu Đang tạo loại thường có Hủy', 'Phiếu Chờ duyệt và loại điều chuyển, nhập ghép, nhập tách không có Hủy']),
    C('Hủy phiếu thành công', 'P0', 'Phiếu Đang tạo của TK-TK lập từ ĐN-1.', ['1. Bấm Hủy', '2. Bấm Hủy phiếu'], '',
      ['Hộp "Xác nhận hủy": "Phiếu <mã> sẽ bị hủy, đề nghị nhập kho nguồn cũng bị hủy theo."',
       'Báo "Đã hủy phiếu nhập kho"; phiếu Đã hủy; ĐN-1 bị hủy theo', 'Người lập đề nghị nhận thông báo']),
    C('Bấm Đóng ở hộp xác nhận hủy', 'P1', 'Đang mở hộp Xác nhận hủy.', ['1. Bấm Đóng'], '', ['Hộp đóng, phiếu không đổi']),
    C('Hủy từ trang Chi tiết thì về danh sách', 'P2', 'Phiếu Đang tạo khác.', ['1. Mở chi tiết, bấm Hủy, Hủy phiếu'], '',
      ['Báo "Đã hủy phiếu nhập kho", quay về danh sách']),
    C('Phiếu đã hủy chỉ còn xem', 'P1', 'Phiếu Đã hủy.', ['1. Xem nút ở dòng và chi tiết'], '', ['Chỉ còn In phiếu, Xem lịch sử']),
    C('Lịch sử ghi khi hủy', 'P1', 'Vừa hủy phiếu.', ['1. Xem lịch sử'], '', ['Mốc Thay đổi trạng thái Đang tạo > Đã hủy, người thực hiện, thời điểm']),
    C('Hủy phiếu vừa bị đổi trạng thái ở nơi khác', 'P2', 'Phiếu mở ở 2 tab; tab 1 đã Lưu và nhập.', ['1. Tab 2 bấm Hủy, Hủy phiếu'], '',
      ['Báo "Không thể hủy phiếu này.", phiếu vẫn Chờ duyệt']),
]

# ------------------------------------------------------------------ X. LỊCH SỬ
K['lich_su_rieng'] = [
    C('Lịch sử đủ mốc qua nhánh không duyệt', 'P0', 'Phiếu đi hết Tạo > Lưu > Lưu và nhập > Không duyệt > Xuất lại.', ['1. Bấm Xem lịch sử'], '',
      ['Từ trên xuống: Thay đổi trạng thái Không duyệt > Đã xuất lại (ghi chú "Tạo phiếu xuất lại PXL-…"); Chờ duyệt > Không duyệt (lý do); '
       'Đang tạo > Chờ duyệt; Thay đổi thông tin (file, SL, vị trí); Tạo mới']),
    C('Lịch sử của phiếu nhập lại', 'P1', 'Phiếu nhập lại vừa tạo.', ['1. Xem lịch sử phiếu mới và phiếu gốc'], '',
      ['Phiếu mới có mốc Tạo mới', 'Phiếu gốc có mốc "Tạo phiếu nhập lại <mã mới>"']),
    C('Phiếu tạo trước khi chuyển hệ thống', 'P2', 'Phiếu cũ (từ hệ thống trước).', ['1. Xem lịch sử'], '',
      ['Có thể không có mốc nào: hiện "Chưa có lịch sử thao tác nào."']),
]

# ------------------------------------------------------------------ XI. XEM CHI TIẾT
S_XEM = [
    C('Mở trang chi tiết bằng Mã phiếu', 'P0', 'Phiếu Chờ duyệt.', ['1. Bấm Mã phiếu', '2. Quay lại, chuột phải Mã phiếu > mở tab mới'], '',
      ['Tiêu đề "Chi tiết phiếu nhập kho: <mã>" kèm nhãn Chờ duyệt', 'Mở tab mới được']),
    C('Các khối thông tin ở trang chi tiết', 'P0', 'Phiếu Chờ duyệt có vận chuyển công ty và bốc xếp.', ['1. Mở chi tiết, xem từng tab'], '',
      ['Tab Thông tin chung: Loại, Phiếu đề nghị nhập kho, Người giao hàng, Kho nhập, Người đề nghị, Ghi chú',
       'Tab Vận chuyển: Tuyến đường, Số km dự kiến, Số km chốt, Chuyến xe, Ghi chú vận chuyển; tab Bốc xếp luôn có',
       'File đính kèm: tên, dung lượng, mở / tải được', 'Bảng hàng hoá có dòng Tổng cộng SL đề nghị, SL thực nhập, SL nhập']),
    C('Các ô ở trang chi tiết chỉ đọc', 'P0', 'Đang ở trang chi tiết.', ['1. Thử gõ vào các ô'], '', ['Mọi ô khóa, không có nút Lưu']),
    C('Dữ liệu chi tiết khớp với dữ liệu đã nhập và dòng trên bảng', 'P0', 'Phiếu vừa Lưu và nhập.', ['1. So chi tiết với dữ liệu đã nhập và dòng trên danh sách'], '',
      ['Mọi trường, SL, vị trí khớp', 'Số hiển thị dạng 1,234,567.89']),
    C('Chi tiết phiếu đang xếp hàng', 'P2', 'Phiếu Đang đi xếp hàng.', ['1. Mở chi tiết'], '', ['Bảng có thêm cột Nhóm, Người đi xếp']),
    C('Chi tiết phiếu không có bốc xếp', 'P2', 'Phiếu không khai bốc xếp.', ['1. Mở tab Bốc xếp'], '', ['Hiện "Không có thông tin bốc xếp"']),
    C('Chi tiết phiếu Không duyệt', 'P1', 'Phiếu Không duyệt.', ['1. Mở chi tiết'], '', ['Có "Lý do không duyệt"; nút Tạo phiếu xuất lại (với người tạo)']),
    C('Thanh nút ở trang chi tiết khớp cột Hành động', 'P1', 'Phiếu Chờ duyệt, đăng nhập TK-KT.', ['1. So thanh nút cuối trang với cột Hành động'], '',
      ['Cùng bộ nút (trừ Xem lịch sử) + Quay lại']),
    C('Mở chi tiết phiếu ngoài phạm vi', 'P0', 'TK-Z; phiếu Chờ duyệt của người khác.', ['1. Dán đường dẫn trang chi tiết'], '',
      ['Báo "Không tìm thấy phiếu nhập kho hoặc bạn không có quyền xem." và về danh sách']),
    C('Phiếu đang đi xếp hàng ai cũng mở được qua liên kết', 'P2', 'Phiếu Đang đi xếp hàng của TK-TK; TK-Z.', ['1. TK-Z dán đường dẫn chi tiết phiếu'], '',
      ['Xem được trang chi tiết, không có nút thao tác của người tạo']),
    C('Quay lại từ chi tiết giữ bộ lọc và trang', 'P1', 'Danh sách đang lọc, ở trang 2.', ['1. Mở chi tiết 1 phiếu', '2. Bấm Quay lại'], '',
      ['Về danh sách, giữ bộ lọc (trong 10 phút)']),
]

# ------------------------------------------------------------------ XII. IN PHIẾU
S_IN = [
    C('In phiếu nhập kho', 'P0', 'Phiếu Chờ duyệt.', ['1. Bấm In phiếu', '2. Bấm In'], '',
      ['Cửa sổ "Xem trước phiếu nhập kho <mã>": tiêu đề công ty của phiếu, "PHIẾU NHẬP KHO", mã phiếu, đề nghị nhập kho, loại nhập, ngày lập, '
       'người đề nghị, người giao hàng, người lập, ghi chú', 'Bảng hàng hoá × vị trí; khối ký Người lập phiếu – Người giao hàng/NVKD – Thủ kho – Trưởng phòng Logistic',
       'Bấm In mở hộp in của trình duyệt']),
    C('In phiếu đang xếp hàng in vị trí dự kiến', 'P2', 'Phiếu Đang đi xếp hàng.', ['1. Bấm In phiếu'], '', ['Bản in hiện vị trí dự kiến']),
    C('In dự kiến ở trang Nhập kho', 'P2', 'Đang ở trang Nhập kho.', ['1. Bấm In dự kiến'], '', ['Mở "Xem trước phiếu nhập kho <mã>" với dữ liệu đã lưu']),
    C('In phiếu xếp hàng', 'P2', 'Phiếu 1 có dòng và người đi xếp.', ['1. Ở trang Phiếu đi xếp hàng bấm In ở Phiếu 1'], '',
      ['Nhóm được lưu, mở "Xem trước phiếu xếp hàng 1 — <mã>"', 'Nút In chỉ hiện ở phiếu có dòng và đã chọn người đi xếp']),
    C('In barcode lô hàng', 'P2', 'Phiếu đã nhập kho.', ['1. Bấm In barcode', '2. Chọn Khổ giấy, bấm In barcode'], '',
      ['Trang có Nhà cung cấp, Năm sản xuất, Khổ giấy và bảng lô', 'Chưa chọn khổ giấy thì nút in bị khóa', 'Xem trước tem rồi bấm In']),
    C('Phiếu chưa nhập kho không in barcode được', 'P2', 'Phiếu Đang đi xếp hàng.', ['1. Xem nút', '2. Dán đường dẫn trang In barcode'], '',
      ['Không có nút In barcode', 'Báo "Phiếu chưa nhập kho (chưa có lô) hoặc bạn không có quyền."']),
    C('Đóng cửa sổ xem trước', 'P2', 'Đang mở cửa sổ xem trước.', ['1. Bấm dấu x'], '', ['Cửa sổ đóng, không ghi dữ liệu gì']),
]

# ------------------------------------------------------------------ XV. RÀNG BUỘC
S_RB = [
    C('Luồng chính đến Đã hạch toán', 'P0', 'ĐN-1 Chờ duyệt; ghi tồn H1 trước.',
      ['1. TK-TK tạo phiếu', '2. Lập phiếu xếp hàng', '3. Nhập kho, Lưu và nhập', '4. TK-KT tạo phiếu nhập hàng, hoàn thành'], '',
      ['Trạng thái lần lượt: Đang tạo (Đang đi xếp hàng > Đang nhập kho) > Chờ duyệt > Đang hạch toán > Đã hạch toán',
       'ĐN-1: Đang nhập kho > Đã nhập kho > …; tồn cộng đúng 1 lần ở bước 3']),
    C('Luồng Không duyệt > Xuất lại > Nhập lại', 'P0', 'Phiếu Chờ duyệt.',
      ['1. TK-KT Không duyệt', '2. TK-TK Xuất lại', '3. TK-TK Nhập lại, Lưu và nhập', '4. TK-KT tạo phiếu nhập hàng cho phiếu mới'], '',
      ['Tồn: giữ nguyên ở bước 1, về như cũ ở bước 2, cộng lại ở bước 3', 'Phiếu gốc Đã nhập lại; phiếu mới đi tiếp luồng chính']),
    C('Phiếu xuất lại xuất hiện ở màn Phiếu xuất điều chỉnh sai số liệu', 'P1', 'Vừa xuất lại.', ['1. Vào menu Kho > Xuất kho > Phiếu xuất điều chỉnh sai số liệu'], '',
      ['Có phiếu PXL-xxxxx ứng với phiếu nhập kho']),
    C('Đề nghị đã có phiếu không còn trong cửa sổ chọn', 'P1', 'ĐN-1 đã có phiếu nhập kho.', ['1. Tạo mới, mở cửa sổ chọn đề nghị'], '',
      ['ĐN-1 không còn trong danh sách (đã hết Chờ duyệt)']),
    C('Tồn ở báo cáo kho khớp sau Lưu và nhập', 'P0', 'Vừa Lưu và nhập H1 SL 2 tại V1.', ['1. Mở menu ' + TON], '',
      ['Tồn H1 tại kho K1 / vị trí V1 tăng 2 so với trước']),
    C('Phiếu Đã hạch toán đi tiếp sang màn báo hàng thừa thiếu', 'P2', 'Phiếu Đã hạch toán.', ['1. Vào menu Kho > Nhập kho > Phiếu nhập kho chờ báo thừa, thiếu'], '',
      ['Phiếu có trong danh sách chờ báo thừa, thiếu']),
    C('Chuyến xe gắn vào phiếu hiện ở màn Chuyến xe chở hàng', 'P2', 'Phiếu có vận chuyển công ty.', ['1. Mở chuyến xe ở menu Vận chuyển > Chuyến xe > Chuyến xe chở hàng'], '',
      ['Chuyến có phiếu nhập kho gắn kèm']),
]

# ------------------------------------------------------------------ XVI. PHÂN QUYỀN
K.update(
    pre_an_nut='TK-TK2 (thủ kho khác) và TK-Z mở phiếu của TK-TK ở các trạng thái.',
    exp_an_nut=['Không có Nhập kho / Sửa phiếu / Hủy / Tạo phiếu xuất lại / Tạo phiếu nhập lại với người không phải người tạo',
                'Không có Tạo phiếu nhập hàng / Không duyệt với người không có "Kế toán kho"'],
    pre_url='TK-Z; phiếu Chờ duyệt của người khác.',
    exp_url=['Báo "Không tìm thấy phiếu nhập kho hoặc bạn không có quyền xem." và về danh sách, không lộ dữ liệu'],
    pre_doi_quyen='TK-KT có "Kế toán kho"; phiếu Chờ duyệt.', man_doi_quyen='hộp Không duyệt của phiếu',
    nut_doi_quyen='Không duyệt (sau khi nhập lý do)',
    exp_doi_quyen=['Bị chặn: "Bạn không có quyền không duyệt phiếu này."', 'Phiếu vẫn Chờ duyệt'],
)
S_QUYEN = [
    C('Vào màn không cần quyền riêng: chỉ thấy phiếu mình tạo', 'P0', 'TK-Z không quyền, chưa tạo phiếu nào.',
      ['1. Đăng nhập TK-Z', '2. Vào menu ' + MENU], 'TK-Z',
      ['Mục menu "Phiếu nhập kho" hiện ở cả 2 phân hệ', 'Danh sách trống "Không có dữ liệu phù hợp."',
       'Không có ô Công ty / Phòng ban ở Tìm kiếm nâng cao']),
    C('Phạm vi "Xem phiếu nhập kho theo tổng công ty"', 'P0', 'TK-ALL.', ['1. Đăng nhập TK-ALL, vào màn', '2. Bấm Tìm kiếm nâng cao'], '',
      ['Thấy phiếu mọi công ty (trừ phiếu Đang tạo của người khác)', 'Có ô Công ty và Phòng ban']),
    C('Phạm vi "Xem phiếu nhập kho theo công ty"', 'P0', 'TK-CTY.', ['1. Đăng nhập TK-CTY, vào màn'], '',
      ['Chỉ phiếu thuộc công ty đang làm việc và phiếu mình tạo']),
    C('Phạm vi "Xem phiếu nhập kho theo phòng ban"', 'P1', 'TK-PB quản lý 1 phòng.', ['1. Đăng nhập TK-PB, vào màn'], '',
      ['Chỉ phiếu thuộc phòng ban được giao quản lý và phiếu mình tạo']),
    C('Thủ kho có "Xem tất cả phiếu xuất nhập kho"', 'P1', 'TK-TK được gán thêm quyền này.', ['1. Đăng nhập TK-TK, vào màn'], '',
      ['Thấy phiếu đã gửi của kho K1 do người khác tạo']),
    C('Kế toán kho thấy phiếu đã gửi của công ty', 'P0', 'TK-KT; có phiếu Chờ duyệt kho K1 do TK-TK tạo và phiếu Đang tạo.',
      ['1. Đăng nhập TK-KT, vào màn', '2. Lọc Trạng thái = Chờ duyệt'], '',
      ['Thấy phiếu Chờ duyệt của công ty, có nút Tạo phiếu nhập hàng, Không duyệt', 'Không thấy phiếu Đang tạo của TK-TK']),
    C('Chỉ thủ kho của kho nhập mới tạo được phiếu', 'P0', 'TK-Z không phải thủ kho; ĐN-1 Chờ duyệt.', ['1. TK-Z mở trang tạo bằng đường dẫn kèm ĐN-1', '2. Bấm Lưu'], '',
      ['Báo "Chỉ thủ kho của kho nhập mới tạo được phiếu nhập kho từ đề nghị đang chờ duyệt."; không tạo phiếu']),
    C('Super admin thao tác như người tạo', 'P2', 'Tài khoản Super admin; phiếu Đang nhập kho của TK-TK.', ['1. Mở phiếu bằng Super admin'], '',
      ['Có Sửa phiếu / Lưu và nhập; tạo được phiếu ở mọi kho']),
] + phan_quyen_chung(K)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', danh_so(hien_thi(K))),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', danh_so(tim_kiem(K))),
    ('III', 'THÊM MỚI', danh_so(S_THEM)),
    ('IV', 'CHỈNH SỬA', danh_so(S_SUA)),
    ('V', 'GỬI DUYỆT', danh_so(S_GUI)),
    ('VI', 'DUYỆT PHIẾU', danh_so(S_DUYET)),
    ('VII', 'KHÔNG DUYỆT PHIẾU', danh_so(S_KD)),
    ('VIII', 'HỦY PHIẾU', danh_so(S_HUY)),
    ('IX', 'LỊCH SỬ THAY ĐỔI', danh_so(lich_su(K))),
    ('X', 'XEM CHI TIẾT PHIẾU NHẬP KHO', danh_so(S_XEM)),
    ('XI', 'IN PHIẾU', danh_so(S_IN)),
    ('XII', 'TÙY CHỈNH CỘT', danh_so(tuy_chinh_cot(K))),
    ('XIII', 'XUẤT DANH SÁCH EXCEL', danh_so(xuat_excel(K))),
    ('XIV', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', danh_so(S_RB)),
    ('XV', 'PHÂN QUYỀN', danh_so(S_QUYEN)),
]

if __name__ == '__main__':
    n = build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='phieu')
    print('Số nhóm: %d' % len(SECTIONS))
