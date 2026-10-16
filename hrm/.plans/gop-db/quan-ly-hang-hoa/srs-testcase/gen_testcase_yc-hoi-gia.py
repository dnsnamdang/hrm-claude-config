# -*- coding: utf-8 -*-
"""Sinh testcase - Yeu cau hoi gia (luong Chuyen doi hang hoa, man 3/5).

Doi chieu code worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa (hrm-api 39c4a91fe,
hrm-client 5c14659e8 — 16/10/2026). SRS cung bo: gen_srs_yc-hoi-gia.py.
Section VI danh rieng cho GIA BAN (gia ban le hien hanh, trang thai hang x cong ty theo luong, gia ban moi / ket qua tinh
gia chi gia ban, in ket qua). So lieu mau lay tu DB dev hrm_erp_giacty Cty 1: PYCHG-04280 (Cho PTKD duyet, KOURITSU),
PYCHG-04283 (Da tinh gia, MLER-AMAT8574091 Bo: Ban le 22,500,000 DMGG 5, TMDT 29,250,000, PTG-03178, PYCTG-03162),
PYCHG-04287 (nhom TORIN Cho XNK duyet, XNK Nguyen Thi Thu Thuy), PYCHG-04282 (nhom BESITA Cho lap YCTG), hang SULI-0-1000 /
SULI-0-400C (XNK Dinh Ha Duyen), TEWI-742058 (TELWIN, XNK Tran Hanh Minh), FOFE-FCS-300 (FOFEN — CHUA co XNK phan cong).
Chay: python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_testcase_yc-hoi-gia.py
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

OUT = os.path.join(HERE, "testcase - Yêu cầu hỏi giá.xlsx")


def L(*lines):
    return "\n".join(lines)


def T(n, func, prio, pre, steps, data, exp):
    return (n, func, prio, pre if isinstance(pre, str) else L(*pre), steps if isinstance(steps, str) else L(*steps),
            data if isinstance(data, str) else L(*data), exp if isinstance(exp, str) else L(*exp))


MENU = "Vào phân hệ Bán hàng › Yêu cầu › nhóm “Hàng hóa” › bấm “YC hỏi giá”"
MENU_TRADING = "Vào phân hệ Danh mục › Hàng hoá › nhóm “Hàng hoá, vật tư” › bấm “Hàng đang kinh doanh”"
MENU_ENTERING = "Vào phân hệ Danh mục › Hàng hoá › nhóm “Hàng hoá, vật tư” › bấm “Hàng hoá nhập thông tin”"
MENU_TEMP = "Vào phân hệ Danh mục › Hàng hoá › nhóm “Hàng hoá, vật tư” › bấm “Hàng tạm”"
Q1 = "PTKD duyệt yêu cầu hỏi giá"
Q2 = "XNK xử lý yêu cầu hỏi giá"
Q3 = "Tính giá bán hàng hoá"
Q4 = "Xem giá vốn hàng hoá"
Q5 = "Xây dựng thông tin hàng hoá"
CONFLICT = "Trạng thái đã bị thay đổi. Vui lòng load lại trang"
NOTFOUND = "Không tìm thấy yêu cầu hỏi giá"
PAGE404 = "Không tìm thấy hoặc không được cấp quyền truy cập trang"
NOPERM = "Bạn không có quyền thực hiện chức năng này"
NOT_XNK = "Bạn không phải XNK phụ trách nhóm này."
NO_ROW = "Vui lòng chọn ít nhất 1 hàng hoá"
NO_XNK_FOFEN = "Nhóm FOFEN — Fofen (Foshan Analytical Instrument Co., Ltd.) chưa có XNK phụ trách tại công ty, chưa gửi được."
REQ = "Bắt buộc phải nhập"

ACC_S = "Tài khoản S (nhân viên kinh doanh) KHÔNG có quyền nào của luồng hỏi giá, đang chọn công ty 1."
ACC_S2 = "Tài khoản S2 (nhân viên khác cùng công ty 1) KHÔNG có quyền nào của luồng hỏi giá."
ACC_P = "Tài khoản P có quyền " + Q1 + " tại công ty 1, đang chọn công ty 1."
ACC_X = ("Tài khoản X = Nguyễn Thị Thu Thủy có quyền " + Q2 + " tại công ty 1 và đang được phân công phụ trách TORIN × TORIN "
         "tại công ty 1.")
ACC_X2 = "Tài khoản X2 có quyền " + Q2 + " tại công ty 1 nhưng KHÔNG được phân công TORIN × TORIN."
GOODS = ["Hàng tại công ty 1:",
         "- SULI-0-1000, SULI-0-400C (SULI — JIANGSU SULI MACHINERY CO., LTD): Đang kinh doanh; XNK phân công Đinh Hà Duyên.",
         "- TEWI-742058 (TELWIN — Telwin S.p.A): Đang kinh doanh; XNK phân công Trần Hạnh Minh.",
         "- FOFE-FCS-300 (FOFEN — Fofen (Foshan Analytical Instrument Co., Ltd.)): Đang kinh doanh; CHƯA có XNK phân công.",
         "- Hàng H1 (SULI): Đang nhập thông tin."]

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     L("Yêu cầu hỏi giá (YCHG, phân hệ Bán hàng) là chứng từ đầu tiên của luồng tính giá bán:",
       "- Ai cũng lập được (không cần quyền), cho hàng Đang nhập thông tin / Đang kinh doanh / hàng tạm của công ty đang làm việc.",
       "- Hàng tự gom nhóm Thương hiệu — Hãng; mỗi nhóm đi tới XNK được phân công phụ trách hãng tại công ty.",
       "- PTKD (quyền " + Q1 + ") duyệt / từ chối cả phiếu; XNK phụ trách duyệt nhóm, báo không có giá, huỷ duyệt, lập YCTG.",
       "- Khi giá của nhóm được áp (qua Phiếu tính giá / Duyệt giá bán), YCHG hiện giá bán mới trong “Chi tiết kết quả” và in được kết quả.")),
    ("2. Đối tượng được tính / hiển thị",
     L("- Danh sách: phiếu của CÔNG TY ĐANG LÀM VIỆC ở các trạng thái Chờ PTKD duyệt, Đang hỏi giá, Đã tính giá, Không có giá, Huỷ duyệt "
       "(mọi người trong công ty thấy).",
       "- Phiếu Đang tạo và Không duyệt: CHỈ người lập thấy.",
       "- Mỗi phiếu bung được các dòng nhóm: Chờ XNK duyệt, Chờ lập YCTG, Đang tính giá, Đã tính giá, Không có giá, Huỷ duyệt.",
       "- Popup Chọn hàng hoá: hàng Đang nhập thông tin / Đang kinh doanh tại công ty; hàng tạm (Hàng tạm, Hàng tạm không duyệt) chưa nằm trong YCHG mở.")),
    ("3. Đối tượng bị ẩn / không tính",
     L("- Phiếu của công ty khác (báo “" + NOTFOUND + "”, không lộ là có phiếu).",
       "- Phiếu Đang tạo / Không duyệt của người khác (mở thẳng ra trang “" + PAGE404 + "”).",
       "- Hàng không chọn được: Chờ tính giá bán / Đang tính giá (đang ở YCHG khác), Ngừng kinh doanh, chưa dùng ở công ty, đã xoá, "
       "hàng tạm đã duyệt chờ duyệt phiếu, hàng tạm đang nằm trong YCHG mở khác.",
       "- Trong Chi tiết kết quả: KHÔNG có giá NCC, chi phí, giá nhập kho, giá vốn.")),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô lọc “Ngày tạo” (khoảng từ ngày – đến ngày) lọc theo ngày lập phiếu, tính trọn cả ngày đầu và ngày cuối. Không có lọc thời gian nào khác."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     L("- Phiếu › nhóm (Thương hiệu × Hãng, số La Mã, sắp tên A đến Z) › hàng (1, 2, 3…).",
       "- Nhóm gom lại MỖI lần lưu; không chọn ĐVT (hỏi giá cho mọi ĐVT).",
       "- 1 nhóm – 1 YCTG – 1 PTG; giá bán mới hiện dưới từng mã hàng, mỗi ĐVT 1 dòng, 6 loại giá.")),
    ("6. Quy tắc cộng dồn / deduplicate",
     L("- Cột Số mã hàng đếm số mã hàng KHÁC NHAU của phiếu.",
       "- “a/b nhóm đã tính giá”: a = số nhóm Đã tính giá, b = tổng số nhóm.",
       "- Chân bảng đếm số PHIẾU (dòng nhóm không tính).",
       "- Chọn trùng 1 hàng ở popup chỉ thêm 1 lần.")),
    ("7. Phân quyền cấp",
     L("Lập / sửa / gửi / xoá / xem / in YCHG KHÔNG cần quyền. Không phân quyền theo phòng ban / cấp. Các quyền (xét TẠI công ty phiếu):",
       "- " + Q1 + ": Duyệt / Từ chối mọi phiếu Chờ PTKD duyệt; duyệt từng hàng tạm; nhận thông báo Chờ duyệt.",
       "- " + Q2 + ": chỉ có tác dụng khi người dùng là XNK được phân công HIỆN HÀNH của thương hiệu × hãng của nhóm.",
       "- " + Q3 + " / " + Q4 + ": chỉ mở link số YCTG trên dòng nhóm.",
       "- " + Q5 + ": sửa hàng tạm do người khác tạo.",
       "Super admin không được miễn.")),
    ("8. Cách tính các ô thống kê",
     L("- Chân bảng “Hiển thị a–b / N yêu cầu”: N = tổng số phiếu khớp bộ lọc.",
       "- Giá bán lẻ hiện hành = giá Bán lẻ đang áp dụng của ĐVT cơ bản tại công ty phiếu, đọc lúc mở màn; chưa có dòng giá thì để trống.",
       "- Giá bán mới = bản chụp lúc áp giá: 6 loại giá × ĐVT + ĐMGG; TMĐT = Bán lẻ × hệ số TMĐT của công ty (vd 22,500,000 × 1.3 = 29,250,000).",
       "- Phiếu Đã tính giá khi mọi nhóm đã đóng và có ít nhất 1 nhóm có giá; mọi nhóm đóng mà không nhóm nào có giá thì Không có giá.")),
    ("9. Ghi chú đọc bảng",
     L("- Số tiền dấu phẩy ngăn nghìn (22,500,000); ngày dd/mm/yyyy.",
       "- Bẫy 1: hàng Đang kinh doanh GIỮ trạng thái suốt luồng; chỉ hàng Đang nhập thông tin đổi sang Chờ tính giá bán khi gửi.",
       "- Bẫy 2: có quyền " + Q2 + " CHƯA đủ — phải đúng người được phân công hãng; đổi phân công thì người mới xử lý.",
       "- Bẫy 3: hàng Đang kinh doanh đang ở YCHG khác chỉ CẢNH BÁO, không chặn; hàng Đang nhập thông tin đang ở YCHG khác thì CHẶN.",
       "- Bẫy 4: Lưu nháp không kiểm XNK; chỉ Lưu và gửi duyệt mới chặn nhóm thiếu XNK.",
       "- Bẫy 5: xem giá bán mới KHÔNG cần quyền Xem giá vốn; giá hiện hành có thể khác giá mới nếu sau đó sửa ở màn Cập nhật giá bán.",
       "- Môi trường thử: DB dev có PYCHG-04280 (Chờ PTKD duyệt), 04283 (Đã tính giá), 04287 (Chờ XNK duyệt), 04282 (Chờ lập YCTG); "
       "danh mục Loại sản phẩm rỗng nên KHÔNG tạo được hàng tạm (phải nhập cây phân loại trước); phân công XNK chỉ có ở công ty 1 và 4.",
       "- Nhóm ca 'gọi thẳng chức năng, bỏ qua giao diện' dành cho tester kỹ thuật (dùng công cụ kiểm thử API).")),
]

# ------------------------------------------------------------------ PHAN QUYEN
ROLE_TCS = [
    ("01", "Không có quyền nào: vẫn xem danh sách, lập phiếu", "P0", [ACC_S],
     ["1. Đăng nhập S.", "2. " + MENU + "."], "—",
     ["- Thấy mục “YC hỏi giá”, màn mở, có nút Tạo mới.", "- Thấy các phiếu đã gửi của công ty 1 (vd PYCHG-04283, PYCHG-04280).",
      "- Không có nút Xử lý ở dòng nào; chỉ có nút In."]),
    ("02", "Không có quyền nào: không thấy Duyệt / Từ chối", "P0", [ACC_S, "PYCHG-04280 đang Chờ PTKD duyệt."],
     ["1. " + MENU + ".", "2. Bấm số phiếu PYCHG-04280."], "—",
     ["- Màn Chi tiết mở, chân màn chỉ có In và Quay lại.", "- KHÔNG có nút Duyệt, Từ chối."]),
    ("03", "Có " + Q1 + ": thấy Duyệt / Từ chối phiếu Chờ PTKD duyệt", "P0", [ACC_P, "PYCHG-04280 đang Chờ PTKD duyệt, do người khác lập."],
     ["1. " + MENU + ".", "2. Ở dòng PYCHG-04280 bấm Xử lý."], "—",
     ["- Dòng PYCHG-04280 có nút Xử lý.", "- Chân màn Chi tiết có Duyệt (xanh), Từ chối (đỏ), In, Quay lại.",
      "- Lưu ý: PTKD duyệt được mọi phiếu của công ty, không xét phân công hãng."]),
    ("04", "Có " + Q1 + " ở công ty KHÁC, không có ở công ty 1", "P0",
     ["Tài khoản P4 có quyền " + Q1 + " tại công ty 4, không có tại công ty 1; đang chọn công ty 1."],
     ["1. Mở Chi tiết PYCHG-04280."], "—", ["- Không có nút Duyệt / Từ chối (quyền phải gán ở đúng công ty phiếu)."]),
    ("05", "Có " + Q2 + " và đúng phân công: thấy nút nhóm", "P0", [ACC_X, "PYCHG-04287 nhóm TORIN Chờ XNK duyệt."],
     ["1. " + MENU + ".", "2. Bung dòng PYCHG-04287.", "3. Bấm Xử lý nhóm."], "—",
     ["- Dòng nhóm TORIN có icon Xử lý nhóm.", "- Màn Chi tiết cuộn tới nhóm TORIN (nền xanh), có nút Duyệt và Không có giá."]),
    ("06", "Có " + Q2 + " nhưng KHÔNG đúng phân công", "P0", [ACC_X2, "PYCHG-04287 nhóm TORIN Chờ XNK duyệt."],
     ["1. Mở Chi tiết PYCHG-04287."], "—",
     ["- Nhóm TORIN không có nút Duyệt / Không có giá; hiện chữ xám “Chờ Nguyễn Thị Thu Thủy duyệt”."]),
    ("07", "Có " + Q3 + " hoặc " + Q4 + ": mở được link YCTG", "P1",
     ["Tài khoản K có quyền " + Q4 + " tại công ty 1.", "PYCHG-04283 nhóm MULLER có YCTG PYCTG-03162."],
     ["1. Mở Chi tiết PYCHG-04283.", "2. Bấm PYCTG-03162 trên dòng nhóm."], "—",
     ["- PYCTG-03162 là link, mở màn Chi tiết YCTG.", "- Với tài khoản S (không quyền): PYCTG-03162 là chữ thường, không bấm được."]),
    ("08", "Super admin chưa được gán " + Q1, "P1", ["Tài khoản quản trị cao nhất, không được gán quyền " + Q1 + " tại công ty 1."],
     ["1. Mở Chi tiết PYCHG-04280."], "—", ["- Không có nút Duyệt / Từ chối (không được miễn quyền)."]),
    ("09", "Người khác không thấy phiếu Đang tạo / Không duyệt", "P0",
     [ACC_S, ACC_S2, "S2 có phiếu PYCHG-A Đang tạo và PYCHG-B Không duyệt."],
     ["1. S mở danh sách, tìm PYCHG-A, PYCHG-B.", "2. S mở thẳng màn Chi tiết PYCHG-B (từ lịch sử trình duyệt / link được gửi)."], "—",
     ["- Bước 1: không có kết quả (“Không có dữ liệu phù hợp”).", "- Bước 2: trang “" + PAGE404 + "”."]),
    ("10", "Bỏ qua giao diện: PTKD duyệt / từ chối khi không có quyền", "P0", [ACC_S, "PYCHG-04280 Chờ PTKD duyệt."],
     ["1. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt PYCHG-04280.", "2. Gọi thẳng chức năng Từ chối với lý do “x”."], "—",
     ["- Cả 2 bị từ chối, báo “" + NOPERM + "”.", "- PYCHG-04280 vẫn Chờ PTKD duyệt, lịch sử không thêm dòng."]),
    ("11", "Bỏ qua giao diện: XNK duyệt nhóm khi không có quyền / sai phân công", "P0",
     [ACC_S, ACC_X2, "PYCHG-04287 nhóm TORIN Chờ XNK duyệt."],
     ["1. S gọi thẳng chức năng Duyệt nhóm TORIN.", "2. X2 gọi thẳng chức năng Duyệt nhóm TORIN.", "3. X2 gọi thẳng Không có giá với lý do “x”."], "—",
     ["- Bước 1: “" + NOPERM + "”.", "- Bước 2, 3: “" + NOT_XNK + "”.", "- Nhóm TORIN vẫn Chờ XNK duyệt."]),
    ("12", "Bỏ qua giao diện: sửa / xoá phiếu của người khác", "P0", [ACC_S, ACC_S2, "S2 có phiếu PYCHG-A Đang tạo."],
     ["1. S gọi thẳng chức năng Sửa PYCHG-A.", "2. S gọi thẳng chức năng Xoá PYCHG-A."], "—",
     ["- Cả 2: “" + NOTFOUND + "” (phiếu nháp người khác coi như không có).", "- PYCHG-A không đổi."]),
    ("13", "Bỏ qua giao diện: thao tác phiếu của công ty khác", "P0",
     ["Tài khoản P có quyền " + Q1 + " ở cả công ty 1 và 4; đang chọn công ty 1.", "Phiếu PYCHG-C thuộc công ty 4, Chờ PTKD duyệt."],
     ["1. Gọi thẳng chức năng xem chi tiết PYCHG-C.", "2. Gọi thẳng Duyệt PYCHG-C.", "3. Gọi thẳng In PYCHG-C."], "—",
     ["- Cả 3: “" + NOTFOUND + "”.", "- Phải đổi sang công ty 4 mới thao tác được."]),
    ("14", "Bỏ qua giao diện: form Duyệt hàng tạm khi không có " + Q1, "P1",
     [ACC_S, "PYCHG-D Chờ PTKD duyệt có hàng tạm HT1."],
     ["1. Gọi thẳng chức năng mở dữ liệu form Duyệt hàng tạm HT1.", "2. Mở thẳng màn Duyệt hàng tạm HT1 trên trình duyệt."], "—",
     ["- Bước 1: “" + NOPERM + "”.", "- Bước 2: trang “" + PAGE404 + "”."]),
]

# ------------------------------------------------------------------ I
S1 = [
    T(1, "Mở màn từ menu", "P0", [ACC_S], ["1. " + MENU + "."], "—",
      ["- Tiêu đề “Yêu cầu hỏi giá”.", "- Bảng 9 cột: STT, Số phiếu, Số mã hàng, Nhóm Thương hiệu — Hãng, Người tạo, Ngày tạo, PTKD duyệt, Trạng thái, Hành động.",
       "- Mặc định 10 dòng / trang, phiếu mới tạo lên trước."]),
    T(2, "Lối vào từ màn Hàng đang kinh doanh có tick hàng", "P0", [ACC_S] + GOODS,
      ["1. " + MENU_TRADING + ".", "2. Tick SULI-0-1000 và TEWI-742058.", "3. Bấm “Lập yêu cầu hỏi giá” ở đầu bảng."], "—",
      ["- Mở form “Tạo yêu cầu hỏi giá” nạp sẵn 2 hàng, 2 nhóm (SULI, TELWIN).", "- Bấm Quay lại: về màn Hàng đang kinh doanh."]),
    T(3, "Lối vào từ màn Hàng hoá nhập thông tin không tick hàng", "P1", [ACC_S],
      ["1. " + MENU_ENTERING + ".", "2. Không tick, bấm “Lập yêu cầu hỏi giá”."], "—", ["- Form Tạo trống, bảng “Chưa có hàng hoá nào. Bấm \"Chọn hàng hoá\" để thêm.”"]),
    T(4, "Lối vào từ màn Hàng tạm", "P1", [ACC_S, "Có hàng tạm HT2 do S tạo, chưa nằm trong YCHG nào (cần cây phân loại có dữ liệu)."],
      ["1. " + MENU_TEMP + ".", "2. Ở dòng HT2 bấm hành động “Lập yêu cầu hỏi giá”."], "—",
      ["- Form Tạo nạp sẵn HT2, trạng thái hàng “Hàng tạm”."]),
    T(5, "Nạp sẵn hàng không lập được thì bị loại kèm câu báo", "P0", [ACC_S, "SUKE-BT-11410301-20A chưa dùng ở công ty 1; SULI-0-400C Đang kinh doanh."],
      ["1. Từ màn hàng hoá tick 2 hàng trên (hoặc mở form với 2 hàng này) rồi bấm Lập yêu cầu hỏi giá."], "—",
      ["- Thông báo “Bỏ 1 hàng không lập yêu cầu hỏi giá được: SUKE-BT-11410301-20A (Hàng chưa dùng ở công ty)”.", "- Form chỉ còn SULI-0-400C."]),
    T(6, "Mở từ thông báo “[YCHG] Chờ duyệt … Nhóm …”", "P0", [ACC_X, "PTKD vừa duyệt PYCHG-04287."],
      ["1. Bấm chuông.", "2. Bấm thông báo “[YCHG] Chờ duyệt: PYCHG-04287. Nhóm: TORIN — …”."], "—",
      ["- Mở Chi tiết PYCHG-04287, nhóm TORIN tô nền xanh, nằm giữa màn."]),
    T(7, "Mở từ link YCHG ở màn YCTG / PTG", "P1", [ACC_X, "PYCTG-03162 thuộc PYCHG-04283."],
      ["1. Mở Chi tiết PYCTG-03162.", "2. Bấm link PYCHG-04283."], "—", ["- Mở Chi tiết PYCHG-04283."]),
    T(8, "Mở thẳng màn Sửa của phiếu không sửa được", "P1", [ACC_S, "PYCHG-04283 Đã tính giá."],
      ["1. Mở thẳng màn Sửa PYCHG-04283 trên trình duyệt."], "—", ["- Tự chuyển sang màn Chi tiết PYCHG-04283, không có ô nhập."]),
    T(9, "Đổi công ty đang làm việc", "P0", ["Tài khoản S làm việc ở công ty 1 và 4."],
      ["1. Ở công ty 1 mở danh sách, ghi số phiếu đầu tiên.", "2. Đổi sang công ty 4."], "—",
      ["- Danh sách tải lại, chỉ còn phiếu công ty 4; không còn phiếu nào của công ty 1."]),
    T(10, "Danh sách rỗng / lỗi tải", "P2", ["Tài khoản ở công ty chưa có YCHG nào."], ["1. Mở màn."], "—",
      ["- Bảng “Không có dữ liệu phù hợp”, chân bảng 0.", "- Mất mạng khi tải: thông báo “Lỗi khi tải dữ liệu”."]),
]

# ------------------------------------------------------------------ II
S2 = [
    T(1, "Tìm theo số phiếu", "P0", [ACC_S], ["1. Gõ “04283” vào ô tìm nhanh.", "2. Nhấn Enter."], "Từ khoá: 04283",
      ["- Chỉ còn PYCHG-04283.", "- Về trang 1."]),
    T(2, "Tìm theo mã / tên hàng trong phiếu", "P0", [ACC_S], ["1. Gõ “AMAT8574091”, bấm Tìm kiếm.", "2. Gõ “Bình bơm dầu”, bấm Tìm kiếm."], "—",
      ["- Bước 1: có PYCHG-04283.", "- Bước 2: có PYCHG-04280."]),
    T(3, "Ô tìm nhanh không tìm theo tên người", "P1", [ACC_S], ["1. Gõ “Nguyễn Anh Tú” (người lập PYCHG-04280), Enter."], "—",
      ["- Không ra PYCHG-04280 (tên người tìm bằng ô chọn Người tạo)."]),
    T(4, "Lọc Trạng thái Chờ PTKD duyệt", "P0", [ACC_S, "Công ty 1 có đúng 1 phiếu Chờ PTKD duyệt (PYCHG-04280)."],
      ["1. Bấm Tìm kiếm nâng cao.", "2. Trạng thái = Chờ PTKD duyệt."], "—", ["- Chỉ 1 dòng PYCHG-04280; chân bảng 1."]),
    T(5, "Lọc Đang hỏi giá gồm cả phiếu cũ ERP", "P1", [ACC_S], ["1. Trạng thái = Đang hỏi giá."], "—",
      ["- Ra cả phiếu mới (PTKD vừa duyệt) và phiếu cũ đang ở bước XNK / tính giá (vd PYCHG-04287, PYCHG-04282); trạng thái đều ghi “Đang hỏi giá”."]),
    T(6, "Lọc Đang tạo chỉ ra phiếu của mình", "P0", [ACC_S, "S có 1 phiếu Đang tạo; S2 có 3 phiếu Đang tạo."], ["1. S lọc Trạng thái = Đang tạo."], "—",
      ["- Chỉ 1 dòng (phiếu của S)."]),
    T(7, "Lọc Thương hiệu / Hãng sản xuất", "P1", [ACC_S], ["1. Thương hiệu = MULLER.", "2. Bỏ, chọn Hãng sản xuất = TORIN (Changshu …)."], "—",
      ["- Bước 1: ra phiếu có nhóm MULLER (PYCHG-04283).", "- Bước 2: ra PYCHG-04287.", "- Ô chọn chỉ liệt kê thương hiệu / hãng có trong phiếu của công ty."]),
    T(8, "Lọc Người tạo / PTKD duyệt / XNK tiếp nhận", "P1", [ACC_S],
      ["1. Người tạo = Nguyễn Anh Tú.", "2. Làm mới, PTKD duyệt = Đặng Tiến Mạnh.", "3. Làm mới, XNK tiếp nhận = Nguyễn Thị Thanh Trà."], "—",
      ["- Bước 1: có PYCHG-04280, 04281, 04282.", "- Bước 2: có PYCHG-04283.", "- Bước 3: có PYCHG-04283.",
       "- Lưu ý: PTKD duyệt gồm cả người đã TỪ CHỐI phiếu."]),
    T(9, "Lọc Ngày tạo tính trọn ngày cuối", "P1", [ACC_S, "PYCHG-04287 tạo 15/09/2026 09:37."],
      ["1. Ngày tạo từ 15/09/2026 đến 15/09/2026."], "—", ["- Có PYCHG-04287 và PYCHG-04286; không có phiếu ngày 14/09."]),
    T(10, "Làm mới và ghi nhớ bộ lọc", "P2", [ACC_S],
      ["1. Lọc Trạng thái = Đã tính giá.", "2. Mở Chi tiết 1 phiếu rồi Quay lại.", "3. Bấm Làm mới."], "—",
      ["- Bước 2: vẫn giữ lọc Đã tính giá (ghi nhớ 10 phút).", "- Bước 3: xoá hết điều kiện, sắp lại Ngày tạo mới đến cũ."]),
]

# ------------------------------------------------------------------ III
S3 = [
    T(1, "Bung / thu dòng nhóm", "P0", [ACC_S], ["1. Bấm nút mũi tên ở cột STT của PYCHG-04283.", "2. Bấm lại."], "—",
      ["- Bước 1: thêm dòng nhóm nền xanh “MULLER — MULLER AUTOMOTIVE SÂS”, nhãn “1 mã hàng”, “XNK: Nguyễn Thị Thanh Trà - HN_XNK - 12210394”, PYCTG-03162, Đã tính giá.",
       "- Bước 2: dòng nhóm ẩn."]),
    T(2, "Nội dung các cột dòng phiếu", "P1", [ACC_S], ["1. Đọc dòng PYCHG-04283."], "—",
      ["- Số mã hàng 1; “1/1 nhóm đã tính giá”; Người tạo “Đặng Tiến Mạnh - HN_XNK - 12210327”; Ngày tạo 14/09/2026.",
       "- PTKD duyệt: “Đặng Tiến Mạnh - HN_XNK - 12210327” + “14/09/2026 16:01”; Trạng thái Đã tính giá (xanh lá)."]),
    T(3, "Dòng nhóm của phiếu chưa qua PTKD", "P1", [ACC_S], ["1. Bung PYCHG-04280."], "—",
      ["- Dòng nhóm KOURITSU có XNK, KHÔNG có nhãn trạng thái nhóm, cột PTKD duyệt trống."]),
    T(4, "Chữ chờ ở dòng nhóm cho người không phải XNK", "P1", [ACC_S], ["1. Bung PYCHG-04287."], "—",
      ["- Nhóm TORIN Chờ XNK duyệt, cột PTKD duyệt “chưa có YCTG”, cột Hành động chữ xám “Chờ Nguyễn Thị Thu Thủy duyệt”.",
       "- Lưu ý: kiểm bảng KHÔNG bị tràn ngang sau khi bung (cột Hành động phải nằm trọn trong khung)."]),
    T(5, "Sắp xếp theo cột", "P1", [ACC_S], ["1. Bấm tiêu đề Số phiếu.", "2. Bấm tiếp.", "3. Bấm tiêu đề PTKD duyệt."], "—",
      ["- Bước 1, 2: số phiếu tăng / giảm.", "- Bước 3: sắp theo thời điểm PTKD xử lý.", "- Chỉ 3 cột sắp được: Số phiếu, Ngày tạo, PTKD duyệt."]),
    T(6, "Phân trang", "P1", [ACC_S, "Tài khoản thấy 2.560 phiếu ở công ty 1."], ["1. Đổi Số dòng/trang = 50.", "2. Sang trang 2."], "—",
      ["- “Hiển thị 51–100 / 2560 yêu cầu”; STT tiếp tục 51…", "- Lựa chọn số dòng: 5, 10, 20, 50, 100."]),
    T(7, "Cài đặt cột: cột khoá", "P2", [ACC_S], ["1. Bấm Cấu hình cột.", "2. Bấm Bỏ chọn hết, Lưu."], "—",
      ["- Popup “Tuỳ chỉnh cột”, “Đang chọn 9/9 cột”.", "- Sau khi lưu: còn STT, Số phiếu, Hành động (3 cột khoá)."]),
    T(8, "Nút hành động theo vai", "P0", [ACC_S, "S có 1 phiếu Đang tạo PYCHG-E."], ["1. Xem cột Hành động của PYCHG-E và PYCHG-04283."], "—",
      ["- PYCHG-E: Sửa, Xóa, In.", "- PYCHG-04283: chỉ In."]),
]

# ------------------------------------------------------------------ IV
S4 = [
    T(1, "Form Tạo trống", "P1", [ACC_S], ["1. " + MENU + ".", "2. Bấm Tạo mới."], "—",
      ["- Tiêu đề “Tạo yêu cầu hỏi giá”; Số phiếu trống placeholder “Tự sinh khi lưu”; Công ty = công ty 1 (khoá); Người tạo = S; trạng thái Đang tạo.",
       "- Footer: Lưu nháp, Lưu và gửi duyệt, Quay lại. Không có “Lưu và tiếp tục”."]),
    T(2, "Chọn hàng bằng popup", "P0", [ACC_S] + GOODS,
      ["1. Bấm Chọn hàng hoá.", "2. Gõ “SULI-0-”.", "3. Tick SULI-0-1000, SULI-0-400C.", "4. Bấm Chọn."], "—",
      ["- Popup hiện 3 hàng SULI-0-…, chân “Đã chọn: 2”.", "- Bảng phiếu: nhóm I “SULI — JIANGSU SULI MACHINERY CO., LTD” “2 mã hàng”, “XNK tiếp nhận: Đinh Hà Duyên - HN-DATD - 11210078”."]),
    T(3, "Popup chọn hàng loại hàng đã có trên phiếu", "P1", ["Như ca 2, phiếu đã có 2 hàng SULI."], ["1. Mở lại Chọn hàng hoá, gõ “SULI-0-”."], "—",
      ["- Chỉ còn SULI-0-400C:01; tổng “Hiển thị 1–1 / 1”."]),
    T(4, "Popup giữ tick qua trang và từ khoá", "P2", [ACC_S], ["1. Tick 1 hàng trang 1.", "2. Sang trang 2 tick 1 hàng.", "3. Đổi từ khoá rồi bấm Chọn."], "—",
      ["- “Đã chọn: 2”; cả 2 hàng vào phiếu."]),
    T(5, "Gom nhiều nhóm, sắp theo tên", "P0", [ACC_S] + GOODS,
      ["1. Chọn TEWI-742058, SULI-0-1000, FOFE-FCS-300."], "—",
      ["- 3 nhóm theo thứ tự I FOFEN, II SULI, III TELWIN.", "- Nhóm FOFEN hiện cảnh báo nâu “Chưa có XNK phụ trách tại công ty — chưa gửi được”."]),
    T(6, "Lưu nháp khi có nhóm thiếu XNK", "P0", ["Như ca 5."], ["1. Bấm Lưu nháp."], "—",
      ["- “Đã lưu nháp yêu cầu hỏi giá”; về danh sách; phiếu mới PYCHG-xxxxx Đang tạo ở đầu.", "- Trạng thái 3 hàng không đổi."]),
    T(7, "Gửi khi có nhóm thiếu XNK bị chặn", "P0", ["Như ca 5."], ["1. Bấm Lưu và gửi duyệt."], "—",
      ["- Chữ đỏ “" + NO_XNK_FOFEN + "”.", "- Không hiện hộp xác nhận, không gửi, ở lại form."]),
    T(8, "Bỏ hàng khỏi phiếu", "P1", ["Như ca 7."], ["1. Bấm thùng rác ở FOFE-FCS-300."], "—",
      ["- Hàng bị bỏ ngay (không hỏi lại); nhóm FOFEN biến mất; chữ đỏ biến mất."]),
    T(9, "Gửi duyệt thành công", "P0", [ACC_S, "Phiếu có SULI-0-1000 (Đang KD), H1 (Đang nhập thông tin), TEWI-742058."],
      ["1. Bấm Lưu và gửi duyệt.", "2. Đọc hộp xác nhận, bấm Lưu và gửi duyệt."], "—",
      ["- Hộp “Gửi yêu cầu hỏi giá”: “Gửi yêu cầu hỏi giá mới (3 mã hàng, 2 nhóm) cho PTKD duyệt? Hàng đang nhập thông tin sẽ chuyển sang \"Chờ tính giá bán\".”",
       "- “Đã gửi yêu cầu hỏi giá”; phiếu Chờ PTKD duyệt.", "- H1 thành Chờ tính giá bán; SULI-0-1000, TEWI-742058 vẫn Đang kinh doanh.",
       "- Lịch sử: “Lập phiếu yêu cầu hỏi giá”."]),
    T(10, "Hủy ở hộp xác nhận gửi", "P2", ["Như ca 9."], ["1. Bấm Lưu và gửi duyệt.", "2. Bấm Hủy."], "—", ["- Không gửi, ở lại form, dữ liệu còn nguyên."]),
    T(11, "Cảnh báo hàng đang được hỏi giá ở phiếu khác", "P0", [ACC_S, "TORI-TRW05001 (Đang KD) đang nằm trong PYCHG-04287 (Đang hỏi giá)."],
      ["1. Chọn TORI-TRW05001 vào phiếu mới.", "2. Lưu và gửi duyệt."], "—",
      ["- Dưới tên hàng: “Đang được hỏi giá ở PYCHG-04287” (nâu).", "- Vẫn gửi được (chỉ cảnh báo)."]),
    T(12, "Rời form chưa lưu", "P1", [ACC_S], ["1. Chọn 1 hàng.", "2. Bấm Quay lại.", "3. Bấm Ở lại, rồi Quay lại, bấm Thoát."], "—",
      ["- Hộp “Thông tin chưa lưu”: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”.", "- Ở lại: giữ form; Thoát: về danh sách, không lưu."]),
    T(13, "Popup Thêm hàng tạm: bắt buộc đồng thời", "P1", [ACC_S], ["1. Bấm Thêm hàng tạm.", "2. Tab Thêm mới thủ công, bấm Lưu khi trống."], "—",
      ["- 9 ô báo “Bắt buộc phải nhập” / “Bắt buộc phải chọn” (Tên, ĐVT, Model, Thương hiệu, Xuất xứ, Hãng sản xuất, % VAT, Loại sản phẩm, Đặc tính).",
       "- 3 ô cây: “Chưa có tính chất — chọn Loại sản phẩm”, “Chưa có nhóm chức năng — chọn Loại sản phẩm”, “Chưa có nhóm sản phẩm — chọn Loại sản phẩm”.",
       "- Thông báo “Vui lòng kiểm tra lại dữ liệu nhập”; popup không đóng."]),
    T(14, "Thêm hàng tạm thành công", "P1", [ACC_S, "Danh mục Loại sản phẩm / Đặc tính đã có dữ liệu."],
      ["1. Nhập đủ ô (Tên “Kìm test YCHG”, ĐVT Cái, Thương hiệu SULI, Hãng JIANGSU SULI…).", "2. Bấm Lưu."], "—",
      ["- “Đã thêm hàng tạm <mã> vào phiếu”; hàng vào nhóm SULI, trạng thái “Hàng tạm”."]),
    T(15, "Tái sử dụng dòng tạm BOM", "P2", [ACC_S, "Dự án S được xem có dòng tạm HHB000123 trong BOM-2026-00029 chưa thành hàng."],
      ["1. Thêm hàng tạm › tab Tái sử dụng.", "2. Chọn dòng HHB000123, bấm Dùng hàng này.", "3. Nhập nốt ô trống, Lưu."], "—",
      ["- Tab nhập điền sẵn + dải “Điền sẵn từ HHB000123 (BOM · <dự án>)”.", "- Sau khi lưu: dòng hàng có “Lập từ HHB000123 · BOM BOM-2026-00029”."]),
    T(16, "Sửa hàng tạm: chỉ người tạo hoặc " + Q5, "P1", [ACC_S, ACC_S2, "HT3 do S2 tạo nằm trong phiếu của S."],
      ["1. S xem dòng HT3 ở form Sửa.", "2. Gán " + Q5 + " cho S, tải lại."], "—", ["- Bước 1: không có nút bút Sửa hàng tạm.", "- Bước 2: có nút bút."]),
    T(17, "Sửa phiếu Không duyệt rồi gửi lại", "P0", [ACC_S, "Phiếu PYCHG-F của S bị PTKD từ chối lý do “Thiếu model”."],
      ["1. Ở danh sách bấm Sửa PYCHG-F.", "2. Thêm 1 hàng, Lưu và gửi duyệt, xác nhận."], "—",
      ["- Màn “Sửa yêu cầu hỏi giá: PYCHG-F”, trạng thái Không duyệt.", "- Gửi xong: Chờ PTKD duyệt; cột PTKD duyệt trống lại; lịch sử vẫn còn dòng “PTKD không duyệt”."]),
    T(18, "Xem chi tiết phiếu đã tính giá", "P0", [ACC_S], ["1. Bấm PYCHG-04283."], "—",
      ["- Tiêu đề “Chi tiết yêu cầu hỏi giá: PYCHG-04283”; mọi ô chỉ đọc.",
       "- Nhóm MULLER: XNK Nguyễn Thị Thanh Trà, Đã tính giá, PYCTG-03162, “Giá bán mới áp ngày 14/09/2026 · Nguyễn Thị Minh - BDH - 10410007 · PTG-03178”, nút In kết quả.",
       "- “Ghi chú PTKD: Reference: AMAT8574091 Price: EUR 316”; lịch sử mới đến cũ."]),
    T(19, "Xoá phiếu nháp", "P0", [ACC_S, "S có phiếu PYCHG-E Đang tạo."], ["1. Bấm Xóa ở dòng PYCHG-E.", "2. Bấm Xóa ở hộp xác nhận."], "—",
      ["- Hộp “Xác nhận xóa”: “Xóa yêu cầu hỏi giá PYCHG-E? Thao tác không hoàn tác được.”", "- “Đã xoá yêu cầu hỏi giá”; PYCHG-E biến khỏi danh sách."]),
    T(20, "Xoá phiếu Không duyệt không đổi trạng thái hàng", "P1", [ACC_S, "PYCHG-F Không duyệt chứa H1 (đã về Đang nhập thông tin)."],
      ["1. Xoá PYCHG-F."], "—", ["- Xoá thành công; H1 vẫn Đang nhập thông tin."]),
    T(21, "Hủy xoá", "P2", [ACC_S], ["1. Bấm Xóa, bấm Hủy."], "—", ["- Phiếu còn nguyên."]),
    T(22, "Mỗi lần lưu gom lại nhóm", "P1", [ACC_S, "Phiếu nháp có nhóm SULI và TELWIN."], ["1. Sửa: bỏ TEWI-742058, Lưu nháp.", "2. Mở Chi tiết."], "—",
      ["- Chỉ còn nhóm I SULI."]),
]

# ------------------------------------------------------------------ V
S5 = [
    T(1, "PTKD duyệt phiếu", "P0", [ACC_P, "PYCHG-04280 Chờ PTKD duyệt, nhóm KOURITSU có XNK Vũ Thị Huyền Trang."],
      ["1. Mở Chi tiết PYCHG-04280, bấm Duyệt.", "2. Nhập ghi chú “Ưu tiên báo trong tuần”, bấm Duyệt."], "—",
      ["- Popup “Duyệt yêu cầu hỏi giá” “PYCHG-04280 — 1 nhóm sẽ chuyển tới XNK phụ trách”, ghi chú không bắt buộc.",
       "- “Đã duyệt yêu cầu hỏi giá”; phiếu Đang hỏi giá; nhóm Chờ XNK duyệt; cột PTKD duyệt = P.",
       "- Vũ Thị Huyền Trang nhận “[YCHG] Chờ duyệt: PYCHG-04280. Nhóm: KOURITSU — Cửa hàng lẻ”."]),
    T(2, "PTKD duyệt không nhập ghi chú", "P1", ["Như ca 1."], ["1. Bấm Duyệt ở popup khi ô trống."], "—", ["- Duyệt thành công; không có dòng “Ghi chú PTKD”."]),
    T(3, "PTKD từ chối", "P0", [ACC_P, "Phiếu PYCHG-G Chờ PTKD duyệt có H1 (Chờ tính giá bán) và SULI-0-1000 (Đang KD)."],
      ["1. Bấm Từ chối.", "2. Nhập lý do “Thiếu model”, bấm Từ chối."], "—",
      ["- “Đã từ chối yêu cầu hỏi giá”; phiếu Không duyệt; H1 về Đang nhập thông tin; SULI-0-1000 vẫn Đang kinh doanh.",
       "- Người lập nhận “[YCHG] Từ chối: PYCHG-G. Lý do: Thiếu model”.", "- Chi tiết: “Ghi chú PTKD: Thiếu model”; lịch sử “PTKD không duyệt”."]),
    T(4, "Từ chối thiếu lý do", "P0", ["Như ca 3."], ["1. Bấm Từ chối ở popup khi ô trống."], "—",
      ["- Chữ đỏ “" + REQ + "” dưới ô, popup không đóng, không gửi."]),
    T(5, "Phiếu Không duyệt biến khỏi danh sách người khác", "P1", ["Sau ca 3; tài khoản S2 không phải người lập."], ["1. S2 tìm PYCHG-G."], "—",
      ["- Không thấy (phiếu Không duyệt chỉ người lập thấy)."]),
    T(6, "PTKD duyệt khi phân công XNK đã bị gỡ", "P0", [ACC_P, "Phiếu PYCHG-H gửi lúc nhóm TELWIN có XNK; sau đó phân công TELWIN tại công ty 1 bị kết thúc."],
      ["1. Duyệt PYCHG-H."], "—",
      ["- Chữ đỏ trong popup “Nhóm TELWIN — Telwin S.p.A chưa có XNK phụ trách tại công ty, chưa duyệt được.”", "- Phiếu vẫn Chờ PTKD duyệt."]),
    T(7, "Duyệt phiếu còn hàng tạm chưa quyết định", "P0", [ACC_P, "PYCHG-D Chờ PTKD duyệt có hàng tạm HT1 trạng thái Hàng tạm."],
      ["1. Rê chuột lên nút Duyệt.", "2. Gọi thẳng chức năng Duyệt bằng công cụ kiểm thử API."], "—",
      ["- Nút Duyệt bị khoá, tooltip “Còn 1 hàng tạm chưa duyệt”; cạnh nút có icon thông tin.", "- Bước 2: hệ thống báo “Còn 1 hàng tạm chưa duyệt”."]),
    T(8, "PTKD Đồng ý hàng tạm", "P1", ["Như ca 7."], ["1. Bấm Duyệt ở dòng HT1.", "2. Bổ sung ô bắt buộc, bấm Đồng ý, xác nhận."], "—",
      ["- Form “Duyệt hàng tạm: HT1”, đầu form “thuộc YCHG PYCHG-D · người lập …”.",
       "- Hỏi “Đồng ý hàng tạm HT1? Hàng chuyển \"Hàng tạm đã duyệt\" và sang \"Chờ tính giá bán\" khi duyệt phiếu PYCHG-D.”",
       "- “Đã đồng ý hàng tạm HT1”; về Chi tiết; HT1 “Hàng tạm đã duyệt”, nút dòng đổi thành Sửa; nút Duyệt phiếu mở khoá."]),
    T(9, "PTKD Không duyệt hàng tạm", "P1", ["Như ca 7."], ["1. Mở form HT1, bấm Không duyệt.", "2. Nhập lý do “Trùng hàng có sẵn”, xác nhận."], "—",
      ["- “Đã không duyệt hàng tạm HT1”.", "- Chi tiết: dòng HT1 mờ, gạch tên, “Không đi tiếp — lý do: Trùng hàng có sẵn”."]),
    T(10, "Duyệt phiếu sau khi quyết định hàng tạm", "P0", ["PYCHG-D: HT1 Đồng ý (nhóm SULI), HT2 Không duyệt (nhóm riêng IPC chỉ có HT2)."],
      ["1. Duyệt PYCHG-D."], "—",
      ["- HT1 sang Chờ tính giá bán; nhóm SULI Chờ XNK duyệt.",
       "- Nhóm IPC đóng Huỷ duyệt lý do “Mọi hàng tạm không được duyệt”; người lập nhận “[YCHG] Hủy: PYCHG-D. Nhóm IPC — …. Lý do: Mọi hàng tạm không được duyệt”."]),
    T(11, "XNK duyệt nhóm", "P0", [ACC_X, "PYCHG-04287 nhóm TORIN Chờ XNK duyệt."],
      ["1. Bấm Duyệt ở dòng nhóm TORIN.", "2. Ghi chú “Đã gửi hãng”, bấm Duyệt."], "—",
      ["- Popup “Duyệt nhóm hàng” “PYCHG-04287 — nhóm TORIN — TORIN (…)”.", "- “Đã duyệt nhóm hàng”; nhóm Chờ lập YCTG; “Ghi chú XNK: Đã gửi hãng”.",
       "- Lịch sử “XNK duyệt” nội dung “Nhóm TORIN — …. Đã gửi hãng”.", "- KHÔNG có thông báo gửi người lập."]),
    T(12, "XNK báo nhóm không có giá", "P0", [ACC_X, "PYCHG-04287 chỉ có 1 nhóm TORIN, Chờ XNK duyệt."],
      ["1. Bấm Không có giá.", "2. Nhập lý do “Hãng ngừng sản xuất”, xác nhận."], "—",
      ["- Popup ghi “… — nhóm sẽ đóng, không gửi lại được”.", "- Nhóm Không có giá, “Lý do: Hãng ngừng sản xuất”; phiếu Không có giá (nhóm cuối đóng, không nhóm nào có giá).",
       "- Người lập nhận “[YCHG] Từ chối: PYCHG-04287. Nhóm TORIN — … không có giá: Hãng ngừng sản xuất”."]),
    T(13, "XNK Huỷ duyệt nhóm chưa có YCTG", "P0", ["Tài khoản Trần Hạnh Minh có " + Q2 + ", phân công BESITA tại công ty 1.", "PYCHG-04282 nhóm BESITA Chờ lập YCTG, chưa có YCTG."],
      ["1. Bấm Huỷ duyệt ở nhóm BESITA.", "2. Lý do “Khách hủy nhu cầu”, xác nhận."], "—",
      ["- “Đã huỷ duyệt nhóm hàng”; nhóm Huỷ duyệt; người lập nhận “[YCHG] Hủy: PYCHG-04282. Nhóm BESITA — …. Lý do: Khách hủy nhu cầu”."]),
    T(14, "Không còn Huỷ duyệt khi nhóm đã có YCTG", "P1", ["Nhóm BESITA đã được lập YCTG."], ["1. Mở Chi tiết PYCHG-04282.", "2. Gọi thẳng chức năng Huỷ duyệt."], "—",
      ["- Không có nút Huỷ duyệt / Lập YCTG; nhãn Đang tính giá.", "- Bước 2: “" + CONFLICT + "”."]),
    T(15, "Lập YCTG từ dòng nhóm", "P0", ["Như ca 13 trước khi huỷ."], ["1. Bấm Lập YCTG ở nhóm BESITA (Chi tiết).", "2. Quay lại; mở danh sách, bung PYCHG-04282, bấm icon Lập YCTG."], "—",
      ["- Cả 2 cách mở màn Tạo YCTG của đúng nhóm BESITA."]),
    T(16, "Đổi phân công XNK khi nhóm đang chờ", "P0", [ACC_X, ACC_X2, "PYCHG-04287 nhóm TORIN Chờ XNK duyệt; đổi phân công TORIN sang X2."],
      ["1. X mở Chi tiết.", "2. X2 mở Chi tiết."], "—",
      ["- X: mất nút Duyệt / Không có giá.", "- X2: có nút; dòng nhóm “XNK tiếp nhận: <X2>”."]),
    T(17, "Phiếu Đã tính giá khi nhóm cuối có giá", "P0", ["Phiếu 2 nhóm: nhóm 1 Không có giá; nhóm 2 vừa được áp giá qua PTG."],
      ["1. Mở danh sách."], "—", ["- Phiếu Đã tính giá; “1/2 nhóm đã tính giá”.", "- Người lập nhận “[YCHG] Đã duyệt: <số phiếu>. Đã tính giá xong 1/2 nhóm”."]),
    T(18, "Thông báo gửi phiếu tới PTKD công ty phiếu", "P0", [ACC_S, ACC_P, "P4 có " + Q1 + " chỉ ở công ty 4."],
      ["1. S gửi phiếu PYCHG-I ở công ty 1."], "—",
      ["- P nhận “[YCHG] Chờ duyệt: PYCHG-I. Người lập: <tên S>”; bấm mở Chi tiết PYCHG-I.", "- P4 KHÔNG nhận."]),
    T(19, "Thông báo khi lỗi gửi không làm hỏng thao tác", "P2", [ACC_P], ["1. Duyệt phiếu khi dịch vụ thông báo đang lỗi."], "—",
      ["- Phiếu vẫn được duyệt đúng; chỉ không có thông báo."]),
    T(20, "PTKD sửa ý hàng tạm trước khi duyệt phiếu", "P2", ["HT1 đã Đồng ý."], ["1. Bấm Sửa ở dòng HT1, bấm Không duyệt với lý do."], "—",
      ["- HT1 chuyển Hàng tạm không duyệt; icon thông tin ở nút Sửa ghi “Mở lại form để đổi quyết định Đồng ý hoặc Không duyệt. Đổi được tới khi bấm Duyệt phiếu.” (nội dung tương đương)."]),
    T(21, "Lưu form hàng tạm đã Đồng ý", "P2", ["HT1 đã Đồng ý."], ["1. Mở form HT1, sửa Ghi chú, bấm Lưu."], "—",
      ["- “Đã lưu — hàng HT1 trở về \"Hàng tạm\" (chờ duyệt lại)”; nút Duyệt phiếu bị khoá lại."]),
    T(22, "Lịch sử đủ các bước", "P1", ["Phiếu đã qua: gửi, PTKD duyệt, XNK duyệt, lập YCTG, tính giá."], ["1. Mở Chi tiết, khối Ghi chú duyệt & lịch sử."], "—",
      ["- Mới đến cũ: Duyệt tính giá, Lập yêu cầu tính giá, XNK duyệt, PTKD duyệt, Lập phiếu yêu cầu hỏi giá; mỗi dòng có người thực hiện + thời gian."]),
]

# ------------------------------------------------------------------ VI GIA BAN
S6 = [
    T(1, "Cột Giá bán lẻ hiện hành", "P0", [ACC_S, "MLER-AMAT8574091 (Bộ) đang có giá Bán lẻ 22,500,000 tại công ty 1."],
      ["1. Mở Chi tiết PYCHG-04283."], "—", ["- Cột Giá bán lẻ hiện hành = 22,500,000 (giá ĐVT cơ bản tại công ty 1)."]),
    T(2, "Giá bán lẻ hiện hành là giá SỐNG, không phải giá lúc lập", "P0", ["Như ca 1; người có quyền Cập nhật giá bán đổi Bán lẻ thành 23,000,000."],
      ["1. Tải lại Chi tiết PYCHG-04283."], "—", ["- Cột hiện 23,000,000; giá bán mới trong Chi tiết kết quả vẫn 22,500,000 (bản chụp lúc áp)."]),
    T(3, "Hàng chưa có giá: ô trống, khác giá 0", "P1", ["Hàng A chưa có dòng giá Bán lẻ; hàng B có Bán lẻ = 0 (vd CH-MN-BINHBOMDAUKHINEN5L)."],
      ["1. Đưa A và B vào phiếu.", "2. In phiếu."], "—", ["- Màn: A để trống, B hiện “0”.", "- Bản in: A hiện “—”, B hiện “0”."]),
    T(4, "Giá bán lẻ theo công ty phiếu", "P0", ["Hàng C có Bán lẻ 1,000,000 ở công ty 1 và 1,200,000 ở công ty 4; S làm ở 2 công ty."],
      ["1. Ở công ty 1 tạo phiếu với C.", "2. Đổi sang công ty 4 tạo phiếu với C."], "—", ["- Công ty 1 hiện 1,000,000; công ty 4 hiện 1,200,000."]),
    T(5, "YCHG không ghi giá", "P0", [ACC_S, ACC_P, "SULI-0-1000 Bán lẻ 1 (ghi lại toàn bộ giá trước khi test)."],
      ["1. Gửi phiếu có SULI-0-1000.", "2. PTKD duyệt.", "3. Mở màn Cập nhật giá bán, tìm SULI-0-1000."], "—",
      ["- Giá 6 loại không đổi; không có nhãn Chờ duyệt."]),
    T(6, "Hàng đang KD trong YCHG vẫn sửa giá được", "P0", ["SULI-0-1000 nằm trong phiếu Đang hỏi giá, nhóm chưa có PTG."],
      ["1. Ở màn Cập nhật giá bán sửa Bán lẻ SULI-0-1000 rồi Lưu."], "—", ["- Lưu được (chỉ bị chặn khi giá đang chờ duyệt ở Phiếu tính giá)."]),
    T(7, "Trạng thái hàng mới theo luồng", "P0", ["H1 Đang nhập thông tin."],
      ["1. Gửi phiếu có H1.", "2. XNK duyệt, lập YCTG, KTMH lưu PTG.", "3. PTG được áp giá cho mọi ĐVT của H1."], "—",
      ["- Sau bước 1: Chờ tính giá bán.", "- Sau bước 2: Đang tính giá.", "- Sau bước 3: Đang kinh doanh; H1 có mặt ở màn Hàng đang kinh doanh."]),
    T(8, "Hàng mới về Đang nhập thông tin khi nhóm đóng", "P0", ["H1 Chờ tính giá bán trong nhóm SULI của phiếu Đang hỏi giá."],
      ["1. XNK SULI bấm Không có giá với lý do."], "—", ["- H1 về Đang nhập thông tin; lập YCHG mới cho H1 được ngay."]),
    T(9, "Hàng mới đang hỏi giá không vào phiếu khác", "P0", ["H1 Chờ tính giá bán trong PYCHG-J."],
      ["1. Mở Chọn hàng hoá ở phiếu mới, tìm H1.", "2. Gọi thẳng chức năng Lưu nháp với H1."], "—",
      ["- Bước 1: H1 không có trong popup.", "- Bước 2: lỗi dưới hàng “H1: Hàng đang được hỏi giá ở PYCHG-J”."]),
    T(10, "Chi tiết kết quả: hiện giá bán mới", "P0", [ACC_S, "PYCHG-04283 nhóm MULLER đã áp giá qua PTG-03178."],
      ["1. Mở Chi tiết PYCHG-04283.", "2. Bấm Chi tiết kết quả."], "—",
      ["- Dưới MLER-AMAT8574091: dòng ĐVT Bộ, Bán lẻ / Theo lô / Đại lý cấp 1 / 2 / 3 = 22,500,000 kèm “ĐMGG 5%”; TMĐT = 29,250,000 kèm “ĐMGG 0%”.",
       "- Nút đổi thành “Ẩn chi tiết kết quả”."]),
    T(11, "TMĐT trong kết quả theo hệ số công ty", "P1", ["Như ca 10; hệ số TMĐT của công ty 1 = 1.3."], ["1. So TMĐT với Bán lẻ."], "—",
      ["- 29,250,000 = 22,500,000 × 1.3."]),
    T(12, "Kết quả chỉ có giá bán", "P0", [ACC_S + " (không có " + Q4 + ")."], ["1. Bật Chi tiết kết quả PYCHG-04283.", "2. In kết quả."], "—",
      ["- Xem và in được.", "- KHÔNG có giá NCC, tỉ giá, chi phí, giá nhập kho, giá vốn ở cả màn và bản in."]),
    T(13, "Ẩn / hiện giá mới từng hàng", "P2", ["Như ca 10."], ["1. Bấm nút X ở bảng giá của MLER-AMAT8574091.", "2. Bấm “Hiện giá mới”."], "—",
      ["- Bước 1: bảng ẩn, dưới cột Giá bán lẻ hiện hành có link “Hiện giá mới”.", "- Bước 2: bảng hiện lại."]),
    T(14, "Không có nút Chi tiết kết quả khi chưa nhóm nào có giá", "P1", [ACC_S], ["1. Mở Chi tiết PYCHG-04287."], "—", ["- Không có nút Chi tiết kết quả."]),
    T(15, "Thông báo giá đã áp mở sẵn kết quả", "P0", ["Người lập YCHG có nhóm vừa được áp giá."],
      ["1. Bấm thông báo “[YCHG] Đã duyệt: <số phiếu>. Nhóm …: đã có giá bán mới”."], "—",
      ["- Mở Chi tiết, nhóm tô nền xanh, Chi tiết kết quả đã bật sẵn."]),
    T(16, "Kết quả chỉ sinh khi giá được duyệt", "P0", ["Công ty 1 bật duyệt giá; PTG của nhóm đã Lưu & duyệt, giá đang Chờ duyệt ở màn Duyệt giá bán."],
      ["1. Mở Chi tiết YCHG."], "—", ["- Nhóm vẫn Đang tính giá, chưa có dòng “Giá bán mới áp ngày …”.", "- Sau khi mọi dòng được Duyệt ở màn Duyệt giá bán: có kết quả, nhóm Đã tính giá."]),
    T(17, "Mọi ĐVT có dòng giá mới", "P1", ["Hàng D có 2 ĐVT Cái và Hộp, đã áp giá cả 2."], ["1. Bật Chi tiết kết quả."], "—",
      ["- Bảng giá của D có 2 dòng Cái, Hộp; cột ĐVT ở phiếu ghi “Cái · Hộp”."]),
    T(18, "Giá chỉ áp cho công ty phiếu", "P0", ["Hàng C kinh doanh ở công ty 1 và 4; PTG của YCHG công ty 1 đã áp giá."],
      ["1. Ở công ty 4 mở màn Cập nhật giá bán, tìm C."], "—", ["- Giá công ty 4 không đổi."]),
]

# ------------------------------------------------------------------ VII
S7 = [
    T(1, "In phiếu từ danh sách", "P1", [ACC_S], ["1. Bấm In ở dòng PYCHG-04283."], "—",
      ["- Popup “Xem trước yêu cầu hỏi giá PYCHG-04283”: “PHIẾU YÊU CẦU HỎI GIÁ”, Số phiếu, Ngày tạo 14/09/2026, Người lập, Trạng thái Đã tính giá.",
       "- Bảng: dòng nhóm “I MULLER — MULLER AUTOMOTIVE SÂS · XNK: … · Đã tính giá”; hàng MLER-AMAT8574091, Bộ, 22,500,000.",
       "- Khối ký Người lập / PTKD duyệt; letterhead công ty 1."]),
    T(2, "In từ chân màn Chi tiết", "P2", [ACC_S], ["1. Mở Chi tiết PYCHG-04280, bấm In."], "—", ["- Cùng bản in như ca 1 cho PYCHG-04280."]),
    T(3, "In kết quả", "P0", [ACC_S], ["1. Mở Chi tiết PYCHG-04283, bấm In kết quả."], "—",
      ["- Popup “Xem trước kết quả tính giá PTG-03178”: “KẾT QUẢ TÍNH GIÁ”, PTG-03178, PYCTG-03162, PYCHG-04283, MULLER — MULLER AUTOMOTIVE SÂS, Người hỏi giá Đặng Tiến Mạnh, Ngày áp giá 14/09/2026.",
       "- 6 dòng loại giá cho ĐVT Bộ (Bán lẻ … Thương mại điện tử 29,250,000, ĐMGG 0)."]),
    T(4, "In phiếu nháp của người khác", "P1", [ACC_S, "S2 có phiếu Đang tạo PYCHG-A."], ["1. Gọi thẳng chức năng In PYCHG-A."], "—", ["- “" + NOTFOUND + "”."]),
    T(5, "In trong popup", "P2", [ACC_S], ["1. Mở popup xem trước, bấm In."], "—", ["- Mở hộp thoại in của trình duyệt; bản in đúng như xem trước."]),
]

# ------------------------------------------------------------------ VIII
S8 = [
    T(1, "Lưu khi chưa có hàng", "P0", [ACC_S], ["1. Form Tạo trống, bấm Lưu nháp.", "2. Bấm Lưu và gửi duyệt."], "—",
      ["- Cả 2: “" + NO_ROW + "”, không gửi gì."]),
    T(2, "Ghi chú 255 / 256 ký tự", "P1", [ACC_S], ["1. Nhập ghi chú 255 ký tự, Lưu nháp.", "2. Nhập 256 ký tự."], "—",
      ["- Bước 1: lưu được.", "- Bước 2: “Vui lòng nhập tối đa 255 ký tự.” ngay khi gõ; bấm Lưu không gửi."]),
    T(3, "Báo đồng thời mọi lỗi", "P0", [ACC_S], ["1. Ghi chú 256 ký tự, có nhóm FOFEN thiếu XNK, bấm Lưu và gửi duyệt."], "—",
      ["- Cùng lúc: lỗi Ghi chú + lỗi nhóm FOFEN; cuộn tới lỗi đầu tiên."]),
    T(4, "Ghi chú PTKD 256 ký tự", "P1", [ACC_P], ["1. Popup Duyệt, nhập 256 ký tự."], "—", ["- “Vui lòng nhập tối đa 255 ký tự.”, không gửi."]),
    T(5, "Lý do từ chối 256 ký tự", "P1", [ACC_P], ["1. Popup Từ chối, nhập 256 ký tự."], "—", ["- “Vui lòng nhập tối đa 255 ký tự.”"]),
    T(6, "Lý do Không có giá / Huỷ duyệt 1000 / 1001 ký tự", "P1", [ACC_X], ["1. Lý do 1000 ký tự.", "2. Lý do 1001 ký tự."], "—",
      ["- 1000: gửi được.", "- 1001: “Vui lòng nhập tối đa 1000 ký tự.”"]),
    T(7, "Lý do chỉ có dấu cách", "P1", [ACC_P], ["1. Popup Từ chối, nhập “   ”, bấm Từ chối."], "—", ["- Hệ thống báo “" + REQ + "” (cắt khoảng trắng)."]),
    T(8, "Lý do Không duyệt hàng tạm", "P2", [ACC_P], ["1. Popup Không duyệt hàng tạm để trống.", "2. Nhập 256 ký tự."], "—",
      ["- “" + REQ + "”; “Vui lòng nhập tối đa 255 ký tự.”"]),
    T(9, "Bỏ qua giao diện: gửi hàng ngừng kinh doanh", "P1", [ACC_S, "Hàng N Ngừng kinh doanh tại công ty 1."],
      ["1. Gọi thẳng chức năng Lưu nháp với N."], "—", ["- Lỗi “N: Hàng ngừng kinh doanh tại công ty”; không lưu."]),
    T(10, "Bỏ qua giao diện: hàng không tồn tại", "P2", [ACC_S], ["1. Gọi thẳng Lưu nháp với 1 mã hàng không tồn tại."], "—", ["- Lỗi “Không tồn tại” ở hàng đó."]),
    T(11, "Bỏ qua giao diện: gửi nhóm thiếu XNK", "P0", [ACC_S], ["1. Gọi thẳng Lưu và gửi duyệt với FOFE-FCS-300."], "—",
      ["- “" + NO_XNK_FOFEN + "”; không lưu, không đổi trạng thái hàng."]),
    T(12, "Bỏ qua giao diện: hàng tạm đã duyệt", "P2", ["Hàng tạm HT1 Hàng tạm đã duyệt trong phiếu Chờ PTKD duyệt khác."],
      ["1. Gọi thẳng Lưu nháp với HT1."], "—", ["- “HT1: Hàng tạm đã được duyệt, đang chờ duyệt phiếu yêu cầu hỏi giá”."]),
]

# ------------------------------------------------------------------ IX
S9 = [
    T(1, "Chỉ thấy phiếu công ty đang làm việc", "P0", ["Tài khoản S làm ở công ty 1 và 4; công ty 4 có PYCHG-04261."],
      ["1. Ở công ty 1 tìm 04261.", "2. Sang công ty 4 tìm 04261."], "—", ["- Công ty 1: không có.", "- Công ty 4: có."]),
    T(2, "Hai PTKD duyệt cùng lúc", "P0", ["P và P' cùng có " + Q1 + "; PYCHG-04280 Chờ PTKD duyệt."],
      ["1. P và P' cùng mở Chi tiết.", "2. P duyệt; P' bấm Từ chối ngay sau."], "—",
      ["- P thành công; P' nhận “" + CONFLICT + "”, màn tải lại thấy Đang hỏi giá.", "- Lịch sử chỉ 1 dòng “PTKD duyệt”."]),
    T(3, "Hai XNK thao tác nhóm cùng lúc", "P1", ["X mở 2 tab Chi tiết PYCHG-04287."], ["1. Tab 1 Duyệt nhóm TORIN.", "2. Tab 2 bấm Không có giá."], "—",
      ["- Tab 2: “" + CONFLICT + "”; nhóm vẫn Chờ lập YCTG."]),
    T(4, "Người lập sửa khi PTKD đang duyệt", "P1", ["Phiếu PYCHG-K Chờ PTKD duyệt; người lập mở màn Sửa từ trước khi gửi ở tab khác."],
      ["1. Người lập bấm Lưu nháp ở tab cũ."], "—", ["- “" + CONFLICT + "”; phiếu vẫn Chờ PTKD duyệt."]),
    T(5, "Hai phiếu gửi cùng hàng mới", "P0", ["S và S2 mỗi người có 1 phiếu nháp chứa H1 (Đang nhập thông tin)."],
      ["1. S và S2 cùng bấm Lưu và gửi duyệt."], "—",
      ["- 1 phiếu gửi được; phiếu còn lại báo “H1: Hàng đang được hỏi giá ở <mã phiếu kia>”."]),
    T(6, "Phiếu công ty khác không nhận thông báo chéo", "P1", ["P4 có " + Q1 + " ở công ty 4."], ["1. Gửi phiếu ở công ty 1."], "—", ["- P4 không nhận thông báo."]),
    T(7, "Lỗi mạng khi duyệt", "P2", [ACC_P], ["1. Ngắt mạng, bấm Duyệt ở popup."], "—",
      ["- Thông báo lỗi, không treo; bật mạng tải lại: phiếu vẫn Chờ PTKD duyệt."]),
    T(8, "Hàng tạm Không duyệt chuyển sang phiếu mới", "P2", ["HT2 Hàng tạm không duyệt nằm lại PYCHG-D (Đang hỏi giá), nhóm IPC chỉ có HT2."],
      ["1. Người lập sửa HT2, đưa vào phiếu mới, Lưu nháp."], "—",
      ["- HT2 về Hàng tạm; bị gỡ khỏi PYCHG-D; nhóm IPC của PYCHG-D đóng Huỷ duyệt “Mọi hàng tạm không được duyệt”."]),
    T(9, "Nhóm đã đóng không mở lại", "P1", ["Nhóm TORIN của PYCHG-04287 Không có giá."], ["1. Tìm cách duyệt / gửi lại nhóm."], "—",
      ["- Không có nút nào; muốn hỏi lại phải lập YCHG mới (TORI-TRW05001 chọn được lại)."]),
]

# ------------------------------------------------------------------ X
S10 = [
    T(1, "Hàng mới: hỏi giá đến khi có giá bán", "P0", [ACC_S, ACC_P, "XNK Đinh Hà Duyên phụ trách SULI; công ty 1 tắt duyệt giá; H1 Đang nhập thông tin."],
      ["1. S tạo YCHG với H1, gửi.", "2. P duyệt.", "3. XNK duyệt nhóm, lập YCTG, gửi.", "4. KTMH tính giá, Lưu & duyệt PTG.", "5. S mở thông báo “[YCHG] Đã duyệt …”."], "—",
      ["- H1 lần lượt: Chờ tính giá bán, Đang tính giá, Đang kinh doanh.", "- Phiếu Đã tính giá; Chi tiết kết quả hiện giá mới mọi ĐVT; Giá bán lẻ hiện hành = giá Bán lẻ mới."]),
    T(2, "Hỏi lại giá hàng đang kinh doanh, có duyệt giá", "P0", ["Công ty 1 bật duyệt giá; SULI-0-1000 Đang KD."],
      ["1. Gửi YCHG, PTKD duyệt, XNK duyệt, lập YCTG, PTG Lưu & duyệt.", "2. Người duyệt giá Duyệt ở màn Duyệt giá bán."], "—",
      ["- Trước bước 2: nhóm Đang tính giá, chưa có kết quả.", "- Sau bước 2: nhóm Đã tính giá, có kết quả; SULI-0-1000 vẫn Đang kinh doanh suốt luồng."]),
    T(3, "Từ chối, sửa, gửi lại, duyệt", "P0", [ACC_S, ACC_P], ["1. S gửi phiếu.", "2. P Từ chối “Thiếu model”.", "3. S sửa, gửi lại.", "4. P Duyệt."], "—",
      ["- Lịch sử đủ: Lập phiếu, PTKD không duyệt, Lập phiếu, PTKD duyệt.", "- Hàng mới về Đang nhập thông tin sau bước 2, sang Chờ tính giá bán sau bước 3."]),
    T(4, "Phiếu 2 nhóm: 1 có giá, 1 không có giá", "P1", ["Phiếu nhóm SULI và TELWIN."], ["1. XNK TELWIN báo Không có giá.", "2. Nhóm SULI được áp giá."], "—",
      ["- Sau bước 1: phiếu vẫn Đang hỏi giá.", "- Sau bước 2: phiếu Đã tính giá, “1/2 nhóm đã tính giá”."]),
    T(5, "Hàng tạm từ BOM đến khi được hỏi giá", "P1", ["Dòng tạm HHB000123 trong BOM dự án."],
      ["1. Thêm hàng tạm từ dòng tạm, gửi phiếu.", "2. PTKD Đồng ý hàng tạm, duyệt phiếu."], "—",
      ["- Hàng tạm sang Chờ tính giá bán; dòng BOM gắn mã hàng mới; nhóm tới XNK phụ trách."]),
]


def _norm(tc):
    return tuple(L(*x) if isinstance(x, list) else x for x in tc)


ROLE_TCS = [_norm(tc) for tc in ROLE_TCS]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP (MENU, MÀN HÀNG HOÁ, THÔNG BÁO, LINK)", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, NHÓM, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "CHỨC NĂNG CHÍNH (TẠO / SỬA / XEM / XOÁ, CHỌN HÀNG, HÀNG TẠM)", S4),
    ("V", "THAO TÁC TRẠNG THÁI (PTKD, XNK, HÀNG TẠM, THÔNG BÁO)", S5),
    ("VI", "GIÁ BÁN — GIÁ HIỆN HÀNH, TRẠNG THÁI HÀNG, GIÁ BÁN MỚI", S6),
    ("VII", "IN PHIẾU / IN KẾT QUẢ", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", S8),
    ("IX", "CÔ LẬP DỮ LIỆU THEO CÔNG TY & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "E2E FLOW", S10),
]

_all = "\n".join("\n".join(map(str, x)) for x in DESCRIPTION_BLOCK + ROLE_TCS + [t for _, _, s in SECTIONS for t in s])
_bad = re.findall(r"[←-⯿\U0001F300-\U0001FAFF]", _all)
assert not _bad, "Con ky tu cam: %s" % sorted(set(_bad))

build(output_file=OUT, sheet_name="Trang tính1", feature_name="Yêu cầu hỏi giá",
      module_name="Yêu cầu hỏi giá", description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
print("OK ->", OUT)
