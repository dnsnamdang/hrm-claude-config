# -*- coding: utf-8 -*-
"""Testcase #11130 - Loai meeting: gan Phieu tong hop ket qua meeting."""
import os, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build

MODULE = "Phiếu tổng hợp kết quả meeting"
FEATURE = "Loại meeting - Phiếu tổng hợp kết quả meeting"

MAU = 'Mẫu phiếu "Tổng hợp kết quả meeting KH"'
C1 = 'Câu 1 "Khách hàng có nhu cầu đầu tư không?"'
C2 = 'Câu 2 "Mức đầu tư dự kiến (triệu đồng)"'
C3 = 'Câu 3 "Ghi chú kết quả"'

DATA_MAU = (
    f'{MAU} (trạng thái Hoạt động) gồm 3 câu:\n'
    f'- {C1}: chọn Có/Không, BẮT BUỘC\n'
    f'- {C2}: nhập số, BẮT BUỘC, chỉ hiển thị khi Câu 1 = "Có"\n'
    f'- {C3}: nhập chữ, không bắt buộc'
)
DATA_LM = ('Loại meeting "Họp khách hàng 11130" đang Hoạt động, đã bật '
           '"Gán phiếu tổng hợp kết quả meeting" và chọn ' + MAU)
DATA_BB = ('Biên bản meeting "TPE.MET.KH.26.0050" thuộc loại meeting "Họp khách hàng 11130", '
           'trạng thái Chốt lịch, tài khoản đăng nhập là người chủ trì')

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     'Cho phép cấu hình trên từng Loại meeting một bộ câu hỏi tổng hợp kết quả (lấy từ danh mục '
     'Mẫu phiếu thu thập thông tin). Biên bản của meeting thuộc loại đó sẽ tự hiện phần "Phiếu tổng '
     'hợp kết quả meeting" dựng đúng theo bộ câu hỏi được gán; người dùng trả lời, lưu cùng biên bản; '
     'còn câu bắt buộc chưa trả lời thì không được chuyển biên bản sang Hoàn thành.'),
    ("2. Đối tượng được tính / hiển thị",
     'Phần "Phiếu tổng hợp kết quả meeting" CHỈ hiện ở tab Biên bản của meeting khi loại meeting của '
     'meeting đó thoả CẢ HAI: (a) công tắc "Gán phiếu tổng hợp kết quả meeting" đang bật, (b) đã chọn '
     'một mẫu phiếu. Ô chọn mẫu phiếu trong Loại meeting chỉ liệt kê mẫu phiếu ở trạng thái Hoạt động. '
     'Câu hỏi trong phiếu chỉ hiện khi thoả luật rẽ nhánh của mẫu (câu không có luật thì luôn hiện).'),
    ("3. Đối tượng bị ẩn / không tính",
     'Loại meeting tắt công tắc, hoặc bật nhưng chưa chọn mẫu thì biên bản KHÔNG hiện phần phiếu. '
     'Mẫu phiếu trạng thái Nháp và Khoá KHÔNG được liệt kê để gán. Câu hỏi đang bị ẩn bởi luật rẽ '
     'nhánh thì KHÔNG bị tính là "câu bắt buộc còn thiếu" khi bấm Hoàn thành. '
     'Phiếu khảo sát nhu cầu đầu tư cũ của loại meeting "Họp tìm hiểu & Giới thiệu sản phẩm" là khối '
     'RIÊNG, chạy song song, không nằm trong phạm vi tính năng này.'),
    ("4. Bộ lọc thời gian áp dụng cho",
     'Không áp dụng - tính năng là cấu hình danh mục và nhập liệu trên biên bản, không có bộ lọc '
     'theo khoảng thời gian.'),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     'Loại meeting trỏ tới 1 Mẫu phiếu. Mẫu phiếu gồm: Phân vùng > Nhóm câu hỏi > Câu hỏi, và '
     'câu hỏi có thể có câu con. Đáp án lưu gắn với từng meeting, mở lại biên bản là hiện đúng đáp án '
     'đã lưu của meeting đó.'),
    ("6. Quy tắc cộng dồn / deduplicate",
     'Mỗi meeting chỉ có 1 bộ đáp án của phiếu. Lưu biên bản nhiều lần thì GHI ĐÈ bộ đáp án cũ, không '
     'sinh thêm bản ghi trùng. Tắt công tắc ở Loại meeting thì mẫu phiếu đang chọn bị bỏ theo (không '
     'giữ lại tham chiếu cũ).'),
    ("7. Phân quyền cấp",
     'Cấu hình trên Loại meeting: "Quản lý danh mục loại meeting" (thêm/sửa), "Xem danh mục loại '
     'meeting" (chỉ xem). Nguồn mẫu phiếu: "Quản lý danh mục mẫu phiếu thu thập thông tin". '
     'Nhập phiếu trên biên bản đi theo quyền của màn meeting sẵn có: "Xem danh sách meeting theo tổng '
     'công ty" / "Xem danh sách meeting theo công ty" / "Xem danh sách meeting theo phòng ban" / '
     '"Xem danh sách meeting theo bộ phận"; quyền sửa biên bản giữ nguyên luật cũ (người tạo, người '
     'chủ trì).'),
    ("8. Cách tính các ô thống kê",
     'Không áp dụng - tính năng không có ô thống kê hay tổng hợp số liệu.'),
    ("9. Ghi chú đọc bảng",
     'Bẫy dễ sai nhất: (1) Câu bị ẩn theo rẽ nhánh KHÔNG được đòi bắt buộc - nếu hệ thống vẫn đòi thì '
     'biên bản không bao giờ Hoàn thành được; (2) Đổi đáp án câu cha phải làm câu con hiện/ẩn NGAY, '
     'không cần lưu hay tải lại trang; (3) Giá trị số 0 VẪN là câu trả lời hợp lệ, không được coi là '
     'bỏ trống; (4) Lưu biên bản KHÔNG bị chặn bởi câu bắt buộc - chỉ nút Hoàn thành mới chặn; '
     '(5) Chốt chặn thật nằm ở máy chủ, nên phải chạy thêm nhóm gọi thẳng chức năng, bỏ qua giao diện.'),
]

ROLE_TCS = [
    ("00", 'Tài khoản có quyền "Quản lý danh mục loại meeting" cấu hình được phiếu', "P0",
     'Tài khoản A chỉ có quyền "Quản lý danh mục loại meeting". Có sẵn ' + MAU,
     '1. Đăng nhập tài khoản A\n2. Vào Danh mục > Loại meeting\n3. Bấm Sửa loại meeting '
     '"Họp khách hàng 11130"\n4. Bật công tắc "Gán phiếu tổng hợp kết quả meeting"\n'
     '5. Chọn mẫu phiếu rồi bấm Lưu',
     'Mẫu phiếu: Tổng hợp kết quả meeting KH',
     '- Công tắc và ô Mẫu phiếu bấm được, không bị mờ\n'
     '- Lưu thành công, hiện thông báo thành công\n'
     '- Mở lại vẫn thấy công tắc bật và đúng mẫu phiếu vừa chọn'),
    ("01", 'Tài khoản chỉ có quyền "Xem danh mục loại meeting" không sửa được cấu hình', "P0",
     'Tài khoản B chỉ có quyền "Xem danh mục loại meeting". ' + DATA_LM,
     '1. Đăng nhập tài khoản B\n2. Vào Danh mục > Loại meeting\n'
     '3. Mở xem loại meeting "Họp khách hàng 11130"',
     '—',
     '- Vẫn đọc được tên mẫu phiếu đang gán\n'
     '- Công tắc "Gán phiếu tổng hợp kết quả meeting" và ô Mẫu phiếu KHÔNG bấm/đổi được\n'
     '- Không thấy nút Lưu'),
    ("02", 'Tài khoản không có quyền nào về loại meeting', "P0",
     'Tài khoản C không được gán quyền nào thuộc nhóm Danh mục',
     '1. Đăng nhập tài khoản C\n2. Mở menu Danh mục\n3. Gõ thẳng địa chỉ màn Loại meeting',
     '—',
     '- Không thấy mục Loại meeting trong menu\n'
     '- Vào bằng địa chỉ trực tiếp thì hệ thống từ chối, báo không có quyền'),
    ("03", 'Không có quyền mẫu phiếu thì ô chọn mẫu phiếu không treo màn', "P1",
     'Tài khoản D có "Quản lý danh mục loại meeting" nhưng KHÔNG có "Quản lý danh mục mẫu phiếu '
     'thu thập thông tin"',
     '1. Đăng nhập tài khoản D\n2. Mở Sửa loại meeting\n'
     '3. Bật công tắc "Gán phiếu tổng hợp kết quả meeting"\n4. Mở ô Mẫu phiếu',
     '—',
     '- Màn hình không treo, không văng lỗi đỏ toàn trang\n'
     '- Ô Mẫu phiếu hiện danh sách rỗng\n'
     '- ⚠️ Không được bung thông báo lỗi kỹ thuật khó hiểu cho người dùng'),
    ("04", "Bỏ qua giao diện, gọi thẳng chức năng Lưu loại meeting với mẫu phiếu Nháp", "P0",
     'Có mẫu phiếu "Phiếu nháp 11130" đang ở trạng thái Nháp. Tài khoản A có quyền quản lý danh mục '
     'loại meeting',
     '1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu loại meeting, bỏ qua giao diện\n'
     '2. Truyền công tắc gán phiếu = bật và mẫu phiếu là "Phiếu nháp 11130"',
     'Mẫu phiếu: Phiếu nháp 11130 (Nháp)',
     '- Hệ thống từ chối lưu\n'
     '- Báo lỗi rõ mẫu phiếu chưa được phát hành, không gán được cho loại meeting\n'
     '- ⚠️ Kiểm lại trong danh mục: loại meeting vẫn giữ cấu hình cũ, không bị đổi'),
    ("05", "Bỏ qua giao diện, gọi thẳng chức năng Hoàn thành biên bản khi thiếu câu bắt buộc", "P0",
     DATA_LM + ". " + DATA_BB + ". " + DATA_MAU,
     '1. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu biên bản với trạng thái Hoàn thành\n'
     '2. Không truyền đáp án nào của phiếu',
     'Trạng thái: Hoàn thành; đáp án phiếu: để trống',
     '- Hệ thống từ chối, không cho chuyển sang Hoàn thành\n'
     '- Thông báo nêu rõ tên câu còn thiếu: "Phiếu tổng hợp kết quả meeting còn thiếu câu bắt buộc: '
     'Khách hàng có nhu cầu đầu tư không?"\n'
     '- ⚠️ Biên bản giữ nguyên trạng thái cũ (Chốt lịch)'),
    ("06", "Bỏ qua giao diện, người ngoài phạm vi xem meeting gọi thẳng chức năng lưu đáp án", "P0",
     'Tài khoản E không thuộc phạm vi xem meeting "TPE.MET.KH.26.0050" (khác phòng ban, không có '
     'quyền xem theo tổng công ty)',
     '1. Đăng nhập tài khoản E để lấy phiên làm việc\n'
     '2. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu biên bản của meeting đó kèm đáp án phiếu',
     'Đáp án Câu 1: Có',
     '- Hệ thống từ chối, báo không có quyền\n'
     '- ⚠️ Mở lại biên bản bằng tài khoản chủ trì: đáp án KHÔNG bị ghi đè'),
]

S1 = [
    ("001", 'Loại meeting có gán phiếu thì biên bản hiện phân vùng phiếu', "P0",
     DATA_LM + ". " + DATA_BB,
     '1. Vào Giao việc > Meeting\n2. Mở meeting "TPE.MET.KH.26.0050"\n3. Chuyển sang tab Biên bản',
     '—',
     '- Có phân vùng tiêu đề "Phiếu tổng hợp kết quả meeting" kèm biểu tượng phiếu\n'
     '- Phân vùng nằm ở phần trên của tab Biên bản, trước mục "Nội dung meeting"\n'
     '- Bên trong hiện đúng 2 câu đang tới lượt: "Khách hàng có nhu cầu đầu tư không?" và '
     '"Ghi chú kết quả"'),
    ("002", "Loại meeting KHÔNG gán phiếu thì biên bản giữ nguyên như cũ", "P0",
     'Loại meeting "Họp nội bộ 11130" đang tắt công tắc "Gán phiếu tổng hợp kết quả meeting". '
     'Có meeting thuộc loại này ở trạng thái Chốt lịch',
     '1. Mở meeting của loại "Họp nội bộ 11130"\n2. Chuyển sang tab Biên bản',
     '—',
     '- KHÔNG có phân vùng "Phiếu tổng hợp kết quả meeting"\n'
     '- Các mục cũ của biên bản (Nội dung meeting, Kết luận, Ghi chú, Tài liệu) hiển thị bình thường'),
    ("003", "Bật công tắc nhưng chưa chọn mẫu thì biên bản không hiện phiếu", "P1",
     'Dữ liệu cũ có loại meeting bật công tắc nhưng chưa có mẫu phiếu',
     '1. Mở meeting thuộc loại meeting đó\n2. Chuyển sang tab Biên bản',
     '—',
     '- KHÔNG hiện phân vùng phiếu\n'
     '- ⚠️ Không hiện khung phiếu rỗng, không báo lỗi đỏ trên màn'),
    ("004", "Tên mẫu phiếu hiển thị đúng trên biên bản", "P1",
     DATA_LM + ". " + DATA_BB,
     '1. Mở tab Biên bản\n2. Đọc tiêu đề bên trong phân vùng phiếu',
     '—',
     '- Hiện đúng tên mẫu phiếu đang gán: "Tổng hợp kết quả meeting KH"\n'
     '- Không hiện mã kỹ thuật hay ký tự lạ'),
    ("005", "Xem biên bản ở chế độ chỉ đọc vẫn thấy đáp án đã lưu", "P1",
     DATA_LM + '. Meeting đã Hoàn thành, đã có đáp án: Câu 1 = "Có", Câu 2 = 500, '
     'Câu 3 = "Khách quan tâm dòng máy A". Tài khoản đăng nhập chỉ được xem',
     '1. Mở meeting đã Hoàn thành\n2. Chuyển sang tab Biên bản',
     '—',
     '- Phân vùng phiếu hiện đủ 3 câu kèm đáp án đã lưu\n- Các ô nhập không sửa được'),
    ("006", "Không tải được bộ câu hỏi của mẫu phiếu", "P2",
     'Mẫu phiếu đang gán bị xoá hoặc không truy cập được',
     '1. Mở tab Biên bản của meeting thuộc loại meeting đó',
     '—',
     '- Màn hình không treo, các mục khác của biên bản vẫn dùng được\n'
     '- ⚠️ Không hiện khung phiếu vỡ, không treo mãi dòng chữ '
     '"Đang tải phiếu tổng hợp kết quả meeting..."'),
]

S2 = [
    ("001", 'Công tắc gán phiếu hiện trong cửa sổ Thêm loại meeting', "P0",
     'Tài khoản có quyền "Quản lý danh mục loại meeting"',
     '1. Vào Danh mục > Loại meeting\n2. Bấm nút Thêm mới',
     '—',
     '- Cửa sổ thêm mới có dòng "Gán phiếu tổng hợp kết quả meeting" kèm ô đánh dấu\n'
     '- Mặc định đang TẮT\n- Khi tắt thì KHÔNG hiện ô Mẫu phiếu'),
    ("002", "Bật công tắc thì hiện ô Mẫu phiếu kèm dòng giải thích", "P0",
     'Đang mở cửa sổ Thêm loại meeting',
     '1. Bấm vào ô đánh dấu "Gán phiếu tổng hợp kết quả meeting"',
     '—',
     '- Hiện ô "Mẫu phiếu" có dấu * bắt buộc\n'
     '- Ô trống hiện chữ mờ "Chọn mẫu phiếu thu thập thông tin"\n'
     '- Bên dưới có dòng giải thích: "Biên bản của loại meeting này sẽ hiện phần \\"Phiếu tổng hợp '
     'kết quả meeting\\" dựng theo bộ câu hỏi của mẫu phiếu đã chọn."\n'
     '- ⚠️ Dòng giải thích phải là chữ XÁM, không được tô đỏ'),
    ("003", "Bấm vào chữ cạnh ô đánh dấu cũng bật/tắt được công tắc", "P2",
     'Đang mở cửa sổ Thêm loại meeting',
     '1. Bấm vào dòng chữ "Gán phiếu tổng hợp kết quả meeting" (không bấm vào ô vuông)',
     '—',
     '- Công tắc đổi trạng thái như khi bấm vào ô vuông'),
    ("004", "Ô Mẫu phiếu chỉ liệt kê mẫu đang Hoạt động", "P0",
     'Danh mục Mẫu phiếu thu thập thông tin có: "Tổng hợp kết quả meeting KH" (Hoạt động), '
     '"Phiếu nháp 11130" (Nháp), "Phiếu cũ 11130" (Khoá)',
     '1. Mở cửa sổ Thêm loại meeting\n2. Bật công tắc gán phiếu\n3. Mở ô Mẫu phiếu',
     '—',
     '- Danh sách CHỈ có "Tổng hợp kết quả meeting KH"\n'
     '- ⚠️ KHÔNG có "Phiếu nháp 11130" và "Phiếu cũ 11130"'),
    ("005", "Tên mẫu phiếu trong danh sách chọn có kèm mã", "P2",
     'Mẫu phiếu "Tổng hợp kết quả meeting KH" có mã "MP-MEET-01"',
     '1. Mở ô Mẫu phiếu trong cửa sổ loại meeting',
     '—',
     '- Dòng chọn hiện dạng "MP-MEET-01 — Tổng hợp kết quả meeting KH"\n'
     '- Mẫu không có mã thì chỉ hiện tên, không hiện dấu gạch thừa'),
    ("006", "Tìm mẫu phiếu bằng cách gõ trong ô chọn", "P1",
     'Danh mục có ít nhất 5 mẫu phiếu đang Hoạt động, trong đó có "Tổng hợp kết quả meeting KH"',
     '1. Mở ô Mẫu phiếu\n2. Gõ "tổng hợp"',
     'Từ khoá: tổng hợp',
     '- Danh sách lọc còn các mẫu có chứa từ khoá\n- Chọn được mẫu từ kết quả lọc'),
    ("007", "Bật công tắc mà không chọn mẫu phiếu thì không lưu được", "P0",
     'Đang mở cửa sổ Thêm loại meeting, đã nhập Tên loại meeting "Họp thử 11130"',
     '1. Bật công tắc gán phiếu\n2. Để trống ô Mẫu phiếu\n3. Bấm Lưu',
     'Tên: Họp thử 11130; Mẫu phiếu: để trống',
     '- Không lưu, cửa sổ KHÔNG đóng\n'
     '- Hiện chữ lỗi màu đỏ ngay dưới ô Mẫu phiếu: "Bắt buộc phải chọn mẫu phiếu khi bật gán phiếu '
     'tổng hợp kết quả"\n'
     '- Dữ liệu đã nhập (Tên loại meeting) vẫn còn nguyên'),
    ("008", "Lưu loại meeting mới có gán phiếu", "P0",
     'Có sẵn ' + MAU,
     '1. Bấm Thêm mới\n2. Nhập Tên "Họp khách hàng 11130"\n3. Bật công tắc gán phiếu\n'
     '4. Chọn mẫu "Tổng hợp kết quả meeting KH"\n5. Bấm Lưu',
     'Tên: Họp khách hàng 11130; Mẫu phiếu: Tổng hợp kết quả meeting KH',
     '- Lưu thành công, cửa sổ đóng, danh sách có dòng mới\n'
     '- Mở lại để Sửa: công tắc đang BẬT và ô Mẫu phiếu hiện đúng mẫu đã chọn'),
    ("009", "Sửa loại meeting đang gán phiếu sang mẫu phiếu khác", "P0",
     DATA_LM + '. Có thêm mẫu "Tổng hợp kết quả meeting NB" đang Hoạt động',
     '1. Bấm Sửa loại meeting "Họp khách hàng 11130"\n'
     '2. Đổi ô Mẫu phiếu sang "Tổng hợp kết quả meeting NB"\n3. Bấm Lưu',
     'Mẫu phiếu: Tổng hợp kết quả meeting NB',
     '- Lưu thành công\n- Mở lại: hiện mẫu mới\n'
     '- Mở biên bản của meeting thuộc loại này: phiếu dựng theo bộ câu hỏi của mẫu MỚI'),
    ("010", "Tắt công tắc thì bỏ luôn mẫu phiếu đang chọn", "P0",
     DATA_LM,
     '1. Bấm Sửa loại meeting "Họp khách hàng 11130"\n2. Tắt công tắc gán phiếu\n3. Bấm Lưu\n'
     '4. Mở lại để Sửa',
     '—',
     '- Ô Mẫu phiếu biến mất ngay khi tắt công tắc\n'
     '- Sau khi lưu, mở lại: công tắc TẮT và ô Mẫu phiếu trống (không giữ lại mẫu cũ)\n'
     '- Biên bản của meeting thuộc loại này KHÔNG còn phân vùng phiếu'),
    ("011", "Bật lại công tắc sau khi đã tắt", "P1",
     'Loại meeting "Họp khách hàng 11130" vừa bị tắt công tắc ở ca trước',
     '1. Bấm Sửa\n2. Bật lại công tắc gán phiếu\n3. Quan sát ô Mẫu phiếu\n4. Bấm Lưu ngay',
     '—',
     '- Ô Mẫu phiếu hiện lại và đang TRỐNG\n'
     '- Bấm Lưu khi chưa chọn mẫu thì báo lỗi đỏ dưới ô Mẫu phiếu'),
    ("012", "Cấu hình phiếu không phá các trường sẵn có của loại meeting", "P0",
     DATA_LM,
     '1. Bấm Sửa loại meeting\n2. Đổi Mô tả và tắt/bật ô "Có khách hàng"\n3. Bấm Lưu\n4. Mở lại',
     'Mô tả: "Cập nhật 11130"',
     '- Tên, Mô tả, Có khách hàng, Trạng thái lưu đúng như nhập\n'
     '- Cấu hình phiếu vẫn giữ nguyên, không bị xoá về mặc định'),
    ("013", "Xem loại meeting ở chế độ chỉ đọc", "P1",
     DATA_LM,
     '1. Mở loại meeting bằng thao tác Xem',
     '—',
     '- Thấy công tắc đang bật và tên mẫu phiếu\n'
     '- Mọi ô đều không sửa được, nhãn Mẫu phiếu không có dấu * bắt buộc'),
    ("014", "Mẫu phiếu mới phát hành xuất hiện ngay mà không cần tải lại trang", "P1",
     'Vừa chuyển mẫu "Phiếu nháp 11130" từ Nháp sang Hoạt động ở tab trình duyệt khác',
     '1. Quay lại màn Loại meeting đang mở sẵn\n2. Bấm Sửa một loại meeting\n'
     '3. Bật công tắc và mở ô Mẫu phiếu',
     '—',
     '- Danh sách có mẫu "Phiếu nháp 11130" vừa chuyển sang Hoạt động\n'
     '- ⚠️ Không phải nhấn F5 mới thấy'),
    ("015", "Mẫu phiếu đang gán bị chuyển sang Khoá", "P1",
     DATA_LM + '. Sau đó mẫu "Tổng hợp kết quả meeting KH" bị chuyển sang trạng thái Khoá',
     '1. Mở Sửa loại meeting "Họp khách hàng 11130"\n2. Quan sát ô Mẫu phiếu\n3. Bấm Lưu',
     '—',
     '- ⚠️ Ô Mẫu phiếu vẫn hiển thị ĐÚNG TÊN mẫu đang gán, không bị trống\n'
     '- Không tự đổi sang mẫu khác\n'
     '- Bấm Lưu mà không đổi gì thì hệ thống báo mẫu chưa được phát hành, không gán được, và dữ '
     'liệu cũ giữ nguyên'),
]

S3 = [
    ("001", "Nhập đáp án rồi Lưu biên bản", "P0",
     DATA_LM + ". " + DATA_BB + ". " + DATA_MAU,
     '1. Mở tab Biên bản\n2. Chọn Câu 1 = "Có"\n3. Nhập Câu 2 = 500\n'
     '4. Nhập Câu 3 = "Khách quan tâm dòng máy A"\n5. Bấm Lưu',
     'Câu 1: Có; Câu 2: 500; Câu 3: Khách quan tâm dòng máy A',
     '- Lưu thành công, hiện thông báo thành công\n- Không có lỗi đỏ ở phân vùng phiếu'),
    ("002", "Mở lại biên bản thì đáp án còn nguyên", "P0",
     'Vừa lưu biên bản với 3 đáp án ở ca trên',
     '1. Thoát khỏi meeting\n2. Mở lại meeting "TPE.MET.KH.26.0050"\n3. Chuyển sang tab Biên bản',
     '—',
     '- Câu 1 đang chọn "Có"\n- Câu 2 hiện 500\n- Câu 3 hiện "Khách quan tâm dòng máy A"\n'
     '- ⚠️ Đáp án phải khớp ĐÚNG từng câu, không bị lệch sang câu khác'),
    ("003", "Lưu biên bản nhiều lần thì ghi đè, không sinh thêm bản ghi", "P0",
     'Meeting đã có bộ đáp án ở ca trên',
     '1. Mở tab Biên bản\n2. Sửa Câu 2 thành 800\n3. Bấm Lưu\n4. Mở lại biên bản',
     'Câu 2: 800',
     '- Câu 2 hiện 800, các câu khác giữ nguyên\n'
     '- ⚠️ Không xuất hiện thêm bộ đáp án thứ hai, không hiện lặp cùng một câu'),
    ("004", "Lưu biên bản khi bỏ trống toàn bộ phiếu", "P0",
     DATA_LM + ". " + DATA_BB + ', biên bản chưa có đáp án nào',
     '1. Mở tab Biên bản\n2. Không nhập gì trong phân vùng phiếu\n'
     '3. Nhập Nội dung meeting rồi bấm Lưu',
     'Đáp án phiếu: để trống hết',
     '- ⚠️ Lưu THÀNH CÔNG - nút Lưu không bị chặn bởi câu bắt buộc\n'
     '- Mở lại: phiếu vẫn trống, không báo lỗi'),
    ("005", "Số 0 được coi là đã trả lời", "P0",
     DATA_LM + ". " + DATA_BB + '. Câu 1 đã chọn "Có" nên Câu 2 đang hiện',
     '1. Nhập Câu 2 = 0\n2. Bấm Hoàn thành',
     'Câu 2: 0',
     '- ⚠️ Hệ thống KHÔNG báo thiếu Câu 2\n- Biên bản chuyển sang Hoàn thành\n'
     '- Mở lại: Câu 2 hiện 0'),
    ("006", "Đáp án chỉ gồm dấu cách bị coi là chưa trả lời", "P1",
     DATA_LM + '. Mẫu phiếu có câu chữ bắt buộc "Kết luận buổi họp"',
     '1. Nhập vào câu bắt buộc 3 dấu cách\n2. Bấm Hoàn thành',
     'Kết luận buổi họp: "   "',
     '- Hệ thống báo thiếu đúng câu "Kết luận buổi họp"\n'
     '- Biên bản không chuyển sang Hoàn thành'),
    ("007", "Câu chọn nhiều đáp án lưu đủ các lựa chọn", "P1",
     'Mẫu phiếu có câu chọn nhiều "Sản phẩm khách quan tâm" với các lựa chọn: Máy A, Máy B, Máy C',
     '1. Tích chọn Máy A và Máy C\n2. Bấm Lưu\n3. Mở lại biên bản',
     'Sản phẩm khách quan tâm: Máy A, Máy C',
     '- Sau khi mở lại, Máy A và Máy C vẫn đang được tích, Máy B không tích'),
    ("008", "Câu nhập ngày lưu và hiện đúng định dạng", "P1",
     'Mẫu phiếu có câu ngày "Ngày dự kiến ký hợp đồng"',
     '1. Chọn ngày 20/09/2026\n2. Bấm Lưu\n3. Mở lại biên bản',
     'Ngày dự kiến ký hợp đồng: 20/09/2026',
     '- Hiện lại đúng 20/09/2026, không lệch ngày, không hiện định dạng lạ'),
    ("009", "Đáp án của meeting này không lẫn sang meeting khác", "P0",
     'Có 2 meeting cùng thuộc loại "Họp khách hàng 11130": "TPE.MET.KH.26.0050" và '
     '"TPE.MET.KH.26.0051". Meeting 0050 đã nhập Câu 3 = "Khách A"',
     '1. Mở biên bản meeting "TPE.MET.KH.26.0051"\n2. Quan sát phân vùng phiếu\n'
     '3. Nhập Câu 3 = "Khách B" rồi Lưu\n4. Mở lại meeting "TPE.MET.KH.26.0050"',
     'Meeting 0051 Câu 3: Khách B',
     '- ⚠️ Phiếu của meeting 0051 ban đầu hoàn toàn TRỐNG, không kéo theo đáp án của meeting 0050\n'
     '- Meeting 0050 vẫn là "Khách A"'),
    ("010", "Đáp án nhập dở bị cảnh báo khi thoát chưa lưu", "P1",
     DATA_LM + ". " + DATA_BB,
     '1. Mở tab Biên bản\n2. Nhập Câu 3 = "Thử thoát"\n3. Bấm Quay lại mà không lưu',
     'Câu 3: Thử thoát',
     '- Hiện cửa sổ xác nhận cảnh báo còn thay đổi chưa lưu\n'
     '- Chọn ở lại thì vẫn giữ nguyên nội dung vừa nhập'),
    ("011", "Chữ tiếng Việt có dấu và ký tự đặc biệt lưu đúng", "P1",
     DATA_LM + ". " + DATA_BB,
     '1. Nhập Câu 3 = "Khách hàng Nguyễn Hữu Học yêu cầu giảm 5% & giao trước 30/09"\n'
     '2. Lưu và mở lại',
     'Câu 3: Khách hàng Nguyễn Hữu Học yêu cầu giảm 5% & giao trước 30/09',
     '- ⚠️ Hiện đúng nguyên văn, không mất dấu, không hiện ký tự lạ thay cho dấu &'),
]

S4 = [
    ("001", "Câu con ẩn khi câu cha chưa được trả lời", "P0",
     DATA_MAU + ". " + DATA_LM + ". " + DATA_BB + ", biên bản chưa nhập gì",
     '1. Mở tab Biên bản\n2. Quan sát danh sách câu hỏi trong phiếu',
     '—',
     '- Hiện Câu 1 và Câu 3\n- ⚠️ Câu 2 KHÔNG hiện'),
    ("002", 'Trả lời câu cha = "Không" thì câu con vẫn ẩn', "P0",
     DATA_MAU + ". " + DATA_LM + ". " + DATA_BB,
     '1. Chọn Câu 1 = "Không"\n2. Quan sát phiếu',
     'Câu 1: Không',
     '- Câu 2 vẫn KHÔNG hiện\n- Không có thông báo đòi nhập Câu 2'),
    ("003", 'Trả lời câu cha = "Có" thì câu con hiện ngay', "P0",
     DATA_MAU + ". " + DATA_LM + ". " + DATA_BB,
     '1. Chọn Câu 1 = "Có"\n2. Quan sát phiếu',
     'Câu 1: Có',
     '- ⚠️ Câu 2 hiện NGAY, không cần lưu hay tải lại trang\n- Câu 2 có dấu * bắt buộc'),
    ("004", 'Đổi câu cha từ "Có" về "Không" thì câu con ẩn lại', "P0",
     'Đang ở trạng thái Câu 1 = "Có", Câu 2 = 500 (chưa lưu)',
     '1. Đổi Câu 1 sang "Không"\n2. Quan sát phiếu\n3. Đổi lại Câu 1 = "Có"',
     'Câu 1: Không rồi đổi lại Có',
     '- Khi chọn "Không": Câu 2 ẩn đi ngay\n- Khi chọn lại "Có": Câu 2 hiện lại'),
    ("005", "Câu bị ẩn không bị đòi bắt buộc khi Hoàn thành", "P0",
     DATA_MAU + ". " + DATA_LM + ". " + DATA_BB,
     '1. Chọn Câu 1 = "Không"\n2. Bỏ trống Câu 3\n3. Bấm Hoàn thành',
     'Câu 1: Không',
     '- ⚠️ KHÔNG báo thiếu Câu 2 (đang ẩn)\n- Biên bản chuyển sang Hoàn thành'),
    ("006", "Luật ẩn hiện áp dụng cho câu hỏi nằm trong nhóm câu hỏi", "P1",
     'Mẫu phiếu có nhóm "Thông tin đầu tư" chứa câu con có luật rẽ nhánh',
     '1. Mở phiếu\n2. Trả lời câu cha để kích hoạt câu con trong nhóm',
     '—',
     '- Câu con trong nhóm cũng ẩn/hiện đúng như câu ngoài nhóm\n'
     '- Nhóm không bị vỡ bố cục khi câu con ẩn'),
    ("007", "Mẫu phiếu không có luật rẽ nhánh thì hiện đủ mọi câu", "P1",
     'Loại meeting gán mẫu "Tổng hợp kết quả meeting NB" gồm 4 câu, không câu nào có luật rẽ nhánh',
     '1. Mở biên bản meeting thuộc loại đó',
     '—',
     '- Hiện đủ 4 câu ngay từ đầu\n- Không câu nào bị ẩn'),
    ("008", "Đáp án của câu bị ẩn không gây lỗi khi lưu", "P1",
     'Đã nhập Câu 2 = 500 khi Câu 1 = "Có", sau đó đổi Câu 1 sang "Không" nên Câu 2 ẩn',
     '1. Bấm Lưu\n2. Mở lại biên bản',
     'Câu 1: Không',
     '- Lưu thành công, không báo lỗi\n- Mở lại: Câu 1 = "Không", Câu 2 đang ẩn'),
]

S5 = [
    ("001", "Chặn Hoàn thành khi chưa trả lời câu bắt buộc đầu tiên", "P0",
     DATA_MAU + ". " + DATA_LM + ". " + DATA_BB + ", phiếu đang trống",
     '1. Mở tab Biên bản\n2. Bấm nút Hoàn thành',
     '—',
     '- Không chuyển sang Hoàn thành\n'
     '- Hiện thông báo: "Phiếu tổng hợp kết quả meeting còn thiếu câu bắt buộc: Khách hàng có nhu '
     'cầu đầu tư không?"\n'
     '- Màn hình tự chuyển về tab Biên bản\n'
     '- Dưới phân vùng phiếu hiện chữ đỏ: "Còn 1 câu bắt buộc chưa trả lời."'),
    ("002", "Chặn Hoàn thành khi câu con vừa hiện còn trống", "P0",
     DATA_MAU + ". " + DATA_LM + ". " + DATA_BB,
     '1. Chọn Câu 1 = "Có"\n2. Bỏ trống Câu 2\n3. Bấm Hoàn thành',
     'Câu 1: Có; Câu 2: để trống',
     '- Không chuyển sang Hoàn thành\n'
     '- Thông báo nêu đúng tên câu thiếu: "Mức đầu tư dự kiến (triệu đồng)"'),
    ("003", "Thiếu nhiều câu thì liệt kê đủ tên các câu", "P1",
     'Mẫu phiếu có 3 câu bắt buộc đang cùng hiện, đều bỏ trống',
     '1. Bấm Hoàn thành',
     '—',
     '- Thông báo liệt kê đủ tên 3 câu, ngăn cách bằng dấu chấm phẩy\n'
     '- Chữ đỏ dưới phiếu ghi "Còn 3 câu bắt buộc chưa trả lời."'),
    ("004", "Trả lời đủ thì Hoàn thành được", "P0",
     DATA_MAU + ". " + DATA_LM + ". " + DATA_BB,
     '1. Chọn Câu 1 = "Có"\n2. Nhập Câu 2 = 500\n3. Bấm Hoàn thành',
     'Câu 1: Có; Câu 2: 500',
     '- Biên bản chuyển sang trạng thái Hoàn thành\n- Đáp án phiếu được lưu kèm\n'
     '- Mở lại: đủ đáp án, trạng thái Hoàn thành'),
    ("005", "Nhập đáp án thì chữ lỗi đỏ tự mất", "P1",
     'Vừa bị chặn Hoàn thành, đang hiện chữ đỏ "Còn 1 câu bắt buộc chưa trả lời."',
     '1. Chọn Câu 1 = "Có"',
     'Câu 1: Có',
     '- Chữ đỏ dưới phân vùng phiếu biến mất ngay khi vừa trả lời\n'
     '- Không phải bấm Hoàn thành lại mới mất'),
    ("006", "Nút Lưu KHÔNG bị chặn bởi câu bắt buộc", "P0",
     DATA_MAU + ". " + DATA_LM + ". " + DATA_BB + ", phiếu đang trống",
     '1. Nhập Nội dung meeting\n2. Bấm Lưu (không bấm Hoàn thành)',
     '—',
     '- ⚠️ Lưu thành công bình thường\n- Không có thông báo đòi câu bắt buộc'),
    ("007", "Loại meeting không gán phiếu thì Hoàn thành không bị chặn", "P0",
     'Meeting thuộc loại "Họp nội bộ 11130" (không gán phiếu), đã nhập đủ các mục bắt buộc cũ của '
     'biên bản',
     '1. Bấm Hoàn thành',
     '—',
     '- Chuyển sang Hoàn thành bình thường\n'
     '- Không có thông báo nào về phiếu tổng hợp kết quả'),
    ("008", "Các điều kiện Hoàn thành cũ vẫn giữ nguyên", "P0",
     DATA_LM + '. Biên bản chưa điểm danh người tham dự nhưng đã trả lời đủ phiếu',
     '1. Bấm Hoàn thành',
     '—',
     '- ⚠️ Vẫn bị chặn bởi điều kiện cũ (điểm danh) và màn hình chuyển về đúng tab liên quan\n'
     '- Tính năng phiếu không làm mất các kiểm tra cũ'),
]

S6 = [
    ("001", "Phiếu khảo sát nhu cầu đầu tư cũ không bị ảnh hưởng", "P0",
     'Meeting thuộc loại "Họp tìm hiểu & Giới thiệu sản phẩm", loại này KHÔNG bật gán phiếu tổng '
     'hợp kết quả',
     '1. Mở biên bản meeting đó\n'
     '2. Quan sát khối khảo sát nhu cầu đầu tư (Lĩnh vực, Nhóm ngành, mức đầu tư)\n'
     '3. Nhập và lưu như cũ',
     '—',
     '- Khối khảo sát đầu tư hiện và hoạt động y như trước\n'
     '- Không xuất hiện thêm phân vùng phiếu tổng hợp kết quả\n'
     '- Lưu và mở lại: dữ liệu khảo sát đầu tư còn nguyên'),
    ("002", "Loại meeting vừa gán phiếu vừa là loại có khảo sát đầu tư", "P1",
     'Bật công tắc gán phiếu cho loại "Họp tìm hiểu & Giới thiệu sản phẩm"',
     '1. Mở biên bản meeting thuộc loại đó\n2. Quan sát cả 2 khối\n3. Nhập cả hai rồi Lưu\n'
     '4. Mở lại biên bản',
     '—',
     '- Cả khối khảo sát đầu tư CŨ và phân vùng phiếu MỚI cùng hiện, nằm tách biệt\n'
     '- Mở lại còn đủ cả hai, không đè lên nhau'),
    ("003", "Báo cáo chăm sóc khách hàng tiềm năng không đổi số liệu", "P0",
     'Đã ghi lại số liệu báo cáo trước khi bật tính năng để đối chiếu',
     '1. Bật gán phiếu cho một loại meeting\n2. Nhập và lưu phiếu cho một meeting\n'
     '3. Mở lại báo cáo chăm sóc khách hàng tiềm năng với cùng bộ lọc',
     '—',
     '- ⚠️ Số liệu báo cáo KHÔNG đổi so với lúc trước khi bật tính năng'),
    ("004", "Mẫu phiếu thu thập thông tin của dự án vẫn dùng bình thường", "P0",
     'Có dự án đang dùng mẫu phiếu thu thập thông tin để nhập liệu',
     '1. Mở màn nhập phiếu thu thập thông tin của dự án\n2. Nhập, lưu, mở lại',
     '—',
     '- Phiếu của dự án hiển thị và lưu như cũ\n'
     '- Câu hỏi của dự án ẩn/hiện theo luật rẽ nhánh như trước, không đổi cách hoạt động'),
    ("005", "In biên bản meeting không bị lỗi khi loại meeting có gán phiếu", "P1",
     DATA_LM + '. Biên bản đã Hoàn thành và có đủ đáp án phiếu',
     '1. Mở biên bản\n2. Bấm In biên bản\n3. Chọn các phần rồi xem trước bản in',
     '—',
     '- Bản xem trước hiện đúng các phần đã chọn, không vỡ bố cục\n'
     '- Không hiện khung trắng hay ký tự lạ ở vị trí phiếu'),
]

S7 = [
    ("001", "Hai người cùng sửa biên bản một lúc", "P1",
     'Tài khoản A và tài khoản B cùng mở biên bản meeting "TPE.MET.KH.26.0050"',
     '1. A nhập Câu 3 = "Của A" rồi Lưu\n2. B chưa tải lại trang, nhập Câu 3 = "Của B" rồi Lưu\n'
     '3. Mở lại biên bản',
     'Câu 3: Của A rồi Của B',
     '- Lần lưu sau ghi đè lần trước, giá trị cuối cùng là "Của B"\n'
     '- ⚠️ Không sinh 2 bộ đáp án, không văng lỗi treo màn'),
    ("002", "Đổi loại meeting của một meeting đã có đáp án phiếu", "P0",
     'Meeting "TPE.MET.KH.26.0050" thuộc loại "Họp khách hàng 11130", đã lưu đủ 3 đáp án',
     '1. Mở meeting, sang tab Thông tin\n'
     '2. Đổi Loại meeting sang "Họp nội bộ 11130" (không gán phiếu)\n3. Lưu\n'
     '4. Sang tab Biên bản\n5. Đổi ngược lại về "Họp khách hàng 11130"',
     'Loại meeting: Họp nội bộ 11130 rồi đổi lại',
     '- Phân vùng phiếu KHÔNG còn hiện khi đổi sang loại không gán phiếu\n- Không văng lỗi\n'
     '- ⚠️ Đổi ngược lại: đáp án cũ hiện lại đầy đủ'),
    ("003", "Đổi mẫu phiếu của loại meeting khi meeting đã có đáp án cũ", "P0",
     'Meeting đã lưu đáp án theo mẫu "Tổng hợp kết quả meeting KH". Sau đó loại meeting được đổi '
     'sang mẫu "Tổng hợp kết quả meeting NB" có bộ câu hỏi khác hẳn',
     '1. Mở lại biên bản meeting đó\n2. Quan sát phân vùng phiếu\n3. Nhập theo mẫu mới rồi Lưu',
     '—',
     '- Phiếu dựng theo bộ câu hỏi của mẫu MỚI\n'
     '- ⚠️ Màn hình không lỗi, không hiện lẫn câu của mẫu cũ\n'
     '- Nhập và lưu theo mẫu mới được bình thường'),
    ("004", "Loại meeting bị Khóa khi đang có meeting dùng", "P1",
     DATA_LM + '. Chuyển loại meeting đó sang trạng thái Khóa',
     '1. Mở meeting đang dùng loại đó\n2. Sang tab Biên bản\n3. Sang tab Thông tin',
     '—',
     '- ⚠️ Phân vùng phiếu vẫn hiện đúng, không mất\n'
     '- Ô Loại meeting ở tab Thông tin vẫn hiện đúng tên loại meeting đang dùng'),
]

S8 = [
    ("001", "Luồng đầy đủ: cấu hình rồi nhập rồi hoàn thành", "P0",
     'Tài khoản có đủ quyền quản lý danh mục loại meeting và quyền sửa biên bản meeting. Có ' + MAU,
     '1. Vào Danh mục > Mẫu phiếu thu thập thông tin, xác nhận mẫu đang Hoạt động\n'
     '2. Vào Danh mục > Loại meeting, Sửa "Họp khách hàng 11130", bật công tắc, chọn mẫu, Lưu\n'
     '3. Vào Giao việc > Meeting, tạo meeting mới loại "Họp khách hàng 11130", chốt lịch\n'
     '4. Mở tab Biên bản, bấm Hoàn thành khi phiếu còn trống\n'
     '5. Trả lời Câu 1 = "Có", nhập Câu 2 = 500, Câu 3 = "Chốt gặp lại tuần sau"\n'
     '6. Bấm Hoàn thành\n7. Mở lại meeting',
     'Câu 1: Có; Câu 2: 500; Câu 3: Chốt gặp lại tuần sau',
     '- Bước 4: bị chặn, thông báo thiếu Câu 1, có chữ đỏ dưới phiếu\n'
     '- Bước 5: Câu 2 hiện ra ngay sau khi chọn "Có"\n'
     '- Bước 6: chuyển Hoàn thành thành công\n'
     '- Bước 7: trạng thái Hoàn thành, 3 đáp án hiện lại đúng nguyên vẹn'),
    ("002", "Luồng gỡ cấu hình rồi bật lại", "P1",
     'Loại meeting "Họp khách hàng 11130" đang gán phiếu, có meeting đã lưu đáp án',
     '1. Tắt công tắc gán phiếu ở loại meeting, Lưu\n'
     '2. Mở biên bản meeting cũ, sửa Nội dung meeting rồi Lưu\n'
     '3. Bật lại công tắc và chọn lại đúng mẫu cũ\n'
     '4. Mở lại biên bản meeting đó',
     '—',
     '- Bước 2: biên bản không hiện phiếu, lưu bình thường\n'
     '- Bước 4: phân vùng phiếu hiện lại, ⚠️ đáp án cũ vẫn còn nguyên, không bị mất'),
    ("003", "Luồng nhiều meeting cùng loại", "P1",
     'Loại meeting "Họp khách hàng 11130" đang gán phiếu; tạo 3 meeting cùng loại',
     '1. Nhập đáp án khác nhau cho từng meeting rồi Lưu\n2. Mở lần lượt từng meeting kiểm tra',
     'Meeting 1 Câu 3: KH A; Meeting 2: KH B; Meeting 3: KH C',
     '- Mỗi meeting hiện đúng đáp án của chính nó\n'
     '- ⚠️ Không meeting nào bị lẫn đáp án của meeting khác'),
]

SECTIONS = [
    ("I", "HIỂN THỊ & TRUY CẬP", S1),
    ("II", "CẤU HÌNH GÁN PHIẾU TRÊN LOẠI MEETING", S2),
    ("III", "NHẬP & LƯU ĐÁP ÁN PHIẾU TRONG BIÊN BẢN", S3),
    ("IV", "ẨN/HIỆN CÂU HỎI THEO LUẬT RẼ NHÁNH", S4),
    ("V", "CHẶN HOÀN THÀNH KHI THIẾU CÂU BẮT BUỘC", S5),
    ("VI", "KHÔNG ẢNH HƯỞNG CHỨC NĂNG CŨ", S6),
    ("VII", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S7),
    ("VIII", "LUỒNG ĐẦU CUỐI", S8),
]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase.xlsx")

build(output_file=OUT, sheet_name="Trang tính1", feature_name=FEATURE, module_name=MODULE,
      description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
