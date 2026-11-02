# -*- coding: utf-8 -*-
"""Testcase màn "Khai báo đầu kỳ công nợ nhà cung cấp" (STT 168, phân hệ Tài chính > Khai báo đầu kỳ).

Chép khuôn màn mẫu ../kh/gen_testcase.py. Nguồn case cũ: ../../gen_testcase.py (02/10/2026, cấu hình NCC — 79 case,
file "testcase HRM - Khai bao dau ky cong no nha cung cap.xlsx"), RÀ LẠI từng case theo code HRM hiện tại (develop, 02/11/2026):
  - menu thật (Tài chính > Khai báo đầu kỳ), nhãn / thông báo nguyên văn;
  - BỎ mọi câu "Đối chiếu ERP", case đối chiếu dữ liệu với ERP và case "gọi thẳng chức năng bằng công cụ kiểm thử API";
  - code đã đổi sau 02/10: bộ lọc chỉ còn NCC, Tài khoản, Số hợp đồng, Người lập HĐ, Người tạo, Người cập nhật, Ngày tạo,
    Công ty – Phòng ban (#11555 — bỏ Loại hợp đồng, Loại dư, Công nợ, Loại tiền, Bộ phận); bỏ "Ngày tính công nợ" (#11565);
    nút "Lưu và tiếp tục"; file mẫu import không có dòng mô tả (#11560); tỷ giá báo cùng lượt (#11557); chặn lưu 2 lần
    (#11559); import bỏ qua dòng vừa bị trùng (#11629); Người tạo "Họ tên - Mã phòng" (#11566).
Mỗi case gắn nhãn: G = giữ nguyên, S = sửa, M = thêm mới. Case bỏ ghi ở BO. Cuối file in thống kê.
Chạy: python gen_testcase.py
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402,F401  (đặt sys.path tới tc_engine)
from tc_engine import build  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Khai báo đầu kỳ công nợ nhà cung cấp'
MODULE = 'Khai báo đầu kỳ công nợ NCC'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SO_CU = 79
TAGS = Counter()

BO = {
    'TC-ROLE-09': 'Gọi thẳng Thêm / Sửa / Xóa bằng công cụ kiểm thử API khi không có quyền (tester kỹ thuật)',
    'TC-ROLE-10': 'Gọi thẳng Sửa / Xóa khai báo đã phát sinh bằng công cụ kiểm thử API (thay bằng TC_10.002 qua giao diện)',
    'TC_02.006': 'Lọc theo Loại dư — màn đã bỏ ô lọc này (#11555), gộp vào TC_02.004',
    'TC_02.007': 'Lọc theo khoảng Công nợ — màn đã bỏ ô lọc này (#11555), gộp vào TC_02.004',
    'TC_02.013': 'Lọc theo Loại tiền — màn đã bỏ ô lọc này (#11555), gộp vào TC_02.004',
    'TC_09.004': 'Gọi thẳng chức năng Thêm với tài khoản tổng hợp / đang khóa (tester kỹ thuật)',
    'TC_09.005': 'Gọi thẳng chức năng Thêm với hợp đồng không tồn tại (đã có ở Import TC_07.004)',
    'TC_10.003': 'Đối chiếu dữ liệu lập bên HRM hiện bên ERP và ngược lại',
}


def L_(*lines):
    return '\n'.join(lines)


def T(tag, n, func, prio, pre, steps, data, exp):
    assert tag in ('G', 'S', 'M')
    TAGS[tag] += 1

    def j(x):
        return x if isinstance(x, str) else L_(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'phân hệ Tài chính > menu Khai báo đầu kỳ > "Khai báo đầu kỳ công nợ nhà cung cấp"'
NCC = 'TCX - BEIJING TAICHENGXIN DIGITAL TECHNOLOGY CO., LTD'
HD1 = '0624/TPE-TCX/VF AXLE GA-PL'
HD2 = 'TPE-TCX/PLC TRAINING'
TK = '3311 - Phải trả cho người bán ngắn hạn'
Q_THEM = 'Khai báo thêm công nợ đầu kỳ nhà cung cấp'
Q_SUA = 'Khai báo sửa công nợ đầu kỳ nhà cung cấp'
Q_XOA = 'Khai báo xoá công nợ đầu kỳ nhà cung cấp'
SO = 'sổ chi tiết tài khoản 3311 (dòng có chứng từ = mã phiếu khai báo; nhờ kế toán có quyền xem sổ đối chiếu)'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '- TK-A: nhân viên công ty TPE, có đủ 3 quyền "' + Q_THEM + '", "' + Q_SUA + '", "' + Q_XOA + '" + "Xem tất cả công nợ đầu kỳ của công ty".',
    '- TK-ALL: như TK-A nhưng phạm vi "Xem tất cả công nợ đầu kỳ". TK-Z: không có quyền nào của nhóm khai báo đầu kỳ.',
    '- Nhà cung cấp NCC-1: ' + NCC + '; HĐ-1: ' + HD1 + ' (hợp đồng mua nước ngoài, USD), HĐ-2: ' + HD2 + ' (hợp đồng mua đầu kỳ, VNĐ), cả 2 chưa khai báo.',
    '- Khai báo Z: lập bằng TK-A cho NCC-1 + HĐ-2 + tài khoản ' + TK + ', VNĐ, Dư có 1,500,000 (chưa có chứng từ công nợ). Dev có sẵn khai báo chưa phát sinh TPE_DKNCC_01302.',
    '- Khai báo Y: một khai báo đã có phiếu chi / phiếu kế toán trên cùng nhà cung cấp + hợp đồng + tài khoản (dev: TPE_DKNCC_01101).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Khai báo đầu kỳ công nợ nhà cung cấp" khai báo SỐ DƯ CÔNG NỢ ĐẦU KỲ của nhà cung cấp theo từng hợp đồng mua × '
        'tài khoản, theo nguyên tệ và quy đổi VND — số mở đầu cho sổ chi tiết công nợ phải trả.',
        'Luồng: chọn nhà cung cấp → "Chọn hợp đồng" (một hoặc nhiều hợp đồng mua) → mỗi dòng nhập Tài khoản, Loại tiền, Tỷ giá, '
        'Loại dư, Công nợ → Lưu. Mỗi dòng thành 1 khai báo riêng (1 mã phiếu, 1 bút toán), KHÔNG qua duyệt.',
        'Đường vào: ' + MENU + '.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới, Sửa, Xem chi tiết, Xóa, Lịch sử, '
        'In danh sách, Xuất Excel, Import Excel.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi xem (xét lần lượt, gặp quyền nào trước thì dùng quyền đó; dùng chung 4 quyền với màn khách hàng):',
        '- "Xem tất cả công nợ đầu kỳ": mọi công ty; khu vực lọc có ô Công ty, Phòng ban.',
        '- "Xem tất cả công nợ đầu kỳ của công ty": công ty đang làm việc; có ô Phòng ban.',
        '- "… của phòng ban" / "… của bộ phận": các phòng ban / bộ phận được giao quản lý.',
        '- Không có quyền nào ở trên: chỉ khai báo do chính mình tạo.',
        'Công ty / phòng ban / bộ phận của khai báo = của NGƯỜI LẬP HỢP ĐỒNG.',
        'Cửa sổ "Chọn hợp đồng nhà cung cấp" gộp 4 nguồn hợp đồng mua (nước ngoài, mua ngoài, mua trong nước, mua đầu kỳ), '
        'mọi trạng thái; ô "Phạm vi" chọn hợp đồng của nhà cung cấp đang chọn hoặc của nhà cung cấp KHÁC.',
        'Tài khoản chọn được: tài khoản chi tiết đang hoạt động có đánh dấu "theo dõi công nợ". Loại tiền: tiền tệ đang hoạt động, VNĐ luôn có.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Khai báo ngoài phạm vi xem: không hiện; mở đường dẫn trực tiếp thì sang trang "Không tìm thấy".',
        '- Trong cửa sổ chọn hợp đồng: hợp đồng đã có khai báo của nhà cung cấp đang chọn hiện mờ, Tình trạng "Đã khai báo", '
        'không chọn được; hợp đồng đã có trên form ghi "Đã chọn".',
        '- Nút Sửa / Xóa ẨN HẲN khi khai báo ĐÃ PHÁT SINH CHỨNG TỪ: cùng nhà cung cấp + hợp đồng + tài khoản đã có phiếu chi, '
        'ủy nhiệm chi, phiếu thu, phiếu báo có hoặc phiếu kế toán ghi sổ, hoặc có chứng từ trừ thẳng vào khai báo.',
        '- Nút Tạo mới / Import ẩn khi thiếu quyền thêm; Sửa / Xóa ẩn khi thiếu quyền sửa / xóa.',
        '- Phiếu nhập hàng, hạch toán trong kỳ trên cùng hợp đồng KHÔNG làm khai báo bị khóa.',
        '- Tài khoản / loại tiền đang khóa: không chọn mới được; khai báo cũ đang dùng thì vẫn hiện kèm biểu tượng khóa.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" (Từ – Đến) lọc theo ngày lập khai báo, tính cả 2 đầu mút.',
        'Ngày hạch toán của khai báo = "Ngày khai báo đầu kỳ" cấu hình ở Khai Quy chế – Cấu hình của công ty; '
        'không hiện trên màn, không phải ô lọc. Bộ lọc được ghi nhớ 10 phút khi rời màn rồi quay lại.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Một lần lập = 1 nhà cung cấp × nhiều hợp đồng mua; mỗi dòng lưu thành 1 khai báo (mã <mã công ty>_DKNCC_<5 chữ số>).',
        'Khai báo gồm: Mã phiếu, Nhà cung cấp, Loại hợp đồng, Số hợp đồng, Người lập hợp đồng, Tài khoản, Loại tiền, Tỷ giá, '
        'Loại dư, Công nợ (nguyên tệ), Quy đổi (VND), Người tạo / Ngày tạo, Người cập nhật / Ngày cập nhật.',
        'Trang Sửa và Chi tiết chỉ có 1 dòng; Mã phiếu, Nhà cung cấp và hợp đồng không đổi được.',
        'Trạng thái (hệ thống tự xác định): Chưa phát sinh chứng từ (Sửa, Xóa được) → Đã phát sinh chứng từ (chỉ xem); '
        'chứng từ bị xóa / hủy ghi sổ thì khai báo trở lại Chưa phát sinh.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Không trùng: cùng nhà cung cấp + hợp đồng + tài khoản chỉ khai báo 1 lần (kể cả trên cùng form, khi Sửa đổi tài '
        'khoản và khi import).',
        '- Công nợ phải lớn hơn 0. Dư nợ ghi Nợ, Dư có ghi Có tài khoản.',
        '- Loại tiền VNĐ: tỷ giá luôn 1, ô khóa. Khác VNĐ: tỷ giá bắt buộc, lớn hơn 0. Quy đổi (VND) = Công nợ × Tỷ giá, làm tròn đến đồng.',
        '- Được chọn hợp đồng của nhà cung cấp khác.',
        '- Sửa / Xóa khai báo thì bút toán sổ chi tiết đổi / mất theo.',
    )),
    ('7. Phân quyền cấp', L_(
        '- Xem màn: không cần quyền riêng (mục menu luôn hiện với người đăng nhập); dữ liệu theo phạm vi ở mục 2.',
        '- "' + Q_THEM + '": nút Tạo mới, Import Excel, cửa sổ chọn hợp đồng.',
        '- "' + Q_SUA + '": nút Sửa. "' + Q_XOA + '": nút Xóa.',
        '- Quyền gán ở màn Phân quyền của HRM.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N": N = tổng khai báo khớp bộ lọc và phạm vi quyền.',
        'Cột "Dư nợ" chỉ có số khi Loại dư = Dư nợ, cột "Dư có" chỉ có số khi Loại dư = Dư có; cột còn lại để TRỐNG.',
        'Cột "Quy đổi (VND)" = Công nợ × Tỷ giá, làm tròn đến đồng.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '- Số theo chuẩn quốc tế: 1,500,000 · 10,391.5.',
        '- Bản in tối đa 2,000 dòng; vượt thì báo phải thu hẹp bộ lọc.',
        '- Tiêu đề cửa sổ Lịch sử dùng MÃ PHIẾU (khai báo không có tên riêng).',
        '- Kiểm sổ sách: sau Lưu / Sửa / Xóa đối chiếu ' + SO + '.',
        '- Cột kết quả / check để trống cho tester điền.',
    )),
]

# ------------------------------------------------------------------ PHÂN QUYỀN
ROLE_TCS = [
    T('S', '00', 'Không có quyền nào vẫn vào được màn, chỉ xem', 'P0',
      'TK-Z không có quyền nào của nhóm khai báo đầu kỳ; TK-Z đã tạo 1 khai báo',
      ['1. Đăng nhập bằng TK-Z', '2. Vào ' + MENU],
      'Tài khoản TK-Z',
      ['- Mục menu hiện, màn mở được; chỉ hiện khai báo do TK-Z tạo',
       '- KHÔNG có nút Tạo mới, Import Excel; dòng KHÔNG có nút Sửa, Xóa',
       '- Vẫn có Xuất Excel, In danh sách, Cấu hình cột hiển thị và nút Lịch sử trên dòng']),
    T('S', '01', 'Quyền "' + Q_THEM + '"', 'P0',
      'TK-B chỉ có quyền thêm',
      ['1. Đăng nhập TK-B, vào màn', '2. Bấm Tạo mới, chọn nhà cung cấp, bấm "Chọn hợp đồng"'],
      '—',
      ['- Có nút Tạo mới, Import Excel; mở được cửa sổ chọn hợp đồng, lưu được',
       '- Dòng trên danh sách KHÔNG có nút Sửa, Xóa']),
    T('S', '02', 'Quyền "' + Q_SUA + '"', 'P0',
      'TK-C chỉ có quyền sửa; có khai báo Z chưa phát sinh trong phạm vi',
      ['1. Đăng nhập TK-C, vào màn', '2. Quan sát dòng Z, bấm Sửa, đổi Công nợ, bấm Lưu'],
      '—',
      ['- Dòng Z có nút Sửa, KHÔNG có nút Xóa', '- Không có nút Tạo mới, Import Excel',
       '- Trang Sửa mở được, "Cập nhật thành công."']),
    T('S', '03', 'Quyền "' + Q_XOA + '"', 'P0',
      'TK-D chỉ có quyền xóa; có khai báo Z chưa phát sinh',
      ['1. Đăng nhập TK-D, vào màn', '2. Quan sát dòng Z, mở chi tiết Z'],
      '—',
      ['- Dòng Z có nút Xóa, KHÔNG có nút Sửa', '- Chân trang Chi tiết: Xóa, Quay lại (không có Sửa)']),
    T('S', '04', 'Phạm vi xem: "Xem tất cả công nợ đầu kỳ"', 'P0',
      'TK-ALL',
      ['1. Đăng nhập TK-ALL, vào màn', '2. Đọc N ở chân bảng, bấm Tìm kiếm nâng cao'],
      '—',
      ['- Thấy khai báo của MỌI công ty', '- Khu vực lọc có ô Công ty, Phòng ban (Phòng ban khóa tới khi chọn Công ty); KHÔNG có ô Bộ phận']),
    T('S', '05', 'Phạm vi xem: "Xem tất cả công nợ đầu kỳ của công ty"', 'P0',
      'TK-A, công ty TPE',
      ['1. Đăng nhập TK-A, vào màn', '2. Bấm Tìm kiếm nâng cao', '3. Lọc Phòng ban = một phòng'],
      '—',
      ['- Chỉ thấy khai báo có công ty = TPE (công ty của NGƯỜI LẬP HỢP ĐỒNG)',
       '- Không có ô Công ty; có ô Phòng ban', '- Lọc Phòng ban ra khai báo của hợp đồng do nhân viên phòng đó lập']),
    T('S', '06', 'Phạm vi xem: "Xem tất cả công nợ đầu kỳ của phòng ban"', 'P1',
      'TK-PB có quyền phòng ban, được giao quản lý 1 phòng ban',
      ['1. Đăng nhập TK-PB, vào màn'],
      '—',
      ['- Chỉ thấy khai báo thuộc phòng ban được giao quản lý (theo người lập hợp đồng)']),
    T('S', '07', 'Phạm vi xem: "Xem tất cả công nợ đầu kỳ của bộ phận"', 'P1',
      'TK-BP có quyền bộ phận, được giao quản lý 1 bộ phận',
      ['1. Đăng nhập TK-BP, vào màn'],
      '—',
      ['- Chỉ thấy khai báo thuộc bộ phận được giao quản lý']),
    T('S', '08', 'Không có quyền phạm vi nào: chỉ thấy khai báo mình tạo', 'P0',
      'TK-F có 3 quyền thao tác nhưng không có quyền phạm vi nào; TK-F đã tạo 3 khai báo',
      ['1. Đăng nhập TK-F, vào màn', '2. Dán đường dẫn trang Chi tiết của một khai báo do người khác tạo'],
      '—',
      ['- Chỉ hiện 3 khai báo của TK-F', '- Khu vực lọc KHÔNG có ô Công ty / Phòng ban',
       '- Đường dẫn khai báo của người khác: trang "Không tìm thấy"']),
    T('M', '09', 'Vào thẳng trang Thêm / Sửa khi thiếu quyền', 'P1',
      'TK-Z (không có quyền thêm, sửa); khai báo Z chưa phát sinh trong phạm vi TK-Z',
      ['1. Đăng nhập TK-Z, dán đường dẫn trang Thêm', '2. Dán đường dẫn trang Sửa của Z'],
      '—',
      ['- Trang Thêm: chuyển sang trang "Không tìm thấy", không tạo được gì',
       '- Trang Sửa: toast "Khai báo đã phát sinh chứng từ hoặc bạn không có quyền sửa." rồi chuyển về trang Chi tiết của Z']),
]

# ------------------------------------------------------------------ I. HIỂN THỊ
S1 = [
    T('S', '001', 'Vào màn qua menu', 'P0', 'TK-A',
      ['1. Đăng nhập TK-A', '2. Vào ' + MENU],
      '—',
      ['- Tiêu đề trang và tiêu đề bảng "Khai báo đầu kỳ công nợ nhà cung cấp"', '- Bảng 10 dòng, khai báo mới lập nhất đứng đầu',
       '- Không cần bấm Tìm kiếm, bảng tự tải']),
    T('S', '002', 'Bộ cột mặc định', 'P0', 'Tài khoản chưa từng tùy chỉnh cột ở màn này',
      ['1. Mở màn danh sách', '2. Đọc tiêu đề cột từ trái sang phải'],
      '—',
      ['- Đúng thứ tự: STT, Mã phiếu, Nhà cung cấp, Số hợp đồng, Loại tiền, Dư nợ, Dư có, Người tạo, Ngày tạo, Hành động',
       '- Các cột Tài khoản, Loại hợp đồng, Người lập hợp đồng, Tỷ giá, Quy đổi (VND), Người cập nhật, Ngày cập nhật bật được ở "Cấu hình cột hiển thị"',
       '- KHÔNG có cột "Ngày tính công nợ"']),
    T('S', '003', 'Mã phiếu là đường dẫn vào Chi tiết', 'P1', 'Có khai báo TPE_DKNCC_01302',
      ['1. Bấm vào mã phiếu', '2. Quay lại, bấm chuột phải vào mã phiếu'],
      '—',
      ['- Bấm trái mở trang "Chi tiết khai báo đầu kỳ công nợ nhà cung cấp: TPE_DKNCC_01302"', '- Chuột phải có "Mở liên kết trong tab mới"']),
    T('S', '004', 'Số hợp đồng mở chứng từ gốc', 'P2', 'Khai báo gắn hợp đồng mua nước ngoài / mua đầu kỳ',
      ['1. Bấm vào số hợp đồng trên dòng'],
      '—',
      ['- Mở tab mới tới trang xem hợp đồng mua', '- Hợp đồng chưa có trang xem thì hiện chữ thường, không bấm được']),
    T('S', '005', 'Định dạng số, ngày, ô trống', 'P1', 'Có khai báo USD Dư có số lẻ (vd 42,963.6) và khai báo VNĐ Dư nợ',
      ['1. Tìm 2 khai báo trên', '2. Đọc cột Loại tiền, Dư nợ, Dư có, Người tạo, Ngày tạo; bật cột Tỷ giá, Quy đổi (VND)'],
      '—',
      ['- Dư có hiện "42,963.6", cột Dư nợ cùng dòng để TRỐNG (không 0, không gạch)', '- Loại tiền "USD" / "VNĐ"',
       '- Quy đổi (VND) = Công nợ × Tỷ giá làm tròn đồng (vd 3,717 × 26,453 = 98,325,801)',
       '- Người tạo dạng "Họ tên - Mã phòng ban"; Ngày tạo dd/mm/yyyy HH:mm']),
]

# ------------------------------------------------------------------ II. LỌC
S2 = [
    T('S', '001', 'Ô tìm nhanh theo mã phiếu, số hợp đồng, mã / tên nhà cung cấp', 'P0', 'Có khai báo của NCC-1',
      ['1. Gõ "TCX" vào ô tìm nhanh (chưa bấm gì)', '2. Nhấn Enter', '3. Lần lượt tìm theo một mã phiếu và một số hợp đồng'],
      'Tìm nhanh: TCX',
      ['- Đang gõ thì bảng chưa đổi; Enter hoặc nút Tìm kiếm mới lọc',
       '- Ra đúng khai báo của nhà cung cấp có mã / tên chứa từ khóa', '- Tìm theo mã phiếu / số hợp đồng ra đúng khai báo chứa chuỗi đó',
       '- Placeholder "Tìm theo mã phiếu, số hợp đồng, mã hoặc tên nhà cung cấp"']),
    T('G', '002', 'Lọc theo Nhà cung cấp (gõ để tìm)', 'P0', 'NCC-1 có khai báo',
      ['1. Mở Tìm kiếm nâng cao', '2. Ô Nhà cung cấp gõ 1 ký tự, rồi gõ "TCX"', '3. Chọn nhà cung cấp trong gợi ý', '4. F5 trang'],
      'Nhà cung cấp: TCX',
      ['- Gõ 1 ký tự: báo cần gõ thêm, chưa tìm', '- Chọn xong bảng tự lọc, chỉ còn khai báo của NCC-1',
       '- F5: ô Nhà cung cấp vẫn hiện đúng tên đã chọn']),
    T('S', '003', 'Lọc theo Tài khoản', 'P1', 'Có khai báo tài khoản 3311',
      ['1. Ô Tài khoản chọn "' + TK + '"', '2. Đổi sang một tài khoản khác không có khai báo'],
      'Tài khoản: 3311',
      ['- Chọn là lọc ngay', '- Bật cột Tài khoản: mọi dòng đúng tài khoản đã chọn',
       '- Tài khoản không có khai báo: "Không có dữ liệu phù hợp bộ lọc."']),
    T('S', '004', 'Bộ ô lọc của màn', 'P1', '—',
      ['1. Bấm Tìm kiếm nâng cao', '2. Đọc các ô lọc'],
      '—',
      ['- Có: Nhà cung cấp, Tài khoản, Số hợp đồng, Người lập hợp đồng, Người tạo, Người cập nhật, Ngày tạo (+ Công ty / Phòng ban theo phạm vi)',
       '- KHÔNG có ô Loại hợp đồng, Loại dư, Công nợ / Số tiền, Loại tiền, Bộ phận',
       '- Bộ lọc cũ đã lưu trước đây ở các ô này không còn lọc ngầm (N bằng N khi Làm mới)']),
    T('S', '005', 'Lọc theo Số hợp đồng', 'P1', 'Có khai báo gắn hợp đồng NAIPAUL0124.HP',
      ['1. Ô Số hợp đồng gõ "NAIPAUL"', '2. Nhấn Enter'],
      'Số hợp đồng: NAIPAUL',
      ['- Chờ Enter mới lọc', '- Ra khai báo có số hợp đồng chứa chuỗi đã gõ, với MỌI loại hợp đồng mua']),
    T('G', '006', 'Lọc theo Người tạo / Người cập nhật', 'P2', 'Có khai báo do TK-A tạo',
      ['1. Ô Người tạo chọn nhân viên của TK-A', '2. Xóa, rồi ô Người cập nhật chọn cùng người'],
      '—',
      ['- Chỉ còn khai báo do người đó tạo / cập nhật lần cuối']),
    T('S', '007', 'Lọc theo Ngày tạo (khoảng)', 'P1', 'Có khai báo tạo ngày 27/09/2025',
      ['1. Ô Ngày tạo chọn từ 27/09/2025 đến 27/09/2025'],
      'Ngày tạo: 27/09/2025 – 27/09/2025',
      ['- Ra đúng các khai báo tạo trong ngày đó, kể cả lúc 23:59']),
    T('S', '008', 'Lọc theo Công ty / Phòng ban', 'P1', 'TK-ALL',
      ['1. Ô Công ty chọn TPE', '2. Ô Phòng ban chọn một phòng', '3. Đổi Công ty'],
      '—',
      ['- Mỗi ô chọn xong là lọc ngay', '- Phòng ban chỉ mở sau khi chọn Công ty', '- Đổi Công ty thì Phòng ban tự xóa']),
    T('S', '009', 'Làm mới xóa hết điều kiện và tải lại', 'P1', 'Đang lọc Tài khoản 3311 và từ khóa "TCX"',
      ['1. Bấm Làm mới'], '—',
      ['- Mọi ô lọc về trống, bảng nạp lại toàn bộ phạm vi']),
    T('G', '010', 'Ghi nhớ bộ lọc khi vào chi tiết rồi quay lại', 'P1', 'Đang lọc Nhà cung cấp = NCC-1',
      ['1. Bấm vào một mã phiếu', '2. Bấm Quay lại'], '—',
      ['- Bộ lọc vẫn còn Nhà cung cấp = NCC-1']),
    T('S', '011', 'Lọc theo Người lập hợp đồng', 'P2', 'Có khai báo của hợp đồng do Vũ Thị Nhài (12510587) lập',
      ['1. Ô Người lập hợp đồng chọn Vũ Thị Nhài'], '—',
      ['- Chỉ còn khai báo có Người lập hợp đồng là người đó (bật cột Người lập hợp đồng để kiểm)']),
    T('M', '012', 'Cài đặt bộ lọc', 'P2', '—',
      ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Người cập nhật", kéo "Số hợp đồng" lên đầu, bấm Lưu', '3. F5 trang', '4. Mở lại, bấm Khôi phục mặc định'],
      '—',
      ['- Cửa sổ liệt kê 8 ô lọc', '- Sau Lưu và F5: ô Người cập nhật ẩn, Số hợp đồng đứng đầu',
       '- Khôi phục mặc định đưa về như ban đầu']),
]

# ------------------------------------------------------------------ III. DANH SÁCH
S3 = [
    T('G', '001', 'Sắp xếp theo Mã phiếu và Ngày tạo', 'P1', 'Có hơn 20 khai báo',
      ['1. Bấm tiêu đề cột Mã phiếu', '2. Bấm lần nữa', '3. Bấm tiêu đề cột Ngày tạo'], '—',
      ['- Mã phiếu tăng dần rồi giảm dần', '- Bấm Ngày tạo thì sắp theo ngày']),
    T('S', '002', 'Phân trang và số dòng / trang', 'P1', 'Có hơn 50 khai báo',
      ['1. Sang trang 3', '2. Đổi số dòng/trang sang 50'], '—',
      ['- Trang 3 STT bắt đầu từ 21', '- Đổi 50 dòng thì về trang 1, "Hiển thị 1–50 / N"']),
    T('S', '003', 'Cấu hình cột hiển thị được ghi nhớ', 'P2', '—',
      ['1. Bấm biểu tượng Cấu hình cột', '2. Bật cột Tỷ giá, Quy đổi (VND), bấm Lưu', '3. F5 trang'], '—',
      ['- Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 10/17 cột" lúc đầu', '- 2 cột mới hiện; sau F5 vẫn còn',
       '- Cột STT, Mã phiếu, Hành động có biểu tượng khóa, không bỏ được']),
    T('S', '004', 'Nút Sửa / Xóa ẩn với khai báo đã phát sinh chứng từ', 'P0', 'Khai báo Y (đã phát sinh) và khai báo Z (chưa); TK-A đủ quyền',
      ['1. Tìm 2 dòng Y và Z'], '—',
      ['- Dòng Y chỉ có nút Lịch sử, KHÔNG có Sửa / Xóa (ẩn hẳn, không hiện xám)', '- Dòng Z có Sửa, Xóa, Lịch sử']),
    T('S', '005', 'Phiếu nhập hàng KHÔNG làm khóa khai báo', 'P0',
      'Hợp đồng H đã có phiếu nhập hàng ghi sổ tài khoản 3311, chưa có phiếu chi / phiếu kế toán; vừa tạo khai báo trên H',
      ['1. Mở danh sách, tìm khai báo vừa tạo'], '—',
      ['- Vẫn có nút Sửa, Xóa', '- Lập phiếu chi / phiếu kế toán cho H thì nút Sửa / Xóa biến mất (TC_11.001)']),
]

# ------------------------------------------------------------------ IV. THÊM MỚI
S4 = [
    T('S', '001', 'Mở trang Thêm mới', 'P0', 'TK-A',
      ['1. Bấm Tạo mới'], '—',
      ['- Tiêu đề "Thêm khai báo đầu kỳ công nợ nhà cung cấp"; góc phải khối Thông tin chung "<tên TK-A> - <ngày giờ hiện tại>"',
       '- Khối "Thông tin chung" có ô Nhà cung cấp (*), placeholder "Chọn nhà cung cấp"',
       '- Khối "Danh sách hợp đồng mua" có nút "Chọn hợp đồng", bảng trống ghi "Chưa chọn hợp đồng nào — bấm "Chọn hợp đồng" để thêm."',
       '- Cột: STT, Loại hợp đồng, Số hợp đồng, Người lập hợp đồng, Tài khoản *, Loại tiền *, Tỷ giá *, Loại dư *, Công nợ *, Quy đổi (VND), nút xóa dòng',
       '- Chân trang: Lưu, Lưu và tiếp tục, Quay lại']),
    T('G', '002', 'Chưa chọn nhà cung cấp thì không mở được cửa sổ chọn hợp đồng', 'P0', '—',
      ['1. Bấm "Chọn hợp đồng" khi ô Nhà cung cấp còn trống'], '—',
      ['- Không mở cửa sổ', '- Báo đỏ dưới ô Nhà cung cấp: "Chọn nhà cung cấp trước khi chọn hợp đồng"']),
    T('S', '003', 'Ô Nhà cung cấp tìm từ máy chủ', 'P1', 'NCC-1',
      ['1. Gõ 1 ký tự', '2. Gõ "TCX"'], 'Nhà cung cấp: TCX',
      ['- Dưới 2 ký tự: báo cần gõ thêm', '- Gợi ý dạng "Mã - Tên", chỉ nhà cung cấp đang hoạt động']),
    T('S', '004', 'Cửa sổ chọn hợp đồng: danh sách và tình trạng', 'P0', 'NCC-1 có 5 hợp đồng mua, hợp đồng 0624/TPE-TCX/ VF AXLE GA đã khai báo',
      ['1. Chọn NCC-1, bấm "Chọn hợp đồng"'], '—',
      ['- Tiêu đề "Chọn hợp đồng nhà cung cấp", dòng phụ "Nhà cung cấp: ' + NCC + '"',
       '- Cột: STT, Loại hợp đồng, Số hợp đồng, Tổng thanh toán, Người tạo, Ngày tạo, Tình trạng',
       '- Hợp đồng đã khai báo: dòng mờ, Tình trạng "Đã khai báo"',
       '- Có ô Phạm vi (mặc định "HĐ nhà cung cấp hiện tại"), Loại hợp đồng, Số hợp đồng; nút Tìm kiếm, Làm mới; phân trang "Hiển thị 1–5 / 5"; nút Đóng']),
    T('S', '005', 'Bấm vào dòng là thêm hợp đồng ngay', 'P0', 'Đang mở cửa sổ chọn hợp đồng của NCC-1',
      ['1. Bấm dòng HĐ-1', '2. Bấm dòng HĐ-2', '3. Bấm lại dòng HĐ-1', '4. Bấm dòng "Đã khai báo"', '5. Bấm Đóng'], '—',
      ['- Mỗi lần bấm hiện "Đã thêm hợp đồng <số hợp đồng>", cửa sổ vẫn mở',
       '- Dòng đã chọn chuyển "Đã chọn", bấm lại không thêm trùng', '- Dòng "Đã khai báo" bấm không có tác dụng',
       '- Đóng cửa sổ: bảng có đúng 2 dòng, Loại dư mặc định Dư nợ']),
    T('S', '006', 'Lọc trong cửa sổ chọn hợp đồng', 'P1', 'Đang mở cửa sổ',
      ['1. Loại hợp đồng chọn "Hợp đồng mua nước ngoài"', '2. Số hợp đồng gõ "AXLE", Enter', '3. Bấm Làm mới'], '—',
      ['- Ô Loại hợp đồng có 4 lựa chọn: Hợp đồng mua nước ngoài, Hợp đồng mua ngoài, Hợp đồng mua trong nước, Hợp đồng mua đầu kỳ',
       '- Chỉ còn hợp đồng đúng loại / chứa chuỗi', '- Làm mới về toàn bộ hợp đồng của nhà cung cấp, Phạm vi về "HĐ nhà cung cấp hiện tại"']),
    T('S', '007', 'Phạm vi: hợp đồng của nhà cung cấp khác', 'P0', 'NCC-1; có hợp đồng mua của nhà cung cấp khác',
      ['1. Mở cửa sổ chọn hợp đồng', '2. Ô Phạm vi chọn "HĐ nhà cung cấp khác"', '3. Bấm 1 dòng, Đóng, nhập đủ rồi Lưu'], '—',
      ['- Bảng thêm cột Nhà cung cấp, chỉ hiện hợp đồng KHÔNG thuộc NCC-1',
       '- Chọn được và lưu được; khai báo mới có Nhà cung cấp = NCC-1, hợp đồng của nhà cung cấp khác']),
    T('S', '008', 'Thêm hợp đồng mua ngoại tệ tự điền Loại tiền, Tỷ giá, Người lập', 'P0',
      'HĐ-1 là hợp đồng mua nước ngoài bằng USD, do Nguyễn Thị Thanh Nhàn (11610149) lập; danh mục tiền tệ USD đang khai tỷ giá 25,990',
      ['1. Chọn HĐ-1', '2. Đóng cửa sổ, đọc dòng vừa thêm'], '—',
      ['- Người lập hợp đồng: "11610149 - Nguyễn Thị Thanh Nhàn"', '- Loại tiền: USD',
       '- Tỷ giá tự điền 25,990 (sửa được)', '- Loại dư mặc định Dư nợ; Tài khoản lấy theo dòng phía trên (nếu có)']),
    T('S', '009', 'Lưu thành công nhiều hợp đồng', 'P0', 'Đã chọn HĐ-1, HĐ-2 của NCC-1',
      ['1. Dòng 1: Tài khoản 3311, USD, Tỷ giá 25,990, Dư có, Công nợ 10,391.5',
       '2. Dòng 2: Tài khoản (đã tự điền 3311), VNĐ, Dư có, Công nợ 25,000,000', '3. Bấm Lưu', '4. Đối chiếu ' + SO],
      ['Dòng 1: ' + TK + ' / USD / 25,990 / Dư có / 10,391.5', 'Dòng 2: ' + TK + ' / VNĐ / Dư có / 25,000,000'],
      ['- Trước khi lưu: Quy đổi (VND) dòng 1 = 270,075,085, dòng 2 = 25,000,000',
       '- "Thêm mới thành công.", quay về danh sách', '- Có 2 khai báo mới, mã nối tiếp dạng TPE_DKNCC_<5 chữ số>',
       '- Sổ: 2 bút toán ghi Có 3311 — dòng 1 nguyên tệ 10,391.5 USD tỷ giá 25,990 quy đổi 270,075,085; dòng 2 25,000,000 VNĐ']),
    T('S', '010', 'Bấm Lưu khi chưa nhập đủ', 'P0', 'Đã chọn 2 hợp đồng (1 USD), chưa nhập Tài khoản, Công nợ; xóa trắng Tỷ giá dòng USD',
      ['1. Bấm Lưu', '2. Bấm Lưu thêm 2 lần liên tiếp'], '—',
      ['- Thông báo "Bạn chưa nhập đầy đủ thông tin.", ở lại form',
       '- Dưới ô Tài khoản, Công nợ của TỪNG dòng và ô Tỷ giá dòng USD báo đỏ cùng một lượt; màn tự cuộn tới ô lỗi đầu tiên',
       '- Bấm nhiều lần không chồng nhiều thông báo giống nhau, không tạo khai báo nào']),
    T('G', '011', 'Xóa dòng trên form', 'P1', 'Đã chọn 3 hợp đồng, dòng 3 đang báo lỗi',
      ['1. Bấm nút xóa ở dòng 1'], '—',
      ['- Còn 2 dòng; lỗi vẫn nằm đúng dòng (nay là dòng 2)', '- Hợp đồng vừa xóa chọn lại được trong cửa sổ']),
    T('G', '012', 'Đổi nhà cung cấp thì danh sách hợp đồng bị xóa', 'P1', 'Đã chọn 2 hợp đồng',
      ['1. Đổi ô Nhà cung cấp sang nhà cung cấp khác'], '—',
      ['- Bảng hợp đồng về trống']),
    T('G', '013', 'Cảnh báo khi thoát lúc chưa lưu', 'P1', 'Đã chọn 1 hợp đồng, đã nhập Công nợ',
      ['1. Bấm Quay lại', '2. Bấm "Ở lại"', '3. Bấm Quay lại lần nữa, bấm "Thoát"'], '—',
      ['- Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"',
       '- Ở lại: giữ nguyên dữ liệu', '- Thoát: về danh sách, không lưu gì']),
    T('M', '014', 'Lưu và tiếp tục', 'P1', 'Đã chọn HĐ-2 của NCC-1, nhập đủ',
      ['1. Bấm "Lưu và tiếp tục"'], '—',
      ['- "Thêm mới thành công."', '- Ở lại trang Thêm, ô Nhà cung cấp và bảng hợp đồng về trống để lập tiếp',
       '- Danh sách có khai báo vừa lưu']),
    T('M', '015', 'Chọn tài khoản 1 dòng thì điền cho các dòng chưa có', 'P2', 'Đã chọn 3 hợp đồng, chưa dòng nào có Tài khoản',
      ['1. Dòng 2 chọn Tài khoản 3311', '2. Dòng 3 đổi sang tài khoản khác', '3. Dòng 1 chọn lại tài khoản khác'], '—',
      ['- Bước 1: dòng 1 và dòng 3 tự điền 3311', '- Bước 2, 3: chỉ dòng đang sửa đổi, dòng đã có tài khoản không bị ghi đè']),
    T('M', '016', 'Đổi Loại tiền: tỷ giá và quy đổi', 'P0', 'Đã chọn HĐ-1 (USD), Công nợ 1,000',
      ['1. Đổi Loại tiền sang VNĐ', '2. Đổi lại USD', '3. Sửa Tỷ giá thành 26,000.1234'], '—',
      ['- VNĐ: Tỷ giá = 1, ô khóa; Quy đổi = 1,000', '- USD: Tỷ giá về tỷ giá danh mục (25,990), ô mở; Quy đổi = 25,990,000',
       '- Tỷ giá nhận tối đa 4 chữ số thập phân; Quy đổi làm tròn đến đồng (26,000,123)']),
]

# ------------------------------------------------------------------ V. CHI TIẾT, SỬA, LỊCH SỬ
S5 = [
    T('S', '001', 'Trang Chi tiết', 'P0', 'Khai báo TPE_DKNCC_01302 (NIPL, USD, Dư có 3,717, tỷ giá 26,453)',
      ['1. Bấm vào mã phiếu'], '—',
      ['- Tiêu đề "Chi tiết khai báo đầu kỳ công nợ nhà cung cấp: TPE_DKNCC_01302"; góc phải "<người tạo> - <ngày giờ tạo>"',
       '- Khối Thông tin chung: Mã phiếu, Nhà cung cấp — đều khóa (không có ô Ngày tính công nợ)',
       '- Bảng đúng 1 dòng, các ô khóa: Người lập hợp đồng "12510587 - Vũ Thị Nhài", USD, 26,453, Dư có, 3,717, Quy đổi 98,325,801',
       '- Có khối "Lịch sử" đang thu gọn', '- Chân trang: Sửa, Xóa, Quay lại']),
    T('G', '002', 'Nút ở Chi tiết khớp với dòng ở danh sách', 'P0', 'Khai báo Y (đã phát sinh), Z (chưa)',
      ['1. Mở chi tiết Y', '2. Mở chi tiết Z'], '—',
      ['- Y: chỉ có Quay lại', '- Z: Sửa, Xóa, Quay lại — giống nút ở dòng danh sách']),
    T('S', '003', 'Sửa: chỉ sửa được tài khoản, loại tiền, tỷ giá, loại dư, công nợ', 'P0', 'Khai báo Z chưa phát sinh (VNĐ, Dư có 1,500,000)',
      ['1. Bấm Sửa', '2. Đổi Loại tiền sang USD, Tỷ giá 25,990, Loại dư Dư nợ, Công nợ 2,750.5', '3. Bấm Lưu', '4. Đối chiếu ' + SO],
      ['Loại tiền: USD, Tỷ giá 25,990', 'Loại dư: Dư nợ', 'Công nợ: 2,750.5'],
      ['- Tiêu đề "Sửa khai báo đầu kỳ công nợ nhà cung cấp"; Mã phiếu, Nhà cung cấp, hợp đồng bị khóa; không có nút Chọn hợp đồng / xóa dòng / Lưu và tiếp tục',
       '- "Cập nhật thành công.", về danh sách; danh sách: Loại tiền USD, Dư nợ 2,750.5, Dư có trống',
       '- Sổ: bút toán đổi sang Nợ 3311, nguyên tệ 2,750.5 USD, quy đổi 71,485,495']),
    T('S', '004', 'Sửa sang tài khoản đã khai báo cho cùng hợp đồng bị chặn', 'P1',
      'Hợp đồng H của NCC-1 có 2 khai báo ở 2 tài khoản A, B (lập bằng Import)',
      ['1. Sửa khai báo tài khoản B, đổi sang A', '2. Bấm Lưu'], '—',
      ['- Dưới ô Tài khoản: "Đã khai báo đầu kỳ cho tài khoản này", không lưu']),
    T('G', '005', 'Vào thẳng trang Sửa của khai báo đã phát sinh', 'P0', 'Khai báo Y',
      ['1. Dán đường dẫn trang Sửa của Y'], '—',
      ['- Thông báo "Khai báo đã phát sinh chứng từ hoặc bạn không có quyền sửa."', '- Tự chuyển về trang Chi tiết của Y']),
    T('S', '006', 'Lịch sử thay đổi ở Chi tiết', 'P0', 'Khai báo Z vừa tạo rồi sửa như TC_05.003',
      ['1. Mở chi tiết Z', '2. Ở khối Lịch sử bấm "Xem lịch sử"', '3. Bấm Bộ lọc'], '—',
      ['- Mới nhất ở trên: "Thay đổi thông tin" — Loại tiền: VNĐ → USD; Tỷ giá: 1.00 → 25,990.00; Loại dư: Dư có → Dư nợ; Công nợ: 1,500,000.00 → 2,750.50 (cũ đỏ, mới xanh)',
       '- Dưới cùng: "Tạo mới" kèm "Người thực hiện: <họ tên> — <phòng ban>"',
       '- Bộ lọc: loại hành động, người thực hiện, Từ ngày, Đến ngày']),
    T('S', '007', 'Lịch sử mở từ danh sách', 'P1', 'Khai báo Z như trên',
      ['1. Ở danh sách, bấm nút Lịch sử của dòng Z'], '—',
      ['- Cửa sổ "Lịch sử thay đổi: <mã Z>", nội dung giống khối ở Chi tiết']),
    T('M', '008', 'Sửa: cảnh báo khi thoát lúc chưa lưu', 'P2', 'Đang ở trang Sửa của Z',
      ['1. Đổi Công nợ', '2. Bấm Quay lại'], '—',
      ['- Hộp "Thông tin chưa lưu" (Thoát / Ở lại) như trang Thêm']),
]

# ------------------------------------------------------------------ VI. XÓA
S6 = [
    T('S', '001', 'Xóa khai báo chưa phát sinh', 'P0', 'Khai báo Z chưa phát sinh',
      ['1. Bấm Xóa ở dòng Z', '2. Bấm Hủy', '3. Bấm Xóa lần nữa, bấm Xóa trong hộp', '4. Đối chiếu ' + SO], '—',
      ['- Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?"', '- Hủy: không đổi gì',
       '- Xóa: "Xóa thành công.", dòng biến mất', '- Sổ: bút toán của Z không còn']),
    T('G', '002', 'Xóa từ trang Chi tiết', 'P1', 'Khai báo Z chưa phát sinh',
      ['1. Mở chi tiết Z, bấm Xóa, xác nhận'], '—',
      ['- Về danh sách, Z không còn']),
    T('S', '003', 'Không xóa được khai báo đã phát sinh', 'P0', 'Khai báo Y',
      ['1. Tìm dòng Y ở danh sách và mở chi tiết'], '—',
      ['- Không có nút Xóa ở cả 2 nơi']),
    T('M', '004', 'Xóa xong hợp đồng chọn lại được', 'P2', 'Vừa xóa khai báo Z của HĐ-2',
      ['1. Tạo mới, chọn NCC-1, mở cửa sổ chọn hợp đồng'], '—',
      ['- HĐ-2 không còn "Đã khai báo", chọn được']),
]

# ------------------------------------------------------------------ VII. IMPORT
S7 = [
    T('S', '001', 'Tải file mẫu', 'P1', '—',
      ['1. Bấm Import Excel', '2. Bấm "Tải file mẫu", mở file'], '—',
      ['- Tên file Mau_import_cong_no_dau_ky_nha_cung_cap.xlsx',
       '- Cột: STT, Nhà cung cấp *, Mã hợp đồng mua *, Loại hợp đồng mua *, Số tài khoản *, Loại tiền *, Tỷ giá, Loại dư, Công nợ *',
       '- Hàng 1 là tiêu đề, KHÔNG có dòng mô tả; có dòng ví dụ', '- Cột Loại hợp đồng mua và Loại dư bấm ra danh sách chọn']),
    T('S', '002', 'Kiểm tra dữ liệu import', 'P0', 'File 5 dòng: 1 đúng, 1 sai mọi cột, 1 trùng dòng 1, 1 USD thiếu tỷ giá, 1 hợp đồng đã khai báo',
      ['1. Chọn file, bấm "Load lên bảng"', '2. Bấm Validate'], '—',
      ['- Tổng 5, Hợp lệ 1, Lỗi 4; "Validate xong: 1 hợp lệ, 4 không hợp lệ…"', '- Dòng đúng: xanh, khóa',
       '- Dòng sai: "Nhà cung cấp – Mã không tồn tại trong hệ thống", "Loại hợp đồng – Chỉ nhận HDMNN / HDMN / HDMTN / HDMDK", '
       '"Số tài khoản – Không tồn tại trong hệ thống", "Loại dư – Chỉ nhận "Dư nợ" hoặc "Dư có"", "Công nợ – Phải lớn hơn 0.", '
       '"Loại tiền – Mã không tồn tại trong hệ thống"',
       '- Dòng trùng: "Trùng với dòng 1 trong file"', '- Dòng USD thiếu tỷ giá: "Tỷ giá – Bắt buộc phải nhập"',
       '- Dòng đã khai báo: "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này"',
       '- Sửa được dòng lỗi ngay trên bảng rồi Validate lại']),
    T('S', '003', 'Import chỉ khi không còn dòng lỗi', 'P0', 'Sau TC_07.002',
      ['1. Quan sát nút Import', '2. Bấm "Bỏ dòng lỗi"', '3. Bấm Import'], '—',
      ['- Bước 1: nút Import mờ', '- Bước 3: báo import thành công 1 dòng; cửa sổ đóng, danh sách nạp lại',
       '- Khai báo mới có mã nối tiếp, Người lập hợp đồng đúng, có mốc "Tạo mới" trong lịch sử và có bút toán trong sổ như khi lập tay']),
    T('S', '004', 'Import kiểm hợp đồng tồn tại', 'P0', 'File: mã hợp đồng không có thật; mã hợp đồng đúng nhưng của nhà cung cấp khác',
      ['1. Load, Validate'], '—',
      ['- Mã không có thật: "Mã hợp đồng – Không tồn tại trong hệ thống"', '- Hợp đồng của nhà cung cấp khác: hợp lệ (được phép như trên form)']),
    T('G', '005', 'Mã loại hợp đồng được nhận', 'P1', 'File dùng lần lượt HDMNN, HDMN, HDMTN, HDMDK và 1 mã khác',
      ['1. Load, Validate'], '—',
      ['- 4 mã trên được nhận; mã khác báo "Loại hợp đồng – Chỉ nhận HDMNN / HDMN / HDMTN / HDMDK"']),
    T('G', '006', 'Import trùng khai báo đã có', 'P1', 'HĐ-2 + tài khoản 3311 đã khai báo cho NCC-1',
      ['1. File có dòng NCC-1 + HĐ-2 + 3311', '2. Validate'], '—',
      ['- "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này"']),
    T('S', '007', 'Import loại tiền, tỷ giá', 'P1', 'File: dòng USD không tỷ giá; dòng USD tỷ giá 0; dòng "VNĐ" và dòng "VND" không tỷ giá; dòng bỏ trống loại tiền',
      ['1. Load, Validate'], '—',
      ['- USD không tỷ giá: "Tỷ giá – Bắt buộc phải nhập"; tỷ giá 0: "Tỷ giá – Phải lớn hơn 0."',
       '- VNĐ / VND: hợp lệ, sau Import tỷ giá 1', '- Trống loại tiền: "Loại tiền – Bắt buộc phải nhập"']),
    T('M', '008', 'File quá 500 dòng', 'P2', 'File 501 dòng dữ liệu',
      ['1. Chọn file, bấm "Load lên bảng"'], '—',
      ['- Báo vượt 500 dòng mỗi lần, không load']),
    T('M', '009', 'Dòng bị người khác khai báo trùng sau Validate', 'P2', '2 tài khoản cùng import 1 file có HĐ-2 + 3311 của NCC-1',
      ['1. Cả 2 Validate xong', '2. Người thứ nhất bấm Import', '3. Người thứ hai bấm Import'], '—',
      ['- Người thứ hai: dòng HĐ-2 bị bỏ qua với lý do "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này", các dòng khác vẫn nhập']),
]

# ------------------------------------------------------------------ VIII. XUẤT / IN
S8 = [
    T('S', '001', 'Xuất Excel: chọn trường trước khi xuất', 'P0', 'Đang lọc từ khóa "TCX"',
      ['1. Bấm Xuất Excel', '2. Xem các trường tích sẵn', '3. Bỏ tích Người tạo, kéo Dư có lên trên Dư nợ, tích thêm Tỷ giá, Quy đổi (VND), bấm Xuất file'], '—',
      ['- Cửa sổ "Chọn trường xuất file" tích sẵn đúng các cột đang hiện; "Đang chọn 8/15 trường"',
       '- Cạnh nút có dòng tiến độ; xong báo "Xuất Excel thành công"',
       '- File khai_bao_dau_ky_cong_no_ncc.xlsx, tiêu đề "DANH SÁCH CÔNG NỢ ĐẦU KỲ THEO NHÀ CUNG CẤP - HỢP ĐỒNG"; chỉ các dòng khớp bộ lọc (mọi trang), cột đúng thứ tự đã kéo',
       '- Cột Tỷ giá, Dư nợ, Dư có, Quy đổi (VND) là SỐ (SUM được), định dạng 1,234,567']),
    T('S', '002', 'In danh sách', 'P0', 'Đang lọc từ khóa "TPE_DKNCC_013"',
      ['1. Bấm In danh sách', '2. Bấm In'], '—',
      ['- Cửa sổ "Xem trước khai báo đầu kỳ công nợ nhà cung cấp" khổ ngang, có tiêu đề công ty, tiêu đề "KHAI BÁO CÔNG NỢ ĐẦU KỲ NHÀ CUNG CẤP"',
       '- Bảng in đúng các cột đang hiện (không có Hành động), đúng các dòng khớp bộ lọc',
       '- Dư nợ / Dư có / Tỷ giá in 2 chữ số thập phân (22,320.00, 42,963.60)', '- Chân bản in "Ngày ..... Tháng ..... Năm .....", "Người lập"',
       '- Bấm In mở hộp in của trình duyệt']),
    T('G', '003', 'In danh sách quá 2,000 dòng', 'P1', 'TK-ALL, không lọc gì, phạm vi hơn 2,000 khai báo',
      ['1. Bấm In danh sách'], '—',
      ['- Không in; báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được…" kèm gợi ý thu hẹp bộ lọc']),
    T('M', '004', 'Xuất Excel khi không có dữ liệu', 'P2', 'Lọc từ khóa "KHONG-TON-TAI"',
      ['1. Bấm Xuất Excel, Xuất file'], '—',
      ['- Báo "Không có dữ liệu để xuất", không tải file']),
]

# ------------------------------------------------------------------ IX. RÀNG BUỘC
S9 = [
    T('G', '001', 'Trùng hợp đồng trên cùng form', 'P0', 'HĐ-1 đã có trên form',
      ['1. Thử chọn lại HĐ-1 trong cửa sổ'], '—',
      ['- Không thêm được (dòng "Đã chọn")']),
    T('S', '002', 'Trùng với khai báo đã có', 'P0', '2 người cùng mở trang Thêm, cùng chọn HĐ-1 + tài khoản 3311 của NCC-1',
      ['1. Người thứ nhất bấm Lưu', '2. Người thứ hai bấm Lưu'], '—',
      ['- Người thứ hai: dưới ô Tài khoản "Đã khai báo đầu kỳ cho tài khoản này"', '- Không lưu dòng nào trong lần đó']),
    T('S', '003', 'Công nợ bằng 0 hoặc để trống', 'P0', '—',
      ['1. Để trống Công nợ, Lưu', '2. Nhập 0, Lưu'], '—',
      ['- Trống: "Bắt buộc phải nhập"', '- 0: báo phải lớn hơn 0', '- Ô tiền không cho gõ dấu âm']),
    T('S', '004', 'Tỷ giá khi khác VNĐ', 'P0', 'Dòng USD',
      ['1. Xóa trống ô Tỷ giá, Lưu', '2. Nhập 0, Lưu'], '—',
      ['- Trống: "Bắt buộc phải nhập" dưới ô Tỷ giá (báo cùng lượt với các ô lỗi khác)', '- 0: báo lỗi phải lớn hơn 0',
       '- Tỷ giá nhận số thập phân lớn hơn 0']),
]

# ------------------------------------------------------------------ X. ĐỒNG THỜI
S10 = [
    T('S', '001', 'Mã phiếu không trùng khi 2 người lưu cùng lúc', 'P1', '2 tài khoản cùng công ty',
      ['1. Hai người cùng lập khai báo (hợp đồng khác nhau), bấm Lưu gần như đồng thời', '2. Một người bấm Lưu 2 lần liền'], '—',
      ['- 2 khai báo có 2 mã nối tiếp, không trùng, không lỗi', '- Bấm Lưu 2 lần liền chỉ tạo 1 lần']),
    T('S', '002', 'Khai báo vừa phát sinh chứng từ trong lúc người khác đang sửa', 'P1',
      'A đang mở trang Sửa khai báo Z; B lập phiếu chi cho hợp đồng của Z (cùng nhà cung cấp, cùng tài khoản)',
      ['1. A bấm Lưu'], '—',
      ['- A bị từ chối với câu "Khai báo đã phát sinh chứng từ, không được sửa / xóa.", dữ liệu không đổi']),
]

# ------------------------------------------------------------------ XI. LUỒNG ĐẦU CUỐI
S11 = [
    T('S', '001', 'Luồng đầu cuối: khai báo, chi tiền, bị khóa, mở lại', 'P0', 'NCC-1 có HĐ-1 chưa khai báo',
      ['1. Lập khai báo Dư có 1,000.25 USD tỷ giá 25,450.5, tài khoản 3311 cho HĐ-1', '2. Đối chiếu ' + SO,
       '3. Lập phiếu chi / ủy nhiệm chi cho HĐ-1 (ghi sổ tài khoản 3311), quay lại danh sách khai báo',
       '4. Xóa / hủy ghi sổ phiếu chi đó, quay lại danh sách'], '—',
      ['- Bước 2: sổ có bút toán Có 3311 nguyên tệ 1,000.25, quy đổi 25,456,863, chứng từ là mã phiếu khai báo',
       '- Bước 3: dòng khai báo không còn Sửa, Xóa; chi tiết chỉ còn Quay lại', '- Bước 4: khai báo có lại Sửa, Xóa']),
    T('S', '002', 'Luồng đầu cuối: import, sửa, xem lịch sử, xóa', 'P1', 'File import 1 dòng hợp lệ',
      ['1. Import', '2. Sửa số tiền', '3. Xem Lịch sử', '4. Xóa'], '—',
      ['- Mỗi bước bút toán trong sổ đổi theo; xóa xong không còn bút toán', '- Lịch sử có "Tạo mới" và "Thay đổi thông tin"']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP KHAI BÁO — CHỌN NHÀ CUNG CẤP & HỢP ĐỒNG', S4),
    ('V', 'XEM CHI TIẾT, SỬA & LỊCH SỬ', S5),
    ('VI', 'XÓA', S6),
    ('VII', 'IMPORT EXCEL', S7),
    ('VIII', 'XUẤT EXCEL / IN', S8),
    ('IX', 'RÀNG BUỘC NHẬP LIỆU', S9),
    ('X', 'THAO TÁC ĐỒNG THỜI', S10),
    ('XI', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S11),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + L.NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
    total = sum(TAGS.values())
    print('Thống kê so với bản cũ (%d case): giữ %d, sửa %d, thêm %d, bỏ %d -> tổng %d'
          % (SO_CU, TAGS['G'], TAGS['S'], TAGS['M'], len(BO), total))
    assert TAGS['G'] + TAGS['S'] + len(BO) == SO_CU, 'giữ + sửa + bỏ phải bằng %d case cũ' % SO_CU
