# -*- coding: utf-8 -*-
"""Sinh file testcase Excel cho man "Phieu yeu cau chuyen hang" (phan he Tai chinh).

Nguon doc code 03/09/2026 (nhanh gop_db):
  BE  Modules/Finance/Routes/api.php (:185-220)
      Modules/Finance/Http/Controllers/V1/ProductTransferRequestController.php
      Modules/Finance/Services/ProductTransferRequestService.php
      Modules/Finance/Entities/ProductTransferRequest/ProductTransferRequest.php
      Modules/Finance/Http/Requests/ProductTransferRequest/ProductTransferRequestRequest.php
      Modules/Finance/Transformers/ProductTransferRequestResource/*.php
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (:1140-1144)
  FE  hrm-client/pages/finance/product-transfer-requests/index.vue
      .../create.vue · .../_id/{index,edit,print}.vue
      .../components/ProductTransferRequestForm.vue
      hrm-client/components/subsystem-menu/finance.js (:195-210)
  Anh that: pycch_shots/ (cong dev hrm-crm.eteksofts.com, 03/09/2026)

Chay:  python .plans/gop-db/finance-product-transfer-request/gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(os.path.exists(HERE) and 0 or 0,
                os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                             "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")
MODULE = "Phiếu yêu cầu chuyển hàng"

MENU = ("Phân hệ Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Điều chuyển > "
        "Phiếu điều chuyển hàng")

# ════════════════════════════════════════════════════ 1. KHỐI MÔ TẢ (9 mục)
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu yêu cầu chuyển hàng là chứng từ do người kinh doanh lập để đề nghị kho chuyển hàng "
     "về phục vụ một hoặc nhiều khách hàng. Màn hình cho phép: lập phiếu (Lưu nháp hoặc Lưu và "
     "gửi duyệt), sửa phiếu nháp, xóa phiếu nháp, xem chi tiết, in phiếu, xuất Excel danh sách, "
     "xem lịch sử thay đổi. Người giữ vai trò kế toán kho khi mở phiếu đang chờ duyệt sẽ có "
     "thêm hai nút: 'Không duyệt' (trả phiếu về cho người lập sửa lại) và 'Tổng hợp' (mở màn "
     "lập phiếu đề nghị xuất hàng ở cổng cũ, mở ở tab mới).\n"
     "Đường dẫn màn hình: " + MENU + ". Chỉ có duy nhất MỘT mục menu trỏ vào màn này — không có "
     "màn 'chờ duyệt' riêng, phiếu chờ duyệt nằm chung trong danh sách và lọc bằng ô Trạng thái."),

    ("2. Đối tượng được tính / hiển thị",
     "Danh sách hiển thị phiếu theo phạm vi quyền của người đăng nhập:\n"
     "- Là quản trị hệ thống, hoặc có quyền 'Xem yêu cầu chuyển hàng theo tổng công ty': thấy "
     "phiếu của mọi công ty.\n"
     "- Có quyền 'Xem yêu cầu chuyển hàng theo công ty': chỉ phiếu thuộc công ty của mình.\n"
     "- Có quyền 'Xem yêu cầu chuyển hàng theo phòng ban': phiếu thuộc các phòng ban mình được "
     "giao quản lý trong công ty mình, CỘNG THÊM mọi phiếu do chính mình lập.\n"
     "- Có quyền 'Xem yêu cầu chuyển hàng theo bộ phận': phiếu thuộc các bộ phận mình được giao "
     "quản lý trong công ty mình, CỘNG THÊM mọi phiếu do chính mình lập.\n"
     "- Không có quyền nào trong 4 quyền trên: chỉ thấy phiếu do chính mình lập.\n"
     "Đủ 13 trạng thái đều được hiển thị: Đã tiếp nhận, Chờ duyệt, Đang tạo, Đang đề nghị, "
     "Đang xuất kho, Đã xuất kho, Đang vận chuyển, Đang nhập kho (hai mã trạng thái khác nhau "
     "nhưng cùng tên hiển thị), Đã nhập kho, Đã nhập hàng, Đã phân bổ, Đã hủy."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu ở trạng thái 'Đang tạo' (nháp) của NGƯỜI KHÁC luôn bị ẩn, kể cả với quản trị hệ "
     "thống và người có quyền xem toàn tổng công ty. Mỗi người chỉ nhìn thấy nháp của chính "
     "mình. Đây là quy tắc luôn được áp dụng sau cùng, không bộ lọc nào gỡ bỏ được.\n"
     "- Người không xác định được thuộc công ty nào (chưa gắn hồ sơ nhân viên) mà chỉ có quyền "
     "xem theo công ty thì danh sách trả về RỖNG, không phải trả về các phiếu chưa có công ty.\n"
     "- Popup thêm hàng hoá chỉ nhận hàng hoá có thật trong danh mục; hàng tạm không thêm được "
     "vào phiếu và không có đường tạo hàng tạm trong popup này.\n"
     "- Hàng hoá đã có trên phiếu thì popup không cho thêm lần hai.\n"
     "- Cột 'Được nhận' ở màn chi tiết chỉ hiện khi phiếu đã ở trạng thái 'Đã phân bổ'; các "
     "trạng thái khác không có cột này."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô 'Ngày tạo từ' và 'Ngày tạo đến' lọc theo NGÀY TẠO PHIẾU (cột Ngày tạo trên lưới), "
     "không phải Ngày tiếp nhận và cũng không phải Ngày cập nhật.\n"
     "Mốc 'đến ngày' lấy trọn ngày: chọn 'Ngày tạo đến' là hôm nay thì phiếu lập lúc 16 giờ "
     "hôm nay vẫn nằm trong kết quả. Bỏ trống một trong hai ô thì phía đó không giới hạn.\n"
     "Màn hình KHÔNG có ô lọc theo Ngày tiếp nhận — muốn xem theo mốc này phải bật cột "
     "'Ngày tiếp nhận' rồi sắp xếp."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu gồm 3 tầng:\n"
     "- Tầng 1 (phiếu): mã yêu cầu sinh tự động dạng PYCCH-xxxxx, ngày lập, người lập, ghi chú, "
     "file đính kèm (PDF), trạng thái, người tiếp nhận + ngày tiếp nhận, ghi chú duyệt.\n"
     "- Tầng 2 (hàng hoá): mỗi dòng là một hàng hoá kèm đơn vị tính, giá niêm yết, số lượng tồn "
     "tham khảo theo kho đang chọn. Một hàng hoá chỉ được xuất hiện MỘT lần trong phiếu.\n"
     "- Tầng 3 (khách hàng cần hàng): mỗi hàng hoá có ít nhất một dòng khách hàng, gồm khách "
     "hàng, số lượng, ngày cần, ghi chú. Ô 'Tổng cộng' dưới mỗi hàng hoá là tổng số lượng của "
     "các dòng khách hàng thuộc hàng đó.\n"
     "Xóa một hàng hoá sẽ xóa theo toàn bộ dòng khách hàng của hàng đó."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- 'Tổng cộng' của một hàng hoá = cộng số lượng của tất cả dòng khách hàng thuộc hàng đó; "
     "dòng để trống số lượng được tính là 0.\n"
     "- Không cộng dồn giữa các hàng hoá khác nhau; phiếu không có dòng tổng cuối bảng.\n"
     "- Hàng hoá trùng nhau bị chặn ngay từ popup chọn hàng; nếu vẫn lọt xuống thì khi lưu hệ "
     "thống báo 'Hàng hóa bị trùng trong phiếu' và không lưu.\n"
     "- Cùng một khách hàng ĐƯỢC PHÉP xuất hiện nhiều dòng trong cùng một hàng hoá (khác ngày "
     "cần / khác ghi chú) — hệ thống không gộp và không chặn.\n"
     "- Ô 'SL tồn' chỉ để tham khảo, không bị cộng trừ theo số lượng đang nhập và KHÔNG chặn "
     "người dùng nhập số lượng vượt tồn."),

    ("7. Phân quyền cấp",
     "Bốn quyền quyết định phạm vi dữ liệu nhìn thấy (đặt tên đúng như trong hệ thống):\n"
     "- Xem yêu cầu chuyển hàng theo tổng công ty\n"
     "- Xem yêu cầu chuyển hàng theo công ty\n"
     "- Xem yêu cầu chuyển hàng theo phòng ban\n"
     "- Xem yêu cầu chuyển hàng theo bộ phận\n"
     "Một quyền thao tác:\n"
     "- Kế toán kho: mở được phiếu của người khác cùng công ty; với phiếu đang 'Chờ duyệt' và "
     "cùng công ty thì có thêm nút 'Không duyệt' và 'Tổng hợp'; đồng thời là nhóm nhận thông "
     "báo khi có phiếu mới được gửi duyệt.\n"
     "Vai trò quản trị hệ thống được coi như có đủ 4 quyền xem ở trên, NHƯNG với nút 'Không "
     "duyệt' / 'Tổng hợp' thì vẫn phải cùng công ty với phiếu mới hiện.\n"
     "Các thao tác Tạo mới / Sửa / Xóa / In / Xuất Excel / Lịch sử KHÔNG cần quyền riêng: ai "
     "đăng nhập cũng tạo được phiếu; Sửa và Xóa chỉ mở với phiếu 'Đang tạo' do CHÍNH MÌNH lập."),

    ("8. Cách tính các ô thống kê",
     "- Dòng 'Hiển thị a–b / N' dưới lưới: a là số thứ tự dòng đầu của trang đang xem, b là số "
     "thứ tự dòng cuối, N là tổng số phiếu khớp bộ lọc VÀ nằm trong phạm vi quyền.\n"
     "- Cột STT đánh theo trang: sang trang 2 với cỡ 10 dòng/trang thì STT bắt đầu từ 11.\n"
     "- Ô 'Tổng cộng' trong ô Khách hàng của form = tổng số lượng các dòng khách hàng của đúng "
     "hàng hoá đó, hiển thị dấu phẩy ngăn hàng nghìn (ví dụ 1,500).\n"
     "- Ô 'SL tồn' = tồn của kho đang chọn quy đổi theo đơn vị tính đang chọn: đổi sang đơn vị "
     "lớn hơn có hệ số 10 thì số tồn hiển thị bằng một phần mười. Chưa chọn kho thì hiển thị "
     "dấu gạch ngang.\n"
     "- Ô 'Giá niêm yết' đổi theo đơn vị tính đang chọn, chỉ để tham khảo, KHÔNG được lưu vào "
     "phiếu và không xuất hiện trên bản in."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này:\n"
     "- Ô tìm nhanh (ghi 'Tìm theo mã yêu cầu...') thực chất tìm theo mã yêu cầu HOẶC tên người "
     "tạo, và phải bấm nút 'Tìm kiếm' mới chạy. Ngược lại, mọi ô trong 'Tìm kiếm nâng cao' — kể "
     "cả ô gõ tay 'Tên/mã hàng hóa' — tự tìm ngay khi gõ, không cần bấm nút.\n"
     "- Cột 'Ngày cập nhật' có mũi tên sắp xếp nhưng hệ thống KHÔNG sắp theo cột này; bấm vào "
     "chỉ đưa danh sách về thứ tự mặc định (mới nhất trước). Chỉ 3 cột sắp xếp thật: Mã yêu "
     "cầu, Ngày tạo, Ngày tiếp nhận.\n"
     "- Nháp của người khác không bao giờ hiện, nên tổng số phiếu mà hai người cùng quyền nhìn "
     "thấy vẫn có thể lệch nhau.\n"
     "- Ngày cần hàng bắt buộc phải LỚN HƠN ngày hôm nay khi thêm mới; nhưng khi sửa phiếu cũ, "
     "dòng giữ nguyên ngày cũ (kể cả ngày đã qua) vẫn lưu được — chỉ dòng mới hoặc dòng vừa đổi "
     "ngày mới bị kiểm tra.\n"
     "- File đính kèm bắt buộc khi TẠO MỚI (ít nhất 1 file PDF), nhưng khi SỬA thì không bắt "
     "buộc chọn thêm file; file cũ vẫn giữ nguyên.\n"
     "- Bấm × trên file đã lưu là xóa VĨNH VIỄN ngay lúc đó, không chờ bấm Lưu.\n"
     "- Bấm 'Không duyệt' không phải là hủy phiếu: phiếu quay về trạng thái 'Đang tạo' để người "
     "lập sửa và gửi lại.\n"
     "- Bộ lọc được ghi nhớ 10 phút: rời màn rồi quay lại trong 10 phút thì điều kiện lọc cũ "
     "vẫn còn, dễ tưởng nhầm là mất dữ liệu."),
]

# ════════════════════════════════════════════════════ 2. PHÂN QUYỀN
ROLE_TCS = [
    ("00", "Không có quyền xem nào — chỉ thấy phiếu của chính mình", "P0",
     "Tài khoản A không có bất kỳ quyền nào trong nhóm 'Xem yêu cầu chuyển hàng theo ...', "
     "không phải quản trị hệ thống, không có quyền 'Kế toán kho'. A đã lập 6 phiếu; phòng ban "
     "của A có tổng 20 phiếu (14 phiếu của người khác).",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào " + MENU + "\n"
     "3. Đếm số phiếu ở dòng 'Hiển thị a–b / N'",
     "—",
     "- Tổng số phiếu N = 6, đúng bằng số phiếu A tự lập\n"
     "- Cột Người tạo của mọi dòng đều là tên A\n"
     "- Không có phiếu nào của 14 người khác trong phòng\n"
     "- Nút Tạo mới, Xuất Excel, Cấu hình cột vẫn hiện bình thường"),

    ("01", "Quyền 'Xem yêu cầu chuyển hàng theo bộ phận'", "P0",
     "Tài khoản B chỉ có quyền 'Xem yêu cầu chuyển hàng theo bộ phận', được giao quản lý bộ "
     "phận Kinh doanh 1 (12 phiếu, trong đó 2 phiếu nháp của người khác). B tự lập 3 phiếu, "
     "trong đó 1 phiếu thuộc bộ phận khác.",
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Vào " + MENU + "\n"
     "3. Đối chiếu danh sách với dữ liệu chuẩn bị",
     "—",
     "- Thấy 10 phiếu của bộ phận Kinh doanh 1 (12 trừ 2 nháp của người khác)\n"
     "- Thấy CẢ 3 phiếu do B lập, kể cả phiếu thuộc bộ phận khác\n"
     "- ⚠️ 2 phiếu nháp của người khác trong chính bộ phận mình vẫn KHÔNG hiện\n"
     "- Không thấy phiếu của bộ phận không được giao quản lý"),

    ("02", "Quyền 'Xem yêu cầu chuyển hàng theo phòng ban'", "P0",
     "Tài khoản C chỉ có quyền 'Xem yêu cầu chuyển hàng theo phòng ban', được giao quản lý "
     "phòng Kinh doanh (30 phiếu, trong đó 4 nháp của người khác) thuộc công ty 1. C tự lập "
     "2 phiếu.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Vào " + MENU + "\n"
     "3. Đối chiếu danh sách với dữ liệu chuẩn bị",
     "—",
     "- Thấy 26 phiếu của phòng Kinh doanh + 2 phiếu của chính C\n"
     "- Không thấy phiếu của phòng ban khác trong cùng công ty\n"
     "- ⚠️ Nháp của người khác trong chính phòng mình vẫn không hiện"),

    ("03", "Quyền 'Xem yêu cầu chuyển hàng theo công ty'", "P0",
     "Tài khoản D chỉ có quyền 'Xem yêu cầu chuyển hàng theo công ty', thuộc công ty 1. Công "
     "ty 1 có 120 phiếu (8 nháp của người khác); công ty 4 có 300 phiếu.",
     "1. Đăng nhập bằng tài khoản D\n"
     "2. Vào " + MENU + "\n"
     "3. Đếm tổng số phiếu",
     "—",
     "- Tổng số phiếu N = 112 (120 trừ 8 nháp của người khác)\n"
     "- Không có phiếu nào của công ty 4\n"
     "- ⚠️ Khác nhánh phòng ban / bộ phận: nhánh công ty KHÔNG cộng thêm phiếu của chính mình "
     "ở công ty khác (thực tế phiếu luôn mang công ty của người lập nên không lệch)"),

    ("04", "Quyền 'Xem yêu cầu chuyển hàng theo tổng công ty'", "P0",
     "Tài khoản E có quyền 'Xem yêu cầu chuyển hàng theo tổng công ty'. Toàn hệ thống có 2.972 "
     "phiếu, trong đó 15 nháp của người khác và 3 nháp của chính E.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Vào " + MENU + "\n"
     "3. Đếm tổng số phiếu",
     "—",
     "- Tổng N = 2.960 (2.972 trừ 15 nháp người khác, vẫn giữ 3 nháp của E)\n"
     "- Thấy phiếu của mọi công ty\n"
     "- Hiện đủ 13 tên trạng thái trong ô lọc Trạng thái"),

    ("05", "Quản trị hệ thống — xem như quyền tổng công ty", "P0",
     "Tài khoản F là quản trị hệ thống, KHÔNG được gán quyền 'Xem yêu cầu chuyển hàng theo "
     "tổng công ty'.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Vào " + MENU + "\n"
     "3. So tổng số phiếu với tài khoản E ở trường hợp trên",
     "—",
     "- F thấy phiếu của mọi công ty, phạm vi tương đương tài khoản E\n"
     "- ⚠️ Nháp của người khác vẫn bị ẩn với F"),

    ("06", "Người có nhiều quyền xem cùng lúc — lấy phạm vi rộng nhất", "P1",
     "Tài khoản G có ĐỒNG THỜI 'Xem yêu cầu chuyển hàng theo công ty' và 'Xem yêu cầu chuyển "
     "hàng theo bộ phận'.",
     "1. Đăng nhập bằng tài khoản G\n"
     "2. Vào " + MENU + "\n"
     "3. Kiểm tra có thấy phiếu của bộ phận khác trong cùng công ty không",
     "—",
     "- G thấy toàn bộ phiếu của công ty mình, không bị bó lại theo bộ phận\n"
     "- Thứ tự ưu tiên: tổng công ty > công ty > phòng ban > bộ phận"),

    ("07", "Quyền 'Kế toán kho' — mở được phiếu của người khác cùng công ty", "P0",
     "Tài khoản H có quyền 'Kế toán kho', thuộc công ty 4. Phiếu PYCCH-07365 do người khác lập, "
     "thuộc công ty 4, trạng thái Chờ duyệt.",
     "1. Đăng nhập bằng tài khoản H\n"
     "2. Mở phiếu PYCCH-07365 từ danh sách\n"
     "3. Quan sát các nút cuối màn chi tiết",
     "—",
     "- Mở được màn chi tiết, không bị chặn\n"
     "- Có nút 'In', 'Không duyệt', 'Tổng hợp', 'Quay lại'\n"
     "- Có khối 'Ghi chú duyệt' cho nhập, gắn dấu sao đỏ\n"
     "- Không có nút 'Sửa' (phiếu không phải nháp của H)"),

    ("08", "Quyền 'Kế toán kho' nhưng KHÁC công ty với phiếu", "P0",
     "Tài khoản K có quyền 'Kế toán kho', thuộc công ty 1. Phiếu PYCCH-07365 thuộc công ty 4, "
     "trạng thái Chờ duyệt, không phải K lập.",
     "1. Đăng nhập bằng tài khoản K\n"
     "2. Gõ thẳng đường dẫn màn chi tiết của phiếu PYCCH-07365 lên thanh địa chỉ\n"
     "3. Quan sát kết quả",
     "—",
     "- Hệ thống từ chối, báo không có quyền xem phiếu này và đưa về danh sách\n"
     "- ⚠️ Quyền 'Kế toán kho' chỉ có tác dụng trong phạm vi công ty của người dùng"),

    ("09", "Quản trị hệ thống khác công ty — vẫn không có nút Không duyệt", "P0",
     "Tài khoản F là quản trị hệ thống thuộc công ty 1. Phiếu PYCCH-07365 thuộc công ty 4, "
     "trạng thái Chờ duyệt.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Mở màn chi tiết phiếu PYCCH-07365\n"
     "3. Quan sát các nút cuối màn",
     "—",
     "- Xem được nội dung phiếu (quyền xem của quản trị là toàn hệ thống)\n"
     "- ⚠️ KHÔNG có nút 'Không duyệt' và 'Tổng hợp', không có khối 'Ghi chú duyệt' — vì phiếu "
     "khác công ty với người đang xem\n"
     "- Vẫn có nút 'In' và 'Quay lại'"),

    ("10", "Bỏ qua giao diện, gọi thẳng chức năng Không duyệt khi không đủ điều kiện", "P0",
     "Tài khoản A không có quyền 'Kế toán kho'. Phiếu PYCCH-07365 đang ở trạng thái Chờ duyệt, "
     "không phải A lập.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt cho phiếu PYCCH-07365, bỏ "
     "qua giao diện\n"
     "3. Mở lại phiếu kiểm tra trạng thái",
     "Ghi chú duyệt: 'test'",
     "- Hệ thống từ chối, báo 'Bạn không có quyền thực hiện thao tác này'\n"
     "- Phiếu vẫn ở trạng thái Chờ duyệt, không bị ghi ghi chú duyệt, không đổi người tiếp nhận\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),

    ("11", "Bỏ qua giao diện, gọi thẳng chức năng Sửa / Xóa phiếu của người khác", "P0",
     "Tài khoản A. Phiếu PYCCH-07340 ở trạng thái 'Đang tạo' do người khác lập (A không nhìn "
     "thấy trên danh sách nhưng biết mã).",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa rồi chức năng Xóa cho phiếu "
     "PYCCH-07340, bỏ qua giao diện\n"
     "3. Đăng nhập lại bằng người lập phiếu để kiểm tra",
     "—",
     "- Cả hai lần hệ thống đều từ chối: 'Chỉ sửa được phiếu Đang tạo do chính bạn lập' và "
     "'Chỉ xóa được phiếu Đang tạo do chính bạn lập'\n"
     "- Phiếu PYCCH-07340 còn nguyên, nội dung không đổi\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),

    ("12", "Bỏ qua giao diện, gọi thẳng chức năng Sửa phiếu đã gửi duyệt của chính mình", "P0",
     "Tài khoản A lập phiếu PYCCH-07361 và đã gửi duyệt (trạng thái Chờ duyệt).",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cho phiếu PYCCH-07361, bỏ qua giao "
     "diện\n"
     "3. Mở lại phiếu kiểm tra",
     "Ghi chú mới: 'sửa lén'",
     "- Hệ thống từ chối: 'Chỉ sửa được phiếu Đang tạo do chính bạn lập'\n"
     "- ⚠️ Điều kiện sửa là TRẠNG THÁI ĐANG TẠO + đúng người lập, thiếu một trong hai là không "
     "sửa được\n"
     "- Ghi chú: trường hợp này dành cho tester kỹ thuật"),
]

# ════════════════════════════════════════════════════ 3. SECTION NGHIỆP VỤ

S1 = [
    ("001", "Mở màn danh sách lần đầu — bố cục và các cột mặc định", "P0",
     "Tài khoản E (quyền xem tổng công ty), hệ thống có 2.972 phiếu, chưa từng chỉnh cấu hình "
     "cột trên màn này.",
     "1. Đăng nhập\n"
     "2. Vào " + MENU + "\n"
     "3. Chờ lưới nạp xong rồi quan sát",
     "—",
     "- Tiêu đề trang và tiêu đề lưới đều là 'Phiếu yêu cầu chuyển hàng'\n"
     "- Lưới có các cột: STT, Mã yêu cầu, Người tiếp nhận, Người tạo, Ngày tạo, Trạng thái, "
     "Hành động\n"
     "- Khối lọc phía trên có ô tìm nhanh ghi 'Tìm theo mã yêu cầu...', nút 'Tìm kiếm', "
     "'Làm mới', 'Cài đặt bộ lọc', 'Tìm kiếm nâng cao'\n"
     "- Thanh công cụ của lưới có 3 nút: 'Tạo mới', 'Xuất Excel' và nút biểu tượng cấu hình cột\n"
     "- Mặc định 10 dòng/trang, dòng đếm ghi 'Hiển thị 1–10 / 2972'"),

    ("002", "Thứ tự mặc định của danh sách", "P0",
     "Có phiếu tạo hôm nay và phiếu tạo tháng trước.",
     "1. Mở màn danh sách, không đụng vào cột sắp xếp\n"
     "2. So cột Ngày tạo giữa dòng 1 và dòng 10",
     "—",
     "- Phiếu mới nhất (Ngày tạo lớn nhất) nằm trên cùng\n"
     "- Ngày tạo giảm dần từ trên xuống"),

    ("003", "Chỉ có duy nhất một mục menu trỏ vào màn này", "P1",
     "Tài khoản E.",
     "1. Mở phân hệ Tài chính\n"
     "2. Mở nhóm 'Hàng hoá - Dịch vụ - Vận chuyển' rồi vào mục 'Điều chuyển'\n"
     "3. Rà toàn bộ các nhóm chức năng còn lại tìm mục trỏ tới màn Phiếu yêu cầu chuyển hàng",
     "—",
     "- Nhóm 'Điều chuyển' có đúng 2 chức năng: 'Phiếu điều chuyển hàng' và 'Phiếu chuyển hàng "
     "nhập thẳng'\n"
     "- 'Phiếu điều chuyển hàng' mở màn có tiêu đề 'Phiếu yêu cầu chuyển hàng'\n"
     "- Không còn mục nào khác trỏ vào cùng màn này"),

    ("004", "Thêm tham số lạ vào thanh địa chỉ", "P1",
     "Tài khoản B (chỉ quyền xem theo bộ phận), đang thấy 13 phiếu.",
     "1. Mở màn danh sách, ghi lại tổng số phiếu\n"
     "2. Thêm đuôi ?type=all vào cuối đường dẫn rồi nhấn Enter\n"
     "3. Đếm lại tổng số phiếu",
     "?type=all",
     "- Trang mở bình thường, không báo lỗi\n"
     "- ⚠️ Tổng số phiếu KHÔNG đổi, vẫn là 13 — tham số lạ không mở rộng được phạm vi dữ liệu"),

    ("005", "Bộ lọc được ghi nhớ khi quay lại trong 10 phút", "P1",
     "Tài khoản E.",
     "1. Chọn Trạng thái = 'Chờ duyệt' rồi chờ lưới lọc xong\n"
     "2. Bấm vào một mã yêu cầu để sang màn chi tiết\n"
     "3. Bấm 'Quay lại' (trong vòng 10 phút)",
     "Trạng thái: Chờ duyệt",
     "- Về lại danh sách, ô Trạng thái vẫn giữ 'Chờ duyệt'\n"
     "- Lưới vẫn chỉ hiện phiếu Chờ duyệt, không tự trở về danh sách đầy đủ"),

    ("006", "Bộ lọc hết hạn ghi nhớ sau 10 phút", "P2",
     "Tài khoản E vừa lọc Trạng thái = 'Chờ duyệt'.",
     "1. Lọc Trạng thái = 'Chờ duyệt'\n"
     "2. Chuyển sang màn khác và để quá 10 phút\n"
     "3. Quay lại màn Phiếu yêu cầu chuyển hàng",
     "Trạng thái: Chờ duyệt",
     "- Ô lọc trở về trống, lưới hiện lại toàn bộ phiếu trong phạm vi quyền"),

    ("007", "Trạng thái mở/đóng của khối tìm kiếm nâng cao được ghi nhớ", "P2",
     "Tài khoản E.",
     "1. Bấm 'Tìm kiếm nâng cao' để mở khối lọc\n"
     "2. Sang màn khác rồi quay lại trong 10 phút",
     "—",
     "- Khối lọc nâng cao vẫn đang mở, nút đổi chữ thành 'Ẩn tìm kiếm nâng cao'"),

    ("008", "Màn danh sách khi không có phiếu nào", "P1",
     "Tài khoản mới tạo, chưa lập phiếu nào, không có quyền xem nào.",
     "1. Đăng nhập\n"
     "2. Vào " + MENU,
     "—",
     "- Lưới hiện dòng chữ 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Dòng đếm ghi 'Không có phiếu nào.'\n"
     "- Nút 'Tạo mới' vẫn dùng được"),

    ("009", "Số lượng thông báo trên chuông sau khi có phiếu gửi duyệt", "P1",
     "Tài khoản H có quyền 'Kế toán kho' công ty 4. Tài khoản A cùng công ty 4 vừa lập và gửi "
     "duyệt 1 phiếu.",
     "1. Đăng nhập tài khoản H\n"
     "2. Mở chuông thông báo\n"
     "3. Bấm vào dòng thông báo mới nhất",
     "—",
     "- Có thông báo dạng '<Tên người lập> vừa tạo yêu cầu chuyển hàng: <mã phiếu>', mã phiếu "
     "in đậm\n"
     "- Bấm vào thông báo mở đúng màn chi tiết của phiếu đó"),

    ("010", "Người khác công ty không nhận thông báo phiếu gửi duyệt", "P1",
     "Tài khoản K có quyền 'Kế toán kho' nhưng thuộc công ty 1. Tài khoản A thuộc công ty 4 vừa "
     "gửi duyệt 1 phiếu.",
     "1. Đăng nhập tài khoản K\n"
     "2. Mở chuông thông báo",
     "—",
     "- Không có thông báo nào về phiếu vừa gửi của công ty 4"),
]

S2 = [
    ("001", "Ô tìm nhanh tìm theo mã yêu cầu", "P0",
     "Có phiếu PYCCH-07365 trong phạm vi quyền.",
     "1. Gõ '07365' vào ô tìm nhanh\n"
     "2. Bấm nút 'Tìm kiếm'",
     "Ô tìm nhanh: 07365",
     "- Lưới còn đúng các phiếu có mã chứa 07365\n"
     "- Dòng đếm cập nhật theo số kết quả"),

    ("002", "Ô tìm nhanh tìm được cả theo TÊN NGƯỜI TẠO", "P0",
     "Có 6 phiếu do 'Phạm Ngọc Thái' lập trong phạm vi quyền.",
     "1. Gõ 'Phạm Ngọc Thái' vào ô tìm nhanh\n"
     "2. Bấm 'Tìm kiếm'",
     "Ô tìm nhanh: Phạm Ngọc Thái",
     "- ⚠️ Dù ô ghi 'Tìm theo mã yêu cầu...' nhưng vẫn ra 6 phiếu của người này\n"
     "- Cột Người tạo của mọi dòng đều là Phạm Ngọc Thái"),

    ("003", "Ô tìm nhanh KHÔNG tự tìm khi đang gõ", "P0",
     "Danh sách đang hiện 2.960 phiếu.",
     "1. Gõ '07365' vào ô tìm nhanh\n"
     "2. Chờ 5 giây, KHÔNG bấm nút\n"
     "3. Quan sát lưới",
     "Ô tìm nhanh: 07365",
     "- Lưới KHÔNG đổi, vẫn hiện 2.960 phiếu\n"
     "- Chỉ khi bấm 'Tìm kiếm' danh sách mới lọc lại"),

    ("004", "Ô 'Tên/mã hàng hóa' TỰ tìm ngay khi gõ", "P0",
     "Có 4 phiếu chứa hàng hoá mã CH-TW-9250.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Gõ 'CH-TW-9250' vào ô 'Tên/mã hàng hóa'\n"
     "3. KHÔNG bấm nút Tìm kiếm, chỉ chờ",
     "Tên/mã hàng hóa: CH-TW-9250",
     "- ⚠️ Lưới tự lọc còn 4 phiếu mà không cần bấm nút\n"
     "- Đây là điểm khác biệt cố ý với ô tìm nhanh"),

    ("005", "Ô 'Tên/mã hàng hóa' tìm theo TÊN hàng hoá", "P1",
     "Có phiếu chứa hàng 'Keo vá lốp màu xanh 250 ml'.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Gõ 'Keo vá lốp' vào ô 'Tên/mã hàng hóa'",
     "Tên/mã hàng hóa: Keo vá lốp",
     "- Lưới hiện các phiếu có ít nhất một hàng hoá tên chứa 'Keo vá lốp'\n"
     "- Mở một phiếu bất kỳ trong kết quả thấy đúng hàng hoá này trong bảng"),

    ("006", "Lọc theo Trạng thái", "P0",
     "Phạm vi quyền có 2.500 phiếu 'Chờ duyệt' và 120 phiếu 'Đã phân bổ'.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Chọn Trạng thái = 'Chờ duyệt'",
     "Trạng thái: Chờ duyệt",
     "- Lưới còn 2.500 dòng, cột Trạng thái của mọi dòng đều ghi 'Chờ duyệt'\n"
     "- Không cần bấm nút Tìm kiếm"),

    ("007", "Danh sách trạng thái trong ô lọc", "P1",
     "Tài khoản E.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Bấm vào ô Trạng thái để mở danh sách",
     "—",
     "- Danh sách có đủ các tên: Đã tiếp nhận, Chờ duyệt, Đang tạo, Đang đề nghị, Đang xuất kho, "
     "Đã xuất kho, Đang vận chuyển, Đang nhập kho, Đã nhập kho, Đã nhập hàng, Đã phân bổ, Đã hủy\n"
     "- ⚠️ Tên 'Đang nhập kho' xuất hiện 2 lần (hai bước khác nhau của kho nhưng trùng tên hiển "
     "thị) — chọn dòng nào cũng chỉ lọc đúng bước tương ứng"),

    ("008", "Lọc Trạng thái = Đang tạo chỉ ra nháp của chính mình", "P0",
     "Tài khoản E có quyền xem tổng công ty, tự lập 3 phiếu nháp; toàn hệ thống có 18 phiếu nháp.",
     "1. Lọc Trạng thái = 'Đang tạo'\n"
     "2. Đếm kết quả và xem cột Người tạo",
     "Trạng thái: Đang tạo",
     "- ⚠️ Chỉ ra 3 phiếu, không phải 18\n"
     "- Cột Người tạo của cả 3 dòng đều là tên E"),

    ("009", "Lọc theo Người tạo", "P1",
     "Có 6 phiếu do 'Phạm Ngọc Thái' lập.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Chọn Người tạo = 'Phạm Ngọc Thái'",
     "Người tạo: Phạm Ngọc Thái",
     "- Lưới còn 6 dòng, cột Người tạo đều là Phạm Ngọc Thái"),

    ("010", "Lọc theo Người tiếp nhận", "P1",
     "Có 2 phiếu do 'Bùi Thị Thịnh' tiếp nhận.",
     "1. Mở 'Tìm kiếm nâng cao'\n"
     "2. Chọn Người tiếp nhận = 'Bùi Thị Thịnh'\n"
     "3. Bật cột 'Ngày tiếp nhận' nếu chưa hiện",
     "Người tiếp nhận: Bùi Thị Thịnh",
     "- Lưới còn 2 dòng, cột Người tiếp nhận đều là Bùi Thị Thịnh\n"
     "- Phiếu chưa có người tiếp nhận (hiển thị dấu gạch ngang) không nằm trong kết quả"),

    ("011", "Lọc khoảng ngày tạo — có cả hai mốc", "P0",
     "Có 8 phiếu tạo trong tháng 7 năm 2026 và 5 phiếu tạo tháng 8 năm 2026.",
     "1. Chọn 'Ngày tạo từ' = 01/07/2026\n"
     "2. Chọn 'Ngày tạo đến' = 31/07/2026",
     "Ngày tạo từ: 01/07/2026 · Ngày tạo đến: 31/07/2026",
     "- Lưới chỉ còn 8 phiếu, cột Ngày tạo đều nằm trong tháng 7/2026\n"
     "- Không có phiếu nào của tháng 8"),

    ("012", "Mốc 'Ngày tạo đến' lấy trọn ngày", "P0",
     "Có 1 phiếu tạo lúc 16:10 ngày 07/08/2026.",
     "1. Chọn 'Ngày tạo đến' = 07/08/2026, để trống 'Ngày tạo từ'\n"
     "2. Tìm phiếu tạo lúc 16:10 trong kết quả",
     "Ngày tạo đến: 07/08/2026",
     "- ⚠️ Phiếu tạo lúc 16:10 ngày 07/08/2026 VẪN nằm trong kết quả (không bị cắt mất vì có "
     "giờ lớn hơn 0 giờ)"),

    ("013", "Chỉ đặt 'Ngày tạo từ'", "P1",
     "Có phiếu trải từ năm 2025 tới nay.",
     "1. Chọn 'Ngày tạo từ' = 01/08/2026, để trống ô còn lại",
     "Ngày tạo từ: 01/08/2026",
     "- Kết quả gồm mọi phiếu từ 01/08/2026 trở về sau, không giới hạn phía trên"),

    ("014", "Chỉ đặt 'Ngày tạo đến'", "P1",
     "Có phiếu trải từ năm 2025 tới nay.",
     "1. Chọn 'Ngày tạo đến' = 31/07/2026, để trống ô còn lại",
     "Ngày tạo đến: 31/07/2026",
     "- Kết quả gồm mọi phiếu từ 31/07/2026 trở về trước"),

    ("015", "Chọn khoảng ngày ngược (từ lớn hơn đến)", "P2",
     "Tài khoản E.",
     "1. Chọn 'Ngày tạo từ' = 31/08/2026\n"
     "2. Chọn 'Ngày tạo đến' = 01/08/2026",
     "Ngày tạo từ: 31/08/2026 · Ngày tạo đến: 01/08/2026",
     "- Lưới trống, hiện 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Không báo lỗi đỏ, không treo trang"),

    ("016", "Kết hợp nhiều điều kiện lọc cùng lúc", "P0",
     "Tài khoản E; có 2 phiếu 'Chờ duyệt' do Phạm Ngọc Thái lập trong tháng 7/2026.",
     "1. Chọn Trạng thái = 'Chờ duyệt'\n"
     "2. Chọn Người tạo = 'Phạm Ngọc Thái'\n"
     "3. Chọn Ngày tạo từ 01/07/2026 đến 31/07/2026",
     "Trạng thái: Chờ duyệt · Người tạo: Phạm Ngọc Thái · 01/07/2026–31/07/2026",
     "- Các điều kiện cộng dồn (VÀ), kết quả còn 2 phiếu thoả tất cả\n"
     "- Mỗi lần đổi một ô, lưới tự nạp lại"),

    ("017", "Nút 'Làm mới' xóa hết điều kiện lọc", "P0",
     "Đang lọc Trạng thái = 'Chờ duyệt', Người tạo = 'Phạm Ngọc Thái', ô tìm nhanh có chữ.",
     "1. Bấm nút 'Làm mới'\n"
     "2. Quan sát các ô lọc và lưới",
     "—",
     "- Tất cả ô lọc và ô tìm nhanh trở về trống\n"
     "- Lưới nạp lại đầy đủ theo phạm vi quyền, quay về trang 1\n"
     "- ⚠️ Phạm vi dữ liệu theo quyền KHÔNG đổi — 'Làm mới' chỉ xóa điều kiện lọc"),

    ("018", "Đổi điều kiện lọc khi đang ở trang 3", "P0",
     "Đang xem trang 3 của danh sách 2.960 phiếu.",
     "1. Chuyển tới trang 3\n"
     "2. Chọn Trạng thái = 'Đã phân bổ'",
     "Trạng thái: Đã phân bổ",
     "- Danh sách nhảy về TRANG 1 của kết quả mới\n"
     "- Không bị lỗi trang trắng do trang 3 vượt quá số trang mới"),

    ("019", "Cài đặt bộ lọc — bỏ bớt ô lọc hiển thị", "P1",
     "Tài khoản E, khối lọc nâng cao đang có 6 ô.",
     "1. Bấm 'Cài đặt bộ lọc'\n"
     "2. Bỏ tích 'Người tiếp nhận' và 'Ngày tạo đến'\n"
     "3. Bấm 'Lưu'",
     "Bỏ tích: Người tiếp nhận, Ngày tạo đến",
     "- Popup đóng, khối lọc nâng cao còn 4 ô\n"
     "- Rời màn rồi quay lại vẫn giữ cấu hình 4 ô này"),

    ("020", "Cài đặt bộ lọc — khôi phục mặc định", "P2",
     "Đã bỏ tích 2 ô lọc ở trường hợp trên.",
     "1. Bấm 'Cài đặt bộ lọc'\n"
     "2. Bấm 'Khôi phục mặc định'\n"
     "3. Bấm 'Lưu'",
     "—",
     "- Khối lọc nâng cao trở lại đủ 6 ô theo đúng thứ tự ban đầu"),

    ("021", "Đổi thứ tự ô lọc bằng kéo thả", "P2",
     "Popup 'Cài đặt bộ lọc' đang mở.",
     "1. Kéo dòng 'Ngày tạo từ' lên vị trí số 1\n"
     "2. Bấm 'Lưu'",
     "—",
     "- Khối lọc nâng cao hiện 'Ngày tạo từ' ở ô đầu tiên"),

    ("022", "Tìm từ khoá không khớp gì", "P1",
     "Tài khoản E.",
     "1. Gõ 'zzzz-khong-ton-tai' vào ô tìm nhanh\n"
     "2. Bấm 'Tìm kiếm'",
     "Ô tìm nhanh: zzzz-khong-ton-tai",
     "- Lưới hiện 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Không báo lỗi, các nút vẫn dùng được"),

    ("023", "Bộ lọc không phá vỡ phạm vi quyền", "P0",
     "Tài khoản B chỉ thấy 13 phiếu; hệ thống có 6 phiếu do 'Phạm Ngọc Thái' lập nhưng đều "
     "ngoài phạm vi của B.",
     "1. Đăng nhập tài khoản B\n"
     "2. Gõ 'Phạm Ngọc Thái' vào ô tìm nhanh rồi bấm 'Tìm kiếm'",
     "Ô tìm nhanh: Phạm Ngọc Thái",
     "- ⚠️ Kết quả RỖNG — tìm kiếm không mở rộng phạm vi dữ liệu ra ngoài quyền của B"),
]

S3 = [
    ("001", "Sắp xếp theo Mã yêu cầu tăng dần / giảm dần", "P0",
     "Danh sách đang ở thứ tự mặc định.",
     "1. Bấm vào tiêu đề cột 'Mã yêu cầu'\n"
     "2. Ghi lại thứ tự\n"
     "3. Bấm lần nữa vào cùng tiêu đề",
     "—",
     "- Lần 1: mã sắp tăng dần (PYCCH nhỏ nhất trên cùng)\n"
     "- Lần 2: đảo thành giảm dần\n"
     "- Danh sách quay về trang 1 sau mỗi lần đổi sắp xếp"),

    ("002", "Sắp xếp theo Ngày tạo", "P0",
     "Danh sách có phiếu nhiều ngày khác nhau.",
     "1. Bấm tiêu đề cột 'Ngày tạo'\n"
     "2. Kiểm tra dòng đầu và dòng cuối trang",
     "—",
     "- Ngày tạo sắp tăng dần; bấm lần nữa thì giảm dần\n"
     "- Giờ phút cũng được tính vào thứ tự (cùng ngày thì phiếu tạo sớm hơn đứng trước)"),

    ("003", "Sắp xếp theo Ngày tiếp nhận", "P1",
     "Đã bật cột 'Ngày tiếp nhận'; có phiếu đã tiếp nhận và phiếu chưa tiếp nhận.",
     "1. Bấm tiêu đề cột 'Ngày tiếp nhận'\n"
     "2. Quan sát vị trí các dòng chưa có ngày tiếp nhận",
     "—",
     "- Các dòng có ngày sắp đúng thứ tự tăng dần\n"
     "- Dòng chưa tiếp nhận (dấu gạch ngang) gom về một phía, không xen kẽ lộn xộn"),

    ("004", "Cột 'Ngày cập nhật' bấm sắp xếp KHÔNG có tác dụng", "P0",
     "Đã bật cột 'Ngày cập nhật'; danh sách có phiếu cập nhật ngày khác nhau.",
     "1. Ghi lại thứ tự 10 dòng đầu ở trạng thái mặc định\n"
     "2. Bấm tiêu đề cột 'Ngày cập nhật'\n"
     "3. So sánh lại thứ tự 10 dòng đầu",
     "—",
     "- ⚠️ Thứ tự KHÔNG đổi theo Ngày cập nhật mà quay về mặc định (mới tạo nhất trước)\n"
     "- Không báo lỗi; đây là hạn chế đã biết, chỉ 3 cột Mã yêu cầu / Ngày tạo / Ngày tiếp nhận "
     "sắp xếp thật"),

    ("005", "Sắp xếp vẫn giữ khi chuyển trang", "P1",
     "Đã sắp xếp theo Mã yêu cầu tăng dần.",
     "1. Bấm sang trang 2\n"
     "2. Quan sát mã yêu cầu dòng đầu trang 2",
     "—",
     "- Mã dòng đầu trang 2 lớn hơn mã dòng cuối trang 1\n"
     "- Mũi tên sắp xếp trên tiêu đề cột vẫn giữ chiều đã chọn"),

    ("006", "Chuyển trang không làm mất bộ lọc", "P0",
     "Đang lọc Trạng thái = 'Chờ duyệt', kết quả 2.500 phiếu.",
     "1. Bấm sang trang 5\n"
     "2. Kiểm tra cột Trạng thái và ô lọc",
     "—",
     "- Mọi dòng vẫn là 'Chờ duyệt'\n"
     "- Ô lọc Trạng thái vẫn giữ giá trị, không bị xoá\n"
     "- Không bị nhảy ngược về trang 1"),

    ("007", "Đổi số dòng/trang", "P0",
     "Đang xem 10 dòng/trang trên 2.960 phiếu.",
     "1. Đổi 'Số dòng/trang' sang 50\n"
     "2. Quan sát lưới và dòng đếm",
     "Số dòng/trang: 50",
     "- Lưới hiện 50 dòng, dòng đếm ghi 'Hiển thị 1–50 / 2960'\n"
     "- Danh sách quay về trang 1"),

    ("008", "Các cỡ trang được hỗ trợ", "P2",
     "Tài khoản E.",
     "1. Mở danh sách 'Số dòng/trang'",
     "—",
     "- Có đủ 5 lựa chọn: 5, 10, 20, 50, 100"),

    ("009", "STT đánh số theo trang", "P1",
     "Đang xem 10 dòng/trang.",
     "1. Sang trang 2\n"
     "2. Đọc cột STT dòng đầu và dòng cuối",
     "—",
     "- STT trang 2 chạy từ 11 đến 20, không bắt đầu lại từ 1"),

    ("010", "Nhảy tới trang cuối", "P1",
     "Danh sách có 2.960 phiếu, 10 dòng/trang.",
     "1. Bấm nút chuyển tới trang cuối\n"
     "2. Quan sát dòng đếm",
     "—",
     "- Trang cuối hiển thị đúng số dòng còn lại\n"
     "- Nút sang trang kế tiếp bị mờ đi, không bấm được"),

    ("011", "Mã yêu cầu là đường dẫn sang màn chi tiết", "P0",
     "Danh sách có phiếu PYCCH-07365.",
     "1. Bấm vào chữ 'PYCCH-07365' ở cột Mã yêu cầu",
     "—",
     "- Chuyển sang màn chi tiết đúng phiếu PYCCH-07365\n"
     "- Tiêu đề màn ghi 'Chi tiết phiếu yêu cầu chuyển hàng · PYCCH-07365'"),

    ("012", "Màu nhãn trạng thái", "P2",
     "Danh sách có cả phiếu 'Chờ duyệt', 'Đang tạo', 'Đã tiếp nhận', 'Đã hủy'.",
     "1. Quan sát cột Trạng thái",
     "—",
     "- 'Chờ duyệt', 'Đang tạo', 'Đã hủy' hiển thị nhãn màu đỏ\n"
     "- Các trạng thái còn lại hiển thị nhãn màu xanh"),

    ("013", "Nút thao tác trên dòng đổi theo trạng thái và người lập", "P0",
     "Tài khoản A có: 1 phiếu 'Đang tạo' do mình lập, 1 phiếu 'Chờ duyệt' do mình lập, 1 phiếu "
     "'Đã tiếp nhận' của người khác cùng công ty (A có quyền Kế toán kho).",
     "1. Quan sát cột Hành động của cả 3 dòng",
     "—",
     "- Dòng 'Đang tạo' của A: có nút Sửa (bút chì), Xóa (thùng rác) và menu ba chấm chứa In, "
     "Lịch sử\n"
     "- Dòng 'Chờ duyệt' của A: có nút Tổng hợp (dấu tích kép), In, Lịch sử — KHÔNG có Sửa/Xóa\n"
     "- Dòng 'Đã tiếp nhận': chỉ có In và Lịch sử\n"
     "- ⚠️ Nút không đủ điều kiện bị ẩn hẳn, không phải hiện mờ"),

    ("014", "Cấu hình cột — ẩn bớt cột", "P1",
     "Tài khoản E, lưới đang hiện đủ cột.",
     "1. Bấm nút biểu tượng cấu hình cột trên thanh công cụ\n"
     "2. Bỏ tích 'Người tiếp nhận'\n"
     "3. Bấm 'Lưu'",
     "Bỏ tích: Người tiếp nhận",
     "- Popup đóng, lưới không còn cột 'Người tiếp nhận'\n"
     "- Rời màn rồi quay lại vẫn giữ cấu hình này"),

    ("015", "Cấu hình cột — 3 cột bị khoá không bỏ được", "P1",
     "Popup 'Tuỳ chỉnh cột' đang mở.",
     "1. Thử bỏ tích 'STT', 'Mã yêu cầu', 'Hành động'",
     "—",
     "- Cả 3 dòng hiện biểu tượng ổ khoá, chữ mờ, không bỏ tích được\n"
     "- Các cột còn lại bỏ tích bình thường"),

    ("016", "Cấu hình cột — bật cột đang ẩn", "P1",
     "Cột 'Ngày tiếp nhận', 'Người cập nhật', 'Ngày cập nhật' đang ẩn mặc định.",
     "1. Mở popup 'Tuỳ chỉnh cột'\n"
     "2. Tích cả 3 cột trên\n"
     "3. Bấm 'Lưu'",
     "—",
     "- Lưới hiện thêm đủ 3 cột, dữ liệu khớp với màn chi tiết của từng phiếu"),

    ("017", "Đổi thứ tự cột bằng kéo thả", "P2",
     "Popup 'Tuỳ chỉnh cột' đang mở.",
     "1. Kéo dòng 'Trạng thái' lên ngay sau 'Mã yêu cầu'\n"
     "2. Bấm 'Lưu'",
     "—",
     "- Trên lưới, cột 'Trạng thái' nằm ngay sau cột 'Mã yêu cầu'"),

    ("018", "Cấu hình cột của màn này không ảnh hưởng màn khác", "P2",
     "Đã ẩn cột 'Người tiếp nhận' ở màn Phiếu yêu cầu chuyển hàng.",
     "1. Mở màn 'Phiếu chuyển hàng nhập thẳng'\n"
     "2. Quan sát các cột",
     "—",
     "- Màn kia giữ nguyên cấu hình cột riêng, không bị ẩn theo"),
]

S4 = [
    ("001", "Mở form Tạo mới — giá trị điền sẵn", "P0",
     "Tài khoản DNS Admin, hôm nay là 03/09/2026.",
     "1. Bấm nút 'Tạo mới' trên thanh công cụ\n"
     "2. Quan sát khối 'Thông tin chung'",
     "—",
     "- Tiêu đề màn: 'Thêm phiếu yêu cầu chuyển hàng'\n"
     "- 'Ngày lập' điền sẵn 03/09/2026 và KHÔNG sửa được\n"
     "- 'Người lập' điền sẵn tên người đang đăng nhập và KHÔNG sửa được\n"
     "- 'Ghi chú' để trống, nhập được\n"
     "- Bảng hàng hoá trống, hiện dòng 'Chưa có hàng hóa'\n"
     "- Ô 'Xem tồn theo kho' đã chọn sẵn một kho mặc định\n"
     "- Cuối trang có 3 nút: 'Lưu nháp', 'Lưu và gửi duyệt', 'Quay lại'"),

    ("002", "Các trường bắt buộc được đánh dấu", "P1",
     "Đang ở form Tạo mới.",
     "1. Quan sát các dấu sao đỏ trên form",
     "—",
     "- Tiêu đề khối 'Danh sách hàng hóa' có dấu sao đỏ\n"
     "- Tiêu đề cột 'ĐVT' và 'Khách hàng' có dấu sao đỏ\n"
     "- Tiêu đề khối 'File đính kèm (PDF)' có dấu sao đỏ\n"
     "- Ô 'Ghi chú' KHÔNG có dấu sao (không bắt buộc)"),

    ("003", "Thêm hàng hoá từ popup", "P0",
     "Đang ở form Tạo mới, bảng hàng hoá trống.",
     "1. Bấm dấu cộng ở góc phải tiêu đề bảng hàng hoá\n"
     "2. Trong popup 'Thêm hàng hoá', tích chọn 1 hàng\n"
     "3. Bấm 'Thêm 1 hàng hoá'\n"
     "4. Bấm 'Đóng'",
     "Hàng hoá: Cầu nâng vận thăng 1 Tấn (mã MUTR-S-VRC:25)",
     "- Popup mở toàn màn hình, có ô tìm nhanh và nút 'Tìm kiếm nâng cao'\n"
     "- Sau khi thêm, popup VẪN MỞ (không tự đóng) để chọn tiếp\n"
     "- Đóng popup thấy bảng có 1 dòng: STT 1, tên hàng, dòng phụ Model và Mã hàng\n"
     "- Ô ĐVT tự chọn sẵn đơn vị đầu tiên, ô 'Giá niêm yết' hiện giá theo đơn vị đó\n"
     "- Dòng khách hàng đầu tiên được tạo sẵn, các ô còn trống"),

    ("004", "Thêm nhiều hàng hoá một lần", "P1",
     "Popup 'Thêm hàng hoá' đang mở.",
     "1. Tích chọn 3 hàng hoá khác nhau\n"
     "2. Bấm 'Thêm 3 hàng hoá'\n"
     "3. Đóng popup",
     "3 hàng hoá bất kỳ",
     "- Bảng có 3 dòng, STT đánh 1, 2, 3\n"
     "- Mỗi dòng đều có sẵn 1 dòng khách hàng trống và đơn vị tính mặc định"),

    ("005", "Chặn thêm trùng hàng hoá", "P0",
     "Bảng đã có hàng 'Cầu nâng vận thăng 1 Tấn'.",
     "1. Mở lại popup 'Thêm hàng hoá'\n"
     "2. Tìm và thử chọn lại đúng hàng 'Cầu nâng vận thăng 1 Tấn'",
     "Hàng hoá: Cầu nâng vận thăng 1 Tấn",
     "- Popup đánh dấu hàng này là đã có trong phiếu và không cho tích chọn lại\n"
     "- Nếu vẫn thêm được thì hệ thống bỏ qua và báo 'Hàng hóa đã có trong phiếu: ...'\n"
     "- Bảng vẫn chỉ có 1 dòng cho hàng này"),

    ("006", "Popup không nhận hàng tạm", "P1",
     "Đang ở popup 'Thêm hàng hoá'.",
     "1. Quan sát các tab và nút trong popup\n"
     "2. Tìm đường thêm hàng tạm",
     "—",
     "- Popup chỉ có danh sách hàng hoá thật, KHÔNG có tab hay nút tạo hàng tạm\n"
     "- Nếu bằng cách nào đó một hàng tạm lọt vào, hệ thống bỏ qua và báo 'phiếu chuyển hàng "
     "chỉ nhận hàng hóa có trong danh mục (không nhận hàng tạm)'"),

    ("007", "Đổi đơn vị tính làm đổi giá niêm yết và số lượng tồn", "P0",
     "Bảng có 1 hàng hoá có 2 đơn vị tính: Cái (hệ số 1) và Thùng (hệ số 10). Kho đang chọn có "
     "tồn 100 Cái.",
     "1. Ghi lại 'Giá niêm yết' và 'SL tồn' khi đang chọn đơn vị 'Cái'\n"
     "2. Đổi ô ĐVT sang 'Thùng (x10)'\n"
     "3. So lại 2 ô trên",
     "ĐVT: Cái → Thùng (x10)",
     "- Nhãn đơn vị trong danh sách có ghi hệ số dạng 'Thùng (x10)'\n"
     "- 'SL tồn' đổi từ 100 xuống 10\n"
     "- 'Giá niêm yết' đổi theo đơn vị mới\n"
     "- Không phải chờ tải lại trang"),

    ("008", "Đổi kho ở ô 'Xem tồn theo kho'", "P0",
     "Bảng có 2 hàng hoá; kho Sài Gòn có tồn, kho Hà Nội không có tồn 2 hàng này.",
     "1. Mở ô 'Xem tồn theo kho'\n"
     "2. Chọn 'Kho Hà Nội'\n"
     "3. Quan sát cột 'SL tồn' của cả 2 dòng",
     "Xem tồn theo kho: Kho Hà Nội",
     "- Cột 'SL tồn' nạp lại theo kho mới cho tất cả dòng cùng lúc\n"
     "- Danh sách kho có cả kho tổng và các kho con thụt đầu dòng"),

    ("009", "Chọn giá trị rỗng ở ô 'Xem tồn theo kho'", "P1",
     "Bảng có hàng hoá, đang chọn 'Kho Sài Gòn'.",
     "1. Mở ô 'Xem tồn theo kho'\n"
     "2. Chọn dòng đầu tiên ghi 'Xem tồn'",
     "Xem tồn theo kho: (rỗng)",
     "- Cột 'SL tồn' của mọi dòng chuyển thành dấu gạch ngang\n"
     "- Không báo lỗi"),

    ("010", "Số lượng tồn bằng 0 không chặn nhập số lượng", "P1",
     "Hàng hoá 'Cầu nâng vận thăng 1 Tấn' có tồn 0 ở kho đang chọn.",
     "1. Thêm hàng này vào bảng\n"
     "2. Nhập số lượng 5 ở dòng khách hàng",
     "SL: 5",
     "- ⚠️ Hệ thống KHÔNG chặn, không cảnh báo vượt tồn\n"
     "- Ô 'SL tồn' vẫn hiện 0; số lượng vẫn nhập và lưu được"),

    ("011", "Chọn khách hàng cho dòng con", "P0",
     "Bảng có 1 hàng hoá với 1 dòng khách hàng trống.",
     "1. Bấm vào ô 'Khách hàng' của dòng con\n"
     "2. Trong popup 'Chọn khách hàng', bấm vào một khách hàng",
     "Khách hàng: 43TPHPAN-58 - KHÁCH HÀNG TEST",
     "- Popup có 3 ô tìm: 'Tên / Mã khách hàng', 'Mã số thuế', 'Số điện thoại'\n"
     "- Bấm chọn xong popup TỰ ĐÓNG\n"
     "- Ô khách hàng hiện dạng 'mã khách hàng - tên khách hàng'"),

    ("012", "Popup chọn khách hàng — tìm theo tên", "P1",
     "Popup 'Chọn khách hàng' đang mở, hệ thống có 17.193 khách hàng.",
     "1. Gõ 'KHÁCH HÀNG TEST' vào ô 'Tên / Mã khách hàng'\n"
     "2. Bấm 'Tìm kiếm'",
     "Tên / Mã khách hàng: KHÁCH HÀNG TEST",
     "- Danh sách còn các khách hàng có tên chứa từ khoá\n"
     "- Dòng đếm cập nhật theo số kết quả"),

    ("013", "Thêm nhiều dòng khách hàng cho cùng một hàng hoá", "P0",
     "Bảng có 1 hàng hoá với 1 dòng khách hàng đã điền.",
     "1. Bấm '+ Thêm khách hàng' 2 lần\n"
     "2. Điền đủ thông tin cho 2 dòng mới",
     "Dòng 1: SL 5 · Dòng 2: SL 3 · Dòng 3: SL 2",
     "- Hàng hoá có 3 dòng khách hàng xếp dọc\n"
     "- Ô 'Tổng cộng' dưới cùng hiện 10"),

    ("014", "Cùng một khách hàng ở nhiều dòng của một hàng hoá", "P1",
     "Bảng có 1 hàng hoá.",
     "1. Thêm 2 dòng khách hàng, chọn CÙNG một khách hàng\n"
     "2. Đặt ngày cần khác nhau cho 2 dòng\n"
     "3. Điền đủ số lượng và ghi chú rồi bấm 'Lưu nháp'",
     "Cùng khách hàng, ngày cần 10/09/2026 và 20/09/2026",
     "- ⚠️ Hệ thống CHO PHÉP, không báo trùng\n"
     "- Lưu thành công, mở lại phiếu thấy đủ 2 dòng"),

    ("015", "Xóa một dòng khách hàng", "P1",
     "Một hàng hoá đang có 3 dòng khách hàng.",
     "1. Bấm dấu × ở cuối dòng khách hàng thứ 2\n"
     "2. Quan sát bảng và ô 'Tổng cộng'",
     "—",
     "- Dòng thứ 2 biến mất ngay, không hỏi xác nhận\n"
     "- Ô 'Tổng cộng' trừ đi số lượng của dòng vừa xóa"),

    ("016", "Không cho xóa dòng khách hàng cuối cùng", "P0",
     "Một hàng hoá chỉ còn đúng 1 dòng khách hàng.",
     "1. Bấm dấu × ở cuối dòng khách hàng duy nhất",
     "—",
     "- Dòng KHÔNG bị xóa\n"
     "- Hệ thống báo 'Mỗi hàng hóa phải có ít nhất 1 dòng khách hàng — hãy xóa cả hàng hóa nếu "
     "không cần'"),

    ("017", "Xóa cả hàng hoá — có hỏi xác nhận", "P0",
     "Bảng có 2 hàng hoá, hàng số 1 có 3 dòng khách hàng.",
     "1. Bấm dấu trừ ở cột cuối của dòng hàng hoá số 1\n"
     "2. Đọc nội dung hộp xác nhận\n"
     "3. Bấm 'Xác nhận'",
     "—",
     "- Hộp thoại 'Xác nhận xóa hàng hóa' báo xóa hàng sẽ xóa toàn bộ dòng khách hàng của hàng đó\n"
     "- Sau khi xác nhận, bảng còn 1 dòng và STT đánh lại từ 1"),

    ("018", "Hủy hộp xác nhận xóa hàng hoá", "P1",
     "Hộp 'Xác nhận xóa hàng hóa' đang mở.",
     "1. Bấm 'Hủy'",
     "—",
     "- Hộp đóng, hàng hoá và các dòng khách hàng còn nguyên"),

    ("019", "Đính kèm file PDF hợp lệ", "P0",
     "Đang ở form Tạo mới, có sẵn file dinh-kem-mau.pdf.",
     "1. Cuộn xuống khối 'File đính kèm (PDF)'\n"
     "2. Bấm ô 'Thêm file'\n"
     "3. Chọn file dinh-kem-mau.pdf",
     "File: dinh-kem-mau.pdf",
     "- Khối đính kèm hiện thẻ file với biểu tượng PDF đỏ và tên file\n"
     "- Thẻ có dấu × để bỏ file\n"
     "- ⚠️ File CHƯA được tải lên lúc này, chỉ gửi đi khi bấm Lưu"),

    ("020", "Đính kèm nhiều file một lần", "P1",
     "Có 3 file PDF hợp lệ.",
     "1. Bấm 'Thêm file'\n"
     "2. Chọn cùng lúc 3 file PDF",
     "3 file PDF",
     "- Khối đính kèm hiện đủ 3 thẻ file"),

    ("021", "Chọn file không phải PDF", "P0",
     "Có file bao-gia.xlsx.",
     "1. Bấm 'Thêm file'\n"
     "2. Chọn bao-gia.xlsx",
     "File: bao-gia.xlsx",
     "- File KHÔNG được thêm vào khối đính kèm\n"
     "- Hiện dòng chữ đỏ ngay dưới khối: 'File \"bao-gia.xlsx\" không phải PDF'"),

    ("022", "Chọn file đuôi .pdf nhưng nội dung hỏng", "P0",
     "Có file hong.pdf thực chất là văn bản lỗi tải về từ cổng hoá đơn (đổi tên thành .pdf).",
     "1. Bấm 'Thêm file'\n"
     "2. Chọn hong.pdf",
     "File: hong.pdf",
     "- ⚠️ Hệ thống phát hiện ngay tại bước chọn, KHÔNG chờ tới lúc lưu\n"
     "- Hiện dòng chữ đỏ: 'File \"hong.pdf\" không phải PDF hợp lệ (file hỏng hoặc tải về lỗi) "
     "— hãy tải lại file'"),

    ("023", "Bỏ một file vừa chọn trước khi lưu", "P1",
     "Khối đính kèm đang có 2 file mới chọn.",
     "1. Bấm dấu × trên thẻ file thứ nhất",
     "—",
     "- Thẻ file biến mất ngay, không hỏi xác nhận (vì chưa tải lên)\n"
     "- Còn lại 1 file"),

    ("024", "Lưu nháp thành công", "P0",
     "Đã điền: ghi chú, 1 hàng hoá với 1 dòng khách hàng đủ thông tin, 1 file PDF.",
     "1. Bấm nút 'Lưu nháp'\n"
     "2. Quan sát thông báo và màn hình sau khi lưu",
     "Ghi chú: 'Phiếu thử' · SL 5 · Ngày cần 10/09/2026 · Ghi chú dòng 'Giao trước ngày lễ'",
     "- Thông báo thành công: 'Yêu cầu của bạn đã được lưu. Bạn cần gửi để yêu cầu được xử lý'\n"
     "- Quay về màn danh sách\n"
     "- Phiếu mới nằm dòng đầu, mã dạng PYCCH-xxxxx, trạng thái 'Đang tạo'\n"
     "- ⚠️ Nút 'Lưu nháp' KHÔNG hỏi xác nhận"),

    ("025", "Lưu và gửi duyệt — có hộp xác nhận", "P0",
     "Form đã điền đủ thông tin hợp lệ.",
     "1. Bấm nút 'Lưu và gửi duyệt'\n"
     "2. Đọc hộp thoại\n"
     "3. Bấm 'Xác nhận'",
     "—",
     "- Hộp 'Xác nhận lưu và gửi duyệt' hỏi 'Bạn đồng ý lưu và duyệt?'\n"
     "- Sau khi xác nhận: thông báo 'Yêu cầu của bạn đã được gửi'\n"
     "- Về danh sách, phiếu mới ở trạng thái 'Chờ duyệt'\n"
     "- ⚠️ Phiếu 'Chờ duyệt' KHÔNG còn nút Sửa/Xóa trên dòng"),

    ("026", "Hủy hộp xác nhận gửi duyệt", "P1",
     "Hộp 'Xác nhận lưu và gửi duyệt' đang mở.",
     "1. Bấm 'Hủy'",
     "—",
     "- Hộp đóng, vẫn ở form, dữ liệu đã nhập còn nguyên\n"
     "- Không có phiếu nào được tạo"),

    ("027", "Gửi duyệt bắn thông báo cho kế toán kho cùng công ty", "P0",
     "Tài khoản A thuộc công ty 4; tài khoản H có quyền 'Kế toán kho' công ty 4; tài khoản K có "
     "quyền 'Kế toán kho' công ty 1.",
     "1. A lập phiếu và bấm 'Lưu và gửi duyệt'\n"
     "2. Đăng nhập H, mở chuông thông báo\n"
     "3. Đăng nhập K, mở chuông thông báo",
     "—",
     "- H nhận được thông báo '<Tên A> vừa tạo yêu cầu chuyển hàng: <mã phiếu>'\n"
     "- K KHÔNG nhận được thông báo\n"
     "- Bấm vào thông báo mở đúng màn chi tiết phiếu"),

    ("028", "Lưu nháp KHÔNG bắn thông báo", "P1",
     "Tài khoản H có quyền 'Kế toán kho' cùng công ty với A.",
     "1. A lập phiếu và bấm 'Lưu nháp'\n"
     "2. Đăng nhập H, mở chuông thông báo",
     "—",
     "- H không nhận thông báo nào về phiếu nháp này\n"
     "- H cũng không thấy phiếu nháp này trên danh sách"),

    ("029", "Chống bấm nút lưu hai lần", "P1",
     "Form đã điền đủ thông tin.",
     "1. Bấm 'Lưu nháp' rồi bấm liên tiếp thêm 2 lần thật nhanh\n"
     "2. Về danh sách đếm số phiếu vừa tạo",
     "—",
     "- Chỉ tạo ra ĐÚNG 1 phiếu, không bị 2-3 phiếu trùng nội dung"),

    ("030", "Cảnh báo khi rời form đang nhập dở", "P0",
     "Form Tạo mới đã nhập ghi chú và thêm 1 hàng hoá, chưa lưu.",
     "1. Bấm nút 'Quay lại'\n"
     "2. Đọc hộp thoại\n"
     "3. Bấm 'Ở lại'",
     "—",
     "- Hộp 'Thông tin chưa lưu' hỏi 'Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?'\n"
     "- Bấm 'Ở lại' thì vẫn ở form, dữ liệu còn nguyên\n"
     "- Bấm 'Thoát' mới về danh sách và mất dữ liệu đang nhập"),

    ("031", "Không cảnh báo khi form còn trống", "P1",
     "Vừa mở form Tạo mới, chưa nhập gì.",
     "1. Bấm 'Quay lại'",
     "—",
     "- Về thẳng danh sách, KHÔNG hiện hộp 'Thông tin chưa lưu'"),

    ("032", "Mã yêu cầu sinh tự động liên tiếp", "P1",
     "Phiếu gần nhất có mã PYCCH-07365.",
     "1. Lập và lưu 1 phiếu mới\n"
     "2. Đọc mã phiếu vừa tạo",
     "—",
     "- Mã có dạng PYCCH- kèm 5 chữ số, ví dụ PYCCH-07366\n"
     "- Người dùng KHÔNG nhập được mã, không có ô mã trên form"),
]

S5 = [
    ("001", "Mở form Sửa từ danh sách", "P0",
     "Tài khoản A có phiếu PYCCH-07366 trạng thái 'Đang tạo' do chính mình lập, có 1 hàng hoá "
     "và 1 file đính kèm.",
     "1. Bấm nút Sửa (biểu tượng bút chì) trên dòng PYCCH-07366\n"
     "2. Quan sát form",
     "—",
     "- Tiêu đề màn: 'Sửa phiếu yêu cầu chuyển hàng'\n"
     "- 'Ngày lập' hiện ngày giờ tạo phiếu gốc, không sửa được\n"
     "- 'Người lập' hiện tên người lập gốc, không sửa được\n"
     "- Ghi chú, bảng hàng hoá, dòng khách hàng và file đính kèm nạp đúng dữ liệu đã lưu\n"
     "- ⚠️ Khối 'File đính kèm (PDF)' KHÔNG còn dấu sao đỏ (khi sửa không bắt buộc thêm file)"),

    ("002", "Sửa ghi chú và lưu nháp lại", "P0",
     "Đang ở form Sửa phiếu PYCCH-07366.",
     "1. Sửa ô 'Ghi chú' thành nội dung mới\n"
     "2. Bấm 'Lưu nháp'\n"
     "3. Mở lại phiếu kiểm tra",
     "Ghi chú: 'Cập nhật lần 2'",
     "- Thông báo 'Yêu cầu của bạn đã được lưu. Bạn cần gửi để yêu cầu được xử lý'\n"
     "- Về danh sách, phiếu vẫn ở trạng thái 'Đang tạo'\n"
     "- Cột 'Người cập nhật' và 'Ngày cập nhật' đổi theo người vừa sửa"),

    ("003", "Sửa rồi gửi duyệt luôn", "P0",
     "Đang ở form Sửa phiếu nháp.",
     "1. Bổ sung thêm 1 dòng khách hàng\n"
     "2. Bấm 'Lưu và gửi duyệt' rồi 'Xác nhận'",
     "Thêm dòng: SL 3 · Ngày cần 15/09/2026",
     "- Thông báo 'Yêu cầu của bạn đã được gửi'\n"
     "- Phiếu chuyển sang trạng thái 'Chờ duyệt', mất nút Sửa/Xóa trên dòng\n"
     "- Kế toán kho cùng công ty nhận được thông báo"),

    ("004", "Ngày cần đã qua trên dòng cũ vẫn lưu được", "P0",
     "Phiếu nháp PYCCH-07340 lập từ tháng trước, dòng khách hàng có ngày cần 15/08/2026 (đã qua). "
     "Hôm nay là 03/09/2026.",
     "1. Mở form Sửa phiếu này\n"
     "2. KHÔNG đụng vào ô 'Ngày cần'\n"
     "3. Chỉ sửa ô Ghi chú rồi bấm 'Lưu nháp'",
     "Chỉ đổi ghi chú",
     "- ⚠️ Lưu THÀNH CÔNG, không báo lỗi ngày quá khứ\n"
     "- Đây là điểm khác biệt cố ý với cổng cũ: dòng giữ nguyên ngày cũ được miễn kiểm tra"),

    ("005", "Đổi ngày cần trên dòng cũ sang ngày quá khứ khác", "P0",
     "Vẫn phiếu PYCCH-07340, dòng có ngày cần 15/08/2026.",
     "1. Mở form Sửa\n"
     "2. Đổi ô 'Ngày cần' của dòng đó sang 20/08/2026 (vẫn quá khứ)\n"
     "3. Bấm 'Lưu nháp'",
     "Ngày cần: 15/08/2026 → 20/08/2026",
     "- ⚠️ Bị chặn: hiện lỗi đỏ 'Ngày cần hàng phải sau ngày hôm nay' ngay dưới ô Ngày cần\n"
     "- Phiếu không được lưu\n"
     "- Vì dòng ĐÃ ĐỔI ngày nên bị kiểm tra như dòng mới"),

    ("006", "Thêm dòng khách hàng mới với ngày quá khứ", "P0",
     "Đang sửa phiếu nháp.",
     "1. Bấm '+ Thêm khách hàng'\n"
     "2. Thử mở lịch chọn ngày 01/09/2026 (đã qua)",
     "Ngày cần: 01/09/2026",
     "- Trên lịch, các ngày từ hôm nay trở về trước bị mờ, không bấm chọn được\n"
     "- Chỉ chọn được từ ngày mai trở đi"),

    ("007", "Thêm file đính kèm khi sửa — file cũ vẫn giữ", "P0",
     "Phiếu nháp đang có 1 file đính kèm.",
     "1. Mở form Sửa\n"
     "2. Bấm 'Thêm file', chọn thêm 1 file PDF khác\n"
     "3. Bấm 'Lưu nháp' rồi mở lại phiếu",
     "Thêm file: phu-luc.pdf",
     "- Sau khi lưu, phiếu có ĐỦ 2 file: file cũ và file mới\n"
     "- File mới nối vào sau, không ghi đè file cũ"),

    ("008", "Lưu khi sửa mà không chọn thêm file", "P0",
     "Phiếu nháp đang có 1 file đính kèm.",
     "1. Mở form Sửa\n"
     "2. Chỉ sửa ghi chú, không chọn thêm file\n"
     "3. Bấm 'Lưu nháp'",
     "—",
     "- Lưu thành công, KHÔNG báo lỗi thiếu file đính kèm\n"
     "- File cũ còn nguyên"),

    ("009", "Xóa file đã lưu — xóa vĩnh viễn ngay lập tức", "P0",
     "Phiếu nháp đang có 1 file đính kèm.",
     "1. Mở form Sửa\n"
     "2. Bấm dấu × trên thẻ file đã lưu\n"
     "3. Đọc hộp xác nhận rồi bấm 'Xác nhận'\n"
     "4. Bấm 'Quay lại' và KHÔNG lưu phiếu\n"
     "5. Mở lại phiếu",
     "—",
     "- Hộp 'Xác nhận xóa file' ghi rõ tên file và cảnh báo 'File sẽ bị xóa vĩnh viễn'\n"
     "- Sau khi xác nhận: thông báo 'Xóa file thành công', thẻ file biến mất\n"
     "- ⚠️ Mở lại phiếu thấy file ĐÃ MẤT dù không bấm Lưu — xóa file có hiệu lực ngay"),

    ("010", "Hủy hộp xác nhận xóa file", "P1",
     "Hộp 'Xác nhận xóa file' đang mở.",
     "1. Bấm 'Hủy'",
     "—",
     "- Hộp đóng, thẻ file còn nguyên, file chưa bị xóa"),

    ("011", "Mở form Sửa của phiếu đã gửi duyệt bằng thanh địa chỉ", "P0",
     "Phiếu PYCCH-07361 do chính mình lập, trạng thái 'Chờ duyệt'.",
     "1. Gõ thẳng đường dẫn màn Sửa của phiếu này lên thanh địa chỉ\n"
     "2. Quan sát",
     "—",
     "- Hệ thống chặn ngay, báo 'Chỉ sửa được phiếu Đang tạo do chính bạn lập'\n"
     "- Tự đưa về màn danh sách, không hiện form Sửa"),

    ("012", "Xóa hàng hoá khi sửa", "P1",
     "Phiếu nháp có 2 hàng hoá.",
     "1. Mở form Sửa\n"
     "2. Bấm dấu trừ trên dòng hàng hoá số 2, xác nhận\n"
     "3. Bấm 'Lưu nháp' rồi mở lại phiếu",
     "—",
     "- Phiếu còn 1 hàng hoá\n"
     "- Toàn bộ dòng khách hàng của hàng vừa xóa cũng biến mất"),

    ("013", "Cảnh báo chưa lưu khi rời form Sửa", "P1",
     "Đang sửa ghi chú của phiếu nháp, chưa bấm Lưu.",
     "1. Bấm 'Quay lại'",
     "—",
     "- Hiện hộp 'Thông tin chưa lưu'\n"
     "- ⚠️ Vừa mở form Sửa mà chưa gõ gì thì bấm 'Quay lại' KHÔNG hiện hộp này (dữ liệu nạp về "
     "không bị coi là người dùng vừa nhập)"),
]

S6 = [
    ("001", "Mở màn chi tiết từ mã yêu cầu", "P0",
     "Phiếu PYCCH-07365 trạng thái 'Chờ duyệt', có 1 hàng hoá, 1 dòng khách hàng, 1 file đính kèm.",
     "1. Bấm vào mã 'PYCCH-07365' trên danh sách\n"
     "2. Quan sát toàn màn",
     "—",
     "- Tiêu đề: 'Chi tiết phiếu yêu cầu chuyển hàng · PYCCH-07365', góc phải có nhãn trạng thái\n"
     "- Khối 'Thông tin chung': Mã yêu cầu, Ngày lập, Người lập, Người tiếp nhận, Ghi chú — tất "
     "cả chỉ đọc\n"
     "- Khối 'File đính kèm' hiện thẻ file PDF\n"
     "- Khối 'Danh sách hàng hóa' có bảng hàng hoá và bảng con khách hàng\n"
     "- Không có ô nào nhập được ngoài 'Ghi chú duyệt' (nếu có quyền)"),

    ("002", "Ô trống hiển thị dấu gạch ngang", "P1",
     "Phiếu chưa có người tiếp nhận và không có ghi chú.",
     "1. Mở màn chi tiết phiếu đó",
     "—",
     "- Ô 'Người tiếp nhận' và ô 'Ghi chú' đều hiện dấu gạch ngang, không để trắng trơn"),

    ("003", "Người tiếp nhận hiện kèm ngày tiếp nhận", "P1",
     "Phiếu PYCCH-07359 đã có người tiếp nhận là 'Bùi Thị Thịnh' ngày 27/07/2026 16:36.",
     "1. Mở màn chi tiết phiếu này",
     "—",
     "- Ô 'Người tiếp nhận' hiện 'Bùi Thị Thịnh · 27/07/2026 16:36'"),

    ("004", "Bảng hàng hoá ở màn chi tiết", "P0",
     "Phiếu có 1 hàng hoá với 2 dòng khách hàng.",
     "1. Mở màn chi tiết\n"
     "2. Đọc bảng hàng hoá",
     "—",
     "- Bảng cha có cột: STT, Hàng hóa, ĐVT, Giá niêm yết, SL cần\n"
     "- Dòng hàng hoá hiện tên, dòng phụ ghi Model, Mã và tên hãng\n"
     "- Bảng con ngay dưới có cột: Khách hàng, SL cần, Ngày cần, Ghi chú\n"
     "- Ngày cần hiển thị dạng ngày/tháng/năm"),

    ("005", "Cột 'Được nhận' chỉ hiện khi phiếu Đã phân bổ", "P0",
     "Có phiếu X trạng thái 'Đã phân bổ' và phiếu Y trạng thái 'Đã xuất kho'.",
     "1. Mở chi tiết phiếu X, xem bảng con khách hàng\n"
     "2. Mở chi tiết phiếu Y, xem bảng con khách hàng",
     "—",
     "- Phiếu X: bảng con CÓ thêm cột 'Được nhận'\n"
     "- ⚠️ Phiếu Y: KHÔNG có cột 'Được nhận'"),

    ("006", "Mở file đính kèm từ màn chi tiết", "P1",
     "Phiếu có 1 file PDF đính kèm.",
     "1. Bấm vào tên file trong khối 'File đính kèm'",
     "—",
     "- File mở ở tab mới, xem được nội dung PDF\n"
     "- Không có nút xóa file ở màn chi tiết"),

    ("007", "Phiếu không có file đính kèm", "P1",
     "Phiếu cũ chuyển từ hệ thống trước, không có file đính kèm.",
     "1. Mở màn chi tiết phiếu này",
     "—",
     "- Khối 'File đính kèm' hiện dòng chữ 'Không có file đính kèm.'\n"
     "- Không báo lỗi"),

    ("008", "Nút cuối màn chi tiết theo trạng thái và quyền", "P0",
     "Tài khoản A: phiếu P1 'Đang tạo' của A; phiếu P2 'Chờ duyệt' cùng công ty (A có quyền Kế "
     "toán kho); phiếu P3 'Đã xuất kho'.",
     "1. Lần lượt mở chi tiết P1, P2, P3\n"
     "2. Ghi lại các nút cuối màn",
     "—",
     "- P1: 'Sửa', 'In', 'Quay lại'\n"
     "- P2: 'In', 'Không duyệt', 'Tổng hợp', 'Quay lại' — không có 'Sửa'\n"
     "- P3: 'In', 'Quay lại'\n"
     "- ⚠️ Thứ tự nút cố định: Sửa · In · Không duyệt · Tổng hợp · Quay lại"),

    ("009", "Ghi chú duyệt cũ hiển thị chỉ đọc", "P1",
     "Phiếu PYCCH-07340 đã từng bị không duyệt với lý do 'Sai số lượng', hiện ở trạng thái "
     "'Đang tạo'. Người xem là người lập phiếu (không có quyền Kế toán kho).",
     "1. Mở màn chi tiết phiếu này",
     "—",
     "- Có khối 'Ghi chú duyệt' hiển thị nội dung 'Sai số lượng' ở dạng chỉ đọc\n"
     "- Không có ô nhập, không có dấu sao đỏ"),

    ("010", "Mở phiếu bằng mã không tồn tại", "P1",
     "Tài khoản E.",
     "1. Gõ đường dẫn màn chi tiết với mã phiếu không có thật lên thanh địa chỉ",
     "—",
     "- Hệ thống báo không tìm thấy dữ liệu và đưa về danh sách\n"
     "- Không treo trang, không hiện màn chi tiết trắng"),

    ("011", "Nút Quay lại từ màn chi tiết", "P1",
     "Đang ở màn chi tiết, trước đó danh sách đang lọc Trạng thái 'Chờ duyệt' trang 2.",
     "1. Bấm 'Quay lại'",
     "—",
     "- Về màn danh sách\n"
     "- Điều kiện lọc 'Chờ duyệt' vẫn còn (được ghi nhớ 10 phút)"),
]

S7 = [
    ("001", "Không duyệt phiếu — luồng đầy đủ", "P0",
     "Tài khoản H có quyền 'Kế toán kho' công ty 4. Phiếu PYCCH-07365 trạng thái 'Chờ duyệt', "
     "công ty 4, do tài khoản A lập.",
     "1. Đăng nhập H, mở chi tiết PYCCH-07365\n"
     "2. Nhập 'Ghi chú duyệt' = 'Thiếu thông tin khách hàng nhận hàng, đề nghị bổ sung'\n"
     "3. Bấm 'Không duyệt'\n"
     "4. Bấm 'Không duyệt' trong hộp xác nhận",
     "Ghi chú duyệt: Thiếu thông tin khách hàng nhận hàng, đề nghị bổ sung",
     "- Hộp 'Xác nhận không duyệt' ghi rõ mã phiếu và câu 'Phiếu sẽ chuyển về trạng thái Đang "
     "tạo để người lập sửa lại'\n"
     "- Sau khi xác nhận: thông báo 'Đã từ chối yêu cầu chuyển hàng'\n"
     "- Phiếu chuyển sang trạng thái 'Đang tạo'\n"
     "- Cột 'Người tiếp nhận' ghi tên H, 'Ngày tiếp nhận' ghi thời điểm vừa bấm"),

    ("002", "Không duyệt khi chưa nhập ghi chú duyệt", "P0",
     "Tài khoản H đang mở phiếu 'Chờ duyệt', ô 'Ghi chú duyệt' còn trống.",
     "1. Bấm 'Không duyệt' mà không nhập gì",
     "—",
     "- KHÔNG mở hộp xác nhận\n"
     "- Ô 'Ghi chú duyệt' viền đỏ, dưới ô hiện chữ đỏ 'Vui lòng nhập ghi chú duyệt'\n"
     "- Phiếu giữ nguyên trạng thái 'Chờ duyệt'"),

    ("003", "Lỗi ghi chú duyệt chỉ hiện sau lần bấm đầu tiên", "P1",
     "Vừa mở màn chi tiết phiếu 'Chờ duyệt', chưa bấm nút nào.",
     "1. Quan sát ô 'Ghi chú duyệt' khi mới vào màn\n"
     "2. Bấm 'Không duyệt' để bung lỗi\n"
     "3. Gõ nội dung vào ô",
     "—",
     "- Lúc mới vào: ô trống, KHÔNG có viền đỏ và chữ đỏ\n"
     "- Sau khi bấm: hiện lỗi đỏ\n"
     "- Gõ nội dung vào thì lỗi đỏ biến mất"),

    ("004", "Hủy hộp xác nhận không duyệt", "P0",
     "Đã nhập ghi chú duyệt, hộp 'Xác nhận không duyệt' đang mở.",
     "1. Bấm 'Hủy'\n"
     "2. Tải lại màn chi tiết",
     "—",
     "- Hộp đóng, phiếu VẪN ở trạng thái 'Chờ duyệt'\n"
     "- Người tiếp nhận vẫn là dấu gạch ngang, ghi chú duyệt chưa được ghi vào phiếu"),

    ("005", "Người lập xem lại phiếu sau khi bị không duyệt", "P0",
     "Phiếu PYCCH-07365 vừa bị H không duyệt với lý do đã ghi.",
     "1. Đăng nhập tài khoản A (người lập)\n"
     "2. Mở chuông thông báo\n"
     "3. Mở chi tiết phiếu",
     "—",
     "- Có thông báo '<Tên H> vừa từ chối yêu cầu chuyển hàng: <mã phiếu>'\n"
     "- Phiếu ở trạng thái 'Đang tạo', A thấy lại nút 'Sửa'\n"
     "- Khối 'Ghi chú duyệt' hiện đúng lý do H đã nhập, ở dạng chỉ đọc"),

    ("006", "Sửa và gửi lại phiếu sau khi bị không duyệt", "P0",
     "Phiếu ở trạng thái 'Đang tạo' sau khi bị không duyệt.",
     "1. Tài khoản A mở form Sửa, bổ sung thông tin còn thiếu\n"
     "2. Bấm 'Lưu và gửi duyệt' rồi xác nhận\n"
     "3. Mở lại chi tiết phiếu",
     "—",
     "- Phiếu trở lại trạng thái 'Chờ duyệt'\n"
     "- Kế toán kho cùng công ty nhận thông báo mới\n"
     "- ⚠️ Ghi chú duyệt của lần từ chối trước vẫn còn trên phiếu (không tự xoá)"),

    ("007", "Không duyệt phiếu KHÔNG ở trạng thái Chờ duyệt", "P0",
     "Phiếu PYCCH-07359 đang ở trạng thái 'Đang đề nghị', cùng công ty với tài khoản H.",
     "1. Đăng nhập H, mở chi tiết PYCCH-07359\n"
     "2. Quan sát các nút cuối màn",
     "—",
     "- KHÔNG có nút 'Không duyệt' và 'Tổng hợp'\n"
     "- KHÔNG có khối 'Ghi chú duyệt' cho nhập\n"
     "- ⚠️ Chỉ phiếu ở đúng trạng thái 'Chờ duyệt' mới không duyệt được"),

    ("008", "Nút 'Tổng hợp' mở màn lập phiếu xuất hàng ở tab mới", "P0",
     "Tài khoản H đang mở phiếu 'Chờ duyệt' cùng công ty.",
     "1. Bấm nút 'Tổng hợp'\n"
     "2. Quan sát trình duyệt",
     "—",
     "- Mở TAB MỚI sang màn lập phiếu đề nghị xuất hàng của cổng cũ, mang sẵn mã phiếu này\n"
     "- Tab đang xem vẫn ở màn chi tiết, phiếu không đổi trạng thái"),

    ("009", "Nút 'Tổng hợp' trên dòng danh sách", "P1",
     "Tài khoản H, danh sách có phiếu 'Chờ duyệt' cùng công ty.",
     "1. Bấm nút Tổng hợp (dấu tích kép) trên dòng phiếu đó",
     "—",
     "- Mở tab mới sang màn lập phiếu đề nghị xuất hàng như ở màn chi tiết\n"
     "- Danh sách không đổi, không nạp lại"),

    ("010", "Chống bấm 'Không duyệt' hai lần", "P1",
     "Đã nhập ghi chú duyệt, hộp xác nhận đang mở.",
     "1. Bấm nút 'Không duyệt' trong hộp xác nhận liên tiếp 3 lần thật nhanh\n"
     "2. Mở lịch sử thay đổi của phiếu",
     "—",
     "- Phiếu chỉ chuyển trạng thái MỘT lần\n"
     "- Lịch sử chỉ ghi một lần đổi trạng thái, không có bản ghi trùng"),

    ("011", "Hai kế toán kho cùng không duyệt một phiếu", "P1",
     "Hai tài khoản H1 và H2 đều có quyền 'Kế toán kho' công ty 4, cùng mở phiếu PYCCH-07365 "
     "trạng thái 'Chờ duyệt'.",
     "1. H1 nhập ghi chú và không duyệt thành công\n"
     "2. H2 (chưa tải lại trang) nhập ghi chú và bấm 'Không duyệt'",
     "—",
     "- H2 bị từ chối, hệ thống báo không có quyền thực hiện thao tác này (vì phiếu đã rời "
     "trạng thái Chờ duyệt)\n"
     "- Người tiếp nhận trên phiếu vẫn là H1, ghi chú duyệt vẫn là của H1"),
]

S8 = [
    ("001", "Xóa phiếu nháp — luồng đầy đủ", "P0",
     "Tài khoản A có phiếu PYCCH-07366 trạng thái 'Đang tạo' do chính mình lập.",
     "1. Bấm nút Xóa (biểu tượng thùng rác) trên dòng PYCCH-07366\n"
     "2. Đọc hộp xác nhận\n"
     "3. Bấm 'Xóa'",
     "—",
     "- Hộp 'Xác nhận xóa' ghi 'Bạn có chắc muốn xóa phiếu yêu cầu chuyển hàng PYCCH-07366?'\n"
     "- Sau khi xóa: thông báo 'Xóa thành công'\n"
     "- Dòng biến mất khỏi danh sách, tổng số phiếu giảm đúng 1\n"
     "- Mở lại đường dẫn cũ của phiếu thì báo không tìm thấy dữ liệu"),

    ("002", "Hủy hộp xác nhận xóa", "P0",
     "Hộp 'Xác nhận xóa' đang mở.",
     "1. Bấm 'Hủy'",
     "—",
     "- Hộp đóng, phiếu còn nguyên trên danh sách, tổng số phiếu không đổi"),

    ("003", "Xóa phiếu kéo theo toàn bộ hàng hoá và dòng khách hàng", "P0",
     "Phiếu nháp có 2 hàng hoá, mỗi hàng 3 dòng khách hàng.",
     "1. Xóa phiếu\n"
     "2. Tìm lại phiếu bằng ô 'Tên/mã hàng hóa' với mã của một hàng trong phiếu vừa xóa",
     "—",
     "- Phiếu vừa xóa không còn xuất hiện trong kết quả tìm theo hàng hoá\n"
     "- Không còn dữ liệu sót lại gây kết quả lạ"),

    ("004", "Không có nút Xóa trên phiếu đã gửi duyệt", "P0",
     "Tài khoản A có phiếu 'Chờ duyệt' do chính mình lập.",
     "1. Quan sát cột Hành động của dòng đó\n"
     "2. Mở màn chi tiết và quan sát các nút cuối màn",
     "—",
     "- Danh sách: KHÔNG có nút Xóa (chỉ có Tổng hợp/In/Lịch sử tuỳ quyền)\n"
     "- Màn chi tiết: KHÔNG có nút Xóa"),

    ("005", "Không có nút Xóa trên phiếu nháp của người khác", "P0",
     "Tài khoản E có quyền xem tổng công ty; hệ thống có nhiều phiếu nháp của người khác.",
     "1. Lọc Trạng thái = 'Đang tạo'\n"
     "2. Quan sát cột Người tạo của các dòng",
     "Trạng thái: Đang tạo",
     "- ⚠️ Không có dòng nào của người khác để mà xóa — nháp người khác vốn không hiện\n"
     "- Mọi dòng đều là nháp của chính E và đều có nút Xóa"),

    ("006", "Xóa phiếu vừa bị người khác đổi trạng thái", "P1",
     "Tài khoản A đang mở danh sách có phiếu nháp P1; trong lúc đó P1 bị đổi trạng thái ở nơi "
     "khác.",
     "1. A bấm Xóa trên dòng P1 (chưa tải lại trang) rồi xác nhận\n"
     "2. Quan sát",
     "—",
     "- Hệ thống từ chối, báo 'Chỉ xóa được phiếu Đang tạo do chính bạn lập'\n"
     "- Danh sách TỰ NẠP LẠI để khớp hiện trạng, không nuốt lỗi im lặng"),

    ("007", "Xóa phiếu rồi tạo phiếu mới — mã không dùng lại", "P2",
     "Vừa xóa phiếu PYCCH-07366.",
     "1. Lập và lưu 1 phiếu mới\n"
     "2. Đọc mã phiếu vừa tạo",
     "—",
     "- Mã mới là PYCCH-07367 (hoặc lớn hơn), KHÔNG dùng lại mã của phiếu đã xóa"),
]

S9 = [
    ("001", "In phiếu từ màn chi tiết", "P0",
     "Phiếu PYCCH-07365 có 1 hàng hoá và 1 dòng khách hàng.",
     "1. Mở chi tiết phiếu\n"
     "2. Bấm nút 'In'",
     "—",
     "- Mở TAB MỚI hiển thị bản in\n"
     "- Đầu trang có ảnh tiêu đề thư (logo và thông tin công ty) chiếm hết chiều ngang\n"
     "- Tiêu đề in đậm 'PHIẾU YÊU CẦU CHUYỂN HÀNG', dưới là 'No: PYCCH-07365'"),

    ("002", "Nội dung bản in khớp dữ liệu phiếu", "P0",
     "Phiếu PYCCH-07365: ngày lập 17/08/2026, người lập DNS Admin, 1 hàng 'Keo vá lốp màu xanh "
     "250 ml' mã CH-TW-9250, đơn vị Lọ, SL 1, khách hàng 'CÔNG TY TNHH THƯƠNG MẠI MẪU', ngày "
     "cần 18/08/2026, ghi chú '111'.",
     "1. Mở bản in\n"
     "2. Đối chiếu từng dòng với màn chi tiết",
     "—",
     "- 'Ngày yêu cầu: 17/08/2026' và 'Người yêu cầu: DNS Admin'\n"
     "- Bảng in có cột: STT, Hàng hóa, ĐVT, SL và nhóm cột 'Chi tiết' gồm Khách hàng, SL, "
     "Ngày cần, Ghi chú\n"
     "- Dòng hàng hoá hiện tên và 'Mã: CH-TW-9250'\n"
     "- ⚠️ Bản in KHÔNG có cột 'Giá niêm yết'\n"
     "- Cuối trang có 2 ô ký: 'Người lập phiếu' và 'Giám đốc công ty', dưới ô người lập có tên "
     "người lập phiếu"),

    ("003", "Tiêu đề thư lấy theo công ty ghi trên phiếu", "P0",
     "Phiếu X thuộc công ty Tân Phát Etek, phiếu Y thuộc công ty khác có ảnh tiêu đề thư riêng. "
     "Người in thuộc công ty thứ ba.",
     "1. In phiếu X, chụp lại phần đầu trang\n"
     "2. In phiếu Y, chụp lại phần đầu trang",
     "—",
     "- ⚠️ Mỗi bản in mang tiêu đề thư của ĐÚNG công ty ghi trên phiếu, KHÔNG phải công ty của "
     "người đang in và cũng không phải công ty của người tạo phiếu"),

    ("004", "In phiếu từ danh sách", "P1",
     "Danh sách có phiếu PYCCH-07365.",
     "1. Bấm nút In (biểu tượng máy in) trên dòng phiếu",
     "—",
     "- Mở tab mới đúng bản in của phiếu đó, giống hệt khi in từ màn chi tiết\n"
     "- Danh sách không đổi"),

    ("005", "Nút In hiện với mọi người xem được phiếu", "P1",
     "Tài khoản A không có quyền 'Kế toán kho', đang xem phiếu do chính mình lập ở trạng thái "
     "'Đã xuất kho'.",
     "1. Mở chi tiết phiếu\n"
     "2. Quan sát các nút",
     "—",
     "- Nút 'In' vẫn hiện\n"
     "- Ai xem được phiếu thì in được phiếu"),

    ("006", "In phiếu không có quyền xem", "P0",
     "Tài khoản K không xem được phiếu PYCCH-07365 (khác công ty, không phải người lập).",
     "1. Gõ thẳng đường dẫn màn in của phiếu này lên thanh địa chỉ",
     "—",
     "- Hệ thống từ chối, báo không có quyền xem phiếu này\n"
     "- Không hiển thị nội dung phiếu"),

    ("007", "Phiếu nhiều hàng hoá — bản in không vỡ bảng", "P1",
     "Phiếu có 8 hàng hoá, mỗi hàng 2-3 dòng khách hàng.",
     "1. Mở bản in\n"
     "2. Xem trước khi in (bấm tổ hợp phím in của trình duyệt)",
     "—",
     "- Bảng có đủ đường viền, không mất viền phải hay viền dưới\n"
     "- Sang trang 2 vẫn còn viền và nội dung không bị cắt tràn lề phải"),

    ("008", "In lại phiếu không làm đổi dữ liệu", "P2",
     "Phiếu PYCCH-07365 trạng thái 'Chờ duyệt'.",
     "1. In phiếu 3 lần\n"
     "2. Mở lịch sử thay đổi của phiếu",
     "—",
     "- Trạng thái, người cập nhật, ngày cập nhật của phiếu KHÔNG đổi\n"
     "- Lịch sử không phát sinh bản ghi mới"),
]

S10 = [
    ("001", "Xuất Excel toàn bộ danh sách trong phạm vi quyền", "P0",
     "Tài khoản E đang thấy 2.960 phiếu, không đặt bộ lọc nào, đang xem trang 1 với 10 dòng.",
     "1. Bấm nút 'Xuất Excel'\n"
     "2. Giữ nguyên 6 trường mặc định, bấm 'Xuất file'\n"
     "3. Mở file tải về",
     "—",
     "- Tên file tải về: danh_sach_yeu_cau_chuyen_hang.xlsx\n"
     "- ⚠️ File có ĐỦ 2.960 dòng, không phải chỉ 10 dòng đang hiển thị\n"
     "- Thông báo 'Xuất Excel thành công'"),

    ("002", "Popup chọn trường xuất file", "P0",
     "Đang ở màn danh sách.",
     "1. Bấm 'Xuất Excel'\n"
     "2. Quan sát popup",
     "—",
     "- Popup 'Chọn trường xuất file' hiện sẵn 6 trường: Mã yêu cầu, Người tiếp nhận, Ngày tiếp "
     "nhận, Trạng thái, Người tạo, Ngày tạo\n"
     "- Dòng chữ dưới ghi rõ thứ tự cột trong file chạy theo đúng thứ tự đã chọn\n"
     "- Có dòng 'Đang chọn 6/6 trường', nút 'Chọn tất cả' và 'Bỏ chọn hết'"),

    ("003", "Bỏ bớt trường xuất", "P1",
     "Popup 'Chọn trường xuất file' đang mở.",
     "1. Bỏ 'Người tiếp nhận' và 'Ngày tiếp nhận'\n"
     "2. Bấm 'Xuất file' rồi mở file",
     "Bỏ: Người tiếp nhận, Ngày tiếp nhận",
     "- File chỉ có 4 cột dữ liệu còn lại, đúng thứ tự đã chọn"),

    ("004", "Đổi thứ tự cột xuất", "P2",
     "Popup 'Chọn trường xuất file' đang mở.",
     "1. Bỏ chọn hết\n"
     "2. Chọn lại theo thứ tự: Trạng thái, Mã yêu cầu, Người tạo\n"
     "3. Xuất file",
     "Thứ tự chọn: Trạng thái → Mã yêu cầu → Người tạo",
     "- Cột trong file xếp đúng thứ tự Trạng thái, Mã yêu cầu, Người tạo"),

    ("005", "Xuất Excel theo bộ lọc đang áp dụng", "P0",
     "Đang lọc Trạng thái = 'Chờ duyệt' (2.500 phiếu) và Ngày tạo từ 01/07/2026.",
     "1. Bấm 'Xuất Excel', xuất đủ 6 trường\n"
     "2. Mở file, đếm số dòng và kiểm tra cột Trạng thái",
     "—",
     "- Số dòng trong file bằng đúng số phiếu khớp bộ lọc\n"
     "- Mọi dòng đều có Trạng thái 'Chờ duyệt' và Ngày tạo từ 01/07/2026 trở đi"),

    ("006", "File Excel có dòng tiêu đề khoảng ngày", "P1",
     "Đang lọc Ngày tạo từ 01/07/2026 đến 31/07/2026.",
     "1. Xuất Excel và mở file",
     "—",
     "- Phía trên bảng có dòng 'Từ ngày 01/07/2026 đến ngày 31/07/2026'\n"
     "- Chỉ đặt một mốc thì dòng này ghi 'Từ ngày ...' hoặc 'Đến ngày ...' tương ứng\n"
     "- Không đặt mốc nào thì không có dòng này"),

    ("007", "Định dạng ngày trong file Excel", "P1",
     "Có phiếu tạo lúc 07/08/2026 16:10.",
     "1. Xuất Excel và mở file\n"
     "2. Xem ô Ngày tạo của phiếu đó",
     "—",
     "- Ô hiển thị 07/08/2026 (chỉ ngày, không kèm giờ)\n"
     "- Phiếu chưa tiếp nhận thì ô Ngày tiếp nhận để trống"),

    ("008", "Xuất Excel không vượt phạm vi quyền", "P0",
     "Tài khoản B chỉ thấy 13 phiếu trên lưới.",
     "1. Đăng nhập B, bấm 'Xuất Excel', xuất đủ trường\n"
     "2. Đếm số dòng trong file",
     "—",
     "- File có đúng 13 dòng\n"
     "- ⚠️ Không có phiếu nào ngoài phạm vi quyền của B lọt vào file"),

    ("009", "Xuất Excel khi kết quả rỗng", "P1",
     "Đang lọc bằng từ khoá không khớp gì, lưới trống.",
     "1. Bấm 'Xuất Excel' và xuất file\n"
     "2. Mở file",
     "—",
     "- File vẫn tải về được, có dòng tiêu đề cột nhưng không có dòng dữ liệu\n"
     "- Không báo lỗi"),
]

S11 = [
    ("001", "Mở lịch sử thay đổi từ danh sách", "P0",
     "Phiếu PYCCH-07365 mới chỉ được tạo, chưa sửa lần nào.",
     "1. Bấm nút Lịch sử (biểu tượng đồng hồ quay ngược) trên dòng phiếu",
     "—",
     "- Popup 'Lịch sử thay đổi' mở, phụ đề ghi 'Phiếu yêu cầu: PYCCH-07365'\n"
     "- Có đúng 1 mốc: thời điểm tạo, nhãn 'Tạo mới', dòng 'Người thực hiện: <tên> — <phòng ban>'"),

    ("002", "Lịch sử ghi lại thao tác sửa", "P0",
     "Phiếu nháp vừa được sửa ghi chú.",
     "1. Mở popup Lịch sử của phiếu",
     "—",
     "- Có thêm mốc thời gian mới với nhãn chỉnh sửa\n"
     "- Ghi rõ trường bị đổi, giá trị cũ và giá trị mới\n"
     "- Ghi đúng tên người thực hiện"),

    ("003", "Lịch sử ghi lại đổi trạng thái", "P0",
     "Phiếu vừa được gửi duyệt (từ 'Đang tạo' sang 'Chờ duyệt').",
     "1. Mở popup Lịch sử",
     "—",
     "- Có mốc riêng thuộc nhóm thay đổi trạng thái\n"
     "- Ghi 'Đang tạo' → 'Chờ duyệt' bằng ĐÚNG TÊN trạng thái, không phải con số"),

    ("004", "Bộ lọc trong popup Lịch sử", "P2",
     "Phiếu có nhiều mốc lịch sử thuộc các nhóm khác nhau.",
     "1. Mở popup Lịch sử\n"
     "2. Bấm nút 'Bộ lọc' và chọn một nhóm thao tác",
     "—",
     "- Danh sách mốc lọc lại đúng nhóm đã chọn\n"
     "- Bỏ lọc thì hiện lại đầy đủ"),

    ("005", "Ai cũng xem được lịch sử của phiếu mình thấy", "P1",
     "Tài khoản A không có quyền đặc biệt nào, đang thấy phiếu do mình lập.",
     "1. Bấm nút Lịch sử trên dòng phiếu đó",
     "—",
     "- Popup mở bình thường, không bị chặn quyền\n"
     "- Nút Lịch sử luôn hiện trên mọi dòng"),

    ("006", "Đóng popup Lịch sử", "P2",
     "Popup Lịch sử đang mở.",
     "1. Bấm 'Đóng'",
     "—",
     "- Popup đóng, danh sách phía sau giữ nguyên trang và bộ lọc"),
]

S12 = [
    ("001", "Lưu khi chưa thêm hàng hoá nào", "P0",
     "Form Tạo mới, đã nhập ghi chú và đính kèm 1 file PDF nhưng bảng hàng hoá trống.",
     "1. Bấm 'Lưu nháp'",
     "—",
     "- Không lưu được\n"
     "- Hiện lỗi đỏ dưới bảng hàng hoá: 'Bắt buộc phải có ít nhất 1 hàng hóa'"),

    ("002", "Lưu khi dòng khách hàng còn trống hết", "P0",
     "Form có 1 hàng hoá, dòng khách hàng chưa nhập gì; chưa đính kèm file.",
     "1. Bấm 'Lưu và gửi duyệt' rồi xác nhận\n"
     "2. Quan sát các ô trên dòng khách hàng và khối đính kèm",
     "—",
     "- Không lưu được, màn hình tự cuộn tới ô lỗi đầu tiên\n"
     "- Dưới ô Khách hàng: 'Bắt buộc chọn'\n"
     "- Dưới ô SL: 'Không được nhỏ hơn 1'\n"
     "- Dưới ô Ngày cần: 'Bắt buộc chọn'\n"
     "- Dưới ô Ghi chú của dòng: 'Bắt buộc nhập'\n"
     "- Dưới khối File đính kèm: 'Bắt buộc phải nhập'\n"
     "- ⚠️ Cửa sổ không đóng, mọi dữ liệu đã nhập vẫn còn"),

    ("003", "Ghi chú phiếu quá 255 ký tự", "P0",
     "Form Tạo mới.",
     "1. Dán 300 ký tự vào ô 'Ghi chú'\n"
     "2. Quan sát ngay khi vừa dán",
     "Chuỗi 300 ký tự",
     "- Lỗi hiện NGAY, không cần bấm Lưu: 'Vui lòng nhập tối đa 255 ký tự.'\n"
     "- Bấm Lưu thì không lưu được"),

    ("004", "Ghi chú phiếu đúng 255 ký tự", "P1",
     "Form Tạo mới, các thông tin khác đã hợp lệ.",
     "1. Dán đúng 255 ký tự vào ô 'Ghi chú'\n"
     "2. Bấm 'Lưu nháp'",
     "Chuỗi 255 ký tự",
     "- Không báo lỗi, lưu thành công\n"
     "- Mở lại phiếu thấy đủ 255 ký tự"),

    ("005", "Ghi chú dòng khách hàng quá 255 ký tự", "P1",
     "Form có 1 hàng hoá với 1 dòng khách hàng.",
     "1. Dán 300 ký tự vào ô 'Ghi chú' của dòng khách hàng",
     "Chuỗi 300 ký tự",
     "- Lỗi đỏ ngay dưới ô: 'Vui lòng nhập tối đa 255 ký tự.'"),

    ("006", "Số lượng bằng 0", "P0",
     "Dòng khách hàng đã chọn khách hàng, ngày cần và ghi chú.",
     "1. Nhập SL = 0\n"
     "2. Quan sát",
     "SL: 0",
     "- Lỗi đỏ ngay dưới ô SL: 'Không được nhỏ hơn 1'\n"
     "- Không lưu được"),

    ("007", "Số lượng vượt trần", "P1",
     "Dòng khách hàng đã điền các ô khác.",
     "1. Nhập SL = 1000000000 (một tỷ)",
     "SL: 1,000,000,000",
     "- Lỗi đỏ dưới ô SL: 'Tối đa 999999999'\n"
     "- Nhập đúng 999,999,999 thì hợp lệ"),

    ("008", "Số lượng là số thập phân", "P1",
     "Dòng khách hàng đã điền các ô khác.",
     "1. Gõ 2.5 vào ô SL\n"
     "2. Bấm ra ngoài ô",
     "SL: 2.5",
     "- Ô chỉ nhận phần nguyên (hiển thị 2 hoặc 25 tuỳ cách gõ), không lưu được số lẻ\n"
     "- Nếu kết quả nhỏ hơn 1 thì hiện lỗi 'Không được nhỏ hơn 1'"),

    ("009", "Số lượng là chữ", "P1",
     "Dòng khách hàng đã điền các ô khác.",
     "1. Gõ 'abc' vào ô SL",
     "SL: abc",
     "- Ô không nhận chữ, giữ trống\n"
     "- Bấm Lưu thì báo 'Không được nhỏ hơn 1'"),

    ("010", "Ngày cần là hôm nay", "P0",
     "Hôm nay là 03/09/2026, đang thêm dòng khách hàng mới.",
     "1. Mở lịch ở ô 'Ngày cần'\n"
     "2. Thử bấm vào ngày 03",
     "Ngày cần: 03/09/2026",
     "- ⚠️ Ngày hôm nay bị mờ, KHÔNG chọn được (phải từ ngày mai trở đi)\n"
     "- Các ngày 01, 02 cũng mờ"),

    ("011", "Ngày cần là ngày mai", "P1",
     "Hôm nay là 03/09/2026.",
     "1. Chọn ngày 04/09/2026 ở ô 'Ngày cần'",
     "Ngày cần: 04/09/2026",
     "- Chọn được, không báo lỗi\n"
     "- Ô hiển thị dạng 04/09/2026"),

    ("012", "Bỏ trống đơn vị tính", "P1",
     "Hàng hoá vừa thêm nhưng danh sách đơn vị tính rỗng nên ô ĐVT trống.",
     "1. Bấm 'Lưu nháp'",
     "—",
     "- Lỗi đỏ dưới ô ĐVT: 'Bắt buộc chọn'\n"
     "- Không lưu được"),

    ("013", "Bỏ trống ô Ghi chú của phiếu", "P1",
     "Form đã điền đủ các mục bắt buộc, riêng ô 'Ghi chú' của phiếu để trống.",
     "1. Bấm 'Lưu nháp'",
     "Ghi chú phiếu: (trống)",
     "- ⚠️ Lưu THÀNH CÔNG — ghi chú của phiếu KHÔNG bắt buộc\n"
     "- Màn chi tiết hiện dấu gạch ngang ở ô Ghi chú\n"
     "- Lưu ý phân biệt với ô 'Ghi chú' của TỪNG DÒNG khách hàng: ô đó BẮT BUỘC"),

    ("014", "Ký tự đặc biệt trong ghi chú", "P2",
     "Form Tạo mới.",
     "1. Nhập ghi chú có dấu tiếng Việt, ký tự < > & và biểu tượng cảm xúc\n"
     "2. Lưu rồi mở lại phiếu, rồi in phiếu",
     "Ghi chú: 'Giao gấp <ưu tiên> & đúng hẹn'",
     "- Nội dung hiển thị nguyên vẹn ở màn chi tiết\n"
     "- Bản in không hiện thẻ định dạng lạ, không bị vỡ bảng"),

    ("015", "Sửa lỗi xong thì lỗi tự biến mất", "P1",
     "Đang có lỗi đỏ 'Bắt buộc nhập' dưới ô Ghi chú của dòng khách hàng.",
     "1. Gõ nội dung vào ô Ghi chú của dòng đó",
     "Ghi chú dòng: 'Giao trước ngày lễ'",
     "- Lỗi đỏ biến mất ngay khi gõ, không cần bấm Lưu lại"),
]

S13 = [
    ("001", "Hai người cùng sửa một phiếu nháp", "P1",
     "Cùng một tài khoản A mở phiếu nháp P1 trên 2 trình duyệt.",
     "1. Trình duyệt 1 sửa ghi chú thành 'AAA' rồi lưu\n"
     "2. Trình duyệt 2 (mở từ trước) sửa ghi chú thành 'BBB' rồi lưu\n"
     "3. Mở lại phiếu",
     "—",
     "- Không văng lỗi hệ thống\n"
     "- Giá trị cuối cùng là 'BBB' (lần lưu sau ghi đè)\n"
     "- Lịch sử ghi đủ 2 lần sửa"),

    ("002", "Phiếu bị xóa trong lúc người khác đang mở màn chi tiết", "P1",
     "Tài khoản A mở màn chi tiết phiếu nháp P1 ở tab 1; ở tab 2 A xóa chính phiếu này.",
     "1. Ở tab 1, bấm nút 'Sửa'",
     "—",
     "- Hệ thống báo không tìm thấy dữ liệu và đưa về danh sách\n"
     "- Không treo trang, không hiện form Sửa trắng"),

    ("003", "Phiếu bị không duyệt trong lúc người lập đang mở form Sửa", "P1",
     "Phiếu P1 'Chờ duyệt'; kế toán kho không duyệt để đưa về 'Đang tạo'; người lập lúc đó đang "
     "xem màn chi tiết (chưa tải lại).",
     "1. Người lập tải lại màn chi tiết\n"
     "2. Quan sát",
     "—",
     "- Trạng thái đổi thành 'Đang tạo'\n"
     "- Nút 'Sửa' xuất hiện\n"
     "- Khối 'Ghi chú duyệt' hiện lý do từ chối"),

    ("004", "Xóa phiếu ở tab khác rồi bấm Xóa lại ở tab cũ", "P1",
     "Cùng phiếu nháp P1 mở trên 2 tab danh sách.",
     "1. Tab 1 xóa P1 thành công\n"
     "2. Tab 2 (chưa tải lại) bấm Xóa dòng P1 rồi xác nhận",
     "—",
     "- Tab 2 báo lỗi xóa thất bại kèm thông báo dữ liệu không còn\n"
     "- Danh sách tab 2 tự nạp lại, dòng P1 biến mất"),

    ("005", "Mở nhiều tab với bộ lọc khác nhau", "P2",
     "Tab 1 lọc Trạng thái 'Chờ duyệt', tab 2 lọc Trạng thái 'Đã phân bổ'.",
     "1. Thao tác qua lại giữa 2 tab, mỗi lần tải lại một tab",
     "—",
     "- Bộ lọc được ghi nhớ CHUNG cho màn, nên tab tải lại sau sẽ lấy bộ lọc lưu gần nhất\n"
     "- Không văng lỗi; muốn chắc chắn thì bấm 'Làm mới' trước khi đọc số liệu"),

    ("006", "Tải lại trang giữa lúc đang nhập form", "P1",
     "Form Tạo mới đã nhập ghi chú và 2 hàng hoá.",
     "1. Nhấn phím tải lại trang\n"
     "2. Đọc cảnh báo của trình duyệt rồi chọn rời trang",
     "—",
     "- Trình duyệt cảnh báo dữ liệu chưa lưu\n"
     "- Chọn rời trang thì form về trắng, không có phiếu nào được tạo"),

    ("007", "Mất kết nối khi đang lưu phiếu", "P2",
     "Form đã điền đủ, ngắt mạng ngay trước khi bấm Lưu.",
     "1. Bấm 'Lưu nháp'\n"
     "2. Nối mạng lại và mở danh sách",
     "—",
     "- Hệ thống báo lỗi lưu, vẫn ở form và giữ nguyên dữ liệu đã nhập\n"
     "- Không có phiếu rỗng hay phiếu thiếu hàng hoá được tạo ra"),
]

S14 = [
    ("001", "Luồng trọn vẹn: lập nháp → sửa → gửi duyệt → bị từ chối → gửi lại", "P0",
     "Tài khoản A thuộc công ty 4 (không có quyền Kế toán kho); tài khoản H có quyền 'Kế toán "
     "kho' công ty 4.",
     "1. A lập phiếu với 1 hàng hoá, 1 khách hàng, 1 file PDF rồi bấm 'Lưu nháp'\n"
     "2. A mở lại phiếu, bấm 'Sửa', thêm 1 dòng khách hàng, bấm 'Lưu và gửi duyệt'\n"
     "3. H mở phiếu, nhập ghi chú duyệt, bấm 'Không duyệt'\n"
     "4. A mở lại phiếu, sửa theo góp ý, bấm 'Lưu và gửi duyệt'\n"
     "5. H mở lại phiếu",
     "—",
     "- Bước 1: trạng thái 'Đang tạo', chỉ A nhìn thấy\n"
     "- Bước 2: trạng thái 'Chờ duyệt', H nhận thông báo, phiếu mất nút Sửa/Xóa\n"
     "- Bước 3: trạng thái về 'Đang tạo', A nhận thông báo từ chối, người tiếp nhận là H\n"
     "- Bước 4: trạng thái 'Chờ duyệt' trở lại, H nhận thông báo mới\n"
     "- Bước 5: H thấy đủ nút 'Không duyệt' và 'Tổng hợp'\n"
     "- Lịch sử phiếu ghi đủ các mốc theo đúng thứ tự thời gian"),

    ("002", "Luồng trọn vẹn: lập nháp rồi xóa bỏ", "P0",
     "Tài khoản A.",
     "1. A lập phiếu, bấm 'Lưu nháp'\n"
     "2. A mở lại phiếu kiểm tra nội dung\n"
     "3. A quay về danh sách, bấm Xóa và xác nhận\n"
     "4. Đếm lại tổng số phiếu",
     "—",
     "- Phiếu được tạo rồi xóa gọn, tổng số phiếu trở về đúng như trước khi lập\n"
     "- Không còn hàng hoá / dòng khách hàng mồ côi (tìm theo mã hàng không ra phiếu đã xóa)"),

    ("003", "Luồng trọn vẹn: kế toán kho tổng hợp phiếu sang màn xuất hàng", "P1",
     "Tài khoản H có quyền 'Kế toán kho'; phiếu P1 'Chờ duyệt' cùng công ty.",
     "1. H mở chi tiết P1\n"
     "2. Bấm 'Tổng hợp'\n"
     "3. Ở tab mới, kiểm tra màn lập phiếu đề nghị xuất hàng có mang sẵn phiếu P1",
     "—",
     "- Tab mới mở đúng màn lập phiếu đề nghị xuất hàng, có sẵn thông tin phiếu P1\n"
     "- Tab cũ giữ nguyên màn chi tiết, phiếu chưa đổi trạng thái\n"
     "- Trạng thái phiếu chỉ đổi khi bên kho hoàn tất thao tác của họ"),

    ("004", "Luồng trọn vẹn: lọc → xuất Excel → đối chiếu", "P1",
     "Tài khoản E, có 2.500 phiếu 'Chờ duyệt'.",
     "1. Lọc Trạng thái = 'Chờ duyệt'\n"
     "2. Ghi lại tổng số phiếu ở dòng đếm\n"
     "3. Bấm 'Xuất Excel', xuất đủ 6 trường\n"
     "4. Mở file và đếm số dòng dữ liệu",
     "—",
     "- Số dòng trong file bằng đúng tổng số phiếu ở dòng đếm trên lưới\n"
     "- Cột Mã yêu cầu trong file trùng khớp với các mã trên lưới"),

    ("005", "Luồng trọn vẹn: người mới không quyền dùng màn từ đầu tới cuối", "P0",
     "Tài khoản mới, không có quyền xem nào, chưa lập phiếu nào.",
     "1. Vào " + MENU + "\n"
     "2. Bấm 'Tạo mới', lập 1 phiếu đầy đủ, bấm 'Lưu và gửi duyệt'\n"
     "3. Về danh sách kiểm tra\n"
     "4. Mở chi tiết phiếu vừa lập\n"
     "5. Bấm 'In'",
     "—",
     "- Bước 1: danh sách trống, vẫn có nút 'Tạo mới'\n"
     "- Bước 2: lập và gửi duyệt được, không cần quyền riêng\n"
     "- Bước 3: danh sách có đúng 1 phiếu 'Chờ duyệt' của mình\n"
     "- Bước 4: xem được chi tiết (là người lập); KHÔNG có nút 'Không duyệt' và 'Tổng hợp'\n"
     "- Bước 5: in được phiếu của chính mình"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "TẠO MỚI PHIẾU", S4),
    ("V", "SỬA PHIẾU", S5),
    ("VI", "XEM CHI TIẾT PHIẾU", S6),
    ("VII", "KHÔNG DUYỆT & TỔNG HỢP", S7),
    ("VIII", "XÓA PHIẾU", S8),
    ("IX", "IN PHIẾU", S9),
    ("X", "XUẤT EXCEL", S10),
    ("XI", "LỊCH SỬ THAY ĐỔI", S11),
    ("XII", "RÀNG BUỘC NHẬP LIỆU", S12),
    ("XIII", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S13),
    ("XIV", "LUỒNG NGHIỆP VỤ TRỌN VẸN", S14),
]

if __name__ == "__main__":
    build(output_file=OUT,
          sheet_name="Trang tính1",
          feature_name="Phiếu yêu cầu chuyển hàng - Cập nhật ngày 03/09/2026",
          module_name=MODULE,
          description_block=DESCRIPTION_BLOCK,
          role_tcs=ROLE_TCS,
          sections=SECTIONS)
