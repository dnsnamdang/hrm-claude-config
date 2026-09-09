# -*- coding: utf-8 -*-
"""Sinh file testcase Excel cho man PHIEU BAO CO + TONG HOP TIEN VE NGAN HANG.

Chay:  python .plans/gop-db/finance-bill-income-report/gen_testcase.py
Output: .plans/gop-db/finance-bill-income-report/testcase.xlsx
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

OUT = os.path.join(HERE, "testcase.xlsx")
MODULE = "Phiếu báo có"

# =============================================================== 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu báo có là chứng từ ghi nhận tiền về tài khoản ngân hàng của công ty theo sao kê. "
     "Mỗi phiếu gồm thông tin chung (loại thu, tài khoản nợ, loại tiền, tỷ giá, ngày hạch toán, "
     "ngân hàng, tài khoản) và các dòng chi tiết gắn số tiền với khách hàng / nhà cung cấp / "
     "hợp đồng.\n"
     "Khi phiếu được duyệt, hệ thống ghi bút toán tương ứng vào sổ kế toán — đây là số liệu kế "
     "toán thật, không hoàn tác được.\n"
     "Màn phụ Tổng hợp tiền về ngân hàng liệt kê từng dòng chi tiết của phiếu đã duyệt để kế "
     "toán đối chiếu công nợ và chuyển sang phiếu yêu cầu điều chỉnh công nợ."),

    ("2. Đối tượng được tính / hiển thị",
     "Màn Danh sách phiếu báo có hiển thị:\n"
     "- Phiếu ở trạng thái Đã duyệt nằm trong phạm vi dữ liệu của người đăng nhập.\n"
     "- Phiếu ở trạng thái Đang tạo DO CHÍNH người đăng nhập lập.\n"
     "Màn Tổng hợp tiền về ngân hàng hiển thị dòng chi tiết thỏa ĐỒNG THỜI 4 điều kiện:\n"
     "- Phiếu cha ở trạng thái Đã duyệt.\n"
     "- Số tài khoản có của dòng thuộc nhóm tài khoản công nợ 1311, 1312, 3311.\n"
     "- Dòng chưa được đánh dấu Không báo tiền về.\n"
     "- Phiếu thuộc công ty của người đăng nhập."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu Đang tạo do NGƯỜI KHÁC lập: ẩn với tất cả mọi người, kể cả người có quyền xem tất "
     "cả phiếu báo có của tổng công ty.\n"
     "- Phiếu của công ty khác: ẩn với người chỉ có quyền xem tất cả phiếu báo có của công ty.\n"
     "- Mọi phiếu không do mình lập: ẩn với người không có quyền xem theo cấp nào.\n"
     "- Ở màn Tổng hợp: dòng của phiếu Đang tạo, dòng có tài khoản có ngoài nhóm 1311/1312/3311, "
     "dòng đã đánh dấu Không báo tiền về, dòng thuộc phiếu của công ty khác.\n"
     "- Người dùng không xác định được công ty: màn Tổng hợp không hiển thị dòng nào."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Màn Danh sách có 2 khoảng ngày độc lập:\n"
     "- Hạch toán từ / Hạch toán đến: lọc theo cột Ngày hạch toán, lấy cả hai đầu mốc.\n"
     "- Ngày tạo từ / Ngày tạo đến: lọc theo cột Ngày tạo (thời điểm lập phiếu), lấy cả hai đầu "
     "mốc.\n"
     "Màn Tổng hợp chỉ có Hạch toán từ / đến, lọc theo Ngày hạch toán của phiếu cha.\n"
     "Ngày chọn bằng lịch; hệ thống hiển thị dd/mm/yyyy."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu báo có gồm nhiều dòng chi tiết (quan hệ cha - con).\n"
     "Cột Khách hàng ở màn danh sách lấy theo dòng chi tiết ĐẦU TIÊN của phiếu; phiếu loại "
     "Thu nhà cung cấp hiển thị tên nhà cung cấp.\n"
     "Màn Tổng hợp tiền về ngân hàng hiển thị theo DÒNG CHI TIẾT, nên một phiếu có 3 dòng sẽ "
     "xuất hiện thành 3 dòng ở màn này.\n"
     "Bảng Chi tiết đổi bộ cột theo Loại thu: Thu bán hàng (khách hàng, hợp đồng, phiếu yêu cầu "
     "xuất hàng), Thu nhà cung cấp (nhà cung cấp, phiếu xuất hàng, hợp đồng mua), Thu khác (chỉ "
     "khách hàng, không bắt buộc)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Ô Tổng cộng của bảng chi tiết = tổng cột Số tiền của mọi dòng, cập nhật ngay khi gõ.\n"
     "- Cột Tổng PS của phiếu = tổng số tiền nguyên tệ các dòng; Tổng PS VND = tổng số tiền quy "
     "đổi (Số tiền nhân Tỷ giá của từng dòng).\n"
     "- Số tiền chưa điều chỉnh của một dòng = Số tiền quy đổi trừ phần đã điều chỉnh công nợ.\n"
     "- Một hợp đồng chỉ được chọn ở MỘT dòng trong cùng một phiếu; một phiếu xuất hàng cũng "
     "không được chọn trùng ở hai dòng.\n"
     "- Duyệt lại một phiếu đã duyệt không ghi thêm bút toán lần hai."),

    ("7. Phân quyền cấp",
     "Ba quyền của màn (tên đúng như hệ thống khai báo):\n"
     "- Quản lý phiếu báo có: Tạo mới, Sửa, Xóa, Duyệt, Import Excel, tích ô Không báo tiền về.\n"
     "- Xem tất cả phiếu báo có của tổng công ty: xem phiếu toàn hệ thống.\n"
     "- Xem tất cả phiếu báo có của công ty: xem phiếu của công ty mình.\n"
     "Không có quyền xem theo cấp nào thì chỉ thấy phiếu do chính mình lập.\n"
     "Điều kiện thao tác trên từng phiếu: Sửa và Xóa cần phiếu Đang tạo + do chính mình lập + có "
     "quyền Quản lý phiếu báo có; Duyệt cần phiếu Đang tạo + có quyền Quản lý phiếu báo có "
     "(không bắt buộc là người lập)."),

    ("8. Cách tính các ô thống kê",
     "- Ô “Hiển thị a–b / N” dưới bảng: a là số thứ tự dòng đầu trang, b là dòng cuối trang, "
     "N là tổng số bản ghi khớp bộ lọc trong phạm vi dữ liệu của người đăng nhập (không phải "
     "tổng toàn hệ thống).\n"
     "- Dòng Tổng cộng của bảng chi tiết trong form: cộng dồn cột Số tiền và cột Số tiền (VND).\n"
     "- Cột Trạng thái ở màn Tổng hợp được TÍNH tại thời điểm xem: còn tiền chưa điều chỉnh thì "
     "hiển thị “Chưa điều chỉnh hết công nợ”, ngược lại “Đã điều chỉnh hết công nợ”.\n"
     "- Kết quả kiểm tra file import hiển thị “Kiểm tra xong: X dòng hợp lệ, Y dòng lỗi”."),

    ("9. Ghi chú đọc bảng",
     "BẪY DỄ SAI NHẤT CỦA MÀN — đọc trước khi test:\n"
     "1. Duyệt phiếu là thao tác GHI SỔ KẾ TOÁN THẬT, không hoàn tác được. Chỉ duyệt trên dữ "
     "liệu test đã thống nhất, tuyệt đối không duyệt phiếu nghiệp vụ thật.\n"
     "2. Import Excel tạo phiếu ĐÃ DUYỆT và ghi sổ ngay — mỗi lần bấm Import là sinh bút toán "
     "thật, phải kiểm file trước.\n"
     "3. Phiếu Đang tạo của người khác luôn bị ẩn: khi test phân quyền phải dùng ĐÚNG tài khoản "
     "đã lập phiếu, đừng kết luận vội là lỗi lọc.\n"
     "4. Bảng danh sách và bảng chi tiết rộng hơn màn hình — phải kéo thanh cuộn ngang mới thấy "
     "cột Trạng thái, cột Hành động, cột Số tiền, Diễn giải.\n"
     "5. Ô tìm nhanh theo mã phiếu chỉ chạy khi bấm nút Tìm kiếm hoặc nhấn Enter; các ô trong "
     "bảng lọc nâng cao thì chạy ngay khi đổi giá trị.\n"
     "6. Hệ thống ghi nhớ bộ lọc trong 10 phút: vào lại màn vẫn thấy điều kiện cũ, bấm Làm mới "
     "để xóa.\n"
     "7. Màn hình chỉ có MỘT lối vào duy nhất (một mục menu). Không có chế độ xem “của tôi” "
     "riêng — xem phiếu của mình bằng cách lọc ô Người tạo.\n"
     "8. Số tiền hiển thị có dấu chấm ngăn cách nghìn; cột Tổng PS giữ 2 số thập phân, cột "
     "Tổng PS VND làm tròn số nguyên.\n"
     "9. Đổi Loại thu sẽ XÓA HẾT dòng chi tiết đang nhập (có hỏi xác nhận) — nhập lại từ đầu."),
]

# =============================================================== TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản có đủ 3 quyền của màn: mở màn và thấy đủ nút thao tác", "P0",
     "Tài khoản A có quyền Quản lý phiếu báo có, Xem tất cả phiếu báo có của tổng công ty và "
     "Xem tất cả phiếu báo có của công ty. Hệ thống đang có 3.834 phiếu, trong đó 4 phiếu "
     "Đang tạo do A lập.",
     "1. Đăng nhập bằng tài khoản A.\n"
     "2. Vào menu Tài chính → Quản lý tiền → Thanh toán tiền mặt → Phiếu báo có.\n"
     "3. Quan sát thanh công cụ và cột Hành động (kéo thanh cuộn ngang sang phải).",
     "—",
     "- Màn hiển thị đủ 3.834 phiếu (ô “Hiển thị a–b / N” hiện đúng tổng N).\n"
     "- Thanh công cụ có nút Tạo mới, Import Excel và biểu tượng Cấu hình cột.\n"
     "- Dòng phiếu Đang tạo do A lập có nút Sửa, nút Xóa và menu ba chấm chứa Duyệt, Lịch sử.\n"
     "- Dòng phiếu Đã duyệt chỉ có menu ba chấm chứa Lịch sử."),

    ("01", "Chỉ có quyền Quản lý phiếu báo có (không có quyền xem theo cấp)", "P0",
     "Tài khoản B chỉ có quyền Quản lý phiếu báo có. B đã lập 6 phiếu; phòng của B có tổng 40 "
     "phiếu do nhiều người lập.",
     "1. Đăng nhập bằng tài khoản B.\n"
     "2. Mở màn Phiếu báo có.\n"
     "3. Đối chiếu số bản ghi ở ô “Hiển thị a–b / N”.",
     "—",
     "- Chỉ hiển thị đúng 6 phiếu do B lập, không thấy phiếu của người khác.\n"
     "- Vẫn có nút Tạo mới và Import Excel.\n"
     "⚠️ Quyền thao tác KHÔNG mở rộng phạm vi xem — thấy nhiều hơn 6 phiếu là sai."),

    ("02", "Chỉ có quyền Xem tất cả phiếu báo có của tổng công ty", "P0",
     "Tài khoản C chỉ có quyền Xem tất cả phiếu báo có của tổng công ty. Hệ thống có 3.834 phiếu "
     "của nhiều công ty; C chưa lập phiếu nào.",
     "1. Đăng nhập bằng tài khoản C.\n"
     "2. Mở màn Phiếu báo có, quan sát thanh công cụ và cột Hành động.\n"
     "3. Mở bảng Tìm kiếm nâng cao.",
     "—",
     "- Thấy toàn bộ phiếu Đã duyệt của mọi công ty.\n"
     "- KHÔNG có nút Tạo mới, KHÔNG có nút Import Excel.\n"
     "- Cột Hành động chỉ còn mục Lịch sử.\n"
     "- Bảng lọc nâng cao có ô Công ty – Phòng ban – Bộ phận."),

    ("03", "Chỉ có quyền Xem tất cả phiếu báo có của công ty", "P0",
     "Tài khoản D thuộc công ty 1, chỉ có quyền Xem tất cả phiếu báo có của công ty. Công ty 1 "
     "có 120 phiếu Đã duyệt; công ty 4 có 80 phiếu Đã duyệt.",
     "1. Đăng nhập bằng tài khoản D.\n"
     "2. Mở màn Phiếu báo có, đếm số bản ghi.\n"
     "3. Gõ mã một phiếu của công ty 4 vào ô tìm nhanh, bấm Tìm kiếm.",
     "Mã phiếu của công ty 4",
     "- Bước 2 chỉ hiển thị 120 phiếu của công ty 1.\n"
     "- Bước 3 không tìm ra phiếu nào; bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n"
     "- Không có nút Tạo mới, Import Excel."),

    ("04", "Tài khoản không có quyền nào của màn", "P0",
     "Tài khoản E không có quyền nào trong 3 quyền của màn; E đã lập 2 phiếu (1 Đang tạo, "
     "1 Đã duyệt).",
     "1. Đăng nhập bằng tài khoản E.\n"
     "2. Mở màn Phiếu báo có.",
     "—",
     "- Màn mở được, chỉ hiển thị đúng 2 phiếu do E lập.\n"
     "- Không có nút Tạo mới, Import Excel, Sửa, Xóa, Duyệt."),

    ("05", "Phiếu Đang tạo của người khác bị ẩn với cả người có quyền xem cao nhất", "P0",
     "Tài khoản B lập 1 phiếu Đang tạo mã TEST.PBC.00001. Tài khoản C có quyền Xem tất cả phiếu "
     "báo có của tổng công ty.",
     "1. Đăng nhập bằng C.\n"
     "2. Gõ TEST.PBC.00001 vào ô tìm nhanh, bấm Tìm kiếm.\n"
     "3. Mở thẳng đường dẫn chi tiết của phiếu đó trên thanh địa chỉ.",
     "Mã phiếu: TEST.PBC.00001",
     "- Bước 2: không có kết quả nào.\n"
     "- Bước 3: hệ thống từ chối, báo không có quyền xem phiếu này.\n"
     "⚠️ Đây là quy tắc cố ý, không phải lỗi lọc."),

    ("06", "Người có quyền thao tác nhưng không phải người lập: không sửa/xóa được", "P0",
     "Phiếu TEST.PBC.00002 ở trạng thái Đang tạo do tài khoản A lập. Tài khoản B cũng có quyền "
     "Quản lý phiếu báo có.",
     "1. Đăng nhập bằng B.\n"
     "2. Tìm phiếu TEST.PBC.00002.",
     "Mã phiếu: TEST.PBC.00002",
     "- B không nhìn thấy phiếu này trong danh sách (phiếu Đang tạo của người khác luôn bị ẩn), "
     "do đó cũng không có nút Sửa / Xóa."),

    ("07", "Người có quyền thao tác duyệt được phiếu Đang tạo của người khác", "P1",
     "Trên dữ liệu test: phiếu Đang tạo do A lập, tài khoản A và B đều có quyền Quản lý phiếu "
     "báo có.",
     "1. Đăng nhập bằng A, mở danh sách.\n"
     "2. Bấm ba chấm ở dòng phiếu Đang tạo → chọn Duyệt.\n"
     "3. Bấm Hủy ở hộp xác nhận.",
     "—",
     "- Mục Duyệt hiển thị cho mọi người có quyền Quản lý phiếu báo có, không bắt buộc là người "
     "lập.\n"
     "- Bấm Hủy thì phiếu vẫn ở trạng thái Đang tạo, không sinh bút toán."),

    ("08", "Bỏ qua giao diện, gọi thẳng chức năng Tạo mới khi không có quyền thao tác", "P0",
     "Tài khoản C chỉ có quyền xem của tổng công ty.",
     "1. Dùng công cụ kiểm thử API đăng nhập bằng tài khoản C.\n"
     "2. Gọi thẳng chức năng Tạo mới phiếu báo có với dữ liệu hợp lệ, bỏ qua giao diện.",
     "Một phiếu hợp lệ: loại thu Thu bán hàng, 1 dòng chi tiết 1.000.000",
     "- Hệ thống từ chối, báo “Bạn không có quyền lập phiếu báo có”.\n"
     "- Không có phiếu nào được tạo trong danh sách."),

    ("09", "Bỏ qua giao diện, gọi thẳng chức năng Sửa / Xóa phiếu của người khác", "P0",
     "Phiếu Đang tạo mã TEST.PBC.00001 do tài khoản B lập. Tài khoản A có quyền Quản lý phiếu "
     "báo có.",
     "1. Dùng công cụ kiểm thử API đăng nhập bằng A.\n"
     "2. Gọi thẳng chức năng Sửa phiếu TEST.PBC.00001.\n"
     "3. Gọi thẳng chức năng Xóa phiếu đó.",
     "Mã phiếu: TEST.PBC.00001",
     "- Cả hai lần hệ thống đều từ chối, báo “Phiếu báo có đã duyệt hoặc không phải của bạn, "
     "không sửa được” / “... không xóa được”.\n"
     "- Dữ liệu phiếu không thay đổi."),

    ("10", "Bỏ qua giao diện, gọi thẳng chức năng Duyệt khi không có quyền thao tác", "P0",
     "Phiếu Đang tạo trong dữ liệu test; tài khoản C chỉ có quyền xem.",
     "1. Dùng công cụ kiểm thử API đăng nhập bằng C.\n"
     "2. Gọi thẳng chức năng Duyệt phiếu đó.",
     "—",
     "- Hệ thống từ chối, báo “Phiếu báo có không ở trạng thái Đang tạo hoặc bạn không có quyền "
     "duyệt”.\n"
     "- Phiếu vẫn ở trạng thái Đang tạo và KHÔNG có bút toán nào được ghi vào sổ."),

    ("11", "Bỏ qua giao diện, gọi thẳng chức năng Import khi không có quyền thao tác", "P0",
     "Tài khoản C chỉ có quyền xem.",
     "1. Dùng công cụ kiểm thử API đăng nhập bằng C.\n"
     "2. Gọi thẳng chức năng kiểm tra file import và chức năng import với 2 dòng hợp lệ.",
     "2 dòng sao kê hợp lệ",
     "- Cả hai lần hệ thống từ chối, báo “Bạn không có quyền import phiếu báo có”.\n"
     "- Không phiếu nào được tạo, không bút toán nào được ghi."),

    ("12", "Bỏ qua giao diện, gọi thẳng chức năng đánh dấu Không báo tiền về", "P1",
     "Phiếu Đã duyệt có 1 dòng chi tiết; tài khoản C chỉ có quyền xem của tổng công ty.",
     "1. Dùng công cụ kiểm thử API đăng nhập bằng C.\n"
     "2. Gọi thẳng chức năng bật cờ Không báo tiền về cho dòng chi tiết đó.",
     "Giá trị gửi lên: bật cờ",
     "- Hệ thống từ chối, báo “Bạn không có quyền cập nhật phiếu báo có”.\n"
     "- Dòng vẫn xuất hiện ở màn Tổng hợp tiền về ngân hàng."),
]

# =============================================================== SECTIONS
SEC_1 = [
    (1, "Mở màn hình từ menu", "P0",
     "Tài khoản A có đủ quyền, hệ thống có 3.834 phiếu.",
     "1. Đăng nhập.\n2. Chọn phân hệ Tài chính.\n"
     "3. Bấm Quản lý tiền → Thanh toán tiền mặt → Phiếu báo có.",
     "—",
     "- Tiêu đề trang hiển thị “Danh sách phiếu báo có”.\n"
     "- Bảng hiển thị 10 dòng đầu tiên, ô dưới bảng hiển thị “Hiển thị 1–10 / 3834”.\n"
     "- Phiếu mới nhất nằm trên cùng."),

    (2, "Mở màn hình bằng đường dẫn trực tiếp", "P1",
     "Tài khoản A đã đăng nhập.",
     "1. Gõ /finance/bill-income-reports vào thanh địa chỉ và nhấn Enter.",
     "—",
     "- Màn danh sách mở bình thường, dữ liệu giống khi vào bằng menu."),

    (3, "Thêm tham số lạ vào đường dẫn", "P1",
     "Tài khoản A đã đăng nhập.",
     "1. Mở đường dẫn /finance/bill-income-reports?type=abc&mode=999.",
     "type=abc, mode=999",
     "- Hệ thống bỏ qua tham số lạ, hiển thị danh sách như bình thường.\n"
     "- Không báo lỗi, không hiển thị thêm phiếu ngoài phạm vi dữ liệu của người đăng nhập.\n"
     "⚠️ Màn chỉ có một lối vào duy nhất, tham số trên thanh địa chỉ không mở rộng phạm vi xem."),

    (4, "Mở màn Tổng hợp tiền về ngân hàng từ menu", "P0",
     "Tài khoản A thuộc công ty có 6.559 dòng chi tiết thỏa điều kiện hiển thị.",
     "1. Bấm Quản lý tiền → Thanh toán tiền mặt → Tổng hợp tiền về ngân hàng.",
     "—",
     "- Tiêu đề trang hiển thị “Tổng hợp tiền về ngân hàng”.\n"
     "- Ô dưới bảng hiển thị “Hiển thị 1–10 / 6559”.\n"
     "- Có nút “Tạo mới điều chỉnh công nợ” và nút Xuất Excel."),

    (5, "Trạng thái rỗng của danh sách", "P1",
     "Tài khoản E chưa lập phiếu nào và không có quyền xem theo cấp.",
     "1. Đăng nhập bằng E.\n2. Mở màn Phiếu báo có.",
     "—",
     "- Bảng hiển thị dòng “Không có dữ liệu phù hợp bộ lọc.”\n"
     "- Ô đếm hiển thị tổng bằng 0, phần chuyển trang chỉ có trang 1."),

    (6, "Hiển thị vòng quay chờ khi đang nạp dữ liệu", "P2",
     "Danh sách có 3.834 phiếu.",
     "1. Mở màn hình và quan sát vùng bảng trong lúc dữ liệu đang tải.",
     "—",
     "- Bảng hiện chỉ báo đang tải dữ liệu, sau đó thay bằng dữ liệu thật.\n"
     "- Không hiện dòng “Không có dữ liệu” trong lúc đang tải."),

    (7, "Bố cục và thanh cuộn ngang của bảng", "P1",
     "Màn hình 1440x900, cấu hình cột để mặc định.",
     "1. Mở màn danh sách.\n2. Kéo thanh cuộn ngang phía trên bảng sang phải hết cỡ.",
     "—",
     "- Có thanh cuộn ngang ở cả trên và dưới bảng.\n"
     "- Kéo hết sang phải thấy đủ cột Trạng thái và cột Hành động.\n"
     "- Cột STT và cột Mã phiếu luôn dính bên trái, không trôi mất khi cuộn."),
]

SEC_2 = [
    (1, "Tìm nhanh theo mã phiếu bằng nút Tìm kiếm", "P0",
     "Có phiếu mã TPE.PBC0926.00003 trong phạm vi xem của người dùng.",
     "1. Gõ PBC0926 vào ô “Tìm theo mã phiếu...”.\n2. Bấm nút Tìm kiếm.",
     "Từ khóa: PBC0926",
     "- Danh sách chỉ còn phiếu có mã chứa chuỗi PBC0926.\n"
     "- Ô đếm cập nhật đúng số bản ghi khớp."),

    (2, "Ô tìm nhanh không tự chạy khi chưa bấm nút", "P1",
     "Danh sách đang hiển thị 3.834 phiếu.",
     "1. Gõ PBC0926 vào ô tìm nhanh.\n2. Chờ 5 giây, KHÔNG bấm nút và không nhấn Enter.",
     "Từ khóa: PBC0926",
     "- Danh sách vẫn giữ nguyên 3.834 phiếu.\n"
     "⚠️ Đây là thiết kế cố ý: ô tìm nhanh chỉ chạy khi bấm Tìm kiếm hoặc nhấn Enter."),

    (3, "Tìm nhanh bằng phím Enter", "P1",
     "Như trên.",
     "1. Gõ từ khóa vào ô tìm nhanh.\n2. Nhấn phím Enter.",
     "Từ khóa: PBC0926",
     "- Danh sách lọc ngay như khi bấm nút Tìm kiếm."),

    (4, "Mở và đóng bảng tìm kiếm nâng cao", "P1",
     "Đang ở màn danh sách.",
     "1. Bấm nút “Tìm kiếm nâng cao”.\n2. Bấm lại nút đó (lúc này ghi “Ẩn tìm kiếm nâng cao”).",
     "—",
     "- Lần 1 mở bảng lọc với đầy đủ các ô đã bật ở Cài đặt bộ lọc.\n"
     "- Lần 2 thu gọn bảng lọc, giá trị đang nhập không bị mất."),

    (5, "Lọc theo Loại thu", "P0",
     "Dữ liệu có cả 3 loại: Thu bán hàng, Thu nhà cung cấp, Thu khác.",
     "1. Mở bảng lọc nâng cao.\n2. Chọn ô Loại thu = Thu nhà cung cấp.",
     "Loại thu: Thu nhà cung cấp",
     "- Danh sách tự lọc ngay, không cần bấm Tìm kiếm.\n"
     "- Mọi dòng đều có cột Loại thu là “Thu nhà cung cấp”."),

    (6, "Lọc theo Trạng thái = Đang tạo", "P0",
     "Người dùng A đang có 4 phiếu Đang tạo.",
     "1. Chọn ô Trạng thái = Đang tạo.",
     "Trạng thái: Đang tạo",
     "- Chỉ hiển thị 4 phiếu Đang tạo do A lập.\n"
     "- Mỗi dòng đều có nút Sửa và nút Xóa."),

    (7, "Lọc theo Trạng thái = Đã duyệt", "P1",
     "Như trên.",
     "1. Chọn ô Trạng thái = Đã duyệt.",
     "Trạng thái: Đã duyệt",
     "- Mọi dòng có nhãn trạng thái “Đã duyệt” màu xanh.\n"
     "- Cột Hành động chỉ còn mục Lịch sử."),

    (8, "Lọc theo Người tạo để xem phiếu của mình", "P0",
     "Tài khoản A có quyền xem của tổng công ty và đã lập 12 phiếu.",
     "1. Chọn ô Người tạo = chính tài khoản A.",
     "Người tạo: A",
     "- Danh sách hiển thị đúng 12 phiếu do A lập.\n"
     "⚠️ Đây là cách thay cho chế độ xem “phiếu của tôi” — màn không có mục menu riêng."),

    (9, "Lọc theo Ngân hàng", "P1",
     "Dữ liệu có phiếu của các ngân hàng VIETINBANK, MB, SHB.",
     "1. Chọn ô Ngân hàng = MB.",
     "Ngân hàng: MB",
     "- Chỉ còn phiếu nhận tiền qua ngân hàng MB (bật cột Số TK ngân hàng để đối chiếu)."),

    (10, "Lọc theo Tài khoản ngân hàng (gõ một phần số)", "P1",
     "Có phiếu gắn số tài khoản 2591100125008.",
     "1. Gõ 25911 vào ô Tài khoản ngân hàng.",
     "Từ khóa: 25911",
     "- Chỉ còn phiếu có số tài khoản chứa chuỗi 25911."),

    (11, "Lọc theo Khách hàng (chọn từ danh sách gợi ý)", "P0",
     "Có 9.435 dòng chi tiết gắn khách hàng KHÁCH KHÔNG RÕ.",
     "1. Bấm ô Khách hàng, gõ “KHACH” (2 ký tự trở lên).\n2. Chọn khách KHÁCH KHÔNG RÕ.",
     "Khách hàng: 29TPHPTH-203 - KHÁCH KHÔNG RÕ",
     "- Danh sách chỉ còn phiếu có ít nhất một dòng chi tiết gắn khách đó.\n"
     "⚠️ Gõ dưới 2 ký tự thì danh sách gợi ý chưa hiện, không phải lỗi."),

    (12, "Lọc theo Tên khách hàng gõ tay", "P1",
     "Có khách hàng mã 29TPHPTU-1 tên CÔNG TY TNHH MTV TOYOTA MỸ ĐÌNH.",
     "1. Gõ “TOYOTA” vào ô Tên khách hàng (gõ tay).",
     "Từ khóa: TOYOTA",
     "- Danh sách chỉ còn phiếu có khách hàng mà chuỗi “Mã - Tên” chứa TOYOTA."),

    (13, "Lọc theo Ghi chú", "P1",
     "Có phiếu ghi chú “Tiền về ngân hàng Vietinbank ngày 27/07/2026”.",
     "1. Gõ “Vietinbank” vào ô Ghi chú.",
     "Từ khóa: Vietinbank",
     "- Chỉ còn phiếu có diễn giải chung chứa chuỗi đó (bật cột Ghi chú để đối chiếu)."),

    (14, "Lọc Không báo tiền về = Có", "P0",
     "Có 1 phiếu Đã duyệt trong đó 1 dòng chi tiết đã được đánh dấu Không báo tiền về.",
     "1. Chọn ô Không báo tiền về = Có.",
     "Không báo tiền về: Có",
     "- Chỉ hiển thị các phiếu có ÍT NHẤT một dòng đã đánh dấu.\n"
     "- Phiếu vừa chuẩn bị ở tiền điều kiện phải nằm trong kết quả."),

    (15, "Lọc Không báo tiền về = Không", "P1",
     "Như trên.",
     "1. Chọn ô Không báo tiền về = Không.",
     "Không báo tiền về: Không",
     "- Chỉ hiển thị phiếu KHÔNG có dòng nào đánh dấu.\n"
     "- Phiếu ở tiền điều kiện không xuất hiện."),

    (16, "Lọc theo khoảng Ngày hạch toán", "P0",
     "Có phiếu hạch toán ngày 24/08/2026 và phiếu hạch toán ngày 03/09/2026.",
     "1. Chọn Hạch toán từ = 24/08/2026.\n2. Chọn Hạch toán đến = 24/08/2026.",
     "Từ 24/08/2026 đến 24/08/2026",
     "- Chỉ hiển thị phiếu có Ngày hạch toán đúng 24/08/2026 (lấy cả hai đầu mốc).\n"
     "- Phiếu ngày 03/09/2026 không xuất hiện."),

    (17, "Lọc theo khoảng Ngày tạo", "P1",
     "Có phiếu lập ngày 24/08/2026 và phiếu lập ngày 03/09/2026.",
     "1. Chọn Ngày tạo từ = 03/09/2026 và Ngày tạo đến = 03/09/2026.",
     "Từ 03/09/2026 đến 03/09/2026",
     "- Chỉ còn phiếu lập trong ngày 03/09/2026, kể cả phiếu lập lúc 23 giờ."),

    (18, "Chọn ngày bắt đầu lớn hơn ngày kết thúc", "P2",
     "Dữ liệu bất kỳ.",
     "1. Chọn Hạch toán từ = 30/09/2026, Hạch toán đến = 01/09/2026.",
     "Từ 30/09/2026 đến 01/09/2026",
     "- Danh sách trả về rỗng, hiển thị “Không có dữ liệu phù hợp bộ lọc.”\n"
     "- Hệ thống không treo, không báo lỗi kỹ thuật."),

    (19, "Kết hợp nhiều điều kiện lọc", "P0",
     "Tài khoản A đã lập 4 phiếu Đang tạo, trong đó 2 phiếu loại Thu bán hàng.",
     "1. Chọn Trạng thái = Đang tạo.\n2. Chọn Loại thu = Thu bán hàng.\n"
     "3. Chọn Người tạo = A.",
     "—",
     "- Kết quả là giao của cả ba điều kiện: đúng 2 phiếu.\n"
     "- Ô đếm hiển thị tổng đúng bằng 2."),

    (20, "Bấm Làm mới để xóa toàn bộ điều kiện", "P0",
     "Đang áp dụng nhiều điều kiện lọc, danh sách còn 2 phiếu.",
     "1. Bấm nút Làm mới.",
     "—",
     "- Mọi ô lọc trở về trống, kể cả ô Khách hàng đã chọn.\n"
     "- Danh sách trở lại đầy đủ 3.834 phiếu, về trang 1."),

    (21, "Hệ thống ghi nhớ bộ lọc trong 10 phút", "P1",
     "Đang lọc Trạng thái = Đang tạo.",
     "1. Sang màn khác (ví dụ Phiếu thu).\n2. Quay lại màn Phiếu báo có trong vòng 10 phút.",
     "—",
     "- Ô Trạng thái vẫn giữ giá trị Đang tạo, danh sách vẫn đang lọc.\n"
     "- Bấm Làm mới thì bộ nhớ này bị xóa."),

    (22, "Lọc theo Công ty với người có quyền xem của tổng công ty", "P1",
     "Tài khoản C có quyền xem của tổng công ty; công ty 1 có 120 phiếu.",
     "1. Mở bảng lọc nâng cao.\n2. Chọn ô Công ty = công ty 1.",
     "Công ty: công ty 1",
     "- Danh sách chỉ còn 120 phiếu của công ty 1.\n"
     "- Với người không có quyền xem theo cấp, ô Công ty không hiển thị."),

    (23, "Lọc trên màn Tổng hợp: theo trạng thái điều chỉnh", "P0",
     "Màn Tổng hợp đang có 6.559 dòng, trong đó có dòng đã điều chỉnh hết và dòng chưa.",
     "1. Mở màn Tổng hợp tiền về ngân hàng.\n"
     "2. Mở tìm kiếm nâng cao, chọn Lọc phiếu = Chưa điều chỉnh hết công nợ.",
     "Lọc phiếu: Chưa điều chỉnh hết công nợ",
     "- Mọi dòng còn lại có cột Số tiền chưa điều chỉnh lớn hơn 0 và nhãn trạng thái vàng "
     "“Chưa điều chỉnh hết công nợ”."),

    (24, "Lọc trên màn Tổng hợp: theo khoảng số tiền", "P1",
     "Có dòng 432.000, dòng 2.943.000 và dòng 340.618.284.",
     "1. Nhập Số tiền từ = 1.000.000, Số tiền đến = 3.000.000.",
     "Từ 1.000.000 đến 3.000.000",
     "- Chỉ còn dòng có Số tiền nằm trong khoảng, ví dụ 2.943.000.\n"
     "- Dòng 432.000 và 340.618.284 không xuất hiện."),

    (25, "Lọc trên màn Tổng hợp: theo Ngân hàng gõ tay", "P1",
     "Có dòng thuộc ngân hàng VIETINBANK, MB, SHB.",
     "1. Gõ “MB” vào ô Ngân hàng rồi chờ danh sách tải lại.",
     "Từ khóa: MB",
     "- Chỉ còn dòng có cột Ngân hàng là MB.\n"
     "- Ô này tìm theo cả mã lẫn tên ngân hàng."),
]

SEC_3 = [
    (1, "Sắp xếp mặc định của danh sách", "P0",
     "Danh sách 3.834 phiếu.",
     "1. Mở màn hình, quan sát cột Mã phiếu và Ngày tạo của 3 dòng đầu.",
     "—",
     "- Phiếu mới nhất nằm trên cùng (mã và ngày tạo giảm dần)."),

    (2, "Sắp xếp theo Tổng PS tăng dần và giảm dần", "P1",
     "Danh sách có phiếu 1,00 và phiếu 99.999.999.999.999,98.",
     "1. Bấm biểu tượng sắp xếp ở tiêu đề cột Tổng PS (lần 1).\n2. Bấm lần 2.",
     "—",
     "- Lần 1 và lần 2 cho hai thứ tự ngược nhau (tăng dần / giảm dần) theo GIÁ TRỊ SỐ, không "
     "phải theo chuỗi.\n"
     "- Danh sách luôn quay về trang 1 sau khi đổi sắp xếp."),

    (3, "Sắp xếp theo Ngày hạch toán", "P1",
     "Dữ liệu có nhiều ngày hạch toán khác nhau.",
     "1. Bấm sắp xếp ở tiêu đề cột Ngày hạch toán.",
     "—",
     "- Danh sách sắp theo ngày, không phải theo chuỗi ký tự (03/09/2026 phải đứng sau "
     "24/08/2026 khi sắp tăng dần)."),

    (4, "Sắp xếp giữ nguyên bộ lọc đang áp dụng", "P1",
     "Đang lọc Loại thu = Thu bán hàng, còn 3.714 phiếu.",
     "1. Bấm sắp xếp cột Tổng PS VND.",
     "—",
     "- Bộ lọc vẫn giữ nguyên, ô đếm vẫn hiển thị 3.714.\n"
     "- Chỉ thứ tự dòng thay đổi."),

    (5, "Cột không có biểu tượng sắp xếp thì không sắp được", "P2",
     "Đang ở màn danh sách.",
     "1. Bấm vào tiêu đề cột Khách hàng và cột Ghi chú.",
     "—",
     "- Không có gì xảy ra, danh sách giữ nguyên thứ tự.\n"
     "- Chỉ 5 cột Mã phiếu, Tổng PS, Tổng PS VND, Ngày tạo, Ngày hạch toán sắp xếp được."),

    (6, "Chuyển trang", "P0",
     "Danh sách 3.834 phiếu, 10 dòng mỗi trang.",
     "1. Bấm số trang 2.\n2. Quan sát cột STT và ô đếm.",
     "—",
     "- STT bắt đầu từ 11, không quay lại 1.\n"
     "- Ô đếm hiển thị “Hiển thị 11–20 / 3834”."),

    (7, "Đổi số dòng mỗi trang", "P0",
     "Như trên.",
     "1. Chọn Số dòng/trang = 100.",
     "Số dòng/trang: 100",
     "- Bảng hiển thị 100 dòng, danh sách quay về trang 1.\n"
     "- Ô đếm hiển thị “Hiển thị 1–100 / 3834”."),

    (8, "Nút về trang đầu / cuối", "P1",
     "Danh sách nhiều trang.",
     "1. Bấm nút » (về trang cuối).\n2. Bấm nút « (về trang đầu).",
     "—",
     "- Trang cuối hiển thị đúng số dòng còn lại; trang đầu hiển thị lại 10 dòng đầu."),

    (9, "Chuyển trang giữ nguyên bộ lọc và sắp xếp", "P1",
     "Đang lọc Loại thu = Thu bán hàng và sắp xếp theo Tổng PS giảm dần.",
     "1. Bấm sang trang 3.",
     "—",
     "- Dữ liệu trang 3 vẫn thuộc bộ lọc, vẫn theo thứ tự đã chọn.\n"
     "- STT tiếp tục liên tục (21, 22, 23...)."),

    (10, "Tuỳ chỉnh cột: bật cột đang ẩn", "P0",
     "Bốn cột Phòng ban, Số TK ngân hàng, Ngày cập nhật, Người cập nhật đang tắt.",
     "1. Bấm biểu tượng Cấu hình cột.\n2. Tích 4 cột nói trên.\n3. Bấm Lưu.",
     "—",
     "- Hệ thống báo “Cập nhật thành công”.\n"
     "- Bảng hiện đủ 4 cột vừa bật, có dữ liệu (không phải dấu gạch ngang hàng loạt)."),

    (11, "Tuỳ chỉnh cột: không ẩn được cột bắt buộc", "P1",
     "Đang mở cửa sổ Tuỳ chỉnh cột.",
     "1. Thử bỏ tích cột STT, Mã phiếu, Hành động.",
     "—",
     "- Ba cột này có biểu tượng ổ khóa, ô tích bị khóa, không bỏ tích được.\n"
     "- Cũng không kéo thả đổi vị trí được."),

    (12, "Tuỳ chỉnh cột: cấu hình lưu theo từng người dùng", "P1",
     "Tài khoản A đã bật cột Phòng ban; tài khoản B chưa đụng vào cấu hình.",
     "1. Đăng nhập bằng B, mở màn Phiếu báo có.",
     "—",
     "- Bảng của B vẫn theo cấu hình mặc định, không bị ảnh hưởng bởi thay đổi của A."),

    (13, "Cài đặt bộ lọc: ẩn bớt tiêu chí", "P1",
     "Bảng lọc đang hiển thị đủ 12 tiêu chí.",
     "1. Bấm Cài đặt bộ lọc.\n2. Bỏ tích tiêu chí Ghi chú và Không báo tiền về.\n3. Bấm Lưu.",
     "—",
     "- Hệ thống báo “Cập nhật thành công”.\n"
     "- Bảng tìm kiếm nâng cao không còn 2 ô đó."),

    (14, "Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị", "P0",
     "Ô Ghi chú đang lọc theo từ khóa “Vietinbank”, danh sách còn 30 phiếu.",
     "1. Bấm Cài đặt bộ lọc, bỏ tích tiêu chí Ghi chú, bấm Lưu.",
     "—",
     "- Ô Ghi chú bị ẩn VÀ giá trị lọc bị xóa; danh sách trở lại đầy đủ.\n"
     "⚠️ Nếu danh sách vẫn còn 30 phiếu là lỗi lọc ngầm bằng ô người dùng không nhìn thấy."),

    (15, "Cài đặt bộ lọc: khôi phục mặc định", "P2",
     "Đang ẩn 2 tiêu chí và đã đổi thứ tự.",
     "1. Bấm Cài đặt bộ lọc → Khôi phục mặc định → Lưu.",
     "—",
     "- Danh sách tiêu chí trở về đủ 12 mục theo thứ tự gốc."),
]

SEC_4 = [
    (1, "Giá trị mặc định của form Tạo mới", "P0",
     "Tài khoản A có quyền Quản lý phiếu báo có. Ngày hiện tại 05/09/2026.",
     "1. Bấm nút Tạo mới.\n2. Quan sát toàn bộ khối Thông tin chung và bảng Chi tiết.",
     "—",
     "- Loại thu = Thu bán hàng; Tài khoản nợ = 1121 - Tiền Việt Nam; Loại tiền = VNĐ; "
     "Tỷ giá = 1 và ô bị khóa; Ngày hạch toán = 05/09/2026.\n"
     "- Ngân hàng và Tài khoản để trống; ô Tài khoản bị khóa.\n"
     "- Bảng Chi tiết có sẵn 1 dòng: Số tài khoản có = 1311, Khách hàng = 29TPHPTH-203, "
     "Tên khách hàng = KHÁCH KHÔNG RÕ, Số tiền = 0."),

    (2, "Ô Tài khoản bị khóa cho tới khi chọn Ngân hàng", "P0",
     "Đang ở form Tạo mới.",
     "1. Bấm vào ô Tài khoản khi chưa chọn Ngân hàng.\n2. Chọn Ngân hàng = MB.\n"
     "3. Bấm lại ô Tài khoản.",
     "Ngân hàng: MB",
     "- Bước 1: ô không mở được danh sách.\n"
     "- Bước 3: danh sách mở ra và CHỈ gồm tài khoản của ngân hàng MB."),

    (3, "Chọn Tài khoản thì Chi nhánh tự điền", "P0",
     "Tài khoản 2591100125008 thuộc chi nhánh Bắc Hải Phòng.",
     "1. Chọn Ngân hàng = MB.\n2. Chọn Tài khoản = 2591100125008.",
     "Tài khoản: 2591100125008",
     "- Ô Chi nhánh tự điền “Bắc Hải Phòng”, không sửa tay được."),

    (4, "Đổi Ngân hàng thì xóa Tài khoản và Chi nhánh", "P0",
     "Đã chọn Ngân hàng MB, Tài khoản 2591100125008, Chi nhánh tự điền.",
     "1. Đổi ô Ngân hàng sang VIETINBANK.",
     "Ngân hàng: VIETINBANK",
     "- Ô Tài khoản và ô Chi nhánh trở về trống.\n"
     "- Danh sách tài khoản chỉ còn tài khoản của VIETINBANK."),

    (5, "Đổi Loại tiền sang ngoại tệ", "P0",
     "Danh mục loại tiền có USD với tỷ giá 25.000.",
     "1. Đổi ô Loại tiền sang USD.\n2. Quan sát ô Tỷ giá và bảng Chi tiết.",
     "Loại tiền: USD",
     "- Ô Tỷ giá mở khóa và tự điền tỷ giá của USD.\n"
     "- Bảng Chi tiết hiện thêm cột Số tiền (VND); tiêu đề cột Số tiền ghi kèm tên loại tiền."),

    (6, "Cột Số tiền (VND) tự quy đổi theo tỷ giá", "P0",
     "Loại tiền USD, tỷ giá 25.000.",
     "1. Nhập Số tiền của dòng 1 = 2.000.\n2. Quan sát cột Số tiền (VND) và dòng Tổng cộng.",
     "Số tiền: 2.000",
     "- Cột Số tiền (VND) hiển thị 50.000.000.\n"
     "- Dòng Tổng cộng hiển thị 2.000 và 50.000.000."),

    (7, "Đổi tỷ giá thì tính lại toàn bộ cột quy đổi", "P0",
     "Đã có 2 dòng chi tiết với số tiền 2.000 và 1.000, tỷ giá 25.000.",
     "1. Sửa ô Tỷ giá thành 26.000.",
     "Tỷ giá: 26.000",
     "- Cột Số tiền (VND) của cả 2 dòng tính lại: 52.000.000 và 26.000.000.\n"
     "- Dòng Tổng cộng cập nhật tương ứng."),

    (8, "Ô Tỷ giá bị khóa khi loại tiền là VNĐ", "P1",
     "Đang ở form Tạo mới với loại tiền VNĐ.",
     "1. Thử bấm và gõ vào ô Tỷ giá.",
     "—",
     "- Ô bị khóa, luôn hiển thị 1.\n"
     "- Bảng Chi tiết không có cột Số tiền (VND)."),

    (9, "Thêm dòng chi tiết", "P0",
     "Đang ở form Tạo mới loại Thu bán hàng.",
     "1. Bấm nút Thêm dòng 2 lần.",
     "—",
     "- Bảng có 3 dòng; mỗi dòng mới đều điền sẵn Số tài khoản có = 1311 và khách hàng "
     "KHÁCH KHÔNG RÕ."),

    (10, "Xóa dòng chi tiết", "P1",
     "Bảng đang có 3 dòng.",
     "1. Bấm biểu tượng thùng rác ở dòng số 2.",
     "—",
     "- Dòng số 2 biến mất, bảng còn 2 dòng, số thứ tự đánh lại liên tục 1 và 2.\n"
     "- Dòng Tổng cộng trừ đi số tiền của dòng vừa xóa."),

    (11, "Đổi Loại thu khi bảng chi tiết còn trống", "P1",
     "Form Tạo mới vừa mở, chưa nhập gì.",
     "1. Đổi Loại thu sang Thu nhà cung cấp.",
     "Loại thu: Thu nhà cung cấp",
     "- Hệ thống KHÔNG hỏi xác nhận (vì chưa có dữ liệu).\n"
     "- Bảng đổi sang bộ cột nhà cung cấp, tài khoản có mặc định 3311."),

    (12, "Đổi Loại thu khi đã nhập dữ liệu — chọn Đồng ý", "P0",
     "Đã nhập số tiền 1.500.000 và diễn giải cho dòng 1.",
     "1. Đổi Loại thu sang Thu khác.\n2. Bấm Đồng ý ở hộp xác nhận.",
     "Loại thu: Thu khác",
     "- Hộp thoại hiện “Đổi loại thu sẽ xóa toàn bộ dòng chi tiết đang nhập. Bạn có chắc chắn?”\n"
     "- Sau khi Đồng ý: bảng còn đúng 1 dòng trống, Số tài khoản có để trống, số tiền về 0."),

    (13, "Đổi Loại thu khi đã nhập dữ liệu — chọn Hủy", "P0",
     "Như trên.",
     "1. Đổi Loại thu sang Thu khác.\n2. Bấm Hủy ở hộp xác nhận.",
     "—",
     "- Ô Loại thu quay về giá trị cũ (Thu bán hàng).\n"
     "- Dữ liệu dòng chi tiết còn nguyên."),

    (14, "Chọn khách hàng cho dòng chi tiết", "P0",
     "Có khách hàng 29TPHPTU-1 - CÔNG TY TNHH MTV TOYOTA MỸ ĐÌNH.",
     "1. Bấm ô cột Khách hàng của dòng 1.\n2. Gõ TOYOTA MỸ ĐÌNH, bấm Tìm kiếm.\n"
     "3. Bấm vào dòng khách hàng trong kết quả.",
     "Từ khóa: TOYOTA MỸ ĐÌNH",
     "- Cửa sổ “Chọn khách hàng” mở ra với các ô tìm theo Tên/Mã, Mã số thuế, Số điện thoại.\n"
     "- Sau khi chọn: ô Khách hàng hiển thị 29TPHPTU-1, cột Tên khách hàng hiển thị tên đầy đủ, "
     "cửa sổ đóng lại."),

    (15, "Đổi khách hàng thì xóa hợp đồng đã chọn", "P0",
     "Dòng 1 đang gắn khách hàng TOYOTA MỸ ĐÌNH và hợp đồng HDDV_TPE_HN_KD2_26_0264_TOYOTAMD_1607.",
     "1. Bấm lại ô Khách hàng, chọn khách khác.",
     "Khách hàng khác bất kỳ",
     "- Ô Số đơn hàng/Hợp đồng, Phiếu YC xuất hàng và cột NVKD của dòng trở về trống.\n"
     "⚠️ Nếu hợp đồng cũ vẫn còn là sai — tiền sẽ gắn vào hợp đồng của khách khác."),

    (16, "Chọn hợp đồng khi chưa chọn khách hàng", "P0",
     "Dòng chi tiết mới thêm, ô Khách hàng đã bị xóa trắng.",
     "1. Bấm ô Số đơn hàng/Hợp đồng.",
     "—",
     "- Hệ thống báo “Chưa chọn khách hàng” và KHÔNG mở cửa sổ chọn hợp đồng."),

    (17, "Cửa sổ hợp đồng chỉ liệt kê hợp đồng của khách đã chọn", "P0",
     "Khách TOYOTA MỸ ĐÌNH có 44 hợp đồng.",
     "1. Chọn khách TOYOTA MỸ ĐÌNH cho dòng 1.\n2. Bấm ô Số đơn hàng/Hợp đồng.",
     "—",
     "- Tiêu đề cửa sổ ghi rõ “29TPHPTU-1 - CÔNG TY TNHH MTV TOYOTA MỸ ĐÌNH”.\n"
     "- Ô đếm hiển thị đúng 44 hợp đồng; các cột Ngày lập, Giá trị hợp đồng, Số tiền còn nợ có "
     "dữ liệu."),

    (18, "Chọn hợp đồng và kiểm tra cột NVKD", "P1",
     "Hợp đồng HDDV_TPE_HN_KD2_26_0264_TOYOTAMD_1607 do một nhân viên kinh doanh tạo.",
     "1. Bấm vào dòng hợp đồng trong cửa sổ.",
     "—",
     "- Ô Số đơn hàng/Hợp đồng điền số hợp đồng, cửa sổ đóng.\n"
     "- Cột NVKD hiển thị tên người tạo hợp đồng."),

    (19, "Không chọn trùng một hợp đồng ở hai dòng", "P1",
     "Dòng 1 đã gắn hợp đồng X của khách TOYOTA MỸ ĐÌNH; dòng 2 cũng gắn khách đó.",
     "1. Ở dòng 2, bấm ô hợp đồng và tìm hợp đồng X.",
     "Hợp đồng X",
     "- Hợp đồng X không chọn lại được (bị khóa trong cửa sổ)."),

    (20, "Hợp đồng nguyên tắc hiện ô tích dư nợ đầu kì", "P1",
     "Khách hàng có hợp đồng nguyên tắc với số dư nợ đầu kỳ 5.000.000.",
     "1. Chọn hợp đồng nguyên tắc đó cho dòng 1.",
     "—",
     "- Ngay dưới ô hợp đồng xuất hiện ô tích “Số dư nợ đầu kì: 5.000.000”.\n"
     "- Cột Phiếu YC xuất hàng mở ra ô để chọn."),

    (21, "Tích dư nợ đầu kì thì không cần chọn phiếu yêu cầu xuất hàng", "P1",
     "Dòng đang gắn hợp đồng nguyên tắc.",
     "1. Tích ô “Số dư nợ đầu kì”.\n2. Nhập số tiền, diễn giải rồi bấm Lưu.",
     "Số tiền: 5.000.000",
     "- Ô Phiếu YC xuất hàng chuyển thành dấu gạch ngang.\n"
     "- Phiếu lưu thành công, không đòi chọn phiếu yêu cầu xuất hàng."),

    (22, "Chọn phiếu yêu cầu xuất hàng khi chưa chọn hợp đồng", "P1",
     "Dòng chi tiết chưa gắn hợp đồng.",
     "1. Bấm ô Phiếu YC xuất hàng (nếu hiển thị).",
     "—",
     "- Hệ thống báo “Chưa chọn hợp đồng” và không mở cửa sổ."),

    (23, "Chọn nhà cung cấp cho loại thu Thu nhà cung cấp", "P0",
     "Danh mục có 9.547 nhà cung cấp.",
     "1. Đổi Loại thu = Thu nhà cung cấp.\n2. Bấm ô Nhà cung cấp của dòng 1.\n"
     "3. Gõ mã hoặc tên rồi bấm Tìm kiếm, chọn một dòng.",
     "—",
     "- Cửa sổ “Chọn nhà cung cấp” hiển thị 2 cột Mã và Tên nhà cung cấp.\n"
     "- Sau khi chọn: ô Nhà cung cấp và cột Tên nhà cung cấp điền đúng giá trị."),

    (24, "Chọn phiếu xuất hàng khi chưa chọn nhà cung cấp", "P0",
     "Dòng chi tiết đã xóa trắng ô Nhà cung cấp.",
     "1. Bấm ô Phiếu xuất hàng.",
     "—",
     "- Hệ thống báo “Chưa chọn nhà cung cấp” và không mở cửa sổ."),

    (25, "Cửa sổ phiếu xuất hàng khi nhà cung cấp không có phiếu nào", "P1",
     "Chọn một nhà cung cấp chưa từng có phiếu xuất trả hàng.",
     "1. Bấm ô Phiếu xuất hàng.",
     "—",
     "- Cửa sổ mở ra và hiển thị “Không có phiếu xuất phù hợp.”\n"
     "- Không báo lỗi kỹ thuật."),

    (26, "Chọn phiếu xuất hàng thì tự điền Hợp đồng mua và NVKD", "P1",
     "Nhà cung cấp có phiếu xuất trả hàng gắn với một hợp đồng mua.",
     "1. Bấm ô Phiếu xuất hàng, chọn một phiếu trong danh sách.",
     "—",
     "- Ô Phiếu xuất hàng điền mã phiếu.\n"
     "- Cột Hợp đồng mua và cột NVKD tự điền theo phiếu xuất đó."),

    (27, "Không chọn trùng phiếu xuất hàng ở hai dòng", "P1",
     "Dòng 1 đã chọn phiếu xuất số PX-001.",
     "1. Ở dòng 2 chọn cùng nhà cung cấp, bấm ô Phiếu xuất hàng và chọn lại PX-001.",
     "Phiếu xuất: PX-001",
     "- Hệ thống báo “Phiếu đã tồn tại!” và không điền vào dòng 2."),

    (28, "Bộ cột của loại thu Thu khác", "P0",
     "Đang ở form Tạo mới.",
     "1. Đổi Loại thu sang Thu khác.\n2. Quan sát tiêu đề các cột của bảng Chi tiết.",
     "Loại thu: Thu khác",
     "- Bảng chỉ có: STT, Số tài khoản có, Tên tài khoản, Khách hàng, Tên khách hàng, Số tiền, "
     "Diễn giải, Không báo tiền về, Xóa.\n"
     "- Cột Khách hàng KHÔNG có dấu sao đỏ (không bắt buộc).\n"
     "- Ô Số tài khoản có để trống, không có giá trị mặc định."),

    (29, "Lưu phiếu ở trạng thái Đang tạo", "P0",
     "Đã nhập đủ: Loại thu Thu bán hàng, Ngân hàng MB, Tài khoản 2591100125008, 1 dòng chi tiết "
     "số tiền 1.500.000 và diễn giải.",
     "1. Bấm nút Lưu.",
     "Số tiền: 1.500.000; Diễn giải: Test luu nhap",
     "- Hệ thống báo “Thêm phiếu báo có thành công!” và quay về danh sách.\n"
     "- Phiếu mới nằm đầu danh sách, trạng thái Đang tạo (nhãn xám), có nút Sửa và Xóa.\n"
     "- Mã phiếu có dạng <mã công ty>.PBC<tháng năm>.<5 chữ số>."),

    (30, "Lưu và duyệt ngay từ form Tạo mới", "P0",
     "Đã nhập đủ thông tin hợp lệ như trên. ĐÂY LÀ THAO TÁC GHI SỔ THẬT — chỉ chạy trên dữ liệu "
     "test đã thống nhất.",
     "1. Bấm nút “Lưu và duyệt”.\n2. Xác nhận ở hộp thoại.",
     "Số tiền: 1.500.000",
     "- Hệ thống báo “Thêm phiếu báo có thành công! Phiếu đã được duyệt và ghi bút toán vào "
     "sổ cái.”\n"
     "- Phiếu ở danh sách có trạng thái Đã duyệt, KHÔNG còn nút Sửa và Xóa.\n"
     "⚠️ Sau bước này phiếu không sửa/xóa được nữa, kiểm tra kỹ trước khi bấm."),

    (31, "Nút Lưu và tiếp tục", "P1",
     "Đã nhập đủ thông tin hợp lệ.",
     "1. Bấm nút “Lưu và tiếp tục”.",
     "—",
     "- Hệ thống báo lưu thành công nhưng GIỮ NGUYÊN màn Tạo mới.\n"
     "- Form trở về trắng với đầy đủ giá trị mặc định như lúc mới mở.\n"
     "- Phiếu vừa lưu ở trạng thái Đang tạo (không phải Đã duyệt)."),

    (32, "Cảnh báo khi rời màn lúc chưa lưu", "P0",
     "Đang ở form Tạo mới, đã nhập số tiền và diễn giải.",
     "1. Bấm nút Quay lại.",
     "—",
     "- Hệ thống hiển thị hộp hỏi xác nhận rời trang.\n"
     "- Chọn ở lại thì dữ liệu còn nguyên; chọn rời đi thì về danh sách và bỏ thay đổi."),

    (33, "Không cảnh báo khi chưa sửa gì", "P2",
     "Vừa mở form Tạo mới, chưa nhập gì.",
     "1. Bấm nút Quay lại.",
     "—",
     "- Về thẳng danh sách, không hỏi xác nhận."),

    (34, "Dòng Tổng cộng cộng đúng nhiều dòng", "P0",
     "Loại tiền VNĐ.",
     "1. Thêm 3 dòng chi tiết với số tiền 1.000.000, 2.500.000 và 500.000.",
     "1.000.000 / 2.500.000 / 500.000",
     "- Dòng Tổng cộng hiển thị 4.000.000 và cập nhật ngay sau mỗi lần gõ."),
]

SEC_5 = [
    (1, "Mở màn Sửa từ danh sách", "P0",
     "Phiếu TEST.PBC.00001 ở trạng thái Đang tạo do tài khoản đang đăng nhập lập.",
     "1. Kéo thanh cuộn ngang sang phải.\n2. Bấm biểu tượng bút chì ở dòng phiếu đó.",
     "—",
     "- Mở màn “Sửa phiếu báo có” với dữ liệu đã điền sẵn đúng như phiếu.\n"
     "- Ô Mã phiếu hiển thị TEST.PBC.00001 và bị khóa.\n"
     "- Có thêm 2 ô chỉ đọc: Người lập và Phòng ban."),

    (2, "Mở màn Sửa từ màn chi tiết", "P1",
     "Như trên.",
     "1. Mở màn chi tiết phiếu.\n2. Bấm nút Sửa ở thanh dưới cùng.",
     "—",
     "- Mở đúng màn Sửa của phiếu đó."),

    (3, "Sửa thông tin chung và lưu", "P0",
     "Phiếu Đang tạo có diễn giải “TEST — Thu bán hàng”.",
     "1. Sửa ô Diễn giải thành “TEST — sua lan 1”.\n2. Bấm Lưu.",
     "Diễn giải: TEST — sua lan 1",
     "- Hệ thống báo “Cập nhật phiếu báo có thành công!” và quay về danh sách.\n"
     "- Cột Ghi chú của phiếu hiển thị giá trị mới."),

    (4, "Sửa bảng chi tiết: thêm dòng", "P0",
     "Phiếu Đang tạo có 1 dòng chi tiết 1.500.000.",
     "1. Mở màn Sửa, bấm Thêm dòng.\n2. Nhập số tiền 500.000, diễn giải, chọn khách hàng.\n"
     "3. Bấm Lưu.",
     "Số tiền dòng 2: 500.000",
     "- Lưu thành công.\n"
     "- Cột Tổng PS của phiếu ở danh sách cập nhật thành 2.000.000."),

    (5, "Sửa bảng chi tiết: xóa dòng", "P1",
     "Phiếu Đang tạo có 2 dòng: 1.500.000 và 500.000.",
     "1. Mở màn Sửa, bấm thùng rác ở dòng 2.\n2. Bấm Lưu.",
     "—",
     "- Lưu thành công, phiếu còn 1 dòng.\n"
     "- Tổng PS trở lại 1.500.000."),

    (6, "Xóa hết dòng chi tiết rồi lưu", "P0",
     "Phiếu Đang tạo có 1 dòng.",
     "1. Xóa dòng duy nhất.\n2. Bấm Lưu.",
     "—",
     "- Hệ thống báo lỗi “Phải có ít nhất 1 dòng chi tiết”, không lưu.\n"
     "- Vẫn ở màn Sửa, dữ liệu còn nguyên."),

    (7, "Mở màn Sửa của phiếu đã duyệt bằng đường dẫn trực tiếp", "P0",
     "Phiếu TPE.PBC0926.00003 ở trạng thái Đã duyệt.",
     "1. Gõ đường dẫn màn Sửa của phiếu đó vào thanh địa chỉ.",
     "—",
     "- Hệ thống tự chuyển sang màn Chi tiết của phiếu, không cho vào màn Sửa.\n"
     "⚠️ Không được dựa vào việc danh sách đã ẩn nút Sửa — phải chặn cả khi vào thẳng."),

    (8, "Sửa phiếu vừa bị người khác xóa", "P1",
     "Mở màn Sửa của một phiếu ở tab 1; ở tab 2 xóa chính phiếu đó.",
     "1. Ở tab 1, bấm Lưu.",
     "—",
     "- Hệ thống báo phiếu không tồn tại hoặc không sửa được, không treo trang."),

    (9, "Mở màn Sửa của phiếu đã bị xóa", "P1",
     "Phiếu vừa bị xóa ở nơi khác.",
     "1. Mở đường dẫn màn Sửa của phiếu đó.",
     "—",
     "- Hệ thống báo “Không tìm thấy dữ liệu”, không hiển thị form trống với dữ liệu rác."),

    (10, "Cảnh báo chưa lưu ở màn Sửa", "P1",
     "Đang ở màn Sửa, đã đổi số tiền.",
     "1. Bấm Quay lại.",
     "—",
     "- Hệ thống hỏi xác nhận rời trang; chọn ở lại thì dữ liệu còn nguyên."),

    (11, "Lưu và duyệt từ màn Sửa", "P0",
     "Phiếu Đang tạo hợp lệ trong dữ liệu test.",
     "1. Mở màn Sửa, bấm “Lưu và duyệt”, xác nhận.",
     "—",
     "- Phiếu chuyển sang Đã duyệt và bút toán được ghi vào sổ.\n"
     "- Mở lại phiếu thì không còn nút Sửa, Xóa."),

    (12, "Màn Sửa giữ đúng tài khoản ngân hàng đã khóa", "P2",
     "Phiếu Đang tạo gắn số tài khoản công ty đã bị khóa trong danh mục.",
     "1. Mở màn Sửa của phiếu.",
     "—",
     "- Ô Tài khoản vẫn hiển thị đúng số tài khoản cũ, không bị trống.\n"
     "- Lưu lại không làm mất giá trị này."),
]

SEC_6 = [
    (1, "Duyệt phiếu từ màn chi tiết", "P0",
     "Phiếu Đang tạo mã TEST.PBC.00001, số tiền 1.500.000, 1 dòng chi tiết. Đây là dữ liệu test "
     "đã thống nhất được phép ghi sổ.",
     "1. Mở màn chi tiết.\n2. Bấm nút Duyệt.\n3. Đọc hộp xác nhận rồi bấm Duyệt.",
     "—",
     "- Hộp thoại ghi “Duyệt phiếu báo có ‘TEST.PBC.00001’? Hệ thống sẽ ghi bút toán vào sổ cái "
     "và phiếu không sửa/xóa được nữa.”\n"
     "- Sau khi xác nhận: báo “Duyệt phiếu báo có thành công.”, quay về danh sách, phiếu chuyển "
     "trạng thái Đã duyệt."),

    (2, "Duyệt phiếu từ danh sách", "P0",
     "Phiếu Đang tạo khác trong dữ liệu test.",
     "1. Kéo cuộn ngang, bấm dấu ba chấm ở dòng phiếu.\n2. Chọn Duyệt.\n3. Xác nhận.",
     "—",
     "- Kết quả giống khi duyệt ở màn chi tiết; danh sách tự tải lại và phiếu đổi nhãn trạng thái."),

    (3, "Bấm Hủy ở hộp xác nhận duyệt", "P0",
     "Phiếu Đang tạo.",
     "1. Bấm Duyệt.\n2. Bấm Hủy.",
     "—",
     "- Hộp thoại đóng, phiếu vẫn Đang tạo.\n"
     "- Không có bút toán nào được ghi vào sổ (kiểm tra ở sổ kế toán không thấy phát sinh mới)."),

    (4, "Bút toán ghi vào sổ cân Nợ và Có", "P0",
     "Phiếu test 1 dòng chi tiết 1.500.000, tài khoản nợ 1121, tài khoản có 1311.",
     "1. Duyệt phiếu.\n2. Kiểm tra sổ kế toán theo mã phiếu vừa duyệt.",
     "—",
     "- Sinh bút toán ghi Nợ tài khoản 1121 và ghi Có tài khoản 1311 cùng số tiền 1.500.000.\n"
     "- Tổng phát sinh Nợ bằng tổng phát sinh Có."),

    (5, "Phiếu nhiều dòng sinh nhiều bút toán", "P1",
     "Phiếu test có 3 dòng chi tiết: 1.000.000, 2.500.000, 500.000.",
     "1. Duyệt phiếu.\n2. Kiểm tra sổ kế toán.",
     "—",
     "- Có 3 cặp bút toán tương ứng 3 dòng, tổng cộng 4.000.000.\n"
     "- Ngày ghi sổ đúng bằng Ngày hạch toán trên phiếu."),

    (6, "Duyệt lại phiếu đã duyệt", "P0",
     "Phiếu vừa duyệt xong ở bước trên.",
     "1. Mở phiếu, quan sát thanh nút.\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt lần nữa.",
     "—",
     "- Giao diện không còn nút Duyệt.\n"
     "- Gọi thẳng chức năng thì hệ thống từ chối và KHÔNG ghi thêm bút toán nào."),

    (7, "Hai người cùng duyệt một phiếu", "P0",
     "Phiếu Đang tạo; tài khoản A và B đều có quyền Quản lý phiếu báo có và đều mở phiếu.",
     "1. A bấm Duyệt và xác nhận.\n2. Ngay sau đó B bấm Duyệt và xác nhận.",
     "—",
     "- Lần của A thành công.\n"
     "- Lần của B bị từ chối với thông báo phiếu không còn ở trạng thái Đang tạo.\n"
     "- Sổ kế toán chỉ có MỘT lần ghi bút toán cho phiếu này."),

    (8, "Thông báo gửi cho kế toán cùng công ty sau khi duyệt", "P1",
     "Tài khoản B có quyền Quản lý phiếu báo có, cùng công ty với phiếu.",
     "1. Tài khoản A duyệt phiếu.\n2. Đăng nhập bằng B, mở chuông thông báo.",
     "—",
     "- B nhận được thông báo có nội dung nêu mã phiếu và tên người lập.\n"
     "- Bấm vào thông báo mở đúng màn chi tiết của phiếu đó."),

    (9, "Phiếu đã duyệt không sửa, không xóa", "P0",
     "Phiếu vừa duyệt.",
     "1. Mở danh sách, tìm phiếu.\n2. Quan sát cột Hành động.\n3. Mở màn chi tiết.",
     "—",
     "- Cột Hành động chỉ còn mục Lịch sử.\n"
     "- Màn chi tiết không có nút Sửa, không có nút Xóa, không có nút Duyệt."),

    (10, "Dòng chi tiết số tiền 0 không sinh bút toán", "P2",
     "Trường hợp dữ liệu cũ có dòng số tiền bằng 0 (dữ liệu nhập từ trước khi có ràng buộc).",
     "1. Duyệt phiếu chứa dòng đó.\n2. Kiểm tra sổ kế toán.",
     "—",
     "- Dòng số tiền 0 không sinh bút toán; các dòng còn lại vẫn ghi bình thường."),
]

SEC_7 = [
    (1, "Xóa phiếu Đang tạo từ danh sách", "P0",
     "Phiếu Đang tạo do chính người dùng lập.",
     "1. Bấm biểu tượng thùng rác ở dòng phiếu.\n2. Đọc hộp thoại rồi bấm Xóa.",
     "—",
     "- Hộp thoại ghi “Bạn có chắc muốn xóa phiếu báo có ‘<mã phiếu>’?”, nút xác nhận màu đỏ.\n"
     "- Sau khi xóa: báo “Xóa thành công.”, danh sách tải lại và không còn phiếu đó."),

    (2, "Xóa phiếu từ màn chi tiết", "P1",
     "Như trên.",
     "1. Mở màn chi tiết, bấm nút Xóa (màu đỏ).\n2. Xác nhận.",
     "—",
     "- Xóa thành công và điều hướng về màn danh sách."),

    (3, "Bấm Hủy ở hộp xác nhận xóa", "P0",
     "Phiếu Đang tạo.",
     "1. Bấm Xóa.\n2. Bấm Hủy.",
     "—",
     "- Hộp thoại đóng, phiếu vẫn còn nguyên trong danh sách."),

    (4, "Xóa phiếu thì xóa cả dòng chi tiết", "P1",
     "Phiếu Đang tạo có 3 dòng chi tiết.",
     "1. Xóa phiếu.\n2. Mở màn Tổng hợp tiền về ngân hàng và tìm theo mã phiếu vừa xóa.",
     "Mã phiếu vừa xóa",
     "- Không còn dòng nào của phiếu đó ở màn Tổng hợp (dù trước đó phiếu chưa duyệt nên vốn "
     "cũng không hiển thị)."),

    (5, "Xóa phiếu đã bị người khác xóa trước đó", "P1",
     "Mở danh sách ở 2 tab; tab 2 đã xóa phiếu X.",
     "1. Ở tab 1 bấm Xóa phiếu X và xác nhận.",
     "—",
     "- Hệ thống báo lỗi rõ ràng (dữ liệu đã thay đổi), tự tải lại danh sách cho khớp thực tế.\n"
     "- Không treo trang, không xóa nhầm phiếu khác."),

    (6, "Nút Xóa của phiếu đã duyệt", "P0",
     "Phiếu Đã duyệt.",
     "1. Quan sát cột Hành động và thanh nút màn chi tiết.",
     "—",
     "- Không có nút Xóa ở cả hai nơi."),
]

SEC_8 = [
    (1, "Tích ô Không báo tiền về ở màn chi tiết", "P0",
     "Phiếu Đã duyệt có 1 dòng chi tiết 1.500.000 đang hiển thị ở màn Tổng hợp.",
     "1. Mở màn chi tiết, kéo tới khối “Đánh dấu không báo tiền về”.\n"
     "2. Tích ô ở cột Không báo tiền về.",
     "—",
     "- Hệ thống báo “Cập nhật thành công.” ngay, không cần bấm nút lưu nào khác."),

    (2, "Dòng đã đánh dấu biến mất khỏi màn Tổng hợp", "P0",
     "Tiếp theo tình huống trên.",
     "1. Mở màn Tổng hợp tiền về ngân hàng.\n2. Tìm theo mã phiếu vừa đánh dấu.",
     "Mã phiếu đã đánh dấu",
     "- Không còn dòng nào của phiếu đó ở màn Tổng hợp.\n"
     "⚠️ Đây là tác động quan trọng nhất của cờ này."),

    (3, "Bỏ tích thì dòng xuất hiện trở lại", "P1",
     "Dòng đang được đánh dấu.",
     "1. Mở màn chi tiết, bỏ tích ô.\n2. Mở lại màn Tổng hợp và tìm theo mã phiếu.",
     "—",
     "- Dòng xuất hiện trở lại đúng số tiền như trước."),

    (4, "Ô tích bị khóa khi không có quyền thao tác", "P0",
     "Tài khoản C chỉ có quyền xem của tổng công ty.",
     "1. Đăng nhập bằng C, mở màn chi tiết một phiếu Đã duyệt.\n2. Thử tích ô.",
     "—",
     "- Ô tích bị khóa, không tích được.\n"
     "- Không có thông báo lỗi kỹ thuật hiện ra."),

    (5, "Đánh dấu Không báo tiền về ngay lúc nhập phiếu", "P1",
     "Đang ở form Tạo mới.",
     "1. Tích ô Không báo tiền về ở dòng chi tiết (kéo cuộn ngang để thấy cột).\n2. Lưu và duyệt.",
     "—",
     "- Phiếu lưu và duyệt thành công.\n"
     "- Dòng đó không xuất hiện ở màn Tổng hợp tiền về ngân hàng."),

    (6, "Ghi lịch sử khi tạo mới", "P0",
     "Vừa lập một phiếu mới.",
     "1. Mở cửa sổ Lịch sử của phiếu.",
     "—",
     "- Có một mốc “Tạo mới” ghi đúng người thực hiện kèm phòng ban và thời điểm."),

    (7, "Ghi lịch sử khi duyệt", "P0",
     "Phiếu vừa được duyệt.",
     "1. Mở cửa sổ Lịch sử.",
     "—",
     "- Có mốc “Thay đổi trạng thái” ghi rõ Đang tạo → Đã duyệt kèm ghi chú đã ghi bút toán "
     "vào sổ cái.\n"
     "- Các mốc sắp xếp mới nhất lên trên."),

    (8, "Ghi lịch sử khi sửa: chỉ ghi phần đã đổi", "P0",
     "Phiếu Đang tạo, chỉ sửa ô Diễn giải từ “A” thành “B”.",
     "1. Sửa và lưu.\n2. Mở Lịch sử.",
     "Diễn giải: A → B",
     "- Mốc mới chỉ liệt kê trường Diễn giải với giá trị cũ và giá trị mới.\n"
     "- Không liệt kê các trường không đổi."),

    (9, "Ghi lịch sử thay đổi bảng chi tiết theo từng dòng", "P1",
     "Phiếu Đang tạo có 2 dòng; sửa số tiền dòng 1 và xóa dòng 2.",
     "1. Sửa và lưu.\n2. Mở Lịch sử.",
     "—",
     "- Lịch sử ghi rõ dòng nào bị sửa cột nào, dòng nào bị bỏ.\n"
     "- Không in lại toàn bộ bảng chi tiết như một khối."),

    (10, "Lịch sử hiển thị bằng nhãn tiếng Việt", "P0",
     "Phiếu có thay đổi Loại thu, Ngân hàng, Tài khoản nợ.",
     "1. Mở Lịch sử và đọc phần giá trị cũ → giá trị mới.",
     "—",
     "- Hiển thị chữ như “Thu bán hàng”, “Đã duyệt”, tên ngân hàng, số hiệu và tên tài khoản.\n"
     "⚠️ Không được hiển thị con số mã nội bộ."),

    (11, "Phiếu chưa có lịch sử", "P2",
     "Phiếu được tạo bằng dữ liệu mẫu, chưa có thao tác nào được ghi.",
     "1. Mở khối Lịch sử ở màn chi tiết.",
     "—",
     "- Hiển thị “Chưa có lịch sử thao tác”, không báo lỗi."),

    (12, "Mở lịch sử từ hai nơi", "P1",
     "Phiếu Đã duyệt có nhiều mốc lịch sử.",
     "1. Mở lịch sử từ menu ba chấm ở danh sách.\n"
     "2. Mở màn chi tiết, bấm “Xem lịch sử”.",
     "—",
     "- Cả hai nơi hiển thị cùng một danh sách mốc, không lệch nhau."),

    (13, "Người chỉ có quyền xem vẫn xem được lịch sử", "P1",
     "Tài khoản C chỉ có quyền xem của tổng công ty.",
     "1. Đăng nhập bằng C, mở lịch sử một phiếu Đã duyệt.",
     "—",
     "- Xem được đầy đủ các mốc lịch sử (lịch sử không cần quyền riêng)."),
]

SEC_9 = [
    (1, "Tải file mẫu import", "P0",
     "Tài khoản có quyền Quản lý phiếu báo có.",
     "1. Bấm Import Excel.\n2. Bấm “Tải file mẫu”.\n3. Mở file vừa tải bằng Excel.",
     "—",
     "- Tải về file Mau_import_phieu_bao_co.xlsx.\n"
     "- File có 1 dòng tiêu đề nền xanh chữ trắng và 1 dòng ví dụ, có kẻ viền.\n"
     "- Ô Số tiền là ô SỐ có dấu ngăn cách nghìn; ô Ngày hạch toán hiển thị dạng dd/mm/yyyy; "
     "ô Số tài khoản hiển thị đủ số, không bị rút gọn thành dạng lũy thừa."),

    (2, "Nạp file mẫu lên bảng xem trước", "P0",
     "Đã tải file mẫu và giữ nguyên dòng ví dụ.",
     "1. Bấm “Chọn file Excel”, chọn chính file mẫu.\n2. Bấm “Load lên bảng”.",
     "File mẫu chưa sửa",
     "- Bảng xem trước hiển thị đúng 1 dòng dữ liệu với 8 cột.\n"
     "- Ô Tổng hiển thị 1.\n"
     "⚠️ File mẫu do hệ thống phát ra phải nạp được — báo “File không đúng mẫu” là lỗi."),

    (3, "Kiểm tra dữ liệu (Validate) với file toàn dòng hợp lệ", "P0",
     "File 2 dòng đều hợp lệ: số tiền 1.000.000 và 2.000.000, ngày hạch toán 05/09/2026, "
     "mã ngân hàng VIETINBANK, số tài khoản 116000142872, chi nhánh có thật, loại tiền VNĐ.",
     "1. Nạp file lên bảng.\n2. Bấm Validate.",
     "2 dòng hợp lệ",
     "- Hệ thống báo “Kiểm tra xong: 2 dòng hợp lệ, 0 dòng lỗi”.\n"
     "- Nút Import mở khóa."),

    (4, "Kiểm tra dữ liệu với dòng sai số tiền", "P0",
     "File có 1 dòng số tiền để trống và 1 dòng số tiền bằng 0.",
     "1. Nạp file, bấm Validate.",
     "Số tiền: trống và 0",
     "- Cả 2 dòng đều bị đánh dấu lỗi với lý do “Số tiền phải lớn hơn 0”.\n"
     "- Số dòng hợp lệ hiển thị đúng phần còn lại."),

    (5, "Kiểm tra dữ liệu với ngày không tồn tại", "P0",
     "File có dòng ghi ngày hạch toán 31/02/2026.",
     "1. Nạp file, bấm Validate.",
     "Ngày hạch toán: 31/02/2026",
     "- Dòng bị đánh dấu lỗi “Ngày hạch toán không đúng định dạng”.\n"
     "⚠️ Ngày tràn tháng phải bị chặn, không được tự đổi thành 03/03/2026."),

    (6, "Kiểm tra dữ liệu với mã ngân hàng sai", "P0",
     "File có dòng ghi mã ngân hàng XYZBANK không có trong danh mục.",
     "1. Nạp file, bấm Validate.",
     "Mã ngân hàng: XYZBANK",
     "- Dòng bị đánh dấu lỗi “Ngân hàng không tồn tại”."),

    (7, "Kiểm tra dữ liệu với số tài khoản sai", "P0",
     "File có dòng ghi số tài khoản 999999999 chưa khai trong danh mục tài khoản công ty.",
     "1. Nạp file, bấm Validate.",
     "Số tài khoản: 999999999",
     "- Dòng bị đánh dấu lỗi “Số tài khoản không tồn tại”."),

    (8, "Kiểm tra dữ liệu với chi nhánh và loại tiền sai", "P1",
     "File có dòng ghi chi nhánh “CN Khong Co” và loại tiền “ABC”.",
     "1. Nạp file, bấm Validate.",
     "Chi nhánh: CN Khong Co; Loại tiền: ABC",
     "- Dòng hiển thị đủ cả 2 lỗi: “Tên chi nhánh không tồn tại” và “Loại tiền không tồn tại”."),

    (9, "Kiểm tra dữ liệu với tỷ giá âm", "P1",
     "File có dòng ghi tỷ giá -5.",
     "1. Nạp file, bấm Validate.",
     "Tỷ giá: -5",
     "- Dòng bị đánh dấu lỗi “Tỷ giá phải lớn hơn 0”.\n"
     "- Dòng bỏ trống tỷ giá thì KHÔNG bị coi là lỗi."),

    (10, "Số tiền có dấu ngăn cách nghìn", "P0",
     "File có dòng ghi số tiền “1.500.000” và dòng ghi “1,234.56”.",
     "1. Nạp file, bấm Validate rồi bấm Import.",
     "1.500.000 và 1,234.56",
     "- Cả 2 dòng đều hợp lệ.\n"
     "- Phiếu tạo ra có số tiền đúng 1.500.000 và 1.234,56, không bị hiểu thành 1,5 hay 1.234."),

    (11, "Lọc chỉ dòng lỗi", "P1",
     "File 10 dòng trong đó 3 dòng lỗi, đã bấm Validate.",
     "1. Bấm nút “Chỉ dòng lỗi”.",
     "—",
     "- Bảng chỉ còn 3 dòng lỗi kèm lý do, giúp sửa nhanh."),

    (12, "Sửa dòng lỗi ngay trên bảng rồi kiểm tra lại", "P1",
     "File có 1 dòng sai mã ngân hàng.",
     "1. Sửa ô Mã ngân hàng trên bảng thành VIETINBANK.\n2. Bấm Validate lại.",
     "Mã ngân hàng: VIETINBANK",
     "- Dòng chuyển thành hợp lệ, số dòng lỗi giảm tương ứng."),

    (13, "Import tạo phiếu đã duyệt và ghi sổ", "P0",
     "File 2 dòng hợp lệ; đây là dữ liệu test đã thống nhất được phép ghi sổ.",
     "1. Bấm Validate rồi bấm Import.\n2. Mở danh sách và mở 1 phiếu vừa tạo.",
     "2 dòng hợp lệ",
     "- Hệ thống báo “Import thành công 2 phiếu báo có!”.\n"
     "- Danh sách có thêm 2 phiếu, cả hai ở trạng thái ĐÃ DUYỆT.\n"
     "- Phiếu có loại thu Thu bán hàng, tài khoản nợ 1121, 1 dòng chi tiết gắn khách "
     "KHÁCH KHÔNG RÕ và tài khoản có 1311.\n"
     "- Sổ kế toán có bút toán tương ứng.\n"
     "⚠️ Không có bước duyệt tay — import là ghi sổ ngay."),

    (14, "Import file vừa có dòng hợp lệ vừa có dòng lỗi", "P0",
     "File 5 dòng: 3 hợp lệ, 2 lỗi.",
     "1. Bấm Validate rồi bấm Import.",
     "5 dòng (3 hợp lệ / 2 lỗi)",
     "- Hệ thống tạo 3 phiếu và báo rõ 2 dòng lỗi.\n"
     "- Dòng lỗi không tạo phiếu, không sinh bút toán."),

    (15, "Import khi không có dòng nào hợp lệ", "P1",
     "File 3 dòng đều sai số tiền.",
     "1. Bấm Validate.",
     "3 dòng lỗi",
     "- Hệ thống báo không có dòng nào hợp lệ và không cho bấm Import."),

    (16, "Import file quá 500 dòng", "P1",
     "File có 600 dòng dữ liệu.",
     "1. Nạp file và bấm Validate.",
     "600 dòng",
     "- Hệ thống từ chối, báo file quá lớn (tối đa 500 dòng) và yêu cầu tách file.\n"
     "- Không tạo phiếu nào."),

    (17, "Phiếu tạo bằng import hiện ở màn Tổng hợp tiền về ngân hàng", "P0",
     "Vừa import 2 phiếu thành công.",
     "1. Mở màn Tổng hợp tiền về ngân hàng, tìm theo mã phiếu vừa import.",
     "Mã phiếu vừa import",
     "- Cả 2 dòng đều xuất hiện với khách hàng KHÁCH KHÔNG RÕ và trạng thái "
     "“Chưa điều chỉnh hết công nợ”."),

    (18, "Lịch sử của phiếu tạo bằng import", "P2",
     "Phiếu vừa import.",
     "1. Mở cửa sổ Lịch sử của phiếu.",
     "—",
     "- Có mốc ghi nhận phiếu được tạo bằng chức năng import, kèm người thực hiện và thời điểm."),
]

SEC_10 = [
    (1, "Chỉ hiển thị dòng của phiếu đã duyệt", "P0",
     "Có 1 phiếu Đang tạo và 1 phiếu Đã duyệt, cả hai đều có dòng gắn tài khoản 1311.",
     "1. Mở màn Tổng hợp, tìm lần lượt theo mã của hai phiếu.",
     "Mã 2 phiếu",
     "- Chỉ dòng của phiếu Đã duyệt xuất hiện.\n"
     "- Phiếu Đang tạo không có dòng nào ở màn này."),

    (2, "Chỉ hiển thị dòng có tài khoản công nợ", "P0",
     "Phiếu Đã duyệt có 2 dòng: 1 dòng tài khoản 1311, 1 dòng tài khoản khác ngoài nhóm "
     "1311/1312/3311.",
     "1. Mở màn Tổng hợp, tìm theo mã phiếu.",
     "Mã phiếu",
     "- Chỉ hiển thị 1 dòng (dòng tài khoản 1311).\n"
     "- Dòng còn lại không xuất hiện."),

    (3, "Không hiển thị dòng của công ty khác", "P0",
     "Người dùng thuộc công ty 1; có phiếu Đã duyệt của công ty 4.",
     "1. Mở màn Tổng hợp, tìm theo mã phiếu của công ty 4.",
     "Mã phiếu công ty 4",
     "- Không có kết quả nào.\n"
     "⚠️ Màn này luôn giới hạn theo công ty, không phụ thuộc quyền xem của tổng công ty."),

    (4, "Cột Số tiền chưa điều chỉnh và Trạng thái", "P0",
     "Dòng có số tiền 5.654.654 và chưa được điều chỉnh công nợ lần nào.",
     "1. Mở màn Tổng hợp, tìm theo mã phiếu.",
     "—",
     "- Cột Số tiền hiển thị 5.654.654, cột Số tiền chưa điều chỉnh cũng 5.654.654.\n"
     "- Cột Trạng thái hiển thị nhãn vàng “Chưa điều chỉnh hết công nợ”.\n"
     "- Ô tích ở cột Điều chỉnh công nợ có thể chọn được."),

    (5, "Dòng đã điều chỉnh hết công nợ", "P0",
     "Dòng đã được điều chỉnh hết bằng phiếu yêu cầu điều chỉnh công nợ.",
     "1. Tìm dòng đó trên màn Tổng hợp.",
     "—",
     "- Cột Số tiền chưa điều chỉnh bằng 0.\n"
     "- Trạng thái hiển thị nhãn xanh “Đã điều chỉnh hết công nợ”.\n"
     "- Cột Điều chỉnh công nợ hiển thị dấu gạch ngang, không có ô tích."),

    (6, "Tích chọn nhiều dòng của cùng một phiếu", "P0",
     "Một phiếu Đã duyệt có 3 dòng đều còn tiền chưa điều chỉnh.",
     "1. Tích lần lượt cả 3 dòng.",
     "—",
     "- Cả 3 ô tích đều được chọn, không có cảnh báo nào."),

    (7, "Chặn tích dòng của hai phiếu khác nhau", "P0",
     "Màn Tổng hợp có dòng của phiếu X và phiếu Y, cả hai đều còn tiền.",
     "1. Tích một dòng của phiếu X.\n2. Tích tiếp một dòng của phiếu Y.",
     "—",
     "- Hệ thống báo “Không thể chọn 2 phiếu báo có khác nhau! Vui lòng bỏ chọn dòng cũ trước.”\n"
     "- Ô tích của dòng phiếu Y trở lại trạng thái chưa chọn (không được hiện dấu tích).\n"
     "⚠️ Đây là lỗi từng gặp: ô vẫn hiện dấu tích dù thao tác bị từ chối."),

    (8, "Bỏ tích rồi chọn phiếu khác", "P1",
     "Đang tích 1 dòng của phiếu X.",
     "1. Bỏ tích dòng đó.\n2. Tích một dòng của phiếu Y.",
     "—",
     "- Lần tích thứ hai thành công, không còn cảnh báo."),

    (9, "Bấm Tạo mới điều chỉnh công nợ khi chưa chọn dòng", "P0",
     "Chưa tích dòng nào.",
     "1. Bấm nút “Tạo mới điều chỉnh công nợ”.",
     "—",
     "- Hệ thống báo “Vui lòng chọn ít nhất một chi tiết báo có.” và không chuyển màn."),

    (10, "Chuyển sang màn tạo phiếu điều chỉnh công nợ", "P0",
     "Đã tích 2 dòng của cùng một phiếu.",
     "1. Bấm “Tạo mới điều chỉnh công nợ”.",
     "—",
     "- Hệ thống chuyển sang màn tạo phiếu yêu cầu điều chỉnh công nợ.\n"
     "- Màn mới đã có sẵn 2 dòng chi tiết báo có vừa chọn."),

    (11, "Đi từ màn chi tiết phiếu báo có sang điều chỉnh công nợ", "P0",
     "Phiếu Đã duyệt còn dòng chưa điều chỉnh hết.",
     "1. Mở màn chi tiết phiếu.\n2. Bấm “Tạo phiếu yêu cầu điều chỉnh công nợ”.\n"
     "3. Ở màn mới, bấm nút Quay lại.",
     "—",
     "- Bước 2 chuyển sang màn tạo phiếu điều chỉnh với các dòng còn tiền của phiếu.\n"
     "- Bước 3 quay về ĐÚNG màn chi tiết phiếu báo có ban đầu, không rơi về danh sách phiếu "
     "điều chỉnh công nợ."),

    (12, "Nút Tạo phiếu yêu cầu điều chỉnh công nợ bị ẩn khi đã điều chỉnh hết", "P1",
     "Phiếu Đã duyệt mà mọi dòng đều đã điều chỉnh hết công nợ.",
     "1. Mở màn chi tiết phiếu.",
     "—",
     "- Không có nút “Tạo phiếu yêu cầu điều chỉnh công nợ” ở thanh dưới."),

    (13, "Mở cửa sổ chọn trường xuất Excel", "P0",
     "Đang ở màn Tổng hợp.",
     "1. Bấm nút Xuất Excel.",
     "—",
     "- Cửa sổ “Chọn trường xuất file” mở ra, hiển thị “Đang chọn 10/10 trường”.\n"
     "- Dòng chú thích cho biết thứ tự cột trong file chạy theo thứ tự chọn."),

    (14, "Xuất Excel đủ 10 trường", "P0",
     "Đang lọc theo Hạch toán từ 01/08/2026 đến 31/08/2026, còn 120 dòng.",
     "1. Bấm Xuất Excel → giữ nguyên 10 trường → bấm Xuất file.\n2. Mở file tải về.",
     "—",
     "- Tải về file Tong-hop-tien-ve-ngan-hang.xlsx, hệ thống báo “Xuất Excel thành công.”\n"
     "- File có ĐỦ 120 dòng (không chỉ 10 dòng của trang đang xem).\n"
     "- Đầu file có logo và tiêu đề công ty, kèm dòng “Từ ngày 01/08/2026 đến ngày 31/08/2026”."),

    (15, "Xuất Excel với ít trường và theo thứ tự chọn", "P1",
     "Đang ở cửa sổ chọn trường.",
     "1. Bấm “Bỏ chọn hết”.\n2. Chọn lần lượt: Số tiền, Số báo có, Khách hàng.\n"
     "3. Bấm Xuất file.",
     "3 trường theo thứ tự Số tiền → Số báo có → Khách hàng",
     "- File chỉ có 3 cột, xếp đúng thứ tự đã chọn."),

    (16, "Định dạng ô số tiền trong file Excel", "P0",
     "File vừa xuất ở bước trên.",
     "1. Mở file, bấm vào một ô ở cột Số tiền.\n2. Thử dùng hàm tính tổng cho cột đó.",
     "—",
     "- Ô là ô SỐ (căn phải, có dấu ngăn cách nghìn), không phải chữ.\n"
     "- Hàm tính tổng ra kết quả đúng, Excel không cảnh báo “số đang ở dạng văn bản”."),

    (17, "Xuất Excel khi bộ lọc không có dữ liệu", "P2",
     "Lọc theo khoảng ngày không có dòng nào.",
     "1. Bấm Xuất Excel → Xuất file.",
     "—",
     "- File tải về có tiêu đề và dòng tiêu đề cột nhưng không có dòng dữ liệu.\n"
     "- Hệ thống không báo lỗi."),

    (18, "Mở chi tiết phiếu từ màn Tổng hợp", "P1",
     "Màn Tổng hợp đang hiển thị dữ liệu.",
     "1. Bấm vào một mã ở cột Số báo có.",
     "—",
     "- Mở đúng màn chi tiết của phiếu báo có chứa dòng đó."),
]

SEC_11 = [
    (1, "Lưu phiếu khi bỏ trống toàn bộ trường bắt buộc", "P0",
     "Đang ở form Tạo mới, xóa hết Ngân hàng, Tài khoản, giữ số tiền 0 và diễn giải trống.",
     "1. Bấm Lưu.",
     "—",
     "- Không rời màn, dữ liệu đã nhập còn nguyên.\n"
     "- Chữ đỏ hiện ngay dưới từng ô: “Bắt buộc chọn” dưới Ngân hàng và Tài khoản; "
     "“Số tiền phải lớn hơn 0” dưới ô Số tiền; “Bắt buộc nhập” dưới ô Diễn giải của dòng."),

    (2, "Số tiền bằng 0", "P0",
     "Dòng chi tiết để số tiền 0, các trường khác hợp lệ.",
     "1. Bấm Lưu.",
     "Số tiền: 0",
     "- Báo “Số tiền phải lớn hơn 0” ngay dưới ô Số tiền, không lưu.\n"
     "⚠️ Trước đây lỗi này không hiện — phải kiểm kỹ."),

    (3, "Số tiền âm", "P1",
     "Nhập số tiền -5.000 (nếu ô cho nhập dấu trừ).",
     "1. Bấm Lưu.",
     "Số tiền: -5.000",
     "- Hệ thống chặn, báo số tiền phải lớn hơn 0."),

    (4, "Số tiền có phần thập phân", "P1",
     "Nhập số tiền 1.234,56 với loại tiền ngoại tệ.",
     "1. Bấm Lưu, mở lại phiếu.",
     "Số tiền: 1.234,56",
     "- Lưu thành công, phiếu hiển thị đúng 1.234,56 (không làm tròn thành 1.235)."),

    (5, "Diễn giải chung đúng 500 ký tự", "P1",
     "Chuẩn bị chuỗi đúng 500 ký tự.",
     "1. Dán vào ô Diễn giải ở khối Thông tin chung, bấm Lưu.",
     "Chuỗi 500 ký tự",
     "- Lưu thành công, không báo lỗi."),

    (6, "Diễn giải chung 501 ký tự", "P0",
     "Chuẩn bị chuỗi 501 ký tự.",
     "1. Dán vào ô Diễn giải, bấm Lưu.",
     "Chuỗi 501 ký tự",
     "- Báo “Tối đa 500 ký tự” ngay dưới ô Diễn giải, không lưu."),

    (7, "Diễn giải của dòng chi tiết 501 ký tự", "P1",
     "Chuẩn bị chuỗi 501 ký tự.",
     "1. Dán vào ô Diễn giải của dòng, bấm Lưu.",
     "Chuỗi 501 ký tự",
     "- Báo “Tối đa 500 ký tự” ngay dưới ô đó."),

    (8, "Diễn giải của dòng để trống", "P0",
     "Dòng chi tiết đã có số tiền nhưng chưa nhập diễn giải.",
     "1. Bấm Lưu.",
     "—",
     "- Báo “Bắt buộc nhập” dưới ô Diễn giải của dòng."),

    (9, "Ngày hạch toán để trống", "P0",
     "Xóa trắng ô Ngày hạch toán.",
     "1. Bấm Lưu.",
     "—",
     "- Báo “Bắt buộc nhập” dưới ô Ngày hạch toán."),

    (10, "Gõ tay ngày hạch toán sai định dạng", "P1",
     "Ô Ngày hạch toán cho gõ tay.",
     "1. Gõ “31/13/2026” rồi bấm Lưu.",
     "31/13/2026",
     "- Hệ thống báo ngày không đúng định dạng, không lưu."),

    (11, "Ngày hạch toán trong quá khứ và tương lai", "P2",
     "Ngày hiện tại 05/09/2026.",
     "1. Chọn ngày 01/01/2025 và lưu.\n2. Sửa thành 31/12/2027 và lưu.",
     "01/01/2025 / 31/12/2027",
     "- Cả hai đều lưu được (màn không giới hạn khoảng ngày).\n"
     "- Ngày ghi sổ của bút toán bằng đúng ngày đã chọn."),

    (12, "Thu bán hàng nhưng xóa trắng khách hàng", "P0",
     "Loại thu Thu bán hàng, xóa giá trị ở ô Khách hàng của dòng.",
     "1. Bấm Lưu.",
     "—",
     "- Báo “Bắt buộc chọn” dưới ô Khách hàng."),

    (13, "Thu nhà cung cấp nhưng xóa trắng nhà cung cấp", "P0",
     "Loại thu Thu nhà cung cấp, ô Nhà cung cấp trống.",
     "1. Bấm Lưu.",
     "—",
     "- Báo “Bắt buộc chọn” dưới ô Nhà cung cấp.\n"
     "⚠️ Ràng buộc này chỉ có ở hệ thống mới, đừng đối chiếu với màn cũ."),

    (14, "Tài khoản có là công nợ, khách hàng cụ thể nhưng chưa chọn hợp đồng", "P0",
     "Dòng có tài khoản có 1311, khách hàng là TOYOTA MỸ ĐÌNH (khác KHÁCH KHÔNG RÕ), chưa chọn "
     "hợp đồng.",
     "1. Bấm Lưu.",
     "—",
     "- Báo “Bắt buộc chọn” dưới ô Số đơn hàng/Hợp đồng, không lưu."),

    (15, "Khách hàng là KHÁCH KHÔNG RÕ thì không bắt buộc hợp đồng", "P0",
     "Dòng có tài khoản có 1311, khách hàng KHÁCH KHÔNG RÕ, không chọn hợp đồng.",
     "1. Nhập số tiền, diễn giải rồi bấm Lưu.",
     "—",
     "- Lưu thành công, không đòi chọn hợp đồng.\n"
     "⚠️ Đây là luồng thường dùng nhất khi chưa biết tiền của ai."),

    (16, "Hợp đồng nguyên tắc không tích dư nợ đầu kì và chưa chọn phiếu yêu cầu xuất hàng", "P1",
     "Dòng gắn hợp đồng nguyên tắc, ô dư nợ đầu kì không tích, ô Phiếu YC xuất hàng trống.",
     "1. Bấm Lưu.",
     "—",
     "- Báo “Bắt buộc chọn” dưới ô Phiếu YC xuất hàng."),

    (17, "Loại thu Thu khác không bắt buộc khách hàng", "P1",
     "Loại thu Thu khác, xóa trắng ô Khách hàng, chọn tài khoản có, nhập tiền và diễn giải.",
     "1. Bấm Lưu.",
     "—",
     "- Lưu thành công (khách hàng không bắt buộc với loại thu này)."),

    (18, "Loại thu Thu khác chưa chọn tài khoản có", "P0",
     "Loại thu Thu khác, ô Số tài khoản có để trống.",
     "1. Bấm Lưu.",
     "—",
     "- Báo “Bắt buộc chọn” dưới ô Số tài khoản có.\n"
     "⚠️ Loại thu này không có tài khoản mặc định nên rất dễ quên."),

    (19, "Tỷ giá bằng 0 với loại tiền ngoại tệ", "P1",
     "Loại tiền USD, sửa tỷ giá thành 0.",
     "1. Bấm Lưu.",
     "Tỷ giá: 0",
     "- Hệ thống chặn, báo lỗi ở ô Tỷ giá; không lưu phiếu với tỷ giá 0."),

    (20, "Nhập chữ vào ô số tiền", "P2",
     "Ô Số tiền của dòng chi tiết.",
     "1. Gõ “abc” vào ô Số tiền.",
     "abc",
     "- Ô không nhận ký tự chữ, giữ nguyên giá trị số."),

    (21, "Ký tự đặc biệt và tiếng Việt có dấu trong Diễn giải", "P2",
     "Ô Diễn giải.",
     "1. Nhập “Thu tiền HĐ số 26/2026 – khách lẻ (đợt 1) &%$#”.\n2. Lưu và mở lại phiếu.",
     "Chuỗi có dấu và ký tự đặc biệt",
     "- Lưu và hiển thị lại đúng nguyên văn, không bị mất dấu, không bị cắt ký tự."),
]

SEC_12 = [
    (1, "Hai người cùng sửa một phiếu", "P1",
     "Phiếu Đang tạo được mở ở 2 tab bằng cùng tài khoản.",
     "1. Tab 1 sửa diễn giải thành “A” và lưu.\n2. Tab 2 (mở trước đó) sửa số tiền và lưu.",
     "—",
     "- Lần lưu sau ghi đè theo dữ liệu của tab 2; hệ thống không báo lỗi kỹ thuật.\n"
     "- Lịch sử ghi đủ 2 lần sửa."),

    (2, "Xóa phiếu trong lúc người khác đang mở màn Sửa", "P1",
     "Tab 1 đang ở màn Sửa phiếu X; tab 2 xóa phiếu X.",
     "1. Tab 1 bấm Lưu.",
     "—",
     "- Hệ thống báo dữ liệu không còn tồn tại, không tạo lại phiếu đã xóa."),

    (3, "Duyệt phiếu trong lúc người khác đang mở màn Sửa", "P0",
     "Tab 1 đang ở màn Sửa phiếu X; tab 2 duyệt phiếu X.",
     "1. Tab 1 bấm Lưu.",
     "—",
     "- Hệ thống từ chối, báo phiếu đã duyệt nên không sửa được.\n"
     "- Nội dung phiếu và bút toán đã ghi không bị thay đổi."),

    (4, "Danh sách tự tải lại sau thao tác bị từ chối", "P1",
     "Phiếu X vừa bị người khác duyệt; danh sách của bạn vẫn hiển thị trạng thái cũ.",
     "1. Bấm Xóa phiếu X và xác nhận.",
     "—",
     "- Hệ thống báo lỗi và tự tải lại danh sách; dòng phiếu X hiển thị trạng thái Đã duyệt và "
     "không còn nút Xóa."),

    (5, "Hai người cùng lập phiếu tại một thời điểm", "P1",
     "Hai tài khoản cùng công ty cùng bấm Lưu trong cùng vài giây.",
     "1. A bấm Lưu.\n2. B bấm Lưu gần như đồng thời.",
     "—",
     "- Hai phiếu được tạo với hai mã KHÁC NHAU, không phiếu nào bị lỗi.\n"
     "- Số thứ tự trong mã tăng liên tiếp."),

    (6, "Cô lập dữ liệu giữa hai công ty ở màn Tổng hợp", "P0",
     "Tài khoản D thuộc công ty 1, tài khoản A thuộc công ty 4.",
     "1. D mở màn Tổng hợp và ghi lại tổng số dòng.\n2. A mở màn Tổng hợp và ghi lại tổng số dòng.",
     "—",
     "- Hai tổng khác nhau; không tài khoản nào thấy dòng của công ty còn lại."),
]

SEC_13 = [
    (1, "Luồng đầy đủ: lập nháp → sửa → duyệt → đối chiếu công nợ", "P0",
     "Tài khoản A có quyền Quản lý phiếu báo có, thuộc công ty 1. Dữ liệu test đã thống nhất.",
     "1. Tạo mới phiếu: loại thu Thu bán hàng, ngân hàng MB, tài khoản 2591100125008, 1 dòng "
     "chi tiết khách KHÁCH KHÔNG RÕ, số tiền 1.500.000, diễn giải “E2E test”. Bấm Lưu.\n"
     "2. Mở lại phiếu bằng nút Sửa, đổi số tiền thành 2.000.000, bấm Lưu.\n"
     "3. Mở màn chi tiết, bấm Duyệt và xác nhận.\n"
     "4. Mở màn Tổng hợp tiền về ngân hàng, tìm theo mã phiếu.\n"
     "5. Tích dòng đó và bấm “Tạo mới điều chỉnh công nợ”.",
     "Số tiền: 1.500.000 → 2.000.000",
     "- Bước 1: phiếu tạo ở trạng thái Đang tạo, mã đúng định dạng.\n"
     "- Bước 2: cột Tổng PS đổi thành 2.000.000; lịch sử ghi 1 mốc sửa đúng trường Số tiền.\n"
     "- Bước 3: phiếu chuyển Đã duyệt, sổ kế toán có bút toán 2.000.000 cân Nợ = Có.\n"
     "- Bước 4: dòng xuất hiện với Số tiền chưa điều chỉnh 2.000.000, trạng thái "
     "“Chưa điều chỉnh hết công nợ”.\n"
     "- Bước 5: chuyển sang màn tạo phiếu điều chỉnh công nợ, mang theo đúng dòng đã chọn."),

    (2, "Luồng import: import sao kê → gán lại khách hàng", "P0",
     "File sao kê 2 dòng hợp lệ; tài khoản A có quyền Quản lý phiếu báo có.",
     "1. Bấm Import Excel, tải file mẫu, điền 2 dòng, nạp lên bảng.\n"
     "2. Bấm Validate rồi Import.\n"
     "3. Mở màn Tổng hợp, tìm theo mã 2 phiếu vừa tạo.\n"
     "4. Tích 1 dòng, bấm “Tạo mới điều chỉnh công nợ”.",
     "2 dòng sao kê hợp lệ",
     "- Bước 2: tạo 2 phiếu ở trạng thái Đã duyệt, sổ kế toán có bút toán tương ứng.\n"
     "- Bước 3: cả 2 dòng hiển thị với khách hàng KHÁCH KHÔNG RÕ.\n"
     "- Bước 4: chuyển sang màn điều chỉnh công nợ với dòng đã chọn."),

    (3, "Luồng phiếu ngoại tệ", "P1",
     "Danh mục có loại tiền USD tỷ giá 25.000.",
     "1. Tạo phiếu loại tiền USD, tỷ giá 25.000, 2 dòng chi tiết 2.000 và 1.000.\n"
     "2. Lưu và duyệt.\n3. Mở danh sách và mở màn chi tiết phiếu.",
     "2.000 USD và 1.000 USD",
     "- Cột Tổng PS hiển thị 3.000, cột Tỷ giá 25.000, cột Tổng PS VND 75.000.000.\n"
     "- Sổ kế toán ghi theo số tiền quy đổi."),

    (4, "Luồng thu nhà cung cấp", "P1",
     "Có nhà cung cấp với phiếu xuất trả hàng gắn hợp đồng mua.",
     "1. Tạo phiếu loại Thu nhà cung cấp, chọn nhà cung cấp, chọn phiếu xuất hàng.\n"
     "2. Nhập số tiền, diễn giải, lưu nháp.\n3. Mở lại phiếu và duyệt.",
     "—",
     "- Cột Hợp đồng mua và NVKD tự điền theo phiếu xuất.\n"
     "- Phiếu duyệt thành công, sổ kế toán ghi Có tài khoản 3311.\n"
     "⚠️ Đây là nhánh chưa có dữ liệu thật nhiều — cần test kỹ."),

    (5, "Luồng đánh dấu không báo tiền về", "P0",
     "Phiếu Đã duyệt có 2 dòng, cả hai đang hiện ở màn Tổng hợp.",
     "1. Mở màn chi tiết, tích Không báo tiền về cho dòng 1.\n"
     "2. Mở màn Tổng hợp, tìm theo mã phiếu.\n"
     "3. Quay lại chi tiết, bỏ tích.\n4. Mở lại màn Tổng hợp.",
     "—",
     "- Bước 2: chỉ còn dòng 2 xuất hiện.\n"
     "- Bước 4: cả 2 dòng xuất hiện trở lại.\n"
     "- Lịch sử ghi đủ 2 mốc bật và tắt cờ."),

    (6, "Luồng người dùng chỉ có quyền xem", "P1",
     "Tài khoản C chỉ có quyền Xem tất cả phiếu báo có của tổng công ty.",
     "1. Đăng nhập bằng C, mở danh sách, lọc theo ngân hàng.\n"
     "2. Mở màn chi tiết một phiếu Đã duyệt, xem lịch sử.\n"
     "3. Mở màn Tổng hợp và xuất Excel.",
     "—",
     "- Mọi thao tác xem đều thực hiện được.\n"
     "- Không nơi nào hiện nút Tạo mới, Sửa, Xóa, Duyệt, Import Excel."),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_1),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_2),
    ("III", "DANH SÁCH, SẮP XẾP, PHÂN TRANG & TUỲ CHỈNH", SEC_3),
    ("IV", "TẠO MỚI PHIẾU BÁO CÓ", SEC_4),
    ("V", "CHỈNH SỬA PHIẾU BÁO CÓ", SEC_5),
    ("VI", "DUYỆT PHIẾU & GHI SỔ KẾ TOÁN", SEC_6),
    ("VII", "XÓA PHIẾU", SEC_7),
    ("VIII", "KHÔNG BÁO TIỀN VỀ & LỊCH SỬ THAY ĐỔI", SEC_8),
    ("IX", "IMPORT EXCEL SAO KÊ", SEC_9),
    ("X", "TỔNG HỢP TIỀN VỀ NGÂN HÀNG & XUẤT EXCEL", SEC_10),
    ("XI", "RÀNG BUỘC NHẬP LIỆU", SEC_11),
    ("XII", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_12),
    ("XIII", "E2E FLOW", SEC_13),
]

build(output_file=OUT, sheet_name="Trang tính1",
      feature_name="Phiếu báo có - Cập nhật ngày 05/09/2026",
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
