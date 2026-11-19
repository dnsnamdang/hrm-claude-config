# -*- coding: utf-8 -*-
"""SRS màn "Hệ số công nghệ theo nhóm hàng hóa" (màn DANH MỤC: danh sách + popup Thêm / Sửa / Xem) — form chuẩn Danh mục quốc gia,
chuẩn 04/11/2026 (Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).

Chạy: python gen_srs.py  → SRS - Hệ số công nghệ theo nhóm hàng hóa.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../bien-ban-xu-ly-thua-thieu-kiem-ke/gen_srs.py (06/11/2026).
Nguồn đọc 06/11/2026 (nhánh develop, checkout từ gop_db, cả 2 repo):
  BE  Modules/CustomerCare/{Entities/BenefitRate/{BenefitRate,BenefitRateHasGroupProduct}.php, Services/BenefitRateService.php,
      Http/Controllers/V1/BenefitRateController.php, Http/Requests/BenefitRate/BenefitRateRequest.php,
      Transformers/BenefitRateResource/BenefitRateResource.php, Routes/api.php (/benefit-rates — KHÔNG gắn checkPermission)},
      Services/WrApproveResultSourceService.php::productCoefficient() (màn đọc ngược hệ số), app/Services/CatalogHistoryService.php
  FE  pages/admin/benefit-rates/{index.vue, components/BenefitRateModal.vue}, components/subsystem-menu/sale-hub.js (Bán hàng ›
      Quy chế - Thiết lập › Thiết lập), components/modal/{CatalogHistoryModal,export-fields-modal}.vue, components/assign/SystemInfoSection.vue,
      utils/export/listExportFile.js, utils/mixins/{filterStateMixin,unsavedModalMixin,formValidateMixin}.js
  Bối cảnh: design.md, plan.md (Redmine #11705), spec docs/superpowers/specs/gop-db/2026-10-13-benefit-rates-design.md
Ảnh: ./hscn_shots — dev-hrm 06/11/2026 (_capture/capture.js, chặn mọi yêu cầu ghi). Công ty của DNS Admin trên dev chưa có hệ số nào →
  danh sách / chi tiết / người lọc / lịch sử là DỮ LIỆU GIẢ trả trên trình duyệt (12 hệ số); 10e_duplicate: yêu cầu Lưu bị chặn, lỗi trùng
  là phản hồi giả trên trình duyệt (đúng câu lỗi của máy chủ).
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

TEN = 'Hệ số công nghệ theo nhóm hàng hóa'
SHOTS = os.path.join(HERE, 'hscn_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Bán hàng => Quy chế - Thiết lập => Thiết lập => Hệ số công nghệ theo nhóm hàng hóa'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Hệ số công nghệ theo nhóm hàng hóa.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
MISS = '“Bạn chưa nhập đầy đủ thông tin.”'
REQ = '“Bắt buộc phải nhập”'
DUP = '“Loại tỷ lệ hưởng đã tồn tại.”'
TAKEN = '“<Tên nhóm> đã thuộc loại hệ số khác.”'
SYS = '“Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”'

A_ND = 'Người dùng thiết lập hệ số'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản (màn không gắn quyền riêng, giữ như hệ thống '
      'cũ); chỉ thao tác trên hệ số thuộc công ty của chính mình.')
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Hệ số công nghệ theo nhóm hàng hóa.\n'
      '3. Tài khoản đã gắn công ty (không có công ty → danh sách luôn rỗng).')

d = SrsDoc(out=OUT, menu=MENU, route='/admin/benefit-rates', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Bán hàng': 'menu_phanhe', 'Quy chế - Thiết lập': 'menu_nhom', 'Thiết lập': 'menu_nhom2',
    'Hệ số công nghệ theo nhóm hàng hóa': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Xem chi tiết': 'link_ten',
    'Lịch sử': 'btn_lichsu_row', 'Xuất Excel': 'btn_xuatexcel',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình danh mục Hệ số công nghệ theo nhóm hàng hóa (trên popup gọi là “tỷ lệ hưởng công '
    'khoán”), chuyển từ hệ thống cũ (Quản trị hệ thống › Cấu hình) sang phân hệ Bán hàng, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phạm vi dữ liệu và luồng xử lý của màn hình.',
    'Làm rõ cách khai báo một loại hệ số (tên loại, hệ số tối đa 2 số lẻ) và gán cho một hoặc nhiều nhóm hàng hóa — mỗi nhóm hàng '
    'hóa chỉ được thuộc đúng một loại hệ số.',
    'Làm rõ hệ số được dùng ở đâu: khi duyệt kết quả lắp đặt (Phiếu nhập kết quả), dòng hàng chưa có hệ số thì hệ thống lấy hệ số '
    'theo nhóm hàng hóa của hàng; nhóm chưa khai hệ số thì lấy 1.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Thêm mới (Lưu / Lưu và tiếp tục), Chỉnh sửa, '
    'Xóa, Xem chi tiết, Xem lịch sử thay đổi, Xuất Excel danh sách. Màn KHÔNG có Khóa / Mở khóa (không có trạng thái), Import Excel, '
    'In (như hệ thống cũ).')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Hệ số là thước đo độ khó công nghệ của nhóm hàng, nhân vào công khoán duyệt của dòng lắp đặt: kết quả công khoán = công khoán '
    'duyệt × hệ số.',
    'Dữ liệu được đọc ngược tại form Duyệt kết quả của Phiếu nhập kết quả (Phần 5); các phiếu chỉ CHÉP số hệ số tại thời điểm lập, '
    'không giữ liên kết tới bản ghi hệ số.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Mỗi người dùng chỉ thấy và thao tác hệ số thuộc công ty của mình (BR-01).',
    'Loại tỷ lệ hưởng không được trùng trong cùng công ty (BR-02).',
    'Một nhóm hàng hóa chỉ thuộc một loại hệ số, kiểm trên TOÀN hệ thống, không theo công ty (BR-03).',
    'Xóa hẳn không điều kiện vì không phiếu nào giữ liên kết tới hệ số (BR-06).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hệ số công nghệ (tỷ lệ hưởng công khoán)', 'Một bản ghi của màn: Loại tỷ lệ hưởng + Hệ số + danh sách Nhóm hàng hóa áp dụng. '
                                               'Danh sách gọi tên cột là “Loại hệ số”, popup gọi “Loại tỷ lệ hưởng” — cùng một trường.'),
    ('Loại tỷ lệ hưởng (Loại hệ số)', 'Tên loại hệ số, 1–255 ký tự, không trùng trong công ty; là trường định danh của bản ghi '
                                      '(màn không có mã).'),
    ('Hệ số', 'Số không âm, tối đa 2 chữ số thập phân, tối đa 999,999.99; hiển thị dấu phẩy ngăn nghìn, dấu chấm thập phân, luôn 2 '
              'số lẻ ở danh sách (vd 1.50).'),
    ('Nhóm hàng hóa', 'Nhóm trong danh mục nhóm hàng hóa dùng chung (cây hàng hóa). Chỉ nhóm đang hoạt động được chọn mới; nhóm đã '
                      'gắn rồi bị khóa vẫn hiện kèm biểu tượng ổ khóa.'),
    ('Nhóm đã thuộc loại hệ số khác', 'Nhóm hàng hóa đã được gán cho một hệ số khác (của bất kỳ công ty nào) — không gán thêm được.'),
    ('Công ty của bản ghi', 'Công ty của người tạo, hệ thống tự ghi khi tạo; quyết định ai được thấy bản ghi.'),
    ('Trạng thái bản ghi', 'Màn KHÔNG có trạng thái (không có Hoạt động / Khóa): bản ghi tồn tại thì có hiệu lực, xóa là mất hẳn.'),
    ('Cấu trúc phân cấp', 'Hệ số > các nhóm hàng hóa áp dụng (quan hệ một – nhiều; mỗi nhóm thuộc tối đa một hệ số).'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn KHÔNG gắn quyền riêng (giữ như hệ thống cũ — user chốt 13/10/2026): menu luôn hiện, mọi thao tác Xem / Thêm / Sửa / Xóa / '
    'Lịch sử / Xuất Excel không kiểm quyền. Phạm vi dữ liệu do CÔNG TY của người đăng nhập quyết định.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', 'Không có quyền riêng (mọi người dùng đã đăng nhập)', 'Thấy menu và màn; dùng được mọi nút: Tạo mới, Sửa, Xóa, Lịch sử, '
                                                               'Xuất Excel, Cấu hình cột, Cài đặt bộ lọc.'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('—', 'Công ty của người đăng nhập', 'Chỉ hệ số có công ty = công ty người đăng nhập (kể cả Super admin). Không gắn công ty → '
                                         'không thấy hệ số nào.'),
], widths=[0.8, 2.2, 3.0])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người dùng (hệ số công ty mình)', 'Hệ số công ty khác', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '❌ không hiện', '✅ (không cần quyền)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌ ô Công ty chọn công ty khác → rỗng', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '—', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '—', '✅'),
    ('FR-05 Thêm mới', '✅ (ghi công ty mình)', '—', '✅'),
    ('FR-06 Chỉnh sửa', '✅', '❌ báo trạng thái đã thay đổi', '✅'),
    ('FR-07 Xóa', '✅', '❌ báo trạng thái đã thay đổi', '✅'),
    ('FR-08 Xem chi tiết', '✅', '❌ báo trạng thái đã thay đổi', '✅'),
    ('FR-09 Xem lịch sử thay đổi', '✅', '—', '✅'),
    ('FR-10 Xuất Excel', '✅ (chỉ công ty mình)', '❌', '✅'),
    ('Khóa / Mở khóa, Import, In', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.9, 1.5, 1.6, 1.0])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Màn không có quyền riêng nên không có trường hợp “thiếu quyền” — người dùng nào đăng nhập cũng vào được và thao tác được.',
    'Mở chi tiết / sửa / xóa hệ số không thuộc công ty mình (hoặc vừa bị người khác xóa) → hệ thống báo ' + CONFLICT +
    ', không hiện dữ liệu.',
    'Tài khoản chưa gắn công ty → danh sách rỗng “Không có dữ liệu phù hợp.”; vẫn bấm được Tạo mới.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới, Xuất Excel, Cấu hình cột', 'Luôn hiện', 'Không gắn quyền'),
    ('Nút Sửa, Lịch sử trên dòng', 'Mọi dòng', 'Hiện thẳng (không có menu ba chấm)'),
    ('Nút Xóa trên dòng', 'Mọi dòng (máy chủ luôn cho xóa)', 'Mở hộp Xác nhận xóa'),
    ('Nút Lưu và tiếp tục', 'Chỉ ở popup Thêm mới', 'Popup Sửa chỉ có Lưu, Đóng'),
    ('Nút Cài đặt bộ lọc, Tìm kiếm nâng cao', 'Bộ lọc có 4 ô (tìm nhanh + 3 ô lọc) > 3', 'Ẩn hết ô lọc bằng Cài đặt bộ lọc thì vẫn còn nút'),
], widths=[2.2, 2.3, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_ND, [0, 1, 2, 3, 4])],
    [('FR-01', 'Xem danh sách hệ số', 'view'),
     ('FR-05', 'Thêm mới hệ số', 'crud'),
     ('FR-06', 'Chỉnh sửa hệ số', 'crud'),
     ('FR-07', 'Xóa hệ số', 'action'),
     ('FR-10', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-08', 'Xem chi tiết', 'view', 'extend', [0], None),
     ('FR-09', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Hệ số công nghệ theo nhóm hàng hóa')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách hệ số',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách hệ số công nghệ theo nhóm hàng hóa',
       mota='Hiển thị bảng các hệ số thuộc công ty của người đăng nhập: loại hệ số, hệ số, các nhóm hàng hóa áp dụng (mỗi nhóm một '
            'dòng trong ô), người tạo, ngày tạo, người cập nhật, ngày cập nhật, kèm phân trang và tổng số. Mỗi dòng có liên kết mở '
            'popup Xem và 3 nút Sửa, Xóa, Lịch sử.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng vào màn từ menu phân hệ Bán hàng.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định công ty của người đăng nhập; chỉ lấy hệ số thuộc công ty đó.\n'
             '3. Hệ thống nạp cấu hình cột đã lưu của người dùng và danh sách Người tạo / Người cập nhật cho bộ lọc.\n'
             '4. Hệ thống sắp hệ số tạo gần nhất ở trên (chưa chọn cột sắp xếp).\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, dòng “Hiển thị a–b / N” và phân trang.',
       phu='• Công ty chưa có hệ số nào / tài khoản chưa gắn công ty → trong bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp danh sách → thông báo “Lỗi khi tải dữ liệu”, bảng trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
           '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo hết phiên, chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 9 cột (STT, Loại hệ số, Hệ số, Nhóm hàng hóa, Người tạo, Ngày tạo, Người cập nhật, Ngày cập '
               'nhật, Hành động); không có cột ẩn mặc định. Cột khóa (không ẩn, không đổi vị trí): STT, Loại hệ số, Hành động; STT và '
               'Loại hệ số ghim trái khi cuộn ngang. Sắp xếp được: Loại hệ số, Hệ số, Ngày tạo, Ngày cập nhật. Đổi sắp xếp / bộ lọc / '
               'số dòng đều về trang 1. Bảng cố định bề rộng cột để không nhảy cột khi sắp xếp.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Hệ số công nghệ theo nhóm hàng hóa'),
   extra=[(shot('00_menu'), 'Vị trí mục menu: phân hệ Bán hàng › Quy chế - Thiết lập › Thiết lập')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Hệ số công nghệ theo nhóm hàng hóa” trên tiêu đề bảng, thanh tiêu đề trang và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Luôn hiện (không gắn quyền)', '- Bấm → mở popup “Thêm mới tỷ lệ hưởng công khoán” (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.10)', '- Khóa trong lúc đang xuất; cạnh nút hiện dòng tiến độ']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa, ghim trái']),
       ('Cột Loại hệ số', 'Link', 'Read-only', '1–255 ký tự', 'Hiển thị',
        ['- Tên loại, xuống dòng khi dài', '- Bấm → mở popup Xem (mục 2.8)', '- Sắp xếp được', '- Cột khóa, ghim trái']),
       ('Cột Hệ số', 'Table/Grid', 'Read-only', '0 – 999,999.99', 'Hiển thị',
        ['- Căn phải, luôn 2 số lẻ, dấu phẩy ngăn nghìn (vd 1.50; 1,234.50)', '- Sắp xếp được (theo giá trị số)']),
       ('Cột Nhóm hàng hóa', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Mỗi nhóm áp dụng một dòng, xếp theo tên nhóm', '- Không sắp xếp']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Dạng “Họ tên - Mã phòng ban”', '- Không sắp xếp']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Sắp xếp được.'),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Người lưu gần nhất, dạng “Họ tên - Mã phòng ban”', '- Mới tạo chưa sửa: bằng Người tạo', '- Không sắp xếp']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Thời điểm lưu gần nhất (kể cả khi chỉ đổi nhóm hàng hóa)', '- Sắp xếp được']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Sửa (bút chì) → popup Chỉnh sửa (mục 2.6)', '- Xóa (thùng rác đỏ) → hộp Xác nhận xóa (mục 2.7)',
           '- Lịch sử (đồng hồ) → cửa sổ Lịch sử thay đổi (mục 2.9)', '- Cột khóa trong Tùy chỉnh cột']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', ['- Trong bảng: “Không có dữ liệu phù hợp.”', '- Chỉ hiện khi N = 0']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang đang xem', '- N: tổng số hệ số khớp bộ lọc của công ty mình']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút « ‹ số trang › »', '- Ở trang đầu « ‹ mờ; ở trang cuối › » mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Lỗi khi tải dữ liệu” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Không kiểm quyền (màn không gắn quyền).\n– Xác định công ty người đăng nhập; không có công ty → tập rỗng.\n'
        'During:\n– Lấy hệ số của công ty, sắp tạo mới nhất trước; nạp cấu hình cột + danh sách người lọc.\n'
        '– Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, dòng “Hiển thị a–b / N”; bộ lọc trống (không khôi phục bộ lọc cũ).'),
       ('Bấm Loại hệ số', 'Click',
        'Before:\n– Hệ số thuộc công ty mình.\nAfter:\n– Mở popup Xem (mục 2.8); danh sách phía sau giữ nguyên trang, bộ lọc.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Loại hệ số, Hệ số, Ngày tạo, Ngày cập nhật hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc; cùng giá trị thì bản ghi mới hơn ở trên.'),
       ('Bấm số trang hoặc nút « ‹ › »', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại một lần theo số dòng mới.'),
       ('Rời màn rồi quay lại / tải lại trang', 'System',
        'Before:\n– Màn không có trang con nên bộ lọc không được ghi nhớ.\n'
        'After:\n– Bộ lọc, ô tìm nhanh, sắp xếp, trang về mặc định; cấu hình cột vẫn giữ (lưu theo người dùng).'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc hệ số',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách hệ số',
       mota='Thu hẹp danh sách theo loại hệ số (ô tìm nhanh), công ty, người tạo, người cập nhật. Các ô lọc nằm trong khối Tìm kiếm '
            'nâng cao, bật / tắt được bằng Cài đặt bộ lọc (mục 2.3). Mọi tiêu chí chỉ thu hẹp trong các hệ số thuộc công ty người '
            'đăng nhập.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập chữ vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn Công ty / Người tạo / Người cập nhật.\n'
             '3. Hệ thống lọc ngay khi một ô chọn đổi giá trị, về trang 1; ô tìm nhanh chỉ áp khi bấm Tìm kiếm / Enter.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Chọn Công ty khác công ty mình → luôn rỗng (ô Công ty chỉ lọc thêm trên phạm vi công ty mình, giữ như hệ thống cũ).\n'
           '• Ô Người tạo / Người cập nhật chỉ liệt kê người đã tạo / đã cập nhật hệ số của công ty mình; chưa có hệ số → ô rỗng.\n'
           '• Ô lọc bị tắt trong Cài đặt bộ lọc → không hiện trên khối lọc.',
       dacbiet='Ô tìm nhanh khớp MỘT PHẦN tên loại hệ số, không phân biệt hoa / thường và không phân biệt dấu (theo cách so sánh chữ '
               'của cơ sở dữ liệu); bỏ khoảng trắng đầu / cuối; không giới hạn số ký tự; ký tự % và _ được tìm đúng nghĩa đen. Mọi '
               'điều kiện kết hợp kiểu VÀ. Bộ lọc KHÔNG được ghi nhớ khi rời màn / tải lại trang.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo loại tỷ lệ hưởng”', '- Khớp một phần Loại hệ số', '- Áp khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Bấm → xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống',
        ['- Mặc định: trống', '- Liệt kê mọi công ty trong hệ thống', '- Chọn công ty mình → như không lọc; công ty khác → rỗng']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Người đã tạo hệ số của công ty mình, dạng “Họ tên - Mã phòng ban”, xếp theo tên']),
       ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Người đã lưu gần nhất các hệ số của công ty mình']),
       ('Kết quả lọc', 'Table/Grid', 'Read-only', '–', '–', 'Theo kết quả',
        ['- Bảng + dòng “Hiển thị a–b / N” cập nhật theo tiêu chí', '- Rỗng: “Không có dữ liệu phù hợp.”']),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\n'
        'During:\n– Bỏ qua khi giá trị không đổi.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí (một lần).'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm hệ số có tên loại chứa chuỗi nhập (không phân biệt hoa / thường, dấu).\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Gõ vào ô tìm nhanh (chưa bấm Tìm kiếm)', 'Change',
        'Before:\n– Chỉ đổi chữ trong ô tìm nhanh.\nAfter:\n– Danh sách chưa đổi cho tới khi bấm Tìm kiếm / Enter.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa mọi tiêu chí, bỏ sắp xếp, nạp lại từ trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\nAfter:\n– Mở / thu gọn khối 3 ô lọc Công ty, Người tạo, Người cập nhật.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn ô lọc muốn thấy trong khối Tìm kiếm nâng cao (Công ty, Người tạo, Người cập nhật) và sắp lại '
            'thứ tự. Cấu hình lưu riêng theo người dùng cho màn này, không ảnh hưởng người khác và không đổi dữ liệu hệ số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 3 mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 3 mục theo thứ tự thiết kế; phải bấm Lưu mới có hiệu lực.\n'
           '• Bỏ tích mục đang có giá trị lọc → mục bị ẩn và giá trị lọc của mục đó bị bỏ.\n'
           '• Bỏ bớt mục để tổng ô (kể cả ô tìm nhanh) ≤ 3 → các ô còn lại bày thẳng trên hàng tìm nhanh, nút Tìm kiếm nâng cao '
           'ẩn; nút Cài đặt bộ lọc vẫn còn để bật lại.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 3 mục', '–', 'Theo cấu hình đã lưu',
        ['- Công ty, Người tạo, Người cập nhật']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → mục đó không hiện ở khối Tìm kiếm nâng cao.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích lại đủ 3 mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Vùng ngoài cửa sổ', 'Popup', 'Enable', '–', '–', 'Hiển thị', '- Click ra ngoài cửa sổ → đóng như nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu (chưa lưu lần nào → đủ 3 mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 3 mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 9 cột của bảng danh sách. Ba cột STT, Loại hệ số, Hành động bị khóa; cấu '
            'hình lưu riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 9 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 9 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ nguyên sau khi tải lại trang, đăng nhập '
               'lại, đổi trình duyệt; người dùng khác không bị ảnh hưởng. Cột đang hiện quyết định trường tích sẵn ở cửa sổ Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 9 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, Loại hệ số, Hệ số, Nhóm hàng hóa, Người tạo', '- Ngày tạo, Người cập nhật, Ngày cập nhật, Hành động']),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Loại hệ số, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/9 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
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
       ('Tích / bỏ tích một cột', 'Change', 'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/9 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng; dữ liệu, bộ lọc, tổng số giữ nguyên.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ dùng chung form
FORM_UI = [
    ('Ô Loại tỷ lệ hưởng', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', [
        '- Gợi ý “Nhập loại tỷ lệ hưởng”', '- Bỏ khoảng trắng đầu / cuối khi lưu; chỉ khoảng trắng coi như trống',
        '- Trống: ' + REQ, '- Quá 255 ký tự: “Vui lòng nhập tối đa 255 ký tự.”',
        '- Trùng tên loại khác cùng công ty (không phân biệt hoa / thường, dấu): ' + DUP]),
    ('Ô Hệ số', 'Textbox', 'Enable', '0 – 999,999.99', 'Có', 'Trống', [
        '- Gợi ý “Nhập hệ số”, căn phải', '- Chỉ nhận chữ số và 1 dấu chấm; chữ, dấu âm bị bỏ ngay khi gõ',
        '- Tối đa 2 số lẻ (gõ số lẻ thứ 3 bị bỏ)', '- Trống: “Bắt buộc phải nhập.”',
        '- Lớn hơn 999,999.99: “Hệ số – Không được lớn hơn 999,999.99”', '- 0 hợp lệ']),
    ('Ô Nhóm hàng hóa áp dụng', 'Dropdown', 'Enable', 'Danh sách nhóm hàng hóa', 'Có', 'Trống', [
        '- Chọn nhiều, gõ để tìm; mỗi nhóm đã chọn là một thẻ có nút ×', '- Gợi ý “Chọn nhóm hàng hóa” (đang tải: “Đang tải...”)',
        '- Lựa chọn: nhóm hàng hóa đang hoạt động, xếp theo tên', '- Trống: ' + REQ,
        '- Nhóm đã thuộc loại hệ số khác: ' + TAKEN]),
    ('Thông báo lỗi dưới ô', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Chữ đỏ có biểu tượng cảnh báo, viền ô đỏ', '- Mất ngay khi sửa đúng ô đó']),
    ('Thông báo thiếu thông tin', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- ' + MISS + ' khi còn ô bắt buộc lỗi', '- Lỗi trùng do máy chủ trả: toast chính câu lỗi trùng']),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng popup; đã đổi dữ liệu thì hỏi “Thông tin chưa lưu”.'),
    ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
    ('Vùng ngoài popup', 'Popup', 'Enable', '–', '–', 'Hiển thị', '- Click ra ngoài → như nút Đóng (có hỏi khi đã đổi dữ liệu).'),
    ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Tiêu đề “Thông tin chưa lưu”', '- Nội dung “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”',
        '- Thoát: đóng popup, bỏ dữ liệu', '- Ở lại: quay lại popup, giữ nguyên dữ liệu đã nhập']),
]

# ------------------------------------------------------------ 2.5 Thêm mới
fr(5, 'Thêm mới hệ số (Lưu / Lưu và tiếp tục)', usecase=('FR-05', 'Thêm mới hệ số', 'crud', A_ND),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Thêm mới hệ số công nghệ theo nhóm hàng hóa',
       mota='Khai báo một loại hệ số mới cho công ty của người đăng nhập: tên loại, hệ số và các nhóm hàng hóa áp dụng. Hệ thống '
            'kiểm tên không trùng trong công ty và mỗi nhóm hàng hóa chưa thuộc loại hệ số nào khác, rồi lưu kèm công ty / phòng ban '
            '/ bộ phận và người tạo.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Tạo mới.\n'
             '2. Hệ thống mở popup “Thêm mới tỷ lệ hưởng công khoán” với 3 ô trống, nạp danh sách nhóm hàng hóa đang hoạt động.\n'
             '3. Người dùng nhập Loại tỷ lệ hưởng, Hệ số, chọn một hoặc nhiều Nhóm hàng hóa áp dụng.\n'
             '4. Người dùng bấm Lưu (hoặc Lưu và tiếp tục).\n'
             '5. Hệ thống kiểm đủ 3 ô bắt buộc trên màn, rồi máy chủ kiểm trùng tên trong công ty và nhóm đã thuộc loại khác.\n'
             '6. Hệ thống lưu hệ số + các nhóm áp dụng, ghi công ty / phòng ban / bộ phận của người tạo.\n'
             '7. Hệ thống ghi một dòng lịch sử “Tạo mới” cho hệ số.\n'
             '8. Hệ thống hiển thị “Thêm mới thành công.”, nạp lại danh sách (hệ số mới ở trên cùng trang 1); Lưu → đóng popup, Lưu '
             'và tiếp tục → giữ popup, làm trắng 3 ô để nhập tiếp.',
       phu='• Thiếu ô bắt buộc → lỗi đỏ dưới từng ô thiếu + toast ' + MISS + ', không gửi máy chủ.\n'
           '• Tên loại trùng trong công ty → lỗi dưới ô Loại tỷ lệ hưởng ' + DUP + ' + toast cùng câu.\n'
           '• Có nhóm đã thuộc loại hệ số khác → lỗi dưới ô Nhóm ' + TAKEN + ' (liệt kê tên các nhóm vướng).\n'
           '• Bấm Đóng / (x) / click ra ngoài khi chưa nhập → đóng ngay; đã nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại).\n'
           '• Nhập rồi xóa về trống như ban đầu → coi như chưa đổi, đóng không hỏi.\n'
           '• Máy chủ lỗi → toast ' + SYS + ', popup giữ nguyên dữ liệu.',
       dacbiet='Nút Lưu / Lưu và tiếp tục / Đóng bị khóa trong lúc đang lưu (chống tạo trùng do bấm liên tục). Màn không có mã tự '
               'sinh; trường duy nhất là Loại tỷ lệ hưởng trong phạm vi công ty. Không có trạng thái mặc định (màn không có trạng thái).'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10_create'), shot_caption='Popup Thêm mới tỷ lệ hưởng công khoán',
               note='Popup Thêm mới được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('10b_validate'), 'Bấm Lưu khi chưa nhập: lỗi dưới từng ô bắt buộc'),
          (shot('10e_duplicate'), 'Lỗi trùng Loại tỷ lệ hưởng và nhóm hàng hóa đã thuộc loại hệ số khác'),
          (shot('10g_unsaved'), 'Hộp Thông tin chưa lưu khi đóng popup đã nhập dữ liệu')],
   ui=[('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Thêm mới tỷ lệ hưởng công khoán”, biểu tượng phần trăm xanh.')]
   + FORM_UI + [
       ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Bấm → kiểm, lưu, đóng popup', '- Khóa khi đang lưu']),
       ('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Chỉ có ở Thêm mới', '- Bấm → kiểm, lưu, giữ popup mở, làm trắng 3 ô']),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Thêm mới thành công.”'),
   ],
   ev=[
       ('Bấm Tạo mới', 'Click',
        'Before:\n– Không kiểm quyền (màn không gắn quyền).\n'
        'After:\n– Mở popup 3 ô trống; nạp nhóm hàng hóa đang hoạt động (ô Nhóm khóa, gợi ý “Đang tải...” trong lúc nạp).'),
       ('Gõ ô Hệ số', 'Change',
        'Before:\n– Lọc ký tự ngay khi gõ: chỉ giữ chữ số + 1 dấu chấm, tối đa 2 số lẻ.\n'
        'After:\n– Trống → “Bắt buộc phải nhập.”; > 999,999.99 → “Hệ số – Không được lớn hơn 999,999.99”; hợp lệ → xóa lỗi.'),
       ('Bấm Lưu / Lưu và tiếp tục', 'Click',
        'Before:\n– Không kiểm quyền; khóa các nút trong lúc lưu.\n'
        '– Kiểm cùng lúc 3 ô bắt buộc trên màn; có lỗi → lỗi đỏ dưới từng ô + toast ' + MISS + ', cuộn tới ô lỗi đầu, không gửi.\n'
        'During:\n– Loại tỷ lệ hưởng trống → ' + REQ + '; quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”\n'
        '– Loại tỷ lệ hưởng trùng trong công ty → ' + DUP + '\n'
        '– Hệ số không phải số không âm 2 số lẻ / > 999999.99 → “Hệ số chỉ nhận số không âm, tối đa 2 chữ số thập phân.”\n'
        '– Nhóm hàng hóa trống → ' + REQ + '; nhóm đã thuộc loại khác → ' + TAKEN + '\n'
        '– Nhóm không còn tồn tại → “Nhóm hàng hóa không tồn tại.”\n' + ERR + '\n'
        'After:\n– Lưu hệ số + nhóm áp dụng, ghi công ty / phòng ban / bộ phận và người tạo.\n'
        '– Ghi một dòng lịch sử “Tạo mới” (Loại hệ số, Hệ số, Nhóm hàng hóa áp dụng).\n'
        '– Hiển thị “Thêm mới thành công.”, nạp lại danh sách + danh sách người lọc.\n'
        '– Lưu: đóng popup. Lưu và tiếp tục: giữ popup, làm trắng 3 ô.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– So dữ liệu với lúc mở popup.\n'
        'After:\n– Không đổi → đóng ngay. Đã đổi → hộp “Thông tin chưa lưu”: Thoát = đóng, bỏ dữ liệu; Ở lại = giữ popup và dữ liệu.'),
       ('Sửa ô đang báo lỗi', 'Change', 'Before:\n– Ô đang có lỗi đỏ.\nAfter:\n– Giá trị hợp lệ → lỗi dưới ô biến mất ngay.'),
   ])

# ------------------------------------------------------------ 2.6 Sửa
fr(6, 'Chỉnh sửa hệ số', usecase=('FR-06', 'Chỉnh sửa hệ số', 'crud', A_ND),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chỉnh sửa hệ số công nghệ theo nhóm hàng hóa',
       mota='Sửa tên loại, hệ số và danh sách nhóm hàng hóa áp dụng của một hệ số thuộc công ty mình. Mọi trường đều sửa được; '
            'hệ thống kiểm trùng như Thêm mới nhưng KHÔNG tính trùng với chính bản ghi đang sửa, rồi ghi lịch sử giá trị cũ → mới.',
       tacnhan=TN, dieukien=DK + '\n4. Hệ số thuộc công ty của người đăng nhập.',
       chinh='1. Người dùng bấm Sửa ở cột Hành động.\n'
             '2. Hệ thống nạp chi tiết hệ số, mở popup “Chỉnh sửa tỷ lệ hưởng công khoán” điền sẵn 3 ô.\n'
             '3. Người dùng sửa thông tin.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống kiểm như Thêm mới (bỏ qua chính bản ghi khi kiểm trùng tên và nhóm).\n'
             '6. Hệ thống lưu, thay toàn bộ nhóm áp dụng theo lựa chọn mới, cập nhật Người cập nhật / Ngày cập nhật.\n'
             '7. Hệ thống ghi một dòng lịch sử “Thay đổi thông tin” với từng trường cũ → mới (không đổi gì thì không ghi).\n'
             '8. Hệ thống hiển thị “Cập nhật thành công.”, đóng popup, nạp lại danh sách (giữ trang đang xem).',
       phu='• Hệ số vừa bị người khác xóa / không thuộc công ty mình → toast ' + CONFLICT + ', popup tự đóng, danh sách nạp lại.\n'
           '• Nhóm đang gắn đã bị khóa ở danh mục nhóm hàng hóa → vẫn hiện trong ô, có biểu tượng ổ khóa; giữ nguyên lưu được.\n'
           '• Lỗi kiểm tra → như Thêm mới (lỗi dưới ô + toast).\n'
           '• Hai người cùng sửa một hệ số → lần lưu sau ghi đè lần trước, mỗi lần đều ghi lịch sử.\n'
           '• Bấm Đóng / (x) / click ra ngoài: chưa đổi → đóng ngay; đã đổi → hộp “Thông tin chưa lưu”.',
       dacbiet='Không có Lưu và tiếp tục. Chỉ đổi nhóm hàng hóa cũng cập nhật Người cập nhật / Ngày cập nhật. Không có trạng thái '
               'Khóa nên không có trường hợp “sửa bản ghi đã khóa”.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('12_edit'),
               shot_caption='Popup Chỉnh sửa tỷ lệ hưởng công khoán (nhóm đã khóa có biểu tượng ổ khóa)',
               note='Popup Chỉnh sửa được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chỉnh sửa tỷ lệ hưởng công khoán”.')]
   + [(r[0], r[1], r[2], r[3], r[4], 'Theo dữ liệu' if r[0].startswith('Ô ') else r[5], r[6]) for r in FORM_UI]
   + [
       ('Nhóm đã khóa trong ô Nhóm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Thẻ có biểu tượng ổ khóa trước tên', '- Chỉ hiện với nhóm đang gắn; không chọn mới được']),
       ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Bấm → kiểm, lưu, đóng popup', '- Khóa khi đang lưu']),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Cập nhật thành công.”'),
   ],
   ev=[
       ('Bấm Sửa', 'Click',
        'Before:\n– Không kiểm quyền.\nDuring:\n– Nạp chi tiết; không thuộc công ty / đã xóa → toast ' + CONFLICT +
        ', đóng popup, nạp lại danh sách.\n'
        'After:\n– Điền sẵn 3 ô; ô Nhóm gồm nhóm đang hoạt động + nhóm đang gắn (đã khóa thì kèm ổ khóa).'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm 3 ô bắt buộc trên màn; lỗi → lỗi dưới ô + toast ' + MISS + '.\n'
        '– Máy chủ kiểm hệ số còn thuộc công ty mình; không → ' + CONFLICT + '.\n'
        'During:\n– Kiểm như Thêm mới; trùng tên / nhóm KHÔNG tính chính bản ghi đang sửa.\n'
        '– Tên loại trùng hệ số khác cùng công ty → ' + DUP + '\n– Nhóm đã thuộc loại hệ số khác → ' + TAKEN + '\n' + ERR + '\n'
        'After:\n– Lưu tên, hệ số; xóa hết nhóm cũ rồi gắn lại nhóm mới; cập nhật Người cập nhật, Ngày cập nhật.\n'
        '– Ghi lịch sử “Thay đổi thông tin”: Loại hệ số / Hệ số / Nhóm hàng hóa áp dụng cũ → mới; không đổi gì thì không ghi.\n'
        '– Hiển thị “Cập nhật thành công.”, đóng popup, nạp lại danh sách giữ trang.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– So dữ liệu với lúc mở popup.\n'
        'After:\n– Không đổi (kể cả đổi rồi trả về giá trị cũ) → đóng ngay. Đã đổi → hộp “Thông tin chưa lưu” (Thoát / Ở lại).'),
       ('Bỏ một nhóm bằng nút × trên thẻ', 'Click',
        'Before:\n– Ô Nhóm đang có ít nhất một thẻ.\nAfter:\n– Bỏ nhóm khỏi lựa chọn; bỏ hết → lỗi ' + REQ + ' khi bấm Lưu.'),
   ])

# ------------------------------------------------------------ 2.7 Xóa
fr(7, 'Xóa hệ số', usecase=('FR-07', 'Xóa hệ số', 'action', A_ND),
   rule=('- Quy tắc Xóa, Thông báo.', 'delete'),
   intro=dict(
       ten='Xóa hệ số công nghệ theo nhóm hàng hóa',
       mota='Xóa hẳn một hệ số và toàn bộ liên kết nhóm hàng hóa của nó. Không có điều kiện chặn vì không phiếu nào giữ liên kết tới '
            'hệ số (phiếu chỉ chép số hệ số); sau khi xóa, các nhóm hàng hóa của hệ số được tự do gán cho loại hệ số khác.',
       tacnhan=TN, dieukien=DK + '\n4. Hệ số thuộc công ty của người đăng nhập.',
       chinh='1. Người dùng bấm Xóa (thùng rác đỏ) ở cột Hành động.\n'
             '2. Hệ thống mở hộp “Xác nhận xóa”: “Bạn có chắc muốn xóa bản ghi này không?”.\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm hệ số còn thuộc công ty mình.\n'
             '5. Hệ thống ghi một dòng lịch sử “Xóa” (giữ giá trị trước khi xóa), xóa các nhóm áp dụng rồi xóa hệ số.\n'
             '6. Hệ thống hiển thị “Xóa thành công.”, đóng hộp, nạp lại danh sách và danh sách người lọc.',
       phu='• Bấm Hủy / (x) / click ra ngoài hộp → đóng, không xóa.\n'
           '• Hệ số đã bị người khác xóa (xóa lần 2) hoặc không thuộc công ty mình → toast ' + CONFLICT + ', danh sách nạp lại.\n'
           '• Máy chủ lỗi → toast ' + SYS + '.\n'
           '• Hộp xác nhận không nêu tên bản ghi — người dùng đối chiếu dòng đã bấm.',
       dacbiet='Xóa hẳn, không khôi phục; không có Khóa thay thế. Phiếu đã lập trước đó giữ nguyên số hệ số đã chép.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp Xác nhận xóa',
               note='Hộp Xác nhận xóa được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Xóa trên dòng', 'Icon Button', 'Enable', 'Hiển thị', ['- Thùng rác đỏ, rê chuột: “Xóa”', '- Mọi dòng đều có']),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Hiển thị', '- “Xác nhận xóa”, biểu tượng cảnh báo đỏ.'),
       ('Nội dung', 'Label', 'Hiển thị', 'Hiển thị', '- “Bạn có chắc muốn xóa bản ghi này không?”'),
       ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', '- Nền đỏ; bấm → xóa hẳn hệ số.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Bấm → đóng hộp, không xóa.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống nút Hủy.'),
       ('Vùng ngoài hộp', 'Popup', 'Enable', 'Hiển thị', '- Click ra ngoài → đóng như Hủy.'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', 'Ẩn', '- “Xóa thành công.”'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- ' + CONFLICT + ' khi đã bị xóa / không thuộc công ty', '- ' + SYS]),
       ('Danh sách sau xóa', 'Table/Grid', 'Read-only', 'Theo kết quả',
        ['- Dòng đã xóa biến mất', '- Tổng N giảm 1, giữ trang và bộ lọc đang xem']),
   ],
   ev=[
       ('Bấm Xóa trên dòng', 'Click', 'Before:\n– Không kiểm quyền.\nAfter:\n– Mở hộp “Xác nhận xóa”, ghi nhớ dòng đang chọn.'),
       ('Bấm Xóa trong hộp', 'Click',
        'Before:\n– Máy chủ kiểm hệ số còn tồn tại và thuộc công ty mình; không → ' + CONFLICT + '.\n'
        'During:\n– Không kiểm ràng buộc dữ liệu (không bảng nào giữ liên kết tới hệ số).\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa” (giá trị trước khi xóa).\n– Xóa các nhóm áp dụng và hệ số.\n'
        '– Hiển thị “Xóa thành công.”, đóng hộp, nạp lại danh sách + người lọc.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không gửi máy chủ.\nAfter:\n– Đóng hộp, dữ liệu không đổi.'),
       ('Xóa hệ số đã bị người khác xóa', 'Click',
        'Before:\n– Danh sách đang hiển thị dữ liệu cũ.\nAfter:\n– Toast ' + CONFLICT + ', đóng hộp, nạp lại danh sách.'),
   ])

# ------------------------------------------------------------ 2.8 Xem chi tiết
fr(8, 'Xem chi tiết hệ số',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết hệ số công nghệ theo nhóm hàng hóa',
       mota='Mở popup chỉ đọc hiển thị Loại tỷ lệ hưởng, Hệ số, Nhóm hàng hóa áp dụng của một hệ số, kèm khối Lịch sử thu gọn để '
            'xem các lần tạo / sửa mà không rời danh sách.',
       tacnhan=TN, dieukien=DK + '\n4. Hệ số thuộc công ty của người đăng nhập.',
       chinh='1. Người dùng bấm vào Loại hệ số ở dòng cần xem.\n'
             '2. Hệ thống nạp chi tiết và mở popup “Xem tỷ lệ hưởng công khoán”, mọi ô chỉ đọc.\n'
             '3. Người dùng bấm Xem lịch sử để mở khối Lịch sử (mục 2.9).\n'
             '4. Người dùng bấm Đóng; danh sách giữ nguyên trang và bộ lọc.',
       phu='• Hệ số đã bị xóa / không thuộc công ty mình → toast ' + CONFLICT + ', popup tự đóng, danh sách nạp lại.\n'
           '• Nhóm đã bị khóa ở danh mục nhóm hàng hóa → hiện kèm biểu tượng ổ khóa.\n'
           '• Đóng bằng Đóng / (x) / click ra ngoài → không hỏi (không có dữ liệu sửa).',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Popup Xem tỷ lệ hưởng công khoán',
               note='Popup Xem được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('17b_detail_history'), 'Popup Xem với khối Lịch sử đã mở')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Xem tỷ lệ hưởng công khoán”.'),
       ('Ô Loại tỷ lệ hưởng', 'Textbox', 'Read-only', '1–255 ký tự', 'Theo dữ liệu', '- Nền xám, không sửa được.'),
       ('Ô Hệ số', 'Textbox', 'Read-only', '0 – 999,999.99', 'Theo dữ liệu',
        ['- Hiện số đã lưu, không ép 2 số lẻ (vd 1.5)', '- Không sửa được']),
       ('Ô Nhóm hàng hóa áp dụng', 'Dropdown', 'Read-only', 'Danh sách', 'Theo dữ liệu',
        ['- Các thẻ nhóm, không có nút ×', '- Nhóm đã khóa kèm biểu tượng ổ khóa']),
       ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
        ['- Tiêu đề “Lịch sử” + số mốc', '- Nút Xem lịch sử / Thu gọn; khi mở có nút Làm mới', '- Nội dung như mục 2.9']),
       ('Nút Xem lịch sử', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở khối, nạp lịch sử lần đầu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → đóng popup. Không có nút Lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Vùng ngoài popup', 'Popup', 'Enable', '–', 'Hiển thị', '- Click ra ngoài → đóng.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- ' + CONFLICT + ' khi hệ số không còn.'),
       ('Danh sách phía sau', 'Table/Grid', 'Read-only', '–', 'Giữ nguyên', '- Đóng popup → giữ trang, bộ lọc, sắp xếp.'),
   ],
   ev=[
       ('Bấm Loại hệ số', 'Click',
        'Before:\n– Hệ số thuộc công ty mình.\nDuring:\n– Nạp chi tiết; lỗi → toast ' + CONFLICT + ', đóng popup.\n'
        'After:\n– Hiển thị popup chỉ đọc, khối Lịch sử thu gọn.'),
       ('Bấm Xem lịch sử', 'Click',
        'Before:\n– Khối đang thu gọn.\nDuring:\n– Nạp lịch sử lần đầu.\nAfter:\n– Mở danh sách mốc, mới nhất trên.'),
       ('Bấm Làm mới (khối Lịch sử)', 'Click', 'Before:\n– Khối đang mở.\nAfter:\n– Nạp lại các mốc lịch sử.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng popup; danh sách giữ nguyên trang, bộ lọc.'),
   ])

# ------------------------------------------------------------ 2.9 Lịch sử
fr(9, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của hệ số',
       mota='Hiển thị các mốc thao tác trên một hệ số: Tạo mới, Thay đổi thông tin (Loại hệ số, Hệ số, Nhóm hàng hóa áp dụng — '
            'trước → sau), kèm người thực hiện, phòng ban, thời điểm; lọc được theo loại hành động, người thực hiện, khoảng ngày.',
       tacnhan=TN, dieukien='1. Người dùng đăng nhập thành công.\n2. Hệ số thuộc công ty của người đăng nhập.',
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc Xem lịch sử trong popup Xem).\n'
             '2. Hệ thống nạp các mốc lịch sử của hệ số.\n'
             '3. Hệ thống hiển thị cửa sổ “Lịch sử thay đổi: <Loại hệ số>”, mốc mới nhất ở trên.\n'
             '4. Người dùng bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.\n'
             '5. Người dùng bấm Đóng để về danh sách.',
       phu='• Chưa có mốc nào (hệ số tạo trước khi có ghi lịch sử) → “Chưa có lịch sử thao tác nào.”.\n'
           '• Lọc không ra mốc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Lỗi nạp → dòng lỗi đỏ + nút Thử lại.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Xem / xuất không ghi lịch sử; Lưu không đổi gì không ghi “Thay đổi thông tin”. Mốc “Xóa” được ghi nhưng không xem '
               'được trên màn vì bản ghi đã mất.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16b_history_filter'), 'Cửa sổ Lịch sử thay đổi đang mở Bộ lọc')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Lịch sử thay đổi: <Loại hệ số>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, hành động (Tạo mới xanh lá / Thay đổi thông tin xanh dương)',
           '- “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi thông tin: Hệ số cũ → mới; Nhóm hàng hóa áp dụng dạng khối Trước / Sau, mỗi nhóm một dòng',
           '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống',
        ['- Nhân viên cùng công ty người tạo, dạng “Tên - Mã phòng - Mã NV”', '- Chọn là lọc ngay']),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc đến hết ngày này.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', '- Xóa điều kiện lọc lịch sử.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- “Chưa có lịch sử thao tác nào.”', '- “Không có lịch sử phù hợp bộ lọc.”']),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Giống nút Đóng.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click',
        'Before:\n– Hệ số thuộc công ty mình.\n'
        'During:\n– Nạp các mốc + danh mục ô lọc; chưa có → “Chưa có lịch sử thao tác nào.”.\nAfter:\n– Hiển thị, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm.\nAfter:\n– Lọc lại danh sách mốc; không khớp → “Không có lịch sử phù hợp bộ lọc.”.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Có điều kiện lọc.\nAfter:\n– Xóa điều kiện, hiện lại đủ mốc.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng; danh sách giữ nguyên trang, bộ lọc.'),
   ])

# ------------------------------------------------------------ 2.10 Xuất Excel
fr(10, 'Xuất Excel danh sách', usecase=('FR-10', 'Xuất Excel', 'io', A_ND),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất Excel danh sách hệ số',
       mota='Xuất danh sách hệ số theo bộ lọc đang áp (trong phạm vi công ty mình) ra file Excel; người dùng chọn trường và thứ tự '
            'cột. File dựng theo khuôn chung các màn danh sách: letterhead công ty, tiêu đề, bảng, khối ký.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn danh sách.',
       chinh='1. Người dùng lọc danh sách theo nhu cầu rồi bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất file” liệt kê 7 trường, tích sẵn các trường đang hiện trên bảng (mặc định đủ 7).\n'
             '3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống tải lần lượt MỌI hệ số khớp bộ lọc (không theo trang đang xem), hiện tiến độ “Đã tải x/y dòng…”, '
             '“Đang dựng file x/y dòng…”.\n'
             '5. Hệ thống tạo file he-so-cong-nghe-theo-nhom-hang-hoa.xlsx (trang “He so cong nghe”): letterhead công ty người xuất, '
             'tiêu đề “HỆ SỐ CÔNG NGHỆ THEO NHÓM HÀNG HÓA”, cột STT + các trường đã chọn đúng thứ tự, khối ký “Ngày ..., tháng ..., '
             'năm ...” / “Người lập”.\n'
             '6. Hệ thống tải file về và hiển thị “Xuất Excel thành công.”.',
       phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Danh sách theo bộ lọc rỗng → thông báo “Không có dữ liệu để xuất”, KHÔNG tạo file.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ chọn trường → không xuất.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”.',
       dacbiet='Hệ số là ô SỐ (định dạng 2 số lẻ); Nhóm hàng hóa mỗi nhóm một dòng trong ô; ngày dạng dd/mm/yyyy hh:mm. Hàng tiêu đề '
               'không gắn nút lọc (Redmine #11705). Xuất không giới hạn số dòng, không ghi lịch sử.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất file”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 7 trường', '–', 'Theo cột đang hiện',
        ['- Loại hệ số, Hệ số, Nhóm hàng hóa, Người tạo', '- Ngày tạo, Người cập nhật, Ngày cập nhật',
         '- Cột STT luôn có trong file (không nằm trong danh sách)']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích',
        ['- Mặc định tích các trường đang hiện trên bảng (cấu hình mặc định: cả 7)', '- Bỏ tích → trường không có trong file']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích cả 7 trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/7 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → tải file danh sách']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, không xuất.'),
       ('Dòng tiến độ', 'Label', 'Read-only', '–', '–', 'Ẩn',
        ['- Cạnh nút Xuất Excel: “Đang chuẩn bị dữ liệu…”, “Đã tải x/y dòng…”, “Đang dựng file x/y dòng…”']),
       ('File Excel', 'Table/Grid', 'Read-only', '.xlsx', '–', '–',
        ['- Tên he-so-cong-nghe-theo-nhom-hang-hoa.xlsx', '- Letterhead công ty người xuất trải bằng bề rộng bảng',
         '- Tiêu đề, STT + trường đã chọn đúng thứ tự, khối ký']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Xuất Excel thành công.”', '- “Không có dữ liệu để xuất”', '- “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không cần quyền riêng; lấy bộ lọc + sắp xếp đang áp.\nAfter:\n– Mở cửa sổ chọn trường, tích sẵn các cột đang hiện.'),
       ('Tích / bỏ tích, kéo thả trường', 'Change',
        'Before:\n– Trong cửa sổ chọn trường.\nAfter:\n– Cập nhật “Đang chọn n/7 trường”; 0 trường → khóa Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; khóa nút Xuất Excel trong lúc xuất.\n'
        'During:\n– Tải tuần tự mọi trang dữ liệu khớp bộ lọc của công ty mình; 0 dòng → “Không có dữ liệu để xuất”, dừng.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.\n'
        'After:\n– Dựng file, tải về, hiển thị “Xuất Excel thành công.”; không ghi lịch sử.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Hệ số công nghệ theo nhóm hàng hóa; không lặp lại các quy tắc đã có trong '
           'SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi theo công ty, không gắn quyền', [
        '– Mọi thao tác chỉ trên hệ số có công ty = công ty người đăng nhập (kể cả Super admin); không có công ty → tập rỗng.',
        '– Không có quyền riêng: ai đăng nhập cũng vào màn và thao tác được (giữ như hệ thống cũ).',
        '– Ô lọc Công ty chỉ lọc thêm trên phạm vi đó; hệ số công ty khác mở / sửa / xóa → báo trạng thái đã thay đổi.'],
     ['Xem danh sách', 'Chỉnh sửa', 'Xóa', 'Xem chi tiết', 'Xuất Excel']),
    ('BR-02', 'Tính duy nhất của Loại tỷ lệ hưởng', [
        '– Không trùng trong cùng công ty; so sánh không phân biệt hoa / thường, dấu (theo cách so sánh chữ của cơ sở dữ liệu).',
        '– Công ty khác được trùng tên. Sửa không tính trùng với chính bản ghi.', '– Trùng → “Loại tỷ lệ hưởng đã tồn tại.”'],
     ['Thêm mới', 'Chỉnh sửa']),
    ('BR-03', 'Mỗi nhóm hàng hóa thuộc một loại hệ số', [
        '– Một nhóm chỉ gắn với tối đa một hệ số, kiểm TOÀN hệ thống (không theo công ty) như hệ thống cũ, vì hệ số được tra theo '
        'nhóm hàng.', '– Vướng → “<Tên các nhóm> đã thuộc loại hệ số khác.”', '– Sửa không tính chính bản ghi.'],
     ['Thêm mới', 'Chỉnh sửa']),
    ('BR-04', 'Dữ liệu bắt buộc và định dạng', [
        '– Loại tỷ lệ hưởng 1–255 ký tự; Hệ số số không âm, tối đa 2 số lẻ, ≤ 999,999.99; ít nhất 1 nhóm hàng hóa.',
        '– Màn kiểm đủ 3 ô cùng lúc trước khi gửi, máy chủ kiểm lại.'], ['Thêm mới', 'Chỉnh sửa']),
    ('BR-05', 'Chuẩn hóa dữ liệu nhập', [
        '– Bỏ khoảng trắng đầu / cuối của Loại tỷ lệ hưởng; dấu phẩy trong Hệ số bị bỏ trước khi kiểm.',
        '– Công ty / phòng ban / bộ phận, người tạo lấy từ người đăng nhập; Người cập nhật / Ngày cập nhật đổi theo lần lưu gần '
        'nhất (kể cả khi chỉ đổi nhóm).', '– Nhóm trùng trong lựa chọn được gộp.'], ['Thêm mới', 'Chỉnh sửa']),
    ('BR-06', 'Điều kiện xóa', [
        '– Xóa hẳn hệ số + liên kết nhóm, không điều kiện: không phiếu nào giữ liên kết tới hệ số (chỉ chép số).',
        '– Không có Khóa / Mở khóa (màn không có trạng thái).'], ['Xóa']),
    ('BR-07', 'Liên kết cha – con', [
        '– Hệ số > các nhóm hàng hóa áp dụng; lưu sửa thì xóa hết nhóm cũ rồi gắn lại nhóm mới.',
        '– Nhóm hàng hóa đã khóa ở danh mục: không chọn mới được; nhóm đang gắn vẫn hiện kèm ổ khóa và giữ nguyên.'],
     ['Thêm mới', 'Chỉnh sửa', 'Xem chi tiết']),
    ('BR-08', 'Sử dụng ở màn khác', [
        '– Duyệt kết quả lắp đặt (Phiếu nhập kết quả): dòng lắp đặt chưa có hệ số → lấy hệ số theo nhóm hàng hóa của hàng; nhóm '
        'chưa có hệ số → 1. Kết quả công khoán = công khoán duyệt × hệ số.',
        '– Phiếu đã lưu giữ nguyên số hệ số đã chép; sửa / xóa hệ số chỉ ảnh hưởng lần lập / duyệt sau.'],
     ['Chỉnh sửa', 'Xóa']),
    ('BR-09', 'Quy tắc ghi lịch sử', [
        '– Ghi: Tạo mới; Thay đổi thông tin (Loại hệ số, Hệ số, Nhóm hàng hóa áp dụng — cũ → mới; không đổi thì không ghi); Xóa.',
        '– Xem / xuất không ghi; hiển thị mới nhất ở trên.'], ['Thêm mới', 'Chỉnh sửa', 'Xóa', 'Lịch sử']),
    ('BR-10', 'Xuất Excel', [
        '– Xuất mọi hệ số khớp bộ lọc của công ty mình, không giới hạn; rỗng → không tạo file.',
        '– Letterhead theo công ty người xuất; không gắn nút lọc ở hàng tiêu đề.'], ['Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Hệ số công nghệ theo nhóm hàng hóa (hệ số theo nhóm hàng hóa).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'CSKH sau bán', 'Phiếu nhập kết quả (form Duyệt kết quả: dòng lắp đặt chưa có hệ số thì lấy hệ số theo nhóm hàng hóa của '
                          'hàng, không có lấy 1; chép số vào phiếu duyệt, kết quả công khoán = công khoán duyệt × hệ số)',
     'CSKH sau bán -> Giao việc'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
