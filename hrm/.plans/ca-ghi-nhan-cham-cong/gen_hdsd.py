# -*- coding: utf-8 -*-
"""
Sinh HDSD "Ca chỉ ghi nhận lịch sử chấm công".

Chạy:  python3 .plans/ca-ghi-nhan-cham-cong/gen_hdsd.py

Dùng engine chung của team (.claude/skills/hdsd-documenter/assets/hdsd_engine.py).
Engine đó cập nhật mục lục bằng PowerShell + Word COM (Windows). Máy này là macOS nên
lớp HdsdBuilderMac dưới đây GHI ĐÈ đúng một bước đó bằng AppleScript, KHÔNG sửa file
của skill (thư mục .claude/skills là tài sản chung, sửa phải qua PR).
"""
import os, sys, subprocess, platform

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, ".claude", "skills", "hdsd-documenter", "assets"))
from hdsd_engine import HdsdBuilder  # noqa: E402

SHOTS = os.path.join(HERE, "hdsd_ca_ghi_nhan_shots")
OUT = os.path.join(HERE, "HDSD_Ca ghi nhan lich su cham cong.docx")


class HdsdBuilderMac(HdsdBuilder):
    """Cập nhật mục lục / danh mục hình ảnh bằng Microsoft Word trên macOS."""

    def _update_fields_by_word(self):
        if platform.system() != "Darwin":
            return super()._update_fields_by_word()

        script = '''
        tell application "Microsoft Word"
            set d to open file name POSIX file "%s"
            try
                repeat with f in (get fields of d)
                    update field f
                end repeat
            end try
            try
                repeat with t in (get tables of contents of d)
                    update t
                    update page numbers t
                end repeat
            end try
            try
                repeat with g in (get tables of figures of d)
                    update g
                    update page numbers g
                end repeat
            end try
            repaginate d
            save d
            close d saving no
        end tell
        ''' % OUT
        res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=180)
        if res.returncode != 0:
            raise RuntimeError(
                "Word (macOS) khong cap nhat duoc muc luc: %s\n"
                "=> Muc luc se con noi dung cua file khung, KHONG duoc ban giao file nay."
                % (res.stderr.strip() or res.stdout.strip())
            )
        print("Cap nhat muc luc bang Word (macOS): OK")


b = HdsdBuilderMac(
    output=OUT,
    shots_dir=SHOTS,
    cover_title="(Màn hình: Ca chỉ ghi nhận lịch sử chấm công)",
    doc_title="HDSD - Ca chỉ ghi nhận lịch sử chấm công",
)

# ----------------------------------------------------------------------------- TỔNG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ dùng trong tài liệu")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Ca chỉ ghi nhận lịch sử chấm công",
     "Loại ca làm việc đặc biệt, sinh ra để nhân sự chấm công lấy lịch sử vào ngày lễ hoặc ngày nghỉ. "
     "Ngày được phân ca này KHÔNG tính công định mức, không tính lương, không trừ phép, không phát sinh "
     "suất cơm và không tính hệ số tăng ca. Tài liệu gọi tắt là “ca ghi nhận”."],
    ["Ca thường", "Các ca làm việc còn lại, có tính công như từ trước tới nay."],
    ["Phân ca", "Gán một ca làm việc cho nhân sự vào một ngày cụ thể."],
    ["Công định mức", "Số ngày công chuẩn của nhân sự trong kỳ, dùng làm mẫu số khi tính lương."],
    ["CC", "Ký hiệu hiển thị trên Bảng công chi tiết, báo rằng ngày đó nhân sự CÓ chấm công theo ca ghi nhận."],
])

b.h2("2. Lịch sử cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung"],
    ["1.0", "29/08/2026", "Ban hành lần đầu, mô tả trọn luồng từ tạo ca đến xem lịch sử chấm công."],
])

b.h2("3. Giới thiệu chung")
b.para(
    "Bình thường nhân sự chỉ chấm công được vào ngày đã được phân ca. Vào ngày lễ hoặc Chủ nhật, "
    "nhân sự không có ca nên bấm chấm công sẽ bị từ chối với thông báo “Chưa có ca làm việc hoặc "
    "đăng ký làm thêm”. Nhưng có những trường hợp công ty vẫn cần ghi nhận việc nhân sự có mặt "
    "trong các ngày đó — ví dụ trực lễ, xử lý sự cố, đi làm bù."
)
b.para(
    "“Ca chỉ ghi nhận lịch sử chấm công” sinh ra để giải quyết đúng việc này: mở cổng cho nhân sự "
    "chấm công được, nhưng ngày đó vẫn được hệ thống coi như một ngày KHÔNG được phân ca — "
    "mọi con số công, lương, phép, tiền cơm giữ nguyên."
)
b.para("Các màn hình liên quan:")
b.table([
    ["Việc cần làm", "Đường dẫn màn hình"],
    ["Tạo / sửa ca làm việc", "/timesheet/timeworking/working-shift"],
    ["Phân ca theo từng ngày (lưới)", "/timesheet/timeworking/shift-detail/general"],
    ["Phân ca theo khoảng ngày", "/timesheet/timeworking/shift-detail/add"],
    ["Xem bảng công và ký hiệu CC", "/timesheet/timesheet_details"],
])

b.h2("4. Phân quyền")
b.para(
    "Luồng này đi qua ba màn hình khác nhau, mỗi màn dùng một nhóm quyền riêng. Người dùng thường "
    "chỉ có một phần trong số này — hãy đối chiếu bảng dưới để biết mình làm được bước nào."
)
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / màn tương ứng"],
    ["Quản lý ca làm việc",
     "Tạo mới, sửa, khoá và xoá ca làm việc — bao gồm cả việc bật cờ “Ca chỉ ghi nhận lịch sử chấm công”",
     "Nút Thêm mới và các thao tác trong menu bánh răng ở màn Ca làm việc"],
    ["Xem danh mục ca làm việc theo tổng công ty",
     "Xem danh sách ca làm việc của mọi công ty", "Màn Ca làm việc"],
    ["Xem danh mục ca làm việc theo công ty",
     "Chỉ xem ca làm việc thuộc công ty của mình", "Màn Ca làm việc"],
    ["Phân ca theo công ty", "Phân ca cho nhân sự trong toàn công ty của mình",
     "Nút “+” trên lưới Tổng hợp phân ca, màn Thêm phân ca chi tiết"],
    ["Phân ca theo phòng ban", "Chỉ phân ca cho nhân sự thuộc phòng ban mình quản lý", "Như trên"],
    ["Phân ca theo bộ phận", "Chỉ phân ca cho nhân sự thuộc bộ phận mình quản lý", "Như trên"],
    ["Xem bảng chấm công chi tiết theo tổng công ty",
     "Xem bảng công và ký hiệu CC của toàn bộ nhân sự", "Màn Bảng công chi tiết trong tháng"],
    ["Xem bảng chấm công chi tiết theo công ty / phòng ban / bộ phận",
     "Xem bảng công trong phạm vi tương ứng", "Như trên"],
])
b.para(
    "Không có quyền thì nút tương ứng sẽ không hiển thị. Nếu cố truy cập thẳng bằng đường dẫn, "
    "hệ thống sẽ chuyển sang trang báo không tìm thấy hoặc từ chối với thông báo không có quyền.",
    bold_prefix="Lưu ý: ",
)

b.h2("5. Luồng tổng thể")
b.para("Toàn bộ nghiệp vụ gồm 5 bước, do 3 nhóm người dùng khác nhau thực hiện:")
b.table([
    ["Bước", "Ai làm", "Làm gì", "Ở đâu"],
    ["1", "Người quản lý ca làm việc", "Tạo một ca và tick cờ “Ca chỉ ghi nhận lịch sử chấm công”", "Màn Ca làm việc"],
    ["2", "Người có quyền phân ca", "Phân ca đó cho nhân sự vào đúng ngày lễ / ngày nghỉ", "Lưới Tổng hợp phân ca"],
    ["3", "Nhân sự", "Mở app, chọn ca vừa được phân rồi chấm công", "App di động (hoặc máy chấm công)"],
    ["4", "Người quản lý chấm công", "Xem ký hiệu CC trên bảng công để biết ai đã có mặt", "Bảng công chi tiết"],
    ["5", "Người quản lý chấm công", "Xuất Excel nếu cần gửi báo cáo", "Bảng công chi tiết"],
])

# ----------------------------------------------------------------------------- PHẦN 1
b.h1("PHẦN 1: TẠO CA CHỈ GHI NHẬN LỊCH SỬ CHẤM CÔNG")

b.h2("1.1. Vào màn này bằng cách nào")
b.para("Vào phân hệ Chấm công → nhóm Ca làm việc → mục Ca làm việc, hoặc gõ thẳng đường dẫn "
       "/timesheet/timeworking/working-shift. Tại màn danh sách, bấm nút Thêm mới ở góc trên bên phải.")
b.para("Yêu cầu quyền Quản lý ca làm việc. Không có quyền này thì nút Thêm mới không hiển thị.",
       bold_prefix="Quyền yêu cầu: ")

b.h2("1.2. Form khi CHƯA tick cờ")
b.para("Mặc định form Thêm ca làm việc hiển thị đầy đủ như mọi ca thường: ngoài thông tin ca còn có "
       "khối Nghỉ giữa ca, khối Tính công và khối Cài đặt.")
b.image("01-form-tao-ca-truoc-tick.png", "Form Thêm ca làm việc khi chưa tick cờ — hiển thị đầy đủ các khối")

b.h2("1.3. Tick cờ “Ca chỉ ghi nhận lịch sử chấm công”")
b.para("Ô tick nằm ngay dưới tiêu đề form, cạnh có biểu tượng chữ i. Đưa chuột vào biểu tượng đó sẽ "
       "hiện dòng giải thích ngắn.")
b.image("03-tooltip-giai-thich.png", "Dòng giải thích khi đưa chuột vào biểu tượng chữ i")
b.para("Ngay khi tick, form tự rút gọn — ba khối sau biến mất vì ca này không tính công:")
b.bullet("Dòng Nghỉ giữa ca và toàn bộ ô giờ nghỉ")
b.bullet("Khối Tính công (Giờ công, Số công, các hệ số ngày thường / ngày nghỉ / ngày lễ)")
b.bullet("Khối Cài đặt (đi muộn về sớm, quên chấm công, tăng ca, ca đêm, phụ cấp cơm, bảng phạt)")
b.image("02-form-tao-ca-sau-tick.png", "Form sau khi tick cờ — chỉ còn các ô cần cho việc chấm công")

b.h2("1.4. Các trường cần nhập")
b.table([
    ["Trường", "Bắt buộc", "Giá trị điền sẵn khi tạo mới", "Ghi chú"],
    ["Ca chỉ ghi nhận lịch sử chấm công", "Không", "Chưa tick", "Tick vào để tạo loại ca này"],
    ["Tên ca", "Có", "Để trống", "Nên đặt tên nói rõ mục đích, ví dụ “Ca ghi nhận chấm công ngày lễ”"],
    ["Mã ca", "Có", "Để trống", "Không được trùng với ca đã có"],
    ["Giờ bắt đầu ca", "Có", "08:00", "Khoảng giờ nhân sự được phép chấm công trong ngày"],
    ["Giờ kết thúc ca", "Có", "17:30", ""],
    ["Chấm vào / Chấm ra", "Không", "Không tick", "Tick nếu muốn giới hạn thêm khung giờ chấm vào / chấm ra"],
    ["Hình thức chấm công hợp lệ", "Có", "Để trống", "Chọn “App điện thoại” và/hoặc “Máy chấm công”"],
    ["Địa điểm chấm công hợp lệ", "Có khi chọn App điện thoại", "Một dòng trống",
     "Gồm Địa chỉ, Vĩ độ, Kinh độ. Bấm dấu cộng để thêm nhiều địa điểm"],
    ["Máy chấm công hợp lệ", "Có khi chọn Máy chấm công", "Để trống", "Chọn địa điểm máy và các máy được phép"],
])
b.para(
    "Bắt buộc khai địa điểm khi cho phép chấm bằng app. Nếu bỏ trống, hệ thống sẽ không có mốc để "
    "đo khoảng cách và nhân sự sẽ chấm công được từ bất kỳ đâu.",
    bold_prefix="Rất quan trọng: ",
)
b.image("04-form-da-dien-day-du.png", "Form đã điền đầy đủ, sẵn sàng lưu")

b.h2("1.5. Lưu ca")
b.para("Bấm Lưu ở góc dưới bên phải. Hệ thống báo “Thêm ca làm việc thành công” và quay về màn danh sách. "
       "Ca mới xuất hiện trong danh sách với Hệ số công và Giờ công đều bằng 0 — đây là dấu hiệu nhận biết "
       "nhanh một ca chỉ ghi nhận chấm công.")
b.image("06-danh-sach-ca-moi.png", "Ca vừa tạo trong danh sách Ca làm việc")

# ----------------------------------------------------------------------------- PHẦN 2
b.h1("PHẦN 2: PHÂN CA CHO NHÂN SỰ")

b.h2("2.1. Hai cách phân ca")
b.para("Ca này được phân giống hệt mọi ca khác, không có màn riêng. Có hai lối vào:")
b.table([
    ["Cách", "Đường bấm", "Phù hợp khi"],
    ["Lưới Tổng hợp phân ca",
     "Chấm công → Ca làm việc → Tổng hợp phân ca (/timesheet/timeworking/shift-detail/general)",
     "Phân cho vài người vào một vài ngày lẻ — đúng với ngày lễ, Chủ nhật"],
    ["Thêm phân ca chi tiết",
     "Chấm công → Ca làm việc → Phân ca làm việc → Thêm mới (/timesheet/timeworking/shift-detail/add)",
     "Phân theo khoảng ngày dài, lặp theo thứ trong tuần, cho nhiều nhân sự cùng lúc"],
])
b.para("Yêu cầu một trong ba quyền Phân ca theo công ty / theo phòng ban / theo bộ phận. "
       "Phạm vi nhân sự bạn thấy được phụ thuộc vào quyền đang có.", bold_prefix="Quyền yêu cầu: ")

b.h2("2.2. Cách 1 — Phân ca trên lưới Tổng hợp phân ca")
b.para("Bước 1: mở màn, bấm Bộ lọc rồi chọn Phòng ban (và Nhân viên nếu muốn thu hẹp), sau đó bấm nút "
       "kính lúp để tìm.")
b.image("07-luoi-tong-hop-phan-ca.png", "Lưới Tổng hợp phân ca sau khi lọc")
b.para("Bước 2: tìm đến ô giao giữa dòng nhân sự và cột ngày cần phân. Ô còn trống sẽ có dấu cộng màu xanh. "
       "Ngày trong quá khứ không có dấu cộng — chỉ phân được từ hôm nay trở đi.")
b.image("08-o-ngay-trong-nut-cong.png", "Ô ngày còn trống có dấu cộng để thêm phân ca")
b.para("Bước 3: bấm dấu cộng, cửa sổ Ca làm việc mở ra kèm danh sách toàn bộ ca. Bấm Bộ lọc trong cửa sổ "
       "này rồi gõ tên hoặc mã ca để tìm nhanh.")
b.image("09-popup-chon-ca.png", "Cửa sổ chọn ca làm việc")
b.image("10-popup-loc-ra-ca-ghi-nhan.png", "Lọc theo mã ca để tìm nhanh ca ghi nhận")
b.para("Bước 4: bấm vào dòng của ca cần phân. Hệ thống hỏi xác nhận, bấm Đồng ý.")
b.image("11-popup-xac-nhan-phan-ca.png", "Cửa sổ xác nhận trước khi phân ca")
b.para("Bước 5: ô ngày chuyển thành ô màu xanh hiển thị khung giờ và tên ca. Đến đây nhân sự đã có thể "
       "chấm công trong ngày đó.")
b.image("12-luoi-sau-khi-phan-ca.png", "Ô ngày đã hiển thị ca vừa phân")
b.para("Muốn bỏ phân ca, bấm dấu X ở góc ô rồi xác nhận. Việc này chỉ gỡ phân ca, "
       "KHÔNG xoá lịch sử chấm công đã ghi nhận trước đó.", bold_prefix="Xoá phân ca: ")

b.h2("2.3. Cách 2 — Phân ca theo khoảng ngày")
b.para("Dùng khi cần phân cho nhiều người trong một khoảng ngày. Nhập Tên bảng phân ca, chọn Ngày bắt đầu "
       "và Ngày kết thúc, tick các thứ trong tuần cần áp dụng rồi chọn ca cho từng thứ.")
b.image("18-man-phan-ca-theo-khoang-ngay.png", "Màn Thêm phân ca chi tiết")
b.para("Bên phải, bấm dấu cộng cạnh Danh sách nhân viên để mở cửa sổ chọn người, tick những nhân sự cần "
       "phân rồi bấm Chọn.")
b.image("19-popup-chon-nhan-vien.png", "Cửa sổ chọn nhân viên")
b.para("Ngày bắt đầu không được nhỏ hơn ngày hôm nay. Bỏ trống Ngày bắt đầu hoặc Ngày kết thúc, "
       "hệ thống sẽ báo lỗi đỏ “Bắt buộc phải nhập” ngay dưới ô.", bold_prefix="Lưu ý: ")

b.h2("2.4. Khi ngày đó nhân sự đã có ca khác")
b.para("Một nhân sự chỉ nên có một ca trong một ngày. Nếu ngày bạn đang phân đã có ca khác — kể cả ca ghi "
       "nhận đã phân trước đó — hệ thống dừng lại và hiện bảng Xác nhận tạo mới, liệt kê rõ từng người: "
       "ca cũ là ca nào, ca mới là ca nào, trùng vào ngày nào.")
b.image("20-canh-bao-trung-ca.png", "Cảnh báo khi ngày đó nhân sự đã có ca khác")
b.bullet("Bấm Huỷ để giữ nguyên ca cũ, không thay đổi gì.")
b.bullet("Bấm Xác nhận nếu thực sự muốn thay ca cũ bằng ca mới.")
b.para("Hãy đọc kỹ cột Ca cũ trước khi bấm Xác nhận. Nếu ca cũ là ca ghi nhận mà bạn xác nhận thay bằng "
       "ca thường, ngày đó sẽ quay lại tính công như bình thường.", bold_prefix="Cẩn thận: ")

# ----------------------------------------------------------------------------- PHẦN 3
b.h1("PHẦN 3: NHÂN SỰ CHẤM CÔNG")

b.h2("3.1. Chấm công bằng app di động")
b.para("Sau khi được phân ca, nhân sự mở app và chấm công như ngày làm việc bình thường. Trong danh sách "
       "hình thức chấm công sẽ xuất hiện một dòng có dạng “Ca ghi nhận chấm công: <tên ca>” kèm khung giờ "
       "và địa điểm hợp lệ. Chọn dòng đó rồi bấm chấm công.")
b.para("Tiền tố “Ca ghi nhận chấm công” giúp nhân sự phân biệt ngay với ca hành chính thông thường, "
       "tránh hiểu nhầm rằng ngày đó có tính công.")

b.h2("3.2. Điều kiện để chấm công thành công")
b.table([
    ["Điều kiện", "Nếu không đạt, hệ thống báo"],
    ["Nhân sự đã được phân ca trong ngày", "Chưa có ca làm việc hoặc đăng ký làm thêm"],
    ["Ca cho phép chấm bằng app", "Ca làm việc không cho phép chấm công bằng điện thoại"],
    ["Đang đứng trong bán kính cho phép quanh địa điểm đã khai", "Vị trí chấm công không hợp lệ"],
    ["Nhân sự đã có mã chấm công", "Chưa có mã chấm công, vui lòng kiểm tra lại"],
])
b.para("Bán kính cho phép do quản trị đặt trong thiết lập chung của từng công ty, không đặt riêng theo ca.")

b.h2("3.3. Chấm công bằng máy chấm công")
b.para("Không cần thao tác gì thêm. Máy chấm công ghi nhận theo mã chấm công của nhân sự, không phụ thuộc "
       "vào việc đã phân ca hay chưa. Dữ liệu vẫn vào lịch sử chấm công như bình thường.")

# ----------------------------------------------------------------------------- PHẦN 4
b.h1("PHẦN 4: XEM KÝ HIỆU CC TRÊN BẢNG CÔNG")

b.h2("4.1. Vào màn này bằng cách nào")
b.para("Vào phân hệ Chấm công → mục Bảng công chi tiết trong tháng, hoặc gõ đường dẫn "
       "/timesheet/timesheet_details. Bấm Bộ lọc, chọn tháng và nhập mã hoặc tên nhân viên, rồi bấm "
       "nút kính lúp.")
b.para("Cần một trong các quyền Xem bảng chấm công chi tiết theo tổng công ty / theo công ty / "
       "theo phòng ban / theo bộ phận. Phạm vi nhân sự nhìn thấy tương ứng với quyền đang có.",
       bold_prefix="Quyền yêu cầu: ")

b.h2("4.2. Ký hiệu CC")
b.para("Ngày nhân sự chấm công theo ca ghi nhận sẽ hiển thị chữ CC trong ô ngày, nằm cùng nhóm với các ký "
       "hiệu quen thuộc khác như P (nghỉ phép), KLĐ (nghỉ không lý do), GV (giao việc), CT (công tác).")
b.image("13-bang-cong-ky-hieu-CC.png", "Ký hiệu CC trên bảng công chi tiết")
b.table([
    ["Trường hợp", "Ô ngày hiển thị"],
    ["Đã phân ca ghi nhận VÀ nhân sự có chấm công", "CC"],
    ["Đã phân ca ghi nhận nhưng nhân sự KHÔNG chấm công", "Để trống"],
    ["Nhân sự chấm công nhiều lần trong ngày", "Vẫn chỉ một chữ CC"],
    ["Ngày làm việc bình thường", "Hiển thị số công như cũ, không có CC"],
])
b.para("Cột Công định mức và các cột công khác KHÔNG thay đổi khi thêm ca ghi nhận. Đây chính là mục đích "
       "của loại ca này.", bold_prefix="Quan trọng: ")

b.h2("4.3. Xem chi tiết giờ chấm công")
b.para("Bấm vào ô có chữ CC, cửa sổ Chi tiết mở ra với hai thẻ.")
b.para("Thẻ Tổng hợp cho biết ngày đó được phân ca nào, kèm dòng nhắc rằng ca này không tính công. "
       "Các dòng Thời gian hợp lệ, Chốt điểm danh, Đi muộn, Về sớm không hiển thị vì ca này không tính công.")
b.image("14-popup-tab-tong-hop.png", "Thẻ Tổng hợp — tên ca và ghi chú không tính công")
b.para("Thẻ Dữ liệu chấm công liệt kê từng lượt chấm trong ngày: hình thức chấm (app hay máy), vị trí, "
       "ngày giờ, hình ảnh chụp lúc chấm và ghi chú. Bấm vào biểu tượng ở cột Hình ảnh để xem ảnh, "
       "bấm vào vị trí để mở bản đồ.")
b.image("15-popup-du-lieu-cham-cong.png", "Thẻ Dữ liệu chấm công — lịch sử từng lượt chấm trong ngày")

b.h2("4.4. Xuất Excel")
b.para("Bấm nút Xuất excel ở góc trên bên phải màn bảng công. File tải về giữ nguyên ký hiệu CC ở đúng ô "
       "ngày, không cần thao tác gì thêm.")

# ----------------------------------------------------------------------------- PHẦN 5
b.h1("PHẦN 5: SỬA, XOÁ VÀ XEM LỊCH SỬ CA")

b.h2("5.1. Các thao tác trên một ca")
b.para("Tại màn Ca làm việc, bấm nút bánh răng ở cột Hành động của dòng ca để mở danh sách thao tác.")
b.image("16-menu-hanh-dong-ca.png", "Menu thao tác trên một ca làm việc")
b.para("Yêu cầu quyền Quản lý ca làm việc cho các thao tác Sửa, Khoá và Xoá.", bold_prefix="Quyền yêu cầu: ")

b.h2("5.2. Bật hoặc tắt cờ trên ca đã được phân")
b.para("Nếu ca đã được phân cho nhân sự mà bạn đổi cờ, hệ thống sẽ hỏi xác nhận trước, vì việc này làm "
       "thay đổi ngay số liệu công của những ngày đã phân:")
b.bullet("Bật cờ: các ngày đã phân sẽ thôi được tính vào công định mức.")
b.bullet("Tắt cờ: các ngày đã phân sẽ được tính vào công định mức trở lại.")

b.h2("5.3. Lịch sử thay đổi")
b.para("Chọn Lịch sử thay đổi trong menu thao tác để xem ai đã tạo, ai đã sửa và sửa những gì. Dòng "
       "“Ca chỉ ghi nhận lịch sử chấm công” được ghi lại như mọi trường khác.")
b.image("17-lich-su-thay-doi-ca.png", "Lịch sử thay đổi của ca làm việc")

# ----------------------------------------------------------------------------- PHẦN 6
b.h1("PHẦN 6: QUY TẮC NGHIỆP VỤ VÀ CÂU HỎI THƯỜNG GẶP")

b.h2("6.1. Những gì ca này KHÔNG ảnh hưởng")
b.para("Ngày được phân ca ghi nhận được hệ thống đối xử đúng như một ngày không được phân ca. Cụ thể:")
b.table([
    ["Nghiệp vụ", "Ảnh hưởng"],
    ["Công định mức", "Không cộng thêm ngày nào"],
    ["Tổng công tính lương", "Không đổi"],
    ["Số ngày trừ phép khi làm đơn nghỉ", "Không đổi"],
    ["Tiền cơm", "Không phát sinh suất ăn cho ngày đó"],
    ["Hệ số tăng ca ngày nghỉ", "Chủ nhật vẫn được tính là ngày nghỉ"],
    ["Thống kê vắng mặt không lý do", "Không bị tính là vắng mặt"],
    ["Đi muộn, về sớm", "Không tính, không trừ"],
    ["Báo cáo giao việc, hạn xử lý phiếu", "Không tính ngày đó là ngày làm việc"],
])

b.h2("6.2. Câu hỏi thường gặp")
b.para("Đã phân ca rồi nhưng ô ngày trên bảng công vẫn trống?", bold_prefix="Hỏi: ")
b.para("Ký hiệu CC chỉ hiện khi nhân sự thực sự có chấm công. Phân ca mà nhân sự không chấm thì ô để trống.",
       bold_prefix="Đáp: ")
b.para("Nhân sự báo trên app không thấy ca để chọn?", bold_prefix="Hỏi: ")
b.para("Kiểm tra ba việc: ngày đó đã được phân ca chưa, ca có tick hình thức “App điện thoại” không, "
       "và nhân sự đã có mã chấm công chưa.", bold_prefix="Đáp: ")
b.para("Chấm công ở nước ngoài có được không?", bold_prefix="Hỏi: ")
b.para("Được, miễn là địa điểm đó đã được khai vĩ độ và kinh độ trên ca. Hệ thống đo khoảng cách đúng ở "
       "mọi vị trí trên thế giới. Lưu ý ngày chấm công được ghi theo giờ Việt Nam, nên nhân sự ở châu Âu "
       "hoặc châu Mỹ chấm vào buổi chiều tối theo giờ sở tại có thể bị ghi sang ngày hôm sau.",
       bold_prefix="Đáp: ")
b.para("Xoá phân ca thì lịch sử chấm công có mất không?", bold_prefix="Hỏi: ")
b.para("Không. Xoá phân ca chỉ làm ký hiệu CC biến mất khỏi bảng công, các lượt chấm công đã ghi vẫn còn "
       "nguyên trong hệ thống.", bold_prefix="Đáp: ")

b.finish()
