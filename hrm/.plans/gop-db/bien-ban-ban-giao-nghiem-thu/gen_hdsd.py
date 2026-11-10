# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Biên bản bàn giao nghiệm thu (form chuẩn Danh mục quốc gia, 10/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Bien ban ban giao nghiem thu.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (bbbgnt_shots/uml/overview.png).
Khuôn cấu trúc: ../phieu-nhap-hang-dieu-chinh-kiem-ke/gen_hdsd.py.
Ảnh + icon: bbbgnt_shots (dev-hrm 10/11/2026, _capture/capture.js, chặn mọi yêu cầu ghi — 0 yêu cầu ghi). Trạng thái thật trên dev
(TPE.BBBG.02738 / 02737 Đang tạo, 02736 Đã duyệt). Ảnh 12b_confirm_approve giả trạng thái trên trình duyệt (SL nghiệm thu = SL đã xuất).
btn_luu.png = bản sao btn_luu_cfg.png (nút Lưu của cửa sổ Cài đặt bộ lọc — hàm chung cai_dat_bo_loc() đọc tên btn_luu).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Biên bản bàn giao nghiệm thu'
SHOTS = os.path.join(HERE, 'bbbgnt_shots')
OUT = os.path.join(HERE, 'HDSD_Bien ban ban giao nghiem thu.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_bbbgnt')

THUAT_NGU = [
    ['Biên bản bàn giao nghiệm thu', 'Chứng từ <mã công ty>.BBBG.NNNNN ghi nhận hàng của 1 hợp đồng / đơn hàng đã bàn giao, nghiệm '
                                     'thu với khách hàng.'],
    ['Hợp đồng/đơn hàng', 'Hợp đồng hãng (Hợp đồng bán hàng hóa - vật tư, Hợp đồng dự án, Đơn hàng nguyên tắc) hoặc Hợp đồng HRM đã '
                          'xuất hết hàng; mỗi hợp đồng có tối đa 1 biên bản.'],
    ['NVKD / NV kỹ thuật', 'Nhân viên kinh doanh của hợp đồng / nhân viên kỹ thuật thực hiện bàn giao.'],
    ['SL đã nghiệm thu', 'Số lượng hàng bàn giao trên biên bản; Lưu và duyệt phải bằng Số lượng đã xuất.'],
    ['Thông tin chi tiết', 'Các dòng Seri, Ngày bàn giao, Thời gian bảo hành (ngày), Hết hạn, Ghi chú của từng hàng.'],
    ['Đang tạo', 'Trạng thái (nhãn xám): đã Lưu nháp, người tạo còn sửa / xóa được.'],
    ['Chờ duyệt', 'Trạng thái (nhãn vàng) của dữ liệu cũ; không có thao tác tạo ra.'],
    ['Đã duyệt', 'Trạng thái (nhãn xanh lá): đã Lưu và duyệt, không sửa / xóa được.'],
]
PHIEN_BAN = [['1.0', '10/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, chi tiết, in, xuất Excel, xem lịch sử',
     'Xem biên bản bàn giao nghiệm thu (mức Tổng công ty / Công ty / Phòng ban). Không có quyền thì thấy biên bản mình tạo; mục '
     '“BB bàn giao nghiệm thu theo NV” thấy biên bản mình là NVKD.'],
    ['Tạo mới, Lưu và duyệt', 'Tạo biên bản bàn giao nghiệm thu.'],
    ['Sửa, Xóa biên bản Đang tạo', 'Người tạo biên bản (có quyền Tạo biên bản bàn giao nghiệm thu).'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.truy_cap([('Công việc', 'menu_phanhe_cv'), ('Kết quả công việc', 'menu_nhom_cv'),
                ('Biên bản bàn giao nghiệm thu', 'menu_muc_cv')],
               'số BBBG', bo_loc=[('Ngày BGNT', 'o_ngaybgnt'), ('Số hợp đồng', 'o_sohd'), ('Khách hàng', 'o_khachhang'),
                                  ('NV kỹ thuật', 'o_nvkt'), ('Người tạo', 'o_nguoitao'), ('Trạng thái', 'o_trangthai'),
                                  ('Ngày tạo', 'o_ngaytao'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban')])
    # 2 lối vào khác ngay dưới Bước 1 không chèn được (hàm chung) → ghi thành đoạn cuối phần 1
    d.p(['Lối vào khác: từ phân hệ CSKH sau bán ', '@menu_phanhe_cc', ', menu Hồ sơ công việc ', '@menu_nhom_cc',
         ', chọn Biên bản bàn giao nghiệm thu ', '@menu_muc_cc', ' (cùng danh sách); hoặc từ phân hệ Thông báo ', '@menu_phanhe_tb',
         ', menu Thông báo ', '@menu_nhom_tb', ', chọn BB bàn giao nghiệm thu theo NV ', '@menu_muc_tb',
         ' để xem các biên bản mình là nhân viên kinh doanh.'])

    d.phan('THÊM MỚI BIÊN BẢN')
    d.step('Bước 1: Truy cập vào màn hình Biên bản bàn giao nghiệm thu (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step(['Bước 3: Bấm ô Hợp đồng/đơn hàng ', '@o_hopdong', ', trong cửa sổ Chọn hợp đồng/đơn hàng tìm theo số hợp đồng ',
            '@btn_timkiem_popup', ' rồi bấm vào dòng hợp đồng cần lập.'])
    d.sub(['Nếu đã có hợp đồng, bấm ', '@btn_xacnhan_doihd', ' để thay bằng hợp đồng mới.'])
    d.img('10c_filled', 'Màn hình Tạo biên bản bàn giao nghiệm thu')
    d.step(['Bước 4: Ở bảng Hàng hoá, nhập Số lượng đã nghiệm thu ', '@o_slnghiemthu',
            '; nhập Seri, Thời gian bảo hành, Ghi chú ở các dòng chi tiết tự thêm.'])
    d.step(['Bước 5: Chọn Nhân viên kỹ thuật ', '@o_nvkythuat', ', Ngày bàn giao ', '@o_ngaybangiao', ', kiểm tra Số điện thoại '
            'người nhận ', '@o_sdtnhan', ', Người nhận bàn giao ', '@o_nguoinhan', ', nhập Ghi chú ', '@o_ghichu'])
    d.step(['Bước 6: Bấm ', '@btn_themtailieu', ' để đính kèm file biên bản (pdf, jpg, jpeg, png, docx).'])
    d.step(['Bước 7: Bấm ', '@btn_luunhap', ' để lưu và về danh sách'])
    d.sub(['Hoặc bấm ', '@btn_luutieptuc', ' để lưu và lập biên bản tiếp'])
    d.sub(['Hoặc bấm ', '@btn_luuduyet', ' để lưu và duyệt ngay (PHẦN 4)'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ', chọn ', '@btn_thoat', ' để không lưu hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('CHỈNH SỬA BIÊN BẢN')
    d.step('Bước 1: Truy cập vào màn hình Biên bản bàn giao nghiệm thu, tìm biên bản Đang tạo do mình tạo.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết biên bản, bấm ', '@btn_sua'])
    d.img('12_edit', 'Màn hình Sửa biên bản bàn giao nghiệm thu')
    d.step(['Bước 3: Sửa thông tin cần sửa (cách nhập như PHẦN 2); bấm ', '@o_hopdong', ' nếu cần chọn lại hợp đồng.'])
    d.step(['Bước 4: Bấm ', '@btn_luunhap', ' để lưu'])
    d.sub(['Hoặc bấm ', '@btn_luuduyet', ' để lưu và duyệt (PHẦN 4)'])
    d.sub(['Hoặc bấm ', '@btn_quaylai_form', ' để không lưu.'])

    d.phan('LƯU VÀ DUYỆT BIÊN BẢN')
    d.step('Bước 1: Mở màn Tạo mới (PHẦN 2) hoặc Sửa (PHẦN 3), nhập đủ Hợp đồng/đơn hàng, Số điện thoại người nhận, Nhân viên kỹ '
           'thuật, Ngày bàn giao, File đính kèm và Số lượng đã nghiệm thu bằng Số lượng đã xuất.')
    d.step(['Bước 2: Bấm ', '@btn_luuduyet', '. Hệ thống hiện hộp Xác nhận lưu và duyệt.'])
    d.img('12b_confirm_approve', 'Hộp Xác nhận lưu và duyệt')
    d.step(['Bước 3: Bấm ', '@btn_luuduyet_confirm', ' để duyệt'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' để không duyệt.'])

    d.phan('XÓA BIÊN BẢN')
    d.step(['Bước 1: Ở dòng biên bản Đang tạo do mình tạo, bấm ', '@btn_xoa_row', ' ở cột Hành động'])
    d.sub(['Hoặc tại màn chi tiết biên bản, bấm ', '@btn_xoa'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa”.')
    d.img('13_delete', 'Hộp xác nhận xóa biên bản')
    d.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa'])
    d.sub(['Hoặc bấm ', '@btn_huy_xoa', ' nếu bấm nhầm.'])

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_lichsu'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step(['Bước 1: Bấm vào Số BBBG ', '@link_sophieu', ' để mở màn chi tiết'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của biên bản')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step('Bước 1: Truy cập vào màn hình Biên bản bàn giao nghiệm thu.')
    d.step(['Bước 2: Bấm vào Số BBBG ', '@link_sophieu', '. Hệ thống mở màn Chi tiết biên bản.'])
    d.sub(['Bấm số hợp đồng ', '@link_hd_detail', ' để mở hợp đồng ở tab mới.'])
    d.img('17_detail', 'Màn hình Chi tiết biên bản bàn giao nghiệm thu')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('IN BIÊN BẢN')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in', ' (dòng có nút Sửa, Xóa)'])
    d.sub(['Hoặc tại màn chi tiết biên bản, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước biên bản bàn giao nghiệm thu')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('IN DANH SÁCH')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1), tối đa 2.000 dòng.')
    d.step(['Bước 2: Bấm ', '@btn_inds', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách biên bản')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.xuat_excel(cua_so='Chọn trường xuất file')
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
