# -*- coding: utf-8 -*-
"""SRS màn "Phiếu xuất hàng mượn" (mã phiếu PXHM) — form chuẩn Danh mục quốc gia, chuẩn user chốt 04/11/2026.

Chạy: python gen_srs.py  → SRS - Phiếu xuất hàng mượn.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../borrow-export-request/gen_srs.py (cùng nghiệp vụ mượn hàng) + ../finance-bill-adjust-dept/gen_srs.py (Mục lục sang
  trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).
Nguồn đọc 05/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Entities/BorrowExport/BorrowExport*.php, Services/BorrowExport{,History}Service.php,
      Services/BorrowExportRequestNotifyService.php (onApproved), Services/BorrowExportRequestHistoryService.php (onApproved),
      Http/Controllers/V1/BorrowExportController.php, Http/Requests/BorrowExport/BorrowExportStoreRequest.php,
      Transformers/BorrowExportResource/BorrowExportListResource.php, Resources/views/prints/borrow-export{,-list}.blade.php,
      Routes/api.php}
  FE  pages/finance/borrow-exports/** (index, create, _id/index, components/{BorrowExportForm, BorrowExportRequestPickerModal,
      export-excel.js}), pages/finance/borrow-export-requests/_id/index.vue (nút Tạo phiếu xuất hàng mượn),
      components/subsystem-menu/finance.js
Ảnh: ./pxhm_shots — dev-hrm 05/11/2026 (_capture/capture.js); popup chọn phiếu yêu cầu có dữ liệu, form đã chọn phiếu, hộp
  "Thông tin chưa lưu", mở từ phiếu yêu cầu, lịch sử có mốc: chụp LOCAL (_capture/capture_local.js) vì dev không có phiếu yêu
  cầu Chờ duyệt / phiếu xuất có lịch sử. Lỗi đỏ "Bắt buộc phải chọn" chụp bằng cách bật cờ trên trình duyệt (không bấm Lưu).
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

TEN = 'Phiếu xuất hàng mượn'
SHOTS = os.path.join(HERE, 'pxhm_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng => Phiếu xuất hàng mượn'
MENU_YC = ('Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng => Yêu cầu xuất hàng mượn => Xem chi tiết '
           '=> Tạo phiếu xuất hàng mượn')
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu xuất hàng mượn.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
NOQ = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này” và dừng xử lý.')

A_KT = 'Kế toán kho'
TN = 'Người dùng có quyền thực hiện chức năng: Kế toán kho.'
TN_COST = ('Người dùng có quyền thực hiện chức năng: Kế toán kho (cột Đơn giá vốn chỉ hiện thêm khi có quyền Xem giá vốn '
           'hàng hoá).')
DK = '1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán kho.\n3. Người dùng đang ở màn danh sách Phiếu xuất hàng mượn.'

d = SrsDoc(out=OUT, menu=MENU, route='/finance/borrow-exports', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Hàng hoá - Dịch vụ - Vận chuyển': 'menu_nhom',
    'Mượn hàng': 'menu_muonhang', 'Phiếu xuất hàng mượn': 'menu_muc', 'Yêu cầu xuất hàng mượn': 'menu_muc_yc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Chọn phiếu yêu cầu': 'o_phieuyc', 'Xem chi tiết': 'link_sophieu',
    'Tạo phiếu xuất hàng mượn': 'btn_taophieuxuat', 'In': 'btn_in_row', 'Xuất Excel': 'btn_xuatexcel',
    'Lịch sử': 'btn_lichsu_row',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    """Biểu đồ Use Case 1 chức năng theo khổ mẫu quốc gia (actor + 1 use case)."""
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None, extra=None):
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event."""
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
    if 'entries' in layout:
        d.p('Đường dẫn màn hình:')
        for m, note in layout['entries']:
            d._menu_para(m)
            d.p(note)
        d.figure(layout['shot'], layout['shot_caption'], width_in=6.2)
    else:
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


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.doc.add_page_break()  # Mục lục sang trang riêng như bản Drive đã chuẩn hoá
d.h2('Mục lục')
d.doc.paragraphs[-1].alignment = 1  # căn giữa chữ 'Mục lục'
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu xuất hàng mượn (mã phiếu PXHM-NNNNN), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ việc Kế toán kho lập Phiếu xuất hàng mượn chính là DUYỆT một phiếu Yêu cầu xuất hàng mượn: tất toán phần '
    'hàng người mượn không trả lại mà xuất hẳn.',
    'Làm rõ cách hệ thống kiểm số “Đang mượn” và các dữ liệu bị ghi ngược sang phiếu yêu cầu và phiếu xuất mượn gốc.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Lập phiếu (Lưu và duyệt / Lưu và '
    'tiếp tục), Chọn phiếu yêu cầu xuất hàng mượn, Xem chi tiết, In phiếu / In danh sách, Xuất Excel, Xem lịch sử thay đổi. '
    'Màn KHÔNG có Lưu nháp, Gửi duyệt, Sửa, Xóa, Không duyệt, Hủy, Khóa / Mở khóa và Import Excel: phiếu sinh ra đã ở '
    'trạng thái Đã duyệt và không thay đổi về sau.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phiếu xuất hàng mượn là chứng từ ghi lại “duyệt bao nhiêu, trừ vào phiếu mượn nào” cho từng mặt hàng.',
    'Số Xuất được ghi ngược thành số Được duyệt trên phiếu yêu cầu và cộng vào số đã trả của phiếu xuất mượn gốc; phiếu '
    'mượn trả hết chuyển trạng thái mượn sang Đã trả.',
    'Số còn mượn ở các màn Danh sách hàng mượn, Hàng sắp hết hạn mượn, Yêu cầu / Phiếu xuất bán hàng mượn, Phiếu yêu cầu '
    'gia hạn hàng mượn giảm tương ứng.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Chỉ Kế toán kho dùng được màn này (cả xem lẫn lập) (BR-01).',
    'Chỉ chọn được phiếu yêu cầu đang Chờ duyệt; mỗi phiếu xuất gắn đúng 1 phiếu yêu cầu (BR-02).',
    'Mọi ô Xuất phải lớn hơn 0 và không vượt số Đang mượn tính lại ngay lúc lưu (BR-03).',
    'Lưu là ghi ngay, không có nháp, không sửa / xóa được về sau (BR-04).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu xuất hàng mượn', 'Chứng từ PXHM-NNNNN của màn này, do Kế toán kho lập để duyệt một phiếu yêu cầu xuất hàng mượn.'),
    ('Phiếu yêu cầu xuất hàng mượn (phiếu yêu cầu)', 'Phiếu PYCXHM-NNNNN do người mượn lập ở màn Yêu cầu xuất hàng mượn, '
                                                    'xin xuất hẳn phần hàng đang mượn không trả lại.'),
    ('Phiếu xuất mượn (phiếu mượn)', 'Phiếu yêu cầu xuất hàng loại Xuất mượn (mã PYCXH-…) đã giao hàng cho người mượn; '
                                    'phiếu yêu cầu gom một hoặc nhiều phiếu mượn.'),
    ('Đang mượn', 'Số lượng của một mặt hàng trên một phiếu mượn còn được phép xuất: đã xuất − đã trả − phần đang chờ ở '
                  'các phiếu khác chưa duyệt (không tính chính phiếu yêu cầu đang duyệt), quy theo đơn vị tính của dòng, '
                  'làm tròn xuống.'),
    ('Xuất', 'Trường đặc thù: số Kế toán kho chấp nhận xuất hẳn của 1 mặt hàng trên 1 phiếu mượn; điền sẵn bằng số người '
             'lập đề nghị, sửa được, phải > 0 và ≤ Đang mượn.'),
    ('Được duyệt', 'Số ghi ngược lên phiếu yêu cầu sau khi lưu phiếu xuất, bằng số Xuất của từng dòng.'),
    ('Đơn giá bán', 'Giá bán của mặt hàng lấy nguyên từ phiếu yêu cầu; Thành tiền = Số lượng × Đơn giá bán.'),
    ('Đơn giá vốn', 'Giá vốn bình quân của phần hàng xuất, tính từ giá vốn trên các phiếu mượn; chỉ người có quyền Xem '
                    'giá vốn hàng hoá thấy.'),
    ('Trạng thái Đã duyệt', 'Trạng thái duy nhất của phiếu (nhãn xanh lá): phiếu lưu xong là Đã duyệt, không đổi về sau.'),
    ('Trạng thái Đang tạo / Chờ duyệt / Không duyệt', 'Chỉ còn trong danh mục trạng thái dùng chung, màn này không tạo ra; '
                                                     'ô lọc Trạng thái chỉ có Đã duyệt.'),
    ('Kế toán kho', 'Người có quyền Kế toán kho — vai trò duy nhất xem và lập phiếu.'),
    ('Cấu trúc phân cấp', 'Phiếu xuất > dòng hàng hóa (mỗi hàng + đơn vị 1 dòng) > dòng chi tiết theo từng phiếu mượn (Phiếu '
                          'mượn, Đang mượn, Xuất). Số lượng của dòng hàng = tổng Xuất các dòng chi tiết.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn chỉ có một vai trò sử dụng là Kế toán kho; không có quyền xem theo cấp (tổng công ty / công ty / phòng ban): '
    'người có quyền Kế toán kho thấy toàn bộ phiếu. Người dùng là Super admin được coi như có đủ quyền.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán kho',
     'Mở được màn danh sách, xem chi tiết, lập phiếu (Lưu và duyệt / Lưu và tiếp tục), chọn phiếu yêu cầu, in, xuất Excel, '
     'xem lịch sử; ở màn Yêu cầu xuất hàng mượn thấy nút Tạo phiếu xuất hàng mượn với phiếu Chờ duyệt.'),
    ('Q2', 'Xem giá vốn hàng hoá',
     'Chỉ bổ sung: hiện cột Đơn giá vốn ở màn chi tiết và trên bản in phiếu. Không có quyền này thì cột bị ẩn và hệ thống '
     'không trả giá vốn.'),
], widths=[0.8, 1.8, 3.4])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '❌ (chỉ có Q2 thì không vào được màn)', '❌ (báo không có quyền, bảng rỗng)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌', '❌'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅ (chỉ lưu cấu hình hiển thị)', '✅ (chỉ lưu cấu hình hiển thị)'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅ (chỉ lưu cấu hình hiển thị)', '✅ (chỉ lưu cấu hình hiển thị)'),
    ('FR-05 Lập phiếu xuất hàng mượn', '✅', '❌', '❌'),
    ('FR-06 Chọn phiếu yêu cầu xuất hàng mượn', '✅', '❌', '❌'),
    ('FR-07 Xem chi tiết phiếu', '✅ (ẩn Đơn giá vốn nếu thiếu Q2)', '✅ cột Đơn giá vốn (khi có cả Q1)', '❌'),
    ('FR-08 In phiếu / In danh sách', '✅ (bản in không có Đơn giá vốn nếu thiếu Q2)', '✅ cột Đơn giá vốn (khi có cả Q1)', '❌'),
    ('FR-09 Xuất Excel', '✅', '❌', '❌'),
    ('FR-10 Xem lịch sử thay đổi', '✅', '❌', '❌'),
    ('Sửa / Xóa / Khóa – Mở khóa / Không duyệt / Import Excel', '—', '—', '— (màn không có chức năng này)'),
], widths=[2.2, 1.3, 1.3, 1.2])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có quyền Kế toán kho: menu vẫn hiện; mở màn thì hệ thống báo “Bạn không có quyền thực hiện chức năng này”, bảng '
    'hiện “Không có dữ liệu phù hợp.”.',
    'Mở màn chi tiết / bản in khi không có quyền (qua đường link): báo “Bạn không có quyền thực hiện chức năng này” và quay về '
    'danh sách.',
    'Mở màn Lập phiếu khi không có quyền: popup chọn phiếu yêu cầu không có dữ liệu, Lưu và duyệt bị máy chủ từ chối với câu '
    'trên; nút Tạo phiếu xuất hàng mượn ở màn Yêu cầu xuất hàng mượn không hiện.',
    'Bị gỡ quyền giữa lúc thao tác: lần bấm tiếp theo bị từ chối như trên (quyền kiểm lại ở từng thao tác).',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới, In, Xuất Excel, Cấu hình cột, Cài đặt bộ lọc', 'Luôn hiện', 'Quyền kiểm tra ở máy chủ khi thao tác'),
    ('Nút In, Lịch sử trên dòng', 'Luôn hiện trên mọi dòng', 'Không có nút Sửa / Xóa / Duyệt'),
    ('Cột Đơn giá vốn (màn chi tiết, bản in phiếu)', 'Có quyền Xem giá vốn hàng hoá', 'Ẩn hẳn cột khi không có quyền'),
    ('Nút Tạo phiếu xuất hàng mượn (màn Yêu cầu xuất hàng mượn)', 'Quyền Kế toán kho và phiếu yêu cầu Chờ duyệt',
     'Lối vào thứ hai của màn Lập phiếu'),
], widths=[2.4, 2.0, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_KT, [0, 1, 2, 3])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu xuất hàng mượn', 'crud'),
     ('FR-08', 'In phiếu / In danh sách', 'io'),
     ('FR-09', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-07', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-10', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn phiếu yêu cầu xuất hàng mượn', 'crud', 'extend', [1], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu xuất hàng mượn')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu xuất hàng mượn',
       mota='Hiển thị bảng toàn bộ phiếu xuất hàng mượn đã lập (không giới hạn theo công ty / phòng ban / người lập), kèm '
            'phân trang, sắp xếp và tổng số phiếu khớp bộ lọc. Màn chỉ có một lối vào từ menu và chỉ dành cho người có quyền '
            'Kế toán kho; mỗi dòng có liên kết sang màn chi tiết và sang phiếu yêu cầu đã được duyệt.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán kho.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống kiểm tra quyền Kế toán kho.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu vừa đi vào màn con của màn này) và cấu hình '
             'cột đã lưu của người dùng.\n'
             '4. Hệ thống lấy toàn bộ phiếu khớp bộ lọc, sắp phiếu tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, kèm dòng “Hiển thị a–b / N” và phân trang.',
       phu='• Không có quyền Kế toán kho → thông báo “Bạn không có quyền thực hiện chức năng này”, bảng hiện “Không có dữ liệu '
           'phù hợp.”.\n'
           '• Không có phiếu nào khớp → trong bảng hiện “Không có dữ liệu phù hợp.”, dưới bảng hiện “Không có phiếu nào.”.\n'
           '• Máy chủ lỗi khi nạp danh sách → thông báo “Lỗi khi tải dữ liệu”, bảng giữ trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó thay cho bộ cột mặc định.\n'
           '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo câu của máy chủ (mặc định “Phiên đăng nhập đã hết hạn”), '
           'hệ thống xóa phiên và chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 11 cột (STT, Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người tạo, Ngày tạo, Trạng thái, '
               'Ghi chú, Người cập nhật, Ngày cập nhật, Hành động); không có cột ẩn mặc định. Cột bắt buộc (không ẩn, không '
               'đổi vị trí): STT, Mã phiếu, Hành động; STT và Mã phiếu ghim trái khi cuộn ngang. Sắp xếp được: Mã phiếu, Ngày '
               'tạo; mặc định Ngày tạo mới nhất ở trên. Đổi sắp xếp, đổi bộ lọc, đổi số dòng đều về trang 1; chuyển trang giữ '
               'bộ lọc và sắp xếp.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Phiếu xuất hàng mượn'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Phiếu xuất hàng mượn” trên thanh tiêu đề, tiêu đề bảng và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “Lập phiếu xuất hàng mượn (duyệt phiếu yêu cầu)”', '- Bấm → mở màn Lập phiếu xuất hàng mượn (mục 2.5)']),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “In danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.8)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.9)',
         '- Khóa trong lúc đang xuất file']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        '- Biểu tượng cột; bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đánh số liên tục theo trang (trang 2 bắt đầu từ số dòng/trang + 1)', '- Cột khóa, ghim trái khi cuộn ngang']),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PXHM-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết phiếu (mục 2.7); chuột phải mở được ở tab mới', '- Sắp xếp được',
         '- Cột khóa, ghim trái khi cuộn ngang']),
       ('Cột Phiếu yêu cầu', 'Table/Grid', 'Read-only', 'PYCXHM-NNNNN', 'Hiển thị',
        ['- Mã phiếu yêu cầu xuất hàng mượn mà phiếu này đã duyệt',
         '- Là liên kết: bấm → mở chi tiết phiếu yêu cầu ở TAB MỚI (danh sách giữ nguyên)', '- Không sắp xếp']),
       ('Cột Người yêu cầu', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Họ tên người lập phiếu yêu cầu (người mượn)', '- Không sắp xếp']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Kế toán kho lập phiếu xuất, dạng “Họ tên - Mã phòng ban”', '- Không sắp xếp']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Thời điểm lưu phiếu (cũng là thời điểm duyệt phiếu yêu cầu)', '- Sắp xếp được; mặc định mới nhất ở trên']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 1 giá trị', 'Hiển thị',
        ['- Đã duyệt: nhãn màu xanh lá', '- Chữ và màu do máy chủ trả về', '- Không sắp xếp']),
       ('Cột Ghi chú', 'Table/Grid', 'Read-only', '0–255 ký tự', 'Hiển thị',
        ['- Ghi chú Kế toán kho nhập khi lập phiếu; trống nếu không nhập', '- Tự xuống dòng khi dài']),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Dạng “Họ tên - Mã phòng ban”', '- Phiếu không sửa được nên trùng người tạo hoặc trống']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        '- Thời điểm cập nhật gần nhất; với phiếu lập trên màn này trùng Ngày tạo.'),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Nút In: bấm → mở cửa sổ Xem trước phiếu (mục 2.8)',
           '- Nút Lịch sử: bấm → mở cửa sổ Lịch sử thay đổi (mục 2.10)',
           '- Không có nút Sửa / Xóa / Duyệt ở bất kỳ phiếu nào', '- Cột khóa trong Tùy chỉnh cột']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Trong bảng: “Không có dữ liệu phù hợp.”', '- Dưới bảng: “Không có phiếu nào.”', '- Chỉ hiện khi N = 0']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang đang xem', '- N: tổng số phiếu khớp bộ lọc']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Ở trang đầu nút về đầu / lùi mờ; ở trang cuối nút tiến / về cuối mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Lỗi khi tải dữ liệu” khi máy chủ lỗi', '- “Bạn không có quyền thực hiện chức năng này” khi thiếu quyền']),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Kiểm tra quyền Kế toán kho.\n' + NOQ + '\n'
        '– Khôi phục bộ lọc (10 phút) và cấu hình cột đã lưu.\n'
        'During:\n– Lấy toàn bộ phiếu khớp bộ lọc, không giới hạn theo công ty / phòng ban / người lập.\n'
        '– Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, phiếu tạo mới nhất ở trên, kèm dòng “Hiển thị a–b / N”.'),
       ('Bấm Mã phiếu', 'Click',
        'Before:\n– Người dùng có quyền Kế toán kho.\n'
        'After:\n– Mở màn chi tiết phiếu (mục 2.7); bộ lọc hiện tại được ghi nhớ 10 phút để khôi phục khi quay lại.'),
       ('Bấm Phiếu yêu cầu', 'Click',
        'Before:\n– Dòng có phiếu yêu cầu.\nAfter:\n– Mở chi tiết phiếu yêu cầu xuất hàng mượn ở tab mới; danh sách giữ nguyên trang và bộ lọc.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ cột Mã phiếu và Ngày tạo hỗ trợ sắp xếp; cột khác không có biểu tượng sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp.\nAfter:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại theo số dòng mới.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu',
       mota='Thu hẹp danh sách theo mã phiếu, mã phiếu yêu cầu, người yêu cầu, người tạo, hàng hóa, trạng thái và ngày tạo. '
            'Ô tìm nhanh tìm đồng thời theo mã phiếu xuất và mã phiếu yêu cầu; 7 ô lọc nâng cao nằm trong khối Tìm kiếm '
            'nâng cao, có thể bật / tắt bằng Cài đặt bộ lọc (mục 2.3). Màn không có ô lọc Công ty / Phòng ban.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập mã vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Hệ thống lọc ngay khi một ô lọc nâng cao đổi giá trị (ô chữ lọc ngay khi gõ), về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Hệ thống ghi nhớ bộ lọc 10 phút khi người dùng đi vào màn con của màn này.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Gõ vào ô tìm nhanh mà chưa bấm Tìm kiếm / Enter → danh sách chưa đổi.\n'
           '• Bấm dấu × trong ô → xóa giá trị của ô đó.\n'
           '• Ô lọc bị tắt trong Cài đặt bộ lọc → không hiện trên khối lọc.',
       dacbiet='Trường tìm nhanh: mã phiếu xuất HOẶC mã phiếu yêu cầu (không tìm theo tên người). Kiểu khớp: một phần (chuỗi '
               'nhập nằm ở bất kỳ vị trí nào), không phân biệt hoa / thường; khoảng trắng đầu / cuối của ô tìm nhanh được bỏ. '
               'Ô Hàng hóa khớp một phần theo tên HOẶC mã hàng hóa trên phiếu. Không giới hạn số ký tự nhập. Ký tự % và _ được '
               'hiểu là ký tự đại diện. Mọi điều kiện kết hợp theo kiểu VÀ. Ngày tạo lấy trọn hai ngày biên, được bỏ trống một '
               'đầu. Ghi nhớ bộ lọc: trên trình duyệt (dùng chung các tab, không theo tài khoản), 10 phút, chỉ khi đi vào màn '
               'con (chi tiết / lập phiếu); F5 hoặc sang màn khác thì bộ lọc về trống.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã phiếu, mã phiếu yêu cầu”', '- Khớp một phần mã phiếu xuất hoặc mã phiếu yêu cầu',
         '- Chỉ lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Bấm → xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc nâng cao', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Mã phiếu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Phiếu có mã chứa chuỗi nhập', '- Lọc ngay khi gõ']),
       ('Mã phiếu yêu cầu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Phiếu có mã phiếu yêu cầu chứa chuỗi nhập', '- Lọc ngay khi gõ']),
       ('Người yêu cầu', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống (mọi người)', '- Lọc phiếu có phiếu yêu cầu do người đó lập']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lọc phiếu xuất do Kế toán kho đó lập']),
       ('Hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập tên hoặc mã hàng hóa”', '- Phiếu có ít nhất 1 dòng hàng có tên hoặc mã chứa chuỗi nhập']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 1 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn: Đã duyệt (trạng thái duy nhất của phiếu)']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
   ],
   ev=[
       ('Đổi giá trị một ô lọc nâng cao', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\n'
        'During:\n– Ghi nhận giá trị mới (ô chữ: theo từng ký tự gõ).\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí đang có.'),
       ('Bấm Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm phiếu có mã phiếu hoặc mã phiếu yêu cầu chứa chuỗi nhập.\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\n'
        'After:\n– Xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\nAfter:\n– Mở / thu gọn khối ô lọc; trạng thái mở được ghi nhớ cùng bộ lọc.'),
       ('Quay lại từ màn con trong 10 phút', 'System',
        'Before:\n– Người dùng vừa đi từ danh sách vào màn chi tiết / lập phiếu.\n'
        'After:\n– Khôi phục bộ lọc và trạng thái khối lọc; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn những ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự của chúng. '
            'Cấu hình lưu riêng theo người dùng cho màn Phiếu xuất hàng mượn, không ảnh hưởng người khác và không làm đổi '
            'dữ liệu phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 7 ô lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 7 ô theo thứ tự thiết kế; vẫn phải bấm Lưu mới có hiệu lực.\n'
           '• Bỏ tích ô đang có giá trị lọc → ô bị ẩn và giá trị lọc của ô đó bị bỏ.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách ô lọc', 'Table/Grid', 'Enable', 'Danh sách 7 ô lọc', '–', 'Theo cấu hình đã lưu',
        ['- Mã phiếu', '- Mã phiếu yêu cầu', '- Người yêu cầu', '- Người tạo', '- Hàng hóa', '- Trạng thái', '- Ngày tạo']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích',
        '- Bỏ tích → ô lọc đó không hiện ở khối Tìm kiếm nâng cao.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí ô lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
        '- Bấm → tích lại đủ 7 ô theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
       ('Khối Tìm kiếm nâng cao sau khi lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình',
        '- Chỉ hiện các ô đã tích, đúng thứ tự đã kéo.'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\n'
        'After:\n– Mở cửa sổ, nạp cấu hình đang lưu của người dùng (chưa lưu lần nào → đủ 7 ô theo thiết kế).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách ô đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 7 ô và đưa thứ tự về thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 11 cột của bảng danh sách. Ba cột STT, Mã phiếu, Hành động bị khóa; '
            'cấu hình lưu riêng theo người dùng trên máy chủ cho màn này, chỉ đổi cách hiển thị, không làm đổi dữ liệu, bộ '
            'lọc hay tổng số phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 11 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 11 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ nguyên sau khi tải lại trang, '
               'đăng nhập lại, đổi trình duyệt / máy khác; người dùng khác không bị ảnh hưởng.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 11 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người tạo, Ngày tạo',
         '- Trạng thái, Ghi chú, Người cập nhật, Ngày cập nhật, Hành động']),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Mã phiếu, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/11 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình',
        '- n = số cột đang tích, cập nhật ngay khi tích / bỏ tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng.'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/11 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng theo cột đã chọn.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu xuất hàng mượn (Lưu và duyệt)', usecase=('FR-05', 'Lập phiếu xuất hàng mượn', 'crud', A_KT),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lập phiếu xuất hàng mượn (duyệt phiếu yêu cầu xuất hàng mượn)',
       mota='Kế toán kho chọn một phiếu yêu cầu xuất hàng mượn đang Chờ duyệt, kiểm tra số Xuất của từng mặt hàng trên '
            'từng phiếu mượn rồi bấm Lưu và duyệt. Một lần lưu: sinh phiếu PXHM-NNNNN ở trạng thái Đã duyệt, ghi số Được '
            'duyệt và trạng thái Đã duyệt về phiếu yêu cầu, cộng số đã trả vào phiếu mượn gốc. Không có bản nháp, không sửa '
            'được sau khi lưu.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán kho.\n'
                '3. Có ít nhất 1 phiếu yêu cầu xuất hàng mượn đang ở trạng thái Chờ duyệt.',
       chinh='1. Người dùng bấm Tạo mới ở danh sách (hoặc Tạo phiếu xuất hàng mượn ở màn chi tiết phiếu yêu cầu).\n'
             '2. Hệ thống mở màn “Lập phiếu xuất hàng mượn”; góc phải khối Thông tin chung ghi “<người tạo> - <ngày giờ '
             'hiện tại>”. Vào từ phiếu yêu cầu thì phiếu đó được chọn sẵn.\n'
             '3. Người dùng bấm ô Phiếu yêu cầu xuất hàng mượn, chọn phiếu ở popup (mục 2.6).\n'
             '4. Hệ thống điền Người lập phiếu yêu cầu, Phòng ban, các chip Phiếu xuất mượn và bảng Chi tiết: mỗi hàng 1 dòng, '
             'mỗi phiếu mượn có hàng đó 1 dòng con với số Đang mượn; ô Xuất điền sẵn số người lập đề nghị.\n'
             '5. Người dùng sửa số Xuất nếu cần, nhập Ghi chú (không bắt buộc).\n'
             '6. Người dùng bấm Lưu và duyệt.\n'
             '7. Hệ thống kiểm tra dữ liệu, tính lại số Đang mượn, sinh mã PXHM-NNNNN, lưu phiếu Đã duyệt.\n'
             '8. Hệ thống ghi số Được duyệt cho từng dòng phiếu yêu cầu, chuyển phiếu yêu cầu sang Đã duyệt (người duyệt, '
             'ngày duyệt), cộng số đã trả vào phiếu mượn gốc; phiếu mượn trả hết chuyển trạng thái mượn Đã trả.\n'
             '9. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu xuất và hành động “Duyệt” trong lịch sử của '
             'phiếu yêu cầu (kèm mã phiếu xuất).\n'
             '10. Hệ thống gửi thông báo “[YCXHM] Đã duyệt: <mã phiếu yêu cầu>” (người duyệt, phiếu xuất) cho người lập phiếu '
             'yêu cầu.\n'
             '11. Hệ thống hiển thị “Thao tác thành công.” và chuyển về màn danh sách.',
       phu='• Bấm Lưu và tiếp tục → lưu như trên, ở lại màn Lập với form trắng (bỏ phiếu yêu cầu chọn sẵn trên đường dẫn).\n'
           '• Chưa chọn phiếu yêu cầu → viền đỏ, “Bắt buộc phải chọn” dưới ô, thông báo “Bạn chưa nhập đầy đủ thông tin.”.\n'
           '• Ô Xuất ≤ 0 → “Phải lớn hơn 0” dưới ô; ô Xuất > Đang mượn → “Không được vượt quá <Đang mượn>”; thông báo “Vui '
           'lòng kiểm tra lại thông tin đã nhập”, tự cuộn tới ô lỗi đầu tiên.\n'
           '• Trong lúc lưu có phiếu khác đã trừ mất hàng → “Số lượng không hợp lệ”; phiếu yêu cầu đã được người khác duyệt '
           '→ “Không thể duyệt yêu cầu này!”; không lưu gì.\n'
           '• Dòng hàng không có trên phiếu mượn nào → dòng mờ “Chưa có phiếu mượn”, không nhập được.\n'
           '• Bấm × trong ô Phiếu yêu cầu → bỏ phiếu đã chọn và toàn bộ bảng Chi tiết.\n'
           '• Bấm Quay lại / chuyển menu / đóng tab khi đã chọn phiếu hoặc đã sửa → hộp “Thông tin chưa lưu” (Thoát / Ở lại); '
           'chưa thay đổi gì thì về danh sách ngay.\n'
           '• Không có quyền Kế toán kho → “Bạn không có quyền thực hiện chức năng này”.',
       dacbiet='Lưu và duyệt ghi ngay, KHÔNG có hộp xác nhận. Hai nút lưu bị khóa trong lúc đang lưu để một lần bấm không tạo '
               '2 phiếu. Phiếu không có trường nhập duy nhất: mã PXHM-NNNNN tự sinh tăng dần, không sửa được; một phiếu yêu '
               'cầu chỉ duyệt được 1 lần nên không thể có 2 phiếu xuất cho cùng phiếu yêu cầu. Ghi chú tối đa 255 ký tự.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới', 'Mở màn Lập phiếu với ô Phiếu yêu cầu trống — chọn phiếu ở popup (mục 2.6).'),
       (MENU_YC, 'Từ màn chi tiết một phiếu yêu cầu Chờ duyệt (chỉ Kế toán kho thấy nút): mở màn Lập phiếu với phiếu yêu '
                 'cầu đó chọn sẵn, bảng Chi tiết điền sẵn.')],
       shot=shot('10c_filled'), shot_caption='Màn Lập phiếu xuất hàng mượn sau khi chọn phiếu yêu cầu'),
   extra=[(shot('10_create'), 'Màn Lập phiếu xuất hàng mượn lúc mới mở'),
          (shot('10b_validate'), 'Lỗi “Bắt buộc phải chọn” khi chưa chọn phiếu yêu cầu'),
          (shot('10g_unsaved'), 'Hộp “Thông tin chưa lưu” khi rời màn')],
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Lập phiếu xuất hàng mượn” (thanh tiêu đề, tab trình duyệt).'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại',
        '- Góc phải khối Thông tin chung: “<Họ tên> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu yêu cầu xuất hàng mượn', 'Textbox', 'Enable', 'Mã phiếu Chờ duyệt', 'Có', 'Trống',
        ['- Gợi ý “Nhấn vào đây để chọn phiếu yêu cầu xuất hàng mượn”; bấm ô → mở popup chọn (mục 2.6)',
         '- Có dấu × để bỏ phiếu đã chọn', '- Lỗi: “Bắt buộc phải chọn” (viền đỏ) sau lần bấm lưu đầu']),
       ('Người lập phiếu yêu cầu', 'Textbox', 'Disable', '–', '–', 'Ẩn',
        '- Chỉ hiện sau khi chọn phiếu; họ tên người lập phiếu yêu cầu.'),
       ('Phòng ban người lập phiếu yêu cầu', 'Textbox', 'Disable', '–', '–', 'Ẩn',
        '- Chỉ hiện sau khi chọn phiếu; phòng ban của người lập phiếu yêu cầu.'),
       ('Phiếu xuất mượn', 'Label', 'Read-only', '–', '–', '“Chưa chọn phiếu xuất mượn”',
        ['- Các chip mã phiếu mượn mà phiếu yêu cầu gom lại', '- Bấm chip → mở phiếu mượn ở tab mới']),
       ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập ghi chú (nếu có)...”', '- Không nhập được quá 255 ký tự']),
       ('Bảng Chi tiết khi chưa chọn phiếu', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chưa chọn phiếu yêu cầu.”'),
       ('Cột STT, Tên hàng hóa', 'Table/Grid', 'Read-only', '–', '–', 'Theo phiếu yêu cầu',
        ['- Tên hàng kèm Model / Mã / Thương hiệu', '- Chỉ dòng hàng có số đề nghị > 0 của phiếu yêu cầu']),
       ('Cột Đơn vị tính', 'Table/Grid', 'Read-only', '–', '–', 'Theo phiếu yêu cầu',
        '- Đơn vị đã chốt trên phiếu yêu cầu, không đổi được; hệ số khác 1 thì ghi “(xN)”.'),
       ('Cột Đơn giá', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo phiếu yêu cầu', '- Đơn giá bán, dạng 1,234,567.'),
       ('Cột Số lượng', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Tổng ô Xuất', '- Tự cộng các ô Xuất của dòng hàng.'),
       ('Cột Phiếu mượn', 'Table/Grid', 'Read-only', 'PYCXH-…', '–', 'Theo phiếu yêu cầu',
        '- Liên kết mở phiếu mượn ở tab mới (đang nhập form nên không mở cùng tab).'),
       ('Cột Đang mượn', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
        '- Số còn được phép xuất của hàng trên phiếu mượn đó (xem Thuật ngữ).'),
       ('Ô Xuất', 'Textbox', 'Enable', 'Số nguyên 1 – Đang mượn', 'Có', 'Số đề nghị trên phiếu yêu cầu',
        ['- Chỉ nhận chữ số, hiển thị dấu phẩy ngăn nghìn', '- Lỗi: “Phải lớn hơn 0”',
         '- Lỗi: “Không được vượt quá <Đang mượn>” (báo ngay khi gõ)']),
       ('Dòng “Chưa có phiếu mượn”', 'Label', 'Disable', '–', '–', 'Ẩn',
        '- Dòng hàng không có trên phiếu mượn nào: tô mờ, không nhập được.'),
       ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '- Tổng cột Số lượng của cả phiếu.'),
       ('Nút Lưu và duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → kiểm tra rồi lưu phiếu + duyệt phiếu yêu cầu, về danh sách', '- Khóa trong lúc lưu']),
       ('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Rê chuột: “Lưu phiếu này rồi tiếp tục lập phiếu mới”', '- Lưu xong ở lại màn Lập với form trắng']),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
       ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Nội dung: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu',
         '- Nút Ở lại: đóng hộp, giữ dữ liệu']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Thao tác thành công.”', '- Thiếu: “Bạn chưa nhập đầy đủ thông tin.”',
         '- Sai số: “Vui lòng kiểm tra lại thông tin đã nhập”', '- Máy chủ: “Số lượng không hợp lệ” / “Không thể duyệt yêu cầu này!”']),
   ],
   ev=[
       ('Mở màn Lập phiếu', 'System',
        'Before:\n– Vào bằng nút Tạo mới hoặc nút Tạo phiếu xuất hàng mượn của phiếu yêu cầu.\n'
        'During:\n– Có phiếu yêu cầu kèm theo → nạp phiếu; phiếu không còn Chờ duyệt / không có quyền → “Phiếu yêu cầu này '
        'không ở trạng thái chờ duyệt hoặc bạn không có quyền duyệt.”.\n'
        'After:\n– Hiển thị form; vào từ phiếu yêu cầu thì bảng Chi tiết điền sẵn, chưa tính là đã thay đổi.'),
       ('Sửa ô Xuất', 'Change',
        'Before:\n– Dòng có phiếu mượn.\n'
        'During:\n– Bỏ ký tự không phải số; > Đang mượn → “Không được vượt quá <Đang mượn>” ngay dưới ô.\n'
        'After:\n– Cập nhật cột Số lượng và dòng Tổng cộng.'),
       ('Bấm Lưu và duyệt', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán kho.\n' + NOQ + '\n'
        '– Kiểm tra phiếu yêu cầu còn Chờ duyệt, nếu không → “Không thể duyệt yêu cầu này!”.\n'
        'During:\n– Chưa chọn phiếu → “Bắt buộc phải chọn”, thông báo “Bạn chưa nhập đầy đủ thông tin.”.\n'
        '– Ô Xuất ≤ 0 → “Phải lớn hơn 0”; vượt Đang mượn → “Không được vượt quá <số>”; thông báo “Vui lòng kiểm tra lại '
        'thông tin đã nhập”.\n'
        '– Ghi chú > 255 ký tự → “Không được vượt quá 255 ký tự”; ô Xuất quá 6 chữ số → “Không được vượt quá 6 chữ số”.\n'
        '– Tính lại Đang mượn; vượt → “Số lượng không hợp lệ”.\n' + ERR + '\n'
        'After:\n– Sinh phiếu PXHM-NNNNN trạng thái Đã duyệt, lưu dòng hàng và dòng chi tiết.\n'
        '– Phiếu yêu cầu: ghi số Được duyệt, chuyển Đã duyệt (người duyệt, ngày duyệt); phiếu mượn: cộng số đã trả.\n'
        '– Ghi một dòng lịch sử “Tạo mới” cho phiếu xuất và “Duyệt” cho phiếu yêu cầu.\n'
        '– Gửi thông báo cho người lập phiếu yêu cầu.\n'
        '– Hiển thị “Thao tác thành công.”, về màn danh sách.'),
       ('Bấm Lưu và tiếp tục', 'Click',
        'Before:\n– Như Lưu và duyệt.\nDuring:\n– Kiểm tra như Lưu và duyệt.\n' + ERR + '\n'
        'After:\n– Lưu như Lưu và duyệt; bỏ phiếu yêu cầu trên đường dẫn, làm trắng form, ở lại màn Lập.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở màn.\n'
        'During:\n– Có thay đổi → hiện hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu; Ở lại: giữ nguyên form.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn phiếu yêu cầu xuất hàng mượn', usecase=('FR-06', 'Chọn phiếu yêu cầu xuất hàng mượn', 'crud', A_KT),
   rule=('- Bộ lọc, Dropdown và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn phiếu yêu cầu xuất hàng mượn ở màn Lập phiếu',
       mota='Popup liệt kê các phiếu yêu cầu xuất hàng mượn đang ở trạng thái Chờ duyệt để Kế toán kho chọn đúng 1 phiếu cần '
            'duyệt. Điều kiện Chờ duyệt do hệ thống áp cố định, người dùng chỉ lọc thêm theo mã phiếu và người tạo; chọn '
            'xong popup tự đóng và form nạp dữ liệu của phiếu.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán kho.\n'
                '3. Người dùng đang ở màn Lập phiếu xuất hàng mượn.',
       chinh='1. Người dùng bấm vào ô Phiếu yêu cầu xuất hàng mượn.\n'
             '2. Hệ thống mở popup “Chọn phiếu yêu cầu xuất hàng mượn”, nạp trang 1 các phiếu Chờ duyệt.\n'
             '3. Người dùng nhập Mã phiếu / chọn Người tạo rồi bấm Tìm kiếm (chọn Người tạo là lọc ngay).\n'
             '4. Người dùng bấm vào dòng phiếu cần chọn.\n'
             '5. Hệ thống đóng popup, điền phiếu vào ô và nạp bảng Chi tiết (mục 2.5).',
       phu='• Không có phiếu Chờ duyệt → bảng hiện “Không có phiếu yêu cầu nào đang chờ duyệt.”.\n'
           '• Bấm Làm mới → xóa 2 ô lọc, nạp lại trang 1.\n'
           '• Máy chủ lỗi → “Không tải được danh sách phiếu yêu cầu” hoặc câu lỗi của máy chủ.\n'
           '• Bấm Đóng / (x) → đóng popup, ô Phiếu yêu cầu giữ giá trị cũ.\n'
           '• Chọn phiếu khác khi đã có phiếu → bảng Chi tiết được thay bằng dữ liệu phiếu mới.',
       dacbiet='Mỗi phiếu xuất chỉ gắn 1 phiếu yêu cầu. Phiếu vừa được duyệt (ở màn này hoặc bởi người khác) không còn trong '
               'popup. Số dòng/trang của popup: 10 / 20 / 50 / 100, tối đa 100.'),
   layout=dict(menu=MENU + ' => Tạo mới => Chọn phiếu yêu cầu', shot=shot('11_picker'),
               shot_caption='Popup Chọn phiếu yêu cầu xuất hàng mượn',
               note='Modal Chọn phiếu yêu cầu xuất hàng mượn được mở ngay trên màn hình Lập phiếu xuất hàng mượn theo '
                    'đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn phiếu yêu cầu xuất hàng mượn”.'),
       ('Dòng mô tả', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Chỉ hiện phiếu đang ở trạng thái Chờ duyệt trong phạm vi Kế toán kho”.'),
       ('Mã phiếu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập mã phiếu”', '- Khớp một phần; áp khi bấm Tìm kiếm / nhấn Enter']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Gợi ý “Chọn người tạo”', '- Mặc định: trống', '- Chọn là lọc ngay']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lọc theo 2 ô, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → xóa 2 ô lọc, nạp lại trang 1.'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Đánh số liên tục theo trang.'),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PYCXHM-NNNNN', '–', 'Hiển thị', '- Mã phiếu yêu cầu Chờ duyệt.'),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- “Họ tên - Mã phòng ban” người lập phiếu yêu cầu.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', '–', 'Hiển thị', '- Ngày lập phiếu yêu cầu.'),
       ('Cột chọn', 'Table/Grid', 'Enable', '–', '–', 'Hiển thị', '- Chữ “Bấm để chọn”; bấm bất kỳ ô nào của dòng là chọn.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- “Không có phiếu yêu cầu nào đang chờ duyệt.”'),
       ('Dòng “Hiển thị a–b / N”, Số dòng/trang, phân trang', 'Pagination', 'Enable', '10, 20, 50, 100', '–', 'Trang 1',
        '- Đổi số dòng → về trang 1.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng popup, không chọn.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Không tải được danh sách phiếu yêu cầu”.'),
   ],
   ev=[
       ('Mở popup', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán kho.\n' + NOQ + '\n'
        'During:\n– Hệ thống áp cố định điều kiện phiếu Chờ duyệt, bất kể tham số gửi lên.\n'
        'After:\n– Hiển thị trang 1 danh sách phiếu Chờ duyệt.'),
       ('Bấm Tìm kiếm / chọn Người tạo', 'Click',
        'Before:\n– Lấy giá trị 2 ô lọc.\nDuring:\n– Lọc trong các phiếu Chờ duyệt.\n' + ERR + '\n'
        'After:\n– Nạp lại trang 1.'),
       ('Bấm vào một dòng', 'Click',
        'Before:\n– Dòng là phiếu Chờ duyệt.\n'
        'During:\n– Nạp phiếu: phiếu đã đổi trạng thái → “Phiếu yêu cầu này không ở trạng thái chờ duyệt hoặc bạn không có '
        'quyền duyệt.”.\n'
        'After:\n– Đóng popup, điền ô Phiếu yêu cầu, nạp bảng Chi tiết; form tính là đã thay đổi.'),
       ('Đổi trang / số dòng', 'Click', 'Before:\n– Giữ 2 ô lọc.\nAfter:\n– Nạp trang mới.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng popup, giữ nguyên form.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Xem chi tiết phiếu', usecase=('FR-07', 'Xem chi tiết phiếu', 'view', A_KT),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu xuất hàng mượn',
       mota='Màn chỉ đọc hiển thị thông tin chung của phiếu, phiếu yêu cầu đã duyệt, các phiếu mượn liên quan, bảng chi tiết '
            'hàng hóa theo từng phiếu mượn (kèm Đơn giá vốn khi có quyền) và khối Lịch sử. Màn không có nút Sửa / Xóa / Duyệt; '
            'chỉ có In và Quay lại.',
       tacnhan=TN_COST,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán kho.\n3. Phiếu tồn tại.',
       chinh='1. Người dùng bấm Mã phiếu ở danh sách.\n'
             '2. Hệ thống kiểm tra quyền Kế toán kho và quyền xem phiếu.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu xuất hàng mượn: <mã>”.\n'
             '4. Hệ thống hiển thị khối Thông tin chung, bảng Chi tiết, dòng Tổng cộng và khối Lịch sử (thu gọn).',
       phu='• Không có quyền / không được xem phiếu → thông báo “Bạn không có quyền thực hiện chức năng này” hoặc “Bạn không '
           'có quyền xem phiếu này”, quay về danh sách.\n'
           '• Phiếu không tồn tại → thông báo lỗi, quay về danh sách.\n'
           '• Không có quyền Xem giá vốn hàng hoá → ẩn cột Đơn giá vốn.\n'
           '• Bấm mã phiếu yêu cầu / mã phiếu mượn → mở màn tương ứng (chip phiếu mượn mở tab mới).\n'
           '• Bấm Quay lại → về danh sách, khôi phục bộ lọc (trong 10 phút).',
       dacbiet='Bảng chi tiết hiện cả dòng hàng có Số lượng 0 (dữ liệu cũ). Thành tiền = Số lượng × Đơn giá bán.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết phiếu xuất hàng mượn'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Chi tiết phiếu xuất hàng mượn: <mã phiếu>”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu yêu cầu xuất hàng mượn', 'Label', 'Read-only', 'PYCXHM-NNNNN', 'Theo dữ liệu',
        '- Chip mã phiếu yêu cầu; bấm → mở chi tiết phiếu yêu cầu.'),
       ('Trạng thái', 'Badge', 'Read-only', 'Danh sách 1 giá trị', 'Đã duyệt', '- Nhãn xanh lá “Đã duyệt”.'),
       ('Người lập phiếu yêu cầu', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Họ tên người mượn lập phiếu yêu cầu.'),
       ('Phòng ban người lập phiếu yêu cầu', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Phòng ban của người lập phiếu yêu cầu.'),
       ('Phiếu xuất mượn', 'Label', 'Read-only', 'PYCXH-…', 'Theo dữ liệu',
        ['- Chip các phiếu mượn của phiếu yêu cầu', '- Bấm chip → mở phiếu mượn ở tab mới']),
       ('Ghi chú', 'Textarea', 'Disable', '0–255 ký tự', 'Theo dữ liệu', '- Trống nếu không nhập.'),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng hóa (Model / Mã / Thương hiệu), Đơn vị tính, Đơn giá bán, Số lượng',
         '- Chi tiết: Phiếu mượn (liên kết), Xuất', '- Thành tiền = Số lượng × Đơn giá bán']),
       ('Cột Đơn giá vốn', 'Table/Grid', 'Read-only', '≥ 0', 'Ẩn khi thiếu quyền',
        '- Chỉ hiện với quyền Xem giá vốn hàng hoá.'),
       ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu', '- Tổng Số lượng và tổng Thành tiền.'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        '- Nút Xem lịch sử mở rộng khối; nội dung như mục 2.10.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → cửa sổ Xem trước phiếu (mục 2.8).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra quyền Kế toán kho và quyền xem phiếu.\n' + NOQ + '\n'
        'During:\n– Lấy dữ liệu phiếu; ẩn giá vốn khi thiếu quyền Xem giá vốn hàng hoá.\n'
        '– Lỗi → thông báo câu của máy chủ hoặc “Không tải được chi tiết phiếu.”, quay về danh sách.\n'
        'After:\n– Hiển thị màn chỉ đọc.'),
       ('Bấm Xem lịch sử', 'Click',
        'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, nạp các mốc lịch sử (lần đầu).'),
       ('Bấm chip / liên kết phiếu', 'Click',
        'Before:\n– Có mã phiếu.\nAfter:\n– Mở màn chi tiết phiếu yêu cầu / phiếu mượn.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Không có dữ liệu cần lưu.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'In phiếu và in danh sách', usecase=('FR-08', 'In phiếu / In danh sách', 'io', A_KT),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu xuất hàng mượn / In danh sách',
       mota='Xem trước và in một phiếu (khổ dọc, có chỗ ký Người lập – Kế toán kho – Thủ kho) hoặc in danh sách theo bộ lọc '
            'đang áp. Bản in mở trong cửa sổ ngay trên màn đang đứng, không mở tab mới nên không mất bộ lọc.',
       tacnhan=TN_COST, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động hoặc ở màn chi tiết (in phiếu), hoặc nút In trên bảng (in danh sách).\n'
             '2. Hệ thống kiểm tra quyền Kế toán kho.\n'
             '3. Hệ thống mở cửa sổ xem trước, hiện “Đang tải dữ liệu in…” trong lúc dựng bản in.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Danh sách khớp bộ lọc quá 2.000 phiếu → không dựng bản in, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.\n'
           '• Không có quyền → “Bạn không có quyền thực hiện chức năng này”.\n'
           '• Lỗi khác → “Không tải được dữ liệu in” hoặc câu lỗi của máy chủ.\n'
           '• Bấm (x) → đóng cửa sổ xem trước.',
       dacbiet='Logo / tên công ty đầu bản in phiếu lấy theo công ty của phiếu yêu cầu được duyệt (phiếu xuất không có công '
               'ty riêng); bản in danh sách lấy theo công ty của người đang xem. Cột Đơn giá vốn chỉ in khi có quyền Xem giá '
               'vốn hàng hoá.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   extra=[(shot('19_printlist'), 'Cửa sổ Xem trước danh sách phiếu xuất hàng mượn')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–',
        ['- In phiếu: “Xem trước phiếu <mã>”', '- In danh sách: “Xem trước danh sách phiếu xuất hàng mượn”']),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị',
        ['- Cạnh tiêu đề; bấm → hộp thoại in của trình duyệt', '- Ẩn khi danh sách vượt 2.000 dòng']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ xem trước.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…”.'),
       ('Đầu bản in phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Logo, tên công ty của phiếu yêu cầu', '- “PHIẾU XUẤT HÀNG MƯỢN”, Số phiếu, Ngày tạo']),
       ('Thông tin phiếu trên bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Người lập, Phiếu yêu cầu, Người yêu cầu, Phòng ban yêu cầu', '- Phiếu xuất mượn, Ghi chú, Trạng thái']),
       ('Bảng hàng trên bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng hóa, ĐVT, Đơn giá bán, Đơn giá vốn (khi có quyền), Số lượng',
         '- Chi tiết theo phiếu mượn: Phiếu mượn, Xuất', '- Dòng Tổng cộng; số dạng 1,234,567']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- Người lập, Kế toán kho, Thủ kho (Ký, họ tên).'),
       ('Bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        ['- Tiêu đề “DANH SÁCH PHIẾU XUẤT HÀNG MƯỢN”, khoảng thời gian (khi lọc Ngày tạo), Tổng số phiếu',
         '- Cột: STT, Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người lập, Ngày lập, Trạng thái']),
       ('Dòng nhắc vượt trần in', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        '- Nhắc danh sách vượt mức in tối đa 2,000 dòng, thu hẹp bộ lọc hoặc dùng Xuất Excel.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Bạn không có quyền thực hiện chức năng này”', '- “Không tải được dữ liệu in”']),
   ],
   ev=[
       ('Bấm In (phiếu)', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán kho và quyền xem phiếu.\n' + NOQ + '\n'
        'During:\n– Lỗi dựng bản in → “Không tải được dữ liệu in”.\n'
        'After:\n– Dựng bản xem trước phiếu khổ dọc, letterhead theo công ty của phiếu yêu cầu.'),
       ('Bấm In (danh sách)', 'Click',
        'Before:\n– Lấy bộ lọc đang áp.\n' + NOQ + '\n'
        'During:\n– Lấy phiếu theo bộ lọc; quá 2.000 dòng → hiện dòng nhắc, ẩn bản in và nút In.\n'
        'After:\n– Dựng bản xem trước danh sách.'),
       ('Bấm In trong cửa sổ xem trước', 'Click', 'Before:\n– Bản in đã dựng xong.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, giữ nguyên màn đang đứng.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'Xuất danh sách ra Excel', usecase=('FR-09', 'Xuất Excel', 'io', A_KT),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ phiếu khớp bộ lọc đang áp (không phân trang) ra file Excel. Cột STT '
            'luôn đứng đầu file; cuối file có khối ký “Người lập”.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 9 trường, tích sẵn tất cả.\n'
             '3. Người dùng tích trường cần xuất, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy toàn bộ phiếu theo bộ lọc, dựng file theo đúng thứ tự trường đã chọn.\n'
             '5. Hệ thống tải file “danh_sach_phieu_xuat_hang_muon.xlsx”, đóng cửa sổ, báo “Xuất Excel thành công”.',
       phu='• Không có phiếu khớp → vẫn xuất file có tiêu đề, dòng tên cột và khối ký.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”, cửa sổ giữ nguyên.\n'
           '• Không có quyền → “Bạn không có quyền thực hiện chức năng này”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng. Nút Xuất Excel bị khóa trong lúc đang xuất. Mã phiếu và ngày giữ dạng chữ để Excel '
               'không tự đổi định dạng.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 9 trường', 'Ít nhất 1', 'Tích tất cả',
        ['- Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người tạo, Ngày tạo',
         '- Trạng thái, Ghi chú, Người cập nhật, Ngày cập nhật']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        '- Rê chuột: “Kéo để đổi vị trí cột trong file”.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/9 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file Excel', '- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Nội dung file Excel', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Dòng tiêu đề “DANH SÁCH PHIẾU XUẤT HÀNG MƯỢN”', '- Dòng “Từ ngày … đến ngày …” khi có lọc Ngày tạo',
         '- Dòng tên cột: STT + các trường đã chọn', '- Khối ký cuối file: “Ngày…Tháng…Năm…”, “Người lập”, “(Ký, họ tên)”']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công”', '- Thất bại: “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ, tích sẵn 9 trường theo thứ tự thiết kế.'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Kéo bằng biểu tượng của trường.\nAfter:\n– Đổi thứ tự trường; đây là thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán kho.\n' + NOQ + '\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc, không phân trang.\n– Lỗi → “Lỗi khi xuất Excel”.\n' + ERR + '\n'
        'After:\n– Tải file “danh_sach_phieu_xuat_hang_muon.xlsx”, đóng cửa sổ, báo “Xuất Excel thành công”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Xem các mốc thao tác của phiếu: người thực hiện, thời điểm và nội dung. Vì phiếu không sửa / xóa / đổi trạng thái '
            'được, thực tế chỉ có mốc “Tạo mới” ghi lúc lưu phiếu (kèm mã phiếu yêu cầu, ghi chú và bảng hàng — không ghi '
            'đơn giá vốn). Cửa sổ ở danh sách và khối Lịch sử ở màn chi tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động, hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n'
             '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <mã phiếu>” và nạp các mốc của phiếu.\n'
             '3. Hệ thống hiển thị các mốc, mới nhất ở trên.',
       phu='• Phiếu lập trước khi có chức năng lịch sử (chuyển từ hệ thống cũ) → “Chưa có lịch sử thao tác nào.”.\n'
           '• Bấm Bộ lọc → mở các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; danh sách giữ nguyên trang, bộ lọc, sắp xếp.',
       dacbiet='Mốc duyệt phiếu yêu cầu do phiếu này gây ra được ghi ở lịch sử của PHIẾU YÊU CẦU, không ghi lặp ở đây. Xem, in, '
               'xuất Excel không ghi mốc. Giá vốn không bao giờ được ghi vào lịch sử.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('17c_detail_history'), 'Khối Lịch sử ở màn chi tiết phiếu'),
          (shot('16b_history_empty'), 'Phiếu chưa có lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <mã phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Tạo mới: Ghi chú, Phiếu yêu cầu, bảng hàng (Mã hàng hóa, Đơn vị tính, Đơn giá bán, số lượng) và chi tiết theo '
           'phiếu mượn', '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách người đã thao tác', 'Trống', '- Chọn là lọc ngay.'),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc đến hết ngày này.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', '- Xóa điều kiện lọc.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Chưa có mốc: “Chưa có lịch sử thao tác nào.”', '- Lọc không ra: “Không có lịch sử phù hợp bộ lọc.”']),
       ('Khối Lịch sử ở màn chi tiết', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        ['- Nút Xem lịch sử / Thu gọn, nút Làm mới, nút Bộ lọc', '- Cùng nội dung với cửa sổ']),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click',
        'Before:\n– Người dùng có quyền Kế toán kho.\n'
        'During:\n– Nạp các mốc lịch sử; chưa có mốc → “Chưa có lịch sử thao tác nào.”.\n'
        'After:\n– Hiển thị các mốc, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm: chọn là lọc.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Khối lọc đang mở.\nAfter:\n– Xóa điều kiện lọc, hiện lại đủ các mốc.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; danh sách giữ nguyên trang và bộ lọc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu xuất hàng mượn; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Vai trò sử dụng duy nhất', [
        '– Mọi chức năng (xem, lập, in, xuất, lịch sử) chỉ dành cho quyền Kế toán kho; Super admin được coi như có quyền.',
        '– Không phân phạm vi theo công ty / phòng ban: Kế toán kho thấy mọi phiếu.',
        '– Quyền kiểm tra ở máy chủ ở từng thao tác, không dựa vào việc ẩn nút.'],
     ['Xem danh sách', 'Xem chi tiết', 'Lập phiếu', 'In', 'Xuất Excel', 'Lịch sử']),
    ('BR-02', 'Phiếu yêu cầu được chọn', [
        '– Chỉ phiếu yêu cầu xuất hàng mượn ở trạng thái Chờ duyệt; điều kiện áp cố định ở máy chủ.',
        '– Mỗi phiếu xuất gắn đúng 1 phiếu yêu cầu; phiếu yêu cầu đã duyệt không chọn lại được.',
        '– Máy chủ kiểm tra lại lúc nạp và lúc lưu (“Không thể duyệt yêu cầu này!”).'], ['Lập phiếu', 'Chọn phiếu yêu cầu']),
    ('BR-03', 'Số lượng Xuất', [
        '– Mọi ô Xuất phải > 0 (“Phải lớn hơn 0”), tối đa 6 chữ số.',
        '– Không vượt Đang mượn = đã xuất − đã trả − phần đang chờ ở phiếu khác (trừ chính phiếu yêu cầu đang duyệt), quy '
        'theo hệ số đơn vị, làm tròn xuống.',
        '– Máy chủ tính lại Đang mượn ngay trong lúc lưu; vượt → “Số lượng không hợp lệ”, không lưu gì.',
        '– Ô Xuất điền sẵn số người lập đề nghị; dòng hàng không có phiếu mượn không nhập được.'], ['Lập phiếu']),
    ('BR-04', 'Vòng đời phiếu', [
        '– Lưu là sinh phiếu ở trạng thái Đã duyệt; không có nháp, gửi duyệt, không duyệt, hủy.',
        '– Không có Sửa / Xóa / Khóa ở bất kỳ phiếu nào; ô lọc Trạng thái chỉ có Đã duyệt.',
        '– Điều kiện xóa: không áp dụng (màn không có chức năng Xóa).'], ['Lập phiếu', 'Xem danh sách']),
    ('BR-05', 'Ghi ngược khi lưu', [
        '– Phiếu yêu cầu: số Được duyệt = số Xuất từng dòng; trạng thái Chờ duyệt → Đã duyệt, ghi người duyệt, ngày duyệt.',
        '– Phiếu mượn gốc: cộng số Xuất (quy về đơn vị gốc) vào số đã trả; phiếu mượn không còn dòng nợ → trạng thái mượn '
        'Đã trả.',
        '– Toàn bộ trong một lần lưu trọn gói: lỗi giữa chừng thì không ghi gì.'], ['Lập phiếu']),
    ('BR-06', 'Tính duy nhất và chống trùng', [
        '– Phiếu không có trường nhập duy nhất; mã PXHM-NNNNN tự sinh tăng dần (giữ dãy mã của hệ thống cũ), không sửa được.',
        '– Một phiếu yêu cầu chỉ có 1 phiếu xuất; hai Kế toán kho cùng lưu thì người sau bị chặn.',
        '– Nút lưu khóa trong lúc lưu để một lần bấm không tạo 2 phiếu.'], ['Lập phiếu']),
    ('BR-07', 'Chuẩn hóa dữ liệu nhập', [
        '– Ghi chú tối đa 255 ký tự, không chặn ký tự đặc biệt, hiển thị nguyên văn.',
        '– Ô Xuất chỉ nhận chữ số, hiển thị dấu phẩy ngăn nghìn.',
        '– Tìm kiếm / lọc chữ khớp một phần, không phân biệt hoa / thường.'], ['Lập phiếu', 'Tìm kiếm và lọc']),
    ('BR-08', 'Liên kết cấp cha – con', [
        '– Phiếu > dòng hàng (hàng + đơn vị) > dòng chi tiết theo phiếu mượn của phiếu yêu cầu.',
        '– Tên hàng, mã, model, thương hiệu, đơn vị, hệ số, đơn giá bán lưu cố định từ phiếu yêu cầu lúc lập.',
        '– Đơn giá vốn của dòng = giá vốn bình quân của phần hàng xuất theo các phiếu mượn.'], ['Lập phiếu', 'Xem chi tiết']),
    ('BR-09', 'Giá vốn là dữ liệu nhạy cảm', [
        '– Đơn giá vốn chỉ trả về và hiển thị khi có quyền Xem giá vốn hàng hoá (màn chi tiết, bản in phiếu).',
        '– Không xuất giá vốn ra Excel danh sách và không ghi vào lịch sử.'], ['Xem chi tiết', 'In', 'Lịch sử']),
    ('BR-10', 'Thông báo', [
        '– Lưu phiếu → gửi “[YCXHM] Đã duyệt: <mã phiếu yêu cầu>” (người duyệt, phiếu xuất) cho người lập phiếu yêu cầu.',
        '– Bấm thông báo → mở chi tiết phiếu yêu cầu.'], ['Lập phiếu']),
    ('BR-11', 'In và xuất', [
        '– Bản in phiếu lấy letterhead theo công ty của phiếu yêu cầu; bản in danh sách theo công ty người xem.',
        '– Bản in danh sách tối đa 2.000 dòng; Xuất Excel không giới hạn, không có phiếu vẫn ra file có tiêu đề và tên cột.'],
     ['In', 'Xuất Excel']),
    ('BR-12', 'Sử dụng ở màn khác', [
        '– Số đã trả của phiếu mượn tăng → số còn mượn giảm ở Danh sách hàng mượn, Hàng sắp hết hạn mượn, Yêu cầu / Phiếu '
        'xuất bán hàng mượn, Phiếu yêu cầu gia hạn hàng mượn, Yêu cầu xuất hàng mượn.',
        '– Phiếu yêu cầu đã duyệt không còn hiện nút Tạo phiếu xuất hàng mượn / Từ chối.'], ['Lập phiếu']),
    ('BR-13', 'Quy tắc ghi lịch sử', [
        '– Ghi mốc “Tạo mới” cho phiếu xuất (ghi chú, phiếu yêu cầu, bảng hàng, chi tiết phiếu mượn); mốc “Duyệt” ghi ở '
        'phiếu yêu cầu.', '– Xem, in, xuất Excel không ghi; hiển thị mới nhất ở trên.'], ['Lập phiếu', 'Lịch sử']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Phiếu xuất hàng mượn (phiếu, dòng hàng, số Xuất theo từng phiếu mượn).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Tài chính', 'Yêu cầu xuất hàng mượn (nút Tạo phiếu xuất hàng mượn mở màn Lập; lưu phiếu xuất ghi ngược số Được '
                       'duyệt, người duyệt, ngày duyệt và trạng thái Đã duyệt về phiếu yêu cầu)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Mượn hàng'),
    ('2', 'Tài chính', 'Yêu cầu xuất hàng (phiếu xuất mượn gốc: cộng số đã trả, chuyển trạng thái mượn Đã trả khi trả hết)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('3', 'Tài chính', 'Danh sách hàng mượn (số còn mượn giảm theo số Xuất)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Mượn hàng'),
    ('4', 'Tài chính', 'Hàng sắp hết hạn mượn (phiếu mượn trả hết không còn cảnh báo)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Mượn hàng'),
    ('5', 'Tài chính', 'Yêu cầu xuất bán hàng mượn (số còn mượn được phép xuất bán giảm)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Mượn hàng'),
    ('6', 'Tài chính', 'Phiếu xuất bán hàng mượn (số còn mượn được phép xuất bán giảm)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Mượn hàng'),
    ('7', 'Tài chính', 'Phiếu yêu cầu gia hạn hàng mượn (số còn mượn để gia hạn giảm)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Mượn hàng'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
