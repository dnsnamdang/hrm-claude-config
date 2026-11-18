# -*- coding: utf-8 -*-
"""SRS màn "Phiếu giao việc được giao" (phân hệ CSKH sau bán › Giao việc) — form chuẩn SRS_MAU (18/11/2026).

Chạy: python gen_srs_duoc_giao.py  -> "SRS - Phiếu giao việc được giao.docx" (SrsDoc.save() tự chạy srs_selfcheck).
Khuôn: ../phieu-cho-giao-viec/gen_srs.py (12/11). Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột.
Màn = lối vào `?type=waiting_import_result` của route Phiếu giao việc; bộ tài liệu lối `?type=all` ("Phiếu giao việc") CHƯA làm.
Nguồn đọc 18/11/2026 (nhánh develop cả 2 repo, con của gop_db):
  BE  Modules/CustomerCare/Services/WrAssignTaskService.php (applyScope nhánh waiting_import_result, actionFlags, canImportResult,
      canDelete, canView, delete, SORTABLE), WrAssignTaskPrintService (mẫu DANH_SACH_PHIEU_GIAO_VIEC), Concerns/LimitsPrintListRows,
      Http/Controllers/V1/WrAssignTaskController.php, Routes/api.php (không checkPermission), WrImportResultStoreService::updateTaskStatus
      (ghi lịch sử PGV), Modules/Assign/Entities/AssignRequest.php (người thực hiện chỉ ghi khi Phiếu công tác đã duyệt);
      app/Support/Permissions/Catalog/customer_care.php (customer_care.phieu_giao_viec.view mức 2-4; customer_care.phieu_nhap_ket_qua.create
      “Nhập kết quả thực hiện” chỉ có tên cũ guard web, platforms erp).
  FE  pages/customer-care/wr-assign-tasks/{index.vue, _id/index.vue, components/WrAssignTaskForm.vue, wrAssignTaskLinks.js},
      components/subsystem-menu/customer-care.js (nhóm "Giao việc"), utils/mixins/filterStateMixin.js.
  Bối cảnh: design.md, plan.md (Check 06/11, 09/11, 11/11, Fix #12138), spec docs/superpowers/specs/gop-db/2026-10-31-phieu-giao-viec-design.md.
Ảnh: ./pgvdg_shots — dev-hrm 18/11/2026 (_capture/capture.js, DNS Admin, chặn mọi yêu cầu ghi: 0 yêu cầu ghi). DNS Admin là người
  thực hiện của 5 phiếu (dữ liệu thật). GIẢ TRẠNG THÁI duy nhất: 13_delete + icon btn_xoa_row (bật cờ Xóa dòng 1 trên trình duyệt).
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

TEN = 'Phiếu giao việc được giao'
SHOTS = os.path.join(HERE, 'pgvdg_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ CSKH sau bán => Giao việc => Phiếu giao việc được giao'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu giao việc được giao.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
QV = 'Xem phiếu giao việc'
QN = 'Nhập kết quả thực hiện'
A_TH = 'Người thực hiện'
A_TAO = 'Người tạo kiêm người thực hiện'
TN = ('Người dùng có quyền thực hiện chức năng: không cần quyền riêng — người đăng nhập có tên trong danh sách người thực hiện '
      '(trưởng nhóm hoặc thành viên) của phiếu giao việc.')
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Phiếu giao việc được giao.\n'
      '3. Người dùng là người thực hiện của ít nhất 1 phiếu giao việc chưa Hủy.')
EMPTY = '“Không có dữ liệu phù hợp.”'
LOAD_ERR = '“Lỗi khi tải dữ liệu”'
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NO_DEL = '“Bạn không có quyền xóa phiếu giao việc này”'
NO_PERM = '“Bạn không có quyền thực hiện chức năng này.”'

d = SrsDoc(out=OUT, menu=MENU, route='/customer-care/wr-assign-tasks', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ CSKH sau bán': 'menu_phanhe', 'Giao việc': 'menu_nhom', 'Phiếu giao việc được giao': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Xuất Excel': 'btn_xuatexcel', 'In danh sách': 'btn_indanhsach', 'Số phiếu giao việc': 'link_sophieu',
    'Nhập kết quả': 'btn_nhapkq_row', 'Xem phiếu nhập kết quả': 'btn_xemnkq_row', 'Xóa': 'btn_xoa_row',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu giao việc được giao (phân hệ CSKH sau bán, nhóm Giao việc) — HỘP VIỆC của '
    'kỹ thuật viên: danh sách các phiếu giao việc mà người đăng nhập có tên trong danh sách người thực hiện, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ tập phiếu hiển thị: phiếu giao việc gốc, chưa Hủy, có người đăng nhập là trưởng nhóm hoặc thành viên thực hiện — không '
    'xét quyền xem theo cấp, không lọc theo trạng thái, không lấy phiếu chỉ do mình tạo.',
    'Làm rõ nguồn của “người thực hiện”: chỉ Phiếu giao công tác ĐÃ DUYỆT ghi người thực hiện sang phiếu giao việc; phiếu chưa gắn '
    'phiếu công tác đã duyệt thì không hiện ở màn này với bất kỳ ai.',
    'Làm rõ các hành động mở ra từ màn: Xem chi tiết phiếu, Nhập kết quả (mở màn Tạo phiếu nhập kết quả), Xem phiếu nhập kết quả, '
    'Xóa (Hủy) phiếu, Xem lịch sử thay đổi, In danh sách, Xuất Excel.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Xem chi tiết phiếu giao việc, Nhập kết quả, '
    'Xem phiếu nhập kết quả, Xóa phiếu giao việc, Xem lịch sử thay đổi, In danh sách, Xuất Excel danh sách. Màn KHÔNG có Thêm mới '
    '(phiếu giao việc lập từ màn Phiếu chờ giao việc), KHÔNG có Chỉnh sửa (giữ như hệ thống ERP — không có lối vào Sửa), KHÔNG có '
    'Khóa / Mở khóa, Gửi duyệt, Duyệt / Không duyệt, Import. Cùng đường dẫn với màn “Phiếu giao việc” (lối vào theo phạm vi quyền) '
    'nhưng tập phiếu khác nhau; bộ lọc, cấu hình cột, cài đặt bộ lọc của 2 lối vào lưu riêng.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Kỹ thuật viên (người thực hiện) biết mình đang được giao những phiếu nào, việc gì, thời gian dự kiến, khách hàng, chứng từ nguồn.',
    'Kỹ thuật viên nhập kết quả thực hiện cho phiếu đã sẵn sàng (Chờ thực hiện + phiếu công tác đã duyệt) và theo dõi phiếu nhập kết '
    'quả đã lập.',
    'In / xuất danh sách phiếu được giao để báo cáo công việc.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Tập phiếu = phiếu giao việc gốc, trạng thái khác Hủy, người đăng nhập có trong danh sách người thực hiện (BR-01).',
    'Người thực hiện chỉ được ghi khi Phiếu giao công tác chứa phiếu giao việc được DUYỆT; bị ghi đè theo nhân sự của phiếu công tác; '
    'gỡ phiếu khỏi phiếu công tác / xóa phiếu công tác đã duyệt thì xóa người thực hiện (BR-02).',
    'Nút Nhập kết quả chỉ hiện khi phiếu Chờ thực hiện, phiếu công tác đã duyệt, chưa có phiếu nhập kết quả (BR-03).',
    'Nút Xóa chỉ hiện với người tạo phiếu, phiếu Chờ thực hiện và chưa gắn phiếu công tác — rất hiếm ở màn này (BR-05).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu giao việc (PGV)', 'Chứng từ giao việc cho kỹ thuật, mã <mã công ty>.PGV.<năm><6 số>, lập từ màn Phiếu chờ giao việc.'),
    ('Phiếu giao việc được giao', 'Lối vào “hộp việc” của người thực hiện — chỉ phiếu mình có tên trong danh sách người thực hiện.'),
    ('Người thực hiện', 'Nhân sự đi làm phiếu (trưởng nhóm hoặc thành viên), do Phiếu giao công tác đã duyệt ghi sang phiếu giao việc.'),
    ('Trưởng nhóm', 'Người thực hiện được đánh dấu trưởng nhóm; cột Người thực hiện ưu tiên hiện người này.'),
    ('Phiếu giao công tác (PCT)', 'Chứng từ phân công nhân sự (phân hệ Công việc); khi duyệt thì ghi người thực hiện cho phiếu giao việc.'),
    ('Phiếu nhập kết quả (PNKQ)', 'Chứng từ ghi kết quả thực hiện của phiếu giao việc, mã <mã công ty>.PNKQ.<năm><6 số>.'),
    ('Chứng từ nguồn', 'Hợp đồng dịch vụ / phụ lục bổ sung, phiếu bảo hành, phiếu yêu cầu lắp đặt bàn giao, phiếu yêu cầu giao việc khác.'),
    ('Người yêu cầu', 'Người lập chứng từ nguồn của phiếu giao việc.'),
    ('Tổng công định mức', 'Tổng công chính + công phụ của phiếu (2 số lẻ).'),
    ('Trạng thái Chờ thực hiện', 'Nhãn cam: phiếu vừa lập / phiếu nhập kết quả bị xóa — trạng thái duy nhất được Nhập kết quả, Xóa.'),
    ('Trạng thái Đang nhập kết quả', 'Nhãn cam: đã lưu nháp phiếu nhập kết quả.'),
    ('Trạng thái Đã nhập kết quả', 'Nhãn xanh lá: phiếu nhập kết quả đã gửi duyệt.'),
    ('Trạng thái Đang duyệt kết quả', 'Nhãn cam: kết quả đang được duyệt.'),
    ('Trạng thái Đã duyệt kết quả', 'Nhãn xanh lá: kết quả đã duyệt.'),
    ('Trạng thái Chờ BKS duyệt kết quả / Đang đề nghị thanh toán / Đã thanh toán',
     'Các bước sau duyệt kết quả (nhãn cam / cam / xanh lá).'),
    ('Trạng thái Hủy', 'Phiếu đã bị xóa — không hiện ở màn này.'),
    ('Cấu trúc phân cấp', 'Chứng từ nguồn > phiếu giao việc > người thực hiện; phiếu giao việc > phiếu nhập kết quả > phiếu duyệt kết quả.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền ở menu và không chặn quyền khi mở (giữ như ERP): ai đăng nhập cũng vào được, dữ liệu là các phiếu mình là '
    'người thực hiện. Các mã quyền liên quan: customer_care.phieu_giao_viec.view (“%s”, 3 mức Phòng ban / Công ty / Tổng công ty) — '
    'KHÔNG mở rộng danh sách của màn này, chỉ có tác dụng ở lối vào Phiếu giao việc và ở màn chi tiết; customer_care.phieu_nhap_ket_qua'
    '.create (“%s”). Quyền tính theo công ty đang làm việc; không có đặc cách Super admin.' % (QV, QN))
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', QN, 'Theo thiết kế (y ERP): cho bấm Nhập kết quả ở phiếu mình không thực hiện. Ở màn này mọi phiếu đều là phiếu mình '
               'thực hiện nên Q1 không làm thay đổi gì. Lưu ý: hệ thống HRM hiện tra quyền này theo tên cũ mà quyền chỉ khai cho ERP '
               '→ luôn “không có” (không ảnh hưởng màn này).'),
    ('—', 'Người thực hiện', 'Không phải quyền: người có tên trong danh sách người thực hiện của phiếu — điều kiện để thấy phiếu.'),
    ('—', 'Người tạo phiếu', 'Không phải quyền: điều kiện của nút Xóa (cùng trạng thái Chờ thực hiện, chưa gắn phiếu công tác).'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (một mã Xem, màn này KHÔNG dùng):')
d.table(['Ký hiệu', 'Quyền – mức phạm vi', 'Phạm vi dữ liệu'], [
    ('V1', QV + ' – Tổng công ty', 'Màn này: không đổi (chỉ phiếu mình thực hiện). Màn chi tiết: xem được mọi phiếu.'),
    ('V2', QV + ' – Công ty', 'Màn này: không đổi. Màn chi tiết: xem được phiếu của công ty mình.'),
    ('V3', QV + ' – Phòng ban', 'Màn này: không đổi. Màn chi tiết: xem được phiếu của phòng mình quản lý.'),
    ('—', 'Không có quyền nào', 'Màn này: phiếu mình là người thực hiện. Không là người thực hiện phiếu nào → danh sách rỗng.'),
], widths=[0.8, 2.2, 3.0])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người thực hiện', 'Người tạo kiêm thực hiện', 'Q1', 'V1–V3 (không thực hiện)', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ phiếu mình thực hiện', '✅', '—', '❌ (rỗng)', '❌ (rỗng)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '—', '✅ (trên tập rỗng)', '✅ (trên tập rỗng)'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '—', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '—', '✅', '✅'),
    ('FR-05 Xem chi tiết phiếu giao việc', '✅', '✅', '—', '✅ theo mức (mở trực tiếp)', '❌ trang 404'),
    ('FR-06 Nhập kết quả', '✅ khi đủ BR-03', '✅ khi đủ BR-03', '— (không tác dụng)', '❌', '❌'),
    ('FR-07 Xem phiếu nhập kết quả', '✅ khi đủ BR-04', '✅', '—', '—', '❌'),
    ('FR-08 Xóa phiếu giao việc', '❌', '✅ khi đủ BR-05', '—', '❌', '❌'),
    ('FR-09 Xem lịch sử thay đổi', '✅', '✅', '—', '—', '❌'),
    ('FR-10 In danh sách', '✅', '✅', '—', '✅ (rỗng)', '✅ (rỗng)'),
    ('FR-11 Xuất Excel danh sách', '✅', '✅', '—', '✅ (không có dữ liệu)', '✅ (không có dữ liệu)'),
    ('Thêm / Sửa / Khóa / Duyệt / Import', '—', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.6, 1.0, 1.0, 0.7, 1.0, 0.9])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không là người thực hiện của phiếu nào (kể cả có quyền Xem phiếu giao việc mức Tổng công ty, kể cả Super admin, kể cả người tạo '
    'phiếu): danh sách hiện “Không có dữ liệu phù hợp.”.',
    'Mở thẳng màn chi tiết phiếu không phải mình tạo / thực hiện và không có quyền xem theo mức → chuyển trang 404.',
    'Bị gỡ khỏi danh sách người thực hiện (phiếu công tác đổi nhân sự / gỡ phiếu) → lần nạp sau phiếu biến mất khỏi danh sách.',
    'Gọi Xóa khi không phải người tạo → hệ thống từ chối, báo %s.' % NO_DEL,
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nhập kết quả', 'Chưa có phiếu nhập kết quả + Chờ thực hiện + phiếu công tác đã duyệt + có người thực hiện + mình là người thực hiện '
                     '(hoặc Q1)', 'Mở màn Tạo phiếu nhập kết quả'),
    ('Xem phiếu nhập kết quả', 'Trạng thái khác Chờ thực hiện + đã có phiếu nhập kết quả', 'Mở chi tiết phiếu nhập kết quả đầu tiên'),
    ('Xóa', 'Mình là người tạo + Chờ thực hiện + chưa gắn phiếu công tác', 'Hiếm ở màn này (BR-05)'),
    ('Lịch sử', 'Mọi dòng', 'Popup Lịch sử thay đổi'),
    ('In danh sách, Xuất Excel, Cấu hình cột, Cài đặt bộ lọc', 'Luôn hiện', 'Dữ liệu = tập phiếu của màn'),
    ('Thêm mới, ô lọc Công ty – Phòng ban', 'Không hiện ở lối vào này', 'Ô Công ty – Phòng ban chỉ ở lối Phiếu giao việc'),
], widths=[1.8, 2.6, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_TH, [0, 1, 3, 4]), (A_TAO, [0, 2])],
    [('FR-01', 'Xem danh sách phiếu được giao', 'view'),
     ('FR-06', 'Nhập kết quả', 'crud'),
     ('FR-08', 'Xóa phiếu giao việc', 'action'),
     ('FR-10', 'In danh sách', 'io'),
     ('FR-11', 'Xuất Excel danh sách', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-05', 'Xem chi tiết phiếu giao việc', 'view', 'extend', [0], None),
     ('FR-07', 'Xem phiếu nhập kết quả', 'view', 'extend', [0], None),
     ('FR-09', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu giao việc được giao')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu giao việc được giao',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu giao việc mình được giao',
       mota='Hiển thị các phiếu giao việc gốc chưa Hủy mà người đăng nhập có tên trong danh sách người thực hiện (trưởng nhóm hoặc thành '
            'viên), ở mọi trạng thái từ Chờ thực hiện đến Đã thanh toán. Không xét quyền xem theo cấp và không lấy phiếu mình tạo nhưng '
            'không thực hiện. Bảng có 13 cột, cột Hành động tính nút theo từng dòng; bộ lọc và cấu hình cột lưu riêng cho lối vào này.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để mở màn; dữ liệu giới hạn theo danh sách người thực hiện.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống đặt tiêu đề trang “Phiếu giao việc được giao”, khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút) và cấu hình '
             'cột đã lưu của người dùng cho lối vào này.\n'
             '3. Hệ thống lấy phiếu giao việc gốc, trạng thái khác Hủy, có người đăng nhập trong danh sách người thực hiện, khớp bộ lọc; '
             'sắp Ngày tạo mới nhất ở trên.\n'
             '4. Hệ thống hiển thị trang 1, 10 dòng/trang, tiêu đề bảng “Phiếu giao việc được giao”, dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Với từng dòng, hệ thống tính các nút ở cột Hành động: Nhập kết quả (BR-03), Xóa (BR-05), Xem phiếu nhập kết quả (BR-04), '
             'Lịch sử (luôn có).\n'
             '6. Người dùng bấm Số phiếu giao việc để mở chi tiết (mục 2.5), bấm Số hợp đồng / Số phiếu yêu cầu để mở chứng từ nguồn ở '
             'tab trình duyệt mới.',
       phu='• Không là người thực hiện của phiếu nào / không khớp bộ lọc → bảng hiện %s, chân bảng “Không có phiếu nào.”.\n'
           '• Máy chủ lỗi khi nạp → thông báo %s, bảng trống.\n'
           '• Đang ở màn mà bấm mục menu “Phiếu giao việc” → hệ thống bỏ bộ lọc của lối vào này, nạp tập phiếu theo phạm vi quyền (màn '
           'khác, ngoài tài liệu này); bấm lại “Phiếu giao việc được giao” thì quay về tập phiếu của mình.\n'
           '• Phiếu bị Hủy / bị gỡ người thực hiện bởi người khác → lần nạp sau biến mất khỏi danh sách.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, chuyển về màn đăng nhập.' % (EMPTY, LOAD_ERR),
       dacbiet='Cột mặc định hiện: tất cả 13 cột. Cột khóa: STT, Số phiếu giao việc, Hành động. Sắp xếp được: Số phiếu giao việc, Số '
               'hợp đồng, Số phiếu yêu cầu, Thời gian dự kiến (theo ngày bắt đầu), Tổng công định mức, Ngày tạo; mặc định Ngày tạo mới '
               'nhất. Mỗi trang tối đa 100 dòng. Không có nút Tạo mới / Import.'),
   layout=dict(entries=[
       (MENU, 'Lối vào duy nhất của màn này. Hiển thị: chỉ phiếu giao việc người đăng nhập là người thực hiện. Cùng nhóm có mục '
              '“Phiếu giao việc” — cùng màn nhưng hiển thị phiếu theo phạm vi quyền xem (tài liệu riêng).')],
       shot=shot('01_list'), shot_caption='Màn Phiếu giao việc được giao'),
   extra=[(shot('00_menu'), 'Mục Phiếu giao việc được giao trong nhóm Giao việc (phân hệ CSKH sau bán)'),
          (shot('03_empty'), 'Trạng thái không có dữ liệu phù hợp')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Phiếu giao việc được giao” trên thanh đầu trang và tab trình duyệt.'),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Phiếu giao việc được giao”.'),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.10).'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.11)', '- Khóa khi đang xuất']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa, cố định khi cuộn ngang']),
       ('Cột Số phiếu giao việc', 'Link', 'Enable', '–', 'Hiển thị',
        ['- Bấm → mở màn Chi tiết phiếu giao việc trong cùng tab (mục 2.5)', '- Sắp xếp được; cột khóa, cố định khi cuộn ngang']),
       ('Cột Số hợp đồng', 'Link', 'Enable', '–', 'Hiển thị',
        ['- Phiếu từ hợp đồng / phụ lục: bấm → chi tiết hợp đồng dịch vụ, tab mới',
         '- Phiếu từ phiếu bảo hành: hiện mã phiếu bảo hành, bấm → chi tiết phiếu bảo hành, tab mới',
         '- Phiếu lắp đặt: số hợp đồng bán, bấm → hợp đồng HRM hoặc hợp đồng bán ở hệ thống ERP, tab mới',
         '- Phiếu giao việc khác: trống', '- Số dài tự xuống dòng; sắp xếp được']),
       ('Cột Số phiếu yêu cầu', 'Link', 'Enable', '–', 'Hiển thị',
        ['- Phiếu yêu cầu lắp đặt bàn giao hoặc phiếu yêu cầu giao việc khác; bấm → chi tiết phiếu yêu cầu, tab mới',
         '- Trống với phiếu từ hợp đồng / bảo hành', '- Sắp xếp được']),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Dạng “Mã KH-Tên khách hàng”', '- Tối đa 2 dòng']),
       ('Cột Người yêu cầu', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Người lập chứng từ nguồn, dạng “Họ tên - SĐT”', '- Thứ tự lấy: hợp đồng / bảo hành → yêu cầu giao việc khác → yêu cầu lắp đặt']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Người lập phiếu giao việc, dạng “Họ tên - SĐT”.'),
       ('Cột Người thực hiện', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Trưởng nhóm; không có trưởng nhóm thì người đầu danh sách', '- Dạng “Họ tên - SĐT”',
         '- Có thể là người khác với người đăng nhập (mình là thành viên)']),
       ('Cột Thời gian dự kiến', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Hiển thị',
        ['- “Ngày bắt đầu-Ngày kết thúc”', '- Sắp xếp theo ngày bắt đầu']),
       ('Cột Tổng công định mức', 'Table/Grid', 'Read-only', '≥ 0', 'Hiển thị',
        ['- 2 số lẻ, phân cách hàng nghìn bằng dấu phẩy', '- Bằng 0 thì để trống', '- Sắp xếp được']),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 8 giá trị', 'Hiển thị',
        ['- Nhãn cam: Chờ thực hiện, Đang nhập kết quả, Đang duyệt kết quả, Chờ BKS duyệt kết quả, Đang đề nghị thanh toán',
         '- Nhãn xanh lá: Đã nhập kết quả, Đã duyệt kết quả, Đã thanh toán', '- Không sắp xếp']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Sắp xếp được; mặc định mới nhất ở trên.'),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Nhập kết quả (biểu tượng sổ bút) → mục 2.6', '- Xóa (thùng rác đỏ) → mục 2.8',
           '- Xem phiếu nhập kết quả (biểu tượng kính lúp trên tài liệu) → mục 2.7', '- Lịch sử (đồng hồ) → mục 2.9',
           '- Tối đa 3 nút hiện thẳng; nút không đủ điều kiện thì ẩn', '- Cột khóa']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Giữa bảng: “Không có dữ liệu phù hợp.” khi N = 0', '- Chân bảng: “Không có phiếu nào.”']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang', '- N: tổng số phiếu được giao khớp bộ lọc']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Trang đầu: về đầu / lùi mờ; trang cuối: tiến / về cuối mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Lỗi khi tải dữ liệu” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định lối vào “được giao”; không kiểm quyền.\n– Khôi phục bộ lọc (10 phút) và cấu hình cột của lối vào.\n'
        'During:\n– Lấy phiếu gốc, khác Hủy, có người đăng nhập trong người thực hiện, khớp bộ lọc; tính cờ nút từng dòng.\n'
        '– Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, phiếu mới tạo nhất ở trên, kèm dòng “Hiển thị a–b / N”.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ 6 cột Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Thời gian dự kiến, Tổng công định mức, Ngày tạo hỗ '
        'trợ sắp xếp.\nDuring:\n– Ghi cột + chiều sắp xếp vào bộ lọc.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc; độ rộng cột cố định nên bảng không nhảy bố cục.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp; bấm lại trang đang xem thì bỏ qua.\nDuring:\n– Nạp dữ liệu trang mới.\n'
        'After:\n– Hiển thị trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nDuring:\n– Tối đa 100 dòng/trang.\nAfter:\n– Về trang 1 và nạp lại theo số dòng mới.'),
       ('Bấm Số hợp đồng / Số phiếu yêu cầu', 'Click',
        'Before:\n– Dòng có chứng từ nguồn tương ứng.\nDuring:\n– Màn đích tự kiểm quyền xem của nó.\n'
        'After:\n– Mở chi tiết chứng từ ở tab trình duyệt mới; danh sách giữ nguyên.'),
       ('Bấm mục menu “Phiếu giao việc” khi đang ở màn', 'Click',
        'Before:\n– Cùng màn, khác lối vào.\nDuring:\n– Xóa bộ lọc đã ghi nhớ của lối vào được giao.\n'
        'After:\n– Nạp bộ lọc, cấu hình cột của lối vào Phiếu giao việc và tập phiếu theo phạm vi quyền.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu được giao',
       mota='Thu hẹp danh sách phiếu mình thực hiện. Ô tìm nhanh tìm theo số phiếu giao việc; 8 ô lọc nằm trong khối Tìm kiếm nâng cao '
            '(Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Trạng thái, Người tạo, Người thực hiện, Thời gian dự kiến), bật '
            '/ tắt được bằng Cài đặt bộ lọc. Mọi điều kiện chỉ lọc TRONG tập phiếu được giao, không mở rộng ra phiếu khác.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập số phiếu giao việc vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Ô chọn (Khách hàng, Người yêu cầu, Trạng thái, Người tạo, Người thực hiện, Thời gian dự kiến) lọc ngay khi đổi; ô gõ chữ '
             '(Số hợp đồng, Số phiếu yêu cầu) lọc khi bấm Tìm kiếm / nhấn Enter; về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Khi người dùng mở chi tiết phiếu, hệ thống ghi nhớ bộ lọc 10 phút để khôi phục lúc quay lại.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện %s.\n'
           '• Ô Khách hàng: gõ tối thiểu 2 ký tự mới hiện gợi ý (tối đa 30, toàn bộ danh mục khách hàng).\n'
           '• Chọn Người thực hiện là người khác → chỉ còn phiếu có CẢ người đó và mình trong danh sách người thực hiện.\n'
           '• Sang màn khác (Nhập kết quả, Xem phiếu nhập kết quả, menu khác) → bộ lọc bị xóa; quay lại màn là danh sách đầy đủ.' % EMPTY,
       dacbiet='Ô tìm nhanh, Số hợp đồng, Số phiếu yêu cầu: khớp một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối, không '
               'giới hạn ký tự; % và _ là ký tự đại diện. Số hợp đồng tìm trên số hợp đồng dịch vụ / mã phiếu bảo hành hoặc số hợp đồng '
               'bán của yêu cầu lắp đặt. Thời gian dự kiến: ngày bắt đầu ≥ Từ ngày và ngày kết thúc ≤ Đến ngày. Người yêu cầu lọc cùng thứ '
               'tự với cột hiển thị. Không có ô Công ty – Phòng ban ở lối vào này.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   extra=[(shot('02b_filter_status'), 'Ô Trạng thái đang mở')],
   ui=[
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu giao việc”', '- Khớp một phần số phiếu', '- Chỉ lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh và ô gõ chữ, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, về trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc, chữ đổi thành “Ẩn tìm kiếm nâng cao”', '- Bấm lại → thu gọn']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Số hợp đồng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Khớp một phần', '- Lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Số phiếu yêu cầu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Khớp một phần số phiếu yêu cầu lắp đặt / giao việc khác', '- Lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Khách hàng', 'Dropdown', 'Enable', 'Tìm trong danh mục khách hàng', 'Không', 'Trống',
        ['- Gợi ý “Gõ để tìm khách hàng...”', '- Gõ tối thiểu 2 ký tự, tối đa 30 gợi ý', '- Lọc đúng khách hàng đã chọn']),
       ('Người yêu cầu', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Mặc định: trống', '- Lọc ngay khi chọn']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 8 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (mọi trạng thái)', '- Lựa chọn: Chờ thực hiện', '- Đang nhập kết quả', '- Đã nhập kết quả',
         '- Đang duyệt kết quả', '- Đã duyệt kết quả', '- Chờ BKS duyệt kết quả', '- Đang đề nghị thanh toán', '- Đã thanh toán']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '- Lọc theo người lập phiếu giao việc.'),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        '- Lọc phiếu có nhân viên đã chọn trong danh sách người thực hiện (trưởng nhóm hoặc thành viên).'),
       ('Thời gian dự kiến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng Từ ngày → Đến ngày', '- Được bỏ trống một đầu', '- Lọc ngay khi chọn']),
       ('Nút × trong ô chọn', 'Icon Button', 'Enable', '–', '–', 'Ẩn', '- Xóa giá trị của ô đó và lọc lại.'),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\nDuring:\n– Ghi nhận giá trị mới; giá trị không đổi thì bỏ qua.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí, trong tập phiếu được giao.'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, Số hợp đồng, Số phiếu yêu cầu; bỏ khoảng trắng đầu / cuối.\nDuring:\n– Tìm phiếu có số phiếu '
        '/ số hợp đồng / số phiếu yêu cầu chứa chuỗi nhập.\nAfter:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nDuring:\n– Đưa mọi ô về trống, bỏ khách hàng đã chọn.\n'
        'After:\n– Bỏ sắp xếp, nạp lại trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\nAfter:\n– Mở / thu gọn khối ô lọc.'),
       ('Gõ vào ô Khách hàng', 'Change',
        'Before:\n– Đã gõ tối thiểu 2 ký tự.\nDuring:\n– Tìm trong danh mục khách hàng.\nAfter:\n– Hiện tối đa 30 khách hàng khớp; chọn → lọc ngay.'),
       ('Quay lại từ màn chi tiết trong 10 phút', 'System',
        'Before:\n– Người dùng vừa mở chi tiết phiếu từ danh sách.\nDuring:\n– Đọc bộ lọc đã ghi nhớ.\n'
        'After:\n– Khôi phục bộ lọc, khách hàng đã chọn, trạng thái khối lọc; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn những ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự. Cấu hình lưu riêng theo '
            'người dùng và riêng cho lối vào Phiếu giao việc được giao (khác với lối vào Phiếu giao việc), không đổi dữ liệu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 8 mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng + lối vào, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 8 mục theo thứ tự thiết kế; vẫn phải bấm Lưu.\n'
           '• Bỏ tích mục đang có giá trị lọc → ô bị ẩn.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet='8 mục: Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Trạng thái, Người tạo, Người thực hiện, Thời gian dự kiến.'),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 8 mục', '–', 'Theo cấu hình đã lưu',
        ['- Số hợp đồng', '- Số phiếu yêu cầu', '- Khách hàng', '- Người yêu cầu', '- Trạng thái', '- Người tạo', '- Người thực hiện',
         '- Thời gian dự kiến']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → ô lọc đó không hiện.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích lại đủ các mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
       ('Khối Tìm kiếm nâng cao sau khi lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình', '- Chỉ hiện ô đã tích, đúng thứ tự.'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\nDuring:\n– Đọc cấu hình đang lưu của lối vào.\n'
        'After:\n– Mở cửa sổ (chưa lưu lần nào → đủ 8 mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại và lối vào Phiếu giao việc được giao.\nDuring:\n– Gửi danh sách mục đã tích theo '
        'đúng thứ tự.\n' + ERR + '\nAfter:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ các mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 13 cột của bảng. Ba cột STT, Số phiếu giao việc, Hành động bị khóa; cấu hình lưu '
            'theo người dùng và riêng cho lối vào này trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 13 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 13 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ sau khi tải lại trang, đăng nhập lại, đổi '
               'trình duyệt; người dùng khác không bị ảnh hưởng. Cột đang hiện được tích sẵn khi Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 13 cột', '–', 'Theo cấu hình đã lưu',
        '- STT, Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Người tạo, Người thực hiện, Thời gian '
        'dự kiến, Tổng công định mức, Trạng thái, Ngày tạo, Hành động.'),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Số phiếu giao việc, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/13 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền riêng.\nDuring:\n– Đọc cấu hình cột của người dùng cho lối vào.\nAfter:\n– Mở cửa sổ.'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/13 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại và lối vào.\nDuring:\n– Gửi danh sách cột đã tích theo thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5
fr(5, 'Xem chi tiết phiếu giao việc',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết 1 phiếu giao việc được giao',
       mota='Bấm Số phiếu giao việc để mở trang chi tiết chỉ đọc: thông tin khách hàng và chứng từ nguồn, các bảng công việc theo loại phiếu '
            '(bảo hành / sửa chữa – bảo dưỡng / lắp đặt bàn giao / dịch vụ đính kèm), vật tư bán thêm, công việc phụ, tổng hợp công định '
            'mức và khối Lịch sử. Chân trang có các nút hành động cùng điều kiện như cột Hành động của danh sách. Không có nút Sửa.',
       tacnhan='Người dùng có quyền thực hiện chức năng: người thực hiện hoặc người tạo phiếu; hoặc có quyền “%s” (mức Phòng ban / '
               'Công ty / Tổng công ty theo phiếu).' % QV,
       dieukien=DK + '\n4. Phiếu chưa Hủy.',
       chinh='1. Người dùng bấm Số phiếu giao việc ở danh sách.\n'
             '2. Hệ thống ghi nhớ bộ lọc danh sách (10 phút) và mở trang “Chi tiết phiếu giao việc: <mã>” kèm nhãn trạng thái.\n'
             '3. Hệ thống kiểm tra người xem: người tạo, người thực hiện, hoặc quyền xem theo mức.\n'
             '4. Hệ thống hiển thị các khối thông tin ở chế độ chỉ đọc, góc phải khối đầu ghi “<Người tạo> - <ngày giờ tạo>”.\n'
             '5. Chân trang hiện Nhập kết quả / Xem phiếu nhập kết quả / Xóa theo điều kiện và nút Quay lại.\n'
             '6. Người dùng bấm Quay lại → về danh sách được giao, khôi phục bộ lọc.',
       phu='• Phiếu không tồn tại / đã Hủy / người xem không có quyền → chuyển trang 404, không thông báo.\n'
           '• Lỗi khác khi tải → thông báo “Không tải được phiếu giao việc.”.\n'
           '• Bấm chứng từ nguồn (hợp đồng / phiếu bảo hành / phiếu yêu cầu) → mở chi tiết chứng từ ở tab mới.\n'
           '• Mở chi tiết bằng đường dẫn trực tiếp / tab mới rồi bấm Quay lại → về màn Phiếu giao việc (lối vào theo phạm vi quyền).\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, chuyển về màn đăng nhập.',
       dacbiet='Các ô có dấu (*) đỏ như hệ thống ERP (chứng từ nguồn, Khách hàng, Người liên hệ, Ngày dự kiến bắt đầu / kết thúc, cột Hàng '
               'hóa, Tên vật tư, Công phụ tính P3) dù đang chỉ đọc. Bảng I. Tổng công định mức hiện 2 số lẻ cố định.'),
   layout=dict(menu=MENU + ' => Số phiếu giao việc', shot=shot('17_detail'),
               shot_caption='Màn Chi tiết phiếu giao việc (phiếu Chờ thực hiện, có nút Nhập kết quả)',
               note='Trang chi tiết mở trong cùng tab trình duyệt khi bấm Số phiếu giao việc ở danh sách.'),
   extra=[(shot('17_detail_full'), 'Toàn trang chi tiết phiếu giao việc từ hợp đồng'),
          (shot('17b_detail_nkq'), 'Chi tiết phiếu Đang nhập kết quả — nút Xem phiếu nhập kết quả')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', ['- “Chi tiết phiếu giao việc: <mã>”', '- Nhãn trạng thái cùng màu danh sách']),
       ('Khối Thông tin khách hàng', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - <dd/mm/yyyy hh:mm>”.'),
       ('Ô chứng từ nguồn', 'Link', 'Enable', '–', 'Theo dữ liệu',
        ['- Nhãn theo loại: Số hợp đồng / Số phiếu bảo hành / Phiếu yêu cầu lắp đặt, bàn giao + Hợp đồng / Phiếu YC giao việc khác',
         '- Bấm → chi tiết chứng từ, tab mới']),
       ('Khách hàng', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- “Mã KH - Tên khách hàng”.'),
       ('Người liên hệ', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- Người liên hệ của khách.'),
       ('SĐT liên hệ', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- Số điện thoại người liên hệ.'),
       ('Địa chỉ lắp đặt', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- Địa chỉ làm việc.'),
       ('Người yêu cầu', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- Người lập chứng từ nguồn; kèm SĐT người yêu cầu, Phòng yêu cầu.'),
       ('Ngày dự kiến bắt đầu', 'Textbox', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Có dấu (*).'),
       ('Ngày dự kiến kết thúc', 'Textbox', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Có dấu (*).'),
       ('Ghi chú', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '- Khóa ở màn chi tiết.'),
       ('Khối A - công việc chính', 'Table/Grid', 'Read-only', '–', 'Theo loại phiếu',
        ['- A - BẢO HÀNH (phiếu bảo hành)', '- A - DỊCH VỤ SỬA CHỮA BẢO DƯỠNG: I - Dịch vụ sửa chữa, II - Danh mục thiết bị cần bảo dưỡng',
         '- A - Lắp đặt bàn giao', '- A - Dịch vụ đính kèm (giao việc khác)', '- Mỗi bảng có dòng Tổng công định mức']),
       ('Khối B - Danh sách vật tư bán thêm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Chỉ phiếu từ hợp đồng / phiếu bảo hành.'),
       ('Khối CÔNG VIỆC PHỤ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- “B - CÔNG VIỆC PHỤ” (giao việc khác) hoặc “C - CÔNG VIỆC PHỤ”', '- I. Công phụ tính P3; không có nút Thêm dòng']),
       ('Khối TỔNG HỢP', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- I. Tổng công định mức (Công chính, Công phụ, 2 số lẻ)', '- II. Tổng dịch vụ trả tiền', '- III. Tổng hợp vật tư phải giao',
         '- V. Chi phí khác']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc (mục 2.9).'),
       ('Nút Nhập kết quả', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Cùng điều kiện BR-03; bấm → mục 2.6.'),
       ('Nút Xem phiếu nhập kết quả', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Cùng điều kiện BR-04; bấm → mục 2.7.'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Nút đỏ, cùng điều kiện BR-05; bấm → mục 2.8.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Lùi về màn trước (danh sách được giao, giữ bộ lọc).'),
       ('Thông báo lỗi tải', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Không tải được phiếu giao việc.”'),
   ],
   ev=[
       ('Bấm Số phiếu giao việc', 'Click',
        'Before:\n– Ghi nhớ bộ lọc danh sách (10 phút).\nDuring:\n– Chuyển sang trang chi tiết trong cùng tab.\n'
        'After:\n– Bắt đầu nạp dữ liệu phiếu.'),
       ('Mở trang chi tiết', 'System',
        'Before:\n– Kiểm tra người xem: người tạo, người thực hiện hoặc quyền “' + QV + '” theo mức.\n'
        '– Không có quyền / phiếu không có / đã Hủy → chuyển trang 404 và dừng xử lý.\n'
        'During:\n– Nạp thông tin phiếu, chứng từ nguồn, bảng công việc, tổng hợp, cờ hành động.\n– Lỗi khác → “Không tải được phiếu giao việc.”.\n'
        'After:\n– Hiển thị chi tiết chỉ đọc + nút chân trang theo điều kiện.'),
       ('Bấm chứng từ nguồn', 'Click',
        'Before:\n– Ô có liên kết.\nAfter:\n– Mở chi tiết chứng từ ở tab mới; màn chi tiết giữ nguyên.'),
       ('Bấm Quay lại / nút lùi trình duyệt', 'Click',
        'Before:\n– Đi vào từ danh sách thì lùi 1 bước; mở trực tiếp thì về màn Phiếu giao việc.\n'
        'After:\n– Về danh sách, khôi phục bộ lọc (nếu còn trong 10 phút), nạp trang 1.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Nhập kết quả', usecase=('FR-06', 'Nhập kết quả', 'crud', A_TH),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Mở màn Tạo phiếu nhập kết quả cho phiếu giao việc được giao',
       mota='Người thực hiện bấm Nhập kết quả ở cột Hành động (hoặc chân trang chi tiết) để mở màn Tạo phiếu nhập kết quả với phiếu giao '
            'việc chọn sẵn. Màn này chỉ quyết định nút hiện hay không; nội dung, kiểm tra và lưu phiếu nhập kết quả thuộc tài liệu Phiếu '
            'nhập kết quả. Lưu xong, trạng thái phiếu giao việc đổi theo phiếu nhập kết quả và nút Nhập kết quả không hiện nữa.',
       tacnhan='Người dùng có quyền thực hiện chức năng: người thực hiện của phiếu (trưởng nhóm hoặc thành viên); theo thiết kế người có '
               'quyền “%s” cũng được (hiện không có tác dụng — xem Phần 2).' % QN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu ở trạng thái Chờ thực hiện.\n3. Phiếu giao công tác chứa phiếu đã được '
                'duyệt và phiếu có người thực hiện.\n4. Phiếu chưa có phiếu nhập kết quả nào.',
       chinh='1. Người dùng bấm Nhập kết quả (biểu tượng sổ bút) ở dòng phiếu, hoặc nút Nhập kết quả ở chân trang chi tiết.\n'
             '2. Hệ thống mở màn “Tạo phiếu nhập kết quả” trong cùng tab, phiếu giao việc chọn sẵn; bộ lọc danh sách không được giữ.\n'
             '3. Màn Tạo nạp thông tin khách hàng, người thực hiện, chấm công, các dòng công việc từ phiếu giao việc.\n'
             '4. Người dùng nhập kết quả rồi bấm Lưu (nháp) hoặc Lưu và gửi duyệt (đặc tả ở tài liệu Phiếu nhập kết quả).\n'
             '5. Lưu nháp → phiếu giao việc chuyển “Đang nhập kết quả”; gửi duyệt → “Đã nhập kết quả”; hệ thống ghi một dòng lịch sử '
             '“Thay đổi trạng thái” trong lịch sử của phiếu giao việc kèm mã phiếu nhập kết quả.\n'
             '6. Quay lại danh sách: dòng phiếu đổi trạng thái, nút Nhập kết quả được thay bằng Xem phiếu nhập kết quả.',
       phu='• Phiếu chưa đủ điều kiện (chưa lập / chưa duyệt phiếu công tác, đã có phiếu nhập kết quả, trạng thái khác Chờ thực hiện) → '
           'không có nút Nhập kết quả.\n'
           '• Phiếu giao việc không còn tồn tại khi mở màn Tạo → màn Tạo báo “Không tìm thấy phiếu giao việc”.\n'
           '• Ở màn Tạo bấm Quay lại khi đã nhập → hộp cảnh báo chưa lưu của màn Tạo.\n'
           '• Phiếu nhập kết quả bị xóa sau đó → phiếu giao việc về Chờ thực hiện, nút Nhập kết quả hiện lại.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, chuyển về màn đăng nhập.',
       dacbiet='Nút là liên kết thật: chuột phải / chuột giữa mở được ở tab mới. Màn Tạo phiếu nhập kết quả không kiểm lại quyền khi mở '
               '(giữ như hệ thống ERP) — điều kiện nằm ở việc hiện nút.'),
   layout=dict(menu=MENU + ' => Nhập kết quả', shot=shot('40_import_create'),
               shot_caption='Màn Tạo phiếu nhập kết quả mở từ nút Nhập kết quả',
               note='Nút Nhập kết quả nằm ở cột Hành động của danh sách và ở chân trang chi tiết phiếu.'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút Nhập kết quả (dòng)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
        ['- Biểu tượng sổ bút, chú thích “Nhập kết quả”', '- Hiện khi đủ BR-03']),
       ('Nút Nhập kết quả (chi tiết)', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Nút xanh ở chân trang chi tiết, cùng điều kiện.'),
       ('Màn Tạo phiếu nhập kết quả', 'Label', 'Hiển thị', '–', 'Ẩn', '- Tiêu đề “Tạo phiếu nhập kết quả”; mở trong cùng tab.'),
       ('Ô Phiếu giao việc', 'Link', 'Read-only', '–', 'Theo dòng đã bấm', '- Mã phiếu giao việc chọn sẵn, không đổi được.'),
       ('Khối Thông tin khách hàng', 'Label', 'Read-only', '–', 'Theo phiếu giao việc', '- Khách hàng, địa chỉ, người liên hệ, người yêu cầu.'),
       ('Khối Chấm công', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Chấm công theo HRM và điều chỉnh theo thực tế.'),
       ('Khối File ảnh đính kèm', 'Table/Grid', 'Enable', '–', 'Trống', '- Ảnh công trình, ảnh biên bản bàn giao; nút Thêm tài liệu.'),
       ('Nút Lưu', 'Button', 'Enable', '–', 'Hiển thị', '- Lưu nháp phiếu nhập kết quả → phiếu giao việc “Đang nhập kết quả”.'),
       ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', 'Hiển thị', '- Gửi duyệt → phiếu giao việc “Đã nhập kết quả”.'),
       ('Nút Quay lại (màn Tạo)', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn trước; hỏi xác nhận nếu đã nhập.'),
       ('Cột Trạng thái sau khi lưu', 'Badge', 'Read-only', '–', 'Theo dữ liệu', '- Đang nhập kết quả (cam) / Đã nhập kết quả (xanh lá).'),
       ('Cột Hành động sau khi lưu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Ẩn Nhập kết quả, hiện Xem phiếu nhập kết quả.'),
   ],
   ev=[
       ('Mở danh sách / chi tiết', 'System',
        'Before:\n– Tính cờ Nhập kết quả cho từng phiếu.\nDuring:\n– Chưa có phiếu nhập kết quả + Chờ thực hiện + phiếu công tác đã duyệt + '
        'có người thực hiện + mình là người thực hiện (hoặc quyền “' + QN + '”).\nAfter:\n– Hiện / ẩn nút Nhập kết quả.'),
       ('Bấm Nhập kết quả', 'Click',
        'Before:\n– Nút chỉ hiện khi đủ BR-03; không hỏi xác nhận.\nDuring:\n– Bỏ bộ lọc đã ghi nhớ của danh sách.\n'
        'After:\n– Mở màn Tạo phiếu nhập kết quả, phiếu giao việc chọn sẵn.'),
       ('Mở màn Tạo phiếu nhập kết quả', 'System',
        'Before:\n– Không kiểm quyền (giữ như ERP).\nDuring:\n– Phiếu giao việc không tồn tại → “Không tìm thấy phiếu giao việc”.\n' + ERR + '\n'
        'After:\n– Hiển thị form với dữ liệu lấy từ phiếu giao việc.'),
       ('Lưu / Lưu và gửi duyệt phiếu nhập kết quả', 'Click',
        'Before:\n– Kiểm tra theo tài liệu Phiếu nhập kết quả.\nDuring:\n– Lỗi kiểm tra → báo lỗi tại màn Tạo, phiếu giao việc không đổi.\n'
        'After:\n– Phiếu giao việc chuyển Đang nhập kết quả / Đã nhập kết quả.\n– Ghi một dòng lịch sử “Thay đổi trạng thái” trong lịch '
        'sử của phiếu giao việc, kèm “Phiếu nhập kết quả <mã>”.\n– Gửi duyệt: báo người duyệt kết quả.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Xem phiếu nhập kết quả',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Mở chi tiết phiếu nhập kết quả của phiếu giao việc',
       mota='Với phiếu đã có phiếu nhập kết quả và đã rời trạng thái Chờ thực hiện, người dùng bấm Xem phiếu nhập kết quả để mở màn Chi tiết '
            'phiếu nhập kết quả (phiếu lập sớm nhất của phiếu giao việc). Từ đó thao tác Sửa / Xóa / Gửi duyệt theo tài liệu Phiếu nhập kết '
            'quả.',
       tacnhan=TN, dieukien=DK + '\n4. Phiếu giao việc khác Chờ thực hiện và đã có phiếu nhập kết quả.',
       chinh='1. Người dùng bấm Xem phiếu nhập kết quả ở cột Hành động hoặc chân trang chi tiết phiếu giao việc.\n'
             '2. Hệ thống mở trang “Chi tiết phiếu nhập kết quả: <mã>” trong cùng tab.\n'
             '3. Màn chi tiết phiếu nhập kết quả tự kiểm quyền xem của nó và hiển thị dữ liệu chỉ đọc.\n'
             '4. Người dùng bấm Quay lại để trở về.',
       phu='• Phiếu Chờ thực hiện hoặc chưa có phiếu nhập kết quả → không có nút.\n'
           '• Người dùng không có quyền xem phiếu nhập kết quả → màn đích chuyển trang không tìm thấy.\n'
           '• Phiếu nhập kết quả đã bị xóa giữa chừng → màn đích báo không tìm thấy; quay lại danh sách nạp lại cờ.\n'
           '• Rời danh sách sang màn này thì bộ lọc danh sách không được giữ.',
       dacbiet='Nút là liên kết thật, mở được ở tab mới. Trước 03/11/2026 nút mở hệ thống ERP; nay mở màn HRM.'),
   layout=dict(menu=MENU + ' => Xem phiếu nhập kết quả', shot=shot('41_import_show'),
               shot_caption='Màn Chi tiết phiếu nhập kết quả mở từ nút Xem phiếu nhập kết quả',
               note='Nút nằm ở cột Hành động của danh sách và ở chân trang chi tiết phiếu giao việc.'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút Xem phiếu nhập kết quả (dòng)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
        ['- Biểu tượng kính lúp trên tài liệu', '- Hiện khi đủ BR-04']),
       ('Nút Xem phiếu nhập kết quả (chi tiết)', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Nút viền, biểu tượng mắt, cùng điều kiện.'),
       ('Tiêu đề màn đích', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '- “Chi tiết phiếu nhập kết quả: <mã>” + nhãn trạng thái.'),
       ('Ô Phiếu giao việc (màn đích)', 'Link', 'Enable', '–', 'Theo dữ liệu', '- Mã phiếu giao việc, bấm mở lại chi tiết phiếu giao việc.'),
       ('Khối thông tin (màn đích)', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Khách hàng, chấm công, file đính kèm, kết quả.'),
       ('Nút Sửa, Xóa (màn đích)', 'Button', 'Enable / Ẩn', '–', 'Theo màn đích', '- Theo điều kiện của tài liệu Phiếu nhập kết quả.'),
       ('Nút Quay lại (màn đích)', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn trước.'),
       ('Cột Trạng thái phiếu giao việc', 'Badge', 'Read-only', '–', 'Theo dữ liệu', '- Khác Chờ thực hiện khi nút hiện.'),
       ('Trang không tìm thấy', 'Label', 'Hiển thị', '–', 'Ẩn', '- Khi không có quyền / phiếu nhập kết quả không còn.'),
       ('Danh sách sau khi quay lại', 'Table/Grid', 'Read-only', '–', 'Trang 1', '- Bộ lọc về trống.'),
       ('Liên kết mở tab mới', 'Link', 'Enable', '–', '–', '- Chuột phải / chuột giữa trên nút.'),
   ],
   ev=[
       ('Mở danh sách / chi tiết', 'System',
        'Before:\n– Tính cờ cho từng phiếu.\nDuring:\n– Trạng thái khác Chờ thực hiện và Hủy + có phiếu nhập kết quả.\nAfter:\n– Hiện / ẩn nút.'),
       ('Bấm Xem phiếu nhập kết quả', 'Click',
        'Before:\n– Nút chỉ hiện khi đủ BR-04.\nDuring:\n– Bỏ bộ lọc đã ghi nhớ của danh sách.\n'
        'After:\n– Mở chi tiết phiếu nhập kết quả đầu tiên của phiếu.'),
       ('Mở màn đích', 'System',
        'Before:\n– Màn đích kiểm quyền xem phiếu nhập kết quả.\nDuring:\n– Không có quyền / không còn phiếu → trang không tìm thấy.\n'
        'After:\n– Hiển thị chi tiết.'),
       ('Bấm Quay lại ở màn đích', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Về màn trước; danh sách nạp lại từ trang 1.'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'Xóa phiếu giao việc', usecase=('FR-08', 'Xóa phiếu giao việc', 'action', A_TAO),
   rule=('- Quy tắc Xóa.', 'delete'),
   intro=dict(
       ten='Xóa (Hủy) phiếu giao việc Chờ thực hiện chưa gắn phiếu công tác',
       mota='Người tạo phiếu xóa phiếu giao việc của mình khi phiếu còn Chờ thực hiện và chưa gắn phiếu giao công tác. Xóa là chuyển phiếu '
            'sang trạng thái Hủy (không xóa cứng) và trả lại số lượng đã giao cho chứng từ nguồn. Ở màn này nút rất hiếm khi hiện, vì phiếu '
            'chỉ có người thực hiện sau khi phiếu công tác đã duyệt (BR-05).',
       tacnhan='Người dùng có quyền thực hiện chức năng: người tạo phiếu giao việc, đồng thời là người thực hiện (không đặc cách Super admin).',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người đăng nhập là người tạo phiếu.\n3. Phiếu Chờ thực hiện và chưa gắn phiếu '
                'giao công tác.',
       chinh='1. Người dùng bấm Xóa (thùng rác đỏ) ở cột Hành động hoặc nút Xóa ở chân trang chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa”: “Bạn có chắc muốn xóa bản ghi này không?” (từ chi tiết: “Bạn có chắc muốn xóa phiếu '
             'giao việc \'<mã>\'?”).\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm tra người tạo, trạng thái Chờ thực hiện, chưa gắn phiếu công tác; chuyển phiếu sang Hủy.\n'
             '5. Hệ thống trả số lượng cho chứng từ nguồn: xóa tiến độ giao việc; phiếu yêu cầu giao việc khác về Chờ giao việc; phiếu '
             'yêu cầu lắp đặt tính lại trạng thái; phiếu bảo hành bật lại đánh dấu chờ giao.\n'
             '6. Hệ thống ghi một dòng lịch sử “Thay đổi trạng thái: Chờ thực hiện → Hủy”, báo “Xóa thành công.”, nạp lại danh sách '
             '(từ màn chi tiết thì chuyển về màn Phiếu giao việc).',
       phu='• Bấm Hủy / (x) / click ra ngoài hộp → không xóa.\n'
           '• Không phải người tạo → hệ thống từ chối, báo %s.\n'
           '• Phiếu đã đổi trạng thái / đã gắn phiếu công tác → %s; danh sách nạp lại.\n'
           '• Phiếu không còn → “Không tìm thấy phiếu giao việc”.\n'
           '• Lỗi khác → “Xóa không thành công”.\n'
           '• Đang ở dòng cuối của trang > 1 → sau khi xóa lùi 1 trang.' % (NO_DEL, CONFLICT),
       dacbiet='Phiếu Hủy rời khỏi mọi danh sách phiếu giao việc; số lượng trả về Phiếu chờ giao việc. Khóa nút trong lúc đang xóa.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp Xác nhận xóa (cờ Xóa bật trên trình duyệt để minh họa)',
               note='Hộp xác nhận được mở ngay trên màn hình danh sách hoặc màn chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Xóa (dòng)', 'Icon Button', 'Enable / Ẩn', 'Theo điều kiện', ['- Thùng rác đỏ, chú thích “Xóa”', '- Chỉ khi đủ BR-05']),
       ('Nút Xóa (màn chi tiết)', 'Button', 'Enable / Ẩn', 'Theo điều kiện', '- Nút đỏ ở chân trang chi tiết, cùng điều kiện.'),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Ẩn', '- “Xác nhận xóa”.'),
       ('Nội dung hộp', 'Label', 'Hiển thị', 'Ẩn',
        ['- Từ danh sách: “Bạn có chắc muốn xóa bản ghi này không?”', '- Từ chi tiết: “Bạn có chắc muốn xóa phiếu giao việc \'<mã>\'?”']),
       ('Nút Xóa (trong hộp)', 'Button', 'Enable', 'Hiển thị', '- Màu đỏ; thực hiện xóa, khóa nút trong lúc xóa.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không xóa.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- “Xóa thành công.”', '- ' + CONFLICT, '- ' + NO_DEL, '- “Xóa không thành công”']),
       ('Dòng phiếu sau khi xóa', 'Table/Grid', 'Hiển thị', 'Theo dữ liệu', '- Biến mất khỏi danh sách; tổng N giảm 1.'),
       ('Lịch sử phiếu', 'Label', 'Hiển thị', 'Theo dữ liệu', '- Thêm dòng “Thay đổi trạng thái: Chờ thực hiện → Hủy”.'),
       ('Chứng từ nguồn', 'Label', 'Hiển thị', 'Theo dữ liệu', '- Số lượng trả lại, có thể quay lại Phiếu chờ giao việc.'),
   ],
   ev=[
       ('Bấm Xóa', 'Click', 'Before:\n– Nút chỉ hiện khi đủ BR-05.\nAfter:\n– Hiện hộp Xác nhận xóa.'),
       ('Bấm Xóa trong hộp', 'Click',
        'Before:\n– Kiểm tra người đăng nhập là người tạo phiếu; nếu không → hệ thống từ chối, báo ' + NO_DEL + ' và dừng xử lý.\n'
        '– Kiểm tra Chờ thực hiện + chưa gắn phiếu công tác (không → ' + CONFLICT + ').\n'
        'During:\n– Khóa phiếu, chuyển Hủy, xóa tiến độ giao việc, trả trạng thái chứng từ nguồn trong 1 lần.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Thay đổi trạng thái” (Chờ thực hiện → Hủy).\n– Hiển thị “Xóa thành công.”; nạp lại danh sách '
        '/ chuyển về màn Phiếu giao việc.'),
       ('Bấm Hủy / (x) / click ra ngoài hộp', 'Click',
        'Before:\n– Không xóa.\nAfter:\n– Đóng hộp, màn giữ nguyên.'),
       ('Xóa dòng cuối của trang', 'System',
        'Before:\n– Trang hiện tại > 1 và chỉ còn 1 dòng.\nAfter:\n– Lùi 1 trang rồi nạp lại.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu giao việc',
       mota='Xem các mốc thao tác của phiếu: thời điểm, hành động, người thực hiện, giá trị cũ → mới. Phiếu có các loại mốc: “Tạo mới” '
            '(lập phiếu ở HRM) và “Thay đổi trạng thái” (do phiếu nhập kết quả lưu / gửi duyệt / bị xóa / được duyệt, hoặc do Xóa phiếu), '
            'kèm mã phiếu nhập kết quả gây ra. Cửa sổ ở danh sách và khối Lịch sử ở màn chi tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử (biểu tượng đồng hồ) ở cột Hành động, hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n'
             '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <mã>” và nạp các mốc.\n'
             '3. Hệ thống hiển thị các mốc, mới nhất ở trên.',
       phu='• Phiếu lập ở hệ thống ERP / trước khi chuyển sang HRM chưa có mốc → “Chưa có lịch sử thao tác nào.”.\n'
           '• Bấm Bộ lọc → mở các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Xem, lọc, in, xuất Excel không ghi mốc. Màn không có Sửa nên không có mốc “Thay đổi thông tin”.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16c_history_filter'), 'Khối Bộ lọc trong cửa sổ Lịch sử thay đổi'),
          (shot('17c_detail_history'), 'Khối Lịch sử ở màn chi tiết phiếu giao việc')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <mã phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái: “Trạng thái: <cũ> → <mới>” kèm dòng “Phiếu nhập kết quả <mã>” nếu do phiếu nhập kết quả',
           '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách hành động', 'Trống', ['- Gợi ý “Chọn loại hành động”', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', '- Chọn là lọc ngay.'),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc đến hết ngày này.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', '- Xóa điều kiện lọc.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- “Chưa có lịch sử thao tác nào.”', '- “Không có lịch sử phù hợp bộ lọc.”']),
       ('Khối Lịch sử ở màn chi tiết', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc; số mốc trên nhãn.'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Giống nút Đóng.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click',
        'Before:\n– Phiếu đang hiển thị trên danh sách / màn chi tiết.\nDuring:\n– Nạp các mốc của phiếu.\n'
        'After:\n– Hiển thị các mốc, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm: chọn là lọc.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Khối lọc đang mở.\nAfter:\n– Xóa điều kiện lọc, hiện lại đủ các mốc.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; danh sách giữ nguyên trang và bộ lọc.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'In danh sách', usecase=('FR-10', 'In danh sách', 'io', A_TH),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In danh sách phiếu được giao theo bộ lọc',
       mota='Xem trước và in danh sách các phiếu được giao khớp bộ lọc (không phân trang), mẫu “DANH SÁCH PHIẾU GIAO VIỆC”, khổ ngang, '
            'letterhead công ty của người in, có chỗ ký Người lập. Tối đa 2.000 dòng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng lọc danh sách (mục 2.2) rồi bấm In danh sách.\n'
             '2. Hệ thống lấy các phiếu được giao theo bộ lọc + sắp xếp, dựng bản in theo mẫu.\n'
             '3. Hệ thống mở cửa sổ “Xem trước danh sách phiếu giao việc”.\n'
             '4. Người dùng bấm In → hộp thoại in của trình duyệt.',
       phu='• Trên 2.000 dòng → không dựng bản in, ẩn nút In, hiện “Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in '
           'được. Vui lòng thu hẹp bộ lọc …”.\n'
           '• Không có dòng → bản in chỉ có tiêu đề cột.\n'
           '• Thiếu mẫu in → “Không tìm thấy mẫu in \"Danh sách phiếu giao việc\"”.\n'
           '• Bấm (x) / phím Esc → đóng cửa sổ.',
       dacbiet='Cột: STT, Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Người tạo, Người thực hiện, Thời '
               'gian dự kiến, Tổng công định mức (2 số lẻ), Trạng thái, Ngày tạo (kèm giờ). Người lập = người đang in.'),
   layout=dict(menu=MENU + ' => In danh sách', shot=shot('19_printlist'), shot_caption='Cửa sổ Xem trước danh sách phiếu giao việc',
               note='Modal Xem trước được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', '- Thanh công cụ của bảng.'),
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước danh sách phiếu giao việc”.'),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', ['- Nút xanh cạnh tiêu đề', '- Ẩn khi vượt 2.000 dòng']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Letterhead', 'Label', 'Read-only', '–', 'Theo công ty người in', '- Ảnh đầu trang của công ty người đang đăng nhập.'),
       ('Tiêu đề bản in', 'Label', 'Read-only', '–', 'Hiển thị', '- “DANH SÁCH PHIẾU GIAO VIỆC”.'),
       ('Bảng danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc', '- STT + 11 cột như danh sách (trừ Hành động).'),
       ('Cột Tổng công định mức', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '- 2 số lẻ, phân cách hàng nghìn; 0 in “0.00”.'),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- “Ngày ..... Tháng ...... Năm .....”, Người lập + họ tên người in.'),
       ('Dòng nhắc vượt trần', 'Label', 'Hiển thị', '–', 'Ẩn', '- Câu “Danh sách có N dòng, vượt mức in tối đa 2,000 dòng…”.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Không tìm thấy mẫu in \"Danh sách phiếu giao việc\"”.'),
   ],
   ev=[
       ('Bấm In danh sách', 'Click',
        'Before:\n– Áp tập phiếu được giao + bộ lọc + sắp xếp đang có; không kiểm quyền.\n'
        'During:\n– Đếm tổng; > 2.000 → dòng nhắc vượt trần.\n– Thiếu mẫu in → thông báo lỗi.\n' + ERR + '\n'
        'After:\n– Hiển thị bản xem trước danh sách.'),
       ('Bấm In', 'Click', 'Before:\n– Bản in đã dựng.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x) / phím Esc', 'Click', 'Before:\n– Không hỏi.\nAfter:\n– Đóng cửa sổ, danh sách giữ nguyên.'),
       ('Mở cửa sổ', 'System', 'Before:\n– Letterhead theo công ty người in.\nAfter:\n– Hiển thị bản in khổ ngang.'),
   ])

# ------------------------------------------------------------ 2.11
fr(11, 'Xuất Excel danh sách', usecase=('FR-11', 'Xuất Excel danh sách', 'io', A_TH),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu được giao ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ phiếu được giao khớp bộ lọc (không phân trang) ra file Excel. File dựng ngay trên '
            'trình duyệt theo từng đợt dữ liệu, có dòng tiến độ; cột STT luôn đứng đầu; ô Tổng công định mức là ô số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất file” với 11 trường, tích sẵn các trường ứng với cột đang hiện.\n'
             '3. Người dùng tích trường, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy lần lượt toàn bộ phiếu, hiện tiến độ “Đã tải x/y dòng…” rồi “Đang dựng file x/y dòng…”.\n'
             '5. Hệ thống tải file “danh_sach_phieu_giao_viec.xlsx” (tiêu đề “DANH SÁCH PHIẾU GIAO VIỆC”, trang tính “Phiếu giao việc”), '
             'báo “Xuất Excel thành công.”.',
       phu='• Không có phiếu khớp → không tạo file, báo “Không có dữ liệu để xuất”.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng (lấy theo từng đợt 2.000 dòng). Tên file, tiêu đề giống lối vào Phiếu giao việc. Khóa nút Xuất '
               'Excel trong lúc xuất.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất file”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 11 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        '- Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Người tạo, Người thực hiện, Thời gian dự kiến, '
        'Tổng công định mức, Trạng thái, Ngày tạo.'),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/11 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file Excel', '- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Dòng tiến độ', 'Label', 'Read-only', '–', '–', 'Ẩn', ['- “Đang chuẩn bị dữ liệu…”', '- “Đã tải x/y dòng…”', '- “Đang dựng file x/y dòng…”']),
       ('Nội dung file Excel', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Tiêu đề “DANH SÁCH PHIẾU GIAO VIỆC”', '- Dòng tên cột: STT + các trường đã chọn', '- Tổng công định mức là ô số']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Xuất Excel thành công.”', '- “Không có dữ liệu để xuất”', '- “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ, tích sẵn trường ứng với cột đang hiện.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng của trường.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất; dữ liệu là tập phiếu được giao.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc + sắp xếp theo từng đợt, hiện tiến độ.\n– Không có dòng → “Không có dữ liệu để xuất”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.\n' + ERR + '\n'
        'After:\n– Tải file, báo “Xuất Excel thành công.”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu giao việc được giao; không lặp lại các quy tắc đã có trong SRS quy '
           'tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Tập phiếu của màn', [
        '– Phiếu giao việc gốc (không lấy phiếu duyệt kết quả), trạng thái khác Hủy, người đăng nhập có trong danh sách người thực hiện '
        '(trưởng nhóm hoặc thành viên).',
        '– Không xét quyền xem theo cấp, không lọc trạng thái, không lấy phiếu mình tạo mà không thực hiện; không đặc cách Super admin.'],
     ['Xem danh sách', 'Tìm kiếm', 'In', 'Xuất Excel']),
    ('BR-02', 'Nguồn người thực hiện', [
        '– Chỉ Phiếu giao công tác ĐÃ DUYỆT ghi người thực hiện (nhân sự + hệ số công + trưởng nhóm) sang phiếu giao việc, xóa danh '
        'sách cũ rồi ghi lại.',
        '– Form phiếu giao việc không có khối người thực hiện; phiếu chưa có phiếu công tác đã duyệt thì không ai thấy ở màn này.',
        '– Gỡ phiếu khỏi phiếu công tác / xóa phiếu công tác đã duyệt → xóa người thực hiện → phiếu rời màn.'],
     ['Xem danh sách', 'Ràng buộc']),
    ('BR-03', 'Điều kiện Nhập kết quả', [
        '– Chưa có phiếu nhập kết quả nào của phiếu giao việc.',
        '– Trạng thái Chờ thực hiện, phiếu công tác đã duyệt, có người thực hiện.',
        '– Người đăng nhập là người thực hiện, hoặc có quyền “%s” (hiện không có tác dụng ở HRM).' % QN],
     ['Nhập kết quả']),
    ('BR-04', 'Điều kiện Xem phiếu nhập kết quả', [
        '– Trạng thái khác Chờ thực hiện và Hủy, đã có phiếu nhập kết quả; mở phiếu nhập kết quả lập sớm nhất.'],
     ['Xem phiếu nhập kết quả']),
    ('BR-05', 'Điều kiện và tác động Xóa', [
        '– Người tạo phiếu + Chờ thực hiện + chưa gắn phiếu công tác (không đặc cách Super admin).',
        '– Xóa = chuyển Hủy; xóa tiến độ giao việc; yêu cầu giao việc khác về Chờ giao việc; yêu cầu lắp đặt tính lại trạng thái; '
        'phiếu bảo hành bật lại đánh dấu chờ giao.',
        '– Ở màn này hiếm khi hiện vì phiếu có người thực hiện thường đã gắn phiếu công tác đã duyệt.'],
     ['Xóa']),
    ('BR-06', 'Luồng trạng thái', [
        '– Chờ thực hiện → Đang nhập kết quả (lưu nháp phiếu nhập kết quả) → Đã nhập kết quả (gửi duyệt) → Đang duyệt kết quả → Đã '
        'duyệt kết quả → Chờ BKS duyệt kết quả → Đang đề nghị thanh toán → Đã thanh toán.',
        '– Xóa phiếu nhập kết quả → về Chờ thực hiện. Xóa phiếu giao việc → Hủy (rời màn).'],
     ['Xem danh sách', 'Nhập kết quả']),
    ('BR-07', 'Sắp xếp, lọc', [
        '– Mặc định Ngày tạo mới nhất ở trên; sắp được 6 cột (BR trong mục 2.1).',
        '– Thời gian dự kiến: ngày bắt đầu ≥ Từ ngày, ngày kết thúc ≤ Đến ngày.',
        '– Người thực hiện: phiếu có nhân viên đã chọn trong danh sách người thực hiện.'],
     ['Xem danh sách', 'Tìm kiếm']),
    ('BR-08', 'Hiển thị cột', [
        '– Người thực hiện: trưởng nhóm, không có thì người đầu danh sách.',
        '– Người yêu cầu: người lập hợp đồng / phiếu bảo hành → yêu cầu giao việc khác → yêu cầu lắp đặt.',
        '– Tổng công định mức 2 số lẻ; bằng 0 thì để trống trên màn (bản in ghi 0.00).'],
     ['Xem danh sách', 'In', 'Xuất Excel']),
    ('BR-09', 'Quy tắc ghi lịch sử', [
        '– “Tạo mới” khi lập phiếu ở HRM.',
        '– “Thay đổi trạng thái” khi phiếu nhập kết quả lưu / gửi duyệt / bị xóa / được duyệt (kèm mã phiếu nhập kết quả) và khi Xóa.',
        '– Xem, lọc, in, xuất không ghi mốc; phiếu lập ở ERP không có mốc cũ.'],
     ['Lịch sử', 'Xóa', 'Nhập kết quả']),
    ('BR-10', 'In, xuất', [
        '– In tối đa 2.000 dòng, vượt thì chặn và nhắc thu hẹp bộ lọc; letterhead công ty người in.',
        '– Xuất Excel không giới hạn dòng, xuất rỗng không ra file.'],
     ['In danh sách', 'Xuất Excel']),
    ('BR-11', 'Ghi nhớ theo lối vào', [
        '– Bộ lọc ghi nhớ 10 phút trên trình duyệt, chỉ khi mở chi tiết rồi quay lại; sang màn khác thì xóa.',
        '– Bộ lọc, cấu hình cột, cài đặt bộ lọc của lối vào này tách riêng với lối vào Phiếu giao việc.'],
     ['Tìm kiếm', 'Tùy chỉnh cột', 'Cài đặt bộ lọc']),
    ('BR-12', 'Duy nhất, chuẩn hóa nhập', [
        '– Màn không tạo / sửa bản ghi nên không có quy tắc trùng; mã phiếu do màn Phiếu chờ giao việc sinh.',
        '– Ô tìm / lọc chữ bỏ khoảng trắng đầu / cuối.'],
     ['Tìm kiếm']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Phiếu giao việc được giao (người thực hiện, trạng thái phiếu, phiếu nhập kết '
    'quả, chứng từ nguồn).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'CSKH sau bán', 'Phiếu chờ giao việc (lập phiếu giao việc; nhận lại số lượng khi phiếu bị Xóa)', 'CSKH sau bán -> Giao việc'),
    ('2', 'CSKH sau bán', 'Phiếu giao việc (cùng dữ liệu, lối vào theo phạm vi quyền xem; dùng chung màn chi tiết)', 'CSKH sau bán -> Giao việc'),
    ('3', 'Công việc', 'Phiếu giao công tác (chọn phiếu giao việc; khi duyệt ghi người thực hiện + cờ đã duyệt; gỡ phiếu thì xóa người '
                       'thực hiện)', 'Công việc -> Phân công công việc'),
    ('4', 'CSKH sau bán', 'Phiếu nhập kết quả (đích của Nhập kết quả / Xem phiếu nhập kết quả; lưu, gửi duyệt, xóa, duyệt đổi trạng thái '
                          'phiếu giao việc và ghi lịch sử)', 'CSKH sau bán -> Giao việc'),
    ('5', 'Bán hàng', 'Danh sách hợp đồng dịch vụ (Số hợp đồng mở chi tiết; người lập là Người yêu cầu)',
     'Bán hàng -> Bán dịch vụ -> HĐ Sửa chữa - Bảo dưỡng - Bảo trì'),
    ('6', 'CSKH sau bán', 'Phiếu bảo hành (Số hợp đồng của phiếu bảo hành mở chi tiết; đánh dấu chờ giao bật lại khi Xóa)',
     'CSKH sau bán -> Kiểm tra bảo hành sửa chữa'),
    ('7', 'Bán hàng', 'YC lắp đặt, bàn giao (Số phiếu yêu cầu mở chi tiết; trạng thái tính lại khi Xóa)', 'Bán hàng -> Yêu cầu -> Lắp đặt - BH - SC'),
    ('8', 'Bán hàng', 'YC giao việc khác (Số phiếu yêu cầu mở chi tiết; về Chờ giao việc khi Xóa)', 'Bán hàng -> Yêu cầu -> Lắp đặt - BH - SC'),
    ('9', 'Hệ thống ERP', 'Hợp đồng bán hàng hãng (Số hợp đồng của phiếu lắp đặt) và các bước Chờ BKS duyệt kết quả, đề nghị thanh toán '
                          '(đổi trạng thái phiếu giao việc)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
