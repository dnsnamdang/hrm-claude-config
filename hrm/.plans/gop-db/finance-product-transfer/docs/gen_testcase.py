# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu điều chuyển hàng" (STT 204) — KHUÔN CHUẨN tab "13. DM quốc gia" (user chốt 03/11/2026), loại 'phieu'.

Bản cũ (khuôn tc_engine + nhóm TC-ROLE, sinh 02/11) giữ ở gen_testcase_v1.py để tra. Bản này giữ mọi case nghiệp vụ cũ
(đưa vào đúng nhóm chuẩn, sửa câu chữ theo giọng tab Quốc gia) và bổ sung case theo checklist "Mẫu tài liệu.xlsx"
(case chung sinh từ _tc_phieu_chung.py).
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

TEN = 'Phiếu điều chuyển hàng'
MODULE = 'Phiếu điều chuyển hàng'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SHEET = 'Trang tính1'
NGAY = '03/11/2026'


def L_(*lines):
    return '\n'.join(lines)


MENU = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Điều chuyển > Phiếu điều chuyển hàng'
KHO = 'PTT - Phan Trọng Tuệ'
KX = 'PTT01 - Phan Trọng Tuệ - Hàng bán'
KN = 'PTT03 - Phan Trọng Tuệ - Hàng khách gửi'
H1 = '2Q-INOX300 - Khay inox chữ nhật kích thước 300X400X50 (ĐVT Cái)'
H2 = 'ENEO-700-V5262 - Dầu ENEOS DEO CK-4 15W40 (ĐVT Xô 18L)'
BC = 'Tra cứu - thông báo > Tra cứu tồn kho > Hàng có thể bán theo công ty'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '-  TK-KT: nhân viên công ty TPE, có quyền "Kế toán kho" + "Xem phiếu điều chuyển hàng theo - công ty".',
    '-  TK-KT2: cùng công ty, có "Kế toán kho" (để kiểm phiếu Đang tạo của người khác).',
    '-  TK-TCT: có "Xem phiếu điều chuyển hàng theo - tổng công ty", không có "Kế toán kho". TK-Z: không có quyền nào của màn.',
    '-  Kho vật lý ' + KHO + '; kho xuất ' + KX + '; kho nhập ' + KN + '.',
    '-  Hàng H1: ' + H1 + ', đang có tồn ở kho xuất; H2: ' + H2 + ' (có ĐVT hệ số khác 1).',
    '-  Phiếu A: phiếu Đang tạo do TK-KT lập (1 dòng H1, SL 1). Phiếu B: một phiếu Đã hạch toán có sẵn (vd PDCH-01118).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Phiếu điều chuyển hàng" chuyển hàng giữa 2 KHO KẾ TOÁN trong cùng 1 KHO VẬT LÝ (hàng không di chuyển, chỉ đổi kho hạch toán).',
        'Luồng: chọn Kho vật lý > Kho xuất, Kho nhập > Thêm hàng hóa, nhập SL chuyển, ĐVT > "Lưu nháp" (Đang tạo, chưa đụng tồn) hoặc '
        '"Lưu và duyệt" (hạch toán ngay: trừ tồn kho xuất, cộng tồn kho nhập, tính giá vốn, ghi Nợ 156 / Có 156, khóa phiếu).',
        'Đường vào: menu ' + MENU + '.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới, Lưu nháp, Lưu và tiếp tục, Lưu và duyệt, '
        'Sửa, Xem chi tiết, Xóa, In phiếu, In danh sách, Xuất Excel, Lịch sử. Không có Gửi duyệt, Không duyệt, Hủy phiếu, Khóa, Import.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi xem (xét lần lượt): quản trị hoặc "… theo - tổng công ty" > mọi công ty; "… theo - công ty" > công ty mình; '
        'không có > chỉ phiếu mình lập.',
        'Phiếu Đang tạo chỉ người lập nhìn thấy, với mọi cấp quyền.',
        'Ô Kho vật lý: kho đang hoạt động có kho kế toán của công ty người dùng. Ô Kho xuất / Kho nhập trên form: kho kế toán '
        'đang hoạt động thuộc đúng kho vật lý đã chọn.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Phiếu ngoài phạm vi: không hiện; mở đường dẫn trực tiếp thì báo "Bạn không có quyền xem phiếu này".',
        '-  Nút Sửa / Xóa ẨN HẲN với phiếu Đã hạch toán hoặc phiếu không do mình lập.',
        '-  Nút Tạo mới ẨN khi không có quyền "Kế toán kho".',
        '-  Cửa sổ chọn hàng không nhận hàng tạm (ngoài danh mục) và hàng đã có trong phiếu.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" lọc theo ngày lập phiếu; ô "Ngày hạch toán" lọc theo ngày duyệt (phiếu Đang tạo không có). Tính cả 2 đầu mút.',
        'Bộ lọc được giữ khi mở trang chi tiết / sửa rồi quay lại trong 10 phút; vào màn khác qua menu thì về mặc định.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Phiếu (Số phiếu PDCH-xxxxx, Kho vật lý, Kho xuất, Kho nhập, Ghi chú, File đính kèm, Trạng thái, Ngày hạch toán) + nhiều dòng '
        'hàng (Tên, Model, Mã hàng, SL chuyển, ĐVT, Đơn giá vốn, Thành tiền vốn, TK nợ 156, TK có 156).',
        'Trạng thái: Đang tạo > Đã hạch toán (một chiều, không hủy). Phiếu Đang tạo xóa được.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  Kho xuất khác Kho nhập. Một hàng + ĐVT chỉ 1 dòng.',
        '-  SL chuyển > 0 và không vượt SL tồn (tồn quy theo ĐVT). Vượt tồn báo đỏ, KHÔNG tự sửa số.',
        '-  Lưu nháp chỉ bắt buộc Kho vật lý; Lưu và duyệt bắt buộc đủ kho + ít nhất 1 dòng có SL, ĐVT.',
        '-  Hàng đang kiểm kho tại kho vật lý không chuyển được.',
    )),
    ('7. Phân quyền cấp', L_(
        '-  "Kế toán kho": nút Tạo mới, lập, lưu, duyệt; sửa / xóa phiếu Đang tạo của mình.',
        '-  "Xem phiếu điều chuyển hàng theo - tổng công ty" / "… - công ty": phạm vi xem như mục 2.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N": N = tổng phiếu khớp bộ lọc và phạm vi.',
        'Đơn giá vốn = (giá trị tồn kho xuất trước - sau khi trừ) / SL quy đổi; Thành tiền vốn = SL quy đổi × Đơn giá vốn.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        'Các bẫy dễ sai nhất của màn này, QA đọc trước khi test:',
        '-  "Lưu và duyệt" là hạch toán NGAY (không có bước gửi duyệt / người duyệt khác); phiếu đã hạch toán khóa vĩnh viễn.',
        '-  Lưu nháp KHÔNG đụng tồn; muốn đưa hàng về kho cũ thì lập phiếu ngược chiều.',
        '-  Bản in danh sách tối đa 2,000 dòng. Kiểm tồn kho: dùng menu ' + BC + ' hoặc cột SL tồn trên form.',
        '-  Số theo chuẩn quốc tế 1,400,000 · 0.5. Cột KQ thực tế, DNS check để trống cho tester điền.',
    )),
]

K = dict(
    menu=MENU,
    tieu_de='Phiếu điều chuyển hàng',
    pre_mo='TK-KT đã đăng nhập, có phiếu trong phạm vi xem.',
    pre_nut='TK-KT (có "Kế toán kho") đã đăng nhập.',
    exp_nut=['Thanh công cụ có: Tạo mới, Xuất Excel, In danh sách, Cấu hình cột hiển thị',
             'Khối tìm kiếm có ô "Tìm theo số phiếu...", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
             'Không có nút Import'],
    cot=['STT', 'Số phiếu', 'Ngày hạch toán', 'Kho vật lý', 'Kho xuất', 'Kho nhập', 'Người tạo', 'Ngày tạo', 'Trạng thái', 'Hành động'],
    cot_an=['Ghi chú', 'Người cập nhật', 'Ngày cập nhật'],
    tong_cot=13,
    cot_khoa=['STT', 'Số phiếu', 'Hành động'],
    cot_bo_thu='Người tạo',
    pre_du_lieu='TK-KT vừa Lưu nháp phiếu A và có phiếu B Đã hạch toán.',
    exp_du_lieu=['Số phiếu dạng PDCH-<5 chữ số>, là liên kết', 'Kho vật lý dạng "Mã - Tên kho"; Kho xuất, Kho nhập đúng kho đã chọn',
                 'Người tạo dạng "Họ tên - Mã phòng ban"',
                 'Phiếu A: Trạng thái "Đang tạo", Ngày hạch toán để TRỐNG', 'Phiếu B: "Đã hạch toán", có Ngày hạch toán'],
    trang_thai=[('Đang tạo', 'xám'), ('Đã hạch toán', 'xanh lá')],
    pre_rong='TK-Z chưa lập phiếu nào, không có quyền xem.',
    rong_bang='Không có dữ liệu phù hợp bộ lọc.',
    rong_chan='Không có phiếu nào.',
    sap_xep=['Số phiếu', 'Ngày hạch toán', 'Ngày tạo'],
    khong_sap_xep=['STT', 'Kho vật lý', 'Kho xuất', 'Kho nhập', 'Người tạo', 'Trạng thái', 'Hành động'],
    ma='Số phiếu', vd_ma='PDCH-01118', vd_mot_phan='0111', placeholder='Tìm theo số phiếu...',
    loc_text=('Tên hàng hóa', 'Khay inox chữ nhật', 'khay inox chu nhat'),
    loc_list=['Công ty – Phòng ban', 'Kho vật lý', 'Kho xuất', 'Kho nhập', 'Trạng thái', 'Người tạo', 'Mã hàng hóa', 'Tên hàng hóa',
              'Ngày tạo', 'Ngày hạch toán'],
    loc_chon=('Trạng thái', 'Đã hạch toán'),
    loc_ket_hop='Kho vật lý = ' + KHO + ', Trạng thái = Đã hạch toán, nhập Mã hàng hóa "INOX300" rồi Enter',
    td_rong='Kho vật lý: ' + KHO + '; Trạng thái: Đang tạo; Người tạo: người chưa lập phiếu nào',
    form_tao='Thêm phiếu điều chuyển hàng', nut_quay_lai='Quay lại', truong_nhap_thu='Ghi chú',
    td_nhap_thu='Ghi chú: "Chuyển hàng khách gửi"', nut_luu_chinh='Lưu nháp',
    lich_su_title='Lịch sử thay đổi: <số phiếu>', nut_lich_su='Lịch sử',
    excel=dict(title='Chọn trường xuất file', so_truong=9,
               truong=['Số phiếu', 'Ngày hạch toán', 'Kho vật lý', 'Kho xuất', 'Kho nhập', 'Người tạo', 'Ngày tạo', 'Trạng thái', 'Ghi chú'],
               mac_dinh='Tích sẵn các trường đang hiện trên bảng, dòng đếm "Đang chọn 8/9 trường" (Ghi chú chưa tích)',
               file='Danh-sach-phieu-dieu-chuyen-hang-<yyyy-mm-dd>.xlsx', tieu_de='DANH SÁCH PHIẾU ĐIỀU CHUYỂN HÀNG', bo_thu='Người tạo',
               exp_them=['Trong lúc xuất, chữ trên nút Xuất Excel đổi thành tiến độ "Đang tải x/y..."'],
               rong=['Báo "Không có dữ liệu để xuất"', 'Không tải file nào']),
)

# ------------------------------------------------------------------ I. HIỂN THỊ (riêng)
K['hien_thi_rieng'] = [
    C('Nút cột Hành động theo trạng thái', 'P0', 'TK-KT có phiếu A (Đang tạo, mình lập) và phiếu B (Đã hạch toán).',
      ['1. Xem cột Hành động dòng phiếu A và B'], '',
      ['Phiếu A: Sửa, Xóa hiện ngoài; In phiếu, Lịch sử trong nút ba chấm "Hành động khác"',
       'Phiếu B: chỉ In phiếu, Lịch sử', 'Không có nút mờ bấm không được']),
]

# ------------------------------------------------------------------ II. LỌC (riêng)
K['loc_rieng'] = [
    C('Lọc theo Kho vật lý, Kho xuất, Kho nhập', 'P0', 'Có phiếu ở nhiều kho.',
      ['1. Bấm Tìm kiếm nâng cao', '2. Chọn Kho vật lý = ' + KHO, '3. Chọn Kho xuất = ' + KX, '4. Chọn Kho nhập = ' + KN], '',
      ['Mỗi lần chọn danh sách lọc ngay', 'Mọi dòng đúng kho đã chọn', 'Ô kho hiện dạng "Mã - Tên kho"']),
    C('Lọc theo Trạng thái', 'P0', 'Có phiếu Đang tạo (mình lập) và phiếu Đã hạch toán.', ['1. Chọn Trạng thái = Đang tạo', '2. Chọn Đã hạch toán', '3. Bỏ trống'], '',
      ['Đang tạo: chỉ phiếu Đang tạo do mình lập', 'Đã hạch toán: chỉ phiếu Đã hạch toán', 'Bỏ trống: hiện cả hai']),
    C('Lọc theo Người tạo', 'P1', 'Có phiếu của nhiều người lập.', ['1. Chọn Người tạo = TK-KT'], '', ['Chỉ phiếu do TK-KT lập']),
    C('Lọc theo Mã hàng hóa và Tên hàng hóa', 'P0', 'Có phiếu chứa H1.',
      ['1. Nhập Mã hàng hóa "INOX300", Enter', '2. Xóa, nhập Tên hàng hóa "Khay inox", Enter'], '',
      ['Chỉ phiếu có ít nhất 1 dòng hàng khớp (tìm gần đúng)', 'Gõ chưa Enter thì chưa lọc']),
    C('Lọc theo Ngày tạo và Ngày hạch toán', 'P1', 'Có phiếu tạo và hạch toán trong tháng 10/2026.',
      ['1. Ngày tạo từ 01/10/2026 đến 31/10/2026', '2. Bỏ, chọn Ngày hạch toán đến 19/10/2026'], '',
      ['Tính cả 2 đầu mút', 'Lọc Ngày hạch toán không ra phiếu Đang tạo']),
    C('Lọc theo Công ty – Phòng ban – Bộ phận', 'P2', 'TK-TCT.', ['1. Chọn Công ty', '2. Chọn Phòng ban, Bộ phận'], '',
      ['Phòng ban, Bộ phận có biểu tượng khóa tới khi chọn cấp trên', 'Kết quả theo tổ chức của người lập phiếu, vẫn trong phạm vi xem']),
    C('Ẩn ô lọc đang có giá trị', 'P2', 'Đang lọc Người tạo = TK-KT.', ['1. Cài đặt bộ lọc, bỏ tích ô Người tạo, Lưu'], '',
      ['Ô Người tạo biến mất và giá trị đang lọc ở ô đó bị xóa', 'Bảng tải lại không còn lọc theo Người tạo']),
]

# ------------------------------------------------------------------ III. THÊM MỚI
S_THEM = [
    C('Mở trang Thêm phiếu điều chuyển hàng', 'P0', 'TK-KT.', ['1. Bấm Tạo mới'], '',
      ['Tiêu đề "Thêm phiếu điều chuyển hàng"', 'Góc phải "<tên TK-KT> - <ngày giờ hiện tại>"',
       'Kho xuất, Kho nhập khóa; khối Chi tiết có dòng hướng dẫn "Chọn đủ Kho vật lý, Kho xuất và Kho nhập…", chưa có nút Thêm hàng hóa',
       'Chân trang: Lưu nháp, Lưu và duyệt, Lưu và tiếp tục, Quay lại']),
    C('Trường bắt buộc và giá trị mặc định', 'P1', 'Đang ở trang Thêm.', ['1. Quan sát nhãn và giá trị các ô'], '',
      ['Kho vật lý có dấu * (bắt buộc khi mọi nút lưu); Kho xuất, Kho nhập bắt buộc khi Lưu và duyệt',
       'Kho vật lý placeholder "Chọn kho vật lý"; Ghi chú placeholder "Nhập ghi chú"; các ô để trống']),
    C('Kho kế toán chỉ thuộc kho vật lý đã chọn', 'P0', 'Đang ở trang Thêm.', ['1. Chọn Kho vật lý = ' + KHO, '2. Mở ô Kho xuất'], '',
      ['Kho xuất, Kho nhập mở khóa', 'Chỉ liệt kê kho kế toán đang hoạt động thuộc ' + KHO + ' (PTT01, PTT02, PTT03)']),
    C('Đổi Kho vật lý thì xóa lựa chọn bên dưới', 'P0', 'Đã chọn 3 kho và 2 dòng hàng.', ['1. Đổi Kho vật lý sang kho khác'], '',
      ['Kho xuất, Kho nhập về trống', 'Bảng hàng trống "Chưa có hàng hóa nào trong phiếu"']),
    C('Thêm hàng hóa', 'P0', 'Đã chọn ' + KHO + ', ' + KX + ', ' + KN + '.',
      ['1. Bấm Thêm hàng hóa', '2. Tích H1, H2, bấm "Thêm 2 hàng hoá"'], '',
      ['Cửa sổ "Thêm hàng hoá" (20 dòng/trang) chỉ có hàng hóa trong danh mục; nút "Thêm 0 hàng hoá" mờ khi chưa tích',
       '2 dòng mới: Tên, Model, Mã hàng tự điền; ĐVT = đơn vị cơ bản; SL chuyển 0',
       'SL tồn = tồn có thể chuyển ở kho xuất; TK nợ, TK có = 156']),
    C('Thêm hàng đã có trong phiếu', 'P1', 'Phiếu đã có H1.', ['1. Thêm hàng hóa, tích lại H1, Thêm'], '',
      ['Không thêm dòng mới; báo "Hàng hóa đã có trong phiếu: <tên H1>"', 'Chỉ 1 thông báo, không hiện 2 thông báo ngược nhau']),
    C('Đổi ĐVT hoặc Kho xuất thì tính lại SL tồn', 'P1', 'H2 có ĐVT hệ số khác 1.',
      ['1. Đổi ĐVT dòng H2 sang đơn vị khác', '2. Đổi Kho xuất sang PTT02'], '',
      ['ĐVT hiện kèm hệ số dạng "Thùng (x24)"', 'SL tồn tính lại theo ĐVT / kho mới, có thể là số lẻ (vd 0.125), không bị làm tròn về 0']),
    C('Xóa dòng hàng', 'P1', 'Có 2 dòng.', ['1. Bấm thùng rác dòng 1', '2. Bấm Hủy', '3. Bấm lại, bấm Xác nhận'], '',
      ['Hộp "Xác nhận xóa hàng hóa": "Bạn có chắc chắn muốn xóa hàng "<tên>" khỏi phiếu?"', 'Hủy: giữ dòng; Xác nhận: bỏ dòng']),
    C('Lưu nháp với đầy đủ thông tin hợp lệ', 'P0', 'Đủ 3 kho, H1 SL 1; ghi SL tồn H1 trước.', ['1. Nhập Ghi chú, thêm 1 tệp pdf', '2. Bấm Lưu nháp'], 'Ghi chú: "Chuyển hàng khách gửi"',
      ['Báo "Lưu thành công", về danh sách', 'Phiếu mới đứng đầu, Số phiếu PDCH-xxxxx, Trạng thái Đang tạo, Ngày hạch toán trống',
       'SL tồn của H1 ở kho xuất KHÔNG đổi']),
    C('Lưu nháp chỉ cần Kho vật lý', 'P1', 'Đang ở trang Thêm.', ['1. Chỉ chọn Kho vật lý', '2. Bấm Lưu nháp'], '',
      ['Lưu được, phiếu Đang tạo không có kho xuất / nhập, không có dòng hàng']),
    C('Lưu nháp bỏ trống Kho vật lý', 'P0', 'Đang ở trang Thêm, chưa chọn gì.', ['1. Nhập Ghi chú', '2. Bấm Lưu nháp'], '',
      ['Dưới ô báo đỏ "Kho vật lý không được để trống"', 'Cuộn tới ô lỗi đầu tiên, không lưu']),
    C('Ghi nhận lịch sử Tạo mới sau khi lưu', 'P1', 'Vừa Lưu nháp phiếu mới.', ['1. Bấm Lịch sử ở dòng phiếu'], '',
      ['Có mốc Tạo mới, người thực hiện TK-KT, thời điểm lưu']),
    C('Kho xuất trùng Kho nhập', 'P0', 'Đang ở trang Thêm.', ['1. Chọn Kho xuất = Kho nhập = ' + KX, '2. Bấm Lưu nháp', '3. Đổi Kho nhập sang ' + KN], '',
      ['Dưới Kho nhập: "Kho xuất, kho nhập không được trùng nhau", không lưu', 'Đổi kho khác thì chữ đỏ mất ngay']),
    C('SL chuyển bằng 0 hoặc để trống', 'P0', 'Có dòng H1.', ['1. SL = 0, bấm Lưu và duyệt', '2. Xóa trống SL, bấm Lưu và duyệt'], '',
      ['0: "Phải lớn hơn 0" dưới ô', 'Trống: "Bắt buộc phải nhập"', 'Ô không gõ được số âm']),
    C('SL chuyển vượt tồn', 'P0', 'H2 SL tồn = n.', ['1. Nhập SL = n + 1', '2. Bấm Lưu nháp'], '',
      ['Dưới ô: "Số lượng chuyển vượt quá số lượng tồn (còn n)"', 'Số đã nhập GIỮ NGUYÊN, không bị tự sửa về n', 'Không lưu (kể cả Lưu nháp)']),
    C('SL chuyển số lẻ', 'P1', 'H1 tồn từ 1 trở lên.', ['1. Nhập SL 0.5', '2. Bấm Lưu nháp'], 'SL: 0.5', ['Lưu được, chi tiết hiện 0.5']),
    C('SL chuyển vượt mức tối đa', 'P2', 'Có dòng H1.', ['1. Nhập SL 1000000000'], 'SL: 1000000000',
      ['Ô không nhận quá 999,999,999 (hoặc báo lỗi dưới ô), không lưu']),
    C('Bỏ trống ĐVT', 'P1', 'Có dòng H2.', ['1. Xóa ĐVT dòng H2', '2. Bấm Lưu và duyệt'], '', ['Báo "Bắt buộc phải chọn đơn vị tính", không lưu']),
    C('Hàng đang kiểm kho', 'P1', 'H1 đang trong đợt kiểm kê theo hàng hóa (chưa xong) tại ' + KHO + '.', ['1. Lập phiếu có H1, bấm Lưu nháp'], '',
      ['Báo "Hàng hóa đang được kiểm kho, không thể điều chuyển" tại dòng H1, không lưu']),
    C('Ghi chú đúng 255 ký tự thì lưu được', 'P2', 'Đang ở trang Thêm, đã chọn Kho vật lý.', ['1. Nhập Ghi chú 255 ký tự', '2. Bấm Lưu nháp'], 'Chuỗi 255 ký tự',
      ['Lưu thành công, chi tiết hiện đủ nội dung']),
    C('Ghi chú vượt 255 ký tự', 'P2', 'Đang ở trang Thêm.', ['1. Nhập Ghi chú 256 ký tự', '2. Bấm Lưu nháp'], 'Chuỗi 256 ký tự',
      ['Báo lỗi độ dài tại ô Ghi chú, không lưu']),
    C('Ghi chú có khoảng trắng đầu và cuối', 'P2', 'Đã chọn Kho vật lý.', ['1. Nhập Ghi chú có dấu cách 2 đầu', '2. Lưu nháp, mở chi tiết'], 'Ghi chú: "  Chuyển kho  "',
      ['Chi tiết hiện "Chuyển kho" đã bỏ khoảng trắng 2 đầu']),
    C('Đính kèm tệp', 'P2', 'Đang ở trang Thêm.', ['1. Bấm Thêm tài liệu, chọn 1 tệp pdf', '2. Chọn tệp .docx', '3. Chọn tệp pdf trên 20MB', '4. Lưu nháp, mở chi tiết'], '',
      ['Tệp pdf hiện ngay trong lưới, xem trước / tải xuống được', '.docx: "Chỉ nhận file pdf, png, jpg, jpeg"',
       'Tệp quá lớn: "Dung lượng tối đa 20MB"', 'Chi tiết có tệp, cột Dung lượng có số']),
    C('Lưu và tiếp tục với dữ liệu hợp lệ', 'P1', 'Đủ dữ liệu.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Báo "Lưu thành công"; phiếu lưu ở trạng thái Đang tạo', 'Ở lại trang Thêm, form trắng hoàn toàn (kể cả bảng hàng)']),
    C('Lưu và tiếp tục khi thiếu Kho vật lý', 'P1', 'Đang ở trang Thêm, chưa chọn Kho vật lý.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Báo "Kho vật lý không được để trống", không lưu, ở lại form']),
    C('Lưu và tiếp tục khi SL không hợp lệ', 'P1', 'Có dòng H1 SL 0.', ['1. Bấm Lưu và tiếp tục'], '', ['Báo "Phải lớn hơn 0", không lưu']),
    C('Lưu và tiếp tục khi trùng kho', 'P2', 'Kho xuất = Kho nhập.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Báo "Kho xuất, kho nhập không được trùng nhau", không lưu']),
    C('Bấm Quay lại ngay sau Lưu và tiếp tục thì không hỏi', 'P1', 'Vừa Lưu và tiếp tục, form trống.', ['1. Bấm Quay lại'], '',
      ['Về danh sách ngay, không hiện hộp "Thông tin chưa lưu"; danh sách có phiếu vừa lưu']),
    C('Không có quyền Kế toán kho mà vẫn lưu', 'P1', 'TK-TCT mở trực tiếp trang Thêm.', ['1. Dán đường dẫn trang Thêm', '2. Nhập dữ liệu, bấm Lưu nháp'], '',
      ['Báo "Bạn không có quyền lập phiếu điều chuyển hàng", không lưu']),
] + them_moi_dong_form(K)

# ------------------------------------------------------------------ IV. CHỈNH SỬA
S_SUA = [
    C('Mở trang Sửa phiếu Đang tạo', 'P0', 'Phiếu A của TK-KT.', ['1. Bấm Sửa ở dòng phiếu A'], '',
      ['Trang "Sửa phiếu điều chuyển hàng" nạp đúng Kho vật lý, Kho xuất, Kho nhập, Ghi chú, tệp, dòng hàng', 'Cột SL tồn được tính lại',
       'Chân trang Lưu nháp, Lưu và duyệt, Quay lại; KHÔNG có Lưu và tiếp tục']),
    C('Sửa một trường', 'P0', 'Phiếu A.', ['1. Đổi SL 1 sang 3', '2. Bấm Lưu nháp'], 'SL: 3',
      ['Báo "Cập nhật thành công", về danh sách', 'Chi tiết hiện SL 3']),
    C('Sửa nhiều trường cùng lúc', 'P0', 'Phiếu A.', ['1. Đổi Kho nhập, Ghi chú, thêm 1 dòng H2', '2. Bấm Lưu nháp', '3. Xem Lịch sử'], '',
      ['Lưu thành công', 'Lịch sử 1 mốc "Thay đổi thông tin": Kho nhập cũ > mới, Ghi chú cũ > mới; Danh sách hàng hóa: thêm mới H2']),
    C('Ngày và người cập nhật đổi theo', 'P1', 'Đã bật cột Người cập nhật, Ngày cập nhật ở Tùy chỉnh cột.', ['1. Sửa phiếu A bằng TK-KT, Lưu nháp', '2. Xem dòng phiếu'], '',
      ['Người cập nhật = TK-KT dạng "Họ tên - Mã phòng ban", Ngày cập nhật = thời điểm lưu']),
    C('Đổi Kho vật lý khi sửa', 'P1', 'Phiếu A có 1 dòng hàng.', ['1. Đổi Kho vật lý'], '',
      ['Kho xuất, Kho nhập và toàn bộ dòng hàng bị xóa như trang Thêm']),
    C('Gỡ tệp đã lưu', 'P2', 'Phiếu A có 2 tệp.', ['1. Xóa 1 tệp ở khối File đính kèm'], '',
      ['Tệp gỡ ngay khỏi phiếu, lịch sử ghi File đính kèm']),
    C('Validate khi sửa: trùng kho, vượt tồn', 'P0', 'Phiếu A.', ['1. Đặt Kho nhập = Kho xuất, Lưu nháp', '2. Sửa lại, nhập SL vượt tồn, Lưu nháp'], '',
      ['Bước 1: "Kho xuất, kho nhập không được trùng nhau"', 'Bước 2: "Số lượng chuyển vượt quá số lượng tồn (còn n)"', 'Không lưu']),
    C('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Ô SL đang báo "Phải lớn hơn 0".', ['1. Nhập SL 1'], '', ['Chữ đỏ biến mất ngay']),
    C('Kho hoặc hàng đã khóa vẫn hiện khi sửa', 'P2', 'Kho nhập của phiếu A vừa bị khóa ở danh mục.', ['1. Mở Sửa phiếu A'], '',
      ['Ô Kho nhập vẫn hiện đúng tên kho đã lưu', 'Kho đã khóa không có trong danh sách chọn mới']),
    C('Mở sửa không thay đổi gì rồi Quay lại', 'P1', 'Phiếu A.', ['1. Bấm Sửa', '2. Bấm Quay lại'], '', ['Về danh sách, không hỏi']),
    C('Sửa rồi trả về giá trị ban đầu', 'P2', 'Phiếu A.', ['1. Đổi Ghi chú', '2. Sửa về như cũ', '3. Bấm Quay lại'], '', ['Về danh sách, không hỏi']),
    C('Đã đổi dữ liệu rồi bấm Quay lại', 'P0', 'Đang sửa phiếu A, đã đổi Ghi chú.', ['1. Bấm Quay lại', '2. Bấm Ở lại', '3. Bấm Quay lại, bấm Thoát'], '',
      ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"', 'Ở lại: giữ dữ liệu đang sửa',
       'Thoát: về danh sách, phiếu A KHÔNG đổi']),
    C('Lưu nháp mà không đổi gì thì không ghi lịch sử', 'P1', 'Phiếu A.', ['1. Mở Sửa, bấm Lưu nháp ngay', '2. Xem Lịch sử'], '',
      ['Không sinh mốc Thay đổi thông tin mới']),
    C('Phiếu Đã hạch toán không sửa được', 'P0', 'Phiếu B.', ['1. Xem dòng phiếu B', '2. Dán đường dẫn trang Sửa phiếu B, bấm Lưu nháp'], '',
      ['Không có nút Sửa (ẩn hẳn)', 'Báo "Phiếu đã hạch toán hoặc bạn không có quyền sửa", dữ liệu không đổi']),
    C('Phiếu vừa bị duyệt ở tab khác', 'P2', 'Phiếu A mở trang Sửa ở 2 tab.', ['1. Tab 1 Lưu và duyệt', '2. Tab 2 Lưu nháp'], '',
      ['Tab 2 báo "Phiếu đã hạch toán hoặc bạn không có quyền sửa", không đổi dữ liệu']),
    C('Phiếu đã bị xóa ở tab khác', 'P2', 'Phiếu A mở trang Sửa ở tab 2; tab 1 đã xóa phiếu A.', ['1. Tab 2 bấm Lưu nháp'], '',
      ['Báo lỗi không tìm thấy phiếu / không có quyền, không tạo lại phiếu']),
]

# ------------------------------------------------------------------ V. XÓA
S_XOA = [
    C('Nút Xóa chỉ có ở phiếu Đang tạo của mình', 'P0', 'TK-KT có phiếu A; phiếu B Đã hạch toán; phiếu C Đang tạo của TK-KT2.', ['1. Xem cột Hành động'], '',
      ['Phiếu A có Xóa', 'Phiếu B không có Xóa', 'Phiếu C không hiện với TK-KT']),
    C('Hộp xác nhận nêu đúng số phiếu', 'P0', 'Phiếu A.', ['1. Bấm Xóa ở dòng phiếu A'], '',
      ['Hộp "Xác nhận xóa": "Bạn có chắc chắn muốn xóa phiếu điều chuyển hàng <số phiếu A>?"', 'Có nút Xóa, Hủy']),
    C('Bấm Hủy thì không xóa', 'P0', 'Đang mở hộp Xác nhận xóa.', ['1. Bấm Hủy'], '', ['Hộp đóng, phiếu A còn nguyên']),
    C('Xóa thành công', 'P0', 'Phiếu A; danh sách có N phiếu; ghi SL tồn H1.', ['1. Bấm Xóa, bấm Xóa trong hộp'], '',
      ['Báo "Xóa thành công"; phiếu A biến mất khỏi danh sách', 'Dòng tổng còn N − 1', 'Tồn kho không đổi (phiếu nháp chưa đụng tồn)']),
    C('Xóa từ trang Chi tiết', 'P1', 'Phiếu Đang tạo khác.', ['1. Mở chi tiết, bấm Xóa, xác nhận'], '', ['"Xóa thành công", quay về danh sách']),
    C('Xóa phiếu đã bị người khác xóa', 'P1', 'Phiếu A mở ở 2 tab; tab 1 đã xóa.', ['1. Tab 2 bấm Xóa, xác nhận'], '',
      ['Báo lỗi, không xóa thêm gì; tải lại danh sách không còn phiếu A']),
    C('Phiếu Đã hạch toán không xóa được', 'P0', 'Phiếu B.', ['1. Mở chi tiết phiếu B'], '',
      ['Không có nút Xóa', 'Nếu vẫn gửi yêu cầu xóa: "Phiếu đã hạch toán hoặc bạn không có quyền xóa"']),
    C('Xóa phiếu không ghi lịch sử', 'P2', 'Vừa xóa phiếu A.', ['1. Tìm phiếu A'], '',
      ['Không còn phiếu A ở danh sách, không có mốc lịch sử nào còn xem được']),
]

# ------------------------------------------------------------------ VI. DUYỆT PHIẾU (Lưu và duyệt)
S_DUYET = [
    C('Điều kiện hiện nút Lưu và duyệt', 'P0', 'TK-KT; phiếu A; phiếu B.', ['1. Mở trang Thêm', '2. Mở trang Sửa phiếu A', '3. Mở chi tiết phiếu B'], '',
      ['Trang Thêm và Sửa phiếu A có Lưu và duyệt', 'Phiếu B không có thao tác duyệt']),
    C('Hộp xác nhận Lưu và duyệt', 'P0', 'Phiếu đủ dữ liệu.', ['1. Bấm Lưu và duyệt', '2. Bấm Hủy'], '',
      ['Hộp "Xác nhận lưu và duyệt": "Bạn đồng ý lưu và duyệt?" (Xác nhận / Hủy)', 'Hủy: không lưu, ở lại form, dữ liệu còn nguyên']),
    C('Bắt buộc dữ liệu khi Lưu và duyệt', 'P0', 'Chỉ chọn Kho vật lý.', ['1. Bấm Lưu và duyệt, Xác nhận'], '',
      ['Báo đỏ dưới Kho xuất, Kho nhập', 'Báo "Phiếu phải có ít nhất một dòng hàng hóa"', 'Không lưu']),
    C('Lưu và duyệt ngay khi lập', 'P0', 'Ghi SL tồn H1 ở kho xuất (a) và kho nhập (b) trước khi duyệt.',
      ['1. Lập phiếu H1 SL 2 (ĐVT Cái), bấm Lưu và duyệt, Xác nhận', '2. Mở chi tiết phiếu', '3. Kiểm SL tồn H1 ở 2 kho'], '',
      ['Báo "Điều chuyển thành công", về danh sách; phiếu Đã hạch toán, Ngày hạch toán = lúc duyệt',
       'Chi tiết có Đơn giá vốn, Thành tiền vốn = 2 × Đơn giá vốn', 'Tồn kho xuất = a − 2; tồn kho nhập = b + 2']),
    C('Duyệt phiếu Đang tạo từ trang Sửa', 'P0', 'Phiếu A.', ['1. Sửa phiếu A, bấm Lưu và duyệt, Xác nhận', '2. Xem Lịch sử'], '',
      ['Phiếu A chuyển Đã hạch toán, tồn chuyển như case lập rồi duyệt ngay',
       'Lịch sử có mốc "Thay đổi trạng thái": Trạng thái Đang tạo > Đã hạch toán, người duyệt TK-KT, thời điểm duyệt']),
    C('Duyệt với ĐVT hệ số khác 1', 'P1', 'H2 có ĐVT hệ số k.', ['1. Lập phiếu H2 SL 1 theo ĐVT hệ số k, Lưu và duyệt'], '',
      ['Tồn kho xuất giảm k đơn vị cơ bản, kho nhập tăng k']),
    C('Vượt tồn hoặc hàng đang kiểm kho khi duyệt', 'P0', 'H1 SL tồn = n.', ['1. Nhập SL n + 1, Lưu và duyệt, Xác nhận'], '',
      ['Báo "Số lượng chuyển vượt quá số lượng tồn (còn n)", không lưu, không hạch toán']),
    C('Kho xuất không có tồn kế toán của hàng', 'P1', 'Hàng chưa từng có tồn kế toán ở kho xuất.', ['1. Lưu và duyệt'], '',
      ['Báo lỗi; toàn bộ thao tác bị hủy, không có phần nào được ghi (phiếu không được tạo, tồn không đổi)']),
    C('Bút toán sổ sau khi duyệt', 'P1', 'Phiếu vừa duyệt.', ['1. Tra sổ chi tiết tài khoản 156 theo số phiếu'], '',
      ['Mỗi dòng hàng có Thành tiền vốn > 0 có 1 cặp Nợ 156 / Có 156 = Thành tiền vốn, chứng từ = Số phiếu, ngày = Ngày hạch toán']),
    C('Phiếu đã hạch toán bị khóa', 'P0', 'Phiếu B.', ['1. Xem dòng phiếu B', '2. Mở chi tiết phiếu B'], '',
      ['Không có Sửa, Xóa (ẩn hẳn)', 'Chân trang chỉ In phiếu, Quay lại', 'Không có thao tác hủy hay duyệt lại']),
    C('Kho nhập chưa từng có hàng', 'P2', 'H1 chưa có tồn ở kho nhập.', ['1. Lập và duyệt phiếu chuyển H1 sang kho đó'], '',
      ['Duyệt thành công, kho nhập có tồn H1 = SL chuyển']),
    C('Tồn bị người khác dùng trước khi duyệt', 'P1', 'H1 tồn ở kho xuất = 3.',
      ['1. TK-KT mở form, nhập H1 SL 3 (chưa lưu)', '2. TK-KT2 duyệt phiếu chuyển H1 SL 2 cùng kho xuất', '3. TK-KT bấm Lưu và duyệt'], '',
      ['TK-KT bị báo "Số lượng chuyển vượt quá số lượng tồn (còn 1)", không hạch toán']),
]

# ------------------------------------------------------------------ LỊCH SỬ (riêng)
K['lich_su_rieng'] = [
    C('Lịch sử khi Lưu và duyệt ngay ở trang Thêm', 'P1', 'Phiếu lập rồi Lưu và duyệt ngay.', ['1. Bấm Lịch sử'], '',
      ['Có mốc Tạo mới với trạng thái Đã hạch toán']),
    C('Lịch sử dòng hàng khi sửa', 'P1', 'Phiếu A đã sửa: thêm H2, xóa H1, đổi ĐVT.', ['1. Bấm Lịch sử'], '',
      ['Danh sách hàng hóa ghi theo nhóm thêm mới / đã xóa / sửa số lượng, ĐVT']),
    C('Phiếu lập trước khi có màn này', 'P2', 'Phiếu cũ.', ['1. Bấm Lịch sử'], '', ['Hiện "Chưa có lịch sử thao tác nào."']),
]

# ------------------------------------------------------------------ XEM CHI TIẾT
S_XEM = [
    C('Bấm Số phiếu mở trang chi tiết', 'P0', 'Phiếu B.', ['1. Bấm Số phiếu B', '2. Quay lại, chuột phải Số phiếu > mở tab mới'], '',
      ['Mở trang "Chi tiết phiếu điều chuyển hàng: <số phiếu>"', 'Mở tab mới được']),
    C('Đầy đủ khối thông tin', 'P0', 'Phiếu B.', ['1. Mở chi tiết'], '',
      ['Khối Thông tin chung (góc phải "<Người tạo> - <ngày giờ tạo>"), File đính kèm, Chi tiết (STT, Tên hàng hóa, Model, Mã hàng, SL chuyển, ĐVT, '
       'Đơn giá vốn, Thành tiền vốn, TK nợ, TK có), khối Lịch sử thu gọn']),
    C('Các ô chỉ đọc, không có nút Lưu', 'P0', 'Đang ở chi tiết.', ['1. Thử sửa các ô'], '', ['Mọi ô khóa, không có nút Lưu']),
    C('Dữ liệu chi tiết khớp danh sách và dữ liệu đã lập', 'P0', 'Phiếu vừa duyệt.', ['1. So chi tiết với dòng trên bảng và dữ liệu đã nhập'], '',
      ['Kho, Ghi chú, dòng hàng, SL khớp', 'Đơn giá vốn, Thành tiền vốn dạng 1,234,567.89']),
    C('Chi tiết phiếu Đang tạo', 'P1', 'Phiếu A.', ['1. Bấm Số phiếu A'], '',
      ['Các ô chỉ đọc; không có cột SL tồn; Đơn giá vốn, Thành tiền vốn để trống', 'Chân trang: Sửa, In phiếu, Xóa, Quay lại']),
    C('Chi tiết phiếu Đã hạch toán', 'P1', 'Phiếu B.', ['1. Mở chi tiết'], '', ['Chân trang chỉ In phiếu, Quay lại']),
    C('Tệp đính kèm ở chi tiết', 'P2', 'Phiếu có tệp.', ['1. Bấm xem / tải tệp'], '', ['Xem trước, tải xuống được; cột Dung lượng có số']),
    C('Mở chi tiết phiếu ngoài phạm vi', 'P0', 'TK-Z; phiếu B.', ['1. Dán đường dẫn trang Chi tiết phiếu B'], '',
      ['Báo "Bạn không có quyền xem phiếu này", không lộ dữ liệu']),
    C('Quay lại từ chi tiết giữ bộ lọc', 'P1', 'Danh sách đang lọc Trạng thái = Đã hạch toán.', ['1. Mở chi tiết', '2. Bấm Quay lại'], '',
      ['Về danh sách, bộ lọc vẫn giữ (trong 10 phút)']),
]

# ------------------------------------------------------------------ IN PHIẾU
S_IN = [
    C('In phiếu', 'P0', 'Phiếu B.', ['1. Bấm In phiếu ở dòng B (hoặc ở chi tiết)', '2. Bấm In'], '',
      ['Cửa sổ "Xem trước phiếu <số phiếu>": tiêu đề công ty ghi trên phiếu, "PHIẾU ĐIỀU CHUYỂN HÀNG", Số phiếu, Kho vật lý, Kho xuất, Kho nhập, Ghi chú',
       'Bảng 10 cột: STT, Tên hàng hóa, Model, Mã hàng hóa, SL chuyển, ĐVT, Đơn giá vốn, Thành tiền vốn, TK nợ 156, TK có 156',
       'Ô ký "Người lập" có tên người lập', 'Bấm In mở hộp in của trình duyệt']),
    C('Tiêu đề bản in theo công ty trên phiếu', 'P1', 'Người in thuộc công ty khác công ty ghi trên phiếu (TK-TCT).', ['1. In phiếu B'], '',
      ['Tiêu đề bản in là công ty ghi trên phiếu, không theo người đang in']),
    C('In phiếu Đang tạo', 'P2', 'Phiếu A.', ['1. Bấm In phiếu'], '', ['Bản in hiện đủ dòng hàng; Đơn giá vốn, Thành tiền vốn để trống']),
    C('In danh sách', 'P0', 'Lọc Kho vật lý = ' + KHO + '.', ['1. Bấm In danh sách'], '',
      ['Cửa sổ "Xem trước danh sách phiếu điều chuyển hàng", tiêu đề "DANH SÁCH PHIẾU ĐIỀU CHUYỂN HÀNG", khổ ngang',
       '9 cột: STT, Số phiếu, Ngày hạch toán, Kho vật lý, Kho xuất, Kho nhập, Người lập, Ngày lập, Trạng thái', 'Đúng các dòng khớp bộ lọc (mọi trang)']),
    C('In danh sách quá 2,000 dòng', 'P2', 'Phạm vi trên 2,000 phiếu, không lọc.', ['1. Bấm In danh sách'], '',
      ['Không in; báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được…"']),
    C('Đóng cửa sổ xem trước', 'P2', 'Đang mở cửa sổ xem trước.', ['1. Bấm dấu x'], '', ['Cửa sổ đóng, danh sách giữ nguyên']),
]

# ------------------------------------------------------------------ RÀNG BUỘC
S_RB = [
    C('Luồng đầu cuối: nháp > sửa > duyệt > kiểm tồn', 'P0', 'Ghi tồn H1 ở kho xuất / nhập trước.',
      ['1. Lập phiếu H1 SL 1, Lưu nháp', '2. Kiểm menu ' + BC + ': tồn không đổi', '3. Sửa SL 2, Lưu và duyệt',
       '4. Kiểm lại tồn', '5. Xem Lịch sử, In phiếu'], '',
      ['Bước 2: tồn chưa đổi', 'Bước 4: kho xuất −2, kho nhập +2', 'Lịch sử: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái',
       'Bản in có Đơn giá vốn, Thành tiền vốn']),
    C('Chuyển ngược lại thay cho hủy', 'P1', 'Phiếu vừa duyệt ở luồng trên.',
      ['1. Lập phiếu Kho xuất = ' + KN + ', Kho nhập = ' + KX + ', H1 SL 2, Lưu và duyệt'], '',
      ['Tồn 2 kho trở về như trước luồng', 'Đơn giá vốn phiếu ngược bằng giá vốn đã chuyển sang']),
    C('Tồn ở màn Hàng có thể bán theo công ty đổi sau duyệt', 'P0', 'Vừa duyệt phiếu H1 SL 2.', ['1. Mở menu ' + BC], '',
      ['Tồn H1 ở kho xuất giảm 2, kho nhập tăng 2']),
    C('Phiếu xuất hàng lấy giá vốn theo lớp nhập do phiếu điều chuyển ghi', 'P2', 'Kho nhập vừa nhận H1 từ phiếu điều chuyển.',
      ['1. Lập phiếu xuất hàng H1 từ kho nhập', '2. Xem giá vốn'], '', ['Giá vốn xuất bằng Đơn giá vốn của phiếu điều chuyển (lớp nhập trước xuất trước)']),
    C('Kho vật lý đã có phiếu điều chuyển không xóa được', 'P2', 'Kho vật lý ' + KHO + ' có phiếu.', ['1. Vào menu Kho > Danh mục > Kho vật lý, xóa ' + KHO], '',
      ['Bị chặn, không xóa được kho']),
    C('Kho kế toán bị khóa không chọn được khi lập phiếu mới', 'P1', 'Khóa kho PTT02 ở danh mục.', ['1. Lập phiếu mới, chọn ' + KHO, '2. Mở ô Kho xuất'], '',
      ['PTT02 không có trong danh sách chọn']),
    C('Mã phiếu không trùng khi 2 người lưu cùng lúc', 'P1', 'TK-KT, TK-KT2.', ['1. Hai người cùng Lưu nháp gần như đồng thời'], '',
      ['2 phiếu có 2 số khác nhau, không lỗi']),
]

# ------------------------------------------------------------------ PHÂN QUYỀN
K.update(
    pre_an_nut='TK-TCT (không "Kế toán kho"); phiếu B Đã hạch toán; Quản trị hệ thống mở phiếu C (Đang tạo của TK-KT2).',
    exp_an_nut=['TK-TCT không có nút Tạo mới', 'Phiếu B không có Sửa, Xóa',
                'Quản trị mở phiếu C không có Sửa, Xóa (chỉ người lập được sửa / xóa)'],
    pre_url='TK-Z; phiếu B thuộc công ty khác.',
    exp_url=['Báo "Bạn không có quyền xem phiếu này", không lộ dữ liệu'],
    pre_doi_quyen='TK-KT có "Kế toán kho" đang ở trang Thêm.', man_doi_quyen='trang Thêm phiếu đã nhập đủ dữ liệu',
    nut_doi_quyen='Lưu nháp',
    exp_doi_quyen=['Báo "Bạn không có quyền lập phiếu điều chuyển hàng", không lưu'],
)
S_QUYEN = [
    C('Không có quyền nào: chỉ thấy phiếu mình lập, không có Tạo mới', 'P0', 'TK-Z.',
      ['1. Đăng nhập TK-Z', '2. Vào menu ' + MENU, '3. Dán đường dẫn trang Chi tiết của phiếu B'], 'Tài khoản TK-Z',
      ['Danh sách chỉ có phiếu do TK-Z lập (có thể rỗng: "Không có dữ liệu phù hợp bộ lọc.")', 'Không có nút Tạo mới',
       'Đường dẫn phiếu B: báo "Bạn không có quyền xem phiếu này"']),
    C('Có "Kế toán kho": có nút Tạo mới', 'P0', 'TK-KT.', ['1. Đăng nhập TK-KT', '2. Vào menu ' + MENU], '',
      ['Có nút Tạo mới, Xuất Excel, In danh sách, Cấu hình cột hiển thị', 'Phiếu Đang tạo của mình có Sửa, Xóa; phiếu Đã hạch toán chỉ In phiếu, Lịch sử']),
    C('Phạm vi "Xem phiếu điều chuyển hàng theo - tổng công ty"', 'P0', 'TK-TCT.', ['1. Đăng nhập TK-TCT, vào màn', '2. Đọc N, lọc Công ty khác'], '',
      ['Thấy phiếu Đã hạch toán của MỌI công ty', 'Không có nút Tạo mới (không có "Kế toán kho")']),
    C('Phạm vi "Xem phiếu điều chuyển hàng theo - công ty"', 'P0', 'TK-KT.', ['1. Đăng nhập TK-KT, vào màn', '2. Lọc Công ty = công ty khác'], '',
      ['Chỉ thấy phiếu có công ty = công ty của TK-KT', 'Lọc công ty khác: không có dòng nào']),
    C('Phiếu Đang tạo của người khác không hiện', 'P0', 'TK-KT2 có phiếu Đang tạo C; TK-TCT.',
      ['1. TK-KT đăng nhập, lọc Trạng thái = Đang tạo', '2. TK-TCT làm tương tự', '3. TK-KT dán đường dẫn Chi tiết phiếu C'], '',
      ['Bước 1, 2: không thấy phiếu C', 'Bước 3: "Bạn không có quyền xem phiếu này"']),
] + phan_quyen_chung(K)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', danh_so(hien_thi(K))),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', danh_so(tim_kiem(K))),
    ('III', 'THÊM MỚI', danh_so(S_THEM)),
    ('IV', 'CHỈNH SỬA', danh_so(S_SUA)),
    ('V', 'XÓA', danh_so(S_XOA)),
    ('VI', 'DUYỆT PHIẾU', danh_so(S_DUYET)),
    ('VII', 'LỊCH SỬ THAY ĐỔI', danh_so(lich_su(K))),
    ('VIII', 'XEM CHI TIẾT PHIẾU ĐIỀU CHUYỂN HÀNG', danh_so(S_XEM)),
    ('IX', 'IN PHIẾU', danh_so(S_IN)),
    ('X', 'TÙY CHỈNH CỘT', danh_so(tuy_chinh_cot(K))),
    ('XI', 'XUẤT DANH SÁCH EXCEL', danh_so(xuat_excel(K))),
    ('XII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', danh_so(S_RB)),
    ('XIII', 'PHÂN QUYỀN', danh_so(S_QUYEN)),
]

if __name__ == '__main__':
    build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='phieu')
    print('Số nhóm: %d' % len(SECTIONS))
