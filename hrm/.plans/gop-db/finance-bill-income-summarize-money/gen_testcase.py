# -*- coding: utf-8 -*-
"""Testcase màn "Tổng hợp tiền về ngân hàng" (phân hệ Tài chính / Thông báo) — skill testcase-documenter (tc_engine).

Chạy: python gen_testcase.py -> testcase.xlsx
03/11/2026: bản đầu theo checklist "Mẫu tài liệu.xlsx" (../phieu-theo-form-quoc-gia/checklist_mau_tai_lieu.json): section
  xếp theo thứ tự nhóm của checklist, BỎ nhóm màn không có (Thêm mới, Chỉnh sửa, Xóa, Khóa/Mở khóa, Lịch sử thay đổi,
  Import Excel, Duyệt, Không duyệt), đánh số liền; rồi phần riêng (Chọn dòng và tạo mới điều chỉnh công nợ). Một nhóm
  Phân quyền duy nhất (role_tcs=[]); case Cài đặt bộ lọc nằm trong nhóm Tìm kiếm và lọc. Đối chiếu ở gen_checklist.py.
Nguồn hành vi (đọc 03/11/2026, nhánh develop cả 2 repo): pages/finance/bill-income-reports/summarize-money.vue,
  V2BaseSmartFilterPanel, V2BaseDataTable, export-fields-modal, column-customization-modal, filterStateMixin, download-excel;
  BE BillIncomeReportSummarizeService, BillIncomeReportLookupService::searchSummarizeCustomers, BillIncomeReportSummarizeExport,
  BillIncomeReportController, BillIncomeReportAccess; màn đích BillAdjustDeptRequestForm + BillAdjustDeptLookupService.
  Số liệu dev-hrm 03/11/2026 (DNS Admin): 8043 dòng, 56 Chưa điều chỉnh hết, 7987 Đã điều chỉnh hết.
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
from tc_engine import build  # noqa: E402
from tc_phieu_bosung import check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Tài chính > menu "Quản lý tiền" > nhóm "Thanh toán tiền mặt" > bấm "Tổng hợp tiền về ngân hàng".'
ADV = 'Bấm Tìm kiếm nâng cao.'
EMPTY = '"Không có dữ liệu phù hợp bộ lọc."'
REJECT = '"Không thể chọn 2 phiếu báo có khác nhau! Vui lòng bỏ chọn dòng cũ trước."'
NONE = '"Vui lòng chọn ít nhất một chi tiết báo có."'

PRE = 'Tài khoản DNS Admin (công ty Tân Phát); màn có 8043 dòng tiền về: 56 dòng Chưa điều chỉnh hết công nợ, 7987 dòng Đã điều chỉnh hết.'
L52 = ('Phiếu TPE.PBC1026.00052 Đã duyệt: ngày hạch toán 20/10/2026 (tạo 08:26), người tạo Nguyễn Hồng Hải - HN_KTTV, ngân hàng '
       'VIETCOMBANK, STK 0301002859668; 14 dòng Chưa điều chỉnh hết, dòng mới nhất 239,093,640 diễn giải "NHATMINH TT HD 8026 …", '
       'dòng kế 779,760.')
L51 = 'Phiếu TPE.PBC1026.00051 Đã duyệt: VIETINBANK, STK 116000142872, 17 dòng Chưa điều chỉnh hết (dòng đầu 112,523,435).'
L50 = 'Phiếu TPE.PBC1026.00050: dòng "o to mien bac tt tan phat", MB, 1,178,100, Số tiền chưa điều chỉnh 0 (Đã điều chỉnh hết).'
ACC_A = 'Tài khoản A: kế toán công ty Tân Phát, không có quyền Xem tất cả phiếu báo có (tổng công ty / công ty), không tạo phiếu báo có nào.'
ACC_B = 'Tài khoản B: nhân viên công ty 2 (khác Tân Phát); công ty 2 có 5 dòng tiền về đủ điều kiện.'
ACC_C = 'Tài khoản C: chưa được gắn công ty làm việc.'
P20 = 'Đổi Số dòng/trang = 20 (dòng 1–14 thuộc TPE.PBC1026.00052, dòng 15–20 thuộc TPE.PBC1026.00051).'


def T(no, func, prio, pre, steps, td, exp):
    if isinstance(pre, (list, tuple)):
        pre = '\n'.join(pre)
    if isinstance(td, (list, tuple)):
        td = '\n'.join(td)
    st = '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(steps))
    ex = '\n'.join(x if x.startswith('- ') else '- ' + x for x in exp)
    return ('%03d' % no, func, prio, pre, st, td, ex)


def renum(cases):
    return [('%03d' % (i + 1),) + tuple(c[1:]) for i, c in enumerate(cases)]


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn Tổng hợp tiền về ngân hàng liệt kê từng khoản tiền về tài khoản ngân hàng (dòng chi tiết của phiếu báo có đã duyệt) '
     'cần đối chiếu công nợ, kèm số tiền chưa điều chỉnh. Kế toán tích các dòng còn tiền của cùng một phiếu báo có rồi bấm '
     '"Tạo mới điều chỉnh công nợ" để lập phiếu yêu cầu điều chỉnh công nợ. Màn chỉ đọc; có Xuất Excel chọn trường.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Dòng của phiếu báo có Đã duyệt, loại thu khác Thu nhà cung cấp.\n'
     '- Tài khoản có của dòng là 1311, 1312 hoặc 3311.\n'
     '- Phiếu ghi công ty = công ty làm việc của người đăng nhập.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Dòng đã đánh dấu "Không báo tiền về" ở màn Chi tiết phiếu báo có.\n'
     '- Phiếu Đang tạo; phiếu Thu nhà cung cấp; dòng tài khoản khác 1311 / 1312 / 3311; phiếu công ty khác.\n'
     '- Màn KHÔNG có Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel, Lịch sử thay đổi.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Ngày hạch toán lọc theo ngày hạch toán của phiếu báo có, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu báo có > dòng tiền về. Mỗi dòng bảng là 1 dòng tiền về; các dòng cùng phiếu có chung Số báo có, Ngày hạch toán, '
     'Người tạo, Ngân hàng, STK.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Số tiền chưa điều chỉnh = Số tiền trừ tiền đã điều chỉnh (cộng dồn khi phiếu kế toán điều chỉnh công nợ được duyệt).\n'
     '- > 0: "Chưa điều chỉnh hết công nợ" (vàng, có ô tích); = 0: "Đã điều chỉnh hết công nợ" (xanh lá, không có ô tích).'),
    ('7. Phân quyền cấp',
     '- Màn không gắn quyền: ai vào được phân hệ Tài chính / Thông báo đều dùng được mọi chức năng.\n'
     '- Dữ liệu theo công ty của người đăng nhập; chưa gắn công ty thì rỗng.\n'
     '- Bấm Số báo có mở chi tiết phiếu theo quyền của màn Phiếu báo có (Xem tất cả phiếu báo có của tổng công ty / công ty, '
     'hoặc người tạo phiếu).'),
    ('8. Cách tính các ô thống kê',
     'Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng dòng tiền về khớp bộ lọc trong phạm vi công ty.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: DNS Admin (công ty Tân Phát), A (kế toán Tân Phát, không quyền xem phiếu báo có theo cấp), '
     'B (công ty 2), C (chưa gắn công ty).\n'
     '- Lưu ý: bộ lọc KHÔNG được ghi nhớ khi rời màn / tải lại trang.\n'
     '- Lưu ý: số tiền hiển thị phân cách hàng nghìn bằng dấu phẩy.\n'
     '- Các case "dùng công cụ kiểm thử API" dành cho tester kỹ thuật.'),
]

# ============================================================== I. HIỂN THỊ DANH SÁCH VÀ TRUY CẬP
S1 = [
    T(1, 'Mở màn từ menu', 'P0', PRE, ['Đăng nhập.', MENU], '—',
      ['Mở màn "Tổng hợp tiền về ngân hàng", tiêu đề bảng "Tổng hợp tiền về ngân hàng".',
       'Mặc định 10 dòng / trang; ô Số dòng/trang có 5, 10, 20, 50, 100.',
       'Dòng nhập gần nhất ở trên (dòng 1 là TPE.PBC1026.00052, 239,093,640).', 'Dưới bảng "Hiển thị 1–10 / 8043".']),
    T(2, 'Mở màn từ 2 lối vào phân hệ Thông báo', 'P1', PRE,
      ['Vào phân hệ Thông báo > menu "Tra cứu - thông báo" > bấm "Tổng hợp tiền về".',
       'Vào phân hệ Thông báo > menu "Thông báo" > bấm "Tổng hợp tiền về ngân hàng".'], '—',
      ['Cả 2 lối đều mở cùng màn "Tổng hợp tiền về ngân hàng".', 'Dữ liệu giống hệt lối vào từ phân hệ Tài chính (8043 dòng).']),
    T(3, 'Tiêu đề màn hình', 'P0', PRE, [MENU, 'Quan sát thanh trên cùng, tab trình duyệt và tiêu đề bảng.'], '—',
      ['Thanh trên cùng và tab trình duyệt: "Tổng hợp tiền về ngân hàng".', 'Tiêu đề bảng: "Tổng hợp tiền về ngân hàng".']),
    T(4, 'Các nút chức năng được hiển thị', 'P0', PRE, [MENU, 'Quan sát khối bộ lọc và thanh công cụ của bảng.'], '—',
      ['Khối bộ lọc: ô "Tìm theo số báo có...", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
       'Thanh công cụ: Tạo mới điều chỉnh công nợ, Xuất Excel, nút biểu tượng cột (Cấu hình cột hiển thị).',
       'KHÔNG có nút Thêm mới, Import Excel, Xóa, Lịch sử.']),
    T(5, 'Các cột mặc định hiển thị', 'P0', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột từ trái sang phải.'], '—',
      ['Đúng 12 cột: STT, Số báo có, Ngày hạch toán, Người tạo, Khách hàng, Ghi chú, Ngân hàng, STK ngân hàng, Số tiền, Số tiền '
       'chưa điều chỉnh, Trạng thái, Điều chỉnh công nợ.', 'STT và Số báo có ghim bên trái khi cuộn ngang.']),
    T(6, 'Không có cột mặc định ẩn', 'P2', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
      ['Cửa sổ "Tuỳ chỉnh cột" tích đủ 12/12 cột, không cột nào ẩn sẵn.']),
    T(7, 'Dữ liệu dòng khớp phiếu báo có', 'P0', [PRE, L52], [MENU, 'Đối chiếu dòng 1 với màn Chi tiết phiếu TPE.PBC1026.00052.'], '—',
      ['Số báo có "TPE.PBC1026.00052" (chữ xanh gạch chân); Ngày hạch toán "20/10/2026 08:26".',
       'Người tạo "Nguyễn Hồng Hải - HN_KTTV"; Ghi chú đúng diễn giải dòng; Ngân hàng "VIETCOMBANK"; STK "0301002859668".',
       'Số tiền "239,093,640", Số tiền chưa điều chỉnh "239,093,640" căn phải.',
       'Khách hàng hiện "Mã - Tên" khách gắn với dòng; dòng chưa gắn khách thì trống.']),
    T(8, 'Nhãn trạng thái dòng', 'P0', [PRE, L52, L50], [MENU, 'Quan sát dòng TPE.PBC1026.00052 và dòng TPE.PBC1026.00050.'], '—',
      ['Dòng còn tiền: nhãn vàng "Chưa điều chỉnh hết công nợ", có ô tích ở cột Điều chỉnh công nợ.',
       'Dòng hết tiền: nhãn xanh lá "Đã điều chỉnh hết công nợ", Số tiền chưa điều chỉnh "0", cột Điều chỉnh công nợ trống.',
       'Cột Trạng thái không sắp xếp được.']),
    T(9, 'Danh sách chưa có dữ liệu', 'P1', ACC_C, ['Đăng nhập C.', MENU], '—',
      ['Bảng hiện ' + EMPTY, 'Dưới bảng ghi "Không có dòng nào.".', 'Không báo lỗi.']),
    T(10, 'Không có dữ liệu phù hợp bộ lọc', 'P1', PRE, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
      ['Bảng hiện ' + EMPTY, 'Dưới bảng "Không có dòng nào.".']),
    T(11, 'Thay đổi số dòng / trang', 'P0', PRE, [MENU, 'Bấm sang trang 3.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
      ['Bảng hiện 20 dòng.', 'Tự quay về trang 1, "Hiển thị 1–20 / 8043".', 'STT chạy 1–20.']),
    T(12, 'Trang trước / trang tiếp theo', 'P0', PRE, [MENU, 'Bấm nút ›.', 'Bấm nút ‹.'], '—',
      ['Bước 2: trang 2, "Hiển thị 11–20 / 8043".', 'Bước 3: về trang 1, "Hiển thị 1–10 / 8043".']),
    T(13, 'Trang đầu / trang cuối', 'P1', PRE, [MENU, 'Bấm nút ».', 'Bấm nút «.'], '—',
      ['Bước 2: trang 805, "Hiển thị 8041–8043 / 8043", đúng 3 dòng (TPE.PBC0825.00001).', 'Bước 3: về trang 1.']),
    T(14, 'Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE, [MENU, 'Ở trang 1 quan sát « và ‹.', 'Về trang cuối, quan sát › và ».'], '—',
      ['Trang 1: « và ‹ mờ, bấm không tác dụng.', 'Trang cuối: › và » mờ, bấm không tác dụng.']),
    T(15, 'STT liên tục giữa các trang', 'P0', PRE, [MENU, 'Sang trang 2, rồi trang 3.'], '—', ['Trang 2: STT 11–20.', 'Trang 3: STT 21–30.']),
    T(16, 'Tổng số bản ghi', 'P0', PRE, [MENU, 'Đọc dòng dưới bảng.', ADV, 'Chọn Trạng thái = Chưa điều chỉnh hết công nợ.'], '—',
      ['Bước 2: "Hiển thị 1–10 / 8043".', 'Bước 4: "Hiển thị 1–10 / 56" (đúng số dòng còn tiền).']),
    T(17, 'Về trang 1 khi thay đổi bộ lọc', 'P0', PRE, [MENU, 'Sang trang 5.', ADV, 'Nhập Ngân hàng = "VIETIN".'], 'Ngân hàng: VIETIN',
      ['Danh sách tự nạp lại ở trang 1.', 'Dòng tổng "Hiển thị 1–10 / 2885".']),
    T(18, 'Sắp xếp mặc định', 'P1', PRE, [MENU, 'Quan sát 3 dòng đầu, chưa bấm tiêu đề cột nào.'], '—',
      ['Dòng nhập gần nhất xếp trên (TPE.PBC1026.00052: 239,093,640, rồi 779,760, rồi 3,672,000).', 'Không cột nào có mũi tên sắp xếp đang bật.']),
    T(19, 'Sắp xếp tăng / giảm theo Số tiền', 'P0', PRE, [MENU, 'Bấm tiêu đề cột Số tiền.', 'Bấm lại tiêu đề Số tiền.'], '—',
      ['Bước 2: tăng dần, mũi tên lên.', 'Bước 3: giảm dần, dòng đầu TPE.PBC0126.00049 "304,249,923,269".']),
    T(20, 'Sắp xếp theo Số báo có, Ngân hàng, Số tiền chưa điều chỉnh', 'P1', PRE,
      [MENU, 'Bấm tiêu đề Số báo có.', 'Bấm tiêu đề Ngân hàng.', 'Bấm tiêu đề Số tiền chưa điều chỉnh 2 lần.'], '—',
      ['Bước 2: tăng dần theo Số báo có, dòng đầu TPE.PBC0126.00001.', 'Bước 3: tăng dần theo mã ngân hàng, dòng đầu ngân hàng MB.',
       'Bước 4: giảm dần, dòng đầu TPE.PBC1026.00051 "27,445,230,000".']),
    T(21, 'Sắp xếp theo Ngày hạch toán', 'P1', PRE, [MENU, 'Bấm tiêu đề Ngày hạch toán.', 'Bấm lại.'], '—',
      ['Lần 1: cũ nhất trên cùng — TPE.PBC0825.00003 "31/07/2025 09:06".', 'Lần 2: mới nhất trên cùng (20/10/2026).',
       'Màn không có cột Ngày tạo / Ngày cập nhật riêng.']),
    T(22, 'Cột không hỗ trợ sắp xếp', 'P2', PRE,
      [MENU, 'Bấm tiêu đề Người tạo, Khách hàng, Ghi chú, STK ngân hàng, Trạng thái, Điều chỉnh công nợ.'], '—',
      ['Các tiêu đề này không có biểu tượng sắp xếp.', 'Bấm không đổi thứ tự, không nạp lại.']),
    T(23, 'Giữ sắp xếp khi chuyển trang', 'P1', PRE, [MENU, 'Bấm tiêu đề Số báo có (tăng dần).', 'Sang trang 2.'], '—',
      ['Trang 2 tiếp tục thứ tự tăng dần của trang 1.', 'Mũi tên sắp xếp vẫn ở cột Số báo có.']),
    T(24, 'Về trang 1 khi đổi sắp xếp', 'P1', PRE, [MENU, 'Sang trang 4.', 'Bấm tiêu đề Ngày hạch toán.'], '—',
      ['Danh sách quay về trang 1, sắp theo Ngày hạch toán tăng dần.']),
    T(25, 'Không có dòng của phiếu không đủ điều kiện', 'P0',
      [PRE, 'Có phiếu báo có Đang tạo TPE.PBC1126.00001; phiếu Thu nhà cung cấp TPE.PBC0826.00013 Đã duyệt; một dòng tài khoản 1121 '
            'của TPE.PBC1026.00052.'],
      [MENU, 'Tìm lần lượt "PBC1126.00001", "PBC0826.00013".', 'Tìm "PBC1026.00052", đếm số dòng.'], '—',
      ['Phiếu Đang tạo và phiếu Thu nhà cung cấp không ra dòng nào (' + EMPTY + ').',
       'TPE.PBC1026.00052 chỉ ra các dòng tài khoản 1311 / 1312 / 3311, không có dòng tài khoản 1121.']),
    T(26, 'Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE, 'Phiên đăng nhập đã hết hạn (đăng xuất ở tab khác).'],
      [MENU, 'Bấm sang trang 2.'], '—', ['Báo "Phiên đăng nhập đã hết hạn".', 'Tự chuyển về màn đăng nhập, không hiện dữ liệu.']),
]

# ============================================================== II. TÌM KIẾM VÀ LỌC
S2 = [
    T(1, 'Tìm theo số báo có chính xác', 'P0', [PRE, L52], [MENU, 'Nhập "TPE.PBC1026.00052", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPE.PBC1026.00052',
      ['Chỉ còn các dòng của TPE.PBC1026.00052: "Hiển thị 1–10 / 14".']),
    T(2, 'Tìm theo một phần số báo có', 'P0', PRE, [MENU, 'Nhập "00052", bấm Tìm kiếm.', 'Đổi thành "PBC0926", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: 00052', 'Ô tìm nhanh: PBC0926'],
      ['Bước 2: 97 dòng của mọi phiếu có số chứa "00052" (TPE.PBC1026.00052, TPE.PBC0626.00052…).', 'Bước 3: 561 dòng của các phiếu tháng 09/2026.']),
    T(3, 'Không phân biệt hoa / thường', 'P0', PRE, [MENU, 'Nhập "tpe.pbc1026.00052", bấm Tìm kiếm.', ADV,
                                                   'Làm mới, nhập Diễn giải = "nhatminh".'], ['Ô tìm nhanh: tpe.pbc1026.00052', 'Diễn giải: nhatminh'],
      ['Bước 2: ra 14 dòng như khi gõ chữ hoa.', 'Bước 4: ra dòng "NHATMINH TT HD 8026 …" (1 dòng).']),
    T(4, 'Có dấu / không dấu ở ô Ngân hàng', 'P1', PRE, [MENU, ADV, 'Nhập Ngân hàng = "Ngoại thương".', 'Đổi thành "Ngoai thuong".'],
      ['Ngân hàng: Ngoại thương', 'Ngân hàng: Ngoai thuong'],
      ['Bước 3: 3076 dòng VIETCOMBANK (khớp tên "Ngân hàng TMCP Ngoại thương Việt Nam").',
       'Bước 4: kết quả giống bước 3 nếu cơ sở dữ liệu so khớp không phân biệt dấu; ghi nhận nếu ra 0 dòng.']),
    T(5, 'Từ khóa không tồn tại', 'P1', PRE, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], 'Ô tìm nhanh: 999999999', ['Bảng hiện ' + EMPTY]),
    T(6, 'Ký tự đặc biệt trong ô tìm nhanh', 'P2', PRE, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "_", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: @#$<>', 'Ô tìm nhanh: _'],
      ['Bước 2: không lỗi, không treo; ' + EMPTY, 'Bước 3: không lỗi.',
       'Lưu ý: ký tự % và _ đang được hiểu là ký tự đại diện nên bước 3 ra toàn bộ 8043 dòng — ghi nhận nếu nghiệp vụ yêu cầu khớp đúng ký tự.']),
    T(7, 'Khoảng trắng đầu / cuối từ khóa', 'P1', PRE, [MENU, 'Nhập "  PBC1026.00052  ", bấm Tìm kiếm.'], 'Ô tìm nhanh: "  PBC1026.00052  "',
      ['Hệ thống bỏ khoảng trắng đầu / cuối, ra 14 dòng của TPE.PBC1026.00052.']),
    T(8, 'Xóa từ khóa', 'P1', 'Đang tìm "00052", bảng còn 97 dòng.', ['Bấm nút × trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
      ['Sau bước 1 bảng chưa đổi (ô tìm nhanh chỉ áp khi bấm Tìm kiếm).', 'Sau bước 2 hiện lại đủ 8043 dòng.']),
    T(9, 'Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P0', PRE, [MENU, 'Nhập "00052", nhấn Enter.', 'Làm mới, nhập lại "00052", bấm Tìm kiếm.'],
      'Ô tìm nhanh: 00052', ['Cả 2 cách đều ra 97 dòng, về trang 1.']),
    T(10, 'Giá trị mặc định của bộ lọc', 'P1', PRE, [MENU, ADV], '—',
      ['Ô tìm nhanh trống; Khách hàng, Diễn giải, Ngân hàng, STK ngân hàng, Người tạo, Trạng thái, Số tiền, Ngày hạch toán đều trống.',
       'Danh sách đủ 8043 dòng.']),
    T(11, 'Lọc Trạng thái', 'P0', PRE, [MENU, ADV, 'Mở ô Trạng thái, chọn "Đã điều chỉnh hết công nợ".', 'Đổi sang "Chưa điều chỉnh hết công nợ".'], '—',
      ['Ô có 2 lựa chọn: Đã điều chỉnh hết công nợ, Chưa điều chỉnh hết công nợ; lọc ngay khi chọn.',
       'Bước 3: 7987 dòng nhãn xanh, không có ô tích.', 'Bước 4: 56 dòng nhãn vàng, đều có ô tích.']),
    T(12, 'Lọc Ngân hàng, STK ngân hàng', 'P0', PRE, [MENU, ADV, 'Nhập Ngân hàng = "vietin".', 'Xóa Ngân hàng, nhập STK = "116000142872".'],
      ['Ngân hàng: vietin', 'STK ngân hàng: 116000142872'],
      ['Lọc ngay khi gõ, không cần bấm Tìm kiếm.', 'Bước 3: 2885 dòng, cột Ngân hàng đều "VIETINBANK".', 'Bước 4: 2883 dòng STK 116000142872.']),
    T(13, 'Lọc Diễn giải', 'P0', [PRE, L52], [MENU, ADV, 'Nhập Diễn giải = "NHATMINH TT HD 8026".'], 'Diễn giải: NHATMINH TT HD 8026',
      ['Còn 1 dòng TPE.PBC1026.00052 239,093,640 (lọc theo cột Ghi chú của dòng).']),
    T(14, 'Lọc Khách hàng', 'P0', [PRE, 'Khách "29TPHPTH-203 - KHÁCH KHÔNG RÕ" đang gắn với các dòng tiền chưa rõ khách.'],
      [MENU, ADV, 'Gõ "2" vào ô Khách hàng.', 'Gõ tiếp "29TPHPTH-203", chọn khách.'], 'Khách hàng: 29TPHPTH-203',
      ['Bước 3: gõ 1 ký tự chưa hiện gợi ý (cần tối thiểu 2 ký tự).', 'Bước 4: gợi ý dạng "Mã - Tên" (tối đa 50, tìm theo tên / SĐT / mã).',
       'Chọn xong lọc ngay: chỉ còn dòng có cột Khách hàng "29TPHPTH-203 - KHÁCH KHÔNG RÕ".']),
    T(15, 'Lọc Người tạo', 'P0', [PRE, 'Đào Thị Thúy tạo các phiếu có 20 dòng tiền về đủ điều kiện.'], [MENU, ADV, 'Chọn Người tạo = Đào Thị Thúy.'],
      'Người tạo: Đào Thị Thúy', ['20 dòng, cột Người tạo đều "Đào Thị Thúy" kèm mã phòng HN_QTTT.']),
    T(16, 'Lọc Số tiền từ – đến (lấy cả biên)', 'P0', [PRE, L52], [MENU, ADV, 'Nhập Số tiền từ 239,093,640 đến 239,093,640.'],
      ['Số tiền từ: 239093640', 'Số tiền đến: 239093640'], ['Ô tự định dạng "239,093,640".', 'Ra đúng 1 dòng 239,093,640 (biên được tính).',
                                         'Lọc theo Số tiền, không theo Số tiền chưa điều chỉnh.']),
    T(17, 'Lọc Ngày hạch toán lấy trọn ngày biên', 'P0', [PRE, 'Ngày 31/07/2025 có 12 dòng (TPE.PBC0825.00003, tạo 09:06).'],
      [MENU, ADV, 'Chọn Ngày hạch toán từ 31/07/2025 đến 31/07/2025.'], 'Ngày hạch toán: 31/07/2025 – 31/07/2025',
      ['Ra đủ 12 dòng ngày 31/07/2025.', 'Không có dòng ngày 30/07 hoặc 01/08.']),
    T(18, 'Kết hợp từ khóa với 1 ô lọc', 'P0', PRE, [MENU, 'Nhập "00052", bấm Tìm kiếm.', ADV, 'Chọn Trạng thái = Chưa điều chỉnh hết công nợ.'],
      ['Từ khóa: 00052', 'Trạng thái: Chưa điều chỉnh hết công nợ'], ['Còn 15 dòng (vừa khớp "00052" vừa còn tiền).', 'Dòng tổng giảm từ 97 xuống 15.']),
    T(19, 'Kết hợp 2 ô lọc với nhau', 'P0', PRE, [MENU, ADV, 'Nhập Ngân hàng = "VIETCOMBANK".', 'Chọn Trạng thái = Chưa điều chỉnh hết công nợ.'],
      ['Ngân hàng: VIETCOMBANK', 'Trạng thái: Chưa điều chỉnh hết công nợ'],
      ['Còn 28 dòng thỏa CẢ HAI điều kiện.', 'Bỏ ô Trạng thái thì nới ra 3076 dòng.']),
    T(20, 'Kết hợp cả 3 tiêu chí', 'P1', PRE,
      [MENU, 'Nhập "PBC1026", bấm Tìm kiếm.', ADV, 'Nhập Ngân hàng = "VIETCOMBANK".', 'Chọn Trạng thái = Chưa điều chỉnh hết công nợ.'],
      ['Từ khóa: PBC1026', 'Ngân hàng: VIETCOMBANK', 'Trạng thái: Chưa điều chỉnh hết công nợ'],
      ['Còn 24 dòng thỏa cả 3 tiêu chí.', 'Bấm Làm mới xóa cả 3 tiêu chí.']),
    T(21, 'Kết hợp tìm kiếm không có kết quả', 'P1', PRE, [MENU, 'Nhập "PBC1026.00052", bấm Tìm kiếm.', ADV, 'Nhập Ngân hàng = "VIETIN".'], '—',
      ['Bảng ' + EMPTY + ' vì TPE.PBC1026.00052 thuộc VIETCOMBANK.', 'Dưới bảng "Không có dòng nào.".']),
    T(22, 'Tổng số và phân trang sau lọc', 'P0', PRE, [MENU, ADV, 'Chọn Trạng thái = Chưa điều chỉnh hết công nợ.', 'Bấm trang cuối.'], '—',
      ['"Hiển thị 1–10 / 56"; có 6 trang.', 'Trang cuối "Hiển thị 51–56 / 56", 6 dòng.']),
    T(23, 'Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Chưa điều chỉnh hết công nợ.', ['Bấm tiêu đề Số tiền chưa điều chỉnh 2 lần.'], '—',
      ['Chỉ 56 dòng còn tiền được sắp giảm dần (dòng đầu 27,445,230,000); bộ lọc giữ nguyên.']),
    T(24, 'Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "00052", lọc Ngân hàng, Trạng thái, Ngày hạch toán, sắp theo Số tiền, ở trang 2.',
      ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống; bỏ sắp xếp.', 'Nạp lại từ trang 1, đủ 8043 dòng.']),
    T(25, 'Độ dài ô tìm nhanh', 'P2', PRE, [MENU, 'Dán chuỗi 300 ký tự vào ô tìm nhanh, bấm Tìm kiếm.'], 'Chuỗi 300 ký tự chữ và số',
      ['Ô nhận hết chuỗi, không lỗi, không treo.', 'Bảng ' + EMPTY, 'Lưu ý: ô chưa giới hạn số ký tự.']),
    T(26, 'Chuyển màn rồi quay lại', 'P1', 'Đang lọc Trạng thái = Chưa điều chỉnh hết công nợ.',
      ['Bấm một Số báo có để mở Chi tiết phiếu báo có.', 'Bấm nút Lùi của trình duyệt.', 'Vào màn khác bằng menu rồi quay lại màn này.'], '—',
      ['Cả 2 lần quay về: bộ lọc trống, hiện đủ 8043 dòng.',
       'Lưu ý: màn không ghi nhớ bộ lọc khi rời màn — ghi nhận nếu nghiệp vụ yêu cầu giữ bộ lọc.']),
    T(27, 'Tải lại trang (F5) khi đang lọc', 'P1', 'Đang lọc Ngân hàng = VIETIN.', ['Nhấn F5.'], '—',
      ['Màn mở lại với bộ lọc trống, đủ 8043 dòng (không giữ bộ lọc).']),
    T(28, 'Mở màn trong tab trình duyệt mới', 'P2', 'Đang lọc Ngân hàng = VIETIN ở tab 1.', ['Mở màn Tổng hợp tiền về ngân hàng ở tab mới.'], '—',
      ['Tab mới có bộ lọc trống; tab 1 vẫn giữ bộ lọc của nó.']),
    T(29, 'Đổi tài khoản trên cùng trình duyệt', 'P1', 'Tài khoản DNS Admin đang lọc Ngân hàng = VIETIN.',
      ['Đăng xuất.', 'Đăng nhập tài khoản A trên cùng trình duyệt.', MENU], '—', ['A thấy bộ lọc trống, không thấy bộ lọc của DNS Admin.']),
    T(30, 'Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích STK ngân hàng, bấm Lưu.', ADV], '—',
      ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô STK ngân hàng.']),
    T(31, 'Cài đặt bộ lọc: danh sách tiêu chí', 'P2', PRE, [MENU, 'Bấm Cài đặt bộ lọc.'], '—',
      ['Cửa sổ "Cài đặt bộ lọc" có 8 tiêu chí: Khách hàng, Diễn giải, Ngân hàng, STK ngân hàng, Người tạo, Trạng thái, Số tiền, '
       'Ngày hạch toán; đánh số 1–8.', 'Có nút Lưu, Khôi phục mặc định, Đóng, (x).']),
    T(32, 'Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô STK ngân hàng ở case trên.',
      ['Bấm Cài đặt bộ lọc, bấm Khôi phục mặc định, bấm Đóng.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
      ['Bước 1: đóng không lưu, ô STK ngân hàng vẫn ẩn.', 'Bước 2: tích lại đủ 8 tiêu chí, ô STK ngân hàng hiện lại.']),
    T(33, 'Cài đặt bộ lọc: kéo đổi thứ tự tiêu chí', 'P2', PRE, [MENU, 'Bấm Cài đặt bộ lọc, kéo Ngày hạch toán lên đầu, bấm Lưu.', ADV], '—',
      ['Ô Ngày hạch toán đứng đầu khối Tìm kiếm nâng cao.']),
    T(34, 'Cài đặt bộ lọc: ẩn tiêu chí đang có giá trị', 'P2', 'Đang lọc Ngân hàng = VIETIN (2885 dòng).',
      ['Bấm Cài đặt bộ lọc, bỏ tích Ngân hàng, bấm Lưu.'], '—', ['Ô Ngân hàng biến mất, giá trị VIETIN bị bỏ, danh sách về 8043 dòng.']),
]

# ============================================================== III. XEM CHI TIẾT (XEM PHIẾU BÁO CÓ)
S3 = [
    T(1, 'Mở chi tiết phiếu báo có từ Số báo có', 'P0', [PRE, L52], [MENU, 'Bấm "TPE.PBC1026.00052" ở dòng 1.'], '—',
      ['Chuyển sang màn chi tiết (trang riêng, không phải cửa sổ nổi).', 'Chuột phải vào Số báo có mở được ở tab mới.']),
    T(2, 'Tiêu đề màn chi tiết', 'P1', [PRE, L52], [MENU, 'Bấm "TPE.PBC1026.00052".'], '—',
      ['Tiêu đề "Chi tiết phiếu báo có: TPE.PBC1026.00052".']),
    T(3, 'Đầy đủ trường', 'P0', [PRE, L52], ['Mở chi tiết TPE.PBC1026.00052.'], '—',
      ['Khối Thông tin chung: Mã phiếu, Loại thu, Tài khoản nợ, Loại tiền, Tỷ giá, Ngày hạch toán, Người lập, Phòng ban, Ngân hàng, '
       'Tài khoản, Chi nhánh, Diễn giải.', 'Bảng Chi tiết đủ các dòng của phiếu; khối Đánh dấu không báo tiền về; khối Lịch sử.']),
    T(4, 'Khớp dữ liệu phiếu', 'P0', [PRE, L52], ['Mở chi tiết TPE.PBC1026.00052.'], '—',
      ['Mã phiếu TPE.PBC1026.00052; Loại thu Thu bán hàng; Ngày hạch toán 20/10/2026; Người lập Nguyễn Hồng Hải; Ngân hàng VIETCOMBANK; '
       'Tài khoản 0301002859668.', 'Diễn giải "Tiền về ngân hàng Vietcombank ngày 20/10/2026".']),
    T(5, 'Khớp danh sách', 'P0', [PRE, L52], [MENU, 'Tìm "PBC1026.00052" (14 dòng), ghi lại số tiền.', 'Mở chi tiết phiếu.'], '—',
      ['Các dòng tài khoản 1311 / 1312 / 3311 chưa đánh dấu Không báo tiền về ở màn chi tiết trùng 14 dòng trên danh sách (số tiền, diễn giải).']),
    T(6, 'Trường chỉ đọc', 'P1', [PRE, L52], ['Mở chi tiết TPE.PBC1026.00052.', 'Thử gõ vào các ô thông tin chung.'], '—',
      ['Mọi ô khóa, không sửa được.']),
    T(7, 'Không có nút Lưu', 'P1', [PRE, L52], ['Mở chi tiết TPE.PBC1026.00052.', 'Quan sát chân màn.'], '—',
      ['Không có nút Lưu, Sửa, Duyệt, Xóa (phiếu Đã duyệt).', 'Có nút Tạo phiếu yêu cầu điều chỉnh công nợ (phiếu còn dòng chưa điều chỉnh) và Quay lại.']),
    T(8, 'Phiếu đã điều chỉnh hết', 'P2', [PRE, 'Phiếu TPE.PBC0825.00003 mọi dòng Đã điều chỉnh hết.'], [MENU, 'Tìm "PBC0825.00003", bấm Số báo có.'], '—',
      ['Màn chi tiết mở bình thường, không có nút Tạo phiếu yêu cầu điều chỉnh công nợ.']),
    T(9, 'Đóng màn chi tiết', 'P0', [PRE, L52], ['Mở chi tiết TPE.PBC1026.00052.', 'Bấm Quay lại.'], '—',
      ['Về danh sách Phiếu báo có (không về màn Tổng hợp tiền về).',
       'Lưu ý: muốn về màn Tổng hợp phải dùng nút Lùi / menu — ghi nhận nếu nghiệp vụ yêu cầu Quay lại về đúng màn gốc.']),
    T(10, 'Giữ trang và bộ lọc khi quay lại', 'P1', 'Đang ở trang 3, lọc Trạng thái = Đã điều chỉnh hết công nợ.',
      ['Bấm Số báo có một dòng.', 'Bấm nút Lùi của trình duyệt.'], '—',
      ['Về màn Tổng hợp ở trang 1, bộ lọc trống (không giữ trang, bộ lọc).',
       'Lưu ý: hành vi theo thiết kế hiện tại — ghi nhận nếu yêu cầu giữ.']),
    T(11, 'Ngoài phạm vi xem phiếu báo có', 'P0', [ACC_A, L52], ['Đăng nhập A.', MENU, 'Bấm "TPE.PBC1026.00052".'], '—',
      ['A vẫn thấy dòng trên màn Tổng hợp (cùng công ty).', 'Màn chi tiết báo "Không tải được phiếu báo có", không hiện dữ liệu phiếu.']),
    T(12, 'Khu vực lịch sử ở màn chi tiết', 'P2', [PRE, L52], ['Mở chi tiết TPE.PBC1026.00052.', 'Kéo xuống khối Lịch sử.'], '—',
      ['Khối Lịch sử hiện các lần tạo / duyệt phiếu báo có (lịch sử của phiếu, không phải của màn Tổng hợp).']),
]

# ============================================================== IV. TÙY CHỈNH CỘT
COL = [MENU, 'Bấm nút biểu tượng cột (Cấu hình cột hiển thị).']
COL_PRE = [PRE, 'Tài khoản chưa từng lưu cấu hình cột.']
S4 = [
    T(1, 'Mở cửa sổ tùy chỉnh cột', 'P1', COL_PRE, COL, '—', ['Mở cửa sổ "Tuỳ chỉnh cột" có nút (x), dòng hướng dẫn.']),
    T(2, 'Danh sách cột', 'P1', COL_PRE, COL, '—',
      ['Đủ 12 cột: STT, Số báo có, Ngày hạch toán, Người tạo, Khách hàng, Ghi chú, Ngân hàng, STK ngân hàng, Số tiền, Số tiền chưa '
       'điều chỉnh, Trạng thái, Điều chỉnh công nợ.']),
    T(3, 'Cột được chọn mặc định', 'P1', COL_PRE, COL, '—', ['Cả 12 cột tích; dòng đếm "Đang chọn 12/12 cột".']),
    T(4, 'Hiện cột đang ẩn', 'P0', [PRE, 'Đã ẩn cột Người tạo.'], COL + ['Tích Người tạo, bấm Lưu.'], '—',
      ['Báo "Cập nhật thành công".', 'Bảng có lại cột Người tạo.']),
    T(5, 'Ẩn cột', 'P0', COL_PRE, COL + ['Bỏ tích Người tạo, bấm Lưu.'], '—', ['Báo "Cập nhật thành công".', 'Bảng không còn cột Người tạo.']),
    T(6, 'Cột bắt buộc không ẩn được', 'P0', COL_PRE, COL + ['Thử bỏ tích STT, Số báo có; di chuột lên biểu tượng cuối dòng.'], '—',
      ['STT, Số báo có: ô tích xám, biểu tượng ổ khóa, gợi ý "Cột bắt buộc — không thể ẩn hoặc đổi vị trí".',
       'Cột Điều chỉnh công nợ bỏ tích được.']),
    T(7, 'Kéo thả đổi thứ tự cột', 'P1', COL_PRE, COL + ['Kéo Điều chỉnh công nợ lên ngay sau Số báo có, bấm Lưu.'], '—',
      ['Cột Điều chỉnh công nợ đứng ngay sau Số báo có trên bảng; ô tích vẫn hoạt động.']),
    T(8, 'Cột cố định', 'P2', COL_PRE, COL + ['Thử kéo STT, Số báo có.', 'Đóng cửa sổ, cuộn bảng sang phải.'], '—',
      ['STT, Số báo có không kéo được.', 'STT, Số báo có ghim trái khi cuộn ngang.']),
    T(9, 'Lưu cấu hình với Chọn tất cả / Bỏ chọn hết', 'P1', COL_PRE, COL + ['Bấm Bỏ chọn hết, bấm Lưu.', 'Mở lại, bấm Chọn tất cả, bấm Lưu.'], '—',
      ['Bước 3: bảng chỉ còn STT, Số báo có.', 'Bước 4: bảng đủ 12 cột.']),
    T(10, 'Đóng không lưu', 'P1', COL_PRE, COL + ['Bỏ tích Ghi chú.', 'Bấm Đóng (hoặc (x) / click ra ngoài).', 'Mở lại cửa sổ.'], '—',
      ['Bảng vẫn có cột Ghi chú.', 'Mở lại thấy Ghi chú vẫn tích.']),
    T(11, 'Ghi nhớ sau khi tải lại', 'P0', 'Đã lưu cấu hình ẩn Người tạo ở TC_04.005.', ['Nhấn F5.'], '—', ['Bảng vẫn không có cột Người tạo.']),
    T(12, 'Cấu hình theo tài khoản', 'P1', 'DNS Admin đã ẩn cột Người tạo.', ['Đăng nhập A trên cùng trình duyệt, mở màn.',
                                                                            'Đăng nhập DNS Admin ở trình duyệt khác, mở màn.'], '—',
      ['A vẫn thấy cột Người tạo.', 'DNS Admin ở trình duyệt khác vẫn không có cột Người tạo (lưu theo tài khoản).']),
    T(13, 'Không ảnh hưởng dữ liệu', 'P1', COL_PRE, COL + ['Ẩn 4 cột, bấm Lưu.'], '—', ['Dòng tổng vẫn "Hiển thị 1–10 / 8043".']),
    T(14, 'Không ảnh hưởng lọc', 'P1', [PRE, 'Đang lọc Ngân hàng = VIETIN.'], COL + ['Ẩn cột Ngân hàng, bấm Lưu.'], '—',
      ['Bộ lọc giữ nguyên, vẫn 2885 dòng.']),
]

# ============================================================== V. XUẤT EXCEL
EXP = [MENU, 'Bấm Xuất Excel trên thanh công cụ.']
FILE = '"Tong-hop-tien-ve-ngan-hang.xlsx"'
S5 = [
    T(1, 'Mở cửa sổ chọn trường', 'P1', PRE, EXP, '—', ['Mở cửa sổ "Chọn trường xuất file", chưa tải file ngay.']),
    T(2, 'Danh sách trường', 'P0', PRE, EXP, '—',
      ['10 trường: Số báo có, Ngày hạch toán, Người tạo, Khách hàng, Diễn giải, Ngân hàng, STK ngân hàng, Số tiền, Số tiền chưa điều '
       'chỉnh, Trạng thái.', 'Không có trường Điều chỉnh công nợ; trường "Diễn giải" tương ứng cột Ghi chú trên bảng.']),
    T(3, 'Trường chọn mặc định', 'P1', [PRE, 'Đã ẩn cột Người tạo bằng Tùy chỉnh cột.'], EXP, '—',
      ['Cả 10 trường đều tích, "Đang chọn 10/10 trường" (kể cả Người tạo đang ẩn trên bảng).',
       'Lưu ý: cửa sổ không theo cột đang hiện trên bảng — ghi nhận nếu yêu cầu tích sẵn đúng cột đang hiện.']),
    T(4, 'Xuất với trường mặc định', 'P0', PRE, [MENU, ADV, 'Chọn Trạng thái = Chưa điều chỉnh hết công nợ.', 'Bấm Xuất Excel, bấm Xuất file.'], '—',
      ['Tải file ' + FILE + ', cửa sổ đóng, báo "Xuất Excel thành công.".', 'File có STT + 10 cột, 56 dòng dữ liệu.']),
    T(5, 'Xuất tất cả trường', 'P1', PRE, EXP + ['Bấm Bỏ chọn hết, rồi Chọn tất cả.', 'Bấm Xuất file.'], '—',
      ['"Đang chọn 10/10 trường".', 'File có STT + 10 cột.']),
    T(6, 'Xuất một số trường', 'P0', PRE, EXP + ['Bấm Bỏ chọn hết, tích Số báo có, Số tiền, Trạng thái.', 'Bấm Xuất file.'], '—',
      ['File đúng STT + 3 cột Số báo có, Số tiền, Trạng thái.']),
    T(7, 'Không chọn trường nào', 'P1', PRE, EXP + ['Bấm Bỏ chọn hết.'], '—', ['"Đang chọn 0/10 trường"; nút Xuất file bị khóa.']),
    T(8, 'Xuất theo từ khóa tìm kiếm', 'P1', PRE, [MENU, 'Tìm "PBC1026.00052".', 'Bấm Xuất Excel, Xuất file.'], '—',
      ['File chỉ gồm 14 dòng của TPE.PBC1026.00052.']),
    T(9, 'Xuất theo bộ lọc', 'P0', PRE, [MENU, ADV, 'Chọn Trạng thái = Chưa điều chỉnh hết công nợ, Ngày hạch toán 01/10/2026 – 20/10/2026.',
                                         'Xuất Excel, Xuất file.'], '—',
      ['File đúng 48 dòng, cột Trạng thái đều "Chưa điều chỉnh hết công nợ".',
       'Dưới tiêu đề có dòng "Từ ngày 01/10/2026 đến ngày 20/10/2026".']),
    T(10, 'Xuất nhiều trang', 'P0', PRE, [MENU, 'Đang ở trang 1 (10 dòng / trang).', 'Xuất Excel, Xuất file.'], '—',
      ['File có đủ 8043 dòng (không chỉ trang đang xem).', 'File tải xong không lỗi quá thời gian.']),
    T(11, 'Xuất danh sách rỗng', 'P0', PRE, [MENU, 'Tìm "ZZZ999".', 'Xuất Excel, Xuất file.'], '—',
      ['Vẫn tải file: logo, tiêu đề "TỔNG HỢP TIỀN VỀ NGÂN HÀNG", hàng tên cột.', 'Ngay dưới hàng tên cột 1 dòng gộp "Không có dữ liệu phù hợp".']),
    T(12, 'Tên file', 'P2', PRE, EXP + ['Bấm Xuất file.'], '—', ['Tên file ' + FILE + '.']),
    T(13, 'Định dạng và bố cục file', 'P1', PRE, EXP + ['Xuất file, mở bằng Excel.'], '—',
      ['Mở được, đuôi .xlsx.', 'Dòng 1 letterhead công ty Tân Phát rộng bằng bảng; dòng 2 tiêu đề "TỔNG HỢP TIỀN VỀ NGÂN HÀNG"; 1 dòng trống; '
       'rồi hàng tên cột in đậm.', 'Bảng có viền.']),
    T(14, 'Tiêu đề cột trong file', 'P1', PRE, EXP + ['Xuất file.'], '—',
      ['Hàng tên cột: STT, Số báo có, Ngày hạch toán, Người tạo, Khách hàng, Diễn giải, Ngân hàng, STK ngân hàng, Số tiền, Số tiền chưa '
       'điều chỉnh, Trạng thái.']),
    T(15, 'Thứ tự cột theo kéo thả', 'P1', PRE, EXP + ['Bỏ chọn hết; tích Số báo có, Trạng thái, Số tiền; kéo Số tiền lên đầu.', 'Xuất file.'], '—',
      ['File: STT, Số tiền, Số báo có, Trạng thái (đúng thứ tự kéo).']),
    T(16, 'Số lượng bản ghi', 'P0', PRE, [MENU, ADV, 'Nhập Ngân hàng = "VIETCOMBANK", chọn Trạng thái = Chưa điều chỉnh hết công nợ.', 'Xuất file.'], '—',
      ['File đúng 28 dòng dữ liệu, STT 1–28 (khớp dòng tổng trên màn).']),
    T(17, 'Dữ liệu khớp danh sách', 'P0', [PRE, L52], [MENU, ADV, 'Nhập Diễn giải = "NHATMINH TT HD 8026".', 'Xuất file.'], '—',
      ['Dòng 1: TPE.PBC1026.00052, 20/10/2026 08:26, Nguyễn Hồng Hải - HN_KTTV, diễn giải đầy đủ, VIETCOMBANK, 0301002859668, '
       '239,093,640, 239,093,640, Chưa điều chỉnh hết công nợ.', 'Giá trị từng ô trùng dòng trên bảng.']),
    T(18, 'Định dạng ngày / số / chữ', 'P1', PRE, EXP + ['Xuất file, mở Excel, chọn các ô Số tiền rồi xem thanh trạng thái.'], '—',
      ['Ngày hạch toán dạng dd/mm/yyyy hh:mm.', 'Số tiền, Số tiền chưa điều chỉnh là ô SỐ định dạng #,##0, Excel cộng SUM được, không cảnh báo "số dạng chữ".',
       'STK giữ nguyên số 0 đầu (0301002859668).', 'Trạng thái ghi tên nghiệp vụ.']),
    T(19, 'Tiếng Việt và ký tự đặc biệt', 'P2', PRE, EXP + ['Xuất file.'], '—',
      ['Người tạo "Nguyễn Hồng Hải - HN_KTTV", "Chưa điều chỉnh hết công nợ" đúng dấu, không vỡ phông.',
       'Diễn giải chứa ký tự "/", ".", ":" giữ nguyên; diễn giải bắt đầu bằng "=" giữ nguyên chữ, không thành công thức.']),
    T(20, 'Đóng cửa sổ không xuất', 'P2', PRE, EXP + ['Bấm Đóng (hoặc (x) / click ra ngoài).'], '—', ['Cửa sổ đóng, không tải file.']),
]

# ============================================================== VI. ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU
S6 = [
    T(1, 'Phiếu báo có vừa duyệt xuất hiện trên màn', 'P0', [ACC_A, 'Kế toán vừa duyệt phiếu báo có mới của công ty Tân Phát có 2 dòng tài khoản 1311.'],
      ['Đăng nhập A.', MENU, 'Tìm theo số báo có vừa duyệt.'], '—',
      ['Ra đủ 2 dòng, trạng thái "Chưa điều chỉnh hết công nợ", Số tiền chưa điều chỉnh = Số tiền.']),
    T(2, 'Phiếu Đang tạo chưa xuất hiện', 'P0', [ACC_A, 'Có phiếu báo có Đang tạo TPE.PBC1126.00001 (2 dòng 1311).'],
      [MENU, 'Tìm "PBC1126.00001".', 'Duyệt phiếu ở màn Phiếu báo có.', 'Quay lại màn Tổng hợp, tìm lại.'], '—',
      ['Bước 2: ' + EMPTY, 'Bước 4: ra 2 dòng.']),
    T(3, 'Đánh dấu Không báo tiền về', 'P0', [PRE, L52],
      ['Mở chi tiết TPE.PBC1026.00052, tích Không báo tiền về cho dòng 779,760.', 'Quay lại màn Tổng hợp, tìm "PBC1026.00052".',
       'Bỏ tích lại ở màn chi tiết, quay lại tìm.'], '—',
      ['Bước 1 báo "Cập nhật thành công.".', 'Bước 2: còn 13 dòng, không có dòng 779,760.', 'Bước 3: dòng 779,760 hiện lại (14 dòng).']),
    T(4, 'Trạng thái tự cập nhật theo phiếu kế toán', 'P0',
      [PRE, L52, 'Đã lập phiếu yêu cầu điều chỉnh công nợ từ dòng 779,760 và kế toán đã duyệt; Phiếu kế toán điều chỉnh 779,760 vừa được duyệt.'],
      [MENU, 'Tìm "PBC1026.00052".'], '—',
      ['Dòng 779,760: Số tiền chưa điều chỉnh "0", nhãn xanh "Đã điều chỉnh hết công nợ", không còn ô tích.']),
    T(5, 'Điều chỉnh một phần', 'P1', [PRE, L52, 'Phiếu kế toán điều chỉnh 39,093,640 cho dòng 239,093,640 vừa được duyệt.'],
      [MENU, 'Tìm "PBC1026.00052".'], '—', ['Dòng đó: Số tiền 239,093,640, Số tiền chưa điều chỉnh 200,000,000, vẫn "Chưa điều chỉnh hết", còn ô tích.']),
    T(6, 'Lưu phiếu yêu cầu chưa đổi số tiền', 'P0', [PRE, L52],
      ['Tích dòng 779,760, bấm Tạo mới điều chỉnh công nợ.', 'Nhập đủ, bấm Gửi duyệt.', 'Về màn Tổng hợp, tìm "PBC1026.00052".'], '—',
      ['Dòng 779,760 vẫn còn 779,760 chưa điều chỉnh (chỉ giảm khi phiếu kế toán được duyệt).']),
    T(7, 'Bộ lọc màn liên quan cập nhật', 'P1', [PRE, 'Dòng 779,760 vừa chuyển Đã điều chỉnh hết (TC_06.004).'],
      [MENU, ADV, 'Lọc Trạng thái = Chưa điều chỉnh hết công nợ.', 'Lọc Trạng thái = Đã điều chỉnh hết công nợ.'], '—',
      ['Bước 3 không còn dòng 779,760; tổng giảm 1.', 'Bước 4 có dòng 779,760.']),
    T(8, 'Không xóa phiếu đang có dòng được điều chỉnh', 'P1', [PRE, L52], ['Mở chi tiết TPE.PBC1026.00052 ở màn Phiếu báo có.'], '—',
      ['Phiếu Đã duyệt không có nút Xóa nên dòng tiền về đã dùng để điều chỉnh không bị mất.']),
    T(9, 'Cấp con đúng cấp cha', 'P1', [PRE, L52], [MENU, 'Tìm "PBC1026.00052".'], '—',
      ['14 dòng cùng Số báo có, cùng Ngày hạch toán, Người tạo, Ngân hàng VIETCOMBANK, STK 0301002859668 của phiếu cha.']),
    T(10, 'Tham chiếu không mất khi đổi trạng thái', 'P1', [PRE, 'Dòng 779,760 vừa chuyển Đã điều chỉnh hết.'], [MENU, 'Tìm "PBC1026.00052".'], '—',
      ['Dòng vẫn còn trên màn với đủ Số báo có, Ghi chú, Ngân hàng, Số tiền; chỉ đổi Số tiền chưa điều chỉnh và Trạng thái.']),
    T(11, 'Không có bản ghi mồ côi', 'P2', [PRE, 'Phiếu báo có Đang tạo bị xóa ở màn Phiếu báo có.'], [MENU, 'Tìm theo số phiếu vừa xóa.'], '—',
      [EMPTY + '; không còn dòng nào của phiếu đã xóa.']),
    T(12, 'Không có dữ liệu trùng', 'P2', PRE, [MENU, 'Đổi 100 dòng/trang, so 2 trang liên tiếp khi sắp theo Số báo có.'], '—',
      ['Không dòng nào lặp lại giữa 2 trang (các dòng cùng giá trị xếp ổn định).',
       'Hai dòng cùng phiếu, cùng số tiền, cùng diễn giải vẫn là 2 dòng khác nhau (sao kê có 2 khoản).']),
    T(13, 'Phiếu Thu nhà cung cấp không xuất hiện', 'P0', [PRE, 'Phiếu TPE.PBC0826.00013 loại Thu nhà cung cấp Đã duyệt, dòng tài khoản 3311.'],
      [MENU, 'Tìm "PBC0826.00013".'], '—', [EMPTY + ' (tiền nhà cung cấp hoàn lại không đưa vào đối chiếu).']),
]

# ============================================================== VII. PHÂN QUYỀN
S7 = renum([
    T(1, 'Xem danh sách không cần quyền riêng', 'P0', ACC_A, ['Đăng nhập A.', MENU], '—',
      ['A mở được màn, thấy đủ 8043 dòng của công ty Tân Phát như DNS Admin.']),
    T(2, 'Phạm vi dữ liệu theo công ty', 'P0', ACC_B, ['Đăng nhập B.', MENU, 'Tìm "PBC1026.00052".'], '—',
      ['B chỉ thấy 5 dòng của công ty 2.', 'Tìm "PBC1026.00052" (phiếu của Tân Phát): ' + EMPTY]),
    T(3, 'Chưa gắn công ty', 'P1', ACC_C, ['Đăng nhập C.', MENU, 'Xuất Excel, Xuất file.'], '—',
      ['Bảng ' + EMPTY, 'File Excel chỉ có dòng "Không có dữ liệu phù hợp".']),
    T(4, 'Xem chi tiết theo quyền của màn Phiếu báo có', 'P0', [ACC_A, L52, 'Tài khoản D: có quyền Xem tất cả phiếu báo có của công ty, công ty Tân Phát.'],
      ['Đăng nhập A, bấm "TPE.PBC1026.00052".', 'Đăng nhập D, bấm "TPE.PBC1026.00052".'], '—',
      ['A: "Không tải được phiếu báo có".', 'D: mở được màn chi tiết.']),
    T(5, 'Không có chức năng Thêm mới / Sửa / Xóa / Khóa / Lịch sử', 'P1', 'Tài khoản DNS Admin (quyền cao nhất).', [MENU, 'Quan sát thanh công cụ và từng dòng.'], '—',
      ['Không có nút Thêm mới, Sửa, Xóa, Khóa / Mở khóa, Import Excel, Lịch sử ở màn.']),
    T(6, 'Xuất Excel trong phạm vi', 'P1', ACC_B, ['Đăng nhập B.', MENU, 'Xuất Excel, Xuất file.'], '—',
      ['File chỉ có 5 dòng của công ty 2; letterhead công ty 2.']),
    T(7, 'Gọi thẳng chức năng danh sách / xuất bỏ qua giao diện', 'P0', [ACC_B, L52],
      ['Dùng công cụ kiểm thử API, đăng nhập B, gọi thẳng chức năng lấy danh sách với từ khóa "PBC1026.00052".',
       'Gọi thẳng chức năng xuất Excel không kèm bộ lọc.'], '—',
      ['Bước 1: tổng 0, không trả dòng của Tân Phát.', 'Bước 2: file chỉ có 5 dòng của công ty 2.']),
    T(8, 'Ẩn / vô hiệu nút theo điều kiện', 'P0', [PRE, L50], [MENU, 'Lọc Trạng thái = Đã điều chỉnh hết công nợ.'], '—',
      ['Dòng Đã điều chỉnh hết không có ô tích (để trống, không hiện xám).', 'Nút Tạo mới điều chỉnh công nợ, Xuất Excel vẫn hiện.']),
    T(9, 'Mở thẳng đường dẫn chi tiết khi thiếu quyền', 'P1', [ACC_A, 'A đã lưu đường dẫn màn chi tiết TPE.PBC1026.00052.'],
      ['Đăng nhập A.', 'Dán đường dẫn vào thanh địa chỉ.'], '—', ['Báo "Không tải được phiếu báo có", không hiện dữ liệu phiếu.']),
    T(10, 'Đổi quyền giữa lúc thao tác', 'P2', 'Tài khoản D đang mở màn Tổng hợp.',
      ['Quản trị gỡ quyền Xem tất cả phiếu báo có của công ty của D.', 'D bấm một Số báo có của người khác tạo.', 'D bấm sang trang 2.'], '—',
      ['Bước 2: "Không tải được phiếu báo có".', 'Bước 3: danh sách vẫn đủ dòng của công ty (màn không phụ thuộc quyền đó).']),
    T(11, 'Đổi công ty làm việc giữa lúc thao tác', 'P2', 'Tài khoản A đang mở màn (công ty Tân Phát).',
      ['Quản trị chuyển A sang công ty 2.', 'A tải lại trang.'], '—', ['A chỉ còn thấy 5 dòng của công ty 2.']),
    T(12, 'Mục menu bị tắt', 'P2', 'Mục "Tổng hợp tiền về ngân hàng" của phân hệ Tài chính bị tắt ở màn Cài đặt phân hệ.',
      ['Đăng nhập tài khoản thường.', 'Mở phân hệ Tài chính.', 'Gõ thẳng đường dẫn màn.'], '—',
      ['Không thấy mục menu.', 'Chuyển sang trang báo chức năng không khả dụng.']),
])

# ============================================================== VIII. CHỌN DÒNG VÀ TẠO MỚI ĐIỀU CHỈNH CÔNG NỢ
S8 = [
    T(1, 'Tích chọn dòng còn tiền', 'P0', [PRE, L52], [MENU, 'Tích ô cột Điều chỉnh công nợ ở dòng 1 và dòng 2.'], '—',
      ['Hai ô hiện dấu tích; không có thông báo.']),
    T(2, 'Dòng đã điều chỉnh hết không chọn được', 'P0', [PRE, L50], [MENU, 'Tìm "PBC1026.00050", quan sát cột Điều chỉnh công nợ.'], '—',
      ['Dòng 1,178,100 (Số tiền chưa điều chỉnh 0) không có ô tích.']),
    T(3, 'Chặn chọn 2 phiếu báo có khác nhau', 'P0', [PRE, L52, L51],
      [MENU, P20, 'Tích dòng 1 (TPE.PBC1026.00052).', 'Tích dòng 15 (TPE.PBC1026.00051).'], '—',
      ['Báo ' + REJECT, 'Ô dòng 15 trở về không tích; dòng 1 vẫn tích.']),
    T(4, 'Bỏ tích rồi chọn phiếu khác', 'P1', [PRE, L52, L51], [MENU, P20, 'Tích dòng 1.', 'Bỏ tích dòng 1.', 'Tích dòng 15.'], '—',
      ['Bước 5 tích được, không báo lỗi (không còn dòng nào của phiếu cũ).']),
    T(5, 'Bấm Tạo mới khi chưa chọn dòng', 'P0', PRE, [MENU, 'Bấm Tạo mới điều chỉnh công nợ.'], '—', ['Báo ' + NONE, 'Đứng yên ở màn.']),
    T(6, 'Tạo mới điều chỉnh công nợ với dòng đã chọn', 'P0', [PRE, L52],
      [MENU, 'Tích dòng 239,093,640 và 779,760.', 'Bấm Tạo mới điều chỉnh công nợ.'], '—',
      ['Chuyển sang màn "Tạo phiếu yêu cầu điều chỉnh công nợ".', 'Số phiếu báo có "TPE.PBC1026.00052"; Người tạo, Phòng ban = người đăng nhập.',
       'Bảng Điều chỉnh từ có 2 dòng Số tiền 779,760 và 239,093,640; Tổng cộng bằng tổng 2 dòng; mỗi dòng kèm 1 dòng Điều chỉnh đến trống.',
       'Diễn giải trống (bắt buộc).']),
    T(7, 'Số tiền mang sang là số tiền chưa điều chỉnh', 'P1', [PRE, 'Dòng X có Số tiền 239,093,640, đã điều chỉnh 39,093,640.'],
      [MENU, 'Tích dòng X, bấm Tạo mới điều chỉnh công nợ.'], '—', ['Dòng Điều chỉnh từ có Số tiền 200,000,000.']),
    T(8, 'Loại phiếu theo phiếu báo có', 'P1', [PRE, 'Dòng Y gắn khách đã rõ (không phải KHÁCH KHÔNG RÕ) thuộc phiếu Thu bán hàng; dòng Z gắn KHÁCH KHÔNG RÕ.'],
      ['Tích dòng Y, bấm Tạo mới điều chỉnh công nợ.', 'Quay lại, tích dòng Z, bấm Tạo mới điều chỉnh công nợ.'], '—',
      ['Bước 1: Loại phiếu "Điều chỉnh công nợ khách hàng", bị khóa.', 'Bước 2: Loại phiếu chọn được (không khóa).']),
    T(9, 'Giữ dòng đã tích khi đổi trang / lọc', 'P0', [PRE, L52],
      [MENU, 'Tích dòng 1.', 'Sang trang 2 rồi về trang 1.', 'Lọc Ngân hàng = VIETIN rồi bấm Làm mới.'], '—',
      ['Dòng 1 vẫn tích sau mỗi bước.', 'Bấm Tạo mới điều chỉnh công nợ mang đúng dòng 1 sang.']),
    T(10, 'Mất dòng đã tích khi rời màn', 'P2', [PRE, L52], [MENU, 'Tích dòng 1.', 'Nhấn F5.'], '—',
      ['Không còn dòng nào được tích; bấm Tạo mới báo ' + NONE]),
    T(11, 'Quay lại từ màn đích không lưu', 'P1', [PRE, L52],
      [MENU, 'Tích dòng 1, bấm Tạo mới điều chỉnh công nợ.', 'Không nhập gì, bấm Quay lại.'], '—',
      ['Về màn Tổng hợp tiền về ngân hàng, không hỏi xác nhận.', 'Không có phiếu yêu cầu nào được tạo.']),
    T(12, 'Quay lại từ màn đích khi đã nhập', 'P1', [PRE, L52],
      ['Tích dòng 1, bấm Tạo mới điều chỉnh công nợ.', 'Nhập Diễn giải "Test".', 'Bấm Quay lại.'], 'Diễn giải: Test',
      ['Hiện hộp xác nhận rời trang (thay đổi chưa lưu).', 'Chọn rời: về màn Tổng hợp, không tạo phiếu.', 'Chọn ở lại: giữ nguyên form.']),
    T(13, 'Lưu phiếu yêu cầu và quay về', 'P0', [PRE, L52],
      ['Tích dòng 779,760, bấm Tạo mới điều chỉnh công nợ.', 'Nhập Diễn giải, chọn Khách hàng, Hợp đồng ở dòng Điều chỉnh đến, Số tiền 779,760.',
       'Bấm Lưu nháp.'], ['Diễn giải: Chuyển tiền về đúng khách', 'Số tiền: 779,760'],
      ['Báo lưu thành công theo màn Phiếu yêu cầu điều chỉnh công nợ, quay về màn Tổng hợp tiền về ngân hàng.',
       'Phiếu yêu cầu mới có Số phiếu báo có TPE.PBC1026.00052 ở danh sách Phiếu yêu cầu điều chỉnh công nợ.']),
    T(14, 'Thiếu Diễn giải ở màn đích', 'P0', [PRE, L52], ['Tích dòng 1, bấm Tạo mới điều chỉnh công nợ.', 'Bỏ trống Diễn giải, bấm Lưu nháp.'], '—',
      ['Ô Diễn giải viền đỏ kèm thông báo lỗi bắt buộc của màn đó; không lưu.']),
    T(15, 'Gọi thẳng màn tạo với dòng của 2 phiếu', 'P2', [PRE, L52, L51],
      ['Sửa đường dẫn màn tạo để chứa 1 dòng của TPE.PBC1026.00052 và 1 dòng của TPE.PBC1026.00051.'], '—',
      ['Màn đích lấy Số phiếu báo có theo dòng đầu tiên và nạp cả 2 dòng.',
       'Lưu ý: chặn 2 phiếu báo có chỉ ở màn Tổng hợp — ghi nhận nếu cần chặn cả ở máy chủ.']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ DANH SÁCH VÀ TRUY CẬP', S1),
    ('II', 'TÌM KIẾM VÀ LỌC', S2),
    ('III', 'XEM CHI TIẾT', S3),
    ('IV', 'TÙY CHỈNH CỘT', S4),
    ('V', 'XUẤT EXCEL', S5),
    ('VI', 'ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU', S6),
    ('VII', 'PHÂN QUYỀN', S7),
    ('VIII', 'CHỌN DÒNG VÀ TẠO MỚI ĐIỀU CHỈNH CÔNG NỢ', S8),
]
check_no_dash_pre(SECTIONS, [])

if __name__ == '__main__':
    n = sum(len(s[2]) for s in SECTIONS)
    p0 = sum(1 for s in SECTIONS for c in s[2] if c[2] == 'P0')
    print('TC', n, 'P0', p0, '%.0f%%' % (100.0 * p0 / n))
    build(output_file=OUT, sheet_name='Trang tính1', feature_name='Tổng hợp tiền về ngân hàng - Cập nhật ngày 03/11/2026',
          module_name='Tổng hợp tiền về ngân hàng', description_block=DESCRIPTION_BLOCK, role_tcs=[], sections=SECTIONS)
