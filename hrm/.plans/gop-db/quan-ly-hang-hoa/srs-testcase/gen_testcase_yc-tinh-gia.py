# -*- coding: utf-8 -*-
"""Sinh testcase - Yeu cau tinh gia (luong Chuyen doi hang hoa, man 4/5).

Doi chieu code worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa (hrm-api 39c4a91fe,
hrm-client 5c14659e8 — 16/10/2026). SRS cung bo: gen_srs_yc-tinh-gia.py.
Section VI danh rieng cho GIA (cong thuc so tien, may chu tinh lai, gia von o cot Chinh sach theo quyen Xem gia von, gia ban moi
chi gia ban). So lieu mau lay tu DB dev hrm_erp_giacty Cty 1: PYCTG-03162 (Da tinh gia, EURO 30,927.74, MLER-AMAT8574091 Bo,
Gia NCC 316, thue 10%, 3 chi phi, PTG-03178, Ban le 22,500,000 DMGG 5, TMDT 29,250,000), PYCTG-01939 (ENEOS 2 DVT Thung / Tuyp),
PYCTG-02786 (Khong duyet, nhom Dang tinh gia), PYCTG-01403 (Khong duyet, nhom Huy duyet), PYCTG-00177 (Dang tinh gia, PTG nhap
nguoi khac), PYCTG-02874 (Dang tao cua nguoi khac), nhom CARLEO PYCHG-04223 / BESITA PYCHG-04282 Cho lap YCTG; USD 26,180.
DB dev KHONG co YCTG Cho tinh gia / Cho duyet gia — tester tu tao theo tien dieu kien.
Chay: python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_testcase_yc-tinh-gia.py
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

OUT = os.path.join(HERE, "testcase - Yêu cầu tính giá.xlsx")


def L(*lines):
    return "\n".join(lines)


def T(n, func, prio, pre, steps, data, exp):
    return (n, func, prio, pre if isinstance(pre, str) else L(*pre), steps if isinstance(steps, str) else L(*steps),
            data if isinstance(data, str) else L(*data), exp if isinstance(exp, str) else L(*exp))


MENU = "Vào phân hệ Bán hàng › Yêu cầu › nhóm “Hàng hóa” › bấm “YC tính giá”"
MENU_YCHG = "Vào phân hệ Bán hàng › Yêu cầu › nhóm “Hàng hóa” › bấm “YC hỏi giá”"
Q1 = "XNK xử lý yêu cầu hỏi giá"
Q2 = "Tính giá bán hàng hoá"
Q3 = "Xem giá vốn hàng hoá"
NOPERM = "Bạn không có quyền thực hiện chức năng này"
NOVIEW = "Bạn không có quyền xem yêu cầu tính giá"
NOTFOUND = "Không tìm thấy yêu cầu tính giá"
PAGE404 = "Không tìm thấy hoặc không được cấp quyền truy cập trang"
CONFLICT = "Trạng thái đã bị thay đổi. Vui lòng load lại trang"
NOT_XNK = "Bạn không phải XNK phụ trách nhóm này."
CLOSED = "Nhóm hàng đã đóng, yêu cầu tính giá chỉ còn xem."
REQ = "Bắt buộc phải nhập"

ACC_N = "Tài khoản N (nhân viên kinh doanh) KHÔNG có quyền nào trong 3 quyền " + Q1 + " / " + Q2 + " / " + Q3 + ", đang chọn công ty 1."
ACC_X = ("Tài khoản X có quyền " + Q1 + " tại công ty 1 và đang được phân công XNK phụ trách CARLEO × Carleo (Ming Lurn Precision "
         "Machine Co., Ltd.) tại công ty 1.")
ACC_X2 = "Tài khoản X2 có quyền " + Q1 + " tại công ty 1 nhưng KHÔNG được phân công hãng nào."
ACC_K = "Tài khoản K (Kế toán mua hàng) có quyền " + Q2 + " tại công ty 1, KHÔNG có quyền " + Q3 + "."
ACC_V = "Tài khoản V chỉ có quyền " + Q3 + " tại công ty 1."
GRP = "Nhóm CARLEO của PYCHG-04223 (7 mã hàng, mỗi mã 1 ĐVT) đang Chờ lập YCTG, chưa có YCTG; PYCHG-04223 Đang hỏi giá."
Y_WAIT = "YCTG Y1 của nhóm CARLEO do X lập, đã gửi, đang Chờ tính giá, chưa có PTG."

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     L("Yêu cầu tính giá (YCTG, phân hệ Bán hàng) là chứng từ thứ 2 của luồng tính giá bán (YCHG sang YCTG sang Phiếu tính giá sang giá áp):",
       "- XNK được phân công phụ trách hãng lập YCTG cho 1 nhóm Thương hiệu — Hãng Chờ lập YCTG của YCHG: chọn tiền tệ, tỉ giá, nhập Giá NCC, "
       "Thuế NK, chi phí cho mọi hàng × ĐVT, rồi gửi.",
       "- Kế toán mua hàng Từ chối (trả XNK sửa) hoặc bấm Tính giá để lập Phiếu tính giá; YCTG chạy theo PTG tới Đã tính giá.",
       "- YCTG không ghi giá bán; giá bán mới chỉ có sau khi PTG được áp giá, xem ở “Chi tiết kết quả”.")),
    ("2. Đối tượng được tính / hiển thị",
     L("- Danh sách: YCTG của CÔNG TY ĐANG LÀM VIỆC ở trạng thái Chờ tính giá, Không duyệt, Đang tính giá, Chờ duyệt giá, Đã tính giá "
       "(mọi người có quyền xem trong công ty thấy).",
       "- YCTG Đang tạo: CHỈ người lập thấy.",
       "- Dòng của YCTG = mọi hàng của nhóm × mọi ĐVT đã khai, ĐVT cơ bản trước.",
       "- Popup Chọn nhóm: nhóm Chờ lập YCTG, chưa có YCTG, YCHG Đang hỏi giá, mà người đăng nhập đang được phân công XNK.")),
    ("3. Đối tượng bị ẩn / không tính",
     L("- YCTG công ty khác (báo “" + NOTFOUND + "”).",
       "- YCTG Đang tạo của người khác (mở thẳng ra trang “" + PAGE404 + "”).",
       "- Hàng tạm của nhóm (Hàng tạm / Hàng tạm đã duyệt / Hàng tạm không duyệt) không đi sang YCTG.",
       "- Số PTG đang nháp của người khác (nút Xem phiếu tính giá không hiện).",
       "- Giá vốn công ty quản lý ở cột Chính sách giá nội bộ với người KHÔNG có quyền " + Q3 + " (hiện “—”).")),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô lọc “Ngày tạo” (từ ngày – đến ngày) lọc theo ngày lập YCTG, tính trọn ngày đầu và ngày cuối. Không có lọc thời gian khác."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     L("- YCHG › nhóm Thương hiệu × Hãng › tối đa 1 YCTG › tối đa 1 PTG › 1 kết quả.",
       "- YCTG › dòng hàng × ĐVT › nhiều dòng chi phí.",
       "- Bảng Hàng hoá: STT đánh theo hàng; ĐVT thứ 2 trở đi ghi “cùng mã” (mũi tên).")),
    ("6. Quy tắc cộng dồn / deduplicate",
     L("- Cột Số mã hàng đếm mã hàng KHÁC NHAU (1 hàng 2 ĐVT = 1).",
       "- Chân bảng đếm số YCTG khớp bộ lọc.",
       "- Mỗi dòng hàng × ĐVT không được có 2 chi phí trùng tên.",
       "- Bản in cột Chi phí = tổng thành tiền VNĐ các chi phí của dòng.")),
    ("7. Phân quyền cấp",
     L("Xem YCTG cần ÍT NHẤT 1 trong 3 quyền (xét tại công ty đang làm việc, super admin không được miễn):",
       "- " + Q1 + ": xem; lập YCTG khi ĐỒNG THỜI là XNK được phân công hiện hành của nhóm; sửa / gửi / xoá YCTG mình lập.",
       "- " + Q2 + ": xem; Từ chối YCTG Chờ tính giá; Tính giá (lập PTG); nhận thông báo Chờ duyệt.",
       "- " + Q3 + ": xem; thấy giá vốn công ty quản lý ở cột Chính sách giá nội bộ.",
       "Không có quyền nào: không thấy menu, không xem được. Không phân quyền theo phòng ban / cấp.")),
    ("8. Cách tính các ô thống kê",
     L("- Đơn giá VNĐ = Giá NCC × Tỉ giá (vd 10 USD × 26,180 = 261,800).",
       "- Thành tiền sau thuế = Đơn giá VNĐ × (1 + Thuế NK / 100) (vd 2,238,390 × 1,05 = 2,350,310).",
       "- Đơn giá chi phí = Tỉ lệ / 100 × Giá NCC; Thành tiền chi phí VNĐ = Đơn giá chi phí × Tỉ giá (vd 10% của 10 USD = 1 USD = 26,180).",
       "- Gợi ý giá ĐVT khác = Giá NCC ĐVT cơ bản × hệ số quy đổi (vd 10 × 20 = 200).",
       "- Máy chủ TÍNH LẠI mọi số khi lưu, làm tròn 2 số thập phân; màn hiện tới đồng.",
       "- Chân bảng “Hiển thị a–b / N”: N = tổng YCTG khớp bộ lọc.")),
    ("9. Ghi chú đọc bảng",
     L("- Số tiền dấu phẩy ngăn nghìn, dấu chấm thập phân (30,927.74); ngày dd/mm/yyyy.",
       "- Bẫy 1: có quyền " + Q1 + " CHƯA đủ để lập — phải đúng người được phân công hãng; nhưng SỬA YCTG đã lập thì không xét lại phân công.",
       "- Bẫy 2: Lưu nháp không bắt buộc Giá NCC nhưng bắt buộc Đơn vị tiền tệ; Lưu và gửi duyệt bắt buộc mọi dòng Giá NCC lớn hơn 0.",
       "- Bẫy 3: YCTG Không duyệt KHÔNG xoá được; nhưng Lưu nháp nó sẽ về Đang tạo rồi xoá được (ghi nhận lệch tài liệu thiết kế).",
       "- Bẫy 4: KTMH không có quyền " + Q3 + " vẫn thấy Giá NCC / chi phí nhưng KHÔNG thấy giá vốn ở cột Chính sách.",
       "- Bẫy 5: mọi YCTG Đã tính giá đều có dòng xám “Nhóm hàng đã kết thúc (Đã tính giá)” — đúng thiết kế, không phải lỗi.",
       "- Môi trường thử: DB dev chỉ có YCTG Đang tạo / Không duyệt / Đang tính giá / Đã tính giá; chưa có chính sách giá nội bộ cho công "
       "ty mua nào nên cột Chính sách luôn là “Hàng hoá của TPE …” ở công ty 1 — muốn thử 3 kiểu thì cấu hình chính sách ở màn Chính sách "
       "giá bán nội bộ và lập YCTG ở công ty mua.",
       "- Nhóm ca 'gọi thẳng chức năng, bỏ qua giao diện' dành cho tester kỹ thuật (dùng công cụ kiểm thử API).")),
]

ROLE_TCS = [
    ("01", "Không có quyền nào: không thấy menu, không xem được", "P0", [ACC_N],
     ["1. Đăng nhập N.", "2. Mở phân hệ Bán hàng › Yêu cầu › nhóm “Hàng hóa”.", "3. Mở thẳng màn danh sách YCTG (link được gửi)."], "—",
     ["- Bước 2: KHÔNG có mục “YC tính giá” (có “YC hỏi giá”).", "- Bước 3: bảng rỗng, thông báo “" + NOVIEW + "”."]),
    ("02", "Không có quyền nào: mở thẳng Chi tiết YCTG", "P0", [ACC_N, "PYCTG-03162 Đã tính giá ở công ty 1."],
     ["1. Mở thẳng màn Chi tiết PYCTG-03162 (link được gửi)."], "—", ["- Chuyển trang “" + PAGE404 + "”, không lộ dữ liệu phiếu."]),
    ("03", "Chỉ có " + Q3 + ": xem được, không có nút ghi", "P0", [ACC_V, "PYCTG-03162 Đã tính giá."],
     ["1. " + MENU + ".", "2. Bấm PYCTG-03162."], "—",
     ["- Thấy menu và danh sách; KHÔNG có nút Tạo mới.", "- Chi tiết: chân màn chỉ Xem phiếu tính giá, In, Quay lại."]),
    ("04", "Có " + Q1 + " + được phân công: thấy Tạo mới, popup có nhóm", "P0", [ACC_X, GRP],
     ["1. " + MENU + ".", "2. Bấm Tạo mới."], "—",
     ["- Có nút Tạo mới.", "- Popup “Chọn nhóm cần lập yêu cầu tính giá” có dòng PYCHG-04223 — CARLEO — Carleo …, 7 mã hàng, nút Chọn."]),
    ("05", "Có " + Q1 + " nhưng KHÔNG được phân công: popup rỗng", "P0", [ACC_X2, GRP],
     ["1. " + MENU + ".", "2. Bấm Tạo mới."], "—", ["- Popup hiện “Không có nhóm nào đang chờ bạn lập YCTG”."]),
    ("06", "Có " + Q2 + ": thấy Xử lý / Tính giá / Từ chối với YCTG Chờ tính giá", "P0", [ACC_K, Y_WAIT],
     ["1. " + MENU + ".", "2. Ở dòng Y1 bấm Xử lý."], "—",
     ["- Dòng Y1 có icon Xử lý và Tính giá; KHÔNG có Sửa / Xóa.", "- Chân màn Chi tiết: Tính giá, Từ chối, In, Quay lại.",
      "- Không có nút Tạo mới (không có " + Q1 + ")."]),
    ("07", "Có " + Q2 + " ở công ty KHÁC, không có ở công ty 1", "P0",
     ["Tài khoản K4 có " + Q2 + " tại công ty 4, không có quyền nào tại công ty 1; đang chọn công ty 1.", Y_WAIT],
     ["1. Mở phân hệ Bán hàng › Yêu cầu › nhóm “Hàng hóa”.", "2. Mở thẳng Chi tiết Y1."], "—",
     ["- Không có mục “YC tính giá”.", "- Bước 2: trang “" + PAGE404 + "” (quyền phải gán đúng công ty phiếu)."]),
    ("08", "Super admin chưa được gán quyền nào trong 3 quyền", "P1", ["Tài khoản quản trị cao nhất, không được gán " + Q1 + " / " + Q2 + " / " + Q3 + " tại công ty 1."],
     ["1. Mở phân hệ Bán hàng › Yêu cầu › nhóm “Hàng hóa”."], "—", ["- Không có mục “YC tính giá” (không được miễn quyền)."]),
    ("09", "Người khác không thấy YCTG Đang tạo", "P0", [ACC_V, "PYCTG-02874 Đang tạo do người khác lập."],
     ["1. " + MENU + ", tìm “PYCTG-02874”.", "2. Mở thẳng Chi tiết PYCTG-02874."], "—",
     ["- Bước 1: “Không có dữ liệu phù hợp”.", "- Bước 2: trang “" + PAGE404 + "”."]),
    ("10", "Bỏ qua giao diện: xem danh sách / chi tiết khi không có quyền nào", "P0", [ACC_N, "PYCTG-03162 Đã tính giá."],
     ["1. Dùng công cụ kiểm thử API gọi thẳng chức năng xem danh sách YCTG.", "2. Gọi thẳng xem chi tiết PYCTG-03162.", "3. Gọi thẳng In PYCTG-03162."], "—",
     ["- Cả 3 bị từ chối, báo “" + NOVIEW + "”; không trả dữ liệu phiếu."]),
    ("11", "Bỏ qua giao diện: lập YCTG khi không có " + Q1 + " / sai phân công", "P0", [ACC_K, ACC_X2, GRP],
     ["1. K gọi thẳng chức năng Lưu YCTG cho nhóm CARLEO.", "2. X2 gọi thẳng chức năng Lưu YCTG cho nhóm CARLEO.", "3. X2 gọi thẳng mở khung form Tạo của nhóm."], "—",
     ["- Bước 1: “" + NOPERM + "”.", "- Bước 2, 3: “" + NOT_XNK + "”.", "- Nhóm CARLEO vẫn Chờ lập YCTG, không có YCTG mới."]),
    ("12", "Bỏ qua giao diện: Từ chối khi không có " + Q2, "P0", [ACC_X, Y_WAIT],
     ["1. X (người lập, không có " + Q2 + ") gọi thẳng chức năng Từ chối Y1 với lý do “x”."], "—",
     ["- Bị từ chối, báo “" + NOPERM + "”.", "- Y1 vẫn Chờ tính giá, lịch sử không thêm dòng."]),
    ("13", "Bỏ qua giao diện: sửa / xoá YCTG của người khác", "P0",
     ["Tài khoản X3 có " + Q1 + " tại công ty 1, không phải người lập.", "YCTG Y2 Đang tạo do X lập; YCTG Y3 Không duyệt do X lập."],
     ["1. X3 gọi thẳng Sửa Y2.", "2. X3 gọi thẳng Xoá Y2.", "3. X3 gọi thẳng Sửa Y3."], "—",
     ["- Bước 1, 2: “" + NOTFOUND + "” (nháp người khác coi như không có).", "- Bước 3: “" + CONFLICT + "”.", "- Y2, Y3 không đổi."]),
    ("14", "Bỏ qua giao diện: thao tác YCTG của công ty khác", "P0",
     ["Tài khoản K có " + Q2 + " ở cả công ty 1 và 4; đang chọn công ty 1.", "YCTG Y4 thuộc công ty 4, Chờ tính giá."],
     ["1. Gọi thẳng xem chi tiết Y4.", "2. Gọi thẳng Từ chối Y4.", "3. Gọi thẳng In Y4."], "—",
     ["- Cả 3: “" + NOTFOUND + "”.", "- Đổi sang công ty 4 mới thao tác được."]),
    ("15", "Bỏ qua giao diện: không có " + Q3 + " thì máy chủ không trả giá vốn", "P0",
     [ACC_K, "YCTG Y5 ở công ty mua có hàng của công ty quản lý, chính sách “Theo giá vốn”."],
     ["1. K gọi thẳng chức năng xem chi tiết Y5, đọc dữ liệu cột Chính sách giá nội bộ."], "—",
     ["- Có cách tính, 2 tỷ lệ, Giá bán lẻ công ty quản lý.", "- Giá vốn công ty quản lý KHÔNG có trong dữ liệu trả về (trống)."]),
]

S1 = [
    T(1, "Mở màn từ menu", "P0", [ACC_V], ["1. " + MENU + "."], "—",
      ["- Mục “YC tính giá” nằm ngay sau “YC hỏi giá”.", "- Tiêu đề “Yêu cầu tính giá”.",
       "- Bảng 10 cột: STT, Số phiếu, Yêu cầu hỏi giá, Thương hiệu – Hãng sản xuất, Số mã hàng, Tiền tệ, Người tạo, Ngày tạo, Trạng thái, Hành động.",
       "- 10 dòng / trang, mới tạo lên trước (DB dev công ty 1: “Hiển thị 1–10 / 2305”)."]),
    T(2, "Lối vào Lập YCTG ở Chi tiết YCHG", "P0", [ACC_X, GRP], ["1. " + MENU_YCHG + ".", "2. Mở PYCHG-04223, ở dòng nhóm CARLEO bấm Lập YCTG.", "3. Bấm Quay lại."], "—",
      ["- Mở form “Tạo yêu cầu tính giá”: Yêu cầu hỏi giá PYCHG-04223, Thương hiệu – Hãng CARLEO — Carleo …, 7 dòng.", "- Quay lại về Chi tiết PYCHG-04223."]),
    T(3, "Lối vào Lập YCTG ở danh sách YCHG", "P1", [ACC_X, GRP], ["1. " + MENU_YCHG + ".", "2. Bung PYCHG-04223, bấm icon Lập YCTG ở dòng nhóm.", "3. Bấm Quay lại."], "—",
      ["- Mở form Tạo của nhóm CARLEO.", "- Quay lại về danh sách YCHG."]),
    T(4, "Lối vào Tạo mới + popup Chọn nhóm", "P0", [ACC_X, GRP], ["1. " + MENU + ".", "2. Bấm Tạo mới, bấm Chọn ở dòng CARLEO."], "—",
      ["- Popup đóng, mở form Tạo của nhóm CARLEO.", "- Quay lại về danh sách YCTG."]),
    T(5, "Mở từ thông báo “[YCTG] Chờ duyệt”", "P0", [ACC_K, "X vừa gửi Y1."], ["1. Bấm chuông.", "2. Bấm thông báo “[YCTG] Chờ duyệt: <số Y1>. Nhóm: CARLEO — …”."], "—",
      ["- Mở Chi tiết Y1, chân màn có Tính giá, Từ chối."]),
    T(6, "Mở từ link YCTG ở Chi tiết YCHG", "P1", [ACC_V, "PYCHG-04283 nhóm MULLER có PYCTG-03162."], ["1. " + MENU_YCHG + ", mở PYCHG-04283.", "2. Bấm PYCTG-03162 trên dòng nhóm."], "—",
      ["- Mở Chi tiết PYCTG-03162.", "- Với tài khoản N: PYCTG-03162 là chữ thường, không bấm được."]),
    T(7, "Mở thẳng màn Sửa của YCTG không sửa được", "P1", [ACC_V, "PYCTG-03162 Đã tính giá."], ["1. Mở thẳng màn Sửa PYCTG-03162 (link được gửi)."], "—",
      ["- Tự chuyển sang màn Chi tiết PYCTG-03162, không có ô nhập."]),
    T(8, "Mở form Tạo của nhóm đã có YCTG", "P1", [ACC_X, "Nhóm CARLEO vừa có YCTG Y1 (do X lập ở tab khác)."], ["1. Ở tab cũ bấm Lập YCTG nhóm CARLEO."], "—",
      ["- Thông báo “" + CONFLICT + "”, về danh sách YCTG."]),
    T(9, "Đổi công ty đang làm việc", "P0", ["Tài khoản V có " + Q3 + " ở công ty 1 và 4."], ["1. Ở công ty 1 mở danh sách.", "2. Đổi sang công ty 4."], "—",
      ["- Danh sách tải lại, chỉ còn YCTG công ty 4 (DB dev: 674 Đã tính giá + 2 Không duyệt)."]),
]

S2 = [
    T(1, "Tìm theo số YCTG", "P0", [ACC_V], ["1. " + MENU + ".", "2. Gõ “03162”, nhấn Enter."], "Từ khoá: 03162", ["- Chỉ còn PYCTG-03162."]),
    T(2, "Tìm theo số YCHG gốc", "P1", [ACC_V], ["1. Gõ “PYCHG-04283”, bấm Tìm kiếm."], "Từ khoá: PYCHG-04283", ["- Hiện PYCTG-03162 (YCHG gốc PYCHG-04283)."]),
    T(3, "Tìm theo mã / tên hàng", "P1", [ACC_V], ["1. Gõ “AMAT8574091”.", "2. Gõ “Bộ chuyển đổi USB”."], "—", ["- Cả 2 lần đều có PYCTG-03162."]),
    T(4, "Lọc Trạng thái", "P0", [ACC_V], ["1. Bấm Tìm kiếm nâng cao.", "2. Trạng thái: Không duyệt."], "Trạng thái: Không duyệt",
      ["- Ô Trạng thái có 6 giá trị: Đang tạo, Chờ tính giá, Không duyệt, Đang tính giá, Chờ duyệt giá, Đã tính giá.", "- DB dev công ty 1: 19 YCTG Không duyệt, có PYCTG-02786."]),
    T(5, "Lọc Đang tạo chỉ ra nháp của mình", "P0", [ACC_V, "Công ty 1 có 4 YCTG Đang tạo của người khác; V không có nháp."], ["1. Trạng thái: Đang tạo."], "—",
      ["- “Không có dữ liệu phù hợp” (không lộ nháp người khác)."]),
    T(6, "Lọc Thương hiệu + Hãng sản xuất", "P1", [ACC_V], ["1. Thương hiệu: MULLER.", "2. Hãng sản xuất: MULLER AUTOMOTIVE SÂS."], "—",
      ["- Chỉ còn YCTG của nhóm MULLER (có PYCTG-03162)."]),
    T(7, "Lọc Người tạo", "P2", [ACC_V], ["1. Người tạo: Nguyễn Thị Thanh Trà - HN_XNK - 12210394."], "—", ["- Chỉ còn YCTG do người này lập (có PYCTG-03162)."]),
    T(8, "Lọc khoảng Ngày tạo tính trọn ngày", "P1", [ACC_V], ["1. Ngày tạo: 14/09/2026 sang 14/09/2026."], "—", ["- Có PYCTG-03163, 03162 (lập 14/09/2026 lúc 16:21)."]),
    T(9, "Làm mới", "P1", [ACC_V, "Đang lọc Không duyệt."], ["1. Bấm Làm mới."], "—", ["- Mọi ô lọc trống, sắp Ngày tạo giảm dần, về trang 1."]),
    T(10, "Ghi nhớ bộ lọc khi quay lại", "P2", [ACC_V], ["1. Lọc Không duyệt.", "2. Mở PYCTG-02786, bấm Quay lại."], "—", ["- Vẫn đang lọc Không duyệt, khối lọc giữ đóng / mở như trước."]),
]

S3 = [
    T(1, "Cột Tiền tệ có tỉ giá", "P1", [ACC_V], ["1. Xem dòng PYCTG-03162."], "—", ["- Cột Tiền tệ “EURO”, dòng dưới “tỉ giá 30,927.74”; dòng VNĐ không có dòng tỉ giá."]),
    T(2, "Cột Số mã hàng đếm mã khác nhau", "P1", [ACC_V, "PYCTG-01939: 1 mã ENEO-124-V5091, 2 ĐVT Thùng / Tuýp."], ["1. Tìm PYCTG-01939."], "—", ["- Số mã hàng = 1."]),
    T(3, "Link số phiếu và số YCHG", "P1", [ACC_V], ["1. Bấm PYCTG-03162.", "2. Quay lại, bấm PYCHG-04283 ở cùng dòng."], "—",
      ["- Bước 1: Chi tiết YCTG.", "- Bước 2: Chi tiết YCHG PYCHG-04283."]),
    T(4, "Sắp xếp theo Số phiếu / Ngày tạo", "P2", [ACC_V], ["1. Bấm tiêu đề Số phiếu.", "2. Bấm tiêu đề Ngày tạo 2 lần."], "—",
      ["- Sắp tăng / giảm đúng cột; các cột khác không sắp được."]),
    T(5, "Phân trang và số dòng", "P1", [ACC_V], ["1. Chọn 50 dòng / trang.", "2. Sang trang 2."], "—", ["- Đổi số dòng về trang 1; “Hiển thị 51–100 / 2305” ở trang 2."]),
    T(6, "Cấu hình cột", "P2", [ACC_V], ["1. Bấm Cấu hình cột, bỏ tích Tiền tệ, Lưu.", "2. Tải lại trang."], "—",
      ["- Popup “Đang chọn 10/10 cột” lúc mở; STT, Số phiếu, Hành động không bỏ tích được.", "- Sau tải lại vẫn ẩn cột Tiền tệ."]),
    T(7, "Hành động theo trạng thái — người lập", "P0", [ACC_X, "X có Y2 Đang tạo, Y3 Không duyệt, Y1 Chờ tính giá."], ["1. Xem cột Hành động 3 dòng."], "—",
      ["- Y2: Sửa, Xóa, In.", "- Y3: Sửa, In (KHÔNG có Xóa).", "- Y1: chỉ In."]),
    T(8, "Hành động Xem phiếu tính giá", "P1", [ACC_V], ["1. Xem dòng PYCTG-03162 và PYCTG-00177."], "—",
      ["- PYCTG-03162: có icon Xem phiếu tính giá sang mở PTG-03178.", "- PYCTG-00177 (PTG nháp người khác): KHÔNG có icon này."]),
]

S4 = [
    T(1, "Form Tạo bung đủ hàng × ĐVT", "P0", [ACC_X, "Nhóm ENEOS Chờ lập YCTG gồm ENEO-746-66123 (ĐVT Tuýp cơ bản, Thùng 20C-0.4Kg hệ số 20) và 6 hàng 1 ĐVT."],
      ["1. Mở form Tạo của nhóm ENEOS."], "—",
      ["- ENEO-746-66123 có 2 dòng: Tuýp trước, dòng sau “cùng mã” (mũi tên) Thùng 20C-0.4Kg.", "- STT đánh theo hàng (không theo dòng).",
       "- Không có ô tick chọn dòng; Trạng thái “Đang tạo”."]),
    T(2, "Hàng tạm của nhóm không đi sang YCTG", "P1", [ACC_X, "Nhóm có 3 hàng thường + 1 hàng tạm Không duyệt nằm lại YCHG."], ["1. Mở form Tạo của nhóm."], "—",
      ["- Chỉ có 3 hàng thường; popup Chọn nhóm đếm Số mã hàng = 3."]),
    T(3, "Thuế NK mặc định theo hàng", "P1", [ACC_X, "Hàng H1 khai thuế nhập khẩu 10%; hàng H2 không khai."], ["1. Mở form Tạo."], "—", ["- H1 Thuế NK = 10; H2 = 0."]),
    T(4, "Chọn USD tự điền tỉ giá", "P0", [ACC_X], ["1. Đơn vị tiền tệ: USD."], "Đơn vị tiền tệ: USD",
      ["- Tỉ giá = 26,180, sửa được.", "- Tiêu đề cột đổi thành “Giá NCC (USD) *”."]),
    T(5, "Chọn VNĐ khoá tỉ giá", "P0", [ACC_X], ["1. Đơn vị tiền tệ: VNĐ."], "—", ["- Tỉ giá = 1, ô bị khoá."]),
    T(6, "Gợi ý giá ĐVT khác", "P0", [ACC_X, "Đã chọn USD."], ["1. Gõ 10 vào Giá NCC dòng Tuýp.", "2. Gõ 220 vào dòng Thùng.", "3. Sửa Tuýp thành 12."], "—",
      ["- Bước 1: Thùng tự điền 200.", "- Bước 3: Thùng giữ 220 (đã gõ tay, không gợi ý đè)."]),
    T(7, "Lưu nháp thành công khi chưa nhập giá", "P0", [ACC_X, GRP], ["1. Chọn VNĐ.", "2. Bấm Lưu nháp."], "—",
      ["- Thông báo “Đã lưu nháp yêu cầu tính giá”, về danh sách YCTG.", "- YCTG mới PYCTG-xxxxx Đang tạo; nhóm CARLEO ở YCHG thành “Đang tính giá”, mất nút Lập YCTG / Huỷ duyệt.",
       "- Lịch sử nhóm KHÔNG thêm dòng; KTMH không nhận thông báo."]),
    T(8, "Lưu nháp khi chưa chọn tiền tệ", "P0", [ACC_X], ["1. Không chọn tiền tệ, bấm Lưu nháp."], "—", ["- “" + REQ + "” dưới Đơn vị tiền tệ; không lưu."]),
    T(9, "Quay lại khi đã nhập", "P1", [ACC_X], ["1. Gõ 1 giá NCC.", "2. Bấm Quay lại.", "3. Bấm Ở lại, rồi Quay lại sang Thoát."], "—",
      ["- Hộp “Thông tin chưa lưu”: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”.", "- Ở lại giữ form; Thoát rời màn, không lưu."]),
    T(10, "Popup Chọn nhóm chỉ nhóm của mình", "P0", [ACC_X, GRP, "Nhóm TORIN Chờ lập YCTG phân công cho người khác."], ["1. Bấm Tạo mới."], "—",
      ["- Có CARLEO, KHÔNG có TORIN.", "- Cột: Yêu cầu hỏi giá, Thương hiệu – Hãng sản xuất, Số mã hàng, Người hỏi giá, Ngày tạo, nút Chọn."]),
    T(11, "Thêm chi phí", "P0", [ACC_X, "Đã chọn USD, dòng Tuýp Giá NCC 10."], ["1. Tab Chi phí, ở dòng Tuýp bấm “+ Thêm chi phí”.", "2. Tỉ lệ 10."], "—",
      ["- Dòng mới chọn sẵn “Cước vận tải quốc tế”, Tỉ lệ 0.", "- Sau bước 2: Đơn giá (USD) 1, Thành tiền (VNĐ) 26,180."]),
    T(12, "Nhập Đơn giá chi phí quy ra tỉ lệ", "P1", [ACC_X, "Dòng Tuýp 10 USD."], ["1. Thêm chi phí thứ 2, gõ Đơn giá 2."], "—",
      ["- Chi phí thứ 2 tự chọn “Chi phí vận chuyển nội địa”.", "- Tỉ lệ thành 20; Thành tiền 52,360."]),
    T(13, "Đơn giá chi phí khoá khi chưa có Giá NCC", "P2", [ACC_X, "Dòng Xô 16KG chưa nhập Giá NCC."], ["1. Thêm chi phí cho dòng này."], "—", ["- Ô Đơn giá bị khoá, chỉ nhập được Tỉ lệ."]),
    T(14, "Xoá dòng chi phí", "P2", [ACC_X], ["1. Bấm thùng rác ở 1 dòng chi phí."], "—", ["- Dòng mất ngay, không hỏi lại; dòng hết chi phí hiện “Chưa có chi phí”."]),
    T(15, "Sửa YCTG Đang tạo", "P0", [ACC_X, "Y2 Đang tạo do X lập."], ["1. Bấm Sửa Y2, đổi Ghi chú “Giá tháng 10”, Lưu nháp."], "—",
      ["- Tiêu đề “Sửa yêu cầu tính giá: <số Y2>”.", "- Lưu xong, cột Số phiếu hiện ghi chú dưới số phiếu."]),
    T(16, "Sửa YCTG Không duyệt thấy lý do", "P0", [ACC_X, "Y3 Không duyệt, lý do “Sai giá NCC”."], ["1. Bấm Sửa Y3."], "—",
      ["- Form có dòng “Lý do không duyệt: Sai giá NCC”; Trạng thái Không duyệt."]),
    T(17, "Lưu nháp YCTG Không duyệt", "P1", [ACC_X, "Y3 Không duyệt."], ["1. Sửa Y3, bấm Lưu nháp.", "2. Xem danh sách và Chi tiết Y3."], "—",
      ["- Y3 thành Đang tạo; dòng Lý do không duyệt không còn hiện; có nút Xóa.", "- Lưu ý: người khác không còn thấy Y3. Ghi nhận lệch thiết kế (Không duyệt chỉ sửa rồi gửi lại) — báo nghiệp vụ."]),
    T(18, "Sửa khi đã mất phân công vẫn được", "P1", [ACC_X, "Y2 Đang tạo do X lập; phân công CARLEO vừa chuyển sang người khác."], ["1. X sửa Y2, Lưu nháp."], "—",
      ["- Lưu được (YCTG thuộc người lập, không xét lại phân công)."]),
    T(19, "Xem chi tiết đủ khối", "P0", [ACC_V], ["1. Mở PYCTG-03162."], "—",
      ["- Dòng xám “Nhóm hàng đã kết thúc (Đã tính giá) — yêu cầu tính giá chỉ còn xem.”.",
       "- Thông tin chung: PYCHG-04283, MULLER — MULLER AUTOMOTIVE SÂS, Người hỏi giá Đặng Tiến Mạnh, EURO, 30,927.74.",
       "- Tab Hàng hoá: MLER-AMAT8574091 Bộ, Giá NCC 316, Đơn giá VNĐ 9,773,166, Thuế 10, Sau thuế 10,750,482.",
       "- Khối lịch sử: Duyệt tính giá sang Lập yêu cầu tính giá sang XNK duyệt."]),
    T(20, "Chi tiết tab Chi phí chỉ xem", "P1", [ACC_V], ["1. Ở PYCTG-03162 bấm tab Chi phí."], "—",
      ["- 3 chi phí: Cước vận tải quốc tế, Chi phí vận chuyển nội địa, Bảo hiểm hàng hóa; ô bị khoá, không có “+ Thêm chi phí”, không có cột Hành động."]),
    T(21, "Chi tiết YCTG Không duyệt của người khác", "P1", [ACC_V], ["1. Mở PYCTG-02786."], "—",
      ["- Dòng “Lý do không duyệt: .”; chân màn chỉ In, Quay lại."]),
    T(22, "Xoá YCTG Đang tạo", "P0", [ACC_X, "Y2 Đang tạo của X (nhóm CARLEO Đang tính giá)."], ["1. Bấm Xóa ở dòng Y2.", "2. Bấm Xóa."], "—",
      ["- Hộp “Xác nhận xóa”: “Xóa yêu cầu tính giá <số Y2>? Nhóm hàng sẽ về \"Chờ lập YCTG\".”.", "- “Đã xoá yêu cầu tính giá”; nhóm CARLEO về Chờ lập YCTG, nút Lập YCTG hiện lại ở YCHG."]),
    T(23, "Huỷ xoá", "P2", [ACC_X, "Y2 Đang tạo."], ["1. Bấm Xóa, rồi Hủy."], "—", ["- Y2 còn nguyên."]),
    T(24, "YCTG Không duyệt không có nút Xóa", "P1", [ACC_X, "Y3 Không duyệt."], ["1. Xem dòng Y3 và Chi tiết Y3."], "—", ["- Không có Xóa ở cả 2 nơi."]),
    T(25, "In phiếu", "P1", [ACC_V], ["1. Ở dòng PYCTG-03162 bấm In."], "—",
      ["- Popup “Xem trước yêu cầu tính giá PYCTG-03162”: tiêu đề PHIẾU YÊU CẦU TÍNH GIÁ, Tiền tệ / tỉ giá “EURO / 30,927.74”, Trạng thái Đã tính giá.",
       "- Bảng 9 cột, dòng MLER-AMAT8574091 316 · 9,773,166 · 10 · 10,750,482.", "- Khối ký XNK lập / Kế toán mua hàng; Ghi chú trống in “.....”."]),
]

S5 = [
    T(1, "Gửi YCTG thành công", "P0", [ACC_X, ACC_K, GRP], ["1. Mở form Tạo nhóm CARLEO, chọn VNĐ, nhập Giá NCC cả 7 dòng.", "2. Bấm Lưu và gửi duyệt sang Lưu và gửi duyệt."], "Giá NCC: 100.000 mỗi dòng",
      ["- Hộp “Gửi yêu cầu tính giá”: “Gửi yêu cầu tính giá mới (7 dòng hàng × ĐVT) cho Kế toán mua hàng tính giá?”.",
       "- “Đã gửi yêu cầu tính giá”; YCTG Chờ tính giá.", "- Lịch sử nhóm thêm “Lập yêu cầu tính giá”, nội dung = số phiếu.",
       "- K nhận “[YCTG] Chờ duyệt: <số phiếu>. Nhóm: CARLEO — Carleo …”."]),
    T(2, "Gửi khi còn dòng chưa có giá", "P0", [ACC_X], ["1. Để trống Giá NCC dòng 3, bấm Lưu và gửi duyệt."], "—",
      ["- “" + REQ + "” dưới Giá NCC dòng 3; tab Hàng hoá gắn chấm đỏ; KHÔNG mở hộp xác nhận."]),
    T(3, "Gửi khi Giá NCC = 0", "P0", [ACC_X], ["1. Giá NCC dòng 1 = 0, bấm Lưu và gửi duyệt."], "Giá NCC: 0", ["- “Phải lớn hơn 0”; không gửi."]),
    T(4, "Huỷ ở hộp xác nhận gửi", "P2", [ACC_X], ["1. Bấm Lưu và gửi duyệt, rồi Hủy."], "—", ["- Không gửi, form giữ nguyên số đã nhập."]),
    T(5, "KTMH từ chối thành công", "P0", [ACC_K, Y_WAIT], ["1. Mở Y1, bấm Từ chối.", "2. Nhập “Sai giá NCC”, bấm Từ chối."], "Lý do từ chối: Sai giá NCC",
      ["- Popup “Từ chối yêu cầu tính giá”, dòng phụ “<số Y1> — trả về XNK sửa giá NCC / chi phí”.", "- “Đã từ chối yêu cầu tính giá”; Y1 Không duyệt, Chi tiết có “Lý do không duyệt: Sai giá NCC”.",
       "- Lịch sử “KTMH không duyệt”, nội dung “<số Y1>. Sai giá NCC”.", "- X nhận “[YCTG] Yêu cầu làm lại: <số Y1>. Lý do: Sai giá NCC”."]),
    T(6, "Từ chối thiếu lý do", "P0", [ACC_K, Y_WAIT], ["1. Bấm Từ chối, để trống, bấm Từ chối."], "—", ["- “" + REQ + "” dưới ô, popup không đóng, Y1 vẫn Chờ tính giá."]),
    T(7, "Từ chối lý do quá 255 ký tự", "P1", [ACC_K, Y_WAIT], ["1. Nhập 256 ký tự, bấm Từ chối."], "Lý do: 256 ký tự", ["- “Vui lòng nhập tối đa 255 ký tự.”; popup giữ nguyên."]),
    T(8, "Sửa và gửi lại sau khi bị từ chối", "P0", [ACC_X, ACC_K, "Y1 Không duyệt."], ["1. X sửa Giá NCC, bấm Lưu và gửi duyệt."], "—",
      ["- Y1 Chờ tính giá; K nhận lại “[YCTG] Chờ duyệt …”; lịch sử thêm “Lập yêu cầu tính giá” lần 2."]),
    T(9, "KTMH bấm Tính giá", "P0", [ACC_K, Y_WAIT], ["1. Ở Chi tiết Y1 bấm Tính giá.", "2. Bấm Quay lại (chưa lưu PTG)."], "—",
      ["- Mở màn Tạo phiếu tính giá của Y1, không có hộp xác nhận.", "- Quay lại về Chi tiết Y1; Y1 vẫn Chờ tính giá."]),
    T(10, "Lưu PTG đổi YCTG Đang tính giá", "P0", [ACC_K, Y_WAIT], ["1. Lập PTG từ Y1, Lưu nháp PTG.", "2. Mở lại Y1."], "—",
      ["- Y1 Đang tính giá; không còn Tính giá / Từ chối; có Xem phiếu tính giá (với K)."]),
    T(11, "PTG gửi duyệt giá — YCTG Chờ duyệt giá", "P1", ["Công ty 1 bật duyệt giá; Y1 Đang tính giá."], ["1. K bấm Lưu và duyệt PTG của Y1."], "—", ["- Y1 Chờ duyệt giá (nhãn tím)."]),
    T(12, "Có dòng giá bị từ chối — YCTG về Đang tính giá", "P1", ["Y1 Chờ duyệt giá."], ["1. Người duyệt giá Không duyệt 1 dòng ở màn Duyệt giá bán."], "—", ["- Y1 về Đang tính giá."]),
    T(13, "Xoá PTG nháp — YCTG về Chờ tính giá", "P1", ["Y1 Đang tính giá, PTG nháp của K."], ["1. K xoá PTG."], "—", ["- Y1 Chờ tính giá; nút Tính giá hiện lại."]),
    T(14, "PTG nháp người khác không lộ số", "P1", [ACC_V], ["1. Mở PYCTG-00177 (Đang tính giá)."], "—", ["- Không có nút Xem phiếu tính giá; không thấy số PTG nào."]),
    T(15, "Nhóm đã đóng chỉ còn xem", "P0", [ACC_V], ["1. Mở PYCTG-01403."], "—",
      ["- Dòng “Nhóm hàng đã kết thúc (Huỷ duyệt) — yêu cầu tính giá chỉ còn xem.”; chân màn chỉ In, Quay lại."]),
    T(16, "Gọi thẳng thao tác ghi trên nhóm đã đóng", "P1", ["Tài khoản lập PYCTG-01403 có " + Q1 + "; K có " + Q2 + "."], ["1. Người lập gọi thẳng Sửa PYCTG-01403.", "2. K gọi thẳng Từ chối PYCTG-01403."], "—",
      ["- Cả 2: “" + CLOSED + "”; phiếu không đổi."]),
    T(17, "Thông báo chỉ trong công ty phiếu", "P1", ["Tài khoản K4 có " + Q2 + " chỉ ở công ty 4."], ["1. X gửi YCTG ở công ty 1."], "—", ["- K4 KHÔNG nhận thông báo."]),
]

S6 = [
    T(1, "Đơn giá VNĐ = Giá NCC × Tỉ giá", "P0", [ACC_X, "Đã chọn USD, tỉ giá 26,180."], ["1. Gõ 10 vào Giá NCC dòng Tuýp."], "Giá NCC: 10", ["- Đơn giá VNĐ 261,800; Thùng gợi ý 200 sang 5,236,000."]),
    T(2, "Thành tiền sau thuế", "P0", [ACC_X, "USD 26,180."], ["1. Giá NCC 85.5, Thuế NK 5."], "Giá NCC: 85.5\nThuế NK: 5", ["- Đơn giá VNĐ 2,238,390; Thành tiền sau thuế 2,350,310."]),
    T(3, "Thành tiền chi phí", "P0", [ACC_X, "USD 26,180, Giá NCC 10."], ["1. Chi phí Cước vận tải quốc tế Tỉ lệ 10."], "—", ["- Đơn giá (USD) 1; Thành tiền (VNĐ) 26,180."]),
    T(4, "Đổi tỉ giá tính lại mọi dòng", "P0", [ACC_X, "Giá NCC 10 ở 2 dòng, chi phí 10%."], ["1. Sửa Tỉ giá thành 25,000."], "Tỉ giá: 25,000",
      ["- Đơn giá VNĐ 250,000; Thành tiền chi phí 25,000 — đổi ngay ở mọi dòng."]),
    T(5, "VNĐ: đơn giá bằng giá NCC", "P1", [ACC_X], ["1. Chọn VNĐ, Giá NCC 1.500.000, Thuế 10."], "—", ["- Đơn giá VNĐ 1,500,000; Sau thuế 1,650,000."]),
    T(6, "Máy chủ tính lại, không lấy số màn hình", "P0", [ACC_X, "USD 26,180."],
      ["1. Dùng công cụ kiểm thử API gửi Lưu nháp với Giá NCC 10 nhưng Đơn giá VNĐ ghi 1 và thành tiền sau thuế ghi 1.", "2. Mở Chi tiết YCTG."], "—",
      ["- Chi tiết hiện Đơn giá VNĐ 261,800 (máy chủ tính lại), không phải 1."]),
    T(7, "Làm tròn 2 số thập phân", "P2", [ACC_X], ["1. Giá NCC 10.456 (gõ 3 số lẻ)."], "—", ["- Ô chỉ giữ 2 số lẻ (10.45 / 10.46 theo ô nhập); số lưu 2 số lẻ."]),
    T(8, "Lưu / gửi YCTG không đổi giá bán", "P0", ["Hàng MLER-AMAT8574091 Bán lẻ hiện hành 22,500,000 ở công ty 1."], ["1. Lập + gửi YCTG có hàng này.", "2. Xem màn Cập nhật giá bán."], "—",
      ["- Giá bán không đổi; trạng thái hàng không đổi (chỉ đổi khi lưu PTG)."]),
    T(9, "Chính sách: hàng của chính công ty", "P1", [ACC_V], ["1. Mở PYCTG-03162, xem cột Chính sách giá nội bộ."], "—", ["- “Hàng hoá của TPE — không có giá mua nội bộ”."]),
    T(10, "Chính sách Theo giá vốn CÓ quyền " + Q3, "P0", [ACC_V, "YCTG Y5 ở công ty mua: hàng của TPE, chính sách Theo giá vốn, Nhập khẩu 3%, Tồn kho 5%; giá vốn TPE 2,310,000, Bán lẻ 2,950,000."],
      ["1. V mở Y5."], "—", ["- “Theo giá vốn · Nhập khẩu 3% · Tồn kho 5%”, “Giá vốn TPE: 2,310,000 · Giá bán lẻ: 2,950,000”."]),
    T(11, "Chính sách Theo giá vốn KHÔNG có quyền " + Q3, "P0", [ACC_K, "Y5 như TC trên."], ["1. K mở Y5."], "—",
      ["- “Giá vốn TPE: —”; Giá bán lẻ 2,950,000 vẫn hiện.", "- Giá NCC, thuế, chi phí vẫn hiện bình thường."]),
    T(12, "Chính sách Theo giá bán", "P1", ["Y5 có hàng chính sách Theo giá bán, Nhập khẩu 10%, Tồn kho 8%, Bán lẻ 95,000."], ["1. Mở Y5."], "—",
      ["- “Theo giá bán · Nhập khẩu 10% · Tồn kho 8%”, chỉ “Giá bán lẻ: 95,000” (không có dòng giá vốn với mọi người)."]),
    T(13, "Chính sách chưa cấu hình", "P1", ["Y5 có hàng của TPE mà TPE chưa khai chính sách cho hãng."], ["1. Mở Y5."], "—", ["- Nhãn cam “Chưa cấu hình” + “TPE chưa khai chính sách cho hãng này”."]),
    T(14, "Bản in không có giá vốn", "P1", [ACC_V, "Y5 có chính sách Theo giá vốn."], ["1. In Y5."], "—", ["- Bản in không có cột Chính sách / giá vốn."]),
    T(15, "Xem giá bán mới", "P0", [ACC_V], ["1. Mở PYCTG-03162.", "2. Bấm Chi tiết kết quả."], "—",
      ["- Trước khi bấm: “Giá bán mới áp ngày 14/09/2026”, bảng giá ẩn.", "- Bảng dưới dòng Bộ: Bán lẻ, Theo lô, Đại lý cấp 1, 2, 3 = 22,500,000 “ĐMGG 5%”; TMĐT 29,250,000 “ĐMGG 0%”.",
       "- Nút đổi “Ẩn chi tiết kết quả”."]),
    T(16, "TMĐT = Bán lẻ × hệ số công ty", "P1", [ACC_V], ["1. Ở bảng giá mới PYCTG-03162 so Bán lẻ và TMĐT."], "—", ["- 22,500,000 × 1,3 = 29,250,000."]),
    T(17, "Giá bán mới theo từng ĐVT", "P1", [ACC_V], ["1. Mở PYCTG-01939, bấm Chi tiết kết quả."], "—", ["- Dòng Thùng và dòng Tuýp mỗi dòng 1 bảng giá riêng."]),
    T(18, "Ẩn / hiện giá mới từng dòng", "P2", [ACC_V], ["1. Bấm dấu X ở bảng dòng Bộ.", "2. Bấm link “Hiện giá mới” (có tam giác nhỏ phía trước)."], "—", ["- Bước 1 ẩn bảng, hiện link dưới ĐVT; bước 2 hiện lại."]),
    T(19, "Xem giá bán mới không cần " + Q3, "P0", [ACC_K], ["1. K mở PYCTG-03162, bấm Chi tiết kết quả."], "—", ["- Thấy đủ 6 loại giá như người có " + Q3 + "."]),
    T(20, "YCTG chưa có kết quả", "P1", [ACC_V], ["1. Mở PYCTG-02786."], "—", ["- Không có “Giá bán mới áp ngày”, không có nút Chi tiết kết quả."]),
    T(21, "Bản chụp giá khác giá hiện hành", "P2", ["Sau khi PYCTG-03162 áp giá, Bán lẻ MLER-AMAT8574091 bị sửa ở màn Cập nhật giá bán thành 23,000,000."], ["1. Mở PYCTG-03162, bật Chi tiết kết quả."], "—",
      ["- Bảng vẫn 22,500,000 (bản chụp lúc áp), không theo giá mới sửa."]),
]

S7 = [
    T(1, "In từ chân màn Chi tiết", "P1", [ACC_V], ["1. Mở PYCTG-03162, bấm In."], "—", ["- Popup xem trước giống in từ danh sách; bấm dấu X đóng popup."]),
    T(2, "Bản in YCTG có chi phí", "P1", [ACC_V], ["1. In PYCTG-03162, xem cột Chi phí."], "—",
      ["- Cột Chi phí = tổng thành tiền VNĐ các chi phí của dòng.", "- Lưu ý: phiếu cũ từ ERP có thể lệch màn Chi tiết (màn tính lại từ tỉ lệ: 1,958,654; bản in lấy số đã lưu: 1,959,031) — đã ghi nhận."]),
    T(3, "In khi không có quyền xem", "P0", [ACC_N], ["1. Gọi thẳng In PYCTG-03162."], "—", ["- “" + NOVIEW + "”, không có bản in."]),
]

S8 = [
    T(1, "Lỗi báo đồng thời", "P0", [ACC_X, "Form Tạo 14 dòng, chưa nhập gì."], ["1. Bấm Lưu và gửi duyệt."], "—",
      ["- 15 lỗi “" + REQ + "” cùng lúc: Đơn vị tiền tệ + 14 Giá NCC; cuộn tới lỗi đầu; không gửi yêu cầu nào."]),
    T(2, "Tỉ giá trống / bằng 0", "P0", [ACC_X, "Đã chọn USD."], ["1. Xoá Tỉ giá, Lưu nháp.", "2. Tỉ giá 0, Lưu nháp."], "—", ["- Bước 1 “" + REQ + "”; bước 2 “Phải lớn hơn 0”."]),
    T(3, "Tỉ giá / Giá NCC quá lớn", "P2", [ACC_X], ["1. Tỉ giá 1.000.000.000.000."], "—", ["- Màn báo “Không hợp lệ”; gọi thẳng chức năng thì máy chủ báo “Không được lớn hơn 999,999,999,999.”."]),
    T(4, "Ghi chú quá 255 ký tự", "P1", [ACC_X], ["1. Ghi chú 256 ký tự, Lưu nháp."], "Ghi chú: 256 ký tự", ["- “Vui lòng nhập tối đa 255 ký tự.”."]),
    T(5, "Thuế NK ngoài 0–100", "P1", [ACC_X], ["1. Thuế NK 120, Lưu nháp."], "Thuế NK: 120", ["- “Phải từ 0 đến 100”."]),
    T(6, "Tỉ lệ chi phí quá 100 do gõ Đơn giá", "P0", [ACC_X, "Dòng Tuýp 10 USD."], ["1. Thêm chi phí, gõ Đơn giá 15.", "2. Lưu nháp."], "Đơn giá chi phí: 15",
      ["- Tỉ lệ tự thành 150 (màn không tự kéo về).", "- Lưu: “Phải từ 0 đến 100” dưới Tỉ lệ; tab Chi phí gắn chấm đỏ, tự chuyển sang tab Chi phí."]),
    T(7, "Chi phí trùng trong 1 dòng", "P1", [ACC_X], ["1. 2 dòng chi phí cùng chọn “Phí kiểm định”, Lưu nháp."], "—", ["- Dòng thứ 2: “Chi phí đã có trong dòng này”."]),
    T(8, "Dòng chi phí chưa chọn tên", "P2", [ACC_X], ["1. Gọi thẳng Lưu nháp với 1 chi phí không có tên."], "—", ["- “" + REQ + "” ở chi phí đó."]),
    T(9, "Tiền tệ đã ngừng dùng", "P2", [ACC_X], ["1. Gọi thẳng Lưu nháp với tiền tệ đã ngừng dùng."], "—", ["- “Không tồn tại” ở Đơn vị tiền tệ."]),
    T(10, "Giá NCC âm", "P1", [ACC_X], ["1. Gọi thẳng Lưu nháp với Giá NCC -5."], "—", ["- “Không hợp lệ”."]),
]

S9 = [
    T(1, "2 XNK cùng lập YCTG 1 nhóm", "P0", ["X và X' cùng được phân công (dữ liệu chuyển giao) và cùng mở form Tạo nhóm CARLEO."], ["1. X Lưu nháp.", "2. X' Lưu nháp."], "—",
      ["- X thành công; X' nhận “" + CONFLICT + "”; nhóm chỉ có 1 YCTG."]),
    T(2, "2 KTMH cùng từ chối", "P1", [ACC_K, "K2 cũng có " + Q2 + "; " + Y_WAIT], ["1. K từ chối Y1.", "2. K2 (màn cũ) từ chối Y1."], "—",
      ["- K2 nhận “" + CONFLICT + "”, màn Chi tiết tải lại hiện Không duyệt."]),
    T(3, "Xoá khi YCTG vừa được gửi ở tab khác", "P1", [ACC_X, "Y2 Đang tạo mở ở 2 tab."], ["1. Tab 1 gửi Y2.", "2. Tab 2 bấm Xóa."], "—", ["- “" + CONFLICT + "”; Y2 không bị xoá."]),
    T(4, "Từ chối trong lúc KTMH khác vừa lập PTG", "P1", [Y_WAIT], ["1. K2 lưu PTG từ Y1.", "2. K (màn cũ) Từ chối Y1."], "—", ["- “" + CONFLICT + "”; Y1 Đang tính giá."]),
    T(5, "Cô lập công ty khi lập", "P0", ["X có " + Q1 + " ở công ty 1 và 4; nhóm G4 thuộc YCHG công ty 4."], ["1. Đang chọn công ty 1, gọi thẳng mở form Tạo của G4."], "—",
      ["- “Không tìm thấy nhóm hàng của yêu cầu hỏi giá”."]),
]

S10 = [
    T(1, "Luồng chuẩn tới giá bán mới (công ty tắt duyệt giá)", "P0", [ACC_X, ACC_K, GRP],
      ["1. X lập YCTG nhóm CARLEO, gửi.", "2. K Tính giá, lập PTG, Lưu và duyệt.", "3. Mở Chi tiết YCTG, bấm Chi tiết kết quả."], "—",
      ["- YCTG lần lượt: Chờ tính giá sang Đang tính giá sang Đã tính giá; nhóm Đã tính giá.", "- Có “Giá bán mới áp ngày <hôm nay>”, bảng 6 loại giá mỗi ĐVT."]),
    T(2, "Luồng có duyệt giá", "P0", ["Công ty 1 bật duyệt giá; Y1 Chờ tính giá."], ["1. K lập PTG, Lưu và duyệt.", "2. Người duyệt Duyệt mọi dòng ở màn Duyệt giá bán."], "—",
      ["- Sau bước 1: Y1 Chờ duyệt giá, chưa có kết quả.", "- Sau bước 2: Y1 Đã tính giá, có kết quả."]),
    T(3, "Từ chối – sửa – gửi lại – tính giá", "P0", [ACC_X, ACC_K], ["1. X gửi.", "2. K Từ chối “Thiếu chi phí”.", "3. X thêm chi phí, gửi lại.", "4. K Tính giá."], "—",
      ["- Lịch sử nhóm: Lập yêu cầu tính giá, KTMH không duyệt, Lập yêu cầu tính giá, Lập phiếu tính giá…", "- X nhận “[YCTG] Yêu cầu làm lại …”, K nhận 2 lần “[YCTG] Chờ duyệt …”."]),
    T(4, "Xoá nháp rồi lập lại", "P1", [ACC_X, GRP], ["1. Lưu nháp YCTG nhóm CARLEO.", "2. Xoá.", "3. Lập lại từ YCHG."], "—",
      ["- Sau bước 2 nhóm về Chờ lập YCTG; bước 3 lập được YCTG mới số khác."]),
]


def _norm(tc):
    return tuple(L(*x) if isinstance(x, list) else x for x in tc)


ROLE_TCS = [_norm(tc) for tc in ROLE_TCS]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP (MENU, LỐI VÀO TỪ YCHG, THÔNG BÁO, LINK)", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "CHỨC NĂNG CHÍNH (TẠO / CHỌN NHÓM / CHI PHÍ / SỬA / XEM / XOÁ / IN)", S4),
    ("V", "THAO TÁC TRẠNG THÁI (GỬI, KTMH TỪ CHỐI, TÍNH GIÁ, THEO PTG, NHÓM ĐÓNG)", S5),
    ("VI", "GIÁ — CÔNG THỨC SỐ TIỀN, GIÁ VỐN Ở CHÍNH SÁCH, GIÁ BÁN MỚI", S6),
    ("VII", "IN PHIẾU", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", S8),
    ("IX", "CÔ LẬP DỮ LIỆU THEO CÔNG TY & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "E2E FLOW", S10),
]

_all = "\n".join("\n".join(map(str, x)) for x in DESCRIPTION_BLOCK + ROLE_TCS + [t for _, _, s in SECTIONS for t in s])
_bad = re.findall(r"[←-⯿\U0001F300-\U0001FAFF]", _all)
assert not _bad, "Con ky tu cam: %s" % sorted(set(_bad))

build(output_file=OUT, sheet_name="Trang tính1", feature_name="Yêu cầu tính giá",
      module_name="Yêu cầu tính giá", description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
print("OK ->", OUT)
