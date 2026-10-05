# -*- coding: utf-8 -*-
"""Sinh "SRS - Yêu cầu tính giá bán.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/pricing-requests/{index.vue,_id/index.vue,_id/edit.vue}
      components/assign/pricing-request/{PricingRequestFormModal,PricingRequestDetailModal}.vue
      pages/assign/prospective-projects/components/ProspectiveProjectReviewProfilesTab.vue (lối lập yêu cầu)
      components/V2BaseSmartFilterPanel.vue · components/modal/{filter-customization-modal,
      column-customization-modal,export-fields-modal,base-confirm-modal}.vue
      components/subsystem-menu/presale.js (mục "Yêu cầu tính giá bán") · subsystem-menu/sale.js (map quyền)
  BE  Modules/Assign/Routes/api.php (prefix assign/pricing-requests + form-info) · PricingRequestController
      Services/PricingRequestService · Entities/PricingRequest (getStatusList, isDraftOwnedByCurrentUser)
      Http/Requests/PricingRequest/* · Transformers/{PricingRequestResource,DetailPricingRequestResource}
      QuotationController::prepareStoreData / QuotationService (duyệt báo giá -> Đã có báo giá; xoá báo giá)
      ProspectiveProjectService::closeProject · SolutionAdjustmentRequestService::cascadeStopPricingRequests
      app/ExcelExport/ExportColumnRegistry ('pricing_requests')
  Quyền: PermissionsTableSeeder id 1080 "Xây dựng giá bán theo công ty", 1091 "Xây dựng giá bán theo phòng"
Ảnh chụp thật (headless, 1440x900, client :3002): shots/ — chỉ để local.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'Yêu cầu tính giá bán'
MENU = 'Phân hệ CSKH trước bán => Yêu cầu tính giá bán'
MENU_TAO = 'Phân hệ CSKH trước bán => Dự án TKT => Mã dự án => Hồ sơ => Yêu cầu xây dựng giá'
A_KD = 'NV kinh doanh phụ trách dự án'
A_GIA = 'Người xây dựng giá'
TN_ALL = 'NV kinh doanh phụ trách dự án; Người xây dựng giá; Người dùng đã đăng nhập'
DK_ALL = 'Người dùng đã đăng nhập. Danh sách hiển thị theo phạm vi quyền V1 / V2 (Phần 2).'
ICONS = {
    'Phân hệ CSKH trước bán': 'icon_phanhe.png',
    'Yêu cầu tính giá bán': 'icon_man.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Cấu hình cột hiển thị': 'icon_cot.png',
    'Xuất Excel': 'icon_xuat.png',
    'Xuất file': 'icon_xuatfile.png',
    'Mã YCBG': 'icon_ma.png',
    'Sửa': 'icon_sua.png',
    'Xóa': 'icon_xoa.png',
    'Tạo báo giá': 'icon_taobaogia.png',
    'Lưu nháp': 'icon_luunhap.png',
    'Lưu và gửi': 'icon_luugui.png',
    'Dự án TKT': 'icon_duan.png',
    'Hồ sơ': 'icon_tab_hoso.png',
    'Yêu cầu xây dựng giá': 'icon_ycxdg.png',
}
NO_OWNER = ('– Không phải người lập hoặc yêu cầu không còn ở trạng thái “Đang tạo” → nút không hiển thị; gọi thẳng '
            'chức năng thì hệ thống báo lỗi tương ứng ở BR-06 và dừng xử lý.')

OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='ycgb_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Yêu cầu tính giá bán (trên giao diện còn gọi là “Yêu cầu xây '
    'dựng giá”), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn Yêu cầu tính giá bán.',
    'Làm rõ yêu cầu tính giá bán sinh ra từ đâu: NV kinh doanh phụ trách dự án TKT lập yêu cầu từ một hồ sơ trình '
    'duyệt giải pháp đã được duyệt, kèm BOM tổng hợp đã duyệt, rồi gửi cho bộ phận xây dựng giá.',
    'Làm rõ luồng 6 trạng thái (Đang tạo → Chờ xây dựng giá → Đã có báo giá, cùng các nhánh Đóng / Dừng) và việc '
    'người xây dựng giá tiếp nhận yêu cầu bằng thao tác Tạo báo giá.',
    'Làm rõ ai nhìn thấy yêu cầu nào (theo quyền xây dựng giá theo công ty / theo phòng) và ai được sửa, xóa, tạo '
    'báo giá.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Yêu cầu tính giá bán (YCBG)', 'Phiếu NV kinh doanh gửi bộ phận xây dựng giá để lập báo giá cho BOM tổng hợp của '
     'một giải pháp / hạng mục. Trên giao diện hiển thị là “Yêu cầu xây dựng giá”, mã tự sinh dạng YCBG-YYYY-NNNNN.'),
    ('Dự án TKT', 'Dự án tiền khả thi — dự án khách hàng tiềm năng mà yêu cầu thuộc về.'),
    ('NV kinh doanh phụ trách dự án', 'Nhân viên kinh doanh chính của dự án TKT; là người duy nhất được lập yêu cầu.'),
    ('Người xây dựng giá', 'Người có quyền “Xây dựng giá bán theo công ty” hoặc “Xây dựng giá bán theo phòng”; tiếp nhận '
     'yêu cầu bằng cách tạo báo giá.'),
    ('Hồ sơ trình duyệt', 'Hồ sơ giải pháp trình duyệt; chỉ hồ sơ ở trạng thái “Đã duyệt” mới được lập yêu cầu.'),
    ('BOM tổng hợp', 'Danh mục hàng hóa / dịch vụ tổng hợp của giải pháp hoặc hạng mục; phải ở trạng thái “Đã duyệt”.'),
    ('Kiểu triển khai dự án', 'Tự triển khai / Triển khai theo Phòng / Liên phòng ban — quyết định ai được xây dựng giá.'),
    ('Phòng làm GP / PM giải pháp', 'Phòng ban làm giải pháp và quản lý giải pháp của dự án (chỉ để hiển thị).'),
    ('Q / V', 'Ký hiệu quyền thao tác (Q) và quyền phạm vi dữ liệu (V) ở Phần 2.'),
], widths=[1.9, 4.1])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Xây dựng giá bán theo công ty',
     'Nút Tạo báo giá hiện trên yêu cầu “Chờ xây dựng giá” chưa có báo giá; tạo được báo giá cho yêu cầu thuộc dự án '
     '“Liên phòng ban” (hoặc dự án chưa xác định kiểu triển khai). Nhận thông báo khi có yêu cầu mới của các dự án đó.'),
    ('Q2', 'Xây dựng giá bán theo phòng',
     'Như Q1 nhưng chỉ cho yêu cầu thuộc dự án “Triển khai theo Phòng” do nhân viên CÙNG phòng ban với người dùng lập. '
     'Nhận thông báo khi có yêu cầu mới của phòng mình.'),
    ('Q3', 'Vai trò NV kinh doanh phụ trách dự án (không phải quyền trong danh mục phân quyền)',
     'Lập yêu cầu từ tab Hồ sơ của dự án TKT; sửa, gửi, xóa yêu cầu do chính mình lập khi còn “Đang tạo”.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xây dựng giá bán theo công ty (cùng quyền Q1)',
     'Mọi yêu cầu ĐÃ GỬI (mọi trạng thái trừ “Đang tạo”) của dự án “Liên phòng ban” hoặc chưa xác định kiểu triển khai.'),
    ('V2', 'Xây dựng giá bán theo phòng (cùng quyền Q2)',
     'Yêu cầu ĐÃ GỬI của dự án “Triển khai theo Phòng” do nhân viên cùng phòng ban với người dùng lập. Người dùng '
     'chưa gắn phòng ban thì quyền này không mở rộng phạm vi.'),
    ('Không có quyền nào', '–', 'Chỉ yêu cầu do chính người dùng lập, mọi trạng thái (kể cả “Đang tạo”).'),
], widths=[0.8, 2.0, 3.2])
d.p('Có cả V1 và V2 thì cộng 2 phạm vi. Lưu ý: người có V1 hoặc V2 KHÔNG thấy bản nháp “Đang tạo” trên danh sách, '
    'kể cả bản nháp do chính mình lập. Menu “Yêu cầu tính giá bán” của phân hệ CSKH trước bán hiển thị với mọi người '
    'dùng vào được phân hệ.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách yêu cầu tính giá bán', '✅ (V1)', '✅ (V2)', '✅', '✅ (của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '✅', '✅'),
    ('FR-05 Xuất Excel', '✅', '✅', '✅', '✅'),
    ('FR-06 Xem chi tiết yêu cầu', '✅', '✅', '✅', '✅'),
    ('FR-07 Lập yêu cầu tính giá bán', '❌', '❌', '✅', '❌'),
    ('FR-08 Sửa và gửi yêu cầu', '❌', '❌', '✅ (người lập, Đang tạo)', '❌'),
    ('FR-09 Xóa yêu cầu', '❌', '❌', '✅ (người lập, Đang tạo)', '❌'),
    ('FR-10 Tạo báo giá từ yêu cầu', '✅ (dự án Liên phòng ban)', '✅ (dự án theo Phòng, cùng phòng)', '❌', '❌'),
], widths=[2.3, 1.0, 1.1, 1.0, 0.9])

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_KD, [0, 1, 2, 3, 4]), (A_GIA, [0, 1, 5])],
    [('FR-01', 'Xem danh sách yêu cầu', 'view'),
     ('FR-05', 'Xuất Excel', 'io'),
     ('FR-07', 'Lập yêu cầu tính giá bán', 'crud'),
     ('FR-08', 'Sửa và gửi yêu cầu', 'crud'),
     ('FR-09', 'Xóa yêu cầu', 'action'),
     ('FR-10', 'Tạo báo giá từ yêu cầu', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết yêu cầu', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1 Xem danh sách
d.h3('2.1 Xem danh sách yêu cầu tính giá bán')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu tính giá bán tại '
           'phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách yêu cầu tính giá bán',
    mota='Hiển thị các yêu cầu tính giá bán trong phạm vi quyền của người dùng, mới tạo nhất ở trên, kèm BOM, dự án, '
         'khách hàng, báo giá đã lập và trạng thái.',
    tacnhan=TN_ALL,
    dieukien=DK_ALL,
    chinh='1. Người dùng vào menu Yêu cầu tính giá bán.\n'
          '2. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có) và nạp trang 1, 10 dòng/trang.\n'
          '3. Hệ thống hiển thị bảng “Danh sách yêu cầu xây dựng giá” theo phạm vi quyền, sắp xếp Ngày tạo giảm dần.\n'
          '4. Người dùng sắp xếp theo cột, chuyển trang hoặc đổi số dòng/trang.',
    phu='• Không có bản ghi → “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Lỗi khi tải → thông báo “Lỗi tải dữ liệu”, bảng trống.\n'
        '• Bấm Mã YCBG → mở màn chi tiết yêu cầu (FR-06); bấm mã BOM → màn chi tiết BOM; bấm mã báo giá → màn chi '
        'tiết báo giá.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-ds.png'),
         shot_caption='Màn danh sách Yêu cầu tính giá bán (tài khoản có quyền xây dựng giá theo công ty)')
d.figure(shot('01b-ds-phai.png'), 'Các cột bên phải của bảng: ngày gửi, ngày tạo, người cập nhật, trạng thái, hành '
         'động', width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Yêu cầu xây dựng giá', '–'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách yêu cầu xây dựng giá', '–'),
    ('STT', 'Text', 'Read-only', '–', 'Theo trang', 'Cột cố định bên trái.'),
    ('Mã YCBG', 'Link', 'Read-only', 'YCBG-YYYY-NNNNN', 'Theo dữ liệu',
     'Cột cố định bên trái, sắp xếp được. Bấm mở màn chi tiết; chuột phải mở được tab mới.'),
    ('BOM list', 'Link', 'Read-only', '–', 'Theo dữ liệu', '“Mã BOM - Tên BOM”, tối đa 2 dòng; bấm mở chi tiết BOM.'),
    ('Dự án TKT', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“Mã dự án - Tên dự án”, tối đa 2 dòng.'),
    ('Khách hàng', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Khách hàng của dự án.'),
    ('Phòng làm GP', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Phòng ban làm giải pháp của dự án.'),
    ('PM giải pháp', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Người quản lý giải pháp.'),
    ('Báo giá', 'Link', 'Read-only', '–', 'Trống khi chưa có', 'Mã báo giá đã lập từ yêu cầu; bấm mở chi tiết báo giá.'),
    ('Deadline', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Người yêu cầu', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“Tên nhân viên - Mã phòng” của người lập.'),
    ('Ngày gửi', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Trống khi chưa gửi', 'Sắp xếp được.'),
    ('Ngày tạo', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Sắp xếp được; mặc định giảm dần.'),
    ('Người cập nhật', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“Tên nhân viên - Mã phòng”.'),
    ('Ngày cập nhật', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Trạng thái', 'Badge', 'Read-only', 'Danh sách 6 giá trị', 'Theo dữ liệu',
     'Đang tạo (xám) · Chờ xây dựng giá (cam) · Đang xây dựng giá (xanh dương) · Đã có báo giá (xanh lá) · Đóng (xám '
     'đậm) · Dừng (đỏ). Chữ và màu do hệ thống trả về.'),
    ('Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
     'Cột cuối, cố định. Sửa (bút) và Xóa (thùng rác): người lập, yêu cầu “Đang tạo”. Tạo báo giá (thẻ giá): người '
     'có Q1/Q2, yêu cầu “Chờ xây dựng giá” chưa có báo giá. Không đủ điều kiện thì ẩn.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-05.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Xem FR-04.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', '10 dòng/trang',
     '“Hiển thị a–b / tổng”; ô Số dòng/trang và các nút trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Khôi phục bộ lọc lưu trên trình duyệt nếu chưa quá 10 phút.\n'
     'After:\n– Nạp danh sách theo phạm vi quyền (Phần 2) và bộ lọc hiện tại; nạp song song cấu hình cột của người '
     'dùng.\n– Lỗi → “Lỗi tải dữ liệu”.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Đổi chiều sắp xếp tăng / giảm, quay về trang 1 và nạp lại.'),
    ('Chuyển trang / đổi Số dòng/trang', 'Click / Change',
     'After:\n– Nạp trang được chọn; đổi số dòng thì quay về trang 1.'),
    ('Bấm Mã YCBG', 'Click', 'After:\n– Mở màn Chi tiết yêu cầu (FR-06).'),
    ('Bấm mã BOM / mã báo giá', 'Click', 'After:\n– Mở màn chi tiết BOM / chi tiết báo giá tương ứng.'),
])

# ------------------------------------------------------------------ 2.2 Tìm kiếm
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.',
           anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc yêu cầu tính giá bán',
    mota='Tìm nhanh theo mã yêu cầu hoặc tên người yêu cầu; lọc nâng cao theo dự án TKT, giải pháp, trạng thái và '
         'khoảng ngày tạo.',
    tacnhan=TN_ALL,
    dieukien=DK_ALL,
    chinh='1. Người dùng gõ ô tìm nhanh rồi nhấn Enter hoặc bấm “Tìm kiếm”.\n'
          '2. Người dùng bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '3. Người dùng chọn Dự án TKT, Giải pháp, Trạng thái, Ngày tạo — mỗi lần chọn hệ thống lọc ngay.\n'
          '4. Hệ thống quay về trang 1 và hiển thị kết quả trong phạm vi quyền.',
    phu='• Chưa chọn Dự án TKT → ô Giải pháp bị khóa.\n'
        '• Đổi / xóa Dự án TKT → ô Giải pháp tự xóa giá trị.\n'
        '• Bấm “Làm mới” → xóa mọi điều kiện lọc và nạp lại đúng 1 lần.\n'
        '• Bộ lọc được nhớ trên trình duyệt 10 phút khi người dùng đi sang màn khác rồi quay lại.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', 'Tự do', 'Không', 'Trống',
     'Gợi ý “Tìm theo mã YCBG, người yêu cầu”; tìm gần đúng theo mã yêu cầu hoặc họ tên người lập.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp ô tìm nhanh, quay về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa toàn bộ điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc thu gọn',
     'Mở / đóng khối lọc nâng cao.'),
    ('Dự án TKT', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Tìm theo từ khóa trên máy chủ (tối đa 20 kết quả), hiển thị “Mã - Tên dự án”; xóa chọn được.'),
    ('Giải pháp', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Không', 'Khóa khi chưa chọn dự án',
     'Chỉ liệt kê giải pháp của dự án đã chọn (tối đa 20), hiển thị “Mã - Tên giải pháp”.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Không', 'Trống',
     'Đang tạo / Chờ xây dựng giá / Đang xây dựng giá / Đã có báo giá / Đóng / Dừng.'),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy – dd/mm/yyyy', 'Không', 'Trống',
     'Một ô khoảng ngày Từ → Đến, so theo ngày tạo yêu cầu.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Nhấn Enter ở ô tìm nhanh / bấm Tìm kiếm', 'Keypress / Click',
     'After:\n– Quay về trang 1 và nạp lại danh sách theo từ khóa cùng các điều kiện lọc đang chọn.'),
    ('Chọn giá trị ở Dự án TKT / Giải pháp / Trạng thái / Ngày tạo', 'Change',
     'After:\n– Tự lọc ngay (không cần bấm Tìm kiếm), quay về trang 1.\n'
     '– Đổi Dự án TKT → xóa giá trị Giải pháp.'),
    ('Gõ vào ô Dự án TKT / Giải pháp', 'Keypress',
     'After:\n– Tìm danh sách gợi ý trên máy chủ theo từ khóa; lỗi thì danh sách gợi ý rỗng.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xóa hết điều kiện lọc, quay về trang 1, nạp lại 1 lần.'),
])

# ------------------------------------------------------------------ 2.3 Cài đặt bộ lọc
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Cho người dùng chọn trường lọc nào hiển thị trong khối Tìm kiếm nâng cao và sắp xếp thứ tự các trường.',
    tacnhan=TN_ALL,
    dieukien=DK_ALL,
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 4 trường: Dự án TKT, Giải pháp, Trạng thái, Ngày tạo.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu” → hệ thống lưu cấu hình và báo “Cập nhật thành công”.',
    phu='• Bấm “Khôi phục mặc định” → về đủ 4 trường theo thứ tự gốc.\n'
        '• Lưu lỗi → “Thao tác thất bại”.\n'
        '• Bấm “Đóng” hoặc dấu × → đóng cửa sổ, không lưu.')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('03-cai-dat-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', '4 trường', 'Không', 'Theo cấu hình đã lưu',
     'Mỗi ô có số thứ tự, tay kéo ⠿ và ô tích.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình cho người dùng trên màn này.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đưa danh sách về mặc định.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với cấu hình đã lưu của người dùng.'),
    ('Kéo thả / tích chọn trường', 'Change', 'After:\n– Cập nhật thứ tự / trạng thái hiển thị tạm trên cửa sổ.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cấu hình theo người dùng + màn hình; khối lọc hiển thị theo cấu hình mới.\n'
     '– Thành công → “Cập nhật thành công”; lỗi → “Thao tác thất bại”.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đặt lại đủ 4 trường theo thứ tự gốc.'),
])

# ------------------------------------------------------------------ 2.4 Tùy chỉnh cột
d.h3('2.4 Tùy chỉnh cột')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Tùy chỉnh cột hiển thị',
    mota='Cho người dùng ẩn / hiện và sắp xếp lại các cột của bảng danh sách; cấu hình lưu theo từng người dùng.',
    tacnhan=TN_ALL,
    dieukien=DK_ALL,
    chinh='1. Người dùng bấm nút Cấu hình cột hiển thị (biểu tượng cột) cạnh nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê đủ 16 cột của bảng.\n'
          '3. Người dùng tích / bỏ tích, kéo biểu tượng ≡ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu” → bảng hiển thị theo cấu hình mới, báo “Cập nhật thành công”.',
    phu='• Cột STT, Mã YCBG, Hành động bị khóa (biểu tượng ổ khóa): luôn hiển thị, không bỏ tích, không kéo được.\n'
        '• Lưu lỗi → “Thao tác thất bại”.\n'
        '• Mặc định (chưa lưu cấu hình) hiển thị toàn bộ cột.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột hiển thị', shot=shot('04-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
    ('Cột khóa: STT, Mã YCBG, Hành động', 'Checkbox', 'Disable', '–', '–', 'Đã tích', 'Có biểu tượng ổ khóa.'),
    ('Các cột còn lại', 'Checkbox', 'Enable', '13 cột', 'Không', 'Theo cấu hình đã lưu',
     'BOM list, Dự án TKT, Khách hàng, Phòng làm GP, PM giải pháp, Báo giá, Deadline, Người yêu cầu, Ngày gửi, '
     'Ngày tạo, Người cập nhật, Ngày cập nhật, Trạng thái; kéo ≡ để đổi thứ tự.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình theo người dùng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ với cấu hình cột đã lưu của người dùng.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cấu hình cột theo người dùng + màn hình; bảng vẽ lại theo cấu hình.\n'
     '– Thành công → “Cập nhật thành công”; lỗi → “Thao tác thất bại”.'),
])

# ------------------------------------------------------------------ 2.5 Xuất Excel
d.h3('2.5 Xuất Excel')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Xuất Excel', 'io', actor=A_KD)
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách yêu cầu tính giá bán',
    mota='Xuất ra file Excel toàn bộ yêu cầu khớp bộ lọc đang áp dụng (không giới hạn theo trang), với các cột người '
         'dùng chọn.',
    tacnhan=TN_ALL,
    dieukien=DK_ALL,
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn các cột đang hiển thị trên bảng.\n'
          '3. Người dùng tích / bỏ tích, kéo ≡ để đổi thứ tự cột trong file.\n'
          '4. Người dùng bấm “Xuất file” → hệ thống tải về file danh_sach_yeu_cau_xay_dung_gia.xlsx và báo “Xuất '
          'Excel thành công”.',
    phu='• Không chọn trường nào → nút “Xuất file” bị khóa.\n'
        '• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n'
        '• Đang xuất → nút Xuất Excel bị khóa, tránh bấm lặp.',
    dacbiet='File có tiêu đề “Danh sách yêu cầu xây dựng giá”, cột STT tự đánh số, các cột theo đúng thứ tự người '
            'dùng sắp; dữ liệu cùng phạm vi quyền và bộ lọc với danh sách đang xem.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel => Xuất file', shot=shot('05-xuat.png'),
         shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất file', '–'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích / bỏ tích toàn bộ trường.'),
    ('Danh sách trường', 'Checkbox', 'Enable', '20 trường', 'Có (≥ 1)', 'Tích sẵn các cột đang hiện trên bảng',
     'Mã YCBG, Mã BOM list, Tên BOM list, Mã dự án TKT, Tên dự án TKT, Khách hàng, Phòng làm GP, PM giải pháp, Mã báo '
     'giá, Deadline, Nội dung yêu cầu, Thời gian giao hàng, Thời gian bảo hành, Điều khoản thanh toán, Trạng thái, '
     'Người yêu cầu, Ngày gửi, Ngày tạo, Người cập nhật, Ngày cập nhật.'),
    ('Bộ đếm', 'Label', 'Hiển thị', '–', '–', 'Theo số trường tích', '“Đang chọn a/20 trường”.'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khóa khi chưa chọn trường hoặc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiển thị.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Có ít nhất 1 trường được chọn.\n'
     'After:\n– Lấy toàn bộ yêu cầu theo phạm vi quyền + bộ lọc hiện tại, xuất các trường đã chọn theo thứ tự đã sắp.\n'
     '– Tải file danh_sach_yeu_cau_xay_dung_gia.xlsx; báo “Xuất Excel thành công”.\n'
     '– Lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.6 Xem chi tiết
d.h3('2.6 Xem chi tiết yêu cầu')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết yêu cầu tính giá bán',
    mota='Hiển thị đầy đủ thông tin một yêu cầu: BOM, dự án, khách hàng, điều kiện thương mại, file đính kèm và báo '
         'giá đã lập; kèm các nút thao tác được phép.',
    tacnhan=TN_ALL,
    dieukien='Người dùng đã đăng nhập; mở từ Mã YCBG trên danh sách hoặc từ thông báo “gửi yêu cầu xây dựng giá”.',
    chinh='1. Người dùng bấm Mã YCBG trên danh sách.\n'
          '2. Hệ thống nạp yêu cầu và hiển thị tiêu đề “Chi tiết yêu cầu XD giá: <mã> (<trạng thái>)”.\n'
          '3. Hệ thống hiển thị khối thông tin, khối File đính kèm, khối Báo giá.\n'
          '4. Hệ thống hiện các nút Sửa / Tạo báo giá / Xóa theo đúng điều kiện ở màn danh sách.',
    phu='• Không tải được → “Không tải được phiếu”, màn hiện “Không tìm thấy phiếu.”\n'
        '• Chưa có file → “Chưa có file đính kèm.”\n'
        '• Chưa có báo giá → “Chưa có báo giá được tạo.” (kèm nút Tạo báo giá nếu được phép).\n'
        '• Bấm “Quay lại” → về màn danh sách.')
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Mã YCBG', shot=shot('06-chitiet.png'),
         shot_caption='Chi tiết yêu cầu đã có báo giá')
d.figure(shot('06b-chitiet-cho.png'), 'Chi tiết yêu cầu “Chờ xây dựng giá” — người có quyền xây dựng giá thấy nút '
         'Tạo báo giá', width_in=6.2)
d.figure(shot('06c-chitiet-nhap.png'), 'Chi tiết bản nháp “Đang tạo” — người lập thấy nút Sửa, Xóa', width_in=6.2)
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề', 'Label', 'Hiển thị', '–', 'Yêu cầu xây dựng giá: <mã>', 'Kèm badge trạng thái.'),
    ('Dòng gửi', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn khi chưa gửi', '“Gửi: <ngày giờ> — <người lập>”.'),
    ('BOM list', 'Link', 'Read-only', '–', 'N/A khi không có', '“Mã — Tên BOM”; bấm mở chi tiết BOM.'),
    ('Dự án', 'Text', 'Read-only', '–', 'N/A khi không có', 'Tên dự án TKT.'),
    ('Khách hàng', 'Text', 'Read-only', '–', 'N/A khi không có', 'Khách hàng của dự án.'),
    ('Deadline', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '–'),
    ('Thời gian giao hàng / Thời gian bảo hành', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Điều kiện thanh toán', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Ghi chú yêu cầu', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khối File đính kèm (n)', 'Table/Grid', 'Read-only', '–', '“Chưa có file đính kèm.”',
     'Mỗi file là link mở tab mới, kèm dung lượng.'),
    ('Khối Báo giá', 'Label', 'Read-only', '–', '“Chưa có báo giá được tạo.”',
     'Có báo giá: mã báo giá • trạng thái báo giá (Đang tạo / Chờ TP duyệt / Chờ BGĐ duyệt / Đã duyệt), dòng “Duyệt: '
     '<ngày giờ>”, nút “Xem báo giá →”.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Hiện khi người dùng là người lập và yêu cầu “Đang tạo”.'),
    ('Nút Tạo báo giá', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Hiện khi người dùng có Q1/Q2, yêu cầu “Chờ xây dựng giá”, chưa có báo giá. Cũng hiện trong khối Báo giá.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Cùng điều kiện với nút Sửa.'),
    ('Đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải...”'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'After:\n– Nạp yêu cầu, file đính kèm, báo giá liên kết; tính các nút được hiện theo người dùng hiện tại.\n'
     '– Lỗi → “Không tải được phiếu”.'),
    ('Bấm Xem báo giá', 'Click', 'After:\n– Mở màn chi tiết báo giá.'),
    ('Bấm Sửa / Tạo báo giá / Xóa', 'Click', 'After:\n– Chuyển sang FR-08 / FR-10 / FR-09.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về màn danh sách Yêu cầu tính giá bán.'),
])

# ------------------------------------------------------------------ 2.7 Lập yêu cầu
d.h3('2.7 Lập yêu cầu tính giá bán')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Lập yêu cầu tính giá bán', 'crud', actor=A_KD)
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi '
           'tiết.', anchor='create')
d.intro_table(
    ten='Lập yêu cầu tính giá bán',
    mota='NV kinh doanh phụ trách dự án lập yêu cầu tính giá bán cho BOM tổng hợp đã duyệt của một hồ sơ trình duyệt '
         'giải pháp, rồi lưu nháp hoặc gửi ngay cho bộ phận xây dựng giá. Màn danh sách không có nút Tạo mới — '
         'yêu cầu chỉ được lập từ tab Hồ sơ của dự án TKT.',
    tacnhan='NV kinh doanh phụ trách dự án; Người dùng đã đăng nhập',
    dieukien='Người dùng là NV kinh doanh phụ trách dự án; dự án KHÔNG phải “Tự triển khai”; hồ sơ trình duyệt ở '
             'trạng thái “Đã duyệt”; giải pháp / hạng mục có BOM tổng hợp “Đã duyệt”.',
    chinh='1. Người dùng mở dự án TKT, chọn tab “Hồ sơ”.\n'
          '2. Trên dòng hồ sơ đã duyệt, người dùng bấm biểu tượng “Yêu cầu xây dựng giá”.\n'
          '3. Hệ thống tự xác định BOM tổng hợp đã duyệt theo giải pháp / hạng mục và version của hồ sơ, hiện ở đầu '
          'cửa sổ.\n'
          '4. Người dùng nhập Deadline, Thời gian giao hàng, Thời gian bảo hành, Điều kiện thanh toán, Ghi chú yêu cầu, '
          'đính kèm file (nếu có).\n'
          '5. Người dùng bấm “Lưu nháp” (yêu cầu ở “Đang tạo”) hoặc “Lưu và gửi” (yêu cầu chuyển “Chờ xây dựng giá”).\n'
          '6. Hệ thống sinh mã YCBG-YYYY-NNNNN, báo “Đã lưu nháp” / “Đã gửi yêu cầu xây dựng giá”, đóng cửa sổ và '
          'nạp lại tab Hồ sơ.',
    phu='• Không có BOM tổng hợp đã duyệt → cửa sổ báo “Chưa có BOM tổng hợp ở trạng thái \"Đã duyệt\" cho giải pháp '
        '(hoặc hạng mục) này. Vui lòng đợi hồ sơ trình duyệt được duyệt để BOM tổng hợp chuyển sang \"Đã duyệt\" '
        'trước khi yêu cầu xây dựng giá.” và ẩn nút lưu.\n'
        '• Người dùng không phải NV kinh doanh phụ trách dự án → “Chỉ NV Kinh doanh phụ trách dự án mới có thể yêu cầu '
        'xây dựng giá.”\n'
        '• Thiếu trường bắt buộc → báo lỗi đỏ ngay dưới từng ô, không gửi lên hệ thống.\n'
        '• File > 20MB → “File <tên file> vượt 20MB”, bỏ qua file đó.',
    dacbiet='Tab Hồ sơ có cột “Yêu cầu XD Giá” cho mở rộng dòng hồ sơ để xem các yêu cầu đã lập (Mã YCBG, Người gửi, '
            'Ngày gửi, Deadline, Trạng thái, Báo giá, Ngày duyệt báo giá) với các nút Xem yêu cầu, Sửa nháp, Xoá — '
            'cùng quy tắc với FR-06, FR-08, FR-09. Dự án “Tự triển khai” không lập yêu cầu mà có nút Tạo báo giá '
            'trực tiếp từ BOM.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU_TAO, shot=shot('11-tao.png'),
         shot_caption='Cửa sổ Yêu cầu xây dựng giá mở từ tab Hồ sơ của dự án TKT')
d.figure(shot('11a-hoso.png'), 'Tab Hồ sơ của dự án TKT — biểu tượng Yêu cầu xây dựng giá trên dòng hồ sơ đã duyệt',
         width_in=6.2)
d.figure(shot('11b-tao-loi.png'), 'Bấm Lưu và gửi khi để trống các trường bắt buộc', width_in=6.2)
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Yêu cầu xây dựng giá', '–'),
    ('BOM list', 'Link', 'Read-only', '–', '–', 'Tự xác định',
     '“Mã — Tên BOM tổng hợp”; bấm mở BOM ở tab mới.'),
    ('Deadline', 'Datepicker', 'Enable', 'dd/mm/yyyy, từ hôm nay trở đi', 'Không', 'Trống',
     'Gợi ý “Chọn ngày...”; không chọn được ngày quá khứ.'),
    ('Thời gian giao hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', 'Gợi ý “VD: 30 ngày sau ký HĐ”.'),
    ('Thời gian bảo hành', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', 'Gợi ý “VD: 12 tháng”.'),
    ('Điều kiện thanh toán', 'Textarea', 'Enable', 'Tự do', 'Có', 'Trống', 'Gợi ý “VD: 50% đặt cọc, 50% bàn giao”.'),
    ('Ghi chú yêu cầu', 'Textarea', 'Enable', 'Tự do', 'Có', 'Trống',
     'Gợi ý “Ghi chú các yêu cầu về mức giá vượt trội để CV làm giá cân đối”.'),
    ('File đính kèm', 'Button', 'Enable', '.pdf .png .jpg .jpeg .docx .doc .xls .xlsx; ≤ 20MB/file', 'Không',
     'Trống', 'Nút “Chọn file” (chọn nhiều); file đã tải hiện thành thẻ có nút Xoá; chưa có file hiện “Tối đa 20MB mỗi '
     'file”.'),
    ('Lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Vui lòng nhập thời gian giao hàng” / “Vui lòng nhập thời gian bảo hành” / “Vui lòng nhập điều kiện thanh toán” '
     '/ “Vui lòng nhập ghi chú”.'),
    ('Nút Lưu và gửi', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Hiện “Đang lưu...” khi xử lý.'),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Yêu cầu xây dựng giá', 'Click',
     'Before:\n– Biểu tượng chỉ hiện khi người dùng là NV kinh doanh phụ trách dự án, dự án không “Tự triển khai”, hồ sơ '
     '“Đã duyệt”.\n'
     'After:\n– Nạp BOM tổng hợp đã duyệt: ưu tiên BOM đúng version, nếu không có lấy BOM chưa gắn version, mới cập '
     'nhật nhất.\n– Không có BOM / không phải NV kinh doanh phụ trách → hiện thông báo ở Dòng sự kiện phụ, ẩn nút lưu.'),
    ('Chọn file', 'Change',
     'During:\n– File > 20MB → “File <tên file> vượt 20MB”, bỏ qua file đó.\n'
     'After:\n– Tải file lên kho lưu trữ, thêm thẻ file; lỗi → “Upload file thất bại”.'),
    ('Bấm Lưu nháp / Lưu và gửi', 'Click',
     'Before:\n– Kiểm tra người dùng là NV kinh doanh phụ trách dự án; nếu không → “Chỉ NV Kinh doanh phụ trách dự án '
     'mới có thể yêu cầu xây dựng giá.” và dừng xử lý.\n'
     'During:\n– Thời gian giao hàng / Thời gian bảo hành / Điều kiện thanh toán / Ghi chú yêu cầu trống → lỗi dưới ô '
     'tương ứng.\n– BOM không thuộc version giải pháp của hồ sơ → “BOM đã chọn không thuộc version giải pháp được yêu '
     'cầu.”\n– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Tạo yêu cầu “Đang tạo”, sinh mã YCBG-YYYY-NNNNN, lưu file đính kèm.\n'
     '– Lưu nháp → “Đã lưu nháp”.\n'
     '– Lưu và gửi → chuyển “Chờ xây dựng giá”, ghi ngày gửi, áp các hiệu ứng ở BR-04 và báo “Đã gửi yêu cầu xây dựng '
     'giá”.\n– Đóng cửa sổ, nạp lại tab Hồ sơ. Lỗi khác → hiển thị nội dung lỗi hoặc “Lỗi lưu yêu cầu”.'),
])

# ------------------------------------------------------------------ 2.8 Sửa và gửi
d.h3('2.8 Sửa và gửi yêu cầu')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Sửa và gửi yêu cầu', 'crud', actor=A_KD)
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi '
           'tiết.', anchor='create')
d.intro_table(
    ten='Sửa và gửi yêu cầu tính giá bán',
    mota='Người lập sửa bản nháp yêu cầu (điều kiện thương mại, ghi chú, file đính kèm) rồi lưu nháp tiếp hoặc gửi cho '
         'bộ phận xây dựng giá. BOM list không đổi được.',
    tacnhan='NV kinh doanh phụ trách dự án (người lập yêu cầu); Người dùng đã đăng nhập',
    dieukien='Người dùng là người lập yêu cầu và yêu cầu đang ở trạng thái “Đang tạo”.',
    chinh='1. Người dùng bấm biểu tượng Sửa trên dòng (hoặc nút Sửa ở màn chi tiết).\n'
          '2. Hệ thống mở màn “Sửa yêu cầu XD giá: <mã>” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa các trường, thêm / bỏ file đính kèm.\n'
          '4a. Bấm “Lưu nháp” → hệ thống lưu, báo “Đã lưu nháp”, ở lại màn Sửa.\n'
          '4b. Bấm “Lưu và gửi” → hệ thống lưu rồi gửi, báo “Đã gửi yêu cầu”, chuyển sang màn chi tiết.',
    phu='• Thiếu một trong các trường bắt buộc → “Vui lòng điền đủ các trường bắt buộc”, không lưu.\n'
        '• Yêu cầu không còn sửa được → form khóa, hiện dòng cảnh báo “Yêu cầu đã gửi, không thể sửa.” và ẩn nút lưu.\n'
        '• File > 20MB → “File <tên file> vượt 20MB”; tải file lỗi → “Upload file thất bại”.\n'
        '• Bấm “Quay lại” → về màn chi tiết yêu cầu.',
    dacbiet='Cũng sửa được bản nháp ngay trên tab Hồ sơ của dự án TKT (nút “Sửa nháp” mở cửa sổ giống FR-07, tiêu đề '
            '“Sửa yêu cầu xây dựng giá”, thành công báo “Đã cập nhật”).')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('08-sua.png'), shot_caption='Màn Sửa yêu cầu (người lập, bản nháp)')
d.figure(shot('07b-ds-nv-phai.png'), 'Danh sách của người lập — nút Sửa, Xóa chỉ hiện trên bản nháp “Đang tạo”',
         width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề', 'Label', 'Hiển thị', '–', '–', 'Sửa yêu cầu XD giá: <mã>', 'Kèm badge trạng thái.'),
    ('Cảnh báo khóa', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Yêu cầu đã gửi, không thể sửa.” khi người dùng không còn được sửa.'),
    ('BOM list', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Mã - Tên BOM”, không sửa được.'),
    ('Deadline', 'Datepicker', 'Enable / Disable', 'dd/mm/yyyy', 'Không', 'Theo dữ liệu', '–'),
    ('Thời gian giao hàng', 'Textbox', 'Enable / Disable', '0–255 ký tự', 'Có', 'Theo dữ liệu', '–'),
    ('Thời gian bảo hành', 'Textbox', 'Enable / Disable', '0–255 ký tự', 'Có', 'Theo dữ liệu', '–'),
    ('Điều kiện thanh toán', 'Textarea', 'Enable / Disable', 'Tự do', 'Có', 'Theo dữ liệu', '–'),
    ('Ghi chú yêu cầu', 'Textarea', 'Enable / Disable', 'Tự do', 'Có', 'Theo dữ liệu', '–'),
    ('File đính kèm', 'Button', 'Enable / Ẩn', '≤ 20MB/file', 'Không', 'Theo dữ liệu',
     'Chọn nhiều file; danh sách file có biểu tượng xóa từng file.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn chi tiết.'),
    ('Nút Lưu nháp', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị khi sửa được', '–'),
    ('Nút Lưu và gửi', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị khi sửa được', 'Hiện “Đang lưu...” khi xử lý.'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Kiểm tra người dùng là người lập và yêu cầu “Đang tạo”.\n' + NO_OWNER + '\n'
     'During:\n– Thiếu trường bắt buộc → “Vui lòng điền đủ các trường bắt buộc”.\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Cập nhật yêu cầu và đồng bộ lại danh sách file đính kèm.\n– Hiển thị “Đã lưu nháp”.\n'
     '– Lỗi khác → nội dung lỗi hoặc “Lỗi lưu”.'),
    ('Bấm Lưu và gửi', 'Click',
     'Before:\n– Như Lưu nháp.\n'
     'During:\n– Như Lưu nháp.\n'
     'After:\n– Lưu yêu cầu, chuyển “Chờ xây dựng giá”, ghi ngày gửi, áp hiệu ứng BR-04.\n'
     '– Hiển thị “Đã gửi yêu cầu”, chuyển sang màn chi tiết.'),
    ('Chọn / xóa file', 'Change / Click',
     'During:\n– File > 20MB → “File <tên file> vượt 20MB”.\n'
     'After:\n– Thêm / bỏ file khỏi danh sách; chỉ ghi nhận khi bấm Lưu.'),
])

# ------------------------------------------------------------------ 2.9 Xóa
d.h3('2.9 Xóa yêu cầu')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Xóa yêu cầu', 'action', actor=A_KD)
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo, Quy tắc Xóa. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', anchor='delete')
d.intro_table(
    ten='Xóa yêu cầu tính giá bán',
    mota='Người lập xóa hẳn bản nháp yêu cầu chưa gửi, kèm toàn bộ file đính kèm.',
    tacnhan='NV kinh doanh phụ trách dự án (người lập yêu cầu); Người dùng đã đăng nhập',
    dieukien='Người dùng là người lập yêu cầu và yêu cầu đang ở trạng thái “Đang tạo”.',
    chinh='1. Người dùng bấm biểu tượng Xóa trên dòng (hoặc nút Xóa ở màn chi tiết).\n'
          '2. Hệ thống hỏi “Bạn có chắc muốn xóa yêu cầu xây dựng giá \'<mã>\'?”.\n'
          '3. Người dùng bấm “Xóa”.\n'
          '4. Hệ thống xóa yêu cầu, báo “Xóa yêu cầu thành công” và nạp lại danh sách (xóa từ màn chi tiết thì quay '
          'về danh sách).',
    phu='• Bấm “Hủy” → đóng hộp thoại, không xóa.\n'
        '• Yêu cầu đã gửi / đã đóng / đã dừng hoặc không phải người lập → báo lỗi ở BR-06; lỗi khác → “Không thể xóa '
        'yêu cầu”.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('09-xoa.png'), shot_caption='Hộp thoại Xác nhận xóa')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Hiển thị', '“Bạn có chắc muốn xóa yêu cầu xây dựng giá \'<mã>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ; thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa trên hộp thoại', 'Click',
     'Before:\n– Kiểm tra người dùng là người lập và yêu cầu “Đang tạo”.\n' + NO_OWNER + '\n'
     'After:\n– Xóa file đính kèm và xóa hẳn yêu cầu.\n– Hiển thị “Xóa yêu cầu thành công”; nạp lại danh sách / về màn '
     'danh sách.\n– Lỗi → nội dung lỗi hoặc “Không thể xóa yêu cầu”.'),
    ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ------------------------------------------------------------------ 2.10 Tạo báo giá
d.h3('2.10 Tạo báo giá từ yêu cầu')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Tạo báo giá từ yêu cầu', 'action', actor=A_GIA)
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', anchor='notice')
d.intro_table(
    ten='Tạo báo giá từ yêu cầu tính giá bán',
    mota='Người xây dựng giá tiếp nhận yêu cầu bằng cách tạo báo giá từ BOM của yêu cầu; người bấm trở thành người làm '
         'giá của báo giá đó.',
    tacnhan='Người xây dựng giá; Người dùng đã đăng nhập',
    dieukien='Người dùng có Q1 hoặc Q2; yêu cầu ở trạng thái “Chờ xây dựng giá” và chưa có báo giá.',
    chinh='1. Người dùng bấm biểu tượng Tạo báo giá trên dòng (hoặc nút Tạo báo giá ở màn chi tiết).\n'
          '2. Hệ thống hỏi “Bạn sẽ trở thành người làm giá cho yêu cầu này. Xác nhận?”.\n'
          '3. Người dùng bấm “Xác nhận”.\n'
          '4. Hệ thống tạo báo giá “Đang tạo” gắn với yêu cầu (lấy BOM, dự án, khách hàng, điều kiện thương mại), báo '
          '“Đã tạo báo giá” và mở màn Sửa báo giá.',
    phu='• Bấm “Huỷ” → đóng hộp thoại.\n'
        '• Dự án “Triển khai theo Phòng” mà người dùng không có Q2 → “Bạn không có quyền xây dựng giá bán theo phòng.”\n'
        '• Yêu cầu không thuộc phòng ban của người dùng → “Yêu cầu xây dựng giá này không thuộc phòng ban của bạn.”\n'
        '• Dự án khác mà người dùng không có Q1 → “Bạn không có quyền xây dựng giá bán theo công ty.”\n'
        '• Thiếu thông tin bắt buộc của báo giá hoặc lỗi khác → hiển thị nội dung lỗi (hoặc “Không thể tạo báo giá”), '
        'nạp lại danh sách.',
    dacbiet='Sau khi tạo, yêu cầu hiện mã báo giá ở cột Báo giá và nút Tạo báo giá ẩn đi. Yêu cầu chuyển “Đã có báo '
            'giá” khi báo giá được duyệt; báo giá bị xóa thì yêu cầu trở lại “Chờ xây dựng giá”.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo báo giá', shot=shot('10-taobaogia-xacnhan.png'),
         shot_caption='Hộp thoại xác nhận Tạo báo giá')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng Tạo báo giá', 'Icon Button', 'Enable / Ẩn', 'Ẩn',
     'Trên dòng danh sách và màn chi tiết; chỉ hiện khi đủ điều kiện ban đầu.'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Tạo báo giá', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Hiển thị', '“Bạn sẽ trở thành người làm giá cho yêu cầu này. Xác nhận?”'),
    ('Nút Xác nhận', 'Button', 'Enable', 'Hiển thị', 'Tạo báo giá.'),
    ('Nút Huỷ', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xác nhận', 'Click',
     'Before:\n– Kiểm tra quyền theo kiểu triển khai dự án (BR-07).\n'
     '– Nếu không có quyền → hiển thị thông báo tương ứng ở Dòng sự kiện phụ và dừng xử lý.\n'
     'After:\n– Tạo báo giá “Đang tạo” gắn với yêu cầu: sao chép dòng hàng của BOM (giá ban đầu 0), BOM, dự án, '
     'khách hàng và Deadline / Thời gian giao hàng / Thời gian bảo hành / Điều kiện thanh toán / Ghi chú.\n'
     '– Dự án chưa tới giai đoạn “Dự toán” thì chuyển sang “Dự toán”.\n'
     '– Hiển thị “Đã tạo báo giá”, mở màn Sửa báo giá.'),
    ('Bấm Huỷ', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ==================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu tính giá bán; không lặp lại các quy tắc đã có '
           'trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Yêu cầu sinh ra từ hồ sơ trình duyệt đã duyệt', [
        '– Chỉ lập từ tab Hồ sơ của dự án TKT, trên hồ sơ trình duyệt giải pháp “Đã duyệt”.',
        '– Chỉ NV kinh doanh phụ trách dự án được lập; dự án “Tự triển khai” không lập yêu cầu (tạo báo giá trực tiếp '
        'từ BOM).',
        '– BOM của yêu cầu là BOM tổng hợp “Đã duyệt” của đúng giải pháp (hoặc hạng mục) — ưu tiên BOM đúng version, '
        'không có thì lấy BOM chưa gắn version mới cập nhật nhất. Một BOM có thể có nhiều yêu cầu.',
    ], 'Lập yêu cầu tính giá bán'),
    ('BR-02', 'Mã yêu cầu tự sinh', [
        '– Dạng YCBG-YYYY-NNNNN (YYYY = năm tạo, NNNNN tăng dần), sinh khi lưu lần đầu, không sửa được.',
    ], 'Lập yêu cầu tính giá bán'),
    ('BR-03', 'Luồng trạng thái', [
        '– Đang tạo (lưu nháp) → Chờ xây dựng giá (người lập gửi).',
        '– Chờ xây dựng giá → Đã có báo giá khi báo giá lập từ yêu cầu được duyệt (tự duyệt, Trưởng phòng hoặc Ban '
        'giám đốc duyệt).',
        '– Đang tạo / Chờ xây dựng giá / Đang xây dựng giá → Đóng khi dự án TKT bị đóng.',
        '– Chờ xây dựng giá / Đang xây dựng giá → Dừng khi yêu cầu điều chỉnh giải pháp của dự án được duyệt; không mở '
        'lại được.',
        '– Báo giá gắn yêu cầu bị xóa (và không còn báo giá nào khác) → yêu cầu trở lại Chờ xây dựng giá.',
        '– “Đang xây dựng giá” có trong danh mục trạng thái; thao tác Tạo báo giá hiện hành giữ yêu cầu ở “Chờ xây dựng '
        'giá” cho tới khi báo giá được duyệt.',
    ], ['Xem danh sách', 'Sửa và gửi', 'Tạo báo giá']),
    ('BR-04', 'Hiệu ứng khi gửi yêu cầu', [
        '– Ghi ngày gửi; dự án TKT chuyển “Dự toán” nếu chưa tới giai đoạn này (không lùi); giải pháp chuyển “Chờ làm '
        'giá”.',
        '– Gửi thông báo “<Người gửi> gửi yêu cầu xây dựng giá <mã> cho dự án <tên dự án>”, bấm mở chi tiết yêu cầu: '
        'dự án “Triển khai theo Phòng” → người có Q2 cùng phòng ban với người lập; dự án khác → người có Q1.',
    ], ['Lập yêu cầu', 'Sửa và gửi']),
    ('BR-05', 'Phạm vi dữ liệu danh sách và file Excel', [
        '– Theo bảng V1 / V2 / Không có quyền nào ở Phần 2; có cả V1 và V2 thì cộng phạm vi.',
        '– Người có V1 / V2 chỉ thấy yêu cầu đã gửi, không thấy bản nháp (kể cả của chính mình).',
        '– File Excel dùng đúng phạm vi và bộ lọc của danh sách, lấy tất cả dòng.',
    ], ['Xem danh sách', 'Xuất Excel']),
    ('BR-06', 'Chỉ người lập sửa / gửi / xóa bản nháp', [
        '– Chỉ người lập, chỉ khi “Đang tạo”. Vi phạm thì báo: “Yêu cầu XD giá đã đóng theo dự án, không thể sửa/xoá.” · '
        '“Yêu cầu XD giá đã dừng do điều chỉnh giải pháp, không thể sửa/xoá.” · “Yêu cầu XD giá đã gửi, không thể '
        'sửa/xoá.” · “Chỉ người tạo mới có thể sửa/xoá yêu cầu này.”',
        '– Nút Sửa / Xóa ẩn ở cả danh sách lẫn chi tiết khi không đủ điều kiện.',
    ], ['Sửa và gửi', 'Xóa']),
    ('BR-07', 'Quyền tạo báo giá theo kiểu triển khai dự án', [
        '– Dự án “Triển khai theo Phòng”: cần Q2 và yêu cầu thuộc cùng phòng ban với người dùng (phòng ban của người '
        'lập yêu cầu).',
        '– Dự án “Liên phòng ban” hoặc chưa xác định: cần Q1.',
        '– Mỗi yêu cầu chỉ tạo 1 báo giá từ màn này; nút ẩn khi yêu cầu đã có báo giá hoặc không ở “Chờ xây dựng giá”.',
    ], 'Tạo báo giá từ yêu cầu'),
    ('BR-08', 'File đính kèm', [
        '– Định dạng .pdf .png .jpg .jpeg .docx .doc .xls .xlsx, tối đa 20MB mỗi file; chọn được nhiều file.',
        '– Xóa yêu cầu thì xóa luôn file đính kèm.',
    ], ['Lập yêu cầu', 'Sửa và gửi', 'Xóa']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')
