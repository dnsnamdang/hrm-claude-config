# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu yêu cầu vận chuyển, bốc xếp" — skill testcase-documenter (tc_engine).

Chạy: python gen_testcase.py -> testcase.xlsx
30/10/2026: bản đầu (82 TC).
02/11/2026: xuất lại theo checklist "Mẫu tài liệu.xlsx" của tester — section sắp đúng thứ tự + tên nhóm checklist
(I..XIII), rồi phần riêng (XIV Chọn đơn hàng/hợp đồng và phiếu YCXH). Cài đặt bộ lọc nằm trong II, phân quyền gom 1 nhóm XI. Mỗi TC khai kèm danh sách
stt checklist nó kiểm (COVER) để gen_checklist.py dựng file "Đối chiếu checklist.xlsx".
Nguồn hành vi: code nhánh develop (FE pages/finance/delivery-requests/**, V2BaseDataTable, filterStateMixin,
columnCustomizationMixin, unsavedChangesMixin, saveAndContinueMixin, CatalogHistoryModal / SystemInfoSection;
BE DeliveryRequestController / StoreRequest / RejectRequest / WriteService / NotifyService / Entity).
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
from tc_engine import build, ROMAN  # noqa: E402
from tc_phieu_bosung import ListScreen, filter_memory_cases, combo_cases, org_cases, check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
FEATURE = 'Phiếu yêu cầu vận chuyển, bốc xếp - Cập nhật ngày 02/11/2026'
MENU = 'Vào phân hệ Bán hàng > nhóm "Yêu cầu" > "Hàng hóa" > bấm "YC vận chuyển, bốc xếp".'
M = '1. Đăng nhập.\n2. ' + MENU
TAO = '1. ' + MENU + '\n2. Bấm "Tạo mới".'
CHON = ('3. Bấm ô Đơn hàng/Hợp đồng, bấm dòng HĐ_TPE_HN_01.\n'
        '4. Bấm ô Phiếu YCXH, bấm dòng PYCXH-44434.')
CHK = 'Vui lòng kiểm tra lại thông tin đã nhập'
REQ = 'Bắt buộc phải nhập'
CONFLICT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'

# Dữ liệu chuẩn bị dùng chung
P25 = ('Tài khoản DNS Admin (Super admin).\nTrong phạm vi xem có 25 phiếu: TPE.YCVC1026.00001 Từ chối, 00003 Đã duyệt, '
       '00004 Chờ duyệt, 00005 và 00006 Đang tạo (DNS Admin lập), 20 phiếu Đã duyệt khác.')
PA = ('Tài khoản A (nhân viên kinh doanh, không có quyền xem theo cấp, không là thủ kho).\n'
      'Có HĐ_TPE_HN_01 còn hiệu lực; phiếu PYCXH-44434 (khách hàng KH0001 - Công ty TNHH An Phát, 6 dòng hàng, '
      '1 dòng số lượng 0) xuất từ Kho Hà Nội, kho có thủ kho G và G2.')
PFORM = PA + '\nA đang ở màn Tạo, đã chọn HĐ_TPE_HN_01 và PYCXH-44434 (bảng Chi tiết có 5 dòng).'
PEDIT = 'Tài khoản A lập phiếu TPE.YCVC1026.00006 trạng thái Đang tạo, Ghi chú "Giao buổi sáng", Tổng số kiện 3, 5 dòng hàng.'
PG = ('Tài khoản G là thủ kho Kho Hà Nội (không có quyền xem theo cấp).\nPhiếu TPE.YCVC1026.00004 trạng thái Chờ duyệt, '
      'gắn PYCXH-44434, do A lập.')
PHIS = 'Phiếu TPE.YCVC1026.00003 Đã duyệt có 8 mốc lịch sử (Tạo mới, Thay đổi thông tin, Thay đổi trạng thái...) do A và G thực hiện.'

COVER = {}   # stt checklist -> [TC ID]


def T(stts, func, prio, pre, steps, data, exp):
    return (list(stts), func, prio, pre, steps, data, exp)


def section(roman, title, items):
    idx = ROMAN.index(roman) + 1
    out = []
    for i, it in enumerate(items, 1):
        stts, rest = it[0], it[1:]
        tcid = 'TC_%02d.%03d' % (idx, i)
        for s in stts:
            COVER.setdefault(s, []).append(tcid)
        out.append(('%03d' % i,) + tuple(rest))
    return (roman, title, out)


def wrap(stts, case):
    """Case dựng sẵn từ tc_phieu_bosung (có id ở đầu) -> T()."""
    return T(stts, *case[1:])


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn Phiếu yêu cầu vận chuyển, bốc xếp dùng để người bán hàng đề nghị thủ kho bố trí vận chuyển và bốc xếp cho '
     'một phiếu yêu cầu xuất hàng của một đơn hàng/hợp đồng.\n'
     'Phiếu lưu nháp được (Đang tạo), gửi duyệt sang Chờ duyệt; thủ kho của kho xuất hàng Duyệt hoặc Từ chối (kèm lý do).'),
    ('2. Đối tượng được tính / hiển thị',
     '- Trạng thái: Đang tạo (xám), Chờ duyệt (cam), Đã duyệt (xanh lá), Từ chối (đỏ).\n'
     '- Danh sách: phiếu theo quyền xem theo cấp; không có quyền thì phiếu mình lập.\n'
     '- Luôn thấy thêm phiếu mình đã duyệt / từ chối và phiếu mình là thủ kho của kho xuất hàng.\n'
     '- Popup Chọn phiếu YCXH: phiếu yêu cầu xuất hàng trạng thái Đã đề nghị, Chờ duyệt, Đang tạo, Đợi TP duyệt, Đợi BGD '
     'duyệt và đã gắn khách hàng.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác: luôn ẩn ở danh sách.\n'
     '- Phiếu YCXH chưa gắn khách hàng: không có trong popup.\n'
     '- Dòng hàng số lượng bằng 0 trên phiếu YCXH: không đưa vào bảng Chi tiết.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày lập phiếu, lấy trọn hai đầu mút.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Phiếu > danh sách dòng hàng chép từ phiếu YCXH (Tên hàng, Model, Mã hàng hóa, ĐVT, Số lượng) + Số kiện người dùng nhập.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Khách hàng, người liên hệ, địa điểm giao, dòng hàng luôn đọc lại từ phiếu YCXH lúc lưu.\n'
     '- Đổi Đơn hàng/Hợp đồng thì xóa phiếu YCXH đã chọn.\n'
     '- Không kiểm trùng: cùng 1 phiếu YCXH lập được nhiều phiếu vận chuyển; mã phiếu tự sinh không trùng.'),
    ('7. Phân quyền cấp',
     '- Xem tất cả phiếu yêu cầu vận chuyển của tổng công ty.\n'
     '- Xem tất cả phiếu yêu cầu vận chuyển của công ty.\n'
     '- Xem tất cả phiếu yêu cầu vận chuyển của phòng ban.\n'
     '- Xem tất cả phiếu yêu cầu vận chuyển của bộ phận.\n'
     '- Lập phiếu, Xuất Excel, Xem lịch sử: không cần quyền riêng.\n'
     '- Duyệt / Từ chối: thủ kho của kho xuất hàng (không phải quyền, khai ở danh mục Kho vật lý), Super admin.\n'
     '- Sửa / Xóa: người lập, phiếu Đang tạo hoặc Từ chối.'),
    ('8. Cách tính các ô thống kê',
     '- Ô "Hiển thị a–b / N": a, b là dòng đầu – cuối của trang, N là tổng phiếu khớp bộ lọc trong phạm vi quyền.\n'
     '- Không có phiếu nào: dòng dưới bảng ghi "Không có phiếu nào.".'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong testcase: A, B (người lập, không quyền xem theo cấp), G, G2 (thủ kho Kho Hà Nội), C (quyền '
     'tổng công ty), D (công ty), E (phòng ban), F (bộ phận), DNS Admin (Super admin).\n'
     '- Mã phiếu dạng <mã công ty>.YCVC<tháng năm>.NNNNN.\n'
     '- Lưu ý: kho xuất hàng chưa khai thủ kho thì KHÔNG gửi duyệt được; cần chuẩn bị kho có thủ kho trước khi test.\n'
     '- Lưu ý: duyệt xong thì phiếu YCXH đổi ô Vận chuyển thành Công ty vận chuyển; kiểm ở màn Phiếu yêu cầu xuất hàng.\n'
     '- Lưu ý: Xuất Excel khi không có dữ liệu chỉ báo "Không có dữ liệu phù hợp." và KHÔNG tải file.\n'
     '- Lưu ý: màn không có Khóa / Mở khóa, Nhập Excel, In.\n'
     '- Nhóm case "dùng công cụ kiểm thử API gọi thẳng chức năng" dành cho tester kỹ thuật.'),
]

# ------------------------------------------------------------------ PHÂN QUYỀN & TRUY CẬP (khối đầu của tc_engine)
ROLE_TCS = [
    ('00', 'Không có quyền nào chỉ thấy phiếu mình lập', 'P0',
     'Tài khoản A không có quyền xem theo cấp, không là thủ kho.\nA lập 3 phiếu; công ty có 50 phiếu.',
     M, '—', '- Dưới bảng "Hiển thị 1–3 / 3".\n- Chỉ có 3 phiếu A lập.\n- Khối lọc không có ô Công ty, Phòng ban.'),
    ('01', 'Quyền xem của tổng công ty', 'P1',
     'Tài khoản C có quyền "Xem tất cả phiếu yêu cầu vận chuyển của tổng công ty"; 2 công ty có 80 phiếu (không tính nháp '
     'của người khác).', '1. Đăng nhập bằng C.\n2. ' + MENU, '—',
     '- Tổng số = 80.\n- Khối lọc có Công ty, Phòng ban, Bộ phận.'),
    ('02', 'Quyền xem của công ty', 'P1',
     'Tài khoản D có quyền "Xem tất cả phiếu yêu cầu vận chuyển của công ty", thuộc công ty 1 có 50 phiếu.',
     '1. Đăng nhập bằng D.\n2. ' + MENU, '—',
     '- Tổng số = 50 (trừ nháp của người khác).\n- Không có ô lọc Công ty; có Phòng ban, Bộ phận.'),
    ('03', 'Quyền xem của phòng ban', 'P1',
     'Tài khoản E có quyền "Xem tất cả phiếu yêu cầu vận chuyển của phòng ban", quản lý phòng Kinh doanh (12 phiếu), tự '
     'lập 2 phiếu ở phòng khác.', '1. Đăng nhập bằng E.\n2. ' + MENU, '—',
     '- Tổng số = 14.\n- Có ô Phòng ban; ô Bộ phận bị khóa.'),
    ('04', 'Quyền xem của bộ phận', 'P1',
     'Tài khoản F có quyền "Xem tất cả phiếu yêu cầu vận chuyển của bộ phận", quản lý bộ phận Bán lẻ (5 phiếu), tự lập 1 '
     'phiếu ở bộ phận khác.', '1. Đăng nhập bằng F.\n2. ' + MENU, '—', '- Tổng số = 6.\n- Có ô Bộ phận.'),
    ('05', 'Thủ kho thấy phiếu của kho mình', 'P0',
     'Tài khoản G là thủ kho Kho Hà Nội, không có quyền xem; có 4 phiếu xuất từ Kho Hà Nội (1 Chờ duyệt).',
     '1. Đăng nhập bằng G.\n2. ' + MENU, '—', '- Thấy đúng 4 phiếu đó.\n- Phiếu Chờ duyệt có icon Duyệt ở cột Hành động.'),
    ('06', 'Nháp của người khác luôn ẩn', 'P0', 'Tài khoản C (tổng công ty); B có 1 phiếu Đang tạo.',
     '1. Đăng nhập bằng C.\n2. ' + MENU + '\n3. Bấm Tìm kiếm nâng cao, chọn Trạng thái = Đang tạo.', 'Trạng thái: Đang tạo',
     '- Không thấy phiếu nháp của B.\n- Chỉ thấy phiếu nháp do C tự lập (nếu có).'),
    ('07', 'Không phải thủ kho không duyệt được', 'P0',
     'Tài khoản C (tổng công ty, không phải thủ kho, không phải Super admin); phiếu Chờ duyệt TPE.YCVC1026.00004.',
     '1. Đăng nhập bằng C.\n2. ' + MENU + '\n3. Quan sát cột Hành động dòng 00004.\n4. Bấm mã 00004 mở chi tiết.', '—',
     '- Cột Hành động dòng 00004 không có icon Duyệt.\n- Màn Chi tiết không có nút Duyệt, Từ chối; chỉ có Quay lại.'),
    ('08', 'Không phải người lập không sửa / xóa được', 'P0',
     'Tài khoản C (tổng công ty); phiếu TPE.YCVC1026.00001 Từ chối do A lập.',
     '1. Đăng nhập bằng C.\n2. ' + MENU + '\n3. Quan sát cột Hành động dòng 00001.\n4. Mở chi tiết phiếu 00001.', '—',
     '- Cột Hành động chỉ có icon Lịch sử, không có Sửa, Xóa.\n- Màn Chi tiết không có nút Sửa, Xóa.'),
    ('09', 'Mở chi tiết phiếu ngoài phạm vi', 'P1',
     'Tài khoản A (không quyền); phiếu TPE.YCVC1026.00003 do B lập, A không liên quan.\nB gửi cho A đường link màn Chi tiết '
     'phiếu 00003.', '1. Đăng nhập bằng A.\n2. Dán đường link B gửi vào thanh địa chỉ, nhấn Enter.', '—',
     '- Hệ thống chuyển sang trang không tìm thấy.\n- KHÔNG hiện dữ liệu phiếu 00003.'),
]
ROLE_COVER = {'00': [287, 299], '01': [299], '02': [299], '03': [299], '04': [299], '05': [287, 299],
              '06': [299], '07': [295], '08': [290, 291, 295], '09': [288, 296]}

SCREEN = ListScreen(menu=MENU, title='Phiếu yêu cầu vận chuyển, bốc xếp', total=25,
                    quick_label='mã phiếu, số hợp đồng, mã phiếu YCXH', quick_sample='YCVC1026',
                    quick_hit='6 phiếu TPE.YCVC1026.00001 đến 00006',
                    filters=[('Trạng thái', 'Đang tạo'), ('Người tạo', 'DNS Admin')],
                    org_levels=('Công ty', 'Phòng ban', 'Bộ phận'))
ORG = org_cases(SCREEN, 1)
MEM = filter_memory_cases(SCREEN, 1)
CMB = combo_cases(SCREEN, 1)

# ================================================================== I
S1 = [
    T([1, 2, 10, 16, 19], 'Mở màn từ menu', 'P0', P25, M, '—',
      '- Thanh tiêu đề trang, tab trình duyệt và đầu bảng ghi "Phiếu yêu cầu vận chuyển, bốc xếp".\n'
      '- Mặc định hiện 10 phiếu / trang; ô Số dòng/trang có các lựa chọn 5, 10, 20, 50, 100.\n'
      '- Sắp xếp phiếu tạo mới nhất ở trên, cũ nhất ở dưới (2 phiếu cùng thời điểm: phiếu lập sau ở trên).\n'
      '- Dưới bảng ghi đúng khuôn "Hiển thị 1–10 / 25".'),
    T([3], 'Các nút chức năng trên màn danh sách', 'P1', P25, M + '\n3. Quan sát khối Bộ lọc danh sách và thanh nút trên bảng.', '—',
      '- Khối lọc: ô tìm nhanh gợi ý "Tìm theo mã phiếu, số hợp đồng, mã phiếu YCXH...", nút Tìm kiếm, Làm mới, Tìm kiếm '
      'nâng cao, Cài đặt bộ lọc.\n'
      '- Trên bảng: nút Tạo mới, Xuất Excel, icon Cấu hình cột hiển thị (rê chuột hiện "Cấu hình cột hiển thị").\n'
      '- KHÔNG có nút Nhập Excel, In, Khóa.'),
    T([4, 5], 'Các cột mặc định hiện và ẩn', 'P1', 'Tài khoản DNS Admin chưa từng tùy chỉnh cột màn này.',
      M + '\n3. Quan sát tiêu đề cột.', '—',
      '- Hiện 12 cột theo thứ tự: STT, Mã phiếu, Số hợp đồng/đơn hàng, Khách hàng, Ngày tạo, Người tạo, Ngày cập nhật, '
      'Người cập nhật, Ngày duyệt, Người duyệt, Trạng thái, Hành động.\n'
      '- Cột Phiếu YCXH mặc định ẩn (chỉ bật trong Tùy chỉnh cột).'),
    T([6], 'Dữ liệu trên lưới đúng với phiếu vừa tạo', 'P0', PA + '\nA thuộc phòng ban mã KD1, họ tên Nguyễn Văn A.',
      TAO + '\n' + CHON + '\n5. Bấm Lưu nháp.\n6. Quan sát dòng đầu tiên của danh sách.', '—',
      '- Mã phiếu dạng TPE.YCVC<tháng năm>.NNNNN, là chữ xanh bấm được.\n'
      '- Số hợp đồng/đơn hàng: HĐ_TPE_HN_01; Khách hàng: KH0001 - Công ty TNHH An Phát.\n'
      '- Ngày tạo, Ngày cập nhật: thời điểm vừa lưu, dạng dd/mm/yyyy hh:mm.\n'
      '- Người tạo, Người cập nhật: "Nguyễn Văn A - KD1".\n'
      '- Ngày duyệt, Người duyệt: trống; Trạng thái: Đang tạo.'),
    T([7], 'Màu nhãn trạng thái', 'P2', P25, M + '\n3. Quan sát cột Trạng thái các phiếu 00001, 00003, 00004, 00006.', '—',
      '- Đang tạo: nhãn xám.\n- Chờ duyệt: nhãn cam.\n- Đã duyệt: nhãn xanh lá.\n- Từ chối: nhãn đỏ.'),
    T([8], 'Danh sách chưa có dữ liệu', 'P1',
      'Tài khoản H mới tạo, không có quyền xem theo cấp, không là thủ kho, chưa lập phiếu nào.',
      '1. Đăng nhập bằng H.\n2. ' + MENU, '—',
      '- Giữa bảng hiện "Không có dữ liệu phù hợp.".\n- Dưới bảng ghi "Không có phiếu nào.".\n'
      '- Nút Tạo mới vẫn hiện, màn không báo lỗi.'),
    T([9], 'Không có dữ liệu phù hợp bộ lọc', 'P1', P25,
      M + '\n3. Nhập "KHONGTONTAI999" vào ô tìm nhanh, bấm Tìm kiếm.', 'Ô tìm nhanh: KHONGTONTAI999',
      '- Giữa bảng hiện "Không có dữ liệu phù hợp.".\n- Dưới bảng ghi "Không có phiếu nào.".\n- Bấm Làm mới thì hiện lại đủ 25 phiếu.'),
    T([11, 18], 'Đổi số dòng/trang', 'P1', P25 + '\nĐang xem trang 2.',
      '1. Ở cuối bảng chọn Số dòng/trang = 20.', 'Số dòng/trang: 20',
      '- Danh sách về trang 1.\n- Hiện 20 phiếu, dưới bảng "Hiển thị 1–20 / 25".\n- Thanh phân trang còn 2 trang.'),
    T([12], 'Nút trang tiếp theo / trang trước', 'P1', P25 + '\nĐang ở trang 1, 10 dòng/trang.',
      '1. Bấm nút trang tiếp theo (mũi tên phải đơn).\n2. Bấm nút trang trước (mũi tên trái đơn).', '—',
      '- Bước 1: sang trang 2, dưới bảng "Hiển thị 11–20 / 25".\n- Bước 2: về trang 1, "Hiển thị 1–10 / 25".'),
    T([13, 14], 'Về trang đầu / trang cuối và trạng thái nút', 'P1', P25 + '\nĐang ở trang 1, 10 dòng/trang.',
      '1. Quan sát nút về trang đầu và nút trang trước.\n2. Bấm nút về trang cuối (mũi tên phải kép).\n'
      '3. Quan sát nút trang tiếp theo và nút về trang cuối.\n4. Bấm nút về trang đầu (mũi tên trái kép).', '—',
      '- Bước 1: nút về trang đầu và trang trước bị mờ, không bấm được.\n- Bước 2: sang trang 3, "Hiển thị 21–25 / 25".\n'
      '- Bước 3: nút trang tiếp theo và về trang cuối bị mờ.\n- Bước 4: về trang 1.'),
    T([15], 'STT liên tục giữa các trang', 'P2', P25 + '\n10 dòng/trang.', '1. Bấm trang 2.\n2. Quan sát cột STT.', '—',
      '- Trang 2 đánh STT từ 11 đến 20 (không bắt đầu lại từ 1).'),
    T([16], 'Tổng số bản ghi cập nhật sau khi lập phiếu', 'P1', 'Tài khoản A đang có 3 phiếu, dưới bảng "Hiển thị 1–3 / 3".',
      TAO + '\n' + CHON + '\n5. Bấm Lưu nháp.\n6. Quan sát dòng dưới bảng.', '—', '- Dưới bảng đổi thành "Hiển thị 1–4 / 4".'),
    T([17], 'Về trang 1 khi đổi bộ lọc', 'P1', P25 + '\nĐang ở trang 3.',
      '1. Bấm Tìm kiếm nâng cao.\n2. Chọn Trạng thái = Đã duyệt.', 'Trạng thái: Đã duyệt',
      '- Danh sách nạp lại ngay, về trang 1.\n- Dưới bảng "Hiển thị 1–10 / 21".'),
    T([20, 21], 'Sắp xếp tăng dần / giảm dần theo Mã phiếu', 'P1', P25,
      M + '\n3. Bấm tiêu đề cột Mã phiếu.\n4. Bấm lại tiêu đề cột Mã phiếu.', '—',
      '- Bước 3: xếp mã tăng dần (00001 trên cùng), biểu tượng mũi tên lên.\n'
      '- Bước 4: xếp mã giảm dần, biểu tượng mũi tên xuống.\n- Mỗi lần bấm đều về trang 1.'),
    T([22], 'Sắp xếp theo Ngày tạo / Ngày cập nhật', 'P1',
      P25 + '\nPhiếu 00003 lập ngày 01/10/2026 nhưng cập nhật gần nhất ngày 28/10/2026.',
      M + '\n3. Bấm tiêu đề cột Ngày tạo hai lần.\n4. Bấm tiêu đề cột Ngày cập nhật hai lần.', '—',
      '- Bước 3: lần 1 xếp ngày tạo cũ nhất lên trên, lần 2 mới nhất lên trên.\n'
      '- Bước 4: lần 2 phiếu 00003 lên gần đầu theo ngày cập nhật 28/10/2026, không theo ngày tạo.'),
    T([23], 'Cột không hỗ trợ sắp xếp', 'P2', P25,
      M + '\n3. Bấm tiêu đề các cột STT, Người tạo, Người cập nhật, Người duyệt, Trạng thái, Hành động.', '—',
      '- Các cột này không có biểu tượng sắp xếp.\n- Bấm tiêu đề không đổi thứ tự danh sách.\n'
      '- Chỉ 6 cột sắp xếp được: Mã phiếu, Số hợp đồng/đơn hàng, Khách hàng, Ngày tạo, Ngày cập nhật, Ngày duyệt.'),
    T([24], 'Giữ sắp xếp khi chuyển trang', 'P1', P25, M + '\n3. Bấm tiêu đề Khách hàng (tăng dần).\n4. Bấm trang 2.', '—',
      '- Trang 2 tiếp tục thứ tự khách hàng tăng dần từ trang 1.\n- Biểu tượng mũi tên lên ở cột Khách hàng vẫn giữ.'),
    T([25], 'Về trang 1 khi đổi sắp xếp', 'P2', P25 + '\nĐang ở trang 2.', '1. Bấm tiêu đề cột Ngày duyệt.', '—',
      '- Danh sách về trang 1, xếp theo Ngày duyệt tăng dần.'),
    T([3], 'Nút trên dòng theo trạng thái và người lập', 'P0',
      'Tài khoản A lập phiếu 00006 (Đang tạo), 00001 (Từ chối), 00003 (Đã duyệt), 00004 (Chờ duyệt).',
      '1. Đăng nhập bằng A.\n2. ' + MENU + '\n3. Quan sát cột Hành động 4 dòng.', '—',
      '- 00006, 00001: có icon Sửa, Xóa, Lịch sử.\n- 00003, 00004: chỉ có icon Lịch sử.\n- A không là thủ kho nên không có icon Duyệt.'),
    T([], 'Bấm Số hợp đồng/đơn hàng mở chứng từ', 'P1',
      P25 + '\nPhiếu 00004 gắn hợp đồng bán trên hệ thống mới; phiếu 00003 gắn hợp đồng chỉ có trên ERP.',
      M + '\n3. Bấm số hợp đồng ở dòng 00004.\n4. Bấm số hợp đồng ở dòng 00003.', '—',
      '- Mỗi lần bấm mở chứng từ ở tab trình duyệt mới (00004 mở màn hợp đồng trên hệ thống mới, 00003 mở màn ERP).\n'
      '- Màn danh sách giữ nguyên.'),
]

# ================================================================== II
S2 = [
    T([26], 'Tìm theo mã phiếu đầy đủ', 'P0', P25, M + '\n3. Nhập "TPE.YCVC1026.00004" vào ô tìm nhanh.\n4. Bấm Tìm kiếm.',
      'Ô tìm nhanh: TPE.YCVC1026.00004', '- Chỉ còn đúng phiếu TPE.YCVC1026.00004.\n- Dưới bảng "Hiển thị 1–1 / 1".'),
    T([27], 'Tìm một phần mã phiếu', 'P0', P25, M + '\n3. Nhập "00004", bấm Tìm kiếm.', 'Ô tìm nhanh: 00004',
      '- Ra mọi phiếu có mã chứa "00004", gồm TPE.YCVC1026.00004.'),
    T([27], 'Tìm một phần số hợp đồng', 'P1', P25 + '\nPhiếu 00003 gắn HĐ_TPE_HN_KD2_26_0412.',
      M + '\n3. Nhập "KD2_26_0412", bấm Tìm kiếm.', 'Ô tìm nhanh: KD2_26_0412', '- Ra phiếu 00003.'),
    T([27], 'Tìm một phần mã phiếu YCXH', 'P1', P25 + '\nPhiếu 00004 gắn PYCXH-44434.',
      M + '\n3. Nhập "44434", bấm Tìm kiếm.', 'Ô tìm nhanh: 44434', '- Ra phiếu 00004 (dù cột Phiếu YCXH đang ẩn).'),
    T([28], 'Không phân biệt chữ hoa / thường', 'P1', P25, M + '\n3. Nhập "tpe.ycvc1026.00004", bấm Tìm kiếm.',
      'Ô tìm nhanh: tpe.ycvc1026.00004', '- Ra phiếu TPE.YCVC1026.00004 như khi gõ chữ hoa.'),
    T([29], 'Tìm có dấu / không dấu', 'P2', P25 + '\nPhiếu 00004 gắn HĐ_TPE_HN_01.',
      M + '\n3. Nhập "hđ_tpe_hn_01", bấm Tìm kiếm.\n4. Nhập "HD_TPE_HN_01" (chữ D không gạch), bấm Tìm kiếm.',
      'Lần 1: hđ_tpe_hn_01\nLần 2: HD_TPE_HN_01',
      '- Lần 1: ra phiếu 00004 (khác hoa / thường vẫn khớp).\n'
      '- Lần 2: "Không có dữ liệu phù hợp." — chữ Đ và D là hai chữ khác nhau.\n'
      '- Lưu ý: ô tìm theo mã / số chứng từ, không bỏ dấu tiếng Việt.'),
    T([30], 'Từ khóa không tồn tại', 'P1', P25, M + '\n3. Nhập "ZZZ-9999", bấm Tìm kiếm.', 'Ô tìm nhanh: ZZZ-9999',
      '- Giữa bảng "Không có dữ liệu phù hợp.".\n- Dưới bảng "Không có phiếu nào.".'),
    T([31], 'Ký tự đặc biệt trong từ khóa', 'P1', P25 + '\nKhông có mã / số hợp đồng nào chứa ký tự %.',
      M + "\n3. Nhập \"%\", bấm Tìm kiếm.\n4. Nhập \"'\" (dấu nháy đơn), bấm Tìm kiếm.\n5. Nhập \"_HN_\", bấm Tìm kiếm.",
      "Lần 1: %\nLần 2: '\nLần 3: _HN_",
      '- Lần 1, 2: "Không có dữ liệu phù hợp.", KHÔNG ra toàn bộ danh sách, không báo lỗi hệ thống.\n'
      '- Lần 3: chỉ ra phiếu có số hợp đồng chứa đúng chuỗi "_HN_" (dấu gạch dưới hiểu là ký tự thường).'),
    T([32], 'Khoảng trắng đầu / cuối từ khóa', 'P1', P25, M + '\n3. Nhập "   00004   ", bấm Tìm kiếm.',
      'Ô tìm nhanh: (3 dấu cách)00004(3 dấu cách)', '- Hệ thống bỏ khoảng trắng, ra phiếu 00004 như khi gõ "00004".'),
    wrap([33], CMB[3]),
    T([34], 'Xóa từ khóa', 'P1', P25 + '\nĐang tìm "00004", bảng còn 1 phiếu.',
      '1. Bấm dấu × cuối ô tìm nhanh (hoặc xóa hết chữ).\n2. Bấm Tìm kiếm.', '—',
      '- Bước 1: ô tìm nhanh trống.\n- Bước 2: danh sách hiện lại đủ 25 phiếu, về trang 1.'),
    T([35], 'Enter và nút Tìm kiếm', 'P1', P25,
      M + '\n3. Gõ "00004" vào ô tìm nhanh, chưa bấm gì.\n4. Nhấn Enter.\n5. Xóa từ khóa, gõ "00003", bấm nút Tìm kiếm.', '—',
      '- Bước 3: danh sách chưa đổi (ô tìm nhanh không lọc ngay khi gõ).\n- Bước 4: chỉ còn phiếu 00004.\n'
      '- Bước 5: chỉ còn phiếu 00003.'),
    T([36], 'Giá trị mặc định của bộ lọc', 'P1', P25 + '\nChưa lọc gì trong 10 phút gần đây.',
      M + '\n3. Bấm Tìm kiếm nâng cao.', '—',
      '- Hiện 6 tiêu chí: Công ty – Phòng ban – Bộ phận, Khách hàng, Hợp đồng, Người tạo, Trạng thái, Ngày tạo.\n'
      '- Mọi ô đều trống (mọi công ty, mọi trạng thái, mọi ngày).\n- Nhãn nút đổi thành "Ẩn tìm kiếm nâng cao".'),
    T([37], 'Lọc theo Trạng thái', 'P0', P25 + '\nCó đúng 2 phiếu Từ chối.',
      M + '\n3. Bấm Tìm kiếm nâng cao.\n4. Chọn Trạng thái = Từ chối.', 'Trạng thái: Từ chối',
      '- Danh sách nạp lại ngay, không cần bấm Tìm kiếm.\n- Còn 2 phiếu, đều nhãn đỏ Từ chối.'),
    T([37], 'Lọc theo Khách hàng', 'P1', P25 + '\nKhách hàng "Công ty Cổ phần Thiết bị Công nghiệp Kinoko" có 1 phiếu.',
      M + '\n3. Bấm Tìm kiếm nâng cao.\n4. Gõ "K" vào ô Khách hàng.\n5. Gõ tiếp thành "Kinoko", chọn dòng gợi ý.', 'Khách hàng: Kinoko',
      '- Bước 4: chưa hiện gợi ý (cần tối thiểu 2 ký tự).\n- Bước 5: gợi ý dạng "Mã - Tên"; chọn xong lọc ngay, còn 1 phiếu.'),
    T([37], 'Lọc theo Hợp đồng', 'P1', P25 + '\n3 phiếu có số hợp đồng chứa "KD2".',
      M + '\n3. Bấm Tìm kiếm nâng cao.\n4. Nhập "KD2" vào ô Hợp đồng.\n5. Nhấn Enter.', 'Hợp đồng: KD2',
      '- Bước 4: danh sách chưa đổi.\n- Bước 5: còn 3 phiếu có số hợp đồng chứa "KD2".'),
    T([37], 'Lọc theo Người tạo', 'P2', P25 + '\nDNS Admin lập 2 phiếu (00005, 00006).',
      M + '\n3. Bấm Tìm kiếm nâng cao.\n4. Chọn Người tạo = DNS Admin.', 'Người tạo: DNS Admin',
      '- Lọc ngay, còn 2 phiếu 00005, 00006.'),
    T([37], 'Lọc theo Ngày tạo lấy trọn ngày biên', 'P0', P25 + '\n3 phiếu tạo ngày 21/10/2026 (lúc 08:05, 12:30, 23:50).',
      M + '\n3. Bấm Tìm kiếm nâng cao.\n4. Chọn Ngày tạo từ 21/10/2026 đến 21/10/2026.', 'Ngày tạo: 21/10/2026 - 21/10/2026',
      '- Đúng 3 phiếu, kể cả phiếu lập lúc 23:50.'),
    wrap([37], ORG[0]), wrap([37], ORG[1]), wrap([37], ORG[2]),
    wrap([38], CMB[1]),
    wrap([39], CMB[0]),
    wrap([38, 40], CMB[2]),
    T([41], 'Tổng số sau lọc', 'P1', P25 + '\n21 phiếu Đã duyệt.',
      M + '\n3. Bấm Tìm kiếm nâng cao.\n4. Chọn Trạng thái = Đã duyệt.', 'Trạng thái: Đã duyệt',
      '- Dưới bảng "Hiển thị 1–10 / 21" (N là tổng phiếu khớp bộ lọc, không phải 25).'),
    T([42], 'Phân trang sau lọc', 'P1', P25 + '\n21 phiếu Đã duyệt.',
      M + '\n3. Lọc Trạng thái = Đã duyệt.\n4. Bấm trang 3.', 'Trạng thái: Đã duyệt',
      '- Thanh phân trang còn 3 trang.\n- Trang 3 có 1 phiếu, "Hiển thị 21–21 / 21", vẫn chỉ phiếu Đã duyệt.'),
    T([43], 'Sắp xếp sau lọc', 'P2', P25, M + '\n3. Lọc Trạng thái = Đã duyệt.\n4. Bấm tiêu đề Ngày duyệt.', 'Trạng thái: Đã duyệt',
      '- Danh sách vẫn chỉ phiếu Đã duyệt, xếp theo Ngày duyệt tăng dần, về trang 1.'),
    T([44], 'Làm mới xóa bộ lọc', 'P1', P25 + '\nĐang lọc Trạng thái = Đã duyệt, Khách hàng = Kinoko, ô tìm nhanh "YCVC", sắp xếp theo Mã phiếu, ở trang 2.',
      '1. Bấm Làm mới.', '—',
      '- Mọi ô lọc và ô tìm nhanh về trống.\n- Bỏ sắp xếp (về Ngày tạo giảm dần), về trang 1, hiện đủ 25 phiếu.'),
    wrap([45], MEM[0]),
    wrap([], MEM[1]),
    wrap([45], MEM[2]),
    T([46], 'Tải lại trang (F5) khi đang lọc', 'P2', 'Đang ở màn danh sách, vừa chọn Trạng thái = Đang tạo (chưa mở phiếu nào).',
      '1. Nhấn F5.', '—',
      '- Danh sách mở lại với bộ lọc trống, đủ 25 phiếu.\n'
      '- Lưu ý: bộ lọc chỉ được ghi nhớ khi mở màn Chi tiết / Sửa của phiếu rồi quay lại trong 10 phút.'),
    wrap([47], MEM[4]),
    T([48], 'Đổi tài khoản trên cùng trình duyệt', 'P1',
      'Tài khoản A đang lọc Trạng thái = Đang tạo và vừa mở màn Chi tiết một phiếu (bộ lọc đã được ghi nhớ).',
      '1. Đăng xuất A.\n2. Trong vòng 10 phút đăng nhập tài khoản B trên cùng trình duyệt.\n3. ' + MENU, '—',
      '- B thấy ô Trạng thái = Đang tạo còn giữ từ phiên của A (bộ lọc ghi nhớ theo trình duyệt, chưa tách theo tài khoản).\n'
      '- Dữ liệu vẫn chỉ trong phạm vi quyền của B.\n'
      '- Lưu ý: nếu nghiệp vụ yêu cầu bộ lọc tách theo tài khoản thì ghi nhận lỗi.'),
]

# ================================================================== III
S3 = [
    T([49], 'Điều hướng vào màn Tạo', 'P0', PA, '1. Đăng nhập bằng A.\n2. ' + MENU + '\n3. Bấm "Tạo mới".', '—',
      '- Chuyển sang màn Tạo (trang riêng, không phải cửa sổ nổi).\n- Màn danh sách không còn hiển thị.'),
    T([50, 53], 'Tiêu đề và giá trị mặc định', 'P0', PA, TAO, '—',
      '- Tiêu đề "Tạo phiếu yêu cầu vận chuyển, bốc xếp".\n- Góc phải khối Thông tin vận chuyển ghi tên A và thời điểm hiện tại.\n'
      '- Mọi ô trống; ô Khách hàng, Người liên hệ, Số ĐT, Địa điểm giao gợi ý "Lấy theo phiếu YCXH".\n'
      '- Bảng Chi tiết "Không có dữ liệu"; khối File đính kèm chưa có file.'),
    T([51], 'Các khối, trường và nút trên màn Tạo', 'P1', PA, TAO, '—',
      '- Khối Thông tin vận chuyển: Đơn hàng/Hợp đồng, Phiếu YCXH, Khách hàng, Người liên hệ, Số ĐT người liên hệ, Địa '
      'điểm giao hàng, Thời gian vận chuyển, Ghi chú.\n'
      '- Khối Bốc xếp: Tổng số kiện, Phương thức bốc xếp, Địa điểm bốc xếp, Thời gian bốc xếp.\n'
      '- Khối File đính kèm có nút Thêm tài liệu.\n'
      '- Bảng Chi tiết cột STT, Tên hàng, Model, Mã hàng hóa, ĐVT, Số lượng, Số kiện.\n'
      '- Không có ô Mã phiếu (mã sinh khi lưu).'),
    T([52], 'Trường bắt buộc / không bắt buộc', 'P1', PA, TAO, '—',
      '- Chỉ Đơn hàng/Hợp đồng và Phiếu YCXH có dấu * đỏ.\n- Các ô còn lại không có dấu *.\n'
      '- Lưu ý: bảng Chi tiết phải có ít nhất 1 dòng hàng (tự có khi chọn phiếu YCXH).'),
    T([54], 'Các nút lưu và quay lại', 'P1', PA, TAO + '\n3. Rê chuột lên nút Lưu và tiếp tục.', '—',
      '- Cuối màn có Lưu nháp, Gửi duyệt, Lưu và tiếp tục, Quay lại.\n'
      '- Rê chuột lên Lưu và tiếp tục hiện "Lưu nháp phiếu này rồi tiếp tục lập phiếu mới".'),
    T([55, 59], 'Lưu nháp với đầy đủ thông tin hợp lệ', 'P0', PFORM,
      '1. Chọn Thời gian vận chuyển 05/11/2026 08:00.\n2. Nhập Ghi chú "Giao buổi sáng".\n3. Nhập Tổng số kiện 12, Phương '
      'thức bốc xếp "Xe nâng", Địa điểm bốc xếp "Cổng số 2", Thời gian bốc xếp 05/11/2026 07:30.\n'
      '4. Nhập Số kiện 5 dòng: 2, 3, 2, 4, 1.\n5. Thêm tài liệu file bienban.pdf (1 MB).\n6. Bấm Lưu nháp.',
      'Thời gian vận chuyển: 05/11/2026 08:00\nGhi chú: Giao buổi sáng\nTổng số kiện: 12\nPhương thức bốc xếp: Xe nâng\n'
      'Địa điểm bốc xếp: Cổng số 2\nFile: bienban.pdf',
      '- Thông báo "Thêm mới thành công.", về màn danh sách.\n- Phiếu mới ở đầu danh sách, trạng thái Đang tạo.'),
    T([56, 57], 'Chỉ nhập trường bắt buộc', 'P0', PA, TAO + '\n' + CHON + '\n5. Không nhập gì thêm, bấm Lưu nháp.', '—',
      '- Thông báo "Thêm mới thành công.".\n- Mở chi tiết phiếu: Thời gian vận chuyển, Ghi chú, khối Bốc xếp, Số kiện đều trống; '
      'không có khối File đính kèm.'),
    T([58], 'Dữ liệu sau lưu khớp dữ liệu đã nhập', 'P0', 'Vừa lưu phiếu ở case "Lưu nháp với đầy đủ thông tin hợp lệ".',
      '1. Bấm mã phiếu vừa lưu.\n2. Đối chiếu từng ô với dữ liệu đã nhập.', '—',
      '- Đơn hàng/Hợp đồng HĐ_TPE_HN_01, Phiếu YCXH PYCXH-44434 là liên kết.\n'
      '- Khách hàng "KH0001 - Công ty TNHH An Phát", người liên hệ, số ĐT, địa điểm giao đúng theo phiếu YCXH.\n'
      '- Thời gian, Ghi chú, khối Bốc xếp, Số kiện 5 dòng đúng như đã nhập; file bienban.pdf có trong khối File đính kèm.'),
    T([60], 'Lịch sử ghi nhận tạo mới', 'P0', 'Vừa lưu nháp một phiếu mới bằng tài khoản A.',
      '1. Ở danh sách bấm icon Lịch sử của phiếu vừa lưu.', '—',
      '- Có đúng 1 mốc "Tạo mới", "Người thực hiện: Nguyễn Văn A", thời điểm lưu.'),
    T([61, 70], 'Bỏ trống trường bắt buộc', 'P0', PA, TAO + '\n3. Không chọn gì, bấm Gửi duyệt.', '—',
      '- Thông báo góc màn hình "' + CHK + '".\n- Ô Đơn hàng/Hợp đồng và Phiếu YCXH viền đỏ, dưới mỗi ô chữ đỏ "' + REQ + '".\n'
      '- Màn tự cuộn tới ô lỗi đầu tiên; không lưu phiếu.'),
    T([61], 'Chọn phiếu YCXH khi chưa chọn hợp đồng', 'P1', PA, TAO + '\n3. Bấm ô Phiếu YCXH.', '—',
      '- Thông báo "Vui lòng chọn đơn hàng/hợp đồng trước.".\n- Không mở cửa sổ chọn phiếu.'),
    T([62], 'Sai định dạng ô số', 'P1', PFORM,
      '1. Gõ "1.5" vào Số kiện dòng 1.\n2. Gõ "-3" vào Số kiện dòng 2.\n3. Gõ "abc" vào Tổng số kiện.', '1.5\n-3\nabc',
      '- Ô chỉ nhận chữ số: dòng 1 thành "15", dòng 2 thành "3", Tổng số kiện để trống.\n- Không có thông báo lỗi.'),
    T([62], 'File đính kèm sai định dạng / quá dung lượng', 'P1', PFORM + '\nCó file baocao.docx và file PDF 25 MB trên máy.',
      '1. Bấm Thêm tài liệu, Chọn tệp baocao.docx.\n2. Chọn tệp PDF 25 MB.\n3. Chọn tệp bienban.pdf 1 MB.', '—',
      '- Bước 1: báo "File "baocao.docx" không thuộc định dạng cho phép".\n- Bước 2: báo file "vượt quá 20MB".\n'
      '- Bước 3: file tải lên, hiện tên và dung lượng.\n- Rê chuột lên Thêm tài liệu hiện "Chấp nhận pdf, xlsx, xls, jpeg, jpg, png — tối đa 20MB/file".'),
    T([63], 'Ký tự đặc biệt trong ô chữ', 'P1', PFORM,
      '1. Nhập Ghi chú "<b>Giao gấp</b> & \'kho 2\' @#$%".\n2. Bấm Lưu nháp.\n3. Mở chi tiết phiếu.',
      "Ghi chú: <b>Giao gấp</b> & 'kho 2' @#$%",
      '- Lưu thành công.\n- Màn Chi tiết hiện nguyên văn chuỗi đã nhập, chữ KHÔNG bị in đậm, không lỗi hiển thị.'),
    T([64], 'Không có độ dài tối thiểu', 'P2', PFORM, '1. Nhập Phương thức bốc xếp "X".\n2. Bấm Lưu nháp.',
      'Phương thức bốc xếp: X', '- Lưu thành công, Phương thức bốc xếp = "X".'),
    T([65], 'Nhập đúng độ dài tối đa', 'P1', PFORM,
      '1. Dán 255 ký tự vào Phương thức bốc xếp và Địa điểm bốc xếp.\n2. Dán 5000 ký tự vào Ghi chú.\n3. Bấm Lưu nháp.',
      '255 ký tự\n5000 ký tự', '- Lưu thành công.\n- Màn Chi tiết hiện đủ 255 / 5000 ký tự.'),
    T([66], 'Vượt độ dài tối đa', 'P1', PFORM,
      '1. Dán 300 ký tự vào Phương thức bốc xếp.\n2. Dán 5001 ký tự vào Ghi chú.\n3. Bấm Lưu nháp.', '300 ký tự\n5001 ký tự',
      '- Bước 1: ô chỉ giữ 255 ký tự đầu.\n- Bước 3: dưới ô Ghi chú chữ đỏ "Vui lòng nhập tối đa 5000 ký tự.", thông báo "' + CHK + '".\n'
      '- Không lưu, dữ liệu đã nhập còn nguyên.'),
    T([66], 'Số kiện vượt giới hạn', 'P2', PFORM, '1. Nhập Số kiện dòng 1 = 3000000000.\n2. Bấm Lưu nháp.', 'Số kiện: 3000000000',
      '- Dưới ô Số kiện dòng 1: "Giá trị nhập vào không được vượt quá 2147483647.".\n- Thông báo "' + CHK + '", không lưu.'),
    T([67, 82], 'Lập 2 phiếu cùng nội dung (không có trường duy nhất)', 'P1', PA + '\nĐã có phiếu Đang tạo gắn HĐ_TPE_HN_01 + PYCXH-44434.',
      TAO + '\n' + CHON + '\n5. Bấm Lưu nháp.', '—',
      '- Lưu thành công, không báo trùng.\n- Danh sách có 2 phiếu cùng hợp đồng, cùng phiếu YCXH, mã phiếu khác nhau (số chạy tiếp).'),
    T([68], 'Khoảng trắng đầu / cuối được bỏ', 'P2', PFORM,
      '1. Nhập Phương thức bốc xếp "   Xe nâng   ".\n2. Bấm Lưu nháp.\n3. Mở màn Sửa phiếu.', 'Phương thức bốc xếp: "   Xe nâng   "',
      '- Phương thức bốc xếp lưu là "Xe nâng" (không còn khoảng trắng hai đầu).'),
    T([69], 'Ô chỉ có khoảng trắng', 'P2', PFORM, '1. Nhập Ghi chú gồm 5 dấu cách.\n2. Bấm Lưu nháp.\n3. Mở chi tiết.',
      'Ghi chú: 5 dấu cách', '- Lưu thành công, Ghi chú trống.'),
    T([71], 'Lỗi biến mất sau khi sửa', 'P1', PA,
      TAO + '\n3. Bấm Lưu nháp (hiện lỗi bắt buộc).\n4. Chọn HĐ_TPE_HN_01.\n5. Chọn PYCXH-44434.', '—',
      '- Bước 4: viền đỏ và chữ "' + REQ + '" dưới Đơn hàng/Hợp đồng mất ngay; Phiếu YCXH vẫn còn lỗi.\n'
      '- Bước 5: lỗi dưới Phiếu YCXH mất.'),
    T([72], 'Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PFORM,
      '1. Nhập Ghi chú "Lô 1", Số kiện dòng 1 = 2.\n2. Bấm Lưu và tiếp tục.', 'Ghi chú: Lô 1',
      '- Thông báo "Thêm mới thành công.".\n- Phiếu được lưu ở trạng thái Đang tạo (kiểm ở danh sách sau đó).'),
    T([73], 'Lưu và tiếp tục khi thiếu bắt buộc', 'P0',
      PA + '\nĐang ở màn Tạo; đã nhập Ghi chú "Giao buổi sáng", Tổng số kiện 3; chưa chọn Đơn hàng/Hợp đồng và Phiếu YCXH.',
      '1. Bấm Lưu và tiếp tục.', 'Ghi chú: Giao buổi sáng\nTổng số kiện: 3',
      '- Thông báo "' + CHK + '".\n- Chữ đỏ "' + REQ + '" dưới Đơn hàng/Hợp đồng và Phiếu YCXH.\n'
      '- KHÔNG lưu phiếu, KHÔNG làm trống form; Ghi chú, Tổng số kiện vẫn còn.'),
    T([74], 'Lưu và tiếp tục khi sai định dạng', 'P1', PFORM, '1. Nhập Tổng số kiện 3000000000.\n2. Bấm Lưu và tiếp tục.',
      'Tổng số kiện: 3000000000',
      '- Dưới ô Tổng số kiện "Giá trị nhập vào không được vượt quá 2147483647.".\n- Không lưu, form giữ nguyên dữ liệu.'),
    T([75], 'Lưu và tiếp tục 2 lần cùng nội dung', 'P2', PFORM,
      '1. Bấm Lưu và tiếp tục.\n2. Trên form trống, chọn lại HĐ_TPE_HN_01 và PYCXH-44434.\n3. Bấm Lưu và tiếp tục.', '—',
      '- Cả 2 lần đều "Thêm mới thành công.", không báo trùng.\n- Danh sách có thêm 2 phiếu, mã khác nhau.'),
    T([76, 77], 'Sau Lưu và tiếp tục ở lại màn Tạo với form trống', 'P0', PFORM + '\nĐã nhập Ghi chú, Tổng số kiện, 1 file đính kèm.',
      '1. Bấm Lưu và tiếp tục.\n2. Quan sát màn hình.', '—',
      '- Vẫn ở màn "Tạo phiếu yêu cầu vận chuyển, bốc xếp" (không về danh sách).\n'
      '- Mọi ô trống: Đơn hàng/Hợp đồng, Phiếu YCXH, Khách hàng..., khối Bốc xếp, File đính kèm.\n'
      '- Bảng Chi tiết "Không có dữ liệu"; dòng người lập ghi thời điểm mới.'),
    T([78], 'Rời màn sau Lưu và tiếp tục', 'P1', 'Vừa bấm Lưu và tiếp tục thành công, form đang trống, chưa nhập gì thêm.',
      '1. Bấm Quay lại.', '—', '- Về danh sách ngay, KHÔNG hỏi "Thông tin chưa lưu".\n- Phiếu vừa lưu có trong danh sách.'),
    T([79], 'Lưu nháp với dữ liệu hợp lệ', 'P0', PFORM, '1. Nhập Số kiện 2 dòng = 1.\n2. Bấm Lưu nháp.', '—',
      '- Thông báo "Thêm mới thành công.", về danh sách.\n- Phiếu mới mã TPE.YCVC<tháng năm>.NNNNN, trạng thái Đang tạo.'),
    T([80], 'Lưu nháp khi thiếu bắt buộc', 'P0', PA, TAO + '\n3. Chọn HĐ_TPE_HN_01, chưa chọn Phiếu YCXH.\n4. Bấm Lưu nháp.', '—',
      '- Dưới Phiếu YCXH chữ đỏ "' + REQ + '"; thông báo "' + CHK + '".\n- Lưu ý: lưu nháp cũng bắt buộc như gửi duyệt; không lưu.'),
    T([81], 'Lưu nháp khi sai định dạng', 'P1', PFORM, '1. Dán 5001 ký tự vào Ghi chú.\n2. Bấm Lưu nháp.', 'Ghi chú: 5001 ký tự',
      '- Dưới Ghi chú "Vui lòng nhập tối đa 5000 ký tự.".\n- Không lưu, ở lại màn Tạo.'),
    T([83, 85], 'Sau Lưu nháp về danh sách, không hỏi xác nhận', 'P1', PFORM + '\nĐã nhập Ghi chú.', '1. Bấm Lưu nháp.', '—',
      '- Hệ thống tự về màn danh sách (màn Tạo là trang, không còn mở).\n- KHÔNG hiện hộp "Thông tin chưa lưu".'),
    T([84, 91], 'Mở lại màn Tạo sau khi lưu', 'P2', 'Vừa Lưu nháp (hoặc Gửi duyệt) thành công, đang ở danh sách.',
      '1. Bấm "Tạo mới".', '—', '- Form trống hoàn toàn, không còn dữ liệu của phiếu vừa lưu.'),
    T([86], 'Gửi duyệt thành công', 'P0', PFORM, '1. Bấm Gửi duyệt.', '—',
      '- Không hỏi xác nhận; thông báo "Gửi duyệt thành công.", về danh sách.\n- Phiếu trạng thái Chờ duyệt.\n'
      '- G và G2 nhận thông báo "[YCVC] Chờ duyệt: <mã phiếu>..." kèm khách hàng, phiếu xuất, nơi giao, người lập.'),
    T([87], 'Gửi duyệt khi kho chưa có thủ kho', 'P0', PA + '\nPhiếu PYCXH-50001 xuất từ Kho Đà Nẵng chưa khai thủ kho.',
      TAO + '\n3. Chọn HĐ_TPE_HN_01 và PYCXH-50001.\n4. Bấm Gửi duyệt.\n5. Bấm Lưu nháp.', '—',
      '- Bước 3: dưới ô Phiếu YCXH chữ xám "Kho của phiếu này chưa có thủ kho — chỉ lưu nháp được, chưa gửi duyệt được.".\n'
      '- Bước 4: dưới ô Phiếu YCXH "Kho xuất hàng chưa có thủ kho, chưa gửi duyệt được.", không lưu.\n'
      '- Bước 5: lưu nháp thành công.'),
    T([87, 61], 'Gửi duyệt khi bảng Chi tiết trống', 'P1', PA + '\nPhiếu PYCXH-50002 có khách hàng nhưng mọi dòng hàng số lượng 0.',
      TAO + '\n3. Chọn HĐ_TPE_HN_01 và PYCXH-50002.\n4. Bấm Gửi duyệt.', '—',
      '- Bước 3: bảng Chi tiết "Không có dữ liệu".\n- Bước 4: dưới bảng chữ đỏ "' + REQ + '", thông báo "' + CHK + '", không lưu.'),
    T([88], 'Gửi duyệt khi sai định dạng', 'P1', PFORM, '1. Nhập Số kiện dòng 3 = 9999999999.\n2. Bấm Gửi duyệt.',
      'Số kiện: 9999999999', '- Dưới ô Số kiện dòng 3 "Giá trị nhập vào không được vượt quá 2147483647.".\n- Không lưu, thủ kho không nhận thông báo.'),
    T([89], 'Gửi duyệt phiếu thứ 2 cho cùng phiếu YCXH', 'P2', PA + '\nĐã có phiếu Chờ duyệt gắn PYCXH-44434.',
      TAO + '\n' + CHON + '\n5. Bấm Gửi duyệt.', '—',
      '- Gửi duyệt thành công, không báo trùng.\n- Có 2 phiếu Chờ duyệt cùng PYCXH-44434; G nhận thêm 1 thông báo.'),
    T([90, 92], 'Sau Gửi duyệt về danh sách, không hỏi xác nhận', 'P1', PFORM, '1. Bấm Gửi duyệt.', '—',
      '- Tự về danh sách, KHÔNG hiện hộp "Thông tin chưa lưu".'),
    T([93], 'Rời màn khi chưa nhập gì', 'P1', PA, TAO + '\n3. Bấm Quay lại.', '—', '- Về danh sách ngay, không hỏi xác nhận.'),
    T([94, 96], 'Rời màn khi đã nhập, chọn Thoát', 'P0', PFORM + '\nĐã nhập Ghi chú "Giao gấp".', '1. Bấm Quay lại.\n2. Bấm Thoát.', '—',
      '- Bước 1: hộp "Thông tin chưa lưu" nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", nút Thoát và Ở lại.\n'
      '- Bước 2: về danh sách, KHÔNG có phiếu mới.'),
    T([97], 'Rời màn khi đã nhập, chọn Ở lại', 'P1', PFORM + '\nĐã nhập Ghi chú "Giao gấp".', '1. Bấm Quay lại.\n2. Bấm Ở lại.', '—',
      '- Hộp đóng, vẫn ở màn Tạo.\n- Hợp đồng, phiếu YCXH, Ghi chú "Giao gấp" còn nguyên.'),
    T([95], 'Đóng tab / tải lại trình duyệt khi có dữ liệu chưa lưu', 'P2', PFORM + '\nĐã nhập Ghi chú.',
      '1. Nhấn F5 (hoặc bấm đóng tab trình duyệt).', '—',
      '- Trình duyệt hỏi xác nhận rời trang.\n- Chọn ở lại thì dữ liệu còn nguyên.\n'
      '- Lưu ý: màn Tạo là trang riêng nên không có nút (x) hay thao tác click ra ngoài.'),
    T([98], 'Nhập rồi xóa hết', 'P2', PA, TAO + '\n3. Gõ "abc" vào Ghi chú, Phương thức bốc xếp.\n4. Xóa hết chữ đã gõ.\n5. Bấm Quay lại.', '—',
      '- Về danh sách ngay, không hỏi xác nhận (dữ liệu đã trở về như lúc mở).'),
    T([99], 'Đổi rồi khôi phục giá trị ban đầu', 'P2', PA,
      TAO + '\n3. Gõ "Giao sáng" vào Ghi chú, sửa thành "Giao chiều".\n4. Xóa hết Ghi chú.\n5. Bấm Quay lại.', '—',
      '- Về danh sách ngay, không hỏi xác nhận.'),
    T([100], 'Không thao tác lâu rồi rời màn', 'P2', PFORM + '\nĐã nhập Ghi chú.',
      '1. Để màn đứng yên 30 phút.\n2. Bấm Quay lại.\n3. Bấm Ở lại.', '—',
      '- Bước 2: vẫn hiện hộp "Thông tin chưa lưu" (không có giới hạn thời gian tự hủy).\n- Bước 3: dữ liệu còn nguyên.'),
    T([101], 'Bấm nút lưu liên tục', 'P0', PFORM, '1. Bấm Lưu nháp 3 lần thật nhanh.', '—',
      '- Nút bị khóa trong lúc đang lưu.\n- Chỉ tạo đúng 1 phiếu.'),
    T([102], 'Hai tài khoản tạo cùng lúc', 'P1', 'A và B cùng mở màn Tạo, cùng chọn HĐ_TPE_HN_01 và PYCXH-44434.',
      '1. A và B bấm Lưu nháp cùng lúc.', '—', '- Cả 2 phiếu đều lưu.\n- Hai mã phiếu khác nhau, số chạy liên tiếp, không trùng.'),
]

# ================================================================== IV
S4 = [
    T([103], 'Mở màn Sửa từ danh sách', 'P0', PEDIT, '1. Đăng nhập bằng A.\n2. ' + MENU + '\n3. Bấm icon Sửa ở dòng 00006.', '—',
      '- Mở màn "Sửa phiếu yêu cầu vận chuyển, bốc xếp: TPE.YCVC1026.00006", tiêu đề kèm nhãn xám Đang tạo.'),
    T([103], 'Mở màn Sửa từ màn Chi tiết', 'P1', PEDIT, '1. Bấm mã 00006.\n2. Bấm nút Sửa.', '—', '- Mở đúng màn Sửa phiếu 00006.'),
    T([104], 'Dữ liệu điền sẵn đúng', 'P0', PEDIT + '\nPhiếu có 1 file bienban.pdf, Số kiện dòng 1 = 2.', '1. Mở màn Sửa phiếu 00006.', '—',
      '- Mã phiếu, Đơn hàng/Hợp đồng, Phiếu YCXH, khách hàng, người liên hệ, địa điểm giao đúng như đã lưu.\n'
      '- Ghi chú "Giao buổi sáng", Tổng số kiện 3, Số kiện dòng 1 = 2; file bienban.pdf có trong danh sách file.'),
    T([105], 'Trường được / không được sửa', 'P1', PEDIT, '1. Mở màn Sửa phiếu 00006.\n2. Thử bấm vào từng ô.', '—',
      '- Sửa được: Đơn hàng/Hợp đồng, Phiếu YCXH, Thời gian vận chuyển, Ghi chú, khối Bốc xếp, Số kiện, file đính kèm.\n'
      '- Không sửa được (chỉ đọc): Mã phiếu, Khách hàng, Người liên hệ, Số ĐT, Địa điểm giao hàng, Tên hàng, Model, Mã '
      'hàng hóa, ĐVT, Số lượng.'),
    T([106], 'Các nút ở màn Sửa', 'P1', PEDIT, '1. Mở màn Sửa phiếu 00006.', '—',
      '- Có Lưu nháp, Gửi duyệt, Quay lại.\n- KHÔNG có nút Lưu và tiếp tục.'),
    T([107], 'Sửa một trường', 'P0', PEDIT, '1. Mở màn Sửa phiếu 00006.\n2. Đổi Ghi chú thành "Giao buổi chiều".\n3. Bấm Lưu nháp.',
      'Ghi chú: Giao buổi chiều', '- Thông báo "Cập nhật thành công.", về danh sách.\n- Phiếu vẫn Đang tạo.'),
    T([108, 112], 'Sửa nhiều trường', 'P0', PEDIT,
      '1. Mở màn Sửa phiếu 00006.\n2. Đổi Ghi chú, Tổng số kiện = 5, Số kiện dòng 1 = 3, Thời gian vận chuyển 06/11/2026 09:00.\n3. Bấm Lưu nháp.\n'
      '4. Mở Lịch sử phiếu 00006.', 'Ghi chú: Giao buổi chiều\nTổng số kiện: 5\nSố kiện dòng 1: 3',
      '- "Cập nhật thành công.".\n- Lịch sử có 1 mốc "Thay đổi thông tin" liệt kê Ghi chú, Tổng số kiện, Thời gian vận chuyển cũ / mới '
      'và dòng hàng đổi Số kiện.'),
    T([109], 'Lưu không đổi giá trị nào', 'P1', PEDIT, '1. Mở màn Sửa phiếu 00006.\n2. Không đổi gì, bấm Lưu nháp.\n3. Mở Lịch sử.', '—',
      '- Thông báo "Cập nhật thành công.".\n- Lịch sử KHÔNG thêm mốc "Thay đổi thông tin".'),
    T([110], 'Dữ liệu sau khi lưu sửa', 'P0', 'Vừa sửa phiếu 00006 ở case "Sửa nhiều trường".',
      '1. Bấm mã 00006 mở chi tiết.', '—', '- Ghi chú, Tổng số kiện 5, Số kiện dòng 1 = 3, Thời gian vận chuyển 06/11/2026 09:00 đúng giá trị mới.'),
    T([111], 'Ngày / người cập nhật sau khi sửa', 'P1', PEDIT + '\nNgày cập nhật hiện là 20/10/2026 10:00.',
      '1. Sửa Ghi chú phiếu 00006, Lưu nháp.\n2. Quan sát dòng 00006 trên danh sách.', '—',
      '- Ngày cập nhật đổi sang thời điểm vừa lưu; Người cập nhật "Nguyễn Văn A - KD1".\n- Ngày tạo, Người tạo giữ nguyên.'),
    T([112], 'Lịch sử ghi giá trị cũ và mới', 'P0', PEDIT, '1. Sửa Ghi chú "Giao buổi sáng" thành "Giao buổi chiều", Lưu nháp.\n2. Mở Lịch sử.', '—',
      '- Mốc mới nhất "Thay đổi thông tin", người thực hiện A.\n- Dòng "Ghi chú: Giao buổi sáng" sang "Giao buổi chiều".'),
    T([], 'Sửa phiếu Từ chối rồi gửi duyệt lại', 'P0', 'Phiếu TPE.YCVC1026.00001 Từ chối do A lập, lý do "Sai địa điểm".',
      '1. Mở màn Sửa phiếu 00001.\n2. Đổi Ghi chú.\n3. Bấm Gửi duyệt.', '—',
      '- Bước 1: màn Sửa hiện ô Lý do từ chối "Sai địa điểm" (chỉ đọc).\n- Bước 3: "Gửi duyệt thành công.", phiếu Chờ duyệt.\n'
      '- Lý do từ chối, Người duyệt, Ngày duyệt cũ bị xóa.\n- Lịch sử: 1 mốc Thay đổi thông tin + 1 mốc Thay đổi trạng thái (Từ chối sang Chờ duyệt).'),
    T([113], 'Bỏ trống trường bắt buộc khi sửa', 'P0', PEDIT,
      '1. Mở màn Sửa phiếu 00006.\n2. Bấm dấu × ở ô Đơn hàng/Hợp đồng.\n3. Bấm Lưu nháp.', '—',
      '- Bước 2: Phiếu YCXH, khách hàng, người liên hệ, địa điểm giao, bảng Chi tiết cũng bị xóa.\n'
      '- Bước 3: "' + REQ + '" dưới Đơn hàng/Hợp đồng và Phiếu YCXH, thông báo "' + CHK + '", không lưu.'),
    T([114], 'Sai định dạng khi sửa', 'P2', PEDIT, '1. Mở màn Sửa phiếu 00006.\n2. Gõ "12a" vào Tổng số kiện.', 'Tổng số kiện: 12a',
      '- Ô chỉ giữ "12", ký tự chữ bị bỏ ngay khi gõ.'),
    T([115], 'Vượt giới hạn khi sửa', 'P1', PEDIT,
      '1. Mở màn Sửa phiếu 00006.\n2. Dán 5001 ký tự vào Ghi chú, nhập Số kiện dòng 2 = 3000000000.\n3. Bấm Lưu nháp.', '—',
      '- Dưới Ghi chú "Vui lòng nhập tối đa 5000 ký tự."; dưới Số kiện dòng 2 "Giá trị nhập vào không được vượt quá 2147483647.".\n'
      '- Không lưu; dữ liệu cũ của phiếu không đổi.'),
    T([116], 'Chọn phiếu YCXH đã dùng ở phiếu khác', 'P2', PEDIT + '\nPhiếu 00004 (người khác lập) gắn PYCXH-44434; phiếu 00006 đang gắn PYCXH-44500.',
      '1. Mở màn Sửa phiếu 00006.\n2. Chọn lại Phiếu YCXH = PYCXH-44434.\n3. Bấm Lưu nháp.', '—',
      '- Lưu thành công, không báo trùng (phiếu không có trường duy nhất).\n- Bảng Chi tiết thay bằng dòng hàng của PYCXH-44434.'),
    T([117, 118], 'Thông báo lỗi và lỗi biến mất khi sửa hợp lệ', 'P1', PEDIT,
      '1. Mở màn Sửa, bấm × ô Đơn hàng/Hợp đồng, bấm Lưu nháp.\n2. Chọn lại HĐ_TPE_HN_01 và một phiếu YCXH.', '—',
      '- Bước 1: viền đỏ, chữ đỏ "' + REQ + '" dưới ô, thông báo góc màn hình "' + CHK + '".\n'
      '- Bước 2: lỗi dưới từng ô mất ngay khi ô có giá trị.'),
    T([119], 'Mở màn Sửa không thay đổi rồi rời đi', 'P1', PEDIT, '1. Mở màn Sửa phiếu 00006.\n2. Bấm Quay lại.', '—',
      '- Về danh sách ngay, không hỏi xác nhận.'),
    T([120], 'Đổi rồi trả về giá trị ban đầu', 'P2', PEDIT,
      '1. Mở màn Sửa.\n2. Đổi Ghi chú thành "Giao chiều".\n3. Sửa lại đúng "Giao buổi sáng".\n4. Bấm Quay lại.', '—',
      '- Về danh sách ngay, không hỏi xác nhận.'),
    T([121, 122], 'Rời màn Sửa khi đã đổi, chọn Thoát', 'P0', PEDIT,
      '1. Mở màn Sửa, đổi Ghi chú thành "Giao chiều".\n2. Bấm Quay lại.\n3. Bấm Thoát.', '—',
      '- Bước 2: hộp "Thông tin chưa lưu".\n- Bước 3: về danh sách, không lưu.'),
    T([123], 'Rời màn Sửa khi đã đổi, chọn Ở lại', 'P1', PEDIT,
      '1. Mở màn Sửa, đổi Ghi chú.\n2. Bấm Quay lại.\n3. Bấm Ở lại.', '—', '- Vẫn ở màn Sửa, Ghi chú mới còn nguyên.'),
    T([124], 'Hủy sửa không lưu dữ liệu', 'P0', PEDIT,
      '1. Mở màn Sửa, đổi Ghi chú thành "Giao chiều", Tổng số kiện 9.\n2. Bấm Quay lại, chọn Thoát.\n3. Mở chi tiết phiếu 00006.', '—',
      '- Ghi chú vẫn "Giao buổi sáng", Tổng số kiện vẫn 3.'),
    T([125], 'Không ghi lịch sử khi hủy / không thay đổi', 'P1', PEDIT + '\nLịch sử phiếu 00006 đang có 2 mốc.',
      '1. Mở màn Sửa, đổi Ghi chú rồi Quay lại, Thoát.\n2. Mở màn Sửa, Quay lại ngay.\n3. Mở Lịch sử phiếu 00006.', '—',
      '- Lịch sử vẫn đúng 2 mốc, không có mốc mới.'),
    T([127], 'Phiếu bị xóa trong lúc đang sửa', 'P1', PEDIT + '\nA mở màn Sửa phiếu 00006 ở tab 1.',
      '1. Ở tab 2, A xóa phiếu 00006.\n2. Quay lại tab 1, đổi Ghi chú, bấm Lưu nháp.', '—',
      '- Hệ thống báo lỗi không tìm thấy phiếu (hiện câu tiếng Anh "Item Not Found!"), không tạo phiếu mới.\n'
      '- Vẫn ở màn Sửa.\n- Lưu ý: câu báo lỗi đang là tiếng Anh — ghi nhận lỗi hiển thị.'),
    T([128], 'Phiếu đổi trạng thái ở tab khác khi đang sửa', 'P1',
      PEDIT + '\nA mở màn Sửa phiếu 00006 ở tab 1.\nỞ tab 2, A mở Sửa cùng phiếu và bấm Gửi duyệt (phiếu sang Chờ duyệt).',
      '1. Quay lại tab 1, bấm Lưu nháp.', '—',
      '- Báo "' + CONFLICT + '".\n- Chuyển sang màn Chi tiết phiếu, trạng thái Chờ duyệt; dữ liệu tab 1 không được lưu.'),
    T([128], 'Hai lượt lưu nháp đồng thời', 'P2', PEDIT + '\nA mở màn Sửa phiếu 00006 ở 2 tab.',
      '1. Tab 1 đổi Ghi chú "Tab 1", Lưu nháp.\n2. Tab 2 đổi Ghi chú "Tab 2", Lưu nháp.\n3. Mở chi tiết và Lịch sử.', '—',
      '- Cả 2 lần đều "Cập nhật thành công.".\n- Ghi chú cuối cùng là "Tab 2" (lượt lưu sau ghi đè).\n- Lịch sử có 2 mốc Thay đổi thông tin theo đúng thứ tự.'),
    T([129], 'Phiếu đang chờ duyệt / đã duyệt không sửa được', 'P0',
      'A lập phiếu 00004 (Chờ duyệt) và 00003 (Đã duyệt); A có đường link màn Sửa của 00004 lưu từ trước.',
      '1. Quan sát cột Hành động 2 dòng.\n2. Dán đường link màn Sửa phiếu 00004 vào thanh địa chỉ.', '—',
      '- Bước 1: không có icon Sửa.\n- Bước 2: hệ thống chuyển sang màn Chi tiết phiếu 00004, không mở form sửa.'),
    T([], 'Xóa file đã lưu ở màn Sửa', 'P1', PEDIT + '\nPhiếu có file bienban.pdf.',
      '1. Mở màn Sửa.\n2. Bấm icon Xóa của file bienban.pdf.\n3. Bấm đồng ý.\n4. Bấm Quay lại.', '—',
      '- Bước 2: hỏi "Bạn có chắc muốn xóa file đính kèm này?".\n- Bước 3: báo "Xóa file thành công", file biến mất ngay (không cần bấm lưu).\n'
      '- Lịch sử có mốc Thay đổi thông tin ghi file đã xóa.'),
]

# ================================================================== V
S5 = [
    T([130], 'Điều kiện hiện nút Xóa', 'P0', 'A lập 00006 (Đang tạo), 00001 (Từ chối), 00004 (Chờ duyệt), 00003 (Đã duyệt).',
      '1. Đăng nhập bằng A.\n2. ' + MENU + '\n3. Quan sát icon Xóa.\n4. Mở chi tiết 00006 và 00004.', '—',
      '- Icon Xóa (thùng rác đỏ) chỉ có ở 00006, 00001.\n- Màn Chi tiết 00006 có nút Xóa; 00004 không có.'),
    T([131, 132], 'Hộp xác nhận xóa', 'P0', 'A lập phiếu TPE.YCVC1026.00005 Đang tạo.', '1. Bấm icon Xóa ở dòng 00005.', '—',
      '- Hộp "Xác nhận xóa" kèm icon cảnh báo.\n- Nội dung "Bạn có chắc muốn xóa phiếu yêu cầu vận chuyển \'TPE.YCVC1026.00005\'?".\n'
      '- Nút Xóa màu đỏ và nút Hủy.'),
    T([133, 139, 140], 'Xóa phiếu thành công', 'P0', 'A thấy 4 phiếu; đang lọc Trạng thái = Đang tạo (2 phiếu 00005, 00006).',
      '1. Bấm icon Xóa ở dòng 00005.\n2. Bấm Xóa.', '—',
      '- Thông báo "Xóa thành công.".\n- Phiếu 00005 biến mất; bộ lọc Đang tạo giữ nguyên, còn 1 phiếu.\n- Tổng số dưới bảng giảm 1.'),
    T([134], 'Hủy xóa', 'P1', 'A lập phiếu 00005 Đang tạo.', '1. Bấm icon Xóa, bấm Hủy.\n2. Bấm icon Xóa, bấm (x).\n3. Bấm icon Xóa, bấm ra ngoài hộp.', '—',
      '- Cả 3 cách: hộp đóng, phiếu 00005 còn nguyên trạng thái Đang tạo.'),
    T([135], 'Không xóa được phiếu đã tác động sang dữ liệu khác', 'P1',
      'A lập phiếu 00003 Đã duyệt (đã đổi ô Vận chuyển của PYCXH-44000) và 00004 Chờ duyệt.', '1. Quan sát cột Hành động và màn Chi tiết 2 phiếu.', '—',
      '- Không có icon / nút Xóa ở cả 2 phiếu.'),
    T([136], 'Xóa phiếu có dòng hàng', 'P1', 'A lập phiếu 00006 Đang tạo có 5 dòng hàng; A giữ đường link chi tiết 00006.',
      '1. Xóa phiếu 00006.\n2. Dán lại đường link chi tiết 00006.', '—',
      '- Bước 1: xóa thành công, không chặn vì có dòng hàng.\n- Bước 2: trang không tìm thấy (phiếu và dòng hàng đã xóa).'),
    T([138], 'Phiếu đã bị xóa ở tab khác', 'P2', 'A mở danh sách ở 2 tab, cùng thấy phiếu 00005.',
      '1. Tab 2 xóa phiếu 00005.\n2. Tab 1 bấm icon Xóa phiếu 00005, bấm Xóa.', '—',
      '- Tab 1 báo lỗi không tìm thấy phiếu (hiện câu tiếng Anh "Item Not Found!").\n- Lưu ý: câu báo lỗi đang là tiếng Anh — ghi nhận lỗi hiển thị.'),
    T([141], 'Dữ liệu liên quan sau khi xóa', 'P1', 'A lập phiếu 00005 Đang tạo gắn PYCXH-44434.',
      '1. Xóa phiếu 00005.\n2. Tạo mới, chọn HĐ_TPE_HN_01, mở ô Phiếu YCXH.\n3. Mở màn Phiếu yêu cầu xuất hàng PYCXH-44434.', '—',
      '- Bước 2: PYCXH-44434 vẫn có trong cửa sổ chọn.\n- Bước 3: phiếu YCXH không đổi gì (ô Vận chuyển giữ nguyên).'),
    T([], 'Xóa từ màn Chi tiết', 'P1', 'A lập phiếu 00001 Từ chối.', '1. Mở chi tiết 00001.\n2. Bấm Xóa, bấm Xóa ở hộp xác nhận.', '—',
      '- Thông báo "Xóa thành công.", quay về màn danh sách.\n- Phiếu 00001 không còn.'),
]

# ================================================================== VI
S6 = [
    T([162], 'Mở cửa sổ lịch sử từ danh sách', 'P0', PHIS, M + '\n3. Bấm icon Lịch sử ở dòng 00003.', '—',
      '- Cửa sổ "Lịch sử thay đổi: TPE.YCVC1026.00003".\n- Hiện đủ 8 mốc.'),
    T([163, 165, 166, 167, 168], 'Nội dung từng mốc lịch sử', 'P0', PHIS, '1. Mở Lịch sử phiếu 00003.\n2. Quan sát một mốc Thay đổi thông tin và một mốc Thay đổi trạng thái.', '—',
      '- Mỗi mốc có: thời điểm thao tác, tên hành động (màu theo loại), dòng "Người thực hiện: <họ tên>" kèm phòng ban.\n'
      '- Thay đổi thông tin: từng trường giá trị cũ sang mới.\n- Thay đổi trạng thái: "Chờ duyệt" sang "Đã duyệt".'),
    T([164], 'Mốc mới nhất lên trên', 'P1', PHIS, '1. Mở Lịch sử phiếu 00003.', '—',
      '- Mốc trên cùng là Thay đổi trạng thái Chờ duyệt sang Đã duyệt (mới nhất); mốc dưới cùng là Tạo mới.'),
    T([169], 'Lọc theo loại hành động', 'P1', PHIS, '1. Mở Lịch sử 00003.\n2. Bấm Bộ lọc.\n3. Chọn Loại hành động = Thay đổi trạng thái.',
      'Loại hành động: Thay đổi trạng thái', '- Lọc ngay, chỉ còn các mốc Thay đổi trạng thái.'),
    T([170], 'Lọc theo người thực hiện', 'P1', PHIS, '1. Mở Lịch sử 00003, bấm Bộ lọc.\n2. Chọn Người thực hiện = G.', 'Người thực hiện: G',
      '- Chỉ còn mốc do G thực hiện (mốc duyệt).'),
    T([171], 'Lọc theo thời gian', 'P1', PHIS + '\n3 mốc ngày 15/10/2026, các mốc khác ngày khác.',
      '1. Mở Lịch sử 00003, bấm Bộ lọc.\n2. Chọn Từ ngày 15/10/2026, Đến ngày 15/10/2026.', 'Từ ngày: 15/10/2026\nĐến ngày: 15/10/2026',
      '- Chỉ còn 3 mốc ngày 15/10/2026.'),
    T([172], 'Kết hợp nhiều ô lọc lịch sử', 'P2', PHIS,
      '1. Bấm Bộ lọc.\n2. Chọn Loại hành động = Thay đổi thông tin, Người thực hiện = A.', '—',
      '- Chỉ còn mốc Thay đổi thông tin do A thực hiện.'),
    T([173], 'Lọc lịch sử không có kết quả', 'P2', PHIS, '1. Bấm Bộ lọc.\n2. Chọn Từ ngày 01/01/2020, Đến ngày 02/01/2020.', '—',
      '- Hiện "Không có lịch sử phù hợp bộ lọc.".'),
    T([174], 'Làm mới bộ lọc lịch sử', 'P2', 'Đang lọc lịch sử theo Loại hành động và Người thực hiện.', '1. Bấm Làm mới trong vùng lọc.', '—',
      '- 4 ô lọc về trống, hiện lại đủ 8 mốc.'),
    T([175], 'Đóng / mở vùng bộ lọc lịch sử', 'P2', PHIS, '1. Bấm Bộ lọc.\n2. Bấm Bộ lọc lần nữa.', '—',
      '- Bước 1: hiện 4 ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày.\n- Bước 2: vùng lọc thu gọn.'),
    T([176], 'Ghi nhận khi tạo mới', 'P0', 'A vừa Gửi duyệt một phiếu mới.', '1. Mở Lịch sử phiếu đó.', '—',
      '- Có mốc "Tạo mới" người thực hiện A.\n- Lưu ý: phiếu tạo thẳng ở trạng thái Chờ duyệt chỉ có mốc Tạo mới.'),
    T([177], 'Ghi nhận sửa một trường', 'P1', PEDIT, '1. Sửa Tổng số kiện 3 thành 4, Lưu nháp.\n2. Mở Lịch sử.', '—',
      '- Mốc "Thay đổi thông tin" chỉ có dòng "Tổng số kiện: 3" sang "4".'),
    T([178, 183], 'Ghi nhận đổi nhiều thông tin cùng lúc', 'P1', PEDIT,
      '1. Sửa Ghi chú, Số kiện dòng 2 = 6, thêm file phieu.xlsx.\n2. Lưu nháp.\n3. Mở Lịch sử.', '—',
      '- Chỉ 1 mốc "Thay đổi thông tin" gồm Ghi chú cũ / mới, dòng hàng đổi Số kiện, file thêm phieu.xlsx.'),
    T([182], 'Không ghi lịch sử khi lưu không đổi', 'P1', PEDIT + '\nLịch sử đang có 2 mốc.', '1. Mở màn Sửa, bấm Lưu nháp ngay.\n2. Mở Lịch sử.', '—',
      '- Vẫn 2 mốc, không sinh mốc rỗng.'),
    T([167], 'Ghi nhận đổi trạng thái khi gửi duyệt', 'P1', PEDIT, '1. Mở màn Sửa, không đổi gì, bấm Gửi duyệt.\n2. Mở Lịch sử.', '—',
      '- Có mốc "Thay đổi trạng thái" Đang tạo sang Chờ duyệt.\n- Không có mốc Thay đổi thông tin rỗng.'),
    T([184], 'Đóng cửa sổ lịch sử', 'P1', PHIS, '1. Mở Lịch sử, bấm Đóng.\n2. Mở lại, bấm (x).\n3. Mở lại, bấm ra ngoài cửa sổ.', '—',
      '- Cả 3 cách đều đóng cửa sổ.'),
    T([185], 'Danh sách giữ trạng thái sau khi đóng lịch sử', 'P1', P25 + '\nĐang ở trang 2, lọc Trạng thái = Đã duyệt, sắp xếp theo Mã phiếu.',
      '1. Mở Lịch sử một phiếu.\n2. Đóng cửa sổ.', '—', '- Danh sách vẫn ở trang 2, giữ bộ lọc và sắp xếp.'),
    T([195], 'Lịch sử ở màn Chi tiết', 'P2', PHIS, '1. Mở chi tiết 00003.\n2. Bấm Xem lịch sử.\n3. Bấm Thu gọn.', '—',
      '- Khối Lịch sử mặc định thu gọn.\n- Bước 2: hiện cùng 8 mốc như cửa sổ ở danh sách, có nút Làm mới.\n- Bước 3: khối thu gọn.'),
    T([], 'Phiếu cũ chưa có lịch sử', 'P2', 'Phiếu TPE.YCVC0926.00010 lập từ hệ thống ERP, chưa từng thao tác trên hệ thống mới.',
      '1. Mở Lịch sử phiếu đó.', '—', '- Hiện "Chưa có lịch sử thao tác nào.".'),
]

# ================================================================== VII
S7 = [
    T([186], 'Mở chi tiết bằng mã phiếu', 'P0', P25, M + '\n3. Bấm mã TPE.YCVC1026.00004.', '—',
      '- Mở màn Chi tiết của phiếu 00004 (trang riêng).'),
    T([187], 'Tiêu đề màn chi tiết', 'P1', P25, '1. Mở chi tiết 00004.', '—',
      '- Tiêu đề "Chi tiết phiếu yêu cầu vận chuyển, bốc xếp: TPE.YCVC1026.00004" kèm nhãn cam Chờ duyệt.\n'
      '- Tab trình duyệt ghi cùng tên, không kèm nhãn.'),
    T([188, 189, 190], 'Đầy đủ trường và khớp dữ liệu', 'P0', 'Phiếu 00004 lập với đủ thông tin vận chuyển, bốc xếp, 1 file, 5 dòng hàng.',
      '1. Đối chiếu dòng 00004 trên danh sách.\n2. Mở chi tiết 00004, đối chiếu với dữ liệu khi tạo.', '—',
      '- Có đủ khối Thông tin vận chuyển, Bốc xếp, File đính kèm, Chi tiết (cột Số kiện).\n'
      '- Mã phiếu, số hợp đồng, khách hàng khớp danh sách.\n- Mọi giá trị khớp dữ liệu đã nhập khi tạo.'),
    T([191, 192], 'Chỉ đọc, không có nút Lưu', 'P0', 'Phiếu TPE.YCVC1026.00004 Chờ duyệt.', '1. Mở chi tiết 00004.\n2. Thử bấm vào các ô.', '—',
      '- Mọi ô xám, không sửa được.\n- Không có nút Lưu nháp, Gửi duyệt.'),
    T([193], 'Nút theo vai trò khi xem phiếu Chờ duyệt', 'P1', PG, '1. Đăng nhập A, mở chi tiết 00004.\n2. Đăng nhập G, mở chi tiết 00004.', '—',
      '- A (người lập): chỉ có Quay lại.\n- G (thủ kho): có Duyệt, Từ chối, Quay lại.'),
    T([], 'Phiếu Từ chối hiện lý do', 'P1', 'Phiếu 00001 Từ chối, lý do "Sai địa điểm".', '1. Mở chi tiết 00001.', '—',
      '- Có Người duyệt, Ngày duyệt, Lý do từ chối "Sai địa điểm".'),
    T([195], 'Khu vực lịch sử ở màn chi tiết', 'P1', PHIS, '1. Mở chi tiết 00003.\n2. Bấm Xem lịch sử.', '—',
      '- Khối Lịch sử thu gọn mặc định; bấm Xem lịch sử mới nạp và hiện các mốc.'),
    T([196], 'Đóng màn chi tiết', 'P2', P25, '1. Mở chi tiết 00004.\n2. Bấm Quay lại.', '—', '- Về màn danh sách.'),
    T([197], 'Giữ bộ lọc khi quay lại danh sách', 'P0', P25 + '\nĐang lọc Trạng thái = Đã duyệt, xem trang 2.',
      '1. Bấm mã một phiếu ở trang 2.\n2. Trong 10 phút bấm Quay lại.', '—',
      '- Danh sách giữ Trạng thái = Đã duyệt.\n- Danh sách mở lại ở trang 1 (số trang không được ghi nhớ).'),
    T([], 'Liên kết hợp đồng và phiếu YCXH', 'P2', 'Phiếu 00004 gắn HĐ_TPE_HN_01, PYCXH-44434.',
      '1. Mở chi tiết 00004.\n2. Bấm Đơn hàng/Hợp đồng.\n3. Bấm Phiếu YCXH.', '—',
      '- Mỗi liên kết mở chứng từ ở tab mới; màn chi tiết giữ nguyên.'),
    T([], 'File đính kèm ở màn chi tiết', 'P2', 'Phiếu 00004 có file bienban.pdf; phiếu 00006 không có file.',
      '1. Mở chi tiết 00004, bấm Xem trước và Tải xuống file.\n2. Mở chi tiết 00006.', '—',
      '- Bước 1: xem trước được file pdf, tải được file; không có nút xóa / thêm file.\n- Bước 2: không có khối File đính kèm.'),
]

# ================================================================== VIII
S8 = [
    T([198], 'Mở cửa sổ tùy chỉnh cột', 'P1', P25, M + '\n3. Bấm icon Cấu hình cột hiển thị.', '—',
      '- Cửa sổ "Tuỳ chỉnh cột" kèm dòng hướng dẫn, nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng.'),
    T([199, 200], 'Danh sách cột và cột chọn mặc định', 'P1', 'Tài khoản chưa từng tùy chỉnh cột.', '1. Mở cửa sổ Tuỳ chỉnh cột.', '—',
      '- 13 cột: STT, Mã phiếu, Số hợp đồng/đơn hàng, Phiếu YCXH, Khách hàng, Ngày tạo, Người tạo, Ngày cập nhật, Người '
      'cập nhật, Ngày duyệt, Người duyệt, Trạng thái, Hành động.\n- Tích sẵn 12 cột; riêng Phiếu YCXH không tích.'),
    T([201], 'Hiện cột đang ẩn', 'P1', P25, '1. Mở Tuỳ chỉnh cột.\n2. Tích Phiếu YCXH, bấm Lưu.', '—',
      '- Báo "Cập nhật thành công", cửa sổ đóng.\n- Bảng có cột Phiếu YCXH, mã là liên kết mở tab mới.'),
    T([202], 'Ẩn cột', 'P1', P25, '1. Mở Tuỳ chỉnh cột.\n2. Bỏ tích Người cập nhật, Ngày cập nhật, bấm Lưu.', '—',
      '- Bảng không còn 2 cột đó.'),
    T([203], 'Cột bắt buộc không ẩn được', 'P0', P25, '1. Mở Tuỳ chỉnh cột.\n2. Bấm ô tích của STT, Mã phiếu, Hành động.\n3. Rê chuột lên các dòng đó.', '—',
      '- 3 ô tích xám, luôn tích, không bỏ được.\n- STT, Mã phiếu: "Cột bắt buộc — không thể ẩn hoặc đổi vị trí".\n'
      '- Hành động: "Cột bắt buộc — không thể ẩn, kéo để đổi vị trí".'),
    T([204], 'Kéo thả đổi thứ tự cột', 'P1', P25, '1. Mở Tuỳ chỉnh cột.\n2. Kéo biểu tượng kéo thả của Trạng thái lên ngay sau Mã phiếu.\n3. Bấm Lưu.', '—',
      '- Bảng hiện cột Trạng thái ngay sau Mã phiếu.'),
    T([205], 'Cột cố định', 'P2', P25, '1. Mở Tuỳ chỉnh cột, thử kéo STT, Mã phiếu; kéo Hành động lên đầu danh sách cột tự do.\n'
      '2. Đóng cửa sổ, cuộn ngang bảng.', '—',
      '- STT, Mã phiếu không kéo được; Hành động kéo được.\n- Khi cuộn ngang, STT và Mã phiếu ghim bên trái.'),
    T([206], 'Lưu cấu hình', 'P1', P25, '1. Đổi cấu hình cột.\n2. Bấm Lưu.', '—', '- Báo "Cập nhật thành công", cửa sổ đóng, bảng vẽ lại ngay.'),
    T([207], 'Đóng không lưu', 'P1', P25, '1. Mở Tuỳ chỉnh cột, bỏ tích Khách hàng.\n2. Bấm Đóng (hoặc (x), hoặc bấm ra ngoài).\n3. Mở lại cửa sổ.', '—',
      '- Không hỏi xác nhận; bảng vẫn có cột Khách hàng.\n- Mở lại thấy Khách hàng vẫn tích.'),
    T([208], 'Ghi nhớ sau F5 và trình duyệt khác', 'P1', 'Tài khoản A đã ẩn Người cập nhật, bật Phiếu YCXH.',
      '1. Nhấn F5.\n2. Đăng nhập A ở trình duyệt khác, mở màn.', '—', '- Cả 2 nơi đều giữ cấu hình đã lưu (lưu theo tài khoản).'),
    T([209], 'Cấu hình theo từng tài khoản', 'P1', 'Tài khoản A đã ẩn cột Người cập nhật; B chưa tùy chỉnh.',
      '1. Đăng nhập B trên cùng trình duyệt.\n2. Mở màn.', '—', '- B vẫn thấy cột Người cập nhật (bộ 12 cột mặc định).'),
    T([210, 211], 'Không ảnh hưởng dữ liệu và bộ lọc', 'P2', P25 + '\nĐang lọc Trạng thái = Đã duyệt (21 phiếu).',
      '1. Ẩn cột Trạng thái, bấm Lưu.', '—', '- Danh sách vẫn 21 phiếu, bộ lọc giữ nguyên; chỉ mất cột hiển thị.'),
    T([], 'Chọn tất cả / Bỏ chọn hết', 'P2', P25, '1. Mở Tuỳ chỉnh cột.\n2. Bấm Bỏ chọn hết.\n3. Bấm Chọn tất cả.', '—',
      '- Bước 2: mọi cột bỏ tích trừ STT, Mã phiếu, Hành động.\n- Bước 3: tích cả 13 cột.'),
]

# ================================================================== IX
S9 = [
    T([212], 'Mở cửa sổ chọn trường xuất', 'P1', P25, M + '\n3. Bấm Xuất Excel.', '—',
      '- Cửa sổ "Chọn trường xuất Excel", dòng hướng dẫn, nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng.'),
    T([213], 'Danh sách trường xuất', 'P1', P25, '1. Mở cửa sổ xuất.', '—',
      '- 10 trường: Mã phiếu, Số hợp đồng/đơn hàng, Khách hàng, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, Ngày '
      'duyệt, Người duyệt, Trạng thái.'),
    T([214], 'Trường chọn mặc định theo cột đang hiện', 'P1', 'Tài khoản đã ẩn cột Người duyệt trong Tùy chỉnh cột.', '1. Mở cửa sổ xuất.', '—',
      '- Tích sẵn 9 trường đang hiện trên bảng; Người duyệt không tích.\n- Dòng "Đang chọn 9/10 trường".'),
    T([215, 223, 224, 225], 'Xuất với trường mặc định', 'P0', P25 + '\nChưa tùy chỉnh cột.', '1. Mở cửa sổ xuất.\n2. Bấm Xuất file.', '—',
      '- Tải file "danh_sach_phieu_yeu_cau_van_chuyen.xlsx", trang tính "Yêu cầu vận chuyển".\n'
      '- Tiêu đề "DANH SÁCH PHIẾU YÊU CẦU VẬN CHUYỂN, BỐC XẾP"; cột STT rồi 10 cột đúng tên trường.\n- Thông báo "Xuất Excel thành công.".'),
    T([216], 'Xuất tất cả trường', 'P1', 'Tài khoản đã ẩn 3 cột trên bảng.', '1. Mở cửa sổ xuất.\n2. Bấm Chọn tất cả, bấm Xuất file.', '—',
      '- File có STT + đủ 10 cột.'),
    T([217, 226], 'Xuất một số trường theo thứ tự kéo thả', 'P0', P25 + '\nĐang lọc Trạng thái = Đã duyệt.',
      '1. Mở cửa sổ xuất.\n2. Bấm Bỏ chọn hết, tích Mã phiếu, Khách hàng, Trạng thái.\n3. Kéo Trạng thái lên trước Khách hàng.\n4. Bấm Xuất file.', '—',
      '- File chỉ có STT, Mã phiếu, Trạng thái, Khách hàng đúng thứ tự đã kéo.'),
    T([218], 'Không chọn trường nào', 'P1', P25, '1. Mở cửa sổ xuất.\n2. Bấm Bỏ chọn hết.', '—',
      '- Dòng "Đang chọn 0/10 trường".\n- Nút Xuất file bị khóa, không xuất được.'),
    T([219], 'Xuất theo tìm kiếm', 'P1', P25, '1. Tìm "YCVC1026".\n2. Xuất Excel với trường mặc định.', 'Ô tìm nhanh: YCVC1026',
      '- File chỉ có 6 phiếu khớp từ khóa.'),
    T([220], 'Xuất theo bộ lọc', 'P0', P25, '1. Lọc Trạng thái = Từ chối.\n2. Xuất Excel.', 'Trạng thái: Từ chối', '- File chỉ có 2 phiếu Từ chối.'),
    T([221, 227], 'Xuất nhiều trang', 'P0', P25 + '\nĐang xem trang 1, 10 dòng/trang.', '1. Xuất Excel không lọc.', '—',
      '- File có đủ 25 dòng (mọi trang), không chỉ 10 dòng đang xem.\n- Số dòng bằng N ở dòng "Hiển thị".'),
    T([222], 'Xuất khi danh sách rỗng', 'P1', 'Bộ lọc đang cho kết quả "Không có dữ liệu phù hợp.".', '1. Bấm Xuất Excel.\n2. Bấm Xuất file.', '—',
      '- Báo "Không có dữ liệu phù hợp.".\n- KHÔNG tải file nào.'),
    T([228], 'Dữ liệu file khớp lưới', 'P1', P25, '1. Xuất Excel.\n2. So 5 dòng đầu file với 5 dòng đầu bảng.', '—',
      '- Cùng thứ tự sắp xếp, mã phiếu, số hợp đồng, khách hàng, người tạo (họ tên kèm mã phòng ban), trạng thái.'),
    T([229], 'Định dạng ngày / chữ trong file', 'P2', P25, '1. Xuất Excel.\n2. Xem cột Ngày tạo, Ngày duyệt, Trạng thái.', '—',
      '- Ngày dạng dd/mm/yyyy hh:mm như trên lưới; phiếu chưa duyệt để trống Ngày duyệt.\n- Trạng thái ghi chữ (Đang tạo, Chờ duyệt, Đã duyệt, Từ chối).'),
    T([230], 'Tiếng Việt và ký tự đặc biệt', 'P2', 'Có phiếu khách hàng "Công ty TNHH Đông Á & Cộng sự", số hợp đồng "HĐ_01/2026".',
      '1. Xuất Excel.', '—', '- Tên khách hàng, số hợp đồng hiện đúng dấu tiếng Việt, ký tự &, /, _ không bị lỗi.'),
    T([293], 'Xuất trong phạm vi quyền', 'P0', 'Tài khoản A (không quyền) lập 3 phiếu; công ty có 50 phiếu.', '1. Đăng nhập A, Xuất Excel đủ 10 trường.', '—',
      '- File chỉ có 3 phiếu của A.'),
    T([], 'Tiến độ và khóa nút khi đang xuất', 'P2', 'Phạm vi xem có 3000 phiếu.', '1. Bấm Xuất Excel, Xuất file.\n2. Quan sát cạnh nút Xuất Excel.', '—',
      '- Hiện "Đang chuẩn bị dữ liệu…", "Đã tải x/y dòng…", "Đang dựng file x/y dòng…".\n- Nút Xuất Excel khóa đến khi xong.'),
    T([], 'Đóng cửa sổ xuất', 'P2', P25, '1. Mở cửa sổ xuất, bấm Đóng.', '—', '- Cửa sổ đóng, không tải file.'),
]

# ================================================================== X
S10 = [
    T([268], 'Lập phiếu từ phiếu YCXH không có dòng hàng', 'P1', PA + '\nPYCXH-50002 có khách hàng, mọi dòng số lượng 0.',
      TAO + '\n3. Chọn HĐ_TPE_HN_01, PYCXH-50002.\n4. Bấm Lưu nháp.', '—',
      '- Bảng Chi tiết "Không có dữ liệu".\n- Dưới bảng "' + REQ + '", không lưu được.'),
    T([269, 283], 'Dòng hàng chép đúng phiếu YCXH', 'P0', PA, TAO + '\n' + CHON + '\n5. Đổi Phiếu YCXH sang PYCXH-44500 (3 dòng).', '—',
      '- Bước 4: bảng có 5 dòng đúng tên hàng, model, mã, ĐVT, số lượng của PYCXH-44434 (bỏ dòng số lượng 0).\n'
      '- Bước 5: bảng thay bằng đúng 3 dòng của PYCXH-44500, không còn dòng cũ.'),
    T([270], 'Không xóa phiếu đã duyệt', 'P1', 'Phiếu 00003 Đã duyệt do A lập (đã đổi ô Vận chuyển của phiếu YCXH).',
      '1. Đăng nhập A, quan sát dòng 00003 và màn chi tiết.', '—', '- Không có icon / nút Xóa.'),
    T([272], 'Sửa không mất liên kết', 'P1', PEDIT, '1. Sửa Ghi chú phiếu 00006, Lưu nháp.\n2. Mở chi tiết, bấm liên kết Đơn hàng/Hợp đồng và Phiếu YCXH.', '—',
      '- Hai liên kết vẫn mở đúng HĐ_TPE_HN_01 và PYCXH-44434.'),
    T([274, 281], 'Duyệt cập nhật phiếu YCXH', 'P0', PG + '\nPYCXH-44434 đang có ô Vận chuyển = Tự vận chuyển.',
      '1. Sau khi A gửi duyệt, mở PYCXH-44434 xem ô Vận chuyển.\n2. G duyệt phiếu 00004.\n3. Mở lại PYCXH-44434.', '—',
      '- Bước 1: ô Vận chuyển chưa đổi.\n- Bước 3: ô Vận chuyển = "Công ty vận chuyển".\n'
      '- Lưu ý: phiếu vận chuyển không hiện ở màn nào khác; đây là thay đổi duy nhất sang màn khác.'),
    T([278], 'Đổi tên khách hàng ở danh mục', 'P2', 'Phiếu 00004 khách hàng "KH0001 - Công ty TNHH An Phát".',
      '1. Đổi tên khách hàng KH0001 thành "Công ty TNHH An Phát Mới".\n2. Xem phiếu 00004 trên danh sách.\n3. Lập phiếu mới từ phiếu YCXH của KH0001.', '—',
      '- Phiếu 00004 vẫn hiện tên cũ (lưu theo thời điểm lập).\n- Phiếu mới hiện tên mới.'),
    T([279], 'Đổi số hợp đồng không mất liên kết', 'P2', 'Phiếu 00004 gắn HĐ_TPE_HN_01.',
      '1. Đổi số hợp đồng ở màn hợp đồng thành HĐ_TPE_HN_01A.\n2. Bấm số hợp đồng ở dòng 00004.', '—',
      '- Dòng 00004 vẫn hiện số cũ HĐ_TPE_HN_01.\n- Bấm vẫn mở đúng hợp đồng (nay số HĐ_TPE_HN_01A).'),
    T([280], 'Xóa phiếu không ảnh hưởng màn khác', 'P1', 'A lập phiếu 00005 Đang tạo gắn PYCXH-44434.',
      '1. Xóa phiếu 00005.\n2. Mở PYCXH-44434.', '—', '- Phiếu YCXH không đổi (ô Vận chuyển, trạng thái giữ nguyên).'),
    T([284], 'Liên kết giữ nguyên khi đổi trạng thái', 'P1', PG,
      '1. G từ chối phiếu 00004.\n2. A sửa, gửi lại; G duyệt.\n3. Sau mỗi bước mở chi tiết 00004.', '—',
      '- Đơn hàng/Hợp đồng, Phiếu YCXH, khách hàng, dòng hàng không đổi qua các trạng thái.'),
    T([285], 'Không để lại dòng hàng mồ côi', 'P2', 'A lập phiếu 00005 có 5 dòng hàng, gắn PYCXH-44434.',
      '1. Xóa phiếu 00005.\n2. Lập phiếu mới từ PYCXH-44434.', '—',
      '- Phiếu mới có đúng 5 dòng hàng của phiếu YCXH, Số kiện trống, không dính dữ liệu của phiếu đã xóa.'),
    T([286], 'Không sinh mã trùng', 'P1', 'A, B cùng công ty.', '1. A và B cùng bấm Gửi duyệt phiếu mới cùng một lúc.', '—',
      '- Hai phiếu có mã khác nhau, không có 2 phiếu cùng mã.'),
    T([], 'Đổi thủ kho của kho xuất hàng', 'P1', PG + '\nG3 chưa là thủ kho.',
      '1. Ở danh mục Kho vật lý thêm G3, bỏ G khỏi thủ kho Kho Hà Nội.\n2. G3 mở chi tiết 00004.\n3. G mở chi tiết 00004.', '—',
      '- G3 thấy nút Duyệt, Từ chối.\n- G không còn nút Duyệt, Từ chối.'),
    T([], 'Luồng lập, gửi, duyệt', 'P0', PA,
      '1. A lập phiếu, Gửi duyệt.\n2. G duyệt.\n3. A mở lại phiếu.', '—',
      '- Bước 1: G nhận thông báo Chờ duyệt.\n- Bước 3: phiếu Đã duyệt; A nhận thông báo Đã duyệt; không còn nút Sửa / Xóa.'),
    T([], 'Luồng từ chối, sửa, gửi lại, duyệt', 'P0', PA,
      '1. A gửi duyệt.\n2. G từ chối lý do "Sai địa điểm".\n3. A sửa, gửi lại.\n4. G duyệt.', '—',
      '- Lịch sử đủ các mốc theo đúng thứ tự.\n- Phiếu cuối cùng Đã duyệt, lý do cũ không còn.'),
]

# ================================================================== XI
S11 = [
    T([289], 'Không có quyền nào vẫn lập được phiếu', 'P0', PA, '1. Đăng nhập A.\n2. ' + MENU + '\n3. Bấm Tạo mới, lập và Lưu nháp.', '—',
      '- Có nút Tạo mới; lưu thành công.\n- Lưu ý: lập phiếu không cần quyền riêng.'),
    T([294], 'Xem lịch sử theo phạm vi', 'P1', 'Tài khoản A thấy 3 phiếu của mình.', '1. Bấm icon Lịch sử ở cả 3 dòng.', '—',
      '- Icon Lịch sử có ở mọi dòng; mở được lịch sử cả 3 phiếu.\n- Không xem được lịch sử phiếu ngoài phạm vi (không có dòng để bấm).'),
    T([296], 'Mở thẳng màn Sửa phiếu của người khác', 'P0',
      'Tài khoản C (tổng công ty); phiếu 00006 Đang tạo do A lập; phiếu 00001 Từ chối do A lập.\nC có đường link màn Sửa của 2 phiếu.',
      '1. Đăng nhập C.\n2. Dán đường link màn Sửa phiếu 00001.\n3. Dán đường link màn Sửa phiếu 00006.', '—',
      '- Bước 2: chuyển sang màn Chi tiết phiếu 00001, không mở form sửa.\n- Bước 3: trang không tìm thấy (nháp của người khác).'),
    T([297], 'Gọi thẳng chức năng ghi khi thiếu quyền', 'P1', 'Tài khoản C; phiếu 00001 Từ chối do A lập; phiếu 00004 Chờ duyệt (C không là thủ kho).',
      '1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa phiếu 00001, bỏ qua giao diện.\n2. Gọi thẳng chức năng Duyệt phiếu 00004.', '—',
      '- Bước 1: hệ thống từ chối, báo "Bạn không có quyền xóa phiếu này".\n- Bước 2: báo "Bạn không có quyền duyệt phiếu này".\n- Dữ liệu không đổi.'),
    T([298], 'Bị gỡ vai trò thủ kho giữa chừng', 'P1', PG + '\nG đang mở màn Chi tiết phiếu 00004.',
      '1. Quản lý kho bỏ G khỏi thủ kho Kho Hà Nội.\n2. G bấm Duyệt, bấm Duyệt ở hộp xác nhận.', '—',
      '- Báo "Bạn không có quyền duyệt phiếu này"; phiếu giữ Chờ duyệt.'),
    T([298], 'Bị gỡ quyền xem giữa chừng', 'P2', 'Tài khoản D (quyền công ty) đang xem 50 phiếu; D tự lập 2 phiếu.',
      '1. Quản trị gỡ quyền "Xem tất cả phiếu yêu cầu vận chuyển của công ty" của D.\n2. D bấm Làm mới.', '—',
      '- Danh sách chỉ còn 2 phiếu D lập.'),
]

# ================================================================== XII
S12 = [
    T([300], 'Điều kiện hiện nút Duyệt', 'P0', PG + '\nPhiếu 00003 Đã duyệt, 00006 Đang tạo cùng kho.',
      '1. Đăng nhập G.\n2. ' + MENU + '\n3. Quan sát cột Hành động.\n4. Mở chi tiết 00004.', '—',
      '- Chỉ dòng 00004 (Chờ duyệt) có icon Duyệt.\n- Màn Chi tiết 00004 có nút Duyệt và Từ chối.\n'
      '- Người lập A, người có quyền xem (không là thủ kho) không thấy nút Duyệt.'),
    T([301], 'Giao diện hộp xác nhận duyệt', 'P1', PG, '1. Mở chi tiết 00004.\n2. Bấm Duyệt.', '—',
      '- Hộp "Xác nhận duyệt" kèm icon dấu hỏi.\n- Nội dung "Bạn có chắc muốn duyệt phiếu yêu cầu vận chuyển \'TPE.YCVC1026.00004\'?".\n'
      '- Nút Duyệt, Hủy, (x).'),
    T([302, 305], 'Duyệt thành công', 'P0', PG, '1. Đăng nhập G, mở chi tiết 00004.\n2. Bấm Duyệt, bấm Duyệt ở hộp xác nhận.', '—',
      '- Báo "Duyệt thành công.", quay về danh sách.\n- Phiếu 00004 trạng thái Đã duyệt (nhãn xanh lá).'),
    T([303], 'Không cần nhập thêm dữ liệu khi duyệt', 'P1', PG, '1. Bấm Duyệt ở chi tiết 00004.', '—',
      '- Hộp xác nhận không có ô nhập nào; mọi trường bắt buộc đã được kiểm khi gửi duyệt.'),
    T([304], 'Phiếu YCXH không còn hợp lệ thì không duyệt được', 'P0', PG + '\nPYCXH-44434 vừa chuyển sang trạng thái Đã hủy (ngoài 5 trạng thái chọn được).',
      '1. G bấm Duyệt, xác nhận.', '—', '- Báo "Phiếu yêu cầu xuất hàng không hợp lệ.".\n- Phiếu 00004 giữ Chờ duyệt.'),
    T([306], 'Dữ liệu cập nhật sau khi duyệt', 'P1', PG, '1. G duyệt 00004.\n2. Xem dòng 00004 và màn chi tiết.', '—',
      '- Ngày duyệt = thời điểm duyệt; Người duyệt = họ tên G.\n- Ngày cập nhật, Người cập nhật đổi theo G.'),
    T([307], 'Ảnh hưởng tới phiếu YCXH', 'P0', PG, '1. G duyệt 00004.\n2. Mở PYCXH-44434.', '—', '- Ô Vận chuyển = "Công ty vận chuyển".'),
    T([308], 'Thông báo gửi đúng người sau khi duyệt', 'P0', PG, '1. G duyệt 00004.\n2. Kiểm chuông thông báo của A, G2, C.', '—',
      '- Chỉ A (người lập) nhận "[YCVC] Đã duyệt: TPE.YCVC1026.00004..." kèm khách hàng, ngày giao, người duyệt.\n- G2, C không nhận.'),
    T([309], 'Nội dung và điều hướng thông báo', 'P1', 'A vừa nhận thông báo Đã duyệt phiếu 00004.', '1. A bấm thông báo.', '—',
      '- Mở màn Chi tiết phiếu 00004, trạng thái Đã duyệt.'),
    T([310], 'Hủy thao tác duyệt', 'P1', PG, '1. Bấm Duyệt.\n2. Bấm Hủy (hoặc (x), hoặc ra ngoài hộp).', '—',
      '- Hộp đóng; phiếu giữ Chờ duyệt, không có thông báo, không có mốc lịch sử mới.'),
    T([311], 'Không duyệt lại phiếu đã xử lý', 'P0', 'G và G2 cùng là thủ kho, cùng mở chi tiết phiếu Chờ duyệt 00004.',
      '1. G duyệt.\n2. G2 bấm Duyệt, xác nhận.\n3. G2 xem lại màn.', '—',
      '- Bước 2: G2 nhận "' + CONFLICT + '", trang tải lại.\n- Bước 3: phiếu Đã duyệt, không còn nút Duyệt / Từ chối.'),
    T([312], 'Lịch sử duyệt', 'P1', PG, '1. G duyệt 00004.\n2. Mở Lịch sử 00004.', '—',
      '- Mốc mới nhất "Thay đổi trạng thái" Chờ duyệt sang Đã duyệt, người thực hiện G, thời điểm duyệt.'),
    T([], 'Icon Duyệt trên dòng mở màn chi tiết', 'P1', PG, '1. Bấm icon Duyệt ở dòng 00004.', '—',
      '- Mở màn Chi tiết 00004; không duyệt thẳng từ danh sách.'),
    T([], 'Super admin duyệt được', 'P2', 'Tài khoản DNS Admin (Super admin, không là thủ kho); phiếu 00004 Chờ duyệt.',
      '1. Mở chi tiết 00004.\n2. Duyệt.', '—', '- Có nút Duyệt; duyệt thành công.'),
]

# ================================================================== XIII
S13 = [
    T([313], 'Điều kiện hiện nút Từ chối', 'P0', PG, '1. Đăng nhập G, mở chi tiết 00004.\n2. Đăng nhập A, mở chi tiết 00004.', '—',
      '- G thấy nút Từ chối (màu đỏ) cạnh Duyệt.\n- A không thấy.\n- Phiếu không ở Chờ duyệt thì không có nút Từ chối.'),
    T([314], 'Giao diện cửa sổ từ chối', 'P1', PG, '1. Bấm Từ chối.', '—',
      '- Cửa sổ "Từ chối phiếu yêu cầu vận chuyển", dòng phụ "Phiếu: TPE.YCVC1026.00004".\n'
      '- Ô Lý do từ chối có dấu *, gợi ý "Nhập lý do từ chối", con trỏ đặt sẵn.\n- Nút Từ chối (đỏ), Hủy, (x).'),
    T([315, 318], 'Từ chối thành công', 'P0', PG, '1. Bấm Từ chối.\n2. Nhập lý do, bấm Từ chối.', 'Lý do: Sai địa điểm',
      '- Báo "Từ chối thành công.", cửa sổ đóng, quay về danh sách.\n- Phiếu 00004 trạng thái Từ chối (nhãn đỏ).'),
    T([316], 'Bỏ trống lý do', 'P0', PG, '1. Bấm Từ chối.\n2. Để trống, bấm Từ chối.\n3. Nhập 5 dấu cách, bấm Từ chối.', '—',
      '- Ô viền đỏ, dưới ô "' + REQ + '", cửa sổ không đóng (cả khi chỉ có khoảng trắng).'),
    T([317], 'Giới hạn ký tự lý do', 'P1', PG, '1. Nhập lý do 5001 ký tự, bấm Từ chối.\n2. Sửa còn 5000 ký tự, bấm Từ chối.', '—',
      '- Bước 1: thông báo "Vui lòng nhập tối đa 5000 ký tự.", cửa sổ không đóng.\n- Bước 2: từ chối thành công.'),
    T([319], 'Hiển thị và lưu lý do từ chối', 'P1', 'Phiếu 00004 vừa bị từ chối, lý do "  Sai địa điểm  ".',
      '1. Mở chi tiết 00004.\n2. A mở màn Sửa 00004.', '—',
      '- Chi tiết có Người duyệt (G), Ngày duyệt, Lý do từ chối "Sai địa điểm" (bỏ khoảng trắng hai đầu).\n- Màn Sửa hiện Lý do từ chối chỉ đọc.'),
    T([320], 'Từ chối không ảnh hưởng phiếu YCXH', 'P1', PG + '\nPYCXH-44434 ô Vận chuyển = Tự vận chuyển.', '1. G từ chối 00004.\n2. Mở PYCXH-44434.', '—',
      '- Ô Vận chuyển vẫn "Tự vận chuyển".'),
    T([321], 'Thông báo sau khi từ chối', 'P0', PG, '1. G từ chối 00004 lý do "Sai địa điểm".\n2. Kiểm chuông của A, G2.', '—',
      '- A nhận "[YCVC] Từ chối: TPE.YCVC1026.00004..." kèm người từ chối và lý do.\n- G2 không nhận; bấm thông báo mở chi tiết phiếu.'),
    T([322], 'Hủy thao tác từ chối', 'P1', PG, '1. Bấm Từ chối, nhập lý do.\n2. Bấm Hủy.\n3. Bấm Từ chối lại.', '—',
      '- Bước 2: đóng ngay, không hỏi; phiếu giữ Chờ duyệt.\n- Bước 3: ô Lý do trống.'),
    T([323], 'Không từ chối phiếu đã được xử lý', 'P0', 'G và G2 cùng là thủ kho, cùng mở chi tiết phiếu Chờ duyệt 00004.',
      '1. G duyệt.\n2. G2 bấm Từ chối, nhập lý do, xác nhận.', '—',
      '- G2 nhận "' + CONFLICT + '", trang tải lại; phiếu vẫn Đã duyệt.'),
    T([324], 'Lịch sử từ chối', 'P1', PG, '1. G từ chối 00004 lý do "Sai địa điểm".\n2. Mở Lịch sử.', '—',
      '- Mốc "Thay đổi trạng thái" Chờ duyệt sang Từ chối, người thực hiện G, thời điểm, kèm lý do "Sai địa điểm".'),
]

# Cài đặt bộ lọc thuộc nhóm II. Tìm kiếm và lọc (user 02/11/2026: không tách thành phần riêng)
S_FCFG = [
    T([], 'Mở cửa sổ Cài đặt bộ lọc', 'P2', P25, M + '\n3. Bấm Cài đặt bộ lọc.', '—',
      '- Cửa sổ "Cài đặt bộ lọc" liệt kê 6 tiêu chí kèm ô tích và biểu tượng kéo thả.\n- Nút Lưu, Khôi phục mặc định, Đóng.'),
    T([], 'Cài đặt bộ lọc: ẩn tiêu chí lọc', 'P2', P25, '1. Cài đặt bộ lọc.\n2. Bỏ tích Người tạo, bấm Lưu.\n3. Bấm Tìm kiếm nâng cao.', '—',
      '- Báo "Cập nhật thành công".\n- Khối tìm kiếm nâng cao không còn ô Người tạo.'),
    T([], 'Cài đặt bộ lọc: đổi thứ tự tiêu chí', 'P2', P25, '1. Cài đặt bộ lọc.\n2. Kéo Trạng thái lên đầu, bấm Lưu.', '—',
      '- Ô Trạng thái đứng đầu khối tìm kiếm nâng cao.'),
    T([], 'Cài đặt bộ lọc: Khôi phục mặc định', 'P2', 'Đã ẩn Người tạo và đổi thứ tự.', '1. Cài đặt bộ lọc.\n2. Bấm Khôi phục mặc định, bấm Lưu.', '—',
      '- Đủ 6 tiêu chí theo thứ tự gốc.'),
    T([], 'Cài đặt bộ lọc: đóng không lưu', 'P2', P25, '1. Cài đặt bộ lọc, bỏ tích Khách hàng.\n2. Bấm Đóng.', '—',
      '- Không hỏi xác nhận; ô Khách hàng vẫn còn.'),
    T([], 'Cài đặt bộ lọc: cấu hình theo tài khoản', 'P2', 'A đã ẩn ô Người tạo; B chưa cài đặt.', '1. Đăng nhập B, mở Tìm kiếm nâng cao.', '—',
      '- B vẫn thấy đủ 6 tiêu chí.'),
]

# ================================================================== XIV
S14 = [
    T([], 'Cửa sổ Chọn đơn hàng/hợp đồng', 'P0', PA, TAO + '\n3. Bấm ô Đơn hàng/Hợp đồng.', '—',
      '- Cửa sổ "Chọn đơn hàng/hợp đồng": cột STT, Số đơn hàng/Hợp đồng, Loại hợp đồng, Ngày tạo.\n'
      '- Ô Loại hợp đồng mặc định Tất cả; 10 dòng / trang, mới tạo lên trước.'),
    T([], 'Lọc Loại hợp đồng trong cửa sổ', 'P1', PA, '1. Mở cửa sổ Chọn đơn hàng/hợp đồng.\n2. Chọn Loại hợp đồng = Hợp đồng mua dịch vụ.',
      'Loại hợp đồng: Hợp đồng mua dịch vụ', '- Chỉ còn hợp đồng mua dịch vụ, về trang 1.'),
    T([], 'Tìm số hợp đồng trong cửa sổ', 'P1', PA, '1. Mở cửa sổ.\n2. Nhập "TPE_HN", nhấn Enter.\n3. Bấm Làm mới.', 'TPE_HN',
      '- Bước 2: chỉ còn hợp đồng có số chứa "TPE_HN".\n- Bước 3: xóa ô tìm và Loại hợp đồng, nạp lại trang 1.'),
    T([], 'Bấm số hợp đồng trong cửa sổ', 'P2', PA, '1. Mở cửa sổ, bấm chữ xanh số hợp đồng ở 1 dòng.', '—',
      '- Mở chứng từ ở tab mới; dòng KHÔNG được chọn, cửa sổ vẫn mở.'),
    T([], 'Chọn hợp đồng', 'P0', PA, TAO + '\n3. Bấm ô Đơn hàng/Hợp đồng, bấm dòng HĐ_TPE_HN_01.', '—',
      '- Ô Đơn hàng/Hợp đồng ghi HĐ_TPE_HN_01, cửa sổ đóng.'),
    T([], 'Hợp đồng bán chỉ của công ty mình', 'P1', PA + '\nHĐ_ETEK_01 (hợp đồng bán còn hiệu lực) do người công ty ETEK lập; A thuộc công ty TPE.',
      '1. Mở cửa sổ, tìm "HĐ_ETEK_01".', '—', '- Không có HĐ_ETEK_01 trong kết quả.'),
    T([], 'Cửa sổ Chọn phiếu YCXH chỉ có phiếu hợp lệ', 'P0', PA + '\nPYCXH-410 chưa gắn khách hàng.',
      TAO + '\n3. Chọn HĐ_TPE_HN_01.\n4. Bấm ô Phiếu YCXH, tìm "410".', '—',
      '- Cửa sổ "Chọn phiếu yêu cầu xuất hàng".\n- Không có PYCXH-410.'),
    T([], 'Chọn phiếu YCXH tự điền dữ liệu', 'P0', PA, TAO + '\n' + CHON, '—',
      '- Khách hàng "KH0001 - Công ty TNHH An Phát", Người liên hệ, Số ĐT, Địa điểm giao hàng tự điền.\n'
      '- Bảng Chi tiết có 5 dòng (bỏ dòng số lượng 0), Số kiện trống.'),
    T([], 'Đổi hợp đồng xóa phiếu YCXH', 'P1', PFORM, '1. Chọn lại hợp đồng khác HĐ_TPE_HN_02.', '—',
      '- Phiếu YCXH, khách hàng, người liên hệ, địa điểm giao, bảng Chi tiết bị xóa.'),
    T([], 'Bỏ chọn phiếu YCXH giữ hợp đồng', 'P2', PFORM, '1. Bấm dấu × ở ô Phiếu YCXH.', '—',
      '- Xóa phiếu YCXH và các ô lấy theo phiếu, bảng Chi tiết trống; ô Đơn hàng/Hợp đồng giữ nguyên.'),
    T([], 'Đóng cửa sổ chọn không chọn', 'P2', PA, '1. Mở cửa sổ Chọn phiếu yêu cầu xuất hàng.\n2. Bấm Đóng / (x) / ra ngoài.', '—',
      '- Cửa sổ đóng, ô Phiếu YCXH không đổi.'),
    T([], 'Phiếu YCXH vừa đổi sang trạng thái không chọn được', 'P2', PA + '\nPYCXH-44434 vừa được duyệt xuất kho trong lúc cửa sổ đang mở.',
      '1. Bấm dòng PYCXH-44434.', '—', '- Dưới ô Phiếu YCXH "Không thể chọn phiếu này.", thông báo "' + CHK + '".\n- Không điền dữ liệu.'),
]

# Một nhóm Phân quyền duy nhất (user 02/11/2026): khối phân quyền đầu file đưa vào đầu XI.
ROLE_P0 = ('01', '02', '03', '04', '09')
S11[:0] = [T(ROLE_COVER[tc[0]], tc[1], 'P0' if tc[0] in ROLE_P0 else tc[2], *tc[3:]) for tc in ROLE_TCS]
S2 += S_FCFG

SECTIONS = [
    section('I', 'HIỂN THỊ DANH SÁCH VÀ TRUY CẬP', S1),
    section('II', 'TÌM KIẾM VÀ LỌC', S2),
    section('III', 'THÊM MỚI', S3),
    section('IV', 'CHỈNH SỬA', S4),
    section('V', 'XÓA', S5),
    section('VI', 'LỊCH SỬ THAY ĐỔI', S6),
    section('VII', 'XEM CHI TIẾT', S7),
    section('VIII', 'TÙY CHỈNH CỘT', S8),
    section('IX', 'XUẤT EXCEL', S9),
    section('X', 'ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU', S10),
    section('XI', 'PHÂN QUYỀN', S11),
    section('XII', 'DUYỆT PHIẾU', S12),
    section('XIII', 'KHÔNG DUYỆT PHIẾU (TỪ CHỐI)', S13),
    section('XIV', 'CHỌN ĐƠN HÀNG/HỢP ĐỒNG VÀ PHIẾU YCXH', S14),
]
# Nâng P0 cho các case nghiệp vụ cốt lõi (ràng buộc nhập liệu, phạm vi quyền, luồng duyệt, lịch sử) — P0 phải >= 40%.
P0_UP = {
    'II': {'028'}, 'III': {'004', '017', '019', '036'}, 'IV': {'004', '015', '023', '025'}, 'V': {'005', '006'},
    'VI': {'015'}, 'VII': {'005'}, 'IX': {'007', '011', '012'}, 'X': {'001', '003', '012'}, 'XI': {'014', '015'},
    'XII': {'006', '010', '012'}, 'XIII': {'005', '006', '007', '009', '011'}, 'XIV': {'009'},
}
SECTIONS = [(r, t, [(tc[0], tc[1], 'P0' if tc[0] in P0_UP.get(r, ()) else tc[2]) + tuple(tc[3:]) for tc in tcs])
            for r, t, tcs in SECTIONS]
check_no_dash_pre(SECTIONS, [])

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1', feature_name=FEATURE,
          module_name='YC vận chuyển, bốc xếp', description_block=DESCRIPTION_BLOCK, role_tcs=[], sections=SECTIONS)
    print('Checklist có TC:', len(COVER))
