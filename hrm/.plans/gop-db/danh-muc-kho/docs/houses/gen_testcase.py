# -*- coding: utf-8 -*-
"""Testcase màn "Danh mục nhà kho" theo KHUÔN CHUẨN tab "13. DM quốc gia" (03/11/2026).

Viết lại từ gen_testcase_v1.py (bản 02/11, khuôn cũ TC-ROLE / TẠO-SỬA-XEM / RÀNG BUỘC NHẬP LIỆU / CÔ LẬP DỮ LIỆU /
E2E):
  - case nghiệp vụ riêng của màn lấy NGUYÊN VĂN từ v1 (hàm O), đưa vào đúng nhóm khuôn danh_muc;
  - case theo checklist "Mẫu tài liệu.xlsx" lấy từ ../warehouses/_tc_dm_kho_chung.py (hàm G), điền theo cấu hình C;
  - sửa theo code: bộ lọc KHÔNG được giữ khi rời màn / F5 (v1 "giữ 10 phút" bỏ); Mã có khoảng trắng bị báo đỏ
    "Chỉ gồm chữ không dấu, số, dấu - và _" (v1 ghi "cắt khoảng trắng rồi lưu" là sai); trùng mã khác hoa / thường bị
    chặn (đối chiếu không phân biệt hoa thường).
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

TEN = 'Danh mục nhà kho'
V1, OLD = CH.load_v1(os.path.join(HERE, 'gen_testcase_v1.py'))
MENU = 'Phân hệ Kho => Danh mục => Nhà kho'
DAY = 'Phân hệ Kho => Danh mục => Dãy'

C = dict(
    out=os.path.join(HERE, 'testcase - %s.xlsx' % TEN), ten=TEN, ngay='03/11/2026',
    menu=MENU, menu_item='Nhà kho', title='Danh sách nhà kho', obj='nhà kho', label='nhà kho',
    ma='Mã nhà kho', tenf='Tên nhà kho',
    A=('NHA-TEST-01', 'Nhà test 01'), B=('NHA-TEST-02', 'Nhà test 02'), K=('NHA-TEST-03', 'Nhà test 03'),
    new=('NHA-TEST-40', 'Nhà test 40'), new2=('NHA-TEST-41', 'Nhà test 41'), new3=('NHA-TEST-42', 'Nhà test 42'),
    new4=('NHA-TEST-43', 'Nhà test 43'), imp=('NHA-IMP-01', 'Nhà import 01'),
    mot_phan='test 0', tu_khoa_chung='NHA-TEST', ten_dau=('Nhà Hà Nội test', 'nha ha noi test'),
    ten_dac_biet='Nhà A, khu: Đông', ma_sai='Nha.Test 42',
    man_khac='Dãy', man_dung=(DAY, 'Nhà kho'),
    form_min=['Kho: KHO-TEST-01 - Kho test 01', 'Số dãy: 1', 'Mã nhà kho: NHA-TEST-41', 'Tên nhà kho: Nhà test 41'],
    form_hai_tab=['Kho: KHO-TEST-01 - Kho test 01', 'Số dãy: 1', 'Mã nhà kho: NHA-TEST-43',
                  'Tên nhà kho: Nhà test 43'],
    title_tao='Tạo mới nhà kho', title_xem='Xem chi tiết nhà kho',
    dup='Đã tồn tại trong kho này', trung_ghi_chu='Kho = KHO-TEST-01', trung_pham_vi='thuộc KHO-TEST-01',
    sort_cols=['Mã nhà kho', 'Tên nhà kho', 'Ngày tạo', 'Ngày cập nhật'],
    nosort_cols=['STT', 'Kho', 'Số dãy', 'Người tạo', 'Người cập nhật', 'Trạng thái', 'Hành động'],
    locked_cols=['STT', 'Mã nhà kho', 'Hành động'], n_cols=12, cols_an=['Số dãy', 'Mô tả'],
    cot_tat='Người cập nhật',
    K_lich_su='NHA-TEST-05', K_lich_su_ten='Nhà test 05', dk_khoa='dãy D1 của nó đã bị khóa',
    K_xoa='NHA-TEST-08', K_xoa_dk='chưa có dãy',
    export_file='danh_sach_nha_kho.xlsx',
    export_fields=['Mã nhà kho', 'Tên nhà kho', 'Kho', 'Số dãy', 'Mô tả', 'Trạng thái', 'Người tạo', 'Ngày tạo',
                   'Người cập nhật', 'Ngày cập nhật'],
    import_title='Import nhà kho', import_ok='Import thành công {n} nhà kho.', import_cot_xoa='Số dãy',
    import_header_err='File không đúng mẫu: thiếu header Mã kho */Mã nhà kho */Tên nhà kho */Số dãy */Trạng thái/'
                      'Mô tả (sheet Data).',
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
    v = v.replace('Mã, tên được cắt khoảng trắng đầu / cuối trước khi kiểm tra; mã giữ nguyên chữ hoa / thường.',
                  'Tên được cắt khoảng trắng đầu / cuối; Mã có khoảng trắng bị báo đỏ (chỉ nhận chữ không dấu, số, dấu - '
                  'và _), mã giữ nguyên chữ hoa / thường khi lưu. So trùng không phân biệt chữ hoa / thường.')
    DESC.append((k, CH._bo_ma(v)))

# ------------------------------------------------------------------ I. HIỂN THỊ TRANG & TRUY CẬP
S_HIEN = [
    o('S1', '001', func='Mở màn hình từ menu', steps=['1. Đăng nhập bằng TK-A', '2. Vào menu ' + MENU,
                                                       '3. Quan sát tiêu đề, khối lọc, hàng nút']),
    o('S1', '002'),
    o('S1', '003', func='Các cột mặc định hiển thị và mặc định ẩn'),
    o('S1', '004', func='Dữ liệu từng cột đúng với dữ liệu đã tạo'),
    o('S1', '005'),
    G['h_trangthai'],
    o('S1', '006'), o('S1', '009'),
    o('S3', '008', func='Cột STT, Mã nhà kho đứng yên khi cuộn ngang; chữ dài xuống tối đa 2 dòng'),
    G['h_rong_dm'], G['h_khong_khop'],
    G['h_so_dong_md'], G['h_doi_so_dong'], G['h_truoc_sau'], G['h_dau_cuoi'], G['h_nut_mo'], G['h_stt'],
    G['h_tong'], G['h_loc_ve_1'],
    o('S3', '001', func='Thứ tự mặc định khi mở màn: nhà mới tạo đứng trước'),
    G['h_sx_ma'], G['h_sx_ten'], G['h_sx_ngay'], G['h_khong_sx'], G['h_sx_giu'], G['h_sx_ve_1'],
]

# ------------------------------------------------------------------ II. TÌM KIẾM & LỌC DANH SÁCH
S_TIM = [
    G['t_chinh_xac'],
    o('S2', '001', func='Tìm theo một phần mã, không phân biệt hoa thường'),
    o('S2', '002', func='Tìm theo tên nhà kho'),
    o('S2', '003', func='Ô tìm kiếm KHÔNG tìm theo tên người tạo'),
    G['t_dau'],
    o('S2', '005', func='Tìm với ký tự đặc biệt'),
    G['t_khoang_trang'], G['t_gioi_han'], G['t_xoa'],
    o('S2', '004', func='Ô tìm kiếm chỉ lọc khi nhấn Enter hoặc bấm Tìm kiếm'),
    G['t_md'],
    o('S2', '006'), o('S2', '007'), o('S2', '008'), o('S2', '009'), o('S2', '010'),
    o('S2', '015'), o('S2', '012'),
    o('S2', '011', func='Kết hợp tìm kiếm với nhiều ô lọc'),
    o('S2', '013', func='Nút Làm mới xóa hết tiêu chí và tải lại'),
    G['t_tong_loc'], G['t_trang_loc'], G['t_sx_loc'],
    G['t_chuyen_man'], G['t_f5'], G['t_tab'], G['t_tk_khac'],
]

# ------------------------------------------------------------------ III. THÊM MỚI
S_THEM = [
    o('S4', '001', func='Mở cửa sổ Tạo mới - đúng ô, nút và giá trị mặc định'),
    o('S4', '002'),
    o('S4', '003', func='Thêm mới đủ thông tin hợp lệ bằng nút Lưu'),
    o('S4', '004'),
    G['a_chi_bat_buoc'], G['a_lich_su'],
    o('S10', '001', func='Bỏ trống mọi ô bắt buộc thì bị chặn'),
    o('S10', '009', func='Mã nhà kho sai định dạng thì báo lỗi'),
    G['a_loi_mat'],
    o('S10', '002', func='Trùng mã với nhà khác trong cùng kho bị chặn'),
    o('S10', '003', func='Trùng tên với nhà khác trong cùng kho bị chặn'),
    o('S10', '004'), o('S10', '005'),
    o('S10', '006', func='Trùng mã khác chữ hoa / thường trong cùng kho bị chặn',
      exp='- Báo đỏ "Đã tồn tại trong kho này" dưới ô Mã nhà kho (so trùng không phân biệt hoa thường), không tạo nhà'),
    G['a_ma_khoang_trang'], G['a_chi_khoang_trang'], G['a_dung_max'],
    o('S10', '008', func='Vượt độ dài tối đa: Mã nhà kho 50, Tên nhà kho 255 ký tự'),
    o('S10', '010', func='Mô tả vượt 500 ký tự thì báo lỗi'),
    o('S10', '011', func='Số dãy bằng 0 thì báo lỗi'),
    o('S10', '012'), o('S10', '013'),
    o('S10', '017', func='Tên có dấu phẩy, hai chấm vẫn lưu được'),
    o('S10', '015', func='Kho vừa bị khóa trong lúc đang nhập cửa sổ thì bị chặn'),
    o('S4', '005', func='Lưu & Tiếp tục với dữ liệu hợp lệ giữ cửa sổ mở'),
    G['a_ltt_thieu'], G['a_ltt_sai'], G['a_ltt_trung'], G['a_ltt_dong'],
    o('S4', '007', func='Bấm Đóng khi chưa nhập thông tin nào'),
    o('S4', '006', func='Bấm Đóng khi đã nhập thông tin - chọn Ở lại / Thoát'),
    G['a_x'], G['a_xoa_het'], G['a_de_lau'],
    o('S10', '016', func='Bấm Lưu liên tục nhiều lần không sinh nhà trùng'),
    G['a_hai_tab'],
]

# ------------------------------------------------------------------ IV. CHỈNH SỬA
S_SUA = [
    o('S4', '009', func='Mở cửa sổ Sửa nhà đã có dãy - dữ liệu điền sẵn, ô bị khóa'),
    o('S4', '010', func='Sửa nhiều trường (Mã, Tên, Mô tả) thành công'),
    G['e_mot_truong'],
    o('S4', '011'), o('S4', '012'), o('S4', '015'),
    o('S10', '007', func='Giữ nguyên mã và tên của chính mình khi sửa'),
    G['e_trong'], G['e_sai'], G['e_vuot'], G['e_trung'], G['e_loi_mat'], G['e_ls'],
    G['e_khong_doi'], G['e_tra_lai'],
    K('Bấm Đóng khi đã thay đổi - chọn Ở lại / Thoát', 'P1', 'Đang mở cửa sổ Sửa NHA-TEST-02.',
      ['Đổi Mô tả, bấm Đóng', 'Bấm "Ở lại"', 'Bấm Đóng lần nữa, bấm "Thoát"', 'Mở Sửa lại NHA-TEST-02'],
      'Mô tả: Đang sửa dở',
      ['Bước 1: hiện hộp "Thông tin chưa lưu" nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", nút '
       'Thoát / Ở lại', 'Bước 2: quay lại cửa sổ, chữ vừa gõ còn nguyên',
       'Bước 3: cửa sổ đóng, danh sách không đổi', 'Bước 4: thấy dữ liệu đã lưu, không còn chữ vừa gõ']),
    G['e_khong_ls'],
    o('S4', '016', func='Nhà đang Khóa không sửa được'),
    o('S11', '006', func='Lưu Sửa khi nhà vừa bị người khác khóa'),
    o('S11', '007', func='Lưu Sửa hoặc Xem khi nhà vừa bị người khác xóa'),
    o('S11', '008'),
    G['e_dong_thoi'],
]

# ------------------------------------------------------------------ V. XÓA
S_XOA = [
    o('S6', '002', func='Xóa nhà không còn dãy'),
    o('S6', '003', func='Bấm Hủy thì không xóa'),
    o('S6', '001'), o('S6', '004'), o('S6', '005'), o('S6', '006'), o('S6', '007'),
    K('Xóa nhà đã bị người khác xóa', 'P2', '"Nhà 1" của KHO-TEST-02 chưa có dãy; TK-A và TK-H cùng mở màn danh sách.',
      ['TK-H xóa "Nhà 1"', 'TK-A (chưa tải lại trang) bấm Xóa "Nhà 1", xác nhận'], '',
      ['TK-A nhận thông báo "Dữ liệu đã thay đổi, vui lòng tải lại"', 'Không treo trang; tải lại thì "Nhà 1" không còn']),
]

# ------------------------------------------------------------------ VI. KHÓA / MỞ KHÓA
S_KHOA = [
    o('S5', '001'), o('S5', '002'), o('S5', '003'), o('S5', '006'),
    o('S4', '013'),
    o('S5', '004'), G['k_huy_mo'], o('S5', '005'),
    o('S11', '003', func='Khóa nhà đã bị người khác khóa'),
    o('S11', '004'), o('S11', '005'),
    G['k_mo_dong_thoi'], G['k_bi_xoa'],
    o('S5', '007', func='Nhà Khóa không chọn được ở màn Dãy'),
]

# ------------------------------------------------------------------ VII. LỊCH SỬ THAY ĐỔI
S_LS = [
    G['l_mo'], G['l_bo_loc'], G['l_loai'], G['l_nguoi'], G['l_tg'], G['l_ket_hop'], G['l_khong_kq'],
    G['l_lam_moi'], G['l_dong_loc'], G['l_thu_tu'],
    o('S8', '001', func='Lịch sử ngay sau khi Tạo mới'),
    G['l_mot_truong'],
    o('S8', '002', func='Lịch sử khi sửa nhiều trường ghi giá trị cũ và mới'),
    o('S8', '003'),
    G['l_import'], G['l_trang_thai_va_ten'],
    o('S8', '005'),
    o('S8', '004', func='Lịch sử xem từ cửa sổ Xem chi tiết giống cửa sổ Lịch sử'),
    G['l_dong'],
]

# ------------------------------------------------------------------ VIII. XEM CHI TIẾT NHÀ KHO
S_XEM = [
    o('S1', '007', func='Mở cửa sổ Xem bằng cách bấm Mã nhà kho'),
    o('S4', '014', func='Cửa sổ Xem chi tiết: các ô, khối Lịch sử'),
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
    o('S7', '005', func='Không chọn trường nào thì không xuất được'),
    o('S7', '003', func='Chọn thêm trường và đổi thứ tự cột trong file'),
    G['x_tim'], G['x_rong'],
    o('S7', '004', func='Dữ liệu trong file khớp danh sách'),
    G['x_ten_cot'], G['x_dinh_dang'],
]

# ------------------------------------------------------------------ XI. IMPORT TỪ FILE EXCEL
S_IMP = [
    o('S9', '001'), o('S9', '002', func='Tải lên file đúng mẫu, Load lên bảng xem trước'),
    G['i_sai_dinh_dang'], G['i_thieu_cot'], G['i_sai_ten_cot'], G['i_rong'], G['i_dong_trong'],
    o('S9', '008', func='File vượt quá 500 dòng'),
    o('S9', '003', func='Kiểm tra dữ liệu - báo lỗi từng dòng: trống, sai định dạng, trùng trong kho, trùng trong file'),
    o('S9', '004', func='Kiểm tra dữ liệu - kho đang Khóa hoặc thuộc công ty khác'),
    o('S9', '005'),
    G['i_vuot_do_dai'], G['i_khoang_trang_hoa'],
    o('S9', '007', func='Sửa dòng lỗi trên bảng rồi Validate lại; Xoá trạng thái validate'),
    G['i_tron'], G['i_khong_hop_le'],
    o('S9', '006', func='Bỏ dòng lỗi rồi Import thành công'),
    G['i_tat_ca_hop_le'],
    o('S9', '010', func='Đóng / Làm mới cửa sổ Import không ghi dữ liệu'),
    G['i_lai_file'],
    o('S9', '009', func='Nhà bị người khác tạo sau lúc Validate thì dòng đó bị bỏ qua'),
    G['i_dong_thoi'],
    K('Dữ liệu import dùng được ngay ở màn Dãy', 'P1', 'Vừa import thành công nhà kho NHA-IMP-01 thuộc KHO-TEST-01.',
      ['Mở ' + DAY, 'Bấm Tạo mới, chọn Kho = KHO-TEST-01, mở ô Nhà kho'], '',
      ['Ô Nhà kho có ngay NHA-IMP-01', 'Không cần tải lại trang mới thấy']),
]

# ------------------------------------------------------------------ XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S_RB = [
    o('S12', '001', func='Vòng đời đầy đủ một nhà kho'),
    o('S12', '002', func='Kho mới sinh nhà, nhập dãy cho nhà sinh tự động'),
    o('S12', '003'),
    K('Đổi tên nhà kho thì màn Dãy hiện tên mới, dãy vẫn đúng nhà', 'P1', 'NHA-TEST-01 có 3 dãy D1, D2, D3.',
      ['Sửa NHA-TEST-01, đổi Tên nhà kho thành "Nhà test 01 mới", Lưu', 'Mở ' + DAY + ', lọc Nhà kho = NHA-TEST-01'],
      'Tên nhà kho: Nhà test 01 mới',
      ['Cột Nhà kho của D1, D2, D3 hiện "Nhà test 01 mới"', 'Đủ 3 dãy, không dãy nào mất liên kết']),
    K('Bộ lọc Nhà kho ở các màn danh mục cấp dưới cập nhật theo danh mục', 'P2',
      'Vừa tạo mới NHA-TEST-40 (Hoạt động) và khóa NHA-TEST-03.',
      ['Lần lượt vào các màn Phân hệ Kho => Danh mục => Dãy, Khoang, Vị trí', 'Ở mỗi màn mở ô lọc Nhà kho'],
      'Nhà kho: NHA-TEST-40 (Hoạt động), NHA-TEST-03 (Khóa)',
      ['Ở cả 3 màn, ô lọc Nhà kho có NHA-TEST-40', 'Ô lọc mặc định không có NHA-TEST-03']),
]

# ------------------------------------------------------------------ XIII. PHÂN QUYỀN
S_QUYEN = [
    o('ROLE', '00'), o('ROLE', '01'), o('ROLE', '02'), G['q_mot_quyen'],
    o('ROLE', '04', func='Phạm vi dữ liệu: người thường chỉ thấy nhà công ty mình, không có ô Công ty'),
    o('ROLE', '03', func='Phạm vi dữ liệu: Super admin thấy nhà của mọi công ty và có ô lọc Công ty'),
    o('ROLE', '05', func='Phạm vi dữ liệu: tài khoản chưa gắn công ty thì không thấy nhà nào'),
    o('S11', '001', func='Phạm vi dữ liệu: người thường không thấy nhà của công ty khác'),
    o('S11', '002', func='Phạm vi dữ liệu: Super admin lọc đúng từng công ty'),
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
    ('XEM CHI TIẾT NHÀ KHO', S_XEM),
    ('TÙY CHỈNH CỘT', S_COT),
    ('XUẤT DANH SÁCH EXCEL', S_XUAT),
    ('IMPORT TỪ FILE EXCEL', S_IMP),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S_RB),
    ('PHÂN QUYỀN', S_QUYEN),
]

if __name__ == '__main__':
    CH.build(C, GROUPS, DESC)
    print('So nhom:', len(GROUPS), '| so case cu (v1): %d' % len(OLD))
