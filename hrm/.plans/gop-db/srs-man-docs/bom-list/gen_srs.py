# -*- coding: utf-8 -*-
"""Sinh "SRS - BOM giải pháp.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/bom-list/{index,add}.vue · _id/{index,edit}.vue
      components/{BomBuilderEditor,BomBuilderInfoCard,BomBuilderTableCard,BomBuilderFooterBar,
      BomBuilderSubBomModal,BomBuilderEditModal,BomImportModal,BomExportModal,BomPrintConfigModal,
      BomPrintPreview,BomListLogModal}.vue
      pages/assign/quotations/components/QuotationProductSearchModal.vue (popup Thêm hàng hoá THẬT —
      BomBuilderAddProductModal.vue là code chết, không đặc tả) · pages/assign/components/cost/CostCatalogPanel.vue
      utils/mixins/bomPrintMixin.js · components/assign/SystemInfoSection.vue
      components/menu-sidebar.js (menuItemsAssign › Làm giải pháp › BOM Giải pháp)
  BE  Modules/Assign/Routes/api.php (prefix assign/bom-lists) · BomListController
      Services/BomListService (index/store/update/destroy/syncChildStatus/syncStatusFromSubmission/
      validateSolutionLevelType/validateUniqueAggregate/validateImportData) · Entities/BomList (isCanEdit/
      isCanDelete/getStatusList) · Entities/BomListLog · Http/Requests/BomList/BomListStoreRequest
      app/Http/Middleware/CheckSolutionMemberActive · app/Helper/PermissionHelper (checkPermissionListWithColumn)
  Quyền: PermissionsTableSeeder id 1031–1035 (nhóm "BOM List") + "Xem giá vốn hàng hoá"
Ảnh chụp thật (headless, 1440x900, client :3002): shots/ — chỉ để local.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'BOM giải pháp'
MENU = 'Phân hệ Công việc => Làm giải pháp => BOM Giải pháp'
A_LAP = 'Người lập BOM'
A_XEM = 'Người xem BOM'
TN_LAP = 'Nhân viên làm giải pháp (PM, trưởng nhóm, thành viên giải pháp / hạng mục); Người dùng đã đăng nhập'
TN_XEM = 'Người lập BOM, quản lý theo cấp, kinh doanh liên quan; Người dùng đã đăng nhập'
ICONS = {
    'Phân hệ Công việc': 'icon_phanhe.png',
    'Làm giải pháp': 'icon_nhom.png',
    'BOM Giải pháp': 'icon_man.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Cấu hình cột hiển thị': 'icon_cot.png',
    'Xuất Excel': 'icon_xuat.png',
    'Xuất file': 'icon_xuatfile.png',
    'Tạo mới': 'icon_taomoi.png',
    'Loại BOM LIST': 'icon_loaibom.png',
    'Chọn BL con': 'icon_chonblcon.png',
    'Gộp BOM con': 'icon_gop.png',
    'Thêm mới': 'icon_themmoi.png',
    'Thêm hàng tạm': 'icon_hangtam.png',
    'Thêm nhóm': 'icon_themnhom.png',
    'Thêm nhóm con': 'icon_themnhomcon.png',
    'Sửa (dòng hàng)': 'icon_suadong.png',
    'Thêm con': 'icon_themcon.png',
    'Xoá (dòng hàng)': 'icon_xoadong.png',
    'Import Excel': 'icon_import.png',
    'Mã BOM': 'icon_ma.png',
    'Sửa': 'icon_sua.png',
    'Xóa': 'icon_xoa.png',
    'Hành động khác': 'icon_more.png',
    'Sao chép': 'icon_saochep.png',
    'In BOM List': 'icon_in.png',
    'In': 'icon_ct_in.png',
    'Xem trước': 'icon_xemtruoc.png',
    'Lịch sử': 'icon_lichsu.png',
    'Lưu nháp': 'icon_luunhap.png',
    'Lưu BOM': 'icon_luubom.png',
}
NO_PERM = ('– Nếu không có quyền → nút không hiển thị; gọi thẳng chức năng thì hiển thị '
           '“Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.')
DK_LIST = ('Người dùng đã đăng nhập. Menu không gắn quyền riêng; dữ liệu hiển thị theo quyền phạm vi V1–V4 '
           '(không có quyền phạm vi nào thì chỉ thấy BOM do mình tạo).')

OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='bomgp_')
_ui = d.ui_table


def _ui_checked(rows, required=True, scope=True):
    n = 5 + (1 if required else 0) + (1 if scope else 0)
    for r in rows:
        assert len(r) == n, 'Sai số ô (%d != %d): %s' % (len(r), n, r[0])
    return _ui(rows, required=required, scope=scope)


d.ui_table = _ui_checked
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn BOM giải pháp (trên giao diện còn gọi là BOM List), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn BOM giải pháp.',
    'Làm rõ cách lập BOM thành phần (nhập hàng hoá, hàng tạm, dịch vụ – chi phí, chia nhóm 2 cấp, import Excel) '
    'và BOM tổng hợp (gộp các BOM con theo hạng mục / giải pháp).',
    'Làm rõ 6 trạng thái của BOM, nút nào hiện ở trạng thái nào, và mối liên hệ với hồ sơ trình duyệt hạng mục / '
    'giải pháp (nơi thực hiện duyệt BOM tổng hợp).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('BOM (BOM List)', 'Bảng kê hàng hoá, dịch vụ và chi phí cần dùng cho một giải pháp / hạng mục của dự án TKT. '
                       'Mã tự sinh dạng BOM-YYYY-NNNNN.'),
    ('BOM thành phần', 'BOM lập trực tiếp từ hàng hoá; là phần con để gộp vào BOM tổng hợp.'),
    ('BOM tổng hợp', 'BOM gộp từ các BOM con. Cấp hạng mục: gộp BOM thành phần của hạng mục. Cấp giải pháp: gộp '
                     'các BOM tổng hợp hạng mục đã duyệt (hoặc BOM thành phần nếu giải pháp không chia hạng mục).'),
    ('BL con / BOM con', 'BOM được chọn để gộp vào một BOM tổng hợp.'),
    ('Dự án TKT', 'Dự án tiền khả thi; mỗi dự án có 1 giải pháp.'),
    ('Giải pháp / Hạng mục', 'Giải pháp kỹ thuật của dự án và các hạng mục (phần việc) của giải pháp.'),
    ('Version GP / Version HM', 'Phiên bản hiện hành của giải pháp / hạng mục tại thời điểm lưu BOM (hệ thống tự ghi).'),
    ('Hàng ERP', 'Hàng hoá có sẵn trong danh mục hàng hoá ERP.'),
    ('Hàng tạm', 'Hàng chưa có trong danh mục ERP, nhập tay trong BOM; mã HHB… do hệ thống tự sinh khi lưu.'),
    ('Dịch vụ & Chi phí khác', 'Khoản dịch vụ / chi phí chọn từ danh mục dịch vụ – chi phí, nằm ở khối B của BOM.'),
    ('Nhóm hàng', 'Nhóm phân loại hàng trong BOM, tối đa 2 cấp (Cấp 1 đánh số La Mã I, II…; Cấp 2 đánh số I.1…).'),
    ('Hồ sơ trình duyệt', 'Hồ sơ gửi duyệt hạng mục / giải pháp; BOM tổng hợp đi kèm hồ sơ được duyệt theo hồ sơ.'),
    ('Q / V', 'Ký hiệu quyền thao tác (Q) và quyền phạm vi dữ liệu (V) ở Phần 2.'),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Tạo BOM List',
     'Hiện nút Tạo mới, Sao chép; vào được màn Tạo mới / Cập nhật; hiện nút Xóa (kèm điều kiện trạng thái và người '
     'tạo). Thiếu quyền mà mở thẳng màn Tạo mới / Cập nhật thì bị đưa về danh sách.'),
    ('Q2', 'Xem giá vốn hàng hoá',
     'Được chọn hàng ERP làm hàng con của một hàng tạm (popup Thêm hàng hoá).'),
    ('Q3', 'Vai trò Người tạo BOM',
     'Không phải quyền trong danh mục phân quyền: chỉ người tạo BOM mới được Sửa (Đang tạo / Hoàn thành / Không '
     'duyệt) và Xóa (Đang tạo); BOM “Đang tạo” chỉ người tạo nhìn thấy.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách BOM List theo tổng công ty', 'Toàn bộ BOM.'),
    ('V2', 'Xem danh sách BOM List theo công ty',
     'BOM thuộc công ty đang làm việc + BOM do mình tạo.'),
    ('V3', 'Xem danh sách BOM List theo phòng ban',
     'BOM của phòng ban / bộ phận mình quản lý + BOM do mình tạo.'),
    ('V4', 'Xem danh sách BOM List theo bộ phận', 'BOM của bộ phận mình quản lý + BOM do mình tạo.'),
    ('–', 'Không có quyền phạm vi nào', 'Chỉ BOM do mình tạo.'),
], widths=[0.8, 2.6, 2.6])
d.p('Có nhiều quyền phạm vi thì áp dụng quyền rộng nhất (V1 > V2 > V3 > V4). Ở mọi phạm vi, BOM đang ở trạng '
    'thái “Đang tạo” chỉ hiện với chính người tạo.')

d.h2('2 Ma trận phân quyền')
Y, N = '✅', '❌'
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách BOM', Y, Y, Y, '✅ (BOM mình tạo)'),
    ('FR-02 Tìm kiếm và lọc', Y, Y, Y, Y),
    ('FR-03 Cài đặt bộ lọc', Y, Y, Y, Y),
    ('FR-04 Tùy chỉnh cột hiển thị', Y, Y, Y, Y),
    ('FR-05 Xuất Excel danh sách', Y, Y, Y, Y),
    ('FR-06 Tạo mới BOM thành phần', Y, N, '–', N),
    ('FR-07 Tạo mới BOM tổng hợp', Y, N, '–', N),
    ('FR-08 Thêm hàng hoá vào BOM', Y, '✅ (hàng ERP làm hàng con của hàng tạm)', '–', N),
    ('FR-09 Thêm hàng tạm', Y, N, '–', N),
    ('FR-10 Thêm dịch vụ & chi phí khác', Y, N, '–', N),
    ('FR-11 Quản lý nhóm hàng 2 cấp', Y, N, '–', N),
    ('FR-12 Thao tác trên lưới hàng hoá', Y, N, '–', N),
    ('FR-13 Import hàng hoá từ Excel', '✅ (cùng Q3)', N, '✅ (cùng Q1)', N),
    ('FR-14 Xuất Excel BOM', Y, Y, Y, Y),
    ('FR-15 Chỉnh sửa BOM', '✅ (cùng Q3)', N, '✅ (cùng Q1)', N),
    ('FR-16 Xem chi tiết BOM', Y, Y, Y, Y),
    ('FR-17 Sao chép BOM', Y, N, N, N),
    ('FR-18 Xóa BOM', '✅ (cùng Q3)', N, '✅ (cùng Q1)', N),
    ('FR-19 In BOM', Y, Y, Y, Y),
    ('FR-20 Xem lịch sử BOM', Y, Y, Y, Y),
    ('FR-21 Theo dõi trạng thái duyệt BOM', Y, Y, Y, Y),
], widths=[2.4, 0.8, 1.2, 0.8, 0.8])
d.p('Ghi chú: các chức năng xem (FR-01…05, 14, 16, 19–21) áp dụng trên những BOM người dùng nhìn thấy theo phạm '
    'vi V1–V4. Thành viên đã bị khoá khỏi giải pháp không lưu được BOM mới của giải pháp đó (xem BR-03).')

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_LAP, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]), (A_XEM, [0, 1, 6, 9, 11])],
    [('FR-01', 'Xem danh sách BOM', 'view'),            # 0
     ('FR-05', 'Xuất Excel danh sách', 'io'),           # 1
     ('FR-06', 'Tạo mới BOM thành phần', 'crud'),       # 2
     ('FR-07', 'Tạo mới BOM tổng hợp', 'crud'),         # 3
     ('FR-13', 'Import hàng hoá từ Excel', 'io'),       # 4
     ('FR-15', 'Chỉnh sửa BOM', 'crud'),                # 5
     ('FR-14', 'Xuất Excel BOM', 'io'),                 # 6
     ('FR-17', 'Sao chép BOM', 'crud'),                 # 7
     ('FR-18', 'Xóa BOM', 'action'),                    # 8
     ('FR-19', 'In BOM', 'io'),                         # 9
     ('FR-11', 'Quản lý nhóm hàng 2 cấp', 'crud'),      # 10
     ('FR-21', 'Theo dõi trạng thái duyệt', 'action')], # 11
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-16', 'Xem chi tiết BOM', 'view', 'extend', [0], None),
     ('FR-20', 'Xem lịch sử BOM', 'view', 'extend', [0], None),
     ('FR-08', 'Thêm hàng hoá vào BOM', 'crud', 'extend', [2], None),
     ('FR-09', 'Thêm hàng tạm', 'crud', 'extend', [2], None),
     ('FR-10', 'Thêm dịch vụ & chi phí', 'crud', 'extend', [2], None),
     ('FR-12', 'Thao tác trên lưới hàng hoá', 'crud', 'extend', [5], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1 Xem danh sách
d.h3('2.1 Xem danh sách BOM')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của '
           'màn BOM giải pháp tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách BOM',
    mota='Hiển thị danh sách BOM (thành phần và tổng hợp) trong phạm vi được xem, mới tạo ở trên cùng; mỗi dòng '
         'có các nút thao tác theo trạng thái và người tạo.',
    tacnhan=TN_XEM,
    dieukien=DK_LIST,
    chinh='1. Người dùng vào menu BOM Giải pháp.\n'
          '2. Hệ thống hiển thị khối “Bộ lọc danh sách” (thu gọn) và bảng “Danh sách BOM List”, 10 dòng / trang, '
          'sắp xếp theo Ngày tạo giảm dần.\n'
          '3. Người dùng bấm mã BOM để mở màn chi tiết, hoặc dùng các nút ở cột Hành động.',
    phu='• Không có BOM phù hợp → bảng hiển thị “Không có dữ liệu phù hợp.”.\n'
        '• Tải dữ liệu lỗi → thông báo “Lỗi khi tải dữ liệu”.\n'
        '• Bấm tiêu đề cột Mã BOM / Tên BOM / Ngày tạo / Ngày cập nhật → sắp xếp tăng / giảm.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-ds.png'), shot_caption='Màn danh sách BOM giải pháp lúc mới mở')
d.figure(shot('01b-ds-phai.png'), 'Các cột bên phải và cột Hành động (cuộn ngang bảng)', width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách BOM List', 'Tiêu đề trên thanh đầu trang cũng là “Danh sách BOM List”.'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q1', 'Mở màn Tạo BOM List (FR-06 / FR-07).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở popup Chọn trường xuất file (FR-05).'),
    ('Nút cấu hình cột', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Mở popup Tuỳ chỉnh cột (FR-04).'),
    ('Cột STT', 'Text', 'Read-only', '–', 'Theo trang', 'Ghim trái, không ẩn được.'),
    ('Cột Mã BOM', 'Link', 'Read-only', 'BOM-YYYY-NNNNN', 'Theo dữ liệu', 'Ghim trái; bấm mở màn chi tiết (FR-16), chuột phải mở tab mới được; sắp xếp được.'),
    ('Cột Tên BOM', 'Text', 'Read-only', '≤ 255 ký tự', 'Theo dữ liệu', 'Tối đa 2 dòng; sắp xếp được.'),
    ('Cột Loại BOM', 'Badge', 'Read-only', '2 giá trị', 'Theo dữ liệu', '“Thành phần” (xám) / “Tổng hợp” (tím).'),
    ('Cột Dự án TKT', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Dạng “Mã dự án - Tên dự án”.'),
    ('Cột Giải pháp', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Dạng “Mã giải pháp - Tên giải pháp”.'),
    ('Cột Hạng mục', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Trống với BOM cấp giải pháp.'),
    ('Cột Version GP / Version HM', 'Badge', 'Read-only', '–', 'Theo dữ liệu', 'Phiên bản giải pháp / hạng mục lúc lưu BOM (vd V1).'),
    ('Cột Khách hàng', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Dạng “Mã KH - Tên KH”.'),
    ('Cột Người tạo / Phòng của người tạo / Ngày tạo', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', '6 giá trị', 'Theo dữ liệu',
     'Đang tạo (xám) · Hoàn thành (xanh lá) · Chờ duyệt (cam) · Đã duyệt (xanh lá) · Đã được tổng hợp (xám đậm) · '
     'Không duyệt (đỏ).'),
    ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
     'Cột cuối, không ẩn được. 2 nút đầu hiện thẳng, phần còn lại vào nút “⋮ Hành động khác”: Sửa (bút) · Xóa '
     '(thùng rác) · Sao chép · In BOM List · Lịch sử. Điều kiện hiện xem BR-05.'),
    ('Phân trang', 'Pagination', 'Enable', '–', '10 dòng / trang', 'Có ô chọn số dòng / trang và dòng “Hiển thị a–b / tổng”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp.”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Áp phạm vi dữ liệu V1–V4 (không có → chỉ BOM mình tạo); ẩn BOM “Đang tạo” của người khác.\n'
     'After:\n– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có), nạp trang 1 và cấu hình cột đã lưu.\n'
     '– Lỗi → “Lỗi khi tải dữ liệu”.'),
    ('Bấm mã BOM', 'Click', 'After:\n– Mở màn Chi tiết BOM List (FR-16).'),
    ('Bấm tiêu đề cột sắp xếp', 'Click', 'After:\n– Đảo chiều sắp xếp, quay về trang 1 và nạp lại.'),
    ('Đổi trang / số dòng mỗi trang', 'Click / Change', 'After:\n– Nạp lại danh sách theo trang / số dòng mới.'),
    ('Bấm nút ⋮ Hành động khác', 'Click', 'After:\n– Mở danh sách các thao tác còn lại của dòng (Sao chép, In BOM List, Lịch sử).'),
])

# ------------------------------------------------------------------ 2.2 Tìm kiếm và lọc
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.',
           anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc',
    mota='Lọc danh sách BOM theo từ khoá (mã, tên BOM) và bộ lọc nâng cao: tổ chức, dự án TKT, giải pháp, hạng mục, '
         'khách hàng, người tạo, trạng thái, loại BOM, ngày tạo.',
    tacnhan=TN_XEM,
    dieukien=DK_LIST,
    chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi bấm “Tìm kiếm” hoặc Enter.\n'
          '2. Người dùng bấm “Tìm kiếm nâng cao” để mở bộ lọc, chọn điều kiện.\n'
          '3. Với ô chọn, hệ thống tự lọc ngay khi đổi giá trị; danh sách quay về trang 1.\n'
          '4. Bấm “Làm mới” để xoá mọi điều kiện và nạp lại.',
    phu='• Chọn Dự án TKT → ô Giải pháp tự điền giải pháp của dự án (không chọn tay), ô Khách hàng tự điền khách '
        'hàng của dự án, danh sách Hạng mục chỉ còn hạng mục của giải pháp đó.\n'
        '• Bỏ chọn Dự án TKT → xoá Giải pháp, Khách hàng, Hạng mục.\n'
        '• Ô Khách hàng: gõ để tìm (tối đa 30 kết quả), không nạp toàn bộ danh mục.\n'
        '• Danh mục dự án / giải pháp chỉ nạp khi mở bộ lọc nâng cao lần đầu.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc.png'),
         shot_caption='Bộ lọc nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', 'Chuỗi', 'Không', 'Trống', 'Gợi ý “Tìm theo mã BOM, tên BOM”; tìm gần đúng.'),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tìm kiếm: lọc theo từ khoá. Làm mới: xoá hết điều kiện.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn', 'Mở / đóng khối bộ lọc.'),
    ('Công ty – Phòng ban – Bộ phận', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Không', 'Trống',
     '3 ô theo tổ chức của người tạo BOM; ô nào không có quyền cấp tương ứng thì khoá (biểu tượng ổ khoá).'),
    ('Dự án TKT', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Hiển thị “Mã - Tên dự án”.'),
    ('Giải pháp', 'Textbox', 'Disable', '–', '–', 'Trống', 'Tự điền theo dự án; gợi ý “Chọn dự án TKT để hiện giải pháp”.'),
    ('Hạng mục', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Chỉ có dữ liệu khi đã có giải pháp.'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Tìm từ xa', 'Không', 'Trống', 'Gõ để tìm; tự điền theo dự án.'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '–'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Không', 'Trống',
     'Đang tạo · Hoàn thành · Chờ duyệt · Đã duyệt · Đã được tổng hợp · Không duyệt.'),
    ('Loại BOM', 'Dropdown', 'Enable', '2 giá trị', 'Không', 'Trống', 'Thành phần · Tổng hợp.'),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống', 'Khoảng ngày gộp trong 1 ô.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter ở ô tìm nhanh', 'Click / Keypress', 'After:\n– Về trang 1, lọc theo mã hoặc tên BOM chứa từ khoá.'),
    ('Đổi giá trị ô chọn bất kỳ', 'Change', 'After:\n– Tự lọc ngay, về trang 1; lưu bộ lọc để khôi phục khi quay lại màn (10 phút).'),
    ('Chọn Dự án TKT', 'Change',
     'After:\n– Tự điền Giải pháp và Khách hàng của dự án, xoá Hạng mục, nạp danh sách Hạng mục theo giải pháp, lọc lại.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá toàn bộ điều kiện, nạp lại đúng 1 lần.'),
])

# ------------------------------------------------------------------ 2.3 Cài đặt bộ lọc
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.',
           anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Cho người dùng tự chọn ô lọc nào hiện trong bộ lọc nâng cao và thứ tự của chúng.',
    tacnhan=TN_XEM,
    dieukien=DK_LIST,
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở popup liệt kê 9 ô lọc kèm ô tích.\n'
          '3. Người dùng bỏ tích / tích và kéo thả để đổi thứ tự.\n'
          '4. Bấm “Lưu” → bộ lọc nâng cao hiển thị theo cấu hình mới.',
    phu='• Bấm “Khôi phục mặc định” → trở về đủ 9 ô theo thứ tự gốc.\n'
        '• Bấm “Đóng” / dấu × → không lưu thay đổi.')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('03-cai-dat-loc.png'), shot_caption='Popup Cài đặt bộ lọc')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', 'Kèm dòng hướng dẫn tích chọn và kéo thả.'),
    ('Danh sách ô lọc', 'Checkbox', 'Enable', '9 ô', 'Không', 'Tích đủ',
     'Công ty – Phòng ban – Bộ phận · Dự án TKT · Giải pháp · Hạng mục · Khách hàng · Người tạo · Trạng thái · Loại BOM · Ngày tạo.'),
    ('Tay kéo', 'Icon', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự ô lọc.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình theo người dùng cho màn này.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup không lưu.'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở popup với cấu hình đang dùng.'),
    ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình ô lọc của người dùng; đóng popup; bộ lọc nâng cao vẽ lại theo cấu hình.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về 9 ô, thứ tự gốc.'),
])

# ------------------------------------------------------------------ 2.4 Tùy chỉnh cột
d.h3('2.4 Tùy chỉnh cột hiển thị')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='excel')
d.intro_table(
    ten='Tùy chỉnh cột hiển thị',
    mota='Cho người dùng ẩn / hiện và sắp xếp lại thứ tự các cột của bảng danh sách BOM.',
    tacnhan=TN_XEM,
    dieukien=DK_LIST,
    chinh='1. Người dùng bấm nút cấu hình cột (biểu tượng cột) ở góc phải bảng.\n'
          '2. Hệ thống mở popup “Tuỳ chỉnh cột” liệt kê đủ 17 cột.\n'
          '3. Người dùng bỏ tích / tích, kéo thả để đổi thứ tự.\n'
          '4. Bấm “Lưu” → bảng hiển thị theo cấu hình mới.',
    phu='• Mặc định hiện đủ tất cả cột.\n'
        '• Bấm “Đóng” → không lưu thay đổi.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột hiển thị', shot=shot('04-cot.png'), shot_caption='Popup Tuỳ chỉnh cột')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
    ('Cột bị khoá: STT, Mã BOM, Hành động', 'Checkbox', 'Disable', '3 cột', '–', 'Tích, xám',
     'Luôn hiện, không bỏ tích và không kéo thả được (biểu tượng ổ khoá).'),
    ('Các cột còn lại', 'Checkbox', 'Enable', '14 cột', 'Không', 'Tích đủ',
     'Tên BOM · Loại BOM · Dự án TKT · Giải pháp · Hạng mục · Version GP · Version HM · Khách hàng · Người tạo · '
     'Phòng của người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật · Trạng thái.'),
    ('Tay kéo', 'Icon', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự cột.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình cột theo người dùng cho màn BOM.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút cấu hình cột', 'Click', 'After:\n– Mở popup với cấu hình đang dùng.'),
    ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình; bảng vẽ lại theo cột và thứ tự đã chọn; popup Chọn trường xuất file tick sẵn đúng các cột đang hiện.'),
])

# ------------------------------------------------------------------ 2.5 Xuất Excel danh sách
d.h3('2.5 Xuất Excel danh sách')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Xuất Excel danh sách BOM', 'io', actor=A_XEM)
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách',
    mota='Xuất toàn bộ BOM đang khớp bộ lọc (không phân trang) ra file Excel, người dùng chọn cột cần xuất.',
    tacnhan=TN_XEM,
    dieukien=DK_LIST,
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Hệ thống mở popup “Chọn trường xuất file”, tick sẵn các cột đang hiện trên bảng.\n'
          '3. Người dùng tích / bỏ tích, kéo thả đổi thứ tự cột.\n'
          '4. Bấm “Xuất file” → tải file danh_sach_bom_list.xlsx.',
    phu='• Đang xuất → nút Xuất Excel khoá, không bấm lặp được.\n'
        '• Lỗi → “Lỗi khi xuất Excel”.',
    dacbiet='Phạm vi dữ liệu file = phạm vi đang xem trên danh sách (do máy chủ áp quyền V1–V4).')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel => Xuất file', shot=shot('05-xuat.png'), shot_caption='Popup Chọn trường xuất file')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất file', 'Kèm dòng hướng dẫn.'),
    ('Danh sách trường', 'Checkbox', 'Enable', '23 trường', 'Có ≥ 1', 'Tick theo cột đang hiện',
     'Mã BOM · Tên BOM · Loại BOM · Mã / Tên dự án TKT · Mã / Tên giải pháp · Hạng mục · Version giải pháp · Version '
     'hạng mục · Mã / Tên khách hàng · Phòng làm GP · PM giải pháp · Phòng kinh doanh · NV kinh doanh · Trạng thái · '
     'Ghi chú · Người tạo · Phòng của người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn n/23 trường', '–'),
    ('Nút Xuất file', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thứ tự cột trong file theo thứ tự trong popup.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất file', 'Click',
     'Before:\n– Đang xuất dở → bỏ qua.\nDuring:\n– Lấy toàn bộ BOM khớp bộ lọc hiện tại trong phạm vi quyền.\n'
     'After:\n– Tải file danh_sach_bom_list.xlsx, hiển thị “Xuất Excel thành công”.\n– Lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.6 Tạo mới BOM thành phần
FORM_UI = [
    ('Mã BOM', 'Textbox', 'Read-only', 'BOM-YYYY-NNNNN', '–', 'Ẩn khi tạo mới', 'Chỉ hiện khi BOM đã có mã (Sửa / Xem).'),
    ('Tên BOM LIST', 'Textbox', 'Enable', '≤ 255 ký tự', 'Có', 'Trống', 'Gợi ý “VD: BOM điều khiển dây chuyền line 01”.'),
    ('Dự án', 'Dropdown', 'Enable', 'Dự án của tôi', 'Có (trừ Lưu nháp)', 'Trống',
     'Tìm theo mã / tên dự án; chỉ liệt kê dự án TKT của người dùng.'),
    ('Giải pháp', 'Textbox', 'Disable', '–', 'Có (trừ Lưu nháp)', 'Tự điền', 'Tự điền giải pháp duy nhất của dự án.'),
    ('Hạng mục', 'Dropdown', 'Enable / Disable', 'Hạng mục của giải pháp', 'Không', 'Trống',
     'Khoá khi chưa có giải pháp. Bỏ trống = BOM cấp giải pháp.'),
    ('Khách hàng', 'Textbox', 'Disable', '–', 'Có (trừ Lưu nháp)', 'Tự điền', 'Khách hàng của dự án; gợi ý “Chọn dự án để tự động hiện khách hàng”.'),
    ('Ghi chú', 'Textbox', 'Enable', 'Chuỗi', 'Không', 'Trống', '–'),
    ('Loại BOM LIST', 'Dropdown', 'Enable / Disable', '2 giá trị', 'Có', 'BOM LIST thành phần',
     'BOM LIST thành phần / BOM LIST tổng hợp. Khoá ở “tổng hợp” khi giải pháp có hạng mục mà chưa chọn hạng mục.'),
    ('Nút Chọn BL con', 'Button', 'Enable / Disable', '–', '–', 'Khoá với BOM thành phần', 'Chỉ bấm được với BOM tổng hợp (FR-07).'),
    ('Khối Chi tiết BOM LIST', 'Table/Grid', 'Enable', '–', '–', 'Chưa có dòng BOM nào.',
     'Khối A — Hàng hoá (nhóm, hàng cha, hàng con) và khối B — Dịch vụ & Chi phí khác; cột Thao tác · STT · Mã hàng · '
     'Tên hàng · Model · Thương hiệu · Xuất xứ · ĐVT · Thông số kỹ thuật · Ghi chú · Số lượng. Không có cột giá.'),
    ('Dòng đếm', 'Label', 'Hiển thị', '–', '–', '0', '“Tổng nhóm cha: n · Tổng hàng con: m · Kéo icon để đổi thứ tự”.'),
    ('Nút Import Excel / Xuất Excel', 'Button', 'Enable / Disable', '–', '–', 'Khoá khi chưa lưu',
     'Tooltip “Vui lòng lưu nháp BOM trước khi import” / “…trước khi xuất Excel” (FR-13, FR-14).'),
    ('Nút Ẩn cấp con / Hiện cấp con', 'Button', 'Enable', '–', '–', 'Ẩn cấp con', 'Ẩn / hiện toàn bộ hàng con.'),
    ('Nút Thêm nhóm · Thu gọn tất cả / Mở rộng tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xem FR-11.'),
    ('Nút Thêm mới (khối A / khối B)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở popup Thêm hàng hoá (FR-08) / Thêm dịch vụ (FR-10).'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ dưới ô Tên / Dự án / Giải pháp / Khách hàng khi máy chủ trả lỗi.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Quay lại màn trước (mở ở tab mới thì về danh sách).'),
    ('Nút Lưu nháp', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị khi tạo mới',
     'Lưu với trạng thái Đang tạo; chỉ bắt buộc Tên. Ở màn Sửa chỉ hiện khi BOM đang “Đang tạo”.'),
    ('Nút Lưu BOM', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu với trạng thái Hoàn thành; bắt buộc đủ trường.'),
]


def save_events(after_extra=''):
    return [
        ('Chọn Dự án', 'Change',
         'After:\n– Tự điền Khách hàng và Giải pháp của dự án; nạp danh sách Hạng mục; bỏ chọn BOM con đã chọn (nếu có).'),
        ('Chọn Hạng mục', 'Change', 'After:\n– Ghi nhận version hiện hành của hạng mục; bỏ chọn BOM con đã chọn.'),
        ('Đổi Loại BOM LIST khi lưới đã có dữ liệu', 'Change',
         'After:\n– Hỏi “Hệ thống sẽ xoá bỏ toàn bộ danh sách hàng hoá đang có. Bạn xác nhận sẽ thay đổi?” (Xoá / Huỷ).\n'
         '– Xoá → xoá hết hàng hoá, nhóm, dịch vụ, BOM con đã chọn. Huỷ → giữ nguyên.'),
        ('Bấm Lưu nháp', 'Click',
         'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
         'During:\n– Tên trống → “Vui lòng nhập tên BOM.”; Tên > 255 ký tự → “Tên BOM không được vượt quá 255 ký tự.”\n'
         '– Hàng ERP thiếu mã → “Mã hàng hoá không được để trống: <danh sách tối đa 5 hàng>[ và n hàng khác]”.\n'
         '– Có lỗi → không thực hiện bước After.\n'
         'After:\n– Lưu BOM trạng thái Đang tạo' + after_extra + '; hiển thị “Đã lưu BOM LIST thành công.” và về danh sách.'),
        ('Bấm Lưu BOM', 'Click',
         'Before:\n– Kiểm tra quyền Q1; thành viên đã bị khoá khỏi giải pháp → “Bạn đã bị khóa khỏi giải pháp này nên '
         'không thao tác được. Vui lòng liên hệ PM hoặc Trưởng phòng giải pháp.”\n'
         'During:\n– Tên trống → “Vui lòng nhập tên BOM.”; Dự án trống → “Vui lòng chọn Dự án.”; Giải pháp trống → '
         '“Vui lòng chọn Giải pháp.”; Khách hàng trống → “Vui lòng chọn Khách hàng.”\n'
         '– Giải pháp có hạng mục mà BOM cấp giải pháp không phải tổng hợp → “Giải pháp có hạng mục con — BOM cấp giải '
         'pháp chỉ được tạo loại Tổng hợp.”\n'
         '– Hàng ERP thiếu mã → “Mã hàng hoá không được để trống: …”.\n'
         '– Có lỗi → báo lỗi (dưới ô và thông báo), không thực hiện bước After.\n'
         'After:\n– Sinh mã BOM-YYYY-NNNNN, lưu BOM trạng thái Hoàn thành kèm version hiện hành của giải pháp / hạng mục' +
         after_extra + '.\n'
         '– Hàng tạm chưa có mã được cấp mã HHB… tự động.\n'
         '– Ghi lịch sử “Tạo mới — Tạo mới BOM List”.\n'
         '– Hiển thị “Đã lưu BOM LIST thành công.” và quay về danh sách.'),
        ('Bấm Quay lại', 'Click', 'After:\n– Rời màn, dữ liệu chưa lưu bị bỏ.'),
    ]


d.h3('2.6 Tạo mới BOM thành phần')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Tạo mới BOM thành phần', 'crud', actor=A_LAP)
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.',
           anchor='create')
d.intro_table(
    ten='Tạo mới BOM thành phần',
    mota='Lập BOM thành phần cho một hạng mục (hoặc giải pháp không chia hạng mục): nhập thông tin chung rồi dựng '
         'lưới hàng hoá, hàng tạm, dịch vụ – chi phí theo nhóm.',
    tacnhan=TN_LAP,
    dieukien='Người dùng có quyền Q1; dự án TKT đã có giải pháp.',
    chinh='1. Người dùng bấm “Tạo mới” ở màn danh sách.\n'
          '2. Hệ thống mở màn “Tạo BOM List”, Loại BOM LIST mặc định “BOM LIST thành phần”, tiền tệ mặc định VNĐ.\n'
          '3. Người dùng nhập Tên BOM LIST, chọn Dự án (Giải pháp, Khách hàng tự điền), chọn Hạng mục, nhập Ghi chú.\n'
          '4. Người dùng thêm nhóm hàng (FR-11), hàng hoá (FR-08), hàng tạm (FR-09), dịch vụ – chi phí (FR-10).\n'
          '5. Người dùng bấm “Lưu BOM”.\n'
          '6. Hệ thống kiểm tra, sinh mã, lưu BOM trạng thái Hoàn thành và quay về danh sách.',
    phu='• Bấm “Lưu nháp” → lưu trạng thái Đang tạo, chỉ bắt buộc Tên.\n'
        '• Giải pháp có hạng mục mà không chọn Hạng mục → hệ thống tự chuyển Loại thành “BOM LIST tổng hợp” và khoá ô '
        'Loại (BOM cấp giải pháp chỉ được là tổng hợp).\n'
        '• Lỗi máy chủ khác → “Lưu BOM LIST thất bại. Vui lòng thử lại.”.\n'
        '• Không có quyền Q1 mà mở thẳng màn → “Bạn không có quyền tạo BOM List” và về danh sách.',
    dacbiet='BOM không quản lý giá: lưới không có cột giá nhập / giá bán; giá được xử lý ở Báo giá.')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Loại BOM LIST', shot=shot('06-tao-tp.png'),
         shot_caption='Form Tạo BOM List – BOM LIST thành phần')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table(FORM_UI)
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([('Mở màn Tạo mới', 'System',
                'Before:\n– Kiểm tra quyền Q1; không có → “Bạn không có quyền tạo BOM List”, về danh sách.\n'
                'After:\n– Nạp danh sách dự án của tôi, giải pháp, hạng mục, BOM con, danh mục ĐVT / thương hiệu / '
                'xuất xứ / model; ô Mã BOM ẩn.')] + save_events())

# ------------------------------------------------------------------ 2.7 Tạo mới BOM tổng hợp
d.h3('2.7 Tạo mới BOM tổng hợp')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Tạo mới BOM tổng hợp', 'crud', actor=A_LAP)
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.',
           anchor='create')
d.intro_table(
    ten='Tạo mới BOM tổng hợp (gộp BOM con)',
    mota='Lập BOM tổng hợp bằng cách chọn các BOM con rồi gộp toàn bộ hàng hoá, nhóm, dịch vụ của chúng vào lưới. '
         'BOM tổng hợp cấp hạng mục gộp BOM thành phần; BOM tổng hợp cấp giải pháp gộp BOM tổng hợp hạng mục đã duyệt.',
    tacnhan=TN_LAP,
    dieukien='Người dùng có quyền Q1; đã có BOM con phù hợp (BR-07).',
    chinh='1. Người dùng bấm “Tạo mới”, nhập Tên, chọn Dự án, chọn Hạng mục (bỏ trống nếu lập cấp giải pháp).\n'
          '2. Người dùng chọn Loại BOM LIST = “BOM LIST tổng hợp”.\n'
          '3. Người dùng bấm “Chọn BL con”; hệ thống mở popup “Chọn BOM con để gộp” chỉ liệt kê BOM con hợp lệ.\n'
          '4. Người dùng tích các BOM con, bấm “Gộp BOM con”.\n'
          '5. Hệ thống gộp hàng hoá, nhóm hàng, dịch vụ của các BOM con vào lưới; dòng “Đã chọn: n BL con” và chip '
          'mã – tên từng BOM con hiện dưới nút.\n'
          '6. Người dùng chỉnh lưới nếu cần, bấm “Lưu BOM”.\n'
          '7. Hệ thống lưu BOM tổng hợp trạng thái Hoàn thành; các BOM thành phần được chọn chuyển “Đã được tổng hợp”.',
    phu='• Chưa có Dự án / Giải pháp mà bấm Chọn BL con → “Vui lòng chọn Dự án và Giải pháp trước khi chọn BL con.”.\n'
        '• Bấm Gộp khi chưa tích BOM nào → “Chưa chọn BL con nào.”.\n'
        '• BOM con khác loại tiền tệ → “Loại tiền tệ không khớp: <mã>. BOM tổng hợp và BOM thành phần phải cùng loại '
        'tiền tệ.”.\n'
        '• BOM con lệch cấu trúc nhóm → “Các BOM con phải có cùng cấu trúc. BOM có nhóm: <mã>. BOM không có nhóm: <mã>.”.\n'
        '• Không tải được BOM con → “Không thể tải dữ liệu BL con. Vui lòng thử lại.”.\n'
        '• Không có BOM con hợp lệ → popup hiện “Không có BL con phù hợp.”.\n'
        '• Đã có BOM tổng hợp cùng giải pháp / hạng mục / version → “Giải pháp[ / Hạng mục] đã có BOM tổng hợp trên '
        'version này: <tên> (<mã>)[ (version …)]”, không lưu.',
    dacbiet='Gộp lại nhiều lần sẽ thay toàn bộ lưới bằng kết quả gộp mới. Nhóm trùng tên được gộp làm một; mã hàng tạm '
            'trùng giữa các BOM con được đánh lại cho khỏi trùng; thứ tự hàng theo ngày tạo BOM con (cũ trước).')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Loại BOM LIST => Chọn BL con => Gộp BOM con', shot=shot('08-chon-bl-con.png'),
         shot_caption='Popup Chọn BOM con để gộp – BOM tổng hợp cấp hạng mục')
d.figure(shot('08b-sau-gop.png'), 'Lưới BOM tổng hợp sau khi gộp 1 BL con', width_in=6.2)
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Loại BOM LIST', 'Dropdown', 'Enable / Disable', '2 giá trị', 'Có', 'BOM LIST thành phần', 'Chọn “BOM LIST tổng hợp”.'),
    ('Nút Chọn BL con', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở popup chọn BOM con.'),
    ('Dòng Đã chọn', 'Label', 'Hiển thị', '–', '–', 'Đã chọn: 0 BL con', 'Kèm chip “Mã - Tên” từng BOM con đã chọn.'),
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn BOM con để gộp', '–'),
    ('Bảng BOM con', 'Table/Grid', 'Enable', 'Theo BR-07', 'Có ≥ 1', 'Chưa tích',
     'Cột Chọn (ô tích) · Mã BL · Tên BL · Dự án · Giải pháp · Hạng mục.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có BL con phù hợp.”'),
    ('Nút Gộp BOM con', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Gộp các BOM đã tích vào lưới.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, giữ lựa chọn.'),
    ('Các trường còn lại của form', 'Form', 'Enable', '–', '–', '–', 'Như FR-06.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Chọn BL con', 'Click',
     'Before:\n– Chưa có Dự án / Giải pháp → “Vui lòng chọn Dự án và Giải pháp trước khi chọn BL con.”, dừng.\n'
     'After:\n– Nạp lại danh sách BOM, lọc theo BR-07, mở popup.'),
    ('Bấm Gộp BOM con', 'Click',
     'Before:\n– Chưa tích → “Chưa chọn BL con nào.”, dừng.\n'
     'During:\n– Tải chi tiết từng BOM con; kiểm tra cùng tiền tệ, cùng cấu trúc nhóm (thông báo như Dòng sự kiện phụ).\n'
     'After:\n– Thay lưới bằng hàng hoá, nhóm, dịch vụ đã gộp; đóng popup.'),
] + save_events(after_extra=' và ghi liên kết BOM con; BOM thành phần được chọn chuyển “Đã được tổng hợp”')[3:])

# ------------------------------------------------------------------ 2.8 Thêm hàng hoá
d.h3('2.8 Thêm hàng hoá vào BOM')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Thêm hàng hoá vào BOM', 'crud', actor=A_LAP)
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown; Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của màn BOM '
           'giải pháp.', anchor='search')
d.intro_table(
    ten='Thêm hàng hoá vào BOM',
    mota='Popup “Thêm hàng hoá” tra cứu danh mục hàng hoá ERP (kèm hàng đang có trong BOM hiện ở đầu danh sách), cho '
         'tích nhiều hàng để thêm vào nhóm hàng chọn sẵn, làm hàng cha hoặc hàng con của một dòng.',
    tacnhan=TN_LAP,
    dieukien='Đang ở màn Tạo mới / Cập nhật BOM.',
    chinh='1. Người dùng bấm “Thêm mới” ở khối A — Hàng hoá, ở dòng nhóm, hoặc “Thêm con” ở một hàng cha (hàng tạm).\n'
          '2. Hệ thống mở popup “Thêm hàng hoá”, ô Nhóm hàng chọn sẵn nhóm đang đứng (hoặc nhóm cuối).\n'
          '3. Người dùng tìm theo tên, mã, model hoặc mở “Tìm kiếm nâng cao”, tích các hàng cần thêm.\n'
          '4. Người dùng bấm “Thêm n hàng hoá”.\n'
          '5. Hệ thống thêm hàng vào lưới, báo “Đã thêm n hàng hoá vào phiếu.”; popup vẫn mở để thêm tiếp.',
    phu='• Hàng đã có trong BOM → hỏi “Hàng hóa \"<tên>\" đã tồn tại trong danh sách. Bạn muốn cộng dồn số lượng hay '
        'tạo dòng mới?” (Cộng dồn số lượng / Tạo dòng mới / Huỷ).\n'
        '• Hàng con trùng mã hàng cha → “Hàng con không được trùng mã với hàng cha (<mã>): <danh sách>”, bỏ các dòng trùng.\n'
        '• Chọn hàng ERP làm con của hàng tạm khi thiếu Q2 → “Bạn không có quyền \"Xem giá vốn hàng hoá\" nên không thể '
        'chọn hàng ERP làm hàng con.”.\n'
        '• Lỗi tải hàng ERP → “Không thể tải danh sách hàng hoá từ ERP.”.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”.',
    dacbiet='Hàng ERP có công thức (hàng con theo ERP) được thêm kèm hàng con và khoá số lượng hàng con. Popup này '
            'dùng chung với màn Báo giá.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Thêm mới', shot=shot('09-them-hang.png'),
         shot_caption='Popup Thêm hàng hoá (mở từ BOM đang sửa)')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Thêm hàng hoá', '–'),
    ('Nhóm hàng', 'Dropdown', 'Enable', 'Nhóm của BOM', 'Có khi BOM có nhóm', 'Nhóm đang đứng', 'Ghi chú “Hàng hoá sẽ được thêm vào nhóm này”.'),
    ('Ô tìm nhanh', 'Textbox', 'Enable', 'Chuỗi', 'Không', 'Trống', '“Tìm theo tên, mã, model hàng hoá”.'),
    ('Nút Thêm hàng tạm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở FR-09.'),
    ('Nút Cài đặt bộ lọc / Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Bộ lọc nâng cao: Tính chất hàng hóa, Loại hàng hóa, Công ty (nguồn hàng), Thương hiệu, Hãng sản xuất, Xuất xứ, '
     'Lĩnh vực, Chương, Nhóm / Cụm công việc, Nhóm hàng hóa, Dùng cho nhóm máy / máy, Hãng / Loại / Model / Đời xe, '
     'Model, Tồn kho.'),
    ('Bảng hàng hoá', 'Table/Grid', 'Enable', 'Phân trang 20 dòng', '–', 'Trang 1',
     'Ô tích · Ảnh · Loại hàng hóa · Tên hàng hoá · Lĩnh vực · Chương · Model · Mã hàng · Nguồn hàng · Giá niêm yết · '
     'Bảo hành · VAT(%) · Định mức đàm phán giá (%) · SL tồn có thể bán · SL KM có thể xuất · SL có thể LR · Ghi chú · '
     'Tính chất hàng hóa · Nguồn (ERP / hàng trong BOM). Thanh cuộn ngang ở cả trên và dưới.'),
    ('Dòng tổng', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu', '“Tổng: n hàng ERP (+m hàng trong BOM hiển thị trên cùng)”.'),
    ('Nút Thêm n hàng hoá', 'Button', 'Enable / Disable', '–', '–', 'Khoá khi chưa tích', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Hộp “Hàng hoá đã tồn tại”', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', 'Nút Cộng dồn số lượng · Tạo dòng mới · Huỷ.'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở popup', 'Click', 'After:\n– Nạp trang 1 danh mục hàng ERP; hàng đang có trong BOM hiển thị trên cùng.'),
    ('Gõ tìm / đổi bộ lọc', 'Keypress / Change', 'After:\n– Tìm lại từ máy chủ, về trang 1.'),
    ('Bấm Thêm n hàng hoá', 'Click',
     'Before:\n– Thêm hàng ERP làm con của hàng tạm mà thiếu Q2 → thông báo như Dòng sự kiện phụ, dừng.\n'
     'During:\n– Hàng trùng → hỏi cộng dồn / tạo dòng mới / huỷ.\n– Hàng con trùng mã hàng cha → bỏ dòng trùng, báo lỗi.\n'
     'After:\n– Thêm vào lưới đúng nhóm / dòng cha; đánh lại STT; báo “Đã thêm n hàng hoá vào phiếu.”.'),
])

# ------------------------------------------------------------------ 2.9 Thêm hàng tạm
d.h3('2.9 Thêm hàng tạm')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Thêm hàng tạm', 'crud', actor=A_LAP)
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.',
           anchor='create')
d.intro_table(
    ten='Thêm hàng tạm',
    mota='Thêm hàng chưa có trong danh mục ERP: dùng lại hàng tạm đang có trên lưới BOM, hoặc nhập tay hàng tạm mới.',
    tacnhan=TN_LAP,
    dieukien='Đang mở popup Thêm hàng hoá (FR-08).',
    chinh='1. Người dùng bấm “Thêm hàng tạm” trong popup Thêm hàng hoá.\n'
          '2. Hệ thống mở hộp “Thêm hàng tạm” gồm 2 tab.\n'
          '3a. Tab “Chọn từ kho hàng tạm (Tái sử dụng)”: tìm theo mã / tên, tích hàng, bấm “Thêm n hàng hóa”.\n'
          '3b. Tab “Thêm mới thủ công”: nhập Tên hàng hoá, Đơn vị tính, Thương hiệu, Xuất xứ (bắt buộc), Model, Số '
          'lượng cần dùng, Ghi chú, Đặc điểm / Thông số kỹ thuật; bấm “Lưu” hoặc “Lưu và tiếp tục”.\n'
          '4. Hệ thống thêm hàng tạm vào lưới (mã HHB… cấp khi lưu BOM).',
    phu='• Thiếu Tên → “Tên là bắt buộc”; thiếu ĐVT → “Đơn vị tính là bắt buộc”; thiếu Thương hiệu → “Thương hiệu là '
        'bắt buộc”; thiếu Xuất xứ → “Xuất xứ là bắt buộc”; BOM có nhóm mà chưa chọn nhóm → “Vui lòng chọn nhóm hàng”.\n'
        '• “Lưu và tiếp tục” → thêm xong xoá trắng form để nhập hàng kế tiếp.\n'
        '• Bấm biểu tượng ⊕ cạnh Model / Thương hiệu / Xuất xứ → thêm nhanh danh mục (nhập Tên; Thương hiệu thêm Mã); '
        'thiếu → “Vui lòng nhập tên.” / “Vui lòng nhập mã.”; thành công → “Đã thêm nhanh thành công.”.\n'
        '• Tab Tái sử dụng chưa có hàng tạm → “Không có hàng tạm phù hợp.”.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Thêm mới => Thêm hàng tạm', shot=shot('10b-hang-tam-thu-cong.png'),
         shot_caption='Hộp Thêm hàng tạm – tab Thêm mới thủ công')
d.figure(shot('10-hang-tam-dung-lai.png'), 'Hộp Thêm hàng tạm – tab Chọn từ kho hàng tạm (Tái sử dụng)', width_in=6.2)
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nhóm hàng', 'Dropdown', 'Enable', 'Nhóm của BOM', 'Có khi BOM có nhóm', 'Nhóm đang đứng', 'Dùng chung cho 2 tab.'),
    ('Tab Chọn từ kho hàng tạm', 'Tab', 'Enable', '–', '–', 'Mở mặc định', 'Liệt kê hàng tạm đang có trên lưới BOM.'),
    ('Ô tìm nhanh (tab 1)', 'Textbox', 'Enable', 'Chuỗi', 'Không', 'Trống', '“Tìm nhanh theo mã / tên hàng tạm...”.'),
    ('Bảng hàng tạm (tab 1)', 'Table/Grid', 'Enable', '–', '–', 'Chưa tích', 'Ô tích · Mã hàng · Tên hàng · Model · Thương hiệu · Xuất xứ · ĐVT · Nguồn.'),
    ('Nút Thêm n hàng hóa (tab 1)', 'Button', 'Enable / Disable', '–', '–', 'Khoá khi chưa tích', '–'),
    ('Tên hàng hoá', 'Textbox', 'Enable', 'Chuỗi', 'Có', 'Trống', 'Gợi ý “Nhập tên hàng hoá”.'),
    ('Đơn vị tính', 'Dropdown', 'Enable', 'Danh mục ĐVT', 'Có', 'Trống', '–'),
    ('Model', 'Dropdown', 'Enable', 'Tìm từ xa', 'Không', 'Trống', 'Có nút ⊕ thêm nhanh.'),
    ('Thương hiệu', 'Dropdown', 'Enable', 'Tìm từ xa', 'Có', 'Trống', 'Có nút ⊕ thêm nhanh (Tên + Mã thương hiệu).'),
    ('Xuất xứ', 'Dropdown', 'Enable', 'Tìm từ xa', 'Có', 'Trống', 'Có nút ⊕ thêm nhanh.'),
    ('Số lượng cần dùng', 'Number', 'Enable', '≥ 0', 'Không', '1', '–'),
    ('Ghi chú', 'Textbox', 'Enable', 'Chuỗi', 'Không', 'Trống', '–'),
    ('Đặc điểm / Thông số kỹ thuật', 'Textarea', 'Enable', 'Văn bản định dạng', 'Không', 'Trống', 'Trình soạn thảo có định dạng.'),
    ('Nút Lưu / Lưu và tiếp tục / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bấm ra ngoài hộp không đóng hộp.'),
])
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Thêm n hàng hóa (tab Tái sử dụng)', 'Click',
     'After:\n– Thêm các hàng tạm đã tích (kèm hàng con) vào lưới, dùng chung mã với dòng gốc; báo “Đã thêm n hàng hóa”.'),
    ('Bấm Lưu / Lưu và tiếp tục (tab thủ công)', 'Click',
     'During:\n– Kiểm tra các trường bắt buộc, thông báo lỗi dưới từng ô như Dòng sự kiện phụ; có lỗi → dừng.\n'
     'After:\n– Thêm hàng tạm vào lưới (đúng nhóm / dòng cha).\n– Lưu: đóng hộp. Lưu và tiếp tục: xoá trắng form, giữ hộp.'),
    ('Bấm ⊕ và Lưu ở hộp thêm nhanh', 'Click',
     'During:\n– Thiếu Tên → “Vui lòng nhập tên.”; Thương hiệu thiếu Mã → “Vui lòng nhập mã.”.\n'
     'After:\n– Tạo danh mục mới, tự chọn vào ô; báo “Đã thêm nhanh thành công.”.'),
])

# ------------------------------------------------------------------ 2.10 Dịch vụ
d.h3('2.10 Thêm dịch vụ & chi phí khác')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Thêm dịch vụ & chi phí khác', 'crud', actor=A_LAP)
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='create')
d.intro_table(
    ten='Thêm dịch vụ & chi phí khác',
    mota='Thêm khoản dịch vụ / chi phí từ danh mục dịch vụ – chi phí vào khối B của BOM.',
    tacnhan=TN_LAP,
    dieukien='Đang ở màn Tạo mới / Cập nhật BOM.',
    chinh='1. Người dùng bấm “Thêm mới” ở dòng “B — Dịch vụ & Chi phí khác”.\n'
          '2. Hệ thống mở popup “Thêm dịch vụ / chi phí” liệt kê danh mục, lọc nhanh Tất cả / Dịch vụ có tính DT / Chi phí khác.\n'
          '3. Người dùng tìm theo tên và bấm vào khoản cần thêm.\n'
          '4. Hệ thống thêm vào khối B (số lượng luôn 1), báo “Đã thêm: <tên>”.',
    phu='• Không tìm thấy → “Không tìm thấy mục nào. Bấm \"Thêm mới\" để tạo nhanh.”; bấm “Thêm mới” để tạo nhanh khoản '
        'dịch vụ / chi phí mới.\n'
        '• Xoá khoản ở khối B bằng nút thùng rác của dòng; kéo biểu tượng ⋮⋮ để đổi thứ tự.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Thêm mới', shot=shot('11-dich-vu.png'), shot_caption='Popup Thêm dịch vụ / chi phí')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Thêm dịch vụ / chi phí', '–'),
    ('Ô tìm kiếm', 'Textbox', 'Enable', 'Chuỗi', 'Không', 'Trống', '“Tìm theo tên dịch vụ / chi phí...”; tìm sau khi ngừng gõ.'),
    ('Nút Thêm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở hộp tạo nhanh khoản dịch vụ / chi phí.'),
    ('Bộ lọc loại', 'Radio', 'Enable', '3 giá trị', 'Không', 'Tất cả', 'Tất cả · Dịch vụ có tính DT · Chi phí khác.'),
    ('Danh sách kết quả', 'List', 'Enable', '–', '–', 'Theo dữ liệu', 'Mỗi dòng: tên, nhãn loại, VAT %. Bấm để thêm.'),
    ('Khối B trên lưới', 'Table/Grid', 'Enable', '–', '–', 'Chưa có dịch vụ / chi phí',
     'Mỗi dòng: tay kéo · nút xoá · STT · Mã · Tên (biểu tượng dịch vụ / chi phí) · Ghi chú.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm một khoản trong danh sách', 'Click', 'After:\n– Thêm vào khối B, số lượng 1; báo “Đã thêm: <tên>”.'),
    ('Bấm thùng rác ở dòng khối B', 'Click', 'After:\n– Bỏ dòng khỏi lưới (chỉ ghi xuống khi Lưu BOM).'),
    ('Kéo thả dòng khối B', 'Drag', 'After:\n– Đổi thứ tự dòng dịch vụ.'),
])

# ------------------------------------------------------------------ 2.11 Nhóm hàng
d.h3('2.11 Quản lý nhóm hàng 2 cấp')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Quản lý nhóm hàng 2 cấp', 'crud', actor=A_LAP)
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='create')
d.intro_table(
    ten='Quản lý nhóm hàng 2 cấp',
    mota='Chia hàng hoá trong BOM thành nhóm Cấp 1 (I, II…) và nhóm con Cấp 2 (I.1, I.2…): thêm, đổi tên, xoá, kéo thả '
         'đổi thứ tự, thu gọn / mở rộng.',
    tacnhan=TN_LAP,
    dieukien='Đang ở màn Tạo mới / Cập nhật BOM.',
    chinh='1. Người dùng bấm “Thêm nhóm” (Cấp 1) hoặc “Thêm nhóm con” ở một nhóm Cấp 1.\n'
          '2. Hệ thống mở hộp “Tạo nhóm hàng”.\n'
          '3. Người dùng nhập Tên nhóm, bấm “Lưu” (hoặc Enter).\n'
          '4. Hệ thống thêm nhóm vào lưới; hàng chưa thuộc nhóm nào được đưa vào nhóm mới.',
    phu='• Bấm bút ở dòng nhóm → hộp “Sửa nhóm hàng” để đổi tên.\n'
        '• Bấm thùng rác ở dòng nhóm → hỏi “Xoá nhóm này sẽ xoá tất cả hàng hoá trong nhóm. Bạn có chắc?”; Xoá → '
        'xoá nhóm và các nhóm con, hàng trong nhóm chuyển về nhóm Cấp 1 đầu tiên còn lại.\n'
        '• Tên nhóm trống → nút Lưu khoá.\n'
        '• Kéo biểu tượng ⋮⋮ ở dòng nhóm để đổi thứ tự trong cùng cấp, cùng nhóm cha.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Thêm nhóm / Thêm nhóm con', shot=shot('12-nhom.png'),
         shot_caption='Hộp Tạo nhóm hàng trên lưới BOM có nhóm 2 cấp')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp', 'Label', 'Hiển thị', '–', '–', 'Tạo nhóm hàng / Sửa nhóm hàng', '–'),
    ('Tên nhóm', 'Textbox', 'Enable', '≤ 255 ký tự', 'Có', 'Trống / tên cũ', 'Gợi ý “Nhập tên nhóm hàng”.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Khoá khi tên trống', '–'),
    ('Nút Huỷ', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Dòng nhóm trên lưới', 'Table/Grid', 'Enable', '–', '–', 'Mở rộng',
     'Nút mở / thu · bút sửa · thùng rác · tay kéo · số thứ tự (I / I.1) · tên nhóm · “Thêm mới” · “Thêm nhóm con” '
     '(chỉ Cấp 1) · “(n hàng)”.'),
    ('Nút Thu gọn tất cả / Mở rộng tất cả', 'Button', 'Enable', '–', '–', 'Thu gọn tất cả', 'Thu / mở mọi nhóm.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu (hộp nhóm)', 'Click',
     'Before:\n– Tên trống → không xử lý.\nAfter:\n– Thêm: tạo nhóm cùng cấp / con của nhóm cha, gom hàng chưa có nhóm vào '
     'nhóm mới. Sửa: đổi tên nhóm.'),
    ('Bấm xoá nhóm → Xoá', 'Click',
     'After:\n– Xoá nhóm và nhóm con; hàng của nhóm bị xoá chuyển về nhóm Cấp 1 đầu tiên (không còn nhóm → bỏ nhóm).'),
    ('Kéo thả dòng nhóm', 'Drag', 'After:\n– Đổi thứ tự nhóm trong cùng cấp.'),
    ('Bấm Lưu BOM', 'Click', 'During:\n– Tên nhóm trống → “Vui lòng nhập tên nhóm hàng.”; > 255 ký tự → “Tên nhóm hàng không được vượt quá 255 ký tự.”'),
])

# ------------------------------------------------------------------ 2.12 Thao tác lưới
d.h3('2.12 Thao tác trên lưới hàng hoá')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Thao tác trên lưới hàng hoá', 'crud', actor=A_LAP)
d.p('2.12.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='create')
d.intro_table(
    ten='Thao tác trên lưới hàng hoá',
    mota='Các thao tác trên từng dòng hàng: sửa nhanh, thêm hàng con, nhân bản hàng tạm, xoá dòng, nhập số lượng / ghi '
         'chú, đổi đơn vị tính hàng ERP, ẩn / hiện hàng con khi in – xuất, kéo thả đổi thứ tự.',
    tacnhan=TN_LAP,
    dieukien='Đang ở màn Tạo mới / Cập nhật BOM; lưới đã có dòng hàng.',
    chinh='1. Người dùng rê chuột vào dòng hàng cha để hiện các nút dưới tên hàng.\n'
          '2. Bấm “Sửa” → hộp “Sửa nhanh hàng hoá” (hoặc “Sửa nhanh dịch vụ”), chỉnh rồi bấm “Lưu cập nhật”.\n'
          '3. Hệ thống cập nhật dòng trên lưới, báo “Đã cập nhật hàng hoá.” / “Đã cập nhật dịch vụ.”.',
    phu='• “Thêm con” (chỉ hàng tạm) → mở FR-08 để thêm hàng con.\n'
        '• “Nhân bản” (hàng tạm không có hàng con) → thêm 1 dòng cùng hàng, dùng chung mã; báo “Đã nhân bản hàng tạm '
        '(dùng chung mã). Chỉnh số lượng nếu cần rồi Lưu.”.\n'
        '• “Xoá” dòng cha → hỏi “Bạn có chắc muốn xoá dòng cha và toàn bộ hàng con của nó?”; dòng con → “Bạn có chắc '
        'muốn xoá dòng con này?”.\n'
        '• Hàng ERP: hộp Sửa nhanh ghi “Hàng hoá lấy từ ERP — chỉ có thể sửa Số lượng. Giá nhập sẽ được lấy từ ERP khi '
        'tạo báo giá.”, các ô khác khoá; số lượng hàng con của hàng ERP khoá.\n'
        '• Sửa nhanh thiếu tên → “Vui lòng nhập tên hàng hoá.” (dịch vụ: “Vui lòng nhập tên dịch vụ.”); thiếu ĐVT → '
        '“Vui lòng chọn đơn vị tính.”; trùng mã → “Mã hàng cha đang bị trùng trong BOM.” / “Mã hàng con đang bị trùng '
        'trong cùng một dòng cha.”.',
    dacbiet='Mọi thay đổi trên lưới chỉ ghi xuống hệ thống khi bấm “Lưu nháp” / “Lưu BOM”.')
d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa => Sửa (dòng hàng)', shot=shot('13c-sua-hang-tam.png'),
         shot_caption='Các nút trên dòng hàng tạm khi rê chuột')
d.figure(shot('14-sua-nhanh.png'), 'Hộp Sửa nhanh hàng hoá', width_in=6.2)
d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tay kéo ⋮⋮', 'Icon', 'Enable', '–', '–', 'Hiển thị', 'Kéo đổi thứ tự hàng cha / hàng con.'),
    ('Nút +/− ở dòng cha', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Mở', 'Chỉ hiện khi có hàng con; thu / mở hàng con.'),
    ('Nút mắt ở dòng cha ERP', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiện',
     'Chỉ hàng ERP có hàng con; “Ẩn hàng con khi in/xuất” / “Hiện hàng con khi in/xuất”.'),
    ('Nút Thêm con', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn với hàng ERP, dịch vụ', '–'),
    ('Nút Sửa', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở hộp Sửa nhanh.'),
    ('Nút Nhân bản', 'Button', 'Enable / Ẩn', '–', '–', 'Chỉ hàng tạm không có hàng con', 'Tooltip “Tạo thêm 1 dòng cùng hàng tạm này (dùng chung mã)”.'),
    ('Nút Xoá', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hỏi xác nhận trước khi xoá.'),
    ('Ô ĐVT (hàng ERP không có con)', 'Dropdown', 'Enable', 'Đơn vị quy đổi của hàng', 'Không', 'ĐVT hiện tại', '–'),
    ('Ô Ghi chú / Số lượng trên dòng', 'Textbox / Number', 'Enable', '≥ 0', 'Không', 'Theo dữ liệu', '–'),
    ('Hộp Sửa nhanh: Tên hàng, Mã', 'Textbox', 'Enable / Disable', '–', 'Có', 'Theo dòng', 'Mã luôn khoá.'),
    ('Hộp Sửa nhanh: Dự án, Giải pháp', 'Textbox', 'Disable', '–', '–', 'Theo BOM', '–'),
    ('Hộp Sửa nhanh: Đơn vị tính', 'Dropdown', 'Enable', 'Danh mục ĐVT', 'Có', 'Theo dòng', '–'),
    ('Hộp Sửa nhanh: Model, Thương hiệu, Xuất xứ', 'Dropdown', 'Enable', 'Danh mục', 'Không', 'Theo dòng', 'Ẩn với dịch vụ.'),
    ('Hộp Sửa nhanh: Số lượng cần dùng, Ghi chú, Đặc điểm / Thông số kỹ thuật', 'Number / Textbox / Textarea', 'Enable', '≥ 0', 'Không', 'Theo dòng', '–'),
    ('Nút Lưu cập nhật / Huỷ / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu cập nhật', 'Click',
     'During:\n– Kiểm tra Tên, ĐVT, trùng mã như Dòng sự kiện phụ; có lỗi → báo dưới ô và dừng.\n'
     'After:\n– Cập nhật dòng trên lưới; báo “Đã cập nhật hàng hoá.” / “Đã cập nhật dịch vụ.”.'),
    ('Bấm Nhân bản', 'Click', 'After:\n– Chèn dòng mới ngay dưới, dùng chung mã khi lưu; báo như Dòng sự kiện phụ.'),
    ('Bấm Xoá → Xoá', 'Click', 'After:\n– Bỏ dòng (dòng cha kèm toàn bộ hàng con); đánh lại STT.'),
    ('Đổi số lượng hàng cha', 'Change', 'After:\n– Tính lại số liệu tổng của dòng.'),
    ('Kéo thả dòng', 'Drag', 'After:\n– Đổi thứ tự hàng cha / hàng con trong nhóm; đánh lại STT.'),
])

# ------------------------------------------------------------------ 2.13 Import
d.h3('2.13 Import hàng hoá từ Excel')
d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'Import hàng hoá từ Excel', 'io', actor=A_LAP)
d.p('2.13.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột; Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.',
           anchor='excel')
d.intro_table(
    ten='Import hàng hoá từ Excel',
    mota='Nạp file Excel (cùng định dạng file xuất ở FR-14) để kiểm tra rồi áp vào lưới BOM theo 2 phương thức: '
         'Import từng phần hoặc Thay thế hoàn toàn.',
    tacnhan=TN_LAP,
    dieukien='Đang ở màn Cập nhật BOM (BOM đã được lưu ít nhất 1 lần), người dùng là người tạo BOM và có Q1.',
    chinh='1. Người dùng bấm “Import Excel” ở khối Chi tiết BOM LIST.\n'
          '2. Hệ thống mở popup “Import hàng hoá BOM List”.\n'
          '3. Người dùng bấm “Chọn file Excel” (có thể “Tải file mẫu” trước), rồi “Load lên bảng”.\n'
          '4. Người dùng bấm “Validate”; hệ thống kiểm tra từng dòng, đánh dấu Hợp lệ / Hợp lệ (tạo mới) / Chờ xác nhận / '
          'Lỗi và hiện số đếm.\n'
          '5. Người dùng sửa dòng lỗi ngay trên bảng rồi Validate lại, hoặc bật “Bỏ qua dòng lỗi”.\n'
          '6. Người dùng bấm “Import”, chọn phương thức rồi bấm “Áp vào lưới”.\n'
          '7. Hệ thống áp dữ liệu vào lưới, báo “Đã áp dữ liệu import vào lưới, kiểm tra rồi bấm \"Lưu BOM\".”.\n'
          '8. Người dùng kiểm tra lưới và bấm “Lưu BOM”.',
    phu='• Chưa lưu BOM → nút Import Excel khoá, tooltip “Vui lòng lưu nháp BOM trước khi import”.\n'
        '• File không phải Excel → “Định dạng file không hỗ trợ. Vui lòng tải lên file Excel đúng định dạng.”.\n'
        '• Bấm Load khi chưa chọn file → “Vui lòng chọn file Excel trước.”.\n'
        '• File sai cấu trúc cột → “Cấu trúc file không hợp lệ. Vui lòng sử dụng file template chuẩn tải từ hệ thống.”.\n'
        '• Validate khi chưa có dòng → “Không có dữ liệu để validate. Hãy load file lên bảng trước.”; lỗi máy chủ → '
        '“Lỗi khi validate dữ liệu import”.\n'
        '• Dòng “Chờ xác nhận” (mã hàng tạm trùng hàng đã có trong dự án) → chọn “Tạo mã mới” (nhập mã mới rồi Validate '
        'lại) hoặc “Giữ nguyên mã và đồng bộ”.\n'
        '• File xuất từ BOM khác → popup “Phát hiện dữ liệu thuộc BOM khác”, nút “Sao chép vào lưới” (tạo dòng mới).\n'
        '• Sửa ô sau khi Validate → “n dòng đã sửa — cần Validate lại”, nút Import khoá.',
    dacbiet='Import không tự lưu: dữ liệu chỉ ghi xuống hệ thống khi bấm “Lưu BOM”. Model / Thương hiệu / Xuất xứ chưa '
            'có trong danh mục được báo vàng “Hợp lệ (tạo mới)” và tự tạo khi import.')
d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa => Import Excel', shot=shot('15-import.png'),
         shot_caption='Popup Import hàng hoá BOM List sau khi Validate')
d.figure(shot('15c-import-phuong-thuc.png'), 'Hộp Chọn phương thức áp dữ liệu', width_in=6.2)
d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Import hàng hoá BOM List',
     'Dòng phụ: “Validate rồi áp dữ liệu vào lưới BOM — chọn phương thức (từng phần / thay thế), kiểm tra rồi bấm \"Lưu BOM\"”.'),
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx, .xls', 'Có', 'Hiển thị', 'Hiện tên file đã chọn bên cạnh.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải file Mau_import_bomlist.xlsx.'),
    ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Khoá khi chưa chọn file', '–'),
    ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Khoá khi bảng rỗng', '–'),
    ('Nút Chỉ dòng lỗi / Hiện tất cả', 'Button', 'Enable / Disable', '–', '–', 'Chỉ dòng lỗi', '–'),
    ('Số đếm', 'Badge', 'Hiển thị', '–', '–', 'Ẩn trước Validate', 'Tổng · Hợp lệ · Lỗi · Chờ xác nhận.'),
    ('Bảng dữ liệu', 'Table/Grid', 'Enable', '14 cột', '–', 'Chưa có dữ liệu',
     '# · Trạng thái · Loại* · Nhóm hàng cha (Cấp 1) · Nhóm hàng con (Cấp 2) · STT* · Mã hàng cha · Mã hàng* · Tên hàng* · '
     'Model · Thương hiệu* · Xuất xứ* · ĐVT* · Số lượng* · Thông số kỹ thuật · Ghi chú. Ô sửa được trực tiếp; dòng hợp lệ '
     'bị khoá sau Validate; lỗi từng dòng hiện ngay dưới dòng.'),
    ('Nút Bỏ qua dòng lỗi', 'Button', 'Enable / Disable', '–', '–', 'Tắt', 'Bật được khi đã Validate và còn dòng lỗi.'),
    ('Nút Xoá trạng thái validate', 'Button', 'Enable / Disable', '–', '–', 'Khoá trước Validate', 'Mở khoá các dòng để sửa lại.'),
    ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Khoá',
     'Chỉ bấm được khi đã Validate, không có dòng sửa dở, không còn dòng Chờ xác nhận chưa chọn, và không còn lỗi (hoặc đã Bỏ qua dòng lỗi).'),
    ('Nút Làm mới / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Làm mới xoá file và bảng.'),
    ('Hộp Chọn phương thức áp dữ liệu', 'Modal', 'Hiển thị', '2 lựa chọn', 'Có', 'Import từng phần',
     'Import từng phần: giữ dòng không có trong file, cập nhật dòng khớp Line ID, thêm dòng mới. Thay thế hoàn toàn: '
     'xoá toàn bộ hàng hoá, nhóm, dịch vụ trên lưới rồi nạp lại. Nút “Áp vào lưới” / “Huỷ”.'),
])
d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Load lên bảng', 'Click',
     'During:\n– Chưa chọn file / sai định dạng / sai cấu trúc → thông báo như Dòng sự kiện phụ.\n'
     'After:\n– Đọc file, hiện các dòng lên bảng ở trạng thái “Chưa validate”.'),
    ('Bấm Validate', 'Click',
     'During:\n– Máy chủ kiểm tra từng dòng, ví dụ: “Loại không hợp lệ. Chỉ nhận \'Hàng hoá\' hoặc \'Dịch vụ & Chi phí '
     'khác\'.” · “Tên hàng là bắt buộc.” · “Nhóm hàng con phải có Nhóm hàng cha.” · “Số lượng phải lớn hơn 0” · '
     '“Đơn vị tính là bắt buộc” · “Dịch vụ & Chi phí khác không hỗ trợ hàng cấp con.” · “Dòng con [STT] không tìm thấy '
     'dòng cha [STT] ở phía trên.” · giới hạn độ dài Tên 255, Nhóm 250, Ghi chú 500 ký tự.\n'
     'After:\n– Đánh dấu trạng thái từng dòng, khoá dòng hợp lệ, hiện số đếm.'),
    ('Bấm Tạo mã mới / Giữ nguyên mã và đồng bộ', 'Click',
     'After:\n– Ghi nhận cách xử lý dòng Chờ xác nhận; Tạo mã mới yêu cầu nhập mã rồi Validate lại.'),
    ('Bấm Import → Áp vào lưới', 'Click',
     'Before:\n– Nút chỉ bấm được khi đủ điều kiện (xem bảng giao diện).\n'
     'After:\n– Áp các dòng hợp lệ vào lưới theo phương thức đã chọn, đóng popup, báo “Đã áp dữ liệu import vào lưới, '
     'kiểm tra rồi bấm \"Lưu BOM\".”. Chưa ghi xuống hệ thống.'),
])

# ------------------------------------------------------------------ 2.14 Xuất Excel BOM
d.h3('2.14 Xuất Excel BOM')
d.p('2.14.1 Biểu đồ Usecase')
d.uc_figure('FR-14', 'Xuất Excel BOM', 'io', actor=A_XEM)
d.p('2.14.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='excel')
d.intro_table(
    ten='Xuất Excel BOM',
    mota='Xuất hàng hoá và dịch vụ của 1 BOM ra file Excel đúng định dạng file import, để sửa rồi nạp lại bằng FR-13.',
    tacnhan=TN_XEM,
    dieukien='BOM đã được lưu; người dùng xem được BOM.',
    chinh='1. Người dùng bấm “Xuất Excel” ở màn Chi tiết (thanh nút cuối màn hoặc khối Chi tiết BOM LIST) hoặc ở màn Cập nhật.\n'
          '2. Hệ thống mở popup “Xuất Excel BOM List”, tích sẵn “Xuất hàng hoá cấp con”.\n'
          '3. Người dùng bấm “Xuất Excel”.\n'
          '4. Hệ thống tải file <Mã BOM>.xlsx, báo “Xuất Excel thành công”.',
    phu='• Bỏ tích “Xuất hàng hoá cấp con” → chỉ xuất hàng cha.\n'
        '• Lỗi → “Lỗi khi xuất Excel”.\n'
        '• Màn Tạo mới chưa lưu → nút khoá, tooltip “Vui lòng lưu nháp BOM trước khi xuất Excel”.',
    dacbiet='File luôn đủ cột theo định dạng import, không cho chọn cột và không có cột giá.')
d.p('2.14.3 Layout màn hình')
d.layout(menu=MENU + ' => Mã BOM => Xuất Excel', shot=shot('16-xuat-bom.png'), shot_caption='Popup Xuất Excel BOM List')
d.p('2.14.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Xuất Excel BOM List', '–'),
    ('Ghi chú định dạng', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“File xuất ra theo đúng định dạng file import (12 cột) nên có thể sửa rồi nạp lại bằng chức năng Import hàng hoá BOM List.”'),
    ('Xuất hàng hoá cấp con', 'Checkbox', 'Enable', '–', 'Không', 'Tích', '–'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải file <Mã BOM>.xlsx.'),
    ('Nút Huỷ', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.14.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel (trong popup)', 'Click',
     'After:\n– Đóng popup, tải file theo tuỳ chọn hàng con; báo “Xuất Excel thành công”.\n– Lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.15 Chỉnh sửa
d.h3('2.15 Chỉnh sửa BOM')
d.p('2.15.1 Biểu đồ Usecase')
d.uc_figure('FR-15', 'Chỉnh sửa BOM', 'crud', actor=A_LAP)
d.p('2.15.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung '
           '- Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Chỉnh sửa BOM',
    mota='Sửa thông tin chung và lưới hàng hoá của BOM do mình tạo khi BOM chưa vào luồng duyệt.',
    tacnhan=TN_LAP,
    dieukien='Người dùng là người tạo BOM, có Q1; BOM ở trạng thái Đang tạo hoặc Hoàn thành (nút Sửa còn hiện với '
             '“Không duyệt”, xem Dòng sự kiện phụ).',
    chinh='1. Người dùng bấm biểu tượng bút ở cột Hành động, hoặc nút “Sửa” ở màn chi tiết.\n'
          '2. Hệ thống mở màn “Cập nhật BOM List” với dữ liệu hiện tại, ô Mã BOM chỉ đọc.\n'
          '3. Người dùng chỉnh thông tin, lưới hàng hoá (FR-08…FR-13), BOM con (với BOM tổng hợp).\n'
          '4. Người dùng bấm “Lưu BOM” (hoặc “Lưu nháp” nếu BOM đang “Đang tạo”).\n'
          '5. Hệ thống lưu, ghi lịch sử thay đổi, báo “Cập nhật BOM LIST thành công.” và quay về danh sách.',
    phu='• BOM ở trạng thái khác Đang tạo / Hoàn thành mở màn Sửa → “BOM ở trạng thái này không được phép sửa.” và '
        'chuyển sang màn chi tiết (áp dụng cả với “Không duyệt” dù nút Sửa vẫn hiện).\n'
        '• Không phải người tạo → máy chủ chặn “Chỉ người tạo BOM mới được phép sửa.”.\n'
        '• Máy chủ chặn trạng thái → “BOM ở trạng thái này không được phép sửa. Chỉ BOM \"Đang tạo\", \"Hoàn thành\" hoặc '
        '\"Không duyệt\" mới được sửa.”.\n'
        '• Thiếu Q1 → “Bạn không có quyền sửa BOM List”, về danh sách.\n'
        '• Lỗi khác → “Cập nhật BOM LIST thất bại. Vui lòng thử lại.”.',
    dacbiet='Lưu BOM tổng hợp với danh sách BOM con mới: BOM thành phần được thêm chuyển “Đã được tổng hợp”, BOM thành '
            'phần bị bỏ ra quay về “Hoàn thành”.')
d.p('2.15.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('13-sua.png'), shot_caption='Màn Cập nhật BOM List (BOM có nhóm 2 cấp)')
d.p('2.15.4 Mô tả chi tiết giao diện')
d.ui_table(FORM_UI)
d.p('2.15.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Cập nhật', 'System',
     'Before:\n– Thiếu Q1 → “Bạn không có quyền sửa BOM List”, về danh sách.\n'
     '– BOM không ở Đang tạo / Hoàn thành → “BOM ở trạng thái này không được phép sửa.”, chuyển màn chi tiết.\n'
     'After:\n– Nạp dữ liệu BOM, nhóm, hàng hoá, dịch vụ, BOM con.'),
    ('Bấm Lưu nháp / Lưu BOM', 'Click',
     'Before:\n– Kiểm tra Q1, người tạo và trạng thái như Dòng sự kiện phụ; vi phạm → báo lỗi, dừng.\n'
     'During:\n– Kiểm tra dữ liệu như FR-06 / FR-07 (kể cả trùng BOM tổng hợp trên cùng version).\n'
     'After:\n– Cập nhật BOM: Lưu nháp giữ Đang tạo, Lưu BOM chuyển Hoàn thành; ghi lại version hiện hành.\n'
     '– Đồng bộ trạng thái BOM con (BR-08).\n'
     '– Ghi lịch sử “Chỉnh sửa — Chỉnh sửa BOM List” kèm trường thay đổi (cũ → mới) và hàng thêm / xoá / sửa.\n'
     '– Báo “Cập nhật BOM LIST thành công.” và quay về danh sách.'),
])

# ------------------------------------------------------------------ 2.16 Xem chi tiết
d.h3('2.16 Xem chi tiết BOM')
d.p('2.16.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết BOM',
    mota='Xem toàn bộ thông tin BOM ở chế độ chỉ đọc kèm các nút thao tác khớp với màn danh sách.',
    tacnhan=TN_XEM,
    dieukien='Người dùng xem được BOM theo phạm vi.',
    chinh='1. Người dùng bấm mã BOM ở danh sách (hoặc liên kết trong thông báo “BOM … đã được duyệt”).\n'
          '2. Hệ thống mở màn “Chi tiết BOM List: <Mã BOM>” gồm: badge trạng thái, người tạo – ngày tạo, thông tin chung, '
          'chip các BOM con (BOM tổng hợp), lưới hàng hoá chỉ đọc, khối Lịch sử (thu gọn).\n'
          '3. Người dùng dùng các nút ở thanh dưới cùng: Sửa · In · Xuất Excel · Sao chép · Xóa · Quay lại.',
    phu='• Nút Sửa / Sao chép / Xóa hiện theo điều kiện ở BR-05.\n'
        '• Bấm Quay lại khi trang mở ở tab mới → về danh sách.')
d.p('2.16.2 Layout màn hình')
d.layout(menu=MENU + ' => Mã BOM', shot=shot('17-chi-tiet.png'), shot_caption='Màn Chi tiết BOM List – BOM Hoàn thành của chính người dùng')
d.figure(shot('23-da-duyet.png'), 'Màn Chi tiết BOM tổng hợp “Đã duyệt” – không còn nút Sửa / Xóa', width_in=6.2)
d.p('2.16.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết BOM List: <Mã BOM>', '–'),
    ('Badge trạng thái', 'Badge', 'Read-only', '6 giá trị', 'Theo dữ liệu', 'Góc trái khối thông tin.'),
    ('Người tạo — ngày tạo', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm:ss', 'Theo dữ liệu', 'Góc phải khối thông tin.'),
    ('Mã BOM, Tên BOM LIST, Dự án, Giải pháp, Hạng mục, Khách hàng, Ghi chú, Loại BOM LIST', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Đã chọn / chip BOM con', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Chỉ BOM tổng hợp.'),
    ('Lưới Chi tiết BOM LIST', 'Table/Grid', 'Read-only', '–', 'Mở rộng',
     'STT · Mã hàng · Tên hàng (kèm Ghi chú nội bộ nếu có) · Model · Thương hiệu · Xuất xứ · ĐVT · Thông số kỹ thuật · '
     'Ghi chú · Số lượng; nhóm thu / mở được; nút Ẩn cấp con / Hiện cấp con, Thu gọn tất cả.'),
    ('Khối Lịch sử', 'Section', 'Enable', '–', 'Thu gọn', 'Xem FR-20.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Hiện khi là người tạo và BOM Đang tạo / Hoàn thành / Không duyệt.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'FR-19.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'FR-14.'),
    ('Nút Sao chép', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q1', 'FR-17.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Hiện khi có Q1, là người tạo và BOM Đang tạo.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '–'),
], required=False)
d.p('2.16.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System', 'After:\n– Nạp chi tiết BOM (không nạp danh mục dùng cho form); hiện nút theo điều kiện.'),
    ('Bấm Sửa / Sao chép', 'Click', 'After:\n– Mở màn Cập nhật (FR-15) / màn Sao chép (FR-17).'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về màn trước; mở ở tab mới thì về danh sách.'),
])

# ------------------------------------------------------------------ 2.17 Sao chép
d.h3('2.17 Sao chép BOM')
d.p('2.17.1 Biểu đồ Usecase')
d.uc_figure('FR-17', 'Sao chép BOM', 'crud', actor=A_LAP)
d.p('2.17.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.',
           anchor='create')
d.intro_table(
    ten='Sao chép BOM',
    mota='Tạo BOM mới điền sẵn từ một BOM có sẵn (ở mọi trạng thái), để chỉnh tiếp rồi lưu thành BOM độc lập.',
    tacnhan=TN_LAP,
    dieukien='Người dùng có quyền Q1 và xem được BOM nguồn.',
    chinh='1. Người dùng bấm “Sao chép” (menu ⋮ ở danh sách hoặc nút ở màn chi tiết).\n'
          '2. Hệ thống mở màn “Sao chép BOM List” điền sẵn dữ liệu BOM nguồn: Tên = “<tên nguồn> - Sao chép”, chưa có '
          'mã, trạng thái Đang tạo, giữ nhóm, hàng hoá, dịch vụ; KHÔNG giữ danh sách BOM con.\n'
          '3. Người dùng chỉnh rồi bấm “Lưu nháp” / “Lưu BOM”.\n'
          '4. Hệ thống tạo BOM mới (ghi nhận BOM nguồn), báo “Đã lưu BOM LIST thành công.” và về danh sách.',
    phu='• Version giải pháp / hạng mục lấy theo version HIỆN HÀNH, không theo BOM nguồn.\n'
        '• BOM nguồn không thay đổi; các BOM con của BOM nguồn không bị đổi trạng thái.\n'
        '• Kiểm tra dữ liệu và thông báo như FR-06 / FR-07.')
d.p('2.17.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Sao chép', shot=shot('18-sao-chep.png'), shot_caption='Màn Sao chép BOM List')
d.p('2.17.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Sao chép BOM List', '–'),
    ('Tên BOM LIST', 'Textbox', 'Enable', '≤ 255 ký tự', 'Có', '<tên nguồn> - Sao chép', '–'),
    ('Mã BOM', 'Textbox', 'Ẩn', '–', '–', 'Ẩn', 'Mã mới sinh khi lưu.'),
    ('Dự án, Giải pháp, Hạng mục, Khách hàng, Ghi chú, Loại BOM LIST', 'Form', 'Enable', '–', 'Như FR-06', 'Theo BOM nguồn', '–'),
    ('BOM con', 'Label', 'Hiển thị', '–', '–', 'Đã chọn: 0 BL con', 'Không kế thừa BOM con.'),
    ('Lưới hàng hoá, dịch vụ, nhóm', 'Table/Grid', 'Enable', '–', '–', 'Theo BOM nguồn', '–'),
    ('Nút Quay lại / Lưu nháp / Lưu BOM', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.17.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sao chép', 'System',
     'Before:\n– Thiếu Q1 → “Bạn không có quyền tạo BOM List”, về danh sách.\n'
     'After:\n– Nạp dữ liệu BOM nguồn đã bỏ mã, người tạo, ngày tạo, BOM con.'),
    ('Bấm Lưu nháp / Lưu BOM', 'Click',
     'During:\n– Kiểm tra như FR-06.\nAfter:\n– Tạo BOM mới gắn BOM nguồn; ghi lịch sử “Tạo mới”; báo “Đã lưu BOM LIST thành công.” và về danh sách.'),
])

# ------------------------------------------------------------------ 2.18 Xóa
d.h3('2.18 Xóa BOM')
d.p('2.18.1 Biểu đồ Usecase')
d.uc_figure('FR-18', 'Xóa BOM', 'action', actor=A_LAP)
d.p('2.18.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xoá. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='delete')
d.intro_table(
    ten='Xóa BOM',
    mota='Xoá hẳn BOM đang lập dở (Đang tạo) do chính mình tạo.',
    tacnhan=TN_LAP,
    dieukien='Người dùng có Q1, là người tạo BOM; BOM ở trạng thái Đang tạo.',
    chinh='1. Người dùng bấm biểu tượng thùng rác ở dòng BOM (hoặc nút “Xóa” ở màn chi tiết).\n'
          '2. Hệ thống hỏi “Bạn có chắc muốn xóa BOM List \'<Mã> - <Tên>\'?”.\n'
          '3. Người dùng bấm “Xóa”.\n'
          '4. Hệ thống xoá BOM, báo “Xóa BOM List thành công” và nạp lại danh sách (từ màn chi tiết thì về danh sách).',
    phu='• Bấm “Hủy” → đóng hộp, không xoá.\n'
        '• Máy chủ chặn: “Chỉ được xoá BOM List ở trạng thái Đang tạo” / “Chỉ người tạo mới được xoá BOM List này”.\n'
        '• Lỗi khác → “Lỗi khi xóa BOM List”.')
d.p('2.18.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('19-xoa.png'), shot_caption='Hộp xác nhận xoá BOM')
d.p('2.18.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo BOM', '“Bạn có chắc muốn xóa BOM List \'<Mã> - <Tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '–'),
], required=False, scope=False)
d.p('2.18.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa (hộp xác nhận)', 'Click',
     'Before:\n– Kiểm tra trạng thái Đang tạo và người tạo; vi phạm → thông báo như Dòng sự kiện phụ, dừng.\n'
     'After:\n– Xoá BOM cùng hàng hoá, liên kết BOM con và lịch sử của BOM.\n'
     '– BOM tổng hợp bị xoá → các BOM thành phần từng là con quay về “Hoàn thành”.\n'
     '– Báo “Xóa BOM List thành công”.'),
])

# ------------------------------------------------------------------ 2.19 In
d.h3('2.19 In BOM')
d.p('2.19.1 Biểu đồ Usecase')
d.uc_figure('FR-19', 'In BOM', 'io', actor=A_XEM)
d.p('2.19.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='notice')
d.intro_table(
    ten='In BOM',
    mota='In “DANH MỤC VẬT TƯ (BOM LIST)” của 1 BOM: chọn cột, xem trước rồi in.',
    tacnhan=TN_XEM,
    dieukien='Người dùng xem được BOM.',
    chinh='1. Người dùng bấm “In BOM List” (menu ⋮ ở danh sách) hoặc nút “In” ở màn chi tiết.\n'
          '2. Hệ thống nạp dữ liệu BOM và mở popup “Cấu hình in BOM List”, tích sẵn tất cả cột và “Hiện hàng hoá cấp con”.\n'
          '3. Người dùng chọn cột, bấm “Xem trước”.\n'
          '4. Hệ thống mở “Xem trước BOM List”: letterhead công ty, tiêu đề, thông tin BOM, bảng hàng theo nhóm, khối '
          'Dịch vụ & Chi phí khác, ghi chú, chữ ký Người lập.\n'
          '5. Người dùng bấm “In”.',
    phu='• Bỏ hết cột → “Vui lòng chọn ít nhất 1 cột để in”.\n'
        '• Không tải được dữ liệu → “Không tải được dữ liệu in BOM List”.')
d.p('2.19.3 Layout màn hình')
d.layout(menu=MENU + ' => Mã BOM => In => Xem trước', shot=shot('20-in-cau-hinh.png'), shot_caption='Popup Cấu hình in BOM List')
d.figure(shot('21-in-xem-truoc.png'), 'Bản xem trước BOM List', width_in=6.2)
d.p('2.19.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Hiện hàng hoá cấp con', 'Checkbox', 'Enable', '–', 'Không', 'Tích', '–'),
    ('Chọn tất cả', 'Checkbox', 'Enable', '–', 'Không', 'Tích', '–'),
    ('Danh sách cột', 'Checkbox', 'Enable', '10 cột', 'Có ≥ 1', 'Tích đủ',
     'STT · Mã hàng · Tên hàng · Model · Thương hiệu · Xuất xứ · ĐVT · Thông số kỹ thuật · Ghi chú · Số lượng. Không có cột giá.'),
    ('Thông báo lỗi', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Vui lòng chọn ít nhất 1 cột để in”.'),
    ('Nút Xem trước / Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Bản xem trước', 'Modal', 'Read-only', '–', '–', '–',
     'Letterhead theo công ty của người đang đăng nhập; thông tin Mã BOM, Tên BOM, Dự án, Giải pháp, Hạng mục, Khách hàng, '
     'Loại BOM, Trạng thái, Người tạo, Ngày tạo; bảng hàng theo nhóm (I., I.1…); khối Dịch vụ & Chi phí khác; Ghi chú; NGƯỜI LẬP.'),
    ('Nút In', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở hộp thoại in của trình duyệt.'),
])
d.p('2.19.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In BOM List / In', 'Click', 'After:\n– Nạp chi tiết BOM; lỗi → “Không tải được dữ liệu in BOM List”; mở popup cấu hình.'),
    ('Bấm Xem trước', 'Click', 'Before:\n– Chưa chọn cột → báo lỗi, dừng.\nAfter:\n– Mở bản xem trước theo cột đã chọn.'),
    ('Bấm In (bản xem trước)', 'Click', 'After:\n– Mở hộp thoại in.'),
])

# ------------------------------------------------------------------ 2.20 Lịch sử
d.h3('2.20 Xem lịch sử BOM')
d.p('2.20.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='history')
d.intro_table(
    ten='Xem lịch sử BOM',
    mota='Xem các lần tạo, sửa, gửi duyệt, duyệt, không duyệt, import của một BOM: popup “Lịch sử BOM List” ở danh '
         'sách và khối “Lịch sử” ở cuối màn chi tiết.',
    tacnhan=TN_XEM,
    dieukien='Người dùng xem được BOM.',
    chinh='1. Người dùng bấm “Lịch sử” ở cột Hành động (hoặc mở khối Lịch sử ở màn chi tiết).\n'
          '2. Hệ thống hiển thị dòng thời gian, mới nhất ở trên: nhóm hành động (màu riêng), người thực hiện, nội dung, '
          'thời điểm.\n'
          '3. Với lần Chỉnh sửa: liệt kê trường đổi “Nhãn: cũ → mới” và hàng hoá Thêm / Xoá / Sửa.',
    phu='• Chưa có lịch sử → “Chưa có lịch sử”.\n'
        '• Lỗi → “Không tải được lịch sử”.\n'
        '• Khối Lịch sử ở màn chi tiết mặc định thu gọn, chỉ tải khi mở; có nút Làm mới, Thu gọn, Bộ lọc.')
d.p('2.20.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử', shot=shot('22-lich-su.png'), shot_caption='Popup Lịch sử BOM List')
d.figure(shot('24-lich-su-phieu.png'), 'Khối Lịch sử ở cuối màn chi tiết', width_in=6.2)
d.p('2.20.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Lịch sử BOM List', '–'),
    ('Nhóm hành động', 'Label', 'Read-only', '8 giá trị', 'Theo dữ liệu',
     'Tạo mới · Chỉnh sửa · Xoá · Hoàn thành · Gửi duyệt · Duyệt · Không duyệt · Import sản phẩm.'),
    ('Người thực hiện — nội dung', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Không có người → “Hệ thống”.'),
    ('Trường thay đổi', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     '“Nhãn: cũ → mới”, giá trị rỗng hiện “(trống)”; theo dõi Tên, Ghi chú, Dự án, Giải pháp, Hạng mục, Khách hàng, '
     'Tiền tệ, Loại BOM.'),
    ('Hàng hoá thay đổi', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Thêm (xanh) · Xoá (đỏ) · Sửa (chi tiết từng hàng).'),
    ('Thời điểm', 'Text', 'Read-only', 'DD/MM/YYYY HH:mm', 'Theo dữ liệu', '–'),
    ('Trạng thái rỗng / đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử” / “Đang tải...”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–'),
], required=False)
d.p('2.20.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lịch sử', 'Click', 'After:\n– Tải lịch sử của BOM, hiển thị mới nhất ở trên; lỗi → “Không tải được lịch sử”.'),
    ('Mở khối Lịch sử ở màn chi tiết', 'Click', 'After:\n– Tải lần đầu khi mở; Làm mới để tải lại.'),
])

# ------------------------------------------------------------------ 2.21 Trạng thái duyệt
d.h3('2.21 Theo dõi trạng thái duyệt BOM')
d.p('2.21.1 Biểu đồ Usecase')
d.uc_figure('FR-21', 'Theo dõi trạng thái duyệt BOM', 'action', actor=A_XEM)
d.p('2.21.2 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của màn BOM giải pháp.', anchor='list')
d.intro_table(
    ten='Theo dõi trạng thái duyệt BOM',
    mota='Màn BOM giải pháp KHÔNG có nút gửi duyệt / duyệt. BOM tổng hợp đi theo hồ sơ trình duyệt của hạng mục / giải '
         'pháp; trạng thái BOM tự cập nhật theo hồ sơ và hiển thị ở cột Trạng thái, màn chi tiết, lịch sử.',
    tacnhan=TN_XEM,
    dieukien='Có BOM tổng hợp ở trạng thái Hoàn thành gắn vào hồ sơ trình duyệt hạng mục / giải pháp (thao tác ở màn '
             'Hạng mục giải pháp / Quản lý giải pháp — tài liệu riêng).',
    chinh='1. Hồ sơ trình duyệt được gửi → BOM tổng hợp kèm hồ sơ chuyển “Chờ duyệt”, lịch sử ghi “Gửi duyệt — Gửi duyệt BOM List”.\n'
          '2. Hồ sơ được duyệt → BOM chuyển “Đã duyệt”, lịch sử ghi “Duyệt — BOM List đã được duyệt”; hệ thống gửi thông '
          'báo “BOM <Mã - Tên> đã được duyệt” (bấm mở màn chi tiết BOM) tới người gửi hồ sơ, PM giải pháp, người lập BOM '
          'và nhân viên kinh doanh phụ trách dự án.\n'
          '3. Hồ sơ bị từ chối → BOM chuyển “Không duyệt”, lịch sử ghi “Không duyệt — BOM List không được duyệt”.',
    phu='• BOM thành phần không đi luồng duyệt: chuyển “Đã được tổng hợp” khi được chọn làm con của BOM tổng hợp và '
        'quay về “Hoàn thành” khi bị bỏ ra / BOM tổng hợp bị xoá.\n'
        '• BOM “Chờ duyệt”, “Đã duyệt”, “Đã được tổng hợp” không sửa, không xoá được; vẫn Xem, In, Xuất Excel, Sao chép, '
        'Lịch sử.\n'
        '• BOM “Không duyệt”: nút Sửa hiện cho người tạo nhưng màn Cập nhật hiện từ chối mở (xem FR-15).')
d.p('2.21.3 Layout màn hình')
d.layout(menu=MENU, shot=shot('01b-ds-phai.png'),
         shot_caption='Cột Trạng thái và các nút thao tác theo trạng thái trên danh sách')
d.p('2.21.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Badge Đang tạo', 'Badge', 'Read-only', 'Màu xám', 'BOM lưu nháp; chỉ người tạo thấy.'),
    ('Badge Hoàn thành', 'Badge', 'Read-only', 'Màu xanh lá', 'BOM đã lưu đầy đủ; được gộp / gửi kèm hồ sơ.'),
    ('Badge Chờ duyệt', 'Badge', 'Read-only', 'Màu cam', 'BOM tổng hợp trong hồ sơ đang chờ duyệt.'),
    ('Badge Đã duyệt', 'Badge', 'Read-only', 'Màu xanh lá', 'BOM tổng hợp đã duyệt; dùng làm căn cứ báo giá.'),
    ('Badge Đã được tổng hợp', 'Badge', 'Read-only', 'Màu xám đậm', 'BOM thành phần đã gộp vào BOM tổng hợp.'),
    ('Badge Không duyệt', 'Badge', 'Read-only', 'Màu đỏ', 'BOM tổng hợp bị từ chối cùng hồ sơ.'),
], required=False, scope=False)
d.p('2.21.5 Danh sách event và xử lý event')
d.event_table([
    ('Hồ sơ trình duyệt đổi trạng thái', 'System',
     'After:\n– Cập nhật trạng thái các BOM tổng hợp kèm hồ sơ: chờ duyệt → Chờ duyệt; duyệt → Đã duyệt; từ chối → Không duyệt.\n'
     '– Ghi 1 dòng lịch sử tương ứng cho từng BOM.\n– Khi duyệt: gửi thông báo tới 4 đối tượng như Dòng sự kiện chính.'),
    ('BOM tổng hợp lưu / sửa / xoá danh sách BOM con', 'System',
     'After:\n– BOM thành phần được thêm → Đã được tổng hợp; bị bỏ ra hoặc BOM tổng hợp bị xoá → Hoàn thành.'),
])

# ==================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn BOM giải pháp; không lặp lại các quy tắc đã có trong SRS '
           'quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi nhìn thấy BOM', [
        '– Theo quyền V1–V4 tính trên người tạo BOM; không có quyền phạm vi → chỉ BOM mình tạo.',
        '– BOM “Đang tạo” chỉ người tạo nhìn thấy, ở mọi phạm vi.',
    ], ['Xem danh sách', 'Xuất Excel danh sách']),
    ('BR-02', 'Mã BOM và mã hàng tạm', [
        '– Mã BOM sinh khi lưu lần đầu: BOM-<năm>-<5 chữ số>; màn Tạo mới / Sao chép chưa hiện mã.',
        '– Hàng tạm không cần mã, hệ thống cấp mã HHB… khi lưu; hàng ERP bắt buộc có mã.',
    ], ['Tạo mới', 'Sao chép']),
    ('BR-03', 'Liên kết dự án – giải pháp – khách hàng', [
        '– Mỗi dự án TKT có 1 giải pháp: chọn dự án tự điền giải pháp và khách hàng; chỉ chọn được dự án của tôi.',
        '– Thành viên đã bị khoá khỏi giải pháp không lưu được BOM mới của giải pháp đó.',
        '– Khi lưu, BOM ghi nhận version hiện hành của giải pháp / hạng mục.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Sao chép']),
    ('BR-04', 'Lưu nháp và Lưu BOM', [
        '– Lưu nháp: trạng thái Đang tạo, chỉ bắt buộc Tên.',
        '– Lưu BOM: trạng thái Hoàn thành, bắt buộc Tên, Dự án, Giải pháp, Khách hàng.',
        '– Nút Lưu nháp chỉ có khi tạo mới hoặc BOM đang “Đang tạo”. Thao tác xong quay về danh sách.',
        '– BOM không quản lý giá; giá xử lý ở Báo giá.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-05', 'Điều kiện hiện nút theo trạng thái', [
        '– Sửa: người tạo + BOM Đang tạo / Hoàn thành / Không duyệt (màn Cập nhật hiện chỉ mở với Đang tạo / Hoàn thành).',
        '– Xóa: Q1 + người tạo + BOM Đang tạo.',
        '– Sao chép: Q1, mọi trạng thái. In, Xuất Excel, Lịch sử, Xem: luôn hiện.',
        '– Chờ duyệt / Đã duyệt / Đã được tổng hợp: chỉ còn Xem, In, Xuất Excel, Sao chép, Lịch sử.',
    ], ['Xem danh sách', 'Xem chi tiết']),
    ('BR-06', 'Loại BOM theo cấp', [
        '– Giải pháp có hạng mục: BOM không chọn hạng mục (cấp giải pháp) bắt buộc là Tổng hợp.',
        '– Mỗi giải pháp / hạng mục chỉ có 1 BOM tổng hợp trên cùng 1 version.',
        '– Đổi loại BOM khi lưới có dữ liệu thì xoá toàn bộ lưới (có xác nhận).',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-07', 'BOM con được phép chọn để gộp', [
        '– Cùng dự án, cùng giải pháp, khác chính BOM đang sửa.',
        '– Tổng hợp cấp hạng mục: BOM thành phần cùng hạng mục, cùng version hạng mục, không phải Đang tạo.',
        '– Tổng hợp cấp giải pháp (giải pháp có hạng mục): BOM tổng hợp cấp hạng mục ở trạng thái Đã duyệt, cùng version giải pháp.',
        '– Tổng hợp cấp giải pháp (không có hạng mục): BOM thành phần không phải Đang tạo, cùng version giải pháp.',
        '– BOM con chưa gắn version vẫn được liệt kê (dữ liệu cũ). Các BOM con phải cùng tiền tệ và cùng cấu trúc nhóm.',
    ], 'Tạo mới BOM tổng hợp'),
    ('BR-08', 'Đồng bộ trạng thái BOM con', [
        '– BOM thành phần được chọn làm con → Đã được tổng hợp; bị bỏ ra hoặc BOM tổng hợp bị xoá → Hoàn thành.',
        '– Sao chép không kế thừa BOM con nên không làm đổi trạng thái BOM nào.',
    ], ['Tạo mới BOM tổng hợp', 'Chỉnh sửa', 'Xóa']),
    ('BR-09', 'Trạng thái duyệt theo hồ sơ trình duyệt', [
        '– Chỉ BOM tổng hợp đi theo hồ sơ: gửi → Chờ duyệt; duyệt → Đã duyệt; từ chối → Không duyệt; mỗi lần ghi 1 dòng lịch sử.',
        '– Duyệt xong gửi thông báo tới người gửi hồ sơ, PM giải pháp, người lập BOM, NV kinh doanh dự án.',
    ], 'Theo dõi trạng thái duyệt'),
    ('BR-10', 'Hàng hoá trong lưới', [
        '– Hàng con không trùng mã hàng cha; mã hàng cha không trùng nhau; mã hàng con không trùng trong cùng dòng cha.',
        '– Hàng ERP làm con của hàng tạm cần quyền Q2. Hàng ERP chỉ sửa được số lượng.',
        '– Nhân bản chỉ áp cho hàng tạm không có hàng con, dòng mới dùng chung mã.',
        '– Nhóm hàng tối đa 2 cấp; xoá nhóm thì hàng chuyển về nhóm Cấp 1 đầu tiên.',
    ], ['Thêm hàng hoá', 'Thêm hàng tạm', 'Thao tác trên lưới', 'Quản lý nhóm hàng']),
    ('BR-11', 'Import không tự lưu', [
        '– Chỉ import vào BOM đã lưu; dữ liệu import chỉ áp vào lưới, ghi xuống khi bấm Lưu BOM.',
        '– Import từng phần cập nhật theo Line ID; Thay thế hoàn toàn xoá lưới rồi nạp lại; file của BOM khác được sao chép thành dòng mới.',
    ], 'Import hàng hoá từ Excel'),
    ('BR-12', 'Xóa BOM', [
        '– Xoá hẳn BOM cùng hàng hoá, liên kết BOM con và lịch sử của BOM; chỉ áp cho BOM Đang tạo của chính người tạo.',
    ], 'Xóa BOM'),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')
