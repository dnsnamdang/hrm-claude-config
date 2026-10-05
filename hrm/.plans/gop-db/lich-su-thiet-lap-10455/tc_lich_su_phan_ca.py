# -*- coding: utf-8 -*-
"""Testcase Redmine #10455 - hang muc 8 "Lich su phan ca" + hang muc 9 "Lich su phan ca theo tung nhan vien".

Chay: /opt/homebrew/opt/python@3.14/bin/python3.14 .plans/gop-db/lich-su-thiet-lap-10455/tc_lich_su_phan_ca.py
Xuat: testcase - Lich su phan ca.xlsx (gom man Lich su phan ca + popup theo tung nhan vien la section rieng).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

# ------------------------------------------------------------------ hang so dung chung
MENU = 'Vào phân hệ Chấm công -> menu "Ca làm việc" -> bấm "Lịch sử phân ca"'
MENU_GEN = 'Vào phân hệ Chấm công -> menu "Ca làm việc" -> bấm "Bảng phân ca tổng hợp"'
MENU_DET = 'Vào phân hệ Chấm công -> menu "Ca làm việc" -> bấm "Bảng phân ca chi tiết"'
DASH = 'dấu gạch ngang "-"'

CA_DATA = (
    "Danh mục ca làm việc có sẵn (tạo trước nếu chưa có):\n"
    "- HC_Ca hành chính (08:00 - 17:00)\n"
    "- KD_Ca kinh doanh (08:30 - 17:30)\n"
    "- TV_Ca tạp vụ (06:00 - 14:00)"
)
NV_DATA = (
    "Nhân viên đang làm việc, CHƯA có ca nào trong tháng 11/2026:\n"
    "- Nguyễn Văn A - KD1 - NV001 (phòng KD1)\n"
    "- Trần Thị B - KD1 - NV002 (phòng KD1)\n"
    "- Lê Văn C - KT - NV003 (phòng KT)"
)
USER = "Đăng nhập tài khoản U1 (phòng NSHC, tên Ngô Thị Lý) có quyền 'Phân ca theo công ty'"
PRE_BASE = USER + "\n" + CA_DATA + "\n" + NV_DATA


def E(action, source, old, new, nv, time, thu, override, desc, extra=None):
    """Ket qua mong doi cho 1 dong lich su tren man Lich su phan ca."""
    lines = [
        "Màn Lịch sử phân ca (mới nhất ở đầu) có 1 dòng mới:",
        "- Người thực hiện: NSHC - Ngô Thị Lý - <ngày giờ vừa thao tác, dd/mm/yyyy hh:mm>",
        "- Hành động: nhãn \"%s\"" % action,
        "- Nguồn phân ca: %s" % source,
        "- Ca làm việc cũ: %s" % old,
        "- Ca làm việc mới: %s" % new,
        "- Nhân viên (theo ca mới): %s" % nv,
        "- Thời gian làm việc (theo ca mới): %s" % time,
        "- Các thứ áp dụng (theo ca mới): %s" % thu,
        "- Có bị ghi đè ca không: %s" % override,
        "- Mô tả sự kiện: \"%s\"" % desc,
    ]
    if extra:
        lines.append(extra)
    return "\n".join(lines)


NV_AB = "2 dòng \"Nguyễn Văn A - KD1 - NV001\" và \"Trần Thị B - KD1 - NV002\""
NV_A = "\"Nguyễn Văn A - KD1 - NV001\""
SRC_T11 = "\"Phân ca chi tiết_PC Kinh doanh T11\""
SRC_GEN = "\"Phân ca tổng hợp\""
T2_T6 = "Thứ 2, Thứ 3, Thứ 4, Thứ 5, Thứ 6"
PRE_T11 = (
    PRE_BASE + "\n"
    "Đã có bảng phân ca chi tiết \"PC Kinh doanh T11\": 02/11/2026 - 27/11/2026, tích Thứ 2 đến Thứ 6 "
    "cùng ca HC_Ca hành chính, danh sách nhân viên: Nguyễn Văn A, Trần Thị B"
)
OPEN_T11 = "1. " + MENU_DET + "\n2. Bấm vào dòng \"PC Kinh doanh T11\" (mở màn Sửa chi tiết phân ca)"
CHECK_LS = "Mở màn Lịch sử phân ca (" + MENU + "), xem dòng đầu tiên"

# ------------------------------------------------------------------ 9 muc mo ta
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Ghi lại mọi lần thay đổi phân ca của nhân viên (ai đổi, lúc nào, từ ca nào sang ca nào, áp cho ngày/thứ nào, "
     "cho những nhân viên nào, có đè lên ca đã có không) từ 2 nguồn: Bảng phân ca chi tiết và Bảng phân ca tổng hợp.\n"
     "Có 2 nơi xem:\n"
     "- Màn \"Lịch sử phân ca\" (menu Ca làm việc) - xem toàn bộ theo phạm vi quyền, 11 cột, 11 ô lọc (2 ô khoảng ngày mỗi ô gồm Từ ngày và Đến ngày, tổng 13 ô nhập).\n"
     "- Popup \"Lịch sử chỉnh sửa - <Tên nhân viên>\" mở từ icon lịch sử cạnh tên nhân viên trên Bảng phân ca tổng hợp - "
     "chỉ các dòng có nhân viên đó, 9 cột (không có cột Nhân viên và Mô tả sự kiện), 1 ô tìm nhanh + 7 ô lọc."),
    ("2. Đối tượng được tính / hiển thị",
     "Mỗi dòng lịch sử = 1 nhóm (Hành động, Ca cũ, Ca mới) trong CÙNG 1 lần lưu; 1 lần lưu có thể sinh nhiều dòng.\n"
     "Các sự kiện được ghi (cột Mô tả sự kiện hiển thị đúng nguyên văn):\n"
     "- Tạo bảng chi tiết, nhân viên chưa có ca: Thêm mới - \"Tạo phân ca chi tiết mới\"\n"
     "- Tạo bảng chi tiết, nhân viên đã có ca ngày đó: Thêm mới - \"Tạo mới phân ca chi tiết có ghi đè ca làm việc của nhân viên\"\n"
     "- Thêm nhân viên vào bảng đã có: Thêm mới - \"Thêm nhân viên mới vào ca đã tồn tại\"\n"
     "- Sửa bảng làm đổi/thêm ca, không đè ca có sẵn: Sửa - \"Sửa phân ca chi tiết\"\n"
     "- Sửa bảng làm đổi ca đã có: Sửa - \"Sửa phân ca chi tiết có ghi đè ca làm việc của nhân viên\"\n"
     "- Bỏ nhân viên khỏi bảng: Xóa - \"Xóa nhân viên khỏi bảng phân ca chi tiết\"\n"
     "- Rút ngắn / dời ngày bắt đầu muộn hơn / bỏ 1 thứ: Xóa - \"Gỡ ca khỏi ngày làm việc của nhân viên\"\n"
     "- Xóa bảng chi tiết: Xóa - \"Xóa bảng phân ca chi tiết\"\n"
     "- Bảng tổng hợp gán ô trống: Thêm mới - \"Phân ca trên bảng phân ca tổng hợp\"\n"
     "- Bảng tổng hợp đổi ca ô đã có: Sửa - \"Sửa ca trên bảng phân ca tổng hợp\"\n"
     "- Bảng tổng hợp xóa ca: Xóa - \"Xóa ca trên bảng phân ca tổng hợp\""),
    ("3. Đối tượng bị ẩn / không tính",
     "- Lưu mà không đổi ca của ai (kể cả chỉ đổi Tên bảng phân ca): KHÔNG sinh dòng.\n"
     "- Chọn lại đúng ca đang có trên 1 ô bảng tổng hợp: KHÔNG sinh dòng.\n"
     "- Lưu bị chặn (thiếu trường bắt buộc, bấm Huỷ ở popup \"Xác nhận tạo mới\" khi trùng ca, bấm Không/Huỷ ở popup xác nhận xóa): KHÔNG sinh dòng.\n"
     "- Xóa bảng chi tiết chỉ gỡ và ghi lịch sử các ngày TỪ NGÀY MAI; ngày hôm nay và quá khứ giữ nguyên, không ghi.\n"
     "- Dòng không thuộc phạm vi quyền của người xem: ẩn hoàn toàn."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "- \"Ngày làm việc\" (từ - đến) lọc theo cột Thời gian làm việc, quy tắc BAO TRÙM: chỉ nhập Từ -> ngày bắt đầu của dòng >= Từ; "
     "chỉ nhập Đến -> ngày kết thúc của dòng <= Đến; nhập cả hai -> khoảng Từ - Đến phải chứa trọn khoảng của dòng (dòng chỉ giao 1 phần bị loại).\n"
     "- \"Ngày thực hiện chỉnh sửa\" (popup gọi là \"Ngày chỉnh sửa\") lọc theo ngày trong cột Người thực hiện, tính cả 2 đầu mút."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng 11 cột màn chính: STT | Người thực hiện | Hành động | Nguồn phân ca | Ca làm việc cũ | Ca làm việc mới | "
     "Nhân viên (theo ca mới) | Thời gian làm việc (theo ca mới) | Các thứ áp dụng (theo ca mới) | Có bị ghi đè ca không | Mô tả sự kiện.\n"
     "Popup theo nhân viên 9 cột: bỏ cột Nhân viên (theo ca mới) và Mô tả sự kiện.\n"
     "Tên nhân viên, phòng ban, tên/mã ca, tên bảng được CHỤP LẠI tại thời điểm ghi - đổi tên ca/xóa ca/nhân viên chuyển phòng về sau không làm đổi dòng cũ."),
    ("6. Quy tắc cộng dồn / deduplicate",
     "- Trong 1 lần lưu, các nhân viên cùng (Hành động, Ca cũ, Ca mới) gộp thành 1 dòng; khác ca cũ hoặc khác ca mới -> tách dòng.\n"
     "- Vì vậy khi tạo bảng có cả người đã có ca và người chưa có ca -> 2 dòng (Có / Không ghi đè).\n"
     "- Thời gian làm việc = ngày nhỏ nhất - ngày lớn nhất trong nhóm; Các thứ áp dụng = các thứ xuất hiện trong nhóm, xếp Thứ 2 -> Chủ nhật.\n"
     "- Thứ 7 tách (lẻ)/(chẵn) theo số tuần trong năm: tháng 11/2026 thì 07/11 và 21/11 là Thứ 7 (lẻ); 14/11 và 28/11 là Thứ 7 (chẵn)."),
    ("7. Phân quyền cấp",
     "Dùng lại 3 quyền phân ca (nhóm Chấm công):\n"
     "- 'Phân ca theo công ty': thấy mọi dòng ghi cho công ty đang chọn làm việc.\n"
     "- 'Phân ca theo phòng ban': thấy dòng có ít nhất 1 nhân viên thuộc phòng ban hoặc bộ phận mình quản lý.\n"
     "- 'Phân ca theo bộ phận': thấy dòng có ít nhất 1 nhân viên thuộc bộ phận mình quản lý.\n"
     "Có nhiều quyền thì lấy quyền rộng nhất (công ty > phòng ban > bộ phận). Dòng đã thấy thì hiện nguyên vẹn (đủ mọi nhân viên của dòng).\n"
     "Không có quyền nào: không thấy menu Lịch sử phân ca (và cả Bảng phân ca tổng hợp/chi tiết), mở màn bằng dấu trang cũ bị chuyển sang trang báo không tìm thấy."),
    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a–b / N\" dưới bảng: a là dòng đầu trang, b là dòng cuối trang, N là tổng số dòng khớp bộ lọc.\n"
     "- Cột Nhân viên: dưới 20 người liệt kê từng người \"Tên - Mã phòng - Mã NV\"; từ 20 người trở lên hiện \"N nhân viên\" + nút tải Excel.\n"
     "- Cột STT đánh tiếp theo trang (trang 2, 10 dòng/trang bắt đầu từ 11)."),
    ("9. Ghi chú đọc bảng",
     "- Màn chính mặc định 10 dòng/trang (chọn 5/10/20/50/100); popup mặc định 20 (chọn 20/50/100). Sắp xếp mới nhất lên đầu.\n"
     "- Ô trống hiển thị dấu gạch ngang \"-\". Có bị ghi đè: Có / Không; dòng Xóa (ca mới trống) hiển thị gạch ngang.\n"
     "- Chọn 1 ô lọc dạng danh sách là tìm ngay; bộ lọc màn chính được ghi nhớ 10 phút.\n"
     "- Sửa bảng chi tiết: phạm vi ghi lại tính từ Ngày bắt đầu của bảng (kể cả ngày đã qua) - sửa ca Thứ 2 của bảng bắt đầu từ tháng trước sẽ ghi cả các Thứ 2 đã qua.\n"
     "- Cột Người thực hiện lấy tên + mã phòng HIỆN TẠI của người thao tác (không chụp lại) - người đó chuyển phòng thì dòng cũ đổi theo mã phòng mới.\n"
     "- CHƯA LÀM (chờ khách chốt), KHÔNG có testcase: sự kiện \"Nhân viên nghỉ việc\" (spec dòng 8) - hiện chuyển nhân viên sang nghỉ việc KHÔNG sinh dòng lịch sử phân ca.\n"
     "- Điểm lệch spec đang theo code (chờ chốt): Xóa nhân viên khỏi bảng / gỡ ca hiển thị Có bị ghi đè = gạch ngang (spec ghi \"Không\"); "
     "xóa bảng vẫn liệt kê nhân viên + thời gian bị gỡ (spec để trống); ô chọn Ca cũ/Ca mới chỉ liệt kê ca đã từng xuất hiện trong lịch sử "
     "(spec: toàn bộ danh mục ca); ô Công ty/Phòng ban liệt kê toàn bộ, không lọc theo phạm vi quyền; ô Người thực hiện ở màn chính liệt kê toàn bộ nhân viên "
     "(popup theo nhân viên chỉ liệt kê người đã từng thao tác phân ca).\n"
     "- Ô lọc ở cả màn chính và popup dùng nhãn nổi (tên ô nằm trong ô, chọn giá trị thì nhãn dời lên viền) nên KHÔNG có placeholder riêng; "
     "riêng 2 ô khoảng ngày hiện chữ gợi ý \"Từ ngày\" và \"Đến ngày\"."),
]

# ------------------------------------------------------------------ PHAN QUYEN
ROLE_TCS = [
    ("00", "Quyền 'Phân ca theo công ty' - thấy toàn bộ lịch sử của công ty", "P0",
     "Tài khoản U1 chỉ có quyền 'Phân ca theo công ty', đang làm việc ở công ty TPE.\n"
     "Công ty TPE có 12 dòng lịch sử phân ca (phòng KD1: 5, KT: 4, NSHC: 3); công ty ETEK có 4 dòng.",
     "1. " + MENU + "\n2. Xem ô tổng dưới bảng",
     "Không nhập bộ lọc",
     "- Menu \"Lịch sử phân ca\" hiển thị trong nhóm Ca làm việc.\n"
     "- Bảng hiện đủ 12 dòng của TPE (Hiển thị 1–10 / 12), KHÔNG có dòng nào của ETEK."),
    ("01", "Quyền 'Phân ca theo phòng ban' - chỉ dòng có nhân viên thuộc phòng/bộ phận mình quản lý", "P0",
     "Tài khoản U2 chỉ có quyền 'Phân ca theo phòng ban', quản lý phòng KD1.\n"
     "Dữ liệu như TC-ROLE-00 (KD1: 5 dòng, KT: 4 dòng, NSHC: 3 dòng).",
     "1. Đăng nhập U2\n2. " + MENU,
     "Không nhập bộ lọc",
     "- Thấy đúng 5 dòng có nhân viên phòng KD1.\n- Không thấy dòng chỉ gồm nhân viên KT hoặc NSHC."),
    ("02", "Quyền 'Phân ca theo bộ phận' - chỉ dòng có nhân viên thuộc bộ phận mình quản lý", "P0",
     "Tài khoản U3 chỉ có quyền 'Phân ca theo bộ phận', quản lý bộ phận KD1-Bán lẻ (thuộc KD1).\n"
     "Trong 5 dòng của KD1 có 2 dòng chứa nhân viên bộ phận KD1-Bán lẻ.",
     "1. Đăng nhập U3\n2. " + MENU,
     "Không nhập bộ lọc",
     "- Thấy đúng 2 dòng.\n- 3 dòng còn lại của KD1 (không có ai thuộc bộ phận KD1-Bán lẻ) không hiển thị."),
    ("03", "Không có quyền phân ca nào - không thấy menu và icon lịch sử", "P0",
     "Tài khoản U4 không có quyền 'Phân ca theo công ty', 'Phân ca theo phòng ban', 'Phân ca theo bộ phận'.",
     "1. Đăng nhập U4\n2. Vào phân hệ Chấm công, mở menu \"Ca làm việc\"",
     "Không",
     "- Không có mục \"Lịch sử phân ca\" (cũng không có \"Bảng phân ca tổng hợp\", \"Bảng phân ca chi tiết\").\n"
     "- Do không vào được Bảng phân ca tổng hợp nên không có icon lịch sử cạnh tên nhân viên."),
    ("04", "Không có quyền - mở màn bằng dấu trang đã lưu bị chặn", "P0",
     "Tài khoản U4 như TC-ROLE-03. Trình duyệt có dấu trang (bookmark) màn Lịch sử phân ca lưu từ tài khoản U1.",
     "1. Đăng nhập U4\n2. Bấm dấu trang màn Lịch sử phân ca",
     "Không",
     "- Hệ thống chuyển sang trang báo không tìm thấy, không hiển thị bảng lịch sử, không lộ dòng nào."),
    ("05", "Có đồng thời nhiều quyền - lấy phạm vi rộng nhất", "P1",
     "Tài khoản U5 có cả 'Phân ca theo bộ phận' và 'Phân ca theo công ty' (công ty TPE, 12 dòng).",
     "1. Đăng nhập U5\n2. " + MENU,
     "Không",
     "Thấy đủ 12 dòng của công ty TPE (theo quyền công ty), không bị thu hẹp về phạm vi bộ phận."),
    ("06", "Dòng có nhiều nhân viên, chỉ 1 phần thuộc phạm vi - dòng hiện nguyên vẹn", "P1",
     "U2 quản lý phòng KD1. Có 1 dòng Thêm mới gồm 3 nhân viên: Nguyễn Văn A (KD1), Trần Thị B (KD1), Lê Văn C (KT).",
     "1. Đăng nhập U2\n2. " + MENU + "\n3. Xem cột Nhân viên của dòng trên",
     "Không",
     "- Dòng hiển thị.\n- Cột Nhân viên liệt kê đủ 3 người, kể cả Lê Văn C (phòng KT) - dòng hiện nguyên vẹn, không cắt bớt."),
    ("07", "Phạm vi theo phòng ban tại thời điểm ghi lịch sử", "P1",
     "U2 quản lý phòng KD1. Ngày 02/11 U1 phân ca cho Lê Văn C khi C còn ở phòng KT (1 dòng chỉ có C).\n"
     "Ngày 05/11 C được chuyển sang phòng KD1.",
     "1. Đăng nhập U2\n2. " + MENU,
     "Không",
     "- Dòng ngày 02/11 của Lê Văn C KHÔNG hiển thị với U2 (lúc ghi C thuộc KT).\n"
     "- Các thay đổi phân ca của C sau ngày 05/11 thì U2 thấy."),
    ("08", "Quyền công ty - đổi công ty làm việc thì danh sách đổi theo", "P1",
     "U1 có quyền 'Phân ca theo công ty' ở cả TPE (12 dòng) và ETEK (4 dòng).",
     "1. " + MENU + "\n2. Bấm biểu tượng chuyển công ty ở thanh trên, chọn ETEK\n3. Mở lại màn Lịch sử phân ca",
     "Công ty: ETEK",
     "Bảng chỉ còn 4 dòng của ETEK, không còn dòng của TPE."),
    ("09", "Ô chọn trong bộ lọc chỉ gồm giá trị trong phạm vi quyền", "P2",
     "U3 (quyền bộ phận) chỉ thấy 2 dòng: bảng \"PC Bán lẻ\", ca HC và KD.\n"
     "Công ty còn bảng \"PC Kỹ thuật\" và ca TV mà U3 không thấy.",
     "1. Đăng nhập U3\n2. " + MENU + "\n3. Mở ô \"Tên bảng phân ca chi tiết\", \"Ca mới\", \"Ca cũ\"",
     "Không",
     "- Ô Tên bảng phân ca chi tiết chỉ có \"PC Bán lẻ\".\n- Ô Ca mới/Ca cũ không có TV_Ca tạp vụ."),
]

# ------------------------------------------------------------------ I. HIEN THI
SEC_I = [
    (1, "Mở màn qua menu", "P0",
     USER + "\nCó 22 dòng lịch sử.",
     "1. " + MENU,
     "Không",
     "- Tiêu đề trang \"Lịch sử phân ca\".\n"
     "- Khối \"Bộ lọc danh sách\" đang mở sẵn: góc phải có nút \"Cài đặt bộ lọc\" và \"Ẩn tìm kiếm nâng cao\"; dưới các ô lọc có nút \"Tìm kiếm\", \"Làm mới\".\n"
     "- Bảng tiêu đề \"Lịch sử phân ca\", 10 dòng/trang, dưới bảng \"Hiển thị 1–10 / 22\".\n"
     "- Cuối trang có nút \"Quay lại\"."),
    (2, "Đủ 11 cột đúng nhãn và thứ tự", "P0",
     USER, "1. " + MENU + "\n2. Đọc dòng tiêu đề bảng",
     "Không",
     "Đúng thứ tự: STT | Người thực hiện | Hành động | Nguồn phân ca | Ca làm việc cũ | Ca làm việc mới | Nhân viên (theo ca mới) | "
     "Thời gian làm việc (theo ca mới) | Các thứ áp dụng (theo ca mới) | Có bị ghi đè ca không | Mô tả sự kiện"),
    (3, "Cột Người thực hiện: Mã phòng ban - Tên - Thời gian", "P0",
     USER + "\nU1 vừa phân ca lúc 09:05 ngày 01/10/2026.",
     "1. " + MENU + "\n2. Xem cột Người thực hiện của dòng đầu",
     "Không",
     "Hiển thị \"NSHC - Ngô Thị Lý - 01/10/2026 09:05\"\n- Thứ tự: mã phòng ban, tên, ngày dd/mm/yyyy giờ hh:mm; chữ thường, không in đậm."),
    (4, "Người thực hiện không có phòng ban", "P2",
     "Tài khoản quản trị \"Quản trị hệ thống\" chưa gắn phòng ban, có quyền 'Phân ca theo công ty', vừa phân ca 1 ô.",
     "1. " + MENU + "\n2. Xem cột Người thực hiện của dòng đầu",
     "Không",
     "Hiển thị \"Quản trị hệ thống - <dd/mm/yyyy hh:mm>\"\n- Không có dấu \" - \" thừa ở đầu."),
    (5, "Cột Nguồn phân ca", "P0",
     "Có 1 dòng từ bảng chi tiết \"PC Kinh doanh T11\" và 1 dòng từ Bảng phân ca tổng hợp.",
     "1. " + MENU + "\n2. Xem cột Nguồn phân ca 2 dòng",
     "Không",
     "- Dòng từ bảng chi tiết: \"Phân ca chi tiết_PC Kinh doanh T11\".\n- Dòng từ bảng tổng hợp: \"Phân ca tổng hợp\"."),
    (6, "Cột Ca làm việc cũ/mới dạng mã ca_tên ca", "P0",
     CA_DATA + "\nCó dòng Sửa đổi từ HC sang KD; có dòng Thêm mới (không có ca cũ).",
     "1. " + MENU + "\n2. Xem 2 cột ca",
     "Không",
     "- Dòng Sửa: Ca làm việc cũ \"HC_Ca hành chính\", Ca làm việc mới \"KD_Ca kinh doanh\".\n"
     "- Dòng Thêm mới: Ca làm việc cũ hiển thị " + DASH + "."),
    (7, "Cột Thời gian làm việc: 1 ngày / khoảng ngày", "P1",
     "Có 1 dòng từ bảng tổng hợp ngày 03/11/2026 và 1 dòng từ bảng chi tiết 02/11/2026 - 27/11/2026.",
     "1. " + MENU + "\n2. Xem cột Thời gian làm việc",
     "Không",
     "- Dòng 1 ngày: \"03/11/2026\" (không lặp 2 lần).\n- Dòng khoảng: \"02/11/2026 - 27/11/2026\"."),
    (8, "Cột Các thứ áp dụng - thứ tự và Thứ 7 chẵn/lẻ", "P1",
     "Có dòng tạo từ bảng áp dụng Chủ nhật, Thứ 7 (chẵn), Thứ 2, Thứ 7 (lẻ) trong tháng 11/2026.",
     "1. " + MENU + "\n2. Xem cột Các thứ áp dụng",
     "Không",
     "Hiển thị đúng thứ tự tuần: \"Thứ 2, Thứ 7 (lẻ), Thứ 7 (chẵn), Chủ nhật\"."),
    (9, "Cột Có bị ghi đè ca không: Có / Không / gạch ngang", "P0",
     "Có 3 dòng: Thêm mới cho người đã có ca; Thêm mới cho người chưa có ca; Xóa ca.",
     "1. " + MENU + "\n2. Xem cột Có bị ghi đè ca không",
     "Không",
     "- Người đã có ca: \"Có\".\n- Người chưa có ca: \"Không\".\n- Dòng Xóa: " + DASH + "."),
    (10, "Cột Hành động - nhãn và màu", "P1",
     "Có đủ 3 loại dòng Thêm mới, Sửa, Xóa.",
     "1. " + MENU + "\n2. Xem cột Hành động",
     "Không",
     "- \"Thêm mới\" nhãn màu xanh lá.\n- \"Sửa\" nhãn màu cam.\n- \"Xóa\" nhãn màu đỏ."),
    (11, "Cột Nhân viên dưới 20 người - liệt kê từng người", "P0",
     NV_DATA + "\nCó dòng gồm 3 người A, B, C.",
     "1. " + MENU + "\n2. Xem cột Nhân viên (theo ca mới)",
     "Không",
     "- Liệt kê 3 dòng, mỗi người 1 dòng dạng \"Tên - Mã phòng - Mã NV\", ví dụ \"Nguyễn Văn A - KD1 - NV001\".\n"
     "- Không có nút tải Excel."),
    (12, "Cột Nhân viên - biên 19 và 20 người", "P0",
     "Có 2 dòng: 1 dòng gồm 19 nhân viên, 1 dòng gồm 20 nhân viên.",
     "1. " + MENU + "\n2. Xem cột Nhân viên 2 dòng",
     "Không",
     "- Dòng 19 người: liệt kê đủ 19 tên, khung cuộn dọc được, không đẩy dòng cao quá mức.\n"
     "- Dòng 20 người: hiện \"20 nhân viên\" và nút tải (biểu tượng tải xuống, di chuột hiện \"Tải danh sách nhân viên\")."),
    (13, "Mô tả sự kiện hiển thị đầy đủ, xuống dòng trong ô", "P2",
     "Có dòng \"Tạo mới phân ca chi tiết có ghi đè ca làm việc của nhân viên\".",
     "1. " + MENU + "\n2. Xem cột Mô tả sự kiện",
     "Không",
     "Câu hiển thị đủ, tự xuống dòng trong ô, không bị cắt \"...\"."),
    (14, "Lịch sử giữ nguyên khi ca bị đổi tên / xóa sau đó", "P1",
     "Có dòng ca mới \"TV_Ca tạp vụ\". Sau đó ở danh mục ca làm việc đổi tên ca TV thành \"Ca vệ sinh\".",
     "1. " + MENU + "\n2. Xem dòng cũ",
     "Không",
     "Dòng cũ vẫn hiển thị \"TV_Ca tạp vụ\" (tên tại thời điểm phân ca), không đổi thành tên mới."),
    (15, "Lịch sử giữ nguyên thông tin nhân viên khi nhân viên chuyển phòng", "P1",
     "Dòng cũ có \"Lê Văn C - KT - NV003\".\nSau đó C chuyển sang phòng KD1.",
     "1. " + MENU + "\n2. Xem cột Nhân viên dòng cũ",
     "Không",
     "Vẫn hiển thị \"Lê Văn C - KT - NV003\"\n(mã phòng lúc phân ca, không đổi theo phòng mới)."),
    (16, "Nút Quay lại", "P2",
     "Đang ở Bảng phân ca chi tiết, rồi vào menu Lịch sử phân ca.",
     "1. Bấm \"Quay lại\" ở cuối màn",
     "Không",
     "Trở về màn trước đó (Bảng phân ca chi tiết)."),
]

# ------------------------------------------------------------------ II. BO LOC
PRE_F = USER + "\nCó 22 dòng lịch sử, công ty TPE (KD1, KT), ETEK; ca HC/KD/TV; 2 bảng \"PC Kinh doanh T11\", \"PC Kỹ thuật T11\"."
SEC_II = [
    (1, "Lọc Công ty", "P0", PRE_F + "\nNhân viên công ty ETEK có 4 dòng (U1 có quyền ở ETEK).",
     "1. " + MENU + "\n2. Chọn ô \"Công ty\"",
     "Công ty: ETEK",
     "- Tìm ngay không cần bấm Tìm kiếm.\n- Chỉ còn các dòng có nhân viên thuộc ETEK."),
    (2, "Lọc Phòng ban - danh sách phòng theo công ty đã chọn", "P0", PRE_F,
     "1. " + MENU + "\n2. Chọn Công ty TPE\n3. Mở ô \"Phòng ban\", chọn KD1",
     "Công ty: TPE; Phòng ban: KD1",
     "- Ô Phòng ban chỉ liệt kê phòng của TPE.\n- Bảng chỉ còn dòng có nhân viên thuộc KD1 (5 dòng)."),
    (3, "Lọc Nhân viên - danh sách theo công ty/phòng, có cả người đã nghỉ", "P0",
     PRE_F + "\nNhân viên Phạm D (KD1) đã nghỉ việc, có 1 dòng lịch sử.",
     "1. " + MENU + "\n2. Chọn Phòng ban KD1\n3. Mở ô \"Nhân viên\", chọn Nguyễn Văn A\n4. Đổi sang chọn Phạm D",
     "Nhân viên: Nguyễn Văn A, rồi Phạm D",
     "- Ô Nhân viên chỉ liệt kê người KD1, dạng \"Tên - Mã phòng - Mã NV\", có cả Phạm D đã nghỉ.\n"
     "- Chọn A: chỉ dòng có A. Chọn Phạm D: hiện 1 dòng của D."),
    (4, "Đổi Công ty thì Phòng ban và Nhân viên đã chọn bị xóa", "P1", PRE_F,
     "1. Chọn Công ty TPE, Phòng ban KD1, Nhân viên Nguyễn Văn A\n2. Đổi Công ty sang ETEK",
     "Công ty: TPE -> ETEK",
     "- Ô Phòng ban và Nhân viên tự trống.\n- Danh sách tải lại 1 lần theo Công ty ETEK."),
    (5, "Lọc Hành động", "P0", PRE_F,
     "1. Mở ô \"Hành động\"\n2. Lần lượt chọn Thêm mới, Sửa, Xóa",
     "Hành động: Thêm mới / Sửa / Xóa",
     "- Ô có đúng 3 lựa chọn Thêm mới, Sửa, Xóa.\n- Mỗi lần chọn, bảng chỉ còn dòng đúng hành động đó."),
    (6, "Lọc Nguồn phân ca - chọn nhiều", "P0", PRE_F,
     "1. Ô \"Nguồn phân ca\" chọn \"Phân ca chi tiết\"\n2. Chọn thêm \"Phân ca tổng hợp\"",
     "Nguồn: Phân ca chi tiết; rồi cả 2",
     "- Chọn 1: chỉ dòng nguồn \"Phân ca chi tiết_...\".\n- Chọn cả 2: hiện đủ 22 dòng."),
    (7, "Ngày làm việc - chỉ nhập Từ", "P0",
     PRE_F + "\nDòng X: 02/11/2026 - 27/11/2026; dòng Y: 30/10/2026 - 05/11/2026; dòng Z: 03/11/2026.",
     "1. Ô \"Ngày làm việc\" chỉ chọn ngày Từ",
     "Từ: 01/11/2026",
     "Hiện X và Z (ngày bắt đầu từ 01/11 trở đi); KHÔNG hiện Y (bắt đầu 30/10)."),
    (8, "Ngày làm việc - chỉ nhập Đến", "P0", "Dữ liệu như TC trên.",
     "1. Ô \"Ngày làm việc\" chỉ chọn ngày Đến",
     "Đến: 05/11/2026",
     "Hiện Y và Z (ngày kết thúc đến hết 05/11); KHÔNG hiện X (kết thúc 27/11)."),
    (9, "Ngày làm việc - nhập cả 2 đầu, quy tắc bao trùm", "P0", "Dữ liệu như TC trên.",
     "1. Chọn Từ 01/11/2026 Đến 10/11/2026",
     "Từ 01/11/2026 - Đến 10/11/2026",
     "- Chỉ hiện Z (03/11 nằm trọn trong khoảng).\n- KHÔNG hiện Y (bắt đầu trước khoảng) và X (kết thúc sau khoảng) dù có giao nhau 1 phần."),
    (10, "Ngày làm việc - khoảng trùng khít", "P2", "Dữ liệu như TC trên.",
     "1. Chọn Từ 02/11/2026 Đến 27/11/2026",
     "Từ 02/11/2026 - Đến 27/11/2026",
     "Hiện X (khớp đúng 2 đầu mút) và Z."),
    (11, "Lọc Người thực hiện", "P0", PRE_F + "\nU1 thực hiện 15 dòng, U6 (Phạm Doãn Chiến) thực hiện 7 dòng.",
     "1. Ô \"Người thực hiện\" chọn Phạm Doãn Chiến",
     "Người thực hiện: Phạm Doãn Chiến",
     "- Ô Người thực hiện liệt kê nhân viên dạng \"Tên - Mã phòng - Mã NV\" (ví dụ \"Phạm Doãn Chiến - NSHC - NV006\").\n- Bảng còn đúng 7 dòng, cột Người thực hiện đều là Phạm Doãn Chiến."),
    (12, "Lọc Ca mới", "P0", PRE_F,
     "1. Mở ô \"Ca mới\", chọn KD_Ca kinh doanh",
     "Ca mới: KD_Ca kinh doanh",
     "- Ô hiển thị lựa chọn dạng \"mã ca_tên ca\".\n- Bảng chỉ còn dòng có Ca làm việc mới = KD_Ca kinh doanh."),
    (13, "Lọc Ca cũ - có cả ca đã bị xóa khỏi danh mục", "P0",
     PRE_F + "\nCa \"CA3_Ca đêm\" từng được phân rồi bị đổi sang HC, sau đó ca CA3 bị xóa khỏi danh mục.",
     "1. Mở ô \"Ca cũ\", chọn CA3_Ca đêm",
     "Ca cũ: CA3_Ca đêm",
     "- CA3_Ca đêm vẫn có trong danh sách chọn.\n- Bảng chỉ còn dòng có Ca làm việc cũ = CA3_Ca đêm."),
    (14, "Lọc Tên bảng phân ca chi tiết - hiện tên mới nhất, có cả bảng đã xóa", "P0",
     PRE_F + "\nBảng \"PC Kỹ thuật T11\" đã đổi tên thành \"PC Kỹ thuật T11-v2\". Bảng \"PC Tạm\" đã bị xóa.",
     "1. Mở ô \"Tên bảng phân ca chi tiết\"\n2. Chọn \"PC Kỹ thuật T11-v2\"\n3. Đổi sang \"PC Tạm\"",
     "Tên bảng: PC Kỹ thuật T11-v2; PC Tạm",
     "- Danh sách có \"PC Kỹ thuật T11-v2\" (tên mới, không lặp tên cũ) và \"PC Tạm\".\n"
     "- Chọn \"PC Kỹ thuật T11-v2\": hiện mọi dòng của bảng đó, kể cả dòng ghi trước khi đổi tên (các dòng cũ vẫn mang tên cũ).\n"
     "- Chọn \"PC Tạm\": hiện các dòng của bảng đã xóa."),
    (15, "Ngày thực hiện chỉnh sửa - chỉ nhập Từ", "P1", PRE_F + "\nCác dòng thực hiện vào 20/07, 23/07, 27/07/2026.",
     "1. Ô \"Ngày thực hiện chỉnh sửa\" chọn Từ 23/07/2026",
     "Từ: 23/07/2026",
     "Hiện dòng ngày 23/07 và 27/07 (tính cả ngày 23/07); không hiện 20/07."),
    (16, "Ngày thực hiện chỉnh sửa - chỉ nhập Đến", "P1", "Dữ liệu như TC trên.",
     "1. Chọn Đến 23/07/2026",
     "Đến: 23/07/2026",
     "Hiện dòng 20/07 và 23/07 (dòng lúc 23:59 ngày 23/07 vẫn hiện); không hiện 27/07."),
    (17, "Ngày thực hiện chỉnh sửa - nhập cả 2 đầu", "P0", "Dữ liệu như TC trên.",
     "1. Chọn Từ 23/07/2026 Đến 23/07/2026",
     "Từ = Đến = 23/07/2026",
     "Chỉ hiện dòng thực hiện trong ngày 23/07/2026."),
    (18, "Kết hợp nhiều bộ lọc", "P1", PRE_F,
     "1. Chọn Phòng ban KD1, Hành động Xóa, Nguồn Phân ca chi tiết",
     "KD1 + Xóa + Phân ca chi tiết",
     "Chỉ còn dòng thỏa ĐỒNG THỜI cả 3 điều kiện."),
    (19, "Không có dòng nào khớp", "P1", PRE_F,
     "1. Chọn Ca mới TV_Ca tạp vụ và Hành động Xóa (không có dòng nào như vậy)",
     "Ca mới TV + Xóa",
     "Bảng hiện \"Không có dữ liệu phù hợp bộ lọc.\" (chữ xám), \"Hiển thị 0\"."),
    (20, "Nút Làm mới", "P0", PRE_F,
     "1. Chọn 4 bộ lọc bất kỳ, sang trang 2\n2. Bấm \"Làm mới\"",
     "Không",
     "- Mọi ô lọc về trống (kể cả 2 ô khoảng ngày).\n- Bảng về trang 1, hiện đủ 22 dòng."),
    (21, "Bộ lọc được ghi nhớ 10 phút", "P2", PRE_F,
     "1. Chọn Hành động = Sửa\n2. Sang màn khác rồi quay lại trong vòng 10 phút\n3. Quay lại sau hơn 10 phút",
     "Hành động: Sửa",
     "- Trong 10 phút: ô Hành động vẫn là Sửa, bảng đã lọc.\n- Sau 10 phút: bộ lọc về trống."),
    (22, "Ẩn / hiện tìm kiếm nâng cao", "P2", PRE_F,
     "1. Bấm \"Ẩn tìm kiếm nâng cao\"\n2. Bấm lại để hiện",
     "Không",
     "- Bước 1: khối 11 ô lọc cùng nút \"Tìm kiếm\", \"Làm mới\" ẩn đi; nút đổi chữ thành \"Tìm kiếm nâng cao\".\n"
     "- Bước 2: khối ô lọc hiện lại, nút trở về \"Ẩn tìm kiếm nâng cao\".\n- Điều kiện đang lọc không bị mất."),
    (23, "Đủ 11 ô lọc đúng nhãn, thứ tự và chữ gợi ý", "P0", PRE_F,
     "1. " + MENU + "\n2. Đọc nhãn các ô trong khối Bộ lọc danh sách (trái sang phải, trên xuống dưới)\n3. Bấm vào ô Ngày làm việc và ô Ngày thực hiện chỉnh sửa",
     "Không",
     "- Đúng 11 ô theo thứ tự: Công ty | Phòng ban | Nhân viên | Hành động | Nguồn phân ca | Ngày làm việc | Người thực hiện | Ca mới | Ca cũ | "
     "Tên bảng phân ca chi tiết | Ngày thực hiện chỉnh sửa.\n"
     "- Nhãn nằm ngay trong ô (không có chữ gợi ý kiểu \"Chọn...\", \"Tất cả\"); chọn giá trị thì nhãn dời lên viền trên của ô.\n"
     "- 2 ô Ngày làm việc và Ngày thực hiện chỉnh sửa là ô khoảng ngày, gồm 2 phần có chữ gợi ý \"Từ ngày\" -> \"Đến ngày\", mỗi phần có biểu tượng lịch.\n"
     "- Nguồn phân ca chọn được nhiều giá trị; các ô còn lại chọn 1 giá trị."),
]

# ------------------------------------------------------------------ III. DANH SACH & PHAN TRANG
SEC_III = [
    (1, "Sắp xếp mới nhất lên đầu", "P0", USER + "\nCó 22 dòng, nhiều thời điểm khác nhau.",
     "1. " + MENU + "\n2. So thời gian cột Người thực hiện từ trên xuống",
     "Không",
     "Thời gian giảm dần; các dòng sinh cùng 1 lần lưu (cùng phút) đứng liền nhau."),
    (2, "Đổi số dòng/trang", "P1", "Có 22 dòng.",
     "1. Mở ô \"Số dòng/trang\"\n2. Chọn 20",
     "Số dòng/trang: 20",
     "- Ô có lựa chọn 5, 10, 20, 50, 100.\n- Chọn 20: về trang 1, hiện 20 dòng, \"Hiển thị 1–20 / 22\"."),
    (3, "Chuyển trang - STT đánh tiếp", "P1", "Có 22 dòng, 10 dòng/trang.",
     "1. Bấm trang 3",
     "Không",
     "Hiện 2 dòng, STT 21 và 22, \"Hiển thị 21–22 / 22\"."),
    (4, "Đổi bộ lọc khi đang ở trang sau thì về trang 1", "P2", "Có 22 dòng, đang ở trang 2.",
     "1. Chọn Hành động = Thêm mới",
     "Hành động: Thêm mới",
     "Bảng về trang 1 của kết quả mới, không hiển thị trang trống."),
]

# ------------------------------------------------------------------ IV. GHI LICH SU - PHAN CA CHI TIET
SAVE_NEW = "1. " + MENU_DET + "\n2. Bấm \"Thêm mới\" (màn Thêm phân ca chi tiết)"
SEC_IV = [
    (1, "Tạo bảng chi tiết - nhân viên chưa có ca (không ghi đè)", "P0", PRE_BASE,
     SAVE_NEW + "\n3. Nhập Tên bảng phân ca, Ngày bắt đầu, Ngày kết thúc, tích Thứ 2 - Thứ 6 và chọn ca\n"
     "4. Bấm biểu tượng Thêm nhân viên, chọn A và B\n5. Bấm \"Lưu\"\n6. " + CHECK_LS,
     "Tên: PC Kinh doanh T11\nNgày bắt đầu 02/11/2026, kết thúc 27/11/2026\nThứ 2 - Thứ 6: HC_Ca hành chính\nNhân viên: A, B",
     E("Thêm mới", SRC_T11, DASH, "HC_Ca hành chính", NV_AB, "02/11/2026 - 27/11/2026", T2_T6, "Không",
       "Tạo phân ca chi tiết mới", "- Lúc lưu báo \"Thao tác thành công!\" và quay về danh sách bảng phân ca.\n- Chỉ sinh ĐÚNG 1 dòng.")),
    (2, "Tạo bảng chi tiết - nhân viên đã có ca (có ghi đè)", "P0",
     PRE_BASE + "\nA và B đã có ca KD_Ca kinh doanh từ Thứ 2 - Thứ 6, 02/11 - 27/11/2026 (bảng \"PC cũ\").",
     SAVE_NEW + "\n3. Nhập như TC_04.001, chọn A và B\n4. Bấm \"Lưu\" -> hiện popup \"Xác nhận tạo mới\" ghi \"2 nhân viên có ca trùng lặp, vui lòng xem chi tiết bên dưới:\" kèm bảng Ca cũ / Ca mới / Ngày trùng\n"
     "5. Bấm \"Xác nhận\"\n6. " + CHECK_LS,
     "Tên: PC Kinh doanh T11\n02/11 - 27/11/2026, Thứ 2 - Thứ 6: HC_Ca hành chính\nNhân viên: A, B",
     E("Thêm mới", SRC_T11, "KD_Ca kinh doanh", "HC_Ca hành chính", NV_AB, "02/11/2026 - 27/11/2026", T2_T6, "Có",
       "Tạo mới phân ca chi tiết có ghi đè ca làm việc của nhân viên",
       "- Trên Bảng phân ca tổng hợp, ô của A, B các ngày đó đổi sang Ca hành chính.")),
    (3, "Tạo bảng chi tiết - lẫn người có ca và chưa có ca: tách 2 dòng", "P0",
     PRE_BASE + "\nA đã có ca KD_Ca kinh doanh Thứ 2 - Thứ 6, 02/11 - 27/11/2026; B và C chưa có ca.",
     SAVE_NEW + "\n3. Nhập như TC_04.001, chọn A, B, C\n4. Bấm \"Lưu\" -> popup \"Xác nhận tạo mới\" (1 nhân viên trùng) -> \"Xác nhận\"\n5. " + CHECK_LS,
     "Tên: PC Kinh doanh T11\nThứ 2 - Thứ 6: HC_Ca hành chính\nNhân viên: A, B, C",
     "Sinh ĐÚNG 2 dòng cùng thời điểm, cùng Hành động \"Thêm mới\", Nguồn " + SRC_T11 + ":\n"
     "- Dòng 1: Ca cũ \"KD_Ca kinh doanh\", Ca mới \"HC_Ca hành chính\", Nhân viên chỉ " + NV_A + ", Có bị ghi đè \"Có\", "
     "Mô tả \"Tạo mới phân ca chi tiết có ghi đè ca làm việc của nhân viên\".\n"
     "- Dòng 2: Ca cũ " + DASH + ", Ca mới \"HC_Ca hành chính\", Nhân viên B và C, Có bị ghi đè \"Không\", "
     "Mô tả \"Tạo phân ca chi tiết mới\".\n"
     "- Cả 2 dòng: Thời gian 02/11/2026 - 27/11/2026, Thứ: " + T2_T6 + "."),
    (4, "Tạo bảng - mỗi thứ 1 ca khác nhau: mỗi ca 1 dòng", "P1", PRE_BASE,
     SAVE_NEW + "\n3. Thứ 2 - Thứ 6 chọn HC, Thứ 7 (lẻ) chọn TV, chọn A\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "02/11 - 27/11/2026\nThứ 2 - Thứ 6: HC_Ca hành chính\nThứ 7 (lẻ): TV_Ca tạp vụ\nNhân viên: A",
     "Sinh 2 dòng \"Thêm mới\", Mô tả \"Tạo phân ca chi tiết mới\":\n"
     "- Ca mới HC_Ca hành chính: Thời gian 02/11/2026 - 27/11/2026, Thứ: " + T2_T6 + ".\n"
     "- Ca mới TV_Ca tạp vụ: Thời gian 07/11/2026 - 21/11/2026, Thứ: \"Thứ 7 (lẻ)\"."),
    (5, "Tạo bảng trùng ca - bấm Huỷ ở popup xác nhận: không sinh dòng", "P0",
     PRE_BASE + "\nA đã có ca KD_Ca kinh doanh trong tháng 11/2026. Ghi nhận số dòng lịch sử hiện tại = N.",
     SAVE_NEW + "\n3. Nhập như TC_04.001, chọn A\n4. Bấm \"Lưu\" -> popup \"Xác nhận tạo mới\"\n5. Bấm \"Huỷ\"\n6. Mở màn Lịch sử phân ca",
     "Nhân viên: A",
     "- Bảng phân ca KHÔNG được tạo; ô của A vẫn là Ca kinh doanh.\n- Tổng số dòng lịch sử vẫn là N."),
    (6, "Tạo bảng thiếu trường bắt buộc: không sinh dòng", "P1", PRE_BASE + "\nSố dòng lịch sử hiện tại = N.",
     SAVE_NEW + "\n3. Để trống Tên bảng phân ca, chọn đủ các trường khác\n4. Bấm \"Lưu\"\n5. Mở màn Lịch sử phân ca",
     "Tên bảng phân ca: (trống)",
     "- Báo \"Vui lòng kiểm tra lại dữ liệu nhập\", ô Tên bảng phân ca có lỗi đỏ ngay dưới ô, không lưu.\n- Lịch sử vẫn N dòng."),
    (7, "Thêm nhân viên chưa có ca vào bảng đã có", "P0", PRE_T11 + "\nC chưa có ca tháng 11.",
     OPEN_T11 + "\n3. Bấm biểu tượng Thêm nhân viên, chọn Lê Văn C\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Thêm nhân viên: Lê Văn C",
     E("Thêm mới", SRC_T11, DASH, "HC_Ca hành chính", "chỉ \"Lê Văn C - KT - NV003\" (không có A, B)",
       "02/11/2026 - 27/11/2026", T2_T6, "Không", "Thêm nhân viên mới vào ca đã tồn tại")),
    (8, "Thêm nhân viên đang có ca ở bảng khác vào bảng đã có", "P1",
     PRE_T11 + "\nC đang có ca TV_Ca tạp vụ Thứ 2 - Thứ 6 tháng 11/2026 (bảng khác).",
     OPEN_T11 + "\n3. Thêm nhân viên Lê Văn C\n4. Bấm \"Lưu\" -> popup \"Xác nhận tạo mới\" -> \"Xác nhận\"\n5. " + CHECK_LS,
     "Thêm nhân viên: Lê Văn C",
     E("Thêm mới", SRC_T11, "TV_Ca tạp vụ", "HC_Ca hành chính", "\"Lê Văn C - KT - NV003\"",
       "02/11/2026 - 27/11/2026", T2_T6, "Có", "Thêm nhân viên mới vào ca đã tồn tại")),
    (9, "Xóa nhân viên khỏi bảng", "P0", PRE_T11,
     OPEN_T11 + "\n3. Ở Danh sách nhân viên, bấm biểu tượng thùng rác (Xóa) dòng Trần Thị B\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Xóa nhân viên: Trần Thị B",
     E("Xóa", SRC_T11, "HC_Ca hành chính", DASH, "\"Trần Thị B - KD1 - NV002\"",
       "02/11/2026 - 27/11/2026", T2_T6, DASH, "Xóa nhân viên khỏi bảng phân ca chi tiết",
       "- Trên Bảng phân ca tổng hợp, các ô của B trong tháng 11 trống.")),
    (10, "Sửa ca của 1 thứ (ghi đè ca đang có)", "P0", PRE_T11,
     OPEN_T11 + "\n3. Ô ca của Thứ 2 đổi từ HC sang KD\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Thứ 2: HC_Ca hành chính -> KD_Ca kinh doanh",
     E("Sửa", SRC_T11, "HC_Ca hành chính", "KD_Ca kinh doanh", NV_AB, "02/11/2026 - 23/11/2026", "Thứ 2", "Có",
       "Sửa phân ca chi tiết có ghi đè ca làm việc của nhân viên",
       "- Chỉ 1 dòng; Thời gian là Thứ 2 đầu tiên - Thứ 2 cuối cùng trong khoảng; các thứ khác không có dòng.")),
    (11, "Kéo dài ngày kết thúc", "P0", PRE_T11,
     OPEN_T11 + "\n3. Đổi Ngày kết thúc 27/11/2026 thành 04/12/2026\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Ngày kết thúc: 27/11/2026 -> 04/12/2026",
     E("Sửa", SRC_T11, DASH, "HC_Ca hành chính", NV_AB, "30/11/2026 - 04/12/2026", T2_T6, "Không",
       "Sửa phân ca chi tiết", "- Chỉ ghi các ngày được thêm; các ngày cũ (02/11 - 27/11) không sinh dòng.")),
    (12, "Rút ngắn ngày kết thúc - gỡ ca ghi là Xóa", "P0", PRE_T11,
     OPEN_T11 + "\n3. Đổi Ngày kết thúc 27/11/2026 thành 20/11/2026\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Ngày kết thúc: 27/11/2026 -> 20/11/2026",
     E("Xóa", SRC_T11, "HC_Ca hành chính", DASH, NV_AB, "23/11/2026 - 27/11/2026", T2_T6, DASH,
       "Gỡ ca khỏi ngày làm việc của nhân viên",
       "- KHÔNG ghi là \"Sửa ... có ghi đè\".\n- Bảng phân ca tổng hợp: ô của A, B từ 23/11 đến 27/11 trống.")),
    (13, "Lùi ngày bắt đầu sớm hơn", "P0", PRE_T11,
     OPEN_T11 + "\n3. Đổi Ngày bắt đầu 02/11/2026 thành 26/10/2026\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Ngày bắt đầu: 02/11/2026 -> 26/10/2026",
     E("Sửa", SRC_T11, DASH, "HC_Ca hành chính", NV_AB, "26/10/2026 - 30/10/2026", T2_T6, "Không",
       "Sửa phân ca chi tiết")),
    (14, "Dời ngày bắt đầu muộn hơn - các ngày bị bỏ được gỡ và ghi lịch sử", "P0", PRE_T11,
     OPEN_T11 + "\n3. Đổi Ngày bắt đầu 02/11/2026 thành 09/11/2026\n4. Bấm \"Lưu\"\n5. " + CHECK_LS +
     "\n6. Mở Bảng phân ca tổng hợp tháng 11/2026, xem ô của A, B từ 02/11 đến 06/11",
     "Ngày bắt đầu: 02/11/2026 -> 09/11/2026",
     E("Xóa", SRC_T11, "HC_Ca hành chính", DASH, NV_AB, "02/11/2026 - 06/11/2026", T2_T6, DASH,
       "Gỡ ca khỏi ngày làm việc của nhân viên",
       "- Bảng phân ca tổng hợp: các ô 02/11 - 06/11 của A, B đã TRỐNG (không còn Ca hành chính sót lại).")),
    (15, "Thêm 1 thứ áp dụng (Thứ 7 chẵn)", "P0", PRE_T11,
     OPEN_T11 + "\n3. Tích \"Thứ 7 (chẵn)\", chọn ca TV_Ca tạp vụ\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Thứ 7 (chẵn): TV_Ca tạp vụ",
     E("Sửa", SRC_T11, DASH, "TV_Ca tạp vụ", NV_AB, "\"14/11/2026\" (1 ngày, không lặp 2 lần)",
       "Thứ 7 (chẵn)", "Không", "Sửa phân ca chi tiết",
       "- Ngày 27/11 là Thứ 6 nên Thứ 7 (chẵn) trong khoảng chỉ có 14/11 (28/11 nằm ngoài khoảng).")),
    (16, "Bỏ 1 thứ áp dụng (Thứ 7 lẻ) - gỡ ca ghi là Xóa", "P0",
     PRE_T11 + "\nBảng đang tích thêm Thứ 7 (lẻ) ca TV_Ca tạp vụ (07/11, 21/11).",
     OPEN_T11 + "\n3. Bỏ tích \"Thứ 7 (lẻ)\"\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Bỏ Thứ 7 (lẻ)",
     E("Xóa", SRC_T11, "TV_Ca tạp vụ", DASH, NV_AB, "07/11/2026 - 21/11/2026", "Thứ 7 (lẻ)", DASH,
       "Gỡ ca khỏi ngày làm việc của nhân viên")),
    (17, "Chỉ đổi tên bảng - không sinh dòng riêng; dòng sau hiện tên mới", "P0",
     PRE_T11 + "\nSố dòng lịch sử hiện tại = N.",
     OPEN_T11 + "\n3. Đổi Tên bảng phân ca, bấm \"Lưu\"\n4. Mở màn Lịch sử phân ca, đếm số dòng\n"
     "5. Mở lại bảng, đổi ca Thứ 3 sang KD, bấm \"Lưu\"\n6. Xem dòng đầu màn Lịch sử phân ca",
     "Tên mới: PC Kinh doanh T11 - sửa",
     "- Sau bước 3: vẫn N dòng (đổi tên không sinh dòng).\n"
     "- Sau bước 5: dòng mới có Nguồn \"Phân ca chi tiết_PC Kinh doanh T11 - sửa\"; các dòng cũ vẫn mang tên cũ \"PC Kinh doanh T11\"."),
    (18, "Lưu mà không thay đổi gì - không sinh dòng", "P0", PRE_T11 + "\nSố dòng lịch sử hiện tại = N.",
     OPEN_T11 + "\n3. Không sửa gì, bấm \"Lưu\"\n4. Mở màn Lịch sử phân ca",
     "Không",
     "- Báo \"Thao tác thành công!\".\n- Lịch sử vẫn N dòng."),
    (19, "1 lần lưu nhiều thay đổi - sinh nhiều dòng cùng thời điểm", "P1", PRE_T11 + "\nC chưa có ca tháng 11.",
     OPEN_T11 + "\n3. Đổi ca Thứ 2 sang KD, thêm nhân viên C, xóa nhân viên B\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Thứ 2 -> KD; thêm C; xóa B",
     "Các dòng cùng thời điểm, mỗi nhóm 1 dòng, ví dụ:\n"
     "- Sửa: HC -> KD, Nhân viên A, Thứ 2, Có, \"Sửa phân ca chi tiết có ghi đè ca làm việc của nhân viên\".\n"
     "- Thêm mới: ca cũ trống -> KD, Nhân viên C, Thứ 2, Không, \"Thêm nhân viên mới vào ca đã tồn tại\".\n"
     "- Thêm mới: ca cũ trống -> HC, Nhân viên C, Thứ 3 - Thứ 6, Không, \"Thêm nhân viên mới vào ca đã tồn tại\".\n"
     "- Xóa: HC -> trống, Nhân viên B, Thứ 2 - Thứ 6, gạch ngang, \"Xóa nhân viên khỏi bảng phân ca chi tiết\".\n"
     "- Không có dòng thừa cho A ở Thứ 3 - Thứ 6 (không đổi ca)."),
    (20, "Sửa bảng làm trùng ca bảng khác - bấm Huỷ: không sinh dòng", "P1",
     PRE_T11 + "\nC có ca TV Thứ 2 - Thứ 6 tháng 11 ở bảng khác. Số dòng lịch sử = N.",
     OPEN_T11 + "\n3. Thêm nhân viên C, bấm \"Lưu\" -> popup \"Xác nhận tạo mới\"\n4. Bấm \"Huỷ\"\n5. Mở màn Lịch sử phân ca",
     "Thêm nhân viên C",
     "- Không lưu; ô của C vẫn Ca tạp vụ.\n- Lịch sử vẫn N dòng."),
    (21, "Xóa bảng phân ca chi tiết - xác nhận", "P0",
     PRE_BASE + "\nHôm nay 28/09/2026. Bảng \"PC Tháng 9-10\": 21/09/2026 - 16/10/2026, Thứ 2 - Thứ 6 ca HC, nhân viên A, B.",
     "1. " + MENU_DET + "\n2. Ở dòng \"PC Tháng 9-10\" bấm nút bánh răng -> \"Xóa\"\n"
     "3. Popup \"Xác nhận xóa\": đọc nội dung, bấm \"Xóa\" (nút đỏ)\n4. " + CHECK_LS,
     "Bảng: PC Tháng 9-10",
     "- Popup tiêu đề \"Xác nhận xóa\", có 2 nút \"Xóa\" (màu đỏ) và \"Hủy\"; nội dung: Bạn có chắc muốn xóa bảng phân ca \"PC Tháng 9-10\"? Ca của nhân viên từ ngày mai trở đi theo bảng này sẽ bị gỡ.\n"
     "- Báo \"Xoá phân ca làm việc thành công\", bảng biến khỏi danh sách.\n" +
     E("Xóa", "\"Phân ca chi tiết_PC Tháng 9-10\"", "HC_Ca hành chính", DASH, NV_AB,
       "29/09/2026 - 16/10/2026 (bắt đầu từ NGÀY MAI)", T2_T6, DASH, "Xóa bảng phân ca chi tiết",
       "- Ca của A, B ngày 28/09 (hôm nay) và trước đó vẫn còn trên Bảng phân ca tổng hợp.")),
    (22, "Xóa bảng - bấm Huỷ ở popup xác nhận: không sinh dòng", "P1",
     "Như TC trên. Số dòng lịch sử = N.",
     "1. " + MENU_DET + "\n2. Dòng \"PC Tháng 9-10\" -> \"Xóa\"\n3. Bấm \"Hủy\" (hoặc dấu × đóng) ở popup \"Xác nhận xóa\"\n4. Mở màn Lịch sử phân ca",
     "Không",
     "- Bảng vẫn còn.\n- Lịch sử vẫn N dòng."),
    (23, "Xóa bảng đã hết hạn (không còn ngày từ mai trở đi)", "P2",
     "Bảng \"PC Tháng 8\": 03/08/2026 - 28/08/2026. Số dòng lịch sử = N.",
     "1. " + MENU_DET + "\n2. Dòng \"PC Tháng 8\" -> \"Xóa\" -> \"Xóa\"\n3. Mở màn Lịch sử phân ca",
     "Bảng: PC Tháng 8",
     "- Bảng bị xóa khỏi danh sách; ca tháng 8 của nhân viên giữ nguyên.\n"
     "- KHÔNG sinh dòng lịch sử (không có ngày nào bị gỡ); vẫn N dòng."),
]

# ------------------------------------------------------------------ V. GHI LICH SU - BANG TONG HOP
PRE_G = PRE_BASE + "\nBảng phân ca tổng hợp lọc tháng 11/2026. Ngày 03/11/2026 là Thứ 3."
SEC_V = [
    (1, "Gán ca vào ô trống", "P0", PRE_G,
     "1. " + MENU_GEN + "\n2. Ở dòng Nguyễn Văn A, ô 03/11 bấm biểu tượng \"Thêm phân ca\"\n"
     "3. Popup \"Ca làm việc\": bấm dòng HC_Ca hành chính\n4. Popup \"Phân ca cho Nguyễn Văn A - ...\": bấm \"Đồng ý\"\n5. " + CHECK_LS,
     "Nhân viên A, ngày 03/11/2026, ca HC",
     E("Thêm mới", SRC_GEN, DASH, "HC_Ca hành chính", NV_A, "03/11/2026", "Thứ 3", "Không",
       "Phân ca trên bảng phân ca tổng hợp", "- Lúc bấm Đồng ý báo \"Tạo thành công\", ô 03/11 của A hiện Ca hành chính.")),
    (2, "Đổi ca ô đã có (màn đang mở cũ) - không tạo 2 ca, ghi Sửa", "P0",
     PRE_G + "\nMở Bảng phân ca tổng hợp ở 2 tab. Tab 1: ô 03/11 của A đang trống.",
     "1. Ở tab 2 gán ca HC cho A ngày 03/11\n2. Quay lại tab 1 (chưa tải lại), bấm \"Thêm phân ca\" ở ô 03/11 của A, chọn KD, \"Đồng ý\"\n"
     "3. Tải lại Bảng phân ca tổng hợp\n4. " + CHECK_LS,
     "Tab 2: HC; Tab 1: KD",
     "- Ô 03/11 của A chỉ có 1 ca \"Ca kinh doanh\" (không hiện 2 ca chồng nhau).\n" +
     E("Sửa", SRC_GEN, "HC_Ca hành chính", "KD_Ca kinh doanh", NV_A, "03/11/2026", "Thứ 3", "Có",
       "Sửa ca trên bảng phân ca tổng hợp")),
    (3, "Chọn lại đúng ca đang có - không sinh dòng", "P1",
     PRE_G + "\nA đã có HC ngày 03/11 (tab cũ vẫn thấy ô trống). Số dòng lịch sử = N.",
     "1. Ở tab cũ bấm \"Thêm phân ca\" ô 03/11 của A, chọn đúng HC, \"Đồng ý\"\n2. Mở màn Lịch sử phân ca",
     "Ca: HC (trùng ca đang có)",
     "- Ô vẫn 1 ca Ca hành chính.\n- Lịch sử vẫn N dòng."),
    (4, "Xóa ca 1 ô", "P0", PRE_G + "\nA có ca HC ngày 03/11/2026.",
     "1. " + MENU_GEN + "\n2. Ô 03/11 của A bấm dấu X\n3. Popup \"Xác nhận xoá phân ca\" (hỏi \"Bạn có muốn xoá phân ca ... của Nguyễn Văn A - NV001 vào Thứ 3 ngày 03/11/2026 không?\") bấm \"Đồng ý\"\n4. " + CHECK_LS,
     "Nhân viên A, 03/11/2026",
     E("Xóa", SRC_GEN, "HC_Ca hành chính", DASH, NV_A, "03/11/2026", "Thứ 3", DASH,
       "Xóa ca trên bảng phân ca tổng hợp", "- Lúc bấm Đồng ý báo \"Xóa thành công\", ô 03/11 của A trống.")),
    (5, "Xóa ca - bấm Không: không sinh dòng", "P1", PRE_G + "\nA có ca HC ngày 03/11. Số dòng = N.",
     "1. " + MENU_GEN + "\n2. Ô 03/11 của A bấm X\n3. Bấm \"Không\"\n4. Mở màn Lịch sử phân ca",
     "Không",
     "- Ô vẫn Ca hành chính.\n- Lịch sử vẫn N dòng."),
    (6, "Phân ca theo ngày - nhiều nhân viên, 2 ca: mỗi ca 1 dòng", "P0", PRE_G,
     "1. " + MENU_GEN + "\n2. Bấm \"Phân ca theo ngày\"\n3. Chọn ngày đăng ký 03/11/2026\n"
     "4. \"Chọn ca đăng ký\": HC và KD\n5. Ca HC chọn nhân sự A, B; ca KD chọn C\n6. Bấm \"Lưu\"\n7. " + CHECK_LS,
     "03/11/2026\nHC: A, B\nKD: C",
     "- Báo \"Cập nhật thành công\".\nSinh 2 dòng cùng thời điểm, Nguồn " + SRC_GEN + ", Hành động \"Thêm mới\", Ca cũ gạch ngang, "
     "Thời gian 03/11/2026, Thứ 3, Có bị ghi đè \"Không\", Mô tả \"Phân ca trên bảng phân ca tổng hợp\":\n"
     "- Ca mới HC_Ca hành chính: Nhân viên A, B.\n- Ca mới KD_Ca kinh doanh: Nhân viên C."),
    (7, "Phân ca theo ngày - chuyển nhân viên sang ca khác", "P0",
     PRE_G + "\nNgày 03/11: A, B ca HC.",
     "1. " + MENU_GEN + "\n2. \"Phân ca theo ngày\", chọn 03/11/2026 (tự hiện ca HC có A, B)\n"
     "3. Bỏ A khỏi ca HC, thêm ca KD và chọn A\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "A: HC -> KD",
     E("Sửa", SRC_GEN, "HC_Ca hành chính", "KD_Ca kinh doanh", NV_A, "03/11/2026", "Thứ 3", "Có",
       "Sửa ca trên bảng phân ca tổng hợp", "- Không có dòng nào cho B (không đổi ca).")),
    (8, "Phân ca theo ngày - bỏ nhân viên khỏi ca", "P0", PRE_G + "\nNgày 03/11: A, B ca HC.",
     "1. " + MENU_GEN + "\n2. \"Phân ca theo ngày\", chọn 03/11/2026\n3. Bỏ B khỏi ca HC\n4. Bấm \"Lưu\"\n5. " + CHECK_LS,
     "Bỏ B khỏi ca HC",
     E("Xóa", SRC_GEN, "HC_Ca hành chính", DASH, "\"Trần Thị B - KD1 - NV002\"", "03/11/2026", "Thứ 3", DASH,
       "Xóa ca trên bảng phân ca tổng hợp")),
    (9, "Phân ca theo ngày từ 20 nhân viên trở lên", "P1", PRE_G + "\nPhòng KD1 có 25 nhân viên chưa có ca ngày 04/11.",
     "1. " + MENU_GEN + "\n2. \"Phân ca theo ngày\", chọn 04/11/2026, ca HC, chọn 25 nhân viên KD1\n3. \"Lưu\"\n4. " + CHECK_LS,
     "25 nhân viên, ca HC",
     "- 1 dòng Thêm mới, cột Nhân viên hiện \"25 nhân viên\" + nút tải Excel.\n- Mô tả \"Phân ca trên bảng phân ca tổng hợp\"."),
    (10, "Ngày đã qua không thao tác được", "P2", PRE_G + "\nHôm nay 28/09/2026, xem tháng 09/2026.",
     "1. " + MENU_GEN + "\n2. Xem ô ngày 25/09/2026 (có ca và trống)",
     "Không",
     "- Ô ngày đã qua không có biểu tượng \"Thêm phân ca\" và không có dấu X.\n- Không thể sinh lịch sử cho ngày đã qua từ bảng tổng hợp."),
]

# ------------------------------------------------------------------ VI. EXCEL
PRE_X = USER + "\nCó dòng Thêm mới 25 nhân viên (ca cũ KD, ca mới HC, 02/11 - 27/11/2026, Thứ 2 - Thứ 6, có ghi đè), " \
    "trong đó nhân viên Hoàng E có Mã chấm công \"0123\" và Mã NV \"0012345\"."
SEC_VI = [
    (1, "Tải Excel danh sách nhân viên - phần đầu file", "P0", PRE_X,
     "1. " + MENU + "\n2. Ở dòng \"25 nhân viên\" bấm nút tải\n3. Mở file",
     "Không",
     "- Tải về file tên dạng danh_sach_nhan_vien_phan_ca_<số>.xlsx.\n"
     "- Dòng 1: \"DANH SÁCH NHÂN VIÊN\".\n"
     "- Dòng 2 đến dòng 6 lần lượt: \"Ca cũ: KD_Ca kinh doanh\", \"Ca mới: HC_Ca hành chính\", \"Thời gian làm việc: 02/11/2026 - 27/11/2026\", "
     "\"Các thứ áp dụng: " + T2_T6 + "\", \"Có ghi đè ca không: Có\"."),
    (2, "Excel - bảng nhân viên", "P0", PRE_X,
     "1. Tải file như TC trên\n2. Xem bảng nhân viên",
     "Không",
     "- Dòng 7 là tiêu đề cột: STT | Mã chấm công | Mã nhân viên | Tên nhân viên | Phòng ban.\n"
     "- Đủ 25 dòng, STT 1 đến 25, khớp số \"25 nhân viên\" trên màn.\n- Phòng ban dạng \"Mã_Tên\", ví dụ \"KD1_Phòng kinh doanh 1\".\n"
     "- Cột Tên nhân viên và Phòng ban đủ rộng, mở file ra đọc được trọn chữ, không bị cột bên cạnh che."),
    (3, "Excel - mã có số 0 ở đầu giữ nguyên", "P0", PRE_X,
     "1. Tải file\n2. Xem dòng Hoàng E",
     "Mã chấm công 0123, Mã NV 0012345",
     "Ô Mã chấm công là \"0123\", Mã nhân viên là \"0012345\" (không bị mất số 0 thành 123 / 12345)."),
    (4, "Excel - dòng Xóa: ca mới và ghi đè", "P1",
     "Có dòng Xóa bảng phân ca chi tiết gồm 30 nhân viên, ca cũ HC.",
     "1. Tải file của dòng đó",
     "Không",
     "- \"Ca cũ: HC_Ca hành chính\".\n- \"Ca mới: (không có)\".\n- \"Có ghi đè ca không: —\"."),
    (5, "Excel - nhân viên không có phòng ban", "P2",
     "Trong dòng 25 nhân viên có 1 người chưa gắn phòng ban.",
     "1. Tải file\n2. Xem cột Phòng ban của người đó",
     "Không",
     "Hiển thị \"—\"."),
    (6, "Excel theo thông tin lúc phân ca", "P1",
     PRE_X + "\nSau khi phân ca, Hoàng E chuyển sang phòng KT và nghỉ việc.",
     "1. Tải file\n2. Xem dòng Hoàng E",
     "Không",
     "Phòng ban vẫn là phòng lúc phân ca (KD1), Hoàng E vẫn có trong danh sách."),
]

# ------------------------------------------------------------------ VII. POPUP THEO NHAN VIEN
PRE_P = USER + "\n" + NV_DATA + "\nNguyễn Văn A có 25 dòng lịch sử (bảng \"PC Kinh doanh T11\" và bảng tổng hợp, ca HC/KD/TV), " \
    "Trần Thị B có 3 dòng. Bảng phân ca tổng hợp đang xem tháng 11/2026."
OPEN_P = "1. " + MENU_GEN + "\n2. Bấm biểu tượng lịch sử ngay cạnh tên \"Nguyễn Văn A\""
OPEN_P_ADV = OPEN_P + "\n3. Bấm \"Tìm kiếm nâng cao\" để mở bộ lọc"
SEC_VII = [
    (1, "Icon lịch sử cạnh tên từng nhân viên", "P0", PRE_P,
     "1. " + MENU_GEN + "\n2. Di chuột vào biểu tượng lịch sử cạnh tên nhân viên",
     "Không",
     "- Mỗi dòng nhân viên có 1 biểu tượng lịch sử ngay sau tên.\n- Di chuột hiện \"Lịch sử phân ca của nhân viên\"."),
    (2, "Mở popup - tiêu đề, nút Đóng, bộ lọc thu gọn sẵn", "P0", PRE_P,
     OPEN_P,
     "Không",
     "- Popup tiêu đề \"Lịch sử chỉnh sửa - Nguyễn Văn A\".\n- Khối \"Bộ lọc lịch sử phân ca\" có nút \"Cài đặt bộ lọc\", \"Tìm kiếm nâng cao\"; ô tìm nhanh cùng nút \"Tìm kiếm\", \"Làm mới\" luôn hiện; 7 ô lọc nâng cao đang THU GỌN.\n"
     "- Chân popup có nút \"Đóng\"."),
    (3, "Bảng 9 cột - không có Nhân viên và Mô tả sự kiện", "P0", PRE_P, OPEN_P + "\n3. Đọc tiêu đề bảng",
     "Không",
     "Đúng thứ tự: STT | Người thực hiện | Hành động | Nguồn phân ca | Ca làm việc cũ | Ca làm việc mới | "
     "Thời gian làm việc (theo ca mới) | Các thứ áp dụng (theo ca mới) | Có bị ghi đè ca không.\nKHÔNG có cột Nhân viên, Mô tả sự kiện."),
    (4, "Chỉ hiện dòng có nhân viên đó, khớp màn chính", "P0", PRE_P,
     OPEN_P + "\n3. Ghi số tổng ở dưới bảng popup\n4. Mở màn Lịch sử phân ca, lọc Nhân viên = Nguyễn Văn A, so sánh",
     "Không",
     "- Popup tổng 25 dòng, không có dòng chỉ gồm B hoặc C.\n- Màn chính lọc theo A cũng 25 dòng, cùng nội dung từng dòng."),
    (5, "Định dạng các cột giống màn chính", "P1", PRE_P, OPEN_P + "\n3. So 1 dòng với dòng tương ứng ở màn chính",
     "Không",
     "Người thực hiện, Hành động (nhãn màu), Nguồn, Ca cũ/mới (mã ca_tên ca), Thời gian, Thứ, Có bị ghi đè hiển thị giống hệt màn chính; "
     "ô dài quá 2 dòng thì cắt và di chuột xem đủ."),
    (6, "Tìm nhanh theo tên bảng phân ca", "P0", PRE_P,
     OPEN_P + "\n3. Gõ vào ô tìm nhanh, nhấn Enter",
     "Từ khóa: Kinh doanh T11",
     "- Placeholder ô: \"Tìm theo tên bảng phân ca, mã/tên ca cũ, mã/tên ca mới\".\n- Chỉ còn các dòng nguồn \"Phân ca chi tiết_PC Kinh doanh T11\" của A."),
    (7, "Tìm nhanh theo mã / tên ca cũ", "P0", PRE_P,
     OPEN_P + "\n3. Gõ \"KD\", Enter\n4. Gõ \"tạp vụ\", Enter",
     "KD; tạp vụ",
     "- \"KD\": hiện dòng có ca cũ hoặc ca mới mã KD.\n- \"tạp vụ\": hiện dòng có ca cũ hoặc ca mới tên Ca tạp vụ (không phân biệt hoa thường)."),
    (8, "Tìm nhanh theo mã / tên ca mới", "P1", PRE_P,
     OPEN_P + "\n3. Gõ \"hành chính\", bấm \"Tìm kiếm\"",
     "hành chính",
     "Hiện các dòng có Ca làm việc mới hoặc cũ là HC_Ca hành chính; vẫn chỉ của A."),
    (9, "Tìm nhanh chỉ chạy khi Enter / Tìm kiếm; xóa từ khóa thì tải lại", "P1", PRE_P,
     OPEN_P + "\n3. Gõ \"TV\" nhưng chưa Enter\n4. Nhấn Enter\n5. Bấm dấu × xóa từ khóa",
     "TV",
     "- Bước 3: bảng chưa đổi.\n- Bước 4: lọc theo TV.\n- Bước 5: bảng trở lại đủ 25 dòng."),
    (10, "Tìm kiếm nâng cao có đủ 7 ô lọc", "P0", PRE_P, OPEN_P_ADV,
     "Không",
     "- Nút đổi chữ thành \"Ẩn tìm kiếm nâng cao\".\n"
     "- Có đúng 7 ô theo thứ tự: Hành động | Nguồn phân ca | Ngày làm việc | Người thực hiện | Ca mới | Ca cũ | Ngày chỉnh sửa.\n"
     "- Nhãn nằm trong ô, không có chữ gợi ý riêng; 2 ô Ngày làm việc và Ngày chỉnh sửa gồm \"Từ ngày\" -> \"Đến ngày\".\n"
     "- Không có ô Công ty, Phòng ban, Nhân viên, Tên bảng phân ca chi tiết."),
    (11, "Popup - lọc Hành động", "P0", PRE_P, OPEN_P_ADV + "\n4. Chọn Hành động = Xóa",
     "Hành động: Xóa",
     "Tìm ngay; chỉ còn dòng \"Xóa\" của A."),
    (12, "Popup - lọc Nguồn phân ca (chọn nhiều)", "P1", PRE_P, OPEN_P_ADV + "\n4. Nguồn phân ca chọn \"Phân ca tổng hợp\"\n5. Chọn thêm \"Phân ca chi tiết\"",
     "Nguồn: Phân ca tổng hợp; rồi cả 2",
     "- Chỉ còn dòng \"Phân ca tổng hợp\".\n- Chọn cả 2: đủ 25 dòng."),
    (13, "Popup - lọc Ngày làm việc (bao trùm)", "P0",
     PRE_P + "\nA có dòng 02/11 - 27/11/2026 và dòng 03/11/2026.",
     OPEN_P_ADV + "\n4. Ngày làm việc Từ 01/11/2026 Đến 10/11/2026",
     "01/11/2026 - 10/11/2026",
     "Chỉ hiện dòng 03/11/2026; không hiện dòng 02/11 - 27/11 (không nằm trọn trong khoảng)."),
    (14, "Popup - lọc Người thực hiện: chỉ người đã thao tác", "P1",
     PRE_P + "\nChỉ U1 (Ngô Thị Lý) và U6 (Phạm Doãn Chiến) từng thao tác phân ca.",
     OPEN_P_ADV + "\n4. Mở ô Người thực hiện, chọn Phạm Doãn Chiến",
     "Người thực hiện: Phạm Doãn Chiến",
     "- Danh sách chỉ gồm người đã từng thao tác phân ca, dạng \"Tên - Mã phòng - Mã NV\".\n- Chỉ còn dòng của A do Phạm Doãn Chiến thực hiện."),
    (15, "Popup - lọc Ca mới", "P1", PRE_P, OPEN_P_ADV + "\n4. Ca mới = KD_Ca kinh doanh",
     "Ca mới: KD_Ca kinh doanh",
     "Chỉ còn dòng của A có Ca làm việc mới KD_Ca kinh doanh."),
    (16, "Popup - lọc Ca cũ", "P1", PRE_P, OPEN_P_ADV + "\n4. Ca cũ = HC_Ca hành chính",
     "Ca cũ: HC_Ca hành chính",
     "Chỉ còn dòng của A có Ca làm việc cũ HC_Ca hành chính."),
    (17, "Popup - lọc Ngày chỉnh sửa", "P1", PRE_P + "\nA có dòng thao tác ngày 20/07 và 27/07/2026.",
     OPEN_P_ADV + "\n4. Ngày chỉnh sửa Từ 27/07/2026 Đến 27/07/2026",
     "27/07/2026 - 27/07/2026",
     "Chỉ hiện dòng thao tác trong ngày 27/07/2026."),
    (18, "Popup - Làm mới", "P1", PRE_P,
     OPEN_P_ADV + "\n4. Nhập từ khóa và chọn 3 ô lọc\n5. Bấm \"Làm mới\"\n6. Chỉ gõ từ khóa \"KD\" vào ô tìm nhanh, nhấn Enter\n7. Bấm \"Làm mới\"",
     "Không",
     "- Bước 5: mọi ô (kể cả ô tìm nhanh) về trống, bảng về trang 1 với đủ 25 dòng của A.\n"
     "- Bước 7: ô tìm nhanh về trống VÀ bảng tải lại đủ 25 dòng (không giữ kết quả lọc theo KD)."),
    (19, "Popup - phân trang 20/50/100", "P0", PRE_P,
     OPEN_P + "\n3. Xem phân trang\n4. Sang trang 2\n5. Đổi số dòng/trang 50",
     "Không",
     "- Mặc định 20 dòng/trang, lựa chọn 20, 50, 100.\n- Trang 2: 5 dòng, STT 21-25.\n- Chọn 50: về trang 1, đủ 25 dòng.\n"
     "- Chỉ khung bảng cuộn, tiêu đề bảng đứng yên khi cuộn."),
    (20, "Popup - không có dòng", "P1", PRE_P + "\nLê Văn C chưa từng được phân ca.",
     "1. " + MENU_GEN + "\n2. Bấm biểu tượng lịch sử cạnh \"Lê Văn C\"",
     "Không",
     "Bảng hiện \"Nhân viên chưa có lịch sử phân ca phù hợp bộ lọc.\" (chữ xám)."),
    (21, "Đóng rồi mở popup nhân viên khác - bộ lọc được xóa", "P0", PRE_P,
     OPEN_P_ADV + "\n4. Chọn Hành động = Xóa, nhập từ khóa \"KD\"\n5. Bấm \"Đóng\"\n6. Bấm biểu tượng lịch sử cạnh \"Trần Thị B\"",
     "Không",
     "- Tiêu đề đổi thành \"Lịch sử chỉnh sửa - Trần Thị B\".\n- Ô tìm nhanh và các ô lọc trống (khối Tìm kiếm nâng cao giữ trạng thái mở/thu gọn như lúc đóng).\n- Hiện đủ 3 dòng của B, không còn dòng của A."),
    (22, "Popup cập nhật ngay sau khi phân ca", "P1", PRE_P,
     "1. " + MENU_GEN + "\n2. Gán ca KD cho A ngày 05/11/2026 (Thêm phân ca -> chọn ca -> Đồng ý)\n3. Bấm biểu tượng lịch sử cạnh A",
     "A, 05/11/2026, ca KD",
     "Dòng đầu popup: Hành động Thêm mới, Nguồn \"Phân ca tổng hợp\", Ca mới \"KD_Ca kinh doanh\", 05/11/2026, Thứ 5, Không."),
]

# ------------------------------------------------------------------ VIII. LOI DA SUA
SEC_VIII = [
    (1, "[Đã sửa] Menu Lịch sử phân ca hiển thị lại", "P0",
     "Tài khoản có 1 trong 3 quyền phân ca. Trước đây mục menu bị ẩn.",
     "1. Vào phân hệ Chấm công -> menu \"Ca làm việc\"",
     "Không",
     "Có mục \"Lịch sử phân ca\" ngay sau \"Bảng phân ca chi tiết\"; bấm vào mở đúng màn Lịch sử phân ca."),
    (2, "[Đã sửa] Có cột Mô tả sự kiện", "P0", USER,
     "1. " + MENU,
     "Không",
     "Bảng có cột cuối \"Mô tả sự kiện\" và mọi dòng mới đều có nội dung (không trống)."),
    (3, "[Đã sửa] Dời ngày bắt đầu muộn hơn gỡ ca cũ + ghi lịch sử", "P0", PRE_T11,
     OPEN_T11 + "\n3. Ngày bắt đầu 02/11 -> 09/11/2026, \"Lưu\"\n4. Xem Bảng phân ca tổng hợp và màn Lịch sử phân ca",
     "Ngày bắt đầu: 09/11/2026",
     "- Trước đây: ô 02/11 - 06/11 vẫn còn ca, không có lịch sử.\n- Nay: các ô đó trống, có dòng Xóa \"Gỡ ca khỏi ngày làm việc của nhân viên\" 02/11/2026 - 06/11/2026."),
    (4, "[Đã sửa] Gán ca vào ô đã có ca không tạo 2 ca", "P0", PRE_G,
     "Làm như TC_05.002 (2 tab, tab cũ gán ca khác vào ô đã có ca)",
     "HC rồi KD",
     "- Trước đây: ô có 2 ca chồng nhau, lịch sử ghi Thêm mới.\n- Nay: ô chỉ 1 ca KD, lịch sử ghi \"Sửa\", ghi đè \"Có\", \"Sửa ca trên bảng phân ca tổng hợp\"."),
    (5, "[Đã sửa] Gỡ ca ghi là Xóa, không phải Sửa có ghi đè", "P0", PRE_T11,
     OPEN_T11 + "\n3. Ngày kết thúc 27/11 -> 20/11/2026, \"Lưu\"\n4. " + CHECK_LS,
     "Ngày kết thúc: 20/11/2026",
     "- Trước đây: Sửa, ca mới trống, ghi đè Có.\n- Nay: Hành động \"Xóa\", Ca mới và Có bị ghi đè là gạch ngang, Mô tả \"Gỡ ca khỏi ngày làm việc của nhân viên\"."),
    (6, "[Đã sửa] Nút Xóa bảng phân ca chi tiết bật lại", "P0",
     USER + "\nCó bảng \"PC Tạm\".",
     "1. " + MENU_DET + "\n2. Bấm nút bánh răng ở dòng \"PC Tạm\"",
     "Không",
     "- Menu thao tác có \"Sửa\" và \"Xóa\".\n- Bấm Xóa hiện popup \"Xác nhận xóa\" (nút Xóa màu đỏ); xác nhận thì xóa được và sinh lịch sử \"Xóa bảng phân ca chi tiết\"."),
    (7, "[Đã sửa] Người thực hiện có mã phòng ban", "P1", USER,
     "1. Phân ca 1 ô bất kỳ\n2. " + CHECK_LS,
     "Không",
     "Cột Người thực hiện dạng \"NSHC - Ngô Thị Lý - dd/mm/yyyy hh:mm\"\n(trước đây thiếu mã phòng)."),
    (8, "[Đã sửa] Excel giữ số 0 đầu của mã", "P1", PRE_X,
     "Làm như TC_06.003",
     "Mã 0123 / 0012345",
     "Mã chấm công và Mã nhân viên giữ nguyên số 0 đầu."),
    (9, "[Đã sửa] Mở ô lọc khi danh sách chưa tải xong không bị đóng mất", "P2", USER,
     "1. " + MENU + "\n2. Ngay khi màn vừa hiện, bấm mở ô \"Ca mới\"",
     "Không",
     "Ô vẫn mở; khi danh sách tải xong hiện ngay các ca, không bị đóng lại / không kẹt \"Không có dữ liệu\"."),
    (10, "[Đã sửa] Nhãn \"Ngày thực hiện chỉnh sửa\" không bị biểu tượng lịch đè", "P2", USER,
     "1. " + MENU + "\n2. Nhìn ô Ngày thực hiện chỉnh sửa khi chưa chọn ngày",
     "Không",
     "Nhãn nằm gọn phía trái, phần dư hiện \"…\", không bị biểu tượng lịch che; di chuột xem đủ nhãn."),
    (11, "[Đã sửa] Màn có dòng tiêu đề, bộ lọc không dính sát thanh menu", "P2", USER,
     "1. " + MENU,
     "Không",
     "Có dòng tiêu đề \"Lịch sử phân ca\" giữa thanh menu và khối bộ lọc."),
    (12, "[Đã sửa] Popup lịch sử theo nhân viên - Làm mới sau khi chỉ tìm nhanh", "P1", PRE_P,
     OPEN_P + "\n3. Gõ \"Kinh doanh T11\" vào ô tìm nhanh, nhấn Enter (bảng còn ít dòng)\n4. Bấm \"Làm mới\"",
     "Từ khóa: Kinh doanh T11",
     "- Trước đây: ô tìm nhanh về trống nhưng bảng vẫn giữ kết quả lọc cũ.\n- Nay: ô tìm nhanh về trống và bảng tải lại đủ 25 dòng của A."),
    (13, "[Đã sửa] File Excel danh sách nhân viên đủ rộng để đọc", "P2", PRE_X,
     "1. " + MENU + "\n2. Ở dòng \"25 nhân viên\" bấm nút tải\n3. Mở file, xem cột Tên nhân viên và Phòng ban",
     "Không",
     "- Trước đây: mọi cột cùng bề rộng mặc định, tên nhân viên bị cột Phòng ban che mất phần sau.\n"
     "- Nay: cột Tên nhân viên và Phòng ban rộng hơn, đọc được trọn chữ mà không phải kéo cột."),
]

# ------------------------------------------------------------------ IX. E2E
SEC_IX = [
    (1, "Luồng đầy đủ 1 bảng phân ca từ tạo đến xóa", "P0", PRE_BASE + "\nSố dòng lịch sử hiện tại = N.",
     "1. Tạo bảng \"PC E2E\" 02/11 - 27/11/2026, Thứ 2 - Thứ 6 ca HC, nhân viên A, B\n"
     "2. Sửa: Thứ 2 sang KD\n3. Sửa: rút ngày kết thúc về 20/11/2026\n4. Sửa: xóa nhân viên B\n"
     "5. Bảng tổng hợp: đổi ca A ngày 03/11 sang TV (Phân ca theo ngày)\n6. Xóa bảng \"PC E2E\"\n7. Mở màn Lịch sử phân ca, lọc Tên bảng = PC E2E; mở popup lịch sử của A",
     "Như các bước",
     "- Mỗi bước sinh đúng dòng: Thêm mới (Tạo phân ca chi tiết mới) -> Sửa có ghi đè -> Xóa gỡ ca -> Xóa nhân viên khỏi bảng -> "
     "Sửa ca trên bảng tổng hợp -> Xóa bảng phân ca chi tiết.\n"
     "- Tổng số dòng tăng đúng bằng số dòng liệt kê, không có dòng thừa.\n"
     "- Popup của A chứa mọi dòng có A (không có dòng Xóa nhân viên B)."),
    (2, "2 người thao tác, phạm vi xem khác nhau", "P1",
     "U1 (quyền công ty), U2 (quyền phòng ban KD1), U3 (quyền bộ phận KD1-Bán lẻ).",
     "1. U1 phân ca cho 1 nhân viên KT và 1 nhân viên KD1-Bán lẻ (2 lần lưu riêng)\n2. Lần lượt đăng nhập U1, U2, U3 mở màn Lịch sử phân ca",
     "Không",
     "- U1 thấy cả 2 dòng.\n- U2 thấy dòng KD1-Bán lẻ, không thấy dòng KT.\n- U3 thấy dòng KD1-Bán lẻ, không thấy dòng KT."),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "GHI LỊCH SỬ - THAO TÁC TRÊN BẢNG PHÂN CA CHI TIẾT", SEC_IV),
    ("V", "GHI LỊCH SỬ - THAO TÁC TRÊN BẢNG PHÂN CA TỔNG HỢP", SEC_V),
    ("VI", "XUẤT EXCEL DANH SÁCH NHÂN VIÊN", SEC_VI),
    ("VII", "POPUP LỊCH SỬ CHỈNH SỬA THEO TỪNG NHÂN VIÊN", SEC_VII),
    ("VIII", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", SEC_VIII),
    ("IX", "E2E FLOW", SEC_IX),
]


def main():
    out = os.path.join(HERE, "testcase - Lịch sử phân ca.xlsx")
    return build(
        output_file=out,
        sheet_name="Trang tính1",
        feature_name="Lịch sử thay đổi - Lịch sử phân ca - Cập nhật ngày 29/09/2026",
        module_name="Lịch sử phân ca",
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )


if __name__ == "__main__":
    main()
