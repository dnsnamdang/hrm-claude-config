# -*- coding: utf-8 -*-
"""Cau hinh 3 man danh muc Tai chinh dung chung cho gen_srs / gen_testcase / gen_hdsd.

Doc code 17/08/2026:
  BE  Modules/Finance/Routes/api.php (122-147) — moi man 1 quyen "Quan ly danh muc <X>"
      Modules/Finance/Http/Requests/{WorkRequest,CostDebtRequest,SourceCapitalRequest}.php
      Modules/Finance/Entities/{Work,CostDebt}.php  -> canDelete()
      Modules/Finance/Http/Controllers/V1/SourceCapitalController.php -> destroy() = blockSourceCapital()
  FE  hrm-client/pages/finance/{works,cost-debts,source-capitals}/index.vue + *Modal.vue
  Anh that: fin_shots/ (cong dev hrm-crm.eteksofts.com, 17/08/2026)
"""

HOST = 'http://hrm-crm.eteksofts.com'

SCREENS = [

    # ============================================================ VỤ VIỆC
    dict(
        key='works',
        ten='Danh mục vụ việc',
        doi_tuong='vụ việc',
        route='/finance/works',
        quyen='Quản lý danh mục vụ việc',
        co_ma=True,
        co_trangthai=True,
        xoa_mem=False,
        dieu_kien_xoa='chưa phát sinh ở bút toán kế toán nào',
        loi_trung='Mã vụ việc đã tồn tại',
        muc_dich=[
            'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý danh mục vụ việc.',
            'Là căn cứ nghiệm thu chức năng và phân quyền.',
            'Làm rõ điều kiện được phép xóa: chỉ vụ việc chưa phát sinh ở bút toán kế toán nào '
            'mới hiện nút Xóa.',
            'Làm rõ khác biệt giữa Xóa và chuyển trạng thái Khóa.',
        ],
        thuat_ngu=[
            ('Vụ việc', 'Đối tượng tập hợp chi phí và doanh thu trong kế toán, dùng để theo dõi '
                        'hiệu quả của từng công việc hoặc từng hợp đồng.'),
            ('Mã vụ việc', 'Mã do người dùng tự đặt, duy nhất trên toàn hệ thống, dùng để chọn '
                           'nhanh khi lập bút toán.'),
            ('Trạng thái Hoạt động', 'Vụ việc còn chọn được khi lập bút toán mới.'),
            ('Trạng thái Khóa', 'Vụ việc không còn chọn được ở nghiệp vụ mới nhưng vẫn nằm trong '
                                'danh mục và các bút toán cũ vẫn giữ nguyên.'),
            ('Bút toán kế toán', 'Dòng hạch toán trong sổ kế toán có gắn vụ việc này.'),
        ],
        cot=[
            ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
            ('Mã vụ việc', 'Mã do người dùng đặt. Luôn hiển thị, sắp xếp được.'),
            ('Tên vụ việc', 'Tên đầy đủ, sắp xếp được.'),
            ('Ghi chú', 'Mặc định ẩn.'),
            ('Người sửa', 'Mặc định ẩn.'),
            ('Ngày cập nhật', 'Mặc định ẩn, sắp xếp được.'),
            ('Người tạo', 'Người đã thêm bản ghi.'),
            ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
            ('Trạng thái', 'Hoạt động hoặc Khóa.'),
            ('Hành động', 'Sửa, Xóa và Lịch sử — hiện thẳng trên cột, không có nút ba chấm.'),
        ],
        loc=[
            ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
             'Tìm theo mã vụ việc và tên vụ việc.'),
            ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Trống',
             'Bỏ trống thì hiện cả hai trạng thái.'),
            ('Người lập', 'Dropdown', 'Danh sách nhân viên', 'Trống',
             'Lọc theo người đã tạo bản ghi.'),
            ('Người cập nhật', 'Dropdown', 'Danh sách nhân viên', 'Trống',
             'Lọc theo người sửa gần nhất.'),
        ],
        truong=[
            ('Mã vụ việc', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Duy nhất toàn hệ thống. Gợi ý nhập dạng VV001. Bỏ trống báo “Bắt buộc phải nhập”; '
             'trùng báo “Mã vụ việc đã tồn tại”.'),
            ('Tên vụ việc', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Bỏ trống báo “Bắt buộc phải nhập”.'),
            ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
             'Chọn Khóa để ngừng sử dụng vụ việc ở nghiệp vụ mới.'),
            ('Ghi chú', 'Textarea', '–', 'Không', 'Trống', 'Ghi chú tự do, 3 dòng.'),
        ],
        shots=dict(
            danhsach='works_01_danhsach.png',
            boloc='works_02_boloc.png',
            taomoi='works_03_taomoi.png',
            validate='works_04_validate.png',
            xoa='works_05_xacnhan_xoa.png',
            lichsu='works_06_lichsu.png',
        ),
    ),

    # ============================================================ MÃ PHÍ
    dict(
        key='cost_debts',
        ten='Danh mục mã phí',
        doi_tuong='mã phí',
        route='/finance/cost-debts',
        quyen='Quản lý danh mục mã phí',
        co_ma=True,
        co_trangthai=True,
        xoa_mem=False,
        dieu_kien_xoa='chưa phát sinh ở bút toán kế toán nào',
        loi_trung='Mã phí đã tồn tại',
        muc_dich=[
            'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý danh mục mã phí.',
            'Là căn cứ nghiệm thu chức năng và phân quyền.',
            'Làm rõ điều kiện được phép xóa: chỉ mã phí chưa phát sinh ở bút toán kế toán nào '
            'mới hiện nút Xóa.',
            'Làm rõ khác biệt giữa Xóa và chuyển trạng thái Khóa.',
        ],
        thuat_ngu=[
            ('Mã phí', 'Mã phân loại khoản phí trong kế toán, dùng để tập hợp và đối chiếu chi '
                       'phí theo từng loại.'),
            ('Trạng thái Hoạt động', 'Mã phí còn chọn được khi lập bút toán mới.'),
            ('Trạng thái Khóa', 'Mã phí không còn chọn được ở nghiệp vụ mới nhưng vẫn nằm trong '
                                'danh mục và các bút toán cũ vẫn giữ nguyên.'),
            ('Bút toán kế toán', 'Dòng hạch toán trong sổ kế toán có gắn mã phí này.'),
        ],
        cot=[
            ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
            ('Mã phí', 'Mã do người dùng đặt. Luôn hiển thị, sắp xếp được.'),
            ('Tên mã phí', 'Tên đầy đủ, sắp xếp được.'),
            ('Ghi chú', 'Mặc định ẩn.'),
            ('Người sửa', 'Mặc định ẩn.'),
            ('Ngày cập nhật', 'Mặc định ẩn, sắp xếp được.'),
            ('Người tạo', 'Người đã thêm bản ghi.'),
            ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
            ('Trạng thái', 'Hoạt động hoặc Khóa.'),
            ('Hành động', 'Sửa, Xóa và Lịch sử — hiện thẳng trên cột, không có nút ba chấm.'),
        ],
        loc=[
            ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
             'Tìm theo mã phí và tên mã phí.'),
            ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Trống',
             'Bỏ trống thì hiện cả hai trạng thái.'),
            ('Người lập', 'Dropdown', 'Danh sách nhân viên', 'Trống',
             'Lọc theo người đã tạo bản ghi.'),
            ('Người cập nhật', 'Dropdown', 'Danh sách nhân viên', 'Trống',
             'Lọc theo người sửa gần nhất.'),
        ],
        truong=[
            ('Mã phí', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Duy nhất toàn hệ thống. Gợi ý nhập dạng MP001. Bỏ trống báo “Bắt buộc phải nhập”; '
             'trùng báo “Mã phí đã tồn tại”.'),
            ('Tên mã phí', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Bỏ trống báo “Bắt buộc phải nhập”.'),
            ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
             'Chọn Khóa để ngừng sử dụng mã phí ở nghiệp vụ mới.'),
            ('Ghi chú', 'Textarea', '–', 'Không', 'Trống', 'Ghi chú tự do, 3 dòng.'),
        ],
        shots=dict(
            danhsach='costdebts_01_danhsach.png',
            boloc='costdebts_02_boloc.png',
            taomoi='costdebts_03_taomoi.png',
            xoa='costdebts_04_xacnhan_xoa.png',
            lichsu='costdebts_05_lichsu.png',
        ),
    ),

    # ============================================================ NGUỒN VỐN
    dict(
        key='source_capitals',
        ten='Danh mục nguồn vốn',
        doi_tuong='nguồn vốn',
        route='/finance/source-capitals',
        quyen='Quản lý danh mục nguồn vốn',
        co_ma=False,
        co_trangthai=False,
        xoa_mem=True,
        dieu_kien_xoa=None,
        loi_trung='Tên nguồn vốn đã tồn tại',
        muc_dich=[
            'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý danh mục nguồn vốn.',
            'Là căn cứ nghiệm thu chức năng và phân quyền.',
            'Làm rõ đặc thù của màn: chỉ có một trường nhập duy nhất, không có mã, không có cột '
            'Trạng thái trên lưới.',
            'Làm rõ thao tác Xóa thực chất là ngừng sử dụng, dữ liệu không mất hẳn.',
        ],
        thuat_ngu=[
            ('Nguồn vốn', 'Nguồn hình thành vốn của khoản chi hoặc tài sản, ví dụ vốn tự có, '
                          'vốn vay ngân hàng.'),
            ('Xóa', 'Trên màn này, xóa là chuyển bản ghi sang trạng thái ngừng sử dụng ở phía '
                    'máy chủ. Bản ghi biến mất khỏi danh sách nhưng dữ liệu không mất hẳn.'),
        ],
        cot=[
            ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
            ('Tên nguồn vốn', 'Tên đầy đủ. Luôn hiển thị, sắp xếp được.'),
            ('Người tạo', 'Người đã thêm bản ghi.'),
            ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
            ('Hành động', 'Sửa, Xóa và Lịch sử.'),
        ],
        loc=[
            ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
             'Tìm theo tên nguồn vốn. Màn hình KHÔNG có bộ lọc nâng cao nào khác.'),
        ],
        truong=[
            ('Tên nguồn vốn', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
             'Duy nhất toàn hệ thống. Bỏ trống báo “Bắt buộc phải nhập”; trùng báo '
             '“Tên nguồn vốn đã tồn tại”.'),
        ],
        shots=dict(
            danhsach='sourcecapitals_01_danhsach.png',
            taomoi='sourcecapitals_02_taomoi.png',
            xoa='sourcecapitals_03_xacnhan_xoa.png',
            lichsu='sourcecapitals_04_lichsu.png',
        ),
    ),
]
