# -*- coding: utf-8 -*-
"""Testcase "Báo cáo hàng có thể bán theo công ty" (HRM: phân hệ Thông báo > Tra cứu tồn kho > Hàng có thể bán theo công ty).

Viết mới theo code HRM hiện tại (02/11/2026) — màn không có TC cũ. Khuôn 17 cột (tc_engine), giọng tester.
Số liệu ví dụ lấy từ dev-hrm 02/11/2026 (công ty CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT); môi trường khác thì ghi số
thật vào cột Ghi chú.
Chạy: python gen_testcase.py
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _lib_report as R  # noqa: E402,F401  (đặt sys.path tới tc_engine)
from tc_engine import build  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

NGAY = R.L.NGAY
TEN = 'Báo cáo hàng có thể bán theo công ty'
MODULE = 'BC hàng có thể bán'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
COUNT = Counter()


def L_(*lines):
    return '\n'.join(lines)


def T(group, n, func, prio, pre, steps, data, exp):
    COUNT[group] += 1

    def j(x):
        return x if isinstance(x, str) else L_(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'Vào phân hệ Thông báo > nhóm Tra cứu tồn kho > bấm "Hàng có thể bán theo công ty"'
CTY = 'CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT'
GIUHANG = 'phân hệ Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Giữ hàng'
XUATHANG = 'phân hệ Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Xuất hàng'
NHAPHANG = 'phân hệ Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng'
DIEUCHUYEN = 'phân hệ Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Điều chuyển'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt:',
    '- TK-A: nhân viên công ty A (' + CTY + '), KHÔNG phải Super admin, không gán quyền gì thêm.',
    '- TK-B: nhân viên công ty B (vd CÔNG TY TNHH THIẾT BỊ TÂN PHÁT SÀI GÒN).',
    '- HH-TEST: một mặt hàng của công ty A có tồn tại 2 kho (vd kho PTT và LN), chưa có hàng giữ / gửi / đề nghị xuất kho. Ghi lại mã thật.',
    '- HH-DVT: mặt hàng có nhiều đơn vị tính (dev: TATE-TZ-03 — Cái / Vỉ x25 / Hộp x100).',
    '- HH-VE: mặt hàng có số ở cột Hàng đang về - Tồn kho (dev: ENEO-700-V5231, Tồn kho 726, 6 chứng từ).',
    '- Từ khóa mẫu "ENEO-AO" (dev: 5 mặt hàng áo ENEOS, đều ở kho PTT).',
    'Trước mỗi TC luồng phát sinh: lọc theo HH-TEST, chụp lại số nền của cả dòng (kể cả nhóm cột theo kho).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Báo cáo cho biết với MỘT công ty, tại các kho đang chọn, mỗi mặt hàng còn bán được bao nhiêu (SL tồn có thể bán), '
        'kèm tồn, hàng khuyến mại, hàng gửi, hàng giữ, hàng đang xuất, hàng đang về và số riêng từng kho.',
        'Chức năng: Xem báo cáo, Tìm kiếm / lọc, Đổi ĐVT trên dòng, Popup Hàng đang về, Xuất Excel, Tùy chỉnh cột. Màn chỉ đọc.',
        'Đường vào: ' + MENU + '.',
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Mỗi dòng = 1 mặt hàng có dòng tồn kho kế toán ở kho kế toán của công ty đang chọn (thuộc các kho đang lọc) và '
        'Tổng tồn + SL KM + Tổng gửi + SL trên đề nghị xuất kho chưa hoàn tất + Tổng giữ > 0.',
        'Cột: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn có thể bán, SL KM có thể xuất, Tổng tồn, '
        'Hàng đang về (KD đặt, Tồn kho), SL KM, Tổng gửi, Tổng giữ, Tổng đang xuất (Hàng bán, Hàng KM), mỗi kho 5 cột '
        '(SL tồn, SL KM, SL gửi, Đang xuất: Hàng bán, Hàng KM).',
        'Dòng Tổng ngay dưới tiêu đề: "Tổng (N mặt hàng, theo ĐVT cơ bản)".',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Mặt hàng chỉ có hàng đang về mà không có tồn / gửi / giữ / đang xuất: không hiện.',
        '- Đề nghị xuất kho đang tạo, đã hủy hoặc đã hoàn tất: không tính vào Tổng đang xuất.',
        '- Nhóm cột của kho có toàn số 0 ở dòng Tổng: ẩn.',
        '- Số 0 để trống; cột Tổng đang xuất - Hàng bán và các cột theo kho chỉ hiện số dương.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Báo cáo KHÔNG có bộ lọc thời gian: số liệu tức thời lúc tải. (Không có case ngày ngược chiều.)',
        'Riêng Hàng đang về chỉ tính đơn đặt hàng / chứng từ phát sinh sau 01/07/2024 (yêu cầu nhập hàng của cột KD đặt '
        'không giới hạn ngày).',
        'Bộ lọc được ghi nhớ 10 phút khi rời màn rồi quay lại (trừ ô Hàng hóa).',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Công ty > kho kế toán (gắn kho vật lý) > tồn từng mặt hàng. Một kho vật lý có thể có kho kế toán của nhiều công ty.',
        'Kho khuyến mại = kho kế toán công ty khai ở Khai Quy chế – Cấu hình.',
        'Tiêu đề bảng 3 tầng: nhóm Hàng đang về, Tổng đang xuất, từng kho (Đang xuất tách Hàng bán / Hàng KM).',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- SL tồn có thể bán = Tổng tồn − SL KM − Tổng gửi − Tổng giữ − Tổng đang xuất (Hàng bán); âm thì 0.',
        '- SL KM có thể xuất = SL KM − Tổng đang xuất (Hàng KM); âm thì 0.',
        '- Hàng bán đang xuất = SL cần xuất − Hàng KM − phần xuất từ hàng giữ − phần xuất từ hàng gửi.',
        '- Tổng giữ tính MỌI kho của công ty (không theo ô Kho). Hàng đang về tính TOÀN hệ thống (không theo công ty, kho).',
        '- Dòng Tổng = cộng mọi dòng khớp lọc (mọi trang), theo ĐVT cơ bản.',
    )),
    ('7. Phân quyền cấp', L_(
        '- Không có quyền riêng: ai đăng nhập cũng mở được, kể cả Xuất Excel.',
        '- Ô Tồn theo công ty mặc định công ty đang làm việc, chọn được MỌI công ty.',
        '- Menu chỉ ẩn khi phân hệ / mục bị tắt ở màn Cài đặt phân hệ.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Không có khối thống kê; chỉ có dòng Tổng và chân bảng "Hiển thị a–b / N".',
        'Số định dạng 1,234,567.89 (tối đa 2 số lẻ). Đổi ĐVT trên dòng: số = số cơ bản ÷ hệ số, làm tròn 2 số lẻ.',
        'Popup Hàng đang về: "Tổng SL" = số đã bấm ở cột Tồn kho.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        DU_LIEU,
        'Bẫy dễ sai:',
        '- Ô tìm nhanh và ô Model chỉ lọc khi bấm Tìm kiếm / Enter; ô chọn lọc ngay.',
        '- Đổi công ty thì kho đã chọn bị bỏ.',
        '- Dòng Tổng không đổi khi đổi ĐVT trên dòng; tải lại bảng thì ĐVT về đơn vị cơ bản.',
        '- Bảng rộng: kéo thanh cuộn ngang để thấy các cột bên phải.',
    )),
]

# ------------------------------------------------------------------ PHÂN QUYỀN + PHẠM VI
ROLE_TCS = [
    T('Q', '00', 'Người dùng không gán quyền gì vẫn mở được báo cáo', 'P0',
      'TK-A không có quyền đặc biệt; phân hệ Thông báo đang bật',
      ['1. Đăng nhập TK-A', '2. ' + MENU],
      'TK-A',
      ['- Mở được màn, tiêu đề "Báo cáo hàng có thể bán theo công ty"',
       '- Có nút Xuất Excel và nút Cấu hình cột hiển thị; bảng có dữ liệu']),
    T('Q', '01', 'Ô Tồn theo công ty mặc định là công ty của người đăng nhập', 'P0',
      'TK-A thuộc công ty A, TK-B thuộc công ty B',
      ['1. Đăng nhập TK-A, mở báo cáo, bấm Tìm kiếm nâng cao', '2. Đăng nhập TK-B, làm lại bước 1'],
      'TK-A, TK-B',
      ['- TK-A: ô Tồn theo công ty = công ty A; tiêu đề bảng "Báo cáo hàng có thể bán theo công ty — <tên công ty A>"',
       '- TK-B: ô = công ty B, số liệu khác TK-A']),
    T('Q', '02', 'Chọn được và xem được số của công ty khác', 'P0',
      'Đăng nhập TK-A',
      ['1. Mở báo cáo, bấm Tìm kiếm nâng cao', '2. Mở ô Tồn theo công ty, chọn công ty B'],
      'Công ty B',
      ['- Ô liệt kê mọi công ty đang hoạt động (dev: 6 công ty)',
       '- Chọn công ty B: bảng tải lại, tiêu đề đổi sang tên công ty B, số khớp khi TK-B tự xem (TC-ROLE-01)',
       '- Ghi nhận: báo cáo không giới hạn công ty theo người xem']),
    T('Q', '03', 'Tắt phân hệ / mục menu ở Cài đặt phân hệ thì không vào được', 'P2',
      'Người quản trị tắt mục "Hàng có thể bán theo công ty" ở màn Cài đặt phân hệ',
      ['1. Đăng nhập TK-A', '2. Mở menu Thông báo > Tra cứu tồn kho', '3. Dán đường dẫn màn báo cáo đã lưu từ trước'],
      '',
      ['- Mục menu không hiện', '- Mở đường dẫn: chuyển sang trang báo chức năng không khả dụng',
       '- Dọn dữ liệu: bật lại mục menu']),
    T('Q', '04', 'Mở chứng từ từ popup tuân theo quyền của màn đích', 'P2',
      'TK-A không có quyền xem Yêu cầu nhập hàng; HH-VE có dòng chứng từ yêu cầu nhập hàng / đề nghị nhập kho',
      ['1. Đăng nhập TK-A, mở popup Hàng đang về của HH-VE', '2. Bấm số phiếu của dòng đề nghị nhập kho (PDNNK-…)'],
      'HH-VE',
      ['- Tab mới mở màn chi tiết chứng từ', '- Không đủ quyền xem chứng từ thì màn đích báo không có quyền; popup báo cáo vẫn mở ở tab cũ']),
]

# ------------------------------------------------------------------ I. GIAO DIỆN
S1 = [
    T('UI', '001', 'Đường vào menu và tiêu đề trang', 'P1', '', ['1. ' + MENU, '2. Rê chuột vào ⓘ cạnh tiêu đề trang trên thanh đầu trang'], '',
      ['- Menu Tra cứu tồn kho có 3 mục: Hàng tồn lâu, Hàng có thể bán theo công ty, Báo cáo hàng gửi; chỉ mục giữa bấm được',
       '- Tiêu đề "Báo cáo hàng có thể bán theo công ty"',
       '- ⓘ: "Tra cứu số lượng hàng hóa còn có thể bán của một công ty tại các kho đã chọn (bỏ trống = mọi kho của công ty), kèm tồn, hàng gửi, hàng giữ, hàng đang xuất và hàng đang về."']),
    T('UI', '002', 'Bố cục mặc định khi mở màn', 'P1', 'Xóa bộ lọc đã ghi nhớ (bấm Làm mới) rồi rời màn > 10 phút', ['1. Mở báo cáo, không thao tác gì'], '',
      ['- Khu vực "Bộ lọc danh sách": ô tìm nhanh placeholder "Tìm theo tên, mã hoặc model hàng hóa", nút Tìm kiếm, Làm mới, Cài đặt bộ lọc, Tìm kiếm nâng cao; khu nâng cao đang thu gọn',
       '- Bảng 10 dòng/trang, sắp theo Tên hàng hóa tăng dần',
       '- Dòng đầu bảng là dòng Tổng "Tổng (N mặt hàng, theo ĐVT cơ bản)" nền xám, chữ đậm',
       '- Chân bảng "Hiển thị 1–10 / N", ô Số dòng/trang = 10']),
    T('UI', '003', 'Tiêu đề bảng gộp nhiều tầng', 'P1', 'Đang xem công ty A, không lọc kho', ['1. Quan sát tiêu đề bảng, kéo cuộn ngang tới hết'], '',
      ['- Nhóm "Hàng đang về" gồm KD đặt, Tồn kho; nhóm "Tổng đang xuất" gồm Hàng bán, Hàng KM',
       '- Mỗi kho có số liệu là 1 nhóm, tiêu đề là mã kho (rê chuột hiện "Mã - Tên kho"), 5 cột SL tồn, SL KM, SL gửi, Đang xuất (Hàng bán, Hàng KM)',
       '- Các nhóm kho xếp theo mã kho A→Z',
       '- Cuộn xuống: tiêu đề bảng dính trên cùng']),
    T('UI', '004', 'Icon ⓘ ở tiêu đề cột', 'P2', '', ['1. Rê chuột lần lượt vào ⓘ ở tiêu đề SL tồn có thể bán, Tổng giữ, Tồn kho'], '',
      ['- SL tồn có thể bán: "Số lượng còn có thể bán của công ty tại các kho đang lọc • SL tồn có thể bán = Tổng tồn − SL KM − Tổng gửi − Tổng giữ − Tổng đang xuất (Hàng bán). • Kết quả âm thì tính là 0."',
       '- Tổng giữ: "Tổng hàng đang giữ của công ty • Tính trên MỌI kho của công ty, không theo ô lọc Kho."',
       '- Tồn kho: có câu "Bấm số để xem danh sách chứng từ."',
       '- Rê / bấm icon không làm đổi sắp xếp cột']),
    T('UI', '005', 'Định dạng số và ô rỗng', 'P1', 'Lọc từ khóa ENEO-AO', ['1. Quan sát các ô số'], 'ENEO-AO',
      ['- Số có dấu phẩy ngăn hàng nghìn (vd 1,746), dấu chấm thập phân, tối đa 2 số lẻ',
       '- Ô bằng 0 để trống, không in 0 hay "-"',
       '- Cột số căn phải']),
    T('UI', '006', 'Thông báo bảng trống', 'P1', '', ['1. Tìm nhanh "zzzz-khong-co", bấm Tìm kiếm', '2. Xóa trống ô Tồn theo công ty (nút ×)'], 'zzzz-khong-co',
      ['- Bước 1: bảng "Không có dữ liệu phù hợp bộ lọc.", không có dòng Tổng, không có chân phân trang',
       '- Bước 2: bảng "Chọn công ty để xem báo cáo.", nút Xuất Excel ẩn']),
    T('UI', '007', 'Phân trang và STT', 'P2', 'Công ty A có > 20 mặt hàng', ['1. Đổi Số dòng/trang = 20', '2. Sang trang 2'], '',
      ['- Bước 1: về trang 1, 20 dòng', '- Bước 2: STT bắt đầu từ 21; "Hiển thị 21–40 / N"', '- Dòng Tổng không đổi giữa các trang']),
]

# ------------------------------------------------------------------ II. BỘ LỌC
S2 = [
    T('F', '001', 'Ô Tồn theo công ty bắt buộc', 'P0', '', ['1. Bấm Tìm kiếm nâng cao, bấm × ở ô Tồn theo công ty', '2. Bấm Tìm kiếm', '3. Chọn lại công ty A'], '',
      ['- Bước 1: bảng "Chọn công ty để xem báo cáo."',
       '- Bước 2: ô viền đỏ, chữ đỏ dưới ô "Vui lòng chọn tồn theo công ty", không tải dữ liệu',
       '- Bước 3: chữ đỏ tắt, bảng tải lại']),
    T('F', '002', 'Ô Kho chỉ liệt kê kho của công ty đang chọn', 'P1', '', ['1. Mở ô Kho khi đang chọn công ty A', '2. Đổi sang công ty B, mở lại ô Kho'], '',
      ['- Danh sách dạng "Mã - Tên kho", chỉ kho có kho kế toán của công ty đang chọn (dev công ty A: CSKH, DATD, HP, KTCN, LN, PTT, SG, SL)',
       '- Đổi công ty: danh sách đổi theo công ty mới', '- ⓘ cạnh nhãn Kho: "Bỏ trống = toàn bộ kho của công ty"']),
    T('F', '003', 'Lọc theo 1 kho / nhiều kho', 'P0', 'HH-TEST có tồn ở PTT và LN', ['1. Lọc HH-TEST', '2. Ô Kho chọn PTT', '3. Chọn thêm LN'], 'HH-TEST',
      ['- Bước 2: chỉ còn nhóm cột PTT; Tổng tồn = SL tồn của PTT',
       '- Bước 3: có 2 nhóm PTT, LN; Tổng tồn = PTT + LN',
       '- Tổng giữ KHÔNG đổi giữa các bước (tính mọi kho)']),
    T('F', '004', 'Đổi công ty thì bỏ kho đã chọn', 'P1', 'Đang chọn kho PTT', ['1. Đổi ô Tồn theo công ty sang công ty B'], '',
      ['- Ô Kho về trống', '- Bảng tải theo mọi kho của công ty B']),
    T('F', '005', 'Tìm nhanh theo tên / mã / model', 'P0', '', ['1. Gõ "ENEO-AO" (chưa bấm gì)', '2. Bấm Tìm kiếm', '3. Gõ "áo khoác", nhấn Enter', '4. Gõ "AOPHONG" (model), bấm Tìm kiếm'], '',
      ['- Bước 1: bảng chưa đổi', '- Bước 2: 5 mặt hàng áo ENEOS (dev), "Tổng (5 mặt hàng, theo ĐVT cơ bản)"',
       '- Bước 3: chỉ dòng Áo khoác ENEOS, không phân biệt hoa thường', '- Bước 4: các dòng có model chứa AOPHONG']),
    T('F', '006', 'Lọc Nhóm / Tính chất / Loại / Thương hiệu / Hãng sản xuất', 'P1', '', ['1. Lần lượt chọn 1 giá trị ở từng ô (mỗi lần Làm mới trước)', '2. Chọn 2 giá trị ở ô Thương hiệu'], 'Thương hiệu ENEOS, TAITEC',
      ['- Mỗi ô lọc ngay khi chọn, không cần bấm Tìm kiếm', '- Dòng nào cũng đúng giá trị đã chọn (đối chiếu cột Thương hiệu / danh mục hàng)',
       '- Chọn 2 thương hiệu: hiện hàng của cả 2']),
    T('F', '007', 'Ô Model chỉ lọc khi bấm Tìm kiếm', 'P2', '', ['1. Gõ "TZ-0" vào ô Model', '2. Bấm Tìm kiếm'], 'TZ-0',
      ['- Bước 1: bảng chưa đổi', '- Bước 2: chỉ hàng có model chứa "TZ-0"']),
    T('F', '008', 'Ô Hàng hóa tìm từ 2 ký tự', 'P1', '', ['1. Gõ 1 ký tự vào ô Hàng hóa', '2. Gõ "TATE-TZ"', '3. Chọn TATE-TZ-03'], '',
      ['- Bước 1: chưa có gợi ý', '- Bước 2: gợi ý dạng "Mã - Tên"', '- Bước 3: bảng còn đúng 1 dòng TATE-TZ-03']),
    T('F', '009', 'Kết hợp nhiều điều kiện', 'P1', '', ['1. Chọn kho PTT, thương hiệu ENEOS, tìm nhanh "ENEO-AO", bấm Tìm kiếm'], '',
      ['- Chỉ dòng thỏa ĐỒNG THỜI mọi điều kiện', '- Dòng Tổng = tổng các dòng đang hiện']),
    T('F', '010', 'Làm mới', 'P1', 'Đang lọc kho PTT, từ khóa ENEO-AO, đang chọn công ty B, sắp xếp Tổng tồn giảm dần',
      ['1. Bấm Làm mới'], '',
      ['- Ô công ty về công ty của người đăng nhập, mọi ô khác trống, bỏ sắp xếp', '- Bảng tải lại từ trang 1']),
    T('F', '011', 'Ghi nhớ bộ lọc 10 phút', 'P2', '', ['1. Lọc kho PTT, chọn Hàng hóa TATE-TZ-03', '2. Sang màn khác rồi quay lại trong 10 phút', '3. Quay lại sau hơn 10 phút'], '',
      ['- Bước 2: ô Kho còn PTT; ô Hàng hóa trống và bảng KHÔNG bị lọc theo hàng hóa', '- Bước 3: bộ lọc về mặc định']),
    T('F', '012', 'Cài đặt bộ lọc', 'P3', '', ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Hãng sản xuất", bấm Lưu', '3. Mở lại, bấm Khôi phục mặc định, Lưu'], '',
      ['- Cửa sổ "Cài đặt bộ lọc" liệt kê 9 ô: Tồn theo công ty, Kho, Nhóm hàng hóa, Tính chất hàng hóa, Loại hàng hóa, Thương hiệu, Hãng sản xuất, Model, Hàng hóa',
       '- Bước 2: ô Hãng sản xuất không còn ở khu nâng cao', '- Bước 3: hiện lại đủ 9 ô']),
]

# ------------------------------------------------------------------ III. SỐ LIỆU
S3 = [
    T('SL', '001', 'Công thức SL tồn có thể bán trên 1 dòng', 'P0', 'Lọc ENEO-AO', ['1. Đọc dòng Áo phông ENEOS, cuộn ngang để thấy đủ cột'], 'ENEO-AO',
      ['- Tổng tồn 805 − SL KM 581 − Tổng gửi 71 − Tổng giữ 0 − Hàng bán đang xuất 50 = 103 = SL tồn có thể bán (số dev 02/11/2026)']),
    T('SL', '002', 'SL tồn có thể bán âm thì ghi 0', 'P1', 'Có mặt hàng giữ nhiều hơn tồn (dev: CH-ER-BDCD, Tổng tồn 0, Tổng giữ 2)', ['1. Tìm nhanh CH-ER-BDCD'], 'CH-ER-BDCD',
      ['- Dòng vẫn hiện (vì có hàng giữ)', '- Ô SL tồn có thể bán trống (bằng 0), không hiện số âm']),
    T('SL', '003', 'Công thức SL KM có thể xuất', 'P0', 'Lọc ENEO-AO', ['1. Đọc dòng Áo phông ENEOS'], '',
      ['- SL KM 581 − Tổng đang xuất Hàng KM 86 = 495 = SL KM có thể xuất']),
    T('SL', '004', 'Dòng Tổng = tổng các dòng', 'P0', 'Lọc ENEO-AO (5 dòng, 1 trang)', ['1. Cộng tay từng cột của 5 dòng, so với dòng Tổng'], '',
      ['- SL tồn có thể bán: 59 + 38 + 105 + 15 + 103 = 320', '- Tổng tồn: 1,746; SL KM 1,170; Tổng gửi 156; Hàng bán 100; Hàng KM 86 (dev)',
       '- Mọi cột khác cũng khớp']),
    T('SL', '005', 'Dòng Tổng tính trên mọi trang', 'P0', 'Không lọc, N > 10', ['1. Ghi số dòng Tổng ở trang 1', '2. Sang trang cuối', '3. Xuất Excel, cộng cột trong file'], '',
      ['- Dòng Tổng giống nhau ở mọi trang', '- Bằng tổng cột trong file Excel (dòng Tổng cộng) và bằng cộng tay mọi dòng của file']),
    T('SL', '006', 'Tổng các kho = cột tổng', 'P1', 'HH-TEST có tồn ở 2 kho', ['1. Lọc HH-TEST, không chọn kho', '2. So nhóm cột từng kho với cột tổng'], '',
      ['- SL tồn các kho cộng lại = Tổng tồn', '- SL KM các kho = SL KM; SL gửi các kho = Tổng gửi', '- Hàng bán / Hàng KM đang xuất các kho = 2 cột Tổng đang xuất']),
    T('SL', '007', 'Tổng giữ không theo ô Kho', 'P0', 'HH-TEST có hàng giữ ở kho PTT (lập ở TC luồng V-001)', ['1. Lọc HH-TEST, ô Kho chọn LN (không chọn PTT)'], '',
      ['- Tổng giữ vẫn bằng số giữ ở PTT', '- SL tồn có thể bán = tồn LN − … − Tổng giữ (bị trừ cả hàng giữ ở PTT)']),
    T('SL', '008', 'Hàng đang về không theo công ty / kho', 'P1', 'HH-VE', ['1. Lọc HH-VE ở công ty A', '2. Đổi sang công ty B (nếu HH-VE có dòng)', '3. Chọn 1 kho bất kỳ'], 'HH-VE',
      ['- KD đặt và Tồn kho giống nhau ở mọi bước (dev: Tồn kho 726)']),
    T('SL', '009', 'Nhóm cột kho chỉ hiện kho có số liệu', 'P1', '', ['1. Lọc ENEO-AO', '2. Bỏ lọc'], '',
      ['- Bước 1: chỉ nhóm PTT (5 mặt hàng chỉ có ở PTT)', '- Bước 2: hiện các kho có số ≠ 0 ở dòng Tổng; kho toàn 0 không hiện']),
    T('SL', '010', 'Sắp xếp theo cột', 'P1', '', ['1. Bấm tiêu đề SL tồn có thể bán 3 lần', '2. Bấm Tổng tồn', '3. Bấm Tên hàng hóa, Model, Mã hàng, Thương hiệu'], '',
      ['- Lần 1 tăng dần, lần 2 giảm dần, lần 3 về theo Tên hàng hóa', '- Sắp xếp trên toàn kết quả, về trang 1; dòng Tổng không đổi',
       '- Các cột khác (KM, gửi, giữ, đang xuất, kho) không có biểu tượng sắp xếp']),
    T('SL', '011', 'Cột Hàng bán đang xuất chỉ hiện số dương', 'P2', '', ['1. Tìm mặt hàng có Hàng bán đang xuất ≤ 0 (đề nghị xuất toàn hàng giữ / gửi)'], '',
      ['- Ô trống, không hiện số âm', '- SL tồn có thể bán vẫn tính theo số thật (BR-04)']),
]

# ------------------------------------------------------------------ IV. ĐVT
S4 = [
    T('DVT', '001', 'Đổi ĐVT trên dòng', 'P0', 'HH-DVT (TATE-TZ-03)', ['1. Lọc TATE-TZ-03', '2. Ô ĐVT chọn "Hộp (x100)"', '3. Chọn "Vỉ (x25)"'], '',
      ['- Ô ĐVT có "Cái", "Vỉ (x25)", "Hộp (x100)"; mặc định Cái',
       '- Bước 2: SL tồn có thể bán 13,375 → 133.75; Tổng tồn 14,375 → 143.75; Tồn kho (đang về) 200 → 2; Hàng bán 1,000 → 10',
       '- Bước 3: 13,375 ÷ 25 = 535',
       '- Dòng Tổng giữ nguyên 13,375 / 14,375']),
    T('DVT', '002', 'Làm tròn 2 chữ số thập phân', 'P2', 'Mặt hàng có số không chia hết cho hệ số', ['1. Đổi sang đơn vị có hệ số lớn'], '',
      ['- Số hiện tối đa 2 chữ số thập phân (vd 0.09 khi 450 Cái đổi sang Thùng x5000)']),
    T('DVT', '003', 'Tải lại bảng thì ĐVT về đơn vị cơ bản', 'P2', 'Đang để Hộp ở TATE-TZ-03', ['1. Bấm Tìm kiếm'], '',
      ['- Ô ĐVT về Cái, số về đơn vị cơ bản']),
]

# ------------------------------------------------------------------ V. LUỒNG PHÁT SINH
S5 = [
    T('LP', '001', 'Phiếu xuất giữ làm tăng Tổng giữ, giảm SL có thể bán', 'P0', 'Có số nền HH-TEST; kho PTT còn ≥ 2',
      ['1. Vào ' + GIUHANG + ', lập Yêu cầu xuất giữ HH-TEST SL 2 tại kho PTT, duyệt', '2. Lập và duyệt Phiếu xuất giữ cho yêu cầu đó', '3. Quay lại báo cáo, lọc HH-TEST'], 'SL giữ: 2',
      ['- Tổng giữ tăng 2', '- SL tồn có thể bán giảm 2', '- Tổng tồn, nhóm cột PTT không đổi (hàng giữ không có cột riêng theo kho)']),
    T('LP', '002', 'Hủy hàng giữ trả lại SL có thể bán', 'P1', 'Đã làm LP-001',
      ['1. Vào ' + GIUHANG + ', lập Yêu cầu hủy hàng giữ cho 2 HH-TEST vừa giữ, duyệt, lập Phiếu hủy hàng giữ', '2. Lọc lại báo cáo'], '',
      ['- Tổng giữ giảm 2, SL tồn có thể bán tăng 2 (về số nền)']),
    T('LP', '003', 'Đề nghị xuất kho bán làm tăng Hàng bán đang xuất', 'P0', 'Có số nền mới',
      ['1. Vào ' + XUATHANG + ', lập Yêu cầu xuất hàng HH-TEST SL 3 tại kho PTT, duyệt', '2. Lập Đề nghị xuất kho cho yêu cầu đó, gửi duyệt (CHƯA xuất kho)', '3. Lọc lại báo cáo'], 'SL: 3',
      ['- Tổng đang xuất - Hàng bán tăng 3; nhóm PTT Đang xuất - Hàng bán tăng 3', '- SL tồn có thể bán giảm 3', '- Tổng tồn không đổi']),
    T('LP', '004', 'Đề nghị xuất kho đang tạo / đã hủy không tính', 'P1', 'Có số nền mới',
      ['1. Lập Đề nghị xuất kho HH-TEST SL 1 nhưng để ở trạng thái Đang tạo', '2. Lọc lại báo cáo', '3. Hủy đề nghị ở LP-003, lọc lại'], '',
      ['- Bước 2: không cột nào đổi', '- Bước 3: Hàng bán đang xuất giảm 3, SL tồn có thể bán tăng 3']),
    T('LP', '005', 'Xuất kho xong: tồn giảm, đang xuất về 0', 'P0', 'Đề nghị xuất kho HH-TEST SL 3 đang chờ (lập lại như LP-003)',
      ['1. Kho hoàn tất xuất kho / Phiếu xuất hàng cho đề nghị đó (hạch toán)', '2. Lọc lại báo cáo'], '',
      ['- Tổng tồn và SL tồn PTT giảm 3', '- Hàng bán đang xuất giảm 3', '- SL tồn có thể bán KHÔNG đổi so với lúc đang chờ xuất']),
    T('LP', '006', 'Đề nghị xuất khuyến mại (HĐ hãng) làm tăng Hàng KM đang xuất', 'P1', 'Công ty có kho khuyến mại có tồn HH-KM',
      ['1. Lập Yêu cầu xuất hàng loại Xuất khuyến mại (HĐ hãng) SL 1, duyệt, lập Đề nghị xuất kho', '2. Lọc lại báo cáo theo HH-KM'], 'SL: 1',
      ['- Tổng đang xuất - Hàng KM tăng 1; SL KM có thể xuất giảm 1', '- Hàng bán đang xuất không đổi', '- Dọn dữ liệu: hủy yêu cầu / đề nghị']),
    T('LP', '007', 'Phiếu nhập hàng làm tăng tồn', 'P0', 'Có số nền mới',
      ['1. Vào ' + NHAPHANG + ', lập Phiếu nhập hàng HH-TEST SL 5 vào kho PTT, hạch toán', '2. Lọc lại báo cáo'], 'SL: 5',
      ['- Tổng tồn, SL tồn PTT, SL tồn có thể bán cùng tăng 5']),
    T('LP', '008', 'Phiếu nhập hàng gửi làm tăng Tổng gửi, không tăng SL có thể bán', 'P1', 'Có số nền mới',
      ['1. Lập Phiếu nhập hàng loại Nhập hàng gửi HH-TEST SL 2 vào kho PTT, hạch toán', '2. Lọc lại báo cáo'], 'SL: 2',
      ['- Tổng gửi và SL gửi PTT tăng 2', '- Tổng tồn tăng 2', '- SL tồn có thể bán không đổi (tăng 2 tồn, trừ 2 gửi)']),
    T('LP', '009', 'Phiếu điều chuyển hàng giữa 2 kho', 'P1', 'Có số nền mới, không lọc kho',
      ['1. Vào ' + DIEUCHUYEN + ', lập Phiếu điều chuyển hàng HH-TEST SL 1 từ PTT sang LN, hoàn tất', '2. Lọc lại báo cáo'], '',
      ['- SL tồn PTT giảm 1, LN tăng 1', '- Tổng tồn và SL tồn có thể bán không đổi', '- Lọc riêng kho PTT: Tổng tồn giảm 1']),
    T('LP', '010', 'Yêu cầu nhập hàng mua trong nước làm tăng KD đặt', 'P1', 'Có số nền mới',
      ['1. Vào ' + NHAPHANG + ', lập Yêu cầu nhập hàng loại Mua hàng trong nước HH-TEST SL 4, gửi đề nghị (trạng thái Đã đề nghị)', '2. Lọc lại báo cáo'], 'SL: 4',
      ['- Hàng đang về - KD đặt tăng 4', '- Các cột tồn, SL tồn có thể bán không đổi', '- Sau khi hạch toán / hủy yêu cầu: KD đặt giảm lại 4']),
    T('LP', '011', 'Đơn đặt hàng (lập ở ERP) làm tăng Hàng đang về - Tồn kho', 'P2', 'Có sẵn đơn đặt hàng nhập khẩu đã duyệt của HH-TEST, SL đang về 10, phát sinh sau 01/07/2024 (đơn đặt hàng chỉ lập ở ERP)',
      ['1. Lọc HH-TEST, bấm số cột Tồn kho'], '',
      ['- Tồn kho có cả 10 của đơn đặt hàng', '- Popup có dòng số đơn đặt hàng kèm "(Phiếu gốc)" (nếu chưa có chứng từ tiếp theo), SL 10']),
]

# ------------------------------------------------------------------ VI. POPUP
S6 = [
    T('PU', '001', 'Mở popup Hàng đang về', 'P0', 'HH-VE', ['1. Lọc ENEO-700-V5231', '2. Bấm số 726 ở cột Hàng đang về - Tồn kho'], 'ENEO-700-V5231',
      ['- Popup tiêu đề "Hàng đang về", dòng phụ "ENEO-700-V5231 - Dầu nhớt động cơ Diesel 4 kỳ SAE 20W-50 CF-4 (18L)"',
       '- Cột: STT, Số phiếu, Số hợp đồng, SL, Ngày dự kiến về kho, Người tạo',
       '- 6 dòng (dev); chân popup "Tổng SL: 726" = số đã bấm']),
    T('PU', '002', 'Thứ tự dòng và "(Phiếu gốc)"', 'P1', 'Popup HH-VE đang mở', ['1. Quan sát cột Ngày dự kiến về kho và Số phiếu'], '',
      ['- Dòng có ngày xếp tăng dần (30/05/2026, 30/09/2026), dòng không ngày xuống cuối',
       '- Đơn đặt hàng chưa có chứng từ tiếp theo: số phiếu kèm chữ xám "(Phiếu gốc)"']),
    T('PU', '003', 'Mở chứng từ từ popup', 'P1', 'Popup HH-VE đang mở', ['1. Bấm số phiếu PDNNK-…', '2. Bấm số phiếu PDHTN-…'], '',
      ['- Bước 1: tab mới mở màn Đề nghị nhập kho của HRM đúng phiếu', '- Bước 2: tab mới mở chứng từ trên hệ thống ERP', '- Popup ở tab cũ vẫn mở']),
    T('PU', '004', 'Số 0 không bấm được', 'P2', '', ['1. Tìm dòng có cột Tồn kho trống'], '', ['- Ô trống, không có liên kết']),
    T('PU', '005', 'Popup không theo ĐVT đang chọn', 'P2', 'HH-DVT có hàng đang về', ['1. Đổi ĐVT dòng TATE-TZ-03 sang Hộp (Tồn kho hiện 2)', '2. Bấm số 2'], '',
      ['- Popup vẫn ghi SL theo chứng từ, "Tổng SL: 200"']),
    T('PU', '006', 'Tổng SL popup khớp cột trên nhiều mặt hàng', 'P1', '', ['1. Lấy 5 mặt hàng bất kỳ có số ở cột Tồn kho, mở popup từng dòng'], '',
      ['- Mỗi popup: Tổng SL = số đã bấm (đối chiếu dev 02/11/2026: 400/400 mặt hàng khớp)']),
    T('PU', '007', 'Phân trang và đóng popup', 'P3', 'Mặt hàng có > 10 chứng từ đang về', ['1. Sang trang 2 trong popup', '2. Bấm Đóng'], '',
      ['- STT nối tiếp; Tổng SL không đổi', '- Đóng popup, bảng báo cáo giữ nguyên bộ lọc và trang']),
]

# ------------------------------------------------------------------ VII. XUẤT EXCEL
S7 = [
    T('EX', '001', 'Cửa sổ chọn trường', 'P1', '', ['1. Bấm Xuất Excel'], '',
      ['- Cửa sổ "Chọn trường xuất Excel", dòng hướng dẫn "Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."',
       '- 16 trường đều tích sẵn, "Đang chọn 16/16 trường"', '- Bỏ chọn hết: nút Xuất file không bấm được']),
    T('EX', '002', 'Nội dung file đúng khuôn', 'P0', 'Lọc ENEO-AO', ['1. Bấm Xuất Excel > Xuất file', '2. Mở file'], '',
      ['- Toast "Xuất Excel thành công"; file bao_cao_hang_co_the_ban_theo_cong_ty.xlsx, trang tính "Tra cứu tồn kho"',
       '- Tiêu đề "TRA CỨU TỒN KHO THEO CÔNG TY", dòng "Kho: <mã các kho của công ty, cách nhau ;>"',
       '- Tiêu đề bảng 3 tầng như màn hình; dòng "Tổng cộng" đậm ngay dưới tiêu đề: 320 / 1,084 / 1,746 …',
       '- 5 dòng hàng khớp màn hình, ô 0 để trống; cuối file "Ngày…….Tháng…….Năm…….", "Người lập", "(Ký, họ tên)"']),
    T('EX', '003', 'Xuất mọi trang, đúng thứ tự sắp xếp', 'P1', 'Không lọc, sắp Tổng tồn giảm dần', ['1. Xuất file'], '',
      ['- Số dòng hàng trong file = N ở chân bảng', '- Thứ tự dòng giống màn hình']),
    T('EX', '004', 'Chọn trường và thứ tự cột', 'P2', '', ['1. Bỏ chọn hết, tích Mã hàng, Tên hàng hóa, SL tồn có thể bán; kéo Mã hàng lên đầu', '2. Xuất file'], '',
      ['- File có STT, Mã hàng, Tên hàng hóa, SL tồn có thể bán theo đúng thứ tự']),
    T('EX', '005', 'File theo ĐVT cơ bản', 'P2', 'Đổi ĐVT dòng TATE-TZ-03 sang Hộp', ['1. Xuất file'], '',
      ['- Cột ĐVT ghi "Cái", số 13,375 (không phải 133.75)']),
    T('EX', '006', 'Nhóm cột theo kho trong file', 'P2', 'Không lọc kho', ['1. Xuất file với trường Theo từng kho'], '',
      ['- Mỗi kho đang hiện nhóm cột trên màn có 5 cột trong file; kho bị ẩn trên màn (toàn 0) không có trong file']),
]

# ------------------------------------------------------------------ VIII. TÙY CHỈNH CỘT
S8 = [
    T('COT', '001', 'Ẩn nhóm cột', 'P2', '', ['1. Bấm Cấu hình cột hiển thị', '2. Bỏ tích "Tổng đang xuất (Hàng bán, Hàng KM)" và "Theo từng kho", bấm Lưu'], '',
      ['- Cửa sổ "Tuỳ chỉnh cột", "Đang chọn 15/15 cột"; STT, Tên hàng hóa, ĐVT, SL tồn có thể bán có biểu tượng khóa, không bỏ tích được',
       '- Lưu: toast "Cập nhật thành công", bảng mất 2 nhóm cột tương ứng, dòng Tổng vẫn khớp cột',
       '- Dọn dữ liệu: bấm Chọn tất cả, Lưu']),
    T('COT', '002', 'Đóng không lưu', 'P3', '', ['1. Bỏ tích Model, bấm Đóng'], '', ['- Cột Model vẫn hiện']),
]

# ------------------------------------------------------------------ IX. HIỆU NĂNG
S9 = [
    T('HN', '001', 'Thời gian tải khi không lọc', 'P1', 'Công ty A (dev: 6,119 mặt hàng), xóa bộ lọc đã ghi nhớ', ['1. Mở báo cáo, bấm giờ tới khi hiện dòng Tổng'], '',
      ['- Bảng hiện trong ≤ 7 giây (dev 02/11/2026: 4.4–6.6 giây gồm cả mở trang)', '- Trong lúc tải bảng hiện "Đang tải dữ liệu..."']),
    T('HN', '002', 'Chuyển trang / sắp xếp', 'P2', 'Như HN-001', ['1. Sang trang 2', '2. Sắp xếp Tổng tồn'], '', ['- Mỗi thao tác ≤ 4 giây (dev: khoảng 2–3 giây)']),
    T('HN', '003', 'Xuất Excel toàn bộ', 'P2', 'Không lọc, công ty A', ['1. Xuất file đủ 16 trường'], '', ['- File tải về trong ≤ 30 giây, không báo "Lỗi khi xuất Excel"', '- Trong lúc xuất nút Xuất Excel không bấm được']),
    T('HN', '004', 'Mở popup Hàng đang về', 'P3', '', ['1. Mở popup 5 mặt hàng'], '', ['- Mỗi popup ≤ 2 giây (dev: trung bình 0.4 giây)']),
]

SECTIONS = [
    ('I', 'GIAO DIỆN & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'SỐ LIỆU, DÒNG TỔNG & SẮP XẾP', S3),
    ('IV', 'ĐỔI ĐƠN VỊ TÍNH', S4),
    ('V', 'LUỒNG PHÁT SINH CHỨNG TỪ', S5),
    ('VI', 'POPUP HÀNG ĐANG VỀ', S6),
    ('VII', 'XUẤT EXCEL', S7),
    ('VIII', 'TÙY CHỈNH CỘT', S8),
    ('IX', 'HIỆU NĂNG', S9),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS,
          role_section_title='Phân quyền & phạm vi dữ liệu')
    print('Số TC theo nhóm:', dict(COUNT), 'tổng', sum(COUNT.values()))
