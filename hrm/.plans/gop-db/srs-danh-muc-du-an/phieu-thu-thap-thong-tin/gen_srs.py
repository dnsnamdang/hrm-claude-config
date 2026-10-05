# -*- coding: utf-8 -*-
"""Sinh "SRS - Phiếu thu thập thông tin.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/phieu-thu-thap-thong-tin/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): phieu-thu-thap-thong-tin_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/form-templates/{index.vue, add.vue, _id/index.vue, _id/edit.vue}
      pages/assign/form-templates/components/{FormBuilder, FormMeta, QuestionLibrary, SectionBuilder,
      QuestionItem, AddQuestionQuickModal, FormPreview}.vue · components/FormTemplatePrintSheet.vue
      components/subsystem-menu/presale.js (menu) · components/subsystems.js (phân hệ)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/form-templates)
      Http/Controllers/Api/V1/FormTemplateController.php · Services/FormTemplateService.php
      Http/Requests/FormTemplate/FormTemplateRequest.php · Entities/FormTemplate.php
      Transformers/FormTemplatesResource/* · Services/SurveyQuestionService.php (resolveOrCreate)
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1013)
Màn liên quan: Ngân hàng câu hỏi khảo sát (.plans/gop-db/srs-danh-muc-du-an/ngan-hang-cau-hoi/)
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

OUT = os.path.join(HERE, 'SRS - Phiếu thu thập thông tin.docx')
SHOTS = os.path.join(HERE, 'phieu-thu-thap-thong-tin_shots')
MENU = 'Phân hệ CSKH trước bán => Danh mục => Phiếu thu thập thông tin'

A_QL = 'Người quản lý mẫu phiếu thu thập thông tin (Q1)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/form-templates',
           full_url='https://<host-hrm>/assign/form-templates', img_prefix='phieuttt_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện (Playwright).
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ CSKH trước bán': 'phanhe', 'Danh mục': 'danhmuc', 'Phiếu thu thập thông tin': 'phieu',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mẫu phiếu': 'taomoi', 'Import Excel': 'import', 'Tạo nhanh': 'taonhanh',
    'Xem trước': 'xemtruoc', 'Sửa mẫu': 'sua', 'Mã mẫu phiếu': 'ma', 'Sao chép mẫu': 'saochep',
    'Hành động khác': 'khac', 'In mẫu phiếu': 'in', 'Xoá mẫu': 'xoa', 'Khoá': 'khoa',
    'Mở khoá': 'mokhoa', 'Xuất Excel': 'xuat',
}.items()})

d.title_block('Phiếu thu thập thông tin')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu thu thập thông tin (danh mục mẫu phiếu '
    'thu thập thông tin dự án) thuộc phân hệ CSKH trước bán, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Mô tả đầy đủ luồng dựng mẫu phiếu: chọn Ứng dụng → thêm Section / Group → kéo câu hỏi từ Thư '
    'viện câu hỏi (Ngân hàng câu hỏi khảo sát) → đánh dấu bắt buộc, logic hiển thị → Lưu nháp hoặc '
    'Lưu và duyệt.',
    'Làm rõ ràng buộc giữa mẫu phiếu với Ngân hàng câu hỏi khảo sát: chỉ dùng câu hỏi đang Hoạt động, '
    'phạm vi “Tất cả” hoặc đúng Ứng dụng của phiếu; câu hỏi đã dùng trong phiếu thì không xoá được ở '
    'ngân hàng.',
    'Làm rõ quy tắc “mỗi Ứng dụng chỉ có 1 mẫu phiếu Hoạt động” và vòng đời Nháp → Hoạt động → Khoá.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Mẫu phiếu (Form)', 'Bộ câu hỏi dùng để thu thập thông tin dự án của một Ứng dụng. Mỗi mẫu phiếu '
     'gắn đúng 1 Ứng dụng.'),
    ('Mã mẫu phiếu', 'Mã do hệ thống tự sinh khi lưu lần đầu, dạng PTT-YYYY-NNNNN (vd PTT-2026-00001). '
     'Người dùng không nhập, không sửa được.'),
    ('Ứng dụng', 'Danh mục Ứng dụng (phân hệ CSKH trước bán). Là căn cứ để lọc câu hỏi trong thư viện và '
     'để chọn mẫu phiếu khi thu thập thông tin dự án.'),
    ('Section', 'Phần lớn của mẫu phiếu (vd “Thông tin chung”). Mỗi section có tiêu đề, mô tả và chứa '
     'hoặc các câu hỏi, hoặc các Group — không chứa cả hai.'),
    ('Group', 'Nhóm câu hỏi bên trong một section. Kéo một câu hỏi loại “Nhóm câu hỏi” từ thư viện vào '
     'section thì hệ thống tự tạo Group chứa các câu hỏi con của nó.'),
    ('Thư viện câu hỏi', 'Khung bên trái màn Tạo / Sửa: danh sách câu hỏi đang Hoạt động của Ngân hàng '
     'câu hỏi khảo sát có phạm vi “Tất cả” hoặc thuộc đúng Ứng dụng đã chọn.'),
    ('Mã câu hỏi', 'Mã của câu hỏi trong ngân hàng, dạng cau_hoi_<số>. Dùng để khai logic hiển thị.'),
    ('Trạng thái Nháp', 'Mẫu phiếu đang soạn, chưa dùng để thu thập thông tin. Được sửa, xoá.'),
    ('Trạng thái Hoạt động', 'Mẫu phiếu đang dùng cho Ứng dụng. Mỗi Ứng dụng chỉ có tối đa 1 mẫu phiếu '
     'Hoạt động.'),
    ('Trạng thái Khoá', 'Mẫu phiếu ngừng sử dụng: không sửa được cho tới khi Mở khoá.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động chứa các thao tác phụ của dòng khi không đủ chỗ '
     'hiển thị: Sao chép mẫu, In mẫu phiếu, Khoá / Mở khoá.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục mẫu phiếu thu thập thông tin',
     'Xem danh sách, tìm kiếm, xem chi tiết; tạo mẫu phiếu (kể cả Import Excel câu hỏi, Tạo nhanh câu '
     'hỏi), sửa, sao chép, in, xoá, khoá / mở khoá và xuất Excel.'),
], widths=[0.8, 2.2, 3.0])
d.p('Màn hình chỉ có 1 quyền, không có quyền “Xem” riêng. Màn hình không phân quyền theo cấp dữ liệu '
    '(công ty / phòng ban / bộ phận): người có Q1 xem được toàn bộ mẫu phiếu của hệ thống.')
d.p('Riêng thao tác “Tạo nhanh” câu hỏi (FR-06) ghi vào Ngân hàng câu hỏi khảo sát nên người dùng cần '
    'có thêm quyền “Quản lý danh mục câu hỏi khảo sát” của màn đó.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách mẫu phiếu', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '❌'),
    ('FR-04 Tạo mới mẫu phiếu', '✅', '❌'),
    ('FR-05 Import Excel câu hỏi vào mẫu phiếu', '✅', '❌'),
    ('FR-06 Tạo nhanh câu hỏi', '✅ (kèm quyền quản lý ngân hàng câu hỏi)', '❌'),
    ('FR-07 Chỉnh sửa mẫu phiếu', '✅', '❌'),
    ('FR-08 Xem chi tiết mẫu phiếu', '✅', '❌'),
    ('FR-09 Sao chép mẫu phiếu', '✅', '❌'),
    ('FR-10 In mẫu phiếu', '✅', '❌'),
    ('FR-11 Xoá mẫu phiếu', '✅', '❌'),
    ('FR-12 Khoá / Mở khoá mẫu phiếu', '✅', '❌'),
    ('FR-13 Xuất Excel', '✅', '❌'),
], widths=[3.4, 1.4, 1.2])

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_QL, [0, 1, 2, 3, 4, 5, 6, 7])],
    [('FR-01', 'Xem danh sách mẫu phiếu', 'view'),
     ('FR-04', 'Tạo mới mẫu phiếu', 'crud'),
     ('FR-07', 'Chỉnh sửa mẫu phiếu', 'crud'),
     ('FR-09', 'Sao chép mẫu phiếu', 'crud'),
     ('FR-10', 'In mẫu phiếu', 'io'),
     ('FR-11', 'Xoá mẫu phiếu', 'action'),
     ('FR-12', 'Khoá / Mở khoá mẫu phiếu', 'action'),
     ('FR-13', 'Xuất Excel danh sách mẫu phiếu', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-08', 'Xem chi tiết mẫu phiếu', 'view', 'extend', [0], None),
     ('FR-05', 'Import Excel câu hỏi vào mẫu phiếu', 'io', 'extend', [1, 2], None),
     ('FR-06', 'Tạo nhanh câu hỏi', 'crud', 'extend', [1, 2], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu thu thập thông tin')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách mẫu phiếu')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Phiếu thu thập thông tin tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách mẫu phiếu',
    mota='Hiển thị toàn bộ mẫu phiếu thu thập thông tin kèm Ứng dụng, số câu hỏi, người tạo / cập '
         'nhật, trạng thái và các thao tác trên từng dòng.',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1.',
    chinh='1. Người dùng vào menu Phân hệ CSKH trước bán → Danh mục → Phiếu thu thập thông tin.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, mẫu phiếu cập nhật gần nhất lên đầu.\n'
          '3. Bảng “Danh sách mẫu phiếu” hiển thị đủ các cột (mặc định hiện hết cột), dòng '
          '“Hiển thị a–b / N” và thanh phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Mã mẫu phiếu → mở màn Xem chi tiết (FR-08); chuột phải để mở ở tab mới.\n'
        '• Bấm tiêu đề cột Mã, Tên, Số câu hỏi, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm '
        'lại để đảo chiều.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách mẫu phiếu lúc mới truy cập')
d.figure(shot('01b-hanh-dong.png'), 'Cột Trạng thái, cột Hành động và menu “…” của một dòng',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách mẫu phiếu”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Nút Tạo mẫu phiếu', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn Tạo mới (FR-04).'),
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
     'Mở cửa sổ Chọn trường xuất file (FR-13). Bị khoá trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Mã mẫu phiếu', 'Table/Grid', 'Read-only', 'PTT-YYYY-NNNNN', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được. Là liên kết mở màn Xem chi tiết.'),
    ('Cột Tên mẫu phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Sắp xếp được; tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Ứng dụng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tên Ứng dụng của mẫu phiếu.'),
    ('Cột Số câu hỏi', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Căn phải, sắp xếp được. Đếm mọi câu hỏi của phiếu, kể cả câu hỏi con trong Group.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Nháp / Hoạt động / Khoá', 'Theo dữ liệu',
     'Nháp màu xám, Hoạt động màu xanh, Khoá màu đỏ.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự: Sửa mẫu, Xoá mẫu, Sao chép mẫu, In mẫu phiếu, Khoá / Mở khoá. Hiện '
     'tối đa 3 nút; nhiều hơn thì 2 nút đầu hiện sẵn, phần còn lại gom vào nút “…”. Thao tác không '
     'dùng được thì ẨN hẳn.'),
    ('Nút Sửa mẫu (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Hiện khi mẫu phiếu chưa Khoá (Nháp hoặc Hoạt động) (FR-07).'),
    ('Nút Xoá mẫu (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện khi mẫu phiếu đang Nháp (FR-11).'),
    ('Mục Sao chép mẫu', 'Button', 'Enable', '–', 'Hiển thị', 'Mọi trạng thái (FR-09).'),
    ('Mục In mẫu phiếu', 'Button', 'Enable', '–', 'Hiển thị', 'Mọi trạng thái (FR-10).'),
    ('Mục Khoá / Mở khoá', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Ẩn khi mẫu phiếu đang Nháp. Hoạt động: mục Khoá; Khoá: mục Mở khoá (FR-12).'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số bản ghi khớp bộ lọc.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5 / 10 / 20 / 50', '10', 'Đổi thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Về đầu / lùi / số trang / tiến / về cuối.'),
    ('Thanh cuộn ngang', 'Table/Grid', 'Enable', '–', 'Hiển thị khi bảng tràn',
     'Có ở cả phía trên và phía dưới bảng.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có).\n'
     '– Nạp cấu hình cột đã lưu của người dùng và danh sách Ứng dụng cho bộ lọc.\n'
     'After:\n– Hiển thị trang 1, 10 dòng, mẫu phiếu cập nhật gần nhất lên đầu.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Mã mẫu phiếu', 'Click', 'After:\n– Mở màn Xem chi tiết mẫu phiếu (FR-08).'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Sao chép mẫu, In mẫu phiếu, Khoá / Mở khoá).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Phiếu thu '
           'thập thông tin tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc mẫu phiếu',
    mota='Tìm nhanh theo mã, tên mẫu phiếu hoặc tên người tạo; lọc nâng cao theo Ứng dụng, Trạng thái, '
         'Người tạo, Người cập nhật, khoảng Ngày cập nhật.',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách mẫu phiếu.',
    chinh='1. Người dùng nhập từ khoá vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
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
     'Placeholder “Tìm theo mã, tên mẫu phiếu, người tạo”. Tìm gần đúng theo Mã, Tên mẫu phiếu hoặc '
     'tên Người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Ứng dụng', 'Dropdown', 'Enable', 'Danh sách Ứng dụng đang Hoạt động', 'Không', 'Trống',
     'Lọc đúng theo Ứng dụng của mẫu phiếu.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Nháp / Hoạt động / Khoá', 'Không', 'Trống', '–'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc đúng theo người tạo.'),
    ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc đúng theo người cập nhật cuối.'),
    ('Ngày cập nhật', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Một ô gồm 2 ngày Từ → Đến, tính cả 2 đầu mút.'),
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
    dieukien='Đang ở màn danh sách mẫu phiếu.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột STT, Mã mẫu phiếu và Hành động luôn hiện, không bỏ tích được (hiển thị xám + ổ khoá).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('03b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('03c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khoá hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '5 trường', 'Không', 'Theo cấu hình đã lưu',
     'Ứng dụng, Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật. Mỗi dòng: số thứ tự, biểu tượng '
     'kéo ⠿, ô tích, tên trường.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '11 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột STT, Mã mẫu phiếu, Hành động bị khoá (luôn hiện).'),
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
    '– Tên form trống → “Bắt buộc phải nhập”; quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”\n'
    '– Chưa chọn Ứng dụng → “Bắt buộc phải chọn ứng dụng”; Ứng dụng không còn → “Ứng dụng không tồn '
    'tại”.\n'
    '– Chưa có Section nào → báo “Bắt buộc phải nhập” ở khung Section.\n'
    '– Tiêu đề Section trống → “Bắt buộc phải nhập” dưới ô tiêu đề; quá 255 ký tự → “Vui lòng nhập '
    'tối đa 255 ký tự.”; mô tả Section quá 500 ký tự → “Vui lòng nhập tối đa 500 ký tự.”\n'
    '– Section chưa có câu hỏi nào (cả trực tiếp lẫn trong Group) → “Bắt buộc phải nhập” ở section đó.\n'
    '– Có câu hỏi đã bị xoá khỏi ngân hàng → “Câu hỏi mã \"cau_hoi_<số>\" không còn tồn tại, vui lòng '
    'chọn câu hỏi khác”; đã bị khoá → “Câu hỏi mã \"cau_hoi_<số>\" đang bị khóa, vui lòng chọn câu hỏi '
    'khác”.\n'
    '– Lưu ở trạng thái Hoạt động mà Ứng dụng đã có mẫu phiếu Hoạt động khác → “Ứng dụng này đã có '
    'mẫu phiếu đang hoạt động” (báo dưới ô Ứng dụng).\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')

d.h3('2.4 Tạo mới mẫu phiếu')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới mẫu phiếu', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới mẫu phiếu')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Tạo mới mẫu phiếu thu thập thông tin',
    mota='Dựng một mẫu phiếu mới cho 1 Ứng dụng: đặt tên, chọn Ứng dụng, thêm các Section / Group rồi '
         'kéo câu hỏi từ Thư viện câu hỏi vào; lưu ở trạng thái Nháp hoặc Lưu và duyệt để đưa vào sử '
         'dụng (Hoạt động).',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mẫu phiếu trên màn danh sách.\n'
          '2. Hệ thống mở màn “Tạo Form thu thập thông tin” gồm: khối thông tin chung (Tên form, Ứng '
          'dụng, nút Import Excel), nút Thêm Section, khung Thư viện câu hỏi (trái) và khung Section '
          '(phải). Thư viện để trống cho tới khi chọn Ứng dụng.\n'
          '3. Người dùng nhập Tên form và chọn Ứng dụng → thư viện nạp các câu hỏi đang Hoạt động có '
          'phạm vi “Tất cả” hoặc thuộc đúng Ứng dụng đã chọn.\n'
          '4. Người dùng bấm Thêm Section (tự đặt tên “Section mới”), sửa tiêu đề, mô tả.\n'
          '5. Người dùng kéo câu hỏi từ thư viện thả vào section (hoặc vào Group). Câu hỏi đã dùng trong '
          'phiếu tự ẩn khỏi thư viện để không bị thêm trùng.\n'
          '6. Với từng câu hỏi: sửa nội dung hiển thị, bấm dấu * để đánh dấu Bắt buộc, Nhân bản, Xoá, '
          'thêm câu hỏi con, khai Logic hiển thị (Nếu câu hỏi mã … Thoả điều kiện … Giá trị …).\n'
          '7. (Tuỳ chọn) Bấm Xem trước để xem phiếu như người trả lời sẽ thấy; bấm Chỉnh sửa để quay lại.\n'
          '8. Người dùng bấm Lưu (lưu Nháp) hoặc Lưu và duyệt → xác nhận “Bạn đồng ý lưu và duyệt?”.\n'
          '9. Hệ thống kiểm tra dữ liệu, sinh Mã mẫu phiếu PTT-YYYY-NNNNN, ghi mẫu phiếu cùng toàn bộ '
          'Section, Group, câu hỏi, đáp án.\n'
          '10. Thông báo “Lưu nháp thành công” / “Lưu và duyệt thành công” và quay về màn danh sách.',
    phu='• Kéo câu hỏi loại “Nhóm câu hỏi” vào section trống → hệ thống tự tạo Group mang tên câu hỏi '
        'đó, chứa các câu hỏi con của nó.\n'
        '• Section đã có câu hỏi thì không thêm Group được (nút Group bị mờ, thả câu hỏi nhóm vào báo '
        '“Không thể thêm câu hỏi cha con vào section đã có câu hỏi. Vui lòng xóa câu hỏi trước.”); '
        'section đã có Group mà thả câu hỏi thường vào khung trống → hệ thống tự tạo Group mới chứa '
        'câu hỏi đó.\n'
        '• Bấm Group khi section đã có câu hỏi → “Không thể thêm group vào section đã có câu hỏi. Vui '
        'lòng xóa câu hỏi trước.”\n'
        '• Bấm Xoá Section / Group → hộp thoại “Bạn có chắc muốn xóa Section này?” / “Bạn có chắc muốn '
        'xóa Group này?” (Đồng ý / Không).\n'
        '• Bấm Nhân bản ở Section → tạo bản sao section ngay bên dưới.\n'
        '• Đổi sang Ứng dụng khác khi phiếu đã có câu hỏi → các câu hỏi / nhóm phạm vi “Theo ứng dụng” '
        'của ứng dụng cũ bị bỏ khỏi phiếu, thông báo “Đã bỏ <n> câu hỏi thuộc phạm vi \"Theo ứng '
        'dụng\" của ứng dụng cũ.”; câu hỏi phạm vi “Tất cả” được giữ.\n'
        '• Import Excel câu hỏi (FR-05) và Tạo nhanh câu hỏi (FR-06) mở từ chính màn này.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Bấm Quay lại → về màn danh sách, không lưu.',
    dacbiet='Mã mẫu phiếu do hệ thống tự sinh, không nhập tay. Mỗi Ứng dụng chỉ có tối đa 1 mẫu phiếu '
            'Hoạt động; lưu Nháp thì không bị giới hạn.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mẫu phiếu', shot=shot('04-tao-moi.png'),
         shot_caption='Màn Tạo mới mẫu phiếu — thư viện câu hỏi bên trái, section bên phải')
d.figure(shot('04c-tao-moi-loi.png'), 'Bấm Lưu khi chưa nhập Tên form, Ứng dụng và chưa có Section',
         width_in=6.2)
d.figure(shot('04b-xem-truoc.png'), 'Chế độ Xem trước mẫu phiếu', width_in=6.2)
d.figure(shot('04d-luu-duyet.png'), 'Hộp thoại xác nhận Lưu và duyệt', width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
FORM_ROWS = [
    ('Nút Xem trước / Chỉnh sửa', 'Button', 'Enable', '–', '–', 'Xem trước',
     'Chuyển giữa chế độ dựng phiếu và chế độ xem trước.'),
    ('Tên form', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Placeholder “Tên form khảo sát...”.'),
    ('Ứng dụng', 'Dropdown', 'Enable / Disable', 'Ứng dụng đang Hoạt động', 'Có', 'Trống',
     'Chọn 1 Ứng dụng; icon ⓘ mô tả khái niệm. Đổi Ứng dụng thì thư viện nạp lại.'),
    ('Nút Import Excel', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ Import (FR-05). Chưa chọn Ứng dụng → “Vui lòng chọn Ứng dụng trước khi import”.'),
    ('Nút Thêm Section', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Thêm 1 section “Section mới” vào cuối phiếu.'),
    ('Khung Thư viện câu hỏi', 'Table/Grid', 'Enable', 'Câu hỏi Hoạt động, phạm vi Tất cả / đúng Ứng dụng',
     '–', 'Trống khi chưa chọn Ứng dụng',
     'Mỗi thẻ: nội dung câu hỏi, loại, Mã (cau_hoi_<số>), kiểu trả lời. Kéo thẻ thả sang section.'),
    ('Ô Tìm trong thư viện', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Lọc thẻ theo nội dung câu hỏi.'),
    ('Nhóm nút lọc loại', 'Button', 'Enable', 'Tất cả / Văn bản / Lựa chọn / Khác', '–', 'Tất cả',
     'Lọc thẻ theo nhóm loại câu hỏi.'),
    ('Nút Tạo nhanh', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Tạo nhanh câu hỏi (FR-06).'),
    ('Tiêu đề Section', 'Textbox', 'Enable', '1–255 ký tự', 'Có', '“Section mới”',
     'Có biểu tượng kéo để đổi thứ tự section.'),
    ('Mô tả Section', 'Textarea', 'Enable', '0–500 ký tự', 'Không', 'Trống', '–'),
    ('Nút Group / Nhân bản / Xoá (Section)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Group bị mờ khi section đã có câu hỏi. Xoá có hộp thoại xác nhận.'),
    ('Tên Group / Mô tả Group', 'Textbox', 'Enable', '–', 'Không', '“Group mới”', 'Có biểu tượng kéo, nút Xoá Group.'),
    ('Vùng thả câu hỏi', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Kéo câu hỏi từ thư viện vào đây”.'),
    ('Dòng câu hỏi', 'Textbox', 'Enable', '–', 'Không', 'Theo thư viện',
     'Số thứ tự, nội dung câu hỏi (sửa được), mã, loại, nhãn “Bắt buộc”; nút * (Đánh dấu / Bỏ bắt '
     'buộc), Nhân bản, Xoá; kéo để đổi thứ tự.'),
    ('Câu hỏi con', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Nút Thêm câu hỏi con; mỗi câu con có nội dung, ô tích Bắt buộc, nút Xoá.'),
    ('Logic hiển thị (nếu có)', 'Dropdown', 'Enable', '= ≠ > < ≥ ≤', 'Không', 'Tắt',
     'Tích “Kích hoạt logic hiển thị” rồi chọn Nếu câu hỏi mã, Thoả điều kiện, Giá trị so sánh.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô / section bị lỗi.'),
]
d.ui_table(FORM_ROWS + [
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu ở trạng thái Nháp.'),
    ('Nút Lưu và duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận rồi lưu ở trạng thái Hoạt động.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách, không lưu.'),
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Tạo mới', 'System',
     'Before:\n– Kiểm tra quyền Q1; không có quyền (kể cả vào bằng đường dẫn trực tiếp) → chuyển tới '
     'trang không tìm thấy.\n'
     'After:\n– Hiện form trống, thư viện câu hỏi trống.'),
    ('Chọn / đổi Ứng dụng', 'Change',
     'After:\n– Nạp lại thư viện: câu hỏi Hoạt động, phạm vi “Tất cả” hoặc đúng Ứng dụng.\n'
     '– Nếu là đổi từ Ứng dụng khác: bỏ câu hỏi / nhóm phạm vi “Theo ứng dụng” khỏi phiếu, thông báo '
     '“Đã bỏ <n> câu hỏi thuộc phạm vi \"Theo ứng dụng\" của ứng dụng cũ.”'),
    ('Kéo thả câu hỏi từ thư viện vào section / group', 'Drag',
     'Before:\n– Section đã có Group → không nhận câu hỏi trực tiếp (tự tạo Group mới).\n'
     '– Section đã có câu hỏi → không nhận câu hỏi nhóm: “Không thể thêm câu hỏi cha con vào section '
     'đã có câu hỏi. Vui lòng xóa câu hỏi trước.”\n'
     'After:\n– Thêm câu hỏi (hoặc Group từ câu hỏi nhóm) vào vị trí thả; ẩn câu hỏi đó khỏi thư viện.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Sinh Mã mẫu phiếu, ghi mẫu phiếu trạng thái Nháp cùng Section, Group, câu hỏi, đáp án; '
     'ghi người tạo, thời điểm tạo.\n'
     '– Câu hỏi nạp từ Import Excel chưa có trong ngân hàng được thêm vào Ngân hàng câu hỏi khảo sát '
     '(trùng thì dùng lại câu cũ).\n'
     '– Thông báo “Lưu nháp thành công”, về màn danh sách.'),
    ('Bấm Lưu và duyệt', 'Click',
     'Before:\n– Hiện hộp thoại “Xác nhận lưu và duyệt” – “Bạn đồng ý lưu và duyệt?”; bấm Hủy thì dừng.\n'
     '– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Kiểm tra như nút Lưu, thêm điều kiện Ứng dụng chưa có mẫu phiếu Hoạt động khác.\n'
     'After:\n– Ghi mẫu phiếu trạng thái Hoạt động; thông báo “Lưu và duyệt thành công”, về màn danh '
     'sách.'),
    ('Bấm Xem trước / Chỉnh sửa', 'Click',
     'After:\n– Chuyển sang chế độ xem trước (hiển thị phiếu như người trả lời) / quay lại chế độ dựng.'),
    ('Bấm Xoá Section / Xoá Group', 'Click',
     'Before:\n– Hiện hộp thoại xác nhận.\n'
     'After:\n– Đồng ý: bỏ section / group khỏi phiếu (chưa ghi dữ liệu cho tới khi Lưu).'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Import Excel câu hỏi vào mẫu phiếu')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Import Excel câu hỏi vào mẫu phiếu', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Import Excel câu hỏi vào mẫu phiếu')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel câu hỏi vào mẫu phiếu',
    mota='Nạp hàng loạt câu hỏi vào mẫu phiếu đang dựng từ tệp Excel theo file mẫu. Câu hỏi được gom '
         'theo cột Tên Section; bước Import chỉ nạp vào màn hình, dữ liệu được ghi khi bấm Lưu mẫu phiếu.',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin',
    dieukien='Người dùng có quyền Q1; đang ở màn Tạo mới / Sửa mẫu phiếu và đã chọn Ứng dụng.',
    chinh='1. Người dùng bấm Import Excel ở khối thông tin chung.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_mau_khao_sat.xlsx (6 cột: Tên Section, '
          'Nội dung câu hỏi, Loại câu hỏi, Bắt buộc, Danh sách đáp án, Phạm vi câu hỏi).\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu, bấm “Load lên bảng”.\n'
          '4. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do.\n'
          '5. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” để '
          'loại các dòng lỗi khỏi bảng.\n'
          '6. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → các câu hỏi '
          'được thêm vào cuối phiếu đang dựng, mỗi Tên Section thành 1 section mới; cửa sổ đóng, thông báo '
          '“Đã nạp <n> câu hỏi (<m> section) vào biểu mẫu. Bấm Lưu để hoàn tất.” Chưa ghi dữ liệu cho tới '
          'khi bấm Lưu mẫu phiếu.',
    phu='• Chưa chọn Ứng dụng → “Vui lòng chọn Ứng dụng trước khi import”, không mở cửa sổ.\n'
        '• Không dòng nào hợp lệ → “Không có dòng nào hợp lệ. Hãy sửa các dòng lỗi và validate lại.”\n'
        '• Còn dòng lỗi → “Validate xong: x hợp lệ, y lỗi. Chỉ câu hỏi hợp lệ được nạp.”; tất cả hợp lệ '
        '→ “Tất cả x câu hỏi hợp lệ. Bấm \"Import\" để nạp vào biểu mẫu.”\n'
        '• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; không '
        'nạp được câu hỏi nào.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Bấm Làm mới → xoá dữ liệu đã nạp để chọn tệp khác. Bấm Đóng → không nạp gì.',
    dacbiet='Khi Lưu mẫu phiếu, câu hỏi import chưa có trong Ngân hàng câu hỏi khảo sát được thêm vào '
            'ngân hàng; câu hỏi trùng (cùng nội dung, loại, đáp án, phạm vi) thì dùng lại câu đã có.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mẫu phiếu => Import Excel', modal='Import form thu thập thông tin',
         shot=shot('05-import.png'), shot_caption='Cửa sổ Import form thu thập thông tin')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Import form thu thập thông tin”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     'Dòng phụ: “Import từ Excel • Validate xong sẽ nạp các câu hỏi hợp lệ vào biểu mẫu”.'),
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải Mau_import_mau_khao_sat.xlsx.'),
    ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa chọn tệp',
     'Đọc tệp ra bảng xem trước.'),
    ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Kiểm tra dữ liệu từng dòng.'),
    ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Disable',
     'Chỉ bấm được khi đã Validate và không còn dòng lỗi. Nạp các câu hỏi vào phiếu đang dựng.'),
    ('Cột Tên Section', 'Textbox', 'Enable', '–', 'Có', 'Theo tệp', 'Câu hỏi cùng tên được gom 1 section.'),
    ('Cột Nội dung câu hỏi', 'Textarea', 'Enable', '–', 'Có', 'Theo tệp', '–'),
    ('Cột Loại câu hỏi', 'Textbox', 'Enable',
     'Text ngắn / Text dài / Số / Dropdown / Radio 1 lựa chọn / Checkbox nhiều lựa chọn / Ngày / File / '
     'Có / Không', 'Có', 'Theo tệp', 'Không nhận loại “Nhóm câu hỏi”.'),
    ('Cột Bắt buộc', 'Textbox', 'Enable', 'Có / Không', 'Có', 'Theo tệp', '–'),
    ('Cột Danh sách đáp án', 'Textarea', 'Enable', 'Phân tách bằng dấu phẩy', 'Có khi loại là Dropdown / '
     'Radio / Checkbox', 'Theo tệp', 'Tối thiểu 2 đáp án.'),
    ('Cột Phạm vi câu hỏi', 'Textbox', 'Enable', 'Tất cả / Theo ứng dụng', 'Có', 'Theo tệp',
     '“Theo ứng dụng” gắn với Ứng dụng đang chọn của phiếu.'),
    ('Dòng Tổng / hợp lệ / lỗi', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Thống kê sau Validate.'),
    ('Nút Bỏ dòng lỗi', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu', 'Loại các dòng lỗi khỏi bảng xem trước.'),
    ('Nút Xoá trạng thái validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Bỏ kết quả Validate để sửa lại dữ liệu.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không nạp.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá dữ liệu đã nạp.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Validate', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During (từng dòng):\n'
     '– Thiếu Tên Section → “Thiếu Tên Section”; thiếu nội dung → “Thiếu Nội dung câu hỏi”.\n'
     '– Loại sai → “Loại câu hỏi không hợp lệ”; Bắt buộc sai → “Bắt buộc chỉ nhận: Có / Không”; Phạm vi '
     'sai → “Phạm vi chỉ nhận: Tất cả / Theo ứng dụng”.\n'
     '– Loại Dropdown / Radio / Checkbox có dưới 2 đáp án → “Loại câu hỏi này cần ít nhất 2 đáp án '
     '(phân tách bằng dấu phẩy)”.\n'
     '– Phạm vi “Theo ứng dụng” mà phiếu chưa chọn Ứng dụng → “Cần chọn Ứng dụng cho phạm vi \"Theo '
     'ứng dụng\"”.\n'
     '– Hai dòng giống hệt nhau trong tệp → “Trùng với dòng <n> trong danh sách (2 dòng y hệt nhau)”.\n'
     '– Câu hỏi đã có sẵn trong phiếu → “Câu hỏi này đã có trong biểu mẫu (trùng nội dung, loại, đáp án '
     'và phạm vi)”.\n'
     'After:\n– Đánh dấu từng dòng hợp lệ / lỗi và hiện dòng thống kê.'),
    ('Bấm Bỏ dòng lỗi', 'Click',
     'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.”\n'
     'After:\n– Loại các dòng lỗi khỏi bảng; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
     '– Nút Import mở nếu còn ≥ 1 dòng.'),
    ('Bấm Import', 'Click',
     'Before:\n– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.\n'
     'During:\n– Không gửi lên máy chủ: các câu hỏi được gom theo Tên Section ngay trên màn hình.\n'
     'After:\n– Thêm section mới theo từng Tên Section vào cuối phiếu (không đụng section đang có), đóng '
     'cửa sổ, thông báo “Đã nạp <n> câu hỏi (<m> section) vào biểu mẫu. Bấm Lưu để hoàn tất.”\n'
     '– Chưa ghi dữ liệu cho tới khi bấm Lưu mẫu phiếu; rời màn mà chưa Lưu thì câu hỏi vừa nạp bị bỏ.'),
    ('Bấm Tải file mẫu', 'Click',
     'After:\n– Tải tệp Mau_import_mau_khao_sat.xlsx; lỗi → “Lỗi khi tải file mẫu”.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Tạo nhanh câu hỏi')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Tạo nhanh câu hỏi', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-06 Tạo nhanh câu hỏi')
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Tạo nhanh câu hỏi vào Ngân hàng câu hỏi khảo sát',
    mota='Khi thư viện chưa có câu hỏi cần dùng, người dùng tạo ngay câu hỏi mới vào Ngân hàng câu hỏi '
         'khảo sát mà không phải rời màn dựng phiếu. Câu hỏi mới xuất hiện trong thư viện để kéo vào phiếu.',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin (có thêm quyền Quản lý danh mục câu hỏi khảo sát)',
    dieukien='Đang ở màn Tạo mới / Sửa mẫu phiếu.',
    chinh='1. Người dùng bấm “Tạo nhanh” ở khung Thư viện câu hỏi.\n'
          '2. Hệ thống mở cửa sổ “Tạo nhanh câu hỏi”, Phạm vi áp dụng mặc định “Theo ứng dụng” gắn Ứng '
          'dụng của phiếu, Trạng thái mặc định Hoạt động.\n'
          '3. Người dùng chọn Loại dữ liệu, nhập Tiêu đề câu hỏi, Mô tả; loại Dropdown / Radio / Checkbox '
          'thì nhập Danh sách đáp án (tạo sẵn 2 dòng).\n'
          '4. Bấm Lưu (lưu rồi đóng) hoặc Lưu và tiếp tục (lưu rồi xoá trắng để nhập câu tiếp).\n'
          '5. Hệ thống ghi câu hỏi vào ngân hàng, thông báo “Đã lưu câu hỏi thành công!” và nạp lại thư viện.',
    phu='• Dữ liệu không hợp lệ → báo lỗi dưới ô, thông báo “Vui lòng kiểm tra lại thông tin”.\n'
        '• Lỗi khác → “Lưu thất bại” (hoặc nội dung lỗi hệ thống trả về).\n'
        '• Bấm Đóng / dấu × → đóng, không lưu.',
    dacbiet='Không tạo được câu hỏi loại “Nhóm câu hỏi” tại đây (chỉ tạo ở màn Ngân hàng câu hỏi).')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mẫu phiếu => Tạo nhanh', modal='Tạo nhanh câu hỏi',
         shot=shot('06-tao-nhanh.png'), shot_caption='Cửa sổ Tạo nhanh câu hỏi')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Phạm vi áp dụng', 'Dropdown', 'Enable', 'Tất cả / Theo ứng dụng', 'Có', 'Theo ứng dụng',
     '“Theo ứng dụng” gắn Ứng dụng đang chọn của phiếu.'),
    ('Loại dữ liệu', 'Dropdown', 'Enable', '9 loại (không có Nhóm câu hỏi)', 'Có', 'Trống', '–'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động', '–'),
    ('Tiêu đề câu hỏi', 'Textarea', 'Enable', '1–1.000 ký tự', 'Có', 'Trống', '–'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Gợi ý trả lời.'),
    ('Danh sách đáp án', 'Table/Grid', 'Enable / Ẩn', '–', 'Có với Dropdown / Radio / Checkbox',
     '2 dòng trống', 'Nút “Thêm đáp án”, mỗi dòng có nút xoá.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu rồi xoá trắng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu / Lưu và tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý danh mục câu hỏi khảo sát.\n' + NO_PERM + '\n'
     'During:\n– Tiêu đề trống → “Bắt buộc phải nhập”; quá 1.000 ký tự → “Vui lòng nhập tối đa 1000 '
     'ký tự.”\n– Chưa chọn Loại dữ liệu → “Bắt buộc phải nhập”.\n'
     '– Phạm vi “Theo ứng dụng” mà chưa có Ứng dụng → “Bắt buộc phải chọn ứng dụng”.\n'
     '– Dòng đáp án trống → “Bắt buộc phải nhập”.\n'
     '– Trùng câu hỏi đã có (cùng nội dung, loại, danh sách đáp án, phạm vi) → “Câu hỏi đã tồn tại '
     'trong phạm vi này (trùng nội dung, loại dữ liệu và danh sách đáp án)”.\n'
     'After:\n– Ghi câu hỏi vào Ngân hàng câu hỏi khảo sát; thông báo “Đã lưu câu hỏi thành công!”; nạp '
     'lại thư viện.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Chỉnh sửa mẫu phiếu')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Chỉnh sửa mẫu phiếu', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Chỉnh sửa mẫu phiếu')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa).',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa mẫu phiếu',
    mota='Cập nhật tên, cấu trúc Section / Group / câu hỏi của một mẫu phiếu chưa Khoá.',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin',
    dieukien='Người dùng có quyền Q1; mẫu phiếu đang Nháp hoặc Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa mẫu trên dòng.\n'
          '2. Hệ thống mở màn “Chỉnh sửa Form” với dữ liệu hiện tại và nạp thư viện theo Ứng dụng của phiếu.\n'
          '3. Người dùng chỉnh sửa như ở màn Tạo mới (FR-04).\n'
          '4. Mẫu phiếu Nháp: bấm Lưu (giữ Nháp) hoặc Lưu và duyệt (chuyển Hoạt động). Mẫu phiếu Hoạt động: '
          'chỉ có Lưu và duyệt (giữ Hoạt động).\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi lại toàn bộ cấu trúc phiếu.\n'
          '6. Thông báo “Lưu nháp thành công” / “Lưu và duyệt thành công”, về màn danh sách.',
    phu='• Mẫu phiếu đang Khoá → nút Sửa mẫu bị ẩn; lưu khi phiếu vừa bị người khác khoá → “Thao tác '
        'không thành công. Dữ liệu đã được thay đổi hoặc chuyển trạng thái bởi người dùng khác. Vui lòng '
        'tải lại trang để cập nhật thông tin mới nhất”.\n'
        '• Mẫu phiếu Hoạt động → ô Ứng dụng bị khoá, không đổi được.\n'
        '• Ứng dụng đang gán nay đã bị khoá → vẫn hiển thị đúng tên (kèm 🔒).\n'
        '• Không tải được dữ liệu → “Không thể tải form template”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Không có quyền Q1 mà vào bằng đường dẫn trực tiếp → chuyển tới trang không tìm thấy.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa mẫu', shot=shot('07-sua.png'),
         shot_caption='Màn Chỉnh sửa mẫu phiếu đang Hoạt động — chỉ còn nút Lưu và duyệt, ô Ứng dụng bị khoá')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang “Chỉnh sửa Form”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Các thành phần dựng phiếu', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu',
     'Giống màn Tạo mới (mục 2.4.4).'),
    ('Ứng dụng', 'Dropdown', 'Enable / Disable', 'Ứng dụng đang Hoạt động + Ứng dụng đang gán', 'Có',
     'Theo dữ liệu', 'Bị khoá khi mẫu phiếu đang Hoạt động.'),
    ('Nút Lưu', 'Button', 'Enable / Ẩn', '–', '–', 'Theo trạng thái', 'Chỉ hiện khi phiếu đang Nháp.'),
    ('Nút Lưu và duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hỏi xác nhận rồi lưu ở trạng thái Hoạt động.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn trước, không lưu.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa mẫu', 'Click',
     'Before:\n– Nút chỉ hiện khi mẫu phiếu chưa Khoá.\n'
     'After:\n– Mở màn Chỉnh sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu / Lưu và duyệt', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Mẫu phiếu đang Khoá → “Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển trạng '
     'thái bởi người dùng khác. Vui lòng tải lại trang để cập nhật thông tin mới nhất” và dừng xử lý.\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Ghi lại tên, Ứng dụng, trạng thái và thay toàn bộ Section, Group, câu hỏi, đáp án theo '
     'nội dung trên màn; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Thông báo “Lưu nháp thành công” / “Lưu và duyệt thành công”, về màn danh sách.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Xem chi tiết mẫu phiếu')
d.p('2.8.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết mẫu phiếu',
    mota='Xem mẫu phiếu ở dạng phiếu hoàn chỉnh (như người trả lời sẽ thấy): tên phiếu, người tạo, '
         'ngày tạo, Ứng dụng và toàn bộ Section, Group, câu hỏi, đáp án, dấu * câu bắt buộc.',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm vào Mã mẫu phiếu trên bảng.\n'
          '2. Hệ thống mở màn “Chi tiết Form” ở chế độ chỉ đọc.\n'
          '3. (Tuỳ chọn) Bấm In mẫu phiếu (FR-10) hoặc Sao chép (FR-09).\n'
          '4. Bấm Quay lại để về danh sách.',
    phu='• Không tải được dữ liệu → “Không thể tải form template”.',
    dacbiet=None)
d.p('2.8.2 Layout màn hình')
d.layout(menu=MENU + ' => Mã mẫu phiếu', shot=shot('08-xem.png'),
         shot_caption='Màn Chi tiết mẫu phiếu')
d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Đầu phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Tên mẫu phiếu; “Người tạo: <tên> · Ngày tạo: dd/mm/yyyy hh:mm”.'),
    ('Mục “1. Thông tin chọn” – Ứng dụng', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', 'Tên Ứng dụng của phiếu.'),
    ('Section (A, B, C…)', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Tiêu đề và mô tả section.'),
    ('Group (Hiện trạng…)', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Tên nhóm và câu hỏi con.'),
    ('Câu hỏi', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Số thứ tự, nội dung, dấu * nếu bắt buộc, ô trả lời mẫu theo loại (ô nhập, lựa chọn, ngày, tệp…).'),
    ('Nút In mẫu phiếu', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Xem trước mẫu phiếu in.'),
    ('Nút Sao chép', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở màn Tạo mới từ bản sao.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
], required=False)
d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Mã mẫu phiếu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Mở màn chi tiết ở chế độ chỉ đọc.'),
    ('Bấm In mẫu phiếu / Sao chép', 'Click', 'After:\n– Chuyển sang FR-10 / FR-09.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về màn danh sách.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Sao chép mẫu phiếu')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Sao chép mẫu phiếu', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-09 Sao chép mẫu phiếu')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Sao chép mẫu phiếu',
    mota='Tạo mẫu phiếu mới từ một mẫu phiếu có sẵn: màn Tạo mới được điền sẵn tên, Ứng dụng và đủ toàn '
         'bộ Section, Group, câu hỏi của phiếu nguồn để người dùng sửa tiếp.',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin',
    dieukien='Người dùng có quyền Q1. Áp dụng với mẫu phiếu ở mọi trạng thái.',
    chinh='1. Người dùng bấm Sao chép mẫu trên dòng (hoặc nút Sao chép ở màn chi tiết).\n'
          '2. Hệ thống mở màn Tạo mới, điền sẵn: Tên = “<tên phiếu nguồn> - Sao chép”, cùng Ứng dụng, '
          'toàn bộ Section, Group, câu hỏi, đáp án, cờ bắt buộc, logic hiển thị.\n'
          '3. Người dùng chỉnh sửa và Lưu / Lưu và duyệt như FR-04.',
    phu='• Người dùng đổi sang Ứng dụng khác → câu hỏi / nhóm phạm vi “Theo ứng dụng” của phiếu nguồn bị '
        'bỏ, thông báo “Đã bỏ <n> câu hỏi thuộc phạm vi \"Theo ứng dụng\" của ứng dụng cũ.”\n'
        '• Không tải được phiếu nguồn → “Không thể tải dữ liệu mẫu phiếu để sao chép”.',
    dacbiet='Bản sao luôn bắt đầu ở trạng thái Nháp và nhận mã mới; phiếu nguồn không thay đổi.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Sao chép mẫu', shot=shot('09-sao-chep.png'),
         shot_caption='Màn Tạo mới được điền sẵn từ mẫu phiếu nguồn')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tên form', 'Textbox', 'Enable', '1–255 ký tự', 'Có', '“<tên phiếu nguồn> - Sao chép”', '–'),
    ('Ứng dụng', 'Dropdown', 'Enable', 'Ứng dụng đang Hoạt động', 'Có', 'Ứng dụng của phiếu nguồn',
     'Đổi thì bỏ câu hỏi phạm vi “Theo ứng dụng”.'),
    ('Section / Group / câu hỏi', 'Table/Grid', 'Enable', '–', '–', 'Như phiếu nguồn',
     'Sửa được như màn Tạo mới.'),
    ('Nút Lưu / Lưu và duyệt / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Như màn Tạo mới.'),
])
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Sao chép mẫu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Nạp dữ liệu phiếu nguồn, mở màn Tạo mới đã điền sẵn.'),
    ('Bấm Lưu / Lưu và duyệt', 'Click', 'After:\n– Xử lý như FR-04; tạo mẫu phiếu mới với mã mới.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 In mẫu phiếu')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'In mẫu phiếu', 'io', actor=A_QL, caption='Biểu đồ Use Case — FR-10 In mẫu phiếu')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột (phần In).', anchor='excel')
d.intro_table(
    ten='In mẫu phiếu',
    mota='Xem trước và in mẫu phiếu thành “PHIẾU THU THẬP THÔNG TIN DỰ ÁN” gồm letterhead công ty, tên, '
         'mã, Ứng dụng, ngày in, người in và bảng Nội dung khảo sát (STT, Nội dung, Loại câu hỏi, Giá trị '
         'lựa chọn đi kèm).',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin',
    dieukien='Người dùng có quyền Q1. Áp dụng với mẫu phiếu ở mọi trạng thái.',
    chinh='1. Người dùng bấm “…” trên dòng rồi chọn In mẫu phiếu (hoặc nút In mẫu phiếu ở màn chi tiết).\n'
          '2. Hệ thống mở cửa sổ “Xem trước mẫu phiếu in”.\n'
          '3. Người dùng bấm In → trình duyệt mở hộp thoại in.',
    phu='• Không tải được mẫu phiếu → “Không thể tải mẫu phiếu để in”.\n'
        '• Trình duyệt chặn cửa sổ bật lên → “Không thể mở cửa sổ in. Vui lòng cho phép popup.”\n'
        '• Bấm Đóng → đóng cửa sổ xem trước.',
    dacbiet='Câu hỏi bắt buộc được đánh dấu (*) màu đỏ trên bản in.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => In mẫu phiếu', modal='Xem trước mẫu phiếu in',
         shot=shot('12-in.png'), shot_caption='Cửa sổ Xem trước mẫu phiếu in')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Letterhead công ty', 'Label', 'Read-only', '–', 'Theo cấu hình công ty', 'Logo, tên, địa chỉ.'),
    ('Tiêu đề “PHIẾU THU THẬP THÔNG TIN DỰ ÁN”', 'Label', 'Read-only', '–', 'Hiển thị', '–'),
    ('Tên mẫu phiếu / Mã mẫu phiếu / Ứng dụng', 'Label', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Ngày in mẫu / Người in mẫu', 'Label', 'Read-only', 'dd/mm/yyyy', 'Ngày hiện tại / người đăng nhập', '–'),
    ('Bảng Nội dung khảo sát', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cột STT, Nội dung, Loại câu hỏi, Giá trị lựa chọn đi kèm; dòng section / group đánh số riêng.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở hộp thoại in của trình duyệt.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn In mẫu phiếu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Nạp chi tiết mẫu phiếu, mở cửa sổ xem trước.'),
    ('Bấm In', 'Click', 'After:\n– Mở cửa sổ in với nội dung bản xem trước và bật hộp thoại in.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Xoá mẫu phiếu')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xoá mẫu phiếu', 'action', actor=A_QL, caption='Biểu đồ Use Case — FR-11 Xoá mẫu phiếu')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa.', anchor='delete')
d.intro_table(
    ten='Xoá mẫu phiếu',
    mota='Xoá hẳn một mẫu phiếu đang Nháp cùng toàn bộ Section, Group, câu hỏi, đáp án của nó.',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin',
    dieukien='Người dùng có quyền Q1; mẫu phiếu đang Nháp.',
    chinh='1. Người dùng bấm nút Xoá mẫu trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xoá mẫu phiếu, thông báo “Xoá mẫu phiếu thành công” và nạp lại danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xoá.\n'
        '• Mẫu phiếu Hoạt động / Khoá → nút Xoá mẫu bị ẩn; muốn ngừng dùng thì Khoá.\n'
        '• Lỗi khi xoá → “Lỗi khi xoá mẫu phiếu” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Xoá là xoá hẳn, không khôi phục được. Câu hỏi trong Ngân hàng câu hỏi khảo sát không bị xoá theo.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xoá mẫu', modal='Xác nhận xóa', shot=shot('10-xoa.png'),
         shot_caption='Hộp thoại xác nhận xoá mẫu phiếu')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa mẫu phiếu \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xoá.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xoá.'),
], required=False, scope=False)
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xoá mẫu trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện khi mẫu phiếu đang Nháp.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Xoá mẫu phiếu cùng Section, Group, câu hỏi, đáp án.\n'
     '– Thông báo “Xoá mẫu phiếu thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.12
d.h3('2.12 Khoá / Mở khoá mẫu phiếu')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Khoá / Mở khoá mẫu phiếu', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-12 Khoá / Mở khoá mẫu phiếu')
d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khoá / Mở khoá mẫu phiếu',
    mota='Ngừng sử dụng một mẫu phiếu đang Hoạt động (Khoá) hoặc đưa mẫu phiếu đã Khoá về Hoạt động '
         '(Mở khoá).',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin',
    dieukien='Người dùng có quyền Q1; mẫu phiếu không ở trạng thái Nháp.',
    chinh='1. Người dùng bấm “…” trên dòng rồi chọn Khoá (hoặc bấm Mở khoá trên dòng đang Khoá).\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khoá” (hoặc “Xác nhận mở khoá”).\n'
          '3. Người dùng bấm Khoá (hoặc Mở khoá).\n'
          '4. Hệ thống đổi trạng thái, thông báo “Khoá mẫu phiếu thành công” / “Mở khoá mẫu phiếu thành '
          'công”, nạp lại danh sách.',
    phu='• Mở khoá khi Ứng dụng đã có mẫu phiếu Hoạt động khác → “Ứng dụng này đã có phiếu thu thập đang '
        'hoạt động”, không đổi trạng thái.\n'
        '• Mẫu phiếu Nháp → không có mục Khoá / Mở khoá.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Mở khoá đưa mẫu phiếu về trạng thái Hoạt động. Mẫu phiếu đang Khoá không Sửa được cho tới khi Mở khoá.')
d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khoá / Mở khoá', modal='Xác nhận khoá / Xác nhận mở khoá',
         shot=shot('11-khoa.png'), shot_caption='Hộp thoại xác nhận khoá mẫu phiếu')
d.figure(shot('11b-mo-khoa.png'), 'Hộp thoại xác nhận mở khoá mẫu phiếu', width_in=6.2)
d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mục Khoá / Mở khoá', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Hoạt động: mục Khoá (ổ khoá đóng). Khoá: nút Mở khoá (ổ khoá mở). Nháp: ẩn.'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khoá” / “Xác nhận mở khoá”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khoá (mở khoá) mẫu phiếu \'<tên>\'?”'),
    ('Nút Khoá / Mở khoá', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Khoá', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Đổi trạng thái sang Khoá, ghi người cập nhật.\n'
     '– Thông báo “Khoá mẫu phiếu thành công”, nạp lại danh sách.'),
    ('Bấm Mở khoá', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Ứng dụng đã có mẫu phiếu Hoạt động khác → “Ứng dụng này đã có phiếu thu thập đang '
     'hoạt động” và dừng xử lý.\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật.\n'
     '– Thông báo “Mở khoá mẫu phiếu thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.13
d.h3('2.13 Xuất Excel')
d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'Xuất Excel danh sách mẫu phiếu', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-13 Xuất Excel')
d.p('2.13.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Phiếu thu thập thông tin.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách mẫu phiếu',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_sach_mau_phieu_thu_thap_thong_tin.xlsx '
         'gồm TẤT CẢ mẫu phiếu khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý mẫu phiếu thu thập thông tin',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất Excel.\n'
          '3. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng.\n'
          '4. Người dùng tích / bỏ tích, kéo để đổi thứ tự trường, rồi bấm Xuất file.\n'
          '5. Trình duyệt tải tệp về, thông báo “Xuất Excel thành công”.',
    phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” để chọn nhanh.\n'
        '• Lỗi khi dựng tệp → thông báo “Lỗi khi xuất Excel”.',
    dacbiet='Nút Xuất Excel bị khoá trong lúc đang xuất để tránh bấm lặp.')
d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('13-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '9 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Mã mẫu phiếu, Tên mẫu phiếu, Ứng dụng, Số câu hỏi, Người tạo, Ngày tạo, Người cập nhật, Ngày cập '
     'nhật, Trạng thái. Kéo ⠿ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/9 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_mau_phieu_thu_thap_thong_tin.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.13.5 Danh sách event và xử lý event')
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
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Phiếu thu thập thông tin; không lặp lại các quy '
           'tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Mã mẫu phiếu tự sinh', [
        '– Mã dạng PTT-YYYY-NNNNN, hệ thống sinh khi lưu lần đầu (kể cả bản sao), không trùng.',
        '– Người dùng không nhập, không sửa được mã.',
    ], ['Tạo mới', 'Sao chép']),
    ('BR-02', 'Thông tin bắt buộc của mẫu phiếu', [
        '– Tên form bắt buộc, tối đa 255 ký tự; Ứng dụng bắt buộc.',
        '– Phải có ít nhất 1 Section; mỗi Section có tiêu đề (≤ 255 ký tự), mô tả ≤ 500 ký tự và ít nhất '
        '1 câu hỏi (trực tiếp hoặc trong Group).',
    ], ['Tạo mới', 'Chỉnh sửa', 'Sao chép']),
    ('BR-03', 'Mỗi Ứng dụng chỉ 1 mẫu phiếu Hoạt động', [
        '– Lưu và duyệt, hoặc Mở khoá, bị chặn khi Ứng dụng đã có mẫu phiếu Hoạt động khác.',
        '– Lưu Nháp không bị giới hạn số lượng.',
        '– Mẫu phiếu Hoạt động của Ứng dụng là phiếu được dùng khi thu thập thông tin dự án.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Khoá / Mở khoá']),
    ('BR-04', 'Vòng đời trạng thái', [
        '– Nháp → (Lưu và duyệt) → Hoạt động → (Khoá) → Khoá → (Mở khoá) → Hoạt động.',
        '– Nháp: được Sửa, Xoá; không Khoá. Hoạt động: được Sửa (giữ Hoạt động), Khoá; không Xoá, không '
        'đổi Ứng dụng. Khoá: chỉ Mở khoá, Sao chép, In, Xem.',
    ], ['Danh sách', 'Chỉnh sửa', 'Xoá', 'Khoá / Mở khoá']),
    ('BR-05', 'Câu hỏi lấy từ Ngân hàng câu hỏi', [
        '– Thư viện chỉ hiện câu hỏi đang Hoạt động, phạm vi “Tất cả” hoặc đúng Ứng dụng của phiếu.',
        '– Mỗi câu hỏi chỉ xuất hiện 1 lần trong phiếu (đã dùng thì ẩn khỏi thư viện).',
        '– Lưu phiếu có câu hỏi đã bị xoá hoặc khoá ở ngân hàng → báo lỗi, không lưu.',
        '– Câu hỏi đang dùng trong mẫu phiếu thì không xoá được ở ngân hàng; câu hỏi nhóm đang dùng thì '
        'không đổi được danh sách câu hỏi con.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Sao chép']),
    ('BR-06', 'Cấu trúc Section / Group', [
        '– Một section chứa hoặc câu hỏi, hoặc Group — không chứa cả hai.',
        '– Câu hỏi loại “Nhóm câu hỏi” khi thả vào section tự thành Group chứa các câu hỏi con.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-07', 'Đổi Ứng dụng', [
        '– Đổi sang Ứng dụng khác thì bỏ các câu hỏi / nhóm phạm vi “Theo ứng dụng” của Ứng dụng cũ; câu '
        'hỏi phạm vi “Tất cả” được giữ.',
        '– Mẫu phiếu Hoạt động không đổi được Ứng dụng.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Sao chép']),
    ('BR-08', 'Import Excel câu hỏi', [
        '– Chỉ import khi đã chọn Ứng dụng; tệp theo mẫu 6 cột.',
        '– Dòng lỗi được báo lý do cụ thể; chỉ dòng hợp lệ được nạp, mỗi Tên Section thành 1 section mới '
        'thêm vào cuối phiếu.',
        '– Dữ liệu chỉ được ghi khi Lưu mẫu phiếu; câu hỏi mới được thêm vào ngân hàng, câu trùng thì '
        'dùng lại.',
    ], ['Import Excel']),
    ('BR-09', 'Sao chép', [
        '– Bản sao giữ nguyên toàn bộ câu hỏi của phiếu nguồn, tên thêm hậu tố “ - Sao chép”, trạng thái '
        'Nháp.',
    ], 'Sao chép'),
    ('BR-10', 'Thao tác không dùng được thì ẩn', [
        '– Sửa mẫu ẩn khi Khoá; Xoá mẫu chỉ hiện khi Nháp; Khoá / Mở khoá ẩn khi Nháp.',
        '– Không hiển thị nút xám.',
    ], 'Danh sách'),
    ('BR-11', 'Xuất theo bộ lọc, chọn trường', [
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)
