# -*- coding: utf-8 -*-
"""Sinh SRS màn hình Báo giá theo khuôn SRS 2026-09-24."""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ASSET_DIR = '/Users/manhcuong/Desktop/dns/HRM/.claude/skills/srs-documenter/assets'
sys.path.insert(0, ASSET_DIR)
from srs_docx_lib import SrsDoc, ACTOR_P1, ACTOR_P2, ACTOR_BOTH

BASE = '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/quotation-no-project'
SHOTS = os.path.join(BASE, 'quotation_shots')
OUT = os.path.join(BASE, 'SRS - Báo giá.docx')

def shot(name):
    return os.path.join(SHOTS, name)

LIST_SHOT = shot('01-danh-sach.png')
CREATE_SHOT = shot('02-tao-moi.png')
DETAIL_SHOT = shot('03-chi-tiet-loading.png')
MENU = 'Phân hệ CSKH TRƯỚC BÁN => Báo giá'

# Ảnh menu được lấy từ ảnh chụp thật của màn đang chạy; layout() thu nhỏ về icon 0,3 inch.
ICONS = {
    'Phân hệ CSKH TRƯỚC BÁN': LIST_SHOT,
    'Báo giá': LIST_SHOT,
    'Tạo mới': CREATE_SHOT,
    'Chỉnh sửa': CREATE_SHOT,
    'Sao chép': LIST_SHOT,
    'Xóa': LIST_SHOT,
    'Import Excel': CREATE_SHOT,
    'Duyệt': DETAIL_SHOT,
    'Từ chối': DETAIL_SHOT,
    'Xem chi tiết': LIST_SHOT,
    'In': DETAIL_SHOT,
    'Xuất Excel': LIST_SHOT,
    'Lịch sử': LIST_SHOT,
}

d = SrsDoc(
    out=OUT,
    menu=MENU,
    route='/assign/quotations',
    full_url='http://127.0.0.1:3002/assign/quotations',
    img_dir=os.path.join(BASE, '_uml'),
    img_prefix='quotation_')
d.set_menu_icons(ICONS)
d.title_block('Báo giá')
d.h2('Mục lục')
d.toc()

d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả màn hình Báo giá thuộc phân hệ CSKH trước bán, là căn cứ nghiệm thu chức năng, phân quyền và các phép tính giá.')
d.bullets([
    'Quản lý báo giá tự nhập, báo giá tạo từ BOM và báo giá không gắn Dự án TKT.',
    'Làm rõ cách hình thành giá vốn, giá bán, tỷ suất lợi nhuận, VAT, giảm giá, chi phí vận chuyển và tổng giá trị báo giá.',
    'Đặc tả đầy đủ các luồng tạo mới, chỉnh sửa, sao chép, xóa, import/export Excel, duyệt, từ chối, in và xem lịch sử.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Báo giá tự nhập', 'Báo giá do người dùng tự tạo nhóm, hàng hóa, dịch vụ và chi phí; không lấy toàn bộ dòng từ BOM.'),
    ('Báo giá từ BOM', 'Báo giá kế thừa các dòng hàng từ BOM tổng hợp đã duyệt.'),
    ('Hàng tạm', 'Hàng hóa chưa có mã hàng ERP, được nhập trực tiếp trong báo giá.'),
    ('Giá nhập / giá vốn', 'Chi phí đầu vào của một dòng hàng hoặc dịch vụ.'),
    ('Tỷ suất lợi nhuận (TSLN)', 'Tỷ lệ lợi nhuận so với giá vốn, hiển thị theo phần trăm.'),
    ('GG', 'Giảm giá; có thể giảm theo mặt hàng hoặc giảm theo tổng báo giá.'),
    ('Cấp duyệt', 'Tự duyệt, Trưởng phòng (TP) duyệt hoặc TP và Ban giám đốc (BGĐ) duyệt theo mức giá trị/cấu hình.'),
    ('Báo giá không gắn Dự án TKT', 'Báo giá có project_id rỗng; khách hàng được chọn trực tiếp và tiền tệ mặc định là VNĐ.'),
])

d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền / điều kiện', 'Tác dụng trên màn hình'], [
    ('Q1', 'Xem tất cả danh sách Báo giá', 'Xem toàn bộ báo giá trong danh sách và mở chi tiết.'),
    ('Q2', 'Xem danh sách Báo giá theo công ty', 'Xem báo giá thuộc công ty của người dùng.'),
    ('Q3', 'Xem danh sách Báo giá theo phòng ban', 'Xem báo giá thuộc phòng ban của người dùng.'),
    ('Q4', 'Xem danh sách Báo giá theo bộ phận', 'Xem báo giá thuộc bộ phận của người dùng.'),
    ('Q5', 'Trưởng phòng duyệt giá Bom giải pháp', 'Duyệt/từ chối báo giá ở cấp TP; xem hàng chờ TP theo phòng ban quản lý.'),
    ('Q6', 'Ban giám đốc duyệt giá Bom giải pháp', 'Duyệt/từ chối báo giá ở cấp BGĐ; xem hàng chờ BGĐ theo công ty.'),
    ('Q7', 'Xây dựng giá bán theo phòng / theo công ty', 'Được dùng khi lập báo giá từ YCBG theo loại triển khai.'),
    ('Q8', 'Cho phép thêm giảm giá trong báo giá', 'Cho phép thay đổi phương thức, dòng giảm giá và giảm giá tổng.'),
    ('Q9', 'Xem giá vốn hàng hoá', 'Hiển thị giá nhập, thành tiền nhập và TSLN của hàng ERP.'),
    ('Q10', 'Điều kiện nghiệp vụ', 'Người lập/Sale phụ trách dự án hoặc người có quyền xây dựng giá được tạo, sửa, sao chép; người lập được xóa bản nháp.'),
], widths=[0.7, 2.25, 3.05])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Q1', 'Toàn bộ báo giá.'),
    ('V2', 'Q2', 'Báo giá trong công ty của người dùng.'),
    ('V3', 'Q3', 'Báo giá trong phòng ban của người dùng.'),
    ('V4', 'Q4', 'Báo giá trong bộ phận của người dùng.'),
    ('—', 'Không có V1–V4', 'Chỉ báo giá do chính người dùng tạo; ngoại lệ là báo giá đang ở hàng chờ duyệt của chính người đó.'),
], widths=[0.7, 2.25, 3.05])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1–Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách, lọc, sắp xếp', '✅ theo V', '❌', '❌', '❌', '❌', '❌', '✅ bản ghi do mình tạo'),
    ('FR-02 Tạo mới / lưu nháp', '❌', '❌', '❌', '✅ khi lập từ YCBG', '✅ phần giảm giá', '❌', '✅ nếu là Sale phụ trách/người được giao'),
    ('FR-03 Chỉnh sửa', '❌', '❌', '❌', '✅ theo nguồn YCBG', '✅ nếu thay đổi GG', '❌', '✅ người lập và trạng thái Đang tạo'),
    ('FR-04 Xóa', '❌', '❌', '❌', '❌', '❌', '❌', '✅ người lập + Đang tạo'),
    ('FR-05 Import / Xuất / In / Chi tiết / Lịch sử', '✅ theo phạm vi', '✅ hàng chờ TP', '✅ hàng chờ BGĐ', '❌', '❌', 'giá vốn theo Q9', 'Không có nếu ngoài phạm vi'),
    ('FR-06 Duyệt / Từ chối', '❌', '✅ cấp TP', '✅ cấp BGĐ', '❌', '❌', '❌', '❌'),
], widths=[1.8, 0.7, 0.45, 0.45, 0.45, 0.45, 0.45, 1.25])

d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
mains = [
    ('FR-01', 'Xem danh sách', 'view'), ('FR-02', 'Tạo mới', 'crud'), ('FR-03', 'Chỉnh sửa', 'crud'),
    ('FR-04', 'Sao chép', 'crud'), ('FR-05', 'Xóa', 'action'), ('FR-06', 'Import Excel', 'io'),
    ('FR-07', 'Duyệt / Từ chối', 'action'), ('FR-08', 'In', 'io'), ('FR-09', 'Xuất Excel', 'io'),
]
subs = [
    ('FR-10', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
    ('FR-11', 'Xem chi tiết', 'view', 'extend', [0], None),
    ('FR-12', 'Xem lịch sử', 'view', 'extend', [0], None),
]
d.overview_figure2([('Người dùng nghiệp vụ', list(range(len(mains)))), ('TP/BGĐ', [6])], mains, subs, 'Sơ đồ Use Case tổng quan màn Báo giá')
d.h2('2 Đặc tả chi tiết từng chức năng')

# Các chức năng được viết theo cùng khuôn, nhưng nội dung điều kiện/event riêng cho từng luồng.
FUNCTIONS = [
    ('2.1', 'Xem danh sách báo giá', 'FR-01', 'view', 'read', 'Xem danh sách báo giá', 'Hiển thị danh sách theo phạm vi quyền V1–V4 hoặc bản ghi do người dùng tạo.', 'Người dùng đã đăng nhập; có ít nhất một quyền Q1–Q4 hoặc có báo giá do mình tạo.', '1. Mở menu CSKH TRƯỚC BÁN → Báo giá.\n2. Hệ thống áp phạm vi dữ liệu.\n3. Nạp danh sách, phân trang và các cột đã cấu hình.', '• Không có quyền/phạm vi phù hợp → danh sách rỗng, không lộ dữ liệu.\n• Báo giá đang chờ chính người dùng duyệt vẫn có thể mở từ hàng chờ tương ứng.', 'list', LIST_SHOT),
    ('2.2', 'Tìm kiếm và lọc báo giá', 'FR-10', 'view', 'read', 'Tìm kiếm và lọc', 'Lọc nhanh theo mã báo giá, tên khách hàng và bộ lọc nâng cao.', 'Đang ở màn danh sách; danh sách đã được giới hạn theo phạm vi quyền.', '1. Nhập từ khóa hoặc mở Tìm kiếm nâng cao.\n2. Chọn bộ lọc.\n3. Bấm Tìm kiếm; hệ thống giữ điều kiện khi phân trang.', '• Không có kết quả → thông báo “Không có dữ liệu phù hợp bộ lọc.”\n• Xóa bộ lọc → tải lại danh sách mặc định.', 'search', LIST_SHOT),
    ('2.3', 'Tạo mới báo giá', 'FR-02', 'crud', 'write', 'Tạo mới báo giá', 'Tạo báo giá từ BOM hoặc tự nhập; hỗ trợ báo giá không gắn Dự án TKT.', 'Có quyền vào màn tạo. Nếu có Dự án TKT thì người dùng là Sale phụ trách hoặc có quyền xây dựng giá tương ứng; nếu không có dự án phải chọn Khách hàng. Báo giá mới ở trạng thái Đang tạo.', '1. Bấm Tạo báo giá.\n2. Chọn Dự án TKT/BOM hoặc bỏ trống dự án.\n3. Nhập thông tin chung, bảng chi tiết, tổng hợp, VAT/giảm giá, điều khoản và ghi chú.\n4. Chọn Lưu nháp hoặc Gửi duyệt.', '• Không gắn dự án → ẩn Giai đoạn dự án, không có BOM; Khách hàng bắt buộc; tiền tệ mặc định VNĐ.\n• Bản nháp thiếu trường nghiệp vụ → vẫn lưu nếu qua validate phạm vi; gửi duyệt phải đủ dữ liệu.\n• Dự án con kế thừa tiền tệ, bảng giá, phương thức giảm giá từ dự án cha.\n• Thay đổi giá bán ERP trong lúc nhập → hiển thị cảnh báo/cho người dùng chọn giữ giá đã lưu hoặc cập nhật giá hiện hành.', 'create', CREATE_SHOT),
    ('2.4', 'Chỉnh sửa báo giá', 'FR-03', 'crud', 'write', 'Chỉnh sửa báo giá', 'Cập nhật báo giá khi bản ghi còn cho phép chỉnh sửa.', 'Người lập báo giá; trạng thái Đang tạo. Báo giá Đã duyệt/Chờ duyệt/Trúng thầu/Đóng/Dừng không cho sửa.', '1. Mở chi tiết và bấm Sửa.\n2. Thay đổi header hoặc dòng chi tiết.\n3. Hệ thống tính lại các giá trị phụ thuộc.\n4. Bấm Lưu nháp hoặc Gửi duyệt.', '• Giá bán/giá vốn ERP thay đổi → hiển thị danh sách thay đổi; chọn cập nhật thì dùng giá hiện hành, chọn từ chối thì giữ giá đã lưu.\n• Hàng ERP lấy VAT từ danh mục ERP; dịch vụ có cost_id lấy VAT từ danh mục chi phí.\n• Lưu thành công quay về danh sách và ghi lịch sử thay đổi.', 'create', CREATE_SHOT),
    ('2.5', 'Sao chép báo giá', 'FR-04', 'crud', 'write', 'Sao chép báo giá', 'Mở bản nháp mới với dữ liệu được lấy từ báo giá nguồn.', 'Báo giá nguồn nằm trong phạm vi xem; người dùng là Sale phụ trách dự án, có quyền xây dựng giá theo nguồn YCBG, hoặc là người lập nếu báo giá không gắn dự án.', '1. Bấm Sao chép.\n2. Xem trước các thay đổi giá bán/giá vốn/VAT.\n3. Hệ thống mở form tạo mới với dữ liệu sao chép.\n4. Người dùng điều chỉnh và bấm Lưu.', '• Bản sao chưa ghi DB cho đến khi bấm Lưu.\n• Giá bán/giá vốn ERP đã thay đổi → cho chọn giá hiện hành hoặc giữ giá nguồn; tỷ giá lấy lại theo hiện hành.\n• Bản sao bắt đầu ở Đang tạo; mã báo giá mới sinh khi lưu.', 'create', CREATE_SHOT),
    ('2.6', 'Xóa báo giá', 'FR-05', 'action', 'confirm', 'Xóa báo giá', 'Xóa báo giá bản nháp khỏi hệ thống.', 'Người dùng là người lập và báo giá ở trạng thái Đang tạo; không được xóa báo giá đã gửi duyệt hoặc đã duyệt.', '1. Bấm Xóa tại danh sách/chi tiết.\n2. Hệ thống mở hộp xác nhận.\n3. Chọn Xóa để xóa bản ghi và dữ liệu dòng liên quan.', '• Chọn Hủy → giữ nguyên dữ liệu.\n• Xóa báo giá gắn YCBG cuối cùng → YCBG quay về trạng thái Chờ xây dựng giá.\n• Không đủ điều kiện → từ chối và không xóa.', 'delete', LIST_SHOT),
    ('2.7', 'Import báo giá từ Excel', 'FR-06', 'io', 'write', 'Import báo giá từ Excel', 'Nạp dữ liệu bảng chi tiết từ file Excel theo file mẫu báo giá.', 'Có báo giá hiện hữu trong phạm vi; báo giá ở trạng thái Đang tạo; file đúng mẫu và người dùng có quyền sửa báo giá.', '1. Tải file mẫu hoặc xuất dữ liệu báo giá.\n2. Chọn file Excel.\n3. Hệ thống validate cấu trúc, mã dòng, hàng hóa, đơn vị, giá, VAT, giảm giá.\n4. Hiển thị preview lỗi/thay đổi.\n5. Xác nhận import rồi Lưu.', '• File sai cấu trúc hoặc dòng lỗi → không ghi dữ liệu lỗi, hiển thị lỗi theo dòng/cột.\n• Hàng chưa có master data có thể được tạo trong bước import theo quy tắc hệ thống.\n• Sau import phải tính lại tổng tiền và TSLN.', 'excel', CREATE_SHOT),
    ('2.8', 'Duyệt và từ chối báo giá', 'FR-07', 'action', 'write', 'Duyệt / Từ chối báo giá', 'Thực hiện quyết định ở cấp TP hoặc BGĐ theo cấp duyệt của báo giá.', 'Báo giá ở Chờ TP duyệt hoặc Chờ BGĐ duyệt. Người dùng có Q5/Q6 tương ứng và báo giá nằm trong phòng ban/công ty được phân công.', '1. Người duyệt mở hàng chờ hoặc chi tiết báo giá.\n2. Kiểm tra dữ liệu và tổng giá trị.\n3. Chọn Duyệt hoặc Từ chối.\n4. Nếu từ chối, nhập lý do.\n5. Hệ thống chuyển trạng thái và thông báo.', '• Duyệt cấp TP có thể chuyển sang Chờ BGĐ nếu cấp duyệt là 3.\n• Duyệt cấp cuối chuyển Đã duyệt.\n• Từ chối phải có lý do và bản ghi trở về luồng xử lý theo quy tắc; lịch sử ghi người, thời gian, lý do.', 'approve', DETAIL_SHOT),
    ('2.9', 'Xem chi tiết báo giá', 'FR-11', 'view', 'read', 'Xem chi tiết báo giá', 'Xem toàn bộ thông tin báo giá ở chế độ chỉ đọc.', 'Báo giá nằm trong phạm vi dữ liệu của người dùng hoặc đang chờ chính người dùng duyệt.', '1. Bấm mã báo giá.\n2. Hệ thống tải thông tin chung, bảng chi tiết, tổng hợp và điều khoản.\n3. Người dùng xem các hành động được phép.', '• Giá vốn/TSLN hàng ERP chỉ hiển thị khi có Q9; người lập/người duyệt được xem giá hàng tạm theo quy định.\n• Có thể mở rộng/thu gọn nhóm, hiện/ẩn cột chi tiết; không làm thay đổi dữ liệu.', 'detail', DETAIL_SHOT),
    ('2.10', 'In báo giá', 'FR-08', 'io', 'read', 'In báo giá', 'Mở bản xem trước và in báo giá theo mẫu chứng từ.', 'Người dùng xem được báo giá; báo giá đã có thông tin cần in.', '1. Từ chi tiết chọn In.\n2. Hệ thống dựng bản in theo dữ liệu báo giá.\n3. Người dùng kiểm tra và dùng hộp thoại in của trình duyệt.', '• Chỉ in dữ liệu trình bày cho khách hàng; ghi chú nội bộ và trường nhạy cảm không đưa lên bản in.\n• Công ty/letterhead lấy theo công ty trên chứng từ.', 'detail', DETAIL_SHOT),
    ('2.11', 'Xuất Excel báo giá', 'FR-09', 'io', 'read', 'Xuất Excel', 'Xuất danh sách hoặc dữ liệu chi tiết báo giá ra Excel.', 'Người dùng xem được dữ liệu; quyền xem giá vốn quyết định có xuất giá nhập/TSLN hay không.', '1. Tại danh sách chọn Xuất Excel và chọn trường.\n2. Hoặc tại chi tiết chọn Xuất Excel báo giá.\n3. Hệ thống sinh file và tải xuống.', '• Xuất danh sách tuân theo bộ lọc và phạm vi quyền.\n• Xuất chi tiết dùng khuôn Import/Export; số tiền là số thật để Excel tính SUM.\n• Không có Q9 → giá vốn/TSLN bị ẩn hoặc để trống.', 'excel', LIST_SHOT),
    ('2.12', 'Xem lịch sử báo giá', 'FR-12', 'view', 'read', 'Xem lịch sử', 'Tra cứu lịch sử thay đổi của báo giá và các dòng chi tiết.', 'Người dùng mở được báo giá; không yêu cầu quyền thao tác ghi riêng.', '1. Chọn Lịch sử tại dòng báo giá hoặc chi tiết.\n2. Hệ thống mở popup lịch sử.\n3. Người dùng lọc theo nhóm/thời gian/người thực hiện và xem giá trị cũ - mới.', '• Lịch sử ghi tạo, sửa, gửi duyệt, duyệt, từ chối, xóa và thay đổi dữ liệu bảng.\n• Giá trị cũ hiển thị trước giá trị mới; thay đổi trạng thái có người và thời gian.', 'history', LIST_SHOT),
]

for no, title, code, group, kind, ten, mota, dieukien, chinh, phu, anchor, image in FUNCTIONS:
    d.h3(f'{no} {title}')
    has_uc = kind in ('write', 'crud', 'action', 'io')
    offset = 0
    if has_uc:
        d.p(f'{no}.1 Biểu đồ Usecase')
        d.uc_figure(code, ten, group, actor=ACTOR_BOTH if code == 'FR-07' else ACTOR_P1, caption=f'Biểu đồ Use Case — {code} {ten}')
        offset = 1
    intro_num = f'{no}.{1 + offset}'
    d.p(f'{intro_num} Giới thiệu')
    d.rule_ref('- Màn Danh sách, Validate dữ liệu, Thông báo, Phân quyền và UI/UX. Chỉ bổ sung quy tắc riêng của Báo giá tại phần mô tả chi tiết.', anchor=anchor)
    special = 'Giá bán/giá vốn ERP có thể thay đổi trong khi tạo, sửa hoặc sao chép; hệ thống phải cho người dùng lựa chọn cập nhật giá hiện hành hoặc giữ giá đã lưu.' if code in ('FR-02', 'FR-03', 'FR-04') else None
    d.intro_table(ten=ten, mota=mota, tacnhan='Người dùng nghiệp vụ; Người dùng đã đăng nhập', dieukien=dieukien, chinh=chinh, phu=phu, dacbiet=special)
    layout_num = f'{no}.{2 + offset}'
    d.p(f'{layout_num} Layout màn hình')
    suffix = {'FR-01':'', 'FR-10':' => Tìm kiếm và lọc', 'FR-11':' => Xem chi tiết', 'FR-12':' => Lịch sử', 'FR-02':' => Tạo mới', 'FR-03':' => Chỉnh sửa', 'FR-04':' => Sao chép', 'FR-05':' => Xóa', 'FR-06':' => Import Excel', 'FR-07':' => Xem chi tiết => Duyệt / Từ chối', 'FR-08':' => Xem chi tiết => In', 'FR-09':' => Xuất Excel'}[code]
    d.layout(menu=MENU + suffix, shot=image, shot_caption=ten)
    ui_num = f'{no}.{3 + offset}'
    d.p(f'{ui_num} Mô tả chi tiết giao diện')
    if kind == 'read':
        rows = [
            ('Tiêu đề / mã báo giá', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', 'Hiển thị tên chức năng và mã báo giá.'),
            ('Bảng báo giá / bảng chi tiết', 'Table/Grid', 'Read-only', 'Danh sách', 'Theo dữ liệu', 'Hiển thị nhóm, mã, tên, SL, ĐVT, giá nhập, giá bán, VAT, giảm giá, TSLN và thành tiền.'),
            ('Badge trạng thái', 'Badge', 'Read-only', '7 trạng thái', 'Theo dữ liệu', 'Màu và chữ do BE trả; phân biệt Đang tạo, Chờ duyệt, Đã duyệt, Đóng, Dừng, Trúng thầu.'),
            ('Nút thao tác', 'Button / Icon Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu điều kiện', 'Chỉ hiện hành động phù hợp quyền và trạng thái.'),
            ('Loading / trạng thái rỗng', 'Loading / Alert', 'Hiển thị', '–', 'Ẩn', 'Hiện trong lúc tải; báo không có dữ liệu khi kết quả rỗng.'),
        ]
        d.ui_table(rows, required=False)
    elif kind == 'confirm':
        d.ui_table([
            ('Hộp xác nhận', 'Modal', 'Hiển thị', 'Hiển thị khi bấm Xóa', 'Nêu rõ báo giá sẽ bị xóa và có nút Xóa/Hủy.'),
            ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Chỉ xử lý khi người lập và trạng thái Đang tạo.'),
            ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng popup, không thay đổi dữ liệu.'),
            ('Thông báo lỗi/thành công', 'Toast / Alert', 'Hiển thị', 'Ẩn', 'Hiển thị kết quả sau khi gọi API.'),
        ], required=False, scope=False)
    elif code == 'FR-02':
        d.ui_table([
            ('Dự án TKT', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Có thể bỏ trống để lập báo giá không gắn dự án.'),
            ('Khách hàng', 'Modal / Dropdown', 'Enable', 'Danh sách', 'Có khi không có dự án', 'Trống', 'Chọn trực tiếp khi không gắn dự án.'),
            ('BOM tổng hợp', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Ẩn nếu không có dự án', 'Chỉ hiện BOM đã duyệt phù hợp.'),
            ('Thông tin chung', 'Table/Form', 'Enable', 'Theo trường', 'Theo điều kiện', 'VNĐ mặc định', 'Email có thể sửa; giao hàng là dữ liệu bắt buộc khi gửi duyệt.'),
            ('Bảng chi tiết', 'Table/Grid', 'Enable', 'Danh sách dòng', 'Có khi gửi duyệt', 'Rỗng', 'Thêm nhóm; hàng có sẵn; hàng tạm; dịch vụ; dịch vụ thêm nhanh; kéo sắp xếp; xóa dòng.'),
            ('VAT / Giảm giá / Làm tròn', 'Dropdown / Number', 'Enable / Disable', '0–100; giá trị tiền', 'Theo quyền', 'VAT theo danh mục', 'Có thể áp VAT đồng loạt; phương thức GG là không GG/GG mặt hàng/GG tổng.'),
            ('Điều khoản / ghi chú nội bộ', 'Editor/Textarea', 'Enable', 'Văn bản', 'Không', 'Trống', 'Điều khoản dùng cho khách hàng; ghi chú nội bộ không in.'),
            ('Lưu nháp / Gửi duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', 'Lưu nháp cho phép thiếu dữ liệu nghiệp vụ; Gửi duyệt chạy validate nghiêm ngặt.'),
        ])
    elif code == 'FR-06':
        d.ui_table([
            ('Nút chọn file', 'Button / File', 'Enable', 'XLSX', 'Có', 'Trống', 'Chọn file Excel theo khuôn.'),
            ('Bảng preview import', 'Table/Grid', 'Read-only', 'Danh sách dòng', '–', 'Ẩn', 'Hiển thị dòng hợp lệ, lỗi, giá cũ/mới.'),
            ('Nút Import', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn đến khi preview hợp lệ', 'Ghi dữ liệu sau khi người dùng xác nhận.'),
            ('Lỗi theo dòng/cột', 'Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Không dùng toast thay cho lỗi dòng.'),
        ])
    else:
        d.ui_table([
            ('Nội dung chức năng', 'Table/Grid / Modal', 'Enable / Read-only', 'Theo dữ liệu', '–', 'Theo dữ liệu', 'Hiển thị đúng dữ liệu và trạng thái của báo giá.'),
            ('Nút xác nhận / thao tác', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', 'Không hiện nút khi thiếu quyền hoặc sai trạng thái.'),
            ('Thông báo / lý do', 'Textarea / Alert', 'Enable / Hiển thị', 'Văn bản', 'Theo thao tác', 'Ẩn', 'Từ chối phải nhập lý do; lỗi hiển thị inline hoặc thông báo nghiệp vụ.'),
        ])
    event_num = f'{no}.{4 + offset}'
    d.p(f'{event_num} Danh sách event và xử lý event')
    event_rows = [
        ('Mở chức năng', 'System', 'Before:\n– Kiểm tra đăng nhập, quyền và phạm vi dữ liệu.\nDuring:\n– Nạp dữ liệu cần thiết.\nAfter:\n– Hiển thị giao diện và trạng thái hiện tại.'),
        ('Bấm thao tác chính', 'Click', f'Before:\n– Kiểm tra điều kiện của {ten}.\n– Không đủ quyền/không đúng trạng thái → từ chối và dừng.\nDuring:\n– Kiểm tra dữ liệu đầu vào; lỗi thì giữ nguyên dữ liệu và không ghi.\nAfter:\n– Thực hiện {ten}; ghi lịch sử và thông báo kết quả.'),
        ('Dữ liệu thay đổi', 'Change / Blur', 'Before:\n– Xác định các giá trị phụ thuộc.\nDuring:\n– Tính lại thành tiền, VAT, giảm giá, tổng và TSLN theo bảng công thức.\nAfter:\n– Cập nhật ngay trên giao diện; không tự sửa giá trị người dùng nhập.'),
    ]
    d.event_table(event_rows)

d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('Các quy tắc dùng chung được định nghĩa tại SRS Các quy tắc chung; phần này chỉ ghi quy tắc đặc thù của màn Báo giá.', anchor='list', head='Quy tắc áp dụng', lead='')
d.rule_table([
    ('BR-01', 'Điều kiện tạo báo giá', ['– Có dự án: người lập phải là Sale phụ trách hoặc có quyền xây dựng giá theo nguồn YCBG.', '– Không có dự án: Khách hàng bắt buộc; tiền tệ mặc định VNĐ; không có Giai đoạn dự án/BOM.'], ['Tạo mới', 'Sao chép']),
    ('BR-02', 'Trạng thái và chỉnh sửa', ['– Báo giá mới ở Đang tạo.', '– Chỉ người lập được sửa/xóa bản nháp; các trạng thái Chờ duyệt, Đã duyệt, Đóng, Dừng, Trúng thầu không được sửa.'], ['Tạo mới', 'Chỉnh sửa', 'Xóa']),
    ('BR-03', 'Duyệt và từ chối', ['– Chờ TP duyệt cần quyền Trưởng phòng duyệt giá Bom giải pháp.', '– Chờ BGĐ duyệt cần quyền Ban giám đốc duyệt giá Bom giải pháp.', '– Từ chối phải ghi lý do; mọi chuyển trạng thái ghi lịch sử.'], ['Duyệt', 'Từ chối']),
    ('BR-04', 'Giá ERP thay đổi', ['– Khi tạo/sửa/sao chép phát hiện giá bán hoặc giá vốn ERP đã thay đổi, hiển thị chênh lệch.', '– Người dùng chọn cập nhật giá hiện hành hoặc giữ giá đã lưu; không tự động ghi đè lựa chọn.'], ['Tạo mới', 'Chỉnh sửa', 'Sao chép']),
    ('BR-05', 'Nhóm và dòng chi tiết', ['– Dòng hàng cha không được thấp hơn tổng dòng con về giá bán; hàng tạm/hàng tự xây còn bị kiểm tra giá vốn cha.', '– Thứ tự nhóm/dòng được lưu theo sort_order; xóa dòng phải cập nhật lại tổng.'], ['Tạo mới', 'Chỉnh sửa', 'Import']),
    ('BR-06', 'VAT', ['– VAT hàng ERP lấy từ danh mục ERP; VAT dịch vụ có cost_id lấy từ danh mục chi phí; VAT vận chuyển dùng trường riêng.', '– VAT hợp lệ trong khoảng 0–100%; VAT tính trên giá sau giảm.'], ['Tạo mới', 'Chỉnh sửa', 'Import']),
    ('BR-07', 'Giảm giá', ['– Không GG: không có giảm giá.', '– GG mặt hàng: giảm giá dòng = số tiền giảm trên đơn vị × số lượng.', '– GG tổng: giảm giá được phân bổ vào dòng; chi phí vận chuyển dùng phần phân bổ riêng.'], ['Tạo mới', 'Chỉnh sửa', 'Sao chép']),
    ('BR-08', 'Lưu nháp và gửi duyệt', ['– Lưu nháp cho phép bỏ qua một số required nghiệp vụ và giữ trạng thái Đang tạo.', '– Gửi duyệt bắt buộc kiểm tra trường bắt buộc, giá bán > 0, VAT/giảm giá, quan hệ cha-con và chi phí vận chuyển.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-09', 'Import/Export Excel', ['– Import validate trước, chỉ ghi sau khi xác nhận; lỗi phải chỉ rõ dòng/cột.', '– Export danh sách theo bộ lọc/phạm vi; export chi tiết theo khuôn có thể import lại.'], ['Import', 'Xuất Excel']),
    ('BR-10', 'Lịch sử và dữ liệu nhạy cảm', ['– Ghi lịch sử tạo, sửa, duyệt, từ chối, xóa và thay đổi từng nhóm/dòng.', '– Giá vốn/TSLN hàng ERP chỉ trả khi có quyền xem giá vốn; không để FE tự quyết định quyền.'], ['Mọi chức năng', 'Lịch sử']),
])

d.h2('Bảng công thức và logic tính toán')
d.table(['STT', 'Chỉ tiêu', 'Công thức / logic', 'Ghi chú áp dụng'], [
    ('1', 'Thành tiền nhập dòng', 'Giá nhập × Số lượng', 'Dòng hàng/dịch vụ; hiển thị khi có quyền xem giá vốn.'),
    ('2', 'Thành tiền bán dòng trước giảm', 'Giá bán × Số lượng', 'Dòng cha là cơ sở tính tổng; không cộng lặp dòng con.'),
    ('3', 'Giảm giá theo mặt hàng', 'Giảm giá đơn vị × Số lượng', 'Áp dụng cho hàng hóa, dịch vụ và chi phí vận chuyển theo trường giảm giá riêng.'),
    ('4', 'Giảm giá theo tổng', 'Khoản giảm giá được phân bổ vào từng dòng', 'Dùng allocated_discount_amount; tổng phân bổ bao gồm phần vận chuyển.'),
    ('5', 'Thành tiền bán sau giảm', 'Thành tiền bán trước giảm − Giảm giá', 'Không được âm; gửi duyệt kiểm tra thành tiền dòng > 0.'),
    ('6', 'Tiền VAT dòng', 'Thành tiền sau giảm × VAT% / 100', 'VAT hàng ERP/dịch vụ lấy từ danh mục; vận chuyển dùng VAT vận chuyển.'),
    ('7', 'Thành tiền sau VAT dòng', 'Thành tiền sau giảm + Tiền VAT', 'Dùng cho bảng chi tiết và bảng tổng hợp.'),
    ('8', 'TSLN dòng', '(Thành tiền bán sau giảm − Thành tiền nhập) / Thành tiền nhập × 100%', 'Nếu giá nhập ≤ 0 thì hiển thị “—”; màu theo ngưỡng TSLN cấu hình.'),
    ('9', 'Tổng trước VAT', 'Tổng thành tiền bán trước giảm − Tổng giảm giá', 'Cộng hàng hóa, dịch vụ, chi phí và vận chuyển.'),
    ('10', 'Tổng VAT', 'Tổng VAT của các dòng', 'Tính trên từng dòng sau giảm rồi cộng.'),
    ('11', 'Tổng giá trị báo giá sau VAT', 'Tổng trước VAT + Tổng VAT', 'Lưu vào total_after_vat và hiển thị trên danh sách/chi tiết.'),
    ('12', 'TSLN tổng', '(Tổng bán sau giảm − Tổng nhập) / Tổng nhập × 100%', 'Chỉ hiển thị khi có dữ liệu giá nhập hợp lệ; không lộ giá vốn nếu thiếu quyền.'),
    ('13', 'Làm tròn', 'Làm tròn theo rounding_mode từ hàng nghìn đến 2 số lẻ', 'VNĐ mặc định làm tròn số nguyên; ngoại tệ dùng cấu hình số lẻ.'),
], widths=[0.45, 1.35, 2.65, 1.55])

d.save()
print(OUT)
