# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu giao việc (lối vào ?type=all, form chuẩn Danh mục quốc gia, 19/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu giao viec.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (pgv_shots/uml/overview.png).
Khuôn cấu trúc: gen_hdsd_duoc_giao.py (bộ "Phiếu giao việc được giao" — không sửa / không chạy lại).
Ảnh + icon: pgv_shots (dev-hrm 19/11/2026, _capture/capture.js, chặn mọi yêu cầu ghi — 0 yêu cầu ghi). Ảnh 41_create_hd là form Tạo với dữ
liệu nguồn GIẢ trên trình duyệt (chi tiết phiếu thật cùng loại) vì DNS Admin không thuộc phòng tiếp nhận; nút Xóa là phiếu thật đủ điều kiện.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu giao việc'
SHOTS = os.path.join(HERE, 'pgv_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu giao viec.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pgv')

THUAT_NGU = [
    ['Phiếu giao việc', 'Chứng từ giao việc cho kỹ thuật, lập từ 1 chứng từ nguồn còn số lượng chưa giao.'],
    ['Chứng từ nguồn', 'Hợp đồng dịch vụ, phụ lục bổ sung, phiếu bảo hành, phiếu yêu cầu lắp đặt bàn giao, phiếu yêu cầu giao việc khác.'],
    ['SL còn trên hợp đồng', 'Số lượng của chứng từ nguồn chưa giao việc.'],
    ['SL giao lần này', 'Số lượng giao trong phiếu này, không vượt SL còn.'],
    ['Tổng công định mức', 'Công chính + Công phụ của phiếu.'],
    ['Chờ thực hiện', 'Trạng thái (nhãn cam) của phiếu vừa lưu — được Xóa, Nhập kết quả.'],
    ['Đang nhập kết quả / Đã nhập kết quả', 'Trạng thái sau khi lưu nháp / gửi duyệt phiếu nhập kết quả.'],
    ['Đang duyệt kết quả / Đã duyệt kết quả', 'Trạng thái trong và sau khi duyệt kết quả.'],
    ['Chờ BKS duyệt kết quả / Đang đề nghị thanh toán / Đã thanh toán', 'Các bước sau duyệt kết quả.'],
]
PHIEN_BAN = [['1.0', '19/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, tìm kiếm, chi tiết, lịch sử, in, xuất Excel', 'Không cần quyền riêng. Phạm vi theo quyền Xem phiếu giao việc (Tổng '
                                                                    'công ty / Công ty / Phòng ban); không có quyền thì phiếu bạn tạo hoặc '
                                                                    'bạn thực hiện.'],
    ['Tạo phiếu giao việc', 'Thuộc phòng tiếp nhận của chứng từ; từ hợp đồng / phụ lục / phiếu bảo hành cần thêm quyền Tạo phiếu giao việc.'],
    ['Xóa', 'Là người tạo phiếu; phiếu Chờ thực hiện, chưa gắn Phiếu giao công tác.'],
    ['Nhập kết quả', 'Là người thực hiện; phiếu Chờ thực hiện, Phiếu giao công tác đã duyệt, chưa có phiếu nhập kết quả.'],
    ['Xem phiếu nhập kết quả', 'Phiếu đã có phiếu nhập kết quả.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.truy_cap([('CSKH sau bán', 'menu_phanhe'), ('Giao việc', 'menu_nhom'), ('Phiếu giao việc', 'menu_muc')],
               'số phiếu giao việc',
               bo_loc=[('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Số hợp đồng', 'o_sohd'), ('Số phiếu yêu cầu', 'o_soyc'),
                       ('Khách hàng', 'o_khachhang'), ('Người yêu cầu', 'o_nguoiyeucau'), ('Trạng thái', 'o_trangthai'),
                       ('Người tạo', 'o_nguoitao'), ('Người thực hiện', 'o_nguoithuchien'), ('Thời gian dự kiến', 'o_thoigian')])

    d.phan('TẠO PHIẾU GIAO VIỆC')
    d.step(['Bước 1: Từ phân hệ CSKH sau bán ', '@menu_phanhe', ', tại menu Giao việc ', '@menu_nhom', ', chọn Phiếu chờ giao việc ',
            '@menu_muc_cho'])
    d.step(['Bước 2: Chọn tab của chứng từ (Hợp đồng, PL bổ sung, Phiếu bảo hành ', '@tab_baohanh', ', Lắp đặt bàn giao, Giao việc khác), '
            'ở dòng chứng từ bấm ', '@btn_taopgv_row'])
    d.step('Bước 3: Hệ thống mở màn Tạo phiếu giao việc, điền sẵn thông tin khách hàng và các dòng việc còn số lượng.')
    d.img('41_create_hd', 'Màn hình Tạo phiếu giao việc')
    d.step('Bước 4: Chọn Ngày dự kiến bắt đầu, Ngày dự kiến kết thúc (bắt buộc).')
    d.step('Bước 5: Sửa SL giao lần này nếu không giao hết (không vượt SL còn trên hợp đồng), nhập Ghi chú nếu cần.')
    d.sub('Hoặc nhập Định mức công ở bảng Dịch vụ đính kèm (phiếu từ yêu cầu giao việc khác)')
    d.step(['Bước 6: Nếu có công phụ, bấm ', '@btn_themdong', ', nhập Công phụ tính P3 và ĐM Công (bắt buộc)'])
    d.sub(['Hoặc bấm ', '@btn_xoadong_p3', ' để xóa dòng công phụ'])
    d.step(['Bước 7: Bấm ', '@btn_luuvaduyet', ', rồi bấm ', '@btn_luuvaduyet_confirm', ' để lưu'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm2', ' để quay lại sửa'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_create', ' để không lưu, chọn ', '@btn_thoat', ' hoặc ', '@btn_olai'])

    d.xoa('Xác nhận xóa', doi_tuong='phiếu giao việc',
          them_cach=['Hoặc mở chi tiết phiếu rồi bấm ', '@btn_xoa_detail', ' ở cuối trang'])

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
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in, tối đa 2.000 dòng (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_indanhsach', '. Hệ thống mở cửa sổ “Xem trước danh sách phiếu giao việc”.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách phiếu giao việc')
    d.step(['Bước 3: Bấm ', '@btn_in_popup', ' để in'])
    d.sub(['Hoặc bấm ', '@btn_x_print', ' để đóng.'])

    d.phan('NHẬP KẾT QUẢ')
    d.step(d.vao)
    d.step(['Bước 2: Ở dòng phiếu Chờ thực hiện, tại cột Hành động bấm ', '@btn_nhapkq_row'])
    d.sub(['Hoặc mở chi tiết phiếu rồi bấm ', '@btn_nhapkq_detail'])
    d.step('Bước 3: Hệ thống mở màn Tạo phiếu nhập kết quả với phiếu giao việc đã chọn sẵn.')
    d.img('45_import_create', 'Màn hình Tạo phiếu nhập kết quả')
    d.step('Bước 4: Nhập kết quả thực hiện (theo HDSD Phiếu nhập kết quả).')
    d.step(['Bước 5: Bấm ', '@btn_luu_nkq', ' để lưu nháp'])
    d.sub(['Hoặc bấm ', '@btn_luuguiduyet', ' để gửi duyệt'])
    d.sub(['Hoặc bấm ', '@btn_quaylai', ' để không lưu.'])

    d.phan('XEM PHIẾU NHẬP KẾT QUẢ')
    d.step(d.vao)
    d.step(['Bước 2: Ở dòng phiếu đã nhập kết quả, tại cột Hành động bấm ', '@btn_xemnkq_row'])
    d.sub(['Hoặc mở chi tiết phiếu rồi bấm ', '@btn_xemnkq_detail'])
    d.step('Bước 3: Hệ thống mở màn Chi tiết phiếu nhập kết quả.')
    d.img('46_import_show', 'Màn hình Chi tiết phiếu nhập kết quả')
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
