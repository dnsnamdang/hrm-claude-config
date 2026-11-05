# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Kế hoạch kiểm kê theo hàng hóa (form chuẩn Danh mục quốc gia, 05/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Ke hoach kiem ke theo hang hoa.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (khkkhh_shots/uml/overview.png).
Khuôn cấu trúc: ../ke-hoach-kiem-ke-theo-vi-tri/gen_hdsd.py.
Ảnh + icon: khkkhh_shots (dev-hrm 05/11/2026, _capture/capture.js chặn mọi yêu cầu ghi). Ảnh Sửa / Xóa / Lập phiếu kiểm kê chụp
bằng cách bật cờ tạm trên trình duyệt (dev chỉ có kế hoạch Đã lập phiếu kiểm kê); popup cảnh báo phiếu chưa xử lý xong mở trên trình duyệt.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Kế hoạch kiểm kê theo hàng hóa'
SHOTS = os.path.join(HERE, 'khkkhh_shots')
OUT = os.path.join(HERE, 'HDSD_Ke hoach kiem ke theo hang hoa.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_khkkhh')

THUAT_NGU = [
    ['Kế hoạch kiểm kê theo hàng hóa', 'Phiếu <mã công ty>.KHKKHH-NNNNN: các kho, danh sách hàng cần kiểm kèm tồn kho kế toán và '
                                       'hội đồng kiểm kê.'],
    ['Kho kế toán', 'Kho sổ sách của kho vật lý theo công ty; mỗi hàng có một hoặc nhiều dòng kho kế toán.'],
    ['Làm mới số liệu', 'Lấy lại tồn kho kế toán hiện tại của các hàng trong bảng (bấm Lưu mới ghi).'],
    ['Hội đồng kiểm kê', 'Nhân viên tham gia kiểm kê, mỗi người kèm 1 chức vụ.'],
    ['Đang tạo', 'Kế hoạch mới lưu; chỉ người tạo thấy, sửa, xóa.'],
    ['Đang kiểm', 'Kế hoạch đã Lưu và kiểm; chờ lập phiếu kiểm kê.'],
    ['Đã lập phiếu kiểm kê', 'Đã có phiếu kiểm kê theo hàng hóa lập từ kế hoạch.'],
]
PHIEN_BAN = [['1.0', '05/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Tạo, Lưu, Lưu và kiểm, In, Xuất Excel, Xem lịch sử', 'Không cần quyền riêng.'],
    ['Sửa, Xóa', 'Người tạo kế hoạch, khi kế hoạch Đang tạo.'],
    ['Xem kế hoạch của mọi công ty', 'Tổng kiểm kê kho theo hàng hóa - tổng công ty.'],
    ['Xem kế hoạch của công ty mình', 'Tổng kiểm kê kho theo hàng hóa (không có quyền: chỉ xem kế hoạch mình tạo).'],
    ['Lập phiếu kiểm kê theo hàng hóa', 'Lập phiếu kiểm kê kho theo hàng hóa.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Kiểm kê ', '@menu_nhom',
            ', chọn Kế hoạch kiểm kê theo hàng hóa ', '@menu_muc'])
    d.img('01_list', 'Màn hình Kế hoạch kiểm kê theo hàng hóa')
    d.step(['Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_kho', ' để lọc theo Kho'])
    for lb, ic in [('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'), ('Mã hàng hóa', 'o_mahang'),
                   ('Tên hàng hóa', 'o_tenhang'), ('Ngày kiểm kê', 'o_ngaykiemke'), ('Công ty', 'o_congty'),
                   ('Phòng ban', 'o_phongban')]:
        d.sub(['Hoặc chọn / nhập giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('THÊM MỚI KẾ HOẠCH')
    d.step('Bước 1: Truy cập vào màn hình Kế hoạch kiểm kê theo hàng hóa (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step(['Bước 3: Chọn Kho ', '@o_kho_form', ' (bắt buộc, chọn được nhiều kho). Ngày kiểm kê tự điền ngày hôm nay.'])
    d.step(['Bước 4: Nhập Ghi chú ', '@o_ghichu', ' nếu cần (tối đa 255 ký tự).'])
    d.step(['Bước 5: Bấm ', '@btn_themhang', ' để chọn hàng cần kiểm (bắt buộc ít nhất 1 hàng, xem PHẦN 3).'])
    d.img('10c_filled', 'Màn hình Tạo kế hoạch kiểm kê theo hàng hóa')
    d.step('Bước 6: Ở khối Hội đồng kiểm kê, chọn Thành viên (bắt buộc); Chức vụ tự điền, đổi được (bắt buộc).')
    d.sub(['Hoặc bấm ', '@btn_themdong', ' để thêm thành viên, bấm ', '@btn_xoa_member', ' để bỏ thành viên.'])
    d.step(['Bước 7: Bấm ', '@btn_luu_form', ' để lưu kế hoạch ở trạng thái Đang tạo, về màn danh sách'])
    d.sub(['Hoặc ', '@btn_luukiem', ' để lưu và chuyển luôn sang Đang kiểm (xem PHẦN 4).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu rồi tạo tiếp kế hoạch khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('THÊM HÀNG HÓA VÀ LÀM MỚI SỐ LIỆU')
    d.step('Bước 1: Ở màn Tạo / Sửa, chọn Kho trước.')
    d.step(['Bước 2: Bấm ', '@btn_themhang', '. Hệ thống mở cửa sổ “Thêm hàng hóa” (chỉ hàng còn tồn kho kế toán trong kho đã chọn).'])
    d.img('11_picker', 'Cửa sổ Thêm hàng hóa')
    d.step('Bước 3: Tìm theo mã / tên / model, tick các hàng cần kiểm.')
    d.sub('Hoặc bấm vào tên hàng để chọn nhanh 1 hàng.')
    d.step(['Bước 4: Bấm ', '@btn_them_picker', '. Hệ thống thêm hàng kèm tồn từng kho kế toán vào bảng Hàng hóa.'])
    d.sub(['Hoặc bấm ', '@btn_dong_picker', ' để không thêm.'])
    d.step(['Bước 5: Bấm ', '@btn_xoa_hang', ' ở cột Hành động để bỏ một hàng.'])
    d.step(['Bước 6: Bấm ', '@btn_lammoisolieu', ' để lấy lại tồn kho kế toán hiện tại (hàng hết tồn bị bỏ); bấm Lưu để ghi.'])
    d.step('Bước 7: Đổi Kho khi bảng đã có hàng: hệ thống hỏi “Đổi kho”.')
    d.sub(['Bấm ', '@btn_doikho', ' để đổi kho (xóa hết hàng đã chọn) hoặc ', '@btn_huy_doikho', ' để giữ kho cũ.'])

    d.phan('LƯU VÀ KIỂM')
    d.step('Bước 1: Ở màn Tạo hoặc Sửa kế hoạch, nhập đủ thông tin như PHẦN 2.')
    d.step(['Bước 2: Bấm ', '@btn_luukiem', '. Hệ thống lưu kế hoạch ở trạng thái Đang kiểm ', '@badge_dangkiem',
            ' và gửi thông báo cho người lập phiếu kiểm kê.'])
    d.step('Bước 3: Nếu các kho còn phiếu nhập / xuất kho chưa xử lý xong, hệ thống hiện cửa sổ “Cảnh báo phiếu chưa xử lý xong”.')
    d.img('10f_pending', 'Cửa sổ Cảnh báo phiếu chưa xử lý xong')
    d.step(['Bước 4: Bấm số phiếu để mở phiếu ở tab mới và xử lý xong, bấm ', '@btn_dong_pending', ' rồi bấm lại ', '@btn_luukiem'])
    d.sub('Hoặc nếu thiếu thông tin, nhập bổ sung các ô viền đỏ rồi bấm lại.')

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Kế hoạch kiểm kê theo hàng hóa.')
    d.step(['Bước 2: Ở dòng kế hoạch Đang tạo ', '@badge_dangtao', ' của mình, bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_sua'])
    d.step('Bước 3: Hệ thống mở màn “Sửa kế hoạch kiểm kê theo hàng hóa”.')
    d.img('12_edit', 'Màn hình Sửa kế hoạch kiểm kê theo hàng hóa')
    d.step(['Bước 4: Sửa thông tin (quy tắc như Thêm mới); cập nhật tồn bằng ', '@btn_lammoisolieu'])
    d.step(['Bước 5: Bấm ', '@btn_luu_form'])
    d.sub(['Hoặc ', '@btn_luukiem', ' để lưu và chuyển Đang kiểm.'])
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
    d.step('Bước 1: Truy cập vào màn hình Kế hoạch kiểm kê theo hàng hóa.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết kế hoạch kiểm kê theo hàng hóa”.'])
    d.img('17_detail', 'Màn hình Chi tiết kế hoạch kiểm kê theo hàng hóa')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('LẬP PHIẾU KIỂM KÊ THEO HÀNG HÓA')
    d.step(['Bước 1: Ở dòng kế hoạch Đang kiểm ', '@badge_dangkiem', ', bấm ', '@btn_lapphieu_row'])
    d.sub(['Hoặc tại màn chi tiết kế hoạch, bấm ', '@btn_lapphieu'])
    d.img('15_send_detail', 'Màn chi tiết kế hoạch Đang kiểm có nút Lập phiếu kiểm kê theo hàng hóa')
    d.step('Bước 2: Hệ thống mở màn Tạo phiếu kiểm kê theo hàng hóa với kế hoạch đã chọn sẵn; lập phiếu ở màn đó.')

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước kế hoạch kiểm kê theo hàng hóa')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách kế hoạch kiểm kê theo hàng hóa')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.xuat_excel()
    d.phan('XUẤT EXCEL MỘT KẾ HOẠCH')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_xuat_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_xuat'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_xuatexcel_detail'])
    d.img('03_rowmenu', 'Nút Xuất Excel trên dòng và trong menu Hành động khác')
    d.step('Bước 2: Mở file Excel kế hoạch đã tải về.')
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
