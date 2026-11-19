# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu nhập kho" (STT 178, Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng; Kho > Nhập kho).

Chưa có TC cũ → viết mới theo code HRM develop (02/11/2026), khuôn form 17 cột (tc_engine) như màn mẫu
finance-declare-debt-beginning/docs/kh/gen_testcase.py. Giọng tester, không thuật ngữ code.
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

TEN = 'Phiếu nhập kho'
MODULE = 'Phiếu nhập kho'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
COUNT = [0]


def L_(*lines):
    return '\n'.join(lines)


def T(n, func, prio, pre, steps, data, exp):
    COUNT[0] += 1

    def j(x):
        return x if isinstance(x, str) else L_(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'phân hệ Tài chính > menu Hàng hoá - Dịch vụ - Vận chuyển > nhóm Nhập hàng > "Phiếu nhập kho"'
MENU2 = 'phân hệ Kho > menu Nhập kho > "Phiếu nhập kho"'
TON = 'phân hệ Kho > Báo cáo kho > "Báo cáo tồn kho chi tiết theo mặt hàng"'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '- TK-TK: thủ kho của kho K1 (Kho Sài Gòn), không có quyền xem phiếu nhập kho nào.',
    '- TK-TK2: thủ kho khác của kho K1. TK-KT: có quyền "Kế toán kho", cùng công ty với K1. TK-KT2: "Kế toán kho" công ty khác.',
    '- TK-CTY: có "Xem phiếu nhập kho theo công ty". TK-ALL: có "Xem phiếu nhập kho theo tổng công ty". TK-Z: không quyền, không phải thủ kho.',
    '- ĐN-1: đề nghị nhập kho Chờ duyệt của kho K1, loại Nhập hàng mua trong nước (TỰ DO + HÃNG), 1 hàng H1 SL đề nghị 2 Cái.',
    '- ĐN-7: đề nghị Chờ duyệt loại Nhập điều chuyển kho chi nhánh của kho K1.',
    '- Vị trí V1, V2 thuộc kho K1 (không kiểm kê); V3 thuộc kho K1 đang trong đợt kiểm kê.',
    '- File đính kèm mẫu: 1 file pdf < 20MB; 1 file .exe; 1 file pdf > 20MB.',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Màn "Phiếu nhập kho" là chứng từ thủ kho nhập hàng VẬT LÝ vào vị trí kho, lập từ 1 đề nghị nhập kho Chờ duyệt. '
        'Luồng: Tạo phiếu (vị trí dự kiến) → Phiếu xếp hàng (chia nhóm, người đi xếp) → Nhập kho (SL, vị trí thực, file) → '
        '"Lưu và nhập" (cộng tồn kho, Chờ duyệt) → kế toán kho lập Phiếu nhập hàng (Đang hạch toán → Đã hạch toán) hoặc '
        'Không duyệt → Xuất lại (trừ tồn) → Nhập lại (phiếu mới). Hủy khi còn Đang tạo.',
        'Đường vào: ' + MENU + '; lối thứ 2: ' + MENU2 + '.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới, Phiếu xếp hàng, Nhập kho / Sửa phiếu, '
        'Xem chi tiết, Hủy, Không duyệt, Tạo phiếu nhập hàng, Tạo phiếu xuất lại, Tạo phiếu nhập lại, In phiếu, In barcode, '
        'Xuất Excel, Lịch sử.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi xem (cộng dồn):',
        '- "Xem phiếu nhập kho theo tổng công ty": mọi công ty; "… theo công ty": công ty đang làm việc; "… theo phòng ban": phòng ban được giao quản lý.',
        '- Thủ kho có quyền "Xem tất cả phiếu xuất nhập kho": phiếu của kho mình là thủ kho.',
        '- "Kế toán kho": phiếu đã gửi (khác Đang tạo) của công ty mình.',
        '- Luôn thấy phiếu do mình tạo.',
        'Cửa sổ chọn đề nghị: chỉ đề nghị Chờ duyệt của kho người dùng là thủ kho.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Phiếu Đang tạo của người khác không hiện ở danh sách (phiếu đang đi xếp hàng vẫn mở được qua liên kết).',
        '- Vị trí đang kiểm kê: mờ, ghi "Đang kiểm kho", không chọn được.',
        '- Nút trên dòng ẩn khi không đúng trạng thái / vai trò (không làm mờ).',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" (Từ – Đến) lọc theo ngày tạo phiếu, tính cả 2 đầu mút. Bộ lọc ghi nhớ 10 phút khi rời màn rồi quay lại.',
        'Ngày nhận = lúc "Lưu và nhập"; Ngày duyệt = lúc lập phiếu nhập hàng (không phải ô lọc).',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Phiếu → dòng hàng (theo đề nghị) → nhiều dòng vị trí (vị trí + SL nhập). Bước xếp hàng: mỗi dòng vị trí thuộc 1 phiếu xếp hàng có 1 người đi xếp.',
        'Trạng thái: Đang tạo (Đang đi xếp hàng / Đang nhập kho), Chờ duyệt, Đang hạch toán, Đã hạch toán, Không duyệt, Đã xuất lại, Đã nhập lại, Đã hủy.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Tổng SL các vị trí của 1 dòng ≤ SL đề nghị (điều chuyển kho chi nhánh: phải bằng); cả phiếu phải có ≥ 1 hàng SL > 0; SL ≤ 999,999.',
        '- 1 dòng hàng không chọn trùng vị trí. Chỉ "Lưu và nhập" mới cộng tồn; Xuất lại trừ toàn bộ; Không duyệt không hoàn tồn.',
    )),
    ('7. Phân quyền cấp', L_(
        '- Màn không có quyền vào riêng. 3 quyền xem nằm ở nhóm "Phiếu nhập kho" màn Phân quyền; "Kế toán kho" là quyền dùng chung kho.',
        '- Thủ kho khai ở danh mục kho (danh sách thủ kho của kho).',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N". Trang chi tiết có dòng Tổng cộng SL đề nghị, SL thực nhập, SL nhập.',
        'Tab Bốc xếp: Số tiền = Đơn giá × Khối lượng (hoặc Số giờ); Số tiền sau VAT = Số tiền × (1 + VAT%).',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '- Số theo chuẩn quốc tế: 1,234,567.89.',
        '- Kiểm tồn: sau "Lưu và nhập" / "Xuất lại" mở ' + TON + ' hoặc cột Tồn ở cửa sổ chọn vị trí.',
        '- Cột kết quả / check để trống cho tester điền.',
    )),
]

# ------------------------------------------------------------------ PHÂN QUYỀN
ROLE_TCS = [
    T('00', 'Vào màn không cần quyền riêng: thấy phiếu mình tạo', 'P0', 'TK-Z không quyền, chưa tạo phiếu nào',
      ['1. Đăng nhập TK-Z', '2. Vào ' + MENU], 'TK-Z',
      ['- Mục menu "Phiếu nhập kho" hiện ở cả 2 phân hệ', '- Danh sách trống "Không có dữ liệu phù hợp."',
       '- Không có ô Công ty / Phòng ban ở Tìm kiếm nâng cao']),
    T('01', 'Phạm vi "Xem phiếu nhập kho theo tổng công ty"', 'P0', 'TK-ALL', ['1. Đăng nhập TK-ALL, vào màn', '2. Bấm Tìm kiếm nâng cao'], '—',
      ['- Thấy phiếu mọi công ty (trừ phiếu Đang tạo của người khác)', '- Có ô Công ty và Phòng ban']),
    T('02', 'Phạm vi "Xem phiếu nhập kho theo công ty"', 'P0', 'TK-CTY', ['1. Đăng nhập TK-CTY, vào màn'], '—',
      ['- Chỉ phiếu thuộc công ty đang làm việc + phiếu mình tạo']),
    T('03', 'Phạm vi "Xem phiếu nhập kho theo phòng ban"', 'P1', 'TK-PB có quyền phòng ban, quản lý 1 phòng', ['1. Đăng nhập TK-PB, vào màn'], '—',
      ['- Chỉ phiếu thuộc phòng ban được giao quản lý + phiếu mình tạo']),
    T('04', 'Thủ kho có "Xem tất cả phiếu xuất nhập kho"', 'P1', 'TK-TK được gán thêm quyền này', ['1. Đăng nhập TK-TK, vào màn'], '—',
      ['- Thấy phiếu (đã gửi) của kho K1 do người khác tạo']),
    T('05', 'Kế toán kho thấy phiếu đã gửi của công ty', 'P0', 'TK-KT; có phiếu Chờ duyệt kho K1 do TK-TK tạo',
      ['1. Đăng nhập TK-KT, vào màn', '2. Lọc Trạng thái = Chờ duyệt'], '—',
      ['- Thấy phiếu Chờ duyệt của công ty, có nút Tạo phiếu nhập hàng, Không duyệt', '- Không thấy phiếu Đang tạo của TK-TK']),
    T('06', 'Mở liên kết phiếu ngoài phạm vi', 'P1', 'TK-Z; phiếu Chờ duyệt của người khác', ['1. Dán đường dẫn trang Chi tiết phiếu đó'], '—',
      ['- Báo "Không tìm thấy phiếu nhập kho hoặc bạn không có quyền xem." và về danh sách']),
    T('07', 'Kế toán kho công ty khác không duyệt được', 'P1', 'TK-KT2; phiếu Chờ duyệt công ty TK-KT', ['1. Đăng nhập TK-KT2, mở phiếu (nếu xem được)'], '—',
      ['- Không có nút Tạo phiếu nhập hàng / Không duyệt']),
]

# ------------------------------------------------------------------ I. HIỂN THỊ
S1 = [
    T('001', 'Vào màn qua 2 đường menu', 'P0', 'TK-ALL', ['1. Vào ' + MENU, '2. Vào ' + MENU2], '—',
      ['- Cả 2 mở cùng màn "Danh sách phiếu nhập kho"', '- Bảng 10 dòng, phiếu tạo gần nhất trên cùng, tự tải không cần bấm Tìm kiếm']),
    T('002', 'Bộ cột mặc định', 'P0', 'Chưa tuỳ chỉnh cột', ['1. Đọc tiêu đề cột trái sang phải'], '—',
      ['- STT, Mã phiếu, Loại, Nhà cung cấp, Kho nhập, Ngày tạo, Phiếu ĐNNK, Người đề nghị, Người yêu cầu, Người tạo, Trạng thái, Tiến trình, Người duyệt, Ngày nhận, Ngày duyệt, Hành động',
       '- Mã phiếu dính khi cuộn ngang']),
    T('003', 'Nhãn trạng thái và tiến trình', 'P1', 'Có phiếu ở nhiều trạng thái', ['1. Xem cột Trạng thái, Tiến trình'], '—',
      ['- Đang tạo xám, Chờ duyệt cam, Không duyệt đỏ…', '- Tiến trình: Đang đi xếp hàng / Đang nhập kho / Hoàn thành nhập kho đúng bước của phiếu']),
    T('004', 'Phiếu nhập lại hiển thị phiếu gốc', 'P2', 'Có phiếu nhập lại', ['1. Xem ô Mã phiếu của phiếu nhập lại', '2. Bấm mã phiếu gốc'], '—',
      ['- Dưới mã có dòng nghiêng "Nhập lại cho phiếu <mã gốc>"', '- Bấm mở chi tiết phiếu gốc']),
    T('005', 'Liên kết Phiếu ĐNNK', 'P2', '—', ['1. Bấm mã ở cột Phiếu ĐNNK'], '—', ['- Mở màn chi tiết Đề nghị nhập kho đúng mã']),
    T('006', 'Ô rỗng để trống', 'P2', 'Phiếu không có nhà cung cấp / chưa duyệt', ['1. Xem các cột'], '—',
      ['- Nhà cung cấp, Người duyệt, Ngày nhận, Ngày duyệt để TRỐNG, không in dấu gạch']),
]

# ------------------------------------------------------------------ II. LỌC
S2 = [
    T('001', 'Tìm nhanh theo mã phiếu', 'P0', '—', ['1. Gõ "PNK-1159" vào ô "Tìm theo Mã phiếu"', '2. Nhấn Enter'], 'PNK-1159',
      ['- Chỉ phiếu có mã chứa chuỗi; về trang 1', '- Chưa nhấn Enter thì chưa lọc']),
    T('002', 'Lọc Kho nhập, Loại, Trạng thái', 'P0', '—', ['1. Tìm kiếm nâng cao', '2. Chọn Kho nhập = K1', '3. Chọn Loại', '4. Chọn Trạng thái = Chờ duyệt'], '—',
      ['- Mỗi lần chọn bảng lọc ngay', '- Kết quả thoả đồng thời các điều kiện']),
    T('003', 'Lọc Hàng hoá', 'P1', 'H1 có trong ĐN-1', ['1. Nhập mã H1 ở ô Hàng hoá, Enter'], '—',
      ['- Ra phiếu có H1 ở đề nghị nguồn hoặc lô thực nhập']),
    T('004', 'Lọc Phiếu ĐNNK, Mã phiếu', 'P1', '—', ['1. Nhập 1 phần mã đề nghị ở ô Phiếu ĐNNK, Enter', '2. Làm mới, nhập 1 phần mã phiếu ở ô Mã phiếu, Enter'], '—',
      ['- Tìm gần đúng đúng cột tương ứng']),
    T('005', 'Lọc Người đề nghị / Người yêu cầu / Người tạo / Người duyệt / Nhà cung cấp', 'P1', '—', ['1. Mở từng ô chọn, chọn 1 giá trị'], '—',
      ['- Danh sách chỉ gồm người / nhà cung cấp có trong phiếu thuộc phạm vi xem', '- Kết quả khớp cột cùng tên']),
    T('006', 'Lọc Ngày tạo tính cả 2 đầu mút', 'P1', 'Có phiếu tạo ngày 28/10/2026', ['1. Chọn Ngày tạo 28/10/2026 – 28/10/2026'], '—',
      ['- Ra các phiếu tạo trong ngày 28/10/2026']),
    T('007', 'Lọc Công ty – Phòng ban', 'P2', 'TK-ALL', ['1. Chọn Công ty', '2. Chọn Phòng ban'], '—',
      ['- Phòng ban chỉ mở sau khi chọn Công ty', '- Lọc theo tổ chức của phiếu']),
    T('008', 'Làm mới', 'P1', 'Đang lọc nhiều điều kiện', ['1. Bấm Làm mới'], '—', ['- Xoá mọi ô lọc, danh sách đầy đủ']),
    T('009', 'Ghi nhớ bộ lọc', 'P2', 'Đang lọc Trạng thái = Chờ duyệt', ['1. Mở 1 phiếu', '2. Quay lại danh sách trong 10 phút'], '—',
      ['- Bộ lọc vẫn giữ']),
    T('010', 'Cài đặt bộ lọc', 'P2', '—', ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Người duyệt", kéo "Trạng thái" lên đầu, Lưu', '3. Khôi phục mặc định'], '—',
      ['- Cửa sổ có đủ 13 ô lọc', '- Áp dụng ngay, lưu theo người dùng; khôi phục về như cũ']),
]

# ------------------------------------------------------------------ III. DANH SÁCH
S3 = [
    T('001', 'Sắp xếp', 'P1', '—', ['1. Bấm tiêu đề Mã phiếu, Loại, Nhà cung cấp, Kho nhập, Ngày tạo, Ngày nhận, Ngày duyệt'], '—',
      ['- Đổi chiều tăng / giảm; cột Trạng thái không sắp xếp', '- Chuyển trang không lặp / mất dòng']),
    T('002', 'Phân trang', 'P1', '> 10 phiếu', ['1. Đổi Số dòng/trang = 20', '2. Sang trang 2'], '—',
      ['- Về trang 1 khi đổi số dòng; STT liên tục; "Hiển thị a–b / N" đúng']),
    T('003', 'Tuỳ chỉnh cột', 'P2', '—', ['1. Bấm Cấu hình cột', '2. Bỏ tích Người yêu cầu, kéo Trạng thái lên sau Mã phiếu, Lưu', '3. Tải lại trang'], '—',
      ['- "Đang chọn 15/16 cột"; bảng áp dụng ngay và giữ sau khi tải lại']),
    T('004', 'Nút trên dòng theo trạng thái (thủ kho tạo)', 'P0', 'TK-TK có phiếu Đang đi xếp hàng, Không duyệt, Đã xuất lại',
      ['1. Xem cột Hành động từng phiếu'], '—',
      ['- Đang đi xếp hàng: Nhập kho, Hủy ngoài; menu ⋮ có Phiếu xếp hàng, In phiếu, Xem lịch sử',
       '- Đang nhập kho: nhãn "Sửa phiếu", có In barcode', '- Không duyệt: Tạo phiếu xuất lại; Đã xuất lại: Tạo phiếu nhập lại']),
]

# ------------------------------------------------------------------ IV. TẠO PHIẾU
S4 = [
    T('001', 'Mở trang tạo', 'P0', 'TK-TK', ['1. Bấm Tạo mới'], '—',
      ['- Trang "Dự kiến vị trí"; góc phải "<tên> - <ngày giờ hiện tại>"', '- Bảng hàng hoá "Chưa chọn phiếu đề nghị nhập kho"; nút Lưu và tiếp tục, Lưu, Quay lại']),
    T('002', 'Cửa sổ chọn đề nghị chỉ có đề nghị Chờ duyệt kho mình', 'P0', 'TK-TK; có đề nghị Chờ duyệt kho khác',
      ['1. Bấm ô Phiếu đề nghị nhập kho'], '—',
      ['- Cửa sổ "Chọn phiếu đề nghị nhập kho", dòng phụ "Chỉ hiện đề nghị Chờ duyệt của kho bạn là thủ kho"',
       '- Chỉ đề nghị Chờ duyệt kho K1; TK-Z: "Không có đề nghị nhập kho chờ duyệt ở kho bạn phụ trách."']),
    T('003', 'Chọn đề nghị điền form', 'P0', 'ĐN-1', ['1. Bấm dòng ĐN-1'], 'ĐN-1',
      ['- Tiêu đề khối = loại đề nghị; Kho nhập, Người đề nghị, Ghi chú theo đề nghị', '- Bảng hàng có H1, SL đề nghị 2, SL nhập mặc định 2',
       '- Loại có vận chuyển thì có tab Vận chuyển']),
    T('004', 'Bỏ trống Người giao hàng', 'P0', 'Đã chọn ĐN-1, vị trí V1', ['1. Để trống Người giao hàng, bấm Lưu'], '—',
      ['- Dưới ô: "Bắt buộc phải nhập"; tab Thông tin chung tô đỏ; không lưu']),
    T('005', 'Người giao hàng / Ghi chú quá 255 ký tự', 'P2', '—', ['1. Nhập 256 ký tự, Lưu'], '256 ký tự',
      ['- "Không được vượt quá 255 ký tự"']),
    T('006', 'Lưu khi chưa chọn đề nghị', 'P1', 'Form trống', ['1. Bấm Lưu'], '—',
      ['- Báo "Phiếu phải có ít nhất 1 hàng hoá có số lượng thực nhập lớn hơn 0", không lưu']),
    T('007', 'Bỏ trống vị trí', 'P0', 'Đã chọn ĐN-1', ['1. Không chọn vị trí, nhập Người giao hàng, Lưu'], '—',
      ['- Dưới ô vị trí: "Bắt buộc phải chọn vị trí"; toast "Số lượng nhập không hợp lệ — xem ô báo đỏ ở bảng hàng hoá"']),
    T('008', 'Vị trí đang kiểm kho không chọn được', 'P1', 'V3 đang kiểm kê', ['1. Mở cửa sổ Chọn vị trí kho', '2. Bấm dòng V3'], '—',
      ['- Dòng V3 mờ, ghi "Đang kiểm kho", không chọn được']),
    T('009', 'Chọn trùng vị trí cho 1 hàng', 'P1', '—', ['1. Thêm vị trí, chọn lại V1 cho dòng thứ 2 của H1'], '—',
      ['- Báo "Vị trí đã được chọn cho hàng này"']),
    T('010', 'Chia 1 hàng ra 2 vị trí', 'P1', '—', ['1. Thêm vị trí', '2. V1 SL 1, V2 SL 1'], '—',
      ['- SL thực nhập = 2; lưu được']),
    T('011', 'Tổng SL vượt SL đề nghị', 'P0', 'SL đề nghị 2', ['1. Nhập SL 3, Lưu'], '3',
      ['- Ô SL đỏ "Vượt SL đề nghị (2)"; không tự sửa số; không lưu']),
    T('012', 'SL để trống / quá 999,999', 'P1', 'Đã chọn vị trí', ['1. Xoá SL, Lưu', '2. Nhập 1000000, Lưu'], '—',
      ['- "Bắt buộc phải nhập"', '- "Không được lớn hơn 999,999"']),
    T('013', 'Điều chuyển kho chi nhánh phải nhập đủ', 'P1', 'ĐN-7, SL đề nghị 5', ['1. Nhập SL 4, Lưu'], '4',
      ['- "SL thực nhập phải bằng SL đề nghị"; không lưu']),
    T('014', 'Áp dụng tất cả vị trí', 'P2', 'Đề nghị nhiều dòng hàng', ['1. Chọn V1 cho dòng 1', '2. Tích "Áp dụng tất cả"'], '—',
      ['- Mọi dòng hàng nhận vị trí V1']),
    T('015', 'Vận chuyển = Công ty vận chuyển bắt buộc chuyến xe', 'P1', 'Loại có vận chuyển', ['1. Tab Vận chuyển chọn Công ty vận chuyển', '2. Không chọn chuyến, Lưu'], '—',
      ['- "Bắt buộc phải chọn chuyến xe"; chọn 2 lần cùng chuyến: "Không được chọn trùng"', '- Nút "Tạo chuyến xe" mở popup tạo nhanh chuyến xe chở hàng, lưu xong chuyến được chọn sẵn']),
    T('016', 'Bốc xếp – thuê ngoài', 'P1', '—', ['1. Tab Bốc xếp chọn Loại hình thuê = Thuê ngoài', '2. Để trống Nhà cung cấp, Loại bốc xếp, Khối lượng, Lưu'], '—',
      ['- 3 ô báo "Bắt buộc phải chọn" / "Bắt buộc phải nhập"; Khối lượng 0: "Phải lớn hơn 0"']),
    T('017', 'Bốc xếp – công ty, chia tiền người nhận việc', 'P1', 'Loại hình thuê = Công ty, Số tiền 200,000',
      ['1. Thêm 2 nhân sự 100,000 và 50,000, Lưu', '2. Sửa 100,000 + 100,000, Lưu'], '—',
      ['- Bước 1: "Tổng số tiền chia cho các nhân viên phải bằng tổng số tiền bốc xếp"', '- Bước 2: lưu được',
       '- Đơn giá, Số tiền tự tính; Số tiền sau VAT = Số tiền × (1 + VAT%)']),
    T('018', 'Lưu thành công', 'P0', 'ĐN-1 đủ dữ liệu', ['1. Bấm Lưu'], '—',
      ['- Báo "Phiếu đã được lưu. Hãy tạo phiếu đi xếp hàng", về danh sách', '- Phiếu PNK-xxxxx Đang tạo / Đang đi xếp hàng, Người tạo = TK-TK',
       '- ĐN-1 chuyển Đang nhập kho; yêu cầu nhập hàng nguồn Đang nhập kho; người lập nhận thông báo', '- Tồn kho H1 CHƯA thay đổi']),
    T('019', 'Lưu và tiếp tục', 'P2', '—', ['1. Bấm Lưu và tiếp tục'], '—', ['- Lưu xong form trống để tạo tiếp']),
    T('020', 'Thông tin chưa lưu', 'P2', 'Đã nhập Người giao hàng', ['1. Bấm Quay lại', '2. Bấm Ở lại', '3. Bấm Quay lại, Thoát'], '—',
      ['- Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"', '- Ở lại giữ form; Thoát về danh sách, không lưu']),
    T('021', 'Tạo từ màn Đề nghị nhập kho', 'P1', 'ĐN-1', ['1. Ở màn Đề nghị nhập kho bấm "Tạo phiếu nhập kho"'], '—',
      ['- Mở trang Dự kiến vị trí đã chọn sẵn ĐN-1']),
    T('022', 'Hàng đang kiểm kho', 'P2', 'H1 thuộc đợt kiểm kê đang chạy ở K1', ['1. Lưu phiếu'], '—', ['- "Hàng <tên> đang kiểm kho!"; không lưu']),
]

# ------------------------------------------------------------------ V. XẾP HÀNG
S5 = [
    T('001', 'Mở Phiếu đi xếp hàng', 'P0', 'Phiếu vừa tạo', ['1. Menu ⋮ > Phiếu xếp hàng'], '—',
      ['- Trang "Phiếu đi xếp hàng: <mã>"; thông tin chung chỉ đọc; "Phiếu 1" chứa mọi dòng vị trí']),
    T('002', 'Chia nhóm và chọn người đi xếp', 'P0', 'Phiếu 2 dòng vị trí', ['1. Thêm phiếu xếp hàng', '2. Kéo 1 dòng sang Phiếu 2', '3. Chọn người đi xếp 2 phiếu', '4. Lưu phiếu xếp hàng'], '—',
      ['- Báo "Đã lưu phiếu xếp hàng"; mở lại giữ nhóm và người đi xếp', '- Danh sách người đi xếp chỉ gồm thủ kho của kho nhập']),
    T('003', 'Thiếu người đi xếp', 'P0', '—', ['1. Bỏ trống người đi xếp Phiếu 2, Lưu phiếu xếp hàng'], '—',
      ['- "Bắt buộc phải chọn người đi xếp"']),
    T('004', 'Nhập kho khi chưa xếp xong', 'P1', 'Còn phiếu chưa có người đi xếp', ['1. Bấm Nhập kho ở trang xếp hàng'], '—',
      ['- "Còn dòng hàng chưa có người đi xếp — chọn người đi xếp cho mọi phiếu.", ở lại']),
    T('005', 'In phiếu xếp hàng', 'P2', 'Phiếu 1 có dòng + người đi xếp', ['1. Bấm In ở Phiếu 1'], '—',
      ['- Nhóm được lưu, mở "Xem trước phiếu xếp hàng 1 — <mã>"']),
    T('006', 'Bỏ phiếu trống', 'P2', '2 phiếu, Phiếu 2 không còn dòng', ['1. Bấm thùng rác ở Phiếu 2'], '—', ['- Phiếu 2 bị bỏ; nút chỉ hiện ở phiếu trống']),
]

# ------------------------------------------------------------------ VI. NHẬP KHO
S6 = [
    T('001', 'Mở trang Nhập kho', 'P0', 'Đã xếp xong', ['1. Bấm Nhập kho ở dòng phiếu'], '—',
      ['- Trang "Phiếu nhập kho: <mã>"; có khối File đính kèm (*); nút In dự kiến, Lưu, Lưu và nhập, Quay lại', '- Không có "Áp dụng tất cả"']),
    T('002', 'Lưu thiếu file', 'P0', 'Phiếu chưa có file', ['1. Bấm Lưu'], '—', ['- "Bắt buộc phải chọn file đính kèm"']),
    T('003', 'File sai định dạng / quá 20MB', 'P1', '—', ['1. Thêm tài liệu file .exe', '2. Thêm file pdf > 20MB'], '—',
      ['- "Chỉ nhận file pdf, jpeg, jpg, png, doc, csv, xlsx, xls, docx"', '- "Dung lượng tối đa 20MB"']),
    T('004', 'Vị trí chỉ bắt buộc khi SL > 0', 'P1', '—', ['1. Thêm vị trí, để SL 0 không chọn vị trí', '2. Lưu'], '—', ['- Lưu được; dòng SL > 0 không vị trí thì báo "Bắt buộc phải chọn vị trí"']),
    T('005', 'Vận chuyển công ty ở bước nhập kho', 'P1', 'Công ty vận chuyển, km dự kiến 50', ['1. Để trống Tuyến đường, Số km chốt, Lưu', '2. Nhập km chốt 60, không ghi chú, Lưu'], '—',
      ['- "Bắt buộc phải chọn" / "Bắt buộc phải nhập"', '- "Số km chốt khác số km dự kiến — bắt buộc nhập ghi chú vận chuyển"']),
    T('006', 'Lưu (chưa nhập kho)', 'P0', 'Đủ dữ liệu', ['1. Bấm Lưu'], '—',
      ['- "Phiếu đã được lưu. Bạn cần gửi để phiếu được xử lý"; Đang tạo / Đang nhập kho', '- Nút đổi thành "Sửa phiếu"; tồn kho chưa đổi']),
    T('007', 'Lưu và nhập: cộng tồn, Chờ duyệt', 'P0', 'Ghi tồn H1 tại V1 trước khi làm', ['1. Bấm Lưu và nhập', '2. Xem tồn H1 tại V1'], '—',
      ['- "Phiếu đã được gửi", về danh sách; Chờ duyệt, Hoàn thành nhập kho, có Ngày nhận',
       '- Tồn H1 tại V1 tăng đúng SL nhập (quy đổi ĐVT)', '- ĐN-1 Đã nhập kho; yêu cầu nhập hàng Đã nhập kho; kế toán kho của kho nhận thông báo']),
    T('008', 'Lưu và nhập khi chuyến xe chưa duyệt', 'P1', 'Công ty vận chuyển, chuyến chưa duyệt', ['1. Bấm Lưu và nhập'], '—',
      ['- "Chuyến xe chưa được duyệt — duyệt chuyến xe trước khi gửi."; tồn không đổi']),
    T('009', 'Chuyến đã duyệt không gỡ được', 'P2', 'Phiếu có chuyến đã duyệt', ['1. Mở Sửa phiếu, tab Vận chuyển'], '—', ['- Ô chuyến đã duyệt bị khoá, không có nút xoá']),
    T('010', 'Người khác không nhập kho được', 'P1', 'TK-TK2 mở liên kết trang Nhập kho phiếu của TK-TK', ['1. Mở đường dẫn'], '—',
      ['- "Phiếu không sửa được hoặc bạn không có quyền.", về danh sách']),
    T('011', 'In dự kiến', 'P2', '—', ['1. Bấm In dự kiến'], '—', ['- Mở "Xem trước phiếu nhập kho <mã>" với dữ liệu đã lưu']),
]

# ------------------------------------------------------------------ VII. CHI TIẾT, HỦY, KHÔNG DUYỆT
S7 = [
    T('001', 'Xem chi tiết', 'P0', 'Phiếu Chờ duyệt', ['1. Bấm mã phiếu'], '—',
      ['- Tiêu đề "Chi tiết phiếu nhập kho: <mã>" + nhãn Chờ duyệt', '- Tab Thông tin chung, Bốc xếp (Vận chuyển nếu công ty vận chuyển); file đính kèm; bảng hàng có Tổng cộng',
       '- Thanh nút giống cột Hành động']),
    T('002', 'Chi tiết phiếu đang xếp hàng', 'P2', 'Phiếu Đang đi xếp hàng', ['1. Mở chi tiết'], '—', ['- Bảng có cột Nhóm, Người đi xếp']),
    T('003', 'Hủy phiếu', 'P0', 'Phiếu Đang tạo của TK-TK', ['1. Bấm Hủy', '2. Bấm Hủy phiếu'], '—',
      ['- Hộp "Xác nhận hủy": "Phiếu <mã> sẽ bị hủy, đề nghị nhập kho nguồn cũng bị hủy theo."', '- "Đã hủy phiếu nhập kho"; phiếu Đã hủy; ĐN nguồn bị hủy',
       '- Lịch sử: Thay đổi trạng thái Đang tạo → Đã hủy']),
    T('004', 'Đóng hộp hủy', 'P2', '—', ['1. Bấm Hủy rồi Đóng'], '—', ['- Không thay đổi']),
    T('005', 'Loại điều chuyển không có nút Hủy', 'P2', 'Phiếu Đang tạo loại Nhập điều chuyển kho chi nhánh', ['1. Xem nút'], '—', ['- Không có Hủy']),
    T('006', 'Không duyệt bắt buộc lý do', 'P0', 'TK-KT, phiếu Chờ duyệt', ['1. Bấm Không duyệt', '2. Để trống lý do, bấm Không duyệt'], '—',
      ['- "Vui lòng nhập lý do không duyệt."; hộp vẫn mở']),
    T('007', 'Không duyệt thành công', 'P0', 'TK-KT', ['1. Nhập lý do "sai số lượng", bấm Không duyệt', '2. Kiểm tồn H1'], '—',
      ['- "Đã không duyệt phiếu nhập kho"; phiếu Không duyệt; chi tiết có "Lý do không duyệt"', '- Người tạo nhận thông báo; tồn H1 KHÔNG giảm']),
    T('008', 'Lý do quá 255 ký tự', 'P2', '—', ['1. Nhập 256 ký tự, Không duyệt'], '—', ['- "Không được vượt quá 255 ký tự"']),
]

# ------------------------------------------------------------------ VIII. PHIẾU NHẬP HÀNG, XUẤT LẠI, NHẬP LẠI
S8 = [
    T('001', 'Tạo phiếu nhập hàng', 'P0', 'TK-KT, phiếu Chờ duyệt', ['1. Bấm Tạo phiếu nhập hàng', '2. Lưu phiếu nhập hàng'], '—',
      ['- Mở Thêm phiếu nhập hàng, ô Chọn phiếu nhập kho = mã phiếu', '- Sau khi lưu: phiếu nhập kho Đang hạch toán, có Người duyệt, Ngày duyệt; hết nút Không duyệt']),
    T('002', 'Phiếu nhập hàng hoàn thành', 'P1', 'Tiếp TC_08.001', ['1. Hoàn thành phiếu nhập hàng'], '—', ['- Phiếu nhập kho Đã hạch toán']),
    T('003', 'Tạo phiếu xuất lại', 'P0', 'Phiếu Không duyệt của TK-TK; ghi tồn trước', ['1. Bấm Tạo phiếu xuất lại', '2. Nhập ghi chú, bấm Xuất lại', '3. Bấm Xuất lại trong hộp xác nhận'], '—',
      ['- Trang "Tạo phiếu xuất lại" hiện Lý do không duyệt và toàn bộ hàng', '- Hộp "Xác nhận xuất lại": "Toàn bộ hàng của phiếu <mã> sẽ bị trừ khỏi tồn kho. Thao tác không hoàn tác được."',
       '- "Hàng đã được xuất lại"; phiếu Đã xuất lại; tồn trở về như trước khi nhập; có phiếu PXL-xxxxx ở màn Phiếu xuất điều chỉnh sai số liệu']),
    T('004', 'Xuất lại khi không đủ tồn', 'P1', 'Hàng của phiếu đã bị xuất bớt khỏi V1', ['1. Xuất lại'], '—',
      ['- "Hàng <tên> không đủ tồn tại vị trí <mã>. Cần x, còn y"; không trừ lô nào']),
    T('005', 'Tạo phiếu nhập lại', 'P0', 'Phiếu Đã xuất lại', ['1. Bấm Tạo phiếu nhập lại', '2. Chọn file, vị trí, bấm Lưu và nhập'], '—',
      ['- Trang "Tạo phiếu nhập lại": Người giao hàng khoá, file trống', '- Sinh phiếu mới "Nhập lại cho phiếu <mã gốc>" Chờ duyệt, tồn cộng lại',
       '- Phiếu gốc Đã nhập lại; lịch sử "Tạo phiếu nhập lại <mã mới>"']),
    T('006', 'Người khác không xuất lại / nhập lại được', 'P2', 'TK-TK2 với phiếu của TK-TK', ['1. Xem nút'], '—', ['- Không có nút Tạo phiếu xuất lại / nhập lại']),
]

# ------------------------------------------------------------------ IX. IN / XUẤT / LỊCH SỬ
S9 = [
    T('001', 'In phiếu nhập kho', 'P0', 'Phiếu Chờ duyệt', ['1. Bấm In phiếu', '2. Bấm In'], '—',
      ['- Cửa sổ "Xem trước phiếu nhập kho <mã>": tiêu đề công ty, "PHIẾU NHẬP KHO", No: <mã>, bảng hàng × vị trí, khối ký', '- Bấm In mở hộp in']),
    T('002', 'In barcode', 'P2', 'Phiếu đã nhập kho', ['1. Bấm In barcode', '2. Chọn khổ giấy, bấm In barcode'], '—',
      ['- Trang có Nhà cung cấp, Năm sản xuất, Khổ giấy và bảng lô', '- Xem trước tem; phiếu chưa nhập kho không có nút In barcode']),
    T('003', 'Xuất Excel', 'P0', 'Đang lọc Trạng thái = Chờ duyệt', ['1. Bấm Xuất Excel', '2. Bỏ tích Người duyệt, kéo Trạng thái lên đầu, Xuất file'], '—',
      ['- Cửa sổ "Chọn trường xuất Excel" tích sẵn 14 trường; "Đang chọn 13/14 trường"', '- File danh_sach_phieu_nhap_kho.xlsx, tiêu đề "DANH SÁCH PHIẾU NHẬP KHO", đúng các dòng khớp lọc (mọi trang), đúng thứ tự cột',
       '- Báo "Xuất Excel thành công"']),
    T('004', 'Lịch sử từ danh sách', 'P1', 'Phiếu đã đi hết Tạo → Lưu và nhập → Không duyệt → Xuất lại', ['1. Menu ⋮ > Xem lịch sử'], '—',
      ['- "Lịch sử thay đổi: <mã>" mới nhất trên cùng: Thay đổi trạng thái (Không duyệt → Đã xuất lại, ghi chú Tạo phiếu xuất lại PXL-…), (Chờ duyệt → Không duyệt, lý do), (Đang tạo → Chờ duyệt), Thay đổi thông tin (file), Tạo mới',
       '- Người thực hiện "<họ tên> — <phòng ban>"']),
    T('005', 'Lịch sử ở trang chi tiết', 'P2', '—', ['1. Mở chi tiết, mở khối Lịch sử', '2. Bộ lọc theo loại hành động'], '—', ['- Hiện đủ mốc, lọc được']),
]

# ------------------------------------------------------------------ X. LUỒNG ĐẦU CUỐI
S10 = [
    T('001', 'Luồng chính đến Đã hạch toán', 'P0', 'ĐN-1 Chờ duyệt',
      ['1. TK-TK tạo phiếu', '2. Lập phiếu xếp hàng', '3. Nhập kho, Lưu và nhập', '4. TK-KT tạo phiếu nhập hàng, hoàn thành'], '—',
      ['- Trạng thái lần lượt: Đang tạo (Đang đi xếp hàng → Đang nhập kho) → Chờ duyệt → Đang hạch toán → Đã hạch toán',
       '- ĐN-1: Đang nhập kho → Đã nhập kho → …; tồn cộng đúng 1 lần ở bước 3']),
    T('002', 'Luồng Không duyệt → Xuất lại → Nhập lại', 'P0', 'Phiếu Chờ duyệt',
      ['1. TK-KT Không duyệt', '2. TK-TK Xuất lại', '3. TK-TK Nhập lại, Lưu và nhập', '4. TK-KT tạo phiếu nhập hàng cho phiếu mới'], '—',
      ['- Tồn: giữ nguyên ở bước 1, về như cũ ở bước 2, cộng lại ở bước 3', '- Phiếu gốc Đã nhập lại; phiếu mới đi tiếp luồng chính']),
    T('003', 'Đồng thời: 2 thủ kho cùng tạo từ 1 đề nghị', 'P1', 'TK-TK và TK-TK2 cùng mở ĐN-1',
      ['1. TK-TK Lưu', '2. TK-TK2 Lưu'], '—',
      ['- TK-TK2 bị chặn: "Chỉ thủ kho của kho nhập mới tạo được phiếu nhập kho từ đề nghị đang chờ duyệt." (đề nghị đã hết Chờ duyệt)']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP, CỘT & NÚT THEO TRẠNG THÁI', S3),
    ('IV', 'TẠO PHIẾU — DỰ KIẾN VỊ TRÍ', S4),
    ('V', 'PHIẾU ĐI XẾP HÀNG', S5),
    ('VI', 'NHẬP KHO — LƯU / LƯU VÀ NHẬP (TỒN KHO)', S6),
    ('VII', 'XEM CHI TIẾT, HỦY, KHÔNG DUYỆT', S7),
    ('VIII', 'PHIẾU NHẬP HÀNG, XUẤT LẠI, NHẬP LẠI', S8),
    ('IX', 'IN, XUẤT EXCEL, LỊCH SỬ', S9),
    ('X', 'LUỒNG ĐẦU CUỐI & ĐỒNG THỜI', S10),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + L.NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
    print('Tổng số case (viết mới, không có TC cũ): %d (phân quyền %d)' % (COUNT[0], len(ROLE_TCS)))
