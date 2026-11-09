# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Tổng hợp xuất nhập tồn (phân hệ Kho › Báo cáo kho), form chuẩn, 09/11/2026.

Chạy: python gen_hdsd.py  → HDSD_Tong hop xuat nhap ton.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (chạy gen_srs.py trước).
Khuôn: ../bao-cao-ton-kho-tong-hop-mat-hang/gen_hdsd.py (07/11).
Ảnh + icon: thxnt_shots (dev-hrm 09/11/2026, DNS Admin, _capture/capture.js chặn mọi yêu cầu ghi — 0). Ảnh Chọn hàng hóa chụp với
công ty TPE (công ty CN Hải Phòng dev báo lỗi 403 khi tải danh sách hàng).
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

TEN = 'Tổng hợp xuất nhập tồn'
SHOTS = os.path.join(HERE, 'thxnt_shots')
OUT = os.path.join(HERE, 'HDSD_Tong hop xuat nhap ton.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_thxnt')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Kỳ', 'Khoảng thời gian báo cáo: Tuần này, Tháng này, Năm nay (mặc định), Năm trước, Tuỳ chọn.'],
    ['Tồn đầu kỳ / Tồn cuối kỳ', 'Số lượng còn ngay trước ngày đầu kỳ / tại hết ngày cuối kỳ.'],
    ['Nhập / Xuất trong kỳ', 'Tổng số lượng tăng / giảm tại các vị trí đang xem trong kỳ.'],
    ['Không nhặt phiếu điều chuyển', 'Loại báo cáo bỏ các lần chuyển hàng giữa 2 vị trí khỏi số liệu.'],
    ['Công ty thuê kho', 'Công ty có kho kế toán gắn với kho; tồn ghi nhận theo từng công ty này.'],
    ['Đầy đủ / Ngắn gọn', 'Kiểu in và xuất Excel: có / không có cột Model và Thương hiệu.'],
]
PHIEN_BAN = [['1.0', '09/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Mọi chức năng (xem, lọc, lọc vị trí, cài đặt bộ lọc, chọn hàng, đổi ĐVT, in, xuất Excel)',
     'Có 1 trong 3 quyền: Xem báo cáo tồn kho theo tổng công ty / theo công ty / theo kho.'],
    ['Xem mọi công ty, mọi kho', 'Xem báo cáo tồn kho theo tổng công ty.'],
    ['Xem kho của công ty mình', 'Xem báo cáo tồn kho theo công ty.'],
    ['Xem kho mình là thủ kho', 'Xem báo cáo tồn kho theo kho.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Kho ', '@menu_phanhe', ', tại menu Báo cáo kho ', '@menu_nhom', ', chọn ', '@menu_muc',
            '. Báo cáo tự hiện theo công ty của bạn, toàn bộ kho, kỳ Năm nay.'])
    d.step(['Bước 2: Chọn kỳ ở ', '@o_ky', ' (mặc định Năm nay)'])
    d.sub(['Chọn Tuỳ chọn thì chọn Từ ngày – Đến ngày ở ', '@o_thoigian', ' (bắt buộc đủ 2 ngày)'])
    d.step(['Bước 3: Chọn ', '@o_loaibc', ' (Tất cả hoặc Không nhặt phiếu điều chuyển)'])
    d.step(['Bước 4: Chọn công ty ở ', '@o_congty', ' (hệ thống tự chọn hết kho của công ty)'])
    d.step(['Bước 5: Bỏ / thêm kho ở ', '@o_kho', ' (bắt buộc ít nhất 1 kho)'])
    d.sub(['Hoặc bỏ tích ', '@o_toanbokho', ' để xóa hết kho rồi tự chọn; tích lại để chọn hết kho'])
    d.step(['Bước 6: Chọn công ty ở ', '@o_congtythue', ' (hệ thống tích sẵn mọi công ty thuê của các kho)'])
    d.step(['Bước 7: Chọn thêm giá trị trong ', '@o_tinhchat', ' để lọc theo Tính chất hàng hóa'])
    for lb, ic in [('Loại hàng hóa', 'o_loai'), ('Thương hiệu', 'o_thuonghieu'), ('Hãng sản xuất', 'o_hangsx'),
                   ('Nhóm hàng hóa', 'o_nhom')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 8: Nhấn ', '@btn_timkiem'])
    d.img('03_detail', 'Màn hình Tổng hợp xuất nhập tồn')
    d.step(['Bước 9: Chọn ', '@btn_xoaloc', ' để về bộ lọc mặc định'])
    d.sub(['Hoặc bấm ', '@btn_timkiemnangcao', ' để thu gọn / mở khối lọc'])
    d.step(['Bước 10: Chọn số dòng ở ', '@o_sodong', ' hoặc bấm số trang ở ', '@o_phantrang', ' để xem trang khác'])
    d.step(['Bước 11: Bấm ', '@btn_thugon', ' để thu gọn / mở khối tổng hợp'])

    d.phan('LỌC THEO NHÀ / DÃY / KHOANG / VỊ TRÍ')
    d.step('Bước 1: Truy cập vào màn hình Tổng hợp xuất nhập tồn, chọn kho (PHẦN 1).')
    d.step(['Bước 2: Tại ', '@o_nha', ' tích Nhà cần xem; cột Dãy hiện các dãy của nhà đã tích'])
    d.step('Bước 3: Lần lượt tích Dãy, Khoang, rồi Vị trí cần xem (hoặc tích Vị trí tự do của kho).')
    d.img('02h_scope_full', 'Lọc theo Nhà / Dãy / Khoang / Vị trí')
    d.step('Bước 4: Chỉ khi có tích ít nhất 1 Vị trí báo cáo mới thu hẹp; khi đó kho không tích gì bị bỏ khỏi số liệu.')

    d.phan('CHỌN HÀNG HÓA')
    d.step('Bước 1: Truy cập vào màn hình Tổng hợp xuất nhập tồn (PHẦN 1).')
    d.step(['Bước 2: Bấm vào ô ', '@o_hanghoa', '. Hệ thống mở cửa sổ “Chọn hàng hóa”.'])
    d.img('04b_picker_tpe', 'Cửa sổ Chọn hàng hóa')
    d.step('Bước 3: Gõ mã / tên hàng vào ô tìm kiếm của cửa sổ, bấm vào tên hàng cần xem.')
    d.sub(['Hoặc bấm ', '@btn_dong_picker', ' để không chọn'])
    d.step(['Bước 4: Bấm ', '@btn_xoahang', ' trên ô Hàng hóa để bỏ hàng đã chọn'])

    d.phan('ĐỔI ĐƠN VỊ TÍNH')
    d.step('Bước 1: Truy cập vào màn hình Tổng hợp xuất nhập tồn (PHẦN 1).')
    d.step(['Bước 2: Ở dòng mặt hàng có nhiều ĐVT, bấm ', '@o_dvt', ' và chọn ĐVT khác'])
    d.img('03d_unit_after', 'Số lượng quy đổi theo ĐVT đã chọn')
    d.step('Bước 3: Cả 4 cột Tồn đầu kỳ, Nhập, Xuất, Tồn cuối kỳ của hàng đổi theo ĐVT mới; In / Xuất Excel dùng ĐVT này.')

    d.phan('XUẤT EXCEL')
    d.step('Bước 1: Lọc báo cáo theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Xuất Excel tổng hợp xuất nhập tồn”.'])
    d.img('06_export', 'Cửa sổ Xuất Excel')
    d.step('Bước 3: Chọn kiểu xuất Đầy đủ hoặc Ngắn gọn.')
    d.step(['Bước 4: Bấm ', '@btn_xuatexcel_popup', '. Hệ thống tải file bao_cao_tong_hop_xuat_nhap_ton_kho.xlsx.'])
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
    d.step(['Bước 1: Ở khối Bộ lọc tổng hợp xuất nhập tồn, bấm ', '@btn_caidatboloc'])
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
