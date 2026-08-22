# -*- coding: utf-8 -*-
"""Sinh testcase Excel cho man "Yeu cau kiem tra sua chua - bao hanh" (phan he Ban hang)."""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(HERE, "testcase.xlsx")
MODULE = "YC sửa chữa - bảo hành"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Kiểm thử TOÀN BỘ màn hình “Yêu cầu kiểm tra sửa chữa – bảo hành” (CSKH → Kiểm tra bảo hành sửa chữa → "
     "Yêu cầu sửa chữa - bảo hành).\n"
     " ► Đây là chứng từ MỞ ĐẦU của luồng dịch vụ: nhân viên kinh doanh ghi nhận yêu cầu của khách "
     "(thiết bị nào hỏng, hỏng gì, sửa ở đâu) rồi gửi cho phòng tiếp nhận xử lý. Phòng tiếp nhận "
     "tạo Phiếu xử lý yêu cầu từ chứng từ này, hoặc chuyển sang phòng khác, hoặc từ chối trả về.\n"
     " ► Phạm vi kiểm thử: danh sách, tìm nhanh, bộ lọc nâng cao, sắp xếp, phân trang, tùy chỉnh "
     "cột, Tạo mới, Sửa, Xem chi tiết, Lưu nháp, Lưu và gửi, Chuyển phòng tiếp nhận, Từ chối, "
     "Xóa, In phiếu, In danh sách, Xuất Excel, đính kèm tài liệu, phân quyền và ràng buộc nhập liệu.\n"
     " ► Màn hình dùng CHUNG dữ liệu với màn tương ứng bên phần mềm ERP: lập phiếu ở cổng nào thì "
     "cổng còn lại cũng thấy ngay, mã phiếu chạy chung một dãy số."),

    ("2. Đối tượng được tính / hiển thị",
     "► Danh sách mặc định hiển thị theo phạm vi quyền của người đăng nhập (xem mục 7), gồm cả "
     "phiếu gửi về phòng tiếp nhận của chính mình dù phiếu do phòng khác lập.\n"
     " ► 9 trạng thái phiếu: “Đang tạo” (xám) · “Chờ xử lý” (cam) · “Đang xử lý” (xanh dương) · "
     "“Đang CCTT” (xanh dương) · “Đã CCTT báo giá” (xanh nhạt) · “Đã báo giá” (xanh nhạt) · "
     "“Đã lập hợp đồng” (xanh nhạt) · “Đã xử lý” (xanh lá) · “Đã tư vấn điện thoại” (xanh lá). "
     "Chữ và màu của nhãn trạng thái do hệ thống quyết định, màn hình chỉ hiển thị lại.\n"
     " ► 7 cột mặc định: STT | Số phiếu | Khách hàng | Người tạo | Ngày tạo | Trạng thái | Hành động. "
     "Người dùng bật thêm cột khác qua nút Tùy chỉnh cột.\n"
     " ► Bảng “Danh mục trang thiết bị hiện có của khách hàng” gom thiết bị từ 3 nguồn: hàng công "
     "ty đã bán, thiết bị cũ của khách và thiết bị của nhà cung cấp khác."),

    ("3. Đối tượng bị ẩn / không tính",
     "► Phiếu ở trạng thái “Đang tạo” của NGƯỜI KHÁC không hiện với bất kỳ ai, kể cả người có "
     "quyền xem toàn tổng công ty. Người lập chỉ thấy phiếu nháp của chính mình.\n"
     " ► Phiếu không thuộc phạm vi quyền của người đăng nhập (xem mục 7) không hiện trong danh sách.\n"
     " ► Trong danh sách chọn khách hàng chỉ hiện khách đang Hoạt động, khách đã khóa không hiện.\n"
     " ► Nút thao tác không đủ điều kiện thì ẨN HẲN, không hiện dạng mờ: phiếu đã gửi đi thì không "
     "còn nút Sửa và Xóa; phiếu đã có Phiếu xử lý yêu cầu thì không còn nút Tạo phiếu xử lý yêu cầu, "
     "Chuyển phòng tiếp nhận và Từ chối."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "► Hai ô “Từ ngày” / “Đến ngày” lọc theo NGÀY TẠO phiếu, tính trọn ngày ở cả hai đầu (chọn "
     "cùng một ngày cho cả hai ô thì vẫn ra phiếu lập trong ngày đó).\n"
     " ► Không lọc theo ngày gửi yêu cầu hay ngày xử lý — 2 mốc này chỉ hiển thị và xuất ra file.\n"
     " ► Để trống cả hai ô thì lấy toàn bộ, không chặn khoảng thời gian tối đa."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "► Mỗi phiếu gắn với đúng 1 khách hàng và có nhiều dòng thiết bị cần kiểm tra (bảng I). "
     "Không có thiết bị nào thì không gửi đi được.\n"
     " ► Mỗi dòng thiết bị gồm: tên thiết bị, thương hiệu, model, nhà cung cấp, serial, mô tả yêu "
     "cầu và 1 tệp đính kèm (không bắt buộc).\n"
     " ► Serial có 2 cách nhập: chọn từ danh sách serial hệ thống đang quản lý, hoặc gõ tay serial "
     "mới. Cùng một serial của cùng một loại thiết bị không được chọn 2 lần trong một phiếu.\n"
     " ► Phiếu → (sau khi phòng tiếp nhận xử lý) → Phiếu xử lý yêu cầu → các chứng từ dịch vụ phía "
     "sau. Trạng thái phiếu từ “Đang xử lý” trở đi do các chứng từ sau cập nhật ngược về."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "► Cột “Tên thiết bị liên quan” khi xuất Excel và khi in gom tên các thiết bị của phiếu, mỗi "
     "tên một dòng trong cùng một ô.\n"
     " ► Bộ lọc “Tên thiết bị” trả về phiếu NÀO CÓ ÍT NHẤT MỘT dòng thiết bị khớp từ khóa; mỗi "
     "phiếu chỉ đếm một lần dù khớp nhiều dòng.\n"
     " ► Khi lưu lại, toàn bộ dòng thiết bị của phiếu được ghi đè bằng danh sách đang có trên màn "
     "hình — xóa dòng trên màn rồi lưu là dòng đó mất hẳn."),

    ("7. Phân quyền cấp",
     "Màn hình dùng 4 quyền:\n"
     " ► “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty” — thấy phiếu của mọi công "
     "ty trong tập đoàn.\n"
     " ► “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo công ty” — thấy phiếu của công ty mình, "
     "cộng thêm phiếu do chính mình lập.\n"
     " ► “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo phòng ban” — thấy phiếu của các phòng "
     "mình được giao quản lý, cộng thêm phiếu do chính mình lập.\n"
     " ► “Xử lý yêu cầu sửa chữa” — quyền của phòng tiếp nhận: Tạo phiếu xử lý yêu cầu, Chuyển "
     "phòng tiếp nhận, Từ chối. Người có quyền này còn thấy được mọi phiếu gửi về phòng mình.\n"
     " ► Không có quyền xem nào ở trên thì vẫn vào được màn hình nhưng chỉ thấy phiếu của chính mình.\n"
     " ► Ai cũng tự lập được phiếu, sửa và xóa phiếu nháp của chính mình."),

    ("8. Cách tính các ô thống kê",
     "► Ô “Hiển thị a–b / N” dưới bảng: a là số thứ tự dòng đầu của trang đang xem, b là dòng cuối, "
     "N là tổng số phiếu khớp bộ lọc (không phải tổng toàn hệ thống).\n"
     " ► Số dòng/trang chọn được 5 / 10 / 20 / 50 / 100, mặc định 10.\n"
     " ► Xuất Excel chạy theo từng đợt 2.000 dòng, có dòng chữ báo tiến độ; số dòng trong file phải "
     "bằng đúng số N nói trên.\n"
     " ► Bảng “Danh mục trang thiết bị hiện có của khách hàng” hiển thị 10 dòng mỗi trang, dòng "
     "“Hiển thị x–y / tổng” đếm theo tổng thiết bị của khách."),

    ("9. Ghi chú đọc bảng",
     "⚠️ Các bẫy dễ sai nhất của màn này:\n"
     " ► “Lưu nháp” KHÔNG bắt buộc nhập gì ngoài Khách hàng; “Lưu và gửi” mới bắt đủ 6 chỗ: "
     "Người liên hệ, Địa chỉ sửa chữa, Ghi chú, Phòng tiếp nhận xử lý, ít nhất 1 thiết bị và mô tả "
     "yêu cầu của từng thiết bị. Đừng test gửi đi rồi kết luận “lưu nháp lỏng lẻo”.\n"
     " ► Bấm “Lưu và gửi” hệ thống hỏi lại một lần nữa mới lưu; bấm Hủy thì phiếu chưa đổi gì.\n"
     " ► Phiếu đã gửi đi mà vẫn cố sửa bằng cách gõ thẳng đường dẫn màn Sửa thì hệ thống chặn và "
     "báo phiếu đã gửi, không cho lưu.\n"
     " ► Người có vai trò Quản trị cấp cao thao tác được với phiếu của MỌI phòng tiếp nhận, không "
     "bị giới hạn theo phòng đang công tác — đây là hành vi đúng, không phải lỗi phân quyền.\n"
     " ► Số phiếu sinh tự động khi lưu lần đầu, kể cả lưu nháp; đã sinh rồi thì không đổi nữa.\n"
     " ► Danh sách hành động ở màn chi tiết phải bằng đúng danh sách ở dòng tương ứng ngoài danh "
     "sách (chi tiết không có nút Xem vì đang ở màn xem)."),
]

ROLE_TCS = [
    ("00", "Người không có quyền xem nào vẫn vào được màn hình nhưng chỉ thấy phiếu của mình", "P0",
     "Tài khoản A không được gán bất kỳ quyền xem nào của màn này. A đã lập 2 phiếu; công ty của A "
     "có tổng cộng 30 phiếu do người khác lập.",
     "1. Đăng nhập bằng tài khoản A\n2. Vào CSKH → Kiểm tra bảo hành sửa chữa → Yêu cầu kiểm tra sửa chữa - bảo hành\n"
     "3. Đọc dòng “Hiển thị a–b / N” dưới bảng",
     "—",
     "- Vào được màn hình, không bị chặn\n- Chỉ hiện đúng 2 phiếu của A, tổng N = 2\n"
     "- Không thấy 30 phiếu của người khác\n- Vẫn có nút Tạo mới"),

    ("01", "Quyền xem theo tổng công ty thấy phiếu của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty”. "
     "Hệ thống có phiếu của ít nhất 2 công ty khác nhau.",
     "1. Đăng nhập bằng tài khoản B\n2. Mở màn hình danh sách\n3. Bật cột Công ty qua nút Tùy chỉnh cột\n"
     "4. Lọc lần lượt từng công ty ở ô Chọn công ty",
     "—",
     "- Thấy phiếu của cả 2 công ty\n- ⚠️ Vẫn KHÔNG thấy phiếu “Đang tạo” của người khác — phiếu "
     "nháp là riêng tư kể cả với quyền cao nhất"),

    ("02", "Quyền xem theo công ty chỉ thấy phiếu công ty mình và phiếu mình lập", "P0",
     "Tài khoản C chỉ có quyền “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo công ty”, thuộc "
     "công ty 1. Công ty 1 có 12 phiếu đã gửi; công ty 2 có 8 phiếu đã gửi; C từng lập 1 phiếu khi "
     "còn ở công ty 2.",
     "1. Đăng nhập bằng tài khoản C\n2. Mở màn hình danh sách\n3. Đếm số phiếu và đối chiếu công ty",
     "—",
     "- Thấy 12 phiếu của công ty 1 và 1 phiếu do chính C lập ở công ty 2 (tổng 13)\n"
     "- Không thấy 7 phiếu còn lại của công ty 2"),

    ("03", "Quyền xem theo phòng ban chỉ thấy phiếu của phòng mình quản lý", "P0",
     "Tài khoản D chỉ có quyền “Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo phòng ban”, được "
     "giao quản lý phòng Kinh doanh 1. Phòng Kinh doanh 1 có 6 phiếu đã gửi, phòng Kinh doanh 2 có "
     "4 phiếu đã gửi.",
     "1. Đăng nhập bằng tài khoản D\n2. Mở màn hình danh sách",
     "—",
     "- Thấy 6 phiếu của phòng Kinh doanh 1 cộng với phiếu do chính D lập\n"
     "- Không thấy 4 phiếu của phòng Kinh doanh 2"),

    ("04", "Quyền xử lý yêu cầu thấy được phiếu gửi về phòng mình dù không có quyền xem nào", "P0",
     "Tài khoản E chỉ có quyền “Xử lý yêu cầu sửa chữa”, đang công tác tại phòng Kỹ thuật. Có 3 "
     "phiếu ở trạng thái “Chờ xử lý” gửi về phòng Kỹ thuật, do người của phòng khác lập.",
     "1. Đăng nhập bằng tài khoản E\n2. Mở màn hình danh sách",
     "—",
     "- Thấy đủ 3 phiếu gửi về phòng Kỹ thuật\n- Mỗi phiếu có các nút Tạo phiếu xử lý yêu cầu, "
     "Chuyển phòng tiếp nhận, Từ chối, In"),

    ("05", "Không có quyền xử lý thì không thấy nút Chuyển phòng tiếp nhận và Từ chối", "P0",
     "Tài khoản C (chỉ có quyền xem theo công ty, không có quyền “Xử lý yêu cầu sửa chữa”). Có "
     "phiếu “Chờ xử lý” gửi về phòng của C.",
     "1. Đăng nhập bằng tài khoản C\n2. Mở danh sách, tìm phiếu “Chờ xử lý”\n"
     "3. Xem cột Hành động và mở tiếp màn chi tiết của phiếu đó",
     "—",
     "- Ở cả danh sách lẫn màn chi tiết đều KHÔNG có nút Tạo phiếu xử lý yêu cầu, Chuyển phòng "
     "tiếp nhận, Từ chối\n- ⚠️ Nút phải ẩn hẳn, không được hiện dạng mờ"),

    ("06", "Chặn Từ chối khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản C không có quyền “Xử lý yêu cầu sửa chữa”. Phiếu số hiệu bất kỳ đang ở “Chờ xử lý”.",
     "1. Đăng nhập bằng tài khoản C\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Từ chối của "
     "phiếu đó, bỏ qua giao diện\n3. Mở lại phiếu kiểm tra",
     "Lý do từ chối: “test”",
     "- Hệ thống từ chối, báo không có quyền\n- Trạng thái phiếu giữ nguyên “Chờ xử lý”, không ghi "
     "lý do từ chối nào\n- (Nhóm test này dành cho tester kỹ thuật)"),

    ("07", "Chặn Chuyển phòng tiếp nhận khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản C không có quyền “Xử lý yêu cầu sửa chữa”. Phiếu đang “Chờ xử lý”, phòng tiếp nhận "
     "hiện tại là phòng Kỹ thuật.",
     "1. Đăng nhập bằng tài khoản C\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Chuyển phòng "
     "tiếp nhận sang phòng Bảo hành\n3. Mở lại phiếu kiểm tra",
     "Phòng tiếp nhận mới: Bảo hành",
     "- Hệ thống từ chối, báo không có quyền\n- Phòng tiếp nhận vẫn là Kỹ thuật"),

    ("08", "Chặn Sửa phiếu của người khác khi gọi thẳng chức năng", "P0",
     "Phiếu nháp “Đang tạo” do tài khoản A lập. Đăng nhập bằng tài khoản B (có quyền xem tổng công ty).",
     "1. Đăng nhập bằng tài khoản B\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa phiếu "
     "nháp của A\n3. Đăng nhập lại bằng A, mở phiếu kiểm tra",
     "Ghi chú: “bi sua trom”",
     "- Hệ thống từ chối, báo phiếu không thuộc quyền chỉnh sửa\n- Nội dung phiếu của A không đổi"),

    ("09", "Chặn Xóa phiếu đã gửi đi khi gọi thẳng chức năng", "P0",
     "Phiếu do chính người đăng nhập lập, đang ở trạng thái “Chờ xử lý”.",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa phiếu đó\n2. Mở lại danh sách",
     "—",
     "- Hệ thống từ chối, báo chỉ được xóa phiếu ở trạng thái “Đang tạo” do chính mình lập\n"
     "- Phiếu vẫn còn nguyên trong danh sách cùng toàn bộ dòng thiết bị"),
]

SEC_I = [
    ("001", "Mở màn hình danh sách từ menu", "P0",
     "Tài khoản có quyền xem theo công ty, công ty có ít nhất 15 phiếu.",
     "1. Đăng nhập\n2. Vào CSKH → Kiểm tra bảo hành sửa chữa → Yêu cầu kiểm tra sửa chữa - bảo hành",
     "—",
     "- Tiêu đề màn hình: “Yêu cầu kiểm tra sửa chữa – bảo hành”\n"
     "- Bảng hiện 7 cột: STT | Số phiếu | Khách hàng | Người tạo | Ngày tạo | Trạng thái | Hành động\n"
     "- Có các nút Tạo mới, Xuất Excel, In danh sách, Tùy chỉnh cột\n- Mặc định 10 dòng/trang"),

    ("002", "Nhãn trạng thái hiển thị đúng chữ và đúng màu", "P0",
     "Có sẵn phiếu ở các trạng thái: Đang tạo, Chờ xử lý, Đã CCTT báo giá, Đã xử lý.",
     "1. Mở danh sách\n2. Đối chiếu từng nhãn ở cột Trạng thái",
     "—",
     "- “Đang tạo” nền xám, “Chờ xử lý” nền cam, “Đã CCTT báo giá” nền xanh nhạt, “Đã xử lý” nền "
     "xanh lá\n- ⚠️ Chữ và màu do hệ thống trả về, không được có trạng thái nào hiện ra số hoặc "
     "chữ tiếng Anh"),

    ("003", "Bấm số phiếu mở màn chi tiết", "P1",
     "Có ít nhất 1 phiếu bất kỳ trong danh sách.",
     "1. Mở danh sách\n2. Bấm vào số phiếu ở cột Số phiếu",
     "—",
     "- Mở màn chi tiết đúng phiếu vừa bấm\n- Tiêu đề màn: “Chi tiết yêu cầu kiểm tra sửa chữa – "
     "bảo hành: <số phiếu>”\n- Toàn bộ ô trên màn ở chế độ chỉ đọc"),

    ("004", "Màn chi tiết hiện đúng số nút hành động như ngoài danh sách", "P0",
     "Phiếu X đang ở “Chờ xử lý”, gửi về phòng của người đăng nhập, người này có quyền “Xử lý yêu "
     "cầu sửa chữa” và phiếu chưa có Phiếu xử lý yêu cầu.",
     "1. Ở danh sách, đếm các nút hành động của phiếu X (mở cả menu “Hành động khác”)\n"
     "2. Mở màn chi tiết phiếu X, đếm nút ở cuối màn",
     "—",
     "- Danh sách có: Tạo phiếu xử lý yêu cầu, Chuyển phòng tiếp nhận, Từ chối, In\n"
     "- Chi tiết có đúng 4 nút đó cộng nút Quay lại\n"
     "- ⚠️ Không được lệch: nút nào ẩn ngoài danh sách thì trong chi tiết cũng phải ẩn"),

    ("005", "Phiếu nháp của người khác không hiện", "P0",
     "Tài khoản A có 1 phiếu “Đang tạo”. Tài khoản B có quyền xem tổng công ty, cùng công ty với A.",
     "1. Đăng nhập bằng B\n2. Lọc trạng thái “Đang tạo”\n3. Tìm số phiếu nháp của A ở ô tìm nhanh",
     "Số phiếu nháp của A",
     "- Không có kết quả nào\n- ⚠️ Đây là hành vi đúng, không phải lỗi mất dữ liệu"),

    ("006", "Vào màn Sửa phiếu đã gửi bằng đường dẫn trực tiếp", "P0",
     "Phiếu Y đang ở “Chờ xử lý”, do chính người đăng nhập lập.",
     "1. Gõ thẳng đường dẫn màn Sửa của phiếu Y lên trình duyệt\n2. Quan sát",
     "—",
     "- Hệ thống không cho ở lại màn Sửa (chuyển về màn Chi tiết hoặc báo không sửa được)\n"
     "- Không có nút Lưu nháp / Lưu và gửi cho phiếu này"),
]

SEC_II = [
    ("001", "Tìm nhanh theo số phiếu", "P0",
     "Tồn tại phiếu có số hiệu đầy đủ, ví dụ TPE.YCSCBH.26.005682.",
     "1. Mở danh sách\n2. Gõ số phiếu vào ô tìm nhanh\n3. Bấm Tìm kiếm",
     "TPE.YCSCBH.26.005682",
     "- Ra đúng 1 phiếu\n- Dòng dưới bảng hiện “Hiển thị 1–1 / 1”"),

    ("002", "Tìm nhanh theo tên khách hàng", "P0",
     "Có ít nhất 5 phiếu của các khách hàng có chữ “HYUNDAI” trong tên.",
     "1. Gõ “HYUNDAI” vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "HYUNDAI",
     "- Mọi dòng trả về đều có chữ HYUNDAI ở cột Khách hàng\n- Tổng N khớp số phiếu thực tế"),

    ("003", "Tìm nhanh theo tên người tạo", "P1",
     "Có phiếu do nhân viên tên “Nguyễn Minh Hoàng” lập.",
     "1. Gõ “Nguyễn Minh Hoàng” vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Nguyễn Minh Hoàng",
     "- Mọi dòng trả về đều có đúng tên đó ở cột Người tạo\n"
     "- ⚠️ Ô tìm nhanh tìm được cả 3 thứ: số phiếu, tên khách hàng và tên người tạo — đúng như "
     "dòng gợi ý trong ô"),

    ("004", "Lọc theo trạng thái", "P0",
     "Có phiếu ở ít nhất 3 trạng thái khác nhau.",
     "1. Mở Tìm kiếm nâng cao\n2. Chọn trạng thái “Chờ xử lý”\n3. Quan sát (không bấm nút nào thêm)",
     "Trạng thái: Chờ xử lý",
     "- Danh sách tự tải lại ngay khi chọn, không cần bấm Tìm kiếm\n"
     "- Cột Trạng thái của mọi dòng đều là “Chờ xử lý”"),

    ("005", "Lọc theo khách hàng", "P1",
     "Khách hàng Z có 18 phiếu.",
     "1. Mở Tìm kiếm nâng cao\n2. Ở ô Chọn khách hàng, gõ tên khách rồi chọn Z",
     "Khách hàng: Z",
     "- Ra đúng 18 phiếu, tất cả cùng khách hàng Z"),

    ("006", "Lọc theo tên thiết bị", "P0",
     "Có phiếu chứa dòng thiết bị tên “Bệ kiểm tra phanh ô tô tải”.",
     "1. Mở Tìm kiếm nâng cao\n2. Nhập “Bệ kiểm tra” vào ô Nhập tên thiết bị",
     "Tên thiết bị: Bệ kiểm tra",
     "- Chỉ ra phiếu có ít nhất một thiết bị khớp từ khóa\n"
     "- ⚠️ Mở vài phiếu bất kỳ trong kết quả để xác nhận đúng thiết bị, mỗi phiếu chỉ xuất hiện 1 lần"),

    ("007", "Lọc theo tỉnh/thành của khách hàng", "P1",
     "Có khách hàng thuộc Hà Nội và khách hàng thuộc Ninh Bình, mỗi bên có phiếu.",
     "1. Mở Tìm kiếm nâng cao\n2. Chọn tỉnh/TP Hà Nội",
     "Tỉnh/TP: Hà Nội",
     "- Chỉ còn phiếu của khách hàng có địa chỉ thuộc Hà Nội"),

    ("008", "Lọc theo khoảng ngày tạo", "P0",
     "Có phiếu lập ngày 28/07/2026 và phiếu lập ngày 19/08/2026.",
     "1. Mở Tìm kiếm nâng cao\n2. Chọn Từ ngày 28/07/2026, Đến ngày 28/07/2026",
     "Từ ngày: 28/07/2026 — Đến ngày: 28/07/2026",
     "- Ra đúng các phiếu lập trong ngày 28/07/2026\n"
     "- ⚠️ Chọn cùng một ngày ở cả 2 ô vẫn phải ra kết quả (tính trọn ngày)"),

    ("009", "Lọc theo công ty và phòng ban", "P1",
     "Người đăng nhập có quyền xem tổng công ty; công ty 1 có phiếu của nhiều phòng.",
     "1. Mở Tìm kiếm nâng cao\n2. Chọn công ty 1\n3. Chọn tiếp phòng ban Kinh doanh 1",
     "Công ty: 1 — Phòng ban: Kinh doanh 1",
     "- Tổng N giảm dần đúng theo từng lần chọn\n- Chọn lại công ty khác thì ô phòng ban tự xóa "
     "lựa chọn cũ"),

    ("010", "Kết hợp nhiều điều kiện lọc", "P0",
     "Có ít nhất 1 phiếu “Chờ xử lý” của khách hàng Z lập trong tháng 7/2026.",
     "1. Chọn trạng thái “Chờ xử lý”\n2. Chọn khách hàng Z\n3. Chọn Từ ngày 01/07/2026, Đến ngày "
     "31/07/2026",
     "Trạng thái: Chờ xử lý — Khách hàng: Z — 01/07/2026 đến 31/07/2026",
     "- Kết quả thỏa mãn đồng thời cả 3 điều kiện\n- Không có dòng nào lệch trạng thái hoặc lệch khách"),

    ("011", "Nút Làm mới xóa hết điều kiện lọc", "P1",
     "Đang áp dụng 3 điều kiện lọc, danh sách còn 4 phiếu trong khi tổng thực tế là 5.368.",
     "1. Bấm nút Làm mới",
     "—",
     "- Mọi ô lọc trở về rỗng, ô tìm nhanh trống\n- Tổng N trở lại 5.368"),

    ("013", "Bộ lọc được ghi nhớ khi quay lại màn hình", "P1",
     "Đang lọc trạng thái “Chờ xử lý”.",
     "1. Mở 1 phiếu bất kỳ\n2. Bấm Quay lại về danh sách",
     "—",
     "- Bộ lọc “Chờ xử lý” vẫn còn, không phải chọn lại\n- Danh sách vẫn đúng kết quả đã lọc"),

    ("014", "Gõ Enter ở ô tìm nhanh", "P2",
     "Đang ở danh sách.",
     "1. Gõ từ khóa vào ô tìm nhanh\n2. Nhấn phím Enter",
     "HYUNDAI",
     "- Danh sách tìm ngay, không cần bấm nút Tìm kiếm"),

    ("015", "Chữ gợi ý trong các ô lọc nói đúng ô đó lọc gì", "P1",
     "Mở Tìm kiếm nâng cao.",
     "1. Đọc chữ mờ trong từng ô lọc",
     "—",
     "- Ô chọn ghi “Chọn <tên trường>”, ô gõ tay ghi “Nhập <tên trường>”\n"
     "- Ô tìm nhanh ghi rõ tìm được theo mã phiếu, tên khách hàng, người tạo\n"
     "- ⚠️ Không ô nào để trống hoặc ghi “Tất cả”"),

    ("016", "Lọc theo người tạo", "P1",
     "Nhân viên “Lê Thị Tuyết” có phiếu trong hệ thống.",
     "1. Mở Tìm kiếm nâng cao\n2. Chọn người yêu cầu là Lê Thị Tuyết",
     "Người yêu cầu: Lê Thị Tuyết",
     "- Mọi dòng đều có Người tạo là Lê Thị Tuyết"),

    ("017", "Lọc theo ngày để trống một đầu", "P2",
     "Có phiếu lập trước và sau ngày 01/08/2026.",
     "1. Chỉ nhập Từ ngày 01/08/2026, để trống Đến ngày",
     "Từ ngày: 01/08/2026",
     "- Chỉ còn phiếu lập từ 01/08/2026 trở đi, không chặn đầu trên"),

    ("012", "Bộ lọc không ra kết quả", "P1",
     "Không có phiếu nào của khách hàng tên “KHONG-TON-TAI-XYZ”.",
     "1. Gõ “KHONG-TON-TAI-XYZ” vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "KHONG-TON-TAI-XYZ",
     "- Bảng hiện đúng một dòng chữ “Không có dữ liệu phù hợp bộ lọc.”\n"
     "- ⚠️ Dòng chữ này phải màu xám, không được màu đỏ (đỏ chỉ dùng cho lỗi nhập liệu)"),
]

SEC_III = [
    ("001", "Sắp xếp theo Ngày tạo", "P1",
     "Danh sách đang có trên 20 phiếu.",
     "1. Bấm tiêu đề cột Ngày tạo\n2. Bấm lần nữa để đảo chiều",
     "—",
     "- Lần 1 sắp xếp theo một chiều, lần 2 đảo ngược lại\n- Ngày ở dòng đầu và dòng cuối đúng "
     "chiều đã chọn"),

    ("002", "Sắp xếp theo Số phiếu và Khách hàng", "P2",
     "Danh sách đang có trên 20 phiếu.",
     "1. Bấm tiêu đề cột Số phiếu\n2. Bấm tiêu đề cột Khách hàng",
     "—",
     "- Thứ tự đổi đúng theo cột vừa bấm, không mất bộ lọc đang áp dụng"),

    ("003", "Chuyển trang và đổi số dòng mỗi trang", "P0",
     "Bộ lọc hiện tại ra 5.368 phiếu.",
     "1. Bấm sang trang 2\n2. Đổi Số dòng/trang sang 50\n3. Bấm về trang 1",
     "Số dòng/trang: 50",
     "- Trang 2 hiện STT 11–20 khi để 10 dòng/trang\n- Sau khi đổi 50, dòng dưới bảng hiện "
     "“Hiển thị 1–50 / 5368”\n- Không dòng nào bị lặp giữa 2 trang"),

    ("004", "Tùy chỉnh cột hiển thị", "P1",
     "Đang ở danh sách với 7 cột mặc định.",
     "1. Bấm nút Tùy chỉnh cột\n2. Bật thêm cột Người cập nhật và Ngày cập nhật\n3. Lưu lại\n"
     "4. Thoát ra rồi vào lại màn hình",
     "Bật: Người cập nhật, Ngày cập nhật",
     "- Bảng hiện thêm đúng 2 cột vừa bật\n- Vào lại màn hình vẫn giữ nguyên các cột đã chọn"),
]

SEC_IV = [
    ("001", "Tạo phiếu và Lưu nháp với dữ liệu tối thiểu", "P0",
     "Khách hàng “CÔNG TY CỔ PHẦN SẢN XUẤT Ô TÔ HYUNDAI THÀNH CÔNG VIỆT NAM” có sẵn 56 thiết bị.",
     "1. Bấm Tạo mới\n2. Bấm vào ô Khách hàng để mở cửa sổ chọn khách\n3. Tìm và chọn khách hàng trên\n"
     "4. Ở bảng “Danh mục trang thiết bị hiện có của khách hàng”, bấm nút chọn ở dòng thiết bị đầu tiên\n"
     "5. Bấm Lưu nháp",
     "Khách hàng: CÔNG TY CỔ PHẦN SẢN XUẤT Ô TÔ HYUNDAI THÀNH CÔNG VIỆT NAM",
     "- Hệ thống báo lưu thành công và quay về danh sách\n- Phiếu mới nằm đầu danh sách, trạng "
     "thái “Đang tạo”, đã có số phiếu\n- ⚠️ Lưu nháp KHÔNG đòi Người liên hệ, Địa chỉ sửa chữa, "
     "Ghi chú hay Phòng tiếp nhận"),

    ("002", "Chọn khách hàng tự điền các thông tin liên quan", "P0",
     "Khách hàng đã khai 79 người liên hệ và 6 địa chỉ giao nhận.",
     "1. Bấm Tạo mới\n2. Bấm vào ô Khách hàng, chọn khách hàng trên\n3. Mở lần lượt ô Người liên "
     "hệ và ô Địa chỉ sửa chữa\n4. Chọn một người liên hệ bất kỳ",
     "—",
     "- Ô Loại hình tổ chức tự điền\n- Ô Người liên hệ có đủ 79 lựa chọn, ô Địa chỉ sửa chữa có 6 "
     "lựa chọn\n- Chọn người liên hệ xong thì ô Số điện thoại liên hệ tự điền theo người đó\n"
     "- Bảng thiết bị của khách tự nạp"),

    ("003", "Ô Khách hàng bấm vào là mở cửa sổ chọn", "P1",
     "Đang ở màn Tạo mới.",
     "1. Bấm thẳng vào ô Khách hàng (ô có chữ mờ “Nhấn vào đây để chọn khách hàng”)",
     "—",
     "- Cửa sổ chọn khách hàng mở ra\n- ⚠️ Không cần bấm nút kính lúp nào bên cạnh; con trỏ chuột "
     "phải đổi thành hình bàn tay khi rê vào ô"),

    ("004", "Tìm khách hàng trong cửa sổ chọn", "P0",
     "Cửa sổ chọn khách hàng đang mở.",
     "1. Gõ “HYUNDAI THÀNH CÔNG” vào ô Nhập tên / mã khách hàng\n2. Bấm Tìm kiếm\n3. Bấm vào dòng "
     "khách hàng cần chọn",
     "HYUNDAI THÀNH CÔNG",
     "- Danh sách rút gọn còn các khách khớp từ khóa\n- Bấm vào dòng nào thì cửa sổ đóng lại và ô "
     "Khách hàng hiện “<mã khách> - <tên khách>”"),

    ("005", "Thêm thiết bị từ bảng thiết bị của khách", "P0",
     "Đã chọn khách hàng có 56 thiết bị.",
     "1. Ở bảng “Danh mục trang thiết bị hiện có của khách hàng”, bấm nút thêm ở 2 dòng khác nhau\n"
     "2. Xem bảng “Danh sách thiết bị cần kiểm tra sửa chữa – bảo hành”",
     "—",
     "- Bảng trên có thêm đúng 2 dòng, tên/thương hiệu/model/nhà cung cấp chép đúng từ dòng đã chọn\n"
     "- Mỗi dòng có ô nhập Mô tả yêu cầu và ô chọn tệp đính kèm"),

    ("006", "Tìm kiếm trong bảng thiết bị của khách", "P1",
     "Khách hàng đang chọn có thiết bị tên chứa chữ “Bệ kiểm tra”.",
     "1. Nhập “Bệ kiểm tra” vào ô tìm của khối “Danh mục trang thiết bị hiện có của khách hàng”\n"
     "2. Bấm nút Tìm kiếm của khối đó\n3. Bấm nút Làm mới",
     "Bệ kiểm tra",
     "- Bảng chỉ còn thiết bị khớp từ khóa\n- Bấm Làm mới thì trở lại danh sách đầy đủ\n"
     "- ⚠️ Nút Tìm kiếm của khối này phải cùng màu với nút Tìm kiếm ngoài màn danh sách"),

    ("007", "Phân trang bảng thiết bị của khách", "P1",
     "Khách hàng đang chọn có 56 thiết bị.",
     "1. Xem dòng chữ dưới bảng thiết bị\n2. Bấm nút Sau\n3. Bấm nút chọn ở dòng đầu tiên của trang 2",
     "—",
     "- Trang 1 hiện 10 dòng, chữ “Hiển thị 1–10 / 56”\n- Trang 2 hiện số thứ tự 11–20\n"
     "- Chọn thiết bị ở trang 2 vẫn thêm đúng dòng đó vào bảng phía trên"),

    ("008", "Xóa dòng thiết bị đã chọn", "P1",
     "Bảng thiết bị cần kiểm tra đang có 2 dòng.",
     "1. Bấm nút xóa (biểu tượng thùng rác) ở dòng thứ 2\n2. Bấm Lưu nháp\n3. Mở lại phiếu",
     "—",
     "- Dòng thứ 2 biến mất khỏi bảng ngay\n- Sau khi lưu và mở lại, phiếu chỉ còn 1 dòng thiết bị"),

    ("009", "Đính kèm tài liệu cho dòng thiết bị", "P1",
     "Đang ở màn Tạo mới, đã thêm 1 dòng thiết bị. Có sẵn tệp PDF dưới 20MB.",
     "1. Ở cột đính kèm của dòng thiết bị, bấm nút Chọn tệp\n2. Chọn tệp PDF\n3. Chờ tải xong",
     "Tệp: tai-lieu-dinh-kem.pdf",
     "- Trong lúc tải hiện dòng chữ báo đang tải lên\n- Tải xong hiện biểu tượng loại tệp PDF, tên "
     "tệp và 3 nút Tải xuống / Thay đổi / Xóa\n- Bấm Tải xuống mở đúng tệp vừa gửi"),

    ("010", "Chặn đính kèm tệp sai định dạng", "P1",
     "Có sẵn tệp .txt.",
     "1. Ở cột đính kèm, bấm Chọn tệp và chọn tệp .txt",
     "Tệp: ghi-chu.txt",
     "- Hệ thống báo chỉ nhận tệp PDF, ảnh, Word hoặc Excel\n- Không có tệp nào được gắn vào dòng "
     "thiết bị"),

    ("011", "Sửa phiếu nháp", "P0",
     "Phiếu nháp do chính người đăng nhập lập, đang có 1 thiết bị.",
     "1. Ở danh sách, bấm nút Sửa của phiếu\n2. Đổi Ghi chú\n3. Thêm 1 thiết bị nữa\n4. Bấm Lưu nháp\n"
     "5. Mở lại phiếu",
     "Ghi chú: “Cập nhật lần 2”",
     "- Lưu thành công\n- Mở lại thấy Ghi chú mới và đủ 2 dòng thiết bị\n- Số phiếu KHÔNG đổi"),

    ("012", "Cảnh báo khi thoát lúc chưa lưu", "P0",
     "Đang ở màn Tạo mới.",
     "1. Gõ nội dung vào ô Ghi chú\n2. Bấm nút Quay lại",
     "Ghi chú: “thu roi man”",
     "- Hiện cửa sổ “Thông tin chưa lưu” với câu hỏi có chắc chắn muốn thoát\n"
     "- Bấm Ở lại thì vẫn ở màn hình cũ, dữ liệu còn nguyên\n- Bấm Thoát mới rời đi"),

    ("013", "Đổi khách hàng sau khi đã chọn thiết bị", "P0",
     "Phiếu đang soạn, đã chọn khách A và thêm 2 thiết bị của khách A.",
     "1. Bấm lại vào ô Khách hàng, chọn khách B\n2. Quan sát 2 bảng thiết bị",
     "Khách hàng mới: B",
     "- Bảng thiết bị của khách nạp lại theo khách B\n- ⚠️ Kiểm tra kỹ bảng thiết bị cần kiểm tra: "
     "không được còn sót thiết bị của khách A"),

    ("014", "Người liên hệ và địa chỉ giữ nguyên khi mở lại phiếu", "P0",
     "Phiếu đã lưu với người liên hệ và địa chỉ sửa chữa cụ thể.",
     "1. Mở lại màn Sửa của phiếu\n2. Xem 2 ô Người liên hệ và Địa chỉ sửa chữa",
     "—",
     "- Hai ô hiện đúng giá trị đã lưu, không bị trống\n- ⚠️ Đây là lỗi hay gặp khi danh sách lựa "
     "chọn nạp chậm, cần kiểm lại sau khi tải xong hẳn trang"),

    ("015", "Nhập serial bằng cách gõ tay", "P1",
     "Thiết bị đã có sẵn serial trong hệ thống.",
     "1. Thêm thiết bị vào bảng\n2. Chọn cách nhập serial mới và gõ một chuỗi serial chưa có\n"
     "3. Nhập mô tả yêu cầu\n4. Lưu và gửi, xác nhận\n5. Mở lại phiếu",
     "Serial: SR-GO-TAY-001",
     "- Lưu thành công\n- Mở lại thấy đúng serial vừa gõ"),

    ("016", "Thay đổi tệp đính kèm đã gắn", "P2",
     "Dòng thiết bị đã gắn 1 tệp PDF.",
     "1. Bấm nút Thay đổi ở dòng đó\n2. Chọn tệp ảnh khác\n3. Lưu nháp và mở lại",
     "Tệp mới: hien-trang.jpg",
     "- Biểu tượng đổi sang loại ảnh, tên tệp là tệp mới\n- Mở lại phiếu vẫn giữ tệp mới"),

    ("017", "Gỡ tệp đính kèm", "P2",
     "Dòng thiết bị đã gắn tệp.",
     "1. Bấm nút Xóa ở ô đính kèm\n2. Lưu nháp và mở lại phiếu",
     "—",
     "- Ô trở lại nút Chọn tệp\n- Mở lại phiếu không còn tệp nào ở dòng đó"),

    ("018", "Bảng thiết bị cuộn ngang được ở cả trên và dưới", "P2",
     "Cửa sổ trình duyệt thu hẹp để bảng bị tràn ngang.",
     "1. Thu hẹp cửa sổ\n2. Kéo thanh cuộn ngang phía TRÊN bảng\n3. Kéo thanh cuộn phía DƯỚI bảng",
     "—",
     "- Có thanh cuộn ngang ở cả trên và dưới bảng\n- Kéo bên nào thì bên kia chạy theo\n"
     "- Phóng cửa sổ đủ rộng thì thanh cuộn trên tự ẩn"),

    ("019", "Tiêu đề màn hình ghép đúng số phiếu", "P2",
     "Phiếu đã có số phiếu.",
     "1. Mở màn chi tiết\n2. Mở màn Sửa",
     "—",
     "- Chi tiết: “Chi tiết yêu cầu kiểm tra sửa chữa – bảo hành: <số phiếu>”\n"
     "- Sửa: “Sửa yêu cầu kiểm tra sửa chữa – bảo hành: <số phiếu>”"),

    ("020", "Ô chỉ đọc không gõ được", "P1",
     "Đang ở màn Tạo mới.",
     "1. Bấm vào ô Số điện thoại liên hệ và ô Loại hình tổ chức, thử gõ",
     "abc",
     "- Không gõ được vào 2 ô này, giá trị chỉ do hệ thống điền\n- Ô có nền xám phân biệt với ô nhập được"),
]

SEC_V = [
    ("001", "Gửi phiếu cho phòng tiếp nhận (Lưu và gửi)", "P0",
     "Phiếu nháp đã có: khách hàng, người liên hệ, địa chỉ sửa chữa, ghi chú, phòng tiếp nhận và 1 "
     "thiết bị đã ghi mô tả yêu cầu.",
     "1. Mở màn Sửa phiếu\n2. Bấm Lưu và gửi\n3. Ở cửa sổ hỏi lại, bấm Xác nhận",
     "—",
     "- Hệ thống hỏi xác nhận trước khi lưu\n- Sau khi xác nhận: báo thành công, quay về danh sách\n"
     "- Phiếu chuyển sang “Chờ xử lý”, không còn nút Sửa và Xóa"),

    ("002", "Hủy ở cửa sổ xác nhận thì phiếu không đổi", "P1",
     "Phiếu nháp đủ điều kiện gửi đi.",
     "1. Bấm Lưu và gửi\n2. Ở cửa sổ hỏi lại, bấm Hủy\n3. Quay về danh sách kiểm tra",
     "—",
     "- Cửa sổ đóng, vẫn ở màn Sửa\n- Phiếu giữ nguyên trạng thái “Đang tạo”"),

    ("003", "Toàn bộ nhân viên phòng tiếp nhận nhận được thông báo", "P0",
     "Phòng Kỹ thuật có 2 nhân viên là E và F. Phiếu gửi về phòng Kỹ thuật.",
     "1. Gửi phiếu đi (Lưu và gửi)\n2. Đăng nhập lần lượt bằng E và F\n3. Mở chuông thông báo",
     "—",
     "- Cả E và F đều có thông báo mới\n- Nội dung dạng: [YCSCBH] Chờ duyệt: <số phiếu>. Khách "
     "hàng: <tên khách>.\n- Bấm vào thông báo mở đúng màn chi tiết phiếu đó"),

    ("004", "Chuyển phòng tiếp nhận sang phòng khác", "P0",
     "Phiếu đang “Chờ xử lý”, phòng tiếp nhận là Kỹ thuật. Người đăng nhập có quyền “Xử lý yêu cầu "
     "sửa chữa”. Phòng Bảo hành có 3 nhân viên.",
     "1. Bấm nút Chuyển phòng tiếp nhận\n2. Chọn phòng Bảo hành\n3. Bấm nút xác nhận trên cửa sổ\n"
     "4. Đăng nhập bằng nhân viên phòng Bảo hành, mở chuông thông báo",
     "Phòng tiếp nhận mới: Bảo hành",
     "- Báo chuyển phòng thành công\n- Phiếu vẫn ở “Chờ xử lý” nhưng phòng tiếp nhận đổi thành Bảo hành\n"
     "- Cả 3 nhân viên phòng Bảo hành nhận được thông báo mới"),

    ("005", "Chặn chuyển sang đúng phòng đang tiếp nhận", "P0",
     "Phiếu đang “Chờ xử lý”, phòng tiếp nhận là Kỹ thuật.",
     "1. Bấm Chuyển phòng tiếp nhận\n2. Chọn lại đúng phòng Kỹ thuật\n3. Bấm xác nhận",
     "Phòng tiếp nhận mới: Kỹ thuật",
     "- Hệ thống báo trùng phòng tiếp nhận trước đó\n- Cửa sổ không đóng, phiếu không đổi gì"),

    ("006", "Chưa chọn phòng mà bấm xác nhận chuyển phòng", "P1",
     "Cửa sổ Chuyển phòng tiếp nhận đang mở, chưa chọn phòng nào.",
     "1. Bấm nút xác nhận",
     "—",
     "- Báo lỗi ngay dưới ô chọn phòng: bắt buộc phải nhập\n- Cửa sổ không đóng"),

    ("007", "Từ chối phiếu kèm lý do", "P0",
     "Phiếu đang “Chờ xử lý”, gửi về phòng của người đăng nhập, người này có quyền “Xử lý yêu cầu "
     "sửa chữa”. Phiếu do nhân viên G lập.",
     "1. Mở menu Hành động khác của phiếu, bấm Từ chối\n2. Nhập lý do\n3. Bấm nút Từ chối\n"
     "4. Đăng nhập bằng G, mở chuông thông báo và mở phiếu",
     "Lý do từ chối: “Thiết bị còn hạn bảo hành hãng”",
     "- Phiếu trở lại trạng thái “Đang tạo”\n- G nhận thông báo dạng: [YCSCBH] Từ chối: <số phiếu>. "
     "Lý do: Thiết bị còn hạn bảo hành hãng\n- G mở phiếu thấy lý do từ chối và sửa/gửi lại được"),

    ("008", "Từ chối mà bỏ trống lý do", "P0",
     "Cửa sổ Từ chối đang mở, ô lý do để trống.",
     "1. Bấm nút Từ chối",
     "—",
     "- Báo lỗi ngay dưới ô Lý do từ chối: bắt buộc phải nhập\n- Cửa sổ không đóng, phiếu chưa đổi "
     "trạng thái"),

    ("009", "Phiếu đã có Phiếu xử lý yêu cầu thì hết nút xử lý", "P1",
     "Phiếu đã được phòng tiếp nhận lập Phiếu xử lý yêu cầu.",
     "1. Mở danh sách, tìm phiếu đó\n2. Xem cột Hành động và mở màn chi tiết",
     "—",
     "- Không còn các nút Tạo phiếu xử lý yêu cầu, Chuyển phòng tiếp nhận, Từ chối\n- Vẫn còn nút In"),

    ("010", "Ngày gửi yêu cầu được ghi lại khi gửi đi", "P1",
     "Phiếu nháp đủ điều kiện gửi.",
     "1. Bấm Lưu và gửi, xác nhận\n2. Bật cột Ngày gửi yêu cầu qua Tùy chỉnh cột",
     "—",
     "- Cột Ngày gửi yêu cầu hiện đúng thời điểm vừa bấm gửi\n- Phiếu chưa gửi thì ô này để trống"),

    ("011", "Từ chối rồi gửi lại thì cập nhật lại ngày gửi", "P2",
     "Phiếu vừa bị từ chối, đang ở “Đang tạo”.",
     "1. Ghi lại Ngày gửi yêu cầu cũ\n2. Sửa phiếu và gửi lại\n3. Xem lại cột Ngày gửi yêu cầu",
     "—",
     "- Ngày gửi yêu cầu cập nhật theo lần gửi mới nhất"),

    ("012", "Nội dung thông báo không quá dài và bấm vào mở đúng phiếu", "P1",
     "Khách hàng có tên rất dài (trên 50 ký tự).",
     "1. Gửi phiếu của khách hàng đó\n2. Đăng nhập bằng người của phòng tiếp nhận, mở chuông\n"
     "3. Bấm vào thông báo",
     "—",
     "- Thông báo hiển thị gọn, số phiếu in đậm, tên khách bị cắt bớt nếu quá dài\n"
     "- Bấm vào mở đúng màn chi tiết phiếu vừa gửi"),

    ("013", "Người lập không nhận thông báo của chính mình gửi đi", "P2",
     "Người lập G KHÔNG thuộc phòng tiếp nhận.",
     "1. G gửi phiếu đi\n2. G mở chuông thông báo của chính mình",
     "—",
     "- G không nhận thông báo “Chờ duyệt” của phiếu do chính mình gửi\n"
     "- ⚠️ Nếu G lại đang thuộc chính phòng tiếp nhận thì có nhận là đúng"),

    ("014", "Lý do từ chối hiển thị trên phiếu", "P1",
     "Phiếu vừa bị từ chối với lý do cụ thể.",
     "1. Người lập mở phiếu\n2. Tìm ô ghi lý do từ chối",
     "—",
     "- Lý do hiện đúng nội dung đã nhập\n- ⚠️ Chữ lý do để màu xám, không tô đỏ"),
]

SEC_VI = [
    ("001", "Xóa phiếu nháp của chính mình", "P0",
     "Phiếu “Đang tạo” do chính người đăng nhập lập, có 2 dòng thiết bị.",
     "1. Bấm nút Xóa ở dòng phiếu\n2. Đọc câu hỏi xác nhận\n3. Bấm Xóa",
     "—",
     "- Cửa sổ hỏi: “Bạn có chắc muốn xóa phiếu '<số phiếu>'?”\n- Sau khi xóa: phiếu biến mất khỏi "
     "danh sách, tổng N giảm 1\n- Các dòng thiết bị của phiếu cũng bị xóa theo"),

    ("002", "Hủy ở cửa sổ xác nhận xóa", "P1",
     "Phiếu nháp của chính mình.",
     "1. Bấm nút Xóa\n2. Bấm Hủy",
     "—",
     "- Cửa sổ đóng, phiếu vẫn còn nguyên trong danh sách"),

    ("003", "Không có nút Xóa với phiếu đã gửi đi", "P0",
     "Phiếu “Chờ xử lý” do chính người đăng nhập lập.",
     "1. Xem cột Hành động của phiếu đó ở danh sách và ở màn chi tiết",
     "—",
     "- Không có nút Xóa ở cả hai nơi\n- ⚠️ Nút phải ẩn hẳn, không hiện dạng mờ"),
]

SEC_VII = [
    ("001", "Xuất Excel toàn bộ danh sách đang lọc", "P0",
     "Bộ lọc hiện tại ra 5.368 phiếu.",
     "1. Bấm nút Xuất Excel\n2. Ở cửa sổ chọn trường, giữ nguyên mặc định và bấm Xuất file\n"
     "3. Chờ tải xong rồi mở tệp",
     "—",
     "- Trong lúc chạy có dòng chữ báo tiến độ\n- Tệp tải về có tên gợi nhớ tới màn hình\n"
     "- Số dòng dữ liệu trong tệp bằng đúng 5.368\n- ⚠️ Toàn bộ phiếu phải có mặt, không dừng ở "
     "trang đang xem"),

    ("002", "Chọn trường và thứ tự cột khi xuất", "P1",
     "Cửa sổ chọn trường xuất đang mở.",
     "1. Bỏ chọn hết\n2. Chọn theo thứ tự: Số phiếu, Trạng thái, Khách hàng\n3. Bấm Xuất file",
     "Trường xuất: Số phiếu, Trạng thái, Khách hàng",
     "- Tệp chỉ có 3 cột, đúng thứ tự vừa chọn"),

    ("003", "Xuất Excel sau khi lọc", "P0",
     "Đang lọc trạng thái “Đang tạo”, còn 4 phiếu.",
     "1. Bấm Xuất Excel rồi Xuất file\n2. Mở tệp",
     "Trạng thái: Đang tạo",
     "- Tệp có đúng 4 dòng, cột Trạng thái đều là “Đang tạo”\n- ⚠️ Không được xuất cả 5.368 phiếu"),

    ("004", "In một phiếu", "P0",
     "Phiếu có 2 dòng thiết bị, đã điền đủ thông tin.",
     "1. Bấm nút In ở dòng phiếu\n2. Xem trang xem trước vừa mở",
     "—",
     "- Mở tab mới hiển thị mẫu phiếu\n- Thấy khung tờ giấy dọc có viền, giấy nền trắng\n"
     "- Trên phiếu có số phiếu, tên khách hàng, đủ 2 dòng thiết bị và khối ký tên (Người yêu cầu, "
     "Trưởng phòng yêu cầu, Phòng nhận yêu cầu, Ban giám đốc)\n"
     "- ⚠️ Không còn chỗ nào bỏ trống dạng ký hiệu chờ điền"),

    ("005", "Bố cục trang xem trước bản in", "P1",
     "Đang ở trang xem trước bản in 1 phiếu.",
     "1. Quan sát đầu trang và vị trí nút In",
     "—",
     "- Không có thanh menu xanh phía trên, không hở dải màu lạ ở đầu trang\n- Nút In nằm bên "
     "phải, thẳng mép phải tờ giấy\n- 4 ô ký tên nằm ngang hàng, chia đều bề ngang"),

    ("006", "In danh sách theo bộ lọc", "P0",
     "Đang lọc trạng thái “Đang tạo”, còn 4 phiếu.",
     "1. Bấm nút In danh sách\n2. Xem trang xem trước",
     "—",
     "- Mở tab mới với mẫu danh sách khổ ngang, có khung tờ giấy\n- Tiêu đề “DANH SÁCH PHIẾU YÊU "
     "CẦU KIỂM TRA SỬA CHỮA BẢO HÀNH”\n- Bảng có đúng 4 phiếu đang lọc\n"
     "- Nền quanh tờ giấy cùng màu với trang in 1 phiếu"),

    ("007", "Bấm nút In trên trang xem trước", "P1",
     "Đang ở trang xem trước.",
     "1. Bấm nút In",
     "—",
     "- Mở hộp thoại in của trình duyệt\n- Bản xem trong hộp thoại chỉ có nội dung phiếu, không có "
     "nút In và không có khung viền của trang xem trước"),

    ("008", "Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật trong tệp xuất", "P1",
     "Phiếu vừa được sửa bởi người khác người lập.",
     "1. Xuất Excel\n2. Mở tệp, xem 4 cột này",
     "—",
     "- 4 cột có đủ dữ liệu, đúng người và đúng thời điểm\n- Phiếu chưa ai sửa thì cột người cập "
     "nhật để trống, không hiện ký tự lạ"),

    ("009", "Cột Tên thiết bị liên quan trong tệp xuất", "P1",
     "Phiếu có 2 thiết bị tên khác nhau.",
     "1. Xuất Excel\n2. Mở tệp, xem ô Tên thiết bị liên quan của phiếu đó",
     "—",
     "- Ô chứa cả 2 tên thiết bị, mỗi tên một dòng trong cùng ô"),

    ("010", "In danh sách khi chưa lọc gì", "P2",
     "Không áp dụng bộ lọc nào, tổng 5.368 phiếu.",
     "1. Bấm In danh sách\n2. Chờ trang xem trước tải xong",
     "—",
     "- Trang hiện đủ số dòng tương ứng, không báo lỗi\n- ⚠️ Bản in rất dài, nên lọc trước khi in"),
]

SEC_VIII = [
    ("001", "Gửi đi khi bỏ trống các ô bắt buộc", "P0",
     "Phiếu nháp mới chỉ chọn khách hàng và 1 thiết bị, chưa nhập gì thêm.",
     "1. Bấm Lưu và gửi\n2. Bấm Xác nhận ở cửa sổ hỏi lại\n3. Quan sát các ô trên màn",
     "—",
     "- Phiếu KHÔNG được gửi đi, vẫn ở màn đang sửa\n- Báo lỗi đỏ ngay dưới từng ô: Người liên hệ, "
     "Địa chỉ sửa chữa, Ghi chú, Phòng tiếp nhận xử lý và ô Mô tả yêu cầu của dòng thiết bị\n"
     "- Các ô lỗi có viền đỏ, dữ liệu đã nhập vẫn còn"),

    ("002", "Gửi đi khi chưa chọn thiết bị nào", "P0",
     "Phiếu đã điền đủ thông tin chung nhưng bảng thiết bị đang trống.",
     "1. Bấm Lưu và gửi rồi Xác nhận",
     "—",
     "- Hệ thống chặn, báo phải có ít nhất 1 thiết bị\n- ⚠️ Dòng chữ “Chưa chọn thiết bị nào…” "
     "trong bảng phải màu xám, không phải màu đỏ"),

    ("003", "Chặn chọn trùng serial trong cùng một phiếu", "P0",
     "Khách hàng có thiết bị đã khai serial trong hệ thống.",
     "1. Thêm cùng một thiết bị 2 lần vào bảng\n2. Ở cả 2 dòng chọn cùng một serial\n"
     "3. Nhập mô tả yêu cầu cho cả 2 dòng\n4. Bấm Lưu và gửi rồi Xác nhận",
     "Serial: 30021180069 (cả 2 dòng)",
     "- Hệ thống chặn, báo bị trùng serial thiết bị\n- Báo lỗi ở CẢ HAI dòng bị trùng"),

    ("004", "Bắt buộc nhập serial khi thiết bị chưa có serial trong hệ thống", "P0",
     "Chọn thiết bị chưa được khai serial nào.",
     "1. Thêm thiết bị đó vào bảng\n2. Nhập mô tả yêu cầu, để trống ô serial\n"
     "3. Bấm Lưu và gửi rồi Xác nhận",
     "Serial: (để trống)",
     "- Hệ thống chặn, báo bắt buộc phải nhập tại ô serial của dòng đó"),

    ("005", "Khách hàng là cá nhân thì không có danh sách người liên hệ", "P1",
     "Có khách hàng thuộc loại cá nhân.",
     "1. Tạo phiếu, chọn khách hàng cá nhân đó\n2. Xem ô Người liên hệ",
     "—",
     "- Ô Người liên hệ chuyển thành ô chỉ đọc, điền sẵn thông tin của chính khách\n"
     "- Không mở được danh sách chọn"),

    ("006", "Lưu nháp không cần chọn thiết bị", "P1",
     "Màn Tạo mới, chỉ chọn khách hàng.",
     "1. Chọn khách hàng\n2. Bấm Lưu nháp ngay",
     "—",
     "- Lưu thành công, phiếu ở “Đang tạo”\n- ⚠️ Ràng buộc thiết bị chỉ áp dụng khi gửi đi"),

    ("007", "Bắt buộc chọn khách hàng", "P0",
     "Màn Tạo mới, chưa chọn gì.",
     "1. Bấm Lưu nháp",
     "—",
     "- Hệ thống chặn, báo lỗi đỏ ngay dưới ô Khách hàng\n- Không tạo ra phiếu nào"),
]

SEC_IX = [
    ("001", "Hai người cùng thao tác trên một phiếu", "P1",
     "Phiếu đang “Chờ xử lý”, cả E và F cùng thuộc phòng tiếp nhận và cùng mở phiếu.",
     "1. E bấm Từ chối và nhập lý do, xác nhận\n2. F (chưa tải lại trang) bấm Chuyển phòng tiếp "
     "nhận và xác nhận",
     "Lý do từ chối: “trùng phiếu”",
     "- Thao tác của F không được thực hiện hoặc hệ thống báo dữ liệu đã thay đổi\n- Không treo "
     "trang, tải lại thấy phiếu ở “Đang tạo”"),

    ("002", "Xóa phiếu vừa bị người khác xóa", "P2",
     "Hai cửa sổ trình duyệt cùng mở danh sách, cùng thấy phiếu nháp X.",
     "1. Cửa sổ 1 xóa phiếu X\n2. Cửa sổ 2 (chưa tải lại) cũng bấm Xóa phiếu X và xác nhận",
     "—",
     "- Cửa sổ 2 báo dữ liệu đã thay đổi, không treo trang\n- Danh sách tải lại không còn phiếu X"),

    ("003", "Dữ liệu lập bên ERP hiện ngay bên đây", "P0",
     "Có tài khoản dùng được cả 2 cổng.",
     "1. Lập 1 phiếu bên phần mềm ERP và gửi đi\n2. Sang màn hình này, tìm theo số phiếu vừa lập",
     "Số phiếu vừa lập bên ERP",
     "- Tìm thấy đúng phiếu đó, trạng thái “Chờ xử lý”\n- Mở chi tiết thấy đủ khách hàng và các "
     "dòng thiết bị đã nhập bên ERP"),
]

SEC_X = [
    ("001", "Luồng đầy đủ: lập → gửi → từ chối → sửa → gửi lại → chuyển phòng", "P0",
     "Nhân viên G (người lập), phòng tiếp nhận Kỹ thuật có nhân viên E, phòng Bảo hành có nhân viên H. "
     "Khách hàng có sẵn thiết bị.",
     "1. G lập phiếu, chọn khách, thêm 1 thiết bị, Lưu nháp\n2. G mở lại, điền đủ thông tin, Lưu và "
     "gửi (phòng tiếp nhận: Kỹ thuật)\n3. E nhận thông báo, mở phiếu, bấm Từ chối kèm lý do\n"
     "4. G nhận thông báo từ chối, sửa lại phiếu và gửi lại\n5. E bấm Chuyển phòng tiếp nhận sang "
     "Bảo hành\n6. H mở chuông thông báo",
     "Lý do từ chối: “Thiếu ảnh hiện trạng thiết bị”",
     "- Bước 1: phiếu “Đang tạo”, đã có số phiếu\n- Bước 2: phiếu “Chờ xử lý”, E có thông báo Chờ duyệt\n"
     "- Bước 3: phiếu về “Đang tạo”, G có thông báo Từ chối kèm lý do\n"
     "- Bước 4: phiếu lại “Chờ xử lý”, số phiếu KHÔNG đổi\n"
     "- Bước 5-6: phòng tiếp nhận thành Bảo hành, H có thông báo mới\n"
     "- Xuyên suốt: mỗi trạng thái chỉ hiện đúng các nút được phép"),

    ("002", "Luồng lập nhanh rồi xóa", "P1",
     "Nhân viên G có quyền lập phiếu.",
     "1. G lập phiếu, Lưu nháp\n2. G mở lại, thêm thiết bị, Lưu nháp\n3. G xóa phiếu\n"
     "4. Kiểm tra lại danh sách và tìm theo số phiếu vừa xóa",
     "—",
     "- Xóa xong không tìm thấy phiếu bằng số phiếu\n- Tổng N trở về như trước khi lập"),

    ("003", "Phiếu đi tiếp sang Phiếu xử lý yêu cầu", "P0",
     "Phiếu đang “Chờ xử lý”, người đăng nhập có quyền “Xử lý yêu cầu sửa chữa”.",
     "1. Bấm nút Tạo phiếu xử lý yêu cầu\n2. Hoàn tất phiếu xử lý bên màn tương ứng\n"
     "3. Quay lại màn danh sách yêu cầu, tìm phiếu ban đầu",
     "—",
     "- Trạng thái phiếu chuyển sang “Đã xử lý” (nếu phiếu xử lý được gửi đi chờ cung cấp thông "
     "tin) hoặc “Đã tư vấn điện thoại” (nếu mọi thiết bị đều chọn phương án tư vấn qua điện "
     "thoại)\n- Cột Người xử lý và Ngày xử lý của phiếu được điền\n"
     "- Phiếu không còn nút Tạo phiếu xử lý yêu cầu, Chuyển phòng tiếp nhận, Từ chối\n"
     "- ⚠️ KHÔNG có trạng thái “Đang xử lý” ở bước này — trạng thái đó tuy có trong danh mục nhưng "
     "không nghiệp vụ nào dùng tới\n- ⚠️ Màn Phiếu xử lý yêu cầu phải đã có trên hệ thống mới "
     "chạy được bước này"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "LẬP PHIẾU, SỬA & XEM", SEC_IV),
    ("V", "GỬI DUYỆT, CHUYỂN PHÒNG TIẾP NHẬN & TỪ CHỐI", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "XUẤT EXCEL / IN", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU – CUỐI", SEC_X),
]

build(output_file=OUTPUT_FILE,
      sheet_name="Trang tính1",
      feature_name="Yêu cầu kiểm tra sửa chữa – bảo hành - Cập nhật ngày 20/08/2026",
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
