# -*- coding: utf-8 -*-
"""Testcase Redmine #10455 - nhom hang muc 5 (Phan quyen), 6 (Nguoi dung),
10 (Cau hinh HCNS), 11 (Cau hinh chung giao viec).

Xuat 4 file:
  testcase - Lich su Phan quyen.xlsx
  testcase - Lich su Nguoi dung.xlsx
  testcase - Lich su Cau hinh HCNS.xlsx
  testcase - Lich su Cau hinh giao viec.xlsx

Chay: /opt/homebrew/opt/python@3.14/bin/python3.14 tc_quyen_hcns_giaoviec.py
Noi dung bam code nhanh task_10455 (worktrees/task_10455-api + task_10455-client).
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


def L(*lines):
    """Ghep nhieu y thanh nhieu dong that trong 1 o."""
    return "\n".join(x for x in lines if x is not None)


def S(*steps):
    """Danh so buoc 1. 2. 3. moi buoc 1 dong."""
    return "\n".join("%d. %s" % (i, s) for i, s in enumerate(steps, start=1))


def E(*items):
    """Expected: moi y 1 dong, gach dau dong."""
    return "\n".join("- " + x for x in items)


def diff(label, old, new):
    return "dòng '%s:' giá trị cũ %s (chữ đỏ) -> mũi tên -> giá trị mới %s (chữ xanh)" % (label, old, new)


def new_only(label, new):
    """Truong truoc do trong: khung chung chi in gia tri moi, khong in '(trong) ->'."""
    return "dòng '%s:' chỉ có giá trị mới %s (chữ xanh), KHÔNG có giá trị cũ và mũi tên" % (label, new)


def group(label, *rows):
    """Khoi danh sach: nhan nhom + moi phan tu 1 dong gach dau."""
    return "nhóm '%s:' gồm %s" % (label, ", ".join("dòng '- %s'" % r for r in rows))


EMPTY_TEXT = "Chưa có lịch sử thao tác nào."
NO_MATCH = "Không có lịch sử phù hợp bộ lọc."
GROUPS3 = "'Tạo mới', 'Thay đổi thông tin', 'Thay đổi trạng thái'"


def popup_layout(title, *extra):
    return E("Popup mở ra: đầu popup có biểu tượng đồng hồ, tiêu đề '%s', dấu X ở góc phải" % title,
             "KHÔNG có dòng mô tả phụ dưới tiêu đề",
             "Thân popup: nút 'Bộ lọc' ở góc phải trên (khối lọc thu gọn sẵn), bên dưới là dòng thời gian các lần thay đổi",
             "Chân popup chỉ có nút 'Đóng'",
             *extra)


def filter_tcs(n, pre, steps, counts, performer, perf_count, dates, extra_group=None):
    """7 TC bo loc chuan cua khung lich su chung (moi o 1 TC).

    counts: dict {'Tạo mới': x, 'Thay đổi thông tin': y, 'Thay đổi trạng thái': z}
    dates: (ngay_som, ngay_giua, ngay_muon) theo dd/mm/yyyy, moi ngay dung 1 muc
    """
    d1, d2, d3 = dates
    total = sum(counts.values())
    cnt = "; ".join("%s: %d mục" % (k, v) for k, v in counts.items())
    pre_c = L(pre, "Đang có %d mục lịch sử (%s)" % (total, cnt))
    pre_d = L(pre, "Có 3 mục ở 3 ngày %s, %s, %s" % dates)
    res_group = [("Chọn '%s': còn đúng %d mục" % (k, v)) if v else ("Chọn '%s': không còn mục nào, hiện '%s'" % (k, NO_MATCH))
                 for k, v in counts.items()]
    return [
        (n, "Khối bộ lọc đủ 4 ô, lọc ngay khi chọn, không có nút Tìm kiếm", "P0", pre_c,
         S(*steps + ["Bấm nút 'Bộ lọc'"]), "—",
         E("Khối lọc mở ra gồm theo thứ tự: 'Loại hành động', 'Người thực hiện', 'Từ ngày', 'Đến ngày'",
           "Ô chọn ghi sẵn 'Chọn loại hành động' / 'Chọn người thực hiện'; ô ngày ghi 'Từ ngày' / 'Đến ngày', dạng dd/mm/yyyy",
           "Dưới cùng bên phải chỉ có nút 'Làm mới', KHÔNG có nút 'Tìm kiếm'",
           "KHÔNG còn các ô lọc cũ 'Thao tác', 'Trường', 'Nhóm cấu hình'",
           "Bấm 'Bộ lọc' lần nữa thì khối lọc thu gọn")),
        (n + 1, "Lọc theo Loại hành động (3 nhóm cố định)", "P0", pre_c,
         S(*steps + ["Bấm 'Bộ lọc', mở ô 'Loại hành động'", "Lần lượt chọn từng lựa chọn (không bấm nút nào khác)"]),
         "Loại hành động: lần lượt 3 lựa chọn",
         E(*["Ô có ĐÚNG 3 lựa chọn theo thứ tự %s, giống nhau ở mọi màn" % GROUPS3,
             "Chọn xong danh sách lọc NGAY, không cần bấm nút"] + res_group
           + ([extra_group] if extra_group else []))),
        (n + 2, "Lọc theo Người thực hiện", "P1", L(pre, "%s đã thực hiện đúng 1 mục; nhân viên 'Kế toán Không Sửa' chưa từng thay đổi gì" % performer),
         S(*steps + ["Bấm 'Bộ lọc', mở ô 'Người thực hiện'", "Gõ tìm rồi chọn '%s'" % performer, "Đổi sang chọn 'Kế toán Không Sửa'"]),
         "Người thực hiện: %s" % performer,
         E("Ô liệt kê ĐỦ nhân sự đang làm việc của %s (không chỉ người đã từng sửa), mỗi dòng dạng 'MÃ PHÒNG - Họ tên', xếp theo A-Z" % perf_count,
           "Chọn %s: còn đúng 1 mục của người đó" % performer,
           "Chọn 'Kế toán Không Sửa': hiện '%s'" % NO_MATCH)),
        (n + 3, "Lọc theo Từ ngày (tính cả ngày biên)", "P1", pre_d,
         S(*steps + ["Bấm 'Bộ lọc', ô 'Từ ngày' chọn %s" % d2]), "Từ ngày: %s" % d2,
         E("Lọc ngay sau khi chọn ngày", "Còn 2 mục ngày %s và %s (tính cả ngày %s)" % (d2, d3, d2), "Mục ngày %s bị ẩn" % d1)),
        (n + 4, "Lọc theo Đến ngày (tính cả ngày biên)", "P1", pre_d,
         S(*steps + ["Bấm 'Bộ lọc', ô 'Đến ngày' chọn %s" % d2]), "Đến ngày: %s" % d2,
         E("Còn 2 mục ngày %s và %s (tính cả ngày %s)" % (d1, d2, d2), "Mục ngày %s bị ẩn" % d3,
           "Chọn thêm Từ ngày %s: chỉ còn mục ngày %s" % (d2, d2))),
        (n + 5, "Làm mới xoá toàn bộ điều kiện lọc", "P1", pre_c,
         S(*steps + ["Bấm 'Bộ lọc', chọn Loại hành động 'Thay đổi thông tin', chọn 1 người thực hiện, chọn Từ ngày", "Bấm 'Làm mới'"]), "—",
         E("Cả 4 ô trở về trống (ô chọn hiện lại 'Tất cả ...')", "Danh sách hiện lại đủ %d mục" % total)),
        (n + 6, "Từ ngày lớn hơn Đến ngày / đóng rồi mở lại", "P2", pre_d,
         S(*steps + ["Bấm 'Bộ lọc', Từ ngày %s, Đến ngày %s" % (d3, d1), "Bấm 'Đóng', mở lại lịch sử của đúng bản ghi đó"]),
         L("Từ ngày: %s" % d3, "Đến ngày: %s" % d1),
         E("Bước 4: hiện biểu tượng phễu gạch và dòng '%s', không báo lỗi hệ thống" % NO_MATCH,
           "Mở lại: khối lọc thu gọn, các ô trống, hiện đủ mọi mục")),
    ]


def out(name):
    return os.path.join(HERE, "testcase - %s.xlsx" % name)


# =====================================================================================
# Menu / quyen dung chung
# =====================================================================================
MENU_ROLES = "Vào phân hệ Quản trị hệ thống -> nhóm 'Người dùng & phân quyền' -> bấm 'Danh sách phân quyền'"
MENU_USERS = "Vào phân hệ Quản trị hệ thống -> nhóm 'Người dùng & phân quyền' -> bấm 'Danh sách người dùng'"
MENU_SALARY = "Vào phân hệ Tính lương -> trên thanh menu ngang bấm 'Cấu hình tiền lương'"
MENU_MANPOWER = "Vào phân hệ Quản trị hệ thống -> nhóm 'Cài đặt chung' -> bấm 'Cấu hình định biên nhân sự'"
MENU_INSURANCE = "Vào phân hệ Bảo hiểm -> nhóm 'Cấu hình' -> bấm 'Tỉ lệ đóng BHXH'"
MENU_ASSIGN = ("Vào phân hệ Công việc -> nhóm 'Thiết lập' -> bấm "
               "'Cấu hình chung (Quy chế thu nhập kỹ thuật - công nghệ)'")
MENU_PRICE = "Vào phân hệ Bán hàng -> nhóm 'Quy chế - Thiết lập' -> mục 'Thiết lập' -> bấm 'Cấu hình duyệt giá'"

Q_ROLE = "'Quản lý phân quyền'"
Q_TS = "'Thiết lập thông số'"
Q_TSL = "'Thiết lập thông số lương'"
Q_ASSIGN = "'Cấu hình phân hệ giao việc/ công tác'"

ACC = L("Tài khoản QT1 (họ tên: Nguyễn Văn Quản Trị) có quyền %s, đang làm việc ở Công ty A" % Q_ROLE,
        "Tài khoản QT2 (họ tên: Trần Thị Kiểm Thử) có cùng quyền, cùng Công ty A")

BLOCKED = ("hệ thống chuyển sang trang 'KHÔNG TÌM THẤY TRANG YÊU CẦU' (dòng 'Không tìm thấy hoặc không được cấp quyền truy cập trang', "
           "nút 'Về trang chủ'), KHÔNG hiện dữ liệu của màn")

TIMELINE_COMMON = [
    "Mỗi lần thay đổi là 1 mục trên dòng thời gian, mục MỚI NHẤT nằm TRÊN CÙNG",
    "Mỗi mục theo thứ tự: thời gian dạng dd/mm/yyyy hh:mm (không có giây) -> tên hành động tô màu"
    " theo BỘ NHÃN CHUẨN dùng chung: 'Tạo mới' (xanh lá), 'Thay đổi thông tin' (xanh dương), 'Khóa' (cam), 'Mở khóa' (xanh lá),"
    " 'Xóa' (đỏ), 'Thay đổi trạng thái' (cam) -> dòng 'Người thực hiện: <họ tên> — <tên phòng ban>' -> khối thay đổi",
    "Trường thường ghi '<Tên trường>: giá trị cũ (chữ đỏ) -> mũi tên -> giá trị mới (chữ xanh)'",
]

# Mo ta chung dung cho muc 4 / muc 9 cua ca 4 sheet
FILTER_DESC = L("Bộ lọc trong popup / khối Lịch sử (bấm 'Bộ lọc'): 'Loại hành động' (đúng 3 nhóm: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái),",
                "'Người thực hiện' (đủ nhân sự công ty, dạng 'MÃ PHÒNG - Họ tên'), 'Từ ngày', 'Đến ngày' so theo NGÀY thực hiện, tính cả 2 ngày biên.",
                "Chọn giá trị là lọc NGAY, không có nút Tìm kiếm; nút 'Làm mới' xoá mọi điều kiện.")
GROUP_RULE = ("Nhóm lọc: tạo mới / thêm dòng -> 'Tạo mới'; sửa trường, thêm / bớt phần tử danh sách, đổi thứ tự -> 'Thay đổi thông tin'; "
              "xoá (và khoá / mở khoá nếu có) -> 'Thay đổi trạng thái'. Tên hành động từng mục là nhãn chuẩn 'Tạo mới' (xanh lá) / "
              "'Thay đổi thông tin' (xanh dương) / 'Khóa' (cam) / 'Mở khóa' (xanh lá) / 'Xóa' (đỏ) / 'Thay đổi trạng thái' (cam); "
              "KHÔNG còn nhãn riêng từng màn (vd 'Cập nhật phân quyền', 'Tạo mới chức vụ', 'Đổi thứ tự ưu tiên').")
LAYOUT_NOTE = L("- Mọi popup lịch sử dùng CHUNG 1 khuôn: tiêu đề 'Lịch sử thay đổi: <nhãn>', nút 'Bộ lọc', dòng thời gian mới -> cũ, chân popup chỉ có 'Đóng'",
                "- Trường trước đó trống: chỉ hiện giá trị mới (không có '(trống) ->'); giá trị mới trống ghi '(trống)'",
                "- Chưa có lịch sử: biểu tượng đồng hồ + '%s' (không có nút Bộ lọc); lọc không ra: '%s'" % (EMPTY_TEXT, NO_MATCH),
                "- Danh sách / bảng con hiển thị theo NHÓM có nhãn '... thêm mới:' (chữ xanh), '... đã xóa:' (chữ đỏ), '... sửa thông tin:' (tên dòng + trường cũ -> mới), mỗi phần tử 1 dòng gạch đầu",
                "- Dòng quá dài (hơn 200 ký tự) bị cắt kèm liên kết 'Xem thêm' / 'Thu gọn'")


# =====================================================================================
# FILE 1 - LICH SU PHAN QUYEN (CHUC VU)
# =====================================================================================
def build_roles():
    open_list = S(MENU_ROLES,
                  "Tại dòng chức vụ 'Kế toán tổng hợp KT' bấm nút bánh răng ở cột Hành động",
                  "Bấm 'Lịch sử thay đổi'")
    list_steps = [MENU_ROLES, "Tại dòng 'Kế toán tổng hợp KT' bấm bánh răng -> 'Lịch sử thay đổi'"]
    role_pre = L(ACC,
                 "Chức vụ 'Kế toán tổng hợp KT' (ID 120): áp dụng Công ty A, Vị trí 5, Ghi chú 'Nhóm kế toán',",
                 "đang có quyền 'Xem' ở thẻ 'Mẫu bảng lương' (Phân hệ tính lương)")
    TITLE = "Lịch sử thay đổi: Kế toán tổng hợp KT"

    def edit_steps(action, save="Bấm 'Lưu' ở chân trang"):
        return S(MENU_ROLES,
                 "Dòng 'Kế toán tổng hợp KT' -> bánh răng -> 'Sửa'",
                 action,
                 save,
                 "Quay lại danh sách, dòng 'Kế toán tổng hợp KT' -> bánh răng -> 'Lịch sử thay đổi'")

    def perm_row(right, module, part):
        return "%s — Phân hệ: %s; Phần: %s" % (right, module, part)

    desc = [
        ("1. Mục đích tính năng",
         L("Ghi lại và cho xem lịch sử thay đổi của từng chức vụ (nhóm quyền) ở màn Danh sách phân quyền:",
           "ai tạo / sửa / xoá chức vụ nào, lúc nào, đổi từ giá trị gì sang giá trị gì.",
           "Xem được ở 2 nơi, cùng 1 nội dung và cùng bộ lọc:",
           "- Popup 'Lịch sử thay đổi: <Tên chức vụ>' mở từ dropdown thao tác của từng dòng trong danh sách",
           "- Khối 'Lịch sử' nằm cuối thân màn Chỉnh sửa chức vụ (mặc định thu gọn, bấm 'Xem lịch sử' mới tải) — thay cho nút 'Lịch sử' ở chân trang trước đây")),
        ("2. Đối tượng được tính / hiển thị",
         L("Các thao tác sinh 1 mục lịch sử:",
           "- Tạo mới chức vụ (tên hành động 'Tạo mới', chữ xanh lá, nhóm lọc Tạo mới): liệt kê thông tin lúc tạo (bỏ trường trống)",
           "- Sửa chức vụ có thay đổi ('Thay đổi thông tin', chữ xanh dương, nhóm lọc Thay đổi thông tin): chỉ hiện phần thay đổi",
           "- Xoá chức vụ ('Xóa', chữ đỏ, nhóm lọc Thay đổi trạng thái): ghi nhận thông tin trước khi xoá",
           "Trường thường: Tên chức vụ, Ghi chú, Vị trí. Danh sách: 'Công ty thêm mới / đã xóa' (công ty áp dụng),",
           "'Quyền thêm mới (<Tên công ty>) / Quyền đã xóa (<Tên công ty>)' — mỗi quyền 1 dòng '<Tên quyền> — Phân hệ: <tên phân hệ>; Phần: <tên phần>'.")),
        ("3. Đối tượng bị ẩn / không tính",
         L("- Bấm Lưu mà không đổi gì: KHÔNG sinh mục lịch sử",
           "- Lưu bị chặn do thiếu Tên chức vụ / thiếu Công ty: KHÔNG sinh mục",
           "- Xoá bị chặn vì đã có nhân viên nhận chức vụ: KHÔNG sinh mục",
           "- Mục cập nhật cũ không còn thay đổi nào hiển thị được: bị ẩn, không hiện mục rỗng",
           "- Chức vụ không áp dụng cho công ty đang làm việc: không có trên danh sách, không xem được lịch sử")),
        ("4. Bộ lọc thời gian áp dụng cho", L(FILTER_DESC, GROUP_RULE)),
        ("5. Cấu trúc dữ liệu / cây phân cấp",
         L("Chi tiết phân quyền hiển thị theo NHÓM từng công ty: 'Quyền thêm mới (<Tên công ty>):' / 'Quyền đã xóa (<Tên công ty>):',",
           "mỗi quyền 1 dòng '- <Tên quyền> — Phân hệ: Phân hệ <tên>; Phần: <tên thẻ>' (thay cho cây Công ty -> Phân hệ -> Phần -> chip quyền trước đây).",
           "Tên phân hệ theo danh sách phân hệ hiện hành: Phân hệ chấm công, Phân hệ tính lương, Phân hệ hành chính nhân sự, Phân hệ giao việc,",
           "Phân hệ meeting, Phân hệ an toàn - 5S, Phân hệ CSKH trước bán, Phân hệ danh mục chung, Phân hệ quản trị hệ thống...",
           "Quyền chưa thuộc phân hệ nào ghi 'Phân hệ: Chưa phân loại phân hệ'.")),
        ("6. Quy tắc cộng dồn / deduplicate",
         L("- Mỗi lần bấm Lưu có thay đổi = đúng 1 mục, gom tất cả trường đổi trong lần đó",
           "- Trong 1 nhóm, quyền xếp theo phân hệ -> phần -> tên quyền",
           "- Tick rồi bỏ tick cùng 1 quyền trước khi Lưu coi như không đổi")),
        ("7. Phân quyền cấp",
         L("Quyền 'Quản lý phân quyền': thấy menu Danh sách phân quyền, vào được màn danh sách + Thêm/Sửa, xem được popup và khối Lịch sử.",
           "Không có quyền riêng cho việc xem lịch sử: ai vào được màn là xem được lịch sử.",
           "Không có quyền: không thấy menu, mở lại màn bị chuyển sang trang không tìm thấy.")),
        ("8. Cách tính các ô thống kê",
         "Không áp dụng. Riêng khối 'Lịch sử' ở màn Sửa có ô số nhỏ cạnh chữ 'Lịch sử' = tổng số mục lịch sử (sau khi đã tải)."),
        ("9. Ghi chú đọc bảng",
         L(LAYOUT_NOTE,
           "- Màn Chỉnh sửa chức vụ: chân trang chỉ còn 'Lưu', 'Quay lại' (KHÔNG còn nút 'Lịch sử'); màn Thêm mới KHÔNG có khối Lịch sử",
           "- Lưu ý: chức vụ đã xoá không còn trên danh sách nên mục 'Xóa' của chức vụ hiện chưa có chỗ xem trên giao diện (đã ghi nhận để chốt)",
           "- Phân quyền hàng loạt KHÔNG thuộc phạm vi lịch sử của màn này",
           "- Hộp thoại xoá chức vụ: tiêu đề 'Cảnh báo', câu hỏi 'Bạn có chắc chắn muốn xóa không?', 2 nút 'Huỷ' / 'Xoá'",
           "- Lưu ý: khối 'Phân hệ chấm công' trên màn Sửa chức vụ hiện ghi 'Phân hệ này chưa khai báo quyền nào' (đang chờ chốt),",
           "  nên các TC dùng quyền của Phân hệ tính lương / giao việc / CSKH sau bán để thao tác tick quyền")),
    ]

    roles = [
        ("01", "Có quyền 'Quản lý phân quyền' thấy menu và nút Lịch sử", "P0",
         L("Tài khoản QT1 có quyền %s" % Q_ROLE, "Công ty A có ít nhất 3 chức vụ"),
         S("Đăng nhập tài khoản QT1", MENU_ROLES, "Bấm bánh răng ở 1 dòng bất kỳ"),
         "—",
         E("Menu 'Danh sách phân quyền' hiển thị trong nhóm 'Người dùng & phân quyền'",
           "Màn 'Phân quyền' mở được, có dữ liệu",
           "Dropdown có 3 mục theo thứ tự: 'Sửa', 'Lịch sử thay đổi', 'Xóa'")),
        ("02", "Không có quyền 'Quản lý phân quyền' không thấy menu", "P0",
         "Tài khoản NV1 KHÔNG có quyền %s" % Q_ROLE,
         S("Đăng nhập tài khoản NV1", "Mở phân hệ Quản trị hệ thống", "Quan sát nhóm 'Người dùng & phân quyền'"),
         "—",
         E("KHÔNG có mục 'Danh sách phân quyền'",
           "KHÔNG có mục 'Danh sách người dùng'",
           "Nếu NV1 cũng không có quyền xem Tài khoản nhân viên thì cả nhóm 'Người dùng & phân quyền' bị ẩn khỏi menu")),
        ("03", "Không có quyền mở lại màn Danh sách phân quyền bị chặn", "P0",
         L("Tài khoản NV1 trước đây có quyền, đã mở màn Danh sách phân quyền",
           "Quản trị gỡ quyền %s khỏi NV1" % Q_ROLE),
         S("NV1 đăng xuất rồi đăng nhập lại",
           "Mở lại màn Danh sách phân quyền từ lịch sử duyệt web của trình duyệt (nút Quay lại / danh sách trang đã xem)"),
         "—",
         E(BLOCKED, "Không mở được popup lịch sử của bất kỳ chức vụ nào")),
        ("04", "Không có quyền mở lại màn Chỉnh sửa chức vụ bị chặn", "P0",
         L("Như TC-ROLE-03, NV1 trước đó đã mở màn Chỉnh sửa chức vụ 'Kế toán tổng hợp KT'"),
         S("NV1 đăng nhập lại", "Mở lại màn Chỉnh sửa chức vụ từ lịch sử duyệt web"),
         "—",
         E(BLOCKED, "Không thấy khối 'Lịch sử' của chức vụ")),
        ("05", "Cấp lại quyền thì thấy lại menu và lịch sử", "P1",
         "NV1 đã bị gỡ quyền như TC-ROLE-03",
         S("Quản trị cấp lại chức vụ có quyền %s cho NV1" % Q_ROLE, "NV1 đăng xuất, đăng nhập lại", MENU_ROLES,
           "Mở 'Lịch sử thay đổi' của 1 chức vụ"),
         "—",
         E("Menu hiện lại", "Popup lịch sử mở được, dữ liệu đầy đủ như tài khoản QT1 xem")),
        ("06", "Chỉ thấy chức vụ áp dụng cho công ty đang làm việc", "P1",
         L("QT1 được làm việc ở Công ty A và Công ty B",
           "Chức vụ 'Kế toán tổng hợp KT' chỉ áp dụng Công ty A; chức vụ 'Kho B' chỉ áp dụng Công ty B"),
         S("QT1 đang ở Công ty A, mở Danh sách phân quyền",
           "Đổi công ty làm việc sang Công ty B (ô chọn công ty trên thanh trên cùng)",
           "Mở lại Danh sách phân quyền"),
         "—",
         E("Ở Công ty A thấy 'Kế toán tổng hợp KT', không thấy 'Kho B'",
           "Ở Công ty B thấy 'Kho B', không thấy 'Kế toán tổng hợp KT'",
           "Lịch sử mở từ dòng nào chỉ là lịch sử của đúng chức vụ đó")),
        ("07", "Mở màn Sửa chức vụ của công ty khác từ lịch sử trình duyệt", "P1",
         L("QT1 đã mở màn Sửa 'Kế toán tổng hợp KT' khi ở Công ty A", "Sau đó đổi công ty sang Công ty B"),
         S("Mở lại màn Sửa 'Kế toán tổng hợp KT' từ lịch sử duyệt web"),
         "—",
         E("Hệ thống báo 'Chức vụ này không thuộc công ty hiện tại'",
           "Tự quay về màn Danh sách phân quyền, KHÔNG hiện form trắng, KHÔNG tải được lịch sử của chức vụ đó")),
    ]

    s1 = [
        (1, "Bố cục popup mở từ danh sách", "P0", role_pre, open_list, "—",
         popup_layout(TITLE, "Tiêu đề chỉ ghép TÊN chức vụ (không kèm mã / ID)")),
        (2, "Khối 'Lịch sử' trong thân màn Chỉnh sửa chức vụ", "P0", role_pre,
         S(MENU_ROLES, "Dòng 'Kế toán tổng hợp KT' -> bánh răng -> 'Sửa'", "Cuộn xuống cuối nội dung, quan sát khối 'Lịch sử'",
           "Bấm 'Xem lịch sử'"),
         "—",
         E("Khối 'Lịch sử' (biểu tượng đồng hồ) nằm ngay dưới mục 'Chi tiết phân quyền', trên chân trang",
           "Mặc định THU GỌN, bên phải chỉ có nút 'Xem lịch sử'; chưa tải dữ liệu cho tới khi bấm",
           "Bấm 'Xem lịch sử': hiện vòng xoay tải rồi hiện dòng thời gian; cạnh chữ 'Lịch sử' có ô số = tổng số mục",
           "Bên phải đổi thành 2 nút 'Làm mới' và 'Thu gọn'",
           "Nội dung, nút 'Bộ lọc' và cách hiển thị GIỐNG HỆT popup mở từ danh sách")),
        (3, "Chân màn Chỉnh sửa chức vụ không còn nút Lịch sử", "P0", role_pre,
         S(MENU_ROLES, "Dòng 'Kế toán tổng hợp KT' -> bánh răng -> 'Sửa'", "Quan sát chân trang"), "—",
         E("Tiêu đề màn 'Chỉnh sửa chức vụ'", "Chân trang chỉ có 'Lưu' và 'Quay lại'",
           "KHÔNG còn nút 'Lịch sử' ở chân trang")),
        (4, "Màn Thêm mới chức vụ không có khối Lịch sử", "P1", ACC,
         S(MENU_ROLES, "Bấm 'Thêm mới'", "Cuộn xuống cuối màn"), "—",
         E("Tiêu đề màn 'Thêm mới chức vụ'", "KHÔNG có khối 'Lịch sử'", "Chân trang chỉ có 'Lưu' và 'Quay lại'")),
        (5, "Chức vụ chưa có lịch sử", "P1",
         L(ACC, "Chức vụ 'Bảo vệ cũ' tạo từ trước khi có tính năng lịch sử, chưa sửa lần nào"),
         S(MENU_ROLES, "Dòng 'Bảo vệ cũ' -> bánh răng -> 'Lịch sử thay đổi'", "Vào màn Sửa 'Bảo vệ cũ', bấm 'Xem lịch sử' ở khối Lịch sử"), "—",
         E("Popup và khối đều hiện biểu tượng đồng hồ và dòng '%s'" % EMPTY_TEXT,
           "KHÔNG hiện nút 'Bộ lọc'")),
        (6, "Thứ tự và thông tin từng mục trên dòng thời gian", "P0",
         L(role_pre, "Chức vụ đã có 3 lần thay đổi: QT1 tạo 01/09/2026 08:00, QT2 sửa 10/09/2026 09:15, QT1 sửa 20/09/2026 14:30",
           "QT1 thuộc 'Phòng Quản trị', QT2 thuộc 'Phòng Kiểm thử'"),
         open_list, "—",
         E(*TIMELINE_COMMON + [
             "Mục trên cùng: '20/09/2026 14:30', 'Thay đổi thông tin' chữ xanh dương, 'Người thực hiện: Nguyễn Văn Quản Trị — Phòng Quản trị'",
             "Mục giữa: '10/09/2026 09:15', 'Người thực hiện: Trần Thị Kiểm Thử — Phòng Kiểm thử'",
             "Mục dưới cùng: '01/09/2026 08:00', 'Tạo mới' chữ xanh lá"])),
        (7, "Mở lịch sử của 2 chức vụ liên tiếp không bị lẫn dữ liệu", "P1",
         L(role_pre, "Chức vụ 'Thủ kho KT' có 1 mục 'Tạo mới'"),
         S(MENU_ROLES, "Mở lịch sử 'Kế toán tổng hợp KT', bấm 'Đóng'", "Mở lịch sử 'Thủ kho KT'"), "—",
         E("Popup thứ 2 có tiêu đề 'Lịch sử thay đổi: Thủ kho KT'", "Chỉ hiện 1 mục 'Tạo mới' của 'Thủ kho KT'",
           "KHÔNG còn mục nào của 'Kế toán tổng hợp KT'")),
        (8, "Người thực hiện không có họ tên", "P2",
         L(role_pre, "Tài khoản QT3 chưa khai họ tên trong hồ sơ, email qt3@congtya.vn, đã sửa chức vụ 1 lần"),
         open_list, "—",
         E("Mục do QT3 thực hiện ghi 'Người thực hiện: Hệ thống'", "Không bỏ trống, không hiện chữ lạ",
           "Lưu ý: khung chung không còn hiện email thay họ tên như popup cũ (đã ghi nhận để chốt)")),
        (9, "Đóng popup bằng nút Đóng và dấu X", "P2", role_pre,
         S(*list_steps + ["Bấm 'Đóng'", "Mở lại, bấm dấu X góc phải trên"]), "—",
         E("Cả 2 cách đều đóng popup", "Màn danh sách giữ nguyên trang và bộ lọc đang xem")),
        (10, "Thu gọn / Làm mới khối Lịch sử ở màn Sửa", "P2", role_pre,
         S(MENU_ROLES, "Dòng 'Kế toán tổng hợp KT' -> 'Sửa'", "Bấm 'Xem lịch sử'", "Bấm 'Làm mới'", "Bấm 'Thu gọn', rồi bấm 'Xem lịch sử' lần nữa"), "—",
         E("'Làm mới' tải lại danh sách, các ô lọc về trống", "'Thu gọn' ẩn nội dung, còn nút 'Xem lịch sử'",
           "Mở lại lần 2 không tải lại từ đầu, nội dung giữ như trước khi thu gọn",
           "Các ô đang nhập trên form KHÔNG bị ảnh hưởng")),
    ]

    s2 = filter_tcs(1, role_pre, list_steps,
                    {"Tạo mới": 1, "Thay đổi thông tin": 2, "Thay đổi trạng thái": 0},
                    "'QTR - Trần Thị Kiểm Thử'", "Công ty A", ("01/09/2026", "10/09/2026", "20/09/2026"),
                    extra_group="Chọn 'Thay đổi thông tin' thấy cả mục chỉ thêm / bỏ công ty hoặc quyền (thêm bớt phần tử danh sách thuộc nhóm này)")
    s2 += [
        (8, "Mục 'Xóa' của chức vụ thuộc nhóm Thay đổi trạng thái", "P2",
         L(ACC, "Chức vụ 'Xoá thử TEST' đã bị xoá (có mục 'Xóa' trong lịch sử)"),
         S(MENU_ROLES, "Tìm 'Xoá thử TEST' trên danh sách"), "—",
         E("Không còn dòng 'Xoá thử TEST' nên không mở được lịch sử của nó",
           "Lưu ý: nếu sau này có lối xem lịch sử chức vụ đã xoá, mục 'Xóa' (chữ đỏ) phải lọc ra khi chọn Loại hành động 'Thay đổi trạng thái'")),
        (9, "Bộ lọc trong khối Lịch sử ở màn Sửa hoạt động như popup", "P1", L(role_pre, "Có 1 mục Tạo mới và 2 mục Thay đổi thông tin"),
         S(MENU_ROLES, "Dòng 'Kế toán tổng hợp KT' -> 'Sửa'", "Khối Lịch sử bấm 'Xem lịch sử' -> 'Bộ lọc'", "Loại hành động chọn 'Tạo mới'"),
         "Loại hành động: Tạo mới",
         E("Khối lọc có đủ 4 ô và nút 'Làm mới' như popup", "Còn đúng 1 mục 'Tạo mới'", "Form sửa phía trên không bị ảnh hưởng")),
    ]

    s3 = [
        (1, "Tạo mới chức vụ đầy đủ thông tin sinh mục 'Tạo mới'", "P0", ACC,
         S(MENU_ROLES, "Bấm 'Thêm mới'",
           "Nhập Tên chức vụ, Vị trí, Ghi chú; ô Công ty chọn Công ty A",
           "Mục 'Chi tiết phân quyền' tab 'Công ty A' -> nhóm '1. NHÂN SỰ' mở khối 'Phân hệ tính lương' -> bấm thẻ 'Mẫu bảng lương' -> tick 'Xem' và 'Sửa'",
           "Bấm 'Lưu'",
           "Ở danh sách, dòng 'Trưởng ca TEST' -> bánh răng -> 'Lịch sử thay đổi'"),
         L("Tên chức vụ: Trưởng ca TEST", "Vị trí: 7", "Ghi chú: Chức vụ kiểm thử", "Công ty: Công ty A"),
         E("Báo 'Tạo mới chức vụ thành công', quay về danh sách",
           "Popup có đúng 1 mục 'Tạo mới' chữ xanh lá, 'Người thực hiện: Nguyễn Văn Quản Trị — <phòng ban>', thời gian = lúc bấm Lưu",
           "Các dòng chỉ có giá trị mới (chữ xanh): 'Tên chức vụ: Trưởng ca TEST', 'Ghi chú: Chức vụ kiểm thử', 'Vị trí: 7'",
           group("Công ty thêm mới", "Công ty A"),
           group("Quyền thêm mới (Công ty A)", perm_row("Sửa", "Phân hệ tính lương", "Mẫu bảng lương"),
                 perm_row("Xem", "Phân hệ tính lương", "Mẫu bảng lương")),
           "Tên quyền ghi đúng chữ cạnh ô tick trên màn Sửa, tên công ty ghi đúng như ô Công ty")),
        (2, "Tạo mới chỉ có Tên và Công ty", "P1", ACC,
         S(MENU_ROLES, "Bấm 'Thêm mới'", "Chỉ nhập Tên chức vụ và chọn Công ty A, không tick quyền nào", "Bấm 'Lưu'",
           "Mở 'Lịch sử thay đổi' của chức vụ vừa tạo"),
         L("Tên chức vụ: Tạp vụ TEST", "Công ty: Công ty A"),
         E("Mục 'Tạo mới' chỉ có 'Tên chức vụ: Tạp vụ TEST' và " + group("Công ty thêm mới", "Công ty A"),
           "KHÔNG hiện dòng Ghi chú, Vị trí (trường trống bị bỏ), KHÔNG có nhóm 'Quyền thêm mới'")),
        (3, "Tạo mới áp dụng 2 công ty, quyền khác nhau từng công ty", "P1",
         L(ACC, "QT1 được chọn Công ty A và Công ty B ở ô Công ty"),
         S(MENU_ROLES, "Bấm 'Thêm mới'", "Nhập Tên, chọn Công ty A và Công ty B",
           "Tab Công ty A tick 1 quyền Phân hệ tính lương; tab Công ty B tick 1 quyền Phân hệ giao việc", "Bấm 'Lưu'",
           "Mở lịch sử chức vụ vừa tạo"),
         L("Tên chức vụ: Điều phối TEST", "Công ty: Công ty A, Công ty B"),
         E("Nhóm 'Công ty thêm mới:' có 2 dòng 'Công ty A', 'Công ty B'",
           "Có 2 nhóm riêng 'Quyền thêm mới (Công ty A):' (quyền Phân hệ tính lương) và 'Quyền thêm mới (Công ty B):' (quyền Phân hệ giao việc)",
           "Không có quyền của công ty này lọt sang nhóm công ty kia")),
        (4, "Tạo mới thiếu Tên chức vụ bị chặn, không sinh lịch sử", "P0", ACC,
         S(MENU_ROLES, "Bấm 'Thêm mới'", "Để trống Tên chức vụ, chọn Công ty A", "Bấm 'Lưu'"),
         "Tên chức vụ: (trống)",
         E("Báo 'Tạo mới chức vụ thất bại'", "Dưới ô Tên chức vụ hiện lỗi 'Bắt buộc nhập'",
           "Màn giữ nguyên dữ liệu đã nhập, danh sách không có chức vụ mới (nên không có lịch sử)")),
        (5, "Tạo mới không chọn Công ty bị chặn", "P1", ACC,
         S(MENU_ROLES, "Bấm 'Thêm mới'", "Nhập Tên chức vụ, không chọn công ty", "Bấm 'Lưu'"),
         L("Tên chức vụ: Không công ty TEST", "Công ty: (trống)"),
         E("Báo 'Tạo mới chức vụ thất bại'", "Dưới ô Công ty hiện lỗi 'Bắt buộc nhập'", "Không tạo chức vụ, không sinh lịch sử")),
    ]

    UPD = "Có 1 mục mới trên cùng 'Thay đổi thông tin' (chữ xanh dương, nhóm lọc Thay đổi thông tin), người thực hiện QT1, thời gian lúc Lưu"
    s4 = [
        (1, "Sửa Tên chức vụ", "P0", role_pre, edit_steps("Đổi Tên chức vụ"),
         L("Tên chức vụ cũ: Kế toán tổng hợp KT", "Tên chức vụ mới: Kế toán trưởng KT"),
         E(UPD,
           "Mục chỉ có 1 " + diff("Tên chức vụ", "Kế toán tổng hợp KT", "Kế toán trưởng KT"),
           "KHÔNG có dòng Ghi chú / Vị trí / nhóm Công ty / nhóm Quyền")),
        (2, "Sửa Ghi chú", "P0", role_pre, edit_steps("Sửa ô Ghi chú"),
         L("Ghi chú cũ: Nhóm kế toán", "Ghi chú mới: Nhóm kế toán tổng hợp"),
         E("Mục mới chỉ có " + diff("Ghi chú", "Nhóm kế toán", "Nhóm kế toán tổng hợp"))),
        (3, "Xoá trắng Ghi chú", "P1", role_pre, edit_steps("Xoá hết nội dung ô Ghi chú"),
         L("Ghi chú cũ: Nhóm kế toán", "Ghi chú mới: (để trống)"),
         E("Mục mới chỉ có " + diff("Ghi chú", "Nhóm kế toán", "(trống)"))),
        (4, "Sửa Vị trí", "P0", role_pre, edit_steps("Đổi ô Vị trí"),
         L("Vị trí cũ: 5", "Vị trí mới: 3"),
         E("Mục mới chỉ có " + diff("Vị trí", "5", "3"))),
        (5, "Nhập Vị trí cho chức vụ đang để trống", "P1",
         L(ACC, "Chức vụ 'Thủ kho KT' có Vị trí trống"),
         S(MENU_ROLES, "Dòng 'Thủ kho KT' -> 'Sửa'", "Nhập Vị trí 2", "Bấm 'Lưu'", "Mở lịch sử 'Thủ kho KT'"),
         "Vị trí mới: 2",
         E("Mục mới chỉ có " + new_only("Vị trí", "2"))),
        (6, "Thêm công ty áp dụng", "P0", role_pre, edit_steps("Ô Công ty chọn thêm Công ty B, không tick quyền ở tab Công ty B"),
         "Công ty thêm: Công ty B",
         E("Mục mới chỉ có " + group("Công ty thêm mới", "Công ty B") + " (chữ xanh)",
           "KHÔNG có nhóm 'Quyền thêm mới' / 'Quyền đã xóa'", "Không có dòng Tên / Ghi chú / Vị trí")),
        (7, "Bỏ công ty áp dụng đang có quyền", "P0",
         L(role_pre, "Chức vụ đang áp dụng thêm Công ty B, có quyền 'Xem' ở thẻ 'Bảng lương' (Phân hệ tính lương) ở Công ty B"),
         edit_steps("Ở ô Công ty bấm bỏ Công ty B"),
         "Công ty bỏ: Công ty B",
         E(group("Công ty đã xóa", "Công ty B") + " (chữ đỏ)",
           group("Quyền đã xóa (Công ty B)", perm_row("Xem", "Phân hệ tính lương", "Bảng lương")) + " (chữ đỏ)")),
        (8, "Thêm 1 quyền trong 1 phân hệ", "P0", role_pre,
         edit_steps("Tab Công ty A, khối 'Phân hệ tính lương', thẻ 'Mẫu bảng lương' tick thêm 'Thêm'"),
         "Quyền thêm: Mẫu bảng lương - Thêm",
         E("Mục mới chỉ có " + group("Quyền thêm mới (Công ty A)", perm_row("Thêm", "Phân hệ tính lương", "Mẫu bảng lương")),
           "KHÔNG liệt kê lại quyền 'Xem' đang có sẵn")),
        (9, "Bỏ 1 quyền", "P0", role_pre,
         edit_steps("Tab Công ty A, thẻ 'Mẫu bảng lương' bỏ tick 'Xem'"),
         "Quyền bỏ: Mẫu bảng lương - Xem",
         E("Mục mới chỉ có " + group("Quyền đã xóa (Công ty A)", perm_row("Xem", "Phân hệ tính lương", "Mẫu bảng lương")) + " (chữ đỏ)")),
        (10, "Thêm và bỏ quyền ở nhiều phân hệ trong 1 lần Lưu", "P1", role_pre,
         edit_steps("Tick thêm 1 quyền Phân hệ giao việc, 1 quyền Phân hệ CSKH sau bán; bỏ tick 'Xem' ở thẻ 'Mẫu bảng lương'"),
         "—",
         E("Chỉ 1 mục mới",
           "Nhóm 'Quyền thêm mới (Công ty A):' có 2 dòng, 1 dòng ghi 'Phân hệ: Phân hệ giao việc', 1 dòng ghi 'Phân hệ: Phân hệ CSKH sau bán'",
           "Nhóm 'Quyền đã xóa (Công ty A):' có 1 dòng " + perm_row("Xem", "Phân hệ tính lương", "Mẫu bảng lương"),
           "Mỗi dòng ghi đúng tên phần (tên thẻ) chứa quyền")),
        (11, "Quyền của phân hệ mới hiển thị đúng tên phân hệ", "P0", role_pre,
         edit_steps("Tick 1 quyền ở mỗi khối: Phân hệ meeting, Phân hệ an toàn - 5S, Phân hệ CSKH trước bán, Phân hệ danh mục chung"),
         "—",
         E("4 dòng trong nhóm 'Quyền thêm mới (Công ty A):' lần lượt ghi 'Phân hệ: Phân hệ meeting', 'Phân hệ: Phân hệ an toàn - 5S', 'Phân hệ: Phân hệ CSKH trước bán', 'Phân hệ: Phân hệ danh mục chung'",
           "Tên phân hệ trùng khớp tiêu đề khối quyền trên màn Chỉnh sửa chức vụ",
           "KHÔNG xuất hiện dạng 'Phân hệ #26' hay 'Chưa phân loại phân hệ' với các quyền này")),
        (12, "Đổi quyền ở 2 công ty trong 1 lần Lưu", "P1",
         L(role_pre, "Chức vụ áp dụng Công ty A và Công ty B"),
         edit_steps("Tab Công ty A tick thêm 1 quyền; tab Công ty B bỏ 1 quyền"), "—",
         E("1 mục mới có 2 nhóm: 'Quyền thêm mới (Công ty A):' (chữ xanh) và 'Quyền đã xóa (Công ty B):' (chữ đỏ), đúng từng quyền")),
        (13, "Sửa nhiều trường trong 1 lần Lưu gom thành 1 mục", "P0", role_pre,
         edit_steps("Đổi Tên chức vụ, Vị trí, Ghi chú và tick thêm 1 quyền"),
         L("Tên: Kế toán tổng hợp KT -> Kế toán TH KT", "Vị trí: 5 -> 6", "Ghi chú: Nhóm kế toán -> Nhóm KT"),
         E("Đúng 1 mục mới 'Thay đổi thông tin'", "Theo thứ tự: Tên chức vụ, Ghi chú, Vị trí (cũ đỏ -> mới xanh) rồi nhóm 'Quyền thêm mới (Công ty A):'",
           "Không tách thành nhiều mục")),
        (14, "Lưu mà không đổi gì thì không sinh mục", "P0", L(role_pre, "Lịch sử đang có 3 mục"),
         edit_steps("Không sửa gì"), "—",
         E("Báo 'Chỉnh sửa chức vụ thành công'", "Popup vẫn đúng 3 mục, KHÔNG có mục mới")),
        (15, "Tick rồi bỏ tick cùng quyền trước khi Lưu", "P1", L(role_pre, "Lịch sử đang có 3 mục"),
         edit_steps("Thẻ 'Tạm ứng lương' tick 'Xem' rồi bỏ tick lại chính ô đó"), "—",
         E("KHÔNG có mục mới")),
        (16, "Sửa bị chặn vì xoá trống Tên chức vụ", "P1", L(role_pre, "Lịch sử đang có 3 mục"),
         S(MENU_ROLES, "Dòng 'Kế toán tổng hợp KT' -> 'Sửa'", "Xoá trống Tên chức vụ, đổi Vị trí thành 9", "Bấm 'Lưu'",
           "Khối Lịch sử cuối màn bấm 'Xem lịch sử'"),
         L("Tên chức vụ: (trống)", "Vị trí: 9"),
         E("Báo 'Chỉnh sửa chức vụ thất bại', dưới ô Tên hiện 'Bắt buộc nhập'",
           "Khối Lịch sử vẫn 3 mục, KHÔNG có mục nào với Vị trí 9")),
        (17, "Người thực hiện và thời gian đúng người bấm Lưu", "P1", role_pre,
         S("Đăng nhập QT2", MENU_ROLES, "Sửa Ghi chú chức vụ 'Kế toán tổng hợp KT', ghi lại giờ bấm Lưu",
           "Đăng nhập QT1, mở lịch sử chức vụ"),
         "Ghi chú mới: Sửa bởi QT2",
         E("Mục mới ghi 'Người thực hiện: Trần Thị Kiểm Thử — <phòng ban của QT2>' (người bấm Lưu), KHÔNG phải người đang xem",
           "Thời gian (giờ:phút) lệch không quá 1 phút so với giờ bấm Lưu")),
    ]

    s5 = [
        (1, "Xoá chức vụ chưa gán nhân viên", "P0",
         L(ACC, "Chức vụ 'Xoá thử TEST' áp dụng Công ty A, có 2 quyền, chưa gán cho nhân viên nào"),
         S(MENU_ROLES, "Dòng 'Xoá thử TEST' -> bánh răng -> 'Xóa'",
           "Hộp thoại 'Cảnh báo' hỏi 'Bạn có chắc chắn muốn xóa không?' -> bấm 'Xoá'"),
         "—",
         E("Báo 'Xóa chức vụ thành công'", "Dòng 'Xoá thử TEST' biến mất khỏi danh sách",
           "Tổng số bản ghi giảm 1",
           "Hệ thống ghi 1 mục 'Xóa' (chữ đỏ, nhóm lọc Thay đổi trạng thái) — hiện chưa có chỗ xem trên giao diện, xem mục 9")),
        (2, "Xoá chức vụ đã có nhân viên nhận bị chặn, không sinh mục Xóa", "P0",
         L(role_pre, "Chức vụ 'Kế toán tổng hợp KT' đang gán cho 3 nhân viên", "Lịch sử đang có 3 mục"),
         S(MENU_ROLES, "Dòng 'Kế toán tổng hợp KT' -> 'Xóa' -> xác nhận", "Mở 'Lịch sử thay đổi' của dòng đó"),
         "—",
         E("Báo lỗi 'Đã có nhân viên nhận chức vụ này!'", "Chức vụ vẫn còn trên danh sách",
           "Lịch sử vẫn 3 mục, KHÔNG có mục 'Xóa'; lọc 'Thay đổi trạng thái' hiện '%s'" % NO_MATCH)),
        (3, "Huỷ hộp thoại xác nhận xoá", "P1", L(ACC, "Chức vụ 'Xoá thử 2 TEST' chưa gán nhân viên"),
         S(MENU_ROLES, "Dòng 'Xoá thử 2 TEST' -> 'Xóa'", "Bấm 'Huỷ' trên hộp thoại 'Cảnh báo'"), "—",
         E("Chức vụ vẫn còn", "Không báo thành công")),
        (4, "Tạo lại chức vụ cùng tên sau khi xoá không kế thừa lịch sử cũ", "P0",
         L(ACC, "Đã xoá chức vụ 'Xoá thử TEST' ở TC_05.001"),
         S(MENU_ROLES, "Bấm 'Thêm mới', tạo chức vụ tên 'Xoá thử TEST', chọn Công ty A, không tick quyền", "Bấm 'Lưu'",
           "Mở 'Lịch sử thay đổi' của chức vụ mới"),
         "Tên chức vụ: Xoá thử TEST",
         E("Popup chỉ có 1 mục 'Tạo mới' của lần tạo này",
           "KHÔNG có mục của chức vụ cũ đã xoá",
           "Màn Sửa chức vụ mới không tự có sẵn công ty / quyền của chức vụ cũ")),
    ]

    s6 = [
        (1, "[Lỗi đã sửa] Người không có quyền không vào được màn phân quyền", "P0",
         "Tài khoản NV1 không có quyền %s" % Q_ROLE,
         S("Đăng nhập NV1", "Mở phân hệ Quản trị hệ thống", "Mở lại màn Danh sách phân quyền từ lịch sử duyệt web"),
         "—",
         E("Không có mục menu 'Danh sách phân quyền'", BLOCKED,
           "Trước đây: vẫn vào được và xem / sửa được chức vụ")),
        (2, "[Lỗi đã sửa] Tên phân hệ trong lịch sử cũ hiện đúng tên", "P0",
         L(role_pre, "Chức vụ có mục lịch sử được ghi trước bản sửa, chứa quyền thuộc Phân hệ danh mục chung và Phân hệ meeting"),
         open_list, "—",
         E("Dòng quyền của mục cũ ghi 'Phân hệ: Phân hệ danh mục chung', 'Phân hệ: Phân hệ meeting'",
           "KHÔNG còn dạng 'Phân hệ #9', 'Phân hệ #26'",
           "Lịch sử ghi trước khi đổi khuôn popup vẫn hiện đầy đủ theo khuôn mới")),
        (3, "[Lỗi đã sửa] Màn Sửa chức vụ xem được lịch sử ngay trong thân trang", "P0", role_pre,
         S(MENU_ROLES, "Dòng 'Kế toán tổng hợp KT' -> 'Sửa'", "Cuộn xuống khối 'Lịch sử', bấm 'Xem lịch sử'"), "—",
         E("Khối 'Lịch sử' có mặt và hiện đúng lịch sử của chức vụ đang sửa",
           "Trước đây: phải bấm nút 'Lịch sử' ở chân trang để mở popup riêng")),
        (4, "[Lỗi đã sửa] Xoá chức vụ dọn sạch công ty và quyền kèm theo", "P1",
         L(ACC, "Chức vụ 'Mồ côi TEST' áp dụng Công ty A, Công ty B, có quyền ở cả 2 công ty, chưa gán nhân viên"),
         S(MENU_ROLES, "Xoá 'Mồ côi TEST'", "Ở Công ty B mở Danh sách phân quyền",
           "Bấm 'Thêm mới' tạo lại 'Mồ côi TEST' chỉ chọn Công ty A", "Mở lịch sử chức vụ mới"),
         "—",
         E("Sau khi xoá, chức vụ không còn ở danh sách của cả Công ty A lẫn Công ty B",
           "Chức vụ tạo lại chỉ có Công ty A, không kéo theo quyền của chức vụ cũ",
           "Lịch sử chức vụ mới chỉ có 1 mục 'Tạo mới'")),
        (5, "[Lỗi đã sửa] Lưu lại chức vụ có Vị trí trống không sinh mục rác", "P1",
         L(ACC, "Chức vụ 'Thủ kho KT' có Vị trí trống, lịch sử đang có 1 mục"),
         S(MENU_ROLES, "Dòng 'Thủ kho KT' -> 'Sửa'", "Không sửa gì, bấm 'Lưu'", "Mở lịch sử 'Thủ kho KT'"), "—",
         E("Không có mục mới", "Không xuất hiện dòng dạng 'Vị trí: 0'")),
        (6, "[Lỗi đã sửa] Không hiện mục cập nhật rỗng", "P1",
         L(role_pre, "Có mục lịch sử cũ chỉ đổi thứ tự sắp xếp nội bộ, không có thay đổi hiển thị được"),
         open_list, "—",
         E("Mục cũ đó bị ẩn", "KHÔNG hiện mục 'Thay đổi thông tin' không có dòng thay đổi nào")),
        (7, "[Lỗi đã sửa] Lịch sử chức vụ nhiều quyền không còn bị mất", "P0",
         L(role_pre, "Chức vụ có rất nhiều quyền (vd 'Super admin' — tick gần hết quyền ở mọi phân hệ, nhiều công ty áp dụng)"),
         S(MENU_ROLES, "Sửa chức vụ đó: bỏ tick 1 quyền, Lưu", "Mở lịch sử chức vụ"), "—",
         E("Có mục 'Thay đổi thông tin' mới nhất, hiện đúng quyền vừa bỏ ở nhóm 'Quyền đã xóa'",
           "Trước đây: lần lưu của chức vụ nhiều quyền bị cắt cụt khi ghi, mục lịch sử không hiện được")),
        (8, "Mục lịch sử cũ bị cắt cụt vẫn hiện, kèm ghi chú", "P1",
         L(role_pre, "Chức vụ 'Super admin' có 4 lần cập nhật ghi TRƯỚC bản sửa (03/08, 08/09, 19/09, 21/09/2026) bị cắt khi lưu"),
         S("Mở lịch sử chức vụ 'Super admin'"), "—",
         E("Vẫn hiện đủ 4 mục 'Thay đổi thông tin' với đúng thời gian và người thực hiện",
           "Mỗi mục có khối ghi chú nền vàng: 'Nội dung chi tiết của lần cập nhật này quá dài nên đã bị cắt khi lưu, không hiển thị được.'",
           "KHÔNG bị ẩn mất như trước")),
    ]

    return build(output_file=out("Lịch sử Phân quyền"), sheet_name="Trang tính1",
                 feature_name="Lịch sử thay đổi - Phân quyền (chức vụ) - Cập nhật ngày 30/09/2026",
                 module_name="Phân quyền (chức vụ)",
                 description_block=desc, role_tcs=roles,
                 sections=[("I", "POPUP LỊCH SỬ & KHỐI LỊCH SỬ MÀN SỬA", s1),
                           ("II", "BỘ LỌC LỊCH SỬ", s2),
                           ("III", "LỊCH SỬ KHI TẠO MỚI CHỨC VỤ", s3),
                           ("IV", "LỊCH SỬ KHI SỬA TỪNG TRƯỜNG", s4),
                           ("V", "XÓA CHỨC VỤ", s5),
                           ("VI", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", s6)])


# =====================================================================================
# FILE 2 - LICH SU NGUOI DUNG
# =====================================================================================
def build_users():
    user_pre = L(ACC,
                 "Người dùng 'NV kiểm thử 01' (mã NV01001, thuộc Công ty A):",
                 "Quyền: 'Nhân viên kinh doanh'; KHÔNG tick 'Quản lý tất cả phòng ban trong công ty của tôi';",
                 "Phân công quản lý phòng ban: Công ty A › Phòng Kinh doanh 1 (không chọn bộ phận)")
    open_list = S(MENU_USERS, "Dòng 'NV kiểm thử 01' -> bánh răng ở cột Hành động -> 'Lịch sử thay đổi'")
    list_steps = [MENU_USERS, "Dòng 'NV kiểm thử 01' -> bánh răng -> 'Lịch sử thay đổi'"]
    TITLE = "Lịch sử thay đổi: NV01001 - NV kiểm thử 01"
    ALL = "Quản lý tất cả phòng ban trong công ty của tôi"

    def edit_steps(action):
        return S(MENU_USERS, "Dòng 'NV kiểm thử 01' -> bánh răng -> 'Sửa'", action, "Bấm 'Lưu'",
                 "Ở danh sách, dòng 'NV kiểm thử 01' -> bánh răng -> 'Lịch sử thay đổi'")

    def dept(name, company, parts=None):
        return "%s — Công ty: %s%s" % (name, company, ("; Bộ phận: " + parts) if parts else "")

    desc = [
        ("1. Mục đích tính năng",
         L("Ghi lại và cho xem lịch sử thay đổi phân quyền của từng người dùng ở màn Danh sách người dùng:",
           "ai đã đổi chức vụ (ô Quyền), cờ Quản lý tất cả phòng ban, phân công quản lý phòng ban/bộ phận của người nào, lúc nào, cũ -> mới.",
           "Xem được ở 2 nơi, cùng nội dung và bộ lọc: popup 'Lịch sử thay đổi: <Mã NV> - <Họ tên>' mở từ dropdown thao tác từng dòng danh sách,",
           "và khối 'Lịch sử' trong thân màn 'Phân quyền người dùng' (thay cho nút 'Lịch sử thay đổi' cạnh nút Lưu trước đây).")),
        ("2. Đối tượng được tính / hiển thị",
         L("Mỗi lần Lưu có thay đổi sinh 1 mục 'Thay đổi thông tin' (chữ xanh dương, nhóm lọc Thay đổi thông tin) gồm các phần có đổi:",
           "- '%s:' Không / Có (cũ đỏ -> mới xanh)" % ALL,
           "- Nhóm 'Quyền thêm mới:' (chữ xanh) / 'Quyền đã xóa:' (chữ đỏ): mỗi chức vụ 1 dòng",
           "- Nhóm 'Phòng ban quản lý thêm mới:' / 'Phòng ban quản lý đã xóa:': mỗi dòng '<Phòng ban> — Công ty: <Công ty>', có bộ phận thì thêm '; Bộ phận: A, B';",
           "  dòng công ty tick 'Quản lý tất cả phòng ban' ghi 'Tất cả phòng ban — Công ty: <Công ty>'",
           "- Nhóm 'Phòng ban quản lý sửa thông tin:': đổi bộ phận của phòng ban đang quản lý, dạng '<Phòng ban>: Bộ phận: cũ -> mới'")),
        ("3. Đối tượng bị ẩn / không tính",
         L("- Lưu không đổi gì: KHÔNG sinh mục",
           "- Vai trò gán từ ERP: chỉ hiển thị để xem ở màn Sửa, KHÔNG sửa được, KHÔNG bị xoá khi Lưu, KHÔNG ghi vào lịch sử",
           "- Lưu bị chặn (dòng phân công chưa chọn công ty): KHÔNG sinh mục",
           "- Dòng phân công chỉ chọn công ty, chưa chọn phòng ban và không tick tất cả: không được lưu nên không có trong lịch sử",
           "- Không có thao tác tạo / xoá người dùng ở màn này (người dùng đến từ hồ sơ nhân sự) nên nhóm 'Tạo mới' và 'Thay đổi trạng thái' luôn trống")),
        ("4. Bộ lọc thời gian áp dụng cho",
         L(FILTER_DESC, GROUP_RULE, "Ô 'Người thực hiện' liệt kê nhân sự của CÔNG TY người dùng đang xem.")),
        ("5. Cấu trúc dữ liệu / cây phân cấp",
         L("Phân công quản lý phòng ban: Công ty -> nhiều Phòng ban -> mỗi phòng ban nhiều Bộ phận.",
           "Mỗi cặp Công ty + Phòng ban là 1 dòng; đổi bộ phận của phòng ban đó hiện ở nhóm 'sửa thông tin', đổi công ty hiện là xoá dòng cũ + thêm dòng mới.")),
        ("6. Quy tắc cộng dồn / deduplicate",
         L("- 1 lần Lưu = 1 mục, gom mọi thay đổi",
           "- Tick '%s' thì toàn bộ phân công phòng ban bị xoá -> lịch sử hiện thêm nhóm 'Phòng ban quản lý đã xóa' tương ứng" % ALL)),
        ("7. Phân quyền cấp",
         L("Quyền 'Quản lý phân quyền': thấy menu Danh sách người dùng, vào màn Sửa, xem lịch sử.",
           "Chỉ xem được lịch sử người dùng thuộc CÔNG TY ĐANG LÀM VIỆC; người dùng công ty khác không xem được (kể cả quản trị).",
           "Không có quyền riêng cho lịch sử. Không có quyền: không thấy menu, mở lại màn bị chuyển sang trang không tìm thấy.")),
        ("8. Cách tính các ô thống kê",
         "Không áp dụng. Khối 'Lịch sử' ở màn Sửa có ô số nhỏ cạnh chữ 'Lịch sử' = tổng số mục (sau khi tải)."),
        ("9. Ghi chú đọc bảng",
         L(LAYOUT_NOTE,
           "- Tiêu đề popup 'Lịch sử thay đổi: Mã NV - Họ tên'; tiêu đề popup chức vụ chỉ có tên chức vụ",
           "- Giá trị Có/Không thống nhất cho mọi cờ",
           "- Màn 'Phân quyền người dùng': cuối màn chỉ còn 'Lưu', 'Quay lại'; khối Lịch sử nằm ngay trên 2 nút này",
           "- Phân quyền hàng loạt (ở màn chức vụ) KHÔNG thuộc phạm vi lịch sử của màn này")),
    ]

    roles = [
        ("01", "Có quyền 'Quản lý phân quyền' thấy menu và nút Lịch sử", "P0", ACC,
         S("Đăng nhập QT1", MENU_USERS, "Bấm bánh răng ở 1 dòng"), "—",
         E("Menu 'Danh sách người dùng' hiển thị", "Dropdown có 'Sửa' và 'Lịch sử thay đổi'")),
        ("02", "Không có quyền không thấy menu Danh sách người dùng", "P0",
         "Tài khoản NV1 không có quyền %s" % Q_ROLE,
         S("Đăng nhập NV1", "Mở phân hệ Quản trị hệ thống"), "—",
         E("Nhóm 'Người dùng & phân quyền' KHÔNG có 'Danh sách người dùng' và 'Danh sách phân quyền'",
           "Nếu NV1 cũng không có quyền xem Tài khoản nhân viên thì cả nhóm bị ẩn khỏi menu")),
        ("03", "Không có quyền mở lại màn Danh sách người dùng bị chặn", "P0",
         L("NV1 từng có quyền và đã mở màn, sau đó bị gỡ quyền %s" % Q_ROLE),
         S("NV1 đăng nhập lại", "Mở lại màn Danh sách người dùng từ lịch sử duyệt web"), "—",
         E(BLOCKED)),
        ("04", "Không có quyền mở lại màn Phân quyền người dùng bị chặn", "P0",
         "NV1 từng mở màn Phân quyền người dùng của 'NV kiểm thử 01', sau đó bị gỡ quyền",
         S("NV1 đăng nhập lại", "Mở lại màn đó từ lịch sử duyệt web"), "—",
         E(BLOCKED, "Không tải thông tin phân quyền, không thấy khối 'Lịch sử'")),
        ("05", "Không có quyền riêng cho lịch sử", "P2", ACC,
         S("Đăng nhập QT2 (chỉ có quyền %s)" % Q_ROLE, MENU_USERS, "Mở lịch sử 1 người dùng thuộc Công ty A"), "—",
         E("QT2 xem được đầy đủ lịch sử, không cần quyền nào khác")),
        ("06", "Không xem được lịch sử người dùng thuộc công ty khác", "P1",
         L(ACC, "QT1 đang làm việc ở Công ty A", "'NV Công ty B' thuộc Công ty B đã có 2 mục lịch sử"),
         S("QT1 mở lại màn Phân quyền người dùng của 'NV Công ty B' từ lịch sử duyệt web", "Bấm 'Xem lịch sử' ở khối 'Lịch sử'"), "—",
         E("Khối Lịch sử báo 'Không tải được lịch sử.' kèm nút 'Thử lại'",
           "KHÔNG lộ mục lịch sử nào của 'NV Công ty B'")),
    ]

    s1 = [
        (1, "Bố cục popup mở từ danh sách", "P0", user_pre, open_list, "—",
         popup_layout(TITLE, "Tiêu đề ghép 'Mã NV - Họ tên'")),
        (2, "Khối 'Lịch sử' trên màn Phân quyền người dùng", "P0", user_pre,
         S(MENU_USERS, "Dòng 'NV kiểm thử 01' -> 'Sửa'", "Quan sát cuối màn", "Bấm 'Xem lịch sử' ở khối 'Lịch sử'"), "—",
         E("Tiêu đề màn 'Phân quyền người dùng'",
           "Khối 'Lịch sử' nằm trên dãy nút cuối màn, mặc định THU GỌN, chỉ có nút 'Xem lịch sử'",
           "Bấm 'Xem lịch sử': tải và hiện dòng thời gian, cạnh chữ 'Lịch sử' có ô số tổng mục, bên phải có 'Làm mới' và 'Thu gọn'",
           "Cuối màn chỉ còn 2 nút 'Lưu', 'Quay lại' — KHÔNG còn nút 'Lịch sử thay đổi'",
           "Nội dung giống hệt popup mở từ danh sách")),
        (3, "Người dùng chưa có lịch sử", "P1", L(ACC, "Người dùng 'NV mới 02' chưa từng được phân quyền lại"),
         S(MENU_USERS, "Dòng 'NV mới 02' -> 'Lịch sử thay đổi'"), "—",
         E("Hiện biểu tượng đồng hồ và '%s'" % EMPTY_TEXT, "Không có nút 'Bộ lọc'")),
        (4, "Thứ tự và thông tin mỗi mục", "P0",
         L(user_pre, "Đã có 2 lần sửa: QT2 ngày 05/09/2026, QT1 ngày 18/09/2026"), open_list, "—",
         E(*TIMELINE_COMMON + ["Mục trên cùng là lần QT1 sửa ngày 18/09/2026, 'Người thực hiện: Nguyễn Văn Quản Trị — <phòng ban>'",
                               "Mọi mục có tên hành động 'Thay đổi thông tin' chữ xanh dương"])),
        (5, "Mở lịch sử 2 người dùng liên tiếp không lẫn dữ liệu", "P1", user_pre,
         S(MENU_USERS, "Mở lịch sử 'NV kiểm thử 01', bấm 'Đóng'", "Mở lịch sử 'NV mới 02'"), "—",
         E("Popup thứ 2 có tiêu đề kèm mã và tên của 'NV mới 02'", "Không còn mục nào của 'NV kiểm thử 01'")),
    ]

    s2 = filter_tcs(1, user_pre, list_steps,
                    {"Tạo mới": 0, "Thay đổi thông tin": 3, "Thay đổi trạng thái": 0},
                    "'QTR - Trần Thị Kiểm Thử'", "công ty của người dùng đang xem (Công ty A)",
                    ("05/09/2026", "12/09/2026", "18/09/2026"),
                    extra_group="Mọi mục của màn này đều thuộc 'Thay đổi thông tin' (chỉ có thao tác cập nhật phân quyền)")

    s3 = [
        (1, "Thêm 1 chức vụ ở ô Quyền", "P0", user_pre, edit_steps("Ô 'Quyền' chọn thêm 'Trưởng nhóm kinh doanh'"),
         "Quyền thêm: Trưởng nhóm kinh doanh",
         E("Báo 'Phân quyền thành công', quay về Danh sách người dùng",
           "1 mục mới 'Thay đổi thông tin' (chữ xanh dương), người thực hiện QT1, thời gian lúc Lưu",
           "Mục chỉ có " + group("Quyền thêm mới", "Trưởng nhóm kinh doanh") + " (chữ xanh)",
           "Không có dòng %s / nhóm Phòng ban quản lý" % ALL)),
        (2, "Bỏ 1 chức vụ ở ô Quyền", "P0", user_pre, edit_steps("Ô 'Quyền' bấm bỏ 'Nhân viên kinh doanh'"),
         "Quyền bỏ: Nhân viên kinh doanh",
         E("Mục mới chỉ có " + group("Quyền đã xóa", "Nhân viên kinh doanh") + " (chữ đỏ)")),
        (3, "Vừa thêm vừa bỏ chức vụ trong 1 lần Lưu", "P1", user_pre,
         edit_steps("Bỏ 'Nhân viên kinh doanh', thêm 'Kế toán tổng hợp KT' và 'Thủ kho KT'"), "—",
         E("1 mục mới: nhóm 'Quyền thêm mới:' 2 dòng 'Kế toán tổng hợp KT', 'Thủ kho KT'; nhóm 'Quyền đã xóa:' 1 dòng 'Nhân viên kinh doanh'")),
        (4, "Tick '%s'" % ALL, "P0", user_pre,
         edit_steps("Tick ô '%s' (bảng phân công bị ẩn)" % ALL),
         "%s: tick" % ALL,
         E("Mục mới có " + diff(ALL, "Không", "Có"),
           "Có thêm " + group("Phòng ban quản lý đã xóa", dept("Phòng Kinh doanh 1", "Công ty A")),
           "Lưu ý: phân công cũ bị xoá khi tick tất cả, lịch sử PHẢI thể hiện điều đó")),
        (5, "Bỏ tick '%s'" % ALL, "P0",
         L(ACC, "'NV kiểm thử 03' đang tick '%s'" % ALL),
         S(MENU_USERS, "Dòng 'NV kiểm thử 03' -> 'Sửa'", "Bỏ tick ô đó, thêm 1 dòng phân công Công ty A › Phòng Hành chính",
           "Bấm 'Lưu'", "Mở lịch sử 'NV kiểm thử 03'"), "—",
         E("Mục mới có " + diff(ALL, "Có", "Không"),
           "Và " + group("Phòng ban quản lý thêm mới", dept("Phòng Hành chính", "Công ty A")))),
        (6, "Thêm dòng phân công: công ty + phòng ban, không bộ phận", "P0", user_pre,
         edit_steps("Bảng 'Phân công quản lý phòng ban' bấm dấu cộng ở tiêu đề, chọn Công ty B, Phòng ban 'Phòng Kỹ thuật B'"),
         L("Công ty: Công ty B", "Phòng ban: Phòng Kỹ thuật B"),
         E("Mục mới chỉ có " + group("Phòng ban quản lý thêm mới", dept("Phòng Kỹ thuật B", "Công ty B")))),
        (7, "Chọn bộ phận cho phòng ban đang quản lý", "P0", user_pre,
         edit_steps("Dòng Công ty A › Phòng Kinh doanh 1, cột 'Các bộ phận' (ô gợi ý 'Bộ phận') chọn 'Nhóm KD Miền Bắc' và 'Nhóm KD Miền Nam'"),
         "Bộ phận: Nhóm KD Miền Bắc, Nhóm KD Miền Nam",
         E("Nhóm 'Phòng ban quản lý sửa thông tin:' có dòng '- Phòng Kinh doanh 1: Bộ phận: (trống) -> Nhóm KD Miền Bắc, Nhóm KD Miền Nam' (cũ đỏ, mới xanh)",
           "KHÔNG tách thành 1 dòng xoá + 1 dòng thêm")),
        (8, "Thêm phòng ban thứ 2 trong cùng công ty", "P1", user_pre,
         edit_steps("Dòng Công ty A bấm 'Thêm phòng ban', chọn 'Phòng Kinh doanh 2'"),
         "Phòng ban thêm: Phòng Kinh doanh 2",
         E("Chỉ có " + group("Phòng ban quản lý thêm mới", dept("Phòng Kinh doanh 2", "Công ty A")),
           "KHÔNG có dòng xoá của Phòng Kinh doanh 1")),
        (9, "Xoá 1 phòng ban trong công ty", "P1",
         L(user_pre, "Công ty A đang quản lý thêm Phòng Kinh doanh 2"),
         edit_steps("Bấm biểu tượng trừ tròn cạnh 'Phòng Kinh doanh 2'"), "—",
         E("Chỉ có " + group("Phòng ban quản lý đã xóa", dept("Phòng Kinh doanh 2", "Công ty A")) + " (chữ đỏ)")),
        (10, "Xoá cả dòng phân công của 1 công ty", "P0",
         L(user_pre, "Có thêm dòng Công ty B › Phòng Kỹ thuật B"),
         edit_steps("Bấm biểu tượng trừ ở cột cuối dòng Công ty B"), "—",
         E(group("Phòng ban quản lý đã xóa", dept("Phòng Kỹ thuật B", "Công ty B")), "Phạm vi Công ty A không bị nhắc tới")),
        (11, "Tick 'Quản lý tất cả phòng ban' cho 1 dòng công ty", "P0", user_pre,
         edit_steps("Dòng Công ty A tick 'Quản lý tất cả phòng ban' (dưới ô công ty)"),
         "Dòng Công ty A: Quản lý tất cả phòng ban",
         E("Ô phòng ban/bộ phận của dòng đổi thành chữ 'Quản lý tất cả phòng ban và bộ phận của công ty này'",
           "Lưu thành công, KHÔNG báo lỗi hệ thống",
           "Lịch sử: " + group("Phòng ban quản lý thêm mới", dept("Tất cả phòng ban", "Công ty A")) + " và "
           + group("Phòng ban quản lý đã xóa", dept("Phòng Kinh doanh 1", "Công ty A")),
           "KHÔNG có dòng '%s' (cờ tổng không đổi)" % ALL)),
        (12, "Bỏ tick 'Quản lý tất cả phòng ban' của dòng công ty", "P1",
         L(ACC, "'NV kiểm thử 04' có dòng Công ty A tick 'Quản lý tất cả phòng ban'"),
         S(MENU_USERS, "Dòng 'NV kiểm thử 04' -> 'Sửa'", "Bỏ tick ở dòng Công ty A, chọn Phòng ban 'Phòng Hành chính'",
           "Bấm 'Lưu'", "Mở lịch sử 'NV kiểm thử 04'"), "—",
         E(group("Phòng ban quản lý đã xóa", dept("Tất cả phòng ban", "Công ty A")),
           group("Phòng ban quản lý thêm mới", dept("Phòng Hành chính", "Công ty A")))),
        (13, "Đổi công ty của 1 dòng phân công", "P1", L(user_pre, "Có dòng Công ty B › Phòng Kỹ thuật B"),
         edit_steps("Dòng Công ty B đổi ô công ty sang Công ty C, chọn Phòng ban 'Phòng Kỹ thuật C'"), "—",
         E(group("Phòng ban quản lý thêm mới", dept("Phòng Kỹ thuật C", "Công ty C")),
           group("Phòng ban quản lý đã xóa", dept("Phòng Kỹ thuật B", "Công ty B")))),
        (14, "Nhiều thay đổi trong 1 lần Lưu gom 1 mục", "P0", user_pre,
         edit_steps("Thêm quyền 'Thủ kho KT', thêm phân công Công ty B › Phòng Kỹ thuật B"), "—",
         E("Đúng 1 mục mới", "Có cả nhóm 'Quyền thêm mới:' và nhóm 'Phòng ban quản lý thêm mới:'")),
    ]

    s4 = [
        (1, "Lưu mà không đổi gì thì không sinh mục", "P0", L(user_pre, "Lịch sử đang có 2 mục"),
         edit_steps("Không sửa gì"), "—",
         E("Báo 'Phân quyền thành công'", "Lịch sử vẫn đúng 2 mục")),
        (2, "Chọn rồi bỏ lại cùng chức vụ trước khi Lưu", "P1", L(user_pre, "Lịch sử đang có 2 mục"),
         edit_steps("Ô Quyền chọn thêm 'Thủ kho KT' rồi bấm bỏ lại"), "—", E("Không có mục mới")),
        (3, "Dòng phân công chưa chọn công ty bị chặn", "P0", L(user_pre, "Lịch sử đang có 2 mục"),
         S(MENU_USERS, "Dòng 'NV kiểm thử 01' -> 'Sửa'", "Bấm dấu cộng thêm 1 dòng phân công, để trống công ty; thêm quyền 'Thủ kho KT'",
           "Bấm 'Lưu'", "Khối Lịch sử cuối màn bấm 'Xem lịch sử'"), "—",
         E("Báo 'Vui lòng chọn công ty cho tất cả các dòng phân công quản lý phòng ban'",
           "Màn không chuyển trang", "Khối Lịch sử vẫn 2 mục (quyền 'Thủ kho KT' KHÔNG được lưu)")),
        (4, "Chọn trùng công ty ở 2 dòng", "P1", user_pre,
         S(MENU_USERS, "Mở màn Sửa 'NV kiểm thử 01'", "Thêm dòng mới, chọn lại Công ty A"), "Công ty: Công ty A",
         E("Dưới ô công ty dòng mới hiện 'Công ty này đã được chọn, vui lòng chọn công ty khác'",
           "Ô Phòng ban của dòng đó không có lựa chọn")),
        (5, "Chọn trùng phòng ban trong cùng công ty", "P2", user_pre,
         S(MENU_USERS, "Mở màn Sửa 'NV kiểm thử 01'", "Dòng Công ty A bấm 'Thêm phòng ban', chọn lại 'Phòng Kinh doanh 1'"), "—",
         E("Hiện 'Phòng ban này đã được chọn, vui lòng chọn phòng ban khác'", "Ô phòng ban vừa chọn bị bỏ trống lại")),
        (6, "Dòng phân công có công ty nhưng chưa chọn phòng ban", "P2", L(user_pre, "Lịch sử đang có 2 mục"),
         edit_steps("Thêm dòng Công ty B, không chọn phòng ban, không tick tất cả"), "—",
         E("Lưu thành công", "Không có mục mới nhắc tới Công ty B",
           "Mở lại màn Sửa không còn dòng Công ty B trống")),
        (7, "Người thực hiện đúng người bấm Lưu", "P1", user_pre,
         S("Đăng nhập QT2", "Sửa quyền của 'NV kiểm thử 01'", "Đăng nhập QT1, mở lịch sử 'NV kiểm thử 01'"), "—",
         E("Mục mới ghi 'Người thực hiện: Trần Thị Kiểm Thử — <phòng ban của QT2>'", "Thời gian đúng lúc QT2 bấm Lưu")),
    ]

    erp_pre = L(ACC, "Người dùng 'NV ERP 05' có quyền HRM 'Nhân viên kinh doanh' và 2 vai trò gán từ ERP: 'Kho - Thủ kho', 'Mua hàng - Nhân viên'")
    s5 = [
        (1, "Hiển thị vai trò gán từ ERP ở chế độ chỉ xem", "P0", erp_pre,
         S(MENU_USERS, "Dòng 'NV ERP 05' -> 'Sửa'", "Quan sát dưới ô 'Quyền'"), "—",
         E("Có dòng chữ xám 'Vai trò gán từ ERP (chỉ xem, không sửa ở màn này, được giữ nguyên khi Lưu):'",
           "Kèm 2 nhãn 'Kho - Thủ kho', 'Mua hàng - Nhân viên'",
           "2 vai trò này KHÔNG nằm trong ô 'Quyền', không bấm bỏ được")),
        (2, "Lưu không đổi gì vẫn giữ nguyên vai trò ERP", "P0", erp_pre,
         S(MENU_USERS, "Dòng 'NV ERP 05' -> 'Sửa'", "Không sửa gì, bấm 'Lưu'", "Mở lại màn Sửa 'NV ERP 05'",
           "Bấm 'Xem lịch sử' ở khối Lịch sử"), "—",
         E("Vẫn hiện đủ 2 vai trò ERP", "Người dùng vẫn dùng được các chức năng bên ERP như trước",
           "Lịch sử KHÔNG có mục mới")),
        (3, "Thêm quyền HRM không làm mất vai trò ERP, lịch sử không nhắc ERP", "P0", erp_pre,
         S(MENU_USERS, "Dòng 'NV ERP 05' -> 'Sửa'", "Ô Quyền thêm 'Thủ kho KT'", "Bấm 'Lưu'", "Mở lại màn Sửa", "Bấm 'Xem lịch sử'"),
         "Quyền thêm: Thủ kho KT",
         E("Vẫn hiện đủ 2 vai trò ERP", "Lịch sử chỉ có " + group("Quyền thêm mới", "Thủ kho KT"),
           "KHÔNG có nhóm 'Quyền đã xóa' mang tên vai trò ERP")),
        (4, "Người dùng không có vai trò ERP thì không hiện dòng ghi chú", "P2", user_pre,
         S(MENU_USERS, "Dòng 'NV kiểm thử 01' -> 'Sửa'"), "—",
         E("Không có dòng 'Vai trò gán từ ERP ...'")),
    ]

    s6 = [
        (1, "[Lỗi đã sửa] Lưu người dùng không làm mất vai trò gán từ ERP", "P0", erp_pre,
         S(MENU_USERS, "Mở màn Sửa 'NV ERP 05'", "Bỏ quyền HRM 'Nhân viên kinh doanh'", "Bấm 'Lưu'", "Mở lại màn Sửa"), "—",
         E("2 vai trò ERP vẫn còn nguyên", "Trước đây: bấm Lưu (kể cả không đổi gì) là mất sạch vai trò ERP")),
        (2, "[Lỗi đã sửa] Tick Quản lý tất cả phòng ban theo công ty lưu được", "P0", user_pre,
         edit_steps("Dòng Công ty A tick 'Quản lý tất cả phòng ban'"), "—",
         E("Lưu thành công, không báo lỗi hệ thống", "Mở lại màn Sửa: dòng Công ty A vẫn đang tick",
           "Lịch sử có dòng '- %s'" % dept("Tất cả phòng ban", "Công ty A"))),
        (3, "[Lỗi đã sửa] Người không có quyền không vào được màn Người dùng", "P0",
         "NV1 không có quyền %s" % Q_ROLE,
         S("Đăng nhập NV1", "Mở phân hệ Quản trị hệ thống", "Mở lại màn Danh sách người dùng từ lịch sử duyệt web"), "—",
         E("Không có menu", BLOCKED, "Trước đây: vào được và đổi quyền người khác")),
        (4, "[Lỗi đã sửa] Cờ Có/Không thống nhất trong popup", "P2", user_pre,
         edit_steps("Tick '%s'" % ALL), "—",
         E("Giá trị hiển thị 'Không' -> 'Có' (không dùng 'Bật/Tắt', 'true/false', '0/1')")),
    ]

    return build(output_file=out("Lịch sử Người dùng"), sheet_name="Trang tính1",
                 feature_name="Lịch sử thay đổi - Người dùng - Cập nhật ngày 30/09/2026",
                 module_name="Người dùng",
                 description_block=desc, role_tcs=roles,
                 sections=[("I", "POPUP LỊCH SỬ & KHỐI LỊCH SỬ MÀN SỬA", s1),
                           ("II", "BỘ LỌC LỊCH SỬ", s2),
                           ("III", "LỊCH SỬ KHI SỬA TỪNG TRƯỜNG", s3),
                           ("IV", "RÀNG BUỘC NHẬP LIỆU & CASE KHÔNG SINH LỊCH SỬ", s4),
                           ("V", "VAI TRÒ GÁN TỪ ERP", s5),
                           ("VI", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", s6)])


# =====================================================================================
# FILE 3 - LICH SU CAU HINH HCNS
# =====================================================================================
def build_hcns():
    pre_ts = L("Tài khoản HC1 (họ tên: Lê Thị Nhân Sự) có quyền %s, đang ở Công ty A" % Q_TS,
               "Tài khoản TL1 (họ tên: Phạm Văn Lương) CHỈ có quyền %s, ở Công ty A" % Q_TSL)
    sal_pre = L(pre_ts, "Công ty A đang có: Lương cơ bản 1,000,000; Phần trăm tăng lương thâm niên 2; Chu kỳ xét thâm niên tháng 12")
    open_sal = S(MENU_SALARY, "Bấm 'Lịch sử thay đổi' (góc phải trên khung cấu hình)")
    ins_pre = L(pre_ts, "Bảng Tỉ lệ đóng BHXH Công ty A có dòng Ngày hiệu lực 07/2026:",
                "NSDLĐ: Hưu trí 14, Ốm đau 3, TNLĐ 0.5, BH thất nghiệp 1, BHYT 3",
                "NLĐ: Hưu trí 8, Ốm đau 0, TNLĐ 0, BH thất nghiệp 1, BHYT 1.5")
    open_ins = S(MENU_INSURANCE, "Bấm 'Lịch sử thay đổi'")

    def sal_steps(action):
        return S(MENU_SALARY, action, "Bấm ra ngoài ô, chờ tới khi góc phải trên hiện thông báo xanh 'Cập nhật thành công'",
                 "Bấm 'Lịch sử thay đổi'")

    def ins_edit(action):
        return S(MENU_INSURANCE, "Dòng 07/2026 bấm nút Sửa (biểu tượng bút chì)", action,
                 "Bấm nút Lưu (biểu tượng đĩa mềm) của dòng", "Bấm 'Lịch sử thay đổi'")

    desc = [
        ("1. Mục đích tính năng",
         L("Ghi lại và cho xem lịch sử thay đổi các thông số cấu hình nhân sự của CÔNG TY ĐANG LÀM VIỆC.",
           "Màn Cấu hình nhân sự gốc đã tách làm 3 màn, mỗi màn có nút 'Lịch sử thay đổi' riêng và CHỈ thấy lịch sử phần của mình:",
           "- Cấu hình tiền lương (phân hệ Tính lương): Lương cơ bản, Phần trăm tăng lương thâm niên, Chu kỳ xét thâm niên tháng",
           "- Cấu hình định biên nhân sự (phân hệ Quản trị hệ thống): Dùng định biên nhân sự",
           "- Tỉ lệ đóng BHXH (phân hệ Bảo hiểm): thêm / sửa / xoá dòng tỉ lệ theo ngày hiệu lực",
           "Màn gốc (không còn trên menu) nếu mở được thì thấy toàn bộ.")),
        ("2. Đối tượng được tính / hiển thị",
         L("- Tiền lương / định biên: tên hành động 'Thay đổi thông tin' (chữ xanh dương, nhóm lọc Thay đổi thông tin): chỉ trường đổi, cũ đỏ -> mới xanh",
           "- Thêm dòng BHXH: 'Tạo mới' (chữ xanh lá, nhóm lọc Tạo mới): nhóm 'Dòng tỉ lệ đóng BHXH thêm mới:' 1 dòng",
           "  '- Ngày hiệu lực MM/YYYY — <10 cột tỉ lệ dạng Nhãn: giá trị, ngăn bằng dấu chấm phẩy>'",
           "- Sửa dòng BHXH: 'Thay đổi thông tin' (chữ xanh dương, nhóm lọc Thay đổi thông tin): nhóm 'Dòng tỉ lệ đóng BHXH sửa thông tin:'",
           "  '- Ngày hiệu lực MM/YYYY: <Cột>: cũ -> mới; ...' chỉ các cột đổi (kể cả Ngày hiệu lực)",
           "- Xoá dòng BHXH: 'Xóa' (chữ đỏ, nhóm lọc Thay đổi trạng thái): nhóm 'Dòng tỉ lệ đóng BHXH đã xóa:' 1 dòng đủ 10 cột trước khi xoá",
           "Nhãn cột BHXH (đúng chữ tiêu đề bảng): 'Người sử dụng lao động — Hưu trí, tử tuất (%)', '... — Ốm đau, thai sản (%)',",
           "'... — TNLĐ, BNN (%)', 'Người sử dụng lao động — BH thất nghiệp', 'Người sử dụng lao động — BHYT' và 5 cột tương ứng",
           "'Người lao động — ...' (BH thất nghiệp (%), BHYT (%)), cộng 'Ngày hiệu lực'.")),
        ("3. Đối tượng bị ẩn / không tính",
         L("- Thay đổi không làm đổi giá trị đã lưu: KHÔNG sinh mục (kể cả bấm Lưu dòng BHXH không sửa gì)",
           "- Nhập số thập phân vào % thâm niên / Chu kỳ: báo lỗi, KHÔNG lưu, KHÔNG sinh mục",
           "- Dòng BHXH thiếu Ngày hiệu lực hoặc tỉ lệ âm: báo lỗi, KHÔNG sinh mục",
           "- Các cột Tổng cộng (tự tính) KHÔNG được ghi lịch sử",
           "- Tỷ suất lợi nhuận mức sàn (màn Cấu hình duyệt giá) KHÔNG thuộc lịch sử HCNS",
           "- Lịch sử của công ty khác không hiện")),
        ("4. Bộ lọc thời gian áp dụng cho",
         L(FILTER_DESC, GROUP_RULE, "Ô 'Người thực hiện' liệt kê nhân sự của công ty đang làm việc.")),
        ("5. Cấu trúc dữ liệu / cây phân cấp",
         L("Mỗi công ty có 1 bộ thông số lương + định biên và nhiều dòng tỉ lệ BHXH (mỗi dòng 1 tháng hiệu lực).",
           "Tên dòng BHXH trong lịch sử là 'Ngày hiệu lực MM/YYYY' để biết dòng nào bị đổi (tên hành động không còn kèm ngày).")),
        ("6. Quy tắc cộng dồn / deduplicate",
         L("- Màn Cấu hình tiền lương và định biên TỰ LƯU khi đổi giá trị (không có nút Lưu); tiền lương gom 0,6 giây sau lần gõ cuối",
           "- Mỗi lần lưu có thay đổi = 1 mục; gõ ngắt quãng lâu hơn 0,6 giây có thể sinh nhiều mục",
           "- Popup ghi theo giá trị THẬT đã lưu")),
        ("7. Phân quyền cấp",
         L("- %s: thấy cả 3 màn + màn gốc, xem được lịch sử cả 3" % Q_TS,
           "- %s: chỉ thấy màn Cấu hình tiền lương và lịch sử của nó" % Q_TSL,
           "- %s: sửa được Tỷ suất lợi nhuận mức sàn ở màn Cấu hình duyệt giá, KHÔNG vào được 3 màn HCNS" % Q_ASSIGN,
           "- Không có quyền nào: không thấy 3 mục menu, mở lại màn bị chuyển sang trang không tìm thấy")),
        ("8. Cách tính các ô thống kê",
         L("Không áp dụng cho popup lịch sử.",
           "Ghi chú: các cột Tổng cộng trên bảng BHXH = tổng các cột % cùng nhóm, KHÔNG xuất hiện trong lịch sử.")),
        ("9. Ghi chú đọc bảng",
         L(LAYOUT_NOTE,
           "- Số hiển thị chuẩn quốc tế: phẩy ngăn nghìn, chấm thập phân (1,500,000 ; 0.5)",
           "- Ngày hiệu lực hiển thị MM/YYYY; dòng BHXH thêm / xoá dài nên bị cắt, bấm 'Xem thêm' để xem đủ 10 cột",
           "- Lưu ý: mục menu 3 màn này còn phụ thuộc cấu hình 'Cài đặt phân hệ' (ẩn mục menu với nhân sự không nằm trong danh sách xem đầy đủ);",
           "  màn bị ẩn thì mở sẽ sang trang 'tính năng không khả dụng' — TC phân quyền giả định 3 mục đang BẬT ở Cài đặt phân hệ",
           "- Dùng định biên hiển thị Có / Không",
           "- Lương cơ bản là trường bắt buộc (dấu * đỏ): xoá trắng thì báo 'Bắt buộc phải nhập' dưới ô, KHÔNG lưu, KHÔNG sinh mục",
           "- Ô tỉ lệ BHXH để trống khi lưu được ghi là 0")),
    ]

    roles = [
        ("01", "Quyền 'Thiết lập thông số' thấy cả 3 màn và nút Lịch sử", "P0", pre_ts,
         S("Đăng nhập HC1", MENU_SALARY, MENU_MANPOWER, MENU_INSURANCE), "—",
         E("Cả 3 mục menu hiển thị và mở được", "Mỗi màn có nút 'Lịch sử thay đổi' ở góc phải trên")),
        ("02", "Chỉ có 'Thiết lập thông số lương' chỉ vào được Cấu hình tiền lương", "P0",
         L(pre_ts, "Công ty A đã có 2 mục lịch sử tiền lương", "3 mục menu cấu hình đang BẬT ở màn Cài đặt phân hệ"),
         S("Đăng nhập TL1", "Mở phân hệ Tính lương", "Bấm 'Cấu hình tiền lương' -> bấm 'Lịch sử thay đổi'",
           "Mở phân hệ Quản trị hệ thống, nhóm 'Cài đặt chung'", "Mở phân hệ Bảo hiểm, nhóm 'Cấu hình'"),
         "—",
         E("Tính lương có mục 'Cấu hình tiền lương', mở được, có nút 'Lịch sử thay đổi'",
           "Popup 'Lịch sử thay đổi: Cấu hình tiền lương' mở được, hiện đủ 2 mục như tài khoản HC1 xem",
           "KHÔNG có mục 'Cấu hình định biên nhân sự'",
           "KHÔNG có mục 'Tỉ lệ đóng BHXH' (nhóm 'Cấu hình' của phân hệ Bảo hiểm bị ẩn nếu không còn mục nào)")),
        ("03", "Chỉ có 'Thiết lập thông số lương' mở lại màn khác bị chặn", "P0",
         L(pre_ts, "TL1 trước đây có thêm %s, đã mở 2 màn Định biên và Tỉ lệ đóng BHXH, nay đã bị gỡ" % Q_TS),
         S("TL1 đăng nhập lại", "Mở lại màn Cấu hình định biên nhân sự từ lịch sử duyệt web", "Làm tương tự với màn Tỉ lệ đóng BHXH"),
         "—", E("Cả 2 lần: " + BLOCKED, "TL1 không có cách nào xem lịch sử định biên / BHXH (kể cả dùng công cụ kiểm thử API gọi thẳng chức năng xem lịch sử: hệ thống từ chối, báo không có quyền)")),
        ("04", "Không có quyền nào không thấy 3 màn", "P0", "Tài khoản NV1 không có %s, %s" % (Q_TS, Q_TSL),
         S("Đăng nhập NV1", "Mở lần lượt 3 phân hệ Tính lương, Quản trị hệ thống, Bảo hiểm",
           "Mở lại màn Cấu hình tiền lương từ lịch sử duyệt web"), "—",
         E("Không thấy 3 mục menu cấu hình", BLOCKED)),
        ("05", "Quyền giao việc lưu được Tỷ suất lợi nhuận mức sàn nhưng không vào được màn HCNS", "P0",
         L("Tài khoản GV1 CHỈ có quyền %s" % Q_ASSIGN, "Tỷ suất lợi nhuận mức sàn Công ty A đang 10"),
         S("Đăng nhập GV1", MENU_PRICE, "Ô 'Tỷ suất lợi nhuận mức sàn (%)' nhập 15, bấm 'Lưu cấu hình' cùng khối",
           "Mở phân hệ Tính lương, Quản trị hệ thống, Bảo hiểm tìm 3 màn cấu hình HCNS"),
         "Tỷ suất lợi nhuận mức sàn (%): 15",
         E("Báo 'Đã lưu mức sàn 15%'", "Tải lại trang vẫn là 15",
           "KHÔNG thấy 3 mục menu cấu hình HCNS, không có cách nào sửa Lương cơ bản / Định biên / BHXH")),
        ("06", "Lưu Tỷ suất lợi nhuận không sinh lịch sử HCNS", "P1",
         L(pre_ts, "Đã làm TC-ROLE-05"), S("Đăng nhập HC1", open_sal, "Mở thêm lịch sử màn Định biên và Tỉ lệ đóng BHXH"), "—",
         E("Không popup nào có mục nhắc tới Tỷ suất lợi nhuận mức sàn")),
    ]

    s1 = [
        (1, "Bố cục popup màn Cấu hình tiền lương", "P0", sal_pre, open_sal, "—",
         popup_layout("Lịch sử thay đổi: Cấu hình tiền lương",
                      "Chỉ có mục 'Thay đổi thông tin' (chữ xanh dương) của tiền lương")),
        (2, "Bố cục popup màn Cấu hình định biên nhân sự", "P0", pre_ts,
         S(MENU_MANPOWER, "Bấm 'Lịch sử thay đổi'"), "—",
         popup_layout("Lịch sử thay đổi: Cấu hình định biên nhân sự",
                      "Chỉ có mục 'Thay đổi thông tin' (chữ xanh dương) của định biên")),
        (3, "Bố cục popup màn Tỉ lệ đóng BHXH", "P0", ins_pre, open_ins, "—",
         popup_layout("Lịch sử thay đổi: Tỉ lệ đóng BHXH",
                      "Chỉ có các mục của dòng tỉ lệ BHXH: 'Tạo mới' (xanh lá), 'Thay đổi thông tin' (xanh dương), 'Xóa' (đỏ)")),
        (4, "Mỗi màn chỉ thấy lịch sử phần của mình", "P0",
         L(pre_ts, "Trong ngày: đổi Lương cơ bản 1 lần, đổi Dùng định biên 1 lần, sửa 1 dòng BHXH 1 lần"),
         S(MENU_SALARY, "Bấm 'Lịch sử thay đổi'", "Đóng popup; " + MENU_MANPOWER + ", bấm 'Lịch sử thay đổi'",
           "Đóng popup; " + MENU_INSURANCE + ", bấm 'Lịch sử thay đổi'"), "—",
         E("Popup Tiền lương: chỉ mục đổi Lương cơ bản", "Popup Định biên: chỉ mục đổi Dùng định biên",
           "Popup BHXH: chỉ mục sửa dòng BHXH", "Không popup nào hiện mục rỗng")),
        (5, "Chưa có lịch sử", "P1", L(pre_ts, "Công ty C chưa từng đổi cấu hình định biên"),
         S("Đổi công ty làm việc sang Công ty C", MENU_MANPOWER, "Bấm 'Lịch sử thay đổi'"), "—",
         E("Hiện biểu tượng đồng hồ và '%s'" % EMPTY_TEXT, "Không có nút 'Bộ lọc'")),
        (6, "Thứ tự và thông tin mục", "P0", L(sal_pre, "Đã có 3 lần đổi lương ở 3 ngày khác nhau bởi HC1 và TL1"), open_sal, "—",
         E(*TIMELINE_COMMON + ["Dòng người thực hiện dạng 'Người thực hiện: Lê Thị Nhân Sự — <phòng ban>' / 'Người thực hiện: Phạm Văn Lương — <phòng ban>'"])),
    ]
    ins_steps = [MENU_INSURANCE, "Bấm 'Lịch sử thay đổi'"]
    s1 += filter_tcs(7, L(ins_pre, "HC1 thuộc phòng 'HCNS', HC2 (Vũ Văn Hai) thuộc phòng 'HCNS'"), ins_steps,
                     {"Tạo mới": 1, "Thay đổi thông tin": 2, "Thay đổi trạng thái": 1},
                     "'HCNS - Vũ Văn Hai'", "công ty đang làm việc", ("03/09/2026", "15/09/2026", "25/09/2026"),
                     extra_group="Mục 'Xóa' (xoá dòng BHXH) nằm ở nhóm 'Thay đổi trạng thái'; mục 'Tạo mới' (thêm dòng BHXH) ở nhóm 'Tạo mới'")
    s1 += [
        (14, "Loại hành động ở màn Tiền lương / Định biên", "P1", L(sal_pre, "Màn Tiền lương có 3 mục, màn Định biên có 2 mục"),
         S(MENU_SALARY, "Bấm 'Lịch sử thay đổi' -> 'Bộ lọc', lần lượt chọn 3 lựa chọn ở ô 'Loại hành động'",
           "Làm lại ở màn Cấu hình định biên nhân sự"), "—",
         E("Ô vẫn đủ 3 lựa chọn %s như mọi màn (không lọc bớt theo màn)" % GROUPS3,
           "'Thay đổi thông tin' ra đủ mục; 'Tạo mới' và 'Thay đổi trạng thái' hiện '%s'" % NO_MATCH)),
    ]

    s2 = [
        (1, "Sửa Lương cơ bản", "P0", sal_pre, sal_steps("Ô 'Lương cơ bản' nhập 1500000"),
         L("Lương cơ bản cũ: 1,000,000", "Lương cơ bản mới: 1,500,000"),
         E("Màn báo 'Cập nhật thành công' (không cần bấm Lưu)",
           "1 mục mới 'Thay đổi thông tin' (chữ xanh dương), người thực hiện HC1, thời gian lúc đổi",
           "Mục chỉ có " + diff("Lương cơ bản", "1,000,000", "1,500,000"))),
        (2, "Sửa Phần trăm tăng lương thâm niên", "P0", sal_pre, sal_steps("Ô 'Phần trăm tăng lương thâm niên (%)' nhập 3"),
         L("Cũ: 2", "Mới: 3"),
         E("Mục mới chỉ có " + diff("Phần trăm tăng lương thâm niên (%)", "2", "3"))),
        (3, "Sửa Chu kỳ xét thâm niên tháng", "P0", sal_pre, sal_steps("Ô 'Chu kỳ xét thâm niên tháng' nhập 24"),
         L("Cũ: 12", "Mới: 24"),
         E("Mục mới chỉ có " + diff("Chu kỳ xét thâm niên tháng", "12", "24"))),
        (4, "Phần trăm tăng lương thâm niên nhập số thập phân bị chặn", "P0", L(sal_pre, "Lịch sử đang có N mục"),
         S(MENU_SALARY, "Ô 'Phần trăm tăng lương thâm niên (%)' nhập 3.5", "Chờ 2 giây", "Tải lại trang", "Mở 'Lịch sử thay đổi'"),
         "Phần trăm tăng lương thâm niên (%): 3.5",
         E("Ô viền đỏ, dưới ô hiện 'Chỉ được nhập số nguyên', ô VẪN giữ 3.5 (không tự làm tròn)",
           "KHÔNG hiện 'Cập nhật thành công'", "Tải lại trang giá trị vẫn là 2", "Lịch sử vẫn N mục")),
        (5, "Chu kỳ xét thâm niên nhập số thập phân bị chặn", "P1", L(sal_pre, "Lịch sử đang có N mục"),
         S(MENU_SALARY, "Ô 'Chu kỳ xét thâm niên tháng' nhập 6.5", "Chờ 2 giây, mở 'Lịch sử thay đổi'"),
         "Chu kỳ xét thâm niên tháng: 6.5",
         E("Dưới ô hiện 'Chỉ được nhập số nguyên'", "Không lưu, lịch sử vẫn N mục")),
        (6, "Gõ liền mạch nhiều ký tự chỉ sinh 1 mục", "P1", sal_pre,
         sal_steps("Ô 'Lương cơ bản' xoá hết rồi gõ liền 2000000 (không dừng)"), "Lương cơ bản: 2,000,000",
         E("Chỉ 1 mục mới: " + diff("Lương cơ bản", "1,000,000", "2,000,000"),
           "KHÔNG có các mục trung gian 2 / 20 / 200...")),
        (7, "Xoá trắng Lương cơ bản bị chặn", "P0", L(sal_pre, "Lịch sử đang có N mục"),
         S(MENU_SALARY, "Xoá hết ô 'Lương cơ bản'", "Chờ 2 giây", "Tải lại trang", "Bấm 'Lịch sử thay đổi'"), "Lương cơ bản: (trống)",
         E("Nhãn 'Lương cơ bản' có dấu * đỏ", "Ô giữ TRỐNG (không tự thành 0), viền đỏ, dưới ô hiện 'Bắt buộc phải nhập'",
           "Không hiện 'Cập nhật thành công'", "Tải lại trang ô vẫn 1,000,000", "Lịch sử vẫn N mục")),
        (8, "Gõ lại đúng giá trị cũ không sinh mục", "P1", L(sal_pre, "Lịch sử đang có N mục"),
         sal_steps("Ô 'Chu kỳ xét thâm niên tháng' xoá rồi gõ lại 12"), "Chu kỳ xét thâm niên tháng: 12",
         E("Lịch sử vẫn N mục")),
        (9, "Tài khoản chỉ có quyền lương sửa và xem lịch sử được", "P0", sal_pre,
         S("Đăng nhập TL1", MENU_SALARY, "Ô 'Lương cơ bản' nhập 1200000", "Bấm 'Lịch sử thay đổi'"), "Lương cơ bản: 1,200,000",
         E("Báo 'Cập nhật thành công'", "Mục mới ghi 'Người thực hiện: Phạm Văn Lương — <phòng ban>'")),
        (10, "Số lớn hiển thị đúng định dạng", "P2", sal_pre, sal_steps("Ô 'Lương cơ bản' nhập 12345678"),
         "Lương cơ bản: 12,345,678", E("Lịch sử hiển thị '12,345,678' (phẩy ngăn nghìn)")),
    ]

    s3 = [
        (1, "Chuyển 'Không dùng định biên' sang 'Dùng định biên'", "P0", L(pre_ts, "Công ty A đang chọn 'Không dùng định biên'"),
         S(MENU_MANPOWER, "Chọn nút tròn 'Dùng định biên'", "Chờ 'Cập nhật thành công'", "Bấm 'Lịch sử thay đổi'"), "—",
         E("1 mục 'Thay đổi thông tin' (chữ xanh dương), người thực hiện HC1",
           "Chỉ có " + diff("Dùng định biên nhân sự", "Không", "Có"))),
        (2, "Chuyển ngược 'Dùng định biên' sang 'Không dùng định biên'", "P0", L(pre_ts, "Đang chọn 'Dùng định biên'"),
         S(MENU_MANPOWER, "Chọn 'Không dùng định biên'", "Bấm 'Lịch sử thay đổi'"), "—",
         E("Mục mới: " + diff("Dùng định biên nhân sự", "Có", "Không"))),
        (3, "Mở màn không đổi gì không sinh mục", "P1", L(pre_ts, "Lịch sử định biên đang có N mục"),
         S(MENU_MANPOWER, "Không bấm gì, bấm 'Lịch sử thay đổi'"), "—", E("Vẫn N mục")),
    ]

    ins_fields = [
        ("NSDLĐ", "Hưu trí, tử tuất (%)", "14", "14.5", "P0"),
        ("NSDLĐ", "Ốm đau, thai sản (%)", "3", "3.5", "P0"),
        ("NSDLĐ", "TNLĐ, BNN (%)", "0.5", "1", "P0"),
        ("NSDLĐ", "BH thất nghiệp", "1", "1.5", "P0"),
        ("NSDLĐ", "BHYT", "3", "4", "P0"),
        ("NLĐ", "Hưu trí, tử tuất (%)", "8", "9", "P0"),
        ("NLĐ", "Ốm đau, thai sản (%)", "0", "1", "P1"),
        ("NLĐ", "TNLĐ, BNN (%)", "0", "0.5", "P1"),
        ("NLĐ", "BH thất nghiệp (%)", "1", "2", "P1"),
        ("NLĐ", "BHYT (%)", "1.5", "2", "P1"),
    ]
    s4 = [
        (1, "Thêm dòng tỉ lệ đóng BHXH", "P0", pre_ts,
         S(MENU_INSURANCE, "Bấm dấu cộng ở cột cuối tiêu đề bảng", "Dòng mới: chọn Ngày hiệu lực 01/2027, nhập đủ 10 ô tỉ lệ",
           "Bấm Lưu (đĩa mềm) của dòng", "Bấm 'Lịch sử thay đổi'"),
         L("Ngày hiệu lực: 01/2027", "NSDLĐ: 14 / 3 / 0.5 / 1 / 3", "NLĐ: 8 / 0 / 0 / 1 / 1.5"),
         E("Báo 'Lưu thành công', dòng mới hiện trong bảng",
           "1 mục 'Tạo mới' chữ xanh lá (nhóm lọc Tạo mới), người thực hiện HC1",
           "Nhóm 'Dòng tỉ lệ đóng BHXH thêm mới:' có 1 dòng chữ xanh bắt đầu '- Ngày hiệu lực 01/2027 — Người sử dụng lao động — Hưu trí, tử tuất (%): 14; Người sử dụng lao động — Ốm đau, thai sản (%): 3; ...'",
           "Dòng dài bị cắt kèm 'Xem thêm'; bấm 'Xem thêm' thấy đủ 10 cột tới 'Người lao động — BHYT (%): 1.5', bấm 'Thu gọn' để thu lại",
           "KHÔNG có dòng Tổng cộng")),
        (2, "Thêm dòng bỏ trống vài ô tỉ lệ", "P2", pre_ts,
         S(MENU_INSURANCE, "Bấm dấu cộng, chọn Ngày hiệu lực 02/2027, chỉ nhập NSDLĐ Hưu trí 14", "Bấm Lưu dòng", "Mở lịch sử"),
         L("Ngày hiệu lực: 02/2027", "Người sử dụng lao động — Hưu trí, tử tuất (%): 14", "Các ô khác: trống"),
         E("Lưu thành công, các ô trống hiển thị 0", "Dòng trong nhóm 'Dòng tỉ lệ đóng BHXH thêm mới:' ghi các cột trống là 0 (không bỏ cột)")),
        (3, "Thêm dòng thiếu Ngày hiệu lực bị chặn", "P0", L(pre_ts, "Lịch sử BHXH đang có N mục"),
         S(MENU_INSURANCE, "Bấm dấu cộng, KHÔNG chọn Ngày hiệu lực, nhập Hưu trí 14", "Bấm Lưu dòng", "Mở lịch sử"),
         "Ngày hiệu lực: (trống)",
         E("Báo 'Lưu thất bại', dưới ô ngày hiện 'Bắt buộc phải nhập'", "Dòng vẫn ở chế độ sửa, số đã nhập còn nguyên",
           "Lịch sử vẫn N mục")),
        (4, "Nhập tỉ lệ âm bị chặn", "P1", L(ins_pre, "Lịch sử BHXH đang có N mục"),
         ins_edit("Ô NSDLĐ Hưu trí, tử tuất nhập -1"), "Người sử dụng lao động — Hưu trí, tử tuất (%): -1",
         E("Báo 'Lưu thất bại', dưới ô hiện 'Không được nhỏ hơn 0.'", "Ô vẫn giữ -1, dòng vẫn ở chế độ sửa", "Lịch sử vẫn N mục")),
        (5, "Sửa Ngày hiệu lực", "P0", ins_pre, ins_edit("Đổi Ngày hiệu lực sang 08/2026"), "Ngày hiệu lực: 07/2026 -> 08/2026",
         E("1 mục 'Thay đổi thông tin' chữ xanh dương (nhóm lọc Thay đổi thông tin)",
           "Nhóm 'Dòng tỉ lệ đóng BHXH sửa thông tin:' có đúng 1 dòng '- Ngày hiệu lực 08/2026: Ngày hiệu lực: 07/2026 (đỏ) -> 08/2026 (xanh)'",
           "Tên dòng lấy theo ngày hiệu lực MỚI")),
        (6, "Nhập số âm ở BH thất nghiệp của Người sử dụng lao động bị chặn", "P0", L(ins_pre, "Lịch sử BHXH đang có N mục"),
         ins_edit("Nhóm cột 'Người sử dụng lao động', ô 'BH thất nghiệp' nhập -1"), "Người sử dụng lao động — BH thất nghiệp: -1",
         E("Báo 'Lưu thất bại', dưới ô BH thất nghiệp hiện 'Không được nhỏ hơn 0.' (chặn giống các cột tỉ lệ khác)",
           "Ô vẫn giữ -1 (không tự sửa số), dòng vẫn ở chế độ sửa", "Lịch sử vẫn N mục")),
    ]
    n = 7
    for grp, col, old, new, prio in ins_fields:
        head = "Người sử dụng lao động" if grp == "NSDLĐ" else "Người lao động"
        label = "%s — %s" % (head, col)
        s4.append((n, "Sửa cột %s" % label, prio, ins_pre,
                   ins_edit("Nhóm cột '%s', ô '%s' đổi thành %s" % (head, col, new)),
                   L("%s cũ: %s" % (label, old), "%s mới: %s" % (label, new)),
                   E("1 mục 'Thay đổi thông tin' chữ xanh dương",
                     "Nhóm 'Dòng tỉ lệ đóng BHXH sửa thông tin:' có dòng '- Ngày hiệu lực 07/2026: %s: %s (đỏ) -> %s (xanh)'" % (label, old, new),
                     "Không có cột nào khác trong dòng đó")))
        n += 1
    s4 += [
        (n, "Sửa nhiều cột trong 1 lần Lưu", "P1", ins_pre,
         ins_edit("Đổi NSDLĐ Hưu trí 14 -> 15 và NLĐ BHYT 1.5 -> 2"), "—",
         E("Đúng 1 mục, có 2 dòng thay đổi tương ứng")),
        (n + 1, "Bấm Lưu dòng không sửa gì không sinh mục", "P0", L(ins_pre, "Lịch sử BHXH đang có N mục"),
         ins_edit("Không đổi ô nào"), "—", E("Báo 'Lưu thành công'", "Lịch sử vẫn N mục, KHÔNG có mục rỗng")),
        (n + 2, "Huỷ sửa dòng không sinh mục", "P1", L(ins_pre, "Lịch sử BHXH đang có N mục"),
         S(MENU_INSURANCE, "Dòng 07/2026 bấm Sửa, đổi Hưu trí thành 20", "Bấm nút Hủy (biểu tượng dấu X) của dòng", "Mở lịch sử"), "—",
         E("Dòng trở lại giá trị cũ 14", "Lịch sử vẫn N mục")),
        (n + 3, "Xoá dòng tỉ lệ đóng BHXH", "P0", ins_pre,
         S(MENU_INSURANCE, "Dòng 07/2026 bấm Xoá (thùng rác)",
           "Hộp thoại 'Xác nhận hủy/xóa' hỏi 'Bạn có chắc chắn muốn hủy/xóa bản ghi này không?' -> bấm 'Đồng ý'",
           "Bấm 'Lịch sử thay đổi'"), "—",
         E("Báo 'Xoá thành công', dòng biến mất",
           "1 mục 'Xóa' chữ đỏ, lọc ra khi chọn Loại hành động 'Thay đổi trạng thái'",
           "Nhóm 'Dòng tỉ lệ đóng BHXH đã xóa:' có 1 dòng chữ đỏ '- Ngày hiệu lực 07/2026 — ...' đủ 10 cột với giá trị trước khi xoá (bấm 'Xem thêm' để xem hết)")),
        (n + 4, "Huỷ hộp thoại xoá", "P2", ins_pre,
         S(MENU_INSURANCE, "Dòng 07/2026 bấm Xoá", "Bấm 'Huỷ' trên hộp thoại 'Xác nhận hủy/xóa'"), "—", E("Dòng còn nguyên, không sinh mục")),
    ]

    s5 = [
        (1, "Lịch sử theo công ty đang làm việc", "P0",
         L(pre_ts, "HC1 làm việc được ở Công ty A và Công ty B", "Công ty A có 3 mục lịch sử tiền lương, Công ty B chưa có"),
         S("Ở Công ty A mở lịch sử Cấu hình tiền lương", "Đổi công ty làm việc sang Công ty B", "Mở lại lịch sử Cấu hình tiền lương"), "—",
         E("Công ty A: 3 mục", "Công ty B: 'Chưa có lịch sử thao tác nào.'", "Không lẫn mục của công ty khác")),
        (2, "Đổi cấu hình ở Công ty B không ảnh hưởng Công ty A", "P1", pre_ts,
         S("Ở Công ty B đổi Dùng định biên", "Đổi về Công ty A, mở lịch sử Định biên"), "—",
         E("Công ty A không có mục của thay đổi vừa làm", "Giá trị Dùng định biên của Công ty A không đổi")),
        (3, "Bảng BHXH và lịch sử BHXH theo công ty", "P1", pre_ts,
         S("Ở Công ty B thêm dòng BHXH 03/2027", "Đổi về Công ty A mở màn Tỉ lệ đóng BHXH và lịch sử"), "—",
         E("Công ty A không thấy dòng 03/2027", "Lịch sử Công ty A không có mục 'Tạo mới' của dòng 03/2027")),
        (4, "Màn Cấu hình nhân sự gốc xem được toàn bộ", "P2",
         L(pre_ts, "Màn gốc không còn trên menu; QA mở từ lịch sử duyệt web đã có trước khi tách màn"),
         S("Đăng nhập HC1", "Mở lại màn Cấu hình nhân sự gốc", "Bấm 'Lịch sử thay đổi'"), "—",
         E("Tiêu đề popup 'Lịch sử thay đổi: Cấu hình nhân sự'",
           "Thấy cả mục tiền lương, định biên và BHXH; mọi mục mang nhãn chuẩn ('Thay đổi thông tin' xanh dương; dòng BHXH thêm / xoá là 'Tạo mới' / 'Xóa')",
           "Ô 'Loại hành động' vẫn là 3 nhóm %s như mọi màn" % GROUPS3)),
        (5, "Màn gốc chặn người không có 'Thiết lập thông số'", "P1", pre_ts,
         S("Đăng nhập TL1", "Mở lại màn Cấu hình nhân sự gốc từ lịch sử duyệt web"), "—", E(BLOCKED)),
    ]

    s6 = [
        (1, "[Lỗi đã sửa] Popup lịch sử tách theo từng màn", "P0",
         L(pre_ts, "Có đủ mục tiền lương, định biên, BHXH"), S(MENU_MANPOWER, "Bấm 'Lịch sử thay đổi'"), "—",
         E("Chỉ thấy mục định biên", "Trước đây: màn nào cũng hiện toàn bộ lịch sử của màn Cấu hình gốc")),
        (2, "[Lỗi đã sửa] % tăng lương thâm niên ghi đúng giá trị đã lưu", "P0", sal_pre,
         S(MENU_SALARY, "Nhập 3.5 vào ô Phần trăm tăng lương thâm niên (%)", "Sửa lại thành 4", "Mở 'Lịch sử thay đổi'"), "—",
         E("3.5 bị chặn với 'Chỉ được nhập số nguyên'", "Chỉ có 1 mục '2 -> 4'",
           "Trước đây: gửi 3.5, hệ thống tự làm tròn 4 nhưng lịch sử ghi 3.5 lệch với dữ liệu thật")),
        (3, "[Lỗi đã sửa] Lưu dòng BHXH không đổi không sinh mục rỗng", "P0", ins_pre, ins_edit("Không đổi gì"), "—",
         E("Không có mục mới", "Trước đây: sinh mục sửa dòng BHXH không có nội dung")),
        (4, "[Lỗi đã sửa] Sửa dòng BHXH cũ không chạm ô ngày vẫn lưu được", "P1", ins_pre,
         ins_edit("Chỉ đổi NSDLĐ BHYT 3 -> 3.5, không chạm Ngày hiệu lực"), "—",
         E("Lưu thành công, Ngày hiệu lực vẫn 07/2026", "Dòng sửa thông tin chỉ có 'Người sử dụng lao động — BHYT: 3 -> 3.5', không có Ngày hiệu lực")),
        (5, "[Lỗi đã sửa] Menu 3 màn HCNS gắn đúng quyền", "P0", pre_ts,
         S("Đăng nhập TL1 kiểm tra menu", "Đăng nhập NV1 (không quyền) kiểm tra menu"), "—",
         E("TL1 chỉ thấy Cấu hình tiền lương", "NV1 không thấy màn nào (nhóm 'Cấu hình' của phân hệ Bảo hiểm bị ẩn hẳn)",
           "Trước đây: ai cũng thấy và sửa được cả 3 màn")),
        (6, "[Lỗi đã sửa] Quyền giao việc lưu được Tỷ suất lợi nhuận mức sàn", "P0",
         "GV1 chỉ có quyền %s" % Q_ASSIGN, S("Đăng nhập GV1", MENU_PRICE, "Nhập 12, bấm 'Lưu cấu hình' khối Tỷ suất lợi nhuận mức sàn"),
         "Tỷ suất lợi nhuận mức sàn (%): 12",
         E("Báo 'Đã lưu mức sàn 12%'", "Trước đây: bị từ chối vì thiếu quyền Thiết lập thông số")),
    ]

    return build(output_file=out("Lịch sử Cấu hình HCNS"), sheet_name="Trang tính1",
                 feature_name="Lịch sử thay đổi - Cấu hình HCNS - Cập nhật ngày 30/09/2026",
                 module_name="Cấu hình HCNS",
                 description_block=desc, role_tcs=roles,
                 sections=[("I", "POPUP LỊCH SỬ & BỘ LỌC", s1),
                           ("II", "CẤU HÌNH TIỀN LƯƠNG - TỪNG TRƯỜNG", s2),
                           ("III", "CẤU HÌNH ĐỊNH BIÊN NHÂN SỰ", s3),
                           ("IV", "TỈ LỆ ĐÓNG BHXH - THÊM / SỬA TỪNG CỘT / XÓA", s4),
                           ("V", "CÔ LẬP DỮ LIỆU THEO CÔNG TY & MÀN GỐC", s5),
                           ("VI", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", s6)])


# =====================================================================================
# FILE 4 - LICH SU CAU HINH GIAO VIEC
# =====================================================================================
def build_assign():
    pre = L("Tài khoản GV1 (họ tên: Hoàng Văn Giao Việc) có quyền %s, đang ở Công ty A" % Q_ASSIGN,
            "Tài khoản GV2 (họ tên: Đỗ Thị Cấu Hình) cùng quyền, cùng Công ty A")
    COMMON_TITLE = "Lịch sử thay đổi: Cấu hình phân hệ giao việc — Thông tin chung"
    PLACES_TITLE = "Lịch sử thay đổi: Cấu hình phân hệ giao việc — Giới hạn khoảng cách tính công tác phí"

    def common_steps(action):
        return S(MENU_ASSIGN, "Tab 'Thông tin chung': " + action, "Bấm 'Lưu' cuối tab",
                 "Bấm 'Lịch sử thay đổi' (cạnh nút Lưu)")

    def places_steps(action):
        return S(MENU_ASSIGN, "Tab 'Giới hạn khoảng cách tính công tác phí': " + action, "Bấm 'Lưu' cuối tab",
                 "Bấm 'Lịch sử thay đổi' (cạnh nút Lưu)")

    PRI = "Tab 'Quản lý dự án' -> tab con 'Cấu hình mức độ ưu tiên'"
    DL = "Tab 'Quản lý dự án' -> tab con 'Cấu hình hạn'"
    PC = "Tab 'Quản lý dự án' -> tab con 'Đóng dự án tự động'"

    desc = [
        ("1. Mục đích tính năng",
         L("Ghi lại và cho xem lịch sử thay đổi màn 'Cấu hình chung (Quy chế thu nhập kỹ thuật - công nghệ)' của phân hệ Công việc,",
           "theo CÔNG TY ĐANG LÀM VIỆC. Có 5 nút 'Lịch sử thay đổi' riêng, mỗi nút chỉ thấy lịch sử phần của mình:",
           "1) Tab Thông tin chung  2) Tab Giới hạn khoảng cách tính công tác phí",
           "3) Cấu hình mức độ ưu tiên  4) Cấu hình hạn  5) Đóng dự án tự động (3 tab con của tab Quản lý dự án)")),
        ("2. Đối tượng được tính / hiển thị",
         L("- Thông tin chung: 23 trường đơn (4 hệ số, 7 khoản hỗ trợ, 2 ô gia hạn, 8 ô bảng Hỗ trợ lưu trú và Công tác phí nước ngoài, 2 ô Tất cả)",
           "  + 3 danh sách: Khung giờ tính ngày xuất phát, Chức vụ được tính PCT kỹ thuật, Chức vụ luôn được tính đủ công hành chính",
           "- Giới hạn khoảng cách: Số Km hỗ trợ lưu trú, Số Km hỗ trợ công tác phí, Danh sách địa điểm gốc",
           "- Mức độ ưu tiên: thêm = 'Tạo mới' (xanh lá, nhóm lọc Tạo mới); sửa và đổi thứ tự = 'Thay đổi thông tin' (xanh dương, nhóm lọc Thay đổi thông tin);",
           "  xoá = 'Xóa' (đỏ, nhóm lọc Thay đổi trạng thái). Tên mức KHÔNG nằm ở tên hành động mà ở nội dung, theo nhóm:",
           "  'Mức độ ưu tiên thêm mới:' - '- <Tên> — Số ngày phản hồi: ...; Số giờ phản hồi: ...; Mã màu: ...' (chữ xanh);",
           "  'Mức độ ưu tiên sửa thông tin:' - '- <Tên>: <Trường>: cũ -> mới' (chỉ trường đổi); 'Mức độ ưu tiên đã xóa:' - '- <Tên> — ...' (chữ đỏ);",
           "  đổi thứ tự hiện 'STT n: <tên cũ> -> <tên mới>' cho từng vị trí đổi. 4 trường: Tên mức độ ưu tiên, Số ngày phản hồi, Số giờ phản hồi, Mã màu",
           "- Cấu hình hạn: 9 trường",
           "- Đóng dự án tự động: 4 tham số chung + Thời hạn (tháng) từng giai đoạn dự án",
           "Mục cập nhật chỉ hiện trường đổi: cũ đỏ -> mới xanh; danh sách theo nhóm 'Khung giờ / Chức vụ / Địa điểm gốc thêm mới:' (xanh) và '... đã xóa:' (đỏ)",
           "Mọi mục của Thông tin chung, Giới hạn khoảng cách, Cấu hình hạn, Đóng dự án tự động thuộc nhóm lọc 'Thay đổi thông tin'")),
        ("3. Đối tượng bị ẩn / không tính",
         L("- Lưu không đổi gì: KHÔNG sinh mục (cả 5 phần)",
           "- Kéo thả rồi thả lại đúng chỗ cũ: KHÔNG sinh mục",
           "- Lưu bị chặn do lỗi nhập liệu (báo đỏ dưới ô): KHÔNG sinh mục",
           "- Thay đổi của tab khác trong cùng lần Lưu: không hiện ở popup của tab này",
           "- Lịch sử của công ty khác: không hiện (trừ Thời hạn theo giai đoạn - xem mục 9)")),
        ("4. Bộ lọc thời gian áp dụng cho",
         L(FILTER_DESC, GROUP_RULE, "Ô 'Người thực hiện' liệt kê nhân sự của công ty đang làm việc.")),
        ("5. Cấu trúc dữ liệu / cây phân cấp",
         L("Nhãn trường trong popup: 'Hệ số công hành chính tối đa — Bảo hành', 'Phiếu công tác kỹ thuật — Phòng tại khu du lịch (VND/phòng)',",
           "'Thời gian có thể gia hạn phiếu giao công tác — Giờ' ... (nhãn = đúng chữ trên form, không viết tắt). Khung giờ ghi 'Trước HH:mmh — X công'. Địa điểm ghi 'Tên (vĩ độ, kinh độ)'.",
           "Đổi thứ tự mức ưu tiên ghi theo vị trí: 'STT 1: Tên cũ -> Tên mới'.",
           "Lưu ý: 2 danh sách chức vụ cùng hiện nhóm 'Chức vụ thêm mới:' / 'Chức vụ đã xóa:' — không ghi rõ thuộc danh sách nào (đã ghi nhận để chốt).")),
        ("6. Quy tắc cộng dồn / deduplicate",
         L("- 1 lần Lưu = 1 mục (Đóng dự án tự động: gom mọi tham số + giai đoạn đổi trong 1 lần Lưu thành 1 mục)",
           "- Tab Thông tin chung và tab Giới hạn khoảng cách dùng CHUNG 1 nút Lưu dữ liệu: Lưu ở tab nào cũng lưu cả 2 tab,",
           "  nhưng mỗi popup chỉ hiện phần của tab mình",
           "- Sửa tên hoặc toạ độ 1 địa điểm gốc hiển thị là bỏ địa điểm cũ + thêm địa điểm mới")),
        ("7. Phân quyền cấp",
         L("%s: thấy menu, vào màn, xem cả 5 popup lịch sử." % Q_ASSIGN,
           "Không có quyền: không thấy menu, mở lại màn bị chuyển sang trang không tìm thấy.",
           "Quyền này cũng dùng cho màn Cấu hình duyệt giá (phân hệ Bán hàng).")),
        ("8. Cách tính các ô thống kê", "Không áp dụng - popup lịch sử không có ô thống kê."),
        ("9. Ghi chú đọc bảng",
         L(LAYOUT_NOTE,
           "- Tiền hiển thị phẩy ngăn nghìn (200,000); cờ Tất cả hiển thị Có / Không; Mã màu hiện dạng chữ (#RRGGBB), không còn ô màu",
           "- Xoá mức độ ưu tiên: 4 dòng 'giá trị cũ -> (trống)' (quy ước chung của khung lịch sử)",
           "- Ô tiền KHÔNG bắt buộc để trống thì giữ trống (không tự thành 0)",
           "- Đóng dự án tự động: giai đoạn để trống hiển thị 'Không tự đóng'",
           "- Lưu ý: Thời hạn theo giai đoạn đang dùng chung mọi công ty nên lịch sử phần này hiện ở mọi công ty",
           "- Nhãn trường trong mọi popup = đúng chữ trên form (kèm đơn vị cạnh ô), vd 'Cảnh báo sớm Issue trước (ngày)',",
           "  'Hạn đóng khi dự án chưa có báo giá (tháng)'; lịch sử ghi trước khi thống nhất nhãn cũng hiển thị theo nhãn mới",
           "- Cấu hình hạn: 3 ô để trống/0 sẽ lấy mặc định (Hạn nhập biên bản meeting sau = 1, Cảnh báo trước khi tự hủy meeting = 3,",
           "  Cảnh báo trước khi đóng nhu cầu = 3 khi để trống)")),
    ]

    roles = [
        ("01", "Có quyền thấy menu và 5 nút Lịch sử", "P0", pre,
         S("Đăng nhập GV1", MENU_ASSIGN, "Lần lượt mở 2 tab đầu và 3 tab con của 'Quản lý dự án'"), "—",
         E("Menu hiển thị, màn mở được, tiêu đề màn 'Cấu hình phân hệ giao việc'",
           "3 tab: 'Thông tin chung', 'Giới hạn khoảng cách tính công tác phí', 'Quản lý dự án' (3 tab con: 'Cấu hình mức độ ưu tiên', 'Cấu hình hạn', 'Đóng dự án tự động')",
           "Cả 5 phần đều có nút 'Lịch sử thay đổi'")),
        ("02", "Không có quyền không thấy menu", "P0", "Tài khoản NV1 không có quyền %s" % Q_ASSIGN,
         S("Đăng nhập NV1", "Mở phân hệ Công việc, nhóm 'Thiết lập'"), "—",
         E("KHÔNG có mục 'Cấu hình chung (Quy chế thu nhập kỹ thuật - công nghệ)'",
           "Các mục khác của nhóm 'Thiết lập' mà NV1 có quyền vẫn hiển thị bình thường; NV1 không có quyền mục nào thì cả nhóm 'Thiết lập' bị ẩn")),
        ("03", "Không có quyền mở lại màn bị chặn", "P0",
         "NV1 từng có quyền và đã mở màn, sau đó bị gỡ quyền %s" % Q_ASSIGN,
         S("NV1 đăng nhập lại", "Mở lại màn Cấu hình chung từ lịch sử duyệt web"), "—", E(BLOCKED)),
        ("04", "Công ty nào chỉ thấy mức ưu tiên của công ty đó", "P0",
         L(pre, "GV1 làm việc được ở Công ty A và Công ty B",
           "Công ty A có 3 mức: Khẩn cấp, Cao, Thường; Công ty B có 2 mức: Gấp B, Bình thường B"),
         S("Ở Công ty A mở " + PRI, "Đổi công ty làm việc sang Công ty B", "Mở lại " + PRI), "—",
         E("Công ty A thấy đúng 3 mức của A", "Công ty B thấy đúng 2 mức của B", "Không lẫn mức của công ty kia")),
        ("05", "Công ty nào chỉ thấy lịch sử của công ty đó", "P0",
         L(pre, "Công ty A đã có mục lịch sử ở cả 5 phần; Công ty B chưa đổi gì"),
         S("Đổi sang Công ty B", MENU_ASSIGN, "Mở lần lượt 4 popup: Thông tin chung, Giới hạn khoảng cách, Mức độ ưu tiên, Cấu hình hạn"), "—",
         E("Cả 4 popup hiện 'Chưa có lịch sử thao tác nào.'", "Không thấy mục nào của Công ty A")),
    ]

    s1 = [
        (1, "Nút Lịch sử và popup tab Thông tin chung", "P0", pre,
         S(MENU_ASSIGN, "Tab 'Thông tin chung' kéo xuống cuối", "Bấm 'Lịch sử thay đổi'"), "—",
         popup_layout(COMMON_TITLE, "Nút 'Lịch sử thay đổi' (biểu tượng đồng hồ) nằm bên trái nút 'Lưu' cuối tab",
                      "Mỗi mục có tên hành động 'Thay đổi thông tin' chữ xanh dương")),
        (2, "Nút Lịch sử và popup tab Giới hạn khoảng cách", "P0", pre,
         S(MENU_ASSIGN, "Tab 'Giới hạn khoảng cách tính công tác phí'", "Bấm 'Lịch sử thay đổi'"), "—",
         popup_layout(PLACES_TITLE, "Chỉ hiện thay đổi của 3 trường tab này (Số Km hỗ trợ lưu trú, Số Km hỗ trợ công tác phí, Danh sách địa điểm gốc)")),
        (3, "Nút Lịch sử và popup Cấu hình mức độ ưu tiên", "P0", pre, S(MENU_ASSIGN, PRI, "Bấm 'Lịch sử thay đổi' (cạnh nút 'Thêm dòng')"), "—",
         popup_layout("Lịch sử thay đổi: Cấu hình mức độ ưu tiên", "Nút nằm ở góc phải trên khung, bên trái 'Thêm dòng'")),
        (4, "Nút Lịch sử và popup Cấu hình hạn", "P0", pre, S(MENU_ASSIGN, DL, "Bấm 'Lịch sử thay đổi' (cạnh 'Lưu cấu hình')"), "—",
         popup_layout("Lịch sử thay đổi: Cấu hình hạn", "Mục có tên hành động 'Thay đổi thông tin' chữ xanh dương")),
        (5, "Nút Lịch sử và popup Đóng dự án tự động", "P0", pre, S(MENU_ASSIGN, PC, "Bấm 'Lịch sử thay đổi' (cạnh 'Lưu cấu hình')"), "—",
         popup_layout("Lịch sử thay đổi: Đóng dự án tự động", "Mục có tên hành động 'Thay đổi thông tin' chữ xanh dương")),
        (6, "Thứ tự mục, người thực hiện", "P1", L(pre, "GV1 rồi GV2 lần lượt sửa Cấu hình hạn"),
         S(MENU_ASSIGN, DL, "Bấm 'Lịch sử thay đổi'"), "—",
         E(*TIMELINE_COMMON + ["Mục trên cùng: 'Người thực hiện: Đỗ Thị Cấu Hình — <phòng ban>'; mục dưới: 'Người thực hiện: Hoàng Văn Giao Việc — <phòng ban>'"])),
    ]
    pri_steps = [MENU_ASSIGN, PRI, "Bấm 'Lịch sử thay đổi'"]
    s1 += filter_tcs(7, L(pre, "Lịch sử Mức độ ưu tiên Công ty A: 1 mục thêm mức, 1 mục sửa mức, 1 mục đổi thứ tự, 1 mục xoá mức"), pri_steps,
                     {"Tạo mới": 1, "Thay đổi thông tin": 2, "Thay đổi trạng thái": 1},
                     "'KTCN - Đỗ Thị Cấu Hình'", "công ty đang làm việc", ("02/09/2026", "12/09/2026", "22/09/2026"),
                     extra_group=("Tạo mới = mục 'Tạo mới' (nhóm 'Mức độ ưu tiên thêm mới:'); Thay đổi thông tin = 2 mục 'Thay đổi thông tin' "
                                  "(sửa mức và đổi thứ tự); Thay đổi trạng thái = mục 'Xóa' (nhóm 'Mức độ ưu tiên đã xóa:')"))
    s1 += [
        (14, "Bộ lọc 4 popup còn lại dùng cùng khuôn", "P1", L(pre, "Mỗi popup có ít nhất 2 mục"),
         S(MENU_ASSIGN, "Lần lượt mở popup tab Thông tin chung, tab Giới hạn khoảng cách, Cấu hình hạn, Đóng dự án tự động",
           "Mỗi popup bấm 'Bộ lọc', mở ô 'Loại hành động', chọn 'Thay đổi thông tin' rồi 'Tạo mới'"), "—",
         E("Cả 4 popup có đúng 4 ô 'Loại hành động', 'Người thực hiện', 'Từ ngày', 'Đến ngày' + nút 'Làm mới'",
           "KHÔNG còn ô 'Trường' (Thông tin chung / Giới hạn khoảng cách / Cấu hình hạn) và ô 'Nhóm cấu hình' (Đóng dự án tự động)",
           "Chọn 'Thay đổi thông tin' ra đủ mục (mọi thay đổi của 4 phần này đều là cập nhật); chọn 'Tạo mới' hiện '%s'" % NO_MATCH)),
    ]

    common_fields = [
        # (nhan form, khoi, nhan popup, cu, moi, prio)
        ("Bảo hành", "Hệ số công hành chính tối đa", "Hệ số công hành chính tối đa — Bảo hành", "1.2", "1.5", "P0"),
        ("Sửa chữa - bảo dưỡng", "Hệ số công hành chính tối đa", "Hệ số công hành chính tối đa — Sửa chữa - bảo dưỡng", "1.3", "1.5", "P0"),
        ("Lắp đặt", "Hệ số công hành chính tối đa", "Hệ số công hành chính tối đa — Lắp đặt", "1", "1.25", "P0"),
        ("Khác", "Hệ số công hành chính tối đa", "Hệ số công hành chính tối đa — Khác", "1", "0.8", "P0"),
        ("Hỗ trợ công tác phí - kỹ thuật", "Hỗ trợ công tác", "Hỗ trợ công tác phí - kỹ thuật", "150,000", "200,000", "P0"),
        ("Hỗ trợ lưu trú - kỹ thuật", "Hỗ trợ công tác", "Hỗ trợ lưu trú - kỹ thuật", "250,000", "300,000", "P0"),
        ("Đơn giá công khoán", "Hỗ trợ công tác", "Đơn giá công khoán", "500,000", "550,000", "P0"),
        ("Hỗ trợ công tác phí (vượt công định mức)", "Hỗ trợ công tác", "Hỗ trợ công tác phí (vượt công định mức)", "100,000", "120,000", "P0"),
        ("Hỗ trợ lưu trú (vượt công định mức)", "Hỗ trợ công tác", "Hỗ trợ lưu trú (vượt công định mức)", "200,000", "220,000", "P0"),
        ("Hỗ trợ công tác phí - PTC khác (Xe công ty)", "Hỗ trợ công tác", "Hỗ trợ công tác phí - PTC khác (Xe công ty)", "50,000", "60,000", "P1"),
        ("Hỗ trợ công tác phí - PCT khác (Xe ngoài)", "Hỗ trợ công tác", "Hỗ trợ công tác phí - PCT khác (Xe ngoài)", "80,000", "90,000", "P1"),
        ("Thời gian có thể gia hạn phiếu giao công tác - ô Giờ", "Hỗ trợ công tác", "Thời gian có thể gia hạn phiếu giao công tác — Giờ", "12:00", "13:30", "P0"),
        ("Thời gian có thể gia hạn phiếu giao công tác - ô Ngày", "Hỗ trợ công tác", "Thời gian có thể gia hạn phiếu giao công tác — Ngày", "0", "1", "P0"),
    ]
    trip_fields = [
        ("Phiếu công tác kỹ thuật", "Công tác phí nước ngoài", "Phiếu công tác kỹ thuật — Công tác phí nước ngoài", "200,000", "300,000", "P0"),
        ("Phiếu công tác kỹ thuật", "Phòng tiêu chuẩn (VND/phòng)", "Phiếu công tác kỹ thuật — Phòng tiêu chuẩn (VND/phòng)", "420,000", "450,000", "P0"),
        ("Phiếu công tác kỹ thuật", "Phòng tại khu du lịch (VND/phòng)", "Phiếu công tác kỹ thuật — Phòng tại khu du lịch (VND/phòng)", "600,000", "700,000", "P0"),
        ("Phiếu công tác kỹ thuật", "Phòng ba (VND/phòng)", "Phiếu công tác kỹ thuật — Phòng ba (VND/phòng)", "900,000", "950,000", "P1"),
        ("Phiếu công tác khác", "Công tác phí nước ngoài", "Phiếu công tác khác — Công tác phí nước ngoài", "150,000", "180,000", "P1"),
        ("Phiếu công tác khác", "Phòng tiêu chuẩn (VND/phòng)", "Phiếu công tác khác — Phòng tiêu chuẩn (VND/phòng)", "300,000", "350,000", "P1"),
        ("Phiếu công tác khác", "Phòng tại khu du lịch (VND/phòng)", "Phiếu công tác khác — Phòng tại khu du lịch (VND/phòng)", "500,000", "550,000", "P1"),
        ("Phiếu công tác khác", "Phòng ba (VND/phòng)", "Phiếu công tác khác — Phòng ba (VND/phòng)", "800,000", "850,000", "P1"),
    ]
    s2 = []
    n = 1
    base_pre = L(pre, "Tab Thông tin chung của Công ty A đang có đủ dữ liệu hợp lệ, giá trị cũ như cột Test Data")
    for form_lbl, block, pop, old, new, prio in common_fields:
        s2.append((n, "Sửa '%s'" % form_lbl, prio, base_pre,
                   common_steps("khối '%s', ô '%s' đổi thành %s" % (block, form_lbl, new)),
                   L("Giá trị cũ: %s" % old, "Giá trị mới: %s" % new),
                   E("Báo 'Thao tác thành công'",
                     "1 mục mới, người thực hiện GV1, thời gian lúc Lưu",
                     "Mục CHỈ có " + diff(pop, old, new))))
        n += 1
    for row, col, pop, old, new, prio in trip_fields:
        s2.append((n, "Sửa bảng lưu trú: %s - %s" % (row, col), prio, base_pre,
                   common_steps("khối 'Hỗ trợ lưu trú và Công tác phí nước ngoài', dòng '%s', cột '%s' đổi thành %s" % (row, col, new)),
                   L("Giá trị cũ: %s" % old, "Giá trị mới: %s" % new),
                   E("1 mục mới CHỈ có " + diff(pop, old, new), "Không có dòng của cột / loại phiếu khác")))
        n += 1
    s2 += [
        (n, "Tick 'Tất cả' ở Chức vụ được tính PCT kỹ thuật", "P0",
         L(base_pre, "Ô chức vụ đang chọn 'Kỹ sư', 'Kỹ thuật viên'"),
         common_steps("khối 'Chức vụ được tính PCT kỹ thuật (đi đường, công tác phí, lưu trú vượt)' tick 'Tất cả'"), "—",
         E("Ô chọn chức vụ bị xoá trống và khoá lại",
           "Mục mới có " + diff("Chức vụ được tính PCT kỹ thuật (đi đường, công tác phí, lưu trú vượt) — Tất cả", "Không", "Có"),
           "Và nhóm 'Chức vụ đã xóa:' 2 dòng chữ đỏ '- Kỹ sư', '- Kỹ thuật viên'")),
        (n + 1, "Tick 'Tất cả' ở Chức vụ luôn được tính đủ công hành chính", "P0",
         L(base_pre, "Ô chức vụ đang chọn 'Trưởng nhóm kỹ thuật'"),
         common_steps("khối 'Chức vụ luôn được tính đủ công hành chính (PCT kỹ thuật)' tick 'Tất cả'"), "—",
         E("Mục mới có " + diff("Chức vụ luôn được tính đủ công hành chính (PCT kỹ thuật) — Tất cả", "Không", "Có"),
           "Và nhóm 'Chức vụ đã xóa:' dòng chữ đỏ '- Trưởng nhóm kỹ thuật'")),
        (n + 2, "Bỏ tick 'Tất cả' và chọn chức vụ cụ thể", "P1",
         L(base_pre, "Khối Chức vụ được tính PCT kỹ thuật đang tick 'Tất cả'"),
         common_steps("bỏ tick 'Tất cả', chọn 'Kỹ sư'"), "—",
         E("Mục mới có " + diff("Chức vụ được tính PCT kỹ thuật (đi đường, công tác phí, lưu trú vượt) — Tất cả", "Có", "Không"),
           "Và nhóm 'Chức vụ thêm mới:' dòng chữ xanh '- Kỹ sư'")),
        (n + 3, "Thêm chức vụ vào 'Chức vụ được tính PCT kỹ thuật'", "P0", L(base_pre, "Đang chọn 'Kỹ sư'"),
         common_steps("ô chọn chức vụ thêm 'Kỹ thuật viên'"), "—",
         E("Mục mới chỉ có " + group("Chức vụ thêm mới", "Kỹ thuật viên") + " (chữ xanh)",
           "Lưu ý: nhóm không ghi tên danh sách 'Chức vụ được tính PCT kỹ thuật' (xem mục 5)")),
        (n + 4, "Bỏ chức vụ khỏi 'Chức vụ luôn được tính đủ công hành chính'", "P0", L(base_pre, "Đang chọn 'Trưởng nhóm kỹ thuật', 'Kỹ sư'"),
         common_steps("bỏ 'Kỹ sư' khỏi ô chức vụ của khối 'Chức vụ luôn được tính đủ công hành chính (PCT kỹ thuật)'"), "—",
         E("Mục mới chỉ có " + group("Chức vụ đã xóa", "Kỹ sư") + " (chữ đỏ)")),
        (n + 5, "Thêm khung giờ tính ngày xuất phát", "P0", L(base_pre, "Đang có khung 'Trước 08:00h - 1 công'"),
         S(MENU_ASSIGN, "Tab 'Thông tin chung', khối 'Khung giờ tính ngày xuất phát' bấm '+ Thêm mới' ở tiêu đề bảng",
           "Popup 'Thêm khung giờ': ô 'Trước giờ' chọn 11:00 trong danh sách giờ, ô 'Công được tính' nhập 0.5, bấm 'OK'", "Bấm 'Lưu' cuối tab", "Bấm 'Lịch sử thay đổi'"),
         L("Trước giờ: 11:00", "Công được tính: 0.5"),
         E("Bấm 'OK' xong popup tự đóng, bảng có thêm dòng 'Trước 11:00h' | 0.5 (giờ luôn đủ 2 chữ số)",
           "Mục mới có " + group("Khung giờ thêm mới", "Trước 11:00h — 0.5 công") + " (chữ xanh)",
           "Không nhắc tới khung 08:00 đang có")),
        (n + 6, "Xoá khung giờ tính ngày xuất phát", "P0", L(base_pre, "Đang có 2 khung 08:00 và 11:00"),
         common_steps("bấm biểu tượng thùng rác ở dòng 'Trước 11:00h'"), "—",
         E("Mục mới có " + group("Khung giờ đã xóa", "Trước 11:00h — 0.5 công") + " (chữ đỏ)")),
        (n + 7, "Ô tiền không bắt buộc để trống thì giữ trống", "P0",
         L(base_pre, "Hỗ trợ lưu trú (vượt công định mức) đang 200,000"),
         common_steps("xoá trắng ô 'Hỗ trợ lưu trú (vượt công định mức)'"), "Hỗ trợ lưu trú (vượt công định mức): (trống)",
         E("Lưu thành công", "Mục mới: " + diff("Hỗ trợ lưu trú (vượt công định mức)", "200,000", "(trống)"),
           "Tải lại trang ô vẫn TRỐNG, KHÔNG tự thành 0")),
        (n + 8, "Đơn giá công khoán không bắt buộc, để trống được lưu", "P0",
         L(base_pre, "Đơn giá công khoán đang 500,000"),
         common_steps("xoá trắng ô 'Đơn giá công khoán'"), "Đơn giá công khoán: (trống)",
         E("Nhãn 'Đơn giá công khoán' KHÔNG có dấu (*)", "Báo 'Thao tác thành công', không báo lỗi dưới ô",
           "Mục mới: " + diff("Đơn giá công khoán", "500,000", "(trống)"), "Tải lại trang ô vẫn TRỐNG, KHÔNG tự thành 0")),
        (n + 9, "Ô bắt buộc để trống bị chặn, không sinh mục", "P0", L(base_pre, "Lịch sử tab đang có N mục"),
         S(MENU_ASSIGN, "Tab 'Thông tin chung' xoá trắng ô 'Hỗ trợ công tác phí - kỹ thuật' (có dấu (*)) và ô hệ số 'Bảo hành'",
           "Bấm 'Lưu'", "Bấm 'Lịch sử thay đổi'"), "—",
         E("Báo 'Vui lòng kiểm tra lại thông tin nhập', tên tab 'Thông tin chung' chuyển màu đỏ",
           "Dưới 2 ô hiện lỗi đỏ, dữ liệu đã nhập còn nguyên", "Lịch sử vẫn N mục")),
        (n + 10, "Lưu không đổi gì không sinh mục", "P0", L(base_pre, "Lịch sử tab đang có N mục"),
         common_steps("không sửa gì"), "—", E("Báo 'Thao tác thành công'", "Lịch sử vẫn N mục")),
        (n + 11, "Sửa nhiều trường 1 lần gom 1 mục", "P1", base_pre,
         common_steps("đổi 'Bảo hành' 1.2 -> 1.4, 'Đơn giá công khoán' 500,000 -> 600,000, thêm chức vụ 'Kỹ thuật viên'"), "—",
         E("Đúng 1 mục có 3 thay đổi tương ứng")),
        (n + 12, "Lưu ở tab Giới hạn khoảng cách sau khi sửa tab Thông tin chung", "P1", base_pre,
         S(MENU_ASSIGN, "Tab 'Thông tin chung' đổi 'Lắp đặt' 1 -> 1.1 (KHÔNG bấm Lưu)",
           "Chuyển tab 'Giới hạn khoảng cách tính công tác phí', đổi 'Số Km hỗ trợ lưu trú' 39 -> 40, bấm 'Lưu'",
           "Mở popup lịch sử của tab Giới hạn khoảng cách", "Mở popup lịch sử của tab Thông tin chung"), "—",
         E("Popup Giới hạn khoảng cách: chỉ 'Số Km hỗ trợ lưu trú: 39 -> 40'",
           "Popup Thông tin chung: chỉ 'Hệ số công hành chính tối đa — Lắp đặt: 1 -> 1.1'",
           "Lưu ý: 1 nút Lưu lưu cả 2 tab")),
    ]

    s3 = [
        (1, "Sửa Số Km hỗ trợ lưu trú", "P0", L(pre, "Số Km hỗ trợ lưu trú đang 39"),
         places_steps("ô 'Số Km hỗ trợ lưu trú' nhập 40"), "39 -> 40",
         E("1 mục mới CHỈ có " + diff("Số Km hỗ trợ lưu trú", "39", "40"))),
        (2, "Sửa Số Km hỗ trợ công tác phí", "P0", L(pre, "Số Km hỗ trợ công tác phí đang 3"),
         places_steps("ô 'Số Km hỗ trợ công tác phí' nhập 5"), "3 -> 5",
         E("1 mục mới CHỈ có " + diff("Số Km hỗ trợ công tác phí", "3", "5"))),
        (3, "Thêm địa điểm gốc", "P0", L(pre, "Danh sách địa điểm gốc đang có 'Văn phòng HN'"),
         places_steps("bảng 'Danh sách địa điểm gốc' bấm biểu tượng '+' (Thêm) ở tiêu đề bảng, ô 'Nhập tên địa điểm' gõ '189 Phan Trọng Tuệ', bấm ô 'Nhấn để chọn trên bản đồ' rồi chọn điểm"),
         L("Tên địa điểm: 189 Phan Trọng Tuệ", "Tọa độ: 20.9524126, 105.81456"),
         E("Mục mới có " + group("Địa điểm gốc thêm mới", "189 Phan Trọng Tuệ (20.9524126, 105.81456)") + " (chữ xanh)")),
        (4, "Xoá địa điểm gốc", "P0", L(pre, "Có 2 địa điểm 'Văn phòng HN', '189 Phan Trọng Tuệ'"),
         places_steps("bấm Xóa ở dòng '189 Phan Trọng Tuệ'"), "—",
         E(group("Địa điểm gốc đã xóa", "189 Phan Trọng Tuệ (20.9524126, 105.81456)") + " (chữ đỏ)")),
        (5, "Sửa tên địa điểm gốc", "P1", L(pre, "Có địa điểm 'PTT' toạ độ 20.9524126, 105.81786"),
         places_steps("đổi tên 'PTT' thành '189 Phan Trọng Tuệ'"), "PTT -> 189 Phan Trọng Tuệ",
         E(group("Địa điểm gốc thêm mới", "189 Phan Trọng Tuệ (20.9524126, 105.81786)"), group("Địa điểm gốc đã xóa", "PTT (20.9524126, 105.81786)"))),
        (6, "Sửa toạ độ địa điểm gốc", "P1", L(pre, "Địa điểm 'Văn phòng HN' toạ độ 21.0285, 105.8542"),
         places_steps("bấm ô Tọa độ của 'Văn phòng HN', chọn điểm khác trên bản đồ"), "—",
         E("Nhóm 'Địa điểm gốc đã xóa:' dòng 'Văn phòng HN' kèm toạ độ cũ; nhóm 'Địa điểm gốc thêm mới:' dòng 'Văn phòng HN' kèm toạ độ mới")),
        (7, "Địa điểm thiếu tên bị chặn", "P1", L(pre, "Lịch sử tab đang có N mục"),
         places_steps("thêm dòng địa điểm, chọn toạ độ nhưng để trống tên"), "—",
         E("Báo 'Vui lòng kiểm tra lại thông tin nhập', lỗi đỏ dưới ô tên", "Lịch sử vẫn N mục")),
        (8, "Lưu tab không đổi gì", "P1", L(pre, "Lịch sử tab đang có N mục"), places_steps("không sửa gì"), "—",
         E("Lịch sử vẫn N mục")),
    ]

    pri_pre = L(pre, "Công ty A có 3 mức theo STT: 1 'Khẩn cấp' (1 ngày, 4 giờ, #dc2626), 2 'Cao' (2 ngày, 0 giờ, #f59e0b), 3 'Thường' (5 ngày, 0 giờ, #16a34a)")

    def pri_edit(action):
        return S(MENU_ASSIGN, PRI, "Dòng 'Cao' bấm 'Sửa'", action, "Bấm 'Lưu' của dòng", "Bấm 'Lịch sử thay đổi'")

    s4 = [
        (1, "Thêm mức độ ưu tiên", "P0", pri_pre,
         S(MENU_ASSIGN, PRI, "Bấm 'Thêm dòng' (hiện thông báo 'Thêm dòng thành công', cuối bảng có dòng mới ghi 'Chưa lưu')",
           "Nhập Tên, Số ngày phản hồi, Số giờ phản hồi, Mã màu", "Bấm 'Lưu' của dòng", "Bấm 'Lịch sử thay đổi'"),
         L("Tên mức độ ưu tiên: Thấp", "Số ngày phản hồi: 7", "Số giờ phản hồi: 0", "Mã màu: #64748b"),
         E("Báo 'Thêm mới thành công!'", "1 mục tên hành động 'Tạo mới' chữ xanh lá (nhóm lọc Tạo mới), người thực hiện GV1",
           "Nội dung: nhóm 'Mức độ ưu tiên thêm mới:' và 1 dòng chữ xanh '- Thấp — Số ngày phản hồi: 7; Số giờ phản hồi: 0; Mã màu: #64748b'")),
        (2, "Sửa Tên mức độ ưu tiên", "P0", pri_pre, pri_edit("Đổi Tên thành 'Cao hơn'"), "Cao -> Cao hơn",
         E("Báo 'Cập nhật thành công!'", "1 mục tên hành động 'Thay đổi thông tin' chữ xanh dương",
           "Nội dung: nhóm 'Mức độ ưu tiên sửa thông tin:' và 1 dòng '- Cao hơn: Tên mức độ ưu tiên: Cao (chữ đỏ) -> Cao hơn (chữ xanh)' (tên đầu dòng là tên MỚI sau khi sửa)",
           "CHỈ có trường Tên mức độ ưu tiên")),
        (3, "Sửa Số ngày phản hồi", "P0", pri_pre, pri_edit("Đổi Số ngày phản hồi 2 -> 3"), "2 -> 3",
         E("1 mục 'Thay đổi thông tin' chữ xanh dương; nhóm 'Mức độ ưu tiên sửa thông tin:' có đúng 1 dòng '- Cao: Số ngày phản hồi: 2 (chữ đỏ) -> 3 (chữ xanh)'")),
        (4, "Sửa Số giờ phản hồi", "P0", pri_pre, pri_edit("Đổi Số giờ phản hồi 0 -> 12"), "0 -> 12",
         E("1 mục 'Thay đổi thông tin' chữ xanh dương; nhóm 'Mức độ ưu tiên sửa thông tin:' có đúng 1 dòng '- Cao: Số giờ phản hồi: 0 (chữ đỏ) -> 12 (chữ xanh)'")),
        (5, "Sửa Mã màu", "P0", pri_pre, pri_edit("Đổi Mã màu thành #7c3aed (chọn bằng ô màu hoặc gõ tay)"), "#f59e0b -> #7c3aed",
         E("1 mục 'Thay đổi thông tin' chữ xanh dương; nhóm 'Mức độ ưu tiên sửa thông tin:' có đúng 1 dòng '- Cao: Mã màu: #f59e0b (chữ đỏ) -> #7c3aed (chữ xanh)'",
           "Mã màu hiện dạng chữ, không kèm ô màu")),
        (6, "Kéo thả đổi thứ tự", "P0", pri_pre,
         S(MENU_ASSIGN, PRI, "Giữ biểu tượng kéo ở cột STT của dòng 'Thường', kéo lên vị trí đầu", "Bấm 'Lịch sử thay đổi'"), "—",
         E("Hiện thông báo 'Đã đổi STT'", "1 mục tên hành động 'Thay đổi thông tin' chữ xanh dương (nhóm lọc Thay đổi thông tin), người thực hiện GV1",
           "Nội dung: 'STT 1: Khẩn cấp -> Thường', 'STT 2: Cao -> Khẩn cấp', 'STT 3: Thường -> Cao'")),
        (7, "Kéo rồi thả lại đúng chỗ cũ không sinh mục", "P0", L(pri_pre, "Lịch sử đang có N mục"),
         S(MENU_ASSIGN, PRI, "Kéo dòng 'Cao' đi rồi thả lại đúng vị trí STT 2", "Bấm 'Lịch sử thay đổi'"), "—",
         E("Thứ tự không đổi", "Lịch sử vẫn N mục")),
        (8, "Xoá mức độ ưu tiên", "P0", L(pri_pre, "Mức 'Thường' chưa được dùng ở đâu"),
         S(MENU_ASSIGN, PRI, "Dòng 'Thường' bấm nút thùng rác", "Hộp thoại 'Xác nhận xóa' hỏi 'Bạn có chắc muốn xóa mức độ ưu tiên 'Thường'?' -> bấm 'Xóa'",
           "Bấm 'Lịch sử thay đổi'"), "—",
         E("Báo 'Xóa mức độ ưu tiên thành công!'", "1 mục tên hành động 'Xóa' chữ đỏ, lọc ra khi chọn Loại hành động 'Thay đổi trạng thái'",
           "Nội dung: nhóm 'Mức độ ưu tiên đã xóa:' và 1 dòng chữ đỏ '- Thường — Số ngày phản hồi: 5; Số giờ phản hồi: 0; Mã màu: #16a34a'",
           "KHÔNG sinh thêm mục đổi thứ tự ('STT n: ...') dù các mức phía sau bị dồn STT")),
        (9, "Xoá mức đang được sử dụng bị chặn", "P1", L(pri_pre, "Mức 'Khẩn cấp' đang được dùng ở giai đoạn dự án", "Lịch sử đang có N mục"),
         S(MENU_ASSIGN, PRI, "Dòng 'Khẩn cấp' bấm thùng rác -> 'Xóa'", "Bấm 'Lịch sử thay đổi'"), "—",
         E("Báo 'Dữ liệu đang được sử dụng, vui lòng tải lại'", "Mức vẫn còn", "Lịch sử vẫn N mục")),
        (10, "Huỷ sửa và Lưu không đổi không sinh mục", "P1", L(pri_pre, "Lịch sử đang có N mục"),
         S(MENU_ASSIGN, PRI, "Dòng 'Cao' bấm 'Sửa', đổi Số ngày 2 -> 9, bấm 'Huỷ'", "Bấm 'Sửa' lại, không đổi gì, bấm 'Lưu'", "Mở lịch sử"), "—",
         E("Sau Huỷ số ngày trở về 2", "Lịch sử vẫn N mục")),
        (11, "Kiểm tra nhập liệu mức độ ưu tiên", "P1", L(pri_pre, "Lịch sử đang có N mục"),
         S(MENU_ASSIGN, PRI, "Bấm 'Thêm dòng', để trống Tên, Số giờ 24, Mã màu 'xanh'", "Bấm 'Lưu' của dòng", "Mở lịch sử"),
         L("Tên: (trống)", "Số giờ phản hồi: 24", "Mã màu: xanh"),
         E("Dưới ô Tên 'Bắt buộc.', dưới Số giờ 'Tối đa 23.', dưới Mã màu 'Sai định dạng (#RRGGBB).'",
           "Hiện khung thông báo 'Lỗi — Chưa hợp lệ — Sửa các trường đang báo lỗi rồi lưu lại.'", "Lịch sử vẫn N mục")),
        (12, "Tên quá 20 ký tự", "P2", pri_pre, S(MENU_ASSIGN, PRI, "Bấm 'Thêm dòng', nhập Tên 21 ký tự, bấm 'Lưu'"),
         "Tên: Mức ưu tiên cực kỳ gấp (22 ký tự)",
         E("Ô Tên chỉ nhận tối đa 20 ký tự: gõ tới ký tự 21 thì không vào thêm, bộ đếm dưới ô dừng ở '20/20'",
           "Không hiện lỗi; bấm 'Lưu' thì lưu tên 20 ký tự đầu 'Mức ưu tiên cực kỳ g'")),
        (13, "Tên trùng mức khác trong CÙNG công ty bị chặn", "P0", L(pri_pre, "Lịch sử đang có N mục"),
         S(MENU_ASSIGN, PRI, "Bấm 'Thêm dòng', Tên 'Cao', Số ngày 3, Mã màu #2563eb", "Bấm 'Lưu' của dòng", "Mở lịch sử"),
         "Tên: Cao",
         E("Báo 'Vui lòng kiểm tra lại thông tin', dưới ô Tên hiện 'Đã tồn tại trên hệ thống'", "Không tạo mức mới, lịch sử vẫn N mục")),
        (14, "Công ty khác được đặt trùng tên mức của Công ty A", "P0",
         L(pri_pre, "GV1 được làm việc ở Công ty A và Công ty B; Công ty B chưa có mức nào tên 'Cao'"),
         S("Đổi công ty làm việc sang Công ty B (ô chọn công ty trên thanh trên cùng)", MENU_ASSIGN, PRI,
           "Bấm 'Thêm dòng', Tên 'Cao', Số ngày 2, Mã màu #f59e0b", "Bấm 'Lưu' của dòng", "Bấm 'Lịch sử thay đổi'"),
         "Tên: Cao",
         E("Báo 'Thêm mới thành công!'", "Công ty B có mức 'Cao'; mức 'Cao' của Công ty A giữ nguyên",
           "Lịch sử Công ty B có mục 'Tạo mới' với nhóm 'Mức độ ưu tiên thêm mới:' - '- Cao — ...'; lịch sử Công ty A không có mục này")),
        (15, "Sửa mức giữ nguyên tên không bị báo trùng", "P1", pri_pre,
         pri_edit("Chỉ đổi Số ngày phản hồi 2 -> 4, giữ Tên 'Cao'"), "2 -> 4",
         E("Báo 'Cập nhật thành công!' (không báo trùng với chính nó)",
           "1 mục 'Thay đổi thông tin'; nhóm 'Mức độ ưu tiên sửa thông tin:' có đúng 1 dòng '- Cao: Số ngày phản hồi: 2 (chữ đỏ) -> 4 (chữ xanh)'")),
    ]

    dl_fields = [
        ("Cảnh báo sớm nhiệm vụ trước", "ngày", "Cảnh báo sớm nhiệm vụ trước (ngày)", "2", "3", "P0"),
        ("Cảnh báo sớm Issue trước", "ngày", "Cảnh báo sớm Issue trước (ngày)", "2", "4", "P0"),
        ("Meeting sắp tới lịch trước", "ngày", "Meeting sắp tới lịch trước (ngày)", "1", "2", "P0"),
        ("Hạn nhập biên bản meeting sau", "ngày", "Hạn nhập biên bản meeting sau (ngày)", "1", "3", "P0"),
        ("Cảnh báo trước khi tự hủy meeting", "giờ", "Cảnh báo trước khi tự hủy meeting (giờ)", "3", "6", "P0"),
        ("Cảnh báo trước khi đóng nhu cầu", "ngày", "Cảnh báo trước khi đóng nhu cầu (ngày)", "3", "5", "P0"),
        ("Giải pháp sắp tới hạn trước", "ngày", "Giải pháp sắp tới hạn trước (ngày)", "2", "3", "P0"),
        ("Hạng mục nhiều nhiệm vụ trễ khi có từ", "nhiệm vụ trễ", "Hạng mục nhiều nhiệm vụ trễ khi có từ (nhiệm vụ trễ)", "3", "5", "P1"),
        ("Nhân sự nhiều nhiệm vụ trễ khi có từ", "nhiệm vụ trễ", "Nhân sự nhiều nhiệm vụ trễ khi có từ (nhiệm vụ trễ)", "3", "4", "P1"),
    ]
    s5 = []
    n = 1
    for lbl, unit, pop, old, new, prio in dl_fields:
        s5.append((n, "Sửa '%s'" % lbl, prio, L(pre, "Cấu hình hạn Công ty A: '%s' đang %s %s" % (lbl, old, unit)),
                   S(MENU_ASSIGN, DL, "Ô '%s' nhập %s" % (lbl, new), "Bấm 'Lưu cấu hình'", "Bấm 'Lịch sử thay đổi'"),
                   "%s -> %s" % (old, new),
                   E("Báo 'Cập nhật thành công!'", "1 mục 'Thay đổi thông tin' (chữ xanh dương), người thực hiện GV1",
                     "Mục CHỈ có " + diff(pop, old, new))))
        n += 1
    s5 += [
        (n, "Để trống 'Hạn nhập biên bản meeting sau' lấy mặc định", "P1", L(pre, "Ô đang 3"),
         S(MENU_ASSIGN, DL, "Xoá trắng ô 'Hạn nhập biên bản meeting sau'", "Bấm 'Lưu cấu hình'", "Bấm 'Lịch sử thay đổi'"), "(trống)",
         E("Ô hiển thị lại 1 sau khi lưu", "Mục mới: " + diff("Hạn nhập biên bản meeting sau (ngày)", "3", "1"))),
        (n + 1, "Nhập 0 cho 'Cảnh báo trước khi tự hủy meeting' lấy mặc định", "P2", L(pre, "Ô đang 6"),
         S(MENU_ASSIGN, DL, "Nhập 0 vào 'Cảnh báo trước khi tự hủy meeting'", "Bấm 'Lưu cấu hình'", "Mở lịch sử"), "0",
         E("Ô hiển thị lại 3", "Mục mới: " + diff("Cảnh báo trước khi tự hủy meeting (giờ)", "6", "3"))),
        (n + 2, "Lưu cấu hình hạn không đổi gì", "P0", L(pre, "Lịch sử Cấu hình hạn đang có N mục"),
         S(MENU_ASSIGN, DL, "Bấm 'Lưu cấu hình'", "Mở lịch sử"), "—", E("Lịch sử vẫn N mục")),
        (n + 3, "Sửa nhiều trường 1 lần gom 1 mục", "P1", pre,
         S(MENU_ASSIGN, DL, "Đổi 'Cảnh báo sớm nhiệm vụ trước' và 'Giải pháp sắp tới hạn trước'", "Bấm 'Lưu cấu hình'", "Mở lịch sử"), "—",
         E("Đúng 1 mục có 2 dòng thay đổi")),
        (n + 4, "Lọc Loại hành động trong popup Cấu hình hạn", "P2", L(pre, "Có 2 mục: đổi 'Cảnh báo sớm nhiệm vụ trước' và đổi 'Meeting sắp tới lịch trước'"),
         S(MENU_ASSIGN, DL, "Mở lịch sử -> 'Bộ lọc'", "Loại hành động chọn 'Thay đổi thông tin', rồi đổi sang 'Tạo mới'"), "—",
         E("KHÔNG còn ô lọc 'Trường'", "'Thay đổi thông tin': đủ 2 mục", "'Tạo mới': hiện '%s'" % NO_MATCH)),
        (n + 5, "Nhãn trong popup khớp chữ trên form", "P1", pre,
         S(MENU_ASSIGN, DL, "Đổi 'Cảnh báo sớm Issue trước'", "Lưu, mở lịch sử"), "—",
         E("Popup ghi 'Cảnh báo sớm Issue trước (ngày)' — đúng chữ trên form, KHÔNG ghi 'Vấn đề'",
           "Lịch sử ghi trước khi thống nhất nhãn cũng hiển thị theo nhãn này")),
    ]

    pc_pre = L(pre, "Đóng dự án tự động Công ty A: Hạn đóng khi dự án chưa có báo giá 3 tháng; Nhắc trước hạn đóng 7 ngày;",
               "Quá hạn bao lâu thì tự đóng 0 ngày; Trưởng phòng được duyệt gia hạn tối đa 30 ngày;",
               "Giai đoạn '1.Giai đoạn nghiên cứu dự án' 6 tháng, giai đoạn '8.Chốt hợp đồng và chuyển sang triển khai dự án' để trống")

    def pc_steps(action):
        return S(MENU_ASSIGN, PC, action, "Bấm 'Lưu cấu hình'", "Bấm 'Lịch sử thay đổi'")

    s6 = [
        (1, "Sửa 'Hạn đóng khi dự án chưa có báo giá'", "P0", pc_pre, pc_steps("Ô 'Hạn đóng khi dự án chưa có báo giá' nhập 4"), "3 -> 4",
         E("Báo 'Đã lưu cấu hình đóng dự án tự động'", "1 mục 'Thay đổi thông tin' (chữ xanh dương), người thực hiện GV1",
           "Mục CHỈ có " + diff("Hạn đóng khi dự án chưa có báo giá (tháng)", "3", "4"))),
        (2, "Sửa 'Nhắc trước hạn đóng'", "P0", pc_pre, pc_steps("Ô 'Nhắc trước hạn đóng' nhập 10"), "7 -> 10",
         E("Mục CHỈ có " + diff("Nhắc trước hạn đóng (ngày)", "7", "10"))),
        (3, "Sửa 'Quá hạn bao lâu thì tự đóng'", "P0", pc_pre, pc_steps("Ô 'Quá hạn bao lâu thì tự đóng' nhập 5"), "0 -> 5",
         E("Mục CHỈ có " + diff("Quá hạn bao lâu thì tự đóng (ngày)", "0", "5"))),
        (4, "Sửa 'Trưởng phòng được duyệt gia hạn tối đa'", "P0", pc_pre, pc_steps("Ô 'Trưởng phòng được duyệt gia hạn tối đa' nhập 45"), "30 -> 45",
         E("Mục CHỈ có " + diff("Trưởng phòng được duyệt gia hạn tối đa (ngày)", "30", "45"))),
        (5, "Đặt thời hạn cho giai đoạn đang để trống", "P0", pc_pre,
         pc_steps("Bảng 'Thời hạn theo giai đoạn', dòng '8.Chốt hợp đồng và chuyển sang triển khai dự án' nhập 12"), "Không tự đóng -> 12",
         E("Mục có " + diff("Giai đoạn: 8.Chốt hợp đồng và chuyển sang triển khai dự án", "Không tự đóng", "12"))),
        (6, "Xoá trống thời hạn giai đoạn", "P0", pc_pre, pc_steps("Dòng '1.Giai đoạn nghiên cứu dự án' xoá trắng ô Thời hạn (tháng)"), "6 -> (trống)",
         E("Lưu thành công, ô hiện placeholder 'Không tự đóng'", "Mục có " + diff("Giai đoạn: 1.Giai đoạn nghiên cứu dự án", "6", "Không tự đóng"),
           "Lưu ý: KHÔNG được lưu thành 0 (0 là đóng ngay)")),
        (7, "Đổi tham số chung và giai đoạn trong 1 lần Lưu gom 1 mục", "P1", pc_pre,
         pc_steps("Đổi 'Nhắc trước hạn đóng' 7 -> 5 và giai đoạn '1.Giai đoạn nghiên cứu dự án' 6 -> 8"), "—",
         E("Đúng 1 mục có 2 dòng: 'Nhắc trước hạn đóng (ngày): 7 -> 5' và 'Giai đoạn: 1.Giai đoạn nghiên cứu dự án: 6 -> 8'",
           "Lọc Loại hành động 'Thay đổi thông tin' thấy mục này (không còn ô 'Nhóm cấu hình')")),
        (8, "Lưu không đổi gì", "P0", L(pc_pre, "Lịch sử đang có N mục"), pc_steps("Không sửa gì"), "—", E("Lịch sử vẫn N mục")),
        (9, "Tham số chung để trống / số âm / số thập phân bị chặn", "P0", L(pc_pre, "Lịch sử đang có N mục"),
         pc_steps("'Hạn đóng khi dự án chưa có báo giá' để trống, 'Nhắc trước hạn đóng' -1, 'Quá hạn bao lâu thì tự đóng' 1.5"), "—",
         E("Báo 'Vui lòng kiểm tra lại các ô được báo đỏ'",
           "Dưới 3 ô lần lượt: 'Bắt buộc phải nhập', 'Không được nhỏ hơn 0', 'Phải là số nguyên'", "Lịch sử vẫn N mục")),
        (10, "Vượt giới hạn tối đa bị chặn", "P1", L(pc_pre, "Lịch sử đang có N mục"),
         pc_steps("'Hạn đóng khi dự án chưa có báo giá' 121, giai đoạn '1.Giai đoạn nghiên cứu dự án' 121"), "121",
         E("Dưới 2 ô hiện 'Không được lớn hơn 120'", "Lịch sử vẫn N mục")),
        (11, "Tham số chung theo công ty, thời hạn giai đoạn dùng chung", "P1", L(pc_pre, "GV1 làm việc được ở Công ty B"),
         S("Ở Công ty A đổi 'Nhắc trước hạn đóng' và giai đoạn '1.Giai đoạn nghiên cứu dự án', Lưu", "Đổi sang Công ty B, mở lịch sử Đóng dự án tự động"), "—",
         E("Công ty B KHÔNG thấy thay đổi 'Nhắc trước hạn đóng' của Công ty A",
           "Công ty B VẪN thấy thay đổi giai đoạn '1.Giai đoạn nghiên cứu dự án' (thời hạn giai đoạn dùng chung mọi công ty)")),
    ]

    s7 = [
        (1, "[Lỗi đã sửa] Mức độ ưu tiên tách theo công ty", "P0",
         L(pre, "Công ty A và Công ty B đều có mức ưu tiên riêng"),
         S("Ở Công ty B thêm mức 'Gấp B'", "Đổi về Công ty A mở " + PRI, "Mở lịch sử Mức độ ưu tiên ở Công ty A"), "—",
         E("Công ty A không thấy 'Gấp B' trong bảng", "Lịch sử Công ty A không có mục nào nhắc 'Gấp B' (nhóm 'Mức độ ưu tiên thêm mới:')",
           "Trước đây: mọi công ty dùng chung 1 bảng mức ưu tiên và 1 lịch sử")),
        (2, "[Lỗi đã sửa] Ô 'Phòng tại khu du lịch' của phiếu kỹ thuật lưu được", "P0", base_pre,
         common_steps("dòng 'Phiếu công tác kỹ thuật', cột 'Phòng tại khu du lịch (VND/phòng)' nhập 650000"), "650,000",
         E("Tải lại trang ô vẫn 650,000", "Lịch sử có 'Phiếu công tác kỹ thuật — Phòng tại khu du lịch (VND/phòng): ... -> 650,000'",
           "Trước đây: bấm Lưu báo thành công nhưng ô quay về giá trị cũ")),
        (3, "[Lỗi đã sửa] Ô tiền trống giữ trống, không thành 0", "P0", base_pre,
         common_steps("xoá trắng 'Hỗ trợ công tác phí - PCT khác (Xe ngoài)' và cột 'Phòng ba (VND/phòng)' của Phiếu công tác khác"), "—",
         E("Tải lại trang 2 ô vẫn trống", "Lịch sử ghi '-> (trống)', KHÔNG ghi '-> 0'")),
        (4, "[Lỗi đã sửa] Popup Đóng dự án tự động hiện đúng họ tên và lọc theo công ty", "P1", pc_pre,
         pc_steps("Đổi 'Nhắc trước hạn đóng' 7 -> 8"), "—",
         E("Mục ghi 'Người thực hiện: Hoàng Văn Giao Việc — <phòng ban>' (không hiện mã số người dùng)", "Popup dùng khuôn chung: có Bộ lọc, nút Đóng")),
        (5, "[Lỗi đã sửa] Kéo thả về chỗ cũ không sinh mục rác", "P1", L(pri_pre, "Lịch sử đang có N mục"),
         S(MENU_ASSIGN, PRI, "Kéo 'Khẩn cấp' xuống rồi thả lại vị trí 1", "Mở lịch sử"), "—", E("Lịch sử vẫn N mục")),
        (6, "[Lỗi đã sửa] Nút Thêm mới khung giờ, popup tự đóng, giờ đủ 2 chữ số", "P1", base_pre,
         S(MENU_ASSIGN, "Tab 'Thông tin chung', khối 'Khung giờ tính ngày xuất phát' bấm vào CHỮ 'Thêm mới' ở tiêu đề bảng",
           "Popup 'Thêm khung giờ': ô 'Trước giờ' chọn 14:00, ô 'Công được tính' nhập 0.5, bấm 'OK'"),
         L("Trước giờ: 14:00", "Công được tính: 0.5"),
         E("Bấm vào chữ 'Thêm mới' (không cần trúng biểu tượng +) vẫn mở popup 'Thêm khung giờ'", "Popup tự đóng ngay sau khi bấm 'OK'", "Bảng hiện dòng 'Trước 14:00h' (KHÔNG hiện 'Trước 14:0h')",
           "Trước đây: chỉ biểu tượng + bấm được; bấm 'OK' popup vẫn mở, phải bấm 'Huỷ' mới đóng; giờ chẵn hiện thiếu số 0 cho tới khi tải lại trang")),
    ]

    return build(output_file=out("Lịch sử Cấu hình giao việc"), sheet_name="Trang tính1",
                 feature_name="Lịch sử thay đổi - Cấu hình chung giao việc - Cập nhật ngày 30/09/2026",
                 module_name="Cấu hình giao việc",
                 description_block=desc, role_tcs=roles,
                 sections=[("I", "NÚT LỊCH SỬ, POPUP & BỘ LỌC", s1),
                           ("II", "TAB THÔNG TIN CHUNG - TỪNG TRƯỜNG", s2),
                           ("III", "TAB GIỚI HẠN KHOẢNG CÁCH TÍNH CÔNG TÁC PHÍ", s3),
                           ("IV", "CẤU HÌNH MỨC ĐỘ ƯU TIÊN (THÊM / SỬA / XÓA / KÉO THẢ)", s4),
                           ("V", "CẤU HÌNH HẠN", s5),
                           ("VI", "ĐÓNG DỰ ÁN TỰ ĐỘNG", s6),
                           ("VII", "CÁC LỖI ĐÃ SỬA TRONG ĐỢT NÀY", s7)])


def main():
    totals = {}
    totals["Phân quyền"] = build_roles()
    totals["Người dùng"] = build_users()
    totals["Cấu hình HCNS"] = build_hcns()
    totals["Cấu hình giao việc"] = build_assign()
    print("=== TONG:", totals, "=", sum(totals.values()))


if __name__ == "__main__":
    main()
