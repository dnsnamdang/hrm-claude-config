# -*- coding: utf-8 -*-
"""Redmine #11130 (ghi chu QA 40915) - gen lai khoi TC "UPDATE RETEST LOI (12/09/2026)" tren sheet
Testcase _ Meeting (dong 422-458):
  1. Bo sung nhom TC hien thi bo cau hoi khao sat cua loai meeting "Hop tim hieu & Gioi thieu san pham".
  2. Viet lai cot G (Tien dieu kien) rieng cho tung TC.
Cac cot khac giu nguyen QA da ghi (doc tu CSV export cua sheet).

Chay: python gen_tc_qa_11130.py <duong_dan_sheet.csv> <file_ra.xlsx>
"""
import csv, sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side

SRC, OUT = sys.argv[1], sys.argv[2]
FIRST, LAST = 422, 458  # dong tren sheet goc (1-based)

LM = '"Họp tìm hiểu & Giới thiệu sản phẩm"'
MT = f'Meeting thuộc loại {LM}'
KS = 'mục "1/ Khảo sát nhu cầu khách hàng"'
DU_HT = ('đã qua giờ bắt đầu (nút Hoàn thành bấm được), đã điểm danh đủ thành viên, '
         'mục "Các nội dung khác" đã có ít nhất 1 dòng nhập đủ, đã nhập Kết luận')
CHU_TRI = 'Tài khoản đăng nhập là người chủ trì.'
DM_CN = 'Danh mục có lĩnh vực "Công nghiệp" kèm ít nhất 1 nhóm ngành đang Hoạt động.'

# ---------------------------------------------------------------- cot G moi cho TC cu
NEW_G = {
    'TC_03.001': f'{MT}, trạng thái Chốt lịch, đang mở màn Sửa, tab Biên bản. {KS} chưa có đáp án nào. {DM_CN} {CHU_TRI}',
    'TC_03.002': 'Đã làm xong TC_03.001: meeting đã lưu đáp án khảo sát (Câu 1 = Có, 1 nhóm ngành thuộc "Công nghiệp" '
                 'có mức đầu tư 500 và thời gian khánh thành, Câu 4 = Có). Đã thoát ra màn danh sách.',
    'TC_03.003': f'{MT} đã lưu đáp án khảo sát, trong đó nhóm ngành thuộc lĩnh vực "Công nghiệp" đang có mức đầu tư = 500. '
                 'Đang mở màn Sửa của meeting đó.',
    'TC_03.004': f'{MT} vừa tạo, chưa trả lời câu nào trong {KS}. Đang mở màn Sửa, tab Biên bản.',
    'TC_03.005': f'{MT}, trạng thái Chốt lịch, {DU_HT}. Trong khảo sát đã có Câu 1 = Có, Câu 4 đã trả lời, đã chọn 1 nhóm ngành '
                 'thuộc "Công nghiệp" và đã chọn thời gian khánh thành; chỉ còn ô Mức đầu tư dự kiến trống.',
    'TC_03.006': f'{MT}, trạng thái Chốt lịch, đã qua giờ bắt đầu, đã điểm danh đủ, khảo sát và "Các nội dung khác" đã nhập đủ. '
                 'Chỉ còn ô "Kết luận" ở tab Biên bản đang trống để kiểm tra nhập toàn dấu cách.',
    'TC_03.007': f'{MT}, đang mở màn Sửa, Câu 1 chưa trả lời. Danh mục có lĩnh vực "Gara ô tô" và "Công nghiệp", '
                 'mỗi lĩnh vực có ít nhất 1 nhóm ngành đang Hoạt động.',
    'TC_03.008': f'{MT}, đang mở màn Sửa, Câu 1 = Có, đã chọn 1 nhóm ngành thuộc "Công nghiệp" (bảng Câu 3 đang hiện ô '
                 'Thời gian khánh thành dự án trống). Ngày chọn phải từ hôm nay trở đi vì ngày quá khứ bị khoá.',
    'TC_03.009': f'Có 2 meeting A và B cùng thuộc loại {LM}, cùng trạng thái Chốt lịch, cả 2 chưa có đáp án khảo sát. '
                 'Tài khoản đăng nhập là người chủ trì của cả 2 meeting.',
    'TC_03.010': f'{MT}, mở màn Sửa từ màn danh sách, chưa thay đổi gì trên màn (chưa có dữ liệu chưa lưu).',
    'TC_03.011': f'{MT}, đang mở màn Sửa, tab Biên bản. Khối khảo sát không có ô nhập chữ tự do nên dùng ô '
                 '"Nội dung / Vấn đề trao đổi" ở mục "Các nội dung khác" để nhập chữ.',
    'TC_04.001': f'{MT} chưa trả lời Câu 1 (nút gạt Có/Không chưa chọn bên nào). Đang mở màn Sửa, tab Biên bản.',
    'TC_04.002': f'{MT}, Câu 1 đang chưa trả lời. Đang mở màn Sửa, tab Biên bản.',
    'TC_04.003': f'{MT}, Câu 1 đang chưa trả lời hoặc đang là "Không". Đang mở màn Sửa, tab Biên bản. {DM_CN}',
    'TC_04.004': f'{MT}, đang mở màn Sửa, Câu 1 chưa trả lời. {DM_CN}',
    'TC_04.005': f'{MT}, trạng thái Chốt lịch, {DU_HT}. Khảo sát chưa trả lời câu nào. {CHU_TRI}',
    'TC_04.006': f'{MT}, đang mở màn Sửa, Câu 1 = Có. Danh mục có 1 lĩnh vực chứa từ 2 nhóm ngành Hoạt động trở lên '
                 '(lĩnh vực là câu cha, nhóm ngành là câu con).',
    'TC_04.007': f'{MT} vừa tạo, khảo sát chưa trả lời câu nào. Đang mở màn Sửa, tab Biên bản.',
    'TC_04.008': f'{MT}, trạng thái Chốt lịch, đang mở màn Sửa. Câu 1 chưa trả lời, Câu 4 đã trả lời, '
                 f'meeting chưa từng lưu dữ liệu đầu tư nào. {DM_CN}',
    'TC_05.001': f'{MT}, trạng thái Chốt lịch, đã qua giờ bắt đầu, đã điểm danh đủ, đã nhập Kết luận. Khảo sát: Câu 1 = "Không", '
                 'Câu 4 chưa trả lời. Mục "Các nội dung khác" chưa có dòng nào. {CHU_TRI}',
    'TC_05.002': f'{MT}, trạng thái Chốt lịch, {DU_HT}. Khảo sát: Câu 1 = Có, Câu 4 đã trả lời, Câu 2 đã chọn 1 lĩnh vực '
                 'nhưng chưa chọn nhóm ngành nào.',
    'TC_05.003': f'{MT}, trạng thái Chốt lịch, đã qua giờ bắt đầu, đã điểm danh đủ, đã nhập Kết luận. Khảo sát: Câu 1 và Câu 4 '
                 'đều chưa trả lời. Mục "Các nội dung khác" chưa có dòng nào (tổng cộng 3 mục thiếu).',
    'TC_05.004': f'{MT}, trạng thái Chốt lịch, {DU_HT}. Khảo sát chưa trả lời câu nào. {DM_CN} {CHU_TRI}',
    'TC_05.005': 'Vừa bấm Hoàn thành ở meeting loại ' + LM + ' và bị chặn vì Câu 1 chưa trả lời; '
                 'dưới Câu 1 đang hiện chữ đỏ báo bắt buộc.',
    'TC_05.006': f'{MT}, đang mở màn Sửa. Khảo sát còn Câu 1 và Câu 4 chưa trả lời.',
    'TC_05.007': f'Meeting thuộc loại meeting KHÁC {LM} (ví dụ Họp nội bộ), trạng thái Chốt lịch, {DU_HT}.',
    'TC_05.008': f'{MT}, trạng thái Chốt lịch, đã qua giờ bắt đầu. Khảo sát và "Các nội dung khác" đã nhập đủ, đã nhập Kết luận. '
                 'Còn ít nhất 1 thành viên chưa điểm danh.',
    'TC_06.001': f'{MT} được tạo và lưu đáp án khảo sát TRƯỚC đợt cập nhật #11130 (dữ liệu cũ có sẵn trên hệ thống).',
    'TC_06.002': f'{MT} đã lưu đáp án khảo sát. Lưu ý: chức năng gán phiếu trên Danh mục Loại meeting đã BỎ, '
                 'loại meeting này chỉ có 1 khối khảo sát.',
    'TC_06.003': 'Đã chụp lại số liệu báo cáo "Báo cáo kết quả chăm sóc khách hàng tiềm năng" tại một khoảng thời gian cố định. '
                 f'Có 1 {MT[0].lower() + MT[1:]} nằm trong khoảng đó, chưa có đáp án khảo sát.',
    'TC_06.004': 'Có 1 dự án đang dùng mẫu phiếu thu thập thông tin, đã có dữ liệu nhập trước đợt cập nhật #11130.',
    'TC_06.005': f'{MT}, trạng thái Hoàn thành, đã lưu đủ đáp án khảo sát (Câu 1 = Có, ít nhất 1 nhóm ngành có mức đầu tư '
                 'và thời gian, Câu 4 đã trả lời).',
    'TC_07.001': f'{MT}, trạng thái Chốt lịch. Tài khoản A (người chủ trì) và tài khoản B (có quyền sửa meeting) cùng mở '
                 'màn Sửa của meeting này trên 2 trình duyệt.',
    'TC_07.002': f'{MT}, đã lưu đủ đáp án khảo sát, trạng thái còn cho sửa tab Thông tin. '
                 'Danh mục có loại meeting khác đang Hoạt động (ví dụ Họp nội bộ).',
    'TC_07.003': f'{MT} đã lưu đáp án khảo sát. Lưu ý: chức năng chọn mẫu phiếu cho Loại meeting đã BỎ, '
                 'bộ câu hỏi khảo sát là cố định.',
    'TC_07.004': f'{MT} đã lưu đáp án khảo sát. Lưu ý: {LM} là loại meeting hệ thống, Danh mục Loại meeting '
                 'không cho sửa/xoá/khoá loại này.',
}
# TC_05.008: cot E dang bi dan nham noi dung tien dieu kien -> tra lai ten chuc nang
NEW_E = {'TC_05.008': 'Phiếu đã trả lời đủ nhưng còn thiếu điều kiện Hoàn thành cũ (chưa điểm danh)'}

# ---------------------------------------------------------------- nhom TC moi: hien thi bo cau hoi
GRP_B, GRP_C = 'Phiếu tổng hợp kết quả meeting', 'HIỂN THỊ BỘ CÂU HỎI KHẢO SÁT'
VAO_BB = '1. Vào Meetings > Lịch meeting, mở màn Sửa meeting\n2. Chọn tab "Biên bản"'
NEW_TC = [
    ('Hiển thị mục Khảo sát nhu cầu khách hàng với loại meeting khảo sát', 'P0',
     f'{MT}, trạng thái Chốt lịch. {CHU_TRI}',
     VAO_BB + '\n3. Quan sát khối "IV/ Nội dung meeting"', '',
     '- Khối "IV/ Nội dung meeting" có 3 mục theo thứ tự: "1/ Khảo sát nhu cầu khách hàng", "2/ Các nội dung khác", '
     '"3/ Tài liệu đính kèm"\n- Mục khảo sát nằm đầu tiên, có đường kẻ ngăn với mục "2/ Các nội dung khác"'),
    ('Loại meeting khác không hiển thị mục khảo sát', 'P0',
     f'Meeting thuộc loại meeting KHÁC {LM} (ví dụ Họp nội bộ), trạng thái Chốt lịch.',
     VAO_BB + '\n3. Quan sát khối "IV/ Nội dung meeting"', '',
     '- KHÔNG có mục "Khảo sát nhu cầu khách hàng"\n- Các mục đánh số lại: "1/ Các nội dung khác", "2/ Tài liệu đính kèm"'),
    ('Trạng thái ban đầu của bộ câu hỏi khi chưa trả lời', 'P0',
     f'{MT} vừa tạo, khảo sát chưa trả lời câu nào.',
     VAO_BB + '\n3. Quan sát mục "1/ Khảo sát nhu cầu khách hàng"', '',
     '- Hiện "Câu 1. Anh/Chị có nhu cầu đầu tư trong thời gian tới? *" kèm nút gạt Có / Không, chưa chọn bên nào\n'
     '- Hiện "Câu 4. Anh/Chị có nhu cầu về dịch vụ sửa chữa bảo dưỡng/bảo trì máy móc thiết bị? *" kèm nút gạt Có / Không, chưa chọn bên nào\n'
     '- Câu 2 và Câu 3 CHƯA hiển thị'),
    ('Chọn Câu 1 = Có thì hiển thị Câu 2 chọn lĩnh vực và nhóm ngành', 'P0',
     f'{MT}, đang mở tab Biên bản, Câu 1 chưa trả lời. {DM_CN}',
     '1. Tại Câu 1, bấm "Có"\n2. Quan sát phần ngay dưới Câu 1', 'Câu 1: Có',
     '- Hiện ngay "Câu 2. Anh/Chị quan tâm tới lĩnh vực và nhóm ngành nào? *" kèm chú thích xám '
     '"(chọn nhiều — chọn nhóm ngành sẽ tự thêm lĩnh vực tương ứng)"\n'
     '- 2 ô nằm cùng hàng: "Lĩnh vực Công ty kinh doanh *" (gợi ý "Chọn lĩnh vực Công ty kinh doanh") và '
     '"Nhóm ngành *" (gợi ý "Chọn nhóm ngành")\n- Câu 3 vẫn chưa hiển thị vì chưa chọn nhóm ngành nào'),
    ('Giải thích nhóm ngành bằng icon ⓘ', 'P2',
     f'{MT}, Câu 1 = Có, Câu 2 đang hiển thị.',
     '1. Rê chuột vào icon ⓘ cạnh nhãn "Nhóm ngành"', '',
     '- Hiện gợi ý: "Nhóm ngành: Là ngành kỹ thuật/công nghệ do TPE cung cấp, được phân chia theo tính chất công nghệ."\n'
     '- 2 ô Lĩnh vực và Nhóm ngành thẳng hàng nhau, không ô nào bị lệch xuống'),
    ('Danh sách lựa chọn của ô Lĩnh vực Công ty kinh doanh', 'P1',
     f'{MT}, Câu 1 = Có. Danh mục có: lĩnh vực X đang Hoạt động có nhóm ngành, lĩnh vực Y đang Hoạt động nhưng '
     'chưa có nhóm ngành nào, lĩnh vực Z đã Khoá.',
     '1. Bấm vào ô "Lĩnh vực Công ty kinh doanh"\n2. Gõ một phần tên lĩnh vực X vào ô "Tìm kiếm..."', 'Lĩnh vực X, Y, Z',
     '- Danh sách chỉ có lĩnh vực X, KHÔNG có Y (chưa có nhóm ngành) và Z (đã khoá)\n'
     '- Ô "Tìm kiếm..." lọc đúng theo chữ vừa gõ\n- Chọn được nhiều lĩnh vực, mỗi lĩnh vực hiện thành 1 thẻ trong ô'),
    ('Danh sách lựa chọn của ô Nhóm ngành gom theo lĩnh vực', 'P0',
     f'{MT}, Câu 1 = Có. Danh mục có lĩnh vực "Công nghiệp" với 3 nhóm ngành Hoạt động.',
     '1. Bấm vào ô "Nhóm ngành"\n2. Bấm vào tên lĩnh vực "Công nghiệp" để mở/đóng nhóm\n3. Tích 1 nhóm ngành của "Công nghiệp"',
     'Lĩnh vực: Công nghiệp',
     '- Nhóm ngành hiện gom theo từng lĩnh vực, bấm tên lĩnh vực thì mở/đóng được danh sách con\n'
     '- Cạnh tên lĩnh vực có số đếm dạng "1/3" (đã chọn / tổng nhóm ngành)\n'
     '- Tích nhóm ngành thì lĩnh vực "Công nghiệp" tự được thêm vào ô "Lĩnh vực Công ty kinh doanh"'),
    ('Chọn nhóm ngành thì hiển thị Câu 3 nhập mức đầu tư và thời gian', 'P0',
     f'{MT}, Câu 1 = Có, Câu 2 chưa chọn nhóm ngành nào. {DM_CN}',
     '1. Tại ô "Nhóm ngành", tích 1 nhóm ngành thuộc "Công nghiệp"\n2. Quan sát phần dưới Câu 2', 'Lĩnh vực: Công nghiệp',
     '- Hiện "Câu 3. Mức đầu tư và thời gian dự kiến triển khai? *"\n'
     '- Dòng tóm tắt xám: "Đang chọn: 1 lĩnh vực · 1 nhóm ngành"\n'
     '- Bảng có 4 cột: "STT", "Lĩnh vực / Nhóm ngành", "Mức đầu tư dự kiến (VNĐ) *", "Thời gian khánh thành dự án *"'),
    ('Bố cục bảng Câu 3 khi chọn nhiều lĩnh vực', 'P1',
     f'{MT}, Câu 1 = Có. Danh mục có lĩnh vực "Gara ô tô" và "Công nghiệp", mỗi lĩnh vực có ít nhất 2 nhóm ngành Hoạt động.',
     '1. Chọn 2 nhóm ngành thuộc "Công nghiệp" và 1 nhóm ngành thuộc "Gara ô tô"\n2. Quan sát bảng Câu 3',
     '3 nhóm ngành thuộc 2 lĩnh vực',
     '- Dòng tóm tắt: "Đang chọn: 2 lĩnh vực · 3 nhóm ngành"\n- Dòng đầu bảng là "Tổng:" in đậm\n'
     '- Mỗi lĩnh vực là 1 dòng in đậm đánh số La Mã (I, II); nhóm ngành nằm dưới, thụt vào, đánh số 1, 2 trong từng lĩnh vực\n'
     '- Mỗi dòng nhóm ngành có ô nhập mức đầu tư, ô chọn ngày và icon thùng rác ở cuối dòng'),
    ('Tự cộng tiền theo lĩnh vực và tổng', 'P1',
     f'{MT}, bảng Câu 3 đang có 2 nhóm ngành thuộc "Công nghiệp" và 1 nhóm ngành thuộc "Gara ô tô".',
     '1. Nhập mức đầu tư 2 nhóm ngành "Công nghiệp" lần lượt 1000000 và 2500000\n'
     '2. Nhập mức đầu tư nhóm ngành "Gara ô tô" là 500000\n3. Quan sát dòng lĩnh vực và dòng "Tổng:"',
     '1000000; 2500000; 500000',
     '- Ô nhập tự định dạng: 1,000,000 / 2,500,000 / 500,000\n'
     '- Dòng lĩnh vực "Công nghiệp" = 3,500,000; dòng "Gara ô tô" = 500,000\n- Dòng "Tổng:" = 4,000,000\n'
     '- Các số căn phải thẳng một mốc'),
    ('Ô Thời gian khánh thành dự án chặn ngày quá khứ', 'P1',
     f'{MT}, bảng Câu 3 đang có 1 nhóm ngành chưa chọn ngày.',
     '1. Bấm vào ô "Thời gian khánh thành dự án"\n2. Thử chọn ngày hôm qua\n3. Chọn ngày hôm nay', '',
     '- Các ngày trước hôm nay bị mờ, không chọn được\n- Chọn hôm nay thì ô hiện đúng dạng DD/MM/YYYY'),
    ('Đổi Câu 1 từ Có sang Không khi đã chọn nhóm ngành', 'P0',
     f'{MT}, Câu 1 = Có, đã chọn 1 nhóm ngành và nhập mức đầu tư.',
     '1. Bấm "Không" ở Câu 1\n2. Bấm "Hủy" ở cửa sổ xác nhận\n3. Bấm lại "Không", lần này bấm "Xoá"', '',
     '- Hiện cửa sổ "Xoá dữ liệu lĩnh vực/nhóm ngành đã chọn?" nội dung "Chuyển sang "Không" sẽ xoá toàn bộ lĩnh vực, '
     'nhóm ngành và mức đầu tư/thời gian đã nhập ở câu 2. Bạn có chắc chắn?"\n'
     '- Bấm "Hủy": Câu 1 giữ "Có", dữ liệu Câu 2 và Câu 3 còn nguyên\n'
     '- Bấm "Xoá": Câu 1 = Không, Câu 2 và Câu 3 ẩn đi, chọn lại "Có" thì Câu 2 trống'),
    ('Xoá dòng nhóm ngành trên bảng Câu 3', 'P1',
     f'{MT}, bảng Câu 3 có 2 nhóm ngành cùng thuộc "Công nghiệp": dòng 1 đã nhập mức đầu tư, dòng 2 chưa nhập gì.',
     '1. Bấm icon thùng rác ở dòng 2\n2. Bấm icon thùng rác ở dòng 1, rồi bấm "Xoá" ở cửa sổ xác nhận\n'
     '3. Quan sát ô "Lĩnh vực Công ty kinh doanh"', '',
     '- Dòng 2 (chưa nhập) bị xoá ngay, không hỏi\n'
     '- Dòng 1 (đã nhập) hiện cửa sổ "Xoá dữ liệu đã nhập?" nội dung "Xoá nhóm ngành "<tên>" sẽ mất mức đầu tư/thời gian '
     'đã nhập của dòng này. Bạn có chắc chắn?"\n'
     '- Xoá hết nhóm ngành: Câu 3 ẩn đi, lĩnh vực "Công nghiệp" VẪN còn ở ô "Lĩnh vực Công ty kinh doanh"'),
    ('Bỏ chọn lĩnh vực đang có nhóm ngành', 'P1',
     f'{MT}, Câu 2 đã chọn lĩnh vực "Công nghiệp" kèm 2 nhóm ngành, chưa nhập mức đầu tư/thời gian.',
     '1. Bấm dấu x trên thẻ "Công nghiệp" ở ô "Lĩnh vực Công ty kinh doanh"\n2. Đọc cửa sổ xác nhận rồi bấm "Xoá"', '',
     '- Hiện cửa sổ "Xoá lĩnh vực/nhóm ngành đã chọn?" nội dung "Bỏ chọn lĩnh vực "Công nghiệp" sẽ xoá 2 nhóm ngành đã chọn. '
     'Bạn có chắc chắn?"\n- Nếu đã nhập mức đầu tư/thời gian: tiêu đề là "Xoá dữ liệu đã nhập?" và câu có thêm '
     '"kèm mức đầu tư/thời gian đã nhập"\n- Bấm "Xoá": lĩnh vực và 2 nhóm ngành bị bỏ, bảng Câu 3 mất 2 dòng tương ứng'),
    ('Hiển thị khảo sát ở màn Tạo mới khi chọn loại meeting khảo sát', 'P0',
     'Tài khoản có quyền tạo meeting.',
     f'1. Vào Meetings > Lịch meeting > Thêm mới\n2. Tab "Thông tin": chọn Loại meeting = {LM}\n'
     '3. Chuyển sang tab "Biên bản"\n4. Quay lại tab "Thông tin", đổi Loại meeting sang loại khác, rồi sang lại tab "Biên bản"',
     f'Loại meeting: {LM} rồi đổi sang Họp nội bộ',
     '- Bước 3: mục "1/ Khảo sát nhu cầu khách hàng" hiện ngay, không cần lưu\n'
     '- Bước 4: mục khảo sát ẩn đi, các mục đánh số lại "1/ Các nội dung khác", "2/ Tài liệu đính kèm"'),
    ('Hiển thị khảo sát ở màn Chi tiết (chỉ xem)', 'P0',
     f'{MT}, đã lưu đáp án khảo sát (Câu 1 = Có, 2 nhóm ngành có mức đầu tư và thời gian, Câu 4 = Không).',
     '1. Vào Meetings > Lịch meeting, bấm vào tên meeting để mở màn Chi tiết\n2. Chọn tab "Biên bản"', '',
     '- Hiện đủ Câu 1 đến Câu 4 với đúng đáp án đã lưu\n'
     '- Nút gạt Có/Không, ô chọn lĩnh vực/nhóm ngành, ô tiền, ô ngày đều bị khoá, không sửa được\n'
     '- Bảng Câu 3 KHÔNG có icon thùng rác'),
    ('Popup In / Xuất Excel có lựa chọn Khảo sát nhu cầu khách hàng', 'P1',
     f'Có 1 {MT[0].lower() + MT[1:]} và 1 meeting loại khác, cả 2 đã lưu.',
     '1. Mở tab "Biên bản" của meeting loại khảo sát, bấm "In"\n2. Xem danh sách phần trong cửa sổ "Cấu hình in biên bản"\n'
     '3. Làm lại với meeting loại khác', '',
     '- Meeting loại khảo sát: danh sách phần có "Khảo sát nhu cầu khách hàng"\n'
     '- Meeting loại khác: KHÔNG có "Khảo sát nhu cầu khách hàng"'),
]

# ---------------------------------------------------------------- doc sheet goc + ghep
rows = list(csv.reader(open(SRC, encoding='utf-8')))
header = rows[5][:20]
block = [r[:20] + [''] * (20 - len(r[:20])) for r in rows[FIRST - 1:LAST]]

out_rows = []  # (values, kind) kind: title|new|changed
out_rows.append((block[0], 'title'))
for i, (name, pri, pre, steps, data, exp) in enumerate(NEW_TC, 1):
    v = [''] * 20
    v[1], v[2] = (GRP_B, GRP_C) if i == 1 else ('', '')
    v[3], v[4], v[5], v[6], v[7], v[8], v[9] = f'TC_11.{i:03d}', name, pri, pre, steps, data, exp
    v[14] = 'Bổ sung 17/10/2026 theo ghi chú QA #11130'
    out_rows.append((v, 'new'))

seen = set()
for r in block[1:]:
    tc = r[3].strip()
    if tc in NEW_G:
        r = list(r)
        r[6] = NEW_G[tc]
        if tc in NEW_E:
            r[4] = NEW_E[tc]
        seen.add(tc)
        out_rows.append((r, 'changed'))
    else:
        out_rows.append((r, ''))
missing = set(NEW_G) - seen
assert not missing, f'Khong thay TC trong sheet: {missing}'

# ---------------------------------------------------------------- ghi xlsx
wb = Workbook()
ws = wb.active
ws.title = 'TC 11130 gen lai'
thin = Side(style='thin', color='BFBFBF')
bd = Border(left=thin, right=thin, top=thin, bottom=thin)
F_NEW = PatternFill('solid', fgColor='E2F0D9')
F_CHG = PatternFill('solid', fgColor='FFF2CC')
F_HEAD = PatternFill('solid', fgColor='D9E1F2')
ws.append(header)
for c in ws[1]:
    c.font, c.fill, c.border = Font(bold=True), F_HEAD, bd
    c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
for vals, kind in out_rows:
    ws.append(vals)
    row = ws[ws.max_row]
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical='top')
        c.border = bd
    if kind == 'title':
        for c in row:
            c.font = Font(bold=True)
    elif kind == 'new':
        for c in row[:10]:
            c.fill = F_NEW
    elif kind == 'changed':
        row[6].fill = F_CHG
        if vals[3].strip() in NEW_E:
            row[4].fill = F_CHG
widths = [14, 18, 20, 11, 34, 7, 45, 45, 22, 50, 30, 10, 10, 10, 26, 10, 10, 10, 10, 22]
for i, w in enumerate(widths):
    ws.column_dimensions[chr(65 + i)].width = w
ws.freeze_panes = 'E2'

# Sheet 2: nhung cho cot khac (ngoai G) dang lech he thong - de QA quyet
notes = wb.create_sheet('Ghi chu ra soat')
notes.append(['TC', 'Cột', 'Vấn đề', 'Đề xuất'])
NOTES = [
    ('TC_03.001, TC_03.008', 'H, I', 'Ngày 20/09/2026 đã qua so với hôm nay; ô Thời gian khánh thành dự án khoá ngày quá khứ nên không chọn được.', 'Đổi sang ngày từ hôm nay trở đi.'),
    ('TC_03.001, 03.007', 'H, I', 'Hệ thống chọn NHÓM NGÀNH (Câu 2) rồi nhập tiền/ngày ở Câu 3, không nhập tiền trực tiếp cho lĩnh vực. Test data ghi "Khách quan tâm dòng máy A", "Máy A, Máy C" không có trên màn.', 'Sửa bước/test data theo Lĩnh vực > Nhóm ngành.'),
    ('TC_03.006, TC_03.011, TC_07.001', 'H, I, J', 'Khối khảo sát không có ô nhập chữ (chỉ có Có/Không, chọn lĩnh vực/nhóm ngành, tiền, ngày). "Câu 3" hiện là bảng mức đầu tư.', 'Dùng ô Kết luận / Nội dung trao đổi, hoặc đổi sang ô tiền.'),
    ('TC_04.007', 'J', 'Expected "Hiện đủ 4 câu ngay từ đầu" sai: ban đầu chỉ hiện Câu 1 và Câu 4 (đã có TC_11.003).', 'Sửa expected hoặc bỏ TC.'),
    ('TC_05.001, TC_05.005', 'J', 'Hệ thống không có dòng "Còn 1 câu bắt buộc chưa trả lời."; chữ đỏ hiện dưới từng câu thiếu là "Bắt buộc phải nhập".', 'Sửa expected.'),
    ('TC_05.008', 'E, J', 'Cột E đang bị dán tiền điều kiện (đã trả lại tên chức năng). Expected "Chuyển sang Hoàn thành bình thường" sai: thiếu điểm danh thì bị chặn, thông báo có "Nhân sự tham gia (còn N thành viên chưa điểm danh)".', 'Sửa expected.'),
    ('TC_06.001', 'G (cũ)', 'G cũ ghi "loại này KHÔNG bật gán phiếu" - công tắc gán phiếu đã bỏ.', 'Đã viết lại G.'),
    ('TC_06.002, TC_07.003', 'E, H, J', 'Kiểm tra chức năng gán/đổi mẫu phiếu cho Loại meeting - chức năng này đã BỎ (#11130 ghi "BỎ").', 'Đề xuất bỏ 2 TC hoặc ghi Not Executed.'),
    ('TC_07.004', 'E, H, J', 'Loại "Họp tìm hiểu & Giới thiệu sản phẩm" là loại hệ thống, không khoá được.', 'Đề xuất bỏ TC, hoặc đổi thành kiểm tra không có nút Khoá ở loại này.'),
]
for n in NOTES:
    notes.append(list(n))
for c in notes[1]:
    c.font, c.fill = Font(bold=True), F_HEAD
for row in notes.iter_rows(min_row=1):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical='top')
        c.border = bd
for col, w in zip('ABCD', (22, 10, 80, 40)):
    notes.column_dimensions[col].width = w

wb.save(OUT)
print('OK', OUT, 'moi:', len(NEW_TC), 'sua G:', len(seen), 'tong dong:', len(out_rows))
