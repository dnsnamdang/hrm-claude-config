# -*- coding: utf-8 -*-
"""Sinh testcase - Duyet gia ban (luong Chuyen doi hang hoa).

Doi chieu code worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa (hrm-api 39c4a91fe,
hrm-client 5c14659e8 — 16/10/2026). SRS cung bo: gen_srs_duyet-gia-ban.py.
Section VI danh rieng cho GIA BAN (gia nguoi duyet sua, he so -> gia, gia hieu luc doi ngay, gia dang chay da doi,
gia von de nghi, quyen Xem gia von). So lieu mau: hang that TEWI-AQUA (gia von Cty 1 = 195,989,760, Ban le 341,000,000
he so 1.6) va SULI-IN-2716-WHEEL-NO12 / -NO14; gia de nghi la so lieu minh hoa (DB dev khong co yeu cau cho duyet).
Chay: python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_testcase_duyet-gia-ban.py
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase - Duyệt giá bán.xlsx")


def L(*lines):
    return "\n".join(lines)


def T(n, func, prio, pre, steps, data, exp):
    return (n, func, prio, pre if isinstance(pre, str) else L(*pre), steps if isinstance(steps, str) else L(*steps),
            data if isinstance(data, str) else L(*data), exp if isinstance(exp, str) else L(*exp))


MENU = "Vào phân hệ Tài chính › Quản lý giá - CTKM › nhóm “Giá bán” › bấm “Duyệt giá bán”"
MENU2 = "Vào phân hệ Tài chính › Chờ duyệt › nhóm “Giá bán chờ duyệt” › bấm “Hàng hoá chờ duyệt giá bán”"
Q1 = "Duyệt giá bán hàng hoá"
Q2 = "Xem giá vốn hàng hoá"
Q3 = "Cập nhật giá bán hàng hoá"
GONE = "Yêu cầu duyệt đã được xử lý."
ACC_A = "Tài khoản A có quyền " + Q1 + " và " + Q2 + " tại công ty A, đang chọn công ty A."
ACC_B = "Tài khoản B chỉ có quyền " + Q1 + " tại công ty A (KHÔNG có " + Q2 + "), đang chọn công ty A."
PROP = "Người đề nghị P (có quyền " + Q3 + " tại công ty A; công ty A đã bật duyệt giá cho mọi hãng) đã Gửi duyệt 3 yêu cầu:"
YC1 = ("- YC1 TEWI-AQUA (Bộ): giá vốn đề nghị 195,989,760 (bằng giá vốn đang chạy); 5 loại giá Bán lẻ, Giá bán theo lô, "
       "Đại lý cấp 1, 2, 3 giá cũ 341,000,000 hệ số 1.6 sang giá mới 333,182,600 hệ số 1.7, ĐMGG 5; TMĐT 0 sang 433,137,380 "
       "hệ số 2.21; 1 giá hiệu lực Bán lẻ 350,000,000 hệ số 1.79 ngày 15/10/2026 (hôm nay 16/10/2026); lý do sửa giá "
       "“Điều chỉnh theo bảng giá hãng tháng 10/2026”.")
YC2 = "- YC2 SULI-IN-2716-WHEEL-NO14 (Cái): chỉ đổi giá vốn 2,915,000 sang 3,100,000."
YC3 = ("- YC3 SULI-IN-2716-WHEEL-NO12 (Cái): giá vốn 1,457,500; Bán lẻ và Giá bán theo lô giá cũ 2,915,000 hệ số 2 sang "
       "3,206,500 hệ số 2.2; SAU khi gửi, phiếu tính giá đã đổi giá Bán lẻ đang chạy thành 3,000,000.")
DATA3 = [PROP, YC1, YC2, YC3]
NOPERM = "Bạn không có quyền thực hiện chức năng này."

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     L("Màn Duyệt giá bán (phân hệ Tài chính) là nơi người có quyền " + Q1 + " xử lý các ĐỀ NGHỊ GIÁ BÁN của công ty mình:",
       "- Mỗi yêu cầu = 1 hàng × 1 ĐVT × 1 công ty: giá vốn đề nghị + các dòng giá đổi (giá đang áp dụng và giá hiệu lực).",
       "- Người duyệt sửa được Hệ số / Giá mới / ĐMGG mới / ngày hiệu lực rồi Duyệt: hệ thống áp ĐÚNG giá đã sửa.",
       "- Không duyệt bắt buộc lý do: giá đang áp dụng giữ nguyên, người đề nghị thấy nhãn Không duyệt kèm lý do.",
       "- Duyệt / Không duyệt từng yêu cầu hoặc hàng loạt; Xuất Excel; popup Lịch sử giá.",
       "- Yêu cầu sinh ra từ màn Cập nhật giá bán (công ty bật duyệt giá) và từ Phiếu tính giá.")),
    ("2. Đối tượng được tính / hiển thị",
     L("- Yêu cầu duyệt giá ĐANG CHỜ có công ty bộ giá = công ty đang làm việc, của mọi người đề nghị.",
       "- Gồm yêu cầu từ màn Cập nhật giá bán và từ Phiếu tính giá (hiển thị giống nhau).",
       "- Mỗi yêu cầu hiện các dòng giá có thay đổi theo thứ tự Bán lẻ, Giá bán theo lô, Đại lý cấp 1, 2, 3, TMĐT; giá hiệu "
       "lực nằm ngay dưới loại giá của nó.",
       "- Yêu cầu chỉ đổi giá vốn: 1 dòng “Chỉ đổi giá vốn — không đổi giá bán”.",
       "- Có quyền " + Q2 + ": thêm cột Giá vốn và Hệ số.")),
    ("3. Đối tượng bị ẩn / không tính",
     L("- Yêu cầu của công ty KHÁC (dù cùng mã hàng, dù người duyệt có quyền ở công ty đó).",
       "- Yêu cầu đã Duyệt / Không duyệt (bị xoá khỏi danh sách chờ ngay khi xử lý).",
       "- Yêu cầu bị đóng vì người đề nghị lưu thẳng ở màn Cập nhật giá bán, hoặc vì hàng bị gỡ / xoá ở công ty.",
       "- Không có quyền " + Q2 + ": giá vốn, giá vốn cũ, hệ số cũ / mới (không hiện ở màn, Excel).")),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng — màn không có ô lọc thời gian. Popup Lịch sử giá có Từ ngày / Đến ngày lọc theo thời điểm thay đổi."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     L("- Yêu cầu (hàng × ĐVT × công ty) › dòng giá (loại giá đang áp dụng / giá hiệu lực).",
       "- Bộ lọc cây phân loại: Tính chất › Nhóm công nghệ › Nhóm sản phẩm › Loại sản phẩm (đổi cấp trên xoá cấp dưới).",
       "- Ô lọc Hãng sản xuất và Người cập nhật chỉ liệt kê giá trị CÓ trong yêu cầu đang chờ của công ty.")),
    ("6. Quy tắc cộng dồn / deduplicate",
     L("- Mỗi hàng × ĐVT × công ty tối đa 1 yêu cầu đang mở: người đề nghị gửi lại là ghi đè yêu cầu cũ.",
       "- Dòng đếm và chân bảng đếm số YÊU CẦU (không phải số dòng giá).",
       "- Lịch sử: mỗi lần Duyệt / Không duyệt 1 dòng, chỉ ghi ô thực sự đổi.")),
    ("7. Phân quyền cấp",
     L("Màn KHÔNG phân quyền theo cấp; quyền xét theo CÔNG TY ĐANG LÀM VIỆC:",
       "- " + Q1 + ": quyền bắt buộc của mọi chức năng (xem, sửa giá đề nghị, Duyệt, Không duyệt, hàng loạt, Excel, Lịch sử); "
       "người có quyền này là người nhận thông báo “[GIA] Chờ duyệt”.",
       "- " + Q2 + ": chỉ có tác dụng khi có " + Q1 + " — thấy Giá vốn + Hệ số, sửa được Hệ số, Excel có 2 cột này.",
       "- " + Q3 + ": không mở được màn; người có " + Q1 + " + " + Q3 + " mà không có " + Q2 + " thấy giá vốn TRONG popup Lịch "
       "sử giá (bảng vẫn ẩn).",
       "Super admin không được miễn.")),
    ("8. Cách tính các ô thống kê",
     L("- Dòng đếm: “· N yêu cầu chờ duyệt tại <công ty>”, N = tổng số yêu cầu khớp bộ lọc.",
       "- Chân bảng: “Hiển thị a–b / N yêu cầu”.",
       "- Chênh lệch dưới Giá mới = Giá mới trừ Giá cũ (giá lúc đề nghị): dấu cộng xanh lá khi tăng, dấu trừ cam khi giảm.",
       "- Gõ hệ số: Giá mới = làm tròn TRĂM (hệ số × giá vốn đề nghị). Vd 1.75 × 195,989,760 ra 342,982,100.",
       "- Ngày hiệu lực trước ngày mai: khi duyệt dời về ngày mai.",
       "- Ngày trong thông báo Đã duyệt: hôm nay nếu có dòng giá đang áp dụng, ngược lại là ngày hiệu lực sớm nhất.")),
    ("9. Ghi chú đọc bảng",
     L("- Số theo chuẩn quốc tế: dấu phẩy ngăn nghìn, dấu chấm thập phân (1.7). Ngày dd/mm/yyyy.",
       "- Bẫy 1: sửa Bán lẻ ở màn Duyệt KHÔNG lan sang 4 loại giá còn lại và KHÔNG tự tính TMĐT (khác màn Cập nhật giá bán).",
       "- Bẫy 2: Duyệt áp giá ĐANG HIỆN TRÊN MÀN (đã sửa), không phải giá người đề nghị gửi.",
       "- Bẫy 3: giá đang chạy đã đổi sau khi đề nghị VẪN duyệt được — chỉ có cảnh báo.",
       "- Bẫy 4: không có " + Q2 + " thì khi duyệt hệ số giữ nguyên bản đề nghị dù đã sửa giá.",
       "- Bẫy 5: hàng bị khoá / Ngừng kinh doanh sau khi gửi đề nghị vẫn duyệt được (chờ nghiệp vụ xác nhận).",
       "- Bẫy 6: ô đã tick và giá đã sửa được giữ khi lọc / đổi trang — Duyệt hàng loạt xử lý cả yêu cầu đang bị lọc ẩn.",
       "- Môi trường thử: 8 công ty đều TẮT duyệt giá, DB không có yêu cầu chờ — trước khi test phải bật duyệt giá cho công ty "
       "A ở màn Quy định và cho tài khoản P Gửi duyệt ở màn Cập nhật giá bán để tạo yêu cầu.",
       "- Ca Duyệt đổi giá thật: ghi lại giá trước khi test và trả lại sau khi test.",
       "- Nhóm ca 'gọi thẳng chức năng, bỏ qua giao diện' dành cho tester kỹ thuật (dùng công cụ kiểm thử API).")),
]

# ------------------------------------------------------------------ PHAN QUYEN
ROLE_TCS = [
    ("01", "Có " + Q1 + " + " + Q2 + " tại công ty đang làm việc", "P0", [ACC_A] + DATA3,
     ["1. Đăng nhập A, chọn công ty A.", "2. " + MENU + "."], "—",
     ["- Thấy mục “Duyệt giá bán” trong nhóm Giá bán.", "- Màn mở, dòng đếm “· 3 yêu cầu chờ duyệt tại …”.",
      "- Có cột Giá vốn và Hệ số; mỗi yêu cầu có nút Duyệt, Không duyệt, Lịch sử giá."]),
    ("02", "Có " + Q1 + " nhưng KHÔNG có " + Q2, "P0", [ACC_B] + DATA3,
     ["1. Đăng nhập B.", "2. " + MENU + "."], "—",
     ["- Màn mở, đủ 3 yêu cầu.", "- KHÔNG có cột Giá vốn, KHÔNG có cột Hệ số (bảng 13 cột).",
      "- Yêu cầu YC2 chỉ thấy dòng “Chỉ đổi giá vốn — không đổi giá bán”, không thấy số giá vốn."]),
    ("03", "Không có quyền nào của màn", "P0", ["Tài khoản C không có quyền " + Q1 + " ở bất kỳ công ty nào."],
     ["1. Đăng nhập C.", "2. Mở phân hệ Tài chính › Quản lý giá - CTKM › Giá bán.", "3. Mở phân hệ Tài chính › Chờ duyệt.",
      "4. Mở lại màn Duyệt giá bán từ lịch sử trình duyệt."], "—",
     ["- Không có mục “Duyệt giá bán”, không có mục “Hàng hoá chờ duyệt giá bán”.",
      "- Mở lại màn: không hiển thị bảng, không lộ yêu cầu / giá nào.", "- Không bật thông báo lỗi liên tục."]),
    ("04", "Có quyền ở công ty KHÁC, không có ở công ty đang làm việc", "P0",
     ["Tài khoản D có quyền " + Q1 + " tại công ty B, KHÔNG có tại công ty A.", "Công ty A có 3 yêu cầu; công ty B có 1 yêu cầu."],
     ["1. Đăng nhập D, chọn công ty A, quan sát menu.", "2. Đổi sang công ty B, mở màn."], "—",
     ["- Công ty A: không thấy 2 mục menu.", "- Công ty B: thấy mục, màn chỉ hiện 1 yêu cầu của công ty B.",
      "- Lưu ý: quyền phải gán Ở ĐÚNG công ty đang làm việc."]),
    ("05", "Chỉ có " + Q2 + " (không có " + Q1 + ")", "P0", ["Tài khoản E chỉ có quyền " + Q2 + " tại công ty A."],
     ["1. Đăng nhập E.", "2. Mở nhóm Giá bán và nhóm Chờ duyệt."], "—",
     ["- Không có mục Duyệt giá bán / Hàng hoá chờ duyệt giá bán.", "- Không xem được yêu cầu nào."]),
    ("06", "Chỉ có " + Q3 + " (không có " + Q1 + ")", "P1", ["Tài khoản P chỉ có quyền " + Q3 + " tại công ty A."],
     ["1. Đăng nhập P.", "2. Mở nhóm Giá bán."], "—",
     ["- Có mục Cập nhật giá bán, KHÔNG có mục Duyệt giá bán.", "- Người đề nghị không tự duyệt được đề nghị của mình nếu không có " + Q1 + "."]),
    ("07", "Có " + Q1 + " + " + Q3 + ", không có " + Q2 + ": lịch sử có giá vốn", "P1",
     ["Tài khoản G có " + Q1 + " và " + Q3 + " tại công ty A, không có " + Q2 + ".", "TEWI-AQUA đã có lịch sử đổi giá vốn tại công ty A."],
     ["1. Đăng nhập G, mở màn.", "2. Bấm Lịch sử giá ở YC1."], "—",
     ["- Bảng KHÔNG có cột Giá vốn, Hệ số.", "- Popup Lịch sử CÓ dòng “Giá vốn (Bộ)” và trường Hệ số.",
      "- Lưu ý: khác tài khoản B (chỉ " + Q1 + ") — xem TC_06.009."]),
    ("08", "Super admin chưa được gán quyền " + Q1, "P1",
     ["Tài khoản quản trị cao nhất, không được gán quyền " + Q1 + " tại công ty A."],
     ["1. Đăng nhập, chọn công ty A.", "2. Mở nhóm Giá bán."], "—", ["- Không có mục Duyệt giá bán (không được miễn quyền)."]),
    ("09", "Bỏ qua giao diện: xem danh sách / Excel khi không có quyền", "P0", ["Tài khoản C không có quyền " + Q1 + "."] + DATA3,
     ["1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy danh sách yêu cầu duyệt giá.", "2. Gọi thẳng chức năng Xuất Excel.",
      "3. Gọi thẳng chức năng Lịch sử giá của TEWI-AQUA."], "—",
     ["- Cả 3 bị từ chối, báo không có quyền (“" + NOPERM + "”).", "- Không trả về giá / giá vốn nào."]),
    ("10", "Bỏ qua giao diện: Duyệt khi không có quyền", "P0", ["Tài khoản C không có quyền " + Q1 + "."] + DATA3,
     ["1. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt YC1.", "2. Gọi thẳng chức năng Duyệt hàng loạt YC1, YC3."], "—",
     ["- Hệ thống từ chối, báo không có quyền.", "- Giá Bán lẻ TEWI-AQUA vẫn 341,000,000; YC1, YC3 vẫn ở danh sách chờ."]),
    ("11", "Bỏ qua giao diện: Không duyệt khi không có quyền", "P0", ["Tài khoản C không có quyền " + Q1 + "."] + DATA3,
     ["1. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt YC1 với lý do “x”.", "2. Gọi thẳng Không duyệt hàng loạt."], "—",
     ["- Hệ thống từ chối, báo không có quyền.", "- YC1 vẫn chờ, không có nhãn Không duyệt ở màn Cập nhật giá bán."]),
    ("12", "Bỏ qua giao diện: có quyền ở công ty B, duyệt yêu cầu của công ty A", "P0",
     ["Tài khoản D có quyền " + Q1 + " tại công ty B, không có tại công ty A; đang chọn công ty B.", "YC1 thuộc công ty A."],
     ["1. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt YC1 (đang ở công ty B)."], "—",
     ["- Hệ thống báo “" + GONE + "” (không lộ là có yêu cầu ở công ty khác).", "- Giá công ty A và B đều không đổi; YC1 vẫn chờ ở công ty A."]),
    ("13", "Bỏ qua giao diện: không có " + Q2 + " mà gửi kèm hệ số khi duyệt", "P0", [ACC_B] + DATA3,
     ["1. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt YC1, gửi kèm hệ số 3 cho dòng Bán lẻ, giá 333,182,600."], "—",
     ["- Duyệt thành công; hệ số Bán lẻ được áp là 1.7 (bản đề nghị), KHÔNG phải 3.",
      "- Danh sách của B không bao giờ chứa giá vốn / hệ số dù gọi thẳng chức năng lấy danh sách."]),
]

# ------------------------------------------------------------------ I
S1 = [
    T(1, "Mở màn từ lối vào chính", "P0", [ACC_A] + DATA3, ["1. " + MENU + "."], "—",
      ["- Tiêu đề trang và tiêu đề khối “Duyệt giá bán”.", "- Dòng đếm “· 3 yêu cầu chờ duyệt tại <tên công ty A>”.",
       "- Chân bảng “Hiển thị 1–3 / 3 yêu cầu”, mặc định 20 dòng / trang."]),
    T(2, "Mở màn từ lối vào phụ (Chờ duyệt)", "P0", [ACC_A] + DATA3, ["1. " + MENU2 + "."], "—",
      ["- Mở đúng màn Duyệt giá bán.", "- Cùng 3 yêu cầu, cùng dòng đếm như TC_01.001 (cùng phạm vi)."]),
    T(3, "Mở từ thông báo “[GIA] Chờ duyệt” của 1 yêu cầu", "P0", [ACC_A, PROP, YC1, YC2, YC3],
      ["1. Bấm chuông thông báo.", "2. Bấm thông báo “[GIA] Chờ duyệt: SULI-IN-2716-WHEEL-NO14 – Bánh xe – Model: wheelφ25. Người đề nghị: <P>”."], "—",
      ["- Màn mở, CHỈ hiện YC2.", "- Dòng đếm “· 1 yêu cầu chờ duyệt …”."]),
    T(4, "Mở thông báo của yêu cầu đã được xử lý", "P0", [ACC_A, "YC2 đã được người khác duyệt; A còn thông báo Chờ duyệt cũ của YC2."],
      ["1. Bấm thông báo “[GIA] Chờ duyệt” của YC2."], "—",
      ["- Cảnh báo “Yêu cầu đã được xử lý”.", "- Bảng rỗng: “Không có dữ liệu phù hợp”, không treo trang."]),
    T(5, "Mở từ thông báo gộp của Phiếu tính giá", "P1",
      [ACC_A, "Phiếu tính giá PTG01 của công ty A vừa gửi duyệt 4 dòng giá."],
      ["1. Bấm thông báo “[GIA] Chờ duyệt: PTG01. 4 dòng giá. Người đề nghị: <tên>”."], "—",
      ["- Màn mở với TOÀN BỘ danh sách (không lọc riêng phiếu).", "- 4 yêu cầu của PTG01 có trong danh sách."]),
    T(6, "Thông báo lọc sẵn bị bỏ khi Tìm kiếm / Làm mới", "P1", [ACC_A] + DATA3,
      ["1. Mở từ thông báo của YC2 (TC_01.003).", "2. Bấm Làm mới."], "—",
      ["- Sau bước 2: hiện đủ 3 yêu cầu, dòng đếm 3."]),
    T(7, "Lối vào từ hệ thống ERP", "P1", [ACC_A, "Tài khoản A đăng nhập ERP."],
      ["1. Trên ERP mở menu Chờ duyệt.", "2. Bấm “Duyệt giá bán (HRM)”.", "3. Trên ERP mở đường vào màn duyệt giá cũ."], "—",
      ["- Bước 2: mở màn Duyệt giá bán của hệ thống mới ở tab mới.", "- Bước 3: được chuyển sang màn Duyệt giá bán của hệ thống mới."]),
    T(8, "Bảng đủ 15 cột, tiêu đề 1 dòng", "P1", [ACC_A] + DATA3, ["1. Mở màn.", "2. Đọc tiêu đề cột trái sang phải."], "—",
      ["- Ô tick, #, Tên hàng hoá, ĐVT, Giá vốn, Loại giá, Giá cũ, Hệ số, Giá mới, ĐMGG cũ, ĐMGG mới, Hiệu lực, Người cập nhật, Thời gian, Mã hàng hoá.",
       "- Mọi tiêu đề nằm trên 1 dòng.", "- Chỉ cột Giá vốn có icon thông tin."]),
    T(9, "Nội dung icon thông tin cột Giá vốn", "P2", [ACC_A] + DATA3, ["1. Rê chuột vào icon thông tin cạnh tiêu đề Giá vốn."], "—",
      ["- “Giá vốn người đề nghị gửi kèm — áp vào công ty khi Duyệt (không sửa ở màn này).”"]),
    T(10, "Không có yêu cầu nào", "P1", [ACC_A, "Công ty A không có yêu cầu chờ duyệt."], ["1. Mở màn."], "—",
      ["- Dòng đếm “· 0 yêu cầu chờ duyệt …”.", "- Bảng “Không có yêu cầu duyệt giá nào”.", "- Ô tick tiêu đề bị khoá."]),
    T(11, "Đổi công ty đang làm việc", "P0",
      ["Tài khoản A có quyền " + Q1 + " ở công ty A (3 yêu cầu) và công ty B (1 yêu cầu)."],
      ["1. Mở màn ở công ty A.", "2. Đổi công ty đang làm việc sang B.", "3. Mở lại màn."], "—",
      ["- Công ty A: 3 yêu cầu. Công ty B: đúng 1 yêu cầu của B.", "- Không còn thấy yêu cầu của công ty A."]),
    T(12, "Rời màn khi đã sửa giá chưa duyệt", "P1", [ACC_A] + DATA3,
      ["1. Sửa hệ số Bán lẻ YC1 thành 1.75.", "2. Bấm sang mục menu khác.", "3. Chọn Ở lại.", "4. Bấm lại mục menu khác, chọn Thoát."],
      "Hệ số: 1.75",
      ["- Bước 2: hộp thoại “Thông tin chưa lưu” — “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”.",
       "- Bước 3: ở lại màn, hệ số vẫn 1.75.", "- Bước 4: rời màn; mở lại thấy giá đề nghị gốc (hệ số 1.7)."]),
    T(13, "Rời màn khi chưa sửa gì", "P2", [ACC_A] + DATA3, ["1. Mở màn, không sửa ô nào.", "2. Bấm sang mục menu khác."], "—",
      ["- Rời màn ngay, không hỏi."]),
]

# ------------------------------------------------------------------ II
S2 = [
    T(1, "Tìm theo mã hàng", "P0", [ACC_A] + DATA3, ["1. Gõ “TEWI” vào ô tìm nhanh, nhấn Enter."], "Từ khoá: TEWI",
      ["- Chỉ còn YC1.", "- Dòng đếm 1, chân bảng “Hiển thị 1–1 / 1 yêu cầu”."]),
    T(2, "Tìm theo tên / model", "P1", [ACC_A] + DATA3, ["1. Gõ “wheel” rồi bấm Tìm kiếm.", "2. Gõ “INVERSPOTTER”, nhấn Enter."],
      ["Từ khoá 1: wheel", "Từ khoá 2: INVERSPOTTER"], ["- Từ khoá 1: YC2, YC3.", "- Từ khoá 2: YC1 (theo model)."]),
    T(3, "Tìm theo mã hàng đã đổi sau khi gửi", "P2", [ACC_A, "YC1 gửi khi mã là TEWI-AQUA; sau đó mã hàng đổi thành TEWI-AQUA-2."],
      ["1. Tìm “TEWI-AQUA-2”.", "2. Tìm “TEWI-AQUA”."], "—",
      ["- Cả 2 lần đều ra YC1 (tìm cả mã lúc gửi và mã hiện tại).", "- Cột Tên / Mã hiện mã MỚI."]),
    T(4, "Không có kết quả", "P1", [ACC_A] + DATA3, ["1. Tìm “KHONGCO123”."], "Từ khoá: KHONGCO123",
      ["- Bảng “Không có dữ liệu phù hợp”.", "- Dòng đếm 0."]),
    T(5, "Lọc Hãng sản xuất chỉ liệt kê hãng có yêu cầu", "P1", [ACC_A] + DATA3,
      ["1. Bấm Tìm kiếm nâng cao.", "2. Mở ô Hãng sản xuất.", "3. Chọn “JIANGSU SULI MACHINERY CO., LTD”."], "—",
      ["- Ô chỉ có 2 hãng: JIANGSU SULI MACHINERY CO., LTD và Telwin S.p.A.", "- Sau bước 3: còn YC2, YC3, lọc ngay không cần bấm Tìm kiếm."]),
    T(6, "Lọc Người cập nhật", "P1", [ACC_A] + DATA3 + ["Người đề nghị Q gửi thêm 1 yêu cầu YC4."],
      ["1. Mở ô Người cập nhật.", "2. Chọn P."], "—",
      ["- Ô liệt kê dạng “<mã phòng> - <họ tên>”, chỉ P và Q, xếp theo tên.", "- Sau bước 2: chỉ YC1, YC2, YC3."]),
    T(7, "Cây phân loại: đổi cấp trên xoá cấp dưới", "P1", [ACC_A, "Có yêu cầu thuộc nhiều Loại sản phẩm."],
      ["1. Chọn Tính chất, Nhóm công nghệ, Nhóm sản phẩm, Loại sản phẩm.", "2. Đổi Tính chất."], "—",
      ["- Mỗi cấp chỉ liệt kê giá trị thuộc cấp trên đã chọn.", "- Bước 2: 3 cấp dưới bị xoá trắng, danh sách tải lại 1 lần."]),
    T(8, "Làm mới xoá mọi điều kiện", "P1", [ACC_A] + DATA3, ["1. Tìm “TEWI”, chọn hãng Telwin S.p.A.", "2. Bấm Làm mới."], "—",
      ["- Ô tìm nhanh và các ô lọc trống.", "- Hiện lại 3 yêu cầu, về trang 1."]),
    T(9, "Lọc lại KHÔNG bỏ ô đã tick", "P0", [ACC_A] + DATA3,
      ["1. Tick YC1 và YC3.", "2. Tìm “TEWI”, nhấn Enter."], "—",
      ["- Bảng chỉ còn YC1 (đang tick).", "- Thanh hàng loạt “Đã chọn 2 yêu cầu (1 đang ẩn do bộ lọc)”."]),
    T(10, "Lọc lại KHÔNG bỏ giá đã sửa", "P0", [ACC_A] + DATA3,
      ["1. Sửa Giá mới Bán lẻ YC3 thành 3,300,000.", "2. Tìm “TEWI”.", "3. Bấm Làm mới."], "Giá mới: 3,300,000",
      ["- Sau bước 3: Giá mới Bán lẻ YC3 vẫn 3,300,000."]),
]

# ------------------------------------------------------------------ III
S3 = [
    T(1, "Thứ tự: yêu cầu cập nhật gần nhất lên trước", "P1", [ACC_A] + DATA3 + ["Thời gian gửi: YC1 16/10 09:15, YC2 16/10 08:40, YC3 15/10 17:02."],
      ["1. Mở màn."], "—", ["- Thứ tự YC1, YC2, YC3; cột Thời gian đúng 3 mốc trên."]),
    T(2, "Một khối yêu cầu hiển thị đúng", "P0", [ACC_A] + DATA3, ["1. Quan sát khối YC1."], "—",
      ["- Tên “Máy hàn bấm và giật tôn 15000A, 3 pha (Kèm PK)”, mã TEWI-AQUA, “Lý do sửa giá: Điều chỉnh theo bảng giá hãng tháng 10/2026”.",
       "- ĐVT Bộ; Giá vốn 195,989,760, KHÔNG có dòng “Cũ:” (bằng giá đang chạy).",
       "- 7 dòng: Bán lẻ, dòng “Giá hiệu lực” ngay dưới Bán lẻ, Giá bán theo lô, Đại lý cấp 1, 2, 3, Thương mại điện tử.",
       "- Cột Người cập nhật “<mã phòng> - <họ tên P>”, Mã hàng hoá là link."]),
    T(3, "Yêu cầu chỉ đổi giá vốn", "P0", [ACC_A] + DATA3, ["1. Quan sát khối YC2."], "—",
      ["- Giá vốn 3,100,000, dưới có “Cũ: 2,915,000”.", "- 1 dòng “Chỉ đổi giá vốn — không đổi giá bán”."]),
    T(4, "Dòng giá hiệu lực", "P1", [ACC_A] + DATA3, ["1. Quan sát dòng Giá hiệu lực của YC1."], "—",
      ["- Giá cũ và ĐMGG cũ để trống; không có chênh lệch dưới Giá mới.", "- Cột Hiệu lực có ô ngày 15/10/2026 + chữ cam “Duyệt sẽ dời về 17/10/2026”.",
       "- Các dòng còn lại ghi “Đang áp dụng” (chữ xanh)."]),
    T(5, "Chênh lệch dưới Giá mới", "P0", [ACC_A] + DATA3, ["1. Quan sát chữ dưới ô Giá mới các dòng của YC1, YC3."], "—",
      ["- Bán lẻ YC1: số âm chữ cam, đúng bằng 333,182,600 trừ 341,000,000 (giảm).", "- TMĐT YC1: “+433,137,380” chữ xanh lá.", "- Bán lẻ YC3: “+291,500” (so với giá lúc đề nghị 2,915,000, KHÔNG so với 3,000,000)."]),
    T(6, "Bấm mã hàng mở chi tiết ở tab mới", "P1", [ACC_A] + DATA3, ["1. Sửa hệ số YC1 thành 1.75.", "2. Bấm link TEWI-AQUA ở cột Mã hàng hoá."], "—",
      ["- Màn Xem chi tiết hàng hoá mở ở tab MỚI.", "- Tab Duyệt giá bán giữ nguyên hệ số 1.75."]),
    T(7, "Đổi số dòng / trang", "P1", [ACC_A, "Công ty A có 25 yêu cầu chờ."], ["1. Chọn Số dòng/trang 10.", "2. Sang trang 3."], "Số dòng/trang: 10",
      ["- “Hiển thị 1–10 / 25 yêu cầu”, về trang 1.", "- Trang 3: “Hiển thị 21–25 / 25 yêu cầu”, cột # chạy 21 đến 25."]),
    T(8, "Đổi trang giữ tick và giá đã sửa", "P0", [ACC_A, "Công ty A có 25 yêu cầu, 10 dòng / trang."],
      ["1. Trang 1: tick yêu cầu số 1, sửa Giá mới của nó.", "2. Sang trang 2, tick yêu cầu số 11.", "3. Quay lại trang 1."], "—",
      ["- Thanh hàng loạt “Đã chọn 2 yêu cầu”; ở trang 2 ghi “(1 đang ẩn do bộ lọc)”.", "- Trang 1: yêu cầu số 1 vẫn tick, giá đã sửa còn nguyên."]),
    T(9, "Ô tick tiêu đề chọn cả trang", "P1", [ACC_A] + DATA3,
      ["1. Tick YC1.", "2. Quan sát ô tick tiêu đề.", "3. Tick ô tiêu đề.", "4. Bỏ tick ô tiêu đề."], "—",
      ["- Bước 2: ô tiêu đề ở trạng thái nửa (gạch ngang).", "- Bước 3: 3 yêu cầu được tick, “Đã chọn 3 yêu cầu”.", "- Bước 4: bỏ tick cả 3, thanh hàng loạt ẩn."]),
    T(10, "Cuộn ngang: cột Tên hàng hoá dính trái", "P2", [ACC_A] + DATA3, ["1. Cuộn bảng sang phải hết cỡ."], "—",
      ["- Ô tick, #, Tên hàng hoá (kèm nút Duyệt / Không duyệt) vẫn hiện bên trái.", "- Tiêu đề cột dính trên khi cuộn dọc."]),
]

# ------------------------------------------------------------------ IV
S4 = [
    T(1, "Sửa hệ số tự tính Giá mới", "P0", [ACC_A] + DATA3, ["1. Ở YC1 dòng Bán lẻ, gõ hệ số 1.75."], "Hệ số: 1.75",
      ["- Giá mới = 342,982,100 (làm tròn trăm của 1.75 × 195,989,760).", "- Chênh lệch “+1,982,100” chữ xanh lá."]),
    T(2, "Sửa Bán lẻ KHÔNG lan sang loại giá khác", "P0", [ACC_A] + DATA3, ["1. Ở YC1 sửa hệ số Bán lẻ 1.75."], "Hệ số Bán lẻ: 1.75",
      ["- Giá bán theo lô, Đại lý cấp 1, 2, 3 vẫn 333,182,600, hệ số 1.7.", "- TMĐT vẫn 433,137,380.",
       "- Lưu ý: khác màn Cập nhật giá bán (ở đó Bán lẻ lan sang 4 loại giá)."]),
    T(3, "Sửa thẳng Giá mới không đổi hệ số", "P1", [ACC_A] + DATA3, ["1. Ở YC1 dòng Đại lý cấp 1, sửa Giá mới 320,000,000."], "Giá mới: 320,000,000",
      ["- Hệ số giữ 1.7.", "- Chênh lệch “-21,000,000” chữ cam."]),
    T(4, "Sửa ĐMGG mới", "P1", [ACC_A] + DATA3, ["1. Ở YC1 dòng Bán lẻ sửa ĐMGG mới 7.5.", "2. Xoá trắng ĐMGG mới dòng Đại lý cấp 2."], ["ĐMGG: 7.5", "ĐMGG: trống"],
      ["- Ô nhận 7.5 (tối đa 2 số lẻ).", "- Ô trống không báo lỗi (khi duyệt ghi 0)."]),
    T(5, "Đổi ngày giá hiệu lực", "P1", [ACC_A] + DATA3, ["1. Ở dòng Giá hiệu lực YC1 chọn ngày 20/10/2026."], "Ngày: 20/10/2026",
      ["- Chữ “Duyệt sẽ dời về …” biến mất.", "- Không xoá trắng được ô ngày."]),
    T(6, "Sửa hệ số dòng giá hiệu lực làm tròn trăm", "P1", [ACC_A] + DATA3, ["1. Ở dòng Giá hiệu lực YC1 gõ hệ số 1.4."], "Hệ số: 1.4",
      ["- Giá = 274,385,700 (làm tròn TRĂM).", "- Lưu ý: màn Cập nhật giá bán ra 274,385,664 (làm tròn đồng) cho cùng hệ số."]),
    T(7, "Không có " + Q2 + ": không sửa được hệ số", "P0", [ACC_B] + DATA3, ["1. Mở màn.", "2. Sửa Giá mới Bán lẻ YC1 thành 335,000,000."], "Giá mới: 335,000,000",
      ["- Không có cột Hệ số nên không có ô hệ số để sửa.", "- Giá mới nhận 335,000,000, chênh lệch “-6,000,000”."]),
    T(8, "Người đề nghị gửi lại trong lúc người duyệt đang sửa", "P1", [ACC_A] + DATA3,
      ["1. A sửa Giá mới Bán lẻ YC1 thành 330,000,000 (chưa duyệt).", "2. P gửi lại YC1 với hệ số 1.8.", "3. A bấm Tìm kiếm (tải lại)."], "—",
      ["- Sau bước 3: YC1 hiện bản mới (hệ số 1.8, giá 352,781,600); giá A đã sửa bị bỏ.", "- Thời gian của YC1 đổi sang lần gửi mới."]),
    T(9, "Sửa ô thì lỗi của đúng ô đó mất", "P1", [ACC_A] + DATA3,
      ["1. Xoá trắng Giá mới dòng Giá bán theo lô và nhập hệ số 100 dòng Đại lý cấp 1 của YC1.", "2. Bấm Duyệt.", "3. Nhập lại Giá mới dòng Giá bán theo lô."], "—",
      ["- Bước 2: 2 ô báo đỏ.", "- Bước 3: lỗi ô Giá bán theo lô mất; lỗi hệ số Đại lý cấp 1 vẫn còn."]),
    T(10, "Gõ hệ số xoá lỗi ô Giá mới cùng dòng", "P2", [ACC_A] + DATA3,
      ["1. Xoá trắng Giá mới Bán lẻ YC1, bấm Duyệt (ô báo đỏ).", "2. Gõ hệ số Bán lẻ 1.7."], "—",
      ["- Giá mới tự điền 333,182,600, lỗi “Bắt buộc phải nhập” mất."]),
]

# ------------------------------------------------------------------ V
S5 = [
    T(1, "Duyệt 1 yêu cầu giữ nguyên đề nghị", "P0", [ACC_A] + DATA3 + ["Ghi lại giá trước khi test để trả lại."],
      ["1. Bấm Duyệt ở YC1.", "2. Đọc popup.", "3. Bấm Duyệt ở popup."], "—",
      ["- Popup “Duyệt giá bán”: “Duyệt giá bán cho:” + “TEWI-AQUA – Máy hàn bấm và giật tôn 15000A, 3 pha (Kèm PK) (Bộ)”.",
       "- Có khối “Giá hiệu lực có ngày trước ngày mai sẽ dời về 17/10/2026: TEWI-AQUA: 15/10/2026 sang 17/10/2026”.",
       "- Thông báo “Đã duyệt 1 yêu cầu giá bán.”; YC1 biến khỏi danh sách, dòng đếm 2.",
       "- Màn Cập nhật giá bán công ty A: Giá hiện tại Bán lẻ 333,182,600, hệ số 1.7, không còn nhãn Chờ duyệt."]),
    T(2, "Duyệt áp đúng giá người duyệt đã sửa", "P0", [ACC_A] + DATA3,
      ["1. Sửa hệ số Bán lẻ YC1 thành 1.75.", "2. Bấm Duyệt, xác nhận."], "Hệ số Bán lẻ: 1.75",
      ["- Màn Cập nhật giá bán: Bán lẻ 342,982,100 hệ số 1.75; 4 loại giá còn lại 333,182,600 (như đề nghị).",
       "- Lịch sử giá có dòng “Duyệt giá”: Bán lẻ (Bộ) 341,000,000 sang 342,982,100."]),
    T(3, "Bấm Hủy ở popup Duyệt", "P1", [ACC_A] + DATA3, ["1. Sửa hệ số Bán lẻ YC1 thành 1.75.", "2. Bấm Duyệt.", "3. Bấm Hủy."], "—",
      ["- Popup đóng, YC1 vẫn ở danh sách, hệ số vẫn 1.75.", "- Giá Bán lẻ ở màn Cập nhật giá bán vẫn 341,000,000."]),
    T(4, "Duyệt khi giá đang chạy đã đổi", "P0", [ACC_A] + DATA3, ["1. Bấm Duyệt ở YC3.", "2. Đọc popup.", "3. Bấm Duyệt."], "—",
      ["- Popup có chữ nâu “Giá đang chạy đã đổi sau khi đề nghị (phiếu tính giá / cron) — vẫn duyệt theo giá trên màn này:” + "
       "“SULI-IN-2716-WHEEL-NO12: giá đang chạy 3,000,000 (lúc đề nghị 2,915,000)”.",
       "- Thông báo “Đã duyệt 1 yêu cầu giá bán. Có 1 dòng giá đang chạy đã đổi trước khi duyệt.”",
       "- Giá Bán lẻ NO12 sau duyệt: 3,206,500 (giá trên màn, không phải 3,000,000)."]),
    T(5, "Duyệt yêu cầu chỉ đổi giá vốn", "P0", [ACC_A] + DATA3, ["1. Bấm Duyệt ở YC2, xác nhận."], "—",
      ["- Giá vốn Cái của NO14 tại công ty A thành 3,100,000.", "- 6 loại giá bán không đổi.", "- Popup ghi “giá vốn đề nghị ghi vào công ty <tên công ty A>”."]),
    T(6, "Không duyệt 1 yêu cầu", "P0", [ACC_A] + DATA3,
      ["1. Bấm Không duyệt ở YC1.", "2. Nhập lý do “Giá cao hơn đối thủ 5%”.", "3. Bấm Không duyệt."], "Lý do: Giá cao hơn đối thủ 5%",
      ["- Popup “Không duyệt giá bán”: “Danh sách mã hàng hoá không duyệt: TEWI-AQUA” và câu “Giá đang áp dụng giữ nguyên; …”.",
       "- Thông báo “Đã không duyệt 1 yêu cầu.”; YC1 biến khỏi danh sách.",
       "- Màn Cập nhật giá bán: Giá hiện tại Bán lẻ vẫn 341,000,000; các ô hiện nhãn “Không duyệt”; dưới tên “Lý do không duyệt: Giá cao hơn đối thủ 5%”."]),
    T(7, "Không duyệt khi chưa nhập lý do", "P0", [ACC_A] + DATA3,
      ["1. Bấm Không duyệt ở YC1.", "2. Để trống lý do, bấm Không duyệt.", "3. Nhập 3 dấu cách, bấm Không duyệt."], "Lý do: trống / 3 dấu cách",
      ["- Cả 2 lần: chữ đỏ “Vui lòng nhập lý do không duyệt”, popup KHÔNG đóng.", "- YC1 vẫn chờ."]),
    T(8, "Không duyệt KHÔNG dùng giá đã sửa", "P1", [ACC_A] + DATA3,
      ["1. Sửa hệ số Bán lẻ YC1 thành 1.75.", "2. Không duyệt YC1 với lý do “Sai giá”.", "3. Mở Lịch sử giá TEWI-AQUA."], "—",
      ["- Dòng “Không duyệt giá”: Bán lẻ (Bộ) 341,000,000 sang 333,182,600 (giá đề nghị gốc, không phải 342,982,100).",
       "- Ghi chú “Lý do không duyệt: Sai giá”."]),
    T(9, "Duyệt hàng loạt áp đúng giá từng yêu cầu", "P0", [ACC_A] + DATA3,
      ["1. Sửa Giá mới Bán lẻ YC1 thành 335,000,000; sửa Giá mới Bán lẻ YC3 thành 3,250,000.", "2. Tick YC1, YC3.",
       "3. Bấm Duyệt ở thanh hàng loạt.", "4. Bấm Duyệt ở popup."], "—",
      ["- Popup “Duyệt giá bán hàng loạt”: “Duyệt 2 yêu cầu giá bán đã chọn:” + 2 dòng mã – tên (ĐVT).",
       "- Có cả khối giá hiệu lực dời ngày (TEWI-AQUA) và khối giá đang chạy đã đổi (NO12).",
       "- Thông báo “Đã duyệt 2 yêu cầu giá bán. Có 1 dòng giá đang chạy đã đổi trước khi duyệt.”",
       "- Bán lẻ TEWI-AQUA 335,000,000; Bán lẻ NO12 3,250,000 (mỗi yêu cầu đúng giá của nó)."]),
    T(10, "Duyệt hàng loạt gồm yêu cầu đang bị lọc ẩn", "P0", [ACC_A] + DATA3,
      ["1. Tick YC1, YC3.", "2. Tìm “TEWI”.", "3. Bấm Duyệt ở thanh hàng loạt, đọc popup, xác nhận."], "—",
      ["- Thanh hàng loạt “Đã chọn 2 yêu cầu (1 đang ẩn do bộ lọc)”.", "- Popup ghi “(gồm cả yêu cầu đang ẩn do bộ lọc)” và liệt kê cả NO12.",
       "- Cả YC1 và YC3 được duyệt."]),
    T(11, "Không duyệt hàng loạt 1 lý do chung", "P0", [ACC_A] + DATA3,
      ["1. Tick YC1, YC2, YC3.", "2. Bấm Không duyệt ở thanh hàng loạt.", "3. Nhập “Chờ bảng giá mới”, bấm Không duyệt."], "Lý do: Chờ bảng giá mới",
      ["- Popup “Không duyệt giá bán hàng loạt”: “Danh sách mã hàng hoá không duyệt: TEWI-AQUA, SULI-IN-2716-WHEEL-NO14, SULI-IN-2716-WHEEL-NO12” + “Một lý do dùng chung cho cả 3 yêu cầu.”",
       "- Thông báo “Đã không duyệt 3 yêu cầu.”", "- Cả 3 hàng ở màn Cập nhật giá bán có “Lý do không duyệt: Chờ bảng giá mới”."]),
    T(12, "Hàng loạt có 1 yêu cầu sai ô thì không gửi yêu cầu nào", "P0", [ACC_A] + DATA3,
      ["1. Xoá trắng Giá mới Bán lẻ YC3.", "2. Tick YC1, YC3.", "3. Bấm Duyệt ở thanh hàng loạt."], "—",
      ["- Thông báo “1 yêu cầu có ô chưa hợp lệ — sửa chữ đỏ rồi duyệt lại”; ô Bán lẻ YC3 báo “Bắt buộc phải nhập”.",
       "- Không mở popup; YC1 cũng KHÔNG được duyệt."]),
    T(13, "Bỏ chọn", "P2", [ACC_A] + DATA3, ["1. Tick YC1, YC3.", "2. Tìm “TEWI”.", "3. Bấm Bỏ chọn.", "4. Bấm Làm mới."], "—",
      ["- Thanh hàng loạt ẩn.", "- Sau bước 4: không yêu cầu nào được tick (kể cả YC3 từng bị ẩn)."]),
    T(14, "Nút tạm khoá khi đang xử lý", "P2", [ACC_A] + DATA3, ["1. Bấm Duyệt YC1, xác nhận.", "2. Trong lúc đang xử lý, bấm Duyệt YC3."], "—",
      ["- Nút Duyệt / Không duyệt mờ trong lúc xử lý; lần bấm thứ 2 không có tác dụng.", "- Chỉ YC1 được duyệt."]),
    T(15, "Duyệt yêu cầu vừa bị người khác xử lý", "P0", ["Tài khoản A và A2 cùng có " + Q1 + " tại công ty A, cùng mở màn."] + DATA3,
      ["1. A2 duyệt YC1.", "2. A (chưa tải lại) bấm Duyệt YC1, xác nhận."], "—",
      ["- A nhận cảnh báo “" + GONE + "”; danh sách tải lại, YC1 biến mất.", "- Giá chỉ áp 1 lần (của A2); lịch sử 1 dòng “Duyệt giá”."]),
    T(16, "Duyệt hàng loạt khi 1 yêu cầu vừa bị người khác xử lý", "P1", ["Như ca 15."],
      ["1. A tick YC1, YC3.", "2. A2 Không duyệt YC1.", "3. A bấm Duyệt hàng loạt, xác nhận."], "—",
      ["- Thông báo “Đã duyệt 1 yêu cầu giá bán. … 1 yêu cầu đã được người khác xử lý.”", "- YC1 giữ kết quả Không duyệt của A2; YC3 được duyệt."]),
    T(17, "Thông báo cho người đề nghị khi Duyệt", "P0", [ACC_A] + DATA3, ["1. A duyệt YC1.", "2. P mở chuông thông báo, bấm thông báo."], "—",
      ["- P nhận “[GIA] Đã duyệt: TEWI-AQUA – Máy hàn bấm và giật tôn 15000A, 3 pha (Kèm PK). Giá mới áp dụng từ 16/10/2026”.",
       "- Bấm thông báo: mở màn Cập nhật giá bán chỉ hiện TEWI-AQUA."]),
    T(18, "Thông báo cho người đề nghị khi Không duyệt", "P0", [ACC_A] + DATA3,
      ["1. A Không duyệt YC1 với lý do “Giá cao”.", "2. P bấm thông báo mới."], "—",
      ["- P nhận “[GIA] Từ chối: TEWI-AQUA – … Lý do: Giá cao” (cả câu tối đa 120 ký tự, tên tối đa 50 ký tự).",
       "- Bấm thông báo: màn Cập nhật giá bán chỉ hiện TEWI-AQUA, bật sẵn lọc Trạng thái duyệt = Không duyệt."]),
    T(19, "Người có quyền duyệt nhận thông báo Chờ duyệt", "P0",
      ["A và A3 có " + Q1 + " tại công ty A; A4 có " + Q1 + " chỉ tại công ty B.", "Công ty A bật duyệt giá."],
      ["1. P Gửi duyệt giá TEWI-AQUA ở màn Cập nhật giá bán.", "2. A, A3, A4 mở chuông."], "—",
      ["- A và A3 nhận “[GIA] Chờ duyệt: TEWI-AQUA – …. Người đề nghị: <P>”.", "- A4 KHÔNG nhận (khác công ty)."]),
    T(20, "Duyệt hàng đã bị khoá sau khi gửi đề nghị", "P1",
      [ACC_A] + DATA3 + ["Sau khi P gửi YC1, TEWI-AQUA bị khoá (Ngừng kinh doanh) tại công ty A."],
      ["1. Mở màn, bấm Duyệt YC1, xác nhận."], "—",
      ["- YC1 vẫn hiện và VẪN duyệt được; giá được áp cho hàng đang Ngừng kinh doanh.",
       "- Lưu ý: hành vi này đang chờ nghiệp vụ xác nhận — ghi KQ thực tế để đối chiếu."]),
]

# ------------------------------------------------------------------ VI
S6 = [
    T(1, "Duyệt ghi đúng giá, hệ số, ĐMGG từng loại giá", "P0", [ACC_A] + DATA3, ["1. Duyệt YC1 không sửa.", "2. Mở màn Cập nhật giá bán, tìm TEWI-AQUA."], "—",
      ["- Bán lẻ, Giá bán theo lô, Đại lý cấp 1, 2, 3: Giá hiện tại 333,182,600, hệ số 1.7, ĐMGG 5.", "- TMĐT: 433,137,380, hệ số 2.21, ĐMGG 0."]),
    T(2, "Giá hiệu lực ngày đã qua dời về ngày mai", "P0", [ACC_A] + DATA3, ["1. Duyệt YC1 (ngày hiệu lực 15/10/2026, hôm nay 16/10/2026)."], "—",
      ["- Giá hiệu lực Bán lẻ 350,000,000 ngày 17/10/2026.", "- Thông báo Đã duyệt ghi “Giá mới áp dụng từ 16/10/2026” (có dòng giá hiện tại)."]),
    T(3, "Giá hiệu lực ngày hôm nay cũng dời về ngày mai", "P1", [ACC_A, "Yêu cầu YC5 chỉ có 1 giá hiệu lực Bán lẻ 300,000,000 ngày 16/10/2026 (hôm nay)."],
      ["1. Quan sát cột Hiệu lực.", "2. Duyệt YC5."], "—",
      ["- Có chữ “Duyệt sẽ dời về 17/10/2026”.", "- Sau duyệt: giá hiệu lực ngày 17/10/2026.",
       "- Thông báo Đã duyệt “Giá mới áp dụng từ 17/10/2026” (chỉ có giá hiệu lực)."]),
    T(4, "Giá hiệu lực ngày tương lai giữ nguyên", "P1", [ACC_A, "YC6 có giá hiệu lực ngày 25/10/2026."], ["1. Duyệt YC6."], "—",
      ["- Không có chữ “Duyệt sẽ dời về”.", "- Giá hiệu lực áp đúng ngày 25/10/2026."]),
    T(5, "Giá hiệu lực đã bị áp trước khi duyệt", "P2", [ACC_A, "YC6 có giá hiệu lực Bán lẻ ngày 17/10; tác vụ hằng đêm đã áp và xoá giá hiệu lực đó trước khi duyệt; YC6 còn dòng Đại lý cấp 1 đổi giá."],
      ["1. Duyệt YC6."], "—", ["- Duyệt thành công; dòng giá hiệu lực bị bỏ qua.", "- Đại lý cấp 1 được áp giá mới."]),
    T(6, "Giá vốn đề nghị được ghi khi duyệt", "P0", [ACC_A] + DATA3, ["1. Duyệt YC2.", "2. Mở màn Cập nhật giá bán, tìm NO14."], "—",
      ["- Giá vốn Cái = 3,100,000.", "- Giá bán NO14 không đổi (4,955,500)."]),
    T(7, "Không có " + Q2 + " vẫn áp giá vốn đề nghị", "P0", [ACC_B] + DATA3, ["1. B duyệt YC2."], "—",
      ["- B không thấy số giá vốn ở bất kỳ đâu trên màn.", "- Giá vốn NO14 tại công ty A vẫn được ghi 3,100,000."]),
    T(8, "Không có " + Q2 + ": hệ số giữ bản đề nghị khi sửa giá", "P0", [ACC_B] + DATA3,
      ["1. B sửa Giá mới Bán lẻ YC1 thành 335,000,000.", "2. Duyệt."], "Giá mới: 335,000,000",
      ["- Bán lẻ: giá 335,000,000, hệ số 1.7 (bản đề nghị, KHÔNG tự tính lại).", "- Lưu ý: giá ÷ giá vốn không còn bằng hệ số — đúng thiết kế."]),
    T(9, "Không có " + Q2 + ": không lộ giá vốn ở popup / Excel / lịch sử", "P0", [ACC_B] + DATA3,
      ["1. Bấm Duyệt YC1, đọc popup.", "2. Xuất Excel.", "3. Mở Lịch sử giá TEWI-AQUA (đã từng đổi giá vốn)."], "—",
      ["- Popup không có số giá vốn (chỉ câu “giá vốn đề nghị ghi vào công ty …”).", "- File Excel không có cột Giá vốn, Hệ số.",
       "- Lịch sử không có dòng Giá vốn, không có trường Hệ số."]),
    T(10, "Duyệt không chạm giá công ty khác", "P0", [ACC_A] + DATA3 + ["TEWI-AQUA tại công ty B: Bán lẻ 350,000,000."], ["1. Duyệt YC1 ở công ty A."], "—",
      ["- Công ty A: Bán lẻ 333,182,600.", "- Công ty B: Bán lẻ vẫn 350,000,000, giá vốn công ty B không đổi."]),
    T(11, "Duyệt không tự tính TMĐT theo Bán lẻ", "P1", [ACC_A] + DATA3, ["1. Sửa Giá mới Bán lẻ YC1 thành 350,000,000 (TMĐT để nguyên).", "2. Duyệt."], "—",
      ["- Bán lẻ 350,000,000; TMĐT 433,137,380 (đúng số trên màn, không phải 455,000,000).",
       "- Lưu ý: ghi KQ thực tế — khác quy tắc TMĐT = Bán lẻ × 1.3 của màn Cập nhật giá bán."]),
    T(12, "Hệ số dòng hiệu lực sửa ở màn Duyệt làm tròn trăm", "P2", [ACC_A] + DATA3, ["1. Gõ hệ số dòng Giá hiệu lực YC1 = 1.4, duyệt."], "Hệ số: 1.4",
      ["- Giá hiệu lực Bán lẻ = 274,385,700 (tròn trăm)."]),
    T(13, "Hàng mới chờ duyệt chuyển Đang kinh doanh", "P0",
      [ACC_A, "Hàng H mới của công ty A (công ty quản lý) đang ở trạng thái chờ duyệt cũ của ERP; có yêu cầu duyệt giá ĐVT Cái tại công ty A."],
      ["1. Duyệt yêu cầu của H.", "2. Tìm H ở màn Cập nhật giá bán và màn Hàng hoá."], "—",
      ["- H chuyển Đang kinh doanh tại công ty A, có đủ 6 loại giá cho mọi ĐVT.", "- H hiện ở màn Cập nhật giá bán."]),
    T(14, "Hàng mới bị Không duyệt", "P1", ["Như ca 13."], ["1. Không duyệt yêu cầu của H, lý do “Thiếu chứng từ”."], "—",
      ["- H chuyển trạng thái Không duyệt; không hiện ở màn Cập nhật giá bán."]),
    T(15, "Yêu cầu từ Phiếu tính giá: duyệt hết dòng", "P0",
      [ACC_A, "PTG01 (công ty A) gửi duyệt 2 dòng: hàng H mới, ĐVT Cái và Bộ; H đang Chờ tính giá bán."],
      ["1. Duyệt cả 2 yêu cầu của PTG01 (hàng loạt).", "2. Mở PTG01."], "—",
      ["- PTG01 chuyển Đã duyệt, dòng phiếu ghi giá thực áp.", "- H chuyển Đang kinh doanh tại công ty A.",
       "- Người lập PTG01 nhận “[PTG] Đã duyệt: PTG01. Giá bán đã được áp”; KHÔNG nhận “[GIA] Đã duyệt” từng dòng."]),
    T(16, "Yêu cầu từ Phiếu tính giá: duyệt 1 dòng còn 1 dòng chờ", "P1", ["Như ca 15."], ["1. Chỉ duyệt yêu cầu ĐVT Cái.", "2. Mở PTG01."], "—",
      ["- PTG01 vẫn Chờ duyệt; dòng Cái ghi đã duyệt.", "- H CHƯA chuyển Đang kinh doanh (còn ĐVT Bộ chưa xong)."]),
    T(17, "Yêu cầu từ Phiếu tính giá: không duyệt 1 dòng", "P0", ["Như ca 15."],
      ["1. Duyệt dòng Cái.", "2. Không duyệt dòng Bộ, lý do “Giá thấp”.", "3. Mở PTG01."], "—",
      ["- PTG01 chuyển Giá bị từ chối; dòng Bộ ghi lý do “Giá thấp”.", "- Người lập nhận “[PTG] Từ chối: PTG01. Lý do: Giá thấp”."]),
    T(18, "Công ty vừa tắt duyệt giá khi còn yêu cầu chờ", "P1", [ACC_A] + DATA3 + ["Sau khi P gửi, công ty A TẮT duyệt giá ở màn Quy định."],
      ["1. Mở màn Duyệt giá bán.", "2. Duyệt YC1."], "—",
      ["- YC1, YC2, YC3 vẫn hiện.", "- YC1 duyệt bình thường."]),
]

# ------------------------------------------------------------------ VII
S7 = [
    T(1, "Xuất Excel theo bộ lọc", "P0", [ACC_A] + DATA3, ["1. Lọc hãng JIANGSU SULI MACHINERY CO., LTD.", "2. Bấm Xuất Excel."], "—",
      ["- Tải file “danh_sach_hang_cho_duyet_gia_ban.xlsx” (đúng tên, đúng đuôi, kể cả trên Safari).",
       "- Đầu file có letterhead công ty A và tiêu đề “DANH SÁCH HÀNG CHỜ DUYỆT GIÁ BÁN”.", "- Chỉ có YC2, YC3."]),
    T(2, "Excel đủ cột", "P0", [ACC_A] + DATA3, ["1. Bấm Xuất Excel, mở file."], "—",
      ["- 18 cột: STT, Mã hàng hoá, Tên hàng hoá, ĐVT, Model, Hãng sản xuất, Loại sản phẩm, Giá vốn, Loại giá, Giá cũ, Hệ số, Giá mới, "
       "ĐMGG cũ (%), ĐMGG mới (%), Ngày hiệu lực, Lý do sửa giá, Người cập nhật, Thời gian.",
       "- Không có quyền Xem giá vốn hàng hoá: 16 cột (bỏ Giá vốn, Hệ số)."]),
    T(3, "Excel: khối yêu cầu và dòng giá hiệu lực", "P1", [ACC_A] + DATA3, ["1. Xuất Excel, xem YC1."], "—",
      ["- Các cột STT … Loại sản phẩm, Giá vốn, Lý do sửa giá, Người cập nhật, Thời gian gộp dọc 7 dòng.",
       "- Dòng giá hiệu lực: Loại giá “Bán lẻ — giá hiệu lực”, Giá cũ và ĐMGG cũ trống, Ngày hiệu lực 15/10/2026.",
       "- Dòng còn lại cột Ngày hiệu lực ghi “Đang áp dụng”."]),
    T(4, "Excel: yêu cầu chỉ đổi giá vốn, số 0", "P1", [ACC_A] + DATA3, ["1. Xuất Excel, xem YC2 và dòng TMĐT của YC1."], "—",
      ["- YC2: cột Loại giá “Chỉ đổi giá vốn”.", "- TMĐT YC1: Giá cũ ghi số 0 (không để trống); ĐMGG mới 0.",
       "- Tiền là số thật có dấu ngăn nghìn, cộng được bằng hàm tổng."]),
    T(5, "Excel ghi giá đề nghị gốc, không ghi giá đang sửa", "P1", [ACC_A] + DATA3, ["1. Sửa hệ số Bán lẻ YC1 thành 1.75 (chưa duyệt).", "2. Xuất Excel."], "—",
      ["- File ghi Bán lẻ YC1 giá mới 333,182,600, hệ số 1.7."]),
    T(6, "Excel khi không có yêu cầu", "P2", [ACC_A, "Công ty A không có yêu cầu chờ."], ["1. Bấm Xuất Excel."], "—",
      ["- File có tiêu đề + dòng tên cột, không có dòng dữ liệu, không lỗi."]),
    T(7, "Excel tối đa 5.000 yêu cầu", "P2", [ACC_A, "Công ty A có 5.200 yêu cầu chờ."], ["1. Bấm Xuất Excel."], "—",
      ["- File có đúng 5.000 yêu cầu, mới cập nhật lên trước."]),
]

# ------------------------------------------------------------------ VIII
S8 = [
    T(1, "Giá mới để trống", "P0", [ACC_A] + DATA3, ["1. Xoá trắng Giá mới dòng Giá bán theo lô YC1.", "2. Bấm Duyệt YC1."], "Giá mới: trống",
      ["- Chữ đỏ “Bắt buộc phải nhập” dưới ô, viền đỏ.", "- Thông báo “1 yêu cầu có ô chưa hợp lệ — sửa chữ đỏ rồi duyệt lại”; không mở popup."]),
    T(2, "Giá mới quá 12 chữ số", "P1", [ACC_A] + DATA3, ["1. Nhập Giá mới Bán lẻ YC1 = 1,000,000,000,000.", "2. Bấm Duyệt."], "Giá mới: 1,000,000,000,000",
      ["- “Không được vượt quá 12 chữ số”."]),
    T(3, "Hệ số để trống", "P1", [ACC_A] + DATA3, ["1. Xoá trắng hệ số Đại lý cấp 2 YC1.", "2. Bấm Duyệt."], "Hệ số: trống",
      ["- “Bắt buộc phải nhập” dưới ô Hệ số."]),
    T(4, "Hệ số từ 100 trở lên", "P1", [ACC_A] + DATA3, ["1. Nhập hệ số Đại lý cấp 1 YC1 = 100.", "2. Bấm Duyệt."], "Hệ số: 100",
      ["- “Không được vượt quá 2 chữ số trước dấu phẩy”.", "- Hệ số 99.99 thì hợp lệ."]),
    T(5, "ĐMGG ngoài 0 – 100", "P1", [ACC_A] + DATA3, ["1. Nhập ĐMGG mới Đại lý cấp 2 YC1 = 120.", "2. Bấm Duyệt."], "ĐMGG: 120",
      ["- “Phải từ 0 đến 100”, không tự kẹp về 100."]),
    T(6, "Ô số chỉ nhận số", "P2", [ACC_A] + DATA3, ["1. Gõ chữ “abc” vào Hệ số, Giá mới, ĐMGG."], "abc",
      ["- Ô không nhận chữ; hệ số / ĐMGG tối đa 2 số lẻ."]),
    T(7, "Báo đồng thời mọi ô sai", "P0", [ACC_A] + DATA3,
      ["1. Ở YC1: xoá trắng Giá mới Giá bán theo lô, hệ số Đại lý cấp 1 = 100, ĐMGG Đại lý cấp 2 = 120.", "2. Bấm Duyệt."], "—",
      ["- CẢ 3 ô cùng báo đỏ: “Bắt buộc phải nhập”, “Không được vượt quá 2 chữ số trước dấu phẩy”, “Phải từ 0 đến 100”.",
       "- Bảng cuộn tới ô sai đầu tiên.", "- Không phải sửa từng ô rồi mới thấy lỗi ô tiếp theo."]),
    T(8, "Lý do không duyệt quá 2000 ký tự", "P1", [ACC_A] + DATA3, ["1. Bấm Không duyệt YC1.", "2. Dán lý do 2001 ký tự, bấm Không duyệt."], "Lý do: 2001 ký tự",
      ["- Mong đợi: báo “Không được vượt quá 2000 ký tự”, giữ popup và lý do đã nhập; YC1 vẫn chờ.",
       "- Lưu ý: bản hiện tại popup đóng, mất lý do và hiện thông báo tiếng Anh “The given data was invalid.” — ghi KQ thực tế (lỗi đã ghi nhận)."]),
    T(9, "Lý do đúng 2000 ký tự", "P2", [ACC_A] + DATA3, ["1. Không duyệt YC1 với lý do 2000 ký tự."], "Lý do: 2000 ký tự",
      ["- Không duyệt thành công; lý do đủ 2000 ký tự ở màn Cập nhật giá bán."]),
    T(10, "Bỏ qua giao diện: duyệt không chọn yêu cầu", "P2", [ACC_A],
      ["1. Dùng công cụ kiểm thử API gọi thẳng Duyệt hàng loạt với danh sách rỗng.", "2. Gọi thẳng Không duyệt hàng loạt danh sách rỗng, lý do trống."], "—",
      ["- Bước 1: “Vui lòng chọn hàng hoá để duyệt”.", "- Bước 2: “Vui lòng chọn hàng hoá để không duyệt” và “Vui lòng nhập lý do không duyệt”."]),
    T(11, "Bỏ qua giao diện: gửi ngày hiệu lực sai định dạng", "P2", [ACC_A] + DATA3,
      ["1. Dùng công cụ kiểm thử API gọi thẳng Duyệt YC1, ngày hiệu lực “2026-13-45”."], "—",
      ["- “Ngày không hợp lệ” ở dòng giá hiệu lực; không ghi gì."]),
]

# ------------------------------------------------------------------ IX
S9 = [
    T(1, "Chỉ thấy yêu cầu của công ty đang làm việc", "P0",
      ["Tài khoản A có " + Q1 + " ở công ty A và B.", "TEWI-AQUA có yêu cầu ở công ty A (YC1) và công ty B (YCB)."],
      ["1. Ở công ty A, tìm TEWI.", "2. Đổi sang công ty B, tìm TEWI."], "—",
      ["- Công ty A: chỉ YC1 (giá của công ty A).", "- Công ty B: chỉ YCB."]),
    T(2, "Duyệt ở công ty A không ảnh hưởng yêu cầu công ty B", "P0", ["Như ca 1."], ["1. Ở công ty A duyệt YC1.", "2. Sang công ty B."], "—",
      ["- YCB vẫn chờ; giá công ty B không đổi."]),
    T(3, "Hai người duyệt cùng lúc 1 yêu cầu", "P0", ["Tài khoản A và A2 có " + Q1 + " ở công ty A."] + DATA3,
      ["1. A và A2 cùng bấm Duyệt YC1 gần như đồng thời."], "—",
      ["- 1 người thành công, người còn lại nhận “" + GONE + "”.", "- Lịch sử chỉ 1 dòng “Duyệt giá”."]),
    T(4, "Một người duyệt, một người không duyệt cùng lúc", "P1", ["Như ca 3."], ["1. A bấm Duyệt YC1, A2 bấm Không duyệt YC1 cùng lúc."], "—",
      ["- Chỉ 1 kết quả được ghi; người còn lại nhận “" + GONE + "”."]),
    T(5, "Người đề nghị lưu thẳng khi yêu cầu đang chờ", "P1", [ACC_A] + DATA3 + ["Công ty A vừa tắt duyệt giá; P lưu thẳng TEWI-AQUA ở màn Cập nhật giá bán."],
      ["1. A (đang mở màn từ trước) bấm Duyệt YC1."], "—",
      ["- “" + GONE + "”; danh sách tải lại, YC1 không còn."]),
    T(6, "Hàng bị gỡ khỏi công ty khi yêu cầu đang chờ", "P2", [ACC_A, "Hàng H có yêu cầu chờ ở công ty A; công ty A gỡ H (trạng thái cho phép gỡ)."],
      ["1. Mở màn, tìm H."], "—", ["- Yêu cầu của H không còn trong danh sách."]),
    T(7, "Duyệt khi đang lỗi đường truyền", "P2", [ACC_A] + DATA3, ["1. Ngắt mạng.", "2. Duyệt YC1."], "—",
      ["- Thông báo lỗi “Thao tác không thành công” (hoặc lỗi mạng), không treo trang.", "- Bật mạng, tải lại: YC1 vẫn chờ, giá chưa đổi."]),
    T(8, "Giá đề nghị vẫn còn khi người duyệt tải lại trang", "P2", [ACC_A] + DATA3, ["1. Sửa hệ số YC1 = 1.75.", "2. Tải lại trình duyệt, chọn rời trang."], "—",
      ["- Trình duyệt hỏi xác nhận rời trang.", "- Sau khi tải lại: YC1 hiện giá đề nghị gốc (giá đã sửa không được lưu)."]),
]

# ------------------------------------------------------------------ X
S10 = [
    T(1, "Gửi duyệt – duyệt có sửa giá – người đề nghị thấy giá mới", "P0",
      [ACC_A, "Tài khoản P có " + Q3 + " tại công ty A; công ty A bật duyệt giá cho mọi hãng.", "TEWI-AQUA Bán lẻ 341,000,000 hệ số 1.6."],
      ["1. P ở màn Cập nhật giá bán sửa hệ số Bán lẻ TEWI-AQUA 1.7, Gửi duyệt.", "2. A mở thông báo “[GIA] Chờ duyệt”.",
       "3. A sửa hệ số Bán lẻ 1.75, Duyệt.", "4. P mở thông báo “[GIA] Đã duyệt”."], "—",
      ["- Bước 2: màn Duyệt giá bán chỉ hiện yêu cầu của TEWI-AQUA.", "- Bước 4: màn Cập nhật giá bán Bán lẻ 342,982,100 hệ số 1.75, không còn nhãn Chờ duyệt.",
       "- Lịch sử: “Gửi duyệt giá”, rồi “Duyệt giá”."]),
    T(2, "Gửi duyệt – không duyệt – sửa lại – duyệt", "P0", ["Như ca 1."],
      ["1. P Gửi duyệt hệ số Bán lẻ 1.7.", "2. A Không duyệt, lý do “Giá cao”.", "3. P mở thông báo Từ chối, sửa hệ số 1.65, Gửi duyệt lại.",
       "4. A Duyệt."], "—",
      ["- Sau bước 2: P thấy nhãn Không duyệt + “Lý do không duyệt: Giá cao”, giá đang áp dụng vẫn 341,000,000.",
       "- Sau bước 3: màn Duyệt có 1 yêu cầu mới hệ số 1.65.", "- Sau bước 4: Bán lẻ 323,383,100, lý do không duyệt mất."]),
    T(3, "Gửi lại đè yêu cầu cũ đang chờ", "P1", ["Như ca 1."], ["1. P Gửi duyệt hệ số 1.7.", "2. P Gửi duyệt lại hệ số 1.8.", "3. A mở màn Duyệt."], "—",
      ["- Chỉ có 1 yêu cầu của TEWI-AQUA (Bộ), hệ số 1.8."]),
    T(4, "Hàng mới qua Phiếu tính giá rồi được duyệt", "P0",
      [ACC_A, "Hàng mới H vừa tạo ở công ty A; công ty A bật duyệt giá."],
      ["1. Lập yêu cầu hỏi giá, yêu cầu tính giá, phiếu tính giá cho H, gửi duyệt.", "2. A duyệt các yêu cầu của phiếu.", "3. Tìm H ở màn Cập nhật giá bán."], "—",
      ["- Bước 2: phiếu Đã duyệt; người lập nhận “[PTG] Đã duyệt”.", "- Bước 3: H Đang kinh doanh, giá = giá đã duyệt, sửa và lưu được."]),
    T(5, "Duyệt hàng loạt cuối ngày", "P1", [ACC_A, "Công ty A có 25 yêu cầu chờ (3 trang 10 dòng)."],
      ["1. Tick tất cả ở trang 1, 2, 3.", "2. Sửa giá 2 yêu cầu ở trang 2.", "3. Bấm Duyệt ở thanh hàng loạt, xác nhận."], "—",
      ["- “Đã chọn 25 yêu cầu (20 đang ẩn do bộ lọc)” khi đứng ở trang 3.", "- Thông báo “Đã duyệt 25 yêu cầu giá bán.”; danh sách rỗng.",
       "- 2 yêu cầu đã sửa áp đúng giá đã sửa."]),
]


def _norm(tc):
    return tuple(L(*x) if isinstance(x, list) else x for x in tc)


ROLE_TCS = [_norm(tc) for tc in ROLE_TCS]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP (4 LỐI VÀO)", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, PHÂN TRANG & CHỌN YÊU CẦU", S3),
    ("IV", "CHỨC NĂNG CHÍNH (SỬA GIÁ ĐỀ NGHỊ)", S4),
    ("V", "THAO TÁC TRẠNG THÁI (DUYỆT, KHÔNG DUYỆT, HÀNG LOẠT, THÔNG BÁO)", S5),
    ("VI", "GIÁ BÁN — GIÁ ÁP KHI DUYỆT, GIÁ HIỆU LỰC, GIÁ VỐN, PHIẾU TÍNH GIÁ", S6),
    ("VII", "XUẤT EXCEL", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", S8),
    ("IX", "CÔ LẬP DỮ LIỆU THEO CÔNG TY & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "E2E FLOW", S10),
]

_all = "\n".join("\n".join(map(str, x)) for x in DESCRIPTION_BLOCK + ROLE_TCS + [t for _, _, s in SECTIONS for t in s])
_bad = re.findall(r"[←-⯿\U0001F300-\U0001FAFF]", _all)
assert not _bad, "Con ky tu cam: %s" % sorted(set(_bad))

build(output_file=OUT, sheet_name="Trang tính1", feature_name="Duyệt giá bán",
      module_name="Duyệt giá bán", description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
print("OK ->", OUT)
