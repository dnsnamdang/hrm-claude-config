# -*- coding: utf-8 -*-
"""HDSD_Phiếu nhập kho điều chỉnh kiểm kê — bản GỌN form quốc gia (khuôn màn mẫu finance-declare-debt-beginning/docs/kh).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Phiếu nhập kho điều chỉnh kiểm kê'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Phiếu nhập kho điều chỉnh kiểm kê', 'Phiếu nhập vào kho phần hàng thừa phát hiện khi kiểm kê hàng hóa; số phiếu dạng PNKĐCKK-00001.'],
        ['Phiếu kiểm kê', 'Phiếu kiểm kê hàng hóa (Kho => Kiểm kho => Theo vị trí => Kiểm kê theo hàng hóa) — nguồn của phiếu nhập kho điều chỉnh.'],
        ['Hàng thừa', 'Hàng có số thực tế nhiều hơn sổ sách, chưa được xử lý.'],
        ['Đang tạo / Chờ duyệt', 'Đã lưu nháp, chưa nhập hàng / đã gửi duyệt, hàng thừa đã nhập vào kho.'],
        ['Đang hạch toán / Đã hạch toán', 'Kế toán kho đã lập phiếu nhập hàng điều chỉnh kiểm kê (chưa duyệt / đã duyệt).'],
    ],
    'phien_ban': [['1.0', '18/11/2026', 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng vào được màn hình và thấy phiếu do mình tạo. Quyền "Xem phiếu nhập kho điều chỉnh kiểm kê" mở rộng phạm vi xem: mức Công ty (phiếu của công ty đang làm việc) hoặc Tổng công ty (phiếu mọi công ty). Phiếu Đang tạo của người khác không bao giờ hiện.',
        'Lập phiếu: cần quyền "Tạo phiếu nhập kho điều chỉnh kiểm kê" và "Xử lý phiếu kiểm kê hàng hóa". Sửa, Gửi duyệt: người tạo phiếu, khi phiếu còn Đang tạo.',
        'Người có quyền "Kế toán kho" thấy thêm mọi phiếu Chờ duyệt, nhận thông báo khi có phiếu gửi duyệt và bấm "Tạo phiếu nhập hàng" để hạch toán.',
        'Màn hình không có Xóa, Hủy, Từ chối phiếu.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Kho {icon:menu_phanhe}, tại menu Nhập kho {icon:menu_nhom}, chọn Phiếu nhập kho điều chỉnh kiểm kê {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình danh sách Phiếu nhập kho điều chỉnh kiểm kê'),
            ('step', 'Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, nhập {icon:o_maphieu} rồi nhấn Enter để lọc theo mã phiếu'),
            ('sub', 'Hoặc chọn giá trị {icon:o_kho} để lọc theo kho'),
            ('sub', 'Hoặc chọn giá trị {icon:o_trangthai} để lọc theo trạng thái'),
            ('sub', 'Hoặc chọn giá trị {icon:o_nguoitao} để lọc theo người tạo'),
            ('sub', 'Hoặc nhập {icon:o_mahang} / {icon:o_tenhang} rồi nhấn Enter để tìm phiếu có hàng hóa đó'),
            ('sub', 'Hoặc chọn khoảng ngày {icon:o_ngaytao}'),
            ('sub', 'Hoặc chọn {icon:o_congty}, {icon:o_phongban} (dùng được theo phạm vi xem của bạn)'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
        ]),
        ('LẬP PHIẾU NHẬP KHO ĐIỀU CHỈNH KIỂM KÊ', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi}'),
            ('sub', 'Hoặc tại chi tiết phiếu kiểm kê hàng hóa, bấm {icon:btn_tu_kiemke} — phiếu kiểm kê được chọn sẵn.'),
            ('img', '10_create', 'Trang Tạo phiếu nhập kho điều chỉnh kiểm kê'),
            ('step', 'Bước 3: Chọn Phiếu kiểm kê (bắt buộc). Danh sách chỉ có phiếu kiểm kê Chờ xử lý / Đang xử lý còn hàng thừa chưa nhập điều chỉnh.'),
            ('step', 'Bước 4: Chọn Kho (bắt buộc) — hệ thống chọn sẵn kho đầu tiên của phiếu kiểm kê; đổi kho thì bảng Chi tiết nạp lại hàng thừa của kho đó.'),
            ('sub2', 'Bảng ghi "Kho này không còn hàng thừa cần nhập điều chỉnh" thì chọn kho khác.'),
            ('step', 'Bước 5: Nhập Ghi chú (bắt buộc, tối đa 255 ký tự).'),
            ('step', 'Bước 6: Bấm {icon:btn_themtailieu} rồi bấm "Chọn tệp" để đính kèm ít nhất 1 file (pdf, png, jpg, jpeg; tối đa 20MB/file).'),
            ('sub2', 'Tự điền: bảng Chi tiết (Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Số lượng) lấy từ phiếu kiểm kê, không sửa được; số phiếu hệ thống sinh khi lưu.'),
            ('img', '10b_create_filled', 'Đã chọn phiếu kiểm kê, kho, nhập ghi chú và đính kèm file'),
            ('step', 'Bước 7: Bấm {icon:btn_luu} để lưu phiếu ở trạng thái Đang tạo (CHƯA nhập hàng vào kho) và về danh sách.'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu rồi lập tiếp phiếu cho phiếu kiểm kê khác.'),
            ('sub', 'Hoặc {icon:btn_guiduyet} để gửi duyệt ngay (xem PHẦN 3).'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lưu; đã nhập dữ liệu thì bấm Thoát để thoát hoặc Ở lại để ở lại.'),
            ('sub2', 'Thiếu thông tin: hệ thống báo đỏ "Bắt buộc phải nhập" dưới ô thiếu và "Bạn chưa nhập đầy đủ thông tin.".'),
        ]),
        ('GỬI DUYỆT PHIẾU', [
            ('step', 'Bước 1: Tại trang Tạo phiếu (hoặc trang Sửa phiếu Đang tạo của bạn), nhập đủ thông tin.'),
            ('step', 'Bước 2: Bấm {icon:btn_guiduyet}. Hệ thống hiện hộp "Xác nhận gửi duyệt".'),
            ('img', '15_send_confirm', 'Hộp Xác nhận gửi duyệt'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_guiduyet} để xác nhận. Hàng thừa được nhập ngay vào kho, phiếu chuyển Chờ duyệt, Kế toán kho nhận thông báo; phiếu không sửa được nữa.'),
            ('sub', 'Hoặc bấm {icon:btn_huy_confirm} nếu bấm nhầm.'),
        ]),
        ('SỬA PHIẾU', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_sua} ở cột Hành động của phiếu Đang tạo do bạn tạo.'),
            ('img', '12_edit', 'Trang Sửa phiếu nhập kho điều chỉnh kiểm kê'),
            ('step', 'Bước 3: Sửa Ghi chú, thêm hoặc xóa file đính kèm. Phiếu kiểm kê, Kho và bảng Chi tiết không sửa được.'),
            ('sub2', 'Xóa file đã lưu: bấm biểu tượng thùng rác rồi bấm Xóa — file bị gỡ ngay, không chờ bấm Lưu. Phiếu phải còn ít nhất 1 file.'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để lưu, hoặc {icon:btn_guiduyet} để gửi duyệt.'),
            ('sub', 'Hoặc {icon:btn_quaylai} nếu muốn hủy.'),
        ]),
        ('XEM CHI TIẾT PHIẾU', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm vào Số phiếu. Hệ thống mở trang "Chi tiết phiếu nhập kho điều chỉnh kiểm kê".'),
            ('img', '17_detail_wait', 'Trang Chi tiết phiếu Chờ duyệt'),
            ('step', 'Bước 3: Bấm {icon:btn_sua_footer} (phiếu Đang tạo của bạn), {icon:btn_taophieunhaphang} (phiếu Chờ duyệt, Kế toán kho) hoặc {icon:btn_in_footer}; bấm {icon:btn_quaylai} để về danh sách.'),
        ]),
        ('TẠO PHIẾU NHẬP HÀNG (KẾ TOÁN KHO)', [
            ('step', 'Bước 1: Lọc Trạng thái = Chờ duyệt để thấy các phiếu đang chờ.'),
            ('step', 'Bước 2: Bấm {icon:btn_taophieunhaphang_row} ở cột Hành động (hoặc nút Tạo phiếu nhập hàng ở trang Chi tiết).'),
            ('step', 'Bước 3: Hệ thống mở trang Thêm Phiếu nhập hàng điều chỉnh kiểm kê (phân hệ Tài chính) với phiếu này chọn sẵn; hoàn tất và lưu theo hướng dẫn của màn đó.'),
            ('step', 'Bước 4: Lưu phiếu nhập hàng thì phiếu nhập kho chuyển Đang hạch toán; Lưu và duyệt thì chuyển Đã hạch toán, cột Người duyệt / Ngày duyệt được ghi.'),
        ]),
        ('IN PHIẾU', [
            ('step', 'Bước 1: Bấm {icon:btn_in_row} ở cột Hành động (hoặc nút In ở trang Chi tiết).'),
            ('img', '19_print', 'Cửa sổ xem trước bản in phiếu'),
            ('step', 'Bước 2: Bấm {icon:btn_in} để in.'),
        ]),
        ('IN DANH SÁCH', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_indanhsach}. Hệ thống mở cửa sổ xem trước bản in danh sách.'),
            ('img', '19b_printlist', 'Cửa sổ xem trước bản in danh sách'),
            ('step', 'Bước 3: Bấm {icon:btn_in} để in. Danh sách quá 2,000 dòng thì cần lọc hẹp lại hoặc dùng Xuất Excel.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ba gạch để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất (danh_sach_phieu_nhap_kho_dieu_chinh_kiem_ke.xlsx).'),
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
