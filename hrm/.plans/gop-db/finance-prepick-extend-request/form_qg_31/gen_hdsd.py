# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Yêu cầu gia hạn hàng giữ (STT 31, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Yêu cầu gia hạn hàng giữ.docx (+ .pdf, render/ để soát)
Ảnh: hdsd_shots/ (capture.js, chụp trên dev-hrm). Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Yêu cầu gia hạn hàng giữ'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên kinh doanh đứng tên giữ.'],
    ['Lô hàng giữ', 'Một dòng hàng giữ cụ thể, gồm: người giữ – khách hàng – hàng hóa – hạn giữ – công ty. Mỗi lô có '
                    'hạn giữ riêng.'],
    ['Hạn giữ', 'Ngày cuối cùng lô hàng còn được giữ. Quá ngày này lô bị coi là hết hạn giữ.'],
    ['Hạn giữ mới', 'Ngày mà người lập đề nghị gia hạn tới.'],
    ['Gia hạn hàng giữ', 'Kéo dài thời gian giữ hàng cho khách. Khi phiếu được duyệt xong, phần mềm chuyển số lượng xin '
                         'gia hạn sang hạn giữ mới.'],
    ['Số ngày cảnh báo', 'Cấu hình chung, hiện là 7 ngày. Chỉ những lô sắp hết hạn trong khoảng này mới hiện ra để lập '
                         'phiếu gia hạn.'],
    ['Số ngày giữ tối đa', 'Cấu hình chung, hiện là 30 ngày. Hạn giữ mới không được vượt quá ngày hôm nay cộng 30 ngày.'],
    ['Đang giữ', 'Số lượng còn lại của chính lô hàng giữ trên dòng đó.'],
    ['Có thể giữ', 'Số lượng hàng còn trong kho có thể giữ tiếp. Đây là số tham khảo, khác với cột Đang giữ.'],
    ['TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán — ba cấp duyệt của phiếu.'],
    ['Trạng thái Đang tạo', 'Phiếu lưu nháp hoặc bị trả về. Người lập được sửa, xóa.'],
    ['Trạng thái Chờ TP / BGĐ / KT duyệt', 'Phiếu đang chờ cấp tương ứng duyệt. Không sửa, không xóa được.'],
    ['Trạng thái Đã duyệt', 'Kế toán đã duyệt, hàng đã được chuyển sang hạn giữ mới. Chỉ xem, in, xuất Excel.'],
]

PHIEN_BAN = [
    ['1.0', '05/09/2026', 'Ban hành lần đầu cho màn hình Yêu cầu gia hạn hàng giữ trên phân hệ Tài chính.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel',
     'Một trong các quyền: Xem phiếu hàng giữ theo tổng công ty / theo công ty / theo phòng ban. Phiếu do chính mình '
     'lập và phiếu đang chờ mình duyệt luôn xem được.'],
    ['Lập phiếu', 'Không cần quyền riêng.'],
    ['Sửa, xóa phiếu', 'Người lập phiếu, phiếu đang ở trạng thái Đang tạo.'],
    ['Duyệt, từ chối phiếu', 'Quyền Trưởng phòng duyệt hàng giữ (phiếu Chờ TP duyệt, thuộc phòng ban mình quản lý) / '
                             'Ban giám đốc duyệt hàng giữ (Chờ BGĐ duyệt) / Kế toán duyệt hàng giữ (Chờ KT duyệt); '
                             'cùng công ty với phiếu.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'),
              ('Giữ hàng', 'menu_giuhang'), (TEN, 'menu_muc')],
        o_nhanh='mã phiếu hoặc tên người tạo',
        bo_loc=[('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Mã phiếu', 'o_maphieu'),
                ('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'), ('Người duyệt', 'o_nguoiduyet'),
                ('Tên hàng hóa', 'o_tenhang'), ('Mã hàng hóa', 'o_mahang'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Lập phiếu
    d.phan('LẬP PHIẾU YÊU CẦU GIA HẠN')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step('Bước 3: Hệ thống mở màn “Thêm yêu cầu gia hạn hàng giữ” và tự nạp các lô hàng giữ của bạn sắp hết hạn '
           '(trong 7 ngày tới) vào khối Chi tiết.')
    d.img('10_create', 'Màn hình Thêm yêu cầu gia hạn hàng giữ')
    d.sub('Không có lô nào sắp hết hạn thì khối Chi tiết báo chưa thể lập phiếu.')
    d.step('Bước 4: Nhập thông tin chung:')
    d.sub('Ghi chú (bắt buộc): lý do xin gia hạn, tối đa 255 ký tự.')
    d.sub(['File đính kèm (tùy chọn): bấm ', '@btn_themtailieu',
           ', chọn tệp PDF, ảnh, Word, Excel; mỗi tệp tối đa 13 MB.'])
    d.step(['Bước 5: Ở khối Chi tiết, tích ', '@o_tick', ' cột Cần gia hạn của các dòng muốn gia hạn, rồi nhập '
            '(bắt buộc với dòng đã tích):'])
    d.sub('Số lượng cần gia hạn: điền sẵn bằng số Đang giữ; chỉ nhập số, lớn hơn 0 và không vượt số Đang giữ.')
    d.sub('Hạn giữ mới: chọn ngày từ ngày mai đến hôm nay cộng 30 ngày.')
    d.step(['Bước 6: Bấm ', '@btn_guiduyet', ' để gửi Trưởng phòng duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (trạng thái Đang tạo).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do bạn lập.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa yêu cầu gia hạn hàng giữ”.')
    d.img('12_edit', 'Màn hình Sửa yêu cầu gia hạn hàng giữ')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Lập phiếu ở PHẦN 2).')
    d.step(['Bước 5: Bấm ', '@btn_guiduyet', ' để gửi duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 5 — Duyệt
    d.phan('DUYỆT PHIẾU')
    d.step(['Bước 1: Bấm ', '@btn_duyet_row', ' ở cột Hành động của phiếu đang chờ bạn duyệt để mở màn chi tiết.'])
    d.sub('Hoặc bấm vào Mã phiếu của phiếu đó.')
    d.step('Bước 2: Kiểm tra các dòng hàng. Bỏ tích cột Cần gia hạn ở dòng không đồng ý, sửa Hạn giữ mới nếu cần '
           '(không sửa được số lượng).')
    d.step(['Bước 3: Bấm nút duyệt theo cấp của bạn (TP duyệt / BGĐ duyệt / KT duyệt), ví dụ ', '@btn_duyet'])
    d.step('Bước 4: Hệ thống hiện hộp xác nhận “Xác nhận duyệt”.')
    d.img('14_approve', 'Hộp xác nhận duyệt phiếu')
    d.step(['Bước 5: Bấm ', '@btn_confirm_duyet', ' để duyệt phiếu'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 6 — Từ chối
    d.phan('TỪ CHỐI PHIẾU')
    d.step(['Bước 1: Bấm ', '@btn_tuchoi_row', ' ở cột Hành động của phiếu đang chờ bạn duyệt.'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_tuchoi'])
    d.step('Bước 2: Hệ thống mở cửa sổ “Từ chối yêu cầu gia hạn hàng giữ”.')
    d.img('15_reject', 'Cửa sổ Từ chối yêu cầu gia hạn hàng giữ')
    d.step('Bước 3: Nhập Lý do từ chối (bắt buộc, tối đa 255 ký tự).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận. Phiếu quay về trạng thái Đang tạo.'])
    d.sub(['Hoặc bấm ', '@btn_dong_reject', ' nếu muốn hủy.'])

    # PHẦN 7 — Lịch sử
    d.lich_su('Mã phiếu', img='16_history', cap='Cửa sổ Lịch sử yêu cầu gia hạn hàng giữ')

    # PHẦN 8 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết yêu cầu gia hạn hàng giữ”.')
    d.img('17_detail', 'Màn hình Chi tiết yêu cầu gia hạn hàng giữ')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 9 — In
    d.phan('IN PHIẾU VÀ IN DANH SÁCH')
    d.h2('1. In phiếu')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước yêu cầu gia hạn hàng giữ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])
    d.h2('2. In danh sách')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách yêu cầu gia hạn hàng giữ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    # PHẦN 10..12
    d.xuat_excel()
    d.cai_dat_bo_loc()
    d.tuy_chinh_cot()
    return d.save(OUT)


if __name__ == '__main__':
    out = build()
    pdf = os.path.splitext(out)[0] + '.pdf'
    size = finalize_word(out, pdf)
    print('docx', out, size)
    print('TOC:')
    for line in toc_lines(out):
        print('  ', line)
    n, warn, sheets = render_check(pdf, os.path.join(HERE, 'out', 'render'))
    print('pages', n)
    for w_ in warn:
        print('WARN', w_)
    for s in sheets:
        print(s)
