# -*- coding: utf-8 -*-
"""Testcase 2 báo cáo bốc xếp (STT 309 theo NCC · 310 theo NV) — KHUÔN CHUẨN skill testcase-documenter
(`assets/tc_chuan.build_chuan`, loai='bao_cao', check_tc phải 0 lỗi). Case chung viết 1 lần, rẽ nhánh theo `K['ncc']`.
Số liệu mẫu đọc trên môi trường thử (dev-hrm) ngày 18/11/2026."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _chung_boc_xep as CH  # noqa: E402
from tc_chuan import build_chuan  # noqa: E402

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


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


# Case cốt lõi nâng P0 (giữ tỉ lệ P0 >= 40% theo skill)
PROMOTE = {
    'Kỳ không có lượt nào', 'Thứ tự dòng mặc định', 'Mở phiếu từ dòng lượt', 'STT liên tục giữa các trang',
    'Giá trị mặc định của các ô lọc', 'Tính cả 2 đầu mút của kỳ Tuỳ chọn', 'Đổi Công ty xoá ô phụ thuộc',
    'Kết hợp nhiều điều kiện lọc', 'Kết hợp Kỳ, Công ty, Nhân viên', 'Danh sách ô Nhân viên',
    'Ngày hạch toán là ngày hạch toán sớm nhất của phiếu', 'Khối THEO LOẠI BỐC XẾP khớp bảng',
    'Số liệu đúng phạm vi quyền ở mọi con số', 'Lọc Công ty theo công ty của nhân viên', 'Tính cả lượt công ty tự bốc và thuê ngoài',
    'Popup theo đúng bộ lọc báo cáo', 'Mở popup từ ô Lượt nhập hàng / Lượt xuất hàng', 'Mở popup từ 1 loại bốc xếp',
    'Xuất Excel danh sách của popup', 'Định dạng số và tiếng Việt trong file', 'In danh sách lượt bốc xếp',
    'Phiếu hạch toán sang kỳ khác', 'Khớp với báo cáo bốc xếp khác cùng kỳ', 'Đổi công ty đang làm việc',
    'Phạm vi áp cho popup, bản In và file Excel',
}
SYM = [('→', '->'), ('≤', 'nhỏ hơn hoặc bằng'), ('☰', 'biểu tượng kéo')]


def _clean(v):
    if isinstance(v, (list, tuple)):
        return [_clean(x) for x in v]
    if isinstance(v, str):
        for a, b in SYM:
            v = v.replace(a, b)
    return v


def C(func, prio, pre, steps, data, exp):
    assert prio in ('P0', 'P1', 'P2'), func
    if func in PROMOTE:
        prio = 'P0'
    pre, steps, data, exp = _clean(pre), _clean(steps), _clean(data), _clean(exp)
    st = _lines(steps)
    st = [s if s[:2].rstrip('.').isdigit() else '%d. %s' % (i + 1, s) for i, s in enumerate(st)]
    return (func, prio, '\n'.join(_lines(pre)), '\n'.join(st), '\n'.join(_lines(data)), _exp(exp))


def sections(groups):
    return [(ROMAN[i], t, [('%03d' % (k + 1),) + c for k, c in enumerate(cs)]) for i, (t, cs) in enumerate(groups)]


def groups(K):
    ncc, ten, dv, Dv, T = K['ncc'], K['ten'], K['dv'], K['Dv'], K['tien']
    MENU = K['menu_txt']
    Q = CH.QUYEN
    SA = 'Tài khoản TK-SA có quyền "%s" mức Tổng công ty.' % Q
    if ncc:
        KY = 'Kỳ Tháng này (tháng 11/2026), môi trường thử: 2 nhà cung cấp, 2 lượt, tổng 445,400.'
        NHIEU = 'Tài khoản TK-SA; kỳ có hơn 10 nhà cung cấp có lượt thuê ngoài (môi trường thử chỉ có 7 nhà cung cấp năm 2026 — dùng Số dòng/trang 10 với dữ liệu kiểm thử đủ lớn).'
    else:
        KY = 'Kỳ Tháng trước (tháng 10/2026), môi trường thử: 14 nhân viên, 133 lượt, tổng 10,245,700.'
        NHIEU = 'Tài khoản TK-SA; kỳ Năm nay (môi trường thử: 18 nhân viên, 2 trang).'

    # ======================================================================== I. HIỂN THỊ
    G1 = [
        C('Mở màn hình từ menu', 'P0', 'Tài khoản bất kỳ đã đăng nhập.', ['Đăng nhập', MENU], '',
          ['Màn mở, tiêu đề trang "%s", cạnh tiêu đề có icon (i)' % ten,
           'Nhóm Báo cáo bốc xếp có 3 mục: Báo cáo cẩu hàng bốc xếp theo nhà cung cấp, Báo cáo cẩu hàng bốc xếp theo nhân viên, Báo cáo chi tiết cẩu hàng bốc xếp theo nhân viên',
           'Báo cáo tự tải kỳ Tháng này, không cần bấm Tìm kiếm']),
        C('Tiêu đề trang và nội dung icon (i)', 'P2', 'Đang mở màn.', ['Rê chuột vào icon (i) cạnh tiêu đề khối bộ lọc'], '',
          ['Khối bộ lọc có tiêu đề "Bộ lọc %s%s"' % (ten[0].lower(), ten[1:]),
           'Chú thích "MỤC ĐÍCH BÁO CÁO" gồm: ' + '; '.join(K['muc_dich'])]),
        C('Các nút chức năng được hiển thị', 'P1', 'Tài khoản TK-SA.', ['Mở màn', 'Quan sát cụm nút góc phải khối bộ lọc và dưới các ô lọc'], '',
          ['Cụm nút theo thứ tự: nút biểu tượng cột (Cấu hình cột hiển thị), "In báo cáo", "Xuất Excel" (nền xanh lá)'
           + (', "Cài đặt bộ lọc", "Ẩn tìm kiếm nâng cao"' if ncc else ''),
           'Nút "Tìm kiếm", "Xóa lọc"' + ('' if ncc else ' nằm cùng hàng với 3 ô lọc (bộ lọc gọn, không có "Cài đặt bộ lọc", "Ẩn tìm kiếm nâng cao")'),
           'Không có nút Thêm / Sửa / Xóa']),
        C('Các cột mặc định hiển thị', 'P0', 'Đang mở màn, kỳ có dữ liệu.', ['Đọc tiêu đề bảng từ trái sang phải'], '',
          ['STT | %s | %s' % (K['cot_cay'], ' | '.join(K['cot_so'])),
           'Cột %s có icon (i)' % T + ('; cột Ngày hạch toán có icon (i)' if ncc else ''),
           'Không có cột nào bị ẩn mặc định (Tuỳ chỉnh cột đang chọn đủ %d/%d cột)' % (len(K['cot_so']) + 2, len(K['cot_so']) + 2)]),
        C('Khối tổng hợp đầu báo cáo', 'P0', KY, ['Mở màn' + ('' if ncc else ', chọn Kỳ = Tháng trước'), 'Đọc khối tổng hợp'], '',
          (['Dòng đầu "Kỳ tháng 11/2026 (theo ngày hạch toán) · 2 lượt · 2 nhà cung cấp · Khối lượng 5 tấn"',
            'Khối LƯỢT BỐC XẾP: "Số tiền 445,400"; ô Lượt bốc xếp 2, Lượt nhập hàng 1, Lượt xuất hàng 1',
            'Khối THEO LOẠI BỐC XẾP: "1 loại", ô "Xe cẩu (Bao gồm xăng xe, Xuất >=8 tấn)" 2 lượt, 445,400'] if ncc else
           ['Dòng đầu "Kỳ tháng 10/2026 (theo ngày hạch toán) · 133 lượt · 14 nhân viên · Khối lượng 1,403.1 tấn"',
            'Khối LƯỢT BỐC XẾP: "Số tiền 10,245,700"; Lượt bốc xếp 133, Lượt nhập hàng 51, Lượt xuất hàng 82',
            'Khối THEO LOẠI BỐC XẾP: "7 loại", loại có số tiền lớn nhất đứng đầu (Người bốc xếp thiết bị (Nhập >=24 tấn) 49 lượt, 5,406,000)'])),
        C('Thu gọn và mở rộng khối tổng hợp', 'P2', 'Đang xem báo cáo có dữ liệu.', ['Bấm "Thu gọn" ở góc phải khối tổng hợp', 'Bấm "Mở rộng"'], '',
          ['Bước 1: 2 khối số liệu ẩn, còn dòng kỳ; nút đổi chữ "Mở rộng"', 'Bước 2: 2 khối hiện lại, bảng không tải lại']),
        C('Dữ liệu trên bảng đúng với phiếu đã lập', 'P0', KY if ncc else 'Kỳ Tháng này (tháng 11/2026): Nguyễn Đức Tuân 1 lượt, 2 tấn, 170,000.',
          (['Mở màn', 'Bấm PXH-43237 ở dòng lượt của CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN, mở tab Bốc xếp của phiếu', 'So với dòng lượt trên báo cáo'] if ncc else
           ['Mở màn', 'Bấm số lượt 1 của Nguyễn Đức Tuân, bấm số phiếu hạch toán trong popup', 'Mở tab Bốc xếp của phiếu, so người bốc xếp, khối lượng, tiền công']), '',
          (['Phiếu xuất hàng PXH-43237: loại thuê Thuê ngoài, nhà cung cấp ETEK GREEN, loại "Xe cẩu (Bao gồm xăng xe, Xuất >=8 tấn)", khối lượng 3',
            'Báo cáo: Ngày hạch toán 07/11/2026 00:14, Phiếu nhập/xuất kho PXK-38146, Nhập/Xuất "Xuất", Số tiền (sau VAT) 275,400 = thành tiền trên phiếu × (1 + VAT%)'] if ncc else
           ['Phiếu có Nguyễn Đức Tuân là người bốc xếp, khối lượng 2, tiền công 170,000', 'Đúng bằng dòng I trên báo cáo'])),
        C('Kỳ không có lượt nào', 'P1', 'Tài khoản TK-SA.', (['Mở màn', 'Nhập "ZZZ999" vào ô Phiếu hạch toán, nhấn Enter'] if ncc else ['Mở màn', 'Chọn Kỳ = Tuần này (tuần không có lượt bốc xếp)']), '',
          ['Khối tổng hợp "· 0 lượt · 0 %s · Khối lượng 0 tấn", khối LƯỢT BỐC XẾP "Số tiền 0", chỉ còn ô Lượt bốc xếp 0 (không bấm được), khối THEO LOẠI BỐC XẾP ẩn' % dv,
           'Dòng TỔNG hiện 0 ở Số lượt, Khối lượng, %s' % T, 'Dòng "Không có lượt bốc xếp nào khớp bộ lọc."',
           'Chân bảng "Hiển thị 0–0 / 0 %s" hoặc không có số trang' % dv]),
        C('Thứ tự dòng mặc định', 'P1', KY, ['Mở màn' + ('' if ncc else ', chọn Kỳ = Tháng trước'), 'Đọc thứ tự các dòng %s' % dv]
          + (['Đọc thứ tự các dòng lượt của 1 nhà cung cấp có nhiều lượt (kỳ Năm nay)'] if ncc else []), '',
          ['%s xếp theo %s GIẢM DẦN; bằng nhau thì theo tên' % (Dv, T)]
          + (['Môi trường thử tháng 11/2026: I ETEK GREEN 275,400 trước II BEIJING FSW 170,000',
              'Dòng lượt trong 1 nhà cung cấp xếp theo Ngày hạch toán tăng dần'] if ncc else
             ['Môi trường thử tháng 10/2026: I Lê Văn Chiến 1,546,900, II Lê Đình Hướng 1,506,800, III Lê Văn Trình 1,035,000'])),
        C('Số thứ tự La Mã' + (' và số dòng lượt' if ncc else ''), 'P1', KY, ['Mở màn', 'Đọc cột STT'], '',
          ['Dòng TỔNG ghi "TỔNG"', 'Dòng %s đánh I, II, III…' % dv] + (['Dòng lượt đánh 1, 2, 3… lại từ 1 trong từng nhà cung cấp'] if ncc else [])),
    ]
    if ncc:
        G1 += [
            C('Ô chọn cấp mặc định và đổi cấp', 'P1', KY, ['Mở màn, quan sát ô chọn cấp ở tiêu đề cột Nhà cung cấp / Phiếu hạch toán', 'Chọn "Chỉ nhà cung cấp"', 'Chọn lại "Đến từng lượt bốc xếp"'], '',
              ['Bước 1: ô chọn cấp mặc định "Đến từng lượt bốc xếp", mọi nhà cung cấp đã bung sẵn dòng lượt',
               'Bước 2: chỉ còn dòng TỔNG và dòng nhà cung cấp; mũi tên mọi dòng ở trạng thái thu', 'Bước 3: bung lại hết; số liệu không đổi, không tải lại']),
            C('Bung / thu riêng 1 nhà cung cấp', 'P2', KY, ['Bấm mũi tên trước tên ETEK GREEN', 'Bấm lại'], '',
              ['Bước 1: chỉ dòng lượt của ETEK GREEN ẩn, nhà cung cấp khác giữ nguyên', 'Rê chuột vào mũi tên hiện "Hiện các lượt bốc xếp" / "Ẩn các lượt bốc xếp"']),
            C('Nhà cung cấp không còn trong danh mục', 'P2', 'Tài khoản TK-SA; kỳ Tháng trước (môi trường thử tháng 10/2026 có 4 nhà cung cấp loại này).', ['Chọn Kỳ = Tháng trước', 'Đọc cột Nhà cung cấp / Phiếu hạch toán'], '',
              ['Nhà cung cấp không tìm thấy trong danh mục vẫn thành 1 nhóm, ghi "Nhà cung cấp #<số>" (vd "Nhà cung cấp #36625"), không có mã',
               'Số lượt, khối lượng, tiền của nhóm vẫn đúng; ghi lại vào cột Ghi chú các nhà cung cấp này để kiểm danh mục']),
            C('Mở phiếu từ dòng lượt', 'P1', KY, ['Bấm PXH-43237', 'Quay lại tab báo cáo, bấm PXK-38146', 'Bấm PNH-15777, PNK-11620'], '',
              ['Mỗi số phiếu mở đúng màn chi tiết Phiếu xuất hàng / Phiếu xuất kho / Phiếu nhập hàng / Phiếu nhập kho ở TAB MỚI',
               'Tab báo cáo giữ nguyên bộ lọc, trang']),
            C('Tên nhà cung cấp dài bị cắt', 'P2', 'Có nhà cung cấp tên dài (vd CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN - 29TPHPTH-1).', ['Rê chuột vào tên nhà cung cấp ở dòng nhóm'], '',
              ['Mã bị cắt "29TP…" khi không đủ chỗ', 'Rê chuột hiện đủ "CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN - 29TPHPTH-1"']),
        ]
    else:
        G1 += [
            C('Bảng 1 cấp, không có ô chọn cấp', 'P1', KY, ['Mở màn', 'Quan sát cột Nhân viên'], '',
              ['Mỗi nhân viên 1 dòng: tên, mã nhân viên chữ nhỏ màu xám', 'Không có mũi tên bung / thu, không có ô chọn cấp, không có dòng lượt con']),
        ]
    G1 += [
        C('Số dòng mặc định mỗi trang và đổi số dòng', 'P0', NHIEU, ['Đọc ô "Số dòng/trang" và đếm số %s trang 1' % dv, 'Đổi Số dòng/trang = 20'], '',
          ['Bước 1: mặc định 10, lựa chọn 10 / 20 / 50 / 100; trang 1 có đúng 10 %s' % dv,
           'Bước 2: về trang 1, hiện tối đa 20 %s; chân bảng "Hiển thị 1–… / N %s", N không đổi' % (dv, dv)]),
        C('Sang trang sau và về trang trước', 'P0', NHIEU, ['Bấm nút › (trang kế tiếp)', 'Bấm nút ‹'], '',
          ['Bước 1: sang trang 2, chân bảng "Hiển thị 11–… / N %s"' % dv, 'Bước 2: về trang 1', 'Dòng TỔNG và khối tổng hợp KHÔNG đổi khi chuyển trang',
           'Không %s nào lặp / thiếu giữa 2 trang' % dv]),
        C('Về trang đầu, trang cuối và trạng thái nút', 'P1', NHIEU, ['Ở trang 1 quan sát nút « và ‹', 'Bấm »', 'Quan sát nút › và »', 'Bấm «'], '',
          ['Trang 1: « và ‹ mờ, bấm không tác dụng', 'Bước 2: tới trang cuối; › và » mờ', 'Bước 4: về trang 1']),
        C('STT liên tục giữa các trang', 'P1', NHIEU, ['Ghi STT dòng %s cuối trang 1' % dv, 'Sang trang 2, đọc STT dòng đầu'], '',
          ['Trang 1 kết thúc ở X thì trang 2 bắt đầu XI (liên tục, không quay về I)']
          + (['Các lượt của 1 nhà cung cấp không bị cắt sang trang khác'] if ncc else [])),
        C('Tổng số %s ở chân bảng' % dv, 'P0', NHIEU, ['Đọc chân bảng', 'So với số "N %s" ở dòng đầu khối tổng hợp' % dv], '',
          ['Chân bảng "Hiển thị a–b / N %s"; N bằng số %s ở khối tổng hợp' % (dv, dv), 'N từ 1,000 trở lên có dấu phẩy ngăn nghìn']),
        C('Đổi bộ lọc khi đang ở trang giữa thì về trang 1', 'P1', NHIEU, ['Sang trang 2', 'Đổi Kỳ sang kỳ khác'], '', ['Bảng về trang 1 theo kết quả mới']),
        C('Đổi số dòng khi đang ở trang 2 thì về trang 1', 'P2', NHIEU, ['Sang trang 2', 'Đổi Số dòng/trang = 50'], '', ['Bảng về trang 1, hiện tối đa 50 %s' % dv]),
        C('Các cột của bảng không cho sắp xếp', 'P2', 'Đang xem báo cáo có dữ liệu.', ['Bấm lần lượt vào tiêu đề từng cột'], '',
          ['Tiêu đề cột không có mũi tên sắp xếp, bấm không đổi thứ tự (thứ tự cố định theo Số tiền giảm dần)']),
        C('Thời gian mở màn', 'P1', 'Tài khoản TK-SA, mạng nội bộ.', [MENU + ', đo thời gian tới khi bảng có số liệu', 'Chọn Kỳ = Năm nay, đo thời gian tải'], '',
          ['Bước 1 dưới 10 giây (môi trường thử 18/11/2026 khoảng 7–8 giây, tính cả tải trang)', 'Bước 2 dưới 10 giây, màn không treo; đang tải thì số liệu cũ mờ đi, không xoá trắng']),
        C('Đổi bộ lọc liên tục chỉ hiện kết quả lần cuối', 'P2', 'Đang xem báo cáo.', ['Đổi Kỳ thật nhanh: Năm nay → Tháng trước → Tháng này'], '',
          ['Kết quả cuối là kỳ Tháng này; khối tổng hợp, dòng TỔNG, bảng cùng 1 kỳ, không lẫn số của kỳ trước']),
    ]

    # ======================================================================== II. TÌM KIẾM & LỌC
    G2 = [
        C('Giá trị mặc định của các ô lọc', 'P1', SA, ['Mở màn', 'Quan sát các ô lọc'], '',
          ['Kỳ = "Tháng này" (không có nút xoá), Công ty trống (có icon (i): "%s")' % K['cong_ty_hint'],
           ('Nhà cung cấp, Loại bốc xếp, Phiếu hạch toán trống' if ncc else 'Nhân viên trống'), 'Không có ô Thời gian']),
        C('Lọc theo Kỳ Tuần này / Tháng trước / Năm nay', 'P0', SA, ['Lần lượt chọn Kỳ = Tuần này, Tháng trước, Năm nay'], 'Ngày hiện tại 18/11/2026',
          ['Báo cáo tải lại NGAY khi chọn (không cần Tìm kiếm), về trang 1',
           'Dòng kỳ lần lượt: "Kỳ tuần này", "Kỳ tháng 10/2026", "Kỳ năm 2026" (theo ngày hạch toán)',
           'Chỉ lượt có ngày hạch toán của phiếu trong khoảng đó']
          + (['Môi trường thử: Tháng trước 18 lượt / 4 nhà cung cấp / 6,929,400; Năm nay 293 lượt / 7 nhà cung cấp / 108,392,728'] if ncc else
             ['Môi trường thử: Tháng trước 133 lượt / 14 nhân viên / 10,245,700; Năm nay 2,325 lượt / 18 nhân viên / 185,902,800'])),
        C('Chọn Kỳ Tuỳ chọn hiện ô Thời gian', 'P1', 'Đang mở màn.', ['Chọn Kỳ = Tuỳ chọn'], '',
          ['Xuất hiện ô "Thời gian" (ngày bắt đầu → ngày kết thúc) ngay sau ô Kỳ', 'Báo cáo CHƯA tải lại, vẫn giữ số kỳ cũ']
          + ([] if ncc else ['Bộ lọc chuyển sang dạng có nút "Cài đặt bộ lọc", "Ẩn tìm kiếm nâng cao", nút Tìm kiếm / Xóa lọc xuống hàng dưới'])),
        C('Bấm Tìm kiếm khi Tuỳ chọn chưa đủ 2 ngày', 'P0', 'Kỳ = Tuỳ chọn, ô Thời gian trống hoặc mới chọn ngày bắt đầu.', ['Bấm Tìm kiếm'], '',
          ['Báo lỗi "Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn."', 'Báo cáo không tải lại']),
        C('Kỳ Tuỳ chọn đủ 2 ngày thì tải ngay', 'P0', 'Kỳ = Tuỳ chọn.', ['Chọn ngày bắt đầu 01/11/2026, ngày kết thúc 30/11/2026'], 'Thời gian: 01/11/2026 - 30/11/2026',
          ['Báo cáo tải lại ngay, dòng kỳ "Kỳ từ 01/11/2026 đến 30/11/2026 (theo ngày hạch toán)"', 'Số liệu bằng kỳ Tháng này']),
        C('Tính cả 2 đầu mút của kỳ Tuỳ chọn', 'P1', 'Có lượt X hạch toán ngày 07/11/2026 (%s).' % ('PXH-43237 lúc 00:14' if ncc else 'lượt của Nguyễn Đức Tuân'),
          ['Lọc 07/11/2026 - 07/11/2026', 'Lọc 08/11/2026 - 30/11/2026', 'Lọc 01/11/2026 - 06/11/2026'], '',
          ['Bước 1: có lượt X (tính từ 00:00 đến hết 23:59 ngày cuối)', 'Bước 2, 3: không có lượt X']),
        C('Ngày kết thúc trước ngày bắt đầu', 'P1', 'Kỳ = Tuỳ chọn.', ['Thử chọn ngày bắt đầu 30/11/2026, ngày kết thúc 01/11/2026'], 'Thời gian: 30/11/2026 - 01/11/2026',
          ['Lịch không cho chọn ngày kết thúc trước ngày bắt đầu; nếu vẫn gửi được thì báo "Ngày kết thúc phải sau hoặc bằng ngày bắt đầu", báo cáo giữ số cũ',
           'Ghi lại hành vi thực tế vào cột Ghi chú']),
        C('Đổi Kỳ khác Tuỳ chọn thì ô Thời gian bị xoá', 'P2', 'Kỳ = Tuỳ chọn, Thời gian 01/10/2026 - 31/10/2026.', ['Chọn Kỳ = Năm nay', 'Chọn lại Kỳ = Tuỳ chọn'], '',
          ['Bước 1: ô Thời gian biến mất, báo cáo theo năm 2026 (không lọc ngầm theo khoảng ngày cũ)', 'Bước 2: ô Thời gian trống']),
        C('Lọc theo Công ty', 'P0', SA, ['Chọn Công ty = CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT', 'Xoá trống ô Công ty'], '',
          ['Bước 1: tải lại ngay; chỉ lượt ' + ('trên Phiếu nhập hàng / Phiếu xuất hàng của công ty đó' if ncc else 'của nhân viên đang làm việc ở công ty đó'),
           'Bước 2: trống = mọi công ty, số liệu về như ban đầu']),
        C('Đổi Công ty xoá ô phụ thuộc', 'P1', SA + (' Đã chọn Nhà cung cấp và Loại bốc xếp.' if ncc else ' Đã chọn 1 Nhân viên.'), ['Đổi ô Công ty sang công ty khác'], '',
          (['Ô Loại bốc xếp bị xoá trống, danh sách loại tải lại theo công ty mới', 'Ô Nhà cung cấp GIỮ nguyên lựa chọn'] if ncc else
           ['Ô Nhân viên bị xoá trống, danh sách nhân viên tải lại theo công ty mới'])),
    ]
    if ncc:
        G2 += [
            C('Ô Nhà cung cấp tìm theo tên, số điện thoại, mã', 'P0', 'Đang mở màn.', ['Bấm ô Nhà cung cấp, gõ "ETEK"', 'Gõ mã "CFSW"', 'Gõ số điện thoại của 1 nhà cung cấp'], '',
              ['Danh sách hiện dạng "Mã - Tên", vd "29TPHPTH-1 - CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN"', 'Tìm gần đúng, không phân biệt hoa thường', 'Tìm trên toàn danh mục khách hàng / nhà cung cấp']),
            C('Gõ dưới 3 ký tự chỉ hiện 20 kết quả', 'P2', 'Đang mở màn.', ['Bấm ô Nhà cung cấp, gõ "a"', 'Gõ "abc"'], '',
              ['Bước 1: tối đa 20 kết quả, mới tạo đứng trước', 'Bước 2: hiện mọi kết quả khớp']),
            C('Chọn một và nhiều nhà cung cấp', 'P0', 'Kỳ Tháng này.', ['Chọn ETEK GREEN', 'Chọn thêm BEIJING FSW', 'Bỏ chọn cả 2'], '',
              ['Bước 1: tải lại ngay, chỉ còn ETEK GREEN (1 lượt, 275,400)', 'Bước 2: 2 nhà cung cấp, TỔNG 445,400', 'Bước 3: về mọi nhà cung cấp']),
            C('Chọn nhà cung cấp không có lượt trong kỳ', 'P1', 'Kỳ Tháng này.', ['Chọn 1 khách hàng bất kỳ không có lượt bốc xếp'], '',
              ['Bảng "Không có lượt bốc xếp nào khớp bộ lọc.", TỔNG 0']),
            C('Lọc theo Loại bốc xếp', 'P0', 'Kỳ Năm nay.', ['Mở ô Loại bốc xếp, đọc danh sách', 'Chọn "Bốc xếp hàng"', 'Chọn thêm "Xe cẩu (Bao gồm xăng xe, Xuất >=8 tấn)"'], '',
              ['Danh sách chỉ gồm loại có lượt trong phạm vi (không theo kỳ)', 'Bước 2: chỉ lượt loại Bốc xếp hàng; khối THEO LOẠI BỐC XẾP còn 1 loại',
               'Bước 3: lượt của cả 2 loại']),
            C('Tìm Phiếu hạch toán đúng số phiếu', 'P0', 'Kỳ Tháng này.', ['Nhập "PXH-43237" vào ô Phiếu hạch toán, nhấn Enter'], 'Phiếu hạch toán: PXH-43237',
              ['Chỉ còn ETEK GREEN với lượt PXH-43237', 'TỔNG 1 lượt, 275,400']),
            C('Tìm Phiếu hạch toán một phần và không phân biệt hoa thường', 'P1', 'Kỳ Tháng này.', ['Nhập "pnh-157", nhấn Enter', 'Nhập "PNH", nhấn Enter'], '',
              ['Bước 1: còn lượt PNH-15777 (gần đúng, không phân biệt hoa thường)', 'Bước 2: chỉ còn các lượt của Phiếu nhập hàng']),
            C('Tìm Phiếu hạch toán không tồn tại', 'P1', 'Kỳ Tháng này.', ['Nhập "ZZZ999", nhấn Enter'], 'Phiếu hạch toán: ZZZ999',
              ['"Không có lượt bốc xếp nào khớp bộ lọc.", TỔNG 0, không báo lỗi']),
            C('Tìm Phiếu hạch toán với ký tự đặc biệt', 'P2', 'Kỳ Năm nay.', ['Lần lượt nhập từng chuỗi ở Test data, nhấn Enter'], ['%', '_', "' OR 1=1 --", '<b>abc</b>'],
              ['Không báo lỗi hệ thống, màn không treo', 'Chuỗi lạ không làm lộ thêm dữ liệu ngoài phạm vi; ghi lại số kết quả của % và _ vào Ghi chú']),
            C('Khoảng trắng đầu / cuối ô Phiếu hạch toán', 'P2', 'Kỳ Tháng này.', ['Nhập "  PXH-43237  ", nhấn Enter'], '', ['Kết quả giống khi nhập "PXH-43237" (khoảng trắng bị bỏ)']),
            C('Giới hạn độ dài ô Phiếu hạch toán', 'P2', 'Đang mở màn.', ['Dán chuỗi 500 ký tự vào ô, nhấn Enter'], 'Chuỗi "abcde" lặp 100 lần',
              ['Ô nhận chuỗi, không báo lỗi hệ thống', 'Bảng "Không có lượt bốc xếp nào khớp bộ lọc."']),
            C('Gõ Phiếu hạch toán chưa Enter thì chưa lọc', 'P1', 'Kỳ Tháng này.', ['Gõ "PXH-43237", không nhấn Enter', 'Nhấn Enter', 'Gõ "PNH-15777", bấm nút Tìm kiếm'], '',
              ['Bước 1: bảng chưa đổi', 'Bước 2: lọc theo phiếu, về trang 1', 'Bước 3: nút Tìm kiếm cho kết quả giống Enter']),
            C('Xoá nội dung Phiếu hạch toán', 'P1', 'Đang lọc Phiếu hạch toán PXH-43237.', ['Xoá hết nội dung ô', 'Nhấn Enter'], '',
              ['Bước 1: bảng chưa đổi', 'Bước 2: về đủ 2 nhà cung cấp của kỳ']),
            C('Kết hợp nhiều điều kiện lọc', 'P1', SA + ' Kỳ Năm nay.', ['Chọn Công ty', 'Chọn Loại bốc xếp', 'Chọn Nhà cung cấp', 'Nhập Phiếu hạch toán, nhấn Enter'], '',
              ['Kết quả thoả ĐỒNG THỜI mọi điều kiện', 'Khối tổng hợp, TỔNG, chân bảng tính lại theo kết quả; bảng về trang 1']),
            C('Ẩn / hiện các ô lọc', 'P2', 'Đang mở màn.', ['Bấm "Ẩn tìm kiếm nâng cao"', 'Bấm "Tìm kiếm nâng cao"'], '',
              ['Bước 1: các ô lọc thu gọn; nút đổi chữ "Tìm kiếm nâng cao"', 'Bước 2: các ô hiện lại, giá trị đã chọn giữ nguyên']),
            C('Cài đặt bộ lọc', 'P2', 'Đang mở màn.', ['Bấm "Cài đặt bộ lọc"', 'Bỏ tích "Loại bốc xếp", bấm Lưu', 'Mở lại, bấm "Khôi phục mặc định", Lưu'], '',
              ['Cửa sổ "Cài đặt bộ lọc": "Tích chọn trường lọc muốn hiển thị; kéo ☰ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình."; danh sách Kỳ, Công ty, Nhà cung cấp, Loại bốc xếp, Phiếu hạch toán; nút Lưu, Khôi phục mặc định, Đóng',
               'Bước 2: ô Loại bốc xếp ẩn khỏi bộ lọc', 'Bước 3: các ô về như ban đầu']),
        ]
    else:
        G2 += [
            C('Danh sách ô Nhân viên', 'P1', SA, ['Bấm ô Nhân viên, đọc danh sách', 'Gõ "Chiến" vào ô tìm của danh sách'], '',
              ['Hiển thị "Mã NV - Tên" (vd "12110292 - Lê Văn Chiến"), xếp theo mã', 'Chỉ gồm nhân viên CÓ lượt bốc xếp trong phạm vi quyền (mọi kỳ — môi trường thử 22 người, nhiều hơn 18 người của năm 2026)',
               'Bước 2: lọc còn người tên có "Chiến"']),
            C('Lọc theo Nhân viên', 'P0', 'Kỳ Tháng trước.', ['Chọn Nhân viên = 12110292 - Lê Văn Chiến', 'Xoá ô Nhân viên'], '',
              ['Bước 1: tải lại ngay; chỉ 1 dòng Lê Văn Chiến 24 lượt, 1,546,900; khối tổng hợp "24 lượt · 1 nhân viên"', 'Bước 2: về 14 nhân viên']),
            C('Chọn nhân viên không có lượt trong kỳ', 'P1', 'Kỳ Tháng này; chọn người chỉ có lượt ở tháng trước (vd Lê Văn Chiến).', ['Chọn Nhân viên = Lê Văn Chiến'], '',
              ['"Không có lượt bốc xếp nào khớp bộ lọc.", TỔNG 0']),
            C('Kết hợp Kỳ, Công ty, Nhân viên', 'P1', SA, ['Chọn Kỳ = Năm nay', 'Chọn Công ty', 'Chọn Nhân viên thuộc công ty đó'], '',
              ['Kết quả thoả đồng thời mọi điều kiện; khối tổng hợp, TỔNG, chân bảng tính lại; về trang 1']),
            C('Bấm Tìm kiếm khi không đổi điều kiện', 'P2', 'Đang xem báo cáo.', ['Bấm Tìm kiếm'], '', ['Tải lại đúng số liệu hiện tại từ trang 1']),
        ]
    G2 += [
        C('Tổng số và phân trang sau khi lọc', 'P1', NHIEU, ['Ghi N ở chân bảng', 'Lọc thêm ' + ('1 Loại bốc xếp' if ncc else '1 Công ty'), 'Đọc chân bảng, chuyển trang'], '',
          ['Chân bảng "Hiển thị 1–… / M %s" với M ≤ N, bằng số %s còn lại; số trang tính theo M' % (dv, dv)]),
        C('Nút Xóa lọc đưa mọi ô về mặc định', 'P0', 'Đã đổi Kỳ, Công ty' + (', Nhà cung cấp, Loại bốc xếp, Phiếu hạch toán.' if ncc else ', Nhân viên.'), ['Bấm "Xóa lọc"'], '',
          ['Kỳ về Tháng này, các ô khác trống, ô Thời gian biến mất', 'Báo cáo tải lại kỳ Tháng này từ trang 1']),
        C('Xóa lọc khi không có quyền tổng công ty', 'P1', 'Tài khoản TK-CT có mức Công ty; ô Công ty khoá ở công ty A.', ['Đổi Kỳ', 'Bấm Xóa lọc'], '',
          ['Kỳ về Tháng này; ô Công ty VẪN khoá ở công ty A']),
        C('Chuyển màn khác rồi quay lại', 'P1', 'Đang xem kỳ Năm nay có lọc thêm.', ['Vào màn khác trên menu', 'Quay lại báo cáo bằng menu'], '',
          ['Bộ lọc về mặc định (Kỳ = Tháng này), báo cáo tải kỳ Tháng này (màn không ghi nhớ bộ lọc)']),
        C('Tải lại trang (F5)', 'P1', 'Đang xem kỳ Năm nay có lọc thêm.', ['Nhấn F5'], '', ['Bộ lọc về mặc định, báo cáo tải kỳ Tháng này']),
        C('Mở màn ở tab mới', 'P2', 'Tab 1 đang lọc kỳ Năm nay.', ['Mở tab mới, vào báo cáo bằng menu', 'Quay lại tab 1'], '',
          ['Tab 2: bộ lọc mặc định (Tháng này)', 'Tab 1: giữ nguyên bộ lọc và kết quả đang xem']),
        C('Tài khoản khác trên cùng trình duyệt', 'P2', 'Có 2 tài khoản A, B.', ['A mở báo cáo, lọc kỳ Năm nay', 'Đăng xuất, đăng nhập B, mở báo cáo'], '',
          ['B thấy bộ lọc mặc định và số liệu theo phạm vi của B, không thấy bộ lọc / số liệu của A']),
    ]

    # ======================================================================== III. SỐ LIỆU
    if ncc:
        G3 = [
            C('Dòng TỔNG bằng tổng các dòng nhà cung cấp', 'P0', KY, ['Cộng Số lượt, Khối lượng, Số tiền (sau VAT) của các dòng nhà cung cấp'], '',
              ['Số lượt 2 = 1 + 1; Khối lượng 5 = 3 + 2; Số tiền 445,400 = 275,400 + 170,000 = dòng TỔNG']),
            C('Dòng nhà cung cấp bằng tổng các dòng lượt', 'P0', 'Kỳ Năm nay, 1 nhà cung cấp có nhiều lượt.', ['Bung nhà cung cấp, cộng Khối lượng và Số tiền các dòng lượt', 'Đếm số dòng lượt'], '',
              ['Tổng các dòng lượt = Khối lượng, Số tiền (sau VAT) của dòng nhà cung cấp (cộng SAU VAT)', 'Số dòng lượt = Số lượt của dòng nhà cung cấp']),
            C('Số tiền (sau VAT) của lượt', 'P0', 'Lượt PXH-43237 (tab Bốc xếp có thành tiền và VAT%).', ['Mở PXH-43237, đọc thành tiền bốc xếp và VAT%', 'Tính thành tiền × (1 + VAT%)'], '',
              ['Kết quả = 275,400 (Số tiền (sau VAT) trên báo cáo); làm tròn tối đa 2 chữ số lẻ']),
            C('Chỉ tính lượt thuê ngoài có nhà cung cấp', 'P0', 'Kỳ có lượt loại thuê "Công ty" (tự bốc xếp) và lượt "Thuê ngoài".', ['Lọc kỳ đó', 'Tìm Phiếu hạch toán của lượt loại thuê Công ty'], '',
              ['Lượt Công ty tự bốc KHÔNG có trên báo cáo', 'Lượt Thuê ngoài có nhà cung cấp có trên báo cáo']),
            C('Ngày hạch toán là ngày hạch toán sớm nhất của phiếu', 'P1', 'Phiếu nhập hàng PNH-15777 hạch toán 07/11/2026 00:00, lập lúc 07/11/2026 09:53.', ['Đọc cột Ngày hạch toán dòng PNH-15777', 'Bấm số lượt, đọc cột Ngày bốc xếp trong popup'], '',
              ['Ngày hạch toán "07/11/2026 00:00" (theo ngày ghi sổ, không theo ngày lập phiếu)', 'Popup: Ngày bốc xếp "07/11/2026 09:53" (ngày giờ lập phiếu)']),
            C('Cột Nhập/Xuất và Phiếu nhập/xuất kho', 'P1', KY, ['Đọc 2 dòng lượt'], '',
              ['PXH-43237: "Xuất", PXK-38146', 'PNH-15777: "Nhập", PNK-11620']),
            C('Khối LƯỢT BỐC XẾP khớp bảng', 'P0', 'Kỳ Năm nay.', ['Đọc khối LƯỢT BỐC XẾP', 'So với dòng TỔNG'], '',
              ['Lượt bốc xếp = Lượt nhập hàng + Lượt xuất hàng = Số lượt dòng TỔNG (môi trường thử 293 = 268 + 25)', '"Số tiền" góc khối = Số tiền (sau VAT) dòng TỔNG (108,392,728)']),
            C('Khối THEO LOẠI BỐC XẾP khớp bảng', 'P1', 'Kỳ Năm nay.', ['Cộng số lượt và số tiền các ô loại'], '',
              ['Tổng số lượt các loại = Số lượt TỔNG; tổng số tiền các loại = Số tiền TỔNG', 'Các ô xếp theo số tiền giảm dần; "N loại" = số ô (môi trường thử 6 loại)']),
        ]
    else:
        G3 = [
            C('Dòng TỔNG bằng tổng các dòng nhân viên mọi trang', 'P0', KY, ['Cộng Số lượt, Khối lượng, Số tiền 14 nhân viên (2 trang, hoặc Số dòng/trang 20)'], '',
              ['Tổng = dòng TỔNG: 133 lượt, Số tiền 10,245,700', 'Dòng TỔNG không đổi khi sang trang 2']),
            C('Số lượt và Số tiền của 1 nhân viên', 'P0', 'Kỳ Tháng trước, Lê Văn Chiến 24 lượt.', ['Bấm số 24 của Lê Văn Chiến', 'Cộng cột Số tiền trong popup (Số dòng/trang 50)'], '',
              ['Popup có đúng 24 lượt, dòng phụ "24 lượt · Số tiền: 1,546,900 · Kỳ tháng 10/2026"', 'Tổng Số tiền các lượt = 1,546,900 = dòng nhân viên trên báo cáo']),
            C('Số tiền là tiền công của nhân viên trên lượt', 'P0', 'Lượt PXH-41234 có Lê Văn Chiến bốc xếp, tiền công 51,300.', ['Mở PXH-41234 tab Bốc xếp, đọc tiền công Lê Văn Chiến', 'So với dòng PXH-41234 trong popup của Lê Văn Chiến'], '',
              ['Số tiền 51,300 bằng tiền công ghi trên phiếu (không cộng VAT)']),
            C('Lượt nhiều người bốc xếp', 'P0', 'Kỳ Tháng trước: 7 nhân viên (dòng IV đến X) cùng 7 lượt, cùng 180.2 tấn.', ['Mở popup của 2 nhân viên trong nhóm', 'So các phiếu và khối lượng'], '',
              ['Cùng các phiếu hạch toán, mỗi người được tính đủ khối lượng lượt (180.2 tấn mỗi người)', 'Số tiền mỗi người là tiền công riêng (773,050, 772,350…)',
               'Lưu ý: dòng TỔNG cộng lặp khối lượng / số lượt của lượt nhiều người — đúng thiết kế, không ghi Failed']),
            C('Tính cả lượt công ty tự bốc và thuê ngoài', 'P1', 'Kỳ có lượt loại thuê "Công ty" có người bốc xếp.', ['Tìm nhân viên của lượt đó'], '',
              ['Lượt có trên báo cáo theo nhân viên (khác báo cáo theo nhà cung cấp chỉ tính thuê ngoài)']),
            C('Khối LƯỢT BỐC XẾP khớp bảng', 'P0', KY, ['Đọc khối LƯỢT BỐC XẾP'], '',
              ['Lượt bốc xếp 133 = Lượt nhập hàng 51 + Lượt xuất hàng 82 = Số lượt dòng TỔNG', '"Số tiền 10,245,700" = Số tiền dòng TỔNG']),
            C('Khối THEO LOẠI BỐC XẾP khớp bảng', 'P1', KY, ['Cộng số lượt và số tiền 7 ô loại'], '',
              ['Tổng số lượt = 133; tổng số tiền = 10,245,700', 'Ô xếp theo số tiền giảm dần']),
            C('Lọc Công ty theo công ty của nhân viên', 'P1', SA + ' Nhân viên A thuộc công ty X bốc xếp cho phiếu của công ty Y.', ['Chọn Công ty = X', 'Chọn Công ty = Y'], '',
              ['Bước 1: có dòng nhân viên A', 'Bước 2: không có A (lọc theo công ty của nhân viên, không theo công ty của phiếu)']),
        ]
    G3 += [
        C('Phiếu chưa hạch toán không lên báo cáo', 'P0', 'Có Phiếu %s hàng có lượt bốc xếp nhưng chưa hạch toán.' % ('xuất' if ncc else 'nhập'), ['Lọc kỳ chứa ngày lập phiếu', 'Tìm phiếu đó'], '',
          ['Lượt của phiếu chưa hạch toán KHÔNG có trên báo cáo', 'Sau khi phiếu được hạch toán: lượt xuất hiện ở kỳ chứa ngày hạch toán']),
        C('Định dạng số', 'P1', 'Kỳ Năm nay.', ['Đọc các cột số'], '',
          ['Số có dấu phẩy ngăn nghìn (vd %s); khối lượng lẻ hiện tối đa 2 chữ số sau dấu chấm' % ('108,392,728' if ncc else '185,902,800'),
           'Dòng nhóm / TỔNG bằng 0 hiện "0"; ô khối tổng hợp bằng 0 thì ẩn (trừ ô Lượt bốc xếp)']),
        C('Định dạng ngày giờ', 'P2', 'Báo cáo có lượt.', ['Đọc cột Ngày hạch toán' + (' ở bảng' if ncc else ' trong popup') + ', Ngày bốc xếp trong popup'], '',
          ['Dạng dd/mm/yyyy HH:mm (vd "07/11/2026 00:14")']),
        C('Số liệu đúng phạm vi quyền ở mọi con số', 'P1', 'Tài khoản không có quyền.', ['Mở báo cáo', 'So khối tổng hợp, TỔNG, popup'], '',
          ['Mọi con số chỉ gồm ' + K['pham_vi_minh']]),
    ]

    # ======================================================================== IV. XEM CHI TIẾT
    pop_kv = KY if ncc else 'Kỳ Tháng trước, Lê Văn Chiến 24 lượt.'
    G4 = [
        C('Mở popup từ số lượt dòng TỔNG', 'P0', KY, ['Bấm số lượt ở dòng TỔNG'], '',
          ['Popup tiêu đề "Tất cả lượt bốc xếp", dòng phụ "%s"' % ('2 lượt · Số tiền (sau VAT): 445,400 · Kỳ tháng 11/2026' if ncc else '133 lượt · Số tiền: 10,245,700 · Kỳ tháng 10/2026'),
           'Có đủ 3 ô lọc: Chọn %s, Chọn nhập / xuất, Chọn loại bốc xếp; dòng đếm "%s"' % (dv, '2 / 2 lượt' if ncc else '133 / 133 lượt')]),
        C('Mở popup từ dòng %s' % dv, 'P0', pop_kv, ['Bấm số lượt ở dòng ' + ('ETEK GREEN' if ncc else 'Lê Văn Chiến')], '',
          ['Tiêu đề "%s"' % ('CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN - 29TPHPTH-1' if ncc else 'Lê Văn Chiến - 12110292'),
           'Chỉ lượt của %s đó; ô "Chọn %s" bị ẩn' % (dv, dv), 'Số dòng = số lượt đã bấm' + ('' if ncc else ' (24)')]),
        C('Mở popup từ ô Lượt nhập hàng / Lượt xuất hàng', 'P1', 'Báo cáo có cả lượt nhập và xuất.', ['Bấm số ở ô Lượt xuất hàng của khối tổng hợp'], '',
          ['Tiêu đề "Lượt xuất hàng"; chỉ lượt của Phiếu xuất hàng; ô "Chọn nhập / xuất" bị ẩn']),
        C('Mở popup từ 1 loại bốc xếp', 'P1', 'Báo cáo có khối THEO LOẠI BỐC XẾP.', ['Bấm số lượt của 1 loại'], '',
          ['Tiêu đề "Loại bốc xếp: <tên loại>"; chỉ lượt loại đó; ô "Chọn loại bốc xếp" bị ẩn']),
        C('Số 0 không bấm được', 'P2', 'Kỳ không có lượt.', ['Bấm số 0 ở dòng TỔNG / ô Lượt bốc xếp'], '', ['Số 0 là chữ thường, không gạch chân, bấm không mở popup']),
        C('Các cột của popup', 'P1', pop_kv, ['Mở popup, đọc tiêu đề cột'], '',
          ['STT | %s | Ngày hạch toán | Phiếu hạch toán | Ngày bốc xếp | Phiếu nhập/xuất kho | Nhập/Xuất | Loại bốc xếp | Khối lượng (tấn) | %s' % (Dv, T),
           'Cột %s ghi tên, mã chữ nhỏ dòng dưới' % Dv, 'Mặc định 10 dòng/trang, chân "Hiển thị 1–… / N lượt"']),
        C('Tìm trong popup theo số phiếu', 'P0', pop_kv, ['Gõ "%s" vào ô "Tìm phiếu hạch toán / phiếu nhập xuất kho…"' % ('pxk-381' if ncc else 'pxh-412'), 'Bấm nút × trong ô'], '',
          ['Lọc ngay tại chỗ (không cần Enter), không phân biệt hoa thường, theo cả số phiếu hạch toán và số phiếu nhập / xuất kho', 'Dòng đếm "a / b lượt" giảm theo',
           'Bước 2: ô trống, về đủ dòng']),
        C('Lọc trong popup bằng các ô chọn', 'P1', 'Popup "Tất cả lượt bốc xếp" có cả Nhập và Xuất.', ['Chọn "Xuất" ở ô Chọn nhập / xuất', 'Chọn 1 loại ở ô Chọn loại bốc xếp', 'Bấm biểu tượng Xoá lọc'], '',
          ['Bước 1, 2: dòng đếm giảm theo, về trang 1', 'Biểu tượng Xoá lọc chỉ hiện khi đang lọc', 'Bước 3: bỏ hết lọc, về đủ dòng']),
        C('Không có dòng khớp lọc trong popup', 'P2', 'Đang mở popup.', ['Gõ "zzz999" vào ô tìm'], '', ['Bảng "Không có lượt bốc xếp nào khớp bộ lọc.", dòng đếm "0 / N lượt"']),
        C('Sắp xếp trong popup', 'P1', pop_kv, ['Bấm tiêu đề cột %s' % T, 'Bấm lần nữa', 'Bấm tiêu đề Ngày hạch toán'], '',
          ['Bước 1, 2: tăng / giảm theo số tiền', 'Bước 3: theo ngày giờ đúng thứ tự thời gian (không theo chữ)', 'Sắp xếp trên tập đang lọc, giữ khi chuyển trang trong popup']),
        C('Phân trang trong popup', 'P2', 'Popup có hơn 10 dòng.', ['Sang trang 2', 'Đổi Số dòng/trang = 50'], '', ['STT liên tục 11, 12…', 'Đổi số dòng về trang 1']),
        C('Mở phiếu từ popup', 'P1', 'Đang mở popup.', ['Bấm số Phiếu hạch toán', 'Bấm số Phiếu nhập/xuất kho'], '', ['Mở đúng phiếu ở tab mới; popup vẫn mở ở tab cũ']),
        C('In danh sách của popup', 'P1', 'Đang mở popup.', ['Bấm "In danh sách"', 'Bỏ tích vài cột, bấm In'], '',
          ['Cửa sổ "In danh sách", "Chọn cột in" liệt kê đúng các cột của popup, tích sẵn hết, nút In / Hủy',
           'Bản xem trước "%s", có dòng tiêu đề của ô đã bấm, chỉ các cột đã chọn, đúng các dòng đang lọc trong popup' % K['tieu_de_ds']]),
        C('Xuất Excel danh sách của popup', 'P1', 'Đang mở popup, đã gõ từ khoá lọc.', ['Bấm "Xuất Excel danh sách"', 'Bấm "Xuất Excel"', 'Mở file'], '',
          ['Cửa sổ "Xuất Excel danh sách", "Chọn cột xuất"', 'Tải file "danh_sach_luot_boc_xep_<yyyymmdd>.xlsx"',
           'File: tiêu đề "%s", dòng tiêu đề ô đã bấm, dòng kỳ, dòng "N lượt · Khối lượng: X tấn · Số tiền: Y VND", các lượt khớp lọc, dòng TỔNG' % K['tieu_de_ds']]),
        C('Đóng popup và mở lại', 'P1', 'Đang mở popup đã lọc / sắp xếp / sang trang 2.', ['Bấm "Đóng"', 'Mở lại popup cùng con số'], '',
          ['Bước 1: về báo cáo, giữ bộ lọc và trang', 'Bước 2: popup ở trạng thái sạch (không lọc, không sắp xếp, trang 1)', 'Nút × góc phải đóng giống nút Đóng']),
        C('Popup theo đúng bộ lọc báo cáo', 'P1', 'Báo cáo đang lọc ' + ('Loại bốc xếp = Bốc xếp hàng, kỳ Năm nay.' if ncc else 'Công ty X, kỳ Năm nay.'), ['Bấm số lượt dòng TỔNG'], '',
          ['Popup chỉ gồm lượt thoả bộ lọc báo cáo; số dòng = số lượt dòng TỔNG']),
    ]

    # ======================================================================== V. TÙY CHỈNH CỘT
    nC = len(K['cot_so']) + 2
    G5 = [
        C('Mở cửa sổ Tuỳ chỉnh cột', 'P1', 'Đang mở màn.', ['Bấm nút biểu tượng cột (Cấu hình cột hiển thị)'], '',
          ['Cửa sổ "Tuỳ chỉnh cột", dòng "Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."',
           'Danh sách: STT, %s, %s; nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng; dòng "Đang chọn %d/%d cột"' % (K['cot_cay'], ', '.join(K['cot_so']), nC, nC)]),
        C('Cột bắt buộc không ẩn được', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.', ['Thử bỏ tích / kéo cột STT và %s' % K['cot_cay'], 'Bấm "Bỏ chọn hết"'], '',
          ['2 cột này luôn tích, không kéo được, luôn đứng đầu', 'Bỏ chọn hết chỉ bỏ các cột số liệu']),
        C('Ẩn cột rồi lưu', 'P0', 'Đang mở cửa sổ Tuỳ chỉnh cột.', ['Bỏ tích "Khối lượng (tấn)"', 'Bấm Lưu'], '',
          ['Cửa sổ đóng, bảng không còn cột Khối lượng (tấn) (cả dòng TỔNG)', 'Số liệu các cột khác không đổi, bộ lọc giữ nguyên']),
        C('Hiện lại cột đã ẩn', 'P1', 'Cột Khối lượng (tấn) đang ẩn.', ['Mở Tuỳ chỉnh cột, tích lại Khối lượng (tấn), Lưu'], '', ['Cột hiện lại đúng vị trí đã lưu']),
        C('Kéo đổi thứ tự cột', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.', ['Kéo ☰ của "%s" lên ngay sau %s' % (T, K['cot_cay']), 'Bấm Lưu'], '',
          ['Bảng hiện cột %s ngay sau cột %s, dòng TỔNG đổi theo' % (T, K['cot_cay'])]),
        C('Đóng không lưu', 'P2', 'Đang mở cửa sổ Tuỳ chỉnh cột.', ['Bỏ tích vài cột', 'Bấm Đóng'], '', ['Bảng giữ cấu hình cũ']),
        C('Giữ cấu hình sau F5 và theo tài khoản', 'P1', 'Tài khoản A đã ẩn 1 cột.', ['Nhấn F5', 'Đăng nhập tài khoản B, mở báo cáo'], '',
          ['A: sau F5 vẫn ẩn cột đó', 'B: thấy đủ cột (cấu hình lưu riêng từng tài khoản và từng màn)']),
        C('Tuỳ chỉnh cột không ảnh hưởng In / Xuất Excel', 'P2', 'Đã ẩn cột Khối lượng (tấn).', ['Bấm In báo cáo, xem danh sách "Chọn cột in"', 'Bấm Xuất Excel, xem "Chọn cột xuất"'], '',
          ['Cả 2 cửa sổ vẫn liệt kê và tích sẵn cột Khối lượng (tấn) (In / Excel chọn cột riêng)']),
    ]

    # ======================================================================== VI. XUẤT EXCEL
    G6 = [
        C('Mở cửa sổ Xuất Excel', 'P1', 'Báo cáo đã tải.', ['Bấm "Xuất Excel"'], '',
          ['Cửa sổ "Xuất Excel" có 2 lựa chọn: "Xuất bảng tổng hợp" (chọn sẵn, "Đúng bảng đang xem, đủ mọi trang%s, kèm dòng TỔNG.") và "Xuất danh sách lượt bốc xếp" ("Mỗi dòng 1 lượt bốc xếp, đúng bộ lọc báo cáo hiện tại.")' % (' và mọi lượt' if ncc else ''),
           'Khối "Chọn cột xuất": %s, tích sẵn hết, ô "Chọn tất cả"; icon (i) ghi cột luôn được xuất' % ', '.join(K['cot_so']), 'Nút "Xuất Excel" (xanh lá), "Hủy"']),
        C('Xuất bảng tổng hợp đủ cột', 'P0', KY, ['Bấm Xuất Excel > "Xuất Excel"', 'Mở file'], '',
          ['Tải file "%s"' % K['file'], 'Dòng 1 logo công ty; dòng 2 "%s"; dòng 3 "%s (theo ngày hạch toán)"' % (K['tieu_de_in'], 'Kỳ tháng 11/2026' if ncc else 'Kỳ tháng 10/2026'),
           'Hàng tiêu đề: STT, %s, %s' % (K['cot_cay'], ', '.join(K['cot_so'])),
           'Dòng TỔNG, dòng %s (STT I, II…)%s; số khớp màn hình' % (dv, ', dòng lượt (1, 2…)' if ncc else ''), 'Cuối file "Ngày dd Tháng mm Năm yyyy", "Người lập"']),
        C('Xuất một số cột', 'P1', 'Đang mở cửa sổ Xuất Excel.', ['Bỏ tích "Khối lượng (tấn)"', 'Bấm Xuất Excel'], '', ['File không có cột Khối lượng (tấn), các cột khác giữ đúng thứ tự']),
        C('Không chọn cột nào', 'P1', 'Đang mở cửa sổ Xuất Excel.', ['Bỏ tích "Chọn tất cả"', 'Bấm Xuất Excel'], '',
          ['Chữ đỏ "Vui lòng chọn ít nhất 1 cột để xuất", cửa sổ không đóng, không tải file']),
        C('Xuất danh sách lượt bốc xếp', 'P0', KY, ['Chọn "Xuất danh sách lượt bốc xếp", bấm Xuất Excel', 'Mở file'], '',
          ['Tải "danh_sach_luot_boc_xep_<yyyymmdd>.xlsx"; tiêu đề "%s"' % K['tieu_de_ds'],
           'Dòng "%s"' % ('2 lượt · Khối lượng: 5 tấn · Số tiền: 445,400 VND' if ncc else '133 lượt · Khối lượng: 1,403.1 tấn · Số tiền: 10,245,700 VND'),
           'Mỗi lượt 1 dòng với các cột %s, Ngày hạch toán, Phiếu hạch toán, Ngày bốc xếp, Phiếu nhập/xuất kho, Nhập/Xuất, Loại bốc xếp, Khối lượng (tấn), %s; dòng TỔNG cuối' % (Dv, T)]),
        C('Xuất lấy mọi trang theo bộ lọc', 'P0', NHIEU, ['Đứng ở trang 1 (10 dòng)', 'Lọc thêm 1 điều kiện', 'Xuất bảng tổng hợp'], '',
          ['File có đủ mọi %s khớp bộ lọc (bằng N ở chân bảng), không chỉ trang đang xem; dòng TỔNG = màn hình' % dv]),
        C('Xuất khi không có dữ liệu', 'P2', 'Bộ lọc cho ra "Không có lượt bốc xếp nào khớp bộ lọc."', ['Bấm Xuất Excel > Xuất Excel'], '',
          ['Không báo lỗi, vẫn tải file; file có tiêu đề, dòng kỳ, hàng tên cột, dòng TỔNG bằng 0']),
        C('Định dạng số và tiếng Việt trong file', 'P1', 'File vừa xuất có số liệu.', ['Bấm 1 ô Số tiền, xem thanh công thức', 'Chọn cả cột Số tiền, xem tổng ở thanh trạng thái', 'Đọc cột tên'], '',
          ['Ô số là kiểu SỐ (cộng được, không cảnh báo số lưu dạng chữ), hiển thị 1,234,567; khối lượng lẻ giữ chữ số thập phân', 'Ngày dạng dd/mm/yyyy HH:mm',
           'Tiếng Việt có dấu, ký tự (&, /, -, ngoặc, >=) hiển thị đúng']),
        C('Hủy cửa sổ Xuất Excel', 'P2', 'Đang mở cửa sổ Xuất Excel.', ['Bấm Hủy (hoặc ×)'], '', ['Đóng cửa sổ, không tải file; mở lại về mặc định (bảng tổng hợp, chọn hết cột)']),
    ]

    # ======================================================================== VII. IN
    G7 = [
        C('Mở cửa sổ In báo cáo', 'P1', 'Báo cáo đã tải.', ['Bấm "In báo cáo"'], '',
          ['Cửa sổ "In báo cáo": "In bảng tổng hợp" (chọn sẵn), "In danh sách lượt bốc xếp"; khối "Chọn cột in" tích sẵn hết; nút In, Hủy']),
        C('In bảng tổng hợp', 'P0', KY, ['Bấm In báo cáo > In'], '',
          ['Cửa sổ "%s" với nút In và ×' % K['xem_truoc'], 'Bản in: tiêu đề công ty, "%s", dòng kỳ + điều kiện lọc, bảng giống màn hình (dòng TỔNG, dòng %s in đậm%s)' % (K['tieu_de_in'], dv, ', dòng lượt' if ncc else ''),
           'Cuối bản in "Ngày dd Tháng mm Năm yyyy", "Người lập (Ký, họ tên)"']),
        C('In danh sách lượt bốc xếp', 'P1', KY, ['Chọn "In danh sách lượt bốc xếp", bấm In'], '',
          ['Cửa sổ "Xem trước danh sách lượt bốc xếp"; bản in "%s", mỗi lượt 1 dòng, đủ mọi trang theo bộ lọc' % K['tieu_de_ds']]),
        C('In theo cột đã chọn', 'P1', 'Đang mở cửa sổ In báo cáo.', ['Bỏ tích 2 cột, bấm In'], '', ['Bản in không có 2 cột đã bỏ; cột STT và %s luôn có' % K['cot_cay']]),
        C('Không chọn cột nào khi in', 'P1', 'Đang mở cửa sổ In báo cáo.', ['Bỏ tích "Chọn tất cả"', 'Bấm In'], '', ['Chữ đỏ "Vui lòng chọn ít nhất 1 cột để in", cửa sổ không đóng']),
        C('In vượt 2.000 dòng', 'P2', 'Bộ lọc cho ra hơn 2.000 dòng in (vd kỳ Năm nay%s).' % (', bản danh sách' if ncc else ' bản danh sách — môi trường thử 2,325 lượt'), ['Chọn In danh sách lượt bốc xếp > In'], '',
          ['Bản xem trước chỉ hiện "Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài."']),
        C('In ra máy in và đóng xem trước', 'P2', 'Đang ở cửa sổ xem trước.', ['Bấm In', 'Bấm ×'], '', ['Bước 1: hộp thoại in của trình duyệt mở, không mở tab mới', 'Bước 2: đóng xem trước, về báo cáo giữ nguyên']),
    ]

    # ======================================================================== VIII. RÀNG BUỘC
    G8 = [
        C('Lập phiếu có bốc xếp mới thì báo cáo tăng', 'P0', 'Ghi lại số nền dòng TỔNG và dòng %s Z kỳ Tháng này.' % dv,
          ['Lập Phiếu xuất hàng có lượt bốc xếp ' + ('Thuê ngoài, nhà cung cấp Z, thành tiền 100,000, VAT 8%' if ncc else 'có người bốc xếp Z, tiền công 50,000'), 'Hạch toán phiếu', 'Mở lại báo cáo'],
          ('Thành tiền 100,000; VAT 8%' if ncc else 'Tiền công Z: 50,000'),
          ['Trước khi hạch toán: báo cáo chưa đổi', 'Sau hạch toán: Số lượt TỔNG và dòng Z tăng 1; Số tiền tăng %s; Lượt xuất hàng tăng 1' % ('108,000' if ncc else '50,000')]),
        C('Phiếu hạch toán sang kỳ khác', 'P1', 'Phiếu lập tháng 11 nhưng hạch toán ngày thuộc tháng 10.', ['Xem kỳ Tháng này và Tháng trước'], '',
          ['Lượt nằm ở kỳ Tháng trước (theo ngày hạch toán), không ở Tháng này']),
        C('Khớp với báo cáo bốc xếp khác cùng kỳ', 'P1', 'Cùng tài khoản, cùng kỳ.',
          (['Ghi TỔNG báo cáo theo nhà cung cấp', 'Mở Báo cáo cẩu hàng bốc xếp theo nhân viên cùng kỳ'] if ncc else
           ['Ghi số lượt / số tiền Lê Văn Chiến kỳ Tháng trước', 'Mở Báo cáo chi tiết cẩu hàng bốc xếp theo nhân viên cùng kỳ']), '',
          (['2 báo cáo KHÁC nhau là đúng: theo nhà cung cấp chỉ lượt thuê ngoài, tiền sau VAT; theo nhân viên là tiền công từng người — ghi số vào Ghi chú'] if ncc else
           ['Dòng Lê Văn Chiến ở báo cáo chi tiết có cùng 24 lượt, 1,546,900'])),
    ]
    if ncc:
        G8.append(C('Đổi loại thuê trên phiếu', 'P2', 'Lượt Thuê ngoài đang có trên báo cáo; phiếu còn sửa được.', ['Sửa loại thuê lượt đó sang Công ty, lưu', 'Mở lại báo cáo'], '',
                    ['Lượt biến mất khỏi báo cáo; TỔNG giảm đúng số tiền lượt đó']))

    # ======================================================================== IX. PHÂN QUYỀN
    G9 = [
        C('Không có quyền vẫn mở được màn', 'P0', 'Tài khoản TK-NV không có quyền "%s".' % Q, ['Đăng nhập TK-NV', MENU], '',
          ['Mục menu hiện, màn mở bình thường, không báo thiếu quyền', 'Ô Công ty khoá ở công ty của TK-NV',
           'Chỉ thấy ' + K['pham_vi_minh'], 'Nút In báo cáo, Xuất Excel, Cấu hình cột vẫn hiện và dùng được (màn không có nút cần quyền riêng)']),
        C('Quyền mức Công ty', 'P0', 'TK-CT có Vai trò cấp "%s" mức Công ty, đang làm việc ở công ty A.' % Q, ['Đăng nhập TK-CT', 'Mở báo cáo kỳ Năm nay'], '',
          ['Ô Công ty khoá ở công ty A', 'Chỉ thấy ' + K['pham_vi_cty'] + ' (A)', 'Không thấy lượt của công ty khác; TỔNG nhỏ hơn hoặc bằng số của TK-SA']),
        C('Quyền mức Tổng công ty', 'P0', SA, ['Đăng nhập TK-SA', 'Mở báo cáo kỳ Năm nay', 'Chọn / bỏ ô Công ty'], '',
          ['Ô Công ty mở, liệt kê các công ty đang hoạt động; trống = mọi công ty', 'Thấy lượt của mọi công ty']),
        C('Có 2 Vai trò khác mức thì lấy mức lớn hơn', 'P1', 'Tài khoản có Vai trò mức Công ty và Vai trò mức Tổng công ty.', ['Đăng nhập', 'Mở báo cáo'], '',
          ['Ô Công ty mở, số liệu như TK-SA']),
        C('Đổi công ty đang làm việc', 'P1', 'TK-CT có mức Công ty ở công ty A và B.', ['Đang làm việc công ty A, mở báo cáo', 'Chuyển công ty làm việc sang B, mở lại báo cáo'], '',
          ['Bước 1: số liệu công ty A', 'Bước 2: ô Công ty khoá ở B, số liệu chỉ của B, không còn của A']),
        C('Mở màn bằng đường dẫn trực tiếp khi không có quyền', 'P1', 'TK-NV không có quyền; biết đường dẫn màn.', ['Dán đường dẫn màn vào thanh địa chỉ, nhấn Enter'], '',
          ['Màn mở như vào từ menu, chỉ thấy ' + K['pham_vi_minh']]),
        C('Đổi quyền giữa lúc đang xem', 'P1', 'TK-CT đang mở báo cáo.', ['Quản trị gỡ Vai trò mức Công ty của TK-CT', 'Ở màn đang mở, bấm Tìm kiếm', 'Nhấn F5'], '',
          ['Bước 2: số liệu thu hẹp ngay về ' + K['pham_vi_minh'], 'Không lúc nào hiện số ngoài phạm vi mới']),
        C('Phạm vi áp cho popup, bản In và file Excel', 'P1', 'TK-NV không có quyền, có lượt trong kỳ.', ['Mở popup "Tất cả lượt bốc xếp"', 'In báo cáo', 'Xuất Excel'], '',
          ['Popup, bản in, file đều chỉ có ' + K['pham_vi_minh'] + '; TỔNG khớp màn hình']),
        C('Người dùng không có quyền đổi ô Công ty', 'P2', 'TK-CT mức Công ty.', ['Thử bấm ô Công ty', 'Bấm Xóa lọc'], '', ['Ô Công ty mờ, không mở được danh sách; Xóa lọc vẫn giữ công ty của mình']),
    ]
    return [
        ('HIỂN THỊ TRANG & TRUY CẬP', G1),
        ('TÌM KIẾM & LỌC DANH SÁCH', G2),
        ('SỐ LIỆU BÁO CÁO', G3),
        ('XEM CHI TIẾT DANH SÁCH LƯỢT BỐC XẾP', G4),
        ('TÙY CHỈNH CỘT', G5),
        ('XUẤT DANH SÁCH EXCEL', G6),
        ('IN BÁO CÁO', G7),
        ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G8),
        ('PHÂN QUYỀN', G9),
    ]


def description(K):
    ncc, dv, T = K['ncc'], K['dv'], K['tien']
    j = '\n'.join
    return [
        ('1. Mục đích tính năng', j(['Báo cáo chỉ đọc: ' + K['muc_dich'][0].lower() + '.',
                                     'Chức năng: Xem báo cáo, Tìm kiếm / lọc, Xem danh sách lượt bốc xếp (popup), Tùy chỉnh cột, In, Xuất Excel.',
                                     'Đường vào: ' + K['menu_txt'] + '.'])),
        ('2. Đối tượng được tính / hiển thị', j([
            ('Lượt bốc xếp trên Phiếu nhập hàng / Phiếu xuất hàng có loại thuê "Thuê ngoài" và có nhà cung cấp, phiếu đã hạch toán.' if ncc else
             'Người bốc xếp trên lượt bốc xếp của Phiếu nhập hàng / Phiếu xuất hàng (mọi loại thuê), phiếu đã hạch toán; 1 lượt nhiều người thì mỗi người 1 dòng.'),
            'Bảng: dòng TỔNG -> dòng %s (I, II…)%s.' % (dv, ' -> dòng lượt (1, 2…)' if ncc else ''),
            'Cột: STT | %s | %s.' % (K['cot_cay'], ' | '.join(K['cot_so']))])),
        ('3. Đối tượng bị ẩn / không tính', j([
            '-  Phiếu chưa hạch toán; ngày hạch toán ngoài kỳ.',
            ('-  Lượt loại thuê "Công ty" (tự bốc xếp); lượt không có nhà cung cấp.' if ncc else '-  Lượt không có người bốc xếp.'),
            '-  Lượt ngoài phạm vi quyền của người xem.'])),
        ('4. Bộ lọc thời gian áp dụng cho', j(['Ô Kỳ lọc theo NGÀY HẠCH TOÁN (sớm nhất) của Phiếu nhập hàng / Phiếu xuất hàng chứa lượt.',
                                                'Tuần này / Tháng này (mặc định) / Tháng trước / Năm nay / Tuỳ chọn (ô Thời gian, tính cả 2 đầu mút).'])),
        ('5. Cấu trúc dữ liệu / cây phân cấp', j([('Cây 2 cấp: Nhà cung cấp -> lượt bốc xếp; ô chọn cấp "Chỉ nhà cung cấp" / "Đến từng lượt bốc xếp" (mặc định).' if ncc else
                                                   'Bảng 1 cấp: mỗi nhân viên 1 dòng; xem từng lượt qua popup.'),
                                                  'Phân trang theo %s, mặc định 10; %s xếp theo %s giảm dần.' % (dv, dv, T)])),
        ('6. Quy tắc cộng dồn / deduplicate', j([('-  Số tiền lượt = thành tiền × (1 + VAT%); nhóm / TỔNG cộng SAU VAT.' if ncc else
                                                   '-  Lượt nhiều người: Số lượt và Khối lượng được tính cho TỪNG người, dòng TỔNG cộng lặp — đúng thiết kế.'),
                                                  '-  Dòng TỔNG và khối tổng hợp tính trên toàn bộ dữ liệu đã lọc, không theo trang.'])),
        ('7. Phân quyền cấp', j(['Màn không chặn quyền vào; mọi người dùng mở được, không có nút cần quyền riêng.',
                                 '-  "%s" — mức: Tổng công ty / Công ty.' % CH.QUYEN,
                                 '-  Tổng công ty: mọi công ty, ô Công ty mở.',
                                 '-  Công ty: ' + K['pham_vi_cty'] + '; ô Công ty khoá.',
                                 '-  Không quyền: ' + K['pham_vi_minh'] + '.'])),
        ('8. Cách tính các ô thống kê', j(['Khối LƯỢT BỐC XẾP: Lượt bốc xếp = Lượt nhập hàng + Lượt xuất hàng; Số tiền = tổng %s.' % T,
                                           'Khối THEO LOẠI BỐC XẾP: số lượt + số tiền từng loại, xếp theo số tiền giảm dần.',
                                           'Chân bảng "Hiển thị a–b / N %s".' % dv])),
        ('9. Ghi chú đọc bảng', j(['-  Số dạng 1,234,567; khối lượng tối đa 2 chữ số lẻ; ngày dd/mm/yyyy HH:mm.',
                                   '-  Màn KHÔNG ghi nhớ bộ lọc: F5 / quay lại đều về Tháng này.',
                                   ('-  Nhà cung cấp không còn trong danh mục hiện "Nhà cung cấp #<số>".' if ncc else '-  Ô Nhân viên liệt kê người có lượt ở mọi kỳ, không riêng kỳ đang xem.'),
                                   'Dữ liệu mẫu: môi trường thử 18/11/2026. TK-SA (mức Tổng công ty), TK-CT (mức Công ty, công ty A), TK-NV (không quyền).'])),
    ]


def run(here, k):
    K = CH.kind(k)
    G = groups(K)
    out = os.path.join(here, 'testcase - %s.xlsx' % K['ten'])
    mod = 'BC bốc xếp theo NCC' if K['ncc'] else 'BC bốc xếp theo NV'
    build_chuan(out, 'Trang tính1', K['ten'] + ' - Cập nhật ngày ' + CH.NGAY, mod, description(K), sections(G), loai='bao_cao')
    print(' · '.join('%s %d' % (t, len(c)) for t, c in G), '· tổng', sum(len(c) for _, c in G))
