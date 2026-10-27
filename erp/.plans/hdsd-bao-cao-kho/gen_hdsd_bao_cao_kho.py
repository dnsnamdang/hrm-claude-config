# -*- coding: utf-8 -*-
"""Sinh HDSD cho 3 man ERP bao cao kho, theo khuon file mau user gui
(HDSD_Yeu_cau_dat_hang_mua_ngoai.docx - ban chi co chu, khong anh):
  - The kho
  - Bao cao ton kho chi tiet theo mat hang
  - Bao cao ton kho tong hop theo mat hang

Cach dung khuon: QgWriter (hrm/.plans/gop-db/_catalog_docs_lib/qg_writer.py) lay chinh file mau lam
vo (bia + muc luc + style), xoa than bai, nhan ban doan mau theo vai tro.

Noi dung doc tu code ERP (D:/laragon/www/erp):
  WarehouseReportsController (stockCard, stockCardDetail, stockGeneralProduct + searchData / export)
  resources/views/warehouse/warehouse_reports/stock_card*.blade.php, stock_general_product.blade.php

Chay:  python -X utf8 .plans/hdsd-bao-cao-kho/gen_hdsd_bao_cao_kho.py
Output: .plans/the-kho/HDSD_The_kho.docx,
        .plans/bao-cao-ton-kho-chi-tiet-theo-mat-hang/HDSD_Bao_cao_ton_kho_chi_tiet_theo_mat_hang.docx,
        .plans/bao-cao-ton-kho-tong-hop-theo-mat-hang/HDSD_Bao_cao_ton_kho_tong_hop_theo_mat_hang.docx
"""
import copy
import os
import sys

from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
PLANS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join("D:/laragon/www/hrm", ".plans", "gop-db", "_catalog_docs_lib"))
from qg_writer import QgWriter, strip_embedded_fonts  # noqa: E402

TPL = os.path.join(HERE, "_tpl", "HDSD_mau_Yeu_cau_dat_hang_mua_ngoai.docx")

# Chi so phan tu body trong file mau (da do 24/10/2026)
ROLES = {'pagebreak': 35, 'h1': 36, 'h2': 21, 'p': 30, 'step': 37, 'sub': 39,
         'blank': 23, 'tbl2': 22, 'tbl4': 25}
BODY_FROM = 19
VERSION = [["Phiên bản", "Ngày", "Người cập nhật", "Nội dung"],
           ["1.0", "24/10/2026", "Phòng Phát triển", "Khởi tạo tài liệu hướng dẫn sử dụng"]]


def tong_quan(w, thuat_ngu, quyen, ghi_chu_quyen, chuc_nang):
    w.h1("TỔNG QUAN", new_page=True)
    w.h2("1. Thuật ngữ sử dụng trong tài liệu")
    w.table([["Thuật ngữ", "Giải thích"]] + thuat_ngu, widths=[1, 2.2])
    w.h2("2. Cập nhật tài liệu")
    w.table(VERSION, widths=[0.9, 1.3, 1.5, 2.7])
    w.h2("3. Quyền sử dụng")
    w.table([["Chức năng", "Quyền cần có"]] + quyen, widths=[1.3, 2])
    if ghi_chu_quyen:
        w.p(ghi_chu_quyen)
    w.h2("4. Sơ đồ chức năng tổng quan")
    w.p("Màn hình gồm các chức năng chính sau:")
    w.table([["STT", "Chức năng"]] + [[str(i + 1), c] for i, c in enumerate(chuc_nang)], widths=[0.5, 3])


def section(w, n, title, lines):
    """lines: list (kind, segs) voi kind 'step' hoac 'sub' (dong 'Hoac ...')."""
    w.h1("PHẦN %d: %s" % (n, title), new_page=True)
    k = 0
    for kind, segs in lines:
        if kind == 'step':
            k += 1
            w.step("Bước %d: %s" % (k, segs))
        else:
            w.raw('sub', segs)


def fix_toc_levels(w):
    """Muc luc file mau phan cap bang style TOC1/TOC2 (khong bang thut le) -> rebuild_toc cua
    QgWriter coi het la cap 1. Gan lai style TOC2 cho cac dong ung voi Heading 2."""
    h2 = {bm for lvl, _t, bm in w.headings if lvl == 2}
    sdt = w.doc.element.body.find(qn('w:sdt'))
    for p in sdt.iter(qn('w:p')):
        hl = p.find(qn('w:hyperlink'))
        if hl is None:
            continue
        st = p.find(qn('w:pPr')).find(qn('w:pStyle'))
        st.set(qn('w:val'), 'TOC2' if hl.get(qn('w:anchor')) in h2 else 'TOC1')


def word_update(path, pdf_path):
    """Cap nhat muc luc + so trang bang Word (Windows COM), luu, xuat PDF de soat."""
    import subprocess
    ps = (
        "$w = New-Object -ComObject Word.Application; $w.Visible = $false;"
        "$d = $w.Documents.Open('%s');"
        "$d.TablesOfContents.Item(1).Update();"
        "$d.Save();"
        "$d.SaveAs2('%s', 17);"
        "$d.Close(0); $w.Quit()" % (path.replace('/', '\\'), pdf_path.replace('/', '\\'))
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


def build(screen, out, thuat_ngu, quyen, ghi_chu_quyen, parts):
    w = QgWriter(TPL, ROLES, BODY_FROM, cover_replace={'Yêu cầu đặt hàng mua ngoài': screen})
    # bang so do chuc nang viet chu thuong nhu file mau ("Truy cập và tìm kiếm")
    names = [t[0] + t[1:].lower() for t, _ in parts]
    names = [n.replace("thẻ kho", "Thẻ kho").replace("excel", "Excel") for n in names]
    tong_quan(w, thuat_ngu, quyen, ghi_chu_quyen, names)
    for i, (title, lines) in enumerate(parts, 1):
        section(w, i, title, lines)
    w.rebuild_toc(levels=(1, 2))
    fix_toc_levels(w)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    w.save(out)
    pdf_dir = os.environ.get("HDSD_PDF_DIR", os.path.join(HERE, "_pdf"))
    os.makedirs(pdf_dir, exist_ok=True)
    pdf = os.path.join(pdf_dir, os.path.splitext(os.path.basename(out))[0] + ".pdf")
    word_update(out, pdf)
    strip_embedded_fonts(out)
    print("Da tao:", out)
    return pdf


S, O = 'step', 'sub'

# =================================================================== THE KHO
THE_KHO = dict(
    screen="Thẻ kho",
    out=os.path.join(PLANS, "the-kho", "HDSD_The_kho.docx"),
    thuat_ngu=[
        ["Thẻ kho", "Báo cáo theo dõi biến động số lượng nhập, xuất, tồn của một mặt hàng trong một "
                    "khoảng thời gian, theo kho và vị trí."],
        ["Tồn đầu kỳ", "Số lượng tồn trước ngày ở ô Từ ngày."],
        ["Nhập trong kỳ", "Tổng số lượng nhập trong khoảng ngày đã chọn (không tính điều chuyển vị trí)."],
        ["Xuất trong kỳ", "Tổng số lượng xuất trong khoảng ngày đã chọn (không tính điều chuyển vị trí)."],
        ["Tồn cuối kỳ", "Tồn đầu kỳ cộng Nhập trong kỳ trừ Xuất trong kỳ."],
        ["SL tồn", "Số lượng tồn lũy kế sau từng chứng từ."],
        ["Công ty thuê kho", "Công ty sở hữu phần hàng đang gửi trong kho."],
        ["Tất cả", "Loại báo cáo hiện cả các dòng điều chuyển vị trí."],
        ["Không nhặt điều chuyển", "Loại báo cáo bỏ các dòng điều chuyển vị trí."],
        ["NVKD", "Người yêu cầu của chứng từ, kèm mã phòng ban."],
    ],
    quyen=[
        ["Xem Thẻ kho", "Thủ kho"],
        ["Chọn công ty khác ở ô Tồn theo công ty", "Xem báo cáo tồn kho theo tổng công ty"],
        ["Chọn kho", "Theo kho được phân cho người dùng"],
        ["In / Xuất Excel", "Như quyền xem Thẻ kho"],
    ],
    ghi_chu_quyen="Nếu không có quyền Thủ kho, người dùng không mở được màn hình Thẻ kho.",
    parts=[
        ("TRUY CẬP VÀ LỌC THẺ KHO", [
            (S, "Từ phân hệ **[Kho]**, tại menu **[Báo cáo kho]**, chọn **[Thẻ kho]**."),
            (S, "Tại ô **Hàng hóa**, bấm nút tìm để mở cửa sổ tìm hàng hóa, chọn hàng hóa cần xem."),
            (S, "Chọn **Tồn theo công ty**, chọn một hoặc nhiều **Kho**; ô **Công ty thuê kho** tự chọn "
                "hết theo kho đã chọn."),
            (O, "Hoặc bỏ bớt công ty ở ô **Công ty thuê kho** để chỉ xem phần tồn của công ty còn lại."),
            (S, "Chọn **Từ ngày**, **Đến ngày** (mặc định từ 01/01 năm nay đến hôm nay)."),
            (S, "Chọn **Loại báo cáo**: **Tất cả** hoặc **Không nhặt điều chuyển**."),
            (S, "Bấm **[Lọc]**, hệ thống hiển thị thẻ kho của hàng hóa đã chọn."),
        ]),
        ("LỌC THEO VỊ TRÍ TRONG KHO", [
            (S, "Chọn hàng hóa và **Kho** như PHẦN 1."),
            (S, "Tại khung **Nhà**, tích chọn nhà; khung **Dãy** hiện các dãy của nhà đã chọn."),
            (S, "Tại khung **Dãy**, tích chọn dãy; khung **Khoang** hiện các khoang của dãy đã chọn."),
            (S, "Tại khung **Khoang**, tích chọn khoang; khung **Vị trí** hiện các vị trí thuộc khoang."),
            (S, "Tại khung **Vị trí**, tích chọn vị trí cần xem."),
            (O, "Hoặc tích vị trí trong mục **Vị trí tự do** của kho."),
            (S, "Bấm **[Lọc]**."),
        ]),
        ("XEM KẾT QUẢ THẺ KHO", [
            (S, "Xem khối tổng hợp đầu bảng: **Tồn đầu kỳ**, **Nhập trong kỳ**, **Xuất trong kỳ**, "
                "**Tồn cuối kỳ**."),
            (S, "Xem các dòng chứng từ bên dưới, sắp theo thời gian: **Ngày chứng từ**, **Số chứng từ**, "
                "**Diễn giải**, số lượng **Nhập** / **Xuất**."),
            (S, "Xem cột **Chi tiết** của từng chứng từ: **Lô**, **Vị trí**, **SL theo vị trí**."),
            (S, "Xem cột **SL tồn** để biết số tồn sau từng chứng từ; cột **NVKD** để biết người yêu cầu."),
        ]),
        ("ĐỔI ĐƠN VỊ TÍNH", [
            (S, "Lọc thẻ kho như PHẦN 1."),
            (S, "Tại dòng **Đơn vị tính** của khối tổng hợp, chọn đơn vị tính cần xem."),
            (S, "Hệ thống quy đổi lại các số lượng theo đơn vị tính đã chọn."),
        ]),
        ("XEM CHỨNG TỪ GỐC", [
            (S, "Lọc thẻ kho như PHẦN 1."),
            (S, "Bấm vào **Số chứng từ** trên dòng cần xem."),
            (S, "Hệ thống mở chi tiết chứng từ ở tab mới (phiếu nhập kho, phiếu xuất kho, phiếu điều chuyển "
                "vị trí, phiếu nhập / xuất kho điều chỉnh…)."),
        ]),
        ("IN", [
            (S, "Chọn hàng hóa và điều kiện lọc (xem PHẦN 1)."),
            (S, "Bấm **[In]**, hệ thống mở cửa sổ **In báo cáo**."),
            (S, "Tại ô **Kiểu in**, chọn **Đầy đủ** hoặc **Rút gọn** (không có cột NVKD)."),
            (S, "Bấm **[IN]**, hệ thống mở bản in ở tab mới; thực hiện in từ trình duyệt."),
        ]),
        ("XUẤT EXCEL", [
            (S, "Chọn hàng hóa và điều kiện lọc (xem PHẦN 1)."),
            (S, "Bấm **[Xuất excel]**, hệ thống mở cửa sổ **Xuất báo cáo**."),
            (S, "Tại ô **Kiểu xuất**, chọn **Đầy đủ** hoặc **Rút gọn**."),
            (S, "Bấm **[Xuất]**, hệ thống tải về file **bao_cao_the_kho.xlsx**."),
        ]),
    ],
)

# =================================================== BAO CAO TON KHO CHI TIET
CHI_TIET = dict(
    screen="Báo cáo tồn kho chi tiết theo mặt hàng",
    out=os.path.join(PLANS, "bao-cao-ton-kho-chi-tiet-theo-mat-hang",
                     "HDSD_Bao_cao_ton_kho_chi_tiet_theo_mat_hang.docx"),
    thuat_ngu=[
        ["Báo cáo tồn kho chi tiết theo mặt hàng", "Báo cáo số lượng tồn của từng mặt hàng tại một kho, "
                                                   "chi tiết theo công ty thuê kho, lô và vị trí."],
        ["Tính đến ngày", "Ngày chốt số tồn của báo cáo."],
        ["SL tồn", "Tổng số lượng tồn của mặt hàng tại kho đã chọn."],
        ["Công ty thuê kho", "Công ty sở hữu phần hàng đang gửi trong kho."],
        ["Lô", "Số lô hàng nhập kho; lô nhập theo hợp đồng có kèm số hợp đồng và thông tin khách hàng."],
        ["Cộng", "Tổng số lượng tồn của một công ty thuê kho."],
    ],
    quyen=[
        ["Xem báo cáo", "Một trong các quyền: Xem báo cáo tồn kho theo tổng công ty / Xem báo cáo tồn kho "
                        "theo công ty / Xem báo cáo tồn kho theo kho"],
        ["Chọn công ty khác ở ô Tồn theo công ty", "Xem báo cáo tồn kho theo tổng công ty"],
        ["Xuất Excel", "Như quyền xem báo cáo"],
    ],
    ghi_chu_quyen="Nếu không có quyền xem nào ở trên, người dùng không mở được màn hình.",
    parts=[
        ("TRUY CẬP VÀ LỌC BÁO CÁO", [
            (S, "Từ phân hệ **[Kho]**, tại menu **[Báo cáo kho]**, chọn **[Báo cáo tồn kho chi tiết theo "
                "mặt hàng]**."),
            (S, "Chọn **Tính đến ngày** (mặc định hôm nay) và **Tồn theo công ty**."),
            (S, "Chọn **Kho**; ô **Công ty thuê kho** tự chọn hết theo kho đã chọn."),
            (S, "Nhập hoặc chọn thêm điều kiện lọc nếu cần:"),
            (O, "Hoặc chọn **Nhóm hàng hóa**, **Tính chất hàng hóa**, **Loại hàng hóa**."),
            (O, "Hoặc chọn **Thương hiệu**, **Hãng sản xuất**."),
            (O, "Hoặc bấm nút tìm ở ô **Hàng hóa** để chọn một hàng hóa."),
            (O, "Hoặc nhập số **Hợp đồng**."),
            (S, "Bấm **[Lọc]**, hệ thống hiển thị danh sách hàng hóa còn tồn."),
        ]),
        ("XEM KẾT QUẢ BÁO CÁO", [
            (S, "Xem thông tin hàng hóa: **Tên hàng hóa**, **Model**, **Mã hàng**, **Thương hiệu**, **SL tồn**."),
            (S, "Xem cột **Chi tiết** của từng hàng: **Công ty**, **Lô**, **Vị trí**, **SL**, **Cộng**."),
            (S, "Chuyển trang ở thanh phân trang cuối bảng (20 hàng hóa mỗi trang)."),
        ]),
        ("ĐỔI ĐƠN VỊ TÍNH", [
            (S, "Lọc báo cáo như PHẦN 1."),
            (S, "Tại cột **ĐVT** của hàng hóa, chọn đơn vị tính cần xem."),
            (S, "Hệ thống quy đổi số lượng của hàng hóa đó theo đơn vị tính đã chọn."),
        ]),
        ("XEM HỢP ĐỒNG CỦA LÔ", [
            (S, "Lọc báo cáo như PHẦN 1."),
            (S, "Tại ô **Lô** có dòng **Hợp đồng**, xem số hợp đồng, khách hàng, ngày đặt hàng, ngày trả hàng."),
            (S, "Bấm vào số hợp đồng để mở hợp đồng."),
        ]),
        ("LÀM MỚI BỘ LỌC", [
            (S, "Bấm nút **[Làm mới]** (biểu tượng mũi tên xoay) cạnh nút Lọc."),
            (S, "Hệ thống xóa các điều kiện lọc, ô **Tính đến ngày** về hôm nay."),
        ]),
        ("XUẤT EXCEL", [
            (S, "Lọc báo cáo theo dữ liệu cần lấy (xem PHẦN 1)."),
            (S, "Bấm **[Xuất excel]**, hệ thống mở cửa sổ **Xuất Excel**."),
            (S, "Tại ô **Mẫu excel**, chọn **Xuất excel đầy đủ** hoặc **Xuất excel ngắn gọn**."),
            (S, "Bấm **[Xuất EXCEL]**, hệ thống tải về file **bao_cao_ton_kho_chi_tiet_mat_hang.xlsx**."),
            (O, "Hoặc khi báo cáo có từ 150 hàng hóa trở lên, hệ thống báo **Báo cáo tồn kho chi tiết theo "
                "mặt hàng sẽ gửi về mail của bạn trong ít phút!** và gửi file về email của người dùng."),
        ]),
    ],
)

# =================================================== BAO CAO TON KHO TONG HOP
TONG_HOP = dict(
    screen="Báo cáo tồn kho tổng hợp theo mặt hàng",
    out=os.path.join(PLANS, "bao-cao-ton-kho-tong-hop-theo-mat-hang",
                     "HDSD_Bao_cao_ton_kho_tong_hop_theo_mat_hang.docx"),
    thuat_ngu=[
        ["Báo cáo tồn kho tổng hợp theo mặt hàng", "Báo cáo tổng số lượng tồn của từng mặt hàng trên một "
                                                   "hoặc nhiều kho."],
        ["Tính đến ngày", "Ngày chốt số tồn của báo cáo."],
        ["Xem toàn bộ kho", "Ô tích chọn sẵn mọi kho của công ty đang chọn."],
        ["SL tồn", "Tổng số lượng tồn của mặt hàng trên các kho đã chọn."],
        ["Công ty thuê kho", "Công ty sở hữu phần hàng đang gửi trong kho."],
        ["Chi tiết", "Nhóm cột số lượng tồn theo từng công ty thuê kho."],
    ],
    quyen=[
        ["Xem báo cáo", "Một trong các quyền: Xem báo cáo tồn kho theo tổng công ty / Xem báo cáo tồn kho "
                        "theo công ty / Xem báo cáo tồn kho theo kho"],
        ["Chọn công ty khác ở ô Tồn theo công ty", "Xem báo cáo tồn kho theo tổng công ty"],
        ["Xem cột Chi tiết theo công ty thuê kho", "Xem báo cáo tồn kho theo tổng công ty"],
        ["Xuất Excel", "Như quyền xem báo cáo"],
    ],
    ghi_chu_quyen="Nếu không có quyền xem nào ở trên, người dùng không mở được màn hình.",
    parts=[
        ("TRUY CẬP VÀ LỌC BÁO CÁO", [
            (S, "Từ phân hệ **[Kho]**, tại menu **[Báo cáo kho]**, chọn **[Báo cáo tồn kho tổng hợp theo "
                "mặt hàng]**."),
            (S, "Chọn **Tính đến ngày** (mặc định hôm nay) và **Tồn theo công ty**."),
            (S, "Nhập hoặc chọn thêm điều kiện lọc nếu cần:"),
            (O, "Hoặc chọn **Nhóm hàng hóa**, **Tính chất hàng hóa**, **Loại hàng hóa**."),
            (O, "Hoặc chọn **Thương hiệu**, **Hãng sản xuất**."),
            (O, "Hoặc bấm nút tìm ở ô **Hàng hóa** để chọn một hàng hóa."),
            (O, "Hoặc nhập số **Hợp đồng**."),
            (S, "Bấm **[Lọc]**, hệ thống hiển thị danh sách hàng hóa còn tồn trên các kho đã chọn."),
        ]),
        ("CHỌN KHO XEM BÁO CÁO", [
            (S, "Giữ tích ô **Xem toàn bộ kho** để xem mọi kho của công ty (mặc định)."),
            (O, "Hoặc bỏ tích ô **Xem toàn bộ kho**, rồi chọn một hoặc nhiều kho ở ô **Kho**."),
            (S, "Ô **Công ty thuê kho** tự chọn hết theo kho đã chọn."),
            (O, "Hoặc bỏ bớt công ty ở ô **Công ty thuê kho** để chỉ xem phần tồn của công ty còn lại."),
            (S, "Bấm **[Lọc]**."),
        ]),
        ("XEM KẾT QUẢ BÁO CÁO", [
            (S, "Xem thông tin hàng hóa: **Tên hàng hóa**, **Model**, **Mã hàng**, **Thương hiệu**, **SL tồn**."),
            (S, "Xem nhóm cột **Chi tiết**: số tồn theo từng công ty thuê kho (chỉ hiện với quyền xem theo "
                "tổng công ty); rê chuột vào tiêu đề cột để xem tên công ty."),
            (S, "Chuyển trang ở thanh phân trang cuối bảng (20 hàng hóa mỗi trang)."),
        ]),
        ("ĐỔI ĐƠN VỊ TÍNH", [
            (S, "Lọc báo cáo như PHẦN 1."),
            (S, "Tại cột **ĐVT** của hàng hóa, chọn đơn vị tính cần xem."),
            (S, "Hệ thống quy đổi số lượng của hàng hóa đó; đơn vị tính đã chọn được giữ khi lọc lại và khi "
                "xuất Excel."),
        ]),
        ("LÀM MỚI BỘ LỌC", [
            (S, "Bấm nút **[Làm mới]** (biểu tượng mũi tên xoay) cạnh nút Lọc."),
            (S, "Hệ thống xóa các điều kiện lọc, ô **Tính đến ngày** về hôm nay."),
        ]),
        ("XUẤT EXCEL", [
            (S, "Lọc báo cáo theo dữ liệu cần lấy (xem PHẦN 1)."),
            (S, "Bấm **[Xuất excel]**, hệ thống mở cửa sổ **Xuất Excel**."),
            (S, "Tại ô **Mẫu excel**, chọn **Xuất excel đầy đủ** (có cột theo công ty thuê kho) hoặc **Xuất "
                "excel ngắn gọn**."),
            (S, "Bấm **[Xuất EXCEL]**, hệ thống tải về file **bao_cao_ton_kho_tong_hop_mat_hang.xlsx**."),
            (O, "Hoặc khi báo cáo có từ 500 hàng hóa trở lên, hệ thống báo **Báo cáo tồn kho tổng hợp sẽ gửi "
                "về mail của bạn trong ít phút!** và gửi file về email của người dùng."),
        ]),
    ],
)

if __name__ == "__main__":
    for cfg in (THE_KHO, CHI_TIET, TONG_HOP):
        build(**cfg)
