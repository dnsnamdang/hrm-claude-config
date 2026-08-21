# -*- coding: utf-8 -*-
"""Cau hinh 6 man danh muc dia ly dung chung cho gen_srs.py.

Doc code 17/08/2026:
  BE  Modules/Human/Routes/api.php (394-456) — KHONG endpoint nao gan quyen
      Modules/Human/Http/Requests/Create{Nation,Areas,Province,District,Ward,Hamlet}Request.php
      Modules/Human/Services/{Nation,Area,Province,District,Ward,Hamlet}Service.php
      app/Services/CatalogHistoryService.php (bang nhan cot lich su)
  FE  hrm-client/pages/human/<man>/index.vue + components/<X>Model.vue
  Anh that: geo_shots/ (cong dev hrm-crm.eteksofts.com, 17/08/2026)
"""

HOST = 'http://hrm-crm.eteksofts.com'

# ---------------------------------------------------------------- dùng chung
QUYEN_CHUNG = (
    'Màn hình này KHÔNG gắn quyền ở bất kỳ chức năng nào. Mọi người dùng đã đăng nhập đều mở '
    'được màn hình và thực hiện được đầy đủ Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa. '
    'Đây là hiện trạng của mã nguồn tại thời điểm lập tài liệu, không phải thiết kế mong muốn.'
)

CANH_BAO_QUYEN = (
    'Vì chưa có quyền, giao diện KHÔNG ẩn hay làm mờ nút nào theo vai trò. Phía máy chủ cũng '
    'không kiểm tra quyền, nên gọi thẳng chức năng mà bỏ qua giao diện vẫn ghi được dữ liệu.'
)

LOI_CHUNG = 'Bắt buộc phải nhập'


def _co_khoa(cfg):
    return cfg.get('co_khoa', True)


# ---------------------------------------------------------------- 6 màn
SCREENS = [

    # ============================================================ QUỐC GIA
    dict(
        key='nations',
        ten='Danh mục quốc gia',
        doi_tuong='quốc gia',
        route='/human/nations',
        co_khoa=True,
        muc_dich=[
            'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý danh mục quốc gia.',
            'Là căn cứ nghiệm thu chức năng.',
            'Làm rõ ràng buộc trùng tên và trùng mã quốc gia — hai trường này duy nhất trên '
            'toàn hệ thống.',
            'Ghi nhận hiện trạng màn hình chưa được gắn quyền, để bộ phận quản trị cân nhắc '
            'bổ sung.',
        ],
        thuat_ngu=[
            ('Quốc gia', 'Bản ghi gốc của cây địa chỉ. Mọi Khu vực và Tỉnh/TP đều trực thuộc '
                         'một quốc gia.'),
            ('Mã quốc gia', 'Mã do người dùng tự đặt, duy nhất trên toàn hệ thống.'),
            ('Mã bưu chính', 'Thông tin tham khảo, chỉ nhận chữ số, không bắt buộc.'),
            ('Trạng thái Hoạt động', 'Quốc gia dùng được ở các màn nghiệp vụ khác.'),
            ('Trạng thái Khóa', 'Quốc gia không còn chọn được ở nơi khác nhưng vẫn nằm trong '
                                'danh mục và vẫn xem được lịch sử.'),
            ('SRS', 'Software Requirements Specification'),
        ],
        cot=[
            ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
            ('Tên quốc gia', 'Tên đầy đủ. Luôn hiển thị, sắp xếp được.'),
            ('Mã quốc gia', 'Mã do người dùng đặt, sắp xếp được.'),
            ('Mã bưu chính', 'Mặc định ẩn, bật ở cửa sổ tuỳ chỉnh cột.'),
            ('Người tạo', 'Người đã thêm bản ghi.'),
            ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
            ('Trạng thái', 'Hoạt động hoặc Khóa.'),
            ('Hành động', 'Sửa, Xóa hiện thẳng; Khóa / Mở khóa và Lịch sử nằm trong nút ba chấm.'),
        ],
        loc=[
            ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
             'Tìm theo tên quốc gia và mã quốc gia.'),
            ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Trống',
             'Bỏ trống thì hiện cả hai trạng thái.'),
        ],
        truong=[
            # (tên, loại, phạm vi, bắt buộc, giá trị ban đầu, mô tả)
            ('Tên quốc gia', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Duy nhất toàn hệ thống. Bỏ trống báo “Bắt buộc phải nhập”; trùng báo '
             '“Tên quốc gia này đã tồn tại”.'),
            ('Mã quốc gia', 'Textbox', '0–50 ký tự', 'Có', 'Trống',
             'Duy nhất toàn hệ thống. Bỏ trống báo “Bắt buộc phải nhập”; trùng báo '
             '“Mã quốc gia này đã tồn tại”.'),
            ('Mã bưu chính', 'Textbox', '1–50 chữ số', 'Không', 'Trống',
             'Chỉ nhận chữ số. Nhập chữ báo “Phải là số”; quá dài báo '
             '“Chỉ được nhập chữ số, từ 1 đến 50 chữ số”.'),
        ],
        loi_trung_ten='Tên quốc gia này đã tồn tại',
        pham_vi_trung='trên toàn hệ thống',
        shots=dict(
            danhsach='nations_01_danhsach.png',
            taomoi='nations_02_taomoi.png',
            validate='nations_03_validate.png',
            menu='nations_04_menu_hanhdong.png',
            khoa='nations_05_xacnhan_khoa.png',
            lichsu='nations_06_lichsu.png',
        ),
        cap_tren=None,
    ),

    # ============================================================ KHU VỰC
    dict(
        key='areas',
        ten='Danh mục khu vực',
        doi_tuong='khu vực',
        route='/human/areas',
        co_khoa=True,
        muc_dich=[
            'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý danh mục khu vực.',
            'Là căn cứ nghiệm thu chức năng.',
            'Làm rõ quan hệ Khu vực trực thuộc Quốc gia và ràng buộc trùng tên khu vực.',
            'Ghi nhận hiện trạng màn hình chưa được gắn quyền.',
        ],
        thuat_ngu=[
            ('Khu vực', 'Nhóm địa lý trung gian giữa Quốc gia và Tỉnh/TP, ví dụ Miền Bắc, '
                        'Miền Nam.'),
            ('Quốc gia', 'Bản ghi cha bắt buộc của khu vực, lấy từ Danh mục quốc gia.'),
            ('Trạng thái Hoạt động', 'Khu vực dùng được ở các màn nghiệp vụ khác.'),
            ('Trạng thái Khóa', 'Khu vực không còn chọn được ở nơi khác nhưng vẫn nằm trong '
                                'danh mục.'),
            ('SRS', 'Software Requirements Specification'),
        ],
        cot=[
            ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
            ('Khu vực', 'Tên khu vực. Luôn hiển thị, sắp xếp được.'),
            ('Quốc gia', 'Quốc gia mà khu vực trực thuộc.'),
            ('Người sửa', 'Mặc định ẩn.'),
            ('Ngày cập nhật', 'Mặc định ẩn, sắp xếp được.'),
            ('Người tạo', 'Người đã thêm bản ghi.'),
            ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
            ('Trạng thái', 'Hoạt động hoặc Khóa.'),
            ('Hành động', 'Sửa, Xóa hiện thẳng; Khóa / Mở khóa và Lịch sử nằm trong nút ba chấm.'),
        ],
        loc=[
            ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống', 'Tìm theo tên khu vực.'),
            ('Quốc gia', 'Dropdown', 'Danh sách', 'Trống', 'Lọc khu vực theo quốc gia.'),
            ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Trống',
             'Bỏ trống thì hiện cả hai trạng thái.'),
        ],
        truong=[
            ('Tên khu vực', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Duy nhất toàn hệ thống. Bỏ trống báo “Bắt buộc phải nhập”; trùng báo '
             '“Tên khu vực này đã tồn tại”.'),
            ('Quốc gia', 'Dropdown', 'Danh sách', 'Có', 'Trống',
             'Lấy từ Danh mục quốc gia. Bỏ trống báo “Bắt buộc phải nhập”.'),
        ],
        loi_trung_ten='Tên khu vực này đã tồn tại',
        pham_vi_trung='trên toàn hệ thống',
        shots=dict(
            danhsach='areas_01_danhsach.png',
            taomoi='areas_02_taomoi.png',
            lichsu='areas_03_lichsu.png',
            xoa='areas_04_xacnhan_xoa.png',
            khoa='areas_05_xacnhan_khoa.png',
        ),
        cap_tren='Quốc gia',
    ),

    # ============================================================ TỈNH / TP
    dict(
        key='provinces',
        ten='Danh mục Tỉnh/TP',
        doi_tuong='tỉnh/TP',
        route='/human/provinces',
        co_khoa=True,
        muc_dich=[
            'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý danh mục Tỉnh/TP.',
            'Là căn cứ nghiệm thu chức năng.',
            'Làm rõ ràng buộc trùng tên xét theo CẶP Quốc gia và Khu vực, khác với các màn '
            'địa lý còn lại.',
            'Ghi nhận hiện trạng màn hình chưa được gắn quyền.',
        ],
        thuat_ngu=[
            ('Tỉnh/TP', 'Đơn vị hành chính cấp tỉnh, trực thuộc một Quốc gia và một Khu vực.'),
            ('Biển số xe', 'Mã biển số của tỉnh, bắt buộc nhập, chỉ nhận chữ số.'),
            ('Mã số tỉnh', 'Mã tham khảo, chỉ nhận chữ số, không bắt buộc.'),
            ('Trạng thái Hoạt động', 'Tỉnh/TP dùng được ở các màn nghiệp vụ khác.'),
            ('Trạng thái Khóa', 'Tỉnh/TP không còn chọn được ở nơi khác nhưng vẫn nằm trong '
                                'danh mục.'),
            ('SRS', 'Software Requirements Specification'),
        ],
        cot=[
            ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
            ('Tên Tỉnh/TP', 'Tên đầy đủ. Luôn hiển thị, sắp xếp được.'),
            ('Mã Tỉnh/TP', 'Mã tham khảo, sắp xếp được.'),
            ('Biển số xe', 'Mặc định ẩn.'),
            ('Quốc gia', 'Mặc định ẩn.'),
            ('Khu vực', 'Mặc định ẩn.'),
            ('Người sửa', 'Mặc định ẩn.'),
            ('Ngày cập nhật', 'Mặc định ẩn, sắp xếp được.'),
            ('Người tạo', 'Người đã thêm bản ghi.'),
            ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
            ('Trạng thái', 'Hoạt động hoặc Khóa.'),
            ('Hành động', 'Sửa, Xóa hiện thẳng; Khóa / Mở khóa và Lịch sử nằm trong nút ba chấm.'),
        ],
        loc=[
            ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
             'Tìm theo tên và mã Tỉnh/TP.'),
            ('Quốc gia', 'Dropdown', 'Danh sách', 'Trống', 'Lọc Tỉnh/TP theo quốc gia.'),
            ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Trống',
             'Bỏ trống thì hiện cả hai trạng thái.'),
        ],
        truong=[
            ('Tên tỉnh/TP', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Không được trùng trong cùng một cặp Quốc gia và Khu vực. Bỏ trống báo '
             '“Bắt buộc phải nhập”.'),
            ('Mã số tỉnh', 'Textbox', '0–10 chữ số', 'Không', 'Trống',
             'Chỉ nhận chữ số. Nhập chữ báo “Phải là số”.'),
            ('Biển số xe', 'Textbox', '0–50 chữ số', 'Có', 'Trống',
             'Chỉ nhận chữ số. Bỏ trống báo “Bắt buộc phải nhập”.'),
            ('Quốc gia', 'Dropdown', 'Danh sách', 'Có', 'Trống',
             'Lấy từ Danh mục quốc gia. Bỏ trống báo “Bắt buộc phải nhập”.'),
            ('Khu vực', 'Dropdown', 'Danh sách', 'Có', 'Trống',
             'Lấy từ Danh mục khu vực. Bỏ trống báo “Bắt buộc phải nhập”.'),
        ],
        loi_trung_ten='Tên khu vực này đã tồn tại',
        pham_vi_trung='trong cùng một cặp Quốc gia và Khu vực',
        shots=dict(
            danhsach='provinces_01_danhsach.png',
            taomoi='provinces_02_taomoi.png',
            lichsu='provinces_03_lichsu_rong.png',
            xoa='provinces_04_xacnhan_xoa.png',
            khoa='provinces_05_xacnhan_khoa.png',
        ),
        cap_tren='Quốc gia và Khu vực',
        ghi_chu_loi_trung=(
            '⚠️ Thông báo trùng tên của màn này hiện đúng nguyên văn “Tên khu vực này đã tồn tại” '
            '— chữ “khu vực” bị lấy nhầm từ màn Danh mục khu vực. Đây là lỗi hiển thị đã ghi nhận, '
            'tài liệu nêu đúng câu người dùng nhìn thấy để bộ phận kiểm thử đối chiếu.'
        ),
    ),

    # ============================================================ QUẬN / HUYỆN
    dict(
        key='districts',
        ten='Danh mục Quận/Huyện',
        doi_tuong='quận/huyện',
        route='/human/districts',
        co_khoa=False,
        muc_dich=[
            'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý danh mục Quận/Huyện.',
            'Là căn cứ nghiệm thu chức năng.',
            'Làm rõ điểm khác biệt so với các màn địa lý khác: màn này KHÔNG có cột Trạng thái '
            'và KHÔNG có thao tác Khóa / Mở khóa.',
            'Ghi nhận hiện trạng màn hình chưa được gắn quyền.',
        ],
        thuat_ngu=[
            ('Quận/Huyện', 'Đơn vị hành chính cấp huyện, trực thuộc một Tỉnh/TP.'),
            ('Xóa', 'Trên màn này, xóa là chuyển bản ghi sang trạng thái ngừng sử dụng ở phía '
                    'máy chủ. Bản ghi biến mất khỏi danh sách nhưng dữ liệu không mất hẳn.'),
            ('SRS', 'Software Requirements Specification'),
        ],
        cot=[
            ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
            ('Tên quận/huyện', 'Tên đầy đủ. Luôn hiển thị, sắp xếp được.'),
            ('Tỉnh/TP', 'Tỉnh/TP mà quận/huyện trực thuộc.'),
            ('Quốc gia', 'Mặc định ẩn.'),
            ('Ngày cập nhật', 'Mặc định ẩn, sắp xếp được.'),
            ('Người tạo', 'Người đã thêm bản ghi.'),
            ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
            ('Hành động', 'Sửa, Xóa và Lịch sử.'),
        ],
        loc=[
            ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống', 'Tìm theo tên quận/huyện.'),
            ('Quốc gia', 'Dropdown', 'Danh sách', 'Trống',
             'Chọn quốc gia sẽ lọc lại danh sách của ô Tỉnh/TP.'),
            ('Tỉnh/TP', 'Dropdown', 'Danh sách', 'Trống',
             'Bị xóa trắng khi đổi Quốc gia.'),
        ],
        truong=[
            ('Tên quận/huyện', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Không được trùng trong cùng một Tỉnh/TP. Bỏ trống báo “Bắt buộc phải nhập”; '
             'trùng báo “Tên quận/huyện này đã tồn tại trong tỉnh/TP”.'),
            ('Tỉnh/TP', 'Dropdown', 'Danh sách', 'Có', 'Trống',
             'Lấy từ Danh mục Tỉnh/TP. Bỏ trống báo “Bắt buộc phải nhập”.'),
        ],
        loi_trung_ten='Tên quận/huyện này đã tồn tại trong tỉnh/TP',
        pham_vi_trung='trong cùng một Tỉnh/TP',
        shots=dict(
            danhsach='districts_01_danhsach.png',
            taomoi='districts_02_taomoi.png',
            xoa='districts_03_xacnhan_xoa.png',
            lichsu='districts_04_lichsu.png',
        ),
        cap_tren='Tỉnh/TP',
    ),

    # ============================================================ PHƯỜNG / XÃ
    dict(
        key='wards',
        ten='Danh mục Phường/Xã',
        doi_tuong='phường/xã',
        route='/human/wards',
        co_khoa=True,
        muc_dich=[
            'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý danh mục Phường/Xã.',
            'Là căn cứ nghiệm thu chức năng.',
            'Làm rõ ràng buộc trùng tên xét trong phạm vi một Tỉnh/TP và quy tắc Mã số bắt buộc.',
            'Ghi nhận hiện trạng màn hình chưa được gắn quyền.',
        ],
        thuat_ngu=[
            ('Phường/Xã', 'Đơn vị hành chính cấp xã, trực thuộc một Tỉnh/TP.'),
            ('Mã số', 'Mã của phường/xã, bắt buộc nhập, chỉ nhận chữ số.'),
            ('Trạng thái Hoạt động', 'Phường/xã dùng được ở các màn nghiệp vụ khác.'),
            ('Trạng thái Khóa', 'Phường/xã không còn chọn được ở nơi khác nhưng vẫn nằm trong '
                                'danh mục.'),
            ('SRS', 'Software Requirements Specification'),
        ],
        cot=[
            ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
            ('Tên phường/xã', 'Tên đầy đủ. Luôn hiển thị, sắp xếp được.'),
            ('Tỉnh/TP', 'Tỉnh/TP mà phường/xã trực thuộc.'),
            ('Quốc gia', 'Mặc định ẩn.'),
            ('Người sửa', 'Mặc định ẩn.'),
            ('Ngày cập nhật', 'Mặc định ẩn, sắp xếp được.'),
            ('Người tạo', 'Người đã thêm bản ghi.'),
            ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
            ('Trạng thái', 'Hoạt động hoặc Khóa.'),
            ('Hành động', 'Sửa, Xóa hiện thẳng; Khóa / Mở khóa và Lịch sử nằm trong nút ba chấm.'),
        ],
        loc=[
            ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống', 'Tìm theo tên phường/xã.'),
            ('Quốc gia', 'Dropdown', 'Danh sách', 'Trống',
             'Chọn quốc gia sẽ lọc lại danh sách của ô Tỉnh/TP.'),
            ('Tỉnh/TP', 'Dropdown', 'Danh sách', 'Trống', 'Bị xóa trắng khi đổi Quốc gia.'),
        ],
        truong=[
            ('Tên phường/xã', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Không được trùng trong cùng một Tỉnh/TP. Bỏ trống báo “Bắt buộc phải nhập”; '
             'trùng báo “Tên phường/xã này đã tồn tại”.'),
            ('Mã số', 'Textbox', '0–10 chữ số', 'Có', 'Trống',
             'Chỉ nhận chữ số. Bỏ trống báo “Bắt buộc phải nhập”; nhập chữ báo “Phải là số”.'),
            ('Tỉnh/TP', 'Dropdown', 'Danh sách', 'Có', 'Trống',
             'Lấy từ Danh mục Tỉnh/TP. Bỏ trống báo “Bắt buộc phải nhập”.'),
        ],
        loi_trung_ten='Tên phường/xã này đã tồn tại',
        pham_vi_trung='trong cùng một Tỉnh/TP',
        shots=dict(
            danhsach='wards_01_danhsach.png',
            taomoi='wards_02_taomoi.png',
            xoa='wards_03_xacnhan_xoa.png',
            khoa='wards_04_xacnhan_khoa.png',
            lichsu='wards_05_lichsu.png',
        ),
        cap_tren='Tỉnh/TP',
    ),

    # ============================================================ ĐƯỜNG / PHỐ
    dict(
        key='hamlets',
        ten='Danh mục Đường/Phố',
        doi_tuong='đường/phố',
        route='/human/hamlets',
        co_khoa=False,
        muc_dich=[
            'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý danh mục Đường/Phố.',
            'Là căn cứ nghiệm thu chức năng.',
            'Làm rõ quy tắc riêng: ô Quận/Huyện chỉ hiện khi Quốc gia KHÁC Việt Nam.',
            'Làm rõ màn này KHÔNG có cột Trạng thái và KHÔNG có thao tác Khóa / Mở khóa.',
            'Ghi nhận hiện trạng màn hình chưa được gắn quyền.',
        ],
        thuat_ngu=[
            ('Đường/Phố', 'Cấp địa chỉ nhỏ nhất trong hệ thống, trực thuộc một Phường/Xã.'),
            ('Quy tắc Việt Nam', 'Khi Quốc gia là Việt Nam, ô Quận/Huyện/Thị xã bị ẩn và không '
                                 'phải nhập; địa chỉ đi thẳng từ Tỉnh/TP xuống Phường/Xã.'),
            ('Xóa', 'Trên màn này, xóa là chuyển bản ghi sang trạng thái ngừng sử dụng ở phía '
                    'máy chủ. Bản ghi biến mất khỏi danh sách nhưng dữ liệu không mất hẳn.'),
            ('SRS', 'Software Requirements Specification'),
        ],
        cot=[
            ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
            ('Tên đường/phố', 'Tên đầy đủ. Luôn hiển thị, sắp xếp được.'),
            ('Phường/xã', 'Phường/xã mà đường/phố trực thuộc.'),
            ('Quận/Huyện/Thị xã', 'Mặc định ẩn.'),
            ('Tỉnh/TP', 'Tỉnh/TP tương ứng.'),
            ('Quốc gia', 'Mặc định ẩn.'),
            ('Ngày cập nhật', 'Mặc định ẩn, sắp xếp được.'),
            ('Người tạo', 'Người đã thêm bản ghi.'),
            ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
            ('Hành động', 'Sửa, Xóa và Lịch sử.'),
        ],
        loc=[
            ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống', 'Tìm theo tên đường/phố.'),
            ('Tỉnh/TP', 'Dropdown', 'Danh sách', 'Trống',
             'Chọn Tỉnh/TP sẽ lọc lại danh sách của ô Phường/xã.'),
            ('Phường/xã', 'Dropdown', 'Danh sách', 'Trống', 'Bị xóa trắng khi đổi Tỉnh/TP.'),
        ],
        truong=[
            ('Tên đường/phố', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Không được trùng trong cùng một Phường/Xã. Bỏ trống báo “Bắt buộc phải nhập”; '
             'trùng báo “Tên đường/phố này đã tồn tại trong phường/xã”.'),
            ('Quốc gia', 'Dropdown', 'Danh sách', 'Có', 'Việt Nam',
             'Quyết định ô Quận/Huyện/Thị xã có hiện hay không.'),
            ('Tỉnh/TP', 'Dropdown', 'Danh sách', 'Có', 'Trống',
             'Chỉ hiện Tỉnh/TP thuộc quốc gia đã chọn.'),
            ('Quận/Huyện/Thị xã', 'Dropdown', 'Danh sách', 'Có khi Quốc gia khác Việt Nam',
             'Ẩn', 'ẨN HẲN khi Quốc gia là Việt Nam; hiện và bắt buộc với mọi quốc gia khác.'),
            ('Phường/xã', 'Dropdown', 'Danh sách', 'Có', 'Trống',
             'Bỏ trống báo “Bắt buộc phải nhập”.'),
        ],
        loi_trung_ten='Tên đường/phố này đã tồn tại trong phường/xã',
        pham_vi_trung='trong cùng một Phường/Xã',
        shots=dict(
            danhsach='hamlets_01_danhsach.png',
            taomoi='hamlets_02_taomoi.png',
            xoa='hamlets_03_xacnhan_xoa.png',
            khac_vn='hamlets_04_quocgia_khac_vn.png',
            lichsu='hamlets_05_lichsu.png',
        ),
        cap_tren='Phường/Xã',
    ),
]
