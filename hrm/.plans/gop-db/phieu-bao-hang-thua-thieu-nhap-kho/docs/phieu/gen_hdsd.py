# -*- coding: utf-8 -*-
"""HDSD_Phiếu báo hàng thừa, thiếu nhập kho (STT 289) — bản GỌN form quốc gia (khuôn HDSD màn mẫu phiếu docs/kh).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Phiếu báo hàng thừa, thiếu nhập kho'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
NGAY = '18/11/2026'
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN
HUY = ('sub', 'Hoặc bấm {icon:btn_huy_confirm} nếu bấm nhầm.')

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Phiếu báo hàng thừa, thiếu nhập kho (phiếu báo)', 'Chứng từ báo các dòng hàng của 1 phiếu nhập kho có số lượng thực nhập khác số lượng đề nghị nhập.'],
        ['Phiếu nhập kho chờ báo thừa, thiếu', 'Phiếu nhập kho đã hạch toán, có hàng lệch số lượng, chưa có phiếu báo — chỉ những phiếu này mới chọn được khi lập phiếu báo.'],
        ['SL thiếu / SL thừa', 'Số lượng đề nghị nhiều hơn / ít hơn số lượng thực nhập.'],
        ['Đang tạo / Chờ xử lý / Không duyệt / Đã xử lý', 'Đã lưu chưa gửi / đã gửi chờ người duyệt / người duyệt trả lại kèm lý do / đã lập phiếu xử lý hàng thiếu.'],
        ['Xử lý', 'Người duyệt mở màn lập phiếu xử lý hàng thiếu nhập kho (ở hệ thống quản lý kho cũ, tab mới); lập xong phiếu báo chuyển Đã xử lý.'],
    ],
    'phien_ban': [['1.0', NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng mở được màn hình và thấy phiếu báo do mình tạo; sửa, xóa phiếu của mình khi phiếu Đang tạo hoặc Không duyệt.',
        'Quyền "Xem xử lý thừa thiếu nhập kho" mức Công ty: xem thêm phiếu của công ty mình; mức Tổng công ty: xem phiếu mọi công ty.',
        'Quyền "Tạo phiếu báo hàng thừa, thiếu nhập kho": lập phiếu báo (nút Tạo mới).',
        'Quyền "Duyệt phiếu báo hàng thừa, thiếu nhập kho": xem thêm phiếu Chờ xử lý của công ty mình, Không duyệt và Xử lý phiếu Chờ xử lý.',
        'Phiếu báo không ghi tồn kho, không sinh bút toán.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Kho {icon:menu_phanhe}, tại menu Nhập kho {icon:menu_nhom}, chọn Phiếu báo hàng thừa, thiếu nhập kho {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình danh sách Phiếu báo hàng thừa, thiếu nhập kho'),
            ('step', 'Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, nhập mã vào {icon:o_pnk}, {icon:o_ycn} hoặc {icon:o_hopdong} rồi nhấn Enter'),
            ('sub', 'Hoặc nhập mã / tên hàng vào {icon:o_hanghoa} rồi nhấn Enter'),
            ('sub', 'Hoặc chọn giá trị {icon:o_ncc}, {icon:o_trangthai}, {icon:o_nguoitao}'),
            ('sub', 'Hoặc chọn khoảng ngày {icon:o_ngaytao}'),
            ('sub', 'Hoặc chọn {icon:o_congty} (chỉ hiện với người xem được mọi công ty)'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
        ]),
        ('LẬP PHIẾU BÁO HÀNG THỪA, THIẾU', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi}'),
            ('sub', 'Hoặc tại màn Phiếu nhập kho chờ báo thừa, thiếu, bấm biểu tượng Báo hàng thừa thiếu ở dòng phiếu nhập kho — ô Phiếu nhập kho được điền sẵn.'),
            ('img', '10_create', 'Trang Tạo phiếu báo hàng thừa, thiếu nhập kho'),
            ('step', 'Bước 3: Bấm vào ô {icon:o_chonpnk}. Hệ thống mở cửa sổ "Chọn phiếu nhập kho".'),
            ('img', '14_picker', 'Cửa sổ Chọn phiếu nhập kho'),
            ('step', 'Bước 4: Bấm vào dòng phiếu nhập kho cần báo (bấm vào chữ Mã phiếu là mở phiếu nhập kho ở tab mới để xem trước).'),
            ('sub2', 'Hệ thống tự điền Yêu cầu nhập, Số hợp đồng, Nhà cung cấp và bảng Chi tiết gồm các dòng hàng lệch: SL thiếu (chữ đỏ), SL thừa (chữ xanh).'),
            ('step', 'Bước 5: Nhập thông tin:'),
            ('sub2', 'Bắt buộc: Diễn giải (tối đa 255 ký tự); File đính kèm — bấm {icon:btn_themtailieu}, bấm "Chọn tệp" và chọn file (ppt, pptx, doc, docx, pdf, xls, xlsx, jpg, jpeg, png, zip, tối đa 15MB/file), ít nhất 1 file.'),
            ('sub2', 'Tự điền, không sửa: Yêu cầu nhập, Số hợp đồng, Nhà cung cấp, bảng Chi tiết; số phiếu hệ thống sinh khi lưu.'),
            ('img', '10b_create_filled', 'Đã chọn phiếu nhập kho, nhập Diễn giải và đính kèm file'),
            ('step', 'Bước 6: Bấm {icon:btn_luugui} để lưu và gửi người duyệt (phiếu chuyển Chờ xử lý, người duyệt nhận thông báo).'),
            ('sub', 'Hoặc {icon:btn_luu} để lưu ở trạng thái Đang tạo, gửi sau.'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu (Đang tạo) rồi lập tiếp phiếu khác.'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lưu; đã nhập dữ liệu thì bấm {icon:btn_thoat} để thoát hoặc {icon:btn_olai} để ở lại.'),
            ('sub2', 'Thiếu thông tin, hệ thống báo đỏ dưới từng ô và hiện "Bạn chưa nhập đầy đủ thông tin."'),
            ('img', '11_validate', 'Báo lỗi khi chưa nhập đủ thông tin bắt buộc'),
        ]),
        ('SỬA PHIẾU BÁO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_sua} ở cột Hành động của phiếu Đang tạo hoặc Không duyệt do mình tạo.'),
            ('img', '12_edit', 'Trang Sửa phiếu báo hàng thừa, thiếu'),
            ('step', 'Bước 3: Sửa Diễn giải, thêm file bằng {icon:btn_themtailieu}. Phiếu nhập kho và bảng Chi tiết không sửa được.'),
            ('sub2', 'Phiếu bị Không duyệt hiện ô "Lý do không duyệt" để biết cần sửa gì.'),
            ('sub2', 'Bấm nút xóa ở dòng file đã lưu và xác nhận thì file bị gỡ ngay, không chờ bấm Lưu.'),
            ('step', 'Bước 4: Bấm {icon:btn_luugui} để gửi lại người duyệt, hoặc {icon:btn_luu} để lưu ở trạng thái Đang tạo.'),
            ('sub', 'Hoặc {icon:btn_quaylai} nếu muốn hủy.'),
        ]),
        ('XEM CHI TIẾT PHIẾU BÁO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm vào Số phiếu. Hệ thống mở trang "Chi tiết phiếu báo hàng thừa, thiếu".'),
            ('img', '17c_detail_draft', 'Trang Chi tiết phiếu Đang tạo'),
            ('step', 'Bước 3: Bấm {icon:btn_sua_footer} hoặc {icon:btn_xoa_footer} (phiếu Đang tạo / Không duyệt của mình), hoặc {icon:btn_quaylai} để về danh sách.'),
        ]),
        ('XÓA PHIẾU BÁO', [
            ('step', 'Bước 1: Bấm {icon:btn_xoa} ở cột Hành động (hoặc nút Xóa ở trang Chi tiết) của phiếu Đang tạo / Không duyệt do mình tạo.'),
            ('step', 'Bước 2: Hệ thống hiện hộp "Xác nhận xóa"'),
            ('img', '13_delete', 'Hộp Xác nhận xóa phiếu báo'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_xoa} để xác nhận. Phiếu nhập kho của phiếu báo quay lại màn Phiếu nhập kho chờ báo thừa, thiếu.'),
            HUY,
        ]),
        ('KHÔNG DUYỆT PHIẾU BÁO', [
            ('step', 'Bước 1: Bấm vào Số phiếu của phiếu Chờ xử lý để mở trang Chi tiết (cần quyền Duyệt phiếu báo hàng thừa, thiếu nhập kho).'),
            ('img', '17_detail', 'Trang Chi tiết phiếu Chờ xử lý'),
            ('step', 'Bước 2: Bấm {icon:btn_khongduyet}. Hệ thống mở cửa sổ "Không duyệt phiếu báo hàng thừa, thiếu".'),
            ('img', '15_reject', 'Cửa sổ Không duyệt'),
            ('step', 'Bước 3: Nhập Lý do không duyệt (bắt buộc, tối đa 255 ký tự), bấm {icon:btn_khongduyet_modal}. Người tạo nhận thông báo kèm lý do.'),
            ('sub', 'Hoặc bấm {icon:btn_huy_modal} nếu bấm nhầm.'),
            ('img', '17d_detail_rejected', 'Phiếu Không duyệt hiện lý do, người duyệt và thời điểm'),
        ]),
        ('XỬ LÝ PHIẾU BÁO', [
            ('step', 'Bước 1: Ở danh sách bấm {icon:btn_xuly} trên dòng phiếu Chờ xử lý, hoặc bấm {icon:btn_xuly_footer} ở trang Chi tiết (cần quyền Duyệt).'),
            ('step', 'Bước 2: Hệ thống mở màn lập phiếu xử lý hàng thiếu nhập kho ở tab mới, đã chọn sẵn phiếu báo; lập phiếu xử lý tại màn đó.'),
            ('step', 'Bước 3: Quay lại danh sách, bấm Tìm kiếm: phiếu báo đã chuyển Đã xử lý.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ba gạch để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất (danh_sach_phieu_bao_hang_thua_thieu_nhap_kho.xlsx).'),
        ]),
        ('XEM LỊCH SỬ THAY ĐỔI', [
            ('p', 'Cách 1: Xem từ màn danh sách:'),
            ('step', 'Ở cột Hành động, bấm {icon:btn_lichsu_row}'),
            ('img', '16_history', 'Cửa sổ Lịch sử thay đổi'),
            ('p', 'Cách 2: Xem từ màn chi tiết:'),
            ('step', 'Bước 1: Bấm vào số phiếu để mở trang Chi tiết'),
            ('step', 'Bước 2: Tại khối Lịch sử cuối trang, bấm {icon:btn_xemlichsu}'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột (STT, Số phiếu, Hành động luôn hiện).'),
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
