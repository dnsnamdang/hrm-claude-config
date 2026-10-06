# -*- coding: utf-8 -*-
# Cấu hình tài liệu màn Danh mục dịch vụ sửa chữa và chi phí khác (phân hệ CSKH sau bán).
# Nguồn: code gop_db 25/09/2026 — FE pages/customer-care/costs/index.vue, components/modal/customer-care/cost-modal.vue;
# BE Modules/CustomerCare (CostController, CostService, CostRequest, CostResource, Entities/Cost/Cost.php),
# app/ExcelExport/ExportColumnRegistry.php ('costs'). Không ghi URL. Chữ UI / message lấy nguyên văn code.

DT = 'dịch vụ / chi phí'

_TRUONG_XUAT = 'Tên dịch vụ / chi phí, Phân loại, ĐM giảm giá, % Tính giá vốn, % VAT, Trạng thái, Người tạo, Ngày tạo'

CFG = {
    'slug': 'costs',
    'ten': 'Danh mục dịch vụ sửa chữa và chi phí khác',
    'doi_tuong': DT,
    'file_hdsd': 'HDSD_Danh muc dich vu sua chua va chi phi khac.docx',
    'file_srs': 'SRS - Danh mục dịch vụ sửa chữa và chi phí khác.docx',
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Dịch vụ sửa chữa và chi phí khác', 'menu_muc')],

    'thuat_ngu': [
        ['Dịch vụ sửa chữa', 'Hạng mục dịch vụ do đơn vị cung cấp, có tính doanh thu (ô “Dịch vụ có tính doanh thu” được tích).'],
        ['Chi phí khác', 'Khoản chi phí phát sinh trong hoạt động dịch vụ, không tính doanh thu (ô “Dịch vụ có tính doanh thu” không tích).'],
        ['Phân loại', 'Cột cho biết dòng danh mục là “Dịch vụ có tính doanh thu” hay “Chi phí khác”.'],
        ['% Tính giá vốn', 'Tỷ lệ phần trăm dùng để tính giá vốn của dịch vụ.'],
        ['% VAT', 'Thuế suất giá trị gia tăng áp cho dịch vụ / chi phí, từ 0 đến 100.'],
        ['ĐM giảm giá', 'Định mức giảm giá (%), khai báo RIÊNG cho từng công ty. Màn hình luôn hiển thị và ghi mức của công ty đang chọn.'],
        ['Chi phí hệ thống', 'Hai dòng “Chi phí đi lại” và “Chi phí vận chuyển” — không sửa, không xóa, không khóa / mở khóa được.'],
        ['Đã được sử dụng', 'Dịch vụ / chi phí đã được chọn ở ít nhất một chứng từ hoặc nghiệp vụ khác (xem Quy tắc xóa). Dòng đã được sử dụng KHÔNG xóa được (nút Xóa bị ẩn); muốn ngừng dùng thì Khóa.'],
        ['Trạng thái Hoạt động', 'Dòng danh mục đang dùng được ở các nghiệp vụ khác.'],
        ['Trạng thái Khóa', 'Ngừng sử dụng: không sửa, không xóa được; vẫn nằm trong danh mục và vẫn xem được chi tiết, lịch sử.'],
    ],
    'phien_ban': [
        ['1.0', '12/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục dịch vụ sửa chữa và chi phí khác.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: bộ lọc gọn một hàng có nhãn nổi, tách cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật, nút Khóa / Mở khóa và Lịch sử chuyển về cột Hành động (nút ba chấm), bấm tên để xem chi tiết, cửa sổ Chọn trường xuất file, bổ sung Import Excel, Tùy chỉnh cột, ô Trạng thái trong cửa sổ Tạo/Sửa; trình bày theo mẫu tài liệu danh mục chung.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bỏ cơ chế “Xóa dòng đã phát sinh chứng từ thì chuyển sang Khóa”: dòng đã được sử dụng ở bất kỳ chứng từ nào thì ẩn nút Xóa và máy chủ chặn xóa; dòng chưa dùng thì xóa hẳn. Khóa / Mở khóa là thao tác riêng, khóa được cả dòng đang được sử dụng; dòng đang Khóa bị chặn sửa / xóa. File Xuất Excel đã có dữ liệu ở cột Phân loại và Trạng thái.'],
    ],
    'muc_dich': [
        'Danh mục dịch vụ sửa chữa và chi phí khác dùng để khai báo và quản lý các dịch vụ sửa chữa cùng các khoản chi phí khác phát sinh trong hoạt động dịch vụ. Mỗi dòng khai báo ba thông số dùng cho các nghiệp vụ phía sau: % Tính giá vốn, % VAT và ĐM giảm giá (định mức giảm giá theo từng công ty).',
        'Danh mục là nguồn dữ liệu cho nhiều chứng từ phía sau (Báo giá hãng, Hợp đồng hãng, báo giá / hợp đồng dịch vụ, đề nghị mua, hạch toán dịch vụ…). Vì vậy dòng đã được sử dụng không xóa được — nút Xóa bị ẩn; muốn ngừng dùng thì Khóa. Xóa là xóa HẲN và chỉ áp cho dòng chưa được sử dụng ở đâu.',
    ],
    'quyen': {
        'truoc': ['Màn hình gắn với 2 quyền. Tài khoản có thể có một trong hai, hoặc cả hai. Không có quyền nào thì mục menu bị ẩn và hệ thống không trả dữ liệu.'],
        'rows': [
            ['Quản lý dịch vụ sửa chữa và chi phí khác', 'Xem danh sách, xem chi tiết, Tạo mới, Sửa, Xóa, Khóa, Mở khóa, Import Excel, Xuất Excel, xem lịch sử.'],
            ['Xem dịch vụ sửa chữa và chi phí khác', 'Chỉ xem danh sách, xem chi tiết, tìm kiếm, Xuất Excel và xem lịch sử. Không thấy nút Tạo mới, Import Excel, Sửa, Xóa, Khóa / Mở khóa.'],
        ],
        'sau': ['Màn hình KHÔNG phân quyền theo cấp công ty / phòng ban: mọi tài khoản có quyền đều thấy toàn bộ danh mục. Công ty đang chọn chỉ quyết định giá trị cột ĐM giảm giá.'],
    },

    'danh_sach': {
        'mo_ta_vao': 'Hệ thống hiển thị danh sách dịch vụ / chi phí, mặc định 10 dòng mỗi trang, dòng mới tạo nằm trên cùng.',
        'bo_cuc': [
            'Khu vực tìm kiếm và lọc — một hàng gồm ô tìm kiếm nhanh, ô Phân loại, ô Trạng thái, nút Tìm kiếm và Làm mới.',
            'Thanh công cụ — nút Tạo mới, nút Xuất Excel, nút Import Excel và biểu tượng Cấu hình cột hiển thị.',
            'Bảng danh sách — các cột thông tin, cột Hành động ở cuối, và phân trang bên dưới.',
        ],
        'cot': [
            ['STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'],
            ['Tên dịch vụ / chi phí', 'Tên khai báo. Luôn hiển thị, sắp xếp được. Bấm vào tên để mở cửa sổ Xem dịch vụ / chi phí.'],
            ['Phân loại', '“Dịch vụ có tính doanh thu” hoặc “Chi phí khác”. Mặc định ẩn.'],
            ['ĐM giảm giá', 'Định mức giảm giá (%) của CÔNG TY ĐANG CHỌN, chưa khai báo thì để trống. Mặc định ẩn.'],
            ['% Tính giá vốn', 'Tỷ lệ tính giá vốn, hiển thị gọn (vd 80%). Mặc định ẩn.'],
            ['% VAT', 'Thuế suất VAT, hiển thị gọn (vd 8%). Mặc định ẩn.'],
            ['Người cập nhật', 'Họ tên người sửa gần nhất. Mặc định ẩn.'],
            ['Ngày cập nhật', 'Thời điểm sửa gần nhất, dạng dd/mm/yyyy hh:mm. Mặc định ẩn, sắp xếp được.'],
            ['Người tạo', 'Họ tên người đã thêm bản ghi.'],
            ['Ngày tạo', 'Thời điểm thêm, dạng dd/mm/yyyy hh:mm, sắp xếp được.'],
            ['Trạng thái', 'Nhãn Hoạt động hoặc Khóa.'],
            ['Hành động', 'Các nút thao tác của dòng (xem mục 4).'],
        ],
        'hanh_dong': {
            'intro': 'Trên mỗi dòng, cột Hành động có các nút:',
            'bullets': [
                'Biểu tượng bút chì {icon:btn_sua} — mở cửa sổ Sửa dịch vụ / chi phí. Chỉ hiện với người có quyền Quản lý, khi dòng đang Hoạt động và không phải chi phí hệ thống.',
                'Biểu tượng thùng rác {icon:btn_xoa} — xóa HẲN dòng. Chỉ hiện với người có quyền Quản lý, khi dòng đang Hoạt động, không phải chi phí hệ thống và CHƯA được sử dụng ở bất kỳ chứng từ nào.',
                'Khóa / Mở khóa — đổi trạng thái. Chỉ hiện với người có quyền Quản lý và không áp cho chi phí hệ thống. Khóa được cả dòng đang được sử dụng.',
                'Lịch sử — mở cửa sổ Lịch sử thay đổi. Luôn hiện.',
                'Có từ 4 nút trở lên thì 2 nút đầu hiện thẳng, các nút còn lại nằm trong nút ba chấm {icon:btn_bacham} “Hành động khác”.',
            ],
            'anh': 'Các nút ở cột Hành động của một dịch vụ / chi phí',
            'luu_y': ['Lưu ý quan trọng: nút không dùng được thì BIẾN MẤT, không hiện mờ. Dòng ĐÃ KHÓA chỉ còn Mở khóa và Lịch sử; dòng đã được sử dụng không có nút Xóa (chỉ còn Sửa, Khóa, Lịch sử); hai chi phí hệ thống “Chi phí đi lại”, “Chi phí vận chuyển” chỉ còn Lịch sử; người chỉ có quyền Xem chỉ thấy Lịch sử.'],
        },
        'phan_trang': [
            'Cuối bảng có dòng “Hiển thị a–b / N”: N là tổng số dịch vụ / chi phí khớp bộ lọc đang áp dụng, không phải tổng toàn danh mục.',
            'Ô Số dòng/trang có các mức 5, 10, 20, 50, 100 (mặc định 10). Đổi số dòng thì hệ thống tự quay về trang 1.',
            'Các cột sắp xếp được: Tên dịch vụ / chi phí, Ngày tạo, Ngày cập nhật. Bấm tiêu đề cột để sắp xếp, bấm lần hai để đảo chiều. Thứ tự sắp xếp được giữ nguyên khi chuyển trang.',
            'Bộ lọc đang áp dụng được ghi nhớ trong 10 phút: rời màn rồi quay lại trong khoảng thời gian này thì các tiêu chí cũ vẫn còn.',
        ],
        'them': [
            ('p', 'Cột ĐM giảm giá khai báo riêng cho từng công ty: cùng một dịch vụ, người dùng của công ty A và công ty B có thể thấy hai mức khác nhau — đó là hành vi đúng, không phải lỗi dữ liệu.'),
        ],
    },

    'loc': {
        'buoc2': 'Bước 2: Nhập chữ vào ô tìm kiếm nhanh hoặc chọn giá trị ở ô Phân loại, Trạng thái.',
        'rows': [
            ['Ô tìm kiếm nhanh', 'Placeholder “Tìm theo tên dịch vụ / chi phí...”. Tìm theo TÊN (gõ một phần tên cũng ra). Nhấn Enter hoặc bấm Tìm kiếm để lọc — gõ xong chưa bấm thì danh sách chưa đổi.'],
            ['Phân loại', '“Dịch vụ có tính doanh thu” hoặc “Chi phí khác”. Bỏ trống thì hiện cả hai. Lọc ngay khi chọn.'],
            ['Trạng thái', 'Hoạt động hoặc Khóa. Bỏ trống thì hiện cả hai trạng thái. Lọc ngay khi chọn.'],
        ],
        'ap_dung': [
            'Các tiêu chí kết hợp với nhau theo kiểu VÀ — chỉ bản ghi thỏa đồng thời tất cả các tiêu chí mới hiện ra. Mỗi lần đổi tiêu chí, danh sách quay về trang 1.',
            'Bấm {icon:btn_lammoi} để xóa toàn bộ tiêu chí; danh sách nạp lại đầy đủ ngay lập tức.',
        ],
        'anh_ket_qua': 'Kết quả tìm nhanh theo tên (gõ “Thiết kế”)',
    },

    'form': {
        'kieu': 'popup',
        'buoc_tao': [
            'Bước 1: Truy cập vào màn hình Danh mục dịch vụ sửa chữa và chi phí khác.',
            'Bước 2: Bấm {icon:btn_taomoi}. Hệ thống mở cửa sổ “Thêm dịch vụ / chi phí”.',
            'Bước 3: Nhập/ chọn thông tin: Tên dịch vụ / chi phí, % Tính giá vốn, % VAT, ĐM giảm giá (%), Trạng thái; giữ hoặc bỏ tích “Dịch vụ có tính doanh thu”.',
            'Bước 4: Bấm {icon:btn_luu} để lưu và đóng cửa sổ, hoặc {icon:btn_luutieptuc} để lưu rồi nhập tiếp dòng khác.',
        ],
        'anh_tao': 'Cửa sổ Thêm dịch vụ / chi phí',
        'truong': [
            ['Tên dịch vụ / chi phí', 'Ô nhập giá trị', 'Có', 'Trống', 'Tối đa 255 ký tự. Không trùng tên đã có (kể cả dòng đang Khóa). Bỏ trống báo “Bắt buộc phải nhập”; trùng báo “Đã tồn tại trên hệ thống”.'],
            ['% Tính giá vốn', 'Ô nhập số', 'Có', 'Trống', 'Không nhỏ hơn 0. Nhập chữ báo “Phải là số”; số âm báo “Không được nhỏ hơn 0”.'],
            ['% VAT', 'Ô nhập số', 'Có', 'Trống', 'Từ 0 đến 100. Lớn hơn 100 báo “Tối đa 100”.'],
            ['ĐM giảm giá (%)', 'Ô nhập số', 'Không', 'Trống', 'Từ 0 đến 100. Bỏ trống hoặc nhập 0 nghĩa là công ty đang chọn không có định mức giảm giá. Giá trị lưu riêng cho công ty đang chọn.'],
            ['Trạng thái', 'Ô chọn giá trị', 'Không', 'Hoạt động', 'Chỉ chọn 1 trong 2 giá trị: Hoạt động / Khóa.'],
            ['Dịch vụ có tính doanh thu', 'Ô tích chọn', 'Không', 'Đã tích', 'Tích = “Dịch vụ có tính doanh thu”; bỏ tích = “Chi phí khác”.'],
        ],
        'sau_truong': ['Số thập phân nhập bằng dấu chấm, ví dụ 12.5.'],
        'nut': [
            ['Lưu', 'Ghi bản ghi rồi đóng cửa sổ, báo “Thêm mới thành công” (hoặc “Cập nhật thành công” khi sửa) và nạp lại danh sách.'],
            ['Lưu và tiếp tục', 'Ghi bản ghi nhưng GIỮ cửa sổ mở và xóa trắng các ô để nhập tiếp. Chỉ có khi Tạo mới.'],
            ['Đóng', 'Đóng cửa sổ, không ghi gì. Nếu đã nhập dở, hệ thống hỏi “Thông tin chưa lưu” — “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại).'],
        ],
        'loi': [
            ['Bắt buộc phải nhập', 'Bỏ trống Tên dịch vụ / chi phí, % Tính giá vốn hoặc % VAT.'],
            ['Đã tồn tại trên hệ thống', 'Tên trùng với dịch vụ / chi phí đã có (kể cả dòng đang Khóa).'],
            ['Vui lòng nhập tối đa 255 ký tự.', 'Tên quá dài.'],
            ['Phải là số', 'Nhập chữ vào ô % Tính giá vốn, % VAT hoặc ĐM giảm giá.'],
            ['Không được nhỏ hơn 0', 'Nhập số âm vào ô phần trăm.'],
            ['Tối đa 100', '% VAT hoặc ĐM giảm giá lớn hơn 100.'],
            ['Bạn chưa nhập đầy đủ thông tin', 'Thông báo chung khi còn ô bị lỗi; xem các ô báo đỏ trong cửa sổ.'],
        ],
    },

    'sua': {
        'buoc': [
            'Bước 1: Truy cập vào màn hình Danh mục dịch vụ sửa chữa và chi phí khác.',
            'Bước 2: Bấm nút {icon:btn_sua} ở cột Hành động của dòng cần sửa.',
            'Bước 3: Hệ thống hiển thị cửa sổ “Sửa dịch vụ / chi phí” với dữ liệu hiện tại.',
            'Bước 4: Cập nhật các thông tin cần sửa (quy tắc nhập như Thêm mới).',
            'Bước 5: Bấm {icon:btn_luu} để xác nhận thay đổi hoặc Đóng nếu muốn hủy.',
        ],
        'anh': 'Cửa sổ Sửa dịch vụ / chi phí',
        'ghi_chu': [
            'Giữ nguyên tên của chính dòng đang sửa thì không bị báo trùng.',
            'Xóa trắng ô ĐM giảm giá hoặc nhập 0 rồi Lưu: hệ thống gỡ định mức giảm giá của CÔNG TY ĐANG CHỌN; định mức của các công ty khác không bị ảnh hưởng.',
            'Dòng đang Khóa và hai chi phí hệ thống không có nút Sửa. Nếu dòng vừa bị người khác khóa, bấm Lưu sẽ nhận thông báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”',
            'Sửa xong, cột Người cập nhật / Ngày cập nhật của dòng đó đổi sang người đang đăng nhập và thời điểm hiện tại.',
        ],
    },
    'xoa': {
        'buoc': [
            'Bước 1: Ở cột Hành động của dòng cần xóa, Người dùng bấm {icon:btn_xoa}.',
            'Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa” — “Bạn có chắc muốn xóa \'…\'?”.',
            'Bước 3: Bấm {icon:btn_confirm_xoa}: hệ thống báo “Xóa thành công”, dòng biến mất khỏi danh sách (xóa HẲN), định mức giảm giá của mọi công ty cũng bị xóa theo. Bấm {icon:btn_huy} nếu bấm nhầm, không có gì thay đổi.',
        ],
        'anh': 'Hộp xác nhận xóa dịch vụ / chi phí',
        'ghi_chu': [
            'Nút Xóa CHỈ hiện khi dòng đang Hoạt động, không phải chi phí hệ thống và CHƯA được sử dụng ở bất kỳ chứng từ, nghiệp vụ nào. Dòng đã được sử dụng không có nút Xóa (ẩn hẳn, không hiện mờ) — muốn ngừng dùng thì Khóa.',
            'Được coi là “đã sử dụng” khi dịch vụ / chi phí đã được chọn ở: Báo giá hãng, Hợp đồng hãng; báo giá, hợp đồng, phụ lục hợp đồng bán hàng / dịch vụ / dự án; đề nghị mua, hợp đồng mua trong nước và nhập khẩu, hóa đơn mua hàng, tờ khai hải quan, chi phí nhập khẩu; đề nghị xuất dịch vụ, đề nghị hạch toán và hạch toán dịch vụ; BOM, tính giá sản phẩm, phân tích dự án, sản xuất; Danh mục công việc, lỗi thiết bị; báo giá, hợp đồng dịch vụ, phiếu giao việc, nhập kết quả, hạch toán dịch vụ bảo hành – sửa chữa; đề nghị thanh toán và báo cáo bảo hành; tổng hợp lắp đặt; đề nghị khác.',
            'Nếu trong lúc đang mở hộp xác nhận, dịch vụ / chi phí vừa được dùng ở một chứng từ, bấm Xóa sẽ nhận thông báo “Dịch vụ/chi phí đang được sử dụng, không thể xóa.” và dòng vẫn còn. Nếu dòng vừa bị người khác khóa, thông báo là “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”',
        ],
    },
    'khoa': {
        'y_nghia': [
            'Bản ghi VẪN nằm trong danh sách, cột Trạng thái hiện chữ Khóa.',
            'Vẫn xem được chi tiết và lịch sử thay đổi của bản ghi.',
            'Khóa / Mở khóa CHỈ đổi trạng thái, không đụng tới thông số khác; định mức giảm giá đã khai báo vẫn giữ nguyên, mở khóa lại là dữ liệu cũ còn đầy đủ.',
            'Nút Sửa và Xóa của dòng đó biến mất; muốn sửa hay xóa phải Mở khóa trước. Nếu gọi thẳng chức năng Sửa / Xóa trên dòng đang Khóa, hệ thống chặn và báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”',
            'Khóa được CẢ dòng đang được sử dụng ở chứng từ — đây là cách ngừng dùng một dịch vụ / chi phí không xóa được. Chứng từ đã lập vẫn giữ nguyên tên và thông số.',
        ],
        'buoc_khoa': [
            'Bước 1: Ở cột Hành động, Người dùng chọn Khóa (trong nút ba chấm nếu dòng có nhiều nút).',
            'Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận khóa” — “Bạn có chắc muốn khóa \'…\'?”. Bấm Khóa để xác nhận; hệ thống báo “Khóa thành công”, cột Trạng thái đổi thành Khóa. Bấm Hủy nếu bấm nhầm.',
        ],
        'buoc_mo': [
            'Bước 1: Ở cột Hành động của dòng đang Khóa, Người dùng chọn Mở khóa.',
            'Bước 2: Hộp xác nhận “Xác nhận mở khóa” — “Bạn có chắc muốn mở khóa \'…\'?”. Bấm Mở khóa: hệ thống báo “Mở khóa thành công”, cột Trạng thái đổi thành Hoạt động. Bấm Hủy nếu bấm nhầm.',
        ],
        'ghi_chu': [
            'Có thể khóa ngay trong cửa sổ Sửa bằng cách chọn Trạng thái = Khóa rồi Lưu.',
            'Hai chi phí hệ thống “Chi phí đi lại” và “Chi phí vận chuyển” không khóa và không mở khóa được.',
        ],
    },
    'lich_su': {
        'buoc': [
            'Xem từ màn danh sách: ở cột Hành động, Người dùng chọn Lịch sử.',
            'Xem từ màn chi tiết: bấm vào tên dịch vụ / chi phí để mở cửa sổ Xem dịch vụ / chi phí, khối Lịch sử nằm ở cuối cửa sổ.',
        ],
        'ghi_chu': [
            'Khóa, Mở khóa (kể cả đổi Trạng thái trong cửa sổ Sửa) được ghi là thay đổi trạng thái. Thay đổi ĐM giảm giá cũng được ghi lại.',
            'Cửa sổ có bộ lọc riêng (loại hành động, người thực hiện, khoảng thời gian) để thu hẹp danh sách khi bản ghi có nhiều lần thay đổi.',
        ],
    },
    'chi_tiet': {
        'buoc': ['Bước 1: Truy cập vào màn hình Danh mục dịch vụ sửa chữa và chi phí khác.',
                 'Bước 2: Bấm vào tên ở cột Tên dịch vụ / chi phí. Hệ thống mở cửa sổ “Xem dịch vụ / chi phí”.'],
        'ghi_chu': ['Cửa sổ hiển thị đủ các trường như cửa sổ Sửa ở chế độ chỉ đọc (không gõ được, không có nút Lưu, chỉ có nút Đóng), kèm khối Lịch sử ở cuối. Dùng được với cả người chỉ có quyền Xem, và với cả dòng đang Khóa.'],
    },
    'xuat': {
        'buoc': [
            'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 2). File xuất chạy theo đúng bộ lọc và thứ tự sắp xếp đang áp dụng.',
            'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ “Chọn trường xuất file”.',
            'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất. Mặc định hệ thống tích sẵn đúng những cột đang hiển thị trên bảng.',
            'Bước 4: Bấm {icon:btn_xuatfile}. Hệ thống tải về file danh_muc_dich_vu_sua_chua_va_chi_phi_khac.xlsx và báo “Xuất Excel thành công”.',
        ],
        'truong': 'Chọn nhiều trường: ' + _TRUONG_XUAT + '.',
        'ghi_chu': [
            'Lưu ý: file xuất chứa TOÀN BỘ kết quả của bộ lọc, không chỉ các dòng của trang đang xem. Cột STT luôn có ở đầu file.',
            'Nút Xuất Excel dùng được với cả người chỉ có quyền Xem. Cột ĐM giảm giá trong file là mức của công ty đang chọn, để trống nếu chưa khai báo.',
        ],
    },
    'import': {
        'tieu_de': 'Import dịch vụ sửa chữa và chi phí khác',
        'file': 'Mau_import_dich_vu_sua_chua.xlsx',
        'cot_text': 'Tên dịch vụ / chi phí (bắt buộc), % Tính giá vốn (bắt buộc), % VAT (bắt buộc), ĐM giảm giá (%), Có tính doanh thu (chọn Có / Không trong danh sách sổ xuống)',
        'toast': 'Import thành công N dịch vụ sửa chữa và chi phí khác.',
        'loi': [
            ['Tên dịch vụ / chi phí không được để trống', 'Dòng đó bỏ trống cột Tên dịch vụ / chi phí.'],
            ['Tên dịch vụ / chi phí tối đa 255 ký tự', 'Tên quá dài, rút gọn lại.'],
            ['Tên dịch vụ / chi phí bị trùng với dòng N trong file', 'Trong chính file có hai dòng cùng tên. Xóa bớt một dòng.'],
            ['Tên dịch vụ / chi phí đã tồn tại trong hệ thống', 'Danh mục đã có dịch vụ / chi phí trùng tên (kể cả dòng đang Khóa).'],
            ['% Tính giá vốn không được để trống', 'Dòng đó bỏ trống cột % Tính giá vốn.'],
            ['% Tính giá vốn không hợp lệ', 'Cột % Tính giá vốn không phải là số.'],
            ['% Tính giá vốn phải nằm trong khoảng 0 - 100', 'Giá trị âm hoặc lớn hơn 100.'],
            ['% VAT không được để trống', 'Dòng đó bỏ trống cột % VAT.'],
            ['% VAT không hợp lệ', 'Cột % VAT không phải là số.'],
            ['% VAT phải nằm trong khoảng 0 - 100', 'Giá trị âm hoặc lớn hơn 100.'],
            ['ĐM giảm giá (%) không hợp lệ', 'Cột ĐM giảm giá (%) không phải là số.'],
            ['ĐM giảm giá (%) phải nằm trong khoảng 0 - 100', 'Giá trị âm hoặc lớn hơn 100.'],
        ],
        'ghi_chu': [
            'Lưu ý: dòng nhập từ Excel luôn được tạo ở trạng thái Hoạt động, người tạo là chính người thực hiện nhập. Cột Có tính doanh thu để trống hoặc ghi Không thì dòng đó thuộc loại “Chi phí khác”. ĐM giảm giá (nếu có) được ghi cho công ty đang chọn.',
            'Mỗi lần nhập tối đa 500 dòng; file dài hơn hệ thống báo “File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần.” Nút Import Excel chỉ hiện với người có quyền Quản lý.',
        ],
    },
    'tuy_chinh_cot': {'cot_khoa': 'Ba cột STT, Tên dịch vụ / chi phí và Hành động'},

    'shots': {'list': '01_list.png', 'rowmenu': '03_rowmenu.png', 'filter': 'filter.png', 'filter_result': '04_filter_result.png',
              'create': '10_create.png', 'create_error': '11_create_error.png', 'edit': '12_edit.png',
              'delete': '13_delete.png', 'lock': '14_lock.png', 'unlock': '15_unlock.png', 'history': '16_history.png',
              'detail': '17_detail.png', 'export': '20_export.png', 'import_open': '21_import_open.png',
              'import_loaded': '22_import_loaded.png', 'import_validated': '23_import_validated.png', 'colcfg': '25_colcfg.png'},

    'capture': {'route': '/customer-care/costs',
                'menu': {'phanhe': 'CSKH SAU BÁN', 'nhom': 'Danh mục', 'muc': 'Dịch vụ sửa chữa và chi phí khác'},
                'search': 'Tìm theo tên dịch vụ', 'searchText': 'Thiết kế', 'detailCol': 1,
                'lockName': 'Thiết kế máng cáp',
                'create': True, 'lock': True},

    'import_test': {
        'cols': ['Tên dịch vụ / chi phí *', '% Tính giá vốn *', '% VAT *', 'ĐM giảm giá (%)', 'Có tính doanh thu'],
        'rows': [
            ['DOC-Thay dầu máy nén khí', '70', '8', '5', 'Có'],
            ['DOC-Vệ sinh cầu nâng', '60', '10', '', 'Có'],
            ['DOC-Chi phí lưu trú kỹ thuật', '100', '0', '', 'Không'],
            ['', '70', '8', '', 'Có'],
            ['DOC-Thay dầu máy nén khí', '70', '8', '', 'Có'],
            ['Chi phí đi lại', '50', '8', '', 'Không'],
            ['DOC-Hiệu chỉnh cảm biến', 'abc', '8', '', 'Có'],
            ['DOC-Bảo trì tủ điện', '70', '150', '120', 'Có'],
        ],
    },

    'uml': {
        'mains': [('FR-01', 'Xem danh sách dịch vụ / chi phí', 'view'), ('FR-03', 'Thêm mới dịch vụ / chi phí', 'crud'),
                  ('FR-04', 'Chỉnh sửa dịch vụ / chi phí', 'crud'), ('FR-05', 'Xóa dịch vụ / chi phí', 'action'),
                  ('FR-06', 'Khóa / Mở khóa dịch vụ / chi phí', 'action'), ('FR-08', 'Import file dịch vụ / chi phí', 'io'),
                  ('FR-09', 'Xuất danh sách ra Excel', 'io')],
        'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-10', 'Xem chi tiết dịch vụ / chi phí', 'view'),
                 ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
        'rieng': [('FR-10', 'Xem chi tiết dịch vụ / chi phí', 'view')],
    },

    'srs': {
        'muc_dich': ['Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
                     'Làm rõ quy tắc ĐM giảm giá theo từng công ty, quy tắc Xóa hẳn chỉ khi chưa được sử dụng, Khóa / Mở khóa và hai chi phí hệ thống bị chặn thao tác.'],
        'quyen_truoc': ['Màn hình gắn với 2 quyền, khai trong nhóm quyền danh mục dịch vụ. Máy chủ kiểm tra quyền ở từng chức năng, nên gọi thẳng chức năng mà bỏ qua giao diện cũng bị chặn.'],
        'quyen_rows': [['Quản lý dịch vụ sửa chữa và chi phí khác', 'Xem danh sách, xem chi tiết, Tạo mới, Sửa, Xóa, Khóa, Mở khóa, Import Excel, Xuất Excel.'],
                       ['Xem dịch vụ sửa chữa và chi phí khác', 'Xem danh sách, xem chi tiết, tìm kiếm, Xuất Excel.']],
        'ma_tran': [['Chức năng', 'Quản lý', 'Xem', 'Không có quyền']] + [
            ['FR-01 Xem danh sách', 'Có', 'Có', 'Không'],
            ['FR-02 Tìm kiếm và lọc', 'Có', 'Có', 'Không'],
            ['FR-03 Thêm mới', 'Có', 'Không', 'Không'],
            ['FR-04 Chỉnh sửa', 'Có', 'Không', 'Không'],
            ['FR-05 Xóa', 'Có', 'Không', 'Không'],
            ['FR-06 Khóa / Mở khóa', 'Có', 'Không', 'Không'],
            ['FR-07 Xem lịch sử thay đổi', 'Có', 'Có', 'Không'],
            ['FR-08 Import file', 'Có', 'Không', 'Không'],
            ['FR-09 Xuất danh sách ra Excel', 'Có', 'Có', 'Không'],
            ['FR-10 Xem chi tiết', 'Có', 'Có', 'Không'],
            ['FR-11 Tùy chỉnh cột hiển thị', 'Có', 'Có', 'Không']],
        'ma_tran_widths': [2.4, 1, 1, 1.2],
        'fr': [
            {'ten': 'Xem danh sách dịch vụ / chi phí',
             'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của Danh mục dịch vụ sửa chữa và chi phí khác.',
             'gioi_thieu': [['Tên chức năng', 'Xem danh sách dịch vụ / chi phí'],
                            ['Mô tả', 'Hiển thị toàn bộ dịch vụ sửa chữa và chi phí khác trong danh mục, có phân trang và sắp xếp.'],
                            ['Tác nhân', 'Người có quyền Quản lý hoặc Xem dịch vụ sửa chữa và chi phí khác'],
                            ['Điều kiện ban đầu', 'Người dùng đã đăng nhập và có ít nhất một trong hai quyền.'],
                            ['Dòng sự kiện chính', '1. Người dùng vào menu CSKH sau bán → Danh mục → Dịch vụ sửa chữa và chi phí khác.\n2. Hệ thống nạp trang đầu tiên (10 dòng), dòng mới tạo trên cùng.\n3. Bảng hiển thị dữ liệu kèm tổng số bản ghi.'],
                            ['Dòng sự kiện phụ', '• Không có bản ghi khớp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n• Không có quyền → mục menu bị ẩn, máy chủ không trả dữ liệu.']],
             'anh': [('list', 'Màn Danh mục dịch vụ sửa chữa và chi phí khác lúc mới truy cập')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Mô tả'],
                    ['1', 'STT', 'Table/Grid', 'Read-only', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'],
                    ['2', 'Tên dịch vụ / chi phí', 'Table/Grid', 'Read-only', 'Luôn hiển thị, sắp xếp được. Bấm vào tên mở cửa sổ Xem (xem 2.10).'],
                    ['3', 'Phân loại', 'Table/Grid', 'Read-only', '“Dịch vụ có tính doanh thu” / “Chi phí khác”. Mặc định ẩn.'],
                    ['4', 'ĐM giảm giá', 'Table/Grid', 'Read-only', 'Mức của công ty đang chọn, trống nếu chưa khai báo. Mặc định ẩn.'],
                    ['5', '% Tính giá vốn', 'Table/Grid', 'Read-only', 'Hiển thị gọn, vd 80%. Mặc định ẩn.'],
                    ['6', '% VAT', 'Table/Grid', 'Read-only', 'Hiển thị gọn, vd 8%. Mặc định ẩn.'],
                    ['7', 'Người cập nhật', 'Table/Grid', 'Read-only', 'Họ tên. Mặc định ẩn.'],
                    ['8', 'Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm. Mặc định ẩn, sắp xếp được.'],
                    ['9', 'Người tạo', 'Table/Grid', 'Read-only', 'Họ tên người đã thêm bản ghi.'],
                    ['10', 'Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm, sắp xếp được.'],
                    ['11', 'Trạng thái', 'Badge', 'Read-only', 'Hoạt động hoặc Khóa.'],
                    ['12', 'Hành động', 'Table/Grid', 'Read-only', 'Sửa, Xóa (khi Hoạt động, không phải chi phí hệ thống, có quyền Quản lý), Khóa / Mở khóa (có quyền Quản lý, không phải chi phí hệ thống), Lịch sử. Từ 4 nút trở lên thì 2 nút đầu hiện thẳng, còn lại trong nút ba chấm.'],
                    ['13', 'Nút Tạo mới', 'Button', 'Enable', 'Chỉ hiện với quyền Quản lý. Mở cửa sổ Thêm dịch vụ / chi phí.'],
                    ['14', 'Nút Xuất Excel', 'Button', 'Enable', 'Mở cửa sổ Chọn trường xuất file (xem 2.9).'],
                    ['15', 'Nút Import Excel', 'Button', 'Enable', 'Chỉ hiện với quyền Quản lý. Mở cửa sổ Import (xem 2.8).'],
                    ['16', 'Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', 'Mở cửa sổ Tuỳ chỉnh cột (xem 2.11).'],
                    ['17', 'Phân trang', 'Pagination', 'Enable', 'Số dòng/trang 5 / 10 / 20 / 50 / 100, mặc định 10.']],
             'ui_widths': [0.6, 1.4, 0.9, 0.8, 3],
             'events': [['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền Quản lý hoặc Xem.\nAfter:\n– Nạp trang đầu, sắp xếp ngày tạo giảm dần, hiển thị tổng số bản ghi.'],
                        ['Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Đổi chiều sắp xếp và nạp lại danh sách từ trang 1.'],
                        ['Chuyển trang', 'Click', 'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'],
                        ['Đổi số dòng mỗi trang', 'Change', 'After:\n– Quay về trang 1 và nạp lại theo số dòng mới.']]},
            {'ten': 'Tìm kiếm và lọc',
             'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang. Chỉ bổ sung các tiêu chí tìm kiếm/lọc riêng của màn.',
             'gioi_thieu': [['Tên chức năng', 'Tìm kiếm và lọc danh sách'],
                            ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh, ô Phân loại và ô Trạng thái (bộ lọc gọn một hàng, nhãn nổi).'],
                            ['Tác nhân', 'Người có quyền Quản lý hoặc Xem'],
                            ['Điều kiện ban đầu', 'Đang ở màn Danh mục dịch vụ sửa chữa và chi phí khác.'],
                            ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa và bấm Tìm kiếm / Enter, hoặc chọn Phân loại / Trạng thái (lọc ngay).\n2. Hệ thống áp đồng thời mọi tiêu chí và nạp lại danh sách từ trang 1.'],
                            ['Dòng sự kiện phụ', '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n• Bấm Làm mới → xóa hết tiêu chí VÀ nạp lại danh sách đầy đủ ngay.\n• Bộ lọc được ghi nhớ 10 phút khi rời màn rồi quay lại.']],
             'anh': [('filter', 'Khu vực tìm kiếm và lọc')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Mô tả'],
                    ['1', 'Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Placeholder “Tìm theo tên dịch vụ / chi phí...”. Tìm theo TÊN (khớp một phần). Không tự lọc khi đang gõ.'],
                    ['2', 'Phân loại', 'Dropdown', 'Enable', 'Dịch vụ có tính doanh thu / Chi phí khác', 'Nhãn nổi. Bỏ trống thì hiện cả hai.'],
                    ['3', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Nhãn nổi. Bỏ trống thì hiện cả hai.'],
                    ['4', 'Nút Tìm kiếm', 'Button', 'Enable', '–', 'Áp dụng các tiêu chí.'],
                    ['5', 'Nút Làm mới', 'Button', 'Enable', '–', 'Xóa hết tiêu chí VÀ nạp lại danh sách ngay.']],
             'ui_widths': [0.6, 1.2, 0.8, 0.7, 1.3, 2.4],
             'events': [['Bấm Tìm kiếm / Enter', 'Click', 'After:\n– Áp đồng thời các tiêu chí theo kiểu “và”, nạp lại bảng từ trang 1.'],
                        ['Chọn Phân loại / Trạng thái', 'Change', 'After:\n– Lọc ngay, nạp lại bảng từ trang 1.'],
                        ['Bấm Làm mới', 'Click', 'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ.']]},
            {'ten': 'Thêm mới dịch vụ / chi phí', 'uc': 'uc_fr03',
             'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Thêm mới dịch vụ / chi phí'],
                            ['Mô tả', 'Thêm một dịch vụ sửa chữa hoặc chi phí khác qua cửa sổ nhập liệu.'],
                            ['Tác nhân', 'Người có quyền “Quản lý dịch vụ sửa chữa và chi phí khác”'],
                            ['Điều kiện ban đầu', 'Đang ở màn danh sách, có quyền Quản lý.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở cửa sổ “Thêm dịch vụ / chi phí”: Trạng thái = Hoạt động, ô “Dịch vụ có tính doanh thu” tích sẵn.\n3. Người dùng nhập Tên, % Tính giá vốn, % VAT, ĐM giảm giá (nếu có) và bấm Lưu.\n4. Hệ thống kiểm tra dữ liệu, ghi bản ghi, ghi ĐM giảm giá cho công ty đang chọn và ghi lịch sử Tạo mới.\n5. Cửa sổ đóng, danh sách nạp lại, báo “Thêm mới thành công”.'],
                            ['Dòng sự kiện phụ', '• Thiếu trường bắt buộc, sai định dạng hoặc trùng tên → báo lỗi đỏ dưới ô + toast “Bạn chưa nhập đầy đủ thông tin”, cửa sổ KHÔNG đóng.\n• Bấm “Lưu và tiếp tục” → ghi bản ghi rồi giữ cửa sổ mở với các ô trống.\n• Bấm Đóng khi đã nhập dở → hỏi “Thông tin chưa lưu” (Thoát / Ở lại).'],
                            ['Yêu cầu đặc biệt', 'Cửa sổ có ba nút: Lưu, Lưu và tiếp tục, Đóng.']],
             'menu_them': ' => Tạo mới {icon:btn_taomoi}',
             'ghi_chu_layout': 'Cửa sổ Thêm dịch vụ / chi phí được mở ngay trên màn hình danh sách.',
             'anh': [('create', 'Cửa sổ Thêm dịch vụ / chi phí'), ('create_error', 'Lỗi đỏ ngay dưới ô còn thiếu')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Mô tả'],
                    ['1', 'Tên dịch vụ / chi phí', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Không trùng tên đã có. Bỏ trống “Bắt buộc phải nhập”; trùng “Đã tồn tại trên hệ thống”; quá dài “Vui lòng nhập tối đa 255 ký tự.”'],
                    ['2', '% Tính giá vốn', 'Number', 'Enable', '≥ 0', 'Có', 'Nhập chữ “Phải là số”; số âm “Không được nhỏ hơn 0”.'],
                    ['3', '% VAT', 'Number', 'Enable', '0–100', 'Có', 'Lớn hơn 100 “Tối đa 100”.'],
                    ['4', 'ĐM giảm giá (%)', 'Number', 'Enable', '0–100', 'Không', 'Lưu riêng cho công ty đang chọn; bỏ trống hoặc 0 = không có định mức.'],
                    ['5', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Mặc định Hoạt động.'],
                    ['6', 'Dịch vụ có tính doanh thu', 'Checkbox', 'Enable', '', 'Không', 'Mặc định tích.'],
                    ['7', 'Nút Lưu', 'Button', 'Enable', '', '', 'Ghi bản ghi rồi đóng cửa sổ.'],
                    ['8', 'Nút Lưu và tiếp tục', 'Button', 'Enable', '', '', 'Ghi bản ghi rồi giữ cửa sổ mở để nhập tiếp.'],
                    ['9', 'Nút Đóng', 'Button', 'Enable', '', '', 'Hủy bỏ, không ghi gì.']],
             'ui_widths': [0.6, 1.3, 0.8, 0.6, 1.1, 0.5, 2.3],
             'events': [['Bấm nút Tạo mới', 'Click', 'After:\n– Mở cửa sổ nhập liệu với các ô trống, Trạng thái = Hoạt động, tích sẵn “Dịch vụ có tính doanh thu”.'],
                        ['Bấm Lưu', 'Click', 'During:\n– Kiểm tra bắt buộc, định dạng số, giới hạn, trùng tên.\n– Có lỗi → báo đỏ dưới ô, không thực hiện After.\nAfter:\n– Ghi bản ghi, ghi ĐM giảm giá cho công ty đang chọn (nếu > 0), ghi lịch sử Tạo mới.\n– Đóng cửa sổ, nạp lại danh sách, báo “Thêm mới thành công”.'],
                        ['Bấm Lưu và tiếp tục', 'Click', 'During:\n– Như nút Lưu.\nAfter:\n– Ghi bản ghi, xóa trắng các ô, GIỮ cửa sổ mở.'],
                        ['Bấm Đóng', 'Click', 'After:\n– Chưa nhập gì → đóng cửa sổ. Đã nhập → hỏi “Thông tin chưa lưu”.']]},
            {'ten': 'Chỉnh sửa dịch vụ / chi phí', 'uc': 'uc_fr04',
             'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Chỉnh sửa dịch vụ / chi phí'],
                            ['Mô tả', 'Sửa thông tin một dòng đã có. Dùng chung cửa sổ với Thêm mới (không có nút Lưu và tiếp tục).'],
                            ['Tác nhân', 'Người có quyền “Quản lý dịch vụ sửa chữa và chi phí khác”'],
                            ['Điều kiện ban đầu', 'Dòng đang Hoạt động và không phải chi phí hệ thống.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm biểu tượng bút chì ở dòng cần sửa.\n2. Hệ thống mở cửa sổ “Sửa dịch vụ / chi phí” với dữ liệu hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi, cập nhật ĐM giảm giá của công ty đang chọn và ghi lịch sử.\n5. Cửa sổ đóng, báo “Cập nhật thành công”.'],
                            ['Dòng sự kiện phụ', '• Giữ nguyên tên của chính bản ghi → không báo trùng.\n• Xóa trắng / nhập 0 ở ĐM giảm giá → gỡ định mức của công ty đang chọn, công ty khác giữ nguyên.\n• Bản ghi vừa bị người khác khóa → báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”']],
             'menu_them': ' => Sửa {icon:btn_sua}',
             'anh': [('edit', 'Cửa sổ Sửa dịch vụ / chi phí')],
             'events': [['Bấm biểu tượng bút chì', 'Click', 'Before:\n– Dòng đã Khóa hoặc là chi phí hệ thống thì nút không hiển thị.\nAfter:\n– Mở cửa sổ với dữ liệu hiện tại.'],
                        ['Bấm Lưu', 'Click', 'During:\n– Kiểm tra như Thêm mới, bỏ qua trùng với chính bản ghi.\nAfter:\n– Ghi thay đổi, ghi lịch sử “Thay đổi thông tin” (đổi Trạng thái ghi “Khóa”/“Mở khóa”), báo “Cập nhật thành công”.']]},
            {'ten': 'Xóa dịch vụ / chi phí', 'uc': 'uc_fr05',
             'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Xóa dịch vụ / chi phí'],
                            ['Mô tả', 'Xóa HẲN dòng chưa được sử dụng ở bất kỳ chứng từ nào, kèm ĐM giảm giá của mọi công ty. Dòng đã được sử dụng không xóa được — muốn ngừng dùng thì Khóa.'],
                            ['Tác nhân', 'Người có quyền “Quản lý dịch vụ sửa chữa và chi phí khác”'],
                            ['Điều kiện ban đầu', 'Dòng đang Hoạt động, không phải chi phí hệ thống và chưa được sử dụng.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm biểu tượng thùng rác.\n2. Hệ thống hiện hộp “Xác nhận xóa” — “Bạn có chắc muốn xóa \'…\'?”, nút Xóa.\n3. Người dùng bấm Xóa.\n4. Hệ thống kiểm tra lại trạng thái và tình trạng sử dụng, xóa bản ghi cùng ĐM giảm giá của mọi công ty, ghi lịch sử, báo “Xóa thành công”, nạp lại danh sách.'],
                            ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Dòng đang Khóa, là chi phí hệ thống hoặc đã được sử dụng → nút Xóa KHÔNG hiển thị.\n• Dòng vừa được dùng ở chứng từ trong lúc mở hộp → báo “Dịch vụ/chi phí đang được sử dụng, không thể xóa.”, không xóa.\n• Dòng vừa bị người khác khóa → báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”']],
             'menu_them': ' => Xóa {icon:btn_xoa}',
             'anh': [('delete', 'Hộp xác nhận xóa dịch vụ / chi phí')],
             'events': [['Bấm biểu tượng thùng rác', 'Click', 'Before:\n– Nút chỉ hiển thị khi dòng đang Hoạt động, không phải chi phí hệ thống và chưa được sử dụng.\nAfter:\n– Hiện hộp “Xác nhận xóa” kèm tên bản ghi.'],
                        ['Bấm Xóa', 'Click', 'During:\n– Dòng đang Khóa → báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”, dừng.\n– Dòng đã được sử dụng → báo “Dịch vụ/chi phí đang được sử dụng, không thể xóa.”, dừng.\nAfter:\n– Xóa hẳn bản ghi và ĐM giảm giá của mọi công ty, ghi lịch sử, nạp lại danh sách, báo “Xóa thành công”.'],
                        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.']]},
            {'ten': 'Khóa / Mở khóa dịch vụ / chi phí', 'uc': 'uc_fr06',
             'qtc': 'Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Khóa / Mở khóa dịch vụ / chi phí'],
                            ['Mô tả', 'Đổi trạng thái giữa Hoạt động và Khóa. Chỉ đổi trạng thái, không đụng tới thông số và ĐM giảm giá.'],
                            ['Tác nhân', 'Người có quyền “Quản lý dịch vụ sửa chữa và chi phí khác”'],
                            ['Điều kiện ban đầu', 'Dòng không phải chi phí hệ thống.'],
                            ['Dòng sự kiện chính', '1. Người dùng chọn Khóa (hoặc Mở khóa) ở cột Hành động.\n2. Hệ thống hiện hộp “Xác nhận khóa” / “Xác nhận mở khóa” nêu rõ tên bản ghi.\n3. Người dùng xác nhận.\n4. Hệ thống đổi trạng thái, ghi lịch sử, báo “Khóa thành công” / “Mở khóa thành công”.'],
                            ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Khóa được cả dòng đang được sử dụng ở chứng từ.\n• Sau khi Khóa, nút Sửa và Xóa biến mất; gọi thẳng Sửa / Xóa bị chặn “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”\n• Dòng đã ở trạng thái đích (người khác vừa đổi) → báo “Chi phí đang bị khóa” / “Chi phí đang hoạt động”.']],
             'menu_them': ' => Khóa / Mở khóa',
             'anh': [('lock', 'Hộp xác nhận khóa dịch vụ / chi phí'), ('rowmenu', 'Các nút ở cột Hành động')],
             'events': [['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên bản ghi.'],
                        ['Xác nhận', 'Click', 'During:\n– Chi phí hệ thống hoặc đã ở trạng thái đích → báo lỗi, dừng.\nAfter:\n– Đổi trạng thái, KHÔNG xóa dữ liệu, ghi lịch sử, cập nhật cột Trạng thái và các nút.'],
                        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.']]},
            {'ten': 'Xem lịch sử thay đổi',
             'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Xem lịch sử thay đổi'],
                            ['Mô tả', 'Liệt kê các lần thay đổi của một dịch vụ / chi phí (kể cả ĐM giảm giá của công ty đang chọn), kèm giá trị cũ → mới, người thực hiện và thời điểm.'],
                            ['Tác nhân', 'Người có quyền Quản lý hoặc Xem'],
                            ['Dòng sự kiện chính', '1. Người dùng chọn Lịch sử ở cột Hành động, hoặc mở cửa sổ Xem dịch vụ / chi phí.\n2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <tên>”, mốc mới nhất ở trên cùng.'],
                            ['Dòng sự kiện phụ', '• Bản ghi chưa từng sửa → chỉ có mốc Tạo mới.\n• Có bộ lọc theo loại hành động, người thực hiện, thời gian.']],
             'menu_them': ' => Lịch sử',
             'anh': [('history', 'Cửa sổ Lịch sử thay đổi')]},
            {'ten': 'Import file dịch vụ / chi phí', 'uc': 'uc_fr08',
             'qtc': 'Quy tắc Import file, Validate dữ liệu, Thông báo và Quy định chung về danh mục. Chỉ bổ sung mapping/validation riêng của màn.',
             'gioi_thieu': [['Tên chức năng', 'Import file dịch vụ / chi phí'],
                            ['Mô tả', 'Thêm nhiều dịch vụ / chi phí cùng lúc từ file Excel mẫu, có bước Validate trước khi ghi.'],
                            ['Tác nhân', 'Người có quyền “Quản lý dịch vụ sửa chữa và chi phí khác”'],
                            ['Điều kiện ban đầu', 'Đang ở màn danh sách và đã chuẩn bị file theo mẫu.'],
                            ['Dòng sự kiện chính', '1. Bấm Import Excel.\n2. Bấm Tải file mẫu (Mau_import_dich_vu_sua_chua.xlsx), điền dữ liệu.\n3. Bấm Chọn file Excel rồi Load lên bảng.\n4. Bấm Validate; hệ thống kiểm tra từng dòng, khóa dòng hợp lệ.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi.\n6. Bấm Import; hệ thống ghi các dòng hợp lệ, báo “Import thành công N dịch vụ sửa chữa và chi phí khác.”, đóng cửa sổ và nạp lại danh sách.'],
                            ['Dòng sự kiện phụ', '• File không phải .xlsx/.xls → “Vui lòng chọn file .xlsx hoặc .xls”.\n• Quá 500 dòng → “File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần.”\n• Còn dòng lỗi → nút Import không bấm được.'],
                            ['Yêu cầu đặc biệt', 'Validate không ghi dữ liệu. Bản ghi import luôn ở trạng thái Hoạt động, người tạo là người thực hiện; ĐM giảm giá ghi cho công ty đang chọn.']],
             'menu_them': ' => Import Excel {icon:btn_import}',
             'ghi_chu_layout': 'Cửa sổ Import được mở ngay trên màn hình danh sách.',
             'anh': [('import_open', 'Cửa sổ Import khi vừa mở'), ('import_loaded', 'Dữ liệu đã được load lên bảng xem trước'),
                     ('import_validated', 'Kết quả Validate — mỗi dòng lỗi nêu rõ lý do')],
             'bang_them': [('Quy tắc kiểm tra riêng của file Import', [['Cột', 'Quy tắc / thông báo lỗi'],
                            ['Tên dịch vụ / chi phí *', 'Bắt buộc (“Tên dịch vụ / chi phí không được để trống”), tối đa 255 ký tự (“Tên dịch vụ / chi phí tối đa 255 ký tự”), không trùng trong file (“Tên dịch vụ / chi phí bị trùng với dòng N trong file”), không trùng hệ thống (“Tên dịch vụ / chi phí đã tồn tại trong hệ thống”).'],
                            ['% Tính giá vốn *', 'Bắt buộc (“% Tính giá vốn không được để trống”), là số (“% Tính giá vốn không hợp lệ”), từ 0 đến 100 (“% Tính giá vốn phải nằm trong khoảng 0 - 100”).'],
                            ['% VAT *', 'Bắt buộc (“% VAT không được để trống”), là số (“% VAT không hợp lệ”), từ 0 đến 100 (“% VAT phải nằm trong khoảng 0 - 100”).'],
                            ['ĐM giảm giá (%)', 'Không bắt buộc; nếu có phải là số (“ĐM giảm giá (%) không hợp lệ”), từ 0 đến 100 (“ĐM giảm giá (%) phải nằm trong khoảng 0 - 100”).'],
                            ['Có tính doanh thu', 'Chọn Có / Không. Để trống hoặc Không → “Chi phí khác”.']], [1.3, 4])]},
            {'ten': 'Xuất danh sách ra Excel', 'uc': 'uc_fr09',
             'qtc': 'Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của màn.',
             'gioi_thieu': [['Tên chức năng', 'Xuất danh sách ra Excel'],
                            ['Mô tả', 'Xuất kết quả đang lọc ra file Excel, cho phép chọn trường và thứ tự cột.'],
                            ['Tác nhân', 'Người có quyền Quản lý hoặc Xem'],
                            ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiển thị trên bảng.\n3. Người dùng tích chọn và kéo ☰ để sắp thứ tự.\n4. Bấm Xuất file; hệ thống tải danh_muc_dich_vu_sua_chua_va_chi_phi_khac.xlsx theo đúng bộ lọc, thứ tự sắp xếp và thứ tự trường, báo “Xuất Excel thành công”.'],
                            ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Bấm Đóng → không xuất gì.\n• Lỗi khi xuất → báo “Lỗi khi xuất Excel”.'],
                            ['Yêu cầu đặc biệt', 'File chứa toàn bộ kết quả lọc, không giới hạn ở trang đang xem; cột STT luôn ở đầu. Chỉ xuất Excel.']],
             'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
             'anh': [('export', 'Cửa sổ Chọn trường xuất file')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
                    ['1', 'Danh sách trường', 'Checkbox chọn nhiều', 'Enable', 'Tích sẵn cột đang hiển thị', _TRUONG_XUAT + '. Kéo ☰ đổi thứ tự.'],
                    ['2', 'Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', 'Hiển thị', 'Tích / bỏ tích toàn bộ.'],
                    ['3', 'Nút Xuất file', 'Button', 'Enable/Disable', 'Mờ khi chưa chọn trường', 'Sinh file và tải về.'],
                    ['4', 'Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.']],
             'ui_widths': [0.6, 1.5, 1, 0.8, 1.2, 2.6]},
            {'ten': 'Xem chi tiết dịch vụ / chi phí', 'uc': 'uc_fr10',
             'qtc': 'Màn Xem chi tiết và Phân quyền.',
             'gioi_thieu': [['Tên chức năng', 'Xem chi tiết dịch vụ / chi phí'],
                            ['Mô tả', 'Cửa sổ “Xem dịch vụ / chi phí” hiển thị đủ các trường ở chế độ chỉ đọc, kèm khối Lịch sử.'],
                            ['Tác nhân', 'Người có quyền Quản lý hoặc Xem'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm tên dịch vụ / chi phí ở danh sách.\n2. Hệ thống mở cửa sổ Xem, chỉ có nút Đóng.'],
                            ['Dòng sự kiện phụ', '• Bản ghi không còn tồn tại → báo “Dữ liệu đã thay đổi, vui lòng tải lại”.']],
             'anh': [('detail', 'Cửa sổ Xem dịch vụ / chi phí ở chế độ chỉ đọc')]},
            {'ten': 'Tùy chỉnh cột hiển thị',
             'qtc': 'Tùy chỉnh cột.',
             'gioi_thieu': [['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
                            ['Mô tả', 'Bật/tắt và sắp xếp thứ tự cột của bảng; cấu hình lưu riêng theo người dùng.'],
                            ['Yêu cầu đặc biệt', 'Cột STT, Tên dịch vụ / chi phí, Hành động bị khóa. Mặc định ẩn: Phân loại, ĐM giảm giá, % Tính giá vốn, % VAT, Người cập nhật, Ngày cập nhật.']],
             'menu_them': ' => Cấu hình cột {icon:btn_cauhinhcot}',
             'anh': [('colcfg', 'Cửa sổ Tuỳ chỉnh cột')]},
        ],
        'quy_tac': [
            ('BR-01', 'Ràng buộc trùng tên',
             ['Tên dịch vụ / chi phí không được trùng trong danh mục, tính cả dòng đang Khóa; khi sửa, bản ghi đang sửa được loại khỏi phép so trùng.',
              'Thông báo khi trùng: “Đã tồn tại trên hệ thống”; khi Import: “Tên dịch vụ / chi phí đã tồn tại trong hệ thống” hoặc “Tên dịch vụ / chi phí bị trùng với dòng N trong file”.'],
             ['Thêm mới dịch vụ / chi phí', 'Chỉnh sửa dịch vụ / chi phí', 'Import file dịch vụ / chi phí']),
            ('BR-02', 'ĐM giảm giá theo từng công ty',
             ['ĐM giảm giá khai báo riêng cho từng công ty; màn hình hiển thị, ghi, xóa đúng mức của công ty người dùng đang chọn.',
              'Bỏ trống hoặc nhập 0 là gỡ định mức của công ty đó, không ảnh hưởng mức của công ty khác.',
              '% Tính giá vốn, % VAT, ĐM giảm giá nhận giá trị 0 – 100; dấu phẩy khi nhập được hiểu là dấu thập phân.'],
             ['Xem danh sách dịch vụ / chi phí', 'Thêm mới dịch vụ / chi phí', 'Chỉnh sửa dịch vụ / chi phí', 'Import file dịch vụ / chi phí']),
            ('BR-03', 'Điều kiện xóa',
             ['Chỉ xóa được dòng đang Hoạt động, không phải chi phí hệ thống và CHƯA được sử dụng; xóa là xóa hẳn kèm ĐM giảm giá của mọi công ty.',
              'Được coi là “đã sử dụng” khi dịch vụ / chi phí đã được chọn ở: Báo giá hãng, Hợp đồng hãng; báo giá, hợp đồng, phụ lục hợp đồng bán hàng / dịch vụ / dự án; đề nghị mua, hợp đồng mua trong nước và nhập khẩu, hóa đơn mua hàng, tờ khai hải quan, chi phí nhập khẩu; đề nghị xuất dịch vụ, đề nghị hạch toán và hạch toán dịch vụ; BOM, tính giá sản phẩm, phân tích dự án, sản xuất; Danh mục công việc, lỗi thiết bị; báo giá, hợp đồng dịch vụ, phiếu giao việc, nhập kết quả, hạch toán dịch vụ bảo hành – sửa chữa; đề nghị thanh toán và báo cáo bảo hành; tổng hợp lắp đặt; đề nghị khác.',
              'Dòng đã được sử dụng: nút Xóa bị ẩn; máy chủ chặn và báo “Dịch vụ/chi phí đang được sử dụng, không thể xóa.”. Muốn ngừng dùng thì Khóa.'],
             ['Xóa dịch vụ / chi phí']),
            ('BR-04', 'Bản ghi đang Khóa',
             ['Dòng đang Khóa không sửa, không xóa được: nút Sửa / Xóa bị ẩn, máy chủ chặn và báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”; phải Mở khóa trước.',
              'Khóa được cả dòng đang được sử dụng. Khóa / Mở khóa chỉ đổi trạng thái, không đụng ĐM giảm giá hay thông số khác.',
              'Dòng đang Khóa không còn được chọn ở nghiệp vụ mới.'],
             ['Chỉnh sửa dịch vụ / chi phí', 'Xóa dịch vụ / chi phí', 'Khóa / Mở khóa dịch vụ / chi phí']),
            ('BR-05', 'Chi phí hệ thống',
             ['Hai chi phí “Chi phí đi lại” và “Chi phí vận chuyển” là chi phí hệ thống: không sửa, không xóa, không khóa / mở khóa được.',
              'Máy chủ chặn và báo “Chi phí này không được phép sửa” / “Chi phí này không được phép khóa”.'],
             ['Chỉnh sửa dịch vụ / chi phí', 'Xóa dịch vụ / chi phí', 'Khóa / Mở khóa dịch vụ / chi phí']),
            ('BR-06', 'Phân loại dịch vụ / chi phí',
             ['Phân loại do ô “Dịch vụ có tính doanh thu” quyết định: tích = Dịch vụ có tính doanh thu, không tích = Chi phí khác.'],
             ['Thêm mới dịch vụ / chi phí', 'Chỉnh sửa dịch vụ / chi phí', 'Tìm kiếm và lọc']),
            ('BR-07', 'Giới hạn Import',
             ['Mỗi lần Import tối đa 500 dòng; bước Validate không ghi dữ liệu.',
              'Dòng nhập từ Excel luôn ở trạng thái Hoạt động; ĐM giảm giá ghi cho công ty người đang Import.'],
             ['Import file dịch vụ / chi phí']),
            ('BR-08', 'Ghi lịch sử thay đổi',
             ['Mọi thao tác Tạo mới, Thay đổi thông tin (kể cả ĐM giảm giá), Khóa, Mở khóa, Xóa đều ghi lịch sử kèm người thực hiện.'],
             ['Thêm mới dịch vụ / chi phí', 'Chỉnh sửa dịch vụ / chi phí', 'Xóa dịch vụ / chi phí', 'Khóa / Mở khóa dịch vụ / chi phí', 'Xem lịch sử thay đổi']),
        ],
    },

    # Lỗi code phát hiện khi rà (KHÔNG sửa code) — báo user
    'loi_code': [
        'Import: thông báo “Tên dịch vụ / chi phí bị trùng với dòng N trong file” đánh số dòng = index + 2 (CostService::validateRows) trong khi cột # của bảng xem trước đánh 1, 2, 3… (V2BaseImportModal __row = idx + 1) → số dòng báo lệch 1 so với bảng.',
        'Cửa sổ Xem của dòng đang KHÓA hiện nhầm dòng cảnh báo “Chi phí này nằm trong danh sách không được phép sửa của hệ thống.” (cost-modal.vue điều kiện id && !is_can_edit, mà is_can_edit = false cả khi bị Khóa lẫn khi là chi phí hệ thống).',
        'Ô ĐM giảm giá trong cửa sổ Tạo/Sửa không truyền :invalid → có chữ lỗi nhưng không viền đỏ (khác 3 ô còn lại).',
        'Nhập số thập phân bằng dấu phẩy (vd % VAT = 12,5): rule FE number_only/min_value/max_value_decimal bỏ dấu phẩy nên đọc thành 125 → báo “Tối đa 100”, trong khi BE (CostRequest::prepareForValidation) lại hiểu dấu phẩy là thập phân (12.5). Hai tầng hiểu khác nhau.',
        'Lệch giới hạn % Tính giá vốn: form Tạo/Sửa chỉ chặn < 0 (không có trần), còn Import chặn ngoài 0 - 100. Cần nghiệp vụ chốt một quy tắc.',
        'Validate Import khi tất cả dòng hợp lệ: toast là “Validate thành công” (BE) chứ không phải “Validate xong: N hợp lệ, 0 không hợp lệ” như case chuẩn do tc_gen sinh — case “Validate file hợp lệ” trong nhóm Import mới sẽ lệch chữ (lỗi khuôn tc_gen, không phải lỗi code).',
    ],
}

# ---- Sửa tab testcase "1. DM dịch vụ sửa chữa và chi p" — kế hoạch 28/09/2026 (Xóa hẳn / Khóa / Trạng thái) ----
# Số hàng theo dump ref/testcase_tab.txt tải LẠI 28/09 sau khi tab bị sửa tay (còn 190 hàng; đã có nhóm X. IMPORT, VII. XUẤT EXCEL đã sửa lượt 25/09).
_NB = 'XÓA (XÓA HẲN KHI CHƯA ĐƯỢC SỬ DỤNG)'
_DUNG_VD = 'Báo giá hãng, Hợp đồng hãng, báo giá / hợp đồng dịch vụ bảo hành – sửa chữa, Danh mục công việc, lỗi thiết bị, đề nghị mua, hạch toán dịch vụ…'
CFG['tc'] = {
    'tab': '1. DM dịch vụ sửa chữa và chi p',
    'hdr_row': 113,            # "VII. XUẤT EXCEL"
    'edits': [
        # --- Khối mô tả đầu tab ---
        ('B4', '► Các khoản “Chi phí phải trả” và “Chi phí bán hàng” KHÔNG thuộc màn này (vẫn quản lý bên phần mềm ERP), nên không xuất hiện trong danh sách.\n► Nút Tạo mới / Sửa / Xóa / Khóa / Mở khóa CHỈ hiện với người có quyền quản lý danh mục. Người chỉ được xem thì cột Hành động chỉ còn nút Lịch sử (bấm vào tên để xem chi tiết).\n► 2 dịch vụ hệ thống là “Chi phí đi lại” và “Chi phí vận chuyển” bị khóa cứng: không sửa, không xóa, không khóa, không mở khóa được. Các nút này bị ẨN hẳn, cột Hành động chỉ còn Lịch sử.\n► Dòng đang ở trạng thái Khóa: nút Sửa và nút Xóa bị ẨN hẳn, chỉ còn Mở khóa và Lịch sử; phải Mở khóa trước.\n► Dòng đã được sử dụng ở bất kỳ chứng từ nào: KHÔNG có nút Xóa (vẫn Sửa, Khóa được).\n► Cửa sổ Tạo mới và cửa sổ Sửa đều có ô “Trạng thái” (Tạo mới mặc định Hoạt động).\n► Nút “Lưu và tiếp tục” chỉ có ở cửa sổ Tạo mới, không có ở cửa sổ Sửa và Xem.'),
        ('B10', '► Toàn bộ Tạo mới / Sửa / Xem đều mở trong một cửa sổ nhỏ ngay trên trang, không chuyển sang màn khác.\n► Lỗi nhập liệu hiển thị ngay dưới từng ô (viền đỏ + chữ đỏ) kèm thông báo đỏ “Bạn chưa nhập đầy đủ thông tin” ở góc màn hình. Cửa sổ không bị đóng và dữ liệu đã nhập vẫn còn.\n►  Ở 3 ô phần trăm, DẤU PHẨY được hiểu là DẤU THẬP PHÂN: nhập “12,5” sẽ lưu là 12,5 phần trăm, KHÔNG phải 125. Đây là chủ đích, khác với màn Tiền tệ.\n►  “% Tính giá vốn” KHÔNG bị chặn trần 100 (chỉ cần từ 0 trở lên) — dữ liệu thật đang có dòng 321%. Riêng “% VAT” và “ĐM giảm giá” bị chặn tối đa 100.\n► Xóa là xóa HẲN và chỉ làm được với dịch vụ CHƯA được sử dụng ở chứng từ nào (%s). Dịch vụ đã được sử dụng thì KHÔNG có nút Xóa; muốn ngừng dùng thì Khóa — Khóa được cả dịch vụ đang được sử dụng.\n► Nút không dùng được thì ẨN hẳn, không hiện mờ. Dòng có từ 4 nút trở lên thì 2 nút đầu hiện thẳng, các nút còn lại nằm trong nút ba chấm “Hành động khác”.\n► Phân trang mặc định 10 dòng/trang, chọn được 5 / 10 / 20 / 50.\n► Các TH ghi “gọi thẳng chức năng, bỏ qua giao diện” là kiểm thử bảo mật, cần công cụ kiểm thử API (Postman hoặc tương đương) — dành cho tester kỹ thuật.'.replace('(%s)', '(' + _DUNG_VD + ')')),
        # --- Phân quyền: nút Khóa / Xóa nằm ở cột Hành động ---
        ('I20', '- Vào được màn hình, bảng hiển thị đủ dòng, bộ lọc dùng bình thường\n- Thanh công cụ CHỈ có nút “Xuất Excel” và Cấu hình cột, KHÔNG có nút “Tạo mới”, “Import Excel”\n- Cột Hành động CHỈ có nút Lịch sử; không có Sửa, Xóa, Khóa / Mở khóa'),
        ('G21', '1. Đăng nhập C, vào màn hình\n2. Quan sát thanh công cụ và cột Hành động của một dịch vụ đang Hoạt động, chưa được sử dụng'),
        ('I21', '- Thanh công cụ có đủ nút “Tạo mới”, “Import Excel” và “Xuất Excel”\n- Cột Hành động có Sửa, Xóa hiện thẳng; Khóa và Lịch sử nằm trong nút ba chấm “Hành động khác”'),
        # --- I. Hiển thị: nhãn Trạng thái ---
        ('I30', '- Dòng Hoạt động: nhãn xanh “Hoạt động”\n- Dòng Khóa: nhãn đỏ “Khóa”'),
        # --- IV. Tạo mới / Sửa: ô Trạng thái, nút ẩn ---
        ('I74', '- Cửa sổ tiêu đề “Thêm dịch vụ / chi phí” mở ra ngay trên trang\n- Có 4 ô nhập: Tên dịch vụ / chi phí (bắt buộc), % Tính giá vốn (bắt buộc), % VAT (bắt buộc), ĐM giảm giá (%)\n- Có ô “Trạng thái”, mặc định “Hoạt động”\n- Có ô tích “Dịch vụ có tính doanh thu” ĐANG ĐƯỢC TÍCH SẴN\n- Chân cửa sổ có 3 nút: “Lưu”, “Lưu và tiếp tục”, “Đóng”'),
        ('D79', 'Tạo mới chọn được Trạng thái'),
        ('F79', 'Đang mở cửa sổ Tạo mới'),
        ('G79', '1. Mở ô Trạng thái\n2. Nhập đủ thông tin, chọn Trạng thái = “Khóa”\n3. Bấm “Lưu”\n4. Xem cột Trạng thái và cột Hành động của dòng vừa tạo'),
        ('H79', 'Trạng thái: Khóa'),
        ('I79', '- Ô Trạng thái chỉ có 2 lựa chọn “Hoạt động” và “Khóa”, mặc định “Hoạt động”\n- Lưu thành công, dòng mới có nhãn “Khóa”\n- Cột Hành động của dòng đó chỉ có Mở khóa và Lịch sử'),
        ('I87', '- Lưu thành công\n- Dòng X đổi sang nhãn “Khóa”\n- Nút Sửa và nút Xóa của dòng X biến mất; cột Hành động chỉ còn Mở khóa và Lịch sử'),
        ('G90', '1. Bấm vào tên dịch vụ ở dòng đó'),
        ('I90', '- Vẫn mở được cửa sổ Xem với đầy đủ thông tin, ô Trạng thái hiển thị “Khóa”\n- Chân cửa sổ chỉ có nút “Đóng”'),
        ('D91', 'Nút Sửa bị ẩn khi dòng đang Khóa'),
        ('G91', '1. Quan sát cột Hành động của dòng đó\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cho dòng này'),
        ('I91', '- KHÔNG có nút Sửa (ẩn hẳn, không phải nút mờ); chỉ còn Mở khóa và Lịch sử\n- Gọi thẳng chức năng Sửa bị chặn, báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”; dữ liệu không đổi'),
        ('G94', '1. Tìm dòng “Chi phí vận chuyển”\n2. Quan sát cột Hành động'),
        ('I94', '- Không có nút Sửa, Xóa, Khóa (ẩn hẳn, không phải nút mờ)\n- Cột Hành động chỉ còn nút Lịch sử'),
        # --- V. Khóa / Mở khóa: nút ở cột Hành động ---
        ('G96', '1. Quan sát cột “Hành động” của: dòng Hoạt động chưa được sử dụng, dòng Hoạt động đã được sử dụng, dòng Khóa'),
        ('H96', 'Dòng đã được sử dụng: “Phí vận chuyển hàng gấp”; dòng Khóa: “DOC-Vệ sinh cầu nâng”'),
        ('I96', '- Nút Khóa / Mở khóa nằm ở cột Hành động, KHÔNG nằm trong cột Trạng thái\n- Dòng Hoạt động chưa dùng: Sửa, Xóa hiện thẳng; Khóa, Lịch sử trong nút ba chấm “Hành động khác”\n- Dòng Hoạt động đã được sử dụng: Sửa, Khóa, Lịch sử (không có Xóa)\n- Dòng Khóa: chỉ có Mở khóa và Lịch sử'),
        ('G97', '1. Chọn “Khóa” ở cột Hành động của dòng đó\n2. Quan sát hộp thoại\n3. Bấm “Khóa”'),
        ('I97', '- Hộp thoại tiêu đề “Xác nhận khóa”, nội dung “Bạn có chắc muốn khóa \'TC Dịch vụ kiểm thử 02\'?”, có 2 nút “Hủy” và “Khóa”\n- Sau khi xác nhận: thông báo “Khóa thành công”, danh sách tải lại, nhãn đổi thành “Khóa”\n- Nút Sửa và nút Xóa của dòng đó biến mất, chỉ còn Mở khóa và Lịch sử'),
        ('G98', '1. Chọn “Khóa” ở cột Hành động\n2. Bấm “Hủy”'),
        ('G99', '1. Chọn “Mở khóa” ở cột Hành động của dòng đó\n2. Quan sát hộp thoại\n3. Bấm “Mở khóa”'),
        ('I99', '- Hộp thoại tiêu đề “Xác nhận mở khóa”, nội dung “Bạn có chắc muốn mở khóa \'TC Dịch vụ kiểm thử 02\'?”, nút xác nhận ghi “Mở khóa”\n- Thông báo “Mở khóa thành công”, nhãn đổi lại thành “Hoạt động”\n- Nút Sửa hiện lại; nút Xóa hiện lại nếu dịch vụ chưa được sử dụng'),
        ('I101', '- % Tính giá vốn, % VAT và Phân loại giữ nguyên\n- Chỉ cột Người cập nhật / Ngày cập nhật đổi sang người và thời điểm mới nhất'),
        ('D102', 'Người chỉ có quyền Xem không thấy nút Khóa / Mở khóa'),
        ('G102', '1. Đăng nhập B, quan sát cột Hành động của một dòng Hoạt động và một dòng Khóa'),
        ('I102', '- Cả hai dòng chỉ có nút Lịch sử, không có Khóa / Mở khóa\n- Cột Trạng thái chỉ có nhãn trạng thái'),
        # --- VI. Xóa: xóa hẳn khi chưa được sử dụng ---
        ('C103', 'VI. ' + _NB),
    ] + [('B%d' % r, _NB) for r in range(104, 113)] + [
        ('F104', 'Dịch vụ “TC Dịch vụ kiểm thử 01” đang Hoạt động và CHƯA được sử dụng ở bất kỳ chứng từ nào'),
        ('G104', '1. Bấm nút Xóa (biểu tượng thùng rác) ở dòng đó\n2. Quan sát hộp thoại\n3. Bấm “Xóa”\n4. Bỏ trống ô Trạng thái, tìm lại theo tên'),
        ('I104', '- Hộp thoại tiêu đề “Xác nhận xóa”, nội dung “Bạn có chắc muốn xóa \'TC Dịch vụ kiểm thử 01\'?”, nút xác nhận ghi “Xóa”\n- Thông báo “Xóa thành công”, dịch vụ BIẾN MẤT khỏi danh sách ở cả trạng thái Hoạt động lẫn Khóa (xóa hẳn, không chuyển sang Khóa)\n- ĐM giảm giá của dịch vụ đó ở MỌI công ty cũng bị xóa theo'),
        ('D105', 'Dịch vụ đã dùng ở Báo giá hãng thì không có nút Xóa'),
        ('F105', 'Dịch vụ Y đang Hoạt động và ĐÃ được dùng trong ít nhất 1 Báo giá hãng'),
        ('G105', '1. Tìm dòng Y\n2. Quan sát cột Hành động'),
        ('H105', 'Y: “Phí vận chuyển hàng gấp”'),
        ('I105', '- KHÔNG có nút Xóa (ẩn hẳn, không phải nút mờ)\n- Vẫn có Sửa, Khóa, Lịch sử\n- Không còn hộp thoại “Xác nhận khóa” thay cho xóa'),
        ('D106', 'Dịch vụ đã dùng ở nghiệp vụ khác thì không có nút Xóa'),
        ('F106', 'Chuẩn bị các dịch vụ đang Hoạt động, mỗi dịch vụ được dùng ở đúng một nơi như Test data'),
        ('G106', '1. Tìm lần lượt từng dịch vụ\n2. Quan sát cột Hành động'),
        ('H106', '1. Hợp đồng hãng: “Chi phí sửa chữa, thay thế”\n2. Danh mục công việc, lỗi thiết bị: “Vật tư sửa chữa số 13”\n3. Báo giá dịch vụ bảo hành – sửa chữa: “Thuê giàn giáo 1 bộ/ngày”'),
        ('I106', '- Cả 3 dịch vụ đều KHÔNG có nút Xóa\n- Vẫn Khóa được bình thường'),
        ('D107', 'Gọi thẳng chức năng Xóa dịch vụ đã được sử dụng'),
        ('F107', 'Dịch vụ Y đang Hoạt động, đã được dùng ở Báo giá hãng'),
        ('G107', '1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa cho Y\n2. Tải lại màn hình, tìm Y'),
        ('H107', 'Y: “Phí vận chuyển hàng gấp”'),
        ('I107', '- Hệ thống từ chối, báo “Dịch vụ/chi phí đang được sử dụng, không thể xóa.”\n- Y vẫn còn, trạng thái vẫn “Hoạt động” (không bị tự chuyển sang Khóa)'),
        ('D109', 'Nút Xóa bị ẩn khi dòng đang Khóa'),
        ('G109', '1. Quan sát cột Hành động của dòng đó\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa cho dòng này'),
        ('I109', '- KHÔNG có nút Xóa (ẩn hẳn), chỉ còn Mở khóa và Lịch sử\n- Gọi thẳng chức năng Xóa bị chặn, báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”; dòng vẫn còn'),
        ('D110', 'Bấm Xóa lần lượt nhiều dòng'),
        ('F110', 'Danh sách có ít nhất 2 dòng xóa được (A, B)'),
        ('G110', '1. Bấm Xóa ở dòng A, bấm “Hủy”\n2. Bấm Xóa ở dòng B, đọc hộp thoại'),
        ('H110', '2 dòng A, B'),
        ('I110', '- Hộp thoại lần 2 ghi đúng tên dòng B, không còn tên A\n- Chỉ mở đúng 1 hộp thoại, không mở chồng 2 hộp'),
    ],
    'clear_k': [4, 10, 20, 21, 30, 74, 79, 87, 90, 91, 94, 96, 97, 98, 99, 101, 102] + list(range(103, 111)),
    'blocks': [
        # V. KHÓA / MỞ KHÓA — cuối nhóm (TC_05.010 ở R102)
        {'after': 102, 'merge_from': 96, 'cases': [
            ('TC_05.011', 'Khóa được dịch vụ đang được sử dụng', 'P0', 'Dịch vụ Y đang Hoạt động, đã được dùng ở Báo giá hãng.',
             '1. Chọn “Khóa” ở cột Hành động của Y\n2. Bấm “Khóa”', 'Y: “Phí vận chuyển hàng gấp”',
             '- Thông báo “Khóa thành công”, nhãn đổi thành “Khóa”\n- Không có thông báo chặn vì đang được sử dụng\n- Chứng từ đã dùng Y vẫn hiện đúng tên Y'),
            ('TC_05.012', 'Người khác khóa trong lúc đang sửa', 'P1', 'Hai tài khoản C, D cùng có quyền quản lý. C đang mở cửa sổ Sửa dịch vụ X.',
             '1. D khóa X\n2. C đổi % VAT của X và bấm “Lưu”', '',
             '- C nhận thông báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”\n- Dữ liệu của X không đổi'),
            ('TC_05.013', 'Khóa / Mở khóa được ghi lịch sử', 'P2', 'Dịch vụ X đang Hoạt động.',
             '1. Khóa X ở cột Hành động\n2. Mở khóa X\n3. Chọn Lịch sử của X', '',
             '- Có 2 dòng thay đổi trạng thái: “Hoạt động” → “Khóa” và “Khóa” → “Hoạt động”, kèm người thực hiện và thời điểm'),
        ]},
        # VI. XÓA — cuối nhóm (TC_06.010 ở R112)
        {'after': 112, 'merge_from': 104, 'cases': [
            ('TC_06.011', 'Dịch vụ được sử dụng trong lúc đang mở hộp xác nhận Xóa', 'P1', 'Dịch vụ X đang Hoạt động, chưa được sử dụng, đang hiện nút Xóa.',
             '1. Bấm Xóa ở dòng X, để hộp xác nhận mở\n2. Ở tab khác, chọn X trong một chứng từ (vd Báo giá hãng) rồi lưu\n3. Quay lại, bấm “Xóa”', '',
             '- Thông báo “Dịch vụ/chi phí đang được sử dụng, không thể xóa.”\n- X vẫn còn trong danh sách, trạng thái “Hoạt động”\n- Tải lại màn hình: dòng X không còn nút Xóa'),
            ('TC_06.012', 'Dịch vụ bị khóa trong lúc đang mở hộp xác nhận Xóa', 'P1', 'Hai tài khoản C, D. X đang Hoạt động, chưa được sử dụng.',
             '1. C bấm Xóa ở dòng X, để hộp xác nhận mở\n2. D khóa X\n3. C bấm “Xóa”', '',
             '- C nhận thông báo “Chi phí đang bị khóa, hãy mở khóa trước khi sửa.”\n- X vẫn còn, ở trạng thái Khóa sau khi tải lại'),
            ('TC_06.013', 'Xóa hẳn rồi tạo lại cùng tên', 'P2', 'Vừa xóa thành công dịch vụ “TC Dịch vụ kiểm thử 01”.',
             '1. Bấm “Tạo mới”\n2. Nhập lại tên “TC Dịch vụ kiểm thử 01”, % Tính giá vốn 70, % VAT 8\n3. Bấm “Lưu”', 'Tên: TC Dịch vụ kiểm thử 01',
             '- Lưu thành công, không bị báo “Đã tồn tại trên hệ thống” (bản ghi cũ đã bị xóa hẳn)'),
            ('TC_06.014', 'Mở khóa dịch vụ chưa dùng thì nút Xóa hiện lại', 'P2', 'Dịch vụ X chưa được sử dụng, đang Khóa.',
             '1. Mở khóa X\n2. Quan sát cột Hành động của X', '',
             '- Có lại nút Xóa cùng Sửa, Khóa, Lịch sử'),
        ]},
    ],
}

# Ngoài phạm vi lượt 28/09 (Xóa / Khóa / Trạng thái) — tab đang lệch code, KHÔNG sửa, báo user
CFG['tc_ngoai_pham_vi'] = [
    'Mô tả R3, R5 và TC_01.003, TC_01.007, TC_01.008: cột “Cập nhật” gộp ngày + người đã bị tách thành 4 cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật; R3 còn ghi 9 cột và “Có tính doanh thu” nhãn màu.',
    'TC_01.003, TC_01.004: bảng mặc định chỉ hiện STT, Tên, Người tạo, Ngày tạo, Trạng thái, Hành động; chỉ 3 cột sắp xếp được.',
    'TC_01.006: Phân loại nay là chữ thường (không còn nhãn màu). TC_01.010: giá trị trống để trống, không hiện gạch ngang.',
    'TC_02.003, TC_02.004, TC_02.009, TC_02.010: bộ lọc gọn 1 hàng, không còn Tìm kiếm nâng cao, ô lọc Tên và Người cập nhật.',
    'TC_03.003 – TC_03.007: các cột này không còn sắp xếp được.',
    'TC-ROLE-01 (R20 đã sửa phần nút), TC-ROLE-03, TC_04.016: không còn nút Xem (con mắt); bấm vào tên để mở cửa sổ Xem.',
    'TC_04.001 và các case khác ghi “Lưu & Tiếp tục”: nút thật là “Lưu và tiếp tục” (đã sửa ở R74, R4).',
    'TC_08.014, TC_08.023 (nhập dấu phẩy thập phân): FE đọc “12,5” thành 125 (xem loi_code).',
    'Tab chưa có case cho Tùy chỉnh cột hiển thị.',
]


# ==== Bổ sung “Mô tả chi tiết giao diện” + “Danh sách event và xử lý event” cho MỌI FR của SRS (28/09/2026) ====
# Bám khuôn SRS Danh mục quốc gia. Nguồn: cửa sổ Tạo/Sửa/Xem (V2BaseModal + unsavedModalMixin), hộp xác nhận
# base-confirm-modal, CatalogHistoryModal + SystemInfoSection, V2BaseImportModal/Toolbar/Table + CatalogImportMixin,
# export-fields-modal, column-customization-modal (lưu theo tài khoản qua column-customizations), V2BaseRowActions (maxInline 3).
def _srs_ui_events(cfg, p):
    fr = {f['ten']: f for f in cfg['srs']['fr']}
    w_form = [0.5, 1.3, 0.8, 0.7, 1.0, 0.6, 1.0, 2.1]
    w4 = [0.6, 1.6, 1.1, 3]
    w_ls = [0.6, 1.4, 1.0, 1.2, 2.8]
    w_imp = [0.5, 1.4, 0.8, 0.8, 0.5, 1.0, 2.5]
    w6 = [0.6, 1.5, 1.0, 0.8, 1.3, 2.5]
    unsaved = '“Thông tin chưa lưu” — “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại)'
    ev_dong = ['Bấm Đóng / biểu tượng × / bấm ra ngoài cửa sổ', 'Click',
               'Before:\n– Chưa thay đổi gì → đóng cửa sổ ngay.\nDuring:\n– Đã thay đổi dữ liệu → hỏi ' + unsaved + '.\n'
               'After:\n– Chọn Thoát → đóng cửa sổ, không ghi gì; chọn Ở lại → giữ nguyên dữ liệu đang nhập.']

    # ---- Chỉnh sửa
    f = fr[p['fr_sua']]
    rows = [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả'],
            ['Biểu tượng bút chì', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
             'Nằm ở cột Hành động (hiện thẳng). ' + p['sua_hien']],
            ['Tiêu đề cửa sổ', 'Label', 'Read-only', '–', '–', '“%s”' % p['tieu_de_sua'],
             'Cửa sổ mở ngay trên màn danh sách, dùng chung với Thêm mới.']]
    rows += [[t, l, 'Enable', pv, bb, 'Dữ liệu hiện tại', mt] for t, l, pv, bb, mt in p['truong_sua']]
    rows += [['Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
              'Mờ trong lúc đang ghi để chống bấm hai lần. Ghi thay đổi rồi đóng cửa sổ. Cửa sổ Sửa KHÔNG có nút Lưu và tiếp tục.'],
             ['Nút Đóng / biểu tượng ×', 'Button', 'Enable', '–', '–', 'Hiển thị',
              'Đóng cửa sổ, không ghi gì; đã sửa dở thì hỏi ' + unsaved + '.']]
    f['ui'] = [rows[0]] + [[str(i)] + r for i, r in enumerate(rows[1:], 1)]
    f['ui_widths'] = w_form
    f['events'] = list(f.get('events') or []) + [ev_dong]

    # ---- Xóa
    f = fr[p['fr_xoa']]
    f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Mô tả'],
               ['1', 'Biểu tượng thùng rác', 'Icon Button', 'Nằm ở cột Hành động (hiện thẳng). ' + p['xoa_hien']],
               ['2', 'Tiêu đề hộp xác nhận', 'Label', '“%s”.' % p['xoa_tieu_de']],
               ['3', 'Nội dung hộp xác nhận', 'Label', '“%s” — nêu rõ %s để tránh xóa nhầm dòng.' % (p['xoa_cau'], p['nhan_ban_ghi'])],
               ['4', 'Nút Xóa', 'Button', 'Xác nhận xóa hẳn bản ghi.'],
               ['5', 'Nút Hủy', 'Button', 'Đóng hộp, không thay đổi gì.']]
    f['ui_widths'] = w4

    # ---- Khóa / Mở khóa
    f = fr[p['fr_khoa']]
    f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Mô tả'],
               ['1', 'Nút ba chấm “Hành động khác”', 'Icon Button',
                'Chỉ có khi dòng có từ 4 thao tác trở lên: 2 thao tác đầu hiện thẳng, các thao tác còn lại (trong đó có Khóa / Mở khóa, Lịch sử) nằm trong nút này. Dòng có ≤ 3 thao tác thì mọi nút hiện thẳng.'],
               ['2', 'Mục Khóa / Mở khóa', 'Button', p['khoa_hien']],
               ['3', 'Tiêu đề hộp xác nhận', 'Label', p['khoa_tieu_de']],
               ['4', 'Nội dung hộp xác nhận', 'Label', p['khoa_cau']],
               ['5', 'Nút Khóa / Mở khóa', 'Button', 'Xác nhận đổi trạng thái; chữ trên nút theo thao tác đang làm.'],
               ['6', 'Nút Hủy', 'Button', 'Đóng hộp, trạng thái không đổi.'],
               ['7', 'Cột Trạng thái', 'Badge', 'Hoạt động (xanh) hoặc Khóa (đỏ), cập nhật ngay sau khi xác nhận.']]
    f['ui_widths'] = w4

    # ---- Lịch sử
    f = fr[p['fr_ls']]
    f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Giá trị ban đầu', 'Mô tả'],
               ['1', 'Mục Lịch sử', 'Button', 'Hiển thị',
                'Ở cột Hành động (trong nút ba chấm khi dòng có từ 4 thao tác). Luôn hiện, không cần quyền riêng.'],
               ['2', 'Tiêu đề cửa sổ', 'Label', 'Lịch sử thay đổi', 'Ghép tên bản ghi: “Lịch sử thay đổi: <%s>”.' % p['nhan_ban_ghi']],
               ['3', 'Nút Bộ lọc', 'Button', 'Vùng lọc thu gọn',
                'Bấm để mở / thu gọn vùng lọc. Vùng lọc ghim ở đầu cửa sổ, cuộn danh sách vẫn thấy.'],
               ['4', 'Loại hành động / Người thực hiện', 'Dropdown', 'Trống',
                'Placeholder “Tất cả loại hành động” / “Tất cả người thực hiện”; có dấu × để xóa lựa chọn. Chọn là lọc ngay, không có nút Tìm kiếm.'],
               ['5', 'Từ ngày / Đến ngày', 'Date', 'Trống', 'Chọn ngày dạng dd/mm/yyyy, lọc ngay khi chọn.'],
               ['6', 'Nút Làm mới (vùng lọc)', 'Button', 'Hiển thị', 'Xóa hết điều kiện lọc của cửa sổ.'],
               ['7', 'Danh sách thay đổi', 'Timeline', 'Theo dữ liệu',
                '- Thời điểm dd/mm/yyyy hh:mm, mới nhất ở trên cùng.\n- Loại: Tạo mới, Thay đổi thông tin, Khóa, Mở khóa (nhóm Thay đổi trạng thái).\n'
                '- “Người thực hiện: <tên>” kèm phòng ban.\n- Giá trị cũ → giá trị mới của từng trường đã đổi (' + p['truong_ls'] + ').'],
               ['8', 'Trạng thái rỗng', 'Label', 'Ẩn',
                '“Chưa có lịch sử thao tác nào.” khi bản ghi chưa có mốc; “Không có lịch sử phù hợp bộ lọc.” khi lọc không ra.'],
               ['9', 'Nút Đóng / biểu tượng ×', 'Button', 'Hiển thị', 'Đóng cửa sổ.']]
    f['ui_widths'] = w_ls
    f['events'] = [['Chọn Lịch sử ở cột Hành động', 'Click',
                    'After:\n– Mở cửa sổ “Lịch sử thay đổi: <%s>”, nạp các mốc thay đổi, mới nhất trước.' % p['nhan_ban_ghi']],
                   ['Bấm Bộ lọc', 'Click', 'After:\n– Mở / thu gọn vùng lọc.'],
                   ['Chọn Loại hành động / Người thực hiện / Từ ngày / Đến ngày', 'Change',
                    'After:\n– Lọc ngay danh sách mốc theo mọi điều kiện đang chọn.\n– Không còn mốc khớp → “Không có lịch sử phù hợp bộ lọc.”'],
                   ['Bấm Làm mới (vùng lọc)', 'Click', 'After:\n– Xóa hết điều kiện lọc, hiện lại đủ các mốc.'],
                   ['Bấm Đóng / biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ; danh sách phía sau giữ nguyên bộ lọc và trang.']]

    # ---- Import
    f = fr[p['fr_import']]
    f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả'],
               ['1', 'Nút Import Excel', 'Button', 'Enable', '–', 'Hiển thị',
                'Thanh công cụ của bảng; chỉ hiện với %s. Mở cửa sổ “%s”, dòng phụ “Import từ Excel • Validate xong dòng hợp lệ sẽ bị khoá”.' % (p['quyen_import'], p['import_tieu_de'])],
               ['2', 'Nút Chọn file Excel', 'Button', 'Enable', 'Có', 'Chưa chọn file', 'Chọn file .xlsx / .xls từ máy; tên file hiện ngay cạnh nút.'],
               ['3', 'Nút Tải file mẫu', 'Button', 'Enable', '–', 'Hiển thị',
                'Tải %s gồm các cột %s; cột bắt buộc có dấu * đỏ.' % (p['import_file'], p['import_cot'])],
               ['4', 'Nút Load lên bảng', 'Button', 'Enable / Disable', '–', 'Mờ khi chưa chọn file', 'Đọc file và đổ dữ liệu lên bảng xem trước.'],
               ['5', 'Nút Validate', 'Button', 'Enable / Disable', '–', 'Mờ khi bảng chưa có dòng nào',
                'Gửi máy chủ kiểm tra từng dòng; dòng hợp lệ bị khóa lại, không sửa được nữa.'],
               ['6', 'Nút Import', 'Button', 'Enable / Disable', '–', 'Mờ',
                'Chỉ bấm được khi đã Validate, không còn dòng lỗi và có ít nhất 1 dòng hợp lệ.'],
               ['7', 'Ô Tổng / Hợp lệ / Lỗi', 'Label', 'Read-only', '–', 'Tổng: 0',
                'Tổng = số dòng đọc được. Sau Validate hiện thêm Hợp lệ / Lỗi; sửa một dòng lỗi thì hiện “Có dòng đã sửa (cần validate lại)”.'],
               ['8', 'Bảng xem trước', 'Table/Grid', 'Enable', '–', 'Trống',
                'Tiêu đề “Preview (chỉ sửa dòng lỗi)”, các cột: %s. Chỉ sửa trực tiếp được ở dòng lỗi; lý do lỗi ghi ngay dưới dòng.' % p['import_cot_bang']],
               ['9', 'Thông báo lỗi / kết quả', 'Label', 'Read-only', '–', 'Ẩn',
                'Dải đỏ nêu lỗi đọc file hoặc lỗi Validate; dải xanh nêu kết quả Validate / Bỏ dòng lỗi.'],
               ['10', 'Nút Bỏ dòng lỗi', 'Button', 'Enable', '–', 'Hiển thị', 'Loại toàn bộ dòng đang lỗi khỏi bảng xem trước (phải Validate trước).'],
               ['11', 'Nút Xoá trạng thái validate', 'Button', 'Enable', '–', 'Hiển thị', 'Bỏ khóa các dòng hợp lệ và bỏ thông báo lỗi để sửa lại từ đầu.'],
               ['12', 'Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', 'Xóa file và dữ liệu đang có, đưa cửa sổ về trạng thái ban đầu.'],
               ['13', 'Nút Đóng / biểu tượng ×', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ, không ghi gì.']]
    f['ui_widths'] = w_imp
    f['events'] = [['Bấm Import Excel', 'Click', 'After:\n– Mở cửa sổ “%s” ở trạng thái rỗng.' % p['import_tieu_de']],
                   ['Bấm Tải file mẫu', 'Click', 'After:\n– Tải file %s về máy.' % p['import_file']],
                   ['Bấm Chọn file Excel', 'Click', 'During:\n– File không phải .xlsx / .xls → “Vui lòng chọn file .xlsx hoặc .xls”.\nAfter:\n– Hiện tên file cạnh nút, nút Load lên bảng sáng lên.'],
                   ['Bấm Load lên bảng', 'Click',
                    'During:\n– File không có dòng dữ liệu → “Không có dòng dữ liệu hợp lệ.”\n– Quá 500 dòng → “File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần.”\n'
                    'After:\n– Đổ dữ liệu lên bảng xem trước, đánh STT 1, 2, 3…, cập nhật ô Tổng.'],
                   ['Bấm Validate', 'Click',
                    'During:\n– Máy chủ kiểm tra từng dòng theo quy tắc Thêm mới (mục 2.3) và bảng quy tắc riêng của file Import.\n'
                    'After:\n– Có dòng lỗi: tô đỏ dòng lỗi kèm lý do, khóa dòng hợp lệ, hiện “Validate xong: a hợp lệ, b không hợp lệ. (Dòng hợp lệ đã bị khoá, chỉ có thể sửa dòng lỗi)”.\n'
                    '– Không có dòng lỗi: “Tất cả N dòng đã hợp lệ. Có thể import ngay.”, nút Import sáng lên.\n– Không dòng nào hợp lệ: “Không có dòng nào hợp lệ để import. Hãy sửa các dòng lỗi và validate lại.”\n– KHÔNG ghi bất kỳ bản ghi nào ở bước này.'],
                   ['Sửa ô ở dòng lỗi', 'Input', 'After:\n– Dòng được đánh dấu đã sửa, hiện “Có dòng đã sửa (cần validate lại)”; phải Validate lại mới Import được.'],
                   ['Bấm Bỏ dòng lỗi', 'Click', 'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.”\nAfter:\n– Loại dòng lỗi, hiện “Đã bỏ N dòng lỗi. Còn lại M dòng hợp lệ.”'],
                   ['Bấm Import', 'Click',
                    'During:\n– Máy chủ kiểm tra lại toàn bộ dòng gửi lên, không tin kết quả Validate trước đó.\n'
                    'After:\n– Ghi các dòng hợp lệ thành %s mới ở trạng thái Hoạt động, người tạo là người thực hiện, ghi lịch sử Tạo mới.\n'
                    '– Báo “%s” (có dòng ghi thất bại thì “%s”), đóng cửa sổ, nạp lại danh sách.' % (p['doi_tuong_import'], p['import_toast'], p['import_toast_loi'])],
                   ['Bấm Làm mới', 'Click', 'After:\n– Xóa file và dữ liệu đang có, cửa sổ về trạng thái rỗng.'],
                   ['Bấm Đóng / biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ, không ghi gì.']]

    # ---- Xuất Excel
    f = fr[p['fr_xuat']]
    f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
               ['1', 'Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Thanh công cụ của bảng, màu xanh lá. ' + p['xuat_hien'] + ' Mở cửa sổ “Chọn trường xuất file”.'],
               ['2', 'Dòng hướng dẫn', 'Label', 'Read-only', 'Hiển thị', '“Tích chọn trường cần xuất, kéo biểu tượng ba gạch để đổi thứ tự cột trong file.”'],
               ['3', 'Danh sách trường', 'Checkbox chọn nhiều', 'Enable', 'Tích sẵn các cột đang hiển thị trên bảng',
                '%s. Kéo biểu tượng ba gạch để đổi thứ tự cột trong file.' % p['xuat_truong']],
               ['4', 'Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', 'Hiển thị', 'Tích / bỏ tích toàn bộ trường.'],
               ['5', 'Dòng “Đang chọn a/%d trường”' % p['xuat_so'], 'Label', 'Read-only', 'Theo số trường tích sẵn', 'Số trường đang chọn trên tổng số trường.'],
               ['6', 'Nút Xuất file', 'Button', 'Enable / Disable', 'Mờ khi chưa chọn trường nào', 'Sinh file Excel và tải về máy; mờ trong lúc đang xuất.'],
               ['7', 'Nút Đóng / biểu tượng ×', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ, không xuất gì.']]
    f['ui_widths'] = w6
    f['events'] = [['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiển thị trên bảng theo thứ tự trên bảng.'],
                   ['Tích / bỏ tích / kéo biểu tượng ba gạch trường', 'Change / Drag',
                    'During:\n– Ghi nhận thứ tự trường để quyết định thứ tự cột trong file.\n– Bỏ chọn hết → nút Xuất file mờ đi, không bấm được.'],
                   ['Bấm Xuất file', 'Click',
                    'During:\n– Sinh file theo ĐÚNG %s đang áp dụng, lấy toàn bộ kết quả (không theo trang), cột STT luôn đứng đầu.\n'
                    'After:\n– Tải file %s về máy, báo “Xuất Excel thành công” (lỗi → “Lỗi khi xuất Excel”).' % (p['xuat_theo'], p['xuat_file'])],
                   ['Bấm Đóng / biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ, không xuất gì.']]

    # ---- Xem chi tiết
    f = fr[p['fr_xem']]
    rows = [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
            [p['nhan_cot'] + ' (ô trên danh sách)', 'Link', 'Enable', 'Hiển thị',
             'Bấm vào %s để mở cửa sổ Xem; màn hình không có nút Xem riêng ở cột Hành động.' % p['nhan_ban_ghi']],
            ['Tiêu đề cửa sổ', 'Label', 'Read-only', '“%s”' % p['tieu_de_xem'], 'Cửa sổ khổ rộng, mở ngay trên màn danh sách.']]
    rows += [[t, l, 'Read-only', 'Dữ liệu hiện tại', mt] for t, l, mt in p['truong_xem']]
    rows += [['Khối Lịch sử', 'Section', 'Enable', 'Thu gọn',
              'Tiêu đề “Lịch sử”. Nút “Xem lịch sử” mở khối và nạp dữ liệu lần đầu, “Thu gọn” đóng lại, “Làm mới” nạp lại. Nội dung, bộ lọc giống cửa sổ Lịch sử thay đổi (mục 2.7).'],
             ['Nút Đóng / biểu tượng ×', 'Button', 'Enable', 'Hiển thị', 'Nút duy nhất ở chân cửa sổ (không có Lưu, Lưu và tiếp tục). Đóng cửa sổ.']]
    f['ui'] = [rows[0]] + [[str(i)] + r for i, r in enumerate(rows[1:], 1)]
    f['ui_widths'] = w6
    f['events'] = [['Bấm %s ở danh sách' % p['nhan_ban_ghi'], 'Click',
                    'During:\n– Nạp dữ liệu mới nhất của bản ghi.\n– Bản ghi không còn tồn tại → báo “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.\n'
                    'After:\n– Mở cửa sổ “%s”, mọi ô ở chế độ chỉ đọc (kể cả bản ghi đang Khóa).' % p['tieu_de_xem']],
                   ['Bấm Xem lịch sử / Thu gọn', 'Click', 'After:\n– Mở khối Lịch sử và nạp các mốc thay đổi (mới nhất trên cùng) / thu gọn khối.'],
                   ['Bấm Đóng / biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ; danh sách giữ nguyên bộ lọc và trang.']]

    # ---- Tùy chỉnh cột
    f = fr[p['fr_cot']]
    f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
               ['1', 'Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', 'Hiển thị',
                'Nút cuối thanh công cụ của bảng; rê chuột hiện “Cấu hình cột hiển thị”. Mở cửa sổ “Tuỳ chỉnh cột”.'],
               ['2', 'Danh sách cột', 'Checkbox chọn nhiều', 'Enable', 'Theo cấu hình đã lưu của người dùng',
                'Liệt kê đủ %d cột: %s. Tích = hiện, bỏ tích = ẩn. Lần đầu (chưa lưu cấu hình) hiện: %s.' % (len(p['cot_all']), ', '.join(p['cot_all']), p['cot_mac_dinh'])],
               ['3', 'Cột bắt buộc', 'Checkbox', 'Disable', 'Luôn tích',
                '%s: chữ xám, có biểu tượng ổ khóa (rê chuột hiện “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”), không bỏ tích và không kéo được.' % p['cot_khoa']],
               ['4', 'Biểu tượng ☰', 'Drag handle', 'Enable', 'Hiển thị', 'Kéo thả để đổi thứ tự các cột không bắt buộc.'],
               ['5', 'Nút Lưu', 'Button', 'Enable', 'Hiển thị',
                'Áp dụng ngay lên bảng và lưu cấu hình theo TÀI KHOẢN người dùng (đăng nhập máy khác vẫn giữ, không ảnh hưởng người khác).'],
               ['6', 'Nút Đóng / biểu tượng ×', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ, bỏ các thay đổi chưa Lưu.']]
    f['ui_widths'] = w6
    f['events'] = [['Bấm biểu tượng Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ “Tuỳ chỉnh cột” với cấu hình cột đang áp dụng.'],
                   ['Tích / bỏ tích, kéo thả cột', 'Change / Drag',
                    'During:\n– Cột bắt buộc không bỏ tích, không kéo được.\n– Chưa áp dụng lên bảng cho tới khi bấm Lưu.'],
                   ['Bấm Lưu', 'Click',
                    'After:\n– Bảng hiện / ẩn và sắp cột theo lựa chọn ngay; cửa sổ Chọn trường xuất file cũng tích sẵn theo bộ cột mới.\n'
                    '– Lưu cấu hình riêng cho tài khoản, báo “Cập nhật thành công” (lỗi lưu → “Thao tác thất bại”).'],
                   ['Bấm Đóng / biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ, danh sách cột trở về cấu hình đang áp dụng.']]


_MSG_LOCKED_COST = 'Chi phí đang bị khóa, hãy mở khóa trước khi sửa.'
_srs_ui_events(CFG, {
    'fr_sua': 'Chỉnh sửa dịch vụ / chi phí', 'fr_xoa': 'Xóa dịch vụ / chi phí', 'fr_khoa': 'Khóa / Mở khóa dịch vụ / chi phí',
    'fr_ls': 'Xem lịch sử thay đổi', 'fr_import': 'Import file dịch vụ / chi phí', 'fr_xuat': 'Xuất danh sách ra Excel',
    'fr_xem': 'Xem chi tiết dịch vụ / chi phí', 'fr_cot': 'Tùy chỉnh cột hiển thị',
    'nhan_ban_ghi': 'tên dịch vụ / chi phí', 'nhan_cot': 'Tên dịch vụ / chi phí',
    'tieu_de_sua': 'Sửa dịch vụ / chi phí', 'tieu_de_xem': 'Xem dịch vụ / chi phí',
    'sua_hien': 'Chỉ hiện khi Người dùng có quyền Quản lý, dòng đang Hoạt động VÀ không phải chi phí hệ thống (“Chi phí đi lại”, “Chi phí vận chuyển”).',
    'truong_sua': [
        ('Tên dịch vụ / chi phí', 'Textbox', '1–255 ký tự', 'Có',
         'Không trùng tên đã có (kể cả dòng đang Khóa), bỏ qua chính bản ghi đang sửa. Bỏ trống “Bắt buộc phải nhập”; trùng “Đã tồn tại trên hệ thống”; quá dài “Vui lòng nhập tối đa 255 ký tự.”'),
        ('% Tính giá vốn', 'Number', '≥ 0', 'Có', 'Nhập chữ “Phải là số”; số âm “Không được nhỏ hơn 0”. Số thập phân dùng dấu chấm (12.5).'),
        ('% VAT', 'Number', '0 – 100', 'Có', 'Lớn hơn 100 “Tối đa 100”; nhập chữ “Phải là số”; số âm “Không được nhỏ hơn 0”.'),
        ('ĐM giảm giá (%)', 'Number', '0 – 100', 'Không',
         'Mức của CÔNG TY ĐANG CHỌN. Xóa trắng hoặc nhập 0 rồi Lưu → gỡ định mức của công ty đang chọn, công ty khác giữ nguyên.'),
        ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Không', 'Không xóa trống được. Chọn Khóa rồi Lưu là khóa ngay trong cửa sổ Sửa.'),
        ('Dịch vụ có tính doanh thu', 'Checkbox', 'Tích / bỏ tích', 'Không', 'Tích = “Dịch vụ có tính doanh thu”; bỏ tích = “Chi phí khác”.'),
    ],
    'xoa_hien': 'Chỉ hiện khi Người dùng có quyền Quản lý, dòng đang Hoạt động, không phải chi phí hệ thống VÀ chưa được sử dụng ở chứng từ, nghiệp vụ nào.',
    'xoa_tieu_de': 'Xác nhận xóa', 'xoa_cau': "Bạn có chắc muốn xóa '<tên dịch vụ / chi phí>'?",
    'khoa_hien': 'Chỉ hiện với quyền Quản lý và dòng KHÔNG phải chi phí hệ thống. Dòng đang Hoạt động hiện “Khóa” (khóa được cả dòng đang được sử dụng), dòng đang Khóa hiện “Mở khóa”.',
    'khoa_tieu_de': '“Xác nhận khóa” hoặc “Xác nhận mở khóa” theo thao tác.',
    'khoa_cau': "“Bạn có chắc muốn khóa '<tên>'?” / “Bạn có chắc muốn mở khóa '<tên>'?”.",
    'truong_ls': 'Tên, Phân loại, % Tính giá vốn, % VAT, ĐM giảm giá của công ty đang chọn, Trạng thái',
    'quyen_import': 'quyền Quản lý', 'import_tieu_de': 'Import dịch vụ sửa chữa và chi phí khác',
    'import_file': 'Mau_import_dich_vu_sua_chua.xlsx',
    'import_cot': 'STT, Tên dịch vụ / chi phí, % Tính giá vốn, % VAT, ĐM giảm giá (%), Có tính doanh thu (chọn Có / Không)',
    'import_cot_bang': 'STT, Tên dịch vụ / chi phí, % Tính giá vốn, % VAT, ĐM giảm giá (%), Có tính doanh thu',
    'doi_tuong_import': 'dịch vụ / chi phí (ĐM giảm giá ghi cho công ty đang chọn)',
    'import_toast': 'Import thành công N dịch vụ sửa chữa và chi phí khác.',
    'import_toast_loi': 'Import thành công x/y dịch vụ sửa chữa và chi phí khác. N dòng thất bại.',
    'xuat_hien': 'Hiện với cả người chỉ có quyền Xem.',
    'xuat_truong': 'Tám trường: ' + _TRUONG_XUAT, 'xuat_so': 8,
    'xuat_theo': 'từ khóa, Phân loại, Trạng thái và thứ tự sắp xếp', 'xuat_file': 'danh_muc_dich_vu_sua_chua_va_chi_phi_khac.xlsx',
    'truong_xem': [('Tên dịch vụ / chi phí', 'Textbox', 'Ô mờ, không gõ được.'),
                   ('% Tính giá vốn / % VAT', 'Number', 'Ô mờ.'),
                   ('ĐM giảm giá (%)', 'Number', 'Ô mờ, mức của công ty đang chọn; trống nếu chưa khai báo.'),
                   ('Trạng thái', 'Dropdown', 'Hoạt động hoặc Khóa, không đổi được.'),
                   ('Dịch vụ có tính doanh thu', 'Checkbox', 'Không tích / bỏ tích được.'),
                   ('Dòng cảnh báo', 'Label', 'Chỉ hiện ở chi phí hệ thống: “Chi phí này nằm trong danh sách không được phép sửa của hệ thống.”')],
    'cot_all': ['STT', 'Tên dịch vụ / chi phí', 'Phân loại', 'ĐM giảm giá', '% Tính giá vốn', '% VAT', 'Người cập nhật',
                'Ngày cập nhật', 'Người tạo', 'Ngày tạo', 'Trạng thái', 'Hành động'],
    'cot_mac_dinh': 'STT, Tên dịch vụ / chi phí, Người tạo, Ngày tạo, Trạng thái, Hành động',
    'cot_khoa': 'STT, Tên dịch vụ / chi phí, Hành động',
})
# Sửa: bổ sung chốt chặn 423 của máy chủ (middleware recordNotLocked, chạy trước cả validate).
for _f in CFG['srs']['fr']:
    if _f['ten'] == 'Chỉnh sửa dịch vụ / chi phí':
        _f['events'][1] = ['Bấm Lưu', 'Click',
                           'Before:\n– Máy chủ chặn nếu dòng đang Khóa (“%s”), không ghi.\n'
                           'During:\n– Kiểm tra như Thêm mới, bỏ qua trùng với chính bản ghi.\n– Có lỗi → báo đỏ dưới ô + “Bạn chưa nhập đầy đủ thông tin”, không thực hiện After.\n'
                           'After:\n– Ghi thay đổi, cập nhật ĐM giảm giá của công ty đang chọn, ghi lịch sử “Thay đổi thông tin” (đổi Trạng thái ghi “Khóa”/“Mở khóa”), báo “Cập nhật thành công”.' % _MSG_LOCKED_COST]
CFG['loi_code'].append('Routes/api.php: middleware recordNotLocked:cost đứng TRƯỚC checkPermission ở PUT/DELETE /costs/{cost} → người chỉ có quyền Xem gọi thẳng API sửa / xóa một dòng đang Khóa nhận 423 “%s” thay vì 403 không có quyền (không ghi được dữ liệu, chỉ sai mã lỗi / lộ trạng thái).' % _MSG_LOCKED_COST)
CFG['loi_code'].append('Cửa sổ “Chọn trường xuất file” không có trường Người cập nhật / Ngày cập nhật (exportFields ở costs/index.vue chỉ 8 trường) dù bảng cho bật 2 cột này ở Cấu hình cột → bật cột rồi Xuất Excel thì file không có 2 cột đó.')
