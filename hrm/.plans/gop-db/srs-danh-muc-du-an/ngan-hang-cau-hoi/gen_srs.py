# -*- coding: utf-8 -*-
"""Sinh "SRS - Ngân hàng câu hỏi khảo sát.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/ngan-hang-cau-hoi/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): ngan-hang-cau-hoi_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/questions/{index.vue, add.vue, _id/index.vue, _id/edit.vue, components/QuestionForm.vue}
      components/modals/AddSurveyQuestionModal.vue (popup Chọn câu hỏi con)
      components/modal/confirm-question-{delete,lock,unlock}.vue
      components/subsystem-menu/master-data.js (menu) · components/subsystems.js (phân hệ)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/questions)
      Http/Controllers/Api/V1/SurveyQuestionController.php · Services/SurveyQuestionService.php
      Http/Requests/SurveyQuestion/SurveyQuestionRequest.php · Entities/SurveyQuestion.php
      Transformers/SurveyQuestionsResource/*
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 982, 997)
Màn liên quan: Phiếu thu thập thông tin (.plans/gop-db/srs-danh-muc-du-an/phieu-thu-thap-thong-tin/)
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))

import srs_docx_lib  # noqa: E402
from srs_docx_lib import SrsDoc  # noqa: E402

# python-docx dùng lại 1 quan hệ (rId) cho các hyperlink trùng URL -> selfcheck đếm thiếu liên kết khi
# không qua Word (save(update_fields=False)). Ép mỗi đoạn "Quy tắc chung" có rId riêng như Word lưu.
_orig_add_hyperlink = srs_docx_lib.add_hyperlink


def _add_hyperlink_own_rel(paragraph, url, text):
    part = paragraph.part

    def _relate_new(target, reltype, is_external=False):
        rid = part.rels._next_rId
        part.rels.add_relationship(reltype, target, rid, is_external)
        return rid

    part.relate_to = _relate_new
    try:
        return _orig_add_hyperlink(paragraph, url, text)
    finally:
        del part.relate_to


srs_docx_lib.add_hyperlink = _add_hyperlink_own_rel

OUT = os.path.join(HERE, 'SRS - Ngân hàng câu hỏi khảo sát.docx')
SHOTS = os.path.join(HERE, 'ngan-hang-cau-hoi_shots')
MENU = 'Phân hệ Danh mục dùng chung => Ngân hàng câu hỏi khảo sát'

A_QL = 'Người quản lý ngân hàng câu hỏi khảo sát (Q1)'
A_XEM = 'Người xem ngân hàng câu hỏi khảo sát (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/questions',
           full_url='https://<host-hrm>/assign/questions', img_prefix='nganhangcauhoi_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện (Playwright).
# Ô phân hệ trong danh sách phân hệ hiển thị tên rút gọn "Danh mục".
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Danh mục dùng chung': 'phanhe', 'Ngân hàng câu hỏi khảo sát': 'nganhang',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Thêm câu hỏi': 'themcauhoi', 'Sửa': 'sua', 'Tiêu đề câu hỏi': 'tieude',
    'Xóa': 'xoa', 'Khóa': 'khoa', 'Mở khóa': 'mokhoa', 'Xuất Excel': 'xuat',
}.items()})

d.title_block('Ngân hàng câu hỏi khảo sát')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Ngân hàng câu hỏi khảo sát thuộc phân hệ '
    'Danh mục dùng chung, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Mô tả cách khai câu hỏi theo 10 loại dữ liệu, phạm vi áp dụng (Tất cả / Theo ứng dụng), danh sách '
    'đáp án và câu hỏi nhóm (câu hỏi cha – con).',
    'Làm rõ ràng buộc với màn Phiếu thu thập thông tin: phiếu chỉ lấy câu hỏi đang Hoạt động của ngân '
    'hàng; câu hỏi đã dùng trong phiếu thì không xoá được, câu hỏi nhóm đã dùng thì không đổi được câu '
    'hỏi con.',
    'Làm rõ quy tắc chống trùng câu hỏi và điều kiện hiện các thao tác Sửa, Xóa, Khóa, Mở khóa.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Câu hỏi khảo sát', 'Câu hỏi dùng chung để dựng mẫu Phiếu thu thập thông tin. Bảng không có cột '
     'mã; cột định danh là Tiêu đề câu hỏi.'),
    ('Mã câu hỏi', 'Mã do hệ thống tự gán theo số thứ tự bản ghi, dạng cau_hoi_<số>. Hiển thị ở popup '
     'chọn câu hỏi, thư viện câu hỏi của phiếu và dùng trong logic hiển thị.'),
    ('Loại dữ liệu', 'Kiểu câu trả lời: Text ngắn, Text dài, Số, Dropdown, Radio 1 lựa chọn, Checkbox '
     'nhiều lựa chọn, Ngày, File, Có / Không, Nhóm câu hỏi.'),
    ('Phạm vi câu hỏi', '“Tất cả”: dùng được cho mọi Ứng dụng. “Theo ứng dụng”: chỉ dùng cho 1 Ứng dụng '
     'đã chọn.'),
    ('Ứng dụng', 'Danh mục Ứng dụng (phân hệ CSKH trước bán); mỗi Ứng dụng có 1 mẫu phiếu Hoạt động.'),
    ('Câu hỏi nhóm (Nhóm câu hỏi)', 'Câu hỏi cha gồm danh sách câu hỏi con chọn từ ngân hàng. Khi đưa vào '
     'phiếu sẽ thành 1 Group chứa các câu hỏi con.'),
    ('Danh sách đáp án', 'Các lựa chọn của câu hỏi loại Dropdown, Radio, Checkbox.'),
    ('Trạng thái Khóa', 'Câu hỏi ngừng sử dụng: không hiện trong thư viện câu hỏi của phiếu, không chọn '
     'làm câu hỏi con, không sửa được. Có thể Mở khóa lại.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục câu hỏi khảo sát',
     'Xem danh sách, xem chi tiết; tạo mới, sửa, xóa, khóa / mở khóa câu hỏi; xuất Excel. Cũng là '
     'quyền cần có để “Tạo nhanh” câu hỏi từ màn Phiếu thu thập thông tin.'),
    ('Q2', 'Xem danh mục câu hỏi khảo sát',
     'Xem danh sách, tìm kiếm, xem chi tiết. Không được thay đổi dữ liệu, không xuất Excel.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền xem '
    'được toàn bộ câu hỏi của hệ thống.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách câu hỏi', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới câu hỏi', '✅', '❌', '❌'),
    ('FR-05 Chọn câu hỏi con', '✅', '❌', '❌'),
    ('FR-06 Chỉnh sửa câu hỏi', '✅', '❌', '❌'),
    ('FR-07 Xem chi tiết câu hỏi', '✅', '✅', '❌'),
    ('FR-08 Xóa câu hỏi', '✅', '❌', '❌'),
    ('FR-09 Khóa / Mở khóa câu hỏi', '✅', '❌', '❌'),
    ('FR-10 Xuất Excel', '✅', '❌', '❌'),
], widths=[3.0, 0.8, 0.8, 1.4])

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_QL, [0, 1, 2, 3, 4, 5]),
     (A_XEM, [0])],
    [('FR-01', 'Xem danh sách câu hỏi', 'view'),
     ('FR-04', 'Tạo mới câu hỏi', 'crud'),
     ('FR-06', 'Chỉnh sửa câu hỏi', 'crud'),
     ('FR-08', 'Xóa câu hỏi', 'action'),
     ('FR-09', 'Khóa / Mở khóa câu hỏi', 'action'),
     ('FR-10', 'Xuất Excel danh sách câu hỏi', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-07', 'Xem chi tiết câu hỏi', 'view', 'extend', [0], None),
     ('FR-05', 'Chọn câu hỏi con', 'view', 'extend', [1, 2], None)],
    'Sơ đồ Use Case tổng quan màn Ngân hàng câu hỏi khảo sát')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách câu hỏi')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Ngân hàng câu hỏi khảo sát tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách câu hỏi khảo sát',
    mota='Hiển thị toàn bộ câu hỏi của ngân hàng kèm loại dữ liệu, phạm vi, Ứng dụng, mô tả, người tạo / '
         'cập nhật, trạng thái và các thao tác trên từng dòng.',
    tacnhan='Người quản lý / người xem ngân hàng câu hỏi khảo sát; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ Danh mục dùng chung → Ngân hàng câu hỏi khảo sát.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, câu hỏi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Tiêu đề câu hỏi → mở màn Xem chi tiết (FR-07); chuột phải để mở ở tab mới.\n'
        '• Bấm tiêu đề cột Tiêu đề câu hỏi, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm lại để '
        'đảo chiều.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách câu hỏi lúc mới truy cập')
d.figure(shot('01b-hanh-dong.png'), 'Cột Trạng thái và cột Hành động (cuộn bảng sang phải)',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Ngân hàng câu hỏi khảo sát”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở màn Tạo mới (FR-04).'),
    ('Nút Xuất Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Chọn trường xuất file (FR-10). Bị khoá trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Tiêu đề câu hỏi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được; tối đa 2 dòng. Là liên kết mở màn Xem chi tiết.'),
    ('Cột Loại dữ liệu', 'Table/Grid', 'Read-only', '10 loại', 'Theo dữ liệu', '–'),
    ('Cột Phạm vi câu hỏi', 'Table/Grid', 'Read-only', 'Tất cả / Theo ứng dụng', 'Theo dữ liệu', '–'),
    ('Cột Ứng dụng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Trống khi phạm vi “Tất cả”.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự Sửa, Xóa, Khóa / Mở khóa. Thao tác không dùng được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và câu hỏi đang Hoạt động (FR-06).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và câu hỏi chưa dùng trong mẫu phiếu nào, không phải câu hỏi nhóm đang có câu '
     'hỏi con (FR-08).'),
    ('Nút Khóa / Mở khóa (ổ khoá)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1. Hoạt động: Khóa; Khóa: Mở khóa (FR-09).'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', 'N là tổng số bản ghi khớp bộ lọc.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5 / 10 / 20 / 50', '10', 'Đổi thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Về đầu / lùi / số trang / tiến / về cuối.'),
    ('Thanh cuộn ngang', 'Table/Grid', 'Enable', '–', 'Hiển thị khi bảng tràn',
     'Có ở cả phía trên và phía dưới bảng.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị ngay khi vào màn', 'Tắt khi nạp xong.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'During:\n– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có).\n'
     '– Nạp cấu hình cột đã lưu của người dùng.\n'
     'After:\n– Hiển thị trang 1, 10 dòng, câu hỏi mới tạo lên đầu.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Tiêu đề câu hỏi', 'Click', 'After:\n– Mở màn Xem chi tiết câu hỏi (FR-07).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Ngân hàng câu '
           'hỏi khảo sát tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc câu hỏi',
    mota='Tìm nhanh theo tiêu đề câu hỏi hoặc tên người tạo; lọc nâng cao theo Ứng dụng, Loại dữ liệu, '
         'Trạng thái.',
    tacnhan='Người quản lý / người xem ngân hàng câu hỏi khảo sát; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách câu hỏi.',
    chinh='1. Người dùng nhập từ khoá vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc (danh sách Ứng dụng chỉ nạp khi mở lần đầu).\n'
          '3. Chọn giá trị ở các ô lọc: chọn xong hệ thống tự lọc lại ngay.\n'
          '4. Bảng hiển thị kết quả từ trang 1.',
    phu='• Bấm Làm mới → xoá hết điều kiện lọc, trả về danh sách ban đầu.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối lọc, điều kiện đang chọn vẫn giữ.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”',
    dacbiet=None)
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Placeholder “Tìm theo tiêu đề câu hỏi, người tạo”. Tìm gần đúng theo Tiêu đề câu hỏi hoặc tên '
     'Người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Ứng dụng', 'Dropdown', 'Enable', 'Danh sách Ứng dụng đang Hoạt động', 'Không', 'Trống',
     'Lọc câu hỏi thuộc đúng Ứng dụng (phạm vi “Theo ứng dụng”).'),
    ('Loại dữ liệu', 'Dropdown', 'Enable', '10 loại', 'Không', 'Trống', '–'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Trống', '–'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter', 'Click / Keypress',
     'Before:\n– Lấy từ khoá người dùng nhập.\n'
     'After:\n– Lọc theo toàn bộ điều kiện; hiển thị trang 1.'),
    ('Đổi giá trị một ô trong khối lọc', 'Change',
     'After:\n– Tự lọc lại ngay theo toàn bộ điều kiện đang chọn, quay về trang 1.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, sắp xếp mặc định, hiển thị trang 1.'),
])

# ---------------------------------------------------------------- 2.3
d.h3('2.3 Cài đặt bộ lọc và tuỳ chỉnh cột')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', actor='Người dùng đã đăng nhập',
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột')
d.p('2.3.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột hiển thị',
    mota='Mỗi người dùng tự chọn trường lọc nào hiện trong khối Tìm kiếm nâng cao, cột nào hiện '
         'trên bảng, và sắp xếp thứ tự bằng kéo thả. Cấu hình lưu riêng theo từng người.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách câu hỏi.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột STT, Tiêu đề câu hỏi và Hành động luôn hiện, không bỏ tích được (hiển thị xám + ổ khoá).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('03b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('03c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khoá hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '3 trường', 'Không', 'Theo cấu hình đã lưu',
     'Ứng dụng, Loại dữ liệu, Trạng thái. Mỗi dòng: số thứ tự, biểu tượng kéo ⠿, ô tích, tên trường.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '12 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột STT, Tiêu đề câu hỏi, Hành động bị khoá (luôn hiện).'),
    ('Nút Lưu (Tuỳ chỉnh cột)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình cột.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Kéo biểu tượng ⠿', 'Drag', 'After:\n– Đổi thứ tự trường / cột trong danh sách.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cấu hình theo người dùng đang đăng nhập; đóng cửa sổ; vẽ lại khối lọc / bảng.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về cấu hình mặc định của màn.'),
])

# ---------------------------------------------------------------- 2.4
SAVE_DURING = (
    '– Tiêu đề câu hỏi trống → “Bắt buộc phải nhập”; quá 1.000 ký tự → “Vui lòng nhập tối đa 1000 ký '
    'tự.”\n'
    '– Chưa chọn Loại dữ liệu → “Bắt buộc phải nhập”.\n'
    '– Phạm vi “Theo ứng dụng” mà chưa chọn Ứng dụng → “Bắt buộc phải chọn ứng dụng”; Ứng dụng không '
    'còn → “Ứng dụng không tồn tại”.\n'
    '– Dòng đáp án để trống → “Bắt buộc phải nhập” dưới dòng đó.\n'
    '– Loại “Nhóm câu hỏi” mà chưa chọn câu hỏi con → “Câu hỏi con chưa được lựa chọn”.\n'
    '– Câu hỏi con đã bị xoá → “Câu hỏi con \"cau_hoi_<số>\" không còn tồn tại, vui lòng chọn câu hỏi '
    'khác”; đang bị khoá → “Câu hỏi con \"cau_hoi_<số>\" đang bị khóa, vui lòng chọn câu hỏi khác”.\n'
    '– Trùng câu hỏi đã có (cùng tiêu đề không phân biệt hoa thường, cùng loại, cùng tập đáp án, cùng '
    'phạm vi / Ứng dụng) → “Câu hỏi đã tồn tại trong phạm vi này (trùng nội dung, loại dữ liệu và danh '
    'sách đáp án)” dưới ô Tiêu đề.')

d.h3('2.4 Tạo mới câu hỏi')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới câu hỏi', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới câu hỏi')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Tạo mới câu hỏi khảo sát',
    mota='Thêm một câu hỏi mới vào ngân hàng: chọn phạm vi, Ứng dụng (nếu theo ứng dụng), loại dữ liệu, '
         'nhập tiêu đề, mô tả; loại lựa chọn thì nhập danh sách đáp án, loại Nhóm câu hỏi thì chọn câu hỏi con.',
    tacnhan='Người quản lý ngân hàng câu hỏi khảo sát',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở màn “Thêm mới câu hỏi”: Phạm vi áp dụng mặc định “Theo ứng dụng”, Trạng thái '
          'mặc định Hoạt động.\n'
          '3. Người dùng chọn Ứng dụng (khi phạm vi Theo ứng dụng), Loại dữ liệu, nhập Tiêu đề câu hỏi, Mô tả.\n'
          '4. Loại Dropdown / Radio / Checkbox: hệ thống tạo sẵn 2 dòng đáp án; người dùng nhập, bấm '
          '“Thêm đáp án” để thêm dòng, nút “–” để bỏ dòng.\n'
          '5. Loại Nhóm câu hỏi: bấm “Thêm câu hỏi” để chọn câu hỏi con (FR-05), kéo để sắp thứ tự.\n'
          '6. Người dùng bấm Lưu (hoặc Lưu và tiếp tục).\n'
          '7. Hệ thống kiểm tra dữ liệu, ghi câu hỏi cùng đáp án / câu hỏi con.\n'
          '8. Thông báo “Thêm mới thành công”; Lưu thì về màn danh sách, Lưu và tiếp tục thì xoá trắng '
          'form để nhập câu tiếp.',
    phu='• Đổi Phạm vi sang “Tất cả” → ẩn ô Ứng dụng và bỏ Ứng dụng đã chọn.\n'
        '• Đổi Loại dữ liệu sang loại không phải lựa chọn → bỏ danh sách đáp án.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).\n'
        '• Bấm Quay lại → về màn danh sách, không lưu.',
    dacbiet='Không cho tạo 2 câu hỏi trùng nhau trong cùng phạm vi (xem BR-03). Câu hỏi mới luôn có '
            'Mã cau_hoi_<số> do hệ thống gán.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('04-tao-moi.png'),
         shot_caption='Màn Thêm mới câu hỏi')
d.figure(shot('04b-tao-moi-loi.png'), 'Bấm Lưu khi chưa nhập các trường bắt buộc', width_in=6.2)
d.figure(shot('04c-dap-an.png'), 'Loại Radio 1 lựa chọn — khối Danh sách đáp án', width_in=6.2)
d.figure(shot('04d-nhom-cau-hoi.png'), 'Loại Nhóm câu hỏi — khối Danh sách câu hỏi con', width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
FORM_ROWS = [
    ('Phạm vi áp dụng', 'Dropdown', 'Enable', 'Tất cả / Theo ứng dụng', 'Có', 'Theo ứng dụng',
     'Không có nút xoá chọn.'),
    ('Ứng dụng', 'Dropdown', 'Enable / Ẩn', 'Ứng dụng đang Hoạt động', 'Có khi phạm vi “Theo ứng dụng”',
     'Trống', 'Chỉ hiện khi phạm vi “Theo ứng dụng”; icon ⓘ mô tả khái niệm.'),
    ('Loại dữ liệu', 'Dropdown', 'Enable', '10 loại', 'Có', 'Trống',
     'Text ngắn, Text dài, Số, Dropdown, Radio 1 lựa chọn, Checkbox nhiều lựa chọn, Ngày, File, '
     'Có / Không, Nhóm câu hỏi.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động', '–'),
    ('Tiêu đề câu hỏi', 'Textarea', 'Enable', '1–1.000 ký tự', 'Có', 'Trống',
     'Placeholder “Nhập tiêu đề câu hỏi”.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Placeholder “Nhập mô tả”.'),
    ('Danh sách đáp án', 'Table/Grid', 'Enable / Ẩn', '–', 'Có với Dropdown / Radio / Checkbox',
     '2 dòng trống', 'Chỉ hiện với loại lựa chọn. Cột STT, Nội dung đáp án, nút “–” xoá dòng; nút '
     '“Thêm đáp án”. Chưa có dòng nào → “Chưa có đáp án nào. Vui lòng thêm đáp án.”'),
    ('Danh sách câu hỏi con', 'Table/Grid', 'Enable / Ẩn', 'Câu hỏi đang Hoạt động', 'Có với Nhóm câu hỏi',
     'Trống', 'Chỉ hiện với loại Nhóm câu hỏi. Mỗi dòng: số thứ tự, tiêu đề, “Loại: … · Mã: cau_hoi_<số>”, '
     'biểu tượng kéo, nút xoá khỏi danh sách; nút “Thêm câu hỏi”.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ ngay dưới ô bị lỗi.'),
]
d.ui_table([('Tiêu đề trang “Thêm mới câu hỏi”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
           + FORM_ROWS + [
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu rồi về màn danh sách.'),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu rồi xoá trắng form để nhập câu tiếp. Chỉ có ở Tạo mới.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách, không lưu.'),
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'Before:\n– Nút chỉ hiển thị khi có quyền Q1.\n'
     'After:\n– Mở màn Thêm mới, Phạm vi = Theo ứng dụng, Trạng thái = Hoạt động.'),
    ('Đổi Loại dữ liệu', 'Change',
     'After:\n– Loại lựa chọn: hiện khối đáp án, tạo sẵn 2 dòng nếu đang trống.\n'
     '– Loại khác: ẩn và bỏ danh sách đáp án. Nhóm câu hỏi: hiện khối câu hỏi con.'),
    ('Bấm Lưu / Lưu và tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin”, không thực hiện bước After.\n'
     'After:\n– Ghi câu hỏi (Phạm vi “Tất cả” thì không gắn Ứng dụng), đáp án theo thứ tự nhập (bỏ dòng '
     'trống), câu hỏi con theo thứ tự đã sắp; ghi người tạo, thời điểm tạo.\n'
     '– Thông báo “Thêm mới thành công”.\n'
     '– Lưu: về màn danh sách. Lưu và tiếp tục: xoá trắng form.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chọn câu hỏi con')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn câu hỏi con', 'view', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chọn câu hỏi con')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', anchor='search')
d.intro_table(
    ten='Chọn câu hỏi con cho câu hỏi nhóm',
    mota='Popup “Chọn câu hỏi” liệt kê các câu hỏi đang Hoạt động của ngân hàng để chọn làm câu hỏi con '
         'của câu hỏi loại Nhóm câu hỏi.',
    tacnhan='Người quản lý ngân hàng câu hỏi khảo sát',
    dieukien='Đang ở màn Tạo mới / Sửa câu hỏi, Loại dữ liệu = Nhóm câu hỏi.',
    chinh='1. Người dùng bấm “Thêm câu hỏi” ở khối Danh sách câu hỏi con.\n'
          '2. Hệ thống mở popup “Chọn câu hỏi”, nạp trang 1 (10 dòng) các câu hỏi đang Hoạt động, bỏ câu '
          'hỏi đang sửa và các câu đã chọn.\n'
          '3. Người dùng tìm theo từ khoá (nút kính lúp), tích chọn nhiều dòng rồi bấm “Chọn”; hoặc bấm '
          'vào 1 dòng để thêm ngay dòng đó.\n'
          '4. Hệ thống thêm các câu đã chọn vào cuối Danh sách câu hỏi con và đóng popup.',
    phu='• Bấm nút làm mới → xoá từ khoá, nạp lại trang 1.\n'
        '• Tích ô đầu bảng → chọn / bỏ chọn tất cả dòng đang hiện.\n'
        '• Không có dữ liệu → “Chưa có dữ liệu”.',
    dacbiet=None)
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Thêm câu hỏi', modal='Chọn câu hỏi',
         shot=shot('05-chon-cau-hoi-con.png'), shot_caption='Popup Chọn câu hỏi')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Chọn câu hỏi”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Ô tìm kiếm', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Tìm theo tiêu đề câu hỏi, người tạo.'),
    ('Nút Tìm kiếm / Làm mới', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Chọn', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thêm các dòng đã tích và đóng popup.'),
    ('Bảng câu hỏi', 'Table/Grid', 'Enable', 'Câu hỏi đang Hoạt động', 'Không', 'Trang 1',
     'Cột ô tích, STT, Tiêu đề câu hỏi, Loại câu hỏi, Mã câu hỏi.'),
    ('Dòng “Tổng số bản ghi: N”, Số dòng/trang, Phân trang', 'Pagination', 'Enable', '–', '–', '10 dòng', '–'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở popup', 'System',
     'After:\n– Nạp câu hỏi đang Hoạt động, bỏ câu hỏi đang sửa và các câu đã chọn.'),
    ('Bấm 1 dòng', 'Click', 'After:\n– Thêm ngay câu hỏi đó vào Danh sách câu hỏi con.'),
    ('Bấm Chọn', 'Click', 'After:\n– Thêm các câu đã tích (bỏ câu trùng), đóng popup.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Chỉnh sửa câu hỏi')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chỉnh sửa câu hỏi', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-06 Chỉnh sửa câu hỏi')
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa).',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa câu hỏi khảo sát',
    mota='Cập nhật thông tin của một câu hỏi đang Hoạt động.',
    tacnhan='Người quản lý ngân hàng câu hỏi khảo sát',
    dieukien='Người dùng có quyền Q1; câu hỏi đang Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng câu hỏi.\n'
          '2. Hệ thống mở màn “Chỉnh sửa câu hỏi” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật câu hỏi, đáp án, câu hỏi con.\n'
          '5. Thông báo “Cập nhật thành công” và về màn danh sách.',
    phu='• Câu hỏi đang Khóa → nút Sửa bị ẩn; lưu khi câu hỏi vừa bị người khác khoá → “Dữ liệu đang bị '
        'khóa, không thể thay đổi dữ liệu”.\n'
        '• Câu hỏi nhóm đã được dùng trong mẫu phiếu mà đổi danh sách câu hỏi con → “Câu hỏi cha đã phát '
        'sinh ở phiếu thu nhập, không thể thay đổi câu hỏi con”.\n'
        '• Ứng dụng đang gán nay đã bị khoá → vẫn hiển thị đúng tên (kèm 🔒) và giữ được khi lưu.\n'
        '• Không tải được dữ liệu → “Không lấy được dữ liệu câu hỏi”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới từng ô, thông báo “Cập nhật thất bại”.',
    dacbiet='Đổi Trạng thái sang Khóa ngay trong form tương đương thao tác Khóa (FR-09).')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('06-sua.png'), shot_caption='Màn Chỉnh sửa câu hỏi')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề trang “Chỉnh sửa câu hỏi”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
           + [(r[0], r[1], r[2], r[3], r[4], 'Theo dữ liệu', r[6]) for r in FORM_ROWS[:-1]]
           + [FORM_ROWS[-1],
              ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không có nút Lưu và tiếp tục.'),
              ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách, không lưu.')])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và câu hỏi đang Hoạt động.\n'
     'After:\n– Mở màn Chỉnh sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Câu hỏi không còn Hoạt động → “Dữ liệu đang bị khóa, không thể thay đổi dữ liệu” và dừng xử lý.\n'
     'During:\n' + SAVE_DURING + '\n'
     '– Câu hỏi nhóm đã dùng trong mẫu phiếu mà danh sách câu hỏi con khác trước → “Câu hỏi cha đã phát '
     'sinh ở phiếu thu nhập, không thể thay đổi câu hỏi con”.\n'
     '– Nếu có lỗi validate → thông báo “Cập nhật thất bại”, không thực hiện bước After.\n'
     'After:\n– Cập nhật câu hỏi, đáp án, câu hỏi con; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Thông báo “Cập nhật thành công”, về màn danh sách.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xem chi tiết câu hỏi')
d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết câu hỏi khảo sát',
    mota='Xem toàn bộ thông tin của một câu hỏi ở chế độ chỉ đọc: phạm vi, Ứng dụng, loại dữ liệu, trạng '
         'thái, tiêu đề, mô tả, danh sách đáp án hoặc danh sách câu hỏi con.',
    tacnhan='Người quản lý / người xem ngân hàng câu hỏi khảo sát',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào Tiêu đề câu hỏi trên bảng.\n'
          '2. Hệ thống mở màn “Chi tiết câu hỏi”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. Người dùng bấm Quay lại để về danh sách.',
    phu='• Không tải được dữ liệu → “Không lấy được dữ liệu câu hỏi”.',
    dacbiet=None)
d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Tiêu đề câu hỏi', shot=shot('07-xem.png'),
         shot_caption='Màn Chi tiết câu hỏi loại Nhóm câu hỏi')
d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang “Chi tiết câu hỏi”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Phạm vi áp dụng / Ứng dụng / Loại dữ liệu / Trạng thái', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu',
     'Ứng dụng chỉ hiện khi phạm vi “Theo ứng dụng”.'),
    ('Tiêu đề câu hỏi / Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Danh sách đáp án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Chỉ với loại lựa chọn.'),
    ('Danh sách câu hỏi con', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Chỉ với Nhóm câu hỏi: tiêu đề, loại, mã từng câu con theo thứ tự.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
], required=False)
d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tiêu đề câu hỏi', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'After:\n– Mở màn chi tiết ở chế độ chỉ đọc.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về màn danh sách.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Xóa câu hỏi')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Xóa câu hỏi', 'action', actor=A_QL, caption='Biểu đồ Use Case — FR-08 Xóa câu hỏi')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa.', anchor='delete')
d.intro_table(
    ten='Xóa câu hỏi khảo sát',
    mota='Xoá hẳn một câu hỏi chưa được dùng trong mẫu phiếu nào, cùng danh sách đáp án của nó.',
    tacnhan='Người quản lý ngân hàng câu hỏi khảo sát',
    dieukien='Người dùng có quyền Q1; câu hỏi chưa dùng trong mẫu phiếu (kể cả làm Group) và không phải '
             'câu hỏi nhóm đang có câu hỏi con.',
    chinh='1. Người dùng bấm nút Xóa trên dòng câu hỏi.\n'
          '2. Hệ thống hiện hộp thoại xác nhận xoá.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xoá câu hỏi và đáp án, thông báo “Xóa thành công” và nạp lại danh sách.',
    phu='• Bấm Huỷ → đóng hộp thoại, không xoá.\n'
        '• Câu hỏi đã dùng trong mẫu phiếu / là câu hỏi nhóm có câu hỏi con → nút Xóa bị ẩn; nếu phát '
        'sinh trong lúc đang xác nhận → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Lỗi khác → “Xóa thất bại”.',
    dacbiet='Xoá là xoá hẳn, không khôi phục được. Muốn ngừng dùng câu hỏi đã có liên kết thì Khóa.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xoá', shot=shot('08-xoa.png'),
         shot_caption='Hộp thoại xác nhận xoá câu hỏi')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Hiển thị', '“Xác nhận hủy/xóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Hiển thị', '“Bạn có chắc chắn muốn hủy/xóa bản ghi này không?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xoá.'),
    ('Nút Huỷ', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xoá.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và câu hỏi đủ điều kiện xoá.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Câu hỏi đã dùng trong mẫu phiếu hoặc là câu hỏi nhóm có câu hỏi con → “Dữ liệu đã thay '
     'đổi, vui lòng tải lại” và dừng xử lý.\n'
     'After:\n– Xoá câu hỏi và đáp án; thông báo “Xóa thành công”, nạp lại danh sách.'),
    ('Bấm Huỷ / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Khóa / Mở khóa câu hỏi')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Khóa / Mở khóa câu hỏi', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-09 Khóa / Mở khóa câu hỏi')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa câu hỏi',
    mota='Chuyển trạng thái câu hỏi giữa Hoạt động và Khóa bằng nút ổ khoá ở cột Hành động.',
    tacnhan='Người quản lý ngân hàng câu hỏi khảo sát',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Khóa (hoặc Mở khóa) trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, thông báo “Khóa thành công” / “Mở khóa thành công”, nạp lại danh sách.',
    phu='• Bấm Huỷ → không đổi trạng thái.\n'
        '• Lỗi → “Khóa thất bại” / “Mở khóa thất bại”.',
    dacbiet='Câu hỏi bị Khóa không còn hiện trong Thư viện câu hỏi của mẫu phiếu, không chọn được làm câu '
            'hỏi con; mẫu phiếu đang chứa câu hỏi đó sẽ không lưu lại được cho tới khi bỏ câu hỏi hoặc '
            'Mở khóa. Câu hỏi đang Khóa không Sửa được.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Khóa / Mở khóa', modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('09-khoa.png'), shot_caption='Hộp thoại xác nhận khoá câu hỏi')
d.figure(shot('09b-mo-khoa.png'), 'Hộp thoại xác nhận mở khoá câu hỏi', width_in=6.2)
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Khóa / Mở khóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: Khóa (ổ khoá đóng). Đang Khóa: Mở khóa (ổ khoá mở).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Hiển thị',
     '“Bạn có chắc chắn muốn khóa (mở khóa) bản ghi này không?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Huỷ', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Đổi trạng thái sang Khóa, ghi người cập nhật.\n'
     '– Thông báo “Khóa thành công”, nạp lại danh sách.'),
    ('Bấm Mở khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật.\n'
     '– Thông báo “Mở khóa thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Xuất Excel')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xuất Excel danh sách câu hỏi', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-10 Xuất Excel')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Ngân hàng câu hỏi khảo sát.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách câu hỏi',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_sach_cau_hoi_khao_sat.xlsx gồm TẤT CẢ '
         'câu hỏi khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý ngân hàng câu hỏi khảo sát',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất Excel.\n'
          '3. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng.\n'
          '4. Người dùng tích / bỏ tích, kéo để đổi thứ tự trường, rồi bấm Xuất file.\n'
          '5. Trình duyệt tải tệp về, thông báo “Xuất Excel thành công”.',
    phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” để chọn nhanh.\n'
        '• Lỗi khi dựng tệp → thông báo “Xuất Excel thất bại”.',
    dacbiet='Nút Xuất Excel bị khoá trong lúc đang xuất để tránh bấm lặp.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('10-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '10 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Tiêu đề câu hỏi, Loại dữ liệu, Phạm vi câu hỏi, Ứng dụng, Mô tả, Người tạo, Ngày tạo, Người cập '
     'nhật, Ngày cập nhật, Trạng thái. Kéo ⠿ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/10 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_cau_hoi_khao_sat.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp với các trường đã chọn theo thứ tự đã sắp.\n'
     '– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Ngân hàng câu hỏi khảo sát; không lặp lại các quy '
           'tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Thông tin bắt buộc', [
        '– Bắt buộc: Phạm vi áp dụng, Loại dữ liệu, Tiêu đề câu hỏi (≤ 1.000 ký tự).',
        '– Phạm vi “Theo ứng dụng” bắt buộc chọn Ứng dụng; phạm vi “Tất cả” không gắn Ứng dụng.',
        '– Trạng thái không gửi thì mặc định Hoạt động (tạo mới) / giữ nguyên (sửa).',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-02', 'Đáp án và câu hỏi con theo loại dữ liệu', [
        '– Dropdown / Radio / Checkbox: mỗi dòng đáp án phải có nội dung; đáp án lưu theo thứ tự nhập.',
        '– Loại khác: không lưu đáp án (đổi loại là bỏ đáp án).',
        '– Nhóm câu hỏi: phải có ít nhất 1 câu hỏi con; câu hỏi con phải còn tồn tại và đang Hoạt động.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Chọn câu hỏi con']),
    ('BR-03', 'Chống trùng câu hỏi', [
        '– Không cho 2 câu hỏi trùng đồng thời: tiêu đề (bỏ khoảng trắng đầu cuối, không phân biệt hoa '
        'thường), loại dữ liệu, tập đáp án (không phân biệt thứ tự, hoa thường) và phạm vi (cùng “Tất cả”, '
        'hoặc cùng Ứng dụng).',
        '– Import câu hỏi từ màn Phiếu thu thập thông tin áp cùng quy tắc: trùng thì dùng lại câu đã có.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-04', 'Mã câu hỏi', [
        '– Mã cau_hoi_<số> do hệ thống gán theo bản ghi, không nhập, không sửa; dùng ở thư viện câu hỏi '
        'và logic hiển thị của mẫu phiếu.',
    ], ['Tạo mới', 'Chọn câu hỏi con']),
    ('BR-05', 'Chỉ sửa câu hỏi đang Hoạt động',
     '– Câu hỏi đang Khóa không sửa được (nút Sửa ẩn); phải Mở khóa trước.',
     ['Chỉnh sửa', 'Danh sách']),
    ('BR-06', 'Ràng buộc với mẫu phiếu', [
        '– Câu hỏi đã dùng trong mẫu phiếu (làm câu hỏi hoặc làm Group) thì không xoá được.',
        '– Câu hỏi nhóm đã dùng trong mẫu phiếu thì không đổi được danh sách câu hỏi con.',
        '– Mẫu phiếu chỉ lấy câu hỏi đang Hoạt động có phạm vi “Tất cả” hoặc đúng Ứng dụng của phiếu.',
    ], ['Chỉnh sửa', 'Xóa']),
    ('BR-07', 'Điều kiện Xóa', [
        '– Chỉ xoá được câu hỏi chưa dùng trong mẫu phiếu và không phải câu hỏi nhóm đang có câu hỏi con.',
        '– Xoá là xoá hẳn cùng đáp án; câu hỏi đã có liên kết thì dùng Khóa.',
    ], 'Xóa'),
    ('BR-08', 'Khóa / Mở khóa', [
        '– Khóa: câu hỏi không còn hiện trong thư viện câu hỏi của phiếu và popup chọn câu hỏi con.',
        '– Mở khóa luôn được phép.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-09', 'Thao tác không dùng được thì ẩn', [
        '– Sửa, Xóa, Khóa / Mở khóa chỉ hiện với người có Q1 VÀ đủ điều kiện nghiệp vụ; không hiển thị '
        'nút xám.',
    ], 'Danh sách'),
    ('BR-10', 'Xuất theo bộ lọc, chọn trường', [
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)
