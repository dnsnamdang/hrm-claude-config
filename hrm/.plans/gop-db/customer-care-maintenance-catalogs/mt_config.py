# -*- coding: utf-8 -*-
"""Cau hinh 2 man danh muc bao duong (phan he CSKH) — dung chung cho gen_srs / gen_testcase /
gen_hdsd.

Doc code 18/08/2026:
  BE  Modules/CustomerCare/Routes/api.php (24-90) — moi man 2 quyen: "Quan ly ..." va "Xem ..."
      Modules/CustomerCare/Http/Requests/Level/LevelRequest.php
      Modules/CustomerCare/Http/Requests/NoteMaintenance/NoteMaintenanceRequest.php
      Modules/CustomerCare/Entities/Level/Level.php            -> USED_BY 6 bang, isCanDelete()
      Modules/CustomerCare/Entities/NoteMaintenance/...php     -> USED_BY 1 bang
      app/Services/CatalogHistoryService.php                   -> nhan cot ghi lich su
  FE  hrm-client/pages/customer-care/{levels,note-maintenances}/index.vue
  Anh that: mt_shots/ (cong dev hrm-crm.eteksofts.com, 18/08/2026)
"""

HOST = 'http://hrm-crm.eteksofts.com'

# ============================================================ CẤP DỊCH VỤ BẢO DƯỠNG
LEVEL = dict(
    key='lv',
    ten='Cấp dịch vụ bảo dưỡng',
    doi_tuong='cấp dịch vụ',
    route='/customer-care/levels',
    host=HOST,
    menu='Phân hệ CSKH → Danh mục → Cấp dịch vụ bảo dưỡng',
    quyen_quan_ly='Quản lý cấp dịch vụ bảo dưỡng',
    quyen_xem='Xem cấp dịch vụ bảo dưỡng',
    tacdung_ql='Mở màn hình và thực hiện đầy đủ Thêm mới, Chỉnh sửa, Xóa. Thiếu quyền này thì '
               'các nút thao tác không hiển thị.',
    tacdung_xem='Chỉ mở được màn hình để tra cứu, xuất Excel và xem lịch sử. Không thấy nút '
                'Tạo mới, Sửa, Xóa.',
    ghichu_quyen='Màn hình tách riêng quyền quản lý và quyền xem. Người chỉ có quyền xem vẫn '
                 'vào được màn hình và tra cứu bình thường nhưng mọi nút ghi dữ liệu đều bị ẩn. '
                 'Người không có quyền nào thì mục menu không hiển thị và truy cập thẳng đường '
                 'dẫn cũng bị chặn.',
    co_trangthai=False,
    truong_trung='Tên cấp',
    loi_trung='Tên cấp đã tồn tại',
    tb_them='Thêm mới cấp dịch vụ thành công',
    tb_sua='Cập nhật cấp dịch vụ thành công',
    tb_xoa='Xóa cấp dịch vụ thành công',
    dieu_kien_xoa='cấp dịch vụ chưa được dùng ở bất kỳ nghiệp vụ nào',
    dieu_kien_an_xoa='cấp dịch vụ đang được sử dụng',
    cauhoi_xoa="Bạn có chắc muốn xóa cấp dịch vụ 'Cấp 2 (24T/6000H)'?",
    muc_dich=[
        'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý Cấp dịch vụ bảo dưỡng.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ điều kiện được phép xóa: chỉ cấp dịch vụ chưa được dùng ở gói bảo dưỡng, báo giá '
        'dịch vụ, hợp đồng dịch vụ, phiếu phân công hay phiếu nhập kết quả mới hiện nút Xóa.',
        'Ghi nhận khác biệt có chủ đích so với màn cũ: bản cũ chỉ kiểm tra một nơi sử dụng nên '
        'vẫn xóa được cấp đang dùng, bản này kiểm tra đủ sáu nơi.',
    ],
    thuat_ngu=[
        ('Cấp dịch vụ bảo dưỡng',
         'Mức độ của một lần bảo dưỡng, thể hiện phạm vi công việc và chu kỳ thực hiện. '
         'Ví dụ: Cấp 1 (6T), Cấp 2 (12T).'),
        ('Gói bảo dưỡng',
         'Gói dịch vụ bán cho khách hàng, gồm nhiều cấp dịch vụ theo từng mốc thời gian.'),
        ('Báo giá dịch vụ', 'Chứng từ chào giá dịch vụ bảo dưỡng gửi khách hàng.'),
        ('Hợp đồng dịch vụ', 'Hợp đồng bảo dưỡng đã ký với khách hàng.'),
        ('Phiếu phân công công việc', 'Chứng từ giao việc bảo dưỡng cho kỹ thuật viên.'),
        ('Phiếu nhập kết quả', 'Chứng từ ghi nhận kết quả sau khi thực hiện bảo dưỡng.'),
        ('Đang được sử dụng',
         'Cấp dịch vụ đã xuất hiện ở ít nhất một trong sáu nghiệp vụ nêu trên; khi đó không '
         'được phép xóa.'),
    ],
    cot=[
        ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
        ('Tên cấp', 'Tên đầy đủ của cấp dịch vụ. Luôn hiển thị, sắp xếp được, bấm vào để mở '
                    'cửa sổ xem.'),
        ('Người tạo', 'Họ tên người đã thêm bản ghi.'),
        ('Ngày tạo', 'Ngày giờ thêm bản ghi, sắp xếp được.'),
        ('Người cập nhật', 'Họ tên người sửa gần nhất. Mặc định ẩn.'),
        ('Ngày cập nhật', 'Ngày giờ sửa gần nhất, sắp xếp được. Mặc định ẩn.'),
        ('Hành động', 'Nút Sửa, Xóa và Lịch sử. Nút Xóa chỉ hiện khi cấp dịch vụ chưa được '
                      'dùng ở đâu.'),
    ],
    nut_thanh_cong_cu=[
        ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện với người có quyền “Quản lý cấp dịch vụ bảo dưỡng”.'),
        ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn trường cần xuất.'),
        ('Nút Tùy chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn cột hiển thị trên bảng.'),
    ],
    loc=[
        ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
         'Tìm theo tên cấp dịch vụ. Không phân biệt chữ hoa chữ thường.'),
    ],
    truong=[
        ('Tên cấp', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Tên của cấp dịch vụ, KHÔNG được trùng với cấp đã có. Bỏ trống báo '
         '“Bắt buộc phải nhập”; trùng báo “Tên cấp đã tồn tại”. Khoảng trắng thừa ở hai đầu '
         'được tự cắt bỏ trước khi kiểm tra.'),
    ],
    tc_sheet='Cap dich vu bao duong',
    tc_module='CSKH - Danh muc',
    tc_mucdich='Quan ly danh muc Cap dich vu bao duong dung cho nghiep vu bao duong. Man hinh '
               'cho phep tra cuu, tim kiem, them moi, chinh sua, xoa, xuat Excel va xem lich su '
               'thay doi. Du lieu cua man nay duoc chon khi lap goi bao duong, bao gia dich vu '
               'va hop dong dich vu.',
    tc_caudata=(
        '- Danh muc phang, khong phan cap cha con.\n'
        '- Moi cap dich vu la mot ban ghi doc lap, chi co dung MOT o nhap la Ten cap.\n'
        '- Ban ghi duoc tham chieu tu sau nghiep vu khac nhau; day la can cu quyet dinh co '
        'xoa duoc hay khong.'),
    tc_dedupe=(
        '- Moi cap dich vu chi hien MOT dong.\n'
        '- Ten cap la duy nhat toan he thong, trung se bi chan khi luu voi thong bao '
        '"Ten cap da ton tai".\n'
        '- Khi sua, ban ghi dang sua duoc loai khoi phep kiem tra trung.'),
    tc_nguon='Du lieu lay tu danh muc Cap dich vu bao duong. Cot Nguoi tao va Nguoi cap nhat '
             'lay ho ten nhan vien thuc hien thao tac.',
    tc_luuy=[
        'Cac bay de sai nhat cua man nay, QA doc truoc khi test:',
        '- Man hinh dung HAI quyen tach roi. Nguoi chi co quyen xem VAN VAO DUOC man hinh va tra cuu binh thuong, chi khong thay cac nut ghi.',
        '- Man nay chi co DUNG MOT o nhap la Ten cap. Khong co ma, khong co ghi chu, khong co trang thai.',
        '- Man nay KHONG co bo loc nang cao, chi co o tim kiem nhanh.',
        '- Man nay KHONG co trang thai Khoa nen khong co nut Khoa / Mo khoa.',
        '- Nut Xoa chi hien voi cap dich vu chua duoc dung o dau. He thong kiem du SAU noi: goi bao duong, cap bao duong cua goi, bao gia dich vu, hop dong dich vu, phieu phan cong va phieu nhap ket qua.',
        '- Nut khong dung duoc phai AN HAN, khong phai hien nut xam.',
    ],
    hdsd_gioithieu=[
        'Cấp dịch vụ bảo dưỡng là nơi khai báo các mức bảo dưỡng dùng cho nghiệp vụ dịch vụ. Mỗi cấp thể hiện phạm vi công việc và chu kỳ thực hiện, ví dụ Cấp 1 (6T) là bảo dưỡng cấp 1 sau mỗi sáu tháng.',
        'Dữ liệu của màn này được chọn khi lập gói bảo dưỡng, báo giá dịch vụ, hợp đồng dịch vụ, phiếu phân công công việc và phiếu nhập kết quả. Vì vậy mỗi thay đổi ở đây đều ảnh hưởng tới các nghiệp vụ phía sau.',
        'Màn hình rất gọn: mỗi cấp dịch vụ chỉ có đúng một thông tin là Tên cấp.',
    ],
    hdsd_loi=[
        ['Bắt buộc phải nhập', 'Bạn chưa nhập Tên cấp. Hãy nhập tên rồi lưu lại.'],
        ['Tên cấp đã tồn tại', 'Đã có cấp dịch vụ khác mang đúng tên này. Hãy đặt tên khác, hoặc tìm lại trong danh sách xem cấp đó đã có sẵn chưa. Hệ thống tự cắt khoảng trắng thừa ở hai đầu trước khi so sánh, nên thêm dấu cách cũng không tránh được báo trùng.'],
    ],
    hdsd_faq=[
        ['Tôi không thấy nút Tạo mới', 'Tài khoản của bạn chỉ có quyền xem. Liên hệ quản trị viên để được cấp quyền quản lý cấp dịch vụ bảo dưỡng.'],
        ['Dòng này không có nút Xóa', 'Cấp dịch vụ đó đang được dùng ở gói bảo dưỡng, báo giá dịch vụ, hợp đồng dịch vụ, phiếu phân công hoặc phiếu nhập kết quả. Phải gỡ khỏi các nghiệp vụ đó trước mới xóa được.'],
        ['Màn này có khóa bản ghi được không', 'Không. Màn này không có trạng thái Khóa. Cấp dịch vụ chỉ có hai khả năng: còn trong danh mục hoặc đã bị xóa hẳn.'],
        ['Tôi không tìm thấy bộ lọc nâng cao', 'Màn này chỉ có ô tìm kiếm nhanh theo tên cấp. Đây là thiết kế đúng vì danh mục chỉ có một thông tin để lọc.'],
        ['Cửa sổ Lịch sử báo chưa có lịch sử nào', 'Bản ghi đó chưa từng bị sửa kể từ khi hệ thống bắt đầu ghi nhật ký. Đây là bình thường, không phải lỗi.'],
    ],
    shots=dict(danhsach='lv_01_danhsach.png', taomoi='lv_02_taomoi.png',
               validate='lv_03_validate.png', xem='lv_04_xem.png', sua='lv_04_xem.png',
               lichsu='lv_05_lichsu.png', xoa='lv_06_xacnhan_xoa.png',
               cot='lv_07_cauhinh_cot.png', xuat='lv_08_xuat_excel.png'),
    funcs=[
        'list', 'filter', ('view', {'nhan': 'Xem chi tiết cấp dịch vụ'}),
        'create', 'edit', 'delete', 'history', 'export', 'columns',
    ],
    quy_tac=[
        ('Tách riêng quyền xem và quyền quản lý', [
            'Màn hình dùng hai quyền: “Quản lý cấp dịch vụ bảo dưỡng” cho mọi thao tác ghi và '
            '“Xem cấp dịch vụ bảo dưỡng” cho tra cứu.',
            'Người chỉ có quyền xem vẫn mở được màn hình, xuất Excel và xem lịch sử, nhưng '
            'không thấy nút Tạo mới, Sửa và Xóa.',
            'Mọi thao tác ghi đều kiểm tra lại quyền ở tầng máy chủ; gọi thẳng chức năng mà bỏ '
            'qua giao diện vẫn bị từ chối.',
        ]),
        ('Tên cấp là duy nhất trên toàn danh mục', [
            'Không cho phép hai cấp dịch vụ trùng tên nhau.',
            'Khi sửa, bản ghi đang sửa được loại khỏi phép so trùng nên giữ nguyên tên cũ '
            'không bị báo lỗi.',
            'Khoảng trắng thừa ở hai đầu được cắt bỏ trước khi so trùng, nên “Cấp 1” và '
            '“ Cấp 1 ” bị coi là trùng nhau.',
        ]),
        ('Chỉ xóa được cấp dịch vụ chưa dùng ở đâu', [
            'Hệ thống kiểm tra đủ sáu nơi: gói bảo dưỡng, cấp bảo dưỡng của gói dịch vụ, báo '
            'giá dịch vụ, hợp đồng dịch vụ, phiếu phân công công việc và phiếu nhập kết quả.',
            'Chỉ cần xuất hiện ở một nơi là nút Xóa bị ẨN HẲN, không hiện nút xám.',
            'Thông báo từ chối nêu tối đa ba nghiệp vụ đang dùng để người dùng biết phải xử lý '
            'ở đâu trước.',
            'Đây là điểm khác có chủ đích so với màn cũ: bản cũ chỉ kiểm tra gói bảo dưỡng nên '
            'vẫn xóa được cấp đang nằm trong hợp đồng, làm mất dữ liệu tham chiếu.',
        ]),
        ('Danh mục không có trạng thái Khóa', [
            'Cấp dịch vụ chỉ có hai khả năng: còn trong danh mục hoặc đã bị xóa hẳn.',
            'Không có thao tác Khóa / Mở khóa như các danh mục Tài chính.',
        ]),
        ('Mọi thay đổi đều được ghi lịch sử', [
            'Thêm mới, sửa và xóa đều ghi lại một dòng lịch sử kèm người thực hiện và thời điểm.',
            'Với thao tác sửa, hệ thống ghi từng trường đã đổi kèm giá trị trước và sau.',
            'Lịch sử sắp xếp mới nhất lên trước và không sửa hay xóa được.',
        ]),
        ('Người tạo và người cập nhật lấy theo nhân viên đăng nhập', [
            'Hai cột Người tạo và Người cập nhật hiển thị họ tên nhân viên thực hiện thao tác.',
            'Bản ghi cũ chuyển từ hệ thống trước có thể để trống hai cột này.',
        ]),
    ],
)

# ============================================================ GHI CHÚ KIỂM TRA BẢO DƯỠNG
NOTE = dict(
    key='nm',
    ten='Danh mục ghi chú kiểm tra bảo dưỡng',
    doi_tuong='ghi chú kiểm tra',
    route='/customer-care/note-maintenances',
    host=HOST,
    menu='Phân hệ CSKH → Danh mục → Danh mục ghi chú kiểm tra bảo dưỡng',
    quyen_quan_ly='Quản lý ghi chú kiểm tra bảo dưỡng',
    quyen_xem='Xem ghi chú kiểm tra bảo dưỡng',
    tacdung_ql='Mở màn hình và thực hiện đầy đủ Thêm mới, Chỉnh sửa, Xóa. Thiếu quyền này thì '
               'các nút thao tác không hiển thị.',
    tacdung_xem='Chỉ mở được màn hình để tra cứu, xuất Excel và xem lịch sử. Không thấy nút '
                'Tạo mới, Sửa, Xóa.',
    ghichu_quyen='Màn hình tách riêng quyền quản lý và quyền xem. Người chỉ có quyền xem vẫn '
                 'vào được màn hình và tra cứu bình thường nhưng mọi nút ghi dữ liệu đều bị ẩn. '
                 'Người không có quyền nào thì mục menu không hiển thị và truy cập thẳng đường '
                 'dẫn cũng bị chặn.',
    co_trangthai=False,
    truong_trung='Hạng mục',
    loi_trung='Hạng mục đã tồn tại',
    loi_khac=['– Ký hiệu đã tồn tại → hiển thị “Ký hiệu đã tồn tại”.'],
    tb_them='Thêm mới ghi chú thành công',
    tb_sua='Cập nhật ghi chú thành công',
    tb_xoa='Xóa ghi chú thành công',
    dieu_kien_xoa='ghi chú chưa được gán vào cấp bảo dưỡng của gói dịch vụ nào',
    dieu_kien_an_xoa='ghi chú đang được gói dịch vụ sử dụng',
    cauhoi_xoa="Bạn có chắc muốn xóa ghi chú 'Kiểm tra ngoại quan không tháo lắp'?",
    muc_dich=[
        'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý Danh mục ghi chú kiểm tra '
        'bảo dưỡng.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ hai ràng buộc trùng độc lập nhau: trùng Hạng mục và trùng Ký hiệu.',
        'Ghi nhận khác biệt có chủ đích so với màn cũ: bản cũ xóa thẳng không kiểm tra gì, bản '
        'này chặn xóa khi ghi chú đang được gói dịch vụ sử dụng.',
    ],
    thuat_ngu=[
        ('Ghi chú kiểm tra bảo dưỡng',
         'Một hạng mục công việc kiểm tra được thực hiện trong quá trình bảo dưỡng thiết bị. '
         'Ví dụ: kiểm tra ngoại quan không tháo lắp, đo kiểm bằng dụng cụ chuyên dùng.'),
        ('Hạng mục', 'Tên đầy đủ của công việc kiểm tra, là trường chính của danh mục.'),
        ('Ký hiệu',
         'Mã viết tắt của hạng mục, dùng để ghi gọn trên phiếu và mẫu in. Ví dụ: KTBM, DK, CC. '
         'Hệ thống tự chuyển thành chữ in hoa khi lưu.'),
        ('Cấp bảo dưỡng của gói dịch vụ',
         'Bảng liên kết giữa gói bảo dưỡng và các ghi chú kiểm tra cần thực hiện ở từng cấp.'),
        ('Đang được sử dụng',
         'Ghi chú đã được gán vào ít nhất một cấp bảo dưỡng của gói dịch vụ; khi đó không được '
         'phép xóa.'),
    ],
    cot=[
        ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
        ('Hạng mục', 'Tên công việc kiểm tra. Luôn hiển thị, sắp xếp được, bấm vào để mở cửa '
                     'sổ xem.'),
        ('Ký hiệu', 'Mã viết tắt của hạng mục. Mặc định ẩn.'),
        ('Mô tả', 'Diễn giải thêm về hạng mục. Mặc định ẩn.'),
        ('Người tạo', 'Họ tên người đã thêm bản ghi.'),
        ('Ngày tạo', 'Ngày giờ thêm bản ghi, sắp xếp được.'),
        ('Người cập nhật', 'Họ tên người sửa gần nhất. Mặc định ẩn.'),
        ('Ngày cập nhật', 'Ngày giờ sửa gần nhất, sắp xếp được. Mặc định ẩn.'),
        ('Hành động', 'Nút Sửa, Xóa và Lịch sử. Nút Xóa chỉ hiện khi ghi chú chưa được gói '
                      'dịch vụ nào dùng.'),
    ],
    nut_thanh_cong_cu=[
        ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện với người có quyền “Quản lý ghi chú kiểm tra bảo dưỡng”.'),
        ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn trường cần xuất.'),
        ('Nút Tùy chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn cột hiển thị trên bảng.'),
    ],
    loc=[
        ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
         'Tìm đồng thời theo Hạng mục và Ký hiệu. Không phân biệt chữ hoa chữ thường.'),
    ],
    truong=[
        ('Hạng mục', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Tên công việc kiểm tra, KHÔNG được trùng. Bỏ trống báo “Bắt buộc phải nhập”; trùng '
         'báo “Hạng mục đã tồn tại”.'),
        ('Ký hiệu', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Mã viết tắt, KHÔNG được trùng và được tự chuyển thành CHỮ IN HOA khi lưu. Bỏ trống '
         'báo “Bắt buộc phải nhập”; trùng báo “Ký hiệu đã tồn tại”.'),
        ('Mô tả', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Diễn giải thêm, không bắt buộc và không kiểm tra trùng.'),
    ],
    tc_sheet='Ghi chu kiem tra bao duong',
    tc_module='CSKH - Danh muc',
    tc_mucdich='Quan ly danh muc Ghi chu kiem tra bao duong. Man hinh cho phep tra cuu, tim '
               'kiem, them moi, chinh sua, xoa, xuat Excel va xem lich su thay doi. Du lieu '
               'cua man nay duoc gan vao tung cap bao duong cua goi dich vu.',
    tc_caudata='- Danh muc phang, khong phan cap cha con.\n'
               '- Moi ghi chu gom ba o nhap: Hang muc, Ky hieu va Mo ta.\n'
               '- Ban ghi duoc tham chieu tu cap bao duong cua goi dich vu; day la can cu quyet '
               'dinh co xoa duoc hay khong.',
    tc_dedupe='- Moi ghi chu chi hien MOT dong.\n'
              '- Hang muc va Ky hieu deu la duy nhat, kiem tra TACH ROI nhau.\n'
              '- Khi sua, ban ghi dang sua duoc loai khoi ca hai phep kiem tra trung.',
    tc_nguon='Du lieu lay tu danh muc Ghi chu kiem tra bao duong. Cot Nguoi tao va Nguoi cap '
             'nhat lay ho ten nhan vien thuc hien thao tac.',
    tc_luuy=[
        'Cac bay de sai nhat cua man nay, QA doc truoc khi test:',
        '- Man hinh dung HAI quyen tach roi. Nguoi chi co quyen xem VAN VAO DUOC man hinh.',
        '- Rang buoc trung ap cho CA Hang muc LAN Ky hieu, kiem tra tach roi nhau. Hai ban ghi khac hang muc nhung trung ky hieu van bi chan.',
        '- Ky hieu duoc tu chuyen thanh CHU IN HOA khi luu, nen "ktbm" va "KTBM" bi coi la trung.',
        '- O Mo ta KHONG bat buoc va KHONG kiem tra trung.',
        '- Man nay KHONG co bo loc nang cao va KHONG co trang thai Khoa.',
        '- Nut Xoa chi hien khi ghi chu chua duoc gan vao cap bao duong cua goi dich vu nao.',
        '- Nut khong dung duoc phai AN HAN, khong phai hien nut xam.',
    ],
    hdsd_gioithieu=[
        'Danh mục ghi chú kiểm tra bảo dưỡng là nơi khai báo các hạng mục công việc cần thực hiện khi kiểm tra, bảo dưỡng thiết bị. Ví dụ: kiểm tra ngoại quan không tháo lắp, đo kiểm bằng dụng cụ chuyên dùng, vệ sinh, bôi trơn.',
        'Mỗi hạng mục có thêm một Ký hiệu viết tắt để ghi gọn trên phiếu và mẫu in.',
        'Dữ liệu của màn này được gán vào từng cấp bảo dưỡng của gói dịch vụ, nên hạng mục đã được gán thì không xóa được nữa.',
    ],
    hdsd_loi=[
        ['Bắt buộc phải nhập', 'Bạn chưa nhập Hạng mục hoặc Ký hiệu. Cả hai ô này đều bắt buộc.'],
        ['Hạng mục đã tồn tại', 'Đã có ghi chú khác mang đúng tên hạng mục này. Hãy đặt tên khác hoặc tìm lại trong danh sách.'],
        ['Ký hiệu đã tồn tại', 'Đã có ghi chú khác dùng đúng ký hiệu này. Hệ thống tự chuyển ký hiệu thành chữ in hoa, nên nhập ktbm hay KTBM đều bị coi là trùng với nhau.'],
    ],
    hdsd_faq=[
        ['Ký hiệu tôi nhập chữ thường mà lưu xong lại thành chữ hoa', 'Đúng theo thiết kế. Hệ thống luôn chuyển ký hiệu thành chữ in hoa để toàn danh mục thống nhất một kiểu.'],
        ['Tôi đổi Hạng mục nhưng vẫn báo Ký hiệu đã tồn tại', 'Hai ràng buộc trùng này kiểm tra tách rời nhau. Đổi hạng mục không giúp gì cho ký hiệu, bạn phải đổi cả ký hiệu.'],
        ['Ô Mô tả có bắt buộc không', 'Không. Mô tả để trống vẫn lưu được, và hệ thống không kiểm tra trùng ô này.'],
        ['Dòng này không có nút Xóa', 'Ghi chú đó đã được gán vào cấp bảo dưỡng của một gói dịch vụ. Phải gỡ khỏi gói đó trước mới xóa được.'],
        ['Tôi không thấy nút Tạo mới và nút Sửa', 'Tài khoản của bạn chỉ có quyền xem ghi chú kiểm tra bảo dưỡng. Liên hệ quản trị viên để được cấp thêm quyền quản lý.'],
    ],
    shots=dict(danhsach='nm_01_danhsach.png', taomoi='nm_02_taomoi.png',
               validate='nm_03_validate.png', xoa='nm_04_xacnhan_xoa.png',
               xem='nm_05_xem.png', sua='nm_05_xem.png', lichsu='nm_06_lichsu.png',
               xuat='nm_07_xuat_excel.png', cot='nm_08_cauhinh_cot.png'),
    funcs=[
        'list', 'filter', ('view', {'nhan': 'Xem chi tiết ghi chú kiểm tra'}),
        'create', 'edit', 'delete', 'history', 'export', 'columns',
    ],
    quy_tac=[
        ('Tách riêng quyền xem và quyền quản lý', [
            'Màn hình dùng hai quyền: “Quản lý ghi chú kiểm tra bảo dưỡng” cho mọi thao tác ghi '
            'và “Xem ghi chú kiểm tra bảo dưỡng” cho tra cứu.',
            'Người chỉ có quyền xem vẫn mở được màn hình, xuất Excel và xem lịch sử, nhưng '
            'không thấy nút Tạo mới, Sửa và Xóa.',
            'Mọi thao tác ghi đều kiểm tra lại quyền ở tầng máy chủ.',
        ]),
        ('Hai ràng buộc trùng độc lập nhau', [
            'Hạng mục phải là duy nhất trên toàn danh mục.',
            'Ký hiệu cũng phải là duy nhất, kiểm tra tách rời với Hạng mục.',
            'Hai bản ghi có Hạng mục khác nhau nhưng Ký hiệu giống nhau vẫn bị chặn, và ngược lại.',
            'Khi sửa, bản ghi đang sửa được loại khỏi cả hai phép so trùng.',
        ]),
        ('Ký hiệu luôn được lưu bằng chữ in hoa', [
            'Hệ thống tự chuyển ký hiệu sang chữ in hoa trước khi kiểm tra trùng và trước khi lưu.',
            'Nhập “ktbm” hay “KTBM” đều cho ra cùng một giá trị, nên hai cách nhập này bị coi '
            'là trùng nhau.',
        ]),
        ('Chỉ xóa được ghi chú chưa gán vào gói dịch vụ', [
            'Hệ thống kiểm tra bảng cấp bảo dưỡng của gói dịch vụ trước khi cho xóa.',
            'Ghi chú đang được dùng thì nút Xóa bị ẨN HẲN, không hiện nút xám.',
            'Đây là điểm khác có chủ đích so với màn cũ: bản cũ xóa thẳng không kiểm tra gì nên '
            'làm mồ côi dữ liệu của gói dịch vụ.',
        ]),
        ('Danh mục không có trạng thái Khóa', [
            'Ghi chú chỉ có hai khả năng: còn trong danh mục hoặc đã bị xóa hẳn.',
            'Không có thao tác Khóa / Mở khóa.',
        ]),
        ('Mọi thay đổi đều được ghi lịch sử', [
            'Thêm mới, sửa và xóa đều ghi lại một dòng lịch sử kèm người thực hiện và thời điểm.',
            'Ba trường Hạng mục, Ký hiệu và Mô tả đều được theo dõi thay đổi.',
            'Lịch sử sắp xếp mới nhất lên trước và không sửa hay xóa được.',
        ]),
    ],
)

SCREENS = [LEVEL, NOTE]
