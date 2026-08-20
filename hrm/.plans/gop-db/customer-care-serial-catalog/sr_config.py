# -*- coding: utf-8 -*-
"""Cau hinh man 'Danh muc serial thiet bi lam dich vu' (/customer-care/serials).

Doc code 18/08/2026:
  BE  Modules/CustomerCare/Routes/api.php (149-158) — CHI DOC, 1 quyen
      "Xem danh muc serial thiet bi lam dich vu"; khong co route ghi, khong co route export.
  FE  hrm-client/pages/customer-care/serials/index.vue — tu dung file Excel bang ExcelJS,
      lay du lieu theo tung lo qua chinh route index (bang hon 21 nghin dong).
  Anh that: sr_shots/ (cong dev hrm-crm.eteksofts.com, 18/08/2026)
"""

HOST = 'http://hrm-crm.eteksofts.com'

SERIAL = dict(
    key='sr',
    ten='Danh mục serial thiết bị làm dịch vụ',
    doi_tuong='serial thiết bị',
    route='/customer-care/serials',
    host=HOST,
    menu='Phân hệ CSKH → Danh mục → Danh mục serial thiết bị làm dịch vụ',
    quyen_quan_ly='Xem danh mục serial thiết bị làm dịch vụ',
    quyen_xem=None,
    tacdung_ql='Mở màn hình để tra cứu và xuất Excel. Đây là màn hình CHỈ ĐỌC nên quyền này '
               'cũng là quyền duy nhất; không có thao tác thêm, sửa hay xóa.',
    tacdung_xem='',
    ghichu_quyen='Màn hình chỉ có MỘT quyền và là quyền tra cứu. Việc thêm, sửa, đổi và xóa '
                 'serial nằm ở màn Quản lý khách hàng, tab Trang thiết bị — không thực hiện '
                 'được từ màn này. Người không có quyền thì mục menu không hiển thị và truy '
                 'cập thẳng đường dẫn cũng bị chặn.',
    co_trangthai=False,
    truong_trung=None,
    loi_trung=None,
    muc_dich=[
        'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn tra cứu Danh mục serial thiết bị '
        'làm dịch vụ.',
        'Là căn cứ nghiệm thu chức năng tra cứu, lọc và xuất Excel.',
        'Làm rõ phạm vi: đây là màn CHỈ ĐỌC, mọi thao tác ghi serial thuộc màn Quản lý khách '
        'hàng nên không đặc tả ở tài liệu này.',
        'Ghi nhận cách xuất Excel: tệp được dựng ngay trên trình duyệt theo từng lô dữ liệu, '
        'do bảng có hơn hai mươi nghìn dòng.',
    ],
    thuat_ngu=[
        ('Serial thiết bị làm dịch vụ',
         'Số hiệu riêng của một thiết bị cụ thể đang được bảo hành hoặc bảo dưỡng, dùng để '
         'truy vết thiết bị qua các lần làm dịch vụ.'),
        ('Tên hàng', 'Tên hàng hóa / thiết bị mà serial này thuộc về.'),
        ('Khách hàng', 'Đơn vị đang sở hữu hoặc sử dụng thiết bị mang serial này.'),
        ('Màn hình chỉ đọc',
         'Màn hình chỉ cho tra cứu và kết xuất, không có bất kỳ thao tác thay đổi dữ liệu nào.'),
    ],
    cot=[
        ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
        ('Serial thiết bị làm dịch vụ', 'Số hiệu riêng của thiết bị. Luôn hiển thị, sắp xếp được.'),
        ('Tên hàng', 'Tên hàng hóa / thiết bị tương ứng.'),
        ('Khách hàng', 'Mã và tên đơn vị đang sở hữu thiết bị.'),
        ('Người cập nhật', 'Họ tên người sửa gần nhất. Mặc định ẩn.'),
        ('Ngày cập nhật', 'Ngày giờ sửa gần nhất, sắp xếp được. Mặc định ẩn.'),
        ('Người tạo', 'Họ tên người đã thêm bản ghi.'),
        ('Ngày tạo', 'Ngày giờ thêm bản ghi, sắp xếp được.'),
        ('Trạng thái', 'Tình trạng của serial, hiển thị dạng badge.'),
    ],
    nut_thanh_cong_cu=[
        ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn và sắp xếp các ô lọc.'),
        ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Đang thu gọn',
         'Bật / tắt khu vực lọc nâng cao.'),
        ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn trường cần xuất.'),
        ('Nút Tùy chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn cột hiển thị trên bảng.'),
    ],
    loc=[
        ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
         'Tìm đồng thời theo serial, tên hàng và tên khách hàng.'),
        ('Khách hàng', 'Dropdown', 'Danh sách', 'Trống',
         'Lọc theo đơn vị đang sở hữu thiết bị.'),
        ('Trạng thái', 'Dropdown', 'Danh sách', 'Trống',
         'Lọc theo tình trạng của serial. Bỏ trống thì hiện mọi trạng thái.'),
        ('Người tạo', 'Dropdown', 'Danh sách', 'Trống', 'Lọc theo người đã thêm bản ghi.'),
        ('Người cập nhật', 'Dropdown', 'Danh sách', 'Trống', 'Lọc theo người sửa gần nhất.'),
    ],
    truong=[
        ('Serial thiết bị làm dịch vụ', 'Textbox', 'Read-only', '0–255 ký tự', 'Không',
         'Theo dữ liệu', 'Chỉ hiển thị, không sửa được từ màn này.'),
        ('Tên hàng', 'Textbox', 'Read-only', '–', 'Không', 'Theo dữ liệu',
         'Tên hàng hóa / thiết bị tương ứng.'),
        ('Khách hàng', 'Textbox', 'Read-only', '–', 'Không', 'Theo dữ liệu',
         'Đơn vị đang sở hữu thiết bị.'),
        ('Trạng thái', 'Badge', 'Read-only', 'Danh sách', 'Không', 'Theo dữ liệu',
         'Tình trạng hiện tại của serial.'),
    ],
    tc_sheet='Serial thiet bi lam dich vu',
    tc_module='CSKH - Danh muc',
    tc_mucdich='Tra cuu danh muc Serial thiet bi lam dich vu. Man hinh CHI DOC: cho phep tim '
               'kiem, loc, tuy chinh hien thi va xuat Excel. Moi thao tac them, sua, doi va xoa '
               'serial nam o man Quan ly khach hang, tab Trang thiet bi.',
    tc_caudata='- Danh muc phang, khong phan cap cha con.\n'
               '- Moi dong la mot serial gan voi mot hang hoa va mot khach hang.\n'
               '- Danh muc rat lon, hon hai muoi nghin dong, nen luon phai phan trang.',
    tc_dedupe='- Moi serial chi hien MOT dong.\n'
              '- Man nay khong tao du lieu nen khong co phep kiem tra trung khi luu.',
    tc_nguon='Du lieu dung chung voi tab Trang thiet bi cua man Quan ly khach hang. Thay doi '
             'ben man do se phan anh ngay o man nay.',
    tc_luuy=[
        'Cac bay de sai nhat cua man nay, QA doc truoc khi test:',
        '- Day la man CHI DOC. Khong co nut Tao moi, Sua, Xoa, Khoa — khong phai bi an do thieu quyen ma la man khong co cac chuc nang do.',
        '- Moi thao tac them, sua, doi va xoa serial nam o man Quan ly khach hang, tab Trang thiet bi.',
        '- Man hinh chi co MOT quyen va la quyen tra cuu.',
        '- Danh muc hon hai muoi nghin dong nen phai kiem thu ky phan trang va thoi gian cho.',
        '- Tep Excel duoc dung ngay tren trinh duyet theo tung lo, nen voi danh muc day du thoi gian xuat co the lau; day la hanh vi dung theo thiet ke.',
        '- Cau hinh o loc va cot hien thi luu rieng theo tung nguoi dung.',
    ],
    hdsd_gioithieu=[
        'Danh mục serial thiết bị làm dịch vụ là nơi tra cứu số hiệu riêng của từng thiết bị đang được bảo hành hoặc bảo dưỡng, kèm hàng hóa tương ứng và khách hàng đang sở hữu.',
        'Đây là màn hình CHỈ ĐỌC: bạn tra cứu, lọc và xuất Excel được, nhưng không thêm, sửa hay xóa được serial từ màn này.',
        'Muốn thay đổi serial, hãy vào màn Quản lý khách hàng rồi mở tab Trang thiết bị của khách hàng tương ứng.',
        'Danh mục có hơn hai mươi nghìn dòng nên hãy dùng bộ lọc để thu hẹp trước khi tra cứu hoặc xuất Excel.',
    ],
    hdsd_loi=[
    ],
    hdsd_faq=[
        ['Vì sao không có nút Tạo mới, Sửa, Xóa', 'Đây là màn tra cứu, cố ý không có các thao tác ghi. Việc thêm và sửa serial nằm ở màn Quản lý khách hàng, tab Trang thiết bị.'],
        ['Xuất Excel toàn bộ danh mục mất khá lâu', 'Danh mục có hơn hai mươi nghìn dòng nên tệp được dựng theo từng lô, cần thời gian. Hãy lọc bớt trước khi xuất nếu bạn chỉ cần một phần dữ liệu.'],
        ['Tôi vừa sửa serial bên màn khách hàng mà ở đây chưa thấy đổi', 'Hãy bấm Làm mới hoặc tải lại trang. Hai màn dùng chung một nguồn dữ liệu nên thay đổi sẽ hiện ngay sau khi nạp lại.'],
        ['Ô lọc tôi cần không có trên màn hình', 'Bấm nút Cài đặt bộ lọc để bật thêm ô lọc và sắp lại thứ tự theo ý bạn.'],
    ],
    hdsd_xuat_them=[
        'Danh mục rất lớn nên tệp được dựng theo từng lô dữ liệu, quá trình có thể mất một lúc. Đừng đóng trang trong khi đang xuất.',
    ],
    shots=dict(danhsach='sr_01_danhsach.png', boloc='sr_02_boloc.png',
               caidat_boloc='sr_03_caidat_boloc.png', xuat='sr_04_xuat_excel.png',
               cot='sr_05_cauhinh_cot.png'),
    funcs=['list', 'filter', 'fcfg', 'export', 'columns'],
    quy_tac=[
        ('Màn hình chỉ đọc, không có thao tác ghi', [
            'Màn này chỉ tra cứu và kết xuất; không có nút Tạo mới, Sửa, Xóa, Khóa.',
            'Việc thêm, sửa, đổi và xóa serial được thực hiện ở màn Quản lý khách hàng, tab '
            'Trang thiết bị.',
            'Phía máy chủ cũng chỉ mở đường tra cứu, không có đường ghi dữ liệu cho màn này.',
        ]),
        ('Một quyền duy nhất và là quyền tra cứu', [
            'Màn hình dùng đúng một quyền “Xem danh mục serial thiết bị làm dịch vụ”.',
            'Không có quyền này thì mục menu không hiển thị và truy cập thẳng đường dẫn bị chặn.',
            'Vì không có thao tác ghi nên không cần quyền quản lý riêng.',
        ]),
        ('Xuất Excel dựng ngay trên trình duyệt', [
            'Danh mục có hơn hai mươi nghìn dòng nên tệp Excel được dựng trên máy người dùng, '
            'lấy dữ liệu theo từng lô thay vì tạo tệp ở máy chủ.',
            'Cách này tránh được tình trạng quá hạn chờ khi kết xuất toàn bộ danh mục.',
            'Tệp xuất ra áp đúng bộ lọc và bộ trường mà người dùng đã chọn.',
        ]),
        ('Bộ lọc và bộ cột lưu riêng theo từng người dùng', [
            'Cấu hình ô lọc hiển thị và cột hiển thị được lưu riêng cho từng người và từng '
            'màn hình.',
            'Lần vào sau, màn hình dựng lại đúng cấu hình đã lưu.',
            'Nút Khôi phục mặc định đưa bộ lọc về trạng thái gốc của màn hình.',
        ]),
        ('Danh mục dùng chung dữ liệu với màn Quản lý khách hàng', [
            'Serial hiển thị ở đây là cùng một nguồn dữ liệu với tab Trang thiết bị của khách hàng.',
            'Thay đổi thực hiện bên màn Quản lý khách hàng sẽ phản ánh ngay ở màn này.',
        ]),
    ],
)

SCREENS = [SERIAL]
