# -*- coding: utf-8 -*-
"""HDSD_Báo cáo chi tiết chuyến xe — bản GỌN + PHẦN "ĐỌC BÁO CÁO" (khuôn sale-customer-debt-reports/docs/compare/gen_hdsd.py).
Ảnh + icon: hdsd_shots/ (capture.js; 13_read_zoom.png do make_zoom.py cắt). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'hieu-qua-gop-xe'))
import _trp_docs as D  # noqa: E402
from _trp_docs import L  # noqa: E402

TEN = 'Báo cáo chi tiết chuyến xe'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập màn hình %s, chọn kỳ cần xem (xem PHẦN 1).' % TEN

COT = [
    ['Cột', 'Ý nghĩa / lấy số từ đâu'],
    ['TỔNG (dòng đầu bảng)', 'Cộng mọi chuyến theo bộ lọc (mọi trang), mỗi chuyến tính 1 lần.'],
    ['Khách hàng / Tuyến đường / Phiếu hạch toán', 'Dòng I, II… là khách hàng (cước sau thuế giảm dần, "Không có khách hàng" cuối); 1, 2… là tuyến đường; 1.1, 1.2… là phiếu hạch toán (1 chuyến), dòng phụ ghi ngày vận chuyển và mã chuyến xe.'],
    ['Số phiếu HT', 'Số phiếu hạch toán (số chuyến) của khách / tuyến. Bấm để xem các phiếu nhập/xuất (PHẦN 3).'],
    ['Xe, Lái xe', 'Biển số xe và lái xe của chuyến (mã lái xe ở dòng phụ).'],
    ['KM, KM phụ trội', 'Km thực tế và km phụ trội ghi trên chuyến (km âm hiển thị 0).'],
    ['Cước chính, Cước phụ trội', 'Cước tính theo công thức vận chuyển và cước của km phụ trội.'],
    ['Cước thực tế, Thuế', 'Phần cước, thuế của khách: cộng số kế toán đã chia cho các phiếu xuất / nhập của khách khi hạch toán chuyến.'],
    ['Cước sau thuế', 'Cước thực tế + Thuế.'],
    ['Vé cầu đường', 'Vé cầu đường ghi trên chuyến.'],
    ['NVKD', 'Người lập yêu cầu xuất / nhập hàng của các phiếu.'],
    ['NV chịu, Công ty chịu', 'Dấu ✓ cho biết ai chịu phí vận chuyển.'],
]

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Chuyến', 'Một phiếu hạch toán chuyến xe của chuyến xe đã hoàn thành.'],
        ['Kỳ', 'Khoảng thời gian xem báo cáo, tính theo ngày tạo chuyến (ngày vận chuyển).'],
        ['Phiếu nhập/xuất', 'Phiếu xuất kho / nhập kho chở trên chuyến.'],
        ['Chuyến ghép', 'Chuyến chở hàng của từ 2 khách trở lên, có nhãn "ghép N KH".'],
        ['NVKD', 'Nhân viên kinh doanh lập yêu cầu xuất / nhập hàng.'],
    ],
    'phien_ban': [['1.0', '18/11/2026', 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng đăng nhập đều mở được màn hình và dùng mọi chức năng.',
        'Số liệu được xem tùy quyền: "Xem báo cáo vận chuyển" hoặc "Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh" mức Tổng công ty xem mọi chuyến; mức Công ty xem chuyến của công ty mình; quyền chi phí vận chuyển theo nhân viên kinh doanh mức Phòng ban xem chuyến của phòng ban mình; không có quyền thì chỉ xem chuyến do mình lập.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Vận chuyển {icon:menu_phanhe}, tại menu Báo cáo vận chuyển {icon:menu_nhom}, chọn Báo cáo chi tiết chuyến xe {icon:menu_muc}'),
            ('img', '01_open', 'Màn hình Báo cáo chi tiết chuyến xe khi mới mở'),
            ('step', 'Bước 2: Chọn kỳ ở ô {icon:o_ky} (chọn Tuỳ chọn thì chọn thêm Từ ngày, Đến ngày).'),
            ('step', 'Bước 3: Chọn cách xem ở ô {icon:o_xemtheo}: Khách hàng (cước của từng khách) hoặc Chuyến xe (từng chuyến và các phiếu nhập/xuất).'),
            ('step', 'Bước 4: Lọc thêm (tùy chọn):'),
            ('sub', 'Chọn {icon:o_congty}, {icon:o_tuyen}, {icon:o_bienso}, {icon:o_doituong}, {icon:o_phongban}, {icon:o_bophan}, {icon:o_nvkd}: báo cáo tự tải lại.'),
            ('sub', 'Hoặc nhập {icon:o_phieuht}, {icon:o_chuyenxe}, {icon:o_laixe}, {icon:o_phieunx} rồi nhấn Enter.'),
            ('step', 'Bước 5: Bấm {icon:btn_timkiem} để tải lại báo cáo,'),
            ('sub', 'Hoặc bấm {icon:btn_xoaloc} để đưa mọi ô lọc về mặc định.'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('p', 'Đầu trang là khối tổng hợp (Chuyến xe, Đối tượng chịu phí, Cước vận chuyển). Khi xem theo Khách hàng, bảng gồm dòng TỔNG, từng khách hàng, tuyến đường của khách và từng phiếu hạch toán; ô {icon:o_capbung} chọn bung đến mức nào.'),
            ('img', '03_report', 'Báo cáo kỳ Tháng trước (tháng 10/2026), xem theo Khách hàng'),
            ('table', COT, [1.9, 4.6]),
            ('img', '13_read_zoom', 'Phóng to cột Cước thực tế, Thuế, Cước sau thuế của khách hàng I, II khi bung đến từng phiếu hạch toán'),
            ('p', '**Ví dụ đọc số từ ảnh phóng to:**'),
            ('sub2', 'Cước sau thuế = Cước thực tế + Thuế: 6,520,000 + 521,600 = 7,041,600 (khách I).'),
            ('sub2', 'Chuyến TPE_HTCXCH_03203 có nhãn "ghép 2 KH": cước cả chuyến được chia cho 2 khách I và II: 6,520,000 + 6,507,164 = 13,027,164. Các cột KM, Cước chính, Cước phụ trội, Vé cầu đường của chuyến này để trống ở dòng khách.'),
            ('img', '13b_read_zoom', 'Phóng to nhóm khách hàng VII (cùng kỳ, cùng cột)'),
            ('sub2', 'Khách VII có 2 phiếu hạch toán trên cùng tuyến: 475,200 + 475,200 = 950,400; Cước sau thuế 513,216 + 513,216 = 1,026,432.'),
            ('p', 'Lưu ý: Thuế có thể có số lẻ (vd 520,573.12) vì thuế của chuyến được chia theo tỉ lệ cước của từng khách. Cột KM, Cước chính ở dòng TỔNG có thể lớn hơn tổng các khách vì chuyến ghép chỉ cộng ở dòng TỔNG.'),
            ('p', 'Xem theo Chuyến xe: mỗi dòng I, II… là 1 chuyến với đủ km, cước, thuế, xe, lái xe; dòng con là các phiếu xuất / nhập kho của chuyến với NVKD, khách hàng, người chịu phí.'),
            ('img', '04_trip', 'Báo cáo xem theo Chuyến xe'),
        ]),
        ('XEM DANH SÁCH PHIẾU NHẬP/XUẤT', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm con số gạch chân ở cột Số phiếu HT, ví dụ {icon:lnk_sophieu}, hoặc ở khối Chuyến xe / Đối tượng chịu phí.'),
            ('step', 'Bước 3: Hệ thống mở cửa sổ danh sách phiếu nhập/xuất của đúng con số đã bấm.'),
            ('img', '05_drill', 'Cửa sổ danh sách phiếu nhập/xuất'),
            ('sub', 'Gõ vào ô tìm hoặc chọn phiếu hạch toán, loại chuyến để lọc nhanh; bấm tiêu đề cột để sắp xếp.'),
            ('step', 'Bước 4: Bấm {icon:btn_indanhsach} để in danh sách,'),
            ('sub', 'Hoặc bấm {icon:btn_xuatexceldanhsach} để tải file Excel các dòng đang hiện,'),
            ('sub', 'Hoặc bấm {icon:btn_dong} để quay về báo cáo.'),
            ('p', 'Bấm mã phiếu hạch toán, mã chuyến xe hoặc mã phiếu nhập/xuất để mở chứng từ ở tab mới.'),
        ]),
        ('IN BÁO CÁO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_in}. Hệ thống mở cửa sổ In báo cáo.'),
            ('img', '09_print_opt', 'Cửa sổ In báo cáo'),
            ('step', 'Bước 3: Chọn "In bảng tổng hợp" (theo cách xem đang chọn) hoặc "Danh sách phiếu nhập/xuất", tích chọn các cột cần in.'),
            ('step', 'Bước 4: Bấm {icon:btn_in_modal}. Hệ thống mở cửa sổ xem trước gồm mọi trang theo bộ lọc.'),
            ('sub', 'Hoặc bấm {icon:btn_huy} để đóng.'),
            ('step', 'Bước 5: Bấm nút In trong cửa sổ xem trước để in ra máy in.'),
            ('sub', 'Báo cáo quá 2.000 dòng thì không in được, hãy thu hẹp kỳ hoặc dùng Xuất Excel.'),
        ]),
        ('XUẤT EXCEL', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. File Excel được tải về ngay, gồm mọi trang, theo cách xem đang chọn (Khách hàng hoặc Chuyến xe).'),
            ('sub', 'Kỳ dài (cả năm) cần chờ vài giây để hệ thống tạo file.'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '12_colcfg', 'Cửa sổ Tuỳ chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột; kéo biểu tượng ☰ để đổi thứ tự (cột có biểu tượng khóa luôn hiện).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột khóa).'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để áp dụng'),
            ('sub', 'Hoặc bấm {icon:btn_dong_cfg} nếu muốn bỏ thay đổi.'),
            ('p', 'Mỗi cách xem (Khách hàng / Chuyến xe) có cấu hình cột riêng.'),
        ]),
    ],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    L.shorten_field_icons(scr)
    print('docx:', D.build_hdsd_report(scr, H, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)
