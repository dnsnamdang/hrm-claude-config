# -*- coding: utf-8 -*-
"""SRS Danh mục gói bảo dưỡng — dựng trên KHUÔN "SRS - Danh mục quốc gia" (bản TPE duyệt 23/09/2026).

4 phần: Giới thiệu / Phân quyền / Đặc tả chi tiết theo chức năng / Quy tắc nghiệp vụ. Mỗi chức
năng: Biểu đồ Usecase · Giới thiệu (dẫn chiếu SRS quy tắc chung) · Layout (đường bấm menu + ảnh thật, KHÔNG ghi URL)
· Mô tả giao diện · Danh sách event. Nội dung bám code gop_db ngày 28/09/2026 (bỏ "Xóa gói đã dùng thì chuyển sang Khóa", thêm nút Khóa riêng,
cấp / ghi chú kiểm tra đã khóa không chọn được).

Chạy:  python3 gen_srs.py "<SRS - Danh mục quốc gia.docx>"
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from qg_writer import QgWriter  # noqa: E402

SH = os.path.join(HERE, 'shots')
IC = os.path.join(HERE, 'icons')
UML = os.path.join(HERE, 'uml')
CROP = os.path.join(HERE, 'crops')

ROLES = {'pagebreak': 11, 'h1': 12, 'h2': 13, 'h3': 35, 'p': 14, 'bullet': 15, 'sub': 36,
         'qtc': 37, 'menu_b': 42, 'menu': 43, 'img': 44, 'cap': 45, 'blank': 19,
         'tbl2': 18, 'tbl4': 50, 'tbl5': 47, 'tbl6': 64, 'tbl7': 87, 'tbl8': 108}


def s(n):
    return os.path.join(SH, n + '.png')


def ic(n, h=0.24, alt=None):
    """Icon cắt từ UI; chưa có file (icon mới chờ cắt) thì dùng chữ `alt`."""
    path = os.path.join(IC, n + '.png')
    if alt is not None and not os.path.exists(path):
        print('  [thiếu icon] %s -> dùng chữ “%s”' % (n, alt))
        return alt
    return ('img', path, h)


MENU = ['Phân hệ CSKH sau bán ', ic('menu_phanhe'), ' => Danh mục ', ic('menu_danhmuc'),
        ' => Gói bảo dưỡng ', ic('menu_goibaoduong_c')]
QTC_LINK = 'SRS_Các quy tắc chung_VN_1.0'


class Srs(object):
    def __init__(self, w):
        self.w = w
        self.sec = 0

    def fr(self, title, uc=None, gioi_thieu=None, qtc=None, layout=None, ui=None, ui_widths=None,
           events=None):
        if not ui or not events:  # skill srs-documenter 28/09/2026: bắt buộc ở mọi chức năng
            raise ValueError('FR "%s" thiếu ui/events' % title)
        w = self.w
        self.sec += 1
        n = '2.%d' % self.sec
        w.h3('%s %s' % (n, title))
        k = 0
        if uc:
            k += 1
            w.raw('sub', '%s.%d Biểu đồ Usecase' % (n, k))
            w.image(os.path.join(UML, uc + '.png'), width=5.2,
                    caption='Biểu đồ Use Case — %s' % title)
        k += 1
        w.raw('sub', '%s.%d Giới thiệu' % (n, k))
        if qtc:
            w.clone_texts('qtc', ['Quy tắc chung: ', 'Áp dụng SRS Các quy tắc chung ', QTC_LINK,
                                  ' - ' + qtc])
        w.table([['Mục', 'Nội dung']] + gioi_thieu, widths=[1, 3.2])
        k += 1
        w.raw('sub', '%s.%d Layout màn hình' % (n, k))
        w.p('Đường dẫn màn hình:')
        w.raw('menu_b', 'Menu: ')
        w.raw('menu', MENU + (layout.get('suffix') or []))
        if layout.get('note'):
            w.p(layout['note'])
        for img, cap in layout['imgs']:
            path = img if os.path.isabs(img) else s(img)
            if os.path.exists(path):
                w.image(path, caption=cap)
            else:  # ảnh mới chờ chụp — bỏ qua, không dừng bản dựng
                print('  [thiếu ảnh] %s — %s' % (os.path.basename(path), cap))
        if ui:
            k += 1
            w.raw('sub', '%s.%d Mô tả chi tiết giao diện' % (n, k))
            w.table(ui, widths=ui_widths)
        if events:
            k += 1
            w.raw('sub', '%s.%d Danh sách event và xử lý event' % (n, k))
            w.table([['STT', 'Event', 'Loại event', 'Xử lý event']] +
                    [[str(i + 1)] + e for i, e in enumerate(events)], widths=[0.6, 1.4, 0.8, 3.4])


def build(template, out):
    w = QgWriter(template, ROLES, body_from=10,
                 cover_replace={'Danh mục quốc gia': 'Danh mục gói bảo dưỡng'})
    S = Srs(w)

    # ============================================================ Phần 1
    w.h1('Phần 1. Giới thiệu')
    w.h2('1 Mục đích')
    w.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục gói bảo dưỡng (phân hệ CSKH sau bán), nhằm:')
    w.bullet('Là căn cứ nghiệm thu chức năng.')
    w.bullet('Làm rõ cách khai bảng nội dung kiểm tra theo cấp bảo dưỡng và cách hệ thống tính giá vốn / giá bán của gói.')
    w.bullet('Làm rõ ràng buộc trùng tên, trùng mã gói, điều kiện xóa hẳn gói chưa được sử dụng và thao tác Khóa / Mở khóa.')
    w.h2('2 Thuật ngữ và viết tắt')
    w.table([
        ['Thuật ngữ', 'Mô tả'],
        ['Gói bảo dưỡng', 'Bản ghi của danh mục: thông tin chung, bảng nội dung kiểm tra theo cấp, giá theo công ty, hàng hóa áp dụng, file PDF.'],
        ['Cấp bảo dưỡng', 'Lấy từ danh mục Cấp dịch vụ bảo dưỡng; mỗi cấp là một cột của bảng nội dung kiểm tra.'],
        ['Nội dung kiểm tra bảo dưỡng', 'Một hạng mục phải làm khi bảo dưỡng; mỗi hạng mục là một dòng, kèm ĐVT và SL.'],
        ['Ghi chú kiểm tra', 'Ký hiệu công việc tại ô giao dòng × cột, lấy từ danh mục Ghi chú kiểm tra bảo dưỡng.'],
        ['Giá vốn', 'Đơn giá công của công ty quản lý × Định mức công × Hệ số công nghệ.'],
        ['Giá công thức', 'Giá vốn × Hệ số giá bán gói bảo dưỡng.'],
        ['Giá bán cơ sở', 'Mặc định = Giá công thức, cho phép sửa tay. Giá bán theo công ty = Giá bán cơ sở × Hệ số giá bán của công ty.'],
        ['Gói đã được sử dụng', 'Gói đã được chọn ở ít nhất một chứng từ: báo giá dịch vụ, hợp đồng dịch vụ, phụ lục hợp đồng dịch vụ, đề nghị xuất dịch vụ, đề nghị hạch toán dịch vụ, hạch toán dịch vụ; báo giá, hợp đồng, phiếu giao việc, phiếu nhập kết quả của dịch vụ bảo hành – sửa chữa. Chỉ gắn hàng hóa áp dụng thì chưa tính là đã sử dụng.'],
        ['Trạng thái Hoạt động / Khóa', 'Hoạt động: dùng được ở màn nghiệp vụ khác. Khóa: vẫn nằm trong danh mục, không chọn được ở chứng từ mới, không sửa/xóa được cho tới khi Mở khóa.'],
    ], widths=[1.3, 3])

    # ============================================================ Phần 2
    w.h1('Phần 2. Phân quyền')
    w.h2('1 Danh sách quyền')
    w.p('Màn hình dùng 3 quyền thuộc nhóm “Danh mục dịch vụ bảo dưỡng”. Các chức năng chỉ xem (xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử) không gắn quyền riêng.')
    w.table([
        ['Tên quyền', 'Tác dụng trên màn hình'],
        ['Thêm danh mục gói bảo dưỡng', 'Hiện nút Tạo mới, Import Excel, Nhân bản; cho phép tải file PDF đính kèm.'],
        ['Sửa danh mục gói bảo dưỡng', 'Hiện nút Sửa, Khóa (gói Hoạt động), Mở khóa (gói Khóa); cho phép tải file PDF đính kèm.'],
        ['Xóa danh mục gói bảo dưỡng', 'Hiện nút Xóa (gói Hoạt động, chưa được sử dụng).'],
    ], widths=[1.5, 3])
    w.h2('2 Ma trận phân quyền')
    Y, N = '✔', '–'
    w.table([
        ['Chức năng', 'Đã đăng nhập (không quyền)', 'Thêm', 'Sửa', 'Xóa'],
        ['FR-01 Xem danh sách gói bảo dưỡng', Y, Y, Y, Y],
        ['FR-02 Tìm kiếm và lọc', Y, Y, Y, Y],
        ['FR-03 Thêm mới gói bảo dưỡng', N, Y, N, N],
        ['FR-04 Chỉnh sửa gói bảo dưỡng', N, N, Y, N],
        ['FR-05 Xóa gói bảo dưỡng', N, N, N, Y],
        ['FR-06 Khóa / Mở khóa gói bảo dưỡng', N, N, Y, N],
        ['FR-07 Xem lịch sử thay đổi', Y, Y, Y, Y],
        ['FR-08 Import file gói bảo dưỡng', N, Y, N, N],
        ['FR-09 Xuất danh sách ra Excel', Y, Y, Y, Y],
        ['FR-10 Xem chi tiết gói bảo dưỡng', Y, Y, Y, Y],
        ['FR-11 Tùy chỉnh cột hiển thị', Y, Y, Y, Y],
        ['FR-12 Nhân bản gói bảo dưỡng', N, Y, N, N],
        ['FR-13 In phiếu kiểm tra bảo dưỡng', Y, Y, Y, Y],
    ], widths=[2.4, 1.3, 0.6, 0.6, 0.6])
    w.p('Khóa / Mở khóa (FR-06) — nút Khóa riêng ở danh sách, chân trang Chi tiết, hoặc đổi Trạng thái trong form Sửa — đều cần quyền Sửa. Nút không có quyền dùng thì bị ẩn hẳn. Máy chủ chặn lại mọi thao tác ghi khi thiếu quyền, kể cả khi gọi thẳng API.')

    # ============================================================ Phần 3
    w.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
    w.h2('1 Sơ đồ UML tổng quan')
    w.image(os.path.join(UML, 'overview.png'), width=5.6,
            caption='Sơ đồ Use Case tổng quan màn Danh mục gói bảo dưỡng')
    w.h2('2 Đặc tả chi tiết từng chức năng')

    ACT_ALL = 'Người dùng đã đăng nhập'

    # 2.1 Xem danh sách
    S.fr('Xem danh sách gói bảo dưỡng',
         qtc='Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của Danh mục gói bảo dưỡng tại phần mô tả chi tiết.',
         gioi_thieu=[
             ['Tên chức năng', 'Xem danh sách gói bảo dưỡng'],
             ['Mô tả', 'Hiển thị toàn bộ gói bảo dưỡng của hệ thống (không phân theo công ty/phòng ban), có phân trang và sắp xếp.'],
             ['Tác nhân', ACT_ALL],
             ['Điều kiện ban đầu', 'Người dùng đã đăng nhập vào hệ thống.'],
             ['Dòng sự kiện chính', '1. Người dùng vào menu Phân hệ CSKH sau bán → Danh mục → Gói bảo dưỡng.\n2. Hệ thống nạp trang đầu tiên (10 dòng), xếp Ngày tạo giảm dần.\n3. Bảng hiển thị dữ liệu kèm dòng “Hiển thị a–b / N”.'],
             ['Dòng sự kiện phụ', '• Không có bản ghi → bảng hiện thông báo không có dữ liệu.\n• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.'],
         ],
         layout={'imgs': [('48_unsaved', 'Màn Danh mục gói bảo dưỡng lúc mới truy cập'),
                          ('33_tooltip_gia', 'Biểu tượng ⓘ hiển thị giá bán theo từng cấp')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Mô tả'],
             ['1', 'STT', 'Table/Grid', 'Read-only', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị, không ẩn được.'],
             ['2', 'Mã', 'Table/Grid', 'Read-only', 'Mã gói, sắp xếp được, không ẩn được. Bấm vào mã mở màn Chi tiết (xem 2.10).'],
             ['3', 'Tên gói bảo dưỡng', 'Table/Grid', 'Read-only', 'Sắp xếp được. Gói đã khai cấp có biểu tượng ⓘ: rê chuột hiện giá bán theo từng cấp (định dạng 1,234,000).'],
             ['4', 'Công ty quản lý gói bảo dưỡng', 'Table/Grid', 'Read-only', 'Mặc định ẩn.'],
             ['5', 'Người cập nhật', 'Table/Grid', 'Read-only', 'Mặc định ẩn.'],
             ['6', 'Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm. Mặc định ẩn, sắp xếp được.'],
             ['7', 'Người tạo', 'Table/Grid', 'Read-only', 'Người tạo gói.'],
             ['8', 'Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm, sắp xếp được.'],
             ['9', 'Trạng thái', 'Badge', 'Read-only', 'Hoạt động (xanh) / Khóa (đỏ).'],
             ['10', 'Hành động', 'Table/Grid', 'Read-only', 'Tối đa 2 nút hiện thẳng, còn lại trong nút ba chấm. Sửa: quyền Sửa + Hoạt động. Xóa: quyền Xóa + Hoạt động + chưa được sử dụng ở chứng từ. Khóa: quyền Sửa + Hoạt động (kể cả gói đã được sử dụng). Mở khóa: quyền Sửa + Khóa. Nhân bản: quyền Thêm. In, Lịch sử: luôn hiện.'],
             ['11', 'Nút Tạo mới', 'Button', 'Enable', 'Chỉ hiện khi có quyền Thêm. Mở trang Thêm gói bảo dưỡng (xem 2.3).'],
             ['12', 'Nút Xuất Excel', 'Button', 'Enable', 'Mở cửa sổ Chọn trường xuất file (xem 2.9).'],
             ['13', 'Nút Import Excel', 'Button', 'Enable', 'Chỉ hiện khi có quyền Thêm. Mở cửa sổ Import gói bảo dưỡng (xem 2.8).'],
             ['14', 'Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', 'Mở cửa sổ Tuỳ chỉnh cột (xem 2.11).'],
             ['15', 'Phân trang', 'Pagination', 'Enable', 'Số dòng/trang 5 / 10 / 20 / 50 / 100, mặc định 10.'],
         ], ui_widths=[0.6, 1.4, 0.9, 0.8, 3],
         events=[['Mở màn hình', 'System', 'After:\n– Nạp trang đầu, xếp Ngày tạo giảm dần, hiển thị tổng số bản ghi.'],
                 ['Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Đổi chiều sắp xếp và nạp lại danh sách từ trang 1.'],
                 ['Chuyển trang', 'Click', 'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'],
                 ['Đổi số dòng mỗi trang', 'Change', 'After:\n– Quay về trang 1 và nạp lại theo số dòng mới.'],
                 ['Rê chuột vào biểu tượng ⓘ', 'Hover', 'After:\n– Hiện danh sách “Cấp: giá bán” của gói.']])

    # 2.2 Tìm kiếm và lọc
    S.fr('Tìm kiếm và lọc',
         qtc='Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang. Chỉ bổ sung các tiêu chí tìm kiếm/lọc riêng của Danh mục gói bảo dưỡng.',
         gioi_thieu=[
             ['Tên chức năng', 'Tìm kiếm và lọc danh sách'],
             ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh, ô Trạng thái và ô Người tạo.'],
             ['Tác nhân', ACT_ALL],
             ['Điều kiện ban đầu', 'Đang ở màn Danh mục gói bảo dưỡng.'],
             ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa hoặc chọn tiêu chí lọc.\n2. Hệ thống tự lọc (ô gõ chờ khoảng 0,4 giây; ô chọn lọc ngay) hoặc lọc ngay khi bấm Tìm kiếm / Enter.\n3. Hệ thống áp đồng thời mọi tiêu chí và nạp lại danh sách từ trang 1.'],
             ['Dòng sự kiện phụ', '• Không có kết quả → bảng hiện thông báo không có dữ liệu.\n• Bấm Làm mới → xóa hết tiêu chí VÀ nạp lại danh sách đầy đủ ngay.'],
         ],
         layout={'imgs': [(os.path.join(CROP, 'filter.png'), 'Khu vực Bộ lọc danh sách'),
                          ('36_filter_status', 'Kết quả lọc Trạng thái = Khóa')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Mô tả'],
             ['1', 'Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Placeholder “Tìm theo tên hoặc mã gói bảo dưỡng...”. Tìm theo TÊN hoặc MÃ (khớp một phần, không phân biệt hoa thường). Từ 2 ký tự trở lên và chưa bấm sắp xếp thì xếp theo độ khớp: trùng khít → bắt đầu bằng từ khóa → chứa từ khóa (mã ưu tiên hơn tên).'],
             ['2', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Nhãn nổi. Bỏ trống thì hiện cả hai trạng thái.'],
             ['3', 'Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Nhãn nổi, hiển thị “Tên - Mã phòng - Mã nhân viên”. Lọc gói do người đó tạo.'],
             ['4', 'Nút Tìm kiếm', 'Button', 'Enable', '–', 'Áp dụng ngay các tiêu chí.'],
             ['5', 'Nút Làm mới', 'Button', 'Enable', '–', 'Xóa hết tiêu chí VÀ nạp lại danh sách ngay.'],
         ], ui_widths=[0.6, 1.2, 0.8, 0.7, 1.1, 2.8],
         events=[['Gõ vào ô tìm kiếm nhanh', 'Input', 'After:\n– Sau khoảng 0,4 giây ngừng gõ, nạp lại bảng từ trang 1.'],
                 ['Chọn Trạng thái / Người tạo', 'Change', 'After:\n– Nạp lại bảng từ trang 1 theo mọi tiêu chí (kiểu “và”).'],
                 ['Bấm Tìm kiếm / Enter', 'Click', 'After:\n– Nạp lại bảng ngay, cập nhật tổng số bản ghi.'],
                 ['Bấm Làm mới', 'Click', 'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ.']])

    # 2.3 Thêm mới
    S.fr('Thêm mới gói bảo dưỡng', uc='uc_fr03',
         qtc='Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
         gioi_thieu=[
             ['Tên chức năng', 'Thêm mới gói bảo dưỡng'],
             ['Mô tả', 'Tạo gói mới trên TRANG RIÊNG gồm 5 khối: Thông tin chung; Danh mục kiểm tra bảo dưỡng định kỳ (ma trận nội dung × cấp) kèm thông số giá; Giá vốn theo công ty; Áp dụng cho hàng hóa; File đính kèm (PDF).'],
             ['Tác nhân', 'Người dùng có quyền “Thêm danh mục gói bảo dưỡng”.'],
             ['Điều kiện ban đầu', 'Đang ở màn Danh mục gói bảo dưỡng.'],
             ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở trang “Thêm gói bảo dưỡng”, Công ty quản lý điền sẵn công ty của người dùng, Trạng thái = Hoạt động, bảng Giá vốn theo công ty liệt kê mọi công ty với hệ số 1.\n3. Người dùng nhập thông tin, khai bảng nội dung kiểm tra, chọn hàng hóa, đính kèm PDF và bấm Lưu.\n4. Hệ thống kiểm tra dữ liệu, ghi gói mới và ghi lịch sử Tạo mới.\n5. Hiển thị “Tạo gói bảo dưỡng thành công” và quay về danh sách.'],
             ['Dòng sự kiện phụ', '• Thiếu trường bắt buộc / sai định dạng / trùng → báo lỗi đỏ dưới ô và toast “Vui lòng kiểm tra lại dữ liệu nhập”, trang KHÔNG chuyển đi, dữ liệu còn nguyên.\n• Bấm “Lưu và tiếp tục” → ghi gói rồi làm trắng form để nhập gói kế tiếp.\n• Bấm Quay lại khi đã nhập dở → hỏi “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại).\n• Bấm Lưu nhiều lần liên tiếp → chỉ tạo đúng một gói.'],
             ['Yêu cầu đặc biệt', 'Chân trang có 3 nút: Lưu, Lưu và tiếp tục, Quay lại. Mã tự chuyển CHỮ IN HOA khi gõ. Bắt buộc ít nhất 1 file PDF.'],
         ],
         layout={'suffix': [' => Tạo mới ', ic('btn_taomoi')],
                
                 'imgs': [('13_create_top', 'Trang Thêm gói bảo dưỡng khi vừa mở'),
                          ('20_sec', 'Khối Thông tin chung'),
                          ('21_sec', 'Khối Danh mục kiểm tra bảo dưỡng định kỳ và thông số giá'),
                          ('22_sec', 'Khối Giá vốn theo công ty'),
                          ('23_sec', 'Khối Áp dụng cho hàng hóa'),
                          (os.path.join(CROP, 'sec_file.png'), 'Khối File đính kèm (PDF)'),
                          (os.path.join(CROP, 'err_fe.png'), 'Lỗi đỏ ngay dưới ô còn thiếu / sai định dạng')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Mô tả'],
             ['1', 'Tên gói bảo dưỡng', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Duy nhất toàn hệ thống. Bỏ trống “Bắt buộc phải nhập”; trùng “Đã tồn tại”; quá dài “Tối đa 255 ký tự”.'],
             ['2', 'Mã gói bảo dưỡng', 'Textbox', 'Enable', '1–255 ký tự; chữ không dấu, số, - và _', 'Có', 'Duy nhất toàn hệ thống, tự in hoa khi gõ. Sai định dạng báo ngay “Chỉ gồm chữ không dấu, số, dấu - và _”; trùng “Đã tồn tại”.'],
             ['3', 'Định mức đàm phán giá (%)', 'Number', 'Enable', '0–99, 2 số thập phân', 'Không', 'Vượt trần “Tối đa 99”.'],
             ['4', 'VAT (%)', 'Number', 'Enable', '0–100, 2 số thập phân', 'Không', 'Trống lưu 0. Vượt trần “Tối đa 100”.'],
             ['5', 'Công ty quản lý gói bảo dưỡng', 'Dropdown', 'Enable', 'Danh sách công ty', 'Có', 'Mặc định công ty của người dùng. Quyết định đơn giá công.'],
             ['6', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Mặc định Hoạt động.'],
             ['7', 'Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'In ở cuối phiếu kiểm tra.'],
             ['8', 'Hệ số giá bán gói bảo dưỡng', 'Number', 'Enable', '1–100', 'Không', 'Trống lưu 1. Nhỏ hơn 1 “Không được nhỏ hơn 1”.'],
             ['9', 'Nội dung kiểm tra bảo dưỡng', 'Textbox (dòng)', 'Enable', '1–255 ký tự', 'Có', 'Mỗi dòng một hạng mục. Nút “Thêm danh mục kiểm tra bảo dưỡng” thêm dòng; thùng rác xóa dòng.'],
             ['10', 'ĐVT', 'Dropdown (dòng)', 'Enable', 'Danh mục đơn vị tính đang hoạt động', 'Có', 'ĐVT đã khóa mà dòng đang dùng vẫn hiển thị kèm 🔒.'],
             ['11', 'SL', 'Number (dòng)', 'Enable', 'Số nguyên', 'Có', ''],
             ['12', 'Cấp bảo dưỡng', 'Dropdown (cột)', 'Enable', 'Danh mục Cấp dịch vụ bảo dưỡng đang hoạt động', 'Có', 'Nút + thêm cột, × xóa cột (hỏi xác nhận). Mỗi cấp chỉ chọn một lần: trùng báo “Cấp bảo dưỡng này đã được chọn ở cột khác”. Cấp đã khóa không chọn được; gói cũ đang dùng cấp đã khóa vẫn hiển thị kèm 🔒. Cấp vừa bị khóa khi Lưu → “Cấp bảo dưỡng đã bị khóa hoặc không tồn tại”.'],
             ['13', 'Ghi chú kiểm tra', 'Multi-select (ô giao)', 'Enable', 'Danh mục Ghi chú kiểm tra đang hoạt động', 'Có', 'Chọn một hoặc nhiều ký hiệu. Ghi chú đã khóa không chọn được; gói cũ vẫn hiển thị kèm 🔒. Ghi chú vừa bị khóa khi Lưu → “Nội dung kiểm tra đã bị khóa hoặc không tồn tại”.'],
             ['14', 'Định mức công', 'Number (cột)', 'Enable', '≥ 0', 'Có', ''],
             ['15', 'Hệ số công nghệ', 'Number (cột)', 'Enable', '≥ 0', 'Không', ''],
             ['16', 'Giá vốn / Giá công thức', 'Number (cột)', 'Read-only', '–', '–', 'Tự tính (xem Phần 4).'],
             ['17', 'Giá bán cơ sở', 'Number (cột)', 'Enable', '≥ 0', 'Không', 'Mặc định = Giá công thức, sửa tay được.'],
             ['18', 'Gợi ý hàng hóa', 'Multi-select (cột)', 'Enable', '–', 'Không', ''],
             ['19', 'Hệ số giá bán theo công ty', 'Number (dòng)', 'Enable', '0 – 99,999,999.99', 'Không', 'Mặc định 1; dòng công ty quản lý bị khóa = 1.'],
             ['20', 'Chọn hàng hóa / Chọn nhóm hàng', 'Button', 'Enable', '–', 'Không', 'Mở popup chọn hàng hóa / nhóm hàng; hàng hóa gom theo nhóm.'],
             ['21', 'File đính kèm (PDF)', 'File', 'Enable', 'PDF, ≤ 20MB/file', 'Có', 'Nút “Thêm tài liệu”; tải lên ngay khi chọn. Thiếu “Bắt buộc phải đính kèm ít nhất 1 file PDF”.'],
             ['22', 'Nút Lưu / Lưu và tiếp tục / Quay lại', 'Button', 'Enable', '–', '–', 'Xem Dòng sự kiện.'],
         ], ui_widths=[0.6, 1.3, 0.8, 0.6, 1.1, 0.5, 2.3],
         events=[['Bấm Tạo mới', 'Click', 'After:\n– Mở trang Thêm gói bảo dưỡng với giá trị mặc định.'],
                 ['Nhập Mã gói', 'Input', 'During:\n– Tự chuyển chữ in hoa; sai định dạng báo lỗi ngay dưới ô, nhập lại đúng thì lỗi tự mất.'],
                 ['Nhập Định mức công / Hệ số công nghệ / Hệ số giá bán gói', 'Input', 'After:\n– Tính lại Giá vốn, Giá công thức, Giá bán cơ sở và Giá bán theo công ty.'],
                 ['Bấm × ở tiêu đề cột cấp', 'Click', 'After:\n– Hỏi “Xóa cột … sẽ xóa toàn bộ ghi chú và giá của cột này. Bạn có chắc chắn?” (Xác nhận / Hủy).'],
                 ['Bấm Lưu', 'Click', 'During:\n– Kiểm tra bắt buộc, định dạng, trùng Tên/Mã, file PDF.\n– Có lỗi → báo đỏ dưới ô + toast “Vui lòng kiểm tra lại dữ liệu nhập”, không thực hiện After.\nAfter:\n– Ghi gói mới (Trạng thái theo ô Trạng thái), ghi lịch sử Tạo mới.\n– Thông báo “Tạo gói bảo dưỡng thành công”, quay về danh sách.'],
                 ['Bấm Lưu và tiếp tục', 'Click', 'During:\n– Như nút Lưu.\nAfter:\n– Ghi gói, làm trắng form, ở lại trang Thêm mới.'],
                 ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách. Đã nhập → hỏi xác nhận “Thông tin chưa lưu”.']])

    # 2.4 Chỉnh sửa
    S.fr('Chỉnh sửa gói bảo dưỡng', uc='uc_fr04',
         qtc='Validate dữ liệu, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
         gioi_thieu=[
             ['Tên chức năng', 'Chỉnh sửa gói bảo dưỡng'],
             ['Mô tả', 'Sửa thông tin một gói đã có. Dùng chung form với Thêm mới.'],
             ['Tác nhân', 'Người dùng có quyền “Sửa danh mục gói bảo dưỡng”.'],
             ['Điều kiện ban đầu', 'Gói cần sửa đang ở trạng thái Hoạt động.'],
             ['Dòng sự kiện chính', '1. Người dùng bấm Sửa ở danh sách hoặc ở chân trang Chi tiết.\n2. Hệ thống mở trang “Sửa gói bảo dưỡng” với dữ liệu hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra dữ liệu, ghi thay đổi và ghi lịch sử (chỉ khi có thay đổi).\n5. Thông báo “Cập nhật gói bảo dưỡng thành công”, quay về danh sách.'],
             ['Dòng sự kiện phụ', '• Giữ nguyên Tên/Mã của chính gói → không báo trùng.\n• Gói đang dùng cấp / ghi chú kiểm tra đã bị khóa → vẫn hiện đúng tên kèm 🔒 và lưu lại được; chọn mới giá trị đã khóa thì bị chặn.\n• Bỏ cột cấp đã phát sinh báo giá dịch vụ → báo “Không thể xóa cấp dịch vụ đã được sử dụng!”, không lưu.\n• Gói đang Khóa → không có nút Sửa; mở trang Sửa từ liên kết đã lưu → báo “Gói bảo dưỡng đang bị khoá, vui lòng mở khoá trước khi sửa.” và chuyển về trang Chi tiết.\n• Gói vừa bị người khác khóa → máy chủ từ chối với “Gói bảo dưỡng đang bị khoá, vui lòng mở khoá trước khi cập nhật.”'],
             ['Yêu cầu đặc biệt', 'Chân trang: Lưu, Nhân bản, Quay lại (không có “Lưu và tiếp tục”).'],
         ],
         layout={'suffix': [' => Sửa ', ic('btn_sua')],
                 'imgs': [('42_edit_top', 'Trang Sửa gói bảo dưỡng')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
             ['1', 'Toàn bộ trường của 5 khối', 'Như 2.3', 'Enable', 'Dữ liệu hiện tại', 'Quy tắc nhập như mục 2.3.'],
             ['2', 'Trạng thái', 'Dropdown', 'Enable', 'Dữ liệu hiện tại', 'Chọn Khóa rồi Lưu cũng khóa được gói (ngoài nút Khóa riêng, xem 2.6).'],
             ['3', 'Nút Lưu', 'Button', 'Enable', 'Hiển thị', 'Ghi thay đổi rồi về danh sách.'],
             ['4', 'Nút Nhân bản', 'Button', 'Enable', 'Hiện khi có quyền Thêm', 'Mở trang Sao chép gói ở tab mới (xem 2.12).'],
             ['5', 'Nút Quay lại', 'Button', 'Enable', 'Hiển thị', 'Về nơi người dùng đi vào; hỏi xác nhận nếu có thay đổi chưa lưu.'],
         ], ui_widths=[0.6, 1.5, 0.8, 0.7, 1.2, 2.6],
         events=[['Bấm Sửa', 'Click', 'Before:\n– Gói đã Khóa thì nút không hiển thị.\nAfter:\n– Mở trang Sửa với dữ liệu hiện tại.'],
                 ['Bấm Lưu', 'Click', 'During:\n– Áp dụng quy tắc kiểm tra như 2.3; bỏ qua kiểm tra trùng với chính gói đang sửa.\n– Gói đang Khóa → từ chối, không lưu.\nAfter:\n– Ghi thay đổi; có thay đổi thì ghi 1 mốc lịch sử “Thay đổi thông tin” (đổi Trạng thái ghi “Khóa”/“Mở khóa”).\n– Thông báo “Cập nhật gói bảo dưỡng thành công”, quay về danh sách.']])

    # 2.5 Xóa
    S.fr('Xóa gói bảo dưỡng', uc='uc_fr05',
         qtc='Quy tắc Xóa, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
         gioi_thieu=[
             ['Tên chức năng', 'Xóa gói bảo dưỡng'],
             ['Mô tả', 'Xóa HẲN một gói CHƯA được sử dụng ở chứng từ nào khỏi danh mục, kèm toàn bộ nội dung kiểm tra, cấp, hàng hóa áp dụng và hệ số giá bán theo công ty. Gói đã được sử dụng không xóa được — dùng Khóa (2.6).'],
             ['Tác nhân', 'Người dùng có quyền “Xóa danh mục gói bảo dưỡng”.'],
             ['Điều kiện ban đầu', 'Gói đang Hoạt động và chưa được chọn ở chứng từ nào (báo giá dịch vụ, hợp đồng dịch vụ, phụ lục hợp đồng dịch vụ, đề nghị xuất dịch vụ, đề nghị hạch toán dịch vụ, hạch toán dịch vụ; báo giá, hợp đồng, phiếu giao việc, phiếu nhập kết quả của dịch vụ bảo hành – sửa chữa). Gói chỉ gắn hàng hóa áp dụng vẫn xóa được.'],
             ['Dòng sự kiện chính', '1. Người dùng bấm Xóa ở danh sách hoặc chân trang Chi tiết.\n2. Hệ thống hiện hộp “Xác nhận xóa”: “Bạn có chắc chắn muốn xóa gói bảo dưỡng \'<tên>\'? Hành động này không thể hoàn tác.”\n3. Người dùng bấm Xóa.\n4. Hệ thống kiểm tra lại trạng thái và tình trạng sử dụng, xóa gói cùng dữ liệu con, ghi lịch sử, thông báo “Xóa gói bảo dưỡng thành công”, nạp lại danh sách (xóa từ Chi tiết thì quay về danh sách).'],
             ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Gói đã được sử dụng / đang Khóa → nút Xóa KHÔNG hiển thị.\n• Gói vừa được chọn ở chứng từ trong lúc mở hộp (hoặc gọi thẳng chức năng xóa gói đã dùng) → máy chủ chặn, báo “Gói bảo dưỡng đang được sử dụng, không thể xóa.”, gói giữ nguyên trạng thái.\n• Gói đang Khóa (người khác vừa khóa, hoặc gọi thẳng) → báo “Gói bảo dưỡng đang bị khoá, vui lòng mở khoá trước khi cập nhật.”\n• Xóa dòng cuối của trang cuối → danh sách tự lùi về trang trước.'],
         ],
         layout={'suffix': [' => Xóa ', ic('btn_xoa')],
                 'note': 'Hộp xác nhận xóa được mở ngay trên màn hình danh sách.',
                 'imgs': [('34_delete_confirm', 'Hộp xác nhận xóa gói bảo dưỡng')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Mô tả'],
             ['1', 'Biểu tượng thùng rác', 'Icon Button', 'Trên cột Hành động / nút Xóa ở chân trang Chi tiết.'],
             ['2', 'Tiêu đề hộp xác nhận', 'Label', '“Xác nhận xóa”.'],
             ['3', 'Nội dung hộp xác nhận', 'Label', 'Nêu rõ tên gói.'],
             ['4', 'Nút Xóa', 'Button', 'Xác nhận thực hiện.'],
             ['5', 'Nút Hủy', 'Button', 'Đóng hộp, không làm gì.'],
         ], ui_widths=[0.6, 1.6, 1, 3],
         events=[['Bấm biểu tượng thùng rác', 'Click', 'Before:\n– Chỉ hiện khi có quyền Xóa, gói đang Hoạt động và chưa được sử dụng.\nAfter:\n– Hiện hộp xác nhận kèm tên gói.'],
                 ['Bấm Xóa', 'Click', 'During:\n– Gói đang Khóa → báo “Gói bảo dưỡng đang bị khoá, vui lòng mở khoá trước khi cập nhật.”, dừng.\n– Gói đã được sử dụng → báo “Gói bảo dưỡng đang được sử dụng, không thể xóa.”, dừng.\nAfter:\n– Xóa hẳn gói và dữ liệu con, ghi lịch sử, thông báo “Xóa gói bảo dưỡng thành công”, nạp lại danh sách.'],
                 ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp xác nhận, không thay đổi.']])

    # 2.6 Khóa / Mở khóa
    S.fr('Khóa / Mở khóa gói bảo dưỡng', uc='uc_fr06',
         qtc='Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
         gioi_thieu=[
             ['Tên chức năng', 'Khóa / Mở khóa gói bảo dưỡng'],
             ['Mô tả', 'Đổi trạng thái gói giữa Hoạt động và Khóa. Khóa được cả gói đang được sử dụng. Gói Khóa vẫn nằm trong danh mục nhưng không chọn được ở chứng từ mới, không sửa/xóa được.'],
             ['Tác nhân', 'Người dùng có quyền “Sửa danh mục gói bảo dưỡng”.'],
             ['Điều kiện ban đầu', 'Khóa: gói đang Hoạt động. Mở khóa: gói đang Khóa.'],
             ['Dòng sự kiện chính', 'Khóa:\n1. Người dùng bấm Khóa ở cột Hành động (gói đã được sử dụng: nút hiện thẳng; gói chưa dùng: trong nút ba chấm) hoặc ở chân trang Chi tiết.\n2. Hệ thống hỏi “Xác nhận khóa”: “Bạn có chắc chắn muốn khóa gói bảo dưỡng \'<tên>\'?”.\n3. Người dùng bấm Khóa → hệ thống đổi Trạng thái = Khóa, ghi lịch sử “Khóa”, thông báo “Khóa gói bảo dưỡng thành công”. Ở danh sách thì nạp lại bảng; ở Chi tiết thì Ở LẠI trang, chân trang đổi ngay sang Mở khóa, Nhân bản, In.\nMở khóa:\n1. Người dùng bấm Mở khóa ở danh sách hoặc chân trang Chi tiết.\n2. Hệ thống hỏi “Bạn có chắc chắn muốn mở khóa gói bảo dưỡng \'<tên>\'?”.\n3. Người dùng bấm Mở khóa → hệ thống đổi Trạng thái = Hoạt động, ghi lịch sử “Mở khóa”, thông báo “Mở khóa gói bảo dưỡng thành công” (ở Chi tiết thì ở lại trang).'],
             ['Dòng sự kiện phụ', '• Cũng khóa được bằng cách chọn Trạng thái = Khóa trong trang Sửa rồi Lưu.\n• Sau khi Khóa: nút Sửa, Xóa, Khóa biến mất; còn Mở khóa, Nhân bản, In, Lịch sử.\n• Bấm Hủy ở hộp xác nhận → không thay đổi.\n• Hai người cùng khóa / cùng mở khóa một gói → người bấm sau nhận “Trạng thái đã bị thay đổi. Vui lòng load lại trang”, không ghi lịch sử trùng.'],
         ],
         layout={'suffix': [' => Khóa ', ic('btn_khoa', alt='Khóa'), ' / Mở khóa ', ic('btn_mokhoa')],
                 'imgs': [('54_rowmenu_lock', 'Nút Khóa trong nút ba chấm của gói chưa được sử dụng'),
                          ('55_lock_confirm', 'Hộp xác nhận khóa gói bảo dưỡng'),
                          ('56_detail_lock', 'Nút Khóa ở chân trang màn Chi tiết'),
                          ('57_detail_locked', 'Màn Chi tiết sau khi khóa — chân trang còn Mở khóa, Nhân bản, In'),
                          ('43_edit_lock', 'Khóa gói bằng ô Trạng thái trong trang Sửa'),
                          ('45_unlock_confirm', 'Hộp xác nhận mở khóa gói bảo dưỡng')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Mô tả'],
             ['1', 'Nút Khóa', 'Icon Button / Button', 'Hiện trên dòng gói Hoạt động (kể cả đã được sử dụng) và chân trang Chi tiết (màu cam) khi có quyền Sửa.'],
             ['2', 'Nút Mở khóa', 'Icon Button / Button', 'Hiện trên dòng gói Khóa và chân trang Chi tiết khi có quyền Sửa.'],
             ['3', 'Hộp xác nhận', 'Modal', 'Tiêu đề “Xác nhận khóa” / “Xác nhận mở khóa”, nêu tên gói; nút Khóa / Mở khóa và Hủy.'],
             ['4', 'Ô Trạng thái (trang Sửa)', 'Dropdown', 'Chọn Khóa rồi Lưu cũng khóa được gói.'],
             ['5', 'Cột Trạng thái', 'Badge', 'Hoạt động (xanh) / Khóa (đỏ).'],
         ], ui_widths=[0.6, 1.6, 1.2, 3],
         events=[['Bấm Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên gói.'],
                 ['Xác nhận Khóa', 'Click', 'During:\n– Gói đã ở trạng thái Khóa (người khác vừa khóa) → báo “Trạng thái đã bị thay đổi. Vui lòng load lại trang”, dừng.\nAfter:\n– Trạng thái = Khóa, KHÔNG xóa dữ liệu, ghi lịch sử “Khóa”, cập nhật cột Trạng thái và các nút (ở Chi tiết thì ở lại trang).'],
                 ['Xác nhận Mở khóa', 'Click', 'During:\n– Gói đã Hoạt động (người khác vừa mở) → báo “Trạng thái đã bị thay đổi. Vui lòng load lại trang”, dừng.\nAfter:\n– Trạng thái = Hoạt động, ghi lịch sử “Mở khóa”, cập nhật cột Trạng thái và các nút.'],
                 ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.']])

    # 2.7 Lịch sử
    S.fr('Xem lịch sử thay đổi',
         qtc='Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục gói bảo dưỡng.',
         gioi_thieu=[
             ['Tên chức năng', 'Xem lịch sử thay đổi'],
             ['Mô tả', 'Liệt kê các lần thay đổi của một gói kèm giá trị cũ → mới, người thực hiện và thời điểm.'],
             ['Tác nhân', ACT_ALL],
             ['Điều kiện ban đầu', 'Gói cần xem đang có trong danh sách.'],
             ['Dòng sự kiện chính', '1. Người dùng chọn Lịch sử trong nút ba chấm ở danh sách, hoặc bấm “Xem lịch sử” ở màn Chi tiết.\n2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <mã> - <tên>” (hoặc khối Lịch sử cuối trang Chi tiết).\n3. Các mốc hiển thị mới nhất ở trên cùng.'],
             ['Dòng sự kiện phụ', '• Gói chưa phát sinh thao tác → “Chưa có lịch sử thao tác nào.”\n• Lưu mà không thay đổi gì → không phát sinh mốc mới.'],
             ['Yêu cầu đặc biệt', 'Trường được theo dõi: Mã, Tên, Công ty quản lý, Định mức đàm phán giá (%), VAT (%), Hệ số giá bán gói, Trạng thái, Ghi chú; và 5 bảng con: nội dung kiểm tra bảo dưỡng, cấp dịch vụ, công ty áp dụng (hệ số), hàng hóa gợi ý/áp dụng, file đính kèm.'],
         ],
         layout={'suffix': [' => Lịch sử'],
                 'imgs': [('52_history_lock', 'Cửa sổ Lịch sử thay đổi của gói bảo dưỡng'),
                          ('53_history_filter', 'Bộ lọc trong cửa sổ Lịch sử')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Giá trị ban đầu', 'Mô tả'],
             ['1', 'Tiêu đề cửa sổ', 'Label', 'Lịch sử thay đổi', 'Kèm mã và tên gói.'],
             ['2', 'Bộ lọc', 'Dropdown / Date', 'Trống', 'Loại hành động (Tạo mới / Thay đổi thông tin / Thay đổi trạng thái), Người thực hiện, Từ ngày – Đến ngày; nút Làm mới.'],
             ['3', 'Thông tin thay đổi', 'Text', 'Theo dữ liệu', '- Thời điểm dd/mm/yyyy hh:mm.\n- Loại: Tạo mới, Thay đổi thông tin, Khóa, Mở khóa.\n- Người thực hiện kèm phòng ban.\n- Giá trị cũ → mới cho từng trường; bảng con liệt kê dòng thêm/sửa/xóa.'],
             ['4', 'Trạng thái rỗng', 'Label', 'Ẩn', '“Chưa có lịch sử thao tác nào.”'],
             ['5', 'Nút Đóng', 'Button', 'Hiển thị', 'Đóng cửa sổ.'],
         ], ui_widths=[0.6, 1.3, 1, 1, 3],
         events=[['Mở lịch sử', 'Click', 'After:\n– Nạp danh sách thay đổi, mới nhất trước.'],
                 ['Đổi bộ lọc', 'Change', 'After:\n– Nạp lại theo tiêu chí.'],
                 ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ; danh sách phía sau giữ nguyên bộ lọc và trang.']])

    # 2.8 Import
    S.fr('Import file gói bảo dưỡng', uc='uc_fr08',
         qtc='Quy tắc Import file, Validate dữ liệu, Thông báo và Quy định chung về danh mục. Chỉ bổ sung mapping/validation riêng của Danh mục gói bảo dưỡng.',
         gioi_thieu=[
             ['Tên chức năng', 'Import file gói bảo dưỡng'],
             ['Mô tả', 'Thêm nhiều gói cùng lúc từ file Excel mẫu 5 sheet (gói, cấp, nội dung kiểm tra, hệ số công ty, hàng hóa). Có bước Validate trước khi ghi.'],
             ['Tác nhân', 'Người dùng có quyền “Thêm danh mục gói bảo dưỡng”.'],
             ['Điều kiện ban đầu', 'Đang ở màn Danh mục gói bảo dưỡng và đã chuẩn bị file theo mẫu.'],
             ['Dòng sự kiện chính', '1. Bấm Import Excel.\n2. Bấm Tải file mẫu (Mau_import_goi_bao_duong.xlsx), điền dữ liệu từ dòng 3 (dòng 2 là dòng gợi ý).\n3. Bấm Chọn file Excel rồi Load lên bảng; dữ liệu hiện theo từng tab sheet, ô Tổng = số gói.\n4. Bấm Validate; hệ thống kiểm tra từng dòng như quy tắc Thêm mới (mục 2.3) và quy tắc riêng ở mục 2.8.6, đánh dấu dòng lỗi, khóa dòng hợp lệ.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi rồi Validate lại.\n6. Bấm Import; hệ thống kiểm tra lại toàn bộ và ghi các gói hợp lệ, báo “Import thành công N gói bảo dưỡng.”, đóng cửa sổ, nạp lại danh sách.'],
             ['Dòng sự kiện phụ', '• File không phải .xlsx/.xls → “Vui lòng chọn file .xlsx hoặc .xls”.\n• Thiếu sheet / thiếu cột → “File không đúng mẫu: thiếu sheet …” / “Sheet … thiếu cột: …”.\n• Sheet 1 không có dòng → “Sheet “1. Gói bảo dưỡng” không có dòng dữ liệu nào.”\n• Còn dòng lỗi → nút Import không bấm được.\n• Dữ liệu đổi giữa Validate và Import → “Import thành công x/y gói bảo dưỡng. z gói thất bại.”\n• Đóng cửa sổ khi đã tải dữ liệu → hỏi “Bạn có thông tin chưa lưu…”.'],
             ['Yêu cầu đặc biệt', 'Validate không ghi dữ liệu. Gói import luôn ở trạng thái Hoạt động, mã tự in hoa, VAT trống lưu 0, Hệ số giá bán trống lưu 1. Tên danh mục so khớp không phân biệt hoa thường. File Excel không nhập file PDF — bổ sung PDF sau ở trang Sửa.'],
         ],
         layout={'suffix': [' => Import Excel ', ic('btn_import')],
                 'note': 'Cửa sổ Import được mở ngay trên màn hình danh sách.',
                 'imgs': [('07_import_open', 'Cửa sổ Import gói bảo dưỡng khi vừa mở'),
                          ('09_import_validated', 'Kết quả Validate — dòng lỗi nêu rõ lý do'),
                          ('10_import_tab3', 'Lỗi ở sheet 3. Nội dung kiểm tra'),
                          ('11_import_ok', 'Tất cả gói hợp lệ — nút Import bấm được')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả'],
             ['1', 'Nút Chọn file Excel', 'Button', 'Enable', 'Có', 'Chưa chọn', 'Chọn file .xlsx/.xls; tên file hiện cạnh nút.'],
             ['2', 'Nút Tải file mẫu', 'Button', 'Enable', '–', 'Hiển thị', 'Tải Mau_import_goi_bao_duong.xlsx (5 sheet, cột * là bắt buộc).'],
             ['3', 'Nút Load lên bảng', 'Button', 'Enable/Disable', '–', 'Mờ khi chưa chọn file', 'Đọc file, đổ dữ liệu lên bảng xem trước.'],
             ['4', 'Nút Validate', 'Button', 'Enable/Disable', '–', 'Mờ khi chưa có dữ liệu', 'Kiểm tra từng dòng, khóa dòng hợp lệ.'],
             ['5', 'Nút Import', 'Button', 'Enable/Disable', '–', 'Mờ', 'Chỉ bấm được khi đã Validate, 0 dòng lỗi và ≥ 1 gói hợp lệ.'],
             ['6', 'Ô Tổng / Hợp lệ / Lỗi', 'Label', 'Read-only', '–', 'Tổng: 0', 'Tổng = số gói; Hợp lệ / Lỗi hiện sau Validate.'],
             ['7', 'Tab sheet', 'Tab', 'Enable', '–', 'Tab 1', '5 tab, mỗi tab ghi số dòng và số lỗi (màu đỏ).'],
             ['8', 'Bảng xem trước', 'Table/Grid', 'Enable', '–', 'Trống', 'Sửa trực tiếp được ở dòng lỗi; lý do lỗi ghi dưới dòng.'],
             ['9', 'Nút Bỏ dòng lỗi', 'Button', 'Enable', '–', 'Hiển thị', 'Loại dòng lỗi (kèm dòng con của gói bị bỏ); cần Validate lại.'],
             ['10', 'Nút Xoá trạng thái validate', 'Button', 'Enable', '–', 'Hiển thị', 'Bỏ khóa dòng hợp lệ và bỏ thông báo lỗi.'],
             ['11', 'Nút Làm mới / Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Làm mới: xóa dữ liệu đang có. Đóng: đóng cửa sổ.'],
         ], ui_widths=[0.6, 1.4, 0.7, 0.8, 0.5, 1, 2.4],
         events=[['Bấm Load lên bảng', 'Click', 'During:\n– Kiểm tra định dạng file, đủ 5 sheet và các cột.\nAfter:\n– Đổ dữ liệu lên bảng, cập nhật ô Tổng.'],
                 ['Bấm Validate', 'Click', 'During:\n– Kiểm tra từng dòng theo quy tắc mục 2.3 và 2.8.4; dòng con lỗi thì gói cha cũng lỗi (“Sheet … dòng N có lỗi”).\nAfter:\n– Có lỗi: tô đỏ dòng lỗi + lý do, thông báo “Còn N dòng lỗi (xem tab có dấu đỏ)…”.\n– Không lỗi: “Tất cả N gói bảo dưỡng đã hợp lệ. Có thể import ngay.”, nút Import sáng.\n– KHÔNG ghi dữ liệu.'],
                 ['Bấm Bỏ dòng lỗi', 'Click', 'After:\n– “Đã bỏ N dòng lỗi (kèm dòng con của gói bị bỏ). Hãy bấm Validate lại.”'],
                 ['Bấm Import', 'Click', 'During:\n– Máy chủ kiểm tra lại toàn bộ dòng.\nAfter:\n– Ghi gói hợp lệ (Hoạt động, người tạo = người import), báo kết quả, đóng cửa sổ, nạp lại danh sách.']])
    w.raw('sub', '2.8.6 Quy tắc kiểm tra riêng của file Import')
    w.table([
        ['Sheet', 'Quy tắc / thông báo lỗi'],
        ['1. Gói bảo dưỡng', 'Mã gói, Tên gói, Công ty quản lý bắt buộc (“… không được để trống”); tối đa 255 ký tự; Mã “Chỉ gồm chữ không dấu, số, dấu - và _”; trùng trong file “… bị trùng với dòng N trong file”; trùng hệ thống “… đã tồn tại trong hệ thống”; Công ty “Công ty quản lý “X” không có trong danh mục”; VAT 0–100, Định mức đàm phán giá 0–99, Hệ số giá bán 1–100 (“… phải là số” / “… tối đa …” / “… không được nhỏ hơn …”); Ghi chú tối đa 255 ký tự; phải có ≥ 1 dòng hợp lệ ở sheet 2 và sheet 3.'],
        ['2. Cấp bảo dưỡng', 'Cấp bảo dưỡng bắt buộc, phải có trong danh mục và đang Hoạt động (“Cấp bảo dưỡng “X” không có trong danh mục hoặc đã bị khóa”), không trùng trong cùng gói (“Cấp bảo dưỡng này đã khai ở dòng N”); Định mức công bắt buộc ≥ 0; Hệ số công nghệ, Giá bán cơ sở ≥ 0.'],
        ['3. Nội dung kiểm tra', 'STT hạng mục bắt buộc; Nội dung, ĐVT, SL bắt buộc ở dòng đầu của hạng mục, các dòng sau để trống hoặc ghi giống dòng đầu; ĐVT phải có trong danh mục đang hoạt động; Cấp phải đã khai ở sheet 2 cho gói đó, không trùng trong hạng mục; Ghi chú kiểm tra bắt buộc, ghi TÊN đầy đủ, nhiều giá trị ngăn bằng dấu ; và phải có trong danh mục, đang Hoạt động (“Ghi chú kiểm tra “X” không có trong danh mục hoặc đã bị khóa”); hạng mục phải khai đủ các cấp của gói (“Hạng mục “X” chưa khai cấp: …”).'],
        ['4. Hệ số theo công ty', 'Công ty bắt buộc, phải có trong danh mục, không trùng; Hệ số bắt buộc, 0 – 99,999,999.99.'],
        ['5. Hàng hoá', 'Mã hàng bắt buộc và phải có trong danh mục hàng hóa; Nhóm hàng bắt buộc và phải có trong danh mục; không trùng hàng trong gói.'],
        ['Sheet 2–5', 'Mã gói phải có ở sheet 1 (“Mã gói “X” không có ở sheet “1. Gói bảo dưỡng””).'],
    ], widths=[1.2, 4])

    # 2.9 Xuất Excel
    S.fr('Xuất danh sách ra Excel', uc='uc_fr09',
         qtc='Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của Danh mục gói bảo dưỡng.',
         gioi_thieu=[
             ['Tên chức năng', 'Xuất danh sách gói bảo dưỡng ra Excel'],
             ['Mô tả', 'Xuất danh sách gói ra file Excel, cho phép chọn trường và thứ tự cột.'],
             ['Tác nhân', ACT_ALL],
             ['Điều kiện ban đầu', 'Đang ở màn Danh mục gói bảo dưỡng.'],
             ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiển thị trên bảng.\n3. Người dùng tích chọn và kéo ☰ để sắp thứ tự.\n4. Bấm Xuất file; hệ thống tải file Danh_sach_goi_bao_duong.xlsx, báo “Xuất Excel thành công”.'],
             ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Bấm Đóng → không xuất gì.\n• Lỗi → “Lỗi khi xuất Excel”.'],
             ['Yêu cầu đặc biệt', 'File chứa TOÀN BỘ gói của danh mục (xếp Ngày tạo giảm dần), KHÔNG áp bộ lọc trên màn hình. Luôn có thêm cột “Giá gói bảo dưỡng” (mỗi cấp một dòng “Cấp: 1,234,000”). File có logo, tiêu đề “Danh sách gói bảo dưỡng” và khối ký “Người lập”. Chỉ xuất Excel, không xuất PDF.'],
         ],
         layout={'suffix': [' => Xuất Excel ', ic('btn_xuatexcel')],
                 'imgs': [('06_export', 'Cửa sổ Chọn trường xuất file')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
             ['1', 'Danh sách trường', 'Checkbox chọn nhiều', 'Enable', 'Tích sẵn cột đang hiển thị', '6 trường: Mã, Tên gói bảo dưỡng, Người tạo, Ngày tạo, Trạng thái, Công ty quản lý. Kéo ☰ đổi thứ tự.'],
             ['2', 'Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', 'Hiển thị', 'Tích / bỏ tích toàn bộ.'],
             ['3', 'Dòng “Đang chọn a/6 trường”', 'Label', 'Read-only', '–', 'Số trường đang chọn.'],
             ['4', 'Nút Xuất file', 'Button', 'Enable/Disable', 'Mờ khi chưa chọn trường', 'Sinh file và tải về.'],
             ['5', 'Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'],
         ], ui_widths=[0.6, 1.5, 1, 0.8, 1.2, 2.6],
         events=[['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn cột đang hiển thị.'],
                 ['Chọn / bỏ / kéo trường', 'Change', 'During:\n– Ghi nhận thứ tự để quyết định thứ tự cột trong file.'],
                 ['Bấm Xuất file', 'Click', 'After:\n– Tải file Danh_sach_goi_bao_duong.xlsx; ô số là số thật, định dạng 1,234,567.']])

    # 2.10 Chi tiết
    S.fr('Xem chi tiết gói bảo dưỡng', uc='uc_fr10',
         qtc='Màn Xem chi tiết và Phân quyền.',
         gioi_thieu=[
             ['Tên chức năng', 'Xem chi tiết gói bảo dưỡng'],
             ['Mô tả', 'Trang “Chi tiết gói bảo dưỡng: <mã>” hiển thị đủ 5 khối ở chế độ chỉ đọc, kèm khối Lịch sử.'],
             ['Tác nhân', ACT_ALL],
             ['Điều kiện ban đầu', 'Gói cần xem có trong danh sách (Hoạt động hoặc Khóa).'],
             ['Dòng sự kiện chính', '1. Người dùng bấm Mã gói ở danh sách.\n2. Hệ thống mở trang Chi tiết (mở được ở tab mới).'],
             ['Dòng sự kiện phụ', '• Bấm tên file ở khối File đính kèm → mở PDF.\n• Chân trang hiện nút giống cột Hành động của gói đó: Sửa, Xóa, Khóa, Mở khóa (theo điều kiện 2.1), In, Nhân bản, Quay lại; nút “Xem lịch sử” mở khối Lịch sử.\n• Khóa / Mở khóa ở chân trang thì ở lại trang Chi tiết; Xóa thì quay về danh sách.'],
         ],
         layout={
                 'imgs': [('40b_detail_active_candelete', 'Trang Chi tiết gói bảo dưỡng'),
                          ('49_detail_history', 'Khối Lịch sử ở cuối trang Chi tiết')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
             ['1', 'Mã (ô trên danh sách)', 'Link', 'Enable', 'Hiển thị', 'Bấm vào mã để mở TRANG Chi tiết (mở được ở tab mới). Không có nút Xem riêng ở cột Hành động.'],
             ['2', 'Tiêu đề trang', 'Label', 'Read-only', '“Chi tiết gói bảo dưỡng: <mã>”', 'Chưa nạp xong dữ liệu thì hiện “Chi tiết gói bảo dưỡng”.'],
             ['3', 'Khối Thông tin chung', 'Section', 'Read-only', 'Dữ liệu hiện tại', 'Ô mờ, không gõ được: Tên gói bảo dưỡng, Mã gói bảo dưỡng, Định mức đàm phán giá (%), VAT (%), Công ty quản lý gói bảo dưỡng, Trạng thái, Ghi chú, Hệ số giá bán gói bảo dưỡng.'],
             ['4', 'Khối Danh mục kiểm tra bảo dưỡng định kỳ', 'Table', 'Read-only', 'Dữ liệu hiện tại', 'Ma trận Nội dung kiểm tra bảo dưỡng × Cấp bảo dưỡng (ĐVT, SL, ghi chú kiểm tra ở từng ô giao) kèm các dòng Định mức công, Hệ số công nghệ, Giá vốn, Giá công thức, Giá bán cơ sở, Gợi ý hàng hoá. Cấp / ghi chú / ĐVT đã khóa vẫn hiện đúng tên kèm 🔒. Không có nút thêm dòng, thêm / xóa cột.'],
             ['5', 'Khối Giá vốn theo công ty', 'Table', 'Read-only', 'Dữ liệu hiện tại', 'STT, Công ty, Đơn giá công, Giá vốn theo từng cấp, Hệ số giá bán, Giá bán theo công ty; số dạng 1,234,567.'],
             ['6', 'Khối Áp dụng cho hàng hóa', 'Table', 'Read-only', 'Dữ liệu hiện tại', 'Hàng hóa gom theo dòng “Nhóm hàng: <tên>”; cột STT, Hình ảnh, Tên hàng, Mã hàng. Không có nút Chọn hàng hóa / Chọn nhóm hàng / xóa. Chưa có dòng → “Chưa chọn hàng hóa áp dụng”.'],
             ['7', 'Khối File đính kèm (PDF)', 'Table', 'Read-only', 'Dữ liệu hiện tại', 'Mỗi file có nút Xem trước và Tải xuống; không có Thêm tài liệu / Thay đổi / Xóa. Chưa có file → “Chưa có tài liệu nào.”'],
             ['8', 'Khối Lịch sử', 'Section', 'Enable', 'Thu gọn', 'Tiêu đề “Lịch sử”. “Xem lịch sử” mở khối và nạp dữ liệu, “Thu gọn” đóng, “Làm mới” nạp lại. Nội dung, bộ lọc giống cửa sổ Lịch sử thay đổi (mục 2.7).'],
             ['9', 'Nút Sửa', 'Button', 'Enable', 'Hiện khi có quyền Sửa và gói đang Hoạt động', 'Mở trang Sửa (mục 2.4).'],
             ['10', 'Nút In', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ xem trước phiếu kiểm tra (mục 2.13).'],
             ['11', 'Nút Nhân bản', 'Button', 'Enable', 'Hiện khi có quyền Thêm', 'Mở trang Sao chép gói bảo dưỡng ở TAB MỚI (mục 2.12).'],
             ['12', 'Nút Xóa (đỏ)', 'Button', 'Enable', 'Hiện khi có quyền Xóa, gói đang Hoạt động và chưa được sử dụng', 'Xóa hẳn gói (mục 2.5).'],
             ['13', 'Nút Khóa (cam) / Mở khóa (xanh lá)', 'Button', 'Enable', 'Theo trạng thái, cần quyền Sửa', 'Đổi trạng thái gói (mục 2.6).'],
             ['14', 'Nút Quay lại', 'Button', 'Enable', 'Hiển thị', 'Về màn danh sách.'],
         ], ui_widths=[0.6, 1.5, 0.8, 0.7, 1.3, 2.6],
         events=[['Bấm Mã gói ở danh sách', 'Click', 'During:\n– Nạp dữ liệu gói; lỗi → “Lỗi khi tải dữ liệu gói bảo dưỡng” và quay lại.\nAfter:\n– Mở trang Chi tiết, mọi ô chỉ đọc (gói đang Khóa vẫn xem được); chân trang hiện đúng các nút như cột Hành động của gói đó.'],
                 ['Bấm Xem trước / Tải xuống ở khối File đính kèm', 'Click', 'After:\n– Mở / tải file PDF đã đính kèm.'],
                 ['Bấm Xem lịch sử / Thu gọn', 'Click', 'After:\n– Mở khối Lịch sử và nạp các mốc thay đổi (mới nhất trên cùng) / thu gọn khối.'],
                 ['Bấm Sửa / In / Nhân bản / Xóa / Khóa / Mở khóa ở chân trang', 'Click', 'After:\n– Xử lý như thao tác cùng tên ở danh sách (mục 2.4, 2.13, 2.12, 2.5, 2.6).\n– Khóa / Mở khóa xong: ở lại trang, chân trang đổi nút theo trạng thái mới. Xóa xong: quay về danh sách. Nhân bản: mở tab mới, trang Chi tiết giữ nguyên.'],
                 ['Bấm Quay lại', 'Click', 'After:\n– Về màn danh sách.']])

    # 2.11 Tuỳ chỉnh cột
    S.fr('Tùy chỉnh cột hiển thị',
         qtc='Tùy chỉnh cột.',
         gioi_thieu=[
             ['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
             ['Mô tả', 'Bật/tắt và sắp xếp thứ tự cột của bảng danh sách; cấu hình lưu riêng theo người dùng.'],
             ['Tác nhân', ACT_ALL],
             ['Yêu cầu đặc biệt', 'Cột STT, Mã, Hành động bị khóa (không tắt, không kéo). Mặc định ẩn: Công ty quản lý gói bảo dưỡng, Người cập nhật, Ngày cập nhật.'],
         ],
         layout={'suffix': [' => Cấu hình cột ', ic('btn_cauhinhcot')],
                 'imgs': [('05_colcfg', 'Cửa sổ Tuỳ chỉnh cột')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
             ['1', 'Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', 'Hiển thị', 'Nút cuối thanh công cụ của bảng; rê chuột hiện “Cấu hình cột hiển thị”. Mở cửa sổ “Tuỳ chỉnh cột”.'],
             ['2', 'Danh sách cột', 'Checkbox chọn nhiều', 'Enable', 'Theo cấu hình đã lưu của người dùng', 'Liệt kê đủ 10 cột: STT, Mã, Tên gói bảo dưỡng, Công ty quản lý gói bảo dưỡng, Người cập nhật, Ngày cập nhật, Người tạo, Ngày tạo, Trạng thái, Hành động. Tích = hiện, bỏ tích = ẩn. Lần đầu hiện: STT, Mã, Tên gói bảo dưỡng, Người tạo, Ngày tạo, Trạng thái, Hành động.'],
             ['3', 'Cột bắt buộc', 'Checkbox', 'Disable', 'Luôn tích', 'STT, Mã, Hành động: chữ xám, có biểu tượng ổ khóa (“Cột bắt buộc — không thể ẩn hoặc đổi vị trí”), không bỏ tích và không kéo được.'],
             ['4', 'Biểu tượng ☰', 'Drag handle', 'Enable', 'Hiển thị', 'Kéo thả để đổi thứ tự các cột không bắt buộc.'],
             ['5', 'Nút Lưu', 'Button', 'Enable', 'Hiển thị', 'Áp dụng ngay lên bảng và lưu cấu hình theo TÀI KHOẢN người dùng (đăng nhập máy khác vẫn giữ, không ảnh hưởng người khác). Bộ cột này cũng là các trường tích sẵn khi Xuất Excel.'],
             ['6', 'Nút Đóng / biểu tượng ×', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ, bỏ các thay đổi chưa Lưu.'],
         ], ui_widths=[0.6, 1.5, 1, 0.8, 1.3, 2.5],
         events=[['Bấm biểu tượng Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ “Tuỳ chỉnh cột” với cấu hình cột đang áp dụng.'],
                 ['Tích / bỏ tích, kéo thả cột', 'Change / Drag', 'During:\n– Cột bắt buộc không bỏ tích, không kéo được.\n– Chưa áp dụng lên bảng cho tới khi bấm Lưu.'],
                 ['Bấm Lưu', 'Click', 'After:\n– Bảng hiện / ẩn và sắp cột theo lựa chọn ngay.\n– Lưu cấu hình riêng cho tài khoản, báo “Cập nhật thành công” (lỗi lưu → “Thao tác thất bại”).'],
                 ['Bấm Đóng / biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ, danh sách cột trở về cấu hình đang áp dụng.']])

    # 2.12 Nhân bản
    S.fr('Nhân bản gói bảo dưỡng', uc='uc_fr12',
         qtc='Màn Thêm mới, Validate dữ liệu và Thông báo.',
         gioi_thieu=[
             ['Tên chức năng', 'Nhân bản gói bảo dưỡng'],
             ['Mô tả', 'Tạo gói mới từ dữ liệu của một gói có sẵn.'],
             ['Tác nhân', 'Người dùng có quyền “Thêm danh mục gói bảo dưỡng”.'],
             ['Điều kiện ban đầu', 'Gói nguồn có trong danh sách (Hoạt động hoặc Khóa).'],
             ['Dòng sự kiện chính', '1. Người dùng bấm Nhân bản ở danh sách (cùng tab) hoặc ở chân trang Chi tiết / Sửa (tab mới).\n2. Hệ thống mở trang “Sao chép gói bảo dưỡng” điền sẵn toàn bộ dữ liệu gói nguồn (kể cả hàng hóa và file đính kèm), hiện dòng nhắc “Đang sao chép từ gói <tên> — hãy đổi tên/mã trước khi lưu.”\n3. Người dùng đổi Tên, Mã và bấm Lưu.\n4. Hệ thống tạo gói mới ở trạng thái Hoạt động, gói nguồn không đổi.'],
             ['Dòng sự kiện phụ', '• Không đổi Tên/Mã → báo “Đã tồn tại”.\n• Không có nút “Lưu và tiếp tục”.'],
         ],
         layout={'suffix': [' => Nhân bản ', ic('btn_nhanban')],
                 'imgs': [('46_copy_top', 'Trang Sao chép gói bảo dưỡng')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả'],
             ['1', 'Nút Nhân bản', 'Icon Button / Button', 'Enable', '–', '–', 'Hiện khi có quyền Thêm', 'Ở cột Hành động (hiện cả với gói đang Khóa; mở ngay trong tab hiện tại) và ở chân trang Chi tiết / Sửa (mở TAB MỚI).'],
             ['2', 'Tiêu đề trang', 'Label', 'Read-only', '–', '–', '“Sao chép gói bảo dưỡng”', 'Trang Thêm mới được điền sẵn từ gói nguồn.'],
             ['3', 'Dòng nhắc sao chép', 'Label', 'Read-only', '–', '–', 'Hiển thị', '“Đang sao chép từ gói <tên gói nguồn> — hãy đổi tên/mã trước khi lưu.” ở đầu trang, kèm thông báo cùng nội dung khi vừa mở.'],
             ['4', 'Tên gói bảo dưỡng / Mã gói bảo dưỡng', 'Textbox', 'Enable', 'Như mục 2.3', 'Có', 'Tên / Mã của gói nguồn', 'Phải đổi: giữ nguyên thì báo “Đã tồn tại”. Mã tự in hoa khi gõ.'],
             ['5', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động', 'Mặc định Hoạt động dù gói nguồn đang Khóa; đổi được sang Khóa trước khi lưu.'],
             ['6', 'Các trường, bảng còn lại', 'Như mục 2.3', 'Enable', 'Như mục 2.3', 'Như mục 2.3', 'Dữ liệu của gói nguồn', 'Thông tin chung, ma trận nội dung kiểm tra × cấp, Giá vốn theo công ty (hệ số giá bán), Áp dụng cho hàng hóa, File đính kèm (PDF) — sửa được như Thêm mới.'],
             ['7', 'Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tạo gói MỚI; gói nguồn không đổi. Trang Sao chép KHÔNG có nút Lưu và tiếp tục.'],
             ['8', 'Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách; đã sửa dở thì hỏi “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại).'],
         ], ui_widths=[0.5, 1.3, 0.8, 0.7, 0.9, 0.6, 1.1, 2.2],
         events=[['Bấm Nhân bản', 'Click', 'Before:\n– Không có quyền Thêm thì nút không hiển thị.\nAfter:\n– Mở trang “Sao chép gói bảo dưỡng” (từ danh sách: cùng tab; từ Chi tiết / Sửa: tab mới), nạp toàn bộ dữ liệu gói nguồn, Trạng thái = Hoạt động, hiện dòng nhắc đổi tên/mã.'],
                 ['Bấm Lưu', 'Click', 'During:\n– Kiểm tra như Thêm mới (mục 2.3); Tên / Mã chưa đổi → “Đã tồn tại”, không lưu.\n– Có lỗi → báo đỏ dưới ô + “Vui lòng kiểm tra lại dữ liệu nhập”.\nAfter:\n– Tạo gói mới, ghi lịch sử Tạo mới cho gói mới; gói nguồn giữ nguyên.\n– Thông báo “Tạo gói bảo dưỡng thành công”, quay về danh sách.'],
                 ['Bấm Quay lại', 'Click', 'After:\n– Chưa sửa gì → về danh sách. Đã sửa → hỏi xác nhận “Thông tin chưa lưu”.']])

    # 2.13 In
    S.fr('In phiếu kiểm tra bảo dưỡng', uc='uc_fr13',
         qtc='Quy tắc In.',
         gioi_thieu=[
             ['Tên chức năng', 'In phiếu Danh mục kiểm tra bảo dưỡng định kỳ'],
             ['Mô tả', 'Xem trước và in phiếu kiểm tra của một gói.'],
             ['Tác nhân', ACT_ALL],
             ['Dòng sự kiện chính', '1. Người dùng chọn In trong nút ba chấm ở danh sách, hoặc bấm In ở chân trang Chi tiết.\n2. Hệ thống mở cửa sổ “Xem trước gói bảo dưỡng <mã>”.\n3. Bấm In để mở hộp thoại in của trình duyệt.'],
             ['Yêu cầu đặc biệt', 'Phiếu gồm: logo + thông tin công ty; “DANH MỤC KIỂM TRA BẢO DƯỠNG ĐỊNH KỲ”, “TÊN DỊCH VỤ: <tên in hoa>”; bảng STT, Nội dung kiểm tra, SL, các cột cấp, Kiểm tra (Có/Không), Ghi chú; Ghi chú của gói, bảng giải thích ký hiệu, chỗ ký Kỹ thuật viên / Khách hàng. Gói chưa có nội dung kiểm tra vẫn in được.'],
         ],
         layout={'suffix': [' => In'],
                 'imgs': [('51_print', 'Cửa sổ xem trước phiếu kiểm tra bảo dưỡng')]},
         ui=[['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
             ['1', 'Mục In (cột Hành động)', 'Button', 'Enable', 'Hiển thị', 'Luôn hiện, không cần quyền riêng, kể cả gói đang Khóa; nằm trong nút ba chấm khi dòng có từ 4 thao tác.'],
             ['2', 'Nút In (chân trang Chi tiết)', 'Button', 'Enable', 'Hiển thị', 'In phiếu của gói đang xem.'],
             ['3', 'Tiêu đề cửa sổ xem trước', 'Label', 'Read-only', 'Theo nơi bấm', '“Xem trước gói bảo dưỡng <mã>” khi mở từ danh sách; “Xem trước gói bảo dưỡng” khi mở từ trang Chi tiết.'],
             ['4', 'Nút In (trong cửa sổ)', 'Button', 'Enable / Disable', 'Mờ khi đang tải', 'Mở hộp thoại in của trình duyệt.'],
             ['5', 'Tờ giấy xem trước', 'Khung A4 dọc', 'Read-only', 'Theo dữ liệu', 'Mẫu in “Danh mục kiểm tra bảo dưỡng”: logo + thông tin công ty; “DANH MỤC KIỂM TRA BẢO DƯỠNG ĐỊNH KỲ”, “TÊN DỊCH VỤ: <tên in hoa>”; bảng STT, Nội dung kiểm tra, SL, các cột cấp, Kiểm tra (Có / Không), Ghi chú; Ghi chú của gói, bảng giải thích ký hiệu, chỗ ký Kỹ thuật viên / Khách hàng.'],
             ['6', 'Dòng thông báo', 'Label', 'Read-only', 'Ẩn', '“Đang tải dữ liệu in…”; lỗi: “Không có dữ liệu để in”, “Không tải được dữ liệu in” hoặc “Không tìm thấy mẫu in "Danh mục kiểm tra bảo dưỡng"”.'],
             ['7', 'Biểu tượng ×', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ xem trước.'],
         ], ui_widths=[0.6, 1.5, 1, 0.8, 1.2, 2.6],
         events=[['Chọn In ở cột Hành động / bấm In ở chân trang Chi tiết', 'Click', 'During:\n– Máy chủ dựng phiếu từ mẫu in “Danh mục kiểm tra bảo dưỡng” với dữ liệu hiện tại của gói (gói chưa có nội dung kiểm tra vẫn in được).\nAfter:\n– Mở cửa sổ xem trước khổ dọc; lỗi → hiện câu lỗi thay cho tờ giấy.'],
                 ['Bấm In trong cửa sổ', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt với đúng nội dung tờ giấy.'],
                 ['Bấm biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ; danh sách / trang Chi tiết giữ nguyên.']])

    # ============================================================ Phần 4
    w.h1('Phần 4. Quy tắc nghiệp vụ')
    w.p('**Quy tắc áp dụng:** Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung SRS_Các quy tắc chung_VN_1.0. Phần này chỉ ghi các quy tắc đặc thù của Danh mục gói bảo dưỡng; không lặp lại các quy tắc đã có trong SRS quy tắc chung.')
    BR = [
        ('BR-01', 'Mã gói và Tên gói duy nhất', ['Tên gói và Mã gói không được trùng trên toàn hệ thống.', 'Mã gói được lưu CHỮ IN HOA, chỉ gồm chữ không dấu, số, dấu - và _; sai định dạng báo “Chỉ gồm chữ không dấu, số, dấu - và _”.'], ['Tạo mới', 'Chỉnh sửa', 'Nhân bản', 'Import Excel']),
        ('BR-02', 'Công thức tính giá', ['Giá vốn = Đơn giá công của công ty quản lý × Định mức công × Hệ số công nghệ.', 'Giá công thức = Giá vốn × Hệ số giá bán gói.', 'Giá bán cơ sở mặc định = Giá công thức (sửa tay được).', 'Giá bán theo công ty = Giá bán cơ sở × Hệ số giá bán của công ty.'], ['Tạo mới', 'Chỉnh sửa', 'Xem chi tiết']),
        ('BR-03', 'Ràng buộc cấp và ghi chú kiểm tra', ['Mỗi cấp bảo dưỡng chỉ xuất hiện một lần trong một gói.', 'Mọi ô giao giữa nội dung kiểm tra và cấp phải có ít nhất một ghi chú kiểm tra.', 'Chỉ chọn được cấp / ghi chú kiểm tra đang Hoạt động; chọn giá trị đã khóa → “Cấp bảo dưỡng đã bị khóa hoặc không tồn tại” / “Nội dung kiểm tra đã bị khóa hoặc không tồn tại”.', 'Gói đang dùng cấp / ghi chú đã khóa vẫn hiển thị đúng tên kèm 🔒 và lưu lại được.'], ['Tạo mới', 'Chỉnh sửa', 'Nhân bản', 'Import Excel']),
        ('BR-04', 'Bắt buộc file PDF đính kèm', ['Gói phải có ít nhất 1 file PDF, mỗi file tối đa 20MB, khi lưu từ form Thêm mới / Sửa / Nhân bản.'], ['Tạo mới', 'Chỉnh sửa', 'Nhân bản']),
        ('BR-05', 'Điều kiện xóa gói', ['Chỉ xóa được gói đang Hoạt động và CHƯA được sử dụng; xóa là xóa hẳn kèm nội dung kiểm tra, cấp, hàng hóa áp dụng, hệ số giá bán theo công ty.', 'Gói được coi là đã sử dụng khi đã được chọn ở: báo giá dịch vụ, hợp đồng dịch vụ, phụ lục hợp đồng dịch vụ, đề nghị xuất dịch vụ, đề nghị hạch toán dịch vụ, hạch toán dịch vụ; báo giá, hợp đồng, phiếu giao việc, phiếu nhập kết quả của dịch vụ bảo hành – sửa chữa. Chỉ gắn hàng hóa áp dụng thì chưa tính.', 'Gói đã được sử dụng: nút Xóa bị ẩn; máy chủ chặn và báo “Gói bảo dưỡng đang được sử dụng, không thể xóa.” (không tự chuyển sang Khóa). Muốn ngừng dùng thì Khóa.'], ['Xóa']),
        ('BR-06', 'Không bỏ cấp đã phát sinh báo giá', ['Không bỏ được cột cấp đã phát sinh báo giá dịch vụ.'], ['Chỉnh sửa']),
        ('BR-07', 'Gói đang Khóa', ['Khóa được cả gói đang được sử dụng.', 'Máy chủ chặn Sửa và Xóa gói đang Khóa, báo “Gói bảo dưỡng đang bị khoá, vui lòng mở khoá trước khi cập nhật.”; phải Mở khóa trước.', 'Gói Khóa không còn chọn được ở màn nghiệp vụ khác; chứng từ đang dùng vẫn giữ nguyên.', 'Khóa / Mở khóa trùng (hai người cùng thao tác) → “Trạng thái đã bị thay đổi. Vui lòng load lại trang”.'], ['Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa']),
        ('BR-08', 'Trạng thái khi nhân bản / import', ['Gói nhân bản: ô Trạng thái mặc định Hoạt động (kể cả khi gói nguồn đang Khóa), người dùng vẫn đổi được sang Khóa trước khi lưu.', 'Gói import luôn được tạo ở trạng thái Hoạt động (file mẫu không có cột Trạng thái).'], ['Nhân bản', 'Import Excel']),
        ('BR-09', 'Ghi lịch sử thao tác', ['Mọi thao tác Tạo mới, Thay đổi thông tin (kể cả bảng con), Khóa, Mở khóa, Xóa đều ghi lịch sử kèm người thực hiện.'], ['Lịch sử thay đổi']),
        ('BR-10', 'Định dạng số', ['Số hiển thị theo chuẩn quốc tế: dấu phẩy ngăn cách hàng nghìn, dấu chấm thập phân (1,234,567.89).'], ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel']),
    ]
    w.table([['STT', 'Mã quy tắc', 'Tên quy tắc', 'Mô tả', 'Phạm vi áp dụng']] +
            [[str(i), a, b, '\n'.join(c), '\n'.join(d)] for i, (a, b, c, d) in enumerate(BR, 1)],
            widths=[0.6, 0.85, 1.3, 2.65, 1.2])

    w.rebuild_toc(levels=(1, 2, 3))
    return w.save(out)


if __name__ == '__main__':
    out = os.path.join(HERE, 'out', 'SRS - Danh mục gói bảo dưỡng.docx')
    print(build(sys.argv[1], out))
