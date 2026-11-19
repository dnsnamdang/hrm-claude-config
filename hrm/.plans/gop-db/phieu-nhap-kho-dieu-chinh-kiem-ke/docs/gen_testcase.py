# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu nhập kho điều chỉnh kiểm kê" (STT 287) — KHUÔN CHUẨN 03/11/2026 (loại phiếu), skill testcase-documenter.

Chưa có TC cũ > viết mới theo code develop 18/11/2026 (xem gen_srs.py) + checklist CHECKLIST_TC_SRS.xlsx tab "Testcase".
Nhóm KHÔNG áp dụng (màn không có): Xóa, Khóa / Mở khóa, Không duyệt phiếu, Hủy phiếu, Import từ file Excel.
Nhóm "DUYỆT PHIẾU" = bước Kế toán kho "Tạo phiếu nhập hàng" (lập phiếu nhập hàng điều chỉnh kiểm kê đổi trạng thái phiếu).
Chạy: python gen_testcase.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
from _tc_chuan import build_chuan  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Phiếu nhập kho điều chỉnh kiểm kê'
MODULE = 'Phiếu nhập kho ĐC kiểm kê'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SHEET = 'Trang tính1'
NGAY = '18/11/2026'


def L_(*lines):
    return '\n'.join(lines)


def C(func, prio, pre, steps, data, exp):
    steps = [steps] if isinstance(steps, str) else steps
    exp = [exp] if isinstance(exp, str) else exp
    data = data if isinstance(data, str) else L_(*data)
    return (func, prio, pre,
            L_(*['%d. %s' % (i, s) for i, s in enumerate(steps, 1)]),
            data,
            L_(*['-  ' + e for e in exp]))


MENU = 'phân hệ Kho > menu Nhập kho > "Phiếu nhập kho điều chỉnh kiểm kê"'
MENU_PKK = 'phân hệ Kho > Kiểm kho > Theo vị trí > "Kiểm kê theo hàng hóa"'
MENU_PNH = 'phân hệ Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > "Phiếu nhập hàng điều chỉnh kiểm kê"'
MENU_TK = 'phân hệ Kho > Báo cáo kho > "Thẻ kho"'
Q_XEM = 'Xem phiếu nhập kho điều chỉnh kiểm kê'
Q_TAO = 'Tạo phiếu nhập kho điều chỉnh kiểm kê'
Q_XL = 'Xử lý phiếu kiểm kê hàng hóa'
Q_KT = 'Kế toán kho'
EMPTY = 'Không có dữ liệu phù hợp.'
UNSAVED = 'Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với 2 nút Thoát, Ở lại'
CHUA_DU = 'Bạn chưa nhập đầy đủ thông tin.'
BB = 'Bắt buộc phải nhập'
CONFIRM = ('Hộp "Xác nhận gửi duyệt": "Gửi duyệt sẽ nhập ngay hàng thừa vào kho và không sửa được phiếu nữa. Bạn có chắc '
           'muốn gửi duyệt?" với 2 nút Gửi duyệt, Hủy')
PKK = 'TPE.KKK-01096'
HANG = 'Gạt mưa xướng cứng UP PARTS 18" /450mm (mã CC-CR5-18, vị trí KHOANG5, SL 1)'
P_CHO = 'PNKĐCKK-00054'
P_DANG = 'PNKĐCKK-00053'
P_DA = 'PNKĐCKK-00052'
FILE = 'bien-ban-kiem-ke.pdf (240 KB)'

DU_LIEU = L_(
    'Dữ liệu mẫu (dev 18/11/2026 — ghi mã thật vào cột Ghi chú nếu môi trường khác):',
    '- TK-A: nhân viên công ty TPE có "' + Q_TAO + '" + "' + Q_XL + '", KHÔNG có quyền xem.',
    '- TK-CTY: có "' + Q_XEM + '" mức Công ty (TPE). TK-TCT: mức Tổng công ty. TK-KT: có "' + Q_KT + '". TK-Z: không có quyền nào.',
    '- Phiếu kiểm kê ' + PKK + ' (Chờ xử lý / Đang xử lý): 3 kho CSKH, DATD (không còn hàng thừa), HP - Hải Phòng (1 dòng thừa: ' + HANG + ').',
    '- Phiếu ' + P_CHO + ' Chờ duyệt (kho LN), ' + P_DANG + ' Đang hạch toán (có 2 mốc lịch sử), ' + P_DA + ' Đã hạch toán.',
    '- Phiếu D: phiếu Đang tạo do TK-A lập (tạo ở TC_03.xxx).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Phiếu nhập kho điều chỉnh kiểm kê" nhập vào kho phần hàng THỪA chưa xử lý của 1 phiếu kiểm kê hàng hóa tại 1 kho.',
        'Luồng: chọn Phiếu kiểm kê > Kho > hệ thống nạp dòng hàng thừa (chỉ đọc) > nhập Ghi chú + File đính kèm > Lưu (Đang tạo) '
        'hoặc Gửi duyệt (Chờ duyệt: nhập ngay hàng vào kho, báo Kế toán kho) > Kế toán kho bấm "Tạo phiếu nhập hàng" lập phiếu nhập '
        'hàng điều chỉnh kiểm kê > phiếu Đang hạch toán / Đã hạch toán.',
        'Đường vào: ' + MENU + '; lối thứ 2 vào trang Thêm: nút "Tạo phiếu nhập kho điều chuyển" ở chi tiết phiếu kiểm kê (' + MENU_PKK + ').',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới (Lưu / Lưu và tiếp tục / Gửi duyệt), Sửa, '
        'Xem chi tiết, Tạo phiếu nhập hàng, Lịch sử, In phiếu, In danh sách, Xuất Excel. KHÔNG có Xóa / Hủy / Từ chối / Import.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi xem theo quyền "' + Q_XEM + '":',
        '- Mức Tổng công ty: phiếu mọi công ty; ô lọc Công ty + Phòng ban dùng được.',
        '- Mức Công ty: phiếu của công ty đang làm việc; ô Phòng ban dùng được.',
        '- Không có quyền xem: chỉ phiếu do mình tạo.',
        '- "' + Q_KT + '": thấy thêm mọi phiếu Chờ duyệt (mọi công ty).',
        'Công ty / phòng ban của phiếu = của NGƯỜI LẬP PHIẾU KIỂM KÊ.',
        'Ô "Phiếu kiểm kê" (trang Thêm): phiếu kiểm kê Chờ xử lý / Đang xử lý, còn hàng thừa chưa xử lý, CHƯA có phiếu nhập kho điều '
        'chỉnh; người dùng phải có cả "' + Q_TAO + '" và "' + Q_XL + '".',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Phiếu Đang tạo của NGƯỜI KHÁC: luôn ẩn, kể cả với mức Tổng công ty; mở đường dẫn trực tiếp > trang "Không tìm thấy".',
        '- Phiếu ngoài phạm vi: không hiện; mở đường dẫn trực tiếp > trang "Không tìm thấy".',
        '- Phiếu kiểm kê đã có phiếu nhập kho điều chỉnh / hết hàng thừa / trạng thái khác Chờ xử lý, Đang xử lý: không có trong ô Phiếu kiểm kê.',
        '- Nút Sửa ẩn khi phiếu không còn Đang tạo hoặc không phải của mình; "Tạo phiếu nhập hàng" ẩn khi phiếu khác Chờ duyệt hoặc '
        'người dùng không có "' + Q_KT + '"; "Tạo mới" ẩn khi thiếu "' + Q_TAO + '".',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" (Từ – Đến) lọc theo ngày tạo phiếu, tính cả 2 đầu mút.',
        'Cột "Ngày kiểm kê" hiển thị NGÀY LẬP PHIẾU NHẬP ĐIỀU CHỈNH (không phải ngày của phiếu kiểm kê) — không có ô lọc riêng.',
        'Bộ lọc được ghi nhớ 10 phút khi vào trang chi tiết / thêm / sửa rồi quay lại.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Phiếu = 1 phiếu kiểm kê × 1 kho; số phiếu PNKĐCKK-<5 chữ số>. Gồm Phiếu kiểm kê, Kho, Ghi chú, File đính kèm (ít nhất 1), '
        'bảng Chi tiết (Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Số lượng), Người tạo / Ngày tạo, Người duyệt / Ngày duyệt.',
        'Trạng thái: Đang tạo > Chờ duyệt > Đang hạch toán > Đã hạch toán (Chờ duyệt có thể sang thẳng Đã hạch toán).',
        'Sửa chỉ đổi Ghi chú + File; Phiếu kiểm kê, Kho, dòng hàng giữ nguyên.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Mỗi phiếu kiểm kê chỉ lập được 1 phiếu nhập kho điều chỉnh (2 người lưu cùng lúc: người sau bị chặn).',
        '- Số lượng dòng = số thừa - số đã xử lý, chỉ lấy dòng còn > 0; dòng hàng lấy LẠI từ phiếu kiểm kê khi lưu.',
        '- Gửi duyệt: mỗi dòng sinh 1 lô nhập điều chỉnh, cộng tồn kho vật lý tại kho + vị trí (số lượng × hệ số ĐVT). Lưu (Đang tạo) không cộng tồn.',
    )),
    ('7. Phân quyền cấp', L_(
        '- Menu không gắn quyền: mọi người vào được màn, thấy phiếu mình tạo.',
        '- "' + Q_XEM + '" — mức: Tổng công ty / Công ty.',
        '- "' + Q_TAO + '": nút Tạo mới, trang Thêm, lưu phiếu mới (cần thêm "' + Q_XL + '" để có phiếu kiểm kê chọn được).',
        '- "' + Q_KT + '": thấy mọi phiếu Chờ duyệt, nút "Tạo phiếu nhập hàng", nhận thông báo gửi duyệt cùng công ty.',
        '- Sửa / Gửi duyệt phiếu Đang tạo: chỉ người tạo phiếu.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N": N = tổng phiếu khớp bộ lọc và phạm vi quyền.',
        'Cột Số lượng ở bảng Chi tiết = |chênh lệch| - đã xử lý của dòng kết quả kiểm kê, tối đa 2 chữ số thập phân, định dạng 1,234.5.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '- Màn KHÔNG có Xóa, Khóa, Không duyệt, Hủy, Import. Bước "duyệt" là Kế toán kho lập phiếu nhập hàng điều chỉnh kiểm kê.',
        '- Kho mặc định trên trang Thêm là kho ĐẦU TIÊN của phiếu kiểm kê, có thể không còn hàng thừa > phải đổi kho.',
        '- Xóa file ĐÃ LƯU ở trang Sửa có hiệu lực NGAY (không cần bấm Lưu).',
        '- Cột Người tạo hiển thị "Mã phòng ban - Họ tên"; Người duyệt chỉ họ tên.',
        '- Bản in danh sách tối đa 2,000 dòng; 9 cột cố định, không theo Tùy chỉnh cột.',
        '- Cột KQ thực tế, DNS check để trống cho tester điền.',
    )),
]

# =============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S_HT = [
    C('Mở màn hình từ menu', 'P0', 'TK-A đăng nhập.', ['Vào ' + MENU], '',
      ['Mở màn danh sách, tiêu đề trang "Phiếu nhập kho điều chỉnh kiểm kê"', 'Tiêu đề bảng "Danh sách phiếu nhập kho điều chỉnh kiểm kê"']),
    C('Tài khoản không có quyền nào vẫn vào được màn', 'P1', 'TK-Z không có quyền nào, chưa lập phiếu nào.', ['Đăng nhập TK-Z', 'Vào ' + MENU], '',
      ['Mục menu vẫn hiện, mở được màn', 'Bảng hiện "' + EMPTY + '"', 'KHÔNG có nút Tạo mới']),
    C('Các nút chức năng hiển thị', 'P0', 'TK-A có "' + Q_TAO + '".', ['Vào màn danh sách'], '',
      ['Thanh trên bảng: Tạo mới, Xuất Excel, In danh sách, biểu tượng Cấu hình cột hiển thị',
       'Khu bộ lọc: ô "Tìm theo số phiếu", Tìm kiếm, Làm mới, Cài đặt bộ lọc, Tìm kiếm nâng cao']),
    C('Các cột mặc định hiển thị', 'P0', 'Có ít nhất 1 phiếu trong phạm vi.', ['Vào màn danh sách'], '',
      ['Đủ 11 cột theo thứ tự: STT, Số phiếu, Phiếu kiểm kê, Ngày kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái, Hành động',
       'Không có cột mặc định ẩn']),
    C('Dữ liệu dòng khớp phiếu đã tạo', 'P0', 'TK-TCT; phiếu ' + P_DA + ' Đã hạch toán.', ['Tìm số phiếu ' + P_DA, 'So từng cột với trang Chi tiết'], P_DA,
      ['Số phiếu, Phiếu kiểm kê, Kho ("Mã - Tên"), Người tạo ("Mã phòng ban - Họ tên"), Ngày tạo dd/mm/yyyy hh:mm khớp chi tiết',
       'Người duyệt, Ngày duyệt có giá trị (Kế toán kho đã lập phiếu nhập hàng)', 'Ngày kiểm kê = ngày tạo phiếu (dd/mm/yyyy)']),
    C('Nhãn trạng thái màu', 'P1', 'TK-TCT; có phiếu đủ 3 trạng thái Chờ duyệt / Đang hạch toán / Đã hạch toán và 1 phiếu Đang tạo của chính mình.',
      ['Xem cột Trạng thái'], '',
      ['Đang tạo màu xám, Chờ duyệt màu vàng, Đang hạch toán màu xanh dương, Đã hạch toán màu xanh lá']),
    C('Danh sách chưa có dữ liệu', 'P2', 'TK-Z chưa lập phiếu nào.', ['Vào màn'], '',
      ['Bảng hiện "' + EMPTY + '"', 'Chân bảng không lỗi, không hiện số âm']),
    C('Không có dữ liệu phù hợp bộ lọc', 'P1', 'TK-TCT.', ['Tìm số phiếu "PNKĐCKK-99999"'], 'PNKĐCKK-99999',
      ['Bảng hiện "' + EMPTY + '"']),
    C('Số bản ghi mặc định mỗi trang', 'P1', 'TK-TCT; có 54 phiếu trong phạm vi.', ['Vào màn'], '',
      ['Mỗi trang 10 dòng', 'Chân bảng "Hiển thị 1–10 / 54"']),
    C('Thay đổi số dòng mỗi trang', 'P1', 'Như trên, đang ở trang 3.', ['Đổi "Số dòng/trang" sang 20'], '20',
      ['Bảng hiện 20 dòng', 'Quay về trang 1, chân bảng "Hiển thị 1–20 / 54"']),
    C('Trang trước / sau, đầu / cuối', 'P1', 'Như trên (10 dòng/trang).', ['Bấm trang sau', 'Bấm trang cuối', 'Bấm trang trước', 'Bấm trang đầu'], '',
      ['Chuyển đúng trang 2 > 6 > 5 > 1', 'Ở trang 1 nút trang đầu / trước bị mờ; ở trang cuối nút trang sau / cuối bị mờ']),
    C('STT liên tục giữa các trang', 'P2', 'Như trên.', ['Sang trang 2'], '', ['STT bắt đầu từ 11']),
    C('Tổng số bản ghi', 'P1', 'Như trên.', ['Xem chân bảng'], '', ['N trong "Hiển thị a–b / N" = tổng phiếu trong phạm vi (54)']),
    C('Về trang 1 khi đổi bộ lọc', 'P1', 'Đang ở trang 3.', ['Chọn Trạng thái = Đã hạch toán'], 'Trạng thái: Đã hạch toán',
      ['Danh sách tải lại từ trang 1']),
    C('Thứ tự mặc định', 'P0', 'TK-TCT.', ['Vào màn'], '', ['Sắp theo Ngày tạo giảm dần: phiếu tạo gần nhất (' + P_CHO + ') ở trên cùng']),
    C('Sắp xếp tăng / giảm theo Số phiếu', 'P1', 'TK-TCT.', ['Bấm tiêu đề cột Số phiếu', 'Bấm lần nữa'], '',
      ['Lần 1: số phiếu tăng dần', 'Lần 2: số phiếu giảm dần']),
    C('Sắp xếp theo Ngày tạo / Ngày duyệt', 'P1', 'TK-TCT.', ['Bấm tiêu đề Ngày tạo (2 lần)', 'Bấm tiêu đề Ngày duyệt (2 lần)'], '',
      ['Đổi chiều tăng / giảm đúng theo cột đã bấm']),
    C('Cột không hỗ trợ sắp xếp', 'P2', 'TK-TCT.', ['Rê chuột / bấm tiêu đề các cột Phiếu kiểm kê, Kho, Trạng thái…'], '',
      ['Chỉ Số phiếu, Ngày tạo, Ngày duyệt có biểu tượng sắp xếp; cột khác bấm không đổi thứ tự']),
    C('Giữ sắp xếp khi chuyển trang, về trang 1 khi đổi sắp xếp', 'P2', 'Đang ở trang 2, sắp Số phiếu tăng.',
      ['Sang trang 3', 'Bấm tiêu đề Ngày tạo'], '',
      ['Trang 3 vẫn sắp Số phiếu tăng', 'Đổi sắp xếp thì về trang 1']),
    C('Bấm Số phiếu mở trang Chi tiết', 'P1', 'TK-TCT.', ['Bấm số phiếu ' + P_DA], '', ['Mở trang "Chi tiết phiếu nhập kho điều chỉnh kiểm kê: ' + P_DA + '"']),
    C('Bấm Phiếu kiểm kê mở tab mới', 'P2', 'TK-TCT.', ['Bấm mã phiếu kiểm kê trên dòng ' + P_DA], '', ['Chi tiết phiếu kiểm kê mở ở TAB MỚI, tab danh sách giữ nguyên']),
    C('Nút trên dòng theo trạng thái', 'P0', 'TK-A có phiếu D Đang tạo; TK-A không có "' + Q_KT + '".', ['Đăng nhập TK-A, xem cột Hành động các dòng'], '',
      ['Phiếu D: Sửa, In, Lịch sử', 'Phiếu Chờ duyệt / Đang hạch toán / Đã hạch toán: chỉ In, Lịch sử', 'Không có nút Xóa ở bất kỳ dòng nào']),
    C('Tải trang trong thời gian chấp nhận được', 'P2', 'TK-TCT, 54 phiếu.', ['Vào màn, đổi 200 dòng/trang'], '', ['Bảng hiện trong vài giây, không treo']),
]

# =============================================================== II. TÌM KIẾM & LỌC
S_LOC = [
    C('Tìm theo số phiếu chính xác', 'P0', 'TK-TCT.', ['Nhập số phiếu vào ô tìm nhanh', 'Bấm Tìm kiếm'], P_DANG, ['Chỉ còn dòng ' + P_DANG]),
    C('Tìm theo một phần số phiếu', 'P1', 'TK-TCT.', ['Nhập "0005"', 'Nhấn Enter'], '0005', ['Hiện các phiếu có số chứa "0005" (00050–00054)']),
    C('Không phân biệt hoa / thường', 'P2', 'TK-TCT.', ['Nhập "pnkđckk-00052"', 'Nhấn Enter'], 'pnkđckk-00052', ['Vẫn ra phiếu ' + P_DA]),
    C('Có dấu / không dấu', 'P2', 'TK-TCT.', ['Nhập "PNKDCKK-00052" (D không gạch)', 'Nhấn Enter'], 'PNKDCKK-00052',
      ['Ghi nhận kết quả thực tế (số phiếu có chữ Đ); không lỗi trang']),
    C('Từ khóa không tồn tại', 'P1', 'TK-TCT.', ['Nhập "ABCXYZ"', 'Nhấn Enter'], 'ABCXYZ', ['Bảng hiện "' + EMPTY + '"']),
    C('Ký tự đặc biệt', 'P2', 'TK-TCT.', ['Nhập "%_\'<>"', 'Nhấn Enter'], '%_\'<>', ['Không lỗi trang, không lộ dữ liệu ngoài phạm vi']),
    C('Khoảng trắng đầu / cuối', 'P2', 'TK-TCT.', ['Nhập "  ' + P_DA + '  "', 'Nhấn Enter'], '  ' + P_DA + '  ', ['Hệ thống bỏ khoảng trắng, vẫn ra ' + P_DA]),
    C('Giới hạn ký tự từ khóa', 'P2', 'TK-TCT.', ['Dán chuỗi 300 ký tự', 'Nhấn Enter'], 'Chuỗi 300 ký tự', ['Không lỗi trang; bảng rỗng']),
    C('Xóa từ khóa', 'P2', 'Đang lọc theo từ khóa.', ['Xóa hết chữ trong ô', 'Nhấn Enter'], '', ['Danh sách hiện lại đầy đủ']),
    C('Ô gõ chữ chỉ lọc khi Enter / Tìm kiếm', 'P1', 'TK-TCT.', ['Gõ số phiếu nhưng KHÔNG bấm gì'], P_DA,
      ['Bảng chưa đổi', 'Bấm Tìm kiếm hoặc Enter mới lọc']),
    C('Giá trị mặc định khu Tìm kiếm nâng cao', 'P2', 'TK-TCT, chưa lọc gì.', ['Bấm Tìm kiếm nâng cao'], '',
      ['Hiện ô Mã phiếu, Kho, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày tạo, Công ty, Phòng ban — đều trống',
       'Nút đổi thành "Ẩn tìm kiếm nâng cao"']),
    C('Lọc theo Mã phiếu', 'P0', 'TK-TCT.', ['Nhập Mã phiếu "00053"', 'Nhấn Enter'], 'Mã phiếu: 00053', ['Chỉ còn ' + P_DANG]),
    C('Lọc theo Kho', 'P0', 'TK-TCT.', ['Chọn Kho = HP - Hải Phòng'], 'Kho: HP - Hải Phòng',
      ['Chỉ phiếu có cột Kho = HP - Hải Phòng', 'Lọc ngay khi chọn, không cần bấm Tìm kiếm', 'Ô Kho chỉ liệt kê kho đã có phiếu trong phạm vi; kho đã khóa có biểu tượng ổ khóa']),
    C('Lọc theo Trạng thái', 'P0', 'TK-TCT.', ['Chọn lần lượt từng trạng thái'], 'Đang tạo / Chờ duyệt / Đang hạch toán / Đã hạch toán',
      ['Mỗi lần chỉ hiện phiếu đúng trạng thái đã chọn', 'Đang tạo: chỉ phiếu Đang tạo của chính người dùng']),
    C('Lọc theo Người tạo', 'P0', 'TK-TCT.', ['Chọn Người tạo = "HDQT - DNS Admin"'], 'Người tạo: HDQT - DNS Admin',
      ['Chỉ phiếu do người đó tạo', 'Ô chỉ liệt kê người đã lập phiếu trong phạm vi, dạng "Mã phòng ban - Họ tên"']),
    C('Lọc theo Mã hàng hóa', 'P0', 'TK-TCT; phiếu ' + P_CHO + ' có hàng mã 3M-035653.', ['Nhập Mã hàng hóa "3M-0356"', 'Nhấn Enter'], 'Mã hàng hóa: 3M-0356',
      ['Hiện các phiếu có ít nhất 1 dòng hàng chứa mã đó, gồm ' + P_CHO]),
    C('Lọc theo Tên hàng hóa', 'P1', 'Như trên.', ['Nhập Tên hàng hóa "Đèn soi màu sơn"', 'Nhấn Enter'], 'Tên hàng hóa: Đèn soi màu sơn',
      ['Hiện phiếu có dòng hàng chứa tên đó']),
    C('Lọc theo Ngày tạo', 'P0', 'TK-TCT.', ['Chọn Ngày tạo từ 31/10/2026 đến 02/11/2026'], 'Ngày tạo: 31/10/2026 > 02/11/2026',
      ['Chỉ phiếu tạo trong khoảng, tính cả 2 đầu mút (gồm phiếu tạo 02/11/2026 16:19)']),
    C('Lọc theo Công ty – Phòng ban (Tổng công ty)', 'P1', 'TK-TCT.', ['Chọn Công ty = CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT', 'Chọn 1 phòng ban'], '',
      ['Chỉ phiếu thuộc công ty / phòng ban đã chọn (công ty, phòng ban của người lập phiếu kiểm kê)']),
    C('Ô Công ty khóa với người không có mức Tổng công ty', 'P1', 'TK-CTY.', ['Mở Tìm kiếm nâng cao'], '',
      ['Ô Công ty không chọn được; ô Phòng ban chọn được trong công ty mình']),
    C('Lọc kết hợp nhiều tiêu chí', 'P0', 'TK-TCT.', ['Chọn Kho = LN - Liên Ninh', 'Trạng thái = Đã hạch toán', 'Ngày tạo 26/10–31/10/2026'], '',
      ['Chỉ phiếu thỏa ĐỒNG THỜI cả 3 điều kiện']),
    C('Kết hợp tìm nhanh với bộ lọc', 'P1', 'TK-TCT.', ['Chọn Trạng thái = Đã hạch toán', 'Nhập "00052" ô tìm nhanh, Enter'], '', ['Chỉ ' + P_DA]),
    C('Lọc không có kết quả', 'P2', 'TK-TCT.', ['Trạng thái = Đang tạo + Kho = SG - Kho Sài Gòn'], '', ['Bảng hiện "' + EMPTY + '"']),
    C('Tổng số và phân trang sau lọc', 'P1', 'TK-TCT.', ['Lọc Kho = LN - Liên Ninh'], '', ['N ở chân bảng = số phiếu khớp; phân trang tính lại theo N']),
    C('Sắp xếp sau lọc', 'P2', 'Đang lọc Kho = LN - Liên Ninh.', ['Bấm tiêu đề Số phiếu'], '', ['Chỉ sắp trong tập đã lọc, bộ lọc giữ nguyên']),
    C('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang lọc nhiều ô + từ khóa.', ['Bấm Làm mới'], '',
      ['Mọi ô lọc và ô tìm nhanh trống', 'Danh sách đầy đủ, về trang 1']),
    C('Lưu trạng thái: vào chi tiết rồi quay lại', 'P1', 'Đang lọc Trạng thái = Đã hạch toán.', ['Bấm 1 số phiếu', 'Bấm Quay lại'], '',
      ['Bộ lọc Trạng thái = Đã hạch toán vẫn giữ (trong 10 phút)']),
    C('Lưu trạng thái: F5', 'P2', 'Đang lọc Kho = HP - Hải Phòng.', ['Nhấn F5'], '', ['Ghi nhận kết quả thực tế: bộ lọc còn / mất; không lỗi trang']),
    C('Lưu trạng thái: tab mới', 'P2', 'Đang lọc ở tab 1.', ['Mở màn ở tab mới'], '', ['Ghi nhận kết quả thực tế; không lỗi trang']),
    C('Lưu trạng thái: tài khoản khác cùng trình duyệt', 'P2', 'TK-TCT đang lọc, đăng xuất.', ['Đăng nhập TK-A, vào màn'], '',
      ['TK-A KHÔNG thấy phiếu ngoài phạm vi của mình dù bộ lọc cũ còn']),
]

# =============================================================== III. THÊM MỚI
S_THEM = [
    C('Mở trang Thêm từ nút Tạo mới', 'P0', 'TK-A.', ['Bấm Tạo mới'], '',
      ['Mở trang "Tạo phiếu nhập kho điều chỉnh kiểm kê"', 'Góc phải khối Thông tin chung: "<họ tên TK-A> - <ngày giờ hiện tại>"']),
    C('Mở trang Thêm từ chi tiết phiếu kiểm kê', 'P0', 'TK-A; phiếu kiểm kê ' + PKK + ' còn hàng thừa.',
      ['Vào ' + MENU_PKK, 'Mở chi tiết ' + PKK, 'Bấm "Tạo phiếu nhập kho điều chuyển"'], PKK,
      ['Mở trang Thêm, ô Phiếu kiểm kê chọn sẵn ' + PKK, 'Ô Kho chọn sẵn kho đầu tiên của phiếu kiểm kê']),
    C('Giao diện trang Thêm', 'P1', 'TK-A.', ['Bấm Tạo mới'], '',
      ['Khối Thông tin chung: Phiếu kiểm kê (*), Kho (*), Ghi chú (*)', 'Khối File đính kèm (*) có nút "Thêm tài liệu"',
       'Khối Chi tiết: STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Số lượng',
       'Chân trang: Lưu, Lưu và tiếp tục, Gửi duyệt, Quay lại']),
    C('Giá trị mặc định', 'P1', 'TK-A.', ['Bấm Tạo mới'], '',
      ['Phiếu kiểm kê trống ("Chọn phiếu kiểm kê"); Kho bị khóa, có biểu tượng i: "Chọn phiếu kiểm kê trước — kho lấy theo các kho của phiếu kiểm kê."',
       'Bảng Chi tiết: "Chọn phiếu kiểm kê để nạp hàng thừa cần nhập điều chỉnh"']),
    C('Danh sách ô Phiếu kiểm kê', 'P0', 'TK-A; ' + PKK + ' còn hàng thừa; 1 phiếu kiểm kê đã có phiếu nhập điều chỉnh (TPE.KKK-01095).',
      ['Mở ô Phiếu kiểm kê'], '',
      ['Có ' + PKK, 'KHÔNG có TPE.KKK-01095 (đã có phiếu ' + P_CHO + ')', 'KHÔNG có phiếu kiểm kê Hoàn thành / Đang kiểm / Chờ KT duyệt',
       'Biểu tượng i: "Chỉ liệt kê phiếu kiểm kê Chờ xử lý / Đang xử lý còn hàng thừa chưa nhập điều chỉnh."']),
    C('Chọn phiếu kiểm kê nạp kho và hàng thừa', 'P0', 'TK-A.', ['Chọn Phiếu kiểm kê = ' + PKK], PKK,
      ['Ô Kho mở, liệt kê CSKH, DATD, HP - Hải Phòng; chọn sẵn kho đầu tiên (CSKH - Chăm sóc khách hàng)',
       'Kho CSKH không còn hàng thừa: bảng ghi "Kho này không còn hàng thừa cần nhập điều chỉnh"']),
    C('Đổi kho nạp lại hàng thừa', 'P0', 'Đã chọn ' + PKK + '.', ['Chọn Kho = HP - Hải Phòng'], 'Kho: HP - Hải Phòng',
      ['Bảng Chi tiết có 1 dòng: ' + HANG, 'Các ô trong bảng chỉ đọc']),
    C('Lưu thành công (đủ thông tin hợp lệ)', 'P0', 'TK-A.',
      ['Chọn ' + PKK + ', Kho = HP - Hải Phòng', 'Nhập Ghi chú', 'Thêm tài liệu, chọn file pdf', 'Bấm Lưu'],
      ['Ghi chú: Nhập điều chỉnh hàng thừa kiểm kê T11', 'File: ' + FILE],
      ['Báo "Lưu thành công.", về danh sách', 'Dòng mới trên cùng: số phiếu PNKĐCKK-<5 số>, trạng thái Đang tạo, Người tạo = TK-A, Người duyệt trống',
       'Phiếu kiểm kê ' + PKK + ' chuyển Đang xử lý (lịch sử phiếu kiểm kê ghi "Phiếu nhập kho điều chỉnh kiểm kê <số phiếu>.")']),
    C('Lưu (Đang tạo) không cộng tồn kho', 'P0', 'Vừa lưu phiếu D ở trên.', ['Mở ' + MENU_TK + ', xem hàng CC-CR5-18 kho HP'], '',
      ['KHÔNG có dòng nhập điều chỉnh của phiếu D; tồn không đổi']),
    C('Dữ liệu sau lưu khớp form', 'P0', 'Phiếu D vừa lưu.', ['Mở chi tiết phiếu D'], '',
      ['Phiếu kiểm kê, Kho, Ghi chú, file, dòng hàng khớp lúc nhập', 'Công ty / phòng ban của phiếu = của người lập phiếu kiểm kê']),
    C('Lịch sử Tạo mới', 'P0', 'Phiếu D vừa lưu.', ['Bấm Lịch sử ở dòng phiếu D'], '', ['Có mốc "Tạo mới", người thực hiện TK-A, đúng thời điểm']),
    C('Bỏ trống mọi ô bắt buộc', 'P0', 'TK-A, trang Thêm trống.', ['Bấm Lưu'], '',
      ['Toast "' + CHUA_DU + '"', 'Dưới Phiếu kiểm kê, Ghi chú, khối File đính kèm: "' + BB + '"', 'Không lưu, cuộn tới ô lỗi đầu tiên']),
    C('Thiếu Kho', 'P1', 'Đã chọn phiếu kiểm kê, bấm x xóa Kho (nếu xóa được).', ['Bấm Lưu'], '', ['Dưới ô Kho: "' + BB + '"']),
    C('Kho không còn hàng thừa thì bị chặn', 'P0', 'Chọn ' + PKK + ', để Kho = CSKH; đủ ghi chú + file.', ['Bấm Lưu'], '',
      ['Báo "Kho không còn hàng thừa cần nhập điều chỉnh."', 'Không lưu']),
    C('Ghi chú chỉ khoảng trắng', 'P1', 'Các ô khác hợp lệ.', ['Nhập 3 dấu cách vào Ghi chú', 'Bấm Lưu'], 'Ghi chú: "   "', ['Dưới Ghi chú: "' + BB + '"']),
    C('Ghi chú đúng 255 ký tự', 'P0', 'Các ô khác hợp lệ.', ['Nhập 255 ký tự', 'Bấm Lưu'], 'Chuỗi 255 ký tự', ['Lưu thành công, ghi chú đủ 255 ký tự']),
    C('Ghi chú vượt 255 ký tự', 'P1', 'Trang Thêm.', ['Dán chuỗi 300 ký tự vào Ghi chú'], 'Chuỗi 300 ký tự',
      ['Ô chỉ nhận 255 ký tự đầu (không gõ thêm được)']),
    C('Ghi chú có ký tự đặc biệt / tiếng Việt', 'P2', 'Các ô khác hợp lệ.', ['Nhập ghi chú có dấu và ký tự <>&"', 'Lưu'], 'Ghi chú: Kiểm kê <T11> & "thừa"',
      ['Lưu được; hiển thị đúng nguyên văn ở Chi tiết và bản in']),
    C('Thiếu file đính kèm', 'P0', 'Các ô khác hợp lệ, chưa có file.', ['Bấm Lưu'], '', ['Dưới khối File đính kèm: "' + BB + '"', 'Không lưu']),
    C('File sai định dạng', 'P0', 'Trang Thêm.', ['Thêm tài liệu', 'Chọn file .docx'], 'bao-cao.docx',
      ['Báo "File "bao-cao.docx" không thuộc định dạng cho phép"', 'File không được thêm']),
    C('File vượt 20MB', 'P0', 'Trang Thêm.', ['Thêm tài liệu', 'Chọn file pdf 21MB'], 'file-21mb.pdf',
      ['Báo "File "file-21mb.pdf" vượt quá 20MB"', 'File không được thêm']),
    C('File đúng 20MB, nhiều file', 'P2', 'Trang Thêm.', ['Thêm 2 file: pdf 20MB và ảnh png'], '', ['Cả 2 file tải lên thành công, hiện dung lượng; lưu được']),
    C('Lỗi biến mất sau khi sửa', 'P0', 'Đã bấm Lưu khi trống, đang có lỗi đỏ.', ['Chọn phiếu kiểm kê', 'Nhập ghi chú', 'Thêm file'], '',
      ['Lỗi dưới từng ô mất ngay khi nhập / chọn hợp lệ']),
    C('Lưu và tiếp tục', 'P0', 'TK-A; có 2 phiếu kiểm kê còn lập được.', ['Nhập đủ cho phiếu kiểm kê thứ nhất', 'Bấm Lưu và tiếp tục'], '',
      ['Báo "Lưu thành công."', 'Ở lại trang Thêm, mọi ô trống, file trống',
       'Ô Phiếu kiểm kê nạp lại, KHÔNG còn phiếu kiểm kê vừa lập']),
    C('Lưu và tiếp tục khi thiếu bắt buộc', 'P1', 'Trang Thêm trống.', ['Bấm Lưu và tiếp tục'], '', ['Báo lỗi như Lưu, không lưu']),
    C('Lưu và tiếp tục khi vào từ phiếu kiểm kê', 'P2', 'Vào trang Thêm từ chi tiết ' + PKK + '.', ['Nhập đủ', 'Bấm Lưu và tiếp tục'], '',
      ['Trang Thêm trống, ô Phiếu kiểm kê không còn chọn sẵn ' + PKK]),
    C('Quay lại khi chưa nhập', 'P1', 'Trang Thêm trống.', ['Bấm Quay lại'], '', ['Về danh sách, không hỏi']),
    C('Quay lại khi đã nhập — Ở lại', 'P1', 'Đã chọn phiếu kiểm kê + nhập ghi chú.', ['Bấm Quay lại', 'Bấm Ở lại'], '',
      [UNSAVED, 'Ở lại: đóng hộp, dữ liệu đã nhập còn nguyên']),
    C('Quay lại khi đã nhập — Thoát', 'P0', 'Như trên.', ['Bấm Quay lại', 'Bấm Thoát'], '', ['Về danh sách, KHÔNG có phiếu mới']),
    C('Nhập rồi xóa hết', 'P2', 'Trang Thêm.', ['Nhập ghi chú rồi xóa hết', 'Bấm Quay lại'], '', ['Ghi nhận: có / không hỏi "Thông tin chưa lưu"; không lỗi']),
    C('Bấm Lưu liên tục', 'P0', 'Đủ dữ liệu hợp lệ.', ['Bấm Lưu 3 lần thật nhanh'], '', ['Chỉ 1 phiếu được tạo; nút bị khóa trong lúc chờ']),
    C('Hai người lập cùng phiếu kiểm kê', 'P0', 'TK-A và TK-A2 (cùng quyền) mở trang Thêm, cùng chọn ' + PKK + ' kho HP.',
      ['TK-A bấm Lưu', 'TK-A2 bấm Lưu'], '',
      ['TK-A lưu thành công', 'TK-A2 bị báo "Phiếu kiểm kê không còn lập được phiếu nhập kho điều chỉnh. Vui lòng load lại trang", không tạo phiếu thứ 2']),
    C('Phiếu kiểm kê vừa hết điều kiện khi đang chọn', 'P2', 'TK-A2 vừa lập phiếu cho ' + PKK + ' trong lúc TK-A đang ở trang Thêm.',
      ['TK-A chọn ' + PKK + ' (danh sách cũ)'], '',
      ['Dưới ô báo "Phiếu kiểm kê không còn lập được phiếu nhập kho điều chỉnh hoặc bạn không có quyền.", ô bị bỏ chọn']),
]

# =============================================================== IV. CHỈNH SỬA
S_SUA = [
    C('Mở trang Sửa', 'P0', 'TK-A có phiếu D Đang tạo.', ['Bấm Sửa ở dòng phiếu D'], '',
      ['Mở trang "Sửa phiếu nhập kho điều chỉnh kiểm kê: <số phiếu D>"', 'Chân trang: Lưu, Gửi duyệt, Quay lại (không có Lưu và tiếp tục)']),
    C('Dữ liệu điền sẵn đúng', 'P1', 'Như trên.', ['Xem trang Sửa'], '', ['Phiếu kiểm kê (liên kết), Kho, Ghi chú, file, bảng Chi tiết khớp phiếu D']),
    C('Trường không sửa được', 'P0', 'Như trên.', ['Thử đổi Phiếu kiểm kê, Kho, bảng Chi tiết'], '',
      ['Phiếu kiểm kê là liên kết, Kho chỉ đọc với biểu tượng i: "Kho không đổi được sau khi tạo phiếu."', 'Bảng Chi tiết chỉ đọc, không nạp lại']),
    C('Sửa Ghi chú', 'P0', 'Như trên.', ['Đổi Ghi chú', 'Bấm Lưu'], 'Ghi chú: Bổ sung biên bản',
      ['Báo "Lưu thành công.", về danh sách', 'Chi tiết hiện ghi chú mới; trạng thái vẫn Đang tạo']),
    C('Thêm file và sửa ghi chú cùng lúc', 'P1', 'Như trên.', ['Đổi Ghi chú', 'Thêm 1 file png', 'Bấm Lưu'], '',
      ['Lưu thành công; phiếu có đủ file cũ + mới']),
    C('Lưu không đổi gì', 'P1', 'Như trên.', ['Mở Sửa', 'Bấm Lưu ngay'], '',
      ['Lưu thành công', 'Lịch sử KHÔNG thêm mốc Thay đổi thông tin']),
    C('Lịch sử ghi giá trị cũ > mới', 'P0', 'Vừa sửa Ghi chú + thêm file.', ['Bấm Lịch sử'], '',
      ['Mốc "Thay đổi thông tin": Ghi chú cũ > mới; File đính kèm liệt kê file thêm']),
    C('Xóa ghi chú bị chặn', 'P1', 'Trang Sửa.', ['Xóa hết Ghi chú', 'Bấm Lưu'], '', ['Dưới Ghi chú: "' + BB + '"']),
    C('Xóa file đã lưu có hiệu lực ngay', 'P0', 'Phiếu D có 2 file đã lưu.', ['Bấm thùng rác ở 1 file', 'Bấm Xóa ở hộp "Xác nhận xóa"', 'Bấm Quay lại > Thoát'], '',
      ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa file đính kèm này?"', 'Báo "Xóa file thành công"',
       'Dù KHÔNG bấm Lưu, mở lại chi tiết phiếu chỉ còn 1 file', 'Lịch sử ghi thay đổi File đính kèm']),
    C('Hủy xóa file', 'P2', 'Như trên.', ['Bấm thùng rác', 'Bấm Hủy'], '', ['File còn nguyên']),
    C('Xóa hết file rồi Lưu', 'P0', 'Phiếu D có 1 file.', ['Xóa file đó (xác nhận Xóa)', 'Bấm Lưu'], '',
      ['Bị chặn: báo thiếu file đính kèm ("' + BB + '" / "File đính kèm – Vui lòng đính kèm ít nhất 1 file.")']),
    C('Quay lại khi đã sửa', 'P1', 'Trang Sửa, đã đổi ghi chú.', ['Bấm Quay lại', 'Chọn Ở lại', 'Bấm Quay lại', 'Chọn Thoát'], '',
      [UNSAVED, 'Ở lại giữ dữ liệu; Thoát về danh sách, ghi chú KHÔNG đổi']),
    C('Đổi rồi trả về ban đầu', 'P2', 'Trang Sửa.', ['Đổi ghi chú rồi gõ lại đúng như cũ', 'Bấm Quay lại'], '', ['Ghi nhận có hỏi hay không; dữ liệu không đổi']),
    C('Phiếu đã gửi duyệt không sửa được', 'P0', 'Phiếu ' + P_CHO + ' Chờ duyệt.', ['Dán đường dẫn trang Sửa của phiếu này'], '',
      ['Chuyển sang trang Chi tiết, không mở form sửa']),
    C('Phiếu của người khác không sửa được', 'P0', 'TK-A2 có phiếu Đang tạo.', ['TK-A dán đường dẫn trang Sửa phiếu của TK-A2'], '',
      ['Trang "Không tìm thấy" (phiếu Đang tạo của người khác không xem được)']),
    C('Hai cửa sổ: phiếu vừa gửi duyệt ở cửa sổ khác', 'P1', 'TK-A mở phiếu D ở 2 tab trang Sửa.',
      ['Tab 1 bấm Gửi duyệt > Gửi duyệt', 'Tab 2 sửa ghi chú, bấm Lưu'], '',
      ['Tab 2 báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không lưu']),
]

# =============================================================== V. GỬI DUYỆT
S_GD = [
    C('Hộp xác nhận gửi duyệt', 'P0', 'TK-A, trang Thêm nhập đủ (' + PKK + ', kho HP).', ['Bấm Gửi duyệt'], '', [CONFIRM]),
    C('Thiếu dữ liệu thì không hỏi xác nhận', 'P1', 'Trang Thêm trống.', ['Bấm Gửi duyệt'], '', ['Báo lỗi như khi Lưu, không hiện hộp xác nhận']),
    C('Hủy gửi duyệt', 'P0', 'Đang ở hộp xác nhận.', ['Bấm Hủy'], '', ['Hộp đóng, ở lại form, dữ liệu còn nguyên', 'Không có phiếu mới']),
    C('Gửi duyệt khi lập phiếu', 'P0', 'Như TC đầu nhóm.', ['Bấm Gửi duyệt', 'Bấm Gửi duyệt trong hộp'], '',
      ['Báo "Gửi duyệt thành công.", về danh sách', 'Phiếu mới trạng thái Chờ duyệt', 'Lịch sử có mốc Tạo mới']),
    C('Gửi duyệt phiếu Đang tạo từ trang Sửa', 'P0', 'TK-A có phiếu D Đang tạo.', ['Mở Sửa phiếu D', 'Bấm Gửi duyệt > Gửi duyệt'], '',
      ['Báo "Gửi duyệt thành công."', 'Phiếu D chuyển Chờ duyệt, KHÔNG còn nút Sửa',
       'Lịch sử: "Thay đổi trạng thái" Đang tạo > Chờ duyệt']),
    C('Gửi duyệt cộng tồn kho vật lý ngay', 'P0', 'Trước gửi: tồn hàng CC-CR5-18 tại kho HP vị trí KHOANG5 = X.', ['Gửi duyệt phiếu cho ' + PKK + ' kho HP', 'Mở ' + MENU_TK + ' hàng CC-CR5-18 kho HP'], '',
      ['Có dòng nhập điều chỉnh kiểm kê của phiếu, số lượng 1', 'Tồn tại KHOANG5 = X + 1']),
    C('Số lượng quy đổi theo hệ số ĐVT', 'P2', 'Phiếu có dòng ĐVT Thùng (hệ số 12), SL 2.', ['Gửi duyệt', 'Xem thẻ kho'], '',
      ['Tồn tăng 24 theo ĐVT cơ bản']),
    C('Thông báo tới Kế toán kho cùng công ty', 'P0', 'TK-KT (Kế toán kho, công ty TPE); TK-A thuộc TPE.', ['TK-A gửi duyệt 1 phiếu', 'Đăng nhập TK-KT, mở chuông thông báo'], '',
      ['Có thông báo "[NKĐCKK] Chờ duyệt: <số phiếu>. Người gửi: <họ tên TK-A>. Kho: <tên kho>"',
       'Kế toán kho công ty KHÁC không nhận']),
    C('Bấm thông báo mở đúng phiếu', 'P0', 'Như trên.', ['TK-KT bấm thông báo'], '', ['Mở trang Chi tiết đúng phiếu, có nút Tạo phiếu nhập hàng']),
    C('Không gửi duyệt lại phiếu đã gửi', 'P1', 'Phiếu ' + P_CHO + ' Chờ duyệt.', ['Mở chi tiết phiếu'], '', ['Không có nút Gửi duyệt / Sửa']),
]

# =============================================================== VI. DUYỆT PHIẾU (Tạo phiếu nhập hàng)
S_DUYET = [
    C('Điều kiện hiện nút Tạo phiếu nhập hàng', 'P0', 'TK-KT; phiếu ' + P_CHO + ' Chờ duyệt, ' + P_DANG + ' Đang hạch toán.', ['Xem cột Hành động 2 dòng'], '',
      ['Dòng ' + P_CHO + ' có nút "Tạo phiếu nhập hàng"', 'Dòng ' + P_DANG + ' không có']),
    C('Người không có Kế toán kho không thấy nút', 'P0', 'TK-TCT (không có "' + Q_KT + '").', ['Xem dòng ' + P_CHO + ' và chi tiết'], '',
      ['Không có nút Tạo phiếu nhập hàng ở dòng và chân trang Chi tiết']),
    C('Mở trang Thêm phiếu nhập hàng chọn sẵn phiếu', 'P0', 'TK-KT.', ['Bấm Tạo phiếu nhập hàng ở dòng ' + P_CHO], '',
      ['Mở trang Thêm Phiếu nhập hàng điều chỉnh kiểm kê (phân hệ Tài chính)', 'Ô Phiếu nhập kho chọn sẵn ' + P_CHO + ', dòng hàng và file của phiếu được nạp']),
    C('Lưu phiếu nhập hàng > Đang hạch toán', 'P0', 'TK-KT ở trang Thêm phiếu nhập hàng từ ' + P_CHO + '.', ['Nhập đủ', 'Bấm Lưu'], '',
      [P_CHO + ' chuyển Đang hạch toán', 'Người duyệt = TK-KT, Ngày duyệt = thời điểm lưu',
       'Lịch sử: Thay đổi trạng thái Chờ duyệt > Đang hạch toán, ghi chú "Phiếu nhập hàng điều chỉnh kiểm kê <mã>."']),
    C('Lưu và duyệt phiếu nhập hàng > Đã hạch toán', 'P0', 'Phiếu nhập hàng của ' + P_DANG + ' đang ở Đang tạo.', ['Mở phiếu nhập hàng đó', 'Bấm Lưu và duyệt'], '',
      [P_DANG + ' chuyển Đã hạch toán', 'Lịch sử thêm mốc Đang hạch toán > Đã hạch toán']),
    C('Lưu và duyệt ngay từ Chờ duyệt', 'P1', 'Phiếu Chờ duyệt mới.', ['Tạo phiếu nhập hàng', 'Bấm Lưu và duyệt ngay'], '',
      ['Phiếu nhập kho chuyển thẳng Đã hạch toán']),
    C('Hủy thao tác (Quay lại) không đổi trạng thái', 'P1', 'TK-KT ở trang Thêm phiếu nhập hàng.', ['Bấm Quay lại > Thoát'], '',
      ['Phiếu nhập kho vẫn Chờ duyệt, Người duyệt trống']),
    C('Không tạo phiếu nhập hàng lần 2', 'P1', 'Phiếu đã Đang hạch toán.', ['Xem dòng + chi tiết'], '', ['Không còn nút Tạo phiếu nhập hàng']),
    C('Phiếu kiểm kê chuyển Hoàn thành khi xử lý hết', 'P2', 'Phiếu kiểm kê chỉ có hàng thừa, đã gửi duyệt phiếu nhập kho.', ['Kế toán kho Lưu và duyệt phiếu nhập hàng', 'Mở chi tiết phiếu kiểm kê'], '',
      ['Phiếu kiểm kê chuyển Hoàn thành (nếu không còn chênh lệch nào chưa xử lý)']),
]

# =============================================================== VII. LỊCH SỬ
S_LS = [
    C('Mở cửa sổ Lịch sử từ danh sách', 'P0', 'TK-TCT.', ['Bấm Lịch sử ở dòng ' + P_DANG], '',
      ['Cửa sổ "Lịch sử thay đổi: ' + P_DANG + '"', '2 mốc: "Thay đổi trạng thái" (Chờ duyệt > Đang hạch toán, ghi chú "Phiếu nhập hàng điều chỉnh kiểm kê PNHĐCKK-00053.") ở trên, "Tạo mới" ở dưới']),
    C('Thông tin mỗi mốc', 'P1', 'Như trên.', ['Xem từng mốc'], '',
      ['Thời điểm dd/mm/yyyy hh:mm, tên hành động, "Người thực hiện: <họ tên> — <phòng ban>"', 'Giá trị cũ màu đỏ, mới màu xanh']),
    C('Mở lịch sử từ trang Chi tiết', 'P2', 'TK-TCT.', ['Mở chi tiết ' + P_DANG, 'Bấm "Xem lịch sử" ở khối Lịch sử'], '', ['Khối mở ra, cùng nội dung cửa sổ']),
    C('Lọc lịch sử theo hành động / người / thời gian', 'P2', 'Như trên.', ['Bấm Bộ lọc', 'Chọn hành động "Tạo mới"', 'Chọn khoảng ngày không có mốc'], '',
      ['Chỉ còn mốc Tạo mới', 'Khoảng ngày rỗng: không còn mốc nào, không lỗi']),
    C('Ghi nhận các loại thao tác', 'P0', 'Phiếu D đi qua: Lưu > Sửa ghi chú > Gửi duyệt > KT kho lưu phiếu nhập hàng.', ['Xem lịch sử phiếu D'], '',
      ['Đủ mốc: Tạo mới, Thay đổi thông tin (Ghi chú), Thay đổi trạng thái Đang tạo > Chờ duyệt, Chờ duyệt > Đang hạch toán']),
    C('Đóng cửa sổ', 'P2', 'Cửa sổ đang mở, danh sách ở trang 2 có lọc.', ['Bấm Đóng'], '', ['Cửa sổ đóng, danh sách giữ trang + bộ lọc']),
]

# =============================================================== VIII. XEM CHI TIẾT
S_CT = [
    C('Mở trang Chi tiết', 'P0', 'TK-TCT.', ['Bấm số phiếu ' + P_DA], '',
      ['Tiêu đề "Chi tiết phiếu nhập kho điều chỉnh kiểm kê: ' + P_DA + '"',
       'Khối Thông tin chung: Phiếu kiểm kê (liên kết), Kho, Ghi chú, Người duyệt, Ngày duyệt; góc phải "<Người tạo> - <ngày giờ tạo>"',
       'Khối File đính kèm, Chi tiết, Lịch sử']),
    C('Dữ liệu khớp danh sách', 'P1', 'Như trên.', ['So với dòng ở danh sách'], '', ['Kho, Người duyệt, Ngày duyệt khớp']),
    C('Mọi ô chỉ đọc, không có nút Lưu', 'P1', 'Như trên.', ['Thử sửa các ô'], '', ['Không sửa được; chân trang chỉ In, Quay lại']),
    C('Người duyệt / Ngày duyệt ẩn khi chưa duyệt', 'P2', 'Phiếu ' + P_CHO + ' Chờ duyệt.', ['Mở chi tiết'], '', ['Không có ô Người duyệt, Ngày duyệt']),
    C('Nút chân trang theo trạng thái', 'P0', 'TK-A có phiếu D Đang tạo; TK-KT.', ['TK-A mở chi tiết phiếu D', 'TK-KT mở chi tiết ' + P_CHO], '',
      ['Phiếu D: Sửa, In, Quay lại', P_CHO + ' với TK-KT: Tạo phiếu nhập hàng, In, Quay lại']),
    C('Xem trước / tải file đính kèm', 'P2', 'Như trên.', ['Bấm Xem trước, Tải xuống ở file pdf'], '', ['Mở xem trước / tải đúng file']),
    C('Bấm Phiếu kiểm kê mở tab mới', 'P2', 'Như trên.', ['Bấm mã phiếu kiểm kê'], '', ['Chi tiết phiếu kiểm kê mở ở tab mới']),
    C('Phiếu không tồn tại / ngoài phạm vi', 'P0', 'TK-A (không quyền xem).', ['Dán đường dẫn chi tiết của ' + P_DA + ' (người khác tạo)'], '', ['Trang "Không tìm thấy"']),
    C('Quay lại giữ trang và bộ lọc', 'P2', 'Danh sách đang trang 2, lọc Kho = LN.', ['Mở 1 chi tiết', 'Bấm Quay lại'], '', ['Về danh sách, giữ bộ lọc Kho = LN']),
]

# =============================================================== IX. IN PHIẾU
S_IN = [
    C('In 1 phiếu', 'P0', 'TK-TCT.', ['Bấm In ở dòng ' + P_DA], '',
      ['Cửa sổ "Xem trước phiếu nhập kho điều chỉnh kiểm kê ' + P_DA + '"',
       'Tiêu đề công ty của phiếu; "PHIẾU NHẬP KHO ĐIỀU CHỈNH KIỂM KÊ", Số phiếu, Ngày lập, Phiếu kiểm kê, Kho, Ghi chú',
       'Bảng STT, Tên hàng, Model, Mã hàng, ĐVT, Vị trí, SL nhập; số gọn (8 chứ không 8.00)',
       'Chân: "Ngày <dd> Tháng <mm> Năm <yyyy>", "Người lập" + họ tên người tạo']),
    C('In từ trang Chi tiết, mọi trạng thái', 'P1', 'Phiếu Đang tạo, Chờ duyệt, Đã hạch toán.', ['Mở chi tiết từng phiếu, bấm In'], '', ['Nút In có ở mọi trạng thái, bản in đúng phiếu']),
    C('Bấm In mở hộp in', 'P2', 'Cửa sổ xem trước đang mở.', ['Bấm In'], '', ['Mở hộp in của trình duyệt']),
    C('In danh sách theo bộ lọc', 'P0', 'TK-TCT, lọc Kho = LN - Liên Ninh.', ['Bấm In danh sách'], '',
      ['Cửa sổ "Xem trước danh sách phiếu nhập kho điều chỉnh kiểm kê"', 'Tiêu đề "DANH SÁCH PHIẾU NHẬP KHO ĐIỀU CHỈNH KIỂM KÊ", công ty của người đăng nhập',
       '9 cột: STT, Số phiếu, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái', 'Chỉ phiếu kho LN, đủ mọi trang']),
    C('In danh sách không theo Tùy chỉnh cột', 'P2', 'Đã ẩn cột Người duyệt.', ['Bấm In danh sách'], '', ['Bản in vẫn đủ 9 cột']),
    C('In danh sách vượt 2,000 dòng', 'P2', 'Bộ lọc ra hơn 2,000 phiếu (môi trường có đủ dữ liệu).', ['Bấm In danh sách'], '',
      ['Không in, báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài."']),
]

# =============================================================== X. TÙY CHỈNH CỘT
S_COT = [
    C('Mở cửa sổ Tùy chỉnh cột', 'P1', 'TK-TCT.', ['Bấm biểu tượng Cấu hình cột hiển thị'], '',
      ['Cửa sổ "Tuỳ chỉnh cột" liệt kê 11 cột, "Đang chọn 11/11 cột"', 'STT, Số phiếu, Hành động có ổ khóa, không bỏ tích được']),
    C('Ẩn cột', 'P1', 'Như trên.', ['Bỏ tích Người duyệt, Ngày duyệt', 'Bấm Lưu'], '', ['Bảng không còn 2 cột này', 'Dữ liệu, bộ lọc giữ nguyên']),
    C('Hiện lại cột đã ẩn', 'P2', 'Đã ẩn Người duyệt.', ['Tích lại', 'Lưu'], '', ['Cột hiện lại']),
    C('Chọn tất cả / Bỏ chọn hết', 'P2', 'Cửa sổ đang mở.', ['Bấm Bỏ chọn hết', 'Bấm Chọn tất cả'], '', ['Bỏ chọn hết vẫn giữ 3 cột khóa', 'Chọn tất cả tích đủ 11']),
    C('Kéo đổi thứ tự cột', 'P2', 'Cửa sổ đang mở.', ['Kéo Trạng thái lên sau Số phiếu', 'Lưu'], '', ['Bảng đổi thứ tự cột đúng']),
    C('Đóng không lưu', 'P2', 'Đã bỏ tích vài cột.', ['Bấm Đóng'], '', ['Bảng không đổi']),
    C('Ghi nhớ sau F5 và theo tài khoản', 'P2', 'TK-TCT đã ẩn Người duyệt.', ['Nhấn F5', 'Đăng nhập TK-A trên máy khác'], '',
      ['TK-TCT: vẫn ẩn sau F5', 'TK-A: cấu hình riêng, không bị ảnh hưởng']),
    C('Cài đặt bộ lọc', 'P2', 'TK-TCT.', ['Bấm Cài đặt bộ lọc', 'Bỏ tích Tên hàng hóa, kéo Trạng thái lên đầu', 'Lưu', 'Bấm Khôi phục mặc định'], '',
      ['Cửa sổ liệt kê 8 ô lọc', 'Sau Lưu: khu lọc ẩn Tên hàng hóa, Trạng thái đứng đầu', 'Khôi phục mặc định: về như ban đầu']),
]

# =============================================================== XI. XUẤT EXCEL
S_XUAT = [
    C('Mở cửa sổ chọn trường', 'P1', 'TK-TCT.', ['Bấm Xuất Excel'], '',
      ['Cửa sổ "Chọn trường xuất Excel" 9 trường: Số phiếu, Phiếu kiểm kê, Ngày kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái',
       'Tích sẵn các cột đang hiện; "Đang chọn 9/9 trường"']),
    C('Trường chọn mặc định theo cột đang hiện', 'P2', 'Đã ẩn cột Người duyệt.', ['Bấm Xuất Excel'], '', ['Người duyệt không được tích sẵn']),
    C('Xuất tất cả trường', 'P0', 'TK-TCT, không lọc.', ['Bấm Chọn tất cả', 'Bấm Xuất file'], '',
      ['Tải file danh_sach_phieu_nhap_kho_dieu_chinh_kiem_ke.xlsx, báo "Xuất Excel thành công"',
       'Tiêu đề "DANH SÁCH PHIẾU NHẬP KHO ĐIỀU CHỈNH KIỂM KÊ"; cột STT + 9 cột', 'Số dòng = N ở chân bảng (54), gồm mọi trang']),
    C('Xuất một số trường theo thứ tự đã kéo', 'P1', 'TK-TCT.', ['Bỏ chọn hết', 'Tích Trạng thái, Số phiếu, Kho; kéo Trạng thái lên đầu', 'Xuất file'], '',
      ['File chỉ có STT + 3 cột theo thứ tự Trạng thái, Số phiếu, Kho']),
    C('Không chọn trường nào', 'P2', 'Cửa sổ đang mở.', ['Bỏ chọn hết', 'Bấm Xuất file'], '', ['Không xuất được (nút khóa hoặc báo phải chọn ít nhất 1 trường)']),
    C('Xuất theo bộ lọc và từ khóa', 'P0', 'Lọc Kho = HP - Hải Phòng + tìm "0005".', ['Xuất file'], '', ['File chỉ có phiếu khớp bộ lọc đang áp']),
    C('Xuất khi danh sách rỗng', 'P1', 'Lọc ra 0 dòng.', ['Xuất file'], '', ['Báo "Không có dữ liệu để xuất", không tải file']),
    C('Định dạng dữ liệu trong file', 'P1', 'File vừa xuất.', ['Mở file'], '',
      ['Ngày tạo / Ngày duyệt dd/mm/yyyy hh:mm, Ngày kiểm kê dd/mm/yyyy', 'Tiếng Việt có dấu hiển thị đúng; dữ liệu từng dòng khớp màn hình']),
    C('Phạm vi khi xuất', 'P0', 'TK-A (không quyền xem).', ['Xuất file'], '', ['Chỉ có phiếu TK-A tạo']),
    C('Tiến độ khi xuất', 'P2', 'Danh sách nhiều dòng.', ['Xuất file, quan sát cạnh nút'], '', ['Hiện "Đang chuẩn bị dữ liệu…", "Đã tải x/y dòng…", "Đang dựng file … dòng…"; nút bị khóa tới khi xong']),
]

# =============================================================== XII. RÀNG BUỘC
S_RB = [
    C('Phiếu kiểm kê đã lập phiếu không còn trong ô chọn', 'P0', 'Vừa lập phiếu cho ' + PKK + '.', ['Bấm Tạo mới, mở ô Phiếu kiểm kê'], '', ['Không còn ' + PKK]),
    C('Nút ở chi tiết phiếu kiểm kê ẩn sau khi lập', 'P1', 'Như trên.', ['Mở chi tiết ' + PKK + ' (' + MENU_PKK + ')'], '', ['Không còn nút "Tạo phiếu nhập kho điều chuyển"']),
    C('Phiếu kiểm kê chuyển Đang xử lý', 'P0', PKK + ' đang Chờ xử lý.', ['Lập phiếu nhập kho điều chỉnh', 'Mở chi tiết ' + PKK], '',
      ['Trạng thái Đang xử lý; lịch sử phiếu kiểm kê ghi "Phiếu nhập kho điều chỉnh kiểm kê <số phiếu>."']),
    C('Phiếu Chờ duyệt xuất hiện ở màn Phiếu nhập hàng', 'P0', 'Có phiếu Chờ duyệt mới.', ['Đăng nhập TK-KT', 'Vào màn Phiếu nhập hàng điều chỉnh kiểm kê (phân hệ Tài chính, menu Nhập hàng)', 'Bấm Tạo mới, mở ô Phiếu nhập kho'], '',
      ['Có phiếu vừa gửi duyệt; phiếu Đang tạo / đã hạch toán không có']),
    C('Thẻ kho hiện dòng nhập điều chỉnh', 'P1', 'Đã gửi duyệt phiếu kho HP.', ['Mở ' + MENU_TK], '', ['Có dòng nhập điều chỉnh kiểm kê, liên kết về phiếu']),
    C('Kho / vị trí đã dùng không xóa được', 'P2', 'Kho HP - Hải Phòng đã có phiếu.', ['Vào phân hệ Kho > Danh mục > Kho vật lý, thử xóa kho HP'], '',
      ['Bị chặn vì kho đang được dùng']),
]

# =============================================================== XIII. PHÂN QUYỀN
S_PQ = [
    C('Không có quyền xem: chỉ thấy phiếu mình tạo', 'P0', 'TK-A đã tạo 1 phiếu Chờ duyệt; không có "' + Q_XEM + '".', ['Đăng nhập TK-A, vào màn'], '',
      ['Chỉ phiếu TK-A tạo', 'Ô Công ty, Phòng ban không chọn được']),
    C('Phạm vi mức Công ty', 'P0', 'TK-CTY thuộc TPE.', ['Đăng nhập TK-CTY, vào màn'], '',
      ['Chỉ phiếu của công ty TPE (theo người lập phiếu kiểm kê)', 'Không thấy phiếu công ty khác', 'Ô Phòng ban chọn được, ô Công ty không']),
    C('Phạm vi mức Tổng công ty', 'P0', 'TK-TCT.', ['Đăng nhập TK-TCT, vào màn'], '', ['Thấy phiếu mọi công ty (54)', 'Ô Công ty + Phòng ban chọn được']),
    C('Phiếu Đang tạo của người khác luôn ẩn', 'P0', 'TK-A2 có phiếu Đang tạo.', ['TK-TCT lọc Trạng thái = Đang tạo'], '', ['Không thấy phiếu Đang tạo của TK-A2']),
    C('Kế toán kho thấy mọi phiếu Chờ duyệt', 'P0', 'TK-KT không có quyền xem; có phiếu Chờ duyệt công ty khác.', ['Đăng nhập TK-KT, vào màn'], '',
      ['Thấy mọi phiếu Chờ duyệt (mọi công ty) + phiếu mình tạo', 'Không thấy phiếu Đang hạch toán / Đã hạch toán của người khác']),
    C('Người có 2 quyền: áp mức lớn hơn', 'P1', 'TK-X có mức Công ty và được thêm mức Tổng công ty.', ['Vào màn'], '', ['Thấy phiếu mọi công ty']),
    C('Đổi công ty đang làm việc', 'P1', 'TK-CTY làm việc ở 2 công ty.', ['Đổi công ty đang làm việc', 'Vào lại màn'], '', ['Danh sách tính lại theo công ty mới, không thấy phiếu công ty cũ']),
    C('Thiếu quyền Tạo: ẩn nút Tạo mới', 'P0', 'TK-CTY không có "' + Q_TAO + '".', ['Vào màn'], '', ['Không có nút Tạo mới']),
    C('Thiếu quyền Tạo: mở thẳng trang Thêm', 'P0', 'TK-CTY.', ['Dán đường dẫn trang Thêm'], '', ['Chuyển trang "Không tìm thấy"']),
    C('Có quyền Tạo nhưng thiếu Xử lý phiếu kiểm kê', 'P0', 'TK-B có "' + Q_TAO + '" nhưng không có "' + Q_XL + '".', ['Bấm Tạo mới, mở ô Phiếu kiểm kê'], '',
      ['Ô Phiếu kiểm kê rỗng, không lập được phiếu']),
    C('Sửa / Gửi duyệt chỉ người tạo', 'P0', 'Phiếu D Đang tạo của TK-A.', ['TK-TCT tìm phiếu D'], '', ['Không thấy phiếu D, không có nút Sửa']),
    C('Tạo phiếu nhập hàng chỉ Kế toán kho', 'P0', 'TK-TCT (không có "' + Q_KT + '").', ['Mở chi tiết ' + P_CHO], '', ['Không có nút Tạo phiếu nhập hàng']),
    C('Xem chi tiết / lịch sử / in ngoài phạm vi', 'P0', 'TK-A (không quyền xem).', ['Dán đường dẫn chi tiết ' + P_DA + ' do người khác tạo'], '',
      ['Trang "Không tìm thấy"; không xem được lịch sử, bản in của phiếu đó']),
    C('Xuất Excel / In danh sách theo phạm vi', 'P1', 'TK-CTY.', ['Xuất Excel', 'In danh sách'], '', ['Chỉ phiếu trong phạm vi công ty']),
    C('Thu hồi quyền giữa thao tác', 'P0', 'TK-A đang ở trang Thêm đã nhập đủ.', ['Quản trị thu hồi "' + Q_TAO + '" của TK-A', 'TK-A bấm Lưu'], '',
      ['Bị từ chối "Bạn không có quyền tạo phiếu nhập kho điều chỉnh kiểm kê.", không tạo phiếu']),
    C('Tài khoản không có quyền nào', 'P1', 'TK-Z.', ['Vào màn'], '', ['Vào được, chỉ thấy phiếu mình tạo (0 dòng), không có Tạo mới']),
]

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', S_HT),
    ('TÌM KIẾM & LỌC DANH SÁCH', S_LOC),
    ('THÊM MỚI', S_THEM),
    ('CHỈNH SỬA', S_SUA),
    ('GỬI DUYỆT', S_GD),
    ('DUYỆT PHIẾU (TẠO PHIẾU NHẬP HÀNG - KẾ TOÁN KHO)', S_DUYET),
    ('LỊCH SỬ THAY ĐỔI', S_LS),
    ('XEM CHI TIẾT PHIẾU', S_CT),
    ('IN PHIẾU (IN PHIẾU VÀ IN DANH SÁCH)', S_IN),
    ('TÙY CHỈNH CỘT', S_COT),
    ('XUẤT DANH SÁCH EXCEL', S_XUAT),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S_RB),
    ('PHÂN QUYỀN', S_PQ),
]
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
SECTIONS = [(ROMAN[i], title, [('%03d' % (k + 1),) + tc for k, tc in enumerate(tcs)])
            for i, (title, tcs) in enumerate(GROUPS)]

if __name__ == '__main__':
    build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='phieu')
