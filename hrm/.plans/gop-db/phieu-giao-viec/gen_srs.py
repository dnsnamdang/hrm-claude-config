# -*- coding: utf-8 -*-
"""SRS màn "Phiếu giao việc" (phân hệ CSKH sau bán › Giao việc, lối vào ?type=all) — form chuẩn SRS_MAU (19/11/2026).

Chạy: python gen_srs.py  -> "SRS - Phiếu giao việc.docx" (SrsDoc.save() tự chạy srs_selfcheck).
Khuôn: gen_srs_duoc_giao.py (bộ anh em "Phiếu giao việc được giao", 18/11 — KHÔNG sửa / không chạy lại) + ../phieu-cho-giao-viec/gen_srs.py.
Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn.
Nguồn đọc 19/11/2026 (nhánh develop cả 2 repo, con của gop_db):
  BE  Modules/CustomerCare/Services/WrAssignTaskService.php (applyScope nhánh all, filteredQuery, SORTABLE, actionFlags, canImportResult,
      canDelete, canView, show, delete, totals, meta scope), WrAssignTaskSourceService (dữ liệu nguồn + quyền theo loại chứng từ),
      WrAssignTaskStoreService (lưu, mã phiếu, tiến độ, đổi trạng thái chứng từ nguồn, lịch sử Tạo mới), WrAssignTaskRemainingService (SL còn),
      Http/Requests/WrAssignTask/WrAssignTaskStoreRequest.php, Http/Controllers/V1/WrAssignTaskController.php, Routes/api.php (POST chỉ gắn
      dueConfig:Tạo phiếu giao việc,manager), Modules/Finance/Http/Middleware/CheckDueConfig + DueConfigBlockService (câu chặn),
      Modules/Assign/Services/WaitingAssignTaskService::checkCreate (PL giảm chờ duyệt), app/Support/Permissions/Catalog/customer_care.php.
  FE  pages/customer-care/wr-assign-tasks/{index.vue, create.vue, _id/index.vue, components/*} (form + 8 bảng con, wrAssignTaskCalc.js,
      wrAssignTaskLinks.js), utils/mixins/unsavedChangesMixin.js, components/subsystem-menu/customer-care.js (nhóm "Giao việc"),
      waiting-assign-tasks (nút Tạo phiếu giao việc), assembly-requests / assign-other-requests (nút Tạo phiếu giao việc, tab mới).
  Bối cảnh: design.md, plan.md (#11978, #11980, #11984, #11988, #11991, #11998, #12138, Check 06/11–11/11), spec mục 8.
Ảnh: ./pgv_shots — dev-hrm 19/11/2026 (_capture/capture.js, DNS Admin, chặn mọi yêu cầu ghi). GIẢ TRẠNG THÁI: form Tạo từ hợp đồng /
  YC lắp đặt / YC giao việc khác (dữ liệu nguồn giả bằng chi tiết phiếu thật cùng loại — DNS Admin không thuộc phòng tiếp nhận), ảnh lỗi kiểm
  tra 42_validate (gán câu lỗi đúng code) và hộp Xác nhận lưu & duyệt 43_confirm_save. Form Tạo từ phiếu bảo hành, nút Xóa là dữ liệu thật.
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

TEN = 'Phiếu giao việc'
SHOTS = os.path.join(HERE, 'pgv_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ CSKH sau bán => Giao việc => Phiếu giao việc'
MENU_CHO = 'Phân hệ CSKH sau bán => Giao việc => Phiếu chờ giao việc'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu giao việc.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
QV = 'Xem phiếu giao việc'
QT = 'Tạo phiếu giao việc'
QN = 'Nhập kết quả thực hiện'
A_QL = 'Người quản lý (quyền Xem phiếu giao việc)'
A_LAP = 'Người lập phiếu (phòng tiếp nhận)'
A_TH = 'Người thực hiện'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người đăng nhập (màn không gắn quyền khi mở); tập phiếu thấy được theo quyền '
      '“%s” (Tổng công ty / Công ty / Phòng ban) hoặc theo vai trò người tạo / người thực hiện.' % QV)
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Phiếu giao việc.\n'
      '3. Danh sách có ít nhất 1 phiếu trong phạm vi được xem.')
EMPTY = '“Không có dữ liệu phù hợp.”'
LOAD_ERR = '“Lỗi khi tải dữ liệu”'
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NO_DEL = '“Bạn không có quyền xóa phiếu giao việc này”'
NO_PERM = '“Không có quyền!”'
REQ = '“Bắt buộc phải nhập”'
MAXV = '“Giá trị nhập vào không được vượt quá N.”'
MSG_START = '“Ngày bắt đầu phải lớn hơn hoặc bằng ngày hiện tại”'
MSG_END = '“Ngày kết thúc phải lớn hơn hoặc bằng ngày hiện tại và ngày bắt đầu”'

d = SrsDoc(out=OUT, menu=MENU, route='/customer-care/wr-assign-tasks', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ CSKH sau bán': 'menu_phanhe', 'Giao việc': 'menu_nhom', 'Phiếu giao việc': 'menu_muc',
    'Phiếu chờ giao việc': 'menu_muc_cho', 'Tạo phiếu giao việc': 'btn_taopgv_row',
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
            if m:
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu giao việc (phân hệ CSKH sau bán, nhóm Giao việc) — màn QUẢN LÝ phiếu giao '
    'việc cho kỹ thuật: lập phiếu từ chứng từ chờ giao việc, xem danh sách theo phạm vi quyền, xem chi tiết, xóa (hủy) phiếu, theo dõi '
    'kết quả thực hiện, in và xuất danh sách, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ phạm vi dữ liệu theo quyền “Xem phiếu giao việc” 3 mức (Tổng công ty / Công ty / Phòng ban) và trường hợp không có quyền '
    '(phiếu mình tạo, cộng phiếu mình là người thực hiện nếu có).',
    'Làm rõ chức năng Tạo phiếu giao việc từ 5 loại chứng từ nguồn (hợp đồng dịch vụ, phụ lục bổ sung, phiếu bảo hành, phiếu yêu cầu lắp '
    'đặt bàn giao, phiếu yêu cầu giao việc khác): điều kiện được tạo, từng trường, số lượng còn giao, công thức tổng công định mức, '
    'tác động lên chứng từ nguồn khi lưu và khi xóa.',
    'Làm rõ các hành động trên từng phiếu: Xem chi tiết, Nhập kết quả, Xem phiếu nhập kết quả, Xóa (Hủy), Xem lịch sử thay đổi.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo phiếu giao việc (lưu là duyệt luôn), Xem chi '
    'tiết, Xóa phiếu giao việc, Xem lịch sử thay đổi, Nhập kết quả, Xem phiếu nhập kết quả, In danh sách, Xuất Excel danh sách. Màn '
    'KHÔNG có nút Thêm mới trên danh sách (phiếu lập từ chứng từ nguồn), KHÔNG có Chỉnh sửa (giữ như hệ thống ERP — không có lối vào '
    'Sửa), KHÔNG có Lưu nháp / Lưu và tiếp tục, Khóa / Mở khóa, Gửi duyệt, Duyệt / Không duyệt riêng, In phiếu, Import. Cùng đường dẫn '
    'với màn “Phiếu giao việc được giao” (hộp việc của người thực hiện — tài liệu riêng) nhưng khác tập phiếu; bộ lọc, cấu hình cột, '
    'cài đặt bộ lọc của 2 lối vào lưu riêng.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phòng tiếp nhận lập phiếu giao việc cho phần việc còn lại của chứng từ nguồn (giao một phần hoặc toàn bộ số lượng còn).',
    'Lãnh đạo / quản lý theo dõi phiếu giao việc theo công ty, phòng ban, trạng thái, thời gian dự kiến, tổng công định mức.',
    'Phiếu giao việc là đầu vào của Phiếu giao công tác (phân công nhân sự), Phiếu nhập kết quả và các báo cáo theo dõi lắp đặt – bàn '
    'giao – sửa chữa – bảo dưỡng.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Phạm vi danh sách theo quyền Xem 3 mức; không có quyền thì chỉ phiếu mình tạo (cộng phiếu mình thực hiện nếu là người thực hiện ở '
    'ít nhất 1 phiếu) (BR-01).',
    'Phiếu chỉ lập từ chứng từ nguồn còn số lượng chưa giao; số lượng giao lần này không vượt số lượng còn (BR-03, BR-04).',
    'Lưu là duyệt luôn: phiếu vào trạng thái Chờ thực hiện, chứng từ nguồn bị trừ số lượng / đổi trạng thái ngay (BR-05).',
    'Xóa chỉ khi mình là người tạo, phiếu Chờ thực hiện và chưa gắn phiếu giao công tác; xóa = chuyển Hủy và trả số lượng về nguồn (BR-08).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu giao việc (PGV)', 'Chứng từ giao việc cho kỹ thuật, mã <mã công ty người lập>.PGV.<năm><6 số>, vd TPE.PGV.2026018712.'),
    ('Chứng từ nguồn', 'Chứng từ sinh ra việc cần giao: hợp đồng dịch vụ, phụ lục bổ sung, phiếu bảo hành, phiếu yêu cầu lắp đặt bàn giao, '
                       'phiếu yêu cầu giao việc khác. Mỗi phiếu giao việc gắn đúng 1 chứng từ nguồn.'),
    ('Phiếu chờ giao việc', 'Màn liệt kê chứng từ nguồn còn số lượng chưa giao (5 tab) — nơi bấm Tạo phiếu giao việc.'),
    ('Phòng tiếp nhận', 'Phòng ban được ghi trên chứng từ nguồn là nơi xử lý; người lập phiếu phải thuộc phòng này (trừ phiếu bảo hành).'),
    ('SL còn (SL còn trên hợp đồng)', 'Số lượng kỹ thuật trên chứng từ − số lượng phụ lục giảm − số lượng đã ghi nhận giao việc / đã hoàn thành.'),
    ('SL giao lần này', 'Số lượng giao trong phiếu này; mặc định bằng SL còn (vật tư bán thêm mặc định 0), không vượt SL còn.'),
    ('Định mức công (ĐM công)', 'Số công chuẩn của 1 dòng việc; thiết bị lấy theo lỗi thiết bị, dịch vụ bảo dưỡng theo gói / cấp dịch vụ.'),
    ('Công chính / Công phụ', 'Công chính = công bảo hành + sửa chữa + bảo dưỡng + lắp đặt + dịch vụ đính kèm; Công phụ = công phụ tính P3.'),
    ('Tổng công định mức', 'Công chính + Công phụ của phiếu (2 số lẻ).'),
    ('Phiếu giao công tác (PCT)', 'Chứng từ phân công nhân sự (phân hệ Công việc); khi duyệt thì ghi người thực hiện cho phiếu giao việc.'),
    ('Người thực hiện', 'Nhân sự đi làm phiếu (trưởng nhóm / thành viên), do phiếu giao công tác đã duyệt ghi sang.'),
    ('Phiếu nhập kết quả (PNKQ)', 'Chứng từ ghi kết quả thực hiện của phiếu giao việc.'),
    ('Trạng thái Chờ thực hiện', 'Nhãn cam: phiếu vừa lưu (lưu là duyệt) — trạng thái duy nhất được Xóa, Nhập kết quả.'),
    ('Trạng thái Đang nhập kết quả / Đã nhập kết quả', 'Nhãn cam / xanh lá: phiếu nhập kết quả đã lưu nháp / đã gửi duyệt.'),
    ('Trạng thái Đang duyệt kết quả / Đã duyệt kết quả', 'Nhãn cam / xanh lá: kết quả đang duyệt / đã duyệt.'),
    ('Trạng thái Chờ BKS duyệt kết quả / Đang đề nghị thanh toán / Đã thanh toán', 'Các bước sau duyệt kết quả (cam / cam / xanh lá).'),
    ('Trạng thái Hủy', 'Phiếu đã bị xóa — không hiện ở danh sách, không mở được chi tiết.'),
    ('Cấu trúc phân cấp', 'Chứng từ nguồn > phiếu giao việc > (thiết bị > công tháo lắp / dịch vụ / vật tư); phiếu giao việc > phiếu giao '
                          'công tác > người thực hiện; phiếu giao việc > phiếu nhập kết quả.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền ở menu và không chặn quyền khi mở (giữ như ERP): ai đăng nhập cũng vào được, dữ liệu theo phạm vi dưới đây. Các '
    'mã quyền: customer_care.phieu_giao_viec.view (“%s”, 3 mức Phòng ban / Công ty / Tổng công ty), customer_care.phieu_giao_viec.create '
    '(“%s”), customer_care.phieu_nhap_ket_qua.create (“%s”). Quyền tính theo công ty đang làm việc; KHÔNG có đặc cách Super admin.'
    % (QV, QT, QN))
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', QT, 'Bắt buộc khi lập phiếu từ hợp đồng / phụ lục bổ sung / phiếu bảo hành (cùng điều kiện phòng tiếp nhận với hợp đồng, phụ '
               'lục). Lập từ yêu cầu lắp đặt / yêu cầu giao việc khác KHÔNG cần Q1 (chỉ cần đúng phòng tiếp nhận) — giữ như ERP.'),
    ('Q2', QN, 'Theo thiết kế (y ERP): cho Nhập kết quả phiếu mình không thực hiện và mở rộng danh sách sang phiếu có người thực hiện. '
               'Lưu ý: hệ thống HRM hiện tra quyền này theo tên cũ mà quyền chỉ khai cho ERP → luôn “không có”.'),
    ('—', 'Người tạo phiếu', 'Không phải quyền: điều kiện của nút Xóa (cùng trạng thái Chờ thực hiện, chưa gắn phiếu giao công tác).'),
    ('—', 'Người thực hiện', 'Không phải quyền: người thực hiện thấy phiếu mình thực hiện và được Nhập kết quả khi đủ điều kiện.'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (một mã Xem, 3 mức):')
d.table(['Ký hiệu', 'Quyền – mức phạm vi', 'Phạm vi dữ liệu'], [
    ('V1', QV + ' – Tổng công ty', 'Mọi phiếu giao việc của mọi công ty; có ô lọc Công ty và Phòng ban.'),
    ('V2', QV + ' – Công ty', 'Phiếu thuộc công ty đang làm việc (công ty của người lập phiếu) + phiếu mình tạo; có ô lọc Phòng ban.'),
    ('V3', QV + ' – Phòng ban', 'Phiếu thuộc các phòng mình quản lý (trong công ty đang làm việc) + phiếu mình tạo; có ô lọc Phòng ban.'),
    ('—', 'Không có quyền Xem', 'Là người thực hiện ở ít nhất 1 phiếu: phiếu mình thực hiện + phiếu mình tạo; còn lại: chỉ phiếu mình '
                                'tạo. Không có ô lọc Công ty – Phòng ban.'),
], widths=[0.8, 2.2, 3.0])
d.p('Có nhiều mức cùng lúc thì áp mức rộng nhất (Tổng công ty > Công ty > Phòng ban).')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không quyền Xem', 'Q1 + phòng tiếp nhận', 'Người thực hiện'], [
    ('FR-01 Xem danh sách', '✅ mọi phiếu', '✅ công ty + mình tạo', '✅ phòng quản lý + mình tạo', '✅ mình tạo (+ mình thực hiện)', '—', '—'),
    ('FR-02 Tìm kiếm và lọc', '✅ + Công ty, Phòng ban', '✅ + Phòng ban', '✅ + Phòng ban', '✅', '—', '—'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '—', '—'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '✅', '✅', '—', '—'),
    ('FR-05 Tạo phiếu giao việc', '—', '—', '—', '✅ từ YC lắp đặt / giao việc khác đúng phòng', '✅ mọi nguồn', '—'),
    ('FR-06 Xem chi tiết', '✅', '✅ theo mức', '✅ theo mức', '✅ mình tạo / thực hiện', '—', '✅'),
    ('FR-07 Xóa', '❌ (trừ người tạo)', '❌ (trừ người tạo)', '❌ (trừ người tạo)', '✅ người tạo khi đủ BR-08', '—', '❌'),
    ('FR-08 Xem lịch sử', '✅', '✅', '✅', '✅', '—', '✅'),
    ('FR-09 Nhập kết quả', '❌ (trừ người thực hiện)', '❌', '❌', '❌', '—', '✅ khi đủ BR-10'),
    ('FR-10 Xem phiếu nhập kết quả', '✅ khi đủ BR-11', '✅', '✅', '✅', '—', '✅'),
    ('FR-11 In danh sách', '✅', '✅', '✅', '✅', '—', '—'),
    ('FR-12 Xuất Excel danh sách', '✅', '✅', '✅', '✅', '—', '—'),
    ('Sửa / Khóa / Duyệt riêng / Import', '—', '—', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.35, 0.85, 0.8, 0.8, 1.0, 0.8, 0.7])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có quyền Xem, không tạo phiếu nào, không là người thực hiện phiếu nào → danh sách “Không có dữ liệu phù hợp.”.',
    'Mở thẳng chi tiết phiếu ngoài phạm vi (không phải người tạo / người thực hiện, không có quyền theo mức) → chuyển trang 404.',
    'Bấm Tạo phiếu giao việc khi không có Q1 (nguồn hợp đồng / phụ lục / phiếu bảo hành) hoặc không thuộc phòng tiếp nhận → thông '
    'báo %s, quay lại màn Phiếu chờ giao việc.' % NO_PERM,
    'Trưởng phòng mà phòng mình quản lý có nhân viên còn hàng giữ / hàng mượn / hàng nhập thẳng quá hạn → bị chặn khi Lưu và duyệt, báo '
    '“Phòng ban bạn quản lý có nhân viên … quá hạn. Không thể thực hiện thao tác này.”.',
    'Gọi Xóa khi không phải người tạo → hệ thống từ chối, báo %s.' % NO_DEL,
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Ô lọc Công ty', 'Có V1', 'Ô Phòng ban: có V1, V2 hoặc V3'),
    ('Nút Tạo phiếu giao việc (màn Phiếu chờ giao việc)', 'HĐ / PL: Q1 + đúng phòng tiếp nhận; LĐ / GVK: đúng phòng tiếp nhận; BH: luôn '
                                                         'hiện', 'Danh sách Phiếu giao việc không có nút Tạo mới'),
    ('Nhập kết quả', 'Chưa có phiếu nhập kết quả + Chờ thực hiện + phiếu giao công tác đã duyệt + có người thực hiện + mình là người '
                     'thực hiện (hoặc Q2)', 'Mở màn Tạo phiếu nhập kết quả'),
    ('Xem phiếu nhập kết quả', 'Trạng thái khác Chờ thực hiện + đã có phiếu nhập kết quả', 'Mở phiếu nhập kết quả lập sớm nhất'),
    ('Xóa', 'Mình là người tạo + Chờ thực hiện + chưa gắn phiếu giao công tác', 'Không đặc cách Super admin'),
    ('Lịch sử, In danh sách, Xuất Excel, Cấu hình cột, Cài đặt bộ lọc', 'Luôn hiện', 'Dữ liệu = phạm vi của người dùng'),
], widths=[1.9, 2.6, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_QL, [0, 4, 5]), (A_LAP, [1, 2]), (A_TH, [3])],
    [('FR-01', 'Xem danh sách phiếu giao việc', 'view'),
     ('FR-05', 'Tạo phiếu giao việc', 'crud'),
     ('FR-07', 'Xóa phiếu giao việc', 'action'),
     ('FR-09', 'Nhập kết quả', 'crud'),
     ('FR-11', 'In danh sách', 'io'),
     ('FR-12', 'Xuất Excel danh sách', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết phiếu giao việc', 'view', 'extend', [0], None),
     ('FR-08', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-10', 'Xem phiếu nhập kết quả', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu giao việc')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu giao việc',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu giao việc theo phạm vi quyền',
       mota='Hiển thị các phiếu giao việc gốc chưa Hủy trong phạm vi của người đăng nhập (quyền “%s” 3 mức; không có quyền thì phiếu '
            'mình tạo, cộng phiếu mình thực hiện), ở mọi trạng thái từ Chờ thực hiện đến Đã thanh toán. Bảng 13 cột, cột Hành động tính '
            'nút theo từng dòng; bộ lọc, cấu hình cột lưu riêng cho lối vào này. Danh sách không có nút Tạo mới: phiếu lập từ màn Phiếu chờ '
            'giao việc (mục 2.5).' % QV,
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để mở màn; dữ liệu giới hạn theo phạm vi quyền.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống đặt tiêu đề trang “Phiếu giao việc”, khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút) và cấu hình cột đã lưu '
             'của người dùng cho lối vào này.\n'
             '3. Hệ thống đọc quyền Xem theo mức của người dùng ở công ty đang làm việc để xác định phạm vi và hiện ô lọc Công ty / Phòng ban.\n'
             '4. Hệ thống lấy phiếu giao việc gốc, trạng thái khác Hủy, trong phạm vi, khớp bộ lọc; sắp Ngày tạo mới nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, tiêu đề bảng “Phiếu giao việc”, dòng “Hiển thị a–b / N” và phân trang.\n'
             '6. Với từng dòng, hệ thống tính các nút ở cột Hành động: Nhập kết quả (BR-10), Xóa (BR-08), Xem phiếu nhập kết quả (BR-11), '
             'Lịch sử (luôn có).\n'
             '7. Người dùng bấm Số phiếu giao việc để mở chi tiết (mục 2.6), bấm Số hợp đồng / Số phiếu yêu cầu để mở chứng từ nguồn ở '
             'tab trình duyệt mới.',
       phu='• Không có phiếu trong phạm vi / không khớp bộ lọc → bảng hiện %s, chân bảng “Không có phiếu nào.”.\n'
           '• Máy chủ lỗi khi nạp → thông báo %s, bảng trống.\n'
           '• Đang ở màn mà bấm mục menu “Phiếu giao việc được giao” → hệ thống bỏ bộ lọc của lối vào này, nạp tập phiếu mình thực hiện '
           '(màn khác, tài liệu riêng); bấm lại “Phiếu giao việc” thì quay về phạm vi quyền.\n'
           '• Vừa tạo phiếu ở màn Tạo → quay về danh sách, phiếu mới ở dòng đầu (Ngày tạo mới nhất).\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, chuyển về màn đăng nhập.' % (EMPTY, LOAD_ERR),
       dacbiet='Cột mặc định hiện: tất cả 13 cột. Cột khóa: STT, Số phiếu giao việc, Hành động. Sắp xếp được: Số phiếu giao việc, Số '
               'hợp đồng, Số phiếu yêu cầu, Thời gian dự kiến (theo ngày bắt đầu), Tổng công định mức, Ngày tạo; mặc định Ngày tạo mới '
               'nhất. Mỗi trang tối đa 100 dòng. Không có nút Tạo mới / Import trên danh sách.'),
   layout=dict(entries=[
       (MENU, 'Lối vào chính. Hiển thị: phiếu giao việc theo phạm vi quyền Xem. Cùng nhóm có mục “Phiếu giao việc được giao” — cùng màn '
              'nhưng chỉ phiếu mình là người thực hiện (tài liệu riêng).'),
       ('', 'Lối vào khác: sau khi Lưu và duyệt ở màn Tạo phiếu giao việc; nút Xóa / Quay lại ở màn chi tiết khi mở chi tiết trực tiếp.')],
       shot=shot('01_list'), shot_caption='Màn Phiếu giao việc (DNS Admin — quyền Tổng công ty)'),
   extra=[(shot('00_menu'), 'Mục Phiếu giao việc trong nhóm Giao việc (phân hệ CSKH sau bán)'),
          (shot('03_empty'), 'Trạng thái không có dữ liệu phù hợp')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Phiếu giao việc” trên thanh đầu trang và tab trình duyệt.'),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Phiếu giao việc”.'),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.11).'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.12)', '- Khóa khi đang xuất']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa, cố định khi cuộn ngang']),
       ('Cột Số phiếu giao việc', 'Link', 'Enable', '–', 'Hiển thị',
        ['- Bấm → mở màn Chi tiết phiếu giao việc trong cùng tab (mục 2.6)', '- Chuột phải / chuột giữa mở được tab mới',
         '- Sắp xếp được; cột khóa, cố định khi cuộn ngang']),
       ('Cột Số hợp đồng', 'Link', 'Enable', '–', 'Hiển thị',
        ['- Phiếu từ hợp đồng / phụ lục: bấm → chi tiết hợp đồng dịch vụ, tab mới',
         '- Phiếu từ phiếu bảo hành: hiện mã phiếu bảo hành, bấm → chi tiết phiếu bảo hành, tab mới',
         '- Phiếu lắp đặt: số hợp đồng bán, bấm → hợp đồng HRM hoặc hợp đồng bán ở hệ thống ERP (chưa chuyển), tab mới',
         '- Phiếu giao việc khác: trống', '- Số dài tự xuống dòng; sắp xếp được']),
       ('Cột Số phiếu yêu cầu', 'Link', 'Enable', '–', 'Hiển thị',
        ['- Phiếu yêu cầu lắp đặt bàn giao hoặc phiếu yêu cầu giao việc khác; bấm → chi tiết phiếu yêu cầu, tab mới',
         '- Trống với phiếu từ hợp đồng / bảo hành', '- Sắp xếp được']),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Dạng “Mã KH-Tên khách hàng”', '- Tối đa 2 dòng']),
       ('Cột Người yêu cầu', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Người lập chứng từ nguồn, dạng “Họ tên - SĐT”', '- Thứ tự lấy: hợp đồng / bảo hành → yêu cầu giao việc khác → yêu cầu lắp đặt']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Người lập phiếu giao việc, dạng “Họ tên - SĐT”.'),
       ('Cột Người thực hiện', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Trưởng nhóm; không có trưởng nhóm thì người đầu danh sách', '- Trống khi chưa có phiếu giao công tác đã duyệt']),
       ('Cột Thời gian dự kiến', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Hiển thị',
        ['- “Ngày bắt đầu-Ngày kết thúc”', '- Sắp xếp theo ngày bắt đầu']),
       ('Cột Tổng công định mức', 'Table/Grid', 'Read-only', '≥ 0', 'Hiển thị',
        ['- 2 số lẻ, phân cách hàng nghìn bằng dấu phẩy (vd 120,000.00)', '- Bằng 0 thì để trống', '- Sắp xếp được']),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 8 giá trị', 'Hiển thị',
        ['- Nhãn cam: Chờ thực hiện, Đang nhập kết quả, Đang duyệt kết quả, Chờ BKS duyệt kết quả, Đang đề nghị thanh toán',
         '- Nhãn xanh lá: Đã nhập kết quả, Đã duyệt kết quả, Đã thanh toán', '- Không sắp xếp']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Sắp xếp được; mặc định mới nhất ở trên.'),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Nhập kết quả (biểu tượng sổ bút) → mục 2.9', '- Xóa (thùng rác đỏ) → mục 2.7',
           '- Xem phiếu nhập kết quả (kính lúp trên tài liệu) → mục 2.10', '- Lịch sử (đồng hồ) → mục 2.8',
           '- Nút không đủ điều kiện thì ẩn; cột khóa']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Giữa bảng: “Không có dữ liệu phù hợp.” khi N = 0', '- Chân bảng: “Không có phiếu nào.”']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang', '- N: tổng số phiếu trong phạm vi khớp bộ lọc']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Trang đầu: về đầu / lùi mờ; trang cuối: tiến / về cuối mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Lỗi khi tải dữ liệu” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định lối vào “Phiếu giao việc”; không chặn quyền khi mở.\n– Khôi phục bộ lọc (10 phút) và cấu hình cột của lối vào.\n'
        '– Đọc quyền Xem theo mức → phạm vi + ô lọc Công ty / Phòng ban.\n'
        'During:\n– Lấy phiếu gốc, khác Hủy, trong phạm vi, khớp bộ lọc; tính cờ nút từng dòng.\n'
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
        'After:\n– Mở chi tiết chứng từ ở tab trình duyệt mới (hợp đồng bán hãng mở hệ thống ERP); danh sách giữ nguyên.'),
       ('Bấm mục menu “Phiếu giao việc được giao” khi đang ở màn', 'Click',
        'Before:\n– Cùng màn, khác lối vào.\nDuring:\n– Xóa bộ lọc đã ghi nhớ của lối vào Phiếu giao việc.\n'
        'After:\n– Nạp bộ lọc, cấu hình cột của lối vào được giao và tập phiếu mình thực hiện.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu giao việc',
       mota='Thu hẹp danh sách trong phạm vi quyền. Ô tìm nhanh tìm theo số phiếu giao việc; khối Tìm kiếm nâng cao có ô Công ty – Phòng '
            'ban (chỉ khi có quyền Xem theo mức, yêu cầu #11984 — ERP không có) và 8 ô: Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người '
            'yêu cầu, Trạng thái, Người tạo, Người thực hiện, Thời gian dự kiến; bật / tắt bằng Cài đặt bộ lọc. Mọi điều kiện chỉ lọc TRONG '
            'phạm vi quyền, không mở rộng phạm vi.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập số phiếu giao việc vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Ô chọn (Công ty, Phòng ban, Khách hàng, Người yêu cầu, Trạng thái, Người tạo, Người thực hiện, Thời gian dự kiến) lọc ngay '
             'khi đổi; ô gõ chữ (Số hợp đồng, Số phiếu yêu cầu) lọc khi bấm Tìm kiếm / nhấn Enter; về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Khi người dùng mở chi tiết phiếu, hệ thống ghi nhớ bộ lọc 10 phút để khôi phục lúc quay lại.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện %s.\n'
           '• Đổi Công ty → ô Phòng ban được xóa giá trị, danh sách phòng theo công ty mới.\n'
           '• Ô Khách hàng: gõ tối thiểu 2 ký tự mới hiện gợi ý (tối đa 30, toàn bộ danh mục khách hàng).\n'
           '• Sang màn khác (Nhập kết quả, Xem phiếu nhập kết quả, menu khác) → bộ lọc bị xóa; quay lại màn là danh sách đầy đủ.' % EMPTY,
       dacbiet='Ô tìm nhanh, Số hợp đồng, Số phiếu yêu cầu: khớp một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối, không '
               'giới hạn ký tự; % và _ là ký tự đại diện. Số hợp đồng tìm trên số hợp đồng dịch vụ / mã phiếu bảo hành hoặc số hợp đồng '
               'bán của yêu cầu lắp đặt. Thời gian dự kiến: ngày bắt đầu ≥ Từ ngày và ngày kết thúc ≤ Đến ngày. Người yêu cầu lọc cùng thứ '
               'tự với cột hiển thị. Công ty / Phòng ban lọc theo công ty / phòng của người lập phiếu.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao (có ô Công ty, Phòng ban — quyền Tổng công ty)'),
   extra=[(shot('02b_filter_status'), 'Ô Trạng thái đang mở'), (shot('02c_filter_company'), 'Ô Công ty đang mở')],
   ui=[
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu giao việc”', '- Khớp một phần số phiếu', '- Chỉ lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh và ô gõ chữ, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, về trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc, chữ đổi thành “Ẩn tìm kiếm nâng cao”', '- Bấm lại → thu gọn']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống',
        ['- Chỉ hiện khi có quyền Xem mức Tổng công ty', '- Gợi ý “Chọn công ty”', '- Đổi → xóa ô Phòng ban, lọc ngay']),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Phòng ban theo quyền', 'Không', 'Trống',
        ['- Hiện khi có quyền Xem (mọi mức)', '- Tổng công ty: phòng của công ty đã chọn; Công ty: phòng của công ty mình; Phòng ban: '
         'phòng mình quản lý', '- Lọc ngay khi chọn']),
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
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí, trong phạm vi quyền.'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, Số hợp đồng, Số phiếu yêu cầu; bỏ khoảng trắng đầu / cuối.\nDuring:\n– Tìm phiếu có số phiếu '
        '/ số hợp đồng / số phiếu yêu cầu chứa chuỗi nhập.\nAfter:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nDuring:\n– Đưa mọi ô về trống, bỏ khách hàng đã chọn.\n'
        'After:\n– Bỏ sắp xếp, nạp lại trang 1; phạm vi quyền giữ nguyên.'),
       ('Đổi Công ty', 'Change',
        'Before:\n– Có quyền Xem mức Tổng công ty.\nDuring:\n– Xóa giá trị Phòng ban, nạp danh sách phòng của công ty mới.\n'
        'After:\n– Lọc phiếu do người thuộc công ty đó lập.'),
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
            'người dùng và riêng cho lối vào Phiếu giao việc (khác lối vào Phiếu giao việc được giao), không đổi dữ liệu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê các mục lọc kèm ô tích, theo cấu hình đang lưu (9 mục khi có quyền Xem theo '
             'mức, 8 mục khi không có).\n'
             '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng + lối vào, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ các mục theo thứ tự thiết kế; vẫn phải bấm Lưu.\n'
           '• Bỏ tích mục đang có giá trị lọc → ô bị ẩn.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet='9 mục: Công ty – Phòng ban (chỉ khi có quyền Xem theo mức), Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Trạng '
               'thái, Người tạo, Người thực hiện, Thời gian dự kiến.'),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 9 mục', '–', 'Theo cấu hình đã lưu',
        ['- Công ty – Phòng ban', '- Số hợp đồng', '- Số phiếu yêu cầu', '- Khách hàng', '- Người yêu cầu', '- Trạng thái', '- Người tạo',
         '- Người thực hiện', '- Thời gian dự kiến']),
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
        'After:\n– Mở cửa sổ (chưa lưu lần nào → đủ các mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại và lối vào Phiếu giao việc.\nDuring:\n– Gửi danh sách mục đã tích theo '
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
fr(5, 'Tạo phiếu giao việc', usecase=('FR-05', 'Tạo phiếu giao việc', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lập phiếu giao việc từ 1 chứng từ nguồn còn số lượng chưa giao (lưu là duyệt)',
       mota='Màn Tạo phiếu giao việc luôn mở từ 1 chứng từ nguồn: hợp đồng dịch vụ, phụ lục bổ sung, phiếu bảo hành, phiếu yêu cầu lắp đặt '
            'bàn giao hoặc phiếu yêu cầu giao việc khác. Hệ thống chép sẵn thông tin khách hàng, các dòng việc còn số lượng chưa giao '
            '(SL giao lần này mặc định = SL còn), định mức công; người lập chỉ nhập ngày dự kiến, chỉnh SL giao lần này, ghi chú, ĐM công '
            'dịch vụ đính kèm và công phụ P3. Bấm Lưu và duyệt → phiếu vào trạng thái Chờ thực hiện ngay (không có nháp), chứng từ nguồn '
            'bị trừ số lượng / đổi trạng thái, rồi quay về danh sách Phiếu giao việc.',
       tacnhan='Người dùng có quyền thực hiện chức năng: người thuộc phòng tiếp nhận của chứng từ nguồn; nguồn hợp đồng / phụ lục bổ sung / '
               'phiếu bảo hành cần thêm quyền “%s” (phiếu bảo hành không xét phòng tiếp nhận).' % QT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Chứng từ nguồn ở trạng thái được giao việc: hợp đồng / phụ lục “Có hiệu lực”, '
                'phiếu bảo hành “Đã duyệt”, phiếu yêu cầu lắp đặt / giao việc khác “Chờ giao việc”.\n'
                '3. Chứng từ nguồn còn số lượng chưa giao; hợp đồng không có phụ lục giảm đang chờ duyệt.',
       chinh='1. Người dùng vào màn Phiếu chờ giao việc, chọn tab (Hợp đồng / PL bổ sung / Phiếu bảo hành / Lắp đặt bàn giao / Giao việc '
             'khác) và bấm Tạo phiếu giao việc (dấu +) ở dòng chứng từ — hoặc bấm Tạo phiếu giao việc ở danh sách / chi tiết phiếu yêu '
             'cầu lắp đặt bàn giao, phiếu yêu cầu giao việc khác (mở tab mới).\n'
             '2. Hệ thống kiểm tra quyền + phòng tiếp nhận + trạng thái + số lượng còn của chứng từ, mở trang “Tạo phiếu giao việc”.\n'
             '3. Hệ thống điền sẵn khối Thông tin khách hàng (chỉ đọc), Ghi chú = ghi chú chứng từ nguồn, các bảng việc theo loại nguồn với '
             'SL còn, SL giao lần này = SL còn (vật tư bán thêm = 0), định mức công, và khối Tổng hợp.\n'
             '4. Người dùng chọn Ngày dự kiến bắt đầu, Ngày dự kiến kết thúc; chỉnh SL giao lần này (không vượt SL còn), ghi chú dòng; '
             'nhập ĐM công dịch vụ đính kèm (giao việc khác); bấm Thêm dòng để nhập công phụ tính P3 nếu có.\n'
             '5. Hệ thống tính lại ngay Tổng công định mức từng bảng và khối Tổng hợp mỗi lần đổi số.\n'
             '6. Người dùng bấm Lưu và duyệt; hệ thống kiểm tra toàn bộ form, có lỗi thì tô đỏ tất cả ô lỗi, báo và cuộn tới ô đầu.\n'
             '7. Hợp lệ → hộp “Xác nhận lưu & duyệt”: “Lưu và duyệt phiếu giao việc cho <loại chứng từ> ‘<mã>’? Phiếu sẽ chuyển sang trạng '
             'thái Chờ thực hiện.”; người dùng bấm Lưu và duyệt.\n'
             '8. Hệ thống khóa chứng từ nguồn, kiểm lại quyền / trạng thái / SL còn, sinh mã phiếu, lưu phiếu trạng thái Chờ thực hiện, ghi '
             'tiến độ giao việc, cập nhật chứng từ nguồn, ghi lịch sử “Tạo mới”.\n'
             '9. Hệ thống báo “Tạo phiếu giao việc thành công.” và chuyển về danh sách Phiếu giao việc.',
       phu='• Không có quyền / không thuộc phòng tiếp nhận / chứng từ đã giao hết khi mở form → thông báo %s (hoặc câu của hệ thống), quay '
           'về Phiếu chờ giao việc đúng tab.\n'
           '• Hợp đồng có phụ lục giảm chờ duyệt → “Hợp đồng đang có PL giảm chờ duyệt!”.\n'
           '• Thiếu ngày / thiếu tên, ĐM công dòng P3 → %s dưới ô, thông báo “Bạn chưa nhập đầy đủ thông tin.”.\n'
           '• SL giao lần này vượt SL còn → %s ngay khi gõ (không tự kéo về), thông báo “Vui lòng kiểm tra lại thông tin đã nhập”.\n'
           '• Trong lúc mở form người khác đã giao bớt / đổi trạng thái chứng từ → máy chủ báo vượt SL tại đúng ô, hoặc %s.\n'
           '• Phiếu bảo hành không còn sản phẩm để giao → “Không có sản phẩm bảo hành để giao”.\n'
           '• Trưởng phòng có nhân viên phòng mình còn hàng quá hạn → “Phòng ban bạn quản lý có nhân viên … quá hạn. Không thể thực hiện '
           'thao tác này.”.\n'
           '• Bấm Hủy trong hộp xác nhận → không lưu, form giữ nguyên.\n'
           '• Bấm Quay lại / rời trang khi đã đổi dữ liệu → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì → về Phiếu chờ giao '
           'việc đúng tab.' % (NO_PERM, REQ, MAXV, CONFLICT),
       dacbiet='Không có Lưu nháp, Lưu và tiếp tục (form lập từ 1 chứng từ, lưu là duyệt — user chốt 02/11/2026, giữ như ERP). Mã phiếu '
               '<mã công ty người lập>.PGV.<năm><số thứ tự 6 số>; công ty, phòng ban của phiếu = của người lập. Khóa nút trong lúc lưu. '
               'Chứng từ nguồn thiếu dữ liệu bắt buộc (lỗi thiết bị, đơn vị tính…) → “Chứng từ nguồn thiếu thông tin <tên>. Vui lòng bổ '
               'sung ở chứng từ nguồn rồi tạo lại.”.'),
   layout=dict(entries=[
       (MENU_CHO + ' => Tạo phiếu giao việc',
        'Lối vào chính: ở 1 trong 5 tab của Phiếu chờ giao việc, bấm Tạo phiếu giao việc (dấu +) ở cột Hành động của dòng chứng từ; màn '
        'Tạo mở trong cùng tab trình duyệt.'),
       ('', 'Lối vào khác: nút Tạo phiếu giao việc ở danh sách / chi tiết Phiếu yêu cầu lắp đặt, bàn giao và Phiếu yêu cầu giao việc '
            'khác (phân hệ Bán hàng → Yêu cầu → Lắp đặt - BH - SC) — mở màn Tạo ở tab trình duyệt mới. Danh sách Phiếu giao việc không '
            'có nút Tạo mới.')],
       shot=shot('41_create_hd'), shot_caption='Màn Tạo phiếu giao việc từ hợp đồng (dữ liệu nguồn giả trên trình duyệt bằng phiếu thật '
                                               'cùng loại)'),
   extra=[(shot('41_create_hd_full'), 'Toàn trang Tạo phiếu giao việc từ hợp đồng: A - Dịch vụ sửa chữa bảo dưỡng, B - Vật tư bán thêm, '
                                      'C - Công việc phụ, D - Tổng hợp'),
          (shot('40_create_bh'), 'Màn Tạo phiếu giao việc từ phiếu bảo hành (dữ liệu thật)'),
          (shot('41b_create_ld_full'), 'Màn Tạo phiếu giao việc từ phiếu yêu cầu lắp đặt, bàn giao (bảng A - Lắp đặt bàn giao)'),
          (shot('41c_create_gvk_full'), 'Màn Tạo phiếu giao việc từ phiếu yêu cầu giao việc khác (bảng A - Dịch vụ đính kèm)'),
          (shot('42_validate'), 'Lỗi kiểm tra khi bấm Lưu và duyệt (câu lỗi gán trên trình duyệt đúng theo code)'),
          (shot('43_confirm_save'), 'Hộp Xác nhận lưu & duyệt'),
          (shot('44_unsaved'), 'Hộp Thông tin chưa lưu khi bấm Quay lại')],
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tạo phiếu giao việc”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập', '- Góc phải khối Thông tin khách hàng: người đang lập + giờ hiện tại.'),
       ('Ô chứng từ nguồn', 'Link', 'Read-only', '–', 'Có (*)', 'Theo chứng từ',
        ['- Nhãn theo loại: Số hợp đồng / Số phiếu bảo hành / Phiếu yêu cầu lắp đặt, bàn giao + Hợp đồng / Phiếu YC giao việc khác',
         '- Bấm mã → mở chi tiết chứng từ, tab mới (hợp đồng bán hãng mở hệ thống ERP)', '- Không đổi được chứng từ']),
       ('Khách hàng', 'Textbox', 'Read-only', '–', 'Có (*)', 'Theo chứng từ', '- “Mã KH - Tên khách hàng”, chép từ chứng từ nguồn.'),
       ('Người liên hệ', 'Textbox', 'Read-only', '–', 'Có (*)', 'Theo chứng từ',
        '- Chép từ chứng từ; chứng từ thiếu → báo lỗi dưới ô khi lưu, phải bổ sung ở chứng từ nguồn.'),
       ('SĐT liên hệ', 'Textbox', 'Read-only', '–', 'Không', 'Theo chứng từ', '- Chép từ chứng từ nguồn.'),
       ('Địa chỉ lắp đặt', 'Textbox', 'Read-only', '–', 'Không', 'Theo chứng từ', '- Địa chỉ làm việc.'),
       ('Người yêu cầu', 'Textbox', 'Read-only', '–', 'Không', 'Người lập chứng từ', '- Kèm 2 ô SĐT người yêu cầu, Phòng yêu cầu.'),
       ('Ngày dự kiến bắt đầu', 'Datepicker', 'Enable', '≥ hôm nay', 'Có', 'Trống',
        ['- Gợi ý “Chọn ngày dự kiến bắt đầu”', '- Lịch khóa các ngày trước hôm nay', '- Trống → ' + REQ, '- Trước hôm nay → ' + MSG_START]),
       ('Ngày dự kiến kết thúc', 'Datepicker', 'Enable', '≥ hôm nay và ≥ ngày bắt đầu', 'Có', 'Trống',
        ['- Gợi ý “Chọn ngày dự kiến kết thúc”', '- Lịch khóa ngày trước hôm nay / trước ngày bắt đầu', '- Trống → ' + REQ,
         '- Sai → ' + MSG_END]),
       ('Ghi chú', 'Textarea', 'Enable', 'Không giới hạn', 'Không', 'Ghi chú chứng từ nguồn', '- Gợi ý “Nhập ghi chú”.'),
       ('Bảng A - BẢO HÀNH', 'Table/Grid', 'Enable', '–', '–', 'Theo phiếu bảo hành',
        ['- Chỉ khi nguồn là phiếu bảo hành', '- Cột: STT, Nội dung công việc, ĐVT, SL còn trên hợp đồng, SL giao lần này, Định mức công, '
         'Ghi chú', '- Mỗi thiết bị: dòng đầu (Tên - Model - Mã hàng, Thiết bị: nguồn, Lỗi thiết bị, Serial, Số BBBGNT hoặc BBXNCV), i.1 '
         'Công tháo lắp sửa chữa thiết bị, i.2 Danh sách dịch vụ, i.3 Danh sách vật tư', '- Dòng “Tổng công định mức”']),
       ('Bảng A - DỊCH VỤ SỬA CHỮA BẢO DƯỠNG', 'Table/Grid', 'Enable', '–', '–', 'Theo hợp đồng / phụ lục',
        ['- Chỉ khi nguồn là hợp đồng / phụ lục bổ sung', '- I - Dịch vụ sửa chữa: cùng khuôn bảng bảo hành, dòng “Tổng công định mức (I)”; '
         'ô SL bị khóa khi SL còn ≤ 0', '- II - Danh mục thiết bị cần bảo dưỡng: thiết bị → gói / cấp dịch vụ → vật tư; cột Loại dịch vụ, '
         'ĐVT, SL còn, SL giao lần này, Định mức công, Ghi chú; dòng tổng II và “Tổng I + II”']),
       ('Bảng A - Lắp đặt bàn giao', 'Table/Grid', 'Enable', '–', '–', 'Theo phiếu yêu cầu',
        ['- Chỉ khi nguồn là phiếu yêu cầu lắp đặt bàn giao', '- Cột: STT, Hàng hóa (*), Model, ĐVT, SL bàn giao (nhập), SL tính công '
         'khoán, Định mức công, Tổng công định mức', '- SL bàn giao mặc định = SL còn, gợi ý “Nhập SL bàn giao”']),
       ('Bảng A - Dịch vụ đính kèm', 'Table/Grid', 'Enable', '–', '–', 'Theo phiếu yêu cầu',
        ['- Chỉ khi nguồn là phiếu yêu cầu giao việc khác', '- Cột: STT, Dịch vụ đi kèm, Định mức công (nhập, mặc định 0, gợi ý “Nhập định '
         'mức công”)', '- Dòng tổng']),
       ('Ô SL giao lần này', 'Number', 'Enable / Disable', '0 – SL còn; số nguyên', 'Không', 'SL còn',
        ['- Gợi ý “Nhập số lượng”', '- Chặn chữ, dấu trừ; thiết bị, dịch vụ, gói bảo dưỡng, lắp đặt, bán thêm chỉ nhận số nguyên; vật tư '
         'nhận 2 số lẻ', '- Vượt SL còn → ' + MAXV + ' ngay khi gõ']),
       ('Ô Ghi chú dòng', 'Textbox', 'Enable', '≤ 255 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập ghi chú”', '- Quá 255 → “Vui lòng nhập tối đa 255 ký tự.”']),
       ('Bảng B - Danh sách vật tư bán thêm', 'Table/Grid', 'Enable', '–', '–', 'Theo hợp đồng / phiếu bảo hành',
        ['- Chỉ nguồn hợp đồng / phụ lục / phiếu bảo hành', '- Cột: STT, Tên vật tư (*) (kèm Model, ĐVT), Số lượng còn trên hợp đồng, '
         'Số lượng giao lần này (mặc định 0)', '- Dòng “Tổng cộng”']),
       ('Khối B / C - CÔNG VIỆC PHỤ', 'Table/Grid', 'Enable', '–', '–', 'Trống',
        ['- “B - CÔNG VIỆC PHỤ” với giao việc khác, còn lại “C - CÔNG VIỆC PHỤ”', '- I. Công phụ tính P3: cột Công phụ tính P3 (*), ĐM Công '
         '(*), Ghi chú, Hành động', '- Nút Thêm dòng; biểu tượng Xóa dòng xóa đúng dòng bấm', '- Tên trống / ĐM công trống → ' + REQ +
         '; tên quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”']),
       ('Khối C / D - TỔNG HỢP', 'Table/Grid', 'Read-only', '–', '–', 'Tự tính',
        ['- I. Tổng công định mức: Công chính, Công phụ, “Tổng công định mức được giao” (2 số lẻ)',
         '- II. Tổng dịch vụ trả tiền: gộp SL dịch vụ theo tên dịch vụ', '- III. Tổng hợp vật tư phải giao: gộp SL vật tư theo hàng hóa',
         '- V. Chi phí khác: chép chi phí của hợp đồng (Tên chi phí, Đơn giá)', '- II, III, V chỉ khi nguồn là hợp đồng / phiếu bảo hành']),
       ('Nút Lưu và duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Biểu tượng dấu tích tròn', '- Kiểm tra form → hộp “Xác nhận lưu & duyệt” → lưu', '- Khóa khi đang lưu']),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về Phiếu chờ giao việc đúng tab của nguồn; đã đổi dữ liệu thì hỏi.'),
       ('Hộp Xác nhận lưu & duyệt', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', '- Nút Lưu và duyệt, Hủy.'),
       ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        '- “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”, nút Thoát, Ở lại.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Tạo phiếu giao việc thành công.”', '- “Bạn chưa nhập đầy đủ thông tin.”', '- “Vui lòng kiểm tra lại thông tin đã nhập”',
         '- ' + NO_PERM + ', ' + CONFLICT, '- “Tạo phiếu giao việc không thành công.”']),
   ],
   ev=[
       ('Bấm Tạo phiếu giao việc (màn nguồn)', 'Click',
        'Before:\n– Nút hiện theo điều kiện của màn nguồn (Q1 + phòng tiếp nhận với hợp đồng / phụ lục; phòng tiếp nhận với lắp đặt / '
        'giao việc khác; phiếu bảo hành luôn hiện).\nDuring:\n– Mở màn Tạo kèm chứng từ nguồn; thiếu / sai chứng từ → trang 404.\n'
        'After:\n– Nạp dữ liệu nguồn.'),
       ('Mở màn Tạo', 'System',
        'Before:\n– Kiểm quyền: hợp đồng / phụ lục: Q1 + đúng phòng tiếp nhận + “Có hiệu lực”; phiếu bảo hành: Q1 + “Đã duyệt”; yêu cầu lắp '
        'đặt / giao việc khác: đúng phòng tiếp nhận + “Chờ giao việc”; còn SL chưa giao; không có phụ lục giảm chờ duyệt.\n'
        '– Không đạt → thông báo ' + NO_PERM + ' (hoặc câu tương ứng), quay về Phiếu chờ giao việc.\n'
        'During:\n– Chép khách hàng, dòng việc còn SL; SL giao = SL còn (âm → 0); vật tư bán thêm = 0; ĐM công thiết bị theo lỗi '
        'thiết bị (thiếu → 0), dịch vụ bảo dưỡng theo gói / cấp (thiếu → 1); dịch vụ đính kèm 0.\n'
        'After:\n– Hiển thị form, tính sẵn khối Tổng hợp.'),
       ('Gõ SL giao lần này / ĐM công', 'Change',
        'Before:\n– Ô số chặn chữ, dấu trừ; cột số nguyên chặn dấu thập phân.\nDuring:\n– Vượt SL còn → ' + MAXV + ' dưới ô ngay; hợp lệ '
        'thì xóa lỗi.\nAfter:\n– Tính lại tổng công định mức bảng, Công chính / Công phụ / Tổng, Tổng dịch vụ, Tổng vật tư.'),
       ('Bấm Thêm dòng / Xóa dòng (công phụ P3)', 'Click',
        'Before:\n– Chỉ ở màn Tạo.\nDuring:\n– Thêm dòng trống / xóa đúng dòng bấm, kéo lỗi các dòng sau theo.\nAfter:\n– Tính lại Công phụ, Tổng.'),
       ('Bấm Lưu và duyệt', 'Click',
        'Before:\n– Kiểm tra cùng lúc: 2 ngày bắt buộc, ≥ hôm nay, kết thúc ≥ bắt đầu; dòng P3 đủ tên + ĐM công; mọi SL ≤ SL còn; ghi chú '
        'dòng / tên công phụ ≤ 255.\n– Có lỗi → tô đỏ mọi ô lỗi, báo “Bạn chưa nhập đầy đủ thông tin.” / “Vui lòng kiểm tra lại thông tin '
        'đã nhập”, cuộn tới ô đầu, dừng.\nDuring:\n– Hiện hộp “Xác nhận lưu & duyệt”.\nAfter:\n– Chờ người dùng xác nhận.'),
       ('Bấm Lưu và duyệt trong hộp xác nhận', 'Click',
        'Before:\n– Chặn trưởng phòng có nhân viên còn hàng quá hạn; kiểm lại quyền, trạng thái, SL còn của chứng từ (đã khóa chứng từ).\n'
        '– Không có quyền → ' + NO_PERM + '; chứng từ đổi trạng thái → ' + CONFLICT + '; vượt SL → lỗi tại ô.\n'
        'During:\n– Sinh mã, lưu phiếu Chờ thực hiện + mọi dòng, tổng công định mức tính lại ở máy chủ; ghi tiến độ giao việc; hợp '
        'đồng / phụ lục trừ SL còn; phiếu bảo hành bỏ đánh dấu chờ giao (hết SL); yêu cầu lắp đặt tính lại trạng thái (Đang giao việc khi '
        'giao hết); yêu cầu giao việc khác → Đã giao việc.\n' + ERR + '\n'
        'After:\n– Ghi lịch sử “Tạo mới”; báo “Tạo phiếu giao việc thành công.”; về danh sách Phiếu giao việc.'),
       ('Bấm Hủy trong hộp xác nhận', 'Click', 'Before:\n– Không lưu.\nAfter:\n– Đóng hộp, form giữ nguyên dữ liệu đã nhập.'),
       ('Bấm Quay lại / rời trang', 'Click',
        'Before:\n– Có thay đổi so với lúc mở (trừ dữ liệu tự nạp) → hộp “Thông tin chưa lưu”.\nDuring:\n– Thoát → bỏ dữ liệu; Ở lại → '
        'đóng hộp.\nAfter:\n– Về Phiếu chờ giao việc đúng tab của nguồn.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Xem chi tiết phiếu giao việc',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết 1 phiếu giao việc',
       mota='Bấm Số phiếu giao việc để mở trang chi tiết chỉ đọc: thông tin khách hàng và chứng từ nguồn, các bảng công việc theo loại phiếu '
            '(bảo hành / sửa chữa – bảo dưỡng / lắp đặt bàn giao / dịch vụ đính kèm), vật tư bán thêm, công việc phụ, tổng hợp công định '
            'mức và khối Lịch sử. Chân trang có các nút hành động cùng điều kiện với cột Hành động. Không có nút Sửa (giữ như ERP). Màn '
            'chi tiết chỉ hiện các dòng đã giao (SL > 0), ẩn cột SL còn.',
       tacnhan='Người dùng có quyền thực hiện chức năng: người tạo hoặc người thực hiện phiếu; hoặc có quyền “%s” (Tổng công ty: mọi phiếu; '
               'Công ty: phiếu công ty mình; Phòng ban: phiếu phòng mình quản lý).' % QV,
       dieukien=DK + '\n4. Phiếu chưa Hủy.',
       chinh='1. Người dùng bấm Số phiếu giao việc ở danh sách (hoặc mã phiếu ở Phiếu giao công tác, Phiếu nhập kết quả, báo cáo theo dõi).\n'
             '2. Hệ thống ghi nhớ bộ lọc danh sách (10 phút) và mở trang “Chi tiết phiếu giao việc: <mã>” kèm nhãn trạng thái.\n'
             '3. Hệ thống kiểm tra người xem: người tạo, người thực hiện, hoặc quyền xem theo mức.\n'
             '4. Hệ thống hiển thị các khối ở chế độ chỉ đọc, góc phải khối đầu ghi “<Người tạo> - <ngày giờ tạo>”.\n'
             '5. Chân trang hiện Nhập kết quả / Xem phiếu nhập kết quả / Xóa theo điều kiện và nút Quay lại.\n'
             '6. Người dùng bấm Quay lại → về màn trước (danh sách, giữ bộ lọc).',
       phu='• Phiếu không tồn tại / đã Hủy / người xem không có quyền → chuyển trang 404, không thông báo.\n'
           '• Lỗi khác khi tải → thông báo “Không tải được phiếu giao việc.”.\n'
           '• Bấm chứng từ nguồn (hợp đồng / phiếu bảo hành / phiếu yêu cầu) → mở chi tiết chứng từ ở tab mới.\n'
           '• Mở chi tiết bằng đường dẫn trực tiếp / tab mới, hoặc vừa lưu ở màn Tạo, rồi bấm Quay lại → về danh sách Phiếu giao việc.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, chuyển về màn đăng nhập.',
       dacbiet='Các ô có dấu (*) đỏ như hệ thống ERP (chứng từ nguồn, Khách hàng, Người liên hệ, Ngày dự kiến bắt đầu / kết thúc, cột Hàng '
               'hóa, Tên vật tư, Công phụ tính P3) dù đang chỉ đọc. Bảng I. Tổng công định mức hiện 2 số lẻ cố định; Định mức công dòng lắp '
               'đặt hiện đủ số lẻ như ERP (1.302, 0.019).'),
   layout=dict(menu=MENU + ' => Số phiếu giao việc', shot=shot('17_detail'),
               shot_caption='Màn Chi tiết phiếu giao việc (phiếu từ hợp đồng, Chờ thực hiện, có nút Nhập kết quả)',
               note='Trang chi tiết mở trong cùng tab trình duyệt khi bấm Số phiếu giao việc ở danh sách.'),
   extra=[(shot('17_detail_full'), 'Toàn trang chi tiết phiếu giao việc từ hợp đồng'),
          (shot('17e_detail_bh'), 'Chi tiết phiếu giao việc từ phiếu bảo hành'),
          (shot('17f_detail_ld_full'), 'Chi tiết phiếu giao việc từ yêu cầu lắp đặt, bàn giao (có nút Xóa)'),
          (shot('17g_detail_gvk'), 'Chi tiết phiếu giao việc từ yêu cầu giao việc khác')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', ['- “Chi tiết phiếu giao việc: <mã>”', '- Nhãn trạng thái cùng màu danh sách']),
       ('Khối Thông tin khách hàng', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - <dd/mm/yyyy hh:mm>”.'),
       ('Ô chứng từ nguồn', 'Link', 'Enable', '–', 'Theo dữ liệu',
        ['- Nhãn theo loại: Số hợp đồng / Số phiếu bảo hành / Phiếu yêu cầu lắp đặt, bàn giao + Hợp đồng / Phiếu YC giao việc khác',
         '- Bấm → chi tiết chứng từ, tab mới']),
       ('Khách hàng', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- “Mã KH - Tên khách hàng”.'),
       ('Người liên hệ', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- Kèm SĐT liên hệ, Địa chỉ lắp đặt.'),
       ('Người yêu cầu', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- Người lập chứng từ nguồn; kèm SĐT người yêu cầu, Phòng yêu cầu.'),
       ('Ngày dự kiến bắt đầu', 'Textbox', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Có dấu (*).'),
       ('Ngày dự kiến kết thúc', 'Textbox', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Có dấu (*).'),
       ('Ghi chú', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '- Khóa ở màn chi tiết.'),
       ('Khối A - công việc chính', 'Table/Grid', 'Read-only', '–', 'Theo loại phiếu',
        ['- A - BẢO HÀNH / A - DỊCH VỤ SỬA CHỮA BẢO DƯỠNG (I, II) / A - Lắp đặt bàn giao / A - Dịch vụ đính kèm',
         '- Chỉ các dòng đã giao; không có cột SL còn', '- Mỗi bảng có dòng Tổng công định mức']),
       ('Khối B - Danh sách vật tư bán thêm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Chỉ phiếu từ hợp đồng / phiếu bảo hành.'),
       ('Khối CÔNG VIỆC PHỤ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- I. Công phụ tính P3; không có nút Thêm dòng, Xóa dòng.'),
       ('Khối TỔNG HỢP', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- I. Tổng công định mức (2 số lẻ) = cột Tổng công định mức ở danh sách', '- II. Tổng dịch vụ trả tiền, III. Tổng hợp vật tư '
         'phải giao, V. Chi phí khác']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc (mục 2.8).'),
       ('Nút Nhập kết quả', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Cùng điều kiện BR-10; bấm → mục 2.9.'),
       ('Nút Xem phiếu nhập kết quả', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Cùng điều kiện BR-11; bấm → mục 2.10.'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Nút đỏ, cùng điều kiện BR-08; bấm → mục 2.7.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Lùi về màn trước (danh sách giữ bộ lọc); mở trực tiếp → danh sách.'),
       ('Thông báo lỗi tải', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Không tải được phiếu giao việc.”'),
   ],
   ev=[
       ('Bấm Số phiếu giao việc', 'Click',
        'Before:\n– Ghi nhớ bộ lọc danh sách (10 phút).\nDuring:\n– Chuyển sang trang chi tiết trong cùng tab.\n'
        'After:\n– Bắt đầu nạp dữ liệu phiếu.'),
       ('Mở trang chi tiết', 'System',
        'Before:\n– Kiểm tra người xem: người tạo, người thực hiện hoặc quyền “' + QV + '” theo mức.\n'
        '– Không có quyền / phiếu không có / đã Hủy → chuyển trang 404 và dừng xử lý.\n'
        'During:\n– Nạp thông tin phiếu, chứng từ nguồn, bảng công việc (dòng đã giao), tổng hợp, cờ hành động.\n'
        '– Lỗi khác → “Không tải được phiếu giao việc.”.\n'
        'After:\n– Hiển thị chi tiết chỉ đọc + nút chân trang theo điều kiện.'),
       ('Bấm chứng từ nguồn', 'Click',
        'Before:\n– Ô có liên kết.\nAfter:\n– Mở chi tiết chứng từ ở tab mới; màn chi tiết giữ nguyên.'),
       ('Bấm Quay lại / nút lùi trình duyệt', 'Click',
        'Before:\n– Đi vào từ danh sách thì lùi 1 bước; mở trực tiếp / vừa tạo thì về danh sách Phiếu giao việc.\n'
        'After:\n– Về danh sách, khôi phục bộ lọc (nếu còn trong 10 phút).'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Xóa phiếu giao việc', usecase=('FR-07', 'Xóa phiếu giao việc', 'action', A_LAP),
   rule=('- Quy tắc Xóa.', 'delete'),
   intro=dict(
       ten='Xóa (Hủy) phiếu giao việc Chờ thực hiện chưa gắn phiếu giao công tác',
       mota='Người tạo phiếu xóa phiếu giao việc của mình khi phiếu còn Chờ thực hiện và chưa gắn phiếu giao công tác. Xóa là chuyển phiếu '
            'sang trạng thái Hủy (không xóa cứng) và trả lại số lượng / trạng thái cho chứng từ nguồn để có thể giao lại từ Phiếu chờ '
            'giao việc.',
       tacnhan='Người dùng có quyền thực hiện chức năng: người tạo phiếu giao việc (không đặc cách Super admin, quyền Xem theo mức không '
               'cho xóa phiếu người khác).',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người đăng nhập là người tạo phiếu.\n3. Phiếu Chờ thực hiện và chưa gắn phiếu '
                'giao công tác (chưa lập phiếu giao công tác cho phiếu này).',
       chinh='1. Người dùng bấm Xóa (thùng rác đỏ) ở cột Hành động hoặc nút Xóa ở chân trang chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa”: “Bạn có chắc muốn xóa bản ghi này không?” (từ chi tiết: “Bạn có chắc muốn xóa phiếu '
             'giao việc \'<mã>\'?”).\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm tra người tạo, trạng thái Chờ thực hiện, chưa gắn phiếu giao công tác; chuyển phiếu sang Hủy.\n'
             '5. Hệ thống trả số lượng cho chứng từ nguồn: xóa tiến độ giao việc (hợp đồng / phụ lục có lại SL còn); phiếu yêu cầu giao '
             'việc khác về Chờ giao việc (ghi lịch sử phiếu yêu cầu); phiếu yêu cầu lắp đặt tính lại trạng thái; phiếu bảo hành bật lại '
             'đánh dấu chờ giao.\n'
             '6. Hệ thống ghi một dòng lịch sử “Thay đổi trạng thái: Chờ thực hiện → Hủy”, báo “Xóa thành công.”, nạp lại danh sách '
             '(từ màn chi tiết thì chuyển về danh sách Phiếu giao việc).',
       phu='• Bấm Hủy / (x) / click ra ngoài hộp → không xóa.\n'
           '• Không phải người tạo → hệ thống từ chối, báo %s.\n'
           '• Phiếu đã đổi trạng thái / đã gắn phiếu giao công tác → %s; danh sách nạp lại.\n'
           '• Phiếu không còn → “Không tìm thấy phiếu giao việc”.\n'
           '• Lỗi khác → “Xóa không thành công”.\n'
           '• Đang ở dòng cuối của trang > 1 → sau khi xóa lùi 1 trang.' % (NO_DEL, CONFLICT),
       dacbiet='Phiếu Hủy rời khỏi mọi danh sách phiếu giao việc, không mở được chi tiết; số lượng trả về Phiếu chờ giao việc. Khóa nút '
               'trong lúc đang xóa.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp Xác nhận xóa từ danh sách (phiếu thật đủ điều kiện)',
               note='Hộp xác nhận được mở ngay trên màn hình danh sách hoặc màn chi tiết theo đường dẫn ở trên.'),
   extra=[(shot('13b_delete_detail'), 'Hộp Xác nhận xóa từ màn chi tiết')],
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Xóa (dòng)', 'Icon Button', 'Enable / Ẩn', 'Theo điều kiện', ['- Thùng rác đỏ, chú thích “Xóa”', '- Chỉ khi đủ BR-08']),
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
       ('Chứng từ nguồn', 'Label', 'Hiển thị', 'Theo dữ liệu', '- Số lượng / trạng thái trả lại, xuất hiện lại ở Phiếu chờ giao việc.'),
   ],
   ev=[
       ('Bấm Xóa', 'Click', 'Before:\n– Nút chỉ hiện khi đủ BR-08.\nAfter:\n– Hiện hộp Xác nhận xóa.'),
       ('Bấm Xóa trong hộp', 'Click',
        'Before:\n– Kiểm tra người đăng nhập là người tạo phiếu; nếu không → hệ thống từ chối, báo ' + NO_DEL + ' và dừng xử lý.\n'
        '– Kiểm tra Chờ thực hiện + chưa gắn phiếu giao công tác (không → ' + CONFLICT + ').\n'
        'During:\n– Khóa phiếu, chuyển Hủy, xóa tiến độ giao việc, trả trạng thái chứng từ nguồn trong 1 lần.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Thay đổi trạng thái” (Chờ thực hiện → Hủy).\n– Hiển thị “Xóa thành công.”; nạp lại danh sách '
        '/ chuyển về danh sách Phiếu giao việc.'),
       ('Bấm Hủy / (x) / click ra ngoài hộp', 'Click',
        'Before:\n– Không xóa.\nAfter:\n– Đóng hộp, màn giữ nguyên.'),
       ('Xóa dòng cuối của trang', 'System',
        'Before:\n– Trang hiện tại > 1 và chỉ còn 1 dòng.\nAfter:\n– Lùi 1 trang rồi nạp lại.'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu giao việc',
       mota='Xem các mốc thao tác của phiếu: thời điểm, hành động, người thực hiện, giá trị cũ → mới. Phiếu có các loại mốc: “Tạo mới” '
            '(lập phiếu ở HRM, kèm số phiếu, khách hàng, ngày dự kiến, tổng công định mức, ghi chú) và “Thay đổi trạng thái” (do phiếu '
            'nhập kết quả lưu / gửi duyệt / bị xóa / được duyệt, hoặc do Xóa phiếu), kèm mã phiếu nhập kết quả gây ra. Cửa sổ ở danh sách '
            'và khối Lịch sử ở màn chi tiết dùng chung nội dung.',
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
           '- Tạo mới: các trường ban đầu của phiếu',
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

# ------------------------------------------------------------ 2.9
fr(9, 'Nhập kết quả', usecase=('FR-09', 'Nhập kết quả', 'crud', A_TH),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Mở màn Tạo phiếu nhập kết quả cho phiếu giao việc',
       mota='Người thực hiện bấm Nhập kết quả ở cột Hành động (hoặc chân trang chi tiết) để mở màn Tạo phiếu nhập kết quả với phiếu giao '
            'việc chọn sẵn. Màn này chỉ quyết định nút hiện hay không; nội dung, kiểm tra và lưu phiếu nhập kết quả thuộc tài liệu Phiếu '
            'nhập kết quả. Lưu xong, trạng thái phiếu giao việc đổi theo phiếu nhập kết quả và nút Nhập kết quả không hiện nữa. Quản lý có '
            'quyền Xem theo mức nhưng không là người thực hiện thì KHÔNG có nút.',
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
       phu='• Phiếu chưa đủ điều kiện (chưa lập / chưa duyệt phiếu giao công tác, đã có phiếu nhập kết quả, trạng thái khác Chờ thực hiện, '
           'mình không là người thực hiện) → không có nút Nhập kết quả.\n'
           '• Phiếu giao việc không còn tồn tại khi mở màn Tạo → màn Tạo báo “Không tìm thấy phiếu giao việc”.\n'
           '• Ở màn Tạo bấm Quay lại khi đã nhập → hộp cảnh báo chưa lưu của màn Tạo.\n'
           '• Phiếu nhập kết quả bị xóa sau đó → phiếu giao việc về Chờ thực hiện, nút Nhập kết quả hiện lại.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, chuyển về màn đăng nhập.',
       dacbiet='Nút là liên kết thật: chuột phải / chuột giữa mở được ở tab mới. Màn Tạo phiếu nhập kết quả không kiểm lại quyền khi mở '
               '(giữ như hệ thống ERP) — điều kiện nằm ở việc hiện nút.'),
   layout=dict(menu=MENU + ' => Nhập kết quả', shot=shot('45_import_create'),
               shot_caption='Màn Tạo phiếu nhập kết quả mở từ nút Nhập kết quả',
               note='Nút Nhập kết quả nằm ở cột Hành động của danh sách và ở chân trang chi tiết phiếu.'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút Nhập kết quả (dòng)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
        ['- Biểu tượng sổ bút, chú thích “Nhập kết quả”', '- Hiện khi đủ BR-10']),
       ('Nút Nhập kết quả (chi tiết)', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Nút xanh ở chân trang chi tiết, cùng điều kiện.'),
       ('Màn Tạo phiếu nhập kết quả', 'Label', 'Hiển thị', '–', 'Ẩn', '- Tiêu đề “Tạo phiếu nhập kết quả”; mở trong cùng tab.'),
       ('Ô Phiếu giao việc', 'Link', 'Read-only', '–', 'Theo dòng đã bấm', '- Mã phiếu giao việc chọn sẵn, không đổi được.'),
       ('Khối Thông tin khách hàng', 'Label', 'Read-only', '–', 'Theo phiếu giao việc', '- Khách hàng, địa chỉ, người liên hệ, người yêu cầu.'),
       ('Khối Chấm công', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Chấm công theo HRM và điều chỉnh theo thực tế.'),
       ('Khối File ảnh đính kèm', 'Table/Grid', 'Enable', '–', 'Trống', '- Ảnh công trình, ảnh biên bản bàn giao.'),
       ('Nút Lưu', 'Button', 'Enable', '–', 'Hiển thị', '- Lưu nháp phiếu nhập kết quả → phiếu giao việc “Đang nhập kết quả”.'),
       ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', 'Hiển thị', '- Gửi duyệt → phiếu giao việc “Đã nhập kết quả”.'),
       ('Nút Quay lại (màn Tạo)', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn trước; hỏi xác nhận nếu đã nhập.'),
       ('Cột Trạng thái sau khi lưu', 'Badge', 'Read-only', '–', 'Theo dữ liệu', '- Đang nhập kết quả (cam) / Đã nhập kết quả (xanh lá).'),
       ('Cột Hành động sau khi lưu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Ẩn Nhập kết quả, hiện Xem phiếu nhập kết quả.'),
   ],
   ev=[
       ('Mở danh sách / chi tiết', 'System',
        'Before:\n– Tính cờ Nhập kết quả cho từng phiếu.\nDuring:\n– Chưa có phiếu nhập kết quả + Chờ thực hiện + phiếu giao công tác đã '
        'duyệt + có người thực hiện + mình là người thực hiện (hoặc quyền “' + QN + '”).\nAfter:\n– Hiện / ẩn nút Nhập kết quả.'),
       ('Bấm Nhập kết quả', 'Click',
        'Before:\n– Nút chỉ hiện khi đủ BR-10; không hỏi xác nhận.\nDuring:\n– Bỏ bộ lọc đã ghi nhớ của danh sách.\n'
        'After:\n– Mở màn Tạo phiếu nhập kết quả, phiếu giao việc chọn sẵn.'),
       ('Mở màn Tạo phiếu nhập kết quả', 'System',
        'Before:\n– Không kiểm quyền (giữ như ERP).\nDuring:\n– Phiếu giao việc không tồn tại → “Không tìm thấy phiếu giao việc”.\n' + ERR + '\n'
        'After:\n– Hiển thị form với dữ liệu lấy từ phiếu giao việc.'),
       ('Lưu / Lưu và gửi duyệt phiếu nhập kết quả', 'Click',
        'Before:\n– Kiểm tra theo tài liệu Phiếu nhập kết quả.\nDuring:\n– Lỗi kiểm tra → báo lỗi tại màn Tạo, phiếu giao việc không đổi.\n'
        'After:\n– Phiếu giao việc chuyển Đang nhập kết quả / Đã nhập kết quả.\n– Ghi một dòng lịch sử “Thay đổi trạng thái” trong lịch '
        'sử của phiếu giao việc, kèm “Phiếu nhập kết quả <mã>”.\n– Gửi duyệt: báo người duyệt kết quả.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem phiếu nhập kết quả',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Mở chi tiết phiếu nhập kết quả của phiếu giao việc',
       mota='Với phiếu đã có phiếu nhập kết quả và đã rời trạng thái Chờ thực hiện, người dùng bấm Xem phiếu nhập kết quả để mở màn Chi tiết '
            'phiếu nhập kết quả (phiếu lập sớm nhất của phiếu giao việc). Nút hiện với mọi người thấy được dòng phiếu (không xét vai trò); '
            'màn đích tự kiểm quyền xem phiếu nhập kết quả.',
       tacnhan=TN, dieukien=DK + '\n4. Phiếu giao việc khác Chờ thực hiện và đã có phiếu nhập kết quả.',
       chinh='1. Người dùng bấm Xem phiếu nhập kết quả ở cột Hành động hoặc chân trang chi tiết phiếu giao việc.\n'
             '2. Hệ thống mở trang “Chi tiết phiếu nhập kết quả: <mã>” trong cùng tab.\n'
             '3. Màn chi tiết phiếu nhập kết quả tự kiểm quyền xem của nó và hiển thị dữ liệu chỉ đọc.\n'
             '4. Người dùng bấm Quay lại để trở về.',
       phu='• Phiếu Chờ thực hiện hoặc chưa có phiếu nhập kết quả → không có nút.\n'
           '• Người dùng không có quyền xem phiếu nhập kết quả → màn đích chuyển trang không tìm thấy.\n'
           '• Phiếu nhập kết quả đã bị xóa giữa chừng → màn đích báo không tìm thấy; quay lại danh sách nạp lại cờ.\n'
           '• Rời danh sách sang màn này thì bộ lọc danh sách không được giữ.',
       dacbiet='Nút là liên kết thật, mở được ở tab mới. Trước 03/11/2026 nút mở hệ thống ERP (#11998); nay mở màn HRM.'),
   layout=dict(menu=MENU + ' => Xem phiếu nhập kết quả', shot=shot('46_import_show'),
               shot_caption='Màn Chi tiết phiếu nhập kết quả mở từ nút Xem phiếu nhập kết quả',
               note='Nút nằm ở cột Hành động của danh sách và ở chân trang chi tiết phiếu giao việc.'),
   extra=[(shot('17b_detail_nkq'), 'Chi tiết phiếu Đang nhập kết quả — nút Xem phiếu nhập kết quả ở chân trang')],
   ui_kw=dict(required=False),
   ui=[
       ('Nút Xem phiếu nhập kết quả (dòng)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
        ['- Biểu tượng kính lúp trên tài liệu', '- Hiện khi đủ BR-11']),
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
        'Before:\n– Nút chỉ hiện khi đủ BR-11.\nDuring:\n– Bỏ bộ lọc đã ghi nhớ của danh sách.\n'
        'After:\n– Mở chi tiết phiếu nhập kết quả đầu tiên của phiếu.'),
       ('Mở màn đích', 'System',
        'Before:\n– Màn đích kiểm quyền xem phiếu nhập kết quả.\nDuring:\n– Không có quyền / không còn phiếu → trang không tìm thấy.\n'
        'After:\n– Hiển thị chi tiết.'),
       ('Bấm Quay lại ở màn đích', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Về màn trước; danh sách nạp lại từ trang 1.'),
   ])

# ------------------------------------------------------------ 2.11
fr(11, 'In danh sách', usecase=('FR-11', 'In danh sách', 'io', A_QL),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In danh sách phiếu giao việc theo bộ lọc',
       mota='Xem trước và in danh sách các phiếu trong phạm vi khớp bộ lọc (không phân trang), mẫu “DANH SÁCH PHIẾU GIAO VIỆC”, khổ ngang, '
            'letterhead công ty của người in, có chỗ ký Người lập. Tối đa 2.000 dòng — với phạm vi Tổng công ty (gần 10.000 phiếu) phải '
            'lọc trước khi in. Màn không có In từng phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng lọc danh sách (mục 2.2) rồi bấm In danh sách.\n'
             '2. Hệ thống lấy các phiếu trong phạm vi theo bộ lọc + sắp xếp, dựng bản in theo mẫu.\n'
             '3. Hệ thống mở cửa sổ “Xem trước danh sách phiếu giao việc”.\n'
             '4. Người dùng bấm In → hộp thoại in của trình duyệt.',
       phu='• Trên 2.000 dòng → không dựng bản in, ẩn nút In, hiện “Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in '
           'được. Vui lòng thu hẹp bộ lọc …”.\n'
           '• Không có dòng → bản in chỉ có tiêu đề cột.\n'
           '• Thiếu mẫu in → “Không tìm thấy mẫu in \"Danh sách phiếu giao việc\"”.\n'
           '• Bấm (x) / phím Esc → đóng cửa sổ.',
       dacbiet='Cột: STT, Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Người tạo, Người thực hiện, Thời '
               'gian dự kiến, Tổng công định mức (2 số lẻ), Trạng thái, Ngày tạo (kèm giờ). Người lập = người đang in.'),
   layout=dict(menu=MENU + ' => In danh sách', shot=shot('19_printlist'), shot_caption='Cửa sổ Xem trước danh sách phiếu giao việc (đã lọc)',
               note='Modal Xem trước được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('19b_print_over'), 'Danh sách vượt 2.000 dòng — câu nhắc thu hẹp bộ lọc, không có nút In')],
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
        'Before:\n– Áp phạm vi quyền + bộ lọc + sắp xếp đang có; không kiểm quyền riêng.\n'
        'During:\n– Đếm tổng; > 2.000 → dòng nhắc vượt trần.\n– Thiếu mẫu in → thông báo lỗi.\n' + ERR + '\n'
        'After:\n– Hiển thị bản xem trước danh sách.'),
       ('Bấm In', 'Click', 'Before:\n– Bản in đã dựng.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x) / phím Esc', 'Click', 'Before:\n– Không hỏi.\nAfter:\n– Đóng cửa sổ, danh sách giữ nguyên.'),
       ('Mở cửa sổ', 'System', 'Before:\n– Letterhead theo công ty người in.\nAfter:\n– Hiển thị bản in khổ ngang.'),
   ])

# ------------------------------------------------------------ 2.12
fr(12, 'Xuất Excel danh sách', usecase=('FR-12', 'Xuất Excel danh sách', 'io', A_QL),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu giao việc ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ phiếu trong phạm vi khớp bộ lọc (không phân trang) ra file Excel. File dựng ngay trên '
            'trình duyệt theo từng đợt 2.000 dòng, có dòng tiến độ; cột STT luôn đứng đầu; ô Tổng công định mức là ô số.',
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
       dacbiet='Không giới hạn số dòng (lấy theo từng đợt 2.000 dòng; phạm vi Tổng công ty gần 10.000 dòng mất vài chục giây). Tên file, '
               'tiêu đề giống lối vào Phiếu giao việc được giao. Khóa nút Xuất Excel trong lúc xuất.'),
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
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất; dữ liệu là phạm vi quyền + bộ lọc.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc + sắp xếp theo từng đợt, hiện tiến độ.\n– Không có dòng → “Không có dữ liệu để xuất”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.\n' + ERR + '\n'
        'After:\n– Tải file, báo “Xuất Excel thành công.”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu giao việc; không lặp lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng', lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi danh sách', [
        '– Phiếu giao việc gốc (không lấy phiếu duyệt kết quả), trạng thái khác Hủy.',
        '– Tổng công ty: mọi phiếu; Công ty: công ty đang làm việc + mình tạo; Phòng ban: phòng mình quản lý trong công ty đang làm việc + '
        'mình tạo; không quyền Xem: mình tạo, cộng mình thực hiện nếu là người thực hiện ở ít nhất 1 phiếu.',
        '– Nhiều mức → áp mức rộng nhất; không đặc cách Super admin; ô lọc Công ty / Phòng ban chỉ lọc thêm trong phạm vi.'],
     ['Xem danh sách', 'Tìm kiếm', 'In', 'Xuất Excel']),
    ('BR-02', 'Quyền lập phiếu theo nguồn', [
        '– Hợp đồng / phụ lục bổ sung: quyền “%s” + phòng tiếp nhận = phòng mình + hợp đồng “Có hiệu lực”.' % QT,
        '– Phiếu bảo hành: quyền “%s” + “Đã duyệt” (không xét phòng tiếp nhận).' % QT,
        '– Yêu cầu lắp đặt bàn giao / giao việc khác: phòng tiếp nhận = phòng mình + “Chờ giao việc” (không cần quyền).',
        '– Trưởng phòng có nhân viên phòng mình còn hàng giữ / mượn / nhập thẳng quá hạn: bị chặn lưu (trừ Super admin).'],
     ['Tạo phiếu giao việc']),
    ('BR-03', 'Số lượng còn giao', [
        '– SL còn = SL kỹ thuật trên chứng từ − SL phụ lục giảm − SL đã ghi nhận ở tiến độ giao việc (không có tiến độ thì SL các phiếu '
        'giao việc hoàn thành 100%); âm hiển thị 0.',
        '– Chỉ hiện dịch vụ / vật tư còn SL > 0; thiết bị sửa chữa hết SL thì khóa ô SL.',
        '– Phiếu bảo hành: chỉ tính tiến độ đã duyệt; được giao khi còn sản phẩm chưa xử lý / chưa đang giao.'],
     ['Tạo phiếu giao việc', 'Xóa']),
    ('BR-04', 'Kiểm tra form', [
        '– Ngày dự kiến bắt đầu / kết thúc bắt buộc, ≥ hôm nay, kết thúc ≥ bắt đầu.',
        '– SL giao lần này 0 – SL còn (thiết bị, dịch vụ, gói bảo dưỡng, lắp đặt, bán thêm là số nguyên); ghi chú dòng, tên công phụ ≤ 255.',
        '– Công phụ P3: tên và ĐM công bắt buộc; mọi lỗi báo cùng lúc, máy chủ kiểm lại y hệt (kể cả vượt SL khi 2 người lưu cùng lúc).'],
     ['Tạo phiếu giao việc']),
    ('BR-05', 'Lưu là duyệt', [
        '– Không có nháp: lưu xong phiếu ở Chờ thực hiện, chưa gắn phiếu giao công tác, chưa có người thực hiện.',
        '– Mã <mã công ty người lập>.PGV.<năm><6 số>; công ty / phòng ban của phiếu = của người lập.',
        '– Chứng từ nguồn: hợp đồng / phụ lục trừ SL còn; phiếu bảo hành bỏ đánh dấu chờ giao khi hết; yêu cầu lắp đặt → Đang giao việc '
        'khi giao hết; yêu cầu giao việc khác → Đã giao việc.'],
     ['Tạo phiếu giao việc']),
    ('BR-06', 'Công thức tổng công định mức', [
        '– Bảo hành = Σ ĐM công thiết bị bảo hành; Sửa chữa (I) = Σ ĐM công thiết bị có SL giao ≠ 0; Bảo dưỡng (II) = Σ ĐM công dịch vụ '
        'bảo dưỡng có SL ≠ 0.',
        '– Lắp đặt: SL tính công khoán = làm tròn lên (SL bàn giao ÷ SL người tính công, thiếu thì 1); Tổng dòng = SL tính công khoán × '
        'ĐM công.',
        '– Công chính = bảo hành + sửa chữa + bảo dưỡng + lắp đặt + dịch vụ đính kèm; Công phụ = Σ ĐM công P3; Tổng = Công chính + Công '
        'phụ, 2 số lẻ; máy chủ tính lại khi lưu.'],
     ['Tạo phiếu giao việc', 'Xem chi tiết']),
    ('BR-07', 'Tổng hợp dịch vụ, vật tư', [
        '– II. Tổng dịch vụ trả tiền: gộp SL dịch vụ bảo hành + sửa chữa theo dịch vụ, gói bảo dưỡng theo dịch vụ bảo dưỡng (2 danh mục '
        'tách riêng).',
        '– III. Tổng hợp vật tư phải giao: gộp SL vật tư bảo hành + sửa chữa + bảo dưỡng + bán thêm theo hàng hóa.',
        '– V. Chi phí khác: chép từ hợp đồng, chỉ đọc.'],
     ['Tạo phiếu giao việc', 'Xem chi tiết']),
    ('BR-08', 'Điều kiện và tác động Xóa', [
        '– Người tạo phiếu + Chờ thực hiện + chưa gắn phiếu giao công tác (không đặc cách Super admin).',
        '– Xóa = chuyển Hủy; xóa tiến độ giao việc; yêu cầu giao việc khác về Chờ giao việc; yêu cầu lắp đặt tính lại trạng thái; '
        'phiếu bảo hành bật lại đánh dấu chờ giao.'],
     ['Xóa']),
    ('BR-09', 'Luồng trạng thái', [
        '– Chờ thực hiện → Đang nhập kết quả (lưu nháp phiếu nhập kết quả) → Đã nhập kết quả (gửi duyệt) → Đang duyệt kết quả → Đã '
        'duyệt kết quả → Chờ BKS duyệt kết quả → Đang đề nghị thanh toán → Đã thanh toán.',
        '– Xóa phiếu nhập kết quả → về Chờ thực hiện. Xóa phiếu giao việc → Hủy.',
        '– Phiếu giao công tác chứa phiếu: lập → chờ duyệt, duyệt → ghi người thực hiện; không duyệt → về chưa gắn.'],
     ['Xem danh sách', 'Nhập kết quả', 'Xóa']),
    ('BR-10', 'Điều kiện Nhập kết quả', [
        '– Chưa có phiếu nhập kết quả; Chờ thực hiện; phiếu giao công tác đã duyệt; có người thực hiện.',
        '– Người đăng nhập là người thực hiện, hoặc có quyền “%s” (hiện không có tác dụng ở HRM).' % QN],
     ['Nhập kết quả']),
    ('BR-11', 'Điều kiện Xem phiếu nhập kết quả', [
        '– Trạng thái khác Chờ thực hiện và Hủy, đã có phiếu nhập kết quả; mở phiếu nhập kết quả lập sớm nhất.'],
     ['Xem phiếu nhập kết quả']),
    ('BR-12', 'Quy tắc ghi lịch sử', [
        '– “Tạo mới” khi lập phiếu ở HRM (số phiếu, khách hàng, ngày dự kiến, tổng công định mức, ghi chú).',
        '– “Thay đổi trạng thái” khi phiếu nhập kết quả lưu / gửi duyệt / bị xóa / được duyệt (kèm mã phiếu nhập kết quả) và khi Xóa.',
        '– Xem, lọc, in, xuất không ghi mốc; phiếu lập ở ERP không có mốc cũ.'],
     ['Lịch sử', 'Tạo phiếu giao việc', 'Xóa', 'Nhập kết quả']),
    ('BR-13', 'Hiển thị, in, xuất', [
        '– Người thực hiện: trưởng nhóm, không có thì người đầu danh sách; Người yêu cầu: người lập hợp đồng / phiếu bảo hành → yêu cầu '
        'giao việc khác → yêu cầu lắp đặt.',
        '– Tổng công định mức 2 số lẻ; bằng 0 thì để trống trên màn (bản in ghi 0.00).',
        '– In tối đa 2.000 dòng; Xuất Excel không giới hạn, rỗng không ra file; bộ lọc ghi nhớ 10 phút khi mở chi tiết rồi quay lại.'],
     ['Xem danh sách', 'In', 'Xuất Excel', 'Tìm kiếm']),
    ('BR-14', 'Duy nhất, chuẩn hóa nhập', [
        '– Mã phiếu tự sinh, không trùng; không có trường nhập duy nhất nên không có quy tắc trùng giữa các phiếu.',
        '– Một chứng từ nguồn lập được nhiều phiếu giao việc (giao nhiều lần) cho đến khi hết SL còn.',
        '– Tên công phụ bỏ khoảng trắng đầu / cuối khi lưu; ô tìm / lọc chữ bỏ khoảng trắng đầu / cuối.'],
     ['Tạo phiếu giao việc', 'Tìm kiếm']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Phiếu giao việc (số lượng đã giao, trạng thái phiếu, người thực hiện, phiếu '
    'nhập kết quả, chứng từ nguồn).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'CSKH sau bán', 'Phiếu chờ giao việc (nút Tạo phiếu giao việc mở form màn này; SL còn trừ khi lưu, trả lại khi Xóa)',
     'CSKH sau bán -> Giao việc'),
    ('2', 'CSKH sau bán', 'Phiếu giao việc được giao (cùng dữ liệu, chỉ phiếu mình là người thực hiện; dùng chung màn chi tiết)',
     'CSKH sau bán -> Giao việc'),
    ('3', 'Công việc', 'Phiếu giao công tác (chọn phiếu giao việc Chờ thực hiện; khi duyệt ghi người thực hiện + cờ đã duyệt; gắn rồi thì '
                       'không Xóa được phiếu)', 'Công việc -> Phân công công việc'),
    ('4', 'CSKH sau bán', 'Phiếu nhập kết quả (đích của Nhập kết quả / Xem phiếu nhập kết quả; lưu, gửi duyệt, xóa, duyệt đổi trạng thái '
                          'phiếu giao việc và ghi lịch sử)', 'CSKH sau bán -> Giao việc'),
    ('5', 'Bán hàng', 'Danh sách hợp đồng dịch vụ, phụ lục bổ sung (nguồn lập phiếu; SL còn trừ / trả theo phiếu)',
     'Bán hàng -> Bán dịch vụ -> HĐ Sửa chữa - Bảo dưỡng - Bảo trì'),
    ('6', 'CSKH sau bán', 'Phiếu bảo hành (nguồn lập phiếu; đánh dấu chờ giao tắt khi giao hết, bật lại khi Xóa)',
     'CSKH sau bán -> Kiểm tra bảo hành sửa chữa'),
    ('7', 'Bán hàng', 'YC lắp đặt, bàn giao (nguồn lập phiếu, có nút Tạo phiếu giao việc; trạng thái Đang giao việc / Chờ giao việc tính '
                      'lại khi lưu và khi Xóa)', 'Bán hàng -> Yêu cầu -> Lắp đặt - BH - SC'),
    ('8', 'Bán hàng', 'YC giao việc khác (nguồn lập phiếu, có nút Tạo phiếu giao việc; Đã giao việc khi lưu, về Chờ giao việc khi Xóa)',
     'Bán hàng -> Yêu cầu -> Lắp đặt - BH - SC'),
    ('9', 'CSKH sau bán', 'Báo cáo theo dõi lắp đặt - bàn giao - sửa chữa - bảo dưỡng (đọc phiếu giao việc, mã phiếu mở chi tiết)',
     'CSKH sau bán -> Báo cáo'),
    ('10', 'Hệ thống ERP', 'Hợp đồng bán hàng hãng (Số hợp đồng của phiếu lắp đặt) và các bước Chờ BKS duyệt kết quả, đề nghị thanh toán '
                           '(đổi trạng thái phiếu giao việc)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
