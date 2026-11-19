# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Báo cáo tồn kho chi tiết theo mặt hàng (phân hệ Kho › Báo cáo kho), form chuẩn, 06/11/2026.

Chạy: python gen_hdsd.py  → HDSD_Bao cao ton kho chi tiet theo mat hang.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (chạy gen_srs.py trước).
Khuôn: ../report-limit-debts/gen_hdsd.py (màn báo cáo) + ../kiem-ke-theo-hang-hoa/gen_hdsd.py.
Ảnh + icon: bctkct_shots (dev-hrm 06/11/2026, DNS Admin, _capture/capture.js chặn mọi yêu cầu ghi — 0). Ảnh Chọn hàng hóa chụp với
công ty TPE (công ty CN Hải Phòng dev báo lỗi tải danh sách hàng).
"""
import os
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Báo cáo tồn kho chi tiết theo mặt hàng'
SHOTS = os.path.join(HERE, 'bctkct_shots')
OUT = os.path.join(HERE, 'HDSD_Bao cao ton kho chi tiet theo mat hang.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_bctkct')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Tính đến ngày', 'Ngày chốt số liệu; tồn được cộng tới hết ngày này.'],
    ['Công ty thuê kho', 'Công ty có kho kế toán gắn với kho; tồn ghi nhận theo từng công ty này.'],
    ['Lô / Vị trí', 'Lô hàng sinh ra khi nhập kho / ô chứa hàng trong kho.'],
    ['SL tồn', 'Số lượng còn trong kho, theo ĐVT đang chọn của từng mặt hàng.'],
    ['Cấp bung', 'Mức hiển thị sẵn của bảng: Chỉ hàng hóa, Đến công ty thuê kho, Đến lô, Tất cả cấp.'],
    ['Đầy đủ / Ngắn gọn', 'Kiểu in và xuất Excel: có / không có khối Chi tiết (Công ty, Lô, Vị trí, SL, Cộng).'],
]
PHIEN_BAN = [['1.0', '06/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Mọi chức năng (xem, lọc, cài đặt bộ lọc, chọn hàng, xem chi tiết, in, xuất Excel)',
     'Có 1 trong 3 quyền: Xem báo cáo tồn kho theo tổng công ty / theo công ty / theo kho.'],
    ['Xem mọi công ty, mọi kho', 'Xem báo cáo tồn kho theo tổng công ty.'],
    ['Xem kho của công ty mình', 'Xem báo cáo tồn kho theo công ty.'],
    ['Xem kho mình là thủ kho', 'Xem báo cáo tồn kho theo kho.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Kho ', '@menu_phanhe', ', tại menu Báo cáo kho ', '@menu_nhom', ', chọn ', '@menu_muc'])
    d.step(['Bước 2: Chọn ngày ở ', '@o_ngay', ' (mặc định hôm nay)'])
    d.step(['Bước 3: Chọn công ty ở ', '@o_congty', ', rồi chọn kho ở ', '@o_kho',
            ' (bắt buộc; hệ thống tự tích các công ty ở ', '@o_congtythue', ')'])
    d.step(['Bước 4: Chọn thêm giá trị trong ', '@o_nhom', ' để lọc theo Nhóm hàng hóa'])
    for lb, ic in [('Tính chất hàng hóa', 'o_tinhchat'), ('Loại hàng hóa', 'o_loai'), ('Thương hiệu', 'o_thuonghieu'),
                   ('Hãng sản xuất', 'o_hangsx')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.sub(['Hoặc gõ mã hợp đồng vào ', '@o_hopdong', ' rồi nhấn Enter'])
    d.step(['Bước 5: Nhấn ', '@btn_timkiem'])
    d.img('01_list', 'Màn hình Báo cáo tồn kho chi tiết theo mặt hàng')
    d.step(['Bước 6: Chọn ', '@btn_xoaloc', ' để xóa giá trị đã lọc'])
    d.sub(['Hoặc bấm ', '@btn_timkiemnangcao', ' để thu gọn / mở khối lọc'])

    d.phan('CHỌN HÀNG HÓA')
    d.step('Bước 1: Truy cập vào màn hình Báo cáo tồn kho chi tiết theo mặt hàng (PHẦN 1).')
    d.step(['Bước 2: Bấm vào ô ', '@o_hanghoa', '. Hệ thống mở cửa sổ “Chọn hàng hóa”.'])
    d.img('04b_picker_tpe', 'Cửa sổ Chọn hàng hóa')
    d.step('Bước 3: Gõ mã / tên hàng vào ô tìm kiếm của cửa sổ, bấm vào tên hàng cần xem.')
    d.sub(['Hoặc bấm ', '@btn_dong_picker', ' để không chọn'])
    d.step(['Bước 4: Bấm ', '@btn_xoahang', ' trên ô Hàng hóa để bỏ hàng đã chọn'])

    d.phan('XEM CHI TIẾT THEO CÔNG TY THUÊ KHO – LÔ – VỊ TRÍ')
    d.step('Bước 1: Truy cập vào màn hình Báo cáo tồn kho chi tiết theo mặt hàng (PHẦN 1).')
    d.step(['Bước 2: Chọn cấp hiển thị ở ', '@o_capbung', ' (Chỉ hàng hóa / Đến công ty thuê kho / Đến lô / Tất cả cấp)'])
    d.img('03_detail', 'Bảng bung tới vị trí của một mặt hàng')
    d.step(['Bước 3: Bấm ', '@btn_caret', ' ở đầu dòng để bung / thu riêng dòng đó'])
    d.step(['Bước 4: Chọn ĐVT ở ', '@o_dvt', ' trên dòng mặt hàng để xem số lượng quy đổi'])
    d.step(['Bước 5: Bấm mã hợp đồng ', '@link_hopdong', ' ở dòng lô để mở hợp đồng ở tab mới'])
    d.step(['Bước 6: Chọn số dòng ở ', '@o_sodong', ' hoặc bấm số trang để xem trang khác'])

    d.phan('XUẤT EXCEL')
    d.step('Bước 1: Lọc báo cáo theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Xuất Excel báo cáo tồn kho chi tiết theo mặt hàng”.'])
    d.img('06_export', 'Cửa sổ Xuất Excel')
    d.step('Bước 3: Chọn kiểu xuất Đầy đủ hoặc Ngắn gọn.')
    d.step(['Bước 4: Bấm ', '@btn_xuatexcel_popup', '. Hệ thống tải file bao_cao_ton_kho_chi_tiet_mat_hang.xlsx.'])
    d.sub(['Hoặc bấm ', '@btn_huy_export', ' để không xuất'])

    d.phan('IN BÁO CÁO')
    d.step('Bước 1: Lọc báo cáo theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_inds', '. Hệ thống mở cửa sổ “In báo cáo”.'])
    d.img('05_print', 'Cửa sổ In báo cáo')
    d.step('Bước 3: Chọn kiểu in Đầy đủ hoặc Ngắn gọn, tích / bỏ tích các cột cần in.')
    d.step(['Bước 4: Bấm ', '@btn_in_popup', '. Hệ thống mở cửa sổ xem trước bản in.'])
    d.sub(['Hoặc bấm ', '@btn_huy_print', ' để không in'])
    d.step(['Bước 5: Bấm ', '@btn_in_preview', ' để in'])
    d.sub(['Hoặc bấm ', '@btn_dong_preview', ' để đóng bản xem trước'])

    d.phan('CÀI ĐẶT BỘ LỌC')
    d.step(['Bước 1: Ở khối Bộ lọc báo cáo tồn kho, bấm ', '@btn_caidatboloc'])
    d.img('07_filtercfg', 'Cửa sổ Cài đặt bộ lọc')
    d.step('Bước 2: Tích để hiện, bỏ tích để ẩn ô lọc; kéo để đổi thứ tự.')
    d.step(['Bước 3: Bấm ', '@btn_luu_cfg', ' để áp dụng'])
    d.sub(['Hoặc bấm ', '@btn_khoiphuc', ' để trả về cấu hình ban đầu'])
    d.sub(['Hoặc bấm ', '@btn_dong_filtercfg', ' nếu muốn bỏ thay đổi.'])
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
