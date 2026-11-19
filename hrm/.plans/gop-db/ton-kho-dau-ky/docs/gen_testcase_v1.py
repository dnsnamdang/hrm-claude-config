# -*- coding: utf-8 -*-
"""Testcase màn "Khai báo tồn kho đầu kỳ" (STT 283, phân hệ Kho > Tồn kho đầu kỳ) — viết MỚI (chưa có TC cũ), khuôn
màn mẫu phiếu finance-declare-debt-beginning/docs/kh/gen_testcase.py (form 17 cột, tc_engine).

Nguồn: code HRM develop 02/11/2026 (xem gen_srs.py) + design/plan của feature (#11828, #11834, #11836, #11837, #11858).
Màn không có Chi tiết, Lịch sử, In; không qua duyệt — trạng thái do hệ thống tự xác định (Chưa / Đã có giao dịch).
Chạy: python gen_testcase.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402,F401  (đặt sys.path tới tc_engine)
from tc_engine import build  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Khai báo tồn kho đầu kỳ'
MODULE = 'Kho - Tồn kho đầu kỳ'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
COUNT = [0]


def L_(*lines):
    return '\n'.join(lines)


def T(n, func, prio, pre, steps, data, exp):
    COUNT[0] += 1

    def j(x):
        return x if isinstance(x, str) else L_(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'phân hệ Kho > menu Tồn kho đầu kỳ > "Khai báo tồn kho đầu kỳ"'
BC = 'phân hệ Kho > Báo cáo kho > "Báo cáo tồn kho theo vị trí"'
TK = 'phân hệ Kho > Báo cáo kho > "Thẻ kho"'
LECH = 'Hàng hóa H-1 khác số lượng đã khai kho kế toán, không thể nhập tồn đầu!'
GD = 'Hàng hóa đã có giao dịch, không thể sửa / xóa tồn đầu!'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '- TK-A: nhân viên công ty TPE, có quyền "Khai báo tồn kho đầu kỳ", không được làm việc ở công ty EG.',
    '- TK-ADMIN: quản trị cao nhất của hệ thống. TK-Z: KHÔNG có quyền "Khai báo tồn kho đầu kỳ".',
    '- Kho PTT (Phan Trọng Tuệ) có kho kế toán của TPE; kho EG_LN chỉ có kho kế toán của EG.',
    '- Hàng H-1: đã khai tồn kho KẾ TOÁN đầu kỳ 10 Bộ tại kho PTT của TPE, CHƯA khai tồn kho đầu kỳ.',
    '- Hàng H-0: chưa khai tồn kho kế toán đầu kỳ tại kho PTT.',
    '- Nhóm N-TU-DO: BLNS-IR-EVOPYRO tại PTT / TPE, 2 vị trí (PTT-N1-D1-K1-T1: 4, N1-T2-KV: 6), chưa có giao dịch.',
    '- Nhóm N-GD: 2Q-GSAQ tại LN / TPE, đã có giao dịch kho (đã xuất / chuyển vị trí).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Khai báo tồn kho đầu kỳ" khai báo TỒN KHO THỰC TẾ ĐẦU KỲ theo hàng × kho × vị trí × công ty — số mở đầu cho thẻ '
        'kho và các báo cáo tồn kho.',
        'Luồng: chọn Kho + Công ty → "Chọn hàng hóa" → mỗi hàng chia số lượng vào 1 hoặc nhiều vị trí, tổng phải bằng SL tồn '
        'kế toán → Lưu. Lưu xong có hiệu lực ngay, KHÔNG qua duyệt.',
        'Đường vào: ' + MENU + '.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới, Sửa (theo nhóm), Xóa (theo nhóm), '
        'Xuất Excel, Import Excel. KHÔNG có trang Chi tiết, Lịch sử, In.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        '- Quản trị cao nhất: dòng của mọi công ty; có cột Công ty và ô lọc Công ty.',
        '- Người khác: chỉ dòng của công ty được làm việc (công ty đang làm việc, công ty gắn vai trò, công ty được giao quản lý).',
        '- Ô Kho ở bộ lọc: kho thường và kho thanh lý đang hoạt động, có kho kế toán của công ty được làm việc.',
        '- Popup chọn vị trí: vị trí đang hoạt động của kho khai báo (vị trí / khoang / dãy / nhà không bị khóa).',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Dòng của công ty ngoài phạm vi: không hiện.',
        '- Nút Sửa / Xóa ẨN HẲN khi nhóm (hàng, kho, công ty) ĐÃ CÓ GIAO DỊCH: có nhập / xuất / điều chuyển khác tồn đầu, hoặc '
        'có phiếu chuyển vị trí / phiếu xuất (kể cả nháp) lấy từ lô tồn đầu.',
        '- Hàng chưa khai tồn kế toán tại kho, hàng đã khai tại kho + công ty: bị chặn khi chọn vào form.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Màn không có ô lọc theo ngày. Ngày tạo / Ngày cập nhật chỉ để hiển thị và sắp xếp.',
        'Bộ lọc được ghi nhớ 10 phút khi rời màn rồi quay lại.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Một dòng danh sách = 1 hàng × 1 vị trí. Nhóm = mọi vị trí của cùng hàng tại cùng kho + công ty.',
        'Sửa: trang Sửa liệt kê mọi vị trí của nhóm, chỉ sửa Số lượng. Xóa: xóa cả nhóm.',
        'Trạng thái (hệ thống tự xác định): Chưa có giao dịch (Sửa, Xóa được) → Đã có giao dịch (chỉ xem); Xóa → nhóm bị gỡ, khai lại được.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Tổng số lượng các vị trí của 1 hàng (quy ĐVT cơ bản) PHẢI BẰNG SL tồn kế toán đầu kỳ (Thêm, Sửa, Import).',
        '- Mỗi nhóm (hàng, kho, công ty) chỉ khai 1 lần; trong 1 hàng không trùng vị trí; trong 1 lần lưu không trùng hàng.',
        '- Lưu / Sửa / Xóa cộng / điều chỉnh / trừ tồn kho thực tế theo kho, vị trí, công ty.',
    )),
    ('7. Phân quyền cấp', L_(
        '- "Khai báo tồn kho đầu kỳ" (phân hệ Kho, nhóm Tồn kho đầu kỳ): thấy menu, vào màn và dùng mọi chức năng.',
        '- Không có quyền phạm vi riêng; phạm vi theo công ty như mục 2.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N": N = tổng dòng khớp bộ lọc và phạm vi.',
        'Trang Thêm / Sửa: "Tổng số lượng" của hàng = tổng các vị trí; "Tổng cộng" = tổng mọi hàng.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '- Số theo chuẩn quốc tế: 1,234.56; ô trống để trống.',
        '- Kiểm số liệu: sau Lưu / Sửa / Xóa mở ' + BC + ' và ' + TK + ' của hàng để thấy tồn đổi theo.',
        '- Cột kết quả / check để trống cho tester điền.',
    )),
]

# ------------------------------------------------------------------ PHÂN QUYỀN + PHẠM VI
ROLE_TCS = [
    T('00', 'Không có quyền thì không thấy menu, không xem được dữ liệu', 'P0', 'TK-Z',
      ['1. Đăng nhập TK-Z', '2. Mở phân hệ Kho, menu Tồn kho đầu kỳ', '3. Dán đường dẫn màn danh sách lên thanh địa chỉ'], 'Tài khoản TK-Z',
      ['- Menu Tồn kho đầu kỳ KHÔNG có "Khai báo tồn kho đầu kỳ"',
       '- Dán đường dẫn: báo "Bạn không có quyền thực hiện chức năng này", bảng không có dữ liệu']),
    T('01', 'Có quyền: đủ chức năng', 'P0', 'TK-A',
      ['1. Đăng nhập TK-A', '2. Vào ' + MENU], 'Tài khoản TK-A',
      ['- Danh sách hiện, chân bảng "Hiển thị 1–10 / N"',
       '- Có nút Tạo mới, Import Excel, Xuất Excel, biểu tượng Cấu hình cột hiển thị',
       '- Dòng nhóm chưa có giao dịch có Sửa, Xóa; dòng nhóm đã có giao dịch không có nút']),
    T('02', 'Phạm vi: người dùng thường chỉ thấy công ty được làm việc', 'P0', 'TK-A (TPE); có dòng khai báo của EG',
      ['1. Đăng nhập TK-A, vào màn', '2. Tìm mã hàng của dòng thuộc EG', '3. Bấm Tìm kiếm nâng cao'], '—',
      ['- Không thấy dòng của EG', '- Không có cột Công ty, không có ô lọc Công ty']),
    T('03', 'Phạm vi: quản trị cao nhất thấy mọi công ty', 'P0', 'TK-ADMIN',
      ['1. Đăng nhập TK-ADMIN, vào màn', '2. Bấm Tìm kiếm nâng cao, chọn Công ty = EG'], '—',
      ['- Bảng có cột Công ty (mã công ty)', '- Có ô lọc Công ty dạng "Mã - Tên"; chọn EG chỉ còn dòng của EG']),
    T('04', 'Khai báo cho công ty ngoài phạm vi bị chặn', 'P1', 'TK-A; file import có dòng Mã công ty = EG',
      ['1. Mở Tạo mới, mở ô Công ty', '2. Import file, bấm Validate'], '—',
      ['- Ô Công ty chỉ liệt kê công ty TK-A được làm việc (không có EG)',
       '- Dòng import của EG báo "Bạn không được làm việc tại công ty này"']),
]

# ------------------------------------------------------------------ I. HIỂN THỊ
S1 = [
    T('001', 'Vào màn qua menu', 'P0', 'TK-A',
      ['1. Vào ' + MENU], '—',
      ['- Tiêu đề trang "Khai báo tồn kho đầu kỳ", tiêu đề bảng "Danh sách khai báo tồn kho đầu kỳ"',
       '- Bảng 10 dòng, dòng khai báo mới nhất đứng đầu, tự tải không cần bấm Tìm kiếm']),
    T('002', 'Bộ cột mặc định', 'P0', 'Tài khoản chưa từng tùy chỉnh cột ở màn này',
      ['1. Mở màn', '2. Đọc tiêu đề cột từ trái sang phải'], '—',
      ['- TK-A: STT, Tên hàng, Mã hàng, Kho, Mã vị trí, Vị trí, ĐVT, Số lượng, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, Hành động',
       '- TK-ADMIN: thêm cột Công ty sau Vị trí']),
    T('003', 'Định dạng số, người, ngày, ô trống', 'P1', 'Có dòng số lượng lẻ (406.81) và dòng chưa ai sửa',
      ['1. Đọc cột Số lượng, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật'], '—',
      ['- Số lượng "406.81", căn phải; số nguyên không có phần lẻ',
       '- Người tạo "Họ tên - Mã phòng ban"; Ngày tạo dd/mm/yyyy HH:mm',
       '- Dòng chưa ai sửa: Người cập nhật, Ngày cập nhật để TRỐNG (không gạch, không 0)']),
    T('004', 'Tên hàng / Kho / Vị trí dài', 'P2', 'Có hàng tên dài hơn 2 dòng',
      ['1. Xem dòng đó', '2. Rê chuột lên tên'], '—',
      ['- Chữ xuống dòng, tối đa 2 dòng; rê chuột hiện đủ tên']),
]

# ------------------------------------------------------------------ II. LỌC
S2 = [
    T('001', 'Tìm nhanh theo mã hoặc tên hàng', 'P0', 'Có nhóm N-TU-DO',
      ['1. Gõ "EVOPYRO" vào ô tìm nhanh (chưa bấm gì)', '2. Nhấn Enter', '3. Gõ một phần tên hàng, bấm Tìm kiếm'], 'EVOPYRO',
      ['- Đang gõ bảng chưa đổi; Enter / Tìm kiếm mới lọc', '- Ra các dòng có mã hoặc tên chứa từ khóa',
       '- Placeholder "Tìm theo mã / tên hàng"']),
    T('002', 'Lọc theo Mã hàng', 'P1', '—',
      ['1. Mở Tìm kiếm nâng cao', '2. Ô Mã hàng gõ "2Q-GS", nhấn Enter'], 'Mã hàng: 2Q-GS',
      ['- Chỉ lọc khi Enter', '- Ra dòng có mã hàng chứa chuỗi đã gõ (không tìm theo tên)']),
    T('003', 'Lọc theo Kho', 'P0', '—',
      ['1. Mở ô Kho, xem danh sách', '2. Chọn "PTT - Phan Trọng Tuệ"'], 'Kho: PTT',
      ['- Danh sách "Mã - Tên kho", chỉ kho thường / thanh lý có kho kế toán của công ty được làm việc',
       '- Chọn là lọc ngay; mọi dòng có Kho = Phan Trọng Tuệ']),
    T('004', 'Lọc theo Vị trí (mã hoặc tên)', 'P1', '—',
      ['1. Ô Vị trí gõ "N1-T2", Enter', '2. Đổi sang "Tầng 1", Enter'], 'Vị trí: N1-T2 / Tầng 1',
      ['- Ra dòng có mã vị trí chứa "N1-T2"', '- Ra dòng có tên vị trí chứa "Tầng 1"']),
    T('005', 'Lọc theo Người tạo', 'P2', 'Có dòng do TK-A tạo',
      ['1. Ô Người tạo chọn nhân viên của TK-A'], '—',
      ['- Danh sách chỉ gồm người đã tạo khai báo trong phạm vi', '- Chỉ còn dòng do người đó tạo']),
    T('006', 'Kết hợp nhiều điều kiện, không có kết quả', 'P1', '—',
      ['1. Kho = PTT, Mã hàng = "KHONG-TON-TAI", Enter'], '—',
      ['- Bảng hiện "Không có dữ liệu phù hợp.", chân bảng 0']),
    T('007', 'Làm mới', 'P1', 'Đang lọc Kho + từ khóa',
      ['1. Bấm Làm mới'], '—',
      ['- Mọi ô lọc về trống, bảng nạp lại toàn bộ phạm vi từ trang 1']),
    T('008', 'Ghi nhớ bộ lọc khi rời màn', 'P2', 'Đang lọc Kho = PTT',
      ['1. Bấm Sửa một dòng', '2. Bấm Quay lại', '3. Chờ quá 10 phút ở màn khác rồi quay lại'], '—',
      ['- Bước 2: vẫn còn Kho = PTT', '- Bước 3: bộ lọc về mặc định']),
    T('009', 'Cài đặt bộ lọc', 'P2', '—',
      ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Người tạo", kéo "Vị trí" lên đầu, bấm Lưu', '3. F5', '4. Mở lại, bấm Khôi phục mặc định'], '—',
      ['- Cửa sổ liệt kê Mã hàng, Kho, Vị trí, Người tạo (TK-ADMIN thêm Công ty)', '- Sau F5: ô Người tạo ẩn, Vị trí đứng đầu',
       '- Khôi phục mặc định đưa về như ban đầu']),
]

# ------------------------------------------------------------------ III. DANH SÁCH
S3 = [
    T('001', 'Sắp xếp', 'P1', 'Có hơn 20 dòng',
      ['1. Bấm tiêu đề Tên hàng, bấm lần nữa', '2. Lần lượt bấm Mã hàng, Số lượng, Ngày tạo, Ngày cập nhật'], '—',
      ['- Mỗi cột sắp tăng rồi giảm dần, về trang 1', '- Cột Kho, Vị trí, Người tạo không có biểu tượng sắp xếp']),
    T('002', 'Phân trang và số dòng / trang', 'P1', 'Có hơn 50 dòng',
      ['1. Sang trang 3', '2. Đổi số dòng/trang sang 50'], '—',
      ['- Trang 3 STT bắt đầu từ 21', '- Đổi 50 dòng thì về trang 1, "Hiển thị 1–50 / N"']),
    T('003', 'Tùy chỉnh cột được ghi nhớ', 'P2', '—',
      ['1. Bấm biểu tượng Cấu hình cột hiển thị', '2. Bỏ cột Người cập nhật, Ngày cập nhật, kéo Số lượng lên sau Mã hàng, bấm Lưu', '3. F5'], '—',
      ['- Cửa sổ "Tuỳ chỉnh cột", "Đang chọn x/14 cột"; STT, Tên hàng, Hành động bị khóa',
       '- Sau Lưu và F5 bảng giữ đúng cấu hình']),
    T('004', 'Nút Sửa / Xóa theo trạng thái giao dịch', 'P0', 'Nhóm N-TU-DO và nhóm N-GD',
      ['1. Tìm các dòng của 2 nhóm'], '—',
      ['- Mọi dòng của N-TU-DO có Sửa, Xóa', '- Mọi dòng của N-GD KHÔNG có nút (ẩn hẳn, không hiện xám)']),
]

# ------------------------------------------------------------------ IV. THÊM MỚI
S4 = [
    T('001', 'Mở trang Thêm', 'P0', 'TK-A',
      ['1. Bấm Tạo mới'], '—',
      ['- Khối "Thông tin chung": ô Kho (*), Công ty (*) — đều trống, không chọn sẵn; góc phải "<tên TK-A> - <ngày giờ hiện tại>"',
       '- Khối "Hàng hóa": nút "Chọn hàng hóa" (bấm được khi đã chọn Kho và Công ty), bảng trống "Chưa chọn hàng hóa"',
       '- Cột: STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT (*), SL tồn kế toán, Tổng số lượng, Vị trí (*), Số lượng (*)',
       '- Chân trang: Lưu, Lưu và tiếp tục, Quay lại']),
    T('002', 'Ô Kho và Công ty độc lập', 'P1', '—',
      ['1. Chọn Kho = PTT', '2. Chọn Công ty = TPE', '3. Đổi Công ty sang công ty khác (bảng chưa có hàng)'], '—',
      ['- Ô Kho liệt kê kho có kho kế toán của công ty đang làm việc', '- Đổi Công ty KHÔNG xóa Kho đã chọn, danh sách Kho không đổi']),
    T('003', 'Chọn hàng hóa hợp lệ', 'P0', 'Kho PTT, Công ty TPE',
      ['1. Bấm Chọn hàng hóa', '2. Tìm H-1, tích chọn, bấm "Thêm (1)"'], 'H-1',
      ['- Cửa sổ "Chọn hàng hóa khai báo tồn đầu", dòng "Công ty <tên TPE>"',
       '- H-1 vào bảng: ĐVT = Bộ (không sửa được), SL tồn kế toán 10, 1 dòng vị trí trống, Số lượng = 10, Tổng số lượng 10']),
    T('004', 'Chặn hàng đã khai tồn đầu tại kho', 'P0', 'Kho PTT, Công ty TPE',
      ['1. Chọn hàng BLNS-IR-EVOPYRO, bấm Thêm'], '—',
      ['- Báo "BLNS-IR-EVOPYRO: Hàng hóa đã được khai báo tồn đầu kì. Kho: PTT"', '- Hàng không vào bảng']),
    T('005', 'Chặn hàng chưa khai tồn kế toán tại kho', 'P0', 'Kho PTT, Công ty TPE',
      ['1. Chọn H-0, bấm Thêm'], '—',
      ['- Báo "<mã H-0>: Hàng hóa chưa khai tồn kho kế toán đầu kỳ tại kho này, không thể nhập tồn đầu!"', '- Hàng không vào bảng']),
    T('006', 'Chọn nhiều hàng, hàng lỗi không chặn hàng hợp lệ', 'P1', '—',
      ['1. Tích H-1 và BLNS-IR-EVOPYRO, bấm "Thêm (2)"'], '—',
      ['- H-1 vào bảng; BLNS-IR-EVOPYRO báo lỗi riêng']),
    T('007', 'Popup chọn vị trí', 'P0', 'Bảng có H-1',
      ['1. Bấm ô Vị trí', '2. Gõ "PTT-N1-D1", Tìm kiếm', '3. Bấm vào một mã vị trí'], '—',
      ['- Cửa sổ "Chọn vị trí kho", dòng phụ "Vị trí của kho khai báo"; cột STT, Vị trí, Nhà, Dãy, Khoang; 10 dòng/trang',
       '- Chỉ vị trí của kho PTT, không có vị trí đang khóa', '- Bấm vị trí: ô điền mã vị trí, cửa sổ đóng']),
    T('008', 'Thêm vị trí tự điền phần còn thiếu', 'P0', 'H-1 dòng 1 đã chọn vị trí',
      ['1. Sửa Số lượng dòng 1 thành 4', '2. Bấm "Thêm vị trí"'], '—',
      ['- Dòng 2 có Số lượng = 6 (10 − 4)', '- Hiện link "Bỏ hàng hóa"; mỗi dòng vị trí có thùng rác "Xóa dòng vị trí"']),
    T('009', 'Không chọn trùng vị trí trong 1 hàng', 'P0', 'H-1 có 2 dòng, dòng 1 vị trí A',
      ['1. Ở dòng 2 chọn lại vị trí A'], '—',
      ['- Báo "Vị trí đã được chọn!", ô dòng 2 không đổi']),
    T('010', 'Tổng số lượng khác SL tồn kế toán', 'P0', 'H-1 hai vị trí 4 + 5',
      ['1. Bấm Lưu'], '—',
      ['- Tổng số lượng 9 chữ đỏ; các ô Số lượng của H-1 viền đỏ, dưới ô cuối "Tổng số lượng phải bằng SL tồn kế toán (10)"',
       '- Thông báo "' + LECH + '"', '- Không lưu']),
    T('011', 'Bỏ trống trường bắt buộc', 'P0', '—',
      ['1. Không chọn Kho, Công ty, bấm Lưu', '2. Chọn Kho, Công ty, thêm H-1, bỏ trống Vị trí, xóa Số lượng, bấm Lưu', '3. Nhập Số lượng 0, Lưu'], '—',
      ['- Bước 1: dưới Kho, Công ty "Bắt buộc phải chọn"; dưới bảng "Chưa chọn hàng hóa"; thông báo "Bạn chưa nhập đầy đủ thông tin."',
       '- Bước 2: dưới Vị trí "Bắt buộc phải chọn", dưới Số lượng "Bắt buộc phải nhập"', '- Bước 3: "Số lượng phải lớn hơn 0"',
       '- Cuộn tới ô lỗi đầu tiên']),
    T('012', 'Ô Số lượng chỉ nhận số', 'P1', '—',
      ['1. Gõ "abc", "-5", "1,000.5"'], '—',
      ['- Không nhận chữ, dấu âm', '- Nhận số thập phân']),
    T('013', 'Lưu thành công', 'P0', 'H-1 chia 2 vị trí 4 + 6 (tổng 10)',
      ['1. Bấm Lưu'], '—',
      ['- Báo "Thêm mới thành công", về danh sách', '- Có 2 dòng mới của H-1 (2 vị trí), Người tạo = TK-A, Người cập nhật trống',
       '- Hai dòng có Sửa, Xóa']),
    T('014', 'Lưu và tiếp tục', 'P1', 'Form hợp lệ',
      ['1. Bấm "Lưu và tiếp tục"'], '—',
      ['- Báo thành công, trang Thêm mở lại trống (Kho, Công ty trống, bảng trống)']),
    T('015', 'Đổi Kho / Công ty khi đã có hàng', 'P1', 'Bảng có H-1',
      ['1. Đổi Kho', '2. Bấm Hủy', '3. Đổi Kho lần nữa, bấm Đồng ý'], '—',
      ['- Hộp "Xác nhận": "Đổi công ty / kho sẽ xoá danh sách hàng hóa đã chọn. Tiếp tục?"', '- Hủy: giữ kho cũ và hàng',
       '- Đồng ý: kho mới, bảng về "Chưa chọn hàng hóa"']),
    T('016', 'Kho không thuộc công ty', 'P1', 'TK-ADMIN đang làm việc ở công ty EG (ô Kho có EG_LN, kho chỉ có kho kế toán của EG)',
      ['1. Chọn Kho = EG_LN, Công ty = TPE', '2. Bấm Chọn hàng hóa, thêm 1 hàng'], '—',
      ['- Báo "Kho không thuộc công ty đã chọn", không thêm hàng']),
    T('017', 'Quay lại khi đã nhập', 'P1', 'Đã chọn Kho, thêm hàng',
      ['1. Bấm Quay lại', '2. Bấm Ở lại', '3. Bấm Quay lại, bấm Thoát'], '—',
      ['- Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"', '- Ở lại: giữ form',
       '- Thoát: về danh sách, không lưu']),
    T('018', 'Bỏ hàng / xóa dòng vị trí', 'P2', 'Bảng có 2 hàng, hàng 1 có 2 vị trí',
      ['1. Bấm thùng rác dòng vị trí 2 của hàng 1', '2. Bấm thùng rác hàng 2'], '—',
      ['- Bước 1: hàng 1 còn 1 vị trí, Tổng số lượng cập nhật', '- Bước 2: hàng 2 bị bỏ khỏi bảng; Tổng cộng cập nhật']),
]

# ------------------------------------------------------------------ V. SỬA
S5 = [
    T('001', 'Mở trang Sửa theo nhóm', 'P0', 'Nhóm N-TU-DO',
      ['1. Bấm Sửa ở dòng vị trí N1-T2-KV'], '—',
      ['- Tiêu đề "Sửa khai báo tồn kho đầu kỳ: BLNS-IR-EVOPYRO"; góc phải "<người tạo> - <ngày giờ tạo>"',
       '- Hàng hóa, Đơn vị (*), Kho, SL tồn kế toán bị khóa',
       '- Khối Vị trí liệt kê ĐỦ 2 vị trí của nhóm (STT, Mã vị trí, Vị trí, Số lượng), dòng Tổng cộng', '- Chân trang: Lưu, Quay lại']),
    T('002', 'Sửa lệch SL tồn kế toán', 'P0', 'Đang ở trang Sửa N-TU-DO (SL kế toán 10)',
      ['1. Sửa vị trí 1 từ 4 thành 3', '2. Bấm Lưu'], '—',
      ['- Tổng cộng 9 chữ đỏ, ô Số lượng viền đỏ, "Tổng số lượng phải bằng SL tồn kế toán (10)"',
       '- Thông báo "Hàng hóa BLNS-IR-EVOPYRO khác số lượng đã khai kho kế toán, không thể nhập tồn đầu!"', '- Không lưu']),
    T('003', 'Sửa chia lại vị trí thành công', 'P0', 'N-TU-DO 4 + 6',
      ['1. Sửa thành 3 + 7', '2. Bấm Lưu', '3. Mở ' + BC + ' lọc hàng BLNS-IR-EVOPYRO'], '—',
      ['- Báo "Cập nhật thành công", về danh sách; 2 dòng hiện 3 và 7, Người cập nhật = người sửa',
       '- Báo cáo: vị trí 1 giảm 1, vị trí 2 tăng 1; tổng tại kho không đổi']),
    T('004', 'Trường Số lượng bắt buộc', 'P1', 'Trang Sửa',
      ['1. Xóa trống 1 ô Số lượng, Lưu', '2. Nhập 0, Lưu'], '—',
      ['- "Bắt buộc phải nhập" / "Số lượng phải lớn hơn 0"; thông báo "Bạn chưa nhập đầy đủ thông tin."']),
    T('005', 'Mở thẳng trang Sửa của nhóm đã có giao dịch', 'P0', 'Nhóm N-GD',
      ['1. Dán đường dẫn trang Sửa của 1 dòng N-GD'], '—',
      ['- Báo "' + GD + '"', '- Tự quay về danh sách']),
    T('006', 'Quay lại khi đã sửa', 'P2', 'Trang Sửa, đã đổi 1 số lượng',
      ['1. Bấm Quay lại'], '—',
      ['- Hỏi "Thông tin chưa lưu" (Thoát / Ở lại); chưa đổi gì thì về thẳng danh sách']),
]

# ------------------------------------------------------------------ VI. XÓA
S6 = [
    T('001', 'Hộp xác nhận xóa', 'P0', 'Nhóm N-TU-DO',
      ['1. Bấm Xóa ở 1 dòng', '2. Bấm Hủy'], '—',
      ['- Hộp "Xác nhận xóa": "Xóa khai báo tồn đầu của hàng BLNS-IR-EVOPYRO tại kho Phan Trọng Tuệ (tất cả vị trí của hàng tại kho này)?"',
       '- Hủy: đóng hộp, không đổi']),
    T('002', 'Xóa cả nhóm', 'P0', 'Nhóm vừa lập ở TC_04.013 (H-1, 2 vị trí)',
      ['1. Bấm Xóa ở 1 trong 2 dòng, bấm Xóa', '2. Mở ' + BC + ' lọc H-1'], '—',
      ['- Báo "Xóa thành công 2 dòng tồn đầu"; cả 2 dòng của H-1 biến mất', '- Báo cáo: tồn H-1 tại PTT về như trước khi khai']),
    T('003', 'Khai lại sau khi xóa', 'P1', 'Đã xóa nhóm H-1',
      ['1. Tạo mới, chọn H-1 tại PTT / TPE'], '—',
      ['- H-1 thêm vào bảng bình thường, lưu được']),
]

# ------------------------------------------------------------------ VII. IMPORT
S7 = [
    T('001', 'Mở cửa sổ và file mẫu', 'P1', '—',
      ['1. Bấm Import Excel', '2. Bấm Tải file mẫu'], '—',
      ['- Cửa sổ "Import khai báo tồn kho đầu kỳ"', '- File Mau_import_ton_kho_dau_ky.xlsx, cột: STT, Tên hàng *, Mã hàng *, ĐVT *, Mã kho *, Mã vị trí *, Số lượng *, Mã công ty *; dòng 2 là hướng dẫn']),
    T('002', 'Validate bắt lỗi từng cột', 'P0', 'File 4 dòng: (1) hàng đã khai tại PTT; (2) mọi mã sai, SL -5; (3) thiếu Tên hàng, ĐVT, Mã vị trí, SL 0; (4) kho LN với công ty EG',
      ['1. Chọn file, Load lên bảng', '2. Validate'], '—',
      ['- "Validate xong: 0 hợp lệ, 4 không hợp lệ"',
       '- (1) "Hàng hóa BLNS-IR-EVOPYRO đã được khai báo tồn đầu kỳ tại kho PTT, không thể nhập tiếp!"',
       '- (2) "Số lượng phải lớn hơn 0 và không quá 999,999,999", "Công ty không tồn tại", "Hàng hóa không tồn tại", "Đơn vị không tồn tại", "Kho không tồn tại"',
       '- (3) "Thiếu Tên hàng", "Thiếu ĐVT", "Thiếu Mã vị trí", "Số lượng phải lớn hơn 0…", "Hàng hóa không tồn tại"',
       '- (4) "Kho không thuộc công ty (chưa có kho kế toán của công ty)"']),
    T('003', 'Nhóm nhiều dòng phải khớp tồn kế toán', 'P0', 'H-1 (kế toán 10): file 2 dòng 4 + 5',
      ['1. Load, Validate', '2. Sửa dòng 2 thành 6, Validate lại'], '—',
      ['- Bước 1: cả 2 dòng báo "Hàng hóa H-1 khác số lượng đã khai kho kế toán (10 theo ĐVT cơ bản, đang nhập 9), không thể nhập tồn đầu!"',
       '- Bước 2: 2 dòng hợp lệ, bị khóa']),
    T('004', 'Một dòng lỗi làm cả nhóm không được ghi', 'P1', 'H-1: 2 dòng, dòng 2 sai mã vị trí',
      ['1. Validate'], '—',
      ['- Dòng 2 "Vị trí không tồn tại trong kho"; dòng 1 "Cùng hàng + kho + công ty với dòng lỗi khác trong file — cả nhóm không được ghi"']),
    T('005', 'Cùng nhóm dùng 2 ĐVT / trùng vị trí', 'P2', 'H-1: 2 dòng khác ĐVT; file khác có 2 dòng cùng vị trí',
      ['1. Validate từng file'], '—',
      ['- "Cùng một hàng tại 1 kho phải dùng 1 ĐVT"', '- "Vị trí đã được chọn!"']),
    T('006', 'Bỏ dòng lỗi rồi Import', 'P0', 'File: H-1 hợp lệ (10) + 1 dòng lỗi',
      ['1. Validate', '2. Bấm Bỏ dòng lỗi', '3. Bấm Import'], '—',
      ['- Còn 1 dòng hợp lệ; Import báo số dòng thành công, danh sách tải lại có H-1',
       '- Báo cáo tồn theo vị trí có H-1 = 10 tại vị trí trong file']),
    T('007', 'File quá 200 dòng', 'P2', 'File 201 dòng',
      ['1. Chọn file, Load / Import'], '—',
      ['- Báo vượt giới hạn 200 dòng, không nhập']),
    T('008', 'Nhóm bị người khác khai trước khi Import', 'P2', 'Validate xong file H-1; người khác vừa lưu H-1 tại cùng kho + công ty',
      ['1. Bấm Import'], '—',
      ['- Nhóm H-1 bị bỏ qua, kết quả nêu dòng lỗi "đã được khai báo tồn đầu kỳ"; nhóm khác vẫn nhập']),
]

# ------------------------------------------------------------------ VIII. XUẤT EXCEL
S8 = [
    T('001', 'Xuất Excel theo bộ lọc', 'P0', 'Đang lọc Kho = PTT, hơn 10 dòng',
      ['1. Bấm Xuất Excel', '2. Bỏ tích Người cập nhật, kéo Số lượng lên đầu, bấm Xuất file'], '—',
      ['- Cửa sổ "Chọn trường xuất Excel" tích sẵn các cột đang hiện; "Đang chọn x/12 trường"',
       '- Cạnh nút có dòng tiến độ; xong báo "Xuất Excel thành công"',
       '- File Khai_bao_ton_dau_vat_ly.xlsx, tiêu đề "DANH SÁCH KHAI BÁO TỒN KHO ĐẦU KỲ", có cột STT; đủ mọi dòng khớp bộ lọc (mọi trang), cột đúng thứ tự đã kéo',
       '- Cột Số lượng là SỐ (SUM được)']),
    T('002', 'Xuất khi không có dữ liệu', 'P2', 'Lọc Mã hàng "KHONG-TON-TAI"',
      ['1. Bấm Xuất Excel, Xuất file'], '—',
      ['- Báo "Không có dữ liệu để xuất", không tải file']),
    T('003', 'Phạm vi khi xuất', 'P1', 'TK-A',
      ['1. Không lọc gì, xuất toàn bộ'], '—',
      ['- File không có dòng của công ty ngoài phạm vi; số dòng = N ở chân bảng']),
]

# ------------------------------------------------------------------ IX. TÁC ĐỘNG SỐ LIỆU / RÀNG BUỘC
S9 = [
    T('001', 'Lưu cộng tồn kho đúng kho, vị trí, công ty', 'P0', 'H-1 chưa khai',
      ['1. Khai H-1 tại PTT / TPE: vị trí A 4, vị trí B 6, Lưu', '2. Mở ' + BC + ' lọc H-1', '3. Mở ' + TK + ' của H-1 tại PTT'], '—',
      ['- Báo cáo: vị trí A 4, vị trí B 6, tổng 10, công ty TPE', '- Thẻ kho có dòng tồn đầu kỳ của H-1 = 10']),
    T('002', 'Khóa khi phát sinh giao dịch', 'P0', 'H-1 đã khai (TC_09.001)',
      ['1. Lập phiếu điều chuyển vị trí (có thể để nháp) chuyển H-1 từ vị trí A', '2. Quay lại danh sách'], '—',
      ['- Mọi dòng của H-1 tại PTT mất nút Sửa, Xóa', '- Tạo mới chọn lại H-1 tại PTT: bị chặn đã khai']),
    T('003', 'Hai người cùng khai 1 hàng', 'P1', '2 tài khoản cùng mở trang Thêm, cùng chọn H-1 tại PTT / TPE hợp lệ',
      ['1. Người 1 bấm Lưu', '2. Người 2 bấm Lưu'], '—',
      ['- Người 2: dưới Tên hàng "Hàng hóa H-1 đã được khai báo tồn đầu kỳ tại kho PTT, không thể nhập tiếp!"',
       '- Chỉ có 1 bộ khai báo của H-1']),
    T('004', 'Nhóm vừa phát sinh giao dịch khi đang sửa', 'P1', 'A mở trang Sửa N-TU-DO; B lập phiếu chuyển vị trí từ lô tồn đầu',
      ['1. A bấm Lưu (tổng vẫn khớp)'], '—',
      ['- A bị từ chối "' + GD + '", dữ liệu không đổi']),
    T('005', 'Không xóa được kho / vị trí / hàng đã có khai báo', 'P2', 'Nhóm H-1 tại PTT, vị trí A',
      ['1. Danh mục Vị trí: xóa vị trí A', '2. Danh mục Kho vật lý: xóa kho PTT', '3. Danh mục hàng hoá: xóa H-1'], '—',
      ['- Mỗi thao tác bị chặn do đang được dùng']),
]

# ------------------------------------------------------------------ X. LUỒNG ĐẦU CUỐI
S10 = [
    T('001', 'Luồng đầu cuối: khai, sửa, xóa, khai lại', 'P0', 'H-1 chưa khai, kế toán 10',
      ['1. Khai H-1 một vị trí 10', '2. Cần chia thêm vị trí: trang Sửa không thêm được vị trí nên Xóa cả nhóm', '3. Khai lại 2 vị trí 3 + 7', '4. Xem ' + BC], '—',
      ['- Mỗi bước báo thành công; báo cáo cuối: 3 và 7 ở đúng 2 vị trí, tổng 10']),
    T('002', 'Luồng đầu cuối: import rồi phát sinh giao dịch', 'P1', 'File import H-1 hợp lệ',
      ['1. Import', '2. Lập phiếu xuất kho điều chỉnh kiểm kê lấy từ lô tồn đầu của H-1', '3. Quay lại danh sách, mở thẳng trang Sửa'], '—',
      ['- Bước 1: dòng H-1 có Sửa, Xóa', '- Bước 3: không còn nút; mở thẳng trang Sửa báo "' + GD + '"']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'THÊM KHAI BÁO — CHỌN HÀNG & VỊ TRÍ', S4),
    ('V', 'SỬA THEO NHÓM', S5),
    ('VI', 'XÓA THEO NHÓM', S6),
    ('VII', 'IMPORT EXCEL', S7),
    ('VIII', 'XUẤT EXCEL', S8),
    ('IX', 'TÁC ĐỘNG SỐ LIỆU & RÀNG BUỘC', S9),
    ('X', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S10),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + L.NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
    print('Tổng số case (viết mới): %d' % COUNT[0])
