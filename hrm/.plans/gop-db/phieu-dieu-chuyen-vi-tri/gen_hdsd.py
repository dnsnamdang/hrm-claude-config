# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu điều chuyển vị trí (form chuẩn Danh mục quốc gia, 09/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu dieu chuyen vi tri.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (pdcvt_shots/uml/overview.png).
Khuôn cấu trúc: ../phieu-xuat-kho-dieu-chinh-kiem-ke/gen_hdsd.py.
Ảnh + icon: pdcvt_shots (dev-hrm 09/11/2026, _capture/capture.js, chặn mọi yêu cầu ghi — 0 yêu cầu ghi; POST In dự kiến cho qua vì
chỉ dựng bản in). Ảnh 10c_filled / 10f / 10e / 18b dùng danh sách Kho GIẢ trên trình duyệt (DNS Admin trên dev không là thủ kho kho
nào). Icon menu Kiểm kho / Theo vị trí / Kiểm kê theo vị trí / Kiểm kê theo hàng hóa chép từ ../kiem-ke-theo-vi-tri/kkvt_shots/icons
và ../kiem-ke-theo-hang-hoa/kkhh_shots/icons (ảnh cắt thật trên dev).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu điều chuyển vị trí'
SHOTS = os.path.join(HERE, 'pdcvt_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu dieu chuyen vi tri.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pdcvt')

THUAT_NGU = [
    ['Phiếu điều chuyển vị trí', 'Chứng từ PĐCVT-NNNNN chuyển hàng giữa các vị trí trong cùng 1 kho, theo lô.'],
    ['Vị trí xuất / Vị trí nhập', 'Vị trí lấy hàng ra (còn tồn hàng đó) / vị trí đặt hàng vào; hai vị trí phải khác nhau.'],
    ['Lô xuất', 'Lô nhập kho của hàng tại vị trí xuất; hàng được chuyển giữ nguyên lô.'],
    ['SL tồn', 'Tồn của lô tại vị trí xuất theo ĐVT của dòng; chữ đỏ khi SL nhập lớn hơn.'],
    ['Đang tạo', 'Trạng thái (nhãn xám): phiếu lưu nháp, chưa đổi tồn; sửa, xóa được.'],
    ['Đã chuyển', 'Trạng thái (nhãn xanh lá): đã điều chuyển, tồn đã ghi; chỉ xem, in.'],
    ['In dự kiến', 'Bản in xem trước theo dữ liệu đang nhập trên form, chưa cần lưu.'],
]
PHIEN_BAN = [['1.0', '09/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, chi tiết, in, xuất Excel, xem lịch sử',
     'Xem điều chuyển vị trí theo tổng công ty / theo công ty / theo kho. Không có quyền nào thì chỉ thấy phiếu mình tạo.'],
    ['Tạo mới phiếu', 'Điều chuyển vị trí (và là thủ kho của kho lập phiếu).'],
    ['Sửa, Xóa, Điều chuyển phiếu Đang tạo', 'Người xem được phiếu đó.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.truy_cap([('Kho', 'menu_phanhe'), ('Điều chuyển', 'menu_nhom'), ('Phiếu điều chuyển vị trí', 'menu_muc')],
               'mã phiếu', bo_loc=[('Trạng thái', 'o_trangthai'), ('Kho', 'o_kho'), ('Người tạo', 'o_nguoitao'),
                                   ('Hàng hóa', 'o_hanghoa'), ('Ngày tạo', 'o_ngaytao'), ('Công ty', 'o_congty'),
                                   ('Phòng ban', 'o_phongban')])

    d.phan('THÊM MỚI PHIẾU')
    d.step('Bước 1: Truy cập vào màn hình Phiếu điều chuyển vị trí (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.sub(['Hoặc từ phân hệ Kho ', '@menu_phanhe', ', nhóm Kiểm kho ', '@kkvt_menu_nhom', ', Theo vị trí ', '@kkvt_menu_nhom2',
           ', chọn Kiểm kê theo vị trí ', '@kkvt_menu_muc', ', bấm ', '@kkvt_btn_taodc_row', ' ở dòng phiếu kiểm kê (hoặc ',
           '@btn_taodieuchuyen', ' ở màn chi tiết phiếu kiểm kê). Kho và các dòng được điền sẵn, chỉ chọn Vị trí nhập.'])
    d.sub(['Hoặc ở Kiểm kê theo hàng hóa ', '@kkhh_menu_muc', ', mở phiếu kiểm kê rồi bấm Tạo phiếu điều chuyển vị trí.'])
    d.step(['Bước 3: Chọn Kho ', '@o_kho', ', nhập Ghi chú ', '@o_ghichu', ', bấm ', '@btn_themtailieu', ' để đính kèm file (pdf, png, '
            'jpg, jpeg).'])
    d.step(['Bước 4: Bấm ', '@btn_themhanghoa', ', chọn hàng cần chuyển rồi bấm Thêm.'])
    d.step(['Bước 5: Ở từng dòng chọn Vị trí xuất ', '@o_vitrixuat', ', Lô xuất ', '@o_loxuat', ', Vị trí nhập ', '@o_vitrinhap',
            ' và nhập SL ', '@o_sl', '.'])
    d.img('10c_filled', 'Màn hình Tạo phiếu điều chuyển vị trí')
    d.sub(['Trường bắt buộc khi Lưu nháp: Kho. Khi Điều chuyển: Kho, Ghi chú, File đính kèm; ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, '
           'SL của từng dòng.'])
    d.step(['Bước 6: Bấm ', '@btn_luunhap', ' để lưu và về danh sách'])
    d.sub(['Hoặc bấm ', '@btn_luutieptuc', ' để lưu và lập phiếu tiếp'])
    d.sub(['Hoặc bấm ', '@btn_dieuchuyen', ' để điều chuyển ngay (PHẦN 4)'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ', chọn ', '@btn_thoat', ' để không lưu hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('CHỈNH SỬA PHIẾU')
    d.step('Bước 1: Truy cập vào màn hình Phiếu điều chuyển vị trí, tìm phiếu Đang tạo.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_sua'])
    d.img('12_edit', 'Màn hình Sửa phiếu điều chuyển vị trí')
    d.step(['Bước 3: Sửa Ghi chú ', '@o_ghichu', ', thêm hàng bằng ', '@btn_themhanghoa', ', sửa vị trí / lô / SL của dòng.'])
    d.step(['Bước 4: Bấm ', '@btn_luunhap', ' để lưu'])
    d.sub(['Hoặc bấm ', '@btn_dieuchuyen', ' để điều chuyển (PHẦN 4)'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ' để không lưu.'])

    d.phan('ĐIỀU CHUYỂN')
    d.step('Bước 1: Mở màn Tạo mới (PHẦN 2) hoặc Sửa (PHẦN 3), nhập đủ thông tin bắt buộc khi Điều chuyển.')
    d.step(['Bước 2: Bấm ', '@btn_dieuchuyen', '. Hệ thống hiện hộp Xác nhận điều chuyển.'])
    d.img('10f_confirm_transfer', 'Hộp Xác nhận điều chuyển')
    d.step(['Bước 3: Bấm ', '@btn_dieuchuyen_confirm', ' để điều chuyển'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm2', ' để không điều chuyển.'])

    d.xoa('Xác nhận xóa', doi_tuong='phiếu', them_cach=['Hoặc tại màn chi tiết phiếu Đang tạo, bấm ', '@btn_xoa'])

    d.phan('IN DỰ KIẾN')
    d.step('Bước 1: Mở màn Tạo mới hoặc Sửa, nhập Kho, Ghi chú và ĐVT, Vị trí xuất, Lô xuất của từng dòng.')
    d.step(['Bước 2: Bấm ', '@btn_indukien', '. Hệ thống mở cửa sổ xem trước bản dự kiến.'])
    d.img('18b_print_expect', 'Cửa sổ Xem trước phiếu dự kiến điều chuyển vị trí')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

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
    d.step('Bước 1: Truy cập vào màn hình Phiếu điều chuyển vị trí.')
    d.step(['Bước 2: Bấm vào Mã phiếu ', '@link_sophieu', '. Hệ thống mở màn Chi tiết phiếu.'])
    d.sub(['Bấm mã phiếu kiểm kê ', '@link_pkk_detail', ' để mở phiếu kiểm kê.'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu điều chuyển vị trí')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở dòng phiếu Đã chuyển, cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu điều chuyển vị trí')
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
