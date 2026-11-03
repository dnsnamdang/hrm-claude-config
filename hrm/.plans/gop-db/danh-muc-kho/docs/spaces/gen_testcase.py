# -*- coding: utf-8 -*-
"""Testcase màn "Danh mục khoang" — viết lại theo KHUÔN CHUẨN tab "13. DM quốc gia" (user chốt 03/11/2026).

Khuôn + thứ tự nhóm + câu chữ: ../../../xuat-tai-lieu-chuyen-doi/TC_CHUAN.md (loại danh_muc), sinh bằng `build_chuan`
của `_tc_chuan.py` (tự chạy check_tc.py, phải 0 lỗi).
  - GIỮ toàn bộ case nghiệp vụ của bản 02/11 (gen_testcase_v1.py, đọc thẳng từ file đó bằng `cu(<section cũ>, <stt>)`),
    xếp lại vào đúng nhóm chuẩn; bỏ nhóm kiểu cũ (TC-ROLE, TẠO / SỬA / XEM, RÀNG BUỘC NHẬP LIỆU, E2E FLOW);
  - BỔ SUNG case cho các dòng checklist "Mẫu tài liệu.xlsx" (tab Testcase) mà bản cũ thiếu — hàm ở KHỐI CHUNG
    (giống hệt ở 4 màn Dãy / Khoang / Vị trí / Kiện, khác nhau ở tham số C) hoặc viết riêng cho màn bằng `moi(...)`;
  - mã case đánh lại TC_<nhóm>.<stt>; mọi chỗ tham chiếu "như TC_xx.yyy" của bản cũ tự đổi sang mã mới.
Chạy: python gen_testcase.py  (ghi đè "testcase - Danh mục khoang.xlsx", sheet "Trang tính1")
"""
import importlib.util
import os
import re
import sys
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'xuat-tai-lieu-chuyen-doi'))
from _tc_chuan import build_chuan  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ====================================================================================================
# KHỐI CHUNG — case chuẩn theo checklist "Mẫu tài liệu.xlsx" (giống nhau ở 4 màn Dãy / Khoang / Vị trí / Kiện,
# chỉ khác tham số màn ở biến C bên dưới). Mỗi hàm trả 1 case (chức năng, P, tiền điều kiện, bước, test data, expected);
# chú thích [n] = số dòng checklist mà case phủ.
# ====================================================================================================
def B(*steps):
    """Bước thực hiện: tự đánh số 1., 2., …"""
    return '\n'.join('%d. %s' % (i, s) for i, s in enumerate(steps, 1))


def E(*lines):
    """Expected: mỗi ý 1 dòng bắt đầu bằng "-  " (giống tab Quốc gia)."""
    return '\n'.join('-  ' + s for s in lines)


def ds(xs):
    return ', '.join(xs)


# ---------------------------------------------------------------- I. HIỂN THỊ TRANG & TRUY CẬP
def ht_chua_co_du_lieu(C):  # [8]
    return ('Danh sách khi chưa có %s nào' % C.dt, 'P2', C.pre_rong,
            B(C.menu, 'Quan sát bảng, dòng tổng dưới bảng và hàng nút'), '',
            E('Bảng hiện dòng "Không có dữ liệu phù hợp."',
              'Dòng dưới bảng hiện "Không có %s nào."' % C.dt,
              'Màn hình không báo lỗi; các nút Tạo mới, Import Excel, Xuất Excel vẫn hiện và dùng được'))


def ht_so_dong_mac_dinh(C):  # [10]
    return ('Số dòng mặc định mỗi trang', 'P1', 'Danh sách có hơn 10 %s.' % C.dt,
            B(C.menu, 'Đếm số dòng trên bảng, đọc ô "Số dòng/trang" ở góc dưới bên phải bảng',
              'Mở ô "Số dòng/trang"'), '',
            E('Mặc định hiện 10 dòng, dòng tổng "Hiển thị 1–10 / N"',
              'Ô "Số dòng/trang" cho chọn 5 / 10 / 20 / 50 / 100'))


def ht_trang_truoc_sau(C):  # [12]
    return ('Nút sang trang kế tiếp và lùi về trang trước', 'P0',
            'Danh sách có ít nhất 3 trang dữ liệu. Đang ở trang 1.',
            B('Bấm nút › (trang kế tiếp)', 'Đọc thanh phân trang và dòng tổng', 'Bấm nút ‹ (trang trước)', 'Đọc lại'),
            '',
            E('Bước 1: chuyển sang trang 2, số trang 2 được tô đậm, dòng tổng hiện "Hiển thị 11–20 / N"',
              'Bước 3: quay lại trang 1, dòng tổng hiện "Hiển thị 1–10 / N"',
              'Dữ liệu từng trang không lặp, không thiếu dòng'))


def ht_trang_dau_cuoi(C):  # [13]
    return ('Nút về trang cuối và về trang đầu', 'P0', 'Danh sách có N %s, nhiều hơn 3 trang. Đang ở trang 1.' % C.dt,
            B('Bấm nút » (về trang cuối)', 'Đọc thanh phân trang, dòng tổng và STT dòng cuối', 'Bấm nút « (về trang đầu)',
              'Đọc lại'),
            'N = tổng số %s trong danh sách' % C.dt,
            E('Bước 1: nhảy tới trang cuối, dòng tổng hiện "Hiển thị …–N / N", STT dòng cuối bằng N',
              'Bước 3: quay về trang 1, dòng tổng hiện "Hiển thị 1–10 / N"'))


def ht_nut_trang_bien(C):  # [14]
    return ('Nút phân trang ở trang đầu và trang cuối', 'P1', 'Danh sách có nhiều hơn 1 trang.',
            B('Đứng ở trang 1, quan sát hai nút « và ‹', 'Bấm » để về trang cuối, quan sát hai nút › và »'), '',
            E('Ở trang 1: nút « và ‹ bị mờ, bấm không có tác dụng',
              'Ở trang cuối: nút › và » bị mờ, bấm không có tác dụng'))


def ht_stt_lien_tuc(C):  # [15]
    return ('Số thứ tự liên tục qua các trang', 'P0', 'Danh sách có nhiều hơn một trang dữ liệu.',
            B('Ghi lại STT dòng cuối trang 1', 'Sang trang 2, đọc STT dòng đầu', 'Đổi "Số dòng/trang" sang 5, sang trang 3'),
            '',
            E('Bước 2: STT nối tiếp liền mạch (10 → 11), không quay về 1',
              'Bước 3: STT dòng đầu trang 3 là 11'))


def ht_tong_so(C):  # [16]
    return ('Tổng số bản ghi khi mở danh sách', 'P0',
            'Trong phạm vi được xem có N %s (gồm cả Hoạt động và Khóa). Chưa lọc gì.' % C.dt,
            B(C.menu, 'Đọc dòng tổng ở góc dưới bên trái bảng'), 'N = tổng số %s trong phạm vi được xem' % C.dt,
            E('Dòng tổng hiện "Hiển thị 1–10 / N" (10 là số dòng mặc định mỗi trang)',
              'N bằng đúng tổng số %s, tính cả %s đã Khóa; số ghi liền, không có dấu phân cách khi dưới 1,000' % (C.dt, C.dt)))


def ht_doi_so_dong_ve_trang_1(C):  # [11][18]
    return ('Đổi số dòng mỗi trang khi đang ở trang giữa', 'P1', 'Danh sách có hơn 30 %s. Đang đứng ở trang 3.' % C.dt,
            B('Đổi ô "Số dòng/trang" sang 20', 'Đếm số dòng trên bảng, đọc dòng tổng'), 'Số dòng/trang: 20',
            E('Bảng quay về trang 1 và hiện đúng 20 dòng', 'Dòng tổng hiện "Hiển thị 1–20 / N", tổng N không đổi'))


def ht_sx_khong_ho_tro(C):  # [22][23]
    return ('Các cột không cho sắp xếp', 'P2', 'Đang ở %s, chưa bấm sắp xếp cột nào.' % C.man,
            B('Di chuột và bấm vào tiêu đề các cột: ' + ds(C.nosort_cols), 'Quan sát thứ tự dòng'), '',
            E('Các cột này KHÔNG có biểu tượng mũi tên sắp xếp',
              'Bấm vào tiêu đề không làm thay đổi thứ tự dòng',
              'Chỉ các cột %s là sắp xếp được' % ds(C.sort_cols)))


def ht_sx_giu_khi_chuyen_trang(C):  # [24]
    return ('Sắp xếp giữ nguyên khi chuyển trang', 'P1',
            'Danh sách có nhiều hơn 1 trang. Đang sắp xếp giảm dần theo cột %s.' % C.sort_cols[0],
            B('Bấm sang trang 2', 'So dòng đầu trang 2 với dòng cuối trang 1', 'Quan sát biểu tượng mũi tên ở tiêu đề cột'),
            '',
            E('Thứ tự nối tiếp liền mạch, không đảo lộn hay lặp %s' % C.dt,
              'Cột %s vẫn giữ biểu tượng mũi tên xuống (giảm dần)' % C.sort_cols[0]))


def ht_sx_ve_trang_1(C):  # [25]
    return ('Bấm sắp xếp khi đang ở trang giữa thì quay về trang 1', 'P1',
            'Danh sách có nhiều hơn 3 trang. Đang đứng ở trang 3.',
            B('Bấm tiêu đề cột %s' % C.sort_cols[0], 'Quan sát thanh phân trang và dòng tổng'), '',
            E('Bảng quay về trang 1, hiện các %s đầu tiên theo %s tăng dần' % (C.dt, C.sort_cols[0]),
              'Dòng tổng hiện "Hiển thị 1–10 / N", tổng N không đổi'))


def ht_sx_tang_giam(C, cot):  # [20][21]
    return ('Sắp xếp theo cột %s' % cot, 'P1', 'Danh sách có ít nhất 5 %s có %s khác nhau.' % (C.dt, cot),
            B('Bấm tiêu đề cột %s' % cot, 'Đọc 5 dòng đầu', 'Bấm tiêu đề cột %s lần thứ hai' % cot, 'Đọc lại 5 dòng đầu'),
            '',
            E('Lần 1: các dòng xếp tăng dần theo %s, biểu tượng mũi tên lên ở tiêu đề cột' % cot,
              'Lần 2: thứ tự đảo ngược (giảm dần), biểu tượng mũi tên xuống'))


# ---------------------------------------------------------------- II. TÌM KIẾM & LỌC DANH SÁCH
def tk_chinh_xac(C):  # [26]
    return ('Tìm nhanh theo đúng %s' % C.tk_truong, 'P0', 'Có %s %s.' % (C.dt, C.tk_vd),
            B('Gõ đúng nguyên văn %s "%s" vào ô tìm nhanh' % (C.tk_truong, C.tk_vd), 'Nhấn Enter'), C.tk_vd,
            E('Bảng chỉ còn %s có %s đúng "%s" (và %s khác có chứa chuỗi này nếu có)' % (C.dt, C.tk_truong, C.tk_vd, C.dt),
              'Dòng tổng đổi theo kết quả'))


def tk_mot_phan(C):  # [27]
    return ('Tìm nhanh theo một phần từ khóa', 'P0', 'Có nhiều %s có %s chứa "%s".' % (C.dt, C.tk_truong, C.tk_mot_phan),
            B('Gõ "%s" vào ô tìm nhanh' % C.tk_mot_phan, 'Bấm nút Tìm kiếm'), 'Từ khóa: ' + C.tk_mot_phan,
            E('Hiện mọi %s có %s CHỨA "%s" (đứng đầu, giữa hay cuối đều ra)' % (C.dt, C.tk_truong, C.tk_mot_phan),
              'Không có dòng nào không chứa từ khóa'))


def tk_hoa_thuong(C):  # [28]
    return ('Tìm nhanh không phân biệt chữ hoa chữ thường', 'P1', 'Có %s %s.' % (C.dt, C.tk_vd),
            B('Gõ "%s" (toàn chữ thường), nhấn Enter, ghi nhận kết quả' % C.tk_vd.lower(),
              'Xóa, gõ lại "%s" (toàn chữ hoa), nhấn Enter' % C.tk_vd.upper(), 'So sánh hai kết quả'), '',
            E('Hai lần tìm cho ra CÙNG một tập kết quả, đều có %s %s' % (C.dt, C.tk_vd)))


def tk_co_dau(C):  # [29]
    return ('Tìm nhanh có dấu và không dấu', 'P2', 'Có %s tên "%s".' % (C.dt, C.tk_co_dau),
            B('Gõ "%s" (có dấu), nhấn Enter' % C.tk_co_dau, 'Gõ "%s" (bỏ dấu), nhấn Enter' % C.tk_khong_dau), '',
            E('Bước 1: ra %s "%s"' % (C.dt, C.tk_co_dau),
              'Bước 2: vẫn ra %s "%s" (tìm không phân biệt dấu)' % (C.dt, C.tk_co_dau)))


def tk_khong_ton_tai(C):  # [30][40]
    return ('Tìm từ khóa không tồn tại', 'P1', 'Danh sách có dữ liệu bình thường.',
            B('Gõ vào ô tìm nhanh một chuỗi chắc chắn không tồn tại', 'Nhấn Enter'), 'Từ khóa: zzzkhongtontai999',
            E('Bảng hiện "Không có dữ liệu phù hợp."', 'Dòng dưới bảng hiện "Không có %s nào."' % C.dt,
              'Không báo lỗi hệ thống'))


def tk_khoang_trang(C):  # [32]
    return ('Từ khóa có khoảng trắng đầu và cuối', 'P2', 'Có %s %s.' % (C.dt, C.tk_vd),
            B('Gõ "   %s   " (thừa khoảng trắng 2 đầu) vào ô tìm nhanh' % C.tk_vd, 'Nhấn Enter'), '',
            E('Kết quả giống hệt khi gõ "%s" không có khoảng trắng' % C.tk_vd, 'Không báo "Không có dữ liệu phù hợp."'))


def tk_gioi_han(C):  # [33]
    return ('Giới hạn độ dài ô tìm kiếm', 'P2', 'Đang ở %s.' % C.man,
            B('Dán chuỗi Test data vào ô tìm nhanh', 'Kiểm tra chuỗi trong ô có bị cắt bớt không', 'Nhấn Enter',
              'Bấm Làm mới'),
            'Chuỗi 500 ký tự (vd chữ "abcde" lặp lại 100 lần)',
            E('Bước 2: ô nhận đủ 500 ký tự, không báo lỗi',
              'Bước 3: bảng hiện "Không có dữ liệu phù hợp."; màn hình không treo, không báo lỗi hệ thống',
              'Bước 4: ô tìm nhanh trống, bảng về toàn bộ danh sách'))


def tk_xoa_tu_khoa(C):  # [34]
    return ('Xóa từ khóa thì danh sách quay về đầy đủ', 'P0', 'Đang tìm với từ khóa cho ra ít kết quả.',
            B('Xóa hết nội dung ô tìm nhanh', 'Nhấn Enter'), '',
            E('Danh sách hiện lại đầy đủ, dòng tổng quay lại như ban đầu', 'Bảng về trang 1'))


def loc_mac_dinh(C):  # [36]
    return ('Giá trị mặc định của bộ lọc khi vào màn', 'P0', 'Có %s Hoạt động và %s đã Khóa.' % (C.dt, C.dt),
            B(C.menu, 'Bấm "Tìm kiếm nâng cao", đọc từng ô lọc'), '',
            E('Ô tìm nhanh trống; các ô %s đều để trống' % ds(C.loc),
              'Danh sách hiện CẢ %s Hoạt động lẫn %s đã Khóa (không lọc trạng thái mặc định)' % (C.dt, C.dt)))


def loc_ket_hop_tim(C):  # [39]
    return ('Kết hợp tìm nhanh với bộ lọc', 'P1', 'Có M %s chứa "%s", trong đó K %s đang Khóa.' % (C.dt, C.tk_mot_phan, C.dt),
            B('Gõ "%s" vào ô tìm nhanh, nhấn Enter, đọc dòng tổng' % C.tk_mot_phan, 'Chọn thêm Trạng thái = Khóa',
              'Đọc lại dòng tổng'),
            'Từ khóa: %s; Trạng thái: Khóa' % C.tk_mot_phan,
            E('Bước 1: dòng tổng "… / M"', 'Bước 3: dòng tổng "… / K", chỉ còn %s vừa chứa từ khóa vừa đang Khóa' % C.dt,
              'Số dòng trên bảng khớp con số dòng tổng'))


def loc_tong_so(C):  # [41]
    return ('Tổng số bản ghi sau khi lọc', 'P0', 'Có K %s đang Khóa trong phạm vi được xem.' % C.dt,
            B('Lọc Trạng thái = Khóa', 'Đọc dòng tổng', 'Bấm Làm mới, đọc lại dòng tổng'), 'Trạng thái: Khóa',
            E('Bước 2: dòng tổng "Hiển thị 1–… / K", K đúng bằng số %s đang Khóa' % C.dt,
              'Bước 3: dòng tổng quay lại tổng ban đầu'))


def loc_ve_trang_1(C):  # [17][42]
    return ('Áp dụng bộ lọc khi đang ở trang giữa', 'P0', 'Đang ở trang 3. Bộ lọc mới cho ra hơn 10 kết quả.',
            B('Chọn một giá trị ở ô lọc (vd Trạng thái = Hoạt động)', 'Quan sát bảng, thanh phân trang', 'Bấm sang trang 2'),
            '',
            E('Bước 2: bảng quay về trang 1, dòng tổng "Hiển thị 1–10 / <số kết quả lọc>"',
              'Bước 3: trang 2 vẫn chỉ gồm %s thỏa bộ lọc, STT tiếp từ 11' % C.dt))


def loc_sap_xep(C):  # [43]
    return ('Sắp xếp sau khi lọc', 'P2', 'Đang lọc Trạng thái = Hoạt động, kết quả hơn 1 trang.',
            B('Bấm tiêu đề cột %s' % C.sort_cols[0], 'Đọc các dòng, đọc ô Trạng thái của bộ lọc'), '',
            E('Kết quả lọc được xếp tăng dần theo %s' % C.sort_cols[0],
              'Bộ lọc giữ nguyên, không lẫn %s đã Khóa vào kết quả' % C.dt))


def luu_chuyen_man(C):  # [45]
    return ('Rời sang màn khác rồi quay lại thì bộ lọc trở về mặc định', 'P1', 'Đang ở %s.' % C.man,
            B('Gõ từ khóa vào ô tìm nhanh và chọn Trạng thái = Hoạt động', 'Ghi nhận dòng tổng',
              'Vào màn khác trên menu (vd %s)' % C.man_khac, 'Khoảng 1 phút sau, quay lại bằng menu',
              'Quan sát khối bộ lọc và bảng'),
            'Từ khóa: %s; Trạng thái: Hoạt động' % C.tk_mot_phan,
            E('Ô tìm nhanh trống, các ô lọc trở về rỗng',
              'Bảng hiện toàn bộ danh sách ở trang 1, dòng tổng bằng tổng số ban đầu'))


def luu_f5(C):  # [46]
    return ('Tải lại trang (F5) khi đang lọc', 'P2', 'Đang ở %s.' % C.man,
            B('Gõ từ khóa vào ô tìm nhanh và chọn Trạng thái = Hoạt động', 'Nhấn F5 tải lại trang',
              'Quan sát khối bộ lọc và bảng'),
            'Từ khóa: %s; Trạng thái: Hoạt động' % C.tk_mot_phan,
            E('Ô tìm nhanh và các ô lọc trở về rỗng', 'Bảng hiện toàn bộ danh sách ở trang 1 với số dòng mặc định 10'))


def luu_tab_moi(C):  # [47]
    return ('Mở màn hình ở tab trình duyệt mới khi tab cũ đang lọc', 'P2', 'Tab 1 đang mở %s.' % C.man,
            B('Ở tab 1: gõ từ khóa và chọn Trạng thái = Hoạt động',
              'Mở tab trình duyệt mới (đã đăng nhập), vào %s bằng menu' % C.man, 'Quan sát tab 2',
              'Quay lại tab 1, quan sát'),
            'Từ khóa: %s; Trạng thái: Hoạt động' % C.tk_mot_phan,
            E('Tab 2: ô tìm nhanh và các ô lọc rỗng, bảng hiện toàn bộ danh sách ở trang 1',
              'Tab 1: vẫn giữ nguyên từ khóa, giá trị lọc và kết quả đang xem'))


def luu_tk_khac(C):  # [48]
    return ('Đăng xuất, đăng nhập tài khoản khác trên cùng trình duyệt', 'P1',
            'Có 2 tài khoản A và B cùng có quyền "Quản lý kho", dùng chung một trình duyệt.',
            B('Đăng nhập tài khoản A, vào %s' % C.man, 'Gõ từ khóa và chọn Trạng thái = Hoạt động', 'Đăng xuất',
              'Đăng nhập tài khoản B, vào %s' % C.man, 'Quan sát khối bộ lọc và bảng'),
            'Từ khóa: %s; Trạng thái: Hoạt động' % C.tk_mot_phan,
            E('Tài khoản B thấy ô tìm nhanh và các ô lọc rỗng, bảng hiện toàn bộ danh sách ở trang 1',
              'Từ khóa và giá trị lọc của tài khoản A KHÔNG hiện sang tài khoản B'))


# ---------------------------------------------------------------- III. THÊM MỚI
def tm_bat_buoc(C):  # [52]
    return ('Trường bắt buộc và không bắt buộc', 'P1', 'Đang mở cửa sổ "%s".' % C.tao_title,
            B('Đọc nhãn từng ô trong cửa sổ'), '',
            E('Có dấu * đỏ ở: ' + ds(C.bb),
              'Không có dấu * ở: ' + ds(C.tuy_chon)))


def tm_chi_bat_buoc(C):  # [56][57]
    return ('Thêm mới chỉ nhập trường bắt buộc', 'P0', 'Đang mở cửa sổ "%s".' % C.tao_title,
            B('Nhập đủ các ô bắt buộc theo Test data, để trống %s' % ds(C.tuy_chon_trong), 'Bấm "Lưu"'),
            C.tao_data,
            E('Hiện "Thêm mới thành công.", cửa sổ đóng', 'Danh sách có %s mới ở dòng đầu, Trạng thái "Hoạt động"' % C.dt,
              'Ô %s của dòng mới để TRỐNG (không in dấu gạch)' % ds(C.tuy_chon_trong)))


def tm_du_lieu_sau_luu(C):  # [58]
    return ('Dữ liệu sau khi lưu khớp với dữ liệu đã nhập', 'P0', 'Vừa tạo %s theo Test data.' % C.dt,
            B('Đọc dòng %s vừa tạo trên bảng' % C.dt, 'Bấm %s để mở cửa sổ "%s"' % (C.link_xem, C.xem_title)), C.tao_data,
            E('Mọi ô trên bảng và trong cửa sổ Xem khớp đúng giá trị đã nhập',
              'Người tạo là tài khoản đang đăng nhập, Ngày tạo là thời điểm lưu (dd/mm/yyyy hh:mm)'))


def tm_lich_su(C):  # [60]
    return ('Ghi nhận lịch sử Tạo mới sau khi thêm thành công', 'P1', 'Vừa tạo %s theo Test data.' % C.dt,
            B('Ở dòng %s vừa tạo, mở "Lịch sử"' % C.dt, 'Đọc dòng trên cùng'), C.tao_data,
            E('Có dòng loại hành động "Tạo mới" kèm người tạo và thời gian tạo'))


def tm_dung_max(C):  # [65]
    return ('Nhập đúng độ dài tối đa thì lưu được', 'P1', 'Đang mở cửa sổ "%s".' % C.tao_title,
            B('Nhập các ô bắt buộc hợp lệ, riêng các ô theo Test data dài đúng giới hạn', 'Bấm "Lưu"'), C.max_data,
            E('Không báo lỗi dưới các ô', 'Lưu thành công, giá trị hiện đủ, không bị cắt bớt'))


def tm_chi_khoang_trang(C):  # [69]
    return ('Nhập toàn khoảng trắng vào ô bắt buộc', 'P1', 'Đang mở cửa sổ "%s", các ô khác đã nhập hợp lệ.' % C.tao_title,
            B('Gõ toàn dấu cách vào ô %s' % C.f_chu, 'Bấm "Lưu"'), '%s: "     "' % C.f_chu,
            E('Dưới ô %s báo "Bắt buộc phải nhập"' % C.f_chu, 'Không tạo %s, cửa sổ vẫn mở' % C.dt))


def tm_loi_bien_mat(C):  # [71]
    return ('Thông báo lỗi biến mất khi nhập lại hợp lệ', 'P1', 'Đang mở cửa sổ "%s".' % C.tao_title,
            B('Để trống mọi ô, bấm "Lưu"', 'Nhập giá trị hợp lệ vào ô %s' % C.f_chu, 'Quan sát dưới ô vừa nhập'), '',
            E('Bước 1: dưới các ô bắt buộc báo "Bắt buộc phải nhập"',
              'Bước 3: lỗi dưới ô %s biến mất, các ô còn trống vẫn giữ lỗi' % C.f_chu))


def tm_ltt_thieu(C):  # [73]
    return ('Lưu & Tiếp tục khi bỏ trống trường bắt buộc', 'P0', 'Đang mở cửa sổ "%s".' % C.tao_title,
            B('Để trống ô %s, nhập các ô khác hợp lệ' % C.f_chu, 'Bấm "Lưu & Tiếp tục"'), '',
            E('Dưới ô %s báo "Bắt buộc phải nhập"' % C.f_chu,
              'Cửa sổ vẫn mở, tiêu đề vẫn "%s"; giá trị đã nhập giữ nguyên, không bị xóa trắng' % C.tao_title,
              'Không hiện "Thêm mới thành công.", danh sách phía sau không có %s mới' % C.dt))


def tm_ltt_sai_dinh_dang(C):  # [74]
    return ('Lưu & Tiếp tục khi nhập sai định dạng', 'P1', 'Đang mở cửa sổ "%s".' % C.tao_title,
            B('Nhập các ô hợp lệ, riêng %s nhập theo Test data' % C.f_dd, 'Bấm "Lưu & Tiếp tục"',
              'Sửa lại đúng định dạng, bấm "Lưu & Tiếp tục"'),
            '%s: %s' % (C.f_dd, C.dd_sai),
            E('Bước 2: dưới ô %s báo "%s", không lưu, cửa sổ vẫn mở, giá trị giữ nguyên' % (C.f_dd, C.dd_msg),
              'Bước 3: lưu thành công, cửa sổ xóa trắng để nhập tiếp'))


def tm_ltt_trung(C):  # [75]
    return ('Lưu & Tiếp tục khi trùng dữ liệu', 'P0', C.pre_trung,
            B('Nhập %s trùng %s đã có (%s)' % (C.f_trung, C.dt, C.pham_vi_trung), 'Bấm "Lưu & Tiếp tục"',
              'Sửa thành giá trị chưa có, bấm lại "Lưu & Tiếp tục"'), '',
            E('Bước 2: dưới ô %s báo "%s", không lưu, cửa sổ vẫn mở, các ô giữ nguyên' % (C.f_trung, C.trung_msg),
              'Bước 3: lưu thành công, cửa sổ xóa trắng để nhập tiếp'))


def tm_ltt_dong(C):  # [78]
    return ('Bấm Lưu & Tiếp tục rồi bấm Đóng ngay thì không hỏi', 'P1',
            'Đang mở cửa sổ "%s", đã nhập đủ trường bắt buộc.' % C.tao_title,
            B('Bấm "Lưu & Tiếp tục"', 'Không nhập gì thêm vào cửa sổ trống', 'Bấm "Đóng"'), C.tao_data,
            E('%s vừa lưu có trong danh sách' % C.Dt,
              'Bấm Đóng thì cửa sổ đóng ngay, KHÔNG hiện hộp "Thông tin chưa lưu"'))


def tm_dong_chua_nhap(C):  # [93]
    return ('Bấm Đóng khi chưa nhập thông tin nào', 'P0', 'Đang mở cửa sổ "%s", chưa nhập gì.' % C.tao_title,
            B('Bấm "Đóng"', 'Xem danh sách'), '',
            E('Cửa sổ đóng ngay, không hỏi', 'KHÔNG có %s mới nào được tạo' % C.dt))


def tm_dong_x(C):  # [95]
    return ('Đã nhập thông tin rồi bấm nút X góc trên cửa sổ', 'P1',
            'Đang mở cửa sổ "%s", đã nhập %s.' % (C.tao_title, C.f_chu),
            B('Bấm nút X ở góc trên bên phải cửa sổ', 'Bấm "Ở lại"', 'Bấm X lần nữa, bấm "Thoát"'), '',
            E('Bước 1: hiện hộp "Thông tin chưa lưu" với câu "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", '
              'nút Thoát, Ở lại',
              'Bước 2: quay về cửa sổ Tạo mới, dữ liệu đã nhập vẫn còn',
              'Bước 3: cửa sổ đóng, không tạo %s' % C.dt))


def tm_nhap_xoa_het(C):  # [98]
    return ('Nhập rồi xóa hết về như ban đầu, bấm Đóng thì không hỏi', 'P2',
            'Đang mở cửa sổ "%s", các ô đang trống.' % C.tao_title,
            B('Gõ vài ký tự vào ô %s' % C.f_chu, 'Xóa hết các ký tự vừa gõ', 'Bấm "Đóng"'), '',
            E('Cửa sổ đóng ngay, KHÔNG hiện hộp "Thông tin chưa lưu"', 'Không có %s mới nào được tạo' % C.dt))


def tm_khong_thao_tac(C):  # [100]
    return ('Nhập đủ dữ liệu rồi để nguyên cửa sổ, không bấm Lưu', 'P2',
            'Đang mở cửa sổ "%s", đã nhập đủ dữ liệu hợp lệ.' % C.tao_title,
            B('Không bấm nút nào, để nguyên khoảng 15 phút', 'Bấm "Lưu"'), C.tao_data,
            E('Trong lúc chờ: cửa sổ giữ nguyên, KHÔNG tự tạo %s' % C.dt,
              'Bước 2: lưu bình thường, hiện "Thêm mới thành công." (hoặc yêu cầu đăng nhập lại nếu phiên đã hết hạn, '
              'không mất dữ liệu đã có)'))


def tm_spam_luu(C):  # [101]
    return ('Bấm Lưu liên tục hai lần', 'P0', 'Đang mở cửa sổ "%s", đã nhập đủ dữ liệu hợp lệ.' % C.tao_title,
            B('Bấm "Lưu"', 'Bấm "Lưu" lần hai thật nhanh', 'Xem danh sách'), C.tao_data,
            E('Chỉ tạo ra ĐÚNG MỘT %s, không tạo hai bản trùng' % C.dt, 'Chỉ hiện một thông báo "Thêm mới thành công."'))


def tm_trung_2_tab(C):  # [102]
    return ('Tạo trùng cùng lúc ở hai tab', 'P1', 'Mở %s ở 2 tab, cả hai đang mở cửa sổ "%s".' % (C.man, C.tao_title),
            B('Ở cả hai tab nhập cùng dữ liệu theo Test data', 'Tab 1 bấm "Lưu"', 'Tab 2 bấm "Lưu"'), C.tao_data,
            E('Tab 1: "Thêm mới thành công."',
              'Tab 2: dưới ô %s báo "%s", không tạo thêm bản ghi' % (C.f_trung, C.trung_msg),
              'Danh sách chỉ có MỘT %s theo dữ liệu này' % C.dt))


# ---------------------------------------------------------------- IV. CHỈNH SỬA
def cs_nut(C):  # [106]
    return ('Các nút trong cửa sổ Sửa', 'P1', 'Có %s đang Hoạt động.' % C.dt,
            B('Bấm "Sửa" ở dòng %s đó' % C.dt, 'Quan sát tiêu đề và chân cửa sổ'), '',
            E('Tiêu đề "%s"' % C.sua_title, 'Chân cửa sổ chỉ có 2 nút "Lưu" và "Đóng", KHÔNG có "Lưu & Tiếp tục"'))


def cs_sua_1(C):  # [107][110]
    return ('Sửa một trường và lưu thành công', 'P0', '%s A đang có %s "%s".' % (C.Dt, C.f_sua, C.sua_cu),
            B('Mở cửa sổ Sửa %s A' % C.dt, 'Đổi %s thành "%s"' % (C.f_sua, C.sua_moi), 'Bấm "Lưu"', 'Xem bảng'),
            '%s: %s' % (C.f_sua, C.sua_moi),
            E('Hiện "Cập nhật thành công.", cửa sổ đóng', 'Cột %s trên bảng đổi thành "%s"' % (C.f_sua_cot, C.sua_moi_hien),
              'Các cột khác giữ nguyên'))


def cs_sua_nhieu(C):  # [108]
    return ('Sửa nhiều trường cùng lúc', 'P0', '%s A đang Hoạt động.' % C.Dt,
            B('Mở cửa sổ Sửa %s A' % C.dt, 'Đổi đồng thời: ' + ds(C.sua_nhieu), 'Bấm "Lưu"',
              'Mở lại cửa sổ Xem của %s A' % C.dt), '',
            E('Hiện "Cập nhật thành công."', 'Mọi trường vừa đổi đều được lưu đúng, hiện đúng trên bảng và cửa sổ Xem'))


def cs_giu_nguyen(C):  # [109]
    return ('Giữ nguyên %s của chính mình khi sửa' % C.f_trung, 'P0', '%s A đang có %s X.' % (C.Dt, C.f_trung),
            B('Mở cửa sổ Sửa %s A' % C.dt, 'KHÔNG đổi %s, chỉ đổi %s' % (C.f_trung, C.f_phu), 'Bấm "Lưu"'), '',
            E('LƯU ĐƯỢC, không báo trùng với chính mình', 'Hiện "Cập nhật thành công."'))


def cs_ngay_nguoi(C):  # [111]
    return ('Người cập nhật và Ngày cập nhật đổi sau khi sửa', 'P1',
            '%s A do tài khoản khác tạo. Đăng nhập tài khoản B.' % C.Dt,
            B('Mở cửa sổ Sửa %s A, đổi %s, bấm "Lưu"' % (C.dt, C.f_phu), 'Đọc cột Người cập nhật, Ngày cập nhật, Người tạo, '
              'Ngày tạo của %s A' % C.dt), '',
            E('Người cập nhật = tài khoản B, Ngày cập nhật = thời điểm vừa lưu',
              'Người tạo, Ngày tạo giữ nguyên như trước khi sửa'))


def cs_lich_su(C):  # [112]
    return ('Sửa xong ghi vào lịch sử', 'P0', 'Vừa đổi %s của %s A từ "%s" thành "%s".' % (C.f_sua, C.dt, C.sua_cu, C.sua_moi),
            B('Mở Lịch sử của %s A' % C.dt, 'Đọc dòng trên cùng'), '',
            E('Có dòng "Thay đổi thông tin", nêu %s: %s → %s' % (C.f_sua, C.sua_cu, C.sua_moi),
              'Kèm người thực hiện và thời điểm'))


def cs_trong(C):  # [113]
    return ('Để trống %s khi sửa' % C.f_chu, 'P0', 'Đang mở cửa sổ Sửa %s A.' % C.dt,
            B('Xóa hết nội dung ô %s' % C.f_chu, 'Bấm "Lưu"'), '',
            E('Dưới ô %s báo "Bắt buộc phải nhập"' % C.f_chu, 'Không lưu, cửa sổ vẫn mở, %s A giữ nguyên dữ liệu cũ' % C.dt))


def cs_sai_dinh_dang(C):  # [114][118]
    return ('Nhập sai định dạng %s khi sửa' % C.f_dd, 'P0', 'Đang mở cửa sổ Sửa %s A.' % C.dt,
            B('Đổi %s theo Test data' % C.f_dd, 'Quan sát dưới ô', 'Sửa lại đúng định dạng'), '%s: %s' % (C.f_dd, C.dd_sai),
            E('Bước 2: dưới ô %s báo "%s", bấm Lưu không lưu' % (C.f_dd, C.dd_msg),
              'Bước 3: lỗi biến mất ngay, bấm Lưu thành công'))


def cs_vuot(C):  # [115]
    return ('Nhập vượt độ dài tối đa khi sửa', 'P1', 'Đang mở cửa sổ Sửa %s A.' % C.dt,
            B('Dán vào ô %s chuỗi dài hơn giới hạn' % C.f_dai, 'Đếm số ký tự còn lại trong ô'), C.dai_data,
            E(*C.dai_exp))


def cs_trung_khac(C):  # [116]
    return ('Sửa trùng %s với %s khác' % (C.f_trung, C.dt), 'P0', C.pre_trung,
            B('Mở cửa sổ Sửa %s A' % C.dt, 'Đổi %s thành đúng %s của %s B (%s)' % (C.f_trung, C.f_trung, C.dt, C.pham_vi_trung),
              'Bấm "Lưu"'), '',
            E('Dưới ô %s báo "%s"' % (C.f_trung, C.trung_msg), 'Không lưu, cửa sổ vẫn mở'))


def cs_mo_khong_doi(C):  # [119]
    return ('Mở Sửa, không thay đổi gì rồi bấm Đóng', 'P1', 'Có %s đang Hoạt động.' % C.dt,
            B('Bấm "Sửa" ở dòng %s đó' % C.dt, 'Không thay đổi ô nào', 'Bấm "Đóng"'), '',
            E('Cửa sổ đóng ngay, KHÔNG hiện hộp "Thông tin chưa lưu"', 'Dữ liệu trên bảng không đổi'))


def cs_doi_tra_ve(C):  # [120]
    return ('Sửa rồi trả lại đúng giá trị cũ, bấm Đóng thì không hỏi', 'P2', '%s A có %s "%s".' % (C.Dt, C.f_sua, C.sua_cu),
            B('Mở cửa sổ Sửa %s A' % C.dt, 'Đổi %s thành "%s"' % (C.f_sua, C.sua_moi), 'Sửa lại đúng "%s"' % C.sua_cu,
              'Bấm "Đóng"'), '',
            E('Cửa sổ đóng ngay, KHÔNG hiện hộp "Thông tin chưa lưu" vì dữ liệu không khác ban đầu'))


def cs_dong_da_doi(C):  # [121][124]
    return ('Bấm Đóng hoặc X khi đã thay đổi thông tin', 'P0', 'Đang mở cửa sổ Sửa %s A.' % C.dt,
            B('Đổi %s' % C.f_sua, 'Bấm "Đóng"'), '',
            E('Hiện hộp "Thông tin chưa lưu" với câu "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", nút Thoát, Ở lại'))


def cs_thoat(C):  # [122][124]
    return ('Bấm Thoát ở hộp "Thông tin chưa lưu" khi đang sửa', 'P1', 'Đang mở cửa sổ Sửa %s A, đã đổi %s.' % (C.dt, C.f_sua),
            B('Bấm "Đóng"', 'Bấm "Thoát"', 'Xem dòng %s A trên bảng' % C.dt), '',
            E('Cửa sổ đóng, quay lại danh sách', '%s của %s A KHÔNG đổi, không ghi lịch sử' % (C.f_sua, C.dt)))


def cs_o_lai(C):  # [123]
    return ('Bấm Ở lại ở hộp "Thông tin chưa lưu" khi đang sửa', 'P1', 'Đang mở cửa sổ Sửa %s A, đã đổi %s.' % (C.dt, C.f_sua),
            B('Bấm "Đóng"', 'Bấm "Ở lại"'), '',
            E('Hộp xác nhận đóng, quay lại cửa sổ Sửa', 'Giá trị vừa đổi vẫn còn để lưu tiếp'))


def cs_khong_lich_su(C):  # [125]
    return ('Bấm Lưu nhưng không đổi gì thì không ghi lịch sử', 'P1', '%s B đang Hoạt động.' % C.Dt,
            B('Mở cửa sổ Sửa %s B' % C.dt, 'Không thay đổi gì', 'Bấm "Lưu"', 'Mở Lịch sử của %s B' % C.dt), '',
            E('Lịch sử KHÔNG có dòng "Thay đổi thông tin" mới'))


def cs_bi_xoa(C):  # [127]
    return ('Sửa %s đã bị người khác xóa' % C.dt, 'P1',
            'Tab 1 đang mở danh sách có %s A (chưa được dùng). Tab 2 cùng tài khoản.' % C.dt,
            B('Tab 2: xóa %s A' % C.dt, 'Tab 1 (chưa tải lại): bấm "Sửa" %s A, hoặc đang mở sẵn cửa sổ Sửa thì bấm "Lưu"' % C.dt),
            '',
            E('Hiện thông báo lỗi, không tạo lại %s A' % C.dt, 'Tải lại danh sách thì %s A không còn' % C.dt))


def cs_2_nguoi(C):  # [128]
    return ('Hai người cùng sửa một %s' % C.dt, 'P2', 'Tài khoản A và B cùng mở cửa sổ Sửa %s X.' % C.dt,
            B('A đổi %s thành "%s", bấm "Lưu"' % (C.f_sua, C.sua_moi), 'B đổi %s, bấm "Lưu"' % C.f_phu,
              'Mở lại cửa sổ Xem và Lịch sử của %s X' % C.dt), '',
            E('Cả hai lần lưu đều báo "Cập nhật thành công."',
              'Dữ liệu cuối cùng là giá trị của lần lưu sau; Lịch sử có đủ 2 dòng "Thay đổi thông tin" của A và B'))


# ---------------------------------------------------------------- V. XÓA
def xoa_popup(C):  # [130][131][132]
    return ('Hộp xác nhận xóa nêu đúng tên', 'P0', '%s A Hoạt động, %s.' % (C.Dt, C.dk_xoa),
            B('Bấm "Xóa" ở dòng %s A' % C.dt, 'Đọc hộp xác nhận'), '',
            E('Hộp tiêu đề "Xác nhận xóa", câu "Bạn có chắc muốn xóa %s \'<%s>\'?"' % (C.dt, C.ten_xn),
              'Hai nút "Hủy" và "Xóa"'))


def xoa_huy(C):  # [134]
    return ('Bấm Hủy thì không xóa', 'P0', 'Đang mở hộp "Xác nhận xóa" của %s A.' % C.dt,
            B('Bấm "Hủy"', 'Xem danh sách'), '',
            E('Hộp đóng, %s A vẫn còn trên danh sách, dòng tổng không đổi' % C.dt))


def xoa_tong_so(C):  # [139][140]
    return ('Sau khi xóa: mất khỏi danh sách và tổng số giảm', 'P0', 'Danh sách có N %s, %s A %s.' % (C.dt, C.dt, C.dk_xoa),
            B('Xóa %s A, bấm "Xóa" ở hộp xác nhận' % C.dt, 'Đọc dòng tổng', 'Tìm nhanh theo %s A' % C.tk_truong), '',
            E('Thông báo "Xóa thành công."', 'Dòng tổng còn N - 1', 'Tìm lại không thấy %s A' % C.dt))


# ---------------------------------------------------------------- VI. KHÓA / MỞ KHÓA
def khoa_popup(C):  # [142][143]
    return ('Hộp xác nhận khóa nêu đúng tên', 'P0', '%s A Hoạt động, %s.' % (C.Dt, C.dk_khoa),
            B('Ở dòng %s A, mở nút ba chấm "Hành động khác" (nếu có), bấm "Khóa"' % C.dt, 'Đọc hộp xác nhận'), '',
            E('Hộp tiêu đề "Xác nhận khóa", câu "Bạn có chắc muốn khóa %s \'<%s>\'?"' % (C.dt, C.ten_xn),
              'Hai nút "Hủy" và "Khóa"'))


def khoa_sau(C):  # [148][149]
    return ('Trạng thái và các nút sau khi Khóa', 'P0', '%s A Hoạt động, %s.' % (C.Dt, C.dk_khoa),
            B('Khóa %s A, bấm "Khóa" ở hộp xác nhận' % C.dt, 'Đọc cột Trạng thái và cột Hành động'), '',
            E('Thông báo "Khóa thành công."', 'Trạng thái đổi sang nhãn "Khóa"',
              'Cột Hành động chỉ còn "Mở khóa" và "Lịch sử"; nút Sửa, Xóa biến mất'))


def mo_khoa_popup_huy(C):  # [151][153]
    return ('Bấm Hủy ở hộp xác nhận mở khóa', 'P1', '%s A đang Khóa, %s.' % (C.Dt, C.dk_mo_khoa),
            B('Bấm "Mở khóa" ở dòng %s A' % C.dt, 'Đọc hộp xác nhận', 'Bấm "Hủy"'), '',
            E('Hộp tiêu đề "Xác nhận mở khóa", câu "Bạn có chắc muốn mở khóa %s \'<%s>\'?", nút "Hủy" và "Mở khóa"'
              % (C.dt, C.ten_xn),
              'Bấm Hủy: hộp đóng, %s A vẫn Khóa, không ghi lịch sử' % C.dt))


def mo_khoa_sau(C):  # [152][154][155]
    return ('Trạng thái và các nút sau khi Mở khóa', 'P0', '%s A đang Khóa, %s.' % (C.Dt, C.dk_mo_khoa),
            B('Bấm "Mở khóa" ở dòng %s A, bấm "Mở khóa" ở hộp xác nhận' % C.dt, 'Đọc cột Trạng thái và cột Hành động'), '',
            E('Thông báo "Mở khóa thành công."', 'Trạng thái đổi về nhãn "Hoạt động"',
              'Nút Sửa hiện lại; Xóa, Khóa hiện theo điều kiện như %s đang hoạt động bình thường' % C.dt))


def mo_khoa_nguoi_khac(C):  # [158]
    return ('Mở khóa %s đã bị người khác mở khóa' % C.dt, 'P1', 'Tab 1 và tab 2 cùng mở danh sách, %s A đang Khóa.' % C.dt,
            B('Tab 2: mở khóa %s A' % C.dt, 'Tab 1 (chưa tải lại): bấm "Mở khóa" %s A, xác nhận' % C.dt), '',
            E('Tab 1 không ghi thêm lần mở khóa thứ hai (báo lỗi hoặc báo thành công nhưng lịch sử chỉ có 1 dòng mở khóa)',
              'Tải lại: %s A đang Hoạt động' % C.dt))


def khoa_bi_xoa(C):  # [159]
    return ('Khóa / mở khóa %s đã bị người khác xóa' % C.dt, 'P1', 'Tab 1 đang mở danh sách có %s A (chưa được dùng).' % C.dt,
            B('Tab 2: xóa %s A' % C.dt, 'Tab 1 (chưa tải lại): bấm "Khóa" %s A, xác nhận' % C.dt), '',
            E('Hiện thông báo lỗi, không có %s nào bị khóa' % C.dt, 'Tải lại thì %s A không còn trong danh sách' % C.dt))


# ---------------------------------------------------------------- VII. LỊCH SỬ THAY ĐỔI
def ls_mo(C):  # [162][163]
    return ('Mở cửa sổ Lịch sử', 'P0', '%s A đã được tạo và sửa ít nhất 1 lần.' % C.Dt,
            B('Ở dòng %s A, mở nút ba chấm "Hành động khác" (nếu có), bấm "Lịch sử"' % C.dt, 'Quan sát cửa sổ'), '',
            E('Cửa sổ tiêu đề "Lịch sử thay đổi: <%s A>"' % C.ten_xn,
              'Có nút "Bộ lọc"; danh sách các lần thao tác, mỗi lần một khối'))


def ls_noi_dung(C):  # [165][166][167][168]
    return ('Mỗi dòng lịch sử nêu đủ thông tin', 'P0', '%s A có lần "Thay đổi thông tin" đổi %s.' % (C.Dt, C.f_sua),
            B('Mở Lịch sử của %s A' % C.dt, 'Đọc khối "Thay đổi thông tin"'), '',
            E('Có người thực hiện (tên nhân viên), thời gian dd/mm/yyyy hh:mm, loại hành động',
              'Nội dung ghi "%s: <giá trị cũ> → <giá trị mới>", giá trị cũ và mới khác màu' % C.f_sua))


def ls_moi_nhat(C):  # [164]
    return ('Thứ tự mới nhất ở trên cùng', 'P0', '%s A lần lượt được Tạo mới, Sửa, Khóa.' % C.Dt,
            B('Mở Lịch sử của %s A' % C.dt, 'Đọc thứ tự các khối'), '',
            E('Khối trên cùng là "Thay đổi trạng thái" (Khóa), dưới là "Thay đổi thông tin", cuối cùng là "Tạo mới"'))


def ls_loc_hanh_dong(C):  # [169]
    return ('Lọc theo Loại hành động', 'P0', 'Lịch sử %s A có đủ Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.' % C.dt,
            B('Mở Lịch sử %s A, bấm "Bộ lọc"' % C.dt, 'Mở ô "Loại hành động"', 'Chọn "Thay đổi thông tin"'), '',
            E('Ô có các lựa chọn: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái',
              'Sau khi chọn: chỉ còn các khối "Thay đổi thông tin"'))


def ls_loc_nguoi(C):  # [170]
    return ('Lọc theo Người thực hiện', 'P0', 'Lịch sử %s A có thao tác của 2 người A và B.' % C.dt,
            B('Mở Lịch sử %s A, bấm "Bộ lọc"' % C.dt, 'Ô "Người thực hiện" chọn B'), '',
            E('Ô chỉ liệt kê những người đã thao tác trên %s A' % C.dt, 'Chỉ còn các khối do B thực hiện'))


def ls_loc_thoi_gian(C):  # [171]
    return ('Lọc theo khoảng thời gian', 'P0', 'Lịch sử %s A có thao tác ở nhiều ngày khác nhau.' % C.dt,
            B('Mở Lịch sử %s A, bấm "Bộ lọc"' % C.dt, 'Chọn "Từ ngày", "Đến ngày" bao một ngày có thao tác'), '',
            E('Chỉ còn các khối có thời gian nằm trong khoảng đã chọn, tính cả 2 đầu mút'))


def ls_loc_ket_hop(C):  # [172][173]
    return ('Lọc kết hợp và lọc không có kết quả', 'P1', 'Lịch sử %s A có nhiều loại hành động của nhiều người.' % C.dt,
            B('Chọn Loại hành động = Thay đổi trạng thái và Người thực hiện = một người chưa từng khóa / mở khóa %s A' % C.dt,
              'Đổi Người thực hiện thành người đã khóa %s A' % C.dt), '',
            E('Bước 1: hiện "Không có lịch sử phù hợp bộ lọc."',
              'Bước 2: chỉ còn các khối Thay đổi trạng thái của người đó'))


def ls_lam_moi(C):  # [174]
    return ('Nút Làm mới trong bộ lọc lịch sử', 'P1', 'Đang lọc lịch sử theo Loại hành động và Người thực hiện.',
            B('Bấm "Làm mới" trong vùng bộ lọc'), '',
            E('Các ô lọc về trống', 'Hiện lại toàn bộ lịch sử của %s' % C.dt))


def ls_dong_mo_loc(C):  # [175]
    return ('Đóng / mở vùng bộ lọc lịch sử', 'P2', 'Đang mở cửa sổ Lịch sử.',
            B('Bấm "Bộ lọc"', 'Bấm "Bộ lọc" lần nữa'), '',
            E('Bước 1: hiện các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày và nút Làm mới',
              'Bước 2: vùng bộ lọc thu gọn lại, danh sách lịch sử không đổi'))


def ls_sua_nhieu(C):  # [178][183]
    return ('Lịch sử khi sửa nhiều trường cùng lúc', 'P0', '%s A đang Hoạt động.' % C.Dt,
            B('Mở Sửa %s A, đổi đồng thời: %s, bấm "Lưu"' % (C.dt, ds(C.sua_nhieu)), 'Mở Lịch sử %s A' % C.dt), '',
            E('Có MỘT khối "Thay đổi thông tin" mới, liệt kê đủ từng trường đã đổi kèm giá trị cũ → mới',
              'Trường không đổi không xuất hiện'))


def ls_dong(C):  # [184][185]
    return ('Đóng cửa sổ Lịch sử giữ nguyên danh sách', 'P2', 'Đang lọc danh sách và đứng ở trang 2.',
            B('Mở Lịch sử của một %s ở trang 2' % C.dt, 'Bấm nút X góc trên (hoặc nút Đóng)'), '',
            E('Cửa sổ đóng', 'Danh sách vẫn ở trang 2, bộ lọc giữ nguyên'))


# ---------------------------------------------------------------- VIII. XEM CHI TIẾT
def xem_chi_doc(C):  # [187][188][191][192]
    return ('Cửa sổ Xem chỉ đọc, không có nút Lưu', 'P0', 'Có %s đang Hoạt động.' % C.dt,
            B('Bấm %s ở dòng %s đó' % (C.link_xem, C.dt), 'Thử gõ vào từng ô', 'Quan sát chân cửa sổ'), '',
            E('Tiêu đề "%s"; có đủ các ô: %s' % (C.xem_title, ds(C.xem_truong)),
              'Mọi ô đều không sửa được, không có dấu * bắt buộc', 'Chân cửa sổ chỉ có nút "Đóng"'))


def xem_khop(C):  # [189][190]
    return ('Dữ liệu trong cửa sổ Xem khớp với dòng trên bảng', 'P0', 'Vừa tạo %s theo Test data.' % C.dt,
            B('Bấm %s của %s vừa tạo' % (C.link_xem, C.dt), 'So từng ô với dữ liệu đã nhập và với dòng trên bảng'),
            C.tao_data, E('Mọi ô khớp với dữ liệu đã nhập và khớp với dòng trên bảng'))


def xem_khoa(C):  # [193][194]
    return ('Xem chi tiết %s đang Khóa' % C.dt, 'P1', 'Có %s đang Khóa.' % C.dt,
            B('Bấm %s ở dòng %s đã Khóa' % (C.link_xem, C.dt)), '',
            E('Cửa sổ Xem mở bình thường, ô Trạng thái hiện "Khóa"', 'Khối Lịch sử bên dưới xem được'))


def xem_dong(C):  # [196][197]
    return ('Đóng cửa sổ Xem giữ nguyên bộ lọc và trang', 'P1', 'Đang lọc danh sách và đứng ở trang 2.',
            B('Bấm %s một %s ở trang 2' % (C.link_xem, C.dt), 'Bấm "Đóng"'), '',
            E('Cửa sổ đóng', 'Danh sách vẫn ở trang 2, bộ lọc giữ nguyên, không tải lại về trang 1'))


# ---------------------------------------------------------------- IX. TÙY CHỈNH CỘT
def cot_mo(C):  # [198][199][200]
    return ('Mở cửa sổ Tuỳ chỉnh cột', 'P0', 'Tài khoản chưa chỉnh cấu hình cột của %s.' % C.man,
            B('Bấm nút "Cấu hình cột hiển thị" (cạnh Xuất Excel)', 'Đọc danh sách cột'), '',
            E('Cửa sổ "Tuỳ chỉnh cột" có dòng hướng dẫn, nút "Chọn tất cả", "Bỏ chọn hết"',
              'Liệt kê đủ cột: ' + ds(C.cot_md + C.cot_an),
              'Cột đang hiện được tích sẵn; %s chưa tích' % ds(C.cot_an)))


def cot_an(C):  # [202]
    return ('Tắt một cột tùy chọn', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
            B('Bỏ tích cột "Người cập nhật"', 'Bấm "Lưu"'), '',
            E('Bảng không còn cột Người cập nhật', 'Các cột khác giữ nguyên thứ tự'))


def cot_keo_tha(C):  # [204][205]
    return ('Kéo thả đổi thứ tự cột', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
            B('Kéo cột "Trạng thái" lên ngay sau cột "%s"' % C.cot_md[2], 'Thử kéo cột "STT"', 'Bấm "Lưu"'), '',
            E('Bước 2: cột STT không kéo được (cột cố định)',
              'Sau khi lưu: bảng hiện cột Trạng thái ngay sau cột %s' % C.cot_md[2]))


def cot_dong_khong_luu(C):  # [207]
    return ('Đóng cửa sổ mà không lưu thì không áp dụng thay đổi', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
            B('Bỏ tích vài cột, kéo đổi vài vị trí', 'Bấm "Đóng" (không bấm Lưu)', 'Mở lại cửa sổ'), '',
            E('Bảng giữ nguyên các cột như trước', 'Mở lại cửa sổ: tích và thứ tự như trước khi chỉnh'))


def cot_theo_tai_khoan(C):  # [209]
    return ('Cấu hình cột lưu riêng theo từng tài khoản', 'P2', 'Tài khoản A đã ẩn cột Người tạo ở %s.' % C.man,
            B('Đăng xuất, đăng nhập tài khoản B', 'Vào %s' % C.man, 'Đăng nhập lại tài khoản A trên máy khác'), '',
            E('Tài khoản B thấy bộ cột mặc định (có cột Người tạo)',
              'Tài khoản A trên máy khác vẫn thấy cột Người tạo bị ẩn (cấu hình lưu theo tài khoản)'))


def cot_khong_anh_huong(C):  # [210][211]
    return ('Cấu hình cột không ảnh hưởng dữ liệu và bộ lọc', 'P1', 'Đang lọc Trạng thái = Hoạt động, đứng ở trang 2.',
            B('Mở Tuỳ chỉnh cột, ẩn cột Ngày tạo, bấm "Lưu"', 'Quan sát bảng, bộ lọc, dòng tổng'), '',
            E('Bộ lọc và dòng tổng không đổi, số dòng không đổi', 'Chỉ mất cột Ngày tạo trên bảng'))


# ---------------------------------------------------------------- X. XUẤT DANH SÁCH EXCEL
def xuat_tat_ca_truong(C):  # [216][225][226]
    return ('Xuất file với tất cả trường', 'P0', 'Danh sách có dữ liệu.',
            B('Bấm "Xuất Excel"', 'Bấm "Chọn tất cả"', 'Bấm "Xuất file"', 'Mở file'), '',
            E('Thông báo "Xuất Excel thành công", tải file %s' % C.file_xuat,
              'File có đủ cột theo đúng thứ tự trong cửa sổ: ' + ds(C.truong_xuat)))


def xuat_bo_truong(C):  # [217][227]
    return ('Bỏ tích một trường thì file không có cột đó', 'P0', 'Đang mở cửa sổ "Chọn trường xuất file".',
            B('Bỏ tích trường "Người cập nhật"', 'Bấm "Xuất file"', 'Mở file'), '',
            E('File không có cột Người cập nhật', 'Dòng cuối cửa sổ trước khi xuất hiện "Đang chọn … trường" giảm 1'))


def xuat_khong_chon(C):  # [218]
    return ('Không chọn trường nào', 'P1', 'Đang mở cửa sổ "Chọn trường xuất file".',
            B('Bấm "Bỏ chọn hết"', 'Bấm "Xuất file"'), '',
            E('Dòng chân cửa sổ hiện "Đang chọn 0/%d trường"' % len(C.truong_xuat),
              'Nút "Xuất file" bị mờ, bấm không có tác dụng, không tải file'))


def xuat_theo_tim(C):  # [219]
    return ('Xuất theo từ khóa tìm nhanh', 'P1', 'Có M %s chứa "%s".' % (C.dt, C.tk_mot_phan),
            B('Gõ "%s" vào ô tìm nhanh, nhấn Enter' % C.tk_mot_phan, 'Xuất Excel', 'Đếm số dòng trong file'), '',
            E('File có đúng M dòng, đều là %s chứa từ khóa' % C.dt))


def xuat_rong(C):  # [222]
    return ('Xuất khi danh sách không có dòng nào', 'P2', 'Đang tìm từ khóa không tồn tại, bảng rỗng.',
            B('Bấm "Xuất Excel", bấm "Xuất file"', 'Mở file (nếu tải được)'), '',
            E('Không báo lỗi hệ thống', 'File (nếu tải) chỉ có tiêu đề và dòng tên cột, không có dòng dữ liệu'))


def xuat_dinh_dang(C):  # [223][224][229][230]
    return ('Tên file, định dạng ngày và tiếng Việt trong file', 'P1',
            'Có %s mà %s chứa dấu tiếng Việt và ký tự đặc biệt (vd "%s").' % (C.dt, C.f_chu, C.vd_dac_biet),
            B('Xuất Excel với "Chọn tất cả"', 'Mở file bằng Excel'), '',
            E('Tên file %s, mở được bằng Excel không báo lỗi' % C.file_xuat,
              'Ngày tạo, Ngày cập nhật dạng dd/mm/yyyy hh:mm; số (nếu có) căn phải, dấu phẩy ngăn nghìn',
              'Chữ tiếng Việt có dấu và ký tự đặc biệt hiện đúng, không lỗi phông'))


# ---------------------------------------------------------------- XI. IMPORT TỪ FILE EXCEL
def imp_sai_file(C):  # [236]
    return ('Chọn file không phải Excel', 'P1', 'Đang mở cửa sổ Import.',
            B('Bấm "Chọn file Excel", chọn file .pdf hoặc .docx'), 'File: tai_lieu.pdf',
            E('Báo "Vui lòng chọn file .xlsx hoặc .xls"', 'Không nạp dữ liệu, nút Load lên bảng vẫn mờ'))


def imp_thieu_cot(C):  # [237][238]
    return ('File thiếu cột bắt buộc hoặc đổi tên / thứ tự cột', 'P1', 'File mẫu đã xóa cột "%s" (hoặc đổi tên cột này).'
            % C.imp_cot_bb,
            B('Chọn file, bấm "Load lên bảng"', 'Bấm "Validate"'), '',
            E('Cột thiếu / sai tên không được đọc: các dòng báo "%s: Bắt buộc phải nhập"' % C.imp_cot_bb,
              'Không tạo %s nào' % C.dt))


def imp_file_rong(C):  # [239][240]
    return ('File không có dòng dữ liệu hoặc có dòng trống', 'P2',
            'File 1: chỉ giữ 2 dòng đầu của file mẫu. File 2: 3 dòng dữ liệu, giữa có 1 dòng trống.',
            B('Chọn File 1, bấm "Load lên bảng"', 'Chọn File 2, bấm "Load lên bảng"'), '',
            E('File 1: báo "Không có dòng dữ liệu hợp lệ."', 'File 2: dòng trống bị bỏ qua, bảng xem trước có 2 dòng'))


def imp_vuot_do_dai(C):  # [245]
    return ('Giá trị vượt độ dài tối đa trong file', 'P1', 'File 1 dòng, ô %s dài hơn giới hạn.' % C.imp_cot_dai,
            B('Load lên bảng', 'Bấm "Validate"'), C.imp_dai_data,
            E('Dòng đó báo lỗi ở cột %s, không được import' % C.imp_cot_dai))


def imp_khoang_trang_hoa_thuong(C):  # [248][249]
    return ('Khoảng trắng và chữ hoa / thường trong file', 'P2', C.imp_ht_pre,
            B('Load lên bảng', 'Bấm "Validate"', 'Import (nếu hợp lệ)'), C.imp_ht_data,
            E(*C.imp_ht_exp))


def imp_tat_ca_hop_le(C):  # [255][259][260]
    return ('Import file tất cả dòng hợp lệ', 'P0', 'File 3 dòng đều hợp lệ, chưa tồn tại trong hệ thống.',
            B('Load lên bảng', 'Bấm "Validate"', 'Bấm "Import"'), '',
            E('Validate: "Hợp lệ: 3", "Lỗi: 0", nút Import sáng',
              'Import: thông báo "Import thành công 3 %s.", cửa sổ đóng' % C.dt,
              'Danh sách tự tải lại, có đủ 3 %s mới, dòng tổng tăng 3' % C.dt))


def imp_khong_hop_le(C):  # [257]
    return ('Không có dòng nào hợp lệ', 'P1', 'File 2 dòng đều có lỗi.',
            B('Load lên bảng', 'Bấm "Validate"', 'Bấm "Bỏ dòng lỗi"'), '',
            E('Validate: "Hợp lệ: 0", "Lỗi: 2", nút Import mờ',
              'Bỏ dòng lỗi: bảng không còn dòng nào, nút Import vẫn mờ; không tạo %s nào' % C.dt))


def imp_lich_su(C):  # [262]
    return ('Lịch sử của %s tạo bằng Import' % C.dt, 'P1', 'Vừa import thành công %s X.' % C.dt,
            B('Mở Lịch sử %s X' % C.dt), '',
            E('Có dòng "Tạo mới" của người import, thời gian bằng lúc bấm Import'))


def imp_lai_cung_file(C):  # [265]
    return ('Import lại cùng một file', 'P1', 'Vừa import thành công file F.',
            B('Mở lại cửa sổ Import, chọn lại file F', 'Load lên bảng, bấm "Validate"'), '',
            E('Mọi dòng báo trùng ("%s"), nút Import mờ' % C.imp_trung_msg, 'Không tạo thêm %s nào' % C.dt))


def imp_dong_thoi(C):  # [264][266]
    return ('Hai người import cùng dữ liệu cùng lúc', 'P2', 'Tài khoản A và B cùng có file chứa %s X (chưa tồn tại).' % C.dt,
            B('A và B cùng Load, Validate (đều hợp lệ)', 'A bấm "Import"', 'B bấm "Import"'), '',
            E('A: import thành công', 'B: dòng X bị bỏ qua vì đã tồn tại, thông báo nêu số dòng lỗi bị bỏ qua',
              'Danh sách chỉ có MỘT %s X' % C.dt))


def cot_bat_buoc(C):  # [203][205][208]
    return ('Cột bắt buộc không tắt được, cấu hình giữ sau khi tải lại', 'P0', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
            B('Thử bỏ tích các cột STT, %s, Hành động' % C.cot_md[1], 'Bỏ tích cột "Người tạo", bấm "Lưu"',
              'Nhấn F5 tải lại trang'), '',
            E('Bước 1: STT, %s có biểu tượng khóa, không bỏ tích, không kéo đổi vị trí được; Hành động không bỏ tích được '
              '(vẫn kéo đổi vị trí được)' % C.cot_md[1],
              'Bước 3: cột Người tạo vẫn ẩn, các cột khác giữ như đã lưu'))


# ---------------------------------------------------------------- PHÂN QUYỀN
def pq_thu_hoi(C):  # [298]
    return ('Bị thu hồi quyền khi đang mở màn', 'P2', 'Tài khoản có quyền "Quản lý kho" đang mở %s.' % C.man,
            B('Quản trị gỡ quyền "Quản lý kho" khỏi vai trò của tài khoản đó',
              'Tài khoản đó (chưa tải lại trang) bấm "Tạo mới", nhập đủ, bấm "Lưu"', 'Tải lại trang'), '',
            E('Bước 2: hệ thống từ chối, báo không có quyền, không tạo %s' % C.dt,
              'Bước 3: menu không còn mục "%s", mở màn bị chặn' % C.Dt))


def pq_lich_su(C):  # [294]
    return ('Lịch sử không cần quyền riêng: có "Quản lý kho" là xem được', 'P2',
            'Tài khoản có quyền "Quản lý kho" (không có quyền nào khác). Có %s A đã có lịch sử.' % C.dt,
            B(C.menu, 'Mở "Lịch sử" của %s A' % C.dt, 'Bấm %s của %s A, xem khối Lịch sử' % (C.link_xem, C.dt)), '',
            E('Mở được cửa sổ "Lịch sử thay đổi: <%s A>", hiện đủ các mốc, không báo thiếu quyền' % C.ten_xn,
              'Khối Lịch sử trong cửa sổ Xem cũng xem được'))


# ====================================================================================================
# NẠP CASE BẢN CŨ (gen_testcase_v1.py — sinh ngày 02/11, sai khuôn) để GIỮ NGUYÊN nội dung nghiệp vụ đã viết
# ====================================================================================================
_spec = importlib.util.spec_from_file_location('gen_testcase_v1', os.path.join(HERE, 'gen_testcase_v1.py'))
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)

_ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
OLD = {}      # (biến section cũ, stt) -> tuple case cũ
OLD_ID = {}   # (biến section cũ, stt) -> mã case ở bản cũ (để đổi các chỗ "như TC_xx.yyy" sang mã mới)
for _roman, _title, _tcs in V.SECTIONS:
    _var = next(k for k, v in vars(V).items() if v is _tcs and re.match(r'^S\d+$', k))
    for _t in _tcs:
        OLD[(_var, _t[0])] = _t
        OLD_ID[(_var, _t[0])] = 'TC_%02d.%03d' % (_ROMAN.index(_roman) + 1, int(_t[0]))
for _t in V.ROLE_TCS:
    OLD[('ROLE', _t[0])] = _t
    OLD_ID[('ROLE', _t[0])] = 'TC-ROLE-%s' % _t[0]


def cu(var, n, **sua):
    """Case giữ từ bản cũ; `sua` = các ô sửa lại (func / prio / pre / steps / data / exp)."""
    t = OLD[(var, n)]
    c = dict(key=(var, n), func=t[1], prio=t[2], pre=t[3], steps=t[4], data=t[5], exp=t[6])
    for k, v in sua.items():
        c[k] = v if isinstance(v, str) else '\n'.join(v)
    return c


def moi(t):
    """Case bổ sung theo checklist (hàm ở KHỐI CHUNG hoặc tuple viết riêng cho màn)."""
    func, prio, pre, steps, data, exp = t
    j = lambda x: x if isinstance(x, str) else '\n'.join(x)  # noqa: E731
    return dict(key=None, func=func, prio=prio, pre=j(pre), steps=j(steps), data=j(data), exp=j(exp))


_TIEN_TO = ('ht', 'tk', 'loc', 'luu', 'tm', 'cs', 'xoa', 'khoa', 'mo', 'ls', 'xem', 'cot', 'xuat', 'imp', 'pq')


def nap_g(C):
    """g.<hàm KHỐI CHUNG>() = case đã điền tham số màn C."""
    return SimpleNamespace(**{k: (lambda f: (lambda *a: moi(f(C, *a))))(f) for k, f in list(globals().items())
                              if callable(f) and k.split('_')[0] in _TIEN_TO})


# ====================================================================================================
# RIÊNG MÀN KHOANG
# ====================================================================================================
NGAY = '03/11/2026'
SHEET = 'Trang tính1'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % V.TEN)

# Khối mô tả giữ của bản cũ; sửa câu ghi nhớ bộ lọc cho đúng code (rời màn / F5 / tab mới đều trả bộ lọc về mặc định)
DESCRIPTION_BLOCK = [(k, v.replace('Hệ thống ghi nhớ bộ lọc trong 10 phút khi rời màn rồi quay lại.',
                                   'Rời sang màn khác, tải lại trang (F5) hay mở tab mới thì bộ lọc trở về mặc định.'))
                     for k, v in V.DESCRIPTION_BLOCK]

C = SimpleNamespace(
    dt='khoang', Dt='Khoang', menu=V.MENU, man='màn Khoang', man_khac='màn Dãy',
    pre_rong='Đăng nhập tài khoản có quyền "Quản lý kho" của một công ty chưa có khoang nào.',
    sort_cols=['Mã khoang', 'Tên khoang', 'Ngày tạo', 'Ngày cập nhật'],
    nosort_cols=['STT', 'Dãy', 'Nhà kho', 'Kho', 'Người tạo', 'Người cập nhật', 'Trạng thái', 'Hành động'],
    tk_truong='mã khoang', tk_vd='KHOANG-TEST-01', tk_mot_phan='TEST', tk_co_dau='Khoang thường',
    tk_khong_dau='khoang thuong',
    loc=['Kho', 'Nhà kho', 'Dãy', 'Trạng thái', 'Người tạo', 'Ngày tạo'],
    tao_title='Tạo mới khoang', sua_title='Sửa khoang', xem_title='Xem chi tiết khoang', link_xem='chữ ở cột Mã khoang',
    bb=['Kho', 'Nhà kho', 'Dãy', 'Mã khoang', 'Tên khoang'], tuy_chon=['Trạng thái', 'Mô tả'], tuy_chon_trong=['Mô tả'],
    tao_data='Kho: KHO-TEST-01; Nhà kho: NHA-TEST-01; Dãy: DAY-TEST-01; Mã khoang: KHOANG-TEST-20; '
             'Tên khoang: Khoang test 20',
    f_chu='Tên khoang', f_dd='Mã khoang', dd_sai='KHOANG @20', dd_msg='Chỉ gồm chữ không dấu, số, dấu - và _',
    f_trung='Mã khoang', pham_vi_trung='cùng dãy', trung_msg='Đã tồn tại trong dãy này',
    pre_trung='Dãy DAY-TEST-01 đã có khoang A (KHOANG-TEST-01) và khoang B (KHOANG-TEST-02).',
    f_sua='Tên khoang', f_sua_cot='Tên khoang', sua_cu='Khoang test 01', sua_moi='Khoang test 01 sửa',
    sua_moi_hien='Khoang test 01 sửa', sua_nhieu=['Mã khoang', 'Tên khoang', 'Mô tả'], f_phu='Mô tả',
    f_dai='Mã khoang', dai_data='Mã khoang: chuỗi 51 ký tự, sau đó 50 ký tự',
    dai_exp=['Với 51 ký tự: ô vẫn nhận đủ nhưng báo đỏ ngay dưới ô Mã khoang (tối đa 50 ký tự), bấm Lưu không lưu',
             'Với 50 ký tự: lỗi biến mất, lưu thành công'],
    ten_xn='Tên khoang',
    dk_xoa='chưa có vị trí, chưa nằm trong kế hoạch kiểm kê (xóa hết vị trí của nó ở màn Vị trí)',
    dk_khoa='không còn vị trí đang hoạt động',
    dk_mo_khoa='dãy chứa nó đang Hoạt động',
    xem_truong=['Kho', 'Nhà kho', 'Dãy', 'Mã khoang', 'Tên khoang', 'Số vị trí', 'Trạng thái', 'Mô tả'],
    cot_md=['STT', 'Mã khoang', 'Tên khoang', 'Dãy', 'Nhà kho', 'Kho', 'Người tạo', 'Ngày tạo', 'Người cập nhật',
            'Ngày cập nhật', 'Trạng thái', 'Hành động'],
    cot_an=['Số vị trí', 'Mô tả'],
    file_xuat='danh_sach_khoang.xlsx',
    truong_xuat=['Mã khoang', 'Tên khoang', 'Dãy', 'Nhà kho', 'Kho', 'Số vị trí', 'Mô tả', 'Trạng thái', 'Người tạo',
                 'Ngày tạo', 'Người cập nhật', 'Ngày cập nhật'],
    vd_dac_biet='Khoang "A&B" - tầng 1',
    imp_cot_bb='Tên khoang *', imp_cot_dai='Tên khoang', imp_dai_data='Tên khoang: chuỗi 256 ký tự',
    imp_ht_pre='File 2 dòng vào KHO-TEST-01 / NHA-TEST-01 / DAY-TEST-02: dòng 1 Mã khoang "KHOANG-IMP-10", Tên khoang '
               '"  Khoang imp 10  " (thừa khoảng trắng 2 đầu); dòng 2 Mã khoang "k1" (chữ thường của mã K1 đã có trong dãy).',
    imp_ht_data='Tên khoang: "  Khoang imp 10  "; Mã khoang: "k1"',
    imp_ht_exp=['Dòng 1: hợp lệ; sau Import, tên lưu là "Khoang imp 10" (đã cắt khoảng trắng 2 đầu)',
                'Dòng 2: báo "Mã khoang: Đã tồn tại trong dãy này" (so trùng không phân biệt hoa thường)'],
    imp_trung_msg='Mã khoang: Đã tồn tại trong dãy này',
)
g = nap_g(C)

DAY, VT, KK = V.DAY, V.VT, V.KK

NHOM = [
    ('HIỂN THỊ TRANG & TRUY CẬP', [
        cu('S1', '001'), cu('S1', '002'), cu('S1', '003'), cu('S3', '007'), cu('S3', '008'), cu('S1', '007'),
        g.ht_chua_co_du_lieu(), cu('S1', '004'),
        cu('S3', '003'), g.ht_trang_truoc_sau(), g.ht_trang_dau_cuoi(), g.ht_nut_trang_bien(),
        cu('S1', '005'), cu('S3', '001'), cu('S3', '002'), g.ht_sx_khong_ho_tro(), cu('S3', '004'), g.ht_sx_ve_trang_1(),
    ]),
    ('TÌM KIẾM & LỌC DANH SÁCH', [
        cu('S2', '009'), g.tk_mot_phan(), g.tk_co_dau(), cu('S2', '010'), g.tk_khoang_trang(), g.tk_gioi_han(),
        g.tk_xoa_tu_khoa(),
        g.loc_mac_dinh(), cu('S2', '001'), cu('S2', '002'), cu('S2', '003'), cu('S2', '004'), cu('S2', '005'),
        cu('S2', '006'), cu('S2', '013'), cu('S2', '007'), cu('S2', '008'), cu('S2', '014'), cu('S2', '011'),
        g.loc_ket_hop_tim(), g.loc_tong_so(), g.loc_ve_trang_1(), g.loc_sap_xep(), cu('S2', '012'),
        cu('S1', '006', func='Rời sang màn khác rồi quay lại thì bộ lọc trở về mặc định', prio='P1',
           exp=['- Lần 1 (quay lại sau 2 phút) và lần 2 (sau hơn 10 phút) cho cùng kết quả: bộ lọc về trống, '
                'hiện toàn bộ danh sách ở trang 1']),
        g.luu_f5(), g.luu_tab_moi(), g.luu_tk_khac(),
    ]),
    ('THÊM MỚI', [
        cu('S4', '001'), g.tm_bat_buoc(), cu('S4', '003'), cu('S4', '002'), cu('S4', '006'), g.tm_chi_bat_buoc(),
        g.tm_du_lieu_sau_luu(), g.tm_lich_su(), cu('S4', '005'),
        cu('S10', '001'), cu('S10', '002'), g.tm_loi_bien_mat(), cu('S10', '012'),
        cu('S10', '003'), cu('S10', '004'), cu('S10', '005'), cu('S10', '006'), cu('S10', '008'), cu('S10', '009'),
        cu('S10', '010'),
        cu('S4', '004'), g.tm_ltt_thieu(), g.tm_ltt_sai_dinh_dang(), g.tm_ltt_trung(), g.tm_ltt_dong(),
        g.tm_dong_chua_nhap(), cu('S4', '015'), g.tm_dong_x(), g.tm_nhap_xoa_het(), g.tm_khong_thao_tac(),
        cu('S10', '011'), cu('S11', '005'), cu('S10', '013'),
    ]),
    ('CHỈNH SỬA', [
        cu('S4', '007'), g.cs_nut(), cu('S4', '008'), g.cs_giu_nguyen(), g.cs_ngay_nguoi(), g.cs_lich_su(),
        cu('S4', '009'), cu('S4', '010'), cu('S4', '013'),
        g.cs_trong(), g.cs_sai_dinh_dang(), g.cs_vuot(), cu('S10', '007'),
        g.cs_mo_khong_doi(), g.cs_doi_tra_ve(), g.cs_dong_da_doi(), g.cs_thoat(), g.cs_o_lai(), g.cs_khong_lich_su(),
        cu('S4', '011'), cu('S4', '014'), g.cs_2_nguoi(),
    ]),
    ('XÓA', [
        g.xoa_popup(), cu('S6', '005'), cu('S6', '001'), g.xoa_tong_so(), cu('S6', '007'),
        cu('S6', '002'), cu('S6', '003'), cu('S6', '004'), cu('S6', '006'), cu('S11', '004'),
    ]),
    ('KHÓA / MỞ KHÓA', [
        g.khoa_popup(), cu('S5', '001'), g.khoa_sau(), cu('S5', '002'), cu('S5', '003'), cu('S5', '008'),
        g.mo_khoa_popup_huy(), cu('S5', '004'), g.mo_khoa_sau(), cu('S5', '005'),
        cu('S11', '001'), cu('S11', '002'), cu('S11', '003'), g.khoa_bi_xoa(),
    ]),
    ('LỊCH SỬ THAY ĐỔI', [
        g.ls_mo(), g.ls_noi_dung(), g.ls_moi_nhat(), cu('S9', '001'), cu('S9', '002'), g.ls_sua_nhieu(),
        cu('S9', '003'), cu('S9', '005'),
        g.ls_loc_hanh_dong(), g.ls_loc_nguoi(), g.ls_loc_thoi_gian(), g.ls_loc_ket_hop(), g.ls_lam_moi(),
        g.ls_dong_mo_loc(), g.ls_dong(),
    ]),
    ('XEM CHI TIẾT KHOANG', [
        cu('S4', '012'), g.xem_khop(), g.xem_khoa(), cu('S9', '004'), g.xem_dong(),
    ]),
    ('TÙY CHỈNH CỘT', [
        g.cot_mo(), cu('S3', '005'), cu('S3', '006'), g.cot_bat_buoc(), g.cot_dong_khong_luu(),
        g.cot_theo_tai_khoan(), g.cot_khong_anh_huong(),
    ]),
    ('XUẤT DANH SÁCH EXCEL', [
        cu('S7', '002'), g.xuat_tat_ca_truong(), g.xuat_bo_truong(), cu('S7', '003'), g.xuat_khong_chon(),
        cu('S7', '001'), g.xuat_theo_tim(), cu('S7', '005'), cu('S7', '004'), g.xuat_dinh_dang(), cu('S7', '006'),
    ]),
    ('IMPORT TỪ FILE EXCEL', [
        cu('S8', '001'), g.imp_sai_file(), g.imp_thieu_cot(), g.imp_file_rong(), cu('S8', '008'),
        cu('S8', '002'), cu('S8', '003'), cu('S8', '004'), cu('S8', '005'), cu('S8', '006'), g.imp_vuot_do_dai(),
        g.imp_khoang_trang_hoa_thuong(), cu('S8', '007'), g.imp_khong_hop_le(), cu('S8', '009'), g.imp_dong_thoi(),
        g.imp_lai_cung_file(),
    ]),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', [
        moi(('Khoang mới tạo có ngay ở ô chọn Khoang của màn Vị trí', 'P0',
             'Vừa tạo KHOANG-TEST-21 (Hoạt động) thuộc DAY-TEST-01.',
             B('Mở ' + VT + ', bấm Tạo mới, Loại vị trí "Thuộc khoang"',
               'Chọn Kho KHO-TEST-01, Nhà kho NHA-TEST-01, Dãy DAY-TEST-01, mở ô Khoang', 'Chọn KHOANG-TEST-21, tạo 1 vị trí'),
             'Mã khoang: KHOANG-TEST-21',
             E('Ô Khoang có KHOANG-TEST-21 ngay, không cần tải lại cả trang',
               'Vị trí tạo xong hiện đúng Khoang / Dãy / Nhà kho / Kho; cột Số vị trí (bật ở Tuỳ chỉnh cột) của '
               'KHOANG-TEST-21 thành 1'))),
        moi(('Khoang tạo bằng Import dùng được ngay ở màn Vị trí', 'P1', 'Vừa import thành công KHOANG-IMP-01 vào DAY-TEST-02.',
             B('Mở ' + VT + ', bấm Tạo mới, chọn tới ô Khoang của DAY-TEST-02'), '',
             E('Ô Khoang có KHOANG-IMP-01, chọn và lưu vị trí được'))),
        cu('S5', '007'),
        moi(('Mở khóa khoang thì chọn lại được ở màn Vị trí', 'P1', 'KHOANG-TEST-05 đang Khóa, dãy cha Hoạt động.',
             B('Mở khóa KHOANG-TEST-05', 'Mở ' + VT + ', bấm Tạo mới, chọn tới ô Khoang của dãy đó'), '',
             E('Ô Khoang có lại KHOANG-TEST-05, chọn và lưu vị trí được'))),
        moi(('Khóa khoang không làm mất liên kết của vị trí bên dưới', 'P1',
             'KHOANG-TEST-06 có 2 vị trí đã Khóa; vừa khóa KHOANG-TEST-06.',
             B('Mở ' + VT + ', tìm 2 vị trí của KHOANG-TEST-06', 'Mở Xem chi tiết một vị trí'), '',
             E('Vị trí vẫn còn, cột Khoang / Dãy / Nhà kho / Kho vẫn đúng', 'Cửa sổ Xem vị trí vẫn hiện đúng khoang'))),
        moi(('Đổi tên khoang thì màn Vị trí hiện tên mới', 'P0', 'KHOANG-TEST-03 có 2 vị trí.',
             B('Sửa Tên khoang KHOANG-TEST-03 thành "Khoang test 03 mới"', 'Mở ' + VT + ', tìm 2 vị trí của khoang này'),
             'Tên khoang: Khoang test 03 mới', E('Cột Khoang của 2 vị trí hiện "Khoang test 03 mới"',
                                                'Ô chọn Khoang ở màn Vị trí hiện tên mới'))),
        moi(('Đổi mã khoang không làm mất liên kết vị trí', 'P1', 'KHOANG-TEST-03 có 2 vị trí.',
             B('Sửa Mã khoang KHOANG-TEST-03 thành KHOANG-TEST-03B', 'Mở ' + VT + ', tìm 2 vị trí của khoang này'), '',
             E('2 vị trí vẫn thuộc khoang này (cột Khoang hiện đúng), mã vị trí KHÔNG tự đổi'))),
        moi(('Xóa khoang thì không còn ở các màn liên quan', 'P1', 'KHOANG-TEST-07 chưa có vị trí, chưa dùng ở đâu.',
             B('Xóa KHOANG-TEST-07', 'Mở ' + VT + ', mở ô Khoang (Tạo mới và bộ lọc)',
               'Mở ' + KK + ', bấm Tạo mới, mở cây vị trí'),
             '', E('KHOANG-TEST-07 không còn trong ô chọn Khoang và cây vị trí', 'Ở màn Dãy, cột Số khoang (bật ở Tuỳ chỉnh cột) của dãy cha giảm 1'))),
        moi(('Ô chọn Khoang ở màn Vị trí cập nhật theo danh mục', 'P2',
             'Vừa tạo KHOANG-TEST-22, vừa khóa KHOANG-TEST-23 (cùng DAY-TEST-01). Màn Vị trí đang mở sẵn ở tab khác.',
             B('Ở tab màn Vị trí, bấm Tạo mới, Loại vị trí "Thuộc khoang", chọn tới Dãy DAY-TEST-01, mở ô Khoang'),
             '', E('Có KHOANG-TEST-22, KHÔNG có KHOANG-TEST-23 (khoang đã khóa không chọn mới được)'))),
        cu('S5', '006'), cu('S12', '002'), cu('S12', '003'), cu('S12', '001'),
    ]),
    ('PHÂN QUYỀN', [
        cu('ROLE', '01'), cu('ROLE', '00'), cu('ROLE', '02'), g.pq_lich_su(), g.pq_thu_hoi(),
        cu('ROLE', '03'), cu('ROLE', '04'), cu('ROLE', '05'),
    ]),
]


# ====================================================================================================
# DỰNG FILE
# ====================================================================================================
def _chuan_hoa(s):
    """Bullet "- " -> "-  " như tab Quốc gia; ô chỉ có "-" -> để trống."""
    s = (s or '').strip()
    for a, b in globals().get('DOI_CHU', []):   # đổi chữ riêng của màn (vd mã dữ liệu mẫu có chữ cấm)
        s = s.replace(a, b)
    if s == '-':
        return ''
    return '\n'.join(re.sub(r'^- (?=\S)', '-  ', ln) for ln in s.split('\n'))


def main():
    new_id, sections = {}, []
    for i, (title, cases) in enumerate(NHOM, 1):
        for j, c in enumerate(cases, 1):
            if c['key']:
                assert c['key'] not in new_id, 'Case cũ dùng 2 lần: %s' % (c['key'],)
                new_id[c['key']] = 'TC_%02d.%03d' % (i, j)
    doi = {OLD_ID[k]: v for k, v in new_id.items()}

    def tham_chieu(m):
        assert m.group(0) in doi, 'Tham chiếu tới case cũ không còn: %s' % m.group(0)
        return doi[m.group(0)]

    for i, (title, cases) in enumerate(NHOM, 1):
        rows = []
        for j, c in enumerate(cases, 1):
            f = {k: re.sub(r'TC[-_](?:ROLE-\d{2}|\d{2}\.\d{3})', tham_chieu, _chuan_hoa(c[k]))
                 for k in ('func', 'pre', 'steps', 'data', 'exp')}
            rows.append(('%03d' % j, f['func'], c['prio'], f['pre'], f['steps'], f['data'], f['exp']))
        sections.append((_ROMAN[i - 1], title, rows))

    thieu = [k for k in OLD if k not in new_id]
    assert not thieu, 'Case bản cũ chưa được đưa vào nhóm nào: %s' % thieu
    so_cu = len(OLD)
    so_moi = sum(len(c) for _, c in NHOM)
    build_chuan(OUT, SHEET, V.TEN + ' - Cập nhật ngày ' + NGAY, V.MODULE, DESCRIPTION_BLOCK, sections, loai='danh_muc')
    print('Bản cũ %d case (giữ đủ %d) + bổ sung %d -> %d case, %d nhóm'
          % (so_cu, len(new_id), so_moi - len(new_id), so_moi, len(NHOM)))


if __name__ == '__main__':
    main()
