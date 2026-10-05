# -*- coding: utf-8 -*-
# Cấu hình tài liệu màn Cấp dịch vụ bảo dưỡng (phân hệ CSKH sau bán).
# Nguồn: code gop_db 25/09/2026 — FE pages/customer-care/levels/index.vue, components/modal/customer-care/level-modal.vue,
# utils/mixins/CatalogImportMixin.js; BE Modules/CustomerCare (LevelController, LevelService, LevelRequest, Level::USAGE_REFERENCES),
# App\ExcelExport\ExportColumnRegistry['levels'].
# Cập nhật 28/09/2026: cột status (Hoạt động / Khóa), Khóa / Mở khóa ở cột Hành động, bộ lọc Trạng thái, xóa hẳn khi
#   đang Hoạt động + chưa dùng, middleware recordNotLocked chặn sửa/xóa cấp đang Khóa (423); ServiceImportService /
#   ServiceService::optionsData / WrServiceQuotationService chỉ lấy cấp đang Hoạt động.
# Không ghi URL. Chữ UI / message lấy nguyên văn code.

DT = 'cấp dịch vụ'
Q_XEM = 'Xem cấp dịch vụ bảo dưỡng'
Q_QL = 'Quản lý cấp dịch vụ bảo dưỡng'
MSG_USED = 'Cấp dịch vụ bảo dưỡng đang được sử dụng, không thể xóa.'
MSG_LOCKED = 'Bản ghi đang bị khoá, vui lòng mở khoá trước khi cập nhật.'
MSG_CONFLICT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'
# Nơi được coi là "đã sử dụng" (Level::USAGE_REFERENCES, ghi bằng tên nghiệp vụ)
USED_L = ('Gói bảo dưỡng (cấp của gói), Cấp bảo dưỡng của gói dịch vụ (bảng nội dung kiểm tra theo cấp), Báo giá dịch vụ, '
          'Hợp đồng dịch vụ, Phiếu phân công công việc, Phiếu nhập kết quả dịch vụ')

CFG = {
    'slug': 'levels',
    'ten': 'Cấp dịch vụ bảo dưỡng',
    'doi_tuong': DT,
    'file_hdsd': 'HDSD_Cap dich vu bao duong.docx',
    'file_srs': 'SRS - Cấp dịch vụ bảo dưỡng.docx',
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Cấp dịch vụ bảo dưỡng', 'menu_muc')],

    'thuat_ngu': [
        ['Cấp dịch vụ bảo dưỡng', 'Mức phân loại công việc bảo dưỡng theo mốc thời gian hoặc số giờ vận hành của thiết bị, ví dụ “Cấp 1 (6T)”, “Cấp 2 (12T)”, “Cấp 1 (12T/2500h)”.'],
        ['Tên cấp', 'Tên của cấp dịch vụ, là trường nghiệp vụ duy nhất của danh mục và không được trùng trên toàn danh mục.'],
        ['Trạng thái Hoạt động', 'Cấp dịch vụ còn chọn được khi lập gói bảo dưỡng mới và khi chọn gói trong báo giá dịch vụ.'],
        ['Trạng thái Khóa', 'Cấp dịch vụ ngừng dùng: không còn chọn được ở chứng từ mới, không sửa và không xóa được cho tới khi Mở khóa; vẫn nằm trong danh mục, vẫn xem được chi tiết và lịch sử, các chứng từ cũ đang dùng vẫn hiển thị đúng tên kèm biểu tượng 🔒.'],
        ['Cấp đang được sử dụng', 'Cấp đã xuất hiện ở ít nhất một nơi: ' + USED_L + '. Cấp đang được sử dụng thì không xóa được (vẫn Khóa được).'],
        ['Quyền Xem', '“%s” — vào màn hình, xem danh sách, xem chi tiết, xuất Excel.' % Q_XEM],
        ['Quyền Quản lý', '“%s” — ngoài quyền Xem còn được Tạo mới, Sửa, Xóa, Khóa, Mở khóa và Import Excel.' % Q_QL],
    ],
    'phien_ban': [
        ['1.0', '13/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Cấp dịch vụ bảo dưỡng.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: bấm tên để Xem chi tiết (bỏ nút Xem), bổ sung cột Người tạo/Ngày tạo/Người cập nhật, Lịch sử thay đổi, cửa sổ Chọn trường xuất file, Import Excel, Tùy chỉnh cột; trình bày theo mẫu tài liệu danh mục chung.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bổ sung trạng thái Hoạt động / Khóa: ô Trạng thái trong cửa sổ Tạo/Sửa (mặc định Hoạt động), cột Trạng thái và bộ lọc Trạng thái ở danh sách, cột Trạng thái trong file Xuất Excel, chức năng Khóa / Mở khóa ở cột Hành động (khóa được cả cấp đang được sử dụng). Cấp đang Khóa ẩn nút Sửa, Xóa và bị máy chủ chặn cập nhật; cấp đã khóa không còn chọn được ở gói bảo dưỡng mới, Import gói bảo dưỡng và danh sách chọn gói trong báo giá dịch vụ. Xóa là xóa hẳn, chỉ khi cấp đang Hoạt động và chưa được sử dụng; bỏ bước hỏi máy chủ trước khi mở hộp xác nhận xóa và đổi câu thông báo chặn xóa.'],
    ],
    'muc_dich': [
        'Màn hình Cấp dịch vụ bảo dưỡng dùng để khai báo danh sách các cấp bảo dưỡng như “Cấp 1 (6T)”, “Cấp 2 (12T)”, “Cấp 2 (24T/6000H)”… Cấp dịch vụ là mức phân loại công việc bảo dưỡng theo mốc thời gian hoặc số giờ vận hành của thiết bị.',
        'Danh mục được dùng lại ở gói bảo dưỡng, cấp bảo dưỡng của gói dịch vụ, báo giá dịch vụ, hợp đồng dịch vụ, phiếu phân công công việc và phiếu nhập kết quả dịch vụ. Vì vậy một cấp đã được dùng ở bất kỳ nơi nào trong số đó sẽ không xóa được; muốn ngừng dùng thì Khóa.',
        'Mỗi cấp có trạng thái Hoạt động hoặc Khóa. Cấp đã khóa không còn chọn được ở chứng từ mới nhưng các chứng từ cũ vẫn giữ nguyên. Danh mục dùng chung cho toàn hệ thống, không phân theo công ty / phòng ban.',
    ],
    'quyen': {
        'truoc': ['Màn hình dùng 2 quyền riêng. Mục menu chỉ hiện khi tài khoản có ít nhất một trong hai quyền; không có quyền nào thì không vào được màn hình.'],
        'rows': [
            [Q_XEM, 'Vào màn hình, xem danh sách, tìm kiếm, lọc, xem chi tiết (bấm vào tên cấp), xem lịch sử, xuất Excel.'],
            [Q_QL, 'Toàn bộ quyền Xem, cộng thêm: Tạo mới, Sửa, Xóa, Khóa, Mở khóa, Import Excel.'],
        ],
        'sau': ['Nút nào Người dùng không có quyền dùng thì hệ thống ẩn hẳn, không hiện nút mờ. Máy chủ cũng kiểm tra quyền, nên gọi thẳng chức năng mà bỏ qua giao diện vẫn bị từ chối.'],
    },

    'danh_sach': {
        'mo_ta_vao': 'Hệ thống hiển thị danh sách cấp dịch vụ hiện có, mặc định 10 dòng mỗi trang, xếp theo thứ tự tạo.',
        'bo_cuc': [
            'Khu vực tìm kiếm và lọc — ô tìm kiếm nhanh, ô Trạng thái, nút Tìm kiếm và Làm mới. Màn hình chỉ có hai tiêu chí nên không có Tìm kiếm nâng cao.',
            'Thanh công cụ — nút Tạo mới, nút Xuất Excel, nút Import Excel và biểu tượng Cấu hình cột hiển thị.',
            'Bảng danh sách — các cột thông tin, cột Hành động ở cuối, và phân trang bên dưới.',
        ],
        'cot': [
            ['STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'],
            ['Tên cấp', 'Tên cấp dịch vụ. Luôn hiển thị, sắp xếp được. Bấm vào tên để mở cửa sổ Xem cấp dịch vụ.'],
            ['Người tạo', 'Người đã thêm bản ghi.'],
            ['Ngày tạo', 'Thời điểm thêm, dạng dd/mm/yyyy hh:mm, sắp xếp được.'],
            ['Người cập nhật', 'Người sửa bản ghi gần nhất. Mặc định ẩn.'],
            ['Ngày cập nhật', 'Thời điểm sửa gần nhất, dạng dd/mm/yyyy hh:mm. Mặc định ẩn, sắp xếp được.'],
            ['Trạng thái', 'Nhãn Hoạt động hoặc Khóa. Danh sách hiện cả cấp đang Hoạt động lẫn đang Khóa.'],
            ['Hành động', 'Các nút thao tác của dòng (xem mục 4).'],
        ],
        'hanh_dong': {
            'intro': 'Trên mỗi dòng, cột Hành động có các nút:',
            'bullets': [
                'Biểu tượng bút chì {icon:btn_sua} — mở cửa sổ Sửa cấp dịch vụ. Chỉ hiện khi Người dùng có quyền Quản lý VÀ cấp đang Hoạt động.',
                'Biểu tượng thùng rác {icon:btn_xoa} — xóa hẳn cấp dịch vụ. Chỉ hiện khi Người dùng có quyền Quản lý, cấp đang Hoạt động VÀ CHƯA được sử dụng ở đâu.',
                'Khóa / Mở khóa — đổi trạng thái cấp dịch vụ. Chỉ hiện khi Người dùng có quyền Quản lý; cấp đang Hoạt động hiện Khóa, cấp đang Khóa hiện Mở khóa.',
                'Lịch sử — mở cửa sổ Lịch sử thay đổi. Luôn hiện, không cần quyền riêng.',
                'Dòng có từ 4 nút trở lên thì 2 nút đầu (Sửa, Xóa) hiện thẳng, các nút còn lại (Khóa, Lịch sử) nằm trong nút ba chấm {icon:btn_bacham} “Hành động khác”.',
            ],
            'anh': 'Các nút ở cột Hành động của một cấp dịch vụ',
            'luu_y': ['Lưu ý: màn hình KHÔNG có nút Xem — muốn xem chi tiết thì bấm thẳng vào tên cấp. Không thấy nút thùng rác nghĩa là cấp đó đang được sử dụng, đang Khóa, hoặc Người dùng chỉ có quyền Xem. Với cấp ĐÃ KHÓA, nút Sửa và Xóa sẽ BIẾN MẤT, chỉ còn Mở khóa và Lịch sử; muốn sửa lại phải Mở khóa trước.'],
        },
        'phan_trang': [
            'Cuối bảng có dòng “Hiển thị a–b / N”: N là tổng số cấp dịch vụ khớp điều kiện tìm kiếm đang áp dụng, không phải tổng toàn danh mục.',
            'Ô Số dòng/trang có các mức 5, 10, 20, 50, 100 (mặc định 10). Đổi số dòng thì hệ thống tự quay về trang 1.',
            'Các cột sắp xếp được: Tên cấp, Ngày tạo, Ngày cập nhật. Bấm tiêu đề cột để sắp xếp, bấm lần hai để đảo chiều. Thứ tự sắp xếp được giữ nguyên khi chuyển trang.',
        ],
    },

    'loc': {
        'buoc2': 'Bước 2: Nhập một phần tên cấp vào ô tìm kiếm nhanh rồi nhấn Enter hoặc bấm {icon:btn_timkiem}, và/hoặc chọn giá trị ở ô Trạng thái.',
        'rows': [
            ['Ô tìm kiếm nhanh', 'Placeholder “Tìm theo tên cấp dịch vụ...”. Tìm theo TÊN cấp, gõ một phần tên cũng ra (gõ “6T” vẫn ra “Cấp 1 (6T)”), không phân biệt chữ hoa chữ thường. Phải nhấn Enter hoặc bấm Tìm kiếm thì danh sách mới lọc.'],
            ['Trạng thái', 'Hoạt động hoặc Khóa. Bỏ trống thì hiện cả hai trạng thái (xóa lựa chọn bằng dấu x trong ô). Lọc ngay khi chọn, không cần bấm Tìm kiếm.'],
        ],
        'ap_dung': [
            'Các tiêu chí kết hợp với nhau theo kiểu VÀ — chỉ cấp thỏa đồng thời từ khóa và Trạng thái mới hiện ra. Mỗi lần đổi tiêu chí, danh sách quay về trang 1. Điều kiện tìm kiếm được ghi nhớ trong 10 phút khi quay lại màn hình.',
            'Bấm {icon:btn_lammoi} để xóa toàn bộ tiêu chí (từ khóa và Trạng thái); danh sách nạp lại đầy đủ ngay lập tức.',
        ],
        'anh_ket_qua': 'Kết quả tìm nhanh theo tên cấp (gõ “Cấp 1”)',
    },

    'form': {
        'kieu': 'popup',
        'buoc_tao': [
            'Bước 1: Truy cập vào màn hình Cấp dịch vụ bảo dưỡng (cần quyền Quản lý).',
            'Bước 2: Bấm {icon:btn_taomoi}. Hệ thống mở cửa sổ “Tạo cấp dịch vụ”.',
            'Bước 3: Nhập Tên cấp; giữ Trạng thái là Hoạt động (hoặc chọn Khóa nếu muốn tạo sẵn ở trạng thái ngừng dùng).',
            'Bước 4: Bấm {icon:btn_luu} để lưu và đóng cửa sổ, hoặc {icon:btn_luutieptuc} để lưu rồi nhập tiếp cấp khác.',
        ],
        'anh_tao': 'Cửa sổ Tạo cấp dịch vụ',
        'truong': [
            ['Tên cấp', 'Ô nhập giá trị', 'Có', 'Trống', 'Gợi ý trong ô “VD: Cấp 1 (6T)”. Tối đa 255 ký tự, duy nhất trên toàn danh mục (tính cả cấp đang Khóa). Khoảng trắng thừa ở đầu và cuối được tự cắt bỏ trước khi kiểm tra trùng. Bỏ trống báo “Bắt buộc phải nhập”; trùng báo “Tên cấp đã tồn tại”.'],
            ['Trạng thái', 'Ô chọn giá trị', 'Không (luôn có giá trị)', 'Hoạt động', 'Chỉ chọn 1 trong 2 giá trị: Hoạt động / Khóa; không xóa trống được. Chọn Khóa thì cấp không còn chọn được ở chứng từ mới.'],
        ],
        'nut': [
            ['Lưu', 'Ghi bản ghi rồi đóng cửa sổ, báo “Thêm mới thành công” (hoặc “Cập nhật thành công” khi sửa) và nạp lại danh sách.'],
            ['Lưu và tiếp tục', 'Ghi bản ghi nhưng GIỮ cửa sổ mở và xóa trắng ô để nhập tiếp. Chỉ có khi Tạo mới.'],
            ['Đóng', 'Đóng cửa sổ, không ghi gì. Nếu đã nhập dở, hệ thống hỏi “Thông tin chưa lưu” — “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại).'],
        ],
        'loi': [
            ['Bắt buộc phải nhập', 'Chưa nhập Tên cấp, hoặc chỉ nhập toàn khoảng trắng.'],
            ['Tên cấp đã tồn tại', 'Đã có cấp dịch vụ khác cùng tên trong danh mục. Hãy kiểm tra lại danh sách trước khi thêm.'],
            ['Vui lòng nhập tối đa 255 ký tự.', 'Tên cấp quá dài.'],
            ['Bạn chưa nhập đầy đủ thông tin', 'Thông báo chung khi còn ô bị lỗi; xem ô báo đỏ trong cửa sổ.'],
        ],
    },

    'sua': {
        'buoc': [
            'Bước 1: Truy cập vào màn hình Cấp dịch vụ bảo dưỡng (cần quyền Quản lý).',
            'Bước 2: Bấm nút {icon:btn_sua} ở cột Hành động của cấp cần sửa (chỉ có ở cấp đang Hoạt động).',
            'Bước 3: Hệ thống hiển thị cửa sổ “Sửa cấp dịch vụ” với Tên cấp và Trạng thái hiện tại.',
            'Bước 4: Sửa Tên cấp và/hoặc Trạng thái (quy tắc nhập như Thêm mới).',
            'Bước 5: Bấm {icon:btn_luu} để xác nhận thay đổi hoặc Đóng nếu muốn hủy. Cửa sổ Sửa không có nút Lưu và tiếp tục.',
        ],
        'anh': 'Cửa sổ Sửa cấp dịch vụ',
        'ghi_chu': [
            'Giữ nguyên tên của chính cấp đang sửa thì không bị báo trùng.',
            'Cấp dịch vụ đang được sử dụng VẪN sửa được; các chứng từ đang dùng cấp này sẽ hiển thị tên mới. Việc đang được sử dụng chỉ chặn thao tác Xóa.',
            'Cấp đang Khóa không có nút Sửa. Nếu cấp vừa bị người khác khóa trong lúc Người dùng đang mở cửa sổ Sửa, bấm Lưu sẽ nhận thông báo “%s”, thay đổi không được ghi.' % MSG_LOCKED,
            'Chọn Trạng thái = Khóa rồi Lưu là cách khóa ngay trong cửa sổ Sửa; lịch sử ghi thành một mốc Thay đổi trạng thái riêng.',
        ],
    },
    'xoa': {
        'buoc': [
            'Bước 1: Ở cột Hành động, Người dùng bấm {icon:btn_xoa}.',
            'Bước 2: Hệ thống hiện hộp “Xác nhận xóa” — “Bạn có chắc muốn xóa cấp dịch vụ "…"?”. Bấm {icon:btn_confirm_xoa} để xác nhận: hệ thống báo “Xóa thành công”, bản ghi biến mất khỏi danh sách.',
            'Bấm {icon:btn_huy} nếu bấm nhầm. Không có gì thay đổi.',
        ],
        'anh': 'Hộp xác nhận xóa cấp dịch vụ',
        'ghi_chu': [
            'Xóa là xóa HẲN cấp dịch vụ khỏi danh mục (không phải chuyển sang Khóa). Nút Xóa chỉ hiện khi cấp đang Hoạt động VÀ CHƯA được sử dụng ở đâu.',
            'Cấp được coi là “đã sử dụng” khi đã xuất hiện ở ít nhất một nơi: ' + USED_L + '. Cấp đã được sử dụng thì dùng Khóa thay cho Xóa.',
            'Nếu cấp vừa được đưa vào chứng từ trong lúc Người dùng đang mở danh sách, bấm Xóa trong hộp xác nhận sẽ nhận thông báo “%s”; vừa bị người khác khóa thì nhận “%s”. Bản ghi không bị xóa.' % (MSG_USED, MSG_LOCKED),
            'Xóa là thao tác không lùi lại được; lịch sử của bản ghi đã xóa không còn xem được trên màn hình.',
        ],
    },
    'khoa': {
        'y_nghia': [
            'Cấp dịch vụ VẪN nằm trong danh sách, cột Trạng thái hiện chữ Khóa; vẫn xem chi tiết và xem lịch sử thay đổi được.',
            'Cấp đã khóa không còn chọn được ở chứng từ mới: ô chọn cấp khi Tạo mới gói bảo dưỡng, file Import gói bảo dưỡng (báo “Cấp bảo dưỡng "…" không có trong danh mục hoặc đã bị khóa”) và danh sách chọn gói bảo dưỡng trong Báo giá dịch vụ.',
            'Gói bảo dưỡng và các chứng từ cũ đang dùng cấp đó giữ nguyên; mở Sửa gói cũ vẫn thấy đúng tên cấp kèm biểu tượng 🔒.',
            'Nút Sửa và Xóa của dòng đó biến mất. Muốn sửa hoặc xóa, Người dùng phải Mở khóa trước.',
            'Khóa được cả cấp đang được sử dụng — đây là cách ngừng dùng một cấp không xóa được.',
        ],
        'buoc_khoa': [
            'Bước 1: Ở cột Hành động của cấp đang Hoạt động, Người dùng chọn Khóa (trong nút ba chấm {icon:btn_bacham} “Hành động khác” nếu dòng có đủ 4 nút).',
            'Bước 2: Hệ thống hiện hộp xác nhận “Khóa cấp dịch vụ” — “Bạn có chắc muốn khóa cấp dịch vụ "…"?”. Bấm Khóa để xác nhận; hệ thống báo “Khóa thành công”, cột Trạng thái đổi thành Khóa. Bấm Hủy nếu bấm nhầm.',
        ],
        'buoc_mo': [
            'Bước 1: Ở cột Hành động của cấp đang Khóa, Người dùng chọn Mở khóa.',
            'Bước 2: Bấm Mở khóa trong hộp xác nhận “Mở khóa cấp dịch vụ” — “Bạn có chắc muốn mở khóa cấp dịch vụ "…"?”. Hệ thống báo “Mở khóa thành công”, cột Trạng thái đổi thành Hoạt động, nút Sửa (và Xóa nếu cấp chưa được sử dụng) hiện lại. Bấm Hủy nếu bấm nhầm.',
        ],
        'ghi_chu': [
            'Chỉ người có quyền Quản lý mới thấy Khóa / Mở khóa.',
            'Có thể khóa ngay trong cửa sổ Sửa bằng cách chọn Trạng thái = Khóa rồi Lưu.',
            'Nếu cấp vừa bị người khác đổi trạng thái, hệ thống báo “%s” và không ghi thêm mốc lịch sử trùng.' % MSG_CONFLICT,
        ],
    },
    'lich_su': {
        'buoc': [
            'Xem từ màn danh sách: ở cột Hành động, Người dùng chọn Lịch sử. Hệ thống mở cửa sổ “Lịch sử thay đổi: <tên cấp>”.',
            'Xem từ màn chi tiết: bấm vào tên cấp để mở cửa sổ Xem cấp dịch vụ, khối Lịch sử nằm ở cuối cửa sổ.',
        ],
        'ghi_chu': [
            'Khóa / Mở khóa (từ cột Hành động hoặc đổi Trạng thái trong cửa sổ Sửa) được ghi thành mốc riêng loại Thay đổi trạng thái.',
            'Cửa sổ có bộ lọc riêng (loại hành động, người thực hiện, khoảng thời gian) để thu hẹp danh sách khi bản ghi có nhiều lần thay đổi. Cấp chưa từng sửa chỉ có mốc Tạo mới (cấp tạo từ trước khi có chức năng lịch sử thì hiện “Chưa có lịch sử thao tác nào.”).',
        ],
    },
    'chi_tiet': {
        'buoc': ['Bước 1: Truy cập vào màn hình Cấp dịch vụ bảo dưỡng.',
                 'Bước 2: Bấm vào tên cấp ở cột Tên cấp. Hệ thống mở cửa sổ “Xem cấp dịch vụ”.'],
        'ghi_chu': ['Cửa sổ hiển thị Tên cấp và Trạng thái ở chế độ chỉ đọc (không gõ được, không có nút Lưu, chỉ có nút Đóng), kèm khối Lịch sử ở cuối. Người chỉ có quyền Xem cũng mở được; cấp đang Khóa vẫn xem được bình thường.'],
    },
    'xuat': {
        'buoc': [
            'Bước 1: Tìm kiếm, lọc đúng dữ liệu cần lấy (xem PHẦN 2). File xuất ra chạy theo đúng từ khóa, Trạng thái và thứ tự sắp xếp đang áp dụng.',
            'Bước 2: Bấm nút {icon:btn_xuatexcel}. Hệ thống mở cửa sổ “Chọn trường xuất file”.',
            'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất. Mặc định hệ thống tích sẵn đúng những cột đang hiển thị trên bảng, theo thứ tự trên bảng (ban đầu là Tên cấp, Người tạo, Ngày tạo, Trạng thái).',
            'Bước 4: Bấm {icon:btn_xuatfile}. Hệ thống tải về file cap_dich_vu_bao_duong.xlsx và báo “Xuất Excel thành công”.',
        ],
        'truong': 'Chọn nhiều trường: Tên cấp, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật.',
        'ghi_chu': [
            'Lưu ý: file xuất chứa TOÀN BỘ kết quả tìm kiếm (tối đa 10,000 dòng), không chỉ các dòng của trang đang xem. Cột STT luôn đứng đầu file; các cột còn lại theo đúng thứ tự trường đã chọn. Cột Trạng thái ghi chữ Hoạt động hoặc Khóa.',
            'Người chỉ có quyền Xem vẫn xuất Excel được.',
        ],
    },
    'import': {
        'tieu_de': 'Import cấp dịch vụ bảo dưỡng',
        'file': 'Mau_import_cap_dich_vu_bao_duong.xlsx',
        'cot_text': 'STT, Tên cấp (bắt buộc)',
        'toast': 'Import thành công N cấp dịch vụ bảo dưỡng.',
        'loi': [
            ['Tên cấp không được để trống', 'Dòng đó bỏ trống cột Tên cấp.'],
            ['Tên cấp tối đa 255 ký tự', 'Tên quá dài, rút gọn lại.'],
            ['Tên cấp bị trùng với dòng N trong file', 'Trong chính file có hai dòng cùng tên (không phân biệt hoa thường). Xóa bớt một dòng.'],
            ['Tên cấp đã tồn tại trong hệ thống', 'Danh mục đã có cấp trùng tên (không phân biệt hoa thường).'],
        ],
        'ghi_chu': ['Lưu ý: nút Import Excel chỉ hiện với người có quyền Quản lý. Mỗi lần nhập tối đa 500 dòng; file dài hơn hệ thống báo “File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần.” Người tạo của cấp nhập từ Excel là chính người thực hiện nhập, và lịch sử có mốc Tạo mới. Cấp nhập từ Excel luôn ở trạng thái Hoạt động (file mẫu không có cột Trạng thái).'],
    },
    'tuy_chinh_cot': {'cot_khoa': 'Ba cột STT, Tên cấp và Hành động'},

    'shots': {'list': '01_list.png', 'rowmenu': '03_rowmenu.png', 'filter': 'filter.png', 'filter_result': '04_filter_result.png',
              'create': '10_create.png', 'create_error': '11_create_error.png', 'edit': '12_edit.png',
              'delete': '13_delete.png', 'lock': '14_lock.png', 'unlock': '15_unlock.png', 'history': '16_history.png',
              'detail': '17_detail.png', 'export': '20_export.png', 'import_open': '21_import_open.png',
              'import_loaded': '22_import_loaded.png', 'import_validated': '23_import_validated.png', 'colcfg': '25_colcfg.png'},

    # lockName: cấp đang Hoạt động, CHƯA được dùng ở đâu (tra DB local_hrm_erp 28/09/2026, id 6) -> dòng đủ 4 nút.
    'capture': {'route': '/customer-care/levels',
                'menu': {'phanhe': 'CSKH SAU BÁN', 'nhom': 'Danh mục', 'muc': 'Cấp dịch vụ bảo dưỡng'},
                'search': 'Tìm theo tên cấp dịch vụ', 'searchText': 'Cấp 1', 'detailCol': 1,
                'lockName': 'Cấp 2 (6T)', 'create': True, 'lock': True},

    'import_test': {
        'cols': ['STT', 'Tên cấp *'],
        'rows': [
            [1, 'DOC-Cấp 1 (6T) thử'],
            [2, 'DOC-Cấp 2 (12T) thử'],
            [3, 'DOC-Cấp 3 (36T/9000H) thử'],
            [4, ''],                              # bỏ trống bắt buộc
            [5, 'DOC-Cấp 1 (6T) thử'],            # trùng dòng 1 trong file
            [6, 'Cấp 1 (6T)'],                    # trùng hệ thống
            [7, 'DOC-' + 'X' * 260],              # quá 255 ký tự
        ],
    },

    'uml': {
        'mains': [('FR-01', 'Xem danh sách cấp dịch vụ', 'view'), ('FR-03', 'Thêm mới cấp dịch vụ', 'crud'),
                  ('FR-04', 'Chỉnh sửa cấp dịch vụ', 'crud'), ('FR-05', 'Xóa cấp dịch vụ', 'action'),
                  ('FR-06', 'Khóa / Mở khóa cấp dịch vụ', 'action'),
                  ('FR-08', 'Import file cấp dịch vụ', 'io'), ('FR-09', 'Xuất danh sách cấp dịch vụ ra Excel', 'io')],
        'subs': [('FR-02', 'Tìm kiếm và lọc cấp dịch vụ', 'view'), ('FR-10', 'Xem chi tiết cấp dịch vụ', 'view'),
                 ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
        'rieng': [('FR-10', 'Xem chi tiết cấp dịch vụ', 'view')],
    },

    'srs': {
        'muc_dich': ['Là căn cứ nghiệm thu chức năng.',
                     'Làm rõ ràng buộc trùng Tên cấp (duy nhất toàn danh mục), trạng thái Hoạt động / Khóa, và điều kiện xóa: chỉ xóa hẳn cấp đang Hoạt động chưa được sử dụng ở 6 nơi (gói bảo dưỡng, cấp bảo dưỡng của gói, báo giá, hợp đồng, phiếu phân công, phiếu nhập kết quả).'],
        'quyen_truoc': ['Màn hình dùng 2 quyền riêng, không phân quyền theo công ty / phòng ban / bộ phận. Không có quyền nào thì mục menu bị ẩn và không vào được màn hình.'],
        'quyen_rows': [[Q_XEM, 'Vào màn hình, xem danh sách, tìm kiếm, lọc, xem chi tiết, xem lịch sử, xuất Excel.'],
                       [Q_QL, 'Toàn bộ quyền Xem, cộng thêm Tạo mới, Sửa, Xóa, Khóa, Mở khóa, Import Excel.']],
        'ma_tran': [['Chức năng', Q_XEM, Q_QL]] + [[f, x, 'Có'] for f, x in [
            ('FR-01 Xem danh sách cấp dịch vụ', 'Có'), ('FR-02 Tìm kiếm và lọc', 'Có'), ('FR-03 Thêm mới cấp dịch vụ', 'Không'),
            ('FR-04 Chỉnh sửa cấp dịch vụ', 'Không'), ('FR-05 Xóa cấp dịch vụ', 'Không'), ('FR-06 Khóa / Mở khóa cấp dịch vụ', 'Không'),
            ('FR-07 Xem lịch sử thay đổi', 'Có'), ('FR-08 Import file cấp dịch vụ', 'Không'), ('FR-09 Xuất danh sách ra Excel', 'Có'),
            ('FR-10 Xem chi tiết cấp dịch vụ', 'Có'), ('FR-11 Tùy chỉnh cột hiển thị', 'Có')]],
        'ma_tran_widths': [2.4, 1.6, 1.6],
        'quyen_sau': ['Nút không có quyền dùng thì ẩn hẳn. Máy chủ kiểm tra lại quyền ở mọi chức năng ghi dữ liệu (Tạo mới, Sửa, Xóa, Khóa, Mở khóa, Import) và ở chức năng xem/xuất.'],
        'fr': [
            {'ten': 'Xem danh sách cấp dịch vụ',
             'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của Cấp dịch vụ bảo dưỡng tại phần mô tả chi tiết.',
             'gioi_thieu': [['Tên chức năng', 'Xem danh sách cấp dịch vụ'],
                            ['Mô tả', 'Hiển thị toàn bộ cấp dịch vụ trong danh mục (cả Hoạt động lẫn Khóa), có phân trang và sắp xếp.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý cấp dịch vụ bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Người dùng đã đăng nhập và có ít nhất một trong hai quyền của màn hình.'],
                            ['Dòng sự kiện chính', '1. Người dùng vào menu CSKH sau bán → Danh mục → Cấp dịch vụ bảo dưỡng.\n2. Hệ thống nạp trang đầu tiên của danh sách (10 dòng).\n3. Bảng hiển thị dữ liệu kèm tổng số bản ghi.'],
                            ['Dòng sự kiện phụ', '• Không có bản ghi khớp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n• Không có quyền nào của màn hình → mục menu bị ẩn, không vào được màn hình.']],
             'anh': [('list', 'Màn Cấp dịch vụ bảo dưỡng lúc mới truy cập')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Mô tả'],
                    ['1', 'STT', 'Table/Grid', 'Read-only', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị, không ẩn được.'],
                    ['2', 'Tên cấp', 'Table/Grid', 'Read-only', 'Tên cấp dịch vụ. Luôn hiển thị, sắp xếp được. Bấm vào tên mở cửa sổ Xem (xem 2.10).'],
                    ['3', 'Người tạo', 'Table/Grid', 'Read-only', 'Người đã thêm bản ghi.'],
                    ['4', 'Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm, sắp xếp được.'],
                    ['5', 'Người cập nhật', 'Table/Grid', 'Read-only', 'Mặc định ẩn.'],
                    ['6', 'Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm. Mặc định ẩn, sắp xếp được.'],
                    ['7', 'Trạng thái', 'Badge', 'Read-only', 'Hoạt động hoặc Khóa.'],
                    ['8', 'Hành động', 'Table/Grid', 'Read-only', 'Sửa (quyền Quản lý, cấp đang Hoạt động), Xóa (quyền Quản lý, cấp đang Hoạt động và chưa được sử dụng), Khóa / Mở khóa (quyền Quản lý), Lịch sử (luôn hiện). Từ 4 nút trở lên thì 2 nút đầu hiện thẳng, còn lại trong nút ba chấm.'],
                    ['9', 'Nút Tạo mới', 'Button', 'Enable', 'Chỉ hiện với quyền Quản lý. Mở cửa sổ Tạo cấp dịch vụ.'],
                    ['10', 'Nút Xuất Excel', 'Button', 'Enable', 'Mở cửa sổ Chọn trường xuất file (xem 2.9).'],
                    ['11', 'Nút Import Excel', 'Button', 'Enable', 'Chỉ hiện với quyền Quản lý. Mở cửa sổ Import cấp dịch vụ bảo dưỡng (xem 2.8).'],
                    ['12', 'Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', 'Mở cửa sổ Tuỳ chỉnh cột (xem 2.11).'],
                    ['13', 'Phân trang', 'Pagination', 'Enable', 'Số dòng/trang 5 / 10 / 20 / 50 / 100, mặc định 10.']],
             'ui_widths': [0.6, 1.4, 0.9, 0.8, 3],
             'events': [['Mở màn hình', 'System', 'After:\n– Nạp trang đầu (xếp theo thứ tự tạo), hiển thị tổng số bản ghi.'],
                        ['Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Đổi chiều sắp xếp và nạp lại danh sách từ trang 1.'],
                        ['Chuyển trang', 'Click', 'Before:\n– Giữ nguyên từ khóa, Trạng thái và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'],
                        ['Đổi số dòng mỗi trang', 'Change', 'After:\n– Quay về trang 1 và nạp lại theo số dòng mới.']]},
            {'ten': 'Tìm kiếm và lọc cấp dịch vụ',
             'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang. Chỉ bổ sung tiêu chí tìm kiếm/lọc riêng của Cấp dịch vụ bảo dưỡng.',
             'gioi_thieu': [['Tên chức năng', 'Tìm kiếm và lọc cấp dịch vụ'],
                            ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh theo tên cấp và ô Trạng thái. Màn hình không có Tìm kiếm nâng cao.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý'],
                            ['Điều kiện ban đầu', 'Đang ở màn Cấp dịch vụ bảo dưỡng.'],
                            ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa và bấm Tìm kiếm / Enter, hoặc chọn Trạng thái (lọc ngay).\n2. Hệ thống áp đồng thời các tiêu chí (tên cấp khớp một phần, không phân biệt hoa thường; đúng Trạng thái) và nạp lại danh sách từ trang 1.'],
                            ['Dòng sự kiện phụ', '• Gõ mà chưa bấm Tìm kiếm / Enter → danh sách chưa lọc.\n• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n• Bấm Làm mới → xóa từ khóa và Trạng thái VÀ nạp lại danh sách đầy đủ ngay.\n• Điều kiện được ghi nhớ 10 phút khi quay lại màn hình.']],
             'anh': [('filter', 'Khu vực tìm kiếm và lọc của màn Cấp dịch vụ bảo dưỡng')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Mô tả'],
                    ['1', 'Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Placeholder “Tìm theo tên cấp dịch vụ...”. Tìm theo TÊN cấp (khớp một phần).'],
                    ['2', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Nhãn nổi. Bỏ trống thì hiện cả hai trạng thái. Chọn là lọc ngay.'],
                    ['3', 'Nút Tìm kiếm', 'Button', 'Enable', '–', 'Áp dụng các tiêu chí.'],
                    ['4', 'Nút Làm mới', 'Button', 'Enable', '–', 'Xóa hết tiêu chí VÀ nạp lại danh sách ngay.']],
             'ui_widths': [0.6, 1.2, 0.8, 0.7, 1.1, 2.6],
             'events': [['Bấm Tìm kiếm / Enter', 'Click', 'After:\n– Áp đồng thời các tiêu chí theo kiểu “và”, nạp lại bảng từ trang 1.'],
                        ['Chọn Trạng thái', 'Change', 'After:\n– Lọc ngay, nạp lại bảng từ trang 1.'],
                        ['Bấm Làm mới', 'Click', 'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ.']]},
            {'ten': 'Thêm mới cấp dịch vụ', 'uc': 'uc_fr03',
             'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Thêm mới cấp dịch vụ'],
                            ['Mô tả', 'Thêm một cấp dịch vụ mới thông qua cửa sổ nhập liệu.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý cấp dịch vụ bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Đang ở màn Cấp dịch vụ bảo dưỡng.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở cửa sổ “Tạo cấp dịch vụ”, Trạng thái mặc định Hoạt động.\n3. Người dùng nhập Tên cấp, (tùy chọn) đổi Trạng thái và bấm Lưu.\n4. Hệ thống cắt khoảng trắng đầu cuối, kiểm tra dữ liệu, ghi bản ghi mới và ghi lịch sử Tạo mới.\n5. Cửa sổ đóng, danh sách nạp lại, báo “Thêm mới thành công”.'],
                            ['Dòng sự kiện phụ', '• Bỏ trống hoặc quá 255 ký tự → báo đỏ ngay dưới ô + toast “Bạn chưa nhập đầy đủ thông tin”, cửa sổ KHÔNG đóng.\n• Trùng tên → ô báo “Tên cấp đã tồn tại”.\n• Bấm “Lưu và tiếp tục” → ghi bản ghi rồi giữ cửa sổ mở với ô trống, Trạng thái về Hoạt động.\n• Bấm Đóng khi đã nhập dở → hỏi “Thông tin chưa lưu” (Thoát / Ở lại).'],
                            ['Yêu cầu đặc biệt', 'Cửa sổ có ba nút: Lưu, Lưu và tiếp tục, Đóng. Nút Lưu bị khóa trong lúc đang ghi để chống bấm hai lần.']],
             'menu_them': ' => Tạo mới {icon:btn_taomoi}',
             'ghi_chu_layout': 'Cửa sổ Tạo cấp dịch vụ được mở ngay trên màn hình danh sách.',
             'anh': [('create', 'Cửa sổ Tạo cấp dịch vụ'), ('create_error', 'Lỗi đỏ ngay dưới ô còn thiếu')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Mô tả'],
                    ['1', 'Tên cấp', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Duy nhất toàn danh mục (kể cả cấp đang Khóa). Bỏ trống “Bắt buộc phải nhập”; trùng “Tên cấp đã tồn tại”; quá dài “Vui lòng nhập tối đa 255 ký tự.”'],
                    ['2', 'Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Mặc định Hoạt động, luôn có giá trị (không xóa trống được).'],
                    ['3', 'Nút Lưu', 'Button', 'Enable', '', '', 'Ghi bản ghi rồi đóng cửa sổ.'],
                    ['4', 'Nút Lưu và tiếp tục', 'Button', 'Enable', '', '', 'Ghi bản ghi rồi giữ cửa sổ mở để nhập tiếp.'],
                    ['5', 'Nút Đóng', 'Button', 'Enable', '', '', 'Hủy bỏ, không ghi gì.']],
             'ui_widths': [0.6, 1.3, 0.8, 0.6, 1.1, 0.5, 2.3],
             'events': [['Bấm nút Tạo mới', 'Click', 'After:\n– Mở cửa sổ nhập liệu với ô Tên cấp trống, Trạng thái = Hoạt động.'],
                        ['Bấm Lưu', 'Click', 'During:\n– Kiểm tra bắt buộc, độ dài, trùng tên toàn danh mục.\n– Có lỗi → báo đỏ dưới ô, không thực hiện After.\nAfter:\n– Ghi bản ghi mới, người tạo là người đang đăng nhập, ghi lịch sử Tạo mới.\n– Đóng cửa sổ, nạp lại danh sách, báo “Thêm mới thành công”.'],
                        ['Bấm Lưu và tiếp tục', 'Click', 'During:\n– Như nút Lưu.\nAfter:\n– Ghi bản ghi, xóa trắng ô, GIỮ cửa sổ mở.'],
                        ['Bấm Đóng', 'Click', 'After:\n– Chưa nhập gì → đóng cửa sổ. Đã nhập → hỏi “Thông tin chưa lưu”.']]},
            {'ten': 'Chỉnh sửa cấp dịch vụ', 'uc': 'uc_fr04',
             'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Chỉnh sửa cấp dịch vụ'],
                            ['Mô tả', 'Sửa tên, trạng thái của một cấp dịch vụ đã có. Dùng chung cửa sổ với Thêm mới.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý cấp dịch vụ bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Cấp dịch vụ đang ở trạng thái Hoạt động.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm biểu tượng bút chì ở dòng cần sửa.\n2. Hệ thống mở cửa sổ “Sửa cấp dịch vụ” với Tên cấp và Trạng thái hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi và ghi lịch sử.\n5. Cửa sổ đóng, báo “Cập nhật thành công”.'],
                            ['Dòng sự kiện phụ', '• Giữ nguyên tên của chính bản ghi → không báo trùng.\n• Trùng tên với cấp khác → báo “Tên cấp đã tồn tại”.\n• Cấp đang được sử dụng vẫn sửa được; chứng từ đang dùng hiển thị tên mới.\n• Cấp vừa bị người khác khóa → báo “%s”, không ghi thay đổi.\n• Cấp vừa bị người khác xóa (lúc mở cửa sổ) → báo “Dữ liệu đã thay đổi, vui lòng tải lại”.' % MSG_LOCKED]],
             'menu_them': ' => Sửa {icon:btn_sua}',
             'anh': [('edit', 'Cửa sổ Sửa cấp dịch vụ')],
             'events': [['Bấm biểu tượng bút chì', 'Click', 'Before:\n– Không có quyền Quản lý hoặc cấp đang Khóa thì nút không hiển thị.\nAfter:\n– Mở cửa sổ với dữ liệu hiện tại.'],
                        ['Bấm Lưu', 'Click', 'Before:\n– Máy chủ chặn nếu cấp đang Khóa (“%s”).\nDuring:\n– Kiểm tra như Thêm mới, bỏ qua trùng với chính bản ghi.\nAfter:\n– Ghi thay đổi, ghi lịch sử “Thay đổi thông tin” (đổi Trạng thái ghi mốc “Thay đổi trạng thái” riêng), báo “Cập nhật thành công”.' % MSG_LOCKED]]},
            {'ten': 'Xóa cấp dịch vụ', 'uc': 'uc_fr05',
             'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Xóa cấp dịch vụ'],
                            ['Mô tả', 'Xóa hẳn một cấp dịch vụ đang Hoạt động và chưa được sử dụng ở đâu.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý cấp dịch vụ bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Cấp đang Hoạt động và chưa xuất hiện ở: ' + USED_L + '.'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm biểu tượng thùng rác.\n2. Hệ thống hiện hộp “Xác nhận xóa” nêu rõ tên cấp.\n3. Người dùng bấm Xóa.\n4. Máy chủ kiểm tra lại trạng thái và tình trạng sử dụng, xóa hẳn bản ghi, ghi lịch sử Xóa.\n5. Hệ thống báo “Xóa thành công”, nạp lại danh sách.'],
                            ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Cấp đang được sử dụng hoặc đang Khóa → nút Xóa KHÔNG hiển thị.\n• Cấp vừa được đưa vào chứng từ sau lúc mở danh sách → báo “%s”, không xóa.\n• Cấp vừa bị người khác khóa → báo “%s”, không xóa.' % (MSG_USED, MSG_LOCKED)]],
             'menu_them': ' => Xóa {icon:btn_xoa}',
             'anh': [('delete', 'Hộp xác nhận xóa cấp dịch vụ')],
             'events': [['Bấm biểu tượng thùng rác', 'Click', 'Before:\n– Chỉ hiện khi cấp đang Hoạt động và chưa được sử dụng.\nAfter:\n– Hiện hộp xác nhận kèm tên bản ghi.'],
                        ['Bấm Xóa', 'Click', 'During:\n– Máy chủ chặn nếu cấp đang Khóa (“%s”) hoặc đã được sử dụng (“%s”).\nAfter:\n– Xóa hẳn bản ghi, nạp lại danh sách, báo “Xóa thành công”.' % (MSG_LOCKED, MSG_USED)],
                        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.']]},
            {'ten': 'Khóa / Mở khóa cấp dịch vụ', 'uc': 'uc_fr06',
             'qtc': 'Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục và Quy tắc ghi lịch sử.',
             'gioi_thieu': [['Tên chức năng', 'Khóa / Mở khóa cấp dịch vụ'],
                            ['Mô tả', 'Đổi trạng thái cấp dịch vụ giữa Hoạt động và Khóa. Cấp đã Khóa vẫn nằm trong danh mục nhưng không chọn được ở chứng từ mới.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý cấp dịch vụ bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Cấp cần đổi trạng thái đang có trong danh sách (khóa được cả cấp đang được sử dụng).'],
                            ['Dòng sự kiện chính', '1. Người dùng chọn Khóa (hoặc Mở khóa) ở cột Hành động.\n2. Hệ thống hiện hộp xác nhận “Khóa cấp dịch vụ” / “Mở khóa cấp dịch vụ” nêu rõ tên cấp.\n3. Người dùng xác nhận.\n4. Hệ thống đổi trạng thái, ghi lịch sử, báo “Khóa thành công” / “Mở khóa thành công”.'],
                            ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Sau khi Khóa, nút Sửa và Xóa biến mất, chỉ còn Mở khóa và Lịch sử.\n• Cấp đã bị người khác đổi trạng thái → báo “%s”.' % MSG_CONFLICT],
                            ['Yêu cầu đặc biệt', 'Cấp đã Khóa không còn chọn được khi Tạo mới gói bảo dưỡng, khi Import gói bảo dưỡng và trong danh sách chọn gói của Báo giá dịch vụ. Gói / chứng từ cũ đang dùng giữ nguyên, hiển thị đúng tên kèm 🔒.']],
             'menu_them': ' => Khóa / Mở khóa',
             'anh': [('lock', 'Hộp xác nhận khóa cấp dịch vụ'), ('unlock', 'Hộp xác nhận mở khóa cấp dịch vụ')],
             'events': [['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên bản ghi.'],
                        ['Xác nhận', 'Click', 'During:\n– Bản ghi đã ở trạng thái đích → báo “%s”, dừng.\nAfter:\n– Đổi trạng thái, KHÔNG xóa dữ liệu, ghi lịch sử “Thay đổi trạng thái”, cập nhật cột Trạng thái và các nút.' % MSG_CONFLICT],
                        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.']]},
            {'ten': 'Xem lịch sử thay đổi',
             'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Cấp dịch vụ bảo dưỡng nếu có.',
             'gioi_thieu': [['Tên chức năng', 'Xem lịch sử thay đổi'],
                            ['Mô tả', 'Liệt kê các lần thay đổi của một cấp dịch vụ (Tên cấp, Trạng thái), kèm giá trị cũ → mới, người thực hiện và thời điểm.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý'],
                            ['Dòng sự kiện chính', '1. Người dùng chọn Lịch sử ở cột Hành động, hoặc mở cửa sổ Xem cấp dịch vụ.\n2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <tên cấp>”, mốc mới nhất ở trên cùng.'],
                            ['Dòng sự kiện phụ', '• Bản ghi chưa có mốc nào → “Chưa có lịch sử thao tác nào.”\n• Có bộ lọc theo loại hành động, người thực hiện, thời gian.']],
             'menu_them': ' => Lịch sử',
             'anh': [('history', 'Cửa sổ Lịch sử thay đổi của cấp dịch vụ')]},
            {'ten': 'Import file cấp dịch vụ', 'uc': 'uc_fr08',
             'qtc': 'Quy tắc Import file, Validate dữ liệu, Thông báo và Quy định chung về danh mục. Chỉ bổ sung mapping/validation riêng của Cấp dịch vụ bảo dưỡng.',
             'gioi_thieu': [['Tên chức năng', 'Import file cấp dịch vụ'],
                            ['Mô tả', 'Thêm nhiều cấp dịch vụ cùng lúc từ file Excel mẫu, có bước Validate trước khi ghi.'],
                            ['Tác nhân', 'Người dùng có quyền Quản lý cấp dịch vụ bảo dưỡng'],
                            ['Điều kiện ban đầu', 'Đang ở màn Cấp dịch vụ bảo dưỡng và đã chuẩn bị file theo mẫu.'],
                            ['Dòng sự kiện chính', '1. Bấm Import Excel.\n2. Bấm Tải file mẫu (Mau_import_cap_dich_vu_bao_duong.xlsx), điền dữ liệu.\n3. Bấm Chọn file Excel rồi Load lên bảng.\n4. Bấm Validate; hệ thống kiểm tra từng dòng như quy tắc Thêm mới (mục 2.3), khóa dòng hợp lệ.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi.\n6. Bấm Import; hệ thống ghi các dòng hợp lệ, báo “Import thành công N cấp dịch vụ bảo dưỡng.”, đóng cửa sổ và nạp lại danh sách.'],
                            ['Dòng sự kiện phụ', '• File không phải .xlsx/.xls → “Vui lòng chọn file .xlsx hoặc .xls”.\n• Quá 500 dòng → “File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần.”\n• Còn dòng lỗi → nút Import không bấm được.\n• Có dòng ghi thất bại lúc Import → “Import thành công x/y cấp dịch vụ bảo dưỡng. N dòng thất bại.”'],
                            ['Yêu cầu đặc biệt', 'Validate không ghi dữ liệu. Bản ghi import luôn ở trạng thái Hoạt động, người tạo là người thực hiện, lịch sử có mốc Tạo mới.']],
             'menu_them': ' => Import Excel {icon:btn_import}',
             'ghi_chu_layout': 'Cửa sổ Import được mở ngay trên màn hình danh sách.',
             'anh': [('import_open', 'Cửa sổ Import cấp dịch vụ bảo dưỡng khi vừa mở'), ('import_loaded', 'Dữ liệu đã được load lên bảng xem trước'),
                     ('import_validated', 'Kết quả Validate — mỗi dòng lỗi nêu rõ lý do')],
             'bang_them': [('Quy tắc kiểm tra riêng của file Import', [['Cột', 'Quy tắc / thông báo lỗi'],
                            ['Tên cấp *', 'Bắt buộc (“Tên cấp không được để trống”), tối đa 255 ký tự (“Tên cấp tối đa 255 ký tự”), không trùng trong file (“Tên cấp bị trùng với dòng N trong file”), không trùng hệ thống kể cả cấp đang Khóa (“Tên cấp đã tồn tại trong hệ thống”). So trùng không phân biệt chữ hoa chữ thường.']], [1.2, 4])]},
            {'ten': 'Xuất danh sách cấp dịch vụ ra Excel', 'uc': 'uc_fr09',
             'qtc': 'Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của Cấp dịch vụ bảo dưỡng.',
             'gioi_thieu': [['Tên chức năng', 'Xuất danh sách cấp dịch vụ ra Excel'],
                            ['Mô tả', 'Xuất kết quả đang tìm kiếm / lọc ra file Excel, cho phép chọn trường và thứ tự cột.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý'],
                            ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiển thị trên bảng.\n3. Người dùng tích chọn và kéo ☰ để sắp thứ tự.\n4. Bấm Xuất file; hệ thống tải cap_dich_vu_bao_duong.xlsx theo đúng từ khóa, Trạng thái, thứ tự sắp xếp và thứ tự trường, báo “Xuất Excel thành công”.'],
                            ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Bấm Đóng → không xuất gì.\n• Kết quả rỗng → file chỉ có dòng tiêu đề.'],
                            ['Yêu cầu đặc biệt', 'File chứa toàn bộ kết quả tìm kiếm (tối đa 10,000 dòng), không giới hạn ở trang đang xem. Cột STT luôn đứng đầu. Chỉ xuất Excel.']],
             'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
             'anh': [('export', 'Cửa sổ Chọn trường xuất file')],
             'ui': [['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả'],
                    ['1', 'Danh sách trường', 'Checkbox chọn nhiều', 'Enable', 'Tích sẵn cột đang hiển thị', 'Tên cấp, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Kéo ☰ đổi thứ tự.'],
                    ['2', 'Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', 'Hiển thị', 'Tích / bỏ tích toàn bộ.'],
                    ['3', 'Nút Xuất file', 'Button', 'Enable/Disable', 'Mờ khi chưa chọn trường', 'Sinh file và tải về.'],
                    ['4', 'Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.']],
             'ui_widths': [0.6, 1.5, 1, 0.8, 1.2, 2.6]},
            {'ten': 'Xem chi tiết cấp dịch vụ', 'uc': 'uc_fr10',
             'qtc': 'Màn Xem chi tiết và Phân quyền.',
             'gioi_thieu': [['Tên chức năng', 'Xem chi tiết cấp dịch vụ'],
                            ['Mô tả', 'Cửa sổ “Xem cấp dịch vụ” hiển thị Tên cấp và Trạng thái ở chế độ chỉ đọc, kèm khối Lịch sử.'],
                            ['Tác nhân', 'Người dùng có quyền Xem hoặc Quản lý'],
                            ['Dòng sự kiện chính', '1. Người dùng bấm tên cấp ở danh sách.\n2. Hệ thống mở cửa sổ Xem, chỉ có nút Đóng.'],
                            ['Dòng sự kiện phụ', '• Cấp đang Khóa vẫn xem được.\n• Cấp vừa bị người khác xóa → báo “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.']],
             'anh': [('detail', 'Cửa sổ Xem cấp dịch vụ ở chế độ chỉ đọc')]},
            {'ten': 'Tùy chỉnh cột hiển thị',
             'qtc': 'Tùy chỉnh cột.',
             'gioi_thieu': [['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
                            ['Mô tả', 'Bật/tắt và sắp xếp thứ tự cột của bảng; cấu hình lưu riêng theo người dùng.'],
                            ['Yêu cầu đặc biệt', 'Cột STT, Tên cấp, Hành động bị khóa. Mặc định ẩn: Người cập nhật, Ngày cập nhật.']],
             'menu_them': ' => Cấu hình cột {icon:btn_cauhinhcot}',
             'anh': [('colcfg', 'Cửa sổ Tuỳ chỉnh cột')]},
        ],
        'quy_tac': [
            ('BR-01', 'Phân quyền Xem và Quản lý',
             ['Quyền “Xem cấp dịch vụ bảo dưỡng”: xem danh sách, tìm kiếm, lọc, xem chi tiết, xem lịch sử, xuất Excel.',
              'Quyền “Quản lý cấp dịch vụ bảo dưỡng”: thêm các thao tác Tạo mới, Sửa, Xóa, Khóa, Mở khóa, Import Excel.'],
             ['Tất cả chức năng']),
            ('BR-02', 'Ràng buộc trùng tên',
             ['Tên cấp không được trùng trên toàn danh mục, kể cả cấp đang Khóa; khoảng trắng thừa đầu cuối được cắt bỏ trước khi kiểm tra.',
              'Thông báo khi trùng: “Tên cấp đã tồn tại”.'],
             ['Thêm mới cấp dịch vụ', 'Chỉnh sửa cấp dịch vụ', 'Import file cấp dịch vụ']),
            ('BR-03', 'Điều kiện xóa cấp dịch vụ',
             ['Chỉ xóa được cấp đang Hoạt động VÀ chưa được sử dụng ở: ' + USED_L + '; ngược lại nút Xóa bị ẩn.',
              'Xóa là xóa hẳn bản ghi khỏi hệ thống. Cấp đã được sử dụng thì dùng Khóa thay cho Xóa.',
              'Máy chủ kiểm tra lại tại thời điểm xóa: đã được sử dụng báo “%s”; đang Khóa báo “%s”.' % (MSG_USED, MSG_LOCKED)],
             ['Xóa cấp dịch vụ']),
            ('BR-04', 'Cấp dịch vụ đang Khóa',
             ['Khóa được cả cấp đang được sử dụng.',
              'Cấp đang Khóa không sửa, không xóa được; phải Mở khóa trước. Máy chủ chặn với câu “%s”.' % MSG_LOCKED,
              'Cấp đang Khóa không còn chọn được khi Tạo mới gói bảo dưỡng, khi Import gói bảo dưỡng (báo “Cấp bảo dưỡng "…" không có trong danh mục hoặc đã bị khóa”) và trong danh sách chọn gói của Báo giá dịch vụ.',
              'Gói bảo dưỡng và chứng từ cũ đang dùng cấp đó giữ nguyên, hiển thị đúng tên kèm 🔒.',
              'Cấp đang được sử dụng vẫn sửa được tên khi đang Hoạt động; tên mới hiển thị ở các chứng từ đang dùng cấp đó.'],
             ['Chỉnh sửa cấp dịch vụ', 'Xóa cấp dịch vụ', 'Khóa / Mở khóa cấp dịch vụ']),
            ('BR-05', 'Thao tác đồng thời',
             ['Hai người cùng Khóa hoặc cùng Mở khóa một cấp: người bấm sau nhận “%s”, không ghi thêm mốc lịch sử trùng.' % MSG_CONFLICT],
             ['Khóa / Mở khóa cấp dịch vụ']),
            ('BR-06', 'Giới hạn Import',
             ['Mỗi lần nhập tối đa 500 dòng dữ liệu.',
              'Cấp nhập từ Excel dùng chung quy tắc với Thêm mới, kể cả kiểm tra trùng tên với dữ liệu có sẵn và giữa các dòng trong file; luôn ở trạng thái Hoạt động.'],
             ['Import file cấp dịch vụ']),
            ('BR-07', 'Ghi lịch sử thay đổi',
             ['Mọi thao tác Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa đều ghi lịch sử kèm người thực hiện.',
              'Đổi Trạng thái ngay trong cửa sổ Sửa được ghi thành mốc “Thay đổi trạng thái” riêng.',
              'Người tạo / người cập nhật lấy theo nhân viên đang đăng nhập.'],
             ['Thêm mới cấp dịch vụ', 'Chỉnh sửa cấp dịch vụ', 'Xóa cấp dịch vụ', 'Khóa / Mở khóa cấp dịch vụ', 'Xem lịch sử thay đổi']),
        ],
    },
}

CFG['loi_code'] = [
    'Import — thông báo “Tên cấp bị trùng với dòng N trong file” đánh số dòng lệch 1: máy chủ lấy N = thứ tự dòng + 2 (LevelService::validateRows), trong khi cột # của bảng xem trước đánh từ 1 và dữ liệu trong file mẫu bắt đầu từ hàng 3 của Excel (hàng 1 tiêu đề, hàng 2 mô tả). Ví dụ trùng với dòng dữ liệu đầu tiên thì báo “dòng 2”, người dùng tìm theo cột # hay theo số hàng Excel đều không khớp.',
    'Thao tác trên cấp VỪA BỊ NGƯỜI KHÁC XÓA (Xóa lần hai, Khóa, Mở khóa, bấm Lưu ở cửa sổ Sửa đang mở) nhận toast tiếng Anh “Item Not Found!”: route dùng model binding {level} nên Laravel trả 404 từ app/Exceptions/Handler trước khi tới guardCatalogExists() — câu “Trạng thái đã bị thay đổi. Vui lòng load lại trang” của LevelService::destroy/lock/unlock không bao giờ chạy tới. Tài liệu không tả câu này.',
    'Routes/api.php: middleware recordNotLocked đứng TRƯỚC checkPermission ở PUT/DELETE /levels/{level} → người chỉ có quyền Xem gọi thẳng API sửa / xóa một cấp đang Khóa nhận 423 “Bản ghi đang bị khoá…” thay vì 403 không có quyền (không ghi được dữ liệu, chỉ sai mã lỗi / lộ trạng thái).',
]

CFG['tc_ngoai_pham_vi'] = [
    'B2, G19, G27: còn ghi đường menu cũ “Chăm sóc khách hàng → Danh mục- Dịch vụ” (G19 còn kèm đường link) — nay là CSKH sau bán → Danh mục → Cấp dịch vụ bảo dưỡng; tài liệu không được ghi URL.',
    'B5, TC_01.004 (R27), TC_03.002 (R41): còn nói cột “Cập nhật” — nay là Ngày cập nhật (mặc định ẩn, bật ở Cấu hình cột) và có thêm Người tạo / Ngày tạo.',
    'TC_04.006 (R54): còn nói nút Xem trên mỗi dòng — nay bỏ nút Xem, bấm vào tên cấp để mở cửa sổ Xem (cửa sổ có thêm ô Trạng thái chỉ đọc).',
    'TC_07.007 (R92): message quá dài nay là “Vui lòng nhập tối đa 255 ký tự.” (không phải “Tối đa 255 ký tự”).',
    'TC_08.002 (R97): sửa cấp vừa bị người khác xóa — thực tế bấm Lưu nhận “Item Not Found!” (xem loi_code), Expected đang ghi chung chung “báo dữ liệu đã thay đổi hoặc không còn tồn tại”.',
    'Chưa có case cho Tùy chỉnh cột và cho khối Lịch sử trong cửa sổ Xem (Lịch sử của Khóa / Mở khóa đã có ở nhóm X).',
]

# ---- Sửa tab testcase "7. DM cấp dịch vụ bảo dưỡng" — số hàng theo dump ref/testcase_tab.txt tải LẠI 28/09/2026 (sau khi tab bị sửa tay, còn 122 hàng) ----
# Lượt 25/09 (Xuất Excel + nhóm IX Import) ĐÃ chạy lên sheet; kế hoạch dưới đây là lượt 28/09 (Trạng thái / Khóa / Xóa hẳn).
_PRE = 'Đăng nhập bằng tài khoản có quyền "Quản lý cấp dịch vụ bảo dưỡng". "Cấp 1" đang Hoạt động, được dùng ở gói bảo dưỡng, hợp đồng dịch vụ và báo giá dịch vụ; "Cấp thử" đang Hoạt động, chưa dùng ở đâu; "Cấp khóa thử" đang Khóa, chưa dùng ở đâu.'
_XF = 'Bấm Xuất Excel → cửa sổ “Chọn trường xuất file” → bấm Xuất file'
_HIDDEN_DEL = '- KHÔNG có nút Xóa (biểu tượng thùng rác)\n- Vẫn có Sửa, Khóa, Lịch sử'
CFG['tc'] = {
    'tab': '7. DM cấp dịch vụ bảo dưỡng',
    'hdr_row': 72,            # "VI. XUẤT EXCEL"
    'blocks': [
        # II. BỘ LỌC & TÌM KIẾM (R31..R38, case cuối TC_02.008) — bộ lọc Trạng thái mới
        {'after': 38, 'merge_from': 31, 'cases': [
            ('TC_02.009', 'Lọc theo Trạng thái = Khóa', 'P0', _PRE,
             '1. Bấm ô Trạng thái\n2. Chọn Khóa', 'Trạng thái: Khóa',
             '- Danh sách lọc NGAY, không cần bấm Tìm kiếm, quay về trang 1\n- Chỉ hiện các cấp có cột Trạng thái = Khóa (có "Cấp khóa thử", không có "Cấp 1")'),
            ('TC_02.010', 'Lọc theo Trạng thái = Hoạt động', 'P1', _PRE,
             '1. Chọn Trạng thái = Hoạt động', 'Trạng thái: Hoạt động',
             '- Chỉ hiện các cấp đang Hoạt động (có "Cấp 1", "Cấp thử"; không có "Cấp khóa thử")'),
            ('TC_02.011', 'Bỏ trống Trạng thái thì hiện cả hai trạng thái', 'P1', _PRE,
             '1. Chọn Trạng thái = Khóa\n2. Bấm dấu x trong ô Trạng thái để xóa lựa chọn', '',
             '- Danh sách hiện lại cả cấp Hoạt động lẫn cấp Khóa, tổng dưới bảng bằng toàn danh mục\n- Ô Trạng thái chỉ có 2 lựa chọn Hoạt động / Khóa, không có lựa chọn “Tất cả”'),
            ('TC_02.012', 'Kết hợp tìm nhanh với Trạng thái', 'P1', _PRE,
             '1. Gõ "Cấp" và bấm Tìm kiếm\n2. Chọn Trạng thái = Khóa', 'Từ khóa: Cấp; Trạng thái: Khóa',
             '- Chỉ hiện cấp có chữ "Cấp" trong tên VÀ đang Khóa'),
            ('TC_02.013', 'Làm mới xóa cả ô Trạng thái', 'P1', _PRE,
             '1. Gõ từ khóa, bấm Tìm kiếm, chọn Trạng thái = Khóa\n2. Bấm Làm mới', '',
             '- Ô tìm nhanh và ô Trạng thái đều trống\n- Danh sách tải lại NGAY đủ toàn bộ cấp (cả Hoạt động lẫn Khóa)'),
        ]},
        # IV. THÊM / SỬA / XEM (R49..R59, case cuối TC_04.011) — ô Trạng thái trong cửa sổ Tạo/Sửa
        {'after': 59, 'merge_from': 49, 'cases': [
            ('TC_04.012', 'Tạo mới cấp ở trạng thái Khóa', 'P1', _PRE,
             '1. Bấm Tạo mới\n2. Nhập Tên cấp, chọn Trạng thái = Khóa\n3. Bấm Lưu\n4. Mở màn Danh mục gói bảo dưỡng, tạo mới một gói, mở danh sách chọn cấp dịch vụ',
             'Tên cấp: Cấp tạo khóa; Trạng thái: Khóa',
             '- Lưu thành công, báo "Thêm mới thành công"\n- Dòng mới có Trạng thái = Khóa, chỉ có Mở khóa và Lịch sử\n- Danh sách chọn cấp của gói mới KHÔNG có "Cấp tạo khóa"'),
            ('TC_04.013', 'Chuyển Trạng thái sang Khóa trong cửa sổ Sửa, kể cả cấp đang được sử dụng', 'P0', _PRE,
             '1. Bấm Sửa dòng "Cấp 1"\n2. Chọn Trạng thái = Khóa\n3. Bấm Lưu', 'Trạng thái: Khóa',
             '- Lưu thành công, báo "Cập nhật thành công" (không bị chặn vì đang được sử dụng)\n- Cột Trạng thái của "Cấp 1" đổi thành Khóa, dòng chỉ còn Mở khóa và Lịch sử\n- Lịch sử có mốc Thay đổi trạng thái: Hoạt động → Khóa'),
            ('TC_04.014', 'Bấm Lưu khi cấp vừa bị người khác khóa', 'P1',
             'Tài khoản A và B cùng có quyền "Quản lý cấp dịch vụ bảo dưỡng"; "Cấp thử" đang Hoạt động.',
             '1. A mở cửa sổ Sửa "Cấp thử", đổi Tên cấp\n2. B khóa "Cấp thử" ở cột Hành động\n3. A bấm Lưu', 'Tên cấp: Cấp thử đổi',
             '- A nhận thông báo "%s"\n- Tên KHÔNG đổi, "Cấp thử" vẫn ở trạng thái Khóa' % MSG_LOCKED),
        ]},
        # V. XÓA (R61..R71, case cuối TC_05.011) — điều kiện xóa mới
        {'after': 71, 'merge_from': 61, 'cases': [
            ('TC_05.012', 'Xóa cấp vừa bị người khác khóa', 'P1',
             'Tài khoản A và B cùng có quyền "Quản lý cấp dịch vụ bảo dưỡng" và cùng mở danh sách; "Cấp thử" đang Hoạt động, chưa dùng ở đâu.',
             '1. B khóa "Cấp thử"\n2. A (chưa tải lại trang) bấm thùng rác ở dòng "Cấp thử", bấm Xóa', '',
             '- A nhận thông báo "%s"\n- "Cấp thử" KHÔNG bị xóa, vẫn ở trạng thái Khóa' % MSG_LOCKED),
            ('TC_05.013', 'Chặn xóa cấp đang Khóa khi bỏ qua giao diện', 'P1', _PRE,
             '1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa "Cấp khóa thử"\n2. Mở lại màn hình', 'Cấp khóa thử (đang Khóa, chưa dùng)',
             '- Hệ thống từ chối, báo "%s"\n- "Cấp khóa thử" vẫn còn, vẫn Khóa' % MSG_LOCKED),
        ]},
        # VI. XUẤT EXCEL (R73..R84, case cuối TC_06.012) — cột Trạng thái trong file
        {'after': 84, 'merge_from': 73, 'cases': [
            ('TC_06.013', 'Cột Trạng thái trong file Excel', 'P1', _PRE,
             '1. Bấm Xuất Excel, giữ nguyên các trường tích sẵn\n2. Bấm Xuất file, mở file', '',
             '- File có cột Trạng thái\n- Cấp đang Hoạt động ghi "Hoạt động", cấp đang Khóa ghi "Khóa", khớp với bảng'),
            ('TC_06.014', 'Xuất Excel theo bộ lọc Trạng thái', 'P1', _PRE,
             '1. Chọn Trạng thái = Khóa\n2. ' + _XF + '\n3. Mở file', 'Trạng thái: Khóa',
             '- File chỉ chứa các cấp đang Khóa, số dòng bằng tổng dưới bảng'),
        ]},
        # Khóa / Mở khóa chưa có case → nhóm MỚI sau case cuối của tab (TC_09.019, R122)
        {'after': 122,
         'groups': [('X', 'KHÓA / MỞ KHÓA (bổ sung 28/09/2026)', 10, [
             ('Hộp xác nhận Khóa nêu đúng tên cấp', 'P0', _PRE,
              '1. Ở cột Hành động của "Cấp thử" bấm nút ba chấm "Hành động khác", chọn Khóa\n2. Đọc hộp xác nhận', '',
              '- Dòng "Cấp thử" có Sửa, Xóa hiện thẳng; Khóa và Lịch sử nằm trong nút ba chấm\n- Hộp tiêu đề "Khóa cấp dịch vụ", câu "Bạn có chắc muốn khóa cấp dịch vụ "Cấp thử"?"\n- Có hai nút Khóa và Hủy'),
             ('Khóa thành công', 'P0', 'Đang mở hộp xác nhận Khóa của "Cấp thử".',
              '1. Bấm Khóa\n2. Quan sát dòng "Cấp thử"', '',
              '- Báo "Khóa thành công"\n- Cột Trạng thái đổi thành Khóa\n- Dòng chỉ còn Mở khóa và Lịch sử (không còn Sửa, Xóa)'),
             ('Bấm Hủy thì không khóa', 'P1', 'Đang mở hộp xác nhận Khóa của "Cấp thử".',
              '1. Bấm Hủy\n2. Xem lại dòng "Cấp thử"', '',
              '- Hộp đóng, "Cấp thử" vẫn Hoạt động, các nút giữ nguyên'),
             ('Khóa được cấp đang được sử dụng', 'P0', _PRE,
              '1. Chọn Khóa ở dòng "Cấp 1"\n2. Bấm Khóa\n3. Mở một gói bảo dưỡng / báo giá dịch vụ cũ đang dùng "Cấp 1"', '',
              '- Khóa thành công, KHÔNG bị chặn vì đang được sử dụng\n- Chứng từ cũ vẫn hiển thị đúng tên "Cấp 1" (ở ô chọn của gói có biểu tượng ổ khóa)'),
             ('Mở khóa thành công', 'P0', '"Cấp khóa thử" đang Khóa, chưa dùng ở đâu.',
              '1. Chọn Mở khóa ở dòng "Cấp khóa thử"\n2. Đọc hộp xác nhận rồi bấm Mở khóa', '',
              '- Hộp tiêu đề "Mở khóa cấp dịch vụ", câu "Bạn có chắc muốn mở khóa cấp dịch vụ "Cấp khóa thử"?"\n- Báo "Mở khóa thành công", cột Trạng thái đổi thành Hoạt động\n- Nút Sửa và Xóa hiện lại'),
             ('Mở khóa cấp đang được sử dụng', 'P1', '"Cấp 1" đang Khóa và đang được dùng ở gói bảo dưỡng.',
              '1. Mở khóa "Cấp 1"\n2. Quan sát cột Hành động', '',
              '- "Cấp 1" về Hoạt động\n- Có Sửa, Khóa và Lịch sử, KHÔNG có nút Xóa'),
             ('Cấp đang Khóa không sửa, không xóa được trên giao diện', 'P0', _PRE,
              '1. Tìm dòng "Cấp khóa thử", quan sát cột Hành động\n2. Bấm vào tên "Cấp khóa thử"', '',
              '- Không có bút chì và thùng rác, chỉ có Mở khóa và Lịch sử\n- Cửa sổ "Xem cấp dịch vụ" vẫn mở được, ô Trạng thái hiện Khóa ở chế độ chỉ đọc'),
             ('Chặn sửa cấp đang Khóa khi bỏ qua giao diện', 'P1', _PRE,
              '1. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa "Cấp khóa thử"\n2. Mở lại màn hình', 'Đổi tên thành "Bị sửa khi khóa"',
              '- Hệ thống từ chối, báo "%s"\n- Tên cũ giữ nguyên' % MSG_LOCKED),
             ('Hai người cùng khóa một cấp', 'P1', 'Tài khoản A và B cùng mở danh sách; "Cấp thử" đang Hoạt động.',
              '1. A khóa "Cấp thử" thành công\n2. B (chưa tải lại trang) chọn Khóa ở dòng "Cấp thử", bấm Khóa', '',
              '- B nhận thông báo "%s"\n- Lịch sử của "Cấp thử" chỉ có MỘT mốc Khóa' % MSG_CONFLICT),
             ('Khóa / Mở khóa được ghi lịch sử', 'P0', 'Vừa khóa rồi mở khóa "Cấp thử".',
              '1. Mở Lịch sử của "Cấp thử"\n2. Đọc 2 dòng trên cùng', '',
              '- Có 2 mốc loại Thay đổi trạng thái: Hoạt động → Khóa và Khóa → Hoạt động\n- Kèm tên người thực hiện và thời điểm'),
             ('Cấp đã Khóa không chọn được khi tạo gói bảo dưỡng mới', 'P0', _PRE,
              '1. Mở màn Danh mục gói bảo dưỡng, bấm Tạo mới\n2. Mở ô chọn cấp dịch vụ', '',
              '- Danh sách chọn KHÔNG có "Cấp khóa thử"\n- Các cấp đang Hoạt động vẫn chọn được'),
             ('Gói cũ đang dùng cấp đã Khóa vẫn hiện đúng tên', 'P1', 'Gói bảo dưỡng G đang dùng "Cấp 1"; vừa khóa "Cấp 1".',
              '1. Mở Sửa gói G\n2. Quan sát ô cấp dịch vụ\n3. Bấm Lưu gói không đổi gì', '',
              '- Ô cấp hiện "Cấp 1" có biểu tượng ổ khóa phía trước, không bị trống, không tự đổi sang cấp khác\n- Lưu gói thành công, cấp vẫn giữ là "Cấp 1"'),
             ('Import gói bảo dưỡng dùng cấp đã Khóa', 'P1', '"Cấp khóa thử" đang Khóa.',
              '1. Ở màn Danh mục gói bảo dưỡng, Import file gói có cột Cấp bảo dưỡng = "Cấp khóa thử"\n2. Bấm Validate', 'Cấp bảo dưỡng: Cấp khóa thử',
              '- Dòng đó báo "Cấp bảo dưỡng "Cấp khóa thử" không có trong danh mục hoặc đã bị khóa"'),
             ('Báo giá dịch vụ không cho chọn gói theo cấp đã Khóa', 'P1', 'Hàng hóa H có gói bảo dưỡng G gắn "Cấp 1"; vừa khóa "Cấp 1".',
              '1. Tạo mới báo giá dịch vụ, thêm hàng hóa H\n2. Mở danh sách chọn gói bảo dưỡng của H', '',
              '- Không còn lựa chọn gói G với "Cấp 1"\n- Báo giá cũ đã có dòng "Cấp 1" vẫn hiển thị đúng'),
             ('Người chỉ có quyền Xem không thấy Khóa / Mở khóa', 'P0', 'Đăng nhập bằng tài khoản chỉ có quyền "Xem cấp dịch vụ bảo dưỡng".',
              '1. Mở màn hình, quan sát cột Hành động ở một dòng Hoạt động và một dòng Khóa', '',
              '- Cả hai dòng chỉ có nút Lịch sử; không có Khóa, Mở khóa, Sửa, Xóa\n- Vẫn thấy cột Trạng thái và lọc được theo Trạng thái'),
         ])]},
    ],
    'import_rows_dung': 'File mẫu điền 3 cấp hợp lệ, chưa có trong danh mục: DOC-Cấp 1 (6T) thử, DOC-Cấp 2 (12T) thử, DOC-Cấp 3 (36T/9000H) thử. Đăng nhập bằng tài khoản có quyền "Quản lý cấp dịch vụ bảo dưỡng"',
    'import_loi_data': {
        'Tên cấp không được để trống': 'Tên cấp: (để trống)',
        'Tên cấp tối đa 255 ký tự': 'Tên cấp: chuỗi 256 ký tự',
        'Tên cấp bị trùng với dòng N trong file': 'Hai dòng cùng tên “DOC-Cấp 1 (6T) thử”',
        'Tên cấp đã tồn tại trong hệ thống': 'Tên cấp: Cấp 1 (6T) (đã có trong danh mục)',
    },
    'import_extra': [
        ('Người chỉ có quyền Xem không thấy nút Import Excel', 'P0', 'Đăng nhập bằng tài khoản chỉ có quyền "Xem cấp dịch vụ bảo dưỡng".',
         '1. Mở màn hình\n2. Quan sát thanh công cụ', '', '- KHÔNG có nút Import Excel (và không có nút Tạo mới)\n- Vẫn có nút Xuất Excel'),
        ('Trùng tên khác chữ hoa thường', 'P1', 'Đã Load file có dòng Tên cấp “cấp 1 (6t)” (danh mục đã có “Cấp 1 (6T)”).',
         '1. Bấm Validate', 'Tên cấp: cấp 1 (6t)', '- Dòng đó báo “Tên cấp đã tồn tại trong hệ thống”'),
    ],
    'edits': [
        # --- Khối mô tả tính năng
        ('B3', '- Toàn bộ cấp dịch vụ trong danh mục, gồm CẢ cấp đang Hoạt động lẫn đang Khóa, KHÔNG phân theo công ty / phòng ban.\n- Bảng mặc định gồm 6 cột: STT, Tên cấp, Người tạo, Ngày tạo, Trạng thái, Hành động (Người cập nhật, Ngày cập nhật mặc định ẩn, bật ở Cấu hình cột).\n- Danh mục hiện có khoảng 29 cấp dịch vụ.'),
        ('B4', '- Không có cấp dịch vụ nào bị ẩn: danh sách hiện CẢ cấp Hoạt động lẫn cấp Khóa; ô Trạng thái để trống là xem cả hai.\n- Khi tìm theo tên hoặc chọn Trạng thái, các cấp không khớp bị loại khỏi kết quả.\n- Cấp đang Khóa không còn chọn được khi tạo gói bảo dưỡng mới, Import gói bảo dưỡng và chọn gói trong báo giá dịch vụ; chứng từ cũ đang dùng vẫn hiện đúng tên kèm biểu tượng ổ khóa.'),
        ('B6', 'Danh sách phẳng, không phân cấp cha- con.\n Tên cấp là giá trị duy nhất trong toàn danh mục (kể cả cấp đang Khóa).\n Quan hệ với màn khác: một cấp dịch vụ có thể được dùng ở 6 nơi — gói bảo dưỡng (cấp của gói), cấp bảo dưỡng của gói dịch vụ (bảng nội dung kiểm tra theo cấp), báo giá dịch vụ, hợp đồng dịch vụ, phiếu phân công công việc, phiếu nhập kết quả dịch vụ. Được dùng ở ít nhất 1 nơi thì coi là "đã sử dụng" — đây là căn cứ chặn XÓA (Khóa thì vẫn được).'),
        ('B8', 'Hai quyền dành riêng cho màn này:\n- "Xem cấp dịch vụ bảo dưỡng": vào màn hình, xem danh sách, tìm kiếm, lọc, mở xem chi tiết, xem lịch sử, xuất Excel.\n- "Quản lý cấp dịch vụ bảo dưỡng": thêm mới, sửa, xóa, khóa, mở khóa, Import Excel.\n Không có quyền nào trong hai quyền trên thì không vào được màn hình.\n Danh mục KHÔNG phân quyền theo công ty / phòng ban / bộ phận.'),
        ('B10', '- Màn có trạng thái Hoạt động / Khóa (bổ sung 28/09/2026): ô Trạng thái trong cửa sổ Tạo/Sửa (mặc định Hoạt động), cột Trạng thái, ô lọc Trạng thái và thao tác Khóa / Mở khóa ở cột Hành động.\n- Xóa là xóa HẲN. Nút Xóa CHỈ hiện với cấp đang Hoạt động VÀ chưa được sử dụng ở 6 nơi nêu ở mục 5; cấp đã sử dụng thì dùng Khóa. Nút Xóa bị ẨN hẳn, không có nút mờ.\n- Khóa được CẢ cấp đang được sử dụng. Cấp đang Khóa chỉ còn Mở khóa và Lịch sử; máy chủ cũng chặn sửa / xóa với câu "' + MSG_LOCKED + '"\n- Thông báo chặn xóa: "' + MSG_USED + '" (không còn liệt kê nơi đang dùng).\n  Ở hệ thống cũ, cấp dịch vụ chỉ bị chặn xóa khi được dùng ở gói bảo dưỡng — bản mới kiểm đủ 6 nơi. Đây là nhóm bắt buộc phải kiểm kỹ.\n- Bộ lọc được ghi nhớ trong 10 phút; kiểm thử tìm kiếm nên bấm Làm mới trước mỗi kịch bản.'),
        # --- Phân quyền
        ('I20', '- Có nút Tạo mới, nút Xuất Excel và nút Import Excel\n- Dòng đang Hoạt động có Sửa, Khóa, Lịch sử; nút Xóa chỉ hiện ở cấp đang Hoạt động và chưa được sử dụng (vd có ở "Cấp thử", không có ở "Cấp 1"). Dòng đủ 4 nút thì Khóa và Lịch sử nằm trong nút ba chấm\n- Dòng đang Khóa chỉ có Mở khóa và Lịch sử\n- Bấm vào tên cấp để mở cửa sổ Xem'),
        # --- I. Hiển thị
        ('I24', '- Tiêu đề trang và tiêu đề bảng đều là "Cấp dịch vụ bảo dưỡng"\n- Khu vực lọc có ô tìm nhanh (gợi ý "Tìm theo tên cấp dịch vụ...") và ô Trạng thái\n- Bảng mặc định có 6 cột: STT, Tên cấp, Người tạo, Ngày tạo, Trạng thái, Hành động\n- Có nút Tạo mới, Xuất Excel, Import Excel và biểu tượng Cấu hình cột hiển thị'),
        ('D26', 'Cột Trạng thái hiển thị Hoạt động / Khóa'),
        ('G26', '1. Mở màn hình\n2. Nhìn cột Trạng thái của "Cấp 1" và "Cấp khóa thử"'),
        ('I26', '- Có cột Trạng thái dạng nhãn: "Cấp 1" hiện Hoạt động, "Cấp khóa thử" hiện Khóa\n- Danh sách hiện CẢ cấp đang Khóa, không ẩn đi'),
        # --- IV. Thêm / sửa / xem
        ('I49', '- Mở cửa sổ tiêu đề "Tạo cấp dịch vụ"\n- Có 2 ô: Tên cấp (bắt buộc, có dấu sao đỏ) và Trạng thái (mặc định Hoạt động, chọn Hoạt động / Khóa)\n- Cuối cửa sổ có 3 nút: Lưu, Lưu và tiếp tục, Đóng'),
        # --- V. Xóa
        ('I61', '- Hộp xác nhận tiêu đề "Xác nhận xóa", câu "Bạn có chắc muốn xóa cấp dịch vụ "Cấp thử"?"\n- Bấm Xóa: báo "Xóa thành công", dòng biến mất, tổng dưới bảng giảm 1\n- Lọc Trạng thái = Khóa cũng KHÔNG thấy "Cấp thử" (xóa hẳn, không phải chuyển sang Khóa)'),
        ('I62', '- Hộp đóng, dòng "Cấp thử" vẫn còn nguyên, không có thông báo gì'),
        ('G63', '1. Mở màn hình, tìm dòng "Cấp 1"\n2. Quan sát cột Hành động'),
        ('I63', _HIDDEN_DEL),
        ('G64', '1. Mở màn hình, tìm dòng "Cấp HĐ"\n2. Quan sát cột Hành động'),
        ('I64', _HIDDEN_DEL),
        ('G65', '1. Mở màn hình, tìm dòng "Cấp BG"\n2. Quan sát cột Hành động'),
        ('I65', _HIDDEN_DEL),
        ('G66', '1. Mở màn hình, tìm dòng "Cấp PC"\n2. Quan sát cột Hành động'),
        ('I66', _HIDDEN_DEL),
        ('G67', '1. Mở màn hình, tìm dòng "Cấp NKQ"\n2. Quan sát cột Hành động'),
        ('I67', _HIDDEN_DEL),
        ('D68', 'Cấp đang Khóa KHÔNG có nút Xóa (kể cả chưa dùng ở đâu)'),
        ('F68', '"Cấp khóa thử" đang Khóa, chưa được sử dụng ở đâu.'),
        ('G68', '1. Chọn Trạng thái = Khóa\n2. Quan sát cột Hành động của dòng "Cấp khóa thử"\n3. Mở khóa "Cấp khóa thử", quan sát lại'),
        ('H68', 'Cấp khóa thử'),
        ('I68', '- Bước 2: chỉ có Mở khóa và Lịch sử; KHÔNG có Sửa, KHÔNG có Xóa\n- Bước 3: sau khi Mở khóa, nút Sửa và Xóa hiện lại'),
        ('G69', '1. Người 1 mở màn hình, dòng "Cấp thử" đang có nút Xóa\n2. Người 2 tạo báo giá dịch vụ dùng "Cấp thử"\n3. Người 1 (chưa tải lại trang) bấm Xóa dòng "Cấp thử" và bấm Xóa trong hộp xác nhận'),
        ('I69', '- Báo "' + MSG_USED + '"\n- "Cấp thử" vẫn còn trong danh sách\n- Tải lại trang: dòng "Cấp thử" không còn nút Xóa'),
        ('I71', '- Mỗi dòng chỉ có nút Lịch sử; KHÔNG có Sửa, Xóa, Khóa / Mở khóa'),
        # --- VI. Xuất Excel (thêm trường Trạng thái)
        ('I74', '- File có cột STT ở đầu, tiếp theo là đúng các cột đã tích theo thứ tự trên bảng: Tên cấp, Người tạo, Ngày tạo, Trạng thái\n- Tiêu đề cột bằng tiếng Việt giống trên màn hình, dữ liệu khớp với bảng'),
        ('I79', '- Mở cửa sổ “Chọn trường xuất file”\n- Có đủ 6 trường: Tên cấp, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật\n- Tích sẵn đúng các cột đang hiển thị trên bảng, xếp lên đầu theo thứ tự trên bảng: Tên cấp, Người tạo, Ngày tạo, Trạng thái\n- Dòng cuối ghi “Đang chọn 4/6 trường”'),
        ('I82', '- Bỏ chọn hết: không trường nào được tích, nút Xuất file không bấm được\n- Chọn tất cả: tích đủ 6 trường, dòng cuối “Đang chọn 6/6 trường”'),
        # --- VIII. Luồng xuyên suốt
        ('G101', '1. Tạo mới cấp "Cấp kiểm thử"\n2. Tạo một báo giá dịch vụ dùng cấp đó\n3. Quay lại màn hình, tải lại danh sách, quan sát cột Hành động của cấp đó'),
        ('I101', '- Bước 3: KHÔNG còn nút Xóa (vẫn có Sửa, Khóa, Lịch sử)\n- Cấp vẫn còn trong danh mục; muốn ngừng dùng thì Khóa'),
        # --- IX. Import (bản ghi import ở trạng thái Hoạt động)
        ('I117', '- Báo “Import thành công N cấp dịch vụ bảo dưỡng.”\n- Cửa sổ đóng, danh sách tải lại có cấp dịch vụ mới ở trạng thái Hoạt động'),
    ],
    'clear_k': [20, 24, 26, 49, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 74, 79, 82, 101, 117],
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
    'fr_sua': 'Chỉnh sửa cấp dịch vụ', 'fr_xoa': 'Xóa cấp dịch vụ', 'fr_khoa': 'Khóa / Mở khóa cấp dịch vụ',
    'fr_ls': 'Xem lịch sử thay đổi', 'fr_import': 'Import file cấp dịch vụ', 'fr_xuat': 'Xuất danh sách cấp dịch vụ ra Excel',
    'fr_xem': 'Xem chi tiết cấp dịch vụ', 'fr_cot': 'Tùy chỉnh cột hiển thị',
    'nhan_ban_ghi': 'tên cấp', 'nhan_cot': 'Tên cấp',
    'tieu_de_sua': 'Sửa cấp dịch vụ', 'tieu_de_xem': 'Xem cấp dịch vụ',
    'sua_hien': 'Chỉ hiện khi Người dùng có quyền Quản lý VÀ cấp đang Hoạt động.',
    'truong_sua': [
        ('Tên cấp', 'Textbox', '1–255 ký tự', 'Có',
         'Duy nhất toàn danh mục (kể cả cấp đang Khóa), bỏ qua chính bản ghi đang sửa; khoảng trắng đầu cuối tự cắt. Bỏ trống “Bắt buộc phải nhập”; trùng “Tên cấp đã tồn tại”; quá dài “Vui lòng nhập tối đa 255 ký tự.”'),
        ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Không',
         'Luôn có giá trị, không xóa trống được. Chọn Khóa rồi Lưu là khóa cấp ngay trong cửa sổ Sửa; lịch sử ghi mốc “Thay đổi trạng thái” riêng.'),
    ],
    'xoa_hien': 'Chỉ hiện khi Người dùng có quyền Quản lý, cấp đang Hoạt động VÀ chưa được sử dụng ở đâu.',
    'xoa_tieu_de': 'Xác nhận xóa', 'xoa_cau': 'Bạn có chắc muốn xóa cấp dịch vụ "<tên cấp>"?',
    'khoa_hien': 'Chỉ hiện với quyền Quản lý. Cấp đang Hoạt động hiện “Khóa”, cấp đang Khóa hiện “Mở khóa” (khóa được cả cấp đang được sử dụng).',
    'khoa_tieu_de': '“Khóa cấp dịch vụ” hoặc “Mở khóa cấp dịch vụ” theo thao tác.',
    'khoa_cau': '“Bạn có chắc muốn khóa cấp dịch vụ "<tên cấp>"?” / “Bạn có chắc muốn mở khóa cấp dịch vụ "<tên cấp>"?”.',
    'truong_ls': 'Tên cấp, Trạng thái',
    'quyen_import': 'quyền Quản lý', 'import_tieu_de': 'Import cấp dịch vụ bảo dưỡng',
    'import_file': 'Mau_import_cap_dich_vu_bao_duong.xlsx', 'import_cot': 'STT, Tên cấp', 'import_cot_bang': 'STT, Tên cấp',
    'doi_tuong_import': 'cấp dịch vụ', 'import_toast': 'Import thành công N cấp dịch vụ bảo dưỡng.',
    'import_toast_loi': 'Import thành công x/y cấp dịch vụ bảo dưỡng. N dòng thất bại.',
    'xuat_hien': 'Hiện với cả người chỉ có quyền Xem.',
    'xuat_truong': 'Sáu trường: Tên cấp, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật', 'xuat_so': 6,
    'xuat_theo': 'từ khóa, Trạng thái và thứ tự sắp xếp', 'xuat_file': 'cap_dich_vu_bao_duong.xlsx',
    'truong_xem': [('Tên cấp', 'Textbox', 'Ô mờ, không gõ được.'),
                   ('Trạng thái', 'Dropdown', 'Hoạt động hoặc Khóa, không đổi được.')],
    'cot_all': ['STT', 'Tên cấp', 'Người tạo', 'Ngày tạo', 'Người cập nhật', 'Ngày cập nhật', 'Trạng thái', 'Hành động'],
    'cot_mac_dinh': 'STT, Tên cấp, Người tạo, Ngày tạo, Trạng thái, Hành động',
    'cot_khoa': 'STT, Tên cấp, Hành động',
})
