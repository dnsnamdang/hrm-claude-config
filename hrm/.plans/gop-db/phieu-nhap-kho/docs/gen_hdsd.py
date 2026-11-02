# -*- coding: utf-8 -*-
"""HDSD_Phiếu nhập kho — bản GỌN form quốc gia (chép khuôn finance-declare-debt-beginning/docs/kh/gen_hdsd.py).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Phiếu nhập kho'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Phiếu nhập kho', 'Chứng từ thủ kho nhập hàng vào vị trí kho, mã PNK-xxxxx, lập từ 1 đề nghị nhập kho đang chờ duyệt.'],
        ['Đề nghị nhập kho', 'Chứng từ nguồn của phiếu nhập kho (màn Đề nghị nhập kho).'],
        ['Thủ kho / Kế toán kho', 'Thủ kho tạo phiếu, đi xếp hàng, nhập kho. Kế toán kho xử lý phiếu Chờ duyệt.'],
        ['Vị trí dự kiến / thực', 'Vị trí chọn khi tạo phiếu / vị trí nhập thực tế ở bước Nhập kho.'],
        ['Phiếu đi xếp hàng', 'Nhóm dòng hàng giao cho 1 người đi xếp.'],
        ['Lưu và nhập', 'Gửi phiếu: cộng tồn kho, phiếu chuyển Chờ duyệt.'],
        ['Xuất lại / Nhập lại', 'Đưa toàn bộ hàng của phiếu bị Không duyệt ra khỏi kho / lập phiếu nhập mới cho phiếu đã xuất lại.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Màn hình không cần quyền riêng để vào. Mỗi người thấy phiếu do mình tạo; thêm phạm vi theo quyền "Xem phiếu nhập kho theo tổng công ty / công ty / phòng ban", thủ kho thấy phiếu kho mình, kế toán kho thấy phiếu đã gửi của công ty mình.',
        'Thủ kho của kho nhập: tạo phiếu, lập phiếu đi xếp hàng, nhập kho, hủy, xuất lại, nhập lại (với phiếu mình tạo).',
        'Kế toán kho (quyền "Kế toán kho") cùng công ty với phiếu: Tạo phiếu nhập hàng hoặc Không duyệt phiếu Chờ duyệt.',
        'Luồng: Tạo phiếu (Đang tạo) → Phiếu xếp hàng → Nhập kho → Lưu và nhập (cộng tồn, Chờ duyệt) → kế toán kho lập phiếu nhập hàng (Đang hạch toán → Đã hạch toán) hoặc Không duyệt → Xuất lại → Nhập lại.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Tài chính {icon:menu_phanhe}, tại menu Hàng hoá - Dịch vụ - Vận chuyển {icon:menu_nhom}, nhóm Nhập hàng, chọn Phiếu nhập kho {icon:menu_muc}'),
            ('sub', 'Hoặc từ phân hệ Kho, menu Nhập kho, chọn "Phiếu nhập kho" (cùng màn hình).'),
            ('img', '01_list', 'Màn hình danh sách Phiếu nhập kho'),
            ('step', 'Bước 2: Nhập mã phiếu vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, chọn giá trị ở {icon:o_kho}'),
            ('sub', 'Hoặc nhập {icon:o_hanghoa}, {icon:o_maphieu}, {icon:o_dnnk} rồi nhấn Enter'),
            ('sub', 'Hoặc chọn {icon:o_loai}, {icon:o_ncc}, {icon:o_trangthai}'),
            ('sub', 'Hoặc chọn {icon:o_nguoidenghi}, {icon:o_nguoiyeucau}, {icon:o_nguoitao}, {icon:o_nguoiduyet}'),
            ('sub', 'Hoặc chọn khoảng ngày {icon:o_ngaytao}; Công ty / Phòng ban chỉ hiện với người có quyền xem rộng'),
            ('sub2', 'Kế toán kho chọn Trạng thái = Chờ duyệt để xem các phiếu cần xử lý.'),
            ('img', '02_filter', 'Khu vực Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
        ]),
        ('TẠO PHIẾU NHẬP KHO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi}. Hệ thống mở trang "Dự kiến vị trí".'),
            ('sub', 'Hoặc tại màn Đề nghị nhập kho bấm "Tạo phiếu nhập kho" — trang mở sẵn đề nghị đó.'),
            ('img', '10_create', 'Trang Dự kiến vị trí'),
            ('step', 'Bước 3: Bấm ô {icon:o_chondnnk} và chọn 1 đề nghị (chỉ có đề nghị Chờ duyệt của kho bạn là thủ kho).'),
            ('img', '14_picker', 'Cửa sổ Chọn phiếu đề nghị nhập kho'),
            ('step', 'Bước 4: Nhập thông tin:'),
            ('sub2', 'Bắt buộc: Người giao hàng; Vị trí và SL nhập cho từng dòng hàng (bấm ô Vị trí để chọn; tích "Áp dụng tất cả" để dùng 1 vị trí cho mọi dòng; "Thêm vị trí" để chia 1 hàng ra nhiều vị trí).'),
            ('sub2', 'Tùy chọn: Ghi chú; tab Vận chuyển (chọn Công ty vận chuyển thì bắt buộc chọn chuyến xe — "Thêm chuyến" hoặc "Tạo chuyến xe"); tab Bốc xếp (chọn Loại hình thuê thì nhập Loại bốc xếp, Khối lượng / Số giờ; Công ty thì thêm người nhận việc).'),
            ('sub2', 'Tự điền: Loại phiếu (tiêu đề khối), Kho nhập, Người đề nghị, Ghi chú, bảng hàng hoá và SL đề nghị theo đề nghị; tồn tại vị trí; Đơn giá và Số tiền bốc xếp.'),
            ('sub2', 'Tổng SL các vị trí không được vượt SL đề nghị; vị trí đang kiểm kho không chọn được.'),
            ('img', '10b_create_filled', 'Đã chọn đề nghị, nhập người giao hàng và vị trí dự kiến'),
            ('img', '10d_create_bocxep', 'Tab Bốc xếp'),
            ('step', 'Bước 5: Bấm {icon:btn_luu}. Phiếu ở trạng thái Đang tạo – Đang đi xếp hàng, đề nghị nhập kho chuyển Đang nhập kho. Lúc này CHƯA cộng tồn kho.'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu rồi tạo tiếp phiếu khác.'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lưu; đã nhập dữ liệu thì bấm {icon:btn_thoat} để thoát hoặc {icon:btn_olai} để ở lại.'),
        ]),
        ('LẬP PHIẾU ĐI XẾP HÀNG', [
            ('step', VAO),
            ('step', 'Bước 2: Ở phiếu Đang đi xếp hàng, bấm {icon:btn_xephang} (trong menu ba chấm của dòng hoặc ở trang Chi tiết).'),
            ('img', '30_arrange', 'Trang Phiếu đi xếp hàng'),
            ('step', 'Bước 3: Bấm {icon:btn_themphieuxep} nếu cần chia nhiều phiếu; kéo dòng hàng sang phiếu khác.'),
            ('step', 'Bước 4: Mỗi phiếu chọn Người đi xếp (thủ kho của kho nhập).'),
            ('step', 'Bước 5: Bấm {icon:btn_luuxephang}. Bấm {icon:btn_in_nhom} ở từng phiếu để in phiếu xếp hàng.'),
            ('step', 'Bước 6: Xếp xong bấm {icon:btn_nhapkho_xh} để sang bước Nhập kho (còn dòng chưa có người đi xếp thì hệ thống báo và ở lại).'),
        ]),
        ('NHẬP KHO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_nhapkho} ở dòng phiếu (phiếu đã lưu nhập kho trước đó thì nút là "Sửa phiếu").'),
            ('img', '40_import', 'Trang Nhập kho'),
            ('step', 'Bước 3: Kiểm tra / sửa SL nhập và vị trí thực từng dòng (vị trí chỉ bắt buộc khi SL > 0).'),
            ('step', 'Bước 4: Bấm "Thêm tài liệu" ở khối File đính kèm để chọn file (bắt buộc ít nhất 1 file; pdf, ảnh, Word, Excel; tối đa 20MB/file).'),
            ('step', 'Bước 5: Tab Vận chuyển (nếu Công ty vận chuyển): chọn Tuyến đường, nhập Số km chốt; km chốt khác km dự kiến thì nhập Ghi chú vận chuyển.'),
            ('img', '40b_import_vanchuyen', 'Tab Vận chuyển ở bước Nhập kho'),
            ('step', 'Bước 6: Bấm {icon:btn_luuvanhap}. Hệ thống cộng tồn kho theo vị trí, phiếu chuyển Chờ duyệt và báo kế toán kho.'),
            ('sub', 'Hoặc {icon:btn_luu} để lưu tạm (chưa cộng tồn), hoặc {icon:btn_indukien} để xem trước bản in.'),
            ('sub2', 'Chuyến xe chưa duyệt thì chưa "Lưu và nhập" được — duyệt chuyến xe trước.'),
        ]),
        ('XEM CHI TIẾT PHIẾU', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm vào Mã phiếu. Hệ thống mở trang "Chi tiết phiếu nhập kho" kèm trạng thái trên tiêu đề.'),
            ('img', '20_detail', 'Trang Chi tiết phiếu Chờ duyệt'),
            ('step', 'Bước 3: Xem các tab Thông tin chung, Vận chuyển, Bốc xếp, file đính kèm, bảng hàng hoá; bấm nút ở thanh dưới để thao tác hoặc {icon:btn_quaylai} để về danh sách.'),
        ]),
        ('HỦY PHIẾU', [
            ('step', 'Bước 1: Ở phiếu Đang tạo do bạn tạo, bấm {icon:btn_huy}.'),
            ('step', 'Bước 2: Hệ thống hiện hộp "Xác nhận hủy"'),
            ('img', '13_cancel', 'Hộp Xác nhận hủy'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_huy}. Phiếu chuyển Đã hủy, đề nghị nhập kho nguồn cũng bị hủy.'),
            ('sub', 'Hoặc bấm {icon:btn_dong_confirm} nếu bấm nhầm.'),
        ]),
        ('KHÔNG DUYỆT PHIẾU (KẾ TOÁN KHO)', [
            ('step', 'Bước 1: Lọc Trạng thái = Chờ duyệt, ở phiếu cần từ chối bấm {icon:btn_khongduyet}.'),
            ('img', '15_deny', 'Hộp Không duyệt phiếu nhập kho'),
            ('step', 'Bước 2: Nhập Lý do không duyệt (bắt buộc, tối đa 255 ký tự).'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_khongduyet}. Phiếu chuyển Không duyệt, người tạo nhận thông báo. Tồn kho chưa bị trừ — người tạo cần lập phiếu xuất lại.'),
            ('sub', 'Hoặc bấm {icon:btn_dong_confirm} để đóng.'),
        ]),
        ('TẠO PHIẾU NHẬP HÀNG (KẾ TOÁN KHO)', [
            ('step', 'Bước 1: Ở phiếu Chờ duyệt, bấm {icon:btn_taophieunhaphang}.'),
            ('step', 'Bước 2: Hệ thống mở trang Thêm phiếu nhập hàng đã chọn sẵn phiếu nhập kho; lập phiếu nhập hàng theo hướng dẫn màn Phiếu nhập hàng.'),
            ('img', '70_create_product_import', 'Trang Thêm phiếu nhập hàng mở từ phiếu nhập kho'),
            ('step', 'Bước 3: Lưu phiếu nhập hàng thì phiếu nhập kho chuyển Đang hạch toán; phiếu nhập hàng hoàn thành thì chuyển Đã hạch toán.'),
        ]),
        ('TẠO PHIẾU XUẤT LẠI', [
            ('step', 'Bước 1: Ở phiếu Không duyệt do bạn tạo, bấm {icon:btn_xuatlai_row}.'),
            ('img', '50_reexport', 'Trang Tạo phiếu xuất lại'),
            ('step', 'Bước 2: Nhập Ghi chú (nếu có), bấm {icon:btn_xuatlai}.'),
            ('img', '51_reexport_confirm', 'Hộp Xác nhận xuất lại'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_xuatlai}. Toàn bộ hàng của phiếu bị trừ khỏi tồn kho (đúng lô, đúng vị trí), phiếu chuyển Đã xuất lại. Thao tác không hoàn tác được.'),
            ('sub2', 'Hàng ở vị trí nào không đủ tồn thì hệ thống báo, không trừ gì.'),
        ]),
        ('TẠO PHIẾU NHẬP LẠI', [
            ('step', 'Bước 1: Ở phiếu Đã xuất lại do bạn tạo, bấm {icon:btn_nhaplai_row}.'),
            ('img', '55_reimport', 'Trang Tạo phiếu nhập lại'),
            ('step', 'Bước 2: Nhập SL, vị trí, chọn file đính kèm mới (bắt buộc), vận chuyển, bốc xếp như bước Nhập kho; Người giao hàng giữ theo phiếu gốc.'),
            ('step', 'Bước 3: Bấm {icon:btn_luuvanhap} (hoặc {icon:btn_luu}). Hệ thống tạo phiếu nhập kho mới "Nhập lại cho phiếu <mã gốc>"; phiếu gốc chuyển Đã nhập lại.'),
        ]),
        ('IN PHIẾU NHẬP KHO', [
            ('step', 'Bước 1: Bấm {icon:btn_inphieu} ở dòng phiếu hoặc trang Chi tiết.'),
            ('img', '19_print', 'Cửa sổ xem trước phiếu nhập kho'),
            ('step', 'Bước 2: Bấm {icon:btn_in} để in.'),
        ]),
        ('IN BARCODE LÔ HÀNG', [
            ('step', 'Bước 1: Ở phiếu đã nhập kho, bấm {icon:btn_inbarcode}.'),
            ('img', '60_barcode', 'Trang In barcode'),
            ('step', 'Bước 2: Chọn Nhà cung cấp, Năm sản xuất, Khổ giấy; mỗi dòng chọn Mẫu in, Ngày sản xuất, Hạn sử dụng, Số lượng in.'),
            ('step', 'Bước 3: Bấm {icon:btn_bc_full}, {icon:btn_bc} hoặc {icon:btn_bc_sub}, rồi bấm In ở cửa sổ xem trước.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất (danh_sach_phieu_nhap_kho.xlsx).'),
        ]),
        ('XEM LỊCH SỬ THAY ĐỔI', [
            ('p', 'Cách 1: Xem từ màn danh sách:'),
            ('step', 'Ở cột Hành động, bấm {icon:btn_lichsu_row} (trong menu ba chấm)'),
            ('img', '16_history', 'Cửa sổ Lịch sử thay đổi'),
            ('p', 'Cách 2: Xem từ màn chi tiết:'),
            ('step', 'Bước 1: Bấm vào mã phiếu để mở trang Chi tiết'),
            ('step', 'Bước 2: Tại khối Lịch sử cuối trang, bấm "Xem lịch sử" để mở các mốc.'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột.'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca_cot} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet_cot} để ẩn tất cả các cột (trừ các cột bắt buộc).'),
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
