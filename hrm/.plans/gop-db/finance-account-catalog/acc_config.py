# -*- coding: utf-8 -*-
"""Cau hinh 2 man 'Danh muc tai khoan' + 'Danh muc loai tai khoan' (phan he Tai chinh).

Doc code 18/08/2026:
  BE  Modules/Finance/Routes/api.php (32-94) — moi man 2 quyen: "Quan ly ..." va "Xem ...";
      route update/delete gan them middleware `recordNotLocked` (ban ghi Khoa thi tu choi).
      Modules/Finance/Http/Requests/Account/AccountRequest.php   -> rang buoc cay 3 bac
      Modules/Finance/Http/Requests/TypeAccount/TypeAccountRequest.php
      Modules/Finance/Entities/Account/Account.php               -> STATUSES, MAX_IDENTIFY_NUMBER
      Modules/Finance/Entities/TypeAccount/TypeAccount.php       -> isLocked(), TRACKED_COLUMNS
  FE  hrm-client/pages/finance/accounts/{index,add,_id/index,_id/edit,print}.vue
      hrm-client/pages/finance/type-accounts/index.vue
  Anh that: acc_shots/ (cong dev hrm-crm.eteksofts.com, 18/08/2026)
"""

HOST = 'http://hrm-crm.eteksofts.com'

_TACDUNG_QL = ('Mở màn hình và thực hiện đầy đủ Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa và '
               'Nhập dữ liệu từ Excel. Thiếu quyền này thì các nút thao tác không hiển thị.')
_TACDUNG_XEM = ('Chỉ mở được màn hình để tra cứu, xuất Excel và xem lịch sử. Không thấy nút '
                'Tạo mới, Sửa, Xóa, Khóa và Import.')
_GHICHU = ('Màn hình tách riêng quyền quản lý và quyền xem. Người chỉ có quyền xem vẫn vào '
           'được màn hình và tra cứu bình thường nhưng mọi nút ghi dữ liệu đều bị ẩn. Người '
           'không có quyền nào thì mục menu không hiển thị và truy cập thẳng đường dẫn cũng '
           'bị chặn.')

# ============================================================ DANH MỤC TÀI KHOẢN
ACCOUNT = dict(
    key='tk',
    ten='Danh mục tài khoản',
    doi_tuong='tài khoản',
    route='/finance/accounts',
    host=HOST,
    menu='Phân hệ Tài chính → Danh mục → Danh mục tài khoản',
    quyen_quan_ly='Quản lý danh mục tài khoản',
    quyen_xem='Xem danh mục tài khoản',
    tacdung_ql=_TACDUNG_QL,
    tacdung_xem=_TACDUNG_XEM + ' Vẫn dùng được chức năng In danh sách.',
    ghichu_quyen=_GHICHU,
    co_trangthai=True,
    truong_trung='Số tài khoản',
    loi_trung='Số tài khoản đã tồn tại',
    loi_khac=[
        '– Số tài khoản có ký tự không phải chữ số, hoặc ít hơn 3 / nhiều hơn 15 chữ số → '
        'hiển thị “Chỉ được nhập chữ số, từ 3 đến 15 chữ số”.',
        '– Bậc tài khoản là 2 hoặc 3 mà bỏ trống Tài khoản mẹ → hiển thị “Bắt buộc phải chọn '
        'tài khoản mẹ với bậc 2 và 3”.',
        '– Tài khoản mẹ không có thật → hiển thị “Không tìm thấy tài khoản mẹ”.',
        '– Tài khoản mẹ không đúng bậc liền trên → hiển thị “Tài khoản mẹ phải là tài khoản '
        'bậc N” kèm bậc thực tế của tài khoản mẹ.',
        '– Số tài khoản con không bắt đầu bằng số tài khoản mẹ → hiển thị hướng dẫn số con '
        'phải nối tiếp số mẹ.',
        '– Tài khoản đang có tài khoản con mà đổi Bậc hoặc Số tài khoản → hiển thị cảnh báo '
        'kèm số lượng tài khoản con, yêu cầu chuyển hoặc xóa các con trước.',
    ],
    loi_import=[
        '– Dòng thiếu Số tài khoản, Tên tài khoản, Bậc hoặc Loại tài khoản → đánh dấu lỗi.',
        '– Số tài khoản đã có trong danh mục hoặc trùng với dòng khác trong tệp → đánh dấu lỗi.',
        '– Tài khoản mẹ không tồn tại hoặc không đúng bậc liền trên → đánh dấu lỗi.',
    ],
    tb_them='Thêm mới tài khoản thành công',
    tb_sua='Cập nhật tài khoản thành công',
    tb_xoa='Xóa tài khoản thành công',
    dieu_kien_xoa='tài khoản chưa phát sinh bút toán và không có tài khoản con',
    dieu_kien_an_xoa='tài khoản đã phát sinh bút toán hoặc đang có tài khoản con',
    cauhoi_xoa="Bạn có chắc muốn xóa tài khoản '1111 - Tài khoản ví dụ bậc 2'?",
    cauhoi_khoa="Bạn có chắc muốn khóa tài khoản '111 - Tiền mặt'?",
    muc_dich=[
        'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý Danh mục tài khoản.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ ràng buộc cây tài khoản ba bậc: quan hệ mẹ – con, quy tắc đặt số và các trường '
        'hợp bị chặn khi tài khoản đã có con.',
        'Làm rõ khác biệt giữa Xóa và chuyển trạng thái Khóa.',
    ],
    thuat_ngu=[
        ('Tài khoản',
         'Một mục trong hệ thống tài khoản kế toán, dùng để ghi nhận và phân loại các nghiệp '
         'vụ phát sinh.'),
        ('Số tài khoản',
         'Dãy chữ số định danh tài khoản, duy nhất trên toàn danh mục. Từ 3 đến 15 chữ số.'),
        ('Bậc tài khoản',
         'Vị trí của tài khoản trên cây ba bậc. Bậc 1 là tài khoản tổng, bậc 2 và 3 là tài '
         'khoản chi tiết.'),
        ('Tài khoản mẹ',
         'Tài khoản ở bậc liền trên. Tài khoản bậc 1 nằm ở gốc cây nên không có tài khoản mẹ.'),
        ('Tài khoản con',
         'Tài khoản ở bậc liền dưới, có số tài khoản bắt đầu bằng số của tài khoản mẹ.'),
        ('Loại tài khoản',
         'Nhóm phân loại tài khoản, lấy từ Danh mục loại tài khoản.'),
        ('Tài khoản theo dõi công nợ',
         'Đánh dấu tài khoản được dùng để theo dõi công nợ phải thu / phải trả theo từng khách '
         'hàng và nhà cung cấp.'),
        ('Trạng thái Hoạt động', 'Tài khoản còn chọn được khi lập bút toán mới.'),
        ('Trạng thái Khóa',
         'Tài khoản không còn chọn được ở nghiệp vụ mới nhưng vẫn nằm trong danh mục và các '
         'bút toán cũ không bị ảnh hưởng.'),
    ],
    cot=[
        ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
        ('Số tài khoản', 'Dãy chữ số định danh. Luôn hiển thị, sắp xếp được, bấm vào để mở '
                         'màn chi tiết.'),
        ('Tên tài khoản', 'Tên đầy đủ của tài khoản.'),
        ('Bậc', 'Bậc 1, 2 hoặc 3 trên cây tài khoản.'),
        ('Tài khoản mẹ', 'Số tài khoản ở bậc liền trên. Tài khoản bậc 1 để trống.'),
        ('Loại tài khoản', 'Nhóm phân loại, lấy từ Danh mục loại tài khoản.'),
        ('Theo dõi công nợ', 'Có hoặc Không.'),
        ('Người tạo', 'Họ tên người đã thêm bản ghi.'),
        ('Ngày tạo', 'Ngày giờ thêm bản ghi, sắp xếp được.'),
        ('Người cập nhật', 'Họ tên người sửa gần nhất. Mặc định ẩn.'),
        ('Ngày cập nhật', 'Ngày giờ sửa gần nhất, sắp xếp được. Mặc định ẩn.'),
        ('Trạng thái', 'Hoạt động hoặc Khóa, hiển thị dạng badge.'),
        ('Hành động', 'Nút Sửa, Xóa, Khóa / Mở khóa và Lịch sử. Hai nút đầu còn dùng được hiện '
                      'thẳng, phần còn lại nằm trong nút ba chấm.'),
    ],
    nut_thanh_cong_cu=[
        ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện với người có quyền quản lý; mở màn hình Thêm tài khoản.'),
        ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị',
         'Mở bản in trên thẻ trình duyệt mới.'),
        ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn trường cần xuất.'),
        ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện với người có quyền quản lý.'),
        ('Nút Tùy chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn cột hiển thị trên bảng.'),
    ],
    loc=[
        ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
         'Tìm đồng thời theo Số tài khoản và Tên tài khoản.'),
        ('Bậc tài khoản', 'Dropdown', 'Bậc 1 / 2 / 3', 'Trống', 'Lọc theo bậc trên cây.'),
        ('Loại tài khoản', 'Dropdown', 'Danh sách', 'Trống', 'Lọc theo nhóm phân loại.'),
        ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Trống',
         'Bỏ trống thì hiện cả hai trạng thái.'),
        ('Người tạo', 'Dropdown', 'Danh sách', 'Trống', 'Lọc theo người đã thêm bản ghi.'),
        ('Người cập nhật', 'Dropdown', 'Danh sách', 'Trống', 'Lọc theo người sửa gần nhất.'),
    ],
    truong=[
        ('Số tài khoản', 'Textbox', 'Enable', '3–15 chữ số', 'Có', 'Trống',
         'Chỉ nhận chữ số và phải là duy nhất. 3 chữ số là bậc 1, 4 chữ số là bậc 2, từ 5 chữ '
         'số là bậc 3. Tài khoản đang có tài khoản con thì ô này bị khóa, không sửa được.'),
        ('Bậc tài khoản', 'Dropdown', 'Enable', 'Bậc 1 / 2 / 3', 'Có', 'Trống',
         'Quyết định vị trí trên cây. Tài khoản đang có tài khoản con thì ô này bị khóa.'),
        ('Tài khoản mẹ', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Có với bậc 2 và 3', 'Trống',
         'Bắt buộc với bậc 2 và 3, phải đúng bậc liền trên. Bậc 1 nằm ở gốc cây nên ô này bị '
         'khóa và ghi rõ lý do.'),
        ('Tên tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Tên đầy đủ của tài khoản. Không kiểm tra trùng tên.'),
        ('Loại tài khoản', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
         'Chọn từ Danh mục loại tài khoản.'),
        ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
         'Đặt sẵn là Hoạt động khi thêm mới.'),
        ('Tài khoản theo dõi công nợ', 'Icon Button', 'Enable', '–', 'Không', 'Không tích',
         'Bật khi tài khoản dùng để theo dõi công nợ theo từng khách hàng, nhà cung cấp.'),
    ],
    tc_sheet='Danh muc tai khoan',
    tc_module='Tai chinh - Danh muc',
    tc_mucdich=(
        'Quan ly he thong tai khoan ke toan ba bac. Man hinh cho phep tra cuu, tim kiem, them '
        'moi, chinh sua, xoa, khoa/mo khoa, nhap tu Excel, xuat Excel, in danh sach va xem lich '
        'su thay doi. Du lieu cua man nay duoc chon khi lap but toan ke toan.'),
    tc_caudata=(
        '- Danh muc CO PHAN CAP, dung ba bac.\n'
        '- Bac suy ra tu do dai so tai khoan: 3 chu so la bac 1, 4 chu so la bac 2, tu 5 chu '
        'so la bac 3.\n'
        '- Tai khoan bac 2 va 3 bat buoc co tai khoan me o bac lien tren, va so cua con phai '
        'bat dau bang so cua me.'),
    tc_dedupe=(
        '- Moi tai khoan chi hien MOT dong.\n'
        '- So tai khoan la duy nhat toan he thong, trung se bi chan voi thong bao '
        '"So tai khoan da ton tai".\n'
        '- Ten tai khoan KHONG kiem tra trung: hai tai khoan khac so duoc phep trung ten.'),
    tc_nguon=(
        'Du lieu lay tu danh muc Tai khoan. Cot Loai tai khoan lay ten tu Danh muc loai tai '
        'khoan. Cot Nguoi tao va Nguoi cap nhat lay ho ten nhan vien thuc hien thao tac.'),
    tc_luuy=[
        'Cac bay de sai nhat cua man nay, QA doc truoc khi test:',
        '- Man hinh dung HAI quyen tach roi. Nguoi chi co quyen xem VAN VAO DUOC man hinh, '
        'khac han cac man chi co mot quyen.',
        '- Them moi va Chinh sua mo TRANG RIENG chu khong phai cua so, khac voi man Loai tai '
        'khoan va man Tien te.',
        '- Chi o Ten tai khoan bao loi do ngay duoi o khi bo trong. Cac o bat buoc con lai '
        '(So tai khoan, Bac, Loai tai khoan) khong bao inline — day la thiet ke chung cua du an, '
        'khong phai loi.',
        '- Tai khoan dang co tai khoan con thi hai o So tai khoan va Bac bi KHOA. Phai chuyen '
        'hoac xoa cac con truoc moi sua duoc.',
        '- Xoa va Khoa la hai viec khac nhau: Khoa van giu ban ghi trong danh sach, Xoa thi mat han.',
        '- Ban ghi da Khoa thi khong duoc sua va khong duoc xoa; chi duoc Mo khoa.',
        '- Nut khong dung duoc phai AN HAN, khong phai hien nut xam.',
    ],
    hdsd_gioithieu=[
        'Danh mục tài khoản là nơi khai báo hệ thống tài khoản kế toán của công ty, tổ chức theo cây ba bậc.',
        'Bậc được suy ra từ độ dài số tài khoản: 3 chữ số là bậc 1 (tài khoản tổng), 4 chữ số là bậc 2, từ 5 chữ số là bậc 3. Tài khoản bậc 2 và 3 bắt buộc phải có tài khoản mẹ ở bậc liền trên, và số của con phải bắt đầu bằng số của mẹ.',
        'Dữ liệu của màn này được chọn khi lập bút toán kế toán, nên mỗi thay đổi ở đây đều ảnh hưởng tới sổ sách.',
        'Khác với các danh mục khác, màn này mở TRANG RIÊNG khi thêm mới và chỉnh sửa, không dùng cửa sổ.',
    ],
    hdsd_loi=[
        ['Bắt buộc phải nhập', 'Bạn chưa nhập Tên tài khoản. Các ô bắt buộc khác như Số tài khoản, Bậc và Loại tài khoản cũng phải điền đủ mới lưu được.'],
        ['Chỉ được nhập chữ số, từ 3 đến 15 chữ số', 'Số tài khoản chỉ nhận chữ số. Kiểm tra xem bạn có gõ nhầm chữ cái hay dấu cách không.'],
        ['Số tài khoản đã tồn tại', 'Đã có tài khoản khác mang đúng số này. Hãy chọn số khác.'],
        ['Bắt buộc phải chọn tài khoản mẹ với bậc 2 và 3', 'Bạn chọn bậc 2 hoặc 3 mà chưa chọn tài khoản mẹ. Hãy chọn tài khoản ở bậc liền trên.'],
        ['Tài khoản mẹ phải là tài khoản bậc N', 'Tài khoản mẹ bạn chọn không đúng bậc liền trên. Tài khoản bậc 2 phải có mẹ bậc 1, bậc 3 phải có mẹ bậc 2.'],
        ['Số tài khoản con phải bắt đầu bằng số tài khoản mẹ', 'Ví dụ mẹ là 111 thì con phải là 1111, 1112. Đặt số không nối tiếp mẹ sẽ làm tài khoản nằm sai vị trí trên cây.'],
        ['Tài khoản đang có N tài khoản con nên không được đổi bậc', 'Phải chuyển hoặc xóa các tài khoản con trước rồi mới đổi được bậc hoặc số tài khoản của tài khoản mẹ.'],
    ],
    hdsd_faq=[
        ['Vì sao ô Số tài khoản và Bậc của tôi bị khóa', 'Tài khoản đó đang có tài khoản con. Cây chỉ có ba bậc nên không thể tự đẩy các con xuống, còn đổi số sẽ làm con mất liên kết với mẹ. Hãy chuyển hoặc xóa các con trước.'],
        ['Tôi bỏ trống Số tài khoản mà không thấy báo lỗi đỏ dưới ô', 'Chỉ ô Tên tài khoản báo lỗi ngay dưới ô. Các ô bắt buộc còn lại được kiểm tra khi lưu. Đây là quy ước chung của hệ thống, không phải lỗi.'],
        ['Dòng này không có nút Xóa', 'Tài khoản đó đã phát sinh bút toán hoặc đang có tài khoản con. Nếu chỉ muốn ngừng dùng, hãy bấm Khóa thay vì Xóa.'],
        ['Bản ghi đang Khóa mà tôi cần sửa', 'Bấm Mở khóa trước, sửa xong rồi Khóa lại nếu cần. Bản ghi đang Khóa không sửa và không xóa được.'],
        ['Loại tài khoản tôi mới tạo không có trong ô lọc Loại tài khoản', 'Ô lọc hiện chỉ liệt kê bảy loại tài khoản gốc của hệ thống. Loại do người dùng tự tạo vẫn chọn được ở form nhưng chưa lọc được ngoài danh sách. Hãy dùng ô tìm nhanh theo tên tài khoản để thay thế.'],
        ['Nhập từ Excel xong mà thiếu vài dòng', 'Những dòng đó bị đánh dấu lỗi ở bước kiểm tra nên không được ghi. Mở lại cửa sổ nhập, tích Chỉ dòng lỗi để xem và sửa lại.'],
    ],
    hdsd_sua_them=[
        'Tài khoản đang có tài khoản con thì hai ô Số tài khoản và Bậc bị khóa. Hệ thống ghi rõ lý do ngay dưới ô để bạn biết cần xử lý gì trước.',
    ],
    shots=dict(danhsach='tk_01_danhsach.png', boloc='tk_02_boloc.png',
               taomoi='tk_03_taomoi.png', validate='tk_04_validate.png',
               sua='tk_05_sua.png', xem='tk_06_chitiet.png', lichsu='tk_07_lichsu.png',
               khoa='tk_08_xacnhan_khoa.png', xoa='tk_09_xacnhan_xoa.png',
               xuat='tk_11_xuat_excel.png', cot='tk_12_cauhinh_cot.png',
               **{'import': 'tk_10_import.png', 'in': 'tk_13_in_danhsach.png'}),
    funcs=[
        'list', 'filter',
        ('view', {'nhan': 'Xem chi tiết tài khoản', 'modal': False,
                  'cot_bam': 'số tài khoản', 'route': '/finance/accounts/{id}'}),
        ('create', {'nhan': 'Thêm mới tài khoản', 'modal': False,
                    'route': '/finance/accounts/add',
                    'rel_them': [('include', 'Kiểm tra ràng buộc cây tài khoản')]}),
        ('edit', {'nhan': 'Chỉnh sửa tài khoản', 'modal': False,
                  'route': '/finance/accounts/{id}/edit',
                  'rel_them': [('extend', 'Khóa ô Số tài khoản và Bậc khi đã có tài khoản con')]}),
        'delete', 'lock', 'history', 'import', 'export', 'print', 'columns',
    ],
    quy_tac=[
        ('Tách riêng quyền xem và quyền quản lý', [
            'Màn hình dùng hai quyền: “Quản lý danh mục tài khoản” cho mọi thao tác ghi và '
            '“Xem danh mục tài khoản” cho tra cứu, xuất Excel, in và xem lịch sử.',
            'Người chỉ có quyền xem không thấy nút Tạo mới, Sửa, Xóa, Khóa và Import.',
            'Mọi thao tác ghi đều kiểm tra lại quyền ở tầng máy chủ.',
        ]),
        ('Cây tài khoản có đúng ba bậc', [
            'Bậc được suy ra từ độ dài số tài khoản: 3 chữ số là bậc 1, 4 chữ số là bậc 2, từ '
            '5 chữ số là bậc 3.',
            'Tài khoản bậc 1 nằm ở gốc cây nên không có tài khoản mẹ.',
            'Tài khoản bậc 2 và bậc 3 bắt buộc phải có tài khoản mẹ, và mẹ phải ở đúng bậc '
            'liền trên.',
        ]),
        ('Số tài khoản con phải nối tiếp số tài khoản mẹ', [
            'Số của tài khoản con bắt buộc bắt đầu bằng số của tài khoản mẹ.',
            'Ví dụ mẹ là 111 thì con phải là 1111, 1112 và tương tự.',
            'Ràng buộc này là điều kiện để cây tài khoản sắp đúng thứ tự; con không nối tiếp mẹ '
            'sẽ nằm sai chỗ và không kéo về đúng vị trí được.',
        ]),
        ('Tài khoản đang có con thì khóa Số tài khoản và Bậc', [
            'Khi tài khoản đã có ít nhất một tài khoản con, hai ô Số tài khoản và Bậc tài khoản '
            'bị khóa, không sửa được.',
            'Lý do: cây chỉ có ba bậc nên không thể tự đẩy các con xuống bậc thấp hơn; còn đổi '
            'số tài khoản sẽ làm các con mất liên kết với mẹ.',
            'Muốn đổi thì phải chuyển hoặc xóa các tài khoản con trước.',
            'Hệ thống ghi rõ lý do ngay dưới ô bị khóa để người dùng biết vì sao không sửa được.',
        ]),
        ('Số tài khoản là duy nhất và chỉ nhận chữ số', [
            'Số tài khoản phải là duy nhất trên toàn danh mục.',
            'Chỉ nhận chữ số, độ dài từ 3 đến 15 chữ số.',
            'Khi sửa, bản ghi đang sửa được loại khỏi phép so trùng.',
        ]),
        ('Bản ghi đã Khóa thì không sửa và không xóa', [
            'Tài khoản ở trạng thái Khóa thì nút Sửa bị ẩn; muốn sửa phải Mở khóa trước.',
            'Máy chủ cũng từ chối mọi yêu cầu sửa và xóa trên bản ghi đang Khóa, kể cả khi gọi '
            'thẳng chức năng mà bỏ qua giao diện.',
            'Mở khóa là thao tác duy nhất được phép thực hiện trên bản ghi đang Khóa, bên cạnh '
            'các thao tác chỉ đọc.',
        ]),
        ('Khóa khác với Xóa', [
            'Khóa chỉ ngừng cho chọn tài khoản ở nghiệp vụ mới; dữ liệu và bút toán cũ giữ nguyên.',
            'Xóa là bỏ hẳn bản ghi khỏi danh mục và chỉ làm được khi tài khoản chưa phát sinh '
            'bút toán và không có tài khoản con.',
            'Khi không xóa được, nút Xóa bị ẩn hẳn chứ không hiện nút xám.',
        ]),
        ('Mọi thay đổi đều được ghi lịch sử', [
            'Thêm mới, sửa, xóa và đổi trạng thái đều ghi lại một dòng lịch sử kèm người thực '
            'hiện và thời điểm.',
            'Với thao tác sửa, hệ thống ghi từng trường đã đổi kèm giá trị trước và sau.',
            'Lịch sử sắp xếp mới nhất lên trước và không sửa hay xóa được.',
        ]),
        ('Nhập từ Excel phải qua bước kiểm tra', [
            'Quy trình bắt buộc ba bước: nạp tệp lên bảng xem trước, kiểm tra dữ liệu, rồi mới ghi.',
            'Nút ghi chỉ dùng được sau khi đã chạy kiểm tra.',
            'Hệ thống chỉ ghi các dòng hợp lệ; dòng lỗi giữ nguyên trên bảng kèm mô tả lỗi để '
            'người dùng sửa lại.',
        ]),
    ],
)

# ============================================================ DANH MỤC LOẠI TÀI KHOẢN
TYPE_ACCOUNT = dict(
    key='ltk',
    ten='Danh mục loại tài khoản',
    doi_tuong='loại tài khoản',
    route='/finance/type-accounts',
    host=HOST,
    menu='Phân hệ Tài chính → Danh mục → Danh mục loại tài khoản',
    quyen_quan_ly='Quản lý danh mục loại tài khoản',
    quyen_xem='Xem danh mục loại tài khoản',
    tacdung_ql=_TACDUNG_QL,
    tacdung_xem=_TACDUNG_XEM,
    ghichu_quyen=_GHICHU,
    co_trangthai=True,
    truong_trung='Mã loại tài khoản',
    loi_trung='Mã loại tài khoản đã tồn tại',
    loi_khac=['– Tên loại tài khoản trùng với bản ghi khác → hiển thị “Tên loại tài khoản '
              'đã tồn tại”.'],
    loi_import=[
        '– Dòng thiếu Mã loại tài khoản hoặc Tên loại tài khoản → đánh dấu lỗi.',
        '– Mã hoặc Tên đã có trong danh mục, hoặc trùng với dòng khác trong tệp → đánh dấu lỗi.',
    ],
    tb_them='Thêm mới loại tài khoản thành công',
    tb_sua='Cập nhật loại tài khoản thành công',
    tb_xoa='Xóa loại tài khoản thành công',
    dieu_kien_xoa='loại tài khoản chưa được gán cho tài khoản nào',
    dieu_kien_an_xoa='loại tài khoản đang được tài khoản sử dụng',
    cauhoi_xoa="Bạn có chắc muốn xóa loại tài khoản 'Loại tài khoản ví dụ 2'?",
    cauhoi_khoa="Bạn có chắc muốn mở khóa loại tài khoản 'Loại tài khoản ví dụ 2'?",
    muc_dich=[
        'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn quản lý Danh mục loại tài khoản.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ hai ràng buộc trùng độc lập nhau: trùng Mã và trùng Tên.',
        'Làm rõ khác biệt giữa Xóa và chuyển trạng thái Khóa.',
    ],
    thuat_ngu=[
        ('Loại tài khoản',
         'Nhóm phân loại tài khoản kế toán, dùng để gom các tài khoản có cùng bản chất. Mỗi '
         'tài khoản trong Danh mục tài khoản phải chọn đúng một loại.'),
        ('Mã loại tài khoản',
         'Mã do người dùng tự đặt, duy nhất trên toàn danh mục, được tự chuyển thành chữ in hoa '
         'khi lưu.'),
        ('Trạng thái Hoạt động', 'Loại tài khoản còn chọn được khi thêm hoặc sửa tài khoản.'),
        ('Trạng thái Khóa',
         'Loại tài khoản không còn chọn được cho tài khoản mới nhưng vẫn nằm trong danh mục và '
         'các tài khoản đang dùng nó không bị ảnh hưởng.'),
        ('Đang được sử dụng',
         'Loại tài khoản đã được gán cho ít nhất một tài khoản; khi đó không được phép xóa.'),
    ],
    cot=[
        ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
        ('Mã loại tài khoản', 'Mã định danh. Luôn hiển thị, sắp xếp được, bấm vào để mở cửa '
                              'sổ xem.'),
        ('Tên loại tài khoản', 'Tên đầy đủ của loại tài khoản, sắp xếp được.'),
        ('Ghi chú', 'Diễn giải thêm. Mặc định ẩn.'),
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
         'Chỉ hiện với người có quyền quản lý; mở cửa sổ Tạo loại tài khoản.'),
        ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn trường cần xuất.'),
        ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện với người có quyền quản lý.'),
        ('Nút Tùy chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ chọn cột hiển thị trên bảng.'),
    ],
    loc=[
        ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
         'Tìm đồng thời theo Mã và Tên loại tài khoản.'),
        ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Trống',
         'Bỏ trống thì hiện cả hai trạng thái.'),
        ('Người tạo', 'Dropdown', 'Danh sách', 'Trống', 'Lọc theo người đã thêm bản ghi.'),
        ('Người cập nhật', 'Dropdown', 'Danh sách', 'Trống', 'Lọc theo người sửa gần nhất.'),
        ('Cập nhật từ', 'Datepicker', 'dd/mm/yyyy', 'Trống',
         'Lọc bản ghi có ngày cập nhật từ mốc này trở đi.'),
        ('Cập nhật đến', 'Datepicker', 'dd/mm/yyyy', 'Trống',
         'Lọc bản ghi có ngày cập nhật đến hết mốc này.'),
    ],
    truong=[
        ('Mã loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Mã định danh, KHÔNG được trùng và được tự chuyển thành CHỮ IN HOA khi lưu. Bỏ trống '
         'báo “Bắt buộc phải nhập”; trùng báo “Mã loại tài khoản đã tồn tại”.'),
        ('Tên loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Tên đầy đủ, KHÔNG được trùng. Bỏ trống báo “Bắt buộc phải nhập”; trùng báo “Tên loại '
         'tài khoản đã tồn tại”.'),
        ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
         'Đặt sẵn là Hoạt động khi thêm mới.'),
        ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Diễn giải thêm, không bắt buộc và không kiểm tra trùng.'),
    ],
    tc_sheet='Danh muc loai tai khoan',
    tc_module='Tai chinh - Danh muc',
    tc_mucdich=(
        'Quan ly danh muc Loai tai khoan — nhom phan loai dung cho tung tai khoan ke toan. Man '
        'hinh cho phep tra cuu, tim kiem, them moi, chinh sua, xoa, khoa/mo khoa, nhap tu Excel, '
        'xuat Excel va xem lich su thay doi.'),
    tc_caudata=(
        '- Danh muc phang, khong phan cap cha con.\n'
        '- Moi loai tai khoan gom bon o: Ma, Ten, Trang thai va Ghi chu.\n'
        '- Ban ghi duoc tham chieu tu Danh muc tai khoan; day la can cu quyet dinh co xoa duoc '
        'hay khong.'),
    tc_dedupe=(
        '- Moi loai tai khoan chi hien MOT dong.\n'
        '- Ma va Ten deu la duy nhat, kiem tra TACH ROI nhau.\n'
        '- Khi sua, ban ghi dang sua duoc loai khoi ca hai phep kiem tra trung.'),
    tc_nguon=(
        'Du lieu lay tu danh muc Loai tai khoan. Cot Nguoi tao va Nguoi cap nhat lay ho ten '
        'nhan vien thuc hien thao tac.'),
    tc_luuy=[
        'Cac bay de sai nhat cua man nay, QA doc truoc khi test:',
        '- Man hinh dung HAI quyen tach roi. Nguoi chi co quyen xem VAN VAO DUOC man hinh.',
        '- Rang buoc trung ap cho CA Ma LAN Ten, kiem tra tach roi. Hai ban ghi khac ma nhung '
        'trung ten van bi chan.',
        '- Ma duoc tu chuyen thanh CHU IN HOA khi luu, nen "ltk001" va "LTK001" bi coi la trung.',
        '- Chi o Ten loai tai khoan bao loi do ngay duoi o khi bo trong; o Ma khong bao inline.',
        '- Ban ghi da Khoa thi khong duoc sua va khong duoc xoa; chi duoc Mo khoa.',
        '- Xoa va Khoa la hai viec khac nhau: Khoa van giu ban ghi trong danh sach.',
        '- Nut khong dung duoc phai AN HAN, khong phai hien nut xam.',
    ],
    hdsd_gioithieu=[
        'Danh mục loại tài khoản là nơi khai báo các nhóm phân loại dùng cho tài khoản kế toán. Mỗi tài khoản trong Danh mục tài khoản phải chọn đúng một loại.',
        'Mỗi loại gồm bốn thông tin: Mã, Tên, Trạng thái và Ghi chú. Mã và Tên đều phải là duy nhất, kiểm tra tách rời nhau.',
        'Loại tài khoản đã được gán cho tài khoản thì không xóa được nữa; muốn ngừng dùng thì chuyển sang trạng thái Khóa.',
    ],
    hdsd_loi=[
        ['Bắt buộc phải nhập', 'Bạn chưa nhập Mã loại tài khoản hoặc Tên loại tài khoản. Cả hai đều bắt buộc.'],
        ['Mã loại tài khoản đã tồn tại', 'Đã có loại khác dùng đúng mã này. Hệ thống tự chuyển mã thành chữ in hoa nên ltk001 và LTK001 bị coi là trùng nhau.'],
        ['Tên loại tài khoản đã tồn tại', 'Đã có loại khác mang đúng tên này. Hãy đặt tên khác.'],
    ],
    hdsd_faq=[
        ['Tôi đổi Mã rồi mà vẫn báo Tên đã tồn tại', 'Hai ràng buộc trùng kiểm tra tách rời nhau. Đổi mã không giúp gì cho tên, bạn phải đổi cả tên.'],
        ['Mã tôi nhập chữ thường mà lưu xong thành chữ hoa', 'Đúng theo thiết kế, để toàn danh mục thống nhất một kiểu.'],
        ['Dòng này không có nút Xóa', 'Loại tài khoản đó đang được gán cho ít nhất một tài khoản. Nếu chỉ muốn ngừng dùng, hãy bấm Khóa thay vì Xóa.'],
        ['Bản ghi đang Khóa mà tôi cần sửa', 'Bấm Mở khóa trước, sửa xong rồi Khóa lại nếu cần.'],
        ['Tôi không thấy nút Tạo mới và Import', 'Tài khoản của bạn chỉ có quyền xem danh mục loại tài khoản. Liên hệ quản trị viên để được cấp thêm quyền quản lý.'],
    ],
    shots=dict(danhsach='ltk_01_danhsach.png', boloc='ltk_02_boloc.png',
               taomoi='ltk_03_taomoi.png', validate='ltk_04_validate.png',
               xem='ltk_05_xem.png', sua='ltk_05_xem.png', lichsu='ltk_06_lichsu.png',
               xoa='ltk_07_xacnhan_xoa.png', khoa='ltk_08_xacnhan_mokhoa.png',
               xuat='ltk_10_xuat_excel.png', cot='ltk_11_cauhinh_cot.png',
               **{'import': 'ltk_09_import.png'}),
    funcs=[
        'list', 'filter', ('view', {'nhan': 'Xem chi tiết loại tài khoản', 'cot_bam': 'mã'}),
        'create', 'edit', 'delete', 'lock', 'history', 'import', 'export', 'columns',
    ],
    quy_tac=[
        ('Tách riêng quyền xem và quyền quản lý', [
            'Màn hình dùng hai quyền: “Quản lý danh mục loại tài khoản” cho mọi thao tác ghi và '
            '“Xem danh mục loại tài khoản” cho tra cứu, xuất Excel và xem lịch sử.',
            'Người chỉ có quyền xem không thấy nút Tạo mới, Sửa, Xóa, Khóa và Import.',
            'Mọi thao tác ghi đều kiểm tra lại quyền ở tầng máy chủ.',
        ]),
        ('Hai ràng buộc trùng độc lập nhau', [
            'Mã loại tài khoản phải là duy nhất trên toàn danh mục.',
            'Tên loại tài khoản cũng phải là duy nhất, kiểm tra tách rời với Mã.',
            'Hai bản ghi khác Mã nhưng trùng Tên vẫn bị chặn, và ngược lại.',
            'Khi sửa, bản ghi đang sửa được loại khỏi cả hai phép so trùng.',
        ]),
        ('Mã luôn được lưu bằng chữ in hoa', [
            'Hệ thống tự chuyển mã sang chữ in hoa trước khi kiểm tra trùng và trước khi lưu.',
            'Nhập “ltk001” hay “LTK001” đều cho cùng một giá trị nên bị coi là trùng nhau.',
        ]),
        ('Bản ghi đã Khóa thì không sửa và không xóa', [
            'Loại tài khoản ở trạng thái Khóa thì nút Sửa bị ẩn; muốn sửa phải Mở khóa trước.',
            'Máy chủ cũng từ chối mọi yêu cầu sửa và xóa trên bản ghi đang Khóa.',
            'Mở khóa là thao tác duy nhất được phép thực hiện trên bản ghi đang Khóa, bên cạnh '
            'các thao tác chỉ đọc.',
        ]),
        ('Khóa khác với Xóa', [
            'Khóa chỉ ngừng cho chọn loại tài khoản khi thêm hoặc sửa tài khoản; các tài khoản '
            'đang dùng nó vẫn giữ nguyên.',
            'Xóa là bỏ hẳn bản ghi và chỉ làm được khi loại tài khoản chưa được gán cho tài '
            'khoản nào.',
            'Khi không xóa được, nút Xóa bị ẩn hẳn chứ không hiện nút xám.',
        ]),
        ('Mọi thay đổi đều được ghi lịch sử', [
            'Bốn trường Mã, Tên, Ghi chú và Trạng thái đều được theo dõi thay đổi.',
            'Với thao tác sửa, hệ thống ghi từng trường đã đổi kèm giá trị trước và sau; riêng '
            'Trạng thái được ghi bằng nhãn tiếng Việt chứ không phải giá trị kỹ thuật.',
            'Lịch sử sắp xếp mới nhất lên trước và không sửa hay xóa được.',
        ]),
        ('Nhập từ Excel phải qua bước kiểm tra', [
            'Quy trình bắt buộc ba bước: nạp tệp lên bảng xem trước, kiểm tra dữ liệu, rồi mới ghi.',
            'Nút ghi chỉ dùng được sau khi đã chạy kiểm tra.',
            'Hệ thống chỉ ghi các dòng hợp lệ; dòng lỗi giữ nguyên kèm mô tả lỗi để sửa lại.',
        ]),
    ],
)

SCREENS = [ACCOUNT, TYPE_ACCOUNT]
