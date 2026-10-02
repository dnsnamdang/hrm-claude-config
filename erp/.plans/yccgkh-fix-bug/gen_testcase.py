# -*- coding: utf-8 -*-
"""Sinh testcase luong Phieu YC chuyen giao khach hang (ERP - Kinh doanh)."""
import os, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, r"d:\CompanyProject\hrm-cursor\.claude\skills\testcase-documenter\assets")
from tc_engine import build

M = "Phiếu YC chuyển giao KH"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Cho phép nhân viên kinh doanh lập phiếu yêu cầu chuyển giao khách hàng của một hợp đồng đã ký "
     "sang một khách hàng khác (đổi bên mua), kèm lý do và tài liệu chứng minh, trình lãnh đạo duyệt. "
     "Khi phiếu được duyệt, thông tin khách hàng trên hợp đồng được cập nhật sang khách hàng mới; "
     "thông tin khách hàng cũ được lưu lại để đối chiếu."),
    ("2. Đối tượng được tính / hiển thị",
     "Màn Danh sách phiếu: hiển thị phiếu ở đủ 5 trạng thái - Đang tạo, Chờ duyệt, Đã duyệt, "
     "Không duyệt, Hủy duyệt (theo phạm vi xem của người đăng nhập).\n"
     "Màn Danh sách chờ duyệt: mặc định CHỈ hiển thị phiếu Chờ duyệt; nếu người dùng tự chọn một "
     "giá trị ở ô lọc Trạng thái thì hiển thị theo lựa chọn đó.\n"
     "Hợp đồng được phép chọn để lập phiếu: Hợp đồng bán hàng và Hợp đồng dịch vụ sửa chữa."),
    ("3. Đối tượng bị ẩn / không tính",
     "Phiếu của đơn vị ngoài phạm vi xem của người đăng nhập (theo quyền xem tổng công ty / công ty / "
     "phòng ban / bộ phận) không hiển thị.\n"
     "Nút Sửa và Xóa bị ẩn với phiếu Chờ duyệt, Đã duyệt, Hủy duyệt và với phiếu do người khác lập.\n"
     "Nút Duyệt / Không duyệt bị ẩn khi phiếu không ở trạng thái Chờ duyệt hoặc người xem không có "
     "quyền duyệt.\n"
     "Nút Hủy duyệt đã được ẩn khỏi giao diện phiếu Đã duyệt theo yêu cầu nghiệp vụ."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô Từ ngày / Đến ngày lọc theo cột Ngày lập của phiếu (không lọc theo Ngày duyệt). "
     "Nhập một đầu để trống thì lọc mở phía đó. Ngày nhập theo dạng ngày/tháng/năm."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu gắn với đúng một hợp đồng và đúng một khách hàng mới. Trong phiếu có 2 khối đối chiếu: "
     "Thông tin khách hàng cũ (chụp lại tại thời điểm lập phiếu, chỉ đọc) và Thông tin khách hàng mới "
     "(lấy từ hồ sơ khách hàng được chọn, một số ô cho sửa như Địa chỉ giao/sửa, Người đại diện, Tài khoản). "
     "Phiếu có kèm danh sách tệp đính kèm và Lịch sử duyệt ghi lại từng lần gửi duyệt / duyệt / không duyệt."),
    ("6. Quy tắc cộng dồn / deduplicate",
     "Không áp dụng - màn này không có ô thống kê cộng dồn, mỗi phiếu là một dòng độc lập, "
     "không gộp dòng theo khách hàng hay hợp đồng."),
    ("7. Phân quyền cấp",
     "Duyệt phiếu YC chuyển giao khách hàng\n"
     "Xem danh sách phiếu chuyển giao khách hàng theo tổng công ty\n"
     "Xem danh sách phiếu chuyển giao khách hàng theo công ty\n"
     "Xem danh sách phiếu chuyển giao khách hàng theo phòng ban\n"
     "Xem danh sách phiếu chuyển giao khách hàng theo bộ phận\n"
     "Người không có quyền duyệt vẫn lập được phiếu của mình nhưng không thấy nút Duyệt / Không duyệt."),
    ("8. Cách tính các ô thống kê",
     "Không có ô thống kê tổng hợp. Các ô cần đối chiếu gồm: cột Ngày lập và Ngày duyệt hiển thị dạng "
     "ngày/tháng/năm giờ:phút; cột Trạng thái hiển thị đúng một trong 5 nhãn; dòng Lịch sử duyệt sắp theo "
     "thứ tự thời gian, cột Nội dung của dòng Gửi duyệt hiển thị đúng Lý do thay đổi khách hàng đã nhập."),
    ("9. Ghi chú đọc bảng",
     "BẪY 1 - Dung lượng tệp: giới hạn thống nhất là 60MB ở cả màn hình lẫn hệ thống phía sau "
     "(trước đây màn hình ghi 60MB nhưng phía sau chỉ nhận 50MB, đã sửa ngày 03/09/2026). "
     "Cần kiểm đúng mốc: tệp 55MB và 59MB phải lưu được, tệp trên 60MB phải bị chặn.\n"
     "BẪY 2 - Sửa phiếu: khi sửa, tệp đã đính kèm trước đó được giữ nguyên nên không bắt buộc chọn tệp mới; "
     "nhưng khi tạo mới thì bắt buộc ít nhất 1 tệp.\n"
     "BẪY 3 - Người đại diện chỉ bắt buộc với khách hàng là tổ chức/doanh nghiệp; khách hàng cá nhân thì không.\n"
     "BẪY 4 - Phiếu Không duyệt vẫn cho người lập Sửa và Xóa (không phải chỉ xem).\n"
     "BẪY 5 - Ngày lập có thể sắp xếp được, các cột còn lại không sắp xếp.\n"
     "BẪY 6 - Phiếu Đang tạo chưa được cấp Số phiếu, chỉ khi Gửi duyệt mới sinh Số phiếu.\n"
     "BẪY 7 - Ở cửa sổ Thêm nhanh khách hàng, sau khi đổi Loại hình tổ chức nhiều lần rồi cuộn, "
     "trước đây nội dung bị kẹt hoặc tự nhảy về đầu - cần kiểm tra lại sau khi đã sửa."),
]

ROLE_TCS = [
    ("00", "Người không có quyền xem nào vào màn danh sách", "P0",
     "Tài khoản A không được gán bất kỳ quyền xem phiếu chuyển giao khách hàng nào. Trong hệ thống có 3 phiếu.",
     "1. Đăng nhập bằng tài khoản A\n2. Mở menu Kinh doanh > Phiếu YC chuyển giao khách hàng", "—",
     "- Hệ thống từ chối truy cập hoặc danh sách không hiện phiếu của đơn vị khác\n"
     "- Không có nút Duyệt / Không duyệt ở bất kỳ phiếu nào"),
    ("01", "Quyền xem theo tổng công ty thấy phiếu của mọi công ty", "P0",
     "Tài khoản B chỉ có quyền Xem danh sách phiếu chuyển giao khách hàng theo tổng công ty. "
     "Có 2 phiếu thuộc công ty 1 và 1 phiếu thuộc công ty 4.",
     "1. Đăng nhập bằng tài khoản B\n2. Mở màn Phiếu YC chuyển giao khách hàng\n3. Không nhập bộ lọc nào",
     "—",
     "- Danh sách hiện đủ cả 3 phiếu của cả 2 công ty\n- Cột Số phiếu, KH mới, KH cũ, Số HĐ hiển thị đúng dữ liệu"),
    ("02", "Quyền xem theo công ty chỉ thấy phiếu công ty mình", "P0",
     "Tài khoản C chỉ có quyền Xem danh sách phiếu chuyển giao khách hàng theo công ty, thuộc công ty 1. "
     "Có 2 phiếu công ty 1 và 1 phiếu công ty 4.",
     "1. Đăng nhập bằng tài khoản C\n2. Mở màn Phiếu YC chuyển giao khách hàng", "—",
     "- Chỉ hiện 2 phiếu của công ty 1\n- ⚠️ Phiếu của công ty 4 không xuất hiện kể cả khi tìm đúng số phiếu"),
    ("03", "Quyền xem theo phòng ban chỉ thấy phiếu phòng mình", "P0",
     "Tài khoản D chỉ có quyền Xem danh sách phiếu chuyển giao khách hàng theo phòng ban, thuộc phòng Kinh doanh 1. "
     "Có 1 phiếu do phòng Kinh doanh 1 lập, 1 phiếu do phòng Kinh doanh 2 lập.",
     "1. Đăng nhập bằng tài khoản D\n2. Mở màn Phiếu YC chuyển giao khách hàng", "—",
     "- Chỉ hiện phiếu do phòng Kinh doanh 1 lập\n- Phiếu của phòng Kinh doanh 2 không hiện"),
    ("04", "Quyền xem theo bộ phận chỉ thấy phiếu bộ phận mình", "P0",
     "Tài khoản E chỉ có quyền Xem danh sách phiếu chuyển giao khách hàng theo bộ phận, thuộc bộ phận Dự án. "
     "Có 1 phiếu do bộ phận Dự án lập, 1 phiếu do bộ phận khác lập.",
     "1. Đăng nhập bằng tài khoản E\n2. Mở màn Phiếu YC chuyển giao khách hàng", "—",
     "- Chỉ hiện phiếu do bộ phận Dự án lập"),
    ("05", "Có quyền duyệt thì thấy nút Duyệt và Không duyệt", "P0",
     "Tài khoản F có quyền Duyệt phiếu YC chuyển giao khách hàng. Phiếu số YCCG-0001 đang ở trạng thái Chờ duyệt.",
     "1. Đăng nhập bằng tài khoản F\n2. Mở chi tiết phiếu YCCG-0001", "—",
     "- Cuối màn có nút Duyệt (biểu tượng dấu tích) và nút Không duyệt (biểu tượng dấu X)\n- Có nút Quay lại"),
    ("06", "Không có quyền duyệt thì không thấy nút Duyệt", "P0",
     "Tài khoản G KHÔNG có quyền Duyệt phiếu YC chuyển giao khách hàng. Phiếu YCCG-0001 đang Chờ duyệt.",
     "1. Đăng nhập bằng tài khoản G\n2. Mở chi tiết phiếu YCCG-0001", "—",
     "- Không có nút Duyệt và không có nút Không duyệt\n- Vẫn xem được đầy đủ nội dung phiếu"),
    ("07", "Không có quyền duyệt, gọi thẳng chức năng Duyệt bỏ qua giao diện", "P0",
     "Tài khoản G không có quyền duyệt. Phiếu YCCG-0001 đang Chờ duyệt.",
     "1. Đăng nhập bằng tài khoản G\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Duyệt phiếu YCCG-0001, bỏ qua giao diện\n"
     "3. Mở lại chi tiết phiếu",
     "—",
     "- Hệ thống từ chối, báo không có quyền\n- ⚠️ Phiếu vẫn ở trạng thái Chờ duyệt, không bị đổi sang Đã duyệt\n"
     "- Lịch sử duyệt không phát sinh dòng mới"),
    ("08", "Không phải người lập, gọi thẳng chức năng Sửa bỏ qua giao diện", "P0",
     "Phiếu YCCG-0002 do tài khoản H lập, đang ở trạng thái Đang tạo. Tài khoản I là người khác.",
     "1. Đăng nhập bằng tài khoản I\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa phiếu YCCG-0002, bỏ qua giao diện",
     "Lý do thay đổi khách hàng: Sửa trái phép",
     "- Hệ thống từ chối, không cho sửa\n- ⚠️ Nội dung phiếu giữ nguyên như trước"),
    ("09", "Không phải người lập, gọi thẳng chức năng Xóa bỏ qua giao diện", "P0",
     "Phiếu YCCG-0002 do tài khoản H lập, trạng thái Đang tạo. Tài khoản I là người khác.",
     "1. Đăng nhập bằng tài khoản I\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa phiếu YCCG-0002, bỏ qua giao diện",
     "—",
     "- Hệ thống từ chối\n- ⚠️ Phiếu vẫn còn trong danh sách"),
    ("10", "Gọi thẳng chức năng Sửa trên phiếu đã duyệt", "P0",
     "Phiếu YCCG-0003 do tài khoản H lập, đã ở trạng thái Đã duyệt.",
     "1. Đăng nhập bằng chính tài khoản H (người lập)\n"
     "2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa phiếu YCCG-0003, bỏ qua giao diện",
     "Lý do thay đổi khách hàng: Sửa sau khi đã duyệt",
     "- Hệ thống từ chối vì phiếu đã duyệt\n- ⚠️ Thông tin khách hàng trên hợp đồng không bị thay đổi thêm lần nữa"),
]

SEC_I = [
    (1, "Mở màn danh sách phiếu hiển thị đủ cột", "P0",
     "Tài khoản có quyền xem theo công ty, công ty 1 có ít nhất 3 phiếu ở các trạng thái khác nhau.",
     "1. Mở menu Kinh doanh > Phiếu YC chuyển giao khách hàng\n2. Quan sát tiêu đề các cột", "—",
     "- Bảng có đủ các cột: STT, Số phiếu, KH mới, KH cũ, Số HĐ, Người lập, Ngày lập, Người duyệt, "
     "Ngày duyệt, Trạng thái, Hành động\n- Không có cột nào trống tiêu đề"),
    (2, "Ngày lập và Ngày duyệt hiển thị kèm giờ phút", "P1",
     "Có 1 phiếu Đã duyệt, lập lúc 08:15 ngày 20/08/2026, duyệt lúc 14:30 cùng ngày.",
     "1. Mở màn danh sách\n2. Tìm phiếu nói trên\n3. Đọc cột Ngày lập và Ngày duyệt", "—",
     "- Cột Ngày lập hiển thị 20/08/2026 08:15\n- Cột Ngày duyệt hiển thị 20/08/2026 14:30\n"
     "- ⚠️ Không hiển thị thiếu phần giờ phút"),
    (3, "Phiếu chưa duyệt để trống Người duyệt và Ngày duyệt", "P1",
     "Có 1 phiếu ở trạng thái Chờ duyệt, chưa ai duyệt.",
     "1. Mở màn danh sách\n2. Đọc dòng của phiếu Chờ duyệt", "—",
     "- Cột Người duyệt và Ngày duyệt để trống\n- Cột Trạng thái hiển thị Chờ duyệt"),
    (4, "Màn Danh sách chờ duyệt mặc định chỉ hiện phiếu Chờ duyệt", "P0",
     "Có 5 phiếu: 2 Chờ duyệt, 1 Đang tạo, 1 Đã duyệt, 1 Không duyệt.",
     "1. Mở menu Chờ duyệt > Phiếu YC chuyển giao khách hàng chờ duyệt\n2. Không chọn bộ lọc nào", "—",
     "- Chỉ hiện 2 phiếu Chờ duyệt\n- ⚠️ Không hiện phiếu Đang tạo, Đã duyệt, Không duyệt"),
    (5, "Mở chi tiết phiếu xem được 2 khối khách hàng cũ và mới", "P0",
     "Phiếu YCCG-0001 chuyển từ khách hàng Công ty ABC sang Công ty XYZ.",
     "1. Mở màn danh sách\n2. Bấm nút Xem (biểu tượng con mắt) ở dòng phiếu YCCG-0001", "—",
     "- Màn chi tiết hiện khối Thông tin khách hàng cũ với tên Công ty ABC\n"
     "- Khối Thông tin khách hàng mới hiện tên Công ty XYZ\n- Hiện được Số hợp đồng và Lý do thay đổi khách hàng"),
    (6, "Xem chi tiết phiếu Đã duyệt không bị lỗi trang", "P0",
     "Có 1 phiếu ở trạng thái Đã duyệt, đã có người duyệt và thời điểm duyệt.",
     "1. Mở màn danh sách\n2. Bấm Xem ở dòng phiếu Đã duyệt", "—",
     "- Trang chi tiết mở bình thường, không báo lỗi\n- ⚠️ Ngày duyệt hiển thị đúng dạng ngày/tháng/năm giờ:phút"),
    (7, "Màu chữ mục menu phiếu chờ duyệt đồng bộ", "P2",
     "Đã đăng nhập, menu Chờ duyệt có nhiều mục con.",
     "1. Mở menu Chờ duyệt\n2. So màu chữ mục Phiếu YC chuyển giao khách hàng với các mục còn lại", "—",
     "- Màu chữ giống hệt các mục anh em, không khác biệt"),
]

SEC_II = [
    (1, "Lọc theo Số phiếu YC", "P0",
     "Có 3 phiếu, trong đó 1 phiếu số YCCG-0002.",
     "1. Mở màn danh sách\n2. Nhập YCCG-0002 vào ô Số phiếu YC\n3. Bấm Tìm kiếm", "Số phiếu YC: YCCG-0002",
     "- Chỉ còn 1 dòng đúng phiếu YCCG-0002"),
    (2, "Lọc theo khoảng Từ ngày - Đến ngày theo Ngày lập", "P0",
     "Phiếu 1 lập 05/08/2026, phiếu 2 lập 20/08/2026, phiếu 3 lập 01/09/2026.",
     "1. Nhập Từ ngày 01/08/2026 và Đến ngày 31/08/2026\n2. Bấm Tìm kiếm",
     "Từ ngày: 01/08/2026 · Đến ngày: 31/08/2026",
     "- Hiện đúng 2 phiếu lập ngày 05/08 và 20/08\n- ⚠️ Phiếu lập 01/09/2026 không hiện\n"
     "- ⚠️ Bộ lọc chạy theo Ngày lập, không theo Ngày duyệt"),
    (3, "Chỉ nhập Từ ngày, bỏ trống Đến ngày", "P1",
     "Phiếu 1 lập 05/08/2026, phiếu 2 lập 01/09/2026.",
     "1. Nhập Từ ngày 20/08/2026, để trống Đến ngày\n2. Bấm Tìm kiếm", "Từ ngày: 20/08/2026",
     "- Chỉ hiện phiếu lập 01/09/2026\n- Không báo lỗi vì thiếu Đến ngày"),
    (4, "Lọc theo Số HĐ", "P0",
     "Phiếu YCCG-0001 gắn hợp đồng số HĐ-2026-001, phiếu YCCG-0002 gắn hợp đồng HĐ-2026-002.",
     "1. Nhập HĐ-2026-001 vào ô Số HĐ\n2. Bấm Tìm kiếm", "Số HĐ: HĐ-2026-001",
     "- Chỉ hiện phiếu YCCG-0001"),
    (5, "Lọc theo KH mới", "P0",
     "Phiếu YCCG-0001 có khách hàng mới là Công ty XYZ; phiếu YCCG-0002 khách hàng mới là Công ty DEF.",
     "1. Bấm vào ô KH mới\n2. Gõ XYZ để tìm\n3. Chọn Công ty XYZ\n4. Bấm Tìm kiếm", "KH mới: Công ty XYZ",
     "- Chỉ hiện phiếu YCCG-0001\n- Ô lọc giữ nguyên tên Công ty XYZ sau khi tìm"),
    (6, "Lọc theo KH cũ", "P1",
     "Phiếu YCCG-0001 có khách hàng cũ là Công ty ABC.",
     "1. Bấm ô KH cũ, gõ ABC, chọn Công ty ABC\n2. Bấm Tìm kiếm", "KH cũ: Công ty ABC",
     "- Chỉ hiện phiếu có khách hàng cũ là Công ty ABC"),
    (7, "Lọc theo Trạng thái", "P0",
     "Có 5 phiếu ở 5 trạng thái khác nhau.",
     "1. Chọn Trạng thái là Không duyệt\n2. Bấm Tìm kiếm", "Trạng thái: Không duyệt",
     "- Chỉ hiện phiếu Không duyệt\n- Cột Trạng thái của dòng đó hiển thị đúng chữ Không duyệt"),
    (8, "Lọc Trạng thái ở màn Danh sách chờ duyệt", "P0",
     "Có 2 phiếu Chờ duyệt và 1 phiếu Không duyệt.",
     "1. Mở màn Danh sách chờ duyệt\n2. Chọn Trạng thái là Không duyệt\n3. Bấm Tìm kiếm",
     "Trạng thái: Không duyệt",
     "- ⚠️ Hiện phiếu Không duyệt (bộ lọc do người dùng chọn được ưu tiên hơn mặc định Chờ duyệt)"),
    (9, "Lọc theo Người lập trả đúng phiếu", "P0",
     "Nhân viên Nguyễn Văn A lập 2 phiếu, nhân viên Trần Thị B lập 1 phiếu.",
     "1. Bấm ô Người lập, chọn Nguyễn Văn A\n2. Bấm Tìm kiếm", "Người lập: Nguyễn Văn A",
     "- Hiện đúng 2 phiếu của Nguyễn Văn A\n- ⚠️ Không trả về 0 dòng khi trong hệ thống có nhân viên trùng tên"),
    (10, "Danh sách chọn Người lập hiển thị đầy đủ nhân viên", "P1",
     "Hệ thống có nhiều nhân viên; nhân viên Nguyễn Văn A đã lập 3 phiếu.",
     "1. Bấm vào ô Người lập\n2. Gõ Nguyễn Văn A\n3. Quan sát danh sách gợi ý", "—",
     "- ⚠️ Tên Nguyễn Văn A chỉ xuất hiện 1 lần, không lặp lại nhiều dòng giống nhau\n"
     "- Danh sách hiển thị nhân viên như các màn khác của hệ thống"),
    (11, "Lọc theo Người duyệt", "P1",
     "Trưởng phòng Lê Văn C đã duyệt 2 phiếu.",
     "1. Bấm ô Người duyệt, chọn Lê Văn C\n2. Bấm Tìm kiếm", "Người duyệt: Lê Văn C",
     "- Hiện đúng 2 phiếu do Lê Văn C duyệt"),
    (12, "Kết hợp nhiều bộ lọc cùng lúc", "P1",
     "Có 6 phiếu; trong đó chỉ 1 phiếu vừa do Nguyễn Văn A lập, vừa Chờ duyệt, vừa lập trong tháng 8/2026.",
     "1. Chọn Người lập Nguyễn Văn A\n2. Chọn Trạng thái Chờ duyệt\n"
     "3. Nhập Từ ngày 01/08/2026, Đến ngày 31/08/2026\n4. Bấm Tìm kiếm",
     "Người lập: Nguyễn Văn A · Trạng thái: Chờ duyệt · 01/08/2026 - 31/08/2026",
     "- Chỉ hiện đúng 1 phiếu thỏa cả 3 điều kiện"),
    (13, "Lọc không có kết quả", "P2",
     "Không có phiếu nào số YCCG-9999.",
     "1. Nhập YCCG-9999 vào ô Số phiếu YC\n2. Bấm Tìm kiếm", "Số phiếu YC: YCCG-9999",
     "- Bảng hiện thông báo không có dữ liệu\n- Không báo lỗi, không trắng trang"),
    (14, "Bộ lọc Bộ phận ở màn Danh sách chờ duyệt", "P1",
     "Tài khoản lãnh đạo cấp cao có quyền xem theo tổng công ty; hệ thống có nhiều bộ phận.",
     "1. Mở màn Danh sách chờ duyệt\n2. Quan sát các ô lọc\n3. Chọn 1 bộ phận rồi bấm Tìm kiếm", "—",
     "- Có ô lọc Bộ phận\n- Chỉ hiện phiếu của bộ phận đã chọn"),
    (15, "Thứ tự các ô lọc đúng bố cục 3 hàng", "P2",
     "Đang ở màn danh sách phiếu.",
     "1. Quan sát khu vực bộ lọc phía trên bảng", "—",
     "- Các ô lọc xếp theo đúng bố cục quy định, gồm đủ: Số phiếu YC, Từ ngày, Đến ngày, Số HĐ, "
     "KH mới, KH cũ, Trạng thái, Người lập, Người duyệt"),
]

SEC_III = [
    (1, "Sắp xếp theo Ngày lập", "P1",
     "Có 3 phiếu lập lần lượt 05/08/2026, 20/08/2026, 01/09/2026.",
     "1. Mở màn danh sách\n2. Bấm vào tiêu đề cột Ngày lập để sắp tăng dần\n3. Bấm lần nữa để sắp giảm dần", "—",
     "- Lần 1: thứ tự từ 05/08 đến 01/09\n- Lần 2: thứ tự từ 01/09 về 05/08"),
    (2, "Các cột khác không sắp xếp được", "P2",
     "Danh sách có ít nhất 3 phiếu.",
     "1. Bấm vào tiêu đề cột KH mới\n2. Quan sát thứ tự các dòng", "—",
     "- ⚠️ Thứ tự các dòng không đổi (chỉ cột Ngày lập cho phép sắp xếp)"),
    (3, "Phân trang khi nhiều phiếu", "P1",
     "Có 25 phiếu trong phạm vi xem.",
     "1. Mở màn danh sách\n2. Xem thanh phân trang cuối bảng\n3. Chuyển sang trang 2", "—",
     "- Trang 1 hiện đúng số dòng theo cấu hình, còn lại chuyển sang trang 2\n"
     "- Số thứ tự ở cột STT tiếp tục liên tục sang trang 2, không quay lại từ 1"),
    (4, "Giữ bộ lọc khi chuyển trang", "P1",
     "Có 25 phiếu, trong đó 15 phiếu Chờ duyệt.",
     "1. Lọc Trạng thái Chờ duyệt\n2. Chuyển sang trang 2", "Trạng thái: Chờ duyệt",
     "- ⚠️ Trang 2 vẫn chỉ hiện phiếu Chờ duyệt, không hiện lại toàn bộ danh sách"),
]

SEC_IV = [
    (1, "Lập phiếu từ hợp đồng bán hàng và lưu nháp", "P0",
     "Hợp đồng bán hàng HĐ-2026-001 của khách hàng Công ty ABC đã ký. Có khách hàng Công ty XYZ trong danh mục "
     "và tệp tài liệu hợp lệ 2MB.",
     "1. Mở hợp đồng HĐ-2026-001\n2. Chọn chức năng lập phiếu YC chuyển giao khách hàng\n"
     "3. Chọn khách hàng mới là Công ty XYZ\n4. Nhập Lý do thay đổi khách hàng\n"
     "5. Chọn Địa chỉ giao/sửa và Người đại diện\n6. Đính kèm tệp\n7. Bấm Lưu nháp",
     "KH mới: Công ty XYZ · Lý do thay đổi khách hàng: Khách hàng chuyển pháp nhân · Tệp: hopdong.pdf (2MB)",
     "- Hệ thống báo lưu thành công\n- Phiếu xuất hiện trong danh sách ở trạng thái Đang tạo\n"
     "- ⚠️ Phiếu ở trạng thái Đang tạo CHƯA được cấp Số phiếu"),
    (2, "Lập phiếu và Gửi duyệt ngay", "P0",
     "Hợp đồng HĐ-2026-002 của Công ty ABC, chưa có phiếu chuyển giao.",
     "1. Lập phiếu đầy đủ như trường hợp trên\n2. Bấm Lưu & Gửi duyệt",
     "KH mới: Công ty XYZ · Lý do thay đổi khách hàng: Sáp nhập doanh nghiệp · Tệp: quyetdinh.pdf (1MB)",
     "- Báo lưu thành công\n- Phiếu ở trạng thái Chờ duyệt và ĐÃ có Số phiếu\n"
     "- Trong Lịch sử duyệt có dòng Gửi duyệt, cột Nội dung hiển thị đúng Lý do đã nhập"),
    (3, "Lập phiếu từ hợp đồng dịch vụ sửa chữa", "P0",
     "Hợp đồng dịch vụ sửa chữa DV-2026-001 của khách hàng Công ty ABC.",
     "1. Mở hợp đồng dịch vụ DV-2026-001\n2. Lập phiếu YC chuyển giao khách hàng\n"
     "3. Nhập đủ thông tin bắt buộc\n4. Bấm Lưu & Gửi duyệt",
     "KH mới: Công ty XYZ · Lý do thay đổi khách hàng: Đổi đơn vị tiếp nhận",
     "- Lưu thành công, phiếu Chờ duyệt\n- Cột Số HĐ ở danh sách hiển thị đúng số hợp đồng dịch vụ"),
    (4, "Thông tin khách hàng cũ được chụp lại đúng", "P0",
     "Hợp đồng HĐ-2026-001 của Công ty ABC, mã số thuế 0100123456, địa chỉ 12 Lê Lợi, "
     "trên hợp đồng có 1 tệp đính kèm.",
     "1. Lập phiếu chuyển giao từ hợp đồng này\n2. Quan sát khối Thông tin khách hàng cũ", "—",
     "- Tên, mã số thuế, địa chỉ hiển thị đúng như trên hợp đồng\n"
     "- ⚠️ Mục Tệp đính kèm của khách hàng cũ hiển thị đúng tệp đang có trên hợp đồng, "
     "KHÔNG hiển thị dòng Chưa có tệp"),
    (5, "Chọn khách hàng mới thì tự điền thông tin", "P0",
     "Khách hàng Công ty XYZ đã có đủ mã số thuế, địa chỉ, số căn cước người đại diện, ngày cấp, nơi cấp, "
     "tài khoản ngân hàng và 3 hãng xe.",
     "1. Ở màn lập phiếu, bấm nút tìm khách hàng mới\n2. Chọn Công ty XYZ\n3. Quan sát khối khách hàng mới", "—",
     "- Tên, mã số thuế, địa chỉ tự điền đúng\n- Số căn cước, Ngày cấp, Nơi cấp tự điền\n"
     "- ⚠️ Ô Ngày cấp và Nơi cấp KHÔNG cho gõ tay, chỉ nhận giá trị tự điền\n"
     "- ⚠️ Ô Hãng xe hiển thị đủ cả 3 hãng của khách hàng, không phải chỉ 1 hãng"),
    (6, "Danh sách tài khoản ngân hàng lấy theo khách hàng đã chọn", "P0",
     "Công ty XYZ có 2 tài khoản: Vietcombank chi nhánh Nghệ An và BIDV chi nhánh Hà Nội.",
     "1. Chọn khách hàng mới là Công ty XYZ\n2. Bấm vào ô chọn tài khoản ngân hàng\n3. Chọn tài khoản Vietcombank",
     "—",
     "- Danh sách hiện đúng 2 tài khoản của Công ty XYZ\n"
     "- Sau khi chọn, ô Ngân hàng, Chi nhánh và Tỉnh/Thành phố tự điền đúng theo tài khoản đã chọn"),
    (7, "Tìm khách hàng mới sắp xếp mới nhất lên đầu", "P1",
     "Vừa tạo mới khách hàng Công ty MỚI NHẤT trong ngày hôm nay.",
     "1. Ở màn lập phiếu, bấm nút tìm khách hàng mới\n2. Không nhập từ khóa, quan sát danh sách", "—",
     "- ⚠️ Công ty MỚI NHẤT nằm ở những dòng đầu tiên (danh sách ưu tiên khách hàng mới nhất)"),
    (8, "Tab Cá nhân trong cửa sổ tìm khách hàng hiện dữ liệu sẵn", "P1",
     "Trong hệ thống có ít nhất 5 khách hàng cá nhân.",
     "1. Bấm nút tìm khách hàng mới\n2. Chuyển sang tab Cá nhân\n3. Không nhập số điện thoại", "—",
     "- ⚠️ Danh sách khách hàng cá nhân hiện ngay, không bắt buộc phải nhập số điện thoại mới ra kết quả"),
    (9, "Bộ lọc Tỉnh/Thành phố trong cửa sổ tìm khách hàng", "P1",
     "Cửa sổ tìm khách hàng đang mở, hệ thống có khách hàng ở nhiều tỉnh thành.",
     "1. Bấm nút tìm khách hàng mới\n2. Bấm vào ô lọc Tỉnh/Thành phố\n3. Chọn Hà Nội rồi bấm Tìm", "Tỉnh/Thành phố: Hà Nội",
     "- ⚠️ Ô lọc Tỉnh/Thành phố có đầy đủ danh sách tỉnh thành để chọn, không để trống\n"
     "- Kết quả chỉ còn khách hàng ở Hà Nội"),
    (10, "Thêm nhanh khách hàng ngay trong cửa sổ tìm kiếm", "P0",
     "Chưa có khách hàng tên Công ty THÊM NHANH trong danh mục.",
     "1. Bấm nút tìm khách hàng mới\n2. Bấm nút Thêm khách hàng\n3. Nhập tên, chọn Loại hình tổ chức, "
     "nhập mã số thuế, địa chỉ, người đại diện\n4. Bấm Lưu",
     "Khách hàng: Công ty THÊM NHANH · Loại hình tổ chức: Doanh nghiệp tư nhân",
     "- Lưu thành công, cửa sổ đóng lại\n- Khách hàng vừa tạo được chọn vào phiếu\n"
     "- ⚠️ Các ô Số căn cước, Ngày cấp, Địa chỉ của khách hàng vừa tạo được tự điền sang phiếu, không để trống"),
    (11, "Thêm nhanh khách hàng có nhập ngày theo dạng ngày/tháng/năm", "P0",
     "Cửa sổ Thêm khách hàng đang mở.",
     "1. Nhập đủ thông tin bắt buộc\n2. Ở ô Ngày cấp nhập 28/08/2026\n3. Ở ô Sinh nhật nhập 15/03/1990\n4. Bấm Lưu",
     "Ngày cấp: 28/08/2026 · Sinh nhật: 15/03/1990",
     "- ⚠️ Lưu thành công, KHÔNG báo lỗi ngày sinh nhật không hợp lệ\n"
     "- Mở lại khách hàng vừa tạo thấy Ngày cấp đúng 28/08/2026 và Sinh nhật đúng 15/03/1990"),
    (12, "Cuộn nội dung cửa sổ Thêm khách hàng sau khi đổi Loại hình tổ chức", "P0",
     "Cửa sổ Thêm khách hàng đang mở, màn hình máy tính độ phân giải thông thường.",
     "1. Cuộn nội dung xuống khoảng giữa biểu mẫu\n2. Đổi Loại hình tổ chức sang một giá trị khác\n"
     "3. Đổi thêm 1-2 lần nữa\n4. Cuộn tiếp lên xuống",
     "Loại hình tổ chức: lần lượt Cá nhân, Doanh nghiệp tư nhân, Cơ quan nhà nước",
     "- ⚠️ Nội dung cuộn được bình thường sau mỗi lần đổi\n"
     "- ⚠️ Nội dung KHÔNG tự nhảy về đầu biểu mẫu và KHÔNG bị kẹt ở giữa\n"
     "- Tiêu đề Thêm khách hàng luôn nhìn thấy ở trên, nút Lưu và Hủy luôn nhìn thấy ở đáy"),
    (13, "Thêm nhanh người liên hệ trong phiếu", "P0",
     "Khách hàng Công ty XYZ đã được chọn, chưa có người liên hệ tên Nguyễn Thị D.",
     "1. Bấm nút tìm người liên hệ\n2. Bấm Thêm mới\n3. Nhập Họ tên, Chức vụ, Số điện thoại\n"
     "4. Chọn Tỉnh/Thành phố\n5. Bấm Lưu",
     "Họ tên: Nguyễn Thị D · Chức vụ: Kế toán trưởng · Số điện thoại: 0912345678 · Tỉnh/Thành phố: Hà Nội",
     "- Lưu thành công, người liên hệ vừa tạo được chọn vào phiếu\n"
     "- ⚠️ Danh sách Tỉnh/Thành phố có dữ liệu để chọn, không để trống"),
    (14, "Biểu mẫu thêm người liên hệ đủ thông tin cần thiết", "P1",
     "Cửa sổ Thêm mới người liên hệ đang mở.",
     "1. Quan sát các ô nhập trong biểu mẫu", "—",
     "- Có đủ các ô: Họ tên, Chức vụ, Số điện thoại, Email, Sinh nhật, Số tài khoản, Chủ tài khoản, "
     "Ngân hàng, Tỉnh/Thành phố, Chi nhánh\n- Bố cục rộng rãi, chữ không bị chen chúc"),
    (15, "Nhập sinh nhật hợp lệ cho người liên hệ", "P0",
     "Cửa sổ Thêm mới người liên hệ đang mở, đã nhập Họ tên, Chức vụ, Số điện thoại.",
     "1. Nhập Sinh nhật là 15/03/1990\n2. Bấm Lưu", "Sinh nhật: 15/03/1990",
     "- ⚠️ Lưu thành công, KHÔNG báo sinh nhật không hợp lệ\n- Người liên hệ được tạo và chọn vào phiếu"),
    (16, "Sửa phiếu ở trạng thái Đang tạo", "P0",
     "Phiếu YCCG-0002 do chính người đăng nhập lập, đang ở trạng thái Đang tạo, đã có 1 tệp đính kèm.",
     "1. Ở danh sách, bấm nút Sửa (biểu tượng bút chì) dòng phiếu YCCG-0002\n"
     "2. Sửa Lý do thay đổi khách hàng\n3. Bấm Lưu nháp",
     "Lý do thay đổi khách hàng: Cập nhật lý do lần 2",
     "- Lưu thành công\n- ⚠️ Không bắt buộc chọn lại tệp đính kèm, tệp cũ vẫn còn nguyên"),
    (17, "Sửa phiếu ở trạng thái Không duyệt", "P0",
     "Phiếu YCCG-0004 do chính người đăng nhập lập, đã bị Không duyệt.",
     "1. Ở danh sách tìm phiếu YCCG-0004\n2. Bấm nút Sửa\n3. Sửa lại lý do\n4. Bấm Lưu & Gửi duyệt",
     "Lý do thay đổi khách hàng: Bổ sung hồ sơ theo yêu cầu",
     "- ⚠️ Phiếu Không duyệt VẪN cho phép Sửa\n- Sau khi gửi lại, phiếu chuyển sang Chờ duyệt"),
    (18, "Không thấy nút Sửa ở phiếu Chờ duyệt", "P0",
     "Phiếu YCCG-0001 do chính người đăng nhập lập, đang Chờ duyệt.",
     "1. Ở danh sách, quan sát cột Hành động dòng phiếu YCCG-0001", "—",
     "- ⚠️ Không có nút Sửa và không có nút Xóa\n- Chỉ có nút Xem"),
    (19, "Người khác không thấy nút Sửa phiếu của mình", "P0",
     "Phiếu YCCG-0002 do tài khoản H lập, trạng thái Đang tạo. Đăng nhập bằng tài khoản I.",
     "1. Đăng nhập tài khoản I\n2. Mở danh sách, tìm phiếu YCCG-0002\n3. Quan sát cột Hành động", "—",
     "- Không có nút Sửa, không có nút Xóa"),
    (20, "Khách hàng cá nhân thì người liên hệ chính là khách hàng đó", "P1",
     "Khách hàng mới là ông Nguyễn Văn E (khách hàng cá nhân), số điện thoại 0987654321.",
     "1. Lập phiếu, chọn khách hàng mới là Nguyễn Văn E\n2. Quan sát khối thông tin người liên hệ", "—",
     "- Thông tin người liên hệ lấy chính theo Nguyễn Văn E, không bắt chọn người đại diện khác"),
]

SEC_V = [
    (1, "Duyệt phiếu Chờ duyệt", "P0",
     "Phiếu YCCG-0001 đang Chờ duyệt, chuyển hợp đồng HĐ-2026-001 từ Công ty ABC sang Công ty XYZ. "
     "Tài khoản đăng nhập có quyền Duyệt phiếu YC chuyển giao khách hàng.",
     "1. Mở chi tiết phiếu YCCG-0001\n2. Bấm nút Duyệt\n3. Xác nhận trên hộp thoại", "—",
     "- Báo duyệt thành công\n- Trạng thái phiếu chuyển sang Đã duyệt\n"
     "- Cột Người duyệt và Ngày duyệt được điền\n"
     "- ⚠️ Mở hợp đồng HĐ-2026-001 thấy khách hàng đã đổi thành Công ty XYZ"),
    (2, "Duyệt xong người lập nhận được thông báo", "P0",
     "Phiếu YCCG-0001 do nhân viên Nguyễn Văn A lập, đang Chờ duyệt. Trưởng phòng Lê Văn C có quyền duyệt.",
     "1. Đăng nhập Lê Văn C, duyệt phiếu YCCG-0001\n2. Đăng nhập lại bằng Nguyễn Văn A\n"
     "3. Mở phần thông báo (biểu tượng chuông)", "—",
     "- ⚠️ Nguyễn Văn A nhận được 1 thông báo báo phiếu chuyển giao khách hàng của mình đã được duyệt\n"
     "- Bấm vào thông báo mở đúng phiếu YCCG-0001"),
    (3, "Không duyệt phiếu kèm lý do", "P0",
     "Phiếu YCCG-0001 đang Chờ duyệt, người đăng nhập có quyền duyệt.",
     "1. Mở chi tiết phiếu\n2. Bấm nút Không duyệt\n3. Nhập lý do vào cửa sổ Không duyệt phiếu\n4. Xác nhận",
     "Lý do không duyệt: Thiếu văn bản xác nhận của khách hàng cũ",
     "- Trạng thái chuyển sang Không duyệt\n"
     "- Lịch sử duyệt có dòng không duyệt, cột Nội dung hiển thị đúng lý do vừa nhập\n"
     "- ⚠️ Thông tin khách hàng trên hợp đồng KHÔNG bị thay đổi"),
    (4, "Không duyệt nhưng bỏ trống lý do", "P1",
     "Phiếu YCCG-0001 đang Chờ duyệt.",
     "1. Bấm nút Không duyệt\n2. Để trống ô lý do\n3. Bấm xác nhận", "Lý do không duyệt: để trống",
     "- Hệ thống báo lỗi yêu cầu nhập lý do, hoặc ghi nhận rõ ràng nếu cho phép để trống\n"
     "- Cửa sổ không tự đóng khi còn lỗi"),
    (5, "Phiếu Đã duyệt không còn nút thao tác duyệt", "P0",
     "Phiếu YCCG-0003 đã ở trạng thái Đã duyệt.",
     "1. Mở chi tiết phiếu YCCG-0003\n2. Quan sát cuối màn", "—",
     "- ⚠️ Không còn nút Duyệt và Không duyệt\n- ⚠️ Không hiện nút Hủy duyệt trên giao diện\n- Chỉ còn nút Quay lại"),
    (6, "Lịch sử duyệt hiển thị đúng thứ tự cột", "P1",
     "Phiếu YCCG-0004 đã trải qua: gửi duyệt, không duyệt, gửi duyệt lại, duyệt.",
     "1. Mở chi tiết phiếu YCCG-0004\n2. Xem bảng Lịch sử duyệt", "—",
     "- Các cột theo thứ tự Tài khoản, Nội dung, Hành động, Thời gian\n"
     "- ⚠️ Không có cột số thứ tự\n- Chữ đầu của Hành động được viết hoa\n- Đủ 4 dòng theo đúng thứ tự thời gian"),
    (7, "Nội dung dòng Gửi duyệt hiển thị lý do", "P0",
     "Phiếu YCCG-0001 được gửi duyệt với lý do Khách hàng chuyển pháp nhân.",
     "1. Mở chi tiết phiếu\n2. Xem dòng Gửi duyệt trong Lịch sử duyệt", "—",
     "- ⚠️ Cột Nội dung của dòng Gửi duyệt hiển thị đúng chữ Khách hàng chuyển pháp nhân, không để trống"),
    (8, "Duyệt hai lần liên tiếp trên hai cửa sổ", "P1",
     "Phiếu YCCG-0001 đang Chờ duyệt, mở cùng lúc trên 2 cửa sổ trình duyệt của cùng người duyệt.",
     "1. Ở cửa sổ 1 bấm Duyệt và xác nhận\n2. Chuyển sang cửa sổ 2 (vẫn đang mở phiếu cũ) bấm Duyệt",
     "—",
     "- ⚠️ Lần duyệt thứ hai bị từ chối vì phiếu không còn ở trạng thái Chờ duyệt\n"
     "- Lịch sử duyệt chỉ có 1 dòng duyệt, không nhân đôi\n- Không treo trang"),
]

SEC_VI = [
    (1, "Xóa phiếu ở trạng thái Đang tạo", "P0",
     "Phiếu YCCG-0002 do chính người đăng nhập lập, trạng thái Đang tạo.",
     "1. Ở danh sách, bấm nút Xóa (biểu tượng thùng rác) dòng phiếu YCCG-0002\n"
     "2. Đọc nội dung hộp thoại xác nhận\n3. Bấm Đồng ý", "—",
     "- Hộp thoại hỏi xác nhận trước khi xóa\n- Sau khi đồng ý, báo xóa phiếu thành công\n"
     "- Phiếu biến mất khỏi danh sách"),
    (2, "Hủy thao tác xóa", "P1",
     "Phiếu YCCG-0002 trạng thái Đang tạo.",
     "1. Bấm nút Xóa\n2. Ở hộp thoại xác nhận bấm Hủy", "—",
     "- Phiếu vẫn còn nguyên trong danh sách\n- Không có thông báo xóa thành công"),
    (3, "Xóa phiếu ở trạng thái Không duyệt", "P0",
     "Phiếu YCCG-0004 do chính người đăng nhập lập, trạng thái Không duyệt.",
     "1. Tìm phiếu YCCG-0004 ở danh sách\n2. Quan sát cột Hành động\n3. Bấm nút Xóa và xác nhận", "—",
     "- ⚠️ Phiếu Không duyệt CÓ nút Xóa\n- Xóa thành công, phiếu biến mất khỏi danh sách"),
    (4, "Không xóa được phiếu Đã duyệt", "P0",
     "Phiếu YCCG-0003 ở trạng thái Đã duyệt.",
     "1. Tìm phiếu YCCG-0003\n2. Quan sát cột Hành động", "—",
     "- ⚠️ Không có nút Xóa ở phiếu Đã duyệt"),
    (5, "Phiếu Đang tạo có đủ 3 nút thao tác", "P1",
     "Phiếu YCCG-0002 do chính người đăng nhập lập, trạng thái Đang tạo.",
     "1. Quan sát cột Hành động dòng phiếu YCCG-0002", "—",
     "- Có đủ nút Xem, Sửa và Xóa"),
]

SEC_VII = [
    (1, "Xuất Excel danh sách phiếu", "P1",
     "Danh sách đang có 5 phiếu ở nhiều trạng thái.",
     "1. Mở màn danh sách\n2. Bấm nút Xuất Excel\n3. Mở tệp vừa tải về", "—",
     "- Tệp tải về mở được, không báo hỏng\n- Các cột trùng khớp với bảng trên màn hình\n"
     "- Số dòng bằng đúng số phiếu đang hiển thị"),
    (2, "Xuất Excel sau khi lọc", "P1",
     "Có 5 phiếu, sau khi lọc Trạng thái Chờ duyệt còn 2 phiếu.",
     "1. Lọc Trạng thái Chờ duyệt\n2. Bấm Xuất Excel\n3. Mở tệp", "Trạng thái: Chờ duyệt",
     "- ⚠️ Tệp chỉ chứa 2 phiếu Chờ duyệt, không xuất toàn bộ danh sách"),
]

SEC_VIII = [
    (1, "Không chọn khách hàng mới", "P0",
     "Đang ở màn lập phiếu, đã chọn hợp đồng.",
     "1. Bỏ trống khách hàng mới\n2. Nhập các thông tin khác\n3. Bấm Lưu & Gửi duyệt", "KH mới: để trống",
     "- Hệ thống báo lỗi Vui lòng chọn khách hàng mới\n- Phiếu không được lưu, dữ liệu đã nhập vẫn còn trên màn"),
    (2, "Không nhập lý do thay đổi khách hàng", "P0",
     "Đang ở màn lập phiếu, đã chọn hợp đồng và khách hàng mới.",
     "1. Bỏ trống ô Lý do thay đổi khách hàng\n2. Bấm Lưu & Gửi duyệt", "Lý do thay đổi khách hàng: để trống",
     "- Hệ thống báo lỗi Vui lòng nhập lý do thay đổi khách hàng\n- Phiếu không được lưu"),
    (3, "Không chọn Địa chỉ giao/sửa", "P0",
     "Đang ở màn lập phiếu, đã chọn khách hàng mới.",
     "1. Bỏ trống ô Địa chỉ giao/sửa\n2. Bấm Lưu & Gửi duyệt", "Địa chỉ giao/sửa: để trống",
     "- Hệ thống báo lỗi Địa chỉ giao/sửa là bắt buộc"),
    (4, "Khách hàng doanh nghiệp bắt buộc Người đại diện", "P0",
     "Khách hàng mới là Công ty XYZ (loại hình doanh nghiệp).",
     "1. Chọn khách hàng mới là Công ty XYZ\n2. Bỏ trống Người đại diện\n3. Bấm Lưu & Gửi duyệt",
     "Người đại diện: để trống",
     "- Hệ thống báo lỗi Người đại diện là bắt buộc đối với khách hàng doanh nghiệp"),
    (5, "Khách hàng cá nhân không bắt buộc Người đại diện", "P0",
     "Khách hàng mới là ông Nguyễn Văn E (khách hàng cá nhân).",
     "1. Chọn khách hàng mới là Nguyễn Văn E\n2. Để trống Người đại diện\n"
     "3. Nhập đủ các trường bắt buộc còn lại\n4. Bấm Lưu & Gửi duyệt",
     "KH mới: Nguyễn Văn E (cá nhân) · Người đại diện: để trống",
     "- ⚠️ Lưu thành công, KHÔNG báo lỗi thiếu Người đại diện"),
    (6, "Tạo mới không đính kèm tệp", "P0",
     "Đang lập phiếu mới, đã nhập đủ thông tin khác.",
     "1. Không chọn tệp nào\n2. Bấm Lưu & Gửi duyệt", "Tệp đính kèm: không chọn",
     "- Hệ thống báo lỗi Bắt buộc đính kèm ít nhất 1 tệp\n- Phiếu không được lưu"),
    (7, "Đính kèm tệp vượt quá dung lượng cho phép", "P0",
     "Có sẵn tệp dung lượng 70MB.",
     "1. Ở màn lập phiếu, chọn tệp 70MB\n2. Quan sát màn hình", "Tệp: tailieu-70mb.pdf",
     "- Hệ thống báo lỗi ngay dưới ô Tệp đính kèm, ghi rõ tệp vượt quá 60MB\n"
     "- ⚠️ Màn hình KHÔNG bị quay vòng chờ mãi, không gửi phiếu đi"),
    (8, "Đính kèm tệp dung lượng trong khoảng 50MB đến 60MB", "P0",
     "Có sẵn tệp dung lượng 55MB. Trên màn ghi chú tối đa 60 MB.",
     "1. Chọn tệp 55MB\n2. Nhập đủ thông tin bắt buộc\n3. Bấm Lưu & Gửi duyệt", "Tệp: tailieu-55mb.pdf",
     "- ⚠️ Tệp 55MB PHẢI lưu thành công (giới hạn 60MB áp dụng thống nhất cả hai phía)\n"
     "- ⚠️ KHÔNG được báo lỗi tệp vượt quá 50MB — nếu còn báo như vậy nghĩa là bản đang test chưa "
     "cập nhật phần sửa ngày 03/09/2026, đánh Failed và ghi chú lại\n"
     "- Mở lại chi tiết phiếu thấy tệp 55MB đã đính kèm và tải về được"),
    (9, "Đính kèm tệp ngay sát mốc giới hạn", "P1",
     "Có sẵn 2 tệp: một tệp 59MB và một tệp 61MB.",
     "1. Chọn tệp 59MB, nhập đủ thông tin bắt buộc, bấm Lưu & Gửi duyệt\n"
     "2. Lập phiếu khác, chọn tệp 61MB, bấm Lưu & Gửi duyệt",
     "Tệp: tailieu-59mb.pdf và tailieu-61mb.pdf",
     "- ⚠️ Tệp 59MB lưu thành công\n"
     "- ⚠️ Tệp 61MB bị chặn ngay trên màn hình, báo vượt quá 60MB, phiếu không được gửi đi"),
    (10, "Ghi chú dung lượng trên màn hình", "P2",
     "Đang ở màn lập phiếu.",
     "1. Quan sát dòng chú thích cạnh ô Tệp đính kèm", "—",
     "- Dòng chú thích ghi tối đa 60 MB"),
    (11, "Đính kèm nhiều tệp cùng lúc", "P1",
     "Có 3 tệp hợp lệ, mỗi tệp khoảng 1MB.",
     "1. Đính kèm lần lượt 3 tệp\n2. Bấm Lưu & Gửi duyệt", "Tệp: a.pdf, b.pdf, c.jpg",
     "- Lưu thành công\n- Mở lại chi tiết phiếu thấy đủ 3 tệp, bấm vào tải về được"),
    (12, "Xóa bớt tệp khi sửa phiếu", "P1",
     "Phiếu YCCG-0002 trạng thái Đang tạo, đang có 2 tệp đính kèm.",
     "1. Bấm Sửa phiếu YCCG-0002\n2. Xóa 1 tệp\n3. Bấm Lưu nháp\n4. Mở lại chi tiết phiếu", "—",
     "- Sau khi lưu chỉ còn 1 tệp\n- Tệp còn lại vẫn tải về được"),
    (13, "Nhập lý do quá dài", "P2",
     "Đang ở màn lập phiếu.",
     "1. Nhập vào ô Lý do thay đổi khách hàng khoảng 1000 ký tự\n2. Bấm Lưu nháp",
     "Lý do thay đổi khách hàng: chuỗi 1000 ký tự",
     "- Lưu thành công hoặc báo lỗi rõ ràng về độ dài\n- Không trắng trang, không mất dữ liệu đã nhập"),
    (14, "Không chọn hợp đồng", "P1",
     "Vào thẳng màn lập phiếu mà không đi từ hợp đồng.",
     "1. Bỏ trống thông tin hợp đồng\n2. Bấm Lưu & Gửi duyệt", "Hợp đồng: để trống",
     "- Hệ thống báo lỗi Vui lòng chọn hợp đồng\n- Phiếu không được lưu"),
    (15, "Chọn tệp không phải tài liệu thông thường", "P2",
     "Có sẵn tệp thuchi.exe.",
     "1. Chọn tệp thuchi.exe làm tệp đính kèm\n2. Bấm Lưu & Gửi duyệt", "Tệp: thuchi.exe",
     "- Hệ thống báo lỗi tệp không hợp lệ, hoặc chấp nhận nhưng ghi nhận rõ ràng\n- Không trắng trang"),
]

SEC_IX = [
    (1, "Hai người cùng lập phiếu cho một hợp đồng", "P1",
     "Hợp đồng HĐ-2026-001 chưa có phiếu chuyển giao. Hai nhân viên cùng mở màn lập phiếu cho hợp đồng này.",
     "1. Nhân viên 1 lập phiếu và Gửi duyệt\n2. Nhân viên 2 (đang mở màn từ trước) cũng bấm Lưu & Gửi duyệt",
     "—",
     "- Hệ thống xử lý rõ ràng: hoặc chặn phiếu thứ hai kèm thông báo dễ hiểu, hoặc cho phép và "
     "hiển thị đủ 2 phiếu\n- ⚠️ Không được treo trang hoặc báo lỗi khó hiểu"),
    (2, "Duyệt phiếu trong khi người lập đang sửa", "P1",
     "Phiếu YCCG-0001 Chờ duyệt. Người lập đang mở màn sửa từ trước khi phiếu chuyển Chờ duyệt.",
     "1. Người duyệt bấm Duyệt phiếu\n2. Người lập bấm Lưu ở màn sửa đang mở", "—",
     "- ⚠️ Thao tác lưu bị từ chối vì phiếu đã được duyệt\n- Nội dung phiếu đã duyệt không bị ghi đè"),
    (3, "Xóa phiếu ở cửa sổ khác rồi mở lại chi tiết", "P2",
     "Phiếu YCCG-0002 đang mở ở 2 cửa sổ.",
     "1. Ở cửa sổ 1 xóa phiếu YCCG-0002\n2. Ở cửa sổ 2 bấm nút Xem lại phiếu đó", "—",
     "- Hệ thống báo dữ liệu đã thay đổi hoặc không tìm thấy phiếu\n- Không treo trang, không trắng trang"),
    (4, "Khách hàng bị khóa vẫn hiển thị trên phiếu đã lập", "P1",
     "Phiếu YCCG-0001 đã chọn khách hàng mới là Công ty XYZ; sau đó Công ty XYZ bị khóa trong danh mục.",
     "1. Khóa khách hàng Công ty XYZ trong danh mục\n2. Mở lại chi tiết phiếu YCCG-0001", "—",
     "- ⚠️ Ô khách hàng mới vẫn hiển thị đúng tên Công ty XYZ, không bị trống\n"
     "- Tên hiển thị nguyên vẹn, không bị thêm chữ đã khóa vào sau tên"),
    (5, "Hợp đồng bị sửa khách hàng sau khi phiếu đã lập", "P2",
     "Phiếu YCCG-0001 đang Chờ duyệt, chụp thông tin khách hàng cũ là Công ty ABC. "
     "Sau đó hợp đồng được sửa đổi thông tin khách hàng.",
     "1. Sửa thông tin khách hàng trên hợp đồng\n2. Mở lại chi tiết phiếu YCCG-0001\n"
     "3. Xem khối Thông tin khách hàng cũ", "—",
     "- ⚠️ Khối khách hàng cũ vẫn giữ nguyên thông tin đã chụp lúc lập phiếu, phục vụ đối chiếu"),
]

SEC_X = [
    (1, "Luồng đầy đủ: lập, gửi duyệt, không duyệt, sửa, gửi lại, duyệt", "P0",
     "Hợp đồng HĐ-2026-010 của Công ty ABC. Nhân viên Nguyễn Văn A lập phiếu. "
     "Trưởng phòng Lê Văn C có quyền duyệt. Khách hàng mới Công ty XYZ.",
     "1. Nguyễn Văn A lập phiếu, đính kèm tệp, bấm Lưu & Gửi duyệt\n"
     "2. Lê Văn C mở phiếu, bấm Không duyệt, nhập lý do Thiếu hồ sơ\n"
     "3. Nguyễn Văn A mở lại phiếu, bấm Sửa, bổ sung tệp, bấm Lưu & Gửi duyệt\n"
     "4. Lê Văn C mở phiếu, bấm Duyệt\n5. Mở lại hợp đồng HĐ-2026-010",
     "KH mới: Công ty XYZ · Lý do thay đổi khách hàng: Khách hàng chuyển pháp nhân · "
     "Lý do không duyệt: Thiếu hồ sơ",
     "- Sau bước 1: trạng thái Chờ duyệt, có Số phiếu\n- Sau bước 2: trạng thái Không duyệt\n"
     "- Sau bước 3: trạng thái Chờ duyệt trở lại\n- Sau bước 4: trạng thái Đã duyệt, có Người duyệt và Ngày duyệt\n"
     "- ⚠️ Sau bước 5: hợp đồng đã đổi sang khách hàng Công ty XYZ\n"
     "- Lịch sử duyệt có đủ 4 dòng đúng thứ tự và đúng nội dung lý do"),
    (2, "Luồng lưu nháp rồi mới gửi duyệt sau", "P0",
     "Hợp đồng HĐ-2026-011 của Công ty ABC.",
     "1. Lập phiếu, bấm Lưu nháp\n2. Kiểm tra danh sách\n3. Mở lại phiếu, bấm Sửa\n4. Bấm Lưu & Gửi duyệt\n"
     "5. Kiểm tra lại danh sách", "KH mới: Công ty XYZ",
     "- Sau bước 1: phiếu ở trạng thái Đang tạo, ⚠️ chưa có Số phiếu\n"
     "- Sau bước 4: phiếu chuyển Chờ duyệt và ⚠️ được cấp Số phiếu\n"
     "- Nút Sửa và Xóa biến mất sau khi phiếu sang Chờ duyệt"),
    (3, "Luồng chuyển giao trên hợp đồng dịch vụ sửa chữa", "P1",
     "Hợp đồng dịch vụ DV-2026-005 của Công ty ABC, khách hàng mới là Công ty XYZ.",
     "1. Lập phiếu từ hợp đồng dịch vụ, gửi duyệt\n2. Người có quyền duyệt bấm Duyệt\n"
     "3. Mở lại hợp đồng dịch vụ DV-2026-005", "KH mới: Công ty XYZ",
     "- Phiếu chuyển sang Đã duyệt\n- ⚠️ Hợp đồng dịch vụ đã đổi sang khách hàng Công ty XYZ"),
    (4, "Luồng tạo khách hàng mới ngay trong khi lập phiếu rồi duyệt", "P0",
     "Hợp đồng HĐ-2026-012 của Công ty ABC. Khách hàng Công ty HOÀN TOÀN MỚI chưa có trong danh mục.",
     "1. Lập phiếu, bấm tìm khách hàng mới, bấm Thêm khách hàng\n"
     "2. Nhập tên, loại hình, mã số thuế, địa chỉ, ngày cấp dạng ngày/tháng/năm, bấm Lưu\n"
     "3. Kiểm tra thông tin tự điền vào phiếu\n4. Nhập lý do, đính kèm tệp, bấm Lưu & Gửi duyệt\n"
     "5. Người có quyền duyệt bấm Duyệt\n6. Mở lại hợp đồng",
     "Khách hàng: Công ty HOÀN TOÀN MỚI · Ngày cấp: 28/08/2026",
     "- Bước 2: tạo khách hàng thành công, không báo lỗi ngày\n"
     "- ⚠️ Bước 3: các ô Số căn cước, Ngày cấp, Địa chỉ được tự điền sang phiếu, không để trống\n"
     "- Bước 5: phiếu Đã duyệt\n- Bước 6: hợp đồng đã đổi sang Công ty HOÀN TOÀN MỚI"),
    (5, "Luồng lập phiếu cho khách hàng cá nhân", "P1",
     "Hợp đồng HĐ-2026-013 của Công ty ABC, chuyển sang khách hàng cá nhân Nguyễn Văn E.",
     "1. Lập phiếu, chọn khách hàng mới là cá nhân Nguyễn Văn E\n2. Để trống Người đại diện\n"
     "3. Nhập lý do, đính kèm tệp, bấm Lưu & Gửi duyệt\n4. Người có quyền duyệt bấm Duyệt\n"
     "5. Mở lại hợp đồng", "KH mới: Nguyễn Văn E (cá nhân)",
     "- Bước 3: lưu thành công dù để trống Người đại diện\n- Bước 4: phiếu Đã duyệt\n"
     "- Bước 5: hợp đồng đã đổi sang Nguyễn Văn E"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "LẬP PHIẾU / SỬA PHIẾU", SEC_IV),
    ("V", "DUYỆT / KHÔNG DUYỆT", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "XUẤT EXCEL", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ TỔNG THỂ", SEC_X),
]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase.xlsx")

build(output_file=OUT, sheet_name="Trang tính1",
      feature_name="Phiếu YC chuyển giao khách hàng",
      module_name=M,
      description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
