# -*- coding: utf-8 -*-
"""Testcase "Danh sách đăng ký khách hàng toàn công ty" — KHUÔN CHUẨN tab "13. DM quốc gia" (loại bao_cao).

Sinh bằng testcase-documenter/assets/tc_chuan.build_chuan (tự chạy check_tc — phải 0 lỗi). Khuôn mẫu:
sale-customer-debt-reports/docs/compare/gen_testcase.py. Giữ các case nghiệp vụ của TC cũ
(../gen_testcase.py, 19/10/2026 — bản đối chiếu 2 hệ thống) nhưng viết lại theo code HRM hiện tại, bỏ phần đối chiếu,
xếp lại theo nhóm chuẩn + checklist CHECKLIST_TC_SRS.xlsx tab Testcase.
Số liệu mẫu đọc trên dev-hrm ngày 18/11/2026 (capture.js).
Chạy: python gen_testcase.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
from tc_chuan import build_chuan  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

NGAY = '18/11/2026'
TEN = 'Danh sách đăng ký khách hàng toàn công ty'
MODULE = 'DS đăng ký KH toàn công ty'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
QUYEN = 'Xem danh sách khách hàng đã đăng ký'

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']


def _lines(x):
    if x is None:
        return []
    return [x] if isinstance(x, str) else list(x)


def _exp(x):
    out = []
    for s in _lines(x):
        s = s.strip()
        if s.startswith('- '):
            s = s[2:].strip()
        out.append('-  ' + s)
    return '\n'.join(out)


def C(func, prio, pre, steps, data, exp):
    assert prio in ('P0', 'P1', 'P2'), func
    return (func, prio, '\n'.join(_lines(pre)), '\n'.join(_lines(steps)), '\n'.join(_lines(data)), _exp(exp))


def sections(groups):
    return [(ROMAN[i], t, [('%03d' % (k + 1),) + c for k, c in enumerate(cs)]) for i, (t, cs) in enumerate(groups)]


def L_(*lines):
    return '\n'.join(lines)


MENU = 'Vào phân hệ CSKH trước bán > Báo cáo > nhóm Báo cáo thị trường > bấm "Danh sách đăng ký khách hàng toàn công ty"'
Q = 'Tài khoản TK-Q có quyền "%s".' % QUYEN
CO = 'TK-Q đang mở màn, chưa lọc; danh sách có 2,134 đăng ký (môi trường thử 18/11/2026).'
ADV = 'Bấm "Tìm kiếm nâng cao"'
TIM = 'Tìm theo khách hàng, người liên hệ, người đăng ký, số báo giá'
EMPTY = '"Không có dữ liệu phù hợp bộ lọc."'
FILE = 'danh_sach_dang_ky_khach_hang.xlsx'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn chỉ đọc: liệt kê mọi lượt nhân viên kinh doanh ĐĂNG KÝ giữ khách hàng / người liên hệ của TOÀN công ty, để biết khách nào '
        'đang được ai giữ, đến ngày nào, sinh từ báo giá nào. Không thêm, sửa, xóa, hủy đăng ký trên màn này.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Sắp xếp, Tùy chỉnh cột, Xuất Excel.',
        'Đường vào: ' + MENU + '.',
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Mọi lượt đăng ký khách hàng của mọi công ty, phòng ban, nhân viên — gồm cả Còn hạn và Hết hạn.',
        'Đăng ký sinh ra khi người lập báo giá hãng bấm "Đăng ký khách hàng" trên danh sách báo giá hãng (chức năng nằm ở hệ thống bán hàng '
        'hiện hành, chưa có trên HRM) — testcase coi các đăng ký này là dữ liệu có sẵn.',
        'Mỗi dòng: STT | Khách hàng đăng ký (dòng dưới chữ nghiêng nhỏ là người liên hệ, nếu có) | Ngày đăng ký (ngày giờ) | '
        'Thời hạn đăng ký (ngày) | Người đăng ký ("Mã phòng - Họ tên") | Số báo giá (liên kết) | Ghi chú.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Đăng ký đã bị HỦY: bị xóa hẳn, không còn trên danh sách (không chuyển thành Hết hạn).',
        '-  Lượt đăng ký bị chặn khi tạo (thiếu ghi chú, trùng người khác đang giữ…): không sinh dòng.',
        '-  Màn không có cột trạng thái, không có dòng tổng, không có nút Thêm / Sửa / Xóa / Hủy đăng ký.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Không có ô khoảng ngày. Ô "Thời hạn đăng ký" (Còn hạn / Hết hạn) so Thời hạn đăng ký với NGÀY hôm nay:',
        '-  Thời hạn đăng ký từ hôm nay trở đi: Còn hạn (hết hạn đúng hôm nay vẫn Còn hạn tới hết ngày).',
        '-  Thời hạn đăng ký trước hôm nay: Hết hạn.',
        'Bỏ trống ô = cả hai.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Danh sách phẳng, mỗi lượt đăng ký 1 dòng. Một khách hàng có thể có nhiều dòng (nhiều người đăng ký nối tiếp, hoặc nhiều người '
        'liên hệ khác nhau của cùng khách tổ chức).',
        '7 cột: STT | Khách hàng đăng ký | Ngày đăng ký | Thời hạn đăng ký | Người đăng ký | Số báo giá | Ghi chú. STT và Khách hàng '
        'đăng ký là cột khóa, đứng yên khi cuộn ngang.',
        'Mặc định xếp Ngày đăng ký giảm dần; sắp xếp được 2 cột Ngày đăng ký, Thời hạn đăng ký. Phân trang 10 dòng (5 / 10 / 20 / 50 / 100).',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        'Không cộng dồn, không gộp: 2 lượt đăng ký cùng khách là 2 dòng.',
        'Chống trùng nằm ở bước tạo đăng ký: cùng lúc chỉ MỘT người giữ đăng ký còn hạn cho cùng khách cá nhân / cùng người liên hệ của '
        'khách tổ chức. Đăng ký còn hạn của người khác chặn chọn khách đó ở Meeting, Dự án TKT, Báo giá trên HRM '
        '(thông báo "Đã có người đăng ký nên bạn không được phép chọn").',
    )),
    ('7. Phân quyền cấp', L_(
        '-  "%s": thấy mục menu, mở màn, xem TOÀN công ty, lọc, xuất Excel, tùy chỉnh cột. Quyền không chia mức phạm vi '
        '(không có mức Tổng công ty / Công ty / Phòng ban / Bộ phận).' % QUYEN,
        '-  Không có quyền: mục menu bị ẩn; mở bằng đường dẫn thì báo "Bạn không có quyền thực hiện chức năng này", bảng không có dữ liệu.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Không có ô thống kê, không có dòng tổng.',
        'Chân bảng "Hiển thị a–b / N": a, b là STT dòng đầu / cuối trang, N là tổng số đăng ký khớp bộ lọc.',
        'Ngày đăng ký dạng dd/mm/yyyy HH:mm; Thời hạn đăng ký dạng dd/mm/yyyy.',
        'Người đăng ký = "Mã phòng ban - Họ tên" theo hồ sơ HIỆN TẠI của nhân viên.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '-  Ô chữ (ô tìm nhanh, Khách hàng đăng ký, Số báo giá) chỉ lọc khi bấm Tìm kiếm / Enter; ô chọn (Thời hạn đăng ký, Người đăng ký) lọc ngay.',
        '-  Ô tìm nhanh tìm cả MÃ khách hàng (chữ gợi ý không nói); ô Khách hàng đăng ký chỉ tìm theo tên.',
        '-  Rời màn / F5 / tab mới: bộ lọc về trống (màn không ghi nhớ bộ lọc).',
        '-  Excel: mặc định tích 6/7 trường (Người liên hệ là cột riêng của file, không tích sẵn).',
        'Dữ liệu mẫu: TK-Q có quyền xem; TK-Z không có quyền; NV-A, NV-B là 2 nhân viên kinh doanh khác phòng có đăng ký; '
        'KH-CN khách cá nhân; KH-DN khách doanh nghiệp có người liên hệ LH1, LH2.',
        'Số liệu mẫu đọc trên môi trường thử 18/11/2026: tổng 2,134; Còn hạn 3 (cả 3 hết hạn đúng 18/11/2026); Hết hạn 2,131; '
        'từ khóa "TOYOTA" 72 dòng. Môi trường khác thì ghi số thật vào cột Ghi chú.',
    )),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
G1 = [
    C('Mở màn hình từ menu', 'P0', Q, ['1. Đăng nhập TK-Q', '2. ' + MENU], '',
      ['Mở đúng màn, tiêu đề trang và tiêu đề bảng "Danh sách đăng ký khách hàng toàn công ty"',
       'Bảng tự tải dữ liệu ngay, không cần bấm Tìm kiếm',
       'Nhóm Báo cáo thị trường có mục "Danh sách đăng ký khách hàng toàn công ty"']),
    C('Các nút chức năng được hiển thị', 'P1', Q, ['1. Mở màn', '2. Quan sát khung "Bộ lọc danh sách" và hàng nút trên bảng'], '',
      ['Có ô tìm nhanh chữ gợi ý "' + TIM + '", nút "Tìm kiếm", "Làm mới", "Cài đặt bộ lọc", "Tìm kiếm nâng cao"',
       'Khu vực ô lọc nâng cao đang thu gọn',
       'Trên bảng có nút "Xuất Excel" và nút biểu tượng cột (Cấu hình cột hiển thị)',
       'KHÔNG có nút Thêm mới, Sửa, Xóa, Hủy đăng ký ở bất kỳ đâu']),
    C('Các cột mặc định hiển thị', 'P0', Q, ['1. Mở màn', '2. Đọc tiêu đề cột từ trái sang phải'], '',
      ['Đủ 7 cột theo thứ tự: STT | Khách hàng đăng ký | Ngày đăng ký | Thời hạn đăng ký | Người đăng ký | Số báo giá | Ghi chú',
       'Ngày đăng ký và Thời hạn đăng ký có biểu tượng mũi tên sắp xếp']),
    C('Không có cột mặc định ẩn', 'P2', 'TK-Q chưa từng lưu cấu hình cột ở màn này.', ['1. Mở màn', '2. Bấm nút Cấu hình cột hiển thị', '3. Đếm số cột đang tích'], '',
      ['Dòng đếm "Đang chọn 7/7 cột" — mọi cột đều hiện mặc định']),
    C('Cột STT và Khách hàng đăng ký đứng yên khi cuộn ngang', 'P2', CO, ['1. Thu nhỏ cửa sổ trình duyệt để bảng có thanh cuộn ngang', '2. Kéo thanh cuộn sang phải'], '',
      ['STT và Khách hàng đăng ký vẫn đứng yên bên trái', 'Các cột còn lại trượt theo thanh cuộn']),
    C('Dữ liệu từng cột của 1 đăng ký có sẵn', 'P0',
      ['Có sẵn đăng ký của NV-A (phòng KD1) cho người liên hệ LH1 của khách KH-DN, từ báo giá hãng BG-01, ghi chú "Khách đã chốt phương án".',
       'Đã biết ngày giờ đăng ký và thời hạn của đăng ký này.'],
      ['1. Mở màn', '2. Gõ "BG-01" vào ô tìm nhanh, nhấn Enter', '3. Đọc từng cột của dòng'], 'Từ khóa: số báo giá BG-01',
      ['Khách hàng đăng ký: dòng trên "KH-DN" chữ thường, dòng dưới "LH1" chữ nhỏ nghiêng màu xám',
       'Ngày đăng ký đúng ngày giờ đăng ký, dạng dd/mm/yyyy HH:mm (vd 19/10/2026 16:00)',
       'Thời hạn đăng ký dạng dd/mm/yyyy (vd 18/11/2026)',
       'Người đăng ký "KD1 - <Họ tên NV-A>"', 'Số báo giá "BG-01" dạng liên kết gạch chân', 'Ghi chú "Khách đã chốt phương án"']),
    C('Khách hàng cá nhân không có dòng người liên hệ', 'P1', 'Có sẵn đăng ký của NV-A cho khách cá nhân KH-CN (không chọn người liên hệ).',
      ['1. Mở màn', '2. Gõ tên KH-CN vào ô tìm nhanh, nhấn Enter'], 'Từ khóa: tên KH-CN',
      ['Cột Khách hàng đăng ký hiện tên KH-CN ở dòng trên, KHÔNG có dòng người liên hệ chữ nghiêng',
       'Lưu ý: ô Khách hàng đăng ký KHÔNG được để trống tên khách']),
    C('Ghi chú dài, nhiều dòng, có ký tự đặc biệt', 'P1', 'Có sẵn đăng ký có ghi chú dài trên 300 ký tự, có xuống dòng và các ký tự & < > " /.',
      ['1. Mở màn, tìm đúng đăng ký đó', '2. Quan sát ô Ghi chú', '3. Rê chuột vào ô Ghi chú'], '',
      ['Ô Ghi chú hiện tối đa 2 dòng, phần còn lại bị ẩn, không đẩy vỡ bảng',
       'Rê chuột hiện đủ nội dung', 'Ký tự & < > " / hiển thị đúng chữ, không biến thành định dạng']),
    C('Danh sách không có dữ liệu', 'P1', 'Môi trường chưa có đăng ký nào (hoặc lọc ra 0 dòng).', ['1. Mở màn', '2. Quan sát bảng và chân bảng'], '',
      ['Giữa bảng hiện ' + EMPTY, 'Chân bảng ghi "Không có đăng ký nào."', 'Không báo lỗi']),
    C('Không có dữ liệu phù hợp bộ lọc', 'P0', CO, ['1. Gõ chuỗi không tồn tại vào ô tìm nhanh', '2. Nhấn Enter'], 'Từ khóa: zzzkhongtontai999',
      ['Giữa bảng hiện ' + EMPTY, 'Chân bảng ghi "Không có đăng ký nào."']),
    # --- phân trang
    C('Số dòng mặc định mỗi trang và đổi số dòng', 'P0', CO, ['1. Đếm số dòng trang 1, đọc ô "Số dòng/trang:"', '2. Sang trang 2', '3. Đổi "Số dòng/trang:" sang 20'], '',
      ['Bước 1: mặc định 10, lựa chọn 5 / 10 / 20 / 50 / 100; trang 1 có đúng 10 dòng',
       'Bước 3: về trang 1, hiện 20 dòng, chân bảng "Hiển thị 1–20 / 2,134"', 'Tổng N không đổi khi đổi số dòng']),
    C('Nút sang trang kế tiếp và lùi về trang trước', 'P0', CO, ['1. Bấm nút ›', '2. Đọc chân bảng', '3. Bấm nút ‹'], '',
      ['Bước 1: sang trang 2, số 2 được tô màu; chân bảng "Hiển thị 11–20 / 2,134"', 'Bước 3: về trang 1, "Hiển thị 1–10 / 2,134"',
       'Dữ liệu 2 trang không lặp dòng']),
    C('Nút về trang cuối và về trang đầu', 'P1', CO, ['1. Bấm nút »', '2. Đọc chân bảng', '3. Bấm nút «'], '',
      ['Bước 1: tới trang cuối, chân bảng "Hiển thị 2,131–2,134 / 2,134"', 'Bước 3: về trang 1']),
    C('Trạng thái nút phân trang ở trang đầu và trang cuối', 'P1', CO, ['1. Ở trang 1 quan sát nút « và ‹', '2. Bấm » rồi quan sát nút › và »'], '',
      ['Trang 1: « và ‹ mờ, bấm không có tác dụng', 'Trang cuối: › và » mờ, bấm không có tác dụng']),
    C('STT liên tục giữa các trang', 'P1', CO, ['1. Đọc STT dòng cuối trang 1', '2. Sang trang 2, đọc STT dòng đầu'], '',
      ['Trang 1 kết thúc ở 10, trang 2 bắt đầu từ 11 (không đánh lại từ 1)']),
    C('Tổng số bản ghi ở chân bảng', 'P0', CO, ['1. Đọc chân bảng', '2. Bấm » về trang cuối, đếm số dòng trang cuối'], '',
      ['Chân bảng dạng "Hiển thị 1–10 / N", N từ 1,000 trở lên có dấu phẩy ngăn hàng nghìn (vd "/ 2,134")',
       'N = 10 × (số trang - 1) + số dòng trang cuối']),
    C('Đổi bộ lọc khi đang ở trang giữa thì về trang 1', 'P0', CO, ['1. Sang trang 3', '2. ' + ADV + ', chọn Thời hạn đăng ký = Hết hạn'], 'Thời hạn đăng ký: Hết hạn',
      ['Bảng về trang 1 theo kết quả lọc mới, chân bảng "Hiển thị 1–10 / 2,131"']),
    C('Đổi số dòng khi đang ở trang giữa thì về trang 1', 'P1', CO, ['1. Sang trang 5', '2. Đổi "Số dòng/trang:" sang 50'], '',
      ['Bảng về trang 1, hiện 50 dòng, chân bảng "Hiển thị 1–50 / 2,134"']),
    # --- sắp xếp
    C('Thứ tự mặc định: đăng ký mới nhất lên đầu', 'P0', CO, ['1. Mở màn, không bấm sắp xếp', '2. Đọc cột Ngày đăng ký 10 dòng đầu'], '',
      ['Ngày đăng ký giảm dần từ trên xuống (dòng 1 là đăng ký mới nhất, vd 19/10/2026 16:00)',
       'Hai đăng ký cùng thời điểm: đăng ký tạo sau đứng trên']),
    C('Sắp xếp tăng dần theo Thời hạn đăng ký', 'P0', CO, ['1. Bấm tiêu đề cột "Thời hạn đăng ký"'], '',
      ['Bảng về trang 1, Thời hạn đăng ký tăng dần (dòng 1 là thời hạn sớm nhất, vd 04/05/2023)', 'Mũi tên trên tiêu đề cột chỉ chiều tăng']),
    C('Sắp xếp giảm dần theo Thời hạn đăng ký', 'P0', CO, ['1. Bấm tiêu đề cột "Thời hạn đăng ký" 2 lần'], '',
      ['Thời hạn đăng ký giảm dần (dòng 1 là thời hạn muộn nhất, vd 18/11/2026)']),
    C('Sắp xếp theo Ngày đăng ký', 'P1', CO, ['1. Bấm tiêu đề cột "Ngày đăng ký"', '2. Bấm lại lần nữa'], '',
      ['Bước 1: Ngày đăng ký tăng dần (đăng ký cũ nhất lên đầu)', 'Bước 2: Ngày đăng ký giảm dần']),
    C('Các cột không cho sắp xếp', 'P2', CO, ['1. Bấm lần lượt tiêu đề STT, Khách hàng đăng ký, Người đăng ký, Số báo giá, Ghi chú'], '',
      ['Các tiêu đề này không có mũi tên sắp xếp', 'Bấm vào không làm đổi thứ tự dòng']),
    C('Giữ sắp xếp khi chuyển trang', 'P1', CO, ['1. Bấm tiêu đề "Thời hạn đăng ký" (tăng dần)', '2. Sang trang 2, trang 3'], '',
      ['Trang 2, 3 vẫn tiếp tục thứ tự Thời hạn đăng ký tăng dần, nối tiếp trang trước']),
    C('Đổi sắp xếp khi đang ở trang giữa thì về trang 1', 'P1', CO, ['1. Sang trang 4', '2. Bấm tiêu đề "Ngày đăng ký"'], '',
      ['Bảng về trang 1 theo thứ tự mới']),
]

# ================================================================== II. TÌM KIẾM & LỌC DANH SÁCH
G2 = [
    C('Tìm nhanh theo số báo giá chính xác', 'P0', CO, ['1. Gõ số báo giá đầy đủ vào ô tìm nhanh', '2. Nhấn Enter'], 'Từ khóa: BGBH_TPE_HN_KD1_26_4246',
      ['Còn đúng 1 dòng có Số báo giá BGBH_TPE_HN_KD1_26_4246', 'Chân bảng "Hiển thị 1–1 / 1"']),
    C('Tìm nhanh theo một phần số báo giá', 'P1', CO, ['1. Gõ phần cuối của số báo giá', '2. Nhấn Enter'], 'Từ khóa: KD1_26_4246',
      ['Ra dòng có số báo giá chứa chuỗi đó (BGBH_TPE_HN_KD1_26_4246)']),
    C('Tìm nhanh theo một phần tên khách hàng', 'P0', CO, ['1. Gõ từ khóa', '2. Nhấn Enter'], 'Từ khóa: TOYOTA',
      ['Chỉ còn các đăng ký có tên khách hàng (hoặc người liên hệ / người đăng ký / số báo giá) chứa "TOYOTA"', 'Chân bảng "/ 72" (số mẫu 18/11/2026)']),
    C('Tìm nhanh theo mã khách hàng', 'P1', 'Có khách hàng mã 29TPHPYE-1 có đăng ký.', ['1. Gõ mã khách hàng', '2. Nhấn Enter'], 'Từ khóa: 29TPHPYE-1',
      ['Ra các đăng ký của khách có mã chứa "29TPHPYE-1" (gồm cả mã 29TPHPYE-10, 29TPHPYE-11… nếu có)', 'Lưu ý: chữ gợi ý ô không nhắc tới mã nhưng vẫn tìm được theo mã']),
    C('Tìm nhanh theo tên người liên hệ', 'P1', CO, ['1. Gõ tên người liên hệ', '2. Nhấn Enter'], 'Từ khóa: Lương Thị Sâm',
      ['Ra đăng ký có người liên hệ "Lương Thị Sâm" (khách CÔNG TY TNHH TOYOTA HÀ ĐÔNG)']),
    C('Tìm nhanh theo họ tên người đăng ký', 'P1', CO, ['1. Gõ họ tên nhân viên', '2. Nhấn Enter'], 'Từ khóa: Đỗ Văn Sáng',
      ['Chỉ còn các đăng ký có Người đăng ký "… - Đỗ Văn Sáng"', 'Chân bảng "/ 25" (số mẫu 18/11/2026)']),
    C('Không phân biệt chữ hoa chữ thường', 'P1', CO, ['1. Gõ "toyota", nhấn Enter, ghi nhận', '2. Gõ "TOYOTA", nhấn Enter'], 'toyota / TOYOTA',
      ['Hai lần ra cùng số dòng (72)']),
    C('Tìm có dấu và không dấu', 'P2', CO, ['1. Gõ "Hoàng", nhấn Enter, ghi nhận', '2. Gõ "hoang", nhấn Enter'], 'Hoàng / hoang',
      ['Hai lần ra cùng tập kết quả (527 dòng, số mẫu 18/11/2026)']),
    C('Từ khóa không tồn tại', 'P1', CO, ['1. Gõ chuỗi không tồn tại', '2. Nhấn Enter'], 'Từ khóa: zzzkhongtontai999',
      ['Bảng hiện ' + EMPTY + ', chân bảng "Không có đăng ký nào."']),
    C('Tìm với ký tự đặc biệt', 'P2', CO, ['1. Gõ lần lượt từng chuỗi ở Test data, nhấn Enter, đọc chân bảng'], ['%', '_', "' OR 1=1 --", '<b>abc</b>'],
      ['Ký tự % và _ được hiểu là ký tự thường: chỉ ra đăng ký có chứa đúng ký tự đó, KHÔNG ra toàn bộ 2,134 dòng',
       'Không báo lỗi hệ thống, màn không treo, không hiện chữ in đậm']),
    C('Khoảng trắng đầu và cuối được bỏ qua', 'P1', CO, ['1. Gõ từ khóa có 2 dấu cách đầu và cuối, nhấn Enter', '2. Gõ lại không có dấu cách, nhấn Enter'], 'Từ khóa: "  TOYOTA  "',
      ['Hai lần ra cùng kết quả (72 dòng)']),
    C('Giới hạn độ dài ô tìm nhanh', 'P2', CO, ['1. Dán chuỗi 500 ký tự vào ô tìm nhanh', '2. Nhấn Enter'], 'Chuỗi "abcde" lặp lại 100 lần',
      ['Ô nhận đủ chuỗi, không báo lỗi', 'Bảng hiện ' + EMPTY + ', màn không treo']),
    C('Xóa từ khóa thì danh sách về đầy đủ', 'P0', 'Đang tìm nhanh "TOYOTA" (72 dòng).', ['1. Bấm nút × trong ô tìm nhanh', '2. Nhấn Enter / bấm Tìm kiếm'], '',
      ['Bước 1: ô trống, bảng chưa đổi', 'Bước 2: chân bảng về "/ 2,134", bảng về trang 1']),
    C('Gõ chưa nhấn Enter thì chưa lọc; Enter và nút Tìm kiếm cho cùng kết quả', 'P1', CO,
      ['1. Gõ từ khóa, KHÔNG nhấn Enter', '2. Nhấn Enter', '3. Gõ từ khóa khác, bấm nút Tìm kiếm'], 'TOYOTA / Hoàng',
      ['Bước 1: bảng chưa đổi', 'Bước 2: bảng lọc theo từ khóa, về trang 1', 'Bước 3: nút Tìm kiếm cho kết quả giống nhấn Enter']),
    C('Giá trị mặc định của các ô lọc', 'P1', CO, ['1. ' + ADV, '2. Quan sát 4 ô lọc'], '',
      ['Có 4 ô: Khách hàng đăng ký (chữ gợi ý "Nhập tên khách hàng"), Thời hạn đăng ký, Người đăng ký, Số báo giá (chữ gợi ý "Nhập số báo giá")',
       'Cả 4 ô đều trống; nút đổi thành "Ẩn tìm kiếm nâng cao"']),
    C('Lọc Khách hàng đăng ký theo tên', 'P0', CO, ['1. ' + ADV, '2. Nhập "TOYOTA" vào ô Khách hàng đăng ký', '3. Nhấn Enter'], 'Khách hàng đăng ký: TOYOTA',
      ['Chỉ còn đăng ký có TÊN khách hàng chứa "TOYOTA"',
       'Ô này KHÔNG tìm theo mã khách, người liên hệ, người đăng ký (khác ô tìm nhanh)']),
    C('Lọc Thời hạn đăng ký = Còn hạn', 'P0', 'Ngày test 18/11/2026; có 3 đăng ký thời hạn 18/11/2026, còn lại thời hạn trước ngày đó.',
      ['1. ' + ADV, '2. Chọn Thời hạn đăng ký = Còn hạn'], 'Thời hạn đăng ký: Còn hạn',
      ['Bảng lọc ngay khi chọn, không cần bấm Tìm kiếm', 'Còn 3 dòng, mọi Thời hạn đăng ký từ 18/11/2026 trở đi',
       'Đăng ký hết hạn đúng hôm nay vẫn được tính Còn hạn']),
    C('Lọc Thời hạn đăng ký = Hết hạn', 'P0', 'Như case trên.', ['1. ' + ADV, '2. Chọn Thời hạn đăng ký = Hết hạn'], 'Thời hạn đăng ký: Hết hạn',
      ['Còn 2,131 dòng, mọi Thời hạn đăng ký trước 18/11/2026', 'Còn hạn + Hết hạn = tổng khi không lọc (3 + 2,131 = 2,134)']),
    C('Lọc Người đăng ký', 'P0', 'NV-A có 5 đăng ký.', ['1. ' + ADV, '2. Bấm ô Người đăng ký, gõ tên NV-A, chọn'], 'Người đăng ký: NV-A',
      ['Bảng lọc ngay khi chọn', 'Chỉ còn 5 đăng ký, cột Người đăng ký đều là "<Mã phòng> - <Họ tên NV-A>"']),
    C('Lọc Số báo giá theo một phần số', 'P0', CO, ['1. ' + ADV, '2. Nhập "KD3_26" vào ô Số báo giá', '3. Nhấn Enter'], 'Số báo giá: KD3_26',
      ['Chỉ còn đăng ký có Số báo giá chứa "KD3_26" (cả báo giá thường và báo giá hãng)']),
    C('Lọc kết hợp nhiều tiêu chí', 'P0', CO,
      ['1. ' + ADV, '2. Chọn Thời hạn đăng ký = Hết hạn', '3. Chọn Người đăng ký = NV-A', '4. Gõ "TOYOTA" vào ô tìm nhanh, nhấn Enter'], '',
      ['Kết quả thỏa ĐỒNG THỜI cả 3 điều kiện', 'Số dòng nhỏ hơn hoặc bằng kết quả của từng điều kiện riêng lẻ']),
    C('Lọc kết hợp không có kết quả', 'P1', CO, ['1. Chọn Thời hạn đăng ký = Còn hạn', '2. Nhập Số báo giá "zzz", nhấn Enter'], '',
      ['Bảng hiện ' + EMPTY]),
    C('Phân trang và sắp xếp sau khi lọc', 'P1', CO, ['1. Chọn Thời hạn đăng ký = Hết hạn', '2. Bấm tiêu đề "Thời hạn đăng ký"', '3. Sang trang 2'], '',
      ['Chân bảng tính theo kết quả lọc ("/ 2,131")', 'Trang 2 vẫn giữ bộ lọc và thứ tự đã chọn']),
    C('Làm mới xóa mọi điều kiện', 'P0', 'Đang lọc Hết hạn + NV-A + từ khóa, đã sắp theo Thời hạn đăng ký, đang ở trang 2.',
      ['1. Bấm "Làm mới"'], '',
      ['Ô tìm nhanh và 4 ô lọc về trống', 'Bỏ sắp xếp, về Ngày đăng ký giảm dần', 'Bảng về trang 1, chân bảng "/ 2,134"']),
    C('Ẩn bớt ô lọc bằng Cài đặt bộ lọc', 'P2', CO, ['1. Bấm "Cài đặt bộ lọc"', '2. Quan sát cửa sổ', '3. Bấm "Đóng"'], '',
      ['Cửa sổ "Cài đặt bộ lọc" liệt kê 4 ô: Khách hàng đăng ký, Thời hạn đăng ký, Người đăng ký, Số báo giá; có nút Lưu, Khôi phục mặc định, Đóng',
       'Bấm Đóng không đổi khu vực lọc']),
    C('Rời sang màn khác rồi quay lại', 'P1', 'TK-Q đang lọc Thời hạn đăng ký = Hết hạn, từ khóa "TOYOTA".',
      ['1. Vào màn khác trên menu (vd CSKH trước bán > Báo cáo > Báo cáo phân chia thị trường)', '2. Quay lại màn bằng menu'], '',
      ['Ô tìm nhanh và ô lọc về trống, bảng hiện đủ 2,134 dòng, xếp mặc định']),
    C('Tải lại trang (F5) khi đang lọc', 'P1', 'TK-Q đang lọc Thời hạn đăng ký = Hết hạn.', ['1. Nhấn F5'], '',
      ['Bộ lọc về trống, bảng hiện đủ 2,134 dòng']),
    C('Mở màn ở tab trình duyệt mới khi tab cũ đang lọc', 'P2', 'Tab 1 đang lọc Còn hạn.', ['1. Mở tab mới, vào màn bằng menu', '2. Quay lại tab 1'], '',
      ['Tab 2: bộ lọc trống, đủ 2,134 dòng', 'Tab 1: giữ nguyên bộ lọc và kết quả đang xem']),
    C('Đăng xuất, đăng nhập tài khoản khác cùng trình duyệt', 'P1', 'TK-Q và TK-Q2 đều có quyền xem.',
      ['1. TK-Q mở màn, lọc Còn hạn', '2. Đăng xuất', '3. Đăng nhập TK-Q2, mở màn'], '',
      ['TK-Q2 thấy bộ lọc trống, không mang bộ lọc của TK-Q']),
]

# ================================================================== III. SỐ LIỆU BÁO CÁO
G3 = [
    C('Đăng ký mới hiện lên đầu danh sách', 'P0',
      ['NV-A vừa đăng ký người liên hệ LH2 của KH-DN từ báo giá hãng BG-02 (bấm "Đăng ký khách hàng" trên danh sách báo giá hãng, nhập ghi chú, Lưu).',
       'Trước đó chân bảng "/ N".'],
      ['1. TK-Q mở màn (hoặc bấm Làm mới)', '2. Đọc dòng 1 và chân bảng'], '',
      ['Dòng 1 là đăng ký vừa tạo: KH-DN / LH2, Người đăng ký NV-A, Số báo giá BG-02, đúng ghi chú đã nhập', 'Chân bảng tăng thành "/ N+1"']),
    C('Thời hạn đăng ký = Ngày đăng ký + số ngày cấu hình', 'P0', 'Cấu hình "Thời gian đăng ký khách hàng" đang đặt 30 ngày; NV-A đăng ký lúc 19/10/2026 16:00.',
      ['1. Tìm đăng ký vừa tạo', '2. So Ngày đăng ký và Thời hạn đăng ký'], '',
      ['Thời hạn đăng ký = 18/11/2026 (19/10/2026 + 30 ngày)']),
    C('Đổi cấu hình không làm đổi thời hạn đăng ký cũ', 'P1', 'Đăng ký cũ có thời hạn 18/11/2026; sau đó cấu hình đổi từ 30 sang 45 ngày.',
      ['1. Mở màn, tìm đăng ký cũ', '2. Tìm một đăng ký tạo SAU khi đổi cấu hình'], '',
      ['Đăng ký cũ giữ nguyên 18/11/2026', 'Đăng ký mới có thời hạn = ngày đăng ký + 45 ngày']),
    C('Hết hạn đúng hôm nay vẫn Còn hạn tới hết ngày', 'P0', 'Có đăng ký thời hạn = hôm nay (vd 18/11/2026), test lúc 17:00 cùng ngày.',
      ['1. Lọc Thời hạn đăng ký = Còn hạn', '2. Lọc Thời hạn đăng ký = Hết hạn'], '',
      ['Bước 1: đăng ký đó CÓ trong danh sách', 'Bước 2: đăng ký đó KHÔNG có', 'Sang ngày hôm sau, đăng ký đó chuyển sang nhóm Hết hạn']),
    C('Đăng ký bị hủy biến mất khỏi danh sách', 'P0', 'Đăng ký còn hạn của NV-A (BG-01) vừa được NV-A hủy ở màn danh sách khách hàng đã đăng ký của mình.',
      ['1. Mở màn, tìm "BG-01"', '2. Lọc Hết hạn, tìm "BG-01"'], '',
      ['Không còn dòng nào của đăng ký đó (bị xóa hẳn, không chuyển thành Hết hạn)', 'Chân bảng giảm 1']),
    C('Nhân viên đổi phòng thì Người đăng ký hiện phòng mới', 'P2', 'NV-B đăng ký khi ở phòng KD2, sau đó chuyển sang phòng KD3.',
      ['1. Mở màn, tìm đăng ký của NV-B'], '',
      ['Cột Người đăng ký ghi "KD3 - <Họ tên NV-B>" (theo hồ sơ hiện tại)', 'Không còn hiện mã phòng cũ KD2']),
    C('Nhân viên chưa có phòng ban', 'P2', 'Có đăng ký của nhân viên chưa được gán phòng ban.', ['1. Mở màn, tìm đăng ký đó'], '',
      ['Cột Người đăng ký chỉ ghi họ tên, không có dấu "-" thừa ở đầu']),
    C('Một khách nhiều người liên hệ là nhiều dòng', 'P1', 'KH-DN có đăng ký của NV-A cho LH1 và của NV-B cho LH2.', ['1. Gõ tên KH-DN vào ô tìm nhanh, nhấn Enter'], '',
      ['Có 2 dòng riêng: KH-DN / LH1 (NV-A) và KH-DN / LH2 (NV-B), không gộp']),
    C('Xem toàn công ty, không thu hẹp theo phòng ban', 'P0', 'TK-Q thuộc công ty 1 phòng KD1; có đăng ký của nhân viên phòng KD2, KD3 và của công ty khác.',
      ['1. Đăng nhập TK-Q, mở màn, không lọc', '2. Lọc Người đăng ký = 1 nhân viên phòng KD3'], '',
      ['Bước 1: thấy cả đăng ký của mọi phòng, mọi công ty', 'Bước 2: thấy đăng ký của nhân viên KD3']),
]

# ================================================================== IV. TÙY CHỈNH CỘT
G4 = [
    C('Mở cửa sổ Tuỳ chỉnh cột', 'P1', CO, ['1. Bấm nút biểu tượng cột cạnh Xuất Excel'], '',
      ['Cửa sổ "Tuỳ chỉnh cột", dòng hướng dẫn "Tích chọn cột cần hiển thị, kéo biểu tượng ba gạch để đổi thứ tự cột trên bảng."',
       'Danh sách 7 cột, dòng đếm "Đang chọn 7/7 cột", nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng']),
    C('Cột bắt buộc không ẩn được', 'P0', 'Đang mở cửa sổ Tuỳ chỉnh cột.', ['1. Thử bỏ tích STT, Khách hàng đăng ký', '2. Bấm Bỏ chọn hết'], '',
      ['STT và Khách hàng đăng ký có biểu tượng khóa, ô tích xám, không bỏ tích được', 'Bỏ chọn hết: còn 2/7 cột (2 cột khóa)']),
    C('Ẩn cột rồi lưu', 'P0', 'Đang mở cửa sổ Tuỳ chỉnh cột.', ['1. Bỏ tích Ghi chú, Người đăng ký', '2. Bấm Lưu'], '',
      ['Toast "Cập nhật thành công"', 'Bảng không còn 2 cột Ghi chú, Người đăng ký', 'Bộ lọc, trang đang xem và dữ liệu không đổi']),
    C('Hiện lại cột đã ẩn', 'P1', 'Đã ẩn Ghi chú.', ['1. Mở Tuỳ chỉnh cột, tích lại Ghi chú (hoặc Chọn tất cả)', '2. Bấm Lưu'], '',
      ['Cột Ghi chú hiện lại đúng vị trí', '"Đang chọn 7/7 cột"']),
    C('Kéo thả đổi thứ tự cột', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.', ['1. Kéo biểu tượng ba gạch của Ghi chú lên trên Ngày đăng ký', '2. Bấm Lưu'], '',
      ['Cột Ghi chú đứng ngay sau Khách hàng đăng ký trên bảng', 'STT, Khách hàng đăng ký vẫn đứng đầu (cột khóa không kéo được)']),
    C('Đóng không lưu', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.', ['1. Bỏ tích Số báo giá', '2. Bấm Đóng', '3. Mở lại cửa sổ'], '',
      ['Bảng vẫn có cột Số báo giá', 'Mở lại: Số báo giá vẫn được tích']),
    C('Cấu hình giữ sau F5 và theo từng tài khoản', 'P1', 'TK-Q đã ẩn cột Ghi chú và Lưu; TK-Q2 chưa chỉnh gì.',
      ['1. TK-Q nhấn F5', '2. TK-Q đăng nhập trên máy khác, mở màn', '3. TK-Q2 mở màn'], '',
      ['Bước 1, 2: cột Ghi chú vẫn ẩn', 'Bước 3: TK-Q2 vẫn thấy đủ 7 cột']),
]

# ================================================================== V. XUẤT DANH SÁCH EXCEL
G5 = [
    C('Mở cửa sổ chọn trường', 'P1', CO, ['1. Bấm "Xuất Excel"'], '',
      ['Cửa sổ "Chọn trường xuất file", dòng hướng dẫn "Tích chọn trường cần xuất, kéo biểu tượng ba gạch để đổi thứ tự cột trong file."',
       '7 trường: Khách hàng đăng ký, Ngày đăng ký, Thời hạn đăng ký, Người đăng ký, Số báo giá, Ghi chú, Người liên hệ']),
    C('Trường chọn mặc định theo cột đang hiện', 'P1', CO, ['1. Bấm "Xuất Excel"', '2. Đọc dòng đếm', '3. Đóng, ẩn cột Ghi chú ở Tuỳ chỉnh cột, bấm Xuất Excel lại'], '',
      ['Bước 2: tích sẵn 6 trường ứng với cột đang hiện, Người liên hệ chưa tích; "Đang chọn 6/7 trường"', 'Bước 3: Ghi chú không được tích sẵn']),
    C('Xuất với trường mặc định', 'P0', CO, ['1. Bấm Xuất Excel > "Xuất file"', '2. Mở file'], '',
      ['Toast "Xuất Excel thành công"', 'File có tiêu đề "Danh sách đăng ký khách hàng toàn công ty", cột STT đứng đầu rồi 6 cột đã chọn']),
    C('Xuất tất cả trường', 'P1', CO, ['1. Bấm Xuất Excel > "Chọn tất cả" > "Xuất file"'], '',
      ['File có 7 cột dữ liệu + STT, Người liên hệ là cột riêng', 'Dòng khách cá nhân: cột Người liên hệ trống']),
    C('Xuất một số trường và đổi thứ tự', 'P1', CO, ['1. Bấm Xuất Excel', '2. Bỏ tích Ghi chú, kéo Số báo giá lên đầu', '3. Bấm "Xuất file"'], '',
      ['File: STT, Số báo giá, Khách hàng đăng ký, Ngày đăng ký, Thời hạn đăng ký, Người đăng ký; không có Ghi chú']),
    C('Không chọn trường nào', 'P1', 'Đang mở cửa sổ chọn trường.', ['1. Bấm "Bỏ chọn hết"', '2. Thử bấm "Xuất file"'], '',
      ['"Đang chọn 0/7 trường"', 'Nút "Xuất file" mờ, không bấm được, không tải file']),
    C('Đóng cửa sổ thì không xuất', 'P2', 'Đang mở cửa sổ chọn trường.', ['1. Bấm "Đóng"'], '',
      ['Cửa sổ đóng, không tải file', 'Bảng giữ nguyên bộ lọc, trang']),
    C('Xuất theo từ khóa tìm nhanh', 'P0', 'Đang tìm nhanh "TOYOTA" (72 dòng).', ['1. Bấm Xuất Excel > "Xuất file"', '2. Đếm dòng trong file'], '',
      ['File có đúng 72 dòng dữ liệu, đều chứa "TOYOTA"']),
    C('Xuất theo bộ lọc', 'P0', 'Đang lọc Thời hạn đăng ký = Còn hạn (3 dòng).', ['1. Bấm Xuất Excel > "Xuất file"'], '',
      ['File có đúng 3 dòng, khớp từng dòng trên màn']),
    C('Xuất lấy tất cả các trang', 'P0', CO, ['1. Để 10 dòng/trang, đứng ở trang 1', '2. Xuất file, đếm dòng'], '',
      ['File có đủ 2,134 dòng (bằng N chân bảng), không phải 10 dòng trang đang xem', 'Thứ tự dòng đúng thứ tự sắp xếp trên màn']),
    C('Xuất khi danh sách rỗng', 'P2', 'Đang tìm nhanh "zzzz", bảng hiện ' + EMPTY + '.', ['1. Bấm Xuất Excel > "Xuất file"'], '',
      ['Không báo lỗi, vẫn tải file', 'File chỉ có tiêu đề và hàng tên cột, không có dòng dữ liệu']),
    C('Tên file và định dạng', 'P1', CO, ['1. Xuất file', '2. Mở bằng Excel'], '',
      ['Tên file "' + FILE + '"', 'Mở được bình thường, không báo file hỏng']),
    C('Dữ liệu và định dạng trong file khớp màn', 'P0', CO, ['1. Xuất file trường mặc định', '2. So 10 dòng đầu file với trang 1 trên màn'], '',
      ['Từng ô khớp màn hình', 'Ngày đăng ký dạng dd/mm/yyyy HH:mm, Thời hạn đăng ký dạng dd/mm/yyyy', 'Cột STT đánh 1, 2, 3… liên tục',
       'Tiếng Việt có dấu, ghi chú nhiều dòng và ký tự & / - hiển thị đúng']),
    C('Bấm Xuất Excel liên tục', 'P2', CO, ['1. Bấm "Xuất file" rồi bấm lại "Xuất Excel" ngay khi đang xuất'], '',
      ['Trong lúc đang xuất, nút "Xuất Excel" không bấm được; chỉ tải 1 file']),
]

# ================================================================== VI. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
LOCK = '"Đã có người đăng ký nên bạn không được phép chọn"'
G6 = [
    C('Bấm Số báo giá của báo giá thường mở màn chi tiết báo giá', 'P1', 'Có đăng ký gắn với báo giá thường BG-T01 trên HRM.',
      ['1. Tìm đăng ký đó', '2. Bấm Số báo giá'], '',
      ['Mở màn chi tiết báo giá BG-T01 ở TAB MỚI', 'Tab danh sách giữ nguyên bộ lọc, trang']),
    C('Bấm Số báo giá của báo giá hãng mở màn báo giá hãng', 'P1', 'Đăng ký từ báo giá hãng BGBH_TPE_HN_KD2_26_5641.',
      ['1. Tìm đăng ký đó', '2. Bấm Số báo giá'], '',
      ['Mở màn chi tiết báo giá hãng ở tab mới (hệ thống bán hàng hiện hành)',
       'Người không có quyền xem báo giá đó: màn đích tự báo không có quyền; màn danh sách không lỗi']),
    C('Meeting: không chọn được khách cá nhân người khác đang đăng ký', 'P0', 'NV-B đang có đăng ký CÒN HẠN cho khách cá nhân KH-CN; đăng nhập NV-A.',
      ['1. Vào Meeting > Tổng hợp meeting > Tạo mới', '2. Chọn khách hàng KH-CN', '3. Bấm Lưu'], 'Khách hàng: KH-CN',
      ['Hệ thống báo đỏ ' + LOCK + ' tại ô khách hàng, không lưu được']),
    C('Meeting: không chọn được người liên hệ người khác đang đăng ký', 'P0', 'NV-B đang đăng ký còn hạn người liên hệ LH1 của KH-DN; đăng nhập NV-A.',
      ['1. Tạo meeting, chọn KH-DN và người liên hệ LH1', '2. Bấm Lưu'], '',
      ['Báo ' + LOCK + ' tại ô người liên hệ', 'Chọn người liên hệ LH2 (không ai đăng ký) thì lưu được']),
    C('Dự án TKT: chặn chọn khách người khác đang đăng ký', 'P0', 'Như case Meeting; đăng nhập NV-A.',
      ['1. Vào CSKH trước bán > Dự án TKT > Tạo mới', '2. Chọn KH-CN (hoặc LH1 của KH-DN)', '3. Bấm Lưu'], '',
      ['Báo ' + LOCK + ', không lưu được']),
    C('Báo giá: chặn chọn khách người khác đang đăng ký', 'P1', 'Như case Meeting; đăng nhập NV-A.',
      ['1. Vào CSKH trước bán > Báo giá > Tạo mới, chọn khách KH-CN', '2. Bấm Lưu'], '',
      ['Báo ' + LOCK + ', không lưu được']),
    C('Chính người đăng ký vẫn chọn được khách của mình', 'P1', 'NV-B đang đăng ký còn hạn KH-CN; đăng nhập NV-B.',
      ['1. Tạo meeting với khách KH-CN', '2. Bấm Lưu'], '',
      ['Lưu thành công, không bị chặn']),
    C('Đăng ký hết hạn thì người khác chọn lại được', 'P0', 'Đăng ký của NV-B cho KH-CN có thời hạn hôm qua (màn danh sách lọc Hết hạn thấy dòng này).',
      ['1. Đăng nhập NV-A, tạo meeting với KH-CN', '2. Bấm Lưu'], '',
      ['Lưu được, không còn báo ' + LOCK]),
    C('Danh mục khách hàng: ô chọn khách bị khóa theo đăng ký', 'P2', 'NV-B đang đăng ký còn hạn KH-CN; đăng nhập NV-A.',
      ['1. Mở cửa sổ chọn khách hàng ở màn tạo meeting', '2. Tìm KH-CN'], '',
      ['KH-CN hiện nhưng bị khóa, kèm chữ ' + LOCK]),
]

# ================================================================== VII. PHÂN QUYỀN
G7 = [
    C('Có quyền xem thấy menu và xem toàn bộ danh sách', 'P0', Q, ['1. Đăng nhập TK-Q', '2. ' + MENU], 'Tài khoản TK-Q',
      ['Thấy mục menu, mở được màn', 'Bảng có dữ liệu toàn công ty, chân bảng ghi tổng số đăng ký',
       'Dùng được Tìm kiếm, Xuất Excel, Tuỳ chỉnh cột']),
    C('Không có quyền thì ẩn mục menu', 'P0', 'Tài khoản TK-Z KHÔNG có quyền "%s".' % QUYEN,
      ['1. Đăng nhập TK-Z', '2. Vào CSKH trước bán > Báo cáo > nhóm Báo cáo thị trường'], 'Tài khoản TK-Z',
      ['KHÔNG có mục "Danh sách đăng ký khách hàng toàn công ty"']),
    C('Mở đường dẫn trực tiếp khi không có quyền', 'P0', 'TK-Z không có quyền; đã lưu dấu trang màn này từ TK-Q.',
      ['1. Đăng nhập TK-Z', '2. Mở dấu trang đã lưu'], 'Tài khoản TK-Z',
      ['Báo "Bạn không có quyền thực hiện chức năng này"', 'Bảng không có dòng dữ liệu nào', 'Bấm Xuất Excel > Xuất file: không tải được file']),
    C('Quyền không chia phạm vi theo công ty / phòng ban', 'P0', 'TK-Q chỉ có quyền "%s", thuộc công ty 1 phòng KD1, không có quyền xem nào khác.' % QUYEN,
      ['1. Đăng nhập TK-Q, mở màn', '2. Đổi công ty đang làm việc sang công ty 2, mở lại màn'], '',
      ['Bước 1: thấy đăng ký của mọi phòng, mọi công ty', 'Bước 2: tổng số dòng không đổi (không phụ thuộc công ty đang làm việc)']),
    C('Đổi quyền trong lúc đang xem', 'P1', 'TK-Q đang mở màn có dữ liệu.',
      ['1. Người quản trị gỡ quyền "%s" của TK-Q' % QUYEN, '2. Ở màn đang mở, bấm Tìm kiếm', '3. Nhấn F5'], '',
      ['Bước 2: báo "Bạn không có quyền thực hiện chức năng này", không tải thêm dữ liệu', 'Bước 3: mục menu biến mất, bảng không có dữ liệu']),
    C('Cấp lại quyền thì xem được', 'P2', 'TK-Z vừa được cấp quyền "%s".' % QUYEN, ['1. TK-Z đăng xuất, đăng nhập lại', '2. ' + MENU], '',
      ['Mục menu hiện, xem được toàn bộ danh sách']),
]

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('TÌM KIẾM & LỌC DANH SÁCH', G2),
    ('SỐ LIỆU BÁO CÁO', G3),
    ('TÙY CHỈNH CỘT', G4),
    ('XUẤT DANH SÁCH EXCEL', G5),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G6),
    ('PHÂN QUYỀN', G7),
]

if __name__ == '__main__':
    build_chuan(OUT, 'Trang tính1', TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, sections(GROUPS), loai='bao_cao')
    print(' · '.join('%s %d' % (t, len(c)) for t, c in GROUPS), '· tổng', sum(len(c) for _, c in GROUPS))
