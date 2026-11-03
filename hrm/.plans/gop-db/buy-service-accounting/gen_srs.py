# -*- coding: utf-8 -*-
"""SRS màn "Hạch toán mua dịch vụ" (mã <mã công ty>.HTMDV.<năm><6 số>) — form chuẩn Danh mục quốc gia (03/11/2026).

Chạy: python gen_srs.py  → SRS - Hạch toán mua dịch vụ.docx
Khung: srs-documenter (SrsDoc) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc: ../buy-service-accounting-request/gen_srs.py.
Nguồn đọc 03/11/2026 (nhánh develop, cả 2 repo):
  BE  Modules/Finance/{Entities/BuyServiceAccounting/*, Services/BuyServiceAccountingService.php,
      Http/Controllers/V1/BuyServiceAccountingController.php, Http/Requests/BuyServiceAccounting/BuyServiceAccountingStoreRequest.php,
      Transformers/BuyServiceAccountingResource/*, Exports/BuyServiceAccountingListExport.php, Routes/api.php},
      app/ExcelExport/ExportColumnRegistry.php, app/Services/CatalogHistoryService.php, PermissionsTableSeeder (1702–1705).
  FE  pages/finance/buy-service-accountings/** (index, create, _id/index, _id/edit, components/{BuyServiceAccountingForm,
      AccountingServiceTable, InsuranceAccountingTable, AccountingEntriesTable}), buy-service-accounting-requests/components/
      {SourcePickerModal, InsuranceSection}, bill-payment-requests/components/AttachmentSection.vue, components/subsystem-menu/{sale-hub,finance}.js.
  Spec docs/superpowers/specs/gop-db/2026-10-12-buy-service-accounting-design.md + plan.md (fix #11708, #11712–#11715, #11840) — code thắng khi lệch.
Ảnh: ./htmdv_shots (dev-hrm 03/11/2026, DNS Admin, script htmdv_shots/_capture/capture.js; mọi yêu cầu ghi bị chặn ở trình duyệt).
  Dev chỉ có phiếu Đã duyệt → nút Sửa / Xóa, menu "…", màn Sửa, 2 hộp Xác nhận xóa chụp trên phiếu TPE.HTMDV.2026000060 với cờ
  is_can_edit / is_can_delete bật tạm trên trình duyệt (không ghi dữ liệu). Dev không có phiếu yêu cầu loại Công nợ bảo hiểm Chờ duyệt
  → không có ảnh form loại bảo hiểm. Ảnh menu dùng lại ảnh chụp cùng ngày của màn Yêu cầu (cùng 2 lối menu, có mục Hạch toán mua dịch vụ).
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

TEN = 'Hạch toán mua dịch vụ'
SHOTS = os.path.join(HERE, 'htmdv_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Bán hàng => Yêu cầu => Mua dịch vụ => Hạch toán mua dịch vụ'
MENU_TC = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mua dịch vụ => Hạch toán mua dịch vụ'
MENU_YC = 'Phân hệ Bán hàng => Yêu cầu => Mua dịch vụ => YC hạch toán mua dịch vụ'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Hạch toán mua dịch vụ.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_KT = 'Kế toán hạch toán'
A_XEM = 'Người xem phiếu'
Q_HT = 'Hạch toán mua dịch vụ'
TN_KT = ('Người dùng có quyền thực hiện chức năng: Hạch toán mua dịch vụ (kế toán; tài khoản Super admin cũng phải được gán quyền '
         'này mới thấy nút Tạo mới và lưu được).')
TN_XEM = ('Người dùng có quyền thực hiện chức năng: người tạo phiếu (phiếu của mình); người có một trong các quyền Xem hạch toán mua '
          'dịch vụ - theo tổng công ty, - theo công ty, - theo phòng ban (theo phạm vi ở Phần 2); tài khoản Super admin xem mọi phiếu.')
TN_SUA = ('Người dùng có quyền thực hiện chức năng: Hạch toán mua dịch vụ, đồng thời là chính người tạo phiếu (người khác kể cả '
          'Super admin không sửa / xóa được).')
DK_XEM = ('1. Người dùng đăng nhập thành công.\n'
          '2. Người dùng có quyền xem phiếu theo phạm vi ở Phần 2 (không có quyền nào thì chỉ thấy phiếu mình tạo).\n'
          '3. Người dùng đang ở màn danh sách Hạch toán mua dịch vụ.')
DK_SUA = ('1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Hạch toán mua dịch vụ và là người tạo phiếu.\n'
          '3. Phiếu đang ở trạng thái Đang tạo (lưu nháp, chưa ghi sổ).')
DK_TAO = ('1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Hạch toán mua dịch vụ.\n'
          '3. Có phiếu Yêu cầu hạch toán mua dịch vụ ở trạng thái Chờ duyệt, cùng công ty với người dùng.')

M_REQ = '“<Tên trường> – Bắt buộc phải nhập”'
M_CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
M_NOPERM = '“Bạn không có quyền thực hiện chức năng này”'
M_SRC = '“Phiếu yêu cầu – Không ở trạng thái Chờ duyệt hoặc bạn không có quyền hạch toán phiếu này.”'
TOAST_422 = '“Bạn chưa nhập đầy đủ thông tin.”'
DEL_MSG = '“Bạn có chắc muốn xóa bản ghi này không?”'
APPROVE_MSG = ('“Phiếu đã duyệt sẽ ghi sổ kế toán và không sửa, xóa được nữa. Thao tác này có thể ảnh hưởng đến dữ liệu. Bạn có '
               'muốn tiếp tục?”')
UNSAVED = ['- Tiêu đề “Thông tin chưa lưu”', '- Nội dung “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”',
           '- Nút Thoát: bỏ thay đổi, rời màn', '- Nút Ở lại: đóng hộp, giữ nguyên dữ liệu đang nhập']
STATUS_LIST = ['- Đang tạo: nhãn xám (phiếu lưu nháp)', '- Đã duyệt: nhãn xanh (đã ghi sổ)']

d = SrsDoc(out=OUT, menu=MENU, route='/finance/buy-service-accountings', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Bán hàng': 'menu_phanhe_banhang', 'Yêu cầu': 'menu_yeucau', 'Mua dịch vụ': 'menu_nhom_muadv',
    'Hạch toán mua dịch vụ': 'menu_muc_sale',
    'Phân hệ Tài chính': 'menu_phanhe_taichinh', 'Hàng hoá - Dịch vụ - Vận chuyển': 'menu_hhdvvc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Lưu và duyệt': 'btn_luuduyet',
    'In phiếu': 'btn_in_row', 'In danh sách': 'btn_indanhsach', 'Xuất Excel': 'btn_xuatexcel',
    'Lịch sử': 'btn_lichsu_row', 'Hạch toán': 'btn_hachtoan_yc',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Hạch toán mua dịch vụ (số phiếu dạng <mã công ty>.HTMDV.<năm><6 chữ số>, vd '
    'TPE.HTMDV.2026000060), màn cuối của chuỗi Mua dịch vụ (Yêu cầu mua dịch vụ → Hợp đồng mua dịch vụ → Yêu cầu hạch toán mua dịch '
    'vụ → Hạch toán mua dịch vụ), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ cách kế toán lập phiếu hạch toán từ một phiếu Yêu cầu hạch toán mua dịch vụ đang Chờ duyệt, theo 2 loại (Dịch vụ thuê '
    'ngoài, Công nợ bảo hiểm).',
    'Làm rõ thao tác Lưu và duyệt: ghi bút toán vào sổ kế toán và cập nhật các chứng từ liên quan (phiếu yêu cầu, hợp đồng mua dịch '
    'vụ, đơn bảo hiểm).',
])
d.p('Phạm vi chức năng (13 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Danh sách: Xem danh sách (2 lối vào: Bán hàng, Tài chính), Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột.',
    'Phiếu của kế toán: Lập phiếu (Lưu nháp / Lưu và tiếp tục), Chọn phiếu yêu cầu hạch toán, Chỉnh sửa, Xóa, Lưu và duyệt (ghi sổ).',
    'Xem: Xem chi tiết (kèm khối Hạch toán — bút toán Nợ / Có), In phiếu và In danh sách, Xuất Excel danh sách, Xem lịch sử thay đổi.',
    'Lối vào thứ 3: nút Hạch toán ở màn Yêu cầu hạch toán mua dịch vụ mở thẳng màn Tạo phiếu của màn này với phiếu yêu cầu chọn sẵn.',
    'Không thuộc màn này: không có Duyệt / Không duyệt riêng (Lưu và duyệt chính là duyệt; trả phiếu về được thực hiện ở màn Yêu cầu '
    'bằng Không duyệt), không có Khóa / Mở khóa, không có Import Excel, không có Xuất Excel một phiếu.',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phiếu là chứng từ ghi nhận chi phí mua dịch vụ và công nợ phải trả nhà cung cấp / công ty bảo hiểm.',
    'Khi Lưu và duyệt, phiếu sinh bút toán trong sổ kế toán (Nợ tài khoản chi phí, Nợ thuế GTGT 1331, Có tài khoản công nợ) — dữ '
    'liệu dùng cho sổ chi tiết tài khoản, báo cáo công nợ nhà cung cấp.',
    'Số lượng đã hạch toán được cộng vào hợp đồng mua dịch vụ để theo dõi phần còn lại; đơn bảo hiểm chuyển Đã hạch toán.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Mỗi phiếu lập từ đúng 1 phiếu Yêu cầu hạch toán mua dịch vụ đang Chờ duyệt, cùng công ty; một phiếu yêu cầu chỉ có 1 phiếu hạch toán.',
    'Lưu nháp chỉ bắt buộc Phiếu yêu cầu; Lưu và duyệt bắt buộc đủ trường và Tổng thanh toán > 0, hỏi xác nhận trước khi ghi sổ.',
    'SL hạch toán từng yêu cầu không âm, không vượt SL yêu cầu (áp cả khi lưu nháp). TK nợ thuộc nhánh 154 bắt buộc Mã vụ việc, nhánh '
    '642 bắt buộc Mã phí.',
    'Chỉ người tạo được Sửa / Xóa và chỉ khi phiếu Đang tạo; xóa là xóa hẳn, phiếu yêu cầu trở lại Chờ duyệt. Phiếu Đã duyệt không sửa, '
    'không xóa được.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu hạch toán mua dịch vụ', 'Chứng từ kế toán ghi nhận chi phí mua dịch vụ; số phiếu do hệ thống sinh dạng '
                                    '<mã công ty>.HTMDV.<năm><6 chữ số>.'),
    ('Phiếu yêu cầu', 'Phiếu Yêu cầu hạch toán mua dịch vụ (TPE.YCHTMDV…) mà phiếu hạch toán được lập từ đó; quyết định loại phiếu, '
                      'hợp đồng, dịch vụ, SL tối đa.'),
    ('Loại yêu cầu', 'Dịch vụ thuê ngoài (từ hợp đồng mua dịch vụ) · Công nợ bảo hiểm (từ đơn bảo hiểm); lấy theo phiếu yêu cầu, không '
                     'đổi được.'),
    ('SL yêu cầu', 'Số lượng ghi trên phiếu yêu cầu cho từng yêu cầu mua dịch vụ — trần của SL hạch toán.'),
    ('SL hạch toán', 'Số lượng kế toán ghi nhận cho từng yêu cầu mua dịch vụ; mặc định bằng SL yêu cầu.'),
    ('Tài khoản nợ / Tài khoản có', 'Tài khoản kế toán ghi Nợ (chi phí) / ghi Có (công nợ phải trả, mặc định 3311). Loại Công nợ bảo hiểm '
                                    'cố định Nợ 1541 / Có 3311.'),
    ('Mã phí / Mã vụ việc', 'Danh mục khoản mục chi phí / vụ việc gắn vào từng dòng dịch vụ; bắt buộc theo nhánh tài khoản nợ (642 / 154).'),
    ('Hóa đơn VAT', 'Kèm hóa đơn (VAT % theo phiếu yêu cầu, bắt buộc file khi duyệt) · Không kèm hóa đơn (VAT = 0).'),
    ('Tổng thanh toán', 'Dịch vụ thuê ngoài: Thành tiền + VAT; Công nợ bảo hiểm: Tổng sau thuế của đơn bảo hiểm.'),
    ('Bút toán', 'Dòng ghi sổ Nợ / Có sinh khi Lưu và duyệt, hiển thị ở khối Hạch toán của màn chi tiết.'),
    ('Ngày hạch toán', 'Thời điểm phiếu được Lưu và duyệt (ghi sổ).'),
    ('Trạng thái Đang tạo', 'Phiếu lưu nháp, chưa ghi sổ; người tạo sửa / xóa / duyệt được. Phiếu yêu cầu nguồn ở Đang hạch toán. Nhãn xám.'),
    ('Trạng thái Đã duyệt', 'Phiếu đã ghi sổ, trạng thái cuối, không sửa / xóa. Phiếu yêu cầu nguồn ở Đã hạch toán. Nhãn xanh.'),
    ('Cấu trúc phân cấp', 'Phiếu > dòng dịch vụ (Đơn giá, Mã phí, Mã vụ việc) > dòng yêu cầu mua dịch vụ (SL hạch toán); phiếu > file '
                          'đính kèm; phiếu Đã duyệt > bút toán. Loại Công nợ bảo hiểm không có dòng dịch vụ, chỉ 1 dòng bảo hiểm.'),
    ('NCC / HĐ / ĐVT', 'Nhà cung cấp / Hợp đồng / Đơn vị tính.'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn dùng 4 quyền: quyền thao tác “Hạch toán mua dịch vụ” (nhóm quyền Yêu cầu hạch toán mua dịch vụ) và 3 quyền xem theo cấp '
    '(nhóm quyền Hạch toán mua dịch vụ), cùng phân hệ Bán hàng.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q_HT, 'Hiện nút Tạo mới; mở được màn Tạo / Sửa, cửa sổ chọn phiếu yêu cầu, danh mục tài khoản / mã phí / vụ việc / nhà cung '
                 'cấp; lưu, sửa, xóa phiếu (sửa / xóa thêm điều kiện người tạo + Đang tạo). Cũng là quyền hiện nút Hạch toán ở màn Yêu cầu.'),
], widths=[0.8, 1.6, 3.6])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét từ trên xuống, có cấp nào áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem hạch toán mua dịch vụ - theo tổng công ty', 'Toàn bộ phiếu; có ô lọc Công ty. Tài khoản Super admin xem như V1.'),
    ('V2', 'Xem hạch toán mua dịch vụ - theo công ty', 'Phiếu thuộc công ty của người dùng.'),
    ('V3', 'Xem hạch toán mua dịch vụ - theo phòng ban', 'Phiếu thuộc phòng ban người dùng quản lý hoặc đang làm việc.'),
    ('—', '(không có quyền nào)', 'Phiếu mình tạo.'),
], widths=[0.8, 2.4, 2.8])
d.p('Mọi cấp: phiếu Đang tạo của người khác bị ẩn. Q1 không mở rộng phạm vi xem.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người tạo (Q1)', 'Q1 (không phải người tạo)', 'V1–V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅ (theo V)', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu', '✅', '✅', '❌', '❌'),
    ('FR-06 Chọn phiếu yêu cầu', '✅ (phiếu Chờ duyệt mình tạo)', '✅', '❌', '❌'),
    ('FR-07 Chỉnh sửa', '✅ (Đang tạo)', '❌', '❌', '❌'),
    ('FR-08 Xóa', '✅ (Đang tạo)', '❌', '❌', '❌'),
    ('FR-09 Xem chi tiết', '✅', '✅ (trong phạm vi V)', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-10 Lưu và duyệt (ghi sổ)', '✅ (Đang tạo)', '❌', '❌', '❌'),
    ('FR-11 In phiếu / In danh sách', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-12 Xuất Excel', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-13 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[2.0, 1.2, 1.3, 0.9, 1.1])
d.p('Màn không có Khóa / Mở khóa, Import Excel và Không duyệt nên ma trận không có cột quyền tương ứng. In, Xuất Excel, Xem lịch sử '
    'không gắn quyền riêng: ai xem được phiếu thì dùng được.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có Q1: không thấy nút Tạo mới; mở thẳng màn Tạo thì danh mục và cửa sổ chọn phiếu yêu cầu không tải được, bấm lưu bị máy '
    'chủ từ chối ' + M_NOPERM + '.',
    'Không có quyền xem nào: chỉ thấy phiếu do mình tạo; ô lọc Công ty / Phòng ban bị ẩn.',
    'Nút không đủ điều kiện thì ẩn hẳn, không hiện xám (cờ do máy chủ trả theo từng phiếu).',
    'Mở thẳng đường dẫn màn chi tiết / sửa của phiếu ngoài phạm vi hoặc không tồn tại → chuyển sang trang “không tìm thấy”; mở màn '
    'Sửa của phiếu không sửa được → tự chuyển sang màn chi tiết.',
    'Gọi thẳng chức năng bỏ qua giao diện → máy chủ từ chối: “Bạn không có quyền sửa phiếu này”, “Bạn không có quyền xóa phiếu này”, '
    '“Bạn không có quyền xem phiếu này”, ' + M_NOPERM + ' (thiếu Q1); phiếu sai trạng thái → ' + M_CONFLICT + '.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Nút / thao tác', 'Hiện khi', 'Vị trí'], [
    ('Tạo mới', 'Người dùng có Q1', 'Thanh công cụ của bảng'),
    ('Xuất Excel, In danh sách, Cấu hình cột', 'Luôn hiện', 'Thanh công cụ của bảng'),
    ('Sửa, Xóa', 'Người đăng nhập là người tạo và phiếu Đang tạo', 'Cột Hành động, chân màn chi tiết'),
    ('In phiếu, Lịch sử', 'Luôn hiện với phiếu xem được', 'Cột Hành động (vào nút “…” khi dòng có hơn 3 nút); màn chi tiết'),
    ('Lưu nháp, Lưu và duyệt', 'Màn Tạo, màn Sửa', 'Chân màn'),
    ('Lưu và tiếp tục', 'Chỉ màn Tạo', 'Chân màn'),
    ('Hạch toán (màn Yêu cầu)', 'Phiếu yêu cầu Chờ duyệt, người có Q1 cùng công ty', 'Màn Yêu cầu hạch toán mua dịch vụ'),
], widths=[1.6, 3.0, 1.8])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_KT, [0, 1, 2, 3, 4, 5, 6]), (A_XEM, [0, 5, 6])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu', 'crud'),
     ('FR-07', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-08', 'Xóa phiếu', 'action'),
     ('FR-10', 'Lưu và duyệt', 'action'),
     ('FR-11', 'In phiếu', 'io'),
     ('FR-12', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-09', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn phiếu yêu cầu', 'crud', 'extend', [1], None)],
    'Sơ đồ Use Case tổng quan màn Hạch toán mua dịch vụ')

d.h2('2 Đặc tả chi tiết từng chức năng')


# ------------------------------------------------------------ Form Tạo / Sửa (dùng chung 2.5 + 2.7)
def form_ui(edit):
    rows = [
        ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–',
         '“Sửa phiếu hạch toán mua dịch vụ: <số phiếu>”' if edit else '“Tạo phiếu hạch toán mua dịch vụ”',
         ['- Cũng là tiêu đề tab trình duyệt',
          '- Màn Sửa ghép số phiếu sau khi nạp xong phiếu' if edit else '- Không có ô Số phiếu: số phiếu sinh khi lưu',
          '- Khung form hiện ngay, dữ liệu đổ vào khi tải xong' if edit else '- Không hiện nhãn trạng thái']),
        ('Dòng người tạo', 'Label', 'Read-only', '–', '–',
         'Người tạo – ngày giờ tạo' if edit else 'Người đăng nhập – thời điểm hiện tại',
         ['- Góc phải tiêu đề khối Thông tin chung', '- Không sửa được']),
        ('Phiếu yêu cầu', 'Textbox', 'Enable' if not edit else 'Read-only', 'Phiếu Chờ duyệt do mình tạo', 'Có',
         'Theo phiếu' if edit else 'Trống (hoặc điền sẵn khi vào từ nút Hạch toán)',
         ['- Màn Tạo: ô chọn, gợi ý “Chọn phiếu yêu cầu...”, biểu tượng kính lúp; bấm ô → cửa sổ chọn phiếu yêu cầu (mục 2.6)',
          '- Nút × bỏ chọn: xóa loại, VAT, hợp đồng, NCC, 2 tài khoản, dòng dịch vụ, thông tin bảo hiểm và file kế thừa (giữ file tự tải, '
          'Diễn giải)',
          '- Màn Sửa: link số phiếu yêu cầu, mở màn chi tiết phiếu yêu cầu ở tab mới; không đổi được',
          '- Trống khi lưu (kể cả Lưu nháp) → “Phiếu yêu cầu – Bắt buộc phải nhập”']),
        ('Loại yêu cầu', 'Textbox', 'Disable', '2 giá trị', '–', 'Gợi ý “Lấy theo phiếu yêu cầu”',
         ['- Tự điền: Dịch vụ thuê ngoài hoặc Công nợ bảo hiểm', '- Quyết định bố cục form (BR-01); chưa chọn phiếu thì hiện bố cục '
          'Dịch vụ thuê ngoài']),
        ('Hợp đồng mua dịch vụ', 'Link', 'Read-only / Ẩn', '–', '–', 'Gợi ý “Lấy theo phiếu yêu cầu”',
         ['- Chỉ loại Dịch vụ thuê ngoài', '- Số hợp đồng là link mở hợp đồng trên ERP ở tab mới']),
        ('Số đơn bảo hiểm', 'Link', 'Read-only / Ẩn', '–', '–', 'Trống',
         ['- Chỉ loại Công nợ bảo hiểm', '- Link mở đơn bảo hiểm trên ERP ở tab mới']),
        ('Phụ lục bổ sung', 'Link', 'Read-only / Ẩn', '–', '–', 'Trống', ['- Chỉ loại Công nợ bảo hiểm', '- Link ERP ở tab mới']),
        ('Số hợp đồng mua', 'Link', 'Read-only / Ẩn', '–', '–', 'Trống', ['- Chỉ loại Công nợ bảo hiểm', '- Link ERP ở tab mới']),
        ('Hóa đơn VAT', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có (khi Lưu và duyệt)', 'Theo phiếu yêu cầu',
         ['- Gợi ý “Chọn hóa đơn VAT”', '- Kèm hóa đơn', '- Không kèm hóa đơn',
          '- Kèm hóa đơn → VAT % = VAT của phiếu yêu cầu, hiện dòng VAT ở bảng dịch vụ, khối File đính kèm thành bắt buộc',
          '- Không kèm hóa đơn → VAT % = 0, ẩn dòng VAT',
          '- Trống khi Lưu và duyệt → “Hóa đơn VAT – Bắt buộc phải nhập”']),
        ('Nhà cung cấp', 'Dropdown', 'Enable / Ẩn', 'Danh sách nhà cung cấp', 'Có (khi Lưu và duyệt)', 'Theo phiếu yêu cầu',
         ['- Chỉ loại Dịch vụ thuê ngoài; gợi ý “Chọn nhà cung cấp” (“Đang tải...” khi đang nạp)',
          '- Mặc định theo phiếu yêu cầu, dạng “Mã - Tên”; kế toán đổi được',
          '- Trống khi Lưu và duyệt → “Nhà cung cấp – Bắt buộc phải nhập”; không tồn tại → “Nhà cung cấp – Không tồn tại”']),
        ('Tài khoản nợ', 'Dropdown', 'Enable / Disable', 'Danh mục tài khoản đang hoạt động', 'Có (khi Lưu và duyệt)',
         'Trống (loại bảo hiểm: 1541)',
         ['- Gợi ý “Chọn tài khoản nợ”, dạng “<số TK> - <tên>”; tài khoản đã khóa vẫn hiện tên (🔒) nếu phiếu đang dùng',
          '- Loại Công nợ bảo hiểm: cố định 1541, khóa ô',
          '- Đổi tài khoản → xóa lỗi Mã phí / Mã vụ việc đang hiện; nhánh 154 → cột Mã vụ việc bắt buộc; nhánh 642 → cột Mã phí bắt buộc',
          '- Trống khi Lưu và duyệt → “Tài khoản nợ – Bắt buộc phải nhập”']),
        ('Tài khoản có', 'Dropdown', 'Enable / Disable', 'Danh mục tài khoản đang hoạt động', 'Có (khi Lưu và duyệt)', '3311',
         ['- Gợi ý “Chọn tài khoản có”; mặc định 3311 ngay khi mở màn Tạo',
          '- Loại Công nợ bảo hiểm: cố định 3311, khóa ô',
          '- Trống khi Lưu và duyệt → “Tài khoản có – Bắt buộc phải nhập”']),
        ('Diễn giải', 'Textarea', 'Enable', '0–1.000 ký tự', 'Không', 'Trống',
         ['- Một nhãn “Diễn giải” cho cả 2 loại, 2 dòng, gợi ý “Nhập diễn giải”', '- Không gõ được quá 1.000 ký tự; nhận mọi ký tự']),
        ('Khối thông tin bảo hiểm', 'Label', 'Read-only / Ẩn', '–', '–', 'Trống',
         ['- Chỉ loại Công nợ bảo hiểm; lấy theo phiếu yêu cầu',
          '- Thông tin công ty bảo hiểm, người liên hệ, người đại diện (như màn Yêu cầu), không sửa được']),
        ('Nút Thêm tài liệu', 'Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Ở tiêu đề khối File đính kèm',
          '- Chữ gợi ý “Chấp nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip — tối đa 20MB/file”']),
        ('Bảng File đính kèm', 'Table/Grid', 'Enable', '9 đuôi file, ≤ 20MB/file', 'Có (khi Kèm hóa đơn và Lưu và duyệt)',
         'Theo phiếu' if edit else 'File của phiếu yêu cầu',
         ['- Cột STT, “Upload / File” (biểu tượng + tên file), Dung lượng; bấm tên file → xem trước',
          '- Màn Tạo: file của phiếu yêu cầu hiện sẵn ngay khi chọn phiếu (kèm dung lượng), gỡ được khỏi phiếu',
          '- Sai đuôi → “File "<tên file>" không thuộc định dạng cho phép”; quá 20MB → “File "<tên file>" vượt quá 20MB”',
          '- Kèm hóa đơn mà chưa có file khi Lưu và duyệt → “File đính kèm – Bắt buộc khi kèm hóa đơn VAT”']),
        ('Nút Xóa file', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         ['- File chưa lưu / file kế thừa: bỏ khỏi danh sách ngay (không xóa file của phiếu yêu cầu)',
          '- File đã lưu (màn Sửa): hỏi xác nhận rồi xóa ngay khỏi phiếu']),
        ('Bảng Chi tiết (dịch vụ)', 'Table/Grid', 'Enable / Ẩn', '–', 'Có (khi Lưu và duyệt)',
         'Theo phiếu' if edit else '“Chọn phiếu yêu cầu để nạp danh sách dịch vụ.”',
         ['- Chỉ loại Dịch vụ thuê ngoài; mỗi dịch vụ gộp ô theo số yêu cầu mua dịch vụ',
          '- Cột STT, Tên dịch vụ, ĐVT (“Gói”), Số lượng (= tổng SL hạch toán), Đơn giá, Thành tiền, nhóm Chi tiết (Yêu cầu, SL yêu cầu, '
          'SL hạch toán), Mã phí, Mã vụ việc',
          '- Yêu cầu: số yêu cầu mua dịch vụ (link tab mới) + người tạo',
          '- Phiếu yêu cầu không có dòng dịch vụ khi Lưu và duyệt → “Danh sách dịch vụ – Phiếu yêu cầu chưa có dòng dịch vụ nào”']),
        ('Ô Đơn giá', 'Textbox', 'Enable', '≥ 0', 'Có (khi Lưu và duyệt)', 'Đơn giá phiếu yêu cầu',
         ['- Gợi ý “Nhập đơn giá”, số có dấu phẩy ngăn nghìn', '- Âm → “Đơn giá – Không được nhỏ hơn 0” (cả Lưu nháp)',
          '- Trống khi Lưu và duyệt → “Đơn giá – Bắt buộc phải nhập”']),
        ('Ô SL hạch toán', 'Textbox', 'Enable', '0 ≤ SL ≤ SL yêu cầu', 'Có', 'SL yêu cầu',
         ['- Gợi ý “Nhập SL hạch toán”', '- Âm → “SL hạch toán – Không được nhỏ hơn 0”',
          '- Lớn hơn SL yêu cầu → “SL hạch toán – Không được vượt SL yêu cầu (<SL yêu cầu>)”; báo đỏ, không tự kéo về trần (cả Lưu nháp)']),
        ('Ô Mã phí', 'Dropdown', 'Enable', 'Danh mục mã phí đang hoạt động', 'Có khi TK nợ nhánh 642', 'Trống',
         ['- Gợi ý “Chọn mã phí”', '- Đổi ở dòng ĐẦU → áp cho mọi dòng; đổi ở dòng khác chỉ áp dòng đó',
          '- Thiếu khi bắt buộc → “Mã phí – Bắt buộc phải nhập”']),
        ('Ô Mã vụ việc', 'Dropdown', 'Enable', 'Danh mục vụ việc đang hoạt động', 'Có khi TK nợ nhánh 154', 'Trống',
         ['- Gợi ý “Chọn mã vụ việc”', '- Đổi ở dòng ĐẦU → áp cho mọi dòng',
          '- Thiếu khi bắt buộc → “Mã vụ việc – Bắt buộc phải nhập”']),
        ('Dòng Thành tiền', 'Label', 'Read-only', '≥ 0', '–', '0', 'Tổng Thành tiền các dịch vụ, tính lại ngay khi đổi SL / Đơn giá.'),
        ('Ô VAT (%)', 'Textbox', 'Enable / Ẩn', '0–100', 'Không', 'VAT của phiếu yêu cầu',
         ['- Chỉ hiện khi Kèm hóa đơn; bên phải hiện tiền VAT', '- Ngoài 0–100 → “VAT (%) – Phải trong khoảng 0 đến 100”']),
        ('Dòng Tổng thanh toán', 'Label', 'Read-only', '> 0 khi duyệt', '–', '0',
         ['- Thành tiền + tiền VAT; máy chủ tự tính lại khi lưu', '- Bằng 0 khi Lưu và duyệt → “Tổng thanh toán – Phải lớn hơn 0 trước khi '
          'duyệt”']),
        ('Bảng Thông tin chi tiết (bảo hiểm)', 'Table/Grid', 'Enable / Ẩn', '1 dòng', '–', '“Chọn phiếu yêu cầu để nạp thông tin.”',
         ['- Chỉ loại Công nợ bảo hiểm: STT, Dịch vụ đi kèm (“Bảo hiểm hàng hóa nhập khẩu”), Phí bảo hiểm, Tổng thanh toán, Mã phí, Vụ việc',
          '- Dòng Tổng trước thuế, VAT (x%), Tổng sau thuế (chỉ đọc); chỉ chọn được Mã phí, Vụ việc']),
        ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         ['- Lưu phiếu ở trạng thái Đang tạo, không ghi sổ', '- Chỉ bắt buộc Phiếu yêu cầu (BR-02)', '- Khóa trong lúc đang lưu']),
        ('Nút Lưu và duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         ['- Kiểm tra đủ trường; hết lỗi mới hỏi “Xác nhận duyệt” (mục 2.10)', '- Duyệt → ghi sổ, phiếu Đã duyệt',
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
         ['- Lưu nháp thành công: “Cập nhật thành công.”' if edit else '- Lưu nháp thành công: “Thêm mới thành công.”',
          '- Lưu và duyệt thành công: “Duyệt thành công.”', '- Thiếu / sai dữ liệu: ' + TOAST_422,
          '- Lỗi nghiệp vụ máy chủ trả: hiện nguyên văn (vd ' + M_SRC + (', ' + M_CONFLICT + ')' if edit else ')'),
          '- Lỗi khác: “Lỗi khi lưu phiếu”']),
        ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', UNSAVED),
    ]
    return rows


def save_ev(edit):
    if edit:
        ev = [('Mở màn Sửa', 'System',
               'Before:\n– Kiểm tra phiếu tồn tại và nằm trong phạm vi xem; sai → chuyển sang trang “không tìm thấy”.\n'
               'During:\n– Nạp dữ liệu phiếu, dòng dịch vụ kèm SL yêu cầu (trần), danh mục tài khoản / mã phí / vụ việc (giữ cả mục đã '
               'khóa mà phiếu đang dùng), danh sách nhà cung cấp.\n'
               '– Phiếu không sửa được (không phải người tạo hoặc không ở Đang tạo) → tự chuyển sang màn chi tiết.\n'
               'After:\n– Hiển thị form với dữ liệu phiếu, Phiếu yêu cầu thành link chỉ đọc; tiêu đề “Sửa phiếu hạch toán mua dịch vụ: '
               '<số phiếu>”.\n– Chốt mốc “chưa đổi gì” để so khi rời màn.')]
    else:
        ev = [('Bấm nút Tạo mới (hoặc nút Hạch toán ở màn Yêu cầu)', 'Click',
               'Before:\n– Nút Tạo mới chỉ hiện với người có quyền Hạch toán mua dịch vụ.\n'
               'During:\n– Dựng form trống; nạp danh mục tài khoản, mã phí, vụ việc, nhà cung cấp; Tài khoản có mặc định 3311.\n'
               '– Vào từ nút Hạch toán: nạp ngay phiếu yêu cầu được chọn sẵn và coi đó là trạng thái gốc (rời màn ngay không hỏi).\n'
               'After:\n– Mở màn “Tạo phiếu hạch toán mua dịch vụ”; bảng dịch vụ hiện câu hướng dẫn chọn phiếu yêu cầu.')]
    ev += [
        ('Đổi Hóa đơn VAT', 'Change',
         'Before:\n– Áp cả 2 loại.\n'
         'During:\n– Kèm hóa đơn → VAT % = VAT của phiếu yêu cầu; Không kèm hóa đơn → VAT % = 0.\n'
         'After:\n– Hiện / ẩn dòng VAT, tính lại Tổng thanh toán; khối File đính kèm thành bắt buộc / không bắt buộc; xóa lỗi đang hiện.'),
        ('Đổi Tài khoản nợ', 'Change',
         'Before:\n– Chỉ loại Dịch vụ thuê ngoài (loại bảo hiểm khóa ô).\n'
         'During:\n– Xác định nhánh tài khoản: thuộc 154 → Mã vụ việc bắt buộc; thuộc 642 → Mã phí bắt buộc.\n'
         'After:\n– Hiện / ẩn dấu * ở tiêu đề cột Mã phí, Mã vụ việc; xóa lỗi Mã phí / Mã vụ việc đang hiện.'),
        ('Nhập Đơn giá hoặc SL hạch toán', 'Change',
         'Before:\n– Chỉ nhận số.\nDuring:\n– Cộng lại Số lượng, Thành tiền của dịch vụ và 3 dòng tổng.\n'
         '– Âm hoặc vượt SL yêu cầu chỉ báo khi bấm lưu.\n'
         'After:\n– Cập nhật số trên bảng; xóa lỗi đang hiện của ô.'),
        ('Đổi Mã phí / Mã vụ việc ở dòng đầu', 'Change',
         'Before:\n– Ô ở dòng dịch vụ đầu tiên.\nDuring:\n– Áp giá trị mới cho mọi dòng dịch vụ (dòng khác chỉ áp riêng dòng đó).\n'
         'After:\n– Cập nhật các ô, xóa lỗi tương ứng.'),
        ('Chọn tệp đính kèm', 'Change',
         'Before:\n– Chỉ nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; tối đa 20MB/file.\n'
         'During:\n– Sai đuôi → “File "<tên file>" không thuộc định dạng cho phép”.\n'
         '– Quá dung lượng → “File "<tên file>" vượt quá 20MB”.\n' + ERR + '\n'
         'After:\n– Tải file lên kho lưu trữ ngay, hiện tên file và dung lượng; file chỉ gắn vào phiếu khi bấm lưu.'),
    ]
    if edit:
        ev.append(('Bấm Xóa file đã lưu', 'Click',
                   'Before:\n– Kiểm tra phiếu Đang tạo (sai → ' + M_CONFLICT + ') và người tạo (sai → “Bạn không có quyền sửa phiếu '
                   'này”).\n– Hiển thị hộp xác nhận xóa file; Hủy → dừng.\n'
                   'During:\n– File không thuộc phiếu → “Không tìm thấy file trong phiếu”.\n' + ERR + '\n'
                   'After:\n– Bỏ file khỏi phiếu ngay (không cần bấm lưu).\n'
                   '– Ghi một dòng lịch sử “Thay đổi thông tin” (File đính kèm đã xóa).\n– Hiển thị “Xóa thành công.”.'))
    perm = ('Before:\n– Kiểm tra quyền Hạch toán mua dịch vụ; không có → hiển thị ' + M_NOPERM + ' và dừng xử lý.\n'
            '– Kiểm tra phiếu còn Đang tạo; sai → hiển thị ' + M_CONFLICT + ' và dừng xử lý.\n'
            '– Kiểm tra người đăng nhập là người tạo; sai → hiển thị “Bạn không có quyền sửa phiếu này” và dừng xử lý.\n') if edit else \
           ('Before:\n– Kiểm tra quyền Hạch toán mua dịch vụ; không có → hiển thị ' + M_NOPERM + ' và dừng xử lý.\n'
            '– Khóa phiếu yêu cầu trong lúc lưu; phiếu yêu cầu không còn Chờ duyệt / khác công ty → ' + M_SRC + '\n'
            '– Khóa các nút lưu trong lúc đang lưu.\n')
    log_draft = ('– Ghi một dòng lịch sử “Thay đổi thông tin” chỉ với trường / dòng dịch vụ / file đã đổi (cũ → mới).\n' if edit else
                 '– Sinh số phiếu <mã công ty>.HTMDV.<năm><6 số>; công ty, phòng ban, bộ phận theo người tạo.\n'
                 '– Ghi một dòng lịch sử “Tạo mới” của phiếu.\n'
                 '– Phiếu yêu cầu nguồn chuyển Đang hạch toán; ghi lịch sử “Thay đổi trạng thái” bên phiếu yêu cầu kèm “Từ phiếu '
                 'hạch toán mua dịch vụ”.\n')
    ev += [
        ('Bấm Lưu nháp', 'Click', perm +
         'During:\n– Phiếu yêu cầu trống → “Phiếu yêu cầu – Bắt buộc phải nhập”.\n'
         '– Đơn giá âm → “Đơn giá – Không được nhỏ hơn 0”; SL hạch toán âm → “SL hạch toán – Không được nhỏ hơn 0”; vượt SL yêu cầu → '
         '“SL hạch toán – Không được vượt SL yêu cầu (<SL>)”; VAT ngoài 0–100 → “VAT (%) – Phải trong khoảng 0 đến 100”.\n'
         '– Dòng không thuộc phiếu yêu cầu → “Dịch vụ – Không thuộc phiếu yêu cầu đã chọn” / “SL hạch toán – Dòng yêu cầu không thuộc '
         'phiếu yêu cầu đã chọn”.\n'
         '– Có lỗi → hiển thị ' + TOAST_422 + ', cuộn tới ô lỗi đầu tiên.\n' + ERR + '\n'
         'After:\n– Lưu phiếu ở trạng thái Đang tạo; ô trống ghi rỗng; tổng tiền máy chủ tự tính; chưa ghi sổ.\n' + log_draft +
         '– Hiển thị “' + ('Cập nhật thành công.' if edit else 'Thêm mới thành công.') + '” và quay về màn danh sách (Back của '
         'trình duyệt không quay lại form vừa lưu).'),
        ('Bấm Lưu và duyệt', 'Click',
         'Before:\n– Kiểm tra trên màn hình đủ trường bắt buộc (như During); còn lỗi thì không mở hộp xác nhận.\n'
         '– Hết lỗi → hiển thị hộp “Xác nhận duyệt”; quy trình ghi sổ ở mục 2.10.\n'
         'During:\n– Thiếu Hóa đơn VAT / Nhà cung cấp / Tài khoản nợ / Tài khoản có / Đơn giá → ' + M_REQ + '.\n'
         '– Kèm hóa đơn mà chưa có file → “File đính kèm – Bắt buộc khi kèm hóa đơn VAT”; Tổng thanh toán = 0 → “Tổng thanh toán – Phải '
         'lớn hơn 0 trước khi duyệt”.\n'
         '– TK nợ nhánh 154 thiếu Mã vụ việc / nhánh 642 thiếu Mã phí → “Mã vụ việc – Bắt buộc phải nhập” / “Mã phí – Bắt buộc phải nhập”.\n'
         '– Có lỗi → hiển thị ' + TOAST_422 + ', cuộn tới ô lỗi đầu tiên.\n' + ERR + '\n'
         'After:\n– Mở hộp “Xác nhận duyệt” (Duyệt / Hủy); bấm Duyệt thì xử lý như mục 2.10.'),
    ]
    if not edit:
        ev.append(('Bấm Lưu và tiếp tục', 'Click',
                   'Before:\n– Chỉ có ở màn Tạo; khóa nút trong lúc đang lưu; kiểm quyền như Lưu nháp.\n'
                   'During:\n– Kiểm tra như Lưu nháp (chỉ bắt buộc Phiếu yêu cầu, Đơn giá / SL không âm, SL không vượt).\n' + ERR + '\n'
                   'After:\n– Lưu phiếu Đang tạo, ghi lịch sử “Tạo mới”, phiếu yêu cầu chuyển Đang hạch toán, hiển thị “Thêm mới thành '
                   'công.”.\n– Ở lại màn Tạo, form trống như lúc mới vào (không còn phiếu yêu cầu chọn sẵn).'))
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
       ten='Truy cập và xem danh sách phiếu hạch toán mua dịch vụ',
       mota='Hiển thị bảng phiếu hạch toán mua dịch vụ nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân trang, sắp xếp và tổng '
            'số phiếu khớp bộ lọc. Mỗi dòng cho biết phiếu yêu cầu nguồn, hợp đồng, nhà cung cấp, tổng thanh toán, ngày hạch toán và '
            'trạng thái ghi sổ; kế toán có quyền Hạch toán mua dịch vụ thấy thêm nút Tạo mới.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Người dùng vào một trong các lối vào ở mục Layout (không cần quyền riêng để vào màn).',
       chinh='1. Người dùng vào một trong 2 lối vào ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem theo thứ tự V1 → V2 → V3; không có cấp nào thì lấy phiếu do chính người đó tạo.\n'
             '3. Hệ thống loại bỏ phiếu Đang tạo của người khác.\n'
             '4. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có) và cấu hình cột của người dùng.\n'
             '5. Hệ thống trả về trang 1, phiếu tạo gần nhất xếp trên, kèm tổng số phiếu; dòng “Hiển thị a–b / N” hiện đúng khoảng '
             'và tổng.\n'
             '6. Hệ thống hiện nút Tạo mới khi người dùng có quyền Hạch toán mua dịch vụ, và nút trên từng dòng theo cờ quyền máy chủ trả.',
       phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng dựng theo cấu hình đó.\n'
           '• Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”; lỗi thiếu quyền không hiện câu này.\n'
           '• Bấm số phiếu yêu cầu → mở màn chi tiết phiếu Yêu cầu hạch toán mua dịch vụ ở tab mới.\n'
           '• Bấm số hợp đồng → mở hợp đồng mua dịch vụ (Dịch vụ thuê ngoài) hoặc hợp đồng nguyên tắc bảo hiểm (Công nợ bảo hiểm) trên '
           'ERP ở tab mới.\n'
           '• Đổi tham số chế độ thành “index” → tiêu đề “Hạch toán mua dịch vụ của tôi”, chỉ phiếu mình tạo; giá trị lạ → coi như chế độ chung.\n'
           '• Bấm nhanh nhiều lần (đổi trang, đổi lọc) → chỉ hiển thị kết quả của lần bấm cuối.\n'
           '• Phiên đăng nhập hết hạn → báo hết phiên đăng nhập, điều hướng về màn đăng nhập.',
       dacbiet='Cột mặc định hiển thị (14): STT, Số phiếu, Loại yêu cầu, Phiếu yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán, '
               'Người tạo, Ngày tạo, Ngày hạch toán, Người cập nhật, Ngày cập nhật, Trạng thái, Hành động; không có cột ẩn mặc định. '
               'Cột bắt buộc (khóa, không ẩn / không đổi vị trí): STT, Số phiếu, Hành động; STT và Số phiếu ghim trái. Mặc định 10 '
               'dòng/trang.'),
   layout=dict(entries=[
       (MENU, 'Hiển thị: tiêu đề “Hạch toán mua dịch vụ”; phiếu trong phạm vi quyền (Phần 2). Đây là lối vào chính.'),
       (MENU_TC, 'Hiển thị: giống lối vào trên (cùng danh sách, cùng bộ lọc).')],
       shot=shot('01_list'), shot_caption='Màn danh sách Hạch toán mua dịch vụ'),
   extra=[('01b_row_draft', 'Dòng phiếu Đang tạo của chính người dùng — nút Sửa, Xóa, menu “…”'),
          ('01c_menu_row', 'Menu “…” (Hành động khác) của dòng: In phiếu, Lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Hạch toán mua dịch vụ”',
        ['- Là tiêu đề thanh trên cùng, tiêu đề bảng và tab trình duyệt', '- Chế độ “của tôi”: “Hạch toán mua dịch vụ của tôi”']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Theo quyền',
        ['- Chỉ hiện với quyền Hạch toán mua dịch vụ', '- Bấm → mở màn Tạo phiếu hạch toán mua dịch vụ (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.12)', '- Khóa trong lúc đang xuất']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ xem trước bản in danh sách theo bộ lọc (mục 2.11).'),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        ['- Biểu tượng cột, chữ gợi ý “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tùy chỉnh cột (mục 2.4)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Liên tục giữa các trang', '- Ghim trái; khóa trong Tùy chỉnh cột']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', '<mã công ty>.HTMDV.<năm><6 số>', 'Theo dữ liệu',
        ['- Bấm số phiếu → mở màn chi tiết (mục 2.9)', '- Sắp xếp được', '- Ghim trái; khóa trong Tùy chỉnh cột']),
       ('Cột Loại yêu cầu', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu',
        ['- Dịch vụ thuê ngoài / Công nợ bảo hiểm', '- Không sắp xếp']),
       ('Cột Phiếu yêu cầu', 'Table/Grid', 'Read-only', '<mã công ty>.YCHTMDV.<năm><6 số>', 'Theo dữ liệu',
        ['- Link mở màn chi tiết phiếu yêu cầu ở tab mới', '- Không sắp xếp']),
       ('Cột Số hợp đồng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Dịch vụ thuê ngoài: số hợp đồng mua dịch vụ; Công nợ bảo hiểm: số hợp đồng nguyên tắc bảo hiểm',
         '- Link mở hợp đồng trên ERP ở tab mới', '- Không sắp xếp']),
       ('Cột Nhà cung cấp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Dạng “Mã - Tên”', '- Tối đa 2 dòng, di chuột xem đủ']),
       ('Cột Tổng thanh toán', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
        ['- Dấu phẩy ngăn nghìn, tối đa 2 số lẻ, căn phải; bằng 0 thì để trống', '- Sắp xếp được']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Họ tên người tạo phiếu', '- Không sắp xếp']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Sắp xếp được; mặc định phiếu mới xếp trên']),
       ('Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Thời điểm Lưu và duyệt (ghi sổ); phiếu Đang tạo để trống', '- Sắp xếp được']),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Người lưu phiếu gần nhất', '- Không sắp xếp']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Thời điểm lưu gần nhất', '- Sắp xếp được']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu', STATUS_LIST + ['- Không sắp xếp']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo quyền và trạng thái',
        ['- Sửa: người tạo, phiếu Đang tạo → màn Sửa (mục 2.7)',
         '- Xóa (đỏ): cùng điều kiện → hộp Xác nhận xóa ngay trên danh sách (mục 2.8)',
         '- In phiếu, Lịch sử: luôn hiện',
         '- Dòng có hơn 3 nút: 2 nút đầu hiện thẳng, còn lại trong nút “…” (Hành động khác)', '- Khóa trong Tùy chỉnh cột']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- a–b: khoảng số thứ tự của trang đang xem', '- N: tổng phiếu khớp phạm vi và bộ lọc']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5, 10, 20, 50, 100', '- Đổi giá trị → về trang 1, nạp lại một lần']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Giữ bộ lọc, sắp xếp khi đổi trang']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp.” khi N = 0.'),
       ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- “Lỗi khi tải dữ liệu” khi máy chủ lỗi']),
   ],
   ev=[('Mở màn hình', 'System',
        'Before:\n– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3; không có cấp nào thì giới hạn ở phiếu do chính người dùng tạo.\n'
        '– Chế độ “index” → chỉ phiếu mình tạo; thiếu / lạ → chế độ chung.\n'
        'During:\n– Nạp cấu hình cột đã lưu, khôi phục bộ lọc của 10 phút gần nhất (nếu có), rồi nạp dữ liệu.\n'
        '– Loại bỏ phiếu Đang tạo của người khác; tính cờ Sửa / Xóa cho từng phiếu và cờ Tạo mới theo quyền Hạch toán mua dịch vụ.\n'
        'After:\n– Trả về trang 1, sắp xếp theo ngày tạo giảm dần, kèm tổng số phiếu.\n'
        '– Hiện / ẩn ô lọc Công ty, Phòng ban theo cấp quyền xem; hiện / ẩn nút Tạo mới.'),
       ('Bấm số phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem (đã lọc ở bước nạp danh sách).\nDuring:\n– Ghi nhớ bộ lọc hiện tại 10 phút.\n'
        'After:\n– Mở màn chi tiết của phiếu (mục 2.9).'),
       ('Bấm số phiếu yêu cầu / số hợp đồng', 'Click',
        'Before:\n– Dòng có giá trị.\nDuring:\n– Phiếu yêu cầu → màn HRM; số hợp đồng → màn hợp đồng ERP theo loại yêu cầu.\n'
        'After:\n– Mở ở tab mới, danh sách giữ nguyên.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ 5 cột Số phiếu, Tổng thanh toán, Ngày tạo, Ngày hạch toán, Ngày cập nhật sắp xếp được.\n'
        'During:\n– Đổi chiều tăng / giảm; giữ nguyên bộ lọc.\nAfter:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Bấm số trang hoặc nút tiến lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nDuring:\n– Nạp dữ liệu của trang được chọn.\n'
        'After:\n– Hiển thị trang mới, STT liên tục, dòng “Hiển thị a–b / N” cập nhật.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Chọn 1 trong 5, 10, 20, 50, 100.\nDuring:\n– Ghi nhận số dòng mới, chỉ gọi máy chủ một lần.\n'
        'After:\n– Quay về trang 1, nạp lại.'),
       ('Bấm nút “…” trên dòng', 'Click',
        'Before:\n– Dòng có hơn 3 nút (phiếu Đang tạo của mình).\nDuring:\n– Mở menu các nút còn lại (In phiếu, Lịch sử).\n'
        'After:\n– Bấm mục → thực hiện như nút tương ứng; bấm ra ngoài → đóng menu.')])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(ten='Tìm kiếm và lọc danh sách phiếu',
              mota='Thu hẹp danh sách theo ô tìm nhanh (số phiếu, phiếu yêu cầu, số hợp đồng) và 6 tiêu chí của khối Tìm kiếm nâng cao: '
                   'Công ty, Phòng ban, Nhà cung cấp, Tên dịch vụ, Loại yêu cầu, Trạng thái, Ngày tạo. Kết quả luôn nằm trong phạm vi '
                   'quyền xem của người dùng.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm hoặc Enter.\n'
                    '2. Hoặc bấm Tìm kiếm nâng cao để mở khối tiêu chí, nhập / chọn giá trị một hoặc nhiều tiêu chí.\n'
                    '3. Ô dạng chọn (Công ty, Phòng ban, Loại yêu cầu, Trạng thái, Ngày tạo) lọc ngay khi đổi giá trị.\n'
                    '4. Ô gõ tay (ô tìm nhanh, Nhà cung cấp, Tên dịch vụ) chỉ áp khi bấm Tìm kiếm / Enter.\n'
                    '5. Hệ thống quay về trang 1, nạp lại danh sách; bộ lọc được ghi nhớ 10 phút khi người dùng đi vào màn chi tiết / '
                    'sửa / tạo của màn này.',
              phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh và sắp xếp, nạp lại từ trang 1.\n'
                  '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
                  '• Đổi Công ty → xóa Phòng ban đang chọn, danh sách phòng ban chỉ còn của công ty mới.\n'
                  '• Ô tìm nhanh không tìm theo nhà cung cấp / tên dịch vụ — dùng 2 ô lọc riêng.\n'
                  '• Sang màn khác bằng menu, hoặc quá 10 phút → bộ lọc trở về trống.',
              dacbiet='Kiểu khớp: ô tìm nhanh khớp MỘT PHẦN (chuỗi chứa) với số phiếu, số phiếu yêu cầu, số hợp đồng (mua dịch vụ hoặc '
                      'bảo hiểm); Nhà cung cấp khớp một phần tên hoặc mã NCC; Tên dịch vụ khớp một phần tên dịch vụ của dòng chi tiết. '
                      'Không phân biệt hoa / thường; tự bỏ khoảng trắng đầu / cuối; không giới hạn số ký tự; ký tự % và _ được hiểu là '
                      'ký tự đại diện. Ô dạng chọn khớp CHÍNH XÁC. Ngày tạo lấy trọn 2 ngày biên. Lọc Công ty chỉ có hiệu lực với người '
                      'xem được mọi công ty (V1).'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách'),
   ui=[('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu, phiếu yêu cầu, số hợp đồng”', '- Khớp một phần', '- Chỉ áp khi bấm Tìm kiếm / Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp ô tìm nhanh và 2 ô gõ tay, về trang 1, nạp lại.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa toàn bộ tiêu chí kể cả ô tìm nhanh, nạp lại từ trang 1.'),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Mở / thu gọn khối tiêu chí', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống',
        ['- Chỉ hiện với quyền V1 (và Super admin)', '- Mặc định: trống (tất cả)', '- Đổi giá trị → xóa Phòng ban đang chọn']),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Hiện với quyền V1, V2, V3', '- Mặc định: trống (tất cả)', '- Chỉ liệt kê phòng ban của Công ty đang chọn']),
       ('Nhà cung cấp', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gõ tay, khớp một phần tên hoặc mã nhà cung cấp', '- Áp khi bấm Tìm kiếm / Enter']),
       ('Tên dịch vụ', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gõ tay, khớp một phần tên dịch vụ của dòng chi tiết', '- Áp khi bấm Tìm kiếm / Enter']),
       ('Loại yêu cầu', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)', '- Công nợ bảo hiểm', '- Dịch vụ thuê ngoài']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)', '- Đang tạo', '- Đã duyệt']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- 1 ô gồm 2 lịch Từ ngày → Đến ngày', '- Lấy trọn cả 2 ngày biên', '- Đã chọn thì ẩn biểu tượng lịch']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp.” khi không có kết quả.')],
   ev=[('Đổi giá trị ô dạng chọn', 'Change',
        'Before:\n– Áp cho Công ty, Phòng ban, Loại yêu cầu, Trạng thái, Ngày tạo.\n'
        'During:\n– Ghi nhận giá trị mới vào bộ lọc.\nAfter:\n– Quay về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí.'),
       ('Bấm nút Tìm kiếm hoặc Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, Nhà cung cấp, Tên dịch vụ đang nhập.\nDuring:\n– Gộp với các tiêu chí đang chọn.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Bấm nút Làm mới', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Đặt lại toàn bộ tiêu chí, ô tìm nhanh, sắp xếp về mặc định.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Đổi Công ty', 'Change',
        'Before:\n– Chỉ có với quyền V1.\nDuring:\n– Xóa Phòng ban đang chọn.\nAfter:\n– Nạp phòng ban của công ty mới, nạp lại danh sách.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối tiêu chí đang thu gọn.\nDuring:\n– Mở khối, nhãn đổi thành “Ẩn tìm kiếm nâng cao”.\n'
        'After:\n– Ghi nhớ trạng thái mở / thu gọn cùng bộ lọc.')])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn tiêu chí lọc muốn thấy ở khối Tìm kiếm nâng cao và sắp xếp lại thứ tự. Cấu hình '
                   'lưu riêng theo người dùng cho màn này; 6 tiêu chí là Công ty – Phòng ban, Nhà cung cấp, Tên dịch vụ, Loại yêu cầu, '
                   'Trạng thái, Ngày tạo.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 6 tiêu chí kèm ô tích theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích, kéo thả để đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối Tìm kiếm nâng cao.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 6 tiêu chí theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu.\n'
                  '• Bỏ tích một tiêu chí đang có giá trị lọc → giá trị đó bị xóa sau khi lưu.\n'
                  '• Lưu thất bại → “Thao tác thất bại”.',
              dacbiet='Cấu hình lưu theo tài khoản và theo màn hình; tài khoản khác không bị ảnh hưởng.'),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách tiêu chí', 'Table/Grid', 'Enable', 'Danh sách 6 tiêu chí', 'Không', 'Theo cấu hình đã lưu',
        ['- Công ty – Phòng ban', '- Nhà cung cấp', '- Tên dịch vụ', '- Loại yêu cầu', '- Trạng thái', '- Ngày tạo']),
       ('Ô tích của tiêu chí', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu',
        ['- Tích: tiêu chí hiện ở khối Tìm kiếm nâng cao', '- Bỏ tích: ẩn tiêu chí, xóa giá trị lọc của nó khi lưu']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự tiêu chí.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình, đóng cửa sổ, áp ngay.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích lại đủ 6 tiêu chí, thứ tự gốc; chưa lưu.'),
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
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Tích lại 6 tiêu chí, thứ tự gốc.\nAfter:\n– Chưa lưu; phải bấm Lưu.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ thay đổi chưa lưu.\nAfter:\n– Đóng cửa sổ, khối lọc giữ nguyên.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Tùy chỉnh cột của bảng danh sách',
              mota='Cho phép mỗi người dùng bật / tắt và kéo sắp xếp 14 cột của bảng danh sách phiếu. Cấu hình lưu theo người dùng; ba '
                   'cột STT, Số phiếu, Hành động bị khóa: luôn hiện, không đổi vị trí. Cấu hình cột đang hiện cũng là các trường được '
                   'tích sẵn khi Xuất Excel.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
                    '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 14 cột theo cấu hình đang áp dụng.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng ba gạch đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình, hiển thị “Cập nhật thành công”, vẽ lại bảng.',
              phu='• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, giữ cấu hình đang áp dụng.\n'
                  '• Cột khóa: ô tích xám, không bỏ tích, không kéo; di chuột hiện “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”.\n'
                  '• Lưu thất bại → “Thao tác thất bại”.\n'
                  '• Cấu hình lưu trên máy chủ theo tài khoản: giữ sau F5, đăng nhập trình duyệt / máy khác vẫn giữ.\n'
                  '• Đổi cột không làm thay đổi dữ liệu, tổng số phiếu, bộ lọc.',
              dacbiet='Mặc định hiện cả 14 cột. Dòng dưới cửa sổ ghi “Đang chọn n/14 cột”.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Tuỳ chỉnh cột”', 'Kèm nút (x) đóng.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', '14 cột', '–', 'Theo cấu hình',
        ['- STT, Số phiếu (khóa)', '- Loại yêu cầu, Phiếu yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán, Người tạo, Ngày tạo',
         '- Ngày hạch toán, Người cập nhật, Ngày cập nhật, Trạng thái', '- Hành động (khóa, luôn cuối)']),
       ('Ô tích của cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình', ['- Tích: cột hiện', '- Cột khóa: xám']),
       ('Biểu tượng ba gạch', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Kéo để đổi vị trí', '- Cột khóa hiện ổ khóa, không kéo']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi cột.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi cột (trừ cột khóa).'),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/14 cột”.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình, đóng cửa sổ, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”'])],
   ev=[('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Cấu hình đã nạp lúc mở màn.\nDuring:\n– Liệt kê 14 cột theo cấu hình đang áp dụng.\nAfter:\n– Mở cửa sổ “Tuỳ chỉnh cột”.'),
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
fr(5, 'Lập phiếu hạch toán mua dịch vụ', usecase=('FR-05', 'Lập phiếu', 'crud', A_KT),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu hạch toán mua dịch vụ',
       mota='Kế toán lập phiếu hạch toán từ một phiếu Yêu cầu hạch toán mua dịch vụ đang Chờ duyệt. Hệ thống nạp loại yêu cầu, hợp '
            'đồng, nhà cung cấp, VAT, dịch vụ, đơn giá, SL yêu cầu và file của phiếu yêu cầu; kế toán chọn tài khoản nợ / có, sửa đơn '
            'giá, SL hạch toán, mã phí, mã vụ việc rồi Lưu nháp hoặc Lưu và duyệt (ghi sổ, mục 2.10).',
       tacnhan=TN_KT, dieukien=DK_TAO,
       chinh='1. Kế toán bấm Tạo mới ở danh sách (hoặc nút Hạch toán ở màn Yêu cầu hạch toán mua dịch vụ); hệ thống mở màn “Tạo phiếu '
             'hạch toán mua dịch vụ”, Tài khoản có mặc định 3311.\n'
             '2. Kế toán bấm ô Phiếu yêu cầu, chọn phiếu (mục 2.6) — vào từ nút Hạch toán thì phiếu đã chọn sẵn.\n'
             '3. Hệ thống điền Loại yêu cầu, Hợp đồng, Nhà cung cấp, Hóa đơn VAT, VAT %, bảng dịch vụ (SL hạch toán = SL yêu cầu) và '
             'file của phiếu yêu cầu; loại Công nợ bảo hiểm điền thông tin bảo hiểm, TK nợ 1541 / TK có 3311 cố định.\n'
             '4. Kế toán chọn Tài khoản nợ, Tài khoản có, Nhà cung cấp; sửa Đơn giá, SL hạch toán, chọn Mã phí / Mã vụ việc (dòng đầu áp '
             'cho mọi dòng); nhập Diễn giải; thêm / gỡ file.\n'
             '5. Kế toán bấm Lưu nháp, Lưu và tiếp tục hoặc Lưu và duyệt.\n'
             '6. Hệ thống kiểm tra dữ liệu theo nút được bấm (BR-02, BR-03), khóa phiếu yêu cầu, lấy lại dịch vụ / SL tối đa từ phiếu yêu '
             'cầu, sinh số phiếu, tính tổng tiền, lưu phiếu.\n'
             '7. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu; phiếu yêu cầu chuyển Đang hạch toán (Lưu nháp) và ghi '
             'lịch sử bên phiếu yêu cầu.\n'
             '8. Hệ thống hiển thị “Thêm mới thành công.” và quay về màn danh sách (Lưu và duyệt: xem mục 2.10).',
       phu='• Lưu nháp khi chưa chọn Phiếu yêu cầu → “Phiếu yêu cầu – Bắt buộc phải nhập”, không gửi máy chủ.\n'
           '• Lưu và duyệt thiếu / sai dữ liệu → báo đỏ dưới từng ô, hiển thị ' + TOAST_422 + ', cuộn tới ô lỗi đầu, không mở hộp '
           'xác nhận.\n'
           '• SL hạch toán vượt SL yêu cầu → báo đỏ đúng ô, không tự kéo về trần (áp cả khi lưu nháp).\n'
           '• Phiếu yêu cầu vừa bị người khác lập phiếu / Không duyệt / khác công ty → ' + M_SRC + '\n'
           '• Lưu và tiếp tục → lưu nháp rồi mở lại form trống, ở lại màn Tạo.\n'
           '• Màn Tạo là trang riêng, không phải cửa sổ nổi: không có nút (x), không đóng bằng click ra ngoài; rời màn bằng Quay '
           'lại / menu → hộp “Thông tin chưa lưu”; F5 / đóng tab → hộp cảnh báo rời trang của trình duyệt.\n'
           '• Bấm nút lưu liên tục → nút khóa trong lúc đang lưu, chỉ tạo 1 phiếu.\n'
           '• Không có quyền Hạch toán mua dịch vụ → không thấy nút Tạo mới; gọi thẳng → ' + M_NOPERM + '.\n'
           '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
       dacbiet='Quy tắc trùng dữ liệu: phiếu không có trường nhập duy nhất, số phiếu tự sinh; mỗi phiếu yêu cầu chỉ lập được 1 phiếu hạch '
               'toán (sau khi lưu, phiếu yêu cầu rời Chờ duyệt nên không chọn lại được; 2 kế toán lưu cùng lúc thì người sau bị chặn). '
               'Máy chủ chỉ tin id dòng của phiếu yêu cầu, Đơn giá, SL, Mã phí, Mã vụ việc; dịch vụ và tổng tiền tự lấy / tự tính. Khóa '
               'các nút lưu trong lúc đang xử lý.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10e_filled'),
               shot_caption='Màn Tạo phiếu — đã chọn phiếu yêu cầu loại Dịch vụ thuê ngoài'),
   extra=[('10_create', 'Màn Tạo phiếu khi mới mở (chưa chọn phiếu yêu cầu, Tài khoản có mặc định 3311)'),
          ('10b_validate', 'Bấm Lưu và duyệt khi chưa nhập — lỗi dưới từng ô'),
          ('10f_filled_table', 'Bảng Chi tiết dịch vụ: Đơn giá, SL yêu cầu, SL hạch toán, Mã phí, Mã vụ việc'),
          ('21_from_request', 'Vào từ nút Hạch toán ở màn Yêu cầu — phiếu yêu cầu chọn sẵn'),
          ('10g_unsaved', 'Hộp Thông tin chưa lưu khi rời màn')],
   ui=form_ui(False), ev=save_ev(False))

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn phiếu yêu cầu hạch toán', usecase=('FR-06', 'Chọn phiếu yêu cầu', 'crud', A_KT),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(ten='Chọn phiếu yêu cầu hạch toán mua dịch vụ',
              mota='Cửa sổ “Chọn phiếu yêu cầu hạch toán mua dịch vụ” ở màn Tạo liệt kê phiếu yêu cầu Chờ duyệt do chính người dùng tạo. '
                   'Bấm một dòng là chọn; hệ thống nạp toàn bộ dữ liệu của phiếu yêu cầu vào form. Phiếu yêu cầu của người khác lập phiếu '
                   'qua nút Hạch toán ở màn Yêu cầu.',
              tacnhan=TN_KT,
              dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Hạch toán mua dịch vụ, đang ở màn Tạo phiếu.\n'
                       '3. Có phiếu yêu cầu Chờ duyệt do chính người dùng tạo.',
              chinh='1. Người dùng bấm ô Phiếu yêu cầu.\n'
                    '2. Hệ thống mở cửa sổ, nạp trang 1 phiếu Chờ duyệt do người dùng tạo (mới tạo xếp trên).\n'
                    '3. Người dùng nhập Mã phiếu, bấm Tìm kiếm hoặc Enter.\n4. Người dùng bấm vào một dòng.\n'
                    '5. Hệ thống kiểm tra phiếu yêu cầu còn Chờ duyệt, cùng công ty, người dùng có quyền; đóng cửa sổ, nạp loại, hợp đồng, '
                    'NCC, VAT, dịch vụ, SL, file (kèm dung lượng); thay file kế thừa của phiếu chọn trước, giữ file tự tải lên.',
              phu='• Không có dữ liệu → “Không có phiếu yêu cầu hạch toán Chờ duyệt nào do bạn tạo.”.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không chọn, ô giữ nguyên.\n'
                  '• Bấm mã phiếu (link) → mở màn chi tiết phiếu yêu cầu ở tab mới, KHÔNG chọn dòng.\n'
                  '• Phiếu yêu cầu không còn Chờ duyệt / khác công ty → ' + M_SRC + '\n'
                  '• Lỗi tải danh sách → “Lỗi khi tải dữ liệu”; lỗi nạp phiếu → “Lỗi khi tải phiếu yêu cầu”.',
              dacbiet='Chỉ phiếu yêu cầu Chờ duyệt do chính người đăng nhập tạo (đúng ERP). Cửa sổ cỡ vừa, 3 cột. SL hạch toán mặc định '
                      'bằng SL yêu cầu; Tài khoản có mặc định 3311.'),
   layout=dict(menu=MENU + ' => Tạo mới => Phiếu yêu cầu', shot=shot('11_request_picker'),
               shot_caption='Cửa sổ Chọn phiếu yêu cầu hạch toán mua dịch vụ',
               note='Cửa sổ chọn được mở ngay trên màn hình Tạo phiếu theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn phiếu yêu cầu hạch toán mua dịch vụ”', ['- Có nút (x) đóng']),
       ('Ô Mã phiếu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Khớp một phần mã phiếu yêu cầu', '- Có nút × xóa nhanh; Enter = Tìm kiếm']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp điều kiện tìm, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa điều kiện tìm và sắp xếp, nạp lại từ trang 1.'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', 'Số thứ tự liên tục.'),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Sắp xếp được', '- Link mở màn chi tiết phiếu yêu cầu ở tab mới (không chọn dòng)']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Theo dữ liệu', ['- Sắp xếp được', '- Mặc định mới tạo trên']),
       ('Dòng phiếu', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu',
        ['- Bấm dòng → chọn, đóng cửa sổ, nạp dữ liệu', '- Rỗng: “Không có phiếu yêu cầu hạch toán Chờ duyệt nào do bạn tạo.”']),
       ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1',
        ['- Dòng “Hiển thị a–b / N”, Số dòng/trang 10, 20, 50, 100', '- Mặc định 10 dòng/trang']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không chọn.'),
       ('Nút × ở ô Phiếu yêu cầu', 'Icon Button', 'Enable', '–', '–', 'Ẩn khi trống',
        ['- Bỏ chọn phiếu yêu cầu', '- Xóa dữ liệu đã nạp và file kế thừa; giữ file tự tải lên, Diễn giải']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Lỗi khi tải dữ liệu”', '- “Lỗi khi tải phiếu yêu cầu”', '- ' + M_SRC])],
   ev=[('Bấm ô Phiếu yêu cầu', 'Click',
        'Before:\n– Chỉ ở màn Tạo; màn Sửa / chi tiết là link chỉ đọc.\n– Kiểm tra quyền Hạch toán mua dịch vụ; không có → máy chủ từ '
        'chối ' + M_NOPERM + '.\nDuring:\n– Xóa điều kiện tìm cũ, nạp trang 1.\nAfter:\n– Mở cửa sổ chọn phiếu yêu cầu.'),
       ('Bấm Tìm kiếm, Enter hoặc tiêu đề cột', 'Click',
        'Before:\n– Lấy điều kiện ở ô Mã phiếu.\nDuring:\n– Tìm theo chuỗi chứa; sắp xếp theo cột bấm.\nAfter:\n– Về trang 1, hiện kết quả.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Xóa điều kiện tìm, sắp xếp.\nAfter:\n– Nạp lại từ trang 1.'),
       ('Bấm một dòng phiếu', 'Click',
        'Before:\n– Kiểm tra phiếu còn Chờ duyệt, cùng công ty, người dùng có quyền Hạch toán mua dịch vụ.\n'
        'During:\n– Sai điều kiện → hiển thị ' + M_SRC + '\n' + ERR + '\n'
        'After:\n– Đóng cửa sổ; điền Phiếu yêu cầu, Loại yêu cầu, Hợp đồng / thông tin bảo hiểm, NCC, Hóa đơn VAT, VAT %, bảng dịch vụ '
        '(SL hạch toán = SL yêu cầu), file kế thừa (kèm dung lượng).\n– Xóa lỗi đang hiện; tính là có thay đổi chưa lưu.'),
       ('Bấm link mã phiếu', 'Click',
        'Before:\n– Mã phiếu là link.\nDuring:\n– Không chọn dòng.\nAfter:\n– Mở màn chi tiết phiếu yêu cầu ở tab mới.'),
       ('Bấm × ở ô Phiếu yêu cầu', 'Click',
        'Before:\n– Đã chọn phiếu.\nDuring:\n– Gỡ dữ liệu đã nạp và file kế thừa.\nAfter:\n– Form trở về như chưa chọn phiếu (giữ Diễn '
        'giải, file tự tải lên).'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không ghi gì vào form.\nAfter:\n– Đóng cửa sổ, ô giữ nguyên.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Chỉnh sửa phiếu', usecase=('FR-07', 'Chỉnh sửa phiếu', 'crud', A_KT),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(ten='Chỉnh sửa phiếu hạch toán mua dịch vụ',
              mota='Người tạo sửa phiếu đang ở trạng thái Đang tạo (chưa ghi sổ). Màn Sửa dùng chung bố cục và quy tắc kiểm tra với màn Tạo '
                   '(mục 2.5), riêng Phiếu yêu cầu bị khóa (không đổi được phiếu nguồn); lưu nháp lại hoặc Lưu và duyệt để ghi sổ.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
                    '2. Hệ thống mở màn “Sửa phiếu hạch toán mua dịch vụ: <số phiếu>” với dữ liệu phiếu.\n'
                    '3. Người dùng sửa các trường (quy tắc như mục 2.5), thêm / xóa file.\n'
                    '4. Người dùng bấm Lưu nháp hoặc Lưu và duyệt.\n'
                    '5. Hệ thống kiểm tra quyền, trạng thái, người tạo, dữ liệu (BR-02, BR-03), lưu phiếu.\n'
                    '6. Hệ thống ghi nhận hành động “Thay đổi thông tin” trong lịch sử của phiếu (chỉ trường đã đổi, cũ → mới); Lưu và '
                    'duyệt thì ghi thêm “Thay đổi trạng thái” Đang tạo → Đã duyệt.\n'
                    '7. Hệ thống hiển thị “Cập nhật thành công.” (hoặc “Duyệt thành công.”), quay về màn danh sách.',
              phu='• Phiếu không sửa được (không phải người tạo / đã duyệt) → tự chuyển sang màn chi tiết.\n'
                  '• Phiếu không tồn tại hoặc ngoài phạm vi → chuyển sang trang “không tìm thấy”.\n'
                  '• Phiếu vừa được duyệt ở tab khác → ' + M_CONFLICT + ', không lưu.\n'
                  '• Rời màn khi chưa lưu → hộp “Thông tin chưa lưu”; không đổi gì (hoặc đổi rồi trả về giá trị ban đầu) → về danh '
                  'sách ngay.\n'
                  '• Phiếu đã bị xóa trong lúc đang sửa → bấm lưu báo lỗi chung của máy chủ (không tìm thấy bản ghi), không lưu.\n'
                  '• Hai tab cùng sửa nháp: lần lưu sau ghi đè lần trước.',
              dacbiet='Trường được sửa: Hóa đơn VAT, VAT (%), Nhà cung cấp, Tài khoản nợ, Tài khoản có, Diễn giải, Đơn giá, SL hạch toán, '
                      'Mã phí, Mã vụ việc, file. Không sửa được: Phiếu yêu cầu, Loại yêu cầu, Hợp đồng / đơn bảo hiểm, Số phiếu, người tạo, '
                      'ngày tạo, công ty / phòng ban. Lịch sử ghi giá trị cũ → mới; không đổi gì thì không ghi. Phiếu Đã duyệt coi như khóa '
                      'sửa. Xóa file đã lưu có hiệu lực ngay.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('19_edit'), shot_caption='Màn Sửa phiếu hạch toán mua dịch vụ'),
   ui=form_ui(True), ev=save_ev(True))

# ------------------------------------------------------------ 2.8
fr(8, 'Xóa phiếu', usecase=('FR-08', 'Xóa phiếu', 'action', A_KT),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(ten='Xóa phiếu hạch toán mua dịch vụ',
              mota='Người tạo xóa hẳn phiếu đang ở trạng thái Đang tạo cùng toàn bộ dòng dịch vụ và dòng yêu cầu. Xóa được ngay ở cột Hành '
                   'động của danh sách hoặc ở chân màn chi tiết, qua hộp xác nhận. Xóa trả phiếu yêu cầu nguồn về Chờ duyệt để lập lại.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở chân màn chi tiết.\n'
                    '2. Hệ thống hiển thị hộp “Xác nhận xóa”.\n3. Người dùng bấm Xóa.\n'
                    '4. Hệ thống kiểm tra quyền, trạng thái, người tạo.\n'
                    '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử của phiếu (kèm dòng dịch vụ, file), rồi xóa dòng yêu cầu, dòng '
                    'dịch vụ và phiếu.\n'
                    '6. Phiếu yêu cầu nguồn đang Đang hạch toán chuyển về Chờ duyệt; ghi lịch sử bên phiếu yêu cầu.\n'
                    '7. Hệ thống hiển thị “Xóa thành công.”: ở danh sách nạp lại bảng; ở màn chi tiết quay về danh sách.',
              phu='• Bấm Hủy / (x) / click ra ngoài hộp → không xóa.\n'
                  '• Phiếu đã đổi trạng thái → ' + M_CONFLICT + '; không phải người tạo → “Bạn không có quyền xóa phiếu này”.\n'
                  '• Thiếu quyền Hạch toán mua dịch vụ → ' + M_NOPERM + '.\n'
                  '• Lỗi khác → “Xóa không thành công”.\n'
                  '• Phiếu đã bị xóa ở tab khác → lỗi chung của máy chủ (không tìm thấy bản ghi).',
              dacbiet='Ràng buộc dữ liệu cấp con: dòng dịch vụ / dòng yêu cầu là của chính phiếu nên bị xóa theo, không chặn. Ràng buộc '
                      'đang sử dụng: phiếu Đã duyệt đã ghi sổ nên không xóa được (nút ẩn, máy chủ chặn). Phiếu yêu cầu, hợp đồng, file '
                      'của phiếu yêu cầu không bị xóa. Khóa nút Xóa trong lúc đang xử lý.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp xác nhận xóa phiếu trên danh sách',
               note='Modal Xác nhận xóa được mở ngay trên màn hình danh sách (hoặc màn chi tiết) theo đường dẫn ở trên.'),
   extra=[('13b_delete_detail', 'Hộp xác nhận xóa ở màn chi tiết phiếu')],
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Xóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Ẩn',
        ['- Cột Hành động, biểu tượng thùng rác đỏ', '- Người tạo, phiếu Đang tạo', '- Bấm → hộp Xác nhận xóa ngay trên danh sách']),
       ('Nút Xóa ở chân màn chi tiết', 'Button', 'Enable / Ẩn', 'Ẩn', ['- Màu đỏ, cùng điều kiện', '- Bấm → hộp Xác nhận xóa']),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', '“Xác nhận xóa”', 'Kèm nút (x) đóng.'),
       ('Nội dung', 'Label', 'Hiển thị', '–', DEL_MSG),
       ('Nút Xóa', 'Button', 'Enable / Disable', 'Hiển thị', ['- Xác nhận xóa phiếu', '- Khóa trong lúc đang xóa']),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Xóa thành công.”', '- Sai trạng thái: ' + M_CONFLICT, '- Không phải người tạo: “Bạn không có quyền xóa phiếu này”',
         '- Lỗi khác: “Xóa không thành công”'])],
   ev=[('Bấm Xóa ở cột Hành động hoặc chân màn chi tiết', 'Click',
        'Before:\n– Nút chỉ hiện với người tạo, phiếu Đang tạo.\nDuring:\n– Ghi nhận phiếu cần xóa.\n'
        'After:\n– Hiển thị hộp “Xác nhận xóa” nội dung ' + DEL_MSG + '.'),
       ('Bấm Xóa trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra quyền Hạch toán mua dịch vụ; không có → hiển thị ' + M_NOPERM + ' và dừng xử lý.\n'
        '– Kiểm tra phiếu Đang tạo; sai → hiển thị ' + M_CONFLICT + ' và dừng xử lý.\n'
        '– Kiểm tra người đăng nhập là người tạo; sai → hiển thị “Bạn không có quyền xóa phiếu này” và dừng xử lý.\n'
        'During:\n– Khóa phiếu, kiểm lại trạng thái; phiếu không còn tồn tại → báo lỗi, không xóa.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa” (kèm dòng dịch vụ, file).\n'
        '– Xóa dòng yêu cầu, dòng dịch vụ, phiếu; phiếu yêu cầu về Chờ duyệt.\n'
        '– Hiển thị “Xóa thành công.”; danh sách nạp lại / màn chi tiết quay về danh sách.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài hộp', 'Click',
        'Before:\n– Hộp đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng hộp, phiếu giữ nguyên.')])

# ------------------------------------------------------------ 2.9
fr(9, 'Xem chi tiết phiếu', usecase=('FR-09', 'Xem chi tiết phiếu', 'view', A_XEM),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Xem chi tiết phiếu hạch toán mua dịch vụ',
              mota='Xem toàn bộ thông tin một phiếu ở chế độ chỉ đọc, dùng lại bố cục form Tạo / Sửa theo loại yêu cầu, kèm khối Hạch toán '
                   '(bút toán Nợ / Có) khi phiếu Đã duyệt và khối Lịch sử. Chân màn hiện các nút thao tác theo vai trò và trạng thái, '
                   'cùng điều kiện với cột Hành động ở danh sách.',
              tacnhan=TN_XEM,
              dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem của người dùng (Phần 2).\n'
                       '3. Phiếu Đang tạo chỉ người tạo xem được.',
              chinh='1. Người dùng bấm số phiếu ở danh sách.\n2. Hệ thống kiểm tra phạm vi xem.\n'
                    '3. Hệ thống mở màn “Chi tiết hạch toán mua dịch vụ: <số phiếu>”, hiện thông tin theo loại.\n'
                    '4. Phiếu Đã duyệt: hiện khối Hạch toán với các bút toán đã ghi sổ và dòng Tổng cộng.\n'
                    '5. Hệ thống hiện nút ở chân màn theo vai trò và trạng thái; khối Lịch sử thu gọn.',
              phu='• Ngoài phạm vi / không tồn tại → chuyển sang trang “không tìm thấy”.\n'
                  '• Lỗi khác → “Lỗi khi tải phiếu”.\n'
                  '• Bấm số phiếu yêu cầu → mở màn chi tiết phiếu yêu cầu ở tab mới; bấm số hợp đồng / đơn bảo hiểm → mở trên ERP ở tab '
                  'mới; bấm số yêu cầu mua dịch vụ → mở màn chi tiết yêu cầu mua dịch vụ ở tab mới.\n'
                  '• Phiếu Đã duyệt: chân màn chỉ còn In phiếu, Quay lại.\n'
                  '• Bấm Quay lại → về danh sách; bộ lọc được giữ nếu quay lại trong 10 phút.',
              dacbiet='Màn chi tiết là trang riêng, mọi ô chỉ đọc, không có nút lưu; bảng dịch vụ bỏ cột SL yêu cầu; không có file thì '
                      'hiện “Không có file đính kèm.”. Số tiền ở khối Hạch toán lấy số gốc (giữ số lẻ) để khớp Tổng thanh toán.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn chi tiết phiếu Đã duyệt'),
   extra=[('17b_detail_entries', 'Khối Hạch toán (bút toán Nợ / Có) và khối Lịch sử ở cuối màn chi tiết')],
   ui_kw=dict(required=False),
   ui=[('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Chi tiết hạch toán mua dịch vụ: <số phiếu>”.'),
       ('Khối Thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Người tạo – ngày giờ tạo ở góc phải', '- Phiếu yêu cầu (link), Loại yêu cầu, Hợp đồng mua dịch vụ (link ERP)',
         '- Hóa đơn VAT, Nhà cung cấp, Tài khoản nợ, Tài khoản có, Diễn giải',
         '- Công nợ bảo hiểm: Số đơn bảo hiểm, Phụ lục bổ sung, Số hợp đồng mua (link ERP)']),
       ('Khối thông tin bảo hiểm', 'Label', 'Read-only / Ẩn', '–', 'Theo dữ liệu',
        ['- Chỉ loại Công nợ bảo hiểm', '- Thông tin công ty bảo hiểm, người liên hệ, người đại diện']),
       ('Bảng File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, Upload / File, Dung lượng', '- Bấm tên file → xem trước', '- Rỗng: “Không có file đính kèm.”']),
       ('Bảng Chi tiết dịch vụ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, Tên dịch vụ, ĐVT, Số lượng, Đơn giá, Thành tiền, Yêu cầu, SL hạch toán, Mã phí, Mã vụ việc',
         '- Dòng Thành tiền, VAT (x%), Tổng thanh toán', '- Rỗng: “Không có dữ liệu.”']),
       ('Bảng Thông tin chi tiết (bảo hiểm)', 'Table/Grid', 'Read-only / Ẩn', '–', 'Theo dữ liệu',
        ['- Chỉ loại Công nợ bảo hiểm', '- Phí bảo hiểm, Tổng thanh toán, Mã phí, Vụ việc; Tổng trước thuế, VAT, Tổng sau thuế']),
       ('Khối Hạch toán', 'Table/Grid', 'Read-only / Ẩn', '–', 'Theo dữ liệu',
        ['- Chỉ phiếu Đã duyệt', '- Cột STT, Tên tài khoản, Số tài khoản, Nợ, Có, Mã đối tượng, Tên đối tượng, Mã vụ việc, Tên vụ việc',
         '- Dòng Tổng cộng (tổng Nợ, tổng Có)', '- Rỗng: “Chưa có bút toán hạch toán.”']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        ['- Nút “Xem lịch sử” / “Thu gọn”, kèm số mốc', '- Nội dung như mục 2.13']),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Người tạo, phiếu Đang tạo', '- Bấm → màn Sửa (mục 2.7)']),
       ('Nút In phiếu', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ xem trước bản in (mục 2.11).'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Màu đỏ; người tạo, phiếu Đang tạo', '- Bấm → mục 2.8']),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- “Lỗi khi tải phiếu”: lỗi khác'])],
   ev=[('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phiếu tồn tại, nằm trong phạm vi xem; phiếu Đang tạo chỉ người tạo xem.\n'
        '– Sai → chuyển sang trang “không tìm thấy”, không hiện thông báo lỗi.\n'
        'During:\n– Nạp dữ liệu phiếu, bút toán (phiếu Đã duyệt) và cờ Sửa / Xóa; dựng bố cục theo loại yêu cầu.\n'
        'After:\n– Hiển thị thông tin chỉ đọc, khối Hạch toán, khối Lịch sử thu gọn; nút chân màn theo vai trò và trạng thái.'),
       ('Bấm link chứng từ', 'Click',
        'Before:\n– Ô có giá trị.\nDuring:\n– Xác định màn đích (màn HRM hoặc ERP).\nAfter:\n– Mở ở tab mới.'),
       ('Bấm tên file đính kèm', 'Click', 'Before:\n– File đã lưu.\nDuring:\n– Lấy đường dẫn file.\nAfter:\n– Mở cửa sổ xem trước file.'),
       ('Bấm Xem lịch sử', 'Click',
        'Before:\n– Khối Lịch sử đang thu gọn.\nDuring:\n– Nạp các mốc lịch sử.\nAfter:\n– Mở khối, nhãn đổi thành “Thu gọn” (mục 2.13).'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Màn chỉ đọc, không hỏi xác nhận.\nDuring:\n– Chuyển màn.\nAfter:\n– Về màn danh sách.')])

# ------------------------------------------------------------ 2.10
fr(10, 'Lưu và duyệt (ghi sổ)', usecase=('FR-10', 'Lưu và duyệt', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Lưu và duyệt phiếu hạch toán mua dịch vụ',
              mota='Thao tác duyệt duy nhất của màn: kế toán bấm Lưu và duyệt ở màn Tạo / Sửa, xác nhận, hệ thống lưu phiếu ở trạng thái '
                   'Đã duyệt, ghi bút toán vào sổ kế toán và cập nhật phiếu yêu cầu, hợp đồng mua dịch vụ hoặc đơn bảo hiểm. Màn không có '
                   'Không duyệt; trả phiếu về được thực hiện ở màn Yêu cầu (trước khi lập phiếu hạch toán).',
              tacnhan=TN_KT,
              dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Hạch toán mua dịch vụ.\n'
                       '3. Đang ở màn Tạo, hoặc màn Sửa của phiếu Đang tạo do chính mình tạo; phiếu yêu cầu nguồn Chờ duyệt / Đang hạch toán.',
              chinh='1. Kế toán nhập đủ thông tin, bấm Lưu và duyệt.\n'
                    '2. Hệ thống kiểm tra trên màn hình; hết lỗi thì hiển thị hộp “Xác nhận duyệt”.\n3. Kế toán bấm Duyệt.\n'
                    '4. Hệ thống kiểm tra lại toàn bộ ở máy chủ, lưu phiếu trạng thái Đã duyệt, Ngày hạch toán = thời điểm duyệt.\n'
                    '5. Hệ thống ghi sổ: Dịch vụ thuê ngoài — Nợ TK nợ theo thành tiền từng dòng, Nợ 1331 tiền VAT, Có TK có tổng sau VAT '
                    '(đối tượng nhà cung cấp); Công nợ bảo hiểm — Nợ 1541 / Có 3311 bằng Tổng sau thuế, kèm Mã phí, Vụ việc.\n'
                    '6. Hệ thống cộng SL hạch toán vào SL đã hạch toán của hợp đồng mua dịch vụ (Dịch vụ thuê ngoài) hoặc chuyển đơn / phụ '
                    'lục bảo hiểm sang Đã hạch toán (Công nợ bảo hiểm).\n'
                    '7. Phiếu yêu cầu chuyển Đã hạch toán, ghi Người duyệt / Ngày duyệt; ghi lịch sử bên phiếu yêu cầu kèm “Từ phiếu hạch '
                    'toán mua dịch vụ”.\n'
                    '8. Hệ thống ghi nhận “Tạo mới” (màn Tạo) hoặc “Thay đổi thông tin” + “Thay đổi trạng thái” (màn Sửa) trong lịch sử '
                    'của phiếu.\n9. Hệ thống hiển thị “Duyệt thành công.” và quay về danh sách.',
              phu='• Còn lỗi → báo đỏ dưới ô, không mở hộp xác nhận.\n'
                  '• Bấm Hủy / (x) / click ra ngoài hộp → không lưu, form giữ nguyên.\n'
                  '• Phiếu yêu cầu đã bị xử lý (Không duyệt / lập phiếu khác) → ' + M_SRC + '\n'
                  '• Phiếu (màn Sửa) vừa được duyệt ở tab khác → ' + M_CONFLICT + '.\n'
                  '• Ghi sổ thất bại → “Tài khoản nợ – <lý do>”, không lưu gì (toàn bộ hủy).\n'
                  '• Không gửi thông báo cho người tạo phiếu yêu cầu.',
              dacbiet='Không quay lại được: phiếu Đã duyệt không sửa, không xóa. Bút toán Dịch vụ thuê ngoài không mang Mã phí / Mã vụ việc '
                      'của dòng (giữ như ERP). Mọi bước trong một giao dịch, khóa phiếu yêu cầu để chặn 2 kế toán duyệt cùng lúc.'),
   layout=dict(menu=MENU + ' => Tạo mới => Lưu và duyệt', shot=shot('14_approve_confirm'), shot_caption='Hộp Xác nhận duyệt',
               note='Modal Xác nhận duyệt được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Lưu và duyệt', 'Button', 'Enable / Disable', 'Hiển thị',
        ['- Chân màn Tạo / Sửa, màu chính', '- Khóa trong lúc đang lưu hoặc khi màn Sửa chưa nạp xong phiếu']),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', '“Xác nhận duyệt”', 'Kèm nút (x) đóng.'),
       ('Nội dung', 'Label', 'Hiển thị', '–', APPROVE_MSG),
       ('Nút Duyệt', 'Button', 'Enable', 'Hiển thị', 'Lưu phiếu Đã duyệt và ghi sổ.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không lưu.'),
       ('Ngày hạch toán', 'Label', 'Read-only', 'Trống', ['- Ghi = thời điểm duyệt', '- Hiện ở cột Ngày hạch toán của danh sách']),
       ('Khối Hạch toán (sau duyệt)', 'Table/Grid', 'Read-only', 'Ẩn', 'Bút toán vừa ghi, xem ở màn chi tiết (mục 2.9).'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Duyệt thành công.”', '- Thiếu dữ liệu: ' + TOAST_422, '- ' + M_SRC, '- “Tài khoản nợ – <lý do>” khi ghi sổ lỗi',
         '- Lỗi khác: “Lỗi khi lưu phiếu”'])],
   ev=[('Bấm Lưu và duyệt', 'Click',
        'Before:\n– Kiểm tra trên màn hình như mục 2.5 / 2.7; còn lỗi → báo đỏ, dừng.\nDuring:\n– Ghi nhận dữ liệu cần lưu.\n'
        'After:\n– Hiển thị hộp “Xác nhận duyệt” nội dung ' + APPROVE_MSG + '.'),
       ('Bấm Duyệt', 'Click',
        'Before:\n– Kiểm tra quyền Hạch toán mua dịch vụ; không có → hiển thị ' + M_NOPERM + ' và dừng xử lý.\n'
        '– Màn Sửa: kiểm tra phiếu Đang tạo (sai → ' + M_CONFLICT + ') và người tạo (sai → “Bạn không có quyền sửa phiếu này”).\n'
        '– Khóa phiếu yêu cầu; không còn Chờ duyệt / Đang hạch toán hợp lệ → ' + M_SRC + '\n'
        'During:\n– Kiểm tra đủ trường bắt buộc, SL ≤ SL yêu cầu, Tổng thanh toán > 0, Mã phí / Mã vụ việc theo nhánh tài khoản.\n'
        '– Ghi sổ lỗi → “Tài khoản nợ – <lý do>”.\n' + ERR + '\n'
        'After:\n– Lưu phiếu Đã duyệt, Ngày hạch toán; ghi bút toán; cộng SL đã hạch toán vào hợp đồng / đơn bảo hiểm sang Đã hạch toán.\n'
        '– Phiếu yêu cầu chuyển Đã hạch toán, ghi Người duyệt, Ngày duyệt và lịch sử bên phiếu yêu cầu.\n'
        '– Ghi lịch sử phiếu (“Tạo mới” hoặc “Thay đổi thông tin” + “Thay đổi trạng thái”).\n'
        '– Hiển thị “Duyệt thành công.”, quay về danh sách (Back không quay lại form).'),
       ('Bấm Hủy, (x) hoặc click ra ngoài hộp', 'Click',
        'Before:\n– Hộp đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng hộp, form giữ nguyên dữ liệu.')])

# ------------------------------------------------------------ 2.11
fr(11, 'In phiếu và in danh sách', usecase=('FR-11', 'In phiếu', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(ten='In phiếu / In danh sách hạch toán mua dịch vụ',
              mota='Xem trước bản in ngay trên màn hình (không mở tab mới) rồi in. In phiếu dựng theo mẫu in “Phiếu hạch toán mua dịch vụ” '
                   'của hệ thống, đầu trang là letterhead công ty ghi trên phiếu. In danh sách dựng theo mẫu “Danh sách hạch toán mua dịch '
                   'vụ” với toàn bộ phiếu khớp bộ lọc (tối đa 2.000 dòng).',
              tacnhan=TN_XEM, dieukien=DK_XEM.replace('3. Người dùng đang ở màn danh sách Hạch toán mua dịch vụ.',
                                                       '3. Người dùng đang ở màn danh sách hoặc màn chi tiết phiếu.'),
              chinh='1. Người dùng bấm In phiếu ở cột Hành động / chân màn chi tiết, hoặc bấm In danh sách trên thanh công cụ.\n'
                    '2. Hệ thống mở cửa sổ “Xem trước phiếu hạch toán mua dịch vụ” / “Xem trước danh sách hạch toán mua dịch vụ”, hiện '
                    '“Đang tải dữ liệu in…”.\n'
                    '3. Hệ thống kiểm tra phạm vi xem, dựng bản in và hiển thị.\n'
                    '4. Người dùng bấm In; hệ thống mở hộp thoại in của trình duyệt.',
              phu='• Bấm (x) / click ra ngoài cửa sổ → đóng.\n'
                  '• Ngoài phạm vi → “Bạn không có quyền xem phiếu này”.\n'
                  '• Thiếu mẫu in → “Không tìm thấy mẫu in "Phiếu hạch toán mua dịch vụ"” / “Không tìm thấy mẫu in "Danh sách hạch toán '
                  'mua dịch vụ"”.\n'
                  '• Danh sách vượt 2.000 dòng → không in, báo vượt mức in tối đa 2.000 dòng, nhắc thu hẹp bộ lọc.\n'
                  '• Bản in rỗng → “Không có dữ liệu để in”; lỗi khác → “Không tải được dữ liệu in”.',
              dacbiet='Letterhead bản in phiếu lấy theo công ty ghi trên phiếu (không theo người đang đăng nhập); bản in danh sách lấy theo '
                      'công ty của người in. Số tiền giữ tối đa 2 số lẻ. In không ghi dữ liệu, không ghi lịch sử.'),
   layout=dict(menu=MENU + ' => In phiếu', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   extra=[('18b_print_list', 'Cửa sổ Xem trước danh sách')],
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo thao tác',
        ['- “Xem trước phiếu hạch toán mua dịch vụ”', '- “Xem trước danh sách hạch toán mua dịch vụ”', '- Có nút (x)']),
       ('Nút In', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Cạnh tiêu đề cửa sổ', '- Khóa khi đang tải hoặc chưa có bản in', '- Bấm → hộp thoại in của trình duyệt']),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu in…”.'),
       ('Đầu bản in phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead công ty của phiếu', '- Số phiếu, ngày lập (dd/mm/yyyy), Loại yêu cầu, Hóa đơn VAT, Phiếu yêu cầu',
         '- Tài khoản nợ, Tài khoản có']),
       ('Thông tin phiếu trên bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Dịch vụ thuê ngoài: Nhà cung cấp, Hợp đồng mua dịch vụ, Diễn giải',
         '- Công nợ bảo hiểm: Số đơn bảo hiểm, Số hợp đồng mua, Phụ lục bổ sung, Diễn giải']),
       ('Bảng chi tiết bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Dịch vụ thuê ngoài: dòng dịch vụ (đơn giá, SL, thành tiền, yêu cầu); 3 dòng tổng',
         '- Công nợ bảo hiểm: dòng bảo hiểm, Tổng trước thuế, VAT, Tổng sau thuế']),
       ('Bảng bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        ['- Các phiếu khớp bộ lọc + phạm vi quyền', '- Tổng thanh toán giữ số lẻ']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Theo mẫu', ['- Theo mẫu in của hệ thống', '- Bản in danh sách ghi người lập = người in']),
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

# ------------------------------------------------------------ 2.12
fr(12, 'Xuất Excel', usecase=('FR-12', 'Xuất Excel', 'io', A_XEM),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất danh sách phiếu ra Excel',
              mota='Người dùng chọn trường và thứ tự cột trong cửa sổ “Chọn trường xuất file” rồi tải file gồm toàn bộ phiếu khớp bộ lọc và '
                   'phạm vi (không riêng trang đang xem). Màn không có xuất Excel một phiếu.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Xuất Excel trên thanh công cụ.\n'
                    '2. Hệ thống mở cửa sổ “Chọn trường xuất file” với 12 trường, tích sẵn đúng các cột đang hiện trên bảng.\n'
                    '3. Người dùng tích / bỏ tích, kéo đổi thứ tự, bấm Xuất file.\n'
                    '4. Hệ thống lấy toàn bộ phiếu theo bộ lọc + phạm vi quyền + sắp xếp, dựng file.\n'
                    '5. Hệ thống tải file “danh_sach_hach_toan_mua_dich_vu.xlsx”, hiển thị “Xuất Excel thành công.”.',
              phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → không xuất.\n'
                  '• Không có phiếu khớp bộ lọc → vẫn tải file, chỉ có tiêu đề cột.\n'
                  '• Lỗi → “Lỗi khi xuất Excel”.',
              dacbiet='Cấu trúc file: dòng 1 logo công ty; dòng 2 tiêu đề “Danh sách hạch toán mua dịch vụ”; dòng 3 tên cột gồm STT rồi các '
                      'trường đã chọn đúng thứ tự; Tổng thanh toán là ô số (cộng SUM được); Số phiếu, Phiếu yêu cầu, Số hợp đồng luôn là ô '
                      'chữ (giữ số 0 đầu, mã toàn chữ số không thành số); ngày dạng dd/mm/yyyy hh:mm. Khóa nút Xuất Excel trong lúc chờ file.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn trường xuất file”', 'Kèm nút (x) đóng.'),
       ('Danh sách trường', 'Table/Grid', 'Enable', '12 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Số phiếu, Loại yêu cầu, Phiếu yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán',
         '- Ngày tạo, Người tạo, Ngày hạch toán, Người cập nhật, Ngày cập nhật, Trạng thái']),
       ('Ô tích của trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Theo cột đang hiện', 'Tích: trường có trong file.'),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Thứ tự trong danh sách = thứ tự cột trong file.'),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/12 trường”.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi trường.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → đóng cửa sổ, tải file']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công.”', '- Lỗi: “Lỗi khi xuất Excel”'])],
   ev=[('Bấm Xuất Excel', 'Click',
        'Before:\n– Nút khóa khi đang có lượt xuất chạy.\nDuring:\n– Tích sẵn các trường tương ứng cột đang hiện.\n'
        'After:\n– Mở cửa sổ “Chọn trường xuất file”.'),
       ('Kéo tay nắm', 'Drag', 'Before:\n– Áp cho mọi trường.\nDuring:\n– Đổi thứ tự.\nAfter:\n– Thứ tự mới là thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; khóa nút Xuất Excel.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc + phạm vi quyền (bỏ phân trang); dựng file với các cột đúng thứ tự đã chọn.\n' + ERR + '\n'
        'After:\n– Tải file “danh_sach_hach_toan_mua_dich_vu.xlsx”; hiển thị “Xuất Excel thành công.”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”; mở khóa nút.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ.')])

# ------------------------------------------------------------ 2.13
fr(13, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(ten='Xem lịch sử thay đổi của phiếu',
              mota='Xem các mốc thao tác trên một phiếu: Tạo mới, Thay đổi thông tin (trường cũ → mới, dòng dịch vụ thêm / xóa, file đính '
                   'kèm thêm / xóa), Thay đổi trạng thái (Đang tạo → Đã duyệt), Xóa; mỗi mốc ghi người thực hiện và thời điểm. Mở từ nút '
                   'Lịch sử ở cột Hành động hoặc khối Lịch sử ở màn chi tiết.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc trong nút “…”), hoặc bấm Xem lịch sử ở màn chi tiết.\n'
                    '2. Hệ thống mở cửa sổ lịch sử thay đổi của phiếu (hoặc mở khối Lịch sử).\n'
                    '3. Hệ thống hiển thị các mốc, mới nhất trên cùng.\n'
                    '4. Người dùng bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.',
              phu='• Phiếu tạo trên ERP trước khi bật lịch sử → “Chưa có lịch sử thao tác nào.”.\n'
                  '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
                  '• Bấm tên file ở mốc File đính kèm → mở cửa sổ xem trước file (mốc ghi trước 15/10/2026 chỉ hiện tên, không bấm được).\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; danh sách giữ nguyên trang, bộ lọc, sắp xếp.',
              dacbiet='Thứ tự: mới nhất trên cùng. Mỗi mốc: thời gian dd/mm/yyyy hh:mm, nhãn hành động có màu, người thực hiện, nội dung cũ '
                      '→ mới. Trường theo dõi: Phiếu yêu cầu, Nhà cung cấp, Hóa đơn VAT, Thuế VAT (%), Tài khoản nợ, Tài khoản có, Mã phí, '
                      'Vụ việc, Diễn giải, Trạng thái, File đính kèm, Dòng dịch vụ (Dịch vụ, Yêu cầu, SL hạch toán, Đơn giá, Mã phí, Vụ '
                      'việc). Lưu không đổi gì thì không sinh mốc.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', ['- Lịch sử thay đổi kèm số phiếu', '- Có nút (x) đóng']),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Mới nhất trên cùng', '- Mỗi mốc: nhãn, thời điểm, người thực hiện']),
       ('Mốc Tạo mới', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Ghi khi lưu phiếu lần đầu (Lưu nháp hoặc Lưu và duyệt).'),
       ('Mốc Thay đổi thông tin', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Trường đã đổi: cũ → mới', '- “Dòng dịch vụ thêm mới / đã xóa”', '- “File đính kèm thêm mới / đã xóa” (bấm tên file xem trước)']),
       ('Mốc Thay đổi trạng thái', 'Label', 'Read-only', '–', 'Theo dữ liệu', ['- Đang tạo → Đã duyệt (sửa rồi Lưu và duyệt)']),
       ('Mốc Xóa', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Ghi khi người tạo xóa phiếu nháp.'),
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
       ('Bấm tên file trong mốc', 'Click', 'Before:\n– Mốc File đính kèm có đường dẫn file.\nDuring:\n– Lấy đường dẫn.\n'
        'After:\n– Mở cửa sổ xem trước file.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không ghi gì.\nAfter:\n– Đóng cửa sổ, danh sách giữ nguyên.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Hạch toán mua dịch vụ; không lặp lại các quy tắc đã có trong SRS '
           'quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Bố cục theo loại yêu cầu', [
        '– Loại lấy theo phiếu yêu cầu, không đổi được.',
        '– Dịch vụ thuê ngoài: Hợp đồng, Nhà cung cấp, TK nợ / có chọn được, bảng dịch vụ (Đơn giá, SL hạch toán, Mã phí, Mã vụ việc).',
        '– Công nợ bảo hiểm: thông tin bảo hiểm chỉ đọc, TK nợ 1541 / TK có 3311 cố định, 1 dòng bảo hiểm chọn Mã phí, Vụ việc.'],
     ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-02', 'Lưu nháp và Lưu và duyệt', [
        '– Lưu nháp chỉ bắt buộc Phiếu yêu cầu; Đơn giá / SL không âm, SL không vượt SL yêu cầu, VAT 0–100.',
        '– Lưu và duyệt bắt buộc Hóa đơn VAT; Kèm hóa đơn phải có ≥ 1 file; Dịch vụ thuê ngoài bắt buộc NCC, TK nợ, TK có, Đơn giá; '
        'Tổng thanh toán > 0; hỏi xác nhận trước khi ghi sổ.'], ['Lập phiếu', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-03', 'SL hạch toán và mã bắt buộc theo tài khoản', [
        '– 0 ≤ SL hạch toán ≤ SL yêu cầu (máy chủ lấy lại SL yêu cầu từ phiếu yêu cầu, không tin số gửi lên).',
        '– TK nợ thuộc nhánh 154 (kể cả tài khoản con) → Mã vụ việc bắt buộc từng dòng; nhánh 642 → Mã phí bắt buộc từng dòng.',
        '– Mã phí / Mã vụ việc đổi ở dòng đầu áp cho mọi dòng.'], ['Lập phiếu', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-04', 'Vòng đời trạng thái', [
        '– Lưu nháp → Đang tạo (phiếu yêu cầu: Đang hạch toán).', '– Lưu và duyệt → Đã duyệt (phiếu yêu cầu: Đã hạch toán); không quay lại.',
        '– Xóa phiếu Đang tạo → phiếu yêu cầu về Chờ duyệt.', '– Sửa / Xóa: người tạo có quyền Q1, phiếu Đang tạo.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Lưu và duyệt']),
    ('BR-05', 'Nguồn lập phiếu', [
        '– Phiếu yêu cầu phải Chờ duyệt, cùng công ty với người lập, người lập có quyền Hạch toán mua dịch vụ.',
        '– Cửa sổ chọn chỉ liệt kê phiếu Chờ duyệt do chính người dùng tạo; phiếu của người khác vào bằng nút Hạch toán ở màn Yêu cầu.',
        '– Khóa phiếu yêu cầu khi lưu: 2 kế toán cùng lập cho 1 phiếu thì người sau bị chặn.'],
     ['Chọn phiếu yêu cầu', 'Lập phiếu']),
    ('BR-06', 'Phạm vi xem', [
        '– Xét V1 → V2 → V3; không có quyền nào thì chỉ phiếu mình tạo; Super admin như V1.',
        '– Phiếu Đang tạo của người khác luôn ẩn.'], ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel', 'Xem lịch sử thay đổi']),
    ('BR-07', 'Ghi sổ kế toán', [
        '– Dịch vụ thuê ngoài: Nợ TK nợ = thành tiền từng dòng; Nợ 1331 = tiền VAT; Có TK có = tổng sau VAT, đối tượng NCC.',
        '– Công nợ bảo hiểm: Nợ 1541 / Có 3311 = Tổng sau thuế, kèm Mã phí, Vụ việc.',
        '– Công ty / phòng ban của bút toán theo hợp đồng (thiếu thì theo người lập); ngày hạch toán = lúc duyệt.'], ['Lưu và duyệt']),
    ('BR-08', 'Cập nhật chứng từ liên quan khi duyệt', [
        '– Cộng SL hạch toán vào SL đã hạch toán của dòng phân bổ hợp đồng mua dịch vụ.',
        '– Đơn bảo hiểm và phụ lục chuyển Đã hạch toán.', '– Phiếu yêu cầu ghi Người duyệt, Ngày duyệt.'], ['Lưu và duyệt']),
    ('BR-09', 'File đính kèm', [
        '– Chỉ nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; tối đa 20MB/file.',
        '– Màn Tạo: file của phiếu yêu cầu hiện sẵn, gỡ được; phiếu lưu đúng danh sách file người dùng thấy.',
        '– Xóa file đã lưu có hiệu lực ngay và ghi lịch sử.'], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-10', 'Tính duy nhất', [
        '– Số phiếu <mã công ty>.HTMDV.<năm><6 số> do hệ thống sinh, duy nhất, không sửa được.',
        '– Mỗi phiếu yêu cầu chỉ có 1 phiếu hạch toán; phiếu không có trường nhập duy nhất khác.'], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-11', 'Chuẩn hóa dữ liệu nhập', [
        '– Ô số (Đơn giá, SL, VAT) chỉ nhận số, hiển thị dấu phẩy ngăn nghìn, tối đa 2 số lẻ.',
        '– Diễn giải tối đa 1.000 ký tự; nhận mọi ký tự, hiển thị nguyên văn.',
        '– Tổng tiền do máy chủ tính lại, không tin số gửi từ màn hình.'], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-12', 'Liên kết cha – con', [
        '– Dòng dịch vụ và dòng yêu cầu thuộc một phiếu; xóa phiếu xóa toàn bộ, không để dòng mồ côi.',
        '– Dòng phải thuộc phiếu yêu cầu đã chọn (“Dịch vụ – Không thuộc phiếu yêu cầu đã chọn”).',
        '– Phiếu yêu cầu nguồn khóa sau khi lưu, không đổi được ở màn Sửa.'], ['Lập phiếu', 'Chỉnh sửa', 'Xóa']),
    ('BR-13', 'Điều kiện xóa và sử dụng ở màn khác', [
        '– Chỉ xóa phiếu Đang tạo (chưa ghi sổ); phiếu Đã duyệt đã có bút toán nên không xóa / sửa.',
        '– Bút toán của phiếu dùng ở sổ kế toán / báo cáo tài khoản; trạng thái phiếu quyết định trạng thái phiếu yêu cầu.'],
     ['Xóa', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-14', 'Quy tắc ghi lịch sử', [
        '– Ghi: Tạo mới, Thay đổi thông tin (cũ → mới, dòng dịch vụ, file), Thay đổi trạng thái (Đang tạo → Đã duyệt), Xóa.',
        '– Lưu không đổi gì thì không ghi; mỗi lần đổi trạng thái phiếu yêu cầu cũng ghi một mốc bên phiếu yêu cầu.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Lưu và duyệt', 'Xem lịch sử thay đổi']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc dữ liệu do Hạch toán mua dịch vụ ghi ra (trạng thái ghi ngược về phiếu yêu cầu, số lượng đã hạch toán và bút toán ghi sổ khi Lưu và duyệt).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Bán hàng', 'Yêu cầu hạch toán mua dịch vụ (trạng thái Đang hạch toán / Đã hạch toán, Người duyệt, Ngày duyệt do phiếu hạch toán ghi ngược về; xóa phiếu hạch toán nháp trả phiếu yêu cầu về Chờ duyệt)', 'Bán hàng -> Yêu cầu -> Mua dịch vụ'),
    ('2', 'Tài chính', 'Yêu cầu hạch toán mua dịch vụ (như dòng 1)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Mua dịch vụ'),
    ('3', 'Tài chính', 'Sổ kế toán, báo cáo tài khoản và công nợ nhà cung cấp (bút toán Nợ / Có, số phiếu, ngày hạch toán, nhà cung cấp, hợp đồng ghi khi Lưu và duyệt)', 'Tài chính -> Sổ tổng hợp; Tài chính -> Kế toán công nợ -> Nhà cung cấp'),
    ('4', 'Hệ thống ERP', 'Hợp đồng mua dịch vụ (cộng số lượng đã hạch toán theo dòng phân bổ khi phiếu được duyệt)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('5', 'Hệ thống ERP', 'Đơn bảo hiểm / phụ lục (duyệt phiếu loại Công nợ bảo hiểm thì đơn chuyển đã hạch toán)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
