# -*- coding: utf-8 -*-
"""Cau hinh man 'Cap nhat nhanh gia dich vu' (/customer-care/service-price-config).

Doc code 18/08/2026:
  BE  Modules/CustomerCare/Routes/api.php (160-172) — gate bang `erpPermission` chu KHONG phai
      `checkPermission` (quyen goc cua he cu dung guard khac).
      Modules/CustomerCare/Http/Requests/ServicePriceConfig/ServicePriceConfigRequest.php
        coefficient_cost_price_service: required|numeric|min:0.01|max:999.99
        sale_max_percent:               nullable|numeric|min:0|max:99
  FE  hrm-client/pages/customer-care/service-price-config/index.vue
  Anh that: sp_shots/ (cong dev hrm-crm.eteksofts.com, 18/08/2026)
"""

HOST = 'http://hrm-crm.eteksofts.com'

PRICE = dict(
    key='sp',
    ten='Cập nhật nhanh giá dịch vụ',
    doi_tuong='cấu hình giá dịch vụ',
    route='/customer-care/service-price-config',
    host=HOST,
    menu='Phân hệ CSKH → Cập nhật nhanh giá dịch vụ',
    quyen_quan_ly='Cập nhật nhanh giá dịch vụ',
    quyen_xem=None,
    tacdung_ql='Mở màn hình và lưu cấu hình. Đây là quyền duy nhất của màn: có quyền thì xem '
               'và sửa được, không có quyền thì không vào được màn hình.',
    tacdung_xem='',
    ghichu_quyen='Màn hình chỉ có MỘT quyền, không tách riêng quyền xem và quyền sửa. Người '
                 'không có quyền thì mục menu không hiển thị và truy cập thẳng đường dẫn cũng '
                 'bị chặn.',
    co_trangthai=False,
    truong_trung=None,
    loi_trung=None,
    loi_khac=[
        '– Hệ số giá bán dịch vụ nhập chữ → hiển thị “Phải là số”.',
        '– Hệ số giá bán dịch vụ nhỏ hơn 0,01 → hiển thị “Không được nhỏ hơn 0.01”.',
        '– Hệ số giá bán dịch vụ lớn hơn 999,99 → hiển thị “Tối đa 999.99”.',
        '– Định mức đàm phán giá nhập chữ → hiển thị “Phải là số”.',
        '– Định mức đàm phán giá nhỏ hơn 0 → hiển thị “Không được nhỏ hơn 0”.',
        '– Định mức đàm phán giá lớn hơn 99 → hiển thị “Tối đa 99”.',
    ],
    muc_dich=[
        'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn Cập nhật nhanh giá dịch vụ.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ phạm vi ảnh hưởng của thao tác Lưu: một lần lưu ghi đè hệ số và định mức cho '
        'TOÀN BỘ gói bảo dưỡng, kể cả gói đã được chỉnh riêng.',
        'Ghi nhận khác biệt có chủ đích so với màn cũ: bản này thêm hộp thoại xác nhận nêu rõ '
        'số gói bị ảnh hưởng trước khi ghi, còn bản cũ bấm Lưu là chạy ngay.',
    ],
    thuat_ngu=[
        ('Hệ số giá bán dịch vụ',
         'Hệ số nhân dùng khi tính giá bán của gói bảo dưỡng từ giá vốn. Giá trị phải lớn hơn '
         'hoặc bằng 0,01 và không vượt quá 999,99.'),
        ('Định mức đàm phán giá (%)',
         'Tỷ lệ phần trăm tối đa được phép giảm khi thương lượng giá với khách hàng. Nhận giá '
         'trị từ 0 đến 99.'),
        ('Gói bảo dưỡng',
         'Gói dịch vụ bán cho khách hàng. Mọi gói đều bị áp lại hệ số và định mức khi lưu.'),
        ('Cấp dịch vụ',
         'Mức độ của một lần bảo dưỡng trong gói. Giá gốc của cấp dịch vụ được tính lại khi hệ '
         'số thay đổi.'),
        ('Ghi đè hàng loạt',
         'Một lần lưu áp giá trị mới cho toàn bộ gói bảo dưỡng, kể cả gói trước đó đã được '
         'chỉnh riêng. Thao tác này không có chức năng hoàn tác.'),
    ],
    cot=[],
    loc=[],
    truong=[
        ('Hệ số giá bán dịch vụ', 'Number', 'Enable', '0,01 – 999,99', 'Có', 'Theo cấu hình đã lưu',
         'Hệ số nhân dùng khi tính giá bán. Bỏ trống báo “Bắt buộc phải nhập”; nhập chữ báo '
         '“Phải là số”; vượt trần báo “Tối đa 999.99”.'),
        ('Định mức đàm phán giá (%)', 'Number', 'Enable', '0 – 99', 'Không', 'Theo cấu hình đã lưu',
         'Tỷ lệ giảm giá tối đa khi thương lượng. Được phép nhập 0; vượt 99 báo “Tối đa 99”.'),
        ('Dòng cảnh báo phạm vi', 'Label', 'Read-only', '–', 'Không', 'Theo dữ liệu',
         'Nêu rõ số gói bảo dưỡng sẽ bị ghi đè khi lưu.'),
        ('Dòng cập nhật gần nhất', 'Label', 'Read-only', '–', 'Không', 'Theo dữ liệu',
         'Ngày giờ và người thực hiện lần lưu gần nhất.'),
    ],
    tc_sheet='Cap nhat nhanh gia dich vu',
    tc_module='CSKH',
    tc_mucdich='Cap nhat he so gia ban dich vu va dinh muc dam phan gia dung chung cho toan he '
               'thong. Mot lan luu se ap lai gia tri moi cho TOAN BO goi bao duong dang co.',
    tc_thoigian='Man hinh KHONG co bo loc thoi gian. Yeu to thoi gian chi xuat hien o dong ghi '
                'chu ve lan cap nhat gan nhat.',
    tc_caudata='- Man hinh chi co MOT ban ghi cau hinh dung chung cho toan he thong.\n'
               '- Khong tach theo cong ty hay theo nhom.\n'
               '- Lan luu sau ghi de len lan luu truoc.',
    tc_dedupe='- Khong co khai niem trung lap o man nay vi chi co mot ban ghi cau hinh.\n'
              '- Moi lan luu deu ghi de len gia tri cu.',
    tc_nguon='Cau hinh dung chung cua he thong. Pham vi anh huong la toan bo goi bao duong va '
             'cap dich vu.',
    tc_luuy=[
        'Cac bay de sai nhat cua man nay, QA doc truoc khi test:',
        '- BAT BUOC sao luu du lieu gia TRUOC khi bam Luu lan dau. Mot lan luu ghi de toan bo goi bao duong va KHONG CO HOAN TAC.',
        '- Goi da duoc chinh rieng cung bi ghi de. Day la hanh vi dung theo thiet ke, khong phai loi.',
        '- Dinh muc dam phan LUON bi ghi de cho moi goi, ke ca khi gia tri khong doi.',
        '- Gia goc cua cap dich vu CHI duoc tinh lai khi he so thuc su thay doi.',
        '- Goi khong xac dinh duoc don gia cong cua cong ty se bi BO QUA, giu nguyen gia cu, va he thong bao lai so goi bi bo qua.',
        '- Man hinh chi co MOT quyen cho ca xem lan sua.',
        '- Man nay khong co danh sach, khong co phan trang, khong co bo loc.',
    ],
    hdsd_gioithieu=[
        'Cập nhật nhanh giá dịch vụ là nơi khai báo hai thông số dùng chung cho toàn bộ gói bảo dưỡng: Hệ số giá bán dịch vụ và Định mức đàm phán giá.',
        'Điểm cần nhớ nhất: đây KHÔNG phải màn danh sách. Toàn hệ thống chỉ có một bộ thông số duy nhất, và một lần lưu sẽ áp lại giá trị mới cho TẤT CẢ gói bảo dưỡng đang có, kể cả những gói đã được chỉnh riêng.',
        'Thao tác này không hoàn tác được. Hãy sao lưu dữ liệu giá trước khi lưu lần đầu.',
    ],
    hdsd_loi=[
        ['Bắt buộc phải nhập', 'Bạn chưa nhập Hệ số giá bán dịch vụ. Ô này bắt buộc.'],
        ['Phải là số', 'Bạn đã nhập chữ vào ô số. Chỉ nhập chữ số và dấu thập phân.'],
        ['Tối đa 999.99', 'Hệ số giá bán dịch vụ không được vượt quá 999,99.'],
        ['Tối đa 99', 'Định mức đàm phán giá là tỷ lệ phần trăm, chỉ nhận giá trị từ 0 đến 99.'],
        ['Không được nhỏ hơn 0.01', 'Hệ số giá bán dịch vụ phải từ 0,01 trở lên.'],
    ],
    hdsd_faq=[
        ['Tôi đã chỉnh giá riêng cho một gói, lưu ở đây có mất không', 'Có. Gói đó cũng bị áp lại theo giá trị chung. Đây là hành vi đúng theo thiết kế, không phải lỗi. Nếu cần giữ giá riêng, hãy chỉnh lại gói đó sau khi lưu.'],
        ['Có hoàn tác được không', 'Không. Hãy sao lưu dữ liệu giá trước khi bấm Lưu lần đầu.'],
        ['Hệ thống báo có gói bị bỏ qua', 'Những gói đó không xác định được đơn giá công của công ty nên hệ thống giữ nguyên giá cũ thay vì ghi giá sai. Bạn cần kiểm tra cấu hình đơn giá công của công ty tương ứng rồi lưu lại.'],
        ['Tôi chỉ đổi định mức, vì sao giá gốc không đổi', 'Giá gốc của cấp dịch vụ chỉ được tính lại khi Hệ số giá bán dịch vụ thay đổi. Đổi riêng định mức thì không ảnh hưởng tới giá gốc.'],
        ['Tôi không vào được màn hình này', 'Màn này cần quyền Cập nhật nhanh giá dịch vụ. Liên hệ quản trị viên để được cấp quyền.'],
    ],
    shots=dict(xem='sp_01_manhinh.png', validate='sp_02_validate.png',
               xacnhan='sp_03_xacnhan.png'),
    funcs=[
        ('view', {'nhan': 'Xem cấu hình giá dịch vụ hiện tại', 'modal': False,
                  'cot_bam': 'mục menu Cập nhật nhanh giá dịch vụ'}),
        'save',
    ],
    quy_tac=[
        ('Một quyền duy nhất cho cả xem và sửa', [
            'Màn hình dùng đúng một quyền “Cập nhật nhanh giá dịch vụ”.',
            'Không tách quyền xem riêng: có quyền thì vừa xem vừa sửa được, không có quyền thì '
            'không vào được màn hình.',
            'Quyền này được kiểm tra theo TÊN quyền nên tài khoản đã được cấp ở hệ thống cũ '
            'vẫn dùng được màn này mà không cần cấp lại.',
        ]),
        ('Cấu hình chỉ có duy nhất một bản ghi', [
            'Toàn hệ thống chỉ có một bộ hệ số và định mức dùng chung, không tách theo công ty '
            'hay theo nhóm.',
            'Lần lưu sau ghi đè lên lần lưu trước.',
            'Nếu chưa có bản ghi nào, hệ thống tự tạo mới khi lưu lần đầu.',
        ]),
        ('Lưu là ghi đè hàng loạt, không có hoàn tác', [
            'Một lần lưu áp hệ số và định mức mới cho TOÀN BỘ gói bảo dưỡng đang có.',
            'Gói đã được chỉnh riêng trước đó cũng bị ghi đè, không có ngoại lệ.',
            'Hệ thống bắt buộc hiển thị hộp thoại xác nhận nêu rõ số gói bảo dưỡng và số cấp '
            'dịch vụ bị ảnh hưởng trước khi thực hiện.',
            'Đây là điểm khác có chủ đích so với màn cũ: bản cũ bấm Lưu là chạy ngay, không hỏi.',
        ]),
        ('Giá gốc chỉ tính lại khi hệ số thực sự thay đổi', [
            'Nếu hệ số giá bán dịch vụ giữ nguyên, hệ thống không tính lại giá gốc của cấp '
            'dịch vụ để tránh thay đổi thừa.',
            'Ngược lại, định mức đàm phán giá LUÔN được ghi đè cho mọi gói, kể cả khi giá trị '
            'không đổi.',
        ]),
        ('Gói thiếu đơn giá công của công ty thì bị bỏ qua', [
            'Gói bảo dưỡng không xác định được đơn giá công của công ty sẽ bị bỏ qua, giữ '
            'nguyên giá cũ.',
            'Hệ thống báo lại số gói bị bỏ qua để người dùng biết mà xử lý riêng.',
            'Đây là điểm khác có chủ đích so với màn cũ: bản cũ ghi giá gốc của gói đó về 0, '
            'làm hỏng dữ liệu giá.',
        ]),
        ('Cần sao lưu trước lần lưu đầu tiên', [
            'Vì thao tác ghi đè toàn bộ gói và không hoàn tác được, phải sao lưu dữ liệu giá '
            'TRƯỚC khi bấm Lưu lần đầu.',
            'Sao lưu sau khi đã lưu là không còn giá trị gốc để đối chiếu.',
        ]),
    ],
)

SCREENS = [PRICE]
