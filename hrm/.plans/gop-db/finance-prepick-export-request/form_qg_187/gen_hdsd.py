# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Yêu cầu xuất giữ (STT 187, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Yêu cầu xuất giữ.docx (+ .pdf, render/ để soát)
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py — khuôn y hệt màn 27.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Yêu cầu xuất giữ'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [
    ['Hàng giữ', 'Số lượng hàng hóa trong kho được giữ lại cho một khách hàng, do một nhân viên kinh doanh đứng tên '
                 'giữ, tới một hạn nhất định.'],
    ['Yêu cầu xuất giữ', 'Phiếu đề nghị giữ hàng, mã PYCXG. Lập xong chưa có nghĩa là hàng đã được giữ.'],
    ['Phiếu xuất giữ', 'Phiếu do Kế toán lập ở bước cuối, mã PXG. Khi phiếu này được duyệt thì hàng mới thực sự '
                       'được giữ.'],
    ['Loại yêu cầu', 'Sáu loại: Xuất giữ thường, Xuất giữ khuyến mại, Xuất giữ HĐDV, Xuất giữ HĐDA, Xuất giữ HĐ hãng '
                     '(năm loại gắn hợp đồng) và Xuất giữ khác (không gắn hợp đồng).'],
    ['Giữ đến ngày', 'Hạn xin giữ hàng tới. Bắt buộc, phải là ngày trong tương lai.'],
    ['Cần xuất', 'Ô tích đánh dấu dòng hàng thực sự xin giữ. Dòng không tích được lưu với số lượng 0.'],
    ['Có thể giữ', 'Số hàng còn trong kho có thể giữ được, là số tham khảo khi nhập số lượng.'],
    ['Đề nghị', 'Số lượng xin giữ cho dòng hàng đó.'],
    ['TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán — ba cấp xử lý của phiếu.'],
    ['Trạng thái Đang tạo', 'Phiếu còn nháp, hoặc vừa bị một cấp trả về. Người lập được sửa, xóa.'],
    ['Trạng thái Chờ TP / BGĐ / KT duyệt', 'Phiếu đang chờ cấp tương ứng xử lý. Không sửa, không xóa được.'],
    ['Trạng thái Đang xuất giữ', 'Kế toán đã lập Phiếu xuất giữ nhưng còn để nháp.'],
    ['Trạng thái Đã duyệt', 'Phiếu xuất giữ đã được duyệt, hàng đã được giữ.'],
]

PHIEN_BAN = [
    ['1.0', '18/09/2026', 'Ban hành lần đầu cho màn hình Yêu cầu xuất giữ trên phân hệ Tài chính.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel',
     'Một trong các quyền: Xem phiếu hàng giữ theo tổng công ty / theo công ty / theo phòng ban. Phiếu do chính mình '
     'lập và phiếu đang chờ mình xử lý luôn xem được.'],
    ['Tạo mới phiếu', 'Không cần quyền riêng.'],
    ['Sửa, xóa phiếu', 'Người lập phiếu, phiếu đang ở trạng thái Đang tạo.'],
    ['Duyệt, từ chối phiếu', 'Trưởng phòng duyệt hàng giữ (phiếu Chờ TP duyệt, phòng mình quản lý) hoặc Ban giám đốc '
                             'duyệt hàng giữ (phiếu Chờ BGĐ duyệt); cùng công ty với phiếu.'],
    ['Lập phiếu xuất giữ, từ chối ở bước Kế toán', 'Kế toán duyệt hàng giữ, cùng công ty với phiếu, phiếu Chờ KT duyệt.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'),
              ('Giữ hàng', 'menu_giuhang'), ('Yêu cầu xuất giữ', 'menu_muc')],
        o_nhanh='mã phiếu',
        bo_loc=[('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Mã phiếu', 'o_maphieu'),
                ('Loại yêu cầu', 'o_loaiyc'), ('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'),
                ('Người duyệt', 'o_nguoiduyet'), ('Khách hàng', 'o_khachhang'), ('Tên, mã hàng', 'o_tenmahang'),
                ('Số hợp đồng', 'o_sohopdong'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Tạo mới
    d.phan('TẠO MỚI YÊU CẦU XUẤT GIỮ')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10_create', 'Màn hình Thêm yêu cầu xuất giữ')
    d.step('Bước 3: Chọn Loại yêu cầu (bắt buộc). Không đổi được loại sau khi đã lưu phiếu.')
    d.step(['Bước 4: Với năm loại có hợp đồng, bấm ', '@btn_chon_hd', '. Hệ thống mở cửa sổ “Chọn hợp đồng”.'])
    d.img('11_contract', 'Cửa sổ Chọn hợp đồng')
    d.step(['Bước 5: Bấm ', '@btn_chon_dong_hd', ' ở dòng hợp đồng cần giữ hàng. Hệ thống tự điền khách hàng và nạp '
            'toàn bộ hàng hóa của hợp đồng.'])
    d.img('11b_create_hd', 'Phiếu loại có hợp đồng sau khi chọn hợp đồng')
    d.step(['Bước 6: Ở khối Chi tiết, tích ', '@o_tick', ' cột Cần xuất các dòng cần giữ và nhập Đề nghị (bắt buộc, '
            'lớn hơn 0, chỉ nhập số, không vượt Có thể giữ và phần còn lại của hợp đồng).'])
    d.sub('Hoặc với loại Xuất giữ khác: chọn Khách hàng (bắt buộc, gõ tối thiểu 2 ký tự để tìm).')
    d.sub2(['Bấm ', '@btn_themhanghoa', ', tích các hàng cần giữ rồi thêm vào phiếu.'])
    d.sub2('Chọn ĐVT (bắt buộc) và nhập Đề nghị cho từng dòng.')
    d.img('12_create_khac', 'Phiếu loại Xuất giữ khác')
    d.step('Bước 7: Nhập thông tin chung:')
    d.sub('Giữ đến ngày (bắt buộc): chọn ngày trong tương lai, không quá hạn ghi dưới ô “Không giữ quá …”.')
    d.sub('Ghi chú: tối đa 255 ký tự; tùy chọn, riêng loại Xuất giữ khác bắt buộc.')
    d.sub(['File đính kèm: bấm ', '@btn_themtailieu', ' rồi chọn tệp PDF, ảnh, Word, Excel (tối đa 13 MB mỗi tệp); '
           'tùy chọn, riêng loại Xuất giữ khác bắt buộc có ít nhất một tệp.'])
    d.step(['Bước 8: Bấm ', '@btn_guiduyet', ' để gửi Trưởng phòng duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (chưa kiểm tra tồn kho).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa yêu cầu xuất giữ”. Phiếu bị trả về có thêm ô Lý do từ chối gần '
           'nhất.')
    d.img('12_edit', 'Màn hình Sửa yêu cầu xuất giữ')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như PHẦN 2; không đổi được Loại yêu cầu và Hợp đồng).')
    d.step(['Bước 5: Bấm ', '@btn_guiduyet', ' để gửi duyệt lại từ bước Trưởng phòng,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 5 — Duyệt (TP / BGĐ)
    d.phan('DUYỆT PHIẾU (TRƯỞNG PHÒNG / BAN GIÁM ĐỐC)')
    d.step(['Bước 1: Bấm ', '@btn_duyet_row', ' ở cột Hành động của phiếu Chờ TP duyệt hoặc Chờ BGĐ duyệt để mở màn '
            'chi tiết.'])
    d.sub('Hoặc bấm vào Mã phiếu của phiếu đó.')
    d.step('Bước 2: Kiểm tra các dòng hàng và số lượng đề nghị.')
    d.step(['Bước 3: Bấm nút duyệt của cấp mình: TP duyệt hoặc ', '@btn_bgd_duyet'])
    d.step('Bước 4: Hệ thống hiện hộp xác nhận “Xác nhận duyệt”.')
    d.img('14_approve', 'Hộp xác nhận duyệt phiếu')
    d.step(['Bước 5: Bấm ', '@btn_confirm_duyet', ' để duyệt. Phiếu chuyển sang Chờ BGĐ duyệt hoặc Chờ KT duyệt.'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 6 — Từ chối
    d.phan('TỪ CHỐI PHIẾU')
    d.step('Bước 1: Mở màn chi tiết của phiếu đang chờ mình xử lý (như Bước 1 PHẦN 5).')
    d.step(['Bước 2: Bấm ', '@btn_tuchoi', '. Hệ thống mở cửa sổ “Từ chối yêu cầu xuất giữ”.'])
    d.img('15_reject', 'Cửa sổ Từ chối yêu cầu xuất giữ')
    d.step('Bước 3: Nhập Lý do từ chối (bắt buộc, tối đa 255 ký tự).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận. Phiếu quay về Đang tạo để người lập sửa và gửi lại.'])
    d.sub(['Hoặc bấm ', '@btn_dong_reject', ' nếu muốn hủy.'])

    # PHẦN 7 — Lập phiếu xuất giữ (Kế toán)
    d.phan('LẬP PHIẾU XUẤT GIỮ (KẾ TOÁN)')
    d.step(['Bước 1: Bấm ', '@btn_lapxg_row', ' ở cột Hành động của phiếu Chờ KT duyệt.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_lapxg'])
    d.step('Bước 2: Hệ thống mở màn lập Phiếu xuất giữ, dữ liệu nạp sẵn từ yêu cầu.')
    d.img('21_pxg_create', 'Màn hình lập Phiếu xuất giữ từ yêu cầu')
    d.step('Bước 3: Lập phiếu theo HDSD Phiếu xuất giữ. Lưu nháp: yêu cầu chuyển sang Đang xuất giữ; Duyệt giữ hàng: '
           'hàng được giữ và yêu cầu chuyển sang Đã duyệt.')
    d.sub('Nút Không duyệt ở màn lập phiếu xuất giữ chỉ lưu nháp, KHÔNG trả yêu cầu về người lập. Muốn trả về thì '
          'bấm Từ chối ở màn chi tiết yêu cầu (PHẦN 6).')

    # PHẦN 8 — Lịch sử
    d.lich_su('Mã phiếu', img='16_history', cap='Cửa sổ Lịch sử yêu cầu xuất giữ')

    # PHẦN 9 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết yêu cầu xuất giữ”.')
    d.img('17_detail', 'Màn hình Chi tiết yêu cầu xuất giữ')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 10 — In
    d.phan('IN PHIẾU VÀ IN DANH SÁCH')
    d.h2('1. In phiếu')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước yêu cầu xuất giữ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])
    d.h2('2. In danh sách')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách yêu cầu xuất giữ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

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
