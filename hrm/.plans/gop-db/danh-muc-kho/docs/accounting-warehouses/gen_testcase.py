# -*- coding: utf-8 -*-
"""Testcase màn "Danh mục kho kế toán" theo KHUÔN CHUẨN tab "13. DM quốc gia" (03/11/2026).

Viết lại từ gen_testcase_v1.py (bản 02/11, khuôn cũ TC-ROLE / TẠO-SỬA-XEM / RÀNG BUỘC NHẬP LIỆU / E2E):
  - case nghiệp vụ riêng của màn lấy NGUYÊN VĂN từ v1 (hàm O), đưa vào đúng nhóm khuôn danh_muc;
  - case theo checklist "Mẫu tài liệu.xlsx" lấy từ ../warehouses/_tc_dm_kho_chung.py (hàm G), điền theo cấu hình C;
  - sửa theo code: bộ lọc KHÔNG được giữ khi rời màn / F5 (v1 "ghi nhớ 10 phút" bỏ); Mã có khoảng trắng bị báo đỏ
    "Chỉ gồm chữ không dấu, số, dấu - và _", Mã chỉ toàn khoảng trắng cũng vậy (v1 ghi "cắt khoảng trắng rồi lưu" /
    "Bắt buộc phải nhập" là sai).
Chạy: python gen_testcase.py  (tự gọi check_tc.py, phải 0 lỗi)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'warehouses'))
sys.path.insert(0, os.path.join(HERE, '..'))
import _tc_dm_kho_chung as CH  # noqa: E402
from _tc_dm_kho_chung import K, O  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Danh mục kho kế toán'
V1, OLD = CH.load_v1(os.path.join(HERE, 'gen_testcase_v1.py'))
MENU = 'Phân hệ Kho => Danh mục => Kho kế toán'
QC = 'Phân hệ Tài chính => Khai Quy chế – Cấu hình'

C = dict(
    out=os.path.join(HERE, 'testcase - %s.xlsx' % TEN), ten=TEN, ngay='03/11/2026',
    menu=MENU, menu_item='Kho kế toán', title='Danh sách kho kế toán', obj='kho kế toán', label='kho kế toán',
    ma='Mã kho kế toán', tenf='Tên kho kế toán',
    A=('KKT-TEST-01', 'Kho KT test 01'), B=('KKT-TEST-02', 'Kho KT test 02'), K=('KKT-TEST-05', 'Kho KT test 05'),
    new=('KKT-TEST-30', 'Kho KT test 30'), new2=('KKT-TEST-31', 'Kho KT test 31'),
    new3=('KKT-TEST-32', 'Kho KT test 32'), new4=('KKT-TEST-33', 'Kho KT test 33'),
    imp=('KKT-IMP-01', 'Kho KT import 01'),
    mot_phan='KT test 0', tu_khoa_chung='KKT-TEST', ten_dau=('Kho kế toán Hà Nội test', 'kho ke toan ha noi test'),
    ten_dac_biet='Kho HN, tầng 2: khu A', ma_sai='KKT.Test 32',
    man_khac='Kho vật lý', man_dung=(QC + ' (Công ty A)', 'Kho khuyến mại'),
    form_min=['Mã kho kế toán: KKT-TEST-31', 'Tên kho kế toán: Kho KT test 31', 'Nhập xuất thẳng: không tích',
              'Kho vật lý: KVL-TEST-A', 'Địa chỉ: 31 Trần Phú', 'Kế toán kho: KT1'],
    form_hai_tab=['Mã kho kế toán: KKT-TEST-33', 'Tên kho kế toán: Kho KT test 33', 'Nhập xuất thẳng: tích',
                  'Kế toán kho: KT1'],
    title_tao='Tạo mới kho kế toán', title_xem='Xem chi tiết kho kế toán',
    dup='Đã tồn tại', trung_ghi_chu='trùng mã trên toàn hệ thống', trung_pham_vi='thuộc Công ty A',
    sort_cols=['Mã kho kế toán', 'Tên kho kế toán', 'Ngày tạo', 'Ngày cập nhật'],
    nosort_cols=['STT', 'Kho vật lý', 'Kế toán kho', 'Công ty', 'Người tạo', 'Người cập nhật', 'Trạng thái',
                 'Hành động'],
    locked_cols=['STT', 'Mã kho kế toán', 'Hành động'], n_cols=15, cols_an=['Nhập xuất thẳng', 'Địa chỉ', 'Mô tả'],
    cot_tat='Công ty',
    K_lich_su='KKT-TEST-14', K_lich_su_ten='Kho KT test 14', dk_khoa='không có tồn',
    K_xoa='KKT-TEST-34', K_xoa_dk='vừa tạo, chưa được dùng ở đâu',
    export_file='danh_sach_kho_ke_toan.xlsx',
    export_fields=['Mã kho kế toán', 'Tên kho kế toán', 'Kho vật lý', 'Nhập xuất thẳng', 'Địa chỉ', 'Kế toán kho',
                   'Công ty', 'Mô tả', 'Trạng thái', 'Người tạo', 'Ngày tạo', 'Người cập nhật', 'Ngày cập nhật'],
    import_title='Import kho kế toán', import_ok='Import thành công {n} kho kế toán.', import_cot_xoa='Mã kế toán kho',
    import_header_err='File không đúng mẫu: thiếu header Mã kho kế toán */Tên kho kế toán */Nhập xuất thẳng/'
                      'Mã kho vật lý/Địa chỉ/Mã kế toán kho */Trạng thái/Mô tả (sheet Data).',
)
G = CH.gen(C)


def o(sec, num, **ov):
    return O(OLD, sec, num, **ov)


# ------------------------------------------------------------------ mô tả: giữ v1, sửa câu sai theo code
DESC = []
for k, v in V1.DESCRIPTION_BLOCK:
    v = v.replace('Không có bộ lọc theo Ngày cập nhật. Hệ thống ghi nhớ bộ lọc trong 10 phút khi rời màn rồi quay lại.',
                  'Không có bộ lọc theo Ngày cập nhật. Bộ lọc KHÔNG được giữ khi rời sang màn khác, tải lại trang (F5) '
                  'hay mở tab mới: quay lại là về mặc định.')
    v = v.replace('- So trùng sau khi đã cắt khoảng trắng 2 đầu, không phân biệt chữ hoa / thường.',
                  '- So trùng không phân biệt chữ hoa / thường; Tên được cắt khoảng trắng 2 đầu, Mã có khoảng trắng bị '
                  'báo đỏ (chỉ nhận chữ không dấu, số, dấu - và _).')
    v = v.replace('- TK-Z: nhân viên Công ty A, KHÔNG có quyền "Quản lý kho".',
                  '- TK-Z: nhân viên Công ty A, KHÔNG có quyền "Quản lý kho".\n- TK-H: nhân viên thứ hai của Công ty A, '
                  'có quyền "Quản lý kho" (dùng cho các case 2 người thao tác cùng lúc).')
    DESC.append((k, CH._bo_ma(v)))

# ------------------------------------------------------------------ I. HIỂN THỊ TRANG & TRUY CẬP
S_HIEN = [
    o('S1', '001', func='Mở màn hình từ menu', steps=['1. Đăng nhập bằng TK-A', '2. Vào menu ' + MENU]),
    o('S1', '002', func='Kiểm tra đủ các cột mặc định của bảng'),
    o('S1', '003', func='Dữ liệu một dòng đúng với dữ liệu đã tạo'),
    o('S1', '004', func='Kho Nhập xuất thẳng: ô Kho vật lý để trống; các cột mặc định ẩn'),
    o('S1', '005', func='Dòng Khóa và chữ dài'),
    G['h_trangthai'], G['h_rong_dm'],
    o('S1', '007', func='Hiển thị khi không có dữ liệu khớp'),
    G['h_so_dong_md'], G['h_doi_so_dong'], G['h_truoc_sau'], G['h_dau_cuoi'], G['h_nut_mo'], G['h_stt'],
    G['h_tong'], G['h_loc_ve_1'],
    o('S3', '001', func='Thứ tự mặc định khi mở màn: kho tạo mới nhất lên đầu'),
    G['h_sx_ma'], G['h_sx_ten'], G['h_sx_ngay'], G['h_khong_sx'], G['h_sx_giu'], G['h_sx_ve_1'],
]

# ------------------------------------------------------------------ II. TÌM KIẾM & LỌC DANH SÁCH
S_TIM = [
    G['t_chinh_xac'],
    o('S2', '001', func='Tìm theo một phần mã, chỉ lọc khi nhấn Enter'),
    o('S2', '002', func='Tìm theo tên và theo người tạo'),
    G['t_dau'],
    o('S2', '003', func='Tìm với ký tự đặc biệt và chỉ toàn khoảng trắng'),
    G['t_khoang_trang'], G['t_gioi_han'], G['t_xoa'], G['t_md'],
    o('S2', '009', func='Các ô lọc của khu vực Tìm kiếm nâng cao'),
    o('S2', '004', func='Lọc theo Trạng thái'), o('S2', '005', func='Lọc theo Người tạo'),
    o('S2', '006', func='Lọc theo Ngày tạo, tính cả 2 đầu mút'), o('S2', '010'),
    o('S2', '007', func='Kết hợp tìm kiếm với ô lọc rồi bấm Làm mới'),
    G['t_tong_loc'], G['t_trang_loc'], G['t_sx_loc'], G['t_lam_moi_tong'],
    o('S2', '011'),
    G['t_chuyen_man'], G['t_f5'], G['t_tab'], G['t_tk_khac'],
]

# ------------------------------------------------------------------ III. THÊM MỚI
S_THEM = [
    o('S4', '001', func='Thêm mới kho thường đủ thông tin hợp lệ', steps=[
        '1. Vào menu ' + MENU, '2. Bấm nút "Tạo mới" (mở cửa sổ "Tạo mới kho kế toán")',
        '3. Nhập Mã, Tên; KHÔNG tích Nhập xuất thẳng; chọn Kho vật lý, nhập Địa chỉ; chọn Kế toán kho KT1; '
        'Trạng thái để Hoạt động; nhập Mô tả', '4. Bấm "Lưu"']),
    o('S4', '002', func='Thêm mới kho Nhập xuất thẳng'),
    o('S4', '003'), o('S4', '004'), o('S4', '005'),
    G['a_chi_bat_buoc'], G['a_lich_su'],
    o('S4', '008'),
    o('S10', '001', func='Bỏ trống các ô bắt buộc (kho thường) thì bị chặn'),
    o('S10', '002', func='Bỏ trống khi Nhập xuất thẳng chỉ đòi Mã, Tên, Kế toán kho'),
    o('S10', '012', func='Mã kho kế toán sai định dạng thì báo lỗi'),
    G['a_loi_mat'],
    o('S10', '003', func='Trùng mã bị chặn (mọi công ty, không phân biệt hoa thường)'),
    o('S10', '004', func='Trùng tên bị chặn'),
    G['a_ma_khoang_trang'], G['a_chi_khoang_trang'], G['a_dung_max'],
    o('S10', '007', func='Vượt độ dài tối đa: Mã 50, Tên và Địa chỉ 255 ký tự'),
    o('S10', '008', func='Mô tả vượt 500 ký tự thì báo lỗi'),
    o('S10', '009', func='Tên có dấu phẩy, dấu hai chấm vẫn lưu được'),
    o('S10', '011', func='Chọn kho vật lý vừa bị người khác khóa thì bị chặn'),
    o('S4', '018'),
    o('S4', '006', func='Lưu & Tiếp tục với dữ liệu hợp lệ giữ cửa sổ mở'),
    G['a_ltt_thieu'], G['a_ltt_sai'], G['a_ltt_trung'], G['a_ltt_dong'],
    o('S4', '017', func='Bấm Đóng khi chưa nhập thông tin nào'),
    o('S4', '007', func='Bấm Đóng khi đã nhập thông tin - chọn Ở lại / Thoát'),
    G['a_x'], G['a_xoa_het'], G['a_de_lau'],
    o('S10', '013', func='Bấm Lưu liên tục nhiều lần không sinh kho trùng'),
    G['a_hai_tab'],
]

# ------------------------------------------------------------------ IV. CHỈNH SỬA
S_SUA = [
    o('S4', '009', func='Mở cửa sổ Sửa và sửa nhiều trường thành công'),
    G['e_mot_truong'],
    o('S4', '010'), o('S4', '011'), o('S4', '012'), o('S4', '013'), o('S4', '014'), o('S4', '016'),
    o('S10', '010', func='Giữ mã của chính mình thì lưu được, đổi sang mã kho khác thì bị chặn'),
    G['e_trong'], G['e_sai'], G['e_vuot'], G['e_loi_mat'], G['e_ls'],
    G['e_khong_doi'], G['e_tra_lai'],
    K('Bấm Đóng khi đã thay đổi - chọn Ở lại / Thoát', 'P1', 'Đang mở cửa sổ Sửa KKT-TEST-02.',
      ['Đổi Mô tả, bấm Đóng', 'Bấm "Ở lại"', 'Bấm Đóng lần nữa, bấm "Thoát"', 'Mở Sửa lại KKT-TEST-02'],
      'Mô tả: Đang sửa dở',
      ['Bước 1: hiện hộp "Thông tin chưa lưu" nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", nút '
       'Thoát / Ở lại', 'Bước 2: quay lại cửa sổ, chữ vừa gõ còn nguyên',
       'Bước 3: cửa sổ đóng, danh sách không đổi', 'Bước 4: thấy dữ liệu đã lưu, không còn chữ vừa gõ']),
    G['e_khong_ls'],
    K('Kho đang Khóa không sửa được', 'P0', 'KKT-TEST-05 đang Khóa.',
      ['Quan sát cột Hành động của KKT-TEST-05', 'Bấm vào mã KKT-TEST-05'], '',
      ['KHÔNG có nút Sửa, KHÔNG có nút Xóa; có Mở khóa và Lịch sử',
       'Cửa sổ Xem vẫn mở được, mọi ô chỉ đọc', 'Muốn sửa phải Mở khóa trước']),
    o('S4', '019', func='Mở Sửa kho đã bị người khác xóa'),
    G['e_dong_thoi'],
]

# ------------------------------------------------------------------ V. XÓA
S_XOA = [
    o('S6', '001', func='Xóa kho chưa dùng ở đâu'),
    o('S6', '007', func='Bấm Hủy thì không xóa'),
    o('S6', '002'), o('S6', '003'), o('S6', '004'), o('S6', '005'), o('S6', '006'),
    o('S6', '008', func='Xóa kho đã bị người khác xóa / vừa bị khóa'),
]

# ------------------------------------------------------------------ VI. KHÓA / MỞ KHÓA
S_KHOA = [
    o('S5', '001'), o('S5', '002', func='Bấm Hủy ở hộp xác nhận khóa'),
    o('S5', '003'), o('S5', '004'), o('S5', '007'), o('S5', '006'),
    o('S5', '005', func='Mở khóa kho'),
    G['k_huy_mo'],
    o('S5', '008', func='Khóa kho đã bị người khác khóa'),
    G['k_mo_dong_thoi'], G['k_bi_xoa'],
    K('Kho kế toán Khóa không chọn được ở màn liên quan, mở khóa thì chọn lại được', 'P1',
      'KKT-TEST-05 đang Khóa.',
      ['Mở ' + QC + ' của Công ty A, mở ô "Kho khuyến mại", tìm KKT-TEST-05', 'Mở khóa KKT-TEST-05',
       'Mở lại ô "Kho khuyến mại", tìm KKT-TEST-05'], '',
      ['Bước 1: KHÔNG có KKT-TEST-05 trong ô chọn', 'Bước 3: KKT-TEST-05 có lại trong ô chọn']),
]

# ------------------------------------------------------------------ VII. LỊCH SỬ THAY ĐỔI
S_LS = [
    G['l_mo'], G['l_bo_loc'], G['l_loai'], G['l_nguoi'], G['l_tg'], G['l_ket_hop'], G['l_khong_kq'],
    G['l_lam_moi'], G['l_dong_loc'], G['l_thu_tu'],
    o('S9', '001', func='Lịch sử ngay sau khi Tạo mới'),
    G['l_mot_truong'],
    o('S9', '002', func='Lịch sử khi sửa nhiều trường ghi giá trị cũ và mới bằng chữ'),
    o('S9', '003', func='Lịch sử đổi Nhập xuất thẳng, Khóa / Mở khóa'),
    G['l_import'], G['l_trang_thai_va_ten'],
    o('S9', '004', func='Lịch sử xem từ cửa sổ Xem chi tiết'),
    G['l_dong'],
]

# ------------------------------------------------------------------ VIII. XEM CHI TIẾT KHO KẾ TOÁN
S_XEM = [
    o('S1', '006', func='Mở cửa sổ Xem bằng cách bấm Mã kho kế toán'),
    o('S4', '015', func='Cửa sổ Xem chi tiết kho Nhập xuất thẳng'),
    G['v_khop'], G['v_chi_doc'], G['v_khoa'], G['v_dong'],
]

# ------------------------------------------------------------------ IX. TÙY CHỈNH CỘT
S_COT = [G['c_mo'], G['c_hien'], G['c_an'], G['c_bat_buoc'], G['c_keo'], G['c_co_dinh'], G['c_dong'], G['c_nho'],
         G['c_tk'], G['c_du_lieu']]

# ------------------------------------------------------------------ X. XUẤT DANH SÁCH EXCEL
S_XUAT = [
    o('S7', '001', func='Mở cửa sổ chọn trường xuất file'),
    G['x_md'],
    o('S7', '002', func='Xuất theo bộ lọc, lấy tất cả các trang'),
    G['x_mot_so'],
    o('S7', '005', func='Không chọn trường nào thì không xuất được; chọn tất cả và đổi thứ tự'),
    G['x_tim'],
    o('S7', '003', func='Xuất theo phạm vi công ty'),
    G['x_rong'],
    o('S7', '004', func='Ô trống trong file để trống'),
    G['x_ten_cot'], G['x_dinh_dang'],
]

# ------------------------------------------------------------------ XI. IMPORT TỪ FILE EXCEL
S_IMP = [
    o('S8', '001'), o('S8', '002', func='Tải lên file đúng mẫu, Load lên bảng xem trước'),
    G['i_sai_dinh_dang'], G['i_thieu_cot'], G['i_sai_ten_cot'], G['i_rong'], G['i_dong_trong'],
    o('S8', '007', func='File vượt quá 500 dòng'),
    o('S8', '003', func='Kiểm tra dữ liệu - báo lỗi từng dòng: trống, sai định dạng, trùng hệ thống, trùng trong file'),
    o('S8', '004', func='Kiểm tra dữ liệu - kế toán đã nghỉ việc, kho vật lý đang khóa'),
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
    o('S11', '001', func='Vòng đời kho kế toán từ lúc tạo tới lúc xóa'),
    o('S11', '002', func='Kho phát sinh tồn rồi xuất hết - các nút đổi đúng'),
    K('Khóa kho vật lý không làm mất liên kết của kho kế toán đang gắn', 'P0',
      'KKT-TEST-01 đang gắn kho vật lý KVL-TEST-A.',
      ['Khóa KVL-TEST-A ở màn Phân hệ Kho => Danh mục => Kho vật lý', 'Quay lại màn Kho kế toán, tải lại trang',
       'Đọc cột Kho vật lý của KKT-TEST-01, mở cửa sổ Xem', 'Mở khóa lại KVL-TEST-A'], '',
      ['Cột Kho vật lý vẫn hiện tên KVL-TEST-A, không bị trống',
       'Cửa sổ Xem hiện "Mã - Tên" của KVL-TEST-A kèm biểu tượng khóa',
       'Trạng thái KKT-TEST-01 KHÔNG tự đổi (vẫn Hoạt động)']),
    K('Đổi tên kho vật lý thì cột Kho vật lý hiện tên mới', 'P1', 'KKT-TEST-01 đang gắn kho vật lý KVL-TEST-A.',
      ['Sửa KVL-TEST-A ở màn Kho vật lý, đổi Tên kho thành "Kho vật lý A mới"', 'Quay lại màn Kho kế toán, tải lại trang'],
      'Tên kho vật lý: Kho vật lý A mới',
      ['Cột Kho vật lý của KKT-TEST-01 hiện "Kho vật lý A mới"', 'Kho kế toán vẫn gắn đúng KVL-TEST-A']),
    K('Kho kế toán mới tạo có ngay ở ô chọn của màn Khai Quy chế – Cấu hình', 'P1',
      'Vừa tạo mới KKT-TEST-30 (Hoạt động) cho Công ty A.',
      ['Mở ' + QC + ' của Công ty A', 'Mở ô "Kho khuyến mại", rồi ô "Kho hàng gửi", tìm KKT-TEST-30'], '',
      ['Cả 2 ô chọn đều có KKT-TEST-30', 'Không cần tải lại trang']),
]

# ------------------------------------------------------------------ XIII. PHÂN QUYỀN
S_QUYEN = [
    o('ROLE', '00'), o('ROLE', '01'), o('ROLE', '02', func='Quyền phải gán vào vai trò theo công ty mới có menu'),
    G['q_mot_quyen'],
    o('ROLE', '03', func='Phạm vi dữ liệu: người thường chỉ thấy kho kế toán của công ty mình'),
    o('ROLE', '04', func='Phạm vi dữ liệu: Super admin thấy mọi công ty, có ô lọc Công ty'),
    o('ROLE', '06', func='Phạm vi dữ liệu: tài khoản không xác định được công ty thì không thấy kho nào'),
    o('ROLE', '05'),
    o('S11', '003', func='Super admin quản lý kho kế toán của công ty khác'),
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
    ('XEM CHI TIẾT KHO KẾ TOÁN', S_XEM),
    ('TÙY CHỈNH CỘT', S_COT),
    ('XUẤT DANH SÁCH EXCEL', S_XUAT),
    ('IMPORT TỪ FILE EXCEL', S_IMP),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S_RB),
    ('PHÂN QUYỀN', S_QUYEN),
]

if __name__ == '__main__':
    CH.build(C, GROUPS, DESC)
    print('So nhom:', len(GROUPS), '| so case cu (v1): %d' % len(OLD))
