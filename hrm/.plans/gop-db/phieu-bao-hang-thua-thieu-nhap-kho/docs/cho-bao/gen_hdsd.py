# -*- coding: utf-8 -*-
"""HDSD_Phiếu nhập kho chờ báo thừa, thiếu (STT 288) — bản GỌN form quốc gia (khuôn HDSD màn mẫu phiếu docs/kh).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Phiếu nhập kho chờ báo thừa, thiếu'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
NGAY = '18/11/2026'
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Phiếu nhập kho chờ báo thừa, thiếu', 'Phiếu nhập kho đã hạch toán (loại nhập hàng mua), có ít nhất 1 dòng hàng số lượng thực nhập khác số lượng đề nghị, chưa có phiếu báo.'],
        ['Phiếu báo hàng thừa, thiếu nhập kho', 'Chứng từ báo các dòng hàng lệch của 1 phiếu nhập kho; lập xong thì phiếu nhập kho rời khỏi màn này.'],
        ['Phiếu ĐNNK', 'Phiếu đề nghị nhập kho của phiếu nhập kho.'],
        ['Người đề nghị / Người yêu cầu / Người tạo', 'Người lập phiếu đề nghị nhập kho / người lập yêu cầu nhập hàng / người lập phiếu nhập kho.'],
    ],
    'phien_ban': [['1.0', NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng mở được màn hình và thấy phiếu nhập kho do mình lập.',
        'Quyền "Xem xử lý thừa thiếu nhập kho" mức Công ty: xem phiếu nhập kho của công ty mình; mức Tổng công ty: xem mọi công ty.',
        'Quyền "Tạo phiếu báo hàng thừa, thiếu nhập kho": thấy nút Báo hàng thừa thiếu trên từng dòng.',
        'Màn chỉ để xem và chuyển sang lập phiếu báo; không sửa phiếu nhập kho, không ghi tồn kho.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Kho {icon:menu_phanhe}, tại menu Nhập kho {icon:menu_nhom}, chọn Phiếu nhập kho chờ báo thừa, thiếu {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình danh sách Phiếu nhập kho chờ báo thừa, thiếu'),
            ('step', 'Bước 2: Nhập mã phiếu nhập kho vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, nhập mã / tên hàng vào {icon:o_hanghoa} hoặc mã đề nghị vào {icon:o_dnnk} rồi nhấn Enter'),
            ('sub', 'Hoặc chọn giá trị {icon:o_khohang}, {icon:o_loai}, {icon:o_ncc}, {icon:o_nguoidenghi}'),
            ('sub', 'Hoặc chọn khoảng ngày {icon:o_ngaytao}'),
            ('sub', 'Hoặc chọn {icon:o_congty} (chỉ hiện với người xem được mọi công ty)'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
            ('sub2', 'Bấm Mã phiếu hoặc Phiếu ĐNNK để mở chứng từ ở tab mới.'),
        ]),
        ('BÁO HÀNG THỪA THIẾU', [
            ('step', VAO),
            ('step', 'Bước 2: Ở dòng phiếu nhập kho cần báo, bấm {icon:btn_baohang} (cần quyền Tạo phiếu báo hàng thừa, thiếu nhập kho).'),
            ('img', '01b_list_actions', 'Nút Báo hàng thừa thiếu ở cột Hành động'),
            ('step', 'Bước 3: Hệ thống mở trang Tạo phiếu báo, đã điền sẵn Phiếu nhập kho, Yêu cầu nhập, Số hợp đồng, Nhà cung cấp và các dòng hàng lệch.'),
            ('img', '10_create_from_queue', 'Trang Tạo phiếu báo đã điền sẵn phiếu nhập kho'),
            ('step', 'Bước 4: Nhập Diễn giải (bắt buộc) và đính kèm ít nhất 1 file (bấm "Thêm tài liệu" → "Chọn tệp").'),
            ('step', 'Bước 5: Bấm {icon:btn_luugui} để gửi người duyệt, hoặc {icon:btn_luu} để lưu ở trạng thái Đang tạo.'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lập phiếu (đã nhập dữ liệu thì hệ thống hỏi trước khi thoát).'),
            ('sub2', 'Lưu xong hệ thống về màn Phiếu báo hàng thừa, thiếu nhập kho; phiếu nhập kho không còn ở màn chờ báo. Xem chi tiết cách lập ở HDSD Phiếu báo hàng thừa, thiếu nhập kho.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ba gạch để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất (danh_sach_phieu_nhap_kho_cho_bao_thua_thieu.xlsx).'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột (STT, Mã phiếu, Hành động luôn hiện).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột bắt buộc).'),
            ('step', 'Bước 4: Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.'),
            ('step', 'Bước 5: Bấm Lưu để áp dụng, hoặc Đóng nếu muốn bỏ thay đổi.'),
        ]),
    ],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', L.build_hdsd(scr, H, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))
