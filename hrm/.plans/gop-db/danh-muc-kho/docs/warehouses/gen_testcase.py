# -*- coding: utf-8 -*-
"""Testcase màn "Danh mục kho vật lý" theo KHUÔN CHUẨN tab "13. DM quốc gia" (03/11/2026).

Viết lại từ gen_testcase_v1.py (bản 02/11, khuôn cũ TC-ROLE / TẠO-SỬA-XEM / RÀNG BUỘC NHẬP LIỆU / E2E):
  - case nghiệp vụ riêng của màn lấy NGUYÊN VĂN từ v1 (hàm O), đưa vào đúng nhóm khuôn danh_muc;
  - case theo checklist "Mẫu tài liệu.xlsx" lấy từ _tc_dm_kho_chung.py (hàm G), điền theo cấu hình C;
  - sửa theo code: bộ lọc KHÔNG được giữ khi rời màn / F5 (v1 ghi "giữ 10 phút" là sai); Mã có khoảng trắng bị báo
    đỏ "Chỉ gồm chữ không dấu, số, dấu - và _" (v1 ghi "cắt khoảng trắng rồi lưu" là sai).
Chạy: python gen_testcase.py  (tự gọi check_tc.py, phải 0 lỗi)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
import _tc_dm_kho_chung as CH  # noqa: E402
from _tc_dm_kho_chung import K, O  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Danh mục kho vật lý'
V1, OLD = CH.load_v1(os.path.join(HERE, 'gen_testcase_v1.py'))
MENU = 'Phân hệ Kho => Danh mục => Kho vật lý'

C = dict(
    out=os.path.join(HERE, 'testcase - %s.xlsx' % TEN), ten=TEN, ngay='03/11/2026',
    menu=MENU, menu_item='Kho vật lý', title='Danh sách kho vật lý', obj='kho', label='kho vật lý',
    ma='Mã kho', tenf='Tên kho',
    A=('KHO-TEST-01', 'Kho test 01'), B=('KHO-TEST-02', 'Kho test 02'), K=('KHO-TEST-05', 'Kho test 05'),
    new=('KHO-TEST-20', 'Kho test 20'), new2=('KHO-TEST-21', 'Kho test 21'), new3=('KHO-TEST-22', 'Kho test 22'),
    new4=('KHO-TEST-23', 'Kho test 23'), imp=('KHO-IMP-01', 'Kho import 01'),
    mot_phan='test 0', tu_khoa_chung='KHO-TEST', ten_dau=('Kho Hà Nội test', 'kho ha noi test'),
    ten_dac_biet='Kho Hà Nội, khu A: tầng 1', ma_sai='Kho.Test 22',
    man_khac='Nhà kho', man_dung=('Phân hệ Kho => Danh mục => Nhà kho', 'Kho'),
    form_min=['Mã kho: KHO-TEST-21', 'Tên kho: Kho test 21', 'Địa chỉ: Số 21 Test', 'Thủ kho: NV-TK1',
              'Số nhà kho: 1'],
    form_hai_tab=['Mã kho: KHO-TEST-23', 'Tên kho: Kho test 23', 'Địa chỉ: Số 23 Test', 'Thủ kho: NV-TK1',
                  'Số nhà kho: 1'],
    title_tao='Tạo mới kho vật lý', title_xem='Xem chi tiết kho vật lý',
    dup='Đã tồn tại', trung_ghi_chu='trùng mã trên toàn hệ thống', trung_pham_vi='thuộc Công ty A',
    sort_cols=['Mã kho', 'Tên kho', 'Ngày tạo', 'Ngày cập nhật'],
    nosort_cols=['STT', 'Thủ kho', 'Công ty', 'Người tạo', 'Người cập nhật', 'Trạng thái', 'Hành động'],
    locked_cols=['STT', 'Mã kho', 'Hành động'], n_cols=14, cols_an=['Địa chỉ', 'Số nhà kho', 'Mô tả'],
    cot_tat='Công ty',
    K_lich_su='KHO-TEST-04', K_lich_su_ten='Kho test 04', dk_khoa='chưa có tồn',
    K_xoa='KHO-TEST-24', K_xoa_dk='vừa tạo, chưa từng có tồn',
    export_file='danh_sach_kho_vat_ly.xlsx',
    export_fields=['Mã kho', 'Tên kho', 'Địa chỉ', 'Thủ kho', 'Công ty', 'Số nhà kho', 'Mô tả', 'Trạng thái',
                   'Người tạo', 'Ngày tạo', 'Người cập nhật', 'Ngày cập nhật'],
    import_title='Import kho vật lý', import_ok='Import thành công {n} kho vật lý.', import_cot_xoa='Địa chỉ',
    import_header_err='File không đúng mẫu: thiếu header Mã kho */Tên kho */Địa chỉ */Mã thủ kho */Số nhà kho */'
                      'Trạng thái/Mô tả (sheet Data).',
)
G = CH.gen(C)


def o(sec, num, **ov):
    return O(OLD, sec, num, **ov)


NHA = 'Phân hệ Kho => Danh mục => Nhà kho'
KKT = 'Phân hệ Kho => Danh mục => Kho kế toán'

# ------------------------------------------------------------------ mô tả: giữ v1, sửa câu sai theo code
DESC = []
for k, v in V1.DESCRIPTION_BLOCK:
    v = v.replace('Không có bộ lọc theo Ngày cập nhật. Hệ thống ghi nhớ bộ lọc trong 10 phút khi rời màn rồi quay lại.',
                  'Không có bộ lọc theo Ngày cập nhật. Bộ lọc KHÔNG được giữ khi rời sang màn khác, tải lại trang (F5) '
                  'hay mở tab mới: quay lại là về mặc định.')
    v = v.replace('Mã, tên, địa chỉ được cắt khoảng trắng đầu / cuối trước khi kiểm tra.',
                  'Tên, địa chỉ được cắt khoảng trắng đầu / cuối trước khi kiểm tra; Mã có khoảng trắng bị báo đỏ '
                  '(chỉ nhận chữ không dấu, số, dấu - và _). So trùng không phân biệt chữ hoa / thường.')
    v = v.replace('- TK-SA: Super admin.', '- TK-SA: Super admin.\n- TK-H: nhân viên thứ hai của Công ty A, có quyền '
                  '"Quản lý kho" (dùng cho các case 2 người thao tác cùng lúc).')
    v = CH._bo_ma(v)
    DESC.append((k, v))

# ------------------------------------------------------------------ I. HIỂN THỊ TRANG & TRUY CẬP
S_HIEN = [
    o('S1', '001', func='Mở màn hình từ menu',
      steps=['1. Đăng nhập bằng TK-A', '2. Vào menu ' + MENU]),
    o('S1', '002', func='Các ô lọc và các nút chức năng được hiển thị', pre='Vừa vào màn từ menu, chưa đặt bộ lọc'),
    o('S1', '003', func='Kiểm tra đủ các cột mặc định của bảng'),
    o('S1', '004', func='Các cột mặc định ẩn: bật lên và đọc giá trị'),
    o('S1', '005', func='Dữ liệu đúng với dữ liệu đã tạo'),
    G['h_trangthai'],
    o('S1', '007'),
    o('S3', '007'),
    G['h_rong_dm'], G['h_khong_khop'],
    G['h_so_dong_md'], G['h_doi_so_dong'], G['h_truoc_sau'], G['h_dau_cuoi'], G['h_nut_mo'], G['h_stt'],
    G['h_tong'], G['h_loc_ve_1'],
    o('S3', '001', func='Thứ tự mặc định khi mở màn: kho tạo mới nhất lên đầu'),
    G['h_sx_ma'], G['h_sx_ten'], G['h_sx_ngay'], G['h_khong_sx'], G['h_sx_giu'], G['h_sx_ve_1'],
]

# ------------------------------------------------------------------ II. TÌM KIẾM & LỌC DANH SÁCH
S_TIM = [
    G['t_chinh_xac'],
    o('S2', '001', func='Tìm theo một phần Mã kho, không phân biệt hoa thường'),
    o('S2', '002', func='Tìm theo Tên kho'),
    o('S2', '003', func='Tìm theo tên Người tạo'),
    G['t_dau'],
    o('S2', '015', func='Tìm với ký tự đặc biệt'),
    G['t_khoang_trang'], G['t_gioi_han'], G['t_xoa'],
    o('S2', '004', func='Ô tìm kiếm chỉ lọc khi nhấn Enter hoặc bấm Tìm kiếm'),
    G['t_md'],
    o('S2', '005'), o('S2', '014'), o('S2', '010'), o('S2', '006'), o('S2', '007'), o('S2', '008'), o('S2', '009'),
    o('S2', '011'),
    o('S2', '012', func='Kết hợp tìm kiếm với nhiều ô lọc rồi bấm Làm mới'),
    G['t_tong_loc'], G['t_trang_loc'], G['t_sx_loc'], G['t_lam_moi_tong'],
    o('S2', '016'),
    G['t_chuyen_man'], G['t_f5'], G['t_tab'], G['t_tk_khac'],
]

# ------------------------------------------------------------------ III. THÊM MỚI
S_THEM = [
    o('S4', '001', func='Mở cửa sổ Tạo mới - đúng ô, nút và giá trị mặc định'),
    o('S4', '002', func='Thêm mới đủ thông tin hợp lệ'),
    o('S4', '003'),
    G['a_chi_bat_buoc'], G['a_lich_su'],
    o('S4', '005'), o('S4', '006'),
    o('S10', '001', func='Bỏ trống mọi ô bắt buộc thì bị chặn'),
    o('S10', '006', func='Mã kho sai định dạng thì báo lỗi'),
    G['a_loi_mat'],
    o('S10', '002', func='Trùng Mã kho với kho của công ty khác bị chặn'),
    o('S10', '003', func='Trùng Tên kho bị chặn'),
    o('S10', '004', func='Trùng mã với kho đã xóa (bị ẩn) vẫn bị chặn',
      pre='KHO-TEST-XOA đã bị xóa (đã có nhà kho nên chỉ bị ẩn), không còn hiện ở danh sách'),
    G['a_ma_khoang_trang'], G['a_chi_khoang_trang'], G['a_dung_max'],
    o('S10', '007', func='Vượt độ dài tối đa: Mã kho 50, Tên kho và Địa chỉ 255 ký tự'),
    o('S10', '008', func='Mô tả vượt 500 ký tự thì báo lỗi'),
    o('S10', '009', func='Số nhà kho chỉ nhận số nguyên từ 1 đến 999'),
    o('S4', '004', func='Lưu & Tiếp tục với dữ liệu hợp lệ giữ cửa sổ mở'),
    G['a_ltt_thieu'], G['a_ltt_sai'], G['a_ltt_trung'], G['a_ltt_dong'],
    o('S4', '019', func='Bấm Đóng khi chưa nhập thông tin nào'),
    G['a_dong'], G['a_x'], G['a_xoa_het'], G['a_de_lau'],
    o('S10', '012', func='Bấm Lưu liên tục nhiều lần không sinh kho trùng'),
    G['a_hai_tab'],
]

# ------------------------------------------------------------------ IV. CHỈNH SỬA
S_SUA = [
    o('S4', '007', func='Mở cửa sổ Sửa - dữ liệu điền sẵn, ô và nút'),
    o('S4', '008', func='Sửa nhiều trường và lưu thành công'),
    G['e_mot_truong'],
    o('S4', '009'), o('S4', '010'), o('S4', '011'), o('S4', '012'), o('S4', '013'),
    o('S10', '011', func='Giữ nguyên mã / tên của chính mình khi sửa'),
    G['e_trong'],
    o('S10', '010', func='Bỏ hết Thủ kho khi sửa thì bị chặn'),
    G['e_sai'], G['e_vuot'], G['e_trung'], G['e_loi_mat'], G['e_ls'],
    G['e_khong_doi'], G['e_tra_lai'],
    o('S4', '018', func='Bấm Đóng khi đã thay đổi - chọn Ở lại / Thoát'),
    G['e_khong_ls'],
    o('S4', '015', func='Kho đã Khóa không sửa được'),
    o('S4', '017', func='Kho còn tồn: ô Trạng thái trong cửa sổ Sửa bị khóa kèm giải thích'),
    o('S4', '020', func='Mở Sửa kho đã bị người khác xóa'),
    G['e_dong_thoi'],
]

# ------------------------------------------------------------------ V. XÓA
S_XOA = [
    o('S6', '001', func='Xóa kho mới tạo (còn nhà kho tự sinh): kho bị ẩn, mã không dùng lại được'),
    o('S6', '009', func='Bấm Hủy thì không xóa'),
    o('S6', '002', func='Xóa hẳn kho không còn dữ liệu liên quan'),
    o('S6', '003'), o('S6', '004'), o('S6', '005'), o('S6', '006'), o('S6', '007'),
    o('S6', '008', func='Xóa kho đã bị người khác xóa'),
]

# ------------------------------------------------------------------ VI. KHÓA / MỞ KHÓA
S_KHOA = [
    o('S5', '001', func='Khóa kho chưa có tồn'),
    o('S5', '005', func='Bấm Hủy ở hộp xác nhận khóa'),
    o('S5', '002'), o('S5', '003'),
    o('S4', '016'),
    o('S5', '004', func='Mở khóa kho'),
    G['k_huy_mo'],
    o('S5', '006', func='Khóa kho đã bị người khác khóa'),
    G['k_mo_dong_thoi'], G['k_bi_xoa'],
    o('S5', '007', func='Kho Khóa không chọn được ở màn Nhà kho, mở khóa thì chọn lại được'),
]

# ------------------------------------------------------------------ VII. LỊCH SỬ THAY ĐỔI
S_LS = [
    G['l_mo'], G['l_bo_loc'], G['l_loai'], G['l_nguoi'], G['l_tg'], G['l_ket_hop'], G['l_khong_kq'],
    G['l_lam_moi'], G['l_dong_loc'], G['l_thu_tu'],
    o('S9', '001', func='Lịch sử ngay sau khi Tạo mới'),
    G['l_mot_truong'],
    o('S9', '002', func='Lịch sử khi sửa nhiều trường ghi giá trị cũ và mới'),
    o('S9', '003', func='Lịch sử Khóa / Mở khóa, lọc theo loại hành động'),
    G['l_import'], G['l_trang_thai_va_ten'],
    o('S9', '004', func='Lịch sử của kho đang Khóa'),
    o('S9', '005', func='Lịch sử xem từ cửa sổ Xem chi tiết'),
    G['l_dong'],
]

# ------------------------------------------------------------------ VIII. XEM CHI TIẾT KHO VẬT LÝ
S_XEM = [
    o('S1', '006', func='Mở cửa sổ Xem bằng cách bấm Mã kho'),
    o('S4', '014', func='Cửa sổ Xem chi tiết: tiêu đề, các ô, khối Lịch sử'),
    G['v_khop'], G['v_chi_doc'], G['v_khoa'], G['v_dong'],
]

# ------------------------------------------------------------------ IX. TÙY CHỈNH CỘT
S_COT = [G['c_mo'], G['c_hien'], G['c_an'], G['c_bat_buoc'], G['c_keo'], G['c_co_dinh'], G['c_dong'], G['c_nho'],
         G['c_tk'], G['c_du_lieu']]

# ------------------------------------------------------------------ X. XUẤT DANH SÁCH EXCEL
S_XUAT = [
    o('S7', '001', func='Mở cửa sổ chọn trường xuất file'),
    G['x_md'],
    o('S7', '002', func='Xuất theo đúng bộ lọc đang áp dụng, lấy tất cả các trang'),
    G['x_mot_so'],
    o('S7', '005', func='Không chọn trường nào thì không xuất được; chọn tất cả và đổi thứ tự'),
    G['x_tim'],
    o('S7', '004', func='Người thường chỉ xuất được kho của công ty mình'),
    G['x_rong'],
    o('S7', '003', func='Dữ liệu trong file khớp danh sách'),
    G['x_ten_cot'], G['x_dinh_dang'],
]

# ------------------------------------------------------------------ XI. IMPORT TỪ FILE EXCEL
S_IMP = [
    o('S8', '001'), o('S8', '002', func='Tải lên file đúng mẫu, Load lên bảng xem trước'),
    G['i_sai_dinh_dang'], G['i_thieu_cot'], G['i_sai_ten_cot'], G['i_rong'], G['i_dong_trong'],
    o('S8', '007', func='File vượt quá 500 dòng'),
    o('S8', '003', func='Kiểm tra dữ liệu - báo lỗi từng dòng: trống, sai định dạng, trùng hệ thống, trùng trong file'),
    o('S8', '004', func='Kiểm tra dữ liệu - mã thủ kho của nhân viên đã nghỉ việc'),
    G['i_vuot_do_dai'], G['i_khoang_trang_hoa'],
    o('S8', '006', func='Sửa dòng lỗi trên bảng rồi Validate lại; Xoá trạng thái validate'),
    G['i_tron'], G['i_khong_hop_le'],
    o('S8', '005', func='Bỏ dòng lỗi rồi Import thành công'),
    G['i_tat_ca_hop_le'],
    o('S8', '009', func='Đóng / Làm mới cửa sổ Import không ghi dữ liệu'),
    G['i_lai_file'],
    o('S8', '008', func='Kho bị người khác tạo sau lúc Validate thì dòng đó bị bỏ qua'),
    G['i_dong_thoi'], G['i_man_khac'],
]

# ------------------------------------------------------------------ XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S_RB = [
    o('S11', '001', func='Vòng đời một kho từ lúc tạo tới lúc xóa'),
    o('S11', '002', func='Kho dùng tiếp ở các màn con và màn nghiệp vụ'),
    K('Kho mới tạo có ngay ở ô chọn Kho của màn Nhà kho và Kho vật lý của màn Kho kế toán', 'P0',
      'Vừa tạo mới kho KHO-TEST-20 (Hoạt động).',
      ['Vào menu ' + NHA + ', bấm Tạo mới, mở ô Kho', 'Vào menu ' + KKT + ', bấm Tạo mới, mở ô Kho vật lý'],
      'Kho: KHO-TEST-20',
      ['Cả 2 ô chọn đều có "KHO-TEST-20 - Kho test 20"', 'Không cần tải lại trang'])
    ,
    K('Đổi tên kho thì các màn liên quan hiện tên mới', 'P0',
      'KHO-TEST-01 đang có nhà kho N1 và được gắn vào 1 kho kế toán.',
      ['Sửa KHO-TEST-01, đổi Tên kho thành "Kho test 01 mới", Lưu', 'Vào ' + NHA + ', tìm nhà kho của KHO-TEST-01',
       'Vào ' + KKT + ', tìm kho kế toán đang gắn KHO-TEST-01'], 'Tên kho: Kho test 01 mới',
      ['Cột Kho ở màn Nhà kho và cột Kho vật lý ở màn Kho kế toán đều hiện "Kho test 01 mới"',
       'Không màn nào còn hiện tên cũ'])
    ,
    K('Khóa kho không làm mất liên kết của nhà kho và kho kế toán đang gắn', 'P0',
      'KHO-TEST-02 (chưa có tồn) có nhà kho N1 và được gắn vào 1 kho kế toán.',
      ['Khóa KHO-TEST-02', 'Vào ' + NHA + ', xem nhà kho N1 của KHO-TEST-02, mở cửa sổ Xem',
       'Vào ' + KKT + ', mở Sửa kho kế toán đang gắn KHO-TEST-02, sửa Mô tả rồi Lưu', 'Mở khóa lại KHO-TEST-02'],
      '',
      ['Nhà kho N1 vẫn hiện đúng tên kho, ô Kho trong cửa sổ Xem có biểu tượng ổ khóa trước tên',
       'Kho kế toán lưu được, vẫn giữ kho vật lý KHO-TEST-02 (hiện kèm biểu tượng khóa)',
       'Nhà kho của kho đang Khóa không mở khóa được cho tới khi mở khóa kho'])
    ,
    K('Bộ lọc Kho ở các màn danh mục cấp dưới cập nhật theo danh mục kho', 'P1',
      'Vừa tạo mới kho KHO-TEST-20 (Hoạt động) và khóa KHO-TEST-05.',
      ['Lần lượt vào các màn Phân hệ Kho => Danh mục => Nhà kho, Dãy, Khoang, Vị trí', 'Ở mỗi màn mở ô lọc Kho'],
      'Kho: KHO-TEST-20 (Hoạt động), KHO-TEST-05 (Khóa)',
      ['Ở cả 4 màn, ô lọc Kho có KHO-TEST-20',
       'Ô lọc Kho mặc định không có KHO-TEST-05; bật biểu tượng ổ khóa trên nhãn ô thì có'])
    ,
    K('Xóa kho thì ô chọn Kho ở các màn liên quan không còn kho đó', 'P1',
      'KHO-TEST-07 vừa bị xóa (còn nhà kho tự sinh nên chỉ bị ẩn).',
      ['Vào ' + NHA + ', bấm Tạo mới, mở ô Kho', 'Vào ' + KKT + ', bấm Tạo mới, mở ô Kho vật lý'], '',
      ['Hai ô chọn đều KHÔNG còn KHO-TEST-07', 'Hai màn mở bình thường, không báo lỗi'])
    ,
]

# ------------------------------------------------------------------ XIII. PHÂN QUYỀN
S_QUYEN = [
    o('ROLE', '00'), o('ROLE', '01'), o('ROLE', '02'), G['q_mot_quyen'],
    o('ROLE', '03', func='Phạm vi dữ liệu: người thường chỉ thấy kho của công ty mình'),
    o('ROLE', '04', func='Phạm vi dữ liệu: Super admin thấy kho mọi công ty và có ô lọc Công ty'),
    o('ROLE', '05', func='Phạm vi dữ liệu: tài khoản không xác định được công ty thì không thấy kho nào'),
    G['q_doi_quyen'],
]

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', S_HIEN),
    ('TÌM KIẾM & LỌC DANH SÁCH', S_TIM),
    ('THÊM MỚI', S_THEM),
    ('CHỈNH SỬA', S_SUA),
    ('XÓA', S_XOA),
    ('KHÓA / MỞ KHÓA', S_KHOA),
    ('LỊCH SỬ THAY ĐỔI', S_LS),
    ('XEM CHI TIẾT KHO VẬT LÝ', S_XEM),
    ('TÙY CHỈNH CỘT', S_COT),
    ('XUẤT DANH SÁCH EXCEL', S_XUAT),
    ('IMPORT TỪ FILE EXCEL', S_IMP),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S_RB),
    ('PHÂN QUYỀN', S_QUYEN),
]

if __name__ == '__main__':
    CH.build(C, GROUPS, DESC)
    print('So nhom:', len(GROUPS), '| so case cu (v1): %d' % len(OLD))
