# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu xuất điều chỉnh sai số liệu (form chuẩn Danh mục quốc gia, 09/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu xuat dieu chinh sai so lieu.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (pxdc_shots/uml/overview.png).
Khuôn cấu trúc: ../borrow-export/gen_hdsd.py.
Ảnh + icon: pxdc_shots (dev-hrm 09/11/2026, _capture/capture.js, chặn mọi yêu cầu ghi — 0 yêu cầu ghi).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu xuất điều chỉnh sai số liệu'
SHOTS = os.path.join(HERE, 'pxdc_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu xuat dieu chinh sai so lieu.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pxdc')

THUAT_NGU = [
    ['Phiếu xuất điều chỉnh sai số liệu (phiếu xuất lại)', 'Chứng từ PXL-NNNNN trừ toàn bộ hàng của một phiếu nhập kho bị '
                                                          'Không duyệt ra khỏi kho, đúng lô và vị trí đã nhập.'],
    ['Phiếu nhập kho', 'Phiếu PNK-NNNNN ở màn Phiếu nhập kho; mỗi phiếu xuất lại gắn 1 phiếu nhập kho gốc.'],
    ['Phiếu nhập lại', 'Phiếu nhập kho mới lập bằng nút Tạo phiếu nhập lại, chép thông tin phiếu nhập kho gốc.'],
    ['Chờ nhập lại', 'Trạng thái (nhãn vàng): phiếu xuất lại chưa có phiếu nhập lại.'],
    ['Đã nhập lại', 'Trạng thái (nhãn xanh lá): đã lập phiếu nhập lại.'],
]
PHIEN_BAN = [['1.0', '09/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, chi tiết, in, xuất Excel, xem lịch sử',
     'Một trong 4 quyền Xem phiếu xuất lại theo tổng công ty / công ty / phòng ban / bộ phận. Không có quyền nào thì chỉ '
     'thấy phiếu mình tạo.'],
    ['Tạo phiếu xuất lại, Tạo phiếu nhập lại', 'Người đã tạo phiếu nhập kho gốc.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Kho ', '@menu_phanhe', ', tại menu Xuất kho ', '@menu_nhom',
            ', chọn Phiếu xuất điều chỉnh sai số liệu ', '@menu_muc'])
    d.img('01_list', 'Màn hình Danh sách phiếu xuất lại')
    d.step(['Bước 2: Nhập mã phiếu hoặc mã phiếu nhập kho vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', nhập ', '@o_maphieu', ' để lọc theo Mã phiếu'])
    for lb, ic in [('Phiếu nhập kho', 'o_phieunhapkho'), ('Người tạo', 'o_nguoitao'), ('Trạng thái', 'o_trangthai'),
                   ('Ngày tạo', 'o_ngaytao'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban')]:
        d.sub(['Hoặc chọn / nhập giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('TẠO PHIẾU XUẤT LẠI')
    d.step(['Bước 1: Từ phân hệ Kho ', '@menu_phanhe', ', tại menu Nhập kho ', '@menu_nhom_nk', ', chọn Phiếu nhập kho ',
            '@menu_muc_pnk', ', mở chi tiết phiếu nhập kho đang Không duyệt do mình tạo.'])
    d.step(['Bước 2: Bấm ', '@btn_taophieuxuatlai', '. Hệ thống mở màn Tạo phiếu xuất lại.'])
    d.img('10_create', 'Màn hình Tạo phiếu xuất lại')
    d.step(['Bước 3: Nhập Ghi chú ', '@o_ghichu', ' (không bắt buộc, tối đa 255 ký tự).'])
    d.step(['Bước 4: Bấm ', '@btn_xuatlai', '. Hệ thống hiện hộp Xác nhận xuất lại.'])
    d.step(['Bước 5: Bấm ', '@btn_xuatlai_confirm', ' để xuất lại, hệ thống chuyển về Danh sách phiếu xuất lại.'])
    d.sub(['Hoặc bấm ', '@btn_dong_confirm', ' để không xuất lại.'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ' để về phiếu nhập kho.'])

    d.phan('TẠO PHIẾU NHẬP LẠI')
    d.step('Bước 1: Truy cập vào màn hình Danh sách phiếu xuất lại (PHẦN 1), tìm phiếu đang Chờ nhập lại.')
    d.step(['Bước 2: Ở cột Hành động, bấm ', '@btn_taophieunhaplai_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_taophieunhaplai'])
    d.img('22_reimport', 'Màn hình Tạo phiếu nhập lại')
    d.step('Bước 3: Kiểm tra số lượng, vị trí từng dòng hàng; đính kèm file và nhập các thông tin bắt buộc như phiếu nhập kho.')
    d.step(['Bước 4: Bấm ', '@btn_luunhap_ri', ' để lưu và nhập kho'])
    d.sub(['Hoặc bấm ', '@btn_luu_ri', ' để lưu phiếu ở trạng thái Đang tạo.'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ' để không lưu.'])

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step(['Bước 1: Bấm vào Mã phiếu ', '@link_sophieu', ' để mở màn chi tiết'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step('Bước 1: Truy cập vào màn hình Danh sách phiếu xuất lại.')
    d.step(['Bước 2: Bấm vào Mã phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết phiếu xuất điều chỉnh sai số liệu”.'])
    d.sub(['Bấm mã phiếu nhập kho ', '@link_pnk_detail', ' để mở phiếu nhập kho gốc.'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu xuất điều chỉnh sai số liệu')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu xuất lại')
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
