"""Testcase task #10564 — Tổng hợp BOM: sắp xếp hàng hoá/dịch vụ theo ngày tạo BOM thành phần.

Đích: Google Sheet "Testcase _Quản lý dự án" (1qlMBESEAhCRlsqb2XyAasQmfdU2-wYN3priOfNAWiWo),
tab "Update_3107_BomList" (gid=1896896388), nối tiếp khối "UPDATE TESTCASE 14/09" (dòng 219–230).

Bám đúng khuôn các khối UPDATE của tab: dòng tiêu đề nền xanh #93C47D ghép C:G,
cột A "BOM Giải pháp" ghép dọc cả khối, cột B nhóm ghép dọc, TC ID dạng TC-BOM-xxx-NN,
cột J ghi mục đích kiểm tra (như các khối UPDATE trước), cột K mặc định "Not Executed".

Sinh ra:
  - testcase-update-3107.html : bảng HTML (giữ ô gộp, màu, xuống dòng) để dán vào Google Sheets
  - testcase-update-3107.tsv  : bản dự phòng dạng text
Chạy xong tự đưa bản HTML vào clipboard (macOS).
"""
import html
import os
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE = "BOM Giải pháp"
SECTION = "UPDATE TESTCASE 24/09- Task: http://quanly.dnsmedia.vn/issues/10564"

# (nhóm, tc_id, chức năng, priority, tiền điều kiện, bước, test data, expected, mục đích)
TCS = [
    # ---------------- Sắp xếp khi gộp BOM con ----------------
    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-01",
     "Gộp 3 BOM thành phần tạo ở 3 thời điểm khác nhau (AC1 + AC2)", "P0",
     "Có 3 BOM Thành phần cùng Dự án TKT, cùng Giải pháp, cùng loại tiền VND, đều không có nhóm, trạng thái Hoàn thành:\n"
     "- BL-A tạo lúc 09:00 (2 hàng: A1, A2)\n- BL-B tạo lúc 09:10 (2 hàng: B1, B2)\n- BL-C tạo lúc 09:20 (2 hàng: C1, C2)\n"
     "(xem giờ tạo ở cột Ngày tạo của màn danh sách BOM)",
     "1. Bấm Tạo mới BOM, chọn Loại BOM = Tổng hợp, chọn Dự án TKT và Giải pháp.\n"
     "2. Bấm \"Chọn BL con\".\n3. Tick lần lượt BL-A, BL-B, BL-C.\n4. Bấm \"Gộp BOM con\".\n"
     "5. Quan sát thứ tự các dòng trên lưới hàng hoá.",
     "BL-A 09:00\nBL-B 09:10\nBL-C 09:20",
     "- Hiện \"Đã chọn: 3 BL con\" và 3 thẻ tên BOM con.\n"
     "- Lưới hiển thị đúng thứ tự: A1, A2, B1, B2, C1, C2.\n"
     "- Hàng hoá xếp theo ngày tạo BOM thành phần tăng dần (cũ nhất lên đầu).",
     "Điều kiện nghiệm thu AC1 + AC2 của task."),

    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-02",
     "Thứ tự KHÔNG phụ thuộc thứ tự tick chọn BOM con", "P0",
     "Bộ dữ liệu như TC-BOM-SORT-01 (BL-A 09:00, BL-B 09:10, BL-C 09:20)",
     "1. Tạo BOM Tổng hợp, bấm \"Chọn BL con\".\n2. Tick theo thứ tự ngược: BL-C, rồi BL-A, rồi BL-B.\n"
     "3. Bấm \"Gộp BOM con\".\n4. Quan sát thứ tự dòng trên lưới.",
     "Thứ tự tick: C, A, B",
     "- Lưới vẫn hiển thị A1, A2, B1, B2, C1, C2.\n"
     "- KHÔNG xếp theo thứ tự người dùng tick (C, A, B).",
     "Trước khi sửa, lưới xếp theo thứ tự tick — đây là lỗi chính của task."),

    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-03",
     "Thứ tự KHÔNG phụ thuộc tên hay mã BOM con", "P0",
     "3 BOM Thành phần đặt tên ngược thứ tự bảng chữ cái so với giờ tạo:\n"
     "- \"Zeta\" tạo lúc 10:00 (hàng Z1)\n- \"Mu\" tạo lúc 10:10 (hàng M1)\n- \"Alpha\" tạo lúc 10:20 (hàng AL1)",
     "1. Tạo BOM Tổng hợp, chọn cả 3 BOM con.\n2. Bấm \"Gộp BOM con\".\n3. Quan sát thứ tự dòng.",
     "Zeta 10:00\nMu 10:10\nAlpha 10:20",
     "- Lưới hiển thị Z1, M1, AL1 (theo giờ tạo).\n"
     "- KHÔNG xếp theo tên A-Z (Alpha, Mu, Zeta).",
     "Tiêu chí sắp xếp duy nhất là ngày tạo BOM thành phần."),

    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-04",
     "Sắp theo ngày TẠO, không theo ngày cập nhật của BOM con", "P0",
     "Bộ dữ liệu như TC-BOM-SORT-01.\nSau khi tạo xong cả 3, mở BL-A (cũ nhất) sửa Số lượng hàng A1 rồi Lưu — BL-A thành BOM được cập nhật gần nhất.",
     "1. Tạo BOM Tổng hợp, chọn BL-A, BL-B, BL-C.\n2. Bấm \"Gộp BOM con\".\n3. Quan sát thứ tự dòng.",
     "BL-A: tạo sớm nhất, cập nhật muộn nhất",
     "- Hàng của BL-A vẫn đứng ĐẦU: A1, A2, B1, B2, C1, C2.\n"
     "- Việc sửa BOM con sau khi tạo KHÔNG làm đổi vị trí của nó.",
     "Phân biệt ngày tạo với ngày cập nhật."),

    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-05",
     "Bảng Dịch vụ & Chi phí khác cũng sắp theo ngày tạo BOM thành phần", "P0",
     "Bộ dữ liệu như TC-BOM-SORT-01, mỗi BOM con có thêm 1 dòng Dịch vụ & Chi phí khác:\n"
     "- BL-A: Vận chuyển\n- BL-B: Lắp đặt\n- BL-C: Bảo trì",
     "1. Tạo BOM Tổng hợp, tick theo thứ tự C, A, B.\n2. Bấm \"Gộp BOM con\".\n"
     "3. Quan sát khối Dịch vụ & Chi phí khác.",
     "Vận chuyển (BL-A)\nLắp đặt (BL-B)\nBảo trì (BL-C)",
     "- Khối Dịch vụ & Chi phí khác hiển thị: Vận chuyển, Lắp đặt, Bảo trì.\n"
     "- Đúng thứ tự ngày tạo BOM thành phần, không theo thứ tự tick.",
     "Task yêu cầu sắp cả hàng hoá LẪN dịch vụ."),

    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-06",
     "Giữ nguyên thứ tự các dòng bên trong cùng một BOM con", "P0",
     "BL-B (tạo giữa) có 3 hàng theo thứ tự đã lưu: B1, B2, B3.\nBL-A, BL-C như TC-BOM-SORT-01.",
     "1. Gộp BL-A, BL-B, BL-C.\n2. Quan sát cụm dòng thuộc BL-B.",
     "BL-B: B1, B2, B3",
     "- Cụm BL-B nằm giữa cụm BL-A và cụm BL-C.\n"
     "- Bên trong cụm giữ nguyên B1, B2, B3 như lúc lập BOM con.",
     "Chỉ sắp giữa các BOM con, không xáo trộn dòng bên trong 1 BOM."),

    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-07",
     "Hàng cha - con giữ nguyên cụm sau khi sắp xếp", "P1",
     "BL-B có 1 hàng cha \"Tủ điện\" kèm 2 hàng con \"Aptomat\", \"Rơ le\".\nBL-A, BL-C như TC-BOM-SORT-01.",
     "1. Tick theo thứ tự C, B, A.\n2. Bấm \"Gộp BOM con\".\n3. Quan sát cụm \"Tủ điện\".",
     "Tủ điện\n- Aptomat\n- Rơ le",
     "- \"Aptomat\", \"Rơ le\" vẫn nằm ngay dưới \"Tủ điện\" và thụt lề là hàng con.\n"
     "- Không có dòng của BOM khác chen vào giữa cụm cha - con.\n"
     "- Thành tiền dòng cha vẫn bằng tổng các dòng con.",
     "Sắp xếp không được làm vỡ cấu trúc cha - con."),

    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-08",
     "Gộp BOM con có nhóm hàng, nhóm trùng tên", "P1",
     "3 BOM con đều có nhóm:\n- BL-A (cũ nhất): nhóm \"Thiết bị mạng\" (A1)\n"
     "- BL-B: nhóm \"Phụ kiện\" (B1)\n- BL-C (mới nhất): nhóm \"Thiết bị mạng\" (C1)",
     "1. Tạo BOM Tổng hợp, tick theo thứ tự C, B, A.\n2. Bấm \"Gộp BOM con\".\n"
     "3. Quan sát danh sách nhóm và dòng trong từng nhóm.",
     "Nhóm trùng tên: \"Thiết bị mạng\"",
     "- Hai nhóm \"Thiết bị mạng\" gộp thành 1 nhóm.\n"
     "- Thứ tự nhóm: \"Thiết bị mạng\" rồi \"Phụ kiện\" (nhóm xuất hiện đầu tiên ở BOM cũ nhất).\n"
     "- Trong nhóm \"Thiết bị mạng\": A1 đứng trước C1.",
     "Kiểm tra sắp xếp khi có nhóm hàng."),

    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-09",
     "Gộp lại sau khi thêm một BOM con mới hơn", "P1",
     "Đang ở màn Tạo BOM Tổng hợp, đã gộp BL-A, BL-C.\nSau đó có thêm BL-Z tạo lúc 11:00 (hàng Z9).",
     "1. Bấm \"Chọn BL con\", giữ BL-A, BL-C và tick thêm BL-Z, BL-B.\n"
     "2. Bấm \"Gộp BOM con\".\n3. Quan sát thứ tự dòng.",
     "BL-Z 11:00 (mới nhất)",
     "- Lưới được sắp lại toàn bộ: A1, A2, B1, B2, C1, C2, Z9.\n"
     "- BL-B chèn đúng vào giữa, BL-Z nằm cuối.\n- Không còn dòng trùng từ lần gộp trước.",
     "Mỗi lần gộp lại phải sắp lại từ đầu, không nối thêm vào cuối."),

    ("Sắp xếp khi gộp BOM con", "TC-BOM-SORT-10",
     "Gộp chỉ 1 BOM con", "P2",
     "Có BL-B với 3 hàng B1, B2, B3 và 1 dòng dịch vụ \"Lắp đặt\"",
     "1. Tạo BOM Tổng hợp, chỉ tick BL-B.\n2. Bấm \"Gộp BOM con\".\n3. Quan sát lưới.",
     "1 BOM con",
     "- Lưới hiển thị B1, B2, B3 và dịch vụ \"Lắp đặt\" đúng thứ tự gốc.\n- Không lỗi, không mất dòng.",
     "Trường hợp biên: 1 BOM con."),

    # ---------------- Lưu & mở lại ----------------
    ("Lưu & mở lại", "TC-BOM-SORT-11",
     "Lưu nháp rồi mở lại vẫn giữ thứ tự", "P0",
     "Đã gộp BL-A, BL-B, BL-C (tick lộn xộn C, A, B), lưới đang hiển thị A1, A2, B1, B2, C1, C2",
     "1. Bấm \"Lưu nháp\".\n2. Về màn danh sách, mở lại BOM Tổng hợp vừa lưu (Sửa).\n"
     "3. Quan sát thứ tự hàng hoá và khối Dịch vụ & Chi phí khác.\n4. Tải lại trang (F5) và quan sát lần nữa.",
     "—",
     "- Thứ tự hàng hoá sau khi mở lại: A1, A2, B1, B2, C1, C2.\n"
     "- Dịch vụ: Vận chuyển, Lắp đặt, Bảo trì.\n- Tải lại trang thứ tự vẫn giữ nguyên.",
     "Task yêu cầu thứ tự được GHI NHẬN khi lưu, không chỉ đúng trên màn hình."),

    ("Lưu & mở lại", "TC-BOM-SORT-12",
     "Lưu BOM rồi xem chi tiết vẫn giữ thứ tự", "P0",
     "Như TC-BOM-SORT-11",
     "1. Bấm \"Lưu BOM\".\n2. Ở màn danh sách, bấm Xem BOM Tổng hợp vừa lưu.\n3. Quan sát thứ tự hàng hoá và dịch vụ.",
     "—",
     "- Màn chi tiết hiển thị đúng A1, A2, B1, B2, C1, C2.\n"
     "- Dịch vụ: Vận chuyển, Lắp đặt, Bảo trì.\n- Trạng thái BL-A, BL-B, BL-C chuyển \"Đã được tổng hợp\".",
     "Đối chiếu thứ tự sau khi lưu chính thức."),

    ("Lưu & mở lại", "TC-BOM-SORT-13",
     "Sửa BOM Tổng hợp đã lưu, gộp lại danh sách BOM con", "P1",
     "BOM Tổng hợp đã Lưu nháp với BL-A, BL-C.\nCó thêm BL-B (tạo giữa BL-A và BL-C) trạng thái Hoàn thành.",
     "1. Mở Sửa BOM Tổng hợp.\n2. Bấm \"Chọn BL con\", tick thêm BL-B.\n3. Bấm \"Gộp BOM con\", rồi \"Lưu nháp\".\n"
     "4. Mở lại BOM Tổng hợp.",
     "Thêm BL-B",
     "- Sau khi gộp: A1, A2, B1, B2, C1, C2.\n- Sau khi lưu và mở lại vẫn đúng thứ tự trên.",
     "Sắp xếp áp dụng cả ở màn Sửa, không riêng màn Tạo mới."),

    # ---------------- Liên thông ----------------
    ("Liên thông", "TC-BOM-SORT-14",
     "Xuất file chi tiết BOM giữ đúng thứ tự", "P1",
     "BOM Tổng hợp đã lưu với thứ tự A1, A2, B1, B2, C1, C2 và dịch vụ Vận chuyển, Lắp đặt, Bảo trì",
     "1. Mở BOM Tổng hợp.\n2. Bấm xuất file chi tiết BOM.\n3. Mở file Excel, đối chiếu thứ tự với màn hình.",
     "—",
     "- Thứ tự hàng hoá và dịch vụ trong file khớp 100% với màn hình.",
     "Thứ tự phải nhất quán ở mọi nơi hiển thị BOM."),

    ("Liên thông", "TC-BOM-SORT-15",
     "Báo giá tạo từ BOM Tổng hợp giữ đúng thứ tự", "P1",
     "BOM Tổng hợp ở TC-BOM-SORT-12 đã được duyệt",
     "1. Tạo báo giá từ BOM Tổng hợp này.\n2. Quan sát thứ tự dòng hàng hoá và dịch vụ trên báo giá.",
     "—",
     "- Báo giá hiển thị hàng hoá A1, A2, B1, B2, C1, C2.\n- Dịch vụ: Vận chuyển, Lắp đặt, Bảo trì.",
     "Báo giá kế thừa BOM phải giữ đúng thứ tự đã chốt."),

    # ---------------- Chặn cũ vẫn hoạt động ----------------
    ("Chặn khi gộp vẫn hoạt động", "TC-BOM-SORT-16",
     "Bấm \"Gộp BOM con\" khi chưa tick BOM nào", "P2",
     "Đang mở popup \"Chọn BOM con để gộp\", chưa tick dòng nào",
     "1. Bấm \"Gộp BOM con\".\n2. Quan sát thông báo.",
     "—",
     "- Hiện thông báo \"Chưa chọn BL con nào.\"\n- Lưới hàng hoá giữ nguyên.",
     "Đảm bảo phần sửa không làm hỏng chặn cũ."),

    ("Chặn khi gộp vẫn hoạt động", "TC-BOM-SORT-17",
     "BOM con khác loại tiền tệ vẫn bị chặn", "P1",
     "BOM Tổng hợp chọn loại tiền VND.\nBL-A, BL-B loại tiền VND; BL-C loại tiền USD.",
     "1. Tick BL-A, BL-B, BL-C.\n2. Bấm \"Gộp BOM con\".\n3. Quan sát thông báo và lưới.",
     "BL-C: USD",
     "- Hiện thông báo \"Loại tiền tệ không khớp: <mã BL-C>. BOM tổng hợp và BOM thành phần phải cùng loại tiền tệ.\"\n"
     "- Không gộp dữ liệu, lưới giữ nguyên như trước khi bấm.",
     "Đảm bảo phần sửa không làm hỏng chặn cũ."),

    ("Chặn khi gộp vẫn hoạt động", "TC-BOM-SORT-18",
     "BOM con khác cấu trúc nhóm vẫn bị chặn", "P1",
     "BL-A, BL-B có nhóm hàng; BL-C không có nhóm",
     "1. Tick cả 3 BOM con.\n2. Bấm \"Gộp BOM con\".\n3. Quan sát thông báo.",
     "BL-C không có nhóm",
     "- Hiện thông báo \"Các BOM con phải có cùng cấu trúc. BOM có nhóm: … BOM không có nhóm: …\"\n"
     "- Không gộp dữ liệu.",
     "Đảm bảo phần sửa không làm hỏng chặn cũ."),

    # ---------------- E2E ----------------
    ("E2E", "TC-BOM-SORT-19",
     "E2E tạo BOM thành phần → gộp → lưu → duyệt → báo giá", "P0",
     "Tài khoản có quyền \"Tạo BOM List\" và quyền duyệt BOM",
     "1. Tạo lần lượt 3 BOM Thành phần BL-A, BL-B, BL-C (cách nhau vài phút), mỗi BOM 2 hàng + 1 dịch vụ, Lưu BOM.\n"
     "2. Tạo BOM Tổng hợp, tick theo thứ tự C, A, B, bấm \"Gộp BOM con\".\n3. Lưu BOM, gửi duyệt và duyệt.\n"
     "4. Tạo báo giá từ BOM Tổng hợp.\n5. Đối chiếu thứ tự ở mọi bước.",
     "BL-A, BL-B, BL-C tạo cách nhau vài phút",
     "- Ở mọi bước (lưới sau khi gộp, màn chi tiết sau khi lưu, sau khi duyệt, báo giá) thứ tự luôn là hàng của BL-A → BL-B → BL-C.\n"
     "- Dịch vụ cũng theo thứ tự BL-A → BL-B → BL-C.",
     "Luồng thực tế từ đầu đến cuối."),
]

# ---------------------------------------------------------------- kiểm tra
ids = [t[1] for t in TCS]
assert len(ids) == len(set(ids)), "Trùng TC ID"
BANNED = [r"`[a-z_]{3,}`", r"\bBE\b", r"\bFE\b", r"\bHTTP\b", r"\b(400|403|404|422)\b",
          r"/api/v1", r"localStorage", r"created_at", r"updated_at", r"\bid\b", r"payload"]
text_all = "\n".join("\n".join(t) for t in TCS)
found = {p: len(re.findall(p, text_all)) for p in BANNED if re.findall(p, text_all)}
print("!!! CON THUAT NGU KY THUAT:", found) if found else print("OK - sach")
emoji = re.findall(r"[\u2190-\u21FF\u2600-\u2BFF\U0001F300-\U0001FAFF]", text_all)
print("!!! CON EMOJI:", set(emoji)) if emoji else print("OK - khong emoji")
p0 = sum(1 for t in TCS if t[3] == "P0")
print(f"Tong {len(TCS)} TC, P0 = {p0} ({p0 * 100 // len(TCS)}%)")

# ---------------------------------------------------------------- HTML (dán vào Sheets)
BASE = "font-family:'Times New Roman';font-size:11pt;border:1px solid #000;vertical-align:middle;white-space:pre-wrap;"
GREEN = "#93c47d"


def cell(v, extra="", attrs=""):
    v = html.escape(v).replace("\n", "<br>")
    return f'<td {attrs} style="{BASE}{extra}">{v}</td>'


rows = []
# dòng tiêu đề khối: A:B trống ghép, C:G ghép chữ, H:Q trống — cùng nền xanh như dòng 219
rows.append("<tr>" + cell("", f"background:{GREEN};", 'colspan="2"')
            + cell(SECTION, f"background:{GREEN};font-weight:bold;", 'colspan="5"')
            + "".join(cell("", f"background:{GREEN};") for _ in range(10)) + "</tr>")

group_span = {}
for t in TCS:
    group_span[t[0]] = group_span.get(t[0], 0) + 1

seen_group = set()
for i, (grp, tid, name, pri, pre, steps, data, exp, why) in enumerate(TCS):
    r = "<tr>"
    if i == 0:
        r += cell(MODULE, "font-weight:bold;", f'rowspan="{len(TCS)}"')
    if grp not in seen_group:
        seen_group.add(grp)
        r += cell(grp, "font-weight:bold;text-align:center;", f'rowspan="{group_span[grp]}"')
    r += cell(tid) + cell(name) + cell(pri) + cell(pre) + cell(steps) + cell(data) + cell(exp) + cell(why)
    r += cell("Not Executed", "font-size:12pt;text-align:center;")
    r += "".join(cell("") for _ in range(6))  # L..Q
    r += "</tr>"
    rows.append(r)

doc = ('<html><head><meta charset="utf-8"></head><body>'
       '<table style="border-collapse:collapse">' + "".join(rows) + "</table></body></html>")
html_path = os.path.join(HERE, "testcase-update-3107.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(doc)

# ---------------------------------------------------------------- TSV dự phòng
def q(v):
    return '"' + v.replace('"', '""') + '"' if ("\n" in v or '"' in v or "\t" in v) else v


tsv = ["\t\t" + SECTION]
for i, (grp, tid, name, pri, pre, steps, data, exp, why) in enumerate(TCS):
    tsv.append("\t".join(q(x) for x in [MODULE if i == 0 else "", grp, tid, name, pri, pre, steps, data, exp, why,
                                        "Not Executed"]))
with open(os.path.join(HERE, "testcase-update-3107.tsv"), "w", encoding="utf-8") as f:
    f.write("\n".join(tsv) + "\n")

# ---------------------------------------------------------------- clipboard (macOS, kiểu HTML)
if sys.platform == "darwin" and "--no-clip" not in sys.argv:
    hexd = doc.encode("utf-8").hex()
    subprocess.run(["osascript", "-e", f"set the clipboard to «data HTML{hexd}»"], check=True)
    print("Da dua bang HTML vao clipboard")
print("HTML:", html_path)
