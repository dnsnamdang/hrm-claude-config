# -*- coding: utf-8 -*-
"""HDSD Danh mục gói bảo dưỡng — bản 1.2 (28/09/2026), dựng trên KHUÔN HDSD Danh mục quốc gia.

Bản 1.2: bỏ "Xóa gói đã dùng thì chuyển sang Khóa" — gói đã dùng ở chứng từ thì ẩn Xóa, máy chủ chặn;
thêm nút Khóa riêng ở danh sách + chân trang Chi tiết; cấp / ghi chú kiểm tra đã khóa không chọn được.

Nội dung bám code nhánh gop_db tại 25/09/2026 (đã có Import Excel 5 sheet, Trạng thái ở form,
quy tắc ký tự mã, In xem trước, Lịch sử theo dõi cả bảng con). Ảnh chụp thật trên local.

Chạy:  python3 gen_hdsd.py <HDSD_Danh mục quốc gia.docx>
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from qg_writer import QgWriter  # noqa: E402

SH = os.path.join(HERE, 'shots')
IC = os.path.join(HERE, 'icons')
UML = os.path.join(HERE, 'uml')
CROP = os.path.join(HERE, 'crops')
os.makedirs(CROP, exist_ok=True)


def s(n):
    return os.path.join(SH, n + '.png')


def ic(n, h=0.22, alt=None):
    """Icon cắt từ UI; chưa có file (icon mới chờ cắt) thì dùng chữ `alt` để bản dựng không vỡ."""
    path = os.path.join(IC, n + '.png')
    if alt is not None and not os.path.exists(path):
        print('  [thiếu icon] %s -> dùng chữ “%s”' % (n, alt))
        return alt
    return ('img', path, h)


def image_opt(w, path, caption):
    """Ảnh mới chờ chụp: chưa có file thì bỏ qua (in cảnh báo) thay vì dừng cả bản dựng."""
    if os.path.exists(path):
        w.image(path, caption=caption)
    else:
        print('  [thiếu ảnh] %s — %s' % (os.path.basename(path), caption))


def crop(src, box, name):
    out = os.path.join(CROP, name + '.png')
    Image.open(s(src)).crop(box).save(out)
    return out


def prepare():
    Image.open(os.path.join(IC, 'menu_goibaoduong.png')).crop((0, 0, 150, 38)).save(
        os.path.join(IC, 'menu_goibaoduong_c.png'))
    crop('30_list_search', (230, 70, 1425, 165), 'filter')
    crop('18_create_filled', (230, 1995, 1435, 2175), 'sec_file')
    crop('16_create_be_errors', (230, 60, 1435, 330), 'err_be')
    crop('14_create_errors', (230, 60, 1440, 330), 'err_fe')


ROLES = {'pagebreak': 39, 'h1': 40, 'h2': 41, 'p': 31, 'bullet': 48, 'step': 42,
         'img': 44, 'cap': 45, 'blank': 26, 'tbl2': 25, 'tbl4': 28, 'tbl5': 90}

MENU = ['Từ phân hệ CSKH sau bán ', ic('menu_phanhe'), ', tại menu ', ic('menu_danhmuc'),
        ', chọn Gói bảo dưỡng ', ic('menu_goibaoduong_c')]


def build(template, out):
    prepare()
    w = QgWriter(template, ROLES, body_from=21,
                 cover_replace={'Danh mục quốc gia': 'Danh mục gói bảo dưỡng'})

    # ================================================================== TỔNG QUAN
    w.h1('TỔNG QUAN')
    w.h2('1. Thuật ngữ sử dụng trong tài liệu')
    w.table([
        ['Thuật ngữ', 'Giải thích'],
        ['Gói bảo dưỡng', 'Một bản ghi của danh mục: gồm thông tin chung, bảng nội dung kiểm tra theo từng cấp, giá theo từng công ty, hàng hóa áp dụng và file PDF kèm theo.'],
        ['Cấp bảo dưỡng', 'Mức độ bảo dưỡng lấy từ danh mục Cấp dịch vụ bảo dưỡng (ví dụ Cấp 1 (6T)). Trong bảng nội dung kiểm tra, mỗi cấp là MỘT CỘT.'],
        ['Nội dung kiểm tra bảo dưỡng', 'Một hạng mục phải làm khi bảo dưỡng, ví dụ “Kiểm tra gas và áp suất”. Mỗi hạng mục là MỘT DÒNG, kèm Đơn vị tính và Số lượng.'],
        ['Ghi chú kiểm tra', 'Ký hiệu công việc tại ô giao giữa một nội dung và một cấp, lấy từ danh mục Ghi chú kiểm tra bảo dưỡng (KTBM, DK, CC, VS…).'],
        ['Định mức công', 'Số công quy đổi cần cho một cấp bảo dưỡng.'],
        ['Hệ số công nghệ', 'Hệ số nhân thêm theo độ phức tạp công nghệ của cấp đó.'],
        ['Giá vốn / Giá công thức / Giá bán cơ sở', 'Giá vốn = Đơn giá công của công ty quản lý × Định mức công × Hệ số công nghệ. Giá công thức = Giá vốn × Hệ số giá bán gói. Giá bán cơ sở mặc định bằng Giá công thức, sửa tay được.'],
        ['Công ty quản lý gói bảo dưỡng', 'Công ty cung cấp đơn giá công để tính giá vốn của gói.'],
        ['Gói đã được sử dụng', 'Gói đã được chọn ở ít nhất một chứng từ: báo giá dịch vụ, hợp đồng dịch vụ, phụ lục hợp đồng dịch vụ, đề nghị xuất dịch vụ, đề nghị hạch toán dịch vụ, hạch toán dịch vụ; báo giá, hợp đồng, phiếu giao việc và phiếu nhập kết quả của dịch vụ bảo hành – sửa chữa. Gói này không xóa được, chỉ Khóa được. Chỉ gắn hàng hóa áp dụng thì CHƯA tính là đã sử dụng.'],

        ['Trạng thái Hoạt động', 'Gói dùng được ở các màn nghiệp vụ khác, sửa được; xóa được nếu chưa được sử dụng.'],
        ['Trạng thái Khóa', 'Gói ngừng sử dụng nhưng vẫn nằm trong danh mục; không sửa, không xóa được cho tới khi Mở khóa.'],
    ], widths=[1, 2.6])

    w.h2('2. Cập nhật tài liệu')
    w.table([
        ['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung'],
        ['1.0', '17/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục gói bảo dưỡng.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: bổ sung Import Excel, ô Trạng thái ở màn Tạo mới/Sửa, quy tắc ký tự của mã, Xem chi tiết, In xem trước, lịch sử theo dõi cả bảng nội dung kiểm tra/giá/hàng hóa/file; trình bày lại theo mẫu tài liệu danh mục chung.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bỏ cơ chế “Xóa gói đã được sử dụng thì chuyển sang Khóa”: gói đã được dùng ở chứng từ (báo giá, hợp đồng, phụ lục, đề nghị xuất, đề nghị hạch toán, hạch toán dịch vụ, phiếu giao việc / nhập kết quả dịch vụ) thì ẩn nút Xóa và máy chủ chặn xóa; gói chỉ gắn hàng hóa vẫn xóa được. Thêm nút Khóa riêng ở danh sách và chân trang màn Chi tiết. Cấp bảo dưỡng, ghi chú kiểm tra đã khóa không chọn được cho gói mới; gói cũ vẫn hiện kèm 🔒.'],
    ], widths=[0.8, 1, 1.4, 3.4])

    w.h2('3. Mục đích')
    w.p('Danh mục gói bảo dưỡng là nơi khai báo các gói bảo dưỡng dùng chung cho toàn hệ thống: mỗi gói nêu rõ phải kiểm tra những hạng mục nào, theo cấp bảo dưỡng nào, giá bán bao nhiêu cho từng công ty, áp dụng cho hàng hóa nào và kèm tài liệu gì.')
    w.p('Gói bảo dưỡng khai ở đây được dùng lại khi lập báo giá dịch vụ và phiếu yêu cầu dịch vụ, nên khai sai nội dung hoặc giá ở màn này sẽ kéo theo sai ở các chứng từ phía sau.')

    w.h2('4. Quyền sử dụng')
    w.p('Màn hình dùng 3 quyền thuộc nhóm quyền “Danh mục dịch vụ bảo dưỡng”:')
    w.table([
        ['Tên quyền', 'Được phép'],
        ['Thêm danh mục gói bảo dưỡng', 'Nút Tạo mới, Import Excel và Nhân bản.'],
        ['Sửa danh mục gói bảo dưỡng', 'Nút Sửa, Khóa (gói đang Hoạt động) và nút Mở khóa (gói đang Khóa).'],
        ['Xóa danh mục gói bảo dưỡng', 'Nút Xóa (gói đang Hoạt động và chưa được sử dụng).'],
    ], widths=[1.4, 2.6])
    w.p('Xem danh sách, xem chi tiết, In phiếu, Xuất Excel và Xem lịch sử KHÔNG đòi quyền riêng: mọi người dùng đã đăng nhập đều thực hiện được. Danh sách hiển thị toàn bộ gói của hệ thống, không phân theo công ty/phòng ban.')
    w.p('Nút nào Người dùng không có quyền dùng thì hệ thống ẩn hẳn, không hiện nút mờ.')

    w.h2('5. Sơ đồ chức năng tổng quan')
    w.image(os.path.join(UML, 'overview.png'), width=5.8,
            caption='Sơ đồ chức năng tổng quan màn Danh mục gói bảo dưỡng')

    # ================================================================== PHẦN 1
    w.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')
    w.h2('1. Truy cập màn hình')
    w.step(MENU)
    w.p('Hệ thống hiển thị danh sách gói bảo dưỡng hiện có, mặc định 10 dòng mỗi trang, gói mới tạo nằm trên cùng.')
    w.image(s('48_unsaved'), caption='Màn hình Danh mục gói bảo dưỡng khi mới truy cập')

    w.h2('2. Bố cục màn hình')
    w.p('Màn hình chia làm ba khu vực từ trên xuống:')
    w.bullet('Khu vực Bộ lọc danh sách — ô tìm kiếm nhanh, ô Trạng thái, ô Người tạo, nút Tìm kiếm và Làm mới.')
    w.bullet('Thanh công cụ — nút Tạo mới, nút Xuất Excel, nút Import Excel và biểu tượng Cấu hình cột hiển thị.')
    w.bullet('Bảng danh sách — các cột thông tin, cột Hành động ở cuối và phân trang bên dưới.')

    w.h2('3. Các cột của bảng danh sách')
    w.table([
        ['Cột', 'Nội dung'],
        ['STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'],
        ['Mã', 'Mã gói bảo dưỡng. Luôn hiển thị, sắp xếp được. Bấm vào mã để mở màn Chi tiết gói bảo dưỡng (xem PHẦN 7).'],
        ['Tên gói bảo dưỡng', 'Tên gói, sắp xếp được. Gói đã khai cấp bảo dưỡng có biểu tượng ⓘ — rê chuột vào để xem giá theo từng cấp.'],
        ['Công ty quản lý gói bảo dưỡng', 'Công ty dùng để lấy đơn giá công. Mặc định ẩn.'],
        ['Người cập nhật', 'Người sửa gói gần nhất. Mặc định ẩn.'],
        ['Ngày cập nhật', 'Thời điểm sửa gần nhất, dạng dd/mm/yyyy hh:mm. Mặc định ẩn, sắp xếp được.'],
        ['Người tạo', 'Người đã tạo gói.'],
        ['Ngày tạo', 'Thời điểm tạo, dạng dd/mm/yyyy hh:mm, sắp xếp được.'],
        ['Trạng thái', 'Nhãn xanh “Hoạt động” hoặc nhãn đỏ “Khóa”.'],
        ['Hành động', 'Tối đa 2 nút hiện thẳng, các nút còn lại nằm trong nút ba chấm (xem mục 4).'],
    ], widths=[1.3, 3])
    w.image(s('33_tooltip_gia'), caption='Rê chuột vào biểu tượng ⓘ để xem giá bán theo từng cấp')

    w.h2('4. Cột Hành động')
    w.p('Nút nào hiện ra tùy theo trạng thái gói và quyền của Người dùng:')
    w.table([
        ['Nút', 'Khi nào hiện', 'Tác dụng'],
        ['Sửa', 'Có quyền Sửa và gói đang Hoạt động.', 'Mở trang Sửa gói bảo dưỡng.'],
        ['Xóa', 'Có quyền Xóa, gói đang Hoạt động và CHƯA được sử dụng ở chứng từ nào.', 'Mở hộp xác nhận xóa.'],
        ['Khóa', 'Có quyền Sửa và gói đang Hoạt động — kể cả gói đã được sử dụng.', 'Mở hộp xác nhận khóa.'],
        ['Mở khóa', 'Có quyền Sửa và gói đang Khóa.', 'Mở hộp xác nhận mở khóa.'],
        ['Nhân bản', 'Có quyền Thêm.', 'Mở trang Sao chép gói bảo dưỡng với dữ liệu điền sẵn.'],
        ['In', 'Luôn hiện.', 'Mở cửa sổ xem trước phiếu Danh mục kiểm tra bảo dưỡng định kỳ.'],
        ['Lịch sử', 'Luôn hiện.', 'Mở cửa sổ Lịch sử thay đổi của gói.'],
    ], widths=[0.9, 2, 2])
    w.p('Hai nút đầu tiên đủ điều kiện được hiện thẳng trên dòng, các nút còn lại nằm trong nút ba chấm “Hành động khác” ')
    w.bullet(['Gói Hoạt động chưa được sử dụng: ', ic('btn_sua'), ' Sửa, ', ic('btn_xoa'), ' Xóa hiện thẳng; Khóa, Nhân bản, In, Lịch sử trong nút ba chấm ', ic('btn_bacham'), '.'])
    w.bullet(['Gói Hoạt động đã được sử dụng: ', ic('btn_sua'), ' Sửa, ', ic('btn_khoa', alt='Khóa'), ' Khóa hiện thẳng; Nhân bản, In, Lịch sử trong nút ba chấm.'])
    w.bullet(['Gói đang Khóa: ', ic('btn_mokhoa'), ' Mở khóa, ', ic('btn_nhanban'), ' Nhân bản hiện thẳng; In, Lịch sử trong nút ba chấm.'])
    image_opt(w, s('54_rowmenu_lock'), 'Nút ba chấm của gói chưa được sử dụng — Khóa, Nhân bản, In, Lịch sử')
    w.p('Lưu ý quan trọng: gói ĐÃ KHÓA không còn nút Sửa, Xóa và Khóa. Muốn sửa, Người dùng phải Mở khóa trước. Gói đã được sử dụng không có nút Xóa.')

    w.h2('5. Phân trang và sắp xếp')
    w.p('Cuối bảng có dòng “Hiển thị a–b / N”: N là tổng số gói khớp bộ lọc đang áp dụng, không phải tổng toàn danh mục.')
    w.p('Ô Số dòng/trang có các mức 5, 10, 20, 50, 100 (mặc định 10). Đổi số dòng thì hệ thống tự quay về trang 1.')
    w.p('Các cột sắp xếp được: Mã, Tên gói bảo dưỡng, Ngày tạo, Ngày cập nhật. Bấm tiêu đề cột để sắp xếp, bấm lần hai để đảo chiều. Thứ tự sắp xếp và bộ lọc được giữ nguyên khi chuyển trang.')

    # ================================================================== PHẦN 2
    w.h1('PHẦN 2: TÌM KIẾM VÀ LỌC DANH SÁCH')
    w.h2('1. Các ô tìm kiếm và lọc')
    w.p('Các bước tìm kiếm, lọc thông tin:')
    w.step(['Bước 1: '] + MENU)
    w.step(['Bước 2: Nhập chữ vào ô tìm kiếm nhanh hoặc chọn giá trị ở ô Trạng thái / Người tạo.'])
    w.image(os.path.join(CROP, 'filter.png'), caption='Khu vực Bộ lọc danh sách')
    w.table([
        ['Ô', 'Cách dùng'],
        ['Ô tìm kiếm nhanh', 'Tìm theo TÊN hoặc MÃ gói (khớp một phần, không phân biệt hoa thường). Gõ từ 2 ký tự trở lên thì kết quả khớp nhất đứng đầu: trùng khít → bắt đầu bằng từ khóa → chứa từ khóa.'],
        ['Trạng thái', 'Chọn Hoạt động hoặc Khóa. Bỏ trống thì hiện cả hai trạng thái.'],
        ['Người tạo', 'Chọn một nhân viên để chỉ xem các gói do người đó tạo. Danh sách hiển thị dạng Tên - Mã phòng - Mã nhân viên.'],
    ], widths=[1.2, 3])

    w.h2('2. Cách áp dụng')
    w.p(['Hệ thống TỰ lọc: gõ vào ô tìm kiếm nhanh thì sau khoảng nửa giây danh sách tự nạp lại; chọn Trạng thái hoặc Người tạo thì lọc ngay. Muốn lọc ngay lập tức thì nhấn Enter hoặc bấm ', ic('btn_timkiem'), '.'])
    w.p('Các tiêu chí kết hợp với nhau theo kiểu VÀ — chỉ gói thỏa đồng thời tất cả tiêu chí mới hiện ra. Mỗi lần đổi tiêu chí, danh sách quay về trang 1.')
    w.p(['Bấm ', ic('btn_lammoi'), ' để xóa toàn bộ tiêu chí; danh sách nạp lại đầy đủ ngay lập tức.'])
    w.image(s('36_filter_status'), caption='Kết quả lọc theo Trạng thái = Khóa')

    # ================================================================== PHẦN 3
    w.h1('PHẦN 3: THÊM MỚI GÓI BẢO DƯỠNG')
    w.h2('1. Các bước Thêm mới gói bảo dưỡng')
    w.step('Bước 1: Truy cập vào màn hình Danh mục gói bảo dưỡng.')
    w.step(['Bước 2: Bấm ', ic('btn_taomoi'), '. Hệ thống mở TRANG RIÊNG “Thêm gói bảo dưỡng” (không phải cửa sổ bật lên, vì lượng thông tin lớn).'])
    w.image(s('13_create_top'), caption='Trang Thêm gói bảo dưỡng khi vừa mở')
    w.step('Bước 3: Nhập khối Thông tin chung (mục 2).')
    w.step('Bước 4: Khai bảng Danh mục kiểm tra bảo dưỡng định kỳ và thông số giá của từng cấp (mục 3, 4).')
    w.step('Bước 5: Nhập hệ số giá bán theo từng công ty nếu cần (mục 5), chọn hàng hóa áp dụng (mục 6) và đính kèm ít nhất 1 file PDF (mục 7).')
    w.step(['Bước 6: Bấm ', ic('btn_luu'), ' để lưu và quay về danh sách, hoặc ', ic('btn_luutieptuc'), ' để lưu rồi nhập tiếp gói khác.'])

    w.h2('2. Khối Thông tin chung')
    w.image(s('20_sec'), caption='Khối Thông tin chung')
    w.table([
        ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị ban đầu', 'Ghi chú'],
        ['Tên gói bảo dưỡng', 'Ô nhập giá trị', 'Có', 'Trống', 'Tối đa 255 ký tự, duy nhất toàn hệ thống. Bỏ trống báo “Bắt buộc phải nhập”; trùng báo “Đã tồn tại”.'],
        ['Mã gói bảo dưỡng', 'Ô nhập giá trị', 'Có', 'Trống', 'Người dùng tự đặt, tối đa 255 ký tự, duy nhất toàn hệ thống. Chỉ gồm chữ không dấu, số, dấu - và _; sai định dạng báo ngay dưới ô “Chỉ gồm chữ không dấu, số, dấu - và _”. Hệ thống tự chuyển thành CHỮ IN HOA khi gõ, nên “bd-01” và “BD-01” bị coi là trùng.'],
        ['Định mức đàm phán giá (%)', 'Ô nhập số', 'Không', 'Trống', 'Từ 0 đến 99, tối đa 2 chữ số thập phân.'],
        ['VAT (%)', 'Ô nhập số', 'Không', 'Trống', 'Từ 0 đến 100, tối đa 2 chữ số thập phân. Để trống thì lưu 0.'],
        ['Công ty quản lý gói bảo dưỡng', 'Ô chọn giá trị', 'Có', 'Công ty của người đang đăng nhập', 'Quyết định đơn giá công dùng để tính giá vốn. Chọn sai công ty là sai toàn bộ giá của gói.'],
        ['Trạng thái', 'Ô chọn giá trị', 'Không', 'Hoạt động', 'Chỉ chọn 1 trong 2 giá trị: Hoạt động / Khóa.'],
        ['Ghi chú', 'Ô nhập giá trị', 'Không', 'Trống', 'Tối đa 255 ký tự. Nội dung được in ở cuối phiếu kiểm tra bảo dưỡng.'],
        ['Hệ số giá bán gói bảo dưỡng', 'Ô nhập số', 'Không', 'Trống', 'Từ 1 đến 100. Để trống thì lưu 1. Dùng để tính Giá công thức.'],
    ], widths=[1.3, 0.9, 0.7, 1.1, 2.6])
    w.p('Các ô số dùng dấu chấm (.) làm dấu thập phân và dấu phẩy (,) ngăn cách hàng nghìn, ví dụ 1,400,000 hoặc 1.5.')

    w.h2('3. Khai bảng Danh mục kiểm tra bảo dưỡng định kỳ')
    w.p('Bảng có dạng ma trận: mỗi DÒNG là một nội dung kiểm tra, mỗi CỘT là một cấp bảo dưỡng, ô giao nhau cho biết ở cấp đó phải làm gì với hạng mục đó.')
    w.step(['Bước 1: Bấm ', ic('btn_themdong', 0.18), ' để thêm một dòng; nhập Nội dung kiểm tra, chọn ĐVT và nhập SL (số nguyên). Cả ba ô đều bắt buộc.'])
    w.step(['Bước 2: Bấm dấu ', ic('btn_themcot', 0.2), ' ở góc phải tiêu đề bảng để thêm một cột, rồi chọn Cấp bảo dưỡng cho cột đó.'])
    w.step('Bước 3: Tại ô giao giữa dòng và cột, chọn một hoặc nhiều Ghi chú kiểm tra (KTBM, DK, CC, VS…). Ô này bắt buộc.')
    w.step('Bước 4: Lặp lại cho tới khi khai đủ các hạng mục và các cấp.')
    w.image(s('21_sec'), caption='Bảng Danh mục kiểm tra bảo dưỡng định kỳ và thông số giá của cấp')
    w.p('Mỗi cấp bảo dưỡng chỉ được chọn MỘT lần. Chọn lại cấp đã dùng ở cột khác, hệ thống báo “Cấp bảo dưỡng này đã được chọn ở cột khác” và không nhận.')
    w.p('Ô Cấp bảo dưỡng và ô Ghi chú kiểm tra chỉ liệt kê các giá trị đang Hoạt động. Gói cũ đang dùng một cấp / ghi chú nay đã bị khóa thì khi mở Sửa, Chi tiết vẫn hiện đúng tên kèm biểu tượng 🔒 và lưu lại bình thường; đổi sang giá trị khác thì giá trị đã khóa biến mất khỏi danh sách chọn.')
    w.p('Bỏ một dòng: bấm biểu tượng thùng rác ở cuối dòng. Bỏ một cột: bấm dấu × ở tiêu đề cột, hệ thống hỏi lại “Xóa cột … sẽ xóa toàn bộ ghi chú và giá của cột này. Bạn có chắc chắn?” — bấm Xác nhận để xóa, Hủy để giữ lại.')
    w.image(s('19_confirm_xoa_cot'), caption='Hộp xác nhận xóa cột cấp bảo dưỡng')

    w.h2('4. Thông số giá của từng cấp')
    w.p('Dưới bảng ma trận, mỗi cột cấp có các dòng thông số:')
    w.table([
        ['Dòng', 'Người dùng nhập hay hệ thống tính', 'Ý nghĩa'],
        ['Định mức công', 'Người dùng nhập — BẮT BUỘC', 'Số công quy đổi cần cho cấp đó.'],
        ['Hệ số công nghệ', 'Người dùng nhập', 'Hệ số nhân thêm theo độ phức tạp công nghệ.'],
        ['Giá vốn', 'Hệ thống tự tính (chỉ đọc)', 'Đơn giá công của công ty quản lý × Định mức công × Hệ số công nghệ.'],
        ['Giá công thức', 'Hệ thống tự tính (chỉ đọc)', 'Giá vốn × Hệ số giá bán gói bảo dưỡng.'],
        ['Giá bán cơ sở', 'Hệ thống điền sẵn, sửa tay được', 'Mặc định bằng Giá công thức; là căn cứ tính giá bán cho từng công ty.'],
        ['Gợi ý hàng hóa', 'Người dùng chọn', 'Hàng hóa gợi ý dùng kèm cho cấp đó.'],
        ['Giá bán theo công ty', 'Hệ thống tự tính', 'Giá bán cơ sở × Hệ số giá bán của từng công ty (mục 5).'],
    ], widths=[1.2, 1.6, 2.6])
    w.p('Ví dụ: công ty quản lý có đơn giá công 700,000; nhập Định mức công = 2, Hệ số công nghệ = 1.5, Hệ số giá bán gói = 1.2. Khi đó Giá vốn = 700,000 × 2 × 1.5 = 2,100,000; Giá công thức = 2,100,000 × 1.2 = 2,520,000; Giá bán cơ sở điền sẵn 2,520,000.')

    w.h2('5. Giá vốn theo công ty')
    w.p('Khối này liệt kê mọi công ty trong hệ thống kèm Đơn giá công và Giá vốn theo từng cấp. Người dùng nhập Hệ số giá bán riêng cho từng công ty (mặc định 1, tối đa 2 chữ số thập phân). Dòng của công ty quản lý bị khóa, luôn bằng 1.')
    w.image(s('22_sec'), caption='Khối Giá vốn theo công ty')

    w.h2('6. Áp dụng cho hàng hóa')
    w.bullet(['Bấm ', ic('btn_chonhanghoa'), ' để mở cửa sổ “Chọn hàng hóa áp dụng”, tìm theo tên/mã/model, tích chọn rồi bấm “Thêm n hàng hoá”.'])
    w.bullet(['Bấm ', ic('btn_chonnhomhang'), ' để thêm nhanh toàn bộ hàng hóa của một nhóm hàng.'])
    w.bullet('Hàng hóa được gom theo nhóm hàng; bấm biểu tượng thùng rác để bỏ một hàng hóa hoặc cả nhóm.')
    w.image(s('17_chon_hang'), caption='Cửa sổ Chọn hàng hóa áp dụng')
    w.p('Lưu ý: chỉ gắn hàng hóa áp dụng thì gói CHƯA được coi là đã sử dụng — vẫn xóa được; khi xóa gói, danh sách hàng hóa áp dụng bị xóa theo.')

    w.h2('7. File đính kèm (PDF)')
    w.step(['Bước 1: Bấm ', ic('btn_themtailieu'), ' để thêm một dòng tài liệu.'])
    w.step('Bước 2: Bấm Chọn tệp và chọn file PDF từ máy. File được tải lên ngay; dòng tài liệu hiện tên file, dung lượng và các nút Xem / Tải xuống / Thay đổi / Xóa.')
    w.image(os.path.join(CROP, 'sec_file.png'), caption='Khối File đính kèm (PDF) sau khi chọn file')
    w.bullet('BẮT BUỘC có ít nhất 1 file PDF mới lưu được gói; thiếu thì báo “Bắt buộc phải đính kèm ít nhất 1 file PDF”.')
    w.bullet('Chỉ nhận file PDF, tối đa 20MB mỗi file; thêm được nhiều file cho một gói.')

    w.h2('8. Tác dụng các nút ở chân trang')
    w.table([
        ['Nút', 'Tác dụng'],
        ['Lưu', 'Kiểm tra và ghi gói, báo “Tạo gói bảo dưỡng thành công” rồi quay về danh sách.'],
        ['Lưu và tiếp tục', 'Ghi gói rồi GIỮ NGUYÊN trang Thêm mới với form trống để nhập gói kế tiếp. Chỉ có ở màn Thêm mới.'],
        ['Quay lại', 'Về danh sách. Nếu đã nhập dở, hệ thống hỏi “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” — chọn Thoát để bỏ, Ở lại để nhập tiếp.'],
    ], widths=[1.2, 4])

    w.h2('9. Các lỗi thường gặp')
    w.p('Khi bấm Lưu mà còn thiếu sót, hệ thống báo “Vui lòng kiểm tra lại dữ liệu nhập” và tô đỏ ngay dưới ô lỗi. Trang KHÔNG chuyển đi, dữ liệu đã nhập vẫn còn nguyên.')
    w.image(os.path.join(CROP, 'err_fe.png'), caption='Lỗi đỏ ngay dưới ô — thiếu Tên và Mã sai định dạng')
    w.image(os.path.join(CROP, 'err_be.png'), caption='Tên và Mã đã tồn tại trên hệ thống')
    w.table([
        ['Thông báo', 'Nguyên nhân và cách xử lý'],
        ['Bắt buộc phải nhập', 'Chưa nhập ô có dấu * (Tên, Mã, Công ty quản lý, Nội dung/ĐVT/SL của dòng, Ghi chú kiểm tra ở ô giao, Định mức công). Cuộn tìm ô có viền đỏ.'],
        ['Đã tồn tại', 'Tên hoặc Mã đã có gói khác dùng. Mã được so sau khi in hoa.'],
        ['Chỉ gồm chữ không dấu, số, dấu - và _', 'Mã có chữ có dấu, khoảng trắng hoặc ký tự đặc biệt khác. Lỗi hiện ngay khi gõ và tự mất khi nhập lại đúng.'],
        ['Cấp bảo dưỡng này đã được chọn ở cột khác', 'Chọn trùng cấp trong bảng ma trận.'],
        ['Bắt buộc phải đính kèm ít nhất 1 file PDF', 'Chưa có file PDF nào ở khối File đính kèm.'],
        ['Tối đa 99 / Tối đa 100 / Không được nhỏ hơn 1', 'Ô số vượt giới hạn (Định mức đàm phán giá, VAT, Hệ số giá bán).'],
        ['Cấp bảo dưỡng đã bị khóa hoặc không tồn tại', 'Cấp đã chọn vừa bị khóa (hoặc bị xóa) ở danh mục Cấp dịch vụ bảo dưỡng trong lúc đang nhập. Chọn cấp khác đang Hoạt động.'],
        ['Nội dung kiểm tra đã bị khóa hoặc không tồn tại', 'Ghi chú kiểm tra đã chọn ở ô giao vừa bị khóa (hoặc bị xóa) ở danh mục Ghi chú kiểm tra bảo dưỡng. Chọn ghi chú khác đang Hoạt động.'],
    ], widths=[1.8, 3])

    # ================================================================== PHẦN 4
    w.h1('PHẦN 4: CHỈNH SỬA VÀ XÓA')
    w.h2('1. Chỉnh sửa')
    w.step('Bước 1: Truy cập vào màn hình Danh mục gói bảo dưỡng.')
    w.step(['Bước 2: Bấm nút ', ic('btn_sua'), ' ở cột Hành động của gói cần sửa (hoặc mở màn Chi tiết rồi bấm ', ic('btn_sua_footer'), ').'])
    w.step('Bước 3: Hệ thống mở trang “Sửa gói bảo dưỡng” với toàn bộ dữ liệu hiện tại đã điền sẵn.')
    w.image(s('42_edit_top'), caption='Trang Sửa gói bảo dưỡng')
    w.step('Bước 4: Cập nhật các thông tin cần sửa (quy tắc nhập như Thêm mới ở PHẦN 3).')
    w.step(['Bước 5: Bấm ', ic('btn_luu'), '. Hệ thống báo “Cập nhật gói bảo dưỡng thành công” và quay về danh sách.'])
    w.p('Điểm khác so với Thêm mới:')
    w.bullet('Giữ nguyên Tên và Mã của chính gói đó thì không bị báo trùng.')
    w.bullet('Không có nút “Lưu và tiếp tục”; có thêm nút Nhân bản ở chân trang.')
    w.bullet('Không bỏ được cột cấp đã phát sinh báo giá dịch vụ: hệ thống báo “Không thể xóa cấp dịch vụ đã được sử dụng!”.')
    w.bullet('Gói đang Khóa không có nút Sửa. Nếu mở trang Sửa của gói đang Khóa từ một liên kết đã lưu, hệ thống báo “Gói bảo dưỡng đang bị khoá, vui lòng mở khoá trước khi sửa.” và chuyển về màn Chi tiết.')

    w.h2('2. Xóa')
    w.p('Tại màn hình danh sách gói bảo dưỡng:')
    w.step(['Bước 1: Ở cột Hành động, bấm ', ic('btn_xoa'), ' (hoặc bấm ', ic('btn_xoa_footer'), ' ở chân trang màn Chi tiết).'])
    w.image(s('34_delete_confirm'), caption='Hộp xác nhận xóa gói bảo dưỡng')
    w.step(['Bước 2: Hộp “Xác nhận xóa” hỏi “Bạn có chắc chắn muốn xóa gói bảo dưỡng \'<tên>\'? Hành động này không thể hoàn tác.”. Bấm ', ic('btn_confirm_xoa'), ' để xác nhận. Hệ thống báo “Xóa gói bảo dưỡng thành công”, gói biến mất khỏi danh sách (xóa từ màn Chi tiết thì quay về danh sách).'])
    w.p(['Bấm ', ic('btn_huy'), ' nếu bấm nhầm. Không có gì thay đổi.'])
    w.p('Xóa là xóa HẲN: gói bị xóa cùng toàn bộ nội dung kiểm tra, cấp bảo dưỡng, hàng hóa áp dụng và hệ số giá bán theo công ty; không chuyển sang Khóa.')
    w.p('Nút Xóa CHỈ hiện khi: Người dùng có quyền Xóa, gói đang Hoạt động và gói CHƯA được sử dụng ở chứng từ nào. Gói được coi là đã sử dụng khi đã được chọn ở: báo giá dịch vụ, hợp đồng dịch vụ, phụ lục hợp đồng dịch vụ, đề nghị xuất dịch vụ, đề nghị hạch toán dịch vụ, hạch toán dịch vụ; báo giá, hợp đồng, phiếu giao việc và phiếu nhập kết quả của dịch vụ bảo hành – sửa chữa. Gói đã được sử dụng thì không có nút Xóa — muốn ngừng dùng thì Khóa (PHẦN 5).')
    w.bullet('Nếu trong lúc đang mở hộp xác nhận, gói vừa được chọn ở một chứng từ: bấm Xóa sẽ nhận thông báo “Gói bảo dưỡng đang được sử dụng, không thể xóa.”, gói vẫn còn.')
    w.bullet('Nếu gói vừa bị người khác khóa: thông báo “Gói bảo dưỡng đang bị khoá, vui lòng mở khoá trước khi cập nhật.”')

    # ================================================================== PHẦN 5
    w.h1('PHẦN 5: KHÓA VÀ MỞ KHÓA')
    w.h2('1. Ý nghĩa')
    w.p('Khi một gói không còn dùng nữa — nhất là gói đã được sử dụng ở chứng từ nên không xóa được — hãy Khóa gói. Khóa được CẢ gói đang được sử dụng. Sau khi khóa:')
    w.bullet('Gói VẪN nằm trong danh sách, cột Trạng thái hiện nhãn đỏ “Khóa”.')
    w.bullet('Nút Sửa, Xóa, Khóa biến mất; chỉ còn Mở khóa, Nhân bản, In, Lịch sử.')
    w.bullet('Gói không còn chọn được ở chứng từ mới; chứng từ đã lập vẫn giữ nguyên gói.')
    w.bullet('Vẫn xem chi tiết, in phiếu, nhân bản và xem lịch sử bình thường.')

    w.h2('2. Các bước khóa')
    w.p('Cách 1 — tại màn hình danh sách:')
    w.step(['Bước 1: Ở cột Hành động của gói cần khóa, bấm ', ic('btn_khoa', alt='Khóa'), ' (gói đã được sử dụng: nút hiện thẳng; gói chưa được sử dụng: nằm trong nút ba chấm ', ic('btn_bacham'), ').'])
    image_opt(w, s('55_lock_confirm'), 'Hộp xác nhận khóa gói bảo dưỡng')
    w.step(['Bước 2: Hộp “Xác nhận khóa” hỏi “Bạn có chắc chắn muốn khóa gói bảo dưỡng \'<tên>\'?”. Bấm ', ic('btn_confirm_khoa', alt='Khóa'), ' để xác nhận. Hệ thống báo “Khóa gói bảo dưỡng thành công”, cột Trạng thái đổi thành Khóa.'])
    w.p(['Hoặc bấm ', ic('btn_huy'), ' nếu bấm nhầm.'])
    w.p('Cách 2 — tại màn Chi tiết gói bảo dưỡng:')
    w.step(['Bước 1: Bấm vào Mã gói để mở màn Chi tiết, bấm ', ic('btn_khoa_footer', alt='Khóa'), ' ở chân trang.'])
    image_opt(w, s('56_detail_lock'), 'Nút Khóa ở chân trang màn Chi tiết gói bảo dưỡng')
    w.step('Bước 2: Xác nhận ở hộp “Xác nhận khóa”. Hệ thống báo “Khóa gói bảo dưỡng thành công” và Ở LẠI màn Chi tiết; chân trang đổi ngay thành Mở khóa, Nhân bản, In.')
    image_opt(w, s('57_detail_locked'), 'Màn Chi tiết sau khi khóa — chân trang chỉ còn Mở khóa, Nhân bản, In')
    w.p('Cách 3 — đổi Trạng thái trong trang Sửa:')
    w.step(['Bước 1: Bấm ', ic('btn_sua'), ' ở gói cần khóa, ở ô Trạng thái chọn “Khóa”.'])
    w.image(s('43_edit_lock'), caption='Đổi Trạng thái sang Khóa trong trang Sửa')
    w.step(['Bước 2: Bấm ', ic('btn_luu'), '. Cột Trạng thái của gói đổi thành Khóa.'])

    w.h2('3. Mở khóa')
    w.step(['Bước 1: Ở cột Hành động của gói đang Khóa, bấm ', ic('btn_mokhoa'), ' (hoặc ', ic('btn_mokhoa_footer'), ' ở chân trang màn Chi tiết). Có thể lọc nhanh bằng Trạng thái = Khóa.'])
    w.image(s('45_unlock_confirm'), caption='Hộp xác nhận mở khóa gói bảo dưỡng')
    w.step(['Bước 2: Bấm ', ic('btn_confirm_mokhoa'), ' để xác nhận. Hệ thống báo “Mở khóa gói bảo dưỡng thành công”, cột Trạng thái đổi thành Hoạt động. Mở khóa ở màn Chi tiết thì Ở LẠI màn đó, chân trang hiện lại nút Sửa, Khóa.'])
    w.p(['Hoặc bấm ', ic('btn_huy'), ' nếu bấm nhầm.'])
    w.p('Khóa / Mở khóa cần quyền Sửa danh mục gói bảo dưỡng. Mọi lần Khóa / Mở khóa đều được ghi vào Lịch sử thay đổi. Nếu hai người cùng khóa (hoặc cùng mở khóa) một gói, người bấm sau nhận thông báo “Trạng thái đã bị thay đổi. Vui lòng load lại trang”.')

    # ================================================================== PHẦN 6
    w.h1('PHẦN 6: XEM LỊCH SỬ THAY ĐỔI')
    w.p('Xem lịch sử từ màn danh sách:')
    w.step(['Ở cột Hành động, bấm nút ba chấm ', ic('btn_bacham'), ' rồi chọn Lịch sử.'])
    w.p('Xem lịch sử từ màn chi tiết:')
    w.step('Bước 1: Bấm vào Mã gói để mở màn Chi tiết gói bảo dưỡng.')
    w.step(['Bước 2: Bấm ', ic('btn_xemlichsu'), ' — khối Lịch sử ở cuối trang mở ra.'])
    w.image(s('52_history_lock'), caption='Cửa sổ Lịch sử thay đổi của gói bảo dưỡng')
    w.p('Cửa sổ liệt kê mọi lần thay đổi của gói, mới nhất trên cùng. Mỗi mốc cho biết:')
    w.bullet('Thời điểm thay đổi, dạng dd/mm/yyyy hh:mm.')
    w.bullet('Loại thay đổi — Tạo mới, Thay đổi thông tin, Khóa, Mở khóa.')
    w.bullet('Người thực hiện kèm phòng ban.')
    w.bullet('Trường nào đã đổi, giá trị cũ → giá trị mới; với bảng con thì liệt kê dòng thêm mới / sửa / xóa.')
    w.p('Các thông tin được ghi lịch sử: Mã, Tên, Công ty quản lý, Định mức đàm phán giá, VAT, Hệ số giá bán gói, Trạng thái, Ghi chú và các bảng: nội dung kiểm tra bảo dưỡng, cấp dịch vụ, công ty áp dụng (hệ số giá bán), hàng hóa gợi ý/áp dụng, file đính kèm.')
    w.p('Bấm Bộ lọc để lọc theo Loại hành động (Tạo mới / Thay đổi thông tin / Thay đổi trạng thái), Người thực hiện và khoảng thời gian.')
    w.image(s('53_history_filter'), caption='Bộ lọc trong cửa sổ Lịch sử thay đổi')

    # ================================================================== PHẦN 7
    w.h1('PHẦN 7: XEM CHI TIẾT GÓI BẢO DƯỠNG')
    w.step('Bước 1: Truy cập vào màn hình Danh mục gói bảo dưỡng.')
    w.step('Bước 2: Bấm vào Mã gói ở cột Mã. Hệ thống mở trang “Chi tiết gói bảo dưỡng: <mã gói>”.')
    # Ảnh 58 (chụp sau 28/09, chân trang có nút Khóa) thay cho 40b cũ khi đã có file
    w.image(s('58_detail_full') if os.path.exists(s('58_detail_full')) else s('40b_detail_active_candelete'),
            caption='Trang Chi tiết gói bảo dưỡng ở chế độ chỉ đọc')
    w.p('Trang hiển thị đủ 5 khối như màn Thêm mới (Thông tin chung, Danh mục kiểm tra bảo dưỡng định kỳ, Giá vốn theo công ty, Áp dụng cho hàng hóa, File đính kèm) ở chế độ chỉ đọc, kèm khối Lịch sử ở cuối trang.')
    w.p('Chân trang có các nút giống cột Hành động ở danh sách của đúng gói đó: Sửa, Xóa, Khóa, Mở khóa (theo điều kiện ở PHẦN 1 mục 4), In, Nhân bản và Quay lại. Khóa / Mở khóa ngay tại màn Chi tiết thì Ở LẠI màn này; Xóa thì quay về danh sách.')

    # ================================================================== PHẦN 8
    w.h1('PHẦN 8: NHÂN BẢN GÓI BẢO DƯỠNG')
    w.p('Nhân bản dùng khi cần tạo một gói gần giống gói đã có, tránh khai lại toàn bộ bảng nội dung kiểm tra.')
    w.step(['Bước 1: Bấm ', ic('btn_nhanban'), ' ở dòng cần sao chép (hoặc ', ic('btn_nhanban_footer'), ' ở chân trang màn Chi tiết / Sửa).'])
    w.step('Bước 2: Hệ thống mở trang “Sao chép gói bảo dưỡng” với toàn bộ dữ liệu của gói nguồn (kể cả hàng hóa áp dụng và file đính kèm), kèm dòng nhắc “Đang sao chép từ gói … — hãy đổi tên/mã trước khi lưu.”.')
    w.image(s('46_copy_top'), caption='Trang Sao chép gói bảo dưỡng')
    w.step('Bước 3: Sửa lại Tên gói và Mã gói cho khác gói nguồn — giữ nguyên thì khi Lưu sẽ báo “Đã tồn tại”.')
    w.step(['Bước 4: Chỉnh các nội dung khác nếu cần rồi bấm ', ic('btn_luu'), '.'])
    w.p('Gói nhân bản luôn được tạo ở trạng thái Hoạt động, kể cả khi nhân bản từ gói đang Khóa. Gói nguồn không bị thay đổi.')

    # ================================================================== PHẦN 9
    w.h1('PHẦN 9: XUẤT DANH SÁCH RA EXCEL')
    w.h2('1. Các bước xuất file')
    w.step(['Bước 1: Bấm nút ', ic('btn_xuatexcel'), '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
    w.image(s('06_export'), caption='Cửa sổ Chọn trường xuất file')
    w.step('Bước 2: Tích chọn các trường cần xuất và kéo biểu tượng ☰ để đổi thứ tự cột trong file. Mặc định hệ thống tích sẵn đúng các cột đang hiển thị trên bảng.')
    w.step(['Bước 3: Bấm ', ic('btn_xuatfile'), '. Hệ thống tải về file Danh_sach_goi_bao_duong.xlsx.'])
    w.h2('2. Tác dụng các thành phần trên cửa sổ')
    w.table([
        ['Thành phần', 'Tác dụng'],
        ['Danh sách trường', 'Chọn nhiều trường: Mã, Tên gói bảo dưỡng, Người tạo, Ngày tạo, Trạng thái, Công ty quản lý.'],
        ['Chọn tất cả', 'Tích hết các trường.'],
        ['Bỏ chọn hết', 'Bỏ tích toàn bộ. Khi không còn trường nào được chọn, nút Xuất file không bấm được.'],
        ['Xuất file', 'Sinh file Excel và tải về máy.'],
        ['Đóng', 'Đóng cửa sổ, không xuất gì.'],
    ], widths=[1.3, 3.5])
    w.p('Lưu ý:')
    w.bullet('File xuất chứa TOÀN BỘ gói bảo dưỡng của danh mục, KHÔNG áp bộ lọc đang có trên màn hình.')
    w.bullet('File luôn có thêm cột “Giá gói bảo dưỡng” liệt kê giá theo từng cấp, ví dụ “Cấp 1 (6T): 2,520,000”.')
    w.bullet('File có tiêu đề “Danh sách gói bảo dưỡng”, logo công ty ở đầu và khối ký “Người lập” ở cuối.')

    # ================================================================== PHẦN 10
    w.h1('PHẦN 10: IMPORT GÓI BẢO DƯỠNG TỪ FILE EXCEL')
    w.h2('1. Các bước nhập dữ liệu')
    w.step(['Bước 1: Tại màn hình danh sách, bấm ', ic('btn_import'), '. Hệ thống mở cửa sổ “Import gói bảo dưỡng”.'])
    w.image(s('07_import_open'), caption='Cửa sổ Import gói bảo dưỡng khi vừa mở')
    w.step(['Bước 2: Bấm ', ic('btn_taifilemau'), ' để lấy file Mau_import_goi_bao_duong.xlsx và điền dữ liệu (cấu trúc 5 sheet ở mục 2). Dòng 2 của mỗi sheet là dòng gợi ý, dữ liệu bắt đầu từ dòng 3.'])
    w.step(['Bước 3: Bấm ', ic('btn_chonfile'), ', chọn file vừa điền, rồi bấm ', ic('btn_load'), '. Dữ liệu hiện lên bảng xem trước theo từng tab sheet, ô Tổng cho biết đọc được bao nhiêu gói.'])
    w.step(['Bước 4: Bấm ', ic('btn_validate'), ' để hệ thống kiểm tra từng dòng. Bước này CHƯA ghi dữ liệu.'])
    w.image(s('09_import_validated'), caption='Kết quả kiểm tra — dòng lỗi tô đỏ, lý do ghi ngay dưới dòng')
    w.p('Sau khi kiểm tra, hệ thống hiện ba con số Tổng / Hợp lệ / Lỗi và dòng thông báo “Còn N dòng lỗi (xem tab có dấu đỏ)…”. Tab sheet nào có lỗi hiện số lỗi màu đỏ; dòng hợp lệ bị khóa, không sửa được nữa.')
    w.image(s('10_import_tab3'), caption='Lỗi ở sheet 3. Nội dung kiểm tra')
    w.step(['Bước 5: Sửa trực tiếp các dòng lỗi rồi bấm Validate lại. Không muốn nhập các dòng lỗi thì bấm ', ic('btn_bodongloi'), ' (bỏ luôn các dòng con của gói bị bỏ) rồi Validate lại. Muốn sửa cả dòng đã khóa thì bấm ', ic('btn_xoavalidate'), '.'])
    w.image(s('11_import_ok'), caption='Tất cả gói đã hợp lệ — nút Import sáng lên')
    w.step(['Bước 6: Bấm ', ic('btn_import_modal'), '. Nút này chỉ bấm được khi đã Validate và không còn dòng lỗi. Hệ thống báo “Import thành công N gói bảo dưỡng.”, đóng cửa sổ và nạp lại danh sách.'])
    w.p('Đóng cửa sổ khi đã tải dữ liệu lên bảng, hệ thống hỏi “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”.')

    w.h2('2. Cấu trúc file mẫu')
    w.table([
        ['Sheet', 'Cột (dấu * là bắt buộc)', 'Ghi chú'],
        ['1. Gói bảo dưỡng', 'Mã gói*, Tên gói*, Công ty quản lý*, VAT (%), Định mức đàm phán giá (%), Hệ số giá bán, Ghi chú', 'Mỗi dòng là một gói.'],
        ['2. Cấp bảo dưỡng', 'Mã gói*, Cấp bảo dưỡng*, Định mức công*, Hệ số công nghệ, Giá bán cơ sở, Gợi ý hàng hoá', 'Mỗi dòng là một cấp của gói. Gợi ý hàng hóa nhiều giá trị ngăn bằng dấu ;'],
        ['3. Nội dung kiểm tra', 'Mã gói*, STT hạng mục*, Nội dung kiểm tra bảo dưỡng*, ĐVT*, SL*, Cấp bảo dưỡng*, Ghi chú kiểm tra*', 'Mỗi dòng là một ô giao (hạng mục × cấp). Nội dung/ĐVT/SL chỉ cần ghi ở dòng đầu của hạng mục. Ghi chú kiểm tra ghi TÊN đầy đủ, nhiều giá trị ngăn bằng dấu ;'],
        ['4. Hệ số theo công ty', 'Mã gói*, Công ty*, Hệ số*', 'Không bắt buộc có dòng.'],
        ['5. Hàng hoá', 'Mã gói*, Mã hàng*, Nhóm hàng*', 'Không bắt buộc có dòng.'],
    ], widths=[1.2, 2.6, 2.2])
    w.p('Tên công ty, cấp bảo dưỡng, ĐVT, ghi chú kiểm tra, nhóm hàng phải ghi đúng tên trong danh mục (không phân biệt hoa thường). Cấp bảo dưỡng, ghi chú kiểm tra, ĐVT, nhóm hàng phải đang Hoạt động.')

    w.h2('3. Các lỗi thường gặp khi kiểm tra dữ liệu')
    w.table([
        ['Thông báo', 'Nguyên nhân'],
        ['Mã gói / Tên gói không được để trống', 'Dòng bỏ trống cột bắt buộc.'],
        ['Mã gói / Tên gói đã tồn tại trong hệ thống', 'Danh mục đã có gói trùng mã/tên.'],
        ['Mã gói / Tên gói bị trùng với dòng N trong file', 'Hai dòng trong file trùng nhau.'],
        ['Mã gói: Chỉ gồm chữ không dấu, số, dấu - và _', 'Mã có chữ có dấu, khoảng trắng hoặc ký tự khác.'],
        ['Mã gói / Tên gói / Ghi chú tối đa 255 ký tự', 'Nội dung quá dài.'],
        ['Công ty quản lý “X” không có trong danh mục', 'Tên công ty ghi sai.'],
        ['VAT tối đa 100 / Định mức đàm phán giá tối đa 99 / Hệ số giá bán không được nhỏ hơn 1', 'Giá trị số ngoài khoảng cho phép; ô chứa chữ báo “… phải là số”.'],
        ['Chưa khai cấp bảo dưỡng nào ở sheet “2. Cấp bảo dưỡng”', 'Gói không có dòng hợp lệ nào ở sheet 2.'],
        ['Chưa khai nội dung kiểm tra nào ở sheet “3. Nội dung kiểm tra”', 'Gói không có dòng hợp lệ nào ở sheet 3.'],
        ['Sheet “…” dòng N có lỗi', 'Dòng con của gói ở sheet khác bị lỗi nên gói cũng bị đánh lỗi.'],
        ['Mã gói “X” không có ở sheet “1. Gói bảo dưỡng”', 'Dòng ở sheet 2–5 trỏ tới mã gói không có ở sheet 1.'],
        ['Cấp bảo dưỡng “X” không có trong danh mục hoặc đã bị khóa / đã khai ở dòng N', 'Tên cấp sai, cấp đang bị Khóa, hoặc khai trùng cấp cho cùng gói.'],
        ['Cấp bảo dưỡng “X” chưa khai ở sheet “2. Cấp bảo dưỡng”', 'Sheet 3 dùng cấp chưa khai cho gói đó ở sheet 2.'],
        ['ĐVT “X” không có trong danh mục / Ghi chú kiểm tra “X” không có trong danh mục hoặc đã bị khóa', 'Ghi sai tên đơn vị tính, ghi sai tên ghi chú kiểm tra hoặc ghi chú đang bị Khóa.'],
        ['Mã hàng “X” không có trong danh mục hàng hoá / Nhóm hàng “X” không có trong danh mục', 'Mã hàng hoặc tên nhóm hàng ghi sai (sheet 5).'],
    ], widths=[2.6, 2.4])
    w.p('Lưu ý: gói nhập từ Excel luôn ở trạng thái Hoạt động, người tạo là người thực hiện nhập, mã tự chuyển thành chữ in hoa; VAT để trống lưu 0, Hệ số giá bán để trống lưu 1. File Excel KHÔNG nhập được file PDF đính kèm — Người dùng bổ sung PDF sau ở trang Sửa (trang Sửa bắt buộc có ít nhất 1 file PDF mới lưu được).')

    # ================================================================== PHẦN 11
    w.h1('PHẦN 11: IN PHIẾU DANH MỤC KIỂM TRA BẢO DƯỠNG')
    w.step(['Bước 1: Ở cột Hành động, bấm nút ba chấm ', ic('btn_bacham'), ' rồi chọn In (hoặc bấm ', ic('btn_in_footer'), ' ở chân trang màn Chi tiết).'])
    w.step('Bước 2: Hệ thống mở cửa sổ “Xem trước gói bảo dưỡng <mã>” hiển thị phiếu trên khổ giấy.')
    w.image(s('51_print'), caption='Cửa sổ xem trước phiếu Danh mục kiểm tra bảo dưỡng định kỳ')
    w.step('Bước 3: Bấm nút In ở đầu cửa sổ để mở hộp thoại in của trình duyệt.')
    w.p('Nội dung phiếu: logo và thông tin công ty; tiêu đề “DANH MỤC KIỂM TRA BẢO DƯỠNG ĐỊNH KỲ” và dòng “TÊN DỊCH VỤ: <tên gói in hoa>”; bảng STT, Nội dung kiểm tra bảo dưỡng, SL, các cột cấp bảo dưỡng, cột Kiểm tra (Có/Không) và Ghi chú để kỹ thuật viên điền tay; cuối phiếu là Ghi chú của gói, bảng giải thích ký hiệu (KTBM, DK, CC, VS…) và chỗ ký của Kỹ thuật viên, Khách hàng.')

    # ================================================================== PHẦN 12
    w.h1('PHẦN 12: TÙY CHỈNH CỘT HIỂN THỊ')
    w.step(['Bước 1: Ở thanh công cụ của bảng, bấm biểu tượng ', ic('btn_cauhinhcot'), '. Hệ thống mở cửa sổ “Tuỳ chỉnh cột”.'])
    w.image(s('05_colcfg'), caption='Cửa sổ Tuỳ chỉnh cột')
    w.step('Bước 2: Tích để hiện cột, bỏ tích để ẩn cột. Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.')
    w.step(['Bước 3: Bấm ', ic('btn_luu'), ' để áp dụng; bấm Đóng nếu muốn bỏ các thay đổi vừa chỉnh.'])
    w.p('Ba cột STT, Mã và Hành động bị khóa: không bỏ tích và không kéo đổi vị trí được.')
    w.p('Cấu hình cột được ghi nhớ riêng cho từng người dùng, lần sau vào màn hình vẫn giữ nguyên.')

    w.rebuild_toc()
    return w.save(out)


if __name__ == '__main__':
    tmpl = sys.argv[1]
    out = os.path.join(HERE, 'out', 'HDSD_Danh muc goi bao duong.docx')
    print(build(tmpl, out))
