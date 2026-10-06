# -*- coding: utf-8 -*-
# Cấu hình tài liệu màn Danh mục ghi chú kiểm tra bảo dưỡng (phân hệ CSKH sau bán).
# Nguồn: code gop_db 25/09/2026 — FE pages/customer-care/note-maintenances/index.vue,
# components/modal/customer-care/note-maintenance-modal.vue, utils/mixins/CatalogImportMixin.js;
# BE Modules/CustomerCare (NoteMaintenanceController, NoteMaintenanceService, NoteMaintenanceRequest, NoteMaintenance::USAGE_REFERENCES),
# App\ExcelExport\ExportColumnRegistry['note_maintenances']. Cột DB note_maintenances.description = varchar(255).
# Cập nhật 28/09/2026: cột status (Hoạt động / Khóa), Khóa / Mở khóa ở cột Hành động, bộ lọc Trạng thái, xóa hẳn khi
#   đang Hoạt động + chưa dùng (bỏ API hỏi "usage" trước khi xóa), middleware recordNotLocked chặn sửa/xóa (423);
#   ServiceImportService / ServiceService::optionsData chỉ lấy ghi chú đang Hoạt động.
# Không ghi URL. Chữ UI / message lấy nguyên văn code.

DT = 'ghi chú kiểm tra'
Q_XEM = 'Xem ghi chú kiểm tra bảo dưỡng'
Q_QL = 'Quản lý ghi chú kiểm tra bảo dưỡng'
MSG_USED = 'Ghi chú kiểm tra bảo dưỡng đang được sử dụng, không thể xóa.'
MSG_LOCKED = 'Bản ghi đang bị khoá, vui lòng mở khoá trước khi cập nhật.'
MSG_CONFLICT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'
# Nơi được coi là "đã sử dụng" (NoteMaintenance::USAGE_REFERENCES, ghi bằng tên nghiệp vụ)
USED_N = 'nội dung kiểm tra trong cấp bảo dưỡng của gói bảo dưỡng (bảng cấp bảo dưỡng của gói dịch vụ)'

CFG = {
    'slug': 'note-maintenances',
    'ten': 'Danh mục ghi chú kiểm tra bảo dưỡng',
    'doi_tuong': DT,
    'file_hdsd': 'HDSD_Danh muc ghi chu kiem tra bao duong.docx',
    'file_srs': 'SRS - Danh mục ghi chú kiểm tra bảo dưỡng.docx',
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Ghi chú kiểm tra bảo dưỡng', 'menu_muc')],

    'thuat_ngu': [
        ['Ghi chú kiểm tra bảo dưỡng', 'Một hạng mục công việc kiểm tra được thực hiện trong quá trình bảo dưỡng thiết bị, ví dụ “Kiểm tra ngoại quan không tháo lắp”, “Đo kiểm, kiểm tra bằng dụng cụ chuyên dùng.”.'],
        ['Hạng mục', 'Tên đầy đủ của công việc kiểm tra, là trường chính của danh mục, không được trùng.'],
        ['Ký hiệu', 'Mã viết tắt của hạng mục (ví dụ KTBM, DK, CC) để nhân viên kỹ thuật ghi nhanh trên phiếu và mẫu in. Không được trùng. Hệ thống tự chuyển thành chữ IN HOA khi lưu.'],
        ['Mô tả', 'Diễn giải chi tiết hạng mục kiểm tra, không bắt buộc.'],
        ['Trạng thái Hoạt động', 'Ghi chú còn chọn được khi khai báo nội dung kiểm tra cho cấp bảo dưỡng của gói bảo dưỡng.'],
        ['Trạng thái Khóa', 'Ghi chú ngừng dùng: không còn chọn được ở gói bảo dưỡng mới / Import gói bảo dưỡng, không sửa và không xóa được cho tới khi Mở khóa; vẫn nằm trong danh mục, vẫn xem được chi tiết và lịch sử; gói cũ đang dùng vẫn hiển thị đúng ký hiệu kèm biểu tượng 🔒.'],
        ['Đang được sử dụng', 'Ghi chú đã được chọn ở ít nhất một ' + USED_N + '; khi đó không xóa được (vẫn Khóa được).'],
    ],
    'phien_ban': [
        ['1.0', '13/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục ghi chú kiểm tra bảo dưỡng.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: bấm Hạng mục để Xem chi tiết (bỏ nút Xem), bổ sung cột Người tạo/Ngày tạo/Người cập nhật, Lịch sử thay đổi, cửa sổ Chọn trường xuất file, Import Excel, Tùy chỉnh cột; trình bày theo mẫu tài liệu danh mục chung.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bổ sung trạng thái Hoạt động / Khóa: ô Trạng thái trong cửa sổ Tạo/Sửa (mặc định Hoạt động), cột Trạng thái và bộ lọc Trạng thái ở danh sách, cột Trạng thái trong file Xuất Excel, chức năng Khóa / Mở khóa ở cột Hành động (khóa được cả ghi chú đang được sử dụng). Ghi chú đang Khóa ẩn nút Sửa, Xóa và bị máy chủ chặn cập nhật; ghi chú đã khóa không còn chọn được ở gói bảo dưỡng mới và Import gói bảo dưỡng. Xóa là xóa hẳn, chỉ khi ghi chú đang Hoạt động và chưa được sử dụng; bỏ bước hỏi máy chủ trước khi mở hộp xác nhận xóa và đổi câu thông báo chặn xóa.'],
    ],
    'muc_dich': [
        'Màn hình Danh mục ghi chú kiểm tra bảo dưỡng dùng để khai báo các hạng mục cần ghi chú khi kiểm tra bảo dưỡng thiết bị, ví dụ “Kiểm tra ngoại quan không tháo lắp”, “Đo kiểm, kiểm tra bằng dụng cụ chuyên dùng.”, “Bôi trơn bạc đạn, cốt, trục xoay (có núm bơm mỡ).”.',
        'Mỗi hạng mục có một Ký hiệu viết tắt (ví dụ KTBM, DK, CC) để nhân viên kỹ thuật ghi nhanh trên phiếu hiện trường. Danh mục này được gắn vào cấp bảo dưỡng của từng gói dịch vụ; ghi chú đã gắn vào gói thì không xóa được, muốn ngừng dùng thì Khóa.',
        'Mỗi ghi chú có trạng thái Hoạt động hoặc Khóa. Ghi chú đã khóa không còn chọn được ở gói bảo dưỡng mới nhưng các gói cũ vẫn giữ nguyên. Danh mục dùng chung cho toàn hệ thống, không phân theo công ty / phòng ban.',
    ],
    'quyen': {
        'truoc': ['Màn hình dùng 2 quyền riêng. Mục menu chỉ hiện khi tài khoản có ít nhất một trong hai quyền; không có quyền nào thì không vào được màn hình.'],
        'rows': [
            [Q_XEM, 'Vào màn hình, xem danh sách, tìm kiếm, lọc, xem chi tiết (bấm vào Hạng mục), xem lịch sử, xuất Excel.'],
            [Q_QL, 'Toàn bộ quyền Xem, cộng thêm: Tạo mới, Sửa, Xóa, Khóa, Mở khóa, Import Excel.'],
        ],
        'sau': ['Nút nào Người dùng không có quyền dùng thì hệ thống ẩn hẳn, không hiện nút mờ. Máy chủ cũng kiểm tra quyền, nên gọi thẳng chức năng mà bỏ qua giao diện vẫn bị từ chối.'],
    },

    'danh_sach': {
        'mo_ta_vao': 'Hệ thống hiển thị danh sách ghi chú kiểm tra hiện có, mặc định 10 dòng mỗi trang, xếp theo thứ tự tạo.',
        'bo_cuc': [
            'Khu vực tìm kiếm và lọc — ô tìm kiếm nhanh, ô Trạng thái, nút Tìm kiếm và Làm mới. Ô tìm nhanh đã quét cả Hạng mục lẫn Ký hiệu nên màn hình không có Tìm kiếm nâng cao.',
            'Thanh công cụ — nút Tạo mới, nút Xuất Excel, nút Import Excel và biểu tượng Cấu hình cột hiển thị.',
            'Bảng danh sách — các cột thông tin, cột Hành động ở cuối, và phân trang bên dưới.',
        ],
        'cot': [
            ['STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'],
            ['Hạng mục', 'Nội dung hạng mục kiểm tra. Luôn hiển thị, sắp xếp được. Bấm vào để mở cửa sổ Xem ghi chú kiểm tra.'],
            ['Ký hiệu', 'Mã viết tắt của hạng mục (chữ in hoa). Mặc định ẩn.'],
            ['Mô tả', 'Diễn giải chi tiết; nội dung dài được xuống dòng trong ô. Mặc định ẩn.'],
            ['Người tạo', 'Người đã thêm bản ghi.'],
            ['Ngày tạo', 'Thời điểm thêm, dạng dd/mm/yyyy hh:mm, sắp xếp được.'],
            ['Người cập nhật', 'Người sửa bản ghi gần nhất. Mặc định ẩn.'],
            ['Ngày cập nhật', 'Thời điểm sửa gần nhất, dạng dd/mm/yyyy hh:mm. Mặc định ẩn, sắp xếp được.'],
            ['Trạng thái', 'Nhãn Hoạt động hoặc Khóa. Danh sách hiện cả ghi chú đang Hoạt động lẫn đang Khóa.'],
            ['Hành động', 'Các nút thao tác của dòng (xem mục 4).'],
        ],
        'hanh_dong': {
            'intro': 'Trên mỗi dòng, cột Hành động có các nút:',
            'bullets': [
                'Biểu tượng bút chì {icon:btn_sua} — mở cửa sổ Sửa ghi chú kiểm tra. Chỉ hiện khi Người dùng có quyền Quản lý VÀ ghi chú đang Hoạt động.',
                'Biểu tượng thùng rác {icon:btn_xoa} — xóa hẳn ghi chú. Chỉ hiện khi Người dùng có quyền Quản lý, ghi chú đang Hoạt động VÀ CHƯA được gắn vào cấp bảo dưỡng của gói dịch vụ nào.',
                'Khóa / Mở khóa — đổi trạng thái ghi chú. Chỉ hiện khi Người dùng có quyền Quản lý; ghi chú đang Hoạt động hiện Khóa, ghi chú đang Khóa hiện Mở khóa.',
                'Lịch sử — mở cửa sổ Lịch sử thay đổi. Luôn hiện, không cần quyền riêng.',
                'Dòng có từ 4 nút trở lên thì 2 nút đầu (Sửa, Xóa) hiện thẳng, các nút còn lại (Khóa, Lịch sử) nằm trong nút ba chấm {icon:btn_bacham} “Hành động khác”.',
            ],
            'anh': 'Các nút ở cột Hành động của một ghi chú kiểm tra',
            'luu_y': ['Lưu ý: màn hình KHÔNG có nút Xem — muốn xem chi tiết thì bấm thẳng vào Hạng mục. Trong thực tế phần lớn ghi chú đang được gắn vào gói dịch vụ nên thường không thấy nút thùng rác; đây là hành vi đúng, không phải lỗi. Với ghi chú ĐÃ KHÓA, nút Sửa và Xóa sẽ BIẾN MẤT, chỉ còn Mở khóa và Lịch sử; muốn sửa lại phải Mở khóa trước.'],
        },
        'phan_trang': [
            'Cuối bảng có dòng “Hiển thị a–b / N”: N là tổng số ghi chú khớp điều kiện tìm kiếm đang áp dụng, không phải tổng toàn danh mục.',
            'Ô Số dòng/trang có các mức 5, 10, 20, 50, 100 (mặc định 10). Đổi số dòng thì hệ thống tự quay về trang 1.',
            'Các cột sắp xếp được: Hạng mục, Ngày tạo, Ngày cập nhật. Bấm tiêu đề cột để sắp xếp, bấm lần hai để đảo chiều. Thứ tự sắp xếp được giữ nguyên khi chuyển trang.',
        ],
    },

    'loc': {
        'buoc2': 'Bước 2: Nhập một phần Hạng mục hoặc Ký hiệu vào ô tìm kiếm nhanh rồi nhấn Enter hoặc bấm {icon:btn_timkiem}, và/hoặc chọn giá trị ở ô Trạng thái.',
        'rows': [
            ['Ô tìm kiếm nhanh', 'Placeholder “Tìm theo hạng mục hoặc ký hiệu...”. Quét hai trường Hạng mục và Ký hiệu — KHÔNG quét Mô tả. Gõ một phần chuỗi là đủ, không phân biệt chữ hoa chữ thường. Phải nhấn Enter hoặc bấm Tìm kiếm thì danh sách mới lọc.'],
            ['Trạng thái', 'Hoạt động hoặc Khóa. Bỏ trống thì hiện cả hai trạng thái (xóa lựa chọn bằng dấu x trong ô). Lọc ngay khi chọn, không cần bấm Tìm kiếm.'],
        ],
        'ap_dung': [
            'Các tiêu chí kết hợp với nhau theo kiểu VÀ — chỉ ghi chú thỏa đồng thời từ khóa và Trạng thái mới hiện ra. Mỗi lần đổi tiêu chí, danh sách quay về trang 1. Điều kiện tìm kiếm được ghi nhớ trong 10 phút khi quay lại màn hình.',
            'Bấm {icon:btn_lammoi} để xóa toàn bộ tiêu chí (từ khóa và Trạng thái); danh sách nạp lại đầy đủ ngay lập tức.',
        ],
        'anh_ket_qua': 'Kết quả tìm nhanh (gõ “Kiểm tra”)',
    },

    'form': {
        'kieu': 'popup',
        'buoc_tao': [
            'Bước 1: Truy cập vào màn hình Danh mục ghi chú kiểm tra bảo dưỡng (cần quyền Quản lý).',
            'Bước 2: Bấm {icon:btn_taomoi}. Hệ thống mở cửa sổ “Tạo ghi chú kiểm tra”.',
            'Bước 3: Nhập Hạng mục, Ký hiệu, (nếu cần) Mô tả; giữ Trạng thái là Hoạt động (hoặc chọn Khóa nếu muốn tạo sẵn ở trạng thái ngừng dùng).',
            'Bước 4: Bấm {icon:btn_luu} để lưu và đóng cửa sổ, hoặc {icon:btn_luutieptuc} để lưu rồi nhập tiếp hạng mục khác.',
        ],
        'anh_tao': 'Cửa sổ Tạo ghi chú kiểm tra',
        'truong': [
            ['Hạng mục', 'Ô nhập giá trị', 'Có', 'Trống', 'Gợi ý “VD: Kiểm tra ngoại quan không tháo lắp.”. Tối đa 255 ký tự, duy nhất trong danh mục. Bỏ trống báo “Bắt buộc phải nhập”; trùng báo “Hạng mục đã tồn tại”.'],
            ['Ký hiệu', 'Ô nhập giá trị', 'Có', 'Trống', 'Gợi ý “VD: KTBM”. Tối đa 255 ký tự, duy nhất trong danh mục. Hệ thống tự cắt khoảng trắng đầu cuối và chuyển thành chữ IN HOA khi lưu (gõ “ktbm” sẽ lưu “KTBM”), nên “ktbm” và “KTBM” bị coi là trùng. Bỏ trống báo “Bắt buộc phải nhập” sau khi bấm Lưu; trùng báo “Ký hiệu đã tồn tại”.'],
            ['Mô tả', 'Ô nhập giá trị', 'Không', 'Trống', 'Gợi ý “Mô tả chi tiết hạng mục kiểm tra (nếu có)”. Tối đa 255 ký tự.'],
            ['Trạng thái', 'Ô chọn giá trị', 'Không (luôn có giá trị)', 'Hoạt động', 'Chỉ chọn 1 trong 2 giá trị: Hoạt động / Khóa; không xóa trống được. Chọn Khóa thì ghi chú không còn chọn được ở gói bảo dưỡng mới.'],
        ],
        'nut': [
            ['Lưu', 'Ghi bản ghi rồi đóng cửa sổ, báo “Thêm mới thành công” (hoặc “Cập nhật thành công” khi sửa) và nạp lại danh sách.'],
            ['Lưu và tiếp tục', 'Ghi bản ghi nhưng GIỮ cửa sổ mở và xóa trắng các ô để nhập tiếp. Chỉ có khi Tạo mới.'],
            ['Đóng', 'Đóng cửa sổ, không ghi gì. Nếu đã nhập dở, hệ thống hỏi “Thông tin chưa lưu” — “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại).'],
        ],
        'loi': [
            ['Bắt buộc phải nhập', 'Chưa nhập Hạng mục hoặc Ký hiệu (hoặc chỉ nhập toàn khoảng trắng).'],
            ['Hạng mục đã tồn tại', 'Đã có ghi chú khác cùng Hạng mục.'],
            ['Ký hiệu đã tồn tại', 'Đã có ghi chú khác cùng Ký hiệu (so sau khi đã chuyển chữ in hoa).'],
            ['Vui lòng nhập tối đa 255 ký tự.', 'Hạng mục, Ký hiệu hoặc Mô tả quá dài.'],
            ['Bạn chưa nhập đầy đủ thông tin', 'Thông báo chung khi còn ô bị lỗi; xem các ô báo đỏ trong cửa sổ.'],
        ],
    },

    'sua': {
        'buoc': [
            'Bước 1: Truy cập vào màn hình Danh mục ghi chú kiểm tra bảo dưỡng (cần quyền Quản lý).',
            'Bước 2: Bấm nút {icon:btn_sua} ở cột Hành động của ghi chú cần sửa (chỉ có ở ghi chú đang Hoạt động).',
            'Bước 3: Hệ thống hiển thị cửa sổ “Sửa ghi chú kiểm tra” với cả bốn ô đã điền sẵn (Hạng mục, Ký hiệu, Mô tả, Trạng thái).',
            'Bước 4: Cập nhật các thông tin cần sửa (quy tắc nhập như Thêm mới).',
            'Bước 5: Bấm {icon:btn_luu} để xác nhận thay đổi hoặc Đóng nếu muốn hủy. Cửa sổ Sửa không có nút Lưu và tiếp tục.',
        ],
        'anh': 'Cửa sổ Sửa ghi chú kiểm tra',
        'ghi_chu': [
            'Giữ nguyên Hạng mục và Ký hiệu của chính ghi chú đang sửa thì không bị báo trùng.',
            'Ghi chú đang được gắn vào gói dịch vụ VẪN sửa được; các gói đang dùng sẽ hiển thị nội dung mới. Việc đang được sử dụng chỉ chặn thao tác Xóa.',
            'Ghi chú đang Khóa không có nút Sửa. Nếu ghi chú vừa bị người khác khóa trong lúc Người dùng đang mở cửa sổ Sửa, bấm Lưu sẽ nhận thông báo “%s”, thay đổi không được ghi.' % MSG_LOCKED,
            'Chọn Trạng thái = Khóa rồi Lưu là cách khóa ngay trong cửa sổ Sửa; lịch sử ghi thành một mốc Thay đổi trạng thái riêng.',
        ],
    },
    'xoa': {
        'buoc': [
            'Bước 1: Ở cột Hành động, Người dùng bấm {icon:btn_xoa}.',
            'Bước 2: Hệ thống hiện hộp “Xác nhận xóa” — “Bạn có chắc muốn xóa ghi chú "…"?”. Bấm {icon:btn_confirm_xoa} để xác nhận: hệ thống báo “Xóa thành công”, bản ghi biến mất khỏi danh sách.',
            'Bấm {icon:btn_huy} nếu bấm nhầm. Không có gì thay đổi.',
        ],
        'anh': 'Hộp xác nhận xóa ghi chú kiểm tra',
        'ghi_chu': [
            'Xóa là xóa HẲN ghi chú khỏi danh mục (không phải chuyển sang Khóa). Nút Xóa chỉ hiện khi ghi chú đang Hoạt động VÀ CHƯA được sử dụng.',
            'Ghi chú được coi là “đã sử dụng” khi đã được chọn ở ít nhất một ' + USED_N + '. Ghi chú đã được sử dụng thì dùng Khóa thay cho Xóa.',
            'Nếu ghi chú vừa được gắn vào gói trong lúc Người dùng đang mở danh sách, bấm Xóa trong hộp xác nhận sẽ nhận thông báo “%s”; vừa bị người khác khóa thì nhận “%s”. Bản ghi không bị xóa.' % (MSG_USED, MSG_LOCKED),
        ],
    },
    'khoa': {
        'y_nghia': [
            'Ghi chú VẪN nằm trong danh sách, cột Trạng thái hiện chữ Khóa; vẫn xem chi tiết và xem lịch sử thay đổi được.',
            'Ghi chú đã khóa không còn chọn được khi khai báo nội dung kiểm tra theo cấp ở gói bảo dưỡng mới, và file Import gói bảo dưỡng dùng ghi chú đó bị báo “Ghi chú kiểm tra "…" không có trong danh mục hoặc đã bị khóa”.',
            'Gói bảo dưỡng cũ đang dùng ghi chú đó giữ nguyên; mở Sửa gói cũ vẫn thấy đúng ký hiệu kèm biểu tượng 🔒.',
            'Nút Sửa và Xóa của dòng đó biến mất. Muốn sửa hoặc xóa, Người dùng phải Mở khóa trước.',
            'Khóa được cả ghi chú đang được sử dụng — đây là cách ngừng dùng một ghi chú không xóa được.',
        ],
        'buoc_khoa': [
            'Bước 1: Ở cột Hành động của ghi chú đang Hoạt động, Người dùng chọn Khóa (trong nút ba chấm {icon:btn_bacham} “Hành động khác” nếu dòng có đủ 4 nút).',
            'Bước 2: Hệ thống hiện hộp xác nhận “Khóa ghi chú kiểm tra” — “Bạn có chắc muốn khóa ghi chú "…"?”. Bấm Khóa để xác nhận; hệ thống báo “Khóa thành công”, cột Trạng thái đổi thành Khóa. Bấm Hủy nếu bấm nhầm.',
        ],
        'buoc_mo': [
            'Bước 1: Ở cột Hành động của ghi chú đang Khóa, Người dùng chọn Mở khóa.',
            'Bước 2: Bấm Mở khóa trong hộp xác nhận “Mở khóa ghi chú kiểm tra” — “Bạn có chắc muốn mở khóa ghi chú "…"?”. Hệ thống báo “Mở khóa thành công”, cột Trạng thái đổi thành Hoạt động, nút Sửa (và Xóa nếu ghi chú chưa được sử dụng) hiện lại. Bấm Hủy nếu bấm nhầm.',
        ],
        'ghi_chu': [
            'Chỉ người có quyền Quản lý mới thấy Khóa / Mở khóa.',
            'Có thể khóa ngay trong cửa sổ Sửa bằng cách chọn Trạng thái = Khóa rồi Lưu.',
            'Nếu ghi chú vừa bị người khác đổi trạng thái, hệ thống báo “%s” và không ghi thêm mốc lịch sử trùng.' % MSG_CONFLICT,
        ],
    },
    'lich_su': {
        'buoc': [
            'Xem từ màn danh sách: ở cột Hành động, Người dùng chọn Lịch sử. Hệ thống mở cửa sổ “Lịch sử thay đổi: <hạng mục>”.',
            'Xem từ màn chi tiết: bấm vào Hạng mục để mở cửa sổ Xem ghi chú kiểm tra, khối Lịch sử nằm ở cuối cửa sổ.',
        ],
        'ghi_chu': [
            'Bốn trường Hạng mục, Ký hiệu, Mô tả, Trạng thái đều được theo dõi thay đổi. Khóa / Mở khóa (từ cột Hành động hoặc đổi Trạng thái trong cửa sổ Sửa) được ghi thành mốc riêng loại Thay đổi trạng thái.',
            'Cửa sổ có bộ lọc riêng (loại hành động, người thực hiện, khoảng thời gian). Bản ghi chưa có mốc nào hiện “Chưa có lịch sử thao tác nào.”',
        ],
    },
    'chi_tiet': {
        'buoc': ['Bước 1: Truy cập vào màn hình Danh mục ghi chú kiểm tra bảo dưỡng.',
                 'Bước 2: Bấm vào Hạng mục ở cột Hạng mục. Hệ thống mở cửa sổ “Xem ghi chú kiểm tra”.'],
        'ghi_chu': ['Cửa sổ hiển thị Hạng mục, Ký hiệu, Mô tả và Trạng thái ở chế độ chỉ đọc (không gõ được, không có nút Lưu, chỉ có nút Đóng), kèm khối Lịch sử ở cuối. Người chỉ có quyền Xem cũng mở được; ghi chú đang Khóa vẫn xem được bình thường.'],
    },
    'xuat': {
        'buoc': [
            'Bước 1: Tìm kiếm, lọc đúng dữ liệu cần lấy (xem PHẦN 2). File xuất ra chạy theo đúng từ khóa, Trạng thái và thứ tự sắp xếp đang áp dụng.',
            'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ “Chọn trường xuất file”.',
            'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất. Mặc định hệ thống tích sẵn đúng những cột đang hiển thị trên bảng, theo thứ tự trên bảng (ban đầu là Hạng mục, Người tạo, Ngày tạo, Trạng thái). Muốn có Ký hiệu, Mô tả trong file thì tích thêm.',
            'Bước 4: Bấm {icon:btn_xuatfile}. Hệ thống tải về file danh_muc_ghi_chu_kiem_tra_bao_duong.xlsx và báo “Xuất Excel thành công”.',
        ],
        'truong': 'Chọn nhiều trường: Hạng mục, Ký hiệu, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật.',
        'ghi_chu': [
            'Lưu ý: file xuất chứa TOÀN BỘ kết quả tìm kiếm (tối đa 10,000 dòng), không chỉ các dòng của trang đang xem. Cột STT luôn đứng đầu file; Mô tả dài được giữ nguyên, không cắt cụt. Cột Trạng thái ghi chữ Hoạt động hoặc Khóa.',
            'Người chỉ có quyền Xem vẫn xuất Excel được.',
        ],
    },
    'import': {
        'tieu_de': 'Import ghi chú kiểm tra bảo dưỡng',
        'file': 'Mau_import_ghi_chu_kiem_tra_bao_duong.xlsx',
        'cot_text': 'STT, Hạng mục (bắt buộc), Ký hiệu (bắt buộc), Mô tả',
        'toast': 'Import thành công N ghi chú kiểm tra bảo dưỡng.',
        'loi': [
            ['Hạng mục không được để trống', 'Dòng đó bỏ trống cột Hạng mục.'],
            ['Hạng mục tối đa 255 ký tự', 'Hạng mục quá dài, rút gọn lại.'],
            ['Hạng mục bị trùng với dòng N trong file', 'Trong chính file có hai dòng cùng Hạng mục (không phân biệt hoa thường).'],
            ['Hạng mục đã tồn tại trong hệ thống', 'Danh mục đã có ghi chú cùng Hạng mục.'],
            ['Ký hiệu không được để trống', 'Dòng đó bỏ trống cột Ký hiệu.'],
            ['Ký hiệu tối đa 255 ký tự', 'Ký hiệu quá dài.'],
            ['Ký hiệu bị trùng với dòng N trong file', 'Trong chính file có hai dòng cùng Ký hiệu (so sau khi chuyển chữ in hoa).'],
            ['Ký hiệu đã tồn tại trong hệ thống', 'Danh mục đã có ghi chú cùng Ký hiệu (so sau khi chuyển chữ in hoa).'],
            ['Mô tả tối đa 255 ký tự', 'Mô tả quá dài, rút gọn lại.'],
        ],
        'ghi_chu': ['Lưu ý: nút Import Excel chỉ hiện với người có quyền Quản lý. Ký hiệu trong file được tự chuyển thành chữ in hoa. Mỗi lần nhập tối đa 500 dòng; file dài hơn hệ thống báo “File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần.” Người tạo của ghi chú nhập từ Excel là chính người thực hiện nhập, và lịch sử có mốc Tạo mới. Ghi chú nhập từ Excel luôn ở trạng thái Hoạt động (file mẫu không có cột Trạng thái).'],
    },
    'tuy_chinh_cot': {'cot_khoa': 'Ba cột STT, Hạng mục và Hành động'},

    'shots': {'list': '01_list.png', 'rowmenu': '03_rowmenu.png', 'filter': 'filter.png', 'filter_result': '04_filter_result.png',
              'create': '10_create.png', 'create_error': '11_create_error.png', 'edit': '12_edit.png',
              'delete': '13_delete.png', 'lock': '14_lock.png', 'unlock': '15_unlock.png', 'history': '16_history.png',
              'detail': '17_detail.png', 'export': '20_export.png', 'import_open': '21_import_open.png',
              'import_loaded': '22_import_loaded.png', 'import_validated': '23_import_validated.png', 'colcfg': '25_colcfg.png'},

    # lockName: ghi chú đang Hoạt động, CHƯA được gắn vào gói nào (tra DB local_hrm_erp 28/09/2026, id 13) -> dòng đủ 4 nút.
    'capture': {'route': '/customer-care/note-maintenances',
                'menu': {'phanhe': 'CSKH SAU BÁN', 'nhom': 'Danh mục', 'muc': 'Ghi chú kiểm tra bảo dưỡng'},
                'search': 'Tìm theo hạng mục hoặc ký hiệu', 'searchText': 'Kiểm tra', 'detailCol': 1,
                'lockName': 'Kiểm tra hệ thống điều hoà ô tô', 'create': True, 'lock': True},

    'import_test': {
        'cols': ['STT', 'Hạng mục *', 'Ký hiệu *', 'Mô tả'],
        'rows': [
            [1, 'DOC-Kiểm tra độ căng dây curoa', 'DOC1', 'Kiểm tra độ căng và độ mòn dây curoa'],
            [2, 'DOC-Kiểm tra áp suất lốp', 'doc2', ''],                         # ký hiệu chữ thường -> DOC2
            [3, 'DOC-Vệ sinh két nước', 'DOC3', 'Vệ sinh két nước làm mát'],
            [4, '', '', ''],                                                     # bỏ trống 2 cột bắt buộc
            [5, 'DOC-Kiểm tra độ căng dây curoa', 'DOC5', ''],                   # trùng Hạng mục dòng 1 trong file
            [6, 'DOC-Kiểm tra đèn báo', 'doc1', ''],                             # trùng Ký hiệu dòng 1 (sau khi in hoa)
            [7, 'Kiểm tra ngoại quan không tháo lắp', 'KTBM', ''],               # trùng hệ thống cả 2
            [8, 'DOC-Mô tả quá dài', 'DOC8', 'M' * 300],                         # Mô tả > 255 ký tự
        ],
    },

    'uml': {
        'mains': [('FR-01', 'Xem danh sách ghi chú kiểm tra', 'view'), ('FR-03', 'Thêm mới ghi chú kiểm tra', 'crud'),
                  ('FR-04', 'Chỉnh sửa ghi chú kiểm tra', 'crud'), ('FR-05', 'Xóa ghi chú kiểm tra', 'action'),
                  ('FR-06', 'Khóa / Mở khóa ghi chú kiểm tra', 'action'),
                  ('FR-08', 'Import file ghi chú kiểm tra', 'io'), ('FR-09', 'Xuất danh sách ghi chú kiểm tra ra Excel', 'io')],
        'subs': [('FR-02', 'Tìm kiếm và lọc ghi chú kiểm tra', 'view'), ('FR-10', 'Xem chi tiết ghi chú kiểm tra', 'view'),
                 ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
        'rieng': [('FR-10', 'Xem chi tiết ghi chú kiểm tra', 'view')],
    },

    'srs': {
        'muc_dich': ['Là căn cứ nghiệm thu chức năng.',
                     'Làm rõ hai ràng buộc trùng độc lập (Hạng mục, Ký hiệu), quy tắc Ký hiệu in hoa, trạng thái Hoạt động / Khóa và điều kiện xóa: chỉ xóa hẳn ghi chú đang Hoạt động chưa gắn vào cấp bảo dưỡng của gói dịch vụ.'],
        'quyen_truoc': ['Màn hình dùng 2 quyền riêng, không phân quyền theo công ty / phòng ban / bộ phận. Không có quyền nào thì mục menu bị ẩn và không vào được màn hình.'],
        'quyen_rows': [[Q_XEM, 'Vào màn hình, xem danh sách, tìm kiếm, lọc, xem chi tiết, xem lịch sử, xuất Excel.'],
                       [Q_QL, 'Toàn bộ quyền Xem, cộng thêm Tạo mới, Sửa, Xóa, Khóa, Mở khóa, Import Excel.']],
        'ma_tran': [['Chức năng', Q_XEM, Q_QL]] + [[f, x, 'Có'] for f, x in [
            ('FR-01 Xem danh sách ghi chú kiểm tra', 'Có'), ('FR-02 Tìm kiếm và lọc', 'Có'), ('FR-03 Thêm mới ghi chú kiểm tra', 'Không'),
            ('FR-04 Chỉnh sửa ghi chú kiểm tra', 'Không'), ('FR-05 Xóa ghi chú kiểm tra', 'Không'), ('FR-06 Khóa / Mở khóa ghi chú kiểm tra', 'Không'),
            ('FR-07 Xem lịch sử thay đổi', 'Có'), ('FR-08 Import file ghi chú kiểm tra', 'Không'), ('FR-09 Xuất danh sách ra Excel', 'Có'),
            ('FR-10 Xem chi tiết ghi chú kiểm tra', 'Có'), ('FR-11 Tùy chỉnh cột hiển thị', 'Có')]],
        'ma_tran_widths': [2.4, 1.6, 1.6],
        'quyen_sau': ['Nút không có quyền dùng thì ẩn hẳn. Máy chủ kiểm tra lại quyền ở mọi chức năng ghi dữ liệu (Tạo mới, Sửa, Xóa, Khóa, Mở khóa, Import) và ở chức năng xem/xuất.'],
        'fr': [
            {'ten': 'Xem danh sách ghi chú kiểm tra',
             'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của Danh mục ghi chú kiểm tra bảo dưỡng tại phần mô tả chi tiết.',
             'gioi_thieu': [['Tên chức năng', 'Xem danh sách ghi chú kiểm tra'],
                            ['Mô tả', 'Hiển thị toàn bộ ghi chú kiểm tra trong danh mục (cả Hoạt động lẫn Khóa), có phân trang và sắp xếp.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý ghi chú kiểm tra bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Người dùng đã đăng nhập và có ít nhất một trong hai quyền của màn hình.'],
                            ['Dòng sự kiện chính', '1. Người dùng vào menu CSKH sau bán → Danh mục → Ghi chú kiểm tra bảo dưỡng.\n2. Hệ thống nạp trang đầu tiên của danh sách (10 dòng).\n3. Bảng hiển thị dữ liệu kèm tổng số bản ghi.'],
                            ['Dòng sự kiện phụ', '• Không có bản ghi khớp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n• Không có quyền nào của màn hình → mục menu bị ẩn, không vào được màn hình.']],
             'anh': [('list', 'Màn Danh mục ghi chú kiểm tra bảo dưỡng lúc mới truy cập')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Mô tả'],
                    ['1', 'STT', 'Table/Grid', 'Read-only', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị, không ẩn được.'],
                    ['2', 'Hạng mục', 'Table/Grid', 'Read-only', 'Luôn hiển thị, sắp xếp được. Bấm vào mở cửa sổ Xem (xem 2.10).'],
                    ['3', 'Ký hiệu', 'Table/Grid', 'Read-only', 'Chữ in hoa. Mặc định ẩn.'],
                    ['4', 'Mô tả', 'Table/Grid', 'Read-only', 'Nội dung dài xuống dòng trong ô. Mặc định ẩn.'],
                    ['5', 'Người tạo', 'Table/Grid', 'Read-only', 'Người đã thêm bản ghi.'],
                    ['6', 'Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm, sắp xếp được.'],
                    ['7', 'Người cập nhật', 'Table/Grid', 'Read-only', 'Mặc định ẩn.'],
                    ['8', 'Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm. Mặc định ẩn, sắp xếp được.'],
                    ['9', 'Trạng thái', 'Badge', 'Read-only', 'Hoạt động hoặc Khóa.'],
                    ['10', 'Hành động', 'Table/Grid', 'Read-only', 'Sửa (quyền Quản lý, ghi chú đang Hoạt động), Xóa (quyền Quản lý, ghi chú đang Hoạt động và chưa gắn vào gói dịch vụ), Khóa / Mở khóa (quyền Quản lý), Lịch sử (luôn hiện). Từ 4 nút trở lên thì 2 nút đầu hiện thẳng, còn lại trong nút ba chấm.'],
                    ['11', 'Nút Tạo mới', 'Button', 'Enable', 'Chỉ hiện với quyền Quản lý. Mở cửa sổ Tạo ghi chú kiểm tra.'],
                    ['12', 'Nút Xuất Excel', 'Button', 'Enable', 'Mở cửa sổ Chọn trường xuất file (xem 2.9).'],
                    ['13', 'Nút Import Excel', 'Button', 'Enable', 'Chỉ hiện với quyền Quản lý. Mở cửa sổ Import ghi chú kiểm tra bảo dưỡng (xem 2.8).'],
                    ['14', 'Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', 'Mở cửa sổ Tuỳ chỉnh cột (xem 2.11).'],
                    ['15', 'Phân trang', 'Pagination', 'Enable', 'Số dòng/trang 5 / 10 / 20 / 50 / 100, mặc định 10.']],
             'ui_widths': [0.6, 1.4, 0.9, 0.8, 3],
             'events': [['Mở màn hình', 'System', 'After:\n– Nạp trang đầu (xếp theo thứ tự tạo), hiển thị tổng số bản ghi.'],
                        ['Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Đổi chiều sắp xếp và nạp lại danh sách từ trang 1.'],
                        ['Chuyển trang', 'Click', 'Before:\n– Giữ nguyên từ khóa, Trạng thái và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'],
                        ['Đổi số dòng mỗi trang', 'Change', 'After:\n– Quay về trang 1 và nạp lại theo số dòng mới.']]},
            {'ten': 'Tìm kiếm và lọc ghi chú kiểm tra',
             'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang. Chỉ bổ sung tiêu chí tìm kiếm/lọc riêng của Danh mục ghi chú kiểm tra bảo dưỡng.',
             'gioi_thieu': [['Tên chức năng', 'Tìm kiếm và lọc ghi chú kiểm tra'],
                            ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh theo Hạng mục hoặc Ký hiệu và ô Trạng thái. Màn hình không có Tìm kiếm nâng cao.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý'],
                            ['Điều kiện ban đầu', 'Đang ở màn Danh mục ghi chú kiểm tra bảo dưỡng.'],
                            ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa và bấm Tìm kiếm / Enter, hoặc chọn Trạng thái (lọc ngay).\n2. Hệ thống áp đồng thời các tiêu chí (Hạng mục HOẶC Ký hiệu chứa từ khóa, không phân biệt hoa thường; đúng Trạng thái), nạp lại danh sách từ trang 1.'],
                            ['Dòng sự kiện phụ', '• Từ khóa chỉ có trong Mô tả → không ra kết quả (Mô tả không được quét).\n• Gõ mà chưa bấm Tìm kiếm / Enter → danh sách chưa lọc.\n• Bấm Làm mới → xóa từ khóa và Trạng thái VÀ nạp lại danh sách đầy đủ ngay.\n• Điều kiện được ghi nhớ 10 phút khi quay lại màn hình.']],
             'anh': [('filter', 'Khu vực tìm kiếm và lọc của màn Danh mục ghi chú kiểm tra bảo dưỡng')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Mô tả'],
                    ['1', 'Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Placeholder “Tìm theo hạng mục hoặc ký hiệu...”. Quét Hạng mục và Ký hiệu (khớp một phần).'],
                    ['2', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Nhãn nổi. Bỏ trống thì hiện cả hai trạng thái. Chọn là lọc ngay.'],
                    ['3', 'Nút Tìm kiếm', 'Button', 'Enable', '–', 'Áp dụng các tiêu chí.'],
                    ['4', 'Nút Làm mới', 'Button', 'Enable', '–', 'Xóa hết tiêu chí VÀ nạp lại danh sách ngay.']],
             'ui_widths': [0.6, 1.2, 0.8, 0.7, 1.1, 2.6],
             'events': [['Bấm Tìm kiếm / Enter', 'Click', 'After:\n– Áp đồng thời các tiêu chí theo kiểu “và”, nạp lại bảng từ trang 1.'],
                        ['Chọn Trạng thái', 'Change', 'After:\n– Lọc ngay, nạp lại bảng từ trang 1.'],
                        ['Bấm Làm mới', 'Click', 'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ.']]},
            {'ten': 'Thêm mới ghi chú kiểm tra', 'uc': 'uc_fr03',
             'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Thêm mới ghi chú kiểm tra'],
                            ['Mô tả', 'Thêm một ghi chú kiểm tra mới thông qua cửa sổ nhập liệu.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý ghi chú kiểm tra bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Đang ở màn Danh mục ghi chú kiểm tra bảo dưỡng.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở cửa sổ “Tạo ghi chú kiểm tra”, Trạng thái mặc định Hoạt động.\n3. Người dùng nhập Hạng mục, Ký hiệu, Mô tả, (tùy chọn) đổi Trạng thái và bấm Lưu.\n4. Hệ thống cắt khoảng trắng đầu cuối, chuyển Ký hiệu thành chữ in hoa, kiểm tra dữ liệu, ghi bản ghi mới và ghi lịch sử Tạo mới.\n5. Cửa sổ đóng, danh sách nạp lại, báo “Thêm mới thành công”.'],
                            ['Dòng sự kiện phụ', '• Bỏ trống Hạng mục / Ký hiệu, quá 255 ký tự → báo đỏ ngay dưới ô + toast “Bạn chưa nhập đầy đủ thông tin”, cửa sổ KHÔNG đóng.\n• Trùng Hạng mục → “Hạng mục đã tồn tại”; trùng Ký hiệu → “Ký hiệu đã tồn tại”.\n• Bấm “Lưu và tiếp tục” → ghi bản ghi rồi giữ cửa sổ mở với các ô trống, Trạng thái về Hoạt động.\n• Bấm Đóng khi đã nhập dở → hỏi “Thông tin chưa lưu” (Thoát / Ở lại).'],
                            ['Yêu cầu đặc biệt', 'Cửa sổ có ba nút: Lưu, Lưu và tiếp tục, Đóng. Nút Lưu bị khóa trong lúc đang ghi để chống bấm hai lần.']],
             'menu_them': ' => Tạo mới {icon:btn_taomoi}',
             'ghi_chu_layout': 'Cửa sổ Tạo ghi chú kiểm tra được mở ngay trên màn hình danh sách.',
             'anh': [('create', 'Cửa sổ Tạo ghi chú kiểm tra'), ('create_error', 'Lỗi đỏ ngay dưới ô còn thiếu')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Mô tả'],
                    ['1', 'Hạng mục', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Duy nhất (kể cả ghi chú đang Khóa). Bỏ trống “Bắt buộc phải nhập”; trùng “Hạng mục đã tồn tại”; quá dài “Vui lòng nhập tối đa 255 ký tự.”'],
                    ['2', 'Ký hiệu', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Duy nhất (kể cả ghi chú đang Khóa), tự chuyển chữ in hoa khi lưu. Bỏ trống “Bắt buộc phải nhập” (máy chủ báo sau khi bấm Lưu); trùng “Ký hiệu đã tồn tại”.'],
                    ['3', 'Mô tả', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Quá dài “Vui lòng nhập tối đa 255 ký tự.”'],
                    ['4', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Mặc định Hoạt động, luôn có giá trị (không xóa trống được).'],
                    ['5', 'Nút Lưu', 'Button', 'Enable', '', '', 'Ghi bản ghi rồi đóng cửa sổ.'],
                    ['6', 'Nút Lưu và tiếp tục', 'Button', 'Enable', '', '', 'Ghi bản ghi rồi giữ cửa sổ mở để nhập tiếp.'],
                    ['7', 'Nút Đóng', 'Button', 'Enable', '', '', 'Hủy bỏ, không ghi gì.']],
             'ui_widths': [0.6, 1.3, 0.8, 0.6, 1.1, 0.5, 2.3],
             'events': [['Bấm nút Tạo mới', 'Click', 'After:\n– Mở cửa sổ nhập liệu với các ô trống, Trạng thái = Hoạt động.'],
                        ['Bấm Lưu', 'Click', 'During:\n– Kiểm tra bắt buộc, độ dài, trùng Hạng mục và trùng Ký hiệu (sau khi in hoa).\n– Có lỗi → báo đỏ dưới ô, không thực hiện After.\nAfter:\n– Ghi bản ghi mới, người tạo là người đang đăng nhập, ghi lịch sử Tạo mới.\n– Đóng cửa sổ, nạp lại danh sách, báo “Thêm mới thành công”.'],
                        ['Bấm Lưu và tiếp tục', 'Click', 'During:\n– Như nút Lưu.\nAfter:\n– Ghi bản ghi, xóa trắng các ô, GIỮ cửa sổ mở.'],
                        ['Bấm Đóng', 'Click', 'After:\n– Chưa nhập gì → đóng cửa sổ. Đã nhập → hỏi “Thông tin chưa lưu”.']]},
            {'ten': 'Chỉnh sửa ghi chú kiểm tra', 'uc': 'uc_fr04',
             'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Chỉnh sửa ghi chú kiểm tra'],
                            ['Mô tả', 'Sửa thông tin, trạng thái của một ghi chú đã có. Dùng chung cửa sổ với Thêm mới.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý ghi chú kiểm tra bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Ghi chú đang ở trạng thái Hoạt động.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm biểu tượng bút chì ở dòng cần sửa.\n2. Hệ thống mở cửa sổ “Sửa ghi chú kiểm tra” với dữ liệu hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi và ghi lịch sử.\n5. Cửa sổ đóng, báo “Cập nhật thành công”.'],
                            ['Dòng sự kiện phụ', '• Giữ nguyên Hạng mục / Ký hiệu của chính bản ghi → không báo trùng.\n• Ghi chú đang được gắn vào gói dịch vụ vẫn sửa được.\n• Ghi chú vừa bị người khác khóa → báo “%s”, không ghi thay đổi.\n• Ghi chú vừa bị người khác xóa (lúc mở cửa sổ) → báo “Dữ liệu đã thay đổi, vui lòng tải lại”.' % MSG_LOCKED]],
             'menu_them': ' => Sửa {icon:btn_sua}',
             'anh': [('edit', 'Cửa sổ Sửa ghi chú kiểm tra')],
             'events': [['Bấm biểu tượng bút chì', 'Click', 'Before:\n– Không có quyền Quản lý hoặc ghi chú đang Khóa thì nút không hiển thị.\nAfter:\n– Mở cửa sổ với dữ liệu hiện tại.'],
                        ['Bấm Lưu', 'Click', 'Before:\n– Máy chủ chặn nếu ghi chú đang Khóa (“%s”).\nDuring:\n– Kiểm tra như Thêm mới, bỏ qua trùng với chính bản ghi.\nAfter:\n– Ghi thay đổi, ghi lịch sử “Thay đổi thông tin” (đổi Trạng thái ghi mốc “Thay đổi trạng thái” riêng), báo “Cập nhật thành công”.' % MSG_LOCKED]]},
            {'ten': 'Xóa ghi chú kiểm tra', 'uc': 'uc_fr05',
             'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Xóa ghi chú kiểm tra'],
                            ['Mô tả', 'Xóa hẳn một ghi chú đang Hoạt động và chưa được gắn vào gói dịch vụ.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý ghi chú kiểm tra bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Ghi chú đang Hoạt động và chưa được chọn ở ' + USED_N + ' nào.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm biểu tượng thùng rác.\n2. Hệ thống hiện hộp “Xác nhận xóa” nêu rõ Hạng mục.\n3. Người dùng bấm Xóa.\n4. Máy chủ kiểm tra lại trạng thái và tình trạng sử dụng, xóa hẳn bản ghi, ghi lịch sử Xóa.\n5. Hệ thống báo “Xóa thành công”, nạp lại danh sách.'],
                            ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Ghi chú đang được sử dụng hoặc đang Khóa → nút Xóa KHÔNG hiển thị.\n• Ghi chú vừa được người khác gắn vào gói → báo “%s”, không xóa.\n• Ghi chú vừa bị người khác khóa → báo “%s”, không xóa.' % (MSG_USED, MSG_LOCKED)]],
             'menu_them': ' => Xóa {icon:btn_xoa}',
             'anh': [('delete', 'Hộp xác nhận xóa ghi chú kiểm tra')],
             'events': [['Bấm biểu tượng thùng rác', 'Click', 'Before:\n– Chỉ hiện khi ghi chú đang Hoạt động và chưa được sử dụng.\nAfter:\n– Hiện hộp xác nhận kèm Hạng mục.'],
                        ['Bấm Xóa', 'Click', 'During:\n– Máy chủ chặn nếu ghi chú đang Khóa (“%s”) hoặc đã được sử dụng (“%s”).\nAfter:\n– Xóa hẳn bản ghi, nạp lại danh sách, báo “Xóa thành công”.' % (MSG_LOCKED, MSG_USED)],
                        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.']]},
            {'ten': 'Khóa / Mở khóa ghi chú kiểm tra', 'uc': 'uc_fr06',
             'qtc': 'Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Khóa / Mở khóa ghi chú kiểm tra'],
                            ['Mô tả', 'Đổi trạng thái ghi chú giữa Hoạt động và Khóa. Ghi chú đã Khóa vẫn nằm trong danh mục nhưng không chọn được ở gói bảo dưỡng mới.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý ghi chú kiểm tra bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Ghi chú cần đổi trạng thái đang có trong danh sách (khóa được cả ghi chú đang được sử dụng).'],
                            ['Dòng sự kiện chính', '1. Người dùng chọn Khóa (hoặc Mở khóa) ở cột Hành động.\n2. Hệ thống hiện hộp xác nhận “Khóa ghi chú kiểm tra” / “Mở khóa ghi chú kiểm tra” nêu rõ Hạng mục.\n3. Người dùng xác nhận.\n4. Hệ thống đổi trạng thái, ghi lịch sử, báo “Khóa thành công” / “Mở khóa thành công”.'],
                            ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Sau khi Khóa, nút Sửa và Xóa biến mất, chỉ còn Mở khóa và Lịch sử.\n• Ghi chú đã bị người khác đổi trạng thái → báo “%s”.' % MSG_CONFLICT],
                            ['Yêu cầu đặc biệt', 'Ghi chú đã Khóa không còn chọn được khi khai báo nội dung kiểm tra theo cấp ở gói bảo dưỡng mới và khi Import gói bảo dưỡng. Gói cũ đang dùng giữ nguyên, hiển thị đúng ký hiệu kèm 🔒.']],
             'menu_them': ' => Khóa / Mở khóa',
             'anh': [('lock', 'Hộp xác nhận khóa ghi chú kiểm tra'), ('unlock', 'Hộp xác nhận mở khóa ghi chú kiểm tra')],
             'events': [['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm Hạng mục.'],
                        ['Xác nhận', 'Click', 'During:\n– Bản ghi đã ở trạng thái đích → báo “%s”, dừng.\nAfter:\n– Đổi trạng thái, KHÔNG xóa dữ liệu, ghi lịch sử “Thay đổi trạng thái”, cập nhật cột Trạng thái và các nút.' % MSG_CONFLICT],
                        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.']]},
            {'ten': 'Xem lịch sử thay đổi',
             'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục ghi chú kiểm tra bảo dưỡng nếu có.',
             'gioi_thieu': [['Tên chức năng', 'Xem lịch sử thay đổi'],
                            ['Mô tả', 'Liệt kê các lần thay đổi của một ghi chú (Hạng mục, Ký hiệu, Mô tả, Trạng thái), kèm giá trị cũ → mới, người thực hiện và thời điểm.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý'],
                            ['Dòng sự kiện chính', '1. Người dùng chọn Lịch sử ở cột Hành động, hoặc mở cửa sổ Xem ghi chú kiểm tra.\n2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <hạng mục>”, mốc mới nhất ở trên cùng.'],
                            ['Dòng sự kiện phụ', '• Bản ghi chưa có mốc nào → “Chưa có lịch sử thao tác nào.”\n• Có bộ lọc theo loại hành động, người thực hiện, thời gian.']],
             'menu_them': ' => Lịch sử',
             'anh': [('history', 'Cửa sổ Lịch sử thay đổi của ghi chú kiểm tra')]},
            {'ten': 'Import file ghi chú kiểm tra', 'uc': 'uc_fr08',
             'qtc': 'Quy tắc Import file, Validate dữ liệu, Thông báo và Quy định chung về danh mục. Chỉ bổ sung mapping/validation riêng của Danh mục ghi chú kiểm tra bảo dưỡng.',
             'gioi_thieu': [['Tên chức năng', 'Import file ghi chú kiểm tra'],
                            ['Mô tả', 'Thêm nhiều ghi chú kiểm tra cùng lúc từ file Excel mẫu, có bước Validate trước khi ghi.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý ghi chú kiểm tra bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Đang ở màn Danh mục ghi chú kiểm tra bảo dưỡng và đã chuẩn bị file theo mẫu.'],
                            ['Dòng sự kiện chính', '1. Bấm Import Excel.\n2. Bấm Tải file mẫu (Mau_import_ghi_chu_kiem_tra_bao_duong.xlsx), điền dữ liệu.\n3. Bấm Chọn file Excel rồi Load lên bảng.\n4. Bấm Validate; hệ thống chuyển Ký hiệu thành chữ in hoa, kiểm tra từng dòng như quy tắc Thêm mới (mục 2.3), khóa dòng hợp lệ.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi.\n6. Bấm Import; hệ thống ghi các dòng hợp lệ, báo “Import thành công N ghi chú kiểm tra bảo dưỡng.”, đóng cửa sổ và nạp lại danh sách.'],
                            ['Dòng sự kiện phụ', '• File không phải .xlsx/.xls → “Vui lòng chọn file .xlsx hoặc .xls”.\n• Quá 500 dòng → “File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần.”\n• Còn dòng lỗi → nút Import không bấm được.\n• Có dòng ghi thất bại lúc Import → “Import thành công x/y ghi chú kiểm tra bảo dưỡng. N dòng thất bại.”'],
                            ['Yêu cầu đặc biệt', 'Validate không ghi dữ liệu. Bản ghi import luôn ở trạng thái Hoạt động, người tạo là người thực hiện, lịch sử có mốc Tạo mới.']],
             'menu_them': ' => Import Excel {icon:btn_import}',
             'ghi_chu_layout': 'Cửa sổ Import được mở ngay trên màn hình danh sách.',
             'anh': [('import_open', 'Cửa sổ Import ghi chú kiểm tra bảo dưỡng khi vừa mở'), ('import_loaded', 'Dữ liệu đã được load lên bảng xem trước'),
                     ('import_validated', 'Kết quả Validate — mỗi dòng lỗi nêu rõ lý do')],
             'bang_them': [('Quy tắc kiểm tra riêng của file Import', [['Cột', 'Quy tắc / thông báo lỗi'],
                            ['Hạng mục *', 'Bắt buộc (“Hạng mục không được để trống”), tối đa 255 ký tự (“Hạng mục tối đa 255 ký tự”), không trùng trong file (“Hạng mục bị trùng với dòng N trong file”), không trùng hệ thống kể cả ghi chú đang Khóa (“Hạng mục đã tồn tại trong hệ thống”). So trùng không phân biệt hoa thường.'],
                            ['Ký hiệu *', 'Tự chuyển chữ in hoa. Bắt buộc (“Ký hiệu không được để trống”), tối đa 255 ký tự (“Ký hiệu tối đa 255 ký tự”), không trùng trong file (“Ký hiệu bị trùng với dòng N trong file”), không trùng hệ thống kể cả ghi chú đang Khóa (“Ký hiệu đã tồn tại trong hệ thống”).'],
                            ['Mô tả', 'Không bắt buộc, tối đa 255 ký tự (“Mô tả tối đa 255 ký tự”) — cùng giới hạn với ô Mô tả ở cửa sổ Tạo mới.']], [1.2, 4])]},
            {'ten': 'Xuất danh sách ghi chú kiểm tra ra Excel', 'uc': 'uc_fr09',
             'qtc': 'Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của Danh mục ghi chú kiểm tra bảo dưỡng.',
             'gioi_thieu': [['Tên chức năng', 'Xuất danh sách ghi chú kiểm tra ra Excel'],
                            ['Mô tả', 'Xuất kết quả đang tìm kiếm / lọc ra file Excel, cho phép chọn trường và thứ tự cột.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý'],
                            ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiển thị trên bảng.\n3. Người dùng tích chọn và kéo ☰ để sắp thứ tự.\n4. Bấm Xuất file; hệ thống tải danh_muc_ghi_chu_kiem_tra_bao_duong.xlsx theo đúng từ khóa, Trạng thái, thứ tự sắp xếp và thứ tự trường, báo “Xuất Excel thành công”.'],
                            ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Bấm Đóng → không xuất gì.\n• Kết quả rỗng → file chỉ có dòng tiêu đề.'],
                            ['Yêu cầu đặc biệt', 'File chứa toàn bộ kết quả tìm kiếm (tối đa 10,000 dòng), không giới hạn ở trang đang xem. Cột STT luôn đứng đầu. Chỉ xuất Excel.']],
             'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
             'anh': [('export', 'Cửa sổ Chọn trường xuất file')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
                    ['1', 'Danh sách trường', 'Checkbox chọn nhiều', 'Enable', 'Tích sẵn cột đang hiển thị', 'Hạng mục, Ký hiệu, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Kéo ☰ đổi thứ tự.'],
                    ['2', 'Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', 'Hiển thị', 'Tích / bỏ tích toàn bộ.'],
                    ['3', 'Nút Xuất file', 'Button', 'Enable/Disable', 'Mờ khi chưa chọn trường', 'Sinh file và tải về.'],
                    ['4', 'Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.']],
             'ui_widths': [0.6, 1.5, 1, 0.8, 1.2, 2.6]},
            {'ten': 'Xem chi tiết ghi chú kiểm tra', 'uc': 'uc_fr10',
             'qtc': 'Màn Xem chi tiết và Phân quyền.',
             'gioi_thieu': [['Tên chức năng', 'Xem chi tiết ghi chú kiểm tra'],
                            ['Mô tả', 'Cửa sổ “Xem ghi chú kiểm tra” hiển thị Hạng mục, Ký hiệu, Mô tả, Trạng thái ở chế độ chỉ đọc, kèm khối Lịch sử.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm Hạng mục ở danh sách.\n2. Hệ thống mở cửa sổ Xem, chỉ có nút Đóng.'],
                            ['Dòng sự kiện phụ', '• Ghi chú đang Khóa vẫn xem được.\n• Ghi chú vừa bị người khác xóa → báo “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.']],
             'anh': [('detail', 'Cửa sổ Xem ghi chú kiểm tra ở chế độ chỉ đọc')]},
            {'ten': 'Tùy chỉnh cột hiển thị',
             'qtc': 'Tùy chỉnh cột.',
             'gioi_thieu': [['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
                            ['Mô tả', 'Bật/tắt và sắp xếp thứ tự cột của bảng; cấu hình lưu riêng theo người dùng.'],
                            ['Yêu cầu đặc biệt', 'Cột STT, Hạng mục, Hành động bị khóa. Mặc định ẩn: Ký hiệu, Mô tả, Người cập nhật, Ngày cập nhật.']],
             'menu_them': ' => Cấu hình cột {icon:btn_cauhinhcot}',
             'anh': [('colcfg', 'Cửa sổ Tuỳ chỉnh cột')]},
        ],
        'quy_tac': [
            ('BR-01', 'Ràng buộc trùng Hạng mục',
             ['Hạng mục không được trùng trong danh mục, kể cả ghi chú đang Khóa; khi sửa, bản ghi đang sửa được loại khỏi phép so trùng.',
              'Thông báo khi trùng: “Hạng mục đã tồn tại”; khi Import: “Hạng mục đã tồn tại trong hệ thống” hoặc “Hạng mục bị trùng với dòng N trong file”.'],
             ['Thêm mới ghi chú kiểm tra', 'Chỉnh sửa ghi chú kiểm tra', 'Import file ghi chú kiểm tra']),
            ('BR-02', 'Ràng buộc trùng Ký hiệu',
             ['Ký hiệu không được trùng trong danh mục (kể cả ghi chú đang Khóa), độc lập với ràng buộc trùng Hạng mục.',
              'Ký hiệu được cắt khoảng trắng hai đầu và lưu bằng chữ IN HOA (cả nhập tay lẫn Import), nên “ktbm” và “KTBM” bị coi là trùng.',
              'Thông báo khi trùng: “Ký hiệu đã tồn tại”; khi Import: “Ký hiệu đã tồn tại trong hệ thống” hoặc “Ký hiệu bị trùng với dòng N trong file”.'],
             ['Thêm mới ghi chú kiểm tra', 'Chỉnh sửa ghi chú kiểm tra', 'Import file ghi chú kiểm tra']),
            ('BR-03', 'Điều kiện xóa ghi chú',
             ['Chỉ xóa được ghi chú đang Hoạt động VÀ chưa được chọn ở ' + USED_N + ' nào; ngược lại nút Xóa bị ẩn.',
              'Xóa là xóa hẳn bản ghi khỏi hệ thống. Ghi chú đã được sử dụng thì dùng Khóa thay cho Xóa.',
              'Máy chủ kiểm tra lại tại thời điểm xóa: đã được sử dụng báo “%s”; đang Khóa báo “%s”.' % (MSG_USED, MSG_LOCKED)],
             ['Xóa ghi chú kiểm tra']),
            ('BR-04', 'Ghi chú đang Khóa',
             ['Khóa được cả ghi chú đang được sử dụng.',
              'Ghi chú đang Khóa không sửa, không xóa được; phải Mở khóa trước. Máy chủ chặn với câu “%s”.' % MSG_LOCKED,
              'Ghi chú đang Khóa không còn chọn được ở gói bảo dưỡng mới và khi Import gói bảo dưỡng (báo “Ghi chú kiểm tra "…" không có trong danh mục hoặc đã bị khóa”).',
              'Gói cũ đang dùng ghi chú đó giữ nguyên, hiển thị đúng ký hiệu kèm 🔒.',
              'Ghi chú đang được gói dịch vụ sử dụng vẫn sửa được khi đang Hoạt động; các gói đang dùng hiển thị nội dung mới.'],
             ['Chỉnh sửa ghi chú kiểm tra', 'Xóa ghi chú kiểm tra', 'Khóa / Mở khóa ghi chú kiểm tra', 'Cấp bảo dưỡng của gói dịch vụ']),
            ('BR-05', 'Thao tác đồng thời',
             ['Hai người cùng Khóa hoặc cùng Mở khóa một ghi chú: người bấm sau nhận “%s”, không ghi thêm mốc lịch sử trùng.' % MSG_CONFLICT],
             ['Khóa / Mở khóa ghi chú kiểm tra']),
            ('BR-06', 'Giới hạn Import',
             ['Mỗi lần Import tối đa 500 dòng; vượt quá báo “File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần.”',
              'Bước Validate không ghi dữ liệu; Hạng mục, Ký hiệu bắt buộc và tối đa 255 ký tự; Mô tả tối đa 255 ký tự.',
              'Ghi chú nhập từ Excel luôn ở trạng thái Hoạt động.'],
             ['Import file ghi chú kiểm tra']),
            ('BR-07', 'Ghi lịch sử thay đổi',
             ['Mọi thao tác Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa đều ghi lịch sử kèm người thực hiện.',
              'Đổi Trạng thái ngay trong cửa sổ Sửa được ghi thành mốc “Thay đổi trạng thái” riêng.',
              'Người tạo / Người cập nhật lấy theo nhân viên đang đăng nhập.'],
             ['Thêm mới ghi chú kiểm tra', 'Chỉnh sửa ghi chú kiểm tra', 'Xóa ghi chú kiểm tra', 'Khóa / Mở khóa ghi chú kiểm tra', 'Import file ghi chú kiểm tra', 'Xem lịch sử thay đổi']),
        ],
    },
}

CFG['loi_code'] = [
    'Import — Mô tả: bước Validate cho phép tới 500 ký tự (NoteMaintenanceService::validateRows báo “Mô tả tối đa 500 ký tự”), trong khi cửa sổ Tạo/Sửa và cột DB note_maintenances.description chỉ 255 ký tự. Dòng có Mô tả 256–500 ký tự qua được Validate, nút Import bấm được, rồi lúc ghi bị lỗi và rơi vào “Import thành công x/y … N dòng thất bại” (hoặc bị cắt cụt nếu MySQL không bật strict). Tài liệu đã tả đúng thiết kế: tối đa 255 ký tự, message “Mô tả tối đa 255 ký tự”.',
    'Import — thông báo “Hạng mục / Ký hiệu bị trùng với dòng N trong file” đánh số dòng lệch 1: máy chủ lấy N = thứ tự dòng + 2, trong khi cột # của bảng xem trước đánh từ 1 và dữ liệu trong file mẫu bắt đầu từ hàng 3 của Excel (hàng 1 tiêu đề, hàng 2 mô tả).',
    'Ký hiệu in hoa không nhất quán giữa Tạo/Sửa và Import: NoteMaintenanceRequest::prepareForValidation (và NoteMaintenanceService payload) dùng strtoupper — chỉ in hoa chữ Latin không dấu (gõ “đk” lưu “đK”), còn Import dùng mb_strtoupper (lưu “ĐK”). Ký hiệu thực tế đều là chữ không dấu nên ít gặp; tài liệu tả chung “tự chuyển chữ IN HOA”.',
    'Form — ô Ký hiệu có dấu * nhưng phía trình duyệt không chặn bỏ trống (chỉ có max:255); phải bấm Lưu mới nhận lỗi “Bắt buộc phải nhập” từ máy chủ. Đúng quy ước “chỉ trường Tên required ở FE” nên chỉ ghi nhận, không phải lỗi.',
    'Thao tác trên ghi chú VỪA BỊ NGƯỜI KHÁC XÓA (Xóa lần hai, Khóa, Mở khóa, bấm Lưu ở cửa sổ Sửa đang mở) nhận toast tiếng Anh “Item Not Found!”: route dùng model binding {noteMaintenance} nên Laravel trả 404 từ app/Exceptions/Handler trước khi tới guardCatalogExists() — câu “Trạng thái đã bị thay đổi. Vui lòng load lại trang” không bao giờ chạy tới. Tài liệu không tả câu này.',
    'Routes/api.php: middleware recordNotLocked đứng TRƯỚC checkPermission ở PUT/DELETE /note-maintenances/{noteMaintenance} → người chỉ có quyền Xem gọi thẳng API sửa / xóa một ghi chú đang Khóa nhận 423 “Bản ghi đang bị khoá…” thay vì 403 không có quyền (không ghi được dữ liệu, chỉ sai mã lỗi).',
]

CFG['tc_ngoai_pham_vi'] = [
    'B2, G19, G27: còn ghi đường menu cũ “Chăm sóc khách hàng → Danh mục- Dịch vụ” (G19 còn kèm đường link) — nay là CSKH sau bán → Danh mục → Ghi chú kiểm tra bảo dưỡng; tài liệu không được ghi URL.',
    'B5, TC_01.003, TC_01.004, TC_03.003 (R26, R27, R42): còn tả cột Mô tả hiện sẵn, cột “Cập nhật”, Mô tả trống hiện dấu gạch ngang — nay Ký hiệu/Mô tả mặc định ẩn, cột là Ngày cập nhật (mặc định ẩn).',
    'TC_03.002 (R41): Ký hiệu nay mặc định ẩn — phải bật ở Cấu hình cột trước khi sắp xếp (BE vẫn cho sắp xếp theo Ký hiệu nhưng cột trên bảng không khai sortable → không có mũi tên sắp xếp).',
    'TC_04.001 (R49): tiêu đề cửa sổ nay là “Tạo ghi chú kiểm tra” (không phải “Thêm ghi chú kiểm tra”), nút “Lưu và tiếp tục” (không phải “Lưu & Tiếp tục”) — ô I49 đã sửa kèm vì phải bổ sung ô Trạng thái; ô D54 còn ghi “Mở cửa sổ Thêm ghi chú kiểm tra”.',
    'TC_04.009 (R57): còn nói nút Xem trên mỗi dòng — nay bỏ nút Xem, bấm vào Hạng mục để mở cửa sổ Xem (cửa sổ có thêm ô Trạng thái chỉ đọc).',
    'TC_07.006–TC_07.008 (R89–R91): message quá dài nay là “Vui lòng nhập tối đa 255 ký tự.” (không phải “Tối đa255 ký tự”).',
    'TC_08.002 (R99): sửa ghi chú vừa bị người khác xóa — thực tế bấm Lưu nhận “Item Not Found!” (xem loi_code).',
    'Chưa có case cho Tùy chỉnh cột và khối Lịch sử trong cửa sổ Xem (Lịch sử của Khóa / Mở khóa đã có ở nhóm X).',
]

# ---- Sửa tab testcase "8. DM ghi chú kiểm tra bảo dưỡn" — số hàng theo dump ref/testcase_tab.txt tải LẠI 28/09/2026 (sau khi tab bị sửa tay, còn 129 hàng) ----
# Lượt 25/09 (Xuất Excel, ràng buộc Ký hiệu in hoa, nhóm IX Import) ĐÃ chạy lên sheet; kế hoạch dưới là lượt 28/09.
_PRE = 'Đăng nhập bằng tài khoản có quyền "Quản lý ghi chú kiểm tra bảo dưỡng". "Kiểm tra ngoại quan không tháo lắp" (KTBM) đang Hoạt động và được gắn vào cấp bảo dưỡng của gói dịch vụ; "Ghi chú thử" đang Hoạt động, chưa dùng ở đâu; "Ghi chú khóa thử" đang Khóa, chưa dùng ở đâu.'
_XF = 'Bấm Xuất Excel → cửa sổ “Chọn trường xuất file” → bấm Xuất file'
CFG['tc'] = {
    'tab': '8. DM ghi chú kiểm tra bảo dưỡn',
    'hdr_row': 69,            # "VI. XUẤT EXCEL"
    'blocks': [
        # II. BỘ LỌC & TÌM KIẾM (R31..R38, case cuối TC_02.008) — bộ lọc Trạng thái mới
        {'after': 38, 'merge_from': 31, 'cases': [
            ('TC_02.009', 'Lọc theo Trạng thái = Khóa', 'P0', _PRE,
             '1. Bấm ô Trạng thái\n2. Chọn Khóa', 'Trạng thái: Khóa',
             '- Danh sách lọc NGAY, không cần bấm Tìm kiếm, quay về trang 1\n- Chỉ hiện các ghi chú có cột Trạng thái = Khóa (có "Ghi chú khóa thử", không có "Ghi chú thử")'),
            ('TC_02.010', 'Lọc theo Trạng thái = Hoạt động', 'P1', _PRE,
             '1. Chọn Trạng thái = Hoạt động', 'Trạng thái: Hoạt động',
             '- Chỉ hiện các ghi chú đang Hoạt động (không có "Ghi chú khóa thử")'),
            ('TC_02.011', 'Bỏ trống Trạng thái thì hiện cả hai trạng thái', 'P1', _PRE,
             '1. Chọn Trạng thái = Khóa\n2. Bấm dấu x trong ô Trạng thái để xóa lựa chọn', '',
             '- Danh sách hiện lại cả ghi chú Hoạt động lẫn Khóa, tổng dưới bảng bằng toàn danh mục\n- Ô Trạng thái chỉ có 2 lựa chọn Hoạt động / Khóa, không có lựa chọn “Tất cả”'),
            ('TC_02.012', 'Kết hợp tìm nhanh với Trạng thái', 'P1', _PRE,
             '1. Gõ "Ghi chú" và bấm Tìm kiếm\n2. Chọn Trạng thái = Khóa', 'Từ khóa: Ghi chú; Trạng thái: Khóa',
             '- Chỉ hiện ghi chú có chữ "Ghi chú" trong Hạng mục / Ký hiệu VÀ đang Khóa (có "Ghi chú khóa thử", không có "Ghi chú thử")'),
            ('TC_02.013', 'Làm mới xóa cả ô Trạng thái', 'P1', _PRE,
             '1. Gõ từ khóa, bấm Tìm kiếm, chọn Trạng thái = Khóa\n2. Bấm Làm mới', '',
             '- Ô tìm nhanh và ô Trạng thái đều trống\n- Danh sách tải lại NGAY đủ toàn bộ ghi chú (cả Hoạt động lẫn Khóa)'),
        ]},
        # IV. THÊM / SỬA / XEM (R49..R61, case cuối TC_04.013) — ô Trạng thái trong cửa sổ Tạo/Sửa
        {'after': 61, 'merge_from': 49, 'cases': [
            ('TC_04.014', 'Tạo mới ghi chú ở trạng thái Khóa', 'P1', _PRE,
             '1. Bấm Tạo mới\n2. Nhập Hạng mục, Ký hiệu, chọn Trạng thái = Khóa\n3. Bấm Lưu\n4. Mở màn Danh mục gói bảo dưỡng, tạo mới một gói, mở danh sách chọn ghi chú kiểm tra ở phần cấp bảo dưỡng',
             'Hạng mục: Ghi chú tạo khóa; Ký hiệu: GCTK; Trạng thái: Khóa',
             '- Lưu thành công, báo "Thêm mới thành công"\n- Dòng mới có Trạng thái = Khóa, chỉ có Mở khóa và Lịch sử\n- Danh sách chọn ghi chú của gói mới KHÔNG có "GCTK"'),
            ('TC_04.015', 'Chuyển Trạng thái sang Khóa trong cửa sổ Sửa, kể cả ghi chú đang được sử dụng', 'P0', _PRE,
             '1. Bấm Sửa dòng "Kiểm tra ngoại quan không tháo lắp"\n2. Chọn Trạng thái = Khóa\n3. Bấm Lưu', 'Trạng thái: Khóa',
             '- Lưu thành công, báo "Cập nhật thành công" (không bị chặn vì đang được sử dụng)\n- Cột Trạng thái của dòng đó đổi thành Khóa, dòng chỉ còn Mở khóa và Lịch sử\n- Lịch sử có mốc Thay đổi trạng thái: Hoạt động → Khóa'),
            ('TC_04.016', 'Bấm Lưu khi ghi chú vừa bị người khác khóa', 'P1',
             'Tài khoản A và B cùng có quyền "Quản lý ghi chú kiểm tra bảo dưỡng"; "Ghi chú thử" đang Hoạt động.',
             '1. A mở cửa sổ Sửa "Ghi chú thử", đổi Mô tả\n2. B khóa "Ghi chú thử" ở cột Hành động\n3. A bấm Lưu', 'Mô tả: sửa khi đã khóa',
             '- A nhận thông báo "%s"\n- Mô tả KHÔNG đổi, "Ghi chú thử" vẫn ở trạng thái Khóa' % MSG_LOCKED),
        ]},
        # V. XÓA (R63..R68, case cuối TC_05.006) — điều kiện xóa mới
        {'after': 68, 'merge_from': 63, 'cases': [
            ('TC_05.007', 'Ghi chú đang Khóa KHÔNG có nút Xóa (kể cả chưa dùng ở đâu)', 'P0', _PRE,
             '1. Chọn Trạng thái = Khóa\n2. Quan sát cột Hành động của dòng "Ghi chú khóa thử"\n3. Mở khóa "Ghi chú khóa thử", quan sát lại', '',
             '- Bước 2: chỉ có Mở khóa và Lịch sử; KHÔNG có Sửa, KHÔNG có Xóa\n- Bước 3: sau khi Mở khóa, nút Sửa và Xóa hiện lại'),
            ('TC_05.008', 'Xóa ghi chú vừa bị người khác khóa', 'P1',
             'Tài khoản A và B cùng có quyền "Quản lý ghi chú kiểm tra bảo dưỡng" và cùng mở danh sách; "Ghi chú thử" đang Hoạt động, chưa dùng ở đâu.',
             '1. B khóa "Ghi chú thử"\n2. A (chưa tải lại trang) bấm thùng rác ở dòng "Ghi chú thử", bấm Xóa', '',
             '- A nhận thông báo "%s"\n- "Ghi chú thử" KHÔNG bị xóa, vẫn ở trạng thái Khóa' % MSG_LOCKED),
            ('TC_05.009', 'Chặn xóa ghi chú đang Khóa khi bỏ qua giao diện', 'P1', _PRE,
             '1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa "Ghi chú khóa thử"\n2. Mở lại màn hình', 'Ghi chú khóa thử (đang Khóa, chưa dùng)',
             '- Hệ thống từ chối, báo "%s"\n- "Ghi chú khóa thử" vẫn còn, vẫn Khóa' % MSG_LOCKED),
        ]},
        # VI. XUẤT EXCEL (R70..R82, case cuối TC_06.013) — cột Trạng thái trong file
        {'after': 82, 'merge_from': 70, 'cases': [
            ('TC_06.014', 'Cột Trạng thái trong file Excel', 'P1', _PRE,
             '1. Bấm Xuất Excel, giữ nguyên các trường tích sẵn\n2. Bấm Xuất file, mở file', '',
             '- File có cột Trạng thái\n- Ghi chú đang Hoạt động ghi "Hoạt động", ghi chú đang Khóa ghi "Khóa", khớp với bảng'),
            ('TC_06.015', 'Xuất Excel theo bộ lọc Trạng thái', 'P1', _PRE,
             '1. Chọn Trạng thái = Khóa\n2. ' + _XF + '\n3. Mở file', 'Trạng thái: Khóa',
             '- File chỉ chứa các ghi chú đang Khóa, số dòng bằng tổng dưới bảng'),
        ]},
        # Khóa / Mở khóa chưa có case → nhóm MỚI sau case cuối của tab (TC_09.024, R129)
        {'after': 129,
         'groups': [('X', 'KHÓA / MỞ KHÓA (bổ sung 28/09/2026)', 10, [
             ('Hộp xác nhận Khóa nêu đúng Hạng mục', 'P0', _PRE,
              '1. Ở cột Hành động của "Ghi chú thử" bấm nút ba chấm "Hành động khác", chọn Khóa\n2. Đọc hộp xác nhận', '',
              '- Dòng "Ghi chú thử" có Sửa, Xóa hiện thẳng; Khóa và Lịch sử nằm trong nút ba chấm\n- Hộp tiêu đề "Khóa ghi chú kiểm tra", câu "Bạn có chắc muốn khóa ghi chú "Ghi chú thử"?"\n- Có hai nút Khóa và Hủy'),
             ('Khóa thành công', 'P0', 'Đang mở hộp xác nhận Khóa của "Ghi chú thử".',
              '1. Bấm Khóa\n2. Quan sát dòng "Ghi chú thử"', '',
              '- Báo "Khóa thành công"\n- Cột Trạng thái đổi thành Khóa\n- Dòng chỉ còn Mở khóa và Lịch sử (không còn Sửa, Xóa)'),
             ('Bấm Hủy thì không khóa', 'P1', 'Đang mở hộp xác nhận Khóa của "Ghi chú thử".',
              '1. Bấm Hủy\n2. Xem lại dòng "Ghi chú thử"', '',
              '- Hộp đóng, "Ghi chú thử" vẫn Hoạt động, các nút giữ nguyên'),
             ('Khóa được ghi chú đang được sử dụng', 'P0', _PRE,
              '1. Chọn Khóa ở dòng "Kiểm tra ngoại quan không tháo lắp"\n2. Bấm Khóa\n3. Mở Sửa một gói bảo dưỡng đang dùng ghi chú KTBM', '',
              '- Khóa thành công, KHÔNG bị chặn vì đang được sử dụng\n- Gói cũ vẫn hiển thị ghi chú KTBM kèm biểu tượng ổ khóa, không bị trống'),
             ('Mở khóa thành công', 'P0', '"Ghi chú khóa thử" đang Khóa, chưa dùng ở đâu.',
              '1. Chọn Mở khóa ở dòng "Ghi chú khóa thử"\n2. Đọc hộp xác nhận rồi bấm Mở khóa', '',
              '- Hộp tiêu đề "Mở khóa ghi chú kiểm tra", câu "Bạn có chắc muốn mở khóa ghi chú "Ghi chú khóa thử"?"\n- Báo "Mở khóa thành công", cột Trạng thái đổi thành Hoạt động\n- Nút Sửa và Xóa hiện lại'),
             ('Mở khóa ghi chú đang được sử dụng', 'P1', '"Kiểm tra ngoại quan không tháo lắp" đang Khóa và đang được gắn vào gói dịch vụ.',
              '1. Mở khóa ghi chú đó\n2. Quan sát cột Hành động', '',
              '- Ghi chú về Hoạt động\n- Có Sửa, Khóa và Lịch sử, KHÔNG có nút Xóa'),
             ('Ghi chú đang Khóa không sửa, không xóa được trên giao diện', 'P0', _PRE,
              '1. Tìm dòng "Ghi chú khóa thử", quan sát cột Hành động\n2. Bấm vào Hạng mục "Ghi chú khóa thử"', '',
              '- Không có bút chì và thùng rác, chỉ có Mở khóa và Lịch sử\n- Cửa sổ "Xem ghi chú kiểm tra" vẫn mở được, ô Trạng thái hiện Khóa ở chế độ chỉ đọc'),
             ('Chặn sửa ghi chú đang Khóa khi bỏ qua giao diện', 'P1', _PRE,
              '1. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa "Ghi chú khóa thử"\n2. Mở lại màn hình', 'Đổi Hạng mục thành "Bị sửa khi khóa"',
              '- Hệ thống từ chối, báo "%s"\n- Nội dung cũ giữ nguyên' % MSG_LOCKED),
             ('Hai người cùng khóa một ghi chú', 'P1', 'Tài khoản A và B cùng mở danh sách; "Ghi chú thử" đang Hoạt động.',
              '1. A khóa "Ghi chú thử" thành công\n2. B (chưa tải lại trang) chọn Khóa ở dòng "Ghi chú thử", bấm Khóa', '',
              '- B nhận thông báo "%s"\n- Lịch sử của "Ghi chú thử" chỉ có MỘT mốc Khóa' % MSG_CONFLICT),
             ('Khóa / Mở khóa được ghi lịch sử', 'P0', 'Vừa khóa rồi mở khóa "Ghi chú thử".',
              '1. Mở Lịch sử của "Ghi chú thử"\n2. Đọc 2 dòng trên cùng', '',
              '- Có 2 mốc loại Thay đổi trạng thái: Hoạt động → Khóa và Khóa → Hoạt động\n- Kèm tên người thực hiện và thời điểm'),
             ('Ghi chú đã Khóa không chọn được ở gói bảo dưỡng mới', 'P0', _PRE,
              '1. Mở màn Danh mục gói bảo dưỡng, bấm Tạo mới\n2. Ở phần cấp bảo dưỡng, mở ô chọn ghi chú kiểm tra', '',
              '- Danh sách chọn KHÔNG có ký hiệu của "Ghi chú khóa thử"\n- Các ghi chú đang Hoạt động vẫn chọn được'),
             ('Import gói bảo dưỡng dùng ghi chú đã Khóa', 'P1', '"Ghi chú khóa thử" đang Khóa.',
              '1. Ở màn Danh mục gói bảo dưỡng, Import file gói có cột Ghi chú kiểm tra = "Ghi chú khóa thử"\n2. Bấm Validate', 'Ghi chú kiểm tra: Ghi chú khóa thử',
              '- Dòng đó báo "Ghi chú kiểm tra "Ghi chú khóa thử" không có trong danh mục hoặc đã bị khóa"'),
             ('Người chỉ có quyền Xem không thấy Khóa / Mở khóa', 'P0', 'Đăng nhập bằng tài khoản chỉ có quyền "Xem ghi chú kiểm tra bảo dưỡng".',
              '1. Mở màn hình, quan sát cột Hành động ở một dòng Hoạt động và một dòng Khóa', '',
              '- Cả hai dòng chỉ có nút Lịch sử; không có Khóa, Mở khóa, Sửa, Xóa\n- Vẫn thấy cột Trạng thái và lọc được theo Trạng thái'),
         ])]},
    ],
    'import_rows_dung': 'File mẫu điền 3 ghi chú hợp lệ, chưa có trong danh mục (Hạng mục có tiền tố DOC-, Ký hiệu DOC1, DOC2, DOC3). Đăng nhập bằng tài khoản có quyền "Quản lý ghi chú kiểm tra bảo dưỡng"',
    'import_loi_data': {
        'Hạng mục không được để trống': 'Hạng mục: (để trống); Ký hiệu: DOC4',
        'Hạng mục tối đa 255 ký tự': 'Hạng mục: chuỗi 256 ký tự',
        'Hạng mục bị trùng với dòng N trong file': 'Hai dòng cùng Hạng mục “DOC-Kiểm tra độ căng dây curoa”',
        'Hạng mục đã tồn tại trong hệ thống': 'Hạng mục: Kiểm tra ngoại quan không tháo lắp',
        'Ký hiệu không được để trống': 'Hạng mục: DOC-Kiểm tra mức dầu; Ký hiệu: (để trống)',
        'Ký hiệu tối đa 255 ký tự': 'Ký hiệu: chuỗi 256 ký tự',
        'Ký hiệu bị trùng với dòng N trong file': 'Dòng 1 Ký hiệu “DOC1”, dòng khác Ký hiệu “doc1”',
        'Ký hiệu đã tồn tại trong hệ thống': 'Ký hiệu: ktbm (danh mục đã có KTBM)',
        'Mô tả tối đa 255 ký tự': 'Mô tả: chuỗi 256 ký tự',
    },
    'import_extra': [
        ('Người chỉ có quyền Xem không thấy nút Import Excel', 'P0', 'Đăng nhập bằng tài khoản chỉ có quyền "Xem ghi chú kiểm tra bảo dưỡng".',
         '1. Mở màn hình\n2. Quan sát thanh công cụ', '', '- KHÔNG có nút Import Excel (và không có nút Tạo mới)\n- Vẫn có nút Xuất Excel'),
        ('Ký hiệu trong file được chuyển chữ in hoa', 'P1', 'Đã Load file hợp lệ có dòng Ký hiệu viết thường “doc2”.',
         '1. Bấm Validate → Import\n2. Bật cột Ký hiệu, tìm ghi chú vừa nhập', 'Ký hiệu: doc2', '- Ghi chú được tạo với Ký hiệu “DOC2”'),
    ],
    'edits': [
        # --- Khối mô tả tính năng
        ('B3', '- Toàn bộ ghi chú kiểm tra trong danh mục, gồm CẢ ghi chú đang Hoạt động lẫn đang Khóa, KHÔNG phân theo công ty / phòng ban.\n- Bảng mặc định gồm 6 cột: STT, Hạng mục, Người tạo, Ngày tạo, Trạng thái, Hành động (Ký hiệu, Mô tả, Người cập nhật, Ngày cập nhật mặc định ẩn, bật ở Cấu hình cột).\n- Danh mục hiện có khoảng 11 ghi chú.'),
        ('B4', '- Không có ghi chú nào bị ẩn: danh sách hiện CẢ ghi chú Hoạt động lẫn ghi chú Khóa; ô Trạng thái để trống là xem cả hai.\n- Khi tìm kiếm hoặc chọn Trạng thái, các ghi chú không khớp bị loại khỏi kết quả.\n- Ghi chú đang Khóa không còn chọn được ở gói bảo dưỡng mới và khi Import gói bảo dưỡng; gói cũ đang dùng vẫn hiện đúng ký hiệu kèm biểu tượng ổ khóa.'),
        ('B6', 'Danh sách phẳng, không phân cấp cha- con.\n Cả Hạng mục và Ký hiệu đều là giá trị duy nhất trong danh mục (kể cả ghi chú đang Khóa).\n Quan hệ với màn khác: ghi chú được chọn làm nội dung kiểm tra trong cấp bảo dưỡng của gói bảo dưỡng. Được chọn ở ít nhất 1 gói thì coi là "đã sử dụng" — đây là căn cứ chặn XÓA (Khóa thì vẫn được).'),
        ('B8', 'Hai quyền dành riêng cho màn này:\n- "Xem ghi chú kiểm tra bảo dưỡng": vào màn hình, xem danh sách, tìm kiếm, lọc, mở xem chi tiết, xem lịch sử, xuất Excel.\n- "Quản lý ghi chú kiểm tra bảo dưỡng": thêm mới, sửa, xóa, khóa, mở khóa, Import Excel.\n Không có quyền nào trong hai quyền trên thì không vào được màn hình.\n Danh mục KHÔNG phân quyền theo công ty / phòng ban / bộ phận.'),
        ('B10', '- Màn có trạng thái Hoạt động / Khóa (bổ sung 28/09/2026): ô Trạng thái trong cửa sổ Tạo/Sửa (mặc định Hoạt động), cột Trạng thái, ô lọc Trạng thái và thao tác Khóa / Mở khóa ở cột Hành động.\n- Xóa là xóa HẲN. Nút Xóa CHỈ hiện với ghi chú đang Hoạt động VÀ chưa được gắn vào cấp bảo dưỡng của gói dịch vụ nào; nút bị ẨN hẳn, không có nút mờ. Ghi chú đã sử dụng thì dùng Khóa.\n- Khóa được CẢ ghi chú đang được sử dụng. Ghi chú đang Khóa chỉ còn Mở khóa và Lịch sử; máy chủ cũng chặn sửa / xóa với câu "' + MSG_LOCKED + '"\n- Thông báo chặn xóa: "' + MSG_USED + '".\n  Ở hệ thống cũ, màn này KHÔNG chặn xóa gì cả, dù phần lớn ghi chú đang được sử dụng — xóa xong là các gói dịch vụ mất ghi chú. Bản mới đã chặn. Đây là nhóm bắt buộc kiểm kỹ.\n- Ở hệ thống cũ, thêm và sửa mở ra TRANG RIÊNG; bản mới đưa về cửa sổ nhỏ cho đồng bộ với các danh mục khác. Đây là thay đổi có chủ ý, không phải lỗi.\n- Cột Mô tả có thể dài, được xuống dòng trong ô, không cắt cụt.\n- Bộ lọc được ghi nhớ trong 10 phút; kiểm thử tìm kiếm nên bấm Làm mới trước mỗi kịch bản.'),
        # --- Phân quyền
        ('I20', '- Có nút Tạo mới, nút Xuất Excel và nút Import Excel\n- Dòng đang Hoạt động có Sửa, Khóa, Lịch sử; nút Xóa chỉ hiện ở ghi chú đang Hoạt động và chưa gắn vào gói dịch vụ (vd có ở "Ghi chú thử"). Dòng đủ 4 nút thì Khóa và Lịch sử nằm trong nút ba chấm\n- Dòng đang Khóa chỉ có Mở khóa và Lịch sử\n- Bấm vào Hạng mục để mở cửa sổ Xem'),
        # --- I. Hiển thị
        ('I24', '- Tiêu đề trang và tiêu đề bảng đều là "Danh mục ghi chú kiểm tra bảo dưỡng"\n- Khu vực lọc có ô tìm nhanh (gợi ý "Tìm theo hạng mục hoặc ký hiệu...") và ô Trạng thái\n- Bảng mặc định có 6 cột: STT, Hạng mục, Người tạo, Ngày tạo, Trạng thái, Hành động\n- Có nút Tạo mới, Xuất Excel, Import Excel và biểu tượng Cấu hình cột hiển thị'),
        ('D28', 'Cột Trạng thái hiển thị Hoạt động / Khóa'),
        ('G28', '1. Mở màn hình\n2. Nhìn cột Trạng thái của "Ghi chú thử" và "Ghi chú khóa thử"'),
        ('I28', '- Có cột Trạng thái dạng nhãn: "Ghi chú thử" hiện Hoạt động, "Ghi chú khóa thử" hiện Khóa\n- Danh sách hiện CẢ ghi chú đang Khóa, không ẩn đi'),
        # --- IV. Thêm / sửa / xem
        ('I49', '- Mở CỬA SỔ NHỎ tiêu đề "Tạo ghi chú kiểm tra", không phải trang riêng\n- Có 4 ô: Hạng mục (bắt buộc), Ký hiệu (bắt buộc), Mô tả, Trạng thái (mặc định Hoạt động, chọn Hoạt động / Khóa)\n- Hai ô bắt buộc có dấu sao đỏ bên cạnh nhãn\n- Cuối cửa sổ có 3 nút: Lưu, Lưu và tiếp tục, Đóng'),
        # --- V. Xóa
        ('I63', '- Hộp xác nhận tiêu đề "Xác nhận xóa", câu "Bạn có chắc muốn xóa ghi chú "Ghi chú thử"?"\n- Thông báo "Xóa thành công"\n- Dòng biến mất, tổng dưới bảng giảm 1; lọc Trạng thái = Khóa cũng KHÔNG thấy (xóa hẳn, không phải chuyển sang Khóa)'),
        ('D65', 'Ghi chú đang được sử dụng thì KHÔNG có nút Xóa'),
        ('G65', '1. Mở màn hình, tìm dòng "Kiểm tra ngoại quan không tháo lắp"\n2. Quan sát cột Hành động'),
        ('I65', '- KHÔNG có nút Xóa (biểu tượng thùng rác) — nút bị ẩn hẳn, không phải hiện mờ\n- Vẫn có Sửa, Khóa, Lịch sử\n  Hệ thống cũ KHÔNG chặn TH này — xóa xong là gói dịch vụ mất ghi chú. Bắt buộc phải kiểm'),
        ('G66', '1. Người 1 mở màn hình (dòng "Ghi chú thử" đang có nút Xóa)\n2. Người 2 gắn ghi chú đó vào cấp bảo dưỡng của một gói dịch vụ\n3. Người 1 (chưa tải lại trang) bấm Xóa và xác nhận'),
        ('I66', '- Hệ thống chặn lại, báo "' + MSG_USED + '"\n- Dòng vẫn còn; tải lại trang thì dòng đó không còn nút Xóa'),
        ('I68', '- Mỗi dòng chỉ có nút Lịch sử; KHÔNG có Sửa, Xóa, Khóa / Mở khóa'),
        # --- VI. Xuất Excel (thêm trường Trạng thái)
        ('I71', '- File có cột STT ở đầu, tiếp theo là đúng các cột đã tích theo thứ tự trong cửa sổ: Hạng mục, Người tạo, Ngày tạo, Trạng thái, Ký hiệu, Mô tả\n- Tiêu đề cột bằng tiếng Việt giống trên màn hình, dữ liệu khớp với bảng'),
        ('I76', '- Mở cửa sổ “Chọn trường xuất file”\n- Có đủ 8 trường: Hạng mục, Ký hiệu, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật\n- Tích sẵn đúng các cột đang hiển thị trên bảng, xếp lên đầu theo thứ tự trên bảng: Hạng mục, Người tạo, Ngày tạo, Trạng thái\n- Dòng cuối ghi “Đang chọn 4/8 trường”'),
        ('I79', '- Bỏ chọn hết: không trường nào được tích, nút Xuất file không bấm được\n- Chọn tất cả: tích đủ 8 trường, dòng cuối “Đang chọn 8/8 trường”'),
        ('I80', '- Trường Ký hiệu được tích sẵn cùng Hạng mục, Người tạo, Ngày tạo, Trạng thái (theo thứ tự cột trên bảng: Hạng mục, Ký hiệu, Người tạo, Ngày tạo, Trạng thái)'),
        # --- VIII. Luồng xuyên suốt
        ('G103', '1. Tạo mới ghi chú "Kiểm tra kiểm thử"\n2. Gắn ghi chú đó vào cấp bảo dưỡng của một gói dịch vụ\n3. Quay lại màn hình, tải lại danh sách, quan sát cột Hành động của ghi chú đó'),
        ('I103', '- Bước 3: KHÔNG còn nút Xóa (vẫn có Sửa, Khóa, Lịch sử)\n- Ghi chú vẫn còn trong danh mục; muốn ngừng dùng thì Khóa'),
        # --- IX. Import (bản ghi import ở trạng thái Hoạt động)
        ('I124', '- Báo “Import thành công N ghi chú kiểm tra bảo dưỡng.”\n- Cửa sổ đóng, danh sách tải lại có ghi chú kiểm tra mới ở trạng thái Hoạt động'),
    ],
    'clear_k': [20, 24, 28, 49, 63, 65, 66, 68, 71, 76, 79, 80, 103, 124],
}


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


_srs_ui_events(CFG, {
    'fr_sua': 'Chỉnh sửa ghi chú kiểm tra', 'fr_xoa': 'Xóa ghi chú kiểm tra', 'fr_khoa': 'Khóa / Mở khóa ghi chú kiểm tra',
    'fr_ls': 'Xem lịch sử thay đổi', 'fr_import': 'Import file ghi chú kiểm tra',
    'fr_xuat': 'Xuất danh sách ghi chú kiểm tra ra Excel', 'fr_xem': 'Xem chi tiết ghi chú kiểm tra', 'fr_cot': 'Tùy chỉnh cột hiển thị',
    'nhan_ban_ghi': 'hạng mục', 'nhan_cot': 'Hạng mục',
    'tieu_de_sua': 'Sửa ghi chú kiểm tra', 'tieu_de_xem': 'Xem ghi chú kiểm tra',
    'sua_hien': 'Chỉ hiện khi Người dùng có quyền Quản lý VÀ ghi chú đang Hoạt động.',
    'truong_sua': [
        ('Hạng mục', 'Textbox', '1–255 ký tự', 'Có',
         'Duy nhất trong danh mục, bỏ qua chính bản ghi đang sửa. Bỏ trống “Bắt buộc phải nhập”; trùng “Hạng mục đã tồn tại”; quá dài “Vui lòng nhập tối đa 255 ký tự.”'),
        ('Ký hiệu', 'Textbox', '1–255 ký tự', 'Có',
         'Tự cắt khoảng trắng đầu cuối và chuyển CHỮ IN HOA khi lưu; duy nhất trong danh mục (so sau khi in hoa). Bỏ trống báo “Bắt buộc phải nhập” sau khi bấm Lưu; trùng “Ký hiệu đã tồn tại”.'),
        ('Mô tả', 'Textbox', '0–255 ký tự', 'Không', 'Quá dài “Vui lòng nhập tối đa 255 ký tự.”'),
        ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Không',
         'Luôn có giá trị, không xóa trống được. Chọn Khóa rồi Lưu là khóa ghi chú ngay trong cửa sổ Sửa; lịch sử ghi mốc “Thay đổi trạng thái” riêng.'),
    ],
    'xoa_hien': 'Chỉ hiện khi Người dùng có quyền Quản lý, ghi chú đang Hoạt động VÀ chưa được sử dụng.',
    'xoa_tieu_de': 'Xác nhận xóa', 'xoa_cau': 'Bạn có chắc muốn xóa ghi chú "<hạng mục>"?',
    'khoa_hien': 'Chỉ hiện với quyền Quản lý. Ghi chú đang Hoạt động hiện “Khóa”, ghi chú đang Khóa hiện “Mở khóa” (khóa được cả ghi chú đang được sử dụng).',
    'khoa_tieu_de': '“Khóa ghi chú kiểm tra” hoặc “Mở khóa ghi chú kiểm tra” theo thao tác.',
    'khoa_cau': '“Bạn có chắc muốn khóa ghi chú "<hạng mục>"?” / “Bạn có chắc muốn mở khóa ghi chú "<hạng mục>"?”.',
    'truong_ls': 'Hạng mục, Ký hiệu, Mô tả, Trạng thái',
    'quyen_import': 'quyền Quản lý', 'import_tieu_de': 'Import ghi chú kiểm tra bảo dưỡng',
    'import_file': 'Mau_import_ghi_chu_kiem_tra_bao_duong.xlsx', 'import_cot': 'STT, Hạng mục, Ký hiệu, Mô tả',
    'import_cot_bang': 'STT, Hạng mục, Ký hiệu, Mô tả',
    'doi_tuong_import': 'ghi chú kiểm tra (Ký hiệu tự chuyển chữ in hoa)', 'import_toast': 'Import thành công N ghi chú kiểm tra bảo dưỡng.',
    'import_toast_loi': 'Import thành công x/y ghi chú kiểm tra bảo dưỡng. N dòng thất bại.',
    'xuat_hien': 'Hiện với cả người chỉ có quyền Xem.',
    'xuat_truong': 'Tám trường: Hạng mục, Ký hiệu, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật', 'xuat_so': 8,
    'xuat_theo': 'từ khóa, Trạng thái và thứ tự sắp xếp', 'xuat_file': 'danh_muc_ghi_chu_kiem_tra_bao_duong.xlsx',
    'truong_xem': [('Hạng mục', 'Textbox', 'Ô mờ, không gõ được.'),
                   ('Ký hiệu', 'Textbox', 'Ô mờ, hiển thị chữ in hoa đã lưu.'),
                   ('Mô tả', 'Textbox', 'Ô mờ; trống nếu chưa nhập.'),
                   ('Trạng thái', 'Dropdown', 'Hoạt động hoặc Khóa, không đổi được.')],
    'cot_all': ['STT', 'Hạng mục', 'Ký hiệu', 'Mô tả', 'Người tạo', 'Ngày tạo', 'Người cập nhật', 'Ngày cập nhật', 'Trạng thái', 'Hành động'],
    'cot_mac_dinh': 'STT, Hạng mục, Người tạo, Ngày tạo, Trạng thái, Hành động',
    'cot_khoa': 'STT, Hạng mục, Hành động',
})
