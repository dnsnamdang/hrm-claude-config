# -*- coding: utf-8 -*-
"""Testcase Redmine #10455 - Lich su thay doi nhom Thiet lap cham cong.

5 file (moi man 1 file):
  - testcase - Lich su Quy dinh chung.xlsx
  - testcase - Lich su Quy dinh lam them.xlsx
  - testcase - Lich su Quy dinh nghi.xlsx
  - testcase - Lich su Cai dat.xlsx
  - testcase - Lich su Ca lam viec.xlsx

Nguon: nhanh task_10455 (worktrees/task_10455-client + task_10455-api). Nhan truong lay tu
FIELD_LABELS cua cac popup lich su (FE), danh sach truong theo doi lay tu TRACKED_FIELDS /
SNAPSHOT_FIELDS cua Service (BE).
Chay: /opt/homebrew/opt/python@3.14/bin/python3.14 tc_thiet_lap_cham_cong.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ------------------------------------------------------------------ helper
def S(*a):
    """Buoc thuc hien: danh so, moi buoc 1 dong."""
    return "\n".join("%d. %s" % (i, x) for i, x in enumerate(a, 1))


def B(*a):
    """Ket qua mong doi: gach dau dong, moi y 1 dong."""
    return "\n".join("- " + x for x in a)


def L(*a):
    return "\n".join(a)


def chg(label, old, new):
    return 'nhãn "%s" | cũ "%s" | mới "%s"' % (label, old, new)


PERM = '"Thiết lập thông số"'
TK_A = ('Tài khoản A: có quyền "Thiết lập thông số", được quản lý Công ty 1 và Công ty 2, '
        'đang chọn làm việc ở Công ty 1')
TK_B = 'Tài khoản B: KHÔNG có quyền "Thiết lập thông số" (chỉ có quyền xem Bảng chấm công chi tiết)'
NOT_FOUND = '"Không tìm thấy trang yêu cầu" (dòng dưới: "Không tìm thấy hoặc không được cấp quyền truy cập trang", nút "Về trang chủ")'
MENU_HIDDEN = '(tài khoản không có quyền nào trong nhóm thì cả nhóm menu "Cấu hình" bị ẩn)'

M_GEN = 'Vào phân hệ Chấm công > nhóm menu "Cấu hình" > bấm "Quy định chung"'
M_OT = 'Vào phân hệ Chấm công > nhóm menu "Cấu hình" > bấm "Quy định làm thêm"'
M_HOL = 'Vào phân hệ Chấm công > nhóm menu "Cấu hình" > bấm "Quy định nghỉ"'
M_MASTER = 'Vào phân hệ Chấm công > nhóm menu "Cấu hình" > bấm "Cài đặt"'
M_SUB = 'Vào phân hệ Chấm công > nhóm menu "Cấu hình" > bấm "Cài đặt phân hệ"'
M_SHIFT = 'Vào phân hệ Chấm công > nhóm menu "Danh mục" > bấm "Danh mục ca làm việc"'

COMMON_FORMAT_NOTE = (
    "Popup lịch sử dùng KHUÔN CHUNG toàn hệ thống (cập nhật 30/09/2026): tiêu đề \"Lịch sử thay đổi: <nhãn>\", "
    "biểu tượng đồng hồ trong ô tròn, dấu x góc phải; chân popup chỉ có nút \"Đóng\".\n"
    "Cách đọc 1 dòng lịch sử (mới nhất trên cùng): thời gian dd/mm/yyyy HH:mm (không có giây) -> tên hành động "
    "theo BỘ NHÃN CHUẨN dùng chung mọi màn thiết lập: \"Tạo mới\" (xanh lá), \"Thay đổi thông tin\" (xanh dương), "
    "\"Khóa\" (cam), \"Mở khóa\" (xanh lá), \"Xóa\" (đỏ), \"Thay đổi trạng thái\" (cam) - KHÔNG còn nhãn riêng từng màn "
    "như \"Cập nhật quy định chung\", \"Thêm nhân viên\", \"Khóa loại nghỉ\" -> "
    "\"Người thực hiện: <họ tên> — <tên phòng ban>\" -> khối thay đổi: nhãn trường in đậm, giá trị CŨ chữ đỏ, mũi tên, "
    "giá trị MỚI chữ xanh. Trong testcase viết gọn là: nhãn \"X\" | cũ \"a\" | mới \"b\". Giá trị cũ trống thì CHỈ hiện "
    "giá trị mới (không có mũi tên); giá trị mới trống hiện \"(trống)\".\n"
    "Danh sách (công ty, chức vụ, nhân viên, địa điểm, máy chấm công, khung giờ phạt) hiện theo NHÓM: dòng nhãn "
    "\"<Đối tượng> thêm mới:\" rồi từng phần tử chữ xanh bắt đầu bằng \"- \"; dòng nhãn \"<Đối tượng> đã xóa:\" rồi từng "
    "phần tử chữ đỏ. KHÔNG còn kiểu \"Thêm N ...\" / \"Bỏ N ...\" hay dấu cộng / dấu trừ.\n"
    "Quy ước giá trị: ô tick / bật-tắt hiện Có / Không (KHÔNG có Bật/Tắt); số theo chuẩn quốc tế dấu phẩy ngăn nghìn, "
    "dấu chấm thập phân, bỏ số 0 thừa (1500 hiện 1,500; 5.00 hiện 5; 7.5 hiện 7.5); ô trống hiện (trống) - KHÁC với số 0; "
    "ngày dd/mm/yyyy; giờ HH:mm; danh mục hiện TÊN chứ không hiện mã số; nội dung dài hơn 200 ký tự bị cắt kèm \"…\" "
    "và liên kết \"Xem thêm\"."
)

FILTER_NOTE = (
    "Bộ lọc trong popup (nút \"Bộ lọc\" góc phải trên, chỉ có khi đã có ít nhất 1 dòng lịch sử) gồm 4 ô: "
    "\"Loại hành động\" (ĐÚNG 3 lựa chọn cố định: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái, gợi ý \"Chọn loại hành động\"); "
    "\"Người thực hiện\" (ĐỦ nhân sự của công ty, dạng \"MÃ PHÒNG - Họ tên\", gợi ý \"Chọn người thực hiện\"); "
    "\"Từ ngày\"; \"Đến ngày\". Chọn là lọc NGAY, không có nút Tìm kiếm; nút \"Làm mới\" xoá cả 4 ô. "
    "Lọc ngày: Từ ngày <= ngày thay đổi <= Đến ngày, tính cả 2 đầu mút. Đóng popup rồi mở lại thì bộ lọc được xoá.\n"
    "ĐÃ BỎ các ô lọc cũ \"Trường chỉnh sửa\" và \"Thao tác\" (Thêm / Sửa / Khóa…): không lọc được theo từng trường hay "
    "từng thao tác chi tiết nữa, chỉ lọc theo 3 nhóm."
)
GROUP_NOTE = (
    "Xếp nhóm Loại hành động: dòng tạo mới / thêm bản ghi -> \"Tạo mới\"; sửa trường, thêm / bớt phần tử của 1 danh sách, "
    "thêm / xóa nhân viên miễn chấm công -> \"Thay đổi thông tin\"; khóa, mở khóa, xóa bản ghi -> \"Thay đổi trạng thái\". "
    "Tên hành động trên từng dòng là nhãn chuẩn: \"Tạo mới\" (xanh lá) / \"Thay đổi thông tin\" (xanh dương) / \"Khóa\" (cam) / "
    "\"Mở khóa\" (xanh lá) / \"Xóa\" (đỏ) / \"Thay đổi trạng thái\" (cam); thêm / bớt phần tử danh sách, đổi thứ tự đều là "
    "\"Thay đổi thông tin\". KHÔNG còn nhãn chi tiết cũ (vd \"Khóa loại nghỉ\", \"Thêm nhân viên\")."
)

ACTOR_A = 'dòng "Người thực hiện: <họ tên tài khoản A> — <tên phòng ban của A>"'
EMPTY_TXT = '"Chưa có lịch sử thao tác nào."'
NO_MATCH = '"Không có lịch sử phù hợp bộ lọc."'
PERF_EXAMPLE = '"BDH - Bùi Thị Phương"'


def popup_std(start, what, pre, open_steps, title_label, row_hint, grp_pre, grp_exp,
              scope="công ty đang chọn làm việc", layout_prio="P0"):
    """Bộ TC chuẩn cho 1 popup lịch sử khuôn chung: bố cục + 5 ô lọc (Loại hành động, Người thực hiện,
    Từ ngày, Đến ngày, Làm mới). `open_steps` = các bước mở popup."""
    o = list(open_steps)
    tcs = [
        (start, "Bố cục popup lịch sử " + what, layout_prio, pre, S(*(o + ["Quan sát popup."])), "—",
         B('Tiêu đề popup "Lịch sử thay đổi: %s"; bên trái tiêu đề có biểu tượng đồng hồ trong ô tròn; góc phải có dấu x.' % title_label,
           'Góc phải trên thân popup có nút "Bộ lọc" (khung lọc đang thu gọn); chân popup có ĐÚNG 1 nút "Đóng".',
           'Mỗi dòng lịch sử gồm lần lượt: thời gian dd/mm/yyyy HH:mm (không có giây) -> tên hành động tô màu theo loại -> '
           '"Người thực hiện: <họ tên> — <tên phòng ban>" -> khối thay đổi.',
           row_hint,
           "Dòng mới nhất nằm trên cùng; lịch sử dài thì chỉ thân popup cuộn, nút Bộ lọc và nút Đóng vẫn luôn nhìn thấy.",
           'Bấm "Đóng" hoặc dấu x đều đóng popup, màn bên dưới giữ nguyên, không tự lưu gì.')),
        (start + 1, "Bộ lọc popup " + what + ": ô Loại hành động lọc theo 3 nhóm", "P0", grp_pre,
         S(*(o + ['Bấm "Bộ lọc".', 'Mở ô "Loại hành động", đọc danh sách.',
                  'Lần lượt chọn "Tạo mới", "Thay đổi thông tin", "Thay đổi trạng thái".'])),
         "Loại hành động: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái",
         B('Khung lọc gồm 4 ô theo thứ tự "Loại hành động", "Người thực hiện", "Từ ngày", "Đến ngày" và nút "Làm mới"; KHÔNG có nút "Tìm kiếm".',
           'Ô "Loại hành động" gợi ý "Chọn loại hành động", có ĐÚNG 3 lựa chọn: "Tạo mới", "Thay đổi thông tin", "Thay đổi trạng thái".',
           "Chọn xong là danh sách lọc NGAY, không phải bấm thêm nút.",
           *grp_exp)),
        (start + 2, "Bộ lọc popup " + what + ": ô Người thực hiện", "P1",
         L(pre, "Lịch sử có dòng do tài khoản A và dòng do tài khoản D (cũng có quyền) thực hiện; nhân viên E chưa từng thao tác."),
         S(*(o + ['Bấm "Bộ lọc", mở ô "Người thực hiện", đọc danh sách.', "Gõ tên tài khoản D vào ô tìm của danh sách, chọn D.",
                  "Đổi sang chọn nhân viên E."])),
         L("Người thực hiện: D", "Người thực hiện: E"),
         B('Ô gợi ý "Chọn người thực hiện"; danh sách liệt kê ĐỦ nhân sự của %s (không chỉ người đã có trong lịch sử), '
           'mỗi người dạng "MÃ PHÒNG - Họ tên" (vd %s), gõ tìm được theo tên.' % (scope, PERF_EXAMPLE),
           "Chọn D: chỉ còn các dòng do D thực hiện, dòng người thực hiện ghi tên D.",
           "Chọn E: hiện " + NO_MATCH + ", kèm biểu tượng phễu.")),
        (start + 3, "Bộ lọc popup " + what + ": ô Từ ngày", "P1",
         L(pre, "Lịch sử có dòng ngày 10/09/2026, 15/09/2026 và 20/09/2026."),
         S(*(o + ['Bấm "Bộ lọc".', 'Ở ô "Từ ngày" chọn 15/09/2026.', 'Đổi "Từ ngày" thành 21/09/2026.'])),
         L("Từ ngày: 15/09/2026", "Từ ngày: 21/09/2026"),
         B('Ô gợi ý "Từ ngày", ngày hiện dạng dd/mm/yyyy.',
           "Từ 15/09/2026: còn dòng ngày 15/09 và 20/09 (tính cả ngày 15/09); không còn dòng 10/09.",
           "Từ 21/09/2026: hiện " + NO_MATCH)),
        (start + 4, "Bộ lọc popup " + what + ": ô Đến ngày", "P1",
         L(pre, "Lịch sử có dòng ngày 10/09/2026, 15/09/2026 và 20/09/2026."),
         S(*(o + ['Bấm "Bộ lọc".', 'Ở ô "Đến ngày" chọn 15/09/2026.', 'Chọn thêm "Từ ngày" 15/09/2026.',
                  'Đổi "Từ ngày" thành 16/09/2026 (sau Đến ngày).'])),
         L("Đến ngày: 15/09/2026", "Từ ngày: 15/09/2026 rồi 16/09/2026"),
         B('Ô gợi ý "Đến ngày".',
           "Chỉ Đến 15/09/2026: còn dòng 10/09 và 15/09 (tính cả ngày 15/09); không còn dòng 20/09.",
           "Từ = Đến = 15/09/2026: chỉ còn dòng ngày 15/09.",
           "Từ ngày sau Đến ngày: hiện " + NO_MATCH + ", không báo lỗi, không treo popup.")),
        (start + 5, "Bộ lọc popup " + what + ": nút Làm mới và mở lại popup", "P1", pre,
         S(*(o + ['Bấm "Bộ lọc", chọn đủ 4 ô sao cho danh sách còn 1 dòng.', 'Bấm "Làm mới".',
                  'Chọn lại "Loại hành động" bất kỳ, bấm "Đóng".', "Mở lại popup."])),
         "—",
         B("Sau Làm mới: 4 ô trở về chữ gợi ý, danh sách hiện lại ĐỦ dòng ngay; khung lọc vẫn đang mở.",
           "Mở lại popup: khung lọc thu gọn, không còn điều kiện cũ, hiện đủ lịch sử.")),
    ]
    return tcs


def renum(tcs, start=1):
    """Đánh lại số thứ tự TC trong 1 section (ghép từ nhiều khối)."""
    return [(start + i,) + tuple(tc[1:]) for i, tc in enumerate(tcs)]


def popup_empty(num, what, pre, open_steps, prio="P2"):
    return (num, "Popup " + what + " khi chưa có lịch sử", prio, pre, S(*(list(open_steps) + ["Quan sát popup."])), "—",
            B("Popup hiện biểu tượng đồng hồ xám và chữ " + EMPTY_TXT,
              'KHÔNG hiện nút "Bộ lọc"; chân popup vẫn có nút "Đóng".'))


def auto_tc(num, prio, menu, tab_step, action, td, label, old, new, title, actor,
            pre_extra=(), exp_extra=(), toast="Cập nhật thành công", open_hist=None):
    """TC 1 truong tren man TU LUU khi doi gia tri (tab Chung Quy dinh chung / lam them / nghi)."""
    open_hist = open_hist or 'Bấm nút "Lịch sử thay đổi" (góc phải trên cùng tab Chung).'
    pre = L(TK_A, *pre_extra)
    steps = S("Đăng nhập tài khoản A.", menu + ".", tab_step, action,
              'Chờ thông báo "%s".' % toast, open_hist, "Quan sát dòng lịch sử trên cùng.")
    exp = B('Hiện thông báo "%s", màn không tải lại.' % toast,
            'Dòng trên cùng popup có tên hành động "%s" (chữ xanh dương), thời gian đúng lúc vừa thao tác, %s.' % (title, actor),
            "Dòng này có ĐÚNG 1 thay đổi: " + chg(label, old, new) + ".",
            "KHÔNG kèm trường nào khác trong cùng dòng.",
            *exp_extra)
    return (num, "Ghi lịch sử khi đổi trường \"%s\"" % label, prio, pre, steps, td, exp)


# ======================================================================
# 1. QUY DINH CHUNG
# ======================================================================
def quy_dinh_chung():
    title = "Thay đổi thông tin"
    actor = ACTOR_A
    tab = 'Ở tab "Chung".'

    desc = [
        ("1. Mục đích tính năng",
         "Ghi lại và cho xem lịch sử thay đổi của màn Quy định chung (phân hệ Chấm công): ai đổi, "
         "đổi trường nào, giá trị cũ, giá trị mới, lúc nào. Có 3 popup lịch sử: tab Chung, tab "
         "Danh sách miễn chấm công, tab Danh sách CTV miễn chấm công."),
        ("2. Đối tượng được tính / hiển thị",
         "Tab Chung: 14 trường được ghi lịch sử (nhãn trong popup):\n"
         "Nghỉ tuần; Bật/tắt số lần tra soát công tối đa trong tháng; Số lần tra soát công tối đa trong tháng; "
         "Bật/tắt tra soát công trong vòng X giờ; Số giờ được tra soát công; Lập đơn đi muộn/về sớm trước (giờ); "
         "Không sử dụng google map với ca làm việc; Bật/tắt khoảng cách chấm công tối đa; "
         "Khoảng cách chấm công tối đa (m); Khoảng cách chấm công tối đa cho phiếu giao việc công tác (m); "
         "Khoảng cách chấm công tối đa cho làm thêm giờ (m); Số ngày công tối thiểu tính BHXH; Bản đồ; "
         "Nội dung đính kèm email.\n"
         "Tab Danh sách miễn chấm công: mỗi lần Thêm / Xóa 1 nhân viên sinh 1 dòng tên hành động \"Thay đổi thông tin\" (xanh dương) "
         "- thêm hay xóa phân biệt ở nội dung, bên dưới là nhóm \"Nhân viên thêm mới:\" / \"Nhân viên đã xóa:\" với dòng "
         "\"- Mã NV - Họ tên - Mã phòng ban\".\n"
         "Tab Danh sách CTV miễn chấm công: dòng Thêm/Xóa sinh tự động khi Sửa phòng ban tick/bỏ tick "
         "\"Cộng tác viên: Nghiệp vụ\" ở Danh mục phòng ban.\n"
         "Tiêu đề 3 popup: \"Lịch sử thay đổi: Quy định chung\", \"Lịch sử thay đổi: Danh sách miễn chấm công\", "
         "\"Lịch sử thay đổi: Danh sách CTV miễn chấm công\"."),
        ("3. Đối tượng bị ẩn / không tính",
         "- Lưu mà không đổi giá trị nào: KHÔNG sinh dòng.\n"
         "- Thao tác bị chặn bởi kiểm tra dữ liệu (vd Số ngày công tối thiểu tính BHXH nhập 1.5): KHÔNG lưu, KHÔNG sinh dòng.\n"
         "- Lịch sử của công ty khác (không phải công ty đang chọn làm việc) không hiện.\n"
         "- Trường Tra soát tháng trước trước ngày mùng không nằm trên màn này (đã chuyển sang màn Cài đặt).\n"
         "- Lọc \"Tạo mới\" hoặc \"Thay đổi trạng thái\" ở cả 3 popup luôn ra rỗng (màn này chỉ có thay đổi thông tin)."),
        ("4. Bộ lọc thời gian áp dụng cho", FILTER_NOTE),
        ("5. Cấu trúc dữ liệu / cây phân cấp",
         "Popup dạng dòng thời gian, mới nhất ở TRÊN CÙNG. Mỗi dòng: thời gian, tên hành động \"Thay đổi thông tin\" (xanh dương), "
         "người thực hiện kèm phòng ban, danh sách trường đổi. Popup miễn chấm công: mỗi dòng 1 nhân viên, "
         "tên hành động \"Thay đổi thông tin\" (xanh dương), nhân viên thêm nằm trong nhóm \"Nhân viên thêm mới:\" chữ xanh, "
         "nhân viên xóa nằm trong nhóm \"Nhân viên đã xóa:\" chữ đỏ.\n" + GROUP_NOTE),
        ("6. Quy tắc cộng dồn / deduplicate",
         "Màn Quy định chung TỰ LƯU ngay khi đổi (tick, chọn radio) hoặc khi rời khỏi ô số / ô nội dung email - "
         "không có nút Lưu. Mỗi lần tự lưu có thay đổi sinh 1 dòng. So sánh theo giá trị THẬT sau khi lưu, "
         "nên \"5\" và 5 là như nhau (không sinh dòng rác). Thêm lại nhân viên đã có trong danh sách miễn chấm công không sinh dòng."),
        ("7. Phân quyền cấp",
         "- \"Thiết lập thông số\": thấy menu Quy định chung, thấy 3 nút \"Lịch sử thay đổi\", đổi được thiết lập.\n"
         "- Không có \"Thiết lập thông số\": không thấy menu; mở địa chỉ màn bị đưa về trang \"Không tìm thấy trang yêu cầu\"; không thấy nút Lịch sử.\n"
         "- Sửa phòng ban (lối sinh lịch sử CTV): cần quyền \"Quản lý danh mục phòng ban\"."),
        ("8. Cách tính các ô thống kê", "Không áp dụng - popup lịch sử không có ô thống kê, không phân trang."),
        ("9. Ghi chú đọc bảng",
         COMMON_FORMAT_NOTE + "\n"
         "Bẫy dễ sai: (1) ô số chỉ lưu khi bấm ra ngoài ô, gõ xong phải bấm ra ngoài; (2) 2 ô Khoảng cách chấm công tối đa "
         "và ... cho phiếu giao việc công tác bị khoá khi ô tick Khoảng cách chấm công tối đa không tick, và ô tick này "
         "đang bị KHOÁ cố định trên màn; (3) Nội dung đính kèm email hiện dạng chữ trơn, dài hơn 200 ký tự thì cắt kèm \"…\" và liên kết \"Xem thêm\"; "
         "(4) Popup miễn chấm công chỉ hiện nhân viên của công ty đang chọn làm việc; (5) Thêm và Xóa nhân viên miễn chấm công "
         "cùng thuộc nhóm \"Thay đổi thông tin\" - bộ lọc không tách riêng được Thêm với Xóa."),
    ]

    roles = [
        ("01", "Tài khoản có quyền thấy menu và 3 nút Lịch sử thay đổi", "P0",
         TK_A,
         S("Đăng nhập tài khoản A.", M_GEN + ".", 'Quan sát tab "Chung".',
           'Bấm tab "Danh sách miễn chấm công", quan sát thanh nút.',
           'Bấm tab "Danh sách CTV miễn chấm công", quan sát thanh nút.'),
         "—",
         B('Menu "Quy định chung" hiện trong nhóm "Cấu hình".',
           'Tab Chung: nút "Lịch sử thay đổi" (biểu tượng đồng hồ) ở góc phải trên cùng.',
           'Tab Danh sách miễn chấm công: nút "Lịch sử thay đổi" nằm bên phải nút "Thêm mới".',
           'Tab Danh sách CTV miễn chấm công: nút "Lịch sử thay đổi" nằm bên trái nút "Bộ lọc".')),
        ("02", "Tài khoản không có quyền không thấy menu, không vào được màn", "P0",
         L(TK_B, "Có sẵn địa chỉ màn Quy định chung (sao chép từ trình duyệt của tài khoản A)."),
         S("Đăng nhập tài khoản B.", 'Mở phân hệ Chấm công, mở nhóm "Cấu hình".',
           "Dán địa chỉ màn Quy định chung đã sao chép vào thanh địa chỉ, Enter."),
         "—",
         B('KHÔNG thấy mục "Quy định chung" ' + MENU_HIDDEN + '.',
           "Mở địa chỉ màn bị chuyển sang trang " + NOT_FOUND + ".",
           "Không nhìn thấy nút Lịch sử thay đổi, không xem được lịch sử.")),
        ("03", "Tài khoản chỉ có quyền Thiết lập thông số lương vẫn không vào được Quy định chung", "P1",
         'Tài khoản C: có "Thiết lập thông số lương", KHÔNG có "Thiết lập thông số".',
         S("Đăng nhập tài khoản C.", 'Mở phân hệ Chấm công, nhóm "Cấu hình".',
           "Dán địa chỉ màn Quy định chung vào thanh địa chỉ."),
         "—",
         B('Không thấy mục "Quy định chung" ' + MENU_HIDDEN + '.', "Bị chuyển sang trang " + NOT_FOUND + ".")),
        ("04", "Thu hồi quyền khi đang mở màn thì tải lại bị chặn", "P1",
         L(TK_A, "Quản trị viên chuẩn bị gỡ quyền \"Thiết lập thông số\" khỏi vai trò của tài khoản A."),
         S("Tài khoản A mở màn Quy định chung.", 'Quản trị viên gỡ quyền "Thiết lập thông số" khỏi A.',
           "Tài khoản A đăng xuất rồi đăng nhập lại, mở lại màn."),
         "—",
         B('Sau khi đăng nhập lại, menu "Quy định chung" biến mất.',
           "Mở lại địa chỉ màn bị chuyển sang trang " + NOT_FOUND + ".")),
    ]

    OPEN_GEN = ["Đăng nhập tài khoản A.", M_GEN + ".", 'Ở tab "Chung" bấm "Lịch sử thay đổi".']
    sec1 = [
        (1, "Vị trí nút Lịch sử thay đổi ở tab Chung", "P1", TK_A,
         S("Đăng nhập tài khoản A.", M_GEN + ".", 'Quan sát phần đầu tab "Chung".'), "—",
         B('Nút "Lịch sử thay đổi" nền sáng, biểu tượng đồng hồ, căn phải, nằm TRÊN mục "Nghỉ tuần".',
           "Nút không che nội dung, không làm lệch các ô bên dưới.")),
        (2, "Thứ tự dòng lịch sử mới nhất ở trên", "P0",
         L(TK_A, "Lần lượt đổi: 09:00 Nghỉ tuần; 09:05 Số giờ được tra soát công; 09:10 Bản đồ."),
         S(*(OPEN_GEN + ["Đọc thời gian 3 dòng đầu."])), "—",
         B("Dòng 1 là thay đổi Bản đồ (09:10), dòng 2 Số giờ được tra soát công (09:05), dòng 3 Nghỉ tuần (09:00).",
           "Thời gian dạng dd/mm/yyyy HH:mm (không có giây).")),
        popup_empty(3, "tab Chung", "Tài khoản A chuyển sang Công ty 2 - công ty chưa từng đổi Quy định chung.",
                    ["Chọn làm việc ở Công ty 2.", M_GEN + ".", 'Bấm "Lịch sử thay đổi".'], prio="P1"),
    ]

    sec2 = popup_std(
        1, "tab Chung", L(TK_A, "Công ty 1 đã có 3 lần đổi thiết lập tab Chung."), OPEN_GEN, "Quy định chung",
        'Dòng đổi trường có tên hành động "Thay đổi thông tin" chữ xanh dương; bên dưới mỗi trường đổi 1 dòng: nhãn in đậm, giá trị cũ đỏ, mũi tên, giá trị mới xanh (vd "Nghỉ tuần: Chủ Nhật -> Thứ 7 và CN").',
        L(TK_A, "Công ty 1 có 3 dòng lịch sử đổi thiết lập tab Chung."),
        ('"Thay đổi thông tin": hiện đủ 3 dòng "Thay đổi thông tin" (mọi thay đổi ở tab Chung đều thuộc nhóm này).',
         '"Tạo mới" và "Thay đổi trạng thái": hiện ' + NO_MATCH + " kèm biểu tượng phễu."))

    # ---- 14 truong tab Chung
    f = []
    f.append(auto_tc(1, "P0", M_GEN, tab, 'Ở mục "Nghỉ tuần", chọn "Chủ Nhật".',
                     L('Mục: Nghỉ tuần', 'Trước: Thứ 7 và CN', 'Sau: Chủ Nhật'),
                     "Nghỉ tuần", "Thứ 7 và CN", "Chủ Nhật", title, actor,
                     pre_extra=('Nghỉ tuần đang chọn "Thứ 7 và CN".',),
                     exp_extra=("Giá trị hiện đúng TÊN lựa chọn, không hiện số thứ tự.",)))
    f.append(auto_tc(2, "P0", M_GEN, tab,
                     'Ở mục "Tra soát công", tick ô "Số lần tra soát công tối đa trong tháng".',
                     L("Ô tick: Số lần tra soát công tối đa trong tháng", "Trước: không tick", "Sau: tick"),
                     "Bật/tắt số lần tra soát công tối đa trong tháng", "Không", "Có", title, actor,
                     pre_extra=("Ô tick này đang bỏ trống, ô số bên cạnh = 3.",),
                     exp_extra=("Hiện Có / Không, KHÔNG hiện Bật / Tắt, 1 / 0 hay true / false.",)))
    f.append(auto_tc(3, "P0", M_GEN, tab,
                     'Sửa ô số cạnh "Số lần tra soát công tối đa trong tháng" từ 3 thành 4 rồi bấm ra ngoài ô.',
                     L("Ô số: Số lần tra soát công tối đa trong tháng (lần)", "Trước: 3", "Sau: 4"),
                     "Số lần tra soát công tối đa trong tháng", "3", "4", title, actor,
                     pre_extra=("Ô tick Số lần tra soát công tối đa trong tháng đang tick, ô số = 3.",),
                     exp_extra=("Gõ số mà chưa bấm ra ngoài ô thì chưa lưu, chưa có dòng mới.",)))
    f.append(auto_tc(4, "P0", M_GEN, tab, 'Bỏ tick ô "Tra soát công trong vòng ... giờ".',
                     L("Ô tick: Tra soát công trong vòng ... giờ", "Trước: tick", "Sau: bỏ tick"),
                     "Bật/tắt tra soát công trong vòng X giờ", "Có", "Không", title, actor,
                     pre_extra=("Ô tick Tra soát công trong vòng ... giờ đang tick, ô số = 48.",),
                     exp_extra=("Ô số 48 bị khoá (xám) sau khi bỏ tick nhưng KHÔNG sinh thay đổi cho Số giờ được tra soát công.",)))
    f.append(auto_tc(5, "P0", M_GEN, tab, 'Sửa ô số giờ trong "Tra soát công trong vòng ... giờ" từ 48 thành 72, bấm ra ngoài ô.',
                     L("Ô số: Tra soát công trong vòng ... giờ", "Trước: 48", "Sau: 72"),
                     "Số giờ được tra soát công", "48", "72", title, actor,
                     pre_extra=("Ô tick Tra soát công trong vòng ... giờ đang tick.",)))
    f.append(auto_tc(6, "P0", M_GEN, tab,
                     'Ở mục "Đăng ký đi muộn về sớm", sửa ô "Lập đơn đăng ký trước ... giờ" từ 2 thành 3, bấm ra ngoài ô.',
                     L("Ô số: Lập đơn đăng ký trước ... giờ", "Trước: 2", "Sau: 3"),
                     "Lập đơn đi muộn/về sớm trước (giờ)", "2", "3", title, actor))
    f.append(auto_tc(7, "P0", M_GEN, tab, 'Ở mục "Chấm công", tick "Không sử dụng google map với ca làm việc".',
                     L("Ô tick: Không sử dụng google map với ca làm việc", "Trước: không tick", "Sau: tick"),
                     "Không sử dụng google map với ca làm việc", "Không", "Có", title, actor))
    f.append((8, 'Trường "Bật/tắt khoảng cách chấm công tối đa" bị khoá trên màn, không sinh lịch sử', "P1",
              L(TK_A, "Ô tick Khoảng cách chấm công tối đa đang ở trạng thái (tick hoặc không) do hệ thống đặt sẵn."),
              S("Đăng nhập tài khoản A.", M_GEN + ".", 'Ở mục "Chấm công", bấm vào ô tick "Khoảng cách chấm công tối đa" (và 2 ô tick cùng hàng bên dưới).',
                "Mở popup lịch sử."),
              "Ô tick: Khoảng cách chấm công tối đa",
              B("Cả 3 ô tick Khoảng cách chấm công tối đa đều bị khoá (xám), bấm không đổi trạng thái.",
                "Không hiện thông báo lưu, popup KHÔNG có dòng mới.",
                'Lưu ý: nhãn "Bật/tắt khoảng cách chấm công tối đa" vẫn có thể xuất hiện trong lịch sử cũ nhưng chỉ đổi được khi hệ thống/cấu hình cũ đổi - ghi Pending nếu nghiệp vụ cần đổi được trên màn.')))
    f.append(auto_tc(9, "P0", M_GEN, tab, 'Sửa ô "Khoảng cách chấm công tối đa ... m" từ 800 thành 1500, bấm ra ngoài ô.',
                     L("Ô số: Khoảng cách chấm công tối đa (m)", "Trước: 800", "Sau: 1500"),
                     "Khoảng cách chấm công tối đa (m)", "800", "1,500", title, actor,
                     pre_extra=("Ô tick Khoảng cách chấm công tối đa đang TICK (ô số mở khoá), ô số = 800.",),
                     exp_extra=("Giá trị mới có dấu phẩy ngăn nghìn: 1,500 (không phải 1500 hay 1.500).",)))
    f.append(auto_tc(10, "P0", M_GEN, tab,
                     'Sửa ô "Khoảng cách chấm công tối đa cho phiếu giao việc công tác ... m" từ 1000 thành 2000, bấm ra ngoài ô.',
                     L("Ô số: Khoảng cách chấm công tối đa cho phiếu giao việc công tác (m)", "Trước: 1000", "Sau: 2000"),
                     "Khoảng cách chấm công tối đa cho phiếu giao việc công tác (m)", "1,000", "2,000", title, actor,
                     pre_extra=("Ô tick Khoảng cách chấm công tối đa đang TICK.",)))
    f.append(auto_tc(11, "P0", M_GEN, tab,
                     'Sửa ô "Khoảng cách chấm công tối đa cho làm thêm giờ ... m" từ 500 thành 700, bấm ra ngoài ô.',
                     L("Ô số: Khoảng cách chấm công tối đa cho làm thêm giờ (m)", "Trước: 500", "Sau: 700"),
                     "Khoảng cách chấm công tối đa cho làm thêm giờ (m)", "500", "700", title, actor,
                     exp_extra=("Ô này mở cho sửa kể cả khi ô tick Khoảng cách chấm công tối đa không tick.",)))
    f.append(auto_tc(12, "P0", M_GEN, tab,
                     'Sửa ô "Số ngày công tối thiểu tính BHXH" từ 14 thành 15, bấm ra ngoài ô.',
                     L("Ô số: Số ngày công tối thiểu tính BHXH (ngày)", "Trước: 14", "Sau: 15"),
                     "Số ngày công tối thiểu tính BHXH", "14", "15", title, actor))
    f.append(auto_tc(13, "P0", M_GEN, tab, 'Ở mục "Bản đồ", tick "Sử dụng bản đồ miễn phí".',
                     L("Mục: Bản đồ", "Trước: Sử dụng bản đồ mất phí", "Sau: Sử dụng bản đồ miễn phí"),
                     "Bản đồ", "Sử dụng bản đồ mất phí", "Sử dụng bản đồ miễn phí", title, actor,
                     pre_extra=('Đang tick "Sử dụng bản đồ mất phí".',),
                     exp_extra=("Ô vừa chọn chuyển sang khoá (không bỏ tick được), ô kia mở ra - 2 ô hoạt động như chọn 1.",)))
    f.append(auto_tc(14, "P0", M_GEN, tab,
                     'Ở ô soạn "Nội dung đính kèm email", sửa câu "Kính gửi anh/chị" thành "Kính gửi Quý anh/chị", rồi bấm ra ngoài ô soạn.',
                     L("Ô: Nội dung đính kèm email", "Trước: Kính gửi anh/chị", "Sau: Kính gửi Quý anh/chị"),
                     "Nội dung đính kèm email", "Kính gửi anh/chị", "Kính gửi Quý anh/chị", title, actor,
                     exp_extra=("Nội dung hiện dạng chữ trơn, KHÔNG hiện thẻ định dạng (dấu < >, p, br...).",)))
    f.append((15, "Nội dung đính kèm email dài hơn 200 ký tự bị cắt, bấm Xem thêm để xem đủ", "P1",
              L(TK_A, "Nội dung email hiện tại ngắn (20 ký tự)."),
              S("Đăng nhập tài khoản A, " + M_GEN + ".", "Dán vào ô soạn email một đoạn 250 ký tự, có in đậm 1 chữ, bấm ra ngoài ô.",
                'Mở popup lịch sử, ở giá trị mới bấm "Xem thêm".', 'Bấm "Thu gọn".'),
              "Nội dung mới: đoạn văn 250 ký tự",
              B('Giá trị mới hiện 200 ký tự đầu, dấu "…" ở cuối và liên kết chữ xanh "Xem thêm".',
                'Bấm "Xem thêm": hiện đủ 250 ký tự dạng chữ trơn, liên kết đổi thành "Thu gọn"; bấm "Thu gọn" quay lại dạng rút gọn.',
                "Chữ in đậm không làm lộ thẻ định dạng trong popup; xuống dòng trong nội dung được giữ.")))

    # ---- mien cham cong
    OPEN_TE = ["Đăng nhập tài khoản A.", M_GEN + ".", 'Bấm tab "Danh sách miễn chấm công".', 'Bấm "Lịch sử thay đổi".']
    OPEN_CTV = ["Đăng nhập tài khoản A.", M_GEN + ".", 'Bấm tab "Danh sách CTV miễn chấm công".', 'Bấm "Lịch sử thay đổi".']
    te_std = popup_std(
        1, "danh sách miễn chấm công", L(TK_A, "Công ty 1 đã có 2 lần thêm, 1 lần xóa nhân viên miễn chấm công."), OPEN_TE,
        "Danh sách miễn chấm công",
        'Cả dòng thêm lẫn dòng xóa đều có tên hành động "Thay đổi thông tin" chữ xanh dương (KHÔNG còn "Thêm nhân viên" / "Xóa nhân viên"); '
        'dòng thêm: nhãn "Nhân viên thêm mới:" và dòng chữ xanh "- <Mã NV> - <Họ tên> - <Mã phòng ban>"; dòng xóa: nhãn "Nhân viên đã xóa:" và dòng chữ đỏ.',
        L(TK_A, "Lịch sử có 2 dòng thêm nhân viên, 1 dòng xóa nhân viên."),
        ('"Thay đổi thông tin": hiện đủ 3 dòng - cả 2 dòng thêm và dòng xóa nhân viên (thêm / bớt phần tử danh sách là thay đổi thông tin).',
         '"Tạo mới" và "Thay đổi trạng thái": hiện ' + NO_MATCH,
         "Lưu ý: bộ lọc KHÔNG tách riêng được Thêm với Xóa (ô Thao tác cũ đã bỏ)."))
    te_rows = [
        (0, "Thêm nhân viên vào danh sách miễn chấm công sinh dòng lịch sử", "P0",
         L(TK_A, "Nhân viên NV001 - Trần Văn Bình - phòng HN_KD1, thuộc Công ty 1, chưa có trong danh sách."),
         S("Đăng nhập tài khoản A.", M_GEN + ".", 'Tab "Danh sách miễn chấm công", bấm "Thêm mới".',
           'Trong popup "Thêm nhân viên" gõ NV001 vào ô "Tìm kiếm...", bấm vào dòng NV001.', 'Chờ thông báo "Thêm nhân viên miễn chấm công thành công".',
           'Popup "Thêm nhân viên" vẫn mở để chọn tiếp: bấm dấu x góc phải để đóng.', 'Bấm "Lịch sử thay đổi".'),
         L("Nhân viên:", "NV001 - Trần Văn Bình - HN_KD1"),
         B("Bảng danh sách có thêm dòng NV001.",
           'Dòng trên cùng popup: tên hành động "Thay đổi thông tin" chữ xanh dương; bên dưới nhãn "Nhân viên thêm mới:" và dòng chữ xanh "- NV001 - Trần Văn Bình - HN_KD1".',
           ACTOR_A[0].upper() + ACTOR_A[1:] + ", thời gian đúng lúc thêm.",
           'Lọc "Loại hành động" = "Thay đổi thông tin" vẫn thấy dòng này.')),
        (0, "Xóa nhân viên khỏi danh sách miễn chấm công sinh dòng lịch sử", "P0",
         L(TK_A, "NV001 đang có trong danh sách miễn chấm công của Công ty 1."),
         S(M_GEN + ", tab Danh sách miễn chấm công.", "Ở dòng NV001 bấm biểu tượng bánh răng > Xóa.",
           'Popup "Cảnh báo" hỏi "Bạn có chắc chắn muốn xóa không?", bấm "Xoá".', 'Chờ thông báo "Xoá thành công".', 'Bấm "Lịch sử thay đổi".'),
         "Nhân viên: NV001",
         B("NV001 biến mất khỏi bảng.",
           'Dòng trên cùng popup: tên hành động "Thay đổi thông tin" chữ xanh dương (KHÔNG phải "Xóa" đỏ - xóa phần tử danh sách là thay đổi thông tin); bên dưới nhãn "Nhân viên đã xóa:" và dòng chữ đỏ "- NV001 - Trần Văn Bình - HN_KD1".',
           'Dòng này thuộc nhóm "Thay đổi thông tin" (KHÔNG thuộc "Thay đổi trạng thái").')),
        (0, "Bấm Huỷ ở xác nhận xóa không sinh dòng", "P1", L(TK_A, "NV002 có trong danh sách."),
         S("Bánh răng dòng NV002 > Xóa.", 'Bấm "Huỷ".', "Mở popup lịch sử."), "—",
         B("NV002 vẫn còn trong bảng.", "Popup không có dòng mới nào nhắc NV002 trong nhóm \"Nhân viên đã xóa:\".")),
        (0, "Thêm lại nhân viên đã có trong danh sách bị từ chối, không sinh dòng", "P1", L(TK_A, "NV002 đã có trong danh sách."),
         S('Bấm "Thêm mới", gõ NV002 vào ô "Tìm kiếm...", bấm vào dòng NV002.', "Bấm dấu x đóng popup Thêm nhân viên, mở popup lịch sử."), "Nhân viên: NV002",
         B('Hiện thông báo lỗi (khung đỏ) "Nhân viên đã có trong danh sách miễn chấm công."; KHÔNG hiện thông báo thành công nào.',
           "Bảng không nhân đôi NV002.", "Popup KHÔNG có dòng mới nào nhắc NV002.")),
        popup_empty(0, "danh sách miễn chấm công", "Tài khoản A chuyển sang Công ty 2 - chưa từng thêm / xóa nhân viên miễn chấm công.",
                    ["Chọn làm việc ở Công ty 2.", M_GEN + ".", 'Bấm tab "Danh sách miễn chấm công", bấm "Lịch sử thay đổi".']),
    ]
    ctv_std = popup_std(
        1, "danh sách CTV miễn chấm công", L(TK_A, "Công ty 1 có 2 dòng thêm nhân viên và 1 dòng xóa nhân viên ở danh sách CTV."), OPEN_CTV,
        "Danh sách CTV miễn chấm công",
        "Chỉ hiện dòng của nhân viên CTV (phòng ban Nghiệp vụ), KHÔNG lẫn dòng của tab Danh sách miễn chấm công; cách hiển thị thêm / xóa nhân viên giống popup Danh sách miễn chấm công (tên hành động \"Thay đổi thông tin\" xanh dương).",
        L(TK_A, "Lịch sử CTV có 2 dòng thêm nhân viên, 1 dòng xóa nhân viên."),
        ('"Thay đổi thông tin": hiện đủ 3 dòng.', '"Tạo mới" và "Thay đổi trạng thái": hiện ' + NO_MATCH),
        layout_prio="P0")
    ctv_rows = [
        (0, "Đổi phòng ban sang Cộng tác viên Nghiệp vụ sinh dòng thêm nhân viên ở popup CTV", "P0",
         L(TK_A + '; có thêm quyền "Quản lý danh mục phòng ban".',
           "Phòng HN_CTV (Công ty 1) có 2 nhân viên NV101, NV102, chưa tick Cộng tác viên."),
         S('Vào phân hệ Nhân sự > "Danh mục phòng ban", Sửa phòng HN_CTV.',
           'Ở "Cộng tác viên" tick "Nghiệp vụ", lưu.', M_GEN + ", tab Danh sách CTV miễn chấm công.", 'Bấm "Lịch sử thay đổi".'),
         "Cộng tác viên: Nghiệp vụ",
         B("Bảng CTV có NV101, NV102.",
           'Popup có 2 dòng "Thay đổi thông tin" (chữ xanh dương), mỗi dòng nhãn "Nhân viên thêm mới:" và "- NV101 - ... - HN_CTV" / "- NV102 - ... - HN_CTV"; người thực hiện là tài khoản A.',
           "Lưu ý: nếu ô Cộng tác viên bị khoá (công ty dùng phân hệ Quyết định) thì ghi Pending, không thực hiện được.")),
        (0, "Bỏ tick Cộng tác viên Nghiệp vụ sinh dòng xóa nhân viên ở popup CTV", "P1",
         L(TK_A, "Phòng HN_CTV đang tick Nghiệp vụ, 2 nhân viên đang trong danh sách CTV."),
         S("Sửa phòng HN_CTV, bỏ tick Nghiệp vụ, lưu.", "Mở popup lịch sử tab Danh sách CTV miễn chấm công."), "—",
         B("NV101, NV102 biến mất khỏi bảng CTV.", 'Popup có 2 dòng "Thay đổi thông tin" chữ xanh dương, nhãn "Nhân viên đã xóa:" và dòng chữ đỏ của từng người.')),
    ]
    sec5 = renum(te_std + te_rows)
    sec6 = renum(ctv_std + ctv_rows)

    sec8 = [
        (1, "Rời ô số mà không đổi giá trị không sinh dòng", "P0", L(TK_A, "Số giờ được tra soát công = 48."),
         S(M_GEN + ".", "Bấm vào ô 48, không gõ gì, bấm ra ngoài.", "Chọn lại đúng radio Nghỉ tuần đang chọn.", "Mở popup lịch sử."),
         "Không đổi giá trị",
         B("Popup KHÔNG có dòng mới (số dòng giữ nguyên như trước thao tác).",
           "Nếu có hiện thông báo Cập nhật thành công thì vẫn KHÔNG được sinh dòng rỗng.")),
        (2, "Nhập sai Số ngày công tối thiểu tính BHXH bị chặn, không sinh dòng", "P0", L(TK_A, "Số ngày công tối thiểu tính BHXH = 14."),
         S(M_GEN + ".", "Nhập 1.5 vào ô Số ngày công tối thiểu tính BHXH, bấm ra ngoài.", "Lặp lại với -3 và abc.", "Tải lại trang, mở popup lịch sử."),
         L("1.5", "-3", "abc"),
         B('Hiện thông báo lỗi "Vui lòng kiểm tra lại dữ liệu nhập", dưới ô hiện chữ đỏ "Giá trị phải là số nguyên dương."',
           "Giá trị user gõ vẫn giữ nguyên trong ô (không tự sửa về 14).",
           "Tải lại trang ô vẫn là 14; popup KHÔNG có dòng mới cho Số ngày công tối thiểu tính BHXH.")),
        (3, "Xoá trống ô số thì lịch sử ghi đúng giá trị thật đã lưu", "P0", L(TK_A, "Lập đơn đăng ký trước = 2 giờ."),
         S(M_GEN + ".", 'Xoá trống ô "Lập đơn đăng ký trước ... giờ", bấm ra ngoài.', "Tải lại trang, ghi nhận giá trị ô hiển thị.", "Mở popup lịch sử."),
         L("Trước: 2", "Sau: để trống"),
         B('Dòng mới: nhãn "Lập đơn đi muộn/về sớm trước (giờ)" | cũ "2" | mới = ĐÚNG giá trị ô hiển thị sau khi tải lại.',
           'Nếu ô hiện trống thì popup ghi "(trống)"; nếu ô hiện 0 thì popup ghi "0" - KHÔNG được ghi (trống) khi màn hiện 0 và ngược lại.')),
        (4, "Sửa liên tiếp 2 trường sinh 2 dòng riêng", "P1", TK_A,
         S(M_GEN + ".", "Đổi Nghỉ tuần sang Thứ 7.", "Đổi Số ngày công tối thiểu tính BHXH 15 thành 16, bấm ra ngoài.", "Mở popup lịch sử."),
         "—",
         B("Có 2 dòng mới: dòng trên cùng là Số ngày công tối thiểu tính BHXH, dòng dưới là Nghỉ tuần.",
           "Mỗi dòng chỉ chứa 1 trường của lần lưu đó.")),
    ]

    sec9 = [
        (1, "Lịch sử tab Chung chỉ của công ty đang chọn làm việc", "P0",
         L(TK_A, "Công ty 1 có 5 dòng lịch sử Quy định chung, Công ty 2 có 1 dòng."),
         S("Đang ở Công ty 1, mở popup lịch sử tab Chung, đếm dòng.", "Đổi công ty làm việc sang Công ty 2.", M_GEN + ", mở lại popup."),
         "—",
         B("Công ty 1: 5 dòng; Công ty 2: đúng 1 dòng.", "Không thấy dòng của công ty kia ở mỗi bên.")),
        (2, "Hai người cùng sửa, mỗi dòng ghi đúng người thực hiện", "P1",
         "Tài khoản A và D cùng có quyền, cùng Công ty 1.",
         S("A đổi Nghỉ tuần.", "D (máy khác) đổi Bản đồ.", "A mở popup lịch sử."), "—",
         B('Dòng Bản đồ ghi "Người thực hiện: <họ tên D> — <phòng ban của D>", dòng Nghỉ tuần ghi "Người thực hiện: <họ tên A> — <phòng ban của A>".')),
    ]

    sec11 = [
        (1, "Trường bật/tắt hiện Có/Không thay cho Bật/Tắt", "P0", TK_A,
         S(M_GEN + ".", 'Tick rồi bỏ tick "Không sử dụng google map với ca làm việc".', "Mở popup lịch sử."), "—",
         B('2 dòng mới lần lượt: cũ "Không" mới "Có"; cũ "Có" mới "Không".', "Không còn chữ Bật / Tắt ở giá trị.")),
        (2, "Số hiển thị chuẩn quốc tế có dấu phẩy ngăn nghìn", "P0", L(TK_A, "Khoảng cách chấm công tối đa = 1000, ô tick đang tick."),
         S(M_GEN + ".", "Sửa Khoảng cách chấm công tối đa thành 12500, bấm ra ngoài.", "Mở popup."), "12500",
         B('Dòng mới: cũ "1,000" mới "12,500".')),
        (3, "Mũi tên giữa giá trị cũ và mới màu xám, không đỏ", "P1", TK_A,
         S("Mở popup lịch sử có ít nhất 1 dòng.", "Quan sát mũi tên giữa giá trị cũ và mới."), "—",
         B("Mũi tên màu xám; chỉ giá trị cũ màu đỏ, giá trị mới màu xanh.")),
        (4, "Danh sách miễn chấm công chỉ hiện nhân viên của công ty đang chọn", "P0",
         L(TK_A, "Công ty 1 có 3 NV miễn chấm công, Công ty 2 có 2 NV miễn chấm công."),
         S("Đang ở Công ty 1, " + M_GEN + ", tab Danh sách miễn chấm công, đếm.", "Đổi sang Công ty 2, mở lại tab."), "—",
         B("Công ty 1 thấy đúng 3 NV, Tổng số bản ghi: 3.", "Công ty 2 thấy đúng 2 NV, Tổng số bản ghi: 2.")),
        (5, "Popup lịch sử miễn chấm công chỉ theo công ty đang chọn", "P0",
         L(TK_A, "Công ty 1 có 3 dòng lịch sử miễn chấm công, Công ty 2 có 1 dòng."),
         S("Ở Công ty 1 mở popup lịch sử tab Danh sách miễn chấm công, đếm.", "Đổi sang Công ty 2, mở lại."), "—",
         B("Công ty 1: 3 dòng; Công ty 2: 1 dòng; không lẫn nhân viên công ty khác.")),
        (6, "Xóa nhân viên miễn chấm công chỉ xóa ở công ty đang chọn", "P1",
         L(TK_A, "NV005 được thêm vào danh sách miễn chấm công ở Công ty 1."),
         S("Ở Công ty 2 mở tab Danh sách miễn chấm công.", "Tìm NV005."), "—",
         B("Công ty 2 không thấy NV005, không có thao tác xóa nhầm được NV005 của Công ty 1.")),
        (8, "Thêm nhân viên đã được miễn chấm công ở công ty khác", "P0",
         L(TK_A, "NV006 đang có trong danh sách miễn chấm công của Công ty 2, chưa có ở Công ty 1; tài khoản A làm việc ở cả 2 công ty."),
         S("Đang ở Công ty 1, " + M_GEN + ', tab Danh sách miễn chấm công, bấm "Thêm mới", chọn NV006.',
           "Mở popup lịch sử.", "Đổi sang Công ty 2, mở lại tab Danh sách miễn chấm công."), "Nhân viên: NV006",
         B('Công ty 1: hiện thông báo "Thêm nhân viên miễn chấm công thành công", bảng có NV006 (trước đây hệ thống bỏ qua im lặng).',
           'Popup lịch sử Công ty 1 có dòng "Thay đổi thông tin" (xanh dương), nhãn "Nhân viên thêm mới:" và dòng chữ xanh "- NV006 - ...".',
           "Công ty 2: NV006 vẫn còn, không bị đổi hay xoá.")),
        (9, "Thêm nhân viên đang thuộc danh sách CTV miễn chấm công", "P1",
         L(TK_A, "NV101 thuộc phòng HN_CTV (tick Nghiệp vụ), đang có ở tab Danh sách CTV miễn chấm công."),
         S(M_GEN + ', tab Danh sách miễn chấm công, bấm "Thêm mới", chọn NV101.'), "Nhân viên: NV101",
         B('Hiện thông báo lỗi (khung đỏ) "Nhân viên đã có trong danh sách CTV miễn chấm công (thuộc phòng ban Nghiệp vụ).".',
           "Bảng Danh sách miễn chấm công không thêm NV101; tab CTV vẫn giữ NV101.")),
        (10, "Danh sách CTV miễn chấm công đủ nhân viên của phòng Nghiệp vụ", "P0",
         L(TK_A + '; có thêm quyền "Quản lý danh mục phòng ban".',
           "Phòng HN_CTV (Công ty 1) có 3 nhân viên NV101, NV102, NV103; NV103 đang ở tab Danh sách miễn chấm công (thường)."),
         S('Sửa phòng HN_CTV, tick Cộng tác viên "Nghiệp vụ", lưu.', "Vào hồ sơ NV101, bấm Lưu 2 lần (không đổi gì).",
           M_GEN + ", xem tab Danh sách CTV miễn chấm công và tab Danh sách miễn chấm công."), "—",
         B("Tab CTV có đủ NV101, NV102, NV103, mỗi người đúng 1 dòng (lưu hồ sơ nhiều lần không nhân đôi).",
           "NV103 chuyển từ tab Danh sách miễn chấm công sang tab CTV.",
           "Nhân viên hiện ở tab CTV của đúng công ty của nhân viên, kể cả khi người sửa phòng ban đang làm việc ở công ty khác.")),
        (7, "Người không có quyền Thiết lập thông số không thấy nút Lịch sử và không lưu được", "P0",
         L(TK_B, "Có sẵn địa chỉ màn Quy định chung."),
         S("Đăng nhập tài khoản B.", "Mở phân hệ Chấm công, nhóm Cấu hình.", "Dán địa chỉ màn Quy định chung."), "—",
         B("Không có mục menu Quy định chung " + MENU_HIDDEN + ".", "Bị chuyển sang trang " + NOT_FOUND + ", không thấy nút Lịch sử, không đổi được thiết lập.")),
    ]

    sections = [
        ("I", "HIỂN THỊ TRANG & TRUY CẬP", sec1),
        ("II", "POPUP LỊCH SỬ TAB CHUNG: BỐ CỤC & BỘ LỌC", sec2),
        ("IV", "GHI LỊCH SỬ TỪNG TRƯỜNG - TAB CHUNG", f),
        ("V", "POPUP LỊCH SỬ DANH SÁCH MIỄN CHẤM CÔNG", sec5),
        ("VI", "POPUP LỊCH SỬ DANH SÁCH CTV MIỄN CHẤM CÔNG", sec6),
        ("VIII", "RÀNG BUỘC NHẬP LIỆU", sec8),
        ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", sec9),
        ("XI", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", sec11),
    ]
    return desc, roles, sections


# ======================================================================
# 2. QUY DINH LAM THEM
# ======================================================================
def quy_dinh_lam_them():
    title = "Thay đổi thông tin"
    actor = ACTOR_A
    tab = 'Ở tab "Chung".'

    desc = [
        ("1. Mục đích tính năng",
         "Ghi lại lịch sử thay đổi màn Quy định làm thêm: tab Chung (9 trường + 3 danh sách công ty / chức vụ) "
         "và tab Khung giờ làm thêm (lịch sử riêng từng khung giờ)."),
        ("2. Đối tượng được tính / hiển thị",
         "Tab Chung - 9 trường (nhãn trong popup): Căn cứ tính giờ làm thêm; Bật/tắt thời gian làm thêm tối thiểu; "
         "Thời gian làm thêm tối thiểu (phút); Bật/tắt thời gian làm thêm hưởng lương tối đa; "
         "Thời gian làm thêm hưởng lương tối đa (giờ/tháng); Bật/tắt giới hạn làm thêm liên tục; "
         "Làm tối đa (phút) phải nghỉ; Thời gian nghỉ tối thiểu (phút); Thời gian làm thêm bắt đầu tính sau ca (phút).\n"
         "Tab Chung - 3 danh sách (chung 1 popup), tên hành động đều là \"Thay đổi thông tin\" (xanh dương): danh sách công ty áp dụng hạn chế "
         "làm thêm hiện nhóm \"Công ty thêm mới:\" / \"Công ty đã xóa:\"; danh sách chức vụ không được làm thêm và danh sách chức vụ Khoán P3 kỹ thuật "
         "hiện nhóm theo ĐÚNG tên danh sách: \"Chức vụ không được làm thêm (<tên công ty>) thêm mới:\" / \"… đã xóa:\" và \"Chức vụ Khoán P3 kỹ thuật (<tên công ty>) thêm mới:\" / \"… đã xóa:\".\n"
         "Tab Khung giờ làm thêm - 6 trường: Loại; Giờ bắt đầu; Giờ kết thúc; Hệ số ngày thường; Hệ số ngày nghỉ; Hệ số ngày lễ. "
         "Thao tác: Thêm (tên hành động \"Tạo mới\" xanh lá, liệt kê đủ 6 trường chữ xanh), Sửa (\"Thay đổi thông tin\" xanh dương, chỉ trường đổi), Xóa (\"Xóa\" đỏ).\n"
         "Tiêu đề popup: \"Lịch sử thay đổi: Quy định làm thêm\"; popup khung giờ \"Lịch sử thay đổi: <giờ bắt đầu - giờ kết thúc> · <loại làm thêm>\" "
         "(vd \"Lịch sử thay đổi: 18:00 - 22:00 · Làm thêm hưởng lương\")."),
        ("3. Đối tượng bị ẩn / không tính",
         "- Không đổi gì: không sinh dòng.\n- Lưu khung giờ bị chặn (trống ô, chồng chéo): không sinh dòng.\n"
         "- Khung giờ đã xóa: dòng đã mất khỏi bảng nên KHÔNG mở được popup của khung giờ đó (lịch sử Xóa vẫn được lưu nhưng không xem được trên giao diện).\n"
         "- Popup tab Chung: lọc \"Tạo mới\" / \"Thay đổi trạng thái\" luôn rỗng (cả 9 trường lẫn 3 danh sách đều là thay đổi thông tin).\n"
         "- Popup khung giờ: dòng \"Xóa\" (đỏ) thuộc nhóm lọc \"Thay đổi trạng thái\" nhưng không xem được vì khung giờ đã mất khỏi bảng."),
        ("4. Bộ lọc thời gian áp dụng cho", FILTER_NOTE),
        ("5. Cấu trúc dữ liệu / cây phân cấp",
         "Popup tab Chung: dòng thời gian, mới nhất trên cùng; dòng 9 trường và dòng danh sách đều có tên hành động \"Thay đổi thông tin\" (xanh dương); "
         "dòng danh sách không có tiêu đề riêng theo loại danh sách (tên công ty của danh sách chức vụ nằm trong nhãn nhóm), bên dưới là nhóm "
         "\"... thêm mới:\" (mỗi mục 1 dòng chữ xanh) và / hoặc \"... đã xóa:\" (mỗi mục 1 dòng chữ đỏ).\n"
         "Popup khung giờ: tiêu đề \"Lịch sử thay đổi: <giờ> · <loại>\"; dòng \"Tạo mới\" xanh lá, \"Thay đổi thông tin\" xanh dương.\n" + GROUP_NOTE),
        ("6. Quy tắc cộng dồn / deduplicate",
         "Tab Chung TỰ LƯU khi đổi (radio / tick) hoặc khi rời ô số. Danh sách công ty / chức vụ TỰ LƯU ngay khi chọn / bỏ 1 mục. "
         "Bỏ 1 công ty đang có chức vụ cấm sinh 2 dòng: bỏ chức vụ (theo công ty đó) rồi bỏ công ty. "
         "Lịch sử 9 trường theo công ty đang chọn; lịch sử 3 danh sách là cấu hình dùng chung, công ty nào cũng thấy."),
        ("7. Phân quyền cấp",
         "- \"Thiết lập thông số\": thấy menu, thấy nút Lịch sử tab Chung và mục \"Lịch sử thay đổi\" trong menu bánh răng từng khung giờ; lưu được.\n"
         "- Không có quyền: không thấy menu, mở địa chỉ màn bị chuyển sang trang \"Không tìm thấy trang yêu cầu\".\n"
         "- Danh sách công ty chỉ thêm/bỏ được công ty trong phạm vi tài khoản được quản lý; công ty ngoài phạm vi đang áp dụng hiện kèm biểu tượng khoá, chỉ xem."),
        ("8. Cách tính các ô thống kê", "Không áp dụng - popup không có ô thống kê, không phân trang."),
        ("9. Ghi chú đọc bảng",
         COMMON_FORMAT_NOTE + "\n"
         "Thông báo đúng đối tượng và đúng thao tác: Thêm khung giờ báo \"Tạo khung giờ làm thêm thành công\", Sửa báo "
         "\"Cập nhật khung giờ làm thêm thành công\"; lưu tab Chung thất bại báo \"Cập nhật thất bại\" khung ĐỎ.\n"
         "Bẫy dễ sai: ô tick \"Sau ca làm việc\" bị khoá nhưng ô số phút bên cạnh vẫn sửa được."),
    ]

    roles = [
        ("01", "Có quyền thấy menu, nút Lịch sử tab Chung và mục Lịch sử của từng khung giờ", "P0", TK_A,
         S("Đăng nhập tài khoản A.", M_OT + ".", "Quan sát tab Chung.", 'Bấm tab "Khung giờ làm thêm", bấm bánh răng ở 1 dòng.'), "—",
         B('Tab Chung có nút "Lịch sử thay đổi" góc phải trên cùng.',
           'Menu bánh răng có 3 mục: "Sửa", "Xóa", "Lịch sử thay đổi".')),
        ("02", "Không có quyền không thấy menu, không vào được màn", "P0",
         L(TK_B, "Có sẵn địa chỉ màn Quy định làm thêm."),
         S("Đăng nhập tài khoản B.", 'Mở phân hệ Chấm công > nhóm "Cấu hình".', "Dán địa chỉ màn Quy định làm thêm."), "—",
         B('Không có mục "Quy định làm thêm" ' + MENU_HIDDEN + '.', "Bị chuyển sang trang " + NOT_FOUND + ".")),
        ("03", "Tài khoản chỉ quản lý 1 công ty chỉ thêm/bỏ được công ty đó", "P0",
         "Tài khoản E: có quyền, chỉ được quản lý Công ty 1. Danh sách hạn chế đang có Công ty 1 và ETEK GREEN (ngoài phạm vi E).",
         S("Đăng nhập tài khoản E.", M_OT + ".", 'Quan sát ô "Công ty" ở mục "Thiết lập chức vụ không được làm thêm".'), "—",
         B("ETEK GREEN hiện có biểu tượng khoá, không có dấu x để bỏ; ô chức vụ của ETEK GREEN bị khoá; không có ô \"Toàn công ty\" cho ETEK GREEN.",
           'Dưới ô có ghi chú xám "Công ty có biểu tượng khoá đang áp dụng nhưng ngoài phạm vi bạn quản lý — chỉ xem, không thêm/bỏ được."')),
    ]

    OPEN_OT = ["Đăng nhập tài khoản A.", M_OT + ".", 'Ở tab "Chung" bấm "Lịch sử thay đổi".']
    OPEN_KG = ["Đăng nhập tài khoản A.", M_OT + '.', 'Bấm tab "Khung giờ làm thêm".', "Bánh răng dòng 18:00 - 22:00 > Lịch sử thay đổi."]
    sec1 = [
        (1, "Popup khung giờ chỉ hiện lịch sử của khung giờ đã chọn", "P0",
         L(TK_A, "Khung giờ 18:00 - 22:00, Làm thêm hưởng lương đã có 1 lần Thêm, 1 lần Sửa; khung 05:00 - 06:00 có 1 lần Thêm."),
         S(*OPEN_KG), "—",
         B('Tiêu đề "Lịch sử thay đổi: 18:00 - 22:00 · Làm thêm hưởng lương".',
           "Chỉ hiện 2 dòng của khung giờ này, không lẫn khung giờ khác.")),
        popup_empty(2, "khung giờ", "Khung giờ tạo trước khi có tính năng lịch sử, chưa sửa lần nào.",
                    [M_OT + ', tab "Khung giờ làm thêm".', "Bánh răng dòng đó > Lịch sử thay đổi."], prio="P1"),
        (3, "Thứ tự mới nhất trên cùng ở popup khung giờ", "P1", "Khung giờ có Thêm lúc 08:00, Sửa lúc 09:00, Sửa lúc 10:00.",
         S(*OPEN_KG), "—", B("Thứ tự: Sửa 10:00, Sửa 09:00, Thêm 08:00; thời gian dạng dd/mm/yyyy HH:mm.")),
    ]

    sec2 = popup_std(
        1, "tab Chung", L(TK_A, "Đã có 2 lần đổi 9 trường và 1 lần thêm công ty."), OPEN_OT, "Quy định làm thêm",
        'Dòng đổi trường và dòng danh sách đều có tên hành động "Thay đổi thông tin" chữ xanh dương; dòng danh sách bên dưới là nhóm '
        '"Công ty thêm mới:" / "Chức vụ không được làm thêm (<tên công ty>) đã xóa:"... mỗi mục 1 dòng bắt đầu "- ".',
        L(TK_A, "Có 2 dòng đổi trường tab Chung và 2 dòng danh sách (1 thêm công ty, 1 bỏ chức vụ)."),
        ('"Thay đổi thông tin": hiện đủ 4 dòng - cả dòng đổi trường lẫn dòng thêm / bỏ phần tử danh sách.',
         '"Tạo mới" và "Thay đổi trạng thái": hiện ' + NO_MATCH))
    sec3 = popup_std(
        1, "khung giờ làm thêm", L(TK_A, "Khung giờ 18:00 - 22:00, Làm thêm hưởng lương đã có 1 lần Thêm, 2 lần Sửa."), OPEN_KG,
        "18:00 - 22:00 · Làm thêm hưởng lương",
        'Dòng thêm: tên hành động "Tạo mới" chữ xanh lá, chỉ liệt kê giá trị mới (không có mũi tên); dòng sửa: "Thay đổi thông tin" chữ xanh dương, chỉ trường đổi dạng cũ -> mới.',
        L(TK_A, "Khung giờ có 1 dòng thêm, 2 dòng sửa."),
        ('"Tạo mới": còn đúng 1 dòng "Tạo mới".',
         '"Thay đổi thông tin": còn đúng 2 dòng "Thay đổi thông tin".',
         '"Thay đổi trạng thái": hiện ' + NO_MATCH + " (dòng Xóa chỉ có khi khung giờ đã bị xóa, lúc đó không còn lối mở popup)."))

    f = []
    f.append(auto_tc(1, "P0", M_OT, tab, 'Ở "Căn cứ tính giờ làm thêm" chọn "Theo đơn đăng ký làm thêm".',
                     L("Trước: Theo cả đơn và thời gian chấm ra thực tế", "Sau: Theo đơn đăng ký làm thêm"),
                     "Căn cứ tính giờ làm thêm", "Theo cả đơn và thời gian chấm ra thực tế", "Theo đơn đăng ký làm thêm",
                     title, actor))
    f.append(auto_tc(2, "P0", M_OT, tab, 'Tick "Thời gian làm thêm tối thiểu".',
                     L("Trước: không tick", "Sau: tick"), "Bật/tắt thời gian làm thêm tối thiểu", "Không", "Có", title, actor))
    f.append(auto_tc(3, "P0", M_OT, tab, 'Sửa ô phút của "Thời gian làm thêm tối thiểu" từ 30 thành 60, bấm ra ngoài ô.',
                     L("Trước: 30", "Sau: 60"), "Thời gian làm thêm tối thiểu (phút)", "30", "60", title, actor,
                     pre_extra=("Ô tick Thời gian làm thêm tối thiểu đang tick.",)))
    f.append(auto_tc(4, "P0", M_OT, tab, 'Bỏ tick "Thời gian làm thêm hưởng lương tối đa".',
                     L("Trước: tick", "Sau: bỏ tick"), "Bật/tắt thời gian làm thêm hưởng lương tối đa", "Có", "Không", title, actor))
    f.append(auto_tc(5, "P0", M_OT, tab, 'Sửa ô giờ/tháng của "Thời gian làm thêm hưởng lương tối đa" từ 40 thành 1200, bấm ra ngoài ô.',
                     L("Trước: 40", "Sau: 1200"), "Thời gian làm thêm hưởng lương tối đa (giờ/tháng)", "40", "1,200", title, actor,
                     pre_extra=("Ô tick Thời gian làm thêm hưởng lương tối đa đang tick.",),
                     exp_extra=("Số có dấu phẩy ngăn nghìn: 1,200.",)))
    f.append(auto_tc(6, "P0", M_OT, tab, 'Tick ô "Làm tối đa ... phút phải nghỉ ít nhất ...".',
                     L("Trước: không tick", "Sau: tick"), "Bật/tắt giới hạn làm thêm liên tục", "Không", "Có", title, actor))
    f.append(auto_tc(7, "P0", M_OT, tab, 'Sửa ô thứ nhất "Làm tối đa ... phút" từ 240 thành 180, bấm ra ngoài ô.',
                     L("Trước: 240", "Sau: 180"), "Làm tối đa (phút) phải nghỉ", "240", "180", title, actor,
                     pre_extra=("Ô tick giới hạn làm thêm liên tục đang tick.",)))
    f.append(auto_tc(8, "P0", M_OT, tab, 'Sửa ô thứ hai "phải nghỉ ít nhất ..." từ 15 thành 30, bấm ra ngoài ô.',
                     L("Trước: 15", "Sau: 30"), "Thời gian nghỉ tối thiểu (phút)", "15", "30", title, actor,
                     pre_extra=("Ô tick giới hạn làm thêm liên tục đang tick.",)))
    f.append(auto_tc(9, "P0", M_OT, tab, 'Ở "Thời gian làm thêm bắt đầu tính từ", sửa ô "Sau ca làm việc ... phút" từ 0 thành 30, bấm ra ngoài ô.',
                     L("Trước: 0", "Sau: 30"), "Thời gian làm thêm bắt đầu tính sau ca (phút)", "0", "30", title, actor,
                     exp_extra=('Ô tick "Sau ca làm việc" luôn khoá, nhưng ô số phút vẫn sửa được.',
                                'Giá trị cũ là "0", KHÔNG hiện "(trống)".')))

    lst = [
        (1, "Thêm 1 công ty vào danh sách áp dụng hạn chế làm thêm", "P0",
         L(TK_A, "Danh sách công ty đang có Công ty 1."),
         S(M_OT + ".", 'Ở mục "* Thiết lập chức vụ không được làm thêm", ô "Công ty" chọn thêm Công ty 2.',
           'Chờ thông báo "Cập nhật danh sách công ty thành công".', 'Bấm "Lịch sử thay đổi".'),
         "Công ty thêm: Công ty 2",
         B('Dòng trên cùng có tên hành động "Thay đổi thông tin" (chữ xanh dương); nhãn nhóm "Công ty thêm mới:" KHÔNG kèm tên công ty trong ngoặc vì đây là cấu hình chung.',
           'Bên dưới nhãn "Công ty thêm mới:" và dòng chữ xanh "- Công ty 2" (tên công ty đầy đủ, không phải mã số).',
           'Dòng thuộc nhóm "Thay đổi thông tin".')),
        (2, "Bỏ 1 công ty có chức vụ cấm sinh 2 dòng", "P0",
         L(TK_A, "Công ty 2 đang trong danh sách, có 2 chức vụ cấm: Nhân viên hỗ trợ, Nhân viên nghiệp vụ."),
         S(M_OT + ".", "Bấm dấu x trên thẻ Công ty 2 ở ô Công ty.", "Mở popup lịch sử."), "Công ty bỏ: Công ty 2",
         B('2 dòng mới đều có tên hành động "Thay đổi thông tin" (chữ xanh dương).',
           'Dòng 1 (trên cùng): nhãn "Công ty đã xóa:" và dòng chữ đỏ "- Công ty 2".',
           'Dòng 2: nhãn "Chức vụ không được làm thêm (Công ty 2) đã xóa:" và 2 dòng chữ đỏ "- Nhân viên hỗ trợ", "- Nhân viên nghiệp vụ".',
           'Hiện 2 thông báo "Cập nhật hạn chế chức vụ thành công" và "Cập nhật danh sách công ty thành công".',
           'Tên chức vụ hiện ĐÚNG TÊN kể cả chức vụ thuộc công ty ngoài phạm vi tài khoản quản lý (KHÔNG hiện dạng "#662").')),
        (3, "Tick Tất cả công ty thêm nhiều công ty trong 1 dòng", "P1",
         L(TK_A, "Tài khoản quản lý 4 công ty, danh sách đang có 1 công ty."),
         S(M_OT + ".", 'Tick "Tất cả công ty".', "Mở popup lịch sử."), "—",
         B('1 dòng "Thay đổi thông tin": nhãn "Công ty thêm mới:" và 3 dòng chữ xanh, mỗi dòng 1 tên công ty.')),
        (4, "Thêm chức vụ không được làm thêm cho 1 công ty", "P0",
         L(TK_A, "Công ty 1 có trong danh sách, chưa có chức vụ cấm."),
         S(M_OT + ".", 'Ở khối "Công ty 1", ô "Chức vụ không được làm thêm" chọn "Trưởng phòng".',
           'Chờ "Cập nhật hạn chế chức vụ thành công".', "Mở popup lịch sử."), "Chức vụ: Trưởng phòng",
         B('Dòng trên cùng có tên hành động "Thay đổi thông tin" (chữ xanh dương).',
           'Bên dưới nhãn "Chức vụ không được làm thêm (Công ty 1) thêm mới:" và dòng chữ xanh "- Trưởng phòng".')),
        (5, "Bỏ chức vụ không được làm thêm", "P0", L(TK_A, "Công ty 1 đang cấm chức vụ Trưởng phòng."),
         S("Bấm dấu x trên thẻ Trưởng phòng.", "Mở popup lịch sử."), "—",
         B('Dòng trên cùng "Thay đổi thông tin" (xanh dương): nhãn "Chức vụ không được làm thêm (Công ty 1) đã xóa:" và dòng chữ đỏ "- Trưởng phòng".',
           'Dòng thuộc nhóm "Thay đổi thông tin" (bỏ phần tử danh sách, KHÔNG phải thay đổi trạng thái).')),
        (6, "Tick Toàn công ty ở chức vụ không được làm thêm", "P1", L(TK_A, "Công ty 1 có 12 chức vụ đang hoạt động, đang cấm 2."),
         S('Tick "Toàn công ty" ở khối Công ty 1.', "Mở popup."), "—",
         B('1 dòng "Thay đổi thông tin": nhãn "Chức vụ không được làm thêm (Công ty 1) thêm mới:" và đủ 10 dòng chữ xanh, mỗi dòng 1 tên chức vụ còn lại.')),
        (7, "Thêm chức vụ Khoán P3 kỹ thuật", "P0", L(TK_A, "Công ty 1 chưa có chức vụ Khoán P3."),
         S(M_OT + ".", 'Ở mục "* Thiết lập loại làm thêm Khoán P3 kỹ thuật theo chức vụ", ô "Chức vụ" chọn "Kỹ thuật viên".',
           'Chờ "Cập nhật thiết lập P3 kỹ thuật thành công".', "Mở popup."), "Chức vụ: Kỹ thuật viên",
         B('Dòng trên cùng có tên hành động "Thay đổi thông tin" (chữ xanh dương).',
           'Bên dưới nhãn "Chức vụ Khoán P3 kỹ thuật (Công ty 1) thêm mới:" (Công ty 1 = công ty đang chọn làm việc) và dòng chữ xanh "- Kỹ thuật viên".')),
        (8, "Bỏ chức vụ Khoán P3 kỹ thuật", "P0", L(TK_A, "Công ty 1 có Khoán P3: Kỹ thuật viên, Thợ điện."),
         S("Bấm dấu x trên Thợ điện.", "Mở popup."), "—",
         B('Dòng trên cùng "Thay đổi thông tin" (xanh dương): nhãn "Chức vụ Khoán P3 kỹ thuật (Công ty 1) đã xóa:" và dòng chữ đỏ "- Thợ điện".')),
        (9, "Chức vụ vừa bị cấm làm thêm tự rời khỏi danh sách Khoán P3 và có dòng lịch sử", "P1",
         L(TK_A, "Công ty 1: Kỹ thuật viên đang là Khoán P3, chưa bị cấm làm thêm."),
         S("Ở khối Công ty 1 (chức vụ không được làm thêm) chọn thêm Kỹ thuật viên.", "Quan sát ô Chức vụ Khoán P3.", "Mở popup lịch sử."), "—",
         B("Kỹ thuật viên biến mất khỏi ô Khoán P3 và khỏi danh sách lựa chọn P3.",
           'Popup có 2 dòng mới "Thay đổi thông tin" (xanh dương): 1 dòng nhóm "Chức vụ không được làm thêm (Công ty 1) thêm mới:" - Kỹ thuật viên và 1 dòng nhóm "Chức vụ Khoán P3 kỹ thuật (Công ty 1) đã xóa:" - Kỹ thuật viên.')),
        (10, "Chọn lại đúng danh sách cũ không sinh dòng", "P2", L(TK_A, "Công ty 1 cấm Trưởng phòng."),
         S('Bấm mở ô "Chức vụ không được làm thêm" của Công ty 1, không chọn gì, bấm ra ngoài.', "Mở popup."), "—",
         B("Mỗi lần lưu có thay đổi thật mới có dòng; mở ô chọn rồi đóng không chọn gì KHÔNG sinh dòng.")),
    ]

    kg = []
    kg.append((1, "Thêm khung giờ làm thêm ghi đủ 6 trường", "P0", TK_A,
               S(M_OT + ', tab "Khung giờ làm thêm", bấm "Thêm mới".',
                 'Popup "Thêm khung giờ làm thêm": Khung giờ 18:00 đến 22:00, Loại làm thêm "Làm thêm hưởng lương", Hệ số ngày thường 1.5, ngày nghỉ 2, ngày lễ 3.',
                 'Bấm "Lưu", chờ "Tạo khung giờ làm thêm thành công".', "Bánh răng dòng vừa thêm > Lịch sử thay đổi."),
               L("Khung giờ: 18:00 - 22:00", "Loại: Làm thêm hưởng lương", "Hệ số: 1.5 / 2 / 3"),
               B('Tiêu đề popup "Lịch sử thay đổi: 18:00 - 22:00 · Làm thêm hưởng lương".',
                 'Có 1 dòng tên hành động "Tạo mới" chữ xanh lá, thuộc nhóm lọc "Tạo mới".',
                 "Liệt kê đủ 6 trường, mỗi trường 1 dòng, chỉ có giá trị mới chữ xanh (không có mũi tên): Loại: Làm thêm hưởng lương; Giờ bắt đầu: 18:00; Giờ kết thúc: 22:00; "
                 "Hệ số ngày thường: 1.5; Hệ số ngày nghỉ: 2; Hệ số ngày lễ: 3.",
                 "Giờ dạng HH:mm, Loại hiện tên (không hiện số 1).")))
    kg_fields = [
        ("Loại", 'ô "Loại làm thêm" từ "Làm thêm hưởng lương" sang "Làm thêm nghỉ bù"', "Làm thêm hưởng lương", "Làm thêm nghỉ bù"),
        ("Giờ bắt đầu", "giờ bắt đầu từ 18:00 sang 17:30", "18:00", "17:30"),
        ("Giờ kết thúc", "giờ kết thúc từ 22:00 sang 23:00", "22:00", "23:00"),
        ("Hệ số ngày thường", "Hệ số ngày thường từ 1.5 sang 1.75", "1.5", "1.75"),
        ("Hệ số ngày nghỉ", "Hệ số ngày nghỉ từ 2 sang 2.5", "2", "2.5"),
        ("Hệ số ngày lễ", "Hệ số ngày lễ từ 3 sang 4", "3", "4"),
    ]
    for i, (lab, act, o, n) in enumerate(kg_fields, start=2):
        kg.append((i, 'Sửa khung giờ - ghi lịch sử trường "%s"' % lab, "P0",
                   L(TK_A, "Khung giờ 18:00 - 22:00, Làm thêm hưởng lương, hệ số 1.5 / 2 / 3; không có khung giờ khác cùng loại chồng lên giờ mới."),
                   S(M_OT + ', tab "Khung giờ làm thêm".', "Bánh răng dòng 18:00 - 22:00 > Sửa.",
                     'Popup "Cập nhật khung giờ làm thêm": đổi ' + act + ", các ô khác giữ nguyên.",
                     'Bấm "Lưu".', "Bánh răng dòng đó > Lịch sử thay đổi."),
                   L("Trường: " + lab, "Trước: " + o, "Sau: " + n),
                   B('Hiện thông báo "Cập nhật khung giờ làm thêm thành công" (khung xanh); popup đóng, bảng cập nhật giá trị mới.',
                     'Dòng trên cùng tên hành động "Thay đổi thông tin" chữ xanh dương, ' + ACTOR_A + '.',
                     "Dòng có ĐÚNG 1 thay đổi: " + chg(lab, o, n) + ".",
                     "KHÔNG báo chồng chéo với chính khung giờ đang sửa.")))
    kg.append((8, "Sửa khung giờ mà không đổi gì không sinh dòng", "P0", TK_A,
               S("Bánh răng dòng 18:00 - 22:00 > Sửa.", 'Không đổi gì, bấm "Lưu".', "Mở Lịch sử thay đổi của dòng."), "—",
               B('Popup sửa đóng, vẫn hiện thông báo "Cập nhật khung giờ làm thêm thành công".', "Không có dòng \"Thay đổi thông tin\" mới.")))
    kg.append((9, "Xóa khung giờ", "P1", L(TK_A, "Khung giờ 05:00 - 06:00 đã có lịch sử Thêm."),
               S("Bánh răng dòng 05:00 - 06:00 > Xóa.", 'Popup "Cảnh báo" bấm "Xoá".'), "—",
               B('Hiện "Xoá khung giờ làm thêm thành công", dòng biến mất khỏi bảng.',
                 "Lưu ý: vì dòng đã mất nên không còn mục Lịch sử thay đổi của khung giờ này để mở; ghi nhận Pending nếu nghiệp vụ yêu cầu xem được dòng Xóa (đặc tả gốc có dòng Xóa ID).")))

    sec8 = [
        (1, "Rời ô số tab Chung mà không đổi không sinh dòng", "P0", L(TK_A, "Thời gian làm thêm tối thiểu = 30."),
         S(M_OT + ".", "Bấm vào ô 30, không gõ, bấm ra ngoài; chọn lại radio Căn cứ đang chọn.", "Mở popup."), "—",
         B("Không có dòng mới.")),
        (2, "Xoá trống ô số tab Chung ghi đúng giá trị thật", "P0", L(TK_A, "Làm tối đa ... phút = 240, ô tick đang tick."),
         S("Xoá trống ô Làm tối đa, bấm ra ngoài.", "Tải lại trang, ghi nhận giá trị ô.", "Mở popup."), "Sau: để trống",
         B('Dòng mới "Làm tối đa (phút) phải nghỉ" | cũ "240" | mới = đúng giá trị ô hiển thị sau khi tải lại ("(trống)" nếu ô trống, "0" nếu ô hiện 0).')),
        (3, "Lưu khung giờ chồng chéo bị chặn, không sinh dòng", "P0",
         L(TK_A, "Đã có khung giờ 18:00 - 22:00, Làm thêm hưởng lương."),
         S('Tab Khung giờ làm thêm, "Thêm mới": 20:00 đến 23:00, cùng loại Làm thêm hưởng lương, hệ số 1.5/2/3.', 'Bấm "Lưu".'),
         "20:00 - 23:00, Làm thêm hưởng lương",
         B('Thông báo lỗi "Làm thêm hưởng lương này đã có khung giờ chồng chéo (18:00 - 22:00). Vui lòng chọn khung giờ khác hoặc thay đổi loại."',
           "Popup không đóng, không có dòng mới trong bảng, không sinh lịch sử.")),
        (4, "Sửa khung giờ để trống 1 ô bị chặn, không sinh dòng", "P1", TK_A,
         S("Bánh răng dòng 18:00 - 22:00 > Sửa.", "Xoá trống Hệ số ngày lễ, bấm Lưu.", "Huỷ, mở Lịch sử của dòng."), "Hệ số ngày lễ: để trống",
         B('Dưới ô Hệ số ngày lễ hiện chữ đỏ "Bắt buộc phải nhập"; thông báo lỗi (khung đỏ) "Cập nhật khung giờ làm thêm thất bại".',
           "Không có dòng \"Thay đổi thông tin\" mới.")),
    ]

    sec11 = [
        (1, "Công ty ngoài phạm vi quản lý (ETEK GREEN) không bị mất khi tài khoản khác lưu", "P0",
         "Danh sách hạn chế có Công ty 1 và ETEK GREEN. Tài khoản E chỉ quản lý Công ty 1.",
         S("Đăng nhập E, " + M_OT + ".", "Ở khối Công ty 1 chọn thêm 1 chức vụ cấm (thao tác này tự lưu).",
           "Bỏ Công ty 1 khỏi ô Công ty rồi chọn lại Công ty 1.", "Tài khoản A (quản lý cả ETEK GREEN) mở lại màn và popup lịch sử."), "—",
         B("ETEK GREEN vẫn còn trong danh sách công ty, các chức vụ cấm của ETEK GREEN giữ nguyên.",
           'Ở tài khoản E, ETEK GREEN hiện biểu tượng khoá, không bỏ được; popup lịch sử KHÔNG có nhóm "Công ty đã xóa:" chứa ETEK GREEN.')),
        (2, "Bỏ tick Tất cả công ty chỉ bỏ công ty trong phạm vi", "P0", "Như TC trên, tài khoản E đang tick Tất cả công ty.",
         S("Tài khoản E bỏ tick Tất cả công ty.", "Mở popup lịch sử."), "—",
         B("Chỉ còn ETEK GREEN (có khoá) trong ô Công ty.", 'Nhóm "Công ty đã xóa:" của dòng mới KHÔNG chứa ETEK GREEN.')),
        (3, "Sửa giờ / hệ số của khung giờ đã có không bị báo chồng chéo với chính nó", "P0",
         "Khung giờ 18:00 - 22:00 Làm thêm hưởng lương là khung duy nhất của loại này.",
         S("Sửa khung giờ đó: Hệ số ngày thường 1.5 thành 2, Lưu.", "Sửa tiếp giờ kết thúc 22:00 thành 21:30, Lưu."), "—",
         B("Cả 2 lần đều lưu thành công, không có thông báo chồng chéo.", "Popup khung giờ có 2 dòng \"Thay đổi thông tin\" tương ứng.")),
        (4, "Thêm khung giờ để trống báo lỗi dưới từng ô", "P0", TK_A,
         S('Tab Khung giờ làm thêm, "Thêm mới".', 'Không nhập gì, bấm "Lưu".'), "Tất cả ô trống",
         B('Dưới Giờ bắt đầu, Giờ kết thúc, Loại làm thêm, Hệ số ngày thường, Hệ số ngày nghỉ, Hệ số ngày lễ đều hiện chữ đỏ "Bắt buộc phải nhập".',
           'Thông báo "Tạo khung giờ làm thêm thất bại"; popup không đóng; KHÔNG bị lỗi hệ thống / treo.',
           "Nhập đủ lại 1 ô rồi Lưu: chữ đỏ của ô đó biến mất.")),
        (5, "Giá trị bật/tắt hiện Có/Không, số theo chuẩn quốc tế", "P1", TK_A,
         S("Đổi Bật/tắt thời gian làm thêm tối thiểu và sửa Thời gian làm thêm hưởng lương tối đa thành 1500.", "Mở popup."), "—",
         B('Giá trị hiện "Có"/"Không" và "1,500"; mũi tên giữa cũ và mới màu xám.')),
        (6, "Người không có quyền không thấy nút Lịch sử và không lưu được", "P0", L(TK_B, "Có địa chỉ màn Quy định làm thêm."),
         S("Đăng nhập B, dán địa chỉ màn."), "—", B("Bị chuyển sang trang " + NOT_FOUND + ".")),
        (8, "Mở Sửa khung giờ ngay sau khi mở Thêm mới: không hiện form trống, Lưu khoá khi đang tải", "P0",
         L(TK_A, "Có khung giờ 05:00 - 06:00, Làm thêm nghỉ bù, hệ số 1.5 / 2 / 3."),
         S(M_OT + ', tab "Khung giờ làm thêm".', 'Bấm "Thêm mới", bấm "Huỷ".', "Ngay lập tức bánh răng dòng 05:00 - 06:00 > Sửa, quan sát nút Lưu và các ô.",
           "Chờ form hiện đủ dữ liệu, đổi Hệ số ngày lễ 3 thành 4, bấm Lưu."), "Hệ số ngày lễ: 4",
         B('Trong lúc đang tải dữ liệu, nút "Lưu" bị khoá (mờ, bấm không được); form KHÔNG hiện dữ liệu của lần mở trước.',
           'Tải xong form hiện đúng 05:00, 06:00, Làm thêm nghỉ bù, 1.50 / 2.00 / 3.00.',
           'Lưu báo "Cập nhật khung giờ làm thêm thành công"; lịch sử có đúng 1 dòng: ' + chg("Hệ số ngày lễ", "3", "4") + '.',
           'KHÔNG bị báo "đã có khung giờ chồng chéo" với chính khung giờ đang sửa, KHÔNG báo "Cập nhật khung giờ làm thêm thất bại".')),
        (7, "Lưu tab Chung thất bại báo lỗi khung đỏ, không sinh dòng", "P2", TK_A,
         S(M_OT + ", tab Chung.", "Ngắt mạng máy đang test (hoặc để hết phiên đăng nhập).", 'Tick/bỏ tick "Bật/tắt thời gian làm thêm tối thiểu".',
           "Bật lại mạng, tải lại trang, mở popup lịch sử."), "—",
         B('Hiện thông báo "Cập nhật thất bại" khung ĐỎ (không phải khung xanh).', "Tải lại trang ô tick giữ giá trị cũ; popup KHÔNG có dòng mới.")),
    ]

    sections = [
        ("I", "HIỂN THỊ TRANG & TRUY CẬP", sec1),
        ("II", "POPUP LỊCH SỬ TAB CHUNG: BỐ CỤC & BỘ LỌC", sec2),
        ("III", "POPUP LỊCH SỬ KHUNG GIỜ LÀM THÊM: BỐ CỤC & BỘ LỌC", sec3),
        ("IV", "GHI LỊCH SỬ TỪNG TRƯỜNG - TAB CHUNG", f),
        ("V", "LỊCH SỬ 3 DANH SÁCH: CÔNG TY / CHỨC VỤ KHÔNG ĐƯỢC LÀM THÊM / KHOÁN P3", lst),
        ("VI", "LỊCH SỬ TAB KHUNG GIỜ LÀM THÊM (THÊM / SỬA TỪNG TRƯỜNG / XÓA)", kg),
        ("VIII", "RÀNG BUỘC NHẬP LIỆU", sec8),
        ("XI", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", sec11),
    ]
    return desc, roles, sections


# ======================================================================
# 3. QUY DINH NGHI
# ======================================================================
def quy_dinh_nghi():
    title = "Thay đổi thông tin"
    actor = ACTOR_A
    tab = 'Ở tab "Chung".'

    desc = [
        ("1. Mục đích tính năng",
         "Ghi lại lịch sử thay đổi màn Quy định nghỉ: tab Chung (26 trường), tab Loại nghỉ, tab Nghỉ lễ, tab Nghỉ cắt phép "
         "(3 tab sau có lịch sử RIÊNG từng dòng, mở từ menu bánh răng)."),
        ("2. Đối tượng được tính / hiển thị",
         "Tab Chung - 26 trường theo 9 nhóm: Tính phép cho thời gian thử việc (bật/tắt, điều kiện, tiếp nhận trước ngày); "
         "Tính phép cho tháng nghỉ việc (3); Tính phép thời gian nghỉ thai sản (bật/tắt, điều kiện, số ngày công tối thiểu); "
         "Nghỉ không lương (3); Cho phép ứng phép (3); Đơn nghỉ phép phải gửi trước (2); Tăng phép theo thâm niên (4); "
         "Chuyển ngày phép sang năm mới (3); Giới hạn thời gian sử dụng (2).\n"
         "Loại nghỉ - 9 trường: Tên; Ký hiệu; Nhóm; Tỉ lệ hưởng lương (%); Có tính ngày lễ/cuối tuần; Cần NSHC duyệt; "
         "Số ngày nghỉ tối đa; Ghi chú; Trạng thái. Thao tác: Thêm, Sửa, Khóa, Mở khóa, Xóa.\n"
         "Nghỉ lễ - 6 trường: Tên ngày nghỉ; Ký hiệu; Ngày; Tỉ lệ hưởng lương (%); Ngày nghỉ bù; Ghi chú. Thao tác: Thêm, Sửa, Xóa.\n"
         "Nghỉ cắt phép - 5 trường + danh sách: Tên ngày nghỉ cắt phép; Ký hiệu; Ngày; Số phép; Ghi chú; Nhân viên đi làm "
         "(chỉ hiện nhân viên được thêm / bỏ, theo nhóm \"Nhân viên đi làm thêm mới:\" / \"Nhân viên đi làm đã xóa:\").\n"
         "Tiêu đề popup: \"Lịch sử thay đổi: Quy định nghỉ\" (tab Chung); \"Lịch sử thay đổi: <Ký hiệu> - <Tên loại nghỉ>\" (vd \"NO - Nghỉ ốm\"); "
         "\"Lịch sử thay đổi: <Tên ngày nghỉ lễ>\"; \"Lịch sử thay đổi: <Tên ngày nghỉ cắt phép>\"."),
        ("3. Đối tượng bị ẩn / không tính",
         "- Lưu không đổi: không sinh dòng.\n- Lưu bị chặn (thiếu Tên, Ký hiệu, Ngày...): không sinh dòng.\n"
         "- Dòng đã Xóa không còn trên bảng nên không mở được popup của nó (lịch sử Xóa vẫn được lưu).\n"
         "- Nút \"Cập nhật dữ liệu\" và \"Import Excel\" trên đầu màn KHÔNG sinh lịch sử (đặc tả gốc có yêu cầu - chưa làm).\n"
         "- Lịch sử của công ty khác không hiện.\n"
         "- Popup tab Chung: lọc \"Tạo mới\" / \"Thay đổi trạng thái\" luôn rỗng. Popup Nghỉ lễ / Nghỉ cắt phép: \"Thay đổi trạng thái\" rỗng (chỉ có Xóa, mà dòng đã xóa không mở được popup)."),
        ("4. Bộ lọc thời gian áp dụng cho", FILTER_NOTE),
        ("5. Cấu trúc dữ liệu / cây phân cấp",
         "Popup dòng thời gian, mới nhất trên cùng. Dòng thêm: tên hành động \"Tạo mới\" chữ xanh lá, liệt kê các trường có giá trị, chỉ giá trị mới chữ xanh (không mũi tên). "
         "Dòng sửa: \"Thay đổi thông tin\" chữ xanh dương, chỉ trường đổi dạng cũ -> mới. Dòng khóa: \"Khóa\" chữ cam; mở khóa: \"Mở khóa\" chữ xanh lá; "
         "xóa: \"Xóa\" chữ đỏ. "
         "Tên bản ghi nằm ngay trong tiêu đề popup (không còn dòng mô tả dưới tiêu đề).\n" + GROUP_NOTE),
        ("6. Quy tắc cộng dồn / deduplicate",
         "Tab Chung TỰ LƯU khi đổi (tick, radio) hoặc khi rời ô số. Tab Loại nghỉ / Nghỉ lễ / Nghỉ cắt phép lưu bằng nút \"Lưu\" "
         "trong popup; 1 lần Lưu = 1 dòng gồm mọi trường đổi. Nhân viên đi làm so theo danh sách: chỉ hiện người thêm/bỏ."),
        ("7. Phân quyền cấp",
         "- \"Thiết lập thông số\": thấy menu Quy định nghỉ, nút Lịch sử tab Chung, mục \"Lịch sử thay đổi\" trong bánh răng 3 tab; lưu / khoá / xoá được.\n"
         "- Không có quyền: không thấy menu; mở địa chỉ màn bị chuyển sang trang \"Không tìm thấy trang yêu cầu\"."),
        ("8. Cách tính các ô thống kê", "Không áp dụng - popup không có ô thống kê, không phân trang."),
        ("9. Ghi chú đọc bảng",
         COMMON_FORMAT_NOTE + "\n"
         "Popup Loại nghỉ / Nghỉ lễ / Nghỉ cắt phép: tiêu đề \"Thêm ...\" khi Thêm mới, \"Cập nhật ...\" khi Sửa; thông báo ghi đúng đối tượng "
         "và đúng thao tác (vd \"Tạo ngày nghỉ lễ thành công\" / \"Cập nhật ngày nghỉ lễ thành công\"); lưu tab Chung thất bại báo \"Cập nhật thất bại\" khung ĐỎ.\n"
         "Bẫy dễ sai: (1) chữ lựa chọn trong popup lịch sử tab Chung ĐÚNG như chữ trên màn, bỏ dấu hai chấm cuối, ô số nằm "
         "trong lựa chọn ghi \"...\" (vd trên màn \"Tối đa [ô số] ngày\", trong lịch sử \"Tối đa ... ngày\"); (2) Loại nghỉ hệ thống: ô Tên loại nghỉ và Nhóm bị khoá khi Sửa; "
         "(3) ô Số ngày công tối thiểu (thai sản) bị khoá khi đang bằng 0 hoặc trống."),
    ]

    roles = [
        ("01", "Có quyền thấy menu, nút Lịch sử tab Chung và mục Lịch sử ở 3 tab", "P0", TK_A,
         S("Đăng nhập A.", M_HOL + ".", "Quan sát tab Chung.", "Lần lượt vào tab Loại nghỉ, Nghỉ lễ, Nghỉ cắt phép, bấm bánh răng 1 dòng."), "—",
         B('Tab Chung có nút "Lịch sử thay đổi" góc phải trên cùng.', 'Bánh răng 3 tab đều có mục "Lịch sử thay đổi" ở cuối.')),
        ("02", "Không có quyền không vào được màn", "P0", L(TK_B, "Có địa chỉ màn Quy định nghỉ."),
         S("Đăng nhập B.", 'Mở nhóm "Cấu hình" phân hệ Chấm công.', "Dán địa chỉ màn."), "—",
         B('Không có mục "Quy định nghỉ" ' + MENU_HIDDEN + '.', "Bị chuyển sang trang " + NOT_FOUND + ".")),
        ("03", "Đăng nhập lại sau khi bị gỡ quyền thì mất lối vào", "P1", TK_A,
         S('Gỡ quyền "Thiết lập thông số" khỏi A.', "A đăng nhập lại, mở màn."), "—", B("Bị chuyển sang trang " + NOT_FOUND + ".")),
    ]

    OPEN_AW = ["Đăng nhập tài khoản A.", M_HOL + ".", 'Ở tab "Chung" bấm "Lịch sử thay đổi".']
    OPEN_LT = ["Đăng nhập tài khoản A.", M_HOL + ".", 'Tab "Loại nghỉ", bánh răng dòng Nghỉ ốm > Lịch sử thay đổi.']
    OPEN_HL = ["Đăng nhập tài khoản A.", M_HOL + ".", 'Tab "Nghỉ lễ", bánh răng dòng Quốc khánh > Lịch sử thay đổi.']
    OPEN_TL = ["Đăng nhập tài khoản A.", M_HOL + ".", 'Tab "Nghỉ cắt phép", bánh răng dòng Nghỉ Tết công ty > Lịch sử thay đổi.']
    sec1 = [
        (1, "Popup loại nghỉ chỉ hiện lịch sử đúng loại nghỉ đã chọn", "P0", "Loại nghỉ Nghỉ ốm (ký hiệu NO) có 3 dòng lịch sử, Nghỉ cưới có 1 dòng.",
         S(*OPEN_LT), "—",
         B('Tiêu đề "Lịch sử thay đổi: NO - Nghỉ ốm".', "Chỉ có 3 dòng của Nghỉ ốm, không lẫn Nghỉ cưới.")),
        (2, "Popup ngày nghỉ lễ chỉ hiện lịch sử đúng ngày nghỉ đã chọn", "P0", "Ngày nghỉ Quốc khánh (QK) có 2 dòng lịch sử.",
         S(*OPEN_HL), "—", B('Tiêu đề "Lịch sử thay đổi: Quốc khánh".', "Chỉ có 2 dòng của Quốc khánh.")),
        (3, "Popup ngày nghỉ cắt phép chỉ hiện lịch sử đúng ngày đã chọn", "P0", "Ngày nghỉ cắt phép Nghỉ Tết công ty (NTC) có 1 dòng.",
         S(*OPEN_TL), "—", B('Tiêu đề "Lịch sử thay đổi: Nghỉ Tết công ty".', "Chỉ có 1 dòng của ngày này.")),
        popup_empty(4, "loại nghỉ", "Loại nghỉ tạo trước khi có tính năng, chưa sửa.",
                    [M_HOL + '.', 'Tab "Loại nghỉ", mở Lịch sử thay đổi của loại nghỉ đó.']),
    ]

    sec2 = popup_std(
        1, "tab Chung", L(TK_A, "Công ty 1 có 2 lần đổi tab Chung."), OPEN_AW, "Quy định nghỉ",
        'Mỗi dòng tên hành động "Thay đổi thông tin" chữ xanh dương, bên dưới từng trường đổi dạng cũ -> mới.',
        L(TK_A, "Công ty 1 có 3 dòng lịch sử đổi thiết lập tab Chung."),
        ('"Thay đổi thông tin": hiện đủ 3 dòng.', '"Tạo mới" và "Thay đổi trạng thái": hiện ' + NO_MATCH))
    sec2 += renum(popup_std(
        1, "loại nghỉ", L(TK_A, "Loại nghỉ Nghỉ ốm (NO) có 4 dòng: Thêm, Cập nhật, Khóa, Mở khóa."), OPEN_LT, "NO - Nghỉ ốm",
        'Dòng thêm "Tạo mới" xanh lá; dòng sửa "Thay đổi thông tin" xanh dương; dòng khóa "Khóa" cam; dòng mở khóa "Mở khóa" xanh lá.',
        L(TK_A, "Loại nghỉ Nghỉ ốm (NO) có 1 dòng thêm, 1 dòng sửa, 1 dòng khóa, 1 dòng mở khóa."),
        ('"Tạo mới": còn đúng dòng "Tạo mới".', '"Thay đổi thông tin": còn đúng dòng "Thay đổi thông tin".',
         '"Thay đổi trạng thái": còn đúng 2 dòng "Mở khóa" và "Khóa" (khóa / mở khóa là thay đổi trạng thái).')), 7)
    sec2 += renum(popup_std(
        1, "ngày nghỉ lễ", L(TK_A, "Ngày nghỉ Quốc khánh (QK) có 1 dòng thêm, 2 dòng sửa."), OPEN_HL, "Quốc khánh",
        'Dòng thêm "Tạo mới" xanh lá; dòng sửa "Thay đổi thông tin" xanh dương.',
        L(TK_A, "Quốc khánh có 1 dòng thêm, 2 dòng sửa."),
        ('"Tạo mới": còn đúng dòng "Tạo mới".', '"Thay đổi thông tin": còn đúng 2 dòng "Thay đổi thông tin".',
         '"Thay đổi trạng thái": hiện ' + NO_MATCH), layout_prio="P1"), 13)
    sec2 += renum(popup_std(
        1, "ngày nghỉ cắt phép", L(TK_A, "Nghỉ Tết công ty (NTC) có 1 dòng thêm, 1 dòng sửa."), OPEN_TL, "Nghỉ Tết công ty",
        'Dòng thêm "Tạo mới" xanh lá; dòng sửa "Thay đổi thông tin" xanh dương; danh sách Nhân viên đi làm hiện theo nhóm "Nhân viên đi làm thêm mới:" / "Nhân viên đi làm đã xóa:".',
        L(TK_A, "Nghỉ Tết công ty có 1 dòng thêm, 1 dòng sửa."),
        ('"Tạo mới": còn đúng dòng "Tạo mới".', '"Thay đổi thông tin": còn đúng dòng "Thay đổi thông tin".',
         '"Thay đổi trạng thái": hiện ' + NO_MATCH), layout_prio="P1"), 19)

    # ---- 26 truong tab Chung
    TC = [
        ("Bật/tắt tính phép cho thời gian thử việc", 'Tick "Tính phép cho thời gian thử việc".', "Không", "Có", "không tick", "tick", ()),
        ("Điều kiện tính phép tháng đầu (thử việc)", 'Ở "Tháng đầu tiên được tính phép nếu:" chọn "Tiếp nhận trước ngày".',
         "Tiếp nhận ngày bất kỳ trong tháng", "Tiếp nhận trước ngày", "Tiếp nhận ngày bất kỳ trong tháng", "Tiếp nhận trước ngày",
         ("Tính phép cho thời gian thử việc đang tick.",)),
        ("Tiếp nhận trước ngày (thử việc)", 'Sửa ô số cạnh "Tiếp nhận trước ngày" (thử việc) từ 31 thành 15, bấm ra ngoài ô.', "31", "15", "31", "15",
         ("Tính phép cho thời gian thử việc đang tick.",)),
        ("Bật/tắt tính phép cho tháng nghỉ việc", 'Tick "Tính phép cho tháng nghỉ việc".', "Không", "Có", "không tick", "tick", ()),
        ("Điều kiện tính phép tháng nghỉ việc", 'Ở "Tháng nghỉ được tính phép nếu:" chọn "Tiếp nhận trước ngày".',
         "Tiếp nhận ngày bất kỳ trong tháng", "Tiếp nhận trước ngày", "Tiếp nhận ngày bất kỳ trong tháng", "Tiếp nhận trước ngày",
         ("Tính phép cho tháng nghỉ việc đang tick.",)),
        ("Tiếp nhận trước ngày (nghỉ việc)", 'Sửa ô số cạnh "Tiếp nhận trước ngày" (tháng nghỉ việc) từ 1 thành 10, bấm ra ngoài ô.', "1", "10", "1", "10",
         ("Tính phép cho tháng nghỉ việc đang tick.",)),
        ("Bật/tắt tính phép thời gian nghỉ thai sản", 'Tick "Tính phép cho thời gian nghỉ thai sản".', "Không", "Có", "không tick", "tick", ()),
        ("Điều kiện tính phép thai sản", 'Chọn "Chỉ tính phép cho tháng đầu và tháng cuối kỳ nghỉ:".',
         "Tất cả thời gian nghỉ đều được tính phép", "Chỉ tính phép cho tháng đầu và tháng cuối kỳ nghỉ",
         "Tất cả thời gian nghỉ đều được tính phép", "Chỉ tính phép cho tháng đầu và tháng cuối kỳ nghỉ", ("Tính phép thai sản đang tick.",)),
        ("Số ngày công tối thiểu (thai sản)", 'Sửa ô "Chỉ tính phép cho tháng có số ngày công lớn hơn hoặc bằng ... ngày" (khối thai sản) từ 1 thành 12, bấm ra ngoài ô.',
         "1", "12", "1", "12", ("Tính phép thai sản đang tick, ô số đang = 1 (khác 0, ô mở khoá).",)),
        ("Bật/tắt tính phép thời gian nghỉ không lương", 'Tick "Tính phép cho thời gian nghỉ không lương".', "Không", "Có", "không tick", "tick", ()),
        ("Điều kiện tính phép nghỉ không lương", 'Chọn "Chỉ tính phép cho tháng có:".',
         "Tất cả thời gian nghỉ đều được tính phép", "Chỉ tính phép cho tháng có",
         "Tất cả thời gian nghỉ đều được tính phép", "Chỉ tính phép cho tháng có:", ("Tính phép nghỉ không lương đang tick.",)),
        ("Số ngày công tối thiểu (nghỉ không lương)", 'Sửa ô số ngày công của khối nghỉ không lương từ 1 thành 14, bấm ra ngoài ô.',
         "1", "14", "1", "14", ("Tính phép nghỉ không lương đang tick.",)),
        ("Bật/tắt cho phép ứng phép", 'Tick "Cho phép ứng phép (...)".', "Không", "Có", "không tick", "tick", ()),
        ("Điều kiện ứng phép", 'Chọn "Tối đa ... ngày" ở khối ứng phép.', "Không giới hạn ngày phép được ứng", "Tối đa ... ngày",
         "Không giới hạn ngày phép được ứng", "Tối đa ... ngày", ("Cho phép ứng phép đang tick.",)),
        ("Số ngày ứng phép tối đa", 'Sửa ô "Tối đa ... ngày" khối ứng phép từ 1 thành 3, bấm ra ngoài ô.', "1", "3", "1", "3", ("Cho phép ứng phép đang tick.",)),
        ("Bật/tắt đơn nghỉ phép phải gửi trước", 'Tick "Đơn xin nghỉ phép phải được gửi trước ... giờ".', "Không", "Có", "không tick", "tick", ()),
        ("Số giờ phải gửi đơn trước", 'Sửa ô giờ của "Đơn xin nghỉ phép phải được gửi trước" từ 24 thành 48, bấm ra ngoài ô.', "24", "48", "24", "48",
         ("Ô tick Đơn xin nghỉ phép phải được gửi trước đang tick.",)),
        ("Bật/tắt tăng phép theo thâm niên", 'Bỏ tick "Tăng phép theo thâm niên".', "Có", "Không", "tick", "bỏ tick", ()),
        ("Cách tăng phép theo thâm niên", 'Chọn "Tuỳ chọn" ở khối Tăng phép theo thâm niên.', "Theo Luật lao động: 5 năm tăng 1 ngày phép", "Tuỳ chọn",
         "Theo Luật lao động: 5 năm tăng 1 ngày phép", "Tuỳ chọn", ("Tăng phép theo thâm niên đang tick.",)),
        ("Số năm được tăng phép", 'Sửa ô "... năm được tăng" từ 1 thành 2, bấm ra ngoài ô.', "1", "2", "1", "2", ("Tăng phép theo thâm niên đang tick.",)),
        ("Số ngày phép được tăng", 'Sửa ô "được tăng ... ngày" từ 1 thành 2, bấm ra ngoài ô.', "1", "2", "1", "2", ("Tăng phép theo thâm niên đang tick.",)),
        ("Bật/tắt chuyển ngày phép sang năm mới", 'Bỏ tick "Chuyển ngày phép chưa dùng từ năm cũ sang năm mới".', "Có", "Không", "tick", "bỏ tick", ()),
        ("Cách chuyển ngày phép", 'Chọn "Tối đa ... ngày" ở khối chuyển ngày phép.', "Chuyển tất cả ngày phép", "Tối đa ... ngày",
         "Chuyển tất cả ngày phép", "Tối đa ... ngày", ("Chuyển ngày phép đang tick.",)),
        ("Số ngày phép chuyển tối đa", 'Sửa ô "Tối đa ... ngày" khối chuyển ngày phép từ 1 thành 5, bấm ra ngoài ô.', "1", "5", "1", "5", ("Chuyển ngày phép đang tick.",)),
        ("Bật/tắt giới hạn thời gian sử dụng", 'Tick "Thời gian sử dụng ... tháng".', "Không", "Có", "không tick", "tick", ()),
        ("Thời gian sử dụng (tháng)", 'Sửa ô "Thời gian sử dụng ... tháng" từ 3 thành 12, bấm ra ngoài ô.', "3", "12", "3", "12",
         ("Ô tick Thời gian sử dụng đang tick.",)),
    ]
    f = []
    for i, (lab, act, o, n, ui_o, ui_n, pre) in enumerate(TC, start=1):
        extra = ()
        if not o.isdigit() and o not in ("Có", "Không"):
            extra = ("Giá trị hiện TÊN phương án ĐÚNG chữ trên màn (không phải chữ rút gọn khác), không hiện số 1 / 2.",)
        if o in ("Có", "Không"):
            extra = ("Hiện Có / Không (không phải Bật / Tắt).",)
        f.append(auto_tc(i, "P0", M_HOL, tab, act, L("Trước: " + ui_o, "Sau: " + ui_n), lab, o, n, title, actor,
                         pre_extra=pre, exp_extra=extra))

    # ---- Loai nghi
    lt_title_upd = "Thay đổi thông tin"
    LT_PRE = L(TK_A, 'Loại nghỉ "Nghỉ ốm" (ký hiệu NO) do công ty tự thêm (xoá được), Nhóm: Nghỉ hưởng BHXH, Tỉ lệ 75, '
                     "không tick Có tính ngày lễ/cuối tuần, tick Cần NSHC duyệt, Số ngày nghỉ tối đa 30, Ghi chú \"Theo BHXH\", Hoạt động.")
    lt = []
    lt.append((1, "Thêm loại nghỉ ghi đủ 9 trường", "P0", TK_A,
               S(M_HOL + ', tab "Loại nghỉ", bấm "Thêm mới".',
                 'Nhập Tên loại nghỉ "Nghỉ chăm con", Ký hiệu "NCC", Nhóm "Nghỉ chế độ hưởng lương", Tỉ lệ hưởng lương 100, tick Có tính ngày lễ/cuối tuần, không tick Cần NSHC duyệt, Số ngày nghỉ tối đa 5, Ghi chú "Con dưới 3 tuổi".',
                 'Bấm "Lưu", chờ "Tạo loại nghỉ thành công".', "Bánh răng dòng Nghỉ chăm con > Lịch sử thay đổi."),
               L("Tên: Nghỉ chăm con", "Ký hiệu: NCC", "Nhóm: Nghỉ chế độ hưởng lương", "Tỉ lệ: 100", "Số ngày tối đa: 5"),
               B('Tiêu đề popup "Lịch sử thay đổi: NCC - Nghỉ chăm con"; 1 dòng tên hành động "Tạo mới" chữ xanh lá, thuộc nhóm lọc "Tạo mới".',
                 'Liệt kê 9 trường, mỗi trường 1 dòng, chỉ giá trị mới chữ xanh (không có mũi tên): Tên: Nghỉ chăm con; Ký hiệu: NCC; Nhóm: Nghỉ chế độ hưởng lương; Tỉ lệ hưởng lương (%): 100; '
                 'Có tính ngày lễ/cuối tuần: Có; Cần NSHC duyệt: Không; Số ngày nghỉ tối đa: 5; Ghi chú: Con dưới 3 tuổi; Trạng thái: Hoạt động.')))
    lt_fields = [
        ("Tên", 'ô "Tên loại nghỉ" từ "Nghỉ ốm" thành "Nghỉ ốm đau"', "Nghỉ ốm", "Nghỉ ốm đau"),
        ("Ký hiệu", 'ô "Ký hiệu" từ "NO" thành "NOD"', "NO", "NOD"),
        ("Nhóm", 'ô "Nhóm" từ "Nghỉ hưởng BHXH" sang "Nghỉ không lương"', "Nghỉ hưởng BHXH", "Nghỉ không lương"),
        ("Tỉ lệ hưởng lương (%)", 'ô "Tỉ lệ hưởng lương (%)" từ 75 thành 62.5', "75", "62.5"),
        ("Có tính ngày lễ/cuối tuần", 'tick ô "Có tính ngày lễ/cuối tuần"', "Không", "Có"),
        ("Cần NSHC duyệt", 'bỏ tick ô "Cần NSHC duyệt"', "Có", "Không"),
        ("Số ngày nghỉ tối đa", 'ô "Số ngày nghỉ tối đa" từ 30 thành 1000', "30", "1,000"),
        ("Ghi chú", 'ô "Ghi chú" từ "Theo BHXH" thành "Theo luật BHXH 2024"', "Theo BHXH", "Theo luật BHXH 2024"),
    ]
    for i, (lab, act, o, n) in enumerate(lt_fields, start=2):
        lt.append((i, 'Sửa loại nghỉ - ghi lịch sử trường "%s"' % lab, "P0", LT_PRE,
                   S(M_HOL + ', tab "Loại nghỉ".', "Bánh răng dòng Nghỉ ốm > Sửa.", "Đổi " + act + ", các ô khác giữ nguyên.",
                     'Bấm "Lưu".', "Bánh răng dòng đó > Lịch sử thay đổi."),
                   L("Trường: " + lab, "Trước: " + o.replace(",", ""), "Sau: " + n.replace(",", "")),
                   B('Popup tiêu đề "Cập nhật loại nghỉ"; sau khi lưu hiện thông báo "Cập nhật loại nghỉ thành công".',
                     'Dòng trên cùng tên hành động "%s" chữ xanh dương, %s.' % (lt_title_upd, ACTOR_A),
                     "Có ĐÚNG 1 thay đổi: " + chg(lab, o, n) + ".", "Không kèm Trạng thái hay trường khác.")))
    lt.append((10, 'Khóa loại nghỉ - ghi lịch sử trường "Trạng thái"', "P0", LT_PRE,
               S('Bánh răng dòng Nghỉ ốm > "Khóa".', 'Popup "Xác nhận khóa" bấm "Đồng ý", chờ "Khóa thành công".', "Mở Lịch sử thay đổi."), "—",
               B('Dòng trên cùng tên hành động "Khóa" chữ cam, thuộc nhóm lọc "Thay đổi trạng thái".', "Có ĐÚNG 1 thay đổi: " + chg("Trạng thái", "Hoạt động", "Khóa") + ".",
                 'Popup "Xác nhận khóa" hỏi "Bạn có chắc chắn muốn khóa bản ghi này không?".',
                 'Cột Trạng thái trên bảng chuyển sang "Khoá"; bánh răng đổi "Khóa" thành "Mở khóa".')))
    lt.append((11, "Mở khóa loại nghỉ", "P0", "Nghỉ ốm đang Khóa.",
               S('Bánh răng > "Mở khóa".', 'Popup "Xác nhận mở khóa" bấm "Đồng ý", chờ "Mở khóa thành công".', "Mở Lịch sử thay đổi."), "—",
               B('Dòng trên cùng tên hành động "Mở khóa" chữ xanh lá, thuộc nhóm lọc "Thay đổi trạng thái".', "Có ĐÚNG 1 thay đổi: " + chg("Trạng thái", "Khóa", "Hoạt động") + ".")))
    lt.append((12, "Xóa loại nghỉ", "P1", 'Loại nghỉ "Nghỉ chăm con" chưa phát sinh chấm công, có nút Xóa.',
               S('Bánh răng > "Xóa".', 'Popup "Cảnh báo" bấm "Xoá".'), "—",
               B('Hiện "Xóa thành công", dòng biến mất.',
                 "Lưu ý: dòng đã xoá không còn nút Lịch sử để mở; lịch sử xóa (tên hành động \"Xóa\" chữ đỏ, nhóm lọc \"Thay đổi trạng thái\") được lưu nhưng không xem được trên giao diện (đặc tả gốc có dòng Xóa - ghi Pending nếu cần).")))
    lt.append((13, "Loại nghỉ hệ thống: Tên và Nhóm bị khoá, không sinh lịch sử 2 trường này", "P1",
               'Loại nghỉ "Nghỉ phép" của hệ thống (không có nút Xóa).',
               S("Bánh răng dòng Nghỉ phép > Sửa.", "Thử sửa Tên loại nghỉ và Nhóm.", "Đổi Ghi chú, Lưu, mở Lịch sử."), "—",
               B("Ô Tên loại nghỉ và Nhóm bị khoá (xám).", "Dòng lịch sử mới chỉ có Ghi chú.")))

    # ---- Nghi le
    HL_PRE = L(TK_A, 'Ngày nghỉ lễ "Quốc khánh" ký hiệu QK, Ngày 02/09/2026, không tick Ngày nghỉ bù, Tỉ lệ hưởng lương 100, Ghi chú "Nghỉ lễ".')
    hl = []
    hl.append((1, "Thêm ngày nghỉ lễ ghi đủ 6 trường", "P0", TK_A,
               S(M_HOL + ', tab "Nghỉ lễ", bấm "Thêm mới".',
                 'Nhập Tên ngày nghỉ "Giỗ Tổ", Ký hiệu "GT", Ngày 26/04/2026, tick "Ngày nghỉ bù", Tỉ lệ hưởng lương 100, Ghi chú "10/3 âm lịch".',
                 'Bấm "Lưu".', "Bánh răng dòng Giỗ Tổ > Lịch sử thay đổi."), "Ngày: 26/04/2026",
               B('Tiêu đề popup "Lịch sử thay đổi: Giỗ Tổ".',
                 'Dòng "Tạo mới" chữ xanh lá (nhóm lọc "Tạo mới"), liệt kê 6 trường chỉ có giá trị mới chữ xanh: Tên ngày nghỉ: Giỗ Tổ; Ký hiệu: GT; Ngày: 26/04/2026; '
                 "Tỉ lệ hưởng lương (%): 100; Ngày nghỉ bù: Có; Ghi chú: 10/3 âm lịch.",
                 "Ngày dạng dd/mm/yyyy.",
                 'Sau khi lưu hiện thông báo "Tạo ngày nghỉ lễ thành công".')))
    hl_fields = [
        ("Tên ngày nghỉ", 'ô "Tên ngày nghỉ" từ "Quốc khánh" thành "Quốc khánh 2/9"', "Quốc khánh", "Quốc khánh 2/9"),
        ("Ký hiệu", 'ô "Ký hiệu" từ "QK" thành "QK29"', "QK", "QK29"),
        ("Ngày", 'ô "Ngày" từ 02/09/2026 sang 03/09/2026', "02/09/2026", "03/09/2026"),
        ("Tỉ lệ hưởng lương (%)", 'ô "Tỉ lệ hưởng lương (%)" từ 100 thành 300', "100", "300"),
        ("Ngày nghỉ bù", 'tick ô "Ngày nghỉ bù"', "Không", "Có"),
        ("Ghi chú", 'ô "Ghi chú" từ "Nghỉ lễ" thành để trống', "Nghỉ lễ", "(trống)"),
    ]
    for i, (lab, act, o, n) in enumerate(hl_fields, start=2):
        hl.append((i, 'Sửa ngày nghỉ lễ - ghi lịch sử trường "%s"' % lab, "P0", HL_PRE,
                   S(M_HOL + ', tab "Nghỉ lễ".', "Bánh răng dòng Quốc khánh > Sửa.", "Đổi " + act + ".", 'Bấm "Lưu".',
                     "Bánh răng dòng đó > Lịch sử thay đổi."),
                   L("Trường: " + lab, "Trước: " + o, "Sau: " + n),
                   B('Popup tiêu đề "Cập nhật ngày nghỉ lễ"; sau khi lưu hiện thông báo "Cập nhật ngày nghỉ lễ thành công" (không còn "Tạo loại nghỉ thành công").',
                     'Dòng trên cùng tên hành động "Thay đổi thông tin" chữ xanh dương, ' + ACTOR_A + '.',
                     "Có ĐÚNG 1 thay đổi: " + chg(lab, o, n) + ".")))
    hl.append((8, "Xóa ngày nghỉ lễ", "P1", "Ngày nghỉ Giỗ Tổ đã có lịch sử Thêm.",
               S("Bánh răng dòng Giỗ Tổ > Xóa, xác nhận."), "—",
               B('Hiện "Xoá ngày nghỉ lễ thành công", dòng biến mất.', "Không còn lối mở lịch sử của dòng đã xoá (ghi chú như Loại nghỉ).")))

    # ---- Nghi cat phep
    TL_PRE = L(TK_A, 'Ngày nghỉ cắt phép "Nghỉ Tết công ty" ký hiệu NTC, Ngày 16/02/2026, Số phép 1, Ghi chú "Cắt 1 ngày phép", '
                     "Nhân viên đi làm: NV001 - Trần Văn Bình.")
    tl = []
    tl.append((1, "Thêm ngày nghỉ cắt phép ghi đủ trường", "P0", TK_A,
               S(M_HOL + ', tab "Nghỉ cắt phép", bấm "Thêm mới".',
                 'Nhập Tên "Nghỉ bù Tết", Ký hiệu "NBT", Ngày 17/02/2026, Số phép 0.5, Nhân viên đi làm chọn NV001, NV002, Ghi chú "Nửa ngày".',
                 'Bấm "Lưu", chờ "Tạo ngày nghỉ cắt phép thành công".', "Bánh răng dòng Nghỉ bù Tết > Lịch sử thay đổi."), "Số phép: 0.5",
               B('Dòng "Tạo mới" chữ xanh lá (nhóm lọc "Tạo mới"), liệt kê giá trị mới chữ xanh: Tên ngày nghỉ cắt phép: Nghỉ bù Tết; Ký hiệu: NBT; Ngày: 17/02/2026; '
                 "Số phép: 0.5; Ghi chú: Nửa ngày.",
                 'Bên dưới nhãn "Nhân viên đi làm thêm mới:" và 2 dòng chữ xanh "- NV001 - Trần Văn Bình", "- NV002 - <họ tên>" (dạng "Mã NV - Họ tên", mỗi người 1 dòng).')))
    tl_fields = [
        ("Tên ngày nghỉ cắt phép", 'ô "Tên ngày nghỉ cắt phép" thành "Nghỉ Tết công ty 2026"', "Nghỉ Tết công ty", "Nghỉ Tết công ty 2026"),
        ("Ký hiệu", 'ô "Ký hiệu" từ NTC thành NTC26', "NTC", "NTC26"),
        ("Ngày", 'ô "Ngày" từ 16/02/2026 sang 18/02/2026', "16/02/2026", "18/02/2026"),
        ("Số phép", 'ô "Số phép" từ 1 thành 1.5', "1", "1.5"),
        ("Ghi chú", 'ô "Ghi chú" thành "Cắt 1,5 ngày phép"', "Cắt 1 ngày phép", "Cắt 1,5 ngày phép"),
    ]
    for i, (lab, act, o, n) in enumerate(tl_fields, start=2):
        tl.append((i, 'Sửa ngày nghỉ cắt phép - ghi lịch sử trường "%s"' % lab, "P0", TL_PRE,
                   S(M_HOL + ', tab "Nghỉ cắt phép".', "Bánh răng dòng Nghỉ Tết công ty > Sửa, chờ form hiện đủ dữ liệu.",
                     "Đổi " + act + ".", 'Bấm "Lưu".', "Bánh răng dòng đó > Lịch sử thay đổi."),
                   L("Trường: " + lab, "Trước: " + o, "Sau: " + n),
                   B('Sau khi lưu hiện thông báo "Cập nhật ngày nghỉ cắt phép thành công".', 'Dòng trên cùng tên hành động "Thay đổi thông tin" chữ xanh dương.', "Có ĐÚNG 1 thay đổi: " + chg(lab, o, n) + ".",
                     'Không có nhóm "Nhân viên đi làm ..." vì danh sách không đổi.')))
    tl.append((7, "Thêm nhân viên đi làm chỉ hiện người được thêm", "P0", TL_PRE,
               S("Sửa Nghỉ Tết công ty, ô Nhân viên đi làm chọn thêm NV003 - Lê Thị Cúc.", 'Bấm "Lưu", mở Lịch sử.'), "Thêm: NV003",
               B('Dòng "Thay đổi thông tin" (xanh dương) có nhãn "Nhân viên đi làm thêm mới:" và dòng chữ xanh "- NV003 - Lê Thị Cúc".',
                 "KHÔNG liệt kê lại NV001 đang có sẵn.")))
    tl.append((8, "Bỏ nhân viên đi làm chỉ hiện người bị bỏ", "P0", "Nghỉ Tết công ty có NV001, NV003.",
               S("Sửa, bỏ NV001 khỏi Nhân viên đi làm, Lưu, mở Lịch sử."), "Bỏ: NV001",
               B('Có nhãn "Nhân viên đi làm đã xóa:" và dòng chữ đỏ "- NV001 - Trần Văn Bình".', "Không liệt kê lại NV003 còn giữ nguyên.")))
    tl.append((9, "Vừa thêm vừa bỏ nhân viên đi làm trong 1 lần lưu", "P1", "Nghỉ Tết công ty có NV003.",
               S("Sửa: bỏ NV003, thêm NV004, Lưu, mở Lịch sử."), "—",
               B('1 dòng duy nhất, trong đó có cả nhóm "Nhân viên đi làm thêm mới:" (chữ xanh "- NV004 - ...") nằm TRƯỚC và nhóm "Nhân viên đi làm đã xóa:" (chữ đỏ "- NV003 - ...").', "Không sinh 2 dòng riêng cho thêm và bỏ.")))
    tl.append((10, "Xóa ngày nghỉ cắt phép", "P1", "Nghỉ bù Tết có 2 nhân viên đi làm.",
               S("Bánh răng dòng Nghỉ bù Tết > Xóa, xác nhận."), "—",
               B('Hiện "Xoá thành công", dòng biến mất; không còn lối mở lịch sử dòng đã xoá.')))

    sec8 = [
        (1, "Sửa loại nghỉ bấm Lưu không đổi gì không sinh dòng", "P0", LT_PRE,
         S("Bánh răng Nghỉ ốm > Sửa.", 'Không đổi gì, bấm "Lưu".', "Mở Lịch sử."), "—", B("Không có dòng \"Thay đổi thông tin\" mới.")),
        (2, "Sửa ngày nghỉ lễ / cắt phép Lưu không đổi không sinh dòng", "P0", HL_PRE,
         S("Sửa Quốc khánh, Lưu không đổi.", "Sửa Nghỉ Tết công ty, Lưu không đổi.", "Mở Lịch sử 2 dòng."), "—",
         B("Không dòng nào có lịch sử mới.")),
        (3, "Lưu loại nghỉ thiếu Tên bị chặn, không sinh dòng", "P0", LT_PRE,
         S("Sửa Nghỉ ốm, xoá trống Ký hiệu, Lưu.", "Huỷ, mở Lịch sử."), "Ký hiệu: trống",
         B('Dưới ô Ký hiệu hiện chữ đỏ "Bắt buộc phải nhập" (cùng câu với mọi ô bắt buộc khác của hệ thống); thông báo lỗi (khung đỏ) "Cập nhật loại nghỉ thất bại"; popup không đóng.', "Không có dòng lịch sử mới.")),
        (4, "Lưu ngày nghỉ cắt phép thiếu Ngày bị chặn", "P1", TK_A,
         S('Tab Nghỉ cắt phép "Thêm mới", chỉ nhập Tên và Ký hiệu, Lưu.'), "Ngày: trống",
         B('Thông báo "Tạo ngày nghỉ cắt phép thất bại"; dưới ô Tên ngày nghỉ cắt phép (nếu trống), Ký hiệu (nếu trống) và Ngày hiện chữ đỏ "Bắt buộc phải nhập".', "Không có dòng mới trong bảng.")),
        (5, "Tab Chung: rời ô số không đổi không sinh dòng", "P1", "Thời gian sử dụng = 12.",
         S(M_HOL + ".", "Bấm vào ô 12, bấm ra ngoài.", "Mở popup tab Chung."), "—", B("Không có dòng mới.")),
        (6, "Tab Chung: xoá trống ô số ghi đúng giá trị thật", "P0", "Số giờ phải gửi đơn trước = 24, ô tick đang tick.",
         S("Xoá trống ô giờ, bấm ra ngoài.", "Tải lại trang, ghi nhận giá trị ô.", "Mở popup."), "Sau: để trống",
         B('Dòng mới "Số giờ phải gửi đơn trước" | cũ "24" | mới đúng bằng giá trị ô sau khi tải lại ("(trống)" hoặc "0").')),
    ]

    sec11 = [
        (1, "Form Sửa loại nghỉ không hiện dữ liệu của dòng mở trước", "P0",
         "Có 2 loại nghỉ: Nghỉ ốm (NO, Tỉ lệ 75) và Nghỉ cưới (NC, Tỉ lệ 100).",
         S("Bánh răng Nghỉ ốm > Sửa, bấm Huỷ.", "Ngay lập tức bánh răng Nghỉ cưới > Sửa, quan sát form trong lúc đang tải."), "—",
         B("Form trống rồi hiện đúng dữ liệu Nghỉ cưới; KHÔNG thoáng hiện dữ liệu Nghỉ ốm.",
           'Trong lúc đang tải, nút "Lưu" bị khoá, không bấm được.')),
        (2, "Lưu nhanh khi form Sửa loại nghỉ chưa tải xong không ghi đè nhầm", "P0", "Mạng chậm (bật giả lập mạng chậm của trình duyệt).",
         S("Bánh răng Nghỉ cưới > Sửa, bấm Lưu ngay khi form vừa mở.", "Mở Lịch sử Nghỉ cưới và Nghỉ ốm."), "—",
         B("Không lưu được khi đang tải (nút Lưu khoá).", "Không có dòng lịch sử lạ ở cả 2 loại nghỉ.")),
        (3, "Form Sửa ngày nghỉ cắt phép không hiện dữ liệu dòng trước", "P0", "Có 2 ngày cắt phép A (NTC) và B (NBT) với danh sách Nhân viên đi làm khác nhau.",
         S("Sửa A, Huỷ.", "Sửa B, quan sát form và ô Nhân viên đi làm."), "—",
         B("Form B hiện đúng Tên, Ký hiệu, Ngày, Số phép, Nhân viên đi làm của B; không lẫn nhân viên của A.", "Nút Lưu khoá tới khi tải xong.")),
        (4, "Giá trị bật/tắt hiện Có/Không, số theo chuẩn quốc tế, mũi tên xám", "P1", TK_A,
         S("Tab Chung tick/bỏ tick Tăng phép theo thâm niên.", "Tab Loại nghỉ sửa Số ngày nghỉ tối đa thành 1000.", "Mở 2 popup."), "—",
         B('Hiện "Có"/"Không" và "1,000"; mũi tên xám; cũ đỏ, mới xanh.')),
        (5, "Người không có quyền không thấy nút Lịch sử, không vào được màn", "P0", L(TK_B, "Có địa chỉ màn Quy định nghỉ."),
         S("Đăng nhập B, dán địa chỉ màn."), "—", B("Bị chuyển sang trang " + NOT_FOUND + ".")),
        (6, "Lịch sử theo công ty đang chọn", "P1", "Công ty 1 và 2 cùng có loại nghỉ tên Nghỉ ốm.",
         S("Ở Công ty 2 mở Lịch sử Nghỉ ốm và popup tab Chung."), "—", B("Chỉ thấy lịch sử của Công ty 2.")),
        (7, "Tiêu đề popup và thông báo đúng đối tượng, đúng Thêm / Cập nhật", "P1", TK_A,
         S('Tab "Nghỉ lễ": bấm "Thêm mới", quan sát tiêu đề, thêm "Giỗ Tổ" rồi Lưu.', 'Sửa "Giỗ Tổ", quan sát tiêu đề, đổi Ghi chú rồi Lưu.',
           'Lặp lại với tab "Loại nghỉ" và "Nghỉ cắt phép".'), "—",
         B('Nghỉ lễ: tiêu đề "Thêm ngày nghỉ lễ" / "Cập nhật ngày nghỉ lễ"; thông báo "Tạo ngày nghỉ lễ thành công" / "Cập nhật ngày nghỉ lễ thành công".',
           'Loại nghỉ: "Tạo loại nghỉ thành công" / "Cập nhật loại nghỉ thành công"; Nghỉ cắt phép: "Tạo ngày nghỉ cắt phép thành công" / "Cập nhật ngày nghỉ cắt phép thành công".',
           'Không còn thông báo "Tạo loại nghỉ thành công" khi lưu Nghỉ lễ.')),
        (9, "Form Sửa ngày nghỉ lễ khoá nút Lưu khi đang tải, không hiện dữ liệu lần mở trước", "P0",
         "Có 2 ngày nghỉ lễ Quốc khánh (QK) và Giỗ Tổ (GT).",
         S('Tab "Nghỉ lễ": bấm "Thêm mới", nhập Tên "abc", bấm "Huỷ".', "Ngay lập tức bánh răng dòng Quốc khánh > Sửa, quan sát nút Lưu và các ô.",
           "Chờ tải xong, đổi Ghi chú rồi Lưu; mở Lịch sử thay đổi của Quốc khánh."), "—",
         B('Trong lúc tải, nút "Lưu" bị khoá, form không còn chữ "abc" của lần mở trước.',
           'Tải xong form hiện đúng Tên, Ký hiệu, Ngày của Quốc khánh; Lưu báo "Cập nhật ngày nghỉ lễ thành công".',
           'Lịch sử Quốc khánh có 1 dòng "Thay đổi thông tin" chỉ có Ghi chú; KHÔNG sinh thêm ngày nghỉ lễ mới trong bảng.')),
        (10, "Lưu trống ở Loại nghỉ / Nghỉ lễ / Nghỉ cắt phép báo cùng một câu lỗi", "P1", TK_A,
         S('Lần lượt ở tab "Loại nghỉ", "Nghỉ lễ", "Nghỉ cắt phép": bấm "Thêm mới", không nhập gì, bấm "Lưu".'), "Tất cả ô trống",
         B('Loại nghỉ: dưới Tên loại nghỉ, Ký hiệu, Nhóm, Tỉ lệ hưởng lương (%) hiện "Bắt buộc phải nhập"; thông báo "Tạo loại nghỉ thất bại".',
           'Nghỉ lễ: dưới Tên ngày nghỉ, Ký hiệu, Ngày, Tỉ lệ hưởng lương (%) hiện "Bắt buộc phải nhập"; thông báo "Tạo ngày nghỉ lễ thất bại".',
           'Nghỉ cắt phép: dưới Tên ngày nghỉ cắt phép, Ký hiệu, Ngày hiện "Bắt buộc phải nhập"; thông báo "Tạo ngày nghỉ cắt phép thất bại".',
           'KHÔNG còn câu "Bắt buộc nhập" lẫn với "Bắt buộc phải nhập".')),
        (8, "Lưu tab Chung thất bại báo lỗi khung đỏ, không sinh dòng", "P2", TK_A,
         S(M_HOL + ", tab Chung.", "Ngắt mạng máy đang test (hoặc để hết phiên đăng nhập).", 'Tick/bỏ tick "Tăng phép theo thâm niên".',
           "Bật lại mạng, tải lại trang, mở popup lịch sử."), "—",
         B('Hiện thông báo "Cập nhật thất bại" khung ĐỎ (không phải khung xanh).', "Tải lại trang ô tick giữ giá trị cũ; popup KHÔNG có dòng mới.")),
    ]

    sections = [
        ("I", "HIỂN THỊ TRANG & TRUY CẬP", sec1),
        ("II", "4 POPUP LỊCH SỬ (TAB CHUNG / LOẠI NGHỈ / NGHỈ LỄ / NGHỈ CẮT PHÉP): BỐ CỤC & BỘ LỌC", sec2),
        ("IV", "GHI LỊCH SỬ TỪNG TRƯỜNG - TAB CHUNG (26 TRƯỜNG)", f),
        ("V", "TAB LOẠI NGHỈ: THÊM / SỬA TỪNG TRƯỜNG / KHÓA / MỞ KHÓA / XÓA", lt),
        ("VI", "TAB NGHỈ LỄ: THÊM / SỬA TỪNG TRƯỜNG / XÓA", hl),
        ("VII", "TAB NGHỈ CẮT PHÉP: THÊM / SỬA TỪNG TRƯỜNG / NHÂN VIÊN ĐI LÀM / XÓA", tl),
        ("VIII", "RÀNG BUỘC NHẬP LIỆU", sec8),
        ("XI", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", sec11),
    ]
    return desc, roles, sections


# ======================================================================
# 4. CAI DAT
# ======================================================================
def cai_dat():
    title = "Thay đổi thông tin"
    actor = ACTOR_A

    desc = [
        ("1. Mục đích tính năng",
         "Ghi lại lịch sử thay đổi màn Cài đặt (phân hệ Chấm công > Cấu hình > Cài đặt) và 3 cờ phân hệ đổi từ màn Cài đặt phân hệ "
         "(ERP, Quản lý cơm, Quyết định) - gom chung 1 popup \"Lịch sử thay đổi cài đặt\"."),
        ("2. Đối tượng được tính / hiển thị",
         "8 trường (nhãn trong popup): Tiêu đề; Sử dụng ERP; Sử dụng quyết định; Sử dụng cơm; "
         "Sử dụng CRM; Tra soát tháng trước trước ngày mùng; Số ngày tra soát tháng trước (hàng tháng); Logo.\n"
         "- Từ màn Cài đặt: Tiêu đề, Sử dụng CRM, Tra soát tháng trước trước ngày mùng (ô tick), Số ngày (ô số), Logo.\n"
         "- Từ màn Cài đặt phân hệ: tick/bỏ tick phân hệ \"ERP\" sinh Sử dụng ERP; phân hệ \"Quản lý cơm\" sinh Sử dụng cơm.\n"
         "- Logo hiện TÊN TỆP ảnh cũ (đỏ) và mới (xanh) dạng liên kết gạch chân; bấm vào mở popup xem trước ảnh.\n"
         "- Tiêu đề popup: \"Lịch sử thay đổi: Cài đặt\"."),
        ("3. Đối tượng bị ẩn / không tính",
         "- Bấm Lưu không đổi gì: không sinh dòng.\n- Lưu bị chặn (ngày mùng ngoài 1-31, Tiêu đề trống, chưa có logo): không sinh dòng.\n"
         "- Màn Cài đặt phân hệ: bật/tắt mục menu khác, thêm/bớt Nhân sự xem đầy đủ KHÔNG sinh dòng ở popup này.\n"
         "- Sử dụng quyết định: không còn phân hệ \"Quyết định\" riêng trên màn Cài đặt phân hệ nên không đổi được từ giao diện (xem mục 9)."),
        ("4. Bộ lọc thời gian áp dụng cho", FILTER_NOTE + "\nRiêng popup Cài đặt: lọc \"Tạo mới\" / \"Thay đổi trạng thái\" luôn rỗng; "
         "ô Người thực hiện liệt kê nhân sự của công ty ĐANG CHỌN làm việc."),
        ("5. Cấu trúc dữ liệu / cây phân cấp",
         "Popup dòng thời gian, mới nhất trên cùng, mỗi dòng tên hành động \"Thay đổi thông tin\" chữ xanh dương. 1 lần Lưu = 1 dòng gồm MỌI trường đổi "
         "(màn Cài đặt gửi cả 5 giá trị mỗi lần Lưu).\n" + GROUP_NOTE),
        ("6. Quy tắc cộng dồn / deduplicate",
         "So theo giá trị đã chuẩn hoá: ô tick so Có/Không, ô số so số (\"5\" và 5 như nhau), Logo so đường dẫn ảnh. "
         "Cài đặt là cấu hình CHUNG toàn hệ thống (không theo công ty): mọi người có quyền đều thấy cùng 1 lịch sử."),
        ("7. Phân quyền cấp",
         "- \"Thiết lập thông số\": thấy menu Cài đặt, nút \"Lịch sử thay đổi\", Lưu được.\n"
         "- \"Quản lý phân quyền\": thấy menu Cài đặt phân hệ, Lưu được (sinh dòng Sử dụng ERP / cơm), nhưng chỉ XEM được popup khi có thêm \"Thiết lập thông số\".\n"
         "- Không có quyền: không thấy menu; mở địa chỉ màn bị chuyển sang trang \"Không tìm thấy trang yêu cầu\"."),
        ("8. Cách tính các ô thống kê", "Không áp dụng - popup không có ô thống kê."),
        ("9. Ghi chú đọc bảng",
         COMMON_FORMAT_NOTE + "\n"
         "Bẫy dễ sai: (1) Lưu thành công hiện \"Thao tác thành công\" và TỰ TẢI LẠI TRANG sau 1 giây; (2) bỏ tick Tra soát tháng trước thì ô số bị khoá "
         "nhưng vẫn giữ giá trị cũ; (3) Lưu màn Cài đặt phân hệ chỉ ghi Sử dụng ERP / Sử dụng cơm; cờ Sử dụng quyết định không còn phân hệ "
         "tương ứng trên màn nên GIỮ NGUYÊN giá trị cũ, không bị đặt về Có và không sinh dòng lịch sử; (4) lịch sử Cài đặt là của toàn hệ thống "
         "nên có thể có dòng do người công ty KHÁC thực hiện, nhưng ô lọc Người thực hiện chỉ liệt kê nhân sự công ty đang chọn - người công ty khác không chọn được để lọc."),
    ]

    roles = [
        ("01", "Có quyền Thiết lập thông số thấy menu và nút Lịch sử thay đổi", "P0", TK_A,
         S("Đăng nhập A.", M_MASTER + ".", "Quan sát cuối màn."), "—",
         B('Góc phải dưới có 2 nút: "Lịch sử thay đổi" (nền sáng, biểu tượng đồng hồ) nằm TRÁI nút "Lưu" (xanh lá).')),
        ("02", "Không có quyền không thấy menu, không vào được màn", "P0", L(TK_B, "Có địa chỉ màn Cài đặt."),
         S("Đăng nhập B.", 'Mở nhóm "Cấu hình".', "Dán địa chỉ màn Cài đặt."), "—",
         B('Không có mục "Cài đặt" ' + MENU_HIDDEN + '.', "Bị chuyển sang trang " + NOT_FOUND + ", không Lưu được, không xem được lịch sử.")),
        ("03", "Chỉ có Thiết lập thông số không thấy menu Cài đặt phân hệ", "P1", 'Tài khoản A không có "Quản lý phân quyền".',
         S("Đăng nhập A.", 'Mở nhóm "Cấu hình".'), "—", B('Có "Cài đặt" nhưng KHÔNG có "Cài đặt phân hệ".')),
        ("04", "Chỉ có Quản lý phân quyền lưu Cài đặt phân hệ được nhưng không xem popup Cài đặt", "P1",
         'Tài khoản F: có "Quản lý phân quyền", KHÔNG có "Thiết lập thông số".',
         S("Đăng nhập F.", M_SUB + ", bỏ tick phân hệ ERP, bấm Lưu.", 'Mở nhóm "Cấu hình" tìm mục "Cài đặt".', "Tài khoản A mở popup Cài đặt."), "—",
         B('F lưu thành công ("Lưu cấu hình hiển thị thành công."), F không có mục "Cài đặt".',
           'Ở tài khoản A, dòng trên cùng popup là "Sử dụng ERP: Có -> Không" với dòng "Người thực hiện: <họ tên F> — <phòng ban của F>".')),
    ]

    OPEN_MS = ["Đăng nhập tài khoản A.", M_MASTER + ".", 'Bấm "Lịch sử thay đổi" (góc phải dưới, bên trái nút "Lưu").']
    sec1 = [
        popup_empty(1, "Cài đặt", "Hệ thống mới, chưa đổi Cài đặt lần nào.", OPEN_MS),
        (2, "Lịch sử cài đặt dùng chung, không theo công ty", "P1", "A đang ở Công ty 1, D đang ở Công ty 2, cả hai có quyền.",
         S("A đổi Tiêu đề.", "D mở popup Cài đặt."), "—", B("D thấy dòng đổi Tiêu đề của A (Cài đặt là cấu hình chung toàn hệ thống).",
                                                           "Dòng ghi đúng tên và phòng ban của A.")),
        (3, "Mở popup không làm mất dữ liệu đang sửa dở", "P2", TK_A,
         S("Gõ Tiêu đề mới nhưng chưa Lưu.", "Mở rồi đóng popup lịch sử."), "—", B("Tiêu đề đang gõ vẫn còn, chưa sinh dòng lịch sử.")),
    ]

    sec2 = popup_std(
        1, "Cài đặt", L(TK_A, "Đã có 3 lần đổi cài đặt."), OPEN_MS, "Cài đặt",
        'Mỗi dòng tên hành động "Thay đổi thông tin" chữ xanh dương, bên dưới từng trường đổi dạng cũ -> mới.',
        L(TK_A, "Lịch sử Cài đặt có 3 dòng đổi cài đặt."),
        ('"Thay đổi thông tin": hiện đủ 3 dòng (kể cả dòng Sử dụng ERP / Sử dụng cơm đổi từ màn Cài đặt phân hệ).',
         '"Tạo mới" và "Thay đổi trạng thái": hiện ' + NO_MATCH))

    MS_PRE = L(TK_A, 'Cài đặt hiện tại: Tiêu đề "HRM", Sử dụng CRM không tick, Tra soát tháng trước trước ngày mùng đang tick với số 5, đã có logo.')

    def ms_tc(num, lab, act, td, o, n, prio="P0", extra=()):
        return (num, 'Ghi lịch sử khi đổi "%s" ở màn Cài đặt' % lab, prio, MS_PRE,
                S("Đăng nhập A.", M_MASTER + ".", act, 'Bấm "Lưu", chờ thông báo "Thao tác thành công" và trang tự tải lại.',
                  'Bấm "Lịch sử thay đổi".'), td,
                B('Dòng trên cùng tên hành động "%s" chữ xanh dương, thời gian đúng lúc lưu, %s.' % (title, actor),
                  "Dòng có ĐÚNG 1 thay đổi: " + chg(lab, o, n) + ".",
                  "Không kèm 4 trường còn lại dù màn gửi cả 5 giá trị khi Lưu.", *extra))

    ms = [
        ms_tc(1, "Tiêu đề", 'Sửa ô "Tiêu đề" từ "HRM" thành "Tân Phát HRM".', L("Trước: HRM", "Sau: Tân Phát HRM"), "HRM", "Tân Phát HRM"),
        ms_tc(2, "Sử dụng CRM", 'Tick "Sử dụng CRM".', L("Trước: không tick", "Sau: tick"), "Không", "Có"),
        ms_tc(3, "Sử dụng CRM", 'Bỏ tick "Sử dụng CRM" (đang tick).', L("Trước: tick", "Sau: bỏ tick"), "Có", "Không", prio="P1"),
        ms_tc(4, "Tra soát tháng trước trước ngày mùng", 'Bỏ tick "Tra soát tháng trước trước ngày mùng ... hàng tháng".',
              L("Trước: tick", "Sau: bỏ tick"), "Có", "Không",
              extra=("Ô số 5 bị khoá nhưng giữ nguyên, KHÔNG sinh thay đổi Số ngày tra soát tháng trước (hàng tháng).",)),
        ms_tc(5, "Số ngày tra soát tháng trước (hàng tháng)", "Sửa ô số ngày mùng từ 5 thành 10.", L("Trước: 5", "Sau: 10"), "5", "10"),
        (6, "Ghi lịch sử khi đổi Logo: hiện ảnh và đường dẫn cũ / mới", "P0", MS_PRE,
         S(M_MASTER + ".", 'Bấm "Tải ảnh lên", chọn ảnh logo_moi.png (200 KB).', 'Bấm "Lưu", chờ trang tải lại.', "Mở popup lịch sử."),
         "Ảnh: logo_moi.png (png, 200 KB)",
         B('Dòng trên cùng có đúng 1 thay đổi "Logo:" gồm: TÊN TỆP logo cũ (chữ đỏ, gạch chân), mũi tên, TÊN TỆP logo mới (chữ xanh, gạch chân).',
           "KHÔNG hiện nguyên đường dẫn dài; rê chuột lên tên tệp hiện đường dẫn đầy đủ.",
           "Bấm vào tên tệp mới: mở popup xem trước ảnh logo ngay trên trang (không mở tab mới); đóng popup xem trước thì popup lịch sử vẫn còn.",
           "Ảnh logo đầu trang cũng đổi sang logo mới.")),
        (7, "Lưu nhiều trường cùng lúc sinh 1 dòng gồm đủ các trường", "P1", MS_PRE,
         S('Sửa Tiêu đề "HRM 2", tick Sử dụng CRM, sửa ngày mùng 5 thành 7.', "Bấm Lưu, mở popup."), "—",
         B("1 dòng mới gồm đúng 3 thay đổi: Tiêu đề, Sử dụng CRM, Số ngày tra soát tháng trước (hàng tháng).")),
    ]

    SUB_PRE = 'Tài khoản G: có cả "Thiết lập thông số" và "Quản lý phân quyền". Phân hệ ERP và Quản lý cơm đang tick (bật).'
    sub = [
        (1, 'Bỏ tick phân hệ ERP sinh dòng "Sử dụng ERP"', "P0", SUB_PRE,
         S("Đăng nhập G.", M_SUB + ".", 'Cột trái chọn phân hệ "ERP", bỏ tick ô tên phân hệ ở đầu cột phải.',
           'Bấm "Lưu" ở chân màn, chờ "Lưu cấu hình hiển thị thành công."', M_MASTER + ', bấm "Lịch sử thay đổi".'), "Phân hệ: ERP",
         B('Dòng trên cùng "Thay đổi thông tin" (xanh dương), dòng "Người thực hiện: <họ tên G> — <phòng ban của G>".', "Có ĐÚNG 1 thay đổi: " + chg("Sử dụng ERP", "Có", "Không") + ".")),
        (2, 'Tick lại phân hệ ERP sinh dòng ngược lại', "P1", "Phân hệ ERP đang bỏ tick.",
         S(M_SUB + ", tick lại ERP, Lưu.", "Mở popup Cài đặt."), "—", B("Dòng mới: " + chg("Sử dụng ERP", "Không", "Có") + ".")),
        (3, 'Bỏ tick phân hệ Quản lý cơm sinh dòng "Sử dụng cơm"', "P0", SUB_PRE,
         S(M_SUB + ', chọn phân hệ "Quản lý cơm", bỏ tick, Lưu.', "Mở popup Cài đặt."), "Phân hệ: Quản lý cơm",
         B("Dòng mới có ĐÚNG 1 thay đổi: " + chg("Sử dụng cơm", "Có", "Không") + ".")),
        (4, "Tắt 2 phân hệ trong 1 lần lưu sinh 1 dòng 2 trường", "P1", SUB_PRE,
         S("Bỏ tick ERP và Quản lý cơm, bấm Lưu 1 lần.", "Mở popup Cài đặt."), "—",
         B("1 dòng mới gồm Sử dụng ERP (Có -> Không) và Sử dụng cơm (Có -> Không).")),
        (5, "Đổi mục menu khác / Nhân sự xem đầy đủ không sinh dòng", "P0", SUB_PRE,
         S(M_SUB + '.', 'Bỏ tick 1 mục menu trong phân hệ "Chấm công"; thêm 1 người ở "Nhân sự xem đầy đủ".', "Lưu.", "Mở popup Cài đặt."), "—",
         B("Không có dòng mới.")),
        (6, "Sử dụng quyết định không đổi được từ màn Cài đặt phân hệ", "P1", SUB_PRE,
         S(M_SUB + '.', 'Tìm phân hệ tên "Quyết định" ở cột trái.', 'Bỏ tick phân hệ "Văn bản - Hồ sơ pháp lý" (phân hệ chứa màn Quyết định), Lưu.', "Mở popup Cài đặt."), "—",
         B('Không có phân hệ nào tên "Quyết định".', 'Popup KHÔNG có dòng "Sử dụng quyết định: Có -> Không".',
           "Lưu ý: đặc tả yêu cầu ghi lịch sử bỏ tick Quyết định; hiện không có lối thao tác - ghi Pending, chờ nghiệp vụ chốt.")),
        (7, "Lưu Cài đặt phân hệ không làm đổi Sử dụng quyết định", "P0",
         L(SUB_PRE, "Cờ Sử dụng quyết định đang là Không (nhờ quản trị hệ thống đặt sẵn); ghi nhận số dòng popup Cài đặt."),
         S("Đăng nhập G.", M_SUB + '.', 'Không đổi gì, bấm "Lưu", chờ "Lưu cấu hình hiển thị thành công."',
           'Bỏ tick phân hệ "Quản lý cơm", Lưu.', 'Tick lại "Quản lý cơm", Lưu.', M_MASTER + ', bấm "Lịch sử thay đổi".'), "—",
         B('Lần Lưu không đổi gì: popup KHÔNG có dòng mới, KHÔNG có dòng "Sử dụng quyết định: Không -> Có".',
           "Có đúng 2 dòng mới: " + chg("Sử dụng cơm", "Có", "Không") + " và " + chg("Sử dụng cơm", "Không", "Có") + "; không dòng nào nhắc Sử dụng quyết định.",
           "Cờ Sử dụng quyết định vẫn là Không (các màn phụ thuộc cờ này, vd ô Cộng tác viên ở Danh mục phòng ban, giữ nguyên trạng thái).")),
    ]

    sec8 = [
        (1, "Bấm Lưu không đổi gì không sinh dòng", "P0", MS_PRE,
         S(M_MASTER + ".", 'Không đổi gì, bấm "Lưu".', "Sau khi trang tải lại, mở popup."), "—",
         B('Có thông báo "Thao tác thành công" nhưng popup KHÔNG có dòng mới.')),
        (2, "Ngày mùng ngoài 1-31 bị chặn, không sinh dòng", "P0", MS_PRE,
         S("Nhập 0 vào ô ngày mùng, bấm Lưu.", "Lần lượt thử 32 và 1.5.", "Mở popup."), L("0", "32", "1.5"),
         B('Dưới ô hiện chữ đỏ "Chỉ nhập ngày từ 1 đến 31" (cả 3 lần 0, 32, 1.5), không lưu, trang không tải lại, không có thông báo.', "Giá trị user nhập giữ nguyên trong ô.", "Popup không có dòng mới.")),
        (3, "Bật tra soát mà để trống ngày mùng bị chặn", "P0", MS_PRE,
         S("Giữ tick Tra soát tháng trước, xoá trống ô số, Lưu."), "Ngày mùng: trống",
         B('Dưới ô hiện "Bắt buộc phải nhập"; không lưu, không sinh dòng.')),
        (4, "Tiêu đề trống bị chặn", "P1", MS_PRE,
         S("Xoá trống Tiêu đề, Lưu."), "Tiêu đề: trống", B('Dưới ô Tiêu đề hiện chữ đỏ "Bắt buộc phải nhập"; không lưu, trang không tải lại; không sinh dòng.')),
        (5, "Xóa ảnh logo rồi Lưu bị chặn", "P1", MS_PRE,
         S('Bấm "Xóa ảnh", bấm Lưu.'), "—", B('Hiện chữ đỏ "Bạn phải chọn ảnh" dưới khung logo; không sinh dòng.')),
        (6, "Tải ảnh sai định dạng / quá 5MB bị chặn", "P2", MS_PRE,
         S('"Tải ảnh lên" chọn file .gif.', "Chọn ảnh .png 6MB."), L("logo.gif", "anh_6mb.png"),
         B('Lần 1 hiện "File không hợp lệ"; lần 2 hiện "Dung lượng tối đa: 5MB"; không sinh dòng.')),
    ]

    sec11 = [
        (1, "Ngày mùng tra soát chỉ nhận 1-31", "P0", MS_PRE,
         S("Nhập 31, Lưu.", "Nhập 25, Lưu.", "Mở popup."), L("31", "25"),
         B("Cả 2 lần lưu được (trước đây bị giới hạn sai).", 'Popup có 2 dòng: 5 -> 31 và 31 -> 25.')),
        (2, "Người không có quyền không xem được lịch sử và không lưu được Cài đặt", "P0", L(TK_B, "Có địa chỉ màn Cài đặt."),
         S("Đăng nhập B, dán địa chỉ màn Cài đặt."), "—",
         B("Bị chuyển sang trang " + NOT_FOUND + "; không có nút Lưu / Lịch sử để thao tác.")),
        (3, "Chưa đăng nhập không lưu được Cài đặt", "P1", "Đăng xuất khỏi hệ thống.",
         S("Mở địa chỉ màn Cài đặt khi chưa đăng nhập."), "—",
         B("Bị đưa về màn Đăng nhập; không thay đổi được cài đặt (màn Đăng nhập vẫn hiện logo, tiêu đề bình thường).")),
        (4, "Giá trị bật/tắt hiện Có/Không, mũi tên xám", "P1", MS_PRE,
         S("Tick Sử dụng CRM, Lưu, mở popup."), "—", B('Hiện "Không" -> "Có" (không phải Bật/Tắt); mũi tên xám.')),
    ]

    sections = [
        ("I", "HIỂN THỊ TRANG & TRUY CẬP", sec1),
        ("II", "POPUP LỊCH SỬ CÀI ĐẶT: BỐ CỤC & BỘ LỌC", sec2),
        ("IV", "GHI LỊCH SỬ TỪNG TRƯỜNG - MÀN CÀI ĐẶT", ms),
        ("V", "GHI LỊCH SỬ 3 CỜ PHÂN HỆ TỪ MÀN CÀI ĐẶT PHÂN HỆ", sub),
        ("VIII", "RÀNG BUỘC NHẬP LIỆU", sec8),
        ("XI", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", sec11),
    ]
    return desc, roles, sections


# ======================================================================
# 5. CA LAM VIEC
# ======================================================================
def ca_lam_viec():
    desc = [
        ("1. Mục đích tính năng",
         "Ghi lại lịch sử thay đổi từng ca làm việc ở Danh mục ca làm việc: tạo mới, sửa từng trường, danh sách địa điểm / máy chấm công / "
         "khung giờ phạt, khoá, mở khoá, xoá. Xem ở 2 nơi: mục \"Lịch sử thay đổi\" trong menu bánh răng của từng ca (popup) và khối \"Lịch sử\" "
         "trong thân màn Sửa ca làm việc (thay cho nút Lịch sử ở chân màn trước đây)."),
        ("2. Đối tượng được tính / hiển thị",
         "42 trường (nhãn trong popup) chia 3 nhóm:\n"
         "Thông tin ca: Ca chỉ ghi nhận lịch sử chấm công; Tên ca; Mã ca; Giờ bắt đầu ca; Giờ kết thúc ca; Chấm giờ vào; Chấm vào từ; Chấm vào đến; "
         "Chấm giờ ra; Chấm ra từ; Chấm ra đến; Nghỉ giữa ca; Nghỉ từ; Nghỉ đến; Nghỉ - chấm ra; Nghỉ chấm ra từ; Nghỉ chấm ra đến; "
         "Nghỉ - chấm vào; Nghỉ chấm vào từ; Nghỉ chấm vào đến; Cho phép máy chấm công; Cho phép app điện thoại; Địa điểm máy chấm công.\n"
         "Tính công: Giờ công; Ngày công; Hệ số ngày thường; Hệ số ngày nghỉ; Hệ số ngày lễ.\n"
         "Cài đặt: Đi muộn về sớm; Cho phép đi muộn (phút); Cho phép về sớm (phút); Phạt đi muộn/về sớm; Không giờ vào bị trừ công; "
         "Trừ giờ công (thiếu giờ vào); Trừ ngày công (thiếu giờ vào); Không giờ ra bị trừ công; Trừ giờ công (thiếu giờ ra); "
         "Trừ ngày công (thiếu giờ ra); Tính công ăn ca; Loại trừ khi không đủ công; Ca đêm; Không hỗ trợ tiền cơm; Trạng thái.\n"
         "Và 3 danh sách: Địa điểm chấm công hợp lệ (địa chỉ + vĩ độ, kinh độ); Máy chấm công hợp lệ (tên máy đang hoạt động); "
         "Khung giờ phạt đi muộn/về sớm (dạng \"Đi muộn 5-10 phút, trừ X giờ / Y ngày\")."),
        ("3. Đối tượng bị ẩn / không tính",
         "- Lưu không đổi gì: không sinh dòng.\n- Lưu bị chặn (thiếu Tên ca, mã trùng...): không sinh dòng.\n"
         "- Máy chấm công đang ngừng hoạt động không đưa vào lịch sử.\n"
         "- Ca đã xoá không còn trên danh sách nên không mở được popup của nó.\n"
         "- Hệ số ngày thường / nghỉ / lễ không có ô trên form: chỉ thấy trong dòng Tạo mới (mặc định 1 / 2 / 3) hoặc khi bật Ca chỉ ghi nhận lịch sử chấm công."),
        ("4. Bộ lọc thời gian áp dụng cho", FILTER_NOTE + "\nÔ Người thực hiện liệt kê nhân sự của công ty sở hữu ca làm việc. "
         "Khối Lịch sử ở màn Sửa ca có đúng bộ lọc này."),
        ("5. Cấu trúc dữ liệu / cây phân cấp",
         "Popup: tiêu đề \"Lịch sử thay đổi: <Mã ca> - <Tên ca>\" (vd \"Lịch sử thay đổi: HC01 - Hành chính\"). Dòng thời gian mới nhất trên cùng.\n"
         "- \"Tạo mới\" (xanh lá): liệt kê lần lượt các trường theo thứ tự Thông tin ca -> Tính công -> Cài đặt, chỉ giá trị mới chữ xanh "
         "(ô tick chỉ hiện khi Có, ô khác chỉ hiện khi có giá trị); kèm các nhóm danh sách \"... thêm mới:\".\n"
         "- \"Thay đổi thông tin\" (xanh dương) / \"Khóa\" (cam) / \"Mở khóa\" (xanh lá): chỉ trường đổi dạng cũ -> mới; "
         "danh sách hiện theo nhóm \"Địa điểm chấm công hợp lệ thêm mới:\" / \"Địa điểm chấm công hợp lệ đã xóa:\", "
         "\"Máy chấm công hợp lệ thêm mới:\" / \"... đã xóa:\", \"Khung giờ phạt đi muộn/về sớm thêm mới:\" / \"... đã xóa:\".\n"
         "- \"Xóa\" (đỏ): liệt kê như Tạo mới, chữ đỏ (không xem được vì ca đã xóa).\n"
         "Khối \"Lịch sử\" ở màn Sửa ca: nằm cuối nội dung, ngay trên hàng nút \"Lưu\" / \"Quay lại\"; mặc định THU GỌN (chỉ có thanh tiêu đề "
         "\"Lịch sử\" và nút \"Xem lịch sử\"); bấm mở mới tải dữ liệu; nội dung, thứ tự và bộ lọc giống hệt popup. Màn Thêm mới ca KHÔNG có khối này.\n" + GROUP_NOTE),
        ("6. Quy tắc cộng dồn / deduplicate",
         "1 lần Lưu = 1 dòng \"Thay đổi thông tin\" gồm mọi trường đổi. Đổi Trạng thái trên form cùng lúc với trường khác sinh 2 dòng: dòng \"Khóa\" / \"Mở khóa\" (chỉ Trạng thái) "
         "rồi dòng \"Thay đổi thông tin\" (phần còn lại). Đổi Giờ bắt đầu / kết thúc / giờ nghỉ làm Giờ công tự tính lại nên cùng dòng có cả Giờ công. "
         "Khung giờ phạt được so theo nội dung, lưu lại y nguyên không sinh dòng."),
        ("7. Phân quyền cấp",
         "- Xem popup lịch sử: \"Quản lý ca làm việc\" HOẶC \"Xem danh mục ca làm việc theo tổng công ty\" HOẶC \"Xem danh mục ca làm việc theo công ty\".\n"
         "- Vào màn Danh mục ca làm việc (menu): \"Xem danh mục ca làm việc theo tổng công ty\" hoặc \"Xem danh mục ca làm việc theo công ty\".\n"
         "- Thêm mới / Sửa / Khóa / Mở khóa / Xóa: \"Quản lý ca làm việc\" (không có thì các mục này ẩn khỏi bánh răng)."),
        ("8. Cách tính các ô thống kê", "Giờ công tự tính = số giờ từ Giờ bắt đầu ca tới Giờ kết thúc ca, trừ đi số giờ từ Nghỉ từ tới Nghỉ đến (đơn vị giờ).\nKhông có ô thống kê khác."),
        ("9. Ghi chú đọc bảng",
         COMMON_FORMAT_NOTE + "\n"
         "Bẫy dễ sai: (1) ô tick Chấm vào / Chấm ra cạnh Giờ bắt đầu / kết thúc ca bị KHOÁ ở màn Sửa (chỉ chọn lúc Thêm); "
         "(2) ca đã được phân cho nhân viên vẫn sửa được mọi ô (đã chốt 29/09: không khoá), nhưng KHÔNG có mục Xóa - nên chuẩn bị ca CHƯA phân để test cả Xóa; "
         "(3) ô Loại trừ khi không làm đủ công chỉ hiện khi tick Tính công ăn ca; ô Không hỗ trợ tiền cơm chỉ hiện khi phân hệ cơm đang bật; "
         "(4) mục Xóa chỉ hiện với ca chưa phân."),
    ]

    PQ = '"Quản lý ca làm việc" và "Xem danh mục ca làm việc theo công ty"'
    TK = "Tài khoản M: có %s, đang ở Công ty 1" % PQ
    roles = [
        ("01", "Có quyền quản lý và xem danh mục thấy đủ mục trong bánh răng", "P0", TK,
         S("Đăng nhập M.", M_SHIFT + ".", "Bấm bánh răng dòng ca HC01 (chưa phân)."), "—",
         B('Màn mở có tiêu đề "Ca làm việc", góc phải có nút "Thêm mới" và "Bộ lọc".',
           'Bánh răng có: "Sửa", "Khóa", "Xóa", "Lịch sử thay đổi" (Lịch sử ở cuối).')),
        ("02", "Chỉ có quyền Xem danh mục ca làm việc theo công ty thấy Lịch sử, không thấy Sửa/Khóa/Xóa", "P0",
         'Tài khoản N: chỉ có "Xem danh mục ca làm việc theo công ty".',
         S("Đăng nhập N.", M_SHIFT + ".", "Bấm bánh răng 1 dòng.", "Bấm Lịch sử thay đổi."), "—",
         B('Không có nút "Thêm mới"; bánh răng chỉ có "Lịch sử thay đổi".', 'Popup "Lịch sử thay đổi: <Mã ca> - <Tên ca>" mở và đọc được lịch sử.')),
        ("03", "Chỉ có quyền Xem danh mục ca làm việc theo tổng công ty xem được lịch sử", "P1",
         'Tài khoản P: chỉ có "Xem danh mục ca làm việc theo tổng công ty".',
         S("Đăng nhập P.", M_SHIFT + ".", "Bánh răng > Lịch sử thay đổi."), "—", B("Mở được popup lịch sử.")),
        ("04", "Không có quyền nào không thấy menu, không vào được màn", "P0", L(TK_B, "Có địa chỉ màn Danh mục ca làm việc."),
         S("Đăng nhập B.", 'Mở nhóm "Danh mục" phân hệ Chấm công.', "Dán địa chỉ màn."), "—",
         B('Không có "Danh mục ca làm việc".', "Bị chuyển sang trang " + NOT_FOUND + ".")),
        ("05", "Chỉ có Quản lý ca làm việc (không có quyền xem danh mục) không vào được màn", "P1",
         'Tài khoản Q: chỉ có "Quản lý ca làm việc".',
         S("Đăng nhập Q.", 'Mở nhóm "Danh mục".', "Dán địa chỉ màn Danh mục ca làm việc."), "—",
         B('Không có mục "Danh mục ca làm việc"; mở địa chỉ bị chuyển sang trang ' + NOT_FOUND + ".",
           "Lưu ý: quyền quản lý nhưng không vào được màn - điểm cần nghiệp vụ chốt.")),
    ]

    OPEN_WS = ["Đăng nhập M.", M_SHIFT + ".", "Bánh răng dòng HC01 > Lịch sử thay đổi."]
    sec1 = [
        (1, "Popup chỉ hiện lịch sử đúng ca đã chọn", "P0", "HC01 có 3 dòng, CA2 có 1 dòng.",
         S("Mở lịch sử HC01, đóng.", "Mở lịch sử CA2."), "—",
         B('Tiêu đề lần lượt "Lịch sử thay đổi: HC01 - Hành chính" và "Lịch sử thay đổi: CA2 - <tên ca>".', "HC01: 3 dòng; CA2: 1 dòng; không lẫn.")),
        popup_empty(2, "ca làm việc", "Ca tạo trước khi có tính năng, chưa sửa.", [M_SHIFT + ".", "Bánh răng dòng ca đó > Lịch sử thay đổi."]),
        (3, "Tạo mới ca ghi dòng Tạo mới đủ trường", "P0", TK,
         S(M_SHIFT + ', bấm "Thêm mới".',
           "Nhập Tên ca \"Ca sáng\", Mã ca \"CS01\", Giờ bắt đầu 07:00 tick Chấm vào (Từ 06:30 Đến 07:30), Giờ kết thúc 11:00 tick Chấm ra (Từ 10:30 Đến 12:00), "
           "Hình thức chấm công hợp lệ: App điện thoại, 1 địa điểm \"Kho Liên Ninh\" vĩ độ 20.93, kinh độ 105.85, Ngày công 0.5.",
           'Bấm "Lưu", chờ "Thêm ca làm việc thành công".', "Bánh răng dòng CS01 > Lịch sử thay đổi."), "Giờ công tự tính: 4",
         B('Tiêu đề popup "Lịch sử thay đổi: CS01 - Ca sáng"; 1 dòng tên hành động "Tạo mới" chữ xanh lá, thuộc nhóm lọc "Tạo mới".',
           "Các trường liệt kê mỗi trường 1 dòng, chỉ có giá trị mới chữ xanh (không có mũi tên), theo thứ tự: Tên ca: Ca sáng; Mã ca: CS01; Giờ bắt đầu ca: 07:00; Giờ kết thúc ca: 11:00; Chấm giờ vào: Có; Chấm vào từ: 06:30; "
           "Chấm vào đến: 07:30; Chấm giờ ra: Có; Chấm ra từ: 10:30; Chấm ra đến: 12:00; Cho phép app điện thoại: Có.",
           "Tiếp theo: Giờ công: 4; Ngày công: 0.5; Hệ số ngày thường: 1; Hệ số ngày nghỉ: 2; Hệ số ngày lễ: 3.",
           'Cuối cùng: Trạng thái: Hoạt động (các ô tick không tick thì không hiện).',
           'Bên dưới nhãn "Địa điểm chấm công hợp lệ thêm mới:" và dòng chữ xanh "- Kho Liên Ninh (20.93, 105.85)".')),
        (4, "Tạo mới ca có máy chấm công và khung giờ phạt", "P1", TK,
         S('"Thêm mới" ca CS02, Hình thức chấm công: Máy chấm công, Địa điểm máy chấm công "VP Hà Nội", Máy chấm công hợp lệ "Máy HN 1".',
           'Tick "Phạt đi làm muộn/ về sớm", thêm khung phạt Đi muộn từ 5 đến 10 phút, Giờ công bị trừ 0.5, Ngày công bị trừ 0.05.', "Lưu, mở lịch sử."), "—",
         B("Dòng Tạo mới có: Cho phép máy chấm công: Có; Địa điểm máy chấm công: VP Hà Nội; Phạt đi muộn/về sớm: Có.",
           'Nhãn "Máy chấm công hợp lệ thêm mới:" và dòng chữ xanh "- Máy HN 1" (TÊN máy).',
           'Nhãn "Khung giờ phạt đi muộn/về sớm thêm mới:" và dòng chữ xanh "- Đi muộn 5-10 phút ... trừ 0.5 giờ / 0.05 ngày".')),
    ]

    sec2 = popup_std(
        1, "ca làm việc", L(TK, "Ca HC01 - Hành chính có 3 dòng lịch sử."), OPEN_WS, "HC01 - Hành chính",
        'Dòng tạo "Tạo mới" chữ xanh lá; dòng sửa "Thay đổi thông tin" xanh dương; dòng khóa "Khóa" cam; dòng mở khóa "Mở khóa" xanh lá.',
        L(TK, "Ca HC01 có 1 dòng tạo mới, 2 dòng sửa, 1 dòng khóa (chưa có mở khóa)."),
        ('"Tạo mới": còn đúng dòng "Tạo mới".', '"Thay đổi thông tin": còn đúng 2 dòng "Thay đổi thông tin".',
         '"Thay đổi trạng thái": còn đúng dòng "Khóa" (khóa / mở khóa là thay đổi trạng thái).'),
        scope="công ty của ca làm việc")

    # ---- Khoi Lich su trong man Sua ca (thay cho nut Lich su o footer)
    EDIT_WS = ["Đăng nhập M.", M_SHIFT + ".", "Bánh răng dòng HC01 > Sửa, chờ màn Sửa ca làm việc tải xong."]
    sec3 = [
        (1, "Màn Sửa ca có khối Lịch sử trong thân trang, không còn nút Lịch sử ở chân màn", "P0", L(TK, "Ca HC01 có 3 dòng lịch sử."),
         S(*(EDIT_WS + ["Cuộn xuống cuối nội dung màn.", "Quan sát khu vực nút ở chân màn."])), "—",
         B('Tiêu đề trang "Sửa ca làm việc".',
           'Cuối nội dung, ngay TRÊN hàng nút "Lưu" / "Quay lại", có khối "Lịch sử" (biểu tượng đồng hồ + chữ "Lịch sử", bên phải nút "Xem lịch sử").',
           "Khối mặc định THU GỌN: chưa hiện dòng lịch sử nào.",
           'Hàng nút chân màn chỉ còn "Lưu" và "Quay lại"; KHÔNG còn nút "Lịch sử" / "Lịch sử thay đổi" ở chân màn hay cạnh nút Lưu.')),
        (2, "Bấm mở khối Lịch sử mới tải dữ liệu, nội dung giống popup ở danh sách", "P0", L(TK, "Ca HC01 có 3 dòng lịch sử."),
         S(*(EDIT_WS + ['Bấm "Xem lịch sử" (hoặc bấm vào thanh tiêu đề khối).', "So với popup Lịch sử thay đổi của HC01 ở màn danh sách.",
                        'Bấm "Thu gọn".'])), "—",
         B("Khi bấm mới hiện biểu tượng đang tải rồi hiện lịch sử (khối thu gọn thì chưa tải).",
           'Cạnh chữ "Lịch sử" hiện số dòng "3"; nút đổi thành "Thu gọn" và có thêm nút "Làm mới".',
           "3 dòng lịch sử giống hệt popup ở danh sách: cùng thứ tự mới -> cũ, cùng tên hành động, người thực hiện, thời gian, giá trị cũ / mới.",
           'Bấm "Thu gọn": khối đóng lại; bấm "Xem lịch sử" lần nữa hiện lại ngay.')),
        (3, "Bộ lọc trong khối Lịch sử màn Sửa ca", "P1", L(TK, "Ca HC01 có 1 dòng tạo mới, 2 dòng sửa, 1 dòng khóa."),
         S(*(EDIT_WS + ['Mở khối Lịch sử, bấm "Bộ lọc".', 'Chọn "Loại hành động" = "Thay đổi trạng thái".', 'Chọn thêm "Người thực hiện" = D (chưa từng sửa ca).',
                        'Bấm "Làm mới" trong khung lọc.'])), "—",
         B('Khung lọc giống popup: "Loại hành động" (Tạo mới / Thay đổi thông tin / Thay đổi trạng thái), "Người thực hiện", "Từ ngày", "Đến ngày", nút "Làm mới"; không có nút Tìm kiếm.',
           'Thay đổi trạng thái: còn đúng dòng "Khóa".',
           "Thêm người thực hiện D: hiện " + NO_MATCH,
           "Làm mới: hiện lại đủ 4 dòng.")),
        (4, "Nút Làm mới ở thanh tiêu đề khối tải lại lịch sử mới nhất", "P2", L(TK, "Đang mở màn Sửa HC01 ở tab 1, khối Lịch sử đang mở (3 dòng)."),
         S("Tab 2: bánh răng HC01 > Khóa, Đồng ý.", 'Quay lại tab 1, bấm "Làm mới" ở thanh tiêu đề khối Lịch sử.'), "—",
         B('Khối tải lại, có thêm dòng "Khóa" (chữ cam) trên cùng, số dòng cạnh tiêu đề thành 4.',
           "Màn Sửa không tải lại, dữ liệu đang nhập trên form giữ nguyên.")),
        (5, "Khối Lịch sử của ca chưa có lịch sử", "P2", "Ca tạo trước khi có tính năng, chưa sửa.",
         S("Đăng nhập M.", M_SHIFT + ".", "Bánh răng dòng ca đó > Sửa.", 'Bấm "Xem lịch sử".'), "—",
         B("Khối hiện biểu tượng đồng hồ xám và chữ " + EMPTY_TXT, 'Không có nút "Bộ lọc"; cạnh chữ "Lịch sử" không hiện số.')),
        (6, "Màn Thêm mới ca KHÔNG có khối Lịch sử", "P0", TK,
         S("Đăng nhập M.", M_SHIFT + '.', 'Bấm "Thêm mới".', "Cuộn xuống cuối màn."), "—",
         B('Tiêu đề trang "Thêm ca làm việc".', 'KHÔNG có khối "Lịch sử"; chân màn chỉ có "Lưu" và "Quay lại".')),
        (7, "Sửa ca rồi mở lại màn Sửa thấy dòng mới trong khối Lịch sử", "P1", L(TK, "Ca HC01 đang có 3 dòng lịch sử."),
         S(*(EDIT_WS + ['Sửa "Tên ca" từ "Hành chính" thành "Hành chính HN", bấm "Lưu".', "Hệ thống quay về danh sách; bánh răng HC01 > Sửa.",
                        'Bấm "Xem lịch sử".'])), "Tên ca: Hành chính HN",
         B('Dòng trên cùng "Thay đổi thông tin" chữ xanh dương, ' + ACTOR_A.replace("tài khoản A", "M").replace("của A", "của M") + ".",
           "Có đúng 1 thay đổi: " + chg("Tên ca", "Hành chính", "Hành chính HN") + ".", 'Số dòng cạnh chữ "Lịch sử" thành 4.')),
    ]

    PRE = L(TK, 'Ca HC01 - Hành chính CHƯA được phân cho nhân viên nào (có mục Xóa), đang Hoạt động: 08:00 - 17:00, tick Chấm vào (Từ 07:00 Đến 09:00), '
                "tick Chấm ra (Từ 16:30 Đến 19:00), tick Nghỉ giữa ca 12:00 - 13:00, Giờ công 8, Ngày công 1, hình thức: App điện thoại + Máy chấm công.")

    def sh(num, lab, act, o, n, prio="P0", pre_extra=(), extra=(), multi=None):
        exp = [
            'Quay về danh sách, thông báo "Sửa ca làm việc thành công".',
            'Dòng trên cùng popup "Thay đổi thông tin" chữ xanh dương, dòng "Người thực hiện: <họ tên M> — <phòng ban của M>", thời gian đúng lúc lưu.',
        ]
        if multi:
            exp.append(multi)
        else:
            exp.append("Có ĐÚNG 1 thay đổi: " + chg(lab, o, n) + ".")
            exp.append("Không kèm trường khác.")
        exp.extend(extra)
        return (num, 'Sửa ca - ghi lịch sử trường "%s"' % lab, prio, L(PRE, *pre_extra),
                S("Đăng nhập M.", M_SHIFT + ".", "Bánh răng dòng HC01 > Sửa.", act, 'Bấm "Lưu".',
                  "Bánh răng dòng HC01 > Lịch sử thay đổi."),
                L("Trường: " + lab, "Trước: " + o, "Sau: " + n), B(*exp))

    f = [
        sh(1, "Tên ca", 'Sửa ô "Tên ca" từ "Hành chính" thành "Hành chính HN".', "Hành chính", "Hành chính HN"),
        sh(2, "Mã ca", 'Sửa ô "Mã ca" từ "HC01" thành "HC01A".', "HC01", "HC01A",
           extra=("Dòng dưới tiêu đề popup đổi thành HC01A - Hành chính khi mở lại.",)),
        sh(3, "Giờ bắt đầu ca", 'Đổi "Giờ bắt đầu ca" từ 08:00 sang 08:30.', "08:00", "08:30",
           multi="Dòng gồm 2 thay đổi: " + chg("Giờ bắt đầu ca", "08:00", "08:30") + "; và " + chg("Giờ công", "8", "7.5") + " (Giờ công tự tính lại).",
           extra=("Giờ dạng HH:mm, không có giây.",)),
        sh(4, "Giờ kết thúc ca", 'Đổi "Giờ kết thúc ca" từ 17:00 sang 17:30.', "17:00", "17:30",
           multi="Dòng gồm: " + chg("Giờ kết thúc ca", "17:00", "17:30") + "; và " + chg("Giờ công", "8", "8.5") + "."),
        sh(5, "Chấm vào từ", 'Ở "Từ" dưới Giờ bắt đầu ca đổi 07:00 sang 06:30.', "07:00", "06:30"),
        sh(6, "Chấm vào đến", 'Ở "Đến" dưới Giờ bắt đầu ca đổi 09:00 sang 09:30.', "09:00", "09:30"),
        sh(7, "Chấm ra từ", 'Ở "Từ" dưới Giờ kết thúc ca đổi 16:30 sang 16:00.', "16:30", "16:00"),
        sh(8, "Chấm ra đến", 'Ở "Đến" dưới Giờ kết thúc ca đổi 19:00 sang 20:00.', "19:00", "20:00"),
        sh(9, "Nghỉ giữa ca", 'Bỏ tick "Nghỉ giữa ca".', "Có", "Không",
           multi="Dòng có " + chg("Nghỉ giữa ca", "Có", "Không") + "; nếu Giờ công tự tính lại thì có thêm dòng Giờ công (8 -> 9)."),
        sh(10, "Nghỉ từ", 'Đổi "Nghỉ từ" 12:00 sang 11:30.', "12:00", "11:30",
           multi="Dòng có " + chg("Nghỉ từ", "12:00", "11:30") + " và " + chg("Giờ công", "8", "7.5") + "."),
        sh(11, "Nghỉ đến", 'Đổi "Nghỉ đến" 13:00 sang 13:30.', "13:00", "13:30",
           multi="Dòng có " + chg("Nghỉ đến", "13:00", "13:30") + " và " + chg("Giờ công", "8", "7.5") + "."),
        sh(12, "Nghỉ - chấm ra", 'Tick ô "Chấm ra" cạnh "Nghỉ từ", nhập Từ 11:45 Đến 12:15.', "Không", "Có",
           multi="Dòng có " + chg("Nghỉ - chấm ra", "Không", "Có") + "; " + "Nghỉ chấm ra từ: 11:45" + "; " + "Nghỉ chấm ra đến: 12:15" + " (2 trường này trước đó trống nên CHỈ hiện giá trị mới chữ xanh, không có mũi tên)."),
        sh(13, "Nghỉ chấm ra từ", 'Đổi "Từ" dưới Nghỉ từ 11:45 sang 11:30.', "11:45", "11:30", pre_extra=("Nghỉ - chấm ra đang tick, Từ 11:45 Đến 12:15.",)),
        sh(14, "Nghỉ chấm ra đến", 'Đổi "Đến" dưới Nghỉ từ 12:15 sang 12:30.', "12:15", "12:30", pre_extra=("Nghỉ - chấm ra đang tick.",)),
        sh(15, "Nghỉ - chấm vào", 'Tick ô "Chấm vào" cạnh "Nghỉ đến", nhập Từ 12:45 Đến 13:15.', "Không", "Có",
           multi="Dòng có " + chg("Nghỉ - chấm vào", "Không", "Có") + "; " + "Nghỉ chấm vào từ: 12:45" + "; " + "Nghỉ chấm vào đến: 13:15" + " (trước đó trống nên chỉ hiện giá trị mới, không có mũi tên)."),
        sh(16, "Nghỉ chấm vào từ", 'Đổi "Từ" dưới Nghỉ đến 12:45 sang 12:30.', "12:45", "12:30", pre_extra=("Nghỉ - chấm vào đang tick.",)),
        sh(17, "Nghỉ chấm vào đến", 'Đổi "Đến" dưới Nghỉ đến 13:15 sang 13:30.', "13:15", "13:30", pre_extra=("Nghỉ - chấm vào đang tick.",)),
        sh(18, "Cho phép app điện thoại", 'Ở "Hình thức chấm công hợp lệ" bỏ "App điện thoại" (giữ Máy chấm công).', "Có", "Không"),
        sh(19, "Cho phép máy chấm công", 'Ở "Hình thức chấm công hợp lệ" bỏ "Máy chấm công" (giữ App điện thoại).', "Có", "Không"),
        sh(20, "Địa điểm máy chấm công", 'Đổi "Địa điểm máy chấm công" từ "Kho Liên Ninh" sang "VPSG".', "Kho Liên Ninh", "VPSG",
           extra=("Hiện TÊN địa điểm, không hiện mã số.",)),
        sh(21, "Giờ công", 'Sửa ô "Giờ công" từ 8 thành 7.5 (không đổi giờ ca).', "8", "7.5"),
        sh(22, "Ngày công", 'Sửa ô "Ngày công" từ 1 thành 0.75.', "1", "0.75"),
        sh(23, "Đi muộn về sớm", 'Tick "Đi muộn về sớm", nhập Cho phép đi muộn 5, Cho phép về sớm 5.', "Không", "Có",
           multi="Dòng có " + chg("Đi muộn về sớm", "Không", "Có") + "; " + chg("Cho phép đi muộn (phút)", "0", "5") + " (nếu trước đó trống thì chỉ hiện giá trị mới 5, không có mũi tên); " + chg("Cho phép về sớm (phút)", "0", "5") + "."),
        sh(24, "Cho phép đi muộn (phút)", 'Sửa "Cho phép đi muộn" từ 5 thành 10.', "5", "10", pre_extra=("Đi muộn về sớm đang tick, cho phép 5 / 5 phút.",)),
        sh(25, "Cho phép về sớm (phút)", 'Sửa "Cho phép về sớm" từ 5 thành 15.', "5", "15", pre_extra=("Đi muộn về sớm đang tick.",)),
        sh(26, "Phạt đi muộn/về sớm", 'Tick "Phạt đi làm muộn/ về sớm", thêm 1 khung phạt Đi muộn 5-10 phút, trừ 1 giờ / 0.1 ngày.', "Không", "Có",
           multi="Dòng có " + chg("Phạt đi muộn/về sớm", "Không", "Có") + ' và nhóm "Khung giờ phạt đi muộn/về sớm thêm mới:" với dòng chữ xanh "- Đi muộn 5-10 phút ... trừ 1 giờ / 0.1 ngày".'),
        sh(27, "Không giờ vào bị trừ công", 'Tick "Nếu không có giờ vào thì bị trừ công", nhập Giờ công 4, Ngày công 0.5.', "Không", "Có",
           multi="Dòng có " + chg("Không giờ vào bị trừ công", "Không", "Có") + "; Trừ giờ công (thiếu giờ vào) -> 4; Trừ ngày công (thiếu giờ vào) -> 0.5."),
        sh(28, "Trừ giờ công (thiếu giờ vào)", 'Sửa ô "Giờ công" dưới "Nếu không có giờ vào thì bị trừ công" từ 4 thành 2.', "4", "2",
           pre_extra=("Không giờ vào bị trừ công đang tick (4 giờ / 0.5 ngày).",)),
        sh(29, "Trừ ngày công (thiếu giờ vào)", 'Sửa ô "Ngày công" dưới "Nếu không có giờ vào thì bị trừ công" từ 0.5 thành 0.25.', "0.5", "0.25",
           pre_extra=("Không giờ vào bị trừ công đang tick.",)),
        sh(30, "Không giờ ra bị trừ công", 'Tick "Nếu không có giờ ra thì bị trừ công", nhập Giờ công 4, Ngày công 0.5.', "Không", "Có",
           multi="Dòng có " + chg("Không giờ ra bị trừ công", "Không", "Có") + "; Trừ giờ công (thiếu giờ ra) -> 4; Trừ ngày công (thiếu giờ ra) -> 0.5."),
        sh(31, "Trừ giờ công (thiếu giờ ra)", 'Sửa ô "Giờ công" dưới "Nếu không có giờ ra thì bị trừ công" từ 4 thành 3.', "4", "3",
           pre_extra=("Không giờ ra bị trừ công đang tick.",)),
        sh(32, "Trừ ngày công (thiếu giờ ra)", 'Sửa ô "Ngày công" dưới "Nếu không có giờ ra thì bị trừ công" từ 0.5 thành 1.', "0.5", "1",
           pre_extra=("Không giờ ra bị trừ công đang tick.",)),
        sh(33, "Tính công ăn ca", 'Tick "Tính công ăn ca".', "Không", "Có"),
        sh(34, "Loại trừ khi không đủ công", 'Tick "Loại trừ khi không làm đủ công" (hiện sau khi tick Tính công ăn ca).', "Không", "Có",
           pre_extra=("Tính công ăn ca đang tick.",)),
        sh(35, "Ca đêm", 'Tick "Ca đêm".', "Không", "Có"),
        sh(36, "Không hỗ trợ tiền cơm", 'Tick "Không hỗ trợ tiền cơm".', "Không", "Có", prio="P1",
           pre_extra=("Phân hệ Quản lý cơm đang bật (ô này mới hiện).",)),
        sh(37, "Ca chỉ ghi nhận lịch sử chấm công", 'Tick "Ca chỉ ghi nhận lịch sử chấm công" ở đầu form.', "Không", "Có",
           multi="Dòng có " + chg("Ca chỉ ghi nhận lịch sử chấm công", "Không", "Có") + " kèm các trường tính công bị đưa về 0 / Không: Giờ công 8 -> 0; Ngày công 1 -> 0; "
                 "Hệ số ngày thường 1 -> 0; Hệ số ngày nghỉ 2 -> 0; Hệ số ngày lễ 3 -> 0; Nghỉ giữa ca Có -> Không ..."),
    ]

    lst = [
        (1, "Thêm địa điểm chấm công hợp lệ", "P0", L(PRE, 'Có 1 địa điểm "Kho Liên Ninh" (20.93, 105.85).'),
         S("Sửa HC01.", 'Ở "Địa điểm chấm công hợp lệ" bấm thêm dòng, nhập địa chỉ "VP Hà Nội", vĩ độ 21.027763, kinh độ 105.834160.', "Lưu, mở lịch sử."),
         "Địa điểm thêm: VP Hà Nội (21.027763, 105.834160)",
         B('Dòng "Thay đổi thông tin" (xanh dương) có nhãn "Địa điểm chấm công hợp lệ thêm mới:" và dòng chữ xanh "- VP Hà Nội (21.027763, 105.834160)".', "Không liệt kê lại Kho Liên Ninh.",
           'Dòng thuộc nhóm "Thay đổi thông tin".')),
        (2, "Bỏ địa điểm chấm công hợp lệ", "P0", L(PRE, "Có 2 địa điểm Kho Liên Ninh và VP Hà Nội."),
         S("Sửa HC01, bấm nút trừ ở dòng VP Hà Nội.", "Lưu, mở lịch sử."), "—",
         B('Có nhãn "Địa điểm chấm công hợp lệ đã xóa:" và dòng chữ đỏ "- VP Hà Nội (21.027763, 105.834160)".')),
        (3, "Sửa vĩ độ của 1 địa điểm", "P0", L(PRE, "Kho Liên Ninh (20.93, 105.85)."),
         S("Sửa HC01, đổi vĩ độ Kho Liên Ninh thành 20.94.", "Lưu, mở lịch sử."), "Vĩ độ: 20.93 -> 20.94",
         B('Có nhãn "Địa điểm chấm công hợp lệ thêm mới:" với dòng chữ xanh "- Kho Liên Ninh (20.94, 105.85)" và nhãn "Địa điểm chấm công hợp lệ đã xóa:" với dòng chữ đỏ "- Kho Liên Ninh (20.93, 105.85)".',
           "Đổi toạ độ được hiện như bỏ địa điểm cũ + thêm địa điểm mới (không có nhóm sửa thông tin).")),
        (4, "Thêm máy chấm công hợp lệ", "P0", L(PRE, "Máy chấm công hợp lệ đang có Máy LN 1."),
         S('Sửa HC01, ô "Máy chấm công hợp lệ" chọn thêm "Máy LN 2".', "Lưu, mở lịch sử."), "Máy thêm: Máy LN 2",
         B('Có nhãn "Máy chấm công hợp lệ thêm mới:" và dòng chữ xanh "- Máy LN 2" (hiện TÊN máy).')),
        (5, "Bỏ máy chấm công hợp lệ", "P0", L(PRE, "Có Máy LN 1, Máy LN 2."),
         S("Sửa HC01, bỏ Máy LN 2.", "Lưu, mở lịch sử."), "—", B('Có nhãn "Máy chấm công hợp lệ đã xóa:" và dòng chữ đỏ "- Máy LN 2".')),
        (6, "Thêm khung giờ phạt", "P0", L(PRE, "Đã tick Phạt đi làm muộn/ về sớm, có khung Đi muộn 5-10 phút trừ 1 giờ / 0.1 ngày."),
         S("Sửa HC01, bấm thêm khung phạt: Loại Về sớm, Thời gian từ 5 Đến 15, Giờ công bị trừ 1.5, Ngày công bị trừ 0.15, bấm Áp dụng.", "Lưu, mở lịch sử."),
         "Về sớm 5-15 phút, 1.5 giờ / 0.15 ngày",
         B('Có nhãn "Khung giờ phạt đi muộn/về sớm thêm mới:" và dòng chữ xanh "- Về sớm 5-15 phút ... trừ 1.5 giờ / 0.15 ngày".', "Không lặp lại khung Đi muộn đang có.")),
        (7, "Sửa khung giờ phạt", "P0", "Như TC trên.",
         S("Sửa HC01, sửa khung Đi muộn 5-10 thành Đến 12 phút.", "Lưu, mở lịch sử."), "—",
         B('Nhóm "Khung giờ phạt đi muộn/về sớm thêm mới:" có dòng chữ xanh "- Đi muộn 5-12 phút ..."; nhóm "Khung giờ phạt đi muộn/về sớm đã xóa:" có dòng chữ đỏ "- Đi muộn 5-10 phút ...".')),
        (8, "Xóa khung giờ phạt", "P0", "HC01 có 2 khung phạt.",
         S("Sửa HC01, xoá khung Về sớm 5-15.", "Lưu, mở lịch sử."), "—", B('Có nhãn "Khung giờ phạt đi muộn/về sớm đã xóa:" và dòng chữ đỏ "- Về sớm 5-15 phút ... trừ 1.5 giờ / 0.15 ngày".')),
        (9, "Lưu lại ca có khung phạt mà không đổi không sinh dòng", "P0", "HC01 có 2 khung phạt.",
         S("Sửa HC01, không đổi gì, Lưu.", "Mở lịch sử."), "—", B("Không có dòng mới (khung phạt được lưu lại y nguyên không tính là thay đổi).")),
        (10, "Chấm giờ vào / Chấm giờ ra bị khoá ở màn Sửa", "P1", PRE,
         S("Sửa HC01.", 'Bấm ô tick "Chấm vào" cạnh Giờ bắt đầu ca và "Chấm ra" cạnh Giờ kết thúc ca.'), "—",
         B("2 ô tick mờ, bấm không đổi; 2 trường Chấm giờ vào / Chấm giờ ra chỉ xuất hiện trong dòng Tạo mới hoặc Xóa.")),
    ]

    st = [
        (1, "Khóa ca từ danh sách", "P0", PRE,
         S(M_SHIFT + ".", 'Bánh răng HC01 > "Khóa", popup "Xác nhận khóa" bấm "Đồng ý".', 'Chờ "Cập nhật thành công".', "Mở lịch sử."), "—",
         B('Dòng trên cùng "Khóa" chữ cam (nhóm lọc "Thay đổi trạng thái"), có ĐÚNG 1 thay đổi: ' + chg("Trạng thái", "Hoạt động", "Khóa") + ".",
           'Cột Trạng thái trên bảng hiện "Khoá"; bánh răng đổi thành "Mở khóa".')),
        (2, "Mở khóa ca từ danh sách", "P0", "HC01 đang Khóa.",
         S('Bánh răng HC01 > "Mở khóa", "Đồng ý".', "Mở lịch sử."), "—",
         B('Dòng trên cùng "Mở khóa" chữ xanh lá (nhóm lọc "Thay đổi trạng thái"): ' + chg("Trạng thái", "Khóa", "Hoạt động") + ".")),
        (3, "Đổi Trạng thái trên form Sửa sinh dòng Khóa riêng", "P0", PRE,
         S('Sửa HC01, ô "Trạng thái" chọn "Khóa", Lưu.', "Mở lịch sử."), "—",
         B('1 dòng mới "Khóa" (chữ cam) chỉ có Trạng thái Hoạt động -> Khóa; KHÔNG có thêm dòng "Thay đổi thông tin" rỗng.')),
        (4, "Đổi Trạng thái và Tên ca cùng lần lưu sinh 2 dòng", "P1", PRE,
         S('Sửa HC01: Trạng thái = Khóa, Tên ca = "Hành chính 2", Lưu.', "Mở lịch sử."), "—",
         B('2 dòng mới cùng thời điểm: "Thay đổi thông tin" xanh dương (chỉ Tên ca) nằm TRÊN, "Khóa" chữ cam (chỉ Trạng thái) nằm dưới.')),
        (5, "Xóa ca chưa phân", "P1", "Ca CS09 chưa phân cho ai.",
         S('Bánh răng CS09 > "Xóa", popup "Cảnh báo" bấm "Xoá".'), "—",
         B('Hiện "Xoá ca làm việc thành công", ca biến mất.', 'Không còn lối mở lịch sử ca đã xoá (dòng "Xóa" chữ đỏ, nhóm lọc "Thay đổi trạng thái", được lưu nhưng không xem được trên giao diện).')),
        (6, "Ca đã phân không có mục Xóa", "P1", "Ca HC02 đã phân cho 20 nhân viên.",
         S("Bánh răng HC02."), "—", B('Không có mục "Xóa"; các mục còn lại bình thường.',
           "Ca chỉ còn nằm trong ngày phân ca cũ (bảng phân ca đã xoá) cũng tính là đã phân - không có mục Xóa.")),
        (7, "Xóa ca vừa được phân cho nhân viên bị hệ thống từ chối", "P0",
         L(TK, "Ca CS10 chưa phân cho ai; tài khoản có quyền Quản lý ca làm việc và quyền phân ca."),
         S("Tab 1: " + M_SHIFT + ", thấy bánh răng CS10 có mục Xóa (không tải lại trang).",
           "Tab 2: vào màn Phân ca, phân ca CS10 cho 1 nhân viên, lưu.",
           'Quay lại tab 1: bánh răng CS10 > "Xóa", popup "Cảnh báo" bấm "Xoá".', "Tải lại tab 1, mở lịch sử CS10."), "—",
         B('Hiện thông báo lỗi (khung đỏ) "Ca làm việc đang được phân cho nhân viên, không thể xóa."',
           "CS10 vẫn còn trong danh sách; sau khi tải lại, bánh răng CS10 KHÔNG còn mục Xóa.",
           "Lịch sử CS10 KHÔNG có dòng \"Xóa\".")),
    ]

    sec8 = [
        (1, "Sửa ca bấm Lưu không đổi gì không sinh dòng", "P0", PRE,
         S("Sửa HC01, không đổi gì, Lưu.", "Mở lịch sử."), "—", B("Không có dòng \"Thay đổi thông tin\" mới.")),
        (2, "Lưu thiếu Tên ca bị chặn", "P0", PRE,
         S('Sửa HC01, xoá trống "Tên ca", Lưu.'), "Tên ca: trống",
         B('Dưới ô hiện "Bắt buộc nhập"; vẫn ở màn Sửa; không có dòng lịch sử.')),
        (3, "Lưu Mã ca trùng bị chặn", "P0", "Đã có ca mã CA2.",
         S('Sửa HC01, Mã ca = "CA2", Lưu.'), "Mã ca: CA2", B('Dưới ô Mã ca hiện "Đã tồn tại"; không sinh dòng.')),
        (4, "Chấm vào đến nhỏ hơn Chấm vào từ bị chặn", "P1", PRE,
         S("Sửa HC01, Chấm vào Từ 09:00 Đến 07:00, Lưu."), "—", B('Hiện "Thời gian đến phải lớn hơn từ"; không lưu, không sinh dòng.')),
        (5, "Ca đã phân vẫn sửa được mọi trường, lịch sử ghi đúng", "P1", "Ca HC02 đã phân cho nhân viên.",
         S("Sửa HC02, đổi Giờ bắt đầu ca và Giờ công, Lưu.", "Mở lịch sử HC02."), "Giờ bắt đầu ca: 08:00 -> 08:30",
         B("Các ô giờ và cài đặt KHÔNG bị khoá dù ca đã được phân (đã chốt: không khoá).",
           "Lưu thành công.",
           "Lịch sử có đúng 1 dòng mới, chỉ ghi những trường thật sự đổi (Giờ bắt đầu ca, Giờ công).")),
    ]

    sec11 = [
        (1, "Mở Sửa rồi Lưu không đổi thì Giờ công giữ nguyên", "P0",
         L(TK, "Ca HC03 08:00 - 17:00, nghỉ 12:00 - 13:00, Giờ công đã chỉnh tay = 7.5 (khác 8 tự tính)."),
         S("Sửa HC03, không đổi gì, Lưu.", "Mở lại Sửa HC03 quan sát Giờ công.", "Mở lịch sử."), "—",
         B("Giờ công vẫn là 7.5 (không bị tính lại thành 8).", "Không có dòng lịch sử mới.")),
        (2, "Giờ công chỉ tính lại khi đổi giờ", "P0", "Như trên.",
         S("Sửa HC03, đổi Giờ kết thúc ca 17:00 sang 17:30, Lưu.", "Mở lịch sử."), "—",
         B("Giờ công tự tính lại theo giờ mới (8.5).", "Dòng lịch sử có Giờ kết thúc ca và Giờ công.")),
        (3, "Số giờ công bị trừ của khung giờ phạt nhận số lẻ", "P0", L(PRE, "Đã tick Phạt đi làm muộn/ về sớm."),
         S("Sửa HC01, thêm khung phạt Đi muộn 1-5 phút, Giờ công bị trừ 1.5, Ngày công bị trừ 0.15, Áp dụng.", "Lưu, mở lại Sửa, mở lịch sử."), "Giờ công bị trừ: 1.5",
         B("Bảng khung phạt hiện Giờ công bị trừ (giờ) = 1.5 (không bị làm tròn thành 2 hay 1).", "Lịch sử ghi \"... trừ 1.5 giờ / 0.15 ngày\".")),
        (4, "Số trong lịch sử bỏ số 0 thừa và theo chuẩn quốc tế", "P1", PRE,
         S("Sửa HC01: Giờ công 8 thành 7.5, Ngày công 1 thành 0.75, Lưu.", "Mở lịch sử."), "—",
         B('Hiện "8" -> "7.5" và "1" -> "0.75" (không hiện 8.00, 1.000).')),
        (5, "Ô tick hiện Có/Không, mũi tên xám", "P1", PRE,
         S("Tick Ca đêm, Lưu, mở lịch sử."), "—", B('"Ca đêm: Không" -> "Có"; mũi tên xám, cũ đỏ, mới xanh.')),
        (7, 'Màn Sửa ca có tiêu đề "Sửa ca làm việc"', "P1", PRE,
         S(M_SHIFT + ".", "Bánh răng dòng HC01 > Sửa, quan sát tiêu đề trang, tiêu đề khối bên trái và tên tab trình duyệt.",
           'Quay lại danh sách, bấm "Thêm mới", quan sát lại.'), "—",
         B('Màn Sửa: cả 3 chỗ ghi "Sửa ca làm việc" (KHÔNG còn ghi "Thêm ca làm việc").', 'Màn Thêm mới: cả 3 chỗ ghi "Thêm ca làm việc".')),
        (6, "Tài khoản không có quyền xem danh mục ca không thấy màn và lịch sử", "P0", L(TK_B, "Có địa chỉ màn Danh mục ca làm việc."),
         S("Đăng nhập B, dán địa chỉ màn."), "—", B("Bị chuyển sang trang " + NOT_FOUND + ".")),
    ]

    sections = [
        ("I", "HIỂN THỊ TRANG & TRUY CẬP (GỒM DÒNG TẠO MỚI)", sec1),
        ("II", "POPUP LỊCH SỬ CA LÀM VIỆC: BỐ CỤC & BỘ LỌC", sec2),
        ("III", "KHỐI LỊCH SỬ TRONG MÀN SỬA CA LÀM VIỆC", sec3),
        ("IV", "GHI LỊCH SỬ TỪNG TRƯỜNG KHI SỬA CA", f),
        ("V", "ĐỊA ĐIỂM / MÁY CHẤM CÔNG / KHUNG GIỜ PHẠT", lst),
        ("VI", "KHÓA / MỞ KHÓA / XÓA CA", st),
        ("VIII", "RÀNG BUỘC NHẬP LIỆU", sec8),
        ("XI", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", sec11),
    ]
    return desc, roles, sections


# ======================================================================
def main():
    jobs = [
        ("Lịch sử Quy định chung", "Quy định chung", quy_dinh_chung),
        ("Lịch sử Quy định làm thêm", "Quy định làm thêm", quy_dinh_lam_them),
        ("Lịch sử Quy định nghỉ", "Quy định nghỉ", quy_dinh_nghi),
        ("Lịch sử Cài đặt", "Cài đặt", cai_dat),
        ("Lịch sử Ca làm việc", "Ca làm việc", ca_lam_viec),
    ]
    grand = 0
    for screen, module, fn in jobs:
        desc, roles, sections = fn()
        out = os.path.join(HERE, "testcase - %s.xlsx" % screen)
        print("=" * 70)
        grand += build(output_file=out, sheet_name="Trang tính1",
                       feature_name="Lịch sử thay đổi - %s - Cập nhật ngày 30/09/2026" % screen.replace("Lịch sử ", ""),
                       module_name=module, description_block=desc, role_tcs=roles, sections=sections)
    print("=" * 70)
    print("TONG CONG:", grand, "TC")


if __name__ == "__main__":
    main()
