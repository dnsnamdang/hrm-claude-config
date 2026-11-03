# -*- coding: utf-8 -*-
"""Testcase màn "Yêu cầu mua dịch vụ" (STT 63, phân hệ Bán hàng > Yêu cầu > Mua dịch vụ) — form 17 cột (tc_engine).
Chưa có TC cũ -> viết mới toàn bộ theo code HRM develop (02/11/2026). Khuôn: finance-declare-debt-beginning/docs/kh/gen_testcase.py.
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

TEN = 'Yêu cầu mua dịch vụ'
MODULE = 'Yêu cầu mua dịch vụ'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
COUNT = [0]


def L_(*lines):
    return '\n'.join(lines)


def T(n, func, prio, pre, steps, data, exp):
    COUNT[0] += 1

    def j(x):
        return x if isinstance(x, str) else L_(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'phân hệ Bán hàng > menu Yêu cầu > nhóm Mua dịch vụ > "Yêu cầu mua dịch vụ"'
QTP = '"Trưởng phòng duyệt yêu cầu mua dịch vụ"'
QKS = '"Ban kiểm soát duyệt giá mua dịch vụ"'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '- NV-A: nhân viên công ty TPE, phòng P1, KHÔNG có quyền riêng của màn (người lập).',
    '- NV-B: nhân viên khác cùng công ty TPE, phòng P2, không có quyền riêng.',
    '- TP-1: có quyền ' + QTP + ', công ty TPE. KS-1: có quyền ' + QKS + ', công ty TPE. KS-2: quyền KS nhưng công ty khác.',
    '- XEM-ALL / XEM-CTY / XEM-PB: lần lượt có "Xem yêu cầu mua dịch vụ - theo tổng công ty" / "- theo công ty" / "- theo phòng ban" (quản lý phòng P1).',
    '- Phiếu P-NHAP: NV-A lập, Lưu nháp. Phiếu P-DUYET: NV-A lập, đã qua TP-1 và KS-1 (Đã duyệt).',
    '- Mã phí dịch vụ: "Chi phí vận chuyển máy móc", "Chi phí lắp đặt ống gió phòng sơn"; file báo giá bao-gia.pdf (< 10 MB).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Nhân viên lập phiếu đề nghị mua dịch vụ thuê ngoài (Ghi chú, file báo giá, các dòng dịch vụ + VAT). Phiếu duyệt 2 nấc: '
        'Trưởng phòng duyệt nội dung -> Ban kiểm soát duyệt giá -> Đã duyệt, làm căn cứ lập Hợp đồng mua dịch vụ.',
        'Đường vào: ' + MENU + '. Mục menu không gắn quyền: mọi nhân viên vào được.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới (Lưu nháp / Gửi duyệt / Lưu và tiếp tục), '
        'Sửa, Xem chi tiết, Xóa, Trưởng phòng duyệt, Kiểm soát duyệt giá, Từ chối, Yêu cầu duyệt lại giá, Hủy yêu cầu, '
        'Lập hợp đồng mua dịch vụ (mở tab ngoài), In phiếu, In danh sách, Xuất Excel, Lịch sử.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi danh sách (xét lần lượt): theo tổng công ty (hoặc Super admin) -> mọi phiếu; theo công ty -> phiếu công ty mình; '
        'theo phòng ban -> phiếu phòng mình quản lý + phòng mình đang ngồi; không quyền nào -> phiếu mình lập.',
        'Người có quyền TP / KS mở được Chi tiết mọi phiếu (trừ Đang tạo) cùng công ty (qua thông báo).',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Phiếu Đang tạo của người khác: không ai thấy (kể cả Super admin).',
        '- Nút không dùng được thì ẨN, không làm mờ.',
        '- Tên dịch vụ: chỉ mã phí loại "Dịch vụ sửa chữa & chi phí khác" đang hoạt động; Nhà cung cấp: chỉ NCC đang hoạt động.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô "Ngày tạo" (Từ – Đến) lọc theo ngày tạo phiếu, tính trọn 2 ngày đầu mút. Bộ lọc ghi nhớ 10 phút khi rời màn rồi quay lại.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Phiếu: Số phiếu <mã cty>.YCMDV.<năm><6 số>, Ghi chú, File đính kèm, VAT (%), công ty / phòng ban của người lập, '
        'Ý kiến Trưởng phòng, Ý kiến Ban kiểm soát, Ngày nhận đơn (TP duyệt), Người / Ngày duyệt giá (KS).',
        'Dòng dịch vụ: Tên dịch vụ, ĐVT "Gói", Số lượng, Giá đề xuất, Thành tiền đề xuất, Giá duyệt, Thành tiền duyệt, Nhà cung cấp.',
        'Trạng thái: Đang tạo -> Chờ TP duyệt -> Chờ KS duyệt -> Đã duyệt -> (Đang lập / Đã lập hợp đồng); nhánh Không duyệt, Hủy, Xóa.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Thành tiền đề xuất = SL × Giá đề xuất; Thành tiền = tổng dòng; VAT = Thành tiền × VAT%; Tổng thanh toán = Thành tiền + VAT.',
        '- Tương tự cho cột duyệt (Giá duyệt). Hệ thống tự tính lại khi lưu / khi KS duyệt giá.',
    )),
    ('7. Phân quyền cấp', L_(
        '- Không quyền riêng: lập phiếu, thao tác trên phiếu mình lập (Sửa / Xóa khi Đang tạo, Không duyệt; Duyệt lại giá / Hủy / Lập hợp đồng khi Đã duyệt).',
        '- ' + QTP + ': duyệt / từ chối phiếu Chờ TP duyệt (không giới hạn phòng ban).',
        '- ' + QKS + ': duyệt giá / từ chối phiếu Chờ KS duyệt CÙNG CÔNG TY.',
        '- 3 quyền xem: theo tổng công ty / công ty / phòng ban (mục 2).',
    )),
    ('8. Cách tính các ô thống kê', 'Chân bảng "Hiển thị a–b / N": N = tổng phiếu khớp bộ lọc + phạm vi.'),
    ('9. Ghi chú đọc bảng', L_(
        '- Số theo chuẩn quốc tế 1,234,567.89; ô rỗng để trống.',
        '- Ngày giờ dd/mm/yyyy hh:mm.',
        '- Thông báo hệ thống ghi nguyên văn trong cột Kết quả mong đợi.',
        '- Cột kết quả / check để trống cho tester điền.',
    )),
]

# ------------------------------------------------------------------ PHÂN QUYỀN + PHẠM VI
ROLE_TCS = [
    T('00', 'Nhân viên không quyền riêng vào được màn và lập phiếu', 'P0', 'NV-A không có quyền riêng của màn',
      ['1. Đăng nhập NV-A', '2. Vào ' + MENU], 'NV-A',
      ['- Màn hiện, tiêu đề "Yêu cầu mua dịch vụ"', '- Có Tạo mới, Xuất Excel, In danh sách, Cấu hình cột hiển thị',
       '- Chỉ thấy phiếu do NV-A lập']),
    T('01', 'Phạm vi "Xem yêu cầu mua dịch vụ - theo tổng công ty"', 'P0', 'XEM-ALL',
      ['1. Đăng nhập XEM-ALL, vào màn', '2. Bấm Tìm kiếm nâng cao'], '—',
      ['- Thấy phiếu của mọi công ty (trừ phiếu Đang tạo của người khác)', '- Khu vực lọc có ô Công ty, Phòng ban']),
    T('02', 'Phạm vi "theo công ty"', 'P0', 'XEM-CTY công ty TPE',
      ['1. Đăng nhập XEM-CTY, vào màn'], '—',
      ['- Chỉ phiếu có Công ty = TPE', '- Không có phiếu Đang tạo của người khác']),
    T('03', 'Phạm vi "theo phòng ban"', 'P1', 'XEM-PB quản lý P1, đang ngồi phòng P3',
      ['1. Đăng nhập XEM-PB, vào màn'], '—',
      ['- Thấy phiếu phòng P1 (quản lý) và phòng P3 (đang ngồi)', '- Không thấy phiếu phòng khác']),
    T('04', 'Phiếu nháp chỉ người lập thấy', 'P0', 'P-NHAP do NV-A lập (Đang tạo)',
      ['1. Đăng nhập XEM-ALL / Super admin, tìm số phiếu P-NHAP', '2. Dán đường dẫn trang Chi tiết P-NHAP'], '—',
      ['- Không có trong danh sách', '- Mở trực tiếp: không xem được (báo "Bạn không có quyền xem phiếu này")']),
    T('05', 'Người không thuộc phạm vi không xem được phiếu', 'P1', 'NV-B không quyền; P-DUYET của NV-A',
      ['1. Đăng nhập NV-B', '2. Dán đường dẫn trang Chi tiết P-DUYET'], '—',
      ['- Không xem được phiếu, không lộ dữ liệu']),
    T('06', 'Người có quyền duyệt xem được phiếu cùng công ty qua thông báo', 'P1', 'TP-1 không có quyền xem; NV-A gửi duyệt phiếu',
      ['1. Đăng nhập TP-1, bấm thông báo "[YCMDV] Chờ duyệt"', '2. Quay về danh sách'], '—',
      ['- Mở được trang Chi tiết phiếu, có nút Trưởng phòng duyệt, Từ chối',
       '- Danh sách (mục menu) chỉ hiện phiếu TP-1 lập (không có quyền xem)']),
    T('07', 'Ban kiểm soát khác công ty không duyệt được', 'P1', 'Phiếu Chờ KS duyệt của TPE; KS-2 công ty khác',
      ['1. Đăng nhập KS-2, mở phiếu (nếu xem được qua quyền xem)'], '—',
      ['- Không có nút Kiểm soát duyệt giá, Từ chối']),
    T('08', 'Nút của người lập không hiện với người khác', 'P0', 'P-DUYET; đăng nhập XEM-ALL',
      ['1. Mở P-DUYET', '2. Xem cột Hành động và chân trang'], '—',
      ['- Không có Yêu cầu duyệt lại giá, Hủy yêu cầu, Lập hợp đồng mua dịch vụ', '- Chỉ có In phiếu, Lịch sử / Quay lại']),
]

# ------------------------------------------------------------------ I. HIỂN THỊ
S1 = [
    T('001', 'Vào màn qua menu', 'P0', 'NV-A', ['1. Vào ' + MENU], '—',
      ['- Tiêu đề trang và bảng "Yêu cầu mua dịch vụ"', '- Bảng 10 dòng, phiếu mới tạo nhất đứng đầu, tự tải']),
    T('002', 'Bộ cột mặc định', 'P0', 'Tài khoản chưa tùy chỉnh cột', ['1. Đọc tiêu đề cột từ trái sang phải'], '—',
      ['- STT, Số phiếu, Ngày tạo, Ngày nhận đơn, Ngày duyệt giá, Người yêu cầu, Phòng yêu cầu, Người duyệt giá, Công ty, Ghi chú, '
       'Ý kiến Trưởng phòng, Ý kiến Ban kiểm soát, Người cập nhật, Ngày cập nhật, Trạng thái, Hành động']),
    T('003', 'Màu nhãn trạng thái', 'P1', 'Có phiếu ở nhiều trạng thái', ['1. Lọc lần lượt từng trạng thái'], '—',
      ['- Đang tạo xám; Chờ TP duyệt, Chờ KS duyệt, Đang lập hợp đồng vàng; Đã duyệt, Đã lập hợp đồng xanh; Không duyệt, Hủy đỏ']),
    T('004', 'Số phiếu là liên kết', 'P1', 'Có P-DUYET', ['1. Bấm Số phiếu', '2. Quay lại, chuột phải vào Số phiếu'], '—',
      ['- Mở "Chi tiết yêu cầu mua dịch vụ: <số phiếu>"', '- Chuột phải có "Mở liên kết trong tab mới"']),
    T('005', 'Định dạng ngày, người, ô trống', 'P1', 'Có phiếu Chờ TP duyệt và phiếu Đã duyệt', ['1. Đọc các cột ngày, người'], '—',
      ['- Ngày dd/mm/yyyy hh:mm', '- Người yêu cầu, Người cập nhật dạng "Họ tên - Mã phòng ban"',
       '- Phiếu chưa TP duyệt: Ngày nhận đơn trống; chưa KS duyệt: Ngày duyệt giá, Người duyệt giá trống (không in "-")']),
    T('006', 'Nút cột Hành động theo trạng thái', 'P0', 'NV-A có P-NHAP và P-DUYET',
      ['1. Đăng nhập NV-A', '2. Xem cột Hành động 2 phiếu'], '—',
      ['- P-NHAP: Sửa, Xóa, menu "…" có In phiếu, Lịch sử',
       '- P-DUYET: Yêu cầu duyệt lại giá, Hủy yêu cầu, menu "…" có Lập hợp đồng mua dịch vụ, In phiếu, Lịch sử',
       '- Không có nút xám bị khóa']),
    T('007', 'Nút duyệt ở danh sách mở trang Chi tiết', 'P1', 'TP-1; phiếu Chờ TP duyệt',
      ['1. Bấm "Trưởng phòng duyệt" ở cột Hành động'], '—', ['- Mở trang Chi tiết phiếu, chưa đổi trạng thái']),
]

# ------------------------------------------------------------------ II. LỌC
S2 = [
    T('001', 'Tìm nhanh theo số phiếu', 'P0', 'Biết số phiếu P-DUYET',
      ['1. Nhập số phiếu vào ô "Tìm theo số phiếu"', '2. Bấm Tìm kiếm'], 'Số phiếu P-DUYET',
      ['- Bảng chỉ còn phiếu khớp số phiếu, chân bảng "Hiển thị 1–1 / 1"']),
    T('002', 'Lọc Số phiếu (gần đúng) chỉ chạy khi Enter', 'P1', '—',
      ['1. Tìm kiếm nâng cao, gõ "YCMDV.2026" vào ô Số phiếu, chưa Enter', '2. Nhấn Enter'], '—',
      ['- Bước 1 bảng chưa đổi', '- Bước 2 chỉ còn phiếu có số chứa chuỗi đã gõ']),
    T('003', 'Lọc Tên dịch vụ', 'P1', 'Có phiếu có dòng "Chi phí vận chuyển máy móc"',
      ['1. Gõ "vận chuyển" vào ô Tên dịch vụ, Enter'], '—', ['- Chỉ phiếu có ít nhất 1 dòng dịch vụ chứa "vận chuyển"']),
    T('004', 'Lọc Trạng thái lọc ngay', 'P0', '—', ['1. Chọn Trạng thái = Đã duyệt'], '—',
      ['- Danh sách 8 lựa chọn: Đang tạo, Chờ TP duyệt, Chờ KS duyệt, Đã duyệt, Đang lập hợp đồng, Đã lập hợp đồng, Không duyệt, Hủy',
       '- Chọn xong bảng tải lại ngay, chỉ còn phiếu Đã duyệt']),
    T('005', 'Lọc Người duyệt giá, Người tạo', 'P1', '—', ['1. Chọn Người duyệt giá = KS-1', '2. Chọn thêm Người tạo = NV-A'], '—',
      ['- Kết quả thỏa đồng thời 2 điều kiện']),
    T('006', 'Lọc Ngày tạo tính trọn ngày đầu mút', 'P1', 'Có phiếu tạo lúc 17:30 ngày X',
      ['1. Chọn Ngày tạo Từ X Đến X'], 'Ngày X', ['- Phiếu tạo lúc 17:30 ngày X có trong kết quả']),
    T('007', 'Lọc Công ty / Phòng ban', 'P1', 'XEM-ALL', ['1. Chọn Công ty = TPE', '2. Chọn Phòng ban = P1'], '—',
      ['- Chỉ phiếu có công ty / phòng ban ghi trên phiếu khớp']),
    T('008', 'Làm mới và nhớ bộ lọc', 'P2', 'Đang lọc Trạng thái = Đã duyệt',
      ['1. Mở trang Chi tiết 1 phiếu rồi quay lại trong 10 phút', '2. Bấm Làm mới'], '—',
      ['- Bước 1 bộ lọc vẫn giữ', '- Bước 2 xoá mọi điều kiện, bảng đầy đủ']),
    T('009', 'Cài đặt bộ lọc', 'P2', '—', ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Tên dịch vụ", kéo "Trạng thái" lên đầu, Lưu'], '—',
      ['- Cửa sổ có 7 ô: Công ty – Phòng ban, Số phiếu, Tên dịch vụ, Trạng thái, Người duyệt giá, Người tạo, Ngày tạo',
       '- Sau Lưu: khu vực lọc đổi theo; "Khôi phục mặc định" đưa về như cũ']),
]

# ------------------------------------------------------------------ III. DANH SÁCH
S3 = [
    T('001', 'Sắp xếp Số phiếu, Ngày tạo, Ngày nhận đơn, Ngày duyệt giá', 'P1', '—',
      ['1. Bấm lần lượt tiêu đề từng cột 2 lần'], '—', ['- Mỗi lần bấm đổi chiều tăng / giảm đúng theo cột']),
    T('002', 'Sắp xếp Ngày cập nhật', 'P2', '—', ['1. Bấm tiêu đề cột Ngày cập nhật 2 lần'], '—',
      ['- Bảng sắp xếp theo Ngày cập nhật tăng / giảm']),
    T('003', 'Phân trang', 'P1', 'Hơn 10 phiếu', ['1. Chuyển trang 2', '2. Đổi 20 dòng/trang'], '—',
      ['- STT nối tiếp (11, 12…)', '- Đổi số dòng về trang 1, chân bảng cập nhật']),
    T('004', 'Tùy chỉnh cột', 'P2', '—', ['1. Bấm Cấu hình cột hiển thị', '2. Bỏ tích Công ty, Ghi chú, Lưu', '3. Tải lại trang'], '—',
      ['- STT, Số phiếu có khóa, không bỏ được', '- 2 cột ẩn và vẫn ẩn sau khi tải lại']),
]

# ------------------------------------------------------------------ IV. LẬP PHIẾU
S4 = [
    T('001', 'Mở trang Tạo', 'P0', 'NV-A', ['1. Bấm Tạo mới'], '—',
      ['- Trang "Tạo phiếu yêu cầu mua dịch vụ"; góc phải "<NV-A> - <ngày giờ hiện tại>"',
       '- Có Ghi chú *, File đính kèm *, Danh sách dịch vụ * với 1 dòng trống, VAT (%) = 0',
       '- Chân trang: Lưu nháp, Gửi duyệt, Lưu và tiếp tục, Quay lại']),
    T('002', 'Lưu nháp chỉ bắt buộc Ghi chú', 'P0', '—', ['1. Nhập Ghi chú, để trống file và dòng dịch vụ', '2. Bấm Lưu nháp'],
      'Ghi chú: "Thuê vận chuyển máy nén khí"',
      ['- Báo "Thêm mới thành công.", về danh sách', '- Phiếu mới trạng thái Đang tạo, số phiếu dạng TPE.YCMDV.<năm><6 số>',
       '- Mở chi tiết: không có dòng dịch vụ (dòng trống bị bỏ qua)']),
    T('003', 'Ghi chú bỏ trống / quá 255 ký tự', 'P0', '—', ['1. Để trống Ghi chú, bấm Lưu nháp', '2. Dán 256 ký tự'], '—',
      ['- Trống: viền đỏ "Bắt buộc phải nhập", không lưu', '- Ô không nhận quá 255 ký tự']),
    T('004', 'Gửi duyệt thiếu file / dòng dịch vụ', 'P0', '—',
      ['1. Nhập Ghi chú, không thêm file, dòng dịch vụ để trống', '2. Bấm Gửi duyệt'], '—',
      ['- File đính kèm: "Bắt buộc phải nhập"', '- Dòng 1: Tên dịch vụ, Số lượng, Giá đề xuất báo "Bắt buộc phải nhập" (nếu trống)',
       '- Cuộn tới ô lỗi đầu tiên, không lưu']),
    T('005', 'Gửi duyệt với Số lượng / Giá = 0', 'P1', '—',
      ['1. Nhập đủ Ghi chú, file, Tên dịch vụ; để Số lượng 0, Giá 0', '2. Bấm Gửi duyệt'], '—',
      ['- Hệ thống báo lỗi Số lượng / Giá đề xuất phải lớn hơn 0, không gửi duyệt phiếu 0 đồng']),
    T('006', 'File đính kèm sai định dạng / quá 10 MB', 'P1', '—',
      ['1. Bấm Thêm tài liệu, chọn file .exe', '2. Chọn file pdf 12 MB'], 'test.exe, big.pdf 12 MB',
      ['- Không nhận file, báo lỗi định dạng / dung lượng', '- Nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip tối đa 10 MB']),
    T('007', 'Tên dịch vụ chỉ mã phí dịch vụ đang hoạt động', 'P1', 'Có mã phí dịch vụ đang khóa',
      ['1. Mở ô Tên dịch vụ, gõ tên mã phí đang khóa'], '—', ['- Không có trong danh sách chọn']),
    T('008', 'Nhà cung cấp tìm theo mã / tên', 'P2', '—', ['1. Mở ô Nhà cung cấp', '2. Gõ một phần tên NCC'], '—',
      ['- Mở là thấy tối đa 50 NCC đang hoạt động, dạng "Mã - Tên"', '- Gõ thì lọc theo mã / tên; bỏ trống được']),
    T('009', 'Tính tiền tự động', 'P0', '—',
      ['1. Dòng 1: SL 2, Giá 3,500,000', '2. Thêm dòng 2: SL 1, Giá 12,000,000', '3. VAT (%) = 8'], '—',
      ['- Thành tiền đề xuất dòng 1 = 7,000,000; dòng 2 = 12,000,000 (không gõ tay được)',
       '- Thành tiền 19,000,000; VAT 1,520,000; Tổng thanh toán 20,520,000']),
    T('010', 'VAT vượt 100', 'P2', '—', ['1. Nhập VAT (%) = 120, bấm Lưu nháp'], '—', ['- Báo "Không được lớn hơn 100.", không lưu']),
    T('011', 'Gửi duyệt hợp lệ', 'P0', 'TP-1 cùng công ty',
      ['1. Nhập đủ dữ liệu như TC IV-009 + file bao-gia.pdf', '2. Bấm Gửi duyệt'], '—',
      ['- "Thêm mới thành công.", về danh sách; phiếu Chờ TP duyệt',
       '- Phiếu ghi Công ty, Phòng yêu cầu = của NV-A',
       '- TP-1 nhận thông báo "[YCMDV] Chờ duyệt: <số phiếu>" có người lập, tổng tiền; bấm mở trang Chi tiết']),
    T('012', 'Lưu và tiếp tục', 'P1', '—', ['1. Nhập Ghi chú', '2. Bấm Lưu và tiếp tục'], '—',
      ['- Lưu nháp thành công, trang Tạo mở lại trống để lập phiếu tiếp']),
    T('013', 'Quay lại khi đã nhập', 'P1', '—', ['1. Nhập Ghi chú', '2. Bấm Quay lại'], '—',
      ['- Hiện hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"',
       '- Ở lại: giữ dữ liệu; Thoát: về danh sách, không lưu']),
    T('014', 'Bấm Lưu 2 lần liên tiếp', 'P2', '—', ['1. Nhập đủ, bấm Lưu nháp 2 lần thật nhanh'], '—', ['- Chỉ tạo 1 phiếu']),
]

# ------------------------------------------------------------------ V. SỬA / CHI TIẾT / XÓA
S5 = [
    T('001', 'Sửa phiếu Đang tạo rồi gửi duyệt', 'P0', 'P-NHAP của NV-A',
      ['1. Bấm Sửa', '2. Thêm file, dòng dịch vụ, bấm Gửi duyệt'], '—',
      ['- Trang "Sửa phiếu yêu cầu mua dịch vụ: <số phiếu>", nhãn Đang tạo', '- Không có nút Lưu và tiếp tục',
       '- "Cập nhật thành công.", phiếu Chờ TP duyệt; TP-1 nhận thông báo']),
    T('002', 'Sửa phiếu Không duyệt', 'P0', 'Phiếu của NV-A bị từ chối',
      ['1. Bấm Sửa', '2. Đọc khối Thông tin chung', '3. Sửa, bấm Lưu nháp'], '—',
      ['- Hiện Ý kiến Trưởng phòng / Ban kiểm soát (lý do từ chối)', '- Sau Lưu nháp: phiếu về Đang tạo']),
    T('003', 'Không sửa được phiếu đã gửi duyệt', 'P0', 'Phiếu Chờ TP duyệt của NV-A',
      ['1. Xem cột Hành động', '2. Dán đường dẫn trang Sửa của phiếu'], '—',
      ['- Không có nút Sửa, Xóa', '- Báo "Phiếu này không sửa được", chuyển sang trang Chi tiết']),
    T('004', 'Người khác không sửa được', 'P1', 'XEM-ALL; phiếu Không duyệt của NV-A',
      ['1. Mở phiếu', '2. Dán đường dẫn trang Sửa'], '—', ['- Không có nút Sửa, Xóa', '- Không sửa được']),
    T('005', 'Sửa không mất số lượng đã lập hợp đồng', 'P2', 'Phiếu có dòng đã lập hợp đồng 1 phần rồi bị trả về sửa (nếu có dữ liệu)',
      ['1. Sửa Ghi chú, Lưu'], '—', ['- Số lượng đã lập hợp đồng của dòng giữ nguyên']),
    T('006', 'Xung đột: phiếu vừa gửi duyệt ở tab khác', 'P2', 'NV-A mở trang Sửa P-NHAP ở 2 tab',
      ['1. Tab 1 bấm Gửi duyệt', '2. Tab 2 bấm Lưu nháp'], '—', ['- Tab 2 báo ' + CONFLICT + ', không lưu']),
    T('007', 'Xem chi tiết', 'P0', 'P-DUYET', ['1. Bấm Số phiếu'], '—',
      ['- Khối Thông tin chung: Ghi chú, Ý kiến TP / KS, góc phải người tạo và ngày giờ tạo',
       '- File đính kèm (xem, tải); Danh sách dịch vụ có Giá duyệt, Thành tiền duyệt, 3 dòng tổng; khối Lịch sử']),
    T('008', 'Xóa phiếu Đang tạo', 'P0', 'P-NHAP của NV-A',
      ['1. Bấm Xóa ở cột Hành động', '2. Ở trang Chi tiết bấm Xóa', '3. Bấm Hủy, rồi bấm Xóa lần nữa và xác nhận'], '—',
      ['- Bước 1 mở trang Chi tiết', '- Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa phiếu yêu cầu mua dịch vụ \'<số phiếu>\'?"',
       '- Hủy: không đổi; Xóa: "Xóa thành công.", về danh sách, phiếu biến mất']),
    T('009', 'Xóa phiếu Không duyệt', 'P1', 'Phiếu Không duyệt của NV-A', ['1. Mở phiếu, Xóa, xác nhận'], '—', ['- Xóa thành công']),
    T('010', 'Gỡ file đã lưu khi sửa', 'P2', 'P-NHAP có 2 file', ['1. Ở trang Sửa xoá 1 file'], '—',
      ['- File biến mất khỏi phiếu; lịch sử có mốc "File đính kèm" đã xóa']),
]

# ------------------------------------------------------------------ VI. LUỒNG DUYỆT
S6 = [
    T('001', 'Trưởng phòng duyệt', 'P0', 'Phiếu Chờ TP duyệt; TP-1 không còn hàng quá hạn',
      ['1. TP-1 mở phiếu, bấm Trưởng phòng duyệt', '2. Nhập ý kiến "Đồng ý", bấm Duyệt'], '—',
      ['- Cửa sổ "Trưởng phòng duyệt yêu cầu mua dịch vụ", dòng "Phiếu: <số phiếu>", ý kiến không bắt buộc',
       '- "Duyệt thành công.", về danh sách; phiếu Chờ KS duyệt',
       '- Ngày nhận đơn = thời điểm duyệt; Ý kiến Trưởng phòng = "Đồng ý"',
       '- KS-1 nhận thông báo "[YCMDV] Chờ duyệt … Trưởng phòng đã duyệt, chờ Ban kiểm soát duyệt giá"']),
    T('002', 'Trưởng phòng duyệt bị chặn do hàng quá hạn', 'P1', 'TP-1 (hoặc nhân viên phòng TP-1 quản lý) còn hàng quá hạn theo cấu hình "Duyệt yêu cầu mua dịch vụ"',
      ['1. TP-1 bấm Trưởng phòng duyệt, Duyệt'], '—',
      ['- Không duyệt được, hiện lý do và danh sách hàng quá hạn', '- Phiếu vẫn Chờ TP duyệt']),
    T('003', 'Trưởng phòng duyệt phiếu phòng khác', 'P2', 'TP-1 quản lý P1; phiếu Chờ TP duyệt phòng P2 cùng công ty',
      ['1. TP-1 mở phiếu P2'], '—', ['- Có nút Trưởng phòng duyệt (không giới hạn phòng ban)']),
    T('004', 'Ban kiểm soát duyệt giá', 'P0', 'Phiếu Chờ KS duyệt (từ VI-001)',
      ['1. KS-1 mở phiếu, bấm Kiểm soát duyệt giá', '2. Nhập ý kiến, bấm Duyệt giá'], '—',
      ['- Cửa sổ "Ban kiểm soát duyệt giá"', '- "Duyệt thành công."; phiếu Đã duyệt; Người duyệt giá = KS-1, Ngày duyệt giá = lúc duyệt',
       '- Danh sách dịch vụ có Giá duyệt, Thành tiền duyệt và tổng duyệt đúng giá Ban kiểm soát chấp nhận (không bằng 0)']),
    T('005', 'Từ chối ở nấc Trưởng phòng', 'P0', 'Phiếu Chờ TP duyệt',
      ['1. TP-1 bấm Từ chối, để trống lý do, bấm Từ chối', '2. Nhập lý do "Thiếu báo giá", bấm Từ chối'], '—',
      ['- Bước 1: "Bắt buộc phải nhập", không gửi', '- Bước 2: "Thao tác thành công."; phiếu Không duyệt; Ý kiến Trưởng phòng = lý do',
       '- NV-A nhận thông báo "[YCMDV] Từ chối" kèm người từ chối và lý do']),
    T('006', 'Từ chối ở nấc Ban kiểm soát', 'P0', 'Phiếu Chờ KS duyệt',
      ['1. KS-1 bấm Từ chối, nhập lý do, bấm Từ chối'], '—',
      ['- Phiếu Không duyệt; lý do ghi vào Ý kiến Ban kiểm soát; người lập nhận thông báo']),
    T('007', 'Gửi duyệt lại sau khi bị từ chối', 'P0', 'Phiếu Không duyệt (VI-005)',
      ['1. NV-A sửa, bấm Gửi duyệt', '2. TP-1 mở lại phiếu'], '—', ['- Phiếu Chờ TP duyệt, TP-1 duyệt được như bình thường']),
    T('008', 'Yêu cầu duyệt lại giá', 'P0', 'P-DUYET của NV-A',
      ['1. NV-A mở P-DUYET, bấm Yêu cầu duyệt lại giá'], '—',
      ['- Thực hiện ngay, "Thao tác thành công."; phiếu về Chờ KS duyệt', '- KS-1 nhận thông báo "Xin duyệt lại giá"',
       '- KS-1 duyệt giá lại được -> Đã duyệt']),
    T('009', 'Hủy yêu cầu', 'P0', 'P-DUYET của NV-A',
      ['1. Bấm Hủy yêu cầu', '2. Nhập lý do "Không còn nhu cầu", bấm Hủy yêu cầu'], '—',
      ['- Cửa sổ "Hủy yêu cầu mua dịch vụ", lý do không bắt buộc', '- "Thao tác thành công."; phiếu Hủy, chỉ còn In phiếu, Lịch sử',
       '- Lịch sử có mốc Thay đổi trạng thái Đã duyệt -> Hủy kèm lý do']),
    T('010', 'Lập hợp đồng mua dịch vụ', 'P1', 'P-DUYET của NV-A',
      ['1. Bấm Lập hợp đồng mua dịch vụ'], '—',
      ['- Mở tab mới tới màn lập hợp đồng của phiếu; trang HRM không đổi',
       '- Sau khi lập hợp đồng một phần / đủ số lượng, phiếu hiện Đang lập hợp đồng / Đã lập hợp đồng']),
    T('011', 'Phiếu Đang lập / Đã lập hợp đồng chỉ xem', 'P1', 'Có phiếu 2 trạng thái này',
      ['1. Mở phiếu bằng người lập'], '—',
      ['- Đang lập hợp đồng: chỉ Lập hợp đồng mua dịch vụ, In phiếu', '- Đã lập hợp đồng: chỉ In phiếu, Quay lại']),
    T('012', 'Xung đột duyệt 2 người cùng lúc', 'P2', 'TP-1 và TP-2 cùng mở phiếu Chờ TP duyệt',
      ['1. TP-1 duyệt', '2. TP-2 bấm Duyệt (chưa tải lại trang)'], '—', ['- TP-2 nhận ' + CONFLICT + ', không duyệt lần 2']),
    T('013', 'Người lập không tự duyệt khi không có quyền', 'P1', 'NV-A không có quyền TP',
      ['1. NV-A mở phiếu mình vừa gửi duyệt'], '—', ['- Không có nút Trưởng phòng duyệt, Từ chối']),
]

# ------------------------------------------------------------------ VII. IN / XUẤT
S7 = [
    T('001', 'In phiếu chưa duyệt', 'P1', 'Phiếu Chờ TP duyệt', ['1. Bấm In phiếu'], '—',
      ['- Cửa sổ "Xem trước phiếu yêu cầu mua dịch vụ", tiêu đề công ty TRÊN PHIẾU',
       '- "PHIẾU YÊU CẦU MUA DỊCH VỤ", Số phiếu, Ngày lập, Ghi chú; bảng 2 cột tiền (Giá đề xuất, Thành tiền đề xuất), ĐVT "Gói"',
       '- Khối ký Ban kiểm soát, Trưởng phòng, Người lập (ô chưa duyệt để trống)']),
    T('002', 'In phiếu Đã duyệt', 'P0', 'P-DUYET', ['1. Bấm In phiếu', '2. Bấm In'], '—',
      ['- Bảng có thêm Giá duyệt, Thành tiền duyệt; 3 dòng tổng đúng số; nhãn "VAT (x%)"',
       '- Dưới Ban kiểm soát / Trưởng phòng có họ tên + "Đã duyệt"', '- Bấm In mở hộp in']),
    T('003', 'In danh sách', 'P1', 'Lọc Trạng thái = Đã duyệt', ['1. Bấm In danh sách'], '—',
      ['- "DANH SÁCH YÊU CẦU MUA DỊCH VỤ", đúng các phiếu đang lọc (mọi trang)',
       '- 9 cột: STT, Số phiếu, Ngày tạo, Ngày nhận đơn, Ngày duyệt giá, Người yêu cầu, Phòng yêu cầu, Người duyệt giá, Trạng thái']),
    T('004', 'In danh sách quá 2,000 dòng', 'P2', 'Phạm vi > 2,000 phiếu, không lọc', ['1. Bấm In danh sách'], '—',
      ['- Không in, hiện câu nhắc thu hẹp bộ lọc, không có nút In']),
    T('005', 'Xuất Excel', 'P0', 'Đang lọc Trạng thái = Đã duyệt',
      ['1. Bấm Xuất Excel', '2. Bỏ tích Công ty, kéo Trạng thái lên đầu, bấm Xuất file'], '—',
      ['- Cửa sổ "Chọn trường xuất file" 14 trường, tích sẵn cột đang hiện', '- "Xuất Excel thành công"',
       '- File danh_sach_yeu_cau_mua_dich_vu.xlsx, tiêu đề "Danh sách yêu cầu mua dịch vụ", đúng dòng đang lọc (mọi trang), đúng cột và thứ tự']),
    T('006', 'Xuất / in theo phạm vi', 'P1', 'NV-B không quyền xem', ['1. NV-B xuất Excel và in danh sách'], '—',
      ['- Chỉ có phiếu do NV-B lập']),
]

# ------------------------------------------------------------------ VIII. LỊCH SỬ
S8 = [
    T('001', 'Lịch sử đủ mốc qua cả luồng', 'P0', 'Phiếu đi hết: tạo nháp -> sửa -> gửi duyệt -> TP duyệt -> KS duyệt giá',
      ['1. Bấm Lịch sử ở cột Hành động', '2. Ở trang Chi tiết bấm Xem lịch sử'], '—',
      ['- Cửa sổ "Lịch sử thay đổi: <số phiếu>", mới nhất ở trên',
       '- Có Tạo mới; Thay đổi thông tin (Ghi chú, Thuế VAT (%), File đính kèm, Dòng dịch vụ — cũ đỏ -> mới xanh); Thay đổi trạng thái từng bước kèm ý kiến',
       '- Mỗi mốc có "Người thực hiện: <họ tên> — <phòng ban>" và thời điểm', '- Khối Lịch sử ở chi tiết hiện y hệt']),
    T('002', 'Một lần gửi duyệt không sinh 2 mốc trạng thái', 'P2', 'Sửa P-NHAP rồi Gửi duyệt',
      ['1. Xem lịch sử'], '—', ['- 1 mốc Thay đổi thông tin (không có dòng Trạng thái) + 1 mốc Thay đổi trạng thái Đang tạo -> Chờ TP duyệt']),
    T('003', 'Bộ lọc lịch sử', 'P2', 'Phiếu có từ 3 mốc', ['1. Bấm Bộ lọc, chọn loại "Thay đổi trạng thái"'], '—',
      ['- Chỉ còn các mốc đổi trạng thái']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & DANH SÁCH', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'SẮP XẾP, PHÂN TRANG & CỘT', S3),
    ('IV', 'LẬP PHIẾU — KIỂM TRA TỪNG TRƯỜNG', S4),
    ('V', 'SỬA, XEM CHI TIẾT & XÓA THEO TRẠNG THÁI', S5),
    ('VI', 'LUỒNG DUYỆT & TÁC ĐỘNG DỮ LIỆU', S6),
    ('VII', 'IN / XUẤT EXCEL', S7),
    ('VIII', 'LỊCH SỬ THAY ĐỔI', S8),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + L.NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
    print('Tổng số case (viết mới, chưa có TC cũ): %d' % COUNT[0])
