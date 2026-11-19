# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu giao việc được giao (form chuẩn Danh mục quốc gia, 18/11/2026).

Chạy: python gen_hdsd_duoc_giao.py  → HDSD_Phieu giao viec duoc giao.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs_duoc_giao.py sinh ra (pgvdg_shots/uml/overview.png).
Khuôn cấu trúc: ../phieu-cho-giao-viec/gen_hdsd.py.
Ảnh + icon: pgvdg_shots (dev-hrm 18/11/2026, _capture/capture.js, chặn mọi yêu cầu ghi — 0 yêu cầu ghi). DNS Admin là người thực hiện của
5 phiếu thật. Ảnh 13_delete + icon btn_xoa_row là GIẢ cờ Xóa trên trình duyệt (không phiếu nào đủ điều kiện Xóa).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu giao việc được giao'
SHOTS = os.path.join(HERE, 'pgvdg_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu giao viec duoc giao.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pgvdg')

THUAT_NGU = [
    ['Phiếu giao việc được giao', 'Danh sách các phiếu giao việc mà bạn có tên trong danh sách người thực hiện (trưởng nhóm hoặc '
                                  'thành viên).'],
    ['Người thực hiện', 'Nhân sự đi làm phiếu, được ghi khi Phiếu giao công tác chứa phiếu giao việc được duyệt.'],
    ['Phiếu nhập kết quả', 'Chứng từ ghi kết quả thực hiện của phiếu giao việc, lập bằng nút Nhập kết quả.'],
    ['Chờ thực hiện', 'Trạng thái (nhãn cam) của phiếu chưa nhập kết quả — được Nhập kết quả.'],
    ['Đang nhập kết quả / Đã nhập kết quả', 'Trạng thái sau khi lưu nháp / gửi duyệt phiếu nhập kết quả.'],
    ['Đang duyệt kết quả / Đã duyệt kết quả', 'Trạng thái trong và sau khi duyệt kết quả.'],
    ['Chờ BKS duyệt kết quả / Đang đề nghị thanh toán / Đã thanh toán', 'Các bước sau duyệt kết quả.'],
]
PHIEN_BAN = [['1.0', '18/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, tìm kiếm, chi tiết, lịch sử, in, xuất Excel', 'Không cần quyền riêng. Chỉ thấy phiếu bạn là người thực hiện.'],
    ['Nhập kết quả', 'Là người thực hiện; phiếu Chờ thực hiện, Phiếu giao công tác đã duyệt, chưa có phiếu nhập kết quả.'],
    ['Xem phiếu nhập kết quả', 'Phiếu đã có phiếu nhập kết quả.'],
    ['Xóa', 'Là người tạo phiếu; phiếu Chờ thực hiện, chưa gắn Phiếu giao công tác.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.truy_cap([('CSKH sau bán', 'menu_phanhe'), ('Giao việc', 'menu_nhom'), ('Phiếu giao việc được giao', 'menu_muc')],
               'số phiếu giao việc',
               bo_loc=[('Số hợp đồng', 'o_sohd'), ('Số phiếu yêu cầu', 'o_soyc'), ('Khách hàng', 'o_khachhang'),
                       ('Người yêu cầu', 'o_nguoiyeucau'), ('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'),
                       ('Người thực hiện', 'o_nguoithuchien'), ('Thời gian dự kiến', 'o_thoigian')])

    d.xoa('Xác nhận xóa', doi_tuong='phiếu giao việc',
          them_cach=['Hoặc mở chi tiết phiếu rồi bấm nút Xóa ở cuối trang'])

    # Viết tay: cột Hành động màn này tối đa 3 nút nên Lịch sử luôn hiện thẳng (không có nút ba chấm)
    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step(['Bước 1: Bấm vào Số phiếu giao việc ', '@link_sophieu', ' để mở màn chi tiết'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step(d.vao)
    d.step(['Bước 2: Bấm vào Số phiếu giao việc ', '@link_sophieu', '. Hệ thống mở màn Chi tiết phiếu giao việc.'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu giao việc')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về danh sách.'])

    d.xuat_excel(cua_so='Chọn trường xuất file')
    d.tuy_chinh_cot()
    d.cai_dat_bo_loc()

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_indanhsach', '. Hệ thống mở cửa sổ “Xem trước danh sách phiếu giao việc”.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách phiếu giao việc')
    d.step(['Bước 3: Bấm ', '@btn_in_popup', ' để in'])
    d.sub(['Hoặc bấm ', '@btn_x_print', ' để đóng.'])

    d.phan('NHẬP KẾT QUẢ')
    d.step(d.vao)
    d.step(['Bước 2: Ở dòng phiếu Chờ thực hiện, tại cột Hành động bấm ', '@btn_nhapkq_row'])
    d.sub(['Hoặc mở chi tiết phiếu rồi bấm ', '@btn_nhapkq_detail'])
    d.step('Bước 3: Hệ thống mở màn Tạo phiếu nhập kết quả với phiếu giao việc đã chọn sẵn.')
    d.img('40_import_create', 'Màn hình Tạo phiếu nhập kết quả')
    d.step('Bước 4: Nhập kết quả thực hiện (theo HDSD Phiếu nhập kết quả).')
    d.step(['Bước 5: Bấm ', '@btn_luu_nkq', ' để lưu nháp'])
    d.sub(['Hoặc bấm ', '@btn_luuguiduyet', ' để gửi duyệt'])
    d.sub(['Hoặc bấm ', '@btn_quaylai', ' để không lưu.'])

    d.phan('XEM PHIẾU NHẬP KẾT QUẢ')
    d.step(d.vao)
    d.step(['Bước 2: Ở dòng phiếu đã nhập kết quả, tại cột Hành động bấm ', '@btn_xemnkq_row'])
    d.sub(['Hoặc mở chi tiết phiếu rồi bấm ', '@btn_xemnkq_detail'])
    d.step('Bước 3: Hệ thống mở màn Chi tiết phiếu nhập kết quả.')
    d.img('41_import_show', 'Màn hình Chi tiết phiếu nhập kết quả')
    d.step(['Bước 4: Bấm ', '@btn_quaylai', ' để trở về.'])
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
