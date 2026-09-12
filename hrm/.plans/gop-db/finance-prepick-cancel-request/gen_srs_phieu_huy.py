# -*- coding: utf-8 -*-
"""Sinh SRS man "Phieu huy hang giu" theo FORM CHUAN 2026-08-28.

Man ANH EM cua "Yeu cau huy hang giu" (gen_srs.py cung thu muc) — DUNG lan lon 2 man:
  · Yeu cau huy hang giu (`PYCHHG-…`) = de nghi huy, KHONG dung toi ton kho.
  · Phieu huy hang giu   (`PHHG-…`)   = chung tu DUYET, chinh luc luu moi TRU TON GIU.

Nguon: code HRM nhanh `gop_db`
  BE  Modules/Finance/{Entities/PrepickCancel/PrepickCancel.php,
      Services/PrepickCancelService.php, Http/Controllers/V1/PrepickCancelController.php,
      Http/Requests/PrepickCancel/PrepickCancelStoreRequest.php, Routes/api.php}
  FE  pages/finance/prepick-cancels/*
Anh chup that: ./phieu_huy_shots (Playwright MCP, 1440x900, ngay 09/09/2026).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, '..', '..', '..', '.claude', 'skills',
                                'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(BASE, 'phieu_huy_shots')
OUT = os.path.join(BASE, 'SRS - Phieu huy hang giu.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Giữ hàng => Phiếu hủy hàng giữ'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/prepick-cancels',
           full_url='https://<host-hrm>/finance/prepick-cancels',
           img_prefix='phhg_')

# ============================================================== TRANG DAU
d.title_block('Phiếu hủy hàng giữ')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu hủy hàng giữ (mã phiếu PHHG), '
    'nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, luồng lập phiếu và phân quyền của màn hình.',
    'Làm rõ bản chất của màn hình: lập một Phiếu hủy hàng giữ CHÍNH LÀ duyệt một Phiếu yêu cầu '
    'hủy hàng giữ đang chờ duyệt, và đây là thời điểm duy nhất tồn hàng giữ bị trừ.',
    'Làm rõ vì sao phiếu không có thao tác Sửa và Xóa: phiếu lập xong là chốt vĩnh viễn.',
    'Làm rõ ý nghĩa của ba cột số lượng “Có thể hủy”, “Yêu cầu hủy” và “Duyệt hủy”.',
    'Làm rõ phạm vi dữ liệu mà mỗi cấp quyền xem được.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hàng giữ', 'Số lượng hàng hóa đang được giữ cho một khách hàng cụ thể, đứng tên một nhân '
                 'viên và có hạn giữ. Đây là số tồn riêng, tách khỏi tồn kho thông thường.'),
    ('Phiếu yêu cầu hủy hàng giữ', 'Chứng từ do nhân viên lập để đề nghị hủy phần hàng mình đang '
                                   'giữ. Mã dạng PYCHHG-NNNNN. Bản thân nó KHÔNG trừ tồn.'),
    ('Phiếu hủy hàng giữ', 'Chứng từ mô tả trong tài liệu này. Mã dạng PHHG-NNNNN. Được lập từ '
                           'một phiếu yêu cầu đang chờ duyệt; lưu phiếu này là duyệt yêu cầu đó '
                           'và trừ tồn hàng giữ.'),
    ('Có thể hủy', 'Số lượng hàng giữ còn lại thực tế của người lập phiếu yêu cầu tại thời điểm '
                   'mở form, đã trừ phần đang nằm trên các đề nghị xuất kho chưa hoàn tất.'),
    ('Yêu cầu hủy', 'Số lượng người lập phiếu yêu cầu đã đề nghị hủy. Chỉ để tham khảo.'),
    ('Duyệt hủy', 'Số lượng người lập phiếu hủy thực sự quyết định hủy. Đây là số bị trừ khỏi '
                  'tồn hàng giữ.'),
    ('Lô hàng giữ', 'Một phần hàng giữ có cùng hạn giữ. Một hàng hóa có thể nằm trên nhiều lô.'),
    ('Trừ theo hạn giữ sớm trước', 'Quy tắc trừ tồn: lô nào hết hạn giữ sớm hơn thì bị trừ trước, '
                                   'trừ hết lô này mới sang lô kế tiếp.'),
    ('Đơn vị cơ bản', 'Đơn vị tính gốc của hàng hóa. Tồn hàng giữ luôn ghi theo đơn vị này.'),
], widths=[1.6, 4.9])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Màn hình dùng lại bộ quyền sẵn có của nhóm nghiệp vụ Giữ hàng, KHÔNG khai thêm quyền riêng '
    'cho Thêm / Sửa / Xóa. Lý do: phiếu hủy chỉ có duy nhất một thao tác ghi là lập phiếu, và '
    'thao tác đó chính là duyệt nên đã được kiểm soát bằng quyền Quản lý giữ hàng.')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý giữ hàng',
     'Được lập Phiếu hủy hàng giữ (tức duyệt phiếu yêu cầu). Thiếu quyền này thì cửa sổ chọn '
     'phiếu yêu cầu luôn rỗng và hệ thống từ chối khi lưu.'),
], widths=[0.8, 1.9, 3.8])

d.p('Nhóm quyền quyết định phạm vi dữ liệu (chọn cấp cao nhất mà người dùng có):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng giữ theo tổng công ty', 'Xem mọi phiếu hủy của mọi công ty.'),
    ('V2', 'Xem phiếu hàng giữ theo công ty', 'Xem phiếu hủy thuộc công ty của mình.'),
], widths=[0.8, 1.9, 3.8])

d.p('Ba quy tắc chung:')
d.bullets([
    'Người không có quyền nào ở hai nhóm trên vẫn xem được phiếu hủy do chính mình lập, và '
    'phiếu hủy sinh ra từ phiếu yêu cầu do chính mình lập.',
    'Người có quyền Quản lý giữ hàng xem được mọi phiếu hủy thuộc công ty mình, tương đương V2.',
    'Màn hình này CHỈ có hai cấp phạm vi (tổng công ty, công ty) — khác màn Yêu cầu hủy hàng giữ '
    'vốn có thêm cấp phòng ban. Đây là chủ ý bám theo hệ thống cũ.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1/V2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách phiếu', '✅', '✅', '✅ (chỉ phiếu liên quan tới mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột hiển thị', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu hủy hàng giữ', '✅', '❌', '❌'),
    ('FR-06 Chọn phiếu yêu cầu từ cửa sổ tra cứu', '✅', '❌', '❌'),
    ('FR-07 Xem chi tiết phiếu', '✅', '✅', '✅ (chỉ phiếu liên quan tới mình)'),
    ('FR-08 In phiếu', '✅', '✅', '✅ (chỉ phiếu liên quan tới mình)'),
    ('FR-09 Xem lịch sử thay đổi', '✅', '✅', '✅ (chỉ phiếu liên quan tới mình)'),
    ('FR-10 Xuất Excel danh sách', '✅', '✅', '✅'),
], widths=[2.6, 0.5, 0.7, 2.2])

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [('Người quản lý giữ hàng', [0, 1, 2]),
     ('Nhân viên kinh doanh', [0, 2])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu hủy hàng giữ', 'crud'),
     ('FR-07', 'Xem chi tiết phiếu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-10', 'Xuất Excel danh sách', 'io', 'extend', [0], None),
     ('FR-06', 'Chọn phiếu yêu cầu từ cửa sổ tra cứu', 'crud', 'include', [1], None),
     ('FR-08', 'In phiếu', 'io', 'extend', [2], None),
     ('FR-09', 'Xem lịch sử thay đổi', 'view', 'extend', [2], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu hủy hàng giữ')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách phiếu')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu hủy hàng giữ tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu hủy hàng giữ',
    mota='Hiển thị bảng phiếu hủy nằm trong phạm vi dữ liệu của người đăng nhập, kèm bộ lọc, '
         'phân trang và ô thống kê tổng số phiếu khớp bộ lọc.',
    tacnhan='Người quản lý giữ hàng; Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào menu Tài chính → Giữ hàng → Phiếu hủy hàng giữ.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem của người dùng.\n'
          '3. Hệ thống trả về trang đầu tiên của danh sách và tổng số phiếu.\n'
          '4. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Bộ lọc đã lưu của lần vào trước còn hiệu lực thì được khôi phục lại.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('phhg-01-danh-sach.png'),
         shot_caption='Màn Phiếu hủy hàng giữ lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Phiếu hủy hàng giữ',
     'Tiêu đề cố định phía trên bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở màn lập phiếu hủy. Người thiếu quyền Quản lý giữ hàng vẫn mở được màn nhưng cửa sổ '
     'chọn phiếu yêu cầu sẽ không có dòng nào.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ chọn trường xuất; bị khóa trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cột cố định, không tắt được.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PHHG-NNNNN', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết. Cột cố định, sắp xếp được.'),
    ('Cột Phiếu yêu cầu', 'Table/Grid', 'Read-only', 'PYCHHG-NNNNN', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết của phiếu yêu cầu gốc. Không có thì để trống.'),
    ('Cột Người yêu cầu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người lập phiếu yêu cầu gốc, KHÔNG phải người lập phiếu hủy.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người lập phiếu hủy, tức người đã duyệt.'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Đã đề nghị', 'Theo dữ liệu',
     'Thực tế mọi phiếu đều ở trạng thái Đã đề nghị, màu xanh lá — phiếu hủy không có vòng đời.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Trùng với người tạo và ngày tạo vì phiếu không sửa được.'),
    ('Cột Khách hàng / Ghi chú', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Bật lên trong cửa sổ Tuỳ chỉnh cột.'),
    ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Cột cố định cuối bảng. Chỉ có hai nút In và Lịch sử — KHÔNG có Sửa, Xóa.'),
    ('Nút In', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ xem trước bản in của phiếu.'),
    ('Nút Lịch sử', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ lịch sử thao tác của phiếu.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, 10 dòng', '–'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện dòng “Không có dữ liệu phù hợp.” khi không có phiếu nào khớp.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị',
     'Hiện ngay khi vào màn và trong lúc nạp lại dữ liệu.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định cấp quyền xem của người dùng theo thứ tự ưu tiên tổng công ty → '
     'công ty → chỉ phiếu liên quan tới mình.\n'
     'During:\n– Áp phạm vi dữ liệu; người có quyền Quản lý giữ hàng được xem mọi phiếu thuộc '
     'công ty mình.\n'
     '– Khôi phục bộ lọc đã lưu của người dùng nếu còn hiệu lực (10 phút).\n'
     'After:\n– Trả về trang 1, tổng số phiếu và danh sách trạng thái để đổ vào ô lọc.'),
    ('Bấm vào mã phiếu', 'Click',
     'Before:\n– Kiểm tra người dùng có được xem phiếu này không.\n'
     '– Nếu không → hệ thống báo không có quyền xem phiếu và không mở màn chi tiết.\n'
     'After:\n– Mở màn chi tiết của phiếu hủy.'),
    ('Bấm vào mã phiếu yêu cầu', 'Click',
     'After:\n– Mở màn chi tiết của phiếu yêu cầu hủy hàng giữ đã sinh ra phiếu này.'),
    ('Bấm tiêu đề cột có mũi tên sắp xếp', 'Click',
     'During:\n– Chỉ ba cột Mã phiếu, Ngày tạo, Ngày cập nhật sắp xếp được.\n'
     'After:\n– Nạp lại danh sách từ trang 1 theo thứ tự mới, giữ nguyên bộ lọc.'),
    ('Bấm số trang / nút tiến lùi / đổi số dòng mỗi trang', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu trang mới; số thứ tự tiếp tục liên tục.'),
])

# ------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các tiêu chí lọc riêng của '
           'màn Phiếu hủy hàng giữ tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu hủy',
    mota='Thu hẹp danh sách theo ô tìm nhanh và bảy tiêu chí lọc nâng cao.',
    tacnhan='Người quản lý giữ hàng; Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách Phiếu hủy hàng giữ.',
    chinh='1. Người dùng gõ vào ô tìm nhanh hoặc mở khu vực Tìm kiếm nâng cao.\n'
          '2. Người dùng nhập / chọn các tiêu chí cần lọc.\n'
          '3. Người dùng bấm Tìm kiếm.\n'
          '4. Hệ thống nạp lại danh sách từ trang 1 theo điều kiện lọc, trong phạm vi quyền.',
    phu='• Bấm Làm mới → xóa toàn bộ điều kiện lọc và thứ tự sắp xếp rồi nạp lại danh sách.\n'
        '• Đổi giá trị một ô lọc bất kỳ (trừ ô tìm nhanh) → hệ thống tự nạp lại, không cần bấm '
        'Tìm kiếm.\n'
        '• Không có phiếu nào khớp → bảng hiện dòng “Không có dữ liệu phù hợp.”.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('phhg-02-bo-loc-nang-cao.png'),
         shot_caption='Khu vực Tìm kiếm nâng cao đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm đồng thời theo mã phiếu hủy, mã phiếu yêu cầu và tên người tạo. '
     'Chỉ áp dụng khi bấm Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng toàn bộ điều kiện lọc.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Xóa hết điều kiện lọc và tự nạp lại danh sách.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đóng / mở khu vực lọc nâng cao.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ chọn và sắp xếp các ô lọc.'),
    ('Ô lọc Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống',
     'Giá trị lấy từ hệ thống. Thực tế mọi phiếu đều là Đã đề nghị nên hai lựa chọn còn lại '
     'luôn cho kết quả rỗng; giữ đủ ba lựa chọn để khớp với hệ thống cũ.'),
    ('Ô lọc Mã phiếu yêu cầu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm gần đúng theo mã phiếu yêu cầu gốc.'),
    ('Ô lọc Người yêu cầu', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu yêu cầu gốc.'),
    ('Ô lọc Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu hủy.'),
    ('Ô lọc Tên/mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Một ô tìm cả tên lẫn mã hàng hóa có trong chi tiết phiếu.'),
    ('Ô lọc Ngày tạo từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo ngày tạo phiếu hủy.'),
    ('Ô lọc Ngày tạo đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo ngày tạo phiếu hủy.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm', 'Click',
     'During:\n– Gom toàn bộ điều kiện đang nhập, kể cả ô tìm nhanh.\n'
     'After:\n– Nạp lại danh sách từ trang 1; ô “Hiển thị a–b / N” cập nhật theo kết quả mới.'),
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'After:\n– Tự nạp lại danh sách từ trang 1, không cần bấm Tìm kiếm.'),
    ('Bấm Làm mới', 'Click',
     'During:\n– Xóa toàn bộ điều kiện lọc và thứ tự sắp xếp.\n'
     'After:\n– Nạp lại danh sách mặc định từ trang 1.'),
    ('Rời màn rồi quay lại trong vòng 10 phút', 'System',
     'After:\n– Khôi phục lại bộ lọc và trạng thái đóng/mở của khu vực lọc nâng cao.'),
])

# ------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'view',
            [('include', 'Lưu cấu hình theo người dùng')],
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Bộ lọc và Cấu hình cột.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc hiển thị',
    mota='Cho phép người dùng tự chọn ô lọc nào được hiện và sắp xếp thứ tự các ô lọc.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách Phiếu hủy hàng giữ.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc.\n'
          '2. Cửa sổ hiện danh sách bảy ô lọc kèm ô tích chọn.\n'
          '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình theo từng người dùng và vẽ lại khu vực lọc.',
    phu='• Bấm Khôi phục mặc định → đưa về đủ bảy ô lọc theo thứ tự gốc.\n'
        '• Bấm Đóng → thoát, không lưu thay đổi.',
    dacbiet='Cấu hình lưu riêng cho từng người dùng, không ảnh hưởng người khác.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('phhg-03-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
     'Nhắc cách tích chọn và kéo thả để sắp xếp.'),
    ('Danh sách ô lọc', 'Table/Grid', 'Enable', 'Bảy ô lọc', 'Không', 'Theo cấu hình đã lưu',
     'Mỗi dòng gồm ô tích chọn, tên ô lọc và tay nắm kéo thả.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi nhận cấu hình và đóng cửa sổ.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đưa về cấu hình gốc của màn.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thoát, không lưu.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi nhận danh sách ô lọc được tích và thứ tự hiện tại.\n'
     'After:\n– Lưu cấu hình theo người dùng, đóng cửa sổ và vẽ lại khu vực lọc.'),
    ('Bấm Khôi phục mặc định', 'Click',
     'After:\n– Đưa danh sách về đủ bảy ô lọc theo thứ tự gốc.'),
    ('Kéo thả một dòng', 'Click', 'After:\n– Đổi vị trí ô lọc trong danh sách.'),
])

# ------------------------------------------------------------ 2.4
d.h3('2.4 Tuỳ chỉnh cột hiển thị')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view',
            [('include', 'Lưu cấu hình theo người dùng')],
            caption='Biểu đồ Use Case — FR-04 Tuỳ chỉnh cột hiển thị')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Cấu hình cột hiển thị.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh cột hiển thị của bảng',
    mota='Cho phép bật / tắt và sắp xếp các cột của bảng danh sách.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách Phiếu hủy hàng giữ.',
    chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
          '2. Cửa sổ hiện danh sách cột kèm ô tích chọn.\n'
          '3. Người dùng tích / bỏ tích và sắp xếp lại.\n'
          '4. Người dùng bấm Lưu; bảng vẽ lại theo cấu hình mới.',
    phu='• Ba cột STT, Mã phiếu và Hành động bị khóa, không tắt được.\n'
        '• Bấm Đóng → thoát, không lưu thay đổi.',
    dacbiet='Cấu hình lưu riêng cho từng người dùng.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột hiển thị', shot=shot('phhg-04-cau-hinh-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột hiển thị')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách cột', 'Table/Grid', 'Enable', 'Mười hai cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột Khách hàng và Ghi chú mặc định tắt.'),
    ('Ô tích chọn của cột bị khóa', 'Icon Button', 'Disable', '–', '–', 'Đang bật',
     'Ba cột STT, Mã phiếu, Hành động luôn hiện.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi nhận cấu hình và vẽ lại bảng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thoát, không lưu.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi nhận các cột được tích và thứ tự.\n'
     'After:\n– Lưu cấu hình theo người dùng và vẽ lại bảng danh sách.'),
    ('Bỏ tích một cột bị khóa', 'Click',
     'During:\n– Hệ thống không cho bỏ tích ba cột STT, Mã phiếu, Hành động.'),
])

# ------------------------------------------------------------ 2.5
d.h3('2.5 Lập phiếu hủy hàng giữ')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Lập phiếu hủy hàng giữ', 'crud',
            [('include', 'Chọn phiếu yêu cầu từ cửa sổ tra cứu'),
             ('include', 'Kiểm tra quyền Quản lý giữ hàng'),
             ('include', 'Trừ tồn hàng giữ theo hạn giữ sớm trước'),
             ('extend', 'Sinh mã phiếu tự động')],
            caption='Biểu đồ Use Case — FR-05 Lập phiếu hủy hàng giữ')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo quy tắc chung.', anchor='create')
d.intro_table(
    ten='Lập phiếu hủy hàng giữ (duyệt phiếu yêu cầu)',
    mota='Người quản lý giữ hàng chọn một phiếu yêu cầu đang chờ duyệt, quyết định số lượng hủy '
         'cho từng dòng hàng rồi lưu. Lưu thành công thì phiếu yêu cầu chuyển sang Đã duyệt và '
         'tồn hàng giữ bị trừ ngay.',
    tacnhan='Người quản lý giữ hàng; Người dùng đã đăng nhập',
    dieukien='Người dùng có quyền Quản lý giữ hàng và tồn tại ít nhất một phiếu yêu cầu hủy hàng '
             'giữ đang ở trạng thái Chờ duyệt trong cùng công ty.',
    chinh='1. Người dùng bấm Tạo mới ở màn danh sách.\n'
          '2. Người dùng bấm nút tra cứu để mở cửa sổ chọn phiếu yêu cầu.\n'
          '3. Người dùng chọn một phiếu yêu cầu đang chờ duyệt.\n'
          '4. Hệ thống điền sẵn Người yêu cầu, Phòng ban yêu cầu, Khách hàng và nạp các dòng '
          'hàng hóa được đề nghị hủy, kèm số Có thể hủy tính lại tại thời điểm mở form.\n'
          '5. Người dùng tích / bỏ tích cột Cần hủy và sửa số ở cột Duyệt hủy nếu cần.\n'
          '6. Người dùng bấm Duyệt và xác nhận trên hộp thoại cảnh báo trừ tồn.\n'
          '7. Hệ thống lưu phiếu, trừ tồn hàng giữ, chuyển phiếu yêu cầu sang Đã duyệt, ghi lịch '
          'sử cho cả hai phiếu và thông báo cho người lập phiếu yêu cầu.\n'
          '8. Hệ thống báo thành công và quay về màn danh sách.',
    phu='• Chưa chọn phiếu yêu cầu → nút Duyệt bị ẩn, bảng chi tiết hiện dòng “Chưa chọn phiếu '
        'yêu cầu”.\n'
        '• Số ở ô Duyệt hủy vượt quá số Có thể hủy → báo lỗi đỏ ngay dưới ô, không gọi lưu.\n'
        '• Trong lúc người dùng đang mở form mà phiếu yêu cầu bị người khác duyệt mất → hệ thống '
        'báo phiếu không còn ở trạng thái chờ duyệt và không lưu.\n'
        '• Tồn hàng giữ không đủ tại thời điểm lưu → toàn bộ thao tác bị hủy bỏ, không trừ một '
        'phần.\n'
        '• Bấm Duyệt và tiếp tục → lưu xong ở lại màn để chọn phiếu yêu cầu kế tiếp.\n'
        '• Bấm Hủy trên hộp thoại xác nhận → không lưu, giữ nguyên dữ liệu đang nhập.',
    dacbiet='Đây là thao tác KHÔNG THỂ HOÀN TÁC. Phiếu lập xong không sửa, không xóa được.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('phhg-09-tao-moi-chua-chon.png'),
         shot_caption='Màn Lập phiếu hủy hàng giữ khi chưa chọn phiếu yêu cầu')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('phhg-11-tao-moi-da-chon.png'),
         shot_caption='Màn Lập phiếu hủy hàng giữ sau khi đã chọn phiếu yêu cầu')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng Người tạo · ngày giờ', 'Label', 'Read-only', '–', '–', 'Người đăng nhập, ngày hôm nay',
     'Nằm góc phải khối Thông tin chung.'),
    ('Ô Phiếu yêu cầu hủy hàng giữ', 'Textbox', 'Read-only', 'PYCHHG-NNNNN', 'Có', 'Trống',
     'Không gõ tay được, chỉ điền qua cửa sổ tra cứu. Placeholder “Chưa chọn phiếu yêu cầu”.'),
    ('Nút tra cứu phiếu yêu cầu', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ chọn phiếu yêu cầu đang chờ duyệt.'),
    ('Ô Người yêu cầu', 'Textbox', 'Disable', '–', 'Không', 'Trống',
     'Tự điền theo phiếu yêu cầu. Placeholder “Tự điền theo phiếu yêu cầu”.'),
    ('Ô Phòng ban yêu cầu', 'Textbox', 'Disable', '–', 'Không', 'Trống',
     'Tự điền theo phiếu yêu cầu.'),
    ('Ô Khách hàng', 'Textbox', 'Disable', '–', 'Không', 'Trống', 'Tự điền theo phiếu yêu cầu.'),
    ('Ô Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Ghi chú riêng của phiếu hủy, không lấy từ phiếu yêu cầu.'),
    ('Cột Cần hủy', 'Icon Button', 'Enable', '–', 'Không', 'Đang tích',
     'Bỏ tích thì dòng bị làm mờ, ô Duyệt hủy bị khóa và dòng đó không bị kiểm tra.'),
    ('Cột Tên hàng hóa / Model / Mã hàng hóa / Thương hiệu', 'Table/Grid', 'Read-only', '–', '–',
     'Theo dữ liệu', 'Lấy từ dòng của phiếu yêu cầu, không sửa được.'),
    ('Cột Có thể hủy', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
     'Tồn hàng giữ còn lại của người lập phiếu yêu cầu, tính lại tại thời điểm mở form.'),
    ('Cột Yêu cầu hủy', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
     'Số người lập phiếu yêu cầu đã đề nghị. Chỉ để tham khảo, KHÔNG chặn số duyệt.'),
    ('Ô Duyệt hủy', 'Number', 'Enable / Disable', '> 0 và ≤ Có thể hủy', 'Có',
     'Bằng số Yêu cầu hủy',
     'Bị khóa khi bỏ tích Cần hủy. Nhập sai thì báo đỏ ngay dưới ô và giữ nguyên số đã gõ.'),
    ('Cột ĐVT', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Luôn là đơn vị cơ bản của hàng hóa, không đổi được.'),
    ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện sau khi đã chọn phiếu yêu cầu.'),
    ('Nút Duyệt và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện ở màn lập phiếu độc lập, sau khi đã chọn phiếu yêu cầu.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện khi ô Duyệt hủy sai; kèm một thông báo chung “Bạn chưa nhập đầy đủ thông tin.”.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn một phiếu yêu cầu ở cửa sổ tra cứu', 'Click',
     'During:\n– Nạp thông tin phiếu yêu cầu và các dòng hàng được đề nghị hủy.\n'
     '– Tính lại số Có thể hủy của từng hàng theo tồn hàng giữ hiện tại của người lập yêu cầu.\n'
     'After:\n– Điền sẵn ô Duyệt hủy bằng số Yêu cầu hủy và tích sẵn cột Cần hủy.'),
    ('Nhập ô Duyệt hủy', 'Change / Blur',
     'During:\n– Bỏ trống → hiển thị “Chưa nhập số lượng”.\n'
     '– Nhập ký tự không phải số → hiển thị “Chỉ được nhập số”.\n'
     '– Nhập số nhỏ hơn hoặc bằng 0 → hiển thị “Phải lớn hơn 0”.\n'
     '– Nhập vượt số Có thể hủy → hiển thị “Không được vượt {số có thể hủy}”.\n'
     '– Hệ thống KHÔNG tự sửa số người dùng vừa gõ.'),
    ('Bỏ tích ô Cần hủy', 'Click',
     'After:\n– Khóa ô Duyệt hủy của dòng đó, xóa lỗi đang treo và bỏ dòng khỏi phần kiểm tra.'),
    ('Bấm Duyệt', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng.\n'
     '– Nếu không có quyền → hệ thống từ chối và báo không đủ quyền duyệt.\n'
     'During:\n– Kiểm tra lại toàn bộ dòng đang tích; còn lỗi → hiển thị “Bạn chưa nhập đầy đủ '
     'thông tin.”, đưa con trỏ về ô lỗi đầu tiên và KHÔNG lưu.\n'
     '– Không tích dòng nào hoặc mọi dòng đều bằng 0 → hiển thị “Phải chọn ít nhất 1 hàng hoá '
     'cần hủy với số lượng lớn hơn 0”.\n'
     '– Hiển thị hộp thoại xác nhận nêu rõ thao tác sẽ trừ tồn và không hoàn tác.\n'
     'After:\n– Khóa phiếu yêu cầu, kiểm tra lại phiếu còn ở trạng thái Chờ duyệt.\n'
     '– Tạo phiếu hủy, sinh mã dạng PHHG-NNNNN.\n'
     '– Trừ tồn hàng giữ theo thứ tự hạn giữ sớm trước và ghi nhật ký biến động hàng giữ.\n'
     '– Chuyển phiếu yêu cầu sang Đã duyệt, ghi người duyệt và thời điểm duyệt.\n'
     '– Ghi một dòng lịch sử cho phiếu hủy và một dòng cho phiếu yêu cầu.\n'
     '– Gửi thông báo cho người lập phiếu yêu cầu.\n'
     '– Hiển thị thông báo “Duyệt phiếu thành công” và quay về màn danh sách.'),
    ('Bấm Duyệt và tiếp tục', 'Click',
     'After:\n– Xử lý y như nút Duyệt, nhưng lưu xong thì ở lại màn lập phiếu để chọn phiếu yêu '
     'cầu kế tiếp.'),
    ('Bấm Hủy trên hộp thoại xác nhận', 'Click',
     'After:\n– Đóng hộp thoại, không lưu, giữ nguyên dữ liệu đang nhập.'),
    ('Rời màn khi chưa lưu', 'System',
     'During:\n– Hiển thị cảnh báo dữ liệu chưa được lưu và hỏi có rời đi không.'),
])

# ------------------------------------------------------------ 2.6
d.h3('2.6 Chọn phiếu yêu cầu từ cửa sổ tra cứu')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chọn phiếu yêu cầu từ cửa sổ tra cứu', 'crud',
            [('include', 'Lọc phiếu đang chờ duyệt trong cùng công ty')],
            caption='Biểu đồ Use Case — FR-06 Chọn phiếu yêu cầu từ cửa sổ tra cứu')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', anchor='search')
d.intro_table(
    ten='Chọn phiếu yêu cầu hủy hàng giữ cần duyệt',
    mota='Cửa sổ liệt kê các phiếu yêu cầu đang ở trạng thái Chờ duyệt thuộc công ty của người '
         'đăng nhập, để chọn ra phiếu cần lập phiếu hủy.',
    tacnhan='Người quản lý giữ hàng; Người dùng đã đăng nhập',
    dieukien='Đang ở màn Lập phiếu hủy hàng giữ.',
    chinh='1. Người dùng bấm nút tra cứu bên phải ô Phiếu yêu cầu hủy hàng giữ.\n'
          '2. Cửa sổ hiện danh sách phiếu chờ duyệt, mới nhất lên trước.\n'
          '3. Người dùng có thể lọc theo Mã phiếu hoặc Người tạo.\n'
          '4. Người dùng bấm vào một dòng bất kỳ để chọn.\n'
          '5. Cửa sổ đóng lại và form được điền sẵn theo phiếu vừa chọn.',
    phu='• Người dùng không có quyền Quản lý giữ hàng → danh sách luôn rỗng.\n'
        '• Không còn phiếu nào chờ duyệt → cửa sổ hiện trạng thái rỗng.\n'
        '• Bấm ra ngoài hoặc nút đóng → thoát, không chọn gì.',
    dacbiet='Bấm vào bất kỳ vị trí nào trên dòng cũng là chọn, không cần bấm đúng một nút.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Chọn phiếu yêu cầu',
         modal='Chọn phiếu yêu cầu hủy hàng giữ',
         shot=shot('phhg-10-popup-chon-phieu-yeu-cau.png'),
         shot_caption='Cửa sổ chọn phiếu yêu cầu đang chờ duyệt')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô lọc Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm gần đúng theo mã phiếu yêu cầu.'),
    ('Ô lọc Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu yêu cầu.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Số thứ tự liên tục', '–'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PYCHHG-NNNNN', '–', 'Theo dữ liệu', '–'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Người lập phiếu yêu cầu.'),
    ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', '–', 'Theo dữ liệu', '–'),
    ('Phân trang', 'Pagination', 'Enable', '10 dòng mỗi trang', '–', 'Trang 1', '–'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện khi không còn phiếu nào chờ duyệt trong phạm vi của người dùng.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở cửa sổ', 'System',
     'Before:\n– Kiểm tra người dùng có quyền Quản lý giữ hàng không.\n'
     '– Không có quyền → trả về danh sách rỗng.\n'
     'During:\n– Lọc phiếu yêu cầu ở trạng thái Chờ duyệt, thuộc công ty của người đăng nhập.\n'
     'After:\n– Hiển thị trang đầu, sắp xếp mới nhất lên trước.'),
    ('Bấm vào một dòng', 'Click',
     'After:\n– Đóng cửa sổ và nạp dữ liệu phiếu yêu cầu đó vào form lập phiếu hủy.'),
    ('Nhập ô lọc rồi tìm', 'Change',
     'After:\n– Nạp lại danh sách trong cửa sổ theo điều kiện lọc.'),
])

# ------------------------------------------------------------ 2.7
d.h3('2.7 Xem chi tiết phiếu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu hủy hàng giữ',
    mota='Hiển thị toàn bộ thông tin của một phiếu hủy ở chế độ chỉ đọc, kèm bảng chi tiết hàng '
         'hóa và khối lịch sử thay đổi.',
    tacnhan='Người quản lý giữ hàng; Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Phiếu tồn tại và nằm trong phạm vi xem của người dùng.',
    chinh='1. Người dùng bấm vào mã phiếu ở màn danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Màn chi tiết hiển thị Thông tin chung, bảng Chi tiết và khối Lịch sử thay đổi.',
    phu='• Người dùng không có quyền xem phiếu → hệ thống báo không có quyền và không mở màn.\n'
        '• Ô Kho thường để trống vì hàng giữ tính theo nhân viên chứ không theo kho.\n'
        '• Không có nút Sửa và Xóa ở màn này.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('phhg-06-chi-tiet.png'),
         shot_caption='Màn Chi tiết phiếu hủy hàng giữ')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu hủy hàng giữ: {mã phiếu}', '–'),
    ('Dòng Người tạo · ngày giờ', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Nằm góc phải khối Thông tin chung.'),
    ('Ô Mã phiếu', 'Textbox', 'Disable', 'PHHG-NNNNN', 'Theo dữ liệu', 'Chỉ có ở màn chi tiết.'),
    ('Ô Phiếu yêu cầu hủy hàng giữ', 'Textbox', 'Disable', 'PYCHHG-NNNNN', 'Theo dữ liệu', '–'),
    ('Ô Người yêu cầu', 'Textbox', 'Disable', '–', 'Theo dữ liệu', 'Người lập phiếu yêu cầu gốc.'),
    ('Ô Phòng ban yêu cầu', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '–'),
    ('Ô Khách hàng', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '–'),
    ('Ô Kho', 'Textbox', 'Disable', '–', 'Trống',
     'Chỉ có ở màn chi tiết. Thường để trống vì hàng giữ không gắn kho.'),
    ('Ô Ghi chú', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '–'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Yêu cầu hủy, Duyệt hủy, ĐVT. '
     'KHÔNG có cột Cần hủy và Có thể hủy như màn lập phiếu.'),
    ('Khối Lịch sử thay đổi', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Bấm Xem lịch sử mới nạp dữ liệu.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ xem trước bản in.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu: người lập phiếu hủy, người lập phiếu yêu cầu gốc, '
     'người có quyền Quản lý giữ hàng, hoặc người có quyền xem theo tổng công ty / công ty.\n'
     '– Không thuộc nhóm nào → hệ thống báo không có quyền và không mở màn.\n'
     'After:\n– Hiển thị dữ liệu phiếu ở chế độ chỉ đọc.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về màn danh sách Phiếu hủy hàng giữ.'),
])

# ------------------------------------------------------------ 2.8
d.h3('2.8 In phiếu')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'In phiếu hủy hàng giữ', 'io',
            [('include', 'Kiểm tra quyền xem phiếu')],
            caption='Biểu đồ Use Case — FR-08 In phiếu')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX.', anchor='notice')
d.intro_table(
    ten='In phiếu hủy hàng giữ',
    mota='Mở cửa sổ xem trước bản in của một phiếu hủy rồi gửi lệnh in.',
    tacnhan='Người quản lý giữ hàng; Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Phiếu tồn tại và nằm trong phạm vi xem của người dùng.',
    chinh='1. Người dùng bấm nút In ở dòng danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống dựng nội dung bản in và mở cửa sổ xem trước.\n'
          '3. Người dùng bấm In trong cửa sổ để gửi lệnh in.',
    phu='• Không có quyền xem phiếu → hệ thống từ chối, không mở cửa sổ.\n'
        '• Bấm đóng → thoát khỏi cửa sổ xem trước.',
    dacbiet='Bản in lấy tiêu đề công ty theo công ty ghi trên phiếu, không theo người đang đăng '
            'nhập.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In', shot=shot('phhg-08-in-phieu.png'),
         shot_caption='Cửa sổ xem trước bản in phiếu hủy hàng giữ')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Xem trước phiếu hủy hàng giữ', '–'),
    ('Nội dung bản in', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm tiêu đề công ty, số phiếu, ngày tạo, phiếu yêu cầu, người yêu cầu, phòng ban, khách '
     'hàng, kho, người tạo, bảng hàng hóa và ghi chú.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Gửi lệnh in tới máy in.'),
    ('Nút đóng', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ xem trước.'),
], required=False)

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu; không có quyền → hệ thống từ chối.\n'
     'During:\n– Dựng nội dung bản in theo dữ liệu phiếu.\n'
     'After:\n– Mở cửa sổ xem trước.'),
    ('Bấm In trong cửa sổ', 'Click', 'After:\n– Gửi lệnh in của trình duyệt.'),
])

# ------------------------------------------------------------ 2.9
d.h3('2.9 Xem lịch sử thay đổi')

d.p('2.9.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Hiển thị các mốc thao tác đã diễn ra trên phiếu, mới nhất lên trước.',
    tacnhan='Người quản lý giữ hàng; Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Phiếu tồn tại và nằm trong phạm vi xem của người dùng.',
    chinh='1. Người dùng bấm Lịch sử ở dòng danh sách, hoặc bấm Xem lịch sử ở màn chi tiết.\n'
          '2. Hệ thống nạp danh sách mốc lịch sử.\n'
          '3. Mỗi mốc hiển thị thời điểm, tên thao tác, người thực hiện và ghi chú.',
    phu='• Phiếu chưa có mốc nào → hiện dòng “Chưa có lịch sử thao tác nào.”.\n'
        '• Bấm Làm mới → nạp lại danh sách mốc.\n'
        '• Bấm Thu gọn → đóng khối lịch sử.',
    dacbiet='Phiếu hủy chỉ có duy nhất một loại mốc là Tạo mới, vì phiếu không sửa và không xóa '
            'được.')

d.p('2.9.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Xem lịch sử', shot=shot('phhg-07-lich-su.png'),
         shot_caption='Khối Lịch sử thay đổi ở màn chi tiết')

d.p('2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi', 'Kèm số mốc đang có.'),
    ('Nút Xem lịch sử / Thu gọn', 'Button', 'Enable', '–', 'Thu gọn',
     'Chỉ nạp dữ liệu khi mở lần đầu.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', 'Ẩn', 'Chỉ hiện khi khối đang mở.'),
    ('Mốc lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm thời điểm, tên thao tác, người thực hiện kèm phòng ban và ghi chú số lô đã trừ tồn.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện dòng “Chưa có lịch sử thao tác nào.”.'),
], required=False)

d.p('2.9.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem lịch sử', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu.\n'
     'After:\n– Nạp và hiển thị danh sách mốc, mới nhất lên trước.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Nạp lại danh sách mốc lịch sử.'),
])

# ------------------------------------------------------------ 2.10
d.h3('2.10 Xuất Excel danh sách')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xuất Excel danh sách phiếu', 'io',
            [('include', 'Chọn trường cần xuất')],
            caption='Biểu đồ Use Case — FR-10 Xuất Excel danh sách')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất danh sách phiếu hủy ra Excel',
    mota='Xuất ra tệp Excel toàn bộ phiếu khớp bộ lọc đang áp dụng, với các trường do người dùng '
         'tự chọn.',
    tacnhan='Người quản lý giữ hàng; Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách Phiếu hủy hàng giữ.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Cửa sổ chọn trường mở ra, tích sẵn đúng các cột đang hiện trên bảng.\n'
          '3. Người dùng tích thêm hoặc bỏ bớt trường.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống tải về tệp Excel và báo xuất thành công.',
    phu='• Đang xuất thì nút Xuất Excel bị khóa để tránh bấm hai lần.\n'
        '• Bấm Đóng → thoát, không xuất.\n'
        '• Có lỗi trong lúc xuất → hệ thống báo lỗi khi xuất Excel.',
    dacbiet='Thứ tự cột trong tệp theo đúng thứ tự người dùng tích chọn. Tệp chỉ chứa phiếu '
            'trong phạm vi quyền của người dùng.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('phhg-05-chon-truong-xuat-excel.png'),
         shot_caption='Cửa sổ Chọn trường xuất Excel')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất Excel', '–'),
    ('Danh sách trường', 'Table/Grid', 'Enable', 'Mười trường', 'Có',
     'Theo cột đang hiện trên bảng',
     'Gồm Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người tạo, Ngày tạo, Trạng thái, '
     'Người cập nhật, Ngày cập nhật, Khách hàng, Ghi chú.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thoát, không xuất.'),
])

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ chọn trường, tích sẵn đúng các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Khóa nút để tránh bấm hai lần.\n'
     'During:\n– Lấy dữ liệu theo bộ lọc đang áp dụng và phạm vi quyền của người dùng.\n'
     'After:\n– Dựng tệp Excel theo thứ tự trường đã tích, tải về máy và hiển thị “Xuất Excel '
     'thành công”.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('- Quy tắc chung toàn hệ thống. Bảng dưới đây chỉ liệt kê quy tắc đặc thù của màn '
           'Phiếu hủy hàng giữ.', head='Quy tắc áp dụng', anchor='list')

d.rule_table([
    ('BR-01', 'Lập phiếu hủy chính là duyệt phiếu yêu cầu', [
        '– Hệ thống KHÔNG có thao tác duyệt riêng cho phiếu yêu cầu hủy hàng giữ.',
        '– Phiếu yêu cầu chỉ chuyển sang Đã duyệt khi phiếu hủy được lưu thành công.',
        '– Một phiếu yêu cầu tương ứng đúng một phiếu hủy.',
        '– Chỉ chọn được phiếu yêu cầu đang ở trạng thái Chờ duyệt và thuộc cùng công ty.',
    ], 'Lập phiếu hủy'),
    ('BR-02', 'Thời điểm và cách trừ tồn hàng giữ', [
        '– Tồn hàng giữ bị trừ ngay tại thời điểm lưu phiếu hủy, không có bước nào khác.',
        '– Trừ dần theo thứ tự hạn giữ sớm trước, muộn sau.',
        '– Lô tồn được tìm theo NGƯỜI LẬP PHIẾU YÊU CẦU và công ty của người đó, không phải '
        'người lập phiếu hủy.',
        '– Nếu tổng các lô không đủ thì toàn bộ thao tác bị hủy bỏ, không trừ một phần.',
        '– Mỗi lần trừ đều ghi một dòng nhật ký biến động hàng giữ.',
    ], 'Lập phiếu hủy'),
    ('BR-03', 'Số lượng duyệt hủy', [
        '– Bắt buộc lớn hơn 0 và không vượt quá số Có thể hủy tại thời điểm lưu.',
        '– KHÔNG bị chặn bởi số Yêu cầu hủy: người duyệt được phép duyệt nhiều hơn số đề nghị '
        'miễn là còn đủ hàng giữ.',
        '– Số Có thể hủy được tính lại lúc mở form, đã trừ phần hàng đang nằm trên các đề nghị '
        'xuất kho chưa hoàn tất.',
        '– Vượt khoảng thì báo lỗi ngay dưới ô và giữ nguyên số người dùng đã gõ.',
    ], 'Lập phiếu hủy'),
    ('BR-04', 'Nguồn dữ liệu dòng hàng hóa', [
        '– Chỉ nạp các dòng được tích Cần hủy trên phiếu yêu cầu.',
        '– Tên hàng, model, mã hàng, thương hiệu và đơn vị tính lấy từ dòng của phiếu yêu cầu, '
        'người lập phiếu hủy không sửa được.',
        '– Người lập phiếu hủy chỉ quyết định được số ở cột Duyệt hủy và việc tích Cần hủy.',
        '– Hàng hóa không nằm trong phiếu yêu cầu thì không được đưa vào phiếu hủy.',
    ], 'Lập phiếu hủy'),
    ('BR-05', 'Phiếu hủy không có vòng đời', [
        '– Phiếu lập xong là chốt vĩnh viễn: không sửa, không xóa, không hủy duyệt.',
        '– Trạng thái luôn là Đã đề nghị.',
        '– Màn danh sách và màn chi tiết đều không có nút Sửa và Xóa.',
        '– Ô lọc Trạng thái vẫn giữ đủ ba lựa chọn để khớp với hệ thống cũ, nhưng hai lựa chọn '
        'Chờ duyệt và Đang tạo luôn cho kết quả rỗng.',
    ], ['Xem danh sách', 'Xem chi tiết']),
    ('BR-06', 'Đơn vị tính và hệ số quy đổi', [
        '– Tồn hàng giữ luôn ghi theo đơn vị cơ bản của hàng hóa nên cột ĐVT chỉ hiển thị.',
        '– Số lượng trừ tồn được quy đổi về đơn vị cơ bản trước khi trừ.',
    ], ['Lập phiếu hủy', 'Xem chi tiết']),
    ('BR-07', 'Phạm vi dữ liệu', [
        '– Áp theo thứ tự ưu tiên: tổng công ty → công ty → chỉ phiếu liên quan tới mình.',
        '– Người có quyền Quản lý giữ hàng xem được mọi phiếu thuộc công ty mình.',
        '– Người không có quyền phạm vi nào vẫn xem được phiếu do mình lập và phiếu sinh ra từ '
        'phiếu yêu cầu do mình lập.',
        '– Màn này KHÔNG có cấp phòng ban, khác với màn Yêu cầu hủy hàng giữ.',
        '– Phạm vi này áp cho cả danh sách, màn chi tiết, bản in và tệp Excel xuất ra.',
    ], 'Toàn màn hình'),
    ('BR-08', 'Chống duyệt trùng và duyệt đồng thời', [
        '– Khi lưu, hệ thống khóa phiếu yêu cầu lại rồi mới kiểm tra trạng thái.',
        '– Hai người cùng duyệt một phiếu yêu cầu thì chỉ người lưu trước thành công; người sau '
        'nhận thông báo phiếu không còn ở trạng thái chờ duyệt.',
        '– Mọi bước tạo phiếu, trừ tồn, chuyển trạng thái và ghi lịch sử nằm trong cùng một giao '
        'dịch: hỏng một bước là hủy sạch, không để lại dữ liệu dở dang.',
    ], 'Lập phiếu hủy'),
    ('BR-09', 'Ghi lịch sử và thông báo', [
        '– Lập phiếu hủy ghi một mốc Tạo mới cho phiếu hủy, kèm số lô hàng giữ đã bị trừ.',
        '– Đồng thời ghi một mốc duyệt cho phiếu yêu cầu, ghi rõ mã phiếu hủy đã sinh ra.',
        '– Người lập phiếu yêu cầu nhận được thông báo phiếu của mình đã được duyệt.',
        '– Hai lệnh ghi lịch sử nằm trong cùng giao dịch với phiếu để không bao giờ mất mốc.',
    ], 'Lập phiếu hủy'),
    ('BR-10', 'Ô Kho trên phiếu', [
        '– Phiếu có ô Kho nhưng hệ thống chưa bao giờ ghi giá trị vào đó, nên ô này thường trống.',
        '– Nguyên nhân: hàng giữ tính theo nhân viên và khách hàng, không gắn với kho nào.',
        '– Vẫn giữ ô này để hai cổng hiển thị giống nhau.',
        '– Ô Kho chỉ xuất hiện ở màn chi tiết, không có ở màn lập phiếu.',
    ], ['Xem chi tiết', 'In phiếu']),
])

d.save()
