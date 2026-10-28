# -*- coding: utf-8 -*-
"""Dựng 3 HDSD (bản GỌN, không ảnh) cho 3 phiếu đầu luồng nhập mua hàng ngoài:
  1. Yêu cầu đặt hàng mua ngoài  (InlandOrderRequest)
  2. Hợp đồng mua hàng ngoài     (InlandBuyContract)
  3. Phiếu báo hàng về           (ProductArrivedNotify)

User chốt 2026-10-13: KHÔNG cần ảnh → bỏ toàn bộ ảnh màn hình / ảnh nút / sơ đồ ảnh.
Vì là chứng từ giao dịch (không phải màn danh mục) nên viết generator tay bằng QgWriter
trên khuôn gọn HDSD_MAU_GON.docx. Nhãn nút để trong ngoặc vuông in đậm **[...]**.
"""
import os
import sys

LIB = '/Users/nguyentrancu/DEV/code/hrm-claude-config/hrm/.plans/gop-db/_catalog_docs_lib'
TPL = '/Users/nguyentrancu/DEV/code/hrm-claude-config/hrm/.claude/skills/hdsd-documenter/assets/HDSD_MAU_GON.docx'
OUT = '/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/TanPhatDev/.plans/hdsd-luong-nhap-mua-ngoai'
sys.path.insert(0, LIB)
from qg_writer import QgWriter  # noqa: E402

ROLES = {'pagebreak': 33, 'h1': 34, 'h2': 21, 'p': 28,
         'step': 43, 'sub': 49, 'sub2': 126,
         'img': 45, 'cap': 46, 'blank': 23, 'tbl2': 22, 'tbl4': 25}

VERSION_ROWS = [
    ['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung'],
    ['1.0', '13/10/2026', 'Phòng Phát triển', 'Khởi tạo tài liệu hướng dẫn sử dụng'],
]


def emit_steps(w, items):
    """items: list; phần tử là chuỗi (một Bước, tự đánh số) hoặc ('sub', 'Hoặc ...')."""
    n = 0
    for it in items:
        if isinstance(it, tuple) and it[0] == 'sub':
            w.raw('sub', it[1])
        else:
            n += 1
            w.step('Bước %d: %s' % (n, it))


def tong_quan(w, thuat_ngu, quyen_rows, func_rows, quyen_note=None):
    w.h1('TỔNG QUAN', new_page=True)
    w.h2('1. Thuật ngữ sử dụng trong tài liệu')
    w.table([['Thuật ngữ', 'Giải thích']] + thuat_ngu, widths=[2.2, 5.0])
    w.h2('2. Cập nhật tài liệu')
    w.table(VERSION_ROWS, widths=[1.0, 1.3, 1.7, 3.0])
    w.h2('3. Quyền sử dụng')
    w.table([['Chức năng', 'Quyền cần có']] + quyen_rows, widths=[3.2, 3.8])
    if quyen_note:
        w.p(quyen_note)
    w.h2('4. Sơ đồ chức năng tổng quan')
    w.p('Màn hình gồm các chức năng chính sau:')
    w.table([['STT', 'Chức năng']] + func_rows, widths=[0.8, 6.2])


def build(cfg):
    w = QgWriter(TPL, ROLES, body_from=19,
                 cover_replace={'Danh mục khu vực': cfg['screen']})
    tong_quan(w, cfg['thuat_ngu'], cfg['quyen'], cfg['func_rows'], cfg.get('quyen_note'))
    for title, steps in cfg['parts']:
        w.h1(title, new_page=True)
        emit_steps(w, steps)
    w.rebuild_toc(levels=(1, 2))
    out = os.path.join(OUT, cfg['file'])
    w.save(out)
    print('ĐÃ DỰNG:', out)
    return out


# ============================================================ PHIẾU 1 — YCĐH
DOC1 = {
    'screen': 'Yêu cầu đặt hàng mua ngoài',
    'file': 'HDSD_Yeu_cau_dat_hang_mua_ngoai.docx',
    'thuat_ngu': [
        ['Yêu cầu đặt hàng mua ngoài', 'Phiếu đề nghị mua hàng hóa từ nhà cung cấp bên ngoài, phục vụ cho khách hàng.'],
        ['Đang tạo', 'Phiếu mới lưu nháp, chưa gửi; chỉ người lập thấy và sửa/xóa được.'],
        ['Chờ TP duyệt', 'Phiếu đã gửi, đang chờ Trưởng phòng duyệt.'],
        ['Chờ duyệt giá', 'Trưởng phòng đã duyệt, đang chờ bộ phận Kiểm soát duyệt giá.'],
        ['Đã duyệt giá', 'Phiếu đã được duyệt giá; có thể lập hợp đồng, lập phụ lục, duyệt lại giá hoặc hủy.'],
        ['Đang lập hợp đồng', 'Đang lập hợp đồng mua từ phiếu.'],
        ['Đã lập hợp đồng', 'Đã lập xong hợp đồng mua từ phiếu.'],
        ['Đã hủy', 'Phiếu đã bị hủy.'],
    ],
    'quyen': [
        ['Xem danh sách theo tổng công ty', 'Xem đặt hàng mua ngoài theo tổng công ty'],
        ['Xem danh sách theo công ty', 'Xem đặt hàng mua ngoài theo công ty'],
        ['Xem danh sách theo phòng ban', 'Xem đặt hàng mua ngoài theo phòng ban'],
        ['Trưởng phòng duyệt yêu cầu', 'Duyệt yêu cầu đặt hàng ngoài'],
        ['Duyệt giá (Kiểm soát)', 'Kiểm soát yêu cầu đặt hàng ngoài'],
        ['Tạo / Sửa / Xóa / Lập hợp đồng', 'Theo người lập phiếu và trạng thái phiếu (không cần quyền riêng)'],
    ],
    'quyen_note': 'Nếu không có quyền xem nào ở trên, người dùng chỉ nhìn thấy các phiếu do chính mình tạo.',
    'func_rows': [
        ['1', 'Truy cập và tìm kiếm'],
        ['2', 'Tạo mới yêu cầu'],
        ['3', 'Sửa yêu cầu'],
        ['4', 'Xóa yêu cầu'],
        ['5', 'Trưởng phòng duyệt yêu cầu'],
        ['6', 'Duyệt yêu cầu (duyệt giá)'],
        ['7', 'Yêu cầu duyệt lại giá'],
        ['8', 'Lập hợp đồng'],
        ['9', 'Tạo phụ lục mua hàng bổ sung'],
        ['10', 'In'],
        ['11', 'Hủy phiếu'],
        ['12', 'Xem chi tiết'],
        ['13', 'Xuất Excel'],
    ],
    'parts': [
        ('PHẦN 1: TRUY CẬP VÀ TÌM KIẾM', [
            'Từ phân hệ **[Kho]**, tại menu **[Mua ngoài]**, nhóm **[Yêu cầu mua]**, chọn **[Danh sách yêu cầu đặt hàng mua ngoài]**.',
            'Tại dòng tìm kiếm trên đầu bảng, nhập hoặc chọn điều kiện lọc:',
            ('sub', 'Hoặc nhập **Số phiếu** cần tìm.'),
            ('sub', 'Hoặc nhập **mã/tên hàng hóa** để tìm theo hàng hóa.'),
            ('sub', 'Hoặc chọn **Người tạo** để lọc theo người tạo.'),
            ('sub', 'Hoặc chọn **Người duyệt** để lọc theo người duyệt giá.'),
            ('sub', 'Hoặc chọn **Khách hàng** để lọc theo khách hàng.'),
            ('sub', 'Hoặc chọn **Trạng thái** để lọc theo trạng thái phiếu.'),
            ('sub', 'Hoặc chọn khoảng thời gian để lọc theo ngày tạo.'),
            'Danh sách tự lọc theo điều kiện đã nhập.',
        ]),
        ('PHẦN 2: TẠO MỚI YÊU CẦU', [
            'Tại màn hình **Danh sách yêu cầu đặt hàng mua ngoài**, bấm **[Thêm mới]**.',
            'Hệ thống mở màn **Tạo yêu cầu đặt hàng ngoài**.',
            'Nhập thông tin chung: **Kiểm soát duyệt**, **Ghi chú**, đính kèm **File đính kèm**.',
            'Tại mục **Chi tiết**, bấm thêm hàng hóa để mở cửa sổ **Tìm kiếm hàng hóa** và chọn hàng hóa.',
            'Với mỗi hàng hóa, chọn **ĐVT**, nhập **Giá đề xuất mua trước VAT**; thêm từng dòng **Khách hàng**, **Số Lượng**, **Ngày cần**.',
            'Nhập đầy đủ thông tin bắt buộc: **ĐVT**, **Khách hàng**, **Số Lượng**, **Ngày cần** (sau ngày hôm nay), **Giá đề xuất mua trước VAT**, **Ghi chú**, **File đính kèm**.',
            'Bấm **[Lưu]** để lưu nháp (trạng thái Đang tạo).',
            ('sub', 'Hoặc bấm **[Lưu & Gửi]** để gửi duyệt (trạng thái Chờ TP duyệt).'),
            ('sub', 'Hoặc bấm **[Hủy]** để thoát không lưu.'),
        ]),
        ('PHẦN 3: SỬA YÊU CẦU', [
            'Tại cột **Hành động**, bấm **[Sửa yêu cầu]** (chỉ hiện với phiếu **Đang tạo** do bạn lập).',
            'Chỉnh sửa thông tin như khi tạo mới.',
            'Bấm **[Lưu]** để lưu, hoặc **[Lưu & Gửi]** để gửi duyệt.',
            ('sub', 'Hoặc bấm **[Hủy]** để thoát không lưu.'),
        ]),
        ('PHẦN 4: XÓA YÊU CẦU', [
            'Tại cột **Hành động**, bấm **[Xóa yêu cầu]** (chỉ hiện với phiếu **Đang tạo** do bạn lập).',
            'Hệ thống hiện hộp xác nhận xóa.',
            'Bấm **[Xác nhận]** để xóa phiếu.',
            ('sub', 'Hoặc bấm **[Hủy]** nếu bấm nhầm.'),
        ]),
        ('PHẦN 5: TRƯỞNG PHÒNG DUYỆT YÊU CẦU', [
            'Tại cột **Hành động**, bấm **[TP duyệt yêu cầu]** (phiếu **Chờ TP duyệt**).',
            'Hệ thống mở màn **Chi tiết yêu cầu đặt hàng ngoài**.',
            'Xem thông tin chung và chi tiết hàng hóa.',
            'Bấm **[Duyệt]** để chuyển phiếu sang **Chờ duyệt giá**.',
            ('sub', 'Hoặc nhập **Ghi chú duyệt** rồi bấm **[Không duyệt]** để trả phiếu về **Đang tạo**.'),
        ]),
        ('PHẦN 6: DUYỆT YÊU CẦU (DUYỆT GIÁ)', [
            'Tại cột **Hành động**, bấm **[Duyệt yêu cầu]** (phiếu **Chờ duyệt giá**).',
            'Hệ thống mở màn **Duyệt yêu cầu đặt hàng ngoài**.',
            'Với mỗi hàng hóa, nhập **Giá duyệt**, chọn **Nhà cung cấp**, phân bổ **Số Lượng** cho người đi mua và chọn người đi mua.',
            'Nhập **Ghi chú duyệt** nếu cần.',
            'Bấm **[Duyệt]** để duyệt giá (phiếu sang **Đã duyệt giá**).',
            ('sub', 'Hoặc nhập **Ghi chú duyệt** rồi bấm **[Không duyệt]** để từ chối (phiếu về **Đang tạo**).'),
        ]),
        ('PHẦN 7: YÊU CẦU DUYỆT LẠI GIÁ', [
            'Tại cột **Hành động**, bấm **[Yêu cầu duyệt lại giá]** (phiếu **Đã duyệt giá**, chưa lập xong hợp đồng).',
            'Hệ thống mở màn **Duyệt lại giá yêu cầu đặt hàng ngoài**.',
            'Chỉnh lại **Giá đề xuất**, **Giá duyệt**, **Số Lượng** người mua; thêm/xóa file đính kèm nếu cần.',
            'Bấm **[Lưu]** để giữ nguyên trạng thái.',
            ('sub', 'Hoặc bấm **[Lưu & Gửi]** để gửi lại cho Kiểm soát duyệt lại.'),
        ]),
        ('PHẦN 8: LẬP HỢP ĐỒNG', [
            'Tại cột **Hành động**, bấm **[Lập hợp đồng]** (phiếu **Đã duyệt giá** / **Đang lập hợp đồng** / **Đã lập hợp đồng**, chưa lập xong).',
            'Hệ thống chuyển sang màn tạo **Hợp đồng mua hàng ngoài** với dữ liệu phiếu.',
            'Khai hợp đồng rồi lưu (xem tài liệu Hợp đồng mua hàng ngoài).',
        ]),
        ('PHẦN 9: TẠO PHỤ LỤC MUA HÀNG BỔ SUNG', [
            'Tại cột **Hành động**, bấm **[Tạo phụ lục mua hàng bổ sung]** (phiếu **Đã duyệt giá** hoặc **Đang lập hợp đồng**, do bạn lập).',
            'Hệ thống chuyển sang màn tạo phụ lục bổ sung của hợp đồng mua ngoài.',
        ]),
        ('PHẦN 10: IN', [
            'Tại cột **Hành động**, bấm **[In]**.',
            'Hệ thống mở bản in phiếu ở tab mới; thực hiện in từ trình duyệt.',
        ]),
        ('PHẦN 11: HỦY PHIẾU', [
            'Tại cột **Hành động**, bấm **[Hủy]** (chỉ hiện với phiếu **Đã duyệt**).',
            'Hệ thống hiện hộp xác nhận **Xác nhận hủy!**.',
            'Bấm **[Xác nhận]** để hủy phiếu.',
            ('sub', 'Hoặc bấm **[Hủy]** để bỏ qua.'),
        ]),
        ('PHẦN 12: XEM CHI TIẾT', [
            'Bấm vào **Số phiếu** trên danh sách.',
            'Hệ thống mở màn **Chi tiết yêu cầu đặt hàng ngoài** (chỉ xem).',
        ]),
        ('PHẦN 13: XUẤT EXCEL', [
            'Lọc danh sách theo dữ liệu cần lấy (xem PHẦN 1).',
            'Bấm **[Xuất Excel]**.',
            'Hệ thống tải về file **danh_sach_dat_hang_ngoai.xlsx** theo bộ lọc hiện tại.',
        ]),
    ],
}

# ============================================================ PHIẾU 2 — HĐ mua ngoài
DOC2 = {
    'screen': 'Hợp đồng mua hàng ngoài',
    'file': 'HDSD_Hop_dong_mua_hang_ngoai.docx',
    'thuat_ngu': [
        ['Hợp đồng mua hàng ngoài', 'Hợp đồng mua hàng hóa từ nhà cung cấp bên ngoài, lập từ phiếu yêu cầu đặt hàng mua ngoài.'],
        ['Phụ lục bổ sung', 'Phụ lục thêm hàng hóa vào hợp đồng mua hàng ngoài đã duyệt.'],
        ['Phụ lục giảm', 'Phụ lục giảm hàng hóa khỏi hợp đồng mua hàng ngoài đã duyệt.'],
        ['Đang tạo', 'Hợp đồng đã lưu nháp, chưa gửi; người lập còn sửa/xóa được. Hợp đồng bị Không duyệt hoặc bị Hủy cũng về trạng thái này.'],
        ['Chờ duyệt', 'Hợp đồng đã gửi, đang chờ người duyệt xử lý.'],
        ['Đã duyệt', 'Hợp đồng đã được duyệt; có thể tạo phiếu báo hàng về, tạo phụ lục bổ sung/giảm hoặc hủy duyệt.'],
    ],
    'quyen': [
        ['Xem hợp đồng theo tổng công ty', 'Xem hợp đồng mua ngoài theo tổng công ty'],
        ['Xem hợp đồng theo công ty', 'Xem hợp đồng mua ngoài theo công ty'],
        ['Xem hợp đồng theo phòng ban', 'Xem hợp đồng mua ngoài theo phòng ban'],
        ['Xem hợp đồng theo bộ phận', 'Xem hợp đông mua ngoài theo bộ phận'],
        ['Duyệt / Không duyệt hợp đồng', 'Duyệt hợp đồng đặt hàng ngoài'],
        ['Lập / Sửa / Xóa hợp đồng', 'Theo người lập phiếu và trạng thái phiếu (không cần quyền riêng)'],
    ],
    'quyen_note': 'Nếu không có quyền xem nào ở trên, người dùng chỉ nhìn thấy các hợp đồng do chính mình lập.',
    'func_rows': [
        ['1', 'Truy cập và tìm kiếm'],
        ['2', 'Tạo hợp đồng mua hàng ngoài'],
        ['3', 'Sửa hợp đồng'],
        ['4', 'Duyệt hợp đồng'],
        ['5', 'Tạo phiếu báo hàng về'],
        ['6', 'Tạo phụ lục bổ sung'],
        ['7', 'Tạo phụ lục giảm'],
        ['8', 'Hủy (hủy duyệt)'],
        ['9', 'In hợp đồng'],
        ['10', 'In phụ lục'],
        ['11', 'Xóa hợp đồng'],
        ['12', 'Xuất Excel'],
    ],
    'parts': [
        ('PHẦN 1: TRUY CẬP VÀ TÌM KIẾM', [
            'Từ phân hệ **[Mua hàng]**, tại menu **[Mua ngoài]**, nhóm **[Yêu cầu mua]**, chọn **[Danh sách hợp đồng mua hàng ngoài]**.',
            'Tại dòng tìm kiếm trên đầu bảng, nhập hoặc chọn điều kiện lọc:',
            ('sub', 'Hoặc nhập **Số hợp đồng**.'),
            ('sub', 'Hoặc chọn **Nhà cung cấp**.'),
            ('sub', 'Hoặc nhập **Hàng hóa** (tên hoặc mã).'),
            ('sub', 'Hoặc chọn **Trạng thái**.'),
            ('sub', 'Hoặc chọn **Người lập** hoặc **Người duyệt**.'),
            ('sub', 'Hoặc nhập **Số tiền từ khoảng** và **Số tiền đến khoảng**.'),
            ('sub', 'Hoặc chọn khoảng thời gian để lọc theo ngày lập.'),
            'Danh sách tự lọc theo điều kiện đã nhập.',
        ]),
        ('PHẦN 2: TẠO HỢP ĐỒNG MUA HÀNG NGOÀI', [
            'Vào màn **Danh sách yêu cầu đặt hàng mua ngoài**, chọn nhóm mua rồi bấm **[Lập hợp đồng]** (màn danh sách hợp đồng không có nút Thêm mới).',
            'Hệ thống mở màn **Hợp đồng mua hàng** với dữ liệu yêu cầu đặt hàng.',
            'Nhập thông tin chung: **Số hợp đồng**, **Ngày Hợp Đồng**, **Ký duyệt**, **Nhà cung cấp**.',
            'Khai các tab: **1. Hàng hóa**, **2. Khuyến mại**, **3. Chi phí**, **4. Thông tin thanh toán**, **Giao hàng**, **Thanh toán**, và chọn **Mẫu in**.',
            'Chọn **Người duyệt** và **Chức vụ** người duyệt.',
            'Nhập đầy đủ thông tin bắt buộc: **Nhóm mua**, **Số hợp đồng** (không trùng), **Ngày Hợp Đồng**, **Ký duyệt**, **Nhà cung cấp**, **Mẫu in**, **Người duyệt** và **Chức vụ**, ít nhất một dòng hàng hóa, một đợt thanh toán và một dòng giao hàng.',
            'Nếu nhà cung cấp là Tổ chức hoặc Nước ngoài, nhập thêm **Người đại diện** và **Chức vụ đại diện**; nếu là Nước ngoài, nhập thêm **Ngân hàng NCC**.',
            'Bấm **[Lưu]** để lưu nháp (trạng thái Đang tạo).',
            ('sub', 'Hoặc bấm **[Lưu & Gửi]** để gửi duyệt (trạng thái Chờ duyệt).'),
        ]),
        ('PHẦN 3: SỬA HỢP ĐỒNG', [
            'Tại cột **Hành động**, bấm **[Sửa hợp đồng]** (phiếu **Đang tạo**, do bạn lập).',
            'Chỉnh sửa thông tin như khi tạo (ô **Số hợp đồng** bị khóa, không sửa được).',
            'Bấm **[Lưu]** để lưu, hoặc **[Lưu & Gửi]** để gửi duyệt.',
        ]),
        ('PHẦN 4: DUYỆT HỢP ĐỒNG', [
            'Tại cột **Hành động**, bấm **[Duyệt hợp đồng]** (phiếu **Chờ duyệt**, bạn là người duyệt).',
            'Hệ thống mở màn chi tiết hợp đồng.',
            'Xem nội dung hợp đồng.',
            'Bấm **[Duyệt]** để duyệt (phiếu sang **Đã duyệt**).',
            ('sub', 'Hoặc nhập **Ghi chú duyệt** rồi bấm **[Không duyệt]** để trả hợp đồng về **Đang tạo**.'),
        ]),
        ('PHẦN 5: TẠO PHIẾU BÁO HÀNG VỀ', [
            'Tại cột **Hành động**, bấm **[Tạo phiếu báo hàng về]** (phiếu **Đã duyệt**, bạn là người lập hoặc Super Admin).',
            'Hệ thống chuyển sang màn **Lập Phiếu Báo Hàng Về** với dữ liệu hàng hóa của hợp đồng.',
            'Khai phiếu báo hàng về rồi gửi (xem tài liệu Phiếu báo hàng về).',
        ]),
        ('PHẦN 6: TẠO PHỤ LỤC BỔ SUNG', [
            'Tại cột **Hành động**, bấm **[Tạo PL bổ sung]** (phiếu **Đã duyệt**, do bạn lập).',
            'Hệ thống chuyển sang màn tạo phụ lục bổ sung của hợp đồng.',
        ]),
        ('PHẦN 7: TẠO PHỤ LỤC GIẢM', [
            'Tại cột **Hành động**, bấm **[Tạo PL giảm]** (phiếu **Đã duyệt**, do bạn lập, chưa có phiếu báo hàng về).',
            'Hệ thống chuyển sang màn tạo phụ lục giảm của hợp đồng.',
        ]),
        ('PHẦN 8: HỦY (HỦY DUYỆT)', [
            'Tại cột **Hành động**, bấm **[Hủy]** (phiếu **Đã duyệt**, bạn là người duyệt, chưa có phụ lục hoặc phiếu báo hàng về).',
            'Hệ thống hiện hộp xác nhận **Xác nhận hủy!**.',
            'Bấm **[Xác nhận]** để đưa hợp đồng về **Đang tạo**.',
            ('sub', 'Hoặc bấm **[Hủy]** để bỏ qua.'),
        ]),
        ('PHẦN 9: IN HỢP ĐỒNG', [
            'Tại cột **Hành động**, bấm **[In hợp đồng]**.',
            'Hệ thống mở bản in hợp đồng theo mẫu đã chọn.',
        ]),
        ('PHẦN 10: IN PHỤ LỤC', [
            'Tại cột **Hành động**, bấm **[In phụ lục]**.',
            'Hệ thống mở bản in phụ lục hợp đồng.',
        ]),
        ('PHẦN 11: XÓA HỢP ĐỒNG', [
            'Tại cột **Hành động**, bấm **[Xóa hợp đồng]** (phiếu **Đang tạo**, do bạn lập).',
            'Hệ thống hiện hộp xác nhận xóa.',
            'Bấm **[Xác nhận]** để xóa hợp đồng.',
            ('sub', 'Hoặc bấm **[Hủy]** nếu bấm nhầm.'),
        ]),
        ('PHẦN 12: XUẤT EXCEL', [
            'Lọc danh sách theo dữ liệu cần lấy (xem PHẦN 1).',
            'Bấm **[Xuất Excel]**.',
            'Hệ thống tải về file **danh_sach_hop_dong_ngoai.xlsx** theo bộ lọc hiện tại.',
        ]),
    ],
}

# ============================================================ PHIẾU 3 — Báo hàng về
DOC3 = {
    'screen': 'Phiếu báo hàng về',
    'file': 'HDSD_Phieu_bao_hang_ve.docx',
    'thuat_ngu': [
        ['Phiếu báo hàng về', 'Phiếu ghi nhận hàng của một hợp đồng mua hàng ngoài đã về, báo cho thủ kho và người yêu cầu đặt hàng.'],
        ['Nhập thẳng', 'Hình thức nhận hàng giao thẳng, không qua kho (không cần chọn kho nhập).'],
        ['Đã gửi', 'Phiếu vừa được lập và gửi; đã báo cho thủ kho và người yêu cầu đặt hàng. Còn được phép tạo yêu cầu nhập hàng.'],
        ['Đã yêu cầu nhập hàng', 'Đã lập tiếp phiếu yêu cầu nhập hàng từ phiếu này.'],
    ],
    'quyen': [
        ['Xem danh sách phiếu của mình', 'Mọi người đăng nhập (chỉ thấy phiếu do mình lập)'],
        ['Xem chi tiết phiếu', 'Người lập, thủ kho của kho trên phiếu, hoặc người yêu cầu đặt hàng'],
        ['Lập phiếu báo hàng về', 'Người được phép lập trên hợp đồng mua hàng ngoài'],
        ['Tạo yêu cầu nhập hàng', 'Người lập phiếu, khi phiếu ở trạng thái Đã gửi'],
    ],
    'quyen_note': 'Màn hình này không gắn quyền riêng theo tên; việc hiển thị và thao tác được kiểm soát theo vai trò (người lập, thủ kho, người yêu cầu đặt hàng) và trạng thái phiếu.',
    'func_rows': [
        ['1', 'Truy cập và tìm kiếm'],
        ['2', 'Lập phiếu báo hàng về'],
        ['3', 'Tạo yêu cầu nhập hàng'],
        ['4', 'Xem chi tiết'],
        ['5', 'In'],
        ['6', 'Xuất Excel'],
    ],
    'parts': [
        ('PHẦN 1: TRUY CẬP VÀ TÌM KIẾM', [
            'Từ phân hệ **[Mua hàng]**, tại menu **[Mua ngoài]**, chọn **[Danh sách phiếu báo hàng về]**.',
            'Tại dòng tìm kiếm trên đầu bảng, nhập hoặc chọn điều kiện lọc:',
            ('sub', 'Hoặc nhập **Mã** phiếu.'),
            ('sub', 'Hoặc nhập **Hợp đồng** (số hợp đồng).'),
            ('sub', 'Hoặc nhập **Tên, mã hàng**.'),
            ('sub', 'Hoặc chọn **Kho**.'),
            ('sub', 'Hoặc chọn **NCC** (nhà cung cấp).'),
            ('sub', 'Hoặc chọn **Trạng thái**.'),
            ('sub', 'Hoặc chọn khoảng thời gian để lọc theo ngày tạo.'),
            'Danh sách tự lọc theo điều kiện đã nhập.',
        ]),
        ('PHẦN 2: LẬP PHIẾU BÁO HÀNG VỀ', [
            'Vào màn chi tiết **Hợp đồng mua hàng ngoài** (hoặc phụ lục), bấm **[Tạo phiếu báo hàng về]** (lối lập phiếu không nằm ở màn danh sách).',
            'Hệ thống mở màn **Lập Phiếu Báo Hàng Về** với hàng hóa của hợp đồng đã nạp sẵn.',
            'Chọn **Kho nhập**.',
            ('sub', 'Hoặc tích **Nhập thẳng** nếu giao thẳng không qua kho (khi đó không cần chọn kho).'),
            'Nhập **Dự kiến về kho**.',
            'Nhập **Ghi chú** nếu cần.',
            'Tại bảng **1. Hàng hóa** (và **2. Khuyến mại**), nhập **SL** hàng về theo từng dòng khách hàng.',
            'Nhập đầy đủ thông tin bắt buộc: **Số hợp đồng**, **Kho nhập** (trừ khi tích Nhập thẳng), **Dự kiến về kho** (từ hôm nay trở đi), và ít nhất một mặt hàng có số lượng về lớn hơn 0.',
            'Bấm **[Gửi]** để gửi phiếu (trạng thái **Đã gửi**).',
            ('sub', 'Hoặc bấm **[Hủy]** để quay lại danh sách.'),
        ]),
        ('PHẦN 3: TẠO YÊU CẦU NHẬP HÀNG', [
            'Tại cột **Hành động**, bấm **[Tạo yêu cầu nhập hàng]** (phiếu **Đã gửi**, do bạn lập).',
            ('sub', 'Hoặc trong màn chi tiết phiếu, bấm **[Tạo phiếu yêu cầu nhập hàng]**.'),
            'Hệ thống chuyển sang màn **Lập phiếu yêu cầu nhập hàng** kèm dữ liệu phiếu báo hàng về.',
            'Sau khi tạo xong yêu cầu nhập hàng, phiếu chuyển sang **Đã yêu cầu nhập hàng**.',
        ]),
        ('PHẦN 4: XEM CHI TIẾT', [
            'Bấm vào **Số phiếu** trên danh sách.',
            'Hệ thống mở màn **Phiếu báo hàng về** (chỉ xem).',
        ]),
        ('PHẦN 5: IN', [
            'Tại cột **Hành động**, bấm **[In]**.',
            'Hệ thống mở bản in **Chi tiết phiếu báo hàng về** ở tab mới.',
        ]),
        ('PHẦN 6: XUẤT EXCEL', [
            'Lọc danh sách theo dữ liệu cần lấy (xem PHẦN 1).',
            'Bấm **[Xuất Excel]**.',
            'Hệ thống tải về file **phieu_bao_hang_ve.xlsx**.',
        ]),
    ],
}


if __name__ == '__main__':
    for cfg in (DOC1, DOC2, DOC3):
        build(cfg)
    print('XONG 3 FILE.')
