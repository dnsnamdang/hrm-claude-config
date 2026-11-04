# -*- coding: utf-8 -*-
"""SRS màn "Phiếu kế toán" (mã <mã công ty>.PKT<mmyy>.<5 số>) — form chuẩn Danh mục quốc gia (04/11/2026).

Chạy: python gen_srs.py  → SRS - Phiếu kế toán.docx
Khung: srs-documenter (SrsDoc) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc: ../buy-service-accounting/gen_srs.py và
  ../finance-addition-accounting-request/gen_srs.py (Mục lục sang trang riêng, Phần 5 bảng 4 cột theo khuôn Drive — chuẩn user chốt 04/11).
Nguồn đọc 04/11/2026 (nhánh develop, cả 2 repo):
  BE  Modules/Finance/{Entities/BillAdjustDept/BillAdjustDept.php (searchByFilter, canView, canEdit, SORTABLE_COLUMNS, STATUSES),
      Services/BillAdjustDept{Write,Source,Notify,History,Picker,OddBalance,Print}Service.php,
      Http/Controllers/V1/BillAdjustDeptController.php, Http/Requests/BillAdjustDept/BillAdjustDeptStoreRequest.php, Routes/api.php},
      app/Services/CatalogHistoryService.php, PermissionsTableSeeder (Kế toán thanh toán; Xem tất cả phiếu kế toán của tổng công ty / công ty).
  FE  pages/finance/bill-adjust-depts/** (index, create, _id/index, _id/edit, components/{BillAdjustDeptForm, AccountingDetailTable,
      BillAdjustDeptRequestPickerModal, ObjectSearchModal, ContractPickerModal, ExportRequestSearchModal}),
      addition-accounting-requests/components/AttachmentSection.vue, components/subsystem-menu/finance.js (nhóm Sổ tổng hợp).
  Plan/spec: .plans/gop-db/finance-bill-adjust-dept/{design,plan}.md, docs/superpowers/specs/gop-db/2026-08-28-finance-bill-adjust-dept-design.md
      (hành vi hiện hành = SAU các fix 30/09 → 15/10, Redmine #11306, #11307, #11608, #11660) — code thắng khi lệch.
Ảnh: ./pkt_shots (dev-hrm 04/11/2026, DNS Admin, script pkt_shots/_capture/capture.js; mọi yêu cầu ghi bị chặn ở trình duyệt).
  Dev có sẵn phiếu Đang tạo TPE.PKT1126.00001 của DNS Admin → nút Sửa / Xóa / màn Sửa / hộp Xác nhận xóa là ảnh thật.
  Ảnh lỗi đỏ: gọi hàm kiểm tra của form trên trình duyệt (không gửi máy chủ). Popup Chọn phiếu yêu cầu xuất hàng: mở thẳng trên trình
  duyệt (dev không có dòng hợp đồng loại 3).
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

TEN = 'Phiếu kế toán'
SHOTS = os.path.join(HERE, 'pkt_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


# Nhóm menu cấp 2 trùng chữ với mục cấp 1 ("Sổ tổng hợp"): thêm ký tự rộng 0 vào chặng thứ 2 để gắn đúng icon nhóm.
NHOM = 'Sổ tổng hợp​'
MENU = 'Phân hệ Tài chính => Sổ tổng hợp => %s => Phiếu kế toán' % NHOM
MENU_YC = ('Phân hệ Tài chính => Khởi tạo => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi => '
           'Phiếu yêu cầu điều chỉnh công nợ')
MENU_HT = ('Phân hệ Tài chính => Khởi tạo => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi => '
           'Phiếu yêu cầu hạch toán bổ sung')
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu kế toán.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_KT = 'Kế toán thanh toán'
A_XEM = 'Người xem phiếu'
Q1 = 'Kế toán thanh toán'
V1 = 'Xem tất cả phiếu kế toán của tổng công ty'
V2 = 'Xem tất cả phiếu kế toán của công ty'
TN_KT = ('Người dùng có quyền thực hiện chức năng: Kế toán thanh toán (tài khoản Super admin cũng phải được gán quyền này mới thấy '
         'nút Tạo mới, Lưu và duyệt và lưu được phiếu).')
TN_XEM = ('Người dùng có quyền thực hiện chức năng: người tạo phiếu (phiếu của mình); người có quyền Xem tất cả phiếu kế toán của tổng '
          'công ty hoặc Xem tất cả phiếu kế toán của công ty (theo phạm vi ở Phần 2); tài khoản Super admin xem mọi phiếu.')
TN_SUA = ('Người dùng có quyền thực hiện chức năng: Kế toán thanh toán, đồng thời là chính người tạo phiếu (người khác kể cả Super '
          'admin không sửa / xóa được).')
DK_XEM = ('1. Người dùng đăng nhập thành công.\n'
          '2. Người dùng có quyền xem phiếu theo phạm vi ở Phần 2 (không có quyền nào thì chỉ thấy phiếu mình tạo).\n'
          '3. Người dùng đang ở màn danh sách Phiếu kế toán.')
DK_SUA = ('1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán thanh toán và là người tạo phiếu.\n'
          '3. Phiếu đang ở trạng thái Đang tạo (lưu nháp, chưa ghi sổ cái).')
DK_TAO = ('1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán thanh toán.\n'
          '3. Người dùng đang ở màn danh sách Phiếu kế toán, hoặc ở màn phiếu nguồn (Phiếu yêu cầu điều chỉnh công nợ Chờ tạo phiếu '
          'kế toán, Phiếu yêu cầu hạch toán bổ sung Chờ duyệt, Danh sách cần hạch toán chi phí vận chuyển nhanh).')

M_REQ = '“Bắt buộc phải nhập”'
M_RATE = '“Tỷ giá (VND) – Phải lớn hơn 0”'
M_MONEY = '“Bắt buộc nhập phát sinh nợ hoặc phát sinh có”'
M_NOROW = '“Định khoản – Phải có ít nhất một dòng”'
M_NOPERM = '“Bạn không có quyền thực hiện chức năng này”'
M_CONFLICT = ('“Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển trạng thái bởi người dùng khác. Vui lòng tải lại '
              'trang để cập nhật thông tin mới nhất.”')
TOAST_422 = '“Bạn chưa nhập đầy đủ thông tin.”'
DEL_MSG = "“Bạn có chắc muốn xóa phiếu kế toán '<mã phiếu>'?”"
APPROVE_TITLE = '“Xác nhận duyệt phiếu kế toán”'
APPROVE_MSG = '“Duyệt phiếu sẽ GHI BÚT TOÁN VÀO SỔ CÁI và không thể hoàn tác. Bạn có chắc chắn muốn duyệt?”'
GROUP_RULES = ['“Bắt buộc nhập phát sinh nợ hoặc phát sinh có”',
               '“Nhóm định khoản <N> đang bị trùng số tài khoản, khách hàng và hợp đồng”',
               '“Tổng số phát sinh nợ và phát sinh có trong một nhóm không bằng nhau”',
               '“Có nhiều phát sinh có và phát sinh nợ trong một nhóm định khoản”',
               '“Tổng số tiền điều chỉnh vượt quá số tiền của báo có!”',
               '“Số tiền phát sinh có vượt quá số dư nợ đầu kì của hợp đồng”',
               '“Số tiền phát sinh nợ vượt quá số dư có đầu kì của hợp đồng”']
UNSAVED = ['- Tiêu đề “Thông tin chưa lưu”', '- Nội dung “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”',
           '- Nút Thoát: bỏ thay đổi, rời màn', '- Nút Ở lại: đóng hộp, giữ nguyên dữ liệu đang nhập']
STATUS_LIST = ['- Đang tạo: nhãn xám (phiếu lưu nháp, chưa ghi sổ)', '- Đã duyệt: nhãn xanh (đã ghi sổ cái)']

d = SrsDoc(out=OUT, menu=MENU, route='/finance/bill-adjust-depts', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Sổ tổng hợp': 'menu_sotonghop', NHOM: 'menu_nhom_sotonghop', 'Phiếu kế toán': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Lưu và duyệt': 'btn_luuduyet',
    'In': 'btn_in_row', 'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row',
    'Tạo phiếu kế toán': 'btn_taopkt_ycdc', 'Lập phiếu kế toán': 'btn_lappkt_htbs',
}.items() if os.path.exists(os.path.join(ICONS, v + '.png'))})

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
        if os.path.exists(shot(png)):
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
d.doc.add_page_break()  # Mục lục sang trang riêng như bản Drive đã chuẩn hoá
d.h2('Mục lục')
d.doc.paragraphs[-1].alignment = 1  # căn giữa chữ 'Mục lục'
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu kế toán (mã phiếu dạng <mã công ty>.PKT<tháng><năm 2 số>.<5 chữ số>, vd '
    'TPE.PKT1126.00001), chứng từ ghi bút toán vào sổ cái — mắt xích cuối của 2 luồng Phiếu yêu cầu điều chỉnh công nợ và Phiếu yêu '
    'cầu hạch toán bổ sung, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ 5 cửa vào lập phiếu (nhập tay, từ Phiếu yêu cầu điều chỉnh công nợ, từ Phiếu yêu cầu hạch toán bổ sung, từ phiếu hạch toán '
    'hoa hồng tháng, từ Danh sách cần hạch toán chi phí vận chuyển nhanh) và dữ liệu mỗi cửa điền sẵn.',
    'Làm rõ thao tác Lưu và duyệt: kiểm tra cân đối từng nhóm định khoản, đề xuất điều chỉnh số dư lẻ, ghi bút toán Nợ / Có vào sổ '
    'cái và cập nhật ngược trạng thái phiếu nguồn.',
])
d.p('Phạm vi chức năng (14 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Danh sách: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột.',
    'Phiếu của kế toán: Lập phiếu (Lưu nháp / Lưu và tiếp tục), Chọn phiếu yêu cầu điều chỉnh công nợ, Chọn đối tượng – hợp đồng – '
    'phiếu yêu cầu xuất hàng cho dòng định khoản, Chỉnh sửa, Xóa, Lưu và duyệt (ghi sổ cái, kèm điều chỉnh số dư lẻ).',
    'Xem: Xem chi tiết, In phiếu, Xuất Excel (danh sách và một phiếu), Xem lịch sử thay đổi.',
    'Không thuộc màn này: không có Duyệt / Không duyệt riêng (Lưu và duyệt chính là duyệt; trả phiếu về làm ở màn phiếu nguồn), không '
    'có Hủy, không có Khóa / Mở khóa, không có Import Excel.',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phiếu là chứng từ kế toán định khoản Nợ / Có theo nhóm định khoản cho khách hàng, nhà cung cấp, nhân viên, phòng ban và hợp đồng.',
    'Khi Lưu và duyệt, mỗi dòng có phát sinh sinh 1 bút toán trong sổ cái dùng chung với hệ thống ERP (kèm tài khoản đối ứng) — dữ liệu '
    'dùng cho báo cáo Đối chiếu công nợ 1 KH, Chi tiết công nợ KH và sổ chi tiết tài khoản.',
    'Trạng thái phiếu nguồn (Phiếu yêu cầu điều chỉnh công nợ, Phiếu yêu cầu hạch toán bổ sung, dòng chi phí vận chuyển nhanh) đi theo '
    'phiếu kế toán; số tiền đã điều chỉnh được cộng vào dòng Phiếu báo có.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Lưu nháp chỉ bắt buộc Ngày hạch toán; Lưu và duyệt bắt buộc Loại tiền, Tỷ giá (ngoại tệ > 0), Diễn giải, ≥ 1 dòng định khoản, '
    'Số tài khoản và Diễn giải từng dòng, mỗi dòng có Nợ hoặc Có, từng nhóm định khoản cân Nợ = Có.',
    'Chỉ người tạo (có quyền Kế toán thanh toán) được Sửa / Xóa và chỉ khi phiếu Đang tạo; phiếu Đã duyệt đã ghi sổ — không sửa, không '
    'xóa, không đảo trạng thái.',
    'Phiếu Đang tạo của người khác luôn bị ẩn với mọi cấp quyền xem. Một Phiếu yêu cầu hạch toán bổ sung chỉ có 1 phiếu kế toán còn '
    'hiệu lực; một Phiếu yêu cầu điều chỉnh công nợ chỉ chọn được khi đang Chờ tạo phiếu kế toán.',
    'Ghi sổ, cập nhật phiếu nguồn và lịch sử chạy trọn trong 1 lần xử lý: lỗi ở bất kỳ bước nào thì không ghi gì.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu kế toán', 'Chứng từ ghi bút toán vào sổ cái; mã phiếu do hệ thống sinh khi lưu lần đầu dạng <mã công ty>.PKT<mmyy>.<5 số> '
                      '(vd TPE.PKT1126.00001), duy nhất, không sửa được.'),
    ('Phiếu nguồn', 'Chứng từ mà phiếu kế toán được lập từ đó: Phiếu yêu cầu điều chỉnh công nợ (YCĐC), Phiếu yêu cầu hạch toán bổ sung, '
                    'Phiếu yêu cầu hạch toán hoa hồng tháng, các dòng chi phí vận chuyển nhanh. Phiếu nhập tay không có phiếu nguồn.'),
    ('Dòng định khoản', 'Một dòng của bảng Chi tiết: Số tài khoản, đối tượng (Mã / Tên khách), Phát sinh nợ hoặc Phát sinh có, Diễn giải, '
                        'Đơn hàng/Hợp đồng, Số phiếu yc xuất hàng, NVKD, Mã phí, Mã vụ việc, Ngân hàng, STK ngân hàng, Nhóm định khoản.'),
    ('Nhóm định khoản', 'Số nguyên ≥ 1 gom các dòng thành 1 bút toán kép; trong 1 nhóm Tổng Nợ = Tổng Có, không vừa nhiều dòng Nợ vừa '
                        'nhiều dòng Có.'),
    ('Đối tượng', 'Khách hàng, Nhà cung cấp hoặc Nhân viên gắn vào dòng định khoản (chọn ở cửa sổ Chọn đối tượng).'),
    ('Phát sinh nợ / Phát sinh có', 'Số tiền ghi Nợ / ghi Có của dòng theo nguyên tệ; nhập bên này thì bên kia tự về 0. Phiếu ngoại tệ có '
                                    'thêm cột quy đổi VNĐ = nguyên tệ × Tỷ giá.'),
    ('Tổng phát sinh', 'Tổng số tiền quy đổi VNĐ của phiếu (cột Tổng phát sinh ở danh sách).'),
    ('Số dư nợ đầu kì', 'Ô tích trên dòng gắn hợp đồng loại 3, đánh dấu dòng điều chỉnh vào số dư đầu kì của hợp đồng.'),
    ('Số dư lẻ', 'Phần dư Nợ / Có còn lại của hợp đồng trên tài khoản 1311 sau phiếu, nhỏ hơn ngưỡng cấu hình của công ty; Lưu và duyệt '
                 'đề xuất cặp bút toán Nợ 811 / Có 1311 (dư nợ) hoặc Nợ 1311 / Có 711 (dư có) để đưa về 0.'),
    ('Ghi sổ cái', 'Lưu và duyệt: mỗi dòng có phát sinh sinh 1 bút toán (kèm tài khoản đối ứng) trong sổ cái dùng chung với ERP.'),
    ('Trạng thái Đang tạo', 'Phiếu lưu nháp, chưa ghi sổ; người tạo sửa / xóa / duyệt được. Nhãn xám.'),
    ('Trạng thái Đã duyệt', 'Phiếu đã ghi sổ cái — trạng thái cuối, không sửa / xóa. Nhãn xanh.'),
    ('Cấu trúc phân cấp', 'Phiếu > nhóm định khoản > dòng định khoản > đối tượng > hợp đồng của đúng đối tượng > phiếu yêu cầu xuất hàng '
                          'của đúng hợp đồng; phiếu > file đính kèm; phiếu Đã duyệt > bút toán sổ cái.'),
    ('YCĐC / YCXH / NVKD / TK / STK', 'Yêu cầu điều chỉnh công nợ / Yêu cầu xuất hàng / Nhân viên kinh doanh (người lập hợp đồng) / '
                                      'Tài khoản / Số tài khoản.'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn dùng 3 quyền: quyền thao tác “Kế toán thanh toán” (nhóm quyền Đề nghị thu tiền, dùng chung các màn Tài chính) và 2 quyền '
    'xem theo cấp (nhóm quyền Phiếu kế toán).')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, 'Hiện nút Tạo mới và nút Lưu và duyệt; lưu nháp, sửa, xóa phiếu, tải / xóa file đính kèm, mở cửa sổ Chọn phiếu yêu cầu '
               'điều chỉnh công nợ (sửa / xóa thêm điều kiện người tạo + Đang tạo). Cũng là quyền hiện nút Tạo phiếu kế toán / Lập phiếu '
               'kế toán ở 2 màn phiếu nguồn.'),
], widths=[0.8, 1.6, 3.6])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét từ trên xuống, có cấp nào áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Toàn bộ phiếu; có ô lọc Công ty. Tài khoản Super admin xem như V1.'),
    ('V2', V2, 'Phiếu thuộc công ty của người dùng; có ô lọc Phòng ban.'),
    ('—', '(không có quyền nào)', 'Phiếu mình tạo (và phiếu mình duyệt khi mở chi tiết).'),
], widths=[0.8, 2.4, 2.8])
d.p('Mọi cấp: phiếu Đang tạo của người khác bị ẩn. Q1 không mở rộng phạm vi xem. Màn chỉ có 2 cấp (không có cấp phòng ban / bộ phận).')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người tạo (Q1)', 'Q1 (không phải người tạo)', 'V1–V2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅ (theo V)', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu', '✅', '✅', '❌', '❌'),
    ('FR-06 Chọn phiếu yêu cầu điều chỉnh công nợ', '✅', '✅', '❌', '❌'),
    ('FR-07 Chọn đối tượng, hợp đồng, phiếu YCXH', '✅', '✅', '❌', '❌'),
    ('FR-08 Chỉnh sửa', '✅ (Đang tạo)', '❌', '❌', '❌'),
    ('FR-09 Xóa', '✅ (Đang tạo)', '❌', '❌', '❌'),
    ('FR-10 Xem chi tiết', '✅', '✅ (trong phạm vi V)', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-11 Lưu và duyệt (ghi sổ cái)', '✅ (Đang tạo)', '✅ (phiếu mới lập)', '❌', '❌'),
    ('FR-12 In phiếu', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-13 Xuất Excel', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-14 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[2.0, 1.2, 1.3, 0.9, 1.1])
d.p('Màn không có Khóa / Mở khóa, Import Excel, Không duyệt và Hủy nên ma trận không có cột quyền tương ứng. In, Xuất Excel, Xem lịch '
    'sử không gắn quyền riêng: ai xem được phiếu thì dùng được.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có Q1: không thấy nút Tạo mới, nút Lưu và duyệt; mở thẳng màn Tạo vẫn vào được nhưng bấm Lưu nháp bị máy chủ từ chối ' +
    M_NOPERM + '; cửa sổ Chọn phiếu yêu cầu điều chỉnh công nợ không có dữ liệu.',
    'Không có quyền xem nào: chỉ thấy phiếu do mình tạo; ô lọc Công ty, Phòng ban bị khóa.',
    'Nút không đủ điều kiện thì ẩn hẳn, không hiện xám (cờ Sửa / Xóa do máy chủ trả theo từng phiếu).',
    'Mở thẳng đường dẫn màn chi tiết / sửa của phiếu ngoài phạm vi → máy chủ từ chối “Bạn không có quyền xem phiếu này”, màn báo “Không '
    'tải được phiếu”.',
    'Gọi thẳng chức năng bỏ qua giao diện → máy chủ từ chối: “Bạn không có quyền sửa phiếu này”, “Bạn không có quyền xóa phiếu này”, ' +
    M_NOPERM + ' (thiếu Q1); duyệt phiếu đã duyệt → ' + M_CONFLICT + '.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Nút / thao tác', 'Hiện khi', 'Vị trí'], [
    ('Tạo mới', 'Người dùng có Q1', 'Thanh công cụ của bảng'),
    ('Xuất Excel, Cấu hình cột', 'Luôn hiện', 'Thanh công cụ của bảng'),
    ('Sửa, Xóa', 'Người đăng nhập là người tạo và phiếu Đang tạo', 'Cột Hành động, chân màn chi tiết'),
    ('In, Xuất Excel (1 phiếu), Lịch sử', 'Luôn hiện với phiếu xem được', 'Cột Hành động (vào nút “…” khi dòng có hơn 3 nút); màn chi tiết'),
    ('Lưu nháp', 'Màn Tạo, màn Sửa', 'Chân màn'),
    ('Lưu và duyệt', 'Màn Tạo, màn Sửa; người có Q1', 'Chân màn'),
    ('Lưu và tiếp tục', 'Chỉ màn Tạo', 'Chân màn'),
    ('Thêm dòng, nút xóa dòng', 'Phiếu không lập từ Phiếu YCĐC và không lập từ chi phí vận chuyển nhanh', 'Đầu khối Chi tiết, cuối dòng'),
], widths=[1.6, 3.0, 1.8])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_KT, [0, 1, 2, 3, 4, 5, 6]), (A_XEM, [0, 5, 6])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu kế toán', 'crud'),
     ('FR-08', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-09', 'Xóa phiếu', 'action'),
     ('FR-11', 'Lưu và duyệt', 'action'),
     ('FR-12', 'In phiếu', 'io'),
     ('FR-13', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-10', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-14', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn phiếu YCĐC', 'crud', 'extend', [1, 2], None),
     ('FR-07', 'Chọn đối tượng, hợp đồng', 'crud', 'extend', [1, 2], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu kế toán')

d.h2('2 Đặc tả chi tiết từng chức năng')


# ------------------------------------------------------------ Form Tạo / Sửa (dùng chung 2.5 + 2.8)
def form_ui(edit):
    """Bảng giao diện màn Tạo (edit=False) / Sửa (edit=True) — 8 cột, mỗi đối tượng 1 hàng."""
    rows = [
        ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–',
         '“Sửa phiếu kế toán: <mã phiếu>”' if edit else '“Tạo phiếu kế toán”',
         ['- Cũng là tiêu đề tab trình duyệt',
          '- Ghép mã phiếu sau khi nạp xong phiếu' if edit else '- Không có ô Mã phiếu: mã sinh khi lưu lần đầu',
          '- Không hiện nhãn trạng thái (giống ERP)']),
        ('Dòng người tạo', 'Label', 'Read-only', '–', '–',
         'Người tạo – ngày giờ tạo' if edit else 'Người đăng nhập – thời điểm hiện tại',
         ['- Góc phải tiêu đề khối Thông tin chung, dạng “<họ tên> - dd/mm/yyyy hh:mm”', '- Không sửa được']),
        ('Ô Phiếu yêu cầu điều chỉnh công nợ', 'Textbox', 'Enable / Ẩn', 'Phiếu Chờ tạo phiếu kế toán', 'Không', 'Trống',
         ['- Hiện khi phiếu không lập từ 3 nguồn còn lại (hạch toán bổ sung, hoa hồng tháng, vận chuyển nhanh)',
          '- Gợi ý “Chọn phiếu yêu cầu điều chỉnh công nợ”',
          '- Bấm ô → mở cửa sổ Chọn phiếu yêu cầu điều chỉnh công nợ (mục 2.6)',
          '- Nút × bỏ chọn: xóa mã phiếu, Loại tiền về VNĐ, Tỷ giá về 1, xóa toàn bộ dòng định khoản' +
          ('' if edit else ' và file thừa hưởng')]),
        ('Ô Phiếu yêu cầu hạch toán bổ sung', 'Textbox', 'Read-only', '–', '–', 'Theo phiếu nguồn',
         ['- Chỉ hiện khi phiếu lập từ Phiếu yêu cầu hạch toán bổ sung', '- Ô khóa, không đổi được']),
        ('Ô Phiếu yêu cầu hạch toán hoa hồng tháng', 'Textbox', 'Read-only', '–', '–', 'Theo phiếu nguồn',
         ['- Chỉ hiện khi phiếu lập từ phiếu hạch toán hoa hồng tháng (màn nguồn chưa có ở hệ thống mới)', '- Ô khóa']),
        ('Ô Chi phí vận chuyển nhanh', 'Textbox', 'Read-only', '–', '–', '“<N> dòng”',
         ['- Chỉ hiện khi lập từ Danh sách cần hạch toán chi phí vận chuyển nhanh', '- N = số dòng chi phí đã tích ở màn nguồn']),
        ('Ô Ngày hạch toán', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Hôm nay',
         ['- Mặc định: ngày hiện tại' if not edit else '- Nạp ngày hạch toán đã lưu',
          '- Phiếu lập từ phiếu YCĐC: lấy theo phiếu nguồn', '- Trống khi Lưu nháp hoặc Lưu và duyệt → ' + M_REQ + ' dưới ô']),
        ('Ô Loại tiền', 'Dropdown', 'Enable / Disable', 'Danh mục loại tiền', 'Có (khi duyệt)', 'VNĐ',
         ['- Mặc định: VNĐ', '- Lựa chọn: các loại tiền đang dùng (VNĐ, USD, EURO, RUPEE…)',
          '- Khóa khi phiếu đã gắn phiếu YCĐC (loại tiền theo phiếu yêu cầu)',
          '- Đổi loại tiền → Tỷ giá lấy theo danh mục, tính lại toàn bộ cột quy đổi VNĐ; ngoại tệ thì cột Nợ / Có tách đôi',
          '- Trống khi Lưu và duyệt → ' + M_REQ]),
        ('Ô Tỷ giá (VND)', 'Textbox', 'Enable / Disable', '> 0, dấu phẩy ngăn nghìn', 'Có (ngoại tệ, khi duyệt)', '1',
         ['- Luôn hiện; khóa khi Loại tiền là VNĐ', '- Ngoại tệ: mặc định tỷ giá hiện hành của danh mục, sửa được',
          '- Đổi tỷ giá → tính lại cột quy đổi VNĐ', '- Ngoại tệ ≤ 0 khi Lưu và duyệt → ' + M_RATE]),
        ('Ô Diễn giải', 'Textarea', 'Enable', '0–65.535 ký tự', 'Có (khi duyệt)', 'Trống',
         ['- Gợi ý “Nhập diễn giải”, 2 dòng', '- Phiếu lập từ phiếu nguồn: điền sẵn nội dung phiếu nguồn',
          '- Trống (hoặc chỉ khoảng trắng) khi Lưu và duyệt → ' + M_REQ]),
        ('Khối File đính kèm', 'Table/Grid', 'Enable', 'Mỗi file ≤ 20MB', 'Không', 'Trống',
         ['- Lưới STT, Tên file, Dung lượng, nút Xem, Thay đổi, Xóa', '- Nút Thêm tài liệu: chọn nhiều file, tải lên ngay',
          '- File thừa hưởng phiếu nguồn hiện sẵn kèm dung lượng',
          '- Xóa file đã lưu hỏi xác nhận rồi xóa ngay' if edit else '- Xóa file chưa lưu: bỏ khỏi danh sách',
          '- Quá 20MB → “Dung lượng tối đa 20MB”']),
        ('Nút Thêm dòng', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
         ['- Góc phải tiêu đề khối “Chi tiết”', '- Ẩn khi phiếu lập từ phiếu YCĐC hoặc chi phí vận chuyển nhanh',
          '- Bấm → thêm dòng cuối, cùng nhóm định khoản dòng trên; tự điền chênh lệch Nợ − Có vào ô ngược lại để nhóm cân']),
        ('Bảng Chi tiết', 'Table/Grid', 'Enable', '18 cột (20 với ngoại tệ)', 'Có ≥ 1 dòng (khi duyệt)', 'Trống',
         ['- 3 cột đầu (STT, Số tài khoản, Tên tài khoản) ghim trái; thanh cuộn ngang ở cả trên và dưới',
          '- Chưa có dòng: “Chưa có dòng định khoản nào.”', '- Không có dòng khi Lưu và duyệt → ' + M_NOROW]),
        ('Cột Số tài khoản', 'Dropdown', 'Enable', 'Danh mục tài khoản', 'Có (khi duyệt)', 'Trống',
         ['- Danh sách xổ xuống “số - tên”, tìm được theo số hoặc tên; ô đã chọn chỉ hiện số',
          '- Tài khoản đã khóa không hiện để chọn; dòng đang lưu tài khoản khóa thì hiện kèm biểu tượng ổ khóa',
          '- Lập từ phiếu YCĐC: mặc định 1311 khi phiếu nguồn không ghi', '- Trống khi Lưu và duyệt → ' + M_REQ]),
        ('Cột Tên tài khoản', 'Table/Grid', 'Read-only', '–', '–', 'Theo Số tài khoản', '- Tự hiện tên của tài khoản đã chọn'),
        ('Cột Mã khách', 'Textbox', 'Enable / Read-only', '–', 'Không', 'Trống',
         ['- Gợi ý “Nhấn để chọn khách hàng”; bấm ô → cửa sổ Chọn đối tượng (mục 2.7)',
          '- Nút × bỏ chọn: xóa luôn hợp đồng, phiếu YCXH của dòng',
          '- Chỉ hiện chữ (không chọn) ở dòng lập từ phiếu YCĐC']),
        ('Cột Tên khách', 'Table/Grid', 'Read-only', '–', '–', 'Theo đối tượng', '- Tên đối tượng đã chọn'),
        ('Cột Phát sinh nợ', 'Textbox', 'Enable / Read-only', '≥ 0, tối đa 2 số lẻ', 'Có Nợ hoặc Có (khi duyệt)', '0',
         ['- Nhập Nợ > 0 → Phát sinh có của dòng tự về 0', '- Ngoại tệ: tách cột <loại tiền> (nhập) và VNĐ (tự tính)',
          '- Chỉ hiện số ở dòng lập từ phiếu YCĐC', '- Cả Nợ và Có = 0 khi Lưu và duyệt → ' + M_MONEY + ' dưới ô']),
        ('Cột Phát sinh có', 'Textbox', 'Enable / Read-only', '≥ 0, tối đa 2 số lẻ', 'Có Nợ hoặc Có (khi duyệt)', '0',
         ['- Nhập Có > 0 → Phát sinh nợ của dòng tự về 0', '- Ngoại tệ: tách cột <loại tiền> và VNĐ']),
        ('Cột Diễn giải', 'Textbox', 'Enable', '0–255 ký tự', 'Có (khi duyệt)', 'Trống',
         ['- Gợi ý “Nhập diễn giải”', '- Sửa được cả ở dòng lập từ phiếu YCĐC', '- Trống khi Lưu và duyệt → ' + M_REQ]),
        ('Cột Đơn hàng/Hợp đồng', 'Textbox', 'Enable / Read-only', 'Hợp đồng của đúng đối tượng', 'Không', 'Trống',
         ['- Gợi ý “Nhấn để chọn hợp đồng”; bấm ô → cửa sổ Chọn đơn hàng / hợp đồng (mục 2.7)',
          '- Dòng chưa có đối tượng → “Chưa chọn đối tượng”',
          '- Hợp đồng loại 3: hiện ô tích “Số dư nợ đầu kì: <số>” ngay dưới']),
        ('Cột Số phiếu yc xuất hàng', 'Textbox', 'Enable / Ẩn', 'Phiếu của đúng hợp đồng', 'Không', 'Trống',
         ['- Gợi ý “Nhấn để chọn phiếu YCXH”, chỉ cho chọn khi hợp đồng loại 3 và không tích Số dư nợ đầu kì',
          '- Ẩn cả cột khi phiếu lập từ yêu cầu hạch toán bổ sung loại Phối hợp kinh doanh']),
        ('Cột NVKD', 'Table/Grid', 'Read-only', '–', '–', 'Theo hợp đồng', '- Họ tên người lập hợp đồng đã chọn'),
        ('Cột Mã phí', 'Dropdown', 'Enable', 'Danh mục mã phí', 'Không', 'Trống',
         ['- Gợi ý “Chọn mã phí”; mã đã khóa không hiện để chọn mới']),
        ('Cột Mã vụ việc', 'Dropdown', 'Enable', 'Danh mục vụ việc', 'Không', 'Trống',
         ['- Gợi ý “Chọn mã vụ việc”; mã đã khóa không hiện để chọn mới']),
        ('Cột Mã khế ước', 'Table/Grid', 'Read-only', '–', '–', 'Trống', '- Luôn trống (giữ như ERP)'),
        ('Cột Ngân hàng', 'Dropdown', 'Enable', 'Ngân hàng có tài khoản của công ty', 'Không', 'Trống',
         ['- Gợi ý “Chọn ngân hàng”', '- Đổi ngân hàng → xóa STK ngân hàng của dòng']),
        ('Cột STK ngân hàng', 'Dropdown', 'Enable', 'Tài khoản của ngân hàng đã chọn', 'Không', 'Trống',
         ['- Dạng “số tài khoản - loại tiền - tên tài khoản”', '- Chưa chọn ngân hàng thì danh sách rỗng']),
        ('Cột Nhóm định khoản', 'Textbox', 'Enable', 'Số nguyên ≥ 1', 'Không', '1', ['- Sửa được ở mọi phiếu']),
        ('Nút xóa dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
         ['- Thùng rác đỏ cuối dòng, chữ gợi ý “Xóa dòng”; bấm → bỏ dòng ngay, không hỏi', '- Ẩn cùng điều kiện với Thêm dòng']),
        ('Dòng Tổng', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
         ['- Tổng Phát sinh nợ, Tổng Phát sinh có (và tổng quy đổi VNĐ với ngoại tệ)']),
        ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Xám, đứng đầu chân màn', '- Lưu ở trạng thái Đang tạo, không ghi sổ', '- Khóa trong lúc đang lưu']),
        ('Nút Lưu và duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Theo quyền',
         ['- Chỉ hiện với quyền Kế toán thanh toán', '- Bấm → hộp xác nhận duyệt (mục 2.11)']),
    ]
    if not edit:
        rows.append(('Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
                     ['- Chỉ màn Tạo', '- Lưu nháp rồi làm mới form để lập phiếu kế tiếp, ở lại màn Tạo']))
    rows += [
        ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Về màn danh sách', '- Đã đổi dữ liệu mà chưa lưu → hộp “Thông tin chưa lưu”']),
        ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', UNSAVED),
        ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         ['- Chữ đỏ dưới từng ô bắt buộc, viền đỏ ô', '- Chỉ hiện sau lần bấm lưu đầu tiên; sửa đúng thì tự mất',
          '- Kèm thông báo nổi ' + TOAST_422 + ', cuộn tới ô lỗi đầu tiên']),
        ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         ['- Thành công: “Cập nhật thành công.”' if edit else '- Thành công: “Thêm mới thành công.”',
          '- Thất bại: câu lỗi đầu tiên máy chủ trả, mặc định “Lưu thất bại”']),
    ]
    return rows


def save_ev(edit):
    who = 'người tạo phiếu, quyền Kế toán thanh toán' if edit else 'quyền Kế toán thanh toán'
    return [
        ('Mở màn %s' % ('Sửa' if edit else 'Tạo'), 'System',
         'Before:\n– Kiểm tra ' + who + ('; phiếu Đang tạo (nút Sửa chỉ hiện theo cờ máy chủ trả).' if edit else '.') + '\n'
         'During:\n– Nạp danh mục tài khoản, mã phí, mã vụ việc, ngân hàng, tài khoản ngân hàng của công ty, loại tiền và cờ quyền.\n' +
         ('– Nạp phiếu: thông tin chung, dòng định khoản, file đính kèm.\n' if edit else
          '– Có tham số phiếu nguồn → nạp dữ liệu phiếu nguồn (mục 2.5 Dòng sự kiện phụ); không có → form trống, Ngày hạch toán = hôm nay.\n') +
         'After:\n– Hiển thị form, ghi nhận ảnh chụp dữ liệu ban đầu để phát hiện thay đổi chưa lưu.'),
        ('Bấm Thêm dòng', 'Click',
         'Before:\n– Phiếu không lập từ phiếu YCĐC hoặc chi phí vận chuyển nhanh.\n'
         'During:\n– Thêm dòng cuối cùng nhóm định khoản với dòng trên; Nợ − Có của phiếu > 0 → điền chênh lệch vào Phát sinh có, < 0 → '
         'vào Phát sinh nợ.\nAfter:\n– Dòng mới hiện ở cuối bảng, dòng Tổng cập nhật.'),
        ('Nhập Phát sinh nợ hoặc Phát sinh có', 'Change',
         'Before:\n– Ô nhập được (dòng không lập từ phiếu YCĐC).\nDuring:\n– Tính cột quy đổi VNĐ = nguyên tệ × Tỷ giá (làm tròn 2 số lẻ).\n'
         '– Nhập bên này > 0 thì bên kia của dòng về 0.\nAfter:\n– Dòng Tổng cập nhật.'),
        ('Đổi Loại tiền hoặc Tỷ giá', 'Change',
         'Before:\n– Loại tiền không bị khóa (phiếu chưa gắn phiếu YCĐC).\nDuring:\n– Đổi Loại tiền → Tỷ giá lấy theo danh mục; VNĐ → 1 và '
         'khóa ô Tỷ giá.\n– Tính lại toàn bộ cột quy đổi VNĐ.\nAfter:\n– Ngoại tệ: cột Nợ / Có tách đôi, tiêu đề 2 tầng.'),
        ('Bấm Lưu nháp', 'Click',
         'Before:\n– Kiểm tra quyền Kế toán thanh toán' + (' và người tạo, phiếu Đang tạo.' if edit else '.') + '\n'
         '– Nếu không có quyền → hiển thị ' + M_NOPERM + ' và dừng xử lý.\n'
         'During:\n– Ngày hạch toán trống → ' + M_REQ + ' dưới ô, thông báo ' + TOAST_422 + '.\n'
         '– Các ô khác không bắt buộc khi lưu nháp; dòng định khoản thiếu tài khoản vẫn lưu được.\n' + ERR + '\n'
         'After:\n' +
         ('– Cập nhật phiếu, dòng định khoản, file mới / file thay thế; trạng thái giữ Đang tạo.\n'
          '– Ghi một dòng lịch sử “Thay đổi thông tin” (chỉ trường đổi, giá trị cũ → mới); không đổi gì thì không ghi.\n'
          '– Hiển thị “Cập nhật thành công.” và quay về danh sách.' if edit else
          '– Sinh mã <mã công ty>.PKT<mmyy>.<5 số>, lưu phiếu Đang tạo cùng dòng định khoản, file.\n'
          '– Phiếu nguồn: Phiếu YCĐC → Đã tạo phiếu kế toán; Phiếu yêu cầu hạch toán bổ sung → Đang duyệt; dòng vận chuyển nhanh → gắn '
          'phiếu, Đã hạch toán.\n– Ghi một dòng lịch sử “Tạo mới”.\n– Hiển thị “Thêm mới thành công.” và quay về danh sách.')),
    ] + ([] if edit else [
        ('Bấm Lưu và tiếp tục', 'Click',
         'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n– Nếu không có quyền → hiển thị ' + M_NOPERM + ' và dừng xử lý.\n'
         'During:\n– Kiểm tra và lưu như Lưu nháp.\n' + ERR + '\n'
         'After:\n– Hiển thị “Thêm mới thành công.”.\n– Làm mới form về như lúc mới vào màn Tạo (Ngày hạch toán = hôm nay, bảng trống), ở '
         'lại màn Tạo.'),
    ]) + [
        ('Bấm Quay lại hoặc rời màn', 'Click',
         'Before:\n– So dữ liệu hiện tại với ảnh chụp lúc mở màn.\nDuring:\n– Không đổi gì → rời màn ngay.\n– Có thay đổi → hiện hộp '
         '“Thông tin chưa lưu”.\nAfter:\n– Thoát: bỏ thay đổi, về danh sách; Ở lại: giữ nguyên dữ liệu đang nhập.'),
    ]


# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu kế toán',
       mota='Hiển thị bảng phiếu kế toán nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân trang, sắp xếp và tổng số phiếu khớp '
            'bộ lọc. Mỗi dòng cho biết mã phiếu, phiếu nguồn (Mã phiếu YCĐC), tổng phát sinh, diễn giải, ngày hạch toán, người / ngày '
            'tạo và cập nhật, phòng ban của phiếu nguồn, loại tiền và trạng thái ghi sổ; kế toán có quyền Kế toán thanh toán thấy thêm '
            'nút Tạo mới.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Người dùng vào màn theo đường dẫn ở mục Layout (không cần quyền riêng để vào màn).',
       chinh='1. Người dùng vào menu Phiếu kế toán ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem theo thứ tự V1 → V2; không có cấp nào thì lấy phiếu do chính người đó tạo.\n'
             '3. Hệ thống loại bỏ phiếu Đang tạo của người khác.\n'
             '4. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có) và cấu hình cột của người dùng.\n'
             '5. Hệ thống trả về trang 1, phiếu tạo gần nhất xếp trên, kèm tổng số phiếu; dòng “Hiển thị a–b / N” hiện đúng khoảng và tổng.\n'
             '6. Hệ thống hiện nút Tạo mới khi người dùng có quyền Kế toán thanh toán, và nút trên từng dòng theo cờ quyền máy chủ trả.',
       phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng dựng theo cấu hình đó.\n'
           '• Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”; lỗi thiếu quyền không hiện câu này.\n'
           '• Bấm Mã phiếu YCĐC → mở phiếu nguồn (Phiếu yêu cầu điều chỉnh công nợ hoặc Phiếu yêu cầu hạch toán bổ sung) ở tab mới; '
           'nguồn hoa hồng tháng chỉ hiện chữ, không có liên kết.\n'
           '• Bấm nhanh nhiều lần (đổi trang, đổi lọc) → chỉ hiển thị kết quả của lần bấm cuối.\n'
           '• Phiên đăng nhập hết hạn → báo hết phiên đăng nhập, điều hướng về màn đăng nhập.',
       dacbiet='Cột mặc định hiển thị (14): STT, Mã phiếu, Mã phiếu YCĐC, Tổng phát sinh, Diễn giải, Ngày hạch toán, Ngày tạo, Người '
               'tạo, Ngày cập nhật, Người cập nhật, Phòng ban, Loại tiền, Trạng thái, Hành động; không có cột ẩn mặc định. Cột bắt buộc '
               '(khóa, không ẩn / không đổi vị trí): STT, Mã phiếu, Hành động; STT và Mã phiếu ghim trái. Mặc định 10 dòng/trang.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Phiếu kế toán'),
   extra=[('01c_menu_row', 'Dòng phiếu Đang tạo của chính người dùng — nút Sửa, Xóa và menu “…” (In, Xuất Excel, Lịch sử)')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Phiếu kế toán”',
        ['- Là tiêu đề thanh trên cùng, tiêu đề bảng và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Theo quyền',
        ['- Chỉ hiện với quyền Kế toán thanh toán', '- Bấm → mở màn Tạo phiếu kế toán (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.13)', '- Đang xuất: chữ nút đổi thành tiến độ “Đang tải a/N...”, khóa nút']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        ['- Biểu tượng cột, chữ gợi ý “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tùy chỉnh cột (mục 2.4)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Liên tục giữa các trang', '- Ghim trái; khóa trong Tùy chỉnh cột']),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '<mã công ty>.PKT<mmyy>.<5 số>', 'Theo dữ liệu',
        ['- Bấm mã → mở màn chi tiết (mục 2.10)', '- Sắp xếp được', '- Ghim trái; khóa trong Tùy chỉnh cột']),
       ('Cột Mã phiếu YCĐC', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mã phiếu nguồn: Phiếu YCĐC, Phiếu yêu cầu hạch toán bổ sung hoặc hoa hồng tháng; phiếu nhập tay để trống',
         '- Bấm → mở phiếu nguồn ở tab mới (trừ hoa hồng tháng)', '- Không sắp xếp']),
       ('Cột Tổng phát sinh', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
        ['- Tổng quy đổi VNĐ, dấu phẩy ngăn nghìn, căn phải', '- Sắp xếp được']),
       ('Cột Diễn giải', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Xuống dòng khi dài', '- Không sắp xếp']),
       ('Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Ngày hạch toán của phiếu; giờ luôn 00:00 (cột chỉ lưu ngày)', '- Không sắp xếp']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Sắp xếp được; mặc định phiếu mới xếp trên']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Họ tên người tạo phiếu', '- Không sắp xếp']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Thời điểm lưu gần nhất', '- Không sắp xếp']),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Người lưu phiếu gần nhất', '- Không sắp xếp']),
       ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Phòng ban của phiếu YCĐC nguồn (giống ERP), không phải phòng người tạo', '- Không sắp xếp']),
       ('Cột Loại tiền', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- VNĐ, USD, EURO…', '- Không sắp xếp']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu', STATUS_LIST + ['- Không sắp xếp']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo quyền và trạng thái',
        ['- Sửa: người tạo, phiếu Đang tạo → màn Sửa (mục 2.8)',
         '- Xóa (đỏ): cùng điều kiện → hộp Xác nhận xóa ngay trên danh sách (mục 2.9)',
         '- In, Xuất Excel, Lịch sử: luôn hiện',
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
        'Before:\n– Xác định cấp quyền xem theo thứ tự V1 → V2 (Super admin như V1); không có cấp nào thì giới hạn ở phiếu do chính người '
        'dùng tạo.\nDuring:\n– Nạp cấu hình cột đã lưu, khôi phục bộ lọc của 10 phút gần nhất (nếu có), rồi nạp dữ liệu.\n'
        '– Loại bỏ phiếu Đang tạo của người khác; tính cờ Sửa / Xóa cho từng phiếu, cờ Tạo mới theo quyền Kế toán thanh toán.\n'
        'After:\n– Trả về trang 1, sắp xếp theo ngày tạo giảm dần, kèm tổng số phiếu.\n'
        '– Mở / khóa ô lọc Công ty, Phòng ban theo cấp quyền xem; hiện / ẩn nút Tạo mới.'),
       ('Bấm mã phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem (đã lọc ở bước nạp danh sách).\nDuring:\n– Ghi nhớ bộ lọc hiện tại 10 phút.\n'
        'After:\n– Mở màn chi tiết của phiếu (mục 2.10).'),
       ('Bấm Mã phiếu YCĐC', 'Click',
        'Before:\n– Dòng có phiếu nguồn và phiếu nguồn có màn trên hệ thống mới.\nDuring:\n– Phiếu YCĐC → màn chi tiết Phiếu yêu cầu điều '
        'chỉnh công nợ; Phiếu yêu cầu hạch toán bổ sung → màn chi tiết của phiếu đó.\nAfter:\n– Mở ở tab mới, danh sách giữ nguyên.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ 3 cột Mã phiếu, Tổng phát sinh, Ngày tạo sắp xếp được.\n'
        'During:\n– Đổi chiều tăng / giảm; giữ nguyên bộ lọc.\nAfter:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Bấm số trang hoặc nút tiến lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nDuring:\n– Nạp dữ liệu của trang được chọn.\n'
        'After:\n– Hiển thị trang mới, STT liên tục, dòng “Hiển thị a–b / N” cập nhật.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Chọn 1 trong 5, 10, 20, 50, 100.\nDuring:\n– Ghi nhận số dòng mới, chỉ gọi máy chủ một lần.\n'
        'After:\n– Quay về trang 1, nạp lại.'),
       ('Bấm nút “…” trên dòng', 'Click',
        'Before:\n– Dòng có hơn 3 nút (phiếu Đang tạo của mình: Sửa, Xóa, In, Xuất Excel, Lịch sử).\nDuring:\n– Mở menu các nút còn lại '
        '(In, Xuất Excel, Lịch sử).\nAfter:\n– Bấm mục → thực hiện như nút tương ứng; bấm ra ngoài → đóng menu.')])

# ------------------------------------------------------------ 2.2
FILTER_UI = [
    ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
     ['- Gợi ý “Tìm theo mã phiếu...”', '- Tìm theo Mã phiếu, khớp một phần, không phân biệt hoa thường',
      '- Gõ xong bấm Tìm kiếm hoặc Enter mới lọc']),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Áp ô tìm nhanh và các ô đang nhập, về trang 1'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Xóa mọi ô lọc, kể cả ô tìm nhanh và sắp xếp', '- Nạp lại trang 1']),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn', '- Mở / thu gọn khối các ô lọc nâng cao'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Mở cửa sổ Cài đặt bộ lọc (mục 2.3)'),
    ('Ô Công ty', 'Dropdown', 'Enable / Disable', 'Danh mục công ty', 'Không', 'Trống',
     ['- Chỉ chọn được với V1 (Super admin)', '- Chọn → lọc ngay, xóa Phòng ban đang chọn']),
    ('Ô Phòng ban', 'Dropdown', 'Enable / Disable', 'Phòng ban của công ty', 'Không', 'Trống',
     ['- Chọn được với V1, V2', '- Lọc theo phòng ban ghi trên phiếu']),
    ('Ô Mã phiếu YCĐC', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     ['- Khớp một phần mã Phiếu YCĐC, Phiếu yêu cầu hạch toán bổ sung hoặc hoa hồng tháng', '- Bấm Tìm kiếm mới lọc']),
    ('Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Mặc định: trống', '- Chọn → lọc ngay']),
    ('Ô Trạng thái', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
     ['- Mặc định: trống (tất cả)', '- Đang tạo', '- Đã duyệt', '- Chọn → lọc ngay']),
    ('Ô Tài khoản', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     ['- Gợi ý “Nhập tên hoặc số tài khoản”', '- Phiếu có ít nhất 1 dòng định khoản có số hoặc tên tài khoản chứa chuỗi']),
    ('Ô Đơn hàng / Hợp đồng', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     ['- Gợi ý “Nhập mã đơn hàng/hợp đồng”', '- Phiếu có dòng gắn hợp đồng chứa chuỗi']),
    ('Ô Khách hàng', 'Dropdown', 'Enable', 'Gõ ≥ 2 ký tự', 'Không', 'Trống',
     ['- Gợi ý “Gõ mã hoặc tên khách hàng / nhà cung cấp”', '- Danh sách “Mã - Tên”, tìm cả khách hàng lẫn nhà cung cấp',
      '- Chọn → lọc ngay các phiếu có dòng định khoản của đối tượng đó']),
    ('Ô Số tiền', 'Textbox', 'Enable', '≥ 0', 'Không', 'Trống',
     ['- 2 ô “Nhập số tiền từ” → “Nhập số tiền đến”, dấu phẩy ngăn nghìn', '- Lọc theo Tổng phát sinh, lấy cả 2 biên',
      '- Nhấn Enter hoặc bấm Tìm kiếm mới lọc']),
    ('Ô Ngân hàng', 'Textbox', 'Enable', '–', 'Không', 'Trống', ['- Gợi ý “Nhập tên ngân hàng”', '- Khớp một phần tên ngân hàng của dòng']),
    ('Ô STK ngân hàng', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     ['- Gợi ý “Nhập số tài khoản ngân hàng”', '- Khớp một phần STK ngân hàng của dòng']),
    ('Ô NVKD', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     ['- Gợi ý “Chọn nhân viên kinh doanh”', '- Phiếu có dòng gắn hợp đồng do nhân viên đó lập']),
    ('Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy – dd/mm/yyyy', 'Không', 'Trống',
     ['- Khoảng ngày tạo phiếu, lấy trọn 2 ngày biên', '- Chọn xong → lọc ngay']),
]
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu kế toán',
       mota='Thu hẹp danh sách bằng ô tìm nhanh theo mã phiếu và 13 ô lọc nâng cao (Công ty, Phòng ban, Mã phiếu YCĐC, Người tạo, Trạng '
            'thái, Tài khoản, Đơn hàng / Hợp đồng, Khách hàng, Số tiền, Ngân hàng, STK ngân hàng, NVKD, Ngày tạo). Các ô lọc theo dòng '
            'định khoản (tài khoản, hợp đồng, khách hàng, ngân hàng, STK, NVKD) giữ phiếu có ít nhất 1 dòng khớp. Bộ lọc được ghi nhớ '
            '10 phút khi người dùng đi vào màn con của chính màn này.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng nhập mã phiếu vào ô tìm nhanh rồi bấm Tìm kiếm hoặc Enter.\n'
             '2. Người dùng bấm Tìm kiếm nâng cao, chọn / nhập các ô lọc cần dùng.\n'
             '3. Hệ thống lọc ngay với ô chọn (Dropdown, Datepicker); ô gõ chữ / số tiền chỉ lọc khi bấm Tìm kiếm hoặc Enter.\n'
             '4. Hệ thống áp đồng thời mọi điều kiện (VÀ) trong phạm vi quyền xem, trả về trang 1 kèm tổng số mới.\n'
             '5. Hệ thống ghi nhớ bộ lọc 10 phút khi người dùng mở màn chi tiết / sửa / tạo của màn và quay lại.',
       phu='• Không có phiếu khớp → “Không có dữ liệu phù hợp.”.\n'
           '• Bấm Làm mới → xóa mọi ô lọc và ô tìm nhanh, bỏ sắp xếp, nạp lại trang 1.\n'
           '• Không có quyền V1 → ô Công ty khóa; không có V1, V2 → ô Phòng ban cũng khóa.\n'
           '• Ô ẩn qua Cài đặt bộ lọc → giá trị của ô đó bị xóa, không lọc ngầm.\n'
           '• Tải lại trang (F5) hoặc vào từ menu sau hơn 10 phút → bộ lọc về trống.\n'
           '• Từ khóa có ký tự % hoặc _ → được hiểu là ký tự đại diện của phép tìm gần đúng.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối bộ lọc danh sách đang mở Tìm kiếm nâng cao'),
   ui=FILTER_UI,
   ev=[('Nhập ô tìm nhanh rồi bấm Tìm kiếm hoặc Enter', 'Click',
        'Before:\n– Giữ nguyên các ô lọc nâng cao đang chọn.\nDuring:\n– Lọc phiếu có mã chứa chuỗi đã nhập (không phân biệt hoa thường).\n'
        'After:\n– Về trang 1, cập nhật tổng số; không khớp → “Không có dữ liệu phù hợp.”.'),
       ('Chọn giá trị ô Dropdown hoặc Datepicker', 'Change',
        'Before:\n– Ô Công ty chỉ mở với V1; Phòng ban với V1, V2.\nDuring:\n– Áp điều kiện ngay, kết hợp VÀ với các ô khác; đổi Công ty xóa '
        'Phòng ban.\nAfter:\n– Về trang 1, nạp lại danh sách, ghi nhớ bộ lọc.'),
       ('Nhập ô chữ hoặc Số tiền rồi bấm Tìm kiếm', 'Click',
        'Before:\n– Chỉ gõ chưa lọc.\nDuring:\n– Ô theo dòng định khoản: giữ phiếu có ít nhất 1 dòng khớp; Số tiền so với Tổng phát sinh, lấy '
        'biên.\nAfter:\n– Về trang 1, cập nhật tổng.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Đang có ít nhất 1 điều kiện.\nDuring:\n– Xóa mọi ô lọc, ô tìm nhanh, sắp xếp; xóa trạng thái chống gọi trùng.\n'
        'After:\n– Nạp lại trang 1 với phạm vi quyền mặc định.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối đang thu gọn hoặc đang mở.\nDuring:\n– Đổi trạng thái mở / thu gọn.\nAfter:\n– Ghi nhớ trạng thái khối cùng bộ lọc.')])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị trong khối Tìm kiếm nâng cao',
       mota='Cho người dùng chọn ô lọc nào hiện trong khối Tìm kiếm nâng cao và thứ tự của chúng. Cấu hình lưu theo tài khoản, áp cho các '
            'lần mở sau và không ảnh hưởng người khác. Màn có 13 ô lọc nên bắt buộc có cửa sổ này; ẩn một ô đang có giá trị thì giá trị '
            'đó bị xóa để không lọc ngầm bằng ô không nhìn thấy.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n2. Hệ thống mở cửa sổ Cài đặt bộ lọc với danh sách ô lọc, ô đang hiện được tích.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng ☰ để đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo tài khoản, thông báo “Cập nhật thành công”, đóng cửa sổ và dựng lại khối bộ lọc.',
       phu='• Bấm Khôi phục mặc định → trả danh sách và thứ tự về cấu hình ban đầu (chưa lưu cho tới khi bấm Lưu).\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu thay đổi.\n'
           '• Bỏ tích ô đang có giá trị rồi Lưu → ô ẩn, giá trị bị xóa, danh sách nạp lại.'),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', '- Kèm nút (x) đóng'),
       ('Danh sách ô lọc', 'Checkbox', 'Enable', '13 ô lọc', 'Không', 'Theo cấu hình đã lưu',
        ['- Mỗi dòng 1 ô lọc: biểu tượng ☰, ô tích, tên ô', '- Công ty – Phòng ban là 1 dòng (2 ô cùng hiện / ẩn)']),
       ('Biểu tượng ☰', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo thả đổi thứ tự ô trong khối Tìm kiếm nâng cao'),
       ('Ô Tìm ô lọc', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- Lọc nhanh danh sách theo tên ô'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đưa danh sách về mặc định, chưa lưu'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu cấu hình theo tài khoản, đóng cửa sổ'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng không lưu'),
       ('Khối Tìm kiếm nâng cao sau lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình', '- Chỉ còn các ô đã tích, đúng thứ tự đã kéo'),
       ('Ô đang có giá trị bị ẩn', 'Label', 'Hiển thị', '–', '–', '–', '- Giá trị bị xóa, danh sách nạp lại'),
       ('Thông báo lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- Thành công: “Cập nhật thành công”', '- Lỗi: thông báo lỗi chung']),
       ('Cấu hình theo tài khoản', 'Label', 'Hiển thị', '–', '–', '–', '- Tài khoản khác giữ cấu hình riêng của họ')],
   ev=[('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Người dùng đang ở màn danh sách.\nDuring:\n– Nạp cấu hình đã lưu của tài khoản (chưa có → mặc định đủ 13 ô).\n'
        'After:\n– Mở cửa sổ, ô đang hiện được tích.'),
       ('Tích hoặc bỏ tích, kéo ☰', 'Change',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Ghi nhận lựa chọn, thứ tự mới trong cửa sổ.\nAfter:\n– Chưa áp lên khối bộ lọc cho tới khi Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Có ít nhất 1 thay đổi hoặc bấm Khôi phục mặc định.\nDuring:\n– Lưu cấu hình theo tài khoản; ô bị ẩn có giá trị thì xóa giá trị.\n'
        + ERR + '\nAfter:\n– Thông báo “Cập nhật thành công”, đóng cửa sổ, dựng lại khối bộ lọc, nạp lại danh sách nếu có ô bị xóa giá trị.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Đưa danh sách, thứ tự về mặc định.\nAfter:\n– Chưa lưu; bấm Lưu mới áp.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Bỏ mọi thay đổi chưa lưu.\nAfter:\n– Đóng cửa sổ, khối bộ lọc giữ nguyên.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Ẩn / hiện và đổi thứ tự cột của bảng danh sách phiếu kế toán',
       mota='Cho người dùng chọn cột hiển thị và sắp thứ tự cột của bảng danh sách. Cấu hình lưu theo tài khoản trên máy chủ, giữ sau khi '
            'tải lại trang và khi đăng nhập trình duyệt khác, không ảnh hưởng dữ liệu, bộ lọc hay người dùng khác. Cột STT, Mã phiếu, '
            'Hành động bắt buộc (khóa, không ẩn, không kéo đi).',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm nút biểu tượng cột (Cấu hình cột hiển thị).\n2. Hệ thống mở cửa sổ Tùy chỉnh cột với 14 cột, cột đang hiện '
             'được tích, cột bắt buộc khóa.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu theo tài khoản, đóng cửa sổ và dựng lại bảng đúng cột, đúng thứ tự.',
       phu='• Bấm Chọn tất cả → tích đủ 14 cột; Bỏ chọn hết → bỏ tích mọi cột trừ cột bắt buộc.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu.\n'
           '• Ẩn cột đang sắp xếp → bảng vẫn giữ thứ tự sắp xếp hiện tại.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Tuỳ chỉnh cột”', '- Kèm dòng “Đang chọn a/14 cột”'),
       ('Danh sách cột', 'Checkbox', 'Enable', '14 cột', 'Không', 'Theo cấu hình đã lưu',
        ['- Mặc định tích đủ 14 cột', '- Thứ tự mặc định như mục 2.1']),
       ('Cột bắt buộc', 'Checkbox', 'Disable', 'STT, Mã phiếu, Hành động', '–', 'Tích',
        ['- Xám, không bỏ tích, không kéo đổi vị trí', '- STT, Mã phiếu ghim trái; Hành động luôn cuối']),
       ('Biểu tượng ☰', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo thả đổi thứ tự cột không bắt buộc'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích đủ 14 cột'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi cột trừ cột bắt buộc'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu cấu hình theo tài khoản, đóng cửa sổ'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng không lưu'),
       ('Bảng sau khi lưu', 'Table/Grid', 'Hiển thị', '–', '–', 'Theo cấu hình', '- Chỉ cột đã tích, đúng thứ tự'),
       ('Ghi nhớ cấu hình', 'Label', 'Hiển thị', '–', '–', '–', ['- Giữ sau F5, đổi trình duyệt', '- Riêng từng tài khoản']),
       ('Thông báo lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- Lỗi lưu: thông báo lỗi chung')],
   ev=[('Bấm nút Cấu hình cột hiển thị', 'Click',
        'Before:\n– Người dùng đang ở màn danh sách.\nDuring:\n– Nạp cấu hình cột của tài khoản (chưa có → mặc định 14 cột).\nAfter:\n– Mở cửa sổ.'),
       ('Tích hoặc bỏ tích cột, kéo ☰', 'Change',
        'Before:\n– Cột không bắt buộc.\nDuring:\n– Cập nhật “Đang chọn a/14 cột”.\nAfter:\n– Chưa áp lên bảng.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cột bắt buộc luôn tích.\nDuring:\n– Lưu cấu hình theo tài khoản.\n' + ERR + '\nAfter:\n– Đóng cửa sổ, dựng lại bảng.'),
       ('Bấm Chọn tất cả hoặc Bỏ chọn hết', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Tích hết / bỏ tích hết (trừ cột bắt buộc).\nAfter:\n– Chưa lưu.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Bỏ thay đổi.\nAfter:\n– Bảng giữ nguyên.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu kế toán', usecase=('FR-05', 'Lập phiếu kế toán', 'crud', A_KT),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu kế toán mới (Lưu nháp / Lưu và tiếp tục)',
       mota='Kế toán lập phiếu định khoản Nợ / Có theo nhóm định khoản, nhập tay hoặc lập từ phiếu nguồn để hệ thống điền sẵn thông tin '
            'chung, dòng định khoản và file. Lưu nháp tạo phiếu Đang tạo, chưa ghi sổ cái, đồng thời cập nhật trạng thái phiếu nguồn. '
            'Phiếu không có trường nhập duy nhất: mã phiếu do hệ thống sinh khi lưu lần đầu, một Phiếu yêu cầu hạch toán bổ sung chỉ có '
            '1 phiếu kế toán còn hiệu lực.',
       tacnhan=TN_KT, dieukien=DK_TAO,
       chinh='1. Người dùng bấm Tạo mới ở danh sách, hoặc bấm Tạo phiếu kế toán / Lập phiếu kế toán / Tạo phiếu kế toán ở màn phiếu nguồn.\n'
             '2. Hệ thống mở màn “Tạo phiếu kế toán”, nạp danh mục; có phiếu nguồn thì điền sẵn Ngày hạch toán, Loại tiền, Tỷ giá, Diễn '
             'giải, dòng định khoản, file.\n'
             '3. Người dùng (tùy chọn) chọn phiếu YCĐC (mục 2.6), nhập Ngày hạch toán, Loại tiền, Tỷ giá, Diễn giải, thêm file.\n'
             '4. Người dùng thêm dòng, chọn Số tài khoản, đối tượng / hợp đồng / phiếu YCXH (mục 2.7), nhập Phát sinh nợ hoặc có, Diễn '
             'giải, Mã phí, Mã vụ việc, Ngân hàng, STK, Nhóm định khoản.\n'
             '5. Người dùng bấm Lưu nháp (hoặc Lưu và tiếp tục, hoặc Lưu và duyệt — mục 2.11).\n'
             '6. Hệ thống kiểm tra Ngày hạch toán, sinh mã phiếu, lưu phiếu Đang tạo cùng dòng định khoản, file.\n'
             '7. Hệ thống cập nhật phiếu nguồn (Phiếu YCĐC → Đã tạo phiếu kế toán; Phiếu yêu cầu hạch toán bổ sung → Đang duyệt; dòng '
             'vận chuyển nhanh → gắn phiếu).\n'
             '8. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
             '9. Hệ thống hiển thị “Thêm mới thành công.” và quay về danh sách (Lưu và tiếp tục: làm mới form, ở lại màn Tạo).',
       phu='• Vào từ Phiếu YCĐC: ô Phiếu YCĐC điền sẵn; Loại tiền khóa; dòng định khoản điền sẵn (Mã khách, Nợ / Có, Hợp đồng chỉ hiện '
           'chữ), không Thêm dòng / xóa dòng; dòng thiếu tài khoản mặc định 1311.\n'
           '• Vào từ Phiếu yêu cầu hạch toán bổ sung: ô phiếu nguồn khóa; Loại tiền theo phiếu, Tỷ giá theo danh mục; file của phiếu nguồn '
           'nối vào phiếu; loại Phối hợp kinh doanh ẩn cột Số phiếu yc xuất hàng. Phiếu nguồn đã có phiếu kế toán → “Phiếu yêu cầu này '
           'đã có phiếu kế toán”.\n'
           '• Vào từ chi phí vận chuyển nhanh: ô “<N> dòng”, mỗi dòng tạo cặp Nợ 35241 / Có 811; dòng đã hạch toán hoặc đã gắn phiếu → '
           '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”; không đủ quyền → “Bạn không có quyền thực hiện thao tác này”.\n'
           '• Nạp phiếu nguồn lỗi → hiện câu lỗi máy chủ trả, mặc định “Không nạp được dữ liệu phiếu nguồn”.\n'
           '• Thiếu Ngày hạch toán → ' + M_REQ + ' dưới ô, ' + TOAST_422 + '.\n'
           '• Không có quyền Kế toán thanh toán → máy chủ từ chối ' + M_NOPERM + '.\n'
           '• Bấm Lưu nháp liên tục → chỉ lần đầu được xử lý (nút khóa trong lúc lưu), không sinh 2 phiếu.\n'
           '• Bấm Quay lại / rời màn khi đã nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa nhập gì → rời ngay.',
       dacbiet='Màn Tạo là trang riêng (không phải cửa sổ nổi): không có (x) / click ngoài; rời màn bằng Quay lại, menu, nút trình duyệt. '
               'Lập 2 phiếu cùng nội dung đều lưu được, mã khác nhau.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới', 'Cửa vào 1 — nhập tay: form trống, Ngày hạch toán = hôm nay, Loại tiền VNĐ.'),
       (MENU_YC + ' => Tạo phiếu kế toán', 'Cửa vào 2 — nút trên dòng phiếu Chờ tạo phiếu kế toán: điền sẵn từ phiếu YCĐC.'),
       (MENU_HT + ' => Lập phiếu kế toán', 'Cửa vào 3 — nút trên phiếu Chờ duyệt: điền sẵn từ Phiếu yêu cầu hạch toán bổ sung.'),
       ('Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng => Danh sách cần hạch toán chi phí vận chuyển nhanh => '
        'Tạo phiếu kế toán', 'Cửa vào 5 — tích các dòng chi phí rồi bấm nút: điền sẵn cặp Nợ 35241 / Có 811 cho từng dòng. Cửa vào 4 '
        '(hạch toán hoa hồng tháng) chưa có màn nguồn trên hệ thống mới.')],
       shot=shot('10_create'), shot_caption='Màn Tạo phiếu kế toán (nhập tay)'),
   extra=[('10e_filled', 'Màn Tạo sau khi chọn phiếu yêu cầu điều chỉnh công nợ — dữ liệu điền sẵn'),
          ('10f_filled_table', 'Bảng Chi tiết điền sẵn từ phiếu YCĐC (cột Mã khách, Nợ / Có chỉ hiện chữ)'),
          ('22_from_addition', 'Màn Tạo mở từ nút Lập phiếu kế toán ở Phiếu yêu cầu hạch toán bổ sung'),
          ('10b_validate', 'Lỗi đỏ dưới ô khi thiếu thông tin bắt buộc'),
          ('10g_unsaved', 'Hộp Thông tin chưa lưu khi rời màn')],
   ui=form_ui(False), ev=save_ev(False))

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn phiếu yêu cầu điều chỉnh công nợ', usecase=('FR-06', 'Chọn phiếu YCĐC', 'crud', A_KT),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn Phiếu yêu cầu điều chỉnh công nợ làm phiếu nguồn',
       mota='Cửa sổ chọn 1 Phiếu yêu cầu điều chỉnh công nợ đang Chờ tạo phiếu kế toán (của mọi công ty, giống ERP) để điền sẵn Diễn '
            'giải, Ngày hạch toán, Loại tiền, Tỷ giá và dòng định khoản vào phiếu kế toán. Chỉ người có quyền Kế toán thanh toán thấy dữ '
            'liệu; chọn xong Loại tiền bị khóa và bảng chi tiết không thêm / bớt dòng.',
       tacnhan=TN_KT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán thanh toán.\n'
                '3. Đang ở màn Tạo / Sửa phiếu không lập từ Phiếu yêu cầu hạch toán bổ sung, hoa hồng tháng hay vận chuyển nhanh.',
       chinh='1. Người dùng bấm ô Phiếu yêu cầu điều chỉnh công nợ.\n2. Hệ thống mở cửa sổ, nạp phiếu Chờ tạo phiếu kế toán, mới nhất trên.\n'
             '3. Người dùng (tùy chọn) nhập Mã phiếu yêu cầu, chọn Người tạo, bấm Tìm kiếm.\n4. Người dùng bấm vào dòng phiếu cần chọn.\n'
             '5. Hệ thống đóng cửa sổ, nạp dữ liệu phiếu: mã phiếu, Diễn giải, Ngày hạch toán, dòng định khoản (thiếu tài khoản → 1311); '
             'phiếu yêu cầu nhà cung cấp lấy loại tiền, tỷ giá theo phiếu, phiếu khách hàng về VNĐ.\n'
             '6. Hệ thống hiển thị “Thêm phiếu thành công”.',
       phu='• Không có phiếu khớp → “Không có phiếu yêu cầu điều chỉnh công nợ phù hợp.”.\n'
           '• Bấm mã phiếu trong bảng → mở phiếu yêu cầu ở tab mới, không chọn dòng.\n'
           '• Bấm Làm mới → xóa 2 ô lọc, nạp lại trang 1.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, phiếu kế toán không đổi.\n'
           '• Nạp dữ liệu phiếu lỗi → hiện câu lỗi máy chủ trả, mặc định “Không nạp được dữ liệu phiếu nguồn”.\n'
           '• Bấm × ở ô đã chọn → bỏ phiếu YCĐC, Loại tiền về VNĐ, Tỷ giá 1, xóa hết dòng định khoản.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('11_request_picker'),
               shot_caption='Cửa sổ Chọn phiếu yêu cầu điều chỉnh công nợ'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn phiếu yêu cầu điều chỉnh công nợ”',
        ['- Dòng phụ “Chỉ phiếu đang Chờ tạo phiếu kế toán”', '- Kèm nút (x)']),
       ('Ô Mã phiếu yêu cầu', 'Textbox', 'Enable', '–', 'Không', 'Trống',
        ['- Gợi ý “Nhập mã phiếu yêu cầu điều chỉnh”', '- Khớp một phần; Enter để tìm', '- Nút × xóa nhanh']),
       ('Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Gợi ý “Chọn người tạo”', '- Chọn → tìm ngay']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Áp 2 ô lọc, về trang 1'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xóa 2 ô lọc, nạp lại'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Liên tục giữa các trang'),
       ('Cột Mã phiếu yêu cầu', 'Link', 'Enable', '<mã công ty>.DNDCCN<mmyy>.<5 số>', '–', 'Theo dữ liệu',
        ['- Bấm mã → mở phiếu yêu cầu ở tab mới', '- Sắp xếp được']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Họ tên người tạo phiếu yêu cầu'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Theo dữ liệu', '- Sắp xếp được; mặc định mới nhất trên'),
       ('Dòng phiếu', 'Table/Grid', 'Enable', '–', '–', '–', '- Bấm vào dòng (ngoài mã phiếu) → chọn phiếu, đóng cửa sổ'),
       ('Phân trang', 'Pagination', 'Enable', '10, 20, 50, 100', '–', '10 dòng', '- Mặc định 10 dòng/trang'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- “Không có phiếu yêu cầu điều chỉnh công nợ phù hợp.”'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không chọn'),
       ('Thông báo chọn', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Thêm phiếu thành công”', '- Lỗi: câu lỗi máy chủ, mặc định “Không nạp được dữ liệu phiếu nguồn”'])],
   ev=[('Bấm ô Phiếu yêu cầu điều chỉnh công nợ', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n– Nếu không có quyền → cửa sổ không có dữ liệu.\nDuring:\n– Nạp phiếu Chờ tạo phiếu '
        'kế toán, 10 dòng/trang, mới nhất trên.\nAfter:\n– Mở cửa sổ.'),
       ('Nhập ô lọc rồi bấm Tìm kiếm', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Lọc theo mã (một phần) và người tạo.\nAfter:\n– Về trang 1; không khớp → trạng thái rỗng.'),
       ('Bấm dòng phiếu', 'Click',
        'Before:\n– Phiếu vẫn ở Chờ tạo phiếu kế toán.\nDuring:\n– Nạp dữ liệu phiếu nguồn; thiếu tài khoản → 1311; phiếu khách hàng về VNĐ.\n'
        + ERR + '\nAfter:\n– Đóng cửa sổ, điền form, khóa Loại tiền, ẩn Thêm dòng; “Thêm phiếu thành công”.'),
       ('Bấm mã phiếu trong bảng', 'Click',
        'Before:\n– Dòng có mã.\nDuring:\n– Không chọn dòng.\nAfter:\n– Mở phiếu yêu cầu ở tab mới.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Không chọn gì.\nAfter:\n– Đóng, form giữ nguyên.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Chọn đối tượng, hợp đồng và phiếu yêu cầu xuất hàng', usecase=('FR-07', 'Chọn đối tượng, hợp đồng', 'crud', A_KT),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn đối tượng công nợ, hợp đồng và phiếu yêu cầu xuất hàng cho dòng định khoản',
       mota='3 cửa sổ chọn mở từ ô của dòng định khoản: Chọn đối tượng (khách hàng, nhà cung cấp, nhân viên), Chọn đơn hàng / hợp đồng '
            '(hợp đồng bán và mua của đúng đối tượng) và Chọn phiếu yêu cầu xuất hàng (theo hợp đồng loại 3). Đổi đối tượng xóa sạch '
            'hợp đồng, phiếu YCXH, Số dư nợ đầu kì của dòng; đổi hợp đồng xóa phiếu YCXH.',
       tacnhan=TN_KT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán thanh toán.\n'
                '3. Đang ở màn Tạo / Sửa, dòng định khoản không lập từ phiếu YCĐC (ô Mã khách cho chọn).',
       chinh='1. Người dùng bấm ô Mã khách của dòng → cửa sổ Chọn đối tượng.\n2. Người dùng lọc theo Mã, Tên, Loại rồi bấm dòng đối tượng.\n'
             '3. Hệ thống điền Mã khách, Tên khách; xóa hợp đồng, phiếu YCXH, Số dư nợ đầu kì của dòng.\n'
             '4. Người dùng bấm ô Đơn hàng/Hợp đồng → cửa sổ Chọn đơn hàng / hợp đồng của đúng đối tượng, bấm dòng hợp đồng.\n'
             '5. Hệ thống điền mã hợp đồng, NVKD; hợp đồng loại 3 hiện ô tích Số dư nợ đầu kì và cho chọn phiếu YCXH.\n'
             '6. Người dùng (tùy chọn) bấm ô Số phiếu yc xuất hàng, chọn Loại yêu cầu xuất, bấm dòng phiếu → hệ thống điền mã phiếu.',
       phu='• Bấm ô Đơn hàng/Hợp đồng khi dòng chưa có đối tượng → thông báo “Chưa chọn đối tượng”, không mở cửa sổ.\n'
           '• Đối tượng vừa là khách hàng vừa là nhà cung cấp → cửa sổ hợp đồng hiện cả hợp đồng bán và hợp đồng mua.\n'
           '• Bấm số hợp đồng trong cửa sổ → mở hợp đồng ở tab mới, không chọn.\n'
           '• Không có dòng khớp → “Không có dữ liệu phù hợp.”.\n'
           '• Bấm × ở ô → bỏ chọn (bỏ đối tượng kéo theo bỏ hợp đồng và phiếu YCXH).\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, dòng giữ nguyên.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('12_object_picker'), shot_caption='Cửa sổ Chọn đối tượng'),
   extra=[('12b_contract_picker', 'Cửa sổ Chọn đơn hàng / hợp đồng'),
          ('12c_export_request_picker', 'Cửa sổ Chọn phiếu yêu cầu xuất hàng')],
   ui=[('Tiêu đề Chọn đối tượng', 'Label', 'Hiển thị', '–', '–', '“Chọn đối tượng”', '- Kèm nút (x)'),
       ('Ô Mã đối tượng', 'Textbox', 'Enable', '–', 'Không', 'Trống', ['- Gợi ý “Nhập mã khách hàng/NCC”', '- Enter để tìm']),
       ('Ô Tên đối tượng', 'Textbox', 'Enable', '–', 'Không', 'Trống', ['- Gợi ý “Nhập tên khách hàng/NCC”', '- Enter để tìm']),
       ('Ô Loại', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Tất cả',
        ['- Mặc định: Tất cả', '- Khách hàng', '- Nhà cung cấp', '- Nhân viên', '- Chọn → tìm ngay']),
       ('Bảng đối tượng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Mã đối tượng (sắp xếp được), Tên đối tượng (sắp xếp được), Loại', '- Bấm dòng → chọn, đóng cửa sổ',
         '- Phân trang 10, 20, 50, 100 (mặc định 10)']),
       ('Tiêu đề Chọn đơn hàng hợp đồng', 'Label', 'Hiển thị', '–', '–', '“Chọn đơn hàng / hợp đồng”',
        '- Dòng phụ “Đối tượng: <mã - tên>”'),
       ('Ô Số đơn hàng/Hợp đồng', 'Textbox', 'Enable', '–', 'Không', 'Trống', ['- Gợi ý “Nhập số đơn hàng/hợp đồng”', '- Enter để tìm']),
       ('Bảng hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Số đơn hàng/Hợp đồng (link mở tab mới), Ngày lập', '- Bấm dòng → chọn', '- Chưa chọn đối tượng: “Chưa chọn đối tượng.”']),
       ('Tiêu đề Chọn phiếu YCXH', 'Label', 'Hiển thị', '–', '–', '“Chọn phiếu yêu cầu xuất hàng”', '- Dòng phụ “Hợp đồng: <mã>”'),
       ('Ô Loại yêu cầu xuất', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có', 'Yêu cầu xuất hàng',
        ['- Mặc định: Yêu cầu xuất hàng', '- Yêu cầu xuất bán hàng mượn', '- Đổi → tìm lại']),
       ('Ô Mã phiếu', 'Textbox', 'Enable', '–', 'Không', 'Trống', ['- Gợi ý “Nhập mã phiếu”', '- Enter để tìm']),
       ('Bảng phiếu YCXH', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Mã phiếu, Ngày tạo', '- Bấm dòng → chọn', '- Có nút Trang trước, Trang sau khi nhiều trang']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Có ở cả 3 cửa sổ'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xóa ô lọc, nạp lại'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không chọn'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- “Không có dữ liệu phù hợp.”'),
       ('Thông báo chưa chọn đối tượng', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Chưa chọn đối tượng”')],
   ev=[('Bấm ô Mã khách', 'Click',
        'Before:\n– Dòng cho chọn (không lập từ phiếu YCĐC).\nDuring:\n– Nạp đối tượng trang 1.\nAfter:\n– Mở cửa sổ Chọn đối tượng.'),
       ('Bấm dòng đối tượng', 'Click',
        'Before:\n– Cửa sổ Chọn đối tượng đang mở.\nDuring:\n– Điền Mã, Tên khách; khách hàng / nhà cung cấp ghi thêm vào thông tin khách '
        'của dòng.\n– Xóa hợp đồng, phiếu YCXH, Số dư nợ đầu kì.\nAfter:\n– Đóng cửa sổ.'),
       ('Bấm ô Đơn hàng/Hợp đồng', 'Click',
        'Before:\n– Dòng đã có đối tượng.\n– Chưa có → “Chưa chọn đối tượng” và dừng.\nDuring:\n– Nạp hợp đồng bán và mua của đối tượng '
        '(dòng vận chuyển nhanh: chỉ hợp đồng bán của NVKD).\nAfter:\n– Mở cửa sổ.'),
       ('Bấm dòng hợp đồng', 'Click',
        'Before:\n– Cửa sổ hợp đồng đang mở.\nDuring:\n– Điền mã hợp đồng, NVKD, loại hợp đồng; xóa phiếu YCXH.\nAfter:\n– Hợp đồng loại 3: '
        'hiện ô tích Số dư nợ đầu kì, cho chọn phiếu YCXH.'),
       ('Bấm ô Số phiếu yc xuất hàng, chọn dòng', 'Click',
        'Before:\n– Hợp đồng loại 3, chưa tích Số dư nợ đầu kì.\nDuring:\n– Lọc phiếu theo hợp đồng và Loại yêu cầu xuất.\nAfter:\n– Điền mã '
        'phiếu, đóng cửa sổ.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– Một trong 3 cửa sổ đang mở.\nDuring:\n– Không chọn.\nAfter:\n– Đóng, dòng giữ nguyên.')])

# ------------------------------------------------------------ 2.8
fr(8, 'Chỉnh sửa phiếu', usecase=('FR-08', 'Chỉnh sửa phiếu', 'crud', A_KT),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Chỉnh sửa phiếu kế toán Đang tạo',
       mota='Người tạo sửa phiếu kế toán còn Đang tạo (chưa ghi sổ cái) trên cùng form của màn Tạo, dữ liệu nạp sẵn. Mọi trường của màn '
            'Tạo đều sửa được trừ mã phiếu và phiếu nguồn đã gắn (Phiếu yêu cầu hạch toán bổ sung, hoa hồng tháng, vận chuyển nhanh khóa; '
            'phiếu YCĐC đổi được qua ô chọn). Lưu nháp giữ Đang tạo; Lưu và duyệt ghi sổ (mục 2.11).',
       tacnhan=TN_SUA, dieukien=DK_SUA,
       chinh='1. Người dùng bấm Sửa ở cột Hành động, hoặc Sửa ở chân màn chi tiết.\n2. Hệ thống mở màn “Sửa phiếu kế toán: <mã phiếu>”, nạp '
             'thông tin chung, dòng định khoản, file.\n3. Người dùng sửa thông tin (quy tắc như mục 2.5).\n4. Người dùng bấm Lưu nháp.\n'
             '5. Hệ thống kiểm tra quyền, trạng thái Đang tạo và Ngày hạch toán.\n6. Hệ thống cập nhật phiếu, thay toàn bộ dòng định khoản, nối '
             'file mới, thay file đã đổi.\n7. Hệ thống ghi nhận hành động “Thay đổi thông tin” trong lịch sử của phiếu (chỉ trường đổi, cũ → '
             'mới; dòng định khoản ghi bảng thêm / sửa / xóa).\n8. Hệ thống hiển thị “Cập nhật thành công.” và quay về danh sách.',
       phu='• Không đổi gì mà bấm Lưu nháp → lưu, không ghi lịch sử.\n'
           '• Đổi Số tài khoản của 1 dòng → lịch sử ghi “Tài khoản: <cũ> → <mới>” trên chính dòng đó.\n'
           '• Phiếu đã được duyệt / xóa bởi người khác trong lúc sửa → máy chủ từ chối (“Bạn không có quyền sửa phiếu này” hoặc ' +
           M_CONFLICT + '); phiếu không còn → báo không tìm thấy dữ liệu.\n'
           '• Mở thẳng đường dẫn Sửa của phiếu không sửa được → form vẫn mở, bấm Lưu nháp bị máy chủ từ chối.\n'
           '• Xóa file đã lưu → hỏi xác nhận, xóa ngay khỏi phiếu, ghi lịch sử “File đính kèm đã xóa”.\n'
           '• Bấm Quay lại khi đã đổi → hộp “Thông tin chưa lưu”; đổi rồi trả về giá trị ban đầu → rời ngay.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('19_edit'), shot_caption='Màn Sửa phiếu kế toán (phiếu ngoại tệ EURO)'),
   extra=[('19b_edit_table', 'Bảng Chi tiết của phiếu ngoại tệ ở màn Sửa — cột Nợ / Có tách nguyên tệ và VNĐ')],
   ui=form_ui(True), ev=save_ev(True))

# ------------------------------------------------------------ 2.9
fr(9, 'Xóa phiếu', usecase=('FR-09', 'Xóa phiếu', 'action', A_KT),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(
       ten='Xóa phiếu kế toán Đang tạo',
       mota='Người tạo xóa hẳn phiếu kế toán còn Đang tạo cùng toàn bộ dòng định khoản. Phiếu chưa ghi sổ nên không có bút toán cần đảo; '
            'phiếu nguồn được trả về trạng thái chờ xử lý để lập lại. Phiếu Đã duyệt không xóa được (nút ẩn, máy chủ chặn).',
       tacnhan=TN_SUA, dieukien=DK_SUA,
       chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở chân màn chi tiết.\n2. Hệ thống hiện hộp “Xác nhận xóa” với nội dung ' + DEL_MSG +
             '.\n3. Người dùng bấm Xóa.\n4. Hệ thống kiểm tra quyền Kế toán thanh toán, người tạo, trạng thái Đang tạo.\n'
             '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử của phiếu (kèm bảng dòng định khoản trước khi xóa).\n'
             '6. Hệ thống trả phiếu nguồn: Phiếu YCĐC → Chờ tạo phiếu kế toán; Phiếu yêu cầu hạch toán bổ sung → Chờ duyệt; dòng vận chuyển '
             'nhanh → gỡ liên kết, chưa hạch toán.\n7. Hệ thống xóa dòng định khoản và phiếu.\n'
             '8. Hệ thống hiển thị “Xóa thành công.”; ở danh sách nạp lại trang, ở màn chi tiết quay về danh sách.',
       phu='• Bấm Hủy hoặc (x) → đóng hộp, không xóa.\n'
           '• Phiếu vừa được duyệt / người khác không phải người tạo → máy chủ từ chối “Bạn không có quyền xóa phiếu này”, danh sách tự nạp lại.\n'
           '• Phiếu đã bị xóa trước đó → báo không tìm thấy dữ liệu.\n'
           '• Lỗi khác → hiện câu lỗi máy chủ, mặc định “Xóa thất bại”.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp Xác nhận xóa ở màn danh sách'),
   extra=[('13b_delete_detail', 'Hộp Xác nhận xóa ở màn chi tiết')],
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Xóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Theo quyền và trạng thái',
        ['- Thùng rác đỏ, chữ gợi ý “Xóa”', '- Chỉ hiện với người tạo, phiếu Đang tạo']),
       ('Nút Xóa ở màn chi tiết', 'Button', 'Enable / Ẩn', 'Theo quyền và trạng thái', '- Nút đỏ ở chân màn, cùng điều kiện'),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', '“Xác nhận xóa”', '- Kèm nút (x)'),
       ('Nội dung hộp', 'Label', 'Hiển thị', DEL_MSG, '- Ghép đúng mã phiếu của dòng'),
       ('Nút Xóa trong hộp', 'Button', 'Enable', 'Hiển thị', '- Xác nhận xóa'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không xóa'),
       ('Danh sách sau xóa', 'Table/Grid', 'Hiển thị', 'Theo dữ liệu', ['- Mất dòng đã xóa', '- Tổng N giảm 1']),
       ('Phiếu nguồn sau xóa', 'Label', 'Hiển thị', 'Theo dữ liệu',
        ['- Phiếu YCĐC: Chờ tạo phiếu kế toán', '- Phiếu yêu cầu hạch toán bổ sung: Chờ duyệt', '- Dòng vận chuyển nhanh: chưa hạch toán']),
       ('Lịch sử sau xóa', 'Label', 'Hiển thị', '–', '- Mốc “Xóa” kèm bảng dòng định khoản trước khi xóa'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', 'Ẩn', '- “Xóa thành công.”'),
       ('Thông báo thất bại', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- “Bạn không có quyền xóa phiếu này”', '- Mặc định “Xóa thất bại”'])],
   ev=[('Bấm Xóa trên dòng hoặc ở màn chi tiết', 'Click',
        'Before:\n– Nút chỉ hiện khi người đăng nhập là người tạo và phiếu Đang tạo.\nDuring:\n– Ghi nhận phiếu cần xóa.\n'
        'After:\n– Hiện hộp “Xác nhận xóa”.'),
       ('Bấm Xóa trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n– Nếu không có quyền → hiển thị ' + M_NOPERM + ' và dừng xử lý.\n'
        '– Kiểm tra người tạo và trạng thái Đang tạo.\nDuring:\n– Không phải người tạo hoặc phiếu đã duyệt → “Bạn không có quyền xóa phiếu '
        'này”.\n– Phiếu không còn → báo không tìm thấy dữ liệu.\n' + ERR + '\nAfter:\n– Ghi một dòng lịch sử “Xóa”.\n– Trả phiếu nguồn về '
        'trạng thái chờ xử lý; xóa dòng định khoản và phiếu.\n– Hiển thị “Xóa thành công.”; danh sách nạp lại, màn chi tiết về danh sách.'),
       ('Bấm Hủy hoặc (x)', 'Click',
        'Before:\n– Hộp đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng hộp, dữ liệu giữ nguyên.'),
       ('Máy chủ từ chối xóa', 'System',
        'Before:\n– Phiếu đã đổi trạng thái hoặc không thuộc người dùng.\nDuring:\n– Hiện câu lỗi máy chủ trả.\n'
        'After:\n– Danh sách tự nạp lại để cập nhật cờ nút.')])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem chi tiết phiếu', usecase=('FR-10', 'Xem chi tiết phiếu', 'view', A_XEM),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu kế toán',
       mota='Hiển thị toàn bộ thông tin phiếu ở chế độ chỉ đọc trên cùng bố cục form: phiếu nguồn (link), Ngày hạch toán, Loại tiền, Tỷ '
            'giá, Diễn giải, file đính kèm, bảng Chi tiết định khoản kèm dòng Tổng và khối Lịch sử. Chân màn có Sửa, In, Xuất Excel, Xóa, '
            'Quay lại theo cờ quyền máy chủ trả.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm mã phiếu ở danh sách (hoặc bấm thông báo chuông của phiếu).\n2. Hệ thống kiểm tra phiếu nằm trong phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu kế toán: <mã phiếu>”, mọi ô khóa, bảng hiện chữ thường.\n'
             '4. Người dùng bấm link phiếu nguồn để mở phiếu nguồn ở tab mới, xem file, mở khối Lịch sử.\n'
             '5. Người dùng bấm Quay lại → về danh sách, giữ trang và bộ lọc (bộ lọc nhớ 10 phút).',
       phu='• Phiếu ngoài phạm vi / không tồn tại → máy chủ từ chối “Bạn không có quyền xem phiếu này”, màn báo “Không tải được phiếu”.\n'
           '• Phiếu Đang tạo của chính mình → chân màn có thêm Sửa, Xóa.\n'
           '• Phiếu ngoại tệ → cột Nợ / Có tách nguyên tệ và VNĐ.\n'
           '• Phiếu nhập tay → không có ô phiếu nguồn.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết phiếu kế toán (phiếu Đã duyệt)'),
   extra=[('17b_detail_table', 'Bảng Chi tiết định khoản ở màn chi tiết (chỉ đọc)'),
          ('17c_detail_history', 'Khối Lịch sử ở màn chi tiết đã mở')],
   ui_kw=dict(required=False),
   ui=[('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Chi tiết phiếu kế toán: <mã phiếu>”', '- Cũng là tiêu đề tab'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- “<người tạo> - <ngày giờ tạo>” góc phải khối Thông tin chung'),
       ('Ô phiếu nguồn', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Phiếu YCĐC hoặc Phiếu yêu cầu hạch toán bổ sung: mã là link mở tab mới', '- Hoa hồng tháng: chữ thường; nhập tay: không có ô']),
       ('Ô Ngày hạch toán', 'Datepicker', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Ô khóa'),
       ('Ô Loại tiền', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu', '- Ô khóa'),
       ('Ô Tỷ giá (VND)', 'Textbox', 'Read-only', '> 0', 'Theo dữ liệu', '- Ô khóa'),
       ('Ô Diễn giải', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '- Ô khóa'),
       ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Xem / tải file', '- Không có nút Thêm tài liệu, Xóa']),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Đủ cột như màn Tạo, hiện chữ thường, ô trống để trống', '- Không có Thêm dòng, nút xóa dòng']),
       ('Dòng Tổng', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '- Tổng Nợ, Tổng Có'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', ['- Nút Xem lịch sử mở khối, Thu gọn để đóng', '- Như mục 2.14']),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Theo quyền', '- Người tạo, phiếu Đang tạo → màn Sửa'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Mở cửa sổ xem trước bản in (mục 2.12)'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', '- Tải Excel 1 phiếu (mục 2.13)'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo quyền', '- Đỏ; người tạo, phiếu Đang tạo → hộp Xác nhận xóa'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về danh sách, giữ trang và bộ lọc'),
       ('Thông báo lỗi tải', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Không tải được phiếu”')],
   ev=[('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem: Super admin, người tạo, người duyệt, V1, V2 (cùng công ty); phiếu Đang tạo chỉ người tạo xem được.\n'
        '– Nếu không có quyền → máy chủ từ chối “Bạn không có quyền xem phiếu này”, màn báo “Không tải được phiếu” và dừng.\n'
        'During:\n– Nạp phiếu, dòng định khoản, file, cờ Sửa / Xóa.\nAfter:\n– Hiện màn chỉ đọc, nút chân màn theo cờ.'),
       ('Bấm link phiếu nguồn', 'Click',
        'Before:\n– Phiếu có phiếu nguồn có màn trên hệ thống mới.\nDuring:\n– Không rời màn hiện tại.\nAfter:\n– Mở phiếu nguồn ở tab mới.'),
       ('Bấm Xem lịch sử', 'Click',
        'Before:\n– Khối đang thu gọn.\nDuring:\n– Lần mở đầu tiên nạp lịch sử của phiếu.\nAfter:\n– Hiện dòng thời gian, nút đổi thành Thu gọn.'),
       ('Bấm Sửa, In, Xuất Excel hoặc Xóa', 'Click',
        'Before:\n– Sửa, Xóa chỉ hiện theo cờ máy chủ.\nDuring:\n– Chuyển sang xử lý của chức năng tương ứng.\nAfter:\n– Sửa → màn Sửa '
        '(2.8); In → xem trước (2.12); Xuất Excel → tải file (2.13); Xóa → hộp xác nhận (2.9).'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Màn chỉ đọc nên không hỏi chưa lưu.\nDuring:\n– Khôi phục bộ lọc đã nhớ.\nAfter:\n– Về danh sách đúng trang, đúng bộ lọc.')])

# ------------------------------------------------------------ 2.11
fr(11, 'Lưu và duyệt (ghi sổ cái)', usecase=('FR-11', 'Lưu và duyệt', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Lưu và duyệt phiếu kế toán — ghi bút toán vào sổ cái',
       mota='Kế toán lưu phiếu ở trạng thái Đã duyệt: hệ thống kiểm tra đủ thông tin và cân đối từng nhóm định khoản, đề xuất điều chỉnh '
            'số dư lẻ của hợp đồng, rồi ghi mỗi dòng có phát sinh thành 1 bút toán (kèm tài khoản đối ứng) vào sổ cái dùng chung với ERP, '
            'cộng số tiền đã điều chỉnh vào dòng Phiếu báo có và cập nhật phiếu nguồn. Thao tác không hoàn tác: phiếu Đã duyệt không sửa, '
            'không xóa.',
       tacnhan=TN_KT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán thanh toán.\n'
                '3. Đang ở màn Tạo, hoặc màn Sửa phiếu Đang tạo do mình tạo.',
       chinh='1. Người dùng bấm Lưu và duyệt.\n2. Hệ thống hiện hộp ' + APPROVE_TITLE + ' với nội dung ' + APPROVE_MSG + '.\n'
             '3. Người dùng bấm Duyệt.\n4. Hệ thống kiểm tra đủ trường bắt buộc (Phần 4 — BR-03) và báo đỏ dưới ô nếu thiếu.\n'
             '5. Hệ thống dò số dư lẻ của hợp đồng trên TK 1311; có đề xuất → hiện khối “Hợp đồng có số dư lẻ”, chưa lưu.\n'
             '6. Hệ thống kiểm tra 5 luật nhóm định khoản và số dư đầu kì (BR-05), lưu phiếu Đã duyệt, người duyệt.\n'
             '7. Hệ thống cộng số tiền đã điều chỉnh vào dòng Phiếu báo có, ghi bút toán sổ cái theo từng nhóm.\n'
             '8. Hệ thống cập nhật phiếu nguồn: Phiếu YCĐC → Đã duyệt phiếu kế toán; Phiếu yêu cầu hạch toán bổ sung → Đã duyệt (kèm '
             'người duyệt, thời gian duyệt).\n'
             '9. Hệ thống ghi nhận hành động “Tạo mới” / “Thay đổi thông tin” và “Thay đổi trạng thái: Đang tạo → Đã duyệt” trong lịch sử.\n'
             '10. Hệ thống gửi thông báo chuông “[PKT] Đã duyệt: <mã phiếu>” cho người lập phiếu nguồn (Phiếu YCĐC, Phiếu yêu cầu hạch '
             'toán bổ sung).\n11. Hệ thống hiển thị “Duyệt phiếu kế toán thành công.” và quay về danh sách.',
       phu='• Bấm Hủy trong hộp xác nhận → đóng hộp, không lưu, phiếu giữ nguyên.\n'
           '• Thiếu thông tin → lỗi đỏ dưới ô, ' + TOAST_422 + ', cuộn tới ô lỗi đầu tiên, không gọi máy chủ.\n'
           '• Có hợp đồng còn số dư lẻ trong ngưỡng → thông báo “Hợp đồng có số dư lẻ”, khối tích chọn; tích rồi bấm “Áp dụng vào bảng '
           'định khoản” → nối cặp bút toán điều chỉnh với nhóm mới; bấm lại Lưu và duyệt để lưu thật.\n'
           '• Vi phạm luật nhóm định khoản → câu lỗi tương ứng (BR-05), không lưu gì.\n'
           '• Phiếu đã được duyệt trước đó → ' + M_CONFLICT + '.\n'
           '• Không có quyền Kế toán thanh toán → nút ẩn; gọi thẳng → ' + M_NOPERM + '.\n'
           '• Lỗi ở bất kỳ bước ghi nào → không ghi sổ, không đổi trạng thái (xử lý trọn gói).',
       dacbiet='Nút khóa trong lúc đang xử lý: bấm liên tục không ghi 2 bộ bút toán. Thông báo chuông lỗi không làm hỏng phiếu đã ghi sổ.'),
   layout=dict(menu=MENU + ' => Tạo mới => Lưu và duyệt', shot=shot('14_approve_confirm'), shot_caption='Hộp Xác nhận duyệt phiếu kế toán'),
   extra=[('10c_validate_table', 'Lỗi đỏ ở bảng Chi tiết khi Lưu và duyệt thiếu Số tài khoản, Diễn giải, Phát sinh')],
   ui=[('Nút Lưu và duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Theo quyền',
        ['- Màu chính, chân màn Tạo / Sửa', '- Chỉ hiện với quyền Kế toán thanh toán', '- Khóa trong lúc đang xử lý']),
       ('Tiêu đề hộp xác nhận', 'Label', 'Hiển thị', '–', '–', APPROVE_TITLE, '- Kèm nút (x)'),
       ('Nội dung hộp xác nhận', 'Label', 'Hiển thị', '–', '–', APPROVE_MSG, '- Nhấn mạnh ghi sổ không hoàn tác'),
       ('Nút Duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xác nhận ghi sổ'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng hộp, không lưu'),
       ('Lỗi đỏ khi thiếu', 'Toast / Alert', 'Hiển thị', '–', 'Có', 'Ẩn',
        ['- ' + M_REQ + ': Ngày hạch toán, Loại tiền, Diễn giải, Số tài khoản, Diễn giải dòng',
         '- ' + M_RATE + ': phiếu ngoại tệ', '- ' + M_MONEY + ': dòng Nợ = Có = 0', '- ' + M_NOROW + ': bảng trống']),
       ('Khối Hợp đồng có số dư lẻ', 'Checkbox', 'Enable / Ẩn', 'Mỗi hợp đồng 1 dòng', 'Không', 'Ẩn',
        ['- Câu dẫn “Tích chọn hợp đồng cần điều chỉnh về 0, hệ thống sẽ thêm cặp bút toán tương ứng vào cuối bảng định khoản.”',
         '- Mỗi dòng: “Hợp đồng <mã> còn số dư nợ / có <số>”']),
       ('Nút Áp dụng vào bảng định khoản', 'Button', 'Enable', '–', '–', 'Ẩn',
        ['- Nối cặp Nợ 811 / Có 1311 (dư nợ) hoặc Nợ 1311 / Có 711 (dư có), mã phí điều chỉnh số dư, diễn giải “Điều chỉnh số dư lẻ”',
         '- Mỗi hợp đồng tích 1 nhóm định khoản mới']),
       ('Thông báo lỗi nghiệp vụ', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', GROUP_RULES),
       ('Thông báo số dư lẻ', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Hợp đồng có số dư lẻ”'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Duyệt phiếu kế toán thành công.”'),
       ('Thông báo chuông', 'Label', 'Hiển thị', '–', '–', '–',
        ['- Người nhận: người lập phiếu nguồn', '- Nội dung “[PKT] Đã duyệt: <mã phiếu>. Từ đề nghị: <mã>. Số tiền … Ngày hạch toán … '
         'Người duyệt …”', '- Bấm → mở màn chi tiết phiếu kế toán'])],
   ev=[('Bấm Lưu và duyệt', 'Click',
        'Before:\n– Nút chỉ hiện với quyền Kế toán thanh toán.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Hiện hộp xác nhận duyệt.'),
       ('Bấm Duyệt trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n– Nếu không có quyền → hiển thị ' + M_NOPERM + ' và dừng xử lý.\n'
        '– Màn Sửa: kiểm tra người tạo và phiếu Đang tạo; đã duyệt → ' + M_CONFLICT + '.\n'
        'During:\n– Trường bắt buộc trống → ' + M_REQ + ' dưới ô, ' + TOAST_422 + '.\n– Phiếu ngoại tệ, tỷ giá ≤ 0 → ' + M_RATE + '.\n'
        '– Dòng Nợ = Có = 0 → ' + M_MONEY + '; bảng trống → ' + M_NOROW + '.\n'
        '– Có số dư lẻ (lần bấm đầu) → trả đề xuất, không lưu.\n– Vi phạm luật nhóm định khoản → câu lỗi BR-05.\n' + ERR + '\n'
        'After:\n– Lưu phiếu Đã duyệt, người duyệt; cộng tiền đã điều chỉnh vào dòng Phiếu báo có; ghi bút toán sổ cái.\n'
        '– Phiếu nguồn: YCĐC → Đã duyệt phiếu kế toán; hạch toán bổ sung → Đã duyệt.\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái: Đang tạo → Đã duyệt” (kèm “Tạo mới” / “Thay đổi thông tin”).\n'
        '– Gửi thông báo cho người lập phiếu nguồn.\n– Hiển thị “Duyệt phiếu kế toán thành công.”, quay về danh sách.'),
       ('Bấm Hủy hoặc (x)', 'Click',
        'Before:\n– Hộp đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng hộp, form giữ nguyên.'),
       ('Tích hợp đồng rồi bấm Áp dụng vào bảng định khoản', 'Click',
        'Before:\n– Khối Hợp đồng có số dư lẻ đang hiện.\nDuring:\n– Mỗi hợp đồng đã tích: nối 2 dòng điều chỉnh với nhóm định khoản tiếp '
        'theo.\nAfter:\n– Ẩn khối; bấm lại Lưu và duyệt thì lưu thẳng, không dò số dư lẻ lần nữa.'),
       ('Bấm thông báo chuông', 'Click',
        'Before:\n– Người nhận là người lập phiếu nguồn.\nDuring:\n– Kiểm tra phạm vi xem phiếu.\nAfter:\n– Mở màn chi tiết phiếu kế toán.')])

# ------------------------------------------------------------ 2.12
fr(12, 'In phiếu', usecase=('FR-12', 'In phiếu', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu kế toán (xem trước bản in khổ ngang)',
       mota='Mở cửa sổ xem trước bản in theo mẫu “PHIẾU KẾ TOÁN” của ERP (khổ A4 ngang) ngay trên màn danh sách hoặc màn chi tiết, không '
            'mở tab mới. Đầu phiếu là letterhead của công ty ghi trên chứng từ; thân phiếu gồm Mã phiếu, Mã phiếu yêu cầu điều chỉnh công '
            'nợ, Người tạo, Phòng ban, Loại tiền, Diễn giải, bảng định khoản và khối ký. Ai xem được phiếu thì in được.',
       tacnhan=TN_XEM, dieukien=DK_XEM.replace('3. Người dùng đang ở màn danh sách Phiếu kế toán.',
                                              '3. Người dùng đang ở màn danh sách hoặc màn chi tiết Phiếu kế toán.'),
       chinh='1. Người dùng bấm In ở cột Hành động (hoặc trong nút “…”), hoặc In ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem, dựng bản in của phiếu.\n'
             '3. Hệ thống mở cửa sổ “Xem trước phiếu <mã phiếu>” khổ ngang.\n4. Người dùng bấm In để mở hộp in của trình duyệt.',
       phu='• Phiếu ngoài phạm vi → “Bạn không có quyền xem phiếu này”, cửa sổ báo lỗi.\n'
           '• Phiếu ngoại tệ → bảng 11 cột (Nợ / Có tách nguyên tệ và VND) và dòng “- Tỷ giá ngoại tệ: <tỷ giá>”.\n'
           '• Bấm Đóng / (x) → đóng cửa sổ, danh sách / màn chi tiết giữ nguyên.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ xem trước bản in Phiếu kế toán'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '“Xem trước phiếu <mã phiếu>”', '- Kèm nút (x)'),
       ('Letterhead', 'Label', 'Hiển thị', '–', 'Theo công ty trên phiếu', '- Logo, tên công ty theo công ty ghi trên chứng từ'),
       ('Tiêu đề bản in', 'Label', 'Hiển thị', '–', '“PHIẾU KẾ TOÁN”', '- Kèm dòng “Ngày … Tháng … Năm …” theo ngày tạo'),
       ('Khối thông tin', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
        ['- Mã phiếu, Mã phiếu yêu cầu điều chỉnh công nợ', '- Người tạo, Phòng ban', '- Loại tiền, Diễn giải (cùng hàng)']),
       ('Bảng định khoản VNĐ', 'Table/Grid', 'Read-only', '9 cột', 'Theo dữ liệu',
        ['- Tài khoản, khách hàng, Nợ, Có, Diễn giải, hợp đồng, NVKD…', '- Dòng Tổng']),
       ('Bảng định khoản ngoại tệ', 'Table/Grid', 'Read-only', '11 cột', 'Theo dữ liệu', '- Nợ / Có tách <loại tiền> và VND'),
       ('Dòng tỷ giá', 'Label', 'Hiển thị', '2 số lẻ', 'Ẩn', '- “- Tỷ giá ngoại tệ: <tỷ giá>”, căn trái, chỉ phiếu ngoại tệ'),
       ('Khối ký', 'Label', 'Hiển thị', '–', 'Hiển thị', '- 3 ô: Ban giám đốc, Kế toán trưởng, Người lập phiếu'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Mở hộp in của trình duyệt'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- Lỗi tải bản in hiện trong cửa sổ')],
   ev=[('Bấm In', 'Click',
        'Before:\n– Kiểm tra phạm vi xem phiếu.\n– Nếu không có quyền → “Bạn không có quyền xem phiếu này” và dừng xử lý.\n'
        'During:\n– Dựng bản in từ dữ liệu phiếu, letterhead theo công ty trên chứng từ, khổ ngang.\nAfter:\n– Mở cửa sổ xem trước.'),
       ('Bấm In trong cửa sổ', 'Click',
        'Before:\n– Bản in đã tải xong.\nDuring:\n– Mở hộp in của trình duyệt.\nAfter:\n– Người dùng chọn máy in / lưu PDF.'),
       ('Bấm Đóng hoặc (x)', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng, màn giữ nguyên.'),
       ('Tải bản in lỗi', 'System',
        'Before:\n– Máy chủ trả lỗi.\nDuring:\n– Hiện thông báo lỗi trong cửa sổ.\nAfter:\n– Người dùng đóng cửa sổ.')])

# ------------------------------------------------------------ 2.13
fr(13, 'Xuất Excel', usecase=('FR-13', 'Xuất Excel', 'io', A_XEM),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất Excel danh sách phiếu kế toán và Excel một phiếu',
       mota='Xuất danh sách: người dùng chọn trường và thứ tự trường ở cửa sổ “Chọn trường xuất file”, hệ thống tải dữ liệu theo trang '
            'đúng bộ lọc đang áp rồi dựng file ngay trên trình duyệt (có letterhead, tiêu đề “DANH SÁCH PHIẾU KẾ TOÁN”). Xuất 1 phiếu: '
            'tải file chi tiết phiếu theo mẫu ERP (letterhead, khối thông tin, bảng định khoản, 5 ô ký). Ô tiền là số thật có dấu phẩy '
            'ngăn nghìn.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng lọc danh sách (mục 2.2), bấm Xuất Excel trên thanh công cụ.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng.\n'
             '3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự, bấm Xuất file.\n'
             '4. Hệ thống tải dữ liệu theo trang (chữ nút hiện tiến độ “Đang tải a/N...”, “Đang dựng file...”), dựng file '
             'Danh-sach-phieu-ke-toan-<yyyy-mm-dd>.xlsx, đóng cửa sổ.\n5. Hệ thống hiển thị “Xuất Excel thành công”.\n'
             '6. Xuất 1 phiếu: bấm Xuất Excel ở cột Hành động / màn chi tiết → tải Phieu-ke-toan-<mã phiếu, dấu chấm thành gạch>.xlsx, '
             '“Xuất Excel thành công”.',
       phu='• Bộ lọc không có phiếu nào → “Không có dữ liệu để xuất”, không tải file.\n'
           '• Không tích trường nào → nút Xuất file không thực hiện.\n'
           '• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích toàn bộ 12 trường.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không xuất.\n'
           '• Lỗi → “Lỗi khi xuất Excel danh sách” (danh sách), “Lỗi khi xuất Excel” (1 phiếu).',
       dacbiet='Tải theo trang 2.000 dòng / lần nên xuất được toàn bộ hơn 15.000 phiếu; nút khóa trong lúc đang xuất.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn trường xuất file”', '- Kèm nút (x), câu “thứ tự cột chạy theo thứ tự bạn chọn”'),
       ('Danh sách trường', 'Checkbox', 'Enable', '12 trường', 'Có ≥ 1', 'Các cột đang hiện',
        ['- Mã phiếu, Mã phiếu YCĐC, Tổng phát sinh, Diễn giải, Ngày hạch toán, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, '
         'Phòng ban, Loại tiền, Trạng thái', '- Mặc định tích đúng cột đang hiện trên bảng']),
       ('Biểu tượng ☰', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi thứ tự cột trong file'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích đủ 12 trường'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Khóa trong lúc đang xuất'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng không xuất'),
       ('File danh sách', 'Label', 'Hiển thị', '.xlsx', '–', '–',
        ['- Tên Danh-sach-phieu-ke-toan-<yyyy-mm-dd>.xlsx, sheet “Phieu ke toan”', '- Letterhead rộng bằng bảng, tiêu đề “DANH SÁCH PHIẾU KẾ TOÁN”',
         '- Cột STT + các trường đã chọn đúng thứ tự; tiền là số có dấu phẩy']),
       ('File 1 phiếu', 'Label', 'Hiển thị', '.xlsx', '–', '–',
        ['- Tên Phieu-ke-toan-<mã phiếu>.xlsx', '- Letterhead, “Ngày … Tháng … Năm …”, khối thông tin 2 cột, bảng 16 cột (VNĐ) / 18 cột '
         '(ngoại tệ), dòng Tổng, dòng tỷ giá ngoại tệ, 5 ô ký']),
       ('Chữ nút Xuất Excel khi đang xuất', 'Label', 'Hiển thị', '–', '–', '“Xuất Excel”', '- “Đang chuẩn bị dữ liệu...” → “Đang tải a/N...” → “Đang dựng file a/N...”'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Xuất Excel thành công”', '- “Không có dữ liệu để xuất”', '- “Lỗi khi xuất Excel danh sách” hoặc “Lỗi khi xuất Excel”'])],
   ev=[('Bấm Xuất Excel trên thanh công cụ', 'Click',
        'Before:\n– Nút không khóa (không có lượt xuất đang chạy).\nDuring:\n– Nạp danh mục trường từ máy chủ, tích sẵn cột đang hiện.\n'
        'After:\n– Mở cửa sổ Chọn trường xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích.\n– Áp phạm vi quyền xem và bộ lọc đang có.\nDuring:\n– Tải dữ liệu từng trang, hiện tiến '
        'độ; dựng file ở trình duyệt.\n– Không có dòng nào → “Không có dữ liệu để xuất”.\n' + ERR + '\nAfter:\n– Tải file, đóng cửa sổ, '
        '“Xuất Excel thành công”.'),
       ('Bấm Chọn tất cả hoặc Bỏ chọn hết, kéo ☰', 'Change',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Cập nhật danh sách trường, thứ tự.\nAfter:\n– Áp ở lần Xuất file.'),
       ('Bấm Xuất Excel của 1 phiếu', 'Click',
        'Before:\n– Kiểm tra phạm vi xem phiếu.\n– Nếu không có quyền → “Bạn không có quyền xem phiếu này” và dừng xử lý.\n'
        'During:\n– Dựng file chi tiết phiếu ở máy chủ.\nAfter:\n– Tải file, “Xuất Excel thành công”; lỗi → “Lỗi khi xuất Excel”.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ.')])

# ------------------------------------------------------------ 2.14
fr(14, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu kế toán',
       mota='Hiển thị dòng thời gian các thao tác trên phiếu: Tạo mới, Thay đổi thông tin (trường đổi, giá trị cũ → mới, bảng dòng định '
            'khoản thêm / sửa / xóa), Thay đổi trạng thái (Đang tạo → Đã duyệt), File đính kèm đã xóa, Xóa. Mở bằng popup từ danh sách '
            'hoặc khối Lịch sử ở màn chi tiết — 2 nơi giống hệt nhau. Phiếu lập trước ngày 03/10/2026 không có lịch sử cũ.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc trong nút “…”), hoặc Xem lịch sử ở màn chi tiết.\n'
             '2. Hệ thống nạp lịch sử của phiếu, mới nhất trên cùng.\n3. Mỗi mốc hiện loại hành động (màu), người thực hiện, thời gian, '
             'nội dung thay đổi.\n4. Người dùng bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.\n'
             '5. Người dùng bấm Đóng → về danh sách giữ nguyên trang, bộ lọc.',
       phu='• Phiếu chưa có mốc nào (phiếu cũ) → “Chưa có lịch sử”.\n'
           '• Lọc không khớp → không có mốc nào hiện.\n'
           '• Lưu không đổi gì → không sinh mốc mới.\n'
           '• Bấm (x) / click ra ngoài → đóng như bấm Đóng.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi của phiếu'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '“Lịch sử thay đổi: Phiếu <mã phiếu>”', '- Kèm nút (x)'),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Thu gọn', '- Mở / đóng khối lọc'),
       ('Ô Loại hành động', 'Dropdown', 'Enable', 'Danh sách', 'Trống',
        ['- Mặc định: tất cả', '- Tạo mới', '- Thay đổi thông tin', '- Thay đổi trạng thái', '- Xóa']),
       ('Ô Người thực hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', '- Lọc mốc theo người'),
       ('Ô Từ ngày, Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc theo khoảng thời gian'),
       ('Mốc lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mới nhất trên cùng', '- Loại hành động có màu: Tạo mới xanh lá, Thay đổi thông tin xanh dương, Thay đổi trạng thái cam, Xóa đỏ']),
       ('Người thực hiện', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Họ tên người thao tác'),
       ('Thời gian', 'Label', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', '- Thời điểm thao tác'),
       ('Nội dung thay đổi', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- “<Trường>: <cũ> → <mới>”: Mã phiếu nguồn, Ngày hạch toán, Loại tiền, Tỷ giá, Diễn giải, Tổng phát sinh',
         '- Bảng dòng định khoản: thêm / sửa (Tài khoản, Nợ, Có, Diễn giải, Hợp đồng, Mã phí, Mã vụ việc, Ngân hàng, STK, Nhóm) / xóa',
         '- File đính kèm thêm / gỡ']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Chưa có lịch sử”'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ')],
   ev=[('Bấm Lịch sử hoặc Xem lịch sử', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\nDuring:\n– Nạp lịch sử, danh mục người thực hiện.\nAfter:\n– Hiện dòng thời gian mới nhất trên.'),
       ('Chọn ô lọc trong khối Bộ lọc', 'Change',
        'Before:\n– Khối Bộ lọc đang mở.\nDuring:\n– Lọc mốc theo loại, người, khoảng ngày (kết hợp VÀ).\nAfter:\n– Chỉ còn mốc khớp.'),
       ('Lưu phiếu (ghi lịch sử)', 'System',
        'Before:\n– Tạo / sửa / duyệt / xóa phiếu hoặc xóa file.\nDuring:\n– So dữ liệu trước và sau; không đổi gì thì không ghi.\n'
        'After:\n– Ghi mốc tương ứng; đổi Số tài khoản của dòng ghi “Tài khoản: cũ → mới” trên chính dòng.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng, danh sách giữ trang và bộ lọc.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('Phần này chỉ ghi các quy tắc đặc thù của Phiếu kế toán, không lặp lại quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Ngoài SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Mã phiếu tự sinh', ['– Dạng <mã công ty>.PKT<mmyy>.<5 số>, đánh tiếp số lớn nhất của tháng (dùng chung dãy số với ERP).',
                                   '– Sinh khi lưu lần đầu, không sửa được; phiếu không có trường nhập duy nhất nên không kiểm tra trùng.'],
     ['Lập phiếu']),
    ('BR-02', 'Phạm vi xem 2 cấp', ['– V1 (và Super admin): mọi phiếu; V2: phiếu cùng công ty; không quyền: phiếu mình tạo.',
                                    '– Phiếu Đang tạo của người khác luôn ẩn; chi tiết còn mở được cho người duyệt phiếu.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel']),
    ('BR-03', 'Bắt buộc theo nút lưu', ['– Lưu nháp: chỉ Ngày hạch toán.',
                                         '– Lưu và duyệt: Ngày hạch toán, Loại tiền, Tỷ giá > 0 (ngoại tệ), Diễn giải, ≥ 1 dòng; mỗi dòng có '
                                         'Số tài khoản, Diễn giải, Nợ hoặc Có.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-04', 'Vòng đời trạng thái', ['– Lưu nháp → Đang tạo; Lưu và duyệt → Đã duyệt (trạng thái cuối, không đảo).',
                                      '– Không có Hủy, Không duyệt; gọi thẳng trạng thái khác bị chặn.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-05', 'Luật nhóm định khoản khi duyệt', ['– Mỗi dòng có Nợ hoặc Có; trong nhóm không trùng cặp tài khoản + đối tượng + hợp đồng.',
                                                 '– Tổng Nợ = Tổng Có (làm tròn 2 số lẻ); không vừa nhiều dòng Nợ vừa nhiều dòng Có.',
                                                 '– Dòng từ Phiếu báo có: tổng điều chỉnh không vượt số tiền báo có; dòng Số dư nợ đầu kì không '
                                                 'vượt số dư đầu kì của hợp đồng.'],
     ['Lưu và duyệt']),
    ('BR-06', 'Nợ / Có loại trừ nhau, quy đổi', ['– Nhập Nợ > 0 thì Có của dòng về 0 và ngược lại.',
                                                 '– Quy đổi VNĐ = nguyên tệ × Tỷ giá, làm tròn 2 số lẻ; đổi tỷ giá tính lại toàn bộ.'],
     ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-07', 'Dữ liệu điền sẵn theo cửa vào', ['– Phiếu YCĐC: khóa Loại tiền, không thêm / xóa dòng, Mã khách / Nợ / Có / Hợp đồng chỉ đọc, '
                                                'thiếu tài khoản → 1311; phiếu khách hàng về VNĐ.',
                                                '– Hạch toán bổ sung: tỷ giá theo danh mục, nối file phiếu nguồn, loại Phối hợp kinh doanh ẩn cột '
                                                'phiếu YCXH; 1 phiếu nguồn chỉ 1 phiếu kế toán.',
                                                '– Vận chuyển nhanh: mỗi dòng cặp Nợ 35241 / Có 811, không thêm / xóa dòng.'],
     ['Lập phiếu']),
    ('BR-08', 'Liên kết đối tượng – hợp đồng – phiếu YCXH', ['– Hợp đồng lấy theo đối tượng của dòng (KH / NCC: cả hợp đồng bán và mua).',
                                                            '– Đổi đối tượng xóa hợp đồng, phiếu YCXH, Số dư nợ đầu kì; đổi hợp đồng xóa phiếu YCXH.',
                                                            '– Phiếu YCXH, Số dư nợ đầu kì chỉ với hợp đồng loại 3.'],
     ['Chọn đối tượng, hợp đồng']),
    ('BR-09', 'Số dư lẻ', ['– Khi Lưu và duyệt: dư = Nợ 1311 − Có 1311 − Có của phiếu theo hợp đồng; |dư| ≤ ngưỡng công ty → đề xuất.',
                           '– Dư nợ: Nợ 811 / Có 1311; dư có: Nợ 1311 / Có 711; mã phí điều chỉnh số dư, diễn giải “Điều chỉnh số dư lẻ”.'],
     ['Lưu và duyệt']),
    ('BR-10', 'Ghi sổ cái', ['– Mỗi dòng có phát sinh → 1 bút toán (Nợ nếu Nợ > 0, ngược lại Có), kèm đối tượng, hợp đồng, nhóm, loại tiền, tỷ giá.',
                             '– Tài khoản đối ứng: dòng lớn nhất nhóm đối ứng mọi tài khoản còn lại; các dòng khác đối ứng dòng lớn nhất.',
                             '– Ghi sổ, cập nhật phiếu nguồn, lịch sử chạy trọn gói; lỗi bất kỳ bước nào thì không ghi gì.'],
     ['Lưu và duyệt']),
    ('BR-11', 'Cập nhật phiếu nguồn', ['– Lưu nháp: YCĐC → Đã tạo phiếu kế toán; hạch toán bổ sung → Đang duyệt; vận chuyển nhanh → gắn phiếu.',
                                       '– Duyệt: YCĐC → Đã duyệt phiếu kế toán; hạch toán bổ sung → Đã duyệt (người duyệt, thời gian).',
                                       '– Xóa: YCĐC → Chờ tạo phiếu kế toán; hạch toán bổ sung → Chờ duyệt; vận chuyển nhanh → gỡ liên kết.'],
     ['Lập phiếu', 'Lưu và duyệt', 'Xóa']),
    ('BR-12', 'Sửa, xóa', ['– Chỉ người tạo (có quyền Kế toán thanh toán), phiếu Đang tạo.',
                           '– Xóa là xóa hẳn phiếu và dòng định khoản; phiếu Đã duyệt không sửa / xóa.'],
     ['Chỉnh sửa', 'Xóa']),
    ('BR-13', 'Sử dụng ở màn khác', ['– Bút toán phiếu Đã duyệt hiện ở báo cáo Đối chiếu công nợ 1 KH, Chi tiết công nợ KH (link về phiếu) và sổ '
                                     'sách ERP (Phần 5).', '– Duyệt gửi thông báo “[PKT] Đã duyệt: <mã phiếu>” cho người lập phiếu nguồn.'],
     ['Lưu và duyệt']),
    ('BR-14', 'Quy tắc ghi lịch sử', ['– Ghi: Tạo mới, Thay đổi thông tin (chỉ trường đổi, cũ → mới, bảng dòng định khoản), Thay đổi trạng thái, '
                                      'File đính kèm đã xóa, Xóa.', '– Không đổi gì thì không ghi; hiển thị mới nhất trên cùng.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Lưu và duyệt', 'Xóa', 'Xem lịch sử thay đổi']),
    ('BR-15', 'Danh mục khóa', ['– Tài khoản, mã phí, mã vụ việc, ngân hàng, STK đã khóa không chọn mới được.',
                                '– Phiếu đã lưu mã khóa vẫn hiện mã đó kèm biểu tượng ổ khóa.'],
     ['Lập phiếu', 'Chỉnh sửa']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Phiếu kế toán (phiếu, dòng định khoản, bút toán sổ cái).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Tài chính', 'Phiếu yêu cầu điều chỉnh công nợ (nút Tạo phiếu kế toán trên phiếu Chờ tạo phiếu kế toán; trạng thái phiếu yêu cầu '
                       'đi theo phiếu kế toán: Đã tạo / Đã duyệt phiếu kế toán, xóa phiếu kế toán thì về Chờ tạo phiếu kế toán; nhận '
                       'thông báo khi duyệt)', 'Tài chính -> Khởi tạo -> Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi'),
    ('2', 'Tài chính', 'Phiếu yêu cầu điều chỉnh công nợ chờ duyệt (cùng nút Tạo phiếu kế toán, cùng cập nhật trạng thái như dòng 1)',
     'Tài chính -> Chờ duyệt -> Phê duyệt - Công nợ - Thu - Chi'),
    ('3', 'Tài chính', 'Phiếu yêu cầu hạch toán bổ sung (nút Lập phiếu kế toán; màn chi tiết có link sang phiếu kế toán; trạng thái Đang duyệt '
                       '/ Đã duyệt theo phiếu kế toán, xóa phiếu kế toán thì về Chờ duyệt; nhận thông báo khi duyệt)',
     'Tài chính -> Khởi tạo -> Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi'),
    ('4', 'Tài chính', 'Phiếu yêu cầu hạch toán bổ sung chờ duyệt (cùng nút Lập phiếu kế toán như dòng 3)',
     'Tài chính -> Chờ duyệt -> Phê duyệt - Công nợ - Thu - Chi'),
    ('5', 'Bán hàng', 'YC điều chỉnh công nợ, YC hạch toán bổ sung (cùng 2 màn ở dòng 1, 3 — trạng thái theo phiếu kế toán)',
     'Bán hàng -> Yêu cầu -> Công nợ - Thu - Chi'),
    ('6', 'Tài chính', 'Danh sách cần hạch toán chi phí vận chuyển nhanh (nút Tạo phiếu kế toán cho các dòng đã tích; dòng đã hạch toán có '
                       'link mở phiếu kế toán; xóa phiếu kế toán thì dòng về chưa hạch toán)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Nhập hàng'),
    ('7', 'Tài chính', 'Tổng hợp tiền về ngân hàng, Phiếu báo có (duyệt phiếu kế toán lập từ phiếu yêu cầu đi từ báo có thì cộng số tiền đã '
                       'điều chỉnh của dòng báo có)', 'Tài chính -> Quản lý tiền -> Thanh toán tiền mặt'),
    ('8', 'Bán hàng', 'Đối chiếu công nợ 1 KH, Chi tiết công nợ KH (đọc bút toán sổ cái do phiếu kế toán ghi; bấm chứng từ mở phiếu kế toán)',
     'Bán hàng -> Báo cáo -> Báo cáo công nợ'),
    ('9', 'Hệ thống ERP', 'Sổ sách và báo cáo công nợ trên ERP (đọc chung bút toán sổ cái và bảng phiếu kế toán dùng chung)',
     'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
