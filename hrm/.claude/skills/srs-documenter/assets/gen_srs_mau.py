# -*- coding: utf-8 -*-
"""KHUNG MAU sinh SRS theo FORM CHUAN MOI (user chot 2026-08-17).

Ban mau doi chieu: .claude/skills/srs-documenter/assets/SRS_MAU.docx
(= "SRS - Danh muc khach hang", ban da duoc user chinh tay va chot lam chuan).

Cach dung: COPY file nay sang .plans/[feature]/gen_srs.py roi thay noi dung.
File nay co du 4 chuong + 2 chuc nang mau (1 chuc nang CHI DOC, 1 chuc nang
GHI DU LIEU) de thay ro khac biet giua 2 kieu bang giao dien.

Cau truc form moi — 4 chuong, KHONG hon:
    Phan 1. Gioi thieu            -> 1 Muc dich | 2 Thuat ngu va viet tat
    Phan 2. Phan quyen            -> 1 Danh sach quyen | 2 Ma tran phan quyen
    Phan 3. Dac ta chi tiet ...   -> 1 So do UML tong quan | 2 Dac ta tung chuc nang
    Phan 4. Quy tac nghiep vu     -> BR-01, BR-02, ...

DA BO so voi form cu: bang thong tin trang bia, muc "Pham vi", chuong "Tong quan",
muc "Quy tac truy cap bat buoc", chuong "Danh muc chuc nang (Function list)",
muc "Tieu chi nghiem thu", dong "Chuc nang lien quan: FR-xx".
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from srs_docx_lib import SrsDoc, ACTOR_P1, ACTOR_BOTH  # noqa: E402

# Thu muc anh chup that cua man hinh (Playwright MCP, 1440x900).
# Lam SRS + HDSD cho cung 1 man thi CHUP 1 LAN, dung chung thu muc nay.
SHOTS = r"d:\CompanyProject\hrm\hrm-claude-config\hrm\.plans\[feature]\[feature]_shots"

OUT = (r"d:\CompanyProject\hrm\hrm-claude-config\hrm\.plans\[feature]"
       r"\SRS - <Ten man hinh>.docx")


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(
    out=OUT,
    # menu/route van truyen de tra cuu trong script, nhung muc Layout cua form moi
    # CHI in ra dong "URL day du".
    menu='Phân hệ <X> → <Nhóm menu> → <Tên màn>',
    route='/duong-dan-man',
    full_url='https://<host-hrm>/duong-dan-man',
    img_prefix='mau_')

# ============================================================== TRANG DAU
# 2 dong can giua, KHONG dung Heading, KHONG co bang thong tin trang bia.
d.title_block('<Tên màn hình>')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình <Tên màn hình>, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền.',
    'Làm rõ <cơ chế phức tạp nhất của màn — vd phạm vi dữ liệu, lớp bảo vệ dữ liệu>.',
    'Làm rõ <quy tắc rẽ nhánh / ràng buộc dễ hiểu sai nhất>.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('<Thuật ngữ nghiệp vụ>', '<Giải thích bằng ngôn ngữ người dùng, không dùng từ code>'),
    ('<Trạng thái Khóa>', 'Đổi trạng thái sang “Khóa”. KHÔNG xóa dữ liệu.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Xem <đối tượng>', 'Mở màn <...>.'),
    ('Q2', 'Thêm <đối tượng>', 'Nút Tạo mới và chức năng Import Excel.'),
    ('Q3', 'Sửa <đối tượng>', 'Nút Sửa.'),
    ('Q4', 'Xóa <đối tượng>', 'Thao tác Khóa và Mở khóa.'),
    ('Q5', 'Xuất dữ liệu <đối tượng>', 'Các nút Xuất CSV / Excel / PDF.'),
], widths=[0.8, 2.0, 3.2])

# Chi them bang nay khi man co phan quyen theo CAP DU LIEU (cong ty/phong ban/bo phan).
d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả <đối tượng>', 'Toàn bộ <đối tượng> của hệ thống.'),
    ('V2', 'Xem tất cả <đối tượng> của công ty', 'Giới hạn theo công ty của người đăng nhập.'),
    ('V3', 'Xem tất cả <đối tượng> của phòng ban', 'Giới hạn theo phòng ban của người đăng nhập.'),
    ('V4', 'Xem tất cả <đối tượng> của bộ phận', 'Giới hạn theo bộ phận của người đăng nhập.'),
    ('—', '(không có cấp nào)', 'Chỉ <đối tượng> do chính mình tạo.'),
], widths=[0.8, 2.0, 3.2])

d.h2('2 Ma trận phân quyền')
# Dung dung 2 ky hieu ✅ / ❌; can chu thich thi viet trong ngoac ngay sau ✅.
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Không có quyền nào'], [
    ('FR-01 Truy cập & xem danh sách', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ bản ghi của mình)'),
    ('FR-02 Tạo mới <đối tượng>', '❌', '✅', '❌', '❌', '❌', '❌'),
], widths=[2.2, 0.5, 0.5, 0.5, 0.5, 0.5, 1.3])

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
# Ten UC PHAI la CUM DONG TU. So do tong quan the hien quan he «extend».
# Xem day du quy uoc o SKILL.md muc "Quy uoc dat ten va quan he use case".
d.overview_rel_figure(
    'Use Case Diagram – Quản lý <đối tượng>',
    '<Tên actor>',
    # (id, nhãn, nhóm màu, cột) — 'main' nối actor, 'side' là use case mở rộng
    [('fr01', 'FR-01  Xem danh sách <đối tượng>',  'view', 'main'),
     ('fr02', 'FR-02  Tạo mới <đối tượng>',        'crud', 'main'),
     ('fr03', 'FR-03  Tìm kiếm và lọc <đối tượng>', 'view', 'side'),
     ('fr04', 'FR-04  Xem chi tiết <đối tượng>',   'view', 'side')],
    # (nguồn, đích, kiểu) — nguồn là đầu mũi tên đi RA
    [('fr03', 'fr01', 'extend'),
     ('fr04', 'fr01', 'extend')],
    caption='Use Case Diagram – Quản lý <đối tượng>')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------- 2.1 chuc nang CHI DOC (khong co UC)
# Chuc nang khong co tuong tac rieng (xem danh sach, tim kiem, xem chi tiet, lich su)
# thi BO muc "Bieu do Usecase" va lui so thu tu cac muc con lai 1 bac.
d.h3('2.1 Xem danh sách <đối tượng>')

d.p('2.1.1 Giới thiệu')
d.intro_table(
    ten='Truy cập và xem danh sách <đối tượng>',
    mota='Hiển thị bảng <đối tượng> nằm trong phạm vi dữ liệu của người đăng nhập, '
         'kèm phân trang và ô thống kê tổng số bản ghi khớp bộ lọc.',
    tacnhan='<Vai trò nghiệp vụ>; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào menu <X> → <Nhóm menu> → <Tên màn>.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem của người dùng.\n'
          '3. Hệ thống trả về trang đầu tiên của danh sách và tổng số bản ghi.\n'
          '4. Bảng hiển thị dữ liệu, ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có bản ghi nào trong phạm vi → bảng hiện thông báo không có dữ liệu.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)          # chuc nang chi doc: BO HAN dong "Yeu cau dac biet"

d.p('2.1.2 Layout màn hình')
d.layout(shot=shot('01-danh-sach.png'),
         shot_caption='Màn <Tên màn hình> lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    # required=False -> 7 cot: Ten | Loai | Trang thai | Pham vi | Gia tri ban dau | Mo ta
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '<Tiêu đề>', 'Tiêu đề cố định phía trên bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Chỉ hiện khi có quyền Thêm <đối tượng>.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Luôn hiển thị, không tắt được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Hoạt động',
     'Hai trạng thái khác màu rõ ràng.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số bản ghi khớp bộ lọc, không phải tổng toàn hệ thống.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     'Có nút về đầu / lùi / số trang / tiến / về cuối và ô chọn số dòng mỗi trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện thông báo không có dữ liệu kèm hình minh họa khi N = 0.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Hiện trong lúc nạp dữ liệu.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định cấp quyền xem của người dùng theo thứ tự ưu tiên.\n'
     'During:\n– Áp phạm vi dữ liệu.\n'
     'After:\n– Trả về trang 1 và tổng số bản ghi; hiển thị bảng.'),
    ('Bấm số trang / nút tiến lùi', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
])

# ---------------------------------------- 2.2 chuc nang GHI DU LIEU (co UC)
d.h3('2.2 Tạo mới <đối tượng>')

d.p('2.2.1 Biểu đồ Usecase')
# So do RIENG cua tung chuc nang: KHONG ve include/extend (BA chot 24/08/2026).
# Cac rang buoc kieu "kiem tra quyen", "sinh ma tu dong" la hanh vi ngam cua he thong
# -> dua vao Phan 4 Quy tac nghiep vu, khong bien thanh use case.
d.uc_figure('FR-02', 'Tạo mới <đối tượng>', 'crud', relations=(),
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-02 Tạo mới <đối tượng>')

d.p('2.2.2 Giới thiệu')
d.intro_table(
    ten='Tạo mới <đối tượng>',
    mota='Thêm một <đối tượng> mới vào danh mục. Mã do hệ thống sinh tự động.',
    tacnhan='<Vai trò nghiệp vụ>',
    dieukien='Người dùng có quyền Thêm <đối tượng>.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở màn thêm mới.\n'
          '3. Người dùng nhập thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, sinh mã và ghi bản ghi mới.\n'
          '5. Hệ thống hiển thị thông báo thành công và quay về danh sách.',
    phu='• Thiếu trường bắt buộc → báo lỗi đỏ ngay dưới ô tương ứng, không đóng màn, '
        'giữ nguyên dữ liệu đã nhập.\n'
        '• Trùng <trường duy nhất> → báo lỗi tương ứng, không tạo bản ghi.\n'
        '• Thoát màn khi đã sửa mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='<Điều đặc biệt của màn này; để chuỗi rỗng nếu cần giữ dòng mà không có nội dung>')

d.p('2.2.3 Layout màn hình')
d.layout(route='/duong-dan-man/add',
         shot=shot('02-tao-moi.png'),
         shot_caption='Form Tạo mới <đối tượng>')

d.p('2.2.4 Mô tả chi tiết giao diện')
d.ui_table([
    # mac dinh 8 cot: Ten | Loai | Trang thai | Pham vi | Bat buoc | Gia tri ban dau | Mo ta
    ('<Tên>', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
     'Thiếu thì báo “Bắt buộc phải nhập”.'),
    ('<Loại>', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống', '–'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xử lý để tránh tạo trùng bản ghi.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi inline', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi.'),
])

d.p('2.2.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'Before:\n– Kiểm tra quyền Thêm <đối tượng>.\n'
     '– Nếu không có quyền → không hiển thị nút; gọi thẳng chức năng thì từ chối với thông báo '
     '“Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'After:\n– Mở màn thêm mới với các ô để trống.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Thêm <đối tượng>.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
     'và dừng xử lý.\n'
     'During:\n'
     '– <Trường> trống → hiển thị “<thông báo lỗi nguyên văn từ FormRequest>”.\n'
     '– <Trường> đã tồn tại → hiển thị “<... đã tồn tại>”.\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Sinh mã và ghi bản ghi mới với trạng thái Hoạt động.\n'
     '– Ghi một dòng lịch sử “Thêm mới”.\n'
     '– Hiển thị thông báo “Thêm mới <đối tượng> thành công” và quay về danh sách.'),
    ('Bấm Quay lại khi đã sửa mà chưa lưu', 'Click',
     'During:\n– Hiển thị hộp hỏi xác nhận rời khỏi trang.\n'
     'After:\n– Chọn ở lại thì giữ nguyên dữ liệu; chọn rời đi thì bỏ mọi thay đổi.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
# Moi rule: 1 dong tieu de "BR-0N — <Ten rule>" + cac gach dau dong.
# KHONG con dong "Chuc nang lien quan: FR-xx" o cuoi moi rule.
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.p('BR-01 — <Tên quy tắc>')
d.bullets([
    '<Phát biểu quy tắc bằng ngôn ngữ nghiệp vụ, truy vết được tới code>.',
    '<Trường hợp biên / ngoại lệ của quy tắc>.',
])

d.p('BR-02 — <Tên quy tắc>')
d.bullets([
    '<...>',
])

d.save()
