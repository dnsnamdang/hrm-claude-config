# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man "Bao cao theo doi giu hang" (Ban hang > Bao cao > Hang giu).

Chay:  python3 .plans/gop-db/bao-cao-theo-doi-giu-hang/gen_testcase.py
Engine dung chung: .claude/skills/testcase-documenter/assets/tc_engine.py

Nguon su that: design.md (ca 2 bang chot cuoi "Chot vuong mac..." va "Chot sau nghiem thu code"
A-K THANG spec), spec docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md,
code nhanh gop_db va 2 bo e2e e2e/tests/sale/prepick-tracking(.api).spec.ts.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

MODULE = "BC theo dõi giữ hàng"
P_ALL = "Xem báo cáo giữ hàng theo tổng công ty"
MENU = "Vào phân hệ Bán hàng > khối Báo cáo > nhóm \"Hàng giữ\" > bấm \"Báo cáo theo dõi giữ hàng\"."


def L(*lines):
    """Moi y 1 dong that trong o."""
    return "\n".join(lines)


# Bo du lieu chuan dung chung cho nhieu TC (mo ta day du o muc 9)
D1 = "Bộ dữ liệu D1 (mục 9 phần mô tả)."
D1_AN = L(
    D1,
    "Nhân viên An (Phòng KD1, bộ phận Dự án, công ty A) đang giữ 5 mã cho khách Đóng tàu Hạ Long:",
    "HH-01 1,234.5 Mét trong hạn (còn 30 ngày) · HH-02 10 Cái sắp hết hạn (còn 3 ngày) · "
    "HH-03 2 Bộ quá hạn 5 ngày · HH-04 100 Mét trong hạn, đã gia hạn 2 lần · "
    "HH-05 1 Cái trong hạn, theo hợp đồng HĐ-001.",
    "Ngưỡng cảnh báo cấu hình hệ thống = 7 ngày.",
)

# ============================================================== 9 MỤC MÔ TẢ
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     L("Theo dõi hàng ĐANG GIỮ cho khách tại đúng thời điểm xem: ai đang giữ, giữ mặt hàng nào, cho "
       "khách nào, bao nhiêu phần còn trong hạn / sắp hết hạn / đã quá hạn giữ, để kịp xuất hàng, gia "
       "hạn hoặc trả lại tồn.",
       "Đường vào: phân hệ Bán hàng > khối Báo cáo > nhóm \"Hàng giữ\" > \"Báo cáo theo dõi giữ hàng\".",
       "Đây là màn MỚI, chạy song song với màn cũ \"Danh sách hàng giữ\" (Tài chính) — màn cũ và màn "
       "\"Hàng sắp hết hạn giữ\" giữ nguyên, không đổi hành vi.",
       "Báo cáo CHỈ ĐỌC; hai nút Gia hạn / Huỷ giữ chỉ mở màn lập phiếu tương ứng, không tự ghi gì.")),

    ("2. Đối tượng được tính / hiển thị",
     L("Một dòng hàng giữ được đưa vào báo cáo khi thoả ĐỦ:",
       "- Số lượng còn giữ lớn hơn 0 (chưa xuất / chưa huỷ hết).",
       "- Thuộc công ty trong phạm vi được xem (xem mục 7).",
       "- Khớp các ô lọc đang chọn.",
       "Cả 2 hình thức giữ đều được tính, và cả 2 đều có khách hàng:",
       "- \"Giữ theo hợp đồng\": phiếu yêu cầu giữ có gắn hợp đồng.",
       "- \"Không theo hợp đồng\": giữ cho khách nhưng chưa gắn hợp đồng.",
       "Hàng giữ sinh ra từ cả 3 loại chứng từ gốc: Phiếu xuất giữ · Nhập hàng cho khách · Điều chuyển giữ "
       "(lập trên hệ thống mới hoặc trên ERP cũ đều tính như nhau).",
       "Mỗi dòng rơi vào ĐÚNG 1 trong 3 trạng thái hạn (chia hết tổng):",
       "- \"Trong hạn\": hạn giữ còn xa hơn hôm nay + N ngày cảnh báo.",
       "- \"Sắp hết hạn\": hạn giữ từ hôm nay tới hôm nay + N (gồm cả 2 đầu mút).",
       "- \"Hết hạn\": hạn giữ đã qua (trước hôm nay).")),

    ("3. Đối tượng bị ẩn / không tính",
     L("- Hàng giữ đã xuất hết hoặc đã huỷ hết (số lượng còn giữ = 0) — kể cả phần dòng cũ đã chuyển "
       "hết sang hạn mới khi gia hạn.",
       "- Hàng giữ của công ty khác khi người xem KHÔNG có quyền \"" + P_ALL + "\".",
       "- Hàng giữ không khớp bộ lọc (phòng ban, bộ phận, nhân viên, khách hàng, thương hiệu, model, "
       "trạng thái hạn, hình thức giữ, từ khoá hàng hoá).",
       "- Báo cáo KHÔNG có cột/ô Kho: hàng giữ không gắn kho, không gắn lô nhập, không có số lô.",
       "- Báo cáo KHÔNG hiện \"Còn phải thu\" của hợp đồng (chỉ gom tiền đã thanh toán, chưa phải công nợ).")),

    ("4. Bộ lọc thời gian áp dụng cho",
     L("KHÔNG có bộ lọc kỳ: số liệu là ảnh chụp tồn giữ HIỆN TẠI (tiêu đề dải tổng hợp ghi "
       "\"Tồn hàng giữ tại dd/mm/yyyy\" = ngày hôm nay).",
       "Mốc duy nhất liên quan thời gian là ô \"Cảnh báo trước (ngày)\" (N, số nguyên 0 – 365):",
       "- Để trống = theo cấu hình hệ thống (đang là 7 ngày, hiện mờ trong ô).",
       "- N chỉ đổi cách chia Trong hạn / Sắp hết hạn của báo cáo, KHÔNG ghi đè cấu hình chung "
       "(màn lập phiếu gia hạn vẫn dùng ngưỡng hệ thống).",
       "- So theo NGÀY (không theo giờ): hạn giữ = hôm nay là \"Sắp hết hạn\", ghi \"hết hạn hôm nay\".")),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     L("Ô \"Tiêu chí theo dõi\" (bắt buộc, chọn 1):",
       "- Theo nhân viên (mặc định): Phòng ban > Nhân viên > Hàng hoá. Cấp bung mặc định \"Đến Nhân viên\".",
       "- Theo hàng hoá: Hàng hoá > Nhân viên. Cấp bung mặc định \"Chỉ Hàng hoá\".",
       "Ô chọn cấp bung nằm trên tiêu đề cột \"Nội dung theo dõi\": Chỉ <cấp 1> / Đến <cấp 2> / "
       "Tất cả cấp (đến <cấp cuối>). Cấp cuối tải khi bung (có biểu tượng đang tải trên dòng).",
       "Bộ phận chỉ là Ô LỌC, không phải một cấp của cây.",
       "Cột bảng: STT · Nội dung theo dõi · Đơn vị · Model · Thương hiệu · Tồn hiện tại · Số lượng giữ · "
       "Trong hạn · Sắp hết hạn · Hết hạn. Cột Đơn vị / Model / Thương hiệu (và Tồn hiện tại) tự ẩn khi "
       "bảng chưa hiện dòng hàng hoá nào; Tồn hiện tại CHỈ có ở tiêu chí Theo hàng hoá.",
       "STT: cấp 1 \"1, 2, 3…\" chạy tiếp qua các trang; cấp 2 \"1.1\"; cấp 3 \"1.1.1\". Dòng đầu bảng là "
       "dòng TỔNG.",
       "3 cửa sổ (popup): Chi tiết hàng giữ (bấm mọi con số) > Lịch sử gia hạn (bấm cột Số lần gia hạn) / "
       "Chứng từ thanh toán (bấm cột Tổng thanh toán).")),

    ("6. Quy tắc cộng dồn / deduplicate",
     L("1 YÊU CẦU GIỮ = Phiếu giữ gốc + Mã hàng + Nhân viên. Một phiếu của nhân viên A xin giữ 5 mã = 5 "
       "yêu cầu giữ (KHÔNG phải 1).",
       "Phiếu giữ gốc phải LẦN NGƯỢC qua mọi lần gia hạn: gia hạn tạo dòng mới với hạn mới, nhưng cột "
       "\"Phiếu giữ gốc\" vẫn ghi phiếu xuất giữ / nhập hàng cho khách / điều chuyển giữ ban đầu, KHÔNG "
       "ghi mã phiếu gia hạn. Gia hạn một phần số lượng sinh 2 dòng nhưng vẫn là 1 yêu cầu giữ.",
       "Đo theo DÒNG, không theo cấp:",
       "- Dòng gom ĐÚNG 1 mã hàng: đo bằng SỐ LƯỢNG (đơn vị cơ bản), 3 cột hạn chia hết cột Số lượng giữ.",
       "- Dòng gom NHIỀU mã: đo bằng SỐ MÃ HÀNG, ghi kèm chữ \"Mã\"; 3 cột hạn đếm CHỒNG LẤN (1 mã vừa "
       "có phần trong hạn vừa có phần quá hạn được đếm ở cả 2 cột) nên tổng 3 cột có thể LỚN HƠN cột Số "
       "lượng giữ.",
       "- Theo nhân viên: TỔNG / Phòng ban / Nhân viên = số mã, Hàng hoá = số lượng. Theo hàng hoá: TỔNG "
       "= số mã, Hàng hoá và Nhân viên (nằm dưới 1 mã) = số lượng. Lọc còn đúng 1 mã thì dòng TỔNG cũng "
       "ra số lượng.",
       "Khối \"Phạm vi đang giữ\" đếm KHÁC NHAU (nhân viên / mã hàng / khách) nên không cộng dồn giữa các "
       "cấp. \"Yêu cầu sắp hết hạn\" và \"Yêu cầu đã hết hạn\" CHỒNG LẤN, không cộng lại thành tổng.")),

    ("7. Phân quyền cấp",
     L("Màn KHÔNG chặn vào: MỌI người đăng nhập đều mở được báo cáo (không cần quyền \"Quản lý giữ hàng\" "
       "của màn cũ).",
       "Báo cáo dùng ĐÚNG 1 quyền: \"" + P_ALL + "\" — quyền này chỉ quyết định PHẠM VI CÔNG TY:",
       "- CÓ quyền: hiện ô chọn \"Công ty\", có thêm mục \"Tất cả công ty\"; xem được công ty bất kỳ.",
       "- KHÔNG quyền: ô Công ty thay bằng nhãn tĩnh ghi tên công ty trong hồ sơ nhân sự; chỉ xem được "
       "hàng giữ của công ty đó; sửa đường dẫn hay gọi thẳng chức năng kèm công ty khác cũng bị bỏ qua.",
       "- Không giới hạn phòng ban: người không quyền vẫn xem TOÀN BỘ hàng giữ của công ty mình.",
       "- Super admin KHÔNG có ngoại lệ: không được gán quyền trên thì cũng chỉ xem công ty mình.",
       "Không dùng 3 quyền \"Xem phiếu hàng giữ theo tổng công ty / theo công ty / theo phòng ban\" của "
       "màn phiếu. Quyền mới KHÔNG gán sẵn cho vai trò nào — quản trị tự gán.")),

    ("8. Cách tính các ô thống kê",
     L("Mọi ô của dải tổng hợp và dòng TỔNG tính trên TOÀN BỘ dữ liệu đã lọc, KHÔNG theo trang đang xem.",
       "Khối \"Phạm vi đang giữ\" (meta: N yêu cầu giữ):",
       "- Nhân viên đang giữ = số nhân viên khác nhau còn hàng giữ (đơn vị \"người\").",
       "- Hàng hoá bị giữ = số mã hàng khác nhau còn hàng giữ (\"mã hàng\").",
       "- Khách hàng = số khách khác nhau đang được giữ hàng (\"khách\").",
       "Khối \"Tình trạng theo yêu cầu giữ\" (meta: N yêu cầu · quá hạn x%):",
       "- Tổng yêu cầu đang giữ hàng = số yêu cầu giữ (mục 6); dòng phụ \"N mã hàng\".",
       "- Yêu cầu sắp hết hạn = số yêu cầu có ÍT NHẤT 1 phần hàng sắp hết hạn; dòng phụ = tỉ lệ trên tổng.",
       "- Yêu cầu đã hết hạn = số yêu cầu có ÍT NHẤT 1 phần hàng quá hạn; dòng phụ = tỉ lệ trên tổng.",
       "- NV có hàng giữ quá hạn = số nhân viên có ít nhất 1 phần hàng quá hạn; dòng phụ \"trên N người\".",
       "Tỉ lệ làm tròn 1 chữ số thập phân; mẫu số 0 thì ghi \"—\".",
       "Bấm số nào cũng mở popup chi tiết; dòng đếm của popup (\"… yêu cầu giữ\") PHẢI bằng đúng con số vừa "
       "bấm. Khối 1 bấm ra danh sách toàn bộ hàng giữ.",
       "Tồn hiện tại = tổng tồn trong các kho đang hoạt động của công ty đang lọc; \"Tất cả công ty\" = "
       "cộng tồn mọi công ty.",
       "Tổng thanh toán (popup) = tổng phát sinh CÓ tài khoản 1311 gắn với hợp đồng, từ 3 loại chứng từ: "
       "Phiếu thu · Phiếu báo có · Phiếu kế toán (quy ra VND). KHÔNG trừ phát sinh Nợ.")),

    ("9. Ghi chú đọc bảng",
     L("Định dạng số chuẩn quốc tế: dấu phẩy ngăn nghìn, dấu chấm thập phân (1,234.5), tối đa 2 số lẻ, "
       "không làm tròn về số nguyên. Ngày dd/mm/yyyy. Báo cáo luôn quy về ĐƠN VỊ CƠ BẢN, không đổi được "
       "đơn vị tính.",
       "Phân trang bảng chính theo NHÓM CẤP 1 (mỗi trang N phòng ban / N hàng hoá kèm toàn bộ cấp con), "
       "mặc định 25, chọn 10/25/50/100, dòng đếm \"Hiển thị a–b / N nhóm\". Popup chi tiết phân trang theo "
       "dòng, mặc định 20, chọn 20/50/100. Popup lịch sử gia hạn và chứng từ thanh toán không phân trang.",
       "Thứ tự mặc định: bảng chính = nhóm có nhiều hàng quá hạn nhất lên trước; popup = hạn giữ tăng dần "
       "(quá hạn lâu nhất lên đầu); chứng từ thanh toán = mới nhất lên đầu; lịch sử gia hạn = cũ nhất lên đầu.",
       "BẪY dễ sai: (1) cộng tay 3 cột hạn ở dòng nhiều mã rồi tưởng số sai; (2) đếm \"yêu cầu giữ\" theo số "
       "phiếu; (3) đọc cột Phiếu giữ gốc ra mã phiếu gia hạn; (4) bản in chỉ ra trang đang xem; (5) chữ "
       "trong ô bảng để chữ thường, không in đậm.",
       "Nhóm test \"gọi thẳng chức năng bằng công cụ kiểm thử API\" dành cho tester kỹ thuật.",
       "BỘ DỮ LIỆU D1 (dùng ở nhiều TC; hôm nay = ngày chạy test; ngưỡng hệ thống 7 ngày):",
       "- Công ty A: Phòng KD1 có 2 bộ phận \"Dự án\" và \"Thương mại\", còn nhân viên chưa phân bộ phận. "
       "Phòng KD2 chưa chia bộ phận; Giang (KD2) giữ 2 mã HH-20, HH-21 trong hạn cho khách Xây dựng Hà Nội.",
       "- An (KD1, bộ phận Dự án) giữ cho khách Đóng tàu Hạ Long: HH-01 Ống thủy lực 1,234.5 Mét hạn "
       "hôm nay+30 · HH-02 Van bi 10 Cái hạn hôm nay+3 · HH-03 Bơm 2 Bộ hạn hôm nay-5 · HH-04 Dây cáp "
       "100 Mét hạn hôm nay+20 (từ phiếu PXG-02, đã gia hạn 2 lần bằng GH-1 rồi GH-2) · HH-05 Máy nén "
       "1 Cái hạn hôm nay+40, theo hợp đồng HĐ-001 (giá trị sau thuế 200,000,000; đã có Phiếu thu PT-01 "
       "50,000,000 và Phiếu báo có BC-01 20,000,000).",
       "- Bình (KD1, chưa phân bộ phận) giữ cho khách Cơ khí Hải Phòng: HH-01 20 Mét hạn hôm nay-2 · "
       "HH-06 Cáp điện 5 Cuộn hạn hôm nay-10 · HH-07 Ống nhựa 3 Cây hạn hôm nay+60.",
       "- Tổng công ty A = 10 yêu cầu giữ (KD1: 8, KD2: 2). Công ty B: Cường giữ 4 mã (4 yêu cầu giữ), tất cả trong hạn.",
       "- Tài khoản: QL (công ty A, được gán quyền \"" + P_ALL + "\"); An (không quyền nào); "
       "SA (Super admin, KHÔNG được gán quyền trên).")),
]

# ============================================================== PHÂN QUYỀN
ROLE_TCS = [
    ("01", "Có quyền xem tổng công ty: ô Công ty là ô chọn, có \"Tất cả công ty\"", "P0",
     L(D1, "Tài khoản QL thuộc công ty A, chỉ được gán quyền \"" + P_ALL + "\" (không phải Super admin)."),
     L("1. Đăng nhập tài khoản QL.", "2. " + MENU, "3. Quan sát ô Công ty trên thanh lọc.",
       "4. Mở ô Công ty, chọn \"Tất cả công ty\"."),
     "Công ty: Tất cả công ty",
     L("- Ô Công ty là ô chọn, mặc định là công ty A (công ty trong hồ sơ của QL).",
       "- Danh sách chọn có mục \"Tất cả công ty\" ở đầu, kèm công ty A và công ty B.",
       "- Chọn \"Tất cả công ty\": báo cáo tải lại, ô \"Tổng yêu cầu đang giữ hàng\" = 10 (công ty A) + 4 "
       "(công ty B) = 14.",
       "- Ô Phòng ban liệt kê phòng ban của cả 2 công ty.")),

    ("02", "\"Tất cả công ty\" bằng đúng tổng từng công ty cộng lại", "P0",
     L(D1, "Tài khoản QL có quyền \"" + P_ALL + "\"."),
     L("1. Đăng nhập QL, mở báo cáo.", "2. Chọn Công ty = công ty A, ghi lại 7 ô của dải tổng hợp.",
       "3. Chọn Công ty = công ty B, ghi lại 7 ô.", "4. Chọn Công ty = Tất cả công ty, đọc lại 7 ô."),
     L("Công ty: công ty A", "Công ty: công ty B", "Công ty: Tất cả công ty"),
     L("- \"Tổng yêu cầu đang giữ hàng\": A = 10, B = 4, Tất cả = 14.",
       "- Mỗi ô đếm theo số lần giữ (Tổng yêu cầu, Yêu cầu đã hết hạn…) của \"Tất cả công ty\" bằng tổng 2 "
       "công ty.",
       "- Lưu ý: \"Nhân viên đang giữ\", \"Hàng hoá bị giữ\", \"Khách hàng\" là đếm khác nhau — một mã giữ ở "
       "cả 2 công ty chỉ tính 1 lần, nên có thể NHỎ HƠN tổng 2 công ty.")),

    ("03", "KHÔNG quyền: ô Công ty thay bằng nhãn tĩnh, chỉ xem công ty mình", "P0",
     L(D1, "Tài khoản An (công ty A) không được gán quyền nào."),
     L("1. Đăng nhập An.", "2. " + MENU, "3. Quan sát vị trí ô Công ty.", "4. Đọc dải tổng hợp."),
     "—",
     L("- Màn mở bình thường (không báo thiếu quyền).",
       "- Vị trí ô Công ty là nhãn tĩnh nền xám ghi \"công ty A\", KHÔNG bấm chọn được, không có \"Tất cả "
       "công ty\".",
       "- \"Tổng yêu cầu đang giữ hàng\" = 10 (chỉ công ty A), không lẫn 4 yêu cầu của công ty B.",
       "- An thấy cả hàng giữ của Bình (cùng công ty) — quyền KHÔNG bó theo phòng ban hay \"của tôi\".")),

    ("04", "KHÔNG quyền sửa đường dẫn để xem công ty khác vẫn chỉ ra công ty mình", "P0",
     L(D1, "Tài khoản An không quyền.", "Biết mã số nội bộ của công ty B."),
     L("1. Đăng nhập An, mở báo cáo.",
       "2. Thêm vào cuối thanh địa chỉ điều kiện công ty = công ty B, rồi Enter.",
       "3. Làm lại với điều kiện công ty = tất cả.",
       "4. Đọc nhãn Công ty và dải tổng hợp."),
     L("Công ty: công ty B", "Công ty: tất cả"),
     L("- Hệ thống bỏ qua điều kiện tự thêm, không lỗi, không treo trang.",
       "- Nhãn vẫn ghi \"công ty A\"; \"Tổng yêu cầu đang giữ hàng\" vẫn = 10.",
       "- KHÔNG có dòng nào của Cường (công ty B) trong bảng.")),

    ("05", "KHÔNG quyền gọi thẳng chức năng báo cáo kèm công ty khác bị ép về công ty mình", "P0",
     L(D1, "Tài khoản An không quyền.", "Tester kỹ thuật có công cụ kiểm thử API, dùng phiên đăng nhập của An."),
     L("1. Gọi thẳng chức năng xem báo cáo kèm công ty = công ty B.",
       "2. Gọi lại kèm công ty = tất cả, rồi bỏ trống công ty.",
       "3. Gọi thẳng chức năng danh sách chi tiết (popup) kèm công ty = công ty B.",
       "4. Gọi thẳng danh mục ô lọc kèm công ty = công ty B."),
     L("Công ty: công ty B", "Công ty: tất cả", "Công ty: (trống)"),
     L("- Cả 3 lần gọi báo cáo đều trả về số liệu y hệt nhau = công ty A (10 yêu cầu giữ).",
       "- Danh sách chi tiết chỉ có dòng của công ty A.",
       "- Danh mục ô lọc báo người này KHÔNG có quyền xem tổng công ty, danh sách công ty chỉ có công ty A.",
       "- Chốt chặn nằm ở hệ thống, không phụ thuộc giao diện có ẩn ô hay không.")),

    ("06", "Super admin KHÔNG được gán quyền = như nhân viên không quyền", "P0",
     L(D1, "Tài khoản SA có vai trò Super admin, công ty A, KHÔNG được gán quyền \"" + P_ALL + "\"."),
     L("1. Đăng nhập SA.", "2. " + MENU, "3. Quan sát ô Công ty.",
       "4. Dùng công cụ kiểm thử API gọi báo cáo kèm công ty = tất cả."),
     "Công ty: tất cả",
     L("- Ô Công ty là nhãn tĩnh \"công ty A\", không có \"Tất cả công ty\".",
       "- Gọi thẳng kèm \"tất cả\" vẫn chỉ ra số của công ty A (10 yêu cầu giữ).",
       "- Lưu ý: KHÔNG có ngoại lệ Super admin — chỉ xét quyền được gán (chốt 03/10/2026).")),

    ("07", "Super admin ĐƯỢC gán quyền thì xem được tất cả công ty", "P1",
     L(D1, "Gán thêm quyền \"" + P_ALL + "\" cho tài khoản SA; SA đăng xuất rồi đăng nhập lại."),
     L("1. Đăng nhập SA.", "2. Mở báo cáo.", "3. Mở ô Công ty, chọn \"Tất cả công ty\"."),
     "Công ty: Tất cả công ty",
     L("- Ô Công ty là ô chọn, có \"Tất cả công ty\".",
       "- \"Tổng yêu cầu đang giữ hàng\" = 14.")),

    ("08", "Mọi người đăng nhập đều vào được màn, kể cả không có quyền nào", "P0",
     L("Tài khoản Dũng là nhân viên công ty A, không có vai trò và không có quyền nào, không giữ hàng.",
       D1),
     L("1. Đăng nhập Dũng.", "2. Vào phân hệ Bán hàng > khối Báo cáo, tìm nhóm \"Hàng giữ\".",
       "3. Bấm \"Báo cáo theo dõi giữ hàng\"."),
     "—",
     L("- Nhóm \"Hàng giữ\" và mục \"Báo cáo theo dõi giữ hàng\" CÓ hiện trong menu.",
       "- Màn mở, không bị đá ra trang lỗi, không có thông báo không có quyền.",
       "- Thấy toàn bộ hàng giữ của công ty A (10 yêu cầu giữ), không phải bảng rỗng.")),

    ("09", "Chưa đăng nhập không mở được báo cáo", "P1",
     "Trình duyệt chưa đăng nhập (hoặc phiên đã hết hạn).",
     L("1. Dán thẳng đường dẫn màn Báo cáo theo dõi giữ hàng vào trình duyệt.",
       "2. Dùng công cụ kiểm thử API gọi các chức năng: xem báo cáo, danh mục lọc, bung cấp con, danh sách "
       "chi tiết, lịch sử gia hạn, chứng từ thanh toán, in, xuất Excel — không kèm phiên đăng nhập."),
     "—",
     L("- Trình duyệt chuyển về màn đăng nhập.",
       "- Cả 8 chức năng đều bị từ chối vì chưa đăng nhập, không trả về dữ liệu.")),

    ("10", "Không quyền xem lịch sử gia hạn của dòng công ty khác bằng cách gọi thẳng", "P0",
     L(D1, "Dòng hàng giữ X của Cường (công ty B) đã gia hạn 1 lần.", "Tài khoản An không quyền."),
     L("1. Dùng công cụ kiểm thử API, phiên của An, gọi chức năng lịch sử gia hạn với dòng X.",
       "2. Gọi lại với một mã dòng không tồn tại.",
       "3. Đăng nhập QL (có quyền), chọn Công ty = công ty B, gọi lịch sử gia hạn của dòng HH-04 (công ty A)."),
     L("Dòng: X (công ty B)", "Dòng: mã không tồn tại", "Dòng: HH-04 khi đang xem công ty B"),
     L("- Cả 3 lần đều bị từ chối với thông báo không tìm thấy dữ liệu, KHÔNG lộ phiếu gia hạn, ngày, người "
       "duyệt của dòng ngoài phạm vi đang xem.",
       "- Gọi đúng dòng HH-04 trong phạm vi công ty A thì ra 2 lần gia hạn.")),

    ("11", "Không quyền xem chứng từ thanh toán của hợp đồng ngoài phạm vi", "P0",
     L(D1, "Hợp đồng HĐ-900 chỉ gắn với hàng giữ của công ty B.", "Tài khoản An không quyền."),
     L("1. Dùng công cụ kiểm thử API, phiên An, gọi chức năng chứng từ thanh toán của HĐ-900.",
       "2. Gọi chức năng đó với HĐ-001 (gắn với dòng HH-05 của An, công ty A)."),
     L("Hợp đồng: HĐ-900", "Hợp đồng: HĐ-001"),
     L("- HĐ-900: bị từ chối, không trả số tiền hay chứng từ nào.",
       "- HĐ-001: trả 2 chứng từ (PT-01, BC-01), đã thanh toán 70,000,000 — người không quyền vẫn xem được "
       "vì hợp đồng gắn với hàng giữ trong công ty mình.")),

    ("12", "Không quyền: bản in và file Excel chỉ chứa công ty mình, không lộ tên công ty khác", "P0",
     L(D1, "Tài khoản An không quyền.", "Khách hàng Thép Miền Nam chỉ có hàng giữ ở công ty B."),
     L("1. Đăng nhập An, bấm \"In danh sách\" > \"In bảng theo dõi\" > In.",
       "2. Đọc dòng \"Bộ lọc đang áp dụng\" và các dòng của bản in.",
       "3. Dùng công cụ kiểm thử API gọi chức năng in kèm công ty = công ty B và khách hàng = Thép Miền Nam.",
       "4. Bấm \"Xuất Excel\" trên thanh tiêu đề."),
     "Khách hàng: Thép Miền Nam (công ty B)",
     L("- Bản in ghi \"Công ty: công ty A\", không có dòng nào của công ty B.",
       "- Gọi thẳng kèm công ty B + khách Thép Miền Nam: bản in vẫn là công ty A, dòng tóm tắt bộ lọc "
       "KHÔNG in tên \"Thép Miền Nam\" (mục khách hàng ngoài phạm vi bị bỏ hẳn).",
       "- File Excel cũng chỉ có dữ liệu công ty A.")),

    ("13", "Không quyền: \"Xóa lọc\" và \"Hàng giữ của tôi\" không mở rộng phạm vi công ty", "P0",
     L(D1, "Tài khoản An không quyền."),
     L("1. Đăng nhập An, chọn Phòng ban = KD1, Trạng thái hạn giữ = Hết hạn.", "2. Bấm \"Xóa lọc\".",
       "3. Bấm \"Hàng giữ của tôi\", rồi bấm lại lần nữa để tắt."),
     L("Phòng ban: KD1", "Trạng thái hạn giữ: Hết hạn"),
     L("- Sau Xóa lọc: nhãn Công ty vẫn \"công ty A\", số liệu vẫn chỉ công ty A (không nhảy sang \"tất cả\").",
       "- Bật / tắt \"Hàng giữ của tôi\": nhãn Công ty không đổi, không lúc nào hiện dữ liệu công ty B.")),

    ("14", "Thu hồi quyền thì lần mở sau mất ô chọn công ty", "P1",
     L(D1, "Tài khoản QL đang có quyền \"" + P_ALL + "\" và đang xem \"Tất cả công ty\"."),
     L("1. Quản trị bỏ quyền \"" + P_ALL + "\" khỏi QL.", "2. QL đăng xuất, đăng nhập lại.",
       "3. Mở lại báo cáo."),
     "—",
     L("- Ô Công ty thành nhãn tĩnh \"công ty A\".",
       "- Số liệu chỉ còn công ty A (10 yêu cầu giữ), không còn giữ lựa chọn \"Tất cả công ty\" cũ.")),

    ("15", "Người có quyền đổi công ty thì các ô lọc đổi theo công ty", "P2",
     L(D1, "Tài khoản QL có quyền."),
     L("1. Đăng nhập QL, chọn Công ty = công ty B.", "2. Mở ô Phòng ban, ô Nhân viên, ô Khách hàng.",
       "3. Đổi lại Công ty = công ty A, mở lại 3 ô đó."),
     L("Công ty: công ty B", "Công ty: công ty A"),
     L("- Ở công ty B: 3 ô chỉ liệt kê phòng ban / nhân viên (Cường) / khách đang có hàng giữ ở công ty B.",
       "- Đổi sang công ty A: Phòng ban, Bộ phận, Nhân viên về \"tất cả\" và danh sách đổi theo công ty A.")),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = [
    (1, "Mở màn từ menu đúng đường bấm", "P0",
     L("Tài khoản An đã đăng nhập.", D1),
     L("1. " + MENU, "2. Quan sát tiêu đề tab trình duyệt, thanh lọc, dải tổng hợp, bảng."),
     "—",
     L("- Tab trình duyệt ghi \"Báo cáo theo dõi giữ hàng\".",
       "- Thanh lọc tiêu đề \"Bộ lọc báo cáo theo dõi giữ hàng\", có nút \"Hàng giữ của tôi\" cạnh tiêu đề.",
       "- Dưới thanh lọc là dải tổng hợp 2 khối rồi tới bảng theo dõi.",
       "- Menu bên trái giữ đúng nhóm Báo cáo của phân hệ Bán hàng, không biến mất khi vào màn.")),

    (2, "Giá trị mặc định khi mở màn", "P0",
     L("Tài khoản An, công ty A.", D1),
     L("1. Mở báo cáo.", "2. Đọc lần lượt từng ô lọc và ô chọn cấp bung."),
     "—",
     L("- Tiêu chí theo dõi = Theo nhân viên.",
       "- Công ty = công ty A (nhãn tĩnh vì An không quyền).",
       "- Phòng ban, Nhân viên, Khách hàng, Thương hiệu, Model, Trạng thái hạn giữ, Hình thức giữ = tất cả "
       "(trống); Tìm hàng hoá trống.",
       "- Bộ phận bị khoá, ghi \"Chọn phòng ban trước\".",
       "- Cảnh báo trước (ngày) trống, hiện mờ số 7 (cấu hình hệ thống).",
       "- Ô cấp bung = \"Đến Nhân viên\"; nút \"Hàng giữ của tôi\" ở trạng thái tắt (nút viền).",
       "- Phân trang 25 nhóm/trang.")),

    (3, "Không có bộ lọc kỳ — tiêu đề dải tổng hợp ghi ngày hôm nay", "P1",
     "Mở báo cáo ngày 03/10/2026.",
     L("1. Mở báo cáo.", "2. Đọc dòng đầu dải tổng hợp.", "3. Tìm ô Từ ngày / Đến ngày / Kỳ trên thanh lọc."),
     "—",
     L("- Dòng đầu: \"Tồn hàng giữ tại 03/10/2026 · N yêu cầu giữ · N nhân viên · N hàng hoá · N khách hàng\".",
       "- Thanh lọc KHÔNG có ô kỳ / ngày nào và KHÔNG có ô Kho.")),

    (4, "Màn cũ \"Danh sách hàng giữ\" vẫn chạy song song, không đổi", "P1",
     "Tài khoản có quyền \"Quản lý giữ hàng\" của màn cũ.",
     L("1. Mở màn cũ Danh sách hàng giữ (Tài chính) từ menu cũ.",
       "2. Mở màn \"Hàng sắp hết hạn giữ\".", "3. Từ ERP bấm liên kết xem hàng giữ theo 1 hàng hoá."),
     "—",
     L("- Màn cũ hiện đúng giao diện và số liệu như trước khi có báo cáo mới.",
       "- \"Hàng sắp hết hạn giữ\" không đổi.",
       "- Liên kết từ ERP vẫn mở màn cũ lọc đúng hàng hoá.")),

    (5, "Đường dẫn kèm điều kiện lạ không làm lỗi màn", "P2",
     "Tài khoản An.",
     L("1. Mở báo cáo, thêm vào cuối đường dẫn các điều kiện lạ (tiêu chí = abc, cấp = 9, trang = -1).",
       "2. Enter."),
     "Tiêu chí: abc · Cấp: 9 · Trang: -1",
     L("- Màn mở với giá trị mặc định (Theo nhân viên, Đến Nhân viên, trang 1).",
       "- Không lỗi trắng trang, không lộ thêm dữ liệu ngoài công ty A.")),

    (6, "Màn hình rộng 1440px và 1200px: không cuộn ngang, cột gọn", "P1",
     L(D1, "Chọn cấp bung \"Tất cả cấp (đến Hàng hoá)\"."),
     L("1. Mở báo cáo ở cửa sổ rộng 1440px.", "2. Thu cửa sổ còn 1200px.",
       "3. Quan sát thanh cuộn ngang của trang và của bảng."),
     "Cấp bung: Tất cả cấp (đến Hàng hoá)",
     L("- Ở cả 2 độ rộng, trang và bảng KHÔNG có thanh cuộn ngang.",
       "- Ô \"Tiêu chí theo dõi\": 2 lựa chọn \"Theo nhân viên\" / \"Theo hàng hoá\" nằm trên 1 hàng, không "
       "đè lên nhãn nổi.")),

    (7, "Thu gọn / mở rộng dải tổng hợp", "P2",
     "Mở báo cáo.",
     L("1. Bấm nút \"Thu gọn\" ở dòng đầu dải tổng hợp.", "2. Bấm \"Mở rộng\"."),
     "—",
     L("- Thu gọn: 2 khối ẩn, chỉ còn dòng \"Tồn hàng giữ tại …\"; nút đổi chữ thành \"Mở rộng\".",
       "- Mở rộng: 2 khối hiện lại đủ 7 ô.")),

    (8, "Nhóm nút góc phải thanh lọc cách đều nhau", "P1",
     "Mở báo cáo ở cửa sổ 1440px, bộ lọc đang mở.",
     L("1. Quan sát cụm nút góc phải thanh lọc.",
       "2. Đo khoảng cách giữa các nút liền kề (công cụ đo của trình duyệt)."),
     "—",
     L("- Đủ 4 nút theo thứ tự: \"In danh sách\" · \"Xuất Excel\" (xanh lá) · \"Cài đặt bộ lọc\" · "
       "\"Ẩn tìm kiếm nâng cao\".",
       "- Khoảng cách giữa mọi cặp nút liền kề BẰNG NHAU (12px), không có cặp nào dính sát 0px.",
       "- 4 nút thẳng hàng theo chiều dọc, cùng chiều cao.")),

    (9, "Chữ trong ô bảng để thường, số đúng định dạng", "P1",
     L(D1, "Công ty A có ít nhất 1 con số từ 1,000 trở lên."),
     L("1. Mở báo cáo, chọn cấp \"Tất cả cấp (đến Hàng hoá)\".",
       "2. Quan sát chữ trong các ô của bảng và các tiêu đề cột Trong hạn / Sắp hết hạn / Hết hạn."),
     "—",
     L("- Chữ trong mọi ô dữ liệu để thường (không in đậm), kể cả tên phòng ban và mã hàng.",
       "- Tiêu đề 3 cột hạn cùng màu xanh ngọc của tiêu đề bảng.",
       "- Mọi con số dạng 1,234.5 (phẩy ngăn nghìn, chấm thập phân).")),
]

# ============================================================== II. BỘ LỌC & TÌM KIẾM
S2 = [
    (1, "Cascade Công ty > Phòng ban > Bộ phận > Nhân viên khi đổi Công ty", "P0",
     L(D1, "Tài khoản QL có quyền, đang chọn công ty A, Phòng ban KD1, Bộ phận Dự án, Nhân viên An."),
     L("1. Đổi Công ty sang công ty B.", "2. Quan sát 3 ô Phòng ban, Bộ phận, Nhân viên."),
     "Công ty: công ty B",
     L("- Phòng ban, Nhân viên về \"tất cả\"; Bộ phận bị khoá \"Chọn phòng ban trước\".",
       "- Danh sách Phòng ban / Nhân viên đổi sang của công ty B.",
       "- Báo cáo tải lại ngay theo công ty B, về trang 1.")),

    (2, "Đổi Phòng ban xoá Bộ phận + Nhân viên đã chọn", "P0",
     L(D1, "Đang chọn Phòng ban KD1, Bộ phận Dự án, Nhân viên An."),
     L("1. Đổi Phòng ban sang KD2.", "2. Quan sát ô Bộ phận, Nhân viên và bảng."),
     "Phòng ban: KD2",
     L("- Bộ phận và Nhân viên về trống (không giữ bộ phận Dự án của phòng cũ).",
       "- Bảng hiện dữ liệu KD2 (Giang, 2 mã), không rỗng vô lý.")),

    (3, "Ô Bộ phận trạng thái 1: chưa chọn phòng ban", "P0",
     "Mở báo cáo, Phòng ban = tất cả.",
     L("1. Quan sát ô Bộ phận.", "2. Bấm thử vào ô."),
     "Phòng ban: (tất cả)",
     L("- Ô bị khoá (nền xám), ghi \"Chọn phòng ban trước\".",
       "- Bấm vào không mở danh sách.")),

    (4, "Ô Bộ phận trạng thái 2: phòng chưa chia bộ phận", "P0",
     L(D1, "Phòng KD2 chưa chia bộ phận nào."),
     L("1. Chọn Phòng ban = KD2.", "2. Quan sát ô Bộ phận."),
     "Phòng ban: KD2",
     L("- Ô Bộ phận bị khoá, ghi \"Phòng này chưa chia bộ phận\".",
       "- Không để ô trống im lặng — luôn có câu giải thích.")),

    (5, "Ô Bộ phận trạng thái 3: phòng có bộ phận + mục \"Chưa phân bộ phận\"", "P0",
     L(D1, "KD1 có bộ phận Dự án (An đang giữ hàng), Thương mại (không ai giữ hàng), và Bình chưa phân bộ phận."),
     L("1. Chọn Phòng ban = KD1.", "2. Mở ô Bộ phận."),
     "Phòng ban: KD1",
     L("- Ô Bộ phận mở được, liệt kê \"Dự án\" và \"Chưa phân bộ phận\".",
       "- KHÔNG có \"Thương mại\" (bộ phận không ai đang giữ hàng).")),

    (6, "Cộng các bộ phận lại bằng đúng tổng của phòng", "P0",
     L(D1, "KD1: An (Dự án) 5 yêu cầu, Bình (chưa phân bộ phận) 3 yêu cầu."),
     L("1. Chọn Phòng ban = KD1, đọc \"Tổng yêu cầu đang giữ hàng\".",
       "2. Chọn Bộ phận = Dự án, đọc lại.", "3. Chọn Bộ phận = Chưa phân bộ phận, đọc lại."),
     L("Bộ phận: (tất cả)", "Bộ phận: Dự án", "Bộ phận: Chưa phân bộ phận"),
     L("- Tất cả = 8; Dự án = 5 (chỉ An); Chưa phân bộ phận = 3 (chỉ Bình).",
       "- 5 + 3 = 8: lọc bộ phận KHÔNG nuốt mất nhóm chưa phân bộ phận.")),

    (7, "Mục \"Chưa phân bộ phận\" chỉ hiện khi phòng còn người chưa gán", "P2",
     "Phòng KD3 có 2 bộ phận, mọi nhân viên đang giữ hàng đều đã được gán bộ phận.",
     L("1. Chọn Phòng ban = KD3.", "2. Mở ô Bộ phận."),
     "Phòng ban: KD3",
     "- Chỉ liệt kê các bộ phận, KHÔNG có mục \"Chưa phân bộ phận\"."),

    (8, "Chọn Bộ phận thì ô Nhân viên chỉ còn người trong bộ phận đó", "P0",
     L(D1),
     L("1. Chọn Phòng ban = KD1, Bộ phận = Dự án.", "2. Mở ô Nhân viên.",
       "3. Đổi Bộ phận = Chưa phân bộ phận, mở lại ô Nhân viên."),
     L("Bộ phận: Dự án", "Bộ phận: Chưa phân bộ phận"),
     L("- Bộ phận Dự án: ô Nhân viên chỉ có An.",
       "- Chưa phân bộ phận: chỉ có Bình.",
       "- Đổi Bộ phận thì Nhân viên đang chọn bị xoá về tất cả.")),

    (9, "Ô Nhân viên chỉ liệt kê người đang giữ hàng, đúng khuôn tên", "P1",
     L(D1, "Phòng KD1 có thêm nhân viên Chi không giữ hàng nào."),
     L("1. Chọn Phòng ban = KD1.", "2. Mở ô Nhân viên."),
     "Phòng ban: KD1",
     L("- Chỉ có An và Bình, KHÔNG có Chi.",
       "- Mỗi dòng theo khuôn \"Tên - Mã phòng - Mã nhân viên\".")),

    (10, "Lọc Khách hàng", "P0",
     L(D1),
     L("1. Mở ô Khách hàng.", "2. Chọn \"Cơ khí Hải Phòng\"."),
     "Khách hàng: Cơ khí Hải Phòng",
     L("- Ô chỉ liệt kê khách đang được giữ hàng trong phạm vi (Đóng tàu Hạ Long, Cơ khí Hải Phòng, Xây dựng Hà Nội).",
       "- Sau khi chọn: bảng chỉ còn KD1 > Bình với 3 mã; \"Tổng yêu cầu đang giữ hàng\" = 3; ô Khách hàng "
       "của dải tổng hợp = 1.")),

    (11, "Lọc Thương hiệu và Model", "P1",
     L(D1, "HH-02 Van bi thương hiệu Kitz, model V100; không mã nào khác dùng Kitz."),
     L("1. Chọn Thương hiệu = Kitz.", "2. Xóa lọc, chọn Model = V100."),
     L("Thương hiệu: Kitz", "Model: V100"),
     L("- Mỗi lần lọc bảng chỉ còn HH-02 dưới An; dòng TỔNG ra số lượng 10 (vì chỉ còn 1 mã).",
       "- Danh sách 2 ô chỉ có thương hiệu / model đang có hàng giữ.")),

    (12, "Lọc Trạng thái hạn giữ", "P0",
     L(D1),
     L("1. Chọn Trạng thái hạn giữ = Hết hạn.", "2. Đổi sang Sắp hết hạn.", "3. Đổi sang Trong hạn."),
     L("Trạng thái: Hết hạn", "Trạng thái: Sắp hết hạn", "Trạng thái: Trong hạn"),
     L("- Hết hạn: còn HH-03 (An), HH-01 + HH-06 (Bình); cột Trong hạn và Sắp hết hạn = 0 ở mọi dòng.",
       "- Sắp hết hạn: chỉ HH-02 (An).",
       "- Trong hạn: HH-01, HH-04, HH-05 (An) và HH-07 (Bình).")),

    (13, "Cảnh báo trước N ngày đổi cách chia Trong hạn / Sắp hết hạn", "P0",
     L(D1, "HH-04 của An hạn hôm nay+20."),
     L("1. Gõ 25 vào ô \"Cảnh báo trước (ngày)\", bấm Enter.", "2. Quan sát dòng An và dòng HH-04.",
       "3. Xoá trống ô, bấm Tìm kiếm."),
     L("Cảnh báo trước (ngày): 25", "Cảnh báo trước (ngày): (trống)"),
     L("- Với 25: HH-04 chuyển từ Trong hạn sang Sắp hết hạn; dòng An: Trong hạn 2 Mã, Sắp hết hạn 2 Mã.",
       "- \"Yêu cầu sắp hết hạn\" tăng thêm 1.",
       "- Để trống: quay về ngưỡng 7 của hệ thống, HH-04 về Trong hạn.",
       "- Gõ số rồi CHƯA Enter thì báo cáo chưa tải lại.")),

    (14, "Ngưỡng 0 ngày: chỉ hàng hết hạn đúng hôm nay là Sắp hết hạn", "P1",
     "Có 1 dòng hàng giữ hạn = hôm nay và 1 dòng hạn = ngày mai.",
     L("1. Gõ 0 vào ô Cảnh báo trước, Enter.", "2. Bấm số Sắp hết hạn của dòng TỔNG."),
     "Cảnh báo trước (ngày): 0",
     L("- Dòng hạn hôm nay thuộc Sắp hết hạn, ô hạn ghi \"hết hạn hôm nay\".",
       "- Dòng hạn ngày mai thuộc Trong hạn.")),

    (15, "Lọc Hình thức giữ", "P0",
     L(D1, "Trong D1 chỉ HH-05 là giữ theo hợp đồng."),
     L("1. Chọn Hình thức giữ = Giữ theo hợp đồng.", "2. Đổi sang Không theo hợp đồng."),
     L("Hình thức giữ: Giữ theo hợp đồng", "Hình thức giữ: Không theo hợp đồng"),
     L("- Theo hợp đồng: chỉ còn HH-05 (An); popup chi tiết cột Số hợp đồng ghi HĐ-001.",
       "- Không theo hợp đồng: 7 yêu cầu còn lại; popup cột Số hợp đồng ghi \"Không theo hợp đồng\".",
       "- Cả 2 trường hợp đều có khách hàng.")),

    (16, "Tìm hàng hoá theo mã hoặc tên", "P0",
     L(D1),
     L("1. Gõ \"HH-01\" vào ô Tìm hàng hoá, Enter.", "2. Xoá, gõ \"van bi\", bấm Tìm kiếm.",
       "3. Gõ \"không-tồn-tại\", Enter."),
     L("Tìm hàng hoá: HH-01", "Tìm hàng hoá: van bi", "Tìm hàng hoá: không-tồn-tại"),
     L("- \"HH-01\": còn An và Bình, mỗi người 1 dòng HH-01; dòng TỔNG ra số lượng 1,254.5.",
       "- \"van bi\": chỉ HH-02.",
       "- Không khớp: bảng ghi \"Không có hàng giữ nào khớp bộ lọc.\", các ô tổng hợp = 0, không lỗi.")),

    (17, "Ô chọn tải lại ngay, ô gõ tay phải Enter / Tìm kiếm", "P1",
     L(D1),
     L("1. Chọn Trạng thái hạn giữ = Hết hạn (quan sát bảng).",
       "2. Gõ \"HH-03\" vào Tìm hàng hoá, KHÔNG Enter, chờ 3 giây.", "3. Bấm Tìm kiếm."),
     L("Trạng thái: Hết hạn", "Tìm hàng hoá: HH-03"),
     L("- Bước 1: bảng tải lại ngay sau khi chọn.",
       "- Bước 2: bảng chưa đổi.",
       "- Bước 3: bảng chỉ còn HH-03.")),

    (18, "Xóa lọc giữ Công ty và Tiêu chí, các ô khác về mặc định", "P0",
     L(D1, "Tài khoản QL có quyền, đang chọn \"Tất cả công ty\", Theo hàng hoá, Phòng ban KD1, Trạng thái "
           "Hết hạn, Tìm hàng hoá \"HH\"."),
     L("1. Bấm \"Xóa lọc\".", "2. Đọc lại các ô lọc."),
     "—",
     L("- Công ty vẫn là \"Tất cả công ty\".",
       "- Tiêu chí vẫn là Theo hàng hoá.",
       "- Phòng ban, Bộ phận, Nhân viên, Khách hàng, Thương hiệu, Model, Trạng thái, Hình thức giữ, Tìm "
       "hàng hoá, Cảnh báo trước đều về trống.",
       "- Báo cáo tải lại, về trang 1.")),

    (19, "\"Hàng giữ của tôi\" bật: ép về đúng hàng của mình", "P0",
     L(D1_AN, "An đang xem Theo hàng hoá, cấp \"Chỉ Hàng hoá\"."),
     L("1. Đăng nhập An, mở báo cáo, chọn Theo hàng hoá.", "2. Bấm \"Hàng giữ của tôi\"."),
     "—",
     L("- Nút chuyển sang nền xanh đặc (đang bật).",
       "- Tiêu chí = Theo nhân viên; Phòng ban = KD1; Bộ phận = Dự án; Nhân viên = An; cấp bung = \"Tất cả "
       "cấp (đến Hàng hoá)\".",
       "- Bảng đúng 7 dòng dưới dòng TỔNG: 1 phòng ban > 1 nhân viên > 5 hàng hoá, bung sẵn hết.")),

    (20, "\"Hàng giữ của tôi\" tắt bằng chính nút đó: khôi phục đúng bộ lọc trước", "P0",
     L(D1, "An đang ở Theo hàng hoá, cấp \"Chỉ Hàng hoá\", Phòng ban trống rồi bật \"Hàng giữ của tôi\"."),
     L("1. Bấm lại \"Hàng giữ của tôi\" để tắt.", "2. Đọc các ô lọc và ô cấp bung."),
     "—",
     L("- Nút về dạng viền (tắt).",
       "- Tiêu chí về Theo hàng hoá, cấp về \"Chỉ Hàng hoá\", Phòng ban / Bộ phận / Nhân viên về trống "
       "đúng như trước khi bật — KHÔNG về mặc định của màn.")),

    (21, "Đổi tay ô bị ép khi đang bật: tắt cờ nhưng giữ lựa chọn mới", "P1",
     L(D1, "An đang bật \"Hàng giữ của tôi\"."),
     L("1. Đổi ô Nhân viên sang Bình.", "2. Quan sát nút và bộ lọc.",
       "3. Bật lại, rồi đổi ô Trạng thái hạn giữ = Hết hạn."),
     L("Nhân viên: Bình", "Trạng thái: Hết hạn"),
     L("- Sau bước 1: nút về tắt; Nhân viên vẫn là Bình (không bị kéo về bộ lọc cũ).",
       "- Đổi Trạng thái (ô không bị ép): nút VẪN bật, bảng chỉ còn HH-03.",
       "- Bấm \"Xóa lọc\" khi đang bật cũng làm nút về tắt.")),

    (22, "\"Hàng giữ của tôi\" khi người chưa gán bộ phận / không giữ gì", "P2",
     L(D1, "Bình chưa phân bộ phận; Dũng không giữ hàng nào."),
     L("1. Đăng nhập Bình, bấm \"Hàng giữ của tôi\".", "2. Đăng nhập Dũng, bấm \"Hàng giữ của tôi\"."),
     "—",
     L("- Bình: Bộ phận để \"tất cả\" (KHÔNG ép \"Chưa phân bộ phận\"), bảng ra 3 mã của Bình.",
       "- Dũng: ô Nhân viên vẫn hiện tên Dũng; bảng ghi \"Không có hàng giữ nào khớp bộ lọc.\".")),

    (23, "Có quyền: bật \"Hàng giữ của tôi\" khi đang xem công ty khác", "P1",
     L(D1, "QL (có quyền, công ty A) giữ 1 mã; đang chọn Công ty = công ty B."),
     L("1. Bấm \"Hàng giữ của tôi\".", "2. Tắt lại."),
     "Công ty: công ty B",
     L("- Bật: Công ty tự chuyển về công ty A cùng phòng ban của QL, bảng ra đúng 1 mã của QL (không rỗng).",
       "- Tắt: Công ty quay về công ty B.")),
]

# ============================================================== III. DẢI TỔNG HỢP
S3 = [
    (1, "Đủ 2 khối, 7 ô, đúng thứ tự", "P0",
     L(D1, "Lọc Phòng ban = KD1."),
     L("1. Đọc dải tổng hợp từ trái sang phải."),
     "Phòng ban: KD1",
     L("- Khối trái \"Phạm vi đang giữ\" (meta \"8 yêu cầu giữ\"): Nhân viên đang giữ 2 người · Hàng hoá bị "
       "giữ 7 mã hàng · Khách hàng 2 khách.",
       "- Khối phải \"Tình trạng theo yêu cầu giữ\" (meta \"8 yêu cầu · quá hạn 37.5%\"): Tổng yêu cầu đang giữ "
       "hàng 8 (7 mã hàng) · Yêu cầu sắp hết hạn 1 (12.5%) · Yêu cầu đã hết hạn 3 (37.5%) · NV có hàng giữ "
       "quá hạn 2 (trên 2 người).",
       "- 2 khối nằm gọn 1 hàng, không sinh cuộn ngang.")),

    (2, "Yêu cầu giữ = Phiếu + Mã hàng + Nhân viên, không đếm theo phiếu", "P0",
     "Phiếu xuất giữ PXG-05 của An xin giữ 5 mã khác nhau, tất cả còn hàng; không có hàng giữ nào khác.",
     L("1. Lọc Nhân viên = An.", "2. Đọc \"Tổng yêu cầu đang giữ hàng\"."),
     "Nhân viên: An",
     L("- \"Tổng yêu cầu đang giữ hàng\" = 5 (KHÔNG phải 1).",
       "- Dòng phụ \"5 mã hàng\".")),

    (3, "Gia hạn một phần số lượng: 2 dòng nhưng vẫn 1 yêu cầu giữ", "P0",
     "An giữ 10 Cái HH-08 từ PXG-03; đã gia hạn 4 Cái sang hạn mới, 6 Cái còn hạn cũ.",
     L("1. Lọc Nhân viên = An, Tìm hàng hoá = HH-08.", "2. Đọc \"Tổng yêu cầu đang giữ hàng\".",
       "3. Bấm vào số đó, đếm dòng trong popup."),
     "Tìm hàng hoá: HH-08",
     L("- \"Tổng yêu cầu đang giữ hàng\" = 1.",
       "- Popup có 2 dòng (6 Cái hạn cũ, 4 Cái hạn mới), dòng đếm ghi \"1 mã hàng · 1 yêu cầu giữ\".",
       "- Cả 2 dòng cột Phiếu giữ gốc đều ghi PXG-03.")),

    (4, "Sắp hết hạn và Đã hết hạn chồng lấn — không cộng thành tổng", "P0",
     "Yêu cầu của An cho HH-09 (1 phiếu) đã gia hạn một phần: 3 Cái quá hạn 1 ngày, 2 Cái còn 2 ngày.",
     L("1. Lọc Tìm hàng hoá = HH-09.", "2. Đọc 3 ô của khối Tình trạng theo yêu cầu giữ.",
       "3. Rê chuột lên biểu tượng chữ i của ô Yêu cầu sắp hết hạn."),
     "Tìm hàng hoá: HH-09",
     L("- Tổng yêu cầu = 1; Yêu cầu sắp hết hạn = 1; Yêu cầu đã hết hạn = 1 (1 + 1 lớn hơn tổng là ĐÚNG).",
       "- Chú thích ghi rõ 2 nhóm CHỒNG LẤN, không cộng lại.")),

    (5, "Bấm từng ô mở popup có số khớp ô vừa bấm", "P0",
     L(D1, "Lọc Phòng ban = KD1."),
     L("1. Bấm số 8 của \"Tổng yêu cầu đang giữ hàng\", đọc dòng đếm popup, đóng.",
       "2. Làm tương tự với Yêu cầu sắp hết hạn (1), Yêu cầu đã hết hạn (3), NV có hàng giữ quá hạn (2).",
       "3. Bấm số \"Nhân viên đang giữ\"."),
     "Phòng ban: KD1",
     L("- Popup Tổng yêu cầu: \"… 8 yêu cầu giữ\", 8 dòng.",
       "- Sắp hết hạn: 1 yêu cầu giữ (HH-02). Đã hết hạn: 3 yêu cầu giữ (HH-03, HH-01 của Bình, HH-06).",
       "- NV quá hạn: chỉ các dòng quá hạn của An và Bình.",
       "- Khối \"Phạm vi đang giữ\": bấm số nào cũng mở danh sách TOÀN BỘ 8 dòng.")),

    (6, "Dải tổng hợp không theo trang", "P0",
     "Công ty A có 30 mã hàng đang giữ; tiêu chí Theo hàng hoá, 10 nhóm/trang.",
     L("1. Ghi lại 7 ô của dải tổng hợp và dòng TỔNG ở trang 1.", "2. Sang trang 2, đọc lại.",
       "3. Đổi cấp bung, đọc lại."),
     L("Tiêu chí: Theo hàng hoá", "Số dòng/trang: 10"),
     "- 7 ô tổng hợp và dòng TỔNG giữ NGUYÊN giá trị ở trang 1, trang 2 và sau khi đổi cấp."),

    (7, "Chú thích ô ghi đúng khoảng ngày sắp hết hạn theo ngưỡng", "P2",
     "Hôm nay 03/10/2026.",
     L("1. Gõ 10 vào ô Cảnh báo trước, Enter.", "2. Rê chuột lên biểu tượng chữ i của Yêu cầu sắp hết hạn."),
     "Cảnh báo trước (ngày): 10",
     "- Chú thích ghi \"Có ít nhất một phần hàng đến hạn trong khoảng 03/10/2026 – 13/10/2026\"."),

    (8, "Tỉ lệ ghi \"—\" khi không có yêu cầu nào", "P2",
     "Bộ lọc không khớp dòng nào.",
     L("1. Tìm hàng hoá = \"không-tồn-tại\", Enter.", "2. Đọc khối Tình trạng theo yêu cầu giữ."),
     "Tìm hàng hoá: không-tồn-tại",
     L("- Các ô = 0; dòng phụ tỉ lệ ghi \"—\" (không ghi 0.0%).",
       "- Số 0 không bấm được.")),
]

# ============================================================== IV. BẢNG THEO DÕI
S4 = [
    (1, "Theo nhân viên: cây Phòng ban > Nhân viên > Hàng hoá, đo theo dòng", "P0",
     L(D1, "Lọc Phòng ban = KD1."),
     L("1. Chọn cấp \"Tất cả cấp (đến Hàng hoá)\".", "2. Đọc dòng TỔNG, dòng KD1, An, Bình và các dòng hàng hoá."),
     "Cấp bung: Tất cả cấp (đến Hàng hoá)",
     L("- Dòng TỔNG: STT \"TỔNG\", nội dung \"Phòng ban / Nhân viên / Hàng hoá\", Số lượng giữ \"7 Mã\".",
       "- KD1: \"7 Mã\"; An: \"5 Mã\" · 3 · 1 · 1; Bình: \"3 Mã\" · 1 · 0 · 2.",
       "- Dòng hàng hoá HH-01 dưới An: Số lượng giữ 1,234.5 (không có chữ Mã), Trong hạn 1,234.5, 2 cột "
       "còn lại 0.",
       "- STT: KD1 = 1; An = 1.1; HH-01 của An = 1.1.1.")),

    (2, "Dòng nhiều mã: 3 cột hạn chồng lấn, lớn hơn cột Số lượng giữ", "P0",
     L(D1, "HH-01 vừa có phần trong hạn (An) vừa có phần quá hạn (Bình)."),
     L("1. Lọc Phòng ban = KD1.", "2. Đọc dòng KD1.", "3. Rê chuột lên biểu tượng chữ i của cột Trong hạn."),
     "Phòng ban: KD1",
     L("- Dòng KD1: Số lượng giữ \"7 Mã\"; Trong hạn 4 Mã; Sắp hết hạn 1 Mã; Hết hạn 3 Mã — tổng 8 lớn hơn 7 "
       "là ĐÚNG (HH-01 đếm ở cả 2 cột).",
       "- Chú thích cột ghi rõ ở dòng gom nhiều mã 3 cột đếm chồng lấn, ở dòng 1 mã thì chia hết.")),

    (3, "Dòng 1 mã: 3 cột hạn chia hết tổng", "P0",
     L(D1),
     L("1. Chọn Tiêu chí = Theo hàng hoá.", "2. Đọc dòng HH-01 và 2 dòng nhân viên con."),
     "Tiêu chí: Theo hàng hoá",
     L("- HH-01: Số lượng giữ 1,254.5; Trong hạn 1,234.5; Sắp hết hạn 0; Hết hạn 20 (cộng = 1,254.5).",
       "- Dòng An dưới HH-01: 1,234.5 (số lượng, không phải \"1 Mã\"); Bình: 20.")),

    (4, "Theo hàng hoá: dòng TỔNG vẫn đếm mã, lọc còn 1 mã thì ra số lượng", "P1",
     L(D1, "Lọc Phòng ban = KD1."),
     L("1. Chọn Theo hàng hoá, đọc dòng TỔNG.", "2. Tìm hàng hoá = HH-01, Enter, đọc lại dòng TỔNG."),
     L("Tiêu chí: Theo hàng hoá", "Tìm hàng hoá: HH-01"),
     L("- Chưa lọc: dòng TỔNG \"Hàng hoá / Nhân viên\" ghi \"7 Mã\" (với phạm vi KD1).",
       "- Lọc còn HH-01: dòng TỔNG ghi 1,254.5, không còn chữ Mã.")),

    (5, "Cột Tồn hiện tại chỉ có ở tiêu chí Theo hàng hoá", "P0",
     "Công ty A: HH-01 tồn kho 907 Mét.",
     L("1. Ở Theo nhân viên, cấp Tất cả cấp, tìm cột Tồn hiện tại.", "2. Đổi sang Theo hàng hoá.",
       "3. Đổi lại Theo nhân viên."),
     L("Tiêu chí: Theo nhân viên", "Tiêu chí: Theo hàng hoá"),
     L("- Theo nhân viên: KHÔNG có cột Tồn hiện tại.",
       "- Theo hàng hoá: có cột \"Tồn hiện tại\"; HH-01 ghi 907; dòng TỔNG và dòng nhân viên ghi \"—\".",
       "- Đổi lại Theo nhân viên: cột biến mất.",
       "- Popup chi tiết KHÔNG có cột Tồn hiện tại ở cả 2 tiêu chí.")),

    (6, "Tồn hiện tại khi xem Tất cả công ty = cộng tồn mọi công ty", "P1",
     "HH-01 tồn công ty A 602, công ty B 456. Tài khoản QL có quyền.",
     L("1. Theo hàng hoá, Công ty = công ty A, đọc Tồn hiện tại của HH-01.",
       "2. Đổi Công ty = Tất cả công ty, đọc lại."),
     L("Công ty: công ty A", "Công ty: Tất cả công ty"),
     L("- Công ty A: 602.", "- Tất cả công ty: 1,058 (602 + 456).")),

    (7, "Cột Đơn vị / Model / Thương hiệu tự ẩn khi chưa có dòng hàng hoá", "P1",
     L(D1),
     L("1. Theo nhân viên, cấp \"Đến Nhân viên\": đếm cột.", "2. Bấm mũi tên dòng An để bung 1 nhánh."),
     "Cấp bung: Đến Nhân viên",
     L("- Bước 1: bảng chỉ có STT · Nội dung theo dõi · Số lượng giữ · Trong hạn · Sắp hết hạn · Hết hạn.",
       "- Bước 2: xuất hiện thêm Đơn vị · Model · Thương hiệu ngay sau cột Nội dung theo dõi.",
       "- Cột Đơn vị chỉ để đọc (đơn vị cơ bản), không có ô đổi đơn vị.")),

    (8, "Ô chọn cấp bung đổi theo tiêu chí", "P1",
     "Mở báo cáo.",
     L("1. Mở ô cấp bung ở Theo nhân viên.", "2. Đổi Theo hàng hoá, mở lại ô cấp bung."),
     "—",
     L("- Theo nhân viên: \"Chỉ Phòng ban\" · \"Đến Nhân viên\" · \"Tất cả cấp (đến Hàng hoá)\".",
       "- Theo hàng hoá: \"Chỉ Hàng hoá\" · \"Tất cả cấp (đến Nhân viên)\"; mặc định \"Chỉ Hàng hoá\".")),

    (9, "Bung tay cấp cuối: tải khi bấm, cộng lại bằng dòng cha", "P0",
     L(D1_AN),
     L("1. Lọc Nhân viên = An, cấp \"Đến Nhân viên\".", "2. Bấm mũi tên ở dòng An.",
       "3. Bấm mũi tên lần nữa."),
     "Nhân viên: An",
     L("- Bấm: hiện biểu tượng đang tải trên dòng An, rồi ra đúng 5 dòng HH-01..HH-05, STT 1.1.1 tới 1.1.5.",
       "- Mũi tên xoay hướng mở; cộng 3 cột hạn của 5 dòng hàng hoá khớp với ý nghĩa dòng An (3 / 1 / 1 mã).",
       "- Bấm lần nữa: thu lại, không tải lại.")),

    (10, "Bung tay khi mạng lỗi: dòng thu lại và báo lỗi", "P2",
     L(D1, "Ngắt mạng (công cụ trình duyệt) ngay trước khi bung."),
     L("1. Ở cấp \"Đến Nhân viên\", bấm mũi tên dòng An khi mạng đang ngắt.", "2. Bật lại mạng, bấm lần nữa."),
     "—",
     L("- Lần 1: có đúng 1 thông báo lỗi; dòng An thu lại (không mở ra rỗng).",
       "- Lần 2: tải lại được 5 dòng hàng hoá.")),

    (11, "Phân trang theo nhóm cấp 1, STT chạy tiếp", "P0",
     "Công ty A có 30 mã hàng đang giữ.",
     L("1. Chọn Theo hàng hoá.", "2. Chọn 10 dòng/trang.", "3. Bấm trang 2."),
     L("Tiêu chí: Theo hàng hoá", "Số dòng/trang: 10"),
     L("- Trang 2: STT cấp 1 chạy 11 tới 20 (không đánh lại từ 1).",
       "- Dòng đếm: \"Hiển thị 11–20 / 30 nhóm\".",
       "- Mỗi trang có tối đa 10 nhóm cấp 1, kèm đủ cấp con của chúng.")),

    (12, "Đổi bộ lọc / sắp xếp về trang 1; đổi cấp bung giữ trang", "P1",
     "Đang ở trang 2 (Theo hàng hoá, 10 dòng/trang).",
     L("1. Đổi cấp bung sang \"Tất cả cấp (đến Nhân viên)\".", "2. Bấm sắp xếp cột Nội dung theo dõi.",
       "3. Về trang 2, đổi Trạng thái hạn giữ = Hết hạn."),
     "—",
     L("- Đổi cấp bung: vẫn ở trang 2.",
       "- Sắp xếp: về trang 1.",
       "- Đổi bộ lọc: về trang 1.")),

    (13, "Đổi cỡ trang khi đang ở trang cuối không ra trang rỗng", "P2",
     "30 nhóm, đang ở trang 3 với 10 dòng/trang.",
     L("1. Đổi cỡ trang sang 50."),
     "Số dòng/trang: 50",
     "- Bảng ra trang 1 với đủ 30 nhóm, không hiện trang trống."),

    (14, "Sắp xếp cột Nội dung theo dõi: A-Z, Z-A, về mặc định", "P0",
     "Công ty A có 4 phòng: An Phú (0 quá hạn), Ánh Dương (2 quá hạn), Bình Minh (5 quá hạn), Đức Thành (1 quá hạn).",
     L("1. Quan sát thứ tự mặc định.", "2. Bấm tiêu đề \"Nội dung theo dõi\" lần 1.",
       "3. Bấm lần 2.", "4. Bấm lần 3."),
     "—",
     L("- Mặc định: nhiều hàng quá hạn nhất lên trước: Bình Minh, Ánh Dương, Đức Thành, An Phú; biểu tượng "
       "hai chiều.",
       "- Lần 1 (mũi tên lên, A-Z theo tiếng Việt): An Phú, Ánh Dương, Bình Minh, Đức Thành (Á, Đ không bị "
       "đẩy xuống cuối).",
       "- Lần 2 (mũi tên xuống): đảo ngược.",
       "- Lần 3: về đúng thứ tự mặc định.",
       "- Sắp xếp trên TOÀN BỘ rồi mới cắt trang.")),

    (15, "Tên hàng dài cắt 2 dòng + chú thích đủ tên", "P1",
     "Có hàng hoá tên dài khoảng 150 ký tự, model dài 40 ký tự.",
     L("1. Bung tới cấp Hàng hoá.", "2. Quan sát ô tên và ô Model.", "3. Rê chuột lên ô tên."),
     "—",
     L("- Ô tên hiện tối đa 2 dòng, phần thừa thành dấu ba chấm; Model / Thương hiệu tối đa 1 dòng.",
       "- Rê chuột hiện đủ \"Mã hàng - Tên hàng\".",
       "- Mã hàng nằm cùng ô, đứng trước tên, chữ nhỏ xám nền nhạt, ngăn bằng dấu \"-\".")),

    (16, "Bấm số trên bảng mở popup đúng nhánh + đúng nhóm hạn", "P0",
     L(D1),
     L("1. Lọc Phòng ban = KD1, bấm số Hết hạn của dòng Bình (2).",
       "2. Đóng, bấm số Số lượng giữ của dòng KD1."),
     "—",
     L("- Popup 1: tiêu đề \"Đang xem hàng giữ đã quá hạn theo Nhân viên: Bình - KD1\", 2 dòng (HH-01 20 Mét, "
       "HH-06 5 Cuộn).",
       "- Popup 2: \"Đang xem hàng giữ theo Phòng ban: KD1\", 8 dòng.",
       "- Số 0 không bấm được.")),

    (17, "Bảng rỗng có câu giải thích", "P2",
     "Bộ lọc không khớp dòng nào.",
     L("1. Chọn Khách hàng = Đóng tàu Hạ Long, Trạng thái = Hết hạn, Hình thức giữ = Giữ theo hợp đồng."),
     "—",
     "- Bảng ghi \"Không có hàng giữ nào khớp bộ lọc.\", dòng TỔNG các cột = 0."),
]

# ============================================================== V. POPUP CHI TIẾT HÀNG GIỮ
S5 = [
    (1, "Đủ 15 cột đúng thứ tự khi mở từ dòng TỔNG", "P0",
     L(D1),
     L("1. Bấm số Số lượng giữ của dòng TỔNG.", "2. Đọc tiêu đề cột từ trái sang phải."),
     "—",
     L("- Đủ 15 cột: STT · Mã hàng - Tên hàng · ĐVT · SL đang giữ · Ngày bắt đầu giữ · Hạn giữ hiện tại · Số "
       "lần gia hạn · Thương hiệu / Model · Khách hàng · Số hợp đồng · Tổng thanh toán · Nhân viên giữ · Phòng "
       "ban · Trạng thái · Phiếu giữ gốc.",
       "- KHÔNG có cột Tồn hiện tại, KHÔNG có cột Hành động riêng.",
       "- Tiêu đề: \"Đang xem hàng giữ — toàn bộ báo cáo\".")),

    (2, "Ẩn cột theo chiều đã cố định", "P0",
     L(D1),
     L("1. Bấm số của dòng KD1 (Phòng ban).", "2. Bấm số của dòng An (Nhân viên).",
       "3. Theo hàng hoá, bấm số của dòng HH-01."),
     "—",
     L("- Từ KD1: ẩn cột Phòng ban; tiêu đề \"…theo Phòng ban: KD1\".",
       "- Từ An: ẩn cả Nhân viên giữ và Phòng ban, ẩn ô lọc nhân viên; tiêu đề \"…theo Nhân viên: An - KD1\".",
       "- Từ HH-01: cột Mã hàng - Tên hàng VẪN hiện; chỉ ô lọc hàng hoá bị ẩn; tiêu đề \"…theo Hàng hoá: "
       "HH-01 - Ống thủy lực\".")),

    (3, "Ẩn cột + ô lọc Trạng thái khi con số đã là 1 trạng thái", "P1",
     L(D1),
     L("1. Bấm số Hết hạn của dòng TỔNG.", "2. Bấm ô \"NV có hàng giữ quá hạn\"."),
     "—",
     L("- Cả 2 popup không có cột Trạng thái và không có ô lọc trạng thái.",
       "- Bấm Số lượng giữ hoặc Tổng yêu cầu thì có lại cột Trạng thái.")),

    (4, "Ghim 3 cột đầu khi cuộn ngang", "P0",
     L(D1, "Cửa sổ 1440px."),
     L("1. Mở popup từ dòng TỔNG.", "2. Kéo thanh cuộn ngang của bảng sang phải hết cỡ.",
       "3. Phóng to popup, cuộn lại."),
     "—",
     L("- STT · Mã hàng - Tên hàng · ĐVT đứng yên, khít nhau, không đè nhau, có viền và nền đặc (nội dung "
       "cột sau không chạy xuyên qua).",
       "- Cột SL đang giữ trở đi trôi theo thanh cuộn.",
       "- Sau khi phóng to vẫn ghim đúng.")),

    (5, "Ô Hạn giữ hiện tại tô màu + ghi số ngày", "P0",
     L(D1_AN),
     L("1. Lọc Nhân viên = An, mở popup từ dòng TỔNG.", "2. Đọc ô Hạn giữ hiện tại của HH-01, HH-02, HH-03."),
     "—",
     L("- HH-01: ngày hạn + \"còn 30 ngày\", chữ xanh lá.",
       "- HH-02: \"còn 3 ngày\", chữ vàng cam.",
       "- HH-03: \"quá hạn 5 ngày\", chữ đỏ.",
       "- Dòng hạn hôm nay ghi \"hết hạn hôm nay\".")),

    (6, "Đổi ngưỡng đổi màu ô hạn", "P1",
     "Dòng HH-10 còn 8 ngày.",
     L("1. Ngưỡng 7: mở popup, xem ô hạn HH-10.", "2. Gõ 10 vào Cảnh báo trước, Enter, mở lại popup."),
     L("Cảnh báo trước (ngày): 7", "Cảnh báo trước (ngày): 10"),
     L("- Ngưỡng 7: xanh lá, badge \"Trong hạn\".", "- Ngưỡng 10: vàng cam, badge \"Sắp hết hạn\".")),

    (7, "Badge Trạng thái đúng chữ và màu", "P1",
     L(D1_AN),
     L("1. Mở popup của An.", "2. Đọc cột Trạng thái 3 dòng HH-01, HH-02, HH-03."),
     "—",
     L("- \"Trong hạn\" chữ xanh lá trên nền xanh lá nhạt.",
       "- \"Sắp hết hạn\" chữ vàng cam trên nền vàng nhạt.",
       "- \"Hết hạn\" chữ đỏ trên nền đỏ nhạt.")),

    (8, "Thứ tự mặc định: quá hạn lâu nhất lên đầu", "P0",
     L(D1),
     L("1. Lọc Phòng ban = KD1, mở popup từ dòng TỔNG.", "2. Đọc cột Hạn giữ hiện tại từ trên xuống."),
     "—",
     "- Thứ tự: HH-06 (quá hạn 10 ngày), HH-03 (quá 5), HH-01 của Bình (quá 2), HH-02 (còn 3), HH-04, HH-01 "
     "của An, HH-05, HH-07 — hạn giữ tăng dần."),

    (9, "Sắp xếp 7 cột, chu kỳ tăng / giảm / mặc định", "P0",
     L(D1),
     L("1. Mở popup từ dòng TỔNG (KD1).",
       "2. Lần lượt bấm tiêu đề: Mã hàng - Tên hàng, SL đang giữ, Khách hàng, Nhân viên giữ, Phòng ban, Ngày bắt "
       "đầu giữ, Hạn giữ hiện tại — mỗi cột bấm 3 lần.",
       "3. Rê chuột lên tiêu đề có sắp xếp.", "4. Bấm thử tiêu đề ĐVT, Số lần gia hạn."),
     "—",
     L("- Mỗi cột: lần 1 tăng dần, lần 2 giảm dần, lần 3 về thứ tự mặc định (hạn giữ tăng dần).",
       "- Sắp xếp trên toàn bộ kết quả, về trang 1.",
       "- Rê chuột: tiêu đề gạch chân, nền KHÔNG đổi màu, chữ vẫn đọc được.",
       "- ĐVT, Số lần gia hạn và các cột khác không sắp xếp được.")),

    (10, "Lọc trong popup: tìm nhanh, Nhân viên, Khách hàng, Hàng hoá, Trạng thái", "P0",
     L(D1),
     L("1. Mở popup từ dòng TỔNG (KD1).", "2. Gõ \"PXG-02\" vào ô tìm nhanh (chờ không quá 1 giây).",
       "3. Xoá, chọn Nhân viên = Bình.", "4. Chọn thêm Trạng thái = Hết hạn.", "5. Bấm \"Xoá lọc\" trong popup."),
     L("Tìm nhanh: PXG-02", "Nhân viên: Bình", "Trạng thái: Hết hạn"),
     L("- Tìm \"PXG-02\": còn HH-04 (tìm được theo mã/tên hàng, khách hàng, nhân viên, phiếu gốc).",
       "- Nhân viên = Bình: 3 dòng; thêm Hết hạn: 2 dòng.",
       "- Nút \"Xoá lọc\" chỉ hiện khi có ô lọc đang chọn; bấm thì về 8 dòng.",
       "- Ô lọc trong popup KHÔNG làm đổi bảng chính phía sau.")),

    (11, "Dòng đếm tính trên toàn bộ kết quả, gộp đơn vị tính", "P1",
     L(D1),
     L("1. Mở popup KD1 (8 dòng, đơn vị Mét, Cái, Bộ, Cuộn, Cây).", "2. Lọc Nhân viên = An.",
       "3. Đổi cỡ trang về 20 rồi sang trang khác (nếu có)."),
     "—",
     L("- KD1: \"7 mã hàng · 8 yêu cầu giữ · 5 đơn vị tính\" (trên 3 đơn vị thì chỉ ghi số đơn vị).",
       "- An: \"5 mã hàng · 5 yêu cầu giữ · ĐVT: \" kèm đủ 3 đơn vị Mét, Cái, Bộ (từ 3 đơn vị trở xuống thì liệt kê tên).",
       "- Dòng đếm không đổi theo trang.")),

    (12, "Phân trang popup: mặc định 20, STT chạy tiếp, giữ cỡ trang khi mở popup khác", "P1",
     "Công ty A có 85 dòng hàng giữ.",
     L("1. Mở popup từ dòng TỔNG.", "2. Sang trang 2.", "3. Đổi cỡ trang sang 50, đóng popup.",
       "4. Mở popup khác từ dòng KD1."),
     "—",
     L("- Mặc định 20 dòng/trang; lựa chọn 20/50/100.",
       "- Trang 2: STT bắt đầu 21.",
       "- Popup mở lại giữ cỡ 50 dòng/trang, nhưng về trang 1 và xoá lọc / sắp xếp của lượt trước.")),

    (13, "Cột Số hợp đồng và Tổng thanh toán", "P0",
     L(D1_AN),
     L("1. Mở popup của An.", "2. Đọc 2 cột Số hợp đồng, Tổng thanh toán ở HH-05 và HH-01."),
     "—",
     L("- HH-05: Số hợp đồng \"HĐ-001\"; Tổng thanh toán 70,000,000 (bấm được).",
       "- HH-01: \"Không theo hợp đồng\"; Tổng thanh toán \"—\".",
       "- Hợp đồng chưa có chứng từ thanh toán: Tổng thanh toán \"0\", không bấm được.")),

    (14, "Cột Phiếu giữ gốc: mã chứng từ gốc, mở tab mới", "P0",
     L(D1_AN),
     L("1. Mở popup của An.", "2. Đọc cột Phiếu giữ gốc của HH-04.", "3. Rê chuột lên mã, bấm vào mã."),
     "—",
     L("- HH-04 ghi \"PXG-02\" (phiếu xuất giữ gốc), KHÔNG ghi GH-1 hay GH-2.",
       "- Rê chuột hiện loại chứng từ (\"Phiếu xuất giữ\").",
       "- Bấm mở phiếu PXG-02 ở tab mới; popup vẫn mở ở tab cũ.",
       "- Dòng không xác định được chứng từ gốc ghi \"—\".")),

    (15, "Cột Số lần gia hạn", "P0",
     L(D1_AN),
     L("1. Mở popup của An.", "2. Đọc cột Số lần gia hạn."),
     "—",
     L("- HH-04 = 2 (bấm được); các dòng khác = 0, không bấm được.",
       "- Số lần gia hạn tính cho TỪNG lần giữ (không cộng dồn lên bảng chính).")),

    (16, "Cột Nhân viên giữ chỉ ghi tên, Khách hàng kèm mã", "P2",
     L(D1),
     L("1. Mở popup từ dòng TỔNG.", "2. Đọc cột Nhân viên giữ, Phòng ban, Khách hàng."),
     "—",
     L("- Nhân viên giữ: \"An\" (không ghép phòng ban vào cùng ô).",
       "- Phòng ban: \"KD1\" ở cột riêng.",
       "- Khách hàng: tên khách, mã khách chữ nhỏ xám liền sau.")),

    (17, "Footer popup: In danh sách · Xuất Excel · Đóng", "P1",
     L(D1),
     L("1. Mở popup.", "2. Quan sát chân popup.", "3. Bấm Đóng."),
     "—",
     L("- Thứ tự từ trái: \"In danh sách\" · \"Xuất Excel\" (xanh lá) · \"Đóng\" (luôn cuối, có mũi tên trái).",
       "- Màu chữ ô dữ liệu xám đậm (không đen tuyền).",
       "- Đóng: popup tắt, màn chính giữ nguyên bộ lọc và trang.")),
]

# ============================================================== VI. LỊCH SỬ GIA HẠN & CHỨNG TỪ THANH TOÁN
S6 = [
    (1, "Lịch sử gia hạn xếp cũ - mới, lần cuối tô nền", "P0",
     L(D1_AN, "HH-04: PXG-02 hạn ban đầu 01/09/2026; GH-1 duyệt 30/08 đổi hạn 01/09 sang 15/09; "
              "GH-2 duyệt 14/09 đổi hạn 15/09 sang hôm nay+20."),
     L("1. Mở popup của An.", "2. Bấm số 2 ở cột Số lần gia hạn của HH-04."),
     "—",
     L("- Popup \"Lịch sử gia hạn giữ hàng\" mở chồng lên popup chi tiết.",
       "- Dòng mô tả: \"HH-04 - Dây cáp · ĐVT: Mét · Khách hàng: Đóng tàu Hạ Long · Nhân viên giữ: An · Đã gia "
       "hạn 2 lần · Phiếu giữ gốc: PXG-02\".",
       "- Cột: Lần · Ngày duyệt · Phiếu gia hạn · Hạn cũ – Hạn mới (2 ngày nối bằng mũi tên) · SL gia hạn · "
       "Người đề nghị · Người duyệt.",
       "- Dòng 1 GH-1, dòng 2 GH-2 (cũ trước, mới sau); dòng 2 tô nền = hạn đang hiệu lực.",
       "- Liền mạch: hạn mới của lần 1 = hạn cũ của lần 2; hạn mới lần cuối = Hạn giữ hiện tại.")),

    (2, "Mã phiếu gia hạn mở tab mới", "P2",
     "Như TC trên.",
     L("1. Bấm mã GH-2 trong popup lịch sử."),
     "—",
     "- Phiếu GH-2 mở ở tab mới; 2 popup ở tab cũ vẫn mở."),

    (3, "Lịch sử gia hạn của dòng sinh ra từ gia hạn một phần", "P1",
     "An giữ 10 Cái HH-08 (PXG-03); GH-5 gia hạn 4 Cái sang hạn mới.",
     L("1. Mở popup của An, bấm Số lần gia hạn ở dòng 4 Cái."),
     "—",
     L("- Số lần gia hạn = 1; lịch sử 1 dòng GH-5, SL gia hạn 4.",
       "- Dòng 6 Cái còn hạn cũ: Số lần gia hạn 0.")),

    (4, "Popup chứng từ thanh toán: Phiếu thu, Phiếu báo có, Phiếu kế toán", "P0",
     L(D1_AN, "HĐ-001 có thêm Phiếu kế toán KT-01 ghi Có tài khoản 1311 số 30,000,000 ngày 01/10."),
     L("1. Mở popup của An.", "2. Bấm số Tổng thanh toán của HH-05."),
     "—",
     L("- Tiêu đề \"Thanh toán của hợp đồng HĐ-001\".",
       "- Dòng mô tả: \"Khách hàng: Đóng tàu Hạ Long · Giá trị hợp đồng: 200,000,000 · Đã thanh toán: "
       "100,000,000 (50%) · Số chứng từ: 3\".",
       "- Cột: STT · Số chứng từ · Loại chứng từ · Ngày hạch toán · Số tiền.",
       "- 3 dòng xếp mới nhất lên đầu: KT-01 Phiếu kế toán · BC-01 Phiếu báo có · PT-01 Phiếu thu.",
       "- Cột Tổng thanh toán ở popup chi tiết = 100,000,000, khớp tổng popup.")),

    (5, "Chỉ lấy phát sinh Có 1311, không trừ Nợ, không có \"Còn phải thu\"", "P0",
     "HĐ-001 có thêm 1 bút toán Nợ tài khoản 1311 số 10,000,000 (ví dụ bù trừ) và 1 Phiếu chi không liên quan 1311.",
     L("1. Mở popup chứng từ thanh toán của HĐ-001.", "2. Đọc số Đã thanh toán và tìm chữ \"Còn phải thu\"."),
     "—",
     L("- Đã thanh toán vẫn = 100,000,000 (KHÔNG trừ 10,000,000 bên Nợ, không cộng Phiếu chi).",
       "- Không có dòng / ô \"Còn phải thu\" nào trong popup.")),

    (6, "Một phiếu tách nhiều bút toán Có 1311 chỉ hiện 1 dòng", "P2",
     "Phiếu thu PT-02 của HĐ-001 tách 2 bút toán Có 1311: 5,000,000 và 3,000,000.",
     L("1. Mở popup chứng từ thanh toán của HĐ-001."),
     "—",
     "- PT-02 hiện 1 dòng số tiền 8,000,000 (gộp theo chứng từ)."),

    (7, "Đóng popup con quay lại popup chi tiết", "P2",
     L(D1),
     L("1. Mở popup chi tiết > popup lịch sử gia hạn.", "2. Đóng popup lịch sử bằng nút X."),
     "—",
     "- Popup chi tiết vẫn mở, giữ đúng trang, bộ lọc, sắp xếp đang có."),
]

# ============================================================== VII. GIA HẠN / HUỶ GIỮ
S7 = [
    (1, "Nút Gia hạn / Huỷ giữ chỉ có ở chế độ \"Hàng giữ của tôi\"", "P0",
     L(D1_AN),
     L("1. Đăng nhập An, mở popup từ dòng TỔNG (chế độ thường).",
       "2. Đóng, bật \"Hàng giữ của tôi\", mở lại popup từ dòng TỔNG."),
     "—",
     L("- Chế độ thường: KHÔNG có nút nào trong ô Hạn giữ hiện tại (kể cả dòng của chính An).",
       "- Chế độ của tôi: 5/5 dòng có 2 nút \"Gia hạn\" (xanh ngọc, biểu tượng lịch) và \"Huỷ giữ\" (đỏ, biểu "
       "tượng dấu x) nằm TRONG ô Hạn giữ hiện tại, dưới dòng \"còn N ngày\".",
       "- Nút dạng viền, có chữ; không có cột Hành động riêng; bảng vẫn 15 cột.")),

    (2, "Gia hạn dòng trong ngưỡng: màn lập phiếu tick sẵn đúng dòng", "P0",
     L(D1_AN),
     L("1. Bật \"Hàng giữ của tôi\", mở popup.", "2. Bấm \"Gia hạn\" ở dòng HH-02 (còn 3 ngày)."),
     "—",
     L("- Không hỏi xác nhận, chuyển sang màn lập Yêu cầu gia hạn hàng giữ.",
       "- Dòng HH-02 được tick sẵn ô \"Cần gia hạn\" và cuộn tới giữa màn.",
       "- Các dòng sắp hết hạn khác vẫn hiện bình thường, không bị tick.")),

    (3, "Gia hạn dòng còn xa hạn: thông báo vàng, không lỗi đỏ", "P0",
     L(D1_AN),
     L("1. Bật \"Hàng giữ của tôi\", mở popup.", "2. Bấm \"Gia hạn\" ở dòng HH-01 (còn 30 ngày)."),
     "—",
     L("- Màn lập phiếu gia hạn mở, đầu bảng có ghi chú nền vàng: \"Hàng này còn 30 ngày mới tới hạn, chưa "
       "lập được yêu cầu gia hạn\" kèm ngưỡng 7 ngày của hệ thống.",
       "- KHÔNG phải thông báo lỗi đỏ, KHÔNG ra màn trống: các dòng sắp hết hạn khác vẫn hiện.",
       "- HH-01 không xuất hiện trong bảng (không nới điều kiện của màn gia hạn).")),

    (4, "Gia hạn dòng không thuộc về mình", "P1",
     L(D1, "An biết mã dòng HH-06 của Bình."),
     L("1. Đăng nhập An, mở thẳng màn lập phiếu gia hạn kèm mã dòng HH-06 của Bình."),
     "Dòng: HH-06 (của Bình)",
     L("- Ghi chú: \"Không tìm thấy hàng giữ cần gia hạn hoặc hàng này không thuộc về bạn.\"",
       "- Không lập được gia hạn hộ Bình.")),

    (5, "Huỷ giữ: điền sẵn khách + đúng hàng hoá", "P0",
     L(D1_AN),
     L("1. Bật \"Hàng giữ của tôi\", mở popup.", "2. Bấm \"Huỷ giữ\" ở dòng HH-03."),
     "—",
     L("- Không hỏi xác nhận, chuyển sang màn lập Yêu cầu hủy hàng giữ.",
       "- Ô Khách hàng điền sẵn \"Đóng tàu Hạ Long\"; bảng hàng hoá có đúng HH-03 (không lẫn hàng hoá có mã "
       "gần giống).",
       "- Ghi chú xám: \"Hủy giữ trừ theo hạn giữ sớm nhất của cùng hàng hoá – khách hàng, kiểm lại số lượng "
       "trước khi gửi.\"",
       "- Thoát ngay không sửa gì: KHÔNG hiện cảnh báo chưa lưu.")),

    (6, "Huỷ giữ dòng đã hết hàng / không còn tồn", "P2",
     "Dòng X của An vừa bị huỷ hết sau khi popup đã mở.",
     L("1. Bấm \"Huỷ giữ\" ở dòng X trên popup cũ."),
     "—",
     L("- Màn lập phiếu hủy báo \"Không tìm thấy hàng giữ cần hủy\".",
       "- Ô khách hàng vẫn chọn được bình thường, không trắng màn.")),

    (7, "Huỷ giữ khi cùng hàng + khách còn nhiều hạn khác nhau", "P1",
     "An giữ HH-09 cho Đóng tàu Hạ Long ở 2 hạn: 3 Cái quá hạn 1 ngày, 2 Cái còn 2 ngày.",
     L("1. Bật \"Hàng giữ của tôi\", bấm \"Huỷ giữ\" ở dòng 2 Cái.",
       "2. Gửi duyệt hủy 2 Cái, duyệt xong mở lại báo cáo."),
     "Số lượng hủy: 2",
     L("- Màn lập phiếu cho sửa số lượng.",
       "- Sau duyệt: hệ thống trừ từ hạn SỚM NHẤT trước (dòng 3 Cái còn 1 Cái, dòng 2 Cái giữ nguyên) — "
       "đúng như ghi chú, không hứa hủy đúng dòng vừa bấm.")),

    (8, "Mở thẳng 2 màn lập phiếu từ menu: hành vi cũ không đổi", "P0",
     L(D1_AN),
     L("1. Mở màn Yêu cầu gia hạn hàng giữ > Thêm mới từ menu (không qua báo cáo).",
       "2. Mở màn Yêu cầu hủy hàng giữ > Thêm mới từ menu."),
     "—",
     L("- Màn gia hạn: liệt kê các dòng sắp hết hạn của An như trước, không tick sẵn dòng nào, không có ghi chú vàng.",
       "- Màn hủy: ô Khách hàng trống, bảng hàng hoá trống, không có ghi chú xám; chọn khách rồi thêm hàng như cũ.")),

    (9, "Bật \"Hàng giữ của tôi\" ngay lúc bảng đang tải không lộ nút trên hàng người khác", "P2",
     L(D1, "Mạng chậm (giả lập 3G)."),
     L("1. Đăng nhập An, đang xem Phòng ban KD1.",
       "2. Bấm \"Hàng giữ của tôi\" rồi bấm ngay vào số của dòng Bình trước khi bảng tải xong."),
     "—",
     "- Nếu popup kịp mở thì là danh sách của Bình KHÔNG có nút Gia hạn / Huỷ giữ."),
]

# ============================================================== VIII. XUẤT EXCEL / IN
S8 = [
    (1, "Popup chọn chế độ In", "P1",
     "Mở báo cáo.",
     L("1. Bấm \"In danh sách\" trên thanh tiêu đề.", "2. Quan sát popup."),
     "—",
     L("- Popup \"In danh sách\" ghi \"Bản in A4 ngang, bám đúng bộ lọc báo cáo đang hiển thị.\"",
       "- 2 lựa chọn: \"In bảng theo dõi\" (mặc định) và \"In danh sách chi tiết\", mỗi lựa chọn có dòng mô tả.",
       "- Chân popup: \"In\" trước, \"Hủy\" sau cùng.")),

    (2, "In bảng theo dõi ở trang 2 vẫn in đủ mọi cấp, mọi trang", "P0",
     "Công ty A có 30 mã hàng; đang Theo hàng hoá, 10 nhóm/trang, đứng ở trang 2, cấp \"Chỉ Hàng hoá\".",
     L("1. Bấm \"In danh sách\" > \"In bảng theo dõi\" > In.", "2. Đếm dòng trong bản xem trước."),
     "—",
     L("- Bản in có đủ 30 hàng hoá và toàn bộ dòng nhân viên con dưới mỗi hàng hoá (không chỉ 10 dòng trang 2, "
       "không dừng ở cấp đang thu gọn).",
       "- Có dòng TỔNG và dải tổng hợp; số liệu khớp màn hình.")),

    (3, "Dòng tóm tắt bộ lọc trên bản in", "P0",
     L(D1, "Tài khoản QL có quyền."),
     L("1. Chọn Công ty A, Phòng ban KD1, Bộ phận Chưa phân bộ phận, Trạng thái Hết hạn, Cảnh báo trước 10, "
       "Hình thức giữ Không theo hợp đồng, Tìm hàng hoá \"HH\".", "2. In bảng theo dõi."),
     "—",
     L("- Đầu bản in có \"Ngày in\" và \"Bộ lọc đang áp dụng: Công ty: công ty A · Phòng ban: KD1 · Bộ phận: Chưa "
       "phân bộ phận · Trạng thái: Hết hạn · Cảnh báo trước: 10 ngày · Hình thức giữ: Không theo hợp đồng · Tìm "
       "hàng hoá: \"HH\"\".",
       "- Ô không chọn thì không in ra.")),

    (4, "Bản in: cấp 2 in đậm, cấp 3 không thụt lề, đo giống màn", "P0",
     L(D1, "Lọc Phòng ban KD1, Theo nhân viên."),
     L("1. In bảng theo dõi.", "2. Quan sát cột Nội dung theo dõi và cột Số lượng giữ."),
     "—",
     L("- Phòng ban (cấp 1) không đậm; nhân viên An, Bình (cấp 2) IN ĐẬM, thụt 1 nấc.",
       "- Dòng hàng hoá (cấp 3) KHÔNG thụt lề, không tràn khổ giấy.",
       "- Số lượng giữ: dòng KD1 / An / Bình ghi \"7 Mã\" / \"5 Mã\" / \"3 Mã\"; dòng hàng hoá ghi số lượng — "
       "giống hệt màn hình.",
       "- Theo hàng hoá: cấp 2 (nhân viên) cũng in đậm.")),

    (5, "Bản in: mã và tên không dính nhau, ô hạn không có chữ nút", "P1",
     L(D1_AN, "An bật \"Hàng giữ của tôi\"."),
     L("1. Mở popup chi tiết, bấm \"In danh sách\" ở chân popup.", "2. Đọc cột Mã hàng - Tên hàng, Khách hàng, "
       "Hạn giữ hiện tại."),
     "—",
     L("- Mã hàng - Tên hàng: \"HH-01 - Ống thủy lực\" (có khoảng trắng 2 bên dấu -).",
       "- Khách hàng: tên và mã cách nhau, không dính liền.",
       "- Ô hạn: \"dd/mm/yyyy còn 30 ngày\" — KHÔNG có chữ \"Gia hạn\" / \"Huỷ giữ\".")),

    (6, "In danh sách chi tiết từ thanh tiêu đề và từ popup", "P0",
     L(D1),
     L("1. Thanh tiêu đề: In danh sách > In danh sách chi tiết > In.",
       "2. Mở popup của Bình, lọc Trạng thái Hết hạn, sắp xếp SL đang giữ giảm dần, bấm In danh sách ở chân popup."),
     "—",
     L("- Bước 1: bản in \"CHI TIẾT HÀNG GIỮ\" đủ mọi dòng theo bộ lọc màn chính (không theo trang 20 dòng).",
       "- Bước 2: chỉ 2 dòng quá hạn của Bình, đúng thứ tự sắp xếp đang chọn trong popup.",
       "- Không có chữ nút trong ô hạn giữ.")),

    (7, "Logo theo công ty đang lọc; Tất cả công ty không logo", "P0",
     "Công ty A và công ty B có logo khác nhau. Tài khoản QL (công ty A) có quyền.",
     L("1. Chọn Công ty = công ty B, In bảng theo dõi.", "2. Chọn Tất cả công ty, In lại.",
       "3. Đăng nhập An (không quyền), In."),
     L("Công ty: công ty B", "Công ty: Tất cả công ty"),
     L("- Công ty B: đầu bản in là logo / letterhead của công ty B (KHÔNG phải công ty của người in).",
       "- Tất cả công ty: không có logo, không có khoảng trống lớn ở đầu trang.",
       "- An: logo công ty A.")),

    (8, "Logo lỗi không để lại khoảng trống lớn", "P2",
     "Công ty C cấu hình đường dẫn logo sai (ảnh không tải được).",
     L("1. In báo cáo của công ty C."),
     "Công ty: công ty C",
     "- Khối đầu trang tự ẩn, tiêu đề \"BÁO CÁO THEO DÕI GIỮ HÀNG\" nằm ngay đầu trang (không có ô trống lớn)."),

    (9, "Bản in quá 2,000 dòng: cắt và cảnh báo", "P1",
     "Tài khoản QL, Tất cả công ty, danh sách chi tiết có 2,412 dòng.",
     L("1. In danh sách > In danh sách chi tiết > In."),
     "Công ty: Tất cả công ty",
     L("- Bản in chỉ có 2,000 dòng đầu.",
       "- Dòng \"Cảnh báo\": \"Danh sách có 2,412 dòng, bản in chỉ hiển thị 2,000 dòng đầu. Dùng Xuất Excel để "
       "lấy đủ dữ liệu.\"",
       "- Dưới 2,000 dòng thì không có dòng cảnh báo.")),

    (10, "Xuất Excel bảng theo dõi đủ dữ liệu", "P0",
     "Công ty A có 30 mã hàng; đang ở trang 2, cấp \"Chỉ Hàng hoá\", Theo hàng hoá.",
     L("1. Bấm \"Xuất Excel\" trên thanh tiêu đề.", "2. Mở file."),
     "—",
     L("- File tải về đúng đuôi .xlsx (kể cả trên Safari).",
       "- Dòng đầu \"BÁO CÁO THEO DÕI GIỮ HÀNG\", dòng 2 là tóm tắt bộ lọc.",
       "- Cột: STT · Nội dung theo dõi · Đơn vị · Model · Thương hiệu · Tồn hiện tại · Số lượng giữ · Trong hạn · "
       "Sắp hết hạn · Hết hạn (Theo nhân viên thì không có Tồn hiện tại).",
       "- Đủ dòng TỔNG + 30 hàng hoá + mọi nhân viên con, không theo trang / cấp trên màn.")),

    (11, "Excel: ô số là số thật, STT không mất số 0", "P0",
     "File Excel của TC trên.",
     L("1. Bấm vào ô Số lượng giữ của 1 dòng hàng hoá.", "2. Dùng SUM cộng cột Hết hạn của các dòng hàng hoá.",
       "3. Đọc STT dòng thứ 10 của cấp 2."),
     "—",
     L("- Ô số là SỐ (căn phải, Excel không báo \"số dạng chữ\"), định dạng 1,234.5.",
       "- SUM ra đúng tổng, không ra 0.",
       "- STT \"1.10\" giữ nguyên (không thành 1.1).",
       "- Dòng gom nhiều mã: chữ \"Mã\" nằm ở cột Đơn vị, ô số vẫn là số.")),

    (12, "Excel: cùng quy tắc thụt lề / in đậm với bản in", "P1",
     L(D1, "Theo nhân viên, Phòng ban KD1."),
     L("1. Xuất Excel.", "2. Quan sát cột Nội dung theo dõi."),
     "—",
     L("- Nhân viên (cấp 2) in đậm, thụt 1 nấc; hàng hoá (cấp 3) không thụt.",
       "- Dòng TỔNG in đậm.",
       "- File Excel không có logo.")),

    (13, "Xuất Excel danh sách chi tiết từ popup", "P0",
     L(D1),
     L("1. Mở popup KD1, lọc Nhân viên = An.", "2. Bấm \"Xuất Excel\" ở chân popup."),
     "—",
     L("- File có đủ 15 cột của popup, 5 dòng của An (không phải chỉ trang đang xem).",
       "- Ô hạn giữ không có chữ \"Gia hạn\" / \"Huỷ giữ\".",
       "- Số lượng, Tổng thanh toán là số thật.")),

    (14, "In / Xuất theo bộ lọc ĐANG HIỂN THỊ, không theo ô vừa gõ chưa Enter", "P1",
     L(D1),
     L("1. Lọc Trạng thái = Hết hạn (bảng đã tải).", "2. Gõ \"HH-03\" vào Tìm hàng hoá nhưng KHÔNG Enter.",
       "3. Bấm Xuất Excel."),
     "Tìm hàng hoá: HH-03 (chưa Enter)",
     "- File chứa đúng 3 dòng hết hạn đang thấy trên bảng, KHÔNG lọc theo \"HH-03\"."),

    (15, "Logo bản in phiếu yêu cầu hủy giữ và Danh sách hàng giữ (màn cũ)", "P2",
     "Công ty A có logo.",
     L("1. In 1 phiếu Yêu cầu hủy hàng giữ.", "2. In màn cũ Danh sách hàng giữ."),
     "—",
     "- Cả 2 bản in hiện đúng logo công ty A (trước đây mất logo)."),
]

# ============================================================== IX. RÀNG BUỘC NHẬP LIỆU
S9 = [
    (1, "Cảnh báo trước nhận số nguyên 0 – 365", "P0",
     "Mở báo cáo.",
     L("1. Lần lượt gõ các giá trị vào ô \"Cảnh báo trước (ngày)\", mỗi lần bấm Enter."),
     L("-1", "366", "2.5", "abc", "0", "365"),
     L("- -1, 366, 2.5: báo lỗi đỏ ngay dưới ô \"Nhập số nguyên từ 0 đến 365\", báo cáo KHÔNG tải lại, số "
       "đã gõ vẫn giữ nguyên (không tự sửa).",
       "- abc: ô số không nhận chữ.",
       "- 0 và 365: hợp lệ, báo cáo tải lại.")),

    (2, "Còn lỗi ở ô Cảnh báo trước thì đổi ô khác cũng không tải", "P1",
     "Ô Cảnh báo trước đang báo lỗi với 500 ngày.",
     L("1. Chọn Trạng thái hạn giữ = Hết hạn.", "2. Bấm sang trang 2, bấm sắp xếp."),
     L("Cảnh báo trước (ngày): 500", "Trạng thái: Hết hạn"),
     L("- Báo cáo không tải lại cho tới khi sửa ô về hợp lệ.",
       "- Sửa về 7 rồi Enter: tải lại theo cả Trạng thái = Hết hạn.")),

    (3, "In / Xuất khi ô Cảnh báo trước đang lỗi dùng ngưỡng hệ thống", "P2",
     "Ô Cảnh báo trước đang báo lỗi với -5, bảng đang hiện theo ngưỡng 7.",
     L("1. Bấm Xuất Excel."),
     "Cảnh báo trước (ngày): -5",
     "- File chia trạng thái theo ngưỡng 7 (đúng bảng đang thấy), không lỗi."),

    (4, "Gọi thẳng chức năng với tham số sai kiểu bị từ chối gọn", "P1",
     "Tester kỹ thuật, phiên đăng nhập An.",
     L("1. Dùng công cụ kiểm thử API gọi danh sách chi tiết với chỉ số = bogus.",
       "2. Gọi báo cáo với tiêu chí gửi dạng danh sách nhiều giá trị.",
       "3. Gọi báo cáo với Cảnh báo trước = -3."),
     L("Chỉ số: bogus", "Tiêu chí: gửi 2 giá trị cùng lúc", "Cảnh báo trước: -3"),
     L("- Bước 1: báo \"Chỉ số không hợp lệ\", KHÔNG trả toàn bộ danh sách.",
       "- Bước 2: báo \"Tham số không hợp lệ: …\", không lỗi hệ thống.",
       "- Bước 3: dùng ngưỡng cấu hình hệ thống (7).")),

    (5, "Ô Tìm hàng hoá với ký tự đặc biệt", "P2",
     L(D1),
     L("1. Gõ lần lượt các giá trị vào Tìm hàng hoá, Enter."),
     L("%", "_", "'", "<b>x</b>"),
     L("- Không lỗi hệ thống; % và _ không khớp tất cả.",
       "- \"<b>x</b>\" in ra nguyên văn trong dòng tóm tắt bộ lọc của bản in, không bị in đậm.")),
]

# ============================================================== X. DỮ LIỆU NGUỒN & PHIẾU GIỮ GỐC
S10 = [
    (1, "Phiếu giữ gốc lần ngược qua nhiều lần gia hạn", "P0",
     "Dòng hàng giữ HH-04 của An: PXG-02 > GH-1 > GH-2 (mỗi lần gia hạn tạo dòng mới, dòng cũ về 0).",
     L("1. Mở popup của An.", "2. Đọc Phiếu giữ gốc của HH-04.", "3. Tìm nhanh \"GH-2\" trong popup."),
     "Tìm nhanh: GH-2",
     L("- Phiếu giữ gốc = PXG-02.",
       "- Tìm \"GH-2\" không ra dòng nào (cột gốc không mang mã phiếu gia hạn).",
       "- Dòng cũ đã về 0 không hiện.")),

    (2, "Gia hạn lập + duyệt trên hệ thống mới: dòng mới giữ đúng phiếu gốc", "P0",
     "An giữ 10 Cái HH-02 từ PXG-01, hạn hôm nay+3.",
     L("1. Lập + duyệt Yêu cầu gia hạn hàng giữ 10 Cái HH-02 trên hệ thống mới.", "2. Mở lại báo cáo, popup của An."),
     "SL gia hạn: 10",
     L("- HH-02: Hạn giữ hiện tại = hạn mới; Số lần gia hạn = 1; Phiếu giữ gốc vẫn = PXG-01.",
       "- Tổng yêu cầu đang giữ hàng của An không đổi (5).")),

    (3, "Gia hạn lập + duyệt trên ERP cũ: báo cáo mới vẫn ra đúng phiếu gốc", "P0",
     "An giữ HH-10 từ PXG-07 lập trên ERP.",
     L("1. Trên ERP, lập và duyệt phiếu gia hạn cho HH-10.", "2. Mở báo cáo mới, popup của An."),
     "—",
     L("- Dòng HH-10 hạn mới, Số lần gia hạn = 1, Phiếu giữ gốc = PXG-07.",
       "- Không đếm thành 2 yêu cầu giữ.")),

    (4, "Phiếu xuất giữ lập trên ERP cũ và trên hệ thống mới", "P0",
     "An chưa giữ HH-11, HH-12.",
     L("1. Trên ERP lập + duyệt Phiếu xuất giữ PXG-08 giữ HH-11 cho khách Đóng tàu Hạ Long.",
       "2. Trên hệ thống mới lập + duyệt Phiếu xuất giữ PXG-09 giữ HH-12.", "3. Mở báo cáo, popup của An."),
     "—",
     L("- HH-11: Phiếu giữ gốc PXG-08; HH-12: PXG-09; rê chuột hiện loại \"Phiếu xuất giữ\".",
       "- Tổng yêu cầu của An tăng thêm 2.")),

    (5, "Nhập hàng cho khách tạo hàng giữ có phiếu gốc đúng", "P1",
     "Trên ERP lập phiếu Nhập hàng cho khách NK-01 cho An giữ HH-13.",
     L("1. Duyệt NK-01.", "2. Mở báo cáo, popup của An."),
     "—",
     "- HH-13: Phiếu giữ gốc NK-01, loại \"Nhập hàng cho khách\"."),

    (6, "Điều chuyển giữ (ERP và hệ thống mới) có phiếu gốc là phiếu điều chuyển", "P1",
     "Bình điều chuyển 5 Cuộn HH-06 sang An bằng phiếu điều chuyển giữ ĐC-01.",
     L("1. Duyệt ĐC-01 (làm 1 lần trên ERP, 1 lần trên hệ thống mới với ĐC-02).", "2. Mở popup của An."),
     "—",
     L("- Dòng HH-06 mới của An: Phiếu giữ gốc ĐC-01 (và ĐC-02), loại \"Điều chuyển giữ\".",
       "- Dòng của Bình giảm tương ứng (về 0 thì biến mất).")),

    (7, "Hàng nhập thêm gộp vào dòng sẵn có cùng hạn: phiếu gốc là phiếu tạo dòng", "P2",
     "An đã giữ HH-01 1,234.5 Mét từ PXG-01 hạn X; lập thêm PXG-10 giữ 100 Mét HH-01 cùng khách, cùng hạn X.",
     L("1. Duyệt PXG-10.", "2. Mở popup của An, đọc dòng HH-01."),
     "—",
     L("- Chỉ 1 dòng HH-01 số lượng 1,334.5, Phiếu giữ gốc vẫn PXG-01 (phiếu đã tạo dòng).",
       "- Lưu ý: ca gộp này rất hiếm; ghi nhận đúng thiết kế, không phải lỗi.")),

    (8, "Dữ liệu cũ trước khi cập nhật có phiếu gốc đúng", "P1",
     "Dòng hàng giữ cũ (tạo trước khi nâng cấp) đã qua 3 lần gia hạn từ phiếu PXG-OLD.",
     L("1. Mở popup, tìm dòng đó."),
     "—",
     L("- Phiếu giữ gốc = PXG-OLD, Số lần gia hạn = 3.",
       "- Dòng không lần ra chứng từ gốc ghi \"—\", không báo lỗi.")),

    (9, "Hàng đã xuất / huỷ hết biến mất khỏi báo cáo", "P0",
     L(D1_AN),
     L("1. Lập + duyệt hủy giữ toàn bộ 2 Bộ HH-03.", "2. Mở lại báo cáo, lọc An."),
     "SL hủy: 2",
     L("- HH-03 không còn trong bảng và popup.",
       "- An: 4 Mã; Hết hạn 0; \"Yêu cầu đã hết hạn\" giảm 1; \"NV có hàng giữ quá hạn\" không còn An.")),

    (10, "Đổi ngưỡng trên báo cáo không ghi đè cấu hình chung", "P1",
     "Ngưỡng hệ thống 7.",
     L("1. Gõ 30 vào Cảnh báo trước trên báo cáo, Enter.", "2. Mở màn lập Yêu cầu gia hạn hàng giữ.",
       "3. Mở lại báo cáo ở tab mới."),
     "Cảnh báo trước (ngày): 30",
     L("- Màn gia hạn vẫn chỉ liệt kê dòng còn tối đa 7 ngày.",
       "- Báo cáo mở mới: ô Cảnh báo trước trống, hiện mờ 7.")),
]

# ============================================================== XI. CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI
S11 = [
    (1, "Đổi lọc liên tiếp nhanh: bảng khớp lựa chọn cuối", "P1",
     L(D1, "Mạng chậm (giả lập 3G)."),
     L("1. Chọn liên tiếp thật nhanh Trạng thái = Hết hạn, rồi Sắp hết hạn, rồi Trong hạn."),
     "—",
     "- Sau khi tải xong, bảng và dải tổng hợp đúng Trong hạn; không bị kết quả Hết hạn về trễ đè lên."),

    (2, "Đổi lọc khi đang bung một dòng", "P2",
     L(D1, "Mạng chậm."),
     L("1. Bấm mũi tên dòng An (đang tải).", "2. Ngay lập tức đổi Phòng ban = KD2."),
     "Phòng ban: KD2",
     "- Bảng KD2 không bị chèn 5 dòng hàng hoá của An vào."),

    (3, "Popup đang mở không đổi theo màn chính", "P2",
     L(D1),
     L("1. Mở popup từ dòng TỔNG (KD1).", "2. Mở tab khác cùng tài khoản, đổi lọc rồi quay lại popup, sang trang 2."),
     "—",
     "- Popup giữ đúng bộ lọc lúc bấm số (KD1), tiêu đề không đổi."),

    (4, "Hai người khác quyền xem cùng lúc", "P1",
     L(D1),
     L("1. Máy 1 đăng nhập QL, chọn Tất cả công ty.", "2. Máy 2 đăng nhập An, mở báo cáo cùng lúc."),
     "—",
     L("- QL thấy 14 yêu cầu (2 công ty); An thấy 10 (công ty A).",
       "- Thao tác của người này không ảnh hưởng phạm vi của người kia.")),

    (5, "Có phiếu được duyệt trong lúc đang xem", "P2",
     L(D1_AN),
     L("1. An mở báo cáo.", "2. Người khác duyệt hủy toàn bộ HH-02 của An.",
       "3. An bấm vào số Sắp hết hạn cũ (1) chưa tải lại.", "4. An bấm Tìm kiếm."),
     "—",
     L("- Bước 3: popup ra danh sách hiện tại (có thể 0 dòng), không lỗi.",
       "- Bước 4: dải tổng hợp cập nhật, Yêu cầu sắp hết hạn = 0.")),

    (6, "Hết phiên đăng nhập khi đang bung dòng", "P2",
     "Phiên đăng nhập của An vừa hết hạn.",
     L("1. Bấm mũi tên bung dòng nhân viên."),
     "—",
     "- Hệ thống đưa về màn đăng nhập, không để dòng mở rỗng."),
]

# ============================================================== XII. LUỒNG NGHIỆP VỤ TỪ ĐẦU ĐẾN CUỐI
S12 = [
    (1, "Nhân viên tự xử lý hàng sắp hết hạn bằng gia hạn", "P0",
     L(D1_AN),
     L("1. An mở báo cáo, bấm \"Hàng giữ của tôi\".",
       "2. Bấm số Sắp hết hạn của dòng An, bấm \"Gia hạn\" ở HH-02.",
       "3. Nhập hạn mới, gửi duyệt; quản lý duyệt.",
       "4. An mở lại báo cáo, bật \"Hàng giữ của tôi\", mở popup, bấm Số lần gia hạn của HH-02."),
     "Hạn mới: hôm nay+30",
     L("- Sau duyệt: HH-02 về Trong hạn; ô Yêu cầu sắp hết hạn của An = 0.",
       "- Số lần gia hạn HH-02 = 1; Phiếu giữ gốc vẫn phiếu xuất giữ ban đầu.",
       "- Lịch sử gia hạn 1 dòng, tô nền, hạn mới = Hạn giữ hiện tại.")),

    (2, "Nhân viên trả lại hàng quá hạn bằng Huỷ giữ", "P0",
     L(D1_AN),
     L("1. An bật \"Hàng giữ của tôi\", mở popup Hết hạn.", "2. Bấm \"Huỷ giữ\" ở HH-03, gửi duyệt hủy 2 Bộ.",
       "3. Duyệt.", "4. Mở lại báo cáo."),
     "SL hủy: 2",
     L("- Màn hủy điền sẵn Đóng tàu Hạ Long + HH-03.",
       "- Sau duyệt: HH-03 biến mất; NV có hàng giữ quá hạn không còn An; Tồn hiện tại của HH-03 (Theo hàng hoá) "
       "không đổi vì báo cáo đọc tồn kho hiện có.")),

    (3, "Quản lý tổng công ty rà hàng quá hạn rồi in / xuất", "P0",
     L(D1, "Tài khoản QL có quyền."),
     L("1. QL mở báo cáo, chọn Tất cả công ty, Trạng thái = Hết hạn.",
       "2. Sắp xếp mặc định, đọc nhóm nhiều quá hạn nhất.",
       "3. In bảng theo dõi.", "4. Xuất Excel.", "5. So số trên màn, bản in, file Excel."),
     L("Công ty: Tất cả công ty", "Trạng thái: Hết hạn"),
     L("- KD1 đứng đầu (3 mã quá hạn).",
       "- Bản in không có logo, dòng tóm tắt ghi \"Trạng thái: Hết hạn\".",
       "- 3 nơi khớp nhau từng con số (dòng TỔNG, từng phòng, từng nhân viên).")),

    (4, "Kế toán ghi nhận thêm thanh toán, báo cáo cập nhật Tổng thanh toán", "P1",
     L(D1_AN),
     L("1. Kế toán lập Phiếu báo có BC-02 30,000,000 ghi Có 1311 cho HĐ-001, hạch toán.",
       "2. Mở báo cáo, popup của An, đọc Tổng thanh toán HH-05.", "3. Bấm vào số đó."),
     "Số tiền: 30,000,000",
     L("- Tổng thanh toán tăng từ 70,000,000 lên 100,000,000.",
       "- Popup chứng từ có BC-02 ở dòng đầu (mới nhất), loại \"Phiếu báo có\".")),

    (5, "Người mới được cấp quyền xem tổng công ty", "P1",
     L(D1, "Tài khoản Em (công ty B) không quyền."),
     L("1. Em mở báo cáo: chỉ thấy công ty B.", "2. Quản trị gán quyền \"" + P_ALL + "\" cho Em.",
       "3. Em đăng nhập lại, mở báo cáo, chọn Tất cả công ty."),
     "—",
     L("- Trước: nhãn tĩnh \"công ty B\", 4 yêu cầu.",
       "- Sau: ô chọn Công ty, Tất cả công ty = 14 yêu cầu.")),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DẢI TỔNG HỢP", S3),
    ("IV", "BẢNG THEO DÕI, SẮP XẾP & PHÂN TRANG", S4),
    ("V", "CỬA SỔ CHI TIẾT HÀNG GIỮ", S5),
    ("VI", "LỊCH SỬ GIA HẠN & CHỨNG TỪ THANH TOÁN", S6),
    ("VII", "GIA HẠN / HUỶ GIỮ TỪ BÁO CÁO", S7),
    ("VIII", "XUẤT EXCEL / IN", S8),
    ("IX", "RÀNG BUỘC NHẬP LIỆU", S9),
    ("X", "DỮ LIỆU NGUỒN & PHIẾU GIỮ GỐC", S10),
    ("XI", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S11),
    ("XII", "LUỒNG NGHIỆP VỤ TỪ ĐẦU ĐẾN CUỐI", S12),
]

if __name__ == "__main__":
    build(
        output_file=os.path.join(HERE, "testcase.xlsx"),
        sheet_name="Trang tính1",
        feature_name="Báo cáo theo dõi giữ hàng - Cập nhật ngày 03/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
    for roman, title, tcs in SECTIONS:
        print("  %s. %s: %d TC" % (roman, title, len(tcs)))
    print("  TC-ROLE: %d TC" % len(ROLE_TCS))
