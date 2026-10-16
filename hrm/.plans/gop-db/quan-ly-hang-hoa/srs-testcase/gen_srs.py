# -*- coding: utf-8 -*-
"""Sinh SRS - Hang hoa nhap thong tin (luong Chuyen doi hang hoa) — form chuan 2026-09-24.

Pham vi: man "Hang hoa nhap thong tin" + Tao moi / Sua / Xem chi tiet / Xoa / Khoa - Mo khoa hang hoa
+ Lap yeu cau hoi gia + Xuat Excel. Tap trung cac quy tac lien quan GIA BAN (bo gia theo cong ty,
trang thai trong luong tinh gia).

Nguon doi chieu code: worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa
(hrm-api 46385a8b4, hrm-client 495c4eecf) — doc ngay 16/10/2026.
Anh chup: Playwright MCP 1440x900, cong 3031 (worktree), tai khoan E2E Assign.
Luu y: DB dev khong co hang o trang thai Dang nhap thong tin -> anh danh sach dung du lieu hang THAT
lay tu man Hang dang kinh doanh, gan trang thai minh hoa (1/2/5) de thay du cac cot + nut dong.

Chay:  python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_srs.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HRM = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(HRM, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'hang-hoa_shots')
OUT = os.path.join(HERE, 'SRS - Hàng hoá nhập thông tin.docx')


def shot(name):
    return os.path.join(SHOTS, name)


ACTOR = 'Nhân viên xây dựng thông tin hàng hoá'
MENU = 'Phân hệ Danh mục => Hàng hoá => Hàng hoá, vật tư => Hàng hoá nhập thông tin'
MENU_TRADING = 'Phân hệ Danh mục => Hàng hoá => Hàng hoá, vật tư => Hàng đang kinh doanh'

d = SrsDoc(out=OUT, menu=MENU, route='/master-data/products/entering',
           full_url='http://hrm/master-data/products/entering', img_prefix='hhntt_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ Danh mục': 'icon_phanhe.png',
    'Hàng hoá': 'icon_rail_hanghoa.png',
    'Hàng hoá, vật tư': 'icon_nhom_hanghoavattu.png',
    'Hàng hoá nhập thông tin': 'icon_hanghoanhapthongtin.png',
    'Tạo mới': 'icon_taomoi.png',
    'Sửa': 'icon_sua.png',
    'Xóa': 'icon_xoa.png',
    'Xem chi tiết': 'icon_xem.png',
    'Khóa': 'icon_khoa.png',
    'Mở khóa': 'icon_mokhoa.png',
    'Lập yêu cầu hỏi giá': 'icon_lapychg.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Tuỳ chỉnh cột': 'icon_tuychinhcot.png',
    'Xuất Excel': 'icon_xuatexcel.png',
}.items()})

# ============================================================== TRANG DAU
d.title_block('Hàng hoá nhập thông tin')
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Hàng hoá nhập thông tin và các thao tác trên '
    'một mã hàng (Tạo mới, Chỉnh sửa, Xem chi tiết, Xóa, Khóa / Mở khóa) thuộc luồng Chuyển đổi hàng hoá '
    'sang hệ thống mới, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn Hàng hoá nhập thông tin.',
    'Làm rõ vòng đời hàng hoá THEO TỪNG CÔNG TY: Đang nhập thông tin → Chờ tính giá bán → Đang tính giá '
    '→ Đang kinh doanh ⇄ Ngừng kinh doanh, và việc nào làm hàng đổi trạng thái.',
    'Làm rõ mọi điểm hàng hoá chạm tới GIÁ BÁN: bộ giá rỗng sinh ra khi tạo hàng / thêm đơn vị tính / lấy về, '
    'bộ giá bị xóa khi xóa / gỡ hàng, giá giữ nguyên khi khóa / mở khóa, hàng chưa có giá không bán được.',
    'Làm rõ 2 phạm vi sửa: công ty tạo hàng sửa toàn bộ, công ty lấy hàng về chỉ khai tab Quản trị hàng hoá.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Công ty đang làm việc', 'Công ty người dùng đang chọn ở góc trên màn hình. Quyền, trạng thái hàng, '
     'dữ liệu quản trị và giá đều xét theo công ty này.'),
    ('Công ty quản lý (công ty tạo)', 'Công ty tạo ra mã hàng. Chỉ công ty này được sửa Thông tin hàng hoá '
     '(phần dùng chung mọi công ty).'),
    ('Lấy về công ty', 'Công ty khác đưa một mã hàng đang kinh doanh của công ty tạo vào dùng (thao tác ở '
     'màn Kho dữ liệu hàng hoá). Hàng lấy về bắt đầu ở trạng thái Đang nhập thông tin.'),
    ('Thông tin hàng hoá', 'Phần CHUNG của mã hàng (tên, model, phân loại, nguồn gốc, đơn vị tính, thông số, '
     'thuế…), mọi công ty dùng chung một bản.'),
    ('Quản trị hàng hoá', 'Phần RIÊNG của từng công ty: nhà cung cấp, chính sách kinh doanh, tồn kho tối thiểu, '
     'bảo hành, catalog kinh doanh. Hệ số công nghệ nằm ở tab này nhưng dùng chung, chỉ công ty tạo sửa.'),
    ('Trạng thái theo công ty', 'Mỗi công ty có 1 trạng thái riêng với 1 mã hàng: Đang nhập thông tin · '
     'Chờ tính giá bán · Đang tính giá · Đang kinh doanh · Ngừng kinh doanh. Công ty chưa dùng hàng: '
     '“Chưa sử dụng”.'),
    ('Bộ giá', 'Với MỖI đơn vị tính, MỖI công ty có 6 loại giá bán (Bán lẻ, Đại lý cấp 1, Đại lý cấp 2, '
     'Đại lý cấp 3, Giá bán theo lô, TMĐT) và 1 giá vốn. Giá của đơn vị quy đổi lưu riêng, không tự tính '
     'từ đơn vị cơ bản × hệ số.'),
    ('Bộ giá rỗng', 'Bộ giá có đủ dòng nhưng mọi giá = 0. Sinh tự động khi tạo hàng, thêm đơn vị tính, lấy hàng về.'),
    ('YCHG', 'Yêu cầu hỏi giá — phiếu người kinh doanh lập để đưa hàng vào luồng tính giá.'),
    ('PTG', 'Phiếu tính giá — phiếu bộ phận xuất nhập khẩu / kế toán mua hàng lập để ra giá bán.'),
    ('PTKD', 'Người duyệt YCHG (phát triển kinh doanh).'),
    ('Khóa (Ngừng kinh doanh)', 'Chuyển hàng Đang kinh doanh sang Ngừng kinh doanh TẠI CÔNG TY ĐANG LÀM VIỆC. '
     'Không xóa dữ liệu, không xóa giá.'),
    ('Xóa cứng', 'Công ty tạo xóa hẳn mã hàng và mọi dữ liệu đi kèm (kể cả giá của mọi công ty).'),
    ('Gỡ', 'Công ty đã lấy hàng về bấm Xóa: chỉ xóa phần của công ty mình, hàng vẫn còn ở công ty tạo.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nguyên tắc chung (đã chốt): thông tin hàng hoá và giá bán KHÔNG bảo mật; quyền chỉ kiểm soát ai được '
    'thao tác ghi dữ liệu và ai được xem giá vốn. Mọi quyền xét theo CÔNG TY ĐANG LÀM VIỆC — có quyền ở '
    'công ty khác không được tính. Super admin không được miễn: thiếu quyền là không thao tác được.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Xây dựng thông tin hàng hoá',
     'Thấy menu và mở được màn Hàng hoá nhập thông tin; nút Tạo mới, Kho dữ liệu; cột Hành động (Sửa, Xóa); '
     'các nút Sửa / Xóa / Khóa / Mở khóa ở màn Xem chi tiết; mở được màn Sửa.'),
    ('Q2', 'Xuất excel danh sách hàng hoá', 'Nút Xuất Excel (cần kèm Q1 vì phải mở được màn).'),
    ('Q3', 'Quản lý danh mục model', 'Nút “+” cạnh ô Model trên form Tạo mới / Sửa để thêm nhanh model.'),
    ('Q4', 'Xem giá vốn hàng hoá', 'Không có tác dụng trên màn này: màn Hàng hoá nhập thông tin, form và màn '
     'chi tiết KHÔNG hiển thị giá bán lẫn giá vốn với bất kỳ ai. Ghi vào bảng để tránh hiểu nhầm.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận). Phạm vi dữ liệu cố định: hàng '
    'có trạng thái Đang nhập thông tin, Chờ tính giá bán hoặc Đang tính giá TẠI CÔNG TY ĐANG LÀM VIỆC.')
d.p('Thao tác “Lập yêu cầu hỏi giá” không cần quyền riêng (ai mở được màn đều dùng được).')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Q4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '❌ (cần Q1)', '❌', '❌', '❌ (không thấy menu; hệ thống từ chối tải danh sách)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌', '❌', '❌', '❌'),
    ('FR-03 Tuỳ chỉnh cột', '✅', '❌', '❌', '❌', '❌'),
    ('FR-04 Xem chi tiết hàng hoá', '✅', '✅', '✅', '✅', '✅ (chỉ xem, không có nút thao tác)'),
    ('FR-05 Tạo mới hàng hoá', '✅', '❌', '✅ nút “+” Model (kèm Q1)', '❌', '❌'),
    ('FR-06 Chỉnh sửa hàng hoá', '✅', '❌', '✅ nút “+” Model (kèm Q1)', '❌', '❌'),
    ('FR-07 Xóa hàng hoá', '✅', '❌', '❌', '❌', '❌'),
    ('FR-08 Khóa / Mở khóa hàng hoá', '✅', '❌', '❌', '❌', '❌'),
    ('FR-09 Lập yêu cầu hỏi giá', '✅', '❌ (cần Q1 để mở màn)', '❌', '❌', '❌'),
    ('FR-10 Xuất Excel', '✅ + Q2', '✅ + Q1', '❌', '❌', '❌'),
], widths=[2.0, 0.5, 0.8, 1.0, 0.4, 1.3])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2, 3, 4, 5, 6])],
    [('FR-01', 'Xem danh sách hàng hoá nhập thông tin', 'view'),
     ('FR-05', 'Tạo mới hàng hoá', 'crud'),
     ('FR-06', 'Chỉnh sửa hàng hoá', 'crud'),
     ('FR-07', 'Xóa hàng hoá', 'action'),
     ('FR-08', 'Khóa / Mở khóa hàng hoá', 'action'),
     ('FR-09', 'Lập yêu cầu hỏi giá', 'action'),
     ('FR-10', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-04', 'Xem chi tiết hàng hoá', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Hàng hoá nhập thông tin')

d.h2('2 Đặc tả chi tiết từng chức năng')

LIST_RULE = ('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc '
             'riêng của màn Hàng hoá nhập thông tin tại phần mô tả chi tiết.')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách hàng hoá nhập thông tin')
d.p('2.1.1 Giới thiệu')
d.rule_ref(LIST_RULE, anchor='list')
d.intro_table(
    ten='Xem danh sách hàng hoá nhập thông tin',
    mota='Hiển thị các mã hàng công ty đang làm việc đang khai thông tin hoặc đang nằm trong luồng tính giá '
         '(chưa bán được): trạng thái Đang nhập thông tin, Chờ tính giá bán, Đang tính giá. Gồm cả hàng công ty '
         'mình tạo lẫn hàng lấy về từ công ty khác.',
    tacnhan=ACTOR + '; Người dùng đã đăng nhập',
    dieukien='Người dùng có quyền Xây dựng thông tin hàng hoá tại công ty đang làm việc.',
    chinh='1. Người dùng vào menu Danh mục → Hàng hoá → Hàng hoá, vật tư → Hàng hoá nhập thông tin.\n'
          '2. Hệ thống lấy các hàng có trạng thái Đang nhập thông tin / Chờ tính giá bán / Đang tính giá tại công ty '
          'đang làm việc, sắp theo Ngày cập nhật mới nhất trước.\n'
          '3. Bảng hiển thị trang 1 (20 dòng) và dòng “Hiển thị a–b / N” ở chân bảng.',
    phu='• Không có hàng nào → bảng hiện “Không có hàng hoá nào”, chân bảng “Không có hàng hoá nào.”.\n'
        '• Người dùng không có quyền tại công ty đang làm việc → không thấy menu; mở trực tiếp màn thì hệ thống '
        'báo không có quyền và bảng rỗng.\n'
        '• Đổi công ty đang làm việc → danh sách tải lại theo công ty mới.\n'
        '• Hàng đã sang Đang kinh doanh hoặc Ngừng kinh doanh → không còn ở màn này (xem ở màn Hàng đang kinh '
        'doanh / Dữ liệu hàng hoá công ty).')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Hàng hoá nhập thông tin (dữ liệu minh hoạ đủ 3 trạng thái)')
d.layout(menu=MENU, shot=shot('04-cot-hanh-dong.png'),
         shot_caption='Phía phải bảng: cột Trạng thái và cột Hành động theo từng trạng thái')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Hàng hoá nhập thông tin',
     'Tiêu đề trên thanh đầu trang và tiêu đề khối bảng.'),
    ('Nút Kho dữ liệu', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q1', [
        '- Chỉ hiện khi có quyền Xây dựng thông tin hàng hoá.',
        '- Tooltip: “Lấy hàng hoá của công ty khác về — mở Kho dữ liệu, chỉ hàng công ty chưa dùng”.',
        '- Bấm → mở màn Kho dữ liệu hàng hoá, bật sẵn lọc “Chỉ hàng công ty chưa dùng”.']),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q1', [
        '- Chỉ hiện khi có quyền Xây dựng thông tin hàng hoá.',
        '- Bấm → mở màn Thêm mới hàng hoá (mục 2.5).']),
    ('Nút Lập yêu cầu hỏi giá', 'Button', 'Enable', '–', 'Hiển thị', [
        '- Luôn hiện, không cần quyền riêng.',
        '- Tooltip: “Lập yêu cầu hỏi giá — tick hàng trước để nạp sẵn vào phiếu”.',
        '- Bấm → mở màn Tạo yêu cầu hỏi giá, nạp sẵn hàng đã tick (mục 2.9).']),
    ('Nút Xuất Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q2',
     ['- Chỉ hiện khi có quyền Xuất excel danh sách hàng hoá.', '- Bấm → mở popup Chọn trường xuất file (mục 2.10).']),
    ('Nút Cấu hình cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
     ['- Tooltip: “Cấu hình cột hiển thị”.', '- Bấm → mở popup Tuỳ chỉnh cột (mục 2.3).']),
    ('Thanh chọn hàng loạt', 'Label', 'Enable / Ẩn', '–', 'Ẩn', [
        '- Hiện khi đã tick ≥ 1 dòng: “Đã chọn n hàng hoá” (n = số dòng đã tick, giữ qua các trang).',
        '- Nút Lập yêu cầu hỏi giá: lập phiếu cho các hàng đã tick.',
        '- Nút Bỏ chọn: bỏ tick toàn bộ.']),
    ('Cột ô tick', 'Checkbox', 'Enable / Ẩn', '–', 'Bỏ tick', [
        '- Cột khoá, luôn ghim trái.',
        '- Chỉ dòng trạng thái Đang nhập thông tin có ô tick; dòng Chờ tính giá bán / Đang tính giá để trống '
        'vì hàng đã nằm trong một YCHG khác.',
        '- Ô tick ở tiêu đề: tick / bỏ tick mọi dòng tick được của trang đang xem.',
        '- Không giới hạn số dòng tick.']),
    ('Cột STT', 'Table/Grid', 'Read-only', 'Số nguyên', 'Theo trang',
     'Cột khoá, ghim trái. Đánh số liên tục theo trang.'),
    ('Cột Mã hàng', 'Table/Grid', 'Read-only', '≤ 32 ký tự', 'Theo dữ liệu', [
        '- Cột khoá, ghim trái, sắp xếp được.',
        '- Mã do hệ thống sinh khi tạo hàng (xem BR-04).',
        '- Bấm mã → mở màn Xem chi tiết hàng hoá ngay tại tab hiện tại (mục 2.4); Quay lại trở về đúng màn này.']),
    ('Cột Ảnh', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Ảnh đại diện (ảnh đầu tiên của hàng). Không có ảnh → biểu tượng ảnh trống.'),
    ('Cột Tên hàng hoá', 'Table/Grid', 'Read-only', '≤ 255 ký tự', 'Hiển thị',
     ['- Sắp xếp được.', '- Hiện tối đa 2 dòng, rê chuột thấy toàn văn.']),
    ('Cột Model', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Tên model của hàng.'),
    ('Cột Tính chất hàng hoá', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Suy từ Loại sản phẩm. Hàng chưa phân loại → để trống.'),
    ('Cột Nhóm chức năng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Suy từ Loại sản phẩm.'),
    ('Cột Nhóm sản phẩm', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Suy từ Loại sản phẩm.'),
    ('Cột Loại sản phẩm', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Loại sản phẩm đã chọn trên form.'),
    ('Cột Thương hiệu', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Thương hiệu của hàng.'),
    ('Cột Hãng sản xuất', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Hãng sản xuất của hàng.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 3 giá trị', 'Hiển thị', [
        '- Trạng thái của hàng TẠI CÔNG TY ĐANG LÀM VIỆC.',
        '- Đang nhập thông tin: nền xám.',
        '- Chờ tính giá bán: nền cam (đã gửi YCHG).',
        '- Đang tính giá: nền xanh dương (đã có phiếu tính giá đang làm).']),
    ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q1', [
        '- Cột chỉ có khi người dùng có quyền Xây dựng thông tin hàng hoá.',
        '- Bút chì “Sửa”: hiện với hàng sửa được (mục 2.6).',
        '- Thùng rác đỏ “Xóa”: chỉ hiện với hàng Đang nhập thông tin đủ điều kiện xóa (mục 2.7).',
        '- Màn này không bao giờ có Khóa / Mở khóa (chỉ hàng Đang kinh doanh mới khóa được).']),
    ('Cột tắt sẵn (bật ở Tuỳ chỉnh cột)', 'Table/Grid', 'Read-only', '–', 'Ẩn', [
        '- Barcode; ĐVT (đơn vị cơ bản); Xuất xứ; Code đặt hàng; Tên tiếng Anh.',
        '- % VAT: số + “%”.',
        '- Bảo hành: theo công ty đang làm việc, vd “12 tháng”.',
        '- SL tồn kho tối thiểu: số có dấu phẩy ngăn nghìn.',
        '- Công ty quản lý (công ty tạo); Người nhập thông tin; Ngày cập nhật (dd/mm/yyyy, sắp xếp được).']),
    ('Không có cột giá', 'Label', 'Hiển thị', '–', '–',
     'Bảng KHÔNG có cột Giá vốn, Giá bán lẻ hay bất kỳ giá nào (đã chốt bỏ). Ô rỗng hiển thị trống, không có “—”.'),
    ('Chân bảng', 'Pagination', 'Enable', '20 / 50 / 100', '20 dòng / trang', [
        '- “Hiển thị a–b / N”: a, b là dòng đầu / cuối trang; N là tổng số hàng khớp bộ lọc.',
        '- Ô “Số dòng/trang” 20 / 50 / 100; đổi số dòng → về trang 1.']),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có hàng hoá nào” giữa bảng.'),
    ('Đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Vòng quay + “Đang tải dữ liệu...”. Lỗi tải: thông báo “Lỗi khi tải dữ liệu”.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Xây dựng thông tin hàng hoá tại công ty đang làm việc.\n'
     '– Không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này” và dừng.\n'
     'During:\n– Lấy hàng có trạng thái Đang nhập thông tin / Chờ tính giá bán / Đang tính giá tại công ty đang làm việc.\n'
     '– Khôi phục bộ lọc nếu vừa quay về từ màn chi tiết / sửa trong vòng 10 phút.\n'
     'After:\n– Hiển thị trang 1, sắp theo Ngày cập nhật mới nhất.'),
    ('Bấm Mã hàng', 'Click', 'After:\n– Mở màn Xem chi tiết hàng hoá; hệ thống ghi nhớ bộ lọc hiện tại 10 phút.'),
    ('Bấm tiêu đề cột Mã hàng / Tên hàng hoá / Ngày cập nhật', 'Click',
     'After:\n– Đổi chiều sắp xếp, tải lại từ trang 1, giữ nguyên bộ lọc.'),
    ('Tick ô dòng / ô tiêu đề', 'Change',
     'After:\n– Cập nhật “Đã chọn n hàng hoá”; tick giữ khi chuyển trang.\n– Dòng không phải Đang nhập thông tin không tick được.'),
    ('Bấm Bỏ chọn', 'Click', 'After:\n– Bỏ toàn bộ tick, ẩn thanh chọn hàng loạt.'),
    ('Đổi trang / số dòng mỗi trang', 'Click / Change', 'After:\n– Tải lại dữ liệu; đổi số dòng thì về trang 1.'),
    ('Bấm Kho dữ liệu', 'Click', 'After:\n– Mở màn Kho dữ liệu hàng hoá với lọc “Chỉ hàng công ty chưa dùng”.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của màn Hàng hoá nhập '
           'thông tin tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc hàng hoá nhập thông tin',
    mota='Thu hẹp danh sách theo từ khoá và các ô lọc phân loại, nguồn gốc, trạng thái, người nhập.',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Hàng hoá nhập thông tin.',
    chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi nhấn Enter hoặc bấm Tìm kiếm.\n'
          '2. Muốn lọc thêm: bấm Tìm kiếm nâng cao để mở các ô lọc, chọn giá trị.\n'
          '3. Hệ thống tải lại danh sách từ trang 1 theo điều kiện đã chọn.',
    phu='• Bấm Làm mới → xoá toàn bộ điều kiện + thứ tự sắp xếp, về trang 1.\n'
        '• Đổi cấp trên của cây phân loại → các cấp dưới bị xoá trắng.\n'
        '• Không có kết quả → “Không có hàng hoá nào”.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc-nang-cao.png'),
         shot_caption='Khối bộ lọc khi mở Tìm kiếm nâng cao')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối', 'Label', 'Hiển thị', '–', 'Không', 'Bộ lọc danh sách', 'Tiêu đề khối lọc.'),
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
        '- Placeholder: “Tìm theo mã, tên hàng hoá, model, barcode”.',
        '- Tìm gần đúng trên Mã hàng, Tên hàng hoá, Barcode, tên Model.',
        '- Không tự tìm khi gõ: chỉ chạy khi nhấn Enter hoặc bấm Tìm kiếm.',
        '- Có nút ✕ xoá nhanh khi đã có chữ.']),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chạy tìm theo từ khoá + các ô lọc, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá mọi điều kiện lọc và sắp xếp, về trang 1, tải lại.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Đóng',
     ['- Mặc định khối ô lọc đang đóng.', '- Bấm để mở / đóng các ô lọc.']),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở popup ẩn / hiện và đổi thứ tự ô lọc; cấu hình lưu theo người dùng.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống (= cả 3)', [
        '- Mặc định: trống = lấy cả 3 trạng thái.',
        '- Đang nhập thông tin.', '- Chờ tính giá bán.', '- Đang tính giá.']),
    ('Tính chất hàng hoá', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Cấp 1 của cây phân loại.', '- Đổi giá trị → xoá trắng Nhóm chức năng, Nhóm sản phẩm, Loại sản phẩm.']),
    ('Nhóm chức năng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Chỉ liệt kê nhóm thuộc Tính chất đã chọn (chưa chọn → liệt kê hết).', '- Đổi → xoá trắng 2 cấp dưới.']),
    ('Nhóm sản phẩm', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Chỉ liệt kê nhóm thuộc Nhóm chức năng đã chọn.', '- Đổi → xoá trắng Loại sản phẩm.']),
    ('Loại sản phẩm', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Chỉ liệt kê loại thuộc Nhóm sản phẩm đã chọn.', '- Loại đã khoá có biểu tượng ổ khoá trước tên.']),
    ('Thương hiệu', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Thương hiệu đang hoạt động, sắp theo tên.'),
    ('Hãng sản xuất', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Hãng sản xuất đang hoạt động.'),
    ('Xuất xứ', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Xuất xứ đang hoạt động.'),
    ('Công ty quản lý', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Lọc theo công ty TẠO hàng — dùng để tách hàng mình tạo và hàng lấy về.'),
    ('Người nhập thông tin', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Người tạo mã hàng. Hiển thị “Tên nhân viên - Mã phòng - Mã nhân viên”.'),
    ('Model', 'Dropdown', 'Enable', 'Tìm trên máy chủ', 'Không', 'Trống',
     ['- Gõ để tìm (tối đa 50 kết quả mỗi lần).', '- Không tải sẵn cả danh mục.']),
], required=True)
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Nhấn Enter / bấm Tìm kiếm', 'Keypress / Click',
     'During:\n– Gửi từ khoá + các ô lọc.\nAfter:\n– Tải lại từ trang 1.'),
    ('Chọn giá trị một ô lọc', 'Change', 'After:\n– Tự tải lại ngay từ trang 1 (không cần bấm Tìm kiếm).'),
    ('Đổi cấp trên cây phân loại', 'Change', 'After:\n– Xoá trắng mọi cấp dưới trong cùng 1 lần tải (1 lần gọi dữ liệu).'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá toàn bộ điều kiện + sắp xếp, tải lại trang 1.'),
    ('Rời sang màn chi tiết / sửa rồi quay lại', 'System',
     'After:\n– Trong 10 phút: khôi phục đúng bộ lọc và trạng thái mở / đóng khối lọc.\n'
     '– Sang màn khác (kể cả Tạo mới, Kho dữ liệu): bộ lọc không được giữ.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Tuỳ chỉnh cột')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Hàng hoá nhập thông tin.',
           anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh cột hiển thị',
    mota='Người dùng chọn cột hiển thị và thứ tự cột của bảng; cấu hình lưu theo từng người dùng.',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Hàng hoá nhập thông tin.',
    chinh='1. Bấm nút Cấu hình cột.\n2. Tick / bỏ tick cột, kéo thả đổi thứ tự.\n3. Bấm Lưu.\n'
          '4. Hệ thống lưu cấu hình, bảng hiển thị theo cấu hình mới.',
    phu='• Bấm Đóng → không lưu.\n• Lưu lỗi → “Thao tác thất bại”.')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Tuỳ chỉnh cột', shot=shot('06-cau-hinh-cot.png'), shot_caption='Popup Tuỳ chỉnh cột')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Không', 'Tuỳ chỉnh cột',
     'Dòng hướng dẫn: “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
    ('Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Không', 'Hiển thị', 'Tick / bỏ tick mọi cột không bị khoá.'),
    ('Cột khoá: Chọn, STT, Mã hàng', 'Checkbox', 'Disable', '–', '–', 'Tick sẵn',
     ['- Không ẩn, không đổi vị trí được.', '- Tooltip: “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”.']),
    ('Cột Hành động', 'Checkbox', 'Disable', '–', '–', 'Tick sẵn',
     ['- Không ẩn được nhưng kéo đổi vị trí được.', '- Tooltip: “Cột bắt buộc — không thể ẩn, kéo để đổi vị trí”.']),
    ('Danh sách cột còn lại', 'Checkbox', 'Enable', '25 cột', 'Không', 'Theo cấu hình đã lưu', [
        '- Mặc định tick: Ảnh, Tên hàng hoá, Model, Tính chất hàng hoá, Nhóm chức năng, Nhóm sản phẩm, Loại sản phẩm, '
        'Thương hiệu, Hãng sản xuất, Trạng thái.',
        '- Bỏ tick sẵn: Barcode, ĐVT, Xuất xứ, Code đặt hàng, Tên tiếng Anh, % VAT, Bảo hành, SL tồn kho tối thiểu, '
        'Công ty quản lý, Người nhập thông tin, Ngày cập nhật.',
        '- Không có cột giá nào trong danh sách.']),
    ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '“Đang chọn x/25 cột”.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình theo người dùng, đóng popup, toast “Cập nhật thành công”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
], required=True)
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'During:\n– Lưu danh sách cột + thứ tự theo người dùng.\nAfter:\n– Toast “Cập nhật thành công”; bảng vẽ lại.\n'
     '– Lỗi → toast “Thao tác thất bại”, popup không đóng.'),
    ('Kéo thả cột', 'Change', 'After:\n– Đổi thứ tự trong popup (chưa lưu).'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Xem chi tiết hàng hoá')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của hàng hoá.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết hàng hoá',
    mota='Xem toàn bộ thông tin của một mã hàng ở chế độ chỉ đọc, kèm trạng thái tại công ty đang làm việc và '
         'các nút thao tác theo quyền + trạng thái. Màn chi tiết KHÔNG hiển thị giá.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Mở từ Mã hàng ở danh sách (hoặc từ màn khác có link mã hàng).',
    chinh='1. Bấm Mã hàng ở danh sách.\n2. Hệ thống tải dữ liệu hàng.\n'
          '3. Hiển thị tab Thông tin hàng hoá (bước Thông tin chung), badge trạng thái, dòng Người tạo / Cập nhật.\n'
          '4. Người dùng chuyển tab / bước để xem.',
    phu='• Mã hàng không tồn tại / đã bị xóa → chuyển sang trang 404.\n'
        '• Công ty đang làm việc chưa dùng hàng → badge “Chưa sử dụng” (xám).\n'
        '• Không có quyền Xây dựng thông tin hàng hoá → chỉ có nút Quay lại.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('30-chi-tiet.png'),
         shot_caption='Màn Chi tiết hàng hoá — tab Thông tin hàng hoá')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('31-chi-tiet-quan-tri.png'),
         shot_caption='Màn Chi tiết hàng hoá — tab Quản trị hàng hoá')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết hàng hoá: <Mã hàng>', 'Chưa tải xong: “Chi tiết hàng hoá”.'),
    ('Badge trạng thái', 'Badge', 'Read-only', 'Danh sách', 'Theo dữ liệu', [
        '- Trạng thái tại công ty đang làm việc, chữ + màu do hệ thống trả.',
        '- Công ty chưa dùng hàng: “Chưa sử dụng” (xám).']),
    ('Tab Thông tin hàng hoá', 'Button', 'Enable', '–', 'Đang chọn',
     'Icon ⓘ: “Thông tin CHUNG của mã hàng — mọi công ty dùng chung một bản. Chỉ công ty tạo ra hàng hoá được sửa phần này.”'),
    ('Tab Quản trị hàng hoá', 'Button', 'Enable', '–', 'Không chọn',
     'Icon ⓘ: “Dữ liệu RIÊNG của công ty đang làm việc (nhà cung cấp, chính sách kinh doanh, tồn kho tối thiểu, bảo hành, '
     'hệ số công nghệ, catalog kinh doanh). Mỗi công ty tự khai, không ảnh hưởng công ty khác.”'),
    ('Bước con', 'Button', 'Enable', '–', 'Thông tin chung', [
        '- 1 Thông tin chung · 2 Thông số kỹ thuật · 3 Mua hàng · 4 Phân loại xe · 5 Nhóm máy.',
        '- Phân loại xe chỉ hiện khi Tính chất là phụ tùng ô tô hoặc hàng đang có dữ liệu xe.']),
    ('Bước Thông tin chung', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Khối Thông tin hàng hoá: Tên hàng hoá, Model, Công ty quản lý, Tên hàng thường gọi, Tên tiếng Anh, Barcode, Ghi chú.',
        '- Khối Phân loại: Tính chất, Nhóm chức năng, Nhóm sản phẩm, Loại sản phẩm, Đặc tính.',
        '- Tính chất hàng hoá — Icon ⓘ: “Phân loại theo bản chất, vai trò của hàng hóa”.',
        '- Nhóm chức năng — Icon ⓘ: “Phân loại theo chức năng hoặc hệ kỹ thuật chính”.',
        '- Nhóm sản phẩm — Icon ⓘ: “Tập hợp các sản phẩm có cùng chức năng cơ bản”.',
        '- Loại sản phẩm — Icon ⓘ: “Phân biệt theo kết cấu, nguyên lý hoặc đặc điểm kỹ thuật”.',
        '- Đặc tính sản phẩm — Icon ⓘ: “Xác định sản phẩm thuộc loại tiêu chuẩn hay có khả năng thay đổi theo nhu cầu khách hàng”.',
        '- Khối Nguồn gốc: Thương hiệu, Xuất xứ, Hãng sản xuất, Code đặt hàng.',
        '- Khối Đơn vị tính: Đơn vị, Đơn vị cơ bản (✓), Hệ số quy đổi, Quy đổi (“1 Hộp = 10 Cái”). Rỗng: “Chưa khai đơn vị tính”.',
        '- Khối Tài liệu kỹ thuật, Hình ảnh, Video.']),
    ('Bước Thông số kỹ thuật', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     ['- Trọng lượng (kg), Kích thước (cm), Định mức công lắp đặt, bảng Thuộc tính.',
      '- Phụ kiện tiêu chuẩn, Đặc điểm; 4 bảng Công thức lắp ráp, Phụ kiện tuỳ chọn mua thêm, Vật tư phục vụ lắp đặt, '
      'Vật tư sửa chữa – bảo dưỡng.']),
    ('Bước Mua hàng', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Tên khai báo hải quan, HS Code, SL tối thiểu nhập mua, % VAT, 2 loại thuế nhập khẩu, Thuế chống bán phá giá, Hệ số tính thuế BVMT.'),
    ('Tab Quản trị hàng hoá', 'Text', 'Read-only', '–', 'Theo công ty đang làm việc', [
        '- Nhà cung cấp, Chính sách kinh doanh, SL tồn kho tối thiểu, Bảo hành, Hệ số công nghệ.',
        '- Nhà cung cấp — Icon ⓘ: “Các nhà cung cấp mà công ty đang mua mặt hàng này.”',
        '- Chính sách kinh doanh — Icon ⓘ: “Xác định chính sách kinh doanh của doanh nghiệp với từng sản phẩm”',
        '- SL tồn kho tối thiểu — Icon ⓘ: “Số lượng tồn kho tối thiểu công ty cần duy trì cho mặt hàng này — làm mốc theo dõi tồn kho để nhập bổ sung.”',
        '- Bảo hành — Icon ⓘ: “Thời gian bảo hành áp dụng khi bán mặt hàng này cho khách hàng, tính theo Đơn vị bảo hành.”',
        '- Hệ số công nghệ — Icon ⓘ: “Hệ số hưởng của kỹ thuật khi lắp đặt mặt hàng này — tự điền sang phiếu phân công lắp đặt.”',
        '- Bảng Phân loại theo lĩnh vực kinh doanh (Lĩnh vực, Chương, Mục, Tiểu mục). Rỗng: “Chưa gắn nhánh nào”.']),
    ('Không có giá', 'Label', 'Hiển thị', '–', '–',
     'Không tab, ô hay bảng nào hiện Giá bán / Giá vốn, kể cả với người có quyền Xem giá vốn hàng hoá.'),
    ('Dòng audit', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', '“Người tạo: <tên> · <ngày giờ>” và “Cập nhật: <tên> · <ngày giờ>”.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Hiện khi hàng sửa được (xem BR-08). Bấm → màn Sửa hàng hoá.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Hiện khi có Q1 và hàng đủ điều kiện xóa / gỡ (BR-11).'),
    ('Nút Khóa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Hiện khi có Q1 và hàng Đang kinh doanh tại công ty đang làm việc.'),
    ('Nút Mở khóa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Hiện khi có Q1 và hàng Ngừng kinh doanh tại công ty đang làm việc.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị',
     'Về đúng màn đã mở vào (vd Hàng hoá nhập thông tin, bộ lọc được khôi phục); không rõ màn vào → Kho dữ liệu hàng hoá.'),
], required=False)
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'During:\n– Tải dữ liệu hàng (không cần quyền).\nAfter:\n– Hiển thị; không tồn tại → trang 404.'),
    ('Bấm tab / bước', 'Click', 'After:\n– Đổi nội dung; bước Phân loại xe chỉ tải danh mục xe khi mở lần đầu.'),
    ('Bấm Sửa / Xóa / Khóa / Mở khóa', 'Click', 'After:\n– Theo mục 2.6 / 2.7 / 2.8.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Tạo mới hàng hoá')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Tạo mới hàng hoá', 'crud', actor=ACTOR,
            caption='Biểu đồ Use Case — FR-05 Tạo mới hàng hoá')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của hàng hoá.',
           anchor='create')
d.intro_table(
    ten='Tạo mới hàng hoá',
    mota='Khai một mã hàng mới thuộc công ty đang làm việc. Hệ thống tự sinh Mã hàng, đặt trạng thái '
         'Đang nhập thông tin và sinh bộ giá rỗng (giá 0) cho mỗi đơn vị tính tại công ty đang làm việc. '
         'Form KHÔNG có ô giá — muốn bán phải đi luồng hỏi giá / tính giá.',
    tacnhan=ACTOR,
    dieukien='Có quyền Xây dựng thông tin hàng hoá tại công ty đang làm việc; danh mục phân loại, thương hiệu, '
             'hãng sản xuất, xuất xứ, đơn vị tính, thuế suất, catalog đã có dữ liệu.',
    chinh='1. Bấm Tạo mới ở màn Hàng hoá nhập thông tin.\n'
          '2. Nhập bước Thông tin chung: Tên, Model, Loại sản phẩm, Thương hiệu, Xuất xứ, Hãng sản xuất, Đơn vị tính…\n'
          '3. (Tuỳ chọn) nhập Thông số kỹ thuật, Mua hàng (bắt buộc % VAT), Phân loại xe, Nhóm máy.\n'
          '4. Mở tab Quản trị hàng hoá, xếp hàng vào ít nhất 1 Tiểu mục catalog kinh doanh.\n'
          '5. Bấm Lưu.\n'
          '6. Hệ thống kiểm tra dữ liệu, sinh Mã hàng, lưu hàng với trạng thái Đang nhập thông tin, sinh bộ giá rỗng.\n'
          '7. Toast “Đã lưu hàng hoá <Mã hàng>”, chuyển sang màn Chi tiết hàng hoá vừa tạo.',
    phu='• Trống Tên hàng hoá → báo đỏ ngay dưới ô, không gửi lên máy chủ.\n'
        '• Thiếu các ô bắt buộc khác → máy chủ báo lỗi MỘT LƯỢT cho mọi ô; mọi tab / bước có lỗi hiện chấm đỏ; '
        'hệ thống mở tab lỗi đầu tiên và đưa con trỏ tới ô lỗi; toast “Vui lòng kiểm tra lại dữ liệu nhập”.\n'
        '• Trùng bộ Tên × Model × Thương hiệu × Hãng sản xuất → “Đã có hàng hoá cùng Tên, Model, Thương hiệu và Hãng sản xuất.”\n'
        '• Rời màn khi đã nhập mà chưa lưu → hỏi “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại).\n'
        '• Không tải được danh mục → khối báo lỗi đỏ + “Thử lại”, nút Lưu không hoạt động.',
    dacbiet='Không nhập giá ở form. Mỗi đơn vị tính khai lúc tạo được sinh sẵn 6 giá bán + 1 giá vốn bằng 0 '
            'cho công ty đang làm việc; hàng không vào được báo giá / chứng từ cho tới khi Đang kinh doanh.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('10-tao-moi-thong-tin-chung.png'),
         shot_caption='Thêm mới hàng hoá — bước Thông tin chung')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('11-tao-moi-thong-so.png'),
         shot_caption='Thêm mới hàng hoá — bước Thông số kỹ thuật')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('12-tao-moi-mua-hang.png'),
         shot_caption='Thêm mới hàng hoá — bước Mua hàng')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('13-tao-moi-nhom-may.png'),
         shot_caption='Thêm mới hàng hoá — bước Nhóm máy')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('14-tao-moi-quan-tri.png'),
         shot_caption='Thêm mới hàng hoá — tab Quản trị hàng hoá')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('15-tao-moi-loi-validate.png'),
         shot_caption='Bấm Lưu khi còn thiếu ô bắt buộc — mọi ô lỗi báo đỏ cùng lúc')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    # Khung
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Thêm mới hàng hoá', '–'),
    ('Tab Thông tin hàng hoá / Quản trị hàng hoá', 'Button', 'Enable', '–', '–', 'Thông tin hàng hoá',
     ['- Icon ⓘ: “Thông tin CHUNG của mã hàng — mọi công ty dùng chung một bản. Chỉ công ty tạo ra hàng hoá được sửa phần này.” (tab Thông tin hàng hoá).', '- Icon ⓘ: “Dữ liệu RIÊNG của công ty đang làm việc (nhà cung cấp, chính sách kinh doanh, tồn kho tối thiểu, bảo hành, hệ số công nghệ, catalog kinh doanh). Mỗi công ty tự khai, không ảnh hưởng công ty khác.” (tab Quản trị hàng hoá).', '- Tab có lỗi sau khi Lưu hiện chấm đỏ.']),
    ('Bước con', 'Button', 'Enable', '–', '–', 'Thông tin chung',
     ['- Thông tin chung · Thông số kỹ thuật · Mua hàng · Phân loại xe (có điều kiện) · Nhóm máy.',
      '- Bước có lỗi hiện chấm đỏ.']),
    # Thong tin hang hoa
    ('Tên hàng hoá', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', [
        '- Placeholder “Nhập tên hàng hoá”.',
        '- Kiểm ngay trên form: trống → “Bắt buộc phải nhập”; quá dài → “Vui lòng nhập tối đa 255 ký tự.”.',
        '- Kiểm trùng bộ 4 trường (BR-05).']),
    ('Model', 'Dropdown', 'Enable', 'Tìm trên máy chủ', 'Có', 'Trống', [
        '- Gõ để tìm model đang hoạt động (tối đa 50 kết quả).',
        '- Dùng để sinh Mã hàng khi không có Code đặt hàng.',
        '- Trống → “Bắt buộc phải nhập”.']),
    ('Nút “+” cạnh Model', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu Q3', [
        '- Tooltip “Thêm model mới”.',
        '- Mở popup Tạo mới model; tạo xong tự chọn model vừa tạo, toast “Thêm mới thành công.”.']),
    ('Công ty quản lý', 'Textbox', 'Disable', '–', '–', 'Công ty đang làm việc', 'Không sửa được.'),
    ('Tên thường gọi / Tên tiếng Anh / Barcode', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Barcode không kiểm trùng.'),
    ('Ghi chú', 'Textarea', 'Enable', 'Không giới hạn', 'Không', 'Trống', '–'),
    # Phan loai
    ('Loại sản phẩm', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống', [
        '- Loại đang hoạt động, sắp theo cây Tính chất › Nhóm chức năng › Nhóm sản phẩm › Loại.',
        '- Chọn → tự điền Tính chất, Nhóm chức năng, Nhóm sản phẩm.',
        '- Chọn → nếu ô % VAT đang trống và loại có khai VAT thì tự điền % VAT (không đè giá trị đã chọn).',
        '- Chọn → nạp lại bảng Thuộc tính theo loại; bật / tắt bước Phân loại xe.',
        '- Đổi sang loại không phải phụ tùng ô tô khi đã nhập dữ liệu xe → hỏi “Dữ liệu Phân loại xe sẽ bị xoá khi Lưu. '
        'Tiếp tục đổi Loại sản phẩm?” (Đổi / Giữ nguyên).']),
    ('Đặc tính', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Đặc tính đang hoạt động.'),
    ('Tính chất / Nhóm chức năng / Nhóm sản phẩm', 'Textbox', 'Disable', '–', '–', 'Trống', 'Tự điền theo Loại sản phẩm.'),
    # Nguon goc
    ('Thương hiệu', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống', 'Thuộc bộ kiểm trùng (BR-05).'),
    ('Xuất xứ', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống', '–'),
    ('Hãng sản xuất', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
     ['- Phần đầu của Mã hàng (BR-04).', '- Thuộc bộ kiểm trùng (BR-05).']),
    ('Code đặt hàng', 'Dropdown', 'Enable', 'Tìm trên máy chủ', 'Không', 'Trống',
     'Có giá trị → Mã hàng dùng tên Code đặt hàng thay cho tên Model.'),
    # DVT
    ('Bảng Đơn vị tính', 'Table/Grid', 'Enable', '≥ 1 dòng', 'Có', '1 dòng cơ bản, hệ số 1', [
        '- Cột: STT, Đơn vị, Đơn vị cơ bản, Hệ số, Quy đổi, Xoá.',
        '- Phải có đúng 1 đơn vị cơ bản (hệ số luôn = 1).',
        '- Đơn vị phụ: hệ số > 0, khác 0 và 1, tối đa 9.999.999.999.',
        '- Không trùng đơn vị.',
        '- Quy đổi tự hiện: “Đơn vị cơ bản” hoặc “1 <Đơn vị> = <Hệ số> <Đơn vị cơ bản>”.',
        '- Mỗi đơn vị khai = 1 bộ giá rỗng tại công ty đang làm việc (BR-14).']),
    ('Nút Thêm đơn vị', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Thêm 1 dòng trống (bảng rỗng → dòng mới là cơ bản, hệ số 1; còn lại là phụ, hệ số trống).'),
    ('Radio Đơn vị cơ bản', 'Checkbox', 'Enable', '1 dòng', '–', 'Dòng 1',
     'Chọn dòng khác làm cơ bản → dòng đó hệ số 1; dòng cơ bản cũ thành phụ, hệ số bị xoá trống để nhập lại.'),
    # Tai lieu
    ('Tài liệu kỹ thuật', 'Table/Grid', 'Enable', '–', 'Không', 'Rỗng', [
        '- Nút Thêm tài liệu; mỗi dòng: Loại tài liệu, Tệp (nhiều tệp), Xoá.',
        '- Đã thêm dòng thì Loại tài liệu bắt buộc (“Bắt buộc phải nhập”).',
        '- Rỗng: “Chưa có tài liệu kỹ thuật nào.”.']),
    ('Hình ảnh', 'File', 'Enable', '≤ 10 ảnh, ≤ 5 MB/ảnh', 'Không', 'Rỗng', [
        '- Nhãn “Hình ảnh (tối đa 10 ảnh, ảnh đầu là ảnh đại diện)”; nút Chọn ảnh, chọn xong tải lên ngay.',
        '- Định dạng jpeg, jpg, png, gif, webp.',
        '- Vượt 10: “Tối đa 10 ảnh (đang có n, chọn thêm m).”; lỗi tải: “Tải ảnh thất bại, vui lòng thử lại.”.',
        '- Nút ★ “Đặt làm ảnh đại diện”, nút Xóa từng ảnh.']),
    ('Video', 'Textbox', 'Enable', 'URL ≤ 1000 ký tự', 'Không', 'Rỗng',
     ['- Nút Thêm video; mỗi dòng 1 đường dẫn.', '- Dòng để trống → “Bắt buộc phải nhập”; sai URL → “Không hợp lệ”.']),
    # Thong so
    ('Thuộc tính theo loại sản phẩm', 'Table/Grid', 'Enable', '–', 'Có với dòng đã tick', 'Theo Loại sản phẩm', [
        '- Cột: Thuộc tính, Giá trị, Đơn vị, Bắt buộc (tick), In tem.',
        '- Cột Bắt buộc — Icon ⓘ: “Chỉ dòng được tick mới lưu và phải nhập giá trị”.',
        '- Dòng đã tick mà trống Giá trị → “Thuộc tính đã tick phải nhập giá trị.”.',
        '- Chưa chọn Loại SP: “Chọn Loại sản phẩm ở bước Thông tin chung để hiện thuộc tính.”.']),
    ('Trọng lượng / Định mức công lắp đặt', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', '–'),
    ('Kích thước', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Phụ kiện tiêu chuẩn / Đặc điểm / Tính năng đặc biệt', 'Textarea', 'Enable', 'Không giới hạn', 'Không', 'Trống', 'Trình soạn thảo định dạng.'),
    ('4 bảng hàng kèm theo', 'Table/Grid', 'Enable', '–', 'Không', 'Rỗng', [
        '- Công thức lắp ráp; Phụ kiện mua thêm; Vật tư lắp đặt; Vật tư sửa chữa – bảo dưỡng.',
        '- Nút Chọn hàng hoá mở popup tìm hàng; dòng mới Số lượng = 1, ĐVT = đơn vị cơ bản.',
        '- Số lượng > 0 (“Phải lớn hơn 0.”).',
        '- Không chọn chính hàng đang khai; không chọn thêm hàng đã xóa, hàng tạm, hàng Ngừng kinh doanh.']),
    # Mua hang
    ('Tên khai báo hải quan / HS Code', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Số lượng tối thiểu nhập mua', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', '–'),
    ('% VAT', 'Dropdown', 'Enable', 'Danh sách thuế suất', 'Có', 'Trống / theo Loại SP',
     ['- Trống → “Bắt buộc phải nhập”.', '- Chỉ là thuộc tính của hàng; KHÔNG làm đổi số giá bán (BR-17).']),
    ('Thuế nhập khẩu (không CO / có CO), Thuế chống bán phá giá', 'Dropdown', 'Enable', 'Danh sách thuế suất', 'Không', 'Trống', '–'),
    ('Hệ số tính thuế BVMT', 'Number', 'Enable', '1 – 999,999', 'Không', 'Trống',
     ['- Icon ⓘ: “Để trống nếu hàng không chịu thuế bảo vệ môi trường.”.',
      '- Nhỏ hơn 1 → “Không được nhỏ hơn 1.”; lớn hơn 999,999 → “Không được lớn hơn 999.999.”.']),
    # Xe, may
    ('Bước Phân loại xe', 'Dropdown', 'Enable / Ẩn', 'Chọn nhiều', 'Không', 'Ẩn', [
        '- Chỉ hiện khi Loại sản phẩm thuộc Tính chất phụ tùng ô tô.',
        '- Hãng xe → Loại xe → Model xe (lọc dây chuyền); bảng Đời xe theo model; tick “Áp dụng tất cả đời xe cho model”.']),
    ('Bước Nhóm máy', 'Dropdown', 'Enable', 'Chọn nhiều', 'Không', 'Trống',
     'Đã chọn Nhóm máy thì phải chọn Máy (“Đã chọn nhóm máy thì phải chọn máy.”).'),
    # Quan tri
    ('Nhà cung cấp', 'Dropdown', 'Enable', 'Chọn nhiều, tìm trên máy chủ', 'Không', 'Trống',
     '“Tìm và thêm nhà cung cấp”; mỗi nhà cung cấp là 1 chip “Mã - Tên”, có nút gỡ.'),
    ('Chính sách kinh doanh', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '–'),
    ('Số lượng tồn kho tối thiểu', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', '–'),
    ('Bảo hành', 'Number', 'Enable', 'Số nguyên 0–1000', 'Không', 'Trống',
     'Số lẻ → “Phải là số nguyên”; > 1000 → “Không được lớn hơn 1000.”.'),
    ('Đơn vị bảo hành', 'Dropdown', 'Enable', 'Ngày / Tháng / Năm', 'Không', 'Tháng', '–'),
    ('Hệ số công nghệ', 'Number', 'Enable', '0 – 1000', 'Không', '1', [
        '- Icon ⓘ: “Dùng chung mọi công ty, chỉ công ty tạo sửa.”.',
        '- Là hệ số hưởng của kỹ thuật khi lắp đặt, KHÔNG phải hệ số giá; không làm đổi giá bán.']),
    ('Catalog kinh doanh', 'Table/Grid', 'Enable', '≥ 1 Tiểu mục', 'Có', 'Rỗng', [
        '- 4 cột tick dây chuyền: Lĩnh vực › Chương › Mục › Tiểu mục (mỗi cột có ô Tìm...). Chỉ Tiểu mục được lưu.',
        '- Nhánh đang khoá có biểu tượng ổ khoá, không tick thêm được.',
        '- Trống → “Phải xếp hàng hoá vào ít nhất 1 Tiểu mục catalog kinh doanh.”.']),
    # Footer
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu hàng (BR-03, BR-04, BR-14). Đang lưu thì bấm lại không có tác dụng.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn đã mở vào (mặc định Hàng hoá nhập thông tin); có thay đổi chưa lưu thì hỏi xác nhận.'),
    ('Không có ô giá', 'Label', 'Hiển thị', '–', '–', '–', 'Form không có ô Giá bán, Giá vốn hay tab Giá.'),
], required=True)
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Loại sản phẩm', 'Change',
     'After:\n– Tự điền Tính chất, Nhóm chức năng, Nhóm sản phẩm.\n– % VAT đang trống → điền theo loại.\n'
     '– Nạp lại bảng Thuộc tính; bật / tắt bước Phân loại xe.\n'
     '– Đổi sang loại không phải phụ tùng khi đã có dữ liệu xe → hỏi “Đổi” / “Giữ nguyên”.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Xây dựng thông tin hàng hoá tại công ty đang làm việc; không có → “Bạn không có quyền '
     'xây dựng thông tin hàng hoá ở công ty đang làm việc.” và dừng.\n'
     '– Tên hàng hoá trống → báo đỏ dưới ô, toast “Vui lòng kiểm tra lại dữ liệu nhập”, không gửi.\n'
     'During:\n– Model / Loại sản phẩm / Thương hiệu / Xuất xứ / Hãng sản xuất / % VAT trống → “Bắt buộc phải nhập”.\n'
     '– Không có đơn vị tính → “Phải khai ít nhất 1 đơn vị tính.”; không đúng 1 cơ bản → “Phải có đúng 1 đơn vị cơ bản.”; '
     'trùng → “Đơn vị tính bị trùng.”; cơ bản hệ số khác 1 → “Đơn vị cơ bản có hệ số quy đổi bằng 1.”; '
     'phụ hệ số 0 hoặc 1 → “Hệ số quy đổi của đơn vị phụ phải khác 0 và 1.”.\n'
     '– Chưa có Tiểu mục → “Phải xếp hàng hoá vào ít nhất 1 Tiểu mục catalog kinh doanh.”.\n'
     '– Trùng Tên × Model × Thương hiệu × Hãng SX → “Đã có hàng hoá cùng Tên, Model, Thương hiệu và Hãng sản xuất.”.\n'
     '– Không sinh được mã → “Không sinh được mã hàng hoá: …” tại ô Hãng sản xuất.\n'
     '– Có lỗi → báo đồng thời mọi ô, chấm đỏ tab / bước, mở tab lỗi đầu tiên; không thực hiện After.\n'
     'After:\n– Sinh Mã hàng; lưu hàng; công ty quản lý = công ty đang làm việc; trạng thái Đang nhập thông tin.\n'
     '– Sinh bộ giá rỗng (6 giá bán + 1 giá vốn = 0) cho từng đơn vị tính tại công ty đang làm việc.\n'
     '– Toast “Đã lưu hàng hoá <Mã hàng>”; chuyển sang màn Chi tiết hàng hoá.'),
    ('Bấm Quay lại / rời trang khi chưa lưu', 'Click',
     'Before:\n– Có thay đổi → hỏi “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại).\n'
     'After:\n– Thoát → về màn đã mở vào, không lưu.'),
    ('Chọn ảnh', 'Change', 'During:\n– Kiểm tối đa 10 ảnh, ≤ 5 MB, đúng định dạng.\nAfter:\n– Tải lên ngay; ảnh đầu là ảnh đại diện.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Chỉnh sửa hàng hoá')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chỉnh sửa hàng hoá', 'crud', actor=ACTOR,
            caption='Biểu đồ Use Case — FR-06 Chỉnh sửa hàng hoá')
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của hàng hoá.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa hàng hoá',
    mota='Sửa thông tin một mã hàng. Có 2 phạm vi: công ty tạo hàng sửa toàn bộ (giống form Tạo mới); công ty đã '
         'lấy hàng về chỉ khai tab Quản trị hàng hoá. Lưu KHÔNG đổi trạng thái và KHÔNG đụng giá; riêng đơn vị '
         'tính mới thêm được sinh bộ giá rỗng.',
    tacnhan=ACTOR,
    dieukien='Có quyền Xây dựng thông tin hàng hoá tại công ty đang làm việc; hàng chưa bị xóa; công ty đang làm '
             'việc là công ty tạo hoặc đã lấy hàng về; hàng KHÔNG ở trạng thái Ngừng kinh doanh tại công ty này.',
    chinh='1. Bấm bút chì Sửa ở danh sách (hoặc nút Sửa ở màn chi tiết).\n'
          '2. Hệ thống xác định phạm vi sửa và mở form có sẵn dữ liệu.\n'
          '3. Người dùng sửa và bấm Lưu.\n'
          '4. Hệ thống kiểm tra, lưu, giữ nguyên trạng thái.\n'
          '5. Toast “Đã lưu hàng hoá <Mã hàng>”, chuyển sang màn Chi tiết hàng hoá.',
    phu='• Công ty lấy về → dải xám “Hàng hoá do <công ty tạo> tạo — chỉ khai được tab Quản trị hàng hoá.”, form '
        'mở thẳng tab Quản trị, tab Thông tin chỉ đọc, Hệ số công nghệ bị khoá.\n'
        '• Hàng đang Ngừng kinh doanh → toast “Hàng hoá đang ngừng kinh doanh, vui lòng mở khoá trước khi cập nhật.” '
        'và chuyển sang màn chi tiết (có nút Mở khóa).\n'
        '• Hàng đã bị xóa / không có quyền / công ty chưa dùng hàng → chuyển trang 404.\n'
        '• Đơn vị tính đã lưu: không sửa, không xoá được; chỉ thêm đơn vị phụ mới.\n'
        '• Lỗi kiểm tra → như Tạo mới.',
    dacbiet='Hàng Chờ tính giá bán / Đang tính giá / Đang kinh doanh vẫn sửa được toàn bộ; sửa xong trạng thái và '
            'giá giữ nguyên. Mã hàng không đổi dù đổi Hãng sản xuất / Code đặt hàng / Model.')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('20-sua.png'), shot_caption='Sửa hàng hoá — công ty tạo hàng (sửa toàn bộ)')
d.layout(menu=MENU + ' => Sửa', shot=shot('21-sua-muc-quan-tri.png'),
         shot_caption='Sửa hàng hoá — công ty lấy về (chỉ khai tab Quản trị hàng hoá)')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.p('Các trường giống form Tạo mới (mục 2.5.4). Bảng dưới chỉ ghi phần KHÁC khi sửa.')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Sửa hàng hoá: <Mã hàng>', 'Chưa tải xong: “Sửa hàng hoá”.'),
    ('Dải báo phạm vi', 'Label', 'Hiển thị / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện với công ty lấy về: “Hàng hoá do <tên công ty tạo> tạo — chỉ khai được tab Quản trị hàng hoá.” (chữ xám).'),
    ('Tab Thông tin hàng hoá (công ty lấy về)', 'Text', 'Read-only', '–', '–', 'Mờ, chỉ đọc',
     'Bấm được để XEM như màn chi tiết; không ô nào nhập được.'),
    ('Công ty quản lý', 'Textbox', 'Disable', '–', '–', 'Công ty tạo hàng', 'Không đổi được.'),
    ('Dòng đơn vị tính đã lưu', 'Table/Grid', 'Disable', '–', '–', 'Theo dữ liệu', [
        '- Nền xám, mọi ô khoá, icon ổ khoá; tooltip “Đơn vị tính đã lưu không sửa/xoá được”.',
        '- Dưới bảng: “Đơn vị đã lưu bị khoá” + icon ⓘ “Đơn vị tính đã lưu không sửa/xoá được; chỉ thêm được đơn vị phụ mới.”.',
        '- Radio Đơn vị cơ bản bị khoá khi đã có đơn vị cơ bản đã lưu.']),
    ('Dòng đơn vị tính mới thêm', 'Table/Grid', 'Enable', 'Hệ số > 0, ≠ 0 và 1', 'Có', 'Trống',
     ['- Chỉ thêm được đơn vị PHỤ.', '- Lưu xong: đơn vị mới có bộ giá rỗng ở mọi công ty đang dùng hàng (BR-15).']),
    ('Hệ số công nghệ', 'Number', 'Enable / Disable', '0 – 1000', 'Không', 'Giá trị hiện có',
     'Công ty lấy về: bị khoá (dùng chung, chỉ công ty tạo sửa).'),
    ('Tab Quản trị hàng hoá', 'Table/Grid', 'Enable', '–', '–', 'Dữ liệu của công ty đang làm việc',
     'Công ty lấy về mới lấy hàng: các ô quản trị trống, tự khai riêng; không ảnh hưởng công ty khác.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Công ty tạo: lưu toàn bộ. Công ty lấy về: chỉ lưu Nhà cung cấp, Chính sách kinh doanh, Tồn kho tối thiểu, Bảo hành, '
     'Đơn vị bảo hành, Catalog.'),
], required=True)
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System',
     'Before:\n– Không có quyền tại công ty đang làm việc → trang 404.\n'
     'During:\n– Hàng đã bị xóa ở ERP → “Hàng hoá đã bị xoá ở ERP, không sửa được.” → trang 404.\n'
     '– Công ty chưa lấy hàng về → “Công ty chưa lấy hàng hoá này về, không khai được dữ liệu quản trị.” → trang 404.\n'
     '– Hàng Ngừng kinh doanh tại công ty → toast “Hàng hoá đang ngừng kinh doanh, vui lòng mở khoá trước khi cập nhật.” '
     '→ chuyển màn chi tiết.\n'
     'After:\n– Xác định phạm vi: công ty tạo = sửa toàn bộ; công ty lấy về = chỉ tab Quản trị.'),
    ('Bấm Lưu (công ty tạo)', 'Click',
     'Before:\n– Kiểm quyền; kiểm công ty đang làm việc là công ty tạo (khác → “Chỉ công ty tạo hàng hoá mới được sửa hàng hoá này.”).\n'
     '– Kiểm hàng chưa bị khoá tại công ty (đang khoá → câu Ngừng kinh doanh ở trên).\n'
     'During:\n– Các kiểm tra như Tạo mới.\n– Đơn vị đã lưu bị đổi đơn vị / cơ bản / hệ số → “Đơn vị tính đã lưu không được sửa.”.\n'
     '– Kiểm trùng Tên × Model × Thương hiệu × Hãng SX chỉ khi 1 trong 4 ô thay đổi.\n'
     'After:\n– Lưu; KHÔNG đổi trạng thái; KHÔNG đổi Mã hàng; KHÔNG đổi giá.\n'
     '– Đơn vị phụ mới → sinh bộ giá rỗng cho mọi công ty đang dùng hàng.\n'
     '– Đổi sang Loại SP không phải phụ tùng → xoá dữ liệu Phân loại xe.\n'
     '– Toast “Đã lưu hàng hoá <Mã hàng>”, chuyển màn chi tiết.'),
    ('Bấm Lưu (công ty lấy về)', 'Click',
     'Before:\n– Chỉ gửi 6 ô quản trị; gửi thêm trường chung → “Chỉ công ty tạo hàng hoá mới được sửa thông tin chung.”.\n'
     'During:\n– Kiểm định dạng ô quản trị; Catalog ≥ 1 Tiểu mục.\nAfter:\n– Lưu dữ liệu quản trị của công ty đang làm việc; trạng thái giữ nguyên.'),
    ('Lỗi khác khi lưu', 'System', 'After:\n– Toast câu hệ thống trả về; mặc định “Lưu không thành công”.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Xóa hàng hoá')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa hàng hoá', 'action', actor=ACTOR, caption='Biểu đồ Use Case — FR-07 Xóa hàng hoá')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo / Quy tắc Xóa. Chỉ bổ sung các quy tắc riêng của hàng hoá.', anchor='delete')
d.intro_table(
    ten='Xóa hàng hoá',
    mota='Xóa một mã hàng đang ở trạng thái Đang nhập thông tin. Công ty tạo: xóa cứng mã hàng và mọi dữ liệu '
         '(kể cả giá mọi công ty). Công ty đã lấy về: gỡ phần của công ty mình (dữ liệu quản trị, nhà cung cấp, '
         'catalog, bộ giá), hàng vẫn còn ở công ty tạo.',
    tacnhan=ACTOR,
    dieukien='Có quyền Xây dựng thông tin hàng hoá tại công ty đang làm việc; hàng ở trạng thái Đang nhập thông tin '
             'tại công ty này; (công ty tạo) chưa có công ty nào khác lấy về.',
    chinh='1. Bấm thùng rác Xóa ở danh sách (hoặc nút Xóa ở màn chi tiết).\n'
          '2. Hệ thống hỏi xác nhận.\n3. Người dùng bấm Xóa.\n'
          '4. Hệ thống kiểm tra đầy đủ điều kiện và xóa / gỡ.\n'
          '5. Toast thành công; danh sách tải lại (từ màn chi tiết thì quay về màn đã mở vào).',
    phu='• Bấm Hủy → không làm gì.\n'
        '• Hàng đã từng phát sinh chứng từ (kể cả đã từng vào YCHG) → “Hàng hoá đã phát sinh chứng từ, không xoá được.”.\n'
        '• Có tồn kho, đang mượn, là phụ kiện / thành phần / máy dùng cho của hàng khác → báo đúng lý do.\n'
        '• Người khác đã xóa trước → “Dữ liệu đã thay đổi, vui lòng tải lại” và tải lại.\n'
        '• Hàng vừa bị khoá / đổi trạng thái → báo câu hệ thống trả và tải lại.',
    dacbiet='Hàng Chờ tính giá bán / Đang tính giá / Đang kinh doanh / Ngừng kinh doanh không xóa được (nút không hiện). '
            'Không có xóa hàng loạt. Tệp ảnh / tài liệu đã tải lên kho lưu trữ không bị xóa.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('05-xac-nhan-xoa.png'), shot_caption='Hộp thoại xác nhận xóa hàng hoá (công ty tạo)')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
    ('Nội dung (công ty tạo)', 'Text', 'Hiển thị', 'Theo dữ liệu',
     '“Xóa hàng hoá <Mã hàng>? Hàng hoá và toàn bộ dữ liệu đi kèm bị xóa hẳn, không khôi phục được.”'),
    ('Nội dung (công ty lấy về)', 'Text', 'Hiển thị', 'Theo dữ liệu',
     '“Gỡ hàng hoá <Mã hàng> khỏi <công ty đang làm việc>? Dữ liệu quản trị, nhà cung cấp và catalog của <công ty> bị xóa; '
     'hàng hoá vẫn còn ở công ty tạo.”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Nút đỏ. Thực hiện xóa / gỡ.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không gửi gì.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     ['- Xóa cứng: “Đã xóa hàng hoá <Mã hàng>”.', '- Gỡ: “Đã gỡ hàng hoá <Mã hàng> khỏi <công ty>”.',
      '- Lỗi: câu hệ thống trả; mặc định “Xóa hàng hoá không thành công”.']),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Không có quyền tại công ty đang làm việc → “Bạn không có quyền xây dựng thông tin hàng hoá ở công ty đang làm việc.”.\n'
     '– Hàng không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     '– Hàng đã bị xoá ở ERP → “Hàng hoá đã bị xoá ở ERP, không thao tác được.”; công ty chưa dùng → “Công ty chưa dùng hàng hoá này.”.\n'
     '– Đang Ngừng kinh doanh → “Hàng hoá đang ngừng kinh doanh, vui lòng mở khoá trước khi cập nhật.”.\n'
     '– Không phải Đang nhập thông tin → “Chỉ xoá được hàng hoá đang ở trạng thái Đang nhập thông tin.”.\n'
     'During (công ty tạo):\n– Đã có công ty khác lấy về → “Hàng hoá đã có công ty khác lấy về (<tên công ty>), không xoá được.”.\n'
     '– “Hàng có tồn kho!” · “Hàng đang mượn chưa trả hết!” · “Hàng nằm trong danh sách phụ kiện! (<mã>…)” · '
     '“Hàng nằm trong công thức ghép bộ! (<mã>…)” · “Hàng nằm trong danh sách phụ kiện lắp đặt của hàng hoá khác! (<mã>…)” · '
     '“Hàng nằm trong danh sách phụ kiện sửa chữa của hàng hoá khác! (<mã>…)” · “Hàng đang được khai là Máy dùng cho của hàng hoá khác! (<mã>…)”.\n'
     '– Đã có chứng từ (báo giá, hợp đồng, nhập / xuất kho, YCHG, PTG, BOM…) → “Hàng hoá đã phát sinh chứng từ, không xoá được.”.\n'
     '– Dừng ở lỗi đầu tiên, không xóa gì.\n'
     'After:\n– Công ty tạo: xóa mã hàng, đơn vị tính, giá + giá vốn + giá hiệu lực + yêu cầu duyệt giá của MỌI công ty, '
     'dữ liệu quản trị, catalog, tài liệu, ảnh.\n'
     '– Công ty lấy về: xóa trạng thái + dữ liệu quản trị + nhà cung cấp + catalog + bộ giá của CÔNG TY MÌNH; công ty tạo giữ nguyên; '
     'hàng về “Chưa sử dụng” tại công ty mình và lấy về lại được.\n– Toast thành công, tải lại.'),
    ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp thoại, không gửi yêu cầu.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 Khóa / Mở khóa hàng hoá')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Khóa / Mở khóa hàng hoá', 'action', actor=ACTOR,
            caption='Biểu đồ Use Case — FR-08 Khóa / Mở khóa hàng hoá')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa. Chỉ bổ sung các quy tắc riêng của hàng hoá.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa hàng hoá',
    mota='Khóa: chuyển hàng Đang kinh doanh sang Ngừng kinh doanh tại công ty đang làm việc. Mở khóa: trả về '
         'Đang kinh doanh. Chỉ đổi trạng thái của công ty đang làm việc, giữ nguyên bộ giá. Thao tác này không có '
         'trên màn Hàng hoá nhập thông tin (màn chỉ chứa hàng chưa kinh doanh) mà ở màn Xem chi tiết và các màn '
         'Hàng đang kinh doanh / Dữ liệu hàng hoá công ty.',
    tacnhan=ACTOR,
    dieukien='Có quyền Xây dựng thông tin hàng hoá tại công ty đang làm việc. Khóa: hàng Đang kinh doanh. '
             'Mở khóa: hàng Ngừng kinh doanh.',
    chinh='1. Mở chi tiết hàng (hoặc ở danh sách Hàng đang kinh doanh / Dữ liệu hàng hoá công ty).\n'
          '2. Bấm Khóa (hoặc Mở khóa).\n3. Xác nhận.\n4. Hệ thống đổi trạng thái.\n'
          '5. Toast thành công; màn chi tiết tải lại tại chỗ (badge + nút đổi).',
    phu='• Bấm Hủy → không làm gì.\n'
        '• Hàng đã bị khóa bởi người khác → “Hàng hoá đang ngừng kinh doanh.” và tải lại.\n'
        '• Hàng không còn Đang kinh doanh → “Chỉ khoá được hàng hoá đang ở trạng thái Đang kinh doanh.”.',
    dacbiet='Khóa theo CÔNG TY: công ty khác đang kinh doanh hàng này vẫn bán bình thường. Đang khóa thì không sửa, '
            'không xóa, không cập nhật giá; muốn sửa phải Mở khóa trước.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU_TRADING + ' => Xem chi tiết => Khóa', shot=shot('40-xac-nhan-khoa.png'),
         shot_caption='Hộp thoại xác nhận khóa hàng hoá')
d.layout(menu=MENU_TRADING + ' => Xem chi tiết => Mở khóa', shot=shot('41-xac-nhan-mo-khoa.png'),
         shot_caption='Hộp thoại xác nhận mở khóa hàng hoá')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận khóa / Xác nhận mở khóa', '–'),
    ('Nội dung Khóa', 'Text', 'Hiển thị', 'Theo dữ liệu',
     '“Khóa hàng hoá <Mã hàng> tại <công ty đang làm việc>? Hàng chuyển sang Ngừng kinh doanh, không sửa được tới khi mở khóa.”'),
    ('Nội dung Mở khóa', 'Text', 'Hiển thị', 'Theo dữ liệu',
     '“Mở khóa hàng hoá <Mã hàng> tại <công ty đang làm việc>? Hàng trở lại Đang kinh doanh.”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện thao tác.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng, không gửi gì.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn', [
        '- “Đã khóa hàng hoá <Mã hàng> — trạng thái Ngừng kinh doanh”.',
        '- “Đã mở khóa hàng hoá <Mã hàng> — trạng thái Đang kinh doanh”.',
        '- Lỗi: câu hệ thống trả; mặc định “Khóa hàng hoá không thành công” / “Mở khóa hàng hoá không thành công”.']),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Khóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm quyền tại công ty đang làm việc; hàng còn tồn tại, chưa bị xoá ở ERP, công ty đang dùng hàng.\n'
     'During:\n– Đang Ngừng kinh doanh → “Hàng hoá đang ngừng kinh doanh.”.\n'
     '– Không phải Đang kinh doanh → “Chỉ khoá được hàng hoá đang ở trạng thái Đang kinh doanh.”.\n'
     'After:\n– Trạng thái tại công ty đang làm việc = Ngừng kinh doanh; giá, giá vốn, giá hiệu lực giữ nguyên.\n'
     '– Hàng biến khỏi popup chọn hàng của chứng từ, màn Cập nhật giá bán, màn Hàng đang kinh doanh của công ty này.\n'
     '– Công ty khác không lấy về được nữa nếu người khóa là công ty tạo.\n– Toast, tải lại.'),
    ('Bấm Mở khóa trong hộp thoại', 'Click',
     'During:\n– Không phải Ngừng kinh doanh → “Hàng hoá không ở trạng thái Ngừng kinh doanh.”.\n'
     'After:\n– Trạng thái = Đang kinh doanh với ĐÚNG bộ giá trước khi khóa (không đặt lại giá).\n– Toast, tải lại.'),
])

# ------------------------------------------------------------------ 2.9
d.h3('2.9 Lập yêu cầu hỏi giá')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Lập yêu cầu hỏi giá', 'action', actor=ACTOR,
            caption='Biểu đồ Use Case — FR-09 Lập yêu cầu hỏi giá')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Màn Danh sách, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của hàng hoá.', anchor='notice')
d.intro_table(
    ten='Lập yêu cầu hỏi giá từ danh sách hàng hoá',
    mota='Lối vào luồng tính giá: tick các hàng Đang nhập thông tin rồi mở màn Tạo yêu cầu hỏi giá đã nạp sẵn hàng. '
         'Đặc tả form YCHG ở SRS riêng của luồng tính giá; mục này chỉ mô tả lối vào và tác động lên trạng thái hàng.',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Hàng hoá nhập thông tin.',
    chinh='1. Tick các hàng Đang nhập thông tin cần hỏi giá.\n'
          '2. Bấm Lập yêu cầu hỏi giá (trên thanh công cụ hoặc thanh chọn hàng loạt).\n'
          '3. Hệ thống mở màn “Tạo yêu cầu hỏi giá” với các hàng đã tick.\n'
          '4. Người dùng hoàn tất và GỬI yêu cầu → hàng sang Chờ tính giá bán (vẫn nằm ở màn Hàng hoá nhập thông tin).',
    phu='• Không tick dòng nào → mở form YCHG trống.\n'
        '• Hàng không đủ điều kiện bị loại khỏi phiếu, toast “Bỏ n hàng không lập yêu cầu hỏi giá được: <mã> (<lý do>); …” '
        '(lý do: Hàng hoá đã bị xoá / Hàng đang được hỏi giá ở <mã YCHG> / Hàng ngừng kinh doanh tại công ty / Hàng chưa dùng ở công ty).\n'
        '• Chỉ Lưu nháp YCHG → hàng vẫn Đang nhập thông tin.',
    dacbiet='Không cần quyền riêng. Dòng Chờ tính giá bán / Đang tính giá không tick được vì đã nằm trong một YCHG.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Lập yêu cầu hỏi giá', shot=shot('03-tick-lap-ychg.png'),
         shot_caption='Tick hàng và thanh chọn hàng loạt “Lập yêu cầu hỏi giá”')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tick dòng', 'Checkbox', 'Enable / Ẩn', 'Dòng Đang nhập thông tin', 'Không', 'Bỏ tick',
     'Chỉ dòng Đang nhập thông tin có ô tick.'),
    ('Thanh chọn hàng loạt', 'Label', 'Hiển thị / Ẩn', '–', '–', 'Ẩn', '“Đã chọn n hàng hoá” + nút Lập yêu cầu hỏi giá + nút Bỏ chọn.'),
    ('Nút Lập yêu cầu hỏi giá (thanh công cụ)', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Tooltip “Lập yêu cầu hỏi giá — tick hàng trước để nạp sẵn vào phiếu”.'),
    ('Nút Lập yêu cầu hỏi giá (thanh hàng loạt)', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Tooltip “Lập yêu cầu hỏi giá cho các hàng đã chọn”.'),
    ('Màn đích', 'Label', 'Hiển thị', '–', '–', 'Tạo yêu cầu hỏi giá', 'Nút Quay lại của màn đích trở về Hàng hoá nhập thông tin.'),
], required=True)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lập yêu cầu hỏi giá', 'Click',
     'During:\n– Mang danh sách hàng đã tick sang màn Tạo yêu cầu hỏi giá.\n– Màn đích kiểm từng hàng, loại hàng không đủ điều kiện + toast lý do.\n'
     'After:\n– Mở màn Tạo yêu cầu hỏi giá.'),
    ('Gửi YCHG (ở màn đích)', 'System',
     'After:\n– Hàng Đang nhập thông tin → Chờ tính giá bán; vẫn hiện ở màn này với badge cam, không tick được nữa.'),
])

# ------------------------------------------------------------------ 2.10
d.h3('2.10 Xuất Excel')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xuất Excel', 'io', actor=ACTOR, caption='Biểu đồ Use Case — FR-10 Xuất Excel')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Hàng hoá nhập thông tin.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách hàng hoá nhập thông tin',
    mota='Xuất ra file Excel đúng tập hàng đang lọc, với các trường người dùng chọn. File không có cột giá.',
    tacnhan=ACTOR,
    dieukien='Có quyền Xây dựng thông tin hàng hoá và Xuất excel danh sách hàng hoá tại công ty đang làm việc.',
    chinh='1. Bấm Xuất Excel.\n2. Popup Chọn trường xuất file mở, tick sẵn các cột đang hiện trên bảng.\n'
          '3. Chọn / sắp xếp trường, bấm Xuất file.\n'
          '4. Hệ thống tải dữ liệu theo từng phần (hiện tiến độ), dựng file và tải về.',
    phu='• Không có dữ liệu → “Không có dữ liệu để xuất”, không tạo file.\n'
        '• Không có quyền xuất ở công ty đang làm việc → “Bạn không có quyền xuất excel danh sách hàng hoá ở công ty đang làm việc”.\n'
        '• Lỗi → “Lỗi khi xuất Excel”.',
    dacbiet='Tên file: hang_hoa_nhap_thong_tin_<mã công ty>_<ddmmyyyy>.xlsx. Số trong file là số thật (có dấu phẩy ngăn nghìn).')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('07-xuat-excel.png'), shot_caption='Popup Chọn trường xuất file')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất file',
     'Dòng hướng dẫn: “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
    ('Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Danh sách trường', 'Checkbox', 'Enable', '21 trường', 'Có (≥ 1)', 'Tick sẵn cột đang hiện', [
        '- Mã hàng, Tên hàng hoá, Model, Tính chất hàng hoá, Nhóm chức năng, Nhóm sản phẩm, Loại sản phẩm, Thương hiệu, '
        'Hãng sản xuất, Trạng thái, Barcode, ĐVT, Xuất xứ, Code đặt hàng, Tên tiếng Anh, % VAT, Bảo hành, SL tồn kho tối thiểu, '
        'Công ty quản lý, Người nhập thông tin, Ngày cập nhật.',
        '- Không có Ảnh, không có trường giá.',
        '- Kéo để đổi vị trí cột trong file.']),
    ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '“Đang chọn x/21 trường”.'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Enable', 'Khoá khi chưa chọn trường nào hoặc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
    ('Dòng tiến độ', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     '“Đang chuẩn bị dữ liệu…” → “Đã tải x/y dòng…” → “Đang dựng file x/y dòng…”.'),
], required=True)
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm quyền Xuất excel danh sách hàng hoá tại công ty đang làm việc.\n'
     'During:\n– Lấy dữ liệu theo đúng bộ lọc + sắp xếp đang áp, từng phần 2.000 dòng.\n'
     'After:\n– File có tiêu đề “HÀNG HOÁ NHẬP THÔNG TIN”, cột STT, các cột đã chọn; toast “Xuất Excel thành công”.\n'
     '– 0 dòng → “Không có dữ liệu để xuất”.'),
])

# ========================================================= PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('chỉ ghi các quy tắc đặc thù của hàng hoá và các điểm chạm giá bán; quy tắc dùng chung không nhắc lại.',
           anchor='list', head='Quy tắc áp dụng', lead='Ngoài SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi màn Hàng hoá nhập thông tin',
     ['– Chỉ hiện hàng có trạng thái Đang nhập thông tin, Chờ tính giá bán hoặc Đang tính giá TẠI CÔNG TY ĐANG LÀM VIỆC.',
      '– Gồm cả hàng công ty mình tạo và hàng lấy về.',
      '– Hàng Đang kinh doanh / Ngừng kinh doanh / hàng tạm không hiện.'], ['Xem danh sách']),
    ('BR-02', 'Quyền xét theo công ty đang làm việc',
     ['– Mọi thao tác ghi cần quyền Xây dựng thông tin hàng hoá ĐƯỢC GÁN Ở CÔNG TY ĐANG LÀM VIỆC.',
      '– Có quyền ở công ty khác → bị từ chối “Bạn không có quyền xây dựng thông tin hàng hoá ở công ty đang làm việc.”.',
      '– Nút không dùng được thì ẩn hẳn; chặn thật ở máy chủ.'], ['Mọi chức năng ghi']),
    ('BR-03', 'Trạng thái khi tạo mới',
     ['– Hàng mới: công ty quản lý = công ty đang làm việc; trạng thái tại công ty này = Đang nhập thông tin.',
      '– Bấm Lưu (tạo hoặc sửa) KHÔNG làm đổi trạng thái; không có nút chuyển kinh doanh thủ công.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-04', 'Sinh Mã hàng',
     ['– Mã = <Mã Hãng sản xuất>-<Tên Code đặt hàng>; không có Code đặt hàng thì dùng <Tên Model>.',
      '– Bỏ dấu, bỏ khoảng trắng, viết hoa, chỉ giữ chữ, số, “_”, “-”; tối đa 32 ký tự.',
      '– Trùng → thêm hậu tố “:01” … “:99”; quá 99 → báo không sinh được mã.',
      '– Mã giữ nguyên mãi mãi, sửa Hãng / Code / Model không đổi mã.'], ['Tạo mới']),
    ('BR-05', 'Kiểm trùng hàng hoá',
     ['– Không được trùng đồng thời Tên × Model × Thương hiệu × Hãng sản xuất với hàng chưa bị xóa.',
      '– Khi sửa chỉ kiểm lại nếu 1 trong 4 trường đổi.', '– Barcode, tên tiếng Anh, tên thường gọi không kiểm trùng.'],
     ['Tạo mới', 'Chỉnh sửa']),
    ('BR-06', 'Kiểm tra bắt buộc báo một lượt',
     ['– Trên form chỉ kiểm Tên hàng hoá; các ô bắt buộc khác máy chủ kiểm và báo ĐỒNG THỜI mọi ô lỗi ở mọi tab.',
      '– Tab / bước có lỗi hiện chấm đỏ; mở tab lỗi đầu tiên và đưa con trỏ tới ô lỗi.',
      '– Không tự sửa giá trị người dùng nhập.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-07', 'Hai phạm vi sửa',
     ['– Công ty tạo hàng: sửa mọi tab.',
      '– Công ty đã lấy về: chỉ khai Nhà cung cấp, Chính sách kinh doanh, Tồn kho tối thiểu, Bảo hành, Đơn vị bảo hành, Catalog.',
      '– Hệ số công nghệ dùng chung, chỉ công ty tạo sửa.',
      '– Dữ liệu quản trị là riêng từng công ty, không ảnh hưởng nhau.'], ['Chỉnh sửa']),
    ('BR-08', 'Điều kiện sửa được',
     ['– Hàng chưa bị xóa; công ty đang làm việc là công ty tạo hoặc đã lấy về; không phải hàng tạm.',
      '– Hàng Ngừng kinh doanh tại công ty này: chặn mọi thao tác ghi, báo “Hàng hoá đang ngừng kinh doanh, vui lòng mở khoá trước khi cập nhật.”.',
      '– Chờ tính giá bán / Đang tính giá / Đang kinh doanh VẪN sửa được.'], ['Chỉnh sửa']),
    ('BR-09', 'Đơn vị tính bất biến sau khi lưu',
     ['– Đúng 1 đơn vị cơ bản, hệ số 1; đơn vị phụ hệ số > 0 và khác 0, 1; không trùng đơn vị.',
      '– Dòng đã lưu không sửa đơn vị / cơ bản / hệ số, không xoá được ở MỌI trạng thái (“Đơn vị tính đã lưu không được sửa.”).',
      '– Chỉ thêm được đơn vị phụ mới.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-10', 'Đổi Loại sản phẩm và dữ liệu xe',
     ['– Chọn Loại sản phẩm tự điền 3 cấp phân loại và % VAT (khi đang trống).',
      '– Đổi sang loại không phải phụ tùng ô tô: hỏi xác nhận; Lưu xong dữ liệu Phân loại xe bị xoá.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-11', 'Điều kiện xóa',
     ['– Chỉ xóa hàng Đang nhập thông tin tại công ty đang làm việc.',
      '– Công ty tạo: xóa cứng, chỉ khi chưa công ty nào lấy về và hàng chưa phát sinh tồn kho, mượn, liên kết phụ kiện / '
      'thành phần / máy dùng cho, chứng từ (kể cả từng vào YCHG).',
      '– Công ty lấy về: gỡ phần của công ty mình.', '– Không xóa hàng loạt; không xóa tệp trên kho lưu trữ.'], ['Xóa']),
    ('BR-12', 'Khóa / Mở khóa theo công ty',
     ['– Chỉ khóa hàng Đang kinh doanh; chỉ mở khóa hàng Ngừng kinh doanh.',
      '– Chỉ đổi trạng thái của công ty đang làm việc; công ty khác không bị ảnh hưởng.',
      '– Công ty tạo khóa hàng → công ty khác không lấy về được nữa.'], ['Khóa / Mở khóa']),
    ('BR-13', 'Vòng đời trạng thái theo công ty (luồng giá)',
     ['– Đang nhập thông tin → (gửi YCHG) Chờ tính giá bán → (lưu PTG) Đang tính giá → (mọi đơn vị tính được áp giá) Đang kinh doanh.',
      '– PTKD không duyệt YCHG, hoặc nhóm hàng bị huỷ / báo không có giá → về Đang nhập thông tin.',
      '– Xóa PTG → Đang tính giá về Chờ tính giá bán (nếu hàng không còn trong PTG dở nào khác của công ty).',
      '– Có dòng giá bị từ chối → hàng giữ Đang tính giá.',
      '– Hàng Đang kinh doanh đưa vào YCHG “hỏi lại giá” vẫn giữ Đang kinh doanh.'], ['Xem danh sách', 'Lập yêu cầu hỏi giá']),
    ('BR-14', 'GIÁ — Bộ giá rỗng khi tạo hàng',
     ['– Mỗi đơn vị tính khai lúc tạo được sinh 6 giá bán (Bán lẻ, Đại lý cấp 1, 2, 3, Theo lô, TMĐT) + 1 giá vốn, tất cả = 0, '
      'CHỈ cho công ty đang làm việc.',
      '– Giá đơn vị quy đổi lưu riêng, không tự tính từ đơn vị cơ bản × hệ số.',
      '– Form không cho nhập giá.'], ['Tạo mới']),
    ('BR-15', 'GIÁ — Thêm đơn vị tính khi sửa',
     ['– Đơn vị phụ mới được sinh bộ giá rỗng cho MỌI công ty đang dùng hàng (công ty tạo + các công ty đã lấy về).',
      '– Giá các đơn vị cũ giữ nguyên.',
      '– Lưu ý: hàng Đang kinh doanh thêm đơn vị mới thì đơn vị mới có giá 0 cho tới khi cập nhật giá.'], ['Chỉnh sửa']),
    ('BR-16', 'GIÁ — Sửa hàng không đụng giá',
     ['– Sửa thông tin chung / quản trị: không đổi trạng thái, không đổi bất kỳ giá, giá vốn, giá hiệu lực nào.',
      '– Hệ số công nghệ là hệ số lắp đặt, không phải hệ số giá.'], ['Chỉnh sửa']),
    ('BR-17', 'GIÁ — % VAT không đổi số giá',
     ['– % VAT là thuộc tính của hàng, chứng từ tự áp VAT theo dòng.',
      '– Đổi % VAT không làm đổi số giá bán đã lưu.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-18', 'GIÁ — Hàng chưa Đang kinh doanh không bán được',
     ['– Hàng Đang nhập thông tin / Chờ tính giá bán / Đang tính giá / Ngừng kinh doanh không xuất hiện ở popup chọn hàng của '
      'báo giá, BOM và chứng từ bán của công ty đó.',
      '– Không cập nhật giá được ở màn Cập nhật giá bán (mỗi trạng thái 1 câu báo riêng).'], ['Xem danh sách', 'Khóa / Mở khóa']),
    ('BR-19', 'GIÁ — Khóa / Mở khóa giữ nguyên giá',
     ['– Khóa không xóa, không đặt lại giá; mở khóa trả về Đang kinh doanh với đúng giá cũ.',
      '– Đang khóa: không cập nhật giá được.'], ['Khóa / Mở khóa']),
    ('BR-20', 'GIÁ — Xóa / gỡ xóa giá',
     ['– Xóa cứng: xóa giá, giá vốn, giá hiệu lực, yêu cầu duyệt giá của MỌI công ty.',
      '– Gỡ: chỉ xóa bộ giá của công ty mình; giá công ty tạo và công ty khác giữ nguyên.'], ['Xóa']),
    ('BR-21', 'GIÁ — Lấy về không chép giá',
     ['– Công ty lấy về bắt đầu ở Đang nhập thông tin với bộ giá rỗng (giá 0, giá vốn 0), KHÔNG chép giá của công ty tạo.',
      '– Muốn bán phải tự đi YCHG → yêu cầu tính giá → PTG cho công ty mình.'], ['Xem danh sách', 'Chỉnh sửa', 'Xóa']),
    ('BR-22', 'GIÁ — Giá riêng theo từng công ty',
     ['– Mỗi công ty có bộ giá riêng cho từng đơn vị tính; trạng thái cũng riêng.',
      '– Cùng một mã hàng có thể Đang kinh doanh ở công ty A và Đang nhập thông tin ở công ty B.'], ['Mọi chức năng']),
    ('BR-23', 'GIÁ — Không hiển thị giá trên màn hàng hoá',
     ['– Danh sách, form, màn chi tiết, file Excel không hiển thị giá bán lẫn giá vốn với bất kỳ ai (kể cả quyền Xem giá vốn hàng hoá).',
      '– Xem / sửa giá ở màn Cập nhật giá bán, Duyệt giá bán.'], ['Mọi chức năng']),
    ('BR-24', 'Dữ liệu cũ / thao tác đồng thời',
     ['– Hai người thao tác cùng lúc: người sau nhận “Dữ liệu đã thay đổi, vui lòng tải lại” (hàng đã bị xóa) hoặc câu báo '
      'trạng thái mới (đã bị khóa / đã đổi trạng thái) và màn tự tải lại.'], ['Xóa', 'Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-25', 'Không có lịch sử thay đổi hàng hoá',
     ['– Tạo / sửa / khóa / mở khóa / xóa hàng không ghi lịch sử; màn chi tiết chỉ có dòng Người tạo / Cập nhật.',
      '– Lịch sử chỉ có ở phần giá bán (màn Cập nhật giá bán / Duyệt giá bán).'], ['Mọi chức năng']),
])

d.save()
print('OK ->', OUT)
