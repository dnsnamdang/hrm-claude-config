# -*- coding: utf-8 -*-
"""Sinh testcase - Phieu tinh gia (luong Chuyen doi hang hoa, man 5/5).

Doi chieu code worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa (hrm-api 39c4a91fe,
hrm-client 5c14659e8 — 16/10/2026). SRS cung bo: gen_srs_phieu-tinh-gia.py.
Section VI danh rieng cho GIA (gia nhap kho, he so -> gia ban tron tram, Ban le lan 4 loai, TMDT, gia hieu luc, Luu va duyet ghi gi vao
bo gia cong ty phieu, gui duyet + bao nguoc, gia von cong ty quan ly theo quyen Xem gia von). So lieu mau lay tu DB dev hrm_erp_giacty
Cty 1: PTG-03178 (Da duyet, PYCTG-03162, EURO 31,900, MLER-AMAT8574091 Bo, Gia NCC 316, thue 10%, 3 chi phi, gia nhap kho
13,108,667, Ban le 22,500,000 he so 1.7 DMGG 5, TMDT 29,250,000), PTG-01959 (ENEOS Thung / Tuyp: gia nhap kho 465,360 / 19,390, he so
dang ap dung 1.61 / 1), PTG-03170 (6 ma hang), PTG-02618 (co gia hieu luc TMDT da luu), PTG-00215 (Dang tao cua nguoi khac).
DB dev KHONG co YCTG Cho tinh gia, KHONG co PTG Cho duyet gia / Gia bi tu choi, moi cong ty TAT duyet gia, khong co chinh sach gia noi
bo cho hang cong ty khac — tester tu tao theo tien dieu kien.
Chay: python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_testcase_phieu-tinh-gia.py
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

OUT = os.path.join(HERE, "testcase - Phiếu tính giá.xlsx")


def L(*lines):
    return "\n".join(lines)


def T(n, func, prio, pre, steps, data, exp):
    return (n, func, prio, pre if isinstance(pre, str) else L(*pre), steps if isinstance(steps, str) else L(*steps),
            data if isinstance(data, str) else L(*data), exp if isinstance(exp, str) else L(*exp))


MENU = "Vào phân hệ Tài chính › Quản lý giá - CTKM › nhóm “Giá bán” › bấm “Phiếu tính giá”"
MENU_YCTG = "Vào phân hệ Bán hàng › Yêu cầu › nhóm “Hàng hóa” › bấm “YC tính giá”"
MENU_DUYET = "Vào phân hệ Tài chính › Quản lý giá - CTKM › nhóm “Giá bán” › bấm “Duyệt giá bán”"
MENU_CNGB = "Vào phân hệ Tài chính › Quản lý giá - CTKM › nhóm “Giá bán” › bấm “Cập nhật giá bán”"
Q1 = "XNK xử lý yêu cầu hỏi giá"
Q2 = "Tính giá bán hàng hoá"
Q3 = "Xem giá vốn hàng hoá"
QD = "Duyệt giá bán hàng hoá"
NOPERM = "Bạn không có quyền thực hiện chức năng này"
NOVIEW = "Bạn không có quyền xem yêu cầu tính giá"
NOTFOUND = "Không tìm thấy phiếu tính giá"
NOCALC = "Bạn không có quyền Tính giá bán hàng hoá"
PAGE404 = "Không tìm thấy hoặc không được cấp quyền truy cập trang"
CONFLICT = "Trạng thái đã bị thay đổi. Vui lòng load lại trang"
CLOSED = "Nhóm hàng đã đóng, yêu cầu tính giá chỉ còn xem."
REQ = "Bắt buộc phải nhập"
SAVED = "Đã lưu phiếu tính giá"
APPLIED = "Đã áp giá bán"
SUBMITTED = "Đã gửi giá sang màn Duyệt giá bán"
PEND_G4 = "Đang có yêu cầu duyệt giá ở màn Cập nhật giá bán"

ACC_N = "Tài khoản N KHÔNG có quyền nào trong 3 quyền " + Q1 + " / " + Q2 + " / " + Q3 + ", đang chọn công ty 1."
ACC_X = "Tài khoản X chỉ có quyền " + Q1 + " tại công ty 1."
ACC_K = "Tài khoản K (Kế toán mua hàng) có quyền " + Q2 + " tại công ty 1, KHÔNG có quyền " + Q3 + "."
ACC_K2 = "Tài khoản K2 (Kế toán mua hàng khác) có quyền " + Q2 + " tại công ty 1."
ACC_V = "Tài khoản V chỉ có quyền " + Q3 + " tại công ty 1."
ACC_KV = "Tài khoản KV có cả " + Q2 + " và " + Q3 + " tại công ty 1."
ACC_D = "Tài khoản D có quyền " + QD + " tại công ty 1."
OFF = "Công ty 1 TẮT quy chế duyệt giá (như DB dev)."
ON = "Công ty 1 BẬT quy chế duyệt giá, áp mọi hãng (cấu hình ở Khai Quy chế – Cấu hình)."
Y1 = ("YCTG Y1 nhóm ENEOS (1 hàng ENEO-124-V5091, 2 ĐVT Thùng / Tuýp, tiền tệ VNĐ, Giá NCC Thùng 465,360, Tuýp 19,390, thuế 0, không chi phí) "
      "đang Chờ tính giá, chưa có PTG.")
CUR = "Giá đang áp dụng tại công ty 1: Thùng hệ số Bán lẻ 1.61, giá 796,000; Tuýp hệ số 1, giá 34,000. Hàng ENEO-124-V5091 ở trạng thái Chờ tính giá bán."
P1 = "PTG P1 của Y1 do K lập, đang Đang tạo (đã Lưu nháp)."

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     L("Phiếu tính giá (PTG, phân hệ Tài chính) là chứng từ cuối của luồng tính giá bán (YCHG sang YCTG sang PTG sang giá áp):",
       "- Kế toán mua hàng lập PTG từ 1 YCTG Chờ tính giá: kiểm / sửa số đầu vào XNK đã nhập, nhập Chi phí khác, ra Giá nhập kho, chốt hệ số / "
       "giá bán / ĐMGG / giá hiệu lực cho 6 loại giá của từng hàng × ĐVT.",
       "- Công ty tắt duyệt giá: “Lưu và duyệt” ghi ngay bộ giá + giá vốn (= giá nhập kho) vào công ty phiếu, hàng mới sang Đang kinh doanh.",
       "- Công ty bật duyệt giá: “Lưu và gửi duyệt” sinh yêu cầu ở màn Duyệt giá bán; kết quả duyệt từng dòng báo ngược về PTG.")),
    ("2. Đối tượng được tính / hiển thị",
     L("- Danh sách: PTG của CÔNG TY ĐANG LÀM VIỆC ở trạng thái Chờ duyệt giá, Giá bị từ chối, Đã duyệt (mọi người có quyền xem trong công ty thấy).",
       "- PTG Đang tạo: CHỈ người lập thấy.",
       "- Dòng PTG = dòng YCTG (mọi hàng × ĐVT); hệ số mặc định = hệ số đang áp dụng tại công ty phiếu.",
       "- Popup Chọn yêu cầu tính giá: YCTG Chờ tính giá của công ty, chưa có PTG, nhóm chưa đóng (không xét phân công hãng).")),
    ("3. Đối tượng bị ẩn / không tính",
     L("- PTG công ty khác (báo “" + NOTFOUND + "”).",
       "- PTG Đang tạo của người khác (mở thẳng ra trang “" + PAGE404 + "”).",
       "- Giá vốn của CÔNG TY QUẢN LÝ hàng (khối chính sách, popup Tạm tính) với người KHÔNG có quyền " + Q3 + " (hiện “—”).",
       "- Dòng đã duyệt của PTG Giá bị từ chối: chỉ xem, không gửi lại.")),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô lọc “Ngày lập” (từ ngày – đến ngày) lọc theo ngày lập PTG, tính trọn ngày đầu và ngày cuối. Giá hiệu lực chỉ nhận ngày từ ngày mai."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     L("- YCHG › nhóm Thương hiệu × Hãng › 1 YCTG › tối đa 1 PTG › 1 kết quả tính giá.",
       "- PTG › dòng hàng × ĐVT › chi phí + 6 loại giá (Bán lẻ, Giá bán theo lô, Đại lý cấp 1, 2, 3, TMĐT) › tối đa 1 giá hiệu lực / loại.",
       "- Tab Tính giá: mỗi dòng hàng × ĐVT là 1 khối gộp dòng.")),
    ("6. Quy tắc cộng dồn / deduplicate",
     L("- Cột Số mã hàng đếm mã hàng KHÁC NHAU (1 hàng 2 ĐVT = 1).",
       "- Tổng chi phí = tổng thành tiền VNĐ các chi phí của dòng.",
       "- Tối đa 1 yêu cầu duyệt mở / hàng × ĐVT × công ty; gửi lại = ghi đè.",
       "- Thông báo gửi duyệt gộp 1 thông báo / PTG (“<n> dòng giá”).")),
    ("7. Phân quyền cấp",
     L("Xem PTG cần ÍT NHẤT 1 trong 3 quyền (xét tại công ty đang làm việc, super admin không được miễn):",
       "- " + Q1 + ": chỉ xem (danh sách, chi tiết, in, tạm tính, xem giá bán mới).",
       "- " + Q2 + ": xem; Tạo mới / lập PTG; Sửa / Xóa / Lưu và duyệt / Lưu và gửi duyệt PTG do chính mình lập.",
       "- " + Q3 + ": xem; thấy giá vốn công ty quản lý hàng ở khối chính sách và popup Tạm tính.",
       "- Liên quan: " + QD + " (màn Duyệt giá bán) duyệt các dòng giá PTG gửi sang.",
       "Không có quyền nào: không thấy menu, không xem được. Không phân quyền theo phòng ban / cấp.")),
    ("8. Cách tính các ô thống kê",
     L("- Đơn giá VNĐ = Giá NCC × Tỉ giá; Sau thuế = Đơn giá VNĐ × (1 + Thuế NK / 100) (vd 316 × 31,900 = 10,080,400; × 1,1 = 11,088,440).",
       "- Chi phí VNĐ = Tỉ lệ / 100 × Giá NCC × Tỉ giá (vd 15% => 1,512,060).",
       "- Giá nhập kho = Sau thuế + Tổng chi phí + Chi phí khác (vd 11,088,440 + 2,020,227 + 0 = 13,108,667).",
       "- Giá bán = làm tròn TRĂM (hệ số × giá nhập kho) (vd 1,61 × 465,360 => 749,200); Giá công thức = giá nhập kho × hệ số làm tròn đồng (TMĐT tròn nghìn).",
       "- TMĐT = Bán lẻ × hệ số TMĐT công ty (dev 1,3): 900,000 => 1,170,000, hệ số 1,8 => 2,34.",
       "- Giá hiệu lực: hệ số × giá nhập kho làm tròn ĐỒNG.",
       "- Tạm tính: Theo giá vốn = tròn trăm(giá vốn × (1 + %)); Theo giá bán = tròn trăm(giá × (1 - %)).",
       "- Chân bảng “Hiển thị a–b / N”: N = tổng PTG khớp bộ lọc.")),
    ("9. Ghi chú đọc bảng",
     L("- Số tiền dấu phẩy ngăn nghìn, dấu chấm thập phân (31,900; 1.61); ngày dd/mm/yyyy.",
       "- Bẫy 1: nút là “Lưu và duyệt” HAY “Lưu và gửi duyệt” tuỳ quy chế duyệt giá của CÔNG TY PHIẾU × hãng — kiểm cấu hình trước khi chạy ca.",
       "- Bẫy 2: Lưu nháp không ghi giá nào; chỉ Lưu và duyệt (hoặc duyệt ở màn Duyệt giá bán) mới đổi giá đang áp dụng.",
       "- Bẫy 3: gõ tay Giá bán thì đổi giá nhập kho KHÔNG cập nhật giá đó; gõ lại Hệ số mới về công thức.",
       "- Bẫy 4: quyền " + Q3 + " chỉ che giá vốn công ty QUẢN LÝ; Giá nhập kho của chính PTG ai xem cũng thấy (ghi nhận để nghiệp vụ xác nhận).",
       "- Bẫy 5: PTG cũ của ERP: màn Chi tiết + bản in tính lại chi phí theo tỉ lệ nên có thể lệch vài đồng so với giá vốn đã áp (PTG-03178).",
       "- Bẫy 6: mọi PTG Đã duyệt có dòng xám “Nhóm hàng đã kết thúc (Đã tính giá)” — đúng thiết kế.",
       "- Môi trường thử: DB dev không có YCTG Chờ tính giá, không có PTG Chờ duyệt giá / Giá bị từ chối, mọi công ty tắt duyệt giá — tester tự "
       "tạo YCTG (màn YC tính giá) và bật quy chế khi cần.",
       "- Nhóm ca 'gọi thẳng chức năng, bỏ qua giao diện' dành cho tester kỹ thuật (dùng công cụ kiểm thử API).")),
]

ROLE_TCS = [
    ("01", "Không có quyền nào: không thấy menu, không xem được", "P0", [ACC_N],
     ["1. Đăng nhập N.", "2. Mở phân hệ Tài chính › Quản lý giá - CTKM.", "3. Mở thẳng màn danh sách PTG (link được gửi)."], "—",
     ["- Bước 2: nhóm Giá bán KHÔNG có mục “Phiếu tính giá”.", "- Bước 3: bảng “Không có dữ liệu phù hợp”, thông báo “" + NOVIEW + "”."]),
    ("02", "Không có quyền nào: mở thẳng Chi tiết PTG", "P0", [ACC_N, "PTG-03178 Đã duyệt ở công ty 1."],
     ["1. Mở thẳng Chi tiết PTG-03178 (link được gửi)."], "—", ["- Chuyển trang “" + PAGE404 + "”, không lộ dữ liệu phiếu."]),
    ("03", "Chỉ có " + Q1 + ": chỉ xem", "P0", [ACC_X, "PTG-03178 Đã duyệt."], ["1. " + MENU + ".", "2. Bấm PTG-03178."], "—",
     ["- Thấy menu, danh sách 2.285 phiếu (DB dev); KHÔNG có nút Tạo mới.", "- Chi tiết: chân màn Xem giá bán mới, In, In kết quả, Quay lại; không có Sửa / Xóa."]),
    ("04", "Chỉ có " + Q3 + ": chỉ xem", "P0", [ACC_V, "PTG-03178 Đã duyệt."], ["1. " + MENU + "."], "—",
     ["- Thấy menu và danh sách; KHÔNG có nút Tạo mới.", "- Cột Hành động chỉ Xem giá bán mới, In."]),
    ("05", "Có " + Q2 + ": thấy Tạo mới, popup Chọn YCTG", "P0", [ACC_K, Y1], ["1. " + MENU + ".", "2. Bấm Tạo mới."], "—",
     ["- Có nút Tạo mới.", "- Popup “Chọn yêu cầu tính giá” có dòng Y1 kèm nút Chọn.", "- Không có YCTG nào chờ => “Không có yêu cầu tính giá nào đang chờ tính giá”."]),
    ("06", "Có " + Q2 + " nhưng không phải người lập: không Sửa / Xóa", "P0", [ACC_K2, P1],
     ["1. K2 " + MENU[0].lower() + MENU[1:] + ", tìm P1."], "—", ["- Bước 1: P1 không hiện (nháp chỉ người lập thấy)."]),
    ("07", "Có " + Q2 + " ở công ty KHÁC, không có ở công ty 1", "P0",
     ["Tài khoản K4 có " + Q2 + " tại công ty 4, không có quyền nào tại công ty 1; đang chọn công ty 1."],
     ["1. Mở phân hệ Tài chính › Quản lý giá - CTKM.", "2. Mở thẳng Chi tiết PTG-03178."], "—",
     ["- Không có mục “Phiếu tính giá”.", "- Bước 2: trang “" + PAGE404 + "” (quyền phải gán đúng công ty phiếu)."]),
    ("08", "Super admin chưa được gán quyền nào trong 3 quyền", "P1", ["Tài khoản quản trị cao nhất, không được gán 3 quyền tại công ty 1."],
     ["1. Mở phân hệ Tài chính › Quản lý giá - CTKM."], "—", ["- Không có mục “Phiếu tính giá” (không được miễn quyền)."]),
    ("09", "Người lập bị gỡ " + Q2 + " sau khi lập", "P1", [P1, "K bị gỡ " + Q2 + ", còn " + Q3 + "."],
     ["1. K mở Chi tiết P1."], "—", ["- Xem được P1; KHÔNG có Sửa / Xóa / Lưu (cờ thao tác yêu cầu người lập còn " + Q2 + ")."]),
    ("10", "Bỏ qua giao diện: xem danh sách / chi tiết / in khi không có quyền nào", "P0", [ACC_N, "PTG-03178 Đã duyệt."],
     ["1. Dùng công cụ kiểm thử API gọi thẳng xem danh sách PTG.", "2. Gọi thẳng xem chi tiết PTG-03178.", "3. Gọi thẳng In PTG-03178.",
      "4. Gọi thẳng Tạm tính cho hàng của PTG-03178."], "—", ["- Cả 4 bị từ chối, báo “" + NOVIEW + "”; không trả dữ liệu."]),
    ("11", "Bỏ qua giao diện: lập / sửa / xoá PTG khi không có " + Q2, "P0", [ACC_X, Y1, P1],
     ["1. X gọi thẳng chức năng Lưu PTG cho Y1.", "2. X gọi thẳng Sửa P1.", "3. X gọi thẳng Xoá P1.", "4. X gọi thẳng mở khung form Lập của Y1."], "—",
     ["- Bước 1–3: “" + NOPERM + "”.", "- Bước 4: “" + NOCALC + "”.", "- Y1 vẫn Chờ tính giá; P1 không đổi."]),
    ("12", "Bỏ qua giao diện: K2 sửa / xoá / Lưu và duyệt PTG của K", "P0", [ACC_K2, "PTG P2 của K đang Giá bị từ chối; P1 Đang tạo của K."],
     ["1. K2 gọi thẳng Sửa P2.", "2. K2 gọi thẳng Lưu và duyệt P2.", "3. K2 gọi thẳng Xoá P1."], "—",
     ["- Bước 1, 2: “" + CONFLICT + "”; bước 3: “" + NOTFOUND + "” (nháp người khác coi như không có).", "- Giá đang áp dụng không đổi."]),
    ("13", "Bỏ qua giao diện: thao tác PTG của công ty khác", "P0",
     ["Tài khoản K có " + Q2 + " ở cả công ty 1 và 4; đang chọn công ty 1.", "PTG P4 thuộc công ty 4, Đang tạo, do K lập."],
     ["1. Gọi thẳng xem chi tiết P4.", "2. Gọi thẳng Sửa P4.", "3. Gọi thẳng Lưu và duyệt P4."], "—",
     ["- Cả 3: “" + NOTFOUND + "”.", "- Bộ giá công ty 4 không đổi; đổi sang công ty 4 mới thao tác được."]),
    ("14", "Bỏ qua giao diện: không có " + Q3 + " thì máy chủ không trả giá vốn công ty quản lý", "P0",
     [ACC_K, "PTG P5 ở công ty mua có hàng của công ty quản lý TPSG, chính sách “Theo giá vốn”, giá vốn TPSG 450,000."],
     ["1. K gọi thẳng xem chi tiết P5, đọc dữ liệu chính sách.", "2. K gọi thẳng Tạm tính cho hàng đó."], "—",
     ["- Có cách tính, 2 tỷ lệ, Giá bán lẻ TPSG.", "- Giá vốn TPSG và giá mua suy từ giá vốn KHÔNG có trong dữ liệu trả về (trống)."]),
    ("15", "Có " + Q2 + " + " + Q3 + ": đủ thao tác và thấy giá vốn", "P1", [ACC_KV, "Như P5."], ["1. KV mở form Lập / Chi tiết P5.", "2. Bấm Tạm tính."], "—",
     ["- Ô Mã hàng: “Giá vốn TPSG: 450,000”.", "- Popup: 450,000 · 472,500 · 486,000 (5% / 8%)."]),
]

S1 = [
    T(1, "Mở màn từ menu", "P0", [ACC_V], ["1. " + MENU + "."], "—",
      ["- Mục “Phiếu tính giá” đứng ĐẦU nhóm Giá bán (trước Cập nhật giá bán, Duyệt giá bán).", "- Tiêu đề “Phiếu tính giá”.",
       "- Bảng 10 cột: STT, Số phiếu, Yêu cầu tính giá, Yêu cầu hỏi giá, Thương hiệu – Hãng sản xuất, Số mã hàng, Người lập, Ngày lập, Trạng thái, Hành động.",
       "- 10 dòng / trang, mới lập lên trước (DB dev công ty 1: “Hiển thị 1–10 / 2285”)."]),
    T(2, "Lối vào nút Tính giá ở YCTG", "P0", [ACC_K, Y1], ["1. " + MENU_YCTG + ".", "2. Mở Y1, bấm Tính giá.", "3. Bấm Quay lại."], "—",
      ["- Mở form “Lập phiếu tính giá”, Yêu cầu tính giá = Y1, mở sẵn tab Tính giá, 2 khối Thùng / Tuýp.", "- Quay lại về Chi tiết Y1."]),
    T(3, "Lối vào Tạo mới + Chọn", "P0", [ACC_K, Y1], ["1. " + MENU + ".", "2. Bấm Tạo mới, ở dòng Y1 bấm Chọn."], "—",
      ["- Popup đóng, mở form Lập của Y1.", "- Quay lại về danh sách PTG."]),
    T(4, "Lối vào Xem phiếu tính giá ở YCTG", "P1", [ACC_V, "PYCTG-03162 Đã tính giá (PTG-03178)."],
      ["1. " + MENU_YCTG + ".", "2. Mở PYCTG-03162, bấm Xem phiếu tính giá."], "—", ["- Mở Chi tiết PTG-03178."]),
    T(5, "Lối vào thông báo [PTG]", "P1", [ACC_K, ON, "P3 của K Chờ duyệt giá; D duyệt hết dòng."], ["1. K bấm chuông, bấm thông báo mới."], "—",
      ["- Thông báo “[PTG] Đã duyệt: <số P3>. Giá bán đã được áp”.", "- Bấm => Chi tiết P3 (Đã duyệt)."]),
    T(6, "Link số YCTG / YCHG ở danh sách", "P1", [ACC_V], ["1. " + MENU + ".", "2. Dòng PTG-03178 bấm PYCTG-03162; quay lại bấm PYCHG-04283."], "—",
      ["- Mở Chi tiết YCTG PYCTG-03162; rồi Chi tiết YCHG PYCHG-04283."]),
    T(7, "Mở thẳng màn Sửa khi không được sửa", "P1", [ACC_K, "PTG-03178 Đã duyệt."], ["1. Mở thẳng màn Sửa PTG-03178 (link được gửi)."], "—",
      ["- Tự chuyển sang Chi tiết PTG-03178, không có ô nhập mở."]),
    T(8, "Đổi công ty đang làm việc", "P1", [ACC_V + " Đồng thời có " + Q3 + " ở công ty 4."], ["1. " + MENU + ".", "2. Đổi công ty sang 4."], "—",
      ["- Danh sách tải lại theo công ty 4 (DB dev: 674 phiếu); không còn PTG công ty 1."]),
    T(9, "Nháp người khác mở thẳng => trang không tìm thấy", "P0", [ACC_V, "PTG-00215 Đang tạo của người khác."], ["1. Mở thẳng Chi tiết PTG-00215."], "—",
      ["- Trang “" + PAGE404 + "”."]),
]

S2 = [
    T(1, "Tìm nhanh theo số PTG", "P1", [ACC_V], ["1. " + MENU + ".", "2. Gõ “PTG-03178”, nhấn Enter."], "Từ khoá: PTG-03178", ["- Còn 1 dòng PTG-03178."]),
    T(2, "Tìm theo số YCTG / YCHG", "P1", [ACC_V], ["1. Gõ “PYCTG-03162” => Tìm kiếm.", "2. Gõ “PYCHG-04283” => Tìm kiếm."], "—", ["- Cả 2 lần ra PTG-03178."]),
    T(3, "Tìm theo mã / tên hàng", "P1", [ACC_V], ["1. Gõ “MLER-AMAT8574091”.", "2. Gõ “Bộ chuyển đổi USB”."], "—", ["- Ra PTG chứa hàng đó (có PTG-03178)."]),
    T(4, "Lọc Trạng thái", "P0", [ACC_K, P1], ["1. Mở Tìm kiếm nâng cao.", "2. Trạng thái: lần lượt 4 giá trị."], "—",
      ["- Ô có đúng 4 giá trị Đang tạo · Chờ duyệt giá · Giá bị từ chối · Đã duyệt.", "- Đang tạo: chỉ P1 (nháp của K), KHÔNG có PTG-00215.", "- Mỗi lần chọn lọc ngay, về trang 1."]),
    T(5, "Lọc Thương hiệu / Hãng / Người lập", "P1", [ACC_V], ["1. Thương hiệu = MULLER.", "2. Làm mới; Người lập = Nguyễn Thị Minh."], "—",
      ["- Ra đúng phiếu khớp; danh sách lựa chọn xếp A => Z."]),
    T(6, "Lọc Ngày lập trọn ngày", "P1", [ACC_V], ["1. Ngày lập 14/09/2026 => 14/09/2026."], "—", ["- Có PTG-03178 (lập 14/09/2026 17:23)."]),
    T(7, "Làm mới", "P2", [ACC_V], ["1. Đặt từ khoá + 2 ô lọc.", "2. Bấm Làm mới."], "—", ["- Xoá mọi điều kiện, sắp Ngày lập giảm dần, trang 1."]),
    T(8, "Ghi nhớ bộ lọc 10 phút", "P2", [ACC_V], ["1. Lọc Trạng thái Đã duyệt.", "2. Mở 1 phiếu, Quay lại."], "—", ["- Bộ lọc + trạng thái mở khối lọc còn nguyên."]),
    T(9, "Không có kết quả", "P2", [ACC_V], ["1. Gõ “XYZ-KHONG-CO”."], "—", ["- “Không có dữ liệu phù hợp”."]),
]

S3 = [
    T(1, "Sắp theo Số phiếu / Ngày lập", "P1", [ACC_V], ["1. Bấm tiêu đề Số phiếu 2 lần.", "2. Bấm tiêu đề Ngày lập."], "—",
      ["- Tăng / giảm đúng; bỏ sắp => Ngày lập giảm dần; về trang 1."]),
    T(2, "Phân trang và số dòng", "P1", [ACC_V], ["1. Đổi số dòng 20.", "2. Sang trang 2."], "—", ["- “Hiển thị 1–20 / 2285”, đổi số dòng về trang 1; STT liên tục."]),
    T(3, "Cột Số mã hàng đếm mã khác nhau", "P0", [ACC_V], ["1. Xem dòng PTG-01959 và PTG-03170."], "—",
      ["- PTG-01959 (1 hàng 2 ĐVT): 1.", "- PTG-03170: 6."]),
    T(4, "Cột Hành động theo trạng thái", "P0", [ACC_K, P1, "P2 của K Giá bị từ chối; P3 Chờ duyệt giá; PTG-03178 Đã duyệt."],
      ["1. " + MENU + ", xem cột Hành động 4 phiếu."], "—",
      ["- P1: Sửa · Xóa · In.", "- P2: Sửa · In.", "- P3: In.", "- PTG-03178: Xem giá bán mới · In."]),
    T(5, "Cấu hình cột", "P2", [ACC_V], ["1. Bấm Cấu hình cột, bỏ tích Người lập, Lưu.", "2. Bấm Bỏ chọn hết."], "—",
      ["- Bảng mất cột Người lập; giữ khi tải lại.", "- STT, Số phiếu, Hành động luôn tích (khoá); “Đang chọn <n>/10 cột”."]),
]

S4 = [
    T(1, "Form Lập nạp đúng từ YCTG", "P0", [ACC_K, Y1, CUR], ["1. Mở form Lập của Y1."], "—",
      ["- Thông tin chung: YCTG = Y1, YCHG, Thương hiệu – Hãng ENEOS — …, Người hỏi giá, Đơn vị tiền tệ VNĐ (chỉ đọc), Tỉ giá 1 khoá, Công ty tính giá = tên công ty 1, Trạng thái Đang tạo.",
       "- Tab Hàng hoá: Giá NCC Thùng 465,360, Tuýp 19,390 (số XNK đã nhập).", "- Dòng người lập “<K> - <ngày giờ hiện tại>”."]),
    T(2, "Lưu nháp lần đầu", "P0", [ACC_K, Y1, OFF], ["1. Mở form Lập của Y1, nhập Chi phí khác Thùng 34,640.", "2. Bấm Lưu nháp."], "Chi phí khác: 34,640",
      ["- Thông báo “" + SAVED + "”, về danh sách; có dòng mới PTG-xxxxx Đang tạo.", "- Y1 => Đang tính giá; hàng ENEO-124-V5091 => Đang tính giá.",
       "- Giá đang áp dụng ở màn Cập nhật giá bán KHÔNG đổi (796,000).", "- Lịch sử nhóm có “Lập phiếu tính giá”."]),
    T(3, "KTMH sửa số XNK trên PTG không đổi YCTG", "P0", [ACC_K, Y1], ["1. Form Lập: tab Hàng hoá sửa Giá NCC Thùng 470,000; Lưu nháp.", "2. Mở Chi tiết Y1."], "Giá NCC: 470,000",
      ["- PTG lưu 470,000.", "- Y1 vẫn ghi 465,360."]),
    T(4, "Thêm / xoá chi phí ở PTG", "P1", [ACC_K, P1], ["1. Sửa P1, tab Chi phí thêm Phí kiểm định 2%.", "2. Lưu nháp, mở lại."], "Tỉ lệ: 2",
      ["- Thành tiền = 2% × 465,360 = 9,307 (VNĐ, tỉ giá 1); Tổng chi phí + Giá nhập kho tăng tương ứng."]),
    T(5, "Popup Chọn YCTG không xét phân công", "P1", [ACC_K2, Y1, "Y1 do XNK phụ trách hãng ENEOS lập; K2 không liên quan hãng."], ["1. K2 bấm Tạo mới."], "—",
      ["- Popup vẫn có Y1."]),
    T(6, "Popup rỗng", "P1", [ACC_K, "Công ty 1 không có YCTG Chờ tính giá (như DB dev)."], ["1. Bấm Tạo mới."], "—",
      ["- “Không có yêu cầu tính giá nào đang chờ tính giá”; nút Đóng."]),
    T(7, "Popup cuộn ngang ở màn 1440px", "P2", [ACC_K, Y1], ["1. Màn hình rộng 1440px, bấm Tạo mới."], "—",
      ["- Lưu ý: bảng trong popup rộng hơn khung (đo 841px trong 726px) — nút Chọn khuất, phải cuộn ngang mới thấy (ghi nhận lỗi giao diện)."]),
    T(8, "Sửa PTG Đang tạo", "P0", [ACC_K, P1], ["1. Ở danh sách bấm Sửa (bút) P1.", "2. Sửa hệ số Bán lẻ Thùng 1.8, Lưu nháp."], "Hệ số: 1.8",
      ["- Tiêu đề “Sửa phiếu tính giá: <số P1>”.", "- Mở lại: hệ số 1.8, giá 900,000 (khi giá nhập kho 500,000) giữ đúng số đã lưu."]),
    T(9, "Chi tiết PTG Đã duyệt", "P0", [ACC_V, "PTG-03178."], ["1. Bấm PTG-03178."], "—",
      ["- Tiêu đề “Chi tiết phiếu tính giá: PTG-03178”; banner xám “Nhóm hàng đã kết thúc (Đã tính giá) — phiếu tính giá chỉ còn xem.”.",
       "- Tỉ giá 31,900; EURO; mở tab Hàng hoá; mọi ô khoá.", "- Chân màn: Xem giá bán mới · In · In kết quả · Quay lại."]),
    T(10, "Khối Lịch sử của nhóm", "P1", [ACC_V, "PTG-03178."], ["1. Cuộn xuống khối Lịch sử."], "—",
      ["- 4 cột Người thực hiện · Hành động · Nội dung · Thời gian, mới => cũ.", "- Có “Duyệt tính giá” 14/09/2026 17:23, “Lập yêu cầu tính giá”, “XNK duyệt”, “PTKD duyệt”."]),
    T(11, "Xoá PTG Đang tạo", "P0", [ACC_K, P1, "Hàng của P1 không nằm trong PTG dở nào khác."], ["1. Bấm Xóa ở dòng P1.", "2. Bấm Xóa trong hộp xác nhận."], "—",
      ["- Hộp “Xác nhận xóa”: “Xóa phiếu tính giá <số P1>? Yêu cầu tính giá sẽ về \"Chờ tính giá\".”.", "- “Đã xoá phiếu tính giá”; P1 biến mất.",
       "- Y1 => Chờ tính giá (nút Tính giá hiện lại); hàng => Chờ tính giá bán; lịch sử nhóm “Xoá phiếu tính giá”."]),
    T(12, "Hủy xoá", "P2", [ACC_K, P1], ["1. Bấm Xóa, bấm Hủy."], "—", ["- P1 còn nguyên."]),
    T(13, "Xoá: hàng còn trong PTG dở khác giữ Đang tính giá", "P1", [ACC_K, P1, "Hàng H nằm trong P1 và trong P6 (Chờ duyệt giá) cùng công ty."],
      ["1. Xoá P1."], "—", ["- Hàng H vẫn Đang tính giá (vì còn ở P6)."]),
    T(14, "Không xoá được PTG đã gửi", "P0", [ACC_K, "P2 Giá bị từ chối, P3 Chờ duyệt giá của K."], ["1. Xem cột Hành động / chân Chi tiết P2, P3."], "—",
      ["- Không có nút Xóa."]),
    T(15, "Rời form chưa lưu", "P1", [ACC_K, Y1], ["1. Form Lập, sửa Chi phí khác 1000.", "2. Bấm Quay lại.", "3. Bấm Ở lại; rồi Quay lại => Thoát."], "—",
      ["- Hộp “Thông tin chưa lưu”: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”.", "- Ở lại giữ số; Thoát về danh sách, không lưu."]),
    T(16, "Xem giá bán mới", "P0", [ACC_V, "PTG-03178."], ["1. Bấm Xem giá bán mới (nhãn giá)."], "—",
      ["- Mở Chi tiết PYCHG-04283, bung kết quả nhóm MULLER: “Giá bán mới áp ngày 14/09/2026 · Nguyễn Thị Minh … · PTG-03178”.",
       "- ĐVT Bộ: Bán lẻ / Theo lô / Đại lý cấp 1–3 22,500,000 ĐMGG 5%; TMĐT 29,250,000 ĐMGG 0%."]),
    T(17, "Không có Xem giá bán mới khi chưa Đã duyệt", "P1", [ACC_K, P1], ["1. Xem dòng / chân Chi tiết P1."], "—", ["- Không có nút Xem giá bán mới, In kết quả."]),
]

S5 = [
    T(1, "Lưu và duyệt — công ty tắt duyệt", "P0", [ACC_K, Y1, CUR, OFF], ["1. Form Lập Y1, Chi phí khác Thùng 34,640, hệ số Bán lẻ Thùng 1.8.", "2. Bấm Lưu và duyệt, xác nhận."],
      ["Chi phí khác: 34,640", "Hệ số Bán lẻ: 1.8"],
      ["- Hộp “Lưu và duyệt”: “Duyệt phiếu tính giá mới? Giá bán áp ngay cho <tên công ty 1>, hàng mới sang Đang kinh doanh.”.",
       "- “" + APPLIED + "”; PTG Đã duyệt; Y1 Đã tính giá; nhóm Đã tính giá.", "- Hàng ENEO-124-V5091 => Đang kinh doanh (cả 2 ĐVT đã xong)."]),
    T(2, "Nút và dòng nhắc theo quy chế", "P0", [ACC_K, Y1], ["1. Với " + OFF + " mở form Lập.", "2. Bật quy chế (" + ON + "), mở lại."], "—",
      ["- Tắt: nút “Lưu và duyệt” (dấu tích), dòng nhắc “Lưu và duyệt sẽ áp giá ngay cho <công ty 1>”.",
       "- Bật: nhãn tím “Bật quy chế duyệt giá”, nút “Lưu và gửi duyệt”, dòng nhắc “<công ty 1> bật quy chế duyệt giá — giá sẽ gửi sang màn Duyệt giá bán”."]),
    T(3, "Quy chế theo danh sách hãng", "P1", [ACC_K, Y1, "Công ty 1 bật duyệt giá, KHÔNG áp mọi hãng, danh sách hãng không có hãng của ENEOS."], ["1. Mở form Lập Y1."], "—",
      ["- Nút “Lưu và duyệt” (hãng không phải duyệt)."]),
    T(4, "Lưu và gửi duyệt — công ty bật duyệt", "P0", [ACC_K, ACC_D, Y1, CUR, ON], ["1. Form Lập Y1, hệ số Bán lẻ Thùng 1.8, Tuýp 1.2.", "2. Bấm Lưu và gửi duyệt, xác nhận."], "—",
      ["- Hộp: “Gửi giá của phiếu tính giá mới sang màn Duyệt giá bán của <công ty 1>?”.", "- “" + SUBMITTED + "”; PTG Chờ duyệt giá; Y1 Chờ duyệt giá.",
       "- D nhận “[GIA] Chờ duyệt: <số PTG>. 2 dòng giá. Người đề nghị: <K>”; màn Duyệt giá bán có 2 yêu cầu Thùng / Tuýp.",
       "- Giá đang áp dụng chưa đổi; hàng vẫn Đang tính giá."]),
    T(5, "Chi tiết PTG Chờ duyệt giá", "P0", [ACC_K, "PTG P3 Chờ duyệt giá."], ["1. Mở Chi tiết P3."], "—",
      ["- Banner tím “Giá đang chờ duyệt ở màn Duyệt giá bán của <công ty 1> — hàng sang Đang kinh doanh và có kết quả tính giá khi mọi dòng giá được duyệt.”.",
       "- Mở tab Tính giá; cột Kết quả duyệt “Chờ duyệt”.", "- Chân màn chỉ In, Quay lại (không Sửa / Xóa)."]),
    T(6, "Duyệt hết dòng => PTG Đã duyệt", "P0", [ACC_D, ACC_K, "P3 Chờ duyệt giá 2 dòng."], ["1. " + MENU_DUYET + ", D duyệt 2 dòng của P3.", "2. K mở P3."], "—",
      ["- P3 Đã duyệt; cột Kết quả duyệt “Đã duyệt” 2 dòng; có Xem giá bán mới.", "- K nhận “[PTG] Đã duyệt: <số P3>. Giá bán đã được áp”.",
       "- Người lập YCHG + XNK nhận “[YCHG] Đã duyệt …”.", "- Hàng => Đang kinh doanh."]),
    T(7, "Duyệt 1 dòng, còn 1 dòng chờ", "P1", [ACC_D, "P3 Chờ duyệt giá 2 dòng."], ["1. D duyệt dòng Thùng."], "—",
      ["- P3 vẫn Chờ duyệt giá; Thùng “Đã duyệt”, Tuýp “Chờ duyệt”.", "- Hàng vẫn Đang tính giá (chưa đủ mọi ĐVT)."]),
    T(8, "Không duyệt => Giá bị từ chối", "P0", [ACC_D, ACC_K, "P3 Chờ duyệt giá 2 dòng."], ["1. D duyệt Thùng, Không duyệt Tuýp lý do “Giá Đại lý cấp 1 thấp”.", "2. K mở P3."], "—",
      ["- P3 Giá bị từ chối; Y1 Đang tính giá.", "- Banner vàng “Giá bị từ chối ở màn Duyệt giá bán: Giá Đại lý cấp 1 thấp. Sửa các dòng bị từ chối rồi Lưu và gửi duyệt lại — dòng đã duyệt giữ nguyên.”.",
       "- K nhận “[PTG] Từ chối: <số P3>. Lý do: Giá Đại lý cấp 1 thấp”; lịch sử nhóm “Giá bị từ chối”."]),
    T(9, "Gửi lại chỉ dòng bị từ chối", "P0", [ACC_K, "P3 Giá bị từ chối: Thùng Đã duyệt, Tuýp Bị từ chối."], ["1. Sửa P3.", "2. Sửa hệ số Tuýp, Lưu và gửi duyệt."], "—",
      ["- Chỉ khối Tuýp mở ô nhập; khối Thùng + Tỉ giá khoá.", "- Chỉ 1 yêu cầu mới ở màn Duyệt giá bán (Tuýp); thông báo “… 1 dòng giá …”.", "- P3 Chờ duyệt giá; giá Thùng đã áp giữ nguyên."]),
    T(10, "Gửi duyệt khi giá trùng giá đang áp dụng", "P1", [ACC_K, Y1, ON, "Không sửa hệ số / giá (hệ số đang áp dụng, giá công thức trùng giá đang áp dụng)."],
      ["1. Lưu và gửi duyệt."], "—", ["- Dòng không sinh yêu cầu, coi như Đã duyệt ngay; mọi dòng trùng => PTG Đã duyệt, thông báo “" + APPLIED + "”."]),
    T(11, "Lưu nháp PTG Giá bị từ chối", "P1", [ACC_K, "P3 Giá bị từ chối."], ["1. Sửa dòng bị từ chối, Lưu nháp."], "—", ["- “" + SAVED + "”; P3 vẫn Giá bị từ chối."]),
    T(12, "Nhóm đã đóng chỉ còn xem", "P1", [ACC_K, "P7 Đang tạo của K; nhóm của P7 bị Huỷ duyệt ở YCHG."], ["1. Mở Chi tiết P7.", "2. Gọi thẳng Lưu P7 (tester kỹ thuật)."], "—",
      ["- Banner “Nhóm hàng đã kết thúc (Huỷ duyệt) — phiếu tính giá chỉ còn xem.”; không Sửa / Xóa.", "- Bước 2: “" + CLOSED + "”."]),
    T(13, "Lưu và duyệt ghi lịch sử", "P1", [ACC_K, Y1, OFF], ["1. Lưu và duyệt.", "2. Mở Chi tiết."], "—", ["- Lịch sử nhóm: “Lập phiếu tính giá”, “Duyệt tính giá”, nội dung có số PTG."]),
    T(14, "Tự duyệt không tự báo cho mình", "P2", [ACC_K, Y1, OFF], ["1. K Lưu và duyệt.", "2. K mở chuông."], "—", ["- K KHÔNG nhận “[PTG] Đã duyệt” cho phiếu mình vừa tự duyệt."]),
]

S6 = [
    T(1, "Giá nhập kho = sau thuế + chi phí + chi phí khác", "P0", [ACC_V, "PTG-03178."], ["1. Chi tiết PTG-03178, tab Tính giá."], "—",
      ["- Đơn giá VNĐ 10,080,400 (316 × 31,900); Sau thuế 11,088,440 (thuế 10%).", "- Tổng chi phí 2,020,227 (1,512,060 + 504,020 + 4,147); Chi phí khác 0.",
       "- Giá nhập kho 13,108,667."]),
    T(2, "Hệ số mặc định = hệ số đang áp dụng", "P0", [ACC_K, Y1, CUR], ["1. Mở form Lập Y1, tab Tính giá."], "—",
      ["- Thùng: hệ số 1.61 cho Bán lẻ; Giá bán gợi ý 749,200 (= tròn trăm 1,61 × 465,360 = 749,229.6); Giá công thức 749,230.",
       "- Tuýp: hệ số 1 => 19,400 (tròn trăm 19,390).", "- “Đang áp dụng: 796,000” / “34,000” ở cột Ngày hiệu lực."]),
    T(3, "Chi phí khác đổi giá nhập kho và giá bán", "P0", [ACC_K, Y1, CUR], ["1. Nhập Chi phí khác Thùng 34,640."], "Chi phí khác: 34,640",
      ["- Giá nhập kho 500,000.", "- Giá bán chưa gõ tay = 1,61 × 500,000 = 805,000 cho 5 loại."]),
    T(4, "Hệ số => giá tròn trăm", "P0", [ACC_K, Y1], ["1. Giá nhập kho Thùng 500,000; nhập hệ số Bán lẻ 1.8."], "Hệ số: 1.8",
      ["- Giá bán Bán lẻ 900,000; Giá công thức 900,000."]),
    T(5, "Bán lẻ lan 4 loại", "P0", [ACC_K, Y1], ["1. Nhập hệ số Bán lẻ 1.8."], "—",
      ["- Giá bán theo lô, Đại lý cấp 1, 2, 3: hệ số 1.8, giá 900,000.", "- Sửa riêng Đại lý cấp 1 sau đó => chỉ Đại lý cấp 1 đổi."]),
    T(6, "TMĐT theo Bán lẻ × hệ số TMĐT", "P0", [ACC_K, Y1, "Hệ số TMĐT công ty 1 = 1,3."], ["1. Bán lẻ Thùng 900,000 hệ số 1.8."], "—",
      ["- TMĐT: hệ số 2.34, Giá bán 1,170,000, ĐMGG 0; 3 ô khoá; dòng phụ “= Bán lẻ × 1.3”.", "- Tuýp Bán lẻ 19,400 => TMĐT 25,220; Giá công thức TMĐT tròn nghìn 25,000."]),
    T(7, "Giá gõ tay giữ nguyên khi giá nhập kho đổi", "P0", [ACC_K, Y1], ["1. Gõ Giá bán Bán lẻ Thùng 950,000.", "2. Đổi Chi phí khác 50,000."], "—",
      ["- Bán lẻ (và 4 loại lan theo) giữ 950,000; Giá nhập kho + Giá công thức đổi.", "- Gõ lại hệ số 1.8 => giá về công thức."]),
    T(8, "Mở lại PTG giữ giá đã chốt", "P1", [ACC_K, P1, "P1 đã lưu Bán lẻ Thùng 950,000."], ["1. Sửa P1, đổi Chi phí khác."], "—",
      ["- Bán lẻ vẫn 950,000 (giá đã lưu không chạy lại theo hệ số)."]),
    T(9, "Máy chủ tính lại TMĐT, không tin số gửi lên", "P0", [ACC_K, P1], ["1. Tester kỹ thuật gọi thẳng Lưu P1 gửi TMĐT giá 1 đồng, hệ số 9."], "—",
      ["- TMĐT lưu = round(Bán lẻ × 1,3), hệ số = hệ số Bán lẻ × 1,3, ĐMGG 0 — bỏ số gửi lên."]),
    T(10, "Máy chủ tính lại giá nhập kho", "P0", [ACC_K, P1], ["1. Gọi thẳng Lưu P1 gửi kèm Giá nhập kho 1 đồng."], "—",
      ["- Giá nhập kho lưu đúng công thức (bỏ số gửi lên)."]),
    T(11, "Giá hiệu lực — hệ số => giá tròn đồng", "P0", [ACC_K, Y1], ["1. Giá nhập kho Thùng 500,000; bấm + Giá hiệu lực ở Bán lẻ.", "2. Nhập hệ số 1.83, ngày mai."], "Hệ số: 1.83",
      ["- Giá hiệu lực = 915,000 (1,83 × 500,000, làm tròn ĐỒNG).", "- TMĐT có dòng “giá sẽ áp dụng” chỉ đọc 1,189,500 / 2.38, cùng ngày."]),
    T(12, "Giá hiệu lực ghi vào công ty khi áp", "P0", [ACC_K, Y1, OFF, "Bán lẻ Thùng có giá hiệu lực 915,000 ngày 31/10/2026."], ["1. Lưu và duyệt.", "2. " + MENU_CNGB + ", mở hàng, ĐVT Thùng."], "—",
      ["- Bán lẻ hiện tại 900,000; có giá hiệu lực 915,000 từ 31/10/2026; TMĐT hiệu lực 1,189,500."]),
    T(13, "Lưu và duyệt ghi bộ giá + giá vốn công ty phiếu", "P0", [ACC_K, Y1, OFF, "Giá nhập kho Thùng 500,000, Bán lẻ 900,000; Tuýp 19,390 / 19,400."],
      ["1. Lưu và duyệt.", "2. " + MENU_CNGB + " (công ty 1), mở ENEO-124-V5091."], "—",
      ["- Thùng: 5 loại 900,000 hệ số 1.8, TMĐT 1,170,000; Giá vốn 500,000; Lý do sửa giá “Phiếu tính giá <số PTG>”.",
       "- Tuýp: 19,400 / TMĐT 25,220; Giá vốn 19,390.", "- Lịch sử giá có 1 dòng / ĐVT."]),
    T(14, "Không đụng công ty khác", "P0", [ACC_K, Y1, OFF, "Hàng có bộ giá ở công ty 4: Thùng Bán lẻ 800,000."], ["1. Lưu và duyệt ở công ty 1.", "2. Xem giá ở công ty 4."], "—",
      ["- Công ty 4 vẫn 800,000, không có dòng lịch sử mới."]),
    T(15, "Gửi duyệt: giá vốn đề nghị = giá nhập kho, giá đang áp dụng chưa đổi", "P0", [ACC_K, ACC_D, Y1, ON], ["1. Lưu và gửi duyệt.", "2. " + MENU_DUYET + "."], "—",
      ["- Yêu cầu Thùng: giá vốn đề nghị 500,000, Bán lẻ đề nghị 900,000, lý do “Phiếu tính giá <số>”.", "- Màn Cập nhật giá bán: Bán lẻ hiện tại vẫn 796,000."]),
    T(16, "Người duyệt sửa giá => PTG chép giá thực áp", "P0", [ACC_D, "P3 Chờ duyệt giá, Thùng đề nghị 900,000."], ["1. D sửa Bán lẻ Thùng 880,000 rồi Duyệt.", "2. Mở Chi tiết P3."], "—",
      ["- Dòng Thùng trên P3 hiện Bán lẻ 880,000 (giá thực áp), không phải 900,000.", "- Kết quả tính giá / Xem giá bán mới hiện 880,000."]),
    T(17, "Giá vốn công ty quản lý theo quyền " + Q3, "P0", ["Hàng H của công ty TPSG, công ty 1 có chính sách Theo giá vốn: Nhập khẩu 5%, Tồn kho 8%, giá vốn TPSG 450,000.", ACC_K, ACC_KV],
      ["1. K mở form Lập có hàng H, xem ô Mã hàng.", "2. KV mở cùng form."], "—",
      ["- K: “Theo giá vốn · Nhập khẩu 5% · Tồn kho 8%”, “Giá vốn TPSG: —”, “Giá bán lẻ: <số>”.", "- KV: “Giá vốn TPSG: 450,000”."]),
    T(18, "Tạm tính Theo giá vốn", "P0", [ACC_KV, "Như ca trên."], ["1. Bấm Tạm tính."], "—",
      ["- Popup “Tạm tính giá mua từ công ty quản lý”: 450,000 · 472,500 · 486,000.", "- “Số tạm tính để tham khảo — làm tròn trăm đồng, không ghi vào bảng giá.”",
       "- Người thiếu " + Q3 + ": 3 ô “—”."]),
    T(19, "Tạm tính Theo giá bán", "P1", ["Chính sách Theo giá bán TPSG 5% / 8%; Bán lẻ TPSG 796,000.", ACC_K], ["1. Bấm Tạm tính."], "—",
      ["- 6 dòng loại giá; Bán lẻ 796,000 => 756,200 / 732,300; hiện cho mọi người có quyền xem."]),
    T(20, "Tạm tính không ghi bảng giá", "P1", [ACC_KV], ["1. Mở Tạm tính, Đóng.", "2. Xem giá ĐVT ở màn Cập nhật giá bán."], "—", ["- Không đổi gì."]),
    T(21, "Hàng của chính công ty / chưa cấu hình", "P2", [ACC_K], ["1. Xem ô Mã hàng hàng TPE; hàng công ty khác chưa cấu hình."], "—",
      ["- “Hàng hoá của TPE — không có giá mua nội bộ” (không có link Tạm tính).", "- Nhãn cam “Chưa cấu hình” + “<mã cty> chưa khai chính sách cho hãng này”."]),
    T(22, "Giá nhập kho không bị che theo " + Q3, "P1", [ACC_X, "PTG-03178."], ["1. X mở Chi tiết, tab Tính giá; bấm In."], "—",
      ["- Thấy Giá nhập kho 13,108,667 và cột Giá nhập kho trên bản in.", "- Lưu ý: số này thành giá vốn công ty phiếu khi áp — ghi nhận để nghiệp vụ xác nhận có cần che theo " + Q3 + " không."]),
    T(23, "Chi tiết tính lại chi phí theo tỉ lệ (phiếu ERP cũ)", "P2", [ACC_V, "PTG-03178 (Bảo hiểm 0,04%)."], ["1. Tab Chi phí."], "—",
      ["- Bảo hiểm 4,147 (tính lại) trong khi giá vốn đã áp 13,108,986 (ERP lưu 4,466) — ghi nhận lệch, không phải lỗi thao tác."]),
]

S7 = [
    T(1, "In phiếu tính giá", "P0", [ACC_V, "PTG-03178."], ["1. Ở dòng PTG-03178 bấm In (máy in)."], "—",
      ["- Popup “Xem trước phiếu tính giá PTG-03178”.", "- “PHIẾU TÍNH GIÁ”, Số phiếu, Ngày tạo 14/09/2026; Yêu cầu tính giá PYCTG-03162, Yêu cầu hỏi giá PYCHG-04283, Tiền tệ / tỉ giá EURO / 31,900, Ghi chú “.....”.",
       "- Bảng 11 cột: … Giá NCC (EURO) 316 · Đơn giá VNĐ 10,080,400 · Thuế NK 10 · Sau thuế 11,088,440 · Chi phí 2,020,227 · Giá nhập kho 13,108,667 · Giá bán lẻ 22,500,000.",
       "- Khối ký Người lập · Người duyệt; không có giá vốn công ty quản lý."]),
    T(2, "In kết quả", "P0", [ACC_V, "PTG-03178."], ["1. Chi tiết PTG-03178 bấm In kết quả."], "—",
      ["- “KẾT QUẢ TÍNH GIÁ”: Phiếu tính giá PTG-03178, Ngày áp giá 14/09/2026.", "- 6 dòng: Bán lẻ, Giá bán theo lô, Đại lý cấp 1–3 22,500,000 ĐMGG 5; Thương mại điện tử 29,250,000 ĐMGG 0.",
       "- Khối ký Người tính giá."]),
    T(3, "In kết quả khi chưa có kết quả", "P1", [ACC_K, P1], ["1. Gọi thẳng In kết quả P1 (tester kỹ thuật)."], "—", ["- “Phiếu tính giá chưa có kết quả”."]),
    T(4, "In PTG Đang tạo của mình", "P2", [ACC_K, P1], ["1. Bấm In ở dòng P1."], "—", ["- Bản in Trạng thái “Đang tạo”."]),
]

S8 = [
    T(1, "Lưu và duyệt khi trống — báo đồng thời", "P0", [ACC_K, ON, "Y1 có Giá NCC trống ở cả 2 ĐVT; hệ số trống."], ["1. Bấm Lưu và gửi duyệt."], "—",
      ["- 22 lỗi cùng lúc: 2 ô Giá NCC + 10 ô Hệ số + 10 ô Giá bán “" + REQ + "”.", "- Tab Hàng hoá, Tính giá gắn chấm đỏ; tự chuyển tab Hàng hoá; không gửi gì lên máy chủ."]),
    T(2, "Lưu nháp cho phép để trống", "P0", [ACC_K, "Như ca trên."], ["1. Bấm Lưu nháp."], "—", ["- Lưu được, “" + SAVED + "”."]),
    T(3, "Giá NCC / Giá bán = 0 khi gửi", "P0", [ACC_K, Y1], ["1. Giá NCC Thùng 0, Giá bán Đại lý cấp 3 = 0; Lưu và duyệt."], "—", ["- 2 ô báo “Phải lớn hơn 0”."]),
    T(4, "Hệ số ngoài khoảng", "P1", [ACC_K, Y1], ["1. Hệ số Bán lẻ 100.", "2. Hệ số -1 (gọi thẳng)."], "—", ["- “Phải từ 0 đến dưới 100”."]),
    T(5, "ĐMGG ngoài 0–100", "P1", [ACC_K, Y1], ["1. ĐMGG Bán lẻ 120, Lưu nháp."], "ĐMGG: 120", ["- “Phải từ 0 đến 100”, không tự kẹp."]),
    T(6, "Tỉ giá", "P1", [ACC_K, "YCTG Y8 tiền tệ USD Chờ tính giá."], ["1. Xoá tỉ giá, Lưu nháp.", "2. Tỉ giá 0.", "3. Tỉ giá 1,000,000,000,000."], "—",
      ["- “" + REQ + "” · “Phải lớn hơn 0” · “Không hợp lệ” (máy chủ: “Không được lớn hơn 999,999,999,999.”)."]),
    T(7, "Tỉ giá khoá khi VNĐ / Giá bị từ chối", "P1", [ACC_K, Y1, "P3 Giá bị từ chối (USD)."], ["1. Form Lập Y1 (VNĐ).", "2. Sửa P3."], "—", ["- Ô Tỉ giá khoá ở cả 2 trường hợp."]),
    T(8, "Ghi chú > 255 / ghi chú dòng > 1000", "P2", [ACC_K, Y1], ["1. Ghi chú 256 ký tự; ghi chú dòng 1001 ký tự; Lưu nháp."], "—",
      ["- “Vui lòng nhập tối đa 255 ký tự.” / “Vui lòng nhập tối đa 1000 ký tự.”"]),
    T(9, "Chi phí khác âm / giá nhập kho quá lớn", "P2", [ACC_K, Y1], ["1. Gọi thẳng Lưu với Chi phí khác -1.", "2. Chi phí khác 999,999,999,999."], "—",
      ["- “Không hợp lệ”.", "- “Giá nhập kho vượt giới hạn lưu trữ”."]),
    T(10, "Chi phí trùng / tỉ lệ sai", "P1", [ACC_K, Y1], ["1. Tab Chi phí: 2 dòng Bảo hiểm hàng hóa; Tỉ lệ 101; Lưu nháp."], "—",
      ["- “Chi phí đã có trong dòng này”; “Phải từ 0 đến 100”."]),
    T(11, "Giá hiệu lực thiếu ngày / ngày quá khứ", "P0", [ACC_K, Y1], ["1. + Giá hiệu lực ở Bán lẻ, không chọn ngày, Lưu và duyệt.", "2. Gọi thẳng với ngày hôm nay."], "—",
      ["- “Bắt buộc phải chọn”, tab Tính giá chấm đỏ.", "- “Phải chọn ngày tương lai”; ô chọn ngày không cho chọn hôm nay trở về trước."]),
    T(12, "Hơn 1 giá hiệu lực / hệ số hiệu lực > 99", "P2", [ACC_K, Y1], ["1. Gọi thẳng gửi 2 giá hiệu lực cho Bán lẻ.", "2. Hệ số hiệu lực 120."], "—",
      ["- “Chỉ được 1 giá hiệu lực”; “Phải từ 0 đến 99”."]),
    T(13, "Chặn chéo: yêu cầu duyệt mở từ Cập nhật giá bán", "P0", [ACC_K, Y1, "Thùng đang có yêu cầu duyệt mở ở màn Cập nhật giá bán."], ["1. Lưu và duyệt."], "—",
      ["- Dưới ô Mã hàng khối Thùng: “" + PEND_G4 + "”; không ghi dòng nào (kể cả Tuýp)."]),
    T(14, "Chặn chéo: giá đang chờ duyệt ở PTG khác", "P0", [ACC_K, "Tuýp đang có yêu cầu duyệt mở của PTG P3."], ["1. Lưu và gửi duyệt PTG khác có Tuýp."], "—",
      ["- “Giá đang chờ duyệt ở <số P3>”; màn Cập nhật giá bán cũng không lưu được Tuýp: “Giá đang chờ duyệt ở <số P3>.”"]),
    T(15, "Lỗi máy chủ báo dưới ô, giữ dữ liệu", "P1", [ACC_K, "Như ca 13."], ["1. Lưu và duyệt, xem form sau lỗi."], "—",
      ["- Form không đóng, số đã nhập còn nguyên; tự chuyển tab Tính giá và cuộn tới lỗi."]),
    T(16, "TMĐT hiện 2 dòng giá hiệu lực (ghi nhận lỗi)", "P1", [ACC_K, "PTG đã lưu có giá hiệu lực Bán lẻ (vd PTG-02618)."], ["1. Mở Sửa / Chi tiết, tab Tính giá, khối TMĐT."], "—",
      ["- Mong đợi: TMĐT chỉ 1 dòng “giá sẽ áp dụng” chỉ đọc.", "- Thực tế đang thấy 2 dòng, dòng đầu nhập được nhưng máy chủ bỏ qua số nhập — báo lỗi nếu còn."]),
]

S9 = [
    T(1, "Công ty phiếu = công ty YCTG", "P0", [ACC_K + " Đồng thời có " + Q2 + " ở công ty 4.", "Y1 ở công ty 1."], ["1. Lập PTG khi đang chọn công ty 1.", "2. Đổi sang công ty 4, mở danh sách."], "—",
      ["- PTG thuộc công ty 1 (“Công ty tính giá” = công ty 1); không hiện ở công ty 4."]),
    T(2, "2 KTMH cùng lập cho 1 YCTG", "P0", [ACC_K, ACC_K2, Y1], ["1. K và K2 cùng mở form Lập Y1.", "2. K Lưu nháp trước, K2 Lưu nháp sau."], "—",
      ["- K thành công; K2 nhận “" + CONFLICT + "”, về danh sách; Y1 chỉ có 1 PTG."]),
    T(3, "XNK sửa YCTG khi KTMH đang lập", "P1", [ACC_K, Y1], ["1. K mở form Lập; XNK cùng lúc thao tác làm Y1 không còn Chờ tính giá.", "2. K Lưu nháp."], "—",
      ["- “" + CONFLICT + "”."]),
    T(4, "Xoá khi phiếu vừa được gửi ở tab khác", "P1", [ACC_K, P1], ["1. Mở P1 ở 2 tab; tab 1 Lưu và gửi duyệt; tab 2 bấm Xóa."], "—", ["- “" + CONFLICT + "”; P1 không bị xoá."]),
    T(5, "Duyệt và sửa PTG cùng lúc", "P2", [ACC_D, ACC_K, "P3 Chờ duyệt giá."], ["1. K gọi thẳng Sửa P3 trong lúc D duyệt."], "—", ["- K nhận “" + CONFLICT + "” (Chờ duyệt giá không sửa được)."]),
    T(6, "Bộ lọc không lộ phiếu nháp người khác", "P2", [ACC_V, "PTG-00215 nháp người khác."], ["1. Lọc Trạng thái Đang tạo."], "—", ["- Không có PTG-00215."]),
]

S10 = [
    T(1, "Luồng đủ — công ty tắt duyệt", "P0", ["Tài khoản sale S, XNK X (phân công ENEOS), KTMH K; " + OFF, "Hàng mới H Chờ tính giá bán."],
      ["1. S lập YCHG có H, PTKD duyệt; X duyệt nhóm, lập YCTG, gửi.", "2. K bấm Tính giá ở YCTG, nhập hệ số, Lưu và duyệt.", "3. S mở YCHG, xem Chi tiết kết quả."], "—",
      ["- PTG Đã duyệt, YCTG Đã tính giá, nhóm Đã tính giá, YCHG Đã tính giá (1/1 nhóm).", "- H Đang kinh doanh, có đủ 6 loại giá ở công ty phiếu; S, X nhận “[YCHG] Đã duyệt …”.",
       "- Kết quả tính giá khớp giá đã áp."]),
    T(2, "Luồng đủ — công ty bật duyệt, có từ chối rồi gửi lại", "P0", [ON, "Như ca trên + D có " + QD + "."],
      ["1. K Lưu và gửi duyệt.", "2. D Không duyệt 1 dòng.", "3. K sửa dòng đó, gửi lại.", "4. D duyệt."], "—",
      ["- Trạng thái PTG: Chờ duyệt giá => Giá bị từ chối => Chờ duyệt giá => Đã duyệt; YCTG: Chờ duyệt giá => Đang tính giá => Chờ duyệt giá => Đã tính giá.",
       "- K nhận lần lượt “[PTG] Từ chối …”, “[PTG] Đã duyệt …”; D nhận 2 lần “[GIA] Chờ duyệt …” (lần 2: 1 dòng giá)."]),
    T(3, "Xoá nháp rồi lập lại", "P1", [ACC_K, Y1], ["1. Lập P1 Lưu nháp.", "2. Xoá P1.", "3. Bấm Tính giá ở Y1 lần nữa."], "—",
      ["- Y1 về Chờ tính giá rồi lập lại được PTG mới (số mới, không dùng lại số cũ)."]),
]


def _norm(tc):
    return tuple(L(*x) if isinstance(x, list) else x for x in tc)


ROLE_TCS = [_norm(tc) for tc in ROLE_TCS]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP (MENU, LỐI VÀO TỪ YCTG, THÔNG BÁO, LINK)", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "CHỨC NĂNG CHÍNH (LẬP / CHỌN YCTG / SỬA / XEM / XOÁ / XEM GIÁ BÁN MỚI)", S4),
    ("V", "THAO TÁC TRẠNG THÁI (LƯU VÀ DUYỆT, GỬI DUYỆT, KẾT QUẢ DUYỆT, GỬI LẠI, NHÓM ĐÓNG)", S5),
    ("VI", "GIÁ — GIÁ NHẬP KHO, GIÁ BÁN 6 LOẠI, GIÁ HIỆU LỰC, GHI BỘ GIÁ, GIÁ VỐN THEO QUYỀN", S6),
    ("VII", "IN PHIẾU / IN KẾT QUẢ", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", S8),
    ("IX", "CÔ LẬP DỮ LIỆU THEO CÔNG TY & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "E2E FLOW", S10),
]

_all = "\n".join("\n".join(map(str, x)) for x in DESCRIPTION_BLOCK + ROLE_TCS + [t for _, _, s in SECTIONS for t in s])
_bad = re.findall(r"[←-⯿\U0001F300-\U0001FAFF]", _all)
assert not _bad, "Con ky tu cam: %s" % sorted(set(_bad))

build(output_file=OUT, sheet_name="Trang tính1", feature_name="Phiếu tính giá",
      module_name="Phiếu tính giá", description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
print("OK ->", OUT)
