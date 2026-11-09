# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu xuất kho điều chỉnh kiểm kê (form chuẩn Danh mục quốc gia, 09/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu xuat kho dieu chinh kiem ke.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (pxkdckk_shots/uml/overview.png).
Khuôn cấu trúc: ../phieu-xuat-dieu-chinh-sai-so-lieu/gen_hdsd.py.
Ảnh + icon: pxkdckk_shots (dev-hrm 09/11/2026, _capture/capture.js, chặn mọi yêu cầu ghi — 0 yêu cầu ghi). Ảnh 12_edit /
12b_confirm_send là GIẢ trạng thái Đang tạo trên trình duyệt (dev không có phiếu Đang tạo). Icon menu Kiểm kho / Theo vị trí /
Kiểm kê theo hàng hóa và nút Thêm tài liệu chép từ ../kiem-ke-theo-hang-hoa/kkhh_shots/icons (ảnh cắt thật trên dev).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu xuất kho điều chỉnh kiểm kê'
SHOTS = os.path.join(HERE, 'pxkdckk_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu xuat kho dieu chinh kiem ke.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pxkdckk')

THUAT_NGU = [
    ['Phiếu xuất kho điều chỉnh kiểm kê', 'Chứng từ PXKĐCKK-NNNNN xuất khỏi kho phần hàng thiếu phát hiện khi kiểm kê, theo '
                                          'từng kho của phiếu kiểm kê.'],
    ['Phiếu kiểm kê', 'Phiếu ở màn Kiểm kê theo hàng hóa; mỗi phiếu kiểm kê chỉ lập 1 phiếu xuất kho điều chỉnh.'],
    ['Hàng thiếu', 'Dòng kiểm kê có số đếm thực tế ít hơn sổ sách, chưa được xử lý.'],
    ['Đang tạo', 'Trạng thái (nhãn xám): phiếu lưu nháp, sửa được.'],
    ['Chờ duyệt', 'Trạng thái (nhãn vàng): đã gửi duyệt, đã trừ tồn kho, chờ Kế toán kho.'],
    ['Đang hạch toán', 'Trạng thái (nhãn xanh dương): Kế toán kho đã lưu phiếu xuất hàng ở dạng nháp.'],
    ['Đã hạch toán', 'Trạng thái (nhãn xanh lá): phiếu xuất hàng đã lưu và duyệt.'],
]
PHIEN_BAN = [['1.0', '09/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, chi tiết, in, xuất Excel, xem lịch sử',
     'Xem phiếu xuất kho điều chỉnh kiểm kê - theo tổng công ty / - theo công ty. Không có quyền nào thì chỉ thấy phiếu mình '
     'tạo. Kế toán kho thấy thêm mọi phiếu Chờ duyệt.'],
    ['Tạo mới phiếu', 'Xử lý phiếu kiểm kê hàng hóa.'],
    ['Sửa, Gửi duyệt phiếu Đang tạo', 'Người tạo phiếu.'],
    ['Tạo phiếu xuất hàng', 'Kế toán kho.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.truy_cap([('Kho', 'menu_phanhe'), ('Xuất kho', 'menu_nhom'), ('Phiếu xuất kho điều chỉnh kiểm kê', 'menu_muc')],
               'số phiếu', bo_loc=[('Mã phiếu', 'o_maphieu'), ('Kho', 'o_kho'), ('Trạng thái', 'o_trangthai'),
                                    ('Người tạo', 'o_nguoitao'), ('Mã hàng hóa', 'o_mahang'), ('Tên hàng hóa', 'o_tenhang'),
                                    ('Ngày tạo', 'o_ngaytao'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban')])

    d.phan('THÊM MỚI PHIẾU')
    d.step('Bước 1: Truy cập vào màn hình Phiếu xuất kho điều chỉnh kiểm kê (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.sub(['Hoặc từ phân hệ Kho ', '@menu_phanhe', ', nhóm Kiểm kho ', '@menu_nhom_kk', ', Theo vị trí ', '@menu_nhom2_kk',
           ', chọn Kiểm kê theo hàng hóa ', '@menu_muc_kk', ', mở phiếu kiểm kê rồi bấm ', '@btn_xuatdc'])
    d.step(['Bước 3: Chọn phiếu kiểm kê ', '@o_phieukiemke', '. Hệ thống điền Kho và nạp hàng thiếu.'])
    d.img('10c_filled', 'Màn hình Tạo phiếu xuất kho điều chỉnh kiểm kê')
    d.step(['Bước 4: Đổi kho ', '@o_kho', ' nếu cần (chỉ các kho của phiếu kiểm kê).'])
    d.step(['Bước 5: Nhập Ghi chú ', '@o_ghichu', ', bấm ', '@btn_themtailieu', ' để đính kèm file (pdf, png, jpg, jpeg).'])
    d.step(['Bước 6: Bấm ', '@btn_luunhap', ' để lưu và về danh sách'])
    d.sub(['Hoặc bấm ', '@btn_luutieptuc', ' để lưu và lập phiếu tiếp'])
    d.sub(['Hoặc bấm ', '@btn_guiduyet', ' để gửi duyệt (PHẦN 4)'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ', chọn ', '@btn_thoat', ' để không lưu hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('CHỈNH SỬA PHIẾU')
    d.step('Bước 1: Truy cập vào màn hình Phiếu xuất kho điều chỉnh kiểm kê, tìm phiếu Đang tạo do mình tạo.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_sua'])
    d.img('12_edit', 'Màn hình Sửa phiếu xuất kho điều chỉnh kiểm kê')
    d.step(['Bước 3: Sửa Ghi chú ', '@o_ghichu', ', thêm file bằng ', '@btn_themtailieu', '.'])
    d.step(['Bước 4: Bấm ', '@btn_luunhap', ' để lưu'])
    d.sub(['Hoặc bấm ', '@btn_guiduyet', ' để gửi duyệt (PHẦN 4)'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ' để không lưu.'])

    d.phan('GỬI DUYỆT PHIẾU')
    d.step('Bước 1: Mở màn Tạo mới (PHẦN 2) hoặc Sửa (PHẦN 3), nhập đủ Phiếu kiểm kê, Ghi chú và File đính kèm.')
    d.step(['Bước 2: Bấm ', '@btn_guiduyet', '. Hệ thống hiện hộp Xác nhận gửi duyệt.'])
    d.img('12b_confirm_send', 'Hộp Xác nhận gửi duyệt')
    d.step(['Bước 3: Bấm ', '@btn_guiduyet_confirm', ' để gửi duyệt'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' để không gửi.'])

    d.phan('TẠO PHIẾU XUẤT HÀNG')
    d.step('Bước 1: Truy cập vào màn hình Phiếu xuất kho điều chỉnh kiểm kê, tìm phiếu Chờ duyệt.')
    d.step(['Bước 2: Bấm ', '@btn_taophieuxuathang_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_taophieuxuathang'])
    d.img('23_product_export', 'Màn hình Tạo phiếu xuất hàng điều chỉnh kiểm kê')
    d.step('Bước 3: Nhập thông tin phiếu xuất hàng, bấm Lưu hoặc Lưu và duyệt (theo HDSD màn Phiếu xuất hàng điều chỉnh kiểm kê).')

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
    d.step('Bước 1: Truy cập vào màn hình Phiếu xuất kho điều chỉnh kiểm kê.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn Chi tiết phiếu.'])
    d.sub(['Bấm mã phiếu kiểm kê ', '@link_pkk_detail', ' để mở phiếu kiểm kê.'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu xuất kho điều chỉnh kiểm kê')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu xuất kho điều chỉnh kiểm kê')
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
