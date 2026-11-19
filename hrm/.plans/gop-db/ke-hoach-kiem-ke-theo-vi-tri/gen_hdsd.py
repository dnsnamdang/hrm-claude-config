# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Kế hoạch kiểm kê theo vị trí (form chuẩn Danh mục quốc gia, 05/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Ke hoach kiem ke theo vi tri.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (khkkvt_shots/uml/overview.png).
Khuôn cấu trúc: ../borrow-export/gen_hdsd.py.
Ảnh + icon: khkkvt_shots (dev-hrm 05/11/2026, _capture/capture.js chặn mọi yêu cầu ghi). Ảnh Sửa / Xóa / Lập phiếu kiểm kê chụp
bằng cách bật cờ tạm trên trình duyệt (dev không có kế hoạch Đang tạo / Đang kiểm của DNS Admin).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Kế hoạch kiểm kê theo vị trí'
SHOTS = os.path.join(HERE, 'khkkvt_shots')
OUT = os.path.join(HERE, 'HDSD_Ke hoach kiem ke theo vi tri.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_khkkvt')

THUAT_NGU = [
    ['Kế hoạch kiểm kê theo vị trí', 'Phiếu <mã công ty>-KHKKVT-NNNNN: phạm vi vị trí cần kiểm, hàng tồn từng lô và hội đồng '
                                     'kiểm kê của một kho vật lý.'],
    ['Phạm vi kiểm kê', 'Các Nhà / Dãy / Khoang / Vị trí được tick trong kho.'],
    ['Lấy vị trí', 'Lấy danh sách hàng còn tồn theo từng lô tại các vị trí đã tick.'],
    ['Hội đồng kiểm kê', 'Nhân viên tham gia kiểm kê, mỗi người kèm 1 chức vụ.'],
    ['Đang tạo', 'Kế hoạch mới lưu; chỉ người tạo thấy, sửa, xóa.'],
    ['Đang kiểm', 'Kế hoạch đã gửi thủ kho; chờ lập phiếu kiểm kê.'],
    ['Đã lập kiểm kê', 'Thủ kho đã lập phiếu kiểm kê từ kế hoạch.'],
    ['Hoàn thành', 'Phiếu kiểm kê của kế hoạch đã xử lý xong.'],
]
PHIEN_BAN = [['1.0', '05/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Tạo, Lưu, Lưu và gửi, In, Xuất Excel, Xem lịch sử', 'Không cần quyền riêng.'],
    ['Sửa, Xóa', 'Người tạo kế hoạch, khi kế hoạch Đang tạo.'],
    ['Xem kế hoạch của mọi công ty', 'Xem kế hoạch kiểm kê theo vị trí theo tổng công ty.'],
    ['Xem kế hoạch của công ty mình', 'Xem kế hoạch kiểm kê theo vị trí theo công ty (không có quyền: chỉ xem kế hoạch mình tạo).'],
    ['Lập phiếu kiểm kê', 'Thủ kho của kho, có quyền Lập phiếu kiểm kê kho theo vị trí.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Kiểm kê ', '@menu_nhom',
            ', chọn Kế hoạch kiểm kê theo vị trí ', '@menu_muc'])
    d.img('01_list', 'Màn hình Kế hoạch kiểm kê theo vị trí')
    d.step(['Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai', ' để lọc theo Trạng thái'])
    for lb, ic in [('Người tạo', 'o_nguoitao'), ('Hàng hóa (mã hoặc tên)', 'o_hanghoa'), ('Ngày kiểm kê', 'o_ngaykiemke'),
                   ('Kho', 'o_kho'), ('Nhà', 'o_nha'), ('Dãy', 'o_day'), ('Khoang', 'o_khoang'), ('Vị trí', 'o_vitri'),
                   ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban')]:
        d.sub(['Hoặc chọn / nhập giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('THÊM MỚI KẾ HOẠCH')
    d.step('Bước 1: Truy cập vào màn hình Kế hoạch kiểm kê theo vị trí (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step(['Bước 3: Chọn Kho vật lý ', '@o_kho_form', ' (bắt buộc). Ngày kiểm kê tự điền ngày hôm nay.'])
    d.step('Bước 4: Ở khối Phạm vi kiểm kê, tick Nhà → Dãy → Khoang → Vị trí cần kiểm (bắt buộc ít nhất 1 vị trí).')
    d.step(['Bước 5: Bấm ', '@btn_layvitri', ' để lấy hàng tồn vào bảng Chi tiết.'])
    d.img('10c_filled', 'Màn hình Tạo kế hoạch kiểm kê theo vị trí')
    d.step('Bước 6: Ở khối Hội đồng kiểm kê, chọn Nhân viên (bắt buộc); Chức vụ tự điền, đổi được (bắt buộc).')
    d.sub(['Hoặc bấm ', '@btn_themdong', ' để thêm thành viên, bấm ', '@btn_xoa_member', ' để bỏ thành viên.'])
    d.step(['Bước 7: Bấm ', '@btn_luu_form', ' để lưu kế hoạch ở trạng thái Đang tạo, về màn danh sách'])
    d.sub(['Hoặc ', '@btn_luugui', ' để lưu và gửi luôn cho thủ kho (xem PHẦN 4).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu rồi tạo tiếp kế hoạch khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('CHỌN PHẠM VI KIỂM KÊ VÀ LẤY VỊ TRÍ')
    d.step('Bước 1: Ở màn Tạo / Sửa, chọn Kho vật lý.')
    d.step('Bước 2: Tick Nhà ở cột Nhà; cột Dãy hiện dãy của nhà đã tick. Làm tương tự với Dãy, Khoang.')
    d.img('10d_scope', 'Khối Phạm vi kiểm kê')
    d.step('Bước 3: Tick Vị trí ở cột Vị trí (gồm nhóm Vị trí tự do).')
    d.sub('Hoặc gõ vào ô tìm của cột để tìm theo mã / tên, tick Chọn hết để chọn mọi mục đang hiện.')
    d.step(['Bước 4: Bấm ', '@btn_layvitri', '. Hệ thống đổ hàng tồn theo từng lô vào bảng Chi tiết.'])
    d.step('Bước 5: Đổi Kho vật lý khi bảng Chi tiết đã có dữ liệu: hệ thống hỏi “Đổi kho vật lý”.')
    d.sub(['Bấm ', '@btn_doikho', ' để đổi kho (xóa phạm vi và bảng Chi tiết) hoặc ', '@btn_huy_doikho', ' để giữ kho cũ.'])

    d.phan('LƯU VÀ GỬI KẾ HOẠCH CHO THỦ KHO')
    d.step('Bước 1: Ở màn Tạo hoặc Sửa kế hoạch, nhập đủ thông tin như PHẦN 2.')
    d.step(['Bước 2: Bấm ', '@btn_luugui', '. Hệ thống lưu kế hoạch ở trạng thái Đang kiểm ', '@badge_dangkiem',
            ' và gửi thông báo cho thủ kho của kho.'])
    d.img('10b_validate', 'Thiếu thông tin bắt buộc: hệ thống báo lỗi đỏ dưới từng ô')
    d.step('Bước 3: Nếu thiếu thông tin, nhập bổ sung các ô viền đỏ rồi bấm lại.')

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Kế hoạch kiểm kê theo vị trí.')
    d.step(['Bước 2: Ở dòng kế hoạch Đang tạo ', '@badge_dangtao', ' của mình, bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_sua'])
    d.step('Bước 3: Hệ thống mở màn “Sửa kế hoạch kiểm kê theo vị trí”.')
    d.img('12_edit', 'Màn hình Sửa kế hoạch kiểm kê theo vị trí')
    d.step(['Bước 4: Sửa thông tin (quy tắc như Thêm mới); đổi phạm vi thì bấm lại ', '@btn_layvitri'])
    d.step(['Bước 5: Bấm ', '@btn_luu_form'])
    d.sub(['Hoặc ', '@btn_luugui', ' để lưu và gửi cho thủ kho.'])
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
    d.step('Bước 1: Truy cập vào màn hình Kế hoạch kiểm kê theo vị trí.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết kế hoạch kiểm kê theo vị trí”.'])
    d.img('17_detail', 'Màn hình Chi tiết kế hoạch kiểm kê theo vị trí')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('LẬP PHIẾU KIỂM KÊ TỪ KẾ HOẠCH')
    d.step(['Bước 1: (Thủ kho) Ở dòng kế hoạch Đang kiểm ', '@badge_dangkiem', ', bấm ', '@btn_lapphieu_row'])
    d.sub(['Hoặc tại màn chi tiết kế hoạch, bấm ', '@btn_lapphieu'])
    d.img('15_send_detail', 'Màn chi tiết kế hoạch Đang kiểm có nút Lập phiếu kiểm kê')
    d.step('Bước 2: Hệ thống mở màn Thêm phiếu kiểm kê theo vị trí với kế hoạch đã chọn sẵn; lập phiếu ở màn đó.')

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước kế hoạch kiểm kê theo vị trí')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách kế hoạch kiểm kê theo vị trí')
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
