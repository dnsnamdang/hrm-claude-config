# -*- coding: utf-8 -*-
"""HDSD_Báo cáo hiệu quả gộp xe vận tải — bản GỌN + PHẦN "ĐỌC BÁO CÁO" (khuôn sale-customer-debt-reports/docs/compare/gen_hdsd.py).
Ảnh + icon: hdsd_shots/ (capture.js). Sơ đồ: uml/overview.png (gen_srs.py vẽ).
Chạy:  python gen_hdsd.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _trp_docs as D  # noqa: E402
from _trp_docs import L  # noqa: E402

TEN = 'Báo cáo hiệu quả gộp xe vận tải'
OUT = os.path.join(HERE, 'HDSD_%s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'HDSD_%s.pdf' % TEN)
VAO = 'Bước 1: Truy cập màn hình %s, chọn kỳ cần xem (xem PHẦN 1).' % TEN

COT = [
    ['Cột', 'Ý nghĩa / lấy số từ đâu'],
    ['TỔNG (dòng đầu bảng)', 'Cộng toàn bộ chuyến theo bộ lọc (mọi trang). Không đổi khi chuyển trang.'],
    ['Công ty / Biển số xe', 'Dòng nền xanh (I, II…) là công ty của lái xe; dòng con (1, 2…) là từng xe. Bấm biển số để mở báo cáo chi tiết của xe đó ở tab mới.'],
    ['Số chuyến', 'Số phiếu hạch toán chuyến xe đã hạch toán, có ngày hạch toán trong kỳ. Bấm số để xem danh sách chuyến (PHẦN 3).'],
    ['KM định mức', 'Km của tuyến đường × 2 nếu chuyến 2 chiều; chuyến xe khác không có tuyến lấy km nhập trên chuyến.'],
    ['KM thực chạy', 'Km kết thúc − km bắt đầu nhập trên chuyến xe.'],
    ['Chênh lệch (KM)', 'KM thực chạy − KM định mức.'],
    ['% Chênh lệch', 'Chênh lệch ÷ KM định mức × 100, tính trên tổng km của dòng (không cộng dồn %).'],
    ['Cước', 'Cước cần phân bổ ghi trên chuyến xe.'],
    ['Chi phí lái xe', 'Tổng bút toán Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường của phiếu hạch toán (gồm cả bút toán không gắn lái xe, không gồm Công tác phí).'],
    ['Lãi gộp', 'Cước − Chi phí lái xe. Số âm là lỗ.'],
]

H = {
    'ten': TEN,
    'thuat_ngu': [
        ['Chuyến', 'Một phiếu hạch toán chuyến xe chở hàng hoặc chuyến xe khác đã hạch toán.'],
        ['Kỳ', 'Khoảng thời gian xem báo cáo, tính theo ngày hạch toán của phiếu hạch toán chuyến xe.'],
        ['Cước', 'Cước cần phân bổ ghi trên chuyến xe.'],
        ['Chi phí lái xe', 'Công lái xe, xăng xe, chi phí khác, vé cầu đường của chuyến.'],
        ['Lãi gộp', 'Cước − Chi phí lái xe.'],
        ['Chuyến lỗ', 'Chuyến có lãi gộp âm.'],
    ],
    'phien_ban': [['1.0', '18/11/2026', 'Đội phát triển phần mềm', 'Phát hành lần đầu']],
    'quyen': [
        'Mọi người dùng đăng nhập đều mở được màn hình và dùng mọi chức năng: xem, tìm kiếm, xem danh sách chuyến, in, xuất Excel, tùy chỉnh cột.',
        'Số liệu được xem tùy quyền "Xem báo cáo vận chuyển": mức Tổng công ty xem mọi công ty; mức Công ty xem chuyến có lái xe thuộc công ty mình; không có quyền thì chỉ xem chuyến do mình lập bút toán.',
    ],
    'phan': [
        ('TRUY CẬP VÀ TÌM KIẾM', [
            ('step', 'Bước 1: Từ phân hệ Vận chuyển {icon:menu_phanhe}, tại menu Báo cáo vận chuyển {icon:menu_nhom}, chọn Báo cáo hiệu quả gộp xe vận tải {icon:menu_muc}'),
            ('img', '01_open', 'Màn hình Báo cáo hiệu quả gộp xe vận tải khi mới mở (kỳ Tháng này)'),
            ('step', 'Bước 2: Chọn kỳ ở ô {icon:o_ky}: Tuần này, Tháng này, Tháng trước, Năm nay hoặc Tuỳ chọn. Báo cáo tự tải lại.'),
            ('sub', 'Chọn Tuỳ chọn thì chọn thêm Từ ngày, Đến ngày ở ô {icon:o_thoigian}.'),
            ('step', 'Bước 3: Lọc thêm (tùy chọn):'),
            ('sub', 'Chọn công ty ở ô {icon:o_congty} (chỉ chọn được khi có quyền xem theo tổng công ty).'),
            ('sub', 'Hoặc chọn biển số ở ô {icon:o_bienso}.'),
            ('step', 'Bước 4: Bấm {icon:btn_timkiem} để tải lại báo cáo,'),
            ('sub', 'Hoặc bấm {icon:btn_xoaloc} để đưa mọi ô lọc về mặc định.'),
        ]),
        ('ĐỌC BÁO CÁO', [
            ('p', 'Đầu trang là khối tổng hợp của kỳ (Chuyến xe, Hiệu quả gộp, Quãng đường). Bảng gồm dòng TỔNG, mỗi công ty một dòng nền xanh, dưới là các xe của công ty. Rê chuột vào biểu tượng ⓘ ở tiêu đề cột để xem cách tính; ô {icon:o_capbung} chọn xem đến công ty hay đến xe.'),
            ('img', '03_report', 'Báo cáo kỳ Tháng trước (tháng 10/2026)'),
            ('table', COT, [1.6, 4.9]),
            ('img', '13_read_money', 'Phóng to cột Số chuyến, Cước, Chi phí lái xe, Lãi gộp (cắt từ ảnh Hình 3)'),
            ('p', '**Ví dụ đọc số từ ảnh phóng to:**'),
            ('sub2', 'Số chuyến dòng TỔNG: 40 = 18 + 18 + 4 (3 công ty).'),
            ('sub2', 'Lãi gộp công ty I: 144,818 = 1,360,859 (xe 29D-54533) + (−1,216,041) (xe 15D-00500); xe 15D-00500 lỗ vì chi phí lái xe 3,498,641 lớn hơn cước 2,282,600.'),
            ('sub2', 'Lãi gộp dòng TỔNG: 24,720,667 − 18,129,331 = 6,591,336.'),
            ('img', '13_read_km', 'Phóng to các cột km (cắt từ ảnh Hình 3)'),
            ('sub2', '% Chênh lệch công ty II: 394 ÷ 1,738 × 100 = 22.67% (tính trên tổng km của công ty, không cộng % của 2 xe 0% + 29.8%).'),
            ('p', 'Lưu ý: KM thực chạy rất lớn (như xe 29D-54533) thường do km bắt đầu / kết thúc trên chuyến xe nhập sai; kiểm lại chuyến bằng cách bấm số chuyến của xe.'),
        ]),
        ('XEM DANH SÁCH CHUYẾN XE', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm con số gạch chân ở cột Số chuyến, ví dụ {icon:lnk_sochuyen}, hoặc ở khối Chuyến xe (Tất cả chuyến, Chuyến xe chở hàng, Chuyến xe khác, Chuyến lỗ).'),
            ('step', 'Bước 3: Hệ thống mở cửa sổ danh sách chuyến của đúng con số đã bấm.'),
            ('img', '05_drill', 'Cửa sổ danh sách chuyến xe'),
            ('sub', 'Gõ vào ô tìm hoặc chọn biển số, loại chuyến để lọc nhanh; bấm tiêu đề cột để sắp xếp.'),
            ('step', 'Bước 4: Bấm {icon:btn_indanhsach} để in danh sách,'),
            ('sub', 'Hoặc bấm {icon:btn_xuatexceldanhsach} để tải file Excel,'),
            ('sub', 'Hoặc bấm {icon:btn_dong} để quay về báo cáo.'),
            ('p', 'Bấm biển số xe {icon:lnk_bienso} ở bảng để mở Báo cáo chi tiết hiệu quả gộp theo chuyến xe của xe đó ở tab mới.'),
        ]),
        ('IN BÁO CÁO', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_in}. Hệ thống mở cửa sổ In báo cáo.'),
            ('img', '09_print_opt', 'Cửa sổ In báo cáo'),
            ('step', 'Bước 3: Chọn "In bảng tổng hợp" hoặc "Danh sách chuyến xe", tích chọn các cột cần in.'),
            ('step', 'Bước 4: Bấm {icon:btn_in_modal}. Hệ thống mở cửa sổ xem trước gồm mọi trang theo bộ lọc.'),
            ('sub', 'Hoặc bấm {icon:btn_huy} để đóng.'),
            ('step', 'Bước 5: Bấm nút In trong cửa sổ xem trước để in ra máy in.'),
            ('sub', 'Báo cáo quá 2.000 dòng thì không in được, hãy thu hẹp kỳ hoặc dùng Xuất Excel.'),
        ]),
        ('XUẤT EXCEL', [
            ('step', VAO),
            ('step', 'Bước 2: Bấm {icon:btn_xuatexcel}. Hệ thống mở cửa sổ Xuất Excel.'),
            ('img', '11_export_opt', 'Cửa sổ Xuất Excel'),
            ('step', 'Bước 3: Chọn "Xuất bảng tổng hợp" hoặc "Danh sách chuyến xe", tích chọn các cột cần xuất.'),
            ('step', 'Bước 4: Bấm {icon:btn_xuat_modal}. File Excel được tải về, gồm mọi trang theo bộ lọc.'),
        ]),
        ('TÙY CHỈNH CỘT HIỂN THỊ', [
            ('step', 'Bước 1: Bấm biểu tượng {icon:btn_cauhinhcot}'),
            ('img', '12_colcfg', 'Cửa sổ Tuỳ chỉnh cột'),
            ('step', 'Bước 2: Tích để hiện cột, bỏ tích để ẩn cột; kéo biểu tượng ☰ để đổi thứ tự (cột có biểu tượng khóa luôn hiện).'),
            ('step', 'Bước 3: Bấm {icon:btn_chontatca} để hiện tất cả các cột.'),
            ('sub', 'Hoặc bấm {icon:btn_bochonhet} để ẩn tất cả các cột (trừ các cột khóa).'),
            ('step', 'Bước 4: Bấm {icon:btn_luu} để áp dụng'),
            ('sub', 'Hoặc bấm {icon:btn_dong_cfg} nếu muốn bỏ thay đổi.'),
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
