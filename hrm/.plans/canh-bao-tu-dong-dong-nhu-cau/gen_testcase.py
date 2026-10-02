# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho Redmine #11377 — Cảnh báo + tự động đóng nhu cầu khách hàng
theo Lĩnh vực Công ty kinh doanh, kèm chặn tạo Dự án TKT.

Chạy:  python .plans/canh-bao-tu-dong-dong-nhu-cau/gen_testcase.py
Nhánh code tham chiếu: tpe-develop-assign (đã merge task_11377).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", ".claude", "skills",
                                       "testcase-documenter", "assets"))
sys.path.insert(0, ASSETS)

from tc_engine import build  # noqa: E402

FEATURE = "Cảnh báo & tự động đóng nhu cầu khách hàng (#11377) - Cập nhật ngày 15/09/2026"
MODULE = "Hạn xử lý nhu cầu KH"
OUT = os.path.join(HERE, "testcase.xlsx")

P_SCOPE_MANAGE = "Quản lý danh mục lĩnh vực Công ty kinh doanh"
P_SCOPE_VIEW = "Xem danh mục lĩnh vực Công ty kinh doanh"
P_SETTING = "Cấu hình phân hệ giao việc/ công tác"
P_DEMAND_COMPANY = "Xem danh sách nhu cầu khách hàng theo công ty"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Nhu cầu khách hàng thu thập được trong cuộc họp mà mãi không lập thành Dự án tiền khả thi (Dự án TKT) "
     "thì hệ thống tự nhắc rồi tự đóng, thay vì để treo mãi.\n"
     "Ba màn liên quan:\n"
     "- Danh mục › Lĩnh vực Công ty kinh doanh: khai N = 'Thời gian hiệu lực nhu cầu (ngày)' cho từng lĩnh vực.\n"
     "- Cấu hình › Cấu hình chung › thẻ Quản lý dự án › thẻ con Cấu hình hạn: khai M = 'Cảnh báo trước khi đóng "
     "nhu cầu' (ngày), dùng chung, mặc định 3.\n"
     "- Nhu cầu khách hàng (và thẻ 'Nhu cầu của khách hàng' ở màn Công việc của tôi): cột 'Thời gian hết hạn "
     "nhu cầu' + nút Tạo Dự án TKT.\n"
     "Công thức: T = thời điểm cuộc họp phát sinh nhu cầu chuyển sang Hoàn thành · cảnh báo tại T + N - M "
     "(chỉ khi N > M) · tự đóng tại T + N."),

    ("2. Đối tượng được tính / hiển thị",
     "Việc quét hạn CHỈ chạm tới nhu cầu thoả ĐỒNG THỜI:\n"
     "- Trạng thái 'Đang theo dõi';\n"
     "- Chưa gắn Dự án TKT nào;\n"
     "- Cuộc họp phát sinh nhu cầu ĐÃ Hoàn thành (đã có mốc T);\n"
     "- Lĩnh vực Công ty kinh doanh của nhu cầu có N > 0.\n"
     "Cột 'Thời gian hết hạn nhu cầu' hiện ngày hết hạn cho đúng nhóm này; tô cam kèm ghi chú khi đã bước vào "
     "vùng cảnh báo M ngày."),

    ("3. Đối tượng bị ẩn / không tính",
     "Không bao giờ tự cảnh báo và không bao giờ tự đóng (cột hạn ghi 'Không giới hạn thời gian hiệu lực'):\n"
     "- Nhu cầu của lĩnh vực đang để N = 0 (đây là giá trị mặc định sau khi bổ sung trường này);\n"
     "- Nhu cầu mà cuộc họp chưa Hoàn thành (chưa có mốc T);\n"
     "- Nhu cầu đã lập Dự án TKT;\n"
     "- Nhu cầu đã ở trạng thái Đóng (do người dùng đóng tay hoặc hệ thống đã đóng trước đó).\n"
     "Riêng luồng GỬI THÔNG BÁO còn bị bỏ qua khi N <= M, hoặc khi M = 0, hoặc khi nhu cầu đó đã được thông báo một lần "
     "rồi (không nhắc lại mỗi ngày)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Tính năng không thêm bộ lọc thời gian mới. Các mốc thời gian dùng trong nghiệp vụ:\n"
     "- T lấy từ thời điểm cuộc họp chuyển sang Hoàn thành, ghi MỘT LẦN DUY NHẤT ở lần đầu chuyển trạng thái; "
     "sửa lại biên bản sau đó KHÔNG đẩy lùi T.\n"
     "- Dữ liệu cũ (cuộc họp đã Hoàn thành từ trước khi có tính năng) được gán T = thời điểm kết thúc cuộc họp.\n"
     "- So sánh hạn tính theo NGÀY, bỏ giờ: hết hạn ngày nào thì đúng 00:00 ngày đó đã coi là tới hạn.\n"
     "- Việc quét chạy tự động mỗi ngày một lần lúc 01:20 (giờ Việt Nam)."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Cuộc họp (có khảo sát nhu cầu) -> nhiều Nhu cầu khách hàng -> mỗi nhu cầu thuộc 1 Lĩnh vực Công ty kinh doanh "
     "và 1 Nhóm ngành -> nhu cầu có thể được chuyển thành 1 Dự án TKT.\n"
     "N nằm ở bản ghi Lĩnh vực; M nằm ở Cấu hình chung theo công ty (công ty chưa khai thì hiểu là 3).\n"
     "Ngày hết hạn tính theo N ĐƯỢC CHỤP LẠI LÚC TẠO nhu cầu, không phải N hiện tại của lĩnh vực: sửa N ở danh "
     "mục thì nhu cầu đã có GIỮ NGUYÊN hạn cũ, chỉ nhu cầu tạo sau mới theo N mới. Vì vậy KHÔNG gia hạn được "
     "nhu cầu đang chạy bằng cách sửa N."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Mỗi nhu cầu chỉ được cảnh báo MỘT lần: hệ thống ghi nhớ đã cảnh báo, những ngày sau không nhắc lại nữa.\n"
     "- Việc quét chạy lại nhiều lần trong ngày cho cùng kết quả: nhu cầu đã đóng thì không bị đụng tới nữa.\n"
     "- Ngày đóng ghi nhận đúng NGÀY HẾT HẠN (T + N), không phải ngày mà việc quét chạy — chạy bù muộn 3 ngày vẫn "
     "ghi đúng ngày hết hạn thật."),

    ("7. Phân quyền cấp",
     "- \"%s\": khai và sửa N trên từng lĩnh vực. \"%s\": chỉ xem được N.\n"
     "- \"%s\": vào Cấu hình chung để khai M.\n"
     "- Nhóm quyền xem nhu cầu theo cấp: \"Xem danh sách nhu cầu khách hàng theo tổng công ty\" · "
     "\"%s\" · \"Xem danh sách nhu cầu khách hàng theo phòng ban\" · "
     "\"Xem danh sách nhu cầu khách hàng theo bộ phận\" — quyết định thấy được hạn của nhu cầu nào.\n"
     "- Luồng cảnh báo và tự đóng do hệ thống chạy, không gắn với quyền của người dùng nào."
     % (P_SCOPE_MANAGE, P_SCOPE_VIEW, P_SETTING, P_DEMAND_COMPANY)),

    ("8. Cách tính các ô thống kê",
     "Không có ô thống kê trên màn. Các con số cần đối chiếu khi test:\n"
     "- Ngày hết hạn hiển thị ở cột 'Thời gian hết hạn nhu cầu' = ngày cuộc họp Hoàn thành + N ngày.\n"
     "- Ghi chú cạnh ngày: '(còn X ngày)' khi X = số ngày từ hôm nay tới hạn và đã vào vùng cảnh báo; "
     "'(hết hạn hôm nay)' khi đúng ngày hết hạn; '(quá hạn X ngày)' khi đã qua hạn mà chưa bị đóng.\n"
     "- Dòng tổng kết sau khi chạy quét: 'Đã đóng A nhu cầu, cảnh báo B nhu cầu (bỏ qua C nhu cầu không đặt thời "
     "hạn)' — C đếm cả nhu cầu chưa có mốc T lẫn nhu cầu thuộc lĩnh vực để N = 0."),

    ("9. Ghi chú đọc bảng",
     "Bẫy dễ sai nhất của đợt này:\n"
     "- N = 0 nghĩa là KHÔNG đặt thời hạn, không phải 'hết hạn ngay'. Mặc định sau khi lên bản mới, mọi lĩnh vực "
     "đều là 0, tức chưa nhu cầu nào bị đóng cho tới khi người quản trị khai N.\n"
     "- N <= M thì KHÔNG có bước cảnh báo, nhu cầu vẫn bị đóng đúng hạn. Đừng báo lỗi 'thiếu thông báo'.\n"
     "- PHÂN BIỆT 2 LUỒNG, đây là chỗ dễ báo nhầm nhất:\n"
     "   (a) TÔ CAM + '(còn X ngày)' ở cột hạn màn danh sách: hiện cho MỌI nhu cầu còn dưới M ngày là hết "
     "hạn, KHÔNG phụ thuộc N lớn hay nhỏ hơn M. Vùng cảnh báo TÍCH LUỸ — đặt M = 3 thì còn 3, 2, 1 ngày và "
     "quá hạn đều tô cam, không phải chỉ đúng mốc 3 ngày.\n"
     "   (b) THÔNG BÁO CHUÔNG do lệnh quét gửi: có ngoại lệ, N <= M thì KHÔNG gửi.\n"
     "   => Nhu cầu N <= M sẽ tô cam trên màn hình nhưng không ai nhận chuông. Đúng yêu cầu, không phải lỗi.\n"
     "- Nhu cầu quá hạn vẫn nằm trong danh sách cho tới lần quét kế tiếp (01:20 hôm sau) mới chuyển sang Đóng — "
     "trong khoảng đó cột hạn hiện '(quá hạn X ngày)' là đúng.\n"
     "- Ngày đóng là ngày HẾT HẠN chứ không phải ngày chạy quét.\n"
     "- Sửa N ở danh mục làm hạn của mọi nhu cầu thuộc lĩnh vực đó đổi ngay, kể cả nhu cầu cũ.\n"
     "- LƯU Ý: Yêu cầu gốc viết badge là 'Đã đóng', hệ thống đang hiển thị 'Đóng' (nhãn có sẵn của màn nhu cầu). "
     "Ghi nhận là điểm cần chốt lại với người viết yêu cầu, không tự sửa.\n"
     "- Nút Tạo Dự án TKT với nhu cầu đã đóng bị ẩn hẳn (quy ước dự án: không hiện nút mờ), khác với câu chữ "
     "'làm mờ kèm tooltip' trong yêu cầu gốc."),
]

ROLE_TCS = [
    ("00", "Người có quyền quản lý danh mục khai được N", "P0",
     "Tài khoản A có quyền \"%s\". Có lĩnh vực LVCTKD.0001 - Công nghiệp." % P_SCOPE_MANAGE,
     "1. Đăng nhập tài khoản A\n2. Vào Danh mục › Lĩnh vực Công ty kinh doanh\n3. Bấm Sửa dòng LVCTKD.0001\n"
     "4. Quan sát ô 'Thời gian hiệu lực nhu cầu (ngày)'",
     "—",
     "- Ô hiện ra, nhập được, có dấu * đỏ và biểu tượng thông tin giải thích\n- Lưu được giá trị mới"),

    ("01", "Người chỉ có quyền xem danh mục không sửa được N", "P0",
     "Tài khoản B chỉ có quyền \"%s\"." % P_SCOPE_VIEW,
     "1. Đăng nhập tài khoản B\n2. Vào Danh mục › Lĩnh vực Công ty kinh doanh\n3. Bấm vào mã để mở cửa sổ xem",
     "—",
     "- Cột 'Thời gian hiệu lực (ngày)' vẫn xem được trên bảng\n"
     "- Trong cửa sổ xem, ô 'Thời gian hiệu lực nhu cầu (ngày)' ở trạng thái khoá, không gõ được\n"
     "- Không có nút Sửa ở cột Hành động"),

    ("02", "Chặn sửa N khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản B chỉ có quyền xem danh mục. Lĩnh vực LVCTKD.0001 đang để N = 0.",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa lĩnh vực với số ngày hiệu lực = 30\n2. Mở lại màn danh mục",
     "Thời gian hiệu lực nhu cầu: 30",
     "- Hệ thống từ chối vì không có quyền\n- Cột 'Thời gian hiệu lực (ngày)' vẫn là 'Không giới hạn thời gian hiệu lực'"),

    ("03", "Người có quyền cấu hình khai được M", "P0",
     "Tài khoản C có quyền \"%s\"." % P_SETTING,
     "1. Đăng nhập tài khoản C\n2. Vào Cấu hình › Cấu hình chung\n3. Mở thẻ Quản lý dự án › thẻ con Cấu hình hạn\n"
     "4. Tìm ô 'Cảnh báo trước khi đóng nhu cầu'",
     "—",
     "- Ô hiện ra kèm đơn vị 'ngày' và biểu tượng chuông cảnh báo\n- Nhập và lưu được"),

    ("04", "Người không có quyền cấu hình không vào được màn Cấu hình chung", "P0",
     "Tài khoản D không có quyền \"%s\"." % P_SETTING,
     "1. Đăng nhập tài khoản D\n2. Mở nhóm menu Cấu hình\n3. Gõ thẳng đường dẫn màn Cấu hình chung",
     "—",
     "- Không thấy mục Cấu hình chung trong menu\n- Vào bằng đường dẫn trực tiếp thì bị từ chối, không sửa được M"),

    ("05", "Chặn sửa M khi gọi thẳng chức năng, bỏ qua giao diện", "P1",
     "Tài khoản D không có quyền cấu hình. M hiện tại là 3.",
     "1. Gọi thẳng chức năng lưu cấu hình hạn với số ngày cảnh báo = 10, bỏ qua giao diện\n"
     "2. Đăng nhập tài khoản C mở lại màn Cấu hình chung",
     "Cảnh báo trước khi đóng nhu cầu: 10",
     "- Hệ thống từ chối vì không có quyền\n- Giá trị M vẫn là 3"),

    ("06", "Phạm vi xem nhu cầu quyết định thấy hạn của nhu cầu nào", "P1",
     "Tài khoản E chỉ có quyền \"%s\" và thuộc công ty 1. Công ty 2 có 4 nhu cầu đang theo dõi." % P_DEMAND_COMPANY,
     "1. Đăng nhập tài khoản E\n2. Vào màn Nhu cầu khách hàng\n3. Quan sát danh sách và cột 'Thời gian hết hạn "
     "nhu cầu'",
     "—",
     "- Chỉ thấy nhu cầu thuộc công ty 1 kèm hạn của chúng\n- Không thấy 4 nhu cầu của công ty 2"),

    ("07", "Chặn tạo Dự án TKT từ nhu cầu đã đóng khi gọi thẳng chức năng", "P0",
     "Nhu cầu #501 đang ở trạng thái Đóng (hệ thống tự đóng do quá hạn). Tài khoản C có quyền tạo Dự án TKT.",
     "1. Gọi thẳng chức năng tạo Dự án TKT gắn nhu cầu #501, bỏ qua giao diện\n2. Mở màn Nhu cầu khách hàng",
     "Nhu cầu: #501",
     "- Hệ thống từ chối kèm đúng câu: 'Nhu cầu này đã quá hạn xử lý và bị đóng tự động. Không thể tạo Dự án tiền "
     "khả thi.'\n- Nhu cầu #501 vẫn ở trạng thái Đóng, không sinh dự án nào"),
]

S1 = [
    (1, "Cột 'Thời gian hiệu lực (ngày)' trên bảng danh mục", "P0",
     "Danh mục có LVCTKD.0001 với N = 30 và LVCTKD.KHAC với N = 0.",
     "1. Vào Danh mục › Lĩnh vực Công ty kinh doanh\n2. Quan sát bảng",
     "—",
     "- Có cột 'Thời gian hiệu lực (ngày)' nằm ngay sau cột Tên, căn phải\n"
     "- Dòng LVCTKD.0001 hiện số 30\n- Dòng LVCTKD.KHAC hiện chữ 'Không giới hạn thời gian hiệu lực' màu xám\n"
     "- LƯU Ý: Không để số 0 trơ ra"),

    (2, "Ô N trong cửa sổ Tạo mới", "P0",
     "Tài khoản có quyền quản lý danh mục.",
     "1. Bấm Tạo mới\n2. Quan sát ô 'Thời gian hiệu lực nhu cầu (ngày)'",
     "—",
     "- Ô nằm cùng hàng với Mã / Tên, có dấu * đỏ\n- Giá trị mặc định là 0\n"
     "- Bên cạnh nhãn có biểu tượng thông tin, rê chuột hiện giải thích: nhu cầu tự đóng sau bấy nhiêu ngày kể từ "
     "khi cuộc họp Hoàn thành nếu chưa lập Dự án TKT, để 0 là không đặt thời hạn"),

    (3, "Tạo mới lĩnh vực có N > 0", "P0",
     "Chưa có mã LVCTKD.N30.",
     "1. Bấm Tạo mới\n2. Nhập mã 'N30', tên 'Lĩnh vực hạn 30 ngày'\n3. Nhập 30 vào ô Thời gian hiệu lực nhu cầu\n"
     "4. Bấm Lưu",
     "Thời gian hiệu lực nhu cầu: 30",
     "- Lưu thành công\n- Dòng mới trên bảng hiện số 30 ở cột Thời gian hiệu lực (ngày)"),

    (4, "Sửa N của lĩnh vực đang có nhu cầu", "P0",
     "Lĩnh vực LVCTKD.0001 đang N = 30, có 5 nhu cầu đang theo dõi thuộc lĩnh vực này.",
     "1. Bấm Sửa dòng LVCTKD.0001\n2. Đổi N thành 60\n3. Bấm Lưu\n4. Sang màn Nhu cầu khách hàng, xem 5 nhu "
     "cầu cũ\n5. Tạo 1 nhu cầu mới thuộc lĩnh vực này rồi xem hạn của nó",
     "Thời gian hiệu lực nhu cầu: 30 -> 60",
     "- Lưu thành công\n- LƯU Ý: Hạn của cả 5 nhu cầu cũ GIỮ NGUYÊN, không lùi ngày nào (N được chụp lại lúc tạo "
     "nhu cầu)\n- Riêng nhu cầu tạo MỚI ở bước 5 mới tính theo N = 60"),

    (5, "Đặt N về 0 thì nhu cầu hết hạn treo", "P0",
     "Lĩnh vực LVCTKD.0001 đang N = 30, có nhu cầu #101 hết hạn ngày 20/09/2026.",
     "1. Sửa LVCTKD.0001, đặt N = 0, bấm Lưu\n2. Sang màn Nhu cầu khách hàng xem nhu cầu #101",
     "Thời gian hiệu lực nhu cầu: 0",
     "- Cột hạn của nhu cầu #101 chuyển thành 'Không giới hạn thời gian hiệu lực'\n- Nhu cầu không còn bị quét đóng nữa"),

    (6, "Ô N để trống báo lỗi bắt buộc", "P0",
     "Đang mở cửa sổ Tạo mới với Mã và Tên hợp lệ.",
     "1. Xoá trắng ô Thời gian hiệu lực nhu cầu\n2. Bấm Lưu",
     "Thời gian hiệu lực nhu cầu: (trống)",
     "- Ô viền đỏ kèm dòng chữ 'Bắt buộc phải nhập' ngay dưới ô\n- Cửa sổ không đóng, không tạo bản ghi\n"
     "- LƯU Ý: Ô để trống KHÔNG được ngầm hiểu thành 0"),

    (7, "Lỗi của cả 3 ô hiện cùng lúc", "P0",
     "Đang mở cửa sổ Tạo mới.",
     "1. Để trống hậu tố Mã, trống Tên, trống Thời gian hiệu lực nhu cầu\n2. Bấm Lưu",
     "—",
     "- Cả 3 ô cùng viền đỏ và cùng hiện dòng lỗi ngay lần bấm đầu tiên\n- Con trỏ nhảy vào ô Mã"),

    (8, "N là số âm", "P0",
     "Đang mở cửa sổ Tạo mới, Mã và Tên hợp lệ.",
     "1. Nhập -5 vào ô Thời gian hiệu lực nhu cầu\n2. Bấm Lưu",
     "Thời gian hiệu lực nhu cầu: -5",
     "- Báo lỗi ngay dưới ô, không lưu\n- LƯU Ý: Hệ thống không được tự đổi thành 0 hay 5"),

    (9, "N là số lẻ", "P1",
     "Đang mở cửa sổ Tạo mới, Mã và Tên hợp lệ.",
     "1. Nhập 7.5 vào ô Thời gian hiệu lực nhu cầu\n2. Bấm Lưu",
     "Thời gian hiệu lực nhu cầu: 7.5",
     "- Báo lỗi phải là số nguyên, không lưu"),

    (10, "N vượt trần 3650 ngày", "P1",
     "Đang mở cửa sổ Tạo mới, Mã và Tên hợp lệ.",
     "1. Nhập 4000 vào ô Thời gian hiệu lực nhu cầu\n2. Bấm Lưu",
     "Thời gian hiệu lực nhu cầu: 4000",
     "- Báo lỗi tối đa 3650 ngày, giữ nguyên số người dùng gõ, không lưu"),

    (11, "N đúng biên 3650", "P2",
     "Đang mở cửa sổ Tạo mới, Mã và Tên hợp lệ.",
     "1. Nhập 3650\n2. Bấm Lưu",
     "Thời gian hiệu lực nhu cầu: 3650",
     "- Lưu thành công (3650 là giá trị lớn nhất được phép)"),

    (12, "N là chữ", "P2",
     "Đang mở cửa sổ Tạo mới.",
     "1. Gõ 'abc' vào ô Thời gian hiệu lực nhu cầu\n2. Bấm Lưu",
     "Thời gian hiệu lực nhu cầu: abc",
     "- Ô không nhận chữ, hoặc báo lỗi phải là số nguyên; không lưu bản ghi"),

    (13, "Ô N khoá khi bản ghi đang Khoá", "P1",
     "Lĩnh vực LVCTKD.T1 đang ở trạng thái Khoá.",
     "1. Mở cửa sổ xem bản ghi LVCTKD.T1 bằng cách bấm vào mã\n2. Quan sát ô Thời gian hiệu lực nhu cầu",
     "—",
     "- Ô ở trạng thái khoá, không nhập được"),

    (14, "Lỗi cũ của ô N mất khi gõ lại", "P2",
     "Vừa bấm Lưu và ô N đang báo lỗi.",
     "1. Gõ lại một số hợp lệ vào ô N",
     "Thời gian hiệu lực nhu cầu: 15",
     "- Dòng lỗi đỏ và viền đỏ biến mất ngay khi gõ, chưa cần bấm Lưu"),

    (15, "N hiển thị lại đúng khi mở Sửa lần sau", "P1",
     "Lĩnh vực LVCTKD.N30 vừa lưu với N = 30.",
     "1. Đóng cửa sổ, bấm Sửa lại dòng đó",
     "—",
     "- Ô Thời gian hiệu lực nhu cầu hiện đúng 30"),
]

S2 = [
    (1, "Vị trí ô M trong Cấu hình chung", "P0",
     "Tài khoản có quyền cấu hình.",
     "1. Vào Cấu hình › Cấu hình chung\n2. Mở thẻ Quản lý dự án\n3. Mở thẻ con Cấu hình hạn\n4. Tìm ô 'Cảnh báo "
     "trước khi đóng nhu cầu'",
     "—",
     "- Ô nằm trong thẻ con Cấu hình hạn, cùng nhóm với các cấu hình hạn khác\n- Bên phải ô có chữ 'ngày'\n"
     "- Rê chuột vào nhãn hiện giải thích: trước khi nhu cầu bị tự đóng bao nhiêu ngày thì gửi thông báo nhắc, "
     "để 0 nếu không muốn cảnh báo"),

    (2, "Giá trị mặc định của M là 3", "P0",
     "Công ty chưa từng lưu cấu hình hạn lần nào.",
     "1. Vào màn Cấu hình chung › Quản lý dự án › Cấu hình hạn\n2. Quan sát ô Cảnh báo trước khi đóng nhu cầu",
     "—",
     "- Ô hiện sẵn số 3"),

    (3, "Lưu M thành công", "P0",
     "M đang là 3.",
     "1. Đổi ô Cảnh báo trước khi đóng nhu cầu thành 5\n2. Bấm nút lưu cấu hình\n3. Tải lại trang và mở lại thẻ đó",
     "Cảnh báo trước khi đóng nhu cầu: 5",
     "- Báo lưu thành công\n- Sau khi tải lại, ô vẫn hiện 5"),

    (4, "M = 0 nghĩa là không cảnh báo", "P0",
     "M đang là 3. Có nhu cầu #101 thuộc lĩnh vực N = 30, hết hạn sau 2 ngày nữa.",
     "1. Đổi M = 0 và lưu\n2. Sang màn Nhu cầu khách hàng xem nhu cầu #101\n3. Nhờ kỹ thuật chạy lệnh quét hạn "
     "nhu cầu (assign:close-expired-customer-demands) ở chế độ liệt kê",
     "Cảnh báo trước khi đóng nhu cầu: 0",
     "- Cột hạn của #101 hiện ngày hết hạn nhưng KHÔNG tô cam, không có ghi chú số ngày còn lại\n"
     "- Kết quả chạy lệnh: 0 nhu cầu được cảnh báo\n- Nhu cầu vẫn bị đóng đúng ngày hết hạn"),

    (5, "M là số âm", "P1",
     "Đang mở màn Cấu hình chung.",
     "1. Nhập -2 vào ô Cảnh báo trước khi đóng nhu cầu\n2. Bấm lưu\n3. Tải lại trang",
     "Cảnh báo trước khi đóng nhu cầu: -2",
     "- Hệ thống không nhận số âm: ô báo lỗi, hoặc sau khi lưu giá trị về 0\n- LƯU Ý: Không được lưu ra số âm rồi dùng "
     "để tính mốc cảnh báo"),

    (6, "M ghi vào lịch sử cấu hình hạn", "P0",
     "M đang là 3.",
     "1. Đổi M thành 7 và lưu\n2. Mở popup Lịch sử cấu hình hạn",
     "Cảnh báo trước khi đóng nhu cầu: 3 -> 7",
     "- Popup có dòng 'Cảnh báo trước khi đóng nhu cầu (ngày)' với giá trị cũ 3 và giá trị mới 7\n"
     "- Có tên người sửa và thời điểm sửa"),

    (7, "Không đụng tới các cấu hình hạn khác", "P1",
     "Các ô cấu hình hạn khác đang có giá trị: hạn nhiệm vụ, hạn nhập biên bản meeting…",
     "1. Chỉ đổi ô Cảnh báo trước khi đóng nhu cầu rồi lưu\n2. Kiểm tra lại các ô còn lại",
     "—",
     "- Giá trị các ô khác giữ nguyên, không bị đặt lại về mặc định"),

    (8, "M áp dụng theo công ty đang làm việc", "P1",
     "Công ty 1 đặt M = 5, công ty 2 chưa khai (hiểu là 3).",
     "1. Đăng nhập tài khoản thuộc công ty 2, mở màn Cấu hình chung\n2. Quan sát ô M",
     "—",
     "- Ô của công ty 2 hiện 3, không lấy nhầm số 5 của công ty 1"),
]

S3 = [
    (1, "Cuộc họp chuyển Hoàn thành thì có mốc tính hạn", "P0",
     "Cuộc họp M-01 có khảo sát nhu cầu, đang ở trạng thái khác Hoàn thành; lĩnh vực của nhu cầu để N = 30.",
     "1. Mở cuộc họp M-01, chuyển trạng thái sang Hoàn thành\n2. Sang màn Nhu cầu khách hàng, tìm nhu cầu của cuộc "
     "họp này\n3. Xem cột Thời gian hết hạn nhu cầu",
     "—",
     "- Trước bước 1, cột hạn ghi 'Không giới hạn thời gian hiệu lực'\n- Sau bước 1, cột hạn hiện đúng ngày = ngày hoàn thành + 30 ngày"),

    (2, "Sửa lại biên bản sau khi Hoàn thành không đẩy lùi hạn", "P0",
     "Cuộc họp M-01 Hoàn thành ngày 01/09/2026, nhu cầu hết hạn 01/10/2026 (N = 30).",
     "1. Mở lại cuộc họp M-01, sửa nội dung biên bản rồi lưu (vẫn trạng thái Hoàn thành)\n2. Xem lại cột hạn của "
     "nhu cầu",
     "—",
     "- Hạn vẫn là 01/10/2026\n- LƯU Ý: Không được nhảy thành ngày sửa + 30"),

    (3, "Cuộc họp bị chuyển khỏi Hoàn thành rồi Hoàn thành lại", "P1",
     "Cuộc họp M-01 đã Hoàn thành ngày 01/09/2026.",
     "1. Chuyển M-01 sang trạng thái khác rồi chuyển lại Hoàn thành\n2. Xem cột hạn của nhu cầu",
     "—",
     "- Hạn vẫn tính theo mốc hoàn thành LẦN ĐẦU (01/09/2026)"),

    (4, "Dữ liệu cũ có mốc tính hạn sau khi lên bản mới", "P0",
     "Cuộc họp M-99 đã Hoàn thành từ 20/08/2026 (trước khi có tính năng), giờ kết thúc cuộc họp là 20/08/2026 16:30.",
     "1. Đặt N = 30 cho lĩnh vực của nhu cầu thuộc M-99\n2. Mở màn Nhu cầu khách hàng, xem nhu cầu của M-99",
     "—",
     "- Hạn hiện 19/09/2026 (tính từ ngày kết thúc cuộc họp + 30 ngày)\n"
     "- LƯU Ý: Không lấy ngày sửa gần nhất của biên bản làm mốc"),

    (5, "Cuộc họp chưa Hoàn thành thì không có hạn", "P0",
     "Cuộc họp M-02 đang ở trạng thái Đang diễn ra, nhu cầu thuộc lĩnh vực có N = 30.",
     "1. Mở màn Nhu cầu khách hàng, tìm nhu cầu của M-02",
     "—",
     "- Cột hạn ghi 'Không giới hạn thời gian hiệu lực'\n- Nhu cầu không bao giờ bị hệ thống tự đóng khi cuộc họp chưa Hoàn thành"),
]

S4 = [
    (1, "Cột 'Thời gian hết hạn nhu cầu' có trên bảng", "P0",
     "Màn Nhu cầu khách hàng có ít nhất 1 dòng.",
     "1. Vào Nhu cầu khách hàng\n2. Quan sát dòng tiêu đề bảng",
     "—",
     "- Có cột 'Thời gian hết hạn nhu cầu', nằm sau cột 'Thời gian khánh thành dự án'\n"
     "- LƯU Ý: Không nhầm với cột 'Thời gian khánh thành dự án' (hai cột khác nhau)"),

    (2, "Nhu cầu còn xa hạn hiện ngày bình thường", "P0",
     "Nhu cầu #101 hết hạn 30/10/2026, hôm nay 15/09/2026, M = 3.",
     "1. Xem dòng #101, cột Thời gian hết hạn nhu cầu",
     "—",
     "- Hiện '30/10/2026' màu chữ bình thường, không có biểu tượng cảnh báo, không có ghi chú số ngày"),

    (3, "Nhu cầu vào vùng cảnh báo tô cam kèm số ngày còn lại", "P0",
     "M = 3, lĩnh vực của nhu cầu #102 có N = 30. Nhu cầu #102 hết hạn 17/09/2026, hôm nay 15/09/2026.",
     "1. Xem dòng #102, cột Thời gian hết hạn nhu cầu",
     "—",
     "- Hiện '17/09/2026 (còn 2 ngày)' màu CAM, đậm, có biểu tượng chuông báo\n"
     "- LƯU Ý: Màu cam chứ không phải đỏ (đỏ chỉ dành cho lỗi nhập liệu)"),

    (4, "Đúng ngày hết hạn ghi 'hết hạn hôm nay'", "P0",
     "M = 3, lĩnh vực của nhu cầu #103 có N = 30. Nhu cầu #103 hết hạn đúng hôm nay.",
     "1. Xem dòng #103",
     "—",
     "- Hiện ngày hôm nay kèm ghi chú '(hết hạn hôm nay)', tô cam"),

    (5, "Nhu cầu đã quá hạn nhưng chưa tới lượt quét", "P0",
     "M = 3, lĩnh vực của nhu cầu #104 có N = 30. Nhu cầu #104 hết hạn 12/09/2026, hôm nay 15/09/2026, lần quét gần nhất chưa chạy.",
     "1. Xem dòng #104",
     "—",
     "- Hiện '12/09/2026 (quá hạn 3 ngày)' tô cam\n"
     "- LƯU Ý: TUYỆT ĐỐI không được hiện '(còn -3 ngày)'"),

    (6, "Nhu cầu không có hạn", "P0",
     "Nhu cầu #105 thuộc lĩnh vực đang để N = 0.",
     "1. Xem dòng #105",
     "—",
     "- Cột hạn ghi 'Không giới hạn thời gian hiệu lực' màu xám nhạt"),

    (7, "Nhu cầu đã lập Dự án TKT không còn hạn", "P0",
     "Nhu cầu #106 đã gắn Dự án TKT, lĩnh vực có N = 30.",
     "1. Xem dòng #106",
     "—",
     "- Cột hạn ghi 'Không giới hạn thời gian hiệu lực'\n- Cột Trạng thái là 'Đã lập dự án TKT'"),

    (8, "Nhu cầu đã đóng không còn hạn", "P1",
     "Nhu cầu #107 đang ở trạng thái Đóng.",
     "1. Xem dòng #107",
     "—",
     "- Cột hạn ghi 'Không giới hạn thời gian hiệu lực'\n- Badge trạng thái hiện 'Đóng' màu xám"),

    (9, "Cột hạn hiện cả ở thẻ Nhu cầu của khách hàng trong Công việc của tôi", "P1",
     "Tài khoản đang phụ trách ít nhất 1 nhu cầu sắp hết hạn, thuộc lĩnh vực có N = 30 (M = 3).",
     "1. Vào Công việc của tôi\n2. Mở thẻ 'Nhu cầu của khách hàng'\n3. Quan sát cột Thời gian hết hạn nhu cầu",
     "—",
     "- Cột hiển thị giống hệt màn Nhu cầu khách hàng, cùng cách tô cam và ghi chú"),

    (10, "Bật tắt cột trong tuỳ chọn hiển thị", "P2",
     "Màn Nhu cầu khách hàng đang hiện cột hạn.",
     "1. Mở tuỳ chọn cấu hình cột\n2. Bỏ chọn cột Thời gian hết hạn nhu cầu\n3. Chọn lại",
     "—",
     "- Cột ẩn / hiện theo lựa chọn, các cột khác giữ nguyên vị trí"),

    (11, "Đổi M làm vùng cảnh báo rộng ra", "P1",
     "M = 3, nhu cầu #108 thuộc lĩnh vực có N = 30, hết hạn sau 5 ngày nữa (chưa tô cam).",
     "1. Đổi M thành 7 ở Cấu hình chung, lưu\n2. Quay lại màn Nhu cầu khách hàng, tải lại",
     "Cảnh báo trước khi đóng nhu cầu: 7",
     "- Dòng #108 chuyển sang tô cam kèm '(còn 5 ngày)'\n"
     "- Mọi dòng còn DƯỚI 7 ngày đều phải tô cam, không phải chỉ dòng đúng 7 ngày"),

    (12, "Nhu cầu có N nhỏ hơn M vẫn tô cam trên màn hình", "P0",
     "M = 7, nhu cầu #109 thuộc lĩnh vực có N = 5 (tức N nhỏ hơn M), còn 2 ngày là hết hạn.",
     "1. Mở màn Nhu cầu khách hàng, xem dòng #109\n2. Chạy lệnh quét hạn nhu cầu, xem chuông "
     "thông báo",
     "Thời gian hiệu lực nhu cầu: 5 · Cảnh báo trước khi đóng: 7",
     "- Bước 1: dòng #109 CÓ tô cam kèm '(còn 2 ngày)' — cột hạn luôn cho biết nhu cầu còn mấy "
     "ngày nữa tự đóng, không phụ thuộc N lớn hay nhỏ hơn M\n"
     "- Bước 2: KHÔNG ai nhận thông báo chuông cho #109 — đúng ngoại lệ 'N <= M thì bỏ qua bước "
     "gửi thông báo' của yêu cầu, không phải lỗi\n"
     "- LƯU Ý: đây là 2 luồng khác nhau. Tô cam trên màn hình nói 'sắp tự đóng'; thông báo "
     "chuông là một hành động riêng và có ngoại lệ riêng\n"
     "- Nhu cầu vẫn bị đóng đúng hạn như thường"),
]

S5 = [
    (1, "Cảnh báo đúng mốc T + N - M", "P0",
     "M = 3, lĩnh vực N = 30. Cuộc họp Hoàn thành 16/08/2026 -> nhu cầu #201 hết hạn 15/09/2026. Hôm nay 12/09/2026. "
     "Nhu cầu chưa từng được cảnh báo, chưa lập dự án.",
     "1. Nhờ kỹ thuật chạy lệnh quét hạn nhu cầu (assign:close-expired-customer-demands)\n2. Đọc kết quả in ra\n"
     "3. Đăng nhập tài khoản chủ trì cuộc họp, mở chuông thông báo",
     "—",
     "- Kết quả in ra có dòng CẢNH BÁO cho nhu cầu #201 — còn 3 ngày, hết hạn 15/09/2026\n"
     "- Người chủ trì nhận được 1 thông báo trong ứng dụng, nội dung nêu tên khách hàng - nhu cầu và số ngày còn "
     "lại trước khi tự đóng\n- Bấm vào thông báo mở đúng màn Nhu cầu khách hàng"),

    (2, "Chưa tới mốc cảnh báo thì im lặng", "P0",
     "Như trên (M = 3, lĩnh vực N = 30) nhưng hôm nay là 10/09/2026 — còn 5 ngày, vùng cảnh báo là 3 ngày.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Đọc kết quả",
     "—",
     "- Không có dòng cảnh báo nào cho nhu cầu #201\n- Không ai nhận được thông báo"),

    (3, "Không cảnh báo lại mỗi ngày", "P0",
     "Nhu cầu #201 (lĩnh vực N = 30, M = 3) đã được cảnh báo hôm 12/09/2026.",
     "1. Ngày 13/09/2026 chạy lại lệnh quét hạn nhu cầu\n2. Đọc kết quả và kiểm tra chuông thông báo",
     "—",
     "- Không có dòng cảnh báo lặp lại cho #201\n- Người chủ trì không nhận thêm thông báo thứ hai"),

    (4, "N <= M thì bỏ qua cảnh báo", "P0",
     "M = 3, lĩnh vực đặt N = 2. Cuộc họp Hoàn thành hôm qua -> nhu cầu #202 hết hạn ngày mai.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Đọc kết quả",
     "Thời gian hiệu lực nhu cầu: 2 · Cảnh báo trước khi đóng: 3",
     "- Không có dòng cảnh báo cho #202\n- LƯU Ý: Đây là đúng yêu cầu (thời gian hiệu lực ngắn hơn thời gian cảnh báo "
     "thì bỏ cảnh báo), không phải lỗi thiếu thông báo\n- Nhu cầu vẫn sẽ bị đóng đúng ngày hết hạn"),

    (5, "N bằng đúng M", "P1",
     "M = 3, lĩnh vực N = 3.",
     "1. Chạy lệnh quét hạn nhu cầu với nhu cầu đang trong 3 ngày cuối\n2. Đọc kết quả",
     "Thời gian hiệu lực: 3 · Cảnh báo trước: 3",
     "- Không cảnh báo (điều kiện là thời gian hiệu lực phải LỚN HƠN thời gian cảnh báo)"),

    (6, "Người nhận cảnh báo gồm cả 3 vai", "P0",
     "Cuộc họp M-01 do Nguyễn Thị Cần chủ trì, do Trần Văn B tạo hộ. Nhu cầu #201 đã bàn giao cho Lê Thị C phụ "
     "trách, đang trong vùng cảnh báo.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Kiểm tra chuông thông báo của cả 3 tài khoản",
     "—",
     "- CẢ 3 đều nhận thông báo: Lê Thị C (nhân sự phụ trách nhu cầu), Trần Văn B (người tạo cuộc họp), "
     "Nguyễn Thị Cần (người chủ trì)\n- Mỗi người nhận ĐÚNG 1 thông báo; nếu một người giữ nhiều vai thì cũng "
     "chỉ nhận 1, không nhận trùng\n- Nhu cầu CHƯA bàn giao lần nào thì người phụ trách hiểu là người chủ trì"),

    (7, "Nội dung thông báo đúng khuôn", "P1",
     "Nhu cầu #201 của khách 'Công ty ABC', nhu cầu 'Dây chuyền sơn', còn 3 ngày.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Mở chuông thông báo đọc nội dung",
     "—",
     "- Nội dung nêu rõ: tên khách hàng - tên nhu cầu, cụm 'Sắp đến hạn', và câu 'Tự đóng sau 3 ngày, lập Dự án "
     "TKT nếu cần.'\n- Tên nhu cầu in đậm, toàn bộ câu không quá dài"),

    (8, "Không cảnh báo nhu cầu đã lập dự án", "P0",
     "Nhu cầu #203 đã gắn Dự án TKT, lĩnh vực N = 30, đang trong vùng 3 ngày cuối.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Đọc kết quả",
     "—",
     "- Không có dòng cảnh báo cho #203"),

    (9, "Không cảnh báo nhu cầu lĩnh vực N = 0", "P0",
     "Nhu cầu #204 thuộc lĩnh vực N = 0.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Đọc kết quả",
     "—",
     "- #204 nằm trong nhóm 'bỏ qua vì không đặt thời hạn', không cảnh báo, không đóng"),

    (10, "Chế độ chạy thử không ghi dữ liệu", "P1",
     "Có 2 nhu cầu trong vùng cảnh báo và 1 nhu cầu quá hạn.",
     "1. Chạy lệnh quét hạn nhu cầu ở chế độ liệt kê (dry-run)\n2. Kiểm tra chuông thông báo và trạng thái nhu cầu",
     "—",
     "- Kết quả in ra đủ 2 dòng cảnh báo và 1 dòng đóng\n- Nhưng KHÔNG ai nhận thông báo, trạng thái nhu cầu không "
     "đổi"),
]

S6 = [
    (1, "Tự đóng đúng ngày hết hạn", "P0",
     "M = 3, N = 30, cuộc họp Hoàn thành 16/08/2026 -> nhu cầu #301 hết hạn 15/09/2026. Hôm nay 15/09/2026.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Mở màn Nhu cầu khách hàng xem #301",
     "—",
     "- Kết quả in ra có dòng ĐÓNG cho #301 — hết hạn 15/09/2026\n"
     "- Trạng thái #301 chuyển sang 'Đóng', badge màu xám\n- Cột hạn chuyển thành 'Không giới hạn thời gian hiệu lực'"),

    (2, "Ngày đóng ghi đúng ngày hết hạn dù chạy muộn", "P0",
     "Nhu cầu #302 hết hạn 10/09/2026 nhưng việc quét không chạy mấy ngày; hôm nay 15/09/2026.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Mở chi tiết / lịch sử của nhu cầu #302 xem ngày đóng",
     "—",
     "- Nhu cầu chuyển sang Đóng\n- LƯU Ý: Ngày đóng ghi 10/09/2026 (ngày hết hạn thật), KHÔNG phải 15/09/2026"),

    (3, "Chưa tới hạn thì chưa đóng", "P0",
     "Nhu cầu #303 hết hạn 20/09/2026, hôm nay 15/09/2026.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Kiểm tra trạng thái #303",
     "—",
     "- Vẫn 'Đang theo dõi', không bị đóng"),

    (4, "Không đóng nhu cầu đã lập Dự án TKT", "P0",
     "Nhu cầu #304 quá hạn 5 ngày nhưng đã gắn Dự án TKT.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Kiểm tra #304",
     "—",
     "- Không bị đóng, trạng thái vẫn là 'Đã lập dự án TKT'"),

    (5, "Không đụng nhu cầu đã đóng tay trước đó", "P0",
     "Nhu cầu #305 đã được người dùng đóng tay kèm ghi chú 'Khách dừng đầu tư'.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Mở #305 xem ghi chú đóng",
     "—",
     "- Ghi chú và người đóng giữ nguyên, không bị ghi đè thành đóng tự động"),

    (6, "Chạy lại nhiều lần cho cùng kết quả", "P0",
     "Vừa chạy quét xong, đã đóng 3 nhu cầu.",
     "1. Chạy lại lệnh quét hạn nhu cầu ngay lập tức\n2. Đọc kết quả",
     "—",
     "- Lần 2 báo đóng 0 nhu cầu, cảnh báo 0 nhu cầu\n- Không nhu cầu nào bị đóng hai lần, không ai nhận thông báo "
     "lặp"),

    (7, "Dòng tổng kết sau khi chạy", "P1",
     "Có 2 nhu cầu tới hạn, 1 nhu cầu trong vùng cảnh báo, 30 nhu cầu thuộc lĩnh vực N = 0.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Đọc dòng tổng kết cuối cùng",
     "—",
     "- Ghi 'Đã đóng 2 nhu cầu, cảnh báo 1 nhu cầu (bỏ qua 30 nhu cầu không đặt thời hạn).'"),

    (8, "Đặt N nhỏ làm nhu cầu cũ tới hạn ngay", "P1",
     "Nhiều nhu cầu cũ của lĩnh vực LVCTKD.0001, cuộc họp Hoàn thành từ 3 tháng trước; lĩnh vực đang N = 0.",
     "1. Sửa lĩnh vực đặt N = 30\n2. Chạy lệnh quét hạn nhu cầu ở chế độ liệt kê\n3. Đọc kết quả",
     "Thời gian hiệu lực nhu cầu: 30",
     "- Kết quả liệt kê toàn bộ nhu cầu cũ sẽ bị đóng, mỗi dòng kèm đúng ngày hết hạn riêng\n"
     "- LƯU Ý: Kiểm kỹ trước khi chạy thật: đặt N nhỏ là đóng hàng loạt nhu cầu cũ ngay lần quét kế tiếp"),

    (9, "Nhu cầu bị đóng vẫn xem được trong danh sách", "P1",
     "Nhu cầu #301 vừa bị hệ thống đóng.",
     "1. Vào màn Nhu cầu khách hàng, lọc trạng thái Đóng\n2. Mở lịch sử cập nhật của #301",
     "Trạng thái: Đóng",
     "- Dòng #301 vẫn nằm trong danh sách khi lọc trạng thái Đóng\n- Lịch sử cho thấy nhu cầu bị đóng, người đóng "
     "để trống nghĩa là hệ thống tự đóng"),
]

S7 = [
    (1, "Ẩn nút Tạo Dự án TKT khi nhu cầu đã đóng", "P0",
     "Nhu cầu #301 đang Đóng, chưa có dự án.",
     "1. Vào màn Nhu cầu khách hàng, tìm dòng #301\n2. Quan sát cột Dự án TKT",
     "—",
     "- Ô chỉ hiện dấu '—', KHÔNG còn nút Tạo Dự án TKT\n"
     "- LƯU Ý: Yêu cầu gốc ghi 'làm mờ kèm tooltip' nhưng quy ước dự án là ẩn hẳn — ghi nhận, không tính là lỗi"),

    (2, "Nút Tạo Dự án TKT còn nguyên với nhu cầu đang theo dõi", "P0",
     "Nhu cầu #303 đang theo dõi, chưa có dự án.",
     "1. Tìm dòng #303, quan sát cột Dự án TKT",
     "—",
     "- Hiện nút 'Tạo Dự án TKT', bấm được và mở màn lập dự án"),

    (3, "Chặn lập dự án khi nhu cầu bị đóng ngay lúc đang mở form", "P0",
     "Người dùng đã mở form lập Dự án TKT từ nhu cầu #306; trong lúc đó việc quét chạy và đóng #306.",
     "1. Quay lại form đang mở, điền đủ thông tin\n2. Bấm Lưu",
     "—",
     "- Hệ thống từ chối kèm câu: 'Nhu cầu này đã quá hạn xử lý và bị đóng tự động. Không thể tạo Dự án tiền khả "
     "thi.'\n- Không tạo ra dự án nào"),

    (4, "Gắn thêm nhu cầu đã đóng vào dự án đang sửa", "P0",
     "Dự án TKT DA-01 đang sửa; nhu cầu #301 đã Đóng.",
     "1. Mở màn Sửa dự án DA-01\n2. Chọn nhu cầu #301 vào dự án\n3. Bấm Lưu",
     "Nhu cầu: #301",
     "- Bị chặn với đúng câu thông báo như mục 3\n- Dự án không lưu được liên kết đó"),

    (5, "Nhu cầu đóng tay cũng bị chặn lập dự án", "P1",
     "Nhu cầu #305 do người dùng đóng tay.",
     "1. Thử lập Dự án TKT từ #305",
     "—",
     "- Không có nút Tạo Dự án TKT; gọi thẳng chức năng cũng bị chặn"),

    (6, "Nhu cầu đã có dự án thì hiện liên kết thay vì nút", "P2",
     "Nhu cầu #106 đã gắn dự án DA-02.",
     "1. Xem cột Dự án TKT của dòng #106",
     "—",
     "- Hiện mã dự án bấm được, dẫn sang màn chi tiết dự án, không còn nút tạo mới"),
]

S8 = [
    (1, "Badge trạng thái của nhu cầu bị đóng", "P0",
     "Nhu cầu #301 vừa bị hệ thống đóng.",
     "1. Xem cột Trạng thái của dòng #301 ở màn Nhu cầu khách hàng, ở thẻ Nhu cầu của khách hàng trong Công việc "
     "của tôi, và trong biên bản cuộc họp phát sinh nhu cầu",
     "—",
     "- Cả 3 nơi đều hiện cùng một nhãn trạng thái màu xám\n"
     "- LƯU Ý: Hệ thống đang ghi 'Đóng' trong khi yêu cầu gốc ghi 'Đã đóng' — ghi nhận để chốt lại, không tự sửa"),

    (2, "Ô N chỉ nhận số nguyên không âm ở mọi đường ghi", "P0",
     "Tài khoản có quyền quản lý danh mục.",
     "1. Gọi thẳng chức năng Sửa lĩnh vực với số ngày hiệu lực = -1, bỏ qua giao diện\n2. Lặp lại với giá trị 'abc' "
     "và 5000",
     "Thời gian hiệu lực nhu cầu: -1 / abc / 5000",
     "- Cả 3 lần đều bị từ chối kèm thông báo tương ứng (không âm, phải là số nguyên, tối đa 3650 ngày)\n"
     "- Giá trị cũ trong danh mục không đổi"),

    (3, "Bỏ trống N khi gọi thẳng chức năng", "P0",
     "Lĩnh vực LVCTKD.0001 đang N = 30.",
     "1. Gọi thẳng chức năng Sửa lĩnh vực, không gửi số ngày hiệu lực",
     "—",
     "- Bị từ chối với thông báo bắt buộc phải nhập\n- LƯU Ý: Không được ngầm hiểu thành 0 rồi tắt hạn của cả lĩnh vực"),

    (4, "Lĩnh vực đang khoá không sửa được N", "P1",
     "Lĩnh vực LVCTKD.T1 đang Khoá, N = 30.",
     "1. Gọi thẳng chức năng Sửa lĩnh vực đó với N = 10",
     "—",
     "- Bị từ chối vì bản ghi đang khoá, phải mở khoá trước\n- N vẫn là 30"),

    (5, "Xuất Excel danh mục có cột thời gian hiệu lực", "P2",
     "Danh mục có lĩnh vực N = 30 và lĩnh vực N = 0.",
     "1. Bấm Xuất Excel ở màn danh mục\n2. Mở file",
     "—",
     "- Nếu file có cột thời gian hiệu lực thì giá trị phải khớp bảng (30 và 'Không giới hạn thời gian hiệu lực'/0)\n"
     "- Nếu file không có cột này thì ghi nhận là điểm cần bổ sung, không phải lỗi chặn"),

    (6, "Bỏ trống cả Mã, Tên và N thì cả 3 ô đều báo lỗi", "P0",
     "Đang mở form Thêm mới lĩnh vực, chưa nhập gì.",
     "1. Bấm Lưu ngay khi form còn trống",
     "—",
     "- CẢ 3 ô Mã, Tên, Thời gian hiệu lực đều viền đỏ kèm text lỗi\n"
     "- LƯU Ý: Không được chỉ mỗi ô Thời gian hiệu lực báo đỏ"),

    (7, "Câu báo lỗi khi bỏ trống N và M", "P0",
     "Form lĩnh vực và màn Cấu hình chung › Cấu hình hạn.",
     "1. Xoá trắng ô Thời gian hiệu lực nhu cầu rồi bấm Lưu\n"
     "2. Xoá trắng ô Cảnh báo trước khi đóng nhu cầu rồi bấm Lưu",
     "—",
     "- Cả 2 ô báo đúng câu: 'Bắt buộc nhập, kiểu số nguyên dương >= 0'\n"
     "- Không báo tiếng Anh, không báo câu chung chung"),

    (8, "Ô M không nhận số âm", "P0",
     "Màn Cấu hình chung › thẻ Quản lý dự án › thẻ con Cấu hình hạn.",
     "1. Gõ dấu trừ vào ô Cảnh báo trước khi đóng nhu cầu\n2. Thử dán giá trị -5 vào ô đó\n3. Bấm Lưu",
     "Cảnh báo trước khi đóng nhu cầu: -5",
     "- Bước 1: bàn phím KHÔNG gõ được dấu trừ\n- Bước 2: dán không vào\n"
     "- LƯU Ý: Hệ thống KHÔNG được tự kéo giá trị về 0, phải báo đỏ và chặn lưu"),

    (9, "Ô N và M không nhận ký tự e, E, dấu cộng", "P1",
     "Form lĩnh vực và màn Cấu hình hạn.",
     "1. Gõ 1e3333 vào ô Thời gian hiệu lực nhu cầu\n2. Làm tương tự với ô Cảnh báo trước khi đóng",
     "—",
     "- Không gõ được e, E, dấu cộng\n- Ô không bị rỗng trắng sau khi gõ, giá trị giữ đúng phần số đã nhập"),

    (10, "Cột hạn hiện đủ chữ, không bị cắt", "P1",
     "Danh mục có lĩnh vực để N = 0; màn Nhu cầu khách hàng có nhu cầu thuộc lĩnh vực đó.",
     "1. Mở màn Danh mục › Lĩnh vực Công ty kinh doanh, xem cột Thời gian hiệu lực\n"
     "2. Mở màn Nhu cầu khách hàng, xem cột Thời gian hết hạn nhu cầu",
     "—",
     "- Cả 2 màn hiện ĐỦ cụm 'Không giới hạn thời gian hiệu lực'\n"
     "- LƯU Ý: Không bị cắt thành '...thời gian hiệu' kèm dấu ba chấm"),
]

S9 = [
    (1, "Đổi N trong lúc nhu cầu đang chờ đóng", "P0",
     "Nhu cầu #431 hết hạn hôm nay, N chụp lúc tạo là 30.",
     "1. Trước khi chạy quét, đổi N của lĩnh vực thành 60\n2. Chạy lệnh quét hạn nhu cầu",
     "Thời gian hiệu lực nhu cầu: 30 -> 60",
     "- LƯU Ý: Nhu cầu #431 VẪN BỊ ĐÓNG hôm nay — sửa N ở danh mục KHÔNG gia hạn được nhu cầu đang chạy\n"
     "- Cột hạn không đổi, vẫn là hạn tính theo N = 30"),

    (2, "Đổi N nhỏ hơn KHÔNG làm nhu cầu quá hạn", "P0",
     "Nhu cầu #432 có cuộc họp Hoàn thành cách đây 40 ngày, N chụp lúc tạo là 60.",
     "1. Đổi N của lĩnh vực xuống 30\n2. Xem cột hạn của #432\n3. Chạy lệnh quét hạn nhu cầu",
     "Thời gian hiệu lực nhu cầu: 60 -> 30",
     "- LƯU Ý: Cột hạn KHÔNG đổi, vẫn tính theo N = 60 nên còn 20 ngày\n- Nhu cầu KHÔNG bị đóng"),

    (3, "Đổi M khi nhu cầu đã được cảnh báo", "P1",
     "Nhu cầu #433 thuộc lĩnh vực có N = 30, đã nhận cảnh báo khi M = 3.",
     "1. Đổi M thành 10\n2. Chạy lại lệnh quét hạn nhu cầu",
     "Cảnh báo trước khi đóng nhu cầu: 3 -> 10",
     "- Không gửi lại thông báo cho #433 (mỗi nhu cầu chỉ cảnh báo một lần)\n- Trên bảng, dòng vẫn tô cam"),

    (4, "Người dùng lập dự án ngay trước giờ quét", "P0",
     "Nhu cầu #434 hết hạn hôm nay; người dùng lập Dự án TKT từ nhu cầu này lúc 23:50.",
     "1. Chạy lệnh quét hạn nhu cầu sau đó\n2. Kiểm tra #434",
     "—",
     "- Không bị đóng, trạng thái là 'Đã lập dự án TKT'"),

    (5, "Hai người cùng thao tác trên một nhu cầu", "P1",
     "Người 1 đang mở form lập dự án từ nhu cầu #435; người 2 đóng tay nhu cầu đó.",
     "1. Người 1 bấm Lưu form lập dự án",
     "—",
     "- Bị chặn kèm thông báo nhu cầu đã đóng, không tạo dự án\n- Màn không treo"),

    (6, "Quét chạy khi hệ thống chưa có cấu hình M", "P1",
     "Công ty của cuộc họp chưa từng lưu cấu hình hạn.",
     "1. Chạy lệnh quét hạn nhu cầu với 1 nhu cầu còn 2 ngày tới hạn (N = 30)",
     "—",
     "- Hệ thống dùng mặc định 3 ngày: nhu cầu vẫn được cảnh báo\n- Không văng lỗi vì thiếu cấu hình"),

    (7, "Cuộc họp bị xoá hoặc thiếu người chủ trì", "P2",
     "Nhu cầu #436 tới vùng cảnh báo nhưng cuộc họp không xác định được người chủ trì lẫn người tạo.",
     "1. Chạy lệnh quét hạn nhu cầu",
     "—",
     "- Không gửi được thông báo nhưng lệnh vẫn chạy hết, các nhu cầu khác vẫn được xử lý bình thường"),
]

S10 = [
    (1, "Luồng đầy đủ: khai N và M -> cảnh báo -> tự đóng -> chặn lập dự án", "P0",
     "Lĩnh vực LVCTKD.E2E đang N = 0; cuộc họp M-E2E có 1 nhu cầu, chưa Hoàn thành; M = 3.",
     "1. Khai N = 5 cho lĩnh vực LVCTKD.E2E\n2. Chuyển cuộc họp M-E2E sang Hoàn thành\n3. Xem cột hạn của nhu cầu\n"
     "4. Chỉnh dữ liệu để nhu cầu còn 3 ngày tới hạn rồi chạy lệnh quét\n5. Chỉnh tiếp để nhu cầu tới hạn rồi chạy "
     "lệnh quét\n6. Thử lập Dự án TKT từ nhu cầu đó",
     "Thời gian hiệu lực nhu cầu: 5 · Cảnh báo trước khi đóng: 3",
     "- Bước 3: cột hạn = ngày Hoàn thành + 5 ngày\n- Bước 4: người chủ trì nhận 1 thông báo, dòng tô cam '(còn 3 "
     "ngày)'\n- Bước 5: nhu cầu chuyển Đóng, ngày đóng đúng ngày hết hạn\n"
     "- Bước 6: không còn nút Tạo Dự án TKT; gọi thẳng chức năng thì bị chặn đúng câu thông báo"),

    (2, "Luồng lập dự án kịp hạn", "P0",
     "Nhu cầu #501 thuộc lĩnh vực có N = 30 (M = 3), còn 2 ngày tới hạn, đã nhận cảnh báo.",
     "1. Bấm nút Tạo Dự án TKT từ nhu cầu #501\n2. Lập dự án và lưu\n3. Quay lại màn Nhu cầu khách hàng\n"
     "4. Chạy lệnh quét hạn nhu cầu sau ngày hết hạn",
     "—",
     "- Sau bước 2: nhu cầu chuyển 'Đã lập dự án TKT', cột hạn thành 'Không giới hạn thời gian hiệu lực'\n"
     "- Sau bước 4: nhu cầu KHÔNG bị đóng"),

    (3, "Luồng lĩnh vực không đặt thời hạn", "P1",
     "Lĩnh vực LVCTKD.KHAC để N = 0, có 10 nhu cầu cũ từ nhiều tháng trước.",
     "1. Chạy lệnh quét hạn nhu cầu\n2. Xem 10 nhu cầu đó trên màn danh sách",
     "—",
     "- Không nhu cầu nào bị đóng, không thông báo nào được gửi\n- Cả 10 dòng đều ghi 'Không giới hạn thời gian hiệu lực'"),

    (4, "Luồng hai lĩnh vực hạn khác nhau trong cùng cuộc họp", "P1",
     "Cuộc họp M-E2E2 Hoàn thành 01/09/2026, phát sinh 2 nhu cầu: một thuộc lĩnh vực N = 10, một thuộc lĩnh vực "
     "N = 40.",
     "1. Xem cột hạn của 2 nhu cầu\n2. Chạy lệnh quét hạn nhu cầu vào ngày 11/09/2026",
     "—",
     "- Nhu cầu thứ nhất hạn 11/09/2026, nhu cầu thứ hai hạn 11/10/2026\n"
     "- Lần quét ngày 11/09 chỉ đóng nhu cầu thứ nhất, nhu cầu thứ hai vẫn Đang theo dõi"),
]

SECTIONS = [
    ("I", "CẤU HÌNH THỜI GIAN HIỆU LỰC (N) Ở DANH MỤC LĨNH VỰC", S1),
    ("II", "CẤU HÌNH THỜI GIAN CẢNH BÁO (M) Ở CẤU HÌNH CHUNG", S2),
    ("III", "MỐC TÍNH HẠN — CUỘC HỌP HOÀN THÀNH", S3),
    ("IV", "HIỂN THỊ HẠN Ở MÀN NHU CẦU KHÁCH HÀNG", S4),
    ("V", "CẢNH BÁO TRƯỚC HẠN", S5),
    ("VI", "TỰ ĐỘNG ĐÓNG NHU CẦU QUÁ HẠN", S6),
    ("VII", "CHẶN TẠO DỰ ÁN TKT TỪ NHU CẦU ĐÃ ĐÓNG", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU & HIỂN THỊ TRẠNG THÁI", S8),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "E2E FLOW", S10),
]

if __name__ == "__main__":
    build(output_file=OUT, sheet_name="Trang tính1", feature_name=FEATURE, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
