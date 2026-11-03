# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu điều chuyển hàng" (STT 204, phân hệ Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Điều chuyển).

Chưa có TC cũ -> viết mới theo code HRM origin/develop (02/11/2026), khuôn gen_testcase.py của màn mẫu phiếu
(finance-declare-debt-beginning/docs/kh). Mọi case gắn nhãn M (thêm mới).
Chạy: python gen_testcase.py
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402,F401  (đặt sys.path tới tc_engine)
from tc_engine import build  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Phiếu điều chuyển hàng'
MODULE = 'Phiếu điều chuyển hàng'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
TAGS = Counter()


def L_(*lines):
    return '\n'.join(lines)


def T(tag, n, func, prio, pre, steps, data, exp):
    assert tag in ('G', 'S', 'M')
    TAGS[tag] += 1

    def j(x):
        return x if isinstance(x, str) else L_(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'phân hệ Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Điều chuyển > "Phiếu điều chuyển hàng"'
KHO = 'PTT - Phan Trọng Tuệ'
KX = 'PTT01 - Phan Trọng Tuệ - Hàng bán'
KN = 'PTT03 - Phan Trọng Tuệ - Hàng khách gửi'
H1 = '2Q-INOX300 - Khay inox chữ nhật kích thước 300X400X50 (ĐVT Cái)'
H2 = 'ENEO-700-V5262 - Dầu ENEOS DEO CK-4 15W40 (ĐVT Xô 18L)'
BC = 'phân hệ Tra cứu - thông báo > Tra cứu tồn kho > "Hàng có thể bán theo công ty"'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '- TK-KT: nhân viên công ty TPE, có quyền "Kế toán kho" + "Xem phiếu điều chuyển hàng theo - công ty".',
    '- TK-KT2: cùng công ty, có "Kế toán kho" (để kiểm phiếu Đang tạo của người khác).',
    '- TK-TCT: có "Xem phiếu điều chuyển hàng theo - tổng công ty", không có "Kế toán kho".',
    '- TK-Z: không có quyền nào của màn.',
    '- Kho vật lý ' + KHO + '; kho xuất ' + KX + '; kho nhập ' + KN + '.',
    '- Hàng H1: ' + H1 + ', đang có tồn ở kho xuất; H2: ' + H2 + '.',
    '- Phiếu A: phiếu Đang tạo do TK-KT lập (1 dòng H1, SL 1). Phiếu B: một phiếu Đã hạch toán có sẵn (vd PDCH-01118).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Phiếu điều chuyển hàng" chuyển hàng giữa 2 KHO KẾ TOÁN trong cùng 1 KHO VẬT LÝ (hàng không di chuyển, chỉ đổi kho hạch toán).',
        'Luồng: chọn Kho vật lý → Kho xuất, Kho nhập → Thêm hàng hóa, nhập SL chuyển, ĐVT → "Lưu nháp" (Đang tạo, chưa đụng tồn) hoặc '
        '"Lưu và duyệt" (hạch toán ngay: trừ tồn kho xuất, cộng tồn kho nhập, tính giá vốn, ghi Nợ 156 / Có 156, khóa phiếu).',
        'Đường vào: ' + MENU + '.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới, Lưu nháp, Lưu và tiếp tục, Lưu và duyệt, '
        'Sửa, Xem chi tiết, Xóa, In phiếu, In danh sách, Xuất Excel, Lịch sử. Không có Import, không có Hủy phiếu.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi xem (xét lần lượt): quản trị hoặc "… theo - tổng công ty" → mọi công ty; "… theo - công ty" → công ty mình; '
        'không có → chỉ phiếu mình lập.',
        'Phiếu Đang tạo chỉ người lập nhìn thấy, với mọi cấp quyền.',
        'Ô Kho vật lý: kho đang hoạt động có kho kế toán của công ty người dùng. Ô Kho xuất / Kho nhập trên form: kho kế toán '
        'đang hoạt động thuộc đúng kho vật lý đã chọn.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Phiếu ngoài phạm vi: không hiện; mở đường dẫn trực tiếp thì báo "Bạn không có quyền xem phiếu này".',
        '- Nút Sửa / Xóa ẨN HẲN với phiếu Đã hạch toán hoặc phiếu không do mình lập.',
        '- Nút Tạo mới ẨN khi không có quyền "Kế toán kho".',
        '- Cửa sổ chọn hàng không nhận hàng tạm (ngoài danh mục) và hàng đã có trong phiếu.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" lọc theo ngày lập phiếu; ô "Ngày hạch toán" lọc theo ngày duyệt (phiếu Đang tạo không có). Tính cả 2 đầu mút.',
        'Bộ lọc được ghi nhớ 10 phút khi rời màn rồi quay lại.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Phiếu (Số phiếu PDCH-xxxxx, Kho vật lý, Kho xuất, Kho nhập, Ghi chú, File đính kèm, Trạng thái, Ngày hạch toán) + nhiều dòng '
        'hàng (Tên, Model, Mã hàng, SL chuyển, ĐVT, Đơn giá vốn, Thành tiền vốn, TK nợ 156, TK có 156).',
        'Trạng thái: Đang tạo → Đã hạch toán (một chiều, không hủy). Phiếu Đang tạo xóa được.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Kho xuất ≠ Kho nhập. Một hàng + ĐVT chỉ 1 dòng.',
        '- SL chuyển > 0 và ≤ SL tồn (tồn quy theo ĐVT). Vượt tồn báo đỏ, KHÔNG tự sửa số.',
        '- Lưu nháp chỉ bắt buộc Kho vật lý; Lưu và duyệt bắt buộc đủ kho + ≥ 1 dòng có SL, ĐVT.',
        '- Hàng đang kiểm kho tại kho vật lý không chuyển được.',
    )),
    ('7. Phân quyền cấp', L_(
        '- "Kế toán kho": nút Tạo mới, lập, lưu, duyệt; sửa / xóa phiếu Đang tạo của mình.',
        '- "Xem phiếu điều chuyển hàng theo - tổng công ty" / "… - công ty": phạm vi xem như mục 2.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N": N = tổng phiếu khớp bộ lọc và phạm vi.',
        'Đơn giá vốn = (giá trị tồn kho xuất trước − sau khi trừ) / SL quy đổi; Thành tiền vốn = SL quy đổi × Đơn giá vốn.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '- Số theo chuẩn quốc tế: 1,400,000 · 0.5.',
        '- Bản in danh sách tối đa 2,000 dòng.',
        '- Kiểm tồn kho: dùng màn ' + BC + ' hoặc cột SL tồn trên form trước / sau khi duyệt.',
        '- Cột kết quả / check để trống cho tester điền.',
    )),
]

ROLE_TCS = [
    T('M', '00', 'Không có quyền nào: chỉ thấy phiếu mình lập, không có Tạo mới', 'P0', 'TK-Z',
      ['1. Đăng nhập TK-Z', '2. Vào ' + MENU, '3. Dán đường dẫn trang Chi tiết của phiếu B'], 'Tài khoản TK-Z',
      ['- Danh sách chỉ có phiếu do TK-Z lập (có thể rỗng: "Không có dữ liệu phù hợp bộ lọc.")', '- Không có nút Tạo mới',
       '- Đường dẫn phiếu B: báo "Bạn không có quyền xem phiếu này", không lộ dữ liệu']),
    T('M', '01', 'Có "Kế toán kho": có nút Tạo mới', 'P0', 'TK-KT', ['1. Đăng nhập TK-KT', '2. Vào ' + MENU], '—',
      ['- Có nút Tạo mới, Xuất Excel, In danh sách, Cấu hình cột hiển thị', '- Phiếu Đang tạo của mình có Sửa, Xóa; phiếu Đã hạch toán chỉ In phiếu, Lịch sử']),
    T('M', '02', 'Phạm vi "… theo - tổng công ty"', 'P0', 'TK-TCT', ['1. Đăng nhập TK-TCT, vào màn', '2. Đọc N, lọc Công ty khác'], '—',
      ['- Thấy phiếu Đã hạch toán của MỌI công ty', '- Không có nút Tạo mới (không có "Kế toán kho")']),
    T('M', '03', 'Phạm vi "… theo - công ty"', 'P0', 'TK-KT', ['1. Đăng nhập TK-KT, vào màn', '2. Lọc Công ty = công ty khác'], '—',
      ['- Chỉ thấy phiếu có công ty = công ty của TK-KT', '- Lọc công ty khác: không có dòng nào']),
    T('M', '04', 'Phiếu Đang tạo của người khác không hiện', 'P0', 'TK-KT2 có phiếu Đang tạo C; TK-TCT',
      ['1. TK-KT đăng nhập, lọc Trạng thái = Đang tạo', '2. TK-TCT làm tương tự', '3. TK-KT dán đường dẫn Chi tiết phiếu C'], '—',
      ['- Bước 1, 2: không thấy phiếu C', '- Bước 3: "Bạn không có quyền xem phiếu này"']),
    T('M', '05', 'Không phải người lập thì không sửa / xóa phiếu Đang tạo', 'P1', 'Quản trị hệ thống mở phiếu C (Đang tạo của TK-KT2)',
      ['1. Mở trang Chi tiết phiếu C bằng đường dẫn'], '—', ['- Không có nút Sửa, Xóa (chỉ người lập được sửa / xóa)']),
]

S1 = [
    T('M', '001', 'Vào màn qua menu', 'P0', 'TK-KT', ['1. Vào ' + MENU], '—',
      ['- Tiêu đề trang và bảng "Phiếu điều chuyển hàng"', '- 10 dòng/trang, phiếu tạo gần nhất đứng đầu', '- Chân bảng "Hiển thị 1–10 / N"']),
    T('M', '002', 'Bộ cột mặc định', 'P0', 'Chưa từng tùy chỉnh cột', ['1. Đọc tiêu đề cột từ trái sang phải'], '—',
      ['- STT, Số phiếu, Ngày hạch toán, Kho vật lý, Kho xuất, Kho nhập, Người tạo, Ngày tạo, Trạng thái, Hành động',
       '- Ghi chú, Người cập nhật, Ngày cập nhật ẩn mặc định']),
    T('M', '003', 'Hiển thị dữ liệu dòng', 'P1', 'Có phiếu A, B', ['1. Xem dòng phiếu A và B'], '—',
      ['- Số phiếu dạng PDCH-xxxxx, là liên kết', '- Người tạo dạng "Họ tên - Mã phòng ban"; ngày dd/mm/yyyy hh:mm',
       '- Phiếu A: Trạng thái "Đang tạo" màu xám, Ngày hạch toán để TRỐNG', '- Phiếu B: "Đã hạch toán" màu xanh lá']),
    T('M', '004', 'Bấm Số phiếu mở chi tiết', 'P1', '—', ['1. Bấm Số phiếu B', '2. Quay lại, chuột phải Số phiếu > mở tab mới'], '—',
      ['- Mở trang "Chi tiết phiếu điều chuyển hàng: <số phiếu>"', '- Mở tab mới được']),
]

S2 = [
    T('M', '001', 'Tìm nhanh theo số phiếu', 'P0', '—', ['1. Nhập "0111" vào ô tìm nhanh', '2. Bấm Tìm kiếm'], '"0111"',
      ['- Chỉ còn phiếu có số chứa "0111"', '- Gõ chưa bấm Tìm kiếm thì danh sách chưa đổi']),
    T('M', '002', 'Lọc Kho vật lý / Kho xuất / Kho nhập', 'P0', '—',
      ['1. Bấm Tìm kiếm nâng cao', '2. Chọn Kho vật lý = ' + KHO, '3. Chọn Kho xuất = ' + KX, '4. Chọn Kho nhập = ' + KN], '—',
      ['- Mỗi lần chọn danh sách lọc ngay', '- Mọi dòng đúng kho đã chọn']),
    T('M', '003', 'Lọc Trạng thái', 'P0', '—', ['1. Chọn Trạng thái = Đang tạo', '2. Chọn Đã hạch toán'], '—',
      ['- Đang tạo: chỉ phiếu Đang tạo do mình lập', '- Đã hạch toán: chỉ phiếu Đã hạch toán']),
    T('M', '004', 'Lọc Người tạo', 'P1', '—', ['1. Chọn Người tạo = TK-KT'], '—', ['- Chỉ phiếu do TK-KT lập']),
    T('M', '005', 'Lọc Mã hàng hóa / Tên hàng hóa', 'P0', '—',
      ['1. Nhập Mã hàng hóa "INOX300", Enter', '2. Xóa, nhập Tên hàng hóa "Khay inox", Enter'], '—',
      ['- Chỉ phiếu có ít nhất 1 dòng hàng khớp (tìm gần đúng)', '- Gõ chưa Enter thì chưa lọc']),
    T('M', '006', 'Lọc Ngày tạo / Ngày hạch toán', 'P1', '—',
      ['1. Ngày tạo từ 01/10/2026 đến 31/10/2026', '2. Bỏ, chọn Ngày hạch toán đến 19/10/2026'], '—',
      ['- Tính cả 2 đầu mút', '- Lọc Ngày hạch toán không ra phiếu Đang tạo']),
    T('M', '007', 'Lọc Công ty – Phòng ban – Bộ phận', 'P2', 'TK-TCT', ['1. Chọn Công ty', '2. Chọn Phòng ban, Bộ phận'], '—',
      ['- Phòng ban, Bộ phận khóa tới khi chọn cấp trên', '- Kết quả theo tổ chức của người lập phiếu, vẫn trong phạm vi xem']),
    T('M', '008', 'Kết hợp nhiều điều kiện + Làm mới', 'P0', '—',
      ['1. Lọc Kho vật lý + Trạng thái + Mã hàng', '2. Bấm Làm mới'], '—',
      ['- Bước 1: áp đồng thời mọi điều kiện', '- Bước 2: xóa hết điều kiện, danh sách đầy đủ, về trang 1']),
    T('M', '009', 'Ghi nhớ bộ lọc', 'P2', '—', ['1. Lọc Trạng thái = Đã hạch toán', '2. Mở chi tiết 1 phiếu rồi Quay lại'], '—',
      ['- Bộ lọc vẫn giữ (trong 10 phút)']),
    T('M', '010', 'Cài đặt bộ lọc', 'P2', '—', ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Tên hàng hóa", kéo "Trạng thái" lên đầu, Lưu', '3. Mở lại, Khôi phục mặc định'], '—',
      ['- Cửa sổ có 10 ô: Công ty – Phòng ban, Kho vật lý, Kho xuất, Kho nhập, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày tạo, Ngày hạch toán',
       '- Lưu xong khu vực lọc đổi theo; khôi phục về như cũ']),
]

S3 = [
    T('M', '001', 'Sắp xếp Số phiếu / Ngày hạch toán / Ngày tạo', 'P1', '—', ['1. Bấm tiêu đề từng cột 2 lần'], '—',
      ['- Đổi tăng / giảm đúng, về trang 1', '- Cột Trạng thái không sắp xếp được']),
    T('M', '002', 'Phân trang', 'P1', 'N > 10', ['1. Sang trang 2', '2. Đổi 20 dòng/trang'], '—',
      ['- STT nối tiếp (11, 12…)', '- Đổi số dòng về trang 1, giữ bộ lọc']),
    T('M', '003', 'Tùy chỉnh cột', 'P2', '—', ['1. Bấm Cấu hình cột hiển thị', '2. Tích Ghi chú, bỏ Người tạo, Lưu', '3. Tải lại trang'], '—',
      ['- "Đang chọn x/13 cột"; STT, Số phiếu, Hành động khóa', '- Bảng đổi theo, tải lại vẫn giữ']),
]

S4 = [
    T('M', '001', 'Mở trang Thêm', 'P0', 'TK-KT', ['1. Bấm Tạo mới'], '—',
      ['- Tiêu đề "Thêm phiếu điều chuyển hàng"', '- Góc phải "<tên TK-KT> - <ngày giờ hiện tại>"',
       '- Kho xuất, Kho nhập khóa; khối Chi tiết có dòng hướng dẫn "Chọn đủ Kho vật lý, Kho xuất và Kho nhập…", chưa có nút Thêm hàng hóa',
       '- Chân trang: Lưu nháp, Lưu và duyệt, Lưu và tiếp tục, Quay lại']),
    T('M', '002', 'Kho kế toán theo kho vật lý', 'P0', '—', ['1. Chọn Kho vật lý = ' + KHO, '2. Mở ô Kho xuất'], '—',
      ['- Chỉ liệt kê kho kế toán thuộc ' + KHO + ' (PTT01, PTT02, PTT03)']),
    T('M', '003', 'Đổi Kho vật lý xóa lựa chọn dưới', 'P0', 'Đã chọn 3 kho và 2 dòng hàng', ['1. Đổi Kho vật lý sang kho khác'], '—',
      ['- Kho xuất, Kho nhập về trống', '- Bảng hàng trống "Chưa có hàng hóa nào trong phiếu"']),
    T('M', '004', 'Thêm hàng hóa', 'P0', 'Đã chọn ' + KHO + ', ' + KX + ', ' + KN,
      ['1. Bấm Thêm hàng hóa', '2. Tích H1, H2, bấm "Thêm 2 hàng hoá"'], '—',
      ['- Cửa sổ "Thêm hàng hoá" chỉ có hàng hóa thật', '- 2 dòng mới: Tên, Model, Mã hàng tự điền; ĐVT = đơn vị cơ bản; SL chuyển 0',
       '- SL tồn = tồn có thể chuyển ở kho xuất; TK nợ, TK có = 156']),
    T('M', '005', 'Thêm hàng đã có trong phiếu', 'P1', 'Phiếu đã có H1', ['1. Thêm hàng hóa, tích lại H1, Thêm'], '—',
      ['- Không thêm dòng mới', '- Chỉ 1 thông báo, không hiện 2 thông báo ngược nhau']),
    T('M', '006', 'Đổi ĐVT / Kho xuất tính lại SL tồn', 'P1', 'H2 có ĐVT hệ số khác 1',
      ['1. Đổi ĐVT dòng H2 sang đơn vị khác', '2. Đổi Kho xuất sang PTT02'], '—',
      ['- ĐVT hiện kèm hệ số dạng "Thùng (x24)"', '- SL tồn tính lại theo ĐVT / kho mới, có thể là số lẻ (vd 0.125), không bị làm tròn về 0']),
    T('M', '007', 'Xóa dòng hàng', 'P1', 'Có 2 dòng', ['1. Bấm thùng rác dòng 1', '2. Bấm Hủy', '3. Bấm lại, bấm Xác nhận'], '—',
      ['- Hộp "Xác nhận xóa hàng hóa": "Bạn có chắc chắn muốn xóa hàng "<tên>" khỏi phiếu?"', '- Hủy: giữ dòng; Xác nhận: bỏ dòng']),
    T('M', '008', 'Lưu nháp thành công', 'P0', 'Đủ 3 kho, H1 SL 1', ['1. Nhập Ghi chú', '2. Bấm Lưu nháp'], '—',
      ['- Báo "Lưu thành công", về danh sách', '- Phiếu mới đứng đầu, Số phiếu PDCH-xxxxx, Trạng thái Đang tạo, Ngày hạch toán trống',
       '- SL tồn của H1 ở kho xuất KHÔNG đổi']),
    T('M', '009', 'Lưu nháp chỉ cần Kho vật lý', 'P1', '—', ['1. Chỉ chọn Kho vật lý', '2. Bấm Lưu nháp'], '—',
      ['- Lưu được, phiếu Đang tạo không có kho xuất / nhập, không có dòng hàng']),
    T('M', '010', 'Lưu và tiếp tục', 'P1', 'Đủ dữ liệu', ['1. Bấm Lưu và tiếp tục'], '—',
      ['- Lưu ở trạng thái Đang tạo', '- Ở lại trang Thêm, form trắng hoàn toàn']),
    T('M', '011', 'Quay lại khi đã nhập', 'P1', 'Đã chọn kho, nhập Ghi chú', ['1. Bấm Quay lại'], '—',
      ['- Hiện hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" (Thoát / Ở lại)',
       '- Thoát: về danh sách, không lưu; Ở lại: giữ nguyên form']),
    T('M', '012', 'Đính kèm tệp', 'P2', '—', ['1. Bấm Thêm tài liệu, chọn 1 tệp pdf', '2. Chọn tệp .docx', '3. Lưu nháp, mở chi tiết'], '—',
      ['- Tệp pdf hiện ngay trong lưới, xem trước / tải xuống được', '- .docx: "Chỉ nhận file pdf, png, jpg, jpeg"',
       '- Chi tiết có tệp, cột Dung lượng có số']),
]

S5 = [
    T('M', '001', 'Bắt buộc khi Lưu và duyệt', 'P0', 'Chỉ chọn Kho vật lý', ['1. Bấm Lưu và duyệt, Xác nhận'], '—',
      ['- Báo đỏ dưới Kho xuất, Kho nhập', '- Báo "Phiếu phải có ít nhất một dòng hàng hóa"', '- Không lưu']),
    T('M', '002', 'Kho xuất trùng Kho nhập', 'P0', '—', ['1. Chọn Kho xuất = Kho nhập = ' + KX, '2. Lưu nháp', '3. Đổi Kho nhập sang ' + KN], '—',
      ['- Dưới Kho nhập: "Kho xuất, kho nhập không được trùng nhau"', '- Đổi kho khác thì chữ đỏ mất']),
    T('M', '003', 'SL chuyển bằng 0 / để trống', 'P0', 'Có dòng H1',
      ['1. SL = 0, Lưu và duyệt', '2. Xóa trống SL, Lưu và duyệt'], '—',
      ['- 0: "Phải lớn hơn 0" dưới ô', '- Trống: "Bắt buộc phải nhập"', '- Ô tiền không gõ được số âm']),
    T('M', '004', 'SL chuyển vượt tồn', 'P0', 'H2 SL tồn = n', ['1. Nhập SL = n + 1, Lưu nháp'], '—',
      ['- Dưới ô: "Số lượng chuyển vượt quá số lượng tồn (còn n)"', '- Số đã nhập GIỮ NGUYÊN, không bị tự sửa về n', '- Không lưu (kể cả Lưu nháp)']),
    T('M', '005', 'SL chuyển số lẻ', 'P1', 'H1 tồn ≥ 1', ['1. Nhập SL 0.5, Lưu nháp'], '—', ['- Lưu được, chi tiết hiện 0.5']),
    T('M', '006', 'Hàng đang kiểm kho', 'P1', 'H1 đang trong đợt kiểm kê theo hàng hóa (chưa xong) tại ' + KHO,
      ['1. Lập phiếu có H1, Lưu nháp'], '—', ['- Báo "Hàng hóa đang được kiểm kho, không thể điều chuyển" tại dòng H1, không lưu']),
    T('M', '007', 'Ghi chú quá 255 ký tự', 'P2', '—', ['1. Nhập Ghi chú 256 ký tự, Lưu nháp'], '—', ['- Báo lỗi độ dài tại ô Ghi chú, không lưu']),
    T('M', '008', 'Không có quyền Kế toán kho gửi lưu', 'P1', 'TK-TCT mở trực tiếp trang Thêm',
      ['1. Dán đường dẫn trang Thêm', '2. Nhập dữ liệu, Lưu nháp'], '—', ['- Báo "Bạn không có quyền lập phiếu điều chuyển hàng", không lưu']),
]

S6 = [
    T('M', '001', 'Hộp xác nhận Lưu và duyệt', 'P0', 'Phiếu đủ dữ liệu', ['1. Bấm Lưu và duyệt', '2. Bấm Hủy'], '—',
      ['- Hộp "Xác nhận lưu và duyệt": "Bạn đồng ý lưu và duyệt?" (Xác nhận / Hủy)', '- Hủy: không lưu, ở lại form']),
    T('M', '002', 'Lưu và duyệt ngay khi lập', 'P0', 'Ghi SL tồn H1 ở kho xuất (a) và kho nhập (b) trước khi duyệt',
      ['1. Lập phiếu H1 SL 2 (ĐVT Cái), Lưu và duyệt, Xác nhận', '2. Mở chi tiết phiếu', '3. Kiểm SL tồn H1 ở 2 kho'], '—',
      ['- Báo "Điều chuyển thành công", về danh sách; phiếu Đã hạch toán, có Ngày hạch toán = lúc duyệt',
       '- Chi tiết có Đơn giá vốn, Thành tiền vốn = 2 × Đơn giá vốn', '- Tồn kho xuất = a − 2; tồn kho nhập = b + 2']),
    T('M', '003', 'Duyệt phiếu Đang tạo từ trang Sửa', 'P0', 'Phiếu A', ['1. Sửa phiếu A, bấm Lưu và duyệt, Xác nhận', '2. Xem Lịch sử'], '—',
      ['- Phiếu A chuyển Đã hạch toán, tồn chuyển như TC_06.002',
       '- Lịch sử có mốc "Thay đổi trạng thái": Trạng thái Đang tạo → Đã hạch toán']),
    T('M', '004', 'Duyệt với ĐVT hệ số khác 1', 'P1', 'H2 có ĐVT hệ số k', ['1. Lập phiếu H2 SL 1 theo ĐVT hệ số k, duyệt'], '—',
      ['- Tồn kho xuất giảm k đơn vị cơ bản, kho nhập tăng k']),
    T('M', '005', 'Bút toán sổ', 'P1', 'Phiếu vừa duyệt ở TC_06.002', ['1. Tra sổ chi tiết tài khoản 156 theo số phiếu'], '—',
      ['- Mỗi dòng hàng 1 cặp Nợ 156 / Có 156 = Thành tiền vốn, chứng từ = Số phiếu, ngày = Ngày hạch toán']),
    T('M', '006', 'Phiếu đã hạch toán bị khóa', 'P0', 'Phiếu B', ['1. Xem dòng phiếu B ở danh sách', '2. Mở chi tiết phiếu B'], '—',
      ['- Không có Sửa, Xóa (ẩn hẳn, không làm mờ)', '- Chân trang chỉ In phiếu, Quay lại', '- Không có thao tác hủy phiếu']),
    T('M', '007', 'Kho nhập chưa từng có hàng', 'P2', 'H1 chưa có tồn ở kho nhập', ['1. Lập và duyệt phiếu chuyển H1 sang kho đó'], '—',
      ['- Duyệt thành công, kho nhập có tồn H1 = SL chuyển']),
]

S7 = [
    T('M', '001', 'Sửa phiếu Đang tạo', 'P0', 'Phiếu A', ['1. Bấm Sửa ở dòng phiếu A', '2. Đổi SL 1 → 3, đổi Kho nhập, Lưu nháp', '3. Xem Lịch sử'], '—',
      ['- Trang "Sửa phiếu điều chuyển hàng" nạp đúng dữ liệu, có SL tồn', '- Không có nút Lưu và tiếp tục',
       '- Báo "Cập nhật thành công", về danh sách', '- Lịch sử "Thay đổi thông tin": Kho nhập cũ → mới; Danh sách hàng hóa: sửa số lượng 1 → 3']),
    T('M', '002', 'Xem chi tiết phiếu Đang tạo', 'P1', 'Phiếu A', ['1. Bấm Số phiếu A'], '—',
      ['- Các ô chỉ đọc; không có cột SL tồn', '- Chân trang: Sửa, In phiếu, Xóa, Quay lại', '- Góc phải "<người lập> - <ngày giờ tạo>"']),
    T('M', '003', 'Lịch sử từ danh sách và từ chi tiết', 'P1', 'Phiếu A đã sửa 1 lần',
      ['1. Bấm Lịch sử ở dòng phiếu A', '2. Mở chi tiết, bấm Xem lịch sử ở khối Lịch sử', '3. Bộ lọc: Loại hoạt động = Tạo mới'], '—',
      ['- 2 nơi cùng nội dung, mới nhất trên cùng: Thay đổi thông tin, Tạo mới', '- Có người thực hiện — phòng ban, thời điểm',
       '- Lọc chỉ còn mốc Tạo mới']),
]

S8 = [
    T('M', '001', 'Xóa phiếu Đang tạo', 'P0', 'Phiếu A', ['1. Bấm Xóa ở dòng phiếu A', '2. Bấm Hủy', '3. Bấm Xóa lại, bấm Xóa'], '—',
      ['- Hộp "Xác nhận xóa": "Bạn có chắc chắn muốn xóa phiếu điều chuyển hàng <số phiếu>?"', '- Hủy: không đổi',
       '- Xóa: "Xóa thành công", phiếu biến mất, tồn kho không đổi']),
    T('M', '002', 'Xóa từ trang Chi tiết', 'P1', 'Phiếu Đang tạo khác', ['1. Mở chi tiết, bấm Xóa, xác nhận'], '—',
      ['- "Xóa thành công", quay về danh sách']),
]

S9 = [
    T('M', '001', 'In phiếu', 'P0', 'Phiếu B', ['1. Bấm In phiếu ở dòng B (hoặc ở chi tiết)', '2. Bấm In'], '—',
      ['- Cửa sổ "Xem trước phiếu <số phiếu>": tiêu đề công ty ghi trên phiếu, "PHIẾU ĐIỀU CHUYỂN HÀNG", Số phiếu, Kho vật lý, Kho xuất, Kho nhập, Ghi chú',
       '- Bảng 10 cột: STT, Tên hàng hóa, Model, Mã hàng hóa, SL chuyển, ĐVT, Đơn giá vốn, Thành tiền vốn, TK nợ 156, TK có 156',
       '- Ô ký "Người lập" có tên người lập', '- Bấm In mở hộp in của trình duyệt']),
    T('M', '002', 'In danh sách', 'P0', 'Lọc Kho vật lý = ' + KHO, ['1. Bấm In danh sách'], '—',
      ['- Cửa sổ "Xem trước danh sách phiếu điều chuyển hàng", tiêu đề "DANH SÁCH PHIẾU ĐIỀU CHUYỂN HÀNG"',
       '- 9 cột: STT, Số phiếu, Ngày hạch toán, Kho vật lý, Kho xuất, Kho nhập, Người lập, Ngày lập, Trạng thái', '- Đúng các dòng khớp bộ lọc']),
    T('M', '003', 'In danh sách quá 2,000 dòng', 'P2', 'Phạm vi > 2,000 phiếu, không lọc', ['1. Bấm In danh sách'], '—',
      ['- Không in; báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được…"']),
    T('M', '004', 'Xuất Excel', 'P0', 'Đang lọc Trạng thái = Đã hạch toán',
      ['1. Bấm Xuất Excel', '2. Tích thêm Ghi chú, kéo Kho nhập lên đầu', '3. Bấm Xuất file'], '—',
      ['- Cửa sổ "Chọn trường xuất file" có 9 trường, tích sẵn cột đang hiện ("Đang chọn 8/9 trường")',
       '- File Danh-sach-phieu-dieu-chuyen-hang-<ngày>.xlsx, tiêu đề "DANH SÁCH PHIẾU ĐIỀU CHUYỂN HÀNG", đủ mọi trang khớp bộ lọc, đúng thứ tự cột',
       '- Báo "Xuất Excel thành công"']),
    T('M', '005', 'Xuất Excel khi không có dữ liệu', 'P2', 'Tìm nhanh "KHONG-TON-TAI"', ['1. Xuất Excel, Xuất file'], '—',
      ['- Báo "Không có dữ liệu để xuất", không tải file']),
]

S10 = [
    T('M', '001', 'Mã phiếu không trùng khi 2 người lưu cùng lúc', 'P1', 'TK-KT, TK-KT2', ['1. Hai người cùng Lưu nháp gần như đồng thời'], '—',
      ['- 2 phiếu có 2 số khác nhau, không lỗi']),
    T('M', '002', 'Tồn bị người khác dùng trước khi duyệt', 'P1', 'H1 tồn ở kho xuất = 3',
      ['1. TK-KT mở form, nhập H1 SL 3 (chưa lưu)', '2. TK-KT2 duyệt phiếu chuyển H1 SL 2 cùng kho xuất', '3. TK-KT bấm Lưu và duyệt'], '—',
      ['- TK-KT bị báo "Số lượng chuyển vượt quá số lượng tồn (còn 1)", không hạch toán']),
    T('M', '003', 'Phiếu vừa bị duyệt ở tab khác', 'P2', 'Phiếu A mở trang Sửa ở 2 tab',
      ['1. Tab 1 Lưu và duyệt', '2. Tab 2 Lưu nháp'], '—', ['- Tab 2 báo "Phiếu đã hạch toán hoặc bạn không có quyền sửa", không đổi dữ liệu']),
]

S11 = [
    T('M', '001', 'Luồng đầu cuối: nháp → sửa → duyệt → kiểm tồn', 'P0', 'Ghi tồn H1 ở kho xuất / nhập trước',
      ['1. Lập phiếu H1 SL 1, Lưu nháp', '2. Kiểm ' + BC + ': tồn không đổi', '3. Sửa SL 2, Lưu và duyệt',
       '4. Kiểm lại tồn', '5. Xem Lịch sử, In phiếu'], '—',
      ['- Bước 2: tồn chưa đổi', '- Bước 4: kho xuất −2, kho nhập +2', '- Lịch sử: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái',
       '- Bản in có Đơn giá vốn, Thành tiền vốn']),
    T('M', '002', 'Chuyển ngược lại thay cho hủy', 'P1', 'Phiếu vừa duyệt ở TC_11.001',
      ['1. Lập phiếu Kho xuất = ' + KN + ', Kho nhập = ' + KX + ', H1 SL 2, duyệt'], '—',
      ['- Tồn 2 kho trở về như trước luồng', '- Đơn giá vốn phiếu ngược bằng giá vốn đã chuyển sang']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP, PHÂN TRANG & CỘT', S3),
    ('IV', 'LẬP PHIẾU — KHO, HÀNG HÓA, LƯU NHÁP', S4),
    ('V', 'RÀNG BUỘC NHẬP LIỆU', S5),
    ('VI', 'LƯU VÀ DUYỆT — TÁC ĐỘNG TỒN KHO & SỔ', S6),
    ('VII', 'SỬA, XEM CHI TIẾT & LỊCH SỬ', S7),
    ('VIII', 'XÓA', S8),
    ('IX', 'IN / XUẤT EXCEL', S9),
    ('X', 'THAO TÁC ĐỒNG THỜI', S10),
    ('XI', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S11),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + L.NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
    print('Tổng %d case (viết mới, không có TC cũ)' % sum(TAGS.values()))
