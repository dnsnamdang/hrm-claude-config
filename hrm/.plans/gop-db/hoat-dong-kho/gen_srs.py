# -*- coding: utf-8 -*-
"""SRS màn "Hoạt động kho" (phân hệ Kho, mục cấp 1) — form chuẩn + quy định màn theo dõi / báo cáo (bảng Cách lấy dữ liệu, bảng vị trí
bấm được) + chuẩn 04/11 (Mục lục trang riêng căn giữa, Phần 5 bảng 4 cột).

Chạy: python gen_srs.py  → SRS - Hoạt động kho.docx
Khuôn chép: ../list-bill-accounting/gen_srs.py (màn chỉ xem dạng danh sách: tìm nhanh + Cấu hình cột + Xuất Excel, cùng bộ component) +
  ../tong-hop-xuat-nhap-ton/gen_srs.py (09/11, báo cáo kho: bảng Cách lấy dữ liệu, bảng vị trí bấm được, Phần 5 4 cột).
Nguồn đọc 10/11/2026 (nhánh develop — con của gop_db — cả 2 repo):
  FE  pages/warehouse/activities/index.vue, components/warehouse/activity/{ActivitySummary.vue, activity-table.js, export-excel.js},
      components/{V2BaseSmartFilterPanel, V2BaseDataTable}.vue, components/modal/{export-fields-modal, column-customization-modal}.vue,
      components/report/ReportInfoTip.vue, utils/mixins/{filterStateMixin, DedupeLoadMixin}.js, utils/export/excel-signature-block.js,
      components/subsystem-menu/warehouse.js (mục cấp 1 “Hoạt động kho”, không có nhóm con).
  BE  Modules/Finance/{Services/WarehouseActivityService.php, Http/Controllers/V1/WarehouseActivityController.php, Routes/api.php
      (GET /warehouse-activities, KHÔNG checkPermission)}; nguồn mốc thời gian: Assign/Services/WarehouseExportService.php (duyệt ĐNXK +
      gửi phiếu xuất kho), Finance/Services/WarehouseImportWriteService.php (duyệt ĐNNK + gửi phiếu nhập kho), WarehouseTransferService.php;
      ERP Model/Warehouse/WarehouseExportRequest::send()/approve(), Employee::getStockerWarehouseIdsAttribute.
  Tài liệu: design.md, plan.md, spec docs/superpowers/specs/gop-db/2026-10-26-hoat-dong-kho-design.md (đoạn tô màu dòng đã bị bỏ 29/10 — #11901).
Ảnh: ./hdk_shots — dev-hrm 10/11/2026, DNS Admin (_capture/capture.js, chặn mọi yêu cầu ghi: 0 lọt). DNS Admin trên dev không là thủ kho
  kho nào nên màn thật RỖNG (ảnh 01b_empty). Các ảnh có dữ liệu: trên TRÌNH DUYỆT thay kết quả danh sách bằng dữ liệu THẬT của kho PTT lấy
  từ màn “Theo dõi theo kho” (cùng hàm dựng dữ liệu, giữ tham số tìm / sắp xếp) = mô phỏng thủ kho kho PTT. Dev không có phiếu “Đã hoàn
  thành” trong ngày → không có ảnh dòng xanh.
Đối soát dev 10/11 (_capture/doisoat.js, chỉ GET): kho PTT 54 dòng = 39 Phiếu đề nghị xuất kho + 15 Phiếu đề nghị nhập kho = đúng tập mã ở
  2 màn danh sách lọc kho PTT, trạng thái Chờ duyệt + Đang xuất / nhập kho; ô tổng hợp 54 / 0 / 54 khớp; MT 5 = 1 + 4; KTCN 2 = 2 + 0.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HRM = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HRM, '.claude', 'skills', 'srs-documenter', 'assets'))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from srs_docx_lib import SrsDoc  # noqa: E402
from srs_split_rows import split_ui_rows  # noqa: E402

TEN = 'Hoạt động kho'
SHOTS = os.path.join(HERE, 'hdk_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Hoạt động kho'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Hoạt động kho.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
EMPTY = '“Không có dữ liệu phù hợp”'
LOADERR = '“Lỗi khi tải dữ liệu”'
XLS_OK = '“Xuất Excel thành công.”'
XLS_ERR = '“Lỗi khi xuất Excel”'
FILE = 'hoat_dong_kho.xlsx'
DNXK = 'Phiếu đề nghị xuất kho'
DNNK = 'Phiếu đề nghị nhập kho'
TIP_KHOI = ('HOẠT ĐỘNG KHO • Phiếu đề nghị xuất kho và đề nghị nhập kho của các kho bạn là thủ kho • Gồm phiếu đang xử lý và phiếu '
            'nhận trong hôm nay (kể cả đã hoàn thành) • Danh sách tự tải lại mỗi 60 giây')
TIP_TONG = 'Tổng số phiếu nhận • Số phiếu đề nghị xuất kho + đề nghị nhập kho đang hiện ở danh sách bên dưới'
TIP_HT = 'Tổng hoàn thành • Số phiếu đã hoàn thành (đã có Thời gian hoàn thành)'
TIP_CXL = ('Tổng chưa xử lý • Tổng số phiếu nhận trừ Tổng hoàn thành • Gồm phiếu "Đã nhận đề nghị" và phiếu đang lấy hàng / xếp hàng')
TIP_TITLE = ('Theo dõi phiếu đề nghị xuất kho / nhập kho của các kho bạn là thủ kho: phiếu đang xử lý và phiếu nhận trong hôm nay. '
             'Phiếu chưa hoàn thành xếp trên, phiếu đã hoàn thành xếp dưới cùng.')
FIELDS = ('Phiếu đề nghị, Loại, Người yêu cầu, Hình thức vận chuyển, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành, '
          'Trạng thái, Tổng thời gian xử lý')

A = 'Thủ kho'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã đăng nhập (màn KHÔNG gắn quyền, giữ như hệ thống ERP); dữ liệu chỉ '
      'gồm phiếu của các kho người dùng là Thủ kho (Phần 2).')
DK = ('1. Người dùng đăng nhập thành công.\n'
      '2. Người dùng là Thủ kho của ít nhất 1 kho (khai ở danh mục Kho vật lý); không là thủ kho kho nào thì danh sách rỗng.\n'
      '3. Người dùng đang ở màn Hoạt động kho, danh sách đã nạp xong.')

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/activities', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Hoạt động kho': 'menu_muc',
    'Cấu hình cột': 'btn_cauhinhcot', 'Xuất Excel': 'btn_xuatexcel', 'Phiếu đề nghị': 'link_maphieu',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None, extra=None):
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event. Trả số mục con kế tiếp."""
    d.h3('2.%d %s' % (no, title))
    k = 1
    if usecase:
        d.p('2.%d.%d Biểu đồ Usecase' % (no, k))
        uc(*usecase)
        k += 1
    d.p('2.%d.%d Giới thiệu' % (no, k))
    tail, anchor = rule
    d.rule_ref(tail + ' ' + RIENG, anchor=anchor)
    d.intro_table(**intro)
    k += 1
    d.p('2.%d.%d Layout màn hình' % (no, k))
    d.layout(**layout)
    for img, cap in (extra or []):
        d.figure(img, cap, width_in=6.2)
    k += 1
    assert ui and ev, 'Thiếu bảng giao diện / event ở 2.%d' % no
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (no, k))
    d.ui_table(split_ui_rows(ui, UI_OVER, UI_EXPLICIT), **(ui_kw or {}))
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (no, k))
    d.event_table(ev)
    return k + 1


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.doc.add_page_break()  # Mục lục sang trang riêng như bản Drive đã chuẩn hoá
d.h2('Mục lục')
d.doc.paragraphs[-1].alignment = 1  # căn giữa chữ 'Mục lục'
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Hoạt động kho thuộc phân hệ Kho (chuyển từ hệ thống ERP: Kho › Hoạt động kho), '
    'nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu bảng THEO DÕI việc của thủ kho: các %s và %s của những kho người dùng là Thủ kho, đang chờ xử lý / đang lấy '
    'hàng, xếp hàng, cùng các phiếu nhận trong hôm nay (kể cả đã hoàn thành).' % (DNXK, DNNK),
    'Ghi rõ điều kiện một phiếu xuất hiện trên bảng, cách xác định Trạng thái, cách tính Tổng thời gian xử lý và 3 ô tổng hợp (Tổng số '
    'phiếu nhận, Tổng hoàn thành, Tổng chưa xử lý) để người nghiệm thu đối soát được với màn danh sách %s / %s.' % (DNXK, DNNK),
    'Ghi rõ các điểm khác hệ thống ERP có chủ đích: tự tải lại mỗi 60 giây thay cho cập nhật tức thời (ERP đã hỏng), khôi phục khối tổng '
    'hợp, thêm ô tìm nhanh mã phiếu, Cấu hình cột, Xuất Excel; mã phiếu mở màn chi tiết ở tab mới.',
])
d.p('Phạm vi chức năng (5 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Xem danh sách hoạt động kho (khối tổng hợp “Phiếu nhận” + bảng 11 cột, sắp xếp theo 5 cột, tự tải lại 60 giây); Tìm kiếm theo mã '
    'phiếu đề nghị; Mở phiếu đề nghị (bấm mã phiếu → màn chi tiết ở tab mới); Tùy chỉnh cột; Xuất Excel.',
    'Không thuộc màn này: màn CHỈ ĐỌC — không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Duyệt / Không duyệt, Import Excel, In, Lịch '
    'sử thay đổi, không phân trang, không có ô lọc nâng cao (không có nút Tìm kiếm nâng cao / Cài đặt bộ lọc). Mọi thao tác trên phiếu '
    '(duyệt, lập phiếu xuất / nhập kho, hủy) làm ở màn của phiếu (Phần 5).',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Thủ kho mở màn đầu ca và để mở trong ngày để biết phiếu nào vừa được gửi tới kho mình (Đã nhận đề nghị), phiếu nào đang lấy / xếp '
    'hàng, phiếu nào đã xong và mất bao lâu; bấm mã phiếu để vào xử lý ở màn phiếu.',
    'Trưởng kho dùng 3 ô tổng hợp và cột Tổng thời gian xử lý để nắm khối lượng việc và tốc độ xử lý trong ngày; xuất Excel để báo cáo.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Màn không gắn quyền; phạm vi dữ liệu = các kho người dùng là Thủ kho (BR-01). Theo quyết định 26/10/2026 Super Admin xem mọi kho; '
    'bản hiện hành (từ 31/10/2026) CHƯA đặc cách Super Admin — xem ghi chú Phần 2.',
    'Phiếu hiện trên bảng khi đang ở trạng thái Chờ duyệt hoặc Đang xuất kho / Đang nhập kho, HOẶC có Thời gian nhận từ 00:00 hôm nay mà '
    'không phải Đang tạo / Đã hủy (BR-02).',
    'Trạng thái trên bảng suy ra từ 3 mốc thời gian, không phải trạng thái của phiếu (BR-03); phiếu chưa hoàn thành luôn xếp trên phiếu '
    'đã hoàn thành (BR-05).',
    'Màn không ghi dữ liệu nào; xem / tìm / xuất không ghi lịch sử (BR-09).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    (DNXK + ' (ĐNXK)', 'Phiếu yêu cầu thủ kho xuất hàng khỏi kho, lập từ Yêu cầu xuất hàng; mã dạng PDNXK-xxxxx.'),
    (DNNK + ' (ĐNNK)', 'Phiếu yêu cầu thủ kho nhận hàng vào kho, lập từ Yêu cầu nhập hàng; mã dạng PDNNK-xxxxx.'),
    ('Thủ kho', 'Nhân viên được gán vào ô Thủ kho của một kho ở danh mục Kho vật lý. Một kho có thể có nhiều thủ kho; một người có thể là '
                'thủ kho nhiều kho.'),
    ('Thời gian nhận', 'Lúc phiếu đề nghị được gửi tới thủ kho (gửi thủ kho).'),
    ('Thời gian lấy/xếp hàng', 'Lúc thủ kho bắt đầu xử lý phiếu: lập Phiếu xuất kho (ĐNXK) / Phiếu nhập kho (ĐNNK) hoặc phiếu điều chuyển '
                               'kho — phiếu đề nghị chuyển sang Đang xuất kho / Đang nhập kho.'),
    ('Thời gian hoàn thành', 'Lúc hàng thực sự rời / vào kho (gửi Phiếu xuất kho / Phiếu nhập kho) — phiếu đề nghị chuyển sang Đã xuất kho '
                             '/ Đã nhập kho.'),
    ('Trạng thái trên bảng', '3 giá trị: “Đã nhận đề nghị” (chưa có Thời gian lấy/xếp hàng, nhãn cam) · “Đang lấy hàng” (ĐNXK) / “Đang xếp '
                             'hàng” (ĐNNK) (đã có Thời gian lấy/xếp hàng, nhãn xanh dương) · “Đã hoàn thành” (đã có Thời gian hoàn '
                             'thành, nhãn xanh lá).'),
    ('Trạng thái phiếu', 'Trạng thái lưu trên phiếu đề nghị: Đang tạo, Chờ duyệt, Đang xuất / nhập kho, Đã xuất / nhập kho, Đang hạch '
                         'toán, Đã hạch toán, Đã hủy — dùng để quyết định phiếu có lên bảng không (BR-02).'),
    ('Tổng thời gian xử lý', 'Khoảng từ Thời gian nhận tới Thời gian hoàn thành, dạng “x ngày y giờ z phút”; dưới 1 phút ghi “Vài giây”.'),
    ('Cấu trúc phân cấp', 'Không có: bảng phẳng, mỗi phiếu đề nghị 1 dòng (ĐNXK và ĐNNK trộn chung).'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn KHÔNG gắn quyền riêng và máy chủ không kiểm quyền (giữ như hệ thống ERP — user chốt 26/10/2026): mục menu luôn hiện, ai đăng nhập '
    'cũng mở được màn và dùng mọi chức năng. Dữ liệu được giới hạn theo kho người dùng là Thủ kho.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', 'Không có quyền riêng (mọi người dùng đã đăng nhập)', 'Thấy menu và màn; dùng được Tìm kiếm, Làm mới, sắp xếp, Thu gọn khối '
                                                               'tổng hợp, bấm mã phiếu, Xuất Excel, Cấu hình cột.'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('P1', 'Thủ kho của kho (khai ở danh mục Kho vật lý)', 'Phiếu đề nghị xuất kho / nhập kho của MỌI kho người dùng là thủ kho (mọi công '
                                                          'ty), theo điều kiện BR-02.'),
    ('P2', 'Không là thủ kho kho nào', 'Danh sách rỗng, 3 ô tổng hợp = 0, bảng hiện ' + EMPTY + '.'),
    ('P3', 'Super Admin', 'Theo quyết định 26/10/2026 (y ERP): mọi kho. Bản hiện hành KHÔNG đặc cách — Super Admin như P1 / P2 theo kho '
                          'mình là thủ kho (đo trên dev 10/11/2026: DNS Admin thấy 0 phiếu); đã báo để xử lý.'),
], widths=[0.8, 2.2, 3.0])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'P1 Thủ kho', 'P2 Không là thủ kho', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách hoạt động kho', '✅ kho mình', '✅ (rỗng)', '✅ (màn không gắn quyền)'),
    ('FR-02 Tìm kiếm theo mã phiếu', '✅', '✅ (rỗng)', '✅'),
    ('FR-03 Mở phiếu đề nghị', '✅ (màn phiếu áp quyền xem của nó)', '— (không có dòng)', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '✅'),
    ('FR-05 Xuất Excel', '✅ kho mình', '✅ (file không có dòng)', '✅'),
], widths=[2.2, 1.4, 1.3, 1.1])
d.p('Màn không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel, In, Lịch sử thay đổi, Duyệt nên ma trận không có các dòng đó.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Màn không có quyền riêng nên không có trường hợp “thiếu quyền”; người không là thủ kho kho nào vẫn mở được màn nhưng bảng rỗng.',
    'Bấm mã phiếu: màn chi tiết phiếu (tab mới) tự áp quyền xem của nó — thiếu quyền xem phiếu thì màn đó báo theo quy tắc của nó.',
    'Chưa đăng nhập / phiên hết hạn → chuyển về màn đăng nhập (quy tắc chung); lượt tự tải lại 60 giây không hiện thông báo lỗi.',
    'Bị gỡ khỏi ô Thủ kho của một kho khi đang mở màn: tới lượt tải lại kế tiếp (≤ 60 giây) phiếu của kho đó biến mất.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Xuất Excel, Cấu hình cột', 'Luôn hiện', 'Xuất Excel bị khóa trong lúc đang xuất'),
    ('Ô tìm nhanh, Tìm kiếm, Làm mới', 'Luôn hiện trên một hàng', 'Bộ lọc gọn: không có Tìm kiếm nâng cao, Cài đặt bộ lọc'),
    ('Khối tổng hợp “Phiếu nhận”', 'Hiện sau lần nạp thành công đầu tiên', 'Có nút Thu gọn / Mở rộng'),
    ('Mã phiếu (link)', 'Mọi dòng', 'Mở màn chi tiết phiếu ở tab mới'),
    ('Nút Thêm mới, Import, In, cột Hành động, phân trang', 'Không có', 'Màn chỉ đọc (như ERP)'),
], widths=[2.2, 2.3, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A, [0, 1])],
    [('FR-01', 'Xem danh sách hoạt động kho', 'view'),
     ('FR-05', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm theo mã phiếu', 'view', 'extend', [0], None),
     ('FR-03', 'Mở phiếu đề nghị', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Hoạt động kho')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
k = fr(1, 'Xem danh sách hoạt động kho',
       rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng và Cấu hình cột.', 'list'),
       intro=dict(
           ten='Truy cập và xem danh sách hoạt động kho',
           mota='Hiển thị trong một bảng (không phân trang) mọi %s và %s của các kho người dùng là Thủ kho, gồm phiếu đang xử lý và phiếu '
                'nhận trong hôm nay, kèm khối tổng hợp “Phiếu nhận” (Tổng số phiếu nhận, Tổng hoàn thành, Tổng chưa xử lý). Bảng tự tải '
                'lại mỗi 60 giây để thủ kho thấy phiếu mới mà không phải bấm. Màn chỉ đọc.' % (DNXK, DNNK),
           tacnhan=TN,
           dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng vào màn từ menu phân hệ Kho.',
           chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
                 '2. Hệ thống nạp cấu hình cột đã lưu của người dùng; có từ khóa tìm kiếm ghi tạm dưới 10 phút (tải lại trang) thì khôi '
                 'phục vào ô tìm nhanh.\n'
                 '3. Hệ thống xác định các kho người dùng là Thủ kho, lấy %s + %s của các kho đó theo điều kiện BR-02.\n'
                 '4. Hệ thống xếp phiếu chưa hoàn thành lên trước, trong mỗi nhóm theo Thời gian nhận mới nhất trước (BR-05).\n'
                 '5. Hệ thống hiển thị khối tổng hợp “Phiếu nhận” và bảng 11 cột, mọi dòng trên một trang.\n'
                 '6. Cứ 60 giây (khi tab trình duyệt đang hiện) hệ thống tự nạp lại bảng và 3 ô tổng hợp theo đúng từ khóa và sắp xếp '
                 'đang áp, không hiện vòng tải.\n'
                 '7. Người dùng bấm tiêu đề cột có biểu tượng sắp xếp để đổi thứ tự; bấm Thu gọn để ẩn 3 ô tổng hợp.' % (DNXK, DNNK),
           phu='• Đang nạp (lần mở màn, bấm Tìm kiếm / Làm mới / sắp xếp) → trong bảng hiện vòng xoay “Đang tải dữ liệu...”.\n'
               '• Người dùng không là thủ kho kho nào, hoặc các kho không có phiếu thỏa BR-02 → bảng hiện ' + EMPTY + ', 3 ô = 0.\n'
               '• Máy chủ lỗi khi nạp (do người dùng bấm) → thông báo ' + LOADERR + ', bảng giữ dữ liệu cũ.\n'
               '• Lượt tự tải lại 60 giây bị lỗi → không báo gì, giữ dữ liệu cũ, thử lại ở lượt sau.\n'
               '• Tab trình duyệt đang ẩn (người dùng mở tab khác) → bỏ lượt tự tải lại; quay lại tab thì lượt kế tiếp nạp như thường.\n'
               '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
               '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo hết phiên, chuyển về màn đăng nhập.',
           dacbiet='Không phân trang (bảng theo dõi trong ngày, ERP cũng đổ hết). Cột mặc định hiện: đủ 11 cột; cột khóa (không ẩn, không '
                   'đổi vị trí): STT, Phiếu đề nghị. Sắp xếp được 5 cột: Phiếu đề nghị, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời '
                   'gian hoàn thành. Sắp xếp không được ghi nhớ khi tải lại trang. Khác ERP có chủ đích: ERP cập nhật tức thời nhưng đã '
                   'hỏng → HRM tự tải lại 60 giây; HRM bỏ tô màu dòng theo thời gian chờ (user chốt 29/10/2026, #11901).'),
       layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn Hoạt động kho (dữ liệu kho PTT trên dev)'),
       extra=[(shot('00_menu'), 'Vị trí mục menu: phân hệ Kho › Hoạt động kho (mục cấp 1)'),
              (shot('01e_tip'), 'Icon ⓘ của khối Phiếu nhận'),
              (shot('01b_empty'), 'Người dùng không là thủ kho kho nào: danh sách rỗng'),
              (shot('03_sort'), 'Sắp xếp theo cột Phiếu đề nghị (giảm dần)')],
       ui_kw=dict(required=False),
       ui=[
           ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
            ['- “Hoạt động kho” trên thanh tiêu đề trang, tiêu đề bảng và tab trình duyệt',
             '- Icon ⓘ: “' + TIP_TITLE + '” (cạnh tiêu đề trang)']),
           ('Khối Bộ lọc danh sách', 'Label', 'Hiển thị', '–', 'Hiển thị',
            ['- Ô tìm nhanh, nút Tìm kiếm, Làm mới trên một hàng', '- Chi tiết ở mục 2.2']),
           ('Khối tổng hợp “Phiếu nhận”', 'Label', 'Hiển thị', '–', 'Hiển thị',
            ['- Tiêu đề “PHIẾU NHẬN” kèm icon ⓘ: “' + TIP_KHOI + '”',
             '- Gồm 3 ô số, đơn vị “phiếu”; số KHÔNG bấm được', '- Chỉ hiện sau khi nạp dữ liệu thành công']),
           ('Ô Tổng số phiếu nhận', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- = số dòng đang hiện trong bảng', '- Icon ⓘ: “' + TIP_TONG + '”']),
           ('Ô Tổng hoàn thành', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- = số dòng có Trạng thái “Đã hoàn thành”', '- Icon ⓘ: “' + TIP_HT + '”']),
           ('Ô Tổng chưa xử lý', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- = Tổng số phiếu nhận − Tổng hoàn thành', '- Icon ⓘ: “' + TIP_CXL + '”']),
           ('Nút Thu gọn', 'Button', 'Enable', '–', 'Hiển thị',
            ['- Góc phải khối tổng hợp', '- Bấm → ẩn 3 ô, chữ đổi thành “Mở rộng”; bấm lại → hiện lại',
             '- Không ghi nhớ: tải lại trang thì khối mở']),
           ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
            ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.5)',
             '- Khóa trong lúc đang xuất']),
           ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
            ['- Biểu tượng cột, rê chuột: “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4)']),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số 1, 2, 3… theo thứ tự đang hiện', '- Cột khóa']),
           ('Cột Phiếu đề nghị', 'Link', 'Enable', '–', 'Hiển thị',
            ['- Mã phiếu: PDNXK-… (đề nghị xuất kho) hoặc PDNNK-… (đề nghị nhập kho), chữ xanh gạch chân',
             '- Bấm → mở màn chi tiết phiếu ở TAB MỚI (mục 2.3)', '- Sắp xếp được theo mã (chữ cái); cột khóa']),
           ('Cột Loại', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- Loại phiếu đề nghị theo tên hệ thống ERP, vd “Xuất mượn”, “Xuất bán (HĐH)”, “Xuất điều chuyển kho chi nhánh”, “Nhập hàng '
             'mượn trả lại”, “Nhập điều chuyển kho nội bộ”', '- Xuống dòng khi dài; không sắp xếp']),
           ('Cột Người yêu cầu', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- Họ tên người lập Yêu cầu xuất hàng / Yêu cầu nhập hàng gốc của phiếu (không phải người lập phiếu đề nghị)',
             '- Phiếu không có yêu cầu gốc (vd ghép / tách) → trống']),
           ('Cột Hình thức vận chuyển', 'Table/Grid', 'Read-only', '3 giá trị', 'Hiển thị',
            ['- Chỉ phiếu đề nghị xuất kho: Tự vận chuyển, Công ty vận chuyển, Khách hàng vận chuyển (lấy từ Yêu cầu xuất hàng)',
             '- Phiếu đề nghị nhập kho: luôn trống']),
           ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- “Mã kho - Tên kho”, vd “PTT - Phan Trọng Tuệ”', '- Sắp xếp được (theo mã kho)']),
           ('Cột Thời gian nhận', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
            ['- Lúc phiếu được gửi tới thủ kho', '- Trống nếu phiếu chưa có mốc này', '- Sắp xếp được']),
           ('Cột Thời gian lấy/xếp hàng', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
            ['- Lúc thủ kho bắt đầu lấy hàng (ĐNXK) / xếp hàng (ĐNNK)', '- Trống khi Đã nhận đề nghị', '- Sắp xếp được']),
           ('Cột Thời gian hoàn thành', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
            ['- Lúc hàng đã xuất / nhập kho xong', '- Trống khi chưa hoàn thành', '- Sắp xếp được']),
           ('Cột Trạng thái', 'Badge', 'Read-only', '4 nhãn', 'Hiển thị',
            ['- “Đã nhận đề nghị” (cam): chưa có Thời gian lấy/xếp hàng',
             '- “Đang lấy hàng” (ĐNXK) / “Đang xếp hàng” (ĐNNK) (xanh dương): đã có Thời gian lấy/xếp hàng, chưa hoàn thành',
             '- “Đã hoàn thành” (xanh lá): đã có Thời gian hoàn thành', '- Không sắp xếp']),
           ('Cột Tổng thời gian xử lý', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- Thời gian hoàn thành − Thời gian nhận, dạng “x ngày y giờ z phút” (bỏ phần bằng 0), vd “2 giờ 15 phút”',
             '- Dưới 1 phút: “Vài giây”', '- Chưa hoàn thành hoặc thiếu Thời gian nhận: trống', '- Không sắp xếp']),
           ('Biểu tượng sắp xếp', 'Icon Button', 'Enable', '–', 'Hiển thị',
            ['- Mũi tên 2 chiều ở 5 cột sắp xếp được', '- Đang sắp tăng: mũi tên lên; giảm: mũi tên xuống']),
           ('Trạng thái đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- Trong bảng: vòng xoay + “Đang tải dữ liệu...”.'),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', ['- Trong bảng: ' + EMPTY, '- Chỉ hiện khi không có dòng nào']),
           ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
            ['- ' + LOADERR + ' khi máy chủ lỗi ở lần nạp do người dùng bấm', '- Lượt tự tải lại không báo lỗi']),
       ],
       ev=[
           ('Mở màn hình', 'System',
            'Before:\n– Không kiểm quyền (màn không gắn quyền).\n– Xác định các kho người dùng là Thủ kho.\n'
            'During:\n– Nạp cấu hình cột; khôi phục từ khóa ghi tạm (nếu còn hạn 10 phút).\n'
            '– Lấy phiếu theo BR-02, xếp theo BR-05; máy chủ lỗi → ' + LOADERR + '.\n'
            'After:\n– Hiển thị khối tổng hợp + bảng, mọi dòng trên một trang; bật bộ đếm tự tải lại 60 giây.'),
           ('Tự tải lại sau mỗi 60 giây', 'System',
            'Before:\n– Bỏ lượt nếu tab trình duyệt đang ẩn.\n– Giữ nguyên từ khóa trong ô tìm nhanh và sắp xếp đang áp.\n'
            'During:\n– Lấy lại dữ liệu, không bật vòng tải; lỗi thì bỏ qua, không báo.\n'
            'After:\n– Cập nhật bảng (phiếu mới gửi tới / phiếu đổi trạng thái / qua ngày) và 3 ô tổng hợp.'),
           ('Bấm tiêu đề cột có sắp xếp', 'Click',
            'Before:\n– Chỉ Phiếu đề nghị, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành.\n'
            'During:\n– Lần 1 tăng dần, bấm tiếp đảo chiều; cột khác đang sắp thì về tăng dần cột mới.\n'
            'After:\n– Nạp lại theo cột đã chọn, cùng giá trị thì giữ thứ tự mặc định (BR-05); từ khóa giữ nguyên.'),
           ('Bấm Thu gọn / Mở rộng', 'Click',
            'Before:\n– Khối tổng hợp đang hiện.\nAfter:\n– Ẩn / hiện 3 ô số; dữ liệu bảng không đổi, không nạp lại.'),
           ('Rê chuột vào icon ⓘ', 'Click',
            'Before:\n– Ở tiêu đề trang, tiêu đề khối Phiếu nhận, 3 ô tổng hợp.\nAfter:\n– Hiện khung giải thích (nguyên văn ở mục 2.1.5).'),
           ('Rời màn rồi quay lại / tải lại trang', 'System',
            'Before:\n– Rời sang màn khác: xóa từ khóa ghi tạm. Tải lại trang (F5) trong 10 phút: giữ từ khóa.\n'
            'After:\n– Sắp xếp về mặc định, khối tổng hợp mở; cấu hình cột vẫn giữ (lưu theo người dùng).'),
       ])

d.p('2.1.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('Bảng dưới mô tả cách hệ thống lấy từng cột, từng ô tổng hợp và nội dung icon ⓘ (nguyên văn trên giao diện). “Tập dữ liệu” là '
    'mọi %s và %s thuộc các kho người dùng là Thủ kho, thỏa điều kiện BR-02, sau khi áp từ khóa ở ô tìm nhanh.' % (DNXK, DNNK))
d.data_table([
    ('Phạm vi kho', 'Các kho có người dùng trong danh sách Thủ kho (danh mục Kho vật lý), mọi công ty. Không là thủ kho kho nào → tập '
                    'rỗng. (Super Admin: xem Phần 2.)', '(dùng chung ⓘ của khối) “…của các kho bạn là thủ kho”'),
    ('Điều kiện phiếu lên bảng', 'Trạng thái phiếu Chờ duyệt hoặc Đang xuất kho / Đang nhập kho (bất kể ngày) HOẶC Thời gian nhận từ 00:00 '
                                 'hôm nay trở đi mà trạng thái không phải Đang tạo, Đã hủy (nên phiếu xong trong ngày vẫn ở lại tới hết '
                                 'ngày). Qua 00:00 hôm sau, phiếu đã xong của hôm trước tự rời bảng ở lượt tải lại kế tiếp.',
     '(dùng chung ⓘ của khối) “Gồm phiếu đang xử lý và phiếu nhận trong hôm nay (kể cả đã hoàn thành)”'),
    ('Ô Tổng số phiếu nhận', 'Đếm số dòng của tập dữ liệu (ĐNXK + ĐNNK). Đổi theo từ khóa tìm kiếm. Bảng không phân trang nên = số dòng '
                             'đang thấy.', TIP_TONG),
    ('Ô Tổng hoàn thành', 'Đếm dòng có Thời gian hoàn thành (Trạng thái “Đã hoàn thành”).', TIP_HT),
    ('Ô Tổng chưa xử lý', 'Tổng số phiếu nhận − Tổng hoàn thành = số dòng “Đã nhận đề nghị” + “Đang lấy hàng” + “Đang xếp hàng”.', TIP_CXL),
    ('Cột Trạng thái', 'Suy ra từ mốc thời gian, theo thứ tự: có Thời gian hoàn thành → Đã hoàn thành; có Thời gian lấy/xếp hàng → Đang '
                       'lấy hàng (ĐNXK) / Đang xếp hàng (ĐNNK); còn lại → Đã nhận đề nghị.', '—'),
    ('Cột Tổng thời gian xử lý', 'Số phút giữa Thời gian nhận và Thời gian hoàn thành, đổi ra ngày (1.440 phút) / giờ / phút, bỏ phần bằng '
                                 '0; 0 phút → “Vài giây”. Thiếu một trong 2 mốc → trống.', '—'),
    ('Cột Người yêu cầu / Hình thức vận chuyển', 'Lấy từ Yêu cầu xuất hàng / Yêu cầu nhập hàng gốc của phiếu: người lập yêu cầu; hình '
                                                 'thức vận chuyển chỉ có ở yêu cầu xuất hàng.', '—'),
    ('Thứ tự dòng', 'Mặc định: phiếu chưa hoàn thành trước, phiếu đã hoàn thành sau; trong mỗi nhóm Thời gian nhận mới nhất trước (phiếu '
                    'thiếu Thời gian nhận xuống cuối nhóm), cùng giờ thì phiếu tạo sau trước. Bấm cột sắp xếp: cột đó trước, rồi thứ tự '
                    'mặc định.', '“…Phiếu chưa hoàn thành xếp trên, phiếu đã hoàn thành xếp dưới cùng.” (ⓘ tiêu đề trang)'),
    ('Ràng buộc khớp số', 'Với 1 kho: số dòng ĐNXK = số phiếu ở màn %s lọc kho đó, trạng thái Chờ duyệt + Đang xuất kho (cộng phiếu Đã '
                          'xuất kho / hạch toán nhận hôm nay); tương tự ĐNNK. Đo dev 10/11/2026 kho PTT: 54 = 39 + 15, khớp đúng từng '
                          'mã.' % DNXK, '—'),
])
k += 1
d.p('2.1.%d Danh sách popup mở từ số liệu' % k)
d.popup_table([
    ('Số ở 3 ô Tổng số phiếu nhận / Tổng hoàn thành / Tổng chưa xử lý', 'Không có popup — số không bấm được',
     'Nắm nhanh khối lượng việc của kho trong ngày', 'Đọc trực tiếp; các phiếu tương ứng chính là các dòng của bảng bên dưới'),
    ('Mã PDNXK-… ở cột Phiếu đề nghị', 'Không phải popup — mở màn chi tiết %s ở tab mới (mục 2.3)' % DNXK,
     'Vào phiếu để duyệt / lập phiếu xuất kho mà không mất bảng đang theo dõi', 'Toàn bộ thông tin + dòng hàng của phiếu'),
    ('Mã PDNNK-… ở cột Phiếu đề nghị', 'Không phải popup — mở màn chi tiết %s ở tab mới (mục 2.3)' % DNNK,
     'Vào phiếu để lập phiếu nhập kho / xếp hàng', 'Toàn bộ thông tin + dòng hàng của phiếu'),
])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm theo mã phiếu',
   rule=('- Kịch bản tìm kiếm và Bộ lọc.', 'search'),
   intro=dict(
       ten='Tìm kiếm phiếu đề nghị theo mã',
       mota='Thu hẹp bảng về các phiếu có mã chứa chuỗi đã nhập (ô tìm nhanh “Tìm theo mã phiếu đề nghị”). Bộ lọc chỉ có ô này nên bày '
            'thẳng trên một hàng cạnh nút Tìm kiếm, Làm mới; không có ô lọc nâng cao (user chốt 26/10/2026). 3 ô tổng hợp tính lại theo kết '
            'quả tìm.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập mã hoặc một phần mã (vd “39053”, “PDNNK”) vào ô tìm nhanh.\n'
             '2. Người dùng bấm Tìm kiếm hoặc nhấn Enter.\n'
             '3. Hệ thống lấy lại các phiếu trong phạm vi + điều kiện BR-02 có mã chứa chuỗi đã nhập.\n'
             '4. Hệ thống hiển thị kết quả theo thứ tự đang áp, cập nhật 3 ô tổng hợp, ghi tạm từ khóa trên trình duyệt (10 phút).\n'
             '5. Người dùng bấm Làm mới để xóa từ khóa, bỏ sắp xếp và xem lại toàn bộ.',
       phu='• Không có phiếu khớp → bảng hiện ' + EMPTY + ', 3 ô = 0.\n'
           '• Bấm × trong ô tìm nhanh → xóa chữ; bảng chỉ đổi khi bấm Tìm kiếm / Enter (hoặc ở lượt tự tải lại / khi sắp xếp).\n'
           '• Đã gõ chữ nhưng chưa bấm Tìm kiếm mà bấm sắp xếp hoặc tới lượt tự tải lại 60 giây → chữ đang gõ cũng được áp.\n'
           '• Tải lại trang trong 10 phút → giữ từ khóa và áp ngay; rời sang màn khác rồi quay lại → ô tìm trống.\n'
           '• Máy chủ lỗi → ' + LOADERR + '.',
       dacbiet='Khớp MỘT PHẦN mã phiếu (chỉ mã, không tìm theo loại / người / kho), không phân biệt hoa / thường; bỏ khoảng trắng đầu / '
               'cuối; ký tự %, _ được tìm đúng nghĩa đen; không giới hạn số ký tự.'),
   layout=dict(menu=MENU + ' => Bộ lọc danh sách', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách: tìm “39053”'),
   extra=[(shot('02b_filter_full'), 'Kết quả tìm “39053”: 1 phiếu, ô tổng hợp tính lại'),
          (shot('04_nores'), 'Không có phiếu khớp từ khóa')],
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã phiếu đề nghị”', '- Khớp một phần mã phiếu', '- Áp khi bấm Tìm kiếm / nhấn Enter',
         '- Mặc định: trống (hoặc từ khóa ghi tạm khi tải lại trang trong 10 phút)']),
       ('Nút × trong ô tìm nhanh', 'Icon Button', 'Enable', '–', '–', 'Ẩn',
        ['- Chỉ hiện khi ô có chữ', '- Bấm → xóa chữ, chưa nạp lại danh sách']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp từ khóa, nạp lại bảng và 3 ô tổng hợp.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Bấm → xóa ô tìm nhanh, bỏ sắp xếp, xóa từ khóa ghi tạm', '- Nạp lại toàn bộ theo thứ tự mặc định']),
       ('Kết quả tìm', 'Table/Grid', 'Read-only', '–', '–', 'Theo kết quả', '- Bảng chỉ còn phiếu khớp, STT đánh lại từ 1.'),
       ('Khối tổng hợp sau tìm', 'Label', 'Read-only', '≥ 0', '–', 'Theo kết quả',
        ['- 3 ô đếm trên kết quả tìm', '- Vd tìm “39053”: Tổng số phiếu nhận 1, Tổng chưa xử lý 1']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Trong bảng: ' + EMPTY),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + LOADERR + ' khi máy chủ lỗi.'),
   ],
   ev=[
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, bỏ khoảng trắng đầu / cuối; giữ sắp xếp đang áp.\n'
        'During:\n– Tìm phiếu có mã chứa chuỗi (không phân biệt hoa / thường); %, _ hiểu đúng nghĩa đen.\n– Máy chủ lỗi → ' + LOADERR +
        '.\nAfter:\n– Hiển thị kết quả, cập nhật 3 ô tổng hợp; không khớp → ' + EMPTY + '; ghi tạm từ khóa 10 phút.'),
       ('Gõ vào ô tìm nhanh (chưa bấm Tìm kiếm)', 'Change',
        'Before:\n– Chỉ đổi chữ trong ô.\nAfter:\n– Ghi tạm chữ; bảng chưa đổi cho tới khi bấm Tìm kiếm / Enter, sắp xếp hoặc lượt tự tải '
        'lại.'),
       ('Bấm × trong ô tìm nhanh', 'Click', 'Before:\n– Ô đang có chữ.\nAfter:\n– Xóa chữ, chưa nạp lại.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có từ khóa / sắp xếp đang áp.\nAfter:\n– Xóa từ khóa (cả bản ghi tạm), bỏ sắp xếp, nạp lại toàn bộ.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Mở phiếu đề nghị từ mã phiếu',
   rule=('- Màn Danh sách và Xem chi tiết.', 'list'),
   intro=dict(
       ten='Mở màn chi tiết phiếu đề nghị xuất kho / nhập kho',
       mota='Từ mã phiếu ở cột Phiếu đề nghị, mở màn chi tiết của phiếu đó (màn %s hoặc %s đã chuyển sang HRM) ở TAB MỚI, để thủ kho xử '
            'lý phiếu mà màn Hoạt động kho vẫn mở, vẫn tự tải lại. Màn Hoạt động kho không có cửa sổ xem chi tiết riêng.' % (DNXK, DNNK),
       tacnhan=TN, dieukien=DK + '\n4. Bảng có ít nhất 1 dòng.',
       chinh='1. Người dùng bấm mã phiếu (chữ xanh gạch chân) ở cột Phiếu đề nghị.\n'
             '2. Mã PDNXK-… → hệ thống mở màn chi tiết %s của phiếu đó ở tab mới; mã PDNNK-… → màn chi tiết %s.\n'
             '3. Màn chi tiết hiển thị thông tin chung + dòng hàng của phiếu, các nút thao tác theo quyền và trạng thái của màn đó.\n'
             '4. Người dùng xử lý xong, quay lại tab Hoạt động kho: trạng thái phiếu cập nhật ở lượt tự tải lại kế tiếp (≤ 60 giây) hoặc '
             'khi bấm Tìm kiếm.' % (DNXK, DNNK),
       phu='• Thiếu quyền xem phiếu ở màn chi tiết → màn đó xử lý theo quy tắc của nó (Hoạt động kho không chặn).\n'
           '• Phiếu đã bị hủy / đổi trạng thái giữa 2 lượt tải lại → màn chi tiết hiện trạng thái mới nhất; dòng rời bảng ở lượt tải lại '
           'sau.\n'
           '• Đóng tab chi tiết → tab Hoạt động kho giữ nguyên từ khóa, sắp xếp, cuộn.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Phiếu đề nghị', shot=shot('05_dnxk'),
               shot_caption='Màn chi tiết Phiếu đề nghị xuất kho mở ở tab mới từ mã phiếu'),
   extra=[(shot('05b_dnnk'), 'Màn chi tiết Phiếu đề nghị nhập kho mở ở tab mới từ mã phiếu')],
   ui_kw=dict(required=False),
   ui=[
       ('Mã phiếu ở cột Phiếu đề nghị', 'Link', 'Enable', '–', 'Hiển thị',
        ['- Chữ xanh gạch chân', '- Bấm → mở tab mới, không rời màn Hoạt động kho']),
       ('Đích của mã PDNXK-…', 'Link', 'Enable', '–', '–',
        '- Màn chi tiết %s (Kho › Xuất kho › %s).' % (DNXK, DNXK)),
       ('Đích của mã PDNNK-…', 'Link', 'Enable', '–', '–',
        '- Màn chi tiết %s (Kho › Nhập kho › %s).' % (DNNK, DNNK)),
       ('Tab Hoạt động kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Giữ nguyên từ khóa, sắp xếp', '- Tiếp tục tự tải lại khi người dùng quay lại tab']),
   ],
   ev=[
       ('Bấm mã phiếu', 'Click',
        'Before:\n– Xác định loại phiếu theo dòng (đề nghị xuất kho / nhập kho).\n'
        'During:\n– Mở màn chi tiết tương ứng ở tab mới; màn đó tự kiểm quyền xem của nó.\n'
        'After:\n– Tab Hoạt động kho giữ nguyên; không ghi dữ liệu, không ghi lịch sử.'),
       ('Quay lại tab Hoạt động kho', 'System',
        'Before:\n– Tab vừa ẩn thì các lượt tự tải lại đã bỏ qua.\nAfter:\n– Lượt kế tiếp (≤ 60 giây) nạp trạng thái mới của phiếu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng hoạt động kho',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 11 cột của bảng. Hai cột STT, Phiếu đề nghị bị khóa; cấu hình lưu riêng theo '
            'người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, từ khóa hay 3 ô tổng hợp.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị (biểu tượng cột cạnh Xuất Excel).\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 11 cột theo cấu hình đang lưu, dòng “Đang chọn 11/11 cột”.\n'
             '3. Người dùng tích / bỏ tích các cột không khóa; kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa (2 cột khóa luôn tích); chưa lưu.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.\n'
           '• Cửa sổ Xuất Excel KHÔNG theo cấu hình cột (luôn tích sẵn đủ 10 trường — mục 2.5).',
       dacbiet='Mặc định hiện đủ 11 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ sau khi tải lại trang, đăng nhập lại, đổi trình '
               'duyệt; người dùng khác không bị ảnh hưởng. Cột ẩn vẫn được tính vào 3 ô tổng hợp và lượt tự tải lại.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tuỳ chỉnh cột',
               note='Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 11 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, ' + FIELDS]),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích',
        ['- 9 cột từ Loại tới Tổng thời gian xử lý', '- Bỏ tích → cột ẩn khỏi bảng']),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Phiếu đề nghị', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa (còn 2/11).'),
       ('Dòng “Đang chọn n/11 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu (chưa lưu lần nào → đủ 11 cột).'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change', 'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/11 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng; dữ liệu, từ khóa, 3 ô tổng hợp giữ nguyên.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5 Xuất Excel
fr(5, 'Xuất Excel danh sách', usecase=('FR-05', 'Xuất Excel', 'io', A),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất Excel danh sách hoạt động kho',
       mota='Xuất các phiếu đang theo dõi (theo từ khóa và sắp xếp đang áp) ra file Excel; người dùng chọn trường và thứ tự cột. File có '
            'letterhead công ty của người xuất, tiêu đề “HOẠT ĐỘNG KHO”, bảng và khối ký. Hệ thống ERP không có chức năng này (bổ sung '
            'theo chuẩn màn danh sách HRM).',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Hoạt động kho.',
       chinh='1. Người dùng tìm / sắp xếp theo nhu cầu rồi bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” liệt kê 10 trường, tích sẵn cả 10 (“Đang chọn 10/10 trường”).\n'
             '3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy LẠI danh sách mới nhất theo từ khóa + sắp xếp đang áp và lấy letterhead công ty của người đăng nhập.\n'
             '5. Hệ thống tạo file %s (trang “Hoạt động kho”): letterhead, tiêu đề “HOẠT ĐỘNG KHO”, cột STT + các trường đã chọn đúng '
             'thứ tự, khối ký “Ngày…….Tháng…….Năm…….” / “Người lập” / “(Ký, họ tên)”.\n'
             '6. Hệ thống tải file về, đóng cửa sổ và hiển thị %s.' % (FILE, XLS_OK),
       phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Danh sách rỗng → VẪN tạo file (chỉ có tiêu đề, hàng tiêu đề cột và khối ký) và báo ' + XLS_OK + '.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ chọn trường → không xuất.\n'
           '• Lỗi khi xuất → thông báo ' + XLS_ERR + ', không tải file; không lấy được letterhead → file không có ảnh đầu trang.\n'
           '• Có phiếu mới / đổi trạng thái sau lần tải bảng gần nhất → file theo dữ liệu MỚI NHẤT lúc bấm Xuất file.',
       dacbiet='Trường tích sẵn KHÔNG theo cột đang ẩn trên bảng (luôn đủ 10). Cột Trạng thái ghi chữ (không màu). Mọi ô xuống dòng, chiều '
               'cao dòng tự giãn theo chữ (#11895). Nút Xuất Excel khóa trong lúc đang xuất. Xuất không ghi lịch sử.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 10 trường', '–', 'Đủ 10 trường',
        ['- ' + FIELDS, '- Cột STT luôn có trong file (không nằm trong danh sách)']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích',
        ['- Mặc định: tích cả 10 trường (không theo cấu hình cột)', '- Bỏ tích → trường không có trong file']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích cả 10 trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/10 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → tải file']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('File Excel', 'Table/Grid', 'Read-only', '.xlsx', '–', '–',
        ['- Tên ' + FILE + ', trang “Hoạt động kho”', '- Letterhead công ty người xuất, tiêu đề “HOẠT ĐỘNG KHO”',
         '- STT + trường đã chọn đúng thứ tự; ngày giờ dạng dd/mm/yyyy hh:mm; Trạng thái ghi chữ',
         '- Khối ký “Người lập” cuối file']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + XLS_OK, '- ' + XLS_ERR]),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không cần quyền riêng; bỏ qua nếu đang có lượt xuất chạy.\n'
        'After:\n– Mở cửa sổ chọn trường, tích sẵn đủ 10 trường.'),
       ('Tích / bỏ tích, kéo thả trường', 'Change',
        'Before:\n– Trong cửa sổ chọn trường.\nAfter:\n– Cập nhật “Đang chọn n/10 trường”; 0 trường → khóa Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; khóa nút Xuất Excel trong lúc xuất.\n'
        'During:\n– Lấy lại danh sách theo từ khóa + sắp xếp đang áp (cùng phạm vi kho, BR-02); lấy letterhead công ty người đăng nhập.\n'
        '– Lỗi → ' + XLS_ERR + '.\n'
        'After:\n– Dựng file (STT + trường đã chọn), tải về, đóng cửa sổ, hiển thị ' + XLS_OK + '; mở lại nút Xuất Excel; không ghi lịch sử.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Hoạt động kho; không lặp lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Không gắn quyền, phạm vi theo thủ kho', [
        '– Ai đăng nhập cũng mở màn và dùng mọi chức năng (y ERP, user chốt 26/10/2026).',
        '– Dữ liệu chỉ gồm phiếu của các kho người dùng là Thủ kho (danh mục Kho vật lý), mọi công ty; không là thủ kho kho nào → rỗng.',
        '– Super Admin: thiết kế là mọi kho (y ERP); bản hiện hành chưa đặc cách (đã báo).'],
     ['Xem danh sách', 'Tìm kiếm', 'Xuất Excel']),
    ('BR-02', 'Điều kiện phiếu lên bảng', [
        '– %s / %s ở trạng thái Chờ duyệt hoặc Đang xuất kho / Đang nhập kho; HOẶC' % (DNXK, DNNK),
        '– Thời gian nhận từ 00:00 hôm nay trở đi và trạng thái không phải Đang tạo, Đã hủy (gồm phiếu đã xuất / nhập kho, đang / đã hạch '
        'toán trong ngày).'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-03', 'Trạng thái trên bảng', [
        '– Có Thời gian hoàn thành → Đã hoàn thành; có Thời gian lấy/xếp hàng → Đang lấy hàng (ĐNXK) / Đang xếp hàng (ĐNNK); còn lại → '
        'Đã nhận đề nghị.',
        '– Không phải trạng thái lưu trên phiếu; nhãn + màu do máy chủ trả.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-04', 'Tổng thời gian xử lý', [
        '– = Thời gian hoàn thành − Thời gian nhận, dạng “x ngày y giờ z phút”, dưới 1 phút “Vài giây”; thiếu mốc → trống.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-05', 'Thứ tự và sắp xếp', [
        '– Mặc định: chưa hoàn thành trước, đã hoàn thành sau; trong nhóm theo Thời gian nhận mới nhất trước.',
        '– Sắp xếp được: Phiếu đề nghị, Kho (theo mã kho), Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành; cùng giá trị '
        'giữ thứ tự mặc định.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-06', 'Ô tổng hợp', [
        '– Tổng số phiếu nhận = số dòng; Tổng hoàn thành = số dòng Đã hoàn thành; Tổng chưa xử lý = hiệu 2 số.',
        '– Tính trên kết quả sau tìm kiếm; số không bấm được.'],
     ['Xem danh sách', 'Tìm kiếm']),
    ('BR-07', 'Tự tải lại', [
        '– Mỗi 60 giây khi tab đang hiện, giữ từ khóa + sắp xếp; không vòng tải, không báo lỗi.',
        '– Thay cho cập nhật tức thời của ERP (đã hỏng) — khác ERP có chủ đích.'],
     ['Xem danh sách']),
    ('BR-08', 'Tìm kiếm', [
        '– Khớp một phần mã phiếu, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; %, _ đúng nghĩa đen.',
        '– Ghi tạm từ khóa 10 phút (giữ khi tải lại trang, xóa khi rời sang màn khác).'],
     ['Tìm kiếm']),
    ('BR-09', 'Chỉ đọc, không ghi lịch sử', [
        '– Màn không có thao tác ghi dữ liệu phiếu; xem / tìm / xuất không ghi lịch sử.',
        '– Mọi thay đổi phiếu làm ở màn phiếu (Phần 5); bảng phản ánh ở lượt tải lại kế tiếp.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-10', 'Xuất Excel', [
        '– Xuất toàn bộ phiếu theo từ khóa + sắp xếp, dữ liệu lấy lại lúc bấm; rỗng vẫn tạo file.',
        '– Letterhead theo công ty của người xuất (file danh sách, không phải chứng từ).'],
     ['Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Hoạt động kho (phiếu đề nghị xuất / nhập kho cùng 3 mốc Thời gian nhận, Thời '
    'gian lấy/xếp hàng, Thời gian hoàn thành và danh sách thủ kho). Hoạt động kho chỉ đọc, không ghi lại màn nào.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', '%s (nguồn các dòng PDNXK; mã phiếu ở cột Phiếu đề nghị mở màn chi tiết phiếu này; hủy phiếu → dòng rời bảng)' % DNXK,
     'Kho -> Xuất kho'),
    ('2', 'Kho', '%s (nguồn các dòng PDNNK; mã phiếu mở màn chi tiết phiếu này; hủy phiếu → dòng rời bảng)' % DNNK, 'Kho -> Nhập kho'),
    ('3', 'Tài chính', 'Phiếu xuất kho (lập phiếu = duyệt đề nghị xuất kho → ghi Thời gian lấy hàng; gửi phiếu → ghi Thời gian hoàn thành)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('4', 'Kho', 'Phiếu nhập kho (lập phiếu = duyệt đề nghị nhập kho → ghi Thời gian xếp hàng; gửi phiếu → ghi Thời gian hoàn thành)',
     'Kho -> Nhập kho'),
    ('5', 'Kho', 'Điều chuyển kho (lập phiếu điều chuyển duyệt đề nghị xuất kho điều chuyển → ghi Thời gian lấy hàng)',
     'Kho -> Điều chuyển'),
    ('6', 'Tài chính', 'Yêu cầu xuất hàng, Yêu cầu nhập hàng (người lập yêu cầu = cột Người yêu cầu; Hình thức vận chuyển của yêu cầu '
                       'xuất hàng)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển'),
    ('7', 'Kho', 'Kho vật lý (ô Thủ kho quyết định phạm vi kho của người xem; mã - tên kho ở cột Kho)', 'Kho -> Danh mục'),
    ('8', 'Kho', 'Theo dõi theo kho (cùng bảng hoạt động, cùng cách tính, cho 1 kho chọn từ danh sách kho; dùng để đối chiếu)',
     'Kho -> Theo dõi theo kho'),
    ('9', 'Hệ thống ERP', 'Phiếu đề nghị xuất / nhập kho lập và gửi thủ kho trên hệ thống ERP (ghi Thời gian nhận) và màn Hoạt động kho '
                          'gốc của ERP (đọc cùng dữ liệu)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
