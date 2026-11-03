# -*- coding: utf-8 -*-
"""Testcase màn "Khai báo đầu kỳ công nợ" (STT 167, phân hệ Tài chính > Khai báo đầu kỳ) — MÀN MẪU nhóm PHIẾU đợt 3.

Chép từ ../../gen_testcase.py (02/10/2026, bản HRM có dòng "Đối chiếu ERP", 74 case màn khách hàng) rồi RÀ LẠI từng
case theo code HRM hiện tại (develop, 02/11/2026):
  - menu thật (Tài chính > Khai báo đầu kỳ; lối thứ 2 Kế toán công nợ > Khách hàng), nhãn / thông báo nguyên văn;
  - BỎ mọi câu "Đối chiếu ERP", case đối chiếu dữ liệu với ERP và case "gọi thẳng chức năng bằng công cụ kiểm thử API";
  - code đã đổi sau 02/10: Quá hạn + Ngày BGNT (#11562/#11584), bỏ "Ngày tính công nợ" khỏi form và danh sách (#11565),
    nhãn ô lọc "Mã hợp đồng" / "Số tiền", nút "Lưu và tiếp tục" (#11555), Người tạo "Họ tên - Mã phòng" (#11566),
    file mẫu import thêm 2 cột quá hạn, bỏ dòng mô tả (#11563), import bỏ qua dòng vừa bị trùng (#11629);
  - kiểm số liệu sổ sách bằng báo cáo HRM (Chi tiết công nợ KH / Đối chiếu công nợ 1 KH) thay vì sổ bên ERP.
Mỗi case gắn nhãn: G = giữ nguyên, S = sửa, M = thêm mới. Case bỏ ghi ở BO. Cuối file in thống kê.
Màn 168 (NCC) dùng chung code: bản cũ của NCC vẫn ở ../../gen_testcase.py (cấu hình NCC) — rà theo cùng cách này.
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

TEN = 'Khai báo đầu kỳ công nợ'
MODULE = 'Khai báo đầu kỳ công nợ KH'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SO_CU = 74
TAGS = Counter()

BO = {
    'TC-ROLE-07': 'Gọi thẳng Thêm / Sửa / Xóa bằng công cụ kiểm thử API khi không có quyền',
    'TC-ROLE-08': 'Gọi thẳng Sửa / Xóa khai báo đã phát sinh bằng công cụ kiểm thử API (thay bằng TC_10.002 qua giao diện)',
    'TC_09.004': 'Gọi thẳng chức năng Thêm với tài khoản tổng hợp / đang khóa (tester kỹ thuật)',
    'TC_09.005': 'Gọi thẳng chức năng Thêm với hợp đồng của khách hàng khác (đã có ở Import TC_07.004)',
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


MENU = 'phân hệ Tài chính > menu Khai báo đầu kỳ > "Khai báo đầu kỳ công nợ"'
MENU2 = 'phân hệ Tài chính > menu Kế toán công nợ > nhóm Khách hàng > "Công nợ đầu kỳ theo khách hàng - hợp đồng"'
BC = 'phân hệ Bán hàng > Báo cáo > Báo cáo công nợ > "Chi tiết công nợ KH"'
KH = '75TPHXCH-2 - CÔNG TY CỔ PHẦN KIM LONG MOTORS HUẾ'
HD1 = 'HĐ_TPE_HN_KD3_26_0826_PO2610-1710'
HD2 = '57/2026/HĐCCLĐ/KLM-EG'
TK = '1311 - Phải thu của khách hàng ngắn hạn'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '- TK-A: nhân viên công ty TPE, có quyền "Quản lý công nợ đầu kỳ" + "Xem tất cả công nợ đầu kỳ của công ty".',
    '- TK-ALL: có "Quản lý công nợ đầu kỳ" + "Xem tất cả công nợ đầu kỳ". TK-Z: KHÔNG có "Quản lý công nợ đầu kỳ".',
    '- Khách hàng KH-1: ' + KH + '; hợp đồng HĐ-1: ' + HD1 + ' (hợp đồng hãng), HĐ-2: ' + HD2 + ' (hợp đồng đầu kỳ), cả 2 chưa khai báo.',
    '- Khai báo Z: lập bằng TK-A cho KH-1 + HĐ-1 + tài khoản ' + TK + ', Dư nợ 1,500,000 (chưa có chứng từ công nợ).',
    '- Khai báo Y: một khai báo thật đã có phiếu thu / phiếu kế toán trên cùng khách hàng + hợp đồng + tài khoản (dev: ETEK GREEN.CNĐKHĐ.03395).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Khai báo đầu kỳ công nợ" khai báo SỐ DƯ CÔNG NỢ ĐẦU KỲ của khách hàng theo từng hợp đồng × tài khoản — số mở '
        'đầu cho sổ chi tiết công nợ và các báo cáo công nợ khách hàng.',
        'Luồng: chọn khách hàng → "Chọn hợp đồng" (một hoặc nhiều) → mỗi dòng nhập Tài khoản, Loại dư, Công nợ (Quá hạn, Ngày '
        'BGNT nếu có) → Lưu. Mỗi dòng thành 1 khai báo riêng (1 mã phiếu, 1 bút toán), KHÔNG qua duyệt.',
        'Đường vào: ' + MENU + '; lối thứ 2: ' + MENU2 + '.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới, Sửa, Xem chi tiết, Xóa, Lịch sử, '
        'In danh sách, Xuất Excel, Import Excel.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi xem (xét lần lượt, gặp quyền nào trước thì dùng quyền đó):',
        '- "Xem tất cả công nợ đầu kỳ": mọi công ty; khu vực lọc có ô Công ty, Phòng ban, Bộ phận.',
        '- "Xem tất cả công nợ đầu kỳ của công ty": công ty đang làm việc; có ô Phòng ban, Bộ phận.',
        '- "… của phòng ban" / "… của bộ phận": các phòng ban / bộ phận được giao quản lý.',
        '- Không có quyền nào ở trên: chỉ khai báo do chính mình tạo.',
        'Công ty / phòng ban / bộ phận của khai báo = của NGƯỜI LẬP HỢP ĐỒNG.',
        'Cửa sổ "Chọn hợp đồng / đơn hàng" chỉ hiện hợp đồng THUỘC khách hàng đang chọn: hợp đồng bán đã duyệt / có hiệu '
        'lực, hợp đồng hãng có hiệu lực, hợp đồng gói dịch vụ, hợp đồng dự án (khác Đang tạo), hợp đồng đầu kỳ, hợp đồng mua.',
        'Tài khoản chọn được: mọi tài khoản chi tiết (không có tài khoản con) đang hoạt động.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Khai báo ngoài phạm vi xem: không hiện; mở đường dẫn trực tiếp thì sang trang "Không tìm thấy".',
        '- Trong cửa sổ chọn hợp đồng: hợp đồng đã có khai báo của khách hàng này hiện mờ, Tình trạng "Đã khai báo", không '
        'chọn được; hợp đồng đã có trên form ghi "Đã chọn".',
        '- Nút Sửa / Xóa ẨN HẲN khi khai báo ĐÃ PHÁT SINH CHỨNG TỪ: cùng khách hàng + hợp đồng + tài khoản đã có phiếu thu, '
        'phiếu chi, phiếu báo có, ủy nhiệm chi hoặc phiếu kế toán ghi sổ, hoặc có chứng từ trừ thẳng vào khai báo.',
        '- Phiếu xuất / nhập hàng, hạch toán dịch vụ trên cùng hợp đồng KHÔNG làm khai báo bị khóa.',
        '- Tài khoản đang khóa: không chọn mới được; khai báo cũ đang dùng thì vẫn hiện kèm biểu tượng khóa.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" (Từ – Đến) lọc theo ngày lập khai báo, tính cả 2 đầu mút.',
        'Ô "Ngày BGNT" (Từ – Đến) lọc theo ngày bàn giao nghiệm thu của khai báo quá hạn.',
        'Ngày hạch toán của khai báo = "Ngày khai báo đầu kỳ" cấu hình ở Khai Quy chế – Cấu hình của công ty người lập; '
        'không hiện trên màn, không phải ô lọc. Bộ lọc được ghi nhớ 10 phút khi rời màn rồi quay lại.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Một lần lập = 1 khách hàng × nhiều hợp đồng; mỗi dòng lưu thành 1 khai báo (mã <mã công ty>.CNĐKHĐ.<5 chữ số>).',
        'Khai báo gồm: Mã phiếu, Khách hàng, Loại hợp đồng, Số hợp đồng, Tài khoản, Loại dư, Công nợ, Quá hạn, Ngày BGNT, '
        'Người tạo / Ngày tạo, Người cập nhật / Ngày cập nhật.',
        'Trang Sửa và Chi tiết chỉ có 1 dòng; Mã phiếu, Khách hàng và hợp đồng không đổi được.',
        'Trạng thái (hệ thống tự xác định): Chưa phát sinh chứng từ (Sửa, Xóa được) → Đã phát sinh chứng từ (chỉ xem); '
        'chứng từ bị xóa / hủy ghi sổ thì khai báo trở lại Chưa phát sinh.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Không trùng: cùng khách hàng + hợp đồng + tài khoản chỉ khai báo 1 lần (kể cả trên cùng form, khi Sửa đổi tài '
        'khoản và khi import).',
        '- Công nợ phải lớn hơn 0. Dư nợ ghi Nợ, Dư có ghi Có tài khoản.',
        '- Chỉ Dư nợ được đánh dấu Quá hạn; Quá hạn thì Ngày BGNT bắt buộc, không lớn hơn hôm nay.',
        '- Hợp đồng phải thuộc khách hàng đang chọn.',
        '- Sửa / Xóa khai báo thì bút toán sổ chi tiết đổi / mất theo.',
    )),
    ('7. Phân quyền cấp', L_(
        '- "Quản lý công nợ đầu kỳ": thấy 2 mục menu, vào màn, xem, thêm, sửa, xóa, import, in, xuất (1 quyền cho cả màn).',
        '- 4 quyền phạm vi xem như mục 2 (dùng chung với màn Khai báo đầu kỳ công nợ nhà cung cấp).',
        '- Quyền gán ở màn Phân quyền của HRM, nhóm "Khai báo đầu kỳ công nợ".',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N": N = tổng khai báo khớp bộ lọc và phạm vi quyền.',
        'Cột "Dư nợ" chỉ có số khi Loại dư = Dư nợ, cột "Dư có" chỉ có số khi Loại dư = Dư có; cột còn lại để TRỐNG.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '- Số theo chuẩn quốc tế: 1,500,000 · 2,750,000.5.',
        '- Bản in tối đa 2,000 dòng; vượt thì báo phải thu hẹp bộ lọc.',
        '- Tiêu đề cửa sổ Lịch sử dùng MÃ PHIẾU (khai báo không có tên riêng).',
        '- Kiểm sổ sách: sau Lưu / Sửa / Xóa mở báo cáo ' + BC + ' của khách hàng để thấy số dư đầu kỳ đổi theo.',
        '- Cột kết quả / check để trống cho tester điền.',
    )),
]

# ------------------------------------------------------------------ PHÂN QUYỀN
ROLE_TCS = [
    T('S', '00', 'Không có quyền "Quản lý công nợ đầu kỳ" thì không thấy màn', 'P0',
      'TK-Z không có quyền "Quản lý công nợ đầu kỳ"',
      ['1. Đăng nhập bằng TK-Z', '2. Mở phân hệ Tài chính, menu Khai báo đầu kỳ và menu Kế toán công nợ > Khách hàng',
       '3. Dán đường dẫn màn danh sách và trang Thêm lên thanh địa chỉ'],
      'Tài khoản TK-Z',
      ['- Menu Khai báo đầu kỳ KHÔNG có "Khai báo đầu kỳ công nợ"; nhóm Khách hàng KHÔNG có "Công nợ đầu kỳ theo khách hàng - hợp đồng"',
       '- Dán đường dẫn: chuyển sang trang "Không tìm thấy", không lộ dữ liệu']),
    T('S', '01', 'Có quyền "Quản lý công nợ đầu kỳ": đủ chức năng', 'P0',
      'TK-A có quyền "Quản lý công nợ đầu kỳ" + "Xem tất cả công nợ đầu kỳ của công ty"',
      ['1. Đăng nhập bằng TK-A', '2. Vào ' + MENU],
      'Tài khoản TK-A',
      ['- Danh sách hiện, chân bảng "Hiển thị 1–10 / N"',
       '- Có nút Tạo mới, Import Excel, Xuất Excel, In danh sách, Cấu hình cột hiển thị',
       '- Khai báo Chưa phát sinh có Sửa, Xóa, Lịch sử; khai báo Đã phát sinh chỉ có Lịch sử']),
    T('S', '02', 'Phạm vi xem: "Xem tất cả công nợ đầu kỳ"', 'P0',
      'TK-ALL có "Quản lý công nợ đầu kỳ" + "Xem tất cả công nợ đầu kỳ"',
      ['1. Đăng nhập TK-ALL, vào màn', '2. Đọc N ở chân bảng, bấm Tìm kiếm nâng cao'],
      '—',
      ['- Thấy khai báo của MỌI công ty',
       '- Khu vực lọc có ô Công ty, Phòng ban, Bộ phận (Phòng ban, Bộ phận khóa tới khi chọn cấp trên)']),
    T('S', '03', 'Phạm vi xem: "Xem tất cả công nợ đầu kỳ của công ty"', 'P0',
      'TK-A như TC-ROLE-01, công ty TPE',
      ['1. Đăng nhập TK-A, vào màn', '2. Bấm Tìm kiếm nâng cao', '3. Lọc Phòng ban = HN_KD3'],
      '—',
      ['- Chỉ thấy khai báo có công ty = TPE (công ty của NGƯỜI LẬP HỢP ĐỒNG)',
       '- Không có ô Công ty; có ô Phòng ban, Bộ phận', '- Lọc Phòng ban ra khai báo của hợp đồng do nhân viên HN_KD3 lập']),
    T('S', '04', 'Phạm vi xem: "Xem tất cả công nợ đầu kỳ của phòng ban"', 'P1',
      'TK-PB có "Quản lý công nợ đầu kỳ" + quyền phòng ban, được giao quản lý phòng HN_KD3',
      ['1. Đăng nhập TK-PB, vào màn'],
      '—',
      ['- Chỉ thấy khai báo thuộc phòng ban được giao quản lý (theo người lập hợp đồng)']),
    T('S', '05', 'Phạm vi xem: "Xem tất cả công nợ đầu kỳ của bộ phận"', 'P1',
      'TK-BP có "Quản lý công nợ đầu kỳ" + quyền bộ phận, được giao quản lý 1 bộ phận',
      ['1. Đăng nhập TK-BP, vào màn'],
      '—',
      ['- Chỉ thấy khai báo thuộc bộ phận được giao quản lý']),
    T('S', '06', 'Không có quyền phạm vi nào: chỉ thấy khai báo mình tạo', 'P0',
      'TK-F có "Quản lý công nợ đầu kỳ" nhưng không có quyền phạm vi nào; TK-F đã tạo khai báo Z',
      ['1. Đăng nhập TK-F, vào màn', '2. Dán đường dẫn trang Chi tiết của một khai báo do người khác tạo'],
      '—',
      ['- Chỉ hiện khai báo do TK-F tạo', '- Khu vực lọc KHÔNG có ô Công ty / Phòng ban / Bộ phận',
       '- Đường dẫn khai báo của người khác: trang "Không tìm thấy"']),
]

# ------------------------------------------------------------------ I. HIỂN THỊ
S1 = [
    T('S', '001', 'Vào màn qua menu', 'P0', 'TK-A',
      ['1. Đăng nhập TK-A', '2. Vào ' + MENU],
      '—',
      ['- Tiêu đề trang và tiêu đề bảng "Khai báo đầu kỳ công nợ"', '- Bảng 10 dòng, khai báo mới lập nhất đứng đầu',
       '- Không cần bấm Tìm kiếm, bảng tự tải']),
    T('S', '002', 'Bộ cột mặc định', 'P0', 'Tài khoản chưa từng tùy chỉnh cột ở màn này',
      ['1. Mở màn danh sách', '2. Đọc tiêu đề cột từ trái sang phải'],
      '—',
      ['- Đúng thứ tự: STT, Mã phiếu, Khách hàng, Số hợp đồng, Dư nợ, Dư có, Quá hạn, Ngày BGNT, Người tạo, Ngày tạo, Hành động',
       '- Các cột Tài khoản, Loại hợp đồng, Người cập nhật, Ngày cập nhật bật được ở "Cấu hình cột hiển thị"',
       '- KHÔNG có cột "Ngày tính công nợ"']),
    T('S', '003', 'Mã phiếu là đường dẫn vào Chi tiết', 'P1', 'Có khai báo Z',
      ['1. Bấm vào mã phiếu Z', '2. Quay lại, bấm chuột phải vào mã phiếu'],
      '—',
      ['- Bấm trái mở trang "Chi tiết khai báo đầu kỳ công nợ: <mã phiếu>"', '- Chuột phải có "Mở liên kết trong tab mới"']),
    T('G', '004', 'Số hợp đồng mở chứng từ gốc', 'P2', 'Khai báo gắn hợp đồng hãng / hợp đồng đầu kỳ',
      ['1. Bấm vào số hợp đồng trên dòng'],
      '—',
      ['- Mở tab mới tới trang xem hợp đồng', '- Hợp đồng chưa có trang xem thì hiện chữ thường, không bấm được']),
    T('S', '005', 'Định dạng số, ngày, ô trống', 'P1', 'Có khai báo Dư có số lẻ (vd 2,750,000.5) và khai báo Dư nợ',
      ['1. Tìm 2 khai báo trên', '2. Đọc cột Dư nợ, Dư có, Quá hạn, Ngày BGNT, Người tạo, Ngày tạo'],
      '—',
      ['- Dư có hiện "2,750,000.5", cột Dư nợ cùng dòng để TRỐNG (không 0, không gạch)', '- Quá hạn "Có" / "Không"; không quá hạn thì Ngày BGNT trống',
       '- Người tạo dạng "Họ tên - Mã phòng ban"; Ngày tạo dd/mm/yyyy HH:mm']),
    T('S', '006', 'Lối vào thứ hai: Kế toán công nợ > Khách hàng', 'P0', 'TK-A',
      ['1. Vào ' + MENU2, '2. So với danh sách mở từ menu Khai báo đầu kỳ'],
      '—',
      ['- Mở CÙNG màn "Khai báo đầu kỳ công nợ", cùng N khai báo, cùng nút']),
]

# ------------------------------------------------------------------ II. LỌC
S2 = [
    T('S', '001', 'Ô tìm nhanh theo mã phiếu, số hợp đồng, mã / tên khách hàng', 'P0', 'Có khai báo của KH-1',
      ['1. Gõ "KIM LONG" vào ô tìm nhanh (chưa bấm gì)', '2. Nhấn Enter', '3. Lần lượt tìm theo một mã phiếu và một số hợp đồng'],
      'Tìm nhanh: KIM LONG',
      ['- Đang gõ thì bảng chưa đổi; Enter hoặc nút Tìm kiếm mới lọc',
       '- Ra đúng khai báo của khách hàng có tên chứa từ khóa', '- Tìm theo mã phiếu / số hợp đồng ra đúng khai báo chứa chuỗi đó',
       '- Placeholder "Tìm theo mã phiếu, số hợp đồng, mã hoặc tên khách hàng"']),
    T('G', '002', 'Lọc theo Khách hàng (gõ để tìm)', 'P0', 'KH-1 có khai báo',
      ['1. Mở Tìm kiếm nâng cao', '2. Ô Khách hàng gõ 1 ký tự, rồi gõ "75TPHXCH-2"', '3. Chọn khách hàng trong gợi ý', '4. F5 trang'],
      'Khách hàng: 75TPHXCH-2',
      ['- Gõ 1 ký tự: báo cần gõ thêm, chưa tìm', '- Chọn xong bảng tự lọc, chỉ còn khai báo của KH-1',
       '- F5: ô Khách hàng vẫn hiện đúng tên đã chọn']),
    T('S', '003', 'Lọc theo Tài khoản', 'P1', 'Có khai báo tài khoản 1311 và 1312',
      ['1. Ô Tài khoản chọn "' + TK + '"', '2. Đổi sang "1312 - Phải thu khách hàng dài hạn"'],
      'Tài khoản: 1311 / 1312',
      ['- Chọn là lọc ngay', '- Bật cột Tài khoản: mọi dòng đúng tài khoản đã chọn']),
    T('S', '004', 'Lọc theo Loại hợp đồng', 'P1', 'Có khai báo gắn hợp đồng đầu kỳ',
      ['1. Ô Loại hợp đồng chọn "Hợp đồng đầu kỳ"'],
      'Loại hợp đồng: Hợp đồng đầu kỳ',
      ['- Chỉ còn khai báo gắn hợp đồng đầu kỳ; bật cột Loại hợp đồng thấy đúng tên loại']),
    T('S', '005', 'Lọc theo Mã hợp đồng', 'P1', 'Có khai báo gắn HĐ-1',
      ['1. Ô Mã hợp đồng gõ "KD3_26_0826"', '2. Nhấn Enter'],
      'Mã hợp đồng: KD3_26_0826',
      ['- Chờ Enter mới lọc', '- Ra khai báo có số hợp đồng chứa chuỗi đã gõ, với MỌI loại hợp đồng']),
    T('S', '006', 'Lọc theo Loại dư', 'P0', 'Có cả khai báo Dư nợ và Dư có',
      ['1. Ô Loại dư chọn "Dư nợ"', '2. Đổi sang "Dư có"'],
      'Loại dư: Dư nợ / Dư có',
      ['- Chọn là lọc ngay', '- Dư nợ: mọi dòng chỉ có số ở cột Dư nợ', '- Dư có: mọi dòng chỉ có số ở cột Dư có']),
    T('S', '007', 'Lọc theo khoảng Số tiền', 'P1', 'Có khai báo 1,500,000 và 10,125,000',
      ['1. Ô Số tiền nhập Từ 1,000,000, Đến 5,000,000', '2. Nhấn Enter'],
      'Số tiền từ 1,000,000 đến 5,000,000',
      ['- Chỉ còn khai báo có số tiền trong khoảng (tính cả 2 đầu, cả Dư nợ lẫn Dư có)', '- Không có 10,125,000']),
    T('S', '008', 'Lọc theo Người tạo / Người cập nhật', 'P2', 'Có khai báo do TK-A tạo',
      ['1. Ô Người tạo chọn nhân viên của TK-A', '2. Xóa, rồi ô Người cập nhật chọn cùng người'],
      '—',
      ['- Chỉ còn khai báo do người đó tạo / cập nhật lần cuối']),
    T('G', '009', 'Lọc theo Ngày tạo (khoảng)', 'P1', 'Có khai báo tạo ngày 15/10/2026',
      ['1. Ô Ngày tạo chọn từ 15/10/2026 đến 15/10/2026'],
      'Ngày tạo: 15/10/2026 – 15/10/2026',
      ['- Ra đúng các khai báo tạo trong ngày đó, kể cả lúc 23:59']),
    T('S', '010', 'Lọc theo Công ty / Phòng ban / Bộ phận', 'P1', 'TK-ALL',
      ['1. Ô Công ty chọn TPE', '2. Ô Phòng ban chọn một phòng', '3. Đổi Công ty'],
      '—',
      ['- Mỗi ô chọn xong là lọc ngay', '- Phòng ban, Bộ phận chỉ mở sau khi chọn cấp trên', '- Đổi Công ty thì Phòng ban, Bộ phận tự xóa']),
    T('G', '011', 'Làm mới xóa hết điều kiện và tải lại', 'P1', 'Đang lọc Loại dư = Dư nợ và từ khóa "KIM LONG"',
      ['1. Bấm Làm mới'], '—',
      ['- Mọi ô lọc về trống, bảng nạp lại toàn bộ phạm vi']),
    T('G', '012', 'Ghi nhớ bộ lọc khi vào chi tiết rồi quay lại', 'P1', 'Đang lọc Loại dư = Dư có',
      ['1. Bấm vào một mã phiếu', '2. Bấm Quay lại'], '—',
      ['- Bộ lọc vẫn còn Loại dư = Dư có']),
    T('M', '013', 'Lọc theo Quá hạn và Ngày BGNT', 'P1', 'Có khai báo quá hạn, Ngày BGNT 30/10/2023',
      ['1. Ô Quá hạn chọn "Có"', '2. Ô Ngày BGNT chọn từ 01/10/2023 đến 31/10/2023', '3. Ô Quá hạn đổi sang "Không", xóa Ngày BGNT'],
      'Quá hạn: Có / Không',
      ['- Bước 1: mọi dòng cột Quá hạn "Có"', '- Bước 2: chỉ còn khai báo có Ngày BGNT trong tháng 10/2023',
       '- Bước 3: mọi dòng "Không", Ngày BGNT trống']),
    T('M', '014', 'Cài đặt bộ lọc', 'P2', '—',
      ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Người cập nhật", kéo "Loại dư" lên đầu, bấm Lưu', '3. F5 trang', '4. Mở lại, bấm Khôi phục mặc định'],
      '—',
      ['- Cửa sổ liệt kê 12 ô lọc kèm số thứ tự', '- Sau Lưu và F5: ô Người cập nhật ẩn, Loại dư đứng đầu',
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
      ['1. Bấm biểu tượng Cấu hình cột', '2. Bật cột Tài khoản, Loại hợp đồng, bấm Lưu', '3. F5 trang'], '—',
      ['- 2 cột mới hiện; sau F5 vẫn còn', '- Cột STT, Mã phiếu có biểu tượng khóa, không bỏ được']),
    T('S', '004', 'Nút Sửa / Xóa ẩn với khai báo đã phát sinh chứng từ', 'P0', 'Khai báo Y (đã phát sinh) và khai báo Z (chưa)',
      ['1. Tìm 2 dòng Y và Z'], '—',
      ['- Dòng Y chỉ có nút Lịch sử, KHÔNG có Sửa / Xóa (ẩn hẳn, không hiện xám)', '- Dòng Z có Sửa, Xóa, Lịch sử']),
    T('S', '005', 'Phiếu xuất hàng KHÔNG làm khóa khai báo', 'P0',
      'Hợp đồng H đã có phiếu xuất hàng ghi sổ tài khoản 1311, chưa có phiếu thu / chi / kế toán; vừa tạo khai báo trên H',
      ['1. Mở danh sách, tìm khai báo vừa tạo'], '—',
      ['- Vẫn có nút Sửa, Xóa', '- Lập phiếu thu / phiếu kế toán cho H thì nút Sửa / Xóa biến mất (TC_11.001)']),
]

# ------------------------------------------------------------------ IV. THÊM MỚI
S4 = [
    T('S', '001', 'Mở trang Thêm mới', 'P0', 'TK-A',
      ['1. Bấm Tạo mới'], '—',
      ['- Tiêu đề "Thêm khai báo đầu kỳ công nợ"; góc phải khối Thông tin chung "<tên TK-A> - <ngày giờ hiện tại>"',
       '- Khối "Thông tin chung" có ô Khách hàng (*), placeholder "Nhập mã/tên khách hàng"',
       '- Khối "Danh sách hợp đồng" có nút "Chọn hợp đồng", bảng trống ghi "Chưa chọn hợp đồng nào — bấm "Chọn hợp đồng" để thêm."',
       '- Cột: STT, Loại hợp đồng, Số hợp đồng, Tài khoản *, Loại dư *, Công nợ *, Quá hạn, Ngày BGNT *, nút xóa dòng',
       '- Chân trang: Lưu, Lưu và tiếp tục, Quay lại']),
    T('G', '002', 'Chưa chọn khách hàng thì không mở được cửa sổ chọn hợp đồng', 'P0', '—',
      ['1. Bấm "Chọn hợp đồng" khi ô Khách hàng còn trống'], '—',
      ['- Không mở cửa sổ', '- Báo đỏ dưới ô Khách hàng: "Chọn khách hàng trước khi chọn hợp đồng"']),
    T('S', '003', 'Ô Khách hàng tìm từ máy chủ', 'P1', 'KH-1',
      ['1. Gõ 1 ký tự', '2. Gõ "75TPHXCH-2"'], 'Khách hàng: 75TPHXCH-2',
      ['- Dưới 2 ký tự: báo cần gõ thêm', '- Gợi ý dạng "Mã - Tên"']),
    T('S', '004', 'Cửa sổ chọn hợp đồng: danh sách và tình trạng', 'P0', 'KH-1 có hợp đồng đầu kỳ 11/2026/HĐCCCLD/KLM đã khai báo',
      ['1. Chọn KH-1, bấm "Chọn hợp đồng"'], '—',
      ['- Tiêu đề "Chọn hợp đồng / đơn hàng", dòng phụ "Khách hàng: ' + KH + '"',
       '- Cột: STT, Loại hợp đồng, Số hợp đồng, Tổng thanh toán, Người tạo, Ngày tạo, Tình trạng',
       '- Hợp đồng đã khai báo: dòng mờ, Tình trạng "Đã khai báo"',
       '- Có ô Loại hợp đồng, Số hợp đồng; nút Tìm kiếm, Làm mới; phân trang "Hiển thị 1–10 / N"; nút Đóng']),
    T('S', '005', 'Bấm vào dòng là thêm hợp đồng ngay', 'P0', 'Đang mở cửa sổ chọn hợp đồng của KH-1',
      ['1. Bấm dòng HĐ-1', '2. Bấm dòng HĐ-2', '3. Bấm lại dòng HĐ-1', '4. Bấm một dòng "Đã khai báo"', '5. Bấm Đóng'], '—',
      ['- Mỗi lần bấm hiện "Đã thêm hợp đồng <số hợp đồng>", cửa sổ vẫn mở',
       '- Dòng đã chọn chuyển "Đã chọn", bấm lại không thêm trùng', '- Dòng "Đã khai báo" bấm không có tác dụng',
       '- Đóng cửa sổ: bảng có đúng 2 dòng, Loại dư mặc định Dư nợ']),
    T('G', '006', 'Lọc trong cửa sổ chọn hợp đồng', 'P1', 'Đang mở cửa sổ',
      ['1. Loại hợp đồng chọn "Hợp đồng đầu kỳ"', '2. Số hợp đồng gõ "KLM", Enter', '3. Bấm Làm mới'], '—',
      ['- Chỉ còn hợp đồng đúng loại / chứa chuỗi', '- Làm mới về toàn bộ hợp đồng của khách hàng']),
    T('S', '007', 'Đủ các nguồn hợp đồng, luôn đúng khách hàng', 'P0', 'Khách hàng có hợp đồng bán, hợp đồng hãng, hợp đồng đầu kỳ',
      ['1. Mở cửa sổ chọn hợp đồng', '2. Lần lượt chọn từng Loại hợp đồng'], '—',
      ['- Có đủ: Hợp đồng hãng, Hợp đồng, Đơn hàng, Hợp đồng nguyên tắc, Hợp đồng thúc đẩy bán, Đơn hàng thúc đẩy bán, '
       'Phụ lục bổ sung, Phụ lục HĐNT, Hợp đồng gói dịch vụ, Hợp đồng dự án, Hợp đồng đầu kỳ, Hợp đồng mua nước ngoài, '
       'Hợp đồng mua ngoài, Hợp đồng mua trong nước',
       '- Mọi kết quả thuộc khách hàng đang chọn', '- Để trống Loại hợp đồng: gộp tất cả nguồn',
       '- Cột Loại hợp đồng của từng dòng đúng tên loại đã lọc (vd lọc "Hợp đồng thúc đẩy bán" thì dòng ghi "Hợp đồng thúc đẩy bán")']),
    T('G', '008', 'Chỉ hợp đồng còn hiệu lực', 'P1', 'Khách hàng có 1 hợp đồng bán Đang tạo và 1 hợp đồng hãng đã thanh lý',
      ['1. Mở cửa sổ chọn hợp đồng'], '—',
      ['- Không thấy 2 hợp đồng trên', '- Hợp đồng bán chỉ hiện khi Đã duyệt / Có hiệu lực; hợp đồng hãng chỉ khi Có hiệu lực']),
    T('S', '009', 'Lưu thành công nhiều hợp đồng', 'P0', 'Đã chọn HĐ-1, HĐ-2 của KH-1',
      ['1. Dòng 1: Tài khoản 1311, Dư nợ, Công nợ 1,500,000', '2. Dòng 2: Tài khoản (tự lấy theo dòng 1), Dư có, Công nợ 5', '3. Bấm Lưu',
       '4. Mở báo cáo ' + BC + ', lọc KH-1'],
      ['Dòng 1: ' + TK + ' / Dư nợ / 1,500,000', 'Dòng 2: ' + TK + ' / Dư có / 5'],
      ['- "Thêm mới thành công.", quay về danh sách', '- Có 2 khai báo mới, mã nối tiếp dạng TPE.CNĐKHĐ.<5 chữ số>',
       '- Báo cáo: số dư đầu kỳ của KH-1 tăng 1,500,000 (nợ) và có thêm 5 (có) trên 2 hợp đồng tương ứng']),
    T('S', '010', 'Bấm Lưu khi chưa nhập đủ', 'P0', 'Đã chọn 2 hợp đồng, chưa nhập Tài khoản, Công nợ',
      ['1. Bấm Lưu', '2. Bấm Lưu thêm 2 lần liên tiếp'], '—',
      ['- Thông báo "Bạn chưa nhập đầy đủ thông tin.", ở lại form',
       '- Dưới ô Tài khoản và ô Công nợ của TỪNG dòng báo đỏ "Bắt buộc phải nhập"; màn tự cuộn tới ô lỗi đầu tiên',
       '- Bấm nhiều lần không chồng nhiều thông báo giống nhau, không tạo khai báo nào']),
    T('G', '011', 'Xóa dòng trên form', 'P1', 'Đã chọn 3 hợp đồng, dòng 3 đang báo lỗi',
      ['1. Bấm nút xóa ở dòng 1'], '—',
      ['- Còn 2 dòng; lỗi vẫn nằm đúng dòng (nay là dòng 2)', '- Hợp đồng vừa xóa chọn lại được trong cửa sổ']),
    T('G', '012', 'Đổi khách hàng thì danh sách hợp đồng bị xóa', 'P1', 'Đã chọn 2 hợp đồng',
      ['1. Đổi ô Khách hàng sang khách hàng khác'], '—',
      ['- Bảng hợp đồng về trống']),
    T('S', '013', 'Cảnh báo khi thoát lúc chưa lưu', 'P1', 'Đã chọn 1 hợp đồng, đã nhập Công nợ',
      ['1. Bấm Quay lại', '2. Bấm "Ở lại"', '3. Bấm Quay lại lần nữa, bấm "Thoát"'], '—',
      ['- Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"',
       '- Ở lại: giữ nguyên dữ liệu', '- Thoát: về danh sách, không lưu gì']),
    T('M', '014', 'Lưu và tiếp tục', 'P1', 'Đã chọn HĐ-2 của KH-1, nhập đủ',
      ['1. Bấm "Lưu và tiếp tục"'], '—',
      ['- "Thêm mới thành công."', '- Ở lại trang Thêm, ô Khách hàng và bảng hợp đồng về trống để lập tiếp',
       '- Danh sách có khai báo vừa lưu']),
    T('M', '015', 'Quá hạn và Ngày BGNT trên form', 'P0', 'Đã chọn 1 hợp đồng',
      ['1. Loại dư = Dư có, thử tích Quá hạn', '2. Đổi Loại dư = Dư nợ, tích Quá hạn', '3. Mở ô Ngày BGNT, thử chọn ngày mai',
       '4. Bỏ trống Ngày BGNT, bấm Lưu', '5. Chọn 30/09/2026, đổi Loại dư sang Dư có'], '—',
      ['- Bước 1: ô Quá hạn bị khóa với Dư có', '- Bước 2: hiện ô Ngày BGNT', '- Bước 3: ngày sau hôm nay không chọn được',
       '- Bước 4: dưới ô Ngày BGNT "Bắt buộc phải nhập", toast "Bạn chưa nhập đầy đủ thông tin."',
       '- Bước 5: tự bỏ tích Quá hạn và xóa Ngày BGNT']),
    T('M', '016', 'Tài khoản dòng sau lấy theo dòng trên', 'P2', 'Đã chọn HĐ-1, dòng 1 chọn tài khoản 1311',
      ['1. Mở cửa sổ, chọn thêm HĐ-2', '2. Đóng cửa sổ'], '—',
      ['- Dòng 2 có sẵn Tài khoản 1311, Loại dư Dư nợ, Công nợ trống']),
    T('M', '017', 'Vào thẳng trang Thêm khi không có quyền', 'P1', 'TK-Z',
      ['1. Đăng nhập TK-Z, dán đường dẫn trang Thêm'], '—',
      ['- Chuyển sang trang "Không tìm thấy", không tạo được gì']),
]

# ------------------------------------------------------------------ V. CHI TIẾT, SỬA, LỊCH SỬ
S5 = [
    T('S', '001', 'Trang Chi tiết', 'P0', 'Khai báo Z',
      ['1. Bấm vào mã phiếu Z'], '—',
      ['- Tiêu đề "Chi tiết khai báo đầu kỳ công nợ: <mã Z>"; góc phải "<người tạo> - <ngày giờ tạo>"',
       '- Khối Thông tin chung: Mã phiếu, Khách hàng — đều khóa', '- Bảng đúng 1 dòng, các ô khóa',
       '- Có khối "Lịch sử" đang thu gọn', '- Chân trang: Sửa, Xóa, Quay lại']),
    T('S', '002', 'Nút ở Chi tiết khớp với dòng ở danh sách', 'P0', 'Khai báo Y (đã phát sinh), Z (chưa)',
      ['1. Mở chi tiết Y', '2. Mở chi tiết Z'], '—',
      ['- Y: chỉ có Quay lại', '- Z: Sửa, Xóa, Quay lại — giống nút ở dòng danh sách']),
    T('S', '003', 'Sửa: chỉ sửa được tài khoản, loại dư, công nợ, quá hạn', 'P0', 'Khai báo Z chưa phát sinh',
      ['1. Bấm Sửa', '2. Đổi Loại dư sang Dư có, Công nợ 2,750,000.5', '3. Bấm Lưu', '4. Mở báo cáo ' + BC + ', lọc KH-1'],
      ['Loại dư: Dư có', 'Công nợ: 2,750,000.5'],
      ['- Tiêu đề "Sửa khai báo đầu kỳ công nợ"; Mã phiếu, Khách hàng, hợp đồng bị khóa; không có nút Chọn hợp đồng / xóa dòng / Lưu và tiếp tục',
       '- "Cập nhật thành công.", về danh sách; danh sách: Dư có 2,750,000.5, Dư nợ trống',
       '- Báo cáo: số dư đầu kỳ của hợp đồng đổi từ nợ 1,500,000 sang có 2,750,000.5']),
    T('S', '004', 'Sửa sang tài khoản đã khai báo cho cùng hợp đồng bị chặn', 'P1',
      'Hợp đồng H của KH-1 có khai báo tài khoản 1311 và khai báo tài khoản 1312 (lập bằng Import)',
      ['1. Sửa khai báo 1312, đổi sang 1311', '2. Bấm Lưu'], '—',
      ['- Dưới ô Tài khoản: "Đã khai báo đầu kỳ cho tài khoản này", không lưu']),
    T('S', '005', 'Vào thẳng trang Sửa của khai báo đã phát sinh', 'P0', 'Khai báo Y',
      ['1. Dán đường dẫn trang Sửa của Y'], '—',
      ['- Thông báo "Khai báo đã phát sinh chứng từ hoặc bạn không có quyền sửa."', '- Tự chuyển về trang Chi tiết của Y']),
    T('S', '006', 'Lịch sử thay đổi ở Chi tiết', 'P0', 'Khai báo Z vừa tạo rồi sửa như TC_05.003',
      ['1. Mở chi tiết Z', '2. Ở khối Lịch sử bấm "Xem lịch sử"', '3. Bấm Bộ lọc'], '—',
      ['- Mới nhất ở trên: "Thay đổi thông tin" — Loại dư: Dư nợ → Dư có; Công nợ: 1,500,000.00 → 2,750,000.50 (cũ đỏ, mới xanh)',
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
      ['1. Bấm Xóa ở dòng Z', '2. Bấm Hủy', '3. Bấm Xóa lần nữa, bấm Xóa trong hộp', '4. Mở báo cáo ' + BC + ', lọc KH-1'], '—',
      ['- Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?"', '- Hủy: không đổi gì',
       '- Xóa: "Xóa thành công.", dòng biến mất', '- Báo cáo: số dư đầu kỳ của hợp đồng không còn']),
    T('G', '002', 'Xóa từ trang Chi tiết', 'P1', 'Khai báo Z chưa phát sinh',
      ['1. Mở chi tiết Z, bấm Xóa, xác nhận'], '—',
      ['- Về danh sách, Z không còn']),
    T('S', '003', 'Không xóa được khai báo đã phát sinh', 'P0', 'Khai báo Y',
      ['1. Tìm dòng Y ở danh sách và mở chi tiết'], '—',
      ['- Không có nút Xóa ở cả 2 nơi']),
    T('M', '004', 'Xóa xong hợp đồng chọn lại được', 'P2', 'Vừa xóa khai báo Z của HĐ-1',
      ['1. Tạo mới, chọn KH-1, mở cửa sổ chọn hợp đồng'], '—',
      ['- HĐ-1 không còn "Đã khai báo", chọn được']),
]

# ------------------------------------------------------------------ VII. IMPORT
S7 = [
    T('S', '001', 'Tải file mẫu', 'P1', '—',
      ['1. Bấm Import Excel', '2. Bấm "Tải file mẫu", mở file'], '—',
      ['- Tên file Mau_import_cong_no_dau_ky_khach_hang.xlsx',
       '- Cột: STT, Mã khách hàng *, Mã hợp đồng *, Loại hợp đồng *, Số tài khoản *, Loại dư, Công nợ *, Công nợ quá hạn, Ngày bàn giao nghiệm thu',
       '- Hàng 1 là tiêu đề, KHÔNG có dòng mô tả; có dòng ví dụ', '- Cột Loại hợp đồng và Loại dư bấm ra danh sách chọn']),
    T('S', '002', 'Kiểm tra dữ liệu import', 'P0', 'File 4 dòng: 1 đúng, 1 sai mọi cột, 1 trùng dòng 1, 1 quá hạn thiếu ngày BGNT',
      ['1. Chọn file, bấm "Load lên bảng"', '2. Bấm Validate'], '—',
      ['- Tổng 4, Hợp lệ 1, Lỗi 3; "Validate xong: 1 hợp lệ, 3 không hợp lệ…"', '- Dòng đúng: xanh, khóa',
       '- Dòng sai: "Khách hàng – Mã không tồn tại trong hệ thống", "Loại hợp đồng – Chỉ nhận HDMNN / HDMN / HDMTN / HDDK / HDHNTDA / HDDV", '
       '"Số tài khoản – Không tồn tại trong hệ thống", "Loại dư – Chỉ nhận "Dư nợ" hoặc "Dư có"", "Công nợ – Phải lớn hơn 0."',
       '- Dòng trùng: "Trùng với dòng 1 trong file"', '- Dòng quá hạn: "Ngày bàn giao nghiệm thu – Bắt buộc phải nhập"',
       '- Sửa được dòng lỗi ngay trên bảng rồi Validate lại']),
    T('S', '003', 'Import chỉ khi không còn dòng lỗi', 'P0', 'Sau TC_07.002',
      ['1. Quan sát nút Import', '2. Bấm "Bỏ dòng lỗi"', '3. Bấm Import'], '—',
      ['- Bước 1: nút Import mờ', '- Bước 3: báo import thành công 1 dòng; cửa sổ đóng, danh sách nạp lại',
       '- Khai báo mới có mã nối tiếp, có mốc "Tạo mới" trong lịch sử và hiện trong báo cáo công nợ như khi lập tay']),
    T('S', '004', 'Import kiểm hợp đồng tồn tại và thuộc khách hàng', 'P0', 'File: mã hợp đồng không có thật; mã hợp đồng của khách hàng khác',
      ['1. Load, Validate'], '—',
      ['- "Mã hợp đồng – Không tồn tại trong hệ thống"', '- "Mã hợp đồng – Không thuộc khách hàng này"']),
    T('G', '005', 'Mã loại hợp đồng được nhận', 'P1', 'File dùng lần lượt HDDK, HDHNTDA, HDDV, HDMNN, HDMN, HDMTN và 1 mã khác',
      ['1. Load, Validate'], '—',
      ['- 6 mã trên được nhận; mã khác báo "Loại hợp đồng – Chỉ nhận …"']),
    T('S', '006', 'Import trùng khai báo đã có', 'P1', 'HĐ-1 + tài khoản 1311 đã khai báo cho KH-1',
      ['1. File có dòng KH-1 + HĐ-1 + 1311', '2. Validate'], '—',
      ['- "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này"']),
    T('M', '007', 'Import cột quá hạn', 'P1', 'File: dòng Dư có + quá hạn 2; dòng quá hạn 2 + ngày 31/12/2099; dòng quá hạn "x"; dòng quá hạn 2 + 30/09/2026',
      ['1. Load, Validate'], '—',
      ['- "Công nợ quá hạn – Chỉ công nợ "Dư nợ" mới được đánh dấu quá hạn"',
       '- "Ngày bàn giao nghiệm thu – Không được lớn hơn ngày hiện tại"', '- "Công nợ quá hạn – Chỉ nhận 1 (không) hoặc 2 (có)"',
       '- Dòng cuối hợp lệ; sau Import khai báo có Quá hạn "Có", Ngày BGNT 30/09/2026']),
    T('M', '008', 'File quá 500 dòng', 'P2', 'File 501 dòng dữ liệu',
      ['1. Chọn file, bấm "Load lên bảng"'], '—',
      ['- Báo vượt 500 dòng mỗi lần, không load']),
    T('M', '009', 'Dòng bị người khác khai báo trùng sau Validate', 'P2', '2 tài khoản cùng import 1 file có HĐ-2 + 1311 của KH-1',
      ['1. Cả 2 Validate xong', '2. Người thứ nhất bấm Import', '3. Người thứ hai bấm Import'], '—',
      ['- Người thứ hai: dòng HĐ-2 bị bỏ qua với lý do "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này", các dòng khác vẫn nhập']),
]

# ------------------------------------------------------------------ VIII. XUẤT / IN
S8 = [
    T('S', '001', 'Xuất Excel: chọn trường trước khi xuất', 'P0', 'Đang lọc từ khóa "75TPHXCH-2"',
      ['1. Bấm Xuất Excel', '2. Xem các trường tích sẵn', '3. Bỏ tích Người tạo, kéo Dư có lên trên Dư nợ, bấm Xuất file'], '—',
      ['- Cửa sổ "Chọn trường xuất file" tích sẵn đúng các cột đang hiện; "Đang chọn x/13 trường"',
       '- Cạnh nút có dòng tiến độ; xong báo "Xuất Excel thành công"',
       '- File khai_bao_dau_ky_cong_no.xlsx, tiêu đề "DANH SÁCH CÔNG NỢ ĐẦU KỲ THEO KHÁCH HÀNG - HỢP ĐỒNG"; chỉ các dòng khớp bộ lọc (mọi trang), cột đúng thứ tự đã kéo',
       '- Cột Dư nợ / Dư có là SỐ (SUM được), định dạng 1,234,567']),
    T('S', '002', 'In danh sách', 'P0', 'Đang lọc từ khóa "75TPHXCH-2"',
      ['1. Bấm In danh sách', '2. Bấm In'], '—',
      ['- Cửa sổ "Xem trước khai báo đầu kỳ công nợ" khổ ngang, có tiêu đề công ty, tiêu đề "Công nợ đầu kỳ theo khách hàng - hợp đồng"',
       '- Bảng in đúng các cột đang hiện (không có Hành động), đúng các dòng khớp bộ lọc',
       '- Số có phần lẻ giữ phần lẻ (2,750,000.5)', '- Bấm In mở hộp in của trình duyệt']),
    T('S', '003', 'In danh sách quá 2,000 dòng', 'P1', 'TK-ALL, không lọc gì, phạm vi hơn 2,000 khai báo',
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
    T('S', '002', 'Trùng với khai báo đã có', 'P0', '2 người cùng mở trang Thêm, cùng chọn HĐ-1 + tài khoản 1311 của KH-1',
      ['1. Người thứ nhất bấm Lưu', '2. Người thứ hai bấm Lưu'], '—',
      ['- Người thứ hai: dưới ô Tài khoản "Đã khai báo đầu kỳ cho tài khoản này"', '- Không lưu dòng nào trong lần đó']),
    T('S', '003', 'Công nợ bằng 0 hoặc để trống', 'P0', '—',
      ['1. Để trống Công nợ, Lưu', '2. Nhập 0, Lưu'], '—',
      ['- Trống: "Bắt buộc phải nhập"', '- 0: "Phải lớn hơn 0"', '- Ô tiền không cho gõ dấu âm']),
]

# ------------------------------------------------------------------ X. ĐỒNG THỜI
S10 = [
    T('S', '001', 'Mã phiếu không trùng khi 2 người lưu cùng lúc', 'P1', '2 tài khoản cùng công ty',
      ['1. Hai người cùng lập khai báo (hợp đồng khác nhau), bấm Lưu gần như đồng thời'], '—',
      ['- 2 khai báo có 2 mã nối tiếp, không trùng, không lỗi']),
    T('S', '002', 'Khai báo vừa phát sinh chứng từ trong lúc người khác đang sửa', 'P1',
      'A đang mở trang Sửa khai báo Z; B lập phiếu thu cho hợp đồng của Z (cùng tài khoản)',
      ['1. A bấm Lưu'], '—',
      ['- A bị từ chối với câu "Khai báo đã phát sinh chứng từ, không được sửa / xóa.", dữ liệu không đổi']),
]

# ------------------------------------------------------------------ XI. LUỒNG ĐẦU CUỐI
S11 = [
    T('S', '001', 'Luồng đầu cuối: khai báo, thu tiền, bị khóa, mở lại', 'P0', 'KH-1 có HĐ-2 chưa khai báo',
      ['1. Lập khai báo Dư nợ 1,500,000 cho HĐ-2, tài khoản 1311', '2. Mở báo cáo ' + BC + ', lọc KH-1',
       '3. Lập phiếu thu cho HĐ-2 (ghi sổ tài khoản 1311), quay lại danh sách khai báo',
       '4. Xóa / hủy ghi sổ phiếu thu đó, quay lại danh sách'], '—',
      ['- Bước 2: số dư đầu kỳ của HĐ-2 là nợ 1,500,000', '- Bước 3: dòng khai báo không còn Sửa, Xóa; chi tiết chỉ còn Quay lại',
       '- Bước 4: khai báo có lại Sửa, Xóa']),
    T('S', '002', 'Luồng đầu cuối: import, sửa, xem lịch sử, xóa', 'P1', 'File import 1 dòng hợp lệ',
      ['1. Import', '2. Sửa số tiền', '3. Xem Lịch sử', '4. Xóa'], '—',
      ['- Mỗi bước báo cáo công nợ đổi theo; xóa xong không còn số dư', '- Lịch sử có "Tạo mới" và "Thay đổi thông tin"']),
    T('M', '003', 'Đã có khai báo thì không đổi được Ngày khai báo đầu kỳ', 'P2', 'Công ty TPE đã có khai báo đầu kỳ công nợ',
      ['1. Vào phân hệ Tài chính > Khai Quy chế – Cấu hình', '2. Xem trường "Ngày khai báo đầu kỳ"'], '—',
      ['- Trường bị khóa (không đổi được vì công ty đã có số dư đầu kỳ)']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP KHAI BÁO — CHỌN KHÁCH HÀNG & HỢP ĐỒNG', S4),
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
