# -*- coding: utf-8 -*-
# Cấu hình tài liệu màn Danh mục công việc, lỗi thiết bị (phân hệ CSKH sau bán).
# Nguồn: code gop_db 26/09/2026 — FE pages/customer-care/device-errors/{index,create}.vue, _id/{index,edit}.vue,
# components/DeviceErrorFormComponent.vue, utils/mixins/exportFieldsMixin.js, components/modal/export-fields-modal.vue;
# BE Modules/CustomerCare (DeviceErrorController, DeviceErrorService, DeviceErrorRequest, DeviceErrorExport, DeviceError::TYPES/REFERENCE_TABLES),
# App\ExcelExport\ExportColumnRegistry['device_errors'], App\ExcelExport\Support\ExportColumns.
# Màn KHÔNG có Import, KHÔNG có mã (bảng device_errors không có cột mã). Form Thêm/Sửa/Xem là TRANG RIÊNG.
# Không ghi URL. Chữ UI / message lấy nguyên văn code.

DT = 'công việc / lỗi thiết bị'
Q = 'Quản lý danh mục công việc - lỗi thiết bị'
LOAI = 'Lỗi đã xác định, Lỗi chưa xác định, Lắp đặt bàn giao, Thiết kế nền móng, Tư vấn, khảo sát, Giám sát thi công'
TRUONG_XUAT = 'Tên công việc / lỗi thiết bị, Loại, Định mức công, Giá, Chiết khấu (%), Hệ số LN, VAT (%), Ghi chú, Trạng thái'
FILE_XUAT = 'danh-muc-cong-viec-loi-thiet-bi.xlsx'

CFG = {
    'slug': 'device-errors',
    'ten': 'Danh mục công việc, lỗi thiết bị',
    'doi_tuong': DT,
    'form_type': 'page',
    'file_hdsd': 'HDSD_Danh mục công việc, lỗi thiết bị.docx',
    'file_srs': 'SRS - Danh mục công việc, lỗi thiết bị.docx',
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Công việc, lỗi thiết bị', 'menu_muc')],

    'thuat_ngu': [
        ['Công việc / lỗi thiết bị', 'Một hạng mục công việc sửa chữa hoặc một tình trạng lỗi của thiết bị, dùng làm cơ sở lập báo giá dịch vụ và phiếu sửa chữa.'],
        ['Loại công việc / lỗi', 'Sáu nhóm phân loại: %s.' % LOAI],
        ['Định mức công', 'Số công chuẩn để hoàn thành hạng mục, là căn cứ tính Công kỹ thuật và Đơn giá bán tự động.'],
        ['Đơn giá công kỹ thuật', 'Giá của một công kỹ thuật, lấy theo cấu hình của công ty người đang đăng nhập; chỉ xem, không sửa ở màn này.'],
        ['Hệ số giá bán dịch vụ', 'Hệ số nhân khi quy đổi Đơn giá bán, lấy theo cấu hình của công ty; chỉ xem, không sửa ở màn này.'],
        ['Công kỹ thuật', 'Giá trị công hệ thống tự tính = Đơn giá công kỹ thuật × Định mức công; chỉ xem.'],
        ['Hệ số công nghệ', 'Hệ số phản ánh mức độ phức tạp công nghệ, bắt buộc lớn hơn 0 (mặc định 1).'],
        ['Định mức giảm giá (%)', 'Tỷ lệ giảm giá tối đa được phép áp cho hạng mục.'],
        ['VAT (%)', 'Thuế suất giá trị gia tăng áp cho hạng mục, tối đa 100.'],
        ['Đơn giá bán', 'Giá bán của hạng mục. Để trống thì hệ thống tự quy đổi = Định mức công × Đơn giá công kỹ thuật × Hệ số giá bán dịch vụ của công ty.'],
        ['Áp dụng cho thiết bị', 'Danh sách hàng hóa / thiết bị mà hạng mục áp dụng. Bắt buộc ít nhất một.'],
        ['Vật tư thay thế', 'Danh sách hàng hóa dùng để thay thế khi thực hiện hạng mục, không bắt buộc.'],
        ['Dịch vụ sửa chữa', 'Các dịch vụ đi kèm; đã thêm dòng thì phải có Giá vốn và Giá dịch vụ.'],
        ['Đã phát sinh chứng từ', 'Hạng mục đã được dùng ở báo giá dịch vụ, hợp đồng dịch vụ, phiếu giao việc, kết quả sửa chữa hoặc phiếu xử lý yêu cầu bảo hành sửa chữa; khi đó không xóa được.'],
        ['Trạng thái Hoạt động / Khóa', 'Hạng mục đã Khóa không còn chọn được ở nghiệp vụ mới nhưng vẫn nằm trong danh mục, vẫn xem, in và xem lịch sử được.'],
    ],
    'phien_ban': [
        ['1.0', '18/08/2026', 'Đội phát triển phần mềm', 'Lập mới cho màn Danh mục công việc, lỗi thiết bị.'],
        ['1.1', '26/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: menu CSKH sau bán, bộ lọc nhãn nổi, nút ba chấm, cửa sổ Chọn trường xuất file, In danh sách / In chi tiết dạng xem trước, màn Chi tiết có khối Lịch sử; trình bày theo mẫu tài liệu danh mục chung.'],
    ],
    'muc_dich': [
        'Danh mục công việc, lỗi thiết bị là danh mục nền của nghiệp vụ sửa chữa. Mỗi bản ghi là một hạng mục công việc hoặc một tình trạng lỗi của thiết bị, kèm định mức công, các hệ số tính giá, danh sách thiết bị áp dụng, vật tư thay thế và dịch vụ sửa chữa đi kèm.',
        'Dữ liệu của màn này được chọn khi lập báo giá dịch vụ và phiếu sửa chữa, nên mỗi thay đổi ở đây đều ảnh hưởng tới việc báo giá cho khách hàng.',
        'Tên hạng mục là duy nhất TRONG CÙNG MỘT LOẠI — hai loại khác nhau được phép có hạng mục trùng tên. Danh mục không có mã, dùng chung toàn hệ thống, không phân theo công ty / phòng ban.',
    ],
    'quyen': {
        'truoc': ['Màn hình dùng đúng MỘT quyền cho cả xem lẫn thao tác.'],
        'rows': [
            [Q, 'Vào màn hình, xem danh sách, tìm kiếm, xem chi tiết, Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, In danh sách, In chi tiết, Xuất Excel.'],
        ],
        'sau': ['Không có quyền thì mục menu Công việc, lỗi thiết bị không hiển thị và không vào được màn hình. Riêng Xem lịch sử thay đổi không gắn quyền riêng. Máy chủ cũng kiểm tra quyền, nên gọi thẳng chức năng mà bỏ qua giao diện vẫn bị từ chối.'],
    },

    'danh_sach': {
        'mo_ta_vao': 'Hệ thống hiển thị danh sách công việc / lỗi thiết bị, gồm cả bản ghi Hoạt động lẫn Khóa, mặc định 20 dòng mỗi trang, mới tạo nhất lên trước.',
        'bo_cuc': [
            'Khu vực tìm kiếm — ô tìm kiếm nhanh, nút Tìm kiếm nâng cao, nút Tìm kiếm và Làm mới.',
            'Thanh công cụ — nút Tạo mới, In danh sách, Xuất Excel và biểu tượng Cấu hình cột hiển thị.',
            'Bảng danh sách — các cột thông tin, cột Hành động ở cuối, và phân trang bên dưới.',
        ],
        'cot': [
            ['STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'],
            ['Tên công việc / Tình trạng lỗi', 'Luôn hiển thị, sắp xếp được. Bấm vào tên để mở màn Chi tiết; bấm biểu tượng {icon:icon_info} cạnh tên để xem cửa sổ “Hàng hóa áp dụng” (Tên thiết bị, Hãng sản xuất, Model, Mã, Code đặt hàng, Nhóm).'],
            ['Loại công việc / lỗi thiết bị', 'Một trong sáu loại. Mặc định ẩn.'],
            ['Áp dụng cho thiết bị', 'Hiện 2 thiết bị đầu, có liên kết “Xem thêm” / “Thu gọn” khi nhiều hơn. Mặc định ẩn.'],
            ['Định mức công', 'Mặc định ẩn.'],
            ['Công kỹ thuật', 'Dạng 1,234,567. Mặc định ẩn.'],
            ['Đơn giá bán', 'Dạng 1,234,567 — giá đã nhập, hoặc giá tự quy đổi khi để trống. Mặc định ẩn, sắp xếp được.'],
            ['Người cập nhật', 'Người sửa gần nhất. Mặc định ẩn.'],
            ['Ngày cập nhật', 'Mặc định ẩn, sắp xếp được.'],
            ['Người tạo', 'Người đã thêm bản ghi.'],
            ['Ngày tạo', 'Thời điểm thêm, sắp xếp được.'],
            ['Trạng thái', 'Nhãn Hoạt động (xanh) hoặc Khóa (đỏ).'],
            ['Hành động', 'Các nút thao tác của dòng (xem mục 4).'],
        ],
        'hanh_dong': {
            'intro': 'Mỗi dòng có tối đa năm thao tác. Cột chỉ hiện THẲNG hai thao tác đầu tiên còn dùng được, phần còn lại dồn vào nút ba chấm {icon:btn_bacham}.',
            'rows': [
                ['Sửa', 'Bản ghi đang Hoạt động.', 'Mở trang Sửa công việc / lỗi thiết bị.'],
                ['Xóa', 'Bản ghi đang Hoạt động VÀ chưa phát sinh chứng từ.', 'Mở hộp Xác nhận xóa.'],
                ['Khóa / Mở khóa', 'Khóa khi đang Hoạt động; Mở khóa khi đang Khóa.', 'Mở hộp xác nhận đổi trạng thái.'],
                ['In', 'Luôn hiện.', 'Mở cửa sổ xem trước bản in chi tiết của hạng mục.'],
                ['Lịch sử', 'Luôn hiện, không cần quyền riêng.', 'Mở cửa sổ Lịch sử thay đổi.'],
            ],
            'anh': 'Nút ba chấm chứa các thao tác còn lại của dòng',
            'luu_y': ['Vì chỉ hai nút đầu hiện thẳng, dòng xóa được sẽ thấy Sửa và Xóa; dòng đã phát sinh chứng từ thấy Sửa và Khóa; dòng đã Khóa chỉ còn Mở khóa, In, Lịch sử. Nút không dùng được thì ẩn hẳn, không hiện nút mờ — đây là thiết kế, không phải lỗi.'],
        },
        'phan_trang': [
            'Cuối bảng có dòng tổng số bản ghi: là tổng số hạng mục khớp bộ lọc đang áp dụng, không phải tổng toàn danh mục.',
            'Ô Số dòng/trang cho chọn số dòng mỗi trang (mặc định 20). Đổi số dòng thì hệ thống tự quay về trang 1.',
            'Các cột sắp xếp được: Tên công việc / Tình trạng lỗi, Đơn giá bán, Ngày cập nhật, Ngày tạo. Bấm tiêu đề cột để sắp xếp, bấm lần hai để đảo chiều. Khi đang tìm bằng ô tìm nhanh mà chưa bấm sắp xếp, kết quả khớp sát nhất với từ khóa được đưa lên đầu.',
        ],
    },

    'loc': {
        'buoc2': 'Bước 2: Nhập chữ vào ô tìm kiếm nhanh, hoặc bấm Tìm kiếm nâng cao để mở thêm các ô lọc, rồi nhấn Enter hoặc bấm {icon:btn_timkiem}.',
        'rows': [
            ['Ô tìm kiếm nhanh', 'Placeholder “Tìm theo tên công việc/lỗi thiết bị, người tạo...”. Gõ một phần Tên hạng mục hoặc tên Người tạo, không phân biệt hoa thường. Phải nhấn Enter hoặc bấm Tìm kiếm.'],
            ['Loại', 'Chọn một trong sáu loại. Lọc ngay khi chọn.'],
            ['Trạng thái', 'Hoạt động hoặc Khóa. Bỏ trống thì hiện cả hai. Lọc ngay khi chọn.'],
            ['Nhóm hàng hóa', 'Chỉ hiện hạng mục có áp dụng cho thiết bị thuộc nhóm đã chọn. Lọc ngay khi chọn.'],
            ['Tên hoặc mã hàng hóa', 'Gõ tên hoặc mã thiết bị: trả về hạng mục CÓ ÁP DỤNG cho thiết bị đó (không phải hạng mục trùng tên). Bấm Tìm kiếm để lọc.'],
            ['Người tạo / Người cập nhật', 'Chọn nhân viên. Lọc ngay khi chọn.'],
            ['Đơn giá bán', 'Hai ô Từ → Đến, nhập số tiền; được phép chỉ nhập một đầu. So theo đúng giá đang hiện ở cột Đơn giá bán, tính cả hai đầu. Bấm Tìm kiếm để lọc.'],
            ['Định mức công', 'Lọc hạng mục có Định mức công BẰNG đúng giá trị nhập. Bấm Tìm kiếm để lọc.'],
        ],
        'ap_dung': [
            'Các tiêu chí kết hợp theo kiểu VÀ. Mỗi lần áp dụng, danh sách quay về trang 1. Điều kiện lọc được ghi nhớ trong 10 phút khi quay lại màn hình.',
            'Bấm {icon:btn_lammoi} để xóa toàn bộ tiêu chí; danh sách nạp lại đầy đủ ngay lập tức.',
        ],
        'anh_ket_qua': 'Kết quả tìm nhanh (gõ “Kiểm tra”)',
    },

    'form': {
        'kieu': 'trang',
        'buoc_tao': [
            'Bước 1: Truy cập vào màn hình Danh mục công việc, lỗi thiết bị.',
            'Bước 2: Bấm {icon:btn_taomoi}. Hệ thống mở TRANG RIÊNG “Thêm công việc / lỗi thiết bị” gồm khối Thông tin chung và ba bảng: Áp dụng cho thiết bị, Dịch vụ sửa chữa, Vật tư thay thế.',
            'Bước 3: Chọn Loại công việc / lỗi, nhập Tên, Định mức công, Định mức giảm giá (%), VAT (%), kiểm tra Hệ số công nghệ; nhập Đơn giá bán, Ghi chú nếu cần.',
            'Bước 4: Ở khối Áp dụng cho thiết bị bấm nút Thiết bị, tìm và tích chọn thiết bị rồi áp dụng (bắt buộc ít nhất 1). Nếu cần, bấm Chọn ở khối Dịch vụ sửa chữa (rồi nhập Giá vốn, Giá dịch vụ từng dòng) và ở khối Vật tư thay thế.',
            'Bước 5: Bấm {icon:btn_luu} để lưu và quay về danh sách, hoặc {icon:btn_luutieptuc} để lưu rồi nhập tiếp hạng mục khác.',
        ],
        'anh_tao': 'Trang Thêm công việc / lỗi thiết bị',
        'truong': [
            ['Loại công việc / lỗi', 'Ô chọn giá trị', 'Có', 'Trống', 'Chọn 1 trong 6 loại. Bỏ trống báo “Bắt buộc phải nhập” sau khi bấm Lưu.'],
            ['Tên công việc / tình trạng lỗi', 'Ô nhập giá trị', 'Có', 'Trống', 'Duy nhất trong cùng một Loại. Bỏ trống báo “Bắt buộc phải nhập” ngay khi gõ; trùng tên trong cùng loại báo “Đã tồn tại trên hệ thống”.'],
            ['Định mức công', 'Ô nhập số', 'Có', 'Trống', 'Dùng để tự tính Công kỹ thuật và Đơn giá bán.'],
            ['Hệ số giá bán dịch vụ', 'Chỉ xem', '–', 'Theo cấu hình công ty', 'Không sửa được.'],
            ['Định mức giảm giá (%)', 'Ô nhập số', 'Có', 'Trống', 'Bỏ trống báo “Bắt buộc phải nhập”.'],
            ['VAT (%)', 'Ô nhập số', 'Có', 'Trống', 'Lớn hơn 100 báo “Tối đa 100”; nhập chữ báo “Phải là số”.'],
            ['Công kỹ thuật', 'Chỉ xem', '–', 'Tự tính', 'Đơn giá công kỹ thuật × Định mức công.'],
            ['Đơn giá công kỹ thuật', 'Chỉ xem', '–', 'Theo cấu hình công ty', 'Không sửa được.'],
            ['Đơn giá bán', 'Ô nhập tiền', 'Không', 'Trống', 'Gợi ý “Để trống = tự tính theo hệ thống”. Hiển thị dạng 1,234,567. Số âm báo “Không được nhỏ hơn 0”.'],
            ['Hệ số công nghệ', 'Ô nhập số', 'Có', '1', 'Bằng 0 hoặc âm báo “Nhập hệ số lớn hơn 0”.'],
            ['Trạng thái', 'Ô chọn giá trị', 'Không', 'Hoạt động', 'Hoạt động / Khóa.'],
            ['Ghi chú', 'Ô nhập văn bản', 'Không', 'Trống', ''],
            ['Áp dụng cho thiết bị', 'Bảng chọn hàng hóa', 'Có', 'Trống', 'Cột: STT, Tên thiết bị, Hãng sản xuất, Model, Mã, Code đặt hàng, Nhóm. Chưa có dòng nào báo “Bắt buộc phải nhập” ở đầu khối.'],
            ['Dịch vụ sửa chữa', 'Bảng chọn dịch vụ', 'Không', 'Trống', 'Cột: STT, Tên dịch vụ, Giá vốn, Giá dịch vụ. Mỗi dòng phải có Giá vốn và Giá dịch vụ (mặc định 0); bỏ trống báo “Bắt buộc phải nhập”, số âm báo “Không được nhỏ hơn 0” ngay tại ô trong bảng.'],
            ['Vật tư thay thế', 'Bảng chọn hàng hóa', 'Không', 'Trống', 'Cùng bộ cột với bảng thiết bị.'],
        ],
        'sau_truong': ['Tiêu đề khối Dịch vụ sửa chữa có ghi kèm “Hệ số giá bán dịch vụ thuê ngoài” theo cấu hình công ty. Chọn trùng hàng hóa / dịch vụ đã có trong bảng thì hệ thống báo “Các hàng hoá đã có trong danh sách” / “Các dịch vụ đã có trong danh sách”.'],
        'nut': [
            ['Lưu', 'Ghi bản ghi, báo “Thêm mới thành công” (hoặc “Cập nhật thành công” khi sửa) rồi quay về màn danh sách.'],
            ['Lưu và tiếp tục', 'Ghi bản ghi rồi mở lại trang Thêm mới trống để nhập tiếp. Chỉ có khi Tạo mới.'],
            ['Quay lại', 'Về màn danh sách. Nếu đã nhập dở, hệ thống hỏi “Thông tin chưa lưu” — “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”.'],
        ],
        'loi': [
            ['Bắt buộc phải nhập', 'Chưa chọn Loại, chưa nhập Tên / Định mức công / Định mức giảm giá / VAT / Hệ số công nghệ, chưa có thiết bị nào, hoặc dòng dịch vụ thiếu Giá vốn / Giá dịch vụ.'],
            ['Đã tồn tại trên hệ thống', 'Đã có hạng mục cùng Tên trong CÙNG Loại. Đổi tên hoặc kiểm tra lại Loại.'],
            ['Tối đa 100', 'VAT (%) lớn hơn 100.'],
            ['Phải là số', 'VAT (%), Đơn giá bán hoặc Giá vốn / Giá dịch vụ nhập không phải số.'],
            ['Nhập hệ số lớn hơn 0', 'Hệ số công nghệ bằng 0 hoặc âm.'],
            ['Không được nhỏ hơn 0', 'Đơn giá bán, Giá vốn hoặc Giá dịch vụ là số âm.'],
            ['Vui lòng kiểm tra lại dữ liệu nhập', 'Thông báo chung khi còn ô bị lỗi; xem các ô báo đỏ trên trang.'],
        ],
    },

    'sua': {
        'buoc': [
            'Bước 1: Ở cột Hành động của hạng mục đang Hoạt động, bấm {icon:btn_sua} (hoặc bấm {icon:btn_sua_footer} ở màn Chi tiết).',
            'Bước 2: Hệ thống mở trang “Sửa công việc / lỗi thiết bị”, mọi ô và cả ba bảng đã điền sẵn dữ liệu hiện tại.',
            'Bước 3: Cập nhật thông tin cần sửa (quy tắc nhập như Thêm mới). Có thể chọn Trạng thái = Khóa để khóa ngay khi lưu.',
            'Bước 4: Bấm {icon:btn_luu}. Hệ thống báo “Cập nhật thành công” và quay về danh sách. Trang Sửa không có nút Lưu và tiếp tục.',
        ],
        'anh': 'Trang Sửa công việc / lỗi thiết bị',
        'ghi_chu': [
            'Giữ nguyên Tên của chính hạng mục đang sửa thì không bị báo trùng. Đổi Loại sang loại đã có hạng mục cùng tên thì bị chặn “Đã tồn tại trên hệ thống”.',
            'Hạng mục đã Khóa không sửa được: nút Sửa bị ẩn; mở thẳng trang Sửa thì hệ thống báo “Bản ghi đang bị khoá, vui lòng mở khóa trước khi chỉnh sửa.” và chuyển về màn Chi tiết.',
        ],
    },
    'xoa': {
        'buoc': [
            'Bước 1: Ở cột Hành động (hoặc footer màn Chi tiết), Người dùng bấm {icon:btn_xoa}.',
            'Bước 2: Hệ thống hiện hộp “Xác nhận xóa” — “Bạn có chắc chắn muốn xóa "…"?”. Bấm {icon:btn_confirm_xoa}: hệ thống báo “Thao tác thành công”, hạng mục biến mất khỏi danh sách.',
            'Bấm {icon:btn_huy} nếu bấm nhầm. Không có gì thay đổi.',
        ],
        'anh': 'Hộp xác nhận xóa công việc / lỗi thiết bị',
        'ghi_chu': [
            'Nút Xóa chỉ hiện khi hạng mục đang Hoạt động VÀ chưa phát sinh chứng từ (báo giá, hợp đồng dịch vụ, phiếu giao việc, kết quả sửa chữa, phiếu xử lý yêu cầu bảo hành sửa chữa…). Thiếu một trong hai điều kiện thì nút ẩn hẳn.',
            'Nếu hạng mục vừa được người khác dùng vào chứng từ sau lúc Người dùng mở danh sách, bấm Xóa sẽ báo “Không được xóa!” và bản ghi giữ nguyên.',
        ],
    },
    'khoa': {
        'y_nghia': [
            'Hạng mục VẪN nằm trong danh sách, cột Trạng thái hiện chữ Khóa.',
            'Không còn chọn được khi lập báo giá dịch vụ hoặc phiếu sửa chữa mới; chứng từ cũ đang dùng hạng mục vẫn hiển thị đầy đủ.',
            'Nút Sửa và Xóa biến mất; chỉ còn Mở khóa, In, Lịch sử.',
        ],
        'buoc_khoa': [
            'Bước 1: Ở cột Hành động, Người dùng chọn Khóa (trong nút ba chấm nếu dòng có nhiều nút), hoặc bấm Khóa ở footer màn Chi tiết.',
            'Bước 2: Hệ thống hiện hộp “Xác nhận khóa” — “Bạn có chắc chắn muốn khóa "…"?”. Bấm Khóa để xác nhận; hệ thống báo “Thao tác thành công”, cột Trạng thái đổi thành Khóa. Bấm Hủy nếu bấm nhầm.',
        ],
        'buoc_mo': [
            'Bước 1: Ở cột Hành động của hạng mục đang Khóa, Người dùng chọn {icon:btn_mokhoa} (hoặc {icon:btn_mokhoa_footer} ở màn Chi tiết).',
            'Bước 2: Bấm {icon:btn_confirm_mokhoa} trong hộp “Xác nhận mở khóa”. Hệ thống báo “Thao tác thành công”, cột Trạng thái đổi thành Hoạt động và nút Sửa hiện lại.',
        ],
        'ghi_chu': ['Có thể khóa ngay ở trang Sửa bằng cách chọn Trạng thái = Khóa rồi Lưu. Nếu hạng mục vừa bị người khác khóa, thao tác Khóa báo “Chỉ có thể khóa lỗi thiết bị đang hoạt động”.'],
    },
    'lich_su': {
        'buoc': [
            'Xem từ màn danh sách: ở cột Hành động (nút ba chấm), Người dùng chọn Lịch sử. Hệ thống mở cửa sổ “Lịch sử thay đổi”, dòng phụ ghi “Công việc / lỗi thiết bị” và tên hạng mục.',
            'Xem từ màn Chi tiết: khối Lịch sử nằm ở cuối trang.',
        ],
        'ghi_chu': ['Cửa sổ có bộ lọc riêng (loại hành động, người thực hiện, khoảng thời gian). Bản ghi chưa có mốc nào hiện “Chưa có lịch sử thao tác nào.”'],
    },
    'chi_tiet': {
        'buoc': ['Bước 1: Truy cập vào màn hình Danh mục công việc, lỗi thiết bị.',
                 'Bước 2: Bấm vào tên hạng mục ở cột Tên công việc / Tình trạng lỗi. Hệ thống mở TRANG “Chi tiết công việc / lỗi thiết bị”.'],
        'anh': 'Trang Chi tiết công việc / lỗi thiết bị',
        'ghi_chu': ['Trang hiển thị toàn bộ thông tin và ba bảng ở chế độ chỉ đọc, kèm khối Lịch sử ở cuối. Footer có các nút khớp đúng cột Hành động của dòng đó: Sửa (đang Hoạt động), In, Xóa (đang Hoạt động và chưa phát sinh chứng từ), Khóa hoặc Mở khóa, và Quay lại.'],
    },
    'phan_rieng': [
        {'tieu_de': 'IN DANH SÁCH VÀ IN CHI TIẾT', 'noi_dung': [
            ('h2', '1. In danh sách'),
            ('s', 'Bước 1: Lọc đúng dữ liệu cần in (xem PHẦN 2).'),
            ('s', 'Bước 2: Bấm nút In danh sách trên thanh công cụ. Hệ thống mở cửa sổ xem trước “Xem trước danh sách lỗi thiết bị” (khổ ngang) theo mẫu in “Danh sách lỗi thiết bị”, gồm TOÀN BỘ hạng mục khớp bộ lọc (không chỉ trang đang xem) và tiêu đề đầu trang của công ty.'),
            ('s', 'Bước 3: Bấm In trong cửa sổ xem trước để in ra máy in.'),
            ('h2', '2. In chi tiết một hạng mục'),
            ('s', 'Bước 1: Ở cột Hành động (nút ba chấm) chọn In, hoặc bấm {icon:btn_in_footer} ở màn Chi tiết.'),
            ('s', 'Bước 2: Hệ thống mở cửa sổ xem trước theo mẫu in “Chi tiết công việc / lỗi thiết bị”: Loại lỗi, Tình trạng lỗi, Định mức công, các hệ số, Định mức giảm giá, Đơn giá công kỹ thuật, Công kỹ thuật, Đơn giá bán (dạng 1,234,567), Ghi chú và các bảng thiết bị, vật tư, dịch vụ.'),
            ('p', 'Thao tác In dùng được cả với hạng mục đã Khóa.'),
        ]},
    ],
    'xuat': {
        'buoc': [
            'Bước 1: Tìm kiếm / lọc đúng dữ liệu cần lấy (xem PHẦN 2). File xuất chạy theo đúng bộ lọc đang áp dụng.',
            'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ “Chọn trường xuất file”.',
            'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất. Mặc định hệ thống tích sẵn các trường tương ứng cột đang hiển thị trên bảng (ban đầu là Tên công việc / lỗi thiết bị và Trạng thái).',
            'Bước 4: Bấm {icon:btn_xuatfile}. Hệ thống tải về file %s và báo “Xuất Excel thành công”.' % FILE_XUAT,
        ],
        'truong': 'Chọn nhiều trường: %s.' % TRUONG_XUAT,
        'ghi_chu': [
            'Lưu ý: file xuất chứa TOÀN BỘ kết quả lọc, không chỉ các dòng của trang đang xem. Ba dòng đầu file là khối tiêu đề “DANH MỤC CÔNG VIỆC / LỖI THIẾT BỊ”, dòng Ngày xuất và Tổng số bản ghi; bảng bắt đầu từ dòng 4, cột STT luôn đứng đầu. Cột số (Định mức công, Giá, Chiết khấu, Hệ số LN, VAT) là số thật, Giá hiển thị dạng 1,234,567. Kết quả rỗng thì dưới dòng tiêu đề ghi “Không có dữ liệu”.',
            'Nút Xuất Excel chỉ hiện với người có quyền Quản lý danh mục công việc - lỗi thiết bị.',
        ],
    },
    'tuy_chinh_cot': {'cot_khoa': 'Ba cột STT, Tên công việc / Tình trạng lỗi và Hành động'},

    'shots': {'list': '01_list.png', 'rowmenu': '03_rowmenu.png', 'filter': 'filter.png', 'filter_result': '04_filter_result.png',
              'create': '10_create.png', 'create_error': '11_create_error.png', 'edit': '12_edit.png',
              'delete': '13_delete.png', 'lock': '14_lock.png', 'unlock': '15_unlock.png', 'history': '16_history.png',
              'detail': '17_detail.png', 'export': '20_export.png', 'colcfg': '25_colcfg.png'},

    'capture': {'route': '/customer-care/device-errors',
                'menu': {'phanhe': 'CSKH SAU BÁN', 'nhom': 'Danh mục', 'muc': 'Công việc, lỗi thiết bị'},
                'search': 'Tìm theo tên công việc/lỗi thiết bị', 'searchText': 'Kiểm tra', 'detailCol': 1,
                'lockName': 'Kiểm tra tình trạng cầu',
                'create': True, 'lock': True},

    'uml': {
        'mains': [('FR-01', 'Xem danh sách công việc / lỗi thiết bị', 'view'), ('FR-03', 'Thêm mới công việc / lỗi thiết bị', 'crud'),
                  ('FR-04', 'Chỉnh sửa công việc / lỗi thiết bị', 'crud'), ('FR-05', 'Xóa công việc / lỗi thiết bị', 'action'),
                  ('FR-06', 'Khóa / Mở khóa', 'action'), ('FR-08', 'Xuất danh sách ra Excel', 'io'), ('FR-09', 'In danh sách / In chi tiết', 'io')],
        'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-10', 'Xem chi tiết', 'view'),
                 ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
        'rieng': [('FR-09', 'In danh sách / In chi tiết', 'io'), ('FR-10', 'Xem chi tiết', 'view')],
    },

    'srs': {
        'muc_dich': ['Là căn cứ nghiệm thu chức năng.',
                     'Làm rõ quy tắc trùng tên theo từng Loại, cách tự tính Công kỹ thuật / Đơn giá bán theo cấu hình công ty, điều kiện xóa (chưa phát sinh chứng từ) và khóa.'],
        'quyen_truoc': ['Màn hình dùng đúng MỘT quyền, không tách quyền xem riêng, không phân quyền theo công ty / phòng ban / bộ phận.'],
        'quyen_rows': [[Q, 'Vào màn hình và thực hiện toàn bộ chức năng: xem, tìm kiếm, xem chi tiết, Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, In, Xuất Excel.']],
        'ma_tran': [['Chức năng', Q]] + [[f, 'Có'] for f in [
            'FR-01 Xem danh sách', 'FR-02 Tìm kiếm và lọc', 'FR-03 Thêm mới', 'FR-04 Chỉnh sửa', 'FR-05 Xóa',
            'FR-06 Khóa / Mở khóa', 'FR-07 Xem lịch sử thay đổi (không cần quyền)', 'FR-08 Xuất Excel',
            'FR-09 In danh sách / In chi tiết', 'FR-10 Xem chi tiết', 'FR-11 Tùy chỉnh cột hiển thị']],
        'ma_tran_widths': [2.6, 2],
        'quyen_sau': ['Nút không dùng được thì ẩn hẳn. Máy chủ kiểm tra quyền ở mọi chức năng xem, ghi, in và xuất; riêng lịch sử không gắn quyền.'],
        'fr': [
            {'ten': 'Xem danh sách công việc / lỗi thiết bị',
             'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của Danh mục công việc, lỗi thiết bị.',
             'gioi_thieu': [['Tên chức năng', 'Xem danh sách công việc / lỗi thiết bị'],
                            ['Mô tả', 'Hiển thị toàn bộ hạng mục (Hoạt động và Khóa), có phân trang, sắp xếp, cấu hình cột.'],
                            ['Tác nhân', 'Người dùng có quyền ' + Q],
                            ['Điều kiện ban đầu', 'Người dùng đã đăng nhập và có quyền của màn hình.'],
                            ['Dòng sự kiện chính', '1. Người dùng vào menu CSKH sau bán → Danh mục → Công việc, lỗi thiết bị.\n2. Hệ thống nạp trang đầu (20 dòng, mới tạo nhất lên trước).\n3. Bảng hiển thị dữ liệu kèm tổng số bản ghi.'],
                            ['Dòng sự kiện phụ', '• Không có bản ghi khớp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n• Bấm biểu tượng ⓘ cạnh tên → cửa sổ “Hàng hóa áp dụng”.\n• Không có quyền → mục menu bị ẩn, không vào được màn hình.']],
             'anh': [('list', 'Màn Danh mục công việc, lỗi thiết bị lúc mới truy cập')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Mô tả'],
                    ['1', 'STT', 'Table/Grid', 'Read-only', 'Chạy liên tục qua các trang, không ẩn được.'],
                    ['2', 'Tên công việc / Tình trạng lỗi', 'Table/Grid', 'Read-only', 'Luôn hiển thị, sắp xếp được. Bấm tên mở màn Chi tiết; icon ⓘ mở “Hàng hóa áp dụng”.'],
                    ['3', 'Loại công việc / lỗi thiết bị', 'Table/Grid', 'Read-only', 'Mặc định ẩn.'],
                    ['4', 'Áp dụng cho thiết bị', 'Table/Grid', 'Read-only', 'Hiện 2 thiết bị đầu + “Xem thêm”. Mặc định ẩn.'],
                    ['5', 'Định mức công / Công kỹ thuật', 'Table/Grid', 'Read-only', 'Mặc định ẩn. Công kỹ thuật dạng 1,234,567.'],
                    ['6', 'Đơn giá bán', 'Table/Grid', 'Read-only', 'Dạng 1,234,567. Mặc định ẩn, sắp xếp được.'],
                    ['7', 'Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'Mặc định ẩn; Ngày cập nhật sắp xếp được.'],
                    ['8', 'Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'Ngày tạo sắp xếp được.'],
                    ['9', 'Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa.'],
                    ['10', 'Hành động', 'Table/Grid', 'Read-only', 'Sửa, Xóa, Khóa/Mở khóa, In, Lịch sử — 2 nút đầu hiện thẳng, còn lại trong nút ba chấm.'],
                    ['11', 'Nút Tạo mới', 'Button', 'Enable', 'Mở trang Thêm công việc / lỗi thiết bị.'],
                    ['12', 'Nút In danh sách', 'Button', 'Enable', 'Mở cửa sổ xem trước bản in danh sách (xem 2.9).'],
                    ['13', 'Nút Xuất Excel', 'Button', 'Enable', 'Mở cửa sổ Chọn trường xuất file (xem 2.8).'],
                    ['14', 'Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', 'Mở cửa sổ Tuỳ chỉnh cột (xem 2.11).'],
                    ['15', 'Phân trang', 'Pagination', 'Enable', 'Mặc định 20 dòng/trang.']],
             'ui_widths': [0.6, 1.5, 0.9, 0.8, 3],
             'events': [['Mở màn hình', 'System', 'After:\n– Nạp trang đầu (mới tạo nhất lên trước), hiển thị tổng số bản ghi.'],
                        ['Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Đổi chiều sắp xếp và nạp lại danh sách từ trang 1.'],
                        ['Chuyển trang', 'Click', 'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'],
                        ['Đổi số dòng mỗi trang', 'Change', 'After:\n– Quay về trang 1 và nạp lại theo số dòng mới.']]},
            {'ten': 'Tìm kiếm và lọc',
             'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Phân trang. Chỉ bổ sung tiêu chí lọc riêng của Danh mục công việc, lỗi thiết bị.',
             'gioi_thieu': [['Tên chức năng', 'Tìm kiếm và lọc'],
                            ['Mô tả', 'Thu hẹp danh sách bằng ô tìm nhanh (Tên, Người tạo) và 8 tiêu chí nâng cao.'],
                            ['Tác nhân', 'Người dùng có quyền ' + Q],
                            ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa hoặc mở Tìm kiếm nâng cao, chọn/nhập tiêu chí.\n2. Ô chọn giá trị lọc ngay khi chọn; ô gõ tay áp dụng khi bấm Tìm kiếm / Enter.\n3. Hệ thống lọc theo kiểu VÀ, nạp lại từ trang 1.'],
                            ['Dòng sự kiện phụ', '• Tên hoặc mã hàng hóa tìm theo THIẾT BỊ ĐƯỢC ÁP DỤNG.\n• Đơn giá bán cho phép nhập một đầu; so theo giá đang hiển thị.\n• Định mức công so BẰNG.\n• Bấm Làm mới → xóa hết tiêu chí và nạp lại ngay.\n• Điều kiện lọc được ghi nhớ 10 phút.']],
             'anh': [('filter', 'Khu vực tìm kiếm và bộ lọc nâng cao')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Mô tả'],
                    ['1', 'Ô tìm kiếm nhanh', 'Textbox', 'Enable', '–', 'Placeholder “Tìm theo tên công việc/lỗi thiết bị, người tạo...”.'],
                    ['2', 'Loại', 'Dropdown', 'Enable', '6 loại', 'Lọc ngay khi chọn.'],
                    ['3', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Bỏ trống = cả hai.'],
                    ['4', 'Nhóm hàng hóa', 'Dropdown', 'Enable', '–', 'Hạng mục có thiết bị thuộc nhóm.'],
                    ['5', 'Tên hoặc mã hàng hóa', 'Textbox', 'Enable', '–', 'Hạng mục có áp dụng cho thiết bị khớp.'],
                    ['6', 'Người tạo / Người cập nhật', 'Dropdown', 'Enable', '–', 'Chọn nhân viên.'],
                    ['7', 'Đơn giá bán', 'Currency (Từ → Đến)', 'Enable', '≥ 0', 'Tính cả hai đầu, cho phép một đầu.'],
                    ['8', 'Định mức công', 'Number', 'Enable', '–', 'So bằng.'],
                    ['9', 'Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', 'Áp dụng / xóa toàn bộ tiêu chí.']],
             'ui_widths': [0.6, 1.3, 0.9, 0.7, 1, 2.4]},
            {'ten': 'Thêm mới công việc / lỗi thiết bị', 'uc': 'uc_fr03',
             'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Thêm mới công việc / lỗi thiết bị'],
                            ['Mô tả', 'Thêm một hạng mục mới trên TRANG RIÊNG, gồm thông tin chung và ba bảng con.'],
                            ['Tác nhân', 'Người dùng có quyền ' + Q],
                            ['Điều kiện ban đầu', 'Đang ở màn Danh mục công việc, lỗi thiết bị.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở trang “Thêm công việc / lỗi thiết bị”.\n3. Người dùng nhập thông tin, chọn ít nhất 1 thiết bị, (tuỳ chọn) dịch vụ sửa chữa và vật tư thay thế, bấm Lưu.\n4. Hệ thống kiểm tra, ghi bản ghi và ghi lịch sử Tạo mới.\n5. Báo “Thêm mới thành công”, quay về danh sách.'],
                            ['Dòng sự kiện phụ', '• Thiếu trường bắt buộc / chưa có thiết bị → “Bắt buộc phải nhập” tại ô, toast “Vui lòng kiểm tra lại dữ liệu nhập”.\n• Trùng tên trong cùng Loại → “Đã tồn tại trên hệ thống”; khác Loại thì lưu được.\n• Bấm “Lưu và tiếp tục” → ghi rồi mở lại trang trống.\n• Bấm Quay lại khi đã nhập dở → hỏi “Thông tin chưa lưu”.'],
                            ['Yêu cầu đặc biệt', 'Công kỹ thuật, Hệ số giá bán dịch vụ, Đơn giá công kỹ thuật là ô chỉ xem theo cấu hình công ty người đang đăng nhập. Đơn giá bán để trống thì tự quy đổi.']],
             'menu_them': ' => Tạo mới {icon:btn_taomoi}',
             'ghi_chu_layout': 'Thêm mới mở trang riêng (không phải cửa sổ) vì form có ba bảng con.',
             'anh': [('create', 'Trang Thêm công việc / lỗi thiết bị'), ('create_error', 'Lỗi đỏ ngay tại ô còn thiếu')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Mô tả'],
                    ['1', 'Loại công việc / lỗi', 'Dropdown', 'Enable', '6 loại', 'Có', '“Bắt buộc phải nhập”.'],
                    ['2', 'Tên công việc / tình trạng lỗi', 'Textbox', 'Enable', '–', 'Có', 'Duy nhất trong cùng Loại, trùng báo “Đã tồn tại trên hệ thống”.'],
                    ['3', 'Định mức công', 'Number', 'Enable', '–', 'Có', '“Bắt buộc phải nhập”.'],
                    ['4', 'Hệ số giá bán dịch vụ', 'Textbox', 'Disable', '–', '–', 'Theo cấu hình công ty.'],
                    ['5', 'Định mức giảm giá (%)', 'Number', 'Enable', '–', 'Có', '“Bắt buộc phải nhập”.'],
                    ['6', 'VAT (%)', 'Number', 'Enable', '≤ 100', 'Có', '“Tối đa 100”, “Phải là số”.'],
                    ['7', 'Công kỹ thuật', 'Textbox', 'Disable', '–', '–', 'Đơn giá công kỹ thuật × Định mức công.'],
                    ['8', 'Đơn giá công kỹ thuật', 'Textbox', 'Disable', '–', '–', 'Theo cấu hình công ty.'],
                    ['9', 'Đơn giá bán', 'Currency', 'Enable', '≥ 0', 'Không', 'Để trống = tự tính; âm báo “Không được nhỏ hơn 0”.'],
                    ['10', 'Hệ số công nghệ', 'Number', 'Enable', '> 0', 'Có', 'Mặc định 1; ≤ 0 báo “Nhập hệ số lớn hơn 0”.'],
                    ['11', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Mặc định Hoạt động.'],
                    ['12', 'Ghi chú', 'Textarea', 'Enable', '–', 'Không', ''],
                    ['13', 'Bảng Áp dụng cho thiết bị', 'Table', 'Enable', '≥ 1 dòng', 'Có', 'Nút Thiết bị mở cửa sổ tìm hàng hóa.'],
                    ['14', 'Bảng Dịch vụ sửa chữa', 'Table', 'Enable', '–', 'Không', 'Mỗi dòng bắt buộc Giá vốn, Giá dịch vụ ≥ 0.'],
                    ['15', 'Bảng Vật tư thay thế', 'Table', 'Enable', '–', 'Không', ''],
                    ['16', 'Nút Lưu / Lưu và tiếp tục / Quay lại', 'Button', 'Enable', '', '', 'Nằm ở footer trang.']],
             'ui_widths': [0.5, 1.5, 0.8, 0.6, 0.9, 0.5, 2.2],
             'events': [['Bấm Lưu', 'Click', 'During:\n– Kiểm tra bắt buộc, trùng tên trong cùng Loại, VAT ≤ 100, Hệ số công nghệ > 0, số không âm, ít nhất 1 thiết bị, Giá vốn / Giá dịch vụ của từng dòng dịch vụ.\n– Có lỗi → báo đỏ tại ô, không thực hiện After.\nAfter:\n– Ghi bản ghi (mặc định Hoạt động), ghi lịch sử Tạo mới.\n– Báo “Thêm mới thành công”, quay về danh sách.'],
                        ['Bấm Lưu và tiếp tục', 'Click', 'During:\n– Như nút Lưu.\nAfter:\n– Ghi bản ghi, mở lại trang Thêm mới trống.'],
                        ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách. Đã nhập → hỏi “Thông tin chưa lưu”.']]},
            {'ten': 'Chỉnh sửa công việc / lỗi thiết bị', 'uc': 'uc_fr04',
             'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Chỉnh sửa công việc / lỗi thiết bị'],
                            ['Mô tả', 'Sửa một hạng mục đang Hoạt động trên trang Sửa (dùng chung form Thêm mới).'],
                            ['Tác nhân', 'Người dùng có quyền ' + Q],
                            ['Điều kiện ban đầu', 'Hạng mục đang ở trạng thái Hoạt động.'],
                            ['Dòng sự kiện chính', '1. Bấm Sửa ở dòng cần sửa (hoặc ở footer màn Chi tiết).\n2. Hệ thống mở trang “Sửa công việc / lỗi thiết bị” với dữ liệu hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi, ghi lịch sử.\n5. Báo “Cập nhật thành công”, quay về danh sách.'],
                            ['Dòng sự kiện phụ', '• Giữ nguyên tên → không báo trùng; đổi Loại sang loại đã có cùng tên → “Đã tồn tại trên hệ thống”.\n• Xóa hết thiết bị → “Bắt buộc phải nhập”.\n• Hạng mục đã Khóa → nút Sửa ẩn; mở thẳng trang Sửa → “Bản ghi đang bị khoá, vui lòng mở khóa trước khi chỉnh sửa.” và chuyển về Chi tiết.']],
             'menu_them': ' => Sửa {icon:btn_sua}',
             'anh': [('edit', 'Trang Sửa công việc / lỗi thiết bị')]},
            {'ten': 'Xóa công việc / lỗi thiết bị', 'uc': 'uc_fr05',
             'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Xóa công việc / lỗi thiết bị'],
                            ['Mô tả', 'Xóa hẳn hạng mục đang Hoạt động và chưa phát sinh chứng từ, kèm các dòng thiết bị, vật tư, dịch vụ của nó.'],
                            ['Tác nhân', 'Người dùng có quyền ' + Q],
                            ['Điều kiện ban đầu', 'Hạng mục đang Hoạt động và chưa được dùng ở chứng từ nào.'],
                            ['Dòng sự kiện chính', '1. Bấm Xóa.\n2. Hệ thống hiện “Xác nhận xóa” nêu rõ tên hạng mục.\n3. Bấm Xóa.\n4. Hệ thống xóa, báo “Thao tác thành công”, nạp lại danh sách.'],
                            ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Đã Khóa hoặc đã phát sinh chứng từ → nút Xóa ẩn hẳn.\n• Vừa bị người khác dùng vào chứng từ → báo “Không được xóa!”.']],
             'menu_them': ' => Xóa {icon:btn_xoa}',
             'anh': [('delete', 'Hộp xác nhận xóa')]},
            {'ten': 'Khóa / Mở khóa', 'uc': 'uc_fr06',
             'qtc': 'Quy tắc Khóa / Mở khóa danh mục, Thông báo và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Khóa / Mở khóa'],
                            ['Mô tả', 'Ngừng / cho phép dùng hạng mục ở nghiệp vụ mới mà không xóa dữ liệu.'],
                            ['Tác nhân', 'Người dùng có quyền ' + Q],
                            ['Dòng sự kiện chính', '1. Chọn Khóa (hoặc Mở khóa) ở nút ba chấm hay footer màn Chi tiết.\n2. Hệ thống hiện “Xác nhận khóa” / “Xác nhận mở khóa” nêu rõ tên.\n3. Bấm Khóa / Mở khóa → báo “Thao tác thành công”, đổi Trạng thái, ghi lịch sử nhóm Thay đổi trạng thái.'],
                            ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Hạng mục vừa bị người khác khóa → “Chỉ có thể khóa lỗi thiết bị đang hoạt động”.\n• Sau khi Khóa, Sửa và Xóa ẩn; hạng mục không còn chọn được ở báo giá / phiếu sửa chữa mới.']],
             'menu_them': ' => Khóa / Mở khóa {icon:btn_mokhoa}',
             'anh': [('lock', 'Hộp xác nhận khóa'), ('unlock', 'Hộp xác nhận mở khóa')]},
            {'ten': 'Xem lịch sử thay đổi',
             'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Xem lịch sử thay đổi'],
                            ['Mô tả', 'Liệt kê các lần tạo, sửa, đổi trạng thái của một hạng mục, kèm giá trị cũ → mới, người thực hiện, thời điểm.'],
                            ['Tác nhân', 'Mọi người dùng vào được màn hình (không gắn quyền riêng)'],
                            ['Dòng sự kiện chính', '1. Chọn Lịch sử ở nút ba chấm, hoặc cuộn tới khối Lịch sử ở màn Chi tiết.\n2. Hệ thống hiện cửa sổ “Lịch sử thay đổi”, mốc mới nhất trên cùng.'],
                            ['Dòng sự kiện phụ', '• Chưa có mốc nào → “Chưa có lịch sử thao tác nào.”']],
             'menu_them': ' => Lịch sử',
             'anh': [('history', 'Cửa sổ Lịch sử thay đổi')]},
            {'ten': 'Xuất danh sách ra Excel', 'uc': 'uc_fr08',
             'qtc': 'Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của Danh mục công việc, lỗi thiết bị.',
             'gioi_thieu': [['Tên chức năng', 'Xuất danh sách ra Excel'],
                            ['Mô tả', 'Xuất kết quả đang lọc ra file Excel, cho phép chọn trường và thứ tự cột.'],
                            ['Tác nhân', 'Người dùng có quyền ' + Q],
                            ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở “Chọn trường xuất file”, tích sẵn các trường tương ứng cột đang hiển thị.\n3. Người dùng tích chọn và kéo ☰ để sắp thứ tự.\n4. Bấm Xuất file; hệ thống tải %s theo đúng bộ lọc, thứ tự sắp xếp và thứ tự trường, báo “Xuất Excel thành công”.' % FILE_XUAT],
                            ['Dòng sự kiện phụ', '• Bỏ chọn hết → nút Xuất file không bấm được.\n• Bấm Đóng → không xuất gì.\n• Kết quả rỗng → dưới dòng tiêu đề ghi “Không có dữ liệu”.\n• Lỗi máy chủ → “Lỗi khi xuất Excel”.'],
                            ['Yêu cầu đặc biệt', 'File chứa toàn bộ kết quả lọc; 3 dòng đầu là khối tiêu đề (tên danh mục, Ngày xuất, Tổng số), bảng từ dòng 4; STT luôn đứng đầu; cột số là số thật.']],
             'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
             'anh': [('export', 'Cửa sổ Chọn trường xuất file')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
                    ['1', 'Danh sách trường', 'Checkbox chọn nhiều', 'Enable', 'Tích sẵn cột đang hiển thị', TRUONG_XUAT + '. Kéo ☰ đổi thứ tự.'],
                    ['2', 'Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', 'Hiển thị', 'Tích / bỏ tích toàn bộ.'],
                    ['3', 'Nút Xuất file', 'Button', 'Enable/Disable', 'Mờ khi chưa chọn trường', 'Sinh file và tải về.'],
                    ['4', 'Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.']],
             'ui_widths': [0.6, 1.5, 1, 0.8, 1.2, 2.6]},
            {'ten': 'In danh sách / In chi tiết', 'uc': 'uc_fr09',
             'qtc': 'Quy tắc In và mẫu in dùng chung.',
             'gioi_thieu': [['Tên chức năng', 'In danh sách / In chi tiết'],
                            ['Mô tả', 'In danh sách theo mẫu “Danh sách lỗi thiết bị” (toàn bộ kết quả lọc) hoặc in một hạng mục theo mẫu “Chi tiết công việc / lỗi thiết bị”.'],
                            ['Tác nhân', 'Người dùng có quyền ' + Q],
                            ['Dòng sự kiện chính', '1. Bấm In danh sách (thanh công cụ) hoặc In (nút ba chấm / footer Chi tiết).\n2. Hệ thống mở cửa sổ xem trước bản in.\n3. Người dùng bấm In.'],
                            ['Dòng sự kiện phụ', '• Hạng mục đã Khóa vẫn in được.\n• In danh sách lấy toàn bộ dòng khớp bộ lọc, không theo trang.']],
             'menu_them': ' => In danh sách'},
            {'ten': 'Xem chi tiết', 'uc': 'uc_fr10',
             'qtc': 'Màn Xem chi tiết và Phân quyền.',
             'gioi_thieu': [['Tên chức năng', 'Xem chi tiết'],
                            ['Mô tả', 'Trang “Chi tiết công việc / lỗi thiết bị” hiển thị toàn bộ thông tin và ba bảng ở chế độ chỉ đọc, kèm khối Lịch sử.'],
                            ['Tác nhân', 'Người dùng có quyền ' + Q],
                            ['Dòng sự kiện chính', '1. Bấm tên hạng mục ở danh sách.\n2. Hệ thống mở trang Chi tiết; footer có Sửa, In, Xóa, Khóa / Mở khóa, Quay lại — khớp điều kiện của cột Hành động.']],
             'anh': [('detail', 'Trang Chi tiết công việc / lỗi thiết bị')]},
            {'ten': 'Tùy chỉnh cột hiển thị',
             'qtc': 'Tùy chỉnh cột.',
             'gioi_thieu': [['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
                            ['Mô tả', 'Bật/tắt và sắp xếp thứ tự cột của bảng; cấu hình lưu riêng theo người dùng.'],
                            ['Yêu cầu đặc biệt', 'Cột STT, Tên công việc / Tình trạng lỗi, Hành động bị khóa. Mặc định ẩn 7 cột: Loại, Áp dụng cho thiết bị, Định mức công, Công kỹ thuật, Đơn giá bán, Người cập nhật, Ngày cập nhật.']],
             'menu_them': ' => Cấu hình cột {icon:btn_cauhinhcot}',
             'anh': [('colcfg', 'Cửa sổ Tuỳ chỉnh cột')]},
        ],
        'quy_tac': [
            ('BR-01', 'Ràng buộc trùng tên trong cùng Loại',
             ['Tên hạng mục không được trùng trong cùng một Loại; khác Loại thì được trùng tên.',
              'Khi sửa, bản ghi đang sửa được loại khỏi phép so trùng; đổi sang Loại khác cũng bị kiểm tra trùng trong Loại mới.',
              'Thông báo khi trùng: “Đã tồn tại trên hệ thống”.'],
             ['Thêm mới công việc / lỗi thiết bị', 'Chỉnh sửa công việc / lỗi thiết bị']),
            ('BR-02', 'Thiết bị và dịch vụ sửa chữa',
             ['Bắt buộc có ít nhất một thiết bị áp dụng.',
              'Bảng Dịch vụ sửa chữa không bắt buộc, nhưng mỗi dòng đã thêm phải có Giá vốn và Giá dịch vụ ≥ 0.',
              'Hệ số công nghệ phải lớn hơn 0 (“Nhập hệ số lớn hơn 0”); VAT (%) tối đa 100.'],
             ['Thêm mới công việc / lỗi thiết bị', 'Chỉnh sửa công việc / lỗi thiết bị']),
            ('BR-03', 'Quy đổi Đơn giá bán',
             ['Đơn giá bán có nhập (> 0) thì dùng đúng giá đã nhập.',
              'Đơn giá bán để trống thì quy đổi = Định mức công × Đơn giá công kỹ thuật × Hệ số giá bán dịch vụ của công ty người đang đăng nhập — hai người ở hai công ty có thể thấy giá khác nhau.',
              'Bộ lọc Đơn giá bán từ / đến so theo đúng giá đang hiển thị ở cột Đơn giá bán.'],
             ['Xem danh sách công việc / lỗi thiết bị', 'Tìm kiếm và lọc', 'Xuất danh sách ra Excel', 'In danh sách / In chi tiết']),
            ('BR-04', 'Điều kiện xóa',
             ['Chỉ xóa được hạng mục đang Hoạt động và chưa phát sinh ở báo giá / hợp đồng dịch vụ, phân công, kết quả nhập, biên bản bảo hành, phiếu xử lý yêu cầu bảo hành sửa chữa, tiến độ công việc.',
              'Máy chủ kiểm tra lại tại thời điểm xóa; không thỏa thì báo “Không được xóa!”.',
              'Xóa hạng mục xóa luôn danh sách thiết bị áp dụng và dịch vụ sửa chữa kèm theo.'],
             ['Xóa công việc / lỗi thiết bị']),
            ('BR-05', 'Bản ghi đang Khóa',
             ['Chỉ khóa được hạng mục đang Hoạt động (“Chỉ có thể khóa lỗi thiết bị đang hoạt động”); có thể khóa ngay trong form Sửa.',
              'Hạng mục đang Khóa không sửa, không xóa được (máy chủ chặn), báo “Bản ghi đang bị khoá, vui lòng khôi phục trước khi cập nhật.”; chỉ còn Mở khóa, In, Lịch sử.',
              'Hạng mục đang Khóa không còn chọn được ở nghiệp vụ mới; chứng từ cũ vẫn giữ nguyên.'],
             ['Chỉnh sửa công việc / lỗi thiết bị', 'Xóa công việc / lỗi thiết bị', 'Khóa / Mở khóa', 'Phiếu xử lý yêu cầu bảo hành sửa chữa', 'Báo giá dịch vụ']),
            ('BR-06', 'Ghi lịch sử thay đổi',
             ['Mọi thao tác Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa đều ghi lịch sử kèm người thực hiện.',
              'Khóa ngay trong form Sửa được ghi thành dòng Thay đổi trạng thái riêng.'],
             ['Thêm mới công việc / lỗi thiết bị', 'Chỉnh sửa công việc / lỗi thiết bị', 'Xóa công việc / lỗi thiết bị', 'Khóa / Mở khóa', 'Xem lịch sử thay đổi']),
            ('BR-07', 'Phạm vi Xuất Excel và In danh sách',
             ['Xuất Excel và In danh sách lấy toàn bộ kết quả theo bộ lọc đang áp dụng, không giới hạn ở trang đang xem.',
              'Danh mục dùng chung toàn hệ thống, không lọc theo công ty / phòng ban.'],
             ['Xuất danh sách ra Excel', 'In danh sách / In chi tiết']),
        ],
    },
}

CFG['loi_code'] = [
    'Xuất Excel bỏ qua phần lớn bộ lọc: DeviceErrorExport::collection() chỉ áp name/type/status/created_by — KHÔNG áp Nhóm hàng hóa, Tên hoặc mã hàng hóa, Người cập nhật, Đơn giá bán từ–đến, Định mức công (trong khi danh sách và In danh sách dùng chung DeviceErrorService::filteredQuery() đủ 8 tiêu chí). Ô tìm nhanh trong file xuất cũng chỉ so Tên, không so Người tạo như danh sách. Thứ tự sắp xếp luôn created_at desc, bỏ qua cột đang sắp xếp. Tài liệu đã tả đúng thiết kế: file theo đúng bộ lọc và thứ tự đang áp dụng.',
    'Xuất Excel luôn xuất đủ 4 cột Chiết khấu (%), Hệ số LN, VAT (%), Ghi chú: DeviceErrorExport::columnDefinitions() khai 4 cột này `always => true` nên ExportColumns::filter() luôn chèn lại, dù cửa sổ “Chọn trường xuất file” cho bỏ tích (bỏ tích không có tác dụng, kéo đổi thứ tự cũng không dời được 4 cột này).',
    'Cửa sổ “Chọn trường xuất file” không có trường Người tạo / Ngày tạo (ExportColumnRegistry[device_errors] và DeviceErrorExport không khai), dù 2 cột này đang hiện mặc định trên bảng → tích sẵn chỉ còn Tên công việc / lỗi thiết bị và Trạng thái. Tên trường cũng lệch tiêu đề cột trên bảng: “Giá” (bảng: Đơn giá bán), “Loại” (bảng: Loại công việc / lỗi thiết bị).',
    'Import: màn KHÔNG có chức năng Import Excel (không nút, không route) nên lỗi “đánh số dòng lệch 1” không áp dụng cho màn này.',
    'Thông báo sau Xóa / Khóa / Mở khóa là câu chung “Thao tác thành công” (FE index.vue & DeviceErrorFormComponent.vue không dùng message BE “Xóa thành công” / “Khóa thành công” / “Khôi phục thành công”). Message BE khi sửa bản ghi khóa ghi “vui lòng khôi phục” trong khi nút là “Mở khóa”. Ghi nhận, không phải lỗi chặn.',
    'Dòng “Không có dữ liệu” dưới 3 bảng con của form dùng class text-muted → hiện màu ĐỎ (quy ước CLAUDE.md: text-muted trong hrm-client là đỏ).',
]

CFG['tc_ngoai_pham_vi'] = [
    'Toàn tab: còn ghi menu cũ “Chăm sóc khách hàng → Danh mục → Công việc, lỗi thiết bị” (G19, G20, G29, B8…) — nay là CSKH sau bán → Danh mục → Công việc, lỗi thiết bị. G21 (TC-ROLE-02) còn ghi đường dẫn /customer-care/device-errors — tài liệu không được ghi URL.',
    'Tên quyền trong tab viết “Quản lý danh mục công việc- lỗi thiết bị” — tên đúng là “Quản lý danh mục công việc - lỗi thiết bị” (có dấu cách hai bên gạch).',
    'TC_04.001 (R64): “Có 11 ô nhập” — form hiện có 12 ô (thêm Trạng thái, trong đó 3 ô chỉ xem: Hệ số giá bán dịch vụ, Công kỹ thuật, Đơn giá công kỹ thuật).',
    'TC_04.015 / TC_04.017 (R78, R80): Công kỹ thuật và Hệ số giá bán dịch vụ nay là ô CHỈ XEM (không nhập / để trống được) — cần viết lại thành kiểm tra giá trị tự tính.',
    'TC_04.012 / TC_05.007 (R75, R97): thông báo khi chưa có thiết bị là “Bắt buộc phải nhập” ở đầu khối Áp dụng cho thiết bị.',
    'TC_04.013 / TC_05.004 / TC_05.005 (R76, R94, R95): thông báo trùng tên là “Đã tồn tại trên hệ thống”.',
    'TC_06.004–TC_06.006, TC_07.002, TC_07.005 (R104–R106, R110, R113): tiêu đề hộp “Xác nhận xóa/khóa/mở khóa”, câu “Bạn có chắc chắn muốn … "…"?”, toast thành công là “Thao tác thành công”.',
    'TC_07.009 / TC_10.002 (R117, R137): khóa bản ghi đã bị khóa báo “Chỉ có thể khóa lỗi thiết bị đang hoạt động”; lưu trang Sửa của bản ghi vừa bị khóa báo “Bản ghi đang bị khoá, vui lòng khôi phục trước khi cập nhật.”.',
    'TC_02.002 (R41): nhãn bộ lọc là “Người cập nhật” (không phải “Người sửa”); các case có số tiền (R48, R49) còn viết kiểu 100.000 — nay định dạng 100,000.',
    'Chưa có case cho màn Chi tiết (trang riêng, footer Sửa/In/Xóa/Khóa/Mở khóa, khối Lịch sử) và cửa sổ “Hàng hóa áp dụng” (icon ⓘ cạnh tên).',
]

# ---- Sửa tab testcase "22. DM công việc, lỗi thiết bị" (đọc từ ref/testcase_tab.txt) ----
_Q = 'Tài khoản có quyền "%s".' % Q
_XF = 'Bấm Xuất Excel → cửa sổ “Chọn trường xuất file” → bấm Xuất file'
CFG['tc'] = {
    'tab': '22. DM công việc, lỗi thiết bị',
    'hdr_row': 118,            # "VIII. IN VÀ XUẤT TỆP BẢNG TÍNH"
    'blocks': [
        # case mới cuối nhóm VIII (case đầu R119, case cuối TC_08.010 ở R128)
        {'after': 128, 'merge_from': 119, 'cases': [
            ('TC_08.011', 'Mở cửa sổ Chọn trường xuất file', 'P0', _Q + ' Chưa chỉnh cấu hình cột.',
             '1. Bấm nút Xuất Excel\n2. Đọc danh sách trường trong cửa sổ', '',
             '- Mở cửa sổ “Chọn trường xuất file”\n- Có đủ 9 trường: %s\n- Tích sẵn các trường tương ứng cột đang hiển thị trên bảng\n- Dòng cuối ghi “Đang chọn a/9 trường”' % TRUONG_XUAT),
            ('TC_08.012', 'Bỏ tích một trường', 'P1', _Q,
             '1. Bấm Xuất Excel, tích thêm Loại và Ghi chú\n2. Bỏ tích trường Ghi chú\n3. Bấm Xuất file, mở file', '',
             '- File KHÔNG có cột Ghi chú, các cột còn lại giữ nguyên\n- Cột STT vẫn đứng đầu bảng'),
            ('TC_08.013', 'Đổi thứ tự cột bằng kéo ☰', 'P2', _Q,
             '1. Bấm Xuất Excel, tích thêm Loại\n2. Kéo biểu tượng ☰ của Loại lên trên Tên công việc / lỗi thiết bị\n3. Bấm Xuất file, mở file', '',
             '- Trong file, cột Loại đứng ngay sau STT, trước Tên công việc / lỗi thiết bị — đúng thứ tự vừa kéo'),
            ('TC_08.014', 'Chọn tất cả / Bỏ chọn hết', 'P2', _Q,
             '1. Bấm Xuất Excel\n2. Bấm Bỏ chọn hết, quan sát nút Xuất file\n3. Bấm Chọn tất cả', '',
             '- Bỏ chọn hết: không trường nào được tích, nút Xuất file không bấm được\n- Chọn tất cả: tích đủ 9 trường, dòng cuối “Đang chọn 9/9 trường”'),
            ('TC_08.015', 'Cột đang hiện trên bảng thì được tích sẵn', 'P2', _Q,
             '1. Bật cột Định mức công và Đơn giá bán ở Cấu hình cột hiển thị\n2. Bấm Xuất Excel', '',
             '- Trường Định mức công và Giá được tích sẵn cùng Tên công việc / lỗi thiết bị, Trạng thái'),
            ('TC_08.016', 'File xuất theo bộ lọc nâng cao', 'P0', _Q + ' Có hạng mục áp dụng cho thiết bị thuộc nhiều nhóm hàng hóa khác nhau.',
             '1. Mở Tìm kiếm nâng cao, chọn Nhóm hàng hóa\n2. Ghi lại tổng số bản ghi ở cuối bảng\n3. ' + _XF + '\n4. Đếm số dòng dữ liệu trong file',
             'Nhóm hàng hóa: (một nhóm có dữ liệu)',
             '- Số dòng dữ liệu trong file bằng tổng số bản ghi ở cuối bảng\n- Chỉ có các hạng mục áp dụng cho thiết bị thuộc nhóm đã chọn'),
            ('TC_08.017', 'File xuất theo thứ tự sắp xếp đang áp dụng', 'P2', _Q,
             '1. Bấm tiêu đề cột Tên công việc / Tình trạng lỗi để sắp xếp tăng dần\n2. ' + _XF + '\n3. So 5 dòng đầu file với 5 dòng đầu bảng', '',
             '- Thứ tự các dòng trong file giống thứ tự trên bảng'),
            ('TC_08.018', 'Khối tiêu đề của file xuất', 'P2', _Q,
             '1. ' + _XF + '\n2. Mở file, đọc 4 dòng đầu', '',
             '- Dòng 1: “DANH MỤC CÔNG VIỆC / LỖI THIẾT BỊ”\n- Dòng 2: “Ngày xuất: dd/mm/yyyy hh:mm | Tổng số: N bản ghi”, N bằng số dòng dữ liệu\n- Dòng 4 là tiêu đề cột, có bộ lọc nhanh và được cố định khi cuộn'),
            ('TC_08.019', 'Bấm Đóng thì không xuất', 'P2', _Q,
             '1. Bấm Xuất Excel\n2. Bấm Đóng', '', '- Cửa sổ đóng, không tải file nào'),
        ]},
    ],
    'edits': [
        ('G119', '1. Chọn Loại và Trạng thái ở Tìm kiếm nâng cao\n2. ' + _XF + '\n3. Mở file, đếm số dòng dữ liệu'),
        ('I119', '- Tải về file %s, thông báo “Xuất Excel thành công”\n- Tệp có đúng 25 dòng dữ liệu (không kể khối tiêu đề và dòng tiêu đề cột)\n- Xuất theo bộ lọc chứ không xuất toàn danh mục' % FILE_XUAT),
        ('G120', '1. Đứng ở trang 2\n2. ' + _XF + '\n3. Đếm số dòng trong tệp'),
        ('G121', '1. Bấm Xuất Excel, tích thêm trường VAT (%)\n2. Bấm Xuất file\n3. Tìm cột VAT (%), đối chiếu hai hạng mục trên'),
        ('I121', '- Cột “VAT (%)” có mặt trong tệp và đúng giá trị của từng hạng mục (8 và 10)'),
        ('F122', 'Có hạng mục với đơn giá bán 1,500,000.'),
        ('G122', '1. Bấm Xuất Excel, tích thêm trường Giá\n2. Bấm Xuất file\n3. Đọc ô cột Giá của hạng mục đó'),
        ('I122', '- Ô Giá hiển thị 1,500,000, là kiểu số, tính toán được (SUM ra đúng)\n- Không bị cảnh báo lưu số dưới dạng chữ'),
        ('G123', '1. ' + _XF + '\n2. Mở tệp bằng phần mềm bảng tính'),
        ('G124', '1. ' + _XF + '\n2. Mở tệp'),
        ('I124', '- Không báo lỗi kỹ thuật\n- Tệp vẫn có khối tiêu đề (Tổng số: 0 bản ghi) và dòng tiêu đề cột, bên dưới ghi “Không có dữ liệu”'),
        ('G140', '1. Lọc theo Loại và Trạng thái\n2. Bật thêm cột Đơn giá bán và Định mức công ở Cấu hình cột hiển thị\n3. Bấm Xuất Excel, kiểm tra trường Giá và Định mức công đã được tích sẵn\n4. Bấm Xuất file, mở tệp đối chiếu với lưới'),
        ('I140', '- Cửa sổ “Chọn trường xuất file” tích sẵn Tên công việc / lỗi thiết bị, Định mức công, Giá, Trạng thái\n- Số dòng trong tệp khớp tổng số bản ghi của bộ lọc\n- Dữ liệu từng dòng khớp với lưới'),
    ],
    'clear_k': [119, 120, 121, 122, 123, 124, 140],
}


# ==== Bổ sung “Mô tả chi tiết giao diện” + “Danh sách event và xử lý event” cho MỌI FR của SRS (28/09/2026) ====
# Bám khuôn SRS Danh mục quốc gia. Nguồn: pages/customer-care/device-errors/index.vue, _id/{index,edit}.vue,
# components/DeviceErrorFormComponent.vue (mode show/edit, V2Footer), base-confirm-modal, CatalogHistoryModal +
# SystemInfoSection, export-fields-modal, column-customization-modal, ReportPrintPreviewModal + reportPrintPreviewMixin;
# BE DeviceErrorController (update 423, printList mẫu 279, printDetail mẫu 280), DeviceErrorService (delete/lock/restore,
# buildPrintTable + printListColumnDefinitions).
_UNSAVED = '“Thông tin chưa lưu” — “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại)'
_MSG_423 = 'Bản ghi đang bị khoá, vui lòng khôi phục trước khi cập nhật.'
_W_FORM = [0.5, 1.3, 0.8, 0.7, 0.9, 0.6, 1.0, 2.2]
_W4 = [0.6, 1.6, 1.1, 3]
_W6 = [0.6, 1.5, 1.0, 0.8, 1.3, 2.5]
_FR = {f['ten']: f for f in CFG['srs']['fr']}


def _stt(rows):
    return [rows[0]] + [[str(i)] + r for i, r in enumerate(rows[1:], 1)]


# ---- 2.2 Tìm kiếm và lọc (ui đã có — bổ sung events)
_FR['Tìm kiếm và lọc']['events'] = [
    ['Bấm Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Click',
     'After:\n– Mở / thu gọn khối Tìm kiếm nâng cao (Loại, Trạng thái, Nhóm hàng hóa, Tên hoặc mã hàng hóa, Người tạo, Người cập nhật, Đơn giá bán, Định mức công).\n'
     '– Lần mở đầu tiên mới nạp danh sách Loại và Nhóm hàng hóa.'],
    ['Nhập ô tìm kiếm nhanh / Tên hoặc mã hàng hóa / Đơn giá bán / Định mức công rồi nhấn Enter hoặc bấm Tìm kiếm', 'Click',
     'Before:\n– Gõ mà chưa nhấn Enter / bấm Tìm kiếm thì danh sách chưa lọc.\nAfter:\n– Áp đồng thời mọi tiêu chí theo kiểu “và”, nạp lại bảng từ trang 1, cập nhật tổng số bản ghi.\n'
     '– Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”'],
    ['Chọn Loại / Trạng thái / Nhóm hàng hóa / Người tạo / Người cập nhật', 'Change',
     'After:\n– Lọc ngay, không cần bấm Tìm kiếm; nạp lại bảng từ trang 1.'],
    ['Bấm Làm mới', 'Click', 'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ (mới tạo nhất lên trước).'],
]

# ---- 2.4 Chỉnh sửa (TRANG RIÊNG)
_f = _FR['Chỉnh sửa công việc / lỗi thiết bị']
_f['ui'] = _stt([
    ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả'],
    ['Nút Sửa', 'Icon Button / Button', 'Enable', '–', '–', 'Hiển thị',
     'Ở cột Hành động (hiện thẳng) và chân trang Chi tiết. Chỉ hiện khi có quyền Quản lý danh mục công việc - lỗi thiết bị VÀ hạng mục đang Hoạt động.'],
    ['Tiêu đề trang', 'Label', 'Read-only', '–', '–', '“Sửa công việc / lỗi thiết bị”', 'Trang riêng, dùng chung form với Thêm mới.'],
    ['Loại công việc / lỗi', 'Dropdown', 'Enable', '6 loại', 'Có', 'Dữ liệu hiện tại', 'Bỏ trống “Bắt buộc phải nhập”. Đổi sang loại đã có hạng mục cùng tên → “Đã tồn tại trên hệ thống”.'],
    ['Tên công việc / tình trạng lỗi', 'Textbox', 'Enable', '–', 'Có', 'Dữ liệu hiện tại',
     'Duy nhất trong cùng Loại, bỏ qua chính bản ghi. Bỏ trống “Bắt buộc phải nhập”; trùng “Đã tồn tại trên hệ thống”.'],
    ['Định mức công', 'Number', 'Enable', '–', 'Có', 'Dữ liệu hiện tại', 'Đổi là Công kỹ thuật và Đơn giá bán tự tính lại.'],
    ['Hệ số giá bán dịch vụ', 'Textbox', 'Disable', '–', '–', 'Theo cấu hình công ty', 'Chỉ xem.'],
    ['Định mức giảm giá (%)', 'Number', 'Enable', '–', 'Có', 'Dữ liệu hiện tại', 'Bỏ trống “Bắt buộc phải nhập”.'],
    ['VAT (%)', 'Number', 'Enable', '≤ 100', 'Có', 'Dữ liệu hiện tại', 'Lớn hơn 100 “Tối đa 100”; nhập chữ “Phải là số”.'],
    ['Công kỹ thuật', 'Textbox', 'Disable', '–', '–', 'Tự tính', 'Đơn giá công kỹ thuật × Định mức công, dạng 1,234,567.'],
    ['Đơn giá công kỹ thuật', 'Textbox', 'Disable', '–', '–', 'Theo cấu hình công ty', 'Chỉ xem.'],
    ['Đơn giá bán', 'Currency', 'Enable', '≥ 0', 'Không', 'Dữ liệu hiện tại', 'Để trống = tự tính theo hệ thống; số âm “Không được nhỏ hơn 0”.'],
    ['Hệ số công nghệ', 'Number', 'Enable', '> 0', 'Có', 'Dữ liệu hiện tại', 'Bằng 0 hoặc âm “Nhập hệ số lớn hơn 0”.'],
    ['Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Dữ liệu hiện tại', 'Chọn Khóa rồi Lưu là khóa hạng mục ngay khi lưu.'],
    ['Ghi chú', 'Textarea', 'Enable', '–', 'Không', 'Dữ liệu hiện tại', ''],
    ['Bảng Áp dụng cho thiết bị', 'Table', 'Enable', '≥ 1 dòng', 'Có', 'Dữ liệu hiện tại',
     'Nút “Thiết bị” mở cửa sổ tìm hàng hóa; thùng rác xóa dòng. Xóa hết dòng → “Bắt buộc phải nhập” ở đầu khối.'],
    ['Bảng Dịch vụ sửa chữa', 'Table', 'Enable', '–', 'Không', 'Dữ liệu hiện tại',
     'Nút “Chọn” thêm dịch vụ; mỗi dòng bắt buộc Giá vốn, Giá dịch vụ ≥ 0.'],
    ['Bảng Vật tư thay thế', 'Table', 'Enable', '–', 'Không', 'Dữ liệu hiện tại', 'Nút “Chọn” thêm vật tư; thùng rác xóa dòng.'],
    ['Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chân trang. Trang Sửa KHÔNG có nút Lưu và tiếp tục.'],
    ['Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách; đã sửa dở thì hỏi ' + _UNSAVED + '.'],
])
_f['ui_widths'] = _W_FORM
_f['events'] = [
    ['Bấm Sửa (cột Hành động / chân trang Chi tiết)', 'Click',
     'Before:\n– Không có quyền hoặc hạng mục đang Khóa thì nút không hiển thị.\nAfter:\n– Mở trang Sửa với dữ liệu hiện tại, nạp đủ ba bảng.'],
    ['Mở trang Sửa của hạng mục đang Khóa (liên kết đã lưu)', 'System',
     'After:\n– Báo “Bản ghi đang bị khoá, vui lòng mở khóa trước khi chỉnh sửa.” và chuyển về trang Chi tiết.'],
    ['Bấm Thiết bị / Chọn ở các bảng', 'Click',
     'After:\n– Mở cửa sổ tìm hàng hóa / dịch vụ, tích nhiều dòng rồi thêm vào bảng (“Đã thêm N hàng hoá” / “Đã thêm N dịch vụ”).\n'
     '– Chọn trùng dòng đã có → “Các hàng hoá đã có trong danh sách” / “Các dịch vụ đã có trong danh sách”.'],
    ['Bấm Lưu', 'Click',
     'During:\n– Kiểm tra như Thêm mới (mục 2.3), bỏ qua trùng tên với chính bản ghi.\n– Có lỗi → báo đỏ tại ô + “Vui lòng kiểm tra lại dữ liệu nhập”, không thực hiện After.\n'
     '– Hạng mục vừa bị người khác khóa → máy chủ từ chối “%s”, không ghi.\n'
     'After:\n– Ghi thay đổi (kể cả ba bảng), ghi lịch sử “Thay đổi thông tin” (đổi Trạng thái ghi mốc “Thay đổi trạng thái”).\n– Báo “Cập nhật thành công”, quay về danh sách.' % _MSG_423],
    ['Bấm Quay lại', 'Click',
     'Before:\n– Chưa sửa gì → về danh sách ngay.\nDuring:\n– Đã sửa → hỏi ' + _UNSAVED + '.\nAfter:\n– Chọn Thoát → về danh sách, không ghi; chọn Ở lại → giữ nguyên trang.'],
]

# ---- 2.5 Xóa
_f = _FR['Xóa công việc / lỗi thiết bị']
_f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Mô tả'],
            ['1', 'Nút Xóa', 'Icon Button / Button',
             'Biểu tượng thùng rác ở cột Hành động (hiện thẳng) và nút Xóa màu đỏ ở chân trang Chi tiết. Chỉ hiện khi có quyền, hạng mục đang Hoạt động VÀ chưa phát sinh chứng từ.'],
            ['2', 'Tiêu đề hộp xác nhận', 'Label', '“Xác nhận xóa”.'],
            ['3', 'Nội dung hộp xác nhận', 'Label', '“Bạn có chắc chắn muốn xóa "<tên hạng mục>"?” — nêu rõ tên để tránh xóa nhầm dòng.'],
            ['4', 'Nút Xóa', 'Button', 'Xác nhận xóa hẳn.'],
            ['5', 'Nút Hủy', 'Button', 'Đóng hộp, không thay đổi gì.']]
_f['ui_widths'] = _W4
_f['events'] = [
    ['Bấm Xóa (cột Hành động / chân trang Chi tiết)', 'Click',
     'Before:\n– Hạng mục đang Khóa hoặc đã phát sinh chứng từ thì nút không hiển thị.\nAfter:\n– Hiện hộp “Xác nhận xóa” kèm tên hạng mục.'],
    ['Bấm Xóa trong hộp xác nhận', 'Click',
     'During:\n– Máy chủ kiểm tra lại: hạng mục không còn Hoạt động hoặc đã phát sinh chứng từ → “Không được xóa!”, dừng.\n'
     'After:\n– Xóa hẳn hạng mục cùng các dòng thiết bị, vật tư, dịch vụ; ghi lịch sử Xóa.\n– Báo “Thao tác thành công”; ở danh sách thì nạp lại bảng, ở Chi tiết thì quay về danh sách.'],
    ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi gì.'],
]

# ---- 2.6 Khóa / Mở khóa
_f = _FR['Khóa / Mở khóa']
_f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Mô tả'],
            ['1', 'Nút ba chấm “Hành động khác”', 'Icon Button',
             'Chỉ có khi dòng có từ 4 thao tác trở lên: 2 thao tác đầu hiện thẳng, còn lại nằm trong nút này. Dòng ≤ 3 thao tác (vd hạng mục đã Khóa: Mở khóa, In, Lịch sử) thì mọi nút hiện thẳng.'],
            ['2', 'Nút Khóa', 'Icon Button / Button', 'Ở cột Hành động và chân trang Chi tiết (màu cam). Hiện khi có quyền VÀ hạng mục đang Hoạt động (kể cả đã phát sinh chứng từ).'],
            ['3', 'Nút Mở khóa', 'Icon Button / Button', 'Ở cột Hành động và chân trang Chi tiết (màu xanh lá). Hiện khi có quyền VÀ hạng mục đang Khóa.'],
            ['4', 'Tiêu đề hộp xác nhận', 'Label', '“Xác nhận khóa” / “Xác nhận mở khóa”.'],
            ['5', 'Nội dung hộp xác nhận', 'Label', '“Bạn có chắc chắn muốn khóa "<tên>"?” / “Bạn có chắc chắn muốn mở khóa "<tên>"?”.'],
            ['6', 'Nút Khóa / Mở khóa, Nút Hủy', 'Button', 'Xác nhận đổi trạng thái / đóng hộp không làm gì.'],
            ['7', 'Cột Trạng thái', 'Badge', 'Hoạt động (xanh) hoặc Khóa (đỏ), cập nhật ngay sau khi xác nhận.']]
_f['ui_widths'] = _W4
_f['events'] = [
    ['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên hạng mục.'],
    ['Xác nhận Khóa', 'Click',
     'During:\n– Hạng mục không còn Hoạt động (người khác vừa khóa) → “Chỉ có thể khóa lỗi thiết bị đang hoạt động”, dừng.\n'
     'After:\n– Trạng thái = Khóa, KHÔNG xóa dữ liệu, ghi lịch sử “Khóa” (nhóm Thay đổi trạng thái), báo “Thao tác thành công”.\n'
     '– Danh sách nạp lại, dòng chỉ còn Mở khóa, In, Lịch sử; ở Chi tiết thì ở lại trang, chân trang đổi sang Mở khóa.'],
    ['Xác nhận Mở khóa', 'Click',
     'After:\n– Trạng thái = Hoạt động, ghi lịch sử “Mở khóa”, báo “Thao tác thành công”; nút Sửa (và Xóa nếu chưa phát sinh chứng từ) hiện lại.'],
    ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, trạng thái không đổi.'],
]

# ---- 2.7 Lịch sử
_f = _FR['Xem lịch sử thay đổi']
_f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Giá trị ban đầu', 'Mô tả'],
            ['1', 'Mục Lịch sử', 'Button', 'Hiển thị',
             'Ở cột Hành động (trong nút ba chấm khi dòng có từ 4 thao tác). Luôn hiện, không cần quyền riêng.'],
            ['2', 'Tiêu đề cửa sổ', 'Label', 'Lịch sử thay đổi', 'Ghép tên hạng mục: “Lịch sử thay đổi: <tên hạng mục>”.'],
            ['3', 'Nút Bộ lọc', 'Button', 'Vùng lọc thu gọn', 'Mở / thu gọn vùng lọc; vùng lọc ghim ở đầu cửa sổ.'],
            ['4', 'Loại hành động / Người thực hiện', 'Dropdown', 'Trống',
             'Placeholder “Tất cả loại hành động” / “Tất cả người thực hiện”. Chọn là lọc ngay.'],
            ['5', 'Từ ngày / Đến ngày', 'Date', 'Trống', 'dd/mm/yyyy, lọc ngay khi chọn.'],
            ['6', 'Nút Làm mới (vùng lọc)', 'Button', 'Hiển thị', 'Xóa hết điều kiện lọc của cửa sổ.'],
            ['7', 'Danh sách thay đổi', 'Timeline', 'Theo dữ liệu',
             '- Thời điểm dd/mm/yyyy hh:mm, mới nhất ở trên cùng.\n- Loại: Tạo mới, Thay đổi thông tin, Khóa, Mở khóa.\n- “Người thực hiện: <tên>” kèm phòng ban.\n'
             '- Giá trị cũ → mới của: Tên công việc / lỗi thiết bị, Phân loại, Định mức công, Ghi chú, Giá bán, ĐM giảm giá (%), Hệ số lợi nhuận, % VAT, Trạng thái.'],
            ['8', 'Trạng thái rỗng', 'Label', 'Ẩn', '“Chưa có lịch sử thao tác nào.” / “Không có lịch sử phù hợp bộ lọc.”'],
            ['9', 'Nút Đóng / biểu tượng ×', 'Button', 'Hiển thị', 'Đóng cửa sổ.']]
_f['ui_widths'] = [0.6, 1.4, 1.0, 1.2, 2.8]
_f['events'] = [
    ['Chọn Lịch sử ở cột Hành động', 'Click', 'After:\n– Mở cửa sổ “Lịch sử thay đổi: <tên hạng mục>”, nạp các mốc, mới nhất trước.'],
    ['Bấm Xem lịch sử ở trang Chi tiết', 'Click', 'After:\n– Mở khối Lịch sử cuối trang, cùng nội dung và bộ lọc như cửa sổ.'],
    ['Chọn Loại hành động / Người thực hiện / Từ ngày / Đến ngày', 'Change', 'After:\n– Lọc ngay danh sách mốc theo mọi điều kiện đang chọn.'],
    ['Bấm Làm mới (vùng lọc)', 'Click', 'After:\n– Xóa hết điều kiện lọc, hiện lại đủ các mốc.'],
    ['Bấm Đóng / biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ; danh sách phía sau giữ nguyên bộ lọc và trang.'],
]

# ---- 2.8 Xuất Excel (ui đã có — bổ sung events)
_FR['Xuất danh sách ra Excel']['events'] = [
    ['Bấm Xuất Excel', 'Click',
     'Before:\n– Nút chỉ hiện với quyền Quản lý danh mục công việc - lỗi thiết bị.\nAfter:\n– Mở cửa sổ “Chọn trường xuất file”, tích sẵn các trường tương ứng cột đang hiển thị trên bảng.'],
    ['Tích / bỏ tích / kéo ☰ trường', 'Change / Drag',
     'During:\n– Ghi nhận thứ tự trường để quyết định thứ tự cột trong file.\n– Bỏ chọn hết → nút Xuất file mờ đi.'],
    ['Bấm Xuất file', 'Click',
     'During:\n– Sinh file theo ĐÚNG bộ lọc đang áp dụng, lấy toàn bộ kết quả (không theo trang).\n'
     'After:\n– Tải ' + FILE_XUAT + ': 3 dòng đầu là khối tiêu đề, bảng từ dòng 4, cột STT đứng đầu; báo “Xuất Excel thành công” (lỗi → “Lỗi khi xuất Excel”).'],
    ['Bấm Đóng / biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ, không xuất gì.'],
]

# ---- 2.9 In danh sách / In chi tiết
_f = _FR['In danh sách / In chi tiết']
_f['ui'] = _stt([
    ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
    ['Nút In danh sách', 'Button', 'Enable', 'Hiển thị', 'Thanh công cụ của bảng. Mở cửa sổ xem trước bản in danh sách.'],
    ['Mục In (cột Hành động)', 'Button', 'Enable', 'Hiển thị', 'Luôn hiện, kể cả hạng mục đã Khóa (nằm trong nút ba chấm khi dòng có từ 4 thao tác).'],
    ['Nút In (chân trang Chi tiết)', 'Button', 'Enable', 'Hiển thị', 'In chi tiết hạng mục đang xem.'],
    ['Tiêu đề cửa sổ xem trước', 'Label', 'Read-only', 'Theo thao tác', '“Xem trước danh sách lỗi thiết bị” (In danh sách) / “Xem trước lỗi thiết bị” (In chi tiết).'],
    ['Nút In (trong cửa sổ)', 'Button', 'Enable / Disable', 'Mờ khi đang tải', 'Mở hộp thoại in của trình duyệt.'],
    ['Tờ giấy xem trước — In danh sách', 'Khung A4 ngang', 'Read-only', 'Theo dữ liệu',
     'Mẫu in “Danh sách lỗi thiết bị”: tiêu đề đầu trang của công ty + bảng TOÀN BỘ hạng mục khớp bộ lọc (không theo trang). Chỉ in các cột đang hiển thị trên bảng trong số: STT, Tên công việc / Tình trạng lỗi, Áp dụng cho thiết bị, Định mức công, Công kỹ thuật, Đơn giá bán, Người sửa, Ngày sửa, Trạng thái.'],
    ['Tờ giấy xem trước — In chi tiết', 'Khung A4 dọc', 'Read-only', 'Theo dữ liệu',
     'Mẫu in “Chi tiết công việc / lỗi thiết bị”: Loại lỗi, Tình trạng lỗi, Định mức công, Hệ số giá bán dịch vụ, Hệ số giá bán dịch vụ thuê ngoài, Định mức giảm giá, Đơn giá công kỹ thuật, Công kỹ thuật, Đơn giá bán (dạng 1,234,567), Ghi chú và bảng thiết bị, vật tư, dịch vụ.'],
    ['Dòng thông báo', 'Label', 'Read-only', 'Ẩn', '“Đang tải dữ liệu in…”; lỗi: “Không có dữ liệu để in”, “Không tải được dữ liệu in” hoặc câu của máy chủ.'],
    ['Biểu tượng ×', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ xem trước.'],
])
_f['ui_widths'] = _W6
_f['events'] = [
    ['Bấm In danh sách', 'Click',
     'During:\n– Máy chủ lấy toàn bộ hạng mục khớp bộ lọc đang áp dụng và các cột đang hiển thị trên bảng.\n'
     'After:\n– Mở cửa sổ “Xem trước danh sách lỗi thiết bị” khổ ngang; không có dòng nào → “Không có dữ liệu để in”.'],
    ['Chọn In ở cột Hành động / bấm In ở chân trang Chi tiết', 'Click',
     'After:\n– Mở cửa sổ “Xem trước lỗi thiết bị” khổ dọc theo mẫu Chi tiết. Hạng mục đã Khóa vẫn in được.'],
    ['Bấm In trong cửa sổ', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt với đúng nội dung tờ giấy.'],
    ['Bấm biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ, danh sách / trang Chi tiết giữ nguyên.'],
]

# ---- 2.10 Xem chi tiết (TRANG RIÊNG)
_f = _FR['Xem chi tiết']
_f['ui'] = _stt([
    ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
    ['Tên công việc / Tình trạng lỗi (ô trên danh sách)', 'Link', 'Enable', 'Hiển thị',
     'Bấm vào tên để mở TRANG Chi tiết (mở được ở tab mới). Không có nút Xem riêng ở cột Hành động.'],
    ['Tiêu đề trang', 'Label', 'Read-only', '“Chi tiết công việc / lỗi thiết bị”', 'Không ghép mã vì danh mục không có mã.'],
    ['Khối Thông tin chung', 'Section', 'Read-only', 'Dữ liệu hiện tại',
     '12 ô mờ, không gõ được: Loại công việc / lỗi, Tên công việc / tình trạng lỗi, Định mức công, Hệ số giá bán dịch vụ, Định mức giảm giá (%), VAT (%), Công kỹ thuật, Đơn giá công kỹ thuật, Đơn giá bán, Hệ số công nghệ, Trạng thái, Ghi chú.'],
    ['Bảng Áp dụng cho thiết bị', 'Table', 'Read-only', 'Dữ liệu hiện tại',
     'STT, Tên thiết bị, Hãng sản xuất, Model, Mã, Code đặt hàng, Nhóm. Không có nút Thiết bị / xóa dòng.'],
    ['Bảng Dịch vụ sửa chữa', 'Table', 'Read-only', 'Dữ liệu hiện tại',
     'Tiêu đề kèm “(Hệ số giá bán dịch vụ thuê ngoài: x)”; cột STT, Tên dịch vụ, Giá vốn, Giá dịch vụ.'],
    ['Bảng Vật tư thay thế', 'Table', 'Read-only', 'Dữ liệu hiện tại', 'STT, Tên vật tư, Hãng sản xuất, Model, Mã, Code đặt hàng, Nhóm.'],
    ['Khối Lịch sử', 'Section', 'Enable', 'Thu gọn',
     'Tiêu đề “Lịch sử”. “Xem lịch sử” mở khối và nạp dữ liệu, “Thu gọn” đóng, “Làm mới” nạp lại. Nội dung, bộ lọc giống cửa sổ Lịch sử (mục 2.7).'],
    ['Nút Sửa', 'Button', 'Enable', 'Hiện khi có quyền và hạng mục đang Hoạt động', 'Mở trang Sửa (mục 2.4).'],
    ['Nút In', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ xem trước bản in chi tiết (mục 2.9).'],
    ['Nút Xóa (đỏ)', 'Button', 'Enable', 'Hiện khi có quyền, đang Hoạt động và chưa phát sinh chứng từ', 'Xóa hẳn hạng mục (mục 2.5).'],
    ['Nút Khóa (cam) / Mở khóa (xanh lá)', 'Button', 'Enable', 'Theo trạng thái, cần quyền', 'Đổi trạng thái (mục 2.6).'],
    ['Nút Quay lại', 'Button', 'Enable', 'Hiển thị', 'Về màn danh sách.'],
])
_f['ui_widths'] = _W6
_f['events'] = [
    ['Bấm tên hạng mục ở danh sách', 'Click',
     'During:\n– Nạp dữ liệu hạng mục; lỗi → báo câu của máy chủ hoặc “Lỗi khi tải dữ liệu” và quay lại.\n'
     'After:\n– Mở trang Chi tiết, mọi ô chỉ đọc; chân trang hiện đúng các nút như cột Hành động của dòng đó.'],
    ['Bấm Xem lịch sử / Thu gọn', 'Click', 'After:\n– Mở khối Lịch sử và nạp các mốc (mới nhất trên cùng) / thu gọn khối.'],
    ['Bấm Sửa / In / Xóa / Khóa / Mở khóa ở chân trang', 'Click',
     'After:\n– Xử lý như thao tác cùng tên ở cột Hành động (mục 2.4, 2.9, 2.5, 2.6).\n– Khóa / Mở khóa xong: ở lại trang, chân trang đổi nút theo trạng thái mới. Xóa xong: quay về danh sách.'],
    ['Bấm Quay lại', 'Click', 'After:\n– Về màn danh sách.'],
]

# ---- 2.11 Tùy chỉnh cột
_COT_ALL = ['STT', 'Tên công việc / Tình trạng lỗi', 'Loại công việc / lỗi thiết bị', 'Áp dụng cho thiết bị', 'Định mức công',
            'Công kỹ thuật', 'Đơn giá bán', 'Người cập nhật', 'Ngày cập nhật', 'Người tạo', 'Ngày tạo', 'Trạng thái', 'Hành động']
_f = _FR['Tùy chỉnh cột hiển thị']
_f['ui'] = [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
            ['1', 'Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', 'Hiển thị',
             'Nút cuối thanh công cụ; rê chuột hiện “Cấu hình cột hiển thị”. Mở cửa sổ “Tuỳ chỉnh cột”.'],
            ['2', 'Danh sách cột', 'Checkbox chọn nhiều', 'Enable', 'Theo cấu hình đã lưu của người dùng',
             'Liệt kê đủ %d cột: %s. Tích = hiện, bỏ tích = ẩn. Lần đầu hiện: STT, Tên công việc / Tình trạng lỗi, Người tạo, Ngày tạo, Trạng thái, Hành động.' % (len(_COT_ALL), ', '.join(_COT_ALL))],
            ['3', 'Cột bắt buộc', 'Checkbox', 'Disable', 'Luôn tích',
             'STT, Tên công việc / Tình trạng lỗi, Hành động: chữ xám, có biểu tượng ổ khóa (“Cột bắt buộc — không thể ẩn hoặc đổi vị trí”), không bỏ tích và không kéo được.'],
            ['4', 'Biểu tượng ☰', 'Drag handle', 'Enable', 'Hiển thị', 'Kéo thả để đổi thứ tự các cột không bắt buộc.'],
            ['5', 'Nút Lưu', 'Button', 'Enable', 'Hiển thị',
             'Áp dụng ngay lên bảng, lưu theo TÀI KHOẢN người dùng. Bộ cột này cũng quyết định cột của bản In danh sách và các trường tích sẵn khi Xuất Excel.'],
            ['6', 'Nút Đóng / biểu tượng ×', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ, bỏ các thay đổi chưa Lưu.']]
_f['ui_widths'] = _W6
_f['events'] = [
    ['Bấm biểu tượng Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ “Tuỳ chỉnh cột” với cấu hình đang áp dụng.'],
    ['Tích / bỏ tích, kéo thả cột', 'Change / Drag', 'During:\n– Cột bắt buộc không bỏ tích, không kéo được.\n– Chưa áp dụng lên bảng cho tới khi bấm Lưu.'],
    ['Bấm Lưu', 'Click', 'After:\n– Bảng hiện / ẩn và sắp cột theo lựa chọn ngay; lưu riêng cho tài khoản, báo “Cập nhật thành công” (lỗi → “Thao tác thất bại”).'],
    ['Bấm Đóng / biểu tượng ×', 'Click', 'After:\n– Đóng cửa sổ, danh sách cột trở về cấu hình đang áp dụng.'],
]

# HDSD mục Lịch sử: tiêu đề cửa sổ nay ghép tên bản ghi (CatalogHistoryModal bỏ dòng phụ từ 19/09/2026).
CFG['lich_su']['buoc'][0] = ('Xem từ màn danh sách: ở cột Hành động (trong nút ba chấm nếu dòng có từ 4 thao tác), Người dùng chọn Lịch sử. '
                             'Hệ thống mở cửa sổ “Lịch sử thay đổi: <tên hạng mục>”.')

CFG['loi_code'] += [
    'Sửa hạng mục đang Khóa: chốt 423 nằm TRONG DeviceErrorController::update() (không phải middleware route) mà controller nhận DeviceErrorRequest → Laravel validate trước, payload thiếu trường nhận 422 chứ không tới 423. Câu 423 lại ghi “vui lòng khôi phục trước khi cập nhật” trong khi FE (trang Sửa) báo “vui lòng mở khóa trước khi chỉnh sửa” — hai câu cho cùng một tình huống.',
    'Mở khóa không kiểm tra trạng thái hiện tại: DeviceErrorService::restore() luôn đặt Hoạt động và ghi mốc lịch sử “Mở khóa” — hai người cùng Mở khóa một hạng mục thì người sau vẫn “Thao tác thành công” và lịch sử có 2 mốc Mở khóa trùng (Khóa thì có chặn “Chỉ có thể khóa lỗi thiết bị đang hoạt động”).',
    'In danh sách không in được cột Loại công việc / lỗi thiết bị, Người tạo, Ngày tạo dù đang hiện trên bảng: printListColumnDefinitions() chỉ khai STT, Tên, Áp dụng cho thiết bị, Định mức công, Công kỹ thuật, Đơn giá bán, Người sửa, Ngày sửa, Trạng thái → với bộ cột mặc định bản in chỉ còn STT, Tên, Trạng thái. Nhãn cột in “Người sửa / Ngày sửa” cũng lệch bảng (“Người cập nhật / Ngày cập nhật”).',
    'Tiêu đề cửa sổ In chi tiết: FE ghép `Xem trước lỗi thiết bị ${item.code}` nhưng danh mục không có mã → luôn ra “Xem trước lỗi thiết bị”, không nêu hạng mục nào đang in.',
]


# Đồng bộ chỗ tester sửa tay trên Drive (so bản Drive 28/09/2026) — build_srs áp qua apply_tester_edits
CFG['srs_tester'] = {
 "del": [
  "1. Người dùng vào menu CSKH sau bán → Danh mục → Công việc, lỗi thiết bị.",
  "Không có bản ghi khớp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”",
  "Bấm biểu tượng ⓘ cạnh tên → cửa sổ “Hàng hóa áp dụng”.",
  "Bấm Làm mới → xóa hết tiêu chí và nạp lại ngay.",
  "Thiếu trường bắt buộc / chưa có thiết bị → “Bắt buộc phải nhập” tại ô, toast “Vui lòng kiểm tra lại dữ liệu nhập”.",
  "Bấm “Lưu và tiếp tục” → ghi rồi mở lại trang trống.",
  "Xóa hết thiết bị → “Bắt buộc phải nhập”.",
  "Chưa có mốc nào → “Chưa có lịch sử thao tác nào.”",
  "Lỗi máy chủ → “Lỗi khi xuất Excel”."
 ],
 "br": {
  "BR-01": [
   "BR-01",
   "Ràng buộc trùng tên trong cùng Loại",
   [
    "Tên hạng mục không được trùng trong cùng một Loại; khác Loại thì được trùng tên.",
    "Khi sửa, bản ghi đang sửa được loại khỏi phép so trùng; đổi sang Loại khác cũng bị kiểm tra trùng trong Loại mới.",
    "Thông báo khi trùng: “Đã tồn tại trên hệ thống”."
   ],
   [
    "Thêm mới ",
    "Chỉnh sửa "
   ]
  ],
  "BR-02": [
   "BR-02",
   "Thiết bị và dịch vụ sửa chữa",
   [
    "Bắt buộc có ít nhất một thiết bị áp dụng.",
    "Bảng Dịch vụ sửa chữa không bắt buộc, nhưng mỗi dòng đã thêm phải có Giá vốn và Giá dịch vụ ≥ 0.",
    "Hệ số công nghệ phải lớn hơn 0 (“Nhập hệ số lớn hơn 0”); VAT (%) tối đa 100."
   ],
   [
    "Thêm mới ",
    "Chỉnh sửa "
   ]
  ],
  "BR-03": [
   "BR-03",
   "Quy đổi Đơn giá bán",
   [
    "Đơn giá bán có nhập (> 0) thì dùng đúng giá đã nhập.",
    "Đơn giá bán để trống thì quy đổi = Định mức công × Đơn giá công kỹ thuật × Hệ số giá bán dịch vụ của công ty người đang đăng nhập — hai người ở hai công ty có thể thấy giá khác nhau.",
    "Bộ lọc Đơn giá bán từ / đến so theo đúng giá đang hiển thị ở cột Đơn giá bán."
   ],
   [
    "Xem danh sách ",
    "Tìm kiếm và lọc",
    "Xuất danh sách ra Excel",
    "In danh sách / In chi tiết"
   ]
  ],
  "BR-04": [
   "BR-04",
   "Điều kiện xóa",
   [
    "Chỉ xóa được hạng mục đang Hoạt động và chưa phát sinh ở báo giá / hợp đồng dịch vụ, phân công, kết quả nhập, biên bản bảo hành, phiếu xử lý yêu cầu bảo hành sửa chữa, tiến độ công việc.",
    "Xóa hạng mục xóa luôn danh sách thiết bị áp dụng và dịch vụ sửa chữa kèm theo."
   ],
   [
    "Xóa công việc / lỗi thiết bị"
   ]
  ],
  "BR-05": [
   "BR-05",
   "Bản ghi đang Khóa",
   [
    "Chỉ khóa được hạng mục đang Hoạt động (“Chỉ có thể khóa lỗi thiết bị đang hoạt động”); có thể khóa ngay trong form Sửa.",
    "Hạng mục đang Khóa không sửa, không xóa được (máy chủ chặn), báo “Bản ghi đang bị khoá, vui lòng khôi phục trước khi cập nhật.”; chỉ còn Mở khóa, In, Lịch sử.",
    "Hạng mục đang Khóa không còn chọn được ở nghiệp vụ mới; chứng từ cũ vẫn giữ nguyên."
   ],
   [
    "Chỉnh sửa ",
    "Xóa ",
    "Khóa / Mở khóa",
    "Phiếu xử lý yêu cầu bảo hành sửa chữa",
    "Báo giá dịch vụ"
   ]
  ],
  "BR-06": [
   "BR-06",
   "Ghi lịch sử thay đổi",
   [
    "Mọi thao tác Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa đều ghi lịch sử kèm người thực hiện.",
    "Khóa ngay trong form Sửa được ghi thành dòng Thay đổi trạng thái riêng."
   ],
   [
    "Thêm mới ",
    "Chỉnh sửa ",
    "Khóa / Mở khóa",
    "Xem lịch sử thay đổi"
   ]
  ]
 }
}

# Tester xoá trắng ô Phạm vi / Mô tả ở bảng giao diện (bản Drive 28/09/2026) — giữ theo tester
for _fr in CFG['srs']['fr']:
    for _r in (_fr.get('ui') or [])[1:]:
        if len(_r) >= 7 and _r[1] in ('Đơn giá bán', 'VAT (%)', 'Bảng Áp dụng cho thiết bị') and _r[4] in ('≥ 0', '≤ 100', '≥ 1 dòng'):
            _r[4] = ''
        if len(_r) >= 7 and _r[1] == 'Bảng Dịch vụ sửa chữa' and _r[-1] == 'Mỗi dòng bắt buộc Giá vốn, Giá dịch vụ ≥ 0.':
            _r[-1] = ''
        if len(_r) == 6 and _r[1] == 'Đơn giá bán' and _r[4] == '≥ 0':
            _r[4] = ''
