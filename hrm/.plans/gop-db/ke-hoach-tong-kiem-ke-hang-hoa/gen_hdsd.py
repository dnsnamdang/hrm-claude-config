# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Kế hoạch tổng kiểm kê hàng hóa (form chuẩn Danh mục quốc gia, 05/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Ke hoach tong kiem ke hang hoa.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (khtkkhh_shots/uml/overview.png).
Khuôn cấu trúc: ../ke-hoach-kiem-ke-theo-hang-hoa/gen_hdsd.py.
Ảnh + icon: khtkkhh_shots (dev-hrm 05/11/2026, _capture/capture.js chặn mọi yêu cầu ghi). Ảnh Sửa / Xóa / menu Hành động khác chụp
bằng cách giả trạng thái Đang tạo trên trình duyệt (dev chỉ có kế hoạch Đã duyệt).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Kế hoạch tổng kiểm kê hàng hóa'
SHOTS = os.path.join(HERE, 'khtkkhh_shots')
OUT = os.path.join(HERE, 'HDSD_Ke hoach tong kiem ke hang hoa.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_khtkkhh')

THUAT_NGU = [
    ['Kế hoạch tổng kiểm kê hàng hóa', 'Phiếu <mã công ty>.KHTKK-NNNNN: thời gian kiểm kê, các kho, công ty thuê kho, thành phần '
                                       'tham gia và nội dung yêu cầu của một đợt tổng kiểm kê.'],
    ['Công ty thuê kho', 'Công ty có kho kế toán trong các kho đã chọn (hiển thị mã công ty).'],
    ['Thành phần tham gia', 'Các phòng ban tham gia đợt kiểm kê.'],
    ['Đang tạo', 'Kế hoạch lưu nháp; chỉ người tạo thấy, sửa, xóa.'],
    ['Đã duyệt', 'Kế hoạch đã Lưu và duyệt; dùng để lập phiếu kiểm kê theo hàng hóa.'],
]
PHIEN_BAN = [['1.0', '05/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Tạo, Lưu nháp, Lưu và duyệt, In, Xuất Excel, Xem lịch sử', 'Không cần quyền riêng.'],
    ['Sửa, Xóa', 'Người tạo kế hoạch, khi kế hoạch Đang tạo.'],
    ['Xem kế hoạch của mọi công ty', 'Tổng kiểm kê kho theo hàng hóa - tổng công ty.'],
    ['Xem kế hoạch của công ty mình', 'Tổng kiểm kê kho theo hàng hóa (không có quyền: chỉ xem kế hoạch mình tạo).'],
    ['Lập phiếu kiểm kê hàng hóa', 'Lập phiếu kiểm kê kho theo hàng hóa.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Kiểm kê ', '@menu_nhom',
            ', chọn Kế hoạch tổng kiểm kê hàng hóa ', '@menu_muc'])
    d.img('01_list', 'Màn hình Kế hoạch tổng kiểm kê hàng hóa')
    d.step(['Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_kho', ' để lọc theo Kho'])
    for lb, ic in [('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'), ('Mã hàng hóa', 'o_mahang'),
                   ('Tên hàng hóa', 'o_tenhang'), ('Ngày tạo', 'o_ngaytao'), ('Công ty', 'o_congty'),
                   ('Phòng ban', 'o_phongban')]:
        d.sub(['Hoặc chọn / nhập giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('THÊM MỚI KẾ HOẠCH')
    d.step('Bước 1: Truy cập vào màn hình Kế hoạch tổng kiểm kê hàng hóa (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10c_filled', 'Màn hình Tạo kế hoạch tổng kiểm kê hàng hóa')
    d.step(['Bước 3: Chọn Ngày kiểm kê từ ', '@o_ngaytu', ' và Ngày kiểm kê đến ', '@o_ngayden', ' (bắt buộc).'])
    d.step(['Bước 4: Chọn Kho ', '@o_kho_form', ' (chọn được nhiều kho). Công ty thuê kho ', '@o_congtythue',
            ' tự chọn theo kho, bỏ bớt nếu cần.'])
    d.step(['Bước 5: Chọn Thành phần tham gia ', '@o_thanhphan', ', nhập Nội dung yêu cầu ', '@o_noidung', ' (tối đa 255 ký tự).'])
    d.step(['Bước 6: Bấm ', '@btn_luunhap', ' để lưu kế hoạch ở trạng thái Đang tạo ', '@badge_dangtao', ', về màn danh sách'])
    d.sub(['Hoặc ', '@btn_luuduyet', ' để lưu và duyệt luôn (xem PHẦN 3).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi tạo tiếp kế hoạch khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('LƯU VÀ DUYỆT')
    d.step('Bước 1: Ở màn Tạo hoặc Sửa kế hoạch, nhập đủ 6 trường: Ngày kiểm kê từ, Ngày kiểm kê đến, Kho, Công ty thuê kho, '
           'Thành phần tham gia, Nội dung yêu cầu.')
    d.step(['Bước 2: Bấm ', '@btn_luuduyet', '. Hệ thống lưu kế hoạch ở trạng thái Đã duyệt ', '@badge_daduyet',
            ' và gửi thông báo cho người lập phiếu kiểm kê.'])
    d.step('Bước 3: Nếu thiếu thông tin, các ô thiếu viền đỏ; nhập bổ sung rồi bấm lại.')
    d.img('10b_validate', 'Màn hình báo thiếu thông tin khi Lưu và duyệt')

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Kế hoạch tổng kiểm kê hàng hóa.')
    d.step(['Bước 2: Ở dòng kế hoạch Đang tạo ', '@badge_dangtao', ' của mình, bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_sua'])
    d.step('Bước 3: Hệ thống mở màn “Sửa kế hoạch tổng kiểm kê hàng hóa”.')
    d.img('12_edit', 'Màn hình Sửa kế hoạch tổng kiểm kê hàng hóa')
    d.step('Bước 4: Sửa thông tin (quy tắc như Thêm mới).')
    d.step(['Bước 5: Bấm ', '@btn_luunhap'])
    d.sub(['Hoặc ', '@btn_luuduyet', ' để lưu và duyệt.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu.'])

    d.phan('XÓA')
    d.step(['Bước 1: Ở dòng kế hoạch Đang tạo của mình, bấm ', '@btn_xoa_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_xoa'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa”')
    d.img('13_delete', 'Hộp xác nhận xóa kế hoạch')
    d.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

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
    d.step('Bước 1: Truy cập vào màn hình Kế hoạch tổng kiểm kê hàng hóa.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết kế hoạch tổng kiểm kê hàng hóa”.'])
    d.img('17_detail', 'Màn hình Chi tiết kế hoạch tổng kiểm kê hàng hóa')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('LẬP PHIẾU KIỂM KÊ HÀNG HÓA')
    d.step(['Bước 1: Ở dòng kế hoạch Đã duyệt ', '@badge_daduyet', ', bấm ', '@btn_lapphieu_row'])
    d.sub(['Hoặc tại màn chi tiết kế hoạch, bấm ', '@btn_lapphieu'])
    d.step('Bước 2: Hệ thống mở màn Tạo phiếu kiểm kê theo hàng hóa đã nạp sẵn kho, công ty thuê kho của kế hoạch; thêm hàng '
           'và lập phiếu ở màn đó.')
    d.img('15b_lapphieu_target', 'Màn Tạo phiếu kiểm kê theo hàng hóa nạp sẵn kế hoạch tổng')

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước kế hoạch tổng kiểm kê hàng hóa')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách kế hoạch tổng kiểm kê hàng hóa')
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
