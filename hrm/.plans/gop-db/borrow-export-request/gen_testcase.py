# -*- coding: utf-8 -*-
"""Testcase màn "Yêu cầu xuất hàng mượn" (PYCXHM) — skill testcase-documenter (tc_engine).

Chạy: python gen_testcase.py -> testcase.xlsx
Lịch sử:
  30/10/2026  bản theo chuẩn mẫu Danh mục quốc gia + 8 ý góp ý tester 07/10 (100 TC).
  02/11/2026  xuất lại theo checklist "Mẫu tài liệu.xlsx" của tester: sắp section đúng thứ tự + tên nhóm checklist
              (I..XIII), rồi phần riêng của màn (XIV In, XV Cài đặt bộ lọc); mỗi dòng checklist áp dụng được có >= 1 TC.
              Mỗi TC có KHÓA (cột đầu tuple) -> số TC tự đánh theo thứ tự trong section; gen_checklist.py tra mã TC qua
              bảng ID[khóa] nên chèn / bớt TC không làm lệch file đối chiếu.
Nguồn: code nhánh develop cả 2 repo (đọc lại 02/11/2026) — hrm-client pages/finance/borrow-export-requests/**,
  pages/finance/borrow-exports/components/BorrowExportForm.vue, components dùng chung (V2BaseDataTable,
  V2BaseSmartFilterPanel, filterStateMixin, unsavedChangesMixin, export-fields-modal, SystemInfoSection,
  V2BaseCurrencyInput, plugins/axios); hrm-api Modules/Finance (BorrowExportRequest entity / service / controller /
  request, BorrowExportService, NotifyService, HistoryService) + app/Services/CatalogHistoryService.
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
from tc_engine import build  # noqa: E402
from tc_phieu_bosung import (ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases,  # noqa: E402
                             weird_param_case, check_no_dash_pre)

OUT = os.path.join(HERE, 'testcase.xlsx')
NGAY = '02/11/2026'
MENU_SALE = 'Vào phân hệ Bán hàng > nhóm "Yêu cầu" > "Hàng hóa" > bấm "YC xuất hàng mượn".'
MENU_KT = ('Vào phân hệ Tài chính > nhóm "Hàng hoá - Dịch vụ - Vận chuyển" > "Mượn hàng" > bấm '
           '"Yêu cầu xuất hàng mượn".')
TAO = [MENU_SALE, 'Bấm "Tạo mới".']
ADV = 'Bấm "Tìm kiếm nâng cao".'

# Bộ dữ liệu mẫu dùng xuyên suốt (tài khoản D: quyền Xem phiếu hàng mượn theo công ty)
PRE_LIST = ('Tài khoản D có quyền Xem phiếu hàng mượn theo công ty.\n'
            'Trong phạm vi có 364 phiếu: 138 Chờ duyệt, 215 Đã duyệt, 11 Không duyệt (37 trang, 10 dòng / trang).')
PRE_A = ('Tài khoản A (không có quyền nào) đã lập phiếu xuất mượn PYCXH-TEST-023 đang Đã mượn: hàng ENEO-408-V5041 '
         'đã xuất 46, chưa trả, Đơn giá 60,500.')
PRE_FORM_OK = (PRE_A + '\nTrên máy có file chungtu.pdf (2 MB).')
PRE_KT = 'Tài khoản B có quyền Kế toán kho (cùng công ty với A).'


def _lines(v, bullet=False):
    if isinstance(v, (list, tuple)):
        if bullet:
            return '\n'.join(x if x.startswith('-') else '- ' + x for x in v)
        return '\n'.join(v)
    return v


def _steps(v):
    if isinstance(v, (list, tuple)):
        return '\n'.join('%d. %s' % (i + 1, x) for i, x in enumerate(v))
    return v


def T(key, func, prio, pre, steps, td, exp):
    """1 testcase: (khóa, chức năng, priority, tiền điều kiện, bước, test data, expected)."""
    return (key, func, prio, _lines(pre), _steps(steps), _lines(td), _lines(exp, bullet=True))


def K(key, case):
    """Gắn khóa cho case dựng sẵn từ tc_phieu_bosung (tuple 7 phần tử, phần tử đầu là số cũ)."""
    return (key,) + tuple(case[1:])


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn Yêu cầu xuất hàng mượn (mã phiếu PYCXHM) dùng để người đang mượn hàng gom các phiếu xuất mượn của '
     'mình vào 1 phiếu, chọn phần hàng KHÔNG trả lại mà xuất hẳn, gửi Kế toán kho duyệt.\n'
     'Phiếu gửi đi vào thẳng trạng thái Chờ duyệt (không có Lưu nháp, không Sửa, không Xóa, không Khóa / Mở khóa, '
     'không Import).\n'
     'Kế toán kho duyệt bằng cách lập Phiếu xuất hàng mượn từ phiếu này, hoặc Từ chối kèm lý do.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Trạng thái hiển thị: Chờ duyệt (nhãn cam), Đã duyệt (nhãn xanh lá), Không duyệt (nhãn đỏ).\n'
     '- Lối vào Bán hàng: phiếu trong phạm vi quyền xem theo cấp, cộng phiếu mình lập; Kế toán kho thấy mọi '
     'phiếu đã gửi.\n'
     '- Lối vào Tài chính (Kế toán kho): mọi phiếu đã gửi, chỉ người có quyền Kế toán kho thấy dữ liệu.\n'
     '- Popup Chọn phiếu xuất mượn: chỉ phiếu yêu cầu xuất hàng loại Xuất mượn do chính mình lập, đang Đã mượn.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu trạng thái Đang tạo (dữ liệu cũ) của người khác: không bao giờ hiện.\n'
     '- Ô lọc Trạng thái không có lựa chọn Đang tạo.\n'
     '- Hàng hóa không có trên phiếu mượn nào đã chọn: dòng bị khóa, không được gửi đi.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Ngày tạo lọc theo ngày lập phiếu, lấy trọn 2 đầu mút (từ 00:00 ngày đầu tới hết ngày cuối).'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Phiếu > dòng hàng hóa > dòng con theo từng phiếu mượn có hàng đó (cột Phiếu mượn, Đang mượn, Xuất).\n'
     'Số lượng xuất của dòng hàng = tổng Xuất các dòng con.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Mỗi phiếu mượn chỉ chọn được 1 lần trong cùng phiếu.\n'
     '- Cùng 1 hàng hóa chỉ thêm 1 dòng (popup chọn hàng báo trùng).\n'
     '- Phiếu không có trường duy nhất ngoài mã tự sinh: 2 phiếu cùng nội dung vẫn lưu được, mã khác nhau.\n'
     '- Đang mượn = đã xuất - đã trả - phần đang chờ ở các phiếu khác chưa duyệt (trả hàng, xuất bán hàng mượn, '
     'xuất hàng mượn), quy theo hệ số đơn vị tính, làm tròn xuống.'),
    ('7. Phân quyền cấp',
     '- Kế toán kho: duyệt (Tạo phiếu xuất hàng mượn), Từ chối, xem mọi phiếu đã gửi.\n'
     '- Xem phiếu hàng mượn theo tổng công ty: mọi phiếu.\n'
     '- Xem phiếu hàng mượn theo công ty: phiếu cùng công ty + phiếu mình lập.\n'
     '- Xem phiếu hàng mượn theo phòng ban: phiếu phòng ban mình quản lý + phiếu mình lập.\n'
     '- Không có quyền nào: chỉ phiếu mình lập. Lập phiếu, in, xuất Excel, xem lịch sử không cần quyền riêng.'),
    ('8. Cách tính các ô thống kê',
     '- Ô "Hiển thị a–b / N": a, b là dòng đầu – cuối của trang, N là tổng phiếu khớp bộ lọc trong phạm vi quyền.\n'
     '- Thành tiền = Số lượng xuất × Đơn giá (theo đơn vị tính đang chọn).\n'
     '- Dòng Tổng cộng = tổng Số lượng xuất và tổng Thành tiền của các dòng.'),
    ('9. Ghi chú đọc bảng',
     '- Số hiển thị dạng 1,234,567 (dấu phẩy ngăn hàng nghìn).\n'
     '- Lưu ý: ô Xuất chỉ nhận chữ số (chữ cái, dấu trừ, dấu chấm bị bỏ); vượt Đang mượn thì báo đỏ, KHÔNG tự kéo số về '
     '(trừ khi đổi đơn vị tính).\n'
     '- Lưu ý: phiếu gửi đi là không sửa được; muốn đổi phải chờ Từ chối rồi lập phiếu mới.\n'
     '- Lưu ý: bộ lọc chỉ được ghi nhớ khi đi vào màn chi tiết phiếu (10 phút); quay lại danh sách luôn về trang 1.\n'
     '- Lưu ý: tài khoản kiểm thử cần có sẵn phiếu xuất mượn Đã mượn do chính mình lập thì mới lập phiếu được.\n'
     '- Các case dùng công cụ kiểm thử API (TC_11.010, TC_11.011) dành cho tester kỹ thuật.'),
]

ROLE_TCS = [
    ('00', 'Tài khoản không có quyền nào chỉ thấy phiếu mình lập', 'P0',
     'Tài khoản A không có quyền Kế toán kho và không có quyền xem theo cấp.\nA đã lập 3 phiếu; công ty có 300 phiếu.',
     '1. Đăng nhập bằng A.\n2. ' + MENU_SALE, '—',
     '- Màn mở được, không báo lỗi quyền.\n- Tổng số = 3, chỉ phiếu A lập.\n- Không thấy nút Duyệt trên dòng.'),
    ('01', 'Quyền Kế toán kho thấy mọi phiếu đã gửi', 'P0',
     'Tài khoản B có quyền Kế toán kho; hệ thống có 300 phiếu đã gửi ở 2 công ty.',
     '1. Đăng nhập bằng B.\n2. ' + MENU_KT, '—',
     '- Tiêu đề "Yêu cầu xuất hàng mượn (Kế toán kho)".\n- Tổng số = 300.\n- Phiếu Chờ duyệt có nút Duyệt ở cột Hành động.'),
    ('02', 'Không có quyền Kế toán kho mở lối vào Kế toán kho', 'P0',
     'Tài khoản A như TC_11.001.', '1. Đăng nhập bằng A.\n2. ' + MENU_KT, '—',
     '- Bảng hiện "Không có dữ liệu phù hợp.".\n- Không lộ phiếu của người khác.'),
    ('03', 'Quyền Xem phiếu hàng mượn theo tổng công ty', 'P1',
     'Tài khoản C có quyền theo tổng công ty; công ty 1 có 200 phiếu, công ty 2 có 100 phiếu.',
     '1. Đăng nhập bằng C.\n2. ' + MENU_SALE, '—',
     '- Tổng số = 300.\n- Bộ lọc nâng cao có ô Công ty và Phòng ban.'),
    ('04', 'Quyền Xem phiếu hàng mượn theo công ty', 'P1',
     'Tài khoản D thuộc công ty 1, có quyền theo công ty; D lập 2 phiếu ở công ty 2 (điều chuyển).',
     '1. Đăng nhập bằng D.\n2. ' + MENU_SALE, '—',
     '- Tổng số = 200 phiếu công ty 1 + 2 phiếu D lập.\n- Bộ lọc không có ô Công ty, có ô Phòng ban.'),
    ('05', 'Quyền Xem phiếu hàng mượn theo phòng ban', 'P1',
     'Tài khoản E quản lý phòng Kinh doanh (40 phiếu).', '1. Đăng nhập bằng E.\n2. ' + MENU_SALE, '—',
     '- Tổng số = 40 + phiếu E tự lập.\n- Mở chi tiết 1 phiếu của phòng Kinh doanh được.'),
    ('06', 'Mở chi tiết phiếu ngoài phạm vi', 'P0',
     'Tài khoản A như TC_11.001; phiếu PYCXHM-00300 của người khác, khác phòng ban.',
     '1. Đăng nhập bằng A.\n2. Mở thông báo / đường link chi tiết phiếu PYCXHM-00300 do người khác gửi.', '—',
     '- Hệ thống báo "Bạn không có quyền xem phiếu này".\n- Quay về màn danh sách, không hiện nội dung phiếu.'),
    ('07', 'Người không có quyền Kế toán kho không thấy nút duyệt / từ chối', 'P0',
     'Tài khoản A lập phiếu PYCXHM-00301 đang Chờ duyệt.', '1. Đăng nhập bằng A.\n2. Mở chi tiết PYCXHM-00301.', '—',
     '- Chỉ có nút In, Quay lại.\n- KHÔNG có nút Tạo phiếu xuất hàng mượn và Từ chối.'),
    ('08', 'Kế toán kho với phiếu đã xử lý', 'P1',
     'Tài khoản B (Kế toán kho); phiếu PYCXHM-00290 Đã duyệt, PYCXHM-00291 Không duyệt.',
     '1. Đăng nhập bằng B.\n2. Mở chi tiết lần lượt 2 phiếu.', '—',
     '- Cả 2 phiếu không có nút Tạo phiếu xuất hàng mượn và Từ chối.\n- Ở danh sách, 2 phiếu này không có nút Duyệt.'),
    ('09', 'Gọi thẳng chức năng Từ chối khi không có quyền Kế toán kho', 'P0',
     'Tài khoản A (không có quyền Kế toán kho); phiếu PYCXHM-00301 của A đang Chờ duyệt.',
     '1. Đăng nhập bằng A.\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Từ chối phiếu PYCXHM-00301, bỏ qua giao diện, '
     'kèm lý do "Thử".', 'Lý do: Thử',
     '- Hệ thống từ chối, trả câu "Phiếu không còn ở trạng thái Chờ duyệt hoặc bạn không đủ quyền.".\n'
     '- Mở lại phiếu: vẫn Chờ duyệt, không có Lý do từ chối, lịch sử không thêm mốc.'),
    ('10', 'Gọi thẳng chức năng xem / in phiếu ngoài phạm vi', 'P1',
     'Tài khoản A như TC_11.001; phiếu PYCXHM-00300 của người khác, khác phòng ban.',
     '1. Đăng nhập bằng A.\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng xem chi tiết và chức năng in phiếu '
     'PYCXHM-00300, bỏ qua giao diện.', '—',
     '- Cả 2 chức năng đều từ chối với câu "Bạn không có quyền xem phiếu này".\n- Không trả nội dung phiếu.'),
]


SCREEN = ListScreen(menu=MENU_SALE, title='Yêu cầu xuất hàng mượn', total=364, quick_label='mã phiếu',
                    quick_sample='0036', quick_hit='8 phiếu PYCXHM-00360 đến PYCXHM-00367',
                    filters=[('Trạng thái', 'Đã duyệt'), ('Người duyệt', 'Cao Thị Thùy Linh')])
ORG = org_cases(SCREEN, 1)
MEM = filter_memory_cases(SCREEN, 1)
COMBO = combo_cases(SCREEN, 1)

# ====================================================================== I. HIỂN THỊ DANH SÁCH VÀ TRUY CẬP
S_LIST = [
    K('l_open', open_menu_case(SCREEN, pre=PRE_LIST,
                               extra=['- Thấy phiếu cùng công ty và phiếu D tự lập; không có thông báo lỗi.'])),
    T('l_open_kt', 'Mở màn từ phân hệ Tài chính (lối vào Kế toán kho)', 'P0',
      PRE_KT + '\nHệ thống có 364 phiếu đã gửi (Chờ duyệt, Đã duyệt, Không duyệt).',
      ['Đăng nhập bằng B.', MENU_KT], '—',
      ['Tiêu đề bảng và tab trình duyệt "Yêu cầu xuất hàng mượn (Kế toán kho)".',
       'Có đủ các phiếu Chờ duyệt, Đã duyệt, Không duyệt; dòng "Hiển thị 1–10 / 364".']),
    T('l_buttons', 'Các nút chức năng được hiển thị', 'P0', PRE_LIST + '\nTài khoản D không có quyền Kế toán kho.',
      ['Đăng nhập bằng D.', MENU_SALE, 'Quan sát khối lọc, thanh nút trên bảng và cột Hành động.'], '—',
      ['Khối "Bộ lọc danh sách": ô tìm nhanh (gợi ý "Tìm kiếm theo mã phiếu"), nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, '
       'Cài đặt bộ lọc.',
       'Trên bảng theo thứ tự: Tạo mới, In, Xuất Excel, nút Cấu hình cột hiển thị (biểu tượng cột).',
       'Cột Hành động mỗi dòng có nút In và Lịch sử; KHÔNG có nút Duyệt (D không phải Kế toán kho).',
       'KHÔNG có nút Sửa, Xóa, Khóa / Mở khóa, Import ở bất kỳ đâu.',
       'Rê chuột lên mỗi nút đều hiện chú thích (vd Tạo mới: "Tạo phiếu yêu cầu xuất hàng mượn mới").']),
    T('l_cols', 'Các cột mặc định hiển thị và mặc định ẩn', 'P0',
      PRE_LIST + '\nTài khoản D chưa từng tùy chỉnh cột.', ['Đăng nhập bằng D.', MENU_SALE], '—',
      ['Hiện theo thứ tự: STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Hành động.',
       'Ẩn: Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối (bật lại được ở Tùy chỉnh cột).']),
    T('l_data', 'Dữ liệu dòng đúng với phiếu đã tạo', 'P0',
      ['Phiếu PYCXHM-00301 do Nguyễn Văn A (phòng MT_KD) gửi lúc 21/10/2026 07:47, đang Chờ duyệt.',
       'Phiếu PYCXHM-00290 do Cao Thị Thùy Linh duyệt lúc 22/10/2026 09:15.'],
      [MENU_SALE, 'Quan sát dòng PYCXHM-00301 và PYCXHM-00290.'], '—',
      ['PYCXHM-00301: Người tạo "Nguyễn Văn A - MT_KD"; Ngày tạo "21/10/2026 07:47"; Trạng thái Chờ duyệt; Người duyệt và '
       'Ngày duyệt để trống.',
       'PYCXHM-00290: Người duyệt "Cao Thị Thùy Linh"; Ngày duyệt "22/10/2026 09:15".',
       'Mã phiếu là liên kết gạch chân.']),
    T('l_status', 'Trạng thái bản ghi: chữ và màu nhãn', 'P1', 'Có phiếu ở đủ 3 trạng thái Chờ duyệt, Đã duyệt, Không duyệt.',
      [MENU_KT, 'Quan sát cột Trạng thái.'], '—',
      ['Chờ duyệt: nhãn cam.', 'Đã duyệt: nhãn xanh lá.', 'Không duyệt: nhãn đỏ.',
       'Không có phiếu nào mang trạng thái Đang tạo của người khác.']),
    T('l_empty', 'Danh sách chưa có dữ liệu', 'P2', 'Tài khoản F mới, chưa lập phiếu nào, không có quyền nào.',
      ['Đăng nhập bằng F.', MENU_SALE], '—',
      ['Trong bảng hiện "Không có dữ liệu phù hợp.".', 'Dưới bảng hiện "Không có phiếu nào." thay cho dòng "Hiển thị".',
       'Các nút Tạo mới, In, Xuất Excel vẫn hiện.']),
    T('l_nomatch', 'Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST,
      [MENU_SALE, ADV, 'Nhập Mã phiếu = "ZZZ999".'], 'Mã phiếu: ZZZ999',
      ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Dưới bảng hiện "Không có phiếu nào.".',
       'Bấm Làm mới: danh sách hiện lại đủ 364 phiếu.']),
    T('l_code_link', 'Bấm mã phiếu mở chi tiết', 'P0', 'Có phiếu PYCXHM-00301.', [MENU_SALE, 'Bấm mã PYCXHM-00301.'], '—',
      ['Mở màn "Chi tiết yêu cầu xuất hàng mượn: PYCXHM-00301".',
       'Chuột phải vào mã chọn mở tab mới: chi tiết mở ở tab mới.']),
    T('l_switch', 'Chuyển qua lại giữa 2 lối vào', 'P1', PRE_KT + '\nĐang ở lối vào Bán hàng, lọc Trạng thái = Đã duyệt.',
      [MENU_SALE, ADV, 'Chọn Trạng thái = Đã duyệt.', MENU_KT, 'Quan sát tiêu đề và danh sách.'], 'Trạng thái: Đã duyệt',
      ['Bước 4: tiêu đề đổi thành "Yêu cầu xuất hàng mượn (Kế toán kho)".',
       'Danh sách nạp lại theo phạm vi Kế toán kho, từ trang 1.']),
    K('l_weird', weird_param_case('0', SCREEN, 'tiêu đề "Yêu cầu xuất hàng mượn"')),
    T('l_pagesize', 'Thay đổi số dòng / trang và về trang 1', 'P0', PRE_LIST + '\nĐang xem trang 3.',
      [MENU_SALE, 'Bấm trang 3.', 'Chọn Số dòng/trang = 50.'], 'Số dòng/trang: 50',
      ['Bảng hiện 50 dòng, về trang 1.', 'Dòng tổng "Hiển thị 1–50 / 364"; thanh phân trang còn 8 trang.',
       'Chọn lại 5: hiện 5 dòng, "Hiển thị 1–5 / 364".']),
    T('l_next', 'Trang trước / trang tiếp theo', 'P1', PRE_LIST, [MENU_SALE, 'Bấm nút trang tiếp (›).', 'Bấm nút trang trước (‹).'],
      '—', ['Bước 2: sang trang 2, "Hiển thị 11–20 / 364".', 'Bước 3: về trang 1, "Hiển thị 1–10 / 364".']),
    T('l_firstlast', 'Trang đầu / trang cuối và trạng thái nút', 'P1', PRE_LIST,
      [MENU_SALE, 'Quan sát nút « và ‹ ở trang 1.', 'Bấm nút về trang cuối (»).', 'Quan sát nút › và ».', 'Bấm nút về trang đầu («).'],
      '—', ['Bước 2: nút « và ‹ mờ, bấm không có tác dụng.', 'Bước 3: sang trang 37, "Hiển thị 361–364 / 364", bảng có 4 dòng.',
            'Bước 4: nút › và » mờ, bấm không có tác dụng.', 'Bước 5: về trang 1.']),
    T('l_stt', 'STT liên tục giữa các trang', 'P1', PRE_LIST, [MENU_SALE, 'Bấm trang 3.'], '—',
      ['"Hiển thị 21–30 / 364"; STT dòng đầu là 21, dòng cuối là 30.']),
    T('l_total', 'Tổng số bản ghi khớp phạm vi', 'P0',
      'Tài khoản D có quyền Xem phiếu hàng mượn theo công ty; công ty của D có 362 phiếu; D tự lập thêm 2 phiếu ở công '
      'ty khác (trước khi điều chuyển).',
      ['Đăng nhập bằng D.', MENU_SALE, 'Đọc dòng tổng dưới bảng.'], '—',
      ['N ở dòng "Hiển thị a–b / N" bằng 362 + 2 = 364 (phiếu công ty mình + phiếu tự lập ở công ty khác).',
       'Lưu ý: N không có dấu phẩy ngăn hàng nghìn (lỗi chung đã ghi nhận).']),
    T('l_page1_filter', 'Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST + '\nĐang xem trang 3.',
      [MENU_SALE, 'Bấm trang 3.', ADV, 'Chọn Trạng thái = Chờ duyệt.'], 'Trạng thái: Chờ duyệt',
      ['Danh sách nạp lại ngay, về trang 1: "Hiển thị 1–10 / 138".']),
    T('l_sort_default', 'Thứ tự sắp xếp mặc định', 'P1', PRE_LIST + '\nPhiếu mới nhất PYCXHM-00367 tạo 01/11/2026 16:20.',
      [MENU_SALE, 'Quan sát 3 dòng đầu và cột Ngày tạo.'], '—',
      ['Dòng đầu là PYCXHM-00367; Ngày tạo giảm dần từ trên xuống.', 'Chưa cột nào có mũi tên sắp xếp được tô đậm.']),
    T('l_sort_code', 'Sắp xếp tăng dần / giảm dần theo Mã phiếu', 'P0', PRE_LIST,
      [MENU_SALE, 'Bấm tiêu đề cột Mã phiếu.', 'Bấm tiêu đề cột Mã phiếu lần nữa.'], '—',
      ['Bước 2: mũi tên lên, dòng đầu là mã nhỏ nhất (PYCXHM-00001).', 'Bước 3: mũi tên xuống, dòng đầu là PYCXHM-00367.',
       'Bấm lần 3 quay lại tăng dần (không có trạng thái bỏ sắp xếp; muốn bỏ thì bấm Làm mới).']),
    T('l_sort_date', 'Sắp xếp theo Ngày tạo / Ngày duyệt', 'P1', PRE_LIST,
      [MENU_SALE, 'Bấm tiêu đề cột Ngày tạo.', 'Bấm tiêu đề cột Ngày duyệt hai lần.'], '—',
      ['Bước 2: phiếu cũ nhất lên đầu.', 'Bước 3: lần 1 tăng dần theo ngày duyệt, lần 2 giảm dần (phiếu duyệt gần nhất lên đầu).',
       'Cột Ngày cập nhật (khi bật hiển thị) không có mũi tên sắp xếp.']),
    T('l_sort_none', 'Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
      [MENU_SALE, 'Bấm tiêu đề các cột Người tạo, Trạng thái, Người duyệt, Hành động.'], '—',
      ['Các cột này không có mũi tên sắp xếp.', 'Bấm tiêu đề không làm đổi thứ tự dòng.']),
    T('l_sort_keep', 'Giữ sắp xếp khi chuyển trang', 'P0', PRE_LIST,
      [MENU_SALE, 'Bấm tiêu đề cột Mã phiếu (tăng dần).', 'Bấm trang 2.'], '—',
      ['Trang 2 tiếp tục thứ tự tăng dần (PYCXHM-00011 đến PYCXHM-00020); mũi tên vẫn ở cột Mã phiếu; STT 11–20.']),
    T('l_sort_page1', 'Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST + '\nĐang xem trang 3.',
      [MENU_SALE, 'Bấm trang 3.', 'Bấm tiêu đề cột Ngày duyệt.'], '—',
      ['Danh sách về trang 1, "Hiển thị 1–10 / 364", sắp theo Ngày duyệt; bộ lọc giữ nguyên.']),
]

# ====================================================================== II. TÌM KIẾM VÀ LỌC
S_SEARCH = [
    T('s_exact', 'Tìm nhanh với mã phiếu chính xác', 'P0', PRE_LIST,
      [MENU_SALE, 'Nhập "PYCXHM-00301" vào ô tìm nhanh.', 'Bấm Tìm kiếm.'], 'Ô tìm nhanh: PYCXHM-00301',
      ['Chỉ còn PYCXHM-00301.', 'Dòng tổng "Hiển thị 1–1 / 1".']),
    T('s_partial', 'Tìm nhanh với một phần mã phiếu', 'P0', PRE_LIST + '\nCó 8 phiếu PYCXHM-00360 đến PYCXHM-00367.',
      [MENU_SALE, 'Nhập "0036" vào ô tìm nhanh.', 'Bấm Tìm kiếm.'], 'Ô tìm nhanh: 0036',
      ['Còn đúng 8 phiếu PYCXHM-00360 đến PYCXHM-00367.', 'Ô tìm theo một phần mã, ở bất kỳ vị trí nào trong mã.']),
    T('s_case', 'Không phân biệt chữ hoa / thường', 'P1', PRE_LIST,
      [MENU_SALE, 'Nhập "pycxhm-00301" (chữ thường) vào ô tìm nhanh.', 'Bấm Tìm kiếm.'], 'Ô tìm nhanh: pycxhm-00301',
      ['Vẫn ra PYCXHM-00301, kết quả giống hệt khi gõ chữ hoa.']),
    T('s_accent', 'Tìm có dấu / không dấu (ô Tên hàng hóa)', 'P1',
      PRE_LIST + '\nCó 2 phiếu chứa hàng tên "Dầu nhớt Eneo 0.8L".',
      [MENU_SALE, ADV, 'Nhập Tên hàng hóa = "dau nhot eneo".', 'Đổi thành "Dầu nhớt Eneo".'], 'Tên hàng hóa: dau nhot eneo',
      ['Cả 2 lần đều ra đúng 2 phiếu: hệ thống so khớp không phân biệt dấu và chữ hoa / thường.',
       'Mã phiếu không có dấu nên ô tìm nhanh không cần kiểm dấu.']),
    T('s_notexist', 'Từ khóa không tồn tại', 'P1', PRE_LIST,
      [MENU_SALE, 'Nhập "XYZ999" vào ô tìm nhanh.', 'Bấm Tìm kiếm.'], 'Ô tìm nhanh: XYZ999',
      ['Bảng hiện "Không có dữ liệu phù hợp.", dưới bảng "Không có phiếu nào.".', 'Không báo lỗi.']),
    T('s_special', 'Ký tự đặc biệt trong ô tìm nhanh', 'P2', PRE_LIST,
      [MENU_SALE, 'Nhập "@#$!" vào ô tìm nhanh, bấm Tìm kiếm.', 'Nhập "%" vào ô tìm nhanh, bấm Tìm kiếm.'],
      'Ô tìm nhanh: @#$!\nÔ tìm nhanh: %',
      ['Bước 2: "Không có dữ liệu phù hợp.", màn không treo, không báo lỗi.',
       'Bước 3: hiện lại cả 364 phiếu.',
       'Lưu ý: ký tự % và _ đang được hiểu là ký tự đại diện (không tìm đúng ký tự đó) — ghi nhận nếu cần tìm đúng nghĩa đen.']),
    T('s_trim', 'Khoảng trắng đầu / cuối từ khóa', 'P1', PRE_LIST,
      [MENU_SALE, 'Nhập "   00301   " (có khoảng trắng hai đầu) vào ô tìm nhanh.', 'Bấm Tìm kiếm.'],
      'Ô tìm nhanh: "   00301   "', ['Hệ thống bỏ khoảng trắng hai đầu, vẫn ra PYCXHM-00301.']),
    K('s_len', COMBO[3]),
    T('s_clear', 'Xóa từ khóa bằng nút × trong ô tìm nhanh', 'P1', PRE_LIST + '\nĐang tìm "0036" (8 phiếu).',
      [MENU_SALE, 'Nhập "0036", bấm Tìm kiếm.', 'Bấm dấu × ở cuối ô tìm nhanh.', 'Bấm Tìm kiếm.'], 'Ô tìm nhanh: 0036',
      ['Bước 3: ô trống ngay; danh sách VẪN giữ 8 phiếu cho tới khi bấm Tìm kiếm.',
       'Bước 4: hiện lại đủ 364 phiếu.']),
    T('s_enter', 'Nhấn Enter thay cho nút Tìm kiếm', 'P0', PRE_LIST,
      [MENU_SALE, 'Nhập "00301" vào ô tìm nhanh.', 'Nhấn phím Enter.'], 'Ô tìm nhanh: 00301',
      ['Danh sách lọc ngay như khi bấm Tìm kiếm, chỉ còn PYCXHM-00301.']),
    T('s_noauto', 'Ô tìm nhanh chỉ chạy khi bấm Tìm kiếm / Enter', 'P1', PRE_LIST,
      [MENU_SALE, 'Nhập "00301", KHÔNG bấm Tìm kiếm, chờ 3 giây.'], 'Ô tìm nhanh: 00301',
      ['Danh sách chưa đổi (vẫn 364 phiếu) cho tới khi bấm Tìm kiếm hoặc Enter.']),
    T('s_not_creator', 'Ô tìm nhanh không tìm theo tên người tạo', 'P2', PRE_LIST + '\nNguyễn Văn A có 3 phiếu.',
      [MENU_SALE, 'Nhập "Nguyễn Văn A" vào ô tìm nhanh.', 'Bấm Tìm kiếm.'], 'Ô tìm nhanh: Nguyễn Văn A',
      ['Không có kết quả (ô chỉ tìm theo mã phiếu); muốn lọc người tạo dùng ô Người tạo.']),
    T('s_default', 'Giá trị mặc định của bộ lọc', 'P1', PRE_LIST + '\nChưa lọc gì trong 10 phút gần đây.',
      [MENU_SALE, 'Quan sát khối lọc.', ADV, 'Mở ô Trạng thái.'], '—',
      ['Khối lọc nâng cao thu gọn khi mới vào; ô tìm nhanh trống.',
       'Mở ra: Phòng ban, Mã phiếu, Trạng thái, Người tạo, Người duyệt, Mã hàng hóa, Tên hàng hóa, Ngày tạo đều trống (tài khoản '
       'D không có ô Công ty).',
       'Ô Trạng thái chỉ có 3 lựa chọn: Chờ duyệt, Đã duyệt, Không duyệt (không có Đang tạo).']),
    T('s_status', 'Lọc theo Trạng thái', 'P0', PRE_LIST, [MENU_SALE, ADV, 'Chọn Trạng thái = Chờ duyệt.'], 'Trạng thái: Chờ duyệt',
      ['Danh sách nạp lại ngay (không cần bấm Tìm kiếm), chỉ còn 138 phiếu Chờ duyệt.']),
    T('s_people', 'Lọc theo Người tạo / Người duyệt', 'P0',
      PRE_LIST + '\nKế toán kho Cao Thị Thùy Linh đã duyệt / từ chối 20 phiếu; Nguyễn Văn A lập 3 phiếu.',
      [MENU_SALE, ADV, 'Chọn Người duyệt = Cao Thị Thùy Linh.', 'Bỏ Người duyệt, chọn Người tạo = Nguyễn Văn A.'],
      'Người duyệt: Cao Thị Thùy Linh\nNgười tạo: Nguyễn Văn A',
      ['Bước 3: còn 20 phiếu, cột Người duyệt đều là Cao Thị Thùy Linh.', 'Bước 4: còn 3 phiếu của Nguyễn Văn A.']),
    T('s_product', 'Lọc theo Mã hàng hóa / Tên hàng hóa', 'P0', PRE_LIST + '\nCó 2 phiếu chứa hàng mã ENEO-408-V5041.',
      [MENU_SALE, ADV, 'Nhập Mã hàng hóa = ENEO-408.'], 'Mã hàng hóa: ENEO-408',
      ['Chỉ còn các phiếu có ít nhất 1 dòng hàng mã chứa "ENEO-408".']),
    T('s_date', 'Lọc theo khoảng Ngày tạo', 'P0', PRE_LIST + '\nCó 4 phiếu tạo từ 01/10/2026 tới 05/10/2026 (1 phiếu lúc 23:59 ngày 05/10).',
      [MENU_SALE, ADV, 'Chọn Ngày tạo từ 01/10/2026 đến 05/10/2026.'], 'Ngày tạo: 01/10/2026 đến 05/10/2026',
      ['Đúng 4 phiếu, kể cả phiếu tạo lúc 23:59 ngày 05/10/2026.']),
    K('s_org_none', ORG[0]),
    K('s_org_pick', ORG[1]),
    K('s_org_change', ORG[2]),
    K('s_combo_kw', COMBO[0]),
    K('s_combo2', COMBO[1]),
    K('s_combo3', COMBO[2]),
    T('s_nores', 'Bộ lọc không có kết quả', 'P1', PRE_LIST + '\nNguyễn Văn A có 3 phiếu, không phiếu nào bị từ chối.',
      [MENU_SALE, ADV, 'Chọn Người tạo = Nguyễn Văn A.', 'Chọn Trạng thái = Không duyệt.'], 'Người tạo: Nguyễn Văn A\nTrạng thái: Không duyệt',
      ['Bảng hiện "Không có dữ liệu phù hợp.", dưới bảng "Không có phiếu nào.".', 'Các ô lọc vẫn giữ giá trị đã chọn.']),
    T('s_total_page', 'Tổng số và phân trang sau lọc', 'P0', PRE_LIST,
      [MENU_SALE, ADV, 'Chọn Trạng thái = Đã duyệt.', 'Bấm nút về trang cuối (»).'], 'Trạng thái: Đã duyệt',
      ['Bước 3: "Hiển thị 1–10 / 215", thanh phân trang còn 22 trang.', 'Bước 4: trang 22 "Hiển thị 211–215 / 215".',
       'Chuyển trang không làm mất bộ lọc.']),
    T('s_sort_after', 'Sắp xếp sau khi lọc', 'P1', PRE_LIST,
      [MENU_SALE, ADV, 'Chọn Trạng thái = Chờ duyệt.', 'Bấm tiêu đề cột Mã phiếu.'], 'Trạng thái: Chờ duyệt',
      ['Chỉ còn 138 phiếu Chờ duyệt, sắp tăng dần theo mã.', 'Ô Trạng thái vẫn là Chờ duyệt.']),
    T('s_reset', 'Bấm Làm mới', 'P0', PRE_LIST + '\nĐang tìm nhanh "0036", lọc Trạng thái = Chờ duyệt, sắp theo Ngày duyệt, ở lối vào Kế toán kho.',
      [MENU_KT, 'Nhập "0036", bấm Tìm kiếm; chọn Trạng thái = Chờ duyệt; bấm tiêu đề Ngày duyệt.', 'Bấm Làm mới.'], '—',
      ['Mọi ô lọc và ô tìm nhanh về trống, bỏ sắp xếp, về trang 1.',
       'Vẫn giữ đúng lối vào Kế toán kho (tiêu đề không đổi).']),
    K('s_mem_detail', MEM[0]),
    K('s_mem_expire', MEM[1]),
    K('s_mem_other', MEM[2]),
    T('s_f5', 'Tải lại trang (F5) khi đang lọc', 'P1', PRE_LIST + '\nTrong 10 phút gần đây chưa mở chi tiết phiếu nào.',
      [MENU_SALE, ADV, 'Chọn Trạng thái = Đã duyệt.', 'Nhấn F5.'], 'Trạng thái: Đã duyệt',
      ['Màn tải lại với bộ lọc trống, hiện đủ 364 phiếu.',
       'Lưu ý: bộ lọc chỉ được ghi nhớ khi đi vào màn chi tiết phiếu; F5 không giữ bộ lọc vừa chọn.']),
    K('s_mem_tab', MEM[4]),
    K('s_mem_account', MEM[3]),
]

# ====================================================================== III. THÊM MỚI
S_CREATE = [
    T('c_open', 'Điều hướng vào màn Thêm mới và tiêu đề', 'P0', PRE_A + '\nA có 3 phiếu xuất mượn Đã mượn.', TAO, '—',
      ['Mở màn "Thêm yêu cầu xuất hàng mượn" (tiêu đề màn và tab trình duyệt).',
       'Góc phải khối Thông tin chung ghi "<tên A> - <ngày giờ hiện tại>".']),
    T('c_fields', 'Hiển thị các trường và các nút', 'P0', PRE_A, TAO, '—',
      ['Thông tin chung: Phiếu xuất mượn (kèm nút Thêm phiếu), Ghi chú.',
       'Khối File đính kèm: bảng STT, Upload / File, Dung lượng và nút Thêm tài liệu.',
       'Bảng Chi tiết: STT, Tên hàng hóa, Đơn vị tính, Đơn giá, Số lượng xuất, Phiếu mượn, Đang mượn, Xuất, Thành tiền, '
       'nút + ở đầu cột cuối.',
       'Chân màn: Gửi duyệt, Lưu và tiếp tục, Quay lại.']),
    T('c_required', 'Trường bắt buộc / không bắt buộc', 'P1', PRE_A, TAO, '—',
      ['Nhãn Phiếu xuất mượn, Ghi chú có dấu * đỏ; khối File đính kèm bắt buộc ít nhất 1 file.',
       'Bảng Chi tiết bắt buộc có ít nhất 1 dòng hàng có số Xuất > 0.',
       'Màn không có trường tùy chọn nào ngoài việc chọn thêm phiếu mượn / file / dòng hàng thứ 2 trở đi.']),
    T('c_default', 'Giá trị mặc định khi mở màn', 'P1', PRE_A, TAO, '—',
      ['Phiếu xuất mượn ghi "Chưa chọn phiếu xuất mượn".', 'Ghi chú trống, gợi ý "Nhập lý do xuất số hàng đang mượn này...".',
       'File đính kèm chưa có file.',
       'Bảng Chi tiết trống: "Không có hàng hóa. Chọn phiếu xuất mượn ở trên, rồi bấm + ở góc phải bảng để thêm hàng hóa.".']),
    T('c_buttons', 'Nút Gửi duyệt / Lưu và tiếp tục / Quay lại (không có Lưu nháp)', 'P1', PRE_A, TAO + ['Rê chuột lên các nút ở chân màn.'],
      '—', ['Có 3 nút: Gửi duyệt, Lưu và tiếp tục (chú thích "Gửi duyệt phiếu này rồi tiếp tục lập phiếu mới"), Quay lại.',
            'KHÔNG có nút Lưu nháp, KHÔNG có nút Đóng / (x) (màn Thêm mới là một trang, không phải cửa sổ).']),
    T('c_pick_valid', 'Popup Chọn phiếu xuất mượn chỉ hiện phiếu hợp lệ của mình', 'P0',
      'A có: PYCXH-TEST-023 (Xuất mượn, Đã mượn), PYCXH-TEST-030 (Xuất mượn, Đã trả), 1 phiếu Xuất bán.',
      TAO + ['Bấm "Thêm phiếu".'], '—',
      ['Cửa sổ "Chọn phiếu xuất mượn", dòng mô tả "Chỉ hiện phiếu yêu cầu xuất hàng loại Xuất mượn do bạn lập…".',
       'Chỉ có PYCXH-TEST-023.', 'KHÔNG có phiếu Đã trả, phiếu Xuất bán và phiếu của người khác.']),
    T('c_pick', 'Chọn phiếu mượn', 'P0', PRE_A, TAO + ['Bấm "Thêm phiếu".', 'Bấm dòng PYCXH-TEST-023.'], '—',
      ['Báo "Thêm thành công.".', 'Ô Phiếu xuất mượn có thẻ PYCXH-TEST-023; dòng trong popup ghi "Đã chọn".',
       'Cửa sổ vẫn mở để chọn tiếp; bảng Chi tiết KHÔNG tự sinh dòng hàng.']),
    T('c_pick_again', 'Bấm lại phiếu đã chọn', 'P1', PRE_A + '\nĐã chọn PYCXH-TEST-023.',
      TAO + ['Chọn PYCXH-TEST-023.', 'Rê chuột rồi bấm lại dòng PYCXH-TEST-023 trong popup.'], '—',
      ['Rê chuột hiện "Phiếu này đã được chọn"; bấm không có tác dụng, không thêm thẻ thứ 2.']),
    T('c_pick_search', 'Tìm phiếu trong popup', 'P2', 'Tài khoản A có 27 phiếu mượn Đã mượn, trong đó PYCXH-TEST-023.',
      TAO + ['Bấm "Thêm phiếu".', 'Nhập "TEST-023" vào ô Mã phiếu xuất mượn.', 'Nhấn Enter.'], 'Mã phiếu xuất mượn: TEST-023',
      ['Chỉ còn PYCXH-TEST-023.', 'Bấm Làm mới: hiện lại 27 phiếu, 10 phiếu / trang.']),
    T('c_pick_close', 'Đóng popup Chọn phiếu xuất mượn', 'P2', PRE_A + '\nĐã chọn PYCXH-TEST-023 trong popup.',
      TAO + ['Bấm "Thêm phiếu", chọn PYCXH-TEST-023.', 'Bấm Đóng (hoặc (x), hoặc bấm ra ngoài cửa sổ).'], '—',
      ['Cửa sổ đóng ngay, không hỏi lại.', 'Thẻ PYCXH-TEST-023 vẫn còn trên form.']),
    T('c_addprod', 'Thêm hàng có trên phiếu mượn', 'P0', PRE_A + '\nĐã chọn PYCXH-TEST-023.',
      TAO + ['Chọn PYCXH-TEST-023.', 'Bấm nút + ở bảng Chi tiết.', 'Tìm ENEO-408-V5041, tích, bấm "Thêm 1 hàng hoá", bấm Đóng.'],
      'Hàng hóa: ENEO-408-V5041',
      ['Bảng có 1 dòng hàng, dòng con Phiếu mượn = PYCXH-TEST-023, Đang mượn = 46, Xuất trống (gợi ý 0).',
       'Đơn giá 60,500 theo đơn vị tính ghi trên phiếu mượn.']),
    T('c_dupprod', 'Thêm trùng một hàng đã có trong phiếu', 'P0', PRE_A + '\nBảng đã có dòng ENEO-408-V5041.',
      TAO + ['Chọn PYCXH-TEST-023, thêm ENEO-408-V5041.', 'Bấm + lần nữa, tích lại ENEO-408-V5041, bấm Thêm.'], '—',
      ['Báo "Hàng hóa đã có trong phiếu: <tên hàng>".', 'Bảng vẫn chỉ 1 dòng ENEO-408-V5041.']),
    T('c_lockedrow', 'Thêm hàng KHÔNG có trên phiếu mượn đã chọn', 'P0', PRE_A + '\nĐã chọn PYCXH-TEST-023.',
      TAO + ['Chọn PYCXH-TEST-023.', 'Bấm +, thêm hàng "Face ID Intellegent Edge AI System".'], '—',
      ['Dòng tô mờ, 3 ô chi tiết gộp thành "Chưa có phiếu mượn".', 'Không nhập được số lượng.']),
    T('c_link', 'Mã phiếu mượn trong bảng mở chi tiết phiếu mượn', 'P2', PRE_A + '\nDòng hàng có dòng con PYCXH-TEST-023.',
      TAO + ['Chọn PYCXH-TEST-023, thêm ENEO-408-V5041.', 'Bấm mã PYCXH-TEST-023 trong bảng.'], '—',
      ['Mở chi tiết phiếu yêu cầu xuất hàng ở tab mới; tab đang nhập giữ nguyên dữ liệu.']),
    T('c_qty', 'Nhập số Xuất hợp lệ và tính tiền', 'P0', PRE_A + '\nDòng ENEO-408-V5041, Đang mượn 46, Đơn giá 60,500.',
      TAO + ['Chọn PYCXH-TEST-023, thêm ENEO-408-V5041.', 'Nhập Xuất = 5.'], 'Xuất: 5',
      ['Số lượng xuất = 5.', 'Thành tiền = 302,500.', 'Dòng Tổng cộng: 5 và 302,500.']),
    T('c_qty_format', 'Sai định dạng ở ô Xuất', 'P1', PRE_A + '\nDòng ENEO-408-V5041, Đang mượn 46.',
      TAO + ['Chọn PYCXH-TEST-023, thêm ENEO-408-V5041.', 'Gõ "abc" vào ô Xuất.', 'Gõ "-3".', 'Gõ "2.5".'],
      'Xuất: abc\nXuất: -3\nXuất: 2.5',
      ['Bước 3: ô không nhận chữ cái, vẫn trống.', 'Bước 4: dấu trừ bị bỏ, ô còn 3.',
       'Bước 5: dấu chấm bị bỏ, ô còn 25 (ô chỉ nhận số nguyên).']),
    T('c_over', 'Nhập Xuất vượt Đang mượn', 'P0', PRE_A + '\nDòng ENEO-408-V5041, Đang mượn 46.',
      TAO + ['Chọn PYCXH-TEST-023, thêm ENEO-408-V5041.', 'Nhập Xuất = 47.'], 'Xuất: 47',
      ['Chữ đỏ "Vượt quá số đang mượn" ngay dưới ô, ô viền đỏ.', 'Ô KHÔNG tự đổi về 46.']),
    T('c_6digit', 'Nhập Xuất quá 6 chữ số', 'P2', PRE_A + '\nDòng ENEO-408-V5041, Đang mượn 46.',
      TAO + ['Chọn PYCXH-TEST-023, thêm ENEO-408-V5041.', 'Nhập Xuất = 1000000.'], 'Xuất: 1000000',
      ['Ô hiện "1,000,000"; chữ đỏ "Không được vượt quá 6 chữ số".']),
    T('c_unit', 'Đổi đơn vị tính tính lại Đang mượn', 'P0',
      'Hàng có 2 đơn vị: Can 0.8L (x1) và Thùng (x24); Đang mượn 46 can; đã nhập Xuất = 30.',
      TAO + ['Chọn phiếu mượn, thêm hàng, nhập Xuất = 30.', 'Đổi Đơn vị tính sang Thùng (x24).'], 'Đơn vị tính: Thùng (x24)',
      ['Đang mượn = 1 (46 / 24 làm tròn xuống).', 'Xuất tự kéo về 1.', 'Đơn giá đổi theo đơn vị Thùng.']),
    T('c_borrowcalc', 'Đang mượn đã trừ phần đang chờ ở phiếu khác', 'P0',
      'PYCXH-TEST-025 hàng ENEO-408-V5037 đã xuất 45, đã trả 22; có 1 yêu cầu xuất bán hàng mượn Chờ duyệt 10.',
      TAO + ['Chọn PYCXH-TEST-025, thêm hàng ENEO-408-V5037.'], '—', ['Đang mượn = 13 (45 trừ 22 trừ 10).']),
    T('c_removeticket', 'Bỏ một phiếu mượn đã chọn', 'P1', 'Đã chọn 2 phiếu mượn, cùng có hàng ENEO-408-V5041.',
      TAO + ['Chọn 2 phiếu, thêm ENEO-408-V5041.', 'Bấm dấu × trên thẻ 1 phiếu.'], '—',
      ['Dòng hàng vẫn còn, chỉ mất dòng con của phiếu vừa bỏ.', 'Nếu không còn dòng con nào: dòng bị khóa "Chưa có phiếu mượn".']),
    T('c_delrow', 'Xóa dòng hàng', 'P2', 'Đang ở màn Thêm mới; bảng có 2 dòng hàng.', ['Bấm biểu tượng thùng rác ở dòng 2.'], '—',
      ['Dòng bị bỏ ngay, không hỏi lại.', 'Còn 1 dòng, STT đánh lại, Tổng cộng cập nhật.']),
    T('c_ok', 'Gửi duyệt thành công với đầy đủ thông tin hợp lệ', 'P0',
      PRE_FORM_OK + '\nKế toán kho B cùng công ty với A.',
      TAO + ['Chọn PYCXH-TEST-023; Ghi chú "Khách lấy luôn 5 can"; Thêm tài liệu chungtu.pdf.',
             'Thêm ENEO-408-V5041, nhập Xuất = 5.', 'Bấm Gửi duyệt.', 'Bấm Gửi duyệt ở hộp xác nhận.'],
      'Ghi chú: Khách lấy luôn 5 can\nFile: chungtu.pdf\nXuất: 5',
      ['Báo "Yêu cầu của bạn đã được gửi.".', 'Về danh sách, phiếu mới PYCXHM-NNNNN ở đầu, trạng thái Chờ duyệt.',
       'Kế toán kho B nhận thông báo "[YCXHM] Chờ duyệt: <mã>".']),
    T('c_ok_min', 'Chỉ nhập trường bắt buộc ở mức tối thiểu', 'P1', PRE_FORM_OK,
      TAO + ['Chọn đúng 1 phiếu PYCXH-TEST-023; Ghi chú "a" (1 ký tự); 1 file chungtu.pdf.',
             'Thêm 1 hàng ENEO-408-V5041, Xuất = 1.', 'Bấm Gửi duyệt, xác nhận.'], 'Ghi chú: a\nXuất: 1',
      ['Gửi thành công, phiếu mới Chờ duyệt.', 'Màn không có trường tùy chọn nào để bỏ trống (mọi trường nhập đều bắt buộc).']),
    T('c_after', 'Dữ liệu sau lưu đúng với dữ liệu đã nhập', 'P0', 'A vừa gửi phiếu ở TC "Gửi duyệt thành công" (Xuất 5, Ghi chú '
      '"Khách lấy luôn 5 can", file chungtu.pdf). A thuộc phòng MT_KD.',
      [MENU_SALE, 'Bấm mã phiếu vừa tạo.'], '—',
      ['Phiếu xuất mượn: thẻ PYCXH-TEST-023; Ghi chú đúng; Phòng ban yêu cầu = MT_KD.',
       'File đính kèm: chungtu.pdf kèm Dung lượng 2 MB.',
       'Bảng Chi tiết: ENEO-408-V5041, Đơn giá 60,500, Số lượng 5, Xuất 5, Được duyệt 0, Thành tiền 302,500.']),
    T('c_status_default', 'Trạng thái mặc định sau khi gửi', 'P0', 'A vừa gửi 1 phiếu.', [MENU_SALE, 'Quan sát dòng phiếu vừa gửi.'],
      '—', ['Trạng thái Chờ duyệt (nhãn cam) — không có bước nháp Đang tạo.', 'Người duyệt, Ngày duyệt để trống.',
            'Người tạo = A, Ngày tạo = thời điểm gửi.']),
    T('c_hist', 'Lịch sử ghi nhận khi tạo', 'P0', 'A vừa gửi 1 phiếu lúc 02/11/2026 09:00.',
      [MENU_SALE, 'Bấm Lịch sử ở dòng phiếu vừa gửi.'], '—',
      ['Có đúng 1 mốc "Tạo mới" lúc 02/11/2026 09:00, Người thực hiện = A.',
       'Nội dung mốc có phiếu xuất mượn, ghi chú và dòng hàng lúc gửi.']),
    T('c_empty_submit', 'Gửi duyệt khi bỏ trống trường bắt buộc', 'P0', 'Tài khoản A có ít nhất 1 phiếu mượn Đã mượn.',
      TAO + ['Bấm Gửi duyệt.'], '—',
      ['Thông báo "Bạn chưa nhập đầy đủ thông tin.".',
       'Chữ đỏ: "Bắt buộc phải chọn ít nhất 1 phiếu xuất mượn", "Bắt buộc phải nhập" (Ghi chú), '
       '"Bắt buộc phải đính kèm ít nhất 1 file", "Chưa có hàng hoá nào để xuất.".',
       'Màn cuộn về ô lỗi đầu tiên; không hiện hộp xác nhận, không gửi.']),
    T('c_nofile', 'Thiếu file đính kèm', 'P0', PRE_A + '\nĐã chọn phiếu, nhập ghi chú, có dòng Xuất = 5, chưa có file.',
      TAO + ['Nhập đủ trừ file.', 'Bấm Gửi duyệt.'], '—',
      ['Khối File đính kèm viền đỏ, "Bắt buộc phải đính kèm ít nhất 1 file".', 'Không gửi.']),
    T('c_filetype', 'File đính kèm sai định dạng / quá dung lượng', 'P0',
      'Đang ở màn Thêm mới; có file baocao.docx và file PDF 25 MB trên máy.',
      ['Bấm Thêm tài liệu, chọn baocao.docx.', 'Bấm Thêm tài liệu, chọn file PDF 25 MB.', 'Chọn file PDF 3 MB.'],
      'File: baocao.docx\nFile: hopdong.pdf 25 MB\nFile: chungtu.pdf 3 MB',
      ['Bước 1: báo "File "baocao.docx" không thuộc định dạng cho phép".', 'Bước 2: báo "File "hopdong.pdf" vượt quá 20MB".',
       'Bước 3: file nhận bình thường, hiện tên và dung lượng.']),
    T('c_special', 'Ký tự đặc biệt trong Ghi chú', 'P2', PRE_FORM_OK,
      TAO + ['Nhập đủ dữ liệu hợp lệ, Ghi chú = "Xuất <b>gấp</b> & 100% @#".', 'Gửi duyệt, xác nhận.', 'Mở chi tiết phiếu vừa gửi.'],
      'Ghi chú: Xuất <b>gấp</b> & 100% @#',
      ['Gửi thành công (Ghi chú không chặn ký tự đặc biệt).', 'Màn chi tiết hiện đúng nguyên văn, không biến thành chữ đậm.']),
    T('c_max_ok', 'Ghi chú đúng độ dài tối đa 255 ký tự', 'P1', PRE_FORM_OK + '\nCó sẵn đoạn văn đúng 255 ký tự.',
      TAO + ['Nhập đủ dữ liệu hợp lệ, dán đoạn 255 ký tự vào Ghi chú.', 'Gửi duyệt, xác nhận.'], 'Ghi chú: 255 ký tự',
      ['Gửi thành công.', 'Màn chi tiết hiện đủ 255 ký tự.']),
    T('c_max_over', 'Ghi chú vượt độ dài tối đa', 'P2', 'Đang ở màn Thêm mới; có sẵn đoạn văn 300 ký tự.',
      ['Dán đoạn 300 ký tự vào Ghi chú.'], 'Ghi chú: 300 ký tự', ['Ô chỉ nhận tối đa 255 ký tự, phần sau bị cắt.']),
    T('c_dup', 'Trùng bản ghi: 2 phiếu cùng nội dung', 'P1',
      PRE_FORM_OK + '\nPhiếu không có trường duy nhất ngoài mã tự sinh.',
      ['Lập và gửi phiếu 1: PYCXH-TEST-023, ENEO-408-V5041 Xuất 5, Ghi chú "Xuất bù".',
       'Lập phiếu 2 y hệt (cùng phiếu mượn, cùng hàng, Xuất 5, cùng Ghi chú, cùng file), gửi duyệt.'], 'Xuất: 5 (cả 2 phiếu)',
      ['Cả 2 phiếu lưu được, mã khác nhau (PYCXHM-NNNNN liên tiếp).',
       'Ở phiếu 2, Đang mượn của hàng chỉ còn 41 (đã trừ 5 đang chờ ở phiếu 1).']),
    T('c_trim', 'Khoảng trắng đầu / cuối Ghi chú', 'P2', PRE_FORM_OK,
      TAO + ['Nhập đủ dữ liệu hợp lệ, Ghi chú = "   Xuất bù   ".', 'Gửi duyệt, xác nhận.', 'Mở chi tiết.'], 'Ghi chú: "   Xuất bù   "',
      ['Ghi chú lưu là "Xuất bù" (bỏ khoảng trắng hai đầu).']),
    T('c_spaces', 'Ghi chú chỉ có khoảng trắng', 'P0', PRE_FORM_OK,
      TAO + ['Nhập đủ dữ liệu hợp lệ, Ghi chú chỉ gồm 5 dấu cách.', 'Bấm Gửi duyệt.'], 'Ghi chú: 5 dấu cách',
      ['Chữ đỏ "Bắt buộc phải nhập" dưới Ghi chú; thông báo "Bạn chưa nhập đầy đủ thông tin."; không gửi.']),
    T('c_err_clear', 'Lỗi biến mất sau khi sửa', 'P1', PRE_A, TAO + ['Bấm Gửi duyệt khi form trống.', 'Nhập Ghi chú "Xuất bù".',
                                                                    'Chọn phiếu PYCXH-TEST-023.'], 'Ghi chú: Xuất bù',
      ['Bước 4: chữ đỏ dưới Ghi chú biến mất ngay khi gõ.', 'Bước 5: lỗi "Bắt buộc phải chọn ít nhất 1 phiếu xuất mượn" biến mất.',
       'Các lỗi chưa sửa vẫn còn.']),
    T('c_dirty_server', 'Số Đang mượn thay đổi trong lúc nhập', 'P1',
      'Đang nhập Xuất = 46 cho ENEO-408-V5041; người khác vừa gửi 1 phiếu chờ trả 10 cái cùng hàng, cùng phiếu mượn.',
      ['Bấm Gửi duyệt, xác nhận.'], '—', ['Báo "Số lượng vượt quá số đang mượn (36).", không gửi; dữ liệu trên form còn nguyên.']),
    T('c_confirm_cancel', 'Hộp xác nhận gửi duyệt — bấm Hủy', 'P0', PRE_FORM_OK + '\nForm đã nhập hợp lệ.',
      ['Bấm Gửi duyệt.', 'Bấm Hủy.'], '—',
      ['Hộp "Xác nhận gửi duyệt": "Gửi duyệt phiếu yêu cầu xuất hàng mượn này? Sau khi gửi, phiếu không sửa được nữa.".',
       'Bấm Hủy: ở lại màn, dữ liệu giữ nguyên, không tạo phiếu.']),
    T('c_send_nav', 'Màn hình sau khi Gửi duyệt và mở lại Thêm mới', 'P0', PRE_FORM_OK + '\nForm đã nhập hợp lệ.',
      ['Bấm Gửi duyệt, xác nhận.', 'Ở danh sách bấm Tạo mới.'], '—',
      ['Bước 1: màn Thêm mới đóng, về danh sách lối vào Bán hàng; không hỏi "Thông tin chưa lưu".',
       'Bước 2: form trống hoàn toàn, không còn dữ liệu của phiếu vừa gửi.']),
    T('c_sc_ok', 'Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM_OK + '\nForm đã nhập hợp lệ.',
      ['Bấm Lưu và tiếp tục.', 'Bấm Gửi duyệt ở hộp xác nhận.'], '—',
      ['Báo "Yêu cầu của bạn đã được gửi."; phiếu được gửi ở trạng thái Chờ duyệt.',
       'Ở lại màn "Thêm yêu cầu xuất hàng mượn" (không về danh sách), trang cuộn lên đầu.']),
    T('c_sc_reset', 'Lưu và tiếp tục: các trường được làm mới', 'P0', PRE_FORM_OK + '\nVừa Lưu và tiếp tục thành công.',
      ['Quan sát form sau khi Lưu và tiếp tục.'], '—',
      ['Phiếu xuất mượn về "Chưa chọn phiếu xuất mượn"; Ghi chú trống; File đính kèm trống; bảng Chi tiết trống.',
       'Không còn chữ đỏ nào; góc phải ghi lại thời điểm hiện tại.']),
    T('c_sc_err', 'Lưu và tiếp tục khi thiếu trường bắt buộc', 'P0',
      PRE_A + '\nForm đã thêm 1 dòng hàng nhưng chưa chọn phiếu mượn, Ghi chú trống.',
      TAO + ['Thêm hàng ENEO-408-V5041.', 'Bấm Lưu và tiếp tục.'], 'Ghi chú: trống',
      ['Thông báo "Bạn chưa nhập đầy đủ thông tin.".', 'Chữ đỏ dưới Phiếu xuất mượn, Ghi chú, File đính kèm.',
       'KHÔNG lưu phiếu, KHÔNG làm mới form; dòng hàng đã thêm vẫn còn.']),
    T('c_sc_fmt', 'Lưu và tiếp tục khi số Xuất sai', 'P1', PRE_FORM_OK + '\nForm hợp lệ trừ ô Xuất = 47 (Đang mượn 46).',
      ['Bấm Lưu và tiếp tục.'], 'Xuất: 47',
      ['Thông báo "Bạn chưa nhập đầy đủ thông tin."; chữ đỏ "Vượt quá số đang mượn" dưới ô Xuất.', 'Không lưu, dữ liệu giữ nguyên.']),
    T('c_sc_dup', 'Lưu và tiếp tục 2 lần với cùng nội dung', 'P2', PRE_FORM_OK,
      ['Nhập phiếu: PYCXH-TEST-023, Xuất 5, Ghi chú "Xuất bù", 1 file; bấm Lưu và tiếp tục, xác nhận.',
       'Nhập lại y hệt; bấm Lưu và tiếp tục, xác nhận.'], 'Xuất: 5 (cả 2 lần)',
      ['Cả 2 lần đều gửi thành công, 2 mã phiếu khác nhau.', 'Lần 2 Đang mượn hiện 41 (đã trừ phần chờ của lần 1).']),
    T('c_sc_close', 'Thoát màn sau Lưu và tiếp tục', 'P2', PRE_FORM_OK + '\nVừa Lưu và tiếp tục thành công, chưa nhập gì thêm.',
      ['Bấm Quay lại.'], '—',
      ['Về danh sách ngay, KHÔNG hỏi "Thông tin chưa lưu".', 'Phiếu vừa gửi có trong danh sách với trạng thái Chờ duyệt.']),
    T('c_back_clean', 'Quay lại khi chưa nhập gì', 'P1', 'Tài khoản A vừa mở màn Thêm mới, chưa thao tác.', TAO + ['Bấm Quay lại.'],
      '—', ['Về màn danh sách ngay, không hỏi xác nhận.']),
    T('c_back_dirty', 'Quay lại khi đã nhập dữ liệu', 'P0', PRE_A + '\nĐã chọn phiếu mượn và nhập Ghi chú.',
      TAO + ['Chọn PYCXH-TEST-023, nhập Ghi chú "Xuất bù".', 'Bấm Quay lại.'], 'Ghi chú: Xuất bù',
      ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", 2 nút Thoát và Ở lại.']),
    T('c_closetab', 'Đóng tab / tải lại trang khi đã nhập (thay cho nút X)', 'P2', PRE_A + '\nĐã nhập Ghi chú.',
      TAO + ['Nhập Ghi chú "Xuất bù".', 'Bấm nút đóng tab của trình duyệt (hoặc F5).'], '—',
      ['Trình duyệt hiện hộp hỏi rời trang (nội dung do trình duyệt quyết định).', 'Chọn ở lại: dữ liệu còn nguyên.']),
    T('c_exit', 'Chọn Thoát ở hộp Thông tin chưa lưu', 'P0', PRE_A + '\nĐã nhập dữ liệu, hộp "Thông tin chưa lưu" đang mở.',
      ['Bấm Thoát.'], '—', ['Về màn danh sách; dữ liệu đã nhập bị bỏ; không có phiếu mới nào được tạo.']),
    T('c_stay', 'Chọn Ở lại ở hộp Thông tin chưa lưu', 'P0', PRE_A + '\nĐã nhập dữ liệu, hộp "Thông tin chưa lưu" đang mở.',
      ['Bấm Ở lại.'], '—', ['Hộp đóng, vẫn ở màn Thêm mới; phiếu mượn, Ghi chú, dòng hàng còn nguyên.']),
    T('c_clear_all', 'Nhập rồi xóa hết dữ liệu', 'P2', PRE_A, TAO + ['Nhập Ghi chú "Xuất bù".', 'Xóa hết nội dung Ghi chú.',
                                                                   'Bấm Quay lại.'], 'Ghi chú: Xuất bù (rồi xóa)',
      ['Về danh sách ngay, KHÔNG hỏi "Thông tin chưa lưu" (form đã trở về như ban đầu).']),
    T('c_restore', 'Đổi rồi khôi phục giá trị ban đầu', 'P2', PRE_A,
      TAO + ['Chọn phiếu PYCXH-TEST-023.', 'Bấm dấu × bỏ thẻ PYCXH-TEST-023.', 'Bấm Quay lại.'], '—',
      ['Về danh sách ngay, KHÔNG hỏi "Thông tin chưa lưu".']),
    T('c_idle', 'Không thao tác lâu đến khi hết phiên đăng nhập', 'P2', PRE_FORM_OK + '\nForm đã nhập hợp lệ; phiên đăng nhập '
      'đã hết hạn trong lúc để yên.',
      ['Để yên màn Thêm mới tới khi hết phiên.', 'Bấm Gửi duyệt, xác nhận.'], '—',
      ['Màn không tự đóng, không tự xóa dữ liệu khi để yên.',
       'Bước 2: báo phiên đăng nhập đã hết hạn (vd "Phiên đăng nhập đã hết hạn") và chuyển về màn đăng nhập; phiếu KHÔNG được tạo.']),
    T('c_doubleclick', 'Bấm nút gửi liên tục nhiều lần', 'P0', PRE_FORM_OK + '\nForm đã nhập hợp lệ.',
      ['Bấm Gửi duyệt.', 'Ở hộp xác nhận bấm nút Gửi duyệt 5 lần thật nhanh.'], '—',
      ['Nút Gửi duyệt và Lưu và tiếp tục bị khóa trong lúc đang gửi.', 'Chỉ 1 phiếu được tạo (danh sách tăng đúng 1).']),
    T('c_concurrent', 'Hai tab cùng gửi phiếu cho một phần hàng', 'P0',
      PRE_FORM_OK + '\nMở màn Thêm mới ở 2 tab, cả 2 chọn PYCXH-TEST-023, hàng ENEO-408-V5041, Xuất = 30.',
      ['Tab 1 bấm Gửi duyệt, xác nhận.', 'Tab 2 bấm Gửi duyệt, xác nhận.'], 'Xuất: 30 (mỗi tab)',
      ['Tab 1 gửi thành công.', 'Tab 2 báo "Số lượng vượt quá số đang mượn (16).", không gửi (phần Đang mượn đã bị tab 1 giữ chỗ).']),
]

# ====================================================================== IV. CHỈNH SỬA (màn không có Sửa)
S_EDIT = [
    T('e_none', 'Không có chức năng Sửa ở mọi trạng thái', 'P0',
      PRE_KT + '\nCó phiếu Chờ duyệt PYCXHM-00301, Đã duyệt PYCXHM-00290, Không duyệt PYCXHM-00291 (A là người lập).',
      ['Đăng nhập bằng A (người lập), mở danh sách và chi tiết 3 phiếu.', 'Đăng nhập bằng B (Kế toán kho), lặp lại.'], '—',
      ['Cột Hành động chỉ có Duyệt (B, phiếu Chờ duyệt), In, Lịch sử — KHÔNG có nút Sửa.',
       'Màn chi tiết mọi ô chỉ đọc, không có nút Sửa / Lưu.',
       'Ghi chú: phiếu gửi đi là vào thẳng Chờ duyệt, không sửa được ở bất kỳ trạng thái nào.']),
    T('e_redo', 'Muốn đổi nội dung phiếu đã gửi thì lập phiếu mới', 'P1',
      PRE_A + '\nA gửi phiếu PYCXHM-00301 (Xuất 5) đang Chờ duyệt; B là Kế toán kho.',
      ['B từ chối PYCXHM-00301 với lý do "Sai số lượng".', 'A bấm Tạo mới, chọn lại PYCXH-TEST-023, thêm ENEO-408-V5041.'], '—',
      ['Phiếu PYCXHM-00301 chuyển Không duyệt, vẫn không sửa / gửi lại được.',
       'Phiếu mới: Đang mượn trở lại 46 (phần 5 của phiếu bị từ chối được trả lại).']),
]

# ====================================================================== V. XÓA (màn không có Xóa)
S_DEL = [
    T('d_none', 'Không có chức năng Xóa', 'P1', PRE_KT + '\nCó phiếu ở đủ 3 trạng thái.',
      ['Đăng nhập bằng A rồi B, mở danh sách và chi tiết từng phiếu.'], '—',
      ['Không có nút Xóa ở cột Hành động, màn chi tiết hay thanh nút trên bảng.',
       'Phiếu không cần dùng nữa xử lý bằng Từ chối (Kế toán kho), không xóa khỏi hệ thống.']),
]

# ====================================================================== VI. LỊCH SỬ THAY ĐỔI
PRE_HIS = ('Phiếu PYCXHM-00340 do A tạo lúc 21/10/2026 08:00, Kế toán kho B duyệt lúc 22/10/2026 10:30 bằng phiếu xuất '
           'PXHM-00120.')
S_HIS = [
    T('h_open', 'Mở popup Lịch sử và nội dung từng mốc', 'P0', PRE_HIS, [MENU_SALE, 'Bấm Lịch sử ở dòng PYCXHM-00340.'], '—',
      ['Cửa sổ "Lịch sử thay đổi: Phiếu PYCXHM-00340".',
       'Mỗi mốc có: thời gian, loại hành động, "Người thực hiện: <tên> — <phòng ban>", nội dung thay đổi.',
       'Mốc "Duyệt": "Trạng thái: Chờ duyệt đến Đã duyệt", ghi chú "Phiếu xuất hàng mượn: PXHM-00120", người thực hiện B.',
       'Mốc "Tạo mới": thông tin phiếu và dòng hàng lúc gửi, người thực hiện A.']),
    T('h_order', 'Mốc mới nhất ở trên', 'P1', PRE_HIS, [MENU_SALE, 'Bấm Lịch sử ở dòng PYCXHM-00340.'], '—',
      ['Mốc Duyệt (22/10/2026 10:30) ở trên, mốc Tạo mới (21/10/2026 08:00) ở dưới.']),
    T('h_f_action', 'Lọc theo loại hành động', 'P1', PRE_HIS,
      [MENU_SALE, 'Bấm Lịch sử ở dòng PYCXHM-00340.', 'Bấm Bộ lọc.', 'Chọn Loại hành động = Thay đổi trạng thái.'],
      'Loại hành động: Thay đổi trạng thái',
      ['Ô Loại hành động có 3 lựa chọn: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.',
       'Chọn là lọc ngay: chỉ còn mốc Duyệt.']),
    T('h_f_user', 'Lọc theo người thực hiện', 'P1', PRE_HIS,
      ['Mở Lịch sử PYCXHM-00340, bấm Bộ lọc.', 'Chọn Người thực hiện = A.'], 'Người thực hiện: A',
      ['Chỉ còn mốc Tạo mới.']),
    T('h_f_time', 'Lọc theo thời gian', 'P1', PRE_HIS,
      ['Mở Lịch sử PYCXHM-00340, bấm Bộ lọc.', 'Chọn Từ ngày = 22/10/2026, Đến ngày = 22/10/2026.'], 'Từ ngày / Đến ngày: 22/10/2026',
      ['Chỉ còn mốc Duyệt (lấy trọn ngày 22/10/2026).']),
    T('h_f_combo', 'Kết hợp nhiều điều kiện lọc', 'P2', PRE_HIS,
      ['Mở Lịch sử PYCXHM-00340, bấm Bộ lọc.', 'Chọn Loại hành động = Tạo mới và Người thực hiện = B.'],
      'Loại hành động: Tạo mới\nNgười thực hiện: B', ['Không còn mốc nào thỏa cả 2 điều kiện.']),
    T('h_f_none', 'Lọc không có kết quả', 'P2', PRE_HIS,
      ['Mở Lịch sử PYCXHM-00340, bấm Bộ lọc.', 'Chọn Từ ngày = 01/01/2026, Đến ngày = 31/01/2026.'], 'Khoảng 01/01/2026 – 31/01/2026',
      ['Hiện "Không có lịch sử phù hợp bộ lọc.".']),
    T('h_f_reset', 'Làm mới bộ lọc lịch sử', 'P2', PRE_HIS + '\nĐang lọc Người thực hiện = A.',
      ['Bấm Làm mới trong khối lọc.'], '—', ['Mọi ô lọc về trống, hiện lại đủ 2 mốc.']),
    T('h_f_toggle', 'Đóng / mở khối bộ lọc lịch sử', 'P2', PRE_HIS, ['Mở Lịch sử PYCXHM-00340.', 'Bấm Bộ lọc.', 'Bấm Bộ lọc lần nữa.'],
      '—', ['Bước 2: hiện các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày, nút Làm mới.', 'Bước 3: khối lọc thu gọn.']),
    T('h_reject', 'Ghi nhận mốc khi phiếu bị từ chối', 'P0', 'Phiếu PYCXHM-00291 bị B từ chối lý do "Sai số lượng".',
      ['Mở Lịch sử PYCXHM-00291.'], '—',
      ['Có mốc "Từ chối": "Trạng thái: Chờ duyệt đến Không duyệt" kèm lý do "Sai số lượng", người thực hiện B.']),
    T('h_multi', 'Một thao tác đổi nhiều thông tin chỉ ghi 1 mốc', 'P2', PRE_HIS,
      ['Mở Lịch sử PYCXHM-00340.', 'Đếm số mốc phát sinh lúc 22/10/2026 10:30.'], '—',
      ['Lần duyệt đổi đồng thời Trạng thái, Người duyệt, Ngày duyệt, cột Được duyệt nhưng chỉ có 1 mốc "Duyệt".']),
    T('h_nolog', 'Không ghi lịch sử khi không thay đổi dữ liệu', 'P0', PRE_HIS + '\nĐang có 2 mốc.',
      ['Mở chi tiết, In, Xuất Excel phiếu PYCXHM-00340.', 'Kế toán kho mở cửa sổ Từ chối của một phiếu Chờ duyệt rồi bấm Đóng.',
       'Mở lại Lịch sử cả 2 phiếu.'], '—', ['Không có mốc mới nào được thêm.']),
    T('h_empty', 'Phiếu chưa có lịch sử', 'P2', 'Phiếu PYCXHM-00010 lập từ trước khi có chức năng lịch sử (dữ liệu cũ).',
      ['Bấm Lịch sử ở dòng PYCXHM-00010.'], '—', ['Hiện "Chưa có lịch sử thao tác nào.".']),
    T('h_close', 'Đóng popup bằng Đóng / (x)', 'P2', PRE_HIS, ['Mở Lịch sử PYCXHM-00340.', 'Bấm Đóng.', 'Mở lại, bấm (x).'], '—',
      ['Cả 2 cách đều đóng cửa sổ ngay.']),
    T('h_close_state', 'Danh sách giữ nguyên sau khi đóng popup', 'P1', PRE_LIST + '\nĐang ở trang 3, lọc Trạng thái = Đã duyệt, sắp theo Mã phiếu.',
      ['Bấm Lịch sử ở một dòng trang 3.', 'Đóng cửa sổ.'], '—',
      ['Vẫn ở trang 3, bộ lọc Đã duyệt và sắp xếp theo Mã phiếu giữ nguyên; danh sách không nạp lại.']),
]

# ====================================================================== VII. XEM CHI TIẾT
S_DETAIL = [
    T('v_content', 'Mở chi tiết: tiêu đề, đầy đủ trường, chỉ đọc', 'P0', 'Phiếu PYCXHM-00337 Chờ duyệt, 2 dòng hàng, 1 file; tài khoản A là người lập.',
      ['Đăng nhập bằng A.', MENU_SALE, 'Bấm mã PYCXHM-00337.'], '—',
      ['Tiêu đề "Chi tiết yêu cầu xuất hàng mượn: PYCXHM-00337".',
       'Có Người tạo – Ngày tạo, Phiếu xuất mượn, Ghi chú, Phòng ban yêu cầu, File đính kèm (có Dung lượng), bảng Chi tiết '
       '(Đơn vị tính, Đơn giá, Số lượng, Phiếu mượn, Xuất, Được duyệt, Thành tiền, Tổng cộng), khối Lịch sử.',
       'Mọi ô chỉ đọc; KHÔNG có nút Lưu / Sửa; chỉ có In và Quay lại (A không phải Kế toán kho).']),
    T('v_match_list', 'Thông tin chi tiết khớp với dòng trên danh sách', 'P1', 'Phiếu PYCXHM-00290 Đã duyệt.',
      [MENU_SALE, 'Ghi lại Mã phiếu, Người tạo, Ngày tạo trên dòng PYCXHM-00290.', 'Bấm mã để mở chi tiết.'], '—',
      ['Mã phiếu ở tiêu đề, Người tạo – Ngày tạo ở góc phải khớp đúng dòng danh sách.']),
    T('v_approved', 'Cột Được duyệt theo trạng thái', 'P0', 'Phiếu PYCXHM-00337 Chờ duyệt và PYCXHM-00290 Đã duyệt (duyệt 5 / xin 5).',
      ['Mở chi tiết 2 phiếu.'], '—', ['Chờ duyệt: Được duyệt = 0.', 'Đã duyệt: Được duyệt = 5, đúng số trên Phiếu xuất hàng mượn.']),
    T('v_rejected', 'Khối Ghi chú duyệt của phiếu Không duyệt', 'P0', 'Phiếu PYCXHM-00291 Không duyệt lý do "Sai số lượng".',
      ['Mở chi tiết PYCXHM-00291.'], '—', ['Có khối "Ghi chú duyệt" ghi "Sai số lượng".', 'Phiếu chưa bị từ chối không có khối này.']),
    T('v_history_block', 'Khối Lịch sử ở màn chi tiết', 'P1', PRE_HIS,
      ['Mở chi tiết PYCXHM-00340.', 'Bấm "Xem lịch sử".', 'Bấm "Thu gọn".'], '—',
      ['Khối Lịch sử thu gọn khi mới mở.', 'Bước 2: hiện các mốc giống hệt cửa sổ Lịch sử ở danh sách, nút đổi thành "Thu gọn".',
       'Bước 3: khối thu gọn lại.']),
    T('v_links', 'Mở phiếu mượn và file đính kèm từ chi tiết', 'P2', 'Phiếu PYCXHM-00337 có thẻ PYCXH-TEST-023 và file chungtu.pdf.',
      ['Mở chi tiết PYCXHM-00337.', 'Bấm thẻ PYCXH-TEST-023 ở Thông tin chung.', 'Bấm Xem trước rồi Tải xuống ở file chungtu.pdf.'], '—',
      ['Bước 2: chi tiết phiếu mượn mở ở tab mới.', 'Bước 3: xem trước được PDF; tải xuống được file về máy.']),
    T('v_notfound', 'Mở phiếu không tồn tại', 'P1', 'Tài khoản A có thông báo của một phiếu đã bị xóa khỏi hệ thống.',
      ['Bấm thông báo cũ của phiếu đó.'], '—', ['Báo "Không tìm thấy dữ liệu", về danh sách.']),
    T('v_back', 'Quay lại về đúng màn trước', 'P2', PRE_KT + '\nVào chi tiết từ lối vào Kế toán kho, đang lọc Trạng thái = Chờ duyệt.',
      [MENU_KT, 'Lọc Trạng thái = Chờ duyệt, bấm mã một phiếu.', 'Bấm Quay lại.'], '—',
      ['Về đúng danh sách Kế toán kho, giữ bộ lọc Chờ duyệt.']),
    T('v_back_keep', 'Giữ trang và bộ lọc khi quay lại danh sách', 'P0', PRE_LIST,
      [MENU_SALE, ADV, 'Chọn Trạng thái = Đã duyệt, bấm trang 3.', 'Bấm mã một phiếu ở trang 3.', 'Bấm Quay lại.'], 'Trạng thái: Đã duyệt',
      ['Bộ lọc Trạng thái = Đã duyệt được giữ.',
       'Lưu ý: danh sách về trang 1 (không giữ trang 3) và bỏ sắp xếp — đúng theo thiết kế hiện tại, chỉ bộ lọc được ghi nhớ.']),
]

# ====================================================================== VIII. TÙY CHỈNH CỘT
PRE_COL = PRE_LIST + '\nTài khoản D chưa từng tùy chỉnh cột.'
S_COL = [
    T('k_open', 'Mở popup Tùy chỉnh cột, danh sách cột và cột chọn mặc định', 'P1', PRE_COL,
      [MENU_SALE, 'Bấm nút Cấu hình cột hiển thị (biểu tượng cột).'], '—',
      ['Cửa sổ "Tuỳ chỉnh cột" liệt kê 13 cột.',
       'Tích sẵn 8 cột: STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Hành động.',
       'Chưa tích: Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối; dòng "Đang chọn 8/13 cột".']),
    T('k_show', 'Hiện cột đang ẩn', 'P1', PRE_COL, ['Mở Tùy chỉnh cột.', 'Tích "Lý do từ chối".', 'Bấm Lưu.'], '—',
      ['Báo "Cập nhật thành công".', 'Bảng có thêm cột Lý do từ chối, phiếu Không duyệt hiện đúng lý do.']),
    T('k_hide', 'Ẩn một cột đang hiện', 'P1', PRE_COL, ['Mở Tùy chỉnh cột.', 'Bỏ tích "Người duyệt".', 'Bấm Lưu.'], '—',
      ['Cột Người duyệt biến mất khỏi bảng; các cột khác giữ nguyên thứ tự.']),
    T('k_locked', 'Cột bắt buộc không ẩn được, cột cố định', 'P0', PRE_COL,
      ['Mở Tùy chỉnh cột.', 'Thử bỏ tích và kéo STT, Mã phiếu, Hành động.', 'Đóng cửa sổ, kéo thanh cuộn ngang của bảng.'], '—',
      ['Ba cột có biểu tượng ổ khóa (rê chuột: "Cột bắt buộc — không thể ẩn hoặc đổi vị trí"), không bỏ tích, không kéo được.',
       'Khi cuộn ngang, cột STT và Mã phiếu ghim bên trái.']),
    T('k_drag', 'Kéo thả đổi thứ tự cột', 'P2', PRE_COL, ['Mở Tùy chỉnh cột.', 'Kéo Ngày tạo lên trên Người tạo.', 'Bấm Lưu.'], '—',
      ['Bảng đổi thứ tự: Ngày tạo đứng trước Người tạo.']),
    T('k_selectall', 'Chọn tất cả / Bỏ chọn hết', 'P2', PRE_COL, ['Mở Tùy chỉnh cột.', 'Bấm Chọn tất cả.', 'Bấm Bỏ chọn hết.'], '—',
      ['Bước 2: tích đủ 13 cột, "Đang chọn 13/13 cột".', 'Bước 3: chỉ còn 3 cột khóa được tích, "Đang chọn 3/13 cột".']),
    T('k_save', 'Lưu cấu hình', 'P0', PRE_COL, ['Mở Tùy chỉnh cột.', 'Tích "Ghi chú", bỏ tích "Ngày duyệt".', 'Bấm Lưu.'], '—',
      ['Báo "Cập nhật thành công", cửa sổ đóng.', 'Bảng hiện cột Ghi chú, không còn cột Ngày duyệt.']),
    T('k_close', 'Đóng không lưu', 'P1', PRE_COL, ['Mở Tùy chỉnh cột.', 'Tích "Ghi chú".', 'Bấm Đóng (hoặc (x), hoặc bấm ra ngoài).'], '—',
      ['Cửa sổ đóng, không hỏi lại.', 'Bảng không có cột Ghi chú; mở lại cửa sổ thấy Ghi chú chưa tích.']),
    T('k_reload', 'Ghi nhớ cấu hình sau F5 và trên trình duyệt khác', 'P1', PRE_COL + '\nĐã lưu cấu hình: bật Ghi chú.',
      ['Nhấn F5.', 'Đăng nhập D trên trình duyệt khác, mở màn danh sách.'], '—',
      ['Cả 2 trường hợp bảng vẫn có cột Ghi chú (cấu hình lưu theo tài khoản, không theo trình duyệt).']),
    T('k_account', 'Cấu hình hiển thị theo từng tài khoản', 'P1', 'Tài khoản D đã bật cột Ghi chú; tài khoản A chưa tùy chỉnh.',
      ['Đăng nhập bằng A trên cùng máy.', MENU_SALE], '—', ['A thấy bộ cột mặc định (không có Ghi chú); cấu hình của D không ảnh hưởng A.']),
    T('k_nodata', 'Tùy chỉnh cột không ảnh hưởng dữ liệu và bộ lọc', 'P1', PRE_COL + '\nĐang lọc Trạng thái = Đã duyệt (215 phiếu), trang 2.',
      ['Mở Tùy chỉnh cột, bỏ tích "Người tạo", bấm Lưu.'], '—',
      ['Tổng số vẫn "/ 215", bộ lọc Đã duyệt giữ nguyên.', 'Dữ liệu phiếu không đổi; bật lại cột thì hiện đủ thông tin như cũ.']),
]

# ====================================================================== IX. XUẤT EXCEL
S_XLS = [
    T('x_open', 'Mở popup chọn trường, danh sách trường và trường chọn mặc định', 'P1', PRE_LIST,
      [MENU_SALE, 'Bấm Xuất Excel.'], '—',
      ['Cửa sổ "Chọn trường xuất Excel" liệt kê 11 trường: Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, '
       'Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối.',
       'Mặc định tích sẵn cả 11 trường, dòng "Đang chọn 11/11 trường".', 'Có nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng.']),
    T('x_default', 'Xuất với trường mặc định', 'P0', PRE_LIST, [MENU_SALE, 'Bấm Xuất Excel.', 'Bấm Xuất file (không đổi gì).'], '—',
      ['Tải file có 12 cột: STT + 11 trường theo đúng thứ tự trong cửa sổ.', 'Báo "Xuất Excel thành công", cửa sổ đóng.']),
    T('x_all', 'Chọn tất cả trường', 'P1', PRE_LIST, ['Bấm Xuất Excel.', 'Bấm Bỏ chọn hết, rồi Chọn tất cả.', 'Bấm Xuất file.'], '—',
      ['Dòng đếm "Đang chọn 11/11 trường"; file đủ 12 cột.']),
    T('x_some', 'Một số trường, theo thứ tự đã chọn', 'P0', PRE_LIST + '\nLọc Trạng thái = Đã duyệt (215 phiếu).',
      ['Bấm Xuất Excel.', 'Bỏ chọn hết, tích Mã phiếu, Trạng thái, Người tạo; kéo để Trạng thái đứng đầu.', 'Bấm Xuất file.'], '—',
      ['File có 4 cột theo thứ tự STT, Trạng thái, Mã phiếu, Người tạo.', 'Số dòng dữ liệu = 215.', 'Báo "Xuất Excel thành công".']),
    T('x_none', 'Không chọn trường nào', 'P0', PRE_LIST, ['Bấm Xuất Excel.', 'Bấm Bỏ chọn hết.'], '—',
      ['Dòng đếm "Đang chọn 0/11 trường".', 'Nút Xuất file mờ, bấm không có tác dụng.']),
    T('x_search', 'Xuất theo từ khóa tìm kiếm', 'P1', PRE_LIST + '\nCó 8 phiếu PYCXHM-00360 đến PYCXHM-00367.',
      ['Nhập "0036" vào ô tìm nhanh, bấm Tìm kiếm.', 'Xuất Excel với trường mặc định.'], 'Ô tìm nhanh: 0036',
      ['File có đúng 8 dòng phiếu PYCXHM-00360 đến PYCXHM-00367.']),
    T('x_filter', 'Xuất theo bộ lọc có Ngày tạo', 'P0', PRE_LIST + '\nCó 4 phiếu tạo từ 01/10/2026 tới 05/10/2026.',
      ['Lọc Ngày tạo 01/10/2026 – 05/10/2026.', 'Xuất Excel với trường mặc định.'], 'Ngày tạo: 01/10/2026 – 05/10/2026',
      ['File có 4 dòng phiếu.', 'Dòng 2 của file ghi "Từ ngày 01/10/2026 đến ngày 05/10/2026".']),
    T('x_pages', 'Xuất toàn bộ khi danh sách nhiều trang', 'P0', PRE_LIST + '\nĐang xem trang 3, 10 dòng / trang.',
      ['Bấm Xuất Excel, Xuất file.'], '—',
      ['File có đủ 364 dòng phiếu (không chỉ 10 dòng trang đang xem).', 'Số dòng khớp N ở dòng "Hiển thị".']),
    T('x_empty', 'Xuất khi danh sách rỗng', 'P2', PRE_LIST + '\nĐang tìm "XYZ999" (không có kết quả).', ['Bấm Xuất Excel, Xuất file.'], '—',
      ['Vẫn tải file có dòng tiêu đề "DANH SÁCH PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN" và dòng tên cột, không có dòng dữ liệu.']),
    T('x_name', 'Tên file và định dạng file', 'P1', PRE_LIST, ['Xuất Excel với trường mặc định.', 'Mở file bằng Excel.'], '—',
      ['Tên file "danh_sach_yeu_cau_xuat_hang_muon.xlsx".', 'File .xlsx mở được, trang tính tên "Yêu cầu xuất hàng mượn".']),
    T('x_header', 'Tiêu đề và tiêu đề cột trong file', 'P1', PRE_LIST, ['Xuất Excel với trường mặc định.', 'Mở file.'], '—',
      ['Dòng 1: "DANH SÁCH PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN" (in đậm, gộp ô).',
       'Dòng tên cột: STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, '
       'Phòng ban, Ghi chú, Lý do từ chối; dòng tiêu đề được cố định khi cuộn.']),
    T('x_match', 'Dữ liệu trong file khớp danh sách', 'P0', 'Phiếu PYCXHM-00290 Đã duyệt: người tạo Nguyễn Văn A, duyệt bởi '
      'Cao Thị Thùy Linh lúc 22/10/2026 09:15.', ['Xuất Excel với trường mặc định.', 'Tìm dòng PYCXHM-00290 trong file.'], '—',
      ['Các ô khớp đúng danh sách: Người tạo "Nguyễn Văn A", Trạng thái "Đã duyệt", Người duyệt "Cao Thị Thùy Linh", Ngày duyệt '
       '"22/10/2026 09:15".']),
    T('x_types', 'Định dạng ngày / chữ trong file', 'P2', PRE_LIST, ['Xuất Excel với trường mặc định.', 'Mở file, xem cột Mã phiếu, Ngày tạo.'],
      '—', ['Mã phiếu là chữ, không bị Excel cảnh báo "số lưu dạng chữ".',
            'Ngày dạng "dd/mm/yyyy hh:mm" giữ nguyên trên mọi máy (không tự đổi theo cài đặt vùng).']),
    T('x_vn', 'Tiếng Việt và ký tự đặc biệt trong file', 'P2', 'Có phiếu Ghi chú "Xuất <b>gấp</b> & 100% @#", người tạo "Nguyễn Thị Ánh".',
      ['Xuất Excel có trường Ghi chú, Người tạo.', 'Mở file.'], '—',
      ['Tiếng Việt có dấu hiển thị đúng; Ghi chú hiện đúng nguyên văn, không lỗi phông.']),
    T('x_scope', 'Xuất Excel trong phạm vi quyền', 'P0', 'Tài khoản A (không có quyền nào), lập 3 phiếu.',
      ['Đăng nhập bằng A.', MENU_SALE, 'Xuất file đủ 11 trường.'], '—', ['File chỉ có 3 phiếu của A.']),
]

# ====================================================================== X. ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU
S_IMPACT = [
    T('i_no_parent', 'Lập phiếu khi chưa có phiếu mượn nào', 'P1', 'Tài khoản F không có phiếu xuất mượn nào đang Đã mượn.',
      ['Đăng nhập bằng F.', MENU_SALE, 'Bấm Tạo mới, bấm "Thêm phiếu".'], '—',
      ['Cửa sổ hiện "Không có phiếu xuất mượn phù hợp.".', 'Không chọn được phiếu nên không gửi được phiếu.']),
    T('i_flow_approve', 'Luồng đầy đủ: lập đến duyệt', 'P0', PRE_A + '\n' + PRE_KT,
      ['A lập phiếu xuất 5 cái ENEO-408-V5041, gửi duyệt.',
       'B mở lối vào Kế toán kho, lọc Chờ duyệt, Tạo phiếu xuất hàng mượn, Lưu và duyệt.', 'A mở lại phiếu.'], '—',
      ['Bước 1: B nhận thông báo.', 'Bước 3: phiếu tự chuyển Đã duyệt, Được duyệt = 5; A nhận thông báo Đã duyệt.',
       'Lập phiếu mới với PYCXH-TEST-023: Đang mượn của hàng đó giảm còn 41.']),
    T('i_appear', 'Phiếu vừa tạo xuất hiện ở màn Phiếu xuất hàng mượn', 'P0', PRE_A + '\n' + PRE_KT,
      ['A gửi phiếu yêu cầu mới.', 'B vào phân hệ Tài chính > "Hàng hoá - Dịch vụ - Vận chuyển" > "Mượn hàng" > "Phiếu xuất hàng mượn", '
       'bấm Tạo mới, mở ô chọn phiếu yêu cầu.'], '—',
      ['Phiếu yêu cầu vừa gửi có trong danh sách chọn (chỉ phiếu Chờ duyệt).']),
    T('i_hold', 'Phiếu Chờ duyệt giữ chỗ số lượng ở màn khác', 'P0', PRE_A + '\nA gửi phiếu xuất 10 cái, còn Chờ duyệt.',
      ['A lập Yêu cầu xuất bán hàng mượn (phân hệ Tài chính > Mượn hàng) với cùng phiếu mượn, cùng hàng.'], '—',
      ['Số còn mượn ở màn đó đã trừ 10 của phiếu yêu cầu xuất hàng mượn đang Chờ duyệt (còn 36).']),
    T('i_picker_after', 'Phiếu đã duyệt không còn được chọn để duyệt lại', 'P1', PRE_KT + '\nPhiếu PYCXHM-00340 vừa Đã duyệt.',
      ['B vào màn Phiếu xuất hàng mượn, bấm Tạo mới, mở ô chọn phiếu yêu cầu, tìm PYCXHM-00340.'], '—',
      ['Không còn PYCXHM-00340 trong danh sách chọn (danh sách tự cập nhật theo trạng thái).']),
    T('i_rename', 'Đổi tên hàng trong danh mục sau khi đã lập phiếu', 'P2',
      'Phiếu PYCXHM-00337 có hàng "Dầu nhớt Eneo 0.8L"; quản trị đổi tên hàng trong danh mục thành "Dầu nhớt Eneo Can 0.8L".',
      ['Mở chi tiết PYCXHM-00337.', 'Lập phiếu mới, thêm cùng hàng.'], '—',
      ['Phiếu cũ vẫn hiện tên lúc lập "Dầu nhớt Eneo 0.8L" (chứng từ lưu tên, đơn giá tại thời điểm lập).',
       'Phiếu mới hiện tên mới "Dầu nhớt Eneo Can 0.8L".']),
    T('i_child_parent', 'Dòng chi tiết thuộc đúng phiếu mượn', 'P0',
      'A có PYCXH-TEST-023 (có ENEO-408-V5041) và PYCXH-TEST-025 (không có ENEO-408-V5041).',
      TAO + ['Chọn cả 2 phiếu.', 'Thêm ENEO-408-V5041, nhập Xuất = 5, gửi duyệt.', 'Mở chi tiết.'], '—',
      ['Dòng hàng chỉ có 1 dòng con Phiếu mượn = PYCXH-TEST-023 (không có dòng con PYCXH-TEST-025).']),
    T('i_ref_keep', 'Tham chiếu giữ nguyên sau khi đổi trạng thái', 'P0', 'Phiếu PYCXHM-00291 vừa bị từ chối.',
      ['Mở chi tiết PYCXHM-00291.', 'Bấm thẻ phiếu mượn.'], '—',
      ['Vẫn hiện đủ phiếu mượn, dòng hàng, file đính kèm như lúc gửi.', 'Thẻ phiếu mượn vẫn mở được chi tiết phiếu mượn.']),
    T('i_no_orphan', 'Không sinh phiếu dở dang khi gửi lỗi', 'P0', PRE_FORM_OK + '\nTổng số phiếu của A trước khi gửi = 3.',
      ['Lập phiếu, nhập Xuất bằng đúng Đang mượn.', 'Trước khi gửi, người khác gửi phiếu chiếm 10 cái cùng hàng.', 'A bấm Gửi duyệt, xác nhận.'],
      '—', ['A nhận "Số lượng vượt quá số đang mượn (n).".', 'Danh sách vẫn 3 phiếu: không có phiếu thiếu dòng hàng hay mã bị bỏ dở.']),
    T('i_flow_reject', 'Luồng đầy đủ: lập đến từ chối đến lập lại', 'P0', PRE_A + '\n' + PRE_KT,
      ['A gửi phiếu Xuất 5.', 'B từ chối với lý do "Sai số lượng".', 'A lập phiếu mới cùng phiếu mượn.'], '—',
      ['Bước 2: A nhận thông báo kèm lý do; phiếu cũ không sửa được.', 'Bước 3: Đang mượn trở lại 46 như trước khi gửi.']),
]

# ====================================================================== XI. PHÂN QUYỀN
S_PERM = [
    T('p_create_all', 'Lập phiếu không cần quyền riêng', 'P0', 'Tài khoản A không có quyền nào; A có phiếu mượn PYCXH-TEST-023 Đã mượn.',
      ['Đăng nhập bằng A.', MENU_SALE, 'Bấm Tạo mới, lập và gửi phiếu hợp lệ.'], '—',
      ['Nút Tạo mới hiện; A gửi phiếu thành công.', 'A chỉ chọn được phiếu mượn do chính mình lập.']),
    T('p_history', 'Xem lịch sử phiếu trong phạm vi', 'P1', 'Tài khoản A không có quyền nào, lập phiếu PYCXHM-00301.',
      ['Đăng nhập bằng A.', MENU_SALE, 'Bấm Lịch sử ở dòng PYCXHM-00301.'], '—',
      ['Mở được cửa sổ Lịch sử (không cần quyền riêng).', 'A chỉ thấy nút Lịch sử ở các phiếu nằm trong danh sách của mình.']),
    T('p_revoke', 'Bị gỡ quyền Kế toán kho giữa lúc thao tác', 'P0', PRE_KT + '\nB đang mở chi tiết PYCXHM-00338 Chờ duyệt.',
      ['Quản trị gỡ quyền Kế toán kho của B.', 'B (chưa tải lại trang) bấm Từ chối, nhập lý do, Xác nhận từ chối.'], 'Lý do: Sai số lượng',
      ['Báo "Phiếu không còn ở trạng thái Chờ duyệt hoặc bạn không đủ quyền.", cửa sổ không đóng.', 'Phiếu vẫn Chờ duyệt.',
       'Tải lại trang: không còn nút Tạo phiếu xuất hàng mượn và Từ chối.']),
]

# ====================================================================== XII. DUYỆT PHIẾU
PRE_APPROVE = PRE_KT + '\nPhiếu PYCXHM-00337 của A đang Chờ duyệt (Xuất 5 cái ENEO-408-V5041, Đang mượn 46).'
S_APPROVE = [
    T('a_btn', 'Điều kiện hiển thị nút Duyệt / Tạo phiếu xuất hàng mượn', 'P0',
      PRE_KT + '\nCó phiếu Chờ duyệt PYCXHM-00337, Đã duyệt PYCXHM-00290, Không duyệt PYCXHM-00291.',
      ['Đăng nhập bằng B.', MENU_KT, 'Quan sát cột Hành động 3 phiếu.', 'Mở chi tiết từng phiếu.'], '—',
      ['Chỉ PYCXHM-00337 có nút Duyệt ở cột Hành động.', 'Chỉ chi tiết PYCXHM-00337 có nút Tạo phiếu xuất hàng mượn và Từ chối.',
       'Tài khoản không có quyền Kế toán kho không thấy các nút này ở bất kỳ phiếu nào.']),
    T('a_row', 'Nút Duyệt trên dòng mở màn chi tiết', 'P1', PRE_APPROVE, [MENU_KT, 'Bấm nút Duyệt ở dòng PYCXHM-00337.'], '—',
      ['Mở màn chi tiết PYCXHM-00337 (nút Duyệt chỉ điều hướng, chưa ghi dữ liệu).']),
    T('a_ui', 'Giao diện duyệt: màn lập Phiếu xuất hàng mượn', 'P1', PRE_APPROVE,
      ['Mở chi tiết PYCXHM-00337, bấm Tạo phiếu xuất hàng mượn.', 'Bấm Lưu và duyệt.'], '—',
      ['Màn lập Phiếu xuất hàng mượn mở với phiếu yêu cầu PYCXHM-00337 và các dòng hàng điền sẵn.',
       'Chân màn có Lưu và duyệt, Lưu và tiếp tục, Quay lại.',
       'Lưu ý: bấm Lưu và duyệt là duyệt luôn, KHÔNG có hộp xác nhận duyệt riêng.']),
    T('a_ok', 'Duyệt thành công và trạng thái sau duyệt', 'P0', PRE_APPROVE,
      ['Mở chi tiết, bấm Tạo phiếu xuất hàng mượn.', 'Ở màn Lập phiếu xuất hàng mượn giữ số Xuất = 5, bấm Lưu và duyệt.',
       'Quay về màn Yêu cầu xuất hàng mượn, mở PYCXHM-00337.'], '—',
      ['Báo "Thao tác thành công.".', 'Phiếu yêu cầu Đã duyệt (nhãn xanh lá), Người duyệt = B, Ngày duyệt = lúc lưu.',
       'Cột Được duyệt = 5; không còn nút Tạo phiếu xuất hàng mượn, Từ chối.']),
    T('a_required', 'Thiếu dữ liệu bắt buộc khi duyệt', 'P0', PRE_APPROVE,
      ['Mở màn Lập phiếu xuất hàng mượn từ PYCXHM-00337.', 'Xóa số ở ô Xuất (về 0).', 'Bấm Lưu và duyệt.'], 'Xuất: 0',
      ['Báo "Bạn chưa nhập đầy đủ thông tin."; chữ đỏ "Phải lớn hơn 0" dưới ô Xuất.', 'Phiếu yêu cầu vẫn Chờ duyệt.']),
    T('a_rule', 'Điều kiện nghiệp vụ khi duyệt: không vượt số đang mượn', 'P0', PRE_APPROVE,
      ['Mở màn Lập phiếu xuất hàng mượn từ PYCXHM-00337.', 'Nhập Xuất = 47.', 'Bấm Lưu và duyệt.'], 'Xuất: 47',
      ['Chữ đỏ "Không được vượt quá 46" dưới ô; báo "Vui lòng kiểm tra lại thông tin đã nhập".', 'Không lưu, phiếu yêu cầu vẫn Chờ duyệt.']),
    T('a_effect', 'Ảnh hưởng tới dữ liệu liên quan sau duyệt', 'P0', PRE_APPROVE + '\nĐã duyệt PYCXHM-00337 bằng phiếu xuất PXHM-00121.',
      ['Mở danh sách Phiếu xuất hàng mượn.', 'A lập phiếu yêu cầu mới với PYCXH-TEST-023, thêm ENEO-408-V5041.'], '—',
      ['Bước 1: có PXHM-00121 gắn phiếu yêu cầu PYCXHM-00337.', 'Bước 2: Đang mượn còn 41 (đã xuất hẳn 5).']),
    T('a_notify', 'Thông báo gửi đúng người sau khi duyệt', 'P0', PRE_APPROVE, ['B duyệt PYCXHM-00337.', 'A và một nhân viên khác mở chuông thông báo.'],
      '—', ['A nhận "[YCXHM] Đã duyệt: PYCXHM-00337" kèm mã phiếu xuất và người duyệt.', 'Nhân viên khác không nhận.']),
    T('a_notify_link', 'Nội dung và điều hướng từ thông báo', 'P1', 'A vừa nhận thông báo Đã duyệt của PYCXHM-00337.',
      ['A bấm vào thông báo.'], '—', ['Mở màn "Chi tiết yêu cầu xuất hàng mượn: PYCXHM-00337", trạng thái Đã duyệt.']),
    T('a_cancel', 'Thoát màn phiếu xuất không lưu', 'P0', PRE_APPROVE, ['Bấm Tạo phiếu xuất hàng mượn.', 'Bấm Quay lại, chọn Thoát nếu được hỏi.'],
      '—', ['Phiếu yêu cầu vẫn Chờ duyệt, không có Người duyệt, lịch sử không thêm mốc.']),
    T('a_again', 'Không cho duyệt lại phiếu đã xử lý', 'P0', PRE_APPROVE + '\nB và B2 (cùng Kế toán kho) cùng mở màn lập phiếu xuất từ PYCXHM-00337.',
      ['B bấm Lưu và duyệt thành công.', 'B2 bấm Lưu và duyệt.', 'B2 mở lại đường dẫn lập phiếu xuất của PYCXHM-00337.'], '—',
      ['Bước 2: B2 nhận "Không thể duyệt yêu cầu này!", không tạo phiếu xuất thứ 2.',
       'Bước 3: báo "Phiếu yêu cầu này không ở trạng thái chờ duyệt hoặc bạn không có quyền duyệt.".']),
    T('a_hist', 'Ghi nhận người duyệt, thời gian duyệt và lịch sử', 'P0', PRE_APPROVE + '\nB duyệt lúc 02/11/2026 10:30.',
      ['Mở danh sách, xem dòng PYCXHM-00337.', 'Bấm Lịch sử.'], '—',
      ['Người duyệt = B, Ngày duyệt = 02/11/2026 10:30.',
       'Mốc "Duyệt": "Trạng thái: Chờ duyệt đến Đã duyệt", "Phiếu xuất hàng mượn: PXHM-…", người thực hiện B.']),
]

# ====================================================================== XIII. KHÔNG DUYỆT PHIẾU (chức năng "Từ chối")
S_REJECT = [
    T('j_btn', 'Điều kiện hiển thị nút Từ chối', 'P0', PRE_KT + '\nCó phiếu Chờ duyệt PYCXHM-00337 và Đã duyệt PYCXHM-00290.',
      ['Đăng nhập bằng B, mở chi tiết 2 phiếu.', 'Đăng nhập bằng A (người lập), mở chi tiết PYCXHM-00337.'], '—',
      ['B: chỉ PYCXHM-00337 có nút Từ chối (màu đỏ).', 'A: không có nút Từ chối.', 'Danh sách không có nút Từ chối trên dòng.']),
    T('j_ui', 'Giao diện cửa sổ Từ chối', 'P1', PRE_APPROVE, ['Mở chi tiết PYCXHM-00337.', 'Bấm Từ chối.'], '—',
      ['Cửa sổ "Từ chối yêu cầu xuất hàng mượn", dòng phụ "Mã phiếu: PYCXHM-00337".',
       'Ô Lý do từ chối (bắt buộc, gợi ý "Nhập lý do không duyệt phiếu..."); dòng nhắc "Phiếu sẽ chuyển sang trạng thái Không '
       'duyệt và không sửa lại được.".', 'Nút Xác nhận từ chối (đỏ), Đóng, (x).']),
    T('j_ok', 'Từ chối thành công: trạng thái và lý do', 'P0', PRE_APPROVE,
      ['Mở chi tiết, bấm Từ chối.', 'Nhập lý do "Sai số lượng", bấm Xác nhận từ chối.', 'Mở lại phiếu.'], 'Lý do: Sai số lượng',
      ['Báo "Thao tác thành công.", về danh sách đã mở.', 'Phiếu sang Không duyệt, Người duyệt = B, Ngày duyệt = lúc từ chối.',
       'Cột Lý do từ chối (bật hiển thị) và khối "Ghi chú duyệt" ở chi tiết ghi "Sai số lượng".']),
    T('j_empty', 'Bỏ trống lý do bắt buộc', 'P0', PRE_APPROVE,
      ['Mở chi tiết, bấm Từ chối.', 'Để trống lý do, bấm Xác nhận từ chối.', 'Nhập 3 dấu cách, bấm Xác nhận từ chối.'], 'Lý do: trống\nLý do: 3 dấu cách',
      ['Cả 2 lần: viền đỏ, "Bắt buộc phải nhập lý do từ chối"; cửa sổ không đóng; phiếu vẫn Chờ duyệt.']),
    T('j_max', 'Định dạng và giới hạn ký tự lý do', 'P1', PRE_APPROVE + '\nCó đoạn văn 300 ký tự.',
      ['Mở cửa sổ Từ chối.', 'Dán đoạn 300 ký tự.', 'Xóa bớt còn đúng 255 ký tự có dấu và ký tự đặc biệt "& % @", Xác nhận từ chối.'],
      'Lý do: 300 ký tự / 255 ký tự',
      ['Ô chỉ nhận tối đa 255 ký tự.', 'Lý do 255 ký tự lưu được, hiển thị đúng nguyên văn ở chi tiết.']),
    T('j_effect', 'Ảnh hưởng tới dữ liệu liên quan sau từ chối', 'P0', PRE_APPROVE,
      ['B từ chối PYCXHM-00337.', 'A lập phiếu mới với PYCXH-TEST-023, thêm ENEO-408-V5041.'], '—',
      ['Đang mượn trở lại 46 (phần 5 giữ chỗ của phiếu bị từ chối được trả lại).', 'Không có Phiếu xuất hàng mượn nào được tạo.']),
    T('j_notify', 'Thông báo gửi đúng người sau khi từ chối', 'P0', PRE_APPROVE, ['B từ chối PYCXHM-00337 lý do "Sai số lượng".',
                                                                                 'A mở chuông thông báo, bấm vào thông báo.'],
      '—', ['A nhận "[YCXHM] Từ chối: PYCXHM-00337" kèm người từ chối và lý do.', 'Bấm vào mở chi tiết phiếu, trạng thái Không duyệt.']),
    T('j_cancel', 'Hủy thao tác từ chối', 'P0', PRE_APPROVE, ['Mở cửa sổ Từ chối, nhập lý do.', 'Bấm Đóng (hoặc (x), hoặc bấm ra ngoài).'],
      '—', ['Cửa sổ đóng ngay, không hỏi lại.', 'Phiếu vẫn Chờ duyệt, không lưu lý do, lịch sử không thêm mốc.']),
    T('j_again', 'Không cho từ chối phiếu đã được xử lý', 'P0', 'B và B2 (cùng Kế toán kho) cùng mở chi tiết PYCXHM-00338 Chờ duyệt.',
      ['B từ chối thành công.', 'B2 bấm Từ chối, nhập lý do, xác nhận.'], '—',
      ['B2 nhận "Phiếu không còn ở trạng thái Chờ duyệt hoặc bạn không đủ quyền.", không lưu lý do của B2.']),
    T('j_hist', 'Ghi nhận người từ chối, thời gian và lịch sử', 'P0', PRE_APPROVE + '\nB từ chối lúc 02/11/2026 11:00.',
      ['Mở danh sách, xem dòng PYCXHM-00337.', 'Bấm Lịch sử.'], '—',
      ['Người duyệt = B, Ngày duyệt = 02/11/2026 11:00.',
       'Mốc "Từ chối": "Trạng thái: Chờ duyệt đến Không duyệt" kèm lý do, người thực hiện B.']),
]

# ====================================================================== XIV. IN (phần riêng của màn)
S_PRINT = [
    T('pr_one', 'In phiếu từ danh sách', 'P1', 'Phiếu PYCXHM-00337 có 2 dòng hàng, thuộc Chi nhánh Vinh.',
      ['Bấm biểu tượng In ở dòng PYCXHM-00337.'], '—',
      ['Cửa sổ "Xem trước phiếu PYCXHM-00337".', 'Tiêu đề "PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN", đúng số phiếu, ngày tạo, hàng hóa.']),
    T('pr_detail', 'In phiếu từ màn chi tiết', 'P2', 'Phiếu PYCXHM-00337.', ['Mở chi tiết PYCXHM-00337.', 'Bấm In.', 'Bấm In trong cửa sổ.'],
      '—', ['Cửa sổ xem trước mở ngay trên màn chi tiết.', 'Bấm In mở hộp thoại in của trình duyệt.']),
    T('pr_logo', 'Logo bản in theo công ty của phiếu', 'P1', 'Phiếu thuộc Chi nhánh Vinh; người in thuộc công ty khác.',
      ['In phiếu.'], '—', ['Đầu bản in là logo, tên của Chi nhánh Vinh.']),
    T('pr_list', 'In danh sách theo bộ lọc', 'P1', PRE_LIST + '\nLọc Trạng thái = Không duyệt (11 phiếu).', ['Bấm nút In trên bảng.'], '—',
      ['Cửa sổ "Xem trước danh sách yêu cầu xuất hàng mượn", khổ ngang, đúng 11 phiếu.']),
    T('pr_limit', 'In danh sách quá 2.000 phiếu', 'P2', 'Tài khoản tổng công ty, không lọc, hơn 2.000 phiếu.', ['Bấm In.'], '—',
      ['Không dựng bản in, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.']),
]

# Cài đặt bộ lọc thuộc nhóm II. Tìm kiếm và lọc (user 02/11/2026: không tách thành phần riêng)
S_FCFG = [
    T('f_open', 'Mở cửa sổ Cài đặt bộ lọc', 'P2', PRE_LIST, [MENU_SALE, 'Bấm Cài đặt bộ lọc.'], '—',
      ['Cửa sổ "Cài đặt bộ lọc" liệt kê 8 ô lọc đều đang tích: Công ty – Phòng ban, Mã phiếu, Trạng thái, Người tạo, Người duyệt, '
       'Mã hàng hóa, Tên hàng hóa, Ngày tạo.']),
    T('f_hide', 'Cài đặt bộ lọc: ẩn ô lọc', 'P1', PRE_LIST, ['Bấm Cài đặt bộ lọc.', 'Bỏ tích "Người duyệt".', 'Bấm Lưu.'], '—',
      ['Báo "Cập nhật thành công".', 'Ô Người duyệt không còn ở khối lọc.', 'Đăng xuất / đăng nhập lại vẫn giữ cấu hình.']),
    T('f_restore', 'Cài đặt bộ lọc: Khôi phục mặc định', 'P2', PRE_LIST + '\nĐã ẩn ô Người duyệt.',
      ['Bấm Cài đặt bộ lọc.', 'Bấm Khôi phục mặc định.', 'Bấm Lưu.'], '—', ['Đủ 8 ô lọc theo thứ tự ban đầu.']),
    T('f_close', 'Đóng cửa sổ Cài đặt bộ lọc không lưu', 'P2', PRE_LIST,
      ['Bấm Cài đặt bộ lọc.', 'Bỏ tích "Mã phiếu".', 'Bấm Đóng (hoặc (x), hoặc bấm ra ngoài).'], '—',
      ['Cửa sổ đóng, không hỏi lại; ô Mã phiếu vẫn hiện ở khối lọc.']),
]

# Một nhóm Phân quyền duy nhất (user 02/11/2026): khối phân quyền đầu file đưa vào XI, khóa r00..r10.
S_PERM[:0] = [('r' + c[0],) + tuple(c[1:]) for c in ROLE_TCS]
S_SEARCH += S_FCFG

SECTIONS_K = [
    ('I', 'HIỂN THỊ DANH SÁCH VÀ TRUY CẬP', S_LIST),
    ('II', 'TÌM KIẾM VÀ LỌC', S_SEARCH),
    ('III', 'THÊM MỚI', S_CREATE),
    ('IV', 'CHỈNH SỬA', S_EDIT),
    ('V', 'XÓA', S_DEL),
    ('VI', 'LỊCH SỬ THAY ĐỔI', S_HIS),
    ('VII', 'XEM CHI TIẾT', S_DETAIL),
    ('VIII', 'TÙY CHỈNH CỘT', S_COL),
    ('IX', 'XUẤT EXCEL', S_XLS),
    ('X', 'ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU', S_IMPACT),
    ('XI', 'PHÂN QUYỀN', S_PERM),
    ('XII', 'DUYỆT PHIẾU', S_APPROVE),
    ('XIII', 'KHÔNG DUYỆT PHIẾU', S_REJECT),
    ('XIV', 'IN PHIẾU VÀ IN DANH SÁCH', S_PRINT),
]
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV']

# Đánh số theo thứ tự trong section; ID[khóa] -> mã TC (gen_checklist.py dùng)
ID = {}
SECTIONS = []
for roman, title, cases in SECTIONS_K:
    out = []
    for i, c in enumerate(cases):
        key = c[0]
        assert key not in ID, 'Trùng khóa TC: %s' % key
        no = '%03d' % (i + 1)
        ID[key] = 'TC_%02d.%s' % (ROMAN.index(roman) + 1, no)
        out.append((no,) + tuple(c[1:]))
    SECTIONS.append((roman, title, out))
check_no_dash_pre(SECTIONS, [])

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name='Yêu cầu xuất hàng mượn - Cập nhật ngày %s' % NGAY,
          module_name='YC xuất hàng mượn', description_block=DESCRIPTION_BLOCK, role_tcs=[], sections=SECTIONS)
