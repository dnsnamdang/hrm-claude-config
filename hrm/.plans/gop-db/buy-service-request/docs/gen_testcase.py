# -*- coding: utf-8 -*-
"""Testcase màn "Yêu cầu mua dịch vụ" (STT 63) — KHUÔN CHUẨN tab "13. DM quốc gia" (user chốt 03/11/2026), loại 'phieu'.

Bản cũ (khuôn tc_engine + nhóm TC-ROLE, sinh 02/11) giữ ở gen_testcase_v1.py để tra. Bản này giữ mọi case nghiệp vụ cũ
(đưa vào đúng nhóm chuẩn, sửa câu chữ theo giọng tab Quốc gia) và bổ sung case theo checklist "Mẫu tài liệu.xlsx"
(case chung sinh từ _tc_phieu_chung.py).
Chạy: python gen_testcase.py  (tự gọi check_tc → phải 0 lỗi)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHUAN = os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi'))
sys.path.insert(0, HERE)
sys.path.insert(0, CHUAN)
from _tc_chuan import build_chuan  # noqa: E402
from _tc_phieu_chung import C, danh_so, hien_thi, tim_kiem, them_moi_dong_form, lich_su, tuy_chinh_cot, \
    xuat_excel, phan_quyen_chung  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Yêu cầu mua dịch vụ'
MODULE = 'Yêu cầu mua dịch vụ'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
SHEET = 'Trang tính1'
NGAY = '03/11/2026'


def L_(*lines):
    return '\n'.join(lines)


MENU = 'Bán hàng > Yêu cầu > Mua dịch vụ > Yêu cầu mua dịch vụ'
QTP = '"Trưởng phòng duyệt yêu cầu mua dịch vụ"'
QKS = '"Ban kiểm soát duyệt giá mua dịch vụ"'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (ghi mã thật vào cột Ghi chú nếu môi trường test khác):',
    '-  NV-A: nhân viên công ty TPE, phòng P1, KHÔNG có quyền riêng của màn (người lập). NV-B: nhân viên khác cùng công ty, phòng P2, không quyền riêng.',
    '-  TP-1: có quyền ' + QTP + ', công ty TPE. TP-2: cũng có quyền TP. KS-1: có quyền ' + QKS + ', công ty TPE. KS-2: quyền KS nhưng công ty khác.',
    '-  XEM-ALL / XEM-CTY / XEM-PB: lần lượt có "Xem yêu cầu mua dịch vụ - theo tổng công ty" / "- theo công ty" / "- theo phòng ban" (quản lý phòng P1).',
    '-  Phiếu P-NHAP: NV-A lập, Lưu nháp. Phiếu P-DUYET: NV-A lập, đã qua TP-1 và KS-1 (Đã duyệt).',
    '-  Mã phí dịch vụ: "Chi phí vận chuyển máy móc", "Chi phí lắp đặt ống gió phòng sơn"; file báo giá bao-gia.pdf (dưới 10 MB).',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Nhân viên lập phiếu đề nghị mua dịch vụ thuê ngoài (Ghi chú, file báo giá, các dòng dịch vụ + VAT). Phiếu duyệt 2 nấc: '
        'Trưởng phòng duyệt nội dung > Ban kiểm soát duyệt giá > Đã duyệt, làm căn cứ lập Hợp đồng mua dịch vụ.',
        'Đường vào: menu ' + MENU + '. Mục menu không gắn quyền: mọi nhân viên vào được.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới (Lưu nháp / Gửi duyệt / Lưu và tiếp tục), '
        'Sửa, Xem chi tiết, Xóa, Trưởng phòng duyệt, Kiểm soát duyệt giá, Từ chối, Yêu cầu duyệt lại giá, Hủy yêu cầu, '
        'Lập hợp đồng mua dịch vụ (mở tab ngoài), In phiếu, In danh sách, Xuất Excel, Lịch sử. Không có Khóa, Import.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi danh sách (xét lần lượt): theo tổng công ty (hoặc Super admin) > mọi phiếu; theo công ty > phiếu công ty mình; '
        'theo phòng ban > phiếu phòng mình quản lý + phòng mình đang ngồi; không quyền nào > phiếu mình lập.',
        'Người có quyền TP / KS mở được Chi tiết mọi phiếu (trừ Đang tạo) cùng công ty (qua thông báo).',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Phiếu Đang tạo của người khác: không ai thấy (kể cả Super admin).',
        '-  Nút không dùng được thì ẨN, không làm mờ.',
        '-  Tên dịch vụ: chỉ mã phí loại "Dịch vụ sửa chữa & chi phí khác" đang hoạt động; Nhà cung cấp: chỉ NCC đang hoạt động.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" (Từ – Đến) lọc theo ngày tạo phiếu, tính trọn 2 ngày đầu mút.',
        'Bộ lọc được giữ khi mở trang chi tiết / sửa rồi quay lại trong 10 phút; vào màn khác qua menu thì về mặc định.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Phiếu: Số phiếu <mã cty>.YCMDV.<năm><6 số>, Ghi chú, File đính kèm, VAT (%), công ty / phòng ban của người lập, '
        'Ý kiến Trưởng phòng, Ý kiến Ban kiểm soát, Ngày nhận đơn (TP duyệt), Người / Ngày duyệt giá (KS).',
        'Dòng dịch vụ: Tên dịch vụ, ĐVT "Gói", Số lượng, Giá đề xuất, Thành tiền đề xuất, Giá duyệt, Thành tiền duyệt, Nhà cung cấp.',
        'Trạng thái: Đang tạo > Chờ TP duyệt > Chờ KS duyệt > Đã duyệt > (Đang lập / Đã lập hợp đồng); nhánh Không duyệt, Hủy, Xóa.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  Thành tiền đề xuất = SL × Giá đề xuất; Thành tiền = tổng dòng; VAT = Thành tiền × VAT%; Tổng thanh toán = Thành tiền + VAT.',
        '-  Tương tự cho cột duyệt (Giá duyệt). Hệ thống tự tính lại khi lưu / khi KS duyệt giá.',
    )),
    ('7. Phân quyền cấp', L_(
        '-  Không quyền riêng: lập phiếu, thao tác trên phiếu mình lập (Sửa / Xóa khi Đang tạo, Không duyệt; Duyệt lại giá / Hủy / '
        'Lập hợp đồng khi Đã duyệt).',
        '-  ' + QTP + ': duyệt / từ chối phiếu Chờ TP duyệt (không giới hạn phòng ban).',
        '-  ' + QKS + ': duyệt giá / từ chối phiếu Chờ KS duyệt CÙNG CÔNG TY.',
        '-  3 quyền xem: theo tổng công ty / công ty / phòng ban (mục 2).',
    )),
    ('8. Cách tính các ô thống kê', 'Chân bảng "Hiển thị a–b / N": N = tổng phiếu khớp bộ lọc + phạm vi.'),
    ('9. Ghi chú đọc bảng', L_(
        'Các bẫy dễ sai nhất của màn này, QA đọc trước khi test:',
        '-  Phiếu Đang tạo chỉ người lập thấy, kể cả Super admin cũng không thấy.',
        '-  Các nút đổi trạng thái và Xóa ở cột Hành động chỉ MỞ trang Chi tiết; thao tác thật bấm ở chân trang Chi tiết.',
        '-  Yêu cầu duyệt lại giá thực hiện NGAY, không có hộp xác nhận.',
        '-  Số theo chuẩn quốc tế 1,234,567.89; ô rỗng để trống; ngày giờ dd/mm/yyyy hh:mm. Cột KQ thực tế, DNS check để trống.',
    )),
]

K = dict(
    menu=MENU,
    tieu_de='Yêu cầu mua dịch vụ',
    pre_mo='NV-A đã đăng nhập, có phiếu do mình lập.',
    pre_nut='NV-A (không quyền riêng) đã đăng nhập.',
    exp_nut=['Thanh công cụ có: Tạo mới, Xuất Excel, In danh sách, Cấu hình cột hiển thị (mọi nhân viên đều thấy)',
             'Khối tìm kiếm có ô "Tìm theo số phiếu", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
             'Không có nút Import'],
    cot=['STT', 'Số phiếu', 'Ngày tạo', 'Ngày nhận đơn', 'Ngày duyệt giá', 'Người yêu cầu', 'Phòng yêu cầu', 'Người duyệt giá', 'Công ty',
         'Ghi chú', 'Ý kiến Trưởng phòng', 'Ý kiến Ban kiểm soát', 'Người cập nhật', 'Ngày cập nhật', 'Trạng thái', 'Hành động'],
    cot_an=[],
    exp_cot_them=['Ghi chú, Ý kiến Trưởng phòng, Ý kiến Ban kiểm soát hiện tối đa 2 dòng, rê chuột xem đủ nội dung'],
    tong_cot=16,
    cot_khoa=['STT', 'Số phiếu', 'Hành động'],
    cot_bo_thu='Công ty',
    pre_du_lieu='NV-A có phiếu Chờ TP duyệt và phiếu P-DUYET.',
    exp_du_lieu=['Số phiếu dạng TPE.YCMDV.<năm><6 chữ số>, là liên kết',
                 'Người yêu cầu, Người cập nhật dạng "Họ tên - Mã phòng ban"; Phòng yêu cầu, Công ty đúng của NV-A lúc lập',
                 'Phiếu Chờ TP duyệt: Ngày nhận đơn, Ngày duyệt giá, Người duyệt giá để TRỐNG',
                 'P-DUYET: có Ngày nhận đơn, Ngày duyệt giá, Người duyệt giá = KS-1'],
    trang_thai=[('Đang tạo', 'xám'), ('Chờ TP duyệt', 'vàng'), ('Chờ KS duyệt', 'vàng'), ('Đang lập hợp đồng', 'vàng'),
                ('Đã duyệt', 'xanh'), ('Đã lập hợp đồng', 'xanh'), ('Không duyệt', 'đỏ'), ('Hủy', 'đỏ')],
    pre_rong='NV-B chưa lập phiếu nào, không có quyền xem.',
    rong_bang='Không có dữ liệu phù hợp.',
    rong_chan='Không có phiếu nào.',
    sap_xep=['Số phiếu', 'Ngày tạo', 'Ngày nhận đơn', 'Ngày duyệt giá', 'Ngày cập nhật'],
    khong_sap_xep=['STT', 'Người yêu cầu', 'Phòng yêu cầu', 'Người duyệt giá', 'Công ty', 'Ghi chú', 'Ý kiến Trưởng phòng',
                   'Ý kiến Ban kiểm soát', 'Người cập nhật', 'Trạng thái', 'Hành động'],
    ma='Số phiếu', vd_ma='TPE.YCMDV.2026000090', vd_mot_phan='YCMDV.2026', placeholder='Tìm theo số phiếu',
    loc_text=('Tên dịch vụ', 'vận chuyển', 'van chuyen'),
    loc_list=['Công ty – Phòng ban', 'Số phiếu', 'Tên dịch vụ', 'Trạng thái', 'Người duyệt giá', 'Người tạo', 'Ngày tạo'],
    exp_mac_dinh_them=['Ô Công ty chỉ hiện với quyền xem theo tổng công ty; ô Phòng ban hiện theo phạm vi xem'],
    loc_chon=('Trạng thái', 'Đã duyệt'),
    loc_ket_hop='Trạng thái = Đã duyệt, Người duyệt giá = KS-1, Người tạo = NV-A',
    td_rong='Trạng thái: Hủy; Người tạo: người chưa hủy phiếu nào',
    form_tao='Tạo phiếu yêu cầu mua dịch vụ', nut_quay_lai='Quay lại', truong_nhap_thu='Ghi chú',
    td_nhap_thu='Ghi chú: "Thuê vận chuyển máy nén khí"', nut_luu_chinh='Lưu nháp',
    lich_su_title='Lịch sử thay đổi: <số phiếu>', nut_lich_su='Lịch sử',
    excel=dict(title='Chọn trường xuất file', so_truong=14,
               truong=['Số phiếu', 'Ngày tạo', 'Ngày nhận đơn', 'Ngày duyệt giá', 'Người yêu cầu', 'Phòng yêu cầu', 'Người duyệt giá',
                       'Trạng thái', 'Công ty', 'Ghi chú', 'Ý kiến Trưởng phòng', 'Ý kiến Ban kiểm soát', 'Người cập nhật', 'Ngày cập nhật'],
               mac_dinh='Tích sẵn các trường đang hiện trên bảng, dòng đếm "Đang chọn 14/14 trường"',
               file='danh_sach_yeu_cau_mua_dich_vu.xlsx', tieu_de='Danh sách yêu cầu mua dịch vụ', bo_thu='Công ty',
               rong=['Báo "Xuất Excel thành công"', 'File chỉ có tiêu đề và dòng tên cột, không có dòng dữ liệu']),
)

# ------------------------------------------------------------------ I. HIỂN THỊ (riêng)
K['hien_thi_rieng'] = [
    C('Nút cột Hành động theo trạng thái', 'P0', 'NV-A có P-NHAP và P-DUYET.', ['1. Đăng nhập NV-A', '2. Xem cột Hành động 2 phiếu'], '',
      ['P-NHAP: Sửa, Xóa hiện ngoài; nút ba chấm "…" có In phiếu, Lịch sử',
       'P-DUYET: Yêu cầu duyệt lại giá, Hủy yêu cầu; nút "…" có Lập hợp đồng mua dịch vụ, In phiếu, Lịch sử',
       'Không có nút xám bị khóa']),
    C('Nút duyệt ở danh sách chỉ mở trang Chi tiết', 'P1', 'TP-1; phiếu Chờ TP duyệt.', ['1. Bấm "Trưởng phòng duyệt" ở cột Hành động'], '',
      ['Mở trang Chi tiết phiếu, phiếu CHƯA đổi trạng thái', 'Thao tác duyệt thật bấm ở chân trang Chi tiết']),
    C('In phiếu, Lịch sử ở danh sách mở cửa sổ tại chỗ', 'P2', 'Có phiếu bất kỳ.', ['1. Bấm In phiếu', '2. Đóng, bấm Lịch sử'], '',
      ['Mỗi nút mở cửa sổ ngay trên danh sách, không chuyển trang']),
]

# ------------------------------------------------------------------ II. LỌC (riêng)
K['loc_rieng'] = [
    C('Lọc theo Số phiếu (gần đúng) chỉ chạy khi Enter', 'P1', 'Đang ở danh sách.',
      ['1. Tìm kiếm nâng cao, gõ "YCMDV.2026" vào ô Số phiếu, chưa Enter', '2. Nhấn Enter'], '',
      ['Bước 1 bảng chưa đổi', 'Bước 2 chỉ còn phiếu có số chứa chuỗi đã gõ']),
    C('Lọc theo Tên dịch vụ', 'P1', 'Có phiếu có dòng "Chi phí vận chuyển máy móc".', ['1. Gõ "vận chuyển" vào ô Tên dịch vụ, Enter'], '',
      ['Chỉ phiếu có ít nhất 1 dòng dịch vụ chứa "vận chuyển"']),
    C('Lọc theo Trạng thái lọc ngay', 'P0', 'Có phiếu nhiều trạng thái.', ['1. Chọn Trạng thái = Đã duyệt'], '',
      ['Danh sách 8 lựa chọn: Đang tạo, Chờ TP duyệt, Chờ KS duyệt, Đã duyệt, Đang lập hợp đồng, Đã lập hợp đồng, Không duyệt, Hủy',
       'Chọn xong bảng tải lại ngay, chỉ còn phiếu Đã duyệt']),
    C('Lọc theo Người duyệt giá, Người tạo', 'P1', 'Có phiếu KS-1 duyệt giá.', ['1. Chọn Người duyệt giá = KS-1', '2. Chọn thêm Người tạo = NV-A'], '',
      ['Kết quả thỏa đồng thời 2 điều kiện']),
    C('Lọc theo Ngày tạo tính trọn ngày đầu mút', 'P1', 'Có phiếu tạo lúc 17:30 ngày X.', ['1. Chọn Ngày tạo Từ X Đến X'], 'Ngày X',
      ['Phiếu tạo lúc 17:30 ngày X có trong kết quả']),
    C('Lọc theo Công ty, Phòng ban', 'P1', 'XEM-ALL.', ['1. Chọn Công ty = TPE', '2. Chọn Phòng ban = P1'], '',
      ['Chỉ phiếu có công ty / phòng ban ghi trên phiếu khớp']),
]

# ------------------------------------------------------------------ III. THÊM MỚI
S_THEM = [
    C('Mở trang Tạo phiếu', 'P0', 'NV-A.', ['1. Bấm Tạo mới'], '',
      ['Trang "Tạo phiếu yêu cầu mua dịch vụ"; góc phải "<NV-A> - <ngày giờ hiện tại>"',
       'Có Ghi chú *, File đính kèm *, Danh sách dịch vụ * với 1 dòng trống, VAT (%) = 0',
       'Chân trang: Lưu nháp, Gửi duyệt, Lưu và tiếp tục, Quay lại']),
    C('Trường bắt buộc và giá trị mặc định', 'P1', 'Đang ở trang Tạo.', ['1. Quan sát các ô'], '',
      ['Ghi chú bắt buộc khi mọi nút lưu; File đính kèm, dòng dịch vụ bắt buộc khi Gửi duyệt',
       'ĐVT cố định "Gói"; Số lượng, Giá đề xuất = 0; Thành tiền đề xuất = 0 không gõ tay được']),
    C('Lưu nháp với đầy đủ thông tin', 'P0', 'Đang ở trang Tạo.', ['1. Nhập Ghi chú, thêm file, 1 dòng dịch vụ đủ', '2. Bấm Lưu nháp'],
      'Ghi chú: "Thuê vận chuyển máy nén khí"',
      ['Báo "Thêm mới thành công.", về danh sách', 'Phiếu mới trạng thái Đang tạo, số phiếu dạng TPE.YCMDV.<năm><6 số>',
       'Công ty, Phòng yêu cầu = của NV-A']),
    C('Lưu nháp chỉ bắt buộc Ghi chú', 'P0', 'Đang ở trang Tạo.', ['1. Nhập Ghi chú, để trống file và dòng dịch vụ', '2. Bấm Lưu nháp'],
      'Ghi chú: "Thuê vận chuyển máy nén khí"',
      ['Báo "Thêm mới thành công."', 'Mở chi tiết: không có dòng dịch vụ (dòng chưa chọn Tên dịch vụ bị bỏ qua)']),
    C('Ghi nhận lịch sử Tạo mới', 'P1', 'Vừa Lưu nháp.', ['1. Bấm Lịch sử ở dòng phiếu'], '', ['Có mốc Tạo mới, người thực hiện NV-A, thời điểm lưu']),
    C('Ghi chú bỏ trống', 'P0', 'Đang ở trang Tạo.', ['1. Để trống Ghi chú, bấm Lưu nháp'], '',
      ['Viền đỏ, dưới ô "Bắt buộc phải nhập", cuộn tới ô lỗi, không lưu']),
    C('Ghi chú chỉ có khoảng trắng', 'P2', 'Đang ở trang Tạo.', ['1. Nhập toàn dấu cách vào Ghi chú, bấm Lưu nháp'], 'Ghi chú: "    "',
      ['Bị chặn như khi để trống']),
    C('Ghi chú đúng 255 ký tự thì lưu được', 'P1', 'Đang ở trang Tạo.', ['1. Nhập Ghi chú 255 ký tự, bấm Lưu nháp'], 'Chuỗi 255 ký tự',
      ['Lưu thành công, chi tiết hiện đủ']),
    C('Ghi chú vượt 255 ký tự', 'P1', 'Đang ở trang Tạo.', ['1. Dán chuỗi 256 ký tự vào Ghi chú'], 'Chuỗi 256 ký tự',
      ['Ô không nhận quá 255 ký tự (hoặc báo "Vui lòng nhập tối đa 255 ký tự."), không lưu']),
    C('Ghi chú có khoảng trắng đầu và cuối', 'P2', 'Đang ở trang Tạo.', ['1. Nhập Ghi chú có dấu cách 2 đầu, Lưu nháp, mở chi tiết'], 'Ghi chú: "  Thuê xe  "',
      ['Chi tiết hiện "Thuê xe" đã bỏ khoảng trắng 2 đầu']),
    C('Lỗi biến mất khi nhập lại hợp lệ', 'P1', 'Ô Ghi chú đang báo "Bắt buộc phải nhập".', ['1. Gõ Ghi chú'], '', ['Chữ đỏ biến mất ngay']),
    C('File đính kèm sai định dạng hoặc quá 10 MB', 'P1', 'Đang ở trang Tạo.', ['1. Bấm Thêm tài liệu, chọn file .exe', '2. Chọn file pdf 12 MB'], 'test.exe, big.pdf 12 MB',
      ['Không nhận file, báo lỗi định dạng / dung lượng', 'Nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip tối đa 10 MB']),
    C('Thao tác với file đã tải lên', 'P2', 'Đã thêm bao-gia.pdf.', ['1. Bấm xem, tải, thay, xóa ở dòng file'], '',
      ['Xem trước / tải được; thay đổi chọn file khác; xóa bỏ dòng file']),
    C('Tên dịch vụ chỉ mã phí dịch vụ đang hoạt động', 'P1', 'Có mã phí dịch vụ đang khóa.', ['1. Mở ô Tên dịch vụ, gõ tên mã phí đang khóa'], '',
      ['Không có trong danh sách chọn']),
    C('Nhà cung cấp tìm theo mã / tên', 'P2', 'Đang ở trang Tạo.', ['1. Mở ô Nhà cung cấp', '2. Gõ một phần tên NCC'], '',
      ['Mở là thấy tối đa 50 NCC đang hoạt động, dạng "Mã - Tên"', 'Gõ thì lọc theo mã / tên; bỏ trống được']),
    C('Thêm và xóa dòng dịch vụ', 'P1', 'Đang ở trang Tạo.', ['1. Bấm Thêm dòng 2 lần', '2. Bấm thùng rác cuối dòng 2'], '',
      ['Bảng thêm dòng trống mới', 'Dòng 2 bị bỏ, tổng tiền tính lại']),
    C('Tính tiền tự động', 'P0', 'Đang ở trang Tạo.', ['1. Dòng 1: SL 2, Giá 3,500,000', '2. Thêm dòng 2: SL 1, Giá 12,000,000', '3. VAT (%) = 8'], '',
      ['Thành tiền đề xuất dòng 1 = 7,000,000; dòng 2 = 12,000,000 (không gõ tay được)',
       'Thành tiền 19,000,000; VAT 1,520,000; Tổng thanh toán 20,520,000']),
    C('VAT vượt 100', 'P2', 'Đang ở trang Tạo.', ['1. Nhập VAT (%) = 120, bấm Lưu nháp'], 'VAT: 120', ['Báo "Không được lớn hơn 100.", không lưu']),
    C('Ô số không nhận chữ và số âm', 'P2', 'Đang ở trang Tạo.', ['1. Gõ "abc", "-5" vào Số lượng, Giá đề xuất'], '',
      ['Ô không nhận chữ, không nhận số âm; số hiển thị dạng 1,234,567.89']),
    C('Lưu và tiếp tục với dữ liệu hợp lệ', 'P1', 'Đang ở trang Tạo.', ['1. Nhập Ghi chú', '2. Bấm Lưu và tiếp tục'], '',
      ['Báo "Thêm mới thành công."; phiếu lưu Đang tạo', 'Trang Tạo mở lại trống (1 dòng dịch vụ trống) để lập tiếp']),
    C('Lưu và tiếp tục khi thiếu Ghi chú', 'P1', 'Đang ở trang Tạo, Ghi chú trống.', ['1. Bấm Lưu và tiếp tục'], '',
      ['Báo "Bắt buộc phải nhập", không lưu, ở lại form']),
    C('Lưu và tiếp tục khi VAT sai', 'P2', 'VAT = 120.', ['1. Bấm Lưu và tiếp tục'], '', ['Báo "Không được lớn hơn 100.", không lưu']),
    C('Bấm Quay lại ngay sau Lưu và tiếp tục thì không hỏi', 'P1', 'Vừa Lưu và tiếp tục, form trống.', ['1. Bấm Quay lại'], '',
      ['Về danh sách ngay, không hỏi; danh sách có phiếu vừa lưu']),
] + them_moi_dong_form(K)

# ------------------------------------------------------------------ IV. CHỈNH SỬA
S_SUA = [
    C('Mở trang Sửa phiếu Đang tạo', 'P0', 'P-NHAP của NV-A.', ['1. Bấm Sửa'], '',
      ['Trang "Sửa phiếu yêu cầu mua dịch vụ: <số phiếu>", nhãn Đang tạo cạnh "<Người tạo> - <ngày giờ tạo>"',
       'Ghi chú, file, dòng dịch vụ, VAT nạp đúng dữ liệu đã lưu', 'Không có nút Lưu và tiếp tục']),
    C('Sửa một trường', 'P0', 'P-NHAP.', ['1. Đổi Ghi chú', '2. Bấm Lưu nháp'], 'Ghi chú: "Thuê xe cẩu 5 tấn"',
      ['Báo "Cập nhật thành công.", về danh sách', 'Chi tiết hiện Ghi chú mới; vẫn Đang tạo']),
    C('Sửa nhiều trường', 'P0', 'P-NHAP.', ['1. Đổi Ghi chú, VAT, thêm 1 dòng dịch vụ', '2. Bấm Lưu nháp', '3. Xem lịch sử'], '',
      ['Lưu thành công; 3 dòng tổng tính lại', 'Lịch sử 1 mốc Thay đổi thông tin: Ghi chú, Thuế VAT (%), Dòng dịch vụ cũ > mới']),
    C('Ngày và người cập nhật đổi theo', 'P1', 'P-NHAP.', ['1. Sửa, Lưu nháp', '2. Xem cột Người cập nhật, Ngày cập nhật'], '',
      ['Người cập nhật = NV-A dạng "Họ tên - Mã phòng ban", Ngày cập nhật = lúc lưu']),
    C('Sửa phiếu Không duyệt', 'P0', 'Phiếu của NV-A bị từ chối.', ['1. Bấm Sửa', '2. Đọc khối Thông tin chung', '3. Sửa, bấm Lưu nháp'], '',
      ['Hiện Ý kiến Trưởng phòng / Ban kiểm soát (lý do từ chối)', 'Sau Lưu nháp: phiếu về Đang tạo']),
    C('Validate khi sửa', 'P0', 'P-NHAP.', ['1. Xóa Ghi chú, bấm Lưu nháp', '2. Nhập lại, đặt VAT 120, bấm Lưu nháp'], '',
      ['Bước 1: "Bắt buộc phải nhập"', 'Bước 2: "Không được lớn hơn 100."', 'Không lưu']),
    C('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Ô VAT đang báo lỗi.', ['1. Nhập VAT 10'], '', ['Chữ đỏ biến mất ngay']),
    C('Gỡ file đã lưu khi sửa', 'P2', 'P-NHAP có 2 file.', ['1. Ở trang Sửa xóa 1 file'], '',
      ['File biến mất khỏi phiếu ngay; lịch sử có mốc File đính kèm đã xóa']),
    C('Mã phí hoặc nhà cung cấp đã khóa vẫn hiện khi sửa', 'P2', 'Mã phí của dòng 1 vừa bị khóa.', ['1. Mở Sửa phiếu'], '',
      ['Ô Tên dịch vụ vẫn hiện đúng tên đã lưu']),
    C('Mở sửa không thay đổi rồi Quay lại', 'P1', 'P-NHAP.', ['1. Bấm Sửa, bấm Quay lại'], '', ['Về danh sách, không hỏi']),
    C('Sửa rồi trả về giá trị ban đầu', 'P2', 'P-NHAP.', ['1. Đổi Ghi chú rồi sửa về như cũ', '2. Bấm Quay lại'], '', ['Về danh sách, không hỏi']),
    C('Đã đổi dữ liệu rồi bấm Quay lại', 'P0', 'Đang sửa P-NHAP, đã đổi Ghi chú.', ['1. Bấm Quay lại', '2. Bấm Ở lại', '3. Bấm Quay lại, bấm Thoát'], '',
      ['Hộp "Thông tin chưa lưu" (Thoát / Ở lại)', 'Ở lại: giữ dữ liệu đang sửa', 'Thoát: về danh sách, phiếu không đổi']),
    C('Lưu nháp không đổi gì thì không ghi lịch sử', 'P1', 'P-NHAP.', ['1. Mở Sửa, bấm Lưu nháp ngay', '2. Xem lịch sử'], '',
      ['Không sinh mốc Thay đổi thông tin mới']),
    C('Không sửa được phiếu đã gửi duyệt', 'P0', 'Phiếu Chờ TP duyệt của NV-A.', ['1. Xem cột Hành động', '2. Dán đường dẫn trang Sửa của phiếu'], '',
      ['Không có nút Sửa, Xóa', 'Báo "Phiếu này không sửa được", chuyển sang trang Chi tiết']),
    C('Người khác không sửa được', 'P1', 'XEM-ALL; phiếu Không duyệt của NV-A.', ['1. Mở phiếu', '2. Dán đường dẫn trang Sửa'], '',
      ['Không có nút Sửa, Xóa', 'Không sửa được; nếu gửi lưu: "Bạn không có quyền sửa phiếu này"']),
    C('Sửa không mất số lượng đã lập hợp đồng', 'P2', 'Phiếu có dòng đã lập hợp đồng 1 phần rồi bị trả về sửa (nếu có dữ liệu).', ['1. Sửa Ghi chú, Lưu'], '',
      ['Số lượng đã lập hợp đồng của dòng giữ nguyên']),
    C('Phiếu vừa gửi duyệt ở tab khác', 'P2', 'NV-A mở trang Sửa P-NHAP ở 2 tab.', ['1. Tab 1 bấm Gửi duyệt', '2. Tab 2 bấm Lưu nháp'], '',
      ['Tab 2 báo ' + CONFLICT + ', không lưu']),
]

# ------------------------------------------------------------------ V. XÓA
S_XOA = [
    C('Nút Xóa chỉ có với người lập, phiếu Đang tạo / Không duyệt', 'P0', 'NV-A có P-NHAP, phiếu Không duyệt, P-DUYET.', ['1. Xem cột Hành động'], '',
      ['P-NHAP, phiếu Không duyệt có Xóa', 'P-DUYET không có Xóa']),
    C('Nút Xóa ở danh sách mở trang Chi tiết', 'P1', 'P-NHAP.', ['1. Bấm Xóa ở cột Hành động'], '', ['Mở trang Chi tiết, chưa xóa']),
    C('Hộp xác nhận nêu đúng số phiếu', 'P0', 'Đang ở chi tiết P-NHAP.', ['1. Bấm Xóa ở chân trang'], '',
      ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa phiếu yêu cầu mua dịch vụ \'<số phiếu>\'?"', 'Có nút Xóa, Hủy']),
    C('Bấm Hủy thì không xóa', 'P0', 'Đang mở hộp Xác nhận xóa.', ['1. Bấm Hủy'], '', ['Hộp đóng, phiếu còn nguyên']),
    C('Xóa phiếu Đang tạo thành công', 'P0', 'P-NHAP; danh sách có N phiếu.', ['1. Bấm Xóa, xác nhận'], '',
      ['Báo "Xóa thành công.", về danh sách', 'Phiếu biến mất, dòng tổng còn N - 1']),
    C('Xóa phiếu Không duyệt', 'P1', 'Phiếu Không duyệt của NV-A.', ['1. Mở phiếu, Xóa, xác nhận'], '', ['Xóa thành công']),
    C('Xóa phiếu vừa được gửi duyệt ở nơi khác', 'P2', 'P-NHAP mở chi tiết ở 2 tab.', ['1. Tab 1 sửa và Gửi duyệt', '2. Tab 2 bấm Xóa, xác nhận'], '',
      ['Tab 2 báo ' + CONFLICT + ', không xóa']),
    C('Xóa phiếu đã bị người lập xóa ở tab khác', 'P2', 'P-NHAP mở ở 2 tab; tab 1 đã xóa.', ['1. Tab 2 bấm Xóa, xác nhận'], '',
      ['Báo lỗi, không xóa thêm gì']),
    C('Không phải người lập không xóa được', 'P1', 'XEM-ALL mở phiếu Không duyệt của NV-A.', ['1. Xem chân trang'], '',
      ['Không có nút Xóa; nếu gửi yêu cầu: "Bạn không có quyền xóa phiếu này"']),
]

# ------------------------------------------------------------------ GỬI DUYỆT (gộp vào THÊM MỚI / CHỈNH SỬA, xem cuối file)
S_GUI = [
    C('Gửi duyệt khi lập phiếu với dữ liệu hợp lệ', 'P0', 'TP-1 cùng công ty.',
      ['1. Nhập Ghi chú, file bao-gia.pdf, 2 dòng dịch vụ đủ, VAT 8', '2. Bấm Gửi duyệt'], '',
      ['Báo "Thêm mới thành công.", về danh sách; phiếu Chờ TP duyệt', 'Phiếu ghi Công ty, Phòng yêu cầu = của NV-A',
       'TP-1 nhận thông báo "[YCMDV] Chờ duyệt: <số phiếu>" có người lập, tổng tiền; bấm mở trang Chi tiết']),
    C('Gửi duyệt thiếu file hoặc dòng dịch vụ', 'P0', 'Đang ở trang Tạo.', ['1. Nhập Ghi chú, không thêm file, dòng dịch vụ để trống', '2. Bấm Gửi duyệt'], '',
      ['File đính kèm: "Bắt buộc phải nhập"', 'Dòng 1: Tên dịch vụ, Số lượng, Giá đề xuất báo "Bắt buộc phải nhập" (nếu trống)',
       'Cuộn tới ô lỗi đầu tiên, không lưu']),
    C('Gửi duyệt với Số lượng hoặc Giá bằng 0', 'P1', 'Đang ở trang Tạo.', ['1. Nhập đủ Ghi chú, file, Tên dịch vụ; Số lượng 0, Giá 0', '2. Bấm Gửi duyệt'], '',
      ['Hệ thống báo lỗi Số lượng / Giá đề xuất phải lớn hơn 0, không gửi duyệt phiếu 0 đồng']),
    C('Gửi duyệt khi VAT sai', 'P2', 'VAT 120.', ['1. Bấm Gửi duyệt'], '', ['Báo "Không được lớn hơn 100.", không gửi']),
    C('Sửa phiếu Đang tạo rồi gửi duyệt', 'P0', 'P-NHAP của NV-A.', ['1. Bấm Sửa', '2. Thêm file, dòng dịch vụ, bấm Gửi duyệt'], '',
      ['"Cập nhật thành công.", phiếu Chờ TP duyệt; TP-1 nhận thông báo']),
    C('Gửi duyệt lại sau khi bị từ chối', 'P0', 'Phiếu Không duyệt.', ['1. NV-A sửa, bấm Gửi duyệt', '2. TP-1 mở lại phiếu'], '',
      ['Phiếu Chờ TP duyệt, TP-1 duyệt được như bình thường']),
    C('Một lần gửi duyệt không sinh 2 mốc trạng thái', 'P2', 'Sửa P-NHAP rồi Gửi duyệt.', ['1. Xem lịch sử'], '',
      ['1 mốc Thay đổi thông tin (không có dòng Trạng thái) + 1 mốc Thay đổi trạng thái Đang tạo > Chờ TP duyệt']),
    C('Bấm Gửi duyệt hai lần liên tục', 'P1', 'Đang ở trang Tạo, dữ liệu hợp lệ.', ['1. Bấm Gửi duyệt 2 lần thật nhanh'], '',
      ['Nút khóa sau lần bấm đầu, chỉ tạo 1 phiếu, chỉ 1 thông báo gửi đi']),
]

# ------------------------------------------------------------------ VII. DUYỆT PHIẾU
S_DUYET = [
    C('Điều kiện hiện nút Trưởng phòng duyệt', 'P0', 'TP-1; phiếu Chờ TP duyệt và phiếu Chờ KS duyệt.', ['1. Mở chi tiết 2 phiếu'], '',
      ['Phiếu Chờ TP duyệt có Trưởng phòng duyệt, Từ chối', 'Phiếu Chờ KS duyệt không có nút của TP']),
    C('Giao diện cửa sổ Trưởng phòng duyệt', 'P1', 'TP-1, phiếu Chờ TP duyệt.', ['1. Bấm Trưởng phòng duyệt'], '',
      ['Cửa sổ "Trưởng phòng duyệt yêu cầu mua dịch vụ", dòng "Phiếu: <số phiếu>"', 'Ô Ý kiến Trưởng phòng không bắt buộc; nút Duyệt, Hủy']),
    C('Trưởng phòng duyệt thành công', 'P0', 'Phiếu Chờ TP duyệt; TP-1 không còn hàng quá hạn.',
      ['1. TP-1 mở phiếu, bấm Trưởng phòng duyệt', '2. Nhập ý kiến "Đồng ý", bấm Duyệt'], '',
      ['"Duyệt thành công.", về danh sách; phiếu Chờ KS duyệt', 'Ngày nhận đơn = thời điểm duyệt; Ý kiến Trưởng phòng = "Đồng ý"',
       'KS-1 nhận thông báo "[YCMDV] Chờ duyệt … Trưởng phòng đã duyệt, chờ Ban kiểm soát duyệt giá"']),
    C('Bấm Hủy ở cửa sổ duyệt', 'P1', 'Đang mở cửa sổ Trưởng phòng duyệt.', ['1. Bấm Hủy'], '', ['Cửa sổ đóng, phiếu vẫn Chờ TP duyệt']),
    C('Trưởng phòng duyệt bị chặn do hàng quá hạn', 'P1', 'TP-1 (hoặc nhân viên phòng TP-1 quản lý) còn hàng quá hạn theo cấu hình "Duyệt yêu cầu mua dịch vụ".',
      ['1. TP-1 bấm Trưởng phòng duyệt, Duyệt'], '', ['Không duyệt được, hiện lý do và danh sách hàng quá hạn', 'Phiếu vẫn Chờ TP duyệt']),
    C('Trưởng phòng duyệt phiếu phòng khác', 'P2', 'TP-1 quản lý P1; phiếu Chờ TP duyệt phòng P2 cùng công ty.', ['1. TP-1 mở phiếu P2'], '',
      ['Có nút Trưởng phòng duyệt (không giới hạn phòng ban)']),
    C('Ban kiểm soát duyệt giá', 'P0', 'Phiếu Chờ KS duyệt (vừa được TP duyệt).', ['1. KS-1 mở phiếu, bấm Kiểm soát duyệt giá', '2. Nhập ý kiến, bấm Duyệt giá'], '',
      ['Cửa sổ "Ban kiểm soát duyệt giá"; không có ô nhập giá duyệt từng dòng', '"Duyệt thành công."; phiếu Đã duyệt; Người duyệt giá = KS-1, Ngày duyệt giá = lúc duyệt',
       'Danh sách dịch vụ có Giá duyệt, Thành tiền duyệt và tổng duyệt đúng giá Ban kiểm soát chấp nhận (không bằng 0)']),
    C('Ban kiểm soát khác công ty không duyệt được', 'P1', 'Phiếu Chờ KS duyệt của TPE; KS-2 công ty khác.', ['1. Đăng nhập KS-2, mở phiếu (nếu xem được qua quyền xem)'], '',
      ['Không có nút Kiểm soát duyệt giá, Từ chối']),
    C('Hai người cùng duyệt 1 phiếu', 'P2', 'TP-1 và TP-2 cùng mở phiếu Chờ TP duyệt.', ['1. TP-1 duyệt', '2. TP-2 bấm Duyệt (chưa tải lại trang)'], '',
      ['TP-2 nhận ' + CONFLICT + ', không duyệt lần 2']),
    C('Người lập không tự duyệt khi không có quyền', 'P1', 'NV-A không có quyền TP.', ['1. NV-A mở phiếu mình vừa gửi duyệt'], '',
      ['Không có nút Trưởng phòng duyệt, Từ chối']),
    C('Không duyệt lại phiếu đã xử lý', 'P1', 'P-DUYET.', ['1. TP-1, KS-1 mở chi tiết'], '', ['Không còn nút duyệt / từ chối']),
    C('Yêu cầu duyệt lại giá', 'P0', 'P-DUYET của NV-A.', ['1. NV-A mở P-DUYET, bấm Yêu cầu duyệt lại giá'], '',
      ['Thực hiện ngay (không có hộp xác nhận), "Thao tác thành công."; phiếu về Chờ KS duyệt', 'KS-1 nhận thông báo "Xin duyệt lại giá"',
       'KS-1 duyệt giá lại được, phiếu về Đã duyệt']),
    C('Lịch sử ghi người duyệt và thời gian', 'P1', 'Phiếu vừa qua TP-1 và KS-1.', ['1. Xem lịch sử'], '',
      ['2 mốc Thay đổi trạng thái (Chờ TP duyệt > Chờ KS duyệt, Chờ KS duyệt > Đã duyệt) kèm ý kiến, người thực hiện, thời điểm']),
]

# ------------------------------------------------------------------ VIII. KHÔNG DUYỆT PHIẾU (Từ chối)
S_KD = [
    C('Điều kiện hiện nút Từ chối', 'P0', 'TP-1, KS-1; phiếu Chờ TP duyệt và Chờ KS duyệt.', ['1. Mỗi người mở 2 phiếu'], '',
      ['TP-1 có Từ chối ở phiếu Chờ TP duyệt', 'KS-1 có Từ chối ở phiếu Chờ KS duyệt cùng công ty', 'NV-A (người lập) không có Từ chối']),
    C('Giao diện cửa sổ Từ chối', 'P1', 'TP-1, phiếu Chờ TP duyệt.', ['1. Bấm Từ chối'], '',
      ['Cửa sổ "Từ chối yêu cầu mua dịch vụ", ô Lý do từ chối bắt buộc, nút Từ chối, Hủy']),
    C('Bỏ trống lý do từ chối', 'P0', 'Đang mở cửa sổ Từ chối.', ['1. Để trống lý do, bấm Từ chối'], '', ['"Bắt buộc phải nhập", không gửi']),
    C('Lý do từ chối vượt 5000 ký tự', 'P2', 'Đang mở cửa sổ Từ chối.', ['1. Nhập lý do 5001 ký tự, bấm Từ chối'], 'Chuỗi 5001 ký tự',
      ['Báo lỗi độ dài, không gửi']),
    C('Từ chối ở nấc Trưởng phòng', 'P0', 'Phiếu Chờ TP duyệt.', ['1. TP-1 nhập lý do "Thiếu báo giá", bấm Từ chối', '2. Mở chi tiết phiếu'], '',
      ['"Thao tác thành công."; phiếu Không duyệt; Ý kiến Trưởng phòng = lý do',
       'NV-A nhận thông báo "[YCMDV] Từ chối" kèm người từ chối và lý do']),
    C('Từ chối ở nấc Ban kiểm soát', 'P0', 'Phiếu Chờ KS duyệt.', ['1. KS-1 bấm Từ chối, nhập lý do, bấm Từ chối'], '',
      ['Phiếu Không duyệt; lý do ghi vào Ý kiến Ban kiểm soát; người lập nhận thông báo']),
    C('Bấm Hủy ở cửa sổ Từ chối', 'P1', 'Đang mở cửa sổ, đã nhập lý do.', ['1. Bấm Hủy'], '', ['Cửa sổ đóng, phiếu không đổi trạng thái']),
    C('Không từ chối lại phiếu đã Không duyệt', 'P1', 'Phiếu Không duyệt.', ['1. TP-1 mở chi tiết'], '', ['Không có nút Từ chối, Trưởng phòng duyệt']),
    C('Từ chối phiếu vừa được duyệt ở nơi khác', 'P2', 'TP-1 và TP-2 cùng mở phiếu Chờ TP duyệt.', ['1. TP-2 duyệt', '2. TP-1 bấm Từ chối'], '',
      ['TP-1 nhận ' + CONFLICT + ', phiếu giữ trạng thái sau khi TP-2 duyệt']),
    C('Lịch sử ghi người từ chối và lý do', 'P1', 'Vừa từ chối.', ['1. Xem lịch sử'], '',
      ['Mốc Thay đổi trạng thái > Không duyệt, người thực hiện, thời điểm, lý do in trong khung vàng']),
]

# ------------------------------------------------------------------ IX. HỦY PHIẾU (Hủy yêu cầu)
S_HUY = [
    C('Điều kiện hiện nút Hủy yêu cầu', 'P0', 'NV-A có P-DUYET và phiếu Chờ TP duyệt; XEM-ALL.', ['1. NV-A xem 2 phiếu', '2. XEM-ALL mở P-DUYET'], '',
      ['Chỉ P-DUYET của người lập có Hủy yêu cầu', 'XEM-ALL không có Hủy yêu cầu']),
    C('Hủy yêu cầu thành công', 'P0', 'P-DUYET của NV-A.', ['1. Bấm Hủy yêu cầu', '2. Nhập lý do "Không còn nhu cầu", bấm Hủy yêu cầu'], '',
      ['Cửa sổ "Hủy yêu cầu mua dịch vụ", lý do không bắt buộc', '"Thao tác thành công."; phiếu Hủy, chỉ còn In phiếu, Lịch sử',
       'Lịch sử có mốc Thay đổi trạng thái Đã duyệt > Hủy kèm lý do; lý do không ghi vào ô ý kiến của phiếu']),
    C('Hủy yêu cầu không nhập lý do', 'P1', 'P-DUYET khác.', ['1. Bấm Hủy yêu cầu, để trống lý do, bấm Hủy yêu cầu'], '', ['Hủy thành công']),
    C('Bấm Hủy ở cửa sổ Hủy yêu cầu', 'P1', 'Đang mở cửa sổ.', ['1. Bấm nút Hủy'], '', ['Cửa sổ đóng, phiếu vẫn Đã duyệt']),
    C('Hủy phiếu vừa bị đổi trạng thái ở nơi khác', 'P2', 'P-DUYET mở ở 2 tab.', ['1. Tab 1 Yêu cầu duyệt lại giá', '2. Tab 2 Hủy yêu cầu'], '',
      ['Tab 2 báo ' + CONFLICT + ', không hủy']),
]

# ------------------------------------------------------------------ LỊCH SỬ (riêng)
K['lich_su_rieng'] = [
    C('Lịch sử đủ mốc qua cả luồng', 'P0', 'Phiếu đi hết: tạo nháp > sửa > gửi duyệt > TP duyệt > KS duyệt giá.',
      ['1. Bấm Lịch sử ở cột Hành động', '2. Ở trang Chi tiết bấm Xem lịch sử'], '',
      ['Có Tạo mới; Thay đổi thông tin (Ghi chú, Thuế VAT (%), File đính kèm, Dòng dịch vụ — cũ đỏ > mới xanh); Thay đổi trạng thái từng bước kèm ý kiến',
       'Mỗi mốc có "Người thực hiện: <họ tên> — <phòng ban>" và thời điểm', 'Khối Lịch sử ở chi tiết hiện y hệt']),
    C('Thao tác ngoài hệ thống không có mốc', 'P2', 'Phiếu đã lập hợp đồng ở cổng quản trị cũ.', ['1. Xem lịch sử'], '',
      ['Không có mốc cho bước lập hợp đồng']),
]

# ------------------------------------------------------------------ XEM CHI TIẾT
S_XEM = [
    C('Bấm Số phiếu mở trang chi tiết', 'P0', 'P-DUYET.', ['1. Bấm Số phiếu', '2. Quay lại, chuột phải vào Số phiếu'], '',
      ['Mở "Chi tiết yêu cầu mua dịch vụ: <số phiếu>"', 'Chuột phải có "Mở liên kết trong tab mới"']),
    C('Đầy đủ khối thông tin', 'P0', 'P-DUYET.', ['1. Mở chi tiết'], '',
      ['Khối Thông tin chung: Ghi chú, Ý kiến TP / KS, góc phải người tạo và ngày giờ tạo',
       'File đính kèm (xem, tải); Danh sách dịch vụ có Giá duyệt, Thành tiền duyệt, 3 dòng tổng; khối Lịch sử thu gọn']),
    C('Các ô chỉ đọc, không có nút Lưu', 'P0', 'Đang ở chi tiết.', ['1. Thử sửa các ô'], '', ['Mọi ô khóa, không có nút Lưu']),
    C('Dữ liệu chi tiết khớp với dữ liệu đã lập và dòng trên bảng', 'P0', 'Phiếu vừa gửi duyệt.', ['1. So chi tiết với dữ liệu đã nhập và dòng danh sách'], '',
      ['Ghi chú, file, dòng dịch vụ, tiền khớp; số dạng 1,234,567.89']),
    C('Chi tiết phiếu chưa tới bước duyệt giá', 'P1', 'Phiếu Chờ TP duyệt.', ['1. Mở chi tiết'], '', ['Bảng dịch vụ KHÔNG có cột Giá duyệt, Thành tiền duyệt']),
    C('Chi tiết phiếu không có file', 'P2', 'P-NHAP không có file.', ['1. Mở chi tiết'], '', ['Khối File đính kèm ghi "Không có file đính kèm."']),
    C('Chi tiết phiếu Không duyệt', 'P1', 'Phiếu bị KS từ chối.', ['1. Mở chi tiết'], '', ['Ý kiến Ban kiểm soát là lý do từ chối']),
    C('Chân trang theo trạng thái và vai trò', 'P1', 'P-DUYET; xem bằng NV-A rồi XEM-ALL.', ['1. Quan sát chân trang'], '',
      ['NV-A: Yêu cầu duyệt lại giá, Hủy yêu cầu, Lập hợp đồng mua dịch vụ, In phiếu, Quay lại', 'XEM-ALL: chỉ In phiếu, Quay lại']),
    C('Mở chi tiết phiếu ngoài phạm vi', 'P0', 'NV-B không quyền; P-DUYET của NV-A.', ['1. Dán đường dẫn trang Chi tiết P-DUYET'], '',
      ['Báo "Bạn không có quyền xem phiếu này", không lộ dữ liệu']),
    C('Quay lại từ chi tiết giữ bộ lọc', 'P1', 'Danh sách đang lọc Trạng thái = Đã duyệt.', ['1. Mở chi tiết', '2. Bấm Quay lại'], '',
      ['Về danh sách, bộ lọc vẫn giữ (trong 10 phút)']),
]

# ------------------------------------------------------------------ IN PHIẾU
S_IN = [
    C('In phiếu chưa duyệt', 'P1', 'Phiếu Chờ TP duyệt.', ['1. Bấm In phiếu'], '',
      ['Cửa sổ "Xem trước phiếu yêu cầu mua dịch vụ", tiêu đề công ty TRÊN PHIẾU, khổ ngang',
       '"PHIẾU YÊU CẦU MUA DỊCH VỤ", Số phiếu, Ngày lập, Ghi chú; bảng 2 cột tiền (Giá đề xuất, Thành tiền đề xuất), ĐVT "Gói"',
       'Khối ký Ban kiểm soát, Trưởng phòng, Người lập (ô chưa duyệt để trống)']),
    C('In phiếu Đã duyệt', 'P0', 'P-DUYET.', ['1. Bấm In phiếu', '2. Bấm In'], '',
      ['Bảng có thêm Giá duyệt, Thành tiền duyệt; 3 dòng tổng đúng số; nhãn "VAT (x%)"',
       'Dưới Ban kiểm soát / Trưởng phòng có họ tên + "Đã duyệt"', 'Bấm In mở hộp in']),
    C('In danh sách', 'P1', 'Lọc Trạng thái = Đã duyệt.', ['1. Bấm In danh sách'], '',
      ['Cửa sổ "Xem trước danh sách yêu cầu mua dịch vụ", tiêu đề "DANH SÁCH YÊU CẦU MUA DỊCH VỤ", đúng các phiếu đang lọc (mọi trang)',
       '9 cột: STT, Số phiếu, Ngày tạo, Ngày nhận đơn, Ngày duyệt giá, Người yêu cầu, Phòng yêu cầu, Người duyệt giá, Trạng thái (ngày dd/mm/yyyy)']),
    C('In danh sách quá 2,000 dòng', 'P2', 'Phạm vi trên 2,000 phiếu, không lọc.', ['1. Bấm In danh sách'], '',
      ['Không in, hiện câu nhắc thu hẹp bộ lọc, không có nút In']),
    C('Đóng cửa sổ xem trước', 'P2', 'Đang mở cửa sổ xem trước.', ['1. Bấm dấu x'], '', ['Cửa sổ đóng, danh sách giữ nguyên']),
]

# ------------------------------------------------------------------ RÀNG BUỘC
S_RB = [
    C('Lập hợp đồng mua dịch vụ', 'P1', 'P-DUYET của NV-A.', ['1. Bấm Lập hợp đồng mua dịch vụ'], '',
      ['Mở tab mới tới màn lập hợp đồng của phiếu; trang hiện tại không đổi', 'Không ghi gì vào phiếu ở bước này']),
    C('Trạng thái đổi theo số lượng đã lập hợp đồng', 'P1', 'Đã lập hợp đồng cho P-DUYET ở màn hợp đồng.', ['1. Lập hợp đồng 1 phần số lượng', '2. Lập đủ số lượng', '3. Xem phiếu'], '',
      ['Bước 1: phiếu Đang lập hợp đồng', 'Bước 2: phiếu Đã lập hợp đồng']),
    C('Phiếu Đang lập / Đã lập hợp đồng chỉ xem', 'P1', 'Có phiếu 2 trạng thái này.', ['1. Mở phiếu bằng người lập'], '',
      ['Đang lập hợp đồng: chỉ Lập hợp đồng mua dịch vụ, In phiếu', 'Đã lập hợp đồng: chỉ In phiếu, Quay lại']),
    C('Số phiếu gốc hiện ở màn YC hạch toán mua dịch vụ', 'P2', 'Có yêu cầu hạch toán lập từ P-DUYET.', ['1. Vào menu Bán hàng > Yêu cầu > Mua dịch vụ > YC hạch toán mua dịch vụ', '2. Bấm số phiếu gốc'], '',
      ['Bảng dịch vụ hiện số phiếu yêu cầu mua dịch vụ gốc', 'Bấm mở đúng trang Chi tiết phiếu']),
    C('Bấm thông báo mở đúng phiếu', 'P1', 'TP-1 có thông báo "[YCMDV] Chờ duyệt".', ['1. Bấm chuông thông báo, bấm thông báo'], '',
      ['Mở trang Chi tiết đúng phiếu, có nút Trưởng phòng duyệt, Từ chối']),
    C('Mã phí dịch vụ khóa thì không chọn được khi lập mới', 'P1', 'Khóa mã phí "Chi phí lắp đặt ống gió phòng sơn".', ['1. Lập phiếu mới, mở ô Tên dịch vụ'], '',
      ['Mã phí đã khóa không có trong danh sách; phiếu cũ đang dùng vẫn hiện đúng tên']),
    C('Luồng đầu cuối: lập > duyệt 2 nấc > lập hợp đồng', 'P0', 'NV-A, TP-1, KS-1.',
      ['1. NV-A lập và gửi duyệt', '2. TP-1 duyệt', '3. KS-1 duyệt giá', '4. NV-A lập hợp đồng đủ số lượng'], '',
      ['Trạng thái lần lượt: Chờ TP duyệt > Chờ KS duyệt > Đã duyệt > Đã lập hợp đồng',
       'Mỗi bước có thông báo đúng người, lịch sử đủ mốc']),
]

# ------------------------------------------------------------------ PHÂN QUYỀN
K.update(
    pre_an_nut='XEM-ALL mở P-DUYET và phiếu Chờ TP duyệt của NV-A; NV-A mở phiếu Chờ TP duyệt của mình.',
    exp_an_nut=['XEM-ALL không có Yêu cầu duyệt lại giá, Hủy yêu cầu, Lập hợp đồng mua dịch vụ, Sửa, Xóa (chỉ người lập)',
                'Người không có quyền TP / KS không có nút duyệt, Từ chối'],
    pre_url='NV-B không quyền; P-DUYET của NV-A.',
    exp_url=['Không xem được phiếu: "Bạn không có quyền xem phiếu này", không lộ dữ liệu'],
    pre_doi_quyen='TP-1 có quyền TP; phiếu Chờ TP duyệt.', man_doi_quyen='cửa sổ Trưởng phòng duyệt của phiếu',
    nut_doi_quyen='Duyệt',
    exp_doi_quyen=['Bị chặn: "Bạn không có quyền duyệt phiếu này"', 'Phiếu vẫn Chờ TP duyệt'],
)
S_QUYEN = [
    C('Nhân viên không quyền riêng vào được màn và lập phiếu', 'P0', 'NV-A không có quyền riêng của màn.',
      ['1. Đăng nhập NV-A', '2. Vào menu ' + MENU], 'NV-A',
      ['Màn hiện, tiêu đề "Yêu cầu mua dịch vụ"', 'Có Tạo mới, Xuất Excel, In danh sách, Cấu hình cột hiển thị', 'Chỉ thấy phiếu do NV-A lập']),
    C('Phạm vi "Xem yêu cầu mua dịch vụ - theo tổng công ty"', 'P0', 'XEM-ALL.', ['1. Đăng nhập XEM-ALL, vào màn', '2. Bấm Tìm kiếm nâng cao'], '',
      ['Thấy phiếu của mọi công ty (trừ phiếu Đang tạo của người khác)', 'Khu vực lọc có ô Công ty, Phòng ban']),
    C('Phạm vi "theo công ty"', 'P0', 'XEM-CTY công ty TPE.', ['1. Đăng nhập XEM-CTY, vào màn'], '',
      ['Chỉ phiếu có Công ty = TPE', 'Không có phiếu Đang tạo của người khác']),
    C('Phạm vi "theo phòng ban"', 'P1', 'XEM-PB quản lý P1, đang ngồi phòng P3.', ['1. Đăng nhập XEM-PB, vào màn'], '',
      ['Thấy phiếu phòng P1 (quản lý) và phòng P3 (đang ngồi)', 'Không thấy phiếu phòng khác']),
    C('Phiếu nháp chỉ người lập thấy', 'P0', 'P-NHAP do NV-A lập (Đang tạo).', ['1. Đăng nhập XEM-ALL / Super admin, tìm số phiếu P-NHAP', '2. Dán đường dẫn trang Chi tiết P-NHAP'], '',
      ['Không có trong danh sách', 'Mở trực tiếp: báo "Bạn không có quyền xem phiếu này"']),
    C('Người có quyền duyệt xem được phiếu cùng công ty qua thông báo', 'P1', 'TP-1 không có quyền xem; NV-A gửi duyệt phiếu.',
      ['1. Đăng nhập TP-1, bấm thông báo "[YCMDV] Chờ duyệt"', '2. Quay về danh sách'], '',
      ['Mở được trang Chi tiết phiếu, có nút Trưởng phòng duyệt, Từ chối', 'Danh sách (mục menu) chỉ hiện phiếu TP-1 lập (không có quyền xem)']),
] + phan_quyen_chung(K)

# Engine chỉ đánh số La Mã tới XV: "Gửi duyệt" (checklist: Thêm mới > Lưu và gửi duyệt) đặt trong THÊM MỚI / CHỈNH SỬA.
S_THEM += [S_GUI[i] for i in (0, 1, 2, 3, 7)]
S_SUA += [S_GUI[i] for i in (4, 5, 6)]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', danh_so(hien_thi(K))),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', danh_so(tim_kiem(K))),
    ('III', 'THÊM MỚI', danh_so(S_THEM)),
    ('IV', 'CHỈNH SỬA', danh_so(S_SUA)),
    ('V', 'XÓA', danh_so(S_XOA)),
    ('VI', 'DUYỆT PHIẾU', danh_so(S_DUYET)),
    ('VII', 'KHÔNG DUYỆT PHIẾU', danh_so(S_KD)),
    ('VIII', 'HỦY PHIẾU', danh_so(S_HUY)),
    ('IX', 'LỊCH SỬ THAY ĐỔI', danh_so(lich_su(K))),
    ('X', 'XEM CHI TIẾT YÊU CẦU MUA DỊCH VỤ', danh_so(S_XEM)),
    ('XI', 'IN PHIẾU', danh_so(S_IN)),
    ('XII', 'TÙY CHỈNH CỘT', danh_so(tuy_chinh_cot(K))),
    ('XIII', 'XUẤT DANH SÁCH EXCEL', danh_so(xuat_excel(K))),
    ('XIV', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', danh_so(S_RB)),
    ('XV', 'PHÂN QUYỀN', danh_so(S_QUYEN)),
]

if __name__ == '__main__':
    build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='phieu')
    print('Số nhóm: %d' % len(SECTIONS))
