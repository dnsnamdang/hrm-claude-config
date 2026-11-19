# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Thẻ kho (phân hệ Kho › Báo cáo kho, màn báo cáo chỉ đọc, form chuẩn, 06/11/2026).

Chạy: python gen_hdsd.py  → HDSD_The kho.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (tk_shots/uml/overview.png).
Khuôn cấu trúc: ../kiem-ke-theo-hang-hoa/gen_hdsd.py.
Ảnh + icon: tk_shots (dev-hrm 06/11/2026, _capture/capture.js chặn mọi yêu cầu ghi — 0 yêu cầu ghi). Trạng thái thật, không giả.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Thẻ kho'
SHOTS = os.path.join(HERE, 'tk_shots')
OUT = os.path.join(HERE, 'HDSD_The kho.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_tk')

THUAT_NGU = [
    ['Thẻ kho', 'Báo cáo nhập, xuất, tồn của 1 mặt hàng theo từng chứng từ trong kỳ, tại các kho / vị trí đã chọn của 1 công ty.'],
    ['Chứng từ', 'Phiếu làm thay đổi tồn: phiếu nhập kho, xuất kho, điều chuyển vị trí, nhập lại, xuất điều chỉnh sai số liệu, '
                 'nhập / xuất kho điều chỉnh kiểm kê, khai báo tồn đầu kỳ (“Nhập tồn đầu”).'],
    ['Lô / vị trí', 'Một lô hàng thay đổi tồn tại một vị trí kho; mỗi chứng từ bung ra được các lô / vị trí của nó.'],
    ['Tồn đầu kỳ / Tồn cuối kỳ', 'Tồn trước ngày đầu kỳ / Tồn đầu kỳ + Nhập trong kỳ − Xuất trong kỳ.'],
    ['SL tồn', 'Số tồn lũy kế sau từng chứng từ.'],
    ['Kỳ', 'Tuần này, Tháng này, Năm nay (mặc định), Năm trước, Tuỳ chọn (chọn Từ ngày → Đến ngày).'],
    ['Công ty thuê kho', 'Công ty có kho kế toán gắn với kho đã chọn.'],
    ['Không nhặt điều chuyển', 'Loại báo cáo bỏ các phiếu điều chuyển vị trí.'],
    ['NVKD', 'Người lập yêu cầu của chứng từ - mã phòng ban.'],
]
PHIEN_BAN = [['1.0', '06/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Mở màn, xem thẻ kho, In, Xuất Excel', 'Thủ kho.'],
    ['Chọn công ty khác ở ô Tồn theo công ty', 'Xem báo cáo tồn kho theo tổng công ty (không có: chỉ công ty mình).'],
    ['Cài đặt bộ lọc', 'Không cần quyền riêng.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS, icon_dirs=[os.path.join(SHOTS, 'icons')])
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Kho ', '@menu_phanhe', ', tại menu Báo cáo kho ', '@menu_nhom', ', chọn Thẻ kho ', '@menu_muc'])
    d.img('07_filter_kho', 'Khối Bộ lọc thẻ kho')
    d.step(['Bước 2: Chọn Kỳ ', '@o_ky', ' (mặc định Năm nay)'])
    d.sub(['Hoặc chọn Tuỳ chọn rồi chọn Từ ngày → Đến ngày ở ô ', '@o_thoigian'])
    d.step(['Bước 3: Bấm ô Hàng hóa ', '@o_hanghoa', ' để chọn hàng (xem PHẦN 2)'])
    d.step(['Bước 4: Kiểm tra Tồn theo công ty ', '@o_congty', ' (bắt buộc)'])
    d.step(['Bước 5: Chọn Kho ', '@o_kho', ' nếu cần xem riêng kho; Công ty thuê kho ', '@o_congtythue', ' tự chọn hết'])
    d.sub(['Hoặc tick Nhà / Dãy / Khoang / Vị trí ', '@o_scope', ' để xem riêng vị trí'])
    d.sub(['Hoặc chọn Loại báo cáo ', '@o_loaibc', ' = Không nhặt điều chuyển để bỏ phiếu điều chuyển vị trí'])
    d.step(['Bước 6: Nhập Số chứng từ / Diễn giải ', '@o_sochungtu', ' rồi nhấn ', '@btn_timkiem'])
    d.step(['Bước 7: Chọn ', '@btn_xoaloc', ' để xóa giá trị đã lọc'])
    d.sub(['Hoặc bấm ', '@btn_antimkiem', ' để thu gọn khối bộ lọc, bấm ', '@btn_timkiemnangcao', ' để mở lại'])

    d.phan('CHỌN HÀNG HÓA')
    d.step(['Bước 1: Bấm vào ô Hàng hóa ', '@o_hanghoa'])
    d.step(['Bước 2: Nhập mã / tên hàng vào ô tìm ', '@o_timhang_picker', ' rồi nhấn Enter'])
    d.img('03b_picker_search', 'Cửa sổ Chọn hàng hóa')
    d.step(['Bước 3: Bấm vào tên hàng ', '@link_tenhang_picker', '. Hệ thống đóng cửa sổ và hiện thẻ kho của hàng'])
    d.sub(['Hoặc bấm ', '@btn_dong_picker', ' để đóng không chọn'])

    d.phan('XEM THẺ KHO')
    d.step('Bước 1: Chọn đủ Kỳ, Hàng hóa, Tồn theo công ty (PHẦN 1).')
    d.step('Bước 2: Xem khối Số lượng (Tồn đầu kỳ, Nhập, Xuất, Tồn cuối kỳ) và khối Chứng từ.')
    d.img('02_main', 'Màn hình Thẻ kho')
    d.step(['Bước 3: Bấm ', '@btn_thugon', ' để thu gọn khối tổng hợp'])
    d.step(['Bước 4: Chọn số dòng / trang, chuyển trang ở ', '@phantrang'])

    d.phan('XEM CHI TIẾT CHỨNG TỪ VÀ LÔ / VỊ TRÍ')
    d.step(['Bước 1: Bấm mũi tên ', '@btn_caret', ' ở dòng chứng từ để hiện các lô / vị trí'])
    d.sub(['Hoặc chọn ', '@o_capbung', ' = Tất cả cấp (đến Lô / vị trí) để bung cả trang'])
    d.img('06_transfer', 'Chứng từ điều chuyển vị trí bung lô / vị trí')
    d.step(['Bước 2: Bấm Số chứng từ ', '@link_sochungtu', ' để mở chứng từ ở tab mới'])

    d.phan('IN THẺ KHO')
    d.step(['Bước 1: Bấm ', '@btn_in_list'])
    d.img('09_print_modal', 'Cửa sổ In báo cáo')
    d.step(['Bước 2: Chọn Đầy đủ hoặc ', '@radio_rutgon', ', tích các cột cần in'])
    d.step(['Bước 3: Bấm ', '@btn_in_modal', ' để xem trước'])
    d.sub(['Hoặc bấm ', '@btn_huy_print', ' để không in'])
    d.step(['Bước 4: Ở cửa sổ xem trước, bấm ', '@btn_in_preview', ' để in'])

    d.phan('XUẤT EXCEL')
    d.step('Bước 1: Lọc thẻ kho theo dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel'])
    d.img('11_export', 'Cửa sổ Xuất Excel thẻ kho')
    d.step('Bước 3: Chọn Kiểu xuất Đầy đủ hoặc Rút gọn.')
    d.step(['Bước 4: Bấm ', '@btn_xuat_modal'])
    d.sub(['Hoặc bấm ', '@btn_huy_xuat', ' để không xuất'])
    d.step('Bước 5: Mở file Excel đã tải về.')

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
