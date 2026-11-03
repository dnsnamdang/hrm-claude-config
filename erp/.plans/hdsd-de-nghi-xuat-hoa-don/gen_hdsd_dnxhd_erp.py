# -*- coding: utf-8 -*-
"""Dung HDSD + Huong dan tao du lieu test man 'De nghi xuat hoa don'
(export_bill_request) - ERP TanPhatDev, nhanh develop_02.

Nguon khao sat (develop_02):
  - app/Http/Controllers/IncomeExpenditure/ExportBillRequestController.php
  - app/Model/IncomeExpenditure/ExportBillRequest.php
  - app/Services/Contracts/SearchContractService.php (popup chon HD)
  - resources/views/income_expenditure/export_bill_requests/*
  - routes/web.php (prefix export_bill_requests) + topmenubar.blade.php

Theo yeu cau user: tai lieu GOM ca "cac buoc tao du lieu de co the test duoc"
(PHAN 1) — phan nay vuot ngoai format HDSD chuan (von cam du lieu test), nhung
la noi dung user yeu cau ro.

Chay:  /usr/local/bin/python3 gen_hdsd_dnxhd_erp.py
Output: ERP/HDSD_luongchinh/HDSD_DeNghiXuatHoaDon.docx
"""
import os
import sys
import zipfile

from docx import Document
from docx.oxml.ns import qn

ERP = "/Users/nguyentrancu/DEV/code/ERP-HRM/ERP"
sys.path.insert(0, os.path.join("/Users/nguyentrancu/DEV/code/ERP-HRM/HRM",
                                ".claude", "skills", "hdsd-documenter", "assets"))
from hdsd_engine import HdsdBuilder  # noqa: E402

OUT_DIR = os.path.join(ERP, "HDSD_luongchinh")
os.makedirs(OUT_DIR, exist_ok=True)
OUTPUT = os.path.join(OUT_DIR, "HDSD_DeNghiXuatHoaDon.docx")

SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_shots_empty")
os.makedirs(SHOTS, exist_ok=True)


def img_placeholder(b, mo_ta):
    b.para(mo_ta, bold_prefix="[Vị trí chèn ảnh] ")


def clear_toc_cache(path):
    """Xoa text cache trong moi field TOC -> Word tu dung lai khi mo."""
    doc = Document(path)
    body = doc.element.body
    fields = []
    for el in body.iter():
        tag = el.tag
        if tag == qn('w:fldChar'):
            t = el.get(qn('w:fldCharType'))
            if t == 'begin':
                fields.append({'instr': '', 'in_result': False})
            elif t == 'separate':
                if fields:
                    fields[-1]['in_result'] = True
            elif t == 'end':
                if fields:
                    fields.pop()
        elif tag == qn('w:instrText'):
            if fields:
                fields[-1]['instr'] += (el.text or '')
        elif tag == qn('w:t'):
            if any(f['in_result'] and 'TOC' in f['instr'] for f in fields):
                el.text = ''
    doc.save(path)


def finish_macos(b):
    b.doc.save(b.output)
    clear_toc_cache(b.output)
    b._set_update_fields()
    removed = b._purge_orphan_media()
    chk = Document(b.output)
    raw = zipfile.ZipFile(b.output).read("word/document.xml").decode("utf-8")
    my_headings = {p.text.strip() for p in chk.paragraphs
                   if p.style.name in ("Heading 1", "Heading 2", "Heading 3")}
    sot = [h for h in b.template_headings if h and h in raw and h not in my_headings]
    h1 = sum(1 for p in chk.paragraphs if p.style.name == "Heading 1")
    print("File:", b.output)
    print("Heading 1:", h1, "| Bang:", len(chk.tables),
          "| Anh:", len(chk.inline_shapes), "| Media mo coi da xoa:", len(removed))
    print("Tieu de khung con sot:", sot or "khong (OK)")
    assert not sot, "Van con tieu de khung: %s" % sot


# ============================================================ NOI DUNG
b = HdsdBuilder(
    output=OUTPUT,
    shots_dir=SHOTS,
    cover_title="(Màn hình: Đề nghị xuất hóa đơn)",
    doc_title="HDSD & Hướng dẫn tạo dữ liệu test - Đề nghị xuất hóa đơn",
)

# ------------------------------------------------- TONG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ & viết tắt")
b.para("Bảng thuật ngữ giúp người dùng hiểu đúng các bước hướng dẫn và các bước tạo dữ liệu test.")
b.table([
    ["Thuật ngữ", "Ý nghĩa"],
    ["Đề nghị xuất hóa đơn (ĐNXHĐ)", "Chứng từ đề nghị Kế toán xuất hóa đơn cho phần hàng hóa / dịch vụ / chi phí của một hợp đồng đã thực giao (đã xuất kho) nhưng CHƯA xuất hóa đơn. Đây chính là màn hình tài liệu này hướng dẫn."],
    ["Hợp đồng hãng (HĐ)", "Hợp đồng bán hàng / bán dự án / đơn hàng nguyên tắc / phụ lục bổ sung. Là nguồn chính để lập Đề nghị xuất hóa đơn."],
    ["Hợp đồng dịch vụ (SC-BD)", "Hợp đồng sửa chữa – bảo dưỡng. Cũng có thể lập Đề nghị xuất hóa đơn cho phần việc / vật tư đã hoàn thành."],
    ["Yêu cầu xuất hàng (YCXH)", "Chứng từ đề nghị xuất hàng, do kinh doanh lập từ hợp đồng — bước đầu của quy trình xuất hàng."],
    ["Đề nghị xuất kho (ĐNXK)", "Chứng từ do Kế toán kho lập từ Yêu cầu xuất hàng, gửi Thủ kho."],
    ["Phiếu xuất kho (PXK)", "Chứng từ Thủ kho thực hiện xuất hàng khỏi kho. CHỈ khi có Phiếu xuất kho thì phần 'đã xuất kho' của dòng hàng mới tăng lên — đây là mấu chốt để hợp đồng đủ điều kiện xuất hóa đơn."],
    ["SL được xuất HĐ", "Số lượng đã thực xuất kho nhưng chưa xuất hóa đơn của một dòng hàng — là mức tối đa được đưa vào Đề nghị xuất hóa đơn."],
    ["SL cần xuất HĐ", "Số lượng người lập nhập cho từng dòng hàng khi lập Đề nghị xuất hóa đơn (không được vượt SL được xuất HĐ)."],
    ["Đang xuất HĐ", "Phần hàng / chi phí đang nằm trong một Đề nghị xuất hóa đơn CHƯA duyệt."],
    ["Đã xuất HĐ", "Phần hàng / chi phí đã được duyệt xuất hóa đơn — không còn đưa vào đề nghị mới."],
])

b.h2("2. Lịch sử cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "02/11/2026", "Khởi tạo HDSD + hướng dẫn tạo dữ liệu test màn Đề nghị xuất hóa đơn (ERP, nhánh develop_02)", "Phòng Phát triển"],
])

b.h2("3. Giới thiệu chung & đường dẫn truy cập")
b.para("Màn hình Đề nghị xuất hóa đơn dùng để lập và quản lý các phiếu đề nghị Kế toán xuất hóa đơn cho phần hàng hóa / dịch vụ / chi phí của hợp đồng đã thực giao nhưng chưa xuất hóa đơn. Phiếu lập xong được gửi duyệt; sau khi duyệt, phần hàng tương ứng được đánh dấu là đã xuất hóa đơn.")
b.bullet("menu Công nợ - Thu - Chi › \"Đề nghị xuất hóa đơn\" (danh sách theo phạm vi quyền).", bold_prefix="Đường dẫn danh sách: ")
b.bullet("menu \"Phiếu đề nghị xuất hóa đơn chờ duyệt\" — danh sách các phiếu đang chờ duyệt (cần quyền Kế toán thanh toán).", bold_prefix="Danh sách chờ duyệt: ")

b.h2("4. Điều kiện để một hợp đồng lập được Đề nghị xuất hóa đơn")
b.para("Đây là phần quan trọng nhất cần nắm trước khi test. Khi lập phiếu, ô chọn hợp đồng chỉ liệt kê những hợp đồng còn phần cần xuất hóa đơn. Một hợp đồng chỉ xuất hiện khi thỏa ĐỒNG THỜI cả bốn điều kiện sau:")
b.table([
    ["#", "Điều kiện", "Giải thích"],
    ["1", "Hợp đồng đã có hiệu lực trở lên", "Hợp đồng đang ở trạng thái Có hiệu lực / Đang xuất hàng / Đã xuất hàng / Đã thanh lý / Đang quyết toán / Đã quyết toán. Hợp đồng còn Đang tạo hoặc Chờ duyệt sẽ không hiện."],
    ["2", "Đúng loại hợp đồng", "Hợp đồng bán, hợp đồng dự án, đơn hàng nguyên tắc, hoặc phụ lục bổ sung (với hợp đồng hãng). Hợp đồng dịch vụ SC-BD xét theo nhánh riêng tương tự."],
    ["3", "Còn phần chưa xuất hóa đơn", "Phải còn ÍT NHẤT một thứ: (a) một dòng hàng đã xuất kho mà chưa xuất hết hóa đơn, HOẶC (b) một khoản chi phí / doanh thu đã được ghi nhận hoàn thành mà chưa xuất hóa đơn. Nếu hợp đồng đã có hiệu lực nhưng CHƯA xuất kho dòng nào và không có chi phí nào hoàn thành thì KHÔNG có gì để xuất hóa đơn → không hiện."],
    ["4", "Do chính người đang đăng nhập lập", "Hợp đồng phải do chính tài khoản đang đăng nhập tạo. Hợp đồng của người khác (dù cùng phòng) sẽ không hiện trong ô chọn."],
])
b.para("Lưu ý thực tế: điều kiện (3) là lý do phổ biến khiến một hợp đồng đứng tên mình, đã có hiệu lực, nhưng vẫn không hiện ra để chọn — vì chưa phát sinh Phiếu xuất kho nên chưa có hàng nào 'đã giao'. Vì vậy phần lớn công sức chuẩn bị dữ liệu test nằm ở việc tạo cho đủ chuỗi chứng từ tới bước xuất kho (PHẦN 1).")

# ------------------------------------------------- PHAN 1
b.h1("PHẦN 1: CHUẨN BỊ DỮ LIỆU ĐỂ TEST")
b.para("Phần này hướng dẫn dựng đủ dữ liệu để có một hợp đồng hiện ra trong ô chọn và lập được Đề nghị xuất hóa đơn. Lý do cần nhiều bước: Đề nghị xuất hóa đơn chỉ xuất hóa đơn cho phần hàng ĐÃ THỰC GIAO. Hàng chỉ được coi là đã giao sau khi có Phiếu xuất kho; còn chi phí dịch vụ thì sau khi hoàn thành bàn giao / nghiệm thu.")

b.h2("1.1. Chuỗi chứng từ cần dựng (hàng hóa)")
b.para("Với hợp đồng bán hàng hóa, cần đi đủ 4 bước A → D dưới đây, bằng một tài khoản có đủ quyền trên các màn tương ứng. Sau bước D, hợp đồng sẽ đủ điều kiện xuất hóa đơn.")
b.table([
    ["Bước", "Chứng từ cần tạo", "Mục tiêu đạt được"],
    ["A", "Hợp đồng hãng — lập & duyệt tới Có hiệu lực", "Có một hợp đồng đúng loại, có hiệu lực, có dòng hàng hóa (thỏa điều kiện 1 & 2)."],
    ["B", "Yêu cầu xuất hàng (YCXH) từ hợp đồng", "Khởi phát quy trình xuất hàng cho hợp đồng đó."],
    ["C", "Đề nghị xuất kho (ĐNXK) — lập & gửi, Thủ kho tiếp nhận", "Chuyển yêu cầu xuất hàng thành đề nghị gửi kho."],
    ["D", "Phiếu xuất kho (PXK) — Thủ kho thực hiện xuất", "Làm tăng phần 'đã xuất kho' của dòng hàng → thỏa điều kiện 3 (còn phần chưa xuất hóa đơn)."],
])

b.h2("1.2. Bước A — Lập và duyệt Hợp đồng hãng có hiệu lực")
b.bullet("Vào màn Hợp đồng hãng, lập hợp đồng mới: chọn khách hàng, thêm ít nhất một dòng hàng hóa có số lượng, đơn giá.", bold_prefix="A1: ")
b.bullet("Dùng chính tài khoản sẽ dùng để test Đề nghị xuất hóa đơn để lập hợp đồng (thỏa điều kiện 4 — hợp đồng phải do người đăng nhập lập).", bold_prefix="A2: ")
b.bullet("Gửi duyệt và duyệt hợp đồng cho tới khi trạng thái là Có hiệu lực. Khi đó hợp đồng đã thỏa điều kiện 1 & 2.", bold_prefix="A3: ")
b.para("Ở cuối bước A, hợp đồng đã có hiệu lực NHƯNG vẫn chưa hiện trong ô chọn của Đề nghị xuất hóa đơn, vì chưa có dòng hàng nào được xuất kho (điều kiện 3 chưa đạt).")

b.h2("1.3. Bước B — Lập Yêu cầu xuất hàng (YCXH)")
b.bullet("Từ hợp đồng vừa có hiệu lực, lập Yêu cầu xuất hàng cho (các) dòng hàng cần giao.", bold_prefix="B1: ")
b.bullet("Gửi duyệt và duyệt Yêu cầu xuất hàng theo quy trình của màn đó.", bold_prefix="B2: ")

b.h2("1.4. Bước C — Lập và gửi Đề nghị xuất kho (ĐNXK)")
b.bullet("Kế toán kho mở Yêu cầu xuất hàng đã duyệt, lập Đề nghị xuất kho: chọn kho xuất, nhập số lượng đề nghị cho từng dòng.", bold_prefix="C1: ")
b.bullet("Bấm \"Lưu & Gửi\" để chuyển Đề nghị xuất kho sang Chờ duyệt — gửi tới Thủ kho của kho.", bold_prefix="C2: ")

b.h2("1.5. Bước D — Thủ kho lập Phiếu xuất kho (PXK)")
b.bullet("Thủ kho của kho xuất mở Đề nghị xuất kho đang Chờ duyệt, bấm \"Tạo phiếu xuất kho\".", bold_prefix="D1: ")
b.bullet("Chọn lô / số lượng xuất và hoàn tất Phiếu xuất kho.", bold_prefix="D2: ")
b.para("Sau khi Phiếu xuất kho hoàn tất, phần 'đã xuất kho' của các dòng hàng tương ứng tăng lên. Lúc này hợp đồng có dòng hàng đã giao mà chưa xuất hóa đơn → thỏa đủ cả 4 điều kiện và sẽ HIỆN trong ô chọn hợp đồng của màn Đề nghị xuất hóa đơn.")

b.h2("1.6. Trường hợp chi phí / dịch vụ (không đi qua xuất kho)")
b.para("Nếu muốn test xuất hóa đơn cho khoản CHI PHÍ (ví dụ chi phí dịch vụ trên hợp đồng) hoặc cho hợp đồng dịch vụ SC-BD thì không cần đi qua Phiếu xuất kho. Thay vào đó, khoản chi phí / phần việc phải được ghi nhận HOÀN THÀNH qua luồng bàn giao – nghiệm thu của nó. Khi khoản chi phí được đánh dấu đã hoàn thành mà chưa xuất hóa đơn, hợp đồng cũng thỏa điều kiện 3 và sẽ hiện trong ô chọn.")
b.bullet("Hoàn tất biên bản bàn giao / nghiệm thu cho phần việc hoặc chi phí dịch vụ của hợp đồng.", bold_prefix="Cách làm: ")
b.bullet("Chi phí vận chuyển không được tính là khoản cần xuất hóa đơn ở màn này.", bold_prefix="Lưu ý: ")

b.h2("1.7. Kiểm tra nhanh: hợp đồng đã đủ điều kiện chưa?")
b.para("Cách đơn giản nhất không cần tra cơ sở dữ liệu: mở màn Tạo Đề nghị xuất hóa đơn, bấm nút tìm hợp đồng để mở ô chọn. Nếu hợp đồng vừa dựng HIỆN trong danh sách → đã đủ điều kiện, tiến hành test tạo phiếu. Nếu KHÔNG hiện → rà lại theo thứ tự: (1) đúng tài khoản lập hợp đồng chưa; (2) hợp đồng đã Có hiệu lực chưa; (3) đã có Phiếu xuất kho (hoặc chi phí đã hoàn thành) chưa; (4) phần hàng đó đã bị một phiếu xuất hóa đơn khác chiếm hết chưa.")

b.h2("1.8. Lưu ý về tài khoản đăng nhập khi test")
b.para("Vì điều kiện 4 ràng buộc hợp đồng phải do chính người đăng nhập lập, hãy dùng CÙNG một tài khoản xuyên suốt: tài khoản đó vừa lập hợp đồng (bước A) vừa là người đăng nhập lập Đề nghị xuất hóa đơn. Nếu lập hợp đồng bằng tài khoản A rồi đăng nhập tài khoản B để test thì ô chọn sẽ trống dù mọi bước khác đã đúng.")

# ------------------------------------------------- PHAN 2
b.h1("PHẦN 2: TRUY CẬP & DANH SÁCH")

b.h2("2.1. Truy cập & các màn danh sách")
b.table([
    ["Màn", "Dùng cho", "Nội dung"],
    ["Đề nghị xuất hóa đơn (danh sách)", "Người lập / người xem", "Danh sách phiếu trong phạm vi quyền; có nút Thêm mới và Xuất Excel."],
    ["Phiếu đề nghị xuất hóa đơn chờ duyệt", "Người duyệt (Kế toán thanh toán)", "Danh sách phiếu đang Chờ duyệt để duyệt / không duyệt."],
])
img_placeholder(b, "Ảnh menu Công nợ - Thu - Chi với mục Đề nghị xuất hóa đơn.")

b.h2("2.2. Bố cục & bộ lọc danh sách")
b.bullet("tiêu đề \"Danh sách phiếu đề nghị xuất hóa đơn\".", bold_prefix="Thanh tiêu đề: ")
b.bullet("tìm theo mã phiếu, hợp đồng, người lập, trạng thái; lọc theo khoảng ngày lập và khoảng số tiền.", bold_prefix="Khu vực lọc: ")
b.bullet("nút Thêm mới (mở màn tạo phiếu) và nút Xuất Excel.", bold_prefix="Công cụ: ")
b.bullet("bảng liệt kê phiếu, cột Hành động (biểu tượng bánh răng) ở cuối mỗi dòng.", bold_prefix="Bảng danh sách: ")
img_placeholder(b, "Ảnh tổng quan màn danh sách Đề nghị xuất hóa đơn.")

b.h2("2.3. Bảng trạng thái phiếu")
b.table([
    ["Trạng thái", "Ý nghĩa"],
    ["Đang tạo", "Phiếu nháp — đã lưu nhưng chưa gửi duyệt. Người lập được Sửa / Xóa."],
    ["Chờ duyệt", "Đã gửi duyệt, chờ người có quyền duyệt xử lý. Không sửa/xóa được."],
    ["Đã duyệt", "Đã được duyệt — phần hàng tương ứng được đánh dấu đã xuất hóa đơn."],
    ["Không duyệt", "Bị từ chối kèm lý do; phiếu quay về cho người lập Sửa / Xóa lại."],
    ["Hủy", "Phiếu đã hủy."],
])

b.h2("2.4. Thao tác trên từng dòng (cột Hành động)")
b.para("Các nút nằm trong menu bánh răng ở cuối dòng, hiển thị tùy trạng thái và quyền:")
b.table([
    ["Nút", "Điều kiện hiển thị", "Kết quả"],
    ["In", "Luôn có.", "Chọn loại VAT và in phiếu đề nghị xuất hóa đơn."],
    ["Sửa", "Phiếu Đang tạo hoặc Không duyệt, do chính bạn lập.", "Mở màn sửa phiếu."],
    ["Xóa", "Phiếu Đang tạo hoặc Không duyệt, do chính bạn lập.", "Xóa phiếu (có xác nhận)."],
    ["Duyệt", "Phiếu Chờ duyệt và bạn có quyền \"Duyệt đề nghị xuất hóa đơn\".", "Mở trang chi tiết để Duyệt / Không duyệt."],
])
b.para("Mã phiếu và mã hợp đồng trên mỗi dòng đều bấm được để mở chi tiết tương ứng.")

# ------------------------------------------------- PHAN 3
b.h1("PHẦN 3: TẠO ĐỀ NGHỊ XUẤT HÓA ĐƠN")

b.h2("3.1. Mở màn tạo phiếu")
b.para("Tại màn danh sách, bấm nút Thêm mới để mở màn tạo phiếu đề nghị xuất hóa đơn.")
img_placeholder(b, "Ảnh màn tạo phiếu đề nghị xuất hóa đơn (chưa chọn hợp đồng).")

b.h2("3.2. Chọn hợp đồng")
b.bullet("Bấm nút tìm (biểu tượng kính lúp) cạnh ô Hợp đồng để mở ô chọn hợp đồng.", bold_prefix="Bước 1: ")
b.bullet("Ô chọn chỉ liệt kê những hợp đồng đủ điều kiện xuất hóa đơn (xem TỔNG QUAN mục 4). Chọn hợp đồng cần lập.", bold_prefix="Bước 2: ")
b.para("Sau khi chọn, hệ thống tự điền thông tin khách hàng và nạp danh sách hàng hóa / dịch vụ / chi phí còn cần xuất hóa đơn của hợp đồng vào phần Chi tiết.")
b.para("Nếu ô chọn trống hoặc thiếu hợp đồng mong đợi: hợp đồng đó chưa thỏa đủ 4 điều kiện — quay lại PHẦN 1 để dựng tiếp dữ liệu.")
img_placeholder(b, "Ảnh ô chọn hợp đồng với danh sách hợp đồng đủ điều kiện.")

b.h2("3.3. Thông tin chung")
b.table([
    ["Trường", "Bắt buộc", "Nhập được?", "Ghi chú"],
    ["Hợp đồng", "Có", "Chọn qua ô tìm", "Chọn từ ô chọn hợp đồng; không gõ tay."],
    ["Ngày bàn giao", "Có", "Có", "Ngày bàn giao của phần hàng; chỉnh được khi tạo."],
    ["Khách hàng trên hợp đồng", "—", "Không", "Tự điền theo hợp đồng (chỉ đọc)."],
    ["Khách hàng xuất hóa đơn", "—", "Có", "Mặc định theo hợp đồng; sửa được nếu xuất hóa đơn cho bên khác."],
    ["Mã số thuế", "—", "Không", "Tự điền theo khách hàng (chỉ đọc)."],
    ["Địa chỉ", "—", "Có", "Địa chỉ xuất hóa đơn; sửa được."],
    ["Số tài khoản", "—", "Không", "Tự điền (chỉ đọc)."],
    ["Ghi chú", "—", "Không", "Kế thừa theo hợp đồng (chỉ đọc)."],
    ["File đính kèm", "Có", "Có", "Bắt buộc đính kèm tài liệu; chấp nhận các định dạng tài liệu / ảnh thông dụng."],
])
img_placeholder(b, "Ảnh khối Thông tin chung đã điền.")

b.h2("3.4. Bảng Chi tiết & các tab")
b.para("Phần Chi tiết hiện sau khi đã chọn hợp đồng, chia theo tab tùy hợp đồng có gì: Hàng hóa, Dịch vụ, Chi phí. Mỗi dòng thể hiện phần còn cần xuất hóa đơn.")
b.table([
    ["Cột", "Nhập được?", "Ghi chú"],
    ["STT", "Không", "Số thứ tự dòng."],
    ["Cần xuất", "Có (ô tích)", "Tích để đưa dòng vào hóa đơn. Bỏ tích → dòng không tính và không nhập số lượng."],
    ["Hàng hóa / Dịch vụ / Nguồn / ĐVT", "Không", "Thông tin dòng, lấy theo hợp đồng."],
    ["SL được xuất HĐ", "Không", "Số lượng tối đa được xuất hóa đơn (phần đã giao, chưa xuất hóa đơn)."],
    ["SL cần xuất HĐ", "Có (nhập số)", "Số lượng đề nghị xuất hóa đơn cho dòng; không được vượt SL được xuất HĐ."],
    ["Đơn giá bán / Thành tiền / Giảm giá / Đơn giá sau giảm / Thành tiền sau giảm", "Không", "Tính tự động theo hợp đồng và số lượng."],
    ["VAT (% và Tiền VAT)", "Có (chọn %)", "Chọn mức thuế suất cho dòng; tiền VAT tính tự động."],
    ["Thành tiền sau VAT", "Không", "Tính tự động."],
])
b.para("Cuối mỗi tab có dòng tổng cộng (tổng thành tiền, tổng giảm giá, tổng tiền VAT, tổng thành tiền sau VAT).")
img_placeholder(b, "Ảnh bảng Chi tiết với tab Hàng hóa.")

b.h2("3.5. Lưu phiếu & quy tắc kiểm tra")
b.table([
    ["Nút", "Hành động"],
    ["Lưu", "Lưu phiếu ở trạng thái Đang tạo (nháp)."],
    ["Lưu và gửi duyệt", "Gửi phiếu đi duyệt — chuyển trạng thái Chờ duyệt."],
    ["Quay lại", "Về danh sách, không lưu."],
])
b.para("Quy tắc kiểm tra khi lưu: phải chọn hợp đồng; nhập Ngày bàn giao; đính kèm file; có ít nhất một dòng được tích \"Cần xuất\" với số lượng lớn hơn 0; không dòng nào có SL cần xuất HĐ vượt SL được xuất HĐ. Số nhập sai sẽ được báo lỗi ngay tại dòng, phiếu không lưu cho tới khi sửa đủ.")
b.para("Ảnh hưởng của thao tác: khi Lưu (nháp) hoặc Gửi duyệt, phần số lượng/chi phí đưa vào phiếu được đánh dấu 'đang xuất hóa đơn' nên tạm thời không còn khả dụng cho phiếu khác.")

# ------------------------------------------------- PHAN 4
b.h1("PHẦN 4: SỬA & XÓA PHIẾU")
b.h2("4.1. Điều kiện")
b.para("Chỉ Sửa / Xóa được phiếu ở trạng thái Đang tạo hoặc Không duyệt, và do chính người đăng nhập lập. Phiếu đã gửi (Chờ duyệt) hoặc đã duyệt thì không sửa/xóa được.")
b.h2("4.2. Cách thực hiện")
b.bullet("Vào menu bánh răng trên dòng phiếu, bấm Sửa; chỉnh số lượng / VAT / thông tin xuất hóa đơn rồi Lưu hoặc Lưu và gửi duyệt.", bold_prefix="Sửa: ")
b.bullet("Vào menu bánh răng, bấm Xóa và xác nhận. Khi xóa, phần số lượng/chi phí đang giữ trong phiếu được hoàn trả để dùng cho phiếu khác.", bold_prefix="Xóa: ")

# ------------------------------------------------- PHAN 5
b.h1("PHẦN 5: DUYỆT / KHÔNG DUYỆT")
b.para("Việc duyệt thực hiện ở trang Chi tiết của phiếu, dành cho người có quyền \"Duyệt đề nghị xuất hóa đơn\" và chỉ với phiếu đang Chờ duyệt.")
b.h2("5.1. Mở phiếu để duyệt")
b.para("Từ danh sách (hoặc danh sách Chờ duyệt), bấm Duyệt trên dòng phiếu, hoặc mở mã phiếu để vào trang Chi tiết. Cuối trang có nút Duyệt và Không duyệt.")
img_placeholder(b, "Ảnh trang chi tiết phiếu với nút Duyệt / Không duyệt.")
b.h2("5.2. Duyệt")
b.bullet("Bấm Duyệt. Phiếu chuyển sang Đã duyệt; phần hàng / chi phí trong phiếu được đánh dấu đã xuất hóa đơn và được ghi vào lịch sử duyệt. Hệ thống gửi thông báo cho người lập.", bold_prefix="Thao tác: ")
b.h2("5.3. Không duyệt (từ chối)")
b.bullet("Bấm Không duyệt, nhập lý do (bắt buộc) rồi xác nhận. Phiếu chuyển sang Không duyệt; phần số lượng/chi phí đang giữ được hoàn trả; người lập nhận thông báo để sửa và gửi lại.", bold_prefix="Thao tác: ")

# ------------------------------------------------- PHAN 6
b.h1("PHẦN 6: XEM CHI TIẾT, IN & XUẤT EXCEL")
b.table([
    ["Chức năng", "Nội dung"],
    ["Xem chi tiết", "Bấm mã phiếu để mở trang chi tiết (chỉ đọc): thông tin chung, bảng chi tiết kèm đơn giá/thành tiền, trạng thái, lịch sử duyệt."],
    ["In", "Từ menu bánh răng chọn In; chọn loại VAT cần in rồi in phiếu."],
    ["Xuất Excel", "Nút trên màn danh sách — tải danh sách phiếu theo bộ lọc hiện tại ra Excel."],
])

# ------------------------------------------------- PHAN 7
b.h1("PHẦN 7: KỊCH BẢN KIỂM THỬ GỢI Ý")
b.para("Bộ kịch bản dưới đây bám theo dữ liệu dựng ở PHẦN 1. Thực hiện bằng tài khoản đã lập hợp đồng.")
b.table([
    ["Mã", "Tình huống", "Bước thực hiện", "Kết quả mong đợi"],
    ["TC-01", "Hợp đồng có hiệu lực nhưng chưa xuất kho", "Dừng sau bước A (chưa làm B–D). Mở màn tạo, bấm chọn hợp đồng.", "Hợp đồng KHÔNG hiện trong ô chọn (chưa có hàng đã giao)."],
    ["TC-02", "Hợp đồng đã có Phiếu xuất kho", "Làm đủ A–D. Mở màn tạo, bấm chọn hợp đồng.", "Hợp đồng HIỆN trong ô chọn; chọn được và nạp dòng hàng với SL được xuất HĐ > 0."],
    ["TC-03", "Lưu nháp", "Chọn hợp đồng, tích dòng, nhập SL cần xuất HĐ hợp lệ, chọn VAT, đính kèm file, nhập Ngày bàn giao → bấm Lưu.", "Phiếu tạo ở trạng thái Đang tạo; về danh sách thấy phiếu; có nút Sửa/Xóa."],
    ["TC-04", "Gửi duyệt", "Mở phiếu nháp, bấm Lưu và gửi duyệt (hoặc gửi ngay khi tạo).", "Phiếu chuyển Chờ duyệt; không còn nút Sửa/Xóa."],
    ["TC-05", "Nhập vượt số được xuất", "Nhập SL cần xuất HĐ lớn hơn SL được xuất HĐ ở một dòng, bấm Lưu.", "Báo lỗi tại dòng; phiếu không được lưu."],
    ["TC-06", "Thiếu dữ liệu bắt buộc", "Bỏ trống Ngày bàn giao hoặc không đính kèm file, bấm Lưu.", "Báo thiếu trường bắt buộc; phiếu không được lưu."],
    ["TC-07", "Duyệt phiếu", "Bằng tài khoản có quyền Duyệt đề nghị xuất hóa đơn, mở phiếu Chờ duyệt, bấm Duyệt.", "Phiếu chuyển Đã duyệt; phần hàng được đánh dấu đã xuất hóa đơn; có dòng trong lịch sử duyệt."],
    ["TC-08", "Hợp đồng đã xuất hóa đơn hết", "Sau TC-07, mở lại màn tạo, bấm chọn hợp đồng.", "Hợp đồng không còn hiện (nếu đã xuất hóa đơn hết phần đã giao), hoặc chỉ còn phần chưa xuất."],
    ["TC-09", "Không duyệt", "Mở phiếu Chờ duyệt, bấm Không duyệt, nhập lý do.", "Phiếu chuyển Không duyệt; phần đang giữ được hoàn trả; người lập thấy lại nút Sửa/Xóa."],
    ["TC-10", "Ràng buộc người lập", "Lập hợp đồng bằng tài khoản A, đăng nhập tài khoản B mở màn tạo chọn hợp đồng.", "Hợp đồng của A KHÔNG hiện cho B (đúng điều kiện người đăng nhập)."],
])

# ------------------------------------------------- PHAN 8
b.h1("PHẦN 8: CÂU HỎI THƯỜNG GẶP")
b.table([
    ["Tình huống", "Giải thích / cách xử lý"],
    ["Hợp đồng đứng tên mình, đã có hiệu lực, nhưng không hiện trong ô chọn", "Thường do chưa có hàng đã giao: cần có Phiếu xuất kho (hàng hóa) hoặc chi phí đã hoàn thành (dịch vụ). Xem PHẦN 1 bước D / mục 1.6."],
    ["Ô chọn hợp đồng trống hoàn toàn", "Kiểm tra: đúng tài khoản lập hợp đồng chưa (điều kiện người đăng nhập); hợp đồng đã Có hiệu lực chưa; đã phát sinh xuất kho chưa."],
    ["Không nhập được số lượng ở một dòng", "Dòng chưa được tích \"Cần xuất\". Tích ô Cần xuất rồi mới nhập SL cần xuất HĐ."],
    ["Báo lỗi khi lưu dù đã nhập số lượng", "Kiểm tra: đã nhập Ngày bàn giao, đã đính kèm file bắt buộc, và không dòng nào vượt SL được xuất HĐ."],
    ["Không thấy nút Sửa / Xóa", "Hai nút này chỉ có với phiếu Đang tạo hoặc Không duyệt, do chính bạn lập. Phiếu đã gửi/đã duyệt thì không sửa/xóa."],
    ["Không thấy nút Duyệt", "Cần quyền \"Duyệt đề nghị xuất hóa đơn\" và phiếu phải đang Chờ duyệt."],
    ["Sau khi duyệt, cùng phần hàng không lập được phiếu mới", "Đúng nghiệp vụ — phần đã duyệt được đánh dấu đã xuất hóa đơn, không đưa vào phiếu mới nữa."],
])

# ============================================================ FINISH
finish_macos(b)
print("XONG.")
