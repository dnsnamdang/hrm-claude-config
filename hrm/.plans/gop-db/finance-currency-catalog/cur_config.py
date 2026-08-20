# -*- coding: utf-8 -*-
"""Cau hinh man 'Danh muc tien te' (/finance/currencies).

Doc code 18/08/2026:
  BE  Modules/Finance/Routes/api.php (95-122) — 2 quyen: "Quan ly danh muc tien te" va
      "Xem danh muc tien te"; route update/delete gan them middleware `recordNotLocked`.
      Modules/Finance/Http/Requests/Currency/CurrencyRequest.php
        code / name: required|max:255|unique;  exchange_rate: required|numeric|gt:0|max:999999.99
        `prepareForValidation` doi ty gia tu dinh dang VN ("999.999,99") sang dang chuan.
      Modules/Finance/Entities/Currency/Currency.php -> STATUSES, isLocked(), USED_BY (~20 bang)
  FE  hrm-client/pages/finance/currencies/index.vue
  Anh that: cur_shots/ (cong dev hrm-crm.eteksofts.com, 18/08/2026)
"""

HOST = 'http://hrm-crm.eteksofts.com'

CURRENCY = dict(
    key='tt',
    ten='Danh mục tiền tệ',
    doi_tuong='tiền tệ',
    route='/finance/currencies',
    host=HOST,
    menu='Phân hệ Tài chính → Danh mục → Danh mục tiền tệ',
    quyen_quan_ly='Quản lý danh mục tiền tệ',
    quyen_xem='Xem danh mục tiền tệ',
    tacdung_ql='Mở màn hình và thực hiện đầy đủ Thêm mới, Chỉnh sửa, Xóa và Khóa / Mở khóa. '
               'Thiếu quyền này thì các nút thao tác không hiển thị.',
    tacdung_xem='Chỉ mở được màn hình để tra cứu, xuất Excel và xem lịch sử. Không thấy nút '
                'Tạo mới, Sửa, Xóa và Khóa.',
    ghichu_quyen='Màn hình tách riêng quyền quản lý và quyền xem. Người chỉ có quyền xem vẫn '
                 'vào được màn hình và tra cứu bình thường nhưng mọi nút ghi dữ liệu đều bị ẩn. '
                 'Người không có quyền nào thì mục menu không hiển thị và truy cập thẳng đường '
                 'dẫn cũng bị chặn.',
    co_trangthai=True,
    truong_trung='Mã tiền tệ',
    loi_trung='Mã tiền tệ đã tồn tại',
    loi_khac=[
        '– Tên tiền tệ trùng với bản ghi khác → hiển thị “Tên tiền tệ đã tồn tại”.',
        '– Tỷ giá nhập chữ → hiển thị “Phải là số”.',
        '– Tỷ giá bằng 0 hoặc số âm → hiển thị “Phải lớn hơn 0”.',
        '– Tỷ giá vượt 999.999,99 → hiển thị “Tối đa 999999.99”.',
    ],
    tb_them='Thêm mới tiền tệ thành công',
    tb_sua='Cập nhật tiền tệ thành công',
    tb_xoa='Xóa tiền tệ thành công',
    dieu_kien_xoa='tiền tệ chưa được dùng ở bất kỳ chứng từ nào',
    dieu_kien_an_xoa='tiền tệ đang được chứng từ sử dụng',
    cauhoi_xoa="Bạn có chắc muốn xóa tiền tệ 'CNY'?",
    cauhoi_khoa="Bạn có chắc muốn khóa tiền tệ 'VietNamDong'?",
    muc_dich=[
        'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý Danh mục tiền tệ.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ cách nhập tỷ giá theo định dạng số của Việt Nam và các giới hạn giá trị.',
        'Làm rõ điều kiện được phép xóa: chỉ tiền tệ chưa xuất hiện ở chứng từ nào mới hiện '
        'nút Xóa; danh sách nơi sử dụng trải rộng khoảng hai mươi loại chứng từ.',
    ],
    thuat_ngu=[
        ('Tiền tệ',
         'Đơn vị tiền dùng trong các chứng từ mua bán, hợp đồng và hóa đơn. Ví dụ: VNĐ, USD, EUR.'),
        ('Mã tiền tệ',
         'Ký hiệu viết tắt của loại tiền, duy nhất trên toàn danh mục và được tự chuyển thành '
         'chữ in hoa khi lưu.'),
        ('Tên gọi khác',
         'Tên gọi thay thế của loại tiền, không bắt buộc và không kiểm tra trùng.'),
        ('Tỷ giá (VNĐ)',
         'Số tiền Việt Nam đồng tương ứng với một đơn vị của loại tiền này. Phải lớn hơn 0 và '
         'không vượt quá 999.999,99.'),
        ('Trạng thái Hoạt động', 'Tiền tệ còn chọn được khi lập chứng từ mới.'),
        ('Trạng thái Khóa',
         'Tiền tệ không còn chọn được ở nghiệp vụ mới nhưng vẫn nằm trong danh mục và các '
         'chứng từ cũ không bị ảnh hưởng.'),
        ('Đang được sử dụng',
         'Tiền tệ đã xuất hiện ở ít nhất một chứng từ như báo giá, hợp đồng mua, hóa đơn, tờ '
         'khai hải quan, yêu cầu nhập hàng…; khi đó không được phép xóa.'),
    ],
    cot=[
        ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
        ('Mã tiền tệ', 'Ký hiệu viết tắt. Luôn hiển thị, sắp xếp được, bấm vào để mở cửa sổ xem.'),
        ('Tên tiền tệ', 'Tên đầy đủ của loại tiền, sắp xếp được.'),
        ('Tỷ giá (VNĐ)', 'Số tiền Việt Nam đồng cho một đơn vị, canh phải, sắp xếp được.'),
        ('Tên gọi khác', 'Tên gọi thay thế. Mặc định ẩn.'),
        ('Người cập nhật', 'Họ tên người sửa gần nhất. Mặc định ẩn.'),
        ('Ngày cập nhật', 'Ngày giờ sửa gần nhất, sắp xếp được. Mặc định ẩn.'),
        ('Người tạo', 'Họ tên người đã thêm bản ghi.'),
        ('Ngày tạo', 'Ngày giờ thêm bản ghi, sắp xếp được.'),
        ('Trạng thái', 'Hoạt động hoặc Khóa, hiển thị dạng badge.'),
        ('Hành động', 'Nút Sửa, Xóa, Khóa / Mở khóa và Lịch sử. Hai nút đầu còn dùng được hiện '
                      'thẳng, phần còn lại nằm trong nút ba chấm.'),
    ],
    nut_thanh_cong_cu=[
        ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện với người có quyền quản lý; mở cửa sổ Tạo tiền tệ.'),
        ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn trường cần xuất.'),
        ('Nút Tùy chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn cột hiển thị trên bảng.'),
    ],
    loc=[
        ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
         'Tìm đồng thời theo Mã, Tên tiền tệ và Tên gọi khác.'),
        ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Trống',
         'Bỏ trống thì hiện cả hai trạng thái.'),
    ],
    truong=[
        ('Mã tiền tệ', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Ký hiệu viết tắt, KHÔNG được trùng và được tự chuyển thành CHỮ IN HOA khi lưu. '
         'Bỏ trống báo “Bắt buộc phải nhập”; trùng báo “Mã tiền tệ đã tồn tại”.'),
        ('Tên tiền tệ', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Tên đầy đủ, KHÔNG được trùng. Bỏ trống báo “Bắt buộc phải nhập”; trùng báo '
         '“Tên tiền tệ đã tồn tại”.'),
        ('Tên gọi khác', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Tên gọi thay thế, không bắt buộc và không kiểm tra trùng.'),
        ('Tỷ giá (VNĐ)', 'Number', 'Enable', 'Lớn hơn 0 và tối đa 999.999,99', 'Có', 'Trống',
         'Nhập theo định dạng số của Việt Nam: dấu chấm ngăn cách hàng nghìn, dấu phẩy ngăn '
         'phần thập phân. Nhập 0 hoặc số âm báo “Phải lớn hơn 0”.'),
        ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
         'Đặt sẵn là Hoạt động khi thêm mới.'),
    ],
    tc_sheet='Danh muc tien te',
    tc_module='Tai chinh - Danh muc',
    tc_mucdich=(
        'Quan ly danh muc Tien te va ty gia quy doi ra dong Viet Nam. Man hinh cho phep tra cuu, '
        'tim kiem, them moi, chinh sua, xoa, khoa/mo khoa, xuat Excel va xem lich su thay doi. '
        'Du lieu cua man nay duoc chon khi lap bao gia, hop dong mua, hoa don va nhieu chung tu khac.'),
    tc_caudata=(
        '- Danh muc phang, khong phan cap cha con.\n'
        '- Moi tien te gom nam o: Ma, Ten, Ten goi khac, Ty gia va Trang thai.\n'
        '- Ban ghi duoc tham chieu tu khoang hai muoi loai chung tu; day la can cu quyet dinh '
        'co xoa duoc hay khong.'),
    tc_dedupe=(
        '- Moi tien te chi hien MOT dong.\n'
        '- Ma va Ten deu la duy nhat, kiem tra TACH ROI nhau. Rieng Ten goi khac KHONG kiem '
        'tra trung.\n'
        '- Khi sua, ban ghi dang sua duoc loai khoi ca hai phep kiem tra trung.'),
    tc_nguon=(
        'Du lieu lay tu danh muc Tien te. Cot so lan su dung duoc tong hop tu cac chung tu dang '
        'dung loai tien do.'),
    tc_luuy=[
        'Cac bay de sai nhat cua man nay, QA doc truoc khi test:',
        '- Man hinh dung HAI quyen tach roi. Nguoi chi co quyen xem VAN VAO DUOC man hinh.',
        '- Ty gia nhap theo dinh dang so cua Viet Nam: dau cham ngan hang nghin, dau phay ngan '
        'phan thap phan. Nhap "999.999,99" la hop le, khong phai loi.',
        '- Ty gia bat buoc LON HON 0. Nhap 0 se bi chan voi thong bao "Phai lon hon 0".',
        '- Ma duoc tu chuyen thanh CHU IN HOA khi luu, nen "usd" va "USD" bi coi la trung.',
        '- Ten goi khac KHONG kiem tra trung — dung bao loi nham.',
        '- Ban ghi da Khoa thi khong duoc sua va khong duoc xoa; chi duoc Mo khoa.',
        '- Man nay KHONG co chuc nang nhap tu Excel va KHONG co in danh sach.',
        '- Nut khong dung duoc phai AN HAN, khong phai hien nut xam.',
    ],
    hdsd_gioithieu=[
        'Danh mục tiền tệ là nơi khai báo các loại tiền dùng trong chứng từ mua bán, hợp đồng và hóa đơn, kèm tỷ giá quy đổi ra đồng Việt Nam.',
        'Mỗi loại tiền gồm Mã, Tên, Tên gọi khác, Tỷ giá và Trạng thái. Mã và Tên phải là duy nhất; riêng Tên gọi khác không kiểm tra trùng.',
        'Tỷ giá nhập theo định dạng số của Việt Nam: dấu chấm ngăn cách hàng nghìn, dấu phẩy ngăn phần thập phân, ví dụ 999.999,99.',
        'Loại tiền đã dùng ở chứng từ thì không xóa được; muốn ngừng dùng thì chuyển sang trạng thái Khóa.',
    ],
    hdsd_loi=[
        ['Bắt buộc phải nhập', 'Bạn chưa nhập Mã tiền tệ, Tên tiền tệ hoặc Tỷ giá. Cả ba đều bắt buộc.'],
        ['Mã tiền tệ đã tồn tại', 'Đã có loại tiền khác dùng đúng mã này. Hệ thống tự chuyển mã thành chữ in hoa nên usd và USD bị coi là trùng nhau.'],
        ['Tên tiền tệ đã tồn tại', 'Đã có loại tiền khác mang đúng tên này. Hãy đặt tên khác.'],
        ['Phải là số', 'Ô Tỷ giá có ký tự không hợp lệ. Chỉ nhập chữ số, dấu chấm ngăn hàng nghìn và dấu phẩy ngăn phần thập phân.'],
        ['Phải lớn hơn 0', 'Tỷ giá phải lớn hơn 0. Không nhập 0 hay số âm.'],
        ['Tối đa 999999.99', 'Tỷ giá không được vượt quá 999.999,99.'],
    ],
    hdsd_faq=[
        ['Tôi nhập tỷ giá 999.999,99 có đúng không', 'Đúng. Hệ thống hiểu dấu chấm là ngăn cách hàng nghìn và dấu phẩy là dấu thập phân, rồi tự chuyển về dạng chuẩn khi lưu.'],
        ['Tên gọi khác của tôi trùng với loại tiền khác, có sao không', 'Không sao. Ô Tên gọi khác cố ý không kiểm tra trùng.'],
        ['Dòng này không có nút Xóa', 'Loại tiền đó đã được dùng ở ít nhất một chứng từ như báo giá, hợp đồng mua, hóa đơn hay tờ khai hải quan. Nếu chỉ muốn ngừng dùng, hãy bấm Khóa thay vì Xóa.'],
        ['Làm sao biết loại tiền nào xóa được', 'Xem cột số lần sử dụng trên danh sách. Loại tiền có số 0 là chưa dùng ở đâu nên xóa được, và dòng đó sẽ có nút Xóa.'],
        ['Bản ghi đang Khóa mà tôi cần sửa', 'Bấm Mở khóa trước, sửa xong rồi Khóa lại nếu cần.'],
        ['Màn này có nhập từ Excel không', 'Không. Danh mục tiền tệ chỉ nhập tay và không có chức năng in danh sách.'],
    ],
    shots=dict(danhsach='tt_01_danhsach.png', boloc='tt_01_danhsach.png',
               taomoi='tt_02_taomoi.png', validate='tt_03_validate.png',
               xem='tt_04_xem.png', sua='tt_04_xem.png', lichsu='tt_05_lichsu.png',
               khoa='tt_06_xacnhan_khoa.png', xoa='tt_07_xacnhan_xoa.png',
               xuat='tt_08_xuat_excel.png', cot='tt_09_cauhinh_cot.png'),
    funcs=[
        'list', 'filter', ('view', {'nhan': 'Xem chi tiết tiền tệ', 'cot_bam': 'mã'}),
        'create', 'edit', 'delete', 'lock', 'history', 'export', 'columns',
    ],
    quy_tac=[
        ('Tách riêng quyền xem và quyền quản lý', [
            'Màn hình dùng hai quyền: “Quản lý danh mục tiền tệ” cho mọi thao tác ghi và '
            '“Xem danh mục tiền tệ” cho tra cứu, xuất Excel và xem lịch sử.',
            'Người chỉ có quyền xem không thấy nút Tạo mới, Sửa, Xóa và Khóa.',
            'Mọi thao tác ghi đều kiểm tra lại quyền ở tầng máy chủ.',
        ]),
        ('Hai ràng buộc trùng độc lập nhau', [
            'Mã tiền tệ phải là duy nhất trên toàn danh mục.',
            'Tên tiền tệ cũng phải là duy nhất, kiểm tra tách rời với Mã.',
            'Riêng Tên gọi khác KHÔNG kiểm tra trùng.',
            'Khi sửa, bản ghi đang sửa được loại khỏi cả hai phép so trùng.',
        ]),
        ('Mã luôn được lưu bằng chữ in hoa', [
            'Hệ thống tự chuyển mã sang chữ in hoa trước khi kiểm tra trùng và trước khi lưu.',
            'Nhập “usd” hay “USD” đều cho cùng một giá trị nên bị coi là trùng nhau.',
        ]),
        ('Tỷ giá nhập theo định dạng số của Việt Nam', [
            'Người dùng nhập dấu chấm để ngăn cách hàng nghìn và dấu phẩy để ngăn phần thập phân, '
            'ví dụ 999.999,99.',
            'Hệ thống tự chuyển về dạng chuẩn trước khi kiểm tra nên người dùng không phải đổi '
            'định dạng thủ công.',
            'Tỷ giá bắt buộc lớn hơn 0 và không vượt quá 999.999,99; vượt trần sẽ bị chặn ngay '
            'thay vì để dữ liệu bị cắt số.',
        ]),
        ('Bản ghi đã Khóa thì không sửa và không xóa', [
            'Tiền tệ ở trạng thái Khóa thì nút Sửa bị ẩn; muốn sửa phải Mở khóa trước.',
            'Máy chủ cũng từ chối mọi yêu cầu sửa và xóa trên bản ghi đang Khóa.',
            'Mở khóa là thao tác duy nhất được phép thực hiện trên bản ghi đang Khóa, bên cạnh '
            'các thao tác chỉ đọc.',
        ]),
        ('Chỉ xóa được tiền tệ chưa dùng ở chứng từ nào', [
            'Hệ thống kiểm tra khoảng hai mươi loại chứng từ, gồm báo giá, hợp đồng mua, hóa đơn, '
            'hóa đơn mua hàng, tờ khai hải quan, yêu cầu nhập hàng, dự án tiềm năng, tài khoản '
            'ngân hàng công ty và nhiều loại khác.',
            'Chỉ cần xuất hiện ở một nơi là nút Xóa bị ẨN HẲN, không hiện nút xám.',
            'Thông báo từ chối nêu tối đa ba nghiệp vụ đang dùng để người dùng biết phải xử lý '
            'ở đâu trước.',
            'Màn danh sách hiển thị sẵn số lần sử dụng của từng loại tiền để người dùng biết '
            'trước loại nào xóa được.',
        ]),
        ('Khóa khác với Xóa', [
            'Khóa chỉ ngừng cho chọn loại tiền ở chứng từ mới; các chứng từ cũ giữ nguyên giá '
            'trị và tỷ giá đã ghi.',
            'Xóa là bỏ hẳn bản ghi khỏi danh mục và chỉ làm được khi tiền tệ chưa dùng ở đâu.',
        ]),
        ('Mọi thay đổi đều được ghi lịch sử', [
            'Năm trường Mã, Tên, Tên gọi khác, Tỷ giá và Trạng thái đều được theo dõi thay đổi.',
            'Với thao tác sửa, hệ thống ghi từng trường đã đổi kèm giá trị trước và sau.',
            'Lịch sử sắp xếp mới nhất lên trước và không sửa hay xóa được.',
        ]),
    ],
)

SCREENS = [CURRENCY]
