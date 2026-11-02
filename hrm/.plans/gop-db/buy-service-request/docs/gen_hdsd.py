# -*- coding: utf-8 -*-
"""HDSD_Yêu cầu mua dịch vụ — bản GỌN form quốc gia (chép khuôn finance-declare-debt-beginning/docs/kh/gen_hdsd.py).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Yêu cầu mua dịch vụ'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN
CT = 'Bước 2: Bấm vào Số phiếu để mở trang Chi tiết phiếu.'
HUY = ('sub', 'Hoặc bấm Hủy nếu bấm nhầm.')

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Phiếu yêu cầu mua dịch vụ', 'Đề nghị mua dịch vụ thuê ngoài (vận chuyển, lắp đặt, thuê nhân công, kiểm định…) gồm Ghi chú, file báo giá và các dòng dịch vụ.'],
        ['TP / KS', 'Trưởng phòng (duyệt nội dung) / Ban kiểm soát (duyệt giá).'],
        ['Đang tạo', 'Phiếu nháp, chỉ người lập thấy; còn Sửa, Xóa được.'],
        ['Chờ TP duyệt / Chờ KS duyệt', 'Phiếu đang chờ Trưởng phòng / Ban kiểm soát duyệt.'],
        ['Đã duyệt', 'Đã qua 2 nấc duyệt, dùng để lập Hợp đồng mua dịch vụ.'],
        ['Không duyệt', 'Bị từ chối; người lập sửa và gửi duyệt lại.'],
        ['Đang lập / Đã lập hợp đồng', 'Đã lập hợp đồng một phần / đủ số lượng (hệ thống tự cập nhật).'],
        ['Hủy', 'Người lập hủy phiếu đã duyệt.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi nhân viên đăng nhập đều vào được màn hình, lập phiếu, xem / sửa / xóa phiếu do mình lập (khi phiếu Đang tạo hoặc Không duyệt), in, xuất Excel.',
        'Trưởng phòng cần quyền "Trưởng phòng duyệt yêu cầu mua dịch vụ"; Ban kiểm soát cần quyền "Ban kiểm soát duyệt giá mua dịch vụ" (chỉ duyệt phiếu cùng công ty). Người duyệt nhận thông báo khi có phiếu chờ duyệt, bấm thông báo để mở phiếu.',
        'Danh sách hiển thị theo quyền xem: "Xem yêu cầu mua dịch vụ - theo tổng công ty" (mọi công ty), "… - theo công ty", "… - theo phòng ban"; không có quyền nào thì chỉ thấy phiếu mình lập. Phiếu Đang tạo chỉ người lập thấy.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Bán hàng {icon:menu_phanhe}, tại menu Yêu cầu {icon:menu_nhom}, nhóm Mua dịch vụ {icon:menu_nhomcon}, chọn Yêu cầu mua dịch vụ {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình danh sách Yêu cầu mua dịch vụ'),
            ('step', 'Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao} để mở các ô lọc:'),
            ('sub', 'Nhập {icon:o_sophieu} hoặc {icon:o_tendv} rồi nhấn Enter'),
            ('sub', 'Hoặc chọn giá trị {icon:o_trangthai} để lọc theo trạng thái'),
            ('sub', 'Hoặc chọn {icon:o_nguoiduyetgia}, {icon:o_nguoitao}'),
            ('sub', 'Hoặc chọn khoảng ngày {icon:o_ngaytao}'),
            ('sub', 'Hoặc chọn {icon:o_congty}, {icon:o_phongban} (chỉ hiện với người có quyền xem rộng)'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
        ]),
        ('LẬP PHIẾU YÊU CẦU MUA DỊCH VỤ', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi}'),
            ('img', '10_create', 'Trang Tạo phiếu yêu cầu mua dịch vụ'),
            ('step', 'Bước 3: Nhập Ghi chú (bắt buộc, tối đa 255 ký tự): nội dung cần mua dịch vụ.'),
            ('step', 'Bước 4: Bấm {icon:btn_themtailieu} để đính kèm báo giá (bắt buộc khi Gửi duyệt; pdf, ảnh, Word, Excel, zip; mỗi file tối đa 10 MB).'),
            ('step', 'Bước 5: Nhập từng dòng dịch vụ, bấm {icon:btn_themdong} để thêm dòng:'),
            ('sub2', 'Bắt buộc khi Gửi duyệt: Tên dịch vụ, Số lượng, Giá đề xuất mua trước VAT.'),
            ('sub2', 'Tùy chọn: Nhà cung cấp (gõ mã hoặc tên để tìm); VAT (%) ở dòng tổng (0 – 100).'),
            ('sub2', 'Tự điền: ĐVT "Gói", Thành tiền đề xuất = Số lượng × Giá đề xuất, các dòng Thành tiền, VAT, Tổng thanh toán; số phiếu hệ thống sinh khi lưu.'),
            ('sub2', 'Bấm thùng rác cuối dòng để bỏ dòng.'),
            ('img', '10b_create_filled', 'Đã nhập Ghi chú, file đính kèm và 2 dòng dịch vụ'),
            ('step', 'Bước 6: Bấm {icon:btn_guiduyet} để gửi Trưởng phòng duyệt. Phiếu chuyển Chờ TP duyệt, Trưởng phòng nhận thông báo; hệ thống về danh sách.'),
            ('sub', 'Hoặc {icon:btn_luunhap} để lưu nháp (Đang tạo — chỉ bắt buộc Ghi chú, chưa gửi ai duyệt).'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu nháp rồi lập tiếp phiếu khác.'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lưu.'),
            ('sub2', 'Thiếu thông tin bắt buộc thì ô lỗi viền đỏ, ghi "Bắt buộc phải nhập", phiếu chưa được lưu:'),
            ('img', '11_validate', 'Báo lỗi khi Gửi duyệt thiếu thông tin'),
        ]),
        ('SỬA PHIẾU', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_sua} ở cột Hành động của phiếu mình lập đang ở trạng thái Đang tạo hoặc Không duyệt.'),
            ('img', '12_edit', 'Trang Sửa phiếu yêu cầu mua dịch vụ'),
            ('step', 'Bước 3: Sửa Ghi chú, file đính kèm, dòng dịch vụ, VAT (quy tắc nhập như khi lập). Phiếu Không duyệt có hiện ý kiến Trưởng phòng / Ban kiểm soát là lý do bị từ chối.'),
            ('step', 'Bước 4: Bấm {icon:btn_guiduyet} để gửi duyệt lại, hoặc {icon:btn_luunhap} để lưu nháp (phiếu Không duyệt lưu nháp sẽ về Đang tạo).'),
            ('sub', 'Hoặc {icon:btn_quaylai} nếu muốn hủy.'),
        ]),
        ('XEM CHI TIẾT PHIẾU', [
            ('step', VAO),
            ('step', CT),
            ('img', '17_detail', 'Trang Chi tiết phiếu Đã duyệt'),
            ('step', 'Bước 3: Xem Ghi chú, ý kiến duyệt, file đính kèm (bấm biểu tượng mắt để xem, mũi tên để tải), Danh sách dịch vụ. Từ Chờ KS duyệt trở đi có thêm cột Giá duyệt, Thành tiền duyệt.'),
            ('step', 'Bước 4: Dùng các nút ở chân trang (chỉ hiện nút bạn được dùng), hoặc {icon:btn_quaylai} để về danh sách.'),
        ]),
        ('XÓA PHIẾU', [
            ('step', 'Bước 1: Mở trang Chi tiết phiếu mình lập ở trạng thái Đang tạo hoặc Không duyệt (bấm Số phiếu, hoặc {icon:btn_xoa} ở cột Hành động).'),
            ('step', 'Bước 2: Bấm {icon:btn_xoa_footer} ở chân trang. Hệ thống hiện hộp "Xác nhận xóa"'),
            ('img', '13_delete', 'Hộp Xác nhận xóa phiếu'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_xoa} để xác nhận. Phiếu và các dòng dịch vụ bị xóa, hệ thống về danh sách.'),
            ('sub', 'Hoặc bấm {icon:btn_huy_confirm} nếu bấm nhầm.'),
        ]),
        ('TRƯỞNG PHÒNG DUYỆT PHIẾU', [
            ('step', 'Bước 1: Bấm thông báo "[YCMDV] Chờ duyệt" hoặc mở phiếu Chờ TP duyệt (bấm Số phiếu).'),
            ('img', '30_detail_wait_tp', 'Trang Chi tiết phiếu Chờ TP duyệt'),
            ('step', 'Bước 2: Bấm {icon:btn_tpduyet}'),
            ('img', '31_tp_modal', 'Cửa sổ Trưởng phòng duyệt'),
            ('step', 'Bước 3: Nhập Ý kiến Trưởng phòng (không bắt buộc), bấm {icon:btn_duyet_modal}. Phiếu chuyển Chờ KS duyệt, Ban kiểm soát nhận thông báo.'),
            ('sub2', 'Nếu bạn (hoặc nhân viên phòng bạn quản lý) còn hàng quá hạn theo quy định, hệ thống chặn và hiện danh sách hàng quá hạn cần xử lý trước.'),
            HUY,
        ]),
        ('BAN KIỂM SOÁT DUYỆT GIÁ', [
            ('step', 'Bước 1: Bấm thông báo "[YCMDV] Chờ duyệt" hoặc mở phiếu Chờ KS duyệt cùng công ty.'),
            ('step', 'Bước 2: Kiểm tra Danh sách dịch vụ, bấm {icon:btn_ksduyet}'),
            ('img', '34_ks_modal', 'Cửa sổ Ban kiểm soát duyệt giá'),
            ('step', 'Bước 3: Nhập Ý kiến Ban kiểm soát (không bắt buộc), bấm {icon:btn_duyetgia_modal}. Phiếu chuyển Đã duyệt; hệ thống ghi Người duyệt giá, Ngày duyệt giá.'),
            HUY,
        ]),
        ('TỪ CHỐI PHIẾU', [
            ('step', 'Bước 1: Mở phiếu Chờ TP duyệt (Trưởng phòng) hoặc Chờ KS duyệt (Ban kiểm soát).'),
            ('step', 'Bước 2: Bấm {icon:btn_tuchoi}'),
            ('img', '32_reject_modal', 'Cửa sổ Từ chối — lý do bắt buộc'),
            ('step', 'Bước 3: Nhập Lý do từ chối (bắt buộc), bấm {icon:btn_tuchoi_modal}. Phiếu chuyển Không duyệt, người lập nhận thông báo kèm lý do.'),
            HUY,
        ]),
        ('YÊU CẦU DUYỆT LẠI GIÁ, HỦY YÊU CẦU, LẬP HỢP ĐỒNG', [
            ('step', 'Bước 1: Mở phiếu Đã duyệt do mình lập.'),
            ('img', '35_detail_approved_owner', 'Các nút của người lập khi phiếu Đã duyệt'),
            ('step', 'Bước 2: Bấm {icon:btn_duyetlai} để xin Ban kiểm soát duyệt lại giá: phiếu về Chờ KS duyệt ngay (không hỏi lại).'),
            ('step', 'Bước 3: Hoặc bấm {icon:btn_huyyc}, nhập Lý do hủy (không bắt buộc), bấm Hủy yêu cầu trong cửa sổ để hủy phiếu.'),
            ('img', '36_cancel_modal', 'Cửa sổ Hủy yêu cầu mua dịch vụ'),
            ('step', 'Bước 4: Hoặc bấm {icon:btn_laphd} để mở màn lập Hợp đồng mua dịch vụ (tab mới) cho phiếu này. Khi hợp đồng được lập, phiếu tự chuyển Đang lập hợp đồng / Đã lập hợp đồng.'),
        ]),
        ('IN PHIẾU', [
            ('step', 'Bước 1: Bấm {icon:btn_inphieu} ở chân trang Chi tiết (hoặc In phiếu ở cột Hành động).'),
            ('img', '19b_printdetail', 'Cửa sổ xem trước phiếu'),
            ('step', 'Bước 2: Bấm {icon:btn_in} để in. Phiếu Đã duyệt in thêm cột Giá duyệt, Thành tiền duyệt.'),
        ]),
        ('IN DANH SÁCH', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_indanhsach}. Hệ thống mở cửa sổ xem trước "Danh sách yêu cầu mua dịch vụ".'),
            ('img', '19_printlist', 'Cửa sổ xem trước bản in danh sách'),
            ('step', 'Bước 3: Bấm {icon:btn_in} để in. Danh sách quá 2,000 dòng thì cần lọc hẹp lại hoặc dùng Xuất Excel.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất file".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất file'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất (danh_sach_yeu_cau_mua_dich_vu.xlsx).'),
        ]),
        ('XEM LỊCH SỬ THAY ĐỔI', [
            ('p', 'Cách 1: Xem từ màn danh sách:'),
            ('step', 'Ở cột Hành động, bấm {icon:btn_lichsu_row} (có thể nằm trong menu "…")'),
            ('img', '16_history', 'Cửa sổ Lịch sử thay đổi'),
            ('p', 'Cách 2: Xem từ màn chi tiết:'),
            ('step', 'Bước 1: Bấm vào Số phiếu để mở trang Chi tiết'),
            ('step', 'Bước 2: Tại khối Lịch sử cuối trang, bấm {icon:btn_xemlichsu}'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột (STT, Số phiếu luôn hiện).'),
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
