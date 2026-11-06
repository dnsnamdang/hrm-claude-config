# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Biên bản xử lý hàng thừa, thiếu sau kiểm kê (form chuẩn Danh mục quốc gia, 06/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Bien ban xu ly hang thua thieu sau kiem ke.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (bbxltt_shots/uml/overview.png).
Khuôn cấu trúc: ../ke-hoach-tong-kiem-ke-hang-hoa/gen_hdsd.py.
Ảnh + icon: bbxltt_shots (dev-hrm 06/11/2026, _capture/capture.js chặn mọi yêu cầu ghi). Ảnh Sửa (12_edit) chụp bằng cách giả trạng
thái Đang tạo trên trình duyệt (dev không có biên bản Đang tạo).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Biên bản xử lý hàng thừa, thiếu sau kiểm kê'
SHOTS = os.path.join(HERE, 'bbxltt_shots')
OUT = os.path.join(HERE, 'HDSD_Bien ban xu ly hang thua thieu sau kiem ke.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_bbxltt')

THUAT_NGU = [
    ['Biên bản xử lý hàng thừa, thiếu', 'Phiếu BBXLKKHH-NNNNN ghi cách xử lý chênh lệch sau kiểm kê của một kho trong khoảng ngày.'],
    ['Hàng thừa / Hàng thiếu', 'Hàng có số thực kiểm lớn hơn / nhỏ hơn số sổ sách trên phiếu kiểm kê theo hàng hóa đã hoàn thành.'],
    ['Phiếu xử lý', 'Phiếu nhập / xuất kho điều chỉnh kiểm kê của hàng — nguồn đơn giá vốn.'],
    ['Giá xử lý', 'Giá vốn hoặc Giá bán — cơ sở tính chi phí của dòng.'],
    ['NV chịu', 'Nhân viên chịu phần chi phí nhân viên của dòng.'],
    ['Đang tạo', 'Biên bản đã lưu, chưa gửi duyệt; chỉ người tạo thấy và sửa.'],
    ['Chờ duyệt', 'Biên bản đã gửi duyệt; người có quyền Duyệt xử lý.'],
    ['Đã duyệt', 'Biên bản đã duyệt, hệ thống đã ghi bút toán.'],
]
PHIEN_BAN = [['1.0', '06/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Tạo mới, Lấy dữ liệu', 'Kế toán kho.'],
    ['Sửa, Lưu và gửi duyệt từ màn Sửa', 'Người tạo biên bản, khi biên bản Đang tạo.'],
    ['Duyệt', 'Duyệt biên bản xử lý hàng thừa, thiếu sau kiểm kê.'],
    ['Xem biên bản của mọi công ty', 'Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo tổng công ty.'],
    ['Xem biên bản của công ty mình', 'Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo công ty (không có quyền: chỉ '
                                      'biên bản mình tạo).'],
    ['In, Xuất Excel, Xem lịch sử', 'Không cần quyền riêng (theo phạm vi xem).'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Kiểm kê ', '@menu_nhom',
            ', chọn Biên bản xử lý hàng thừa, thiếu sau kiểm kê ', '@menu_muc'])
    d.img('01_list', 'Màn hình Biên bản xử lý hàng thừa, thiếu sau kiểm kê')
    d.step(['Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_kho', ' để lọc theo Kho'])
    for lb, ic in [('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'), ('Người duyệt', 'o_nguoiduyet'),
                   ('Ngày tạo', 'o_ngaytao')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('THÊM MỚI BIÊN BẢN')
    d.step('Bước 1: Truy cập vào màn hình Biên bản xử lý hàng thừa, thiếu sau kiểm kê (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step(['Bước 3: Chọn Từ ngày ', '@o_tungay', ', Đến ngày ', '@o_denngay', ', Kho vật lý ', '@o_kho_form',
            ' (bắt buộc); nhập Ghi chú ', '@o_ghichu', ' nếu cần.'])
    d.step(['Bước 4: Bấm ', '@btn_laydulieu', '. Hệ thống nạp các phiếu kiểm kê và chia hàng vào 2 tab ', '@tab_thua', ' và ',
            '@tab_thieu'])
    d.img('10c_filled', 'Màn hình Tạo biên bản sau khi Lấy dữ liệu')
    d.sub(['Hoặc bỏ tích phiếu kiểm kê ', '@chk_phieukk', ' để bỏ các dòng của phiếu đó.'])
    d.step(['Bước 5: Ở từng dòng của 2 tab, nhập Lý do ', '@o_lydo', ', chọn Giá xử lý ', '@o_giaxuly', ', nhập % Chi phí nhân viên ',
            '@o_pctnv', ', chọn NV chịu ', '@o_nvchiu', ' (bắt buộc).'])
    d.step(['Bước 6: Bấm ', '@btn_luu', ' để lưu biên bản ở trạng thái Đang tạo ', '@badge_dangtao', ', về màn danh sách'])
    d.sub(['Hoặc ', '@btn_luuguiduyet', ' để lưu và gửi duyệt luôn (xem PHẦN 3).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu rồi tạo tiếp biên bản khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('LƯU VÀ GỬI DUYỆT')
    d.step('Bước 1: Ở màn Tạo hoặc Sửa biên bản, Lấy dữ liệu và nhập đủ Lý do, Giá xử lý, %, NV chịu cho mọi dòng.')
    d.step(['Bước 2: Bấm ', '@btn_luuguiduyet', '. Hệ thống lưu biên bản ở trạng thái Chờ duyệt ', '@badge_choduyet',
            ' và gửi thông báo cho người duyệt.'])
    d.step('Bước 3: Nếu thiếu thông tin, các ô thiếu viền đỏ; nhập bổ sung rồi bấm lại.')
    d.img('10e_row_validate', 'Màn hình báo thiếu thông tin ở từng dòng')

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Biên bản xử lý hàng thừa, thiếu sau kiểm kê.')
    d.step(['Bước 2: Ở dòng biên bản Đang tạo ', '@badge_dangtao', ' của mình, bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_sua'])
    d.step('Bước 3: Hệ thống mở màn “Sửa biên bản xử lý hàng thừa, thiếu”.')
    d.img('12_edit', 'Màn hình Sửa biên bản')
    d.step(['Bước 4: Sửa thông tin (quy tắc như Thêm mới); đổi ngày hoặc kho thì bấm lại ', '@btn_laydulieu'])
    d.step(['Bước 5: Bấm ', '@btn_luu'])
    d.sub(['Hoặc ', '@btn_luuguiduyet', ' để lưu và gửi duyệt.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu.'])

    d.phan('DUYỆT BIÊN BẢN')
    d.step(['Bước 1: Ở dòng biên bản Chờ duyệt ', '@badge_choduyet', ', bấm ', '@btn_duyet_row', ' để mở màn chi tiết'])
    d.sub('Hoặc bấm thông báo “[BBXLKKHH] Chờ duyệt” trên chuông.')
    d.img('14_approve', 'Màn hình Chi tiết biên bản chờ duyệt')
    d.step(['Bước 2: Kiểm tra, sửa nếu cần Giá xử lý ', '@o_giaxuly', ', % Chi phí nhân viên ', '@o_pctnv', ', NV chịu ', '@o_nvchiu'])
    d.step(['Bước 3: Bấm ', '@btn_duyet', '. Hệ thống chuyển biên bản sang Đã duyệt ', '@badge_daduyet', ' và ghi bút toán.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không duyệt.'])

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_lichsu'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step(['Bước 1: Bấm vào Số phiếu ', '@link_sophieu', ' để mở màn chi tiết'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step('Bước 1: Truy cập vào màn hình Biên bản xử lý hàng thừa, thiếu sau kiểm kê.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết biên bản xử lý hàng thừa, thiếu”.'])
    d.img('17_detail', 'Màn hình Chi tiết biên bản')
    d.step(['Bước 3: Bấm ', '@tab_thieu', ' để xem hàng thiếu; bấm số phiếu xử lý ', '@link_phieuxuly', ' để mở phiếu ở tab mới.'])
    d.step(['Bước 4: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('IN BIÊN BẢN')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước biên bản')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách biên bản')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.xuat_excel()
    d.phan('XUẤT EXCEL 1 BIÊN BẢN')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_xuat_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_xuat'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_xuat'])
    d.step('Bước 2: Hệ thống tải file Excel của biên bản; mở file đã tải để xem.')
    d.img('03b_rowmenu_wait', 'Nút Xuất Excel trong menu Hành động khác')
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
