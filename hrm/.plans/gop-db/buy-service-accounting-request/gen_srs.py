# -*- coding: utf-8 -*-
"""SRS màn "Yêu cầu hạch toán mua dịch vụ" (mã <mã công ty>.YCHTMDV.<năm><6 số>) — form chuẩn Danh mục quốc gia (03/11/2026).

Chạy: python gen_srs.py  → SRS - Yêu cầu hạch toán mua dịch vụ.docx
Khung: srs-documenter (SrsDoc) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc: ../finance-addition-accounting-request/gen_srs.py.
Nguồn đọc 03/11/2026 (nhánh develop, cả 2 repo):
  BE  Modules/Finance/{Entities/BuyServiceAccountingRequest/*, Services/BuyServiceAccountingRequest{,Notify}Service.php,
      Http/Controllers/V1/BuyServiceAccountingRequestController.php, Http/Requests/BuyServiceAccountingRequest/*,
      Transformers/BuyServiceAccountingRequestResource/*, Services/BuyServiceAccountingService.php (đổi trạng thái phiếu yêu cầu)},
      app/ExcelExport/{ExportColumnRegistry,DynamicExport}.php, app/Services/CatalogHistoryService.php, PermissionsTableSeeder (4 quyền).
  FE  pages/finance/buy-service-accounting-requests/** (index, create, _id/index, _id/edit, components/{BuyServiceAccountingRequestForm,
      ServiceDetailTable, InsuranceSection, SourcePickerModal}), buy-service-requests/components/CommentModal.vue,
      bill-payment-requests/components/AttachmentSection.vue, components/subsystem-menu/{sale-hub,finance}.js.
  Spec docs/superpowers/specs/gop-db/2026-10-12-buy-service-accounting-request-design.md + plan.md (fix #11699…#11710) — code thắng khi lệch.
Ảnh: ./ychtmdv_shots (dev-hrm 03/11/2026, DNS Admin, script ychtmdv_shots/_capture/capture.js). Dev không có phiếu Đang tạo / Không duyệt
  của DNS Admin → ảnh nút Sửa / Xóa, màn Sửa, hộp Xác nhận xóa chụp trên phiếu Không duyệt TPE.YCHTMDV.2026000045 với cờ is_can_edit /
  is_can_delete bật tạm trên trình duyệt (không ghi dữ liệu). Dev không có đơn bảo hiểm → popup Chọn đơn bảo hiểm chụp ở trạng thái rỗng.
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

TEN = 'Yêu cầu hạch toán mua dịch vụ'
SHOTS = os.path.join(HERE, 'ychtmdv_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Bán hàng => Yêu cầu => Mua dịch vụ => YC hạch toán mua dịch vụ'
MENU_TC = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mua dịch vụ => Yêu cầu hạch toán mua dịch vụ'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Yêu cầu hạch toán mua dịch vụ.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_LAP = 'Người lập phiếu'
A_KT = 'Kế toán hạch toán'
Q_HT = 'Hạch toán mua dịch vụ'
TN_MOI = ('Người dùng có quyền thực hiện chức năng: Người lập phiếu — chức năng không gắn quyền riêng, mọi nhân viên vào được '
          'màn danh sách đều lập được phiếu của mình.')
TN_XEM = ('Người dùng có quyền thực hiện chức năng: Người lập phiếu (phiếu của mình); người có một trong các quyền Xem yêu cầu '
          'hạch toán mua dịch vụ - theo tổng công ty, - theo công ty, - theo phòng ban (theo phạm vi ở Phần 2); người có quyền '
          'Hạch toán mua dịch vụ (phiếu Chờ duyệt cùng công ty và phiếu mình đã xử lý).')
TN_SUA = 'Người dùng có quyền thực hiện chức năng: Người lập phiếu (chỉ chính người tạo phiếu, không cần quyền riêng).'
TN_KT = ('Người dùng có quyền thực hiện chức năng: Hạch toán mua dịch vụ (phiếu Chờ duyệt thuộc cùng công ty với người dùng; '
         'tài khoản Super admin cũng phải được gán quyền này).')
DK_XEM = ('1. Người dùng đăng nhập thành công.\n'
          '2. Người dùng có quyền xem phiếu theo phạm vi ở Phần 2 (không có quyền nào thì chỉ thấy phiếu mình tạo).\n'
          '3. Người dùng đang ở màn danh sách Yêu cầu hạch toán mua dịch vụ.')
DK_SUA = ('1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo phiếu.\n'
          '3. Phiếu đang ở trạng thái Đang tạo (mới lưu nháp) hoặc Không duyệt (kế toán trả về).')
DK_KT = ('1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Hạch toán mua dịch vụ và cùng công ty với phiếu.\n'
         '3. Phiếu đang ở trạng thái Chờ duyệt.')

M_REQ = '“<Tên trường> – Bắt buộc phải nhập”'
M_CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
M_NOPERM = '“Bạn không có quyền thực hiện chức năng này”'
TOAST_422 = '“Bạn chưa nhập đầy đủ thông tin.”'
DEL_MSG = '“Bạn có chắc muốn xóa bản ghi này không?”'
UNSAVED = ['- Tiêu đề “Thông tin chưa lưu”', '- Nội dung “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”',
           '- Nút Thoát: bỏ thay đổi, rời màn', '- Nút Ở lại: đóng hộp, giữ nguyên dữ liệu đang nhập']
STATUS_LIST = ['- Đang tạo: nhãn xám', '- Chờ duyệt: nhãn vàng', '- Đang hạch toán: nhãn vàng', '- Đã hạch toán: nhãn xanh',
               '- Không duyệt: nhãn đỏ']
NOTI_SEND = ('“[YCHTMDV] Chờ duyệt: <số phiếu>” tới người có quyền Hạch toán mua dịch vụ cùng công ty với phiếu, kèm người gửi, '
             'loại yêu cầu, nhà cung cấp, số hợp đồng, tổng thanh toán, ghi chú')

d = SrsDoc(out=OUT, menu=MENU, route='/finance/buy-service-accounting-requests', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Bán hàng': 'menu_phanhe_banhang', 'Yêu cầu': 'menu_yeucau', 'Mua dịch vụ': 'menu_nhom_muadv',
    'YC hạch toán mua dịch vụ': 'menu_muc_sale',
    'Phân hệ Tài chính': 'menu_phanhe_taichinh', 'Hàng hoá - Dịch vụ - Vận chuyển': 'menu_hhdvvc',
    'Yêu cầu hạch toán mua dịch vụ': 'menu_muc_tc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Hạch toán': 'btn_hachtoan_row',
    'Không duyệt': 'btn_khongduyet_row', 'In phiếu': 'item_in', 'In danh sách': 'btn_indanhsach', 'Xuất Excel': 'btn_xuatexcel',
    'Lịch sử': 'item_lichsu',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None, extra=None):
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event.
    extra: [(ảnh, chú thích)] — ảnh trạng thái đặc biệt / popup phụ, đặt ngay sau ảnh chính của Layout."""
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
    for png, cap in (extra or []):
        d.figure(shot(png), cap, width_in=6.2)
    k += 1
    assert ui and ev, 'Thiếu bảng giao diện / event ở 2.%d' % no
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (no, k))
    d.ui_table(split_ui_rows(ui, UI_OVER, UI_EXPLICIT), **(ui_kw or {}))
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (no, k))
    d.event_table(ev)


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.h2('Mục lục')
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Yêu cầu hạch toán mua dịch vụ (số phiếu dạng <mã công ty>.YCHTMDV.'
    '<năm><6 chữ số>, vd TPE.YCHTMDV.2026000069), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ 2 loại yêu cầu (Dịch vụ thuê ngoài, Công nợ bảo hiểm) và nguồn dữ liệu của từng loại (hợp đồng mua dịch vụ, đơn '
    'bảo hiểm).',
    'Làm rõ cách tính số lượng còn được hạch toán của hợp đồng và vai trò của kế toán (Hạch toán / Không duyệt).',
])
d.p('Phạm vi chức năng (14 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Danh sách: Xem danh sách (2 lối vào: Bán hàng, Tài chính), Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột.',
    'Phiếu của người lập: Lập phiếu (Lưu nháp / Lưu và gửi duyệt / Lưu và tiếp tục), Chọn hợp đồng mua dịch vụ / đơn bảo hiểm, '
    'Chỉnh sửa, Xóa.',
    'Xem: Xem chi tiết, In phiếu và In danh sách, Xuất Excel danh sách, Xem lịch sử thay đổi.',
    'Xử lý của kế toán: Hạch toán (thay cho thao tác Duyệt — mở màn Tạo phiếu hạch toán mua dịch vụ) và Không duyệt.',
    'Không thuộc màn này: không có Khóa / Mở khóa, không có Import Excel, không có Xuất Excel một phiếu; nội dung màn Tạo phiếu '
    'hạch toán mua dịch vụ theo SRS màn Hạch toán mua dịch vụ.',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phiếu là chứng từ đề nghị kế toán ghi nhận công nợ phải trả nhà cung cấp dịch vụ thuê ngoài / công ty bảo hiểm.',
    'Dịch vụ, đơn giá, yêu cầu mua dịch vụ và số lượng lấy từ hợp đồng mua dịch vụ đã duyệt; số lượng hạch toán của phiếu '
    'giữ chỗ trên hợp đồng để không hạch toán vượt.',
    'Phiếu Chờ duyệt là nguồn để kế toán lập phiếu Hạch toán mua dịch vụ; trạng thái, Người duyệt, Ngày duyệt theo dõi tiến độ.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Lưu nháp chỉ bắt buộc Loại yêu cầu; Lưu và gửi duyệt bắt buộc đủ trường theo loại và tổng SL hạch toán > 0 (loại Dịch vụ '
    'thuê ngoài).',
    'SL hạch toán từng yêu cầu không được âm, không vượt SL hợp đồng còn lại (áp cả khi lưu nháp).',
    'Chỉ người tạo được Sửa / Xóa, và chỉ khi phiếu Đang tạo hoặc Không duyệt; xóa là xóa hẳn.',
    'Không duyệt bắt buộc ghi chú; Hạch toán / Không duyệt chỉ cho người có quyền Hạch toán mua dịch vụ cùng công ty với phiếu.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu yêu cầu hạch toán mua dịch vụ', 'Phiếu đề nghị kế toán hạch toán chi phí mua dịch vụ; số phiếu do hệ thống sinh dạng '
                                            '<mã công ty>.YCHTMDV.<năm><6 chữ số>.'),
    ('Loại yêu cầu', 'Dịch vụ thuê ngoài (lập từ hợp đồng mua dịch vụ) · Công nợ bảo hiểm (lập từ đơn bảo hiểm).'),
    ('Hợp đồng mua dịch vụ', 'Hợp đồng đã duyệt do chính người lập tạo; quy định dịch vụ, đơn giá, VAT và số lượng chia cho '
                             'từng yêu cầu mua dịch vụ.'),
    ('Yêu cầu mua dịch vụ', 'Phiếu yêu cầu gốc (màn Yêu cầu mua dịch vụ) mà hợp đồng phân bổ số lượng cho.'),
    ('SL HĐ còn lại', 'SL của dòng phân bổ trên hợp đồng − SL đã hạch toán − SL các phiếu yêu cầu khác đang giữ (Đang tạo, Chờ '
                      'duyệt, Đang hạch toán); không âm.'),
    ('SL hạch toán', 'Số lượng đề nghị hạch toán cho từng yêu cầu mua dịch vụ; ô nhập duy nhất của bảng dịch vụ.'),
    ('Đơn bảo hiểm', 'Đơn bảo hiểm nguyên tắc đã duyệt (kèm phụ lục bổ sung, hợp đồng mua) — nguồn của loại Công nợ bảo hiểm.'),
    ('Hóa đơn VAT', 'Kèm hóa đơn (bắt buộc đính kèm file khi gửi duyệt, VAT % lấy theo hợp đồng) · Không kèm hóa đơn (VAT = 0).'),
    ('Tổng thanh toán', 'Dịch vụ thuê ngoài: Thành tiền + VAT; Công nợ bảo hiểm: Tổng sau thuế của đơn bảo hiểm.'),
    ('Trạng thái Đang tạo', 'Phiếu mới lưu nháp. Người tạo sửa / xóa / gửi duyệt được. Nhãn xám.'),
    ('Trạng thái Chờ duyệt', 'Đã gửi, chờ kế toán Hạch toán hoặc Không duyệt. Không sửa / xóa được. Nhãn vàng.'),
    ('Trạng thái Đang hạch toán', 'Kế toán đã lưu nháp phiếu Hạch toán mua dịch vụ lập từ phiếu này. Nhãn vàng.'),
    ('Trạng thái Đã hạch toán', 'Phiếu Hạch toán mua dịch vụ đã duyệt (ghi sổ). Trạng thái cuối. Nhãn xanh.'),
    ('Trạng thái Không duyệt', 'Kế toán trả về kèm Ghi chú duyệt; người tạo sửa / xóa / gửi duyệt lại được. Nhãn đỏ.'),
    ('Người duyệt / Ngày duyệt', 'Kế toán đã Không duyệt phiếu, hoặc đã duyệt phiếu Hạch toán lập từ phiếu này, và thời điểm đó.'),
    ('Ghi chú duyệt', 'Lý do Không duyệt gần nhất của kế toán.'),
    ('Cấu trúc phân cấp', 'Phiếu > dòng dịch vụ (theo dịch vụ của hợp đồng) > dòng yêu cầu mua dịch vụ (SL hạch toán); phiếu > '
                          'danh sách file đính kèm; loại Công nợ bảo hiểm không có dòng dịch vụ, chỉ có 1 dòng bảo hiểm.'),
    ('NCC / HĐ / ĐVT', 'Nhà cung cấp / Hợp đồng / Đơn vị tính.'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Lập phiếu không cần quyền riêng. Sửa / Xóa: chỉ người tạo phiếu, khi phiếu Đang tạo hoặc Không duyệt. 4 quyền của màn thuộc '
    'nhóm quyền “Yêu cầu hạch toán mua dịch vụ” (phân hệ Bán hàng).')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q_HT, 'Thấy thêm phiếu Chờ duyệt cùng công ty và phiếu mình đã xử lý; với phiếu Chờ duyệt cùng công ty: Hạch toán, Không '
                 'duyệt; nhận thông báo khi có phiếu gửi duyệt cùng công ty.'),
], widths=[0.8, 1.6, 3.6])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét từ trên xuống, có cấp nào áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem yêu cầu hạch toán mua dịch vụ - theo tổng công ty', 'Toàn bộ phiếu; có ô lọc Công ty. Tài khoản Super admin xem như V1.'),
    ('V2', 'Xem yêu cầu hạch toán mua dịch vụ - theo công ty', 'Phiếu thuộc công ty của người dùng.'),
    ('V3', 'Xem yêu cầu hạch toán mua dịch vụ - theo phòng ban', 'Phiếu thuộc phòng ban người dùng quản lý hoặc đang làm việc.'),
    ('—', '(không có quyền nào)', 'Phiếu mình tạo.'),
], widths=[0.8, 2.4, 2.8])
d.p('Mọi cấp: phiếu Đang tạo của người khác bị ẩn. Q1 cộng thêm (không thay thế) phạm vi V1–V3.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người tạo', 'Q1', 'V1–V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅ (+ Chờ duyệt cùng công ty)', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu', '✅', '✅', '✅', '✅'),
    ('FR-06 Chọn hợp đồng / đơn bảo hiểm', '✅ (HĐ do mình tạo)', '✅', '✅', '✅'),
    ('FR-07 Chỉnh sửa', '✅ (Đang tạo, Không duyệt)', '❌', '❌', '❌'),
    ('FR-08 Xóa', '✅ (Đang tạo, Không duyệt)', '❌', '❌', '❌'),
    ('FR-09 Xem chi tiết', '✅', '✅', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-10 Hạch toán', '❌', '✅ (Chờ duyệt, cùng công ty)', '❌', '❌'),
    ('FR-11 Không duyệt', '❌', '✅ (Chờ duyệt, cùng công ty)', '❌', '❌'),
    ('FR-12 In phiếu / In danh sách', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-13 Xuất Excel', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-14 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[2.1, 1.2, 1.3, 0.9, 1.0])
d.p('Màn không có Khóa / Mở khóa và Import Excel nên ma trận không có cột quyền tương ứng. In, Xuất Excel, Xem lịch sử không gắn '
    'quyền riêng: ai xem được phiếu thì dùng được.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có quyền xem nào: chỉ thấy phiếu do mình tạo; ô lọc Công ty / Phòng ban bị ẩn.',
    'Nút không đủ điều kiện thì ẩn hẳn, không hiện xám (cờ do máy chủ trả theo từng phiếu).',
    'Mở thẳng đường dẫn màn chi tiết / sửa của phiếu ngoài phạm vi hoặc không tồn tại → chuyển sang trang “không tìm thấy”; mở màn '
    'Sửa của phiếu không sửa được → tự chuyển sang màn chi tiết.',
    'Gọi thẳng chức năng bỏ qua giao diện → máy chủ từ chối: “Bạn không có quyền sửa phiếu này”, “Bạn không có quyền xóa phiếu '
    'này”, “Bạn không có quyền xem phiếu này”, ' + M_NOPERM + ' (Không duyệt khi thiếu quyền Q1), “Bạn không có quyền thao tác '
    'trên phiếu này” (Không duyệt phiếu khác công ty); phiếu sai trạng thái → ' + M_CONFLICT + '.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Nút / thao tác', 'Hiện khi', 'Vị trí'], [
    ('Tạo mới, Xuất Excel, In danh sách, Cấu hình cột', 'Luôn hiện', 'Thanh công cụ của bảng'),
    ('Sửa, Xóa', 'Người đăng nhập là người tạo và phiếu Đang tạo / Không duyệt', 'Cột Hành động, chân màn chi tiết'),
    ('Hạch toán, Không duyệt', 'Phiếu Chờ duyệt, người có quyền Q1 cùng công ty với phiếu', 'Cột Hành động, chân màn chi tiết'),
    ('In phiếu, Lịch sử', 'Luôn hiện với phiếu xem được', 'Cột Hành động (vào nút “…” khi dòng có hơn 3 nút); màn chi tiết'),
    ('Lưu nháp, Lưu và gửi duyệt', 'Màn Tạo, màn Sửa', 'Chân màn'),
    ('Lưu và tiếp tục', 'Chỉ màn Tạo', 'Chân màn'),
], widths=[1.6, 3.0, 1.8])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_LAP, [0, 1, 2, 3, 6, 7]), (A_KT, [0, 4, 5, 6, 7])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu', 'crud'),
     ('FR-07', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-08', 'Xóa phiếu', 'action'),
     ('FR-10', 'Hạch toán', 'action'),
     ('FR-11', 'Không duyệt', 'action'),
     ('FR-12', 'In phiếu', 'io'),
     ('FR-13', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-09', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-14', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn hợp đồng / đơn bảo hiểm', 'crud', 'extend', [1, 2], None)],
    'Sơ đồ Use Case tổng quan màn Yêu cầu hạch toán mua dịch vụ')

d.h2('2 Đặc tả chi tiết từng chức năng')


# ------------------------------------------------------------ Form Tạo / Sửa (dùng chung 2.5 + 2.7)
def form_ui(edit):
    rows = [
        ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–',
         '“Sửa phiếu yêu cầu hạch toán mua dịch vụ: <số phiếu>”' if edit else '“Tạo phiếu yêu cầu hạch toán mua dịch vụ”',
         ['- Cũng là tiêu đề tab trình duyệt',
          '- Màn Sửa ghép số phiếu sau khi nạp xong phiếu' if edit else '- Không có ô Số phiếu: số phiếu sinh khi lưu',
          '- Trong lúc nạp phiếu hiện “Đang tải dữ liệu phiếu...”' if edit else '- Không hiện nhãn trạng thái']),
        ('Dòng người tạo', 'Label', 'Read-only', '–', '–',
         'Người tạo – ngày giờ tạo' if edit else 'Người đăng nhập – thời điểm hiện tại',
         ['- Góc phải tiêu đề khối Thông tin chung', '- Không sửa được']),
        ('Loại yêu cầu', 'Dropdown', 'Enable' if not edit else 'Disable', 'Danh sách 2 giá trị', 'Có',
         'Theo phiếu' if edit else 'Dịch vụ thuê ngoài',
         ['- Mặc định: Dịch vụ thuê ngoài' if not edit else '- Màn Sửa: khóa, không đổi được loại đã lưu',
          '- Dịch vụ thuê ngoài', '- Công nợ bảo hiểm',
          '- Đổi loại → xóa hợp đồng, nhà cung cấp, bảng dịch vụ, đơn bảo hiểm đã chọn; không hỏi xác nhận (BR-01)',
          '- Trống khi lưu → “Loại yêu cầu – Bắt buộc phải nhập”']),
        ('Hợp đồng mua dịch vụ', 'Textbox', 'Enable / Ẩn', '–', 'Có (khi gửi duyệt)', 'Theo phiếu' if edit else 'Trống',
         ['- Chỉ có ở loại Dịch vụ thuê ngoài; gợi ý “Chọn hợp đồng mua dịch vụ...”',
          '- Bấm ô (biểu tượng kính lúp) → mở cửa sổ Chọn hợp đồng mua dịch vụ (mục 2.6)',
          '- Chọn xong tự điền Nhà cung cấp, VAT % theo hợp đồng và nạp bảng Danh sách dịch vụ',
          '- Nút × bỏ chọn: xóa luôn Nhà cung cấp, toàn bộ dòng dịch vụ; đang Kèm hóa đơn thì VAT % về 0',
          '- Trống khi Lưu và gửi duyệt → “Hợp đồng mua dịch vụ – Bắt buộc phải nhập”']),
        ('Nhà cung cấp', 'Dropdown', 'Enable / Ẩn', 'Gõ để tìm, tối đa 50 gợi ý', 'Có (khi gửi duyệt)',
         'Theo phiếu' if edit else 'Trống',
         ['- Chỉ có ở loại Dịch vụ thuê ngoài; gợi ý “Chọn nhà cung cấp”',
          '- Tự điền theo hợp đồng, dạng “Mã - Tên”; vẫn đổi được',
          '- Gõ mã hoặc tên để tìm, trong lúc tìm hiện “Đang tìm...”',
          '- Trống khi Lưu và gửi duyệt → “Nhà cung cấp – Bắt buộc phải nhập”']),
        ('Số đơn bảo hiểm', 'Textbox', 'Enable / Ẩn', '–', 'Có (khi gửi duyệt)', 'Theo phiếu' if edit else 'Trống',
         ['- Chỉ có ở loại Công nợ bảo hiểm; gợi ý “Chọn đơn bảo hiểm...”',
          '- Bấm ô → mở cửa sổ Chọn đơn bảo hiểm (mục 2.6); chọn xong nạp toàn bộ thông tin bảo hiểm (chỉ đọc)',
          '- Nút × bỏ chọn: xóa toàn bộ thông tin bảo hiểm',
          '- Trống khi Lưu và gửi duyệt → “Số đơn bảo hiểm – Bắt buộc phải nhập”']),
        ('Phụ lục bổ sung', 'Textbox', 'Read-only / Ẩn', '–', '–', 'Trống',
         ['- Chỉ ở loại Công nợ bảo hiểm, gợi ý “Lấy theo đơn bảo hiểm”', '- Tự điền theo đơn bảo hiểm, không sửa được']),
        ('Số hợp đồng mua', 'Textbox', 'Read-only / Ẩn', '–', '–', 'Trống',
         ['- Chỉ ở loại Công nợ bảo hiểm, gợi ý “Lấy theo đơn bảo hiểm”', '- Tự điền theo đơn bảo hiểm, không sửa được']),
        ('Hóa đơn VAT', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có (khi gửi duyệt)', 'Theo phiếu' if edit else 'Trống',
         ['- Mặc định: trống, gợi ý “Chọn hóa đơn VAT”', '- Kèm hóa đơn', '- Không kèm hóa đơn',
          '- Chọn Kèm hóa đơn → VAT % = VAT của hợp đồng, hiện dòng VAT ở bảng dịch vụ, khối File đính kèm thành bắt buộc',
          '- Chọn Không kèm hóa đơn → VAT % = 0, ẩn dòng VAT',
          '- Trống khi Lưu và gửi duyệt → “Hóa đơn VAT – Bắt buộc phải nhập”']),
        ('Diễn giải / Ghi chú', 'Textarea', 'Enable', '0–1.000 ký tự', 'Không', 'Theo phiếu' if edit else 'Trống',
         ['- Nhãn “Diễn giải” (Dịch vụ thuê ngoài) hoặc “Ghi chú” (Công nợ bảo hiểm), 2 dòng',
          '- Gợi ý “Nhập diễn giải” / “Nhập ghi chú”', '- Không gõ được quá 1.000 ký tự; nhận mọi ký tự']),
        ('Ghi chú duyệt', 'Textarea', 'Read-only', '–', '–', 'Ẩn',
         ['- Chỉ hiện khi phiếu đã có lý do Không duyệt', '- Không sửa được']),
        ('Khối Thông tin công ty bảo hiểm', 'Label', 'Read-only / Ẩn', '–', '–', 'Trống',
         ['- Chỉ ở loại Công nợ bảo hiểm; lấy theo đơn bảo hiểm',
          '- Tên công ty bảo hiểm (Mã - Tên), Mã số thuế, Địa chỉ, Số điện thoại, Chi nhánh',
          '- Số tài khoản ngân hàng, Tên tài khoản ngân hàng, Ngân hàng, Tỉnh/TP']),
        ('Khối Thông tin người liên hệ', 'Label', 'Read-only / Ẩn', '–', '–', 'Trống',
         ['- Chỉ ở loại Công nợ bảo hiểm', '- Họ và tên, Số điện thoại, Email']),
        ('Khối Thông tin người đại diện', 'Label', 'Read-only / Ẩn', '–', '–', 'Trống',
         ['- Chỉ ở loại Công nợ bảo hiểm', '- Họ và tên, Chức vụ']),
        ('Bảng Danh sách dịch vụ (bảo hiểm)', 'Table/Grid', 'Read-only / Ẩn', '1 dòng', '–', '“Chọn đơn bảo hiểm để nạp thông tin.”',
         ['- Chỉ ở loại Công nợ bảo hiểm', '- Cột STT, Dịch vụ đi kèm (“Bảo hiểm hàng hóa nhập khẩu”), Phí bảo hiểm, Mức khấu trừ, '
          'Tổng thanh toán', '- Dòng Tổng trước thuế, VAT (x%), Tổng sau thuế']),
        ('Nút Thêm tài liệu', 'Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Ở tiêu đề khối File đính kèm',
          '- Chữ gợi ý “Chấp nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip — tối đa 20MB/file”',
          '- Bấm → thêm 1 dòng có nút Chọn tệp']),
        ('Nút Chọn tệp', 'Button', 'Enable', '9 đuôi file, ≤ 20MB', '–', 'Hiển thị',
         ['- Chọn file từ máy → tải lên ngay, hiện “Đang tải lên <tên file>...”',
          '- Sai đuôi → “File "<tên file>" không thuộc định dạng cho phép”', '- Quá 20MB → “File "<tên file>" vượt quá 20MB”']),
        ('Bảng File đính kèm', 'Table/Grid', 'Enable', 'Nhiều file', 'Có (khi Kèm hóa đơn và gửi duyệt)',
         'Theo phiếu' if edit else 'Chưa có file',
         ['- Cột STT, “Upload / File” (biểu tượng loại file + tên file), Dung lượng', '- Bấm tên file → xem trước file',
          '- Kèm hóa đơn mà chưa có file khi Lưu và gửi duyệt → “File đính kèm – Bắt buộc khi kèm hóa đơn VAT”']),
        ('Nút Xóa file', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Chữ gợi ý “Xóa”', '- File chưa lưu: bỏ khỏi danh sách ngay',
          '- File đã lưu: hỏi “Bạn có chắc muốn xóa file đính kèm này?” (Xóa / Hủy); Xóa → xóa hẳn, báo “Xóa file thành công”']),
        ('Bảng Danh sách dịch vụ', 'Table/Grid', 'Enable / Ẩn', '–', 'Có (khi gửi duyệt)',
         'Theo phiếu' if edit else '“Chọn hợp đồng mua dịch vụ để nạp danh sách dịch vụ.”',
         ['- Chỉ ở loại Dịch vụ thuê ngoài; dữ liệu lấy từ hợp đồng, mỗi dịch vụ gộp ô theo số yêu cầu mua dịch vụ',
          '- Cột STT, Tên dịch vụ, ĐVT (“Gói”), Số lượng (= tổng SL hạch toán của dịch vụ), Đơn giá, Thành tiền',
          '- Nhóm cột Chi tiết: Yêu cầu (số yêu cầu mua dịch vụ + người tạo, bấm mở ở tab mới), SL HĐ còn lại, SL hạch toán',
          '- Hợp đồng chưa có dòng dịch vụ khi gửi duyệt → “Danh sách dịch vụ – Hợp đồng chưa có dòng dịch vụ nào”']),
        ('Ô SL hạch toán', 'Textbox', 'Enable', '0 ≤ SL ≤ SL HĐ còn lại', 'Có', 'SL HĐ còn lại' if not edit else 'Theo phiếu',
         ['- Gợi ý “Nhập SL hạch toán”, nhập số, có dấu phẩy ngăn nghìn',
          '- Màn Tạo: tự điền bằng SL HĐ còn lại khi chọn hợp đồng',
          '- Âm → “Không được âm”; lớn hơn SL HĐ còn lại → “Không được vượt SL còn lại” (cả Lưu nháp)',
          '- Tổng SL bằng 0 khi Lưu và gửi duyệt → “Vui lòng nhập SL hạch toán trước khi gửi duyệt.”']),
        ('Dòng Thành tiền', 'Label', 'Read-only', '≥ 0', '–', '0', 'Tổng Thành tiền các dịch vụ, tính lại ngay khi đổi SL.'),
        ('Ô VAT (%)', 'Textbox', 'Enable / Ẩn', '0–100', 'Không', 'VAT của hợp đồng',
         ['- Chỉ hiện khi Kèm hóa đơn; bên phải hiện tiền VAT', '- Ngoài 0–100 → “VAT (%) – Phải trong khoảng 0 đến 100”']),
        ('Dòng Tổng thanh toán', 'Label', 'Read-only', '≥ 0', '–', '0',
         'Thành tiền + tiền VAT; máy chủ tự tính lại khi lưu, không nhận số từ màn hình.'),
        ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         ['- Lưu phiếu ở trạng thái Đang tạo', '- Chỉ bắt buộc Loại yêu cầu (BR-02)', '- Khóa trong lúc đang lưu']),
        ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         ['- Lưu phiếu ở trạng thái Chờ duyệt, không hỏi xác nhận', '- Kiểm tra đủ trường bắt buộc theo loại (BR-02)',
          '- Khóa trong lúc đang lưu']),
    ]
    if not edit:
        rows.append(('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
                     ['- Chỉ có ở màn Tạo; chữ gợi ý “Lưu nháp phiếu này rồi tiếp tục lập phiếu mới”',
                      '- Lưu nháp như nút Lưu nháp rồi mở lại form trống, ở lại màn Tạo']))
    rows += [
        ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Về màn danh sách', '- Có thay đổi chưa lưu → hộp Thông tin chưa lưu']),
        ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         ['- Chữ đỏ ngay dưới ô, ô đổi viền đỏ; chỉ hiện sau lần bấm lưu đầu tiên',
          '- Báo mọi ô thiếu / sai cùng lúc, tự cuộn tới ô lỗi đầu tiên', '- Sửa ô nào thì lỗi ô đó biến mất']),
        ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         ['- Thành công: “Cập nhật thành công.”' if edit else '- Thành công: “Thêm mới thành công.”',
          '- Thiếu / sai dữ liệu: ' + TOAST_422, '- Lỗi nghiệp vụ máy chủ trả: hiện nguyên văn (vd “Hợp đồng mua dịch vụ không '
          'hợp lệ hoặc chưa được duyệt.”' + (', ' + M_CONFLICT + ')' if edit else ')'), '- Lỗi khác: “Lỗi khi lưu phiếu”']),
        ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', UNSAVED),
    ]
    return rows


def save_ev(edit):
    if edit:
        ev = [('Mở màn Sửa', 'System',
               'Before:\n– Kiểm tra phiếu tồn tại và nằm trong phạm vi xem; sai → chuyển sang trang “không tìm thấy”.\n'
               'During:\n– Nạp dữ liệu phiếu (dòng dịch vụ kèm SL HĐ còn lại không trừ phần chính phiếu này đang giữ).\n'
               '– Phiếu không sửa được (không phải người tạo hoặc không ở Đang tạo / Không duyệt) → tự chuyển sang màn chi tiết.\n'
               'After:\n– Hiển thị form với dữ liệu phiếu, Loại yêu cầu bị khóa; tiêu đề “Sửa phiếu yêu cầu hạch toán mua dịch vụ: '
               '<số phiếu>”.\n– Chốt mốc “chưa đổi gì” để so khi rời màn.')]
    else:
        ev = [('Bấm nút Tạo mới', 'Click',
               'Before:\n– Chức năng không gắn quyền riêng.\n'
               'During:\n– Dựng form trống, Loại yêu cầu = Dịch vụ thuê ngoài, người tạo = người đăng nhập.\n'
               'After:\n– Mở màn “Tạo phiếu yêu cầu hạch toán mua dịch vụ”; chưa có file, bảng dịch vụ hiện câu hướng dẫn chọn hợp đồng.')]
    ev += [
        ('Đổi Loại yêu cầu', 'Change',
         'Before:\n– Chỉ ở màn Tạo (màn Sửa khóa ô).\n'
         'During:\n– Xóa hợp đồng, nhà cung cấp, bảng dịch vụ, đơn bảo hiểm đã chọn; xóa các lỗi đang hiện.\n'
         '– Giữ nguyên Hóa đơn VAT, Diễn giải, file đính kèm.\n'
         'After:\n– Hiện các ô của loại mới (BR-01); không hỏi xác nhận.'),
        ('Đổi Hóa đơn VAT', 'Change',
         'Before:\n– Áp cả 2 loại.\n'
         'During:\n– Kèm hóa đơn → VAT % = VAT của hợp đồng đã chọn; Không kèm hóa đơn → VAT % = 0.\n'
         'After:\n– Hiện / ẩn dòng VAT, tính lại Tổng thanh toán; khối File đính kèm thành bắt buộc / không bắt buộc.'),
        ('Nhập SL hạch toán', 'Change',
         'Before:\n– Chỉ nhận số.\nDuring:\n– Cộng lại Số lượng, Thành tiền của dịch vụ và 3 dòng tổng.\n'
         '– Âm hoặc vượt SL HĐ còn lại chỉ báo khi bấm lưu.\n'
         'After:\n– Cập nhật số trên bảng; xóa lỗi đang hiện của ô.'),
        ('Chọn tệp đính kèm', 'Change',
         'Before:\n– Chỉ nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; tối đa 20MB/file.\n'
         'During:\n– Sai đuôi → “File "<tên file>" không thuộc định dạng cho phép”.\n'
         '– Quá dung lượng → “File "<tên file>" vượt quá 20MB”.\n' + ERR + '\n'
         'After:\n– Tải file lên kho lưu trữ ngay, hiện tên file và dung lượng; file chỉ gắn vào phiếu khi bấm lưu.'),
    ]
    if edit:
        ev.append(('Bấm Xóa file đã lưu', 'Click',
                   'Before:\n– Kiểm tra phiếu Đang tạo / Không duyệt (sai → ' + M_CONFLICT + ') và người tạo (sai → “Bạn không có '
                   'quyền sửa phiếu này”).\n– Hiển thị hộp “Xác nhận xóa” nội dung “Bạn có chắc muốn xóa file đính kèm này?”; Hủy → dừng.\n'
                   'During:\n– File không thuộc phiếu → “Không tìm thấy file trong phiếu”.\n' + ERR + '\n'
                   'After:\n– Bỏ file khỏi phiếu ngay (không cần bấm lưu).\n'
                   '– Ghi một dòng lịch sử “Thay đổi thông tin” (File đính kèm đã xóa).\n– Hiển thị “Xóa file thành công”.'))
    perm = ('Before:\n– Kiểm tra phiếu còn Đang tạo / Không duyệt; sai → hiển thị ' + M_CONFLICT + ' và dừng xử lý.\n'
            '– Kiểm tra người đăng nhập là người tạo; sai → hiển thị “Bạn không có quyền sửa phiếu này” và dừng xử lý.\n') if edit else \
           'Before:\n– Phiếu mới: không cần quyền riêng; khóa các nút lưu trong lúc đang lưu.\n'
    log_draft = ('– Ghi một dòng lịch sử “Thay đổi thông tin” chỉ với trường / dòng dịch vụ / file đã đổi; phiếu Không duyệt lưu nháp '
                 'thì ghi thêm “Thay đổi trạng thái” Không duyệt → Đang tạo.\n' if edit else
                 '– Sinh số phiếu <mã công ty>.YCHTMDV.<năm><6 số>; công ty, phòng ban, bộ phận theo người tạo.\n'
                 '– Ghi một dòng lịch sử “Tạo mới” của phiếu.\n')
    log_send = ('– Ghi một dòng lịch sử “Thay đổi thông tin” (trường đã đổi) và một dòng “Thay đổi trạng thái” <trạng thái cũ> → '
                'Chờ duyệt.\n' if edit else
                '– Sinh số phiếu; công ty, phòng ban, bộ phận theo người tạo.\n– Ghi một dòng lịch sử “Tạo mới” của phiếu.\n')
    ev += [
        ('Bấm Lưu nháp', 'Click', perm +
         'During:\n– Loại yêu cầu trống → “Loại yêu cầu – Bắt buộc phải nhập”.\n'
         '– SL hạch toán âm → “Không được âm”; vượt SL HĐ còn lại (máy chủ tính lại có khóa dòng hợp đồng) → “Không được vượt SL '
         'còn lại”; VAT ngoài 0–100 → “VAT (%) – Phải trong khoảng 0 đến 100”.\n'
         '– Hợp đồng không phải hợp đồng đã duyệt do mình tạo → “Hợp đồng mua dịch vụ không hợp lệ hoặc chưa được duyệt.”.\n'
         '– Có lỗi → hiển thị ' + TOAST_422 + ', cuộn tới ô lỗi đầu tiên.\n' + ERR + '\n'
         'After:\n– Lưu phiếu ở trạng thái Đang tạo; ô trống để trống; tổng tiền máy chủ tự tính.\n' + log_draft +
         '– Hiển thị “' + ('Cập nhật thành công.' if edit else 'Thêm mới thành công.') + '” và quay về màn danh sách (Back của '
         'trình duyệt không quay lại form vừa lưu).'),
        ('Bấm Lưu và gửi duyệt', 'Click', perm + '– Không hỏi xác nhận trước khi gửi.\n'
         'During:\n– Hóa đơn VAT trống → “Hóa đơn VAT – Bắt buộc phải nhập”; Kèm hóa đơn mà chưa có file → “File đính kèm – Bắt '
         'buộc khi kèm hóa đơn VAT”.\n'
         '– Dịch vụ thuê ngoài: thiếu Hợp đồng mua dịch vụ / Nhà cung cấp → ' + M_REQ + '; hợp đồng không có dịch vụ → '
         '“Danh sách dịch vụ – Hợp đồng chưa có dòng dịch vụ nào”; tổng SL = 0 → “Vui lòng nhập SL hạch toán trước khi gửi duyệt.”; '
         'SL âm / vượt → như Lưu nháp.\n'
         '– Công nợ bảo hiểm: thiếu Số đơn bảo hiểm → “Số đơn bảo hiểm – Bắt buộc phải nhập”; đơn đã bị phiếu khác giữ → “Số đơn '
         'bảo hiểm – Đơn không hợp lệ hoặc đã có yêu cầu hạch toán khác.”.\n'
         '– Có lỗi → hiển thị ' + TOAST_422 + ', cuộn tới ô lỗi đầu tiên.\n' + ERR + '\n'
         'After:\n– Lưu phiếu ở trạng thái Chờ duyệt; loại Công nợ bảo hiểm chuyển đơn (và phụ lục) bảo hiểm sang Đang hạch toán.\n'
         + log_send +
         '– Gửi thông báo ' + NOTI_SEND + '.\n'
         '– Hiển thị “' + ('Cập nhật thành công.' if edit else 'Thêm mới thành công.') + '” và quay về màn danh sách.'),
    ]
    if not edit:
        ev.append(('Bấm Lưu và tiếp tục', 'Click',
                   'Before:\n– Chỉ có ở màn Tạo; khóa nút trong lúc đang lưu.\n'
                   'During:\n– Kiểm tra như Lưu nháp (chỉ bắt buộc Loại yêu cầu, SL không âm / không vượt).\n' + ERR + '\n'
                   'After:\n– Lưu phiếu Đang tạo, ghi lịch sử “Tạo mới”, hiển thị “Thêm mới thành công.”.\n'
                   '– Ở lại màn Tạo, form trống như lúc mới vào.'))
    ev.append(('Bấm Quay lại hoặc rời màn', 'Click',
               'Before:\n– So dữ liệu hiện tại (kể cả file vừa tải) với mốc lúc mở màn.\n'
               'During:\n– Có thay đổi chưa lưu → hiển thị hộp “Thông tin chưa lưu” nội dung “Bạn có thông tin chưa lưu. Có chắc '
               'chắn muốn thoát?”.\n'
               'After:\n– Bấm Thoát: bỏ thay đổi, rời màn; bấm Ở lại: giữ nguyên dữ liệu.\n'
               '– Không có thay đổi: về màn danh sách ngay.'))
    return ev


# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu yêu cầu hạch toán mua dịch vụ',
       mota='Hiển thị bảng phiếu yêu cầu hạch toán mua dịch vụ nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân trang, sắp '
            'xếp và tổng số phiếu khớp bộ lọc. Màn dùng chung cho người lập và kế toán: người có quyền Hạch toán mua dịch vụ thấy '
            'thêm phiếu Chờ duyệt cùng công ty và xử lý ngay trên dòng (không có màn chờ duyệt riêng).',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Người dùng vào một trong các lối vào ở mục Layout (không cần quyền riêng để vào màn).',
       chinh='1. Người dùng vào một trong 2 lối vào ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem theo thứ tự V1 → V2 → V3; không có cấp nào thì lấy phiếu do chính người đó tạo.\n'
             '3. Người có quyền Hạch toán mua dịch vụ: cộng thêm phiếu Chờ duyệt cùng công ty và phiếu mình là Người duyệt.\n'
             '4. Hệ thống loại bỏ phiếu Đang tạo của người khác.\n'
             '5. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có) và cấu hình cột của người dùng.\n'
             '6. Hệ thống trả về trang 1, phiếu tạo gần nhất xếp trên, kèm tổng số phiếu; dòng “Hiển thị a–b / N” hiện đúng khoảng '
             'và tổng.\n'
             '7. Hệ thống hiện nút trên từng dòng theo cờ quyền máy chủ trả cho phiếu đó.',
       phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng dựng theo cấu hình đó.\n'
           '• Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”; lỗi thiếu quyền không hiện câu này.\n'
           '• Bấm số hợp đồng → mở hợp đồng mua dịch vụ (loại Dịch vụ thuê ngoài) hoặc hợp đồng nguyên tắc bảo hiểm (loại Công nợ '
           'bảo hiểm) trên hệ thống ERP ở tab mới.\n'
           '• Bấm nhanh nhiều lần (đổi trang, đổi lọc) → chỉ hiển thị kết quả của lần bấm cuối.\n'
           '• Phiên đăng nhập hết hạn → báo hết phiên đăng nhập, điều hướng về màn đăng nhập.',
       dacbiet='Cột mặc định hiển thị (15): STT, Số phiếu, Loại yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán, Ngày tạo, Người '
               'tạo, Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, Diễn giải, Trạng thái, Hành động; không có cột ẩn mặc '
               'định. Cột bắt buộc (khóa, không ẩn / không đổi vị trí): STT, Số phiếu, Hành động. Mặc định 10 dòng/trang.'),
   layout=dict(entries=[
       (MENU, 'Hiển thị: tiêu đề “Yêu cầu hạch toán mua dịch vụ”; phiếu trong phạm vi quyền (Phần 2). Đây là lối vào chính.'),
       (MENU_TC, 'Hiển thị: giống lối vào trên (cùng danh sách, cùng bộ lọc).')],
       shot=shot('01_list'), shot_caption='Màn danh sách Yêu cầu hạch toán mua dịch vụ'),
   extra=[('01c_menu_row', 'Dòng phiếu Chờ duyệt với người có quyền Hạch toán — nút Hạch toán, Không duyệt, menu “…”')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Yêu cầu hạch toán mua dịch vụ”',
        ['- Là tiêu đề thanh trên cùng, tiêu đề bảng và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Không gắn quyền riêng', '- Bấm → mở màn Tạo phiếu yêu cầu hạch toán mua dịch vụ (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.13)', '- Khóa trong lúc đang xuất']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ xem trước bản in danh sách theo bộ lọc (mục 2.12).'),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        ['- Biểu tượng cột, chữ gợi ý “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tùy chỉnh cột (mục 2.4)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Liên tục giữa các trang', '- Ghim trái; khóa trong Tùy chỉnh cột']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', '<mã công ty>.YCHTMDV.<năm><6 số>', 'Theo dữ liệu',
        ['- Bấm số phiếu → mở màn chi tiết (mục 2.9)', '- Sắp xếp được', '- Ghim trái; khóa trong Tùy chỉnh cột']),
       ('Cột Loại yêu cầu', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu',
        ['- Dịch vụ thuê ngoài / Công nợ bảo hiểm', '- Không sắp xếp']),
       ('Cột Số hợp đồng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Dịch vụ thuê ngoài: số hợp đồng mua dịch vụ; Công nợ bảo hiểm: số hợp đồng nguyên tắc bảo hiểm',
         '- Là link mở hợp đồng trên ERP ở tab mới', '- Không sắp xếp']),
       ('Cột Nhà cung cấp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Dạng “Mã - Tên”', '- Tối đa 2 dòng, di chuột xem đủ']),
       ('Cột Tổng thanh toán', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
        ['- Dấu phẩy ngăn nghìn, tối đa 2 số lẻ, căn phải; bằng 0 thì để trống', '- Sắp xếp được']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Sắp xếp được; mặc định phiếu mới xếp trên']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Họ tên người tạo phiếu.'),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Kế toán đã Không duyệt phiếu, hoặc đã duyệt phiếu Hạch toán lập từ phiếu', '- Trống khi chưa ai xử lý']),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Thời điểm Không duyệt / duyệt hạch toán; phiếu hạch toán từ ERP không có thì lấy ngày hạch toán', '- Sắp xếp được']),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lưu phiếu gần nhất trên HRM.'),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Thời điểm lưu gần nhất', '- Sắp xếp được']),
       ('Cột Diễn giải', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Diễn giải / Ghi chú của phiếu', '- Tối đa 2 dòng']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu', STATUS_LIST + ['- Không sắp xếp']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo quyền và trạng thái',
        ['- Sửa: người tạo, phiếu Đang tạo / Không duyệt → màn Sửa (mục 2.7)',
         '- Xóa (đỏ): cùng điều kiện → mở màn chi tiết để xác nhận xóa (mục 2.8)',
         '- Hạch toán (biểu tượng máy tính): phiếu Chờ duyệt, người có quyền Q1 cùng công ty (mục 2.10)',
         '- Không duyệt (đỏ): cùng điều kiện Hạch toán (mục 2.11)', '- In phiếu, Lịch sử: luôn hiện',
         '- Dòng có hơn 3 nút: 2 nút đầu hiện thẳng, còn lại trong nút “…” (Hành động khác)', '- Khóa trong Tùy chỉnh cột']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- a–b: khoảng số thứ tự của trang đang xem', '- N: tổng phiếu khớp phạm vi và bộ lọc']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5, 10, 20, 50, 100', '- Đổi giá trị → về trang 1, nạp lại']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Giữ bộ lọc, sắp xếp khi đổi trang']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp.” khi N = 0.'),
       ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- “Lỗi khi tải dữ liệu” khi máy chủ lỗi']),
   ],
   ev=[('Mở màn hình', 'System',
        'Before:\n– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3; không có cấp nào thì giới hạn ở phiếu do chính người dùng tạo.\n'
        '– Người có quyền Hạch toán mua dịch vụ: cộng phiếu Chờ duyệt cùng công ty và phiếu mình là Người duyệt.\n'
        'During:\n– Nạp cấu hình cột đã lưu, khôi phục bộ lọc của 10 phút gần nhất (nếu có), rồi nạp dữ liệu.\n'
        '– Loại bỏ phiếu Đang tạo của người khác; tính cờ Sửa / Xóa / Hạch toán cho từng phiếu.\n'
        'After:\n– Trả về trang 1, sắp xếp theo ngày tạo giảm dần, kèm tổng số phiếu.\n'
        '– Hiện / ẩn ô lọc Công ty, Phòng ban theo cấp quyền xem.'),
       ('Bấm số phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem (đã lọc ở bước nạp danh sách).\nDuring:\n– Ghi nhớ bộ lọc hiện tại 10 phút.\n'
        'After:\n– Mở màn chi tiết của phiếu (mục 2.9).'),
       ('Bấm số hợp đồng', 'Click',
        'Before:\n– Dòng có số hợp đồng.\nDuring:\n– Chọn màn hợp đồng ERP theo loại yêu cầu.\nAfter:\n– Mở hợp đồng ở tab mới, '
        'danh sách giữ nguyên.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ 5 cột Số phiếu, Tổng thanh toán, Ngày tạo, Ngày duyệt, Ngày cập nhật sắp xếp được.\n'
        'During:\n– Đổi chiều tăng / giảm; giữ nguyên bộ lọc.\nAfter:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Bấm số trang hoặc nút tiến lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nDuring:\n– Nạp dữ liệu của trang được chọn.\n'
        'After:\n– Hiển thị trang mới, STT liên tục, dòng “Hiển thị a–b / N” cập nhật.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Chọn 1 trong 5, 10, 20, 50, 100.\nDuring:\n– Ghi nhận số dòng mới.\nAfter:\n– Quay về trang 1, nạp lại.'),
       ('Bấm nút “…” trên dòng', 'Click',
        'Before:\n– Dòng có hơn 3 nút.\nDuring:\n– Mở menu các nút còn lại (In phiếu, Lịch sử).\nAfter:\n– Bấm mục → thực hiện như nút '
        'tương ứng; bấm ra ngoài → đóng menu.')])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(ten='Tìm kiếm và lọc danh sách phiếu',
              mota='Thu hẹp danh sách theo ô tìm nhanh (số phiếu, số hợp đồng, tên dịch vụ) và 8 tiêu chí của khối Tìm kiếm nâng cao: '
                   'Công ty, Phòng ban, Loại yêu cầu, Trạng thái, Nhà cung cấp, Người duyệt, Người tạo, Ngày tạo. Kết quả luôn nằm '
                   'trong phạm vi quyền xem của người dùng.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm hoặc Enter.\n'
                    '2. Hoặc bấm Tìm kiếm nâng cao để mở khối tiêu chí, chọn giá trị một hoặc nhiều tiêu chí.\n'
                    '3. Ô dạng chọn (Công ty, Phòng ban, Loại yêu cầu, Trạng thái, Nhà cung cấp, Người duyệt, Người tạo, Ngày tạo) '
                    'lọc ngay khi đổi giá trị.\n'
                    '4. Ô tìm nhanh chỉ áp khi bấm Tìm kiếm / Enter.\n'
                    '5. Hệ thống quay về trang 1, nạp lại danh sách; bộ lọc được ghi nhớ 10 phút khi người dùng đi vào màn chi tiết / '
                    'sửa / tạo của màn này.',
              phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh và sắp xếp, nạp lại từ trang 1.\n'
                  '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
                  '• Đổi Công ty → xóa Phòng ban đang chọn, danh sách phòng ban chỉ còn của công ty mới.\n'
                  '• Ô Nhà cung cấp gõ dưới 2 ký tự → chưa tìm; tối đa 50 gợi ý.\n'
                  '• Biểu tượng ổ khóa cạnh nhãn Công ty / Phòng ban: bật để hiện cả công ty / phòng ban đã khóa trong danh sách chọn.\n'
                  '• Sang màn khác bằng menu, hoặc quá 10 phút → bộ lọc trở về trống.',
              dacbiet='Kiểu khớp: ô tìm nhanh khớp MỘT PHẦN (chuỗi chứa) với số phiếu, số hợp đồng (mua dịch vụ hoặc bảo hiểm) hoặc tên '
                      'dịch vụ của dòng chi tiết; không phân biệt hoa / thường; tự bỏ khoảng trắng đầu / cuối; không giới hạn số ký '
                      'tự; ký tự % và _ được hiểu là ký tự đại diện. Ô dạng chọn khớp CHÍNH XÁC. Ngày tạo lấy trọn 2 ngày biên. '
                      'Lọc Công ty chỉ có hiệu lực với người xem được mọi công ty (V1).'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách'),
   ui=[('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu, số hợp đồng, tên dịch vụ”', '- Khớp một phần', '- Chỉ áp khi bấm Tìm kiếm / Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp ô tìm nhanh, về trang 1, nạp lại.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa toàn bộ tiêu chí kể cả ô tìm nhanh, nạp lại từ trang 1.'),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Mở / thu gọn khối tiêu chí', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống',
        ['- Chỉ hiện với quyền V1 (và Super admin)', '- Mặc định: trống (tất cả)', '- Đổi giá trị → xóa Phòng ban đang chọn']),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Hiện với quyền V1, V2, V3', '- Mặc định: trống (tất cả)', '- Chỉ liệt kê phòng ban của Công ty đang chọn']),
       ('Loại yêu cầu', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)', '- Công nợ bảo hiểm', '- Dịch vụ thuê ngoài']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)', '- Đang tạo', '- Chờ duyệt', '- Đang hạch toán', '- Đã hạch toán', '- Không duyệt']),
       ('Nhà cung cấp', 'Dropdown', 'Enable', 'Gõ tối thiểu 2 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhà cung cấp”; tìm theo mã hoặc tên', '- Tối đa 50 gợi ý', '- Lọc phiếu đúng nhà cung cấp đã chọn']),
       ('Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Mặc định: trống (tất cả)']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Mặc định: trống (tất cả)']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- 1 ô gồm 2 lịch Từ ngày → Đến ngày', '- Lấy trọn cả 2 ngày biên']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp.” khi không có kết quả.')],
   ev=[('Đổi giá trị ô dạng chọn', 'Change',
        'Before:\n– Áp cho Công ty, Phòng ban, Loại yêu cầu, Trạng thái, Nhà cung cấp, Người duyệt, Người tạo, Ngày tạo.\n'
        'During:\n– Ghi nhận giá trị mới vào bộ lọc.\nAfter:\n– Quay về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí.'),
       ('Bấm nút Tìm kiếm hoặc Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh đang nhập.\nDuring:\n– Gộp với các tiêu chí đang chọn.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Bấm nút Làm mới', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Đặt lại toàn bộ tiêu chí, ô tìm nhanh, sắp xếp về mặc định.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Đổi Công ty', 'Change',
        'Before:\n– Chỉ có với quyền V1.\nDuring:\n– Xóa Phòng ban đang chọn.\nAfter:\n– Nạp phòng ban của công ty mới, nạp lại danh sách.'),
       ('Gõ ô Nhà cung cấp', 'Change',
        'Before:\n– Chỉ tìm khi gõ từ 2 ký tự.\nDuring:\n– Tìm nhà cung cấp có mã hoặc tên chứa chuỗi gõ (tối đa 50).\n'
        'After:\n– Hiển thị gợi ý; chọn 1 dòng thì lọc ngay.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối tiêu chí đang thu gọn.\nDuring:\n– Mở khối, nhãn đổi thành “Ẩn tìm kiếm nâng cao”.\n'
        'After:\n– Ghi nhớ trạng thái mở / thu gọn cùng bộ lọc.')])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn tiêu chí lọc muốn thấy ở khối Tìm kiếm nâng cao và sắp xếp lại thứ tự. Cấu hình '
                   'lưu riêng theo người dùng cho màn này; 7 tiêu chí là Công ty – Phòng ban, Loại yêu cầu, Trạng thái, Nhà cung cấp, '
                   'Người duyệt, Người tạo, Ngày tạo.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 7 tiêu chí kèm ô tích theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích, kéo thả để đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối Tìm kiếm nâng cao.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 7 tiêu chí theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu.\n'
                  '• Bỏ tích một tiêu chí đang có giá trị lọc → giá trị đó bị xóa sau khi lưu.\n'
                  '• Lưu thất bại → “Thao tác thất bại”.',
              dacbiet='Cấu hình lưu theo tài khoản và theo màn hình; tài khoản khác không bị ảnh hưởng.'),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách tiêu chí', 'Table/Grid', 'Enable', 'Danh sách 7 tiêu chí', 'Không', 'Theo cấu hình đã lưu',
        ['- Công ty – Phòng ban', '- Loại yêu cầu', '- Trạng thái', '- Nhà cung cấp', '- Người duyệt', '- Người tạo', '- Ngày tạo']),
       ('Ô tích của tiêu chí', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu',
        ['- Tích: tiêu chí hiện ở khối Tìm kiếm nâng cao', '- Bỏ tích: ẩn tiêu chí, xóa giá trị lọc của nó khi lưu']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự tiêu chí.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình, đóng cửa sổ, áp ngay.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích lại đủ 7 tiêu chí, thứ tự gốc; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”'])],
   ev=[('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Cấu hình gắn với người dùng đang đăng nhập.\nDuring:\n– Nạp cấu hình đang lưu.\nAfter:\n– Mở cửa sổ “Cài đặt bộ lọc”.'),
       ('Kéo đổi vị trí tiêu chí', 'Drag',
        'Before:\n– Kéo bằng tay nắm của dòng.\nDuring:\n– Đổi thứ tự trong cửa sổ.\nAfter:\n– Chưa áp cho tới khi bấm Lưu.'),
       ('Bỏ tích một tiêu chí', 'Change',
        'Before:\n– Áp cho mọi tiêu chí.\nDuring:\n– Ghi nhận trạng thái tích.\nAfter:\n– Chưa áp cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng.\nDuring:\n– Ghi cấu hình; lỗi → “Thao tác thất bại”.\n'
        'After:\n– Hiển thị “Cập nhật thành công”; khối lọc cập nhật; tiêu chí vừa bỏ tích bị xóa giá trị, danh sách nạp lại.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Tích lại 7 tiêu chí, thứ tự gốc.\nAfter:\n– Chưa lưu; phải bấm Lưu.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ thay đổi chưa lưu.\nAfter:\n– Đóng cửa sổ, khối lọc giữ nguyên.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Tùy chỉnh cột của bảng danh sách',
              mota='Cho phép mỗi người dùng bật / tắt và kéo sắp xếp 15 cột của bảng danh sách phiếu. Cấu hình lưu theo người dùng; ba '
                   'cột STT, Số phiếu, Hành động bị khóa: luôn hiện, không đổi vị trí. Cấu hình cột đang hiện cũng là các trường '
                   'được tích sẵn khi Xuất Excel.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
                    '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 15 cột theo cấu hình đang áp dụng.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng ba gạch đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình, hiển thị “Cập nhật thành công”, vẽ lại bảng.',
              phu='• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, giữ cấu hình đang áp dụng.\n'
                  '• Cột khóa: ô tích xám, không bỏ tích, không kéo; di chuột hiện “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”.\n'
                  '• Lưu thất bại → “Thao tác thất bại”.\n'
                  '• Cấu hình lưu trên máy chủ theo tài khoản: giữ sau F5, đăng nhập trình duyệt / máy khác vẫn giữ.\n'
                  '• Đổi cột không làm thay đổi dữ liệu, tổng số phiếu, bộ lọc.',
              dacbiet='Mặc định hiện cả 15 cột. Dòng dưới cửa sổ ghi “Đang chọn n/15 cột”.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Tuỳ chỉnh cột”', 'Kèm nút (x) đóng.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', '15 cột', '–', 'Theo cấu hình',
        ['- STT, Số phiếu (khóa)', '- Loại yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán, Ngày tạo, Người tạo',
         '- Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, Diễn giải, Trạng thái', '- Hành động (khóa, luôn cuối)']),
       ('Ô tích của cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình', ['- Tích: cột hiện', '- Cột khóa: xám']),
       ('Biểu tượng ba gạch', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Kéo để đổi vị trí', '- Cột khóa hiện ổ khóa, không kéo']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi cột.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi cột (trừ cột khóa).'),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/15 cột”.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình, đóng cửa sổ, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”'])],
   ev=[('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Cấu hình đã nạp lúc mở màn.\nDuring:\n– Liệt kê 15 cột theo cấu hình đang áp dụng.\nAfter:\n– Mở cửa sổ “Tuỳ chỉnh cột”.'),
       ('Kéo biểu tượng ba gạch', 'Drag',
        'Before:\n– Cột khóa không kéo được.\nDuring:\n– Đổi thứ tự trong cửa sổ.\nAfter:\n– Chưa áp cho tới khi bấm Lưu.'),
       ('Bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa không bỏ tích được.\nDuring:\n– Ghi nhận trạng thái.\nAfter:\n– Chưa áp cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng.\nDuring:\n– Ghi cấu hình; lỗi → “Thao tác thất bại”.\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ thay đổi chưa lưu.\nAfter:\n– Đóng cửa sổ; lần mở sau hiện đúng cấu hình đang áp.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu yêu cầu hạch toán mua dịch vụ', usecase=('FR-05', 'Lập phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu yêu cầu hạch toán mua dịch vụ',
       mota='Tạo một phiếu đề nghị kế toán hạch toán chi phí mua dịch vụ. Loại Dịch vụ thuê ngoài: chọn hợp đồng mua dịch vụ đã duyệt '
            'do mình tạo, hệ thống nạp dịch vụ, đơn giá, các yêu cầu mua dịch vụ và SL còn lại; người dùng chỉ nhập SL hạch toán. '
            'Loại Công nợ bảo hiểm: chọn đơn bảo hiểm, mọi thông tin lấy theo đơn. Sau đó lưu nháp hoặc gửi duyệt cho kế toán.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Yêu cầu hạch toán mua dịch vụ.\n'
                '3. Loại Dịch vụ thuê ngoài: người dùng có hợp đồng mua dịch vụ đã duyệt do chính mình tạo; loại Công nợ bảo hiểm: '
                'có đơn bảo hiểm đã duyệt chưa bị phiếu khác giữ.',
       chinh='1. Người dùng bấm Tạo mới; hệ thống mở màn “Tạo phiếu yêu cầu hạch toán mua dịch vụ”, Loại yêu cầu = Dịch vụ thuê ngoài.\n'
             '2. Người dùng chọn Loại yêu cầu (BR-01).\n'
             '3. Dịch vụ thuê ngoài: bấm ô Hợp đồng mua dịch vụ, chọn hợp đồng (mục 2.6); hệ thống điền Nhà cung cấp, VAT và nạp '
             'bảng dịch vụ với SL hạch toán = SL HĐ còn lại; người dùng sửa SL hạch toán nếu cần.\n'
             '4. Công nợ bảo hiểm: bấm ô Số đơn bảo hiểm, chọn đơn (mục 2.6); hệ thống nạp toàn bộ thông tin bảo hiểm.\n'
             '5. Người dùng chọn Hóa đơn VAT, nhập Diễn giải / Ghi chú, bấm Thêm tài liệu để đính kèm file.\n'
             '6. Người dùng bấm Lưu nháp, Lưu và gửi duyệt hoặc Lưu và tiếp tục.\n'
             '7. Hệ thống kiểm tra dữ liệu theo nút được bấm (BR-02), khóa các dòng hợp đồng và tính lại SL còn lại (BR-03), lấy '
             'lại dịch vụ / đơn giá từ hợp đồng, sinh số phiếu, tính tổng tiền, lưu phiếu.\n'
             '8. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
             '9. Lưu và gửi duyệt: hệ thống gửi thông báo “[YCHTMDV] Chờ duyệt: <số phiếu>” cho người có quyền Hạch toán mua dịch '
             'vụ cùng công ty; loại Công nợ bảo hiểm chuyển đơn bảo hiểm sang Đang hạch toán.\n'
             '10. Hệ thống hiển thị “Thêm mới thành công.” và quay về màn danh sách.',
       phu='• Lưu nháp khi Loại yêu cầu trống → lỗi dưới ô, không gửi máy chủ.\n'
           '• Lưu và gửi duyệt thiếu / sai dữ liệu → báo đỏ dưới từng ô, hiển thị ' + TOAST_422 + ', cuộn tới ô lỗi đầu, giữ dữ liệu.\n'
           '• SL hạch toán vượt SL còn lại (kể cả do người khác vừa lập phiếu cùng hợp đồng) → “Không được vượt SL còn lại” đúng ô.\n'
           '• Chọn hợp đồng chưa có dòng dịch vụ → báo “Hợp đồng chưa có dòng dịch vụ nào.”.\n'
           '• Đổi Loại yêu cầu → xóa dữ liệu nguồn của loại cũ, không hỏi xác nhận.\n'
           '• Lưu và tiếp tục → lưu nháp rồi mở lại form trống, ở lại màn Tạo.\n'
           '• Màn Tạo là trang riêng, không phải cửa sổ nổi: không có nút (x), không đóng bằng click ra ngoài; rời màn bằng Quay '
           'lại / menu → hộp “Thông tin chưa lưu”; F5 / đóng tab → hộp cảnh báo rời trang của trình duyệt.\n'
           '• Bấm nút lưu liên tục → nút khóa trong lúc đang lưu, chỉ tạo 1 phiếu.\n'
           '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
       dacbiet='Quy tắc trùng dữ liệu: phiếu KHÔNG có trường duy nhất, số phiếu tự sinh — 2 phiếu cùng hợp đồng đều lưu được nếu tổng '
               'SL không vượt SL hợp đồng (BR-03); một đơn bảo hiểm chỉ được một phiếu Chờ duyệt / Đang hạch toán / Đã hạch toán '
               'giữ. Máy chủ chỉ tin id dòng hợp đồng và SL hạch toán gửi lên; dịch vụ, đơn giá, tổng tiền tự lấy / tự tính. Khóa '
               'các nút lưu trong lúc đang xử lý.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10e_filled'),
               shot_caption='Màn Tạo phiếu — loại Dịch vụ thuê ngoài đã chọn hợp đồng'),
   extra=[('10b_validate', 'Bấm Lưu và gửi duyệt khi chưa nhập — lỗi dưới từng ô'),
          ('10d_insurance', 'Màn Tạo phiếu — loại Công nợ bảo hiểm'),
          ('10g_unsaved', 'Hộp Thông tin chưa lưu khi rời màn')],
   ui=form_ui(False), ev=save_ev(False))

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn hợp đồng mua dịch vụ và đơn bảo hiểm', usecase=('FR-06', 'Chọn hợp đồng / đơn bảo hiểm', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(ten='Chọn chứng từ nguồn của phiếu',
              mota='Hai cửa sổ chọn dùng ở màn Tạo / Sửa phiếu: “Chọn hợp đồng mua dịch vụ” (loại Dịch vụ thuê ngoài) và “Chọn đơn bảo '
                   'hiểm” (loại Công nợ bảo hiểm). Bấm một dòng là chọn; hệ thống nạp dữ liệu của chứng từ vào form.',
              tacnhan=TN_MOI,
              dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Tạo hoặc Sửa phiếu (người tạo, phiếu Đang tạo / '
                       'Không duyệt).\n3. Đã chọn Loại yêu cầu tương ứng.',
              chinh='1. Người dùng bấm ô Hợp đồng mua dịch vụ (hoặc Số đơn bảo hiểm).\n'
                    '2. Hệ thống mở cửa sổ, nạp trang 1 chứng từ hợp lệ (mới tạo xếp trên).\n'
                    '3. Người dùng nhập điều kiện tìm, bấm Tìm kiếm hoặc Enter.\n4. Người dùng bấm vào một dòng.\n'
                    '5. Hệ thống đóng cửa sổ, nạp dữ liệu chứng từ: hợp đồng → nhà cung cấp, VAT, dịch vụ, yêu cầu, SL còn lại; đơn '
                    'bảo hiểm → thông tin công ty bảo hiểm, người liên hệ, người đại diện, phí, tổng tiền.',
              phu='• Không có dữ liệu → “Không có hợp đồng mua dịch vụ đã duyệt nào do bạn tạo.” / “Không có đơn bảo hiểm phù hợp.”.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không chọn, ô giữ nguyên.\n'
                  '• Bấm số hợp đồng / số đơn / số hợp đồng mua (link) → mở chứng từ trên ERP ở tab mới, KHÔNG chọn dòng.\n'
                  '• Bấm × trong ô tìm → xóa chữ và tìm lại ngay.\n'
                  '• Lỗi tải danh sách → “Lỗi khi tải dữ liệu”; lỗi nạp chứng từ → “Lỗi khi tải hợp đồng” / “Lỗi khi tải đơn bảo hiểm”.',
              dacbiet='Hợp đồng chọn được: đã duyệt và do chính người đăng nhập tạo (kể cả Super admin). Đơn bảo hiểm chọn được: đã '
                      'duyệt, hoặc Đang hạch toán nhưng không còn phiếu nào giữ. Màn Sửa: SL còn lại không trừ phần chính phiếu đang '
                      'sửa giữ. Trong lúc nạp hợp đồng hiện thanh tải trên cùng.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('11_contract_picker'), shot_caption='Cửa sổ Chọn hợp đồng mua dịch vụ',
               note='Các cửa sổ chọn được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   extra=[('12_insurance_picker', 'Cửa sổ Chọn đơn bảo hiểm (dữ liệu môi trường thử chưa có đơn)')],
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Theo cửa sổ',
        ['- “Chọn hợp đồng mua dịch vụ”', '- “Chọn đơn bảo hiểm”', '- Có nút (x) đóng']),
       ('Ô Số hợp đồng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Cửa sổ chọn hợp đồng; gợi ý “Nhập số hợp đồng”', '- Khớp một phần', '- Có nút × xóa nhanh; Enter = Tìm kiếm']),
       ('Ô Số đơn', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Cửa sổ chọn đơn bảo hiểm; gợi ý “Nhập số đơn”', '- Khớp một phần']),
       ('Ô Số phụ lục', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', ['- Cửa sổ chọn đơn bảo hiểm', '- Khớp một phần']),
       ('Ô Số hợp đồng mua', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', ['- Cửa sổ chọn đơn bảo hiểm', '- Khớp một phần']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp điều kiện tìm, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa điều kiện tìm và sắp xếp, nạp lại từ trang 1.'),
       ('Bảng hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Số hợp đồng (sắp xếp được, link ERP), Nhà cung cấp, Ngày tạo (sắp xếp được)',
         '- Bấm dòng → chọn, đóng cửa sổ', '- Rỗng: “Không có hợp đồng mua dịch vụ đã duyệt nào do bạn tạo.”']),
       ('Bảng đơn bảo hiểm', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Số đơn (link ERP), Số phụ lục, Số hợp đồng mua (link ERP), Ngày tạo — đều sắp xếp được',
         '- Bấm dòng → chọn, đóng cửa sổ', '- Rỗng: “Không có đơn bảo hiểm phù hợp.”']),
       ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1',
        ['- Dòng “Hiển thị a–b / N”, Số dòng/trang 10, 20, 50, 100', '- Mặc định 10 dòng/trang']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không chọn.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Lỗi khi tải dữ liệu”', '- “Lỗi khi tải hợp đồng”, “Lỗi khi tải đơn bảo hiểm”',
         '- “Hợp đồng chưa có dòng dịch vụ nào.”', '- “Bạn không có quyền xem hợp đồng này” (hợp đồng không phải của mình)'])],
   ev=[('Bấm ô Hợp đồng mua dịch vụ / Số đơn bảo hiểm', 'Click',
        'Before:\n– Chỉ ở màn Tạo / Sửa; màn chi tiết là link chỉ đọc.\nDuring:\n– Xóa điều kiện tìm cũ, nạp trang 1.\n'
        'After:\n– Mở cửa sổ chọn tương ứng.'),
       ('Bấm Tìm kiếm, Enter hoặc tiêu đề cột', 'Click',
        'Before:\n– Lấy điều kiện ở các ô tìm.\nDuring:\n– Tìm theo chuỗi chứa; sắp xếp theo cột bấm.\nAfter:\n– Về trang 1, hiện kết quả.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Xóa điều kiện tìm, sắp xếp.\nAfter:\n– Nạp lại từ trang 1.'),
       ('Bấm một dòng hợp đồng', 'Click',
        'Before:\n– Hợp đồng đã duyệt do chính người dùng tạo; sai → “Bạn không có quyền xem hợp đồng này”.\n'
        'During:\n– Nạp dịch vụ, đơn giá, yêu cầu mua dịch vụ, SL HĐ còn lại (trừ phần các phiếu khác đang giữ).\n'
        'After:\n– Điền hợp đồng, nhà cung cấp (“Mã - Tên”), VAT (nếu Kèm hóa đơn), bảng dịch vụ với SL hạch toán = SL còn lại.\n'
        '– Hợp đồng chưa có dòng dịch vụ → báo “Hợp đồng chưa có dòng dịch vụ nào.”.'),
       ('Bấm một dòng đơn bảo hiểm', 'Click',
        'Before:\n– Đơn đã duyệt hoặc không còn phiếu nào giữ.\nDuring:\n– Nạp thông tin đơn (lỗi → “Lỗi khi tải đơn bảo hiểm”).\n'
        'After:\n– Điền Số đơn, Phụ lục bổ sung, Số hợp đồng mua và 3 khối thông tin bảo hiểm, bảng phí.'),
       ('Bấm link trong bảng', 'Click',
        'Before:\n– Số hợp đồng / số đơn / số hợp đồng mua là link.\nDuring:\n– Không chọn dòng.\nAfter:\n– Mở chứng từ trên ERP ở tab mới.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không ghi gì vào form.\nAfter:\n– Đóng cửa sổ, ô giữ nguyên.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Chỉnh sửa phiếu', usecase=('FR-07', 'Chỉnh sửa phiếu', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(ten='Chỉnh sửa phiếu yêu cầu hạch toán mua dịch vụ',
              mota='Người tạo sửa phiếu đang ở trạng thái Đang tạo hoặc Không duyệt. Màn Sửa dùng chung bố cục và quy tắc kiểm tra với '
                   'màn Tạo (mục 2.5), riêng Loại yêu cầu bị khóa; SL HĐ còn lại tính không trừ phần chính phiếu đang giữ; lưu nháp '
                   'hoặc gửi duyệt lại.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
                    '2. Hệ thống mở màn “Sửa phiếu yêu cầu hạch toán mua dịch vụ: <số phiếu>” với dữ liệu phiếu.\n'
                    '3. Người dùng sửa các trường (quy tắc như mục 2.5), đổi hợp đồng / đơn bảo hiểm, thêm / xóa file.\n'
                    '4. Người dùng bấm Lưu nháp hoặc Lưu và gửi duyệt.\n'
                    '5. Hệ thống kiểm tra trạng thái, người tạo, dữ liệu (BR-02, BR-03), lưu phiếu.\n'
                    '6. Hệ thống ghi nhận hành động “Thay đổi thông tin” trong lịch sử của phiếu (chỉ trường đã đổi, cũ → mới); đổi '
                    'trạng thái thì ghi thêm “Thay đổi trạng thái”.\n'
                    '7. Lưu và gửi duyệt: gửi thông báo “[YCHTMDV] Chờ duyệt: <số phiếu>” cho người có quyền Hạch toán mua dịch vụ '
                    'cùng công ty.\n'
                    '8. Hệ thống hiển thị “Cập nhật thành công.”, quay về màn danh sách.',
              phu='• Phiếu không sửa được (không phải người tạo / đã gửi duyệt) → tự chuyển sang màn chi tiết.\n'
                  '• Phiếu không tồn tại hoặc ngoài phạm vi → chuyển sang trang “không tìm thấy”.\n'
                  '• Phiếu đổi trạng thái giữa chừng (vd vừa gửi duyệt ở tab khác) → ' + M_CONFLICT + ', không lưu.\n'
                  '• Phiếu Không duyệt hiện Ghi chú duyệt (lý do) ở khối Thông tin chung.\n'
                  '• Rời màn khi chưa lưu → hộp “Thông tin chưa lưu”; không đổi gì (hoặc đổi rồi trả về giá trị ban đầu) → về danh '
                  'sách ngay.\n'
                  '• Phiếu đã bị xóa trong lúc đang sửa → bấm lưu báo lỗi chung của máy chủ “Item Not Found!”, không lưu.\n'
                  '• Hai tab cùng sửa nháp: lần lưu sau ghi đè lần trước.',
              dacbiet='Trường được sửa: Hợp đồng mua dịch vụ / Số đơn bảo hiểm, Nhà cung cấp, Hóa đơn VAT, VAT (%), Diễn giải / Ghi chú, '
                      'SL hạch toán, file. Không sửa được: Loại yêu cầu, Số phiếu, người tạo, ngày tạo, công ty / phòng ban, Ghi chú '
                      'duyệt, các ô lấy theo hợp đồng / đơn bảo hiểm. Kiểm tra SL không tính trùng phần chính phiếu đang giữ. Lịch sử '
                      'ghi giá trị cũ → mới; không đổi gì thì không ghi. Phiếu Chờ duyệt / Đang hạch toán / Đã hạch toán coi như khóa '
                      'sửa. Xóa file đã lưu có hiệu lực ngay.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('19_edit'), shot_caption='Màn Sửa phiếu yêu cầu hạch toán mua dịch vụ (phiếu Không duyệt)'),
   ui=form_ui(True), ev=save_ev(True))

# ------------------------------------------------------------ 2.8
fr(8, 'Xóa phiếu', usecase=('FR-08', 'Xóa phiếu', 'action', A_LAP),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(ten='Xóa phiếu yêu cầu hạch toán mua dịch vụ',
              mota='Người tạo xóa hẳn phiếu đang ở trạng thái Đang tạo hoặc Không duyệt cùng toàn bộ dòng dịch vụ và dòng yêu cầu. Nút Xóa '
                   'ở cột Hành động mở màn chi tiết của phiếu; việc xác nhận và xóa thực hiện ở chân màn chi tiết qua hộp xác nhận. '
                   'Xóa trả lại SL hợp đồng mà phiếu đang giữ.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Người dùng bấm Xóa ở cột Hành động (mở màn chi tiết) hoặc bấm Xóa ở chân màn chi tiết.\n'
                    '2. Hệ thống hiển thị hộp “Xác nhận xóa”.\n3. Người dùng bấm Xóa.\n'
                    '4. Hệ thống kiểm tra trạng thái, người tạo.\n'
                    '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử của phiếu (kèm dòng dịch vụ, file), rồi xóa dòng yêu cầu, dòng '
                    'dịch vụ và phiếu.\n'
                    '6. Hệ thống hiển thị “Xóa thành công.” và quay về màn danh sách.',
              phu='• Bấm Hủy / (x) / click ra ngoài hộp → không xóa.\n'
                  '• Phiếu đã đổi trạng thái → ' + M_CONFLICT + '; không phải người tạo → “Bạn không có quyền xóa phiếu này”.\n'
                  '• Lỗi khác → “Xóa không thành công”.\n'
                  '• Phiếu đã bị xóa ở tab khác → lỗi chung của máy chủ “Item Not Found!”.',
              dacbiet='Ràng buộc dữ liệu cấp con: dòng dịch vụ / dòng yêu cầu là của chính phiếu nên bị xóa theo, không chặn. Ràng buộc '
                      'đang sử dụng: phiếu đã gửi duyệt hoặc đã có phiếu Hạch toán không còn ở Đang tạo / Không duyệt nên không xóa được '
                      '(nút ẩn). Hợp đồng, đơn bảo hiểm, yêu cầu mua dịch vụ không bị xóa; SL phiếu giữ được trả lại cho hợp đồng.'),
   layout=dict(menu=MENU + ' => Xem chi tiết => Xóa', shot=shot('13_delete'), shot_caption='Hộp xác nhận xóa phiếu',
               note='Modal Xác nhận xóa được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Xóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Ẩn',
        ['- Cột Hành động, biểu tượng thùng rác đỏ', '- Người tạo, phiếu Đang tạo / Không duyệt', '- Bấm → mở màn chi tiết phiếu']),
       ('Nút Xóa ở chân màn chi tiết', 'Button', 'Enable / Ẩn', 'Ẩn', ['- Màu đỏ, cùng điều kiện', '- Bấm → hộp Xác nhận xóa']),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', '“Xác nhận xóa”', 'Kèm nút (x) đóng.'),
       ('Nội dung', 'Label', 'Hiển thị', '–', DEL_MSG),
       ('Nút Xóa', 'Button', 'Enable / Disable', 'Hiển thị', ['- Xác nhận xóa phiếu', '- Khóa trong lúc đang xóa']),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Xóa thành công.”', '- Sai trạng thái: ' + M_CONFLICT, '- Không phải người tạo: “Bạn không có quyền xóa phiếu này”',
         '- Lỗi khác: “Xóa không thành công”'])],
   ev=[('Bấm Xóa ở cột Hành động', 'Click',
        'Before:\n– Nút chỉ hiện với người tạo, phiếu Đang tạo / Không duyệt.\nDuring:\n– Chuyển màn.\n'
        'After:\n– Mở màn chi tiết của phiếu (nút Xóa ở chân màn).'),
       ('Bấm Xóa ở chân màn chi tiết', 'Click',
        'Before:\n– Nút chỉ hiện khi đủ điều kiện.\nDuring:\n– Ghi nhận phiếu cần xóa.\nAfter:\n– Hiển thị hộp “Xác nhận xóa” nội dung ' + DEL_MSG + '.'),
       ('Bấm Xóa trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra phiếu Đang tạo / Không duyệt; sai → hiển thị ' + M_CONFLICT + ' và dừng xử lý.\n'
        '– Kiểm tra người đăng nhập là người tạo; sai → hiển thị “Bạn không có quyền xóa phiếu này” và dừng xử lý.\n'
        'During:\n– Phiếu không còn tồn tại → báo lỗi, không xóa.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa” (kèm dòng dịch vụ, file).\n'
        '– Xóa dòng yêu cầu, dòng dịch vụ, phiếu (trả lại SL cho hợp đồng).\n'
        '– Hiển thị “Xóa thành công.”, quay về danh sách.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài hộp', 'Click',
        'Before:\n– Hộp đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng hộp, phiếu giữ nguyên.')])

# ------------------------------------------------------------ 2.9
fr(9, 'Xem chi tiết phiếu', usecase=('FR-09', 'Xem chi tiết phiếu', 'view', A_LAP),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Xem chi tiết phiếu yêu cầu hạch toán mua dịch vụ',
              mota='Xem toàn bộ thông tin một phiếu ở chế độ chỉ đọc, dùng lại bố cục form Tạo / Sửa theo loại yêu cầu, kèm khối Lịch sử. '
                   'Chân màn hiện các nút thao tác theo vai trò và trạng thái, cùng điều kiện với cột Hành động ở danh sách.',
              tacnhan=TN_XEM,
              dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem của người dùng (Phần 2).\n'
                       '3. Phiếu Đang tạo chỉ người tạo xem được.',
              chinh='1. Người dùng bấm số phiếu ở danh sách (hoặc bấm thông báo).\n2. Hệ thống kiểm tra phạm vi xem.\n'
                    '3. Hệ thống mở màn “Chi tiết yêu cầu hạch toán mua dịch vụ: <số phiếu>”, hiện thông tin theo loại.\n'
                    '4. Hệ thống hiện nút ở chân màn theo vai trò và trạng thái; khối Lịch sử thu gọn.',
              phu='• Ngoài phạm vi / không tồn tại → chuyển sang trang “không tìm thấy”.\n'
                  '• Lỗi khác → “Lỗi khi tải phiếu”.\n'
                  '• Bấm số hợp đồng / phụ lục / hợp đồng mua → mở trên ERP ở tab mới; bấm số yêu cầu mua dịch vụ → mở màn chi tiết yêu '
                  'cầu mua dịch vụ ở tab mới.\n'
                  '• Phiếu Đang hạch toán / Đã hạch toán: chân màn chỉ còn In phiếu, Quay lại.\n'
                  '• Bấm Quay lại → về danh sách; bộ lọc được giữ nếu quay lại trong 10 phút.',
              dacbiet='Màn chi tiết là trang riêng, mọi ô chỉ đọc, không có nút lưu; bảng dịch vụ bỏ cột SL HĐ còn lại; không có file thì '
                      'hiện “Không có file đính kèm.”. Phiếu Không duyệt hiện Ghi chú duyệt.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn chi tiết phiếu Chờ duyệt — người có quyền Hạch toán'),
   extra=[('17b_detail_rejected', 'Màn chi tiết phiếu Không duyệt — có Ghi chú duyệt')],
   ui_kw=dict(required=False),
   ui=[('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Chi tiết yêu cầu hạch toán mua dịch vụ: <số phiếu>”.'),
       ('Khối Thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Người tạo – ngày giờ tạo ở góc phải', '- Loại yêu cầu, Hợp đồng mua dịch vụ (link ERP), Nhà cung cấp, Hóa đơn VAT, '
         'Diễn giải', '- Công nợ bảo hiểm: Số đơn bảo hiểm, Phụ lục bổ sung, Số hợp đồng mua (link ERP), Ghi chú',
         '- Ghi chú duyệt: chỉ khi phiếu có lý do Không duyệt']),
       ('3 khối thông tin bảo hiểm', 'Label', 'Read-only / Ẩn', '–', 'Theo dữ liệu',
        ['- Chỉ loại Công nợ bảo hiểm', '- Thông tin công ty bảo hiểm, người liên hệ, người đại diện']),
       ('Bảng File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, Upload / File, Dung lượng', '- Bấm tên file → xem trước', '- Rỗng: “Không có file đính kèm.”']),
       ('Bảng Danh sách dịch vụ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, Tên dịch vụ, ĐVT, Số lượng, Đơn giá, Thành tiền, Yêu cầu, SL hạch toán', '- Dòng Thành tiền, VAT (x%), '
         'Tổng thanh toán', '- Bấm số yêu cầu → mở yêu cầu mua dịch vụ ở tab mới', '- Rỗng: “Không có dữ liệu.”']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        ['- Nút “Xem lịch sử” / “Thu gọn”, kèm số mốc', '- Nội dung như mục 2.14']),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Người tạo, phiếu Đang tạo / Không duyệt', '- Bấm → màn Sửa (mục 2.7)']),
       ('Nút Hạch toán', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Phiếu Chờ duyệt, quyền Q1 cùng công ty', '- Bấm → mục 2.10']),
       ('Nút Không duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Màu đỏ, cùng điều kiện Hạch toán', '- Bấm → mục 2.11']),
       ('Nút In phiếu', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ xem trước bản in (mục 2.12).'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Màu đỏ; người tạo, phiếu Đang tạo / Không duyệt', '- Bấm → mục 2.8']),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- “Lỗi khi tải phiếu”: lỗi khác'])],
   ev=[('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phiếu tồn tại, nằm trong phạm vi xem; phiếu Đang tạo chỉ người tạo xem.\n'
        '– Sai → chuyển sang trang “không tìm thấy”, không hiện thông báo lỗi.\n'
        'During:\n– Nạp dữ liệu phiếu và cờ Sửa / Xóa / Hạch toán; dựng bố cục theo loại yêu cầu.\n'
        'After:\n– Hiển thị thông tin chỉ đọc, khối Lịch sử thu gọn; nút chân màn theo vai trò và trạng thái.'),
       ('Bấm link chứng từ', 'Click',
        'Before:\n– Ô có giá trị.\nDuring:\n– Xác định màn đích (ERP hoặc màn Yêu cầu mua dịch vụ).\nAfter:\n– Mở ở tab mới.'),
       ('Bấm tên file đính kèm', 'Click', 'Before:\n– File đã lưu.\nDuring:\n– Lấy đường dẫn file.\nAfter:\n– Mở cửa sổ xem trước file.'),
       ('Bấm Xem lịch sử', 'Click',
        'Before:\n– Khối Lịch sử đang thu gọn.\nDuring:\n– Nạp các mốc lịch sử.\nAfter:\n– Mở khối, nhãn đổi thành “Thu gọn” (mục 2.14).'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Màn chỉ đọc, không hỏi xác nhận.\nDuring:\n– Chuyển màn.\nAfter:\n– Về màn danh sách.')])

# ------------------------------------------------------------ 2.10
fr(10, 'Hạch toán phiếu (duyệt)', usecase=('FR-10', 'Hạch toán', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Hạch toán phiếu yêu cầu (thay cho thao tác Duyệt)',
              mota='Kế toán mở màn “Tạo phiếu hạch toán mua dịch vụ” với phiếu yêu cầu chọn sẵn để ghi sổ. Màn này không có nút Duyệt '
                   'riêng: trạng thái phiếu yêu cầu đi theo phiếu hạch toán — lưu nháp phiếu hạch toán → Đang hạch toán; Lưu và duyệt '
                   'phiếu hạch toán → Đã hạch toán; xóa phiếu hạch toán còn nháp → trở lại Chờ duyệt.',
              tacnhan=TN_KT, dieukien=DK_KT,
              chinh='1. Kế toán bấm Hạch toán (biểu tượng máy tính) ở cột Hành động hoặc ở chân màn chi tiết.\n'
                    '2. Hệ thống mở màn “Tạo phiếu hạch toán mua dịch vụ” với phiếu yêu cầu chọn sẵn, dữ liệu điền sẵn.\n'
                    '3. Kế toán hoàn thiện và lưu phiếu hạch toán (theo SRS màn Hạch toán mua dịch vụ).\n'
                    '4. Lưu nháp: phiếu yêu cầu chuyển Đang hạch toán.\n'
                    '5. Lưu và duyệt → hộp “Xác nhận duyệt” → Duyệt: ghi sổ, phiếu yêu cầu chuyển Đã hạch toán, ghi Người duyệt / Ngày '
                    'duyệt; SL đã hạch toán được cộng vào hợp đồng mua dịch vụ (loại Dịch vụ thuê ngoài) hoặc đơn bảo hiểm chuyển Đã hạch '
                    'toán (loại Công nợ bảo hiểm).\n'
                    '6. Mỗi lần đổi trạng thái, hệ thống ghi nhận hành động “Thay đổi trạng thái” kèm ghi chú “Từ phiếu hạch toán mua '
                    'dịch vụ” trong lịch sử của phiếu yêu cầu.',
              phu='• Bấm Hạch toán không có hộp xác nhận; hộp xác nhận ở bước Lưu và duyệt của phiếu hạch toán: tiêu đề “Xác nhận duyệt”, '
                  'nội dung “Phiếu đã duyệt sẽ ghi sổ kế toán và không sửa, xóa được nữa. Thao tác này có thể ảnh hưởng đến dữ liệu. '
                  'Bạn có muốn tiếp tục?” (Duyệt / Hủy); bấm Hủy → không lưu, phiếu yêu cầu giữ nguyên.\n'
                  '• Thoát màn Tạo phiếu hạch toán không lưu → phiếu yêu cầu giữ Chờ duyệt.\n'
                  '• Phiếu yêu cầu không còn Chờ duyệt hoặc người dùng không đủ quyền → “Phiếu yêu cầu – Không ở trạng thái Chờ duyệt '
                  'hoặc bạn không có quyền hạch toán phiếu này.”.\n'
                  '• Xóa phiếu hạch toán đang nháp → phiếu yêu cầu trở lại Chờ duyệt.\n'
                  '• Không đủ điều kiện → nút không hiện.',
              dacbiet='Chỉ người có quyền Hạch toán mua dịch vụ cùng công ty với phiếu (Super admin cũng phải có quyền). Màn Hạch toán '
                      'không gửi thông báo cho người tạo phiếu yêu cầu khi duyệt.'),
   layout=dict(menu=MENU + ' => Hạch toán', shot=shot('21_accounting_create'),
               shot_caption='Màn Tạo phiếu hạch toán mua dịch vụ mở từ phiếu yêu cầu'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Hạch toán trên dòng', 'Icon Button', 'Enable / Ẩn', 'Ẩn',
        ['- Cột Hành động, biểu tượng máy tính, chữ gợi ý “Hạch toán”', '- Phiếu Chờ duyệt, quyền Q1 cùng công ty']),
       ('Nút Hạch toán ở chân màn', 'Button', 'Enable / Ẩn', 'Ẩn', ['- Màn chi tiết, cùng điều kiện', '- Bấm → màn Tạo phiếu hạch toán']),
       ('Màn Tạo phiếu hạch toán mua dịch vụ', 'Label', 'Hiển thị', 'Ẩn',
        ['- Ô Phiếu yêu cầu chọn sẵn số phiếu', '- Nhà cung cấp, hợp đồng, dịch vụ, SL điền sẵn',
         '- Bố cục và quy tắc theo SRS màn Hạch toán mua dịch vụ']),
       ('Nút Lưu nháp (phiếu hạch toán)', 'Button', 'Enable', 'Hiển thị', 'Lưu phiếu hạch toán nháp → phiếu yêu cầu Đang hạch toán.'),
       ('Nút Lưu và duyệt (phiếu hạch toán)', 'Button', 'Enable', 'Hiển thị', 'Hỏi “Xác nhận duyệt” rồi ghi sổ → phiếu yêu cầu Đã hạch toán.'),
       ('Hộp Xác nhận duyệt', 'Popup', 'Hiển thị', 'Ẩn',
        ['- Tiêu đề “Xác nhận duyệt”', '- Nội dung như dòng sự kiện phụ', '- Nút Duyệt / Hủy']),
       ('Nút Quay lại (phiếu hạch toán)', 'Button', 'Enable', 'Hiển thị', 'Về danh sách phiếu hạch toán; chưa lưu → hộp Thông tin chưa lưu.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- “Thêm mới thành công.” / “Duyệt thành công.” (màn phiếu hạch toán)',
         '- “Phiếu yêu cầu – Không ở trạng thái Chờ duyệt hoặc bạn không có quyền hạch toán phiếu này.”'])],
   ev=[('Bấm Hạch toán', 'Click',
        'Before:\n– Kiểm tra phiếu Chờ duyệt, người dùng có quyền Hạch toán mua dịch vụ và cùng công ty với phiếu.\n'
        '– Không đủ điều kiện thì nút không hiện.\n'
        'During:\n– Chuyển sang màn Tạo phiếu hạch toán, gửi kèm phiếu yêu cầu.\n'
        'After:\n– Màn Tạo phiếu hạch toán tự nạp dữ liệu phiếu yêu cầu; chưa ghi dữ liệu nào.'),
       ('Lưu nháp phiếu hạch toán', 'System',
        'Before:\n– Kiểm tra lại phiếu yêu cầu Chờ duyệt và quyền; sai → “Phiếu yêu cầu – Không ở trạng thái Chờ duyệt hoặc bạn không '
        'có quyền hạch toán phiếu này.”.\nDuring:\n– Lưu phiếu hạch toán theo SRS màn Hạch toán mua dịch vụ.\n' + ERR + '\n'
        'After:\n– Phiếu yêu cầu chuyển Đang hạch toán; ghi lịch sử “Thay đổi trạng thái” Chờ duyệt → Đang hạch toán.'),
       ('Lưu và duyệt phiếu hạch toán', 'System',
        'Before:\n– Hộp “Xác nhận duyệt”; Hủy → dừng.\nDuring:\n– Ghi sổ kế toán; cộng SL đã hạch toán vào hợp đồng / chuyển đơn bảo '
        'hiểm Đã hạch toán.\n' + ERR + '\n'
        'After:\n– Phiếu yêu cầu chuyển Đã hạch toán, ghi Người duyệt, Ngày duyệt; ghi lịch sử “Thay đổi trạng thái”.'),
       ('Xóa phiếu hạch toán nháp', 'System',
        'Before:\n– Phiếu hạch toán chưa duyệt.\nDuring:\n– Xóa phiếu hạch toán.\n'
        'After:\n– Phiếu yêu cầu đang Đang hạch toán thì trở lại Chờ duyệt; ghi lịch sử “Thay đổi trạng thái”.')])

# ------------------------------------------------------------ 2.11
fr(11, 'Không duyệt phiếu', usecase=('FR-11', 'Không duyệt', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Không duyệt phiếu yêu cầu hạch toán mua dịch vụ',
              mota='Kế toán trả phiếu Chờ duyệt về trạng thái Không duyệt, bắt buộc nhập Ghi chú duyệt. Ghi chú hiện trên phiếu để người '
                   'tạo sửa lại, ghi vào lịch sử, gửi thông báo cho người tạo; hệ thống ghi Người duyệt / Ngày duyệt và trả lại SL hợp '
                   'đồng / đơn bảo hiểm mà phiếu đang giữ.',
              tacnhan=TN_KT, dieukien=DK_KT,
              chinh='1. Kế toán bấm Không duyệt ở cột Hành động hoặc ở chân màn chi tiết.\n'
                    '2. Hệ thống mở cửa sổ “Không duyệt yêu cầu hạch toán mua dịch vụ” (dòng phụ “Phiếu: <số phiếu>”), con trỏ đặt ở ô '
                    'Ghi chú duyệt.\n3. Kế toán nhập Ghi chú duyệt, bấm Không duyệt.\n'
                    '4. Hệ thống kiểm tra quyền, trạng thái, ghi chú.\n'
                    '5. Hệ thống chuyển phiếu sang Không duyệt, lưu Ghi chú duyệt, ghi Người duyệt / Ngày duyệt; loại Công nợ bảo hiểm '
                    'trả đơn bảo hiểm về Đã duyệt.\n'
                    '6. Hệ thống ghi nhận hành động “Thay đổi trạng thái” Chờ duyệt → Không duyệt kèm ghi chú trong lịch sử của phiếu.\n'
                    '7. Hệ thống gửi thông báo “[YCHTMDV] Từ chối: <số phiếu>” cho người tạo, kèm người từ chối và lý do.\n'
                    '8. Hệ thống hiển thị “Thao tác thành công.”: ở danh sách nạp lại bảng; ở màn chi tiết quay về danh sách.',
              phu='• Ghi chú trống (kể cả chỉ dấu cách) → “Bắt buộc phải nhập” dưới ô, không gửi.\n'
                  '• Bấm Hủy / (x) / click ra ngoài cửa sổ → đóng, không xử lý (nội dung đã nhập bị bỏ, không hỏi xác nhận).\n'
                  '• Thiếu quyền Hạch toán mua dịch vụ → ' + M_NOPERM + '; khác công ty → “Bạn không có quyền thao tác trên phiếu '
                  'này”; phiếu đã được xử lý → ' + M_CONFLICT + '.\n'
                  '• Ghi chú quá 255 ký tự → máy chủ báo lỗi độ dài, phiếu giữ Chờ duyệt.\n'
                  '• Lỗi khác → “Thao tác không thành công”.',
              dacbiet='Ghi chú tối đa 255 ký tự. Người tạo sửa và gửi lại được; phiếu Không duyệt không còn giữ SL hợp đồng. Khóa nút '
                      'Không duyệt trong lúc đang xử lý.'),
   layout=dict(menu=MENU + ' => Không duyệt', shot=shot('15_reject'), shot_caption='Cửa sổ Không duyệt phiếu',
               note='Modal Không duyệt yêu cầu hạch toán mua dịch vụ được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo '
                    'đường dẫn ở trên.'),
   extra=[('15b_reject_validate', 'Bấm Không duyệt khi chưa nhập Ghi chú duyệt')],
   ui=[('Nút Không duyệt trên dòng / chân màn', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
        ['- Màu đỏ, biểu tượng dấu x tròn', '- Phiếu Chờ duyệt, quyền Q1 cùng công ty', '- Bấm → mở cửa sổ Không duyệt']),
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Không duyệt yêu cầu hạch toán mua dịch vụ”',
        ['- Dòng phụ “Phiếu: <số phiếu>”', '- Có nút (x) đóng']),
       ('Ghi chú duyệt', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
        ['- 3 dòng, con trỏ đặt sẵn', '- Trống → “Bắt buộc phải nhập”, viền đỏ', '- Tự bỏ khoảng trắng đầu / cuối khi gửi']),
       ('Nút Không duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Màu đỏ', '- Khóa trong lúc đang xử lý']),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xử lý.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Thao tác thành công.”', '- Thiếu quyền: ' + M_NOPERM, '- Đã xử lý: ' + M_CONFLICT,
         '- Lỗi khác: “Thao tác không thành công”'])],
   ev=[('Bấm Không duyệt trên dòng / chân màn', 'Click',
        'Before:\n– Nút chỉ hiện với phiếu Chờ duyệt, quyền Q1 cùng công ty.\nDuring:\n– Xóa ghi chú cũ, tắt báo lỗi.\n'
        'After:\n– Mở cửa sổ Không duyệt, đặt con trỏ vào ô ghi chú.'),
       ('Bấm Không duyệt trong cửa sổ', 'Click',
        'Before:\n– Kiểm tra quyền Hạch toán mua dịch vụ; thiếu → hiển thị ' + M_NOPERM + ' và dừng xử lý.\n'
        '– Kiểm tra phiếu Chờ duyệt (khóa phiếu, kiểm lại); sai → ' + M_CONFLICT + '.\n'
        '– Kiểm tra cùng công ty; sai → “Bạn không có quyền thao tác trên phiếu này”.\n'
        'During:\n– Ghi chú trống → “Bắt buộc phải nhập”.\n– Ghi chú quá 255 ký tự → lỗi độ dài.\n' + ERR + '\n'
        'After:\n– Phiếu chuyển Không duyệt; lưu Ghi chú duyệt; ghi Người duyệt, Ngày duyệt; trả đơn bảo hiểm (loại Công nợ bảo hiểm).\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái” Chờ duyệt → Không duyệt kèm ghi chú.\n'
        '– Gửi thông báo “[YCHTMDV] Từ chối: <số phiếu>” cho người tạo.\n'
        '– Hiển thị “Thao tác thành công.”; danh sách nạp lại / màn chi tiết quay về danh sách.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả đã nhập ghi chú.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng cửa sổ, phiếu giữ Chờ duyệt.')])

# ------------------------------------------------------------ 2.12
fr(12, 'In phiếu và in danh sách', usecase=('FR-12', 'In phiếu', 'io', A_LAP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(ten='In phiếu / In danh sách yêu cầu hạch toán mua dịch vụ',
              mota='Xem trước bản in ngay trên màn hình (không mở tab mới) rồi in. In phiếu dựng theo mẫu in “Phiếu yêu cầu hạch toán '
                   'mua dịch vụ” của hệ thống, đầu trang là letterhead công ty ghi trên phiếu. In danh sách dựng theo mẫu “Danh sách yêu '
                   'cầu hạch toán mua dịch vụ” với toàn bộ phiếu khớp bộ lọc (tối đa 2.000 dòng).',
              tacnhan=TN_XEM, dieukien=DK_XEM.replace('3. Người dùng đang ở màn danh sách Yêu cầu hạch toán mua dịch vụ.',
                                                       '3. Người dùng đang ở màn danh sách hoặc màn chi tiết phiếu.'),
              chinh='1. Người dùng bấm In phiếu ở cột Hành động / chân màn chi tiết, hoặc bấm In danh sách trên thanh công cụ.\n'
                    '2. Hệ thống mở cửa sổ “Xem trước phiếu yêu cầu hạch toán mua dịch vụ” / “Xem trước danh sách yêu cầu hạch toán '
                    'mua dịch vụ”, hiện “Đang tải dữ liệu in…”.\n'
                    '3. Hệ thống kiểm tra phạm vi xem, dựng bản in và hiển thị.\n'
                    '4. Người dùng bấm In; hệ thống mở hộp thoại in của trình duyệt.',
              phu='• Bấm (x) / click ra ngoài cửa sổ → đóng.\n'
                  '• Ngoài phạm vi → “Bạn không có quyền xem phiếu này”.\n'
                  '• Thiếu mẫu in → “Không tìm thấy mẫu in "Phiếu yêu cầu hạch toán mua dịch vụ"” / “Không tìm thấy mẫu in "Danh sách '
                  'yêu cầu hạch toán mua dịch vụ"”.\n'
                  '• Danh sách vượt 2.000 dòng → không in, báo “Danh sách có <N> dòng, vượt mức in tối đa 2.000 dòng nên chưa in được. '
                  'Vui lòng thu hẹp bộ lọc …”.\n'
                  '• Bản in rỗng → “Không có dữ liệu để in”; lỗi khác → “Không tải được dữ liệu in”.',
              dacbiet='Letterhead bản in phiếu lấy theo công ty ghi trên phiếu (không theo người đang đăng nhập); bản in danh sách lấy theo '
                      'công ty của người in. Số tiền giữ tối đa 2 số lẻ. In không ghi dữ liệu, không ghi lịch sử.'),
   layout=dict(menu=MENU + ' => In phiếu', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   extra=[('18b_print_list', 'Cửa sổ Xem trước danh sách')],
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo thao tác',
        ['- “Xem trước phiếu yêu cầu hạch toán mua dịch vụ”', '- “Xem trước danh sách yêu cầu hạch toán mua dịch vụ”', '- Có nút (x)']),
       ('Nút In', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Cạnh tiêu đề cửa sổ', '- Khóa khi đang tải hoặc chưa có bản in', '- Bấm → hộp thoại in của trình duyệt']),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu in…”.'),
       ('Đầu bản in phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead công ty của phiếu', '- Tiêu đề “PHIẾU YÊU CẦU HẠCH TOÁN MUA DỊCH VỤ”, số phiếu, ngày lập (dd/mm/yyyy)',
         '- Loại yêu cầu, Hóa đơn VAT']),
       ('Thông tin phiếu trên bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Dịch vụ thuê ngoài: Nhà cung cấp, Hợp đồng mua dịch vụ, Diễn giải',
         '- Công nợ bảo hiểm: Số đơn bảo hiểm, Số hợp đồng mua, Phụ lục bổ sung, Ghi chú']),
       ('Bảng chi tiết bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Dịch vụ thuê ngoài: STT, Tên dịch vụ, ĐVT, Số lượng, Đơn giá, Thành tiền, Yêu cầu, SL hạch toán; 3 dòng tổng',
         '- Công nợ bảo hiểm: dòng bảo hiểm, Tổng trước thuế, VAT, Tổng sau thuế']),
       ('Bảng bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc', 'Các phiếu khớp bộ lọc + phạm vi quyền.'),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Theo mẫu', 'Theo mẫu in của hệ thống.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Bạn không có quyền xem phiếu này”', '- “Không tìm thấy mẫu in …”', '- Câu vượt 2.000 dòng',
         '- “Không có dữ liệu để in”', '- “Không tải được dữ liệu in”'])],
   ev=[('Bấm In phiếu', 'Click',
        'Before:\n– Kiểm tra phiếu nằm trong phạm vi xem; sai → “Bạn không có quyền xem phiếu này”.\n'
        'During:\n– Mở cửa sổ, hiện “Đang tải dữ liệu in…”; dựng bản in theo mẫu, letterhead theo công ty của phiếu.\n' + ERR + '\n'
        'After:\n– Hiển thị bản in, mở khóa nút In. Không ghi dữ liệu.'),
       ('Bấm In danh sách', 'Click',
        'Before:\n– Lấy bộ lọc + phạm vi quyền hiện tại.\nDuring:\n– Đếm số phiếu; vượt 2.000 → hiện câu nhắc thu hẹp bộ lọc.\n' + ERR + '\n'
        'After:\n– Hiển thị bản in danh sách.'),
       ('Bấm In', 'Click', 'Before:\n– Bản in đã tải xong.\nDuring:\n– Dựng trang in ẩn với đúng nội dung.\nAfter:\n– Mở hộp thoại in.'),
       ('Bấm (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Dọn trang in ẩn.\nAfter:\n– Đóng cửa sổ, màn giữ nguyên.')])

# ------------------------------------------------------------ 2.13
fr(13, 'Xuất Excel', usecase=('FR-13', 'Xuất Excel', 'io', A_LAP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất danh sách phiếu ra Excel',
              mota='Người dùng chọn trường và thứ tự cột trong cửa sổ “Chọn trường xuất file” rồi tải file gồm toàn bộ phiếu khớp bộ lọc và '
                   'phạm vi (không riêng trang đang xem). Màn không có xuất Excel một phiếu.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Xuất Excel trên thanh công cụ.\n'
                    '2. Hệ thống mở cửa sổ “Chọn trường xuất file” với 12 trường, tích sẵn đúng các cột đang hiện trên bảng.\n'
                    '3. Người dùng tích / bỏ tích, kéo đổi thứ tự, bấm Xuất file.\n'
                    '4. Hệ thống lấy toàn bộ phiếu theo bộ lọc + phạm vi quyền + sắp xếp, dựng file.\n'
                    '5. Hệ thống tải file “danh_sach_yeu_cau_hach_toan_mua_dich_vu.xlsx”, hiển thị “Xuất Excel thành công”.',
              phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → không xuất.\n'
                  '• Không có phiếu khớp bộ lọc → vẫn tải file, chỉ có tiêu đề cột.\n'
                  '• Lỗi → “Lỗi khi xuất Excel”.',
              dacbiet='Cấu trúc file: dòng 1 logo công ty; dòng 2 tiêu đề “Danh sách yêu cầu hạch toán mua dịch vụ”; dòng 3 tên cột gồm STT '
                      'rồi các trường đã chọn đúng thứ tự; Tổng thanh toán là ô số (cộng SUM được); ngày dạng dd/mm/yyyy hh:mm. Không giới '
                      'hạn số dòng. Khóa nút Xuất Excel trong lúc chờ file.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn trường xuất file”', 'Kèm nút (x) đóng.'),
       ('Danh sách trường', 'Table/Grid', 'Enable', '12 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Số phiếu, Loại yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán, Ngày tạo',
         '- Người tạo, Ngày duyệt, Người duyệt, Người cập nhật, Ngày cập nhật, Trạng thái']),
       ('Ô tích của trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Theo cột đang hiện', 'Tích: trường có trong file.'),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Thứ tự trong danh sách = thứ tự cột trong file.'),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/12 trường”.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi trường.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → đóng cửa sổ, tải file']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công”', '- Lỗi: “Lỗi khi xuất Excel”'])],
   ev=[('Bấm Xuất Excel', 'Click',
        'Before:\n– Nút khóa khi đang có lượt xuất chạy.\nDuring:\n– Tích sẵn các trường tương ứng cột đang hiện.\n'
        'After:\n– Mở cửa sổ “Chọn trường xuất file”.'),
       ('Kéo tay nắm', 'Drag', 'Before:\n– Áp cho mọi trường.\nDuring:\n– Đổi thứ tự.\nAfter:\n– Thứ tự mới là thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; khóa nút Xuất Excel.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc + phạm vi quyền (bỏ phân trang); dựng file với các cột đúng thứ tự đã chọn.\n' + ERR + '\n'
        'After:\n– Tải file “danh_sach_yeu_cau_hach_toan_mua_dich_vu.xlsx”; hiển thị “Xuất Excel thành công”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”; mở khóa nút.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ.')])

# ------------------------------------------------------------ 2.14
fr(14, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(ten='Xem lịch sử thay đổi của phiếu',
              mota='Xem các mốc thao tác trên một phiếu: Tạo mới, Thay đổi thông tin (trường cũ → mới, dòng dịch vụ thêm / xóa, file đính '
                   'kèm thêm / xóa), Thay đổi trạng thái (gửi duyệt, Không duyệt kèm ghi chú, Đang hạch toán / Đã hạch toán từ phiếu '
                   'hạch toán), Xóa; mỗi mốc ghi người thực hiện và thời điểm. Mở từ nút Lịch sử ở cột Hành động hoặc khối Lịch sử ở '
                   'màn chi tiết.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc trong nút “…”), hoặc bấm Xem lịch sử ở màn chi tiết.\n'
                    '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <số phiếu>” (hoặc mở khối Lịch sử).\n'
                    '3. Hệ thống hiển thị các mốc, mới nhất trên cùng.\n'
                    '4. Người dùng bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.',
              phu='• Phiếu tạo từ hệ thống ERP trước khi bật lịch sử → “Chưa có lịch sử thao tác nào.”.\n'
                  '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
                  '• Bấm tên file ở mốc File đính kèm → mở cửa sổ xem trước file.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; danh sách giữ nguyên trang, bộ lọc, sắp xếp.',
              dacbiet='Thứ tự: mới nhất trên cùng. Mỗi mốc: thời gian dd/mm/yyyy hh:mm, nhãn hành động có màu, “Người thực hiện: <tên> — '
                      '<phòng ban>”, nội dung cũ → mới. Trường theo dõi: Loại yêu cầu, Hợp đồng mua dịch vụ, Số đơn bảo hiểm, Nhà cung '
                      'cấp, Hóa đơn VAT, Thuế VAT (%), Diễn giải, Trạng thái, Ghi chú duyệt, File đính kèm, Dòng dịch vụ (Dịch vụ, Yêu '
                      'cầu, SL hạch toán, Đơn giá). Lưu không đổi gì thì không sinh mốc.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', ['- “Lịch sử thay đổi: <số phiếu>”', '- Có nút (x) đóng']),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Mới nhất trên cùng', '- Mỗi mốc: nhãn, thời điểm, người thực hiện']),
       ('Mốc Tạo mới', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Ghi khi lưu phiếu lần đầu.'),
       ('Mốc Thay đổi thông tin', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Trường đã đổi: cũ → mới', '- “Dòng dịch vụ thêm mới / đã xóa”', '- “File đính kèm thêm mới / đã xóa” (bấm tên file xem trước)']),
       ('Mốc Thay đổi trạng thái', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Trạng thái cũ → mới', '- Không duyệt: kèm ghi chú', '- Từ màn hạch toán: kèm “Từ phiếu hạch toán mua dịch vụ”']),
       ('Mốc Xóa', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Ghi khi người tạo xóa phiếu.'),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Mở / thu gọn vùng ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách', 'Trống', ['- Mặc định: trống (tất cả)', '- Các hành động đã có của phiếu']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Trống', ['- Mặc định: trống (tất cả)']),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', 'Gợi ý “Từ ngày”.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', 'Gợi ý “Đến ngày”.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', 'Xóa các ô lọc lịch sử.'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', ['- “Chưa có lịch sử thao tác nào.”', '- “Không có lịch sử phù hợp bộ lọc.”'])],
   ev=[('Mở lịch sử', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\nDuring:\n– Nạp các mốc lịch sử và danh mục ô lọc.\n'
        'After:\n– Hiển thị các mốc, mới nhất trên cùng; không có mốc → “Chưa có lịch sử thao tác nào.”.'),
       ('Đổi ô lọc lịch sử', 'Change',
        'Before:\n– Vùng ô lọc đang mở.\nDuring:\n– Lọc theo loại hành động, người thực hiện, khoảng ngày.\nAfter:\n– Hiển thị lại mốc khớp.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Xóa các ô lọc.\nAfter:\n– Hiển thị lại toàn bộ mốc.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không ghi gì.\nAfter:\n– Đóng cửa sổ, danh sách giữ nguyên.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu hạch toán mua dịch vụ; không lặp lại các quy tắc đã có trong SRS '
           'quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Trường theo loại yêu cầu', [
        '– Dịch vụ thuê ngoài: Hợp đồng mua dịch vụ, Nhà cung cấp, Hóa đơn VAT, Diễn giải, bảng Danh sách dịch vụ (nhập SL hạch toán).',
        '– Công nợ bảo hiểm: Số đơn bảo hiểm (Phụ lục, Số hợp đồng mua, 3 khối thông tin, bảng phí lấy theo đơn), Hóa đơn VAT, Ghi chú.',
        '– Đổi loại xóa dữ liệu nguồn của loại cũ; màn Sửa khóa Loại yêu cầu.'], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-02', 'Lưu nháp và Lưu và gửi duyệt', [
        '– Lưu nháp chỉ bắt buộc Loại yêu cầu; SL hạch toán không âm, không vượt; VAT 0–100.',
        '– Lưu và gửi duyệt bắt buộc Hóa đơn VAT; Kèm hóa đơn phải có ≥ 1 file; Dịch vụ thuê ngoài bắt buộc hợp đồng, nhà cung cấp, '
        'hợp đồng có dịch vụ, tổng SL > 0; Công nợ bảo hiểm bắt buộc đơn bảo hiểm.'], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-03', 'SL hạch toán còn lại của hợp đồng', [
        '– SL còn lại = SL dòng phân bổ − SL đã hạch toán − SL các phiếu Đang tạo / Chờ duyệt / Đang hạch toán khác đang giữ; không âm.',
        '– Khi lưu, máy chủ khóa các dòng hợp đồng rồi tính lại: 2 người lập song song không vượt được tổng.',
        '– Phiếu Không duyệt / đã xóa không còn giữ SL; màn Sửa không trừ phần chính phiếu đang giữ.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Chọn hợp đồng / đơn bảo hiểm', 'Xóa', 'Không duyệt']),
    ('BR-04', 'Vòng đời trạng thái', [
        '– Lưu nháp → Đang tạo; Lưu và gửi duyệt → Chờ duyệt.', '– Không duyệt → Không duyệt (sửa / xóa / gửi lại được).',
        '– Lưu nháp phiếu hạch toán → Đang hạch toán; duyệt phiếu hạch toán → Đã hạch toán; xóa phiếu hạch toán nháp → về Chờ duyệt.',
        '– Sửa / Xóa: người tạo, phiếu Đang tạo / Không duyệt.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Hạch toán', 'Không duyệt']),
    ('BR-05', 'Người xử lý', [
        '– Hạch toán, Không duyệt: người có quyền Hạch toán mua dịch vụ cùng công ty với phiếu, phiếu Chờ duyệt.',
        '– Super admin không tự có quyền này, phải được gán.'], ['Hạch toán', 'Không duyệt']),
    ('BR-06', 'Phạm vi xem', [
        '– Xét V1 → V2 → V3; không có quyền nào thì chỉ phiếu mình tạo.',
        '– Quyền Hạch toán cộng thêm phiếu Chờ duyệt cùng công ty và phiếu mình là Người duyệt.',
        '– Phiếu Đang tạo của người khác luôn ẩn.'], ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel']),
    ('BR-07', 'Thông báo', [
        '– Gửi duyệt → người có quyền Hạch toán mua dịch vụ cùng công ty (“[YCHTMDV] Chờ duyệt: <số phiếu>”).',
        '– Không duyệt → người tạo kèm người từ chối, lý do (“[YCHTMDV] Từ chối: <số phiếu>”).',
        '– Bấm thông báo mở màn chi tiết phiếu.'], ['Lập phiếu', 'Chỉnh sửa', 'Không duyệt']),
    ('BR-08', 'Nguồn chọn được', [
        '– Hợp đồng mua dịch vụ: đã duyệt, do chính người lập tạo.',
        '– Đơn bảo hiểm: đã duyệt, hoặc Đang hạch toán nhưng không còn phiếu nào giữ; một đơn chỉ một phiếu Chờ duyệt / Đang hạch '
        'toán / Đã hạch toán giữ.',
        '– Gửi duyệt loại Công nợ bảo hiểm chuyển đơn (+ phụ lục) sang Đang hạch toán; Không duyệt trả về Đã duyệt.'],
     ['Chọn hợp đồng / đơn bảo hiểm', 'Lập phiếu', 'Không duyệt']),
    ('BR-09', 'File đính kèm', [
        '– Chỉ nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; tối đa 20MB/file.',
        '– File tải lên ngay khi chọn nhưng chỉ gắn vào phiếu khi lưu; xóa file đã lưu có hiệu lực ngay và ghi lịch sử.'],
     ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-10', 'Tính duy nhất', [
        '– Số phiếu <mã công ty>.YCHTMDV.<năm><6 số> do hệ thống sinh, duy nhất, không sửa được.',
        '– Phiếu không có trường nghiệp vụ duy nhất; giới hạn dùng chung nguồn theo BR-03 và BR-08.'], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-11', 'Chuẩn hóa dữ liệu nhập', [
        '– Ô số (SL hạch toán, VAT) chỉ nhận số, hiển thị dấu phẩy ngăn nghìn, làm tròn 2 số lẻ khi lưu.',
        '– Diễn giải tối đa 1.000 ký tự, Ghi chú duyệt tối đa 255 ký tự; nhận mọi ký tự, hiển thị nguyên văn.',
        '– Dịch vụ, đơn giá, tổng tiền do máy chủ tính lại, không tin số gửi từ màn hình.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Không duyệt']),
    ('BR-12', 'Liên kết cha – con', [
        '– Dòng dịch vụ và dòng yêu cầu thuộc một phiếu; xóa phiếu xóa toàn bộ, không để dòng mồ côi.',
        '– Dòng yêu cầu phải thuộc hợp đồng đã chọn (“Dòng yêu cầu không thuộc hợp đồng đã chọn.”).',
        '– Đổi trạng thái không làm mất dòng dịch vụ, file, chứng từ nguồn.'], ['Lập phiếu', 'Chỉnh sửa', 'Xóa']),
    ('BR-13', 'Sử dụng ở màn khác', [
        '– Chỉ phiếu Chờ duyệt mới lập được phiếu Hạch toán mua dịch vụ.',
        '– Phiếu đã có phiếu hạch toán (Đang hạch toán / Đã hạch toán) không sửa, xóa, Không duyệt được.',
        '– Duyệt phiếu hạch toán cộng SL đã hạch toán vào hợp đồng mua dịch vụ.'], ['Hạch toán', 'Chỉnh sửa', 'Xóa']),
    ('BR-14', 'Quy tắc ghi lịch sử', [
        '– Ghi: Tạo mới, Thay đổi thông tin (cũ → mới, dòng dịch vụ, file), Thay đổi trạng thái (gửi duyệt, Không duyệt kèm ghi chú, '
        'đổi trạng thái từ phiếu hạch toán), Xóa.',
        '– Lưu không đổi gì thì không ghi; sửa kèm gửi duyệt ghi 2 mốc riêng.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Hạch toán', 'Không duyệt', 'Xem lịch sử thay đổi']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc dữ liệu do Yêu cầu hạch toán mua dịch vụ ghi ra (phiếu, dòng dịch vụ, số lượng hạch toán, file đính kèm và đơn bảo hiểm của phiếu).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Bán hàng', 'Hạch toán mua dịch vụ (chọn phiếu Chờ duyệt để lập phiếu hạch toán, nạp loại, nhà cung cấp, hợp đồng, dịch vụ, số lượng, file, đơn bảo hiểm; Lưu nháp → phiếu yêu cầu Đang hạch toán, Lưu và duyệt → Đã hạch toán; xóa phiếu hạch toán nháp trả phiếu yêu cầu về Chờ duyệt)', 'Bán hàng -> Yêu cầu -> Mua dịch vụ'),
    ('2', 'Tài chính', 'Hạch toán mua dịch vụ (như dòng 1)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Mua dịch vụ'),
    ('3', 'Hệ thống ERP', 'Hợp đồng mua dịch vụ (số lượng của phiếu Đang tạo / Chờ duyệt / Đang hạch toán được giữ chỗ khi tính số lượng còn lại; xóa phiếu thì trả lại số lượng)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('4', 'Hệ thống ERP', 'Đơn bảo hiểm (gửi duyệt phiếu loại Công nợ bảo hiểm thì đơn chuyển Đang hạch toán; Không duyệt trả đơn về Đã duyệt)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
