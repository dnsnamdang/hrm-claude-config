# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu chi tiền" (bản Drive 28/10) theo FORM "Danh mục quốc gia" (TPE Pass) — STT 161.

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu chi tiền.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Khuôn chép từ màn 27 (finance-product-import-direct-transfer/form_qg/patch_srs.py). Luôn đọc bản Drive gốc.
Đối chiếu code: hrm-client/pages/finance/bill-payments/*, hrm-api Modules/Finance (BillPayment*).
"""
import os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
import docx  # noqa: E402
from formqg_lib import *  # noqa: E402,F401
import formqg_lib as L  # noqa: E402
import docxlib  # noqa: E402

SRC = os.path.join(HERE, 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
OUT = os.path.join(OUT_DIR, 'SRS - Phiếu chi tiền.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu chi tiền'
# finance.js: hubGroup 'Quản lý tiền' > nhóm 'Thanh toán tiền mặt' > mục 'Phiếu chi'
MENU = 'Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu chi'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
              'bấm Thoát thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem tất cả phiếu chi của tổng công ty (V1) / Xem tất '
              'cả phiếu chi của công ty (V2); không có quyền nào thì chỉ thấy phiếu do mình lập.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1, V2); không có quyền nào vẫn xem được phiếu do chính mình lập.')
ACTOR_Q1 = 'Người dùng có quyền Kế toán thanh toán (Q1).'
ACTOR_OWNER = 'Người lập phiếu có quyền Kế toán thanh toán (Q1).'
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu và có quyền Kế toán thanh toán (Q1).\n'
              '3. Phiếu đang ở trạng thái Đang tạo.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu; người đã duyệt phiếu; người có quyền V1; người có '
               'quyền V2 cùng công ty với phiếu; người có quyền duyệt (Q2 / Q3) cùng công ty khi phiếu đang chờ '
               'đúng cấp duyệt của mình.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu Đang tạo chỉ người lập xem được.')
ACTOR_APPROVE = ('Người dùng có quyền Kế toán trưởng duyệt phiếu chi (Q2) — cấp 1, chỉ với loại Chi thu nhập cho '
                 'nhân viên; hoặc quyền Thủ quỹ duyệt phiếu chi (Q3) — cấp cuối. Bắt buộc cùng công ty với phiếu.')
COND_APPROVE = ('1. Đăng nhập thành công.\n'
                '2. Có quyền Q2 (phiếu Chờ KT trưởng duyệt) hoặc Q3 (phiếu Chờ chi tiền) và cùng công ty với phiếu.\n'
                '3. Phiếu đang ở trạng thái Chờ KT trưởng duyệt hoặc Chờ chi tiền.')

SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST,
                COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.3 ': ('Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.', ACTOR_LIST,
                COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.4 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_Q1,
                '1. Đăng nhập thành công.\n2. Có quyền Kế toán thanh toán (Q1).'),
    r'^2\.5 ': ('Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.', ACTOR_Q1,
                '1. Đăng nhập thành công.\n2. Có quyền Kế toán thanh toán (Q1).\n'
                '3. Đang ở màn Tạo mới hoặc Chỉnh sửa phiếu chi, Loại chi thuộc luồng lập từ Đề nghị thanh toán.'),
    r'^2\.6 ': ('Màn Thêm mới, Validate dữ liệu và UI/UX.', ACTOR_Q1,
                '1. Đăng nhập thành công.\n2. Có quyền Kế toán thanh toán (Q1).\n'
                '3. Đang ở màn Tạo mới hoặc Chỉnh sửa phiếu chi, Loại chi = Chi thu nhập cho nhân viên.'),
    r'^2\.7 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.8 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.9 ': ('Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.', ACTOR_APPROVE, COND_APPROVE),
    r'^2\.10 ': ('Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.', ACTOR_APPROVE, COND_APPROVE),
    r'^2\.11 ': ('Quy tắc xóa và Thông báo.', ACTOR_OWNER, COND_OWNER),
    r'^2\.12 ': ('Quy tắc màn In và bố cục bản in.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.13 ': ('Quy tắc Excel.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.14 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

MENU_LINES = {
    r'^2\.1 ': ('Menu: %s' % MENU, None),
    r'^2\.2 ': ('Menu: %s => Tìm kiếm nâng cao' % MENU, None),
    r'^2\.3 ': ('Menu: %s => Cài đặt bộ lọc / Tùy chỉnh cột' % MENU,
                'Modal Cài đặt bộ lọc và Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.4 ': ('Menu: %s => Tạo mới' % MENU,
                'Modal Xác nhận lưu và gửi duyệt được mở ngay trên màn hình Tạo mới phiếu chi theo đường dẫn ở trên.'),
    r'^2\.5 ': ('Menu: %s => Tạo mới / Chỉnh sửa => Số phiếu đề nghị' % MENU,
                'Modal Chọn phiếu đề nghị chi được mở ngay trên màn hình Tạo mới hoặc Chỉnh sửa phiếu chi theo '
                'đường dẫn ở trên.'),
    r'^2\.6 ': ('Menu: %s => Tạo mới / Chỉnh sửa => Loại chi “Chi thu nhập cho nhân viên” => Phòng ban chi' % MENU,
                'Bảng thu nhập nhân viên hiển thị ngay trên màn hình Tạo mới hoặc Chỉnh sửa phiếu chi sau khi chọn '
                'Phòng ban chi.'),
    r'^2\.7 ': ('Menu: %s => Sửa (trên dòng phiếu) / Xem chi tiết => Sửa' % MENU, None),
    r'^2\.8 ': ('Menu: %s => bấm Mã phiếu' % MENU, None),
    r'^2\.9 ': ('Menu: %s => Xem chi tiết => Duyệt phiếu chi' % MENU,
                'Modal Duyệt phiếu chi tiền (loại Chi thu nhập cho nhân viên: Modal Duyệt phiếu chi thu nhập nhân '
                'viên) và Modal Xác nhận duyệt được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.10 ': ('Menu: %s => Xem chi tiết => Hủy phiếu chi' % MENU,
                 'Modal Hủy phiếu chi tiền được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.11 ': ('Menu: %s => Xóa (trên dòng phiếu) / Xem chi tiết => Xóa' % MENU,
                 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa trên dòng) hoặc màn hình '
                 'chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.12 ': ('Menu: %s => In (trên dòng phiếu) / Xem chi tiết => In' % MENU,
                 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo '
                 'đường dẫn ở trên.'),
    r'^2\.13 ': ('Menu: %s => Xuất Excel (trên dòng phiếu) / Xem chi tiết => Xuất Excel' % MENU, None),
    r'^2\.14 ': ('Menu: %s => Lịch sử (trên dòng phiếu) / Xem chi tiết => Xem lịch sử' % MENU,
                 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử '
                 'thay đổi nằm cuối màn hình chi tiết phiếu.'),
}

USECASES = {
    r'^2\.4 ': ('Kế toán thanh toán', 'FR-04', 'Tạo mới phiếu chi', 'crud'),
    r'^2\.5 ': ('Kế toán thanh toán', 'FR-05', 'Chọn phiếu đề nghị thanh toán', 'crud'),
    r'^2\.6 ': ('Kế toán thanh toán', 'FR-06', 'Lấy số liệu thu nhập nhân viên', 'crud'),
    r'^2\.7 ': ('Người lập phiếu', 'FR-07', 'Sửa phiếu chi', 'crud'),
    r'^2\.8 ': ('Người dùng có quyền', 'FR-08', 'Xem chi tiết phiếu chi', 'view'),
    r'^2\.9 ': ('KT trưởng / Thủ quỹ', 'FR-09', 'Duyệt phiếu chi', 'action'),
    r'^2\.10 ': ('KT trưởng / Thủ quỹ', 'FR-10', 'Hủy phiếu chi', 'action'),
    r'^2\.11 ': ('Người lập phiếu', 'FR-11', 'Xóa phiếu chi', 'action'),
    r'^2\.12 ': ('Người dùng có quyền', 'FR-12', 'In phiếu chi', 'io'),
    r'^2\.13 ': ('Người dùng có quyền', 'FR-13', 'Xuất Excel một phiếu', 'io'),
}

# Ảnh cũ -> ảnh chụp mới trên dev (dùng chung bộ ảnh HDSD). Khóa = đoạn đầu chú thích Hình.
NEW_IMAGES = {
    'Màn Danh sách phiếu chi lúc mới truy cập': '01_list',
    'Khối Tìm kiếm nâng cao khi đang mở': '02_filter',
    'Danh sách sau khi cuộn ngang': '01b_list_actions',
    'Cửa sổ Cài đặt bộ lọc': '26_filtercfg',
    'Cửa sổ Tùy chỉnh cột hiển thị': '25_colcfg',
    'Màn Thêm phiếu chi tiền khi vừa mở': '10_create',
    'Luồng lập từ Đề nghị thanh toán': '12_create_request',
    'Luồng Chi thu nhập cho nhân viên': '14_employee_form',
    'Cửa sổ Chọn phiếu đề nghị chi': '11_request',
    'Bảng thu nhập nhân viên sau khi chọn': '15_employee_table',
    'Màn Sửa phiếu chi tiền': '16_edit',
    'Màn chi tiết phiếu đang Chờ chi tiền': '17_detail',
    'Màn chi tiết phiếu đã hủy': '22_detail_cancel',
    'Cửa sổ Duyệt phiếu chi tiền': '18_approve',
    'Cửa sổ Hủy phiếu chi tiền': '21_cancel',
    'Lỗi khi bấm Xác nhận lúc chưa nhập lý do hủy': '21b_cancel_error',
    'Hộp xác nhận xóa phiếu chi': '20_delete',
    'Cửa sổ Lịch sử thay đổi mở từ màn danh sách': '24_history',
    'Khối Lịch sử ở cuối màn chi tiết': '24b_history_detail',
}
NEW_CAPTIONS = {
    'Cửa sổ Duyệt phiếu chi tiền': 'Cửa sổ Duyệt phiếu chi tiền (luồng lập từ Đề nghị thanh toán)',
    'Màn chi tiết phiếu đang Chờ chi tiền': 'Màn chi tiết phiếu đang Chờ chi tiền — đủ nút Sửa, Duyệt phiếu chi, '
                                            'Hủy phiếu chi, In, Xuất Excel, Xóa',
    'Bản in phiếu chi loại Chi thu nhập': 'Cửa sổ Xem trước bản in phiếu chi',
    'Nút Xuất Excel trên thanh nút cuối': 'Nút Xuất Excel trên thanh nút cuối màn chi tiết',
}

# Câu chữ kỹ thuật -> nghiệp vụ, và chỗ lệch code. (regex dòng, dòng mới | None = bỏ dòng). Áp mọi ô + đoạn.
LINE_FIX = [
    # ---- Phần 2
    (r'^Lập, sửa, xoá, gửi duyệt phiếu chi; mở được cửa sổ chọn phiếu đề nghị và endpoint',
     'Lập, sửa, xoá, gửi duyệt phiếu chi; mở được cửa sổ chọn phiếu đề nghị và lấy được số liệu thu nhập nhân '
     'viên. Hệ thống kiểm tra quyền ngay khi lưu, không dựa vào việc giao diện ẩn nút.'),
    (r'^So sánh công ty: hai vế cùng rỗng',
     'So sánh công ty: phiếu chưa xác định công ty và người dùng chưa gắn công ty KHÔNG được coi là cùng công '
     'ty. Hệ thống cũ coi hai trường hợp này là cùng công ty — lỗ hổng đã được bịt.'),
    # ---- 2.1
    (r'^1\. Người dùng vào menu Tài chính', '1. Người dùng vào menu %s.' % MENU),
    (r'^Luôn hiển thị, không gắn cờ quyền ở giao diện; quyền Q1 chặn ở phía máy chủ\.',
     'Luôn hiển thị; người không có quyền Q1 bấm lưu sẽ bị từ chối.'),
    (r'^Là đường dẫn sang màn chi tiết Đề nghị thanh toán\. Loại Chi thu nhập',
     'Bấm mã mở màn chi tiết Đề nghị thanh toán ở TAB MỚI. Loại Chi thu nhập cho nhân viên không có phiếu đề '
     'nghị nên ô để trống.'),
    (r'^Đối tượng nhận tiền của dòng chi tiết đầu tiên; không có thì hiện dấu gạch ngang\.',
     'Mã và tên đối tượng nhận tiền của dòng chi tiết đầu tiên; không có thì để trống.'),
    (r'^Nhãn xám với Đang tạo, vàng với hai trạng thái chờ duyệt',
     'Nhãn màu theo trạng thái: Đang tạo, Chờ KT trưởng duyệt, Chờ chi tiền, Đã duyệt, Hủy. Sắp xếp được.'),
    (r'^– Chỉ nhận các cột nằm trong danh sách cho phép sắp xếp\.',
     '– Chỉ nhận năm cột: Mã phiếu, Số tiền, Ngày tạo, Ngày cập nhật, Trạng thái.'),
    (r'^– Điều hướng sang màn chi tiết Đề nghị thanh toán tương ứng\.',
     '– Mở TAB MỚI sang màn chi tiết Đề nghị thanh toán; tab hiện tại giữ nguyên bộ lọc và trang đang xem.'),
    # ---- 2.2
    (r'^• Tham số lạ thêm vào đường dẫn', None),
    # ---- 2.4
    (r'^6\. Hệ thống khóa dòng phiếu đề nghị, kiểm tra chưa có phiếu chi nào',
     ['6. Hệ thống kiểm tra phiếu đề nghị chưa có phiếu chi nào (hai người lưu cùng lúc cũng chỉ một người thành '
      'công), sinh mã tự động và ghi phiếu cùng các dòng chi tiết.']),
    (r'^7\. Nếu gửi duyệt: phiếu chuyển sang trạng thái chờ duyệt tương ứng luồng',
     ['7. Nếu gửi duyệt: phiếu chuyển sang trạng thái chờ duyệt tương ứng luồng và hệ thống gửi thông báo cho '
      'cấp duyệt đó trong cùng công ty.',
      '8. Ghi nhận hành động Tạo mới (kèm đổi trạng thái nếu gửi duyệt) trong lịch sử của phiếu.',
      '9. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.']),
    (r'^• Lưu nháp: KHÔNG bắt buộc trường nào ngoài Loại chi; các rule định dạng vẫn áp\.',
     '• Lưu nháp: KHÔNG bắt buộc trường nào ngoài Loại chi; các kiểm tra định dạng vẫn áp.'),
    (r'^• Phiếu đề nghị đã có phiếu chi khác → bị chặn',
     '• Phiếu đề nghị đã có phiếu chi khác → báo “Đề nghị thanh toán đã lập phiếu chi tiền.”, không tạo phiếu thứ hai.'),
    (r'^• Bấm Quay lại khi đã nhập dở → hỏi xác nhận rời trang\.', UNSAVED),
    (r'^Hai điểm KHÁC hệ thống cũ có chủ đích: \(1\) lưu nháp',
     'Hai điểm KHÁC hệ thống cũ có chủ đích: (1) lưu nháp không bắt buộc trường nào ngoài Loại chi — hệ thống cũ '
     'áp cùng một bộ luật cho cả hai nút; (2) số tiền chi bị kiểm trần “không vượt số tiền đề nghị chi” ngay ở '
     'bước lưu (cả Lưu nháp lẫn Lưu và gửi duyệt) — hệ thống cũ tự kéo số về bằng số đề nghị nên người dùng '
     'không hiểu vì sao số tự nhảy. Mở màn Tạo mới từ màn Đề nghị thanh toán (nút Tạo phiếu chi trên phiếu đề '
     'nghị) thì form nạp sẵn phiếu đề nghị đó và không có nút Lưu và tiếp tục.'),
    (r'^– Số tiền chi vượt số tiền đề nghị chi của dòng → “Không được lớn hơn số tiền đề nghị chi”\.', None),
    (r'^– Kiểm tra quyền Q1; không có quyền → hiển thị “Bạn không có quyền lập phiếu chi tiền” và dừng xử lý\.',
     ['– Kiểm tra quyền Q1; không có quyền → hiển thị “Bạn không có quyền lập phiếu chi tiền” và dừng xử lý.',
      '– Áp cho CẢ Lưu nháp lẫn Lưu và gửi duyệt: dòng có Số tiền chi lớn hơn Số tiền đề nghị chi → báo '
      '“Không được lớn hơn số tiền đề nghị chi ({số đề nghị})” dưới ô và thông báo “Số tiền chi ở dòng {n} đang '
      'lớn hơn số tiền đề nghị chi”, không lưu.',
      '– Luồng Chi thu nhập nhân viên: tổng 6 khoản chi của một nhân viên khác Số tiền chi của dòng → thông báo '
      '“Tổng số tiền chi theo mã vụ việc và tổng số tiền đề nghị chi khác nhau!”; một khoản chi vượt số dư (so '
      'theo giá trị tuyệt đối) → “Số tiền chi không được vượt quá số dư!”.']),
    (r'^– Với Lưu và gửi duyệt: mở hộp xác nhận, chỉ tiếp tục khi người dùng đồng ý\.',
     '– Với Lưu và gửi duyệt: mở hộp xác nhận “Xác nhận lưu và gửi duyệt”, chỉ tiếp tục khi người dùng đồng ý.'),
    (r'^– Khóa dòng phiếu đề nghị rồi kiểm tra chưa có phiếu chi nào; đã có thì chặn và dừng\.',
     '– Kiểm tra phiếu đề nghị chưa có phiếu chi nào (kể cả khi hai người lưu cùng lúc); đã có thì hiển thị '
     '“Đề nghị thanh toán đã lập phiếu chi tiền.” và dừng.'),
    (r'^– Sinh mã phiếu tự động \(có khóa dòng',
     '– Sinh mã phiếu tự động (hai người lưu cùng lúc không bị trùng mã), ghi phiếu và các dòng chi tiết.'),
    (r'^– Hiển thị “Thêm phiếu chi tiền thành công!” và quay về danh sách\.',
     '– Hiển thị “Thêm phiếu chi tiền thành công!” (Lưu nháp) hoặc “Phiếu chi tiền cần được duyệt trước khi có '
     'hiệu lực, vui lòng theo dõi thông báo” (Lưu và gửi duyệt), rồi quay về danh sách. Lưu và tiếp tục: lưu '
     'nháp rồi mở lại màn Tạo mới trống.'),
    # ---- 2.5
    (r'^Cửa sổ này CỐ Ý không áp phạm vi xem của màn Đề nghị thanh toán',
     'Cửa sổ này CỐ Ý không áp phạm vi xem của màn Đề nghị thanh toán — mọi kế toán thanh toán đều chọn được mọi '
     'phiếu đề nghị đủ điều kiện, và lấy dữ liệu phiếu đã chọn về form cũng chỉ cần quyền Q1.'),
    (r'^• Bấm Đóng → cửa sổ đóng, ô Số phiếu đề nghị giữ nguyên giá trị cũ\.',
     '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận; ô Số phiếu đề nghị giữ '
     'nguyên giá trị cũ.'),
    (r'^– Kiểm tra quyền Q1 một lần nữa ở endpoint kéo dữ liệu',
     '– Kiểm tra quyền Q1 một lần nữa khi lấy dữ liệu phiếu đề nghị; thiếu quyền → “Bạn không có quyền xem phiếu '
     'đề nghị chi”.'),
    # ---- 2.7
    (r'^• Không thỏa điều kiện sửa → từ chối và đưa về danh sách\.',
     '• Không thỏa điều kiện sửa → từ chối với thông báo “Bạn không có quyền sửa phiếu chi.” (thiếu quyền Q1) '
     'hoặc “Phiếu chi đã bị khóa, không sửa được.” (phiếu không còn Đang tạo hoặc không phải người lập).'),
    (r'^• Bấm Quay lại khi đã sửa dở → hỏi xác nhận rời trang\.', UNSAVED),
    (r'^ĐIỂM SIẾT CHẶT HƠN HỆ THỐNG CŨ: hệ thống cũ chỉ kiểm trạng thái',
     'ĐIỂM SIẾT CHẶT HƠN HỆ THỐNG CŨ: hệ thống cũ chỉ kiểm trạng thái nên người khác vẫn sửa được phiếu nháp không '
     'phải của mình. Quản trị hệ thống CỐ Ý không được miễn trừ ở chức năng này — miễn trừ chỉ áp cho việc XEM. '
     'Màn Sửa có thêm ba ô chỉ đọc: Mã phiếu, Người lập, Ngày lập; không có nút Lưu và tiếp tục.'),
    (r'^6\. Hệ thống ghi một dòng lịch sử chỉnh sửa và một dòng lịch sử đổi trạng thái nếu trạng thái thay đổi\.',
     ['6. Ghi nhận thay đổi trong lịch sử của phiếu (thêm một dòng đổi trạng thái nếu gửi duyệt).',
      '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.']),
    (r'^Mở màn Sửa và nạp dữ liệu đã lưu, kèm tài khoản đã khóa|^– Mở màn Sửa và nạp dữ liệu đã lưu, kèm tài khoản đã khóa',
     '– Mở màn Sửa và nạp dữ liệu đã lưu, kèm tài khoản đã khóa (nếu có) để ô chọn vẫn hiện đúng tên.'),
    (r'^– Kiểm tra lại ở phía máy chủ; không thoả → từ chối và đưa về danh sách\.',
     '– Hệ thống kiểm tra lại điều kiện; không thoả → từ chối và đưa về danh sách.'),
    (r'^– Kiểm tra lại đủ ba điều kiện sửa ở phía máy chủ\.', '– Hệ thống kiểm tra lại đủ ba điều kiện sửa.'),
    (r'^– Khóa dòng phiếu đề nghị và kiểm tra ràng buộc một phiếu đề nghị một phiếu chi',
     '– Kiểm tra ràng buộc một phiếu đề nghị một phiếu chi, bỏ qua chính phiếu đang sửa.'),
    (r'^– Ghi một dòng lịch sử chỉnh sửa; nếu trạng thái đổi thì ghi thêm',
     '– Ghi nhận thay đổi theo từng trường trong lịch sử; nếu gửi duyệt thì ghi thêm một dòng đổi trạng thái '
     'bằng TÊN trạng thái.'),
    (r'^– Hiển thị “Cập nhật phiếu chi tiền thành công!” và quay về danh sách\.',
     '– Hiển thị “Cập nhật phiếu chi tiền thành công!” (Lưu nháp) hoặc “Phiếu chi tiền cần được duyệt trước khi '
     'có hiệu lực, vui lòng theo dõi thông báo” (Lưu và gửi duyệt), rồi quay về danh sách.'),
    # ---- 2.8
    (r'^4\. Hệ thống hiển thị nội dung và tính các cờ quyết định 7 nút thao tác\.',
     '4. Hệ thống hiển thị nội dung và các nút thao tác theo trạng thái phiếu và quyền người xem.'),
    (r'^• Phiếu đã hủy → hiện thêm dải băng ở đầu màn với Lý do hủy và Ghi chú\.',
     '• Phiếu đã hủy, hoặc người duyệt có ghi chú → hiện thêm dải băng ở đầu màn với Lý do hủy, Ghi chú, Ghi chú '
     'của người duyệt.'),
    (r'^Bảy cờ quyền \(xem',
     'Điều kiện hiện các nút Sửa, Xóa, Duyệt phiếu chi, Hủy phiếu chi, In, Xuất Excel được xác định ở một nơi và '
     'dùng chung cho màn danh sách lẫn màn chi tiết, nên với cùng một phiếu hai màn luôn hiện cùng bộ nút.'),
    (r'^– Hiển thị nội dung và tính 7 cờ quyền quyết định các nút thao tác\.',
     '– Hiển thị nội dung và các nút thao tác theo trạng thái phiếu và quyền người xem.'),
    (r'^CHỈ hiện với phiếu đã hủy; nền vàng, hiện Lý do hủy và Ghi chú của người duyệt\.',
     'Hiện khi phiếu có Lý do hủy, Ghi chú khi hủy hoặc Ghi chú của người duyệt; nền vàng, nằm đầu màn.'),
    # ---- 2.9
    (r'^2\. Bấm nút Duyệt phiếu chi; hệ thống mở cửa sổ hiện lại bảng chi tiết',
     '2. Bấm nút Duyệt phiếu chi; hệ thống mở cửa sổ Duyệt phiếu chi tiền (loại Chi thu nhập cho nhân viên: Duyệt '
     'phiếu chi thu nhập nhân viên) hiện lại bảng chi tiết với cột Số tiền thực chi là ô nhập.'),
    (r'^4\. Bấm Duyệt\. Hệ thống khóa dòng phiếu, kiểm tra chưa duyệt rồi mới kiểm quyền\.',
     '4. Bấm Duyệt, rồi bấm Duyệt ở hộp “Xác nhận duyệt”. Hệ thống kiểm tra phiếu chưa được duyệt rồi mới kiểm '
     'tra quyền.'),
    (r'^6\. Hệ thống ghi lịch sử và hiển thị “Duyệt phiếu chi thành công!”\.',
     ['6. Ghi nhận hành động Duyệt (kèm ghi chú của người duyệt) trong lịch sử của phiếu.',
      '7. Hệ thống hiển thị “Duyệt phiếu chi thành công!” và quay về màn danh sách.']),
    (r'^• Số tiền thực chi vượt trần → từ chối, không ghi bút toán nào\.',
     '• Số tiền thực chi vượt trần → giao diện báo “Không được lớn hơn số tiền đề nghị chi ({số})” dưới ô; hệ '
     'thống kiểm lại và báo “Số tiền chi không được vượt quá số dư!”, không ghi bút toán nào.'),
    (r'^• Toàn bộ bước ghi nằm trong một giao dịch',
     ['• Các bước ghi khi duyệt thực hiện trọn vẹn cùng nhau: lỗi ở bất kỳ bước nào thì phiếu giữ nguyên, không có '
      'bút toán nào được ghi.',
      '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận; phiếu giữ nguyên.',
      '• Bấm Hủy ở hộp Xác nhận duyệt → quay lại cửa sổ Duyệt, chưa duyệt.']),
    (r'^Bước Thủ quỹ KHÔNG HOÀN TÁC ĐƯỢC\. Hai điểm KHÁC hệ thống cũ',
     'Bước Thủ quỹ KHÔNG HOÀN TÁC ĐƯỢC. Hai điểm KHÁC hệ thống cũ: (1) hệ thống cũ duyệt hai lần là nhân đôi bút '
     'toán trong sổ kế toán, nay lần duyệt sau bị chặn; (2) hệ thống cũ KHÔNG kiểm trần số tiền lúc duyệt, nay có '
     'kiểm. Kiểm tra “phiếu đã duyệt” đứng TRƯỚC kiểm tra quyền, để người vừa duyệt xong không nhận thông báo '
     'thiếu quyền sai sự thật.'),
    (r'^Có dấu sao đỏ\. Với luồng Chi thu nhập nhân viên, trần so theo giá trị tuyệt đối của số dư\.',
     'Có dấu sao đỏ. Gõ quá Số tiền đề nghị chi → báo “Không được lớn hơn số tiền đề nghị chi ({số})” dưới ô và '
     'chặn duyệt. Loại Chi thu nhập cho nhân viên: bảng gồm Nhân viên, 6 khoản Số tiền đề nghị chi, 6 khoản Số '
     'tiền thực chi và Tổng cộng; trần so theo giá trị tuyệt đối của số dư.'),
    (r'^– KHÓA DÒNG phiếu rồi mới đọc trạng thái\.',
     ['– Hiện hộp “Xác nhận duyệt” (“Bạn có chắc muốn duyệt phiếu chi \"{mã phiếu}\"?”), chỉ tiếp tục khi bấm Duyệt.',
      '– Đọc lại trạng thái mới nhất của phiếu (hai người duyệt cùng lúc chỉ một người thành công).']),
    (r'^– Số tiền thực chi vượt trần của dòng → từ chối với thông báo số tiền chi không được vượt quá số dư',
     '– Số tiền thực chi vượt trần của dòng → giao diện báo “Không được lớn hơn số tiền đề nghị chi ({số})” dưới '
     'ô; hệ thống kiểm lại và báo “Số tiền chi không được vượt quá số dư!”. Luồng Chi thu nhập nhân viên so '
     'theo giá trị tuyệt đối của số dư.'),
    (r'^– Số tiền thực chi âm → “Số tiền chi không được âm”\.', '– Số tiền thực chi âm → “Số tiền thực chi – Không được âm”.'),
    (r'^– Ghi một dòng log riêng', None),
    (r'^– Ghi lịch sử và hiển thị “Duyệt phiếu chi thành công!”\.',
     ['– Ghi nhận hành động Duyệt (thay đổi số tiền thực chi + đổi trạng thái, kèm ghi chú) trong lịch sử của phiếu.',
      '– Hiển thị “Duyệt phiếu chi thành công!” và quay về màn danh sách.']),
    (r'^– Gửi thông báo cho Thủ quỹ cùng công ty\.',
     ['– Gửi thông báo cho Thủ quỹ cùng công ty.',
      '– Ghi nhận hành động Duyệt cấp Kế toán trưởng (kèm ghi chú) trong lịch sử của phiếu.']),
    # ---- 2.10
    (r'^4\. Hệ thống khóa dòng phiếu, kiểm tra lại quyền\.',
     '4. Hệ thống kiểm tra lại quyền hủy theo trạng thái mới nhất của phiếu.'),
    (r'^5\. Hệ thống chuyển phiếu sang Hủy và ghi một dòng lịch sử kèm lý do hủy và ghi chú\.',
     ['5. Hệ thống chuyển phiếu sang Hủy.',
      '6. Ghi nhận hành động Hủy kèm lý do hủy và ghi chú trong lịch sử của phiếu.',
      '7. Hệ thống hiển thị “Hủy phiếu chi thành công!” và quay về màn danh sách.']),
    (r'^• Lý do hủy để trống → hiển thị “Vui lòng nhập lý do hủy phiếu chi\.”',
     '• Lý do hủy để trống → hiển thị “Lý do hủy – Bắt buộc nhập” dưới ô; cửa sổ không đóng.'),
    (r'^• Bấm Đóng → cửa sổ đóng, phiếu giữ nguyên trạng thái\.',
     '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận kể cả khi đã nhập lý do; '
     'phiếu giữ nguyên trạng thái.'),
    (r'^Người lập CỐ Ý không được tự hủy phiếu đã gửi duyệt',
     'Người lập CỐ Ý không được tự hủy phiếu đã gửi duyệt: gửi đi rồi thì quyền định đoạt thuộc về người duyệt. '
     'Lý do hủy và Ghi chú được lưu vào lịch sử thay đổi của phiếu; màn chi tiết phiếu đã hủy hiện lại hai nội '
     'dung này ở dải băng đầu màn. Hệ thống cũ có ô ghi chú nhưng chữ gõ vào bị mất.'),
    (r'^– Khóa dòng phiếu rồi kiểm tra lại quyền hủy',
     '– Đọc lại trạng thái mới nhất của phiếu rồi kiểm tra lại quyền hủy; không thoả → hiển thị “Bạn không có '
     'quyền hủy phiếu chi này.” và dừng xử lý.'),
    (r'^– Lý do hủy trống → hiển thị “Vui lòng nhập lý do hủy phiếu chi\.”',
     '– Lý do hủy trống → hiển thị “Lý do hủy – Bắt buộc nhập” dưới ô.'),
    (r'^– Ghi một dòng lịch sử đổi trạng thái, kèm lý do hủy và ghi chú của người duyệt\.',
     '– Ghi nhận hành động Hủy, kèm lý do hủy và ghi chú, trong lịch sử của phiếu.'),
    (r'^– Hiển thị “Hủy phiếu chi thành công!”\.', '– Hiển thị “Hủy phiếu chi thành công!” và quay về màn danh sách.'),
    # ---- 2.11
    (r'^2\. Hệ thống mở hộp xác nhận nêu rõ mã phiếu\.',
     '2. Hệ thống mở hộp “Xác nhận xóa”: “Bạn có chắc muốn xóa phiếu chi tiền \'{mã phiếu}\'?”.'),
    (r'^4\. Hệ thống kiểm tra lại điều kiện, chụp lại nội dung phiếu rồi xoá phiếu',
     '4. Hệ thống kiểm tra lại điều kiện rồi xoá phiếu cùng toàn bộ dòng chi tiết.'),
    (r'^5\. Hệ thống ghi một dòng lịch sử xoá và nạp lại danh sách\.',
     ['5. Ghi nhận hành động Xóa trong lịch sử.',
      '6. Hiển thị thông báo thành công: xóa ở màn danh sách thì nạp lại danh sách; xóa ở màn chi tiết thì quay '
      'về màn danh sách.']),
    (r'^• Không thoả điều kiện xoá → từ chối; hệ thống nạp lại danh sách cho khớp hiện trạng\.',
     '• Không thoả điều kiện xoá → từ chối với thông báo “Bạn không có quyền xóa phiếu chi.” hoặc “Phiếu chi đã bị '
     'khóa, không xóa được.”; hệ thống nạp lại dữ liệu cho khớp hiện trạng.'),
    (r'^Bạn có chắc muốn xóa phiếu chi tiền "\{mã phiếu\}"\?', 'Bạn có chắc muốn xóa phiếu chi tiền \'{mã phiếu}\'?'),
    (r'^– Kiểm tra lại đủ ba điều kiện ở phía máy chủ; không thoả → từ chối và nạp lại danh sách\.',
     '– Hệ thống kiểm tra lại đủ ba điều kiện; không thoả → từ chối và nạp lại dữ liệu.'),
    (r'^– Chụp lại nội dung phiếu kèm bảng chi tiết để ghi vào lịch sử\.', None),
    (r'^– Xoá phiếu cùng toàn bộ dòng chi tiết trong một giao dịch duy nhất\.', '– Xoá phiếu cùng toàn bộ dòng chi tiết.'),
    (r'^– Ghi một dòng lịch sử xoá\.', '– Ghi nhận hành động Xóa trong lịch sử.'),
    (r'^– Hiển thị “Xóa phiếu chi thành công!” và nạp lại danh sách\.',
     '– Màn danh sách: hiển thị “Xóa thành công” và nạp lại danh sách. Màn chi tiết: hiển thị “Xóa phiếu chi '
     'thành công!” và quay về màn danh sách.'),
    # ---- 2.12
    (r'^Mở bản in của phiếu ở tab mới, gồm ĐỦ 2 LIÊN',
     'Mở cửa sổ Xem trước bản in ngay trên màn đang đứng (không mở tab mới), gồm ĐỦ 2 LIÊN, kèm ảnh tiêu đề thư '
     'của công ty ghi trên phiếu.'),
    (r'^2\. Hệ thống mở tab mới trỏ tới trang in\.', '2. Hệ thống mở cửa sổ Xem trước bản in.'),
    (r'^4\. Trang in hiển thị 2 liên và trình duyệt tự mở hộp thoại in\.',
     '4. Cửa sổ hiển thị bản in 2 liên; người dùng bấm In để mở hộp thoại in của trình duyệt.'),
    (r'^• Người dùng đóng hộp thoại in → vẫn xem được bản in trên trang',
     '• Bấm Đóng cửa sổ xem trước → quay lại màn đang đứng, không in.'),
    (r'^Nằm ở góc trên bên trái, mở lại hộp thoại in của trình duyệt\.',
     'Nằm trong cửa sổ Xem trước bản in, mở hộp thoại in của trình duyệt.'),
    (r'^– Mở tab mới trỏ tới trang in của phiếu\.', '– Mở cửa sổ Xem trước bản in của phiếu.'),
    (r'^– Hiển thị bản in 2 liên và mở hộp thoại in của trình duyệt; không ghi',
     '– Hiển thị bản in 2 liên trong cửa sổ xem trước; không ghi bất kỳ thay đổi nào lên phiếu.'),
    # ---- 2.13
    (r'^3\. Hệ thống dựng tệp từ dữ liệu phiếu và trả về trình duyệt\.',
     '3. Hệ thống dựng tệp phieu_chi_tien_{mã phiếu}.xlsx từ dữ liệu phiếu, tải về máy và báo “Xuất Excel thành công”.'),
    (r'^– Dựng tệp Excel từ dữ liệu của đúng phiếu đó và trả về trình duyệt\.',
     '– Dựng tệp phieu_chi_tien_{mã phiếu}.xlsx từ dữ liệu của đúng phiếu đó, tải về máy và báo “Xuất Excel thành công”.'),
    # ---- 2.14
    (r'^Lịch sử là NƠI DUY NHẤT lưu Lý do hủy và Ghi chú của người duyệt',
     'Lịch sử là NƠI DUY NHẤT lưu Lý do hủy và Ghi chú của người duyệt. Đổi trạng thái luôn là một dòng lịch sử '
     'RIÊNG, tách khỏi dòng thay đổi thông tin.'),
    # ---- Phần 4
    (r'^– Loại chi nằm ngoài 7 giá trị hợp lệ bị chặn ngay',
     '– Loại chi nằm ngoài 7 giá trị hợp lệ bị từ chối với thông báo “Loại chi không hợp lệ”.'),
    (r'^– Các rule về ĐỊNH DẠNG',
     '– Các kiểm tra ĐỊNH DẠNG (kiểu số, giá trị phải có trong danh mục) vẫn áp ở cả hai nút — bỏ bắt buộc chỉ để '
     'cất được form đang làm dở, không phải để ghi dữ liệu sai.'),
    (r'^– Phiếu nháp được lưu với tài khoản “chưa chọn”', None),
    (r'^– Hai vế công ty cùng rỗng KHÔNG được coi là cùng công ty',
     '– Phiếu chưa xác định công ty và người dùng chưa gắn công ty KHÔNG được coi là cùng công ty.'),
    (r'^– Đây là điểm SIẾT CHẶT HƠN hệ thống cũ: hệ thống cũ chỉ kiểm trạng thái',
     '– Đây là điểm SIẾT CHẶT HƠN hệ thống cũ: hệ thống cũ chỉ kiểm trạng thái nên người khác vẫn sửa hoặc xoá '
     'được phiếu nháp không phải của mình.'),
    (r'^– Xóa phiếu xoá kèm toàn bộ dòng chi tiết trong một giao dịch',
     '– Xóa phiếu xoá kèm toàn bộ dòng chi tiết; không khôi phục lại được.'),
    (r'^– Khi lưu, hệ thống KHÓA DÒNG phiếu đề nghị rồi mới kiểm tra',
     '– Khi lưu, hệ thống kiểm tra lại ngay tại thời điểm ghi, nên hai người bấm lưu cùng lúc vẫn chỉ tạo được '
     'một phiếu chi; người sau nhận thông báo “Đề nghị thanh toán đã lập phiếu chi tiền.”.'),
    (r'^– Giao diện chỉ có MỘT nút Duyệt phiếu chi và MỘT endpoint duyệt',
     '– Giao diện chỉ có MỘT nút Duyệt phiếu chi; người duyệt không phải chọn cấp duyệt.'),
    (r'^– Toàn bộ bước duyệt nằm trong MỘT giao dịch',
     '– Duyệt và ghi sổ thực hiện trọn vẹn cùng nhau: ghi sổ lỗi thì phiếu giữ nguyên trạng thái cũ, không có '
     'phiếu “Đã duyệt” mà sổ kế toán trống.'),
    (r'^– Trước khi duyệt hoặc hủy, hệ thống KHÓA DÒNG phiếu rồi mới đọc lại trạng thái\.',
     '– Trước khi duyệt hoặc hủy, hệ thống đọc lại trạng thái mới nhất của phiếu.'),
    (r'^– Nhờ vậy hai người duyệt cùng lúc không thể ghi trùng bút toán\.',
     '– Nhờ vậy hai người duyệt cùng lúc không thể ghi trùng bút toán (hệ thống cũ duyệt hai lần là nhân đôi bút '
     'toán trong sổ kế toán).'),
    (r'^– Sinh mã phiếu cũng dùng khóa dòng', '– Hai người lưu cùng lúc cũng không bị sinh trùng mã phiếu.'),
    (r'^– Giao diện chống bấm nhiều lần bằng cách khoá nút trong lúc xử lý, nhưng chốt chặn thật nằm ở phía máy chủ\.',
     '– Giao diện chống bấm nhiều lần bằng cách khoá nút trong lúc xử lý; hệ thống vẫn kiểm tra lại khi ghi.'),
    (r'^– Luật này được kiểm ở HAI thời điểm bằng CÙNG một hàm',
     '– Luật này được kiểm ở HAI thời điểm theo cùng một cách tính: lúc lập/sửa phiếu và lúc duyệt, nên không có '
     'trường hợp lưu được mà bị chặn ở bước duyệt (hoặc ngược lại).'),
    (r'^– Hệ thống cũ KHÔNG hề kiểm trần lúc duyệt do điều kiện kiểm tra bị viết sai nhánh',
     '– Hệ thống cũ KHÔNG kiểm trần lúc duyệt — đây là lỗi đã được sửa.'),
    (r'^– Việc khớp dòng phiếu chi với dòng phiếu đề nghị dựa trên bộ khóa nhiều trường',
     '– Mỗi dòng phiếu chi được ghép đúng với dòng tương ứng của phiếu đề nghị, không dựa vào thứ tự dòng.'),
    (r'^– Cả hai KHÔNG được lưu lên phiếu mà lưu vào LỊCH SỬ THAY ĐỔI',
     '– Cả hai được lưu vào LỊCH SỬ THAY ĐỔI của phiếu.'),
    (r'^– Sinh mã có khóa dòng; hệ thống cũ không khóa',
     '– Hai phiếu tạo cùng lúc không bị trùng mã (hệ thống cũ có thể sinh trùng mã khiến một phiếu lưu lỗi).'),
    (r'^– Ngoại lệ: phiếu đang gắn tài khoản đã bị khóa thì tài khoản đó vẫn được trả kèm để select',
     '– Ngoại lệ: phiếu đang gắn tài khoản đã bị khóa thì tài khoản đó vẫn hiện trong ô chọn với đúng tên, tránh '
     'việc người dùng vô tình lưu đè mất giá trị cũ.'),
    (r'^– Bước Thủ quỹ duyệt ghi thêm một dòng đối soát riêng', None),
    (r'^– Bản in luôn gồm ĐỦ 2 LIÊN',
     '– Bản in hiển thị trong cửa sổ Xem trước bản in, gồm ĐỦ 2 LIÊN, mỗi liên có ảnh tiêu đề thư của công ty và 5 ô ký.'),
]

# Cột Loại: (mục, regex tên đối tượng, loại mới)
TYPE_FIX = [
    (r'^2\.1 ', r'^Cột Số tiền$', 'Table/Grid'),
    (r'^2\.1 ', r'^Cột Trạng thái$', 'Table/Grid'),
    (r'^2\.2 ', r'^Ô lọc Số tiền từ', 'Textbox'),
    (r'^2\.4 ', r'^Loại tiền$', 'Dropdown / Label'),
    (r'^2\.4 ', r'^Tỷ giá', 'Textbox'),
    (r'^2\.4 ', r'^Người đề nghị$', 'Label'),
    (r'^2\.4 ', r'^Phòng ban$', 'Label'),
    (r'^2\.4 ', r'^Cột Số tiền đề nghị chi$', 'Table/Grid'),
    (r'^2\.4 ', r'^Cột Số tiền chi$', 'Textbox'),
    (r'^2\.4 ', r'^Khối Ngân hàng nhận tiền$', 'Label'),
    (r'^2\.4 ', r'^Khối Ngân hàng trung gian$', 'Label'),
    (r'^2\.6 ', r'^Cột Tên tài khoản$', 'Table/Grid'),
    (r'^2\.6 ', r'^Cột Nhân viên$', 'Table/Grid'),
    (r'^2\.6 ', r'^Cột Số dư$', 'Table/Grid'),
    (r'^2\.6 ', r'^Cột Số tiền chi$', 'Textbox'),
    (r'^2\.7 ', r'^Mã phiếu$', 'Label'),
    (r'^2\.7 ', r'^Người lập$', 'Label'),
    (r'^2\.7 ', r'^Ngày lập$', 'Label'),
    (r'^2\.8 ', r'^Dải băng Lý do hủy$', 'Label'),
    (r'^2\.8 ', r'^Khối Thông tin chung$', 'Label'),
    (r'^2\.9 ', r'^Cột Số tiền thực chi$', 'Textbox'),
    (r'^2\.12 ', r'^Ảnh tiêu đề thư$', 'Image'),
]
DEL_ROWS = [  # (mục, regex tên đối tượng) — dòng không phải đối tượng (thông báo lỗi chung)
    (r'^2\.4 ', r'^Thông báo lỗi inline$'),
    (r'^2\.10 ', r'^Lỗi inline của Lý do hủy$'),
]

PART5 = [  # STT | Nhóm | Màn hình | Đường dẫn
    ('1', 'Tài chính', 'Đề nghị thanh toán (cột Số tiền chi lấy từ phiếu chi; trạng thái phiếu đề nghị cập nhật khi '
     'phiếu chi được gửi duyệt / duyệt / hủy; nút Tạo phiếu chi mở màn Tạo mới phiếu chi)',
     'Tài chính -> Quản lý tiền -> Đề nghị'),
    ('2', 'Bán hàng', 'Đối chiếu công nợ 1 KH; Chi tiết công nợ KH (khoản chi trả lại khách hàng đọc bút toán do '
     'phiếu chi ghi khi Thủ quỹ duyệt, kèm mã phiếu chi)', 'Bán hàng -> Báo cáo -> Báo cáo công nợ'),
    ('3', 'Tài chính', 'Danh mục tài khoản; Danh mục tiền tệ (tài khoản / loại tiền đang dùng trên phiếu chi được '
     'tính là đang sử dụng)', 'Tài chính -> Danh mục'),
]


# ============================================================== XỬ LÝ
def all_line_fix(doc):
    """Áp LINE_FIX cho mọi ô bảng (theo dòng) và mọi đoạn thường không có hyperlink."""
    used = set()

    def fix(lines):
        out, ch = [], False
        for l in lines:
            for i, (rx, new) in enumerate(LINE_FIX):
                if re.search(rx, l.strip()):
                    used.add(i)
                    ch = True
                    if new is not None:
                        out.extend(new if isinstance(new, list) else [new])
                    break
            else:
                out.append(l)
        return out, ch

    body = doc.element.body
    for tc in body.iter(W('tc')):
        if tc.find('.//' + W('tbl')) is not None:
            continue
        lines = cell_lines(tc)
        new, ch = fix(lines)
        if ch:
            write_cell(tc, new or [''])
    for p in list(body.iterchildren(W('p'))):
        if p.find(W('hyperlink')) is not None or style_of(p):
            continue
        t = txt(p)
        if not t.strip():
            continue
        new, ch = fix([t])
        if ch:
            if not new:
                p.getparent().remove(p)
            else:
                set_runs_text(p, new[0])
    miss = [LINE_FIX[i][0] for i in range(len(LINE_FIX)) if i not in used]
    for m in miss:
        log('!! LINE_FIX không khớp: ' + m)


def fix_heading_numbers(doc):
    """161 đánh số lẫn '2 ' / '2.1.' — thống nhất '2. Ma trận' / '2. Đặc tả' / '2.x Tên'."""
    for e in items(doc):
        if e.tag != W('p') or style_of(e) not in ('Heading2', 'Heading3'):
            continue
        t = txt(e)
        new = None
        if style_of(e) == 'Heading2' and re.match(r'^2 (Ma trận|Đặc tả)', t):
            new = re.sub(r'^2 ', '2. ', t)
        elif style_of(e) == 'Heading3' and re.match(r'^\d+\.\d+\.\s', t):
            new = re.sub(r'^(\d+\.\d+)\.\s', r'\1 ', t)
        if new:
            for x in e.iter(W('t')):  # sửa trong <w:t> (giữ bookmark của mục lục)
                if x.text and x.text.strip():
                    if style_of(e) == 'Heading2':
                        x.text = re.sub(r'^(\s*)2 ', r'\g<1>2. ', x.text, 1)
                    else:
                        x.text = re.sub(r'^(\s*\d+\.\d+)\.', r'\1', x.text, 1)
                    break
            if txt(e) != new:  # chữ số tách nhiều run -> ghi lại cả đoạn
                set_runs_text(e, new)
            log('Đánh lại số heading: %s → %s' % (t, txt(e)))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)

    fix_heading_numbers(doc)
    # Câu "Nếu có lỗi thì KHÔNG thực hiện bước After." cũ -> bỏ, add_err_line thêm câu chuẩn có link
    for tc in doc.element.body.iter(W('tc')):
        ls = cell_lines(tc)
        if any(re.search(r'(?i)không thực hiện bước After', l) for l in ls):
            write_cell(tc, [l for l in ls if not re.search(r'(?i)không thực hiện bước After', l)])
    all_line_fix(doc)

    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    for rx, (menu, popup) in MENU_LINES.items():
        sec = section(doc, rx)
        p = sec_par(sec, r'^Menu:')
        set_runs_text(p, menu)
        nxt = p.getnext()
        is_text = (nxt is not None and nxt.tag == W('p') and txt(nxt).strip()
                   and not list(nxt.iter(L.A_NS + 'blip')) and not txt(nxt).startswith('Hình '))
        if popup and is_text:
            set_runs_text(nxt, popup)
        elif popup:
            strip_ids(docxlib.clone_par_after(p, p, popup))

    for srx, orx, new in TYPE_FIX:
        ui = sec_ui(section(doc, srx))
        set_col(ui, header_index(ui, 'Loại'), orx, new)
    for srx, orx in DEL_ROWS:
        delete_row(sec_ui(section(doc, srx)), orx)

    patch_sections(doc, rid)
    patch_part4(doc)
    add_part5(doc)
    replace_images(doc)

    remove_usecase(doc, section(doc, r'^2\.3 '))
    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.9 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
        else:
            set_image(doc, blk[1], png)
            set_runs_text(blk[2], 'Hình 0: Biểu đồ Use Case — %s %s' % (code, name))
    renumber_subheadings(doc)
    nfig = renumber_figures(doc)
    log('Số Hình sau khi đánh lại: %d' % nfig)

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.join(OUT_DIR, 'SRS - Phiếu chi tiền.pdf'))


def ev_row_set(ev, event_regex, col, lines):
    write_cell(cells(find_row(ev, 1, event_regex))[col], lines)


def patch_sections(doc, rid):
    # 2.2: gộp Enter vào sự kiện Tìm kiếm (bỏ loại Keypress)
    ev = sec_ev(section(doc, r'^2\.2 '))
    ev_row_set(ev, r'^Bấm nút Tìm kiếm$', 1, ['Bấm nút Tìm kiếm hoặc nhấn Enter trong ô tìm nhanh'])
    delete_row(ev, r'^Gõ vào ô tìm nhanh')

    # 2.3: kéo thả
    s = section(doc, r'^2\.3 ')
    ev = sec_ev(s)
    clone_row_after(ev, r'^Bỏ tích một mục', [None, 'Kéo thả một dòng', 'Drag',
                                              ['After:', '– Đổi vị trí ô lọc / cột; áp dụng sau khi bấm Lưu.']])
    kv = sec_kv(s)
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'),
               [l if not l.startswith('• Bấm Đóng →') else
                '• Bấm Đóng / (x) / click ra ngoài cửa sổ → thoát mà không lưu thay đổi, không hỏi xác nhận.'
                for l in kv_get(kv, 'Dòng sự kiện phụ')])

    # 2.4 Tạo mới
    s = section(doc, r'^2\.4 ')
    ui = sec_ui(s)
    clone_row_after(ui, r'^Nút Lưu và gửi duyệt$',
                    [None, 'Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
                     'Chỉ có ở màn Tạo mới (không có khi mở từ màn Đề nghị thanh toán): lưu nháp rồi mở lại màn '
                     'Tạo mới trống để lập phiếu tiếp.'])
    write_cell(cells(find_row(ui, 1, r'^Nút Lưu và gửi duyệt$'))[-1],
               ['Mở hộp “Xác nhận lưu và gửi duyệt” trước khi lưu và gửi duyệt.'])
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # 2.5 Chọn phiếu đề nghị
    s = section(doc, r'^2\.5 ')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Tiêu đề cửa sổ$'))[-1],
               ['Phụ đề ghi “Chỉ phiếu Chờ tạo phiếu chi và chưa lập phiếu chi”.'])

    # 2.7 Sửa
    s = section(doc, r'^2\.7 ')
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # 2.8 Chi tiết: thứ tự nút theo code
    ui = sec_ui(section(doc, r'^2\.8 '))
    write_cell(cells(find_row(ui, 1, r'^Nút Quay lại$'))[-1],
               ['Về danh sách, giữ nguyên bộ lọc đã lưu. Thứ tự nút cuối màn: Sửa, Duyệt phiếu chi, Hủy phiếu '
                'chi, In, Xuất Excel, Xóa, Quay lại.'])

    # 2.9 Duyệt
    s = section(doc, r'^2\.9 ')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Tiêu đề cửa sổ$'))[-1],
               ['“Duyệt phiếu chi tiền”, hoặc “Duyệt phiếu chi thu nhập nhân viên” với loại Chi thu nhập cho nhân '
                'viên. Phụ đề ghi “Phiếu chi: {mã phiếu}”.'])
    clone_row_after(ui, r'^Nút Đóng$',
                    [None, 'Hộp Xác nhận duyệt', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
                     'Hiện sau khi bấm Duyệt: “Bạn có chắc muốn duyệt phiếu chi \"{mã phiếu}\"?”, nút Duyệt / Hủy.'])
    add_err_line(sec_ev(s), r'^Bấm Duyệt trong cửa sổ', rid)

    # 2.10 Hủy
    add_err_line(sec_ev(section(doc, r'^2\.10 ')), r'^Bấm Xác nhận trong cửa sổ hủy', rid)
    # 2.11 Xóa
    add_err_line(sec_ev(section(doc, r'^2\.11 ')), r'^Bấm Xóa trong hộp xác nhận', rid)

    # 2.12 In: Use case / ảnh minh họa giữ, ghi lại tên nút
    # 2.13 Xuất Excel: thêm dòng sự kiện phụ tên tệp
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Tên tệp: phieu_chi_tien_{mã phiếu}.xlsx (dấu chấm trong mã đổi thành gạch ngang).'])

    # 2.14 Lịch sử
    s = section(doc, r'^2\.14 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa từng thao tác',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện “Chưa có lịch sử thao tác nào.”')


def lines_replace(lines, old_regex, new):
    out = []
    for l in lines:
        if re.search(old_regex, l):
            if new is not None:
                out.extend(new if isinstance(new, list) else [new])
        else:
            out.append(l)
    return out


def kv_edit(kv, key, old_regex, new):
    write_cell(kv_row(kv, key), lines_replace(kv_get(kv, key), old_regex, new))


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and txt(e).startswith('Phần %d' % n):
            return e
    raise KeyError(n)


def patch_part4(doc):
    h = part_heading(doc, 4)
    intro = h.getnext()
    set_rule_head(intro, 'Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
    set_rule_tail(intro, '. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có trong SRS '
                         'quy tắc chung.' % SCREEN)
    tbl = intro.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()

    def desc(code, old_regex, new):
        tc = cells(find_row(tbl, 1, '^%s$' % code))[3]
        write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))

    # Bỏ ý trùng quy tắc chung
    desc('BR-12', r'^– Lỗi gửi thông báo KHÔNG được làm hỏng', None)
    desc('BR-17', r'^– Xem lịch sử không cần quyền riêng', None)
    desc('BR-16', r'^– In phiếu và xuất Excel chỉ cần quyền XEM phiếu', None)
    desc('BR-11', r'^– Mỗi dòng phiếu chi được ghép', [
        '– Mỗi dòng phiếu chi được ghép đúng với dòng tương ứng của phiếu đề nghị, không dựa vào thứ tự dòng.',
        '– Phiếu chi bị hủy: phiếu đề nghị chuyển sang Hủy và KHÔNG lập lại được phiếu chi khác cho phiếu đề nghị '
        'đó (hành vi kế thừa hệ thống cũ, đã chốt giữ nguyên).'])
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc dữ liệu do %s ghi ra (phiếu chi, '
                                    'dòng chi tiết và bút toán ghi khi Thủ quỹ duyệt).' % SCREEN)
    strip_ids(intro)
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


def replace_images(doc):
    its = items(doc)
    for i, e in enumerate(its):
        if e.tag != W('p') or not re.match(r'^Hình \d+:', txt(e)):
            continue
        cap = re.sub(r'^Hình \d+:\s*', '', txt(e))
        img = its[i - 1]
        for key, new in NEW_CAPTIONS.items():
            if cap.startswith(key):
                set_runs_text(e, 'Hình 0: ' + new)
        for key, name in NEW_IMAGES.items():
            if cap.startswith(key):
                png = os.path.join(SHOTS, name + '.png')
                if os.path.exists(png) and list(img.iter(L.A_NS + 'blip')):
                    set_image(doc, img, png)
                    log('Thay ảnh: %s ← %s' % (cap[:50], name))
                else:
                    log('!! Thiếu ảnh mới cho: ' + cap)
                break
    # Hình in: ảnh mới cửa sổ xem trước
    png = os.path.join(SHOTS, '23_print.png')
    for i, e in enumerate(its):
        if e.tag == W('p') and 'Cửa sổ Xem trước bản in phiếu chi' in txt(e) and os.path.exists(png):
            set_image(doc, its[i - 1], png)
            log('Thay ảnh bản in ← 23_print')
    png = os.path.join(SHOTS, '17_detail.png')
    for i, e in enumerate(its):
        if e.tag == W('p') and 'Nút Xuất Excel trên thanh nút cuối màn chi tiết' in txt(e) and os.path.exists(png):
            set_image(doc, its[i - 1], png)


if __name__ == '__main__':
    main()
