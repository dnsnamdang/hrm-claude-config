# -*- coding: utf-8 -*-
"""HDSD_Khai báo tồn kho đầu kỳ — bản GỌN form quốc gia (khuôn màn mẫu phiếu finance-declare-debt-beginning/docs/kh/).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402

TEN = 'Khai báo tồn kho đầu kỳ'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập vào màn hình %s.' % TEN

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Khai báo tồn kho đầu kỳ', 'Số lượng tồn thực tế của 1 hàng tại 1 vị trí trong 1 kho của 1 công ty khi bắt đầu dùng hệ thống; mỗi dòng danh sách là 1 hàng × 1 vị trí.'],
        ['Nhóm khai báo', 'Mọi vị trí đã khai của cùng hàng tại cùng kho, cùng công ty. Sửa và Xóa luôn áp cho cả nhóm.'],
        ['SL tồn kế toán', 'Số đã khai tồn kho kế toán đầu kỳ của hàng tại kho. Tổng số lượng các vị trí phải bằng số này.'],
        ['Chưa có giao dịch', 'Hàng tại kho chưa có nhập, xuất, điều chuyển nào khác — còn Sửa, Xóa được.'],
        ['Đã có giao dịch', 'Hàng tại kho đã có giao dịch kho (kể cả phiếu nháp lấy từ hàng tồn đầu) — chỉ còn xem, không Sửa, không Xóa.'],
    ],
    'phien_ban': [['1.0', L.NGAY, 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Người dùng có quyền "Khai báo tồn kho đầu kỳ" (phân hệ Kho, nhóm Tồn kho đầu kỳ) được dùng mọi chức năng của màn hình: xem, tìm kiếm, tạo mới, sửa, xóa, xuất Excel, import Excel, tùy chỉnh cột.',
        'Người dùng chỉ xem và khai báo cho các công ty mình được làm việc; quản trị cao nhất xem được mọi công ty (có thêm cột và ô lọc Công ty).',
        'Khai báo không qua bước duyệt: lưu xong là có hiệu lực và đã cộng vào tồn kho thực tế của kho, vị trí.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Kho {icon:menu_phanhe}, tại menu Tồn kho đầu kỳ {icon:menu_nhom}, chọn Khai báo tồn kho đầu kỳ {icon:menu_muc}'),
            ('img', '01_list', 'Màn hình danh sách Khai báo tồn kho đầu kỳ'),
            ('step', 'Bước 2: Nhập mã hoặc tên hàng vào ô tìm kiếm nhanh {icon:o_timnhanh}'),
            ('step', 'Bước 3: Nhấn {icon:btn_timkiem}'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiemnangcao}, nhập {icon:o_mahang} rồi nhấn Enter để lọc theo mã hàng'),
            ('sub', 'Hoặc chọn giá trị {icon:o_kho} để lọc theo kho'),
            ('sub', 'Hoặc nhập mã / tên vị trí ở {icon:o_vitri} rồi nhấn Enter'),
            ('sub', 'Hoặc chọn giá trị {icon:o_nguoitao} để lọc theo người tạo'),
            ('sub', 'Hoặc chọn {icon:o_congty} (chỉ hiện với người xem được mọi công ty)'),
            ('img', '02_filter', 'Vùng Tìm kiếm nâng cao'),
            ('step', 'Bước 5: Chọn {icon:btn_lammoi} để xóa giá trị đã lọc'),
            ('step', 'Bước 6: Bấm {icon:btn_caidatboloc} để chọn ô lọc hiển thị và thứ tự ô lọc, bấm Lưu để áp dụng.'),
        ]),
        ('THÊM KHAI BÁO TỒN KHO ĐẦU KỲ', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_taomoi}'),
            ('img', '10_create', 'Trang Thêm khai báo tồn kho đầu kỳ'),
            ('step', 'Bước 3: Chọn Kho và Công ty (bắt buộc). Kho phải có kho kế toán của công ty đã chọn.'),
            ('sub2', 'Đã có hàng trong bảng mà đổi Kho hoặc Công ty, hệ thống hỏi xác nhận; bấm {icon:btn_dongy} thì danh sách hàng bị xóa, bấm {icon:btn_huy_doikho} để giữ nguyên.'),
            ('step', 'Bước 4: Bấm {icon:btn_chonhang}. Hệ thống mở cửa sổ "Chọn hàng hóa khai báo tồn đầu".'),
            ('img', '14_picker', 'Cửa sổ Chọn hàng hóa khai báo tồn đầu'),
            ('step', 'Bước 5: Tìm và tích chọn một hoặc nhiều hàng, bấm {icon:btn_them_popup}'),
            ('sub2', 'Chỉ thêm được hàng đã khai tồn kho kế toán đầu kỳ tại kho này và chưa khai tồn đầu; hàng không hợp lệ hệ thống báo lỗi theo từng hàng (ví dụ "Hàng hóa đã được khai báo tồn đầu kì").'),
            ('step', 'Bước 6: Nhập thông tin từng hàng:'),
            ('sub2', 'Tự điền: Tên hàng, Model, Mã hàng, ĐVT và SL tồn kế toán (theo khai báo tồn kho kế toán, không sửa được); dòng vị trí đầu có sẵn Số lượng bằng SL tồn kế toán.'),
            ('sub2', 'Bắt buộc: Vị trí (bấm vào ô để mở cửa sổ "Chọn vị trí kho", bấm vào mã vị trí để chọn) và Số lượng (lớn hơn 0).'),
            ('sub2', 'Hàng để ở nhiều vị trí: bấm {icon:btn_themvitri} — dòng mới tự điền phần số lượng còn thiếu; không chọn trùng vị trí trong cùng một hàng.'),
            ('sub2', 'Tổng số lượng các vị trí phải BẰNG SL tồn kế toán; lệch thì ô Số lượng báo đỏ "Tổng số lượng phải bằng SL tồn kế toán".'),
            ('img', '10c_create_mismatch', 'Hàng chia 2 vị trí, tổng 9 khác SL tồn kế toán 10 nên báo đỏ'),
            ('step', 'Bước 7: Bấm {icon:btn_luu} để lưu và về danh sách. Mỗi vị trí thành 1 dòng khai báo và được cộng ngay vào tồn kho của kho, vị trí.'),
            ('sub', 'Hoặc {icon:btn_luutieptuc} để lưu rồi khai tiếp.'),
            ('sub', 'Hoặc {icon:btn_quaylai} để không lưu; đã nhập dữ liệu thì bấm {icon:btn_thoat} để thoát hoặc {icon:btn_olai} để ở lại.'),
        ]),
        ('SỬA KHAI BÁO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_sua} ở cột Hành động của dòng cần sửa (chỉ có khi hàng Chưa có giao dịch tại kho).'),
            ('img', '12_edit', 'Trang Sửa khai báo tồn kho đầu kỳ'),
            ('step', 'Bước 3: Sửa Số lượng từng vị trí. Trang Sửa liệt kê mọi vị trí đã khai của hàng tại kho; Hàng hóa, Đơn vị, Kho, Vị trí không sửa được. Tổng số lượng vẫn phải bằng SL tồn kế toán.'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để lưu; tồn kho của các vị trí được điều chỉnh theo.'),
            ('sub', 'Hoặc {icon:btn_quaylai} nếu muốn hủy.'),
        ]),
        ('XÓA KHAI BÁO', [
            ('step', 'Bước 1: Bấm {icon:btn_xoa} ở cột Hành động của dòng cần xóa (chỉ có khi hàng Chưa có giao dịch tại kho).'),
            ('step', 'Bước 2: Hệ thống hiện hộp "Xác nhận xóa" — thao tác xóa TẤT CẢ vị trí của hàng tại kho đó.'),
            ('img', '13_delete', 'Hộp Xác nhận xóa khai báo'),
            ('step', 'Bước 3: Bấm {icon:btn_confirm_xoa} để xác nhận. Các dòng khai báo của hàng tại kho bị xóa và tồn kho được trừ lại.'),
            ('sub', 'Hoặc bấm {icon:btn_huy_confirm} nếu bấm nhầm.'),
        ]),
        ('XUẤT DANH SÁCH RA EXCEL', [
            ('step', 'Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).'),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ "Chọn trường xuất Excel".'),
            ('img', '20_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('step', 'Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.'),
            ('sub', 'Hoặc bấm {icon:btn_chontatca} / {icon:btn_bochonhet} để chọn / bỏ chọn nhanh.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuatfile}'),
            ('step', 'Bước 5: Mở file Excel đã xuất (Khai_bao_ton_dau_vat_ly.xlsx).'),
        ]),
        ('IMPORT KHAI BÁO TỪ FILE EXCEL', [
            ('step', 'Bước 1: Tại màn hình danh sách, bấm {icon:btn_import}. Hệ thống mở cửa sổ "Import khai báo tồn kho đầu kỳ".'),
            ('img', '21_import_open', 'Cửa sổ Import khi vừa mở'),
            ('step', 'Bước 2: Bấm {icon:btn_taifilemau} để lấy file mẫu'),
            ('step', 'Bước 3: Điền dữ liệu vào file mẫu, mỗi dòng 1 hàng tại 1 vị trí, mỗi lần tối đa 200 dòng:'),
            ('sub2', 'Bắt buộc tất cả các cột: Tên hàng, Mã hàng (đúng mã và tên trong hệ thống), ĐVT, Mã kho, Mã vị trí, Số lượng (lớn hơn 0), Mã công ty.'),
            ('sub2', 'Các dòng cùng hàng + kho + công ty được tính chung: tổng số lượng phải bằng SL tồn kế toán; một dòng lỗi thì cả nhóm không được nhập.'),
            ('step', 'Bước 4: Bấm {icon:btn_chonfile}, chọn file vừa điền'),
            ('step', 'Bước 5: Bấm {icon:btn_load}'),
            ('step', 'Bước 6: Bấm {icon:btn_validate} để hệ thống kiểm tra từng dòng.'),
            ('img', '23_import_validated', 'Kết quả kiểm tra — mỗi dòng lỗi nêu rõ lý do'),
            ('step', 'Bước 7:'),
            ('sub2', 'Sửa trực tiếp các dòng lỗi trên bảng rồi bấm Validate lại.'),
            ('sub2', 'Nếu không muốn nhập các dòng lỗi thì bấm {icon:btn_bodongloi}'),
            ('sub2', 'Muốn sửa lại những dòng đã khoá, bấm {icon:btn_xoavalidate}'),
            ('step', 'Bước 8: Bấm {icon:btn_import_modal}. Hệ thống báo số dòng nhập thành công và tải lại danh sách.'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Ở màn danh sách, bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột (STT, Tên hàng, Hành động luôn hiện).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột bắt buộc).'),
            ('step', 'Bước 4: Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.'),
            ('step', 'Bước 5: Bấm Lưu để áp dụng, hoặc Đóng nếu muốn bỏ thay đổi.'),
        ]),
    ],
}

if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', L.build_hdsd(scr, H, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))
