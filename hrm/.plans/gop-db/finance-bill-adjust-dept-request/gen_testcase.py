# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu yêu cầu điều chỉnh công nợ" — skill testcase-documenter (tc_engine).

Chạy: python gen_testcase.py -> testcase.xlsx
Bản 02/11/2026: sắp lại section theo đúng thứ tự + tên nhóm của checklist "Mẫu tài liệu.xlsx"
(../phieu-theo-form-quoc-gia/checklist_mau_tai_lieu.json), rồi tới phần riêng của màn (In phiếu, Cài đặt bộ lọc,
Gửi duyệt từ chi tiết, luồng tổng thể). Bỏ nhóm Khóa/Mở khóa và Import Excel (màn không có).
Mỗi case có KHÓA (cột đầu của T(...)) — gen_checklist.py tra mã TC theo khóa qua ID[...] để map không lệch khi
thêm / bớt case. Nguồn: code nhánh develop (cả 2 repo) đọc 30/10 và 02/11/2026.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_engine import build, ROMAN  # noqa: E402
from tc_phieu_bosung import (ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases,  # noqa: E402
                             weird_param_case, check_no_dash_pre)

OUT = os.path.join(HERE, 'testcase.xlsx')
NGAY = '02/11/2026'
MENU = ('Vào phân hệ Tài chính > menu "Khởi tạo" > nhóm "Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi" > bấm '
        '"Phiếu yêu cầu điều chỉnh công nợ".')
MENU_SALE = 'Vào phân hệ Bán hàng > menu "Yêu cầu" > nhóm "Công nợ - Thu - Chi" > bấm "YC điều chỉnh công nợ".'
MENU_CD = ('Vào phân hệ Tài chính > menu "Chờ duyệt" > nhóm "Phê duyệt - Công nợ - Thu - Chi" > bấm '
           '"Phiếu yêu cầu điều chỉnh công nợ chờ duyệt".')
MENU_PKT = 'Vào phân hệ Tài chính > menu "Sổ tổng hợp" > bấm "Phiếu kế toán".'
NV = 'Bấm Tìm kiếm nâng cao.'
TAO = [MENU, 'Bấm "Tạo mới".']
DONG = ['Nhập Diễn giải "Chuyển công nợ HĐ-A1 sang HĐ-B1".', 'Bấm nút Thêm dòng (+).',
        'Bên "Điều chỉnh từ": chọn khách hàng KH-A, hợp đồng HĐ-A1, nhập Số tiền 10,000,000.',
        'Bên "Điều chỉnh đến": chọn khách hàng KH-B, hợp đồng HĐ-B1, nhập Số tiền 10,000,000.']
DOT3 = 'Bấm nút ba chấm ở cột Hành động của dòng'

PRE_LIST = 'Tài khoản DNS Admin; danh sách có 12540 phiếu, đủ 2 loại phiếu và 6 trạng thái.'
PRE_FORM = ('Tài khoản A (phòng Kinh doanh, công ty 1, không có quyền xem theo cấp); KH-A có hợp đồng HĐ-A1 còn nợ '
            '50,000,000; KH-B có hợp đồng HĐ-B1; KH-C có hợp đồng HĐ-C1.')
PRE_NHAP = 'Tài khoản A lập phiếu TPE.DNDCCN1026.00402 trạng thái Đang tạo: 1 nhóm KH-A / HĐ-A1 10,000,000 sang KH-B / HĐ-B1 10,000,000.'
PRE_CHO = ('Phiếu TPE.DNDCCN1026.00401 trạng thái Chờ tạo phiếu kế toán do A (công ty 1) lập; tài khoản K có quyền '
           'Kế toán thanh toán, công ty 1.')


class T(object):
    """Một test case có khóa để tra mã TC sau khi đánh số."""

    def __init__(self, key, func, prio, pre, steps, td, exp):
        self.key, self.func, self.prio, self.pre, self.td = key, func, prio, pre, td
        self.steps = steps if isinstance(steps, str) else '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(steps))
        if isinstance(exp, str):
            self.exp = exp
        else:
            self.exp = '\n'.join(x if x.startswith('- ') else '- ' + x for x in exp)

    @classmethod
    def of(cls, key, tup):
        """Bọc tuple sinh từ tc_phieu_bosung (số thứ tự cũ bị bỏ, đánh lại theo vị trí)."""
        return cls(key, tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])


SCREEN = ListScreen(menu=MENU, title='Phiếu yêu cầu điều chỉnh công nợ', total=12540, quick_label='mã phiếu',
                    quick_sample='DNDCCN1026', quick_hit='các phiếu lập tháng 10/2026',
                    filters=[('Loại phiếu', 'Điều chỉnh công nợ khách hàng'), ('Trạng thái', 'Chờ tạo phiếu kế toán')],
                    org_levels=('Công ty', 'Phòng ban', 'Bộ phận'))

# ================================================================== MÔ TẢ
DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn Phiếu yêu cầu điều chỉnh công nợ dùng để đề nghị chuyển công nợ từ khách hàng / nhà cung cấp, hợp đồng này sang '
     'khách hàng / nhà cung cấp, hợp đồng khác.\n'
     'Phiếu lưu nháp được (Đang tạo), gửi duyệt sang Chờ tạo phiếu kế toán; Kế toán thanh toán Từ chối (kèm lý do) hoặc '
     '"duyệt" bằng cách Tạo phiếu kế toán để ghi sổ (màn này không có nút Duyệt riêng).'),
    ('2. Đối tượng được tính / hiển thị',
     '- Hai loại phiếu: Điều chỉnh công nợ khách hàng, Điều chỉnh công nợ nhà cung cấp.\n'
     '- Trạng thái: Đang tạo, Chờ tạo phiếu kế toán, Đã tạo phiếu kế toán, Đã duyệt phiếu kế toán, Hủy (dữ liệu cũ), Từ chối.\n'
     '- Danh sách chung: phiếu theo quyền xem theo cấp; không có quyền thì phiếu mình lập.\n'
     '- Danh sách chờ duyệt: phiếu Chờ tạo phiếu kế toán của người lập cùng công ty, chỉ Kế toán thanh toán thấy.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác: luôn ẩn (kể cả với quyền xem của tổng công ty).\n'
     '- Ở màn chờ duyệt: người không có quyền Kế toán thanh toán thấy danh sách rỗng.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày lập phiếu, lấy trọn hai đầu mút (tính cả 23:59 của ngày cuối).'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Phiếu > nhiều nhóm "Điều chỉnh từ" (khách hàng / NCC, hợp đồng, số tiền) > mỗi nhóm có một hoặc nhiều dòng '
     '"Điều chỉnh đến". Xóa phiếu hoặc xóa nhóm thì các dòng con đi theo.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tổng "Điều chỉnh đến" của mỗi nhóm phải bằng số tiền "Điều chỉnh từ" khi gửi duyệt.\n'
     '- Bên "đến" không được trùng khách hàng / hợp đồng với bên "từ" (kiểm cả khi lưu nháp).\n'
     '- Phiếu không có trường duy nhất: mã phiếu do hệ thống sinh, hai phiếu cùng nội dung vẫn lưu được.'),
    ('7. Phân quyền cấp',
     '- Xem tất cả phiếu yêu cầu điều chỉnh của tổng công ty.\n'
     '- Xem tất cả phiếu yêu cầu điều chỉnh của công ty.\n'
     '- Xem tất cả phiếu yêu cầu điều chỉnh của phòng ban.\n'
     '- Xem tất cả phiếu yêu cầu điều chỉnh của bộ phận.\n'
     '- Kế toán thanh toán: màn chờ duyệt, Từ chối, Tạo phiếu kế toán (cùng công ty người lập).\n'
     '- Lập phiếu, Xuất Excel, In, Lịch sử không gắn quyền riêng; Sửa / Xóa / Gửi duyệt chỉ người lập.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Số tiền còn lại" của nhóm = Số tiền "từ" trừ tổng Số tiền "đến".\n'
     '- Dòng Tổng cộng = tổng tiền bên "từ" và bên "đến".\n'
     '- Ô "Hiển thị a–b / N": N là tổng phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('9. Ghi chú đọc bảng',
     '- Số tiền hiển thị dạng 1,234,567.\n'
     '- Lưu ý: hợp đồng bên "đến" chỉ bắt buộc khi Gửi duyệt; Lưu nháp vẫn để trống được.\n'
     '- Lưu ý: bấm Gửi duyệt khi thiếu nhiều ô, mọi ô lỗi phải đỏ CÙNG MỘT LƯỢT, không báo từng ô một.\n'
     '- Lưu ý: màn chưa có cửa sổ chọn trường xuất Excel; Xuất Excel tải file 12 cột cố định ngay.\n'
     '- Lưu ý: form Tạo / Sửa là trang riêng (không phải cửa sổ nổi) nên các case "đóng cửa sổ" kiểm bằng nút Quay lại '
     'và đóng tab.\n'
     '- Lưu ý: các case "gọi thẳng chức năng bằng công cụ kiểm thử API" dành cho tester kỹ thuật.'),
]

# ================================================================== PHÂN QUYỀN (khối đầu file)
ROLE_TCS = [
    ('00', 'Không có quyền nào chỉ thấy phiếu mình lập', 'P0', 'Tài khoản A không có quyền xem, không là kế toán; A lập 3 phiếu.',
     '1. Đăng nhập bằng A.\n2. ' + MENU, '—', '- Tổng số = 3.\n- Chỉ phiếu A lập.'),
    ('01', 'Quyền xem của tổng công ty', 'P1', 'Tài khoản C có quyền Xem tất cả phiếu yêu cầu điều chỉnh của tổng công ty.',
     '1. Đăng nhập bằng C.\n2. ' + MENU, '—',
     '- Thấy phiếu mọi công ty (trừ nháp của người khác).\n- Khối lọc có Công ty, Phòng ban, Bộ phận.'),
    ('02', 'Quyền xem của công ty', 'P1', 'Tài khoản D công ty 1, có quyền Xem tất cả phiếu yêu cầu điều chỉnh của công ty.',
     '1. Đăng nhập bằng D.\n2. ' + MENU, '—', '- Chỉ phiếu công ty 1.'),
    ('03', 'Quyền xem của phòng ban', 'P1', 'Tài khoản E quản lý phòng Kinh doanh, tự lập 2 phiếu ở phòng khác.',
     '1. Đăng nhập bằng E.\n2. ' + MENU, '—', '- Phiếu phòng Kinh doanh + 2 phiếu E lập.'),
    ('04', 'Quyền xem của bộ phận', 'P1', 'Tài khoản F quản lý bộ phận Bán lẻ.', '1. Đăng nhập bằng F.\n2. ' + MENU, '—',
     '- Phiếu bộ phận Bán lẻ + phiếu F lập.'),
    ('05', 'Nháp của người khác luôn ẩn', 'P0', 'C (tổng công ty); B có 1 phiếu Đang tạo.',
     '1. Đăng nhập C.\n2. ' + MENU + '\n3. ' + NV + '\n4. Lọc Trạng thái Đang tạo.', '—', '- Không thấy nháp của B.'),
    ('06', 'Kế toán thanh toán thấy màn chờ duyệt', 'P0', 'Tài khoản K có quyền Kế toán thanh toán, công ty 1; công ty 1 có 5 phiếu chờ.',
     '1. Đăng nhập K.\n2. ' + MENU_CD, '—',
     '- Tiêu đề "Phiếu yêu cầu điều chỉnh công nợ chờ duyệt".\n- Đúng 5 phiếu, đều Chờ tạo phiếu kế toán.\n- Không có nút Tạo mới.'),
    ('07', 'Không có quyền Kế toán thanh toán ở màn chờ duyệt', 'P0', 'Tài khoản A.',
     '1. Đăng nhập A.\n2. Tìm mục menu chờ duyệt.\n3. Mở màn chờ duyệt bằng đường link do K gửi.', '—',
     '- Không có mục menu chờ duyệt.\n- Mở bằng đường link thì danh sách rỗng.'),
    ('08', 'Kế toán khác công ty không xử lý được', 'P0', 'Tài khoản K2 Kế toán thanh toán công ty 2; phiếu chờ của người lập công ty 1.',
     '1. Đăng nhập K2.\n2. Mở chi tiết phiếu (nếu trong phạm vi xem).', '—', '- Không có nút Tạo phiếu kế toán, Từ chối.'),
    ('09', 'Không phải người lập không sửa / xóa / gửi duyệt', 'P0', 'C; phiếu Từ chối của A.', '1. Mở chi tiết phiếu.', '—',
     '- Không có nút Sửa, Gửi duyệt, Xóa.\n- Ở danh sách dòng phiếu này không có nút Sửa, Xóa.'),
    ('10', 'Mở chi tiết ngoài phạm vi', 'P1', 'A; phiếu người khác ngoài phạm vi.', '1. Mở đường link chi tiết do người khác gửi.', '—',
     '- Báo "Bạn không có quyền xem phiếu này".'),
]

# ================================================================== I. HIỂN THỊ DANH SÁCH VÀ TRUY CẬP
S1 = [
    T.of('list_open', open_menu_case(SCREEN, pre='Tài khoản DNS Admin; trong phạm vi xem có 12540 phiếu.',
                                     extra=['- Lưu ý: số tổng chưa có dấu phẩy ngăn hàng nghìn (lỗi chung đã ghi nhận).'])),
    T('list_open_sale', 'Mở màn từ phân hệ Bán hàng', 'P1', PRE_LIST, [MENU_SALE, 'So tổng số với lối vào Tài chính.'], '—',
      ['Cùng màn, cùng tiêu đề "Phiếu yêu cầu điều chỉnh công nợ".', 'Cùng tổng số phiếu với lối vào từ phân hệ Tài chính.']),
    T('list_title', 'Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát tiêu đề bảng và tên tab trình duyệt.'], '—',
      ['Tiêu đề bảng: "Phiếu yêu cầu điều chỉnh công nợ".', 'Tab trình duyệt cũng ghi "Phiếu yêu cầu điều chỉnh công nợ".',
       'Lối vào chờ duyệt: cả hai ghi "Phiếu yêu cầu điều chỉnh công nợ chờ duyệt".']),
    T('list_buttons', 'Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc và thanh công cụ của bảng.'], '—',
      ['Khối bộ lọc: ô tìm nhanh "Tìm theo mã phiếu...", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
       'Thanh công cụ: nút Tạo mới, Xuất Excel (màu xanh lá), nút biểu tượng Cấu hình cột hiển thị.',
       'Ở lối vào chờ duyệt KHÔNG có nút Tạo mới.']),
    T('list_cols', 'Các cột mặc định hiển thị', 'P0', 'Tài khoản DNS Admin chưa từng lưu Tùy chỉnh cột.', [MENU, 'Quan sát tiêu đề cột.'], '—',
      ['15 cột theo thứ tự: STT, Mã phiếu, Loại phiếu, Số phiếu báo có, KH / NCC, Số tiền, Ngày tạo, Người tạo, Ngày cập nhật, '
       'Người cập nhật, Phòng ban, Ngày nhận, Người duyệt, Trạng thái, Hành động.',
       'STT và Mã phiếu ghim bên trái khi cuộn ngang.']),
    T('list_cols_hidden', 'Các cột mặc định ẩn', 'P2', 'Tài khoản DNS Admin chưa từng lưu Tùy chỉnh cột.',
      [MENU, 'Bấm nút Cấu hình cột hiển thị.', 'Đếm số cột đang được tích.'], '—',
      ['Cả 15 cột đều đang tích: màn KHÔNG có cột nào ẩn mặc định.', 'Bảng hiện đủ 15 cột như cửa sổ Tùy chỉnh cột.']),
    T('list_data', 'Dữ liệu dòng đúng với phiếu đã tạo', 'P0',
      'A vừa gửi duyệt phiếu loại khách hàng: KH-A / HĐ-A1 10,000,000 sang KH-B / HĐ-B1 10,000,000, phòng Kinh doanh.',
      [MENU, 'Tìm dòng phiếu vừa tạo (trên cùng danh sách).'], '—',
      ['Mã phiếu dạng TPE.DNDCCN<tháng năm>.NNNNN, Loại phiếu "Điều chỉnh công nợ khách hàng".',
       'KH / NCC: "mã - tên" của KH-B (khách hàng bên "đến" của dòng đầu); Số tiền 10,000,000 canh phải.',
       'Ngày tạo dạng dd/mm/yyyy hh:mm, Người tạo = A, Phòng ban = Kinh doanh, Ngày nhận = thời điểm gửi duyệt.',
       'Trạng thái "Chờ tạo phiếu kế toán"; Số phiếu báo có trống (phiếu lập tay).']),
    T('list_status', 'Trạng thái bản ghi: nhãn và màu', 'P1', PRE_LIST, [MENU, NV, 'Lần lượt lọc từng trạng thái, quan sát cột Trạng thái.'], '—',
      ['Nhãn đỏ: Đang tạo, Chờ tạo phiếu kế toán, Hủy, Từ chối.', 'Nhãn xanh: Đã tạo phiếu kế toán, Đã duyệt phiếu kế toán.',
       'Ô lọc Trạng thái có đúng 6 lựa chọn trên.']),
    T('list_empty', 'Danh sách chưa có dữ liệu', 'P1', 'Tài khoản G mới tạo, không có quyền xem theo cấp, chưa lập phiếu nào.',
      ['Đăng nhập bằng G.', MENU], '—',
      ['Bảng hiện "Không có dữ liệu phù hợp bộ lọc.".', 'Dưới bảng ghi "Không có phiếu nào.", không có dòng "Hiển thị".',
       'Nút Tạo mới vẫn bấm được; màn không báo lỗi.']),
    T('list_nomatch', 'Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "XYZ999" vào ô tìm nhanh, bấm Tìm kiếm.'],
      'Ô tìm nhanh: XYZ999', ['Bảng hiện "Không có dữ liệu phù hợp bộ lọc.".', 'Dưới bảng ghi "Không có phiếu nào.".']),
    T('list_row_btn', 'Nút trên dòng theo trạng thái và vai trò', 'P0',
      'A lập phiếu 00402 Đang tạo; K là Kế toán thanh toán công ty 1; phiếu 00401 Chờ tạo phiếu kế toán do A lập.',
      ['A mở danh sách, xem dòng 00402, bấm nút ba chấm.', 'K mở danh sách, xem dòng 00401, bấm nút ba chấm.'], '—',
      ['00402 (A): nút Sửa, Xóa và nút ba chấm gồm In phiếu, Xuất Excel, Lịch sử.',
       '00401 (K): nút Tạo phiếu kế toán, Từ chối và nút ba chấm.', 'Nút không dùng được thì ẨN HẲN, không hiện mờ.']),
    T('list_code_link', 'Bấm Mã phiếu mở chi tiết', 'P0', PRE_LIST, [MENU, 'Bấm mã TPE.DNDCCN1026.00401.'], '—',
      ['Mở màn "Chi tiết phiếu yêu cầu điều chỉnh công nợ: TPE.DNDCCN1026.00401".', 'Chuột phải vào mã có mục mở ở tab mới.']),
    T('list_report_link', 'Bấm Số phiếu báo có', 'P2', 'Phiếu 00371 được tạo từ phiếu báo có TPE.BC1026.00055.',
      [MENU, 'Bấm số phiếu báo có ở dòng 00371.'], '—',
      ['Mở chi tiết phiếu báo có TPE.BC1026.00055 ở tab mới.', 'Tab danh sách giữ nguyên trang và bộ lọc.']),
    T('pg_size', 'Thay đổi số dòng/trang', 'P1', PRE_LIST, [MENU, 'Bấm sang trang 3.', 'Đổi Số dòng/trang = 20.'], 'Số dòng/trang: 20',
      ['Bảng hiện 20 dòng.', 'Quay về trang 1, dòng dưới bảng "Hiển thị 1–20 / 12540".']),
    T('pg_next', 'Trang trước / tiếp theo', 'P1', PRE_LIST, [MENU, 'Bấm nút trang tiếp theo (›).', 'Bấm nút trang trước (‹).'], '—',
      ['Bước 1: sang trang 2, "Hiển thị 11–20 / 12540".', 'Bước 2: về trang 1, "Hiển thị 1–10 / 12540".']),
    T('pg_first_last', 'Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm nút về trang cuối (»).', 'Bấm nút về trang đầu («).'], '—',
      ['Bước 1: trang 1254, "Hiển thị 12531–12540 / 12540", chỉ 10 dòng.', 'Bước 2: về trang 1.']),
    T('pg_btn_state', 'Trạng thái nút tại trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Quan sát nút phân trang ở trang 1.', 'Về trang cuối, quan sát lại.'], '—',
      ['Trang 1: nút « và ‹ mờ, không bấm được.', 'Trang cuối: nút › và » mờ, không bấm được.']),
    T('pg_stt', 'STT liên tục giữa các trang', 'P1', PRE_LIST, [MENU, 'Quan sát STT trang 1.', 'Sang trang 2.'], '—',
      ['Trang 1: STT 1 đến 10.', 'Trang 2: STT bắt đầu từ 11, không đánh lại từ 1.']),
    T('pg_total', 'Tổng số bản ghi', 'P1', 'Tài khoản A không có quyền xem theo cấp, đã lập 23 phiếu.', ['Đăng nhập A.', MENU], '—',
      ['Dòng dưới bảng "Hiển thị 1–10 / 23".', 'Trang 3 hiện đúng 3 dòng, "Hiển thị 21–23 / 23".']),
    T('pg_reset_filter', 'Về trang 1 khi thay đổi bộ lọc', 'P1', PRE_LIST, [MENU, 'Sang trang 5.', NV, 'Chọn Loại phiếu = Điều chỉnh công nợ nhà cung cấp.'],
      'Loại phiếu: Điều chỉnh công nợ nhà cung cấp', ['Danh sách tự nạp lại về trang 1.', 'STT bắt đầu từ 1.']),
    T('sort_asc', 'Sắp xếp tăng dần', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số tiền một lần.'], '—',
      ['Biểu tượng mũi tên lên ở cột Số tiền.', 'Phiếu số tiền nhỏ nhất lên đầu, tăng dần xuống dưới.']),
    T('sort_desc', 'Sắp xếp giảm dần', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số tiền hai lần.'], '—',
      ['Biểu tượng mũi tên xuống.', 'Phiếu số tiền lớn nhất lên đầu.', 'Hai phiếu cùng số tiền: phiếu tạo sau đứng trên.']),
    T('sort_date', 'Sắp xếp theo Ngày tạo / Ngày cập nhật / Ngày nhận', 'P1', PRE_LIST,
      [MENU, 'Bấm tiêu đề Ngày tạo.', 'Bấm tiêu đề Ngày cập nhật.', 'Bấm tiêu đề Ngày nhận.'], '—',
      ['Mỗi lần bấm danh sách sắp đúng theo cột đó, đổi chiều khi bấm lại.', 'Phiếu chưa gửi duyệt (Ngày nhận trống) dồn về một đầu.']),
    T('sort_none', 'Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
      [MENU, 'Rê chuột và bấm tiêu đề các cột Loại phiếu, KH / NCC, Người tạo, Phòng ban, Trạng thái.'], '—',
      ['Các cột này không có biểu tượng sắp xếp, bấm không đổi thứ tự.',
       'Chỉ 5 cột sắp xếp được: Mã phiếu, Số tiền, Ngày tạo, Ngày cập nhật, Ngày nhận.']),
    T('sort_keep_page', 'Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Sắp xếp Số tiền giảm dần.', 'Sang trang 2.'], '—',
      ['Trang 2 tiếp nối thứ tự giảm dần của trang 1 (số tiền dòng đầu trang 2 không lớn hơn dòng cuối trang 1).',
       'Biểu tượng sắp xếp vẫn ở cột Số tiền.']),
    T('sort_reset_page', 'Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 4.', 'Bấm tiêu đề cột Ngày tạo.'], '—',
      ['Danh sách về trang 1 theo thứ tự mới.']),
    T.of('list_weird_param', weird_param_case('000', SCREEN, 'tiêu đề "Phiếu yêu cầu điều chỉnh công nợ", có nút Tạo mới')),
    T('list_mode_switch', 'Đang lọc rồi mở lối vào chờ duyệt', 'P1',
      'Tài khoản K có quyền Kế toán thanh toán; đang ở danh sách chung, lọc Trạng thái = Từ chối.',
      [MENU_CD, 'Quan sát tiêu đề và danh sách.'], '—',
      ['Tiêu đề "Phiếu yêu cầu điều chỉnh công nợ chờ duyệt", không có nút Tạo mới.',
       'Danh sách chỉ còn phiếu Chờ tạo phiếu kế toán của người lập cùng công ty, từ trang 1 (bộ lọc Từ chối không mang sang).']),
    T('list_mode_reset', 'Làm mới ở màn chờ duyệt giữ nguyên chế độ', 'P2', 'Tài khoản K; đang ở màn chờ duyệt, lọc Loại phiếu.',
      [MENU_CD, 'Bấm Làm mới.'], '—', ['Xóa điều kiện lọc nhưng vẫn ở màn chờ duyệt (tiêu đề không đổi).']),
    T('list_session', 'Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2',
      'Tài khoản A đang mở danh sách; phiên đăng nhập vừa hết hạn (hoặc đăng xuất ở tab khác).',
      ['Bấm sang trang 2.'], '—',
      ['Báo "Phiên đăng nhập đã hết hạn".', 'Chuyển về màn đăng nhập; đăng nhập lại mở được danh sách.']),
]

# ================================================================== II. TÌM KIẾM VÀ LỌC
QS = 'Ô tìm nhanh'
S2 = [
    T('qs_exact', 'Tìm theo mã phiếu chính xác', 'P0', PRE_LIST,
      [MENU, 'Nhập "TPE.DNDCCN1026.00401" vào ô tìm nhanh.', 'Nhấn Enter.'], QS + ': TPE.DNDCCN1026.00401',
      ['Chỉ còn phiếu TPE.DNDCCN1026.00401.', 'Dòng dưới bảng "Hiển thị 1–1 / 1".']),
    T('qs_partial', 'Tìm theo một phần mã phiếu', 'P0', PRE_LIST + ' Tháng 10/2026 có 160 phiếu.',
      [MENU, 'Nhập "DNDCCN1026" vào ô tìm nhanh, bấm Tìm kiếm.'], QS + ': DNDCCN1026',
      ['Còn đúng các phiếu có mã chứa "DNDCCN1026" (160 phiếu).', 'Khớp một phần ở bất kỳ vị trí nào trong mã.']),
    T('qs_case', 'Không phân biệt hoa / thường', 'P1', PRE_LIST, [MENU, 'Nhập "dndccn1026.00401", bấm Tìm kiếm.'], QS + ': dndccn1026.00401',
      ['Ra phiếu TPE.DNDCCN1026.00401 như khi gõ chữ hoa.']),
    T('qs_accent', 'Có dấu / không dấu', 'P2', PRE_LIST + ' Khách hàng "Công ty Tân Phát" nhận công nợ ở 2 phiếu.',
      [MENU, NV, 'Gõ "tan phat" vào ô Khách hàng / Nhà cung cấp.', 'Gõ lại "Tân Phát".'], 'Khách hàng / Nhà cung cấp: tan phat',
      ['Cả hai cách gõ đều gợi ý "Công ty Tân Phát" (so khớp không phân biệt dấu).',
       'Lưu ý: chữ "đ" và "d" được coi là khác nhau (gõ "dong" không ra "Đông").',
       'Ô tìm nhanh chỉ tìm mã phiếu (không dấu) nên không áp dụng case dấu.']),
    T('qs_notfound', 'Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "DNDCCN9999", bấm Tìm kiếm.'], QS + ': DNDCCN9999',
      ['Bảng hiện "Không có dữ liệu phù hợp bộ lọc.".', 'Không báo lỗi, màn không treo.']),
    T('qs_special', 'Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "\'" rồi bấm Tìm kiếm.', 'Nhập "%" rồi bấm Tìm kiếm.'],
      "Ô tìm nhanh: ' ; %",
      ['Bước 1: không lỗi, bảng báo "Không có dữ liệu phù hợp bộ lọc.".',
       'Bước 2: danh sách hiện TOÀN BỘ phiếu (dấu % được hiểu là "mọi ký tự").',
       'Lưu ý: bước 2 là hành vi hiện tại của hệ thống, không phải lỗi treo màn.']),
    T('qs_trim', 'Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "   00401   " (có khoảng trắng hai đầu), bấm Tìm kiếm.'],
      QS + ': "   00401   "', ['Hệ thống bỏ khoảng trắng hai đầu, vẫn ra phiếu có mã chứa "00401".']),
    T('qs_clear', 'Xóa từ khóa', 'P1', 'Đang tìm "00401", danh sách còn 1 phiếu.',
      [MENU, 'Bấm nút × trong ô tìm nhanh (hoặc xóa hết chữ).', 'Bấm Tìm kiếm.'], '—',
      ['Ô tìm nhanh trống.', 'Danh sách hiện lại đủ 12540 phiếu từ trang 1.']),
    T('qs_enter', 'Enter / nút Tìm kiếm mới áp ô tìm nhanh', 'P1', PRE_LIST,
      [MENU, 'Gõ "00401" vào ô tìm nhanh, KHÔNG bấm gì.', 'Bấm nút Tìm kiếm.', 'Xóa chữ, gõ "00402", nhấn Enter.'], QS + ': 00401 ; 00402',
      ['Bước 1: danh sách chưa đổi.', 'Bước 2: lọc theo "00401".', 'Bước 3: lọc theo "00402".']),
    T('flt_default', 'Giá trị mặc định của bộ lọc', 'P1', 'Tài khoản DNS Admin chưa lọc gì trong 10 phút gần nhất.',
      [MENU, NV, 'Quan sát các ô lọc.'], '—',
      ['Khối Tìm kiếm nâng cao mặc định thu gọn.', 'Mọi ô lọc trống: Loại phiếu, Trạng thái = tất cả; Ngày tạo, Số tiền trống.',
       'Danh sách hiện mọi phiếu trong phạm vi quyền.']),
    T('flt_type', 'Lọc Loại phiếu', 'P0', 'Có 3 phiếu loại nhà cung cấp Chờ tạo phiếu kế toán.',
      [MENU, NV, 'Chọn Loại phiếu = Điều chỉnh công nợ nhà cung cấp.', 'Chọn Trạng thái = Chờ tạo phiếu kế toán.'],
      'Loại phiếu: Điều chỉnh công nợ nhà cung cấp\nTrạng thái: Chờ tạo phiếu kế toán',
      ['Mỗi lần đổi ô, danh sách tự nạp lại (không cần bấm Tìm kiếm).', 'Còn đúng 3 phiếu.']),
    T('flt_status', 'Lọc Trạng thái', 'P0', PRE_LIST, [MENU, NV, 'Chọn Trạng thái = Từ chối.'], 'Trạng thái: Từ chối',
      ['Chỉ còn phiếu nhãn "Từ chối".']),
    T('flt_party', 'Lọc Khách hàng / Nhà cung cấp', 'P1', 'Khách hàng KH-B nhận công nợ ở 2 phiếu, không nằm ở bên "từ" phiếu nào.',
      [MENU, NV, 'Gõ 1 ký tự "K" vào ô Khách hàng / Nhà cung cấp.', 'Gõ tiếp thành "KH-B", chọn KH-B.'], 'Khách hàng / Nhà cung cấp: KH-B',
      ['Bước 2: chưa có gợi ý (cần tối thiểu 2 ký tự).', 'Bước 3: ra 2 phiếu (lọc cả bên "từ" lẫn bên "đến").']),
    T('flt_contract', 'Lọc Hợp đồng điều chỉnh từ / đến', 'P1', 'Hợp đồng KD2_26_1434 là bên "đến" của 1 phiếu.',
      [MENU, NV, 'Nhập Hợp đồng điều chỉnh đến = "KD2_26_1434".', 'Xóa ô đó, nhập Hợp đồng điều chỉnh từ = "KD2_26_1434".'],
      'Hợp đồng điều chỉnh đến: KD2_26_1434',
      ['Bước 2: chỉ phiếu có hợp đồng bên "đến" chứa chuỗi.', 'Bước 3: không ra phiếu đó (hợp đồng không nằm bên "từ").']),
    T('flt_money', 'Lọc Số tiền', 'P1', PRE_LIST, [MENU, NV, 'Nhập Số tiền từ 1,000,000 đến 5,000,000, nhấn Enter.'],
      'Số tiền: 1,000,000 - 5,000,000', ['Chỉ phiếu có tổng tiền trong khoảng, tính cả 2 đầu mút.']),
    T('flt_date', 'Lọc Ngày tạo', 'P1', 'Có phiếu tạo lúc 23:59 ngày 21/10/2026.', [MENU, NV, 'Chọn Ngày tạo 21/10/2026 đến 21/10/2026.'],
      'Ngày tạo: 21/10/2026 - 21/10/2026', ['Chỉ phiếu tạo ngày 21/10/2026, kể cả phiếu lúc 23:59.']),
    T('flt_people', 'Lọc Người tạo / Người duyệt', 'P2', 'Kế toán Dương Đức Thái đã từ chối 4 phiếu.',
      [MENU, NV, 'Chọn Người duyệt = Dương Đức Thái.'], 'Người duyệt: Dương Đức Thái', ['Ra đúng 4 phiếu người này đã xử lý.']),
    T('flt_report', 'Lọc Số phiếu báo có', 'P2', 'Phiếu 00371 tạo từ phiếu báo có TPE.BC1026.00055.',
      [MENU, NV, 'Nhập Số phiếu báo có = "BC1026.00055".'], 'Số phiếu báo có: BC1026.00055', ['Ra phiếu 00371.']),
] + [T.of(k, c) for k, c in zip(['org_none', 'org_pick', 'org_change'], org_cases(SCREEN, 1))] + [
    T.of(k, c) for k, c in zip(['combo_1', 'combo_2', 'combo_3', 'qs_len'], combo_cases(SCREEN, 1))] + [
    T('flt_nores', 'Không có kết quả khi lọc', 'P1', PRE_LIST,
      [MENU, NV, 'Chọn Trạng thái = Hủy.', 'Chọn Ngày tạo 01/11/2026 đến 01/11/2026.'], 'Trạng thái: Hủy\nNgày tạo: 01/11/2026',
      ['Bảng hiện "Không có dữ liệu phù hợp bộ lọc.".', 'Dưới bảng "Không có phiếu nào.".']),
    T('flt_total', 'Tổng số sau lọc', 'P1', 'Có 37 phiếu Từ chối.', [MENU, NV, 'Chọn Trạng thái = Từ chối.'], 'Trạng thái: Từ chối',
      ['Dòng dưới bảng "Hiển thị 1–10 / 37".']),
    T('flt_paging', 'Phân trang sau lọc', 'P1', 'Có 37 phiếu Từ chối.', [MENU, NV, 'Chọn Trạng thái = Từ chối.', 'Sang trang 4.'],
      'Trạng thái: Từ chối', ['Trang 4 hiện 7 dòng, "Hiển thị 31–37 / 37".', 'Có 4 trang; mọi dòng đều là Từ chối.']),
    T('flt_sort', 'Sắp xếp sau lọc', 'P2', 'Có 37 phiếu Từ chối.', [MENU, NV, 'Chọn Trạng thái = Từ chối.', 'Bấm tiêu đề Số tiền.'],
      'Trạng thái: Từ chối', ['Vẫn chỉ 37 phiếu Từ chối, sắp tăng dần theo Số tiền, về trang 1.']),
    T('flt_reset', 'Làm mới / Xóa lọc', 'P1', 'Đang lọc Loại phiếu, Trạng thái, Số tiền và ô tìm nhanh "1026"; đang sắp theo Số tiền.',
      [MENU, 'Bấm Làm mới.'], '—',
      ['Mọi ô lọc và ô tìm nhanh trống.', 'Danh sách nạp lại từ trang 1, thứ tự về mặc định (mới tạo lên trên).']),
] + [T.of(k, c) for k, c in zip(['mem_back', 'mem_expire', 'mem_other', 'mem_account', 'mem_tab'], filter_memory_cases(SCREEN, 1))] + [
    T('mem_f5', 'Tải lại trang (F5) khi đang lọc', 'P2', 'Đang ở danh sách, vừa chọn Trạng thái = Từ chối; chưa mở chi tiết phiếu nào.',
      [MENU, NV, 'Chọn Trạng thái = Từ chối.', 'Nhấn F5.'], '—',
      ['Bộ lọc trở về trống, danh sách hiện đầy đủ.',
       'Lưu ý: bộ lọc chỉ được ghi nhớ khi đi vào màn chi tiết / sửa của chính màn; nếu vừa vào chi tiết trong 10 phút thì F5 '
       'khôi phục bộ lọc của lần đó.']),
]

# ================================================================== III. THÊM MỚI
S3 = [
    T('add_nav', 'Điều hướng vào màn Tạo mới', 'P0', PRE_FORM, TAO, '—',
      ['Mở màn tạo phiếu dạng trang riêng (không phải cửa sổ nổi), có nút Quay lại ở chân màn.']),
    T('add_title', 'Tiêu đề màn Tạo', 'P1', PRE_FORM, TAO + ['Quan sát tiêu đề trang và tab trình duyệt.'], '—',
      ['Tiêu đề "Tạo phiếu yêu cầu điều chỉnh công nợ" ở trang và tab trình duyệt.']),
    T('add_fields', 'Hiển thị các trường và các nút', 'P0', PRE_FORM, TAO + ['Bấm Thêm dòng (+).', 'Quan sát form.'], '—',
      ['Khối Thông tin chung: Loại phiếu, Người tạo, Phòng ban, Diễn giải; góc phải dòng "<Người lập> - <ngày giờ>".',
       'Bảng Chi tiết: khối "Điều chỉnh từ" và "Điều chỉnh đến *", mỗi bên cột Khách hàng, Hợp đồng/Đơn hàng, Số dư cuối kỳ, NVKD, Số tiền.',
       'Dòng nút của nhóm: Thêm điều chỉnh, Chọn nhanh hợp đồng; dòng "Số tiền còn lại"; dòng Tổng cộng.',
       'Chân màn: Lưu nháp, Gửi duyệt, Lưu và tiếp tục, Quay lại.']),
    T('add_required', 'Đánh dấu bắt buộc / không bắt buộc', 'P1', PRE_FORM, TAO + ['Bấm Thêm dòng (+).', 'Quan sát dấu * đỏ.'], '—',
      ['Có dấu *: Loại phiếu, Diễn giải, tiêu đề "Điều chỉnh đến", cột Khách hàng hai bên, cột Số tiền hai bên, Hợp đồng/Đơn hàng bên "đến".',
       'Không có dấu *: Hợp đồng/Đơn hàng bên "từ".', 'Loại nhà cung cấp có thêm Tiền tệ *, ngoại tệ thì Tỷ giá *.']),
    T('add_default', 'Giá trị mặc định', 'P1', PRE_FORM, TAO, '—',
      ['Loại phiếu = "Điều chỉnh công nợ khách hàng".', 'Người tạo = A, Phòng ban = Kinh doanh (chỉ đọc).',
       'Diễn giải trống; bảng ghi "Chưa có dòng điều chỉnh nào.".', 'Không có ô Tiền tệ, Tỷ giá, Số phiếu báo có.']),
    T('add_send_ok', 'Gửi duyệt với đầy đủ thông tin hợp lệ', 'P0', PRE_FORM + ' K là Kế toán thanh toán công ty 1.',
      TAO + DONG + ['Bấm Gửi duyệt.'], '—',
      ['Báo "Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công".', 'Về màn danh sách; phiếu mới ở trên cùng.',
       'Mã TPE.DNDCCN<tháng năm>.NNNNN, trạng thái Chờ tạo phiếu kế toán, có Ngày nhận.', 'K nhận thông báo.']),
    T('add_required_only', 'Gửi duyệt chỉ nhập trường bắt buộc', 'P0', PRE_FORM,
      TAO + ['Nhập Diễn giải "Điều chỉnh".', 'Bấm Thêm dòng; bên "từ" chọn KH-A, KHÔNG chọn hợp đồng, Số tiền 5,000,000.',
             'Bên "đến" chọn KH-B, HĐ-B1, Số tiền 5,000,000.', 'Bấm Gửi duyệt.'], 'Hợp đồng bên "từ": để trống',
      ['Gửi duyệt thành công (hợp đồng bên "từ" không bắt buộc).', 'Chi tiết phiếu: ô hợp đồng bên "từ" trống, Số dư cuối kỳ 0.']),
    T('add_draft_ok', 'Lưu nháp dữ liệu hợp lệ', 'P0', PRE_FORM, TAO + DONG + ['Bấm Lưu nháp.'], '—',
      ['Báo "Lưu phiếu yêu cầu điều chỉnh công nợ thành công".', 'Về màn danh sách; phiếu mới trạng thái "Đang tạo", Ngày nhận trống.',
       'Kế toán thanh toán KHÔNG nhận thông báo.']),
    T('add_draft_missing', 'Lưu nháp khi thiếu trường bắt buộc', 'P0', PRE_FORM,
      TAO + ['Để trống Diễn giải, không thêm dòng.', 'Bấm Lưu nháp.'], 'Diễn giải: trống\nBảng: không có dòng',
      ['Lưu thành công, trạng thái Đang tạo (nháp chỉ bắt buộc Loại phiếu).', 'Không có ô nào bị tô đỏ.']),
    T('add_after', 'Dữ liệu sau lưu', 'P0', 'Phiếu vừa gửi duyệt ở case "Gửi duyệt với đầy đủ thông tin hợp lệ".',
      [MENU, 'Bấm mã phiếu vừa tạo.'], '—',
      ['Loại phiếu, Người tạo, Phòng ban, Diễn giải đúng như đã nhập.',
       'Bảng: 1 nhóm KH-A / HĐ-A1 10,000,000 sang KH-B / HĐ-B1 10,000,000; Số dư cuối kỳ, NVKD tự điền theo hợp đồng.',
       'Số tiền còn lại = 0; Tổng cộng 10,000,000 hai bên.']),
    T('add_history', 'Lịch sử tạo', 'P1', 'Phiếu vừa lưu nháp ở case "Lưu nháp dữ liệu hợp lệ".', [MENU, DOT3 + ' vừa tạo, chọn Lịch sử.'], '—',
      ['Có đúng 1 mốc "Tạo mới", người thực hiện A, thời điểm lưu.', 'Mốc kèm thông tin phiếu và bảng chi tiết lúc tạo.']),
    T('add_send_empty', 'Gửi duyệt khi trống: báo lỗi một lượt', 'P0', PRE_FORM, TAO + ['Bấm Gửi duyệt.'], '—',
      ['Cùng lúc: Diễn giải đỏ "Vui lòng nhập diễn giải"; dưới bảng "Phải có ít nhất một dòng điều chỉnh".',
       'Toast "Vui lòng kiểm tra dữ liệu nhập"; màn cuộn tới ô lỗi đầu tiên.', 'Phiếu không được lưu.']),
    T('add_send_missing_to', 'Gửi duyệt thiếu khách hàng / hợp đồng / số tiền bên đến', 'P0', PRE_FORM,
      TAO + ['Nhập Diễn giải, bấm Thêm dòng.', 'Chọn bên "từ" đủ, bên "đến" để trống, Số tiền "đến" 0.', 'Bấm Gửi duyệt.'], '—',
      ['Cùng lượt: Khách hàng "đến" "Bắt buộc phải nhập", Hợp đồng "đến" "Bắt buộc chọn hợp đồng/đơn hàng", Số tiền "Phải lớn hơn 0".',
       'Lưu ý: mọi ô báo CÙNG MỘT LƯỢT, không báo từng ô một.']),
    T('add_format', 'Sai định dạng ở ô Số tiền', 'P1', PRE_FORM,
      TAO + ['Bấm Thêm dòng.', 'Gõ "abc" vào ô Số tiền bên "từ".', 'Gõ "12000000".'], 'Số tiền: abc ; 12000000',
      ['Bước 3: ô không nhận chữ, vẫn trống.', 'Bước 4: ô tự hiện "12,000,000".']),
    T('add_rate', 'Tỷ giá ngoại tệ không hợp lệ', 'P1', PRE_FORM,
      TAO + ['Chọn Loại phiếu nhà cung cấp, Tiền tệ USD.', 'Xóa Tỷ giá về 0, nhập đủ bảng, Gửi duyệt.'], 'Tỷ giá: 0',
      ['Ô Tỷ giá đỏ "Vui lòng nhập tỷ giá lớn hơn 0".', 'Phiếu không được lưu.']),
    T('add_special', 'Ký tự đặc biệt ở Diễn giải', 'P2', PRE_FORM,
      TAO + ['Nhập Diễn giải "<b>Test</b> & \'nháy\' #@!".', 'Nhập đủ bảng, bấm Lưu nháp.', 'Mở chi tiết phiếu.'],
      'Diễn giải: <b>Test</b> & \'nháy\' #@!',
      ['Lưu thành công (Diễn giải không giới hạn ký tự đặc biệt).', 'Chi tiết hiện đúng nguyên văn, không biến thành chữ đậm.']),
    T('add_minlen', 'Dưới độ dài tối thiểu', 'P2', PRE_FORM, TAO + DONG[1:] + ['Nhập Diễn giải 1 ký tự "a".', 'Bấm Gửi duyệt.'],
      'Diễn giải: a', ['Gửi duyệt thành công: Diễn giải không có độ dài tối thiểu.']),
    T('add_maxlen', 'Độ dài lớn ở Diễn giải', 'P2', PRE_FORM, TAO + DONG[1:] + ['Dán Diễn giải 5,000 ký tự.', 'Bấm Lưu nháp.', 'Mở chi tiết.'],
      'Diễn giải: chuỗi 5,000 ký tự', ['Lưu thành công, chi tiết hiện đủ 5,000 ký tự.',
                                      'Lưu ý: Diễn giải chưa có giới hạn tối đa trên màn và không có thông báo vượt độ dài.']),
    T('add_overlen', 'Vượt độ dài tối đa ở Diễn giải', 'P2', PRE_FORM,
      TAO + DONG[1:] + ['Dán Diễn giải 70,000 ký tự.', 'Bấm Lưu nháp.', 'Mở chi tiết, so độ dài.'], 'Diễn giải: chuỗi 70,000 ký tự',
      ['Màn không chặn, không báo lỗi độ dài.',
       'Lưu ý: nếu sau lưu Diễn giải bị cắt ngắn mà không báo thì ghi nhận lỗi (hệ thống chưa giới hạn độ dài tối đa).']),
    T('add_dup', 'Trùng bản ghi', 'P1', PRE_FORM + ' Đã có phiếu nháp 00402 cùng nội dung.',
      TAO + DONG + ['Bấm Lưu nháp.'], '—',
      ['Lưu thành công, phiếu mới mang mã khác 00402.', 'Phiếu không có trường duy nhất nên không báo trùng.']),
    T('add_trim', 'Khoảng trắng đầu / cuối ở Diễn giải', 'P2', PRE_FORM,
      TAO + DONG[1:] + ['Nhập Diễn giải "   Điều chỉnh   ".', 'Bấm Lưu nháp, mở chi tiết.'], 'Diễn giải: "   Điều chỉnh   "',
      ['Diễn giải lưu thành "Điều chỉnh" (bỏ khoảng trắng hai đầu).']),
    T('add_spaces', 'Diễn giải chỉ có khoảng trắng', 'P1', PRE_FORM,
      TAO + DONG[1:] + ['Nhập Diễn giải "     ".', 'Bấm Gửi duyệt.'], 'Diễn giải: 5 khoảng trắng',
      ['Ô Diễn giải báo "Vui lòng nhập diễn giải" như khi để trống.', 'Phiếu không được gửi.']),
    T('add_err_clear', 'Lỗi biến mất sau khi sửa', 'P1', PRE_FORM,
      TAO + ['Nhập Diễn giải, Thêm dòng, chọn đủ hai bên, Số tiền "từ" 0.', 'Bấm Gửi duyệt.', 'Nhập lại Số tiền "từ" 10,000,000.'],
      'Số tiền: 0 ; 10,000,000', ['Bước 2: ô Số tiền đỏ "Phải lớn hơn 0".', 'Bước 3: lỗi tự mất ngay khi số lớn hơn 0, không cần bấm lại.']),
    T('add_total_mismatch', 'Tổng tiền không khớp', 'P0', PRE_FORM, TAO + DONG + ['Sửa Số tiền "đến" = 8,000,000.', 'Bấm Gửi duyệt.'],
      'Số tiền "đến": 8,000,000',
      ['Dòng "Số tiền còn lại" = 2,000,000 tô đỏ.',
       'Dưới dòng "đến": "Tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh từ (còn thiếu 2,000,000)".', 'Phiếu không được gửi.']),
    T('add_same_contract', 'Bên đến trùng hợp đồng bên từ', 'P0', PRE_FORM,
      TAO + ['Nhập Diễn giải, Thêm dòng.', 'Chọn bên "từ" KH-A / HĐ-A1 10,000,000, bên "đến" cùng KH-A / HĐ-A1 10,000,000.', 'Bấm Lưu nháp.'], '—',
      ['Báo "Hợp đồng điều chuyển đến trùng với điều chuyển từ".', 'Lưu ý: chặn cả khi Lưu nháp; phiếu không được lưu.']),
    T('add_split', 'Chia công nợ cho nhiều nơi nhận', 'P1', PRE_FORM,
      TAO + DONG + ['Sửa "đến" 6,000,000.', 'Bấm Thêm điều chỉnh, chọn KH-C / HĐ-C1, Số tiền 4,000,000.', 'Bấm Gửi duyệt.'], '—',
      ['Gửi thành công; nhóm có 2 dòng "đến"; Số tiền còn lại 0.']),
    T('add_pick_customer', 'Popup chọn khách hàng', 'P1', PRE_FORM, TAO + ['Bấm Thêm dòng, bấm ô Khách hàng bên "từ".', 'Gõ "KH-A", nhấn Enter, bấm dòng KH-A.'], '—',
      ['Cửa sổ "Chọn khách hàng": ô Tên / mã, Mã số thuế, Số điện thoại.',
       'Cột: STT, Mã KH - Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP.',
       'Chọn xong: ô hiện "mã - tên" KH-A, báo "Chọn khách hàng thành công".']),
    T('add_contract_locked', 'Hợp đồng khóa khi chưa chọn khách hàng', 'P1', PRE_FORM,
      TAO + ['Bấm Thêm dòng, chưa chọn khách hàng, rê chuột và bấm ô Hợp đồng/Đơn hàng.'], '—',
      ['Ô bị khóa, gợi ý "Vui lòng chọn khách hàng trước".']),
    T('add_pick_contract', 'Popup chọn hợp đồng', 'P0', PRE_FORM, TAO + ['Bấm Thêm dòng, chọn KH-A, bấm ô Hợp đồng/Đơn hàng.', 'Bấm dòng HĐ-A1.'], '—',
      ['Cửa sổ "Chọn đơn hàng/hợp đồng" ghi tên KH-A: cột Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ.',
       'Chọn xong: Số dư cuối kỳ 50,000,000 và NVKD tự điền.']),
    T('add_no_contract', 'Khách hàng không có hợp đồng', 'P2', PRE_FORM + ' KH-D không có hợp đồng nào.',
      TAO + ['Thêm dòng, chọn KH-D, mở popup hợp đồng.'], '—', ['Popup ghi "Không có hợp đồng phù hợp.".']),
    T('add_change_type', 'Đổi loại phiếu khi đã có dòng', 'P1', PRE_FORM + ' Bảng có 1 nhóm đã nhập.',
      TAO + DONG + ['Đổi Loại phiếu sang "Điều chỉnh công nợ nhà cung cấp".'], '—',
      ['KHÔNG hỏi xác nhận; bảng chi tiết GIỮ NGUYÊN các dòng.',
       'Nhãn cột đổi: Nhà cung cấp, Hợp đồng mua, Số dư, Nhân viên.', 'Hiện ô Tiền tệ = VNĐ, Tỷ giá = 1 (bị khóa).']),
    T('add_foreign', 'Loại NCC ngoại tệ', 'P1', PRE_FORM, TAO + ['Chọn Loại nhà cung cấp, Tiền tệ USD.', 'Quan sát Tỷ giá và bảng.'], '—',
      ['Tỷ giá tự điền theo danh mục tiền tệ, sửa được.', 'Bảng thêm cột Số dư (VNĐ), Số tiền (VNĐ) = số tiền × tỷ giá.']),
    T('add_unknown_supplier', 'NCC bên đến là KHÁCH KHÔNG RÕ', 'P2', PRE_FORM,
      TAO + ['Loại nhà cung cấp; bên "đến" chọn 29TPHPTH-203-KHÁCH KHÔNG RÕ, để trống hợp đồng mua.', 'Gửi duyệt (tổng khớp).'], '—',
      ['Gửi thành công: hợp đồng mua bên "đến" được miễn khi là KHÁCH KHÔNG RÕ.']),
    T('add_from_report', 'Tạo phiếu từ màn chi tiết Phiếu báo có', 'P1',
      'Phiếu báo có TPE.BC1026.00055 loại thu khách hàng có 2 dòng; A có quyền xem phiếu báo có.',
      ['Mở chi tiết phiếu báo có TPE.BC1026.00055, tích 2 dòng.', 'Bấm "Tạo phiếu yêu cầu điều chỉnh công nợ".'], '—',
      ['Mở màn Tạo, có ô Số phiếu báo có = TPE.BC1026.00055.', 'Loại phiếu bị khóa, chú thích "Loại phiếu lấy theo phiếu báo có, không đổi được".',
       '2 nhóm "từ" điền sẵn, chỉ đọc; không có nút Thêm dòng, Xóa nhóm.']),
    T('sc_ok', 'Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, TAO + DONG + ['Bấm Lưu và tiếp tục.'], '—',
      ['Báo "Lưu phiếu yêu cầu điều chỉnh công nợ thành công"; phiếu lưu ở trạng thái Đang tạo.',
       'Vẫn ở màn Tạo; form trở về trống như lúc mới mở (Loại phiếu khách hàng, bảng "Chưa có dòng điều chỉnh nào.").']),
    T('sc_missing', 'Lưu và tiếp tục khi dữ liệu còn thiếu', 'P0',
      PRE_FORM + ' Đã thêm 1 dòng, bên "từ" chọn KH-A nhưng chưa nhập Số tiền, bên "đến" để trống; Diễn giải trống.',
      TAO + ['Bấm Thêm dòng, chọn KH-A bên "từ".', 'Bấm Lưu và tiếp tục.'], 'Diễn giải: trống\nSố tiền: trống',
      ['Phiếu vẫn được lưu nháp (Đang tạo) và mở form trống để lập tiếp — nháp không bắt buộc các ô này.',
       'Lưu ý: các ô thiếu chỉ bị chặn khi Gửi duyệt.']),
    T('sc_format', 'Lưu và tiếp tục khi bên đến trùng bên từ', 'P1', PRE_FORM,
      TAO + ['Nhập Diễn giải, Thêm dòng; hai bên cùng KH-A / HĐ-A1.', 'Bấm Lưu và tiếp tục.'], '—',
      ['Báo "Hợp đồng điều chuyển đến trùng với điều chuyển từ".', 'KHÔNG lưu; form giữ nguyên dữ liệu vừa nhập, không bị làm trống.']),
    T('sc_dup', 'Lưu và tiếp tục hai phiếu cùng nội dung', 'P2', PRE_FORM,
      TAO + DONG + ['Bấm Lưu và tiếp tục.'] + DONG + ['Bấm Lưu và tiếp tục lần nữa.'], '—',
      ['Cả 2 phiếu đều lưu, mã liên tiếp nhau, không báo trùng.']),
    T('sc_close', 'Đóng màn sau Lưu và tiếp tục', 'P2', PRE_FORM, TAO + DONG + ['Bấm Lưu và tiếp tục.', 'Bấm Quay lại.'], '—',
      ['Về danh sách ngay, KHÔNG hỏi "Thông tin chưa lưu" (form trống chưa nhập gì).', 'Danh sách có phiếu nháp vừa lưu ở trên cùng.']),
    T('draft_close', 'Màn sau khi Lưu nháp / Gửi duyệt', 'P1', PRE_FORM, TAO + DONG + ['Bấm Lưu nháp.', 'Bấm Tạo mới lần nữa.'], '—',
      ['Bước 3: rời màn Tạo, về danh sách (không còn ở form).', 'Bước 4: form mới trống hoàn toàn, không còn dữ liệu phiếu trước.',
       'Gửi duyệt thành công cũng về danh sách như vậy.']),
    T('add_from_report_back', 'Lưu xong khi vào từ Phiếu báo có', 'P2', 'Đang ở màn Tạo mở từ chi tiết phiếu báo có TPE.BC1026.00055.',
      ['Nhập Diễn giải, bên "đến" chọn đủ, bấm Gửi duyệt.'], '—', ['Lưu xong quay về màn chi tiết phiếu báo có, không về danh sách.']),
    T('close_empty', 'Đóng khi chưa nhập', 'P1', PRE_FORM, TAO + ['Bấm Quay lại ngay.'], '—', ['Về danh sách, không hỏi xác nhận.']),
    T('close_dirty', 'Đóng khi đã nhập', 'P0', PRE_FORM, TAO + ['Nhập Diễn giải "abc".', 'Bấm Quay lại.'], '—',
      ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", 2 nút Thoát, Ở lại.']),
    T('close_tab', 'Đóng tab / tải lại trang khi đã nhập', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải "abc".', 'Bấm dấu X đóng tab (hoặc F5).'], '—',
      ['Trình duyệt hỏi xác nhận rời trang.', 'Chọn ở lại: form giữ nguyên chữ "abc".',
       'Lưu ý: form là trang riêng nên không có nút X của cửa sổ; case này kiểm bằng dấu X của tab.']),
    T('close_exit', 'Chọn Thoát', 'P1', 'Đang ở hộp "Thông tin chưa lưu" của case "Đóng khi đã nhập".', ['Bấm Thoát.'], '—',
      ['Về danh sách; không có phiếu nào được tạo thêm.']),
    T('close_stay', 'Chọn Ở lại', 'P1', 'Đang ở hộp "Thông tin chưa lưu" của case "Đóng khi đã nhập".', ['Bấm Ở lại.'], '—',
      ['Hộp đóng, vẫn ở màn Tạo, Diễn giải còn "abc".']),
    T('close_cleared', 'Nhập rồi xóa hết', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải "abc".', 'Xóa hết chữ.', 'Bấm Quay lại.'], '—',
      ['Về danh sách, KHÔNG hỏi xác nhận (form giống lúc mới mở).']),
    T('close_restored', 'Đổi rồi khôi phục ban đầu', 'P2', PRE_FORM, TAO + ['Bấm Thêm dòng (+).', 'Bấm thùng rác xóa nhóm vừa thêm.', 'Bấm Quay lại.'],
      '—', ['Về danh sách, KHÔNG hỏi xác nhận (bảng trở lại rỗng như ban đầu).']),
    T('close_idle', 'Không thao tác lâu rồi lưu', 'P2', PRE_FORM + ' Phiên đăng nhập hết hạn trong lúc đang nhập.',
      TAO + DONG + ['Để màn yên tới khi phiên hết hạn.', 'Bấm Lưu nháp.'], '—',
      ['Báo "Phiên đăng nhập đã hết hạn", chuyển về màn đăng nhập.', 'Phiếu không được lưu; dữ liệu đang nhập bị mất.']),
    T('add_double', 'Bấm nút Lưu liên tục', 'P0', PRE_FORM, TAO + DONG + ['Bấm nhanh Gửi duyệt 3 lần liên tiếp.'], '—',
      ['Nút bị khóa ngay sau lần bấm đầu, có lớp tải che màn.', 'Chỉ 1 phiếu được tạo; danh sách không có phiếu trùng.']),
    T('add_concurrent', 'Tạo trùng đồng thời hai tab / tài khoản', 'P2', PRE_FORM + ' Tài khoản A2 cùng công ty.',
      ['A mở màn Tạo ở tab 1, A2 mở màn Tạo ở tab 2, nhập cùng nội dung.', 'Bấm Gửi duyệt ở hai tab gần như cùng lúc.'], '—',
      ['Cả 2 phiếu đều lưu, mã khác nhau và liên tiếp; không có 2 phiếu trùng mã.']),
]

# ================================================================== IV. CHỈNH SỬA
S4 = [
    T('ed_open', 'Mở màn Sửa từ danh sách', 'P0', PRE_NHAP, [MENU, 'Bấm biểu tượng Sửa (bút chì) ở dòng 00402.'], '—',
      ['Mở trang "Sửa phiếu yêu cầu điều chỉnh công nợ: TPE.DNDCCN1026.00402" (trang riêng, không phải cửa sổ nổi).',
       'Từ màn chi tiết bấm Sửa cũng mở đúng trang này.']),
    T('ed_fill', 'Dữ liệu điền đúng', 'P0', PRE_NHAP, [MENU, 'Mở Sửa phiếu 00402.'], '—',
      ['Loại phiếu, Mã phiếu, Người tạo, Phòng ban, Diễn giải đúng như đã lưu.',
       'Bảng có đúng nhóm KH-A / HĐ-A1 10,000,000 sang KH-B / HĐ-B1 10,000,000; Số dư cuối kỳ tính theo công nợ hiện tại.']),
    T('ed_fields', 'Trường cho phép / không cho phép sửa', 'P0', PRE_NHAP, [MENU, 'Mở Sửa phiếu 00402.', 'Thử bấm các ô.'], '—',
      ['Bị khóa: Loại phiếu, Mã phiếu, Người tạo, Phòng ban.', 'Sửa được: Diễn giải, Tiền tệ / Tỷ giá (loại NCC), toàn bộ bảng chi tiết.',
       'Phiếu tạo từ phiếu báo có: bên "từ" chỉ đọc.']),
    T('ed_buttons', 'Các nút ở màn Sửa', 'P1', PRE_NHAP, [MENU, 'Mở Sửa phiếu 00402.'], '—',
      ['Chân màn: Lưu nháp, Gửi duyệt, Quay lại.', 'KHÔNG có nút Lưu và tiếp tục.']),
    T('ed_one', 'Sửa một trường', 'P0', PRE_NHAP, [MENU, 'Mở Sửa phiếu 00402.', 'Sửa Diễn giải thành "Điều chỉnh lần 2".', 'Bấm Lưu nháp.'],
      'Diễn giải: Điều chỉnh lần 2', ['Báo "Lưu phiếu yêu cầu điều chỉnh công nợ thành công", về danh sách.', 'Phiếu vẫn Đang tạo.']),
    T('ed_many', 'Sửa nhiều trường', 'P1', PRE_NHAP,
      [MENU, 'Mở Sửa phiếu 00402.', 'Sửa Diễn giải, Số tiền "từ" 12,000,000.', 'Sửa "đến" KH-B 8,000,000, thêm dòng "đến" KH-C / HĐ-C1 4,000,000.',
       'Bấm Lưu nháp.'], '—', ['Lưu thành công; chi tiết hiện đủ các thay đổi, Tổng cộng 12,000,000 hai bên.']),
    T('ed_same', 'Giữ nguyên giá trị rồi lưu', 'P1', PRE_NHAP, [MENU, 'Mở Sửa phiếu 00402.', 'Không đổi gì, bấm Lưu nháp.'], '—',
      ['Lưu thành công, dữ liệu không đổi.', 'Lịch sử KHÔNG có thêm mốc "Thay đổi thông tin".']),
    T('ed_after', 'Dữ liệu sau lưu', 'P0', 'Vừa sửa phiếu 00402 ở case "Sửa nhiều trường".', [MENU, 'Quan sát dòng 00402.', 'Mở chi tiết.'], '—',
      ['Cột Số tiền = 12,000,000.', 'Chi tiết: 1 nhóm, 2 dòng "đến" đúng khách hàng, hợp đồng, số tiền.']),
    T('ed_updated', 'Ngày / người cập nhật', 'P1', 'Tài khoản A vừa sửa phiếu 00402 lúc 10:15.', [MENU, 'Quan sát dòng 00402.'], '—',
      ['Ngày cập nhật = thời điểm lưu (dd/mm/yyyy 10:15).', 'Người cập nhật = A; Ngày tạo, Người tạo không đổi.']),
    T('ed_history', 'Lịch sử sửa', 'P0', 'Vừa sửa phiếu 00402 ở case "Sửa nhiều trường".', [MENU, DOT3 + ' 00402, chọn Lịch sử.'], '—',
      ['Mốc mới nhất "Thay đổi thông tin", người thực hiện A.', 'Ghi Diễn giải, Tổng tiền cũ và mới; bảng chi tiết khối "Trước" / "Sau" đúng dòng thêm / sửa.']),
    T('ed_required', 'Bỏ trống bắt buộc khi sửa', 'P0', PRE_NHAP, [MENU, 'Mở Sửa phiếu 00402.', 'Xóa hết Diễn giải.', 'Bấm Gửi duyệt.'], 'Diễn giải: trống',
      ['Ô Diễn giải đỏ "Vui lòng nhập diễn giải", toast "Vui lòng kiểm tra dữ liệu nhập".', 'Phiếu giữ Đang tạo, dữ liệu cũ không đổi.']),
    T('ed_format', 'Sai định dạng khi sửa', 'P1', 'A có phiếu nháp loại nhà cung cấp, Tiền tệ USD, Tỷ giá 25,000.',
      [MENU, 'Mở Sửa phiếu.', 'Xóa Tỷ giá về 0.', 'Bấm Gửi duyệt.'], 'Tỷ giá: 0', ['Ô Tỷ giá đỏ "Vui lòng nhập tỷ giá lớn hơn 0"; không lưu.']),
    T('ed_overlimit', 'Vượt giới hạn khi chọn nhanh hợp đồng', 'P1', PRE_NHAP + ' KH-B có HĐ-B1 và HĐ-B2.',
      [MENU, 'Mở Sửa phiếu 00402.', 'Bấm Chọn nhanh hợp đồng, chọn KH-B.', 'Nhập HĐ-B1 7,000,000, HĐ-B2 5,000,000, bấm Áp dụng.'], '—',
      ['Dòng HĐ-B2 đỏ "Tổng số tiền vượt quá số tiền điều chỉnh từ".',
       'Toast "Tổng số tiền điều chỉnh đến không được lớn hơn số tiền điều chỉnh từ"; popup không đóng, bảng không đổi.']),
    T('ed_dup_other', 'Sửa thành trùng nội dung phiếu khác', 'P2', PRE_NHAP + ' A còn phiếu nháp 00403 nội dung khác.',
      [MENU, 'Mở Sửa phiếu 00403.', 'Sửa bảng giống hệt phiếu 00402.', 'Bấm Lưu nháp.'], '—',
      ['Lưu thành công: không kiểm trùng giữa các phiếu (không có trường duy nhất).']),
    T('ed_err_clear', 'Lỗi biến mất khi sửa hợp lệ', 'P1', PRE_NHAP,
      [MENU, 'Mở Sửa phiếu 00402.', 'Sửa Số tiền "đến" về 0, bấm Gửi duyệt.', 'Nhập lại 10,000,000.'], '—',
      ['Bước 3: ô đỏ "Phải lớn hơn 0".', 'Bước 4: lỗi tự mất ngay.']),
    T('ed_reject_resend', 'Sửa phiếu Từ chối rồi gửi lại', 'P0', 'Phiếu 00114 của A bị Từ chối, lý do "Sai hợp đồng nhận".',
      [MENU, 'Mở chi tiết 00114, đọc ô Ghi chú không duyệt.', 'Bấm Sửa, sửa hợp đồng "đến".', 'Bấm Gửi duyệt.'], '—',
      ['Màn chi tiết hiện ô Ghi chú không duyệt "Sai hợp đồng nhận"; màn Sửa không hiện ô này.',
       'Gửi thành công: phiếu Chờ tạo phiếu kế toán, Ngày nhận mới, lý do cũ bị xóa.']),
    T('ed_nochange_close', 'Mở Sửa không thay đổi rồi đóng', 'P1', PRE_NHAP, [MENU, 'Mở Sửa phiếu 00402.', 'Bấm Quay lại.'], '—',
      ['Về danh sách, không hỏi xác nhận.']),
    T('ed_restore', 'Đổi rồi trả về ban đầu', 'P2', PRE_NHAP + ' Diễn giải đang là "Điều chỉnh".',
      [MENU, 'Mở Sửa phiếu 00402.', 'Sửa Diễn giải thành "Điều chỉnh 2".', 'Sửa lại đúng "Điều chỉnh".', 'Bấm Quay lại.'], '—',
      ['Về danh sách, KHÔNG hỏi xác nhận.']),
    T('ed_dirty_close', 'Đóng khi đã đổi', 'P0', PRE_NHAP, [MENU, 'Mở Sửa phiếu 00402.', 'Sửa Diễn giải.', 'Bấm Quay lại.'], '—',
      ['Hộp "Thông tin chưa lưu" với 2 nút Thoát, Ở lại.']),
    T('ed_exit', 'Xác nhận Thoát không lưu', 'P1', 'Đang ở hộp "Thông tin chưa lưu" của case "Đóng khi đã đổi".', ['Bấm Thoát.', 'Mở lại chi tiết 00402.'], '—',
      ['Về danh sách.', 'Diễn giải vẫn là giá trị cũ; Ngày cập nhật không đổi.']),
    T('ed_stay', 'Xác nhận Ở lại', 'P1', 'Đang ở hộp "Thông tin chưa lưu" của case "Đóng khi đã đổi".', ['Bấm Ở lại.'], '—',
      ['Vẫn ở màn Sửa, Diễn giải vừa sửa còn nguyên.']),
    T('ed_no_log', 'Không ghi lịch sử khi hủy sửa', 'P2', PRE_NHAP, [MENU, 'Mở Sửa 00402, sửa Diễn giải, bấm Quay lại, chọn Thoát.', 'Mở Lịch sử 00402.'], '—',
      ['Không có mốc mới nào.']),
    T('ed_deleted', 'Bản ghi bị xóa ở nơi khác khi đang sửa', 'P2', PRE_NHAP,
      ['Tab 1: mở Sửa phiếu 00402.', 'Tab 2: xóa phiếu 00402.', 'Tab 1: sửa Diễn giải, bấm Lưu nháp.'], '—',
      ['Lưu thất bại, hiện thông báo lỗi; không tạo phiếu mới.',
       'Lưu ý: hiện thông báo là "Item Not Found!" (tiếng Anh) — ghi nhận lệch chuẩn thông báo tiếng Việt.']),
    T('ed_concurrent', 'Hai phiên sửa đồng thời', 'P1', PRE_NHAP,
      ['Tab 1 và tab 2 (cùng A) mở Sửa phiếu 00402.', 'Tab 1: bấm Gửi duyệt.', 'Tab 2: sửa Diễn giải, bấm Lưu nháp.'], '—',
      ['Tab 2 báo "Bạn không có quyền sửa phiếu này"; phiếu giữ Chờ tạo phiếu kế toán với dữ liệu của tab 1.',
       'Lưu ý: nếu cả hai tab cùng Lưu nháp thì lần lưu sau ghi đè lần trước (không khóa phiếu khi sửa).']),
    T('ed_in_use', 'Phiếu đang được dùng ở phiếu kế toán', 'P0', 'Phiếu 00401 đã có phiếu kế toán, trạng thái Đã tạo phiếu kế toán.',
      ['A mở danh sách, xem dòng 00401.', 'A mở chi tiết 00401.'], '—',
      ['Không có nút Sửa, Xóa, Gửi duyệt ở cả danh sách và chi tiết.']),
]

# ================================================================== V. XÓA
S5 = [
    T('del_btn', 'Điều kiện hiển thị nút Xóa', 'P0', 'A có phiếu 00402 Đang tạo, 00114 Từ chối, 00401 Chờ tạo phiếu kế toán.',
      ['Đăng nhập A.', MENU, 'Quan sát cột Hành động 3 dòng.'], '—',
      ['00402, 00114: có biểu tượng Xóa (thùng rác đỏ).', '00401: không có nút Xóa.']),
    T('del_popup', 'Popup xác nhận và thông tin', 'P0', PRE_NHAP, [MENU, 'Bấm Xóa ở dòng 00402.'], '—',
      ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa phiếu yêu cầu điều chỉnh công nợ \'TPE.DNDCCN1026.00402\'?".', 'Nút Xóa (đỏ), Hủy, dấu (x).']),
    T('del_ok', 'Xóa phiếu không ràng buộc', 'P0', PRE_NHAP + ' A có 23 phiếu.', ['Đăng nhập A.', MENU, 'Bấm Xóa dòng 00402.', 'Bấm Xóa.'], '—',
      ['Báo "Xóa thành công".', 'Dòng 00402 không còn; dòng tổng "Hiển thị 1–10 / 22".', 'Tìm "00402" ra "Không có dữ liệu phù hợp bộ lọc.".']),
    T('del_cancel', 'Hủy xóa', 'P1', PRE_NHAP, [MENU, 'Bấm Xóa dòng 00402, bấm Hủy.', 'Bấm Xóa lần nữa, bấm dấu (x).'], '—',
      ['Hộp đóng, phiếu còn nguyên, tổng số không đổi.']),
    T('del_in_use', 'Xóa phiếu đang được sử dụng', 'P0', 'Phiếu 00401 của A đã có phiếu kế toán (Đã tạo phiếu kế toán).',
      ['Đăng nhập A.', MENU, 'Tìm dòng 00401, mở chi tiết.'], '—',
      ['Không có nút Xóa ở danh sách lẫn chi tiết.', 'Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa: báo "Bạn không có quyền xóa phiếu này", phiếu còn.']),
    T('del_children', 'Xóa phiếu có dữ liệu cấp con', 'P1', 'A có phiếu nháp 00405 gồm 2 nhóm "từ", tổng 3 dòng "đến".',
      [MENU, 'Xóa phiếu 00405.', 'Mở lại đường link chi tiết 00405 đã lưu trước đó.'], '—',
      ['Xóa thành công cả phiếu và 5 dòng chi tiết (không chặn vì dữ liệu con).', 'Đường link cũ báo "Không tải được dữ liệu phiếu".']),
    T('del_detail', 'Xóa từ màn chi tiết', 'P1', PRE_NHAP, [MENU, 'Mở chi tiết 00402.', 'Bấm Xóa ở chân màn, bấm Xóa.'], '—',
      ['Báo "Xóa thành công", tự quay về danh sách.']),
    T('del_gone', 'Phiếu đã bị người khác xóa', 'P2', PRE_NHAP, ['Tab 1 và tab 2 cùng mở danh sách.', 'Tab 1 xóa 00402.', 'Tab 2 bấm Xóa dòng 00402, bấm Xóa.'],
      '—', ['Tab 2 báo lỗi, không treo; nạp lại thì dòng biến mất.',
            'Lưu ý: hiện thông báo là "Item Not Found!" (tiếng Anh) — ghi nhận lệch chuẩn thông báo tiếng Việt.']),
    T('del_changed', 'Phiếu vừa đổi trạng thái ở tab khác', 'P1', PRE_NHAP,
      ['Tab 1 mở danh sách.', 'Tab 2 gửi duyệt 00402.', 'Tab 1 bấm Xóa 00402, bấm Xóa.'], '—',
      ['Báo "Bạn không có quyền xóa phiếu này".', 'Danh sách tự nạp lại: 00402 ở trạng thái Chờ tạo phiếu kế toán, không còn nút Xóa.']),
    T('del_related', 'Dữ liệu liên quan sau xóa', 'P2', 'Phiếu nháp TPE.DNDCCN1026.00410 là mã lớn nhất tháng 10 của công ty TPE.',
      ['Xóa phiếu 00410.', 'Lập phiếu mới, Lưu nháp.'], '—',
      ['Phiếu mới mang mã 00411, KHÔNG cấp lại 00410.', 'Phiếu báo có / hợp đồng đã chọn trên phiếu xóa không bị thay đổi.']),
]

# ================================================================== VI. LỊCH SỬ THAY ĐỔI
PRE_HIS = ('Phiếu 00402 có 4 mốc: Tạo mới (A, 20/10), Thay đổi thông tin (A, 21/10), Thay đổi trạng thái Đang tạo → Chờ tạo '
           'phiếu kế toán (A, 22/10), Thay đổi trạng thái Chờ tạo phiếu kế toán → Từ chối (K, 23/10).').replace('→', 'sang')
S6 = [
    T('his_open', 'Mở popup lịch sử', 'P0', PRE_HIS, [MENU, DOT3 + ' 00402, chọn Lịch sử.'], '—',
      ['Cửa sổ "Lịch sử thay đổi: TPE.DNDCCN1026.00402".', 'Có nút Bộ lọc, nút Đóng và dấu (x).']),
    T('his_cols', 'Thông tin của mỗi mốc', 'P1', PRE_HIS, [MENU, 'Mở Lịch sử 00402.'], '—',
      ['Mỗi mốc có: loại hành động, "Người thực hiện: <tên>", thời điểm dd/mm/yyyy hh:mm, nội dung thay đổi.']),
    T('his_order', 'Mới nhất trước', 'P0', PRE_HIS, [MENU, 'Mở Lịch sử 00402.'], '—',
      ['Thứ tự từ trên xuống: Từ chối (23/10), gửi duyệt (22/10), Thay đổi thông tin (21/10), Tạo mới (20/10).']),
    T('his_actor', 'Người thực hiện và thời gian', 'P1', PRE_HIS, [MENU, 'Mở Lịch sử 00402.'], '—',
      ['Mốc Từ chối ghi người thực hiện K; các mốc khác ghi A.', 'Thời điểm đúng ngày giờ thao tác.']),
    T('his_type', 'Loại hành động', 'P1', PRE_HIS, [MENU, 'Mở Lịch sử 00402.'], '—',
      ['Có đủ nhãn: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.']),
    T('his_content', 'Nội dung thay đổi cũ và mới', 'P0', PRE_HIS, [MENU, 'Mở Lịch sử 00402, đọc mốc Thay đổi thông tin và mốc Từ chối.'], '—',
      ['Thay đổi thông tin: từng trường giá trị cũ và mới; bảng chi tiết khối "Trước" / "Sau".',
       'Từ chối: trạng thái Chờ tạo phiếu kế toán sang Từ chối, kèm lý do.', 'Số tiền, tỷ giá có dấu phẩy ngăn nghìn như trên màn.']),
    T('his_f_action', 'Lọc theo hành động', 'P1', PRE_HIS, [MENU, 'Mở Lịch sử 00402.', 'Bấm Bộ lọc, chọn Loại hành động = Thay đổi trạng thái.'], '—',
      ['Chỉ còn 2 mốc Thay đổi trạng thái.', 'Ô Loại hành động chỉ liệt kê các loại đã có của phiếu.']),
    T('his_f_actor', 'Lọc theo người thực hiện', 'P1', PRE_HIS, [MENU, 'Mở Lịch sử 00402, bấm Bộ lọc.', 'Chọn Người thực hiện = K.'], '—',
      ['Chỉ còn mốc Từ chối.', 'Ô Người thực hiện dạng "Tên - Mã phòng - Mã NV".']),
    T('his_f_date', 'Lọc theo thời gian', 'P1', PRE_HIS, [MENU, 'Mở Lịch sử 00402, bấm Bộ lọc.', 'Chọn Từ ngày 21/10/2026, Đến ngày 22/10/2026.'], '—',
      ['Còn 2 mốc ngày 21/10 và 22/10; lọc ngay khi chọn, không có nút Tìm kiếm.']),
    T('his_f_combo', 'Kết hợp lọc', 'P2', PRE_HIS, [MENU, 'Mở Lịch sử 00402, bấm Bộ lọc.', 'Chọn Loại hành động = Thay đổi trạng thái và Người thực hiện = A.'],
      '—', ['Chỉ còn mốc gửi duyệt ngày 22/10.']),
    T('his_f_none', 'Không có kết quả lọc', 'P2', PRE_HIS, [MENU, 'Mở Lịch sử 00402, bấm Bộ lọc.', 'Chọn Người thực hiện = K, Từ ngày 20/10 đến 21/10.'],
      '—', ['Hiện "Không có lịch sử phù hợp bộ lọc.".']),
    T('his_f_reset', 'Làm mới bộ lọc lịch sử', 'P2', 'Đang lọc lịch sử 00402 theo Người thực hiện = K.', ['Bấm Làm mới trong vùng lọc.'], '—',
      ['Các ô lọc trống, hiện lại đủ 4 mốc.']),
    T('his_f_toggle', 'Đóng / mở bộ lọc', 'P2', PRE_HIS, [MENU, 'Mở Lịch sử 00402.', 'Bấm Bộ lọc.', 'Bấm Bộ lọc lần nữa.'], '—',
      ['Bước 2: hiện 4 ô lọc.', 'Bước 3: thu gọn vùng lọc.']),
    T('his_create', 'Ghi nhận khi tạo mới', 'P0', PRE_FORM, TAO + DONG + ['Bấm Lưu nháp.', 'Mở Lịch sử phiếu vừa tạo.'], '—',
      ['Có mốc "Tạo mới" của A kèm thông tin phiếu và bảng chi tiết.']),
    T('his_edit_one', 'Ghi nhận khi sửa một trường', 'P1', PRE_NHAP, ['Sửa Diễn giải phiếu 00402, Lưu nháp.', 'Mở Lịch sử.'], '—',
      ['Mốc "Thay đổi thông tin" chỉ ghi Diễn giải cũ và mới, không liệt kê trường không đổi.']),
    T('his_edit_many', 'Ghi nhận khi sửa nhiều trường', 'P1', PRE_NHAP,
      ['Sửa Diễn giải, Số tiền hai bên của 00402 thành 12,000,000, Lưu nháp.', 'Mở Lịch sử.'], '—',
      ['Một mốc "Thay đổi thông tin" ghi Diễn giải, Tổng tiền và các dòng chi tiết đổi số tiền.']),
    T('his_nochange', 'Không ghi khi không đổi', 'P1', PRE_NHAP, ['Mở Sửa 00402, không đổi gì, bấm Lưu nháp.', 'Mở Lịch sử.'], '—',
      ['Không có mốc mới.']),
    T('his_multi', 'Đổi nhiều thông tin cùng lúc kèm gửi duyệt', 'P1', 'Phiếu 00114 của A đang Từ chối.',
      ['Mở Sửa 00114, sửa Diễn giải và hợp đồng "đến".', 'Bấm Gửi duyệt.', 'Mở Lịch sử 00114.'], '—',
      ['Một mốc "Thay đổi thông tin" ghi đủ: Diễn giải, dòng "đến" đổi hợp đồng, Trạng thái Từ chối sang Chờ tạo phiếu kế toán.']),
    T('his_status', 'Ghi nhận gửi duyệt từ màn chi tiết', 'P1', PRE_NHAP, ['Mở chi tiết 00402, bấm Gửi duyệt.', 'Mở khối Lịch sử.'], '—',
      ['Mốc "Thay đổi trạng thái" Đang tạo sang Chờ tạo phiếu kế toán, người thực hiện A.']),
    T('his_empty', 'Phiếu chưa có lịch sử', 'P2', 'Phiếu 00098 lập trước khi hệ thống bật ghi lịch sử.', [MENU, 'Mở Lịch sử 00098.'], '—',
      ['Hiện "Chưa có lịch sử thao tác nào.".']),
    T('his_close', 'Đóng bằng Đóng / X', 'P1', PRE_HIS, [MENU, 'Mở Lịch sử 00402, bấm Đóng.', 'Mở lại, bấm dấu (x).', 'Mở lại, bấm ra ngoài cửa sổ.'],
      '—', ['Mỗi cách đều đóng cửa sổ.']),
    T('his_keep', 'Trạng thái danh sách sau khi đóng', 'P1', 'Đang ở trang 3, lọc Trạng thái = Từ chối, sắp theo Số tiền.',
      [DOT3 + ' bất kỳ, chọn Lịch sử.', 'Bấm Đóng.'], '—', ['Danh sách giữ nguyên trang 3, bộ lọc, thứ tự sắp xếp.']),
]

# ================================================================== VII. XEM CHI TIẾT
S7 = [
    T('dt_open', 'Mở màn chi tiết', 'P0', PRE_CHO, [MENU, 'Bấm mã TPE.DNDCCN1026.00401.'], '—',
      ['Mở trang chi tiết (trang riêng); có nút Quay lại ở chân màn.']),
    T('dt_title', 'Tiêu đề màn chi tiết', 'P1', PRE_CHO, [MENU, 'Mở chi tiết 00401.'], '—',
      ['Tiêu đề "Chi tiết phiếu yêu cầu điều chỉnh công nợ: TPE.DNDCCN1026.00401" ở trang và tab.']),
    T('dt_fields', 'Đầy đủ trường', 'P0', PRE_CHO, [MENU, 'Mở chi tiết 00401.'], '—',
      ['Loại phiếu, Mã phiếu, Người tạo, Phòng ban, Diễn giải; dòng người lập - ngày giờ.',
       'Bảng "Điều chỉnh từ" / "Điều chỉnh đến" gộp dòng đúng nhóm, dòng Số tiền còn lại, Tổng cộng.', 'Khối Lịch sử ở cuối.']),
    T('dt_match_create', 'Khớp dữ liệu lúc tạo', 'P0', 'Phiếu vừa tạo ở case "Gửi duyệt với đầy đủ thông tin hợp lệ".', [MENU, 'Mở chi tiết phiếu đó.'], '—',
      ['Mọi giá trị trùng khớp dữ liệu đã nhập lúc tạo.']),
    T('dt_match_list', 'Khớp với danh sách', 'P1', PRE_CHO, [MENU, 'Ghi lại các cột của dòng 00401.', 'Mở chi tiết 00401.'], '—',
      ['Mã phiếu, Loại phiếu, Người tạo, Phòng ban, Tổng tiền khớp với dòng danh sách.']),
    T('dt_readonly', 'Trường chỉ đọc', 'P0', PRE_CHO, [MENU, 'Mở chi tiết 00401.', 'Thử gõ vào các ô.'], '—',
      ['Mọi ô chỉ đọc; bảng không có nút Thêm dòng, Xóa, Chọn nhanh hợp đồng.']),
    T('dt_no_save', 'Không có nút Lưu', 'P1', PRE_CHO, [MENU, 'Mở chi tiết 00401.'], '—',
      ['Không có nút Lưu nháp, Lưu và tiếp tục.', 'Nút Gửi duyệt chỉ có với người lập và phiếu Đang tạo / Từ chối.']),
    T('dt_buttons', 'Nút theo trạng thái và vai trò', 'P0', PRE_NHAP + ' ' + PRE_CHO, ['A mở chi tiết 00402.', 'K mở chi tiết 00401.'], '—',
      ['00402 (A): Sửa, Gửi duyệt, In phiếu, Xuất Excel, Xóa, Quay lại.', '00401 (K): Tạo phiếu kế toán, Từ chối, In phiếu, Xuất Excel, Quay lại.']),
    T('dt_reject_note', 'Phiếu Từ chối hiện lý do', 'P1', 'Phiếu 00114 Từ chối, lý do "Sai hợp đồng nhận".', [MENU, 'Mở chi tiết 00114.'], '—',
      ['Có ô "Ghi chú không duyệt" = "Sai hợp đồng nhận", chỉ đọc.']),
    T('dt_history', 'Khu vực lịch sử', 'P1', PRE_HIS, [MENU, 'Mở chi tiết 00402.', 'Bấm Xem lịch sử.', 'Bấm Thu gọn.'], '—',
      ['Mặc định khối Lịch sử thu gọn.', 'Mở ra: có nút Làm mới, Bộ lọc, các mốc mới nhất trên cùng.', 'Thu gọn lại được.']),
    T('dt_close', 'Đóng màn chi tiết', 'P1', PRE_CHO, [MENU, 'Mở chi tiết 00401.', 'Bấm Quay lại.'], '—',
      ['Về màn danh sách, không hỏi xác nhận (màn chỉ đọc).']),
    T('dt_keep', 'Giữ trang và bộ lọc khi quay lại', 'P1', 'Đang ở trang 3, lọc Trạng thái = Từ chối, sắp Số tiền giảm dần.',
      ['Bấm mã một phiếu ở trang 3.', 'Bấm Quay lại.'], '—',
      ['Danh sách giữ bộ lọc Trạng thái = Từ chối và thứ tự sắp xếp.',
       'Lưu ý: số trang trở về trang 1 (hệ thống chỉ nhớ bộ lọc, không nhớ trang đang xem).']),
]

# ================================================================== VIII. TÙY CHỈNH CỘT
S8 = [
    T('col_open', 'Mở popup tùy chỉnh cột', 'P1', PRE_LIST, [MENU, 'Bấm nút Cấu hình cột hiển thị.'], '—',
      ['Cửa sổ "Tuỳ chỉnh cột": danh sách cột có ô tích, biểu tượng kéo; nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng, dấu (x).']),
    T('col_list', 'Danh sách cột', 'P1', PRE_LIST, [MENU, 'Mở Tùy chỉnh cột.'], '—',
      ['Đủ 15 cột đúng thứ tự trên bảng.']),
    T('col_default', 'Cột chọn mặc định', 'P2', 'Tài khoản chưa từng lưu Tùy chỉnh cột.', [MENU, 'Mở Tùy chỉnh cột.'], '—',
      ['Cả 15 cột đều được tích.']),
    T('col_show', 'Hiện cột đang ẩn', 'P1', 'Đã ẩn cột Phòng ban.', [MENU, 'Mở Tùy chỉnh cột, tích Phòng ban, bấm Lưu.'], '—',
      ['Cột Phòng ban hiện lại đúng vị trí.']),
    T('col_hide', 'Ẩn cột', 'P0', PRE_LIST, [MENU, 'Mở Tùy chỉnh cột, bỏ tích Phòng ban, Người duyệt, bấm Lưu.'], '—',
      ['Bảng không còn 2 cột này; các cột khác giữ thứ tự.']),
    T('col_locked', 'Cột bắt buộc không ẩn được', 'P0', PRE_LIST, [MENU, 'Mở Tùy chỉnh cột.', 'Thử bỏ tích STT, Mã phiếu, Hành động.', 'Bấm Bỏ chọn hết.'], '—',
      ['3 cột xám, có ổ khóa, rê chuột hiện "Cột bắt buộc — không thể ẩn hoặc đổi vị trí".',
       'Bỏ chọn hết: 3 cột này vẫn tích.']),
    T('col_drag', 'Kéo thả thứ tự', 'P1', PRE_LIST, [MENU, 'Mở Tùy chỉnh cột.', 'Kéo Trạng thái lên ngay sau Loại phiếu, bấm Lưu.'], '—',
      ['Bảng hiện cột Trạng thái ngay sau Loại phiếu.']),
    T('col_fixed', 'Cột cố định', 'P2', PRE_LIST, [MENU, 'Cuộn ngang bảng sang phải.', 'Mở Tùy chỉnh cột, thử kéo STT, Mã phiếu, Hành động.'], '—',
      ['STT, Mã phiếu luôn ghim bên trái khi cuộn.', '3 cột khóa không kéo được; Hành động luôn ở cuối.']),
    T('col_save', 'Lưu cấu hình', 'P0', PRE_LIST, [MENU, 'Ẩn cột Số phiếu báo có, bấm Lưu.'], '—',
      ['Cửa sổ đóng, bảng vẽ lại ngay theo cấu hình mới.']),
    T('col_close', 'Đóng không lưu', 'P1', PRE_LIST, [MENU, 'Mở Tùy chỉnh cột, bỏ tích Người tạo.', 'Bấm Đóng (hoặc dấu x).'], '—',
      ['Bảng vẫn có cột Người tạo; mở lại cửa sổ thì Người tạo vẫn tích.']),
    T('col_f5', 'Ghi nhớ sau F5', 'P1', 'Đã ẩn cột Số phiếu báo có và lưu.', ['Nhấn F5.', 'Đăng xuất, đăng nhập lại.'], '—',
      ['Cả hai lần bảng vẫn ẩn cột Số phiếu báo có.']),
    T('col_account', 'Hiển thị theo tài khoản', 'P1', 'Tài khoản A đã ẩn cột Phòng ban; tài khoản B chưa cấu hình.',
      ['B đăng nhập cùng máy, mở danh sách.', 'A đăng nhập trên trình duyệt khác / máy khác.'], '—',
      ['B thấy đủ 15 cột.', 'A ở trình duyệt khác vẫn không có cột Phòng ban (lưu theo tài khoản, không theo trình duyệt).']),
    T('col_data', 'Không ảnh hưởng dữ liệu', 'P2', 'Đã ẩn cột Số tiền.', [MENU, 'Xem tổng số.', 'Bấm Xuất Excel.'], '—',
      ['Tổng số phiếu không đổi.', 'File Excel vẫn có cột Số tiền.']),
    T('col_filter', 'Không ảnh hưởng lọc', 'P2', 'Đã ẩn cột Trạng thái.', [MENU, NV, 'Lọc Trạng thái = Từ chối.'], '—',
      ['Lọc vẫn đúng, còn các phiếu Từ chối dù cột Trạng thái đang ẩn.']),
    T('col_all', 'Chọn tất cả / Bỏ chọn hết', 'P2', 'Đã ẩn 4 cột.', [MENU, 'Mở Tùy chỉnh cột, bấm Chọn tất cả.', 'Bấm Bỏ chọn hết.'], '—',
      ['Chọn tất cả: tích đủ 15 cột.', 'Bỏ chọn hết: chỉ còn 3 cột khóa được tích.']),
    T('col_pending', 'Dùng chung cho màn chờ duyệt', 'P2', 'K đã ẩn cột Phòng ban ở danh sách chung.', [MENU_CD, 'Quan sát tiêu đề cột.'], '—',
      ['Màn chờ duyệt cũng không có cột Phòng ban.']),
]

# ================================================================== IX. XUẤT EXCEL
FILE = 'Danh-sach-yeu-cau-dieu-chinh-cong-no-<năm-tháng-ngày>.xlsx'
S9 = [
    T('xl_no_popup', 'Không có cửa sổ chọn trường xuất', 'P1', PRE_LIST, [MENU, 'Bấm Xuất Excel trên thanh công cụ.'], '—',
      ['Không mở cửa sổ chọn trường; file tải về ngay.', 'Lưu ý: màn chưa có chức năng chọn trường / thứ tự trường xuất.']),
    T('xl_fixed_cols', 'File luôn đủ 12 cột cố định', 'P1', 'Đã ẩn cột Phòng ban, Người duyệt bằng Tùy chỉnh cột.', [MENU, 'Bấm Xuất Excel.'], '—',
      ['File vẫn có đủ 12 cột (không theo Tùy chỉnh cột).', 'Không có cột Ngày cập nhật, Người cập nhật, Hành động.']),
    T('xl_search', 'Xuất theo tìm kiếm', 'P0', 'Tháng 10/2026 có 160 phiếu.', [MENU, 'Tìm nhanh "DNDCCN1026".', 'Bấm Xuất Excel.'], '—',
      ['File có đúng 160 dòng dữ liệu, đều mã chứa "DNDCCN1026".']),
    T('xl_filter', 'Xuất theo bộ lọc', 'P0', 'Có 37 phiếu Từ chối.', [MENU, NV, 'Lọc Trạng thái = Từ chối.', 'Bấm Xuất Excel.'], '—',
      ['File có đúng 37 dòng, cột Trạng thái đều "Từ chối".', 'Báo "Xuất Excel thành công".']),
    T('xl_pages', 'Xuất khi kết quả nhiều trang', 'P1', 'Có 37 phiếu Từ chối; đang xem trang 2, 10 dòng/trang.', [MENU, 'Bấm Xuất Excel.'], '—',
      ['File có đủ 37 dòng, không chỉ 10 dòng của trang đang xem.']),
    T('xl_empty', 'Xuất khi danh sách rỗng', 'P1', PRE_LIST, [MENU, 'Tìm nhanh "XYZ999".', 'Bấm Xuất Excel.'], '—',
      ['Vẫn tải file: logo công ty, tiêu đề "DANH SÁCH PHIẾU YÊU CẦU ĐIỀU CHỈNH CÔNG NỢ", hàng tên cột, không có dòng dữ liệu.']),
    T('xl_name', 'Tên file', 'P2', PRE_LIST, [MENU, 'Bấm Xuất Excel ngày 02/11/2026.'], '—',
      ['File tên "Danh-sach-yeu-cau-dieu-chinh-cong-no-2026-11-02.xlsx".']),
    T('xl_format', 'Định dạng file', 'P2', PRE_LIST, [MENU, 'Xuất Excel, mở file bằng Excel.'], '—', ['File .xlsx mở được, không báo hỏng.']),
    T('xl_head', 'Tiêu đề cột', 'P1', PRE_LIST, [MENU, 'Xuất Excel, mở file.'], '—',
      ['Dòng 1 logo công ty của người đang đăng nhập; tiêu đề in đậm, gộp ô, canh giữa.', 'Hàng tên cột in đậm, kẻ viền toàn bảng.']),
    T('xl_order', 'Thứ tự cột', 'P1', PRE_LIST, [MENU, 'Xuất Excel, mở file.'], '—',
      ['STT, Mã phiếu, Loại phiếu, Số phiếu báo có, KH / NCC, Số tiền, Ngày tạo, Người tạo, Phòng ban, Ngày nhận, Người duyệt, Trạng thái.']),
    T('xl_count', 'Số lượng bản ghi', 'P1', PRE_LIST, [MENU, 'Không lọc gì, bấm Xuất Excel.'], '—',
      ['File chỉ chứa 5,000 dòng đầu theo thứ tự đang sắp (giới hạn xuất).', 'Lọc còn 37 phiếu thì file đúng 37 dòng.']),
    T('xl_data', 'Dữ liệu khớp danh sách', 'P0', 'Có 37 phiếu Từ chối.', [MENU, 'Lọc Từ chối, xuất Excel.', 'So 10 dòng đầu với trang 1.'], '—',
      ['Cùng thứ tự; mã, loại, KH / NCC, số tiền, ngày, người, trạng thái trùng khớp.']),
    T('xl_types', 'Định dạng ngày / số / chữ', 'P1', PRE_LIST, [MENU, 'Xuất Excel, mở file.', 'Chọn cả cột Số tiền.'], '—',
      ['Số tiền là ô số dạng 1,234,567, Excel cộng SUM được, không báo "formatted as text".',
       'Ngày tạo, Ngày nhận dạng dd/mm/yyyy hh:mm.', 'Chữ dài tự xuống dòng trong ô.']),
    T('xl_vn', 'Tiếng Việt và ký tự đặc biệt', 'P2', 'Có phiếu của khách "Công ty Nghệ An & Cộng sự".', [MENU, 'Xuất Excel, mở file.'], '—',
      ['Tên hiện đúng dấu ("Nghệ", không ra "Nghẽ"), dấu & giữ nguyên.']),
    T('xl_pending', 'Xuất ở màn chờ duyệt', 'P1', 'Công ty 1 có 5 phiếu chờ; K là Kế toán thanh toán.', [MENU_CD, 'Bấm Xuất Excel.'], '—',
      ['File có đúng 5 dòng Chờ tạo phiếu kế toán.']),
    T('xl_busy', 'Khóa nút trong lúc xuất', 'P2', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm tiếp ngay lần nữa.'], '—',
      ['Nút đổi chữ "Đang xuất..." và bị khóa; chỉ tải 1 file.']),
    T('xl_one', 'Xuất Excel một phiếu', 'P1', PRE_CHO, [MENU, DOT3 + ' 00401, chọn Xuất Excel.'], '—',
      ['Tải file "Yeu-cau-dieu-chinh-cong-no-TPE-DNDCCN1026-00401.xlsx".',
       'File có logo công ty ghi trên phiếu, thông tin chung và bảng từ / đến như bản in.']),
]

# ================================================================== X. ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU
S10 = [
    T('ef_no_child', 'Tạo khi chưa có dữ liệu con', 'P1', PRE_FORM, TAO + ['Nhập Diễn giải, không thêm dòng.', 'Bấm Lưu nháp.', 'Mở chi tiết, bấm Gửi duyệt.'], '—',
      ['Lưu nháp được.', 'Gửi duyệt báo "Phiếu chưa có dòng điều chỉnh nào", phiếu giữ Đang tạo.']),
    T('ef_child', 'Tạo khi có dữ liệu con', 'P1', PRE_FORM, TAO + ['Thêm 2 nhóm, mỗi nhóm 2 dòng "đến", tổng khớp.', 'Gửi duyệt, mở chi tiết.'], '—',
      ['Chi tiết đúng 2 nhóm, mỗi nhóm 2 dòng "đến" nằm dưới đúng nhóm "từ".']),
    T('ef_edit_link', 'Không mất liên kết khi sửa', 'P1', 'Phiếu 00114 Từ chối; K là Kế toán thanh toán.',
      ['A sửa hợp đồng "đến" của 00114 thành HĐ-C1, gửi duyệt.', 'K bấm Tạo phiếu kế toán ở 00114.'], '—',
      ['Màn Tạo phiếu kế toán điền sẵn đúng phiếu 00114 với hợp đồng mới HĐ-C1.']),
    T('ef_appear', 'Phiếu tạo xuất hiện ở màn liên quan', 'P0', PRE_FORM + ' K là Kế toán thanh toán công ty 1.',
      ['A lập phiếu, Gửi duyệt.', 'K mở màn chờ duyệt.', 'K mở màn Phiếu kế toán, bấm chọn phiếu yêu cầu.'], '—',
      ['Phiếu có ở màn chờ duyệt của K.', 'Phiếu có trong danh sách chọn phiếu yêu cầu của màn Phiếu kế toán.']),
    T('ef_rename', 'Đổi thông tin đồng bộ sang màn liên quan', 'P1', 'Phiếu 00114 Từ chối, bên "đến" KH-B.',
      ['A sửa bên "đến" thành KH-C, gửi duyệt.', 'Xem dòng 00114 ở danh sách và ở màn chờ duyệt.'], '—',
      ['Cột KH / NCC hiện KH-C ở cả 2 nơi.']),
    T('ef_delete_sync', 'Xóa đồng bộ', 'P1', 'Phiếu 00401 Đã tạo phiếu kế toán qua phiếu kế toán PKT-0091.',
      ['Kế toán xóa phiếu kế toán PKT-0091.', 'Mở danh sách và màn chờ duyệt.'], '—',
      ['Phiếu 00401 trở về Chờ tạo phiếu kế toán, có lại ở màn chờ duyệt.', 'Lịch sử 00401 có mốc Thay đổi trạng thái về Chờ tạo phiếu kế toán.']),
    T('ef_status_auto', 'Trạng thái tự động cập nhật', 'P0', PRE_CHO,
      ['K Tạo phiếu kế toán từ 00401, Lưu nháp phiếu kế toán.', 'K Lưu và duyệt phiếu kế toán.'], '—',
      ['Bước 1: 00401 sang Đã tạo phiếu kế toán (nhãn xanh).', 'Bước 2: 00401 sang Đã duyệt phiếu kế toán.']),
    T('ef_filter', 'Bộ lọc màn liên quan cập nhật', 'P1', PRE_CHO, ['K Tạo và lưu phiếu kế toán từ 00401.', 'K mở màn chờ duyệt.', 'Lọc danh sách chung theo Trạng thái = Đã tạo phiếu kế toán.'],
      '—', ['00401 không còn ở màn chờ duyệt.', '00401 có trong kết quả lọc Đã tạo phiếu kế toán.']),
    T('ef_parent', 'Cấp con đúng cấp cha', 'P1', 'Phiếu 00405: nhóm 1 KH-A sang KH-B, KH-C; nhóm 2 KH-D sang KH-E.',
      ['Mở chi tiết 00405.', 'In phiếu.', 'Xuất Excel một phiếu.'], '—',
      ['Ở cả 3 nơi: KH-B, KH-C nằm dưới nhóm KH-A; KH-E nằm dưới nhóm KH-D.']),
    T('ef_ref_keep', 'Tham chiếu không mất khi đổi trạng thái', 'P1', 'Phiếu 00371 tạo từ phiếu báo có TPE.BC1026.00055.',
      ['K từ chối 00371.', 'A sửa, gửi duyệt lại.', 'K tạo và duyệt phiếu kế toán.'], '—',
      ['Sau mỗi bước, cột Số phiếu báo có vẫn là TPE.BC1026.00055 và còn bấm được.', 'Phiếu kế toán ghi đúng mã 00371.']),
    T('ef_orphan', 'Không có bản ghi mồ côi', 'P1', 'Phiếu nháp 00405 có 2 nhóm.',
      ['Mở Sửa 00405, bấm thùng rác xóa nhóm 2.', 'Lưu nháp, mở chi tiết.'], '—',
      ['Chỉ còn nhóm 1; các dòng "đến" của nhóm 2 cũng biến mất, Tổng cộng tính lại.']),
    T('ef_no_dup', 'Không có dữ liệu trùng', 'P1', PRE_FORM + ' KH-B có HĐ-B1, HĐ-B2.',
      TAO + ['Thêm dòng, bên "từ" KH-A 10,000,000.', 'Chọn nhanh hợp đồng: KH-B, HĐ-B1 4,000,000, Áp dụng.',
             'Chọn nhanh lần nữa: KH-B, HĐ-B1 6,000,000, HĐ-B2 4,000,000, Áp dụng.'], '—',
      ['Sau bước 4 bảng chỉ còn 2 dòng "đến" KH-B (dòng cũ được thay), không nhân đôi HĐ-B1.']),
]

# ================================================================== XI. PHÂN QUYỀN (khối phân quyền đầu file được đưa vào đầu nhóm này)
S11 = [
    T('pq_create', 'Thêm mới không cần quyền riêng', 'P0', 'Tài khoản A không có quyền nào của màn.', ['Đăng nhập A.', MENU, 'Bấm Tạo mới, lập phiếu, Lưu nháp.'], '—',
      ['Có nút Tạo mới; lưu thành công, người tạo là A.']),
    T('pq_export', 'Xuất Excel theo phạm vi quyền', 'P1', 'Tài khoản A không có quyền xem, lập 23 phiếu.', ['Đăng nhập A.', MENU, 'Bấm Xuất Excel.'], '—',
      ['File có đúng 23 phiếu của A.', 'Màn không có chức năng Import.']),
    T('pq_history', 'Xem lịch sử theo phạm vi xem', 'P1', 'Tài khoản A; phiếu 00402 của A.', ['Đăng nhập A.', MENU, DOT3 + ' 00402.'], '—',
      ['Luôn có mục Lịch sử, mở được, không cần quyền riêng.']),
    T('pq_url', 'Dán đường dẫn màn Sửa khi không phải người lập', 'P0', 'Tài khoản C (quyền xem tổng công ty); phiếu nháp... 00114 Từ chối của A.'.replace('nháp... ', ''),
      ['A sao chép đường dẫn màn Sửa phiếu 00114 gửi C.', 'C dán đường dẫn vào thanh địa chỉ.', 'C sửa Diễn giải, bấm Lưu nháp.'], '—',
      ['Màn Sửa có mở nhưng bấm Lưu báo "Bạn không có quyền sửa phiếu này".', 'Phiếu không đổi.']),
    T('pq_api', 'Gọi thẳng chức năng khi thiếu quyền', 'P1', 'Tài khoản A (không có Kế toán thanh toán); phiếu 00401 Chờ tạo phiếu kế toán.',
      ['Dùng công cụ kiểm thử API, đăng nhập A, gọi thẳng chức năng Từ chối phiếu 00401 kèm lý do.'], '—',
      ['Hệ thống từ chối: "Bạn không có quyền từ chối phiếu này".', 'Phiếu giữ Chờ tạo phiếu kế toán.']),
    T('pq_revoke', 'Đổi quyền giữa thao tác', 'P1', PRE_CHO, ['K mở chi tiết 00401.', 'Quản trị gỡ quyền Kế toán thanh toán của K.', 'K bấm Từ chối, nhập lý do, bấm Từ chối.'],
      '—', ['Báo "Bạn không có quyền từ chối phiếu này"; phiếu không đổi.', 'Tải lại trang thì nút Từ chối, Tạo phiếu kế toán biến mất.']),
]

# ================================================================== XII. DUYỆT PHIẾU (Tạo phiếu kế toán)
S12 = [
    T('ap_btn', 'Điều kiện hiển thị nút Tạo phiếu kế toán', 'P0', PRE_CHO + ' ' + PRE_NHAP,
      ['K mở danh sách, xem dòng 00401 và 00402.', 'A mở chi tiết 00401.'], '—',
      ['Chỉ dòng 00401 (Chờ tạo phiếu kế toán) có nút Tạo phiếu kế toán với K.', 'A (người lập) không thấy nút này.',
       'Màn không có nút "Duyệt": duyệt = Tạo phiếu kế toán.']),
    T('ap_popup', 'Giao diện khi bấm Tạo phiếu kế toán', 'P1', PRE_CHO, [MENU_CD, 'Bấm Tạo phiếu kế toán ở dòng 00401.'], '—',
      ['Không có cửa sổ xác nhận: mở thẳng màn "Tạo phiếu kế toán" điền sẵn phiếu 00401.',
       'Xác nhận ghi sổ nằm ở nút "Lưu và duyệt" của màn phiếu kế toán.']),
    T('ap_ok', 'Lưu phiếu kế toán thành công', 'P0', PRE_CHO, [MENU_CD, 'Bấm Tạo phiếu kế toán ở 00401.', 'Nhập Ngày hạch toán, bấm Lưu nháp.'], '—',
      ['Phiếu kế toán lưu thành công.', 'Phiếu yêu cầu 00401 sang "Đã tạo phiếu kế toán", rời màn chờ duyệt.']),
    T('ap_required', 'Dữ liệu bắt buộc trước khi lưu phiếu kế toán', 'P0', PRE_CHO,
      [MENU_CD, 'Bấm Tạo phiếu kế toán ở 00401.', 'Xóa Ngày hạch toán, bấm Lưu nháp.'], 'Ngày hạch toán: trống',
      ['Báo "Bạn chưa nhập đầy đủ thông tin.", ô thiếu đỏ.', 'Phiếu yêu cầu 00401 vẫn Chờ tạo phiếu kế toán.']),
    T('ap_rules', 'Điều kiện nghiệp vụ trước khi tạo phiếu kế toán', 'P1', PRE_CHO + ' K2 Kế toán thanh toán công ty 2.',
      ['K2 mở danh sách chung, tìm 00401.', 'K mở phiếu Đang tạo / Từ chối của người công ty 1.'], '—',
      ['K2 (khác công ty) không có nút Tạo phiếu kế toán.', 'Phiếu không ở trạng thái Chờ tạo phiếu kế toán: không có nút.']),
    T('ap_data', 'Dữ liệu được tạo sau khi lập phiếu kế toán', 'P0', PRE_CHO, ['K Tạo phiếu kế toán từ 00401 và Lưu nháp.', 'Mở chi tiết phiếu kế toán.'], '—',
      ['Phiếu kế toán ghi mã phiếu yêu cầu TPE.DNDCCN1026.00401.', 'Đầu phiếu và các dòng định khoản lấy theo phiếu yêu cầu.']),
    T('ap_related', 'Ảnh hưởng khi duyệt phiếu kế toán', 'P0', 'Phiếu 00401 Đã tạo phiếu kế toán qua PKT-0091 (nháp).',
      ['K mở PKT-0091, bấm Lưu và duyệt, xác nhận.', 'Xem dòng 00401.'], '—',
      ['00401 sang "Đã duyệt phiếu kế toán".', 'Cột Người duyệt = K.']),
    T('ap_notify', 'Thông báo sau khi duyệt', 'P1', 'Như case "Ảnh hưởng khi duyệt phiếu kế toán"; A là người lập 00401.',
      ['K Lưu và duyệt PKT-0091.', 'A mở chuông thông báo.'], '—',
      ['A nhận "[PKT] Đã duyệt: PKT-0091" kèm "Từ đề nghị: TPE.DNDCCN1026.00401", số tiền, người duyệt.',
       'Lưu nháp phiếu kế toán (chưa duyệt) KHÔNG gửi thông báo cho A.']),
    T('ap_notify_link', 'Nội dung và điều hướng từ thông báo', 'P1', 'A vừa nhận thông báo ở case "Thông báo sau khi duyệt"; K vừa nhận "[DCCN] Chờ duyệt".',
      ['A bấm thông báo [PKT].', 'K bấm thông báo [DCCN] Chờ duyệt.'], '—',
      ['A: mở màn chi tiết phiếu kế toán PKT-0091.', 'K: mở màn chi tiết phiếu yêu cầu tương ứng.', 'Mã phiếu trong thông báo in đậm.']),
    T('ap_cancel', 'Hủy thao tác tạo phiếu kế toán', 'P1', PRE_CHO, ['K bấm Tạo phiếu kế toán ở 00401.', 'Bấm Quay lại, không lưu.'], '—',
      ['00401 vẫn Chờ tạo phiếu kế toán, vẫn ở màn chờ duyệt.', 'Lịch sử 00401 không có mốc mới.']),
    T('ap_again', 'Không tạo phiếu kế toán lần hai', 'P0', 'Phiếu 00401 Đã tạo phiếu kế toán.', ['K mở màn chờ duyệt.', 'K mở chi tiết 00401.'], '—',
      ['00401 không còn ở màn chờ duyệt.', 'Chi tiết không còn nút Tạo phiếu kế toán, Từ chối.']),
    T('ap_history', 'Lịch sử khi tạo / duyệt phiếu kế toán', 'P1', 'Như case "Ảnh hưởng khi duyệt phiếu kế toán".', ['Mở Lịch sử 00401.'], '—',
      ['Mốc "Thay đổi trạng thái" Chờ tạo phiếu kế toán sang Đã tạo phiếu kế toán, ghi chú "Phiếu kế toán PKT-0091", người thực hiện K.',
       'Mốc Đã tạo sang Đã duyệt phiếu kế toán, thời điểm duyệt.']),
]

# ================================================================== XIII. KHÔNG DUYỆT PHIẾU (Từ chối)
S13 = [
    T('rj_btn', 'Điều kiện hiển thị nút Từ chối', 'P0', PRE_CHO, ['K mở màn chờ duyệt, xem dòng 00401.', 'K bấm Từ chối ở dòng.', 'A mở chi tiết 00401.'], '—',
      ['K: có nút Từ chối ở dòng; bấm mở màn chi tiết phiếu (không nhập lý do ngay ở dòng).', 'A không có nút Từ chối.']),
    T('rj_popup', 'Giao diện cửa sổ từ chối', 'P1', PRE_CHO, ['K mở chi tiết 00401, bấm Từ chối.'], '—',
      ['Cửa sổ "Từ chối phiếu yêu cầu điều chỉnh công nợ", dòng phụ "Phiếu: TPE.DNDCCN1026.00401".',
       'Ô Lý do từ chối * trống, con trỏ đặt sẵn; nút Từ chối (đỏ), Hủy, dấu (x).']),
    T('rj_ok', 'Từ chối thành công', 'P0', PRE_CHO, ['K mở chi tiết 00401, bấm Từ chối.', 'Nhập lý do, bấm Từ chối.'], 'Lý do: Sai hợp đồng nhận',
      ['Báo "Từ chối phiếu yêu cầu điều chỉnh công nợ thành công", đóng cửa sổ, về danh sách chung.']),
    T('rj_empty', 'Bỏ trống lý do', 'P0', PRE_CHO, ['K bấm Từ chối.', 'Để trống, bấm Từ chối.', 'Nhập 5 khoảng trắng, bấm Từ chối.'], 'Lý do: trống ; 5 khoảng trắng',
      ['Ô đỏ "Vui lòng nhập lý do từ chối", cửa sổ không đóng.', 'Phiếu không đổi.']),
    T('rj_len', 'Giới hạn ký tự lý do', 'P1', PRE_CHO, ['K bấm Từ chối, dán 1001 ký tự, bấm Từ chối.', 'Xóa còn 1000 ký tự, bấm Từ chối.'], 'Lý do: 1001 ; 1000 ký tự',
      ['Bước 1: báo "Vui lòng nhập tối đa 1000 ký tự.", cửa sổ giữ nguyên nội dung.', 'Bước 2: từ chối thành công.']),
    T('rj_status', 'Trạng thái phiếu sau khi từ chối', 'P0', 'K vừa từ chối 00401.', [MENU, 'Tìm 00401.'], '—',
      ['Trạng thái "Từ chối"; Người duyệt = K; Ngày cập nhật = thời điểm từ chối.']),
    T('rj_reason', 'Hiển thị và lưu trữ lý do', 'P1', 'K vừa từ chối 00401 với lý do "Sai hợp đồng nhận".', ['A mở chi tiết 00401.', 'Mở khối Lịch sử.'], '—',
      ['Ô "Ghi chú không duyệt" = "Sai hợp đồng nhận".', 'Mốc từ chối trong lịch sử kèm đúng lý do.']),
    T('rj_related', 'Ảnh hưởng đến dữ liệu liên quan', 'P1', 'K vừa từ chối 00401.', ['K mở màn chờ duyệt.', 'A mở danh sách, xem dòng 00401.', 'A sửa, gửi duyệt lại.'], '—',
      ['00401 rời màn chờ duyệt.', 'A có nút Sửa, Xóa ở dòng 00401.', 'Gửi lại: lý do cũ bị xóa, phiếu quay lại màn chờ duyệt.']),
    T('rj_notify', 'Thông báo sau khi từ chối', 'P0', 'K vừa từ chối 00401 của A.', ['A mở chuông thông báo.', 'Bấm vào thông báo.'], '—',
      ['A nhận "[DCCN] Từ chối: TPE.DNDCCN1026.00401" kèm "Người từ chối: K" và "Lý do: Sai hợp đồng nhận".', 'Bấm mở màn chi tiết 00401.']),
    T('rj_cancel', 'Hủy thao tác từ chối', 'P1', PRE_CHO, ['K bấm Từ chối, nhập lý do, bấm Hủy.', 'Bấm Từ chối lần nữa.'], '—',
      ['Cửa sổ đóng; phiếu vẫn Chờ tạo phiếu kế toán.', 'Mở lại: ô lý do trống.']),
    T('rj_again', 'Không từ chối phiếu đã xử lý', 'P0', PRE_CHO + ' K3 cũng là Kế toán thanh toán công ty 1.',
      ['K và K3 cùng mở chi tiết 00401.', 'K từ chối thành công.', 'K3 bấm Từ chối, nhập lý do, bấm Từ chối.'], '—',
      ['K3 báo "Không thể chuyển phiếu từ trạng thái hiện tại sang trạng thái này".', 'Cửa sổ giữ nguyên lý do vừa nhập; phiếu giữ kết quả của K.']),
    T('rj_history', 'Lịch sử khi từ chối', 'P1', 'K vừa từ chối 00401.', ['Mở Lịch sử 00401.'], '—',
      ['Mốc "Thay đổi trạng thái" Chờ tạo phiếu kế toán sang Từ chối, người thực hiện K, thời điểm từ chối, kèm lý do.']),
]

# ================================================================== XIV. IN PHIẾU
S14 = [
    T('pr_list', 'In phiếu từ danh sách', 'P1', PRE_CHO, [MENU, DOT3 + ' 00401, chọn In phiếu.', 'Bấm In.'], '—',
      ['Cửa sổ "Xem trước phiếu TPE.DNDCCN1026.00401" ngay trên danh sách, không mở tab mới.',
       'Tiêu đề "PHIẾU YÊU CẦU ĐIỀU CHỈNH CÔNG NỢ", bảng từ / đến, khối chữ ký.', 'Bấm In mở hộp thoại in của trình duyệt.']),
    T('pr_detail', 'In phiếu từ màn chi tiết', 'P2', PRE_CHO, [MENU, 'Mở chi tiết 00401, bấm In phiếu.'], '—',
      ['Cùng bản xem trước như khi in từ danh sách.']),
    T('pr_letterhead', 'Letterhead theo công ty của phiếu', 'P1', 'Phiếu 00401 của công ty 1; tài khoản DNS Admin thuộc công ty 2.',
      ['DNS Admin in phiếu 00401.'], '—', ['Đầu bản in là logo / letterhead của công ty 1 (công ty ghi trên phiếu), không phải công ty 2.']),
    T('pr_foreign', 'In phiếu NCC ngoại tệ', 'P2', 'Phiếu 00371 loại nhà cung cấp, USD.', ['In phiếu 00371.'], '—',
      ['Bản in khổ ngang, đủ cột nguyên tệ và VNĐ, số ngoại tệ 2 số lẻ, không tràn lề.']),
    T('pr_close', 'Đóng cửa sổ xem trước', 'P2', 'Đang mở bản xem trước 00401 ở trang 3 danh sách.', ['Bấm dấu (x).'], '—',
      ['Cửa sổ đóng, danh sách giữ nguyên trang 3.']),
]

# ================================================================== XV. GỬI DUYỆT TỪ CHI TIẾT, LUỒNG TỔNG THỂ (3 case fc_* chuyển sang II)
S15 = [
    T('fc_open', 'Cài đặt bộ lọc: ẩn ô và khôi phục', 'P2', PRE_LIST,
      [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Số tiền, bấm Lưu.', 'Mở lại, bấm Khôi phục mặc định, Lưu.'], '—',
      ['Bước 2: khối nâng cao không còn ô Số tiền.', 'Bước 3: đủ 11 ô lọc theo thứ tự ban đầu.']),
    T('fc_hide_value', 'Cài đặt bộ lọc: ẩn ô lọc đang có giá trị', 'P2', 'Đang lọc Số tiền từ 1,000,000.', ['Cài đặt bộ lọc, bỏ tích Số tiền, Lưu.'], '—',
      ['Giá trị Số tiền bị xóa, danh sách nạp lại không còn lọc theo tiền.']),
    T('fc_drag', 'Cài đặt bộ lọc: kéo đổi thứ tự, đóng không lưu', 'P2', PRE_LIST,
      [MENU, 'Cài đặt bộ lọc, kéo Trạng thái lên đầu, Lưu.', 'Mở lại, bỏ tích Người tạo, bấm Đóng.'], '—',
      ['Bước 2: ô Trạng thái đứng đầu khối nâng cao.', 'Bước 3: ô Người tạo vẫn còn (đóng không lưu).']),
    T('sd_ok', 'Gửi duyệt từ màn chi tiết', 'P0', PRE_NHAP, ['Mở chi tiết 00402, bấm Gửi duyệt.'], '—',
      ['Báo "Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công"; màn tải lại, phiếu Chờ tạo phiếu kế toán, nút đổi theo.']),
    T('sd_missing', 'Gửi duyệt từ chi tiết khi thiếu hợp đồng bên đến', 'P0', 'Phiếu nháp 00406 của A thiếu hợp đồng bên "đến".',
      ['Mở chi tiết 00406, bấm Gửi duyệt.'], '—',
      ['Báo "Dòng 1 có dòng "Điều chỉnh đến" chưa chọn hợp đồng/đơn hàng"; phiếu giữ Đang tạo.'.replace('"Điều chỉnh đến"', '\'Điều chỉnh đến\'')]),
    T('sd_from_sc', 'Gửi duyệt phiếu nháp lưu bằng Lưu và tiếp tục', 'P1', 'Phiếu nháp ở case "Lưu và tiếp tục khi dữ liệu còn thiếu".',
      ['Mở chi tiết phiếu nháp.', 'Bấm Gửi duyệt.'], '—',
      ['Báo lỗi đầu tiên còn thiếu (vd "Vui lòng nhập diễn giải trước khi gửi duyệt"); phiếu giữ Đang tạo.']),
    T('sd_twice', 'Gửi duyệt phiếu đã được gửi ở tab khác', 'P2', PRE_NHAP, ['Tab 1, tab 2 mở chi tiết 00402.', 'Tab 1 bấm Gửi duyệt.', 'Tab 2 bấm Gửi duyệt.'], '—',
      ['Tab 2 báo "Không thể chuyển phiếu từ trạng thái hiện tại sang trạng thái này".']),
    T('e2e_ok', 'Luồng lập, gửi, tạo phiếu kế toán', 'P0', 'A người lập; K kế toán cùng công ty.',
      ['A lập phiếu, Gửi duyệt.', 'K mở màn chờ duyệt, Tạo phiếu kế toán, Lưu.', 'K Lưu và duyệt phiếu kế toán.'], '—',
      ['Bước 1: K nhận thông báo; phiếu có trong màn chờ duyệt.', 'Bước 2: phiếu rời màn chờ duyệt, Đã tạo phiếu kế toán.',
       'Bước 3: phiếu Đã duyệt phiếu kế toán, A nhận thông báo [PKT] Đã duyệt.']),
    T('e2e_reject', 'Luồng từ chối, sửa, gửi lại', 'P0', 'A người lập; K kế toán cùng công ty.', ['A gửi phiếu.', 'K từ chối.', 'A sửa, gửi lại.'], '—',
      ['Lịch sử đủ mốc theo thứ tự; phiếu quay lại màn chờ duyệt.']),
]

# user 02/11/2026: chỉ 1 nhóm Phân quyền (khối đầu file vào XI) và Cài đặt bộ lọc thuộc nhóm Tìm kiếm và lọc.
S11[:0] = [T.of(('ROLE', tc[0]), tc) for tc in ROLE_TCS]
S2 += [t for t in S15 if t.key.startswith('fc_')]
S15[:] = [t for t in S15 if not t.key.startswith('fc_')]

SECTIONS_KEYED = [
    ('HIỂN THỊ DANH SÁCH VÀ TRUY CẬP', S1),
    ('TÌM KIẾM VÀ LỌC', S2),
    ('THÊM MỚI', S3),
    ('CHỈNH SỬA', S4),
    ('XÓA', S5),
    ('LỊCH SỬ THAY ĐỔI', S6),
    ('XEM CHI TIẾT', S7),
    ('TÙY CHỈNH CỘT', S8),
    ('XUẤT EXCEL', S9),
    ('ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU', S10),
    ('PHÂN QUYỀN', S11),
    ('DUYỆT PHIẾU (TẠO PHIẾU KẾ TOÁN)', S12),
    ('KHÔNG DUYỆT PHIẾU (TỪ CHỐI)', S13),
    ('IN PHIẾU', S14),
    ('GỬI DUYỆT TỪ MÀN CHI TIẾT VÀ LUỒNG TỔNG THỂ', S15),
]

# Case nghiệp vụ cốt lõi nâng lên P0 (luật chặn gửi duyệt, đồng bộ trạng thái, phân quyền thao tác, dữ liệu xuất)
PROMOTE_P0 = {
    'pg_total', 'pg_reset_filter', 'flt_party', 'flt_money', 'flt_date', 'flt_reset', 'add_rate', 'add_spaces',
    'add_split', 'add_change_type', 'add_foreign', 'sc_format', 'ed_many', 'ed_updated', 'ed_overlimit', 'ed_exit',
    'del_changed', 'his_edit_many', 'his_multi', 'his_status', 'dt_reject_note', 'xl_pages', 'xl_types', 'xl_pending',
    'ef_edit_link', 'ef_delete_sync', 'ef_filter', 'ef_orphan', 'pq_api', 'pq_revoke', 'ap_history', 'rj_reason',
    'rj_related', 'rj_history', 'rj_len', 'sd_from_sc',
}
for _title, _cases in SECTIONS_KEYED:
    for _t in _cases:
        if _t.key in PROMOTE_P0:
            _t.prio = 'P0'
assert PROMOTE_P0 <= {t.key for _x, cs in SECTIONS_KEYED for t in cs}, 'Khóa PROMOTE_P0 không tồn tại'

# Đánh số + bảng tra khóa -> mã TC (gen_checklist.py dùng)
ID = {}
SECTIONS = []
for idx, (title, cases) in enumerate(SECTIONS_KEYED):
    roman = ROMAN[idx]
    rows = []
    for n, t in enumerate(cases, 1):
        assert t.key not in ID, 'Trùng khóa case: %s' % t.key
        ID[t.key] = 'TC_%02d.%03d' % (idx + 1, n)
        rows.append(('%03d' % n, t.func, t.prio, t.pre, t.steps, t.td, t.exp))
    SECTIONS.append((roman, title, rows))
check_no_dash_pre(SECTIONS, [])


def role(suffix):
    return ID[('ROLE', suffix)]


if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name='Phiếu yêu cầu điều chỉnh công nợ - Cập nhật ngày %s' % NGAY,
          module_name='YC điều chỉnh công nợ', description_block=DESCRIPTION_BLOCK, role_tcs=[], sections=SECTIONS)
