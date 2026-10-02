# -*- coding: utf-8 -*-
"""Sinh tai lieu HUONG DAN TEST cho Redmine #11354 - Quan ly nhan su giai phap.

Dung chung engine cua skill hdsd-documenter (khung Word da duyet cua team).
Chay:  python .plans/solution-member-management/gen_huong_dan_test.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills",
                                "hdsd-documenter", "assets"))
from hdsd_engine import HdsdBuilder  # noqa: E402

OUT = os.path.join(HERE, "Huong dan test - 11354 Quan ly nhan su giai phap.docx")

b = HdsdBuilder(
    output=OUT,
    shots_dir=HERE,
    cover_title="(Hướng dẫn test - Quản lý nhân sự giải pháp - Redmine #11354)",
    doc_title="Hướng dẫn test - Quản lý nhân sự giải pháp",
)

# ============================================================ 1. TỔNG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Nội dung đã làm")
b.para(
    "Tab Nhân sự của màn Quản lý giải pháp trước đây chỉ Thêm được thành viên. "
    "Đợt này bổ sung 3 thao tác còn thiếu trên từng dòng thành viên: Sửa phân công, "
    "Khóa / Mở khóa (kèm chặn khi thành viên còn công việc tồn đọng) và Xóa (chặn khi "
    "thành viên đã phát sinh dữ liệu). Kèm theo là việc chuẩn hóa dữ liệu hiển thị của "
    "bảng nhân sự và hiệu lực của trạng thái Đã khóa trong phạm vi giải pháp."
)

b.h2("2. Phạm vi cần test")
b.table([
    ["#", "Nhóm chức năng", "Nội dung"],
    ["1", "Hiển thị bảng nhân sự",
     "Cột Trạng thái, Ngày kết thúc lấy đúng dữ liệu của thành viên; người vừa là Leader "
     "vừa là thành viên chỉ hiện 1 dòng"],
    ["2", "Quyền thao tác",
     "Ai được Sửa / Khóa / Xóa dòng nào; dòng PM và Leader hạng mục không có nút"],
    ["3", "Sửa phân công",
     "Đổi hạng mục, vai trò, mô tả, ngày bắt đầu, ngày kết thúc"],
    ["4", "Khóa / Mở khóa",
     "Khóa khi hết việc tồn đọng; chặn + hiện danh sách việc khi còn tồn đọng; "
     "Nhắc bàn giao; Mở khóa"],
    ["5", "Xóa có ràng buộc",
     "Xóa được khi chưa phát sinh dữ liệu; bị chặn khi đã phát sinh"],
    ["6", "Hiệu lực trạng thái Đã khóa",
     "Thành viên bị khóa không vào được giải pháp, không tạo Nhiệm vụ / Vấn đề / BOM"],
])

b.h2("3. Không nằm trong phạm vi đợt này")
b.bullet("Người quản lý KHÔNG lập phiếu bàn giao hộ thành viên. Popup việc tồn đọng chỉ để XEM "
         "và nhắc; thành viên phải tự vào màn Bàn giao công việc.")
b.bullet("Màn Bàn giao công việc giữ nguyên, không sửa gì trong đợt này.")
b.bullet("Việc phân loại nhân sự chính / cộng tác viên / đối tác (yêu cầu khác) chưa làm.")

b.h2("4. Màn hình cần vào")
b.para("Đường dẫn: /assign/solutions → mở 1 giải pháp → nút Quản lý → chọn tab Nhân sự "
       "(đường dẫn đầy đủ dạng /assign/solutions/{mã số giải pháp}/manager).")

# ============================================================ 2. CHUẨN BỊ
b.h1("CHUẨN BỊ TRƯỚC KHI TEST")

b.h2("1. Môi trường")
b.bullet("Mã nguồn nằm ở nhánh task_11354 của cả 2 kho (hrm-api và hrm-client), rẽ từ nhánh tpe. "
         "Cần đứng đúng nhánh này ở cả 2 kho, nếu không tab Nhân sự vẫn là bản cũ.")
b.bullet("Đợt này có thay đổi cấu trúc dữ liệu (bổ sung Ngày kết thúc và Trạng thái cho bản ghi "
         "thành viên), nên phải chạy cập nhật cấu trúc dữ liệu trước khi test. Các thành viên "
         "đang có sẵn sẽ được đưa về trạng thái Đang hoạt động.")

b.h2("2. Tài khoản cần chuẩn bị")
b.para("Chức năng này phân quyền theo VAI TRÒ TRONG GIẢI PHÁP, không theo quyền hệ thống. "
       "Cần tối thiểu 4 tài khoản để phủ hết các ca:")
b.table([
    ["Vai trò trong giải pháp", "Là ai", "Được thao tác trên"],
    ["Trưởng phòng giải pháp", "Người tạo ra giải pháp", "Mọi thành viên của giải pháp"],
    ["PM", "Người được phân công làm PM của giải pháp", "Mọi thành viên của giải pháp"],
    ["Leader hạng mục", "Người được chọn làm Leader của một hạng mục",
     "Chỉ thành viên thuộc hạng mục mình phụ trách"],
    ["Thành viên thường", "Người được thêm vào giải pháp / hạng mục",
     "Không được thao tác trên ai (dùng để test hiệu lực của trạng thái Đã khóa)"],
])

b.h2("3. Dữ liệu cần dựng")
b.para("Thành viên được lưu ở 2 chỗ khác nhau tùy loại giải pháp, nên PHẢI test trên cả 2 loại:")
b.table([
    ["Loại giải pháp", "Thành viên nằm ở đâu", "Ghi chú khi test"],
    ["Giải pháp KHÔNG chia hạng mục", "Thành viên của giải pháp",
     "Popup Sửa không có ô Hạng mục"],
    ["Giải pháp CÓ chia hạng mục", "Thành viên của hạng mục",
     "Popup Sửa có thêm ô Hạng mục (bắt buộc), đổi hạng mục là chuyển thành viên sang hạng mục khác"],
])
b.para("Chuẩn bị thêm, mỗi giải pháp nên có:")
b.bullet("1 thành viên CHƯA phát sinh gì (chưa tạo và chưa được giao Nhiệm vụ / Vấn đề / BOM) "
         "— dùng cho ca Xóa thành công.")
b.bullet("1 thành viên ĐÃ tạo hoặc đã được giao Nhiệm vụ / Vấn đề / BOM — dùng cho ca Xóa bị chặn.")
b.bullet("1 thành viên đang được giao ít nhất 2 Nhiệm vụ đang mở — dùng cho ca Khóa bị chặn.")
b.bullet("1 thành viên KHÔNG được giao việc nào đang mở — dùng cho ca Khóa thành công.")
b.bullet("1 người vừa là Leader hạng mục vừa được thêm làm thành viên của chính hạng mục đó "
         "— dùng để kiểm tra không bị nhân đôi dòng.")
b.bullet("1 giải pháp ở trạng thái Đã đóng — dùng để kiểm tra ẩn hết nút thao tác.")

b.h2("4. Cách xác định một công việc là ĐANG MỞ")
b.para("Khi khóa thành viên, hệ thống đếm các việc còn đang mở của người đó trong phạm vi giải "
       "pháp. Tester dựng dữ liệu theo đúng bảng sau:")
b.table([
    ["Đối tượng", "TÍNH là đang mở", "KHÔNG tính"],
    ["Nhiệm vụ (Task)",
     "Chờ phê duyệt triển khai · Chờ bắt đầu · Đang thực hiện · Tạm dừng · "
     "Hoàn thành - Chờ duyệt · Từ chối kết quả · Từ chối triển khai",
     "Nháp · Hoàn thành · Hủy"],
    ["Vấn đề (Issue)",
     "Đã phân công · Đang xử lý · Đã xử lý xong · Mở lại · Hoàn thành · Từ chối",
     "Mới ghi nhận · Đã đóng"],
])

# ============================================================ 3. CÁC BƯỚC TEST
b.h1("HƯỚNG DẪN TEST TỪNG CHỨC NĂNG")

# ---------- 3.1
b.h2("1. Bảng nhân sự và cột Thao tác")
b.para("Đăng nhập bằng tài khoản PM của giải pháp, vào tab Nhân sự.")
b.para("Kiểm tra bảng có đủ 9 cột: STT, Thành viên, Hạng mục, Vai trò, Ngày bắt đầu, "
       "Ngày kết thúc, Task đang phụ trách, Trạng thái, Thao tác.")
b.h3("Cần kiểm")
b.table([
    ["#", "Điểm kiểm", "Kết quả đúng"],
    ["1", "Dòng PM làm giải pháp", "Cột Thao tác hiển thị dấu — , không có nút nào"],
    ["2", "Dòng Leader hạng mục", "Cột Thao tác hiển thị dấu — , không có nút nào"],
    ["3", "Dòng thành viên thường", "Có đủ 3 nút: Sửa phân công, Khóa thành viên, Xóa khỏi giải pháp"],
    ["4", "Người vừa là Leader vừa là thành viên của chính hạng mục đó",
     "Chỉ hiện 1 dòng duy nhất, cột Vai trò ghi ghép cả hai vai trò"],
    ["5", "Cột Trạng thái",
     "Hiển thị đúng trạng thái của thành viên (Đang hoạt động / Đã khóa), không phải "
     "trạng thái của giải pháp"],
    ["6", "Cột Ngày kết thúc",
     "Hiển thị ngày kết thúc của chính thành viên đó; chưa nhập thì hiện dấu —"],
    ["7", "Mở giải pháp ở trạng thái Đã đóng",
     "Toàn bộ dòng đều không có nút thao tác, kể cả dòng thành viên"],
])
b.para("Lưu ý khi đối chiếu: dòng PM và dòng Leader hạng mục không phải là bản ghi thành viên "
       "mà lấy từ cấu hình giải pháp / hạng mục. Muốn đổi PM hoặc Leader phải dùng nút Phân công "
       "ở góc trên bên phải, không sửa ở cột Thao tác. Đây là thiết kế, không phải thiếu nút.")

# ---------- 3.2
b.h2("2. Phân quyền thao tác")
b.h3("2.1. Tài khoản Trưởng phòng giải pháp (người tạo giải pháp)")
b.bullet("Vào tab Nhân sự: mọi dòng thành viên đều có đủ 3 nút.")
b.h3("2.2. Tài khoản PM của giải pháp")
b.bullet("Vào tab Nhân sự: mọi dòng thành viên đều có đủ 3 nút.")
b.h3("2.3. Tài khoản Leader hạng mục")
b.bullet("Dòng thành viên THUỘC hạng mục mình phụ trách: có đủ 3 nút.")
b.bullet("Dòng thành viên của hạng mục KHÁC: không có nút nào.")
b.bullet("Dòng thành viên cấp giải pháp (giải pháp không chia hạng mục): không có nút nào.")
b.h3("2.4. Tài khoản không giữ vai trò nào trong giải pháp")
b.bullet("Không dòng nào có nút thao tác.")
b.h3("2.5. Kiểm tra chặn ở máy chủ (dành cho tester có kỹ thuật)")
b.para("Việc ẩn nút chỉ là lớp giao diện. Nếu gọi thẳng lệnh Sửa / Khóa / Xóa bằng công cụ "
       "kỹ thuật với tài khoản không đủ vai trò, hệ thống vẫn phải từ chối và báo: "
       "“Bạn không có quyền thao tác trên thành viên này.”")

# ---------- 3.3
b.h2("3. Sửa phân công thành viên")
b.para("Bấm nút Sửa phân công (biểu tượng bút chì) ở dòng thành viên. Popup "
       "“Sửa phân công thành viên” mở ra, dòng đầu ghi tên thành viên đang sửa.")
b.h3("3.1. Các trường trong popup")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị hiển thị sẵn khi mở"],
    ["Hạng mục", "Danh sách chọn (chỉ hiện với giải pháp có chia hạng mục)", "Có",
     "Hạng mục thành viên đang thuộc"],
    ["Vai trò dự án", "Danh sách chọn", "Không", "Vai trò đang được phân công"],
    ["Mô tả công việc", "Ô nhập nhiều dòng", "Không", "Mô tả đang có"],
    ["Ngày bắt đầu", "Ô chọn ngày", "Không", "Ngày bắt đầu đang có"],
    ["Ngày kết thúc", "Ô chọn ngày", "Không", "Ngày kết thúc đang có, chưa có thì để trống"],
])
b.para("Cuối popup có 2 nút: Lưu và Hủy.")
b.h3("3.2. Các ca cần test")
b.table([
    ["#", "Thao tác", "Kết quả đúng"],
    ["1", "Đổi Vai trò dự án rồi bấm Lưu",
     "Popup đóng, hiện thông báo “Đã cập nhật phân công”, cột Vai trò trên bảng đổi ngay"],
    ["2", "Nhập Ngày kết thúc rồi bấm Lưu",
     "Cột Ngày kết thúc trên bảng hiển thị đúng ngày vừa nhập"],
    ["3", "Nhập Ngày kết thúc NHỎ HƠN Ngày bắt đầu rồi bấm Lưu",
     "Hệ thống báo lỗi đỏ dưới ô Ngày kết thúc: “Ngày kết thúc phải từ ngày bắt đầu trở đi.”, "
     "popup KHÔNG đóng, dữ liệu không đổi"],
    ["4", "Sửa Mô tả công việc rồi bấm Lưu", "Lưu thành công, mở lại popup thấy mô tả mới"],
    ["5", "Bấm Hủy sau khi đã sửa vài ô", "Popup đóng, dữ liệu trên bảng giữ nguyên như cũ"],
])
b.h3("3.3. Riêng giải pháp CÓ chia hạng mục")
b.table([
    ["#", "Thao tác", "Kết quả đúng"],
    ["1", "Đổi Hạng mục sang hạng mục khác của cùng giải pháp rồi Lưu",
     "Thành viên chuyển sang hạng mục mới, cột Hạng mục trên bảng đổi theo, sơ đồ cấu trúc "
     "nhân sự bên dưới cũng vẽ lại đúng nhánh mới"],
    ["2", "Đổi Hạng mục sang hạng mục MÀ NGƯỜI NÀY ĐÃ LÀ THÀNH VIÊN rồi Lưu",
     "Hệ thống chặn, báo lỗi “Nhân sự đã có trong hạng mục này.”, popup không đóng"],
    ["3", "Sau khi chuyển hạng mục, kiểm tra các Nhiệm vụ / Vấn đề cũ của người đó",
     "Dữ liệu cũ vẫn còn nguyên, không bị mất (hệ thống chuyển bản ghi chứ không xóa tạo lại)"],
])

# ---------- 3.4
b.h2("4. Khóa thành viên - trường hợp KHÔNG còn việc tồn đọng")
b.para("Chọn thành viên không được giao việc nào đang mở. Bấm nút Khóa thành viên "
       "(biểu tượng ổ khóa).")
b.bullet("Hộp xác nhận hiện ra, tiêu đề “Xác nhận khóa thành viên”, nội dung: "
         "Khóa “<tên thành viên>”? Thành viên sẽ không tạo thêm BOM, Task hay Issue trong "
         "giải pháp này nữa. Dữ liệu cũ vẫn giữ nguyên. Hai nút: Khóa và Hủy.")
b.bullet("Bấm Hủy: không có gì thay đổi.")
b.bullet("Bấm Khóa: hiện thông báo “Đã khóa thành viên”; cột Trạng thái của dòng đó chuyển "
         "sang Đã khóa; nút ổ khóa đổi thành nút Mở khóa thành viên.")
b.bullet("Bấm Khóa lần nữa trên thành viên đã khóa (bằng cách gọi thẳng lệnh, do giao diện đã "
         "đổi nút): hệ thống báo “Thành viên đã ở trạng thái Đã khóa.”")

b.h2("5. Khóa thành viên - trường hợp CÒN việc tồn đọng")
b.para("Chọn thành viên đang được giao ít nhất 2 Nhiệm vụ đang mở. Bấm nút Khóa thành viên rồi "
       "xác nhận Khóa.")
b.h3("5.1. Kết quả đúng")
b.bullet("Hệ thống KHÔNG khóa. Popup “Bàn giao công việc tồn đọng trước khi khóa thành viên” "
         "mở ra ngay, không phải bấm thêm gì.")
b.bullet("Dòng đầu popup ghi: <tên thành viên> còn <số lượng> công việc chưa hoàn tất trong "
         "giải pháp này. Con số phải khớp với số việc đang mở đã dựng.")
b.bullet("Bảng Task liệt kê đủ các nhiệm vụ đang mở, có các cột: Mã, Tên task, Hạn, Bàn giao.")
b.bullet("Bảng Issue liệt kê đủ các vấn đề đang mở, có các cột: Mã, Tiêu đề, Hạn, Bàn giao.")
b.bullet("Popup CHỈ ĐỂ XEM - không có nút nào lập phiếu bàn giao hộ.")
b.bullet("Cuối popup có 3 nút: Nhắc bàn giao, Mở màn Bàn giao, Đóng.")
b.h3("5.2. Cột Bàn giao trong popup")
b.table([
    ["Tình huống dựng", "Cột Bàn giao hiển thị"],
    ["Công việc chưa nằm trong phiếu bàn giao nào", "Chưa bàn giao"],
    ["Công việc đã nằm trong phiếu bàn giao đang chờ duyệt",
     "Đã nằm trong phiếu <mã phiếu> — <trạng thái phiếu>"],
])
b.para("Lưu ý quan trọng: việc đã nằm trong phiếu bàn giao chờ duyệt VẪN tính là tồn đọng và "
       "vẫn chặn khóa. Chỉ khi phiếu được duyệt và việc thực sự chuyển sang người khác thì số "
       "tồn đọng mới về 0. Đây là thiết kế, không phải lỗi.")
b.h3("5.3. Nút Nhắc bàn giao")
b.bullet("Bấm Nhắc bàn giao: hiện thông báo “Đã gửi nhắc bàn giao cho thành viên”.")
b.bullet("Đăng nhập bằng tài khoản thành viên bị nhắc, mở chuông thông báo: có thông báo mới "
         "dạng [BGCV] Nhắc báo cáo: <tên giải pháp in đậm>. Còn <số> công việc cần bàn giao. "
         "<tên người nhắc> nhắc.")
b.bullet("Bấm vào thông báo: chuyển sang màn Bàn giao công việc đúng giải pháp đang xét.")
b.bullet("Tên giải pháp quá dài phải bị cắt còn tối đa 50 ký tự, có dấu ba chấm ở cuối.")
b.h3("5.4. Nút Mở màn Bàn giao")
b.bullet("Bấm Mở màn Bàn giao: chuyển sang màn /assign/handover.")
b.h3("5.5. Khép vòng - sau khi bàn giao xong")
b.bullet("Đăng nhập tài khoản thành viên, lập phiếu bàn giao ở màn Bàn giao công việc, "
         "chuyển hết việc đang mở sang người khác, và để phiếu được duyệt / tiếp nhận.")
b.bullet("Quay lại tab Nhân sự bằng tài khoản PM, bấm Khóa thành viên đó: lúc này khóa được, "
         "hiện thông báo “Đã khóa thành viên”.")

b.h2("6. Mở khóa thành viên")
b.bullet("Ở dòng thành viên đang Đã khóa, bấm nút Mở khóa thành viên.")
b.bullet("Hộp xác nhận “Xác nhận mở khóa”, nội dung: Mở khóa “<tên>”? Thành viên tham gia lại "
         "giải pháp như bình thường.")
b.bullet("Xác nhận: hiện thông báo “Đã mở khóa thành viên”, cột Trạng thái trở lại "
         "Đang hoạt động, nút đổi lại thành Khóa thành viên.")
b.bullet("Kiểm tra bằng tài khoản thành viên: vào lại được giải pháp và tạo được Nhiệm vụ / "
         "Vấn đề / BOM như trước.")

# ---------- 3.5
b.h2("7. Xóa thành viên khỏi giải pháp")
b.para("Bấm nút Xóa khỏi giải pháp (biểu tượng thùng rác, màu đỏ). Hộp xác nhận "
       "“Xác nhận xóa thành viên” hiện ra với nội dung: Xóa “<tên>” khỏi danh sách nhân sự "
       "giải pháp?")
b.h3("7.1. Thành viên CHƯA phát sinh dữ liệu")
b.bullet("Xác nhận Xóa: hiện thông báo “Đã xóa thành viên khỏi giải pháp”, dòng đó biến mất "
         "khỏi bảng, số Nhân sự ở sơ đồ cấu trúc bên dưới giảm đi 1.")
b.h3("7.2. Thành viên ĐÃ phát sinh dữ liệu")
b.para("Hệ thống chặn xóa nếu thành viên, trong phạm vi giải pháp đang xét, thuộc một trong "
       "các trường hợp:")
b.bullet("Đã tạo BOM;")
b.bullet("Đã tạo Nhiệm vụ, hoặc đang được giao Nhiệm vụ;")
b.bullet("Đã tạo Vấn đề, hoặc đang được giao Vấn đề.")
b.para("Kết quả đúng: không xóa được, hệ thống báo NGUYÊN VĂN câu sau (tester đối chiếu "
       "từng chữ): “Thành viên đã phát sinh dữ liệu (BOM/Task/Issue). Vui lòng sử dụng chức "
       "năng Khóa để bảo toàn dữ liệu hệ thống.”")
b.para("Lưu ý phân biệt: điều kiện CHẶN XÓA rộng hơn điều kiện CHẶN KHÓA. Một thành viên đã "
       "làm xong hết việc (không còn việc đang mở) thì KHÓA ĐƯỢC nhưng vẫn KHÔNG XÓA ĐƯỢC, "
       "vì dữ liệu cũ do người đó tạo vẫn còn. Đây là thiết kế.")
b.h3("7.3. Ca bảo vệ dữ liệu")
b.bullet("Thử xóa một thành viên bằng cách sửa mã số trên đường dẫn thành mã của thành viên "
         "thuộc GIẢI PHÁP KHÁC: hệ thống phải báo “Không tìm thấy thành viên trong giải pháp "
         "này. Vui lòng tải lại danh sách.” và không xóa nhầm.")
b.bullet("Thử thao tác trên dòng PM hoặc Leader hạng mục bằng công cụ kỹ thuật: hệ thống báo "
         "“Chỉ thao tác được trên thành viên. PM và Leader hạng mục thay đổi qua chức năng "
         "Phân công.”")

# ---------- 3.6
b.h2("8. Hiệu lực của trạng thái Đã khóa")
b.para("Sau khi khóa một thành viên, đăng nhập bằng chính tài khoản thành viên đó và kiểm tra "
       "trong phạm vi giải pháp bị khóa:")
b.table([
    ["#", "Thao tác của thành viên bị khóa", "Kết quả đúng"],
    ["1", "Mở màn Quản lý giải pháp đó",
     "Bị chặn, hệ thống báo “Bạn đã bị khóa khỏi giải pháp này nên không thao tác được. "
     "Vui lòng liên hệ PM hoặc Trưởng phòng giải pháp.”"],
    ["2", "Tạo Nhiệm vụ mới trong giải pháp đó", "Bị chặn, báo đúng câu trên"],
    ["3", "Tạo Vấn đề mới trong giải pháp đó", "Bị chặn, báo đúng câu trên"],
    ["4", "Tạo BOM trong giải pháp đó", "Bị chặn, báo đúng câu trên"],
    ["5", "Mở một giải pháp KHÁC mà mình không bị khóa",
     "Vào bình thường, không bị chặn oan"],
    ["6", "Xem lại Nhiệm vụ / Vấn đề / BOM cũ do mình tạo",
     "Dữ liệu cũ vẫn còn nguyên, không bị xóa"],
])

# ============================================================ 4. LƯU Ý
b.h1("CÁC ĐIỂM ĐÃ BIẾT - KHÔNG PHẢI LỖI")
b.para("Ba điểm dưới đây đã được thống nhất chấp nhận trong đợt này, tester gặp thì KHÔNG ghi "
       "nhận là lỗi:")
b.table([
    ["#", "Hiện tượng", "Lý do"],
    ["1",
     "Cột “Task đang phụ trách” trên bảng hiện 0 nhưng bấm Khóa lại bị chặn vì còn việc tồn đọng",
     "Cột đếm trên bảng dùng bộ trạng thái cũ, thiếu trạng thái Từ chối triển khai. Việc sửa bộ "
     "trạng thái cũ ảnh hưởng nhiều màn khác nên đợt này giữ nguyên"],
    ["2",
     "Vấn đề ở trạng thái Đã xử lý xong / Hoàn thành / Từ chối vẫn bị tính là tồn đọng, "
     "chặn khóa thành viên",
     "Lấy đúng tập trạng thái mà màn Bàn giao đang cho bàn giao, để không sinh ra việc "
     "không bàn giao được. Sửa sẽ phải đổi hành vi màn Bàn giao đang chạy thật"],
    ["3",
     "Việc đã nằm trong phiếu bàn giao chờ duyệt vẫn tính là tồn đọng",
     "Phiếu chưa duyệt thì việc chưa sang tay ai. Nếu bỏ đếm ở bước này, người quản lý khóa "
     "được ngay trong khi việc còn treo vô chủ"],
])

b.h1("DỌN DỮ LIỆU SAU KHI TEST")
b.bullet("Mở khóa lại các thành viên đã khóa trong lúc test.")
b.bullet("Thêm lại các thành viên đã xóa, hoặc khôi phục về đúng danh sách ban đầu.")
b.bullet("Trả các Nhiệm vụ / Vấn đề mượn để dựng ca tồn đọng về người phụ trách cũ và "
         "trạng thái cũ.")
b.bullet("Xóa các phiếu bàn giao và thông báo tạo ra trong lúc test.")
b.bullet("Trả PM / Leader hạng mục về đúng người ban đầu nếu có đổi để test quyền.")

b.h1("ĐỐI CHIẾU VỚI BỘ TEST CASE")
b.para("Bộ test case chi tiết của yêu cầu này gồm 48 ca, mã từ TC-ROLE-92 đến TC-ROLE-139, nằm "
       "ở file “testcase - 11354 Quan ly nhan su giai phap.xlsx” cùng thư mục tài liệu, chia "
       "theo 6 nhóm: quyền thao tác · cập nhật phân công · khóa và mở khóa · xóa có ràng buộc · "
       "hiệu lực của trạng thái Đã khóa · hiển thị và dữ liệu bảng. Tài liệu này là phần hướng "
       "dẫn cách dựng dữ liệu và trình tự thao tác cho bộ test case đó, hai file dùng kèm nhau.")

b.finish()
print("Xong:", OUT)
