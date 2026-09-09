# -*- coding: utf-8 -*-
"""Sinh SRS man "Yeu cau kiem tra sua chua - bao hanh" (/customer-care/warranty-repair-requests).

Nguon doi chieu (doc truc tiep tu code 03/09/2026, nhanh gop_db):
  BE  Modules/CustomerCare/{Routes/api.php,
        Http/Controllers/V1/WarrantyRepairRequestController.php,
        Http/Requests/WarrantyRepairRequest/WarrantyRepairRequestRequest.php,
        Services/{WarrantyRepairRequestService, WarrantyRepairRequestPrintService,
                  WarrantyRepairRequestNotifier}.php,
        Entities/WarrantyRepairRequest/WarrantyRepairRequest.php,
        Support/WarrantyRepairPermission.php}
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (quyen 1507-1510)
  FE  hrm-client/pages/customer-care/warranty-repair-requests/
        {index.vue, create.vue, _id/index.vue, _id/edit.vue,
         components/WarrantyRepairRequestForm.vue,
         components/RejectRequestModal.vue, components/TransferDepartmentModal.vue}
  Anh chup that: .plans/gop-db/warranty-repair-request/wrr_shots/ (Playwright, 1440x900, 03/09/2026)

Chay:  python3 .plans/gop-db/warranty-repair-request/gen_srs.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))                       # .plans/gop-db (lop mac)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "srs-documenter", "assets"))
from _mac_docx import patch_srs  # noqa: E402

patch_srs()
from srs_docx_lib import SrsDoc, ACTOR_P1  # noqa: E402

SHOTS = os.path.join(HERE, "wrr_shots")
OUT = os.path.join(HERE, "SRS - Yêu cầu kiểm tra sửa chữa - bảo hành.docx")

MENU_CSKH = ('Phân hệ CSKH => Kiểm tra bảo hành sửa chữa '
             '=> Yêu cầu kiểm tra sửa chữa - bảo hành')
MENU_SALE = ('Phân hệ Bán hàng => Bán dịch vụ => Báo giá dịch vụ SC-BD-BT '
             '=> Yêu cầu sửa chữa - bảo hành')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(
    out=OUT,
    menu='Phân hệ CSKH → Kiểm tra bảo hành sửa chữa → Yêu cầu kiểm tra sửa chữa - bảo hành',
    route='/customer-care/warranty-repair-requests',
    full_url='/customer-care/warranty-repair-requests',   # lib giu de tham chieu
    img_prefix='wrr_')



# ================================================================= TRANG DAU
d.title_block('Yêu cầu kiểm tra sửa chữa – bảo hành')

d.h2('Mục lục')
d.toc()

# ============================================================ PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Yêu cầu kiểm tra sửa chữa – bảo hành, '
    'nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và phạm vi dữ liệu của màn hình.',
    'Làm rõ hai lối vào màn hình cho ra hai phạm vi dữ liệu khác nhau.',
    'Làm rõ quy tắc bắt buộc nhập khác nhau giữa Lưu nháp và Lưu và gửi.',
    'Làm rõ điều kiện hiện/ẩn của từng thao tác (Sửa, Xóa, Chuyển phòng tiếp nhận, Từ chối, '
    'Tạo phiếu xử lý yêu cầu).',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu yêu cầu', 'Một bản ghi trên màn hình này. Là chứng từ MỞ ĐẦU của luồng dịch vụ '
                      '(kiểm tra – sửa chữa – bảo hành).'),
    ('Phòng tiếp nhận xử lý', 'Phòng ban được giao xử lý phiếu. Chỉ người thuộc phòng này và có '
                              'quyền xử lý mới thao tác được với phiếu.'),
    ('Phiếu xử lý yêu cầu', 'Chứng từ tiếp theo của luồng, do phòng tiếp nhận lập từ phiếu yêu cầu.'),
    ('Lưu nháp', 'Lưu phiếu ở trạng thái Đang tạo, chưa gửi cho phòng tiếp nhận. Chỉ bắt buộc '
                 'nhập Khách hàng và tên thiết bị.'),
    ('Lưu và gửi', 'Lưu và chuyển phiếu sang trạng thái Chờ xử lý, gửi thông báo cho phòng tiếp '
                   'nhận. Bắt buộc nhập đầy đủ thông tin.'),
    ('Số BBBGNT / BBXNCV', 'Số biên bản bàn giao nghiệm thu hoặc biên bản xác nhận công việc, '
                           'ghi theo hồ sơ đã ký với khách hàng.'),
    ('Trang thiết bị hiện có của khách hàng', 'Danh mục thiết bị khách đang sở hữu, gồm thiết bị '
                                             'mua của Tân Phát và thiết bị mua của nhà cung cấp khác.'),
], widths=[1.9, 4.1])

# ============================================================ PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Xử lý yêu cầu sửa chữa',
     'Hiện 3 thao tác dành cho phòng tiếp nhận: Tạo phiếu xử lý yêu cầu, Chuyển phòng tiếp nhận, '
     'Từ chối. Ngoài ra được nhìn thấy mọi phiếu gửi về phòng mình.'),
], widths=[0.8, 2.2, 3.0])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty',
     'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo công ty',
     'Phiếu thuộc công ty của người đăng nhập, cộng phiếu do chính mình lập.'),
    ('V3', 'Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo phòng ban',
     'Phiếu thuộc các phòng mà người đăng nhập được phân quản lý, cộng phiếu do chính mình lập.'),
    ('—', '(không có quyền xem theo cấp nào)', 'Chỉ phiếu do chính mình lập.'),
], widths=[0.8, 2.4, 2.8])

d.p('Hai quy tắc áp cho MỌI cấp quyền ở trên:')
d.bullets([
    'Người có quyền Xử lý yêu cầu sửa chữa được nhìn thấy thêm mọi phiếu có phòng tiếp nhận xử lý '
    'là phòng của mình.',
    'Phiếu ở trạng thái Đang tạo của người khác không hiển thị với bất kỳ ai, kể cả người quản '
    'trị hệ thống. Phiếu nháp chỉ người lập nhìn thấy.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅ (trong phạm vi của mình)'),
    ('FR-03 Tùy chỉnh cột và cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Lập phiếu yêu cầu', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Sửa phiếu', '✅', '✅', '✅', '✅', '✅ (phiếu Đang tạo của mình)'),
    ('FR-06 Xem chi tiết phiếu', '✅', '✅', '✅', '✅', '✅ (trong phạm vi của mình)'),
    ('FR-07 Chuyển phòng tiếp nhận', '✅', '❌', '❌', '❌', '❌'),
    ('FR-08 Từ chối yêu cầu', '✅', '❌', '❌', '❌', '❌'),
    ('FR-09 Tạo phiếu xử lý yêu cầu', '✅', '❌', '❌', '❌', '❌'),
    ('FR-10 Xóa phiếu', '✅', '✅', '✅', '✅', '✅ (phiếu Đang tạo của mình)'),
    ('FR-11 In phiếu và in danh sách', '✅', '✅', '✅', '✅', '✅'),
    ('FR-12 Xuất Excel', '✅', '✅', '✅', '✅', '✅'),
    ('FR-13 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅'),
], widths=[2.4, 0.5, 0.5, 0.5, 0.5, 1.6])

d.p('Ghi chú: các ô ✅ ở nhóm Q1/V1–V3 chỉ nói về quyền, còn hiện hay ẩn nút vẫn phụ thuộc điều '
    'kiện nghiệp vụ nêu tại Phần 4 (trạng thái phiếu, người lập, phòng tiếp nhận).')

# ==================================================== PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
# Bam DUNG khuon SRS_MAU.docx (Phieu de nghi thu tien) — cung dang chung tu:
#   · man that (danh sach / lap / sua / chi tiet) = main, noi THANG toi actor
#   · thao tac tren MAN DANH SACH (loc, cau hinh cot, XOA, xuat Excel) = «extend» FR-01
#   · thao tac tren MAN CHI TIET (duyet/tu choi, in, lich su) = «extend» man chi tiet
# Truoc 05/09/2026 tung de Sua + Xoa «extend» cua "Lap phieu" — sai ca nghiep vu lan mau.
d.overview_figure2(
    [('Người lập phiếu', [0, 1, 2, 3]),
     ('Phòng tiếp nhận xử lý', [0, 3])],
    # mains: MÀN HÌNH thật — nối thẳng tới actor
    [('FR-01', 'Xem danh sách yêu cầu', 'view'),
     ('FR-04', 'Lập phiếu yêu cầu', 'crud'),
     ('FR-05', 'Sửa phiếu yêu cầu', 'crud'),
     ('FR-06', 'Xem chi tiết phiếu', 'view')],
    # subs: thao tác làm ngay trên màn đó — nối bằng «include» / «extend»
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cấu hình bộ lọc và cột', 'view', 'extend', [0], None),
     ('FR-10', 'Xóa phiếu yêu cầu', 'action', 'extend', [0], None),
     ('FR-12', 'Xuất danh sách ra Excel', 'io', 'extend', [0], None),
     ('FR-07', 'Chuyển phòng tiếp nhận', 'action', 'extend', [3], None),
     ('FR-08', 'Từ chối yêu cầu', 'action', 'extend', [3], None),
     ('FR-09', 'Tạo phiếu xử lý yêu cầu', 'action', 'extend', [3], None),
     ('FR-11', 'In phiếu / in danh sách', 'io', 'extend', [3], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Yêu cầu kiểm tra sửa chữa – bảo hành')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1 Xem danh sach
d.h3('2.1 Xem danh sách yêu cầu')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu kiểm tra sửa chữa – bảo hành tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách yêu cầu kiểm tra sửa chữa – bảo hành',
    mota='Hiển thị danh sách phiếu yêu cầu nằm trong phạm vi dữ liệu của người đăng nhập, kèm '
         'phân trang, sắp xếp và trạng thái của từng phiếu.',
    tacnhan='Người lập phiếu; Phòng tiếp nhận xử lý; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào màn hình theo một trong hai lối vào ở mục Layout.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo lối vào và cấp quyền xem của người dùng.\n'
          '3. Hệ thống trả về trang đầu tiên, mặc định 10 dòng, sắp xếp theo Ngày tạo giảm dần.\n'
          '4. Bảng hiển thị dữ liệu; dòng “Hiển thị a–b / N” cho biết khoảng đang xem và tổng số '
          'phiếu khớp bộ lọc.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện thông báo không có dữ liệu.\n'
        '• Phiếu Đang tạo của người khác luôn bị loại khỏi danh sách.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU_CSKH + '   (hiển thị: toàn bộ phiếu trong phạm vi quyền của người '
                          'đăng nhập)')
d.p('Menu: ' + MENU_SALE + '   (hiển thị: chỉ phiếu do chính người đăng nhập lập — phạm vi mặc định)')
d.figure(shot('01-danh-sach.png'), 'Màn Yêu cầu kiểm tra sửa chữa – bảo hành lúc mới truy cập', width_in=6.2)

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Yêu cầu kiểm tra sửa chữa – bảo hành',
     'Tiêu đề cố định trên thanh công cụ.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Luôn hiển thị, không tắt được, ghim trái khi cuộn ngang.'),
    ('Cột Số phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết. Sắp xếp được. Không tắt được.'),
    ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Hiển thị dạng “mã khách hàng - tên khách hàng”.'),
    ('Cột Tên thiết bị liên quan', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Hiện 2 dòng đầu, còn lại thu gọn sau liên kết “Xem thêm” / “Thu gọn”.'),
    ('Cột Địa chỉ sửa chữa', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Bật ở cửa sổ Tùy chỉnh cột.'),
    ('Cột Ngày gửi yêu cầu', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn mặc định',
     'Sắp xếp được. Được ghi khi phiếu chuyển sang Chờ xử lý.'),
    ('Cột Người xử lý / Ngày xử lý', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Do chứng từ tiếp theo ghi ngược về, không phải màn này nhập.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Ngày tạo sắp xếp được, mặc định giảm dần.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Trống nếu phiếu chưa từng được sửa.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 9 giá trị', 'Theo dữ liệu',
     'Chữ và màu do máy chủ quyết định, xem Phần 4 BR-02.'),
    ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện từng phiếu',
     'Hai thao tác đầu hiện thẳng, còn lại nằm trong menu “Hành động khác”. Thao tác không đủ '
     'điều kiện thì ẩn hẳn, không hiện dạng khóa mờ.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, 10 dòng',
     'Có nút về đầu, lùi, số trang, tiến, về cuối.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', 'Hiện khi không có phiếu nào.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Đọc tham số lối vào để xác định phạm vi (toàn phạm vi quyền hay chỉ phiếu của '
     'mình).\n– Xác định cấp quyền xem theo thứ tự tổng công ty → công ty → phòng ban.\n'
     'During:\n– Áp phạm vi dữ liệu; loại bỏ phiếu Đang tạo của người khác.\n'
     'After:\n– Trả về trang 1 và tổng số phiếu; hiển thị bảng.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'During:\n– Đổi chiều sắp xếp của cột đó, giữ nguyên bộ lọc.\n'
     'After:\n– Nạp lại danh sách từ trang 1.'),
    ('Bấm liên kết “Xem thêm” ở cột thiết bị', 'Click',
     'After:\n– Mở rộng ô hiển thị đủ danh sách thiết bị; liên kết đổi thành “Thu gọn”.'),
    ('Bấm số trang hoặc đổi số dòng mỗi trang', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\n'
     'After:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
])

# ------------------------------------------------------------ 2.2 Tim kiem & loc
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang. Chỉ bổ sung các tiêu chí tìm kiếm và lọc riêng của màn hình tại phần mô tả chi tiết.',
           anchor='search')
d.intro_table(
    ten='Tìm kiếm nhanh và lọc nâng cao',
    mota='Thu hẹp danh sách theo từ khóa hoặc theo các tiêu chí trạng thái, khách hàng, thiết bị, '
         'người yêu cầu, tỉnh/thành phố, khoảng ngày và đơn vị.',
    tacnhan='Người lập phiếu; Phòng tiếp nhận xử lý',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh hoặc mở khối Tìm kiếm nâng cao.\n'
          '2. Người dùng chọn các tiêu chí cần lọc.\n'
          '3. Người dùng bấm Tìm kiếm hoặc nhấn Enter.\n'
          '4. Hệ thống nạp lại danh sách từ trang 1 theo điều kiện lọc, trong phạm vi dữ liệu của '
          'người dùng.',
    phu='• Bấm Làm mới → xóa mọi điều kiện lọc nhưng giữ nguyên lối vào (phạm vi dữ liệu).\n'
        '• Không có kết quả → bảng hiện thông báo không có dữ liệu, tổng số bằng 0.\n'
        '• Điều kiện lọc được ghi nhớ trong 10 phút; sau đó trở lại mặc định.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành')
d.p('Menu: ' + 'Phân hệ Bán hàng => Bán dịch vụ => Báo giá dịch vụ SC-BD-BT => Yêu cầu sửa chữa - bảo hành')
d.figure(shot('02-bo-loc-nang-cao.png'), 'Khối Tìm kiếm nâng cao đang mở', width_in=6.2)

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Gợi ý “Tìm theo mã phiếu, tên khách hàng, người tạo”. Tìm đúng ba trường đó.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng mọi điều kiện đang chọn.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Xóa điều kiện lọc, giữ nguyên phạm vi dữ liệu của lối vào.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 9 giá trị', 'Không', 'Trống',
     'Gợi ý “Chọn trạng thái”.'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Gõ để tìm; danh sách nạp dần từ danh mục khách hàng.'),
    ('Tên thiết bị', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Lọc theo tên thiết bị trong phiếu. Chờ Enter hoặc nút Tìm kiếm.'),
    ('Người yêu cầu', 'Dropdown', 'Enable', 'Danh sách nhân sự', 'Không', 'Trống',
     'Lọc theo người lập phiếu.'),
    ('Tỉnh/TP', 'Dropdown', 'Enable', 'Danh sách tỉnh/thành phố', 'Không', 'Trống',
     'Lọc theo tỉnh/thành phố của khách hàng.'),
    ('Ngày yêu cầu từ / đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo ngày tạo phiếu, tính trọn ngày ở cả hai đầu.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Ẩn khi thiếu quyền',
     'Chỉ hiện với người có quyền xem theo cấp; có biểu tượng ổ khóa khi bị giới hạn.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Không', 'Ẩn khi thiếu quyền',
     'Như trên. Lọc theo đơn vị của người lập phiếu.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm hoặc nhấn Enter', 'Click / Keypress',
     'During:\n– Gom mọi điều kiện đang chọn.\n'
     'After:\n– Nạp lại danh sách từ trang 1 trong phạm vi dữ liệu của người dùng; cập nhật tổng '
     'số phiếu.'),
    ('Chọn giá trị ở ô dạng danh sách', 'Change',
     'After:\n– Danh sách tự tìm lại ngay, không cần bấm thêm nút.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Xóa toàn bộ điều kiện lọc, giữ nguyên lối vào; nạp lại danh sách.'),
])

# ------------------------------------------- 2.3 Tuy chinh cot & cai dat bo loc
d.h3('2.3 Tùy chỉnh cột hiển thị và cài đặt bộ lọc')

d.p('2.3.1 Giới thiệu')
d.rule_ref('- Cấu hình bộ lọc và Tùy chỉnh cột. Chỉ bổ sung danh sách cột và ô lọc riêng của màn hình tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Tùy chỉnh cột hiển thị và cài đặt bộ lọc',
    mota='Cho phép mỗi người tự chọn cột nào hiện trên bảng và ô lọc nào hiện ở khối tìm kiếm '
         'nâng cao, kèm thứ tự sắp xếp.',
    tacnhan='Người lập phiếu; Phòng tiếp nhận xử lý',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm biểu tượng Cấu hình cột hiển thị hoặc nút Cài đặt bộ lọc.\n'
          '2. Hệ thống mở cửa sổ tương ứng với lựa chọn hiện tại.\n'
          '3. Người dùng tích chọn hoặc bỏ chọn, kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu; hệ thống áp dụng ngay và ghi nhớ cho lần vào sau.',
    phu='• Bấm Khôi phục mặc định → trở lại cấu hình gốc của màn hình.\n'
        '• Cột STT, Số phiếu và Hành động luôn hiển thị, không bỏ chọn được.',
    dacbiet=None)

d.p('2.3.2 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Cài đặt bộ lọc / Tuỳ chỉnh cột', shot=shot('05-cau-hinh-cot.png'), shot_caption='Cửa sổ Tùy chỉnh cột')
d.figure(shot('03-cai-dat-bo-loc.png'), 'Cửa sổ Cài đặt bộ lọc', width_in=6.2)

d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách cột', 'Modal', 'Enable', 'Danh sách 14 cột', 'Không', 'Theo cấu hình đã lưu',
     'Mỗi dòng có ô tích chọn và tay nắm kéo thả đổi thứ tự.'),
    ('Cột bị khóa', 'Icon', 'Read-only', '–', 'Hiển thị',
     'Biểu tượng ổ khóa ở các cột bắt buộc hiển thị.'),
    ('Danh sách ô lọc', 'Modal', 'Enable', 'Danh sách 8 ô lọc', 'Không', 'Theo cấu hình đã lưu',
     'Đánh số thứ tự hiển thị trên khối tìm kiếm nâng cao.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng và ghi nhớ cấu hình.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Chỉ có ở cửa sổ Cài đặt bộ lọc.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
])

d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi nhận danh sách cột hoặc ô lọc đang tích chọn cùng thứ tự.\n'
     'After:\n– Áp dụng ngay cho bảng, ghi nhớ theo từng người và từng màn hình.'),
    ('Bấm Khôi phục mặc định', 'Click',
     'After:\n– Trả lựa chọn về cấu hình gốc của màn hình; vẫn phải bấm Lưu để áp dụng.'),
])

# ---------------------------------------------------------------- 2.4 Lap phieu
d.h3('2.4 Lập phiếu yêu cầu')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Lập phiếu yêu cầu', 'crud',
            [('include', 'Chọn khách hàng'),
             ('include', 'Chọn thiết bị từ danh mục của khách'),
             ('include', 'Sinh số phiếu tự động'),
             ('extend', 'Gửi thông báo cho phòng tiếp nhận khi Lưu và gửi')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-04 Lập phiếu yêu cầu')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các trường riêng của phiếu và quy tắc bắt buộc nhập theo từng nút bấm tại phần mô tả chi tiết.',
           anchor='create')
d.intro_table(
    ten='Lập phiếu yêu cầu kiểm tra sửa chữa – bảo hành',
    mota='Ghi nhận yêu cầu của khách hàng: khách nào, liên hệ ai, sửa ở đâu, những thiết bị nào '
         'cần kiểm tra và yêu cầu cụ thể cho từng thiết bị. Phiếu có thể lưu nháp để hoàn thiện '
         'sau, hoặc gửi ngay cho phòng tiếp nhận.',
    tacnhan='Người lập phiếu (nhân viên kinh doanh, nhân viên chăm sóc khách hàng)',
    dieukien='Người dùng đã đăng nhập. Chức năng không yêu cầu quyền riêng.',
    chinh='1. Người dùng bấm Tạo mới ở màn danh sách.\n'
          '2. Hệ thống mở màn lập phiếu với các ô để trống.\n'
          '3. Người dùng chọn khách hàng; hệ thống tự điền loại hình tổ chức và nạp danh sách '
          'người liên hệ, địa chỉ sửa chữa cùng danh mục thiết bị hiện có của khách.\n'
          '4. Người dùng chọn thiết bị từ bảng “Danh mục trang thiết bị hiện có của khách hàng” '
          'sang bảng thiết bị cần kiểm tra, rồi nhập serial, số biên bản, nội dung yêu cầu và '
          'đính kèm tệp nếu cần.\n'
          '5. Người dùng bấm Lưu nháp hoặc Lưu và gửi.\n'
          '6. Hệ thống kiểm tra dữ liệu, sinh số phiếu và ghi phiếu; hiển thị thông báo thành '
          'công rồi quay về danh sách.',
    phu='• Thiếu trường bắt buộc → báo lỗi đỏ ngay dưới ô tương ứng, không rời màn, giữ nguyên dữ '
        'liệu đã nhập.\n'
        '• Trùng serial giữa các dòng thiết bị → báo lỗi tại dòng bị trùng.\n'
        '• Gõ tay một serial đã có trong danh mục → yêu cầu chọn từ danh sách thay vì gõ.\n'
        '• Thoát màn khi đã nhập mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Bấm Lưu và gửi có bước xác nhận “Bạn đồng ý lưu và gửi?” trước khi thực hiện.')

d.p('2.4.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Tạo mới', shot=shot('06-tao-moi.png'), shot_caption='Màn Lập phiếu yêu cầu lúc mới mở')
d.figure(shot('07-chon-khach-hang.png'), 'Cửa sổ Chọn khách hàng', width_in=6.2)

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khách hàng', 'Textbox', 'Read-only', 'Danh sách khách hàng', 'Có', 'Trống',
     'Bấm vào ô để mở cửa sổ Chọn khách hàng (tìm theo tên/mã, mã số thuế, số điện thoại). '
     'Thiếu thì báo “Bắt buộc phải nhập”.'),
    ('Người liên hệ', 'Dropdown', 'Enable / Disable', 'Danh sách người liên hệ của khách',
     'Có khi Lưu và gửi', 'Trống',
     'Khóa cho tới khi chọn khách hàng. Khách hàng cá nhân thì tự điền tên và số điện thoại của '
     'chính khách.'),
    ('Số điện thoại liên hệ', 'Textbox', 'Disable', '–', 'Không', 'Tự động theo người liên hệ',
     'Không nhập tay được.'),
    ('Địa chỉ sửa chữa', 'Dropdown', 'Enable / Disable', 'Danh sách địa chỉ của khách',
     'Có khi Lưu và gửi', 'Trống', 'Khóa cho tới khi chọn khách hàng.'),
    ('Loại hình tổ chức', 'Textbox', 'Disable', '–', 'Không', 'Tự động theo khách hàng',
     'Chỉ để đọc.'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Có khi Lưu và gửi', 'Trống', '–'),
    ('Phòng tiếp nhận xử lý', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Có khi Lưu và gửi',
     'Trống', 'Quyết định phòng nào nhận thông báo và được xử lý phiếu.'),
    ('Bảng thiết bị – Tên thiết bị', 'Table/Grid', 'Read-only', '–', 'Có', 'Theo thiết bị đã chọn',
     'Lấy từ bảng danh mục thiết bị bên dưới, không gõ tay.'),
    ('Bảng thiết bị – Serial', 'Dropdown', 'Enable', 'Danh sách serial hoặc gõ tay',
     'Có khi Lưu và gửi', 'Trống',
     'Có nút chuyển giữa “Chọn serial” và “Nhập serial tạm” khi số lượng lớn hơn số serial đã khai.'),
    ('Bảng thiết bị – Số BBBGNT / BBXNCV', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Bảng thiết bị – Nội dung yêu cầu', 'Textarea', 'Enable', '0–1000 ký tự',
     'Có khi Lưu và gửi', 'Trống', 'Mô tả tình trạng hỏng hoặc việc cần làm.'),
    ('Bảng thiết bị – File đính kèm', 'Button', 'Enable', 'PDF, ảnh, Word, Excel; tối đa 20MB',
     'Không', 'Trống', 'Tải lên ngay khi chọn tệp; sai định dạng hoặc quá dung lượng thì báo lỗi.'),
    ('Bảng thiết bị – Xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Bỏ thiết bị khỏi phiếu.'),
    ('Danh mục thiết bị của khách – ô tìm', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo mã, model hoặc tên thiết bị.'),
    ('Danh mục thiết bị của khách – nút thêm', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Đưa thiết bị sang bảng thiết bị cần kiểm tra.'),
    ('Nút Thêm trang thiết bị của khách hàng', 'Button', 'Enable / Ẩn', '–', '–',
     'Ẩn khi chưa chọn khách hàng', 'Khai bổ sung thiết bị mà khách đang có nhưng chưa có trong '
     'danh mục.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu ở trạng thái Đang tạo. Chỉ bắt buộc Khách hàng và tên thiết bị.'),
    ('Nút Lưu và gửi', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Có bước xác nhận. Bắt buộc nhập đầy đủ.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi inline', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi, viền ô chuyển đỏ.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'After:\n– Mở màn lập phiếu với các ô để trống; số phiếu chưa sinh.'),
    ('Chọn khách hàng', 'Change',
     'During:\n– Nạp người liên hệ, địa chỉ sửa chữa và danh mục thiết bị hiện có của khách.\n'
     'After:\n– Tự điền loại hình tổ chức; mở khóa các ô đang bị khóa; xóa thiết bị đã chọn của '
     'khách hàng trước đó.'),
    ('Bấm Lưu nháp', 'Click',
     'During:\n– Khách hàng trống → hiển thị “Bắt buộc phải nhập”.\n'
     '– Có dòng thiết bị thiếu tên → hiển thị “Bắt buộc phải nhập”.\n'
     '– Nếu có lỗi thì không thực hiện bước After.\n'
     'After:\n– Sinh số phiếu, ghi phiếu ở trạng thái Đang tạo.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Hiển thị “Lưu thành công” và quay về danh sách.'),
    ('Bấm Lưu và gửi', 'Click',
     'Before:\n– Hiển thị hộp xác nhận “Bạn đồng ý lưu và gửi?”; chọn Hủy thì dừng.\n'
     'During:\n– Thiếu bất kỳ trường bắt buộc nào (Khách hàng, Người liên hệ, Địa chỉ sửa chữa, '
     'Ghi chú, Phòng tiếp nhận xử lý, Serial, Nội dung yêu cầu) → hiển thị “Bắt buộc phải nhập” '
     'tại đúng ô.\n'
     '– Phiếu không có thiết bị nào → hiển thị “Yêu cầu phải có ít nhất 1 thiết bị”.\n'
     '– Trùng serial giữa hai dòng → hiển thị “Bị trùng serial thiết bị”.\n'
     '– Serial gõ tay đã có trong danh mục → hiển thị “Serial đã có trong danh mục, vui lòng chọn '
     'từ danh sách”.\n'
     '– Nếu có lỗi thì không thực hiện bước After.\n'
     'After:\n– Sinh số phiếu, ghi phiếu ở trạng thái Chờ xử lý, ghi mốc ngày gửi yêu cầu.\n'
     '– Gửi thông báo cho toàn bộ nhân viên phòng tiếp nhận xử lý.\n'
     '– Ghi một dòng lịch sử; hiển thị “Gửi yêu cầu thành công” và quay về danh sách.'),
    ('Bấm Quay lại khi đã nhập mà chưa lưu', 'Click',
     'During:\n– Hiển thị hộp hỏi xác nhận rời khỏi trang.\n'
     'After:\n– Chọn ở lại thì giữ nguyên dữ liệu; chọn rời đi thì bỏ mọi thay đổi.'),
])

# ------------------------------------------------------------------- 2.5 Sua
d.h3('2.5 Sửa phiếu yêu cầu')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Sửa phiếu yêu cầu', 'crud',
            [('include', 'Kiểm tra phiếu đang ở trạng thái Đang tạo'),
             ('include', 'Kiểm tra người sửa là người lập phiếu')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-05 Sửa phiếu yêu cầu')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung điều kiện được phép sửa của màn hình tại phần mô tả chi tiết.',
           anchor='create')
d.intro_table(
    ten='Sửa phiếu yêu cầu',
    mota='Chỉnh sửa phiếu chưa gửi đi: đổi thông tin liên hệ, thêm bớt thiết bị, sửa nội dung yêu '
         'cầu, rồi lưu nháp tiếp hoặc gửi cho phòng tiếp nhận.',
    tacnhan='Người lập phiếu',
    dieukien='Phiếu đang ở trạng thái Đang tạo và do chính người đăng nhập lập.',
    chinh='1. Người dùng bấm Sửa ở dòng phiếu hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn sửa với dữ liệu hiện có.\n'
          '3. Người dùng chỉnh sửa và bấm Lưu nháp hoặc Lưu và gửi.\n'
          '4. Hệ thống kiểm tra dữ liệu, ghi lại phiếu và ghi lịch sử thay đổi.',
    phu='• Phiếu đã gửi đi hoặc không phải của mình → nút Sửa không hiển thị; vào thẳng bằng đường '
        'dẫn thì hệ thống chuyển về màn chi tiết và từ chối cập nhật.\n'
        '• Các nhánh lỗi nhập liệu giống mục 2.4.',
    dacbiet='Số phiếu và người lập không đổi được.')

d.p('2.5.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Chỉnh sửa', shot=shot('11-sua.png'), shot_caption='Màn Sửa phiếu yêu cầu với dữ liệu thật')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.p('Bố cục và danh sách trường giống mục 2.4.4, khác ở các điểm sau:')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Sửa yêu cầu kiểm tra sửa chữa – bảo hành: '
     '<số phiếu>', 'Có kèm số phiếu.'),
    ('Các ô thông tin khách hàng', 'Textbox / Dropdown', 'Enable', '–', 'Như mục 2.4',
     'Theo dữ liệu đã lưu', 'Đổi khách hàng thì phải chọn lại thiết bị.'),
    ('Bảng thiết bị', 'Table/Grid', 'Enable', '–', 'Như mục 2.4', 'Theo dữ liệu đã lưu',
     'Thêm, bớt, sửa từng dòng như khi lập mới.'),
    ('Nút Lưu nháp / Lưu và gửi', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Như mục 2.4.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Kiểm tra phiếu ở trạng thái Đang tạo và do chính mình lập.\n'
     '– Không thỏa mãn → nút không hiển thị; truy cập thẳng bằng đường dẫn thì chuyển về màn chi '
     'tiết.\n'
     'After:\n– Mở màn sửa với dữ liệu hiện có.'),
    ('Bấm Lưu nháp / Lưu và gửi ở màn sửa', 'Click',
     'Before:\n– Máy chủ kiểm tra lại điều kiện sửa; không thỏa mãn thì từ chối với thông báo '
     'phiếu đã gửi đi hoặc không thuộc quyền chỉnh sửa.\n'
     'During:\n– Kiểm tra dữ liệu như mục 2.4.\n'
     'After:\n– Ghi lại phiếu; ghi một dòng lịch sử “Thay đổi thông tin” liệt kê đúng những '
     'trường đã đổi (kể cả thiết bị thêm mới, bị xóa, bị sửa).'),
])

# --------------------------------------------------------------- 2.6 Chi tiet
d.h3('2.6 Xem chi tiết phiếu')

d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung bố cục các khối và điều kiện hiện / ẩn từng nút của màn hình tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu yêu cầu',
    mota='Xem toàn bộ thông tin phiếu ở chế độ chỉ đọc, kèm khối Lịch sử và các thao tác phù hợp '
         'với trạng thái phiếu.',
    tacnhan='Người lập phiếu; Phòng tiếp nhận xử lý',
    dieukien='Phiếu nằm trong phạm vi xem của người đăng nhập.',
    chinh='1. Người dùng bấm số phiếu ở danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống hiển thị thông tin khách hàng, danh sách thiết bị và khối Lịch sử.\n'
          '4. Thanh nút cuối trang hiển thị đúng các thao tác mà người dùng được phép làm.',
    phu='• Không có quyền xem phiếu hoặc phiếu không tồn tại → chuyển sang trang báo không tìm '
        'thấy.\n'
        '• Phiếu từng bị từ chối → hiện dòng “Lý do từ chối gần nhất”.',
    dacbiet=None)

d.p('2.6.2 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Xem chi tiết', shot=shot('08-chi-tiet.png'), shot_caption='Màn Chi tiết phiếu yêu cầu')

d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết yêu cầu kiểm tra sửa chữa – bảo hành: '
     '<số phiếu>', 'Kèm số phiếu.'),
    ('Dòng người yêu cầu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Ghi người lập và thời điểm lập, ở góc phải khối thông tin khách hàng.'),
    ('Các ô thông tin khách hàng', 'Textbox', 'Disable', '–', 'Theo dữ liệu', 'Chỉ đọc.'),
    ('Bảng thiết bị', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Không có cột thao tác; dòng không có tệp thì để trống.'),
    ('Dòng Lý do từ chối gần nhất', 'Label', 'Read-only', '–', 'Ẩn khi chưa từng bị từ chối',
     'Chữ xám dưới khối thông tin khách hàng.'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở; xem mục 2.11.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Điều kiện như mục 2.5.'),
    ('Nút Tạo phiếu xử lý yêu cầu', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
     'Điều kiện như mục 2.9.'),
    ('Nút Chuyển phòng tiếp nhận', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
     'Điều kiện như mục 2.7.'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Điều kiện như mục 2.8.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Điều kiện như mục 2.10.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Luôn hiển thị.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Trở về danh sách.'),
], required=False)

d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm số phiếu ở danh sách', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu: người lập luôn xem được; sau đó xét quyền tổng công '
     'ty, công ty, phòng ban và phòng tiếp nhận.\n'
     '– Không thỏa mãn → chuyển sang trang báo không tìm thấy, không hiện dữ liệu.\n'
     'After:\n– Hiển thị chi tiết phiếu và các nút phù hợp.'),
])

# ------------------------------------------------------- 2.7 Chuyen phong
d.h3('2.7 Chuyển phòng tiếp nhận')

d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Chuyển phòng tiếp nhận', 'action',
            [('include', 'Kiểm tra quyền Xử lý yêu cầu sửa chữa'),
             ('include', 'Kiểm tra phiếu đang Chờ xử lý của phòng mình'),
             ('extend', 'Gửi thông báo cho phòng tiếp nhận mới')],
            caption='Biểu đồ Use Case — FR-07 Chuyển phòng tiếp nhận')

d.p('2.7.2 Giới thiệu')
d.rule_ref('- Quy tắc thao tác trạng thái, Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung điều kiện chuyển phòng tiếp nhận của màn hình tại phần mô tả chi tiết.',
           anchor='notice')
d.intro_table(
    ten='Chuyển phòng tiếp nhận xử lý',
    mota='Chuyển phiếu sang phòng khác khi phiếu được gửi nhầm phòng hoặc phòng khác phù hợp hơn '
         'để xử lý.',
    tacnhan='Phòng tiếp nhận xử lý (người có quyền Xử lý yêu cầu sửa chữa)',
    dieukien='Phiếu ở trạng thái Chờ xử lý, phòng tiếp nhận hiện tại là phòng của người đăng '
             'nhập, phiếu chưa có phiếu xử lý, và người dùng có quyền Xử lý yêu cầu sửa chữa.',
    chinh='1. Người dùng bấm Chuyển phòng tiếp nhận ở dòng phiếu hoặc màn chi tiết.\n'
          '2. Hệ thống mở cửa sổ, hiển thị phòng tiếp nhận hiện tại.\n'
          '3. Người dùng chọn phòng tiếp nhận mới và bấm Xác nhận.\n'
          '4. Hệ thống đổi phòng tiếp nhận, làm mới mốc ngày gửi yêu cầu và gửi thông báo cho '
          'phòng mới.',
    phu='• Không chọn phòng → báo “Bắt buộc phải nhập”.\n'
        '• Chọn đúng phòng hiện tại → hệ thống báo trùng phòng tiếp nhận trước đó và không thực '
        'hiện.\n'
        '• Phiếu đã đổi trạng thái ở nơi khác → hệ thống từ chối và báo phiếu không ở trạng thái '
        'cho phép chuyển.',
    dacbiet='Thao tác này KHÔNG đổi trạng thái phiếu — phiếu vẫn là Chờ xử lý.')

d.p('2.7.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Chuyển phòng tiếp nhận', modal='Chuyển phòng tiếp nhận', shot=shot('17-chuyen-phong.png'), shot_caption='Cửa sổ Chuyển phòng tiếp nhận')

d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chuyển phòng tiếp nhận',
     'Kèm dòng phụ ghi số phiếu.'),
    ('Phòng tiếp nhận hiện tại', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Chữ xám.'),
    ('Phòng tiếp nhận mới', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Có', 'Trống',
     'Không liệt kê phòng tiếp nhận hiện tại.'),
    ('Nút Xác nhận', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thực hiện chuyển phòng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không thay đổi gì.'),
])

d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Chuyển phòng tiếp nhận', 'Click',
     'Before:\n– Kiểm tra quyền Xử lý yêu cầu sửa chữa và điều kiện phiếu.\n'
     '– Không có quyền → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối và báo '
     'không có quyền.\n'
     'After:\n– Mở cửa sổ chuyển phòng.'),
    ('Bấm Xác nhận', 'Click',
     'During:\n– Chưa chọn phòng → hiển thị “Bắt buộc phải nhập”.\n'
     '– Chọn trùng phòng hiện tại → hiển thị “Trùng phòng tiếp nhận trước đó.”\n'
     '– Phiếu không còn ở trạng thái Chờ xử lý → hiển thị “Phiếu không ở trạng thái cho phép '
     'chuyển phòng tiếp nhận.”\n'
     '– Nếu có lỗi thì không thực hiện bước After.\n'
     'After:\n– Đổi phòng tiếp nhận, làm mới mốc ngày gửi yêu cầu; trạng thái giữ nguyên.\n'
     '– Gửi thông báo cho toàn bộ nhân viên phòng tiếp nhận mới.\n'
     '– Ghi một dòng lịch sử nhóm “Thay đổi thông tin”.\n'
     '– Hiển thị “Chuyển phòng tiếp nhận thành công” và nạp lại danh sách.'),
])

# ------------------------------------------------------------------ 2.8 Tu choi
d.h3('2.8 Từ chối yêu cầu')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Từ chối yêu cầu', 'action',
            [('include', 'Kiểm tra quyền Xử lý yêu cầu sửa chữa'),
             ('include', 'Nhập lý do từ chối'),
             ('extend', 'Gửi thông báo cho người lập phiếu')],
            caption='Biểu đồ Use Case — FR-08 Từ chối yêu cầu')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc thao tác trạng thái, Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung điều kiện từ chối và tác động lên trạng thái phiếu tại phần mô tả chi tiết.',
           anchor='notice')
d.intro_table(
    ten='Từ chối yêu cầu',
    mota='Trả phiếu về cho người lập khi thông tin chưa đủ hoặc yêu cầu không hợp lệ, kèm lý do '
         'để người lập sửa và gửi lại.',
    tacnhan='Phòng tiếp nhận xử lý (người có quyền Xử lý yêu cầu sửa chữa)',
    dieukien='Như mục 2.7.',
    chinh='1. Người dùng bấm Từ chối ở dòng phiếu hoặc màn chi tiết.\n'
          '2. Hệ thống mở cửa sổ Từ chối yêu cầu.\n'
          '3. Người dùng nhập lý do từ chối và bấm Từ chối.\n'
          '4. Hệ thống chuyển phiếu về trạng thái Đang tạo, lưu lý do và báo cho người lập phiếu.',
    phu='• Không nhập lý do → báo “Bắt buộc phải nhập”.\n'
        '• Phiếu đã đổi trạng thái ở nơi khác → hệ thống từ chối và báo phiếu không ở trạng thái '
        'cho phép từ chối.',
    dacbiet='Phiếu trở lại Đang tạo nên chỉ người lập nhìn thấy; người lập sửa rồi gửi lại từ đầu.')

d.p('2.8.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Từ chối', modal='Từ chối yêu cầu', shot=shot('16-tu-choi.png'), shot_caption='Cửa sổ Từ chối yêu cầu')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Từ chối yêu cầu', 'Kèm dòng phụ ghi số phiếu.'),
    ('Dòng giải thích', 'Label', 'Read-only', '–', '–', 'Hiển thị',
     'Nêu rõ phiếu sẽ trở về trạng thái Đang tạo để người yêu cầu sửa lại.'),
    ('Lý do từ chối', 'Textarea', 'Enable', '0–1000 ký tự', 'Có', 'Trống',
     'Gợi ý “Nhập lý do từ chối”.'),
    ('Nút Từ chối', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Màu đỏ, nhóm thao tác nguy hiểm.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không thay đổi gì.'),
])

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Từ chối trong cửa sổ', 'Click',
     'Before:\n– Kiểm tra quyền Xử lý yêu cầu sửa chữa; không có quyền thì từ chối và báo không '
     'có quyền.\n'
     'During:\n– Lý do trống → hiển thị “Bắt buộc phải nhập”.\n'
     '– Phiếu không ở trạng thái cho phép → hiển thị “Phiếu không ở trạng thái cho phép từ chối.”\n'
     '– Nếu có lỗi thì không thực hiện bước After.\n'
     'After:\n– Chuyển phiếu về trạng thái Đang tạo và lưu lý do từ chối.\n'
     '– Ghi một dòng lịch sử nhóm “Thay đổi trạng thái” kèm lý do.\n'
     '– Gửi thông báo cho người lập phiếu.\n'
     '– Hiển thị “Từ chối yêu cầu thành công”.'),
])

# ------------------------------------------------- 2.9 Tao phieu xu ly yeu cau
d.h3('2.9 Tạo phiếu xử lý yêu cầu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Tạo phiếu xử lý yêu cầu', 'action',
            [('include', 'Kiểm tra quyền Xử lý yêu cầu sửa chữa'),
             ('include', 'Kiểm tra phiếu chưa có phiếu xử lý'),
             ('include', 'Chép dữ liệu sang phiếu xử lý')],
            caption='Biểu đồ Use Case — FR-09 Tạo phiếu xử lý yêu cầu')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc điều hướng sang chứng từ tiếp theo và Phân quyền. Chỉ bổ sung điều kiện lập phiếu xử lý của màn hình tại phần mô tả chi tiết.',
           anchor='notice')
d.intro_table(
    ten='Tạo phiếu xử lý yêu cầu từ phiếu yêu cầu',
    mota='Mở màn lập Phiếu xử lý yêu cầu với dữ liệu chép sẵn từ phiếu yêu cầu này. Đây là bước '
         'chuyển tiếp sang chứng từ thứ hai của luồng dịch vụ.',
    tacnhan='Phòng tiếp nhận xử lý (người có quyền Xử lý yêu cầu sửa chữa)',
    dieukien='Phiếu ở trạng thái Chờ xử lý, phòng tiếp nhận là phòng của người đăng nhập, và '
             'phiếu chưa từng có phiếu xử lý nào.',
    chinh='1. Người dùng bấm Tạo phiếu xử lý yêu cầu.\n'
          '2. Hệ thống mở màn lập Phiếu xử lý yêu cầu, chép sẵn thông tin khách hàng và danh sách '
          'thiết bị.\n'
          '3. Người dùng hoàn thiện và lưu phiếu xử lý (đặc tả ở tài liệu của màn đó).',
    phu='• Phiếu đã có phiếu xử lý → nút không còn hiển thị.\n'
        '• Gọi thẳng chức năng khi không đủ điều kiện → hệ thống từ chối và báo không thể lập '
        'phiếu xử lý cho phiếu yêu cầu này.',
    dacbiet='Mỗi phiếu yêu cầu chỉ lập được MỘT phiếu xử lý.')

d.p('2.9.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Tạo phiếu xử lý yêu cầu', shot=shot('15-menu-hanh-dong.png'), shot_caption='Các thao tác của một phiếu đang ở trạng thái Chờ xử lý')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Tạo phiếu xử lý yêu cầu', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
     'Hiện ở cột Hành động và ở thanh nút cuối màn chi tiết.'),
    ('Menu Hành động khác', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Chứa các thao tác còn lại: Từ chối, In, Lịch sử.'),
], required=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạo phiếu xử lý yêu cầu', 'Click',
     'Before:\n– Kiểm tra quyền, trạng thái phiếu, phòng tiếp nhận và việc phiếu chưa có phiếu '
     'xử lý.\n'
     '– Không thỏa mãn → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối và báo '
     'phiếu yêu cầu không ở trạng thái chờ xử lý của phòng bạn, hoặc đã có phiếu xử lý.\n'
     'After:\n– Mở màn lập Phiếu xử lý yêu cầu với dữ liệu chép sẵn từ phiếu này.'),
])

# ------------------------------------------------------------------- 2.10 Xoa
d.h3('2.10 Xóa phiếu yêu cầu')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu yêu cầu', 'crud',
            [('include', 'Kiểm tra phiếu Đang tạo do chính mình lập'),
             ('include', 'Xác nhận trước khi xóa')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu yêu cầu')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa, Thông báo và Quy định xác nhận. Chỉ bổ sung điều kiện được phép xóa của màn hình tại phần mô tả chi tiết.',
           anchor='delete')
d.intro_table(
    ten='Xóa phiếu yêu cầu',
    mota='Xóa hẳn phiếu chưa gửi đi cùng toàn bộ dòng thiết bị của phiếu.',
    tacnhan='Người lập phiếu',
    dieukien='Phiếu ở trạng thái Đang tạo và do chính người đăng nhập lập.',
    chinh='1. Người dùng bấm Xóa ở dòng phiếu hoặc màn chi tiết.\n'
          '2. Hệ thống hiển thị hộp xác nhận có ghi số phiếu.\n'
          '3. Người dùng bấm Xóa để xác nhận.\n'
          '4. Hệ thống xóa phiếu, ghi lịch sử và nạp lại danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa gì.\n'
        '• Phiếu đã gửi đi → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối.\n'
        '• Xóa dòng cuối của trang → tự lùi về trang trước.',
    dacbiet='Xóa là vĩnh viễn, không khôi phục được.')

d.p('2.10.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Xóa', modal='Xác nhận xóa', shot=shot('10-xac-nhan-xoa.png'), shot_caption='Hộp xác nhận xóa phiếu')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Cố định.'),
    ('Nội dung', 'Label', 'Read-only', 'Bạn có chắc muốn xóa phiếu “<số phiếu>”?',
     'Có ghi rõ số phiếu để tránh xóa nhầm.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa ở hộp xác nhận', 'Click',
     'Before:\n– Máy chủ kiểm tra lại phiếu ở trạng thái Đang tạo và do chính mình lập.\n'
     '– Không thỏa mãn → từ chối với thông báo “Chỉ được xóa phiếu ở trạng thái Đang tạo do chính '
     'bạn tạo.”\n'
     'After:\n– Xóa phiếu cùng toàn bộ dòng thiết bị.\n'
     '– Ghi một dòng lịch sử “Xóa”.\n'
     '– Hiển thị “Xóa thành công” và nạp lại danh sách.'),
])

# ------------------------------------------------------------------ 2.11 In
d.h3('2.11 In phiếu và in danh sách')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'In phiếu và in danh sách', 'io',
            [('include', 'Dựng bản in theo mẫu của công ty'),
             ('extend', 'Chặn in khi danh sách vượt 2.000 dòng')],
            caption='Biểu đồ Use Case — FR-11 In phiếu và in danh sách')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc In và Mẫu in chứng từ. Chỉ bổ sung nội dung bản in và giới hạn in danh sách của màn hình tại phần mô tả chi tiết.',
           anchor='notice')
d.intro_table(
    ten='In phiếu yêu cầu và in danh sách',
    mota='Dựng bản in một phiếu (khổ dọc) hoặc bản in danh sách theo bộ lọc đang áp dụng (khổ '
         'ngang), xem trước ngay trên màn hình rồi gửi ra máy in.',
    tacnhan='Người lập phiếu; Phòng tiếp nhận xử lý',
    dieukien='Với bản in một phiếu: phiếu nằm trong phạm vi xem của người dùng.',
    chinh='1. Người dùng bấm In ở dòng phiếu, ở màn chi tiết, hoặc bấm In danh sách trên thanh '
          'công cụ.\n'
          '2. Hệ thống dựng nội dung theo mẫu in của công ty ghi trên chứng từ.\n'
          '3. Cửa sổ xem trước hiển thị bản in.\n'
          '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
    phu='• In danh sách mà kết quả lọc vượt 2.000 dòng → hệ thống không dựng bản in, chỉ hiện lời '
        'nhắc thu hẹp bộ lọc hoặc dùng Xuất Excel.\n'
        '• Không có quyền xem phiếu → hệ thống từ chối in.',
    dacbiet='Tiêu đề công ty trên bản in lấy theo công ty ghi trên chứng từ, không theo người đang '
            'đăng nhập.')

d.p('2.11.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => In', modal='Xem trước phiếu yêu cầu', shot=shot('12-ban-in.png'), shot_caption='Xem trước bản in một phiếu')
d.figure(shot('14-in-danh-sach-ok.png'), 'Xem trước bản in danh sách theo bộ lọc', width_in=6.2)
d.figure(shot('13-in-danh-sach.png'),
         'Lời nhắc khi danh sách vượt mức in tối đa 2.000 dòng', width_in=6.2)

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In (từng phiếu)', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Có ở cột Hành động và ở thanh nút cuối màn chi tiết.'),
    ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', 'Trên thanh công cụ danh sách.'),
    ('Cửa sổ xem trước', 'Modal', 'Hiển thị', '–', 'Ẩn',
     'Tiêu đề “Xem trước phiếu yêu cầu” hoặc “Xem trước danh sách…”.'),
    ('Nút In trong cửa sổ', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở hộp thoại in của trình duyệt; bản in không kèm nút và khung viền.'),
    ('Lời nhắc vượt trần in', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     'Nền vàng, ghi rõ số dòng thực tế và mức tối đa 2.000 dòng.'),
    ('Nội dung bản in một phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tiêu đề công ty; thông tin khách hàng, người yêu cầu, phòng yêu cầu, ngày nhận yêu cầu; '
     'bảng thiết bị 7 cột; 4 ô ký tên.'),
    ('Nội dung bản in danh sách', 'Table/Grid', 'Read-only', '–', 'Theo bộ lọc',
     'Hai dòng Thời gian và Phòng yêu cầu (ghi “Tất cả” khi không lọc); bảng 10 cột; mỗi phiếu '
     'một dòng dù có nhiều thiết bị.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In ở một phiếu', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu; không có quyền thì từ chối.\n'
     'During:\n– Dựng nội dung theo mẫu in, lấy tiêu đề công ty theo công ty ghi trên chứng từ.\n'
     'After:\n– Mở cửa sổ xem trước.'),
    ('Bấm In danh sách', 'Click',
     'During:\n– Đếm số dòng khớp bộ lọc hiện tại.\n'
     '– Vượt 2.000 dòng → không dựng bản in, hiển thị lời nhắc thu hẹp bộ lọc.\n'
     'After:\n– Dựng bản in danh sách theo đúng bộ lọc và mở cửa sổ xem trước.'),
])

# ------------------------------------------------------------- 2.12 Xuat Excel
d.h3('2.12 Xuất Excel')

d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Xuất Excel', 'io',
            [('include', 'Chọn trường và thứ tự cột'),
             ('include', 'Tải dữ liệu theo từng đợt 2.000 dòng')],
            caption='Biểu đồ Use Case — FR-12 Xuất Excel')

d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của màn hình tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Xuất danh sách ra tệp Excel',
    mota='Xuất toàn bộ phiếu khớp bộ lọc hiện tại ra tệp Excel, với các cột và thứ tự cột do '
         'người dùng chọn.',
    tacnhan='Người lập phiếu; Phòng tiếp nhận xử lý',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ Chọn trường xuất file với 6 trường mặc định trong tổng số 13.\n'
          '3. Người dùng chọn trường theo thứ tự mong muốn rồi bấm Xuất file.\n'
          '4. Hệ thống tải dữ liệu theo từng đợt và hiển thị dòng tiến độ.\n'
          '5. Tệp được dựng và tải về máy người dùng.',
    phu='• Bỏ chọn hết trường → không xuất được.\n'
        '• Bộ lọc không ra dòng nào → hệ thống báo không có dữ liệu để xuất.\n'
        '• Trong lúc xuất, nút Xuất Excel bị khóa để tránh bấm nhiều lần.',
    dacbiet='Tệp xuất theo đúng bộ lọc đang áp dụng, không giới hạn ở trang đang xem.')

d.p('2.12.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Xuất excel', modal='Chọn trường xuất file', shot=shot('04-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Trường xuất', 'Dropdown', 'Enable', 'Danh sách 13 trường', 'Có', '6 trường mặc định',
     'Thứ tự cột trong tệp chạy theo đúng thứ tự chọn.'),
    ('Dòng “Thứ tự cột trong file”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn',
     'Cho biết trước thứ tự cột sẽ xuất.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khóa khi chưa chọn trường nào hoặc đang xuất.'),
    ('Dòng tiến độ', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện “Đã tải …/… dòng” rồi “Đang dựng file …/… dòng”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ.'),
])

d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất file', 'Click',
     'During:\n– Chưa chọn trường nào → nút không dùng được.\n'
     '– Tải dữ liệu theo từng đợt 2.000 dòng trong phạm vi dữ liệu và bộ lọc hiện tại.\n'
     'After:\n– Dựng tệp Excel với cột STT ở đầu, tải về máy và hiển thị “Xuất Excel thành công”.'),
])

# ---------------------------------------------------------------- 2.13 Lich su
d.h3('2.13 Xem lịch sử thay đổi')

d.p('2.13.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung danh sách trường được theo dõi riêng của màn hình tại phần mô tả chi tiết.',
           anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Xem ai đã làm gì với phiếu: tạo mới, sửa những trường nào (giá trị cũ → giá trị mới), '
         'đổi trạng thái và lý do kèm theo.',
    tacnhan='Người lập phiếu; Phòng tiếp nhận xử lý',
    dieukien='Phiếu nằm trong phạm vi xem của người đăng nhập.',
    chinh='1. Người dùng chọn Lịch sử ở dòng phiếu, hoặc bấm Xem lịch sử ở khối Lịch sử trong màn '
          'chi tiết.\n'
          '2. Hệ thống nạp danh sách thao tác, mới nhất lên đầu.\n'
          '3. Người dùng có thể lọc theo loại hoạt động, người thực hiện và khoảng ngày.',
    phu='• Phiếu chưa có thao tác nào → hiện thông báo chưa có lịch sử.\n'
        '• Bản ghi tạo từ hệ thống cũ có thể không có lịch sử.',
    dacbiet='Thay đổi ở bảng thiết bị được ghi rõ thiết bị nào thêm mới, bị xóa, hoặc sửa trường nào.')

d.p('2.13.2 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Lịch sử', modal='Lịch sử thay đổi', shot=shot('18-lich-su-popup.png'), shot_caption='Cửa sổ Lịch sử thay đổi mở từ danh sách')
d.figure(shot('09-lich-su.png'), 'Khối Lịch sử trong màn chi tiết', width_in=6.2)

d.p('2.13.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng thời gian', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mục gồm thời điểm, tên hành động, người thực hiện kèm phòng ban và khối thay đổi.'),
    ('Giá trị cũ / giá trị mới', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Giá trị cũ màu đỏ, giá trị mới màu xanh.'),
    ('Bộ lọc', 'Dropdown / Datepicker', 'Enable', 'Loại hoạt động, người thực hiện, khoảng ngày',
     'Trống', 'Loại hoạt động gồm Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', 'Nạp lại lịch sử.'),
    ('Nút Thu gọn / Xem lịch sử', 'Button', 'Enable', '–', 'Thu gọn',
     'Chỉ có ở khối Lịch sử trong màn chi tiết.'),
], required=False)

d.p('2.13.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở lịch sử', 'Click',
     'After:\n– Nạp danh sách thao tác của đúng phiếu đó, sắp xếp mới nhất lên đầu.'),
    ('Chọn điều kiện lọc rồi bấm Tìm kiếm', 'Click',
     'After:\n– Chỉ hiển thị các mục thỏa mãn; không gọi lại máy chủ.'),
])

# =================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu kiểm tra sửa chữa – bảo '
           'hành; không lặp lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại ')

d.rule_table([
    ('BR-01', 'Số phiếu sinh tự động',
     '– Số phiếu theo khuôn “<mã công ty>.YCSCBH.<2 số cuối của năm>.<6 chữ số>”, ví dụ TPE.YCSCBH.26.005682.\n– Số phiếu do hệ thống sinh sau khi ghi phiếu, người dùng không nhập và không sửa được.\n– Mã công ty lấy theo công ty của người lập phiếu.', 'Lập phiếu'),
    ('BR-02', 'Bộ trạng thái của phiếu',
     '– Phiếu có 9 trạng thái: Đang tạo, Chờ xử lý, Đang xử lý, Đang CCTT, Đã CCTT báo giá, Đã báo giá, Đã lập hợp đồng, Đã xử lý, Đã tư vấn điện thoại.\n– Màn hình này chỉ trực tiếp tạo ra hai trạng thái: Đang tạo (Lưu nháp, hoặc bị Từ chối trả về) và Chờ xử lý (Lưu và gửi).\n– Các trạng thái còn lại do những chứng từ phía sau của luồng dịch vụ ghi ngược về; cùng lúc đó hệ thống ghi Người xử lý và Ngày xử lý lên phiếu.\n– Chữ và màu của trạng thái do máy chủ quyết định để mọi màn hình hiển thị thống nhất.', 'Toàn màn hình'),
    ('BR-03', 'Bắt buộc nhập khác nhau giữa Lưu nháp và Lưu và gửi',
     '– Lưu nháp chỉ bắt buộc: Khách hàng và tên thiết bị của từng dòng.\n– Lưu và gửi bắt buộc thêm: Người liên hệ, Địa chỉ sửa chữa, Ghi chú, Phòng tiếp nhận xử lý, Serial và Nội dung yêu cầu của từng thiết bị, và phiếu phải có ít nhất một thiết bị.\n– Đây là điểm khác có chủ đích so với phần mềm ERP: bên ERP bắt buộc đầy đủ ngay cả khi lưu nháp.', 'Lập phiếu\nChỉnh sửa phiếu'),
    ('BR-04', 'Ràng buộc serial thiết bị',
     '– Không được trùng serial giữa các dòng trong cùng một phiếu, kể cả serial chọn từ danh mục lẫn serial gõ tay.\n– Serial gõ tay mà đã tồn tại trong danh mục thì phải chọn từ danh sách, không được gõ.\n– Chỉ được chuyển sang chế độ nhập serial tạm khi số lượng thiết bị lớn hơn số serial đã khai trong danh mục.', 'Lập phiếu\nChỉnh sửa phiếu'),
    ('BR-05', 'Điều kiện sửa và xóa',
     '– Chỉ sửa và xóa được phiếu ở trạng thái Đang tạo và do chính người đăng nhập lập.\n– Điều kiện được kiểm tra ở máy chủ, không chỉ ẩn nút trên giao diện: vào thẳng màn sửa bằng đường dẫn sẽ bị chuyển về màn chi tiết và mọi yêu cầu cập nhật đều bị từ chối.\n– Xóa phiếu là xóa cả các dòng thiết bị của phiếu, không khôi phục được.', 'Chỉnh sửa phiếu\nXóa phiếu'),
    ('BR-06', 'Ba thao tác của phòng tiếp nhận',
     '– Tạo phiếu xử lý yêu cầu, Chuyển phòng tiếp nhận và Từ chối dùng chung một bộ điều kiện: phiếu ở trạng thái Chờ xử lý, phòng tiếp nhận là phòng của người đăng nhập, phiếu chưa có phiếu xử lý, và người dùng có quyền Xử lý yêu cầu sửa chữa.\n– Người quản trị hệ thống được bỏ qua điều kiện phòng ban.\n– Mỗi phiếu yêu cầu chỉ lập được một phiếu xử lý; lập xong thì cả ba thao tác này đều biến mất.', 'Chuyển phòng tiếp nhận\nTừ chối yêu cầu\nTạo phiếu xử lý yêu cầu'),
    ('BR-07', 'Phiếu nháp là riêng tư',
     '– Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy, kể cả người có quyền xem theo tổng công ty và người quản trị hệ thống.\n– Phiếu bị Từ chối trở về Đang tạo nên cũng chỉ người lập nhìn thấy cho tới khi gửi lại.\n– Đây là điểm chặt hơn có chủ đích so với phần mềm ERP.', 'Xem danh sách\nXem chi tiết phiếu'),
    ('BR-08', 'Phạm vi dữ liệu theo lối vào',
     '– Vào từ CSKH: hiển thị toàn bộ phiếu trong phạm vi quyền của người đăng nhập.\n– Vào từ Bán hàng: chỉ hiển thị phiếu do chính người đăng nhập lập, bất kể người đó có quyền xem theo cấp nào.\n– Người có quyền Xử lý yêu cầu sửa chữa luôn được nhìn thấy thêm mọi phiếu gửi về phòng mình.', 'Xem danh sách\nTìm kiếm và lọc'),
    ('BR-09', 'Thông báo cho người liên quan',
     '– Phiếu chuyển sang Chờ xử lý (do gửi mới hoặc do chuyển phòng): thông báo gửi cho TOÀN BỘ nhân viên của phòng tiếp nhận xử lý.\n– Phiếu bị Từ chối: thông báo gửi cho người lập phiếu, kèm lý do từ chối. Đây là điểm bổ sung so với phần mềm ERP.\n– Lỗi gửi thông báo không làm hỏng nghiệp vụ: phiếu vẫn được lưu và đổi trạng thái bình thường.', 'Lập phiếu\nChuyển phòng tiếp nhận\nTừ chối yêu cầu'),
    ('BR-10', 'Chuyển phòng tiếp nhận không đổi trạng thái',
     '– Thao tác chuyển phòng chỉ đổi phòng tiếp nhận và làm mới mốc ngày gửi yêu cầu; phiếu vẫn ở trạng thái Chờ xử lý.\n– Không được chọn lại đúng phòng tiếp nhận hiện tại.\n– Thao tác được ghi vào lịch sử ở nhóm “Thay đổi thông tin”.', 'Chuyển phòng tiếp nhận'),
    ('BR-11', 'Ghi lịch sử thay đổi',
     '– Hệ thống ghi lịch sử cho các trường: số phiếu, tên khách hàng, người liên hệ, số điện thoại liên hệ, địa chỉ sửa chữa, ghi chú, phòng tiếp nhận xử lý và bảng thiết bị.\n– Đổi trạng thái được ghi riêng ở nhóm “Thay đổi trạng thái”, kèm lý do nếu thao tác có nhập lý do.\n– Thay đổi ở bảng thiết bị chỉ liệt kê đúng trường đã đổi của từng thiết bị, không in lại cả dòng.', 'Toàn màn hình'),
    ('BR-12', 'Giới hạn khi in danh sách',
     '– Bản in danh sách chỉ dựng được tối đa 2.000 dòng; vượt mức này hệ thống không dựng bản in mà nhắc người dùng thu hẹp bộ lọc hoặc dùng Xuất Excel.\n– Bản in danh sách gộp mỗi phiếu một dòng, các thiết bị xuống dòng trong cùng một ô — khác với phần mềm ERP tách mỗi thiết bị một dòng.\n– Tiêu đề công ty trên mọi bản in lấy theo công ty ghi trên chứng từ, không theo người đang đăng nhập.', 'In phiếu và in danh sách'),
])

d.save()
