# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu báo hàng về" (phân hệ Thông báo, 3 tab) — skill testcase-documenter (tc_engine).

Chạy: python gen_testcase.py -> testcase.xlsx
03/11/2026: bản đầu theo checklist "Mẫu tài liệu.xlsx" (../phieu-theo-form-quoc-gia/checklist_mau_tai_lieu.json): section
  xếp theo thứ tự nhóm của checklist, BỎ nhóm màn không có (Thêm mới, Chỉnh sửa, Khóa/Mở khóa, Lịch sử thay đổi, Import Excel,
  Duyệt, Không duyệt), đánh số liền; rồi phần riêng (In phiếu, Tạo chứng từ từ phiếu). Một nhóm Phân quyền duy nhất
  (role_tcs=[]); case Cài đặt bộ lọc nằm trong nhóm Tìm kiếm và lọc. Đối chiếu từng dòng checklist ở gen_checklist.py.
Nguồn hành vi (đọc 03/11/2026, nhánh develop cả 2 repo):
  FE pages/lookup/product-arrived-notifies/** (index, tabConfigs, ArrivedNotifyList, detailPageMixin, import|inland|outside/_id),
     V2BaseSmartFilterPanel, V2BaseDataTable, V2BaseRowActions, export-fields-modal, column-customization-modal(+mixin),
     filter-customization-modal, ReportPrintPreviewModal, plugins/axios (hết phiên), pages/extras/404.
  BE Modules/Finance: ProductArrivedNotifySummaryService (phạm vi, lọc, xóa), ProductArrivedNotifySummaryController,
     ProductArrivedNotifyImportPrintService, ProductArrivedNotify2Export + blade, DynamicExport + blade dynamic,
     ProductImportRequestService (lập yêu cầu nhập hàng đánh dấu phiếu Đã yêu cầu nhập hàng), PermissionsTableSeeder.
  Số liệu dev-hrm 03/11/2026 (DNS Admin): tab Nhập khẩu 17 phiếu, Trong nước 0, Mua ngoài 878.
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
from tc_phieu_bosung import ListScreen, open_menu_case, combo_cases, check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Thông báo > menu "Thông báo" > bấm "Phiếu báo hàng về".'
TAB_IN = 'Bấm tab "Trong nước".'
TAB_OUT = 'Bấm tab "Mua ngoài".'
ADV = 'Bấm Tìm kiếm nâng cao.'

ACC_A = ('Tài khoản A: nhân viên mua hàng công ty 1, không có quyền xem phiếu báo hàng về theo cấp; A đang phụ trách mua '
         'thương hiệu HOZUMI ở công ty 1.')
ACC_B = 'Tài khoản B: nhân viên công ty 1, không có quyền xem theo cấp, không phụ trách thương hiệu nào.'
PRE_IMP = 'Tài khoản DNS Admin; tab Nhập khẩu trong phạm vi có 17 phiếu, cả 17 phiếu Đã gửi.'
PRE_OUT = 'Tài khoản DNS Admin; tab Mua ngoài có 878 phiếu (Đã gửi và Đã yêu cầu nhập hàng).'
IMP_667 = ('Phiếu PBHV-00667 nhập khẩu Đã gửi: tạo 21/10/2026 09:08, kho "SG - Kho Sài Gòn", invoice S77-077, hợp đồng '
           '"SHINWA 0926 HCM", người tạo Nguyễn Thị Thanh Trà; 1 dòng hàng HOZU-SDR-III, SL 1, khách 50TPHPTA-1166.')
OUT_2820 = ('Phiếu PBHV-02820 mua ngoài Đã gửi do DNS Admin tạo 27/10/2026 14:08, kho "LN - Liên Ninh", hợp đồng '
            '"HDMN-00892-0926/TPE-ASIN/ M019 TRAM CAN VMET" của CÔNG TY CỔ PHẦN ASIN VIỆT NAM; 1 dòng hàng TPE-COTTHEPM24, SL 1, '
            'SL nhập kho 1.')
A01 = 'A tạo phiếu PBHV-A01 nhập khẩu Đã gửi (invoice INV-A01, 2 dòng hàng, 1 dòng khuyến mại).'
A02 = 'A tạo phiếu PBHV-A02 nhập khẩu Đã yêu cầu nhập hàng.'
OUT_A = 'A tạo phiếu PBHV-A05 mua ngoài Đã gửi theo hợp đồng HĐMN-A1.'


def T(no, func, prio, pre, steps, td, exp):
    """Một test case. pre / td: chuỗi hoặc list (mỗi ý 1 dòng); steps: list (tự đánh số); exp: list (tự gạch đầu dòng)."""
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
     'Màn Phiếu báo hàng về (phân hệ Thông báo) để tra cứu các phiếu báo hàng mua sắp về kho, chia 3 tab: Nhập khẩu (hàng mua '
     'nước ngoài theo invoice), Trong nước (hàng mua trong nước theo hợp đồng mới), Mua ngoài (theo hợp đồng / phụ lục hợp đồng '
     'mua trong nước). Phiếu được lập ở hệ thống ERP; màn này chủ yếu chỉ đọc. Người tạo phiếu (phiếu Đã gửi) được Xóa phiếu '
     'nhập khẩu, Tạo phân bổ chi phí, Tạo phiếu yêu cầu nhập hàng. Mọi người trong phạm vi được In, Xuất Excel.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Tab Nhập khẩu: phiếu trong phạm vi quyền (xem mục 7).\n'
     '- Tab Trong nước, Mua ngoài: toàn bộ phiếu, không giới hạn theo quyền.\n'
     '- Trạng thái: Đã gửi (nhãn vàng), Đã yêu cầu nhập hàng (nhãn xanh lá).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Tab Nhập khẩu: phiếu Đã yêu cầu nhập hàng của người khác luôn ẩn.\n'
     '- Màn KHÔNG có Thêm mới, Chỉnh sửa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel, Lịch sử thay đổi.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Ngày tạo (tab Nhập khẩu, Mua ngoài) lọc theo ngày tạo phiếu, lấy trọn hai ngày biên. Tab Trong nước không có ô Ngày tạo.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu > dòng hàng hóa > dòng chi tiết khách (khách hàng, đơn đặt hàng, số lượng).\n'
     '- Phiếu nhập khẩu gắn 1 invoice; màn chi tiết còn hiện Khuyến mại, Hàng bảo hành, Hàng thừa thiếu của invoice.\n'
     '- Phiếu mua ngoài gắn hợp đồng hoặc phụ lục hợp đồng; có bảng Khuyến mại.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tổng SL dòng hàng nhập khẩu = tổng SL các dòng chi tiết khách.\n'
     '- Chênh lệch (mua ngoài) = SL trừ SL nhập kho.\n'
     '- Mỗi invoice chỉ có 1 phiếu báo hàng về nhập khẩu còn hiệu lực; xóa phiếu thì invoice lập lại được.'),
    ('7. Phân quyền cấp',
     '- Xem phiếu báo hàng về mua nhập khẩu theo tổng công ty: mọi phiếu nhập khẩu.\n'
     '- Xem phiếu báo hàng về mua nhập khẩu theo công ty: phiếu của công ty đang chọn làm việc.\n'
     '- Xem phiếu báo hàng về mua nhập khẩu theo phòng ban: phiếu của phòng ban mình quản lý.\n'
     '- Không có quyền nào: phiếu mình tạo + phiếu có hàng thuộc thương hiệu mình đang phụ trách mua.\n'
     '- Xóa, Tạo phân bổ chi phí, Tạo (phiếu) yêu cầu nhập hàng: chỉ người tạo phiếu, phiếu Đã gửi (không gắn quyền).'),
    ('8. Cách tính các ô thống kê',
     'Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng phiếu của tab khớp bộ lọc trong phạm vi.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (nhân viên mua hàng công ty 1, không quyền theo cấp, phụ trách thương hiệu HOZUMI), B (nhân viên '
     'khác), C (quyền theo tổng công ty), D (quyền theo công ty, công ty 1), E (quyền theo phòng ban, quản lý phòng Mua hàng 1), DNS '
     'Admin.\n'
     '- Lưu ý: mã invoice, hợp đồng, đơn đặt hàng mở màn của hệ thống ERP ở tab mới.\n'
     '- Lưu ý: màn chi tiết là TRANG riêng (không phải cửa sổ nổi).\n'
     '- Lưu ý: bộ lọc mỗi tab được ghi nhớ trên trình duyệt 10 phút kể từ lần đổi cuối.\n'
     '- Các case "dùng công cụ kiểm thử API" dành cho tester kỹ thuật.'),
]

# ============================================================== I. HIỂN THỊ DANH SÁCH VÀ TRUY CẬP
SCREEN = ListScreen(menu=MENU, title='Phiếu báo hàng về nhập khẩu', total=17, quick_label='mã phiếu',
                    quick_sample='PBHV-006', quick_hit='các phiếu PBHV-006xx',
                    filters=[('Kho', 'LN - Liên Ninh'), ('Trạng thái', 'Đã gửi')])
S1 = [
    open_menu_case(SCREEN, pre=PRE_IMP, extra=['- Mặc định mở tab Nhập khẩu (tab nền xanh nhạt).']),
    T(2, 'Tiêu đề màn hình và tiêu đề bảng theo tab', 'P0', [PRE_IMP, PRE_OUT],
      [MENU, 'Quan sát tiêu đề trên thanh trên cùng và tiêu đề bảng.', TAB_IN, TAB_OUT], '—',
      ['Tiêu đề màn và tab trình duyệt: "Phiếu báo hàng về".', 'Tab Nhập khẩu: bảng "Phiếu báo hàng về nhập khẩu".',
       'Tab Trong nước: "Phiếu báo hàng về trong nước".', 'Tab Mua ngoài: "Phiếu báo hàng về mua ngoài".']),
    T(3, 'Các nút chức năng được hiển thị', 'P0', PRE_IMP, [MENU, 'Quan sát khối bộ lọc và thanh công cụ của bảng.'], '—',
      ['Thanh tab: Nhập khẩu, Trong nước, Mua ngoài.',
       'Khối bộ lọc: ô tìm nhanh "Tìm theo mã phiếu", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
       'Thanh công cụ: Xuất Excel và nút biểu tượng cột (Cấu hình cột hiển thị).',
       'KHÔNG có nút Tạo mới, Import Excel.']),
    T(4, 'Các cột mặc định hiển thị tab Nhập khẩu', 'P0', [PRE_IMP, 'Tài khoản chưa từng lưu cấu hình cột.'],
      [MENU, 'Đọc tiêu đề cột từ trái sang phải.'], '—',
      ['Đúng 10 cột: STT, Mã, Ngày tạo, Kho, Nhà cung cấp, Invoice, Hợp đồng, Người tạo, Trạng thái, Hành động.',
       'STT và Mã ghim bên trái khi cuộn ngang.']),
    T(5, 'Các cột mặc định tab Trong nước, Mua ngoài', 'P1', 'Tài khoản chưa từng lưu cấu hình cột.', [MENU, TAB_IN, TAB_OUT], '—',
      ['Trong nước: STT, Mã, Ngày tạo, Hợp đồng, Nhà cung cấp, Kho, Trạng thái.',
       'Mua ngoài: STT, Mã, Ngày tạo, Kho, Hợp đồng, Nhà cung cấp, Trạng thái.', 'Hai tab này không có cột Hành động.']),
    T(6, 'Không có cột mặc định ẩn', 'P2', 'Tài khoản chưa từng lưu cấu hình cột.', [MENU, 'Bấm nút biểu tượng cột.'], '—',
      ['Cửa sổ "Tuỳ chỉnh cột" tích đủ 10/10 cột, không cột nào bị ẩn sẵn.']),
    T(7, 'Dữ liệu dòng khớp phiếu đã tạo (Nhập khẩu)', 'P0', [PRE_IMP, IMP_667], [MENU, 'Đối chiếu dòng PBHV-00667.'], '—',
      ['Mã PBHV-00667; Ngày tạo "21/10/2026 09:08"; Kho "SG - Kho Sài Gòn".', 'Invoice "S77-077"; Hợp đồng "SHINWA 0926 HCM" (chữ xanh gạch chân).',
       'Người tạo "Nguyễn Thị Thanh Trà"; Trạng thái nhãn vàng "Đã gửi".']),
    T(8, 'Dữ liệu dòng tab Mua ngoài', 'P1', [PRE_OUT, OUT_2820], [MENU, TAB_OUT, 'Đối chiếu dòng PBHV-02820.'], '—',
      ['Hợp đồng "HDMN-00892-0926/TPE-ASIN/ M019 TRAM CAN VMET".',
       'Nhà cung cấp "HDMN-00892-0926/TPE-ASIN/ M019 TRAM CAN VMET - CÔNG TY CỔ PHẦN ASIN VIỆT NAM".',
       'Kho "LN - Liên Ninh"; Trạng thái "Đã gửi".']),
    T(9, 'Nhãn trạng thái của phiếu', 'P0', PRE_OUT, [MENU, TAB_OUT, 'Quan sát cột Trạng thái các dòng.'], '—',
      ['Đã gửi: nhãn vàng.', 'Đã yêu cầu nhập hàng: nhãn xanh lá.', 'Cột Trạng thái không sắp xếp được.']),
    T(10, 'Danh sách chưa có dữ liệu (tab Trong nước)', 'P1', 'Hệ thống chưa có phiếu báo hàng về trong nước nào.', [MENU, TAB_IN], '—',
      ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Dưới bảng ghi "Không có phiếu nào.".', 'Không báo lỗi.']),
    T(11, 'Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_IMP, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
      ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Dưới bảng ghi "Không có phiếu nào.".']),
    T(12, 'Thay đổi số dòng / trang', 'P0', PRE_OUT, [MENU, TAB_OUT, 'Bấm sang trang 3.', 'Đổi ô Số dòng/trang từ 10 thành 20.'],
      'Số dòng/trang: 20', ['Bảng hiện 20 phiếu.', 'Tự quay về trang 1, dòng tổng "Hiển thị 1–20 / 878".', 'STT chạy từ 1 đến 20.']),
    T(13, 'Trang trước / trang tiếp theo', 'P0', PRE_OUT, [MENU, TAB_OUT, 'Bấm nút trang tiếp theo (›).', 'Bấm nút trang trước (‹).'], '—',
      ['Bước 3: sang trang 2, "Hiển thị 11–20 / 878".', 'Bước 4: về trang 1, "Hiển thị 1–10 / 878".']),
    T(14, 'Trang đầu / trang cuối', 'P1', PRE_OUT, [MENU, TAB_OUT, 'Bấm nút về trang cuối (»).', 'Bấm nút về trang đầu («).'], '—',
      ['Bước 3: trang 88, "Hiển thị 871–878 / 878", có đúng 8 dòng.', 'Bước 4: về trang 1.']),
    T(15, 'Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_OUT,
      [MENU, TAB_OUT, 'Ở trang 1 quan sát nút « và ‹.', 'Về trang cuối, quan sát nút › và ».'], '—',
      ['Trang 1: nút « và ‹ mờ, bấm không có tác dụng.', 'Trang cuối: nút › và » mờ, bấm không có tác dụng.']),
    T(16, 'STT liên tục giữa các trang', 'P0', PRE_OUT, [MENU, TAB_OUT, 'Sang trang 2, rồi trang 3.'], '—',
      ['Trang 2: STT từ 11 đến 20.', 'Trang 3: STT từ 21 đến 30.']),
    T(17, 'Tổng số bản ghi', 'P0', PRE_IMP, [MENU, 'Đọc dòng dưới bảng.', 'Đổi sang 20 dòng/trang.'], '—',
      ['Bước 2: "Hiển thị 1–10 / 17"; có 2 trang.', 'Bước 3: "Hiển thị 1–17 / 17", 1 trang.']),
    T(18, 'Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_OUT, [MENU, TAB_OUT, 'Sang trang 5.', ADV, 'Chọn Trạng thái = Đã gửi.'],
      'Trạng thái: Đã gửi', ['Danh sách tự nạp lại ở trang 1.', 'Dòng tổng "Hiển thị 1–10 / <số phiếu Đã gửi>".']),
    T(19, 'Sắp xếp tăng / giảm theo Mã', 'P0', PRE_IMP, [MENU, 'Bấm tiêu đề cột Mã.', 'Bấm tiêu đề cột Mã lần nữa.'], '—',
      ['Bước 2: mã xếp tăng dần (PBHV-00079 trên cùng), biểu tượng mũi tên lên.', 'Bước 3: mã xếp giảm dần, biểu tượng mũi tên xuống.']),
    T(20, 'Sắp xếp theo Ngày tạo', 'P1', PRE_IMP, [MENU, 'Bấm tiêu đề Ngày tạo.', 'Bấm tiêu đề Ngày tạo lần nữa.'], '—',
      ['Lần 1: cũ nhất trên cùng.', 'Lần 2: mới nhất trên cùng (PBHV-00667 21/10/2026).', 'Màn không có cột Ngày cập nhật.']),
    T(21, 'Cột không hỗ trợ sắp xếp', 'P2', PRE_IMP,
      [MENU, 'Bấm tiêu đề các cột Kho, Nhà cung cấp, Invoice, Hợp đồng, Người tạo, Trạng thái.'], '—',
      ['Các tiêu đề này không có biểu tượng sắp xếp.', 'Bấm vào không đổi thứ tự, không nạp lại danh sách.']),
    T(22, 'Giữ sắp xếp khi chuyển trang', 'P1', PRE_OUT, [MENU, TAB_OUT, 'Bấm tiêu đề Mã (tăng dần).', 'Sang trang 2.'], '—',
      ['Trang 2 tiếp tục thứ tự tăng dần của trang 1.', 'Biểu tượng sắp xếp vẫn ở cột Mã.']),
    T(23, 'Về trang 1 khi đổi sắp xếp', 'P1', PRE_OUT, [MENU, TAB_OUT, 'Sang trang 4.', 'Bấm tiêu đề cột Ngày tạo.'], '—',
      ['Danh sách quay về trang 1, sắp theo Ngày tạo tăng dần.']),
    T(24, 'Chuyển qua lại giữa các tab', 'P0', [PRE_IMP, PRE_OUT],
      [MENU, 'Lọc Trạng thái = Đã gửi ở tab Nhập khẩu.', TAB_OUT, 'Bấm lại tab "Nhập khẩu".'], '—',
      ['Tab Mua ngoài hiện danh sách riêng, bộ lọc riêng (không mang bộ lọc của tab Nhập khẩu sang).',
       'Quay lại tab Nhập khẩu vẫn còn Trạng thái = Đã gửi.', 'Tab đang chọn có nền xanh nhạt.']),
    T(25, 'Tải lại trang giữ đúng tab', 'P1', PRE_OUT, [MENU, TAB_OUT, 'Nhấn F5.'], '—',
      ['Màn mở lại đúng tab Mua ngoài (tab ghi trên đường dẫn trình duyệt).']),
    T(26, 'Sửa tay tham số tab trên thanh địa chỉ thành giá trị lạ', 'P1', [ACC_B, 'B không thấy phiếu nhập khẩu nào.'],
      ['Đăng nhập B.', MENU, 'Sửa phần tham số tab trên thanh địa chỉ thành "abc", nhấn Enter.'], '—',
      ['Hệ thống bỏ qua giá trị lạ, mở tab Nhập khẩu.', 'Vẫn chỉ thấy phiếu trong phạm vi của B (không lộ thêm), không báo lỗi.']),
    T(27, 'Bấm mã invoice / hợp đồng mở hệ thống ERP', 'P2', [PRE_IMP, IMP_667], [MENU, 'Bấm "S77-077".', 'Bấm "SHINWA 0926 HCM".'], '—',
      ['Mỗi lần mở 1 tab trình duyệt mới: màn invoice / hợp đồng mua của hệ thống ERP.', 'Màn danh sách giữ nguyên.']),
    T(28, 'Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_IMP, 'Phiên đăng nhập đã hết hạn (đăng xuất ở tab khác).'],
      [MENU, 'Bấm sang trang 2.'], '—', ['Báo "Phiên đăng nhập đã hết hạn".', 'Tự chuyển về màn đăng nhập, không hiện dữ liệu.']),
]

# ============================================================== II. TÌM KIẾM VÀ LỌC
PRE_F = PRE_IMP + '\nĐang ở tab Nhập khẩu.'
S2 = [
    T(1, 'Tìm theo mã phiếu chính xác', 'P0', PRE_F, [MENU, 'Nhập "PBHV-00667" vào ô tìm nhanh, bấm Tìm kiếm.'],
      'Ô tìm nhanh: PBHV-00667', ['Chỉ còn 1 dòng PBHV-00667.', 'Dòng tổng "Hiển thị 1–1 / 1".']),
    T(2, 'Tìm theo một phần mã phiếu', 'P0', PRE_F, [MENU, 'Nhập "00667", bấm Tìm kiếm.', 'Đổi thành "PBHV-006", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: 00667', 'Ô tìm nhanh: PBHV-006'], ['Bước 2: ra PBHV-00667.', 'Bước 3: ra mọi phiếu có mã chứa "PBHV-006" (PBHV-00667, 00650, 00609).']),
    T(3, 'Không phân biệt hoa / thường', 'P0', PRE_F, [MENU, 'Nhập "pbhv-00667", bấm Tìm kiếm.'], 'Ô tìm nhanh: pbhv-00667',
      ['Ra phiếu PBHV-00667 như khi gõ chữ hoa.']),
    T(4, 'Có dấu / không dấu ở ô Tên, mã hàng', 'P1', [PRE_OUT, OUT_2820],
      [MENU, TAB_OUT, ADV, 'Nhập Tên, mã hàng = "cot thep", bấm Tìm kiếm.', 'Đổi thành "CỘT THÉP", bấm Tìm kiếm.'],
      ['Tên, mã hàng: cot thep', 'Tên, mã hàng: CỘT THÉP'],
      ['Cả 2 bước đều ra PBHV-02820 (hàng "Cột thép trạm cân M24"): không phân biệt dấu thanh, hoa / thường.',
       'Lưu ý: mã phiếu không có dấu nên kiểm ở ô Tên, mã hàng.']),
    T(5, 'Từ khóa không tồn tại', 'P1', PRE_F, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], 'Ô tìm nhanh: 999999999',
      ['Bảng hiện "Không có dữ liệu phù hợp.".']),
    T(6, 'Ký tự đặc biệt trong ô tìm nhanh', 'P2', PRE_F, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'],
      ['Ô tìm nhanh: @#$<>', 'Ô tìm nhanh: %'],
      ['Bước 2: không lỗi, không treo; bảng "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi, không treo.',
       'Lưu ý: ký tự % và _ đang được hiểu là ký tự đại diện nên bước 3 ra toàn bộ 17 phiếu — ghi nhận nếu nghiệp vụ yêu cầu khớp đúng ký tự.']),
    T(7, 'Khoảng trắng đầu / cuối từ khóa', 'P1', PRE_F, [MENU, 'Nhập "  00667  " (2 dấu cách mỗi đầu), bấm Tìm kiếm.'],
      'Ô tìm nhanh: "  00667  "', ['Hệ thống bỏ khoảng trắng đầu / cuối, vẫn ra PBHV-00667.']),
    T(8, 'Xóa từ khóa', 'P1', 'Đang tìm "00667", bảng còn 1 dòng.', ['Bấm nút × trong ô tìm nhanh (hoặc xóa hết chữ).', 'Bấm Tìm kiếm.'], '—',
      ['Sau bước 1 bảng chưa đổi (ô gõ chỉ áp khi bấm Tìm kiếm).', 'Sau bước 2 hiện lại đủ 17 phiếu.']),
    T(9, 'Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P0', PRE_F,
      [MENU, 'Nhập "00667", nhấn Enter.', 'Làm mới, nhập lại "00667", bấm nút Tìm kiếm.'], 'Ô tìm nhanh: 00667',
      ['Cả 2 cách đều ra PBHV-00667, về trang 1.']),
    T(10, 'Giá trị mặc định của bộ lọc', 'P1', [PRE_F, 'Chưa lọc gì trong 10 phút gần nhất.'], [MENU, ADV], '—',
      ['Ô tìm nhanh trống; Nhà cung cấp, Invoice, Hợp đồng, Tên, mã hàng, Kho, Model, Barcode, Người tạo, Trạng thái, Ngày tạo đều trống.',
       'Danh sách hiện đủ 17 phiếu.']),
    T(11, 'Lọc Kho', 'P0', PRE_F, [MENU, ADV, 'Chọn Kho = "LN - Liên Ninh".'], 'Kho: LN - Liên Ninh',
      ['Lọc ngay khi chọn, không cần bấm Tìm kiếm.', 'Cột Kho mọi dòng đều "LN - Liên Ninh".']),
    T(12, 'Lọc Trạng thái', 'P0', PRE_OUT, [MENU, TAB_OUT, ADV, 'Chọn Trạng thái = Đã yêu cầu nhập hàng.'], 'Trạng thái: Đã yêu cầu nhập hàng',
      ['Chỉ còn phiếu nhãn xanh "Đã yêu cầu nhập hàng".', 'Ô Trạng thái có 2 lựa chọn: Đã yêu cầu nhập hàng, Đã gửi.']),
    T(13, 'Lọc Nhà cung cấp tab Nhập khẩu', 'P0', [PRE_F, 'Invoice S77-077 của phiếu PBHV-00667 thuộc nhà cung cấp NCC-X; không phiếu nào khác dùng NCC-X.'],
      [MENU, ADV, 'Gõ "N" vào ô Nhà cung cấp, gõ tiếp "NCC-X", chọn NCC-X.'], 'Nhà cung cấp: NCC-X',
      ['Gõ từ 1 ký tự đã hiện gợi ý dạng "Mã - Tên" (tối đa 30 đối tác đang hoạt động).', 'Ra đúng PBHV-00667 (lọc theo nhà cung cấp của invoice).']),
    T(14, 'Lọc Nhà cung cấp tab Mua ngoài', 'P1', [PRE_OUT, OUT_2820], [MENU, TAB_OUT, ADV, 'Chọn Nhà cung cấp = CÔNG TY CỔ PHẦN ASIN VIỆT NAM.'],
      'Nhà cung cấp: CÔNG TY CỔ PHẦN ASIN VIỆT NAM',
      ['Ra các phiếu có hợp đồng / phụ lục của nhà cung cấp này, gồm PBHV-02820.', 'Cột Nhà cung cấp đều chứa "ASIN VIỆT NAM".']),
    T(15, 'Lọc Invoice, Hợp đồng (ô gõ)', 'P1', [PRE_F, IMP_667],
      [MENU, ADV, 'Nhập Invoice = "S77", bấm Tìm kiếm.', 'Xóa Invoice, nhập Hợp đồng = "SHINWA", nhấn Enter.'],
      ['Invoice: S77', 'Hợp đồng: SHINWA'], ['Bước 3: ra PBHV-00667.', 'Bước 4: ra PBHV-00667.', 'Nhập xong chưa bấm Tìm kiếm / Enter thì bảng chưa đổi.']),
    T(16, 'Lọc Tên, mã hàng; Model; Barcode', 'P1', [PRE_F, IMP_667],
      [MENU, ADV, 'Nhập Tên, mã hàng = "HOZU", bấm Tìm kiếm.', 'Làm mới, nhập Model = "SDR-III", bấm Tìm kiếm.',
       'Làm mới, nhập Barcode = "ZZZ", bấm Tìm kiếm.'], ['Tên, mã hàng: HOZU', 'Model: SDR-III', 'Barcode: ZZZ'],
      ['Bước 3, 4: ra PBHV-00667 (phiếu có dòng hàng khớp).', 'Bước 5: "Không có dữ liệu phù hợp." (Barcode tìm theo Code đặt hàng).']),
    T(17, 'Lọc Người tạo', 'P1', [PRE_F, 'Nguyễn Thị Ngoan tạo 3 phiếu trong phạm vi.'], [MENU, ADV, 'Chọn Người tạo = Nguyễn Thị Ngoan.'],
      'Người tạo: Nguyễn Thị Ngoan', ['Đúng 3 phiếu, cột Người tạo đều "Nguyễn Thị Ngoan".']),
    T(18, 'Lọc Tên hàng, Mã hàng tab Trong nước', 'P2', 'Hệ thống chưa có phiếu trong nước.',
      [MENU, TAB_IN, ADV, 'Nhập Tên hàng = "cân", Mã hàng = "TPE", bấm Tìm kiếm.'], ['Tên hàng: cân', 'Mã hàng: TPE'],
      ['Tab Trong nước có đủ 6 ô: Hợp đồng, Tên hàng, Mã hàng, Nhà cung cấp, Kho, Trạng thái; KHÔNG có ô Ngày tạo.',
       'Bảng "Không có dữ liệu phù hợp.", không lỗi.']),
    T(19, 'Lọc Ngày tạo lấy trọn ngày biên', 'P0', [PRE_OUT, 'PBHV-02820 tạo 27/10/2026 14:08; PBHV-02819 tạo 27/10/2026 14:07.'],
      [MENU, TAB_OUT, ADV, 'Chọn Ngày tạo từ 27/10/2026 đến 27/10/2026.'], 'Ngày tạo: 27/10/2026 – 27/10/2026',
      ['Ra cả PBHV-02820 và PBHV-02819.', 'Không có phiếu ngày 26 hoặc 28.']),
    T(20, 'Kết hợp tìm kiếm với không có kết quả', 'P1', PRE_F,
      [MENU, 'Nhập "00667", bấm Tìm kiếm.', ADV, 'Chọn Kho = "LN - Liên Ninh".'], '—',
      ['Bảng "Không có dữ liệu phù hợp." vì PBHV-00667 thuộc kho Sài Gòn.', 'Dưới bảng "Không có phiếu nào.".']),
    T(21, 'Tổng số và phân trang sau lọc', 'P0', [PRE_OUT, 'Có 33 phiếu mua ngoài Đã gửi.'], [MENU, TAB_OUT, ADV, 'Chọn Trạng thái = Đã gửi.', 'Bấm trang cuối.'], '—',
      ['Dòng tổng "Hiển thị 1–10 / 33"; có 4 trang.', 'Trang cuối "Hiển thị 31–33 / 33", 3 dòng.']),
    T(22, 'Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Đã gửi ở tab Mua ngoài.', ['Bấm tiêu đề Mã.'], '—',
      ['Chỉ các phiếu Đã gửi được sắp tăng theo Mã; bộ lọc giữ nguyên.']),
    T(23, 'Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "PBHV-00", lọc Kho, Trạng thái, Ngày tạo, sắp theo Mã, đang ở trang 2.',
      ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống; bỏ sắp xếp theo Mã.', 'Nạp lại từ trang 1, đủ 17 phiếu.']),
    T(24, 'Chưa chọn Công ty thì ô Phòng ban (tab Mua ngoài)', 'P1', ACC_B,
      ['Đăng nhập B.', MENU, TAB_OUT, ADV, 'Mở ô Phòng ban khi ô Công ty còn trống.'], '—',
      ['Ô Phòng ban liệt kê phòng ban của mọi công ty.', 'B (không có quyền theo cấp) vẫn chọn được mọi công ty ở tab này.']),
    T(25, 'Chọn Công ty thì ô Phòng ban chỉ còn con của công ty đó', 'P0', [ACC_B, 'Công ty 1 có 5 phòng ban.'],
      [MENU, TAB_OUT, ADV, 'Chọn Công ty = Công ty 1.', 'Mở ô Phòng ban.'], 'Công ty: Công ty 1',
      ['Ô Phòng ban chỉ còn 5 phòng ban của Công ty 1.', 'Danh sách chỉ còn phiếu của Công ty 1.']),
    T(26, 'Đổi Công ty xóa Phòng ban, Bộ phận', 'P1', ACC_B,
      [MENU, TAB_OUT, ADV, 'Chọn Công ty 1, Phòng ban Mua hàng 1, Bộ phận BP1.', 'Đổi Công ty = Công ty 2.'], '—',
      ['Ô Phòng ban, Bộ phận bị xóa; danh sách lọc lại theo Công ty 2.']),
    T(27, 'Giữ bộ lọc khi mở màn chi tiết rồi quay lại', 'P0', 'Đang ở tab Nhập khẩu, đã chọn Kho = LN - Liên Ninh.',
      ['Bấm mã một phiếu để mở màn chi tiết.', 'Trong vòng 10 phút bấm Quay lại.'], '—',
      ['Quay về tab Nhập khẩu vẫn giữ Kho = LN - Liên Ninh.', 'Danh sách đúng theo bộ lọc đó, ở trang 1.']),
    T(28, 'Sang màn khác rồi quay lại trong 10 phút', 'P1', 'Đang ở tab Nhập khẩu, đã chọn Kho = LN - Liên Ninh.',
      ['Vào một màn khác bằng menu.', 'Quay lại màn Phiếu báo hàng về bằng menu trong 10 phút.'], '—',
      ['Bộ lọc Kho = LN - Liên Ninh vẫn còn.', 'Màn ghi nhớ bộ lọc mỗi khi đổi, không chỉ khi vào màn chi tiết.']),
    T(29, 'Bộ lọc hết hiệu lực sau 10 phút', 'P2', 'Đang ở tab Nhập khẩu, đã chọn Kho = LN - Liên Ninh.',
      ['Rời màn, chờ quá 10 phút không thao tác lọc.', 'Mở lại màn.'], '—', ['Bộ lọc trở về trống, hiện đủ 17 phiếu.']),
    T(30, 'Tải lại trang (F5) khi đang lọc', 'P0', 'Đang ở tab Mua ngoài, lọc Trạng thái = Đã gửi.', ['Nhấn F5.'], '—',
      ['Màn mở lại tab Mua ngoài, vẫn giữ Trạng thái = Đã gửi (trong 10 phút).']),
    T(31, 'Mở màn trong tab trình duyệt mới', 'P2', 'Đang ở tab Nhập khẩu, lọc Kho = LN - Liên Ninh.',
      ['Trong 10 phút mở màn Phiếu báo hàng về ở một tab trình duyệt mới.'], '—',
      ['Tab mới cũng có Kho = LN - Liên Ninh.', 'Bộ lọc dùng chung giữa các tab trên cùng trình duyệt.']),
    T(32, 'Đổi tài khoản trên cùng trình duyệt', 'P1', 'Tài khoản A đang lọc Kho = LN - Liên Ninh ở tab Nhập khẩu.',
      ['Đăng xuất A.', 'Đăng nhập tài khoản B trên cùng trình duyệt trong vòng 10 phút.', 'Mở màn Phiếu báo hàng về.'], '—',
      ['B thấy bộ lọc trống, KHÔNG thấy bộ lọc của A.',
       'Lưu ý: hiện bộ lọc lưu theo trình duyệt, không theo tài khoản; nếu B còn thấy Kho = LN - Liên Ninh thì ghi nhận lỗi.']),
    T(33, 'Bộ lọc nhớ riêng từng tab', 'P1', 'Không có bộ lọc nào đang lưu.',
      [MENU, 'Tab Nhập khẩu lọc Kho = LN - Liên Ninh.', TAB_OUT, 'Lọc Trạng thái = Đã gửi.', 'Bấm tab Nhập khẩu.'], '—',
      ['Tab Mua ngoài không có Kho = LN - Liên Ninh.', 'Quay về tab Nhập khẩu: Kho = LN - Liên Ninh, không có Trạng thái.']),
]
n2 = len(S2) + 1
S2 += combo_cases(SCREEN, n2)
n2 += 4
S2 += [
    T(n2, 'Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_F, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Model, bấm Lưu.'], '—',
      ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Model.', 'Tab Mua ngoài không bị ảnh hưởng (cấu hình riêng từng tab).']),
    T(n2 + 1, 'Cài đặt bộ lọc: danh sách tiêu chí theo tab', 'P2', PRE_F, [MENU, 'Bấm Cài đặt bộ lọc.', 'Đóng, sang tab Trong nước, bấm Cài đặt bộ lọc.'], '—',
      ['Tab Nhập khẩu: 10 tiêu chí đánh số 1–10.', 'Tab Trong nước: 6 tiêu chí.']),
    T(n2 + 2, 'Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Model ở case trên.',
      ['Bấm Cài đặt bộ lọc, bấm Khôi phục mặc định, bấm Đóng.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
      ['Bước 1: đóng không lưu, ô Model vẫn ẩn.', 'Bước 2: tích lại đủ 10 tiêu chí, ô Model hiện lại.']),
    T(n2 + 3, 'Cài đặt bộ lọc: kéo đổi thứ tự tiêu chí lọc', 'P2', PRE_F, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
      ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao.']),
]

# ============================================================== III. XÓA
S3 = [
    T(1, 'Điều kiện hiện nút Xóa', 'P0', [ACC_A, A01, A02, 'PBHV-00667 do người khác tạo, Đã gửi, có hàng HOZUMI (A thấy được).'],
      ['Đăng nhập A.', MENU, 'Quan sát cột Hành động 3 dòng.'], '—',
      ['PBHV-A01: có nút Xóa (thùng rác đỏ), In, Xuất Excel.', 'PBHV-A02 (Đã yêu cầu nhập hàng): không có nút Xóa.',
       'PBHV-00667 (người khác tạo): không có nút Xóa.']),
    T(2, 'Hộp xác nhận xóa', 'P0', [ACC_A, A01], [MENU, 'Bấm Xóa ở PBHV-A01.'], '—',
      ['Hộp tiêu đề "Xác nhận xóa" có biểu tượng cảnh báo đỏ và nút (x).', 'Hai nút Xóa (đỏ) và Hủy.']),
    T(3, 'Thông tin trong hộp xác nhận', 'P1', [ACC_A, A01], [MENU, 'Bấm Xóa ở PBHV-A01.'], '—',
      ['Nội dung "Bạn có chắc muốn xóa bản ghi này không?".',
       'Lưu ý: câu hỏi không ghi mã phiếu PBHV-A01 — ghi nhận nếu yêu cầu hiện mã phiếu trong hộp.']),
    T(4, 'Xóa phiếu thành công', 'P0', [ACC_A, A01, 'A đang thấy 3 phiếu ở tab Nhập khẩu.'],
      [MENU, 'Bấm Xóa ở PBHV-A01.', 'Bấm Xóa trong hộp.'], '—',
      ['Báo "Xóa thành công.".', 'Danh sách nạp lại, không còn PBHV-A01.', 'Dòng tổng giảm từ 3 xuống 2.']),
    T(5, 'Hủy xóa', 'P1', [ACC_A, A01], [MENU, 'Bấm Xóa ở PBHV-A01.', 'Bấm Hủy (hoặc (x), hoặc click ra ngoài hộp).'], '—',
      ['Hộp đóng, phiếu vẫn còn, không có thông báo.']),
    T(6, 'Phiếu đang được sử dụng không xóa được', 'P0', [ACC_A, A02], ['Đăng nhập A.', MENU, 'Quan sát dòng PBHV-A02.', 'Mở chi tiết PBHV-A02.'], '—',
      ['Không có nút Xóa ở cả danh sách và màn chi tiết (phiếu đã lập yêu cầu nhập hàng / phân bổ chi phí).']),
    T(7, 'Xóa phiếu có dữ liệu cấp con', 'P1', [ACC_A, A01],
      [MENU, 'Xóa PBHV-A01.', 'Lọc Tên, mã hàng theo mã một dòng hàng của PBHV-A01.'], '—',
      ['Xóa thành công, không hỏi thêm về dòng hàng.', 'Bước 3 không còn ra PBHV-A01 (dòng hàng, dòng chi tiết khách, khuyến mại, bảo '
       'hành của phiếu bị xóa theo).']),
    T(8, 'Phiếu đã bị người khác xóa', 'P1', [ACC_A, A01],
      ['Tab 1 mở danh sách.', 'Tab 2 xóa PBHV-A01.', 'Tab 1 bấm Xóa ở PBHV-A01, bấm Xóa.'], '—',
      ['Tab 1 báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang".', 'Bảng tự nạp lại, không còn PBHV-A01.']),
    T(9, 'Phiếu vừa được lập yêu cầu nhập hàng ở nơi khác', 'P0', [ACC_A, A01],
      ['Tab 1 mở danh sách.', 'Ở hệ thống ERP lập phân bổ chi phí từ PBHV-A01 (phiếu chuyển Đã yêu cầu nhập hàng).',
       'Tab 1 bấm Xóa PBHV-A01, bấm Xóa.'], '—',
      ['Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang".', 'Bảng nạp lại, dòng PBHV-A01 nhãn xanh, không còn nút Xóa.']),
    T(10, 'Không còn trên danh sách và tổng số sau xóa', 'P0', [ACC_A, A01, 'A thấy 3 phiếu.'],
      [MENU, 'Xóa PBHV-A01.', 'Tìm "PBHV-A01".', 'Bấm Làm mới.'], '—',
      ['Bước 3: "Không có dữ liệu phù hợp.".', 'Bước 4: "Hiển thị 1–2 / 2".']),
    T(11, 'Dữ liệu liên quan sau khi xóa', 'P1', [ACC_A, A01],
      ['Xóa PBHV-A01.', 'Ở hệ thống ERP mở invoice INV-A01, lập phiếu báo hàng về mới.'], '—',
      ['Invoice INV-A01 trở về chưa báo hàng về, lập được phiếu báo hàng về mới.',
       'Khuyến mại / bảo hành / thừa thiếu của invoice INV-A01 không bị xóa.']),
    T(12, 'Xóa từ màn chi tiết', 'P0', [ACC_A, A01], ['Mở chi tiết PBHV-A01.', 'Bấm Xóa ở chân màn, bấm Xóa.'], '—',
      ['Báo "Xóa thành công.", tự về tab Nhập khẩu.']),
    T(13, 'Bấm Xóa liên tục', 'P2', [ACC_A, A01], ['Bấm Xóa ở chân màn chi tiết, bấm Xóa trong hộp 2 lần thật nhanh.'], '—',
      ['Chỉ 1 lần xóa được thực hiện, 1 thông báo "Xóa thành công.".']),
]

# ============================================================== IV. XEM CHI TIẾT
S4 = [
    T(1, 'Mở màn chi tiết', 'P0', [PRE_IMP, IMP_667], [MENU, 'Bấm mã PBHV-00667.'], '—',
      ['Mở TRANG chi tiết (không phải cửa sổ nổi).', 'Chuột phải vào mã mở được ở tab mới.']),
    T(2, 'Tiêu đề màn chi tiết', 'P1', [PRE_IMP, IMP_667], [MENU, 'Bấm PBHV-00667.'], '—',
      ['Tiêu đề và tab trình duyệt "Chi tiết phiếu báo hàng về: PBHV-00667".', 'Không có nhãn trạng thái trên tiêu đề.']),
    T(3, 'Đầy đủ trường phiếu nhập khẩu', 'P0', [PRE_IMP, IMP_667], [MENU, 'Mở chi tiết PBHV-00667.'], '—',
      ['Thông tin chung: Số Invoice*, Hợp đồng, Nhập thẳng, Kho nhận*, Dự kiến về kho*, Ghi chú; góc phải "Nguyễn Thị Thanh Trà - 21/10/2026 09:08".',
       'Khối Chi tiết có ô Chi tiết và 4 tab Hàng hóa, Khuyến mại, Hàng bảo hành, Hàng thừa thiếu.',
       'Tab Hàng hóa: STT, PI, Model, Code đặt hàng, Hàng hóa, ĐVT, Tổng SL, Khách hàng, SL.']),
    T(4, 'Đầy đủ trường phiếu mua ngoài', 'P0', [PRE_OUT, OUT_2820], [MENU, TAB_OUT, 'Mở chi tiết PBHV-02820.'], '—',
      ['Thông tin chung: Số hợp đồng*, Kho nhập*, Nhập xuất thẳng, Dự kiến về kho*, Ghi chú.',
       'Tab Hàng hóa: STT, Tên hàng, Mã hàng, ĐVT, Tổng SL, Khách hàng, SL, SL nhập kho, Chênh lệch; tab Khuyến mại.',
       'Dòng TPE-COTTHEPM24: SL 1, SL nhập kho 1, Chênh lệch 0.']),
    T(5, 'Bố cục phiếu trong nước', 'P2', 'Có phiếu trong nước PBHV-T01 (dữ liệu chuẩn bị riêng, dev chưa có).', [MENU, TAB_IN, 'Mở chi tiết PBHV-T01.'], '—',
      ['Thông tin chung: Hợp đồng, Nhà cung cấp, Kho nhận, Ghi chú (không có dấu *).',
       'Bảng Hàng hóa: STT, Tên hàng hóa, Mã, Model, ĐVT, SL, Dự kiến hàng về, nhóm Chi tiết (Yêu cầu, Khách hàng, SL về).',
       'Chỉ hiện dòng có SL lớn hơn 0; dòng tồn kho công ty ghi "Tồn kho công ty".']),
    T(6, 'Dữ liệu khớp phiếu đã tạo', 'P0', [PRE_IMP, IMP_667], ['Mở chi tiết PBHV-00667.'], '—',
      ['Số Invoice S77-077, Hợp đồng SHINWA 0926 HCM, Kho nhận SG - Kho Sài Gòn, Dự kiến về kho 23/10/2026.',
       'Dòng hàng: Số PI PIV26-019, Ngày PI 15/09/2026, Model SDR-III, Mã hàng HOZU-SDR-III, ĐVT Bộ, Tổng SL 1.',
       'Khách hàng "50TPHPTA-1166" và "PDHNK-03694 - Nguyễn Văn Thu - KV4", SL 1.']),
    T(7, 'Dữ liệu khớp danh sách', 'P1', [PRE_IMP, IMP_667], [MENU, 'Ghi lại Kho, Invoice, Hợp đồng, Người tạo của dòng PBHV-00667.', 'Mở chi tiết.'], '—',
      ['Kho nhận, Số Invoice, Hợp đồng, người tạo trùng với dòng trên danh sách.']),
    T(8, 'Mọi trường chỉ đọc', 'P0', [PRE_IMP, IMP_667], ['Mở chi tiết PBHV-00667.', 'Thử gõ vào Kho nhận, Ghi chú, bấm ô Nhập thẳng.'], '—',
      ['Các ô nền xám, không gõ được.', 'Ô Nhập thẳng không đổi được.']),
    T(9, 'Không có nút Lưu', 'P1', [PRE_IMP, IMP_667], ['Mở chi tiết PBHV-00667 bằng tài khoản DNS Admin (không phải người tạo).'], '—',
      ['Chân màn chỉ có In, Xuất Excel, Quay lại; không có Lưu, Sửa.']),
    T(10, 'Phiếu Đã gửi của chính mình', 'P0', [ACC_A, A01], ['Đăng nhập A.', 'Mở chi tiết PBHV-A01.'], '—',
      ['Chân màn: Tạo phân bổ chi phí, In, Xuất Excel, Xóa, Quay lại.']),
    T(11, 'Phiếu đã kết thúc (Đã yêu cầu nhập hàng)', 'P1', [ACC_A, A02], ['Đăng nhập A.', 'Mở chi tiết PBHV-A02.'], '—',
      ['Chỉ còn In, Xuất Excel, Quay lại; không có Tạo phân bổ chi phí, Xóa.']),
    T(12, 'Ô Chi tiết và các tab của invoice', 'P1', [PRE_IMP, IMP_667],
      ['Mở chi tiết PBHV-00667.', 'Tích ô Chi tiết.', 'Bấm tab Khuyến mại, Hàng bảo hành, Hàng thừa thiếu.'], '—',
      ['Bước 2: dòng khách hiện thêm "Tên khách: CÔNG TY CỔ PHẦN LEXUS PHÚ MỸ HƯNG", "Ngày cần: 28/10/2026" (nhãn in đậm).',
       'Bước 3: invoice S77-077 không có dòng nên mỗi tab hiện "Không có dữ liệu".']),
    T(13, 'Bấm liên kết ở màn chi tiết', 'P2', [PRE_IMP, IMP_667], ['Mở chi tiết PBHV-00667.', 'Bấm "S77-077", "SHINWA 0926 HCM", "PDHNK-03694".'], '—',
      ['Mỗi lần mở màn invoice / hợp đồng / đơn đặt hàng của hệ thống ERP ở tab mới.']),
    T(14, 'Quay lại danh sách giữ bộ lọc', 'P0', 'Đang ở tab Mua ngoài, lọc Trạng thái = Đã gửi, sắp theo Mã, ở trang 3.',
      ['Bấm một mã phiếu ở trang 3.', 'Trong vòng 10 phút bấm Quay lại.'], '—',
      ['Về đúng tab Mua ngoài, giữ Trạng thái = Đã gửi và sắp theo Mã.',
       'Lưu ý: danh sách quay về trang 1, KHÔNG giữ trang 3 — ghi nhận nếu yêu cầu giữ cả trang.']),
    T(15, 'Mở chi tiết phiếu không tồn tại', 'P2', 'Phiếu PBHV-A01 vừa bị xóa, A còn giữ đường dẫn màn chi tiết.',
      ['Dán đường dẫn vào thanh địa chỉ.'], '—',
      ['Hiện trang "Không tìm thấy trang yêu cầu" kèm "Không tìm thấy hoặc không được cấp quyền truy cập trang" và nút Về trang chủ.']),
]

# ============================================================== V. TÙY CHỈNH CỘT
COL = [MENU, 'Bấm nút biểu tượng cột (Cấu hình cột hiển thị).']
COL_PRE = [PRE_IMP, 'Tài khoản chưa từng lưu cấu hình cột.']
S5 = [
    T(1, 'Mở cửa sổ tùy chỉnh cột', 'P1', COL_PRE, COL, '—', ['Mở cửa sổ "Tuỳ chỉnh cột" có nút (x) và dòng hướng dẫn.']),
    T(2, 'Danh sách cột', 'P1', COL_PRE, COL, '—',
      ['Đủ 10 cột: STT, Mã, Ngày tạo, Kho, Nhà cung cấp, Invoice, Hợp đồng, Người tạo, Trạng thái, Hành động.']),
    T(3, 'Cột được chọn mặc định', 'P1', COL_PRE, COL, '—', ['Cả 10 cột đang tích; dòng đếm "Đang chọn 10/10 cột".']),
    T(4, 'Hiện cột đang ẩn', 'P0', [PRE_IMP, 'Đã ẩn cột Invoice trước đó.'], COL + ['Tích Invoice, bấm Lưu.'], '—',
      ['Báo "Cập nhật thành công".', 'Bảng có lại cột Invoice.']),
    T(5, 'Ẩn cột', 'P0', COL_PRE, COL + ['Bỏ tích Người tạo, bấm Lưu.'], '—', ['Báo "Cập nhật thành công".', 'Bảng không còn cột Người tạo.']),
    T(6, 'Cột bắt buộc không ẩn được', 'P0', COL_PRE, COL + ['Thử bỏ tích STT, Mã, Hành động; di chuột lên biểu tượng cuối dòng.'], '—',
      ['STT, Mã: ô tích xám, có biểu tượng ổ khóa, gợi ý "Cột bắt buộc — không thể ẩn hoặc đổi vị trí".',
       'Hành động: ô tích xám không bỏ được, vẫn có biểu tượng ba gạch để kéo.']),
    T(7, 'Kéo thả đổi thứ tự cột', 'P1', COL_PRE, COL + ['Kéo biểu tượng ba gạch của Trạng thái lên ngay sau Mã, bấm Lưu.'], '—',
      ['Cột Trạng thái đứng ngay sau Mã trên bảng.']),
    T(8, 'Cột cố định', 'P2', COL_PRE, COL + ['Thử kéo STT, Mã.', 'Đóng cửa sổ, cuộn bảng sang phải.'], '—',
      ['STT, Mã không kéo được.', 'STT, Mã ghim bên trái khi cuộn ngang.']),
    T(9, 'Chọn tất cả / Bỏ chọn hết', 'P2', COL_PRE, COL + ['Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
      ['Bỏ chọn hết: bỏ tích mọi cột trừ STT, Mã, Hành động.', 'Chọn tất cả: tích đủ 10 cột.']),
    T(10, 'Đóng không lưu', 'P1', COL_PRE, COL + ['Bỏ tích Kho.', 'Bấm Đóng (hoặc (x) / click ra ngoài).', 'Mở lại cửa sổ.'], '—',
      ['Bảng vẫn có cột Kho.', 'Mở lại thấy Kho vẫn tích.']),
    T(11, 'Ghi nhớ sau khi tải lại', 'P0', 'Đã lưu cấu hình ẩn Người tạo ở TC_05.005.', ['Nhấn F5.'], '—', ['Bảng vẫn không có cột Người tạo.']),
    T(12, 'Cấu hình theo tài khoản', 'P1', 'A đã ẩn cột Người tạo ở tab Nhập khẩu.',
      ['Đăng nhập B trên cùng trình duyệt, mở màn.', 'Đăng nhập A ở trình duyệt khác, mở màn.'], '—',
      ['B vẫn thấy cột Người tạo.', 'A ở trình duyệt khác vẫn không có cột Người tạo (lưu theo tài khoản).']),
    T(13, 'Không ảnh hưởng dữ liệu', 'P1', COL_PRE, COL + ['Ẩn 4 cột, bấm Lưu.'], '—', ['Dòng tổng vẫn "Hiển thị 1–10 / 17".']),
    T(14, 'Không ảnh hưởng lọc', 'P1', [PRE_IMP, 'Đang lọc Kho = LN - Liên Ninh.'], COL + ['Ẩn cột Kho, bấm Lưu.'], '—',
      ['Bộ lọc Kho giữ nguyên, danh sách không đổi.']),
    T(15, 'Cấu hình riêng từng tab', 'P2', 'Đã ẩn cột Kho ở tab Nhập khẩu.', [MENU, TAB_OUT, 'Bấm nút biểu tượng cột.'], '—',
      ['Tab Mua ngoài vẫn có cột Kho; cửa sổ liệt kê 7 cột của tab Mua ngoài, "Đang chọn 7/7 cột".']),
]

# ============================================================== VI. XUẤT EXCEL
EXP = [MENU, 'Bấm Xuất Excel trên thanh công cụ.']
S6 = [
    T(1, 'Mở cửa sổ chọn trường', 'P1', PRE_IMP, EXP, '—', ['Mở cửa sổ "Chọn trường xuất file", chưa tải file ngay.']),
    T(2, 'Danh sách trường theo tab', 'P1', [PRE_IMP, PRE_OUT], EXP + ['Đóng, bấm tab Mua ngoài, bấm Xuất Excel.'], '—',
      ['Tab Nhập khẩu 8 trường: Mã, Ngày tạo, Kho, Nhà cung cấp, Invoice, Hợp đồng, Người tạo, Trạng thái.',
       'Tab Mua ngoài 6 trường: Mã, Ngày tạo, Kho, Hợp đồng, Nhà cung cấp, Trạng thái.']),
    T(3, 'Trường chọn mặc định', 'P1', [PRE_IMP, 'Đã ẩn cột Người tạo ở Tùy chỉnh cột.'], EXP, '—',
      ['Tích sẵn đúng các cột đang hiện: dòng đếm "Đang chọn 7/8 trường", Người tạo bỏ tích.']),
    T(4, 'Xuất với trường mặc định', 'P0', COL_PRE, EXP + ['Bấm Xuất file.'], '—',
      ['Cửa sổ đóng, tải file "phieu_bao_hang_ve_nhap_khau.xlsx".', 'Báo "Xuất Excel thành công.".', 'File có cột STT + 8 cột.']),
    T(5, 'Xuất tất cả trường', 'P1', PRE_IMP, EXP + ['Bấm Chọn tất cả.', 'Bấm Xuất file.'], '—', ['"Đang chọn 8/8 trường".', 'File có STT + 8 cột.']),
    T(6, 'Xuất một số trường', 'P0', PRE_IMP, EXP + ['Bấm Bỏ chọn hết, tích Mã, Invoice, Trạng thái.', 'Bấm Xuất file.'], '—',
      ['File đúng STT + 3 cột Mã, Invoice, Trạng thái.']),
    T(7, 'Không chọn trường nào', 'P1', PRE_IMP, EXP + ['Bấm Bỏ chọn hết.'], '—', ['"Đang chọn 0/8 trường"; nút Xuất file bị khóa.']),
    T(8, 'Xuất theo từ khóa tìm kiếm', 'P1', PRE_IMP, [MENU, 'Tìm "PBHV-006".', 'Bấm Xuất Excel, Xuất file.'], '—',
      ['File chỉ gồm 3 phiếu PBHV-00667, 00650, 00609.']),
    T(9, 'Xuất theo bộ lọc', 'P0', [PRE_OUT, 'Có 33 phiếu mua ngoài Đã gửi.'], [MENU, TAB_OUT, 'Lọc Trạng thái = Đã gửi.', 'Xuất Excel, Xuất file.'], '—',
      ['Tải "phieu_bao_hang_ve_mua_ngoai.xlsx" đúng 33 dòng, cột Trạng thái đều "Đã gửi".']),
    T(10, 'Xuất nhiều trang', 'P0', PRE_OUT, [MENU, TAB_OUT, 'Đang ở trang 1 (10 dòng / trang).', 'Xuất Excel, Xuất file.'], '—',
      ['File có đủ 878 dòng (không chỉ trang đang xem).']),
    T(11, 'Xuất danh sách rỗng', 'P0', PRE_OUT, [MENU, TAB_OUT, 'Tìm "ZZZ999".', 'Xuất Excel, Xuất file.'], '—',
      ['Vẫn tải file: có logo, tiêu đề "Phiếu báo hàng về mua ngoài", hàng tên cột, khối ký cuối.',
       'Không có dòng dữ liệu nào.']),
    T(12, 'Tên file', 'P2', PRE_IMP, [MENU, 'Xuất file ở từng tab.'], '—',
      ['Nhập khẩu: "phieu_bao_hang_ve_nhap_khau.xlsx".', 'Trong nước: "phieu_bao_hang_ve_trong_nuoc.xlsx".',
       'Mua ngoài: "phieu_bao_hang_ve_mua_ngoai.xlsx".']),
    T(13, 'Định dạng và bố cục file', 'P1', PRE_IMP, EXP + ['Xuất file, mở bằng Excel.'], '—',
      ['Mở được, đuôi .xlsx.', 'Dòng 1 logo; dòng 2 tiêu đề "Phiếu báo hàng về nhập khẩu"; dòng 3 tên cột; cuối file "Ngày ..., tháng ..., năm ...", '
       '"Người lập", "(Ký, họ tên)".', 'Bảng có viền.']),
    T(14, 'Tiêu đề cột trong file', 'P1', PRE_IMP, EXP + ['Bấm Chọn tất cả, Xuất file.'], '—',
      ['Hàng tên cột: STT, Mã, Ngày tạo, Kho, Nhà cung cấp, Invoice, Hợp đồng, Người tạo, Trạng thái.']),
    T(15, 'Thứ tự cột theo kéo thả', 'P1', PRE_IMP, EXP + ['Kéo Trạng thái lên đầu danh sách, Xuất file.'], '—',
      ['Trong file cột Trạng thái đứng ngay sau STT.']),
    T(16, 'Số lượng bản ghi', 'P0', [PRE_IMP, 'Kho LN - Liên Ninh có 12 phiếu trong phạm vi.'], [MENU, 'Lọc Kho = LN - Liên Ninh.', 'Xuất file.'], '—',
      ['File đúng 12 dòng dữ liệu, STT 1–12.']),
    T(17, 'Dữ liệu khớp danh sách', 'P0', [PRE_IMP, IMP_667], [MENU, 'Tìm "00667", Xuất file.'], '—',
      ['Dòng 1: PBHV-00667, 21/10/2026 09:08, SG - Kho Sài Gòn, S77-077, SHINWA 0926 HCM, Nguyễn Thị Thanh Trà, Đã gửi.', 'Giá trị từng ô trùng với dòng trên bảng.']),
    T(18, 'Định dạng ngày / chữ', 'P1', PRE_IMP, EXP + ['Bấm Chọn tất cả, Xuất file, mở Excel.'], '—',
      ['Ngày tạo dạng dd/mm/yyyy hh:mm.', 'Trạng thái ghi tên nghiệp vụ "Đã gửi" / "Đã yêu cầu nhập hàng".',
       'Lưu ý: mã invoice toàn chữ số (vd 202611428) có thể bị Excel coi là số — ghi nhận nếu cần giữ dạng chữ.']),
    T(19, 'Tiếng Việt và ký tự đặc biệt', 'P2', PRE_OUT, [MENU, TAB_OUT, 'Tìm "02820", Xuất file.'], '—',
      ['Ô Nhà cung cấp "… - CÔNG TY CỔ PHẦN ASIN VIỆT NAM" đúng dấu tiếng Việt.', 'Ký tự "/" trong mã hợp đồng giữ nguyên, không lỗi phông.']),
    T(20, 'Đóng cửa sổ không xuất', 'P2', PRE_IMP, EXP + ['Bấm Đóng (hoặc (x) / click ra ngoài).'], '—', ['Cửa sổ đóng, không tải file.']),
    T(21, 'Xuất Excel một phiếu nhập khẩu', 'P0', [PRE_IMP, IMP_667], [MENU, 'Ở dòng PBHV-00667 bấm biểu tượng Xuất Excel ở cột Hành động.'], '—',
      ['Tải ngay "phieu_bao_hang_ve_PBHV-00667.xlsx", không mở cửa sổ chọn trường; báo "Xuất Excel thành công.".',
       'File: letterhead công ty ghi trên phiếu, "PHIẾU BÁO HÀNG VỀ", ngày xuất; Số invoice S77-077, Kho nhập SG - Kho Sài Gòn, Dự kiến về '
       'kho 23/10/2026, Số hợp đồng SHINWA 0926 HCM, Người tạo, Ngày tạo 21/10/2026.',
       'Khối I. HÀNG HÓA 9 cột; Tổng SL, SL là ô số; cuối file "Người lập phiếu (Ký, họ tên)".']),
    T(22, 'Xuất Excel một phiếu từ màn chi tiết', 'P0', [PRE_IMP, IMP_667], ['Mở chi tiết PBHV-00667.', 'Bấm Xuất Excel ở chân màn.'], '—',
      ['Tải cùng file như TC_06.021; nút khóa trong lúc đang xuất.']),
]

# ============================================================== VII. ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU
YCNH = 'Vào phân hệ Tài chính, mở màn Phiếu yêu cầu nhập hàng, bấm Tạo mới, chọn loại "Nhập hàng mua ngoài", bấm ô Phiếu báo hàng về.'
S7 = [
    T(1, 'Phiếu mua ngoài Đã gửi xuất hiện ở màn yêu cầu nhập hàng', 'P0', [ACC_A, OUT_A], ['Đăng nhập A.', YCNH], '—',
      ['Cửa sổ chọn có PBHV-A05 (phiếu của A, Đã gửi).', 'Không có phiếu của người khác, không có phiếu Đã yêu cầu nhập hàng.']),
    T(2, 'Lập yêu cầu nhập hàng đổi trạng thái phiếu', 'P0', [ACC_A, OUT_A],
      ['Mở chi tiết PBHV-A05, bấm Tạo phiếu yêu cầu nhập hàng.', 'Chọn Kho nhập, Vận chuyển, bấm Lưu nháp.', 'Quay lại tab Mua ngoài.'], '—',
      ['Dòng PBHV-A05 chuyển nhãn xanh "Đã yêu cầu nhập hàng".', 'Mở lại chi tiết: không còn nút Tạo phiếu yêu cầu nhập hàng.']),
    T(3, 'Phiếu đã dùng không chọn lại được', 'P1', [ACC_A, 'PBHV-A05 đã Đã yêu cầu nhập hàng ở TC_07.002.'], [YCNH], '—',
      ['Cửa sổ chọn không còn PBHV-A05 (không lập 2 phiếu yêu cầu nhập hàng từ cùng phiếu).']),
    T(4, 'Không xóa phiếu đang được sử dụng', 'P0', [ACC_A, A02], [MENU, 'Quan sát PBHV-A02.', 'Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa PBHV-A02.'], '—',
      ['Không có nút Xóa.', 'Hệ thống từ chối "Trạng thái đã bị thay đổi. Vui lòng load lại trang", phiếu còn nguyên.']),
    T(5, 'Bộ lọc màn liên quan cập nhật', 'P1', [ACC_A, 'PBHV-A05 vừa chuyển Đã yêu cầu nhập hàng.'],
      [MENU, TAB_OUT, 'Lọc Trạng thái = Đã gửi.', 'Lọc Trạng thái = Đã yêu cầu nhập hàng.'], '—',
      ['Bước 3 không còn PBHV-A05; bước 4 có PBHV-A05.']),
    T(6, 'Xóa đồng bộ với invoice', 'P0', [ACC_A, A01], ['Xóa PBHV-A01.', 'Kiểm tra ở hệ thống ERP invoice INV-A01.'], '—',
      ['Invoice INV-A01 được đánh dấu chưa báo hàng về, lập lại phiếu báo hàng về được.', 'Tab Nhập khẩu không còn PBHV-A01 ở mọi tài khoản.']),
    T(7, 'Trạng thái tự cập nhật theo màn liên quan', 'P1', [ACC_A, A01],
      ['Ở hệ thống ERP lập phân bổ chi phí từ PBHV-A01.', 'Mở lại tab Nhập khẩu.'], '—',
      ['PBHV-A01 chuyển "Đã yêu cầu nhập hàng", không còn nút Xóa, Tạo phân bổ chi phí.']),
    T(8, 'Dữ liệu dòng hàng khớp màn yêu cầu nhập hàng', 'P1', [PRE_OUT, OUT_2820],
      ['Mở chi tiết PBHV-02820, bấm Tạo phiếu yêu cầu nhập hàng (tài khoản DNS Admin, người tạo phiếu).'], '—',
      ['Màn "Thêm phiếu yêu cầu nhập hàng": Loại "Nhập hàng mua ngoài", Phiếu báo hàng về "PBHV-02820".',
       'Hợp đồng "HDMN-00892-0926/TPE-ASIN/ M019 TRAM CAN VMET", Nhà cung cấp ASIN VIỆT NAM, dòng hàng Cột thép trạm cân M24 SL 1.']),
    T(9, 'Cấp con đúng cấp cha', 'P1', [PRE_IMP, IMP_667], ['Mở chi tiết PBHV-00667.'], '—',
      ['Tổng SL dòng hàng (1) bằng tổng SL các dòng khách (1).', 'Khuyến mại / bảo hành / thừa thiếu là của invoice S77-077.']),
    T(10, 'Tham chiếu không mất khi đổi trạng thái', 'P1', [ACC_A, 'PBHV-A05 đã Đã yêu cầu nhập hàng.'], ['Mở chi tiết PBHV-A05.'], '—',
      ['Hợp đồng, kho, dòng hàng, khách giữ nguyên như lúc Đã gửi.']),
    T(11, 'Không có bản ghi mồ côi sau xóa', 'P1', [ACC_A, A01], ['Xóa PBHV-A01.', 'Lọc tab Nhập khẩu theo Tên, mã hàng / Model / Barcode của dòng hàng PBHV-A01.'], '—',
      ['Không ra phiếu nào; không còn dòng hàng của phiếu đã xóa.']),
    T(12, 'Không có dữ liệu trùng', 'P2', PRE_IMP, [MENU, 'Đổi sang 100 dòng/trang, xem cột Invoice.'], '—',
      ['Mỗi invoice chỉ xuất hiện ở 1 phiếu.', 'Mã phiếu không trùng nhau.']),
]

# ============================================================== VIII. PHÂN QUYỀN
S8 = renum([
    T(1, 'Không có quyền nào: phiếu mình tạo + thương hiệu phụ trách', 'P0',
      [ACC_A, A01, 'Hệ thống có PBHV-00667 (người khác tạo) chứa hàng HOZUMI và PBHV-00650 (người khác tạo) không có hàng HOZUMI.'],
      ['Đăng nhập A.', MENU], '—',
      ['Thấy PBHV-A01 (mình tạo) và PBHV-00667 (hàng thương hiệu A phụ trách mua).', 'Không thấy PBHV-00650.']),
    T(2, 'Quyền theo tổng công ty', 'P0', 'Tài khoản C có quyền Xem phiếu báo hàng về mua nhập khẩu theo tổng công ty; công ty 1, 2 đều có phiếu.',
      ['Đăng nhập C.', MENU], '—', ['Thấy phiếu nhập khẩu của mọi công ty.', 'Không thấy phiếu Đã yêu cầu nhập hàng của người khác.']),
    T(3, 'Quyền theo công ty', 'P0', 'Tài khoản D có quyền Xem phiếu báo hàng về mua nhập khẩu theo công ty, đang làm việc ở công ty 1.',
      ['Đăng nhập D.', MENU, 'Đổi công ty làm việc sang công ty 2.'], '—',
      ['Bước 2: chỉ phiếu nhập khẩu của công ty 1.', 'Bước 3: chỉ phiếu của công ty 2.']),
    T(4, 'Quyền theo phòng ban', 'P1', 'Tài khoản E có quyền Xem phiếu báo hàng về mua nhập khẩu theo phòng ban, quản lý phòng Mua hàng 1.',
      ['Đăng nhập E.', MENU], '—', ['Chỉ thấy phiếu nhập khẩu của phòng Mua hàng 1.']),
    T(5, 'Phiếu Đã yêu cầu nhập hàng chỉ người tạo thấy', 'P0', ['Tài khoản C (tổng công ty).', A02],
      ['Đăng nhập C.', MENU, 'Tìm "PBHV-A02".', 'Đăng nhập A, tìm "PBHV-A02".'], '—',
      ['C: "Không có dữ liệu phù hợp.".', 'A: thấy PBHV-A02.']),
    T(6, 'Tab Trong nước, Mua ngoài không giới hạn', 'P0', [ACC_B, PRE_OUT], ['Đăng nhập B.', MENU, TAB_OUT], '—',
      ['B thấy đủ 878 phiếu mua ngoài như DNS Admin (tab không giới hạn theo quyền).']),
    T(7, 'Xem chi tiết theo phạm vi', 'P0', [ACC_B, IMP_667, 'B không thấy PBHV-00667 ở danh sách và đã lưu đường dẫn màn chi tiết của phiếu.'],
      ['Đăng nhập B.', 'Dán đường dẫn vào thanh địa chỉ.'], '—',
      ['Hiện trang "Không tìm thấy trang yêu cầu", không lộ dữ liệu phiếu.']),
    T(8, 'Không có chức năng Thêm mới', 'P1', 'Tài khoản DNS Admin (quyền cao nhất).', [MENU, 'Quan sát 3 tab.'], '—',
      ['Không có nút Tạo mới ở cả 3 tab (phiếu lập ở hệ thống ERP).']),
    T(9, 'Chỉ người tạo được xóa', 'P0', ['Tài khoản C (tổng công ty).', A01], ['Đăng nhập C.', MENU, 'Quan sát dòng PBHV-A01.', 'Mở chi tiết PBHV-A01.'], '—',
      ['Không có nút Xóa, Tạo phân bổ chi phí (C không phải người tạo).', 'Có In, Xuất Excel.']),
    T(10, 'Xuất Excel trong phạm vi xem', 'P1', [ACC_A, 'A thấy 2 phiếu nhập khẩu.'], ['Đăng nhập A.', MENU, 'Xuất Excel, Xuất file.'], '—',
      ['File chỉ có 2 phiếu của phạm vi A.', 'Màn không có Import Excel.']),
    T(11, 'In, Xuất Excel một phiếu ngoài phạm vi', 'P1', [ACC_B, IMP_667],
      ['Dùng công cụ kiểm thử API, đăng nhập B, gọi thẳng chức năng In và Xuất Excel của PBHV-00667.'], '—',
      ['Hệ thống báo "Không tìm thấy dữ liệu", không trả bản in / file.']),
    T(12, 'Ẩn nút khi không đủ điều kiện', 'P0', [ACC_A, A02], ['Đăng nhập A.', 'Mở chi tiết PBHV-A02.'], '—',
      ['Không có Xóa, Tạo phân bổ chi phí; nút ẩn hẳn, không hiện xám.']),
    T(13, 'Gọi thẳng chức năng Xóa khi không phải người tạo', 'P0', [ACC_B, 'B xem được tab Nhập khẩu nhưng không tạo phiếu PBHV-A01.', A01],
      ['Dùng công cụ kiểm thử API, đăng nhập B, gọi thẳng chức năng Xóa PBHV-A01, bỏ qua giao diện.'], '—',
      ['Hệ thống từ chối "Trạng thái đã bị thay đổi. Vui lòng load lại trang".', 'PBHV-A01 còn nguyên.']),
    T(14, 'Bị gỡ quyền giữa lúc xem', 'P2', 'Tài khoản C đang mở tab Nhập khẩu thấy phiếu công ty 2.',
      ['Quản trị gỡ quyền Xem phiếu báo hàng về mua nhập khẩu theo tổng công ty của C.', 'C bấm sang trang 2 / tải lại trang.'], '—',
      ['Danh sách thu hẹp về phiếu C tạo + thương hiệu C phụ trách mua.']),
    T(15, 'Quyền theo công ty nhưng chưa chọn công ty', 'P2', 'Tài khoản D có quyền theo công ty nhưng chưa chọn công ty làm việc.',
      ['Đăng nhập D.', MENU], '—', ['Tab Nhập khẩu "Không có dữ liệu phù hợp.".']),
    T(16, 'Màn không có Lịch sử thay đổi', 'P2', PRE_IMP, [MENU, 'Quan sát cột Hành động và màn chi tiết.'], '—',
      ['Không có nút Lịch sử / khối Lịch sử (màn chỉ đọc).']),
])

# ============================================================== IX. IN PHIẾU NHẬP KHẨU
S9 = [
    T(1, 'Mở cửa sổ xem trước bản in', 'P0', [PRE_IMP, IMP_667], [MENU, 'Bấm biểu tượng máy in ở dòng PBHV-00667.'], '—',
      ['Mở cửa sổ "Xem trước phiếu báo hàng về" ngay trên màn (không mở tab mới), khổ ngang.',
       'Trong lúc dựng hiện "Đang tải dữ liệu in…", nút In khóa.']),
    T(2, 'Nội dung bản in', 'P0', [PRE_IMP, IMP_667], [MENU, 'In PBHV-00667.'], '—',
      ['Letterhead công ty ghi trên phiếu; "PHIẾU BÁO HÀNG VỀ"; "Ngày <ngày in>".',
       'Số Invoice: S77-077; Kho nhận: SG - Kho Sài Gòn; Số hợp đồng: SHINWA 0926 HCM; Dự kiến về kho: 23/10/2026.',
       'I. HÀNG HÓA: STT, PI, Model, Code đặt hàng, Hàng hóa, ĐVT, Tổng SL, Khách hàng, SL; chỗ ký "NGƯỜI LẬP PHIẾU".']),
    T(3, 'Letterhead theo công ty ghi trên phiếu', 'P1', ['Tài khoản C thuộc công ty 2.', 'Phiếu PBHV-00667 của công ty 1.'],
      ['Đăng nhập C.', 'In PBHV-00667.'], '—', ['Letterhead là của công ty 1 (công ty trên phiếu), không phải công ty của C.']),
    T(4, 'Bấm In', 'P0', [PRE_IMP, IMP_667], ['In PBHV-00667.', 'Bấm nút In trong cửa sổ.'], '—',
      ['Mở hộp thoại in của trình duyệt, khổ A4 ngang, nội dung như bản xem trước.']),
    T(5, 'In từ màn chi tiết và đóng cửa sổ', 'P2', [PRE_IMP, IMP_667], ['Mở chi tiết PBHV-00667, bấm In.', 'Bấm (x) hoặc click ra ngoài cửa sổ.'], '—',
      ['Mở cùng cửa sổ xem trước.', 'Cửa sổ đóng, màn chi tiết giữ nguyên.']),
    T(6, 'Khối khuyến mại / bảo hành khi invoice có dữ liệu', 'P2', [ACC_A, A01], ['In PBHV-A01.'], '—',
      ['Sau khối I. HÀNG HÓA có "II. HÀNG KHUYẾN MẠI" với dòng khuyến mại của invoice.', 'Khối không có dòng thì không in.']),
]

# ============================================================== X. TẠO CHỨNG TỪ TỪ PHIẾU
S10 = [
    T(1, 'Điều kiện hiện nút Tạo phân bổ chi phí', 'P0', [ACC_A, A01, A02], ['Đăng nhập A.', 'Mở chi tiết PBHV-A01.', 'Mở chi tiết PBHV-A02.'], '—',
      ['PBHV-A01: có nút xanh "Tạo phân bổ chi phí".', 'PBHV-A02: không có nút.']),
    T(2, 'Bấm Tạo phân bổ chi phí', 'P0', [ACC_A, A01], ['Mở chi tiết PBHV-A01.', 'Bấm Tạo phân bổ chi phí.'], '—',
      ['Mở form tạo phân bổ chi phí của hệ thống ERP ở tab mới, phiếu PBHV-A01 chọn sẵn.', 'Màn chi tiết giữ nguyên, không đổi dữ liệu.']),
    T(3, 'Điều kiện hiện nút Tạo phiếu yêu cầu nhập hàng', 'P0', [PRE_OUT, OUT_2820, 'Phiếu PBHV-02818 Đã yêu cầu nhập hàng.'],
      [MENU, TAB_OUT, 'Mở chi tiết PBHV-02820.', 'Mở chi tiết PBHV-02818.'], '—',
      ['PBHV-02820 (DNS Admin tạo, Đã gửi): có nút "Tạo phiếu yêu cầu nhập hàng".', 'PBHV-02818: không có nút.']),
    T(4, 'Mở màn Thêm phiếu yêu cầu nhập hàng', 'P0', [PRE_OUT, OUT_2820], ['Mở chi tiết PBHV-02820.', 'Bấm Tạo phiếu yêu cầu nhập hàng.'], '—',
      ['Chuyển sang màn "Thêm phiếu yêu cầu nhập hàng" trong hệ thống (không mở tab mới).',
       'Loại yêu cầu "Nhập hàng mua ngoài", Phiếu báo hàng về "PBHV-02820" chọn sẵn; Kho nhập, Vận chuyển còn trống (bắt buộc).']),
    T(5, 'Rời màn yêu cầu nhập hàng không lưu', 'P1', [PRE_OUT, OUT_2820], ['Bấm Tạo phiếu yêu cầu nhập hàng ở PBHV-02820.', 'Bấm Quay lại (hệ thống hỏi xác nhận thì chọn Thoát).', 'Mở lại tab Mua ngoài.'], '—',
      ['PBHV-02820 vẫn "Đã gửi"; nút tạo vẫn còn ở màn chi tiết.']),
    T(6, 'Tạo yêu cầu nhập hàng từ phiếu trong nước', 'P2', ['Có phiếu trong nước PBHV-T01 Đã gửi do tài khoản đang dùng tạo (dữ liệu chuẩn bị riêng).'],
      ['Mở chi tiết PBHV-T01.', 'Bấm Tạo yêu cầu nhập hàng.'], '—',
      ['Mở form tạo yêu cầu nhập hàng của hệ thống ERP ở tab mới.', 'Người không phải người tạo không thấy nút.']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ DANH SÁCH VÀ TRUY CẬP', S1),
    ('II', 'TÌM KIẾM VÀ LỌC', S2),
    ('III', 'XÓA', S3),
    ('IV', 'XEM CHI TIẾT', S4),
    ('V', 'TÙY CHỈNH CỘT', S5),
    ('VI', 'XUẤT EXCEL', S6),
    ('VII', 'ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU', S7),
    ('VIII', 'PHÂN QUYỀN', S8),
    ('IX', 'IN PHIẾU NHẬP KHẨU', S9),
    ('X', 'TẠO PHÂN BỔ CHI PHÍ VÀ YÊU CẦU NHẬP HÀNG TỪ PHIẾU', S10),
]
check_no_dash_pre(SECTIONS, [])

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1', feature_name='Phiếu báo hàng về - Cập nhật ngày 03/11/2026',
          module_name='Phiếu báo hàng về', description_block=DESCRIPTION_BLOCK, role_tcs=[], sections=SECTIONS)
