# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu nhập hàng điều chỉnh kiểm kê (form chuẩn Danh mục quốc gia, 09/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu nhap hang dieu chinh kiem ke.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (pnhdckk_shots/uml/overview.png).
Khuôn cấu trúc: ../phieu-xuat-kho-dieu-chinh-kiem-ke/gen_hdsd.py.
Ảnh + icon: pnhdckk_shots (dev-hrm 09/11/2026, _capture/capture.js, chặn mọi yêu cầu ghi — 0 yêu cầu ghi). Trạng thái thật trên dev
(PNHĐCKK-00053 Đang tạo, 00052 Đã hạch toán, PNKĐCKK-00054 Chờ duyệt) — không giả trạng thái. Icon mục menu menu_muc / menu_muc_kho
cắt từ ảnh 00_menu / 00b_menu_kho (phần tử dài bị cắt chữ khi chụp theo khung).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu nhập hàng điều chỉnh kiểm kê'
SHOTS = os.path.join(HERE, 'pnhdckk_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu nhap hang dieu chinh kiem ke.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pnhdckk')

THUAT_NGU = [
    ['Phiếu nhập hàng điều chỉnh kiểm kê', 'Chứng từ PNHĐCKK-NNNNN do Kế toán kho lập để hạch toán phần hàng thừa phát hiện khi '
                                           'kiểm kê.'],
    ['Phiếu nhập kho điều chỉnh kiểm kê', 'Chứng từ PNKĐCKK-NNNNN ở phân hệ Kho, đang Chờ duyệt; nguồn để lập phiếu này.'],
    ['Phiếu kiểm kê', 'Phiếu ở màn Kiểm kê theo hàng hóa có hàng thừa.'],
    ['Kho kế toán', 'Kho sổ sách mà từng dòng hàng được phân bổ vào; tổng Số lượng các kho kế toán phải bằng SL nhập.'],
    ['Nhân viên', 'Nhân viên chịu trách nhiệm phần hàng thừa (ghi bút toán theo nhân viên này).'],
    ['Đang tạo', 'Trạng thái (nhãn xám): phiếu đã lưu, người tạo còn sửa được.'],
    ['Đã hạch toán', 'Trạng thái (nhãn xanh lá): đã Lưu và duyệt, đã cộng tồn kho kế toán và ghi sổ, không sửa được.'],
]
PHIEN_BAN = [['1.0', '09/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, chi tiết, in, xuất Excel, xem lịch sử',
     'Xem phiếu nhập hàng điều chỉnh kiểm kê - theo tổng công ty / - theo công ty. Không có quyền nào thì chỉ thấy phiếu mình tạo.'],
    ['Tạo mới phiếu', 'Kế toán kho.'],
    ['Sửa, Lưu và duyệt phiếu Đang tạo', 'Người tạo phiếu.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.truy_cap([('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'), ('Nhập hàng', 'menu_nhaphang'),
                ('Phiếu nhập hàng điều chỉnh kiểm kê', 'menu_muc')],
               'số phiếu', bo_loc=[('Mã phiếu', 'o_maphieu'), ('Kho', 'o_kho'), ('Trạng thái', 'o_trangthai'),
                                    ('Người tạo', 'o_nguoitao'), ('Mã hàng hóa', 'o_mahang'), ('Tên hàng hóa', 'o_tenhang'),
                                    ('Ngày tạo', 'o_ngaytao'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban')])

    d.phan('THÊM MỚI PHIẾU')
    d.step('Bước 1: Truy cập vào màn hình Phiếu nhập hàng điều chỉnh kiểm kê (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.sub(['Hoặc từ phân hệ Kho ', '@menu_phanhe_kho', ', nhóm Nhập kho ', '@menu_nhom_kho', ', chọn Phiếu nhập kho điều chỉnh '
           'kiểm kê ', '@menu_muc_kho', ', ở dòng phiếu Chờ duyệt bấm ', '@btn_taophieunhaphang_row', ' (hoặc ',
           '@btn_taophieunhaphang', ' ở màn chi tiết phiếu)'])
    d.step(['Bước 3: Chọn phiếu nhập kho ', '@o_phieunhapkho', '. Hệ thống điền Phiếu kiểm kê, Kho, Thủ kho và nạp dòng hàng.'])
    d.img('10c_filled', 'Màn hình Tạo phiếu nhập hàng điều chỉnh kiểm kê')
    d.step(['Bước 4: Chọn Nhân viên ', '@o_nhanvien', ', nhập Ghi chú ', '@o_ghichu'])
    d.step(['Bước 5: Ở bảng Chi tiết, sửa Đơn giá nhập ', '@o_dongia', ' nếu cần, chọn Kho kế toán ', '@o_khoketoan',
            ' và nhập Số lượng cho từng dòng.'])
    d.sub(['Bấm ', '@btn_themkho', ' để chia 1 dòng vào nhiều kho kế toán, bấm ', '@btn_xoakho', ' để bỏ kho thừa (tổng Số lượng '
           'phải bằng SL nhập).'])
    d.step(['Bước 6: Bấm ', '@btn_themtailieu', ' để đính kèm thêm file (pdf, png, jpg, jpeg) nếu cần.'])
    d.step(['Bước 7: Bấm ', '@btn_luu_form', ' để lưu và về danh sách'])
    d.sub(['Hoặc bấm ', '@btn_luutieptuc', ' để lưu và lập phiếu tiếp'])
    d.sub(['Hoặc bấm ', '@btn_luuduyet', ' để lưu và hạch toán ngay (PHẦN 4)'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ', chọn ', '@btn_thoat', ' để không lưu hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('CHỈNH SỬA PHIẾU')
    d.step('Bước 1: Truy cập vào màn hình Phiếu nhập hàng điều chỉnh kiểm kê, tìm phiếu Đang tạo do mình tạo.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_sua'])
    d.img('12_edit', 'Màn hình Sửa phiếu nhập hàng điều chỉnh kiểm kê')
    d.step(['Bước 3: Sửa Nhân viên ', '@o_nhanvien', ', Ghi chú ', '@o_ghichu', ', Đơn giá nhập ', '@o_dongia', ', Kho kế toán ',
            '@o_khoketoan', ', thêm file bằng ', '@btn_themtailieu', '.'])
    d.step(['Bước 4: Bấm ', '@btn_luu_form', ' để lưu'])
    d.sub(['Hoặc bấm ', '@btn_luuduyet', ' để lưu và duyệt (PHẦN 4)'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ' để không lưu.'])

    d.phan('LƯU VÀ DUYỆT PHIẾU')
    d.step('Bước 1: Mở màn Tạo mới (PHẦN 2) hoặc Sửa (PHẦN 3), nhập đủ Phiếu nhập kho, Nhân viên, Đơn giá nhập, Kho kế toán và '
           'Số lượng.')
    d.step(['Bước 2: Bấm ', '@btn_luuduyet', '. Hệ thống hiện hộp Xác nhận lưu và duyệt.'])
    d.img('10g_confirm_approve', 'Hộp Xác nhận lưu và duyệt')
    d.step(['Bước 3: Bấm ', '@btn_luuduyet_confirm', ' để duyệt'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' để không duyệt.'])

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step(['Bước 1: Bấm vào Số phiếu ', '@link_sophieu', ' để mở màn chi tiết'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step('Bước 1: Truy cập vào màn hình Phiếu nhập hàng điều chỉnh kiểm kê.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn Chi tiết phiếu.'])
    d.sub(['Bấm mã phiếu nhập kho ', '@link_pnk_detail', ' hoặc mã phiếu kiểm kê ', '@link_pkk_detail', ' để mở phiếu đó ở tab mới.'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu nhập hàng điều chỉnh kiểm kê')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu nhập hàng điều chỉnh kiểm kê')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_inds', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách phiếu')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.xuat_excel()
    d.tuy_chinh_cot()
    d.cai_dat_bo_loc()
    return d.save(OUT)


if __name__ == '__main__':
    out = build()
    os.makedirs(CHECK_DIR, exist_ok=True)
    pdf = os.path.join(CHECK_DIR, 'HDSD.pdf')
    size = finalize_word(out, pdf)
    print('docx', out, size)
    for line in toc_lines(out):
        print('  ', line)
    n, warn, sheets = render_check(pdf, os.path.join(CHECK_DIR, 'render'))
    print('pages', n)
    for w_ in warn:
        print('WARN', w_)
    for s in sheets:
        print(s)
